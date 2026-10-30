"""Sci-Hub fetcher for pre-2021 papers of the S7 retrieval queue that the OA / browser routes could not cache.

Landing page: https://sci-hub.reatk.com/<doi> embeds the PDF as https://sci.bban.top/pdf/<doi>.pdf (the same URL as
its `location.href=...?download=true` link), so one landing request yields the direct PDF URL. The site puts a
Cloudflare Turnstile gate in front of the landing pages after a burst of requests; once solved it sets the cookie
`scihub_verified=1` (30 min), which this script reads from cache/literature/scihub_cookies.json. `--warm` opens a
headed Chrome (system Chrome, profile cache/browser_profiles/scihub_chromium), loads the DOI that triggered the gate
and dumps the cookie; every later run reuses it until it expires. A verification page (or HTTP 403/429/503) arms the
breaker logs/.lit_scihub_blocked.json and the run stops; remove the file by hand after refreshing the cookie.

Politeness: one landing request every --gap (default 20-30 s, random) and the same spacing on sci.bban.top for the PDF,
so a run is ~1 request pair per 20 s; a global lock (logs/.lit_scihub.lock) keeps one run at a time; HTTP 404 or an
empty embed (no sci-hub copy) is `not_found`, never retried in the same run.

Cache: references/<paper_id>/source.pdf (.part, %PDF magic + Content-Length + >= 20 kB checked) and source.json
(route scihub, redistribution restricted_local_only) when absent. Status per attempt is appended to
logs/lit_fetch_status.jsonl (shared with lit_fetch_oa.py / lit_fetch_browser.py); run log logs/lit_fetch_scihub_<ts>.

Candidates: data/_staging/literature/cache_list.csv rows with a DOI, year <= --max-year (default 2020) and no local
source.pdf; --paper-ids overrides. Next step: scripts/lit_extract.py --pending.

Usage: uv run python scripts/lit_fetch_scihub.py [--max 10] [--max-year 2020] [--gap 20:30] [--order year|rank]
         [--paper-ids a,b] [--warm [DOI] [--run]] [--dry-run]
Exit codes: 0 all ok / skipped / not_found, 3 some paper failed, 4 blocked (breaker or missing cookie), 5 another run.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import fcntl
import hashlib
import json
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from photonics_atlas.paths import CACHE, LOGS, ROOT, STAGING
from photonics_atlas.runlog import RunLog

CACHE_LIST = STAGING / "literature" / "cache_list.csv"
STATUS = LOGS / "lit_fetch_status.jsonl"
REFS = ROOT / "references"
COOKIE_FILE = CACHE / "literature" / "scihub_cookies.json"
PROFILE = CACHE / "browser_profiles" / "scihub_chromium"
BREAKER = LOGS / ".lit_scihub_blocked.json"
LOCK = LOGS / ".lit_scihub.lock"
GAP_HOST = LOGS / ".lit_sci_bban_top.last"
GAP_LANDING = LOGS / ".lit_sci_hub_reatk_com.last"
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)
LANDING = "https://sci-hub.reatk.com/{doi}"
MIN_PDF_BYTES = 20000
PDF_HOST = "sci.bban.top"
VERIFY_MARK = "cf-turnstile"
EMBED_RE = re.compile(r"<(?:embed|iframe)[^>]*\bsrc=[\"']([^\"']*)[\"']", re.I)


def now() -> str:
    return dt.datetime.now(dt.UTC).isoformat(timespec="seconds")


def parse_gap(spec: str) -> tuple[float, float]:
    lo, _, hi = spec.partition(":")
    return float(lo), float(hi or lo)


def wait_host(gap: tuple[float, float], stamp: Path) -> float:
    """Sleep so two requests to the same host are >= gap apart (jittered); shared with parallel runs."""
    lo, hi = gap
    target = random.uniform(lo, hi)
    if not stamp.exists():
        return 0.0
    last = float(stamp.read_text().strip() or 0)
    delta = time.time() - last
    wait = max(0.0, target - delta)
    if wait:
        time.sleep(wait)
    return wait


def mark_host(stamp: Path) -> None:
    stamp.write_text(f"{time.time():.3f}")


def load_cookie() -> tuple[str, float] | None:
    if not COOKIE_FILE.exists():
        return None
    try:
        cookies = json.loads(COOKIE_FILE.read_text())
    except json.JSONDecodeError:
        return None
    for c in cookies:
        if c.get("name") == "scihub_verified":
            return c.get("value", ""), float(c.get("expires") or 0)
    return None


def request(url: str, cookie: str | None = None, timeout: float = 60) -> tuple[int, bytes, dict[str, str]]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    if cookie:
        req.add_header("Cookie", f"scihub_verified={cookie}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:  # noqa: S310 - fixed https hosts
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers or {})
    finally:
        mark_host(GAP_LANDING if "sci-hub" in url else GAP_HOST)


def arm_breaker(reason: str, paper_id: str) -> None:
    BREAKER.write_text(json.dumps({"at": now(), "reason": reason, "paper_id": paper_id}))


def append_status(paper_id: str, status: str, body: bytes = b"", detail: str = "", **extra: Any) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    rec: dict[str, Any] = {
        "ts": now(),
        "paper_id": paper_id,
        "route": "scihub",
        "status": status,
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest() if body else "",
    }
    if detail:
        rec["detail"] = detail[:300]
    rec.update(extra)
    with STATUS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")


def is_pdf(body: bytes) -> bool:
    return body[:5] == b"%PDF-" and len(body) >= MIN_PDF_BYTES


def save_pdf(row: dict[str, str], body: bytes, pdf_url: str) -> str:
    out = REFS / row["paper_id"]
    created = not out.exists()
    out.mkdir(parents=True, exist_ok=True)
    part = out / "source.pdf.part"
    try:
        part.write_bytes(body)
        part.replace(out / "source.pdf")
    finally:
        part.unlink(missing_ok=True)
        if created and not any(out.iterdir()):
            out.rmdir()
    meta = out / "source.json"
    if not meta.exists():
        meta.write_text(
            json.dumps(
                {
                    "paper_id": row["paper_id"],
                    "uid": row.get("uid", ""),
                    "doi": row["doi"],
                    "title": row.get("title", ""),
                    "url": LANDING.format(doi=row["doi"]),
                    "route": "scihub",
                    "pdf_host": urllib.parse.urlsplit(pdf_url).netloc,
                    "access": "scihub",
                    "content_type": "application/pdf",
                    "retrieved_on": now(),
                    "redistribution": "restricted_local_only",
                    "bytes": len(body),
                    "sha256": hashlib.sha256(body).hexdigest(),
                    "venue": row.get("venue", ""),
                    "venue_type": row.get("venue_type", ""),
                    "year": row.get("year", ""),
                },
                indent=1,
            )
            + "\n"
        )
    return "ok"


def warm_browser(doi: str, log: RunLog) -> bool:
    """Open headed Chrome, pass the Turnstile gate, dump the scihub cookies; True when a live cookie was saved.

    The gate only appears when the browser has no clearance, so an existing clearance makes the page load without
    setting `scihub_verified`. When that happens the site cookies are cleared and the page is reloaded to force it.
    """
    from playwright.sync_api import sync_playwright

    PROFILE.mkdir(parents=True, exist_ok=True)

    def live(ctx: Any) -> dict[str, Any] | None:
        for c in ctx.cookies():
            if c.get("name") == "scihub_verified" and float(c.get("expires") or 0) > time.time() + 600:
                return dict(c)
        return None

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE),
            channel="chrome",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1280, "height": 900},
        )
        try:
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            for attempt in (1, 2):
                page.goto(LANDING.format(doi=doi), wait_until="domcontentloaded", timeout=90000)
                t0 = time.time()
                while time.time() - t0 < 120:
                    if live(ctx):
                        break
                    time.sleep(2)
                if live(ctx):
                    break
                log.event("warm", "no_cookie", doi=doi, attempt=attempt, url=page.url)
                if attempt == 1:
                    ctx.clear_cookies()
            cookies = ctx.cookies()
            COOKIE_FILE.parent.mkdir(parents=True, exist_ok=True)
            COOKIE_FILE.write_text(json.dumps(cookies, indent=1) + "\n")
            found = live(ctx)
            log.event("warm", "ok" if found else "failed", doi=doi, url=page.url, n_cookies=len(cookies),
                      expires=found["expires"] if found else None)
            return found is not None
        finally:
            ctx.close()


def candidates(max_year: int, paper_ids: list[str], order: str) -> list[dict[str, str]]:
    rows = list(csv.DictReader(CACHE_LIST.open()))
    if paper_ids:
        want = set(paper_ids)
        picked = [r for r in rows if r["paper_id"] in want]
    else:
        picked = [r for r in rows if r.get("doi") and int(r["year"] or 9999) <= max_year]
    picked = [r for r in picked if r.get("doi") and not (REFS / r["paper_id"] / "source.pdf").exists()]
    if order == "year":
        picked.sort(key=lambda r: (int(r["year"] or 9999), int(r["rank"] or 9999)))
    else:
        picked.sort(key=lambda r: int(r["rank"] or 9999))
    return picked


def pdf_url(html: str) -> str | None:
    for src in EMBED_RE.findall(html):
        if PDF_HOST in src:
            src = "https:" + src if src.startswith("//") else src
            return urllib.parse.unquote(src)  # some embeds double-encode the DOI (10.1049/el%253A20021185)
    return None


def _tokens(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if len(w) > 2}


def title_overlap(pdf: bytes, title: str) -> float | None:
    """Share of the title's words found on the first two pages; None when PyMuPDF is unavailable."""
    try:
        import pymupdf
    except ImportError:
        return None
    with pymupdf.open(stream=pdf, filetype="pdf") as doc:  # type: ignore[no-untyped-call]
        text = "".join(doc[i].get_text() for i in range(min(2, doc.page_count)))
    want = _tokens(title)
    return len(want & _tokens(text)) / max(1, len(want)) if want else None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--max", type=int, default=10, help="papers attempted in this run (default 10)")
    ap.add_argument("--max-year", type=int, default=2020, help="edit year cutoff, inclusive (default 2020 = pre-2021)")
    ap.add_argument("--gap", default="20:30", help="seconds between requests to the same host (default 20:30)")
    ap.add_argument("--order", choices=["year", "rank"], default="year")
    ap.add_argument("--paper-ids", default="", help="comma separated paper_id list (overrides the year filter)")
    ap.add_argument("--warm", nargs="?", const="", metavar="DOI", help="open Chrome, pass the gate, save the cookie")
    ap.add_argument("--renew", action="store_true", help="warm only when the cookie is missing or dies within 5 min")
    ap.add_argument("--run", action="store_true", help="keep fetching after --warm (default: warm and stop)")
    ap.add_argument("--min-title", type=float, default=0.5, help="title overlap below which a PDF is quarantined")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    gap = parse_gap(a.gap)
    with RunLog("lit_fetch_scihub", a.dry_run) as log:
        if a.warm is not None:
            doi = a.warm or (candidates(a.max_year, [p for p in a.paper_ids.split(",") if p], a.order) or [{}])[0].get("doi")
            if not doi:
                log.info("--warm needs a DOI or a pending candidate")
                return 4
            warm_browser(doi, log)
            if not load_cookie():
                log.info("warm did not yield a live scihub_verified cookie; check the Chrome window")
                return 4
            log.info(f"cookie saved to {COOKIE_FILE.relative_to(ROOT)}")
            BREAKER.unlink(missing_ok=True)
            if not a.run:
                return 0

        if a.renew:
            live = load_cookie()
            if not live or live[1] < time.time() + 300:
                doi = (candidates(a.max_year, [p for p in a.paper_ids.split(",") if p], a.order) or [{"doi": ""}])[0]["doi"]
                if not doi:
                    log.info("--renew needs a pending candidate or a DOI via --warm")
                    return 4
                warm_browser(doi, log)
                if not load_cookie():
                    log.info("renew did not yield a live scihub_verified cookie; check the Chrome window")
                    return 4
                BREAKER.unlink(missing_ok=True)
                log.info(f"cookie renewed at {now()}")

        if BREAKER.exists():
            log.info(f"breaker active: {BREAKER.read_text().strip()}; refresh with --warm")
            return 4
        cookie = load_cookie()
        if not cookie or cookie[1] < time.time() + 120:
            log.info("no live scihub_verified cookie: run --warm first")
            return 4

        ids = [p for p in a.paper_ids.split(",") if p]
        todo = candidates(a.max_year, ids, a.order)
        log.info(f"{len(todo)} candidates (max_year {a.max_year}); attempting {min(a.max, len(todo))}")
        if a.dry_run:
            for r in todo[: a.max]:
                log.info(f"would fetch {r['paper_id']} {r['year']} {r['doi']}")
            return 0

        LOCK.parent.mkdir(parents=True, exist_ok=True)
        lock = LOCK.open("w")
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            log.info("another scihub fetcher is running")
            return 5

        failed = 0
        for i, row in enumerate(todo[: a.max], 1):
            pid, doi = row["paper_id"], row["doi"]
            if (REFS / pid / "source.pdf").exists():
                continue
            wait_host(gap, GAP_LANDING)
            wait_host(gap, GAP_HOST)
            url = LANDING.format(doi=doi)
            t0 = time.time()
            try:
                code, body, _ = request(url, cookie[0])
            except Exception as e:  # noqa: BLE001 - network error
                arm_breaker(f"network error: {e}", pid)
                append_status(pid, "blocked", detail=f"network error: {e}", url=url)
                log.info(f"[{i}/{a.max}] {pid} network error: {e}")
                return 4
            html = body.decode("utf-8", "replace")
            if VERIFY_MARK in html or code in (403, 429, 503):
                arm_breaker(f"challenge/http {code}", pid)
                append_status(pid, "blocked", detail=f"challenge or http {code}", url=url)
                log.info(f"[{i}/{a.max}] {pid} challenge (http {code}) at {now()}; stopped")
                return 4
            found = pdf_url(html)
            if not found:
                append_status(pid, "not_found", detail=f"landing {code}, no embed", url=url)
                log.info(f"[{i}/{a.max}] {pid} {row['year']} not_found ({time.time() - t0:.0f}s)")
                continue
            wait_host(gap, GAP_HOST)
            try:
                pcode, pdf, headers = request(found)
            except Exception as e:  # noqa: BLE001
                arm_breaker(f"pdf network error: {e}", pid)
                append_status(pid, "blocked", detail=f"pdf network error: {e}", url=found)
                return 4
            if pcode != 200 or not is_pdf(pdf):
                failed += 1
                append_status(pid, "not_pdf", pdf, detail=f"http {pcode}, {len(pdf)} bytes", url=found)
                log.info(f"[{i}/{a.max}] {pid} not_pdf http {pcode} {len(pdf)} B")
                continue
            if "Content-Length" in headers and int(headers["Content-Length"]) != len(pdf):
                failed += 1
                append_status(pid, "error", pdf, detail="truncated download", url=found)
                log.info(f"[{i}/{a.max}] {pid} truncated {len(pdf)} B")
                continue
            overlap = title_overlap(pdf, row.get("title", ""))
            ovtxt = "n/a" if overlap is None else f"{overlap:.2f}"
            if overlap is not None and overlap < a.min_title:
                qdir = CACHE / "literature" / "quarantine" / pid
                qdir.mkdir(parents=True, exist_ok=True)
                (qdir / "source.pdf").write_bytes(pdf)
                failed += 1
                append_status(pid, "title_mismatch", pdf, url=found, title_overlap=round(overlap, 2))
                log.info(f"[{i}/{a.max}] {pid} title overlap {overlap:.2f} -> quarantined")
                continue
            save_pdf(row, pdf, found)
            append_status(pid, "ok", pdf, url=found, pdf_host=urllib.parse.urlsplit(found).netloc,
                          title_overlap=None if overlap is None else round(overlap, 2))
            log.info(f"[{i}/{a.max}] {pid} {row['year']} ok {len(pdf)} B overlap {ovtxt} "
                     f"({time.time() - t0:.0f}s) {now()}")
        log.info(f"done: {failed} failed")
        return 3 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
