"""Throttled browser fetcher for Optica, IEEE Xplore and publisher PDFs (DevLog-006 S7, D142 / D143).

Adapted from advanced-packaging-atlas scripts/ieee_fetch.py + xplore_common.py. Headed Playwright persistent
context (one profile per site and browser under git-ignored cache/browser_profiles/), one paper every 60-120 s,
at most --max papers per run (session; default 30 IEEE, 20 Optica per D142) and 60 saved PDFs per rolling 2 h per
site. Challenge detection (captcha / AWS WAF / Cloudflare / access denied / HTTP 403-429-503 / HTML instead of PDF):
IEEE retries twice ~8-10 s apart, Optica retries never (its traffic was flagged before: stop at the first
challenge); then the breaker file logs/.lit_browser_blocked_<site>.json is written and every run refuses to start
until it is removed by hand. Paywall / abstract-only answers are `no_access` (no breaker). Two consecutive
unexplained HTML-instead-of-PDF answers: IEEE re-probes the session and stops if it is lost; Optica sets the breaker.

--site ieee also takes queue route ieee_search (Optica conference papers whose Xplore copy has no IEEE DOI): a
same-origin POST /rest/search from the signed-in Xplore page with the exact title in quotes (rowsPerPage 10); a hit
needs normalized-title similarity >= 0.93 and a shared author surname (cache_list first_author / last_author), then
the PDF is fetched by arnumber as for ieee_browser. Status lines carry ieee_arnumber and match_score; no hit is
`no_ieee_copy` (no breaker). After a search-only attempt the next paper waits 20-30 s instead of 60-120 s, so searches
stay >= 20 s apart and PDFs >= 60 s apart; every row counts toward the session cap.

--site publisher (Nature, Wiley, AIP, ACS, IOP, De Gruyter; these block non-browser clients): DOI landing, then the
page's citation_pdf_url or the publisher's PDF link pattern, opened in the tab (viewer or download event). No retries;
breakers are per publisher host (logs/.lit_browser_blocked_publisher_<host>.json, host from the DOI prefix) so a block
on one publisher skips only that publisher's papers. At most 20 per session; the 60 per rolling 2 h cap is shared by
all publisher hosts. --login opens --login-url (default https://www.nature.com) for an optional institutional sign-in.

PDFs: references/<paper_id>/source.pdf (.part, %PDF + minimum-size check, rename); source.json written when absent.
Status: one line per attempt appended to the shared logs/lit_fetch_status.jsonl (ts, paper_id, route, status, bytes,
sha256, detail; status ok = saved). Run log: logs/lit_fetch_browser_<site>_<ts>.log/.jsonl. No extraction (scripts/lit_extract.py).

Usage:
  uv run python scripts/lit_fetch_browser.py --site optica|ieee|publisher --login [--login-url URL]
      [--browser chromium|firefox]
  uv run python scripts/lit_fetch_browser.py --site optica|ieee|publisher --run (--day N [--session S] | --paper-ids a,b)
      [--max N] [--browser chromium|firefox] [--dry-run]
Queue: data/_staging/literature/retrieval_queue.csv (route optica_browser / ieee_browser + ieee_search /
publisher_browser);
--paper-ids also falls back
to data/_staging/literature/cache_list.csv. When the rolling cap is reached the run sleeps until a slot frees.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import html as htmllib
import json
import queue
import random
import re
import sys
import threading
import time
import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urljoin, urlsplit

from photonics_atlas.paths import CACHE, LOGS, ROOT, STAGING
from photonics_atlas.runlog import RunLog

QUEUE_CSV = STAGING / "literature" / "retrieval_queue.csv"
CACHE_LIST = STAGING / "literature" / "cache_list.csv"
STATUS = LOGS / "lit_fetch_status.jsonl"
REFS = ROOT / "references"
PROFILES = CACHE / "browser_profiles"
PW_CACHE = Path.home() / "Library" / "Caches" / "ms-playwright"

CAP = 60
CAP_WINDOW_H = 2.0
GAP_S = (60.0, 120.0)
CHALLENGE_WAIT_S = 8.0
MIN_PDF_BYTES = 20000
SAVED = ("ok", "saved")  # status values of a saved PDF in lit_fetch_status.jsonl ("ok" = stream R2 convention)
NAV_TIMEOUT_MS = 90000
IEEE_BASE = "https://ieeexplore.ieee.org"
OPTICA_BASE = "https://opg.optica.org"
SEARCH_ROUTE = "ieee_search"
MATCH_MIN = 0.93
SEARCH_GAP_S = (20.0, 30.0)  # after a search-only attempt (no_ieee_copy); PDFs keep GAP_S
PROBE_ARNUMBER = "10195565"  # subscription document used only to read Xplore userInfo (as in ieee_fetch.py)


@dataclass(frozen=True)
class Site:
    name: str
    route: str
    base: str
    doi_prefixes: tuple[str, ...]
    retries: int
    default_max: int
    max_cap: int


# Publisher DOI prefix -> canonical host (breaker key; the DOI is resolved before the host is known).
PUBLISHER_HOSTS = {
    "10.1038/": "www.nature.com",
    "10.1002/": "onlinelibrary.wiley.com",
    "10.1111/": "onlinelibrary.wiley.com",
    "10.1063/": "pubs.aip.org",
    "10.1021/": "pubs.acs.org",
    "10.1088/": "iopscience.iop.org",
    "10.1515/": "www.degruyterbrill.com",
}

SITES = {
    "ieee": Site("ieee", "ieee_browser", IEEE_BASE, ("10.1109/", "10.23919/"), 2, 30, 30),
    "optica": Site("optica", "optica_browser", OPTICA_BASE, ("10.1364/",), 0, 20, 30),
    "publisher": Site("publisher", "publisher_browser", "", tuple(PUBLISHER_HOSTS), 0, 20, 20),
}

# Strong signatures: never on a normal article / PDF page.
CHALLENGE_RE = re.compile(
    r"awsWafCookieDomainList|AwsWafIntegration|aws-waf-token|gokuProps|challenge-container|cf_chl_|"
    r"cf-turnstile|cf-browser-verification|<title>\s*Just a moment|Attention Required! \| Cloudflare|"
    r"Error 10(?:06|07|08|20)|<title>\s*Access Denied|You don't have permission to access|Request (?:blocked|rejected)|"
    r"unusual traffic|automated (?:queries|requests|access)|verify you are (?:a )?human|Are you a robot",
    re.I,
)
# Signatures count only when the page is not an article page (citation_* meta), which a challenge page never is.
# Weak signature: a captcha widget (not the bare word: Xplore article pages carry a `.captcha` CSS class).
CAPTCHA_RE = re.compile(
    r"g-recaptcha|recaptcha/api|hcaptcha\.com|captcha[-_](?:container|form|image|challenge|box)|id=\"captcha", re.I
)
JSCHECK_RE = re.compile(r"checkjs\.cfm|<p>\s*Please wait\.\.\.\s*</p>", re.I)
# Article pages: citation_* meta, or the IEEE Xplore document app (no citation meta; 2026-10-22 false positive).
ARTICLE_RE = re.compile(
    r'<meta[^>]+name="citation_(?:title|doi)"|xplGlobal\.document\.metadata|class="document-title', re.I
)
PAYWALL_RE = re.compile(
    r"Purchase (?:this )?(?:article|PDF|Details)|Buy (?:this )?article|Get Access|Login to access|"
    r"Sign in to (?:view|access|download)|requires (?:a )?subscription|You do not have (?:subscription )?access|"
    r"Access to this (?:document|article|content) requires|Subscribe to (?:view|access)|Article Access Options|"
    r"Institutional Sign In",
    re.I,
)
# Optica signed-in markers (unverified; terminal confirmation is the primary login signal).
OPTICA_ACCESS_RE = re.compile(r"Access provided by|Signed in as|Log ?out|Sign ?out", re.I)


# ---------- pure helpers (unit-tested) ----------


def doi_ok(site: Site, doi: str) -> bool:
    return doi.strip().lower().startswith(site.doi_prefixes)


def arnumber_from_url(url: str) -> str | None:
    m = re.search(r"/document/(\d+)", url) or re.search(r"[?&]arnumber=(\d+)", url)
    return m.group(1) if m else None


def optica_uri_from_url(url: str) -> tuple[str | None, str | None]:
    """(journal path segment or None, uri) from an opg.optica.org abstract / fulltext / viewmedia URL."""
    parts = urlsplit(url)
    if not parts.netloc.endswith("optica.org"):
        return None, None
    uri = parse_qs(parts.query).get("uri", [""])[0]
    if not uri:
        return None, None
    segs = [s for s in parts.path.split("/") if s]
    journal = segs[0] if len(segs) >= 2 and segs[-1].endswith(".cfm") else None
    return journal, uri


def optica_pdf_url(html: str, page_url: str) -> str | None:
    """PDF link an Optica article page offers: citation_pdf_url meta, a viewmedia.cfm link, or built from the uri."""
    meta = meta_pdf_url(html, page_url)
    if meta:
        return meta
    m = re.search(r'href="([^"]*viewmedia\.cfm\?[^"]*uri=[^"]*seq=0[^"]*)"', html, re.I)
    if m:
        return urljoin(page_url, htmllib.unescape(m.group(1)))
    journal, uri = optica_uri_from_url(page_url)
    if not uri:
        return None
    prefix = f"{OPTICA_BASE}/{journal}" if journal else OPTICA_BASE
    return f"{prefix}/viewmedia.cfm?uri={uri}&seq=0"


def embedded_pdf_url(html: str, page_url: str) -> str | None:
    """A direct PDF link inside an interstitial / viewer page (iframe / embed / object / directpdfaccess href)."""
    m = re.search(r'<(?:iframe|embed|object)[^>]+(?:src|data)="([^"]+)"', html, re.I)
    if m and re.search(r"\.pdf|directpdfaccess|getPDF", m.group(1), re.I):
        return urljoin(page_url, htmllib.unescape(m.group(1)))
    m = re.search(r'href="([^"]*directpdfaccess[^"]*)"', html, re.I)
    return urljoin(page_url, htmllib.unescape(m.group(1))) if m else None


def ieee_pdf_url(html: str, arnumber: str) -> str:
    m = re.search(r'src="([^"]*getPDF\.jsp[^"]*)"', html)
    if not m:
        return f"{IEEE_BASE}/stampPDF/getPDF.jsp?tp=&arnumber={arnumber}&ref="
    src = htmllib.unescape(m.group(1))
    return IEEE_BASE + src if src.startswith("/") else src


def is_challenge(html: str, status: int | None = None) -> bool:
    if status in (403, 429, 503):
        return True
    head = html[:200000]
    if ARTICLE_RE.search(head):
        return False
    return bool(CHALLENGE_RE.search(head) or CAPTCHA_RE.search(head))


def classify_html(html: str, status: int | None = None) -> str:
    """'challenge' (breaker), 'no_access' (paywall / abstract only) or 'not_pdf' (unexplained HTML)."""
    if is_challenge(html, status):
        return "challenge"
    if PAYWALL_RE.search(html[:400000]):
        return "no_access"
    return "not_pdf"


def classify_nav_page(html: str) -> str:
    """Final page after opening a PDF link in the tab: 'challenge' (incl. a JS check that never cleared),
    'no_access' (redirected to the article / abstract page or a paywall), or 'not_pdf'."""
    if is_challenge(html) or JSCHECK_RE.search(html):
        return "challenge"
    if ARTICLE_RE.search(html) or PAYWALL_RE.search(html[:400000]):
        return "no_access"
    return "not_pdf"


def publisher_host(doi: str) -> str | None:
    d = doi.strip().lower()
    return next((h for pre, h in PUBLISHER_HOSTS.items() if d.startswith(pre)), None)


def meta_pdf_url(html: str, page_url: str) -> str | None:
    m = re.search(r'<meta[^>]+name="citation_pdf_url"[^>]+content="([^"]+)"', html, re.I) or re.search(
        r'<meta[^>]+content="([^"]+)"[^>]+name="citation_pdf_url"', html, re.I
    )
    return urljoin(page_url, htmllib.unescape(m.group(1))) if m else None


def publisher_pdf_url(html: str, page_url: str, doi: str) -> str | None:
    """PDF link for a publisher landing page: citation_pdf_url meta, else the publisher's PDF link pattern.

    Wiley: /doi/pdf/ and /doi/epdf/ are reader pages, so any Wiley link is rewritten to /doi/pdfdirect/<doi>."""
    parts = urlsplit(page_url)
    host = parts.netloc.lower()
    doi = doi.strip().lower()
    origin = f"{parts.scheme or 'https'}://{host}"
    if "wiley.com" in host:
        return f"{origin}/doi/pdfdirect/{doi}"
    meta = meta_pdf_url(html, page_url)
    if meta:
        return meta
    if host.endswith("nature.com"):
        m = re.match(r"/articles/([^/?#.]+)", parts.path)
        return f"{origin}/articles/{m.group(1)}.pdf" if m else None
    if host.endswith("pubs.acs.org"):
        return f"{origin}/doi/pdf/{doi}"
    if host.endswith("iopscience.iop.org"):
        return f"{origin}/article/{doi}/pdf"
    if "degruyter" in host:
        return f"{origin}/document/doi/{doi}/pdf"
    if host.endswith("pubs.aip.org"):
        m = re.search(r'href="([^"]*/article-pdf/[^"]+)"', html, re.I)
        return urljoin(page_url, htmllib.unescape(m.group(1))) if m else None
    return None


def is_pdf(body: bytes, min_bytes: int = MIN_PDF_BYTES) -> bool:
    return body[:5] == b"%PDF-" and len(body) >= min_bytes


def parse_ts(s: str) -> dt.datetime:
    t = dt.datetime.fromisoformat(s)
    return t if t.tzinfo else t.replace(tzinfo=dt.UTC)


def saved_times(lines: list[str], routes: str | tuple[str, ...], now: dt.datetime, hours: float) -> list[dt.datetime]:
    """Timestamps of `saved` status lines for `routes` within the last `hours`, oldest first."""
    routes = (routes,) if isinstance(routes, str) else routes
    cutoff = now - dt.timedelta(hours=hours)
    out = []
    for ln in lines:
        try:
            e = json.loads(ln)
            ts = parse_ts(e["ts"])
        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            continue
        if e.get("route") in routes and e.get("status") in SAVED and cutoff <= ts <= now:
            out.append(ts)
    return sorted(out)


def cap_wait_s(times: list[dt.datetime], cap: int, hours: float, now: dt.datetime) -> float:
    """Seconds until one more save fits under `cap` per rolling `hours` (0 when it fits now)."""
    if len(times) < cap:
        return 0.0
    frees = times[len(times) - cap] + dt.timedelta(hours=hours)
    return max(0.0, (frees - now).total_seconds())


def site_routes(site: Site) -> tuple[str, ...]:
    return (site.route, SEARCH_ROUTE) if site.name == "ieee" else (site.route,)


def make_target(r: dict[str, str], c: dict[str, str] | None, site: Site) -> tuple[dict[str, str] | None, str]:
    """Target for one queue / cache_list row, or (None, reason). An `ieee_search` row keeps its non-IEEE DOI (the
    Xplore copy is found by title); an IEEE row whose own DOI is not IEEE uses its `ieee_doi` when that is IEEE."""
    route = r.get("route") or site.route
    doi = (r.get("doi") or "").strip().lower()
    ieee_doi = (r.get("ieee_doi") or "").strip().lower()
    if site.name == "ieee" and route != SEARCH_ROUTE and not doi_ok(site, doi) and doi_ok(site, ieee_doi):
        doi = ieee_doi
    if route == SEARCH_ROUTE:
        if site.name != "ieee":
            return None, f"{r['paper_id']}: route {SEARCH_ROUTE} needs --site ieee"
    elif not doi_ok(site, doi):
        return None, f"{r['paper_id']}: doi {doi or '-'} is not a {site.name} DOI"
    else:
        route = site.route
    c = c or {}
    t = {
        "paper_id": r["paper_id"],
        "doi": doi,
        "route": route,
        "route_url": r.get("route_url") or "",
        "title": r.get("title") or c.get("title") or "",
        "first_author": c.get("first_author") or r.get("first_author") or "",
        "last_author": c.get("last_author") or r.get("last_author") or "",
    }
    if route == SEARCH_ROUTE and not t["title"]:
        return None, f"{r['paper_id']}: no title for the Xplore search"
    return t, ""


def select_targets(
    queue_rows: list[dict[str, str]],
    cache_rows: list[dict[str, str]],
    site: Site,
    day: int | None,
    session: str | None,
    paper_ids: list[str] | None,
) -> tuple[list[dict[str, str]], list[str]]:
    """Targets (paper_id, doi, route, route_url, title, authors) in queue order, plus warnings for dropped ids."""
    warn: list[str] = []
    out: list[dict[str, str]] = []
    by_c = {r["paper_id"]: r for r in cache_rows}
    if paper_ids:
        by_q = {r["paper_id"]: r for r in queue_rows}
        rows: list[dict[str, str]] = []
        for pid in paper_ids:
            r = by_q.get(pid) or by_c.get(pid)
            if r:
                rows.append(r)
            else:
                warn.append(f"{pid}: not in retrieval_queue.csv or cache_list.csv")
    else:
        rows = [
            r
            for r in queue_rows
            if r.get("route") in site_routes(site)
            and str(r.get("day", "")).strip() == str(day)
            and (session is None or str(r.get("session", "")).strip() == session)
        ]
    for r in rows:
        t, why = make_target(r, by_c.get(r["paper_id"]), site)
        if t:
            out.append(t)
        else:
            warn.append(why)
    return out, warn


# ---------- Xplore title search (route ieee_search; pure parts unit-tested) ----------


def norm_match_title(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", htmllib.unescape(s or ""))
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def title_similarity(a: str, b: str) -> float:
    na, nb = norm_match_title(a), norm_match_title(b)
    return SequenceMatcher(None, na, nb).ratio() if na and nb else 0.0


def surnames(*names: str) -> set[str]:
    """Candidate surnames: last token of each name, plus a leading ALL-CAPS token ("MATSUMOTO Takeshi")."""
    out: set[str] = set()
    for n in names:
        toks = norm_match_title(n).split()
        raw = re.sub(r"[^A-Za-z\s-]", " ", unicodedata.normalize("NFKD", n or "")).split()
        if toks:
            out.add(toks[-1])
        if raw and len(raw[0]) > 1 and raw[0].isupper() and toks:
            out.add(toks[0])
    return {x for x in out if len(x) > 1}


def search_body(title: str) -> dict[str, Any]:
    q = re.sub(r"\s+", " ", title.replace('"', " ")).strip()
    return {"queryText": f'"{q}"', "rowsPerPage": 10, "pageNumber": 1, "newsearch": True}


def best_xplore_hit(records: list[dict[str, Any]], title: str, authors: set[str]) -> tuple[str | None, float]:
    """(arnumber, score) of the best record with title similarity >= MATCH_MIN and a shared author surname;
    (None, best similarity seen) when nothing qualifies."""
    best: tuple[str | None, float] = (None, 0.0)
    seen = 0.0
    for rec in records:
        sim = title_similarity(title, str(rec.get("articleTitle") or ""))
        seen = max(seen, sim)
        names = [str(a.get("preferredName") or a.get("normalizedName") or "") for a in rec.get("authors") or []]
        tokens = {tok for n in names for tok in norm_match_title(n).split()}
        an = str(rec.get("articleNumber") or "")
        if sim >= MATCH_MIN and an and authors & tokens and sim > best[1]:
            best = (an, sim)
    return best if best[0] else (None, seen)


# ---------- files ----------


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def breaker_path(site: Site, host: str | None = None) -> Path:
    return LOGS / (
        f".lit_browser_blocked_{site.name}_{host}.json" if host else f".lit_browser_blocked_{site.name}.json"
    )


def set_breaker(site: Site, reason: str, paper_id: str, host: str | None = None) -> None:
    now = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    rec = {"at": now, "site": site.name, "host": host, "reason": reason, "paper_id": paper_id}
    breaker_path(site, host).write_text(json.dumps(rec))


def breaker_key(site: Site, doi: str) -> str | None:
    """Per-host breaker key for --site publisher; None (one breaker per site) otherwise."""
    return publisher_host(doi) if site.name == "publisher" else None


def append_status(
    paper_id: str, route: str, status: str, body: bytes = b"", detail: str = "", extra: dict[str, Any] | None = None
) -> None:
    LOGS.mkdir(parents=True, exist_ok=True)
    rec: dict[str, Any] = {
        "ts": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
        "paper_id": paper_id,
        "route": route,
        "status": status,
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest() if body else "",
    }
    if detail:
        rec["detail"] = detail[:300]
    rec.update(extra or {})
    with STATUS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")


def status_lines() -> list[str]:
    return STATUS.read_text(encoding="utf-8").splitlines() if STATUS.exists() else []


def snapshot(site: Site, paper_id: str, html: str) -> Path:
    p = LOGS / f"lit_browser_{site.name}_{paper_id}_{dt.datetime.now():%Y%m%dT%H%M%S}.html"
    p.write_text(html[:200000], encoding="utf-8")
    return p


def save_pdf(t: dict[str, str], site: Site, body: bytes, url: str, extra: dict[str, Any] | None = None) -> str:
    out = REFS / t["paper_id"]
    created = not out.exists()
    out.mkdir(parents=True, exist_ok=True)
    part = out / "source.pdf.part"
    try:
        part.write_bytes(body)
        if not is_pdf(part.read_bytes()):
            return "not_pdf"
        part.replace(out / "source.pdf")
    finally:
        part.unlink(missing_ok=True)
        if created and not any(out.iterdir()):
            out.rmdir()
    if not (out / "source.pdf").exists():
        return "not_pdf"
    meta = out / "source.json"
    if not meta.exists():
        meta.write_text(
            json.dumps(
                {
                    "paper_id": t["paper_id"],
                    "doi": t["doi"],
                    "url": f"https://doi.org/{t['doi']}",
                    "route": t.get("route") or site.route,
                    "pdf_host": urlsplit(url).netloc,
                    "access": "publisher_browser_session",
                    "content_type": "application/pdf",
                    "retrieved_on": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
                    "redistribution": "restricted_local_only",
                    "bytes": len(body),
                    "sha256": hashlib.sha256(body).hexdigest(),
                    **(extra or {}),
                },
                indent=1,
            )
            + "\n"
        )
    return "ok"


# ---------- browser ----------


def chromium_executable(default: str) -> str | None:
    """Playwright's expected Chromium if installed, else the newest bundled chromium-* build in ms-playwright."""
    if Path(default).exists():
        return None
    app = "chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
    builds = sorted(PW_CACHE.glob("chromium-*"), key=lambda p: int(p.name.split("-")[1]), reverse=True)
    for b in builds:
        if (b / app).exists():
            return str(b / app)
    raise SystemExit(f"no Playwright Chromium under {PW_CACHE}")


def open_ctx(p: Any, browser: str, site: Site) -> Any:
    prof = PROFILES / f"{site.name}_{browser}"
    if browser == "firefox" and not Path(p.firefox.executable_path).exists():
        raise SystemExit(
            f"Playwright Firefox is not installed ({p.firefox.executable_path}); "
            "installing it needs the coordinator's approval (uv run playwright install firefox)"
        )
    prof.mkdir(parents=True, exist_ok=True)
    kw: dict[str, Any] = {
        "headless": False,
        "accept_downloads": True,
        "viewport": {"width": 1280, "height": 900},
        "locale": "en-US",
    }
    if browser == "chromium":
        exe = chromium_executable(p.chromium.executable_path)
        if exe:
            kw["executable_path"] = exe
        return p.chromium.launch_persistent_context(str(prof), **kw)
    return p.firefox.launch_persistent_context(str(prof), **kw)


def main_page(ctx: Any) -> Any:
    return ctx.pages[0] if ctx.pages else ctx.new_page()


def goto(page: Any, url: str) -> tuple[int | None, str]:
    resp = page.goto(url, wait_until="domcontentloaded", timeout=NAV_TIMEOUT_MS)
    page.wait_for_timeout(int(random.uniform(3.0, 5.0) * 1000))
    return (resp.status if resp else None), page.content()


def ieee_access(ctx: Any, attempts: int = 3) -> dict[str, Any]:
    """Xplore userInfo for the signed-in state, tolerating pages that are mid-navigation (SSO redirects)."""
    last = ""
    for attempt in range(attempts):
        pages = [pg for pg in ctx.pages if pg.url.startswith(IEEE_BASE)]
        page = pages[-1] if pages else main_page(ctx)
        try:
            r = page.evaluate(
                """async (u) => { const r = await fetch(u, {credentials: 'same-origin'});
                                  return {status: r.status, text: await r.text()}; }""",
                f"{IEEE_BASE}/rest/document/{PROBE_ARNUMBER}/abstract",
            )
        except Exception as exc:  # noqa: BLE001  execution context destroyed during navigation
            last = str(exc)[:120]
            if attempt + 1 < attempts:
                page.wait_for_timeout(2000)
            continue
        try:
            ui = json.loads(r["text"]).get("userInfo", {})
        except json.JSONDecodeError:
            return {"status": r["status"], "ok": False}
        ok = bool(ui.get("institute") or ui.get("individual"))
        return {"status": r["status"], "ok": ok, "institute": ui.get("institute"), "individual": ui.get("individual")}
    return {"status": None, "ok": False, "error": last or "no IEEE page"}


def optica_access(ctx: Any) -> dict[str, Any]:
    for page in ctx.pages:
        if "optica.org" in page.url:
            try:
                txt = page.content()
            except Exception:  # noqa: BLE001  mid-navigation
                continue
            m = OPTICA_ACCESS_RE.search(txt)
            if m:
                return {"ok": True, "marker": m.group(0)}
    return {"ok": False}


def access(ctx: Any, site: Site) -> dict[str, Any]:
    if site.name == "ieee":
        return ieee_access(ctx)
    if site.name == "optica":
        return optica_access(ctx)
    return {"ok": False, "note": "no access probe for publishers; confirm in the terminal"}


def fetch_bytes(ctx: Any, url: str, referer: str) -> tuple[int, str, bytes]:
    r = ctx.request.get(url, headers={"Referer": referer}, timeout=120000)
    return r.status, r.headers.get("content-type") or "", r.body()


def nav_pdf(page: Any, url: str, part: Path, wait_s: float = 30.0) -> tuple[bytes, str, str]:
    """Open the PDF URL in the tab and let the site's own JS run (Optica checkjs.cfm, publisher JS challenges).

    Handles the download-event case and the in-browser viewer case. Returns (body, html, final_url): body is the PDF
    when one was captured, html the final page when not."""
    got: dict[str, Any] = {}

    def on_resp(r: Any) -> None:
        if "application/pdf" in (r.headers.get("content-type") or "").lower():
            got.setdefault("resp", r)

    def on_dl(d: Any) -> None:
        got.setdefault("dl", d)

    page.on("response", on_resp)
    page.on("download", on_dl)
    try:
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=NAV_TIMEOUT_MS)
        except Exception as exc:  # noqa: BLE001  "Download is starting" / ERR_ABORTED when the PDF downloads
            if "download" not in str(exc).lower() and "err_aborted" not in str(exc).lower():
                raise
        deadline = time.monotonic() + wait_s
        html = ""
        while time.monotonic() < deadline and not got:
            page.wait_for_timeout(1500)
            try:
                html = page.content()
            except Exception:  # noqa: BLE001  mid-navigation (JS redirect)
                continue
            if not got and ARTICLE_RE.search(html) and not JSCHECK_RE.search(html):
                page.wait_for_timeout(1500)
                break  # landed on an article (abstract) page: no PDF for this session
        page.wait_for_timeout(1000)
        if "dl" in got:
            created = not part.parent.exists()
            part.parent.mkdir(parents=True, exist_ok=True)
            try:
                got["dl"].save_as(str(part))
                return part.read_bytes(), "", page.url
            finally:
                part.unlink(missing_ok=True)
                if created and not any(part.parent.iterdir()):
                    part.parent.rmdir()
        if "resp" in got:
            try:
                return got["resp"].body(), "", got["resp"].url
            except Exception:  # noqa: BLE001  the viewer may not expose the body; caller re-requests the URL
                return b"", "", got["resp"].url
        try:
            html = page.content()
        except Exception:  # noqa: BLE001
            pass
        return b"", html, page.url
    finally:
        page.remove_listener("response", on_resp)
        page.remove_listener("download", on_dl)


# ---------- per-site fetch ----------


class Fetcher:
    def __init__(self, ctx: Any, site: Site, rl: RunLog) -> None:
        self.ctx = ctx
        self.site = site
        self.rl = rl
        self.page = main_page(ctx)
        self.extra: dict[str, Any] = {}

    def _retry_wait(self, pid: str, what: str, attempt: int) -> None:
        wait = CHALLENGE_WAIT_S + random.uniform(0, 2)
        self.rl.info(f"{what} retry {attempt}/{self.site.retries} {pid} (wait {wait:.0f} s)")
        self.rl.event("challenge_retry", "retry", paper_id=pid, what=what, attempt=attempt, wait_s=round(wait, 1))
        time.sleep(wait)

    def page_with_retries(self, pid: str, url: str, ok_re: str | None = None) -> tuple[str, int | None, str]:
        """('ok' | 'challenge', status, html) for an HTML page; retries only on challenge signatures."""
        status, html = goto(self.page, url)
        for attempt in range(1, self.site.retries + 1):
            if (ok_re and re.search(ok_re, html)) or not is_challenge(html, status):
                break
            snapshot(self.site, pid, html)
            self._retry_wait(pid, "page", attempt)
            status, html = goto(self.page, url)
        if (ok_re and re.search(ok_re, html)) or not is_challenge(html, status):
            return "ok", status, html
        snapshot(self.site, pid, html)
        return "challenge", status, html

    def pdf_with_retries(self, pid: str, url: str, referer: str) -> tuple[str, bytes, str]:
        """('pdf' | 'challenge' | 'no_access' | 'not_pdf', body, detail)."""
        status, ctype, body = fetch_bytes(self.ctx, url, referer)
        for attempt in range(1, self.site.retries + 1):
            if is_pdf(body) or not is_challenge(body[:200000].decode("utf-8", "replace"), status):
                break
            self._retry_wait(pid, f"pdf status={status}", attempt)
            status, ctype, body = fetch_bytes(self.ctx, url, referer)
        if is_pdf(body):
            return "pdf", body, ""
        html = body[:400000].decode("utf-8", "replace")
        detail = f"status={status} type={ctype} bytes={len(body)}"
        if body[:5] == b"%PDF-":
            return "not_pdf", b"", f"pdf below {MIN_PDF_BYTES} bytes: {detail}"
        kind = classify_html(html, status)
        if kind != "challenge" and "html" in ctype.lower():
            inner = embedded_pdf_url(html, url)
            if inner and inner != url:
                self.rl.info(f"{pid}: interstitial page; following embedded PDF link")
                return self.pdf_with_retries(pid, inner, url)
        if kind != "challenge":
            snapshot(self.site, pid, html)
        return kind, b"", detail

    def fetch(self, t: dict[str, str]) -> tuple[str, bytes, str]:
        self.extra = {}
        if t.get("route") == SEARCH_ROUTE:
            return self.fetch_ieee_search(t)
        if self.site.name == "ieee":
            return self.fetch_ieee(t)
        if self.site.name == "publisher":
            return self.fetch_publisher(t)
        return self.fetch_optica(t)

    def xplore_search(self, pid: str, title: str) -> tuple[str, Any, str]:
        """Same-origin POST /rest/search from the signed-in Xplore page: ('ok', json, '') | ('challenge' | 'error',
        None, detail). Challenges are retried like the PDF path (IEEE: twice, ~8-10 s apart)."""
        if not self.page.url.startswith(IEEE_BASE):
            goto(self.page, IEEE_BASE + "/Xplore/home.jsp")
        body = search_body(title)
        status, text = 0, ""
        for attempt in range(self.site.retries + 1):
            if attempt:
                self._retry_wait(pid, f"search status={status}", attempt)
            r = self.page.evaluate(
                """async (body) => {
                    const r = await fetch('/rest/search', {method: 'POST', credentials: 'same-origin',
                        headers: {'content-type': 'application/json', accept: 'application/json, text/plain, */*'},
                        body: JSON.stringify(body)});
                    return {status: r.status, text: await r.text()}; }""",
                body,
            )
            status, text = int(r["status"]), str(r["text"])
            self.rl.event("xplore_search", str(status), paper_id=pid, bytes=len(text))
            if not (is_challenge(text, status) or not text.strip()):
                break
        detail = f"search status={status} bytes={len(text)}"
        if is_challenge(text, status) or not text.strip():
            snapshot(self.site, pid, text)
            return "challenge", None, detail
        if status != 200:
            return "error", None, detail
        try:
            return "ok", json.loads(text), ""
        except json.JSONDecodeError:
            snapshot(self.site, pid, text)
            return "challenge", None, f"{detail} (HTML instead of JSON)"

    def fetch_ieee_search(self, t: dict[str, str]) -> tuple[str, bytes, str]:
        """Route ieee_search: find the Xplore copy by exact-title search, then fetch it by arnumber."""
        pid = t["paper_id"]
        st, data, detail = self.xplore_search(pid, t["title"])
        if st == "challenge":
            return "blocked", b"", f"challenge on Xplore search: {detail}"
        if st != "ok":
            return "error", b"", detail
        records = data.get("records") or [] if isinstance(data, dict) else []
        names = surnames(t.get("first_author") or "", t.get("last_author") or "")
        an, score = best_xplore_hit(records, t["title"], names)
        self.extra = {"ieee_arnumber": an or "", "match_score": round(score, 4)}
        if not an:
            why = "no author surnames" if not names else f"{len(records)} hits, best title similarity {score:.3f}"
            return "no_ieee_copy", b"", why
        self.rl.info(f"{pid}: Xplore copy arnumber={an} similarity={score:.3f}")
        time.sleep(random.uniform(4.0, 8.0))
        kind, body, detail = self.fetch_ieee({**t, "route_url": f"{IEEE_BASE}/document/{an}"})
        return kind, body, detail

    def fetch_ieee(self, t: dict[str, str]) -> tuple[str, bytes, str]:
        pid = t["paper_id"]
        an = arnumber_from_url(t.get("route_url") or "")
        if not an:
            st, status, html = self.page_with_retries(pid, f"https://doi.org/{t['doi']}")
            if st == "challenge":
                return "blocked", b"", f"challenge on DOI landing status={status}"
            an = arnumber_from_url(self.page.url)
        if not an:
            return "no_arnumber", b"", f"landing {self.page.url[:120]}"
        stamp = f"{IEEE_BASE}/stamp/stamp.jsp?tp=&arnumber={an}"
        st, status, html = self.page_with_retries(pid, stamp, ok_re=r"getPDF")
        if st == "challenge":
            return "blocked", b"", f"challenge on stamp page arnumber={an} status={status}"
        pdf_url = ieee_pdf_url(html, an)
        kind, body, detail = self.pdf_with_retries(pid, pdf_url, stamp)
        if kind == "pdf":
            return "pdf", body, pdf_url
        if kind == "challenge":
            return "blocked", b"", f"challenge on PDF arnumber={an} {detail}"
        if kind == "not_pdf" and "getPDF" not in html and PAYWALL_RE.search(html):
            kind = "no_access"
        return kind, b"", f"arnumber={an} {detail}"

    def fetch_optica(self, t: dict[str, str]) -> tuple[str, bytes, str]:
        """DOI landing (article page) -> the PDF link it offers -> open that link in the tab (browser JS check)."""
        pid = t["paper_id"]
        ru = t.get("route_url") or ""
        on_site = urlsplit(ru).netloc.endswith("opg.optica.org") and "viewmedia.cfm" not in ru
        landing = ru if on_site else f"https://doi.org/{t['doi']}"
        st, status, html = self.page_with_retries(pid, landing)
        if st == "challenge":
            return "blocked", b"", f"challenge on landing status={status}"
        page_url = self.page.url
        if "optica.org" not in urlsplit(page_url).netloc:
            return "resolve_failed", b"", f"landing {page_url[:120]}"
        if JSCHECK_RE.search(html):
            snapshot(self.site, pid, html)
            return "blocked", b"", "landing stuck on the JS check interstitial"
        pdf_url = optica_pdf_url(html, page_url)
        if not pdf_url:
            return "no_pdf_link", b"", f"landing {page_url[:120]}"
        time.sleep(random.uniform(4.0, 8.0))
        return self.open_pdf(pid, pdf_url, page_url)

    def open_pdf(self, pid: str, pdf_url: str, referer: str) -> tuple[str, bytes, str]:
        """Open a PDF link in the tab; classify the outcome."""
        body, nhtml, final = nav_pdf(self.page, pdf_url, REFS / pid / "source.pdf.part")
        if is_pdf(body):
            return "pdf", body, final
        if not nhtml and final:
            # viewer showed the PDF but its body was not exposed: one same-session request for the final URL
            status, ctype, body = fetch_bytes(self.ctx, final, referer)
            if is_pdf(body):
                return "pdf", body, final
            nhtml = body[:400000].decode("utf-8", "replace")
            if is_challenge(nhtml, status):
                return "blocked", b"", f"challenge on PDF re-request status={status} type={ctype}"
        kind = classify_nav_page(nhtml)
        snapshot(self.site, pid, nhtml)
        if kind == "challenge":
            return "blocked", b"", f"challenge after opening the PDF link (final {final[:100]})"
        return kind, b"", f"pdf link {pdf_url[:100]} final {final[:100]}"

    def settle(self, html: str, wait_s: float = 15.0) -> str:
        """Give an in-browser JS challenge (Nature, AWS WAF) time to clear by itself; no new request from us."""
        deadline = time.monotonic() + wait_s
        while (is_challenge(html) or JSCHECK_RE.search(html)) and time.monotonic() < deadline:
            self.page.wait_for_timeout(2500)
            try:
                html = self.page.content()
            except Exception:  # noqa: BLE001  mid-navigation
                continue
        return str(html)

    def fetch_publisher(self, t: dict[str, str]) -> tuple[str, bytes, str]:
        """DOI landing -> citation_pdf_url or the publisher pattern -> open in the tab (viewer or download)."""
        pid = t["paper_id"]
        status, html = goto(self.page, f"https://doi.org/{t['doi']}")
        html = self.settle(html)
        if is_challenge(html, status) or JSCHECK_RE.search(html):
            snapshot(self.site, pid, html)
            return "blocked", b"", f"challenge on landing status={status} url={self.page.url[:100]}"
        page_url = self.page.url
        pdf_url = publisher_pdf_url(html, page_url, t["doi"])
        if not pdf_url:
            snapshot(self.site, pid, html)
            return "no_pdf_link", b"", f"landing {page_url[:120]}"
        time.sleep(random.uniform(4.0, 8.0))
        return self.open_pdf(pid, pdf_url, page_url)


# ---------- commands ----------


def stdin_waiter() -> queue.Queue[str]:
    q: queue.Queue[str] = queue.Queue()

    def _read() -> None:
        try:
            q.put(sys.stdin.readline())
        except Exception:  # noqa: BLE001
            q.put("")

    threading.Thread(target=_read, daemon=True).start()
    return q


def login(site: Site, browser: str, login_url: str) -> int:
    from playwright.sync_api import sync_playwright

    if breaker_path(site).exists():
        print(f"note: breaker {breaker_path(site)} is set; --run stays blocked until it is removed by hand")
    start = {"ieee": f"{IEEE_BASE}/document/{PROBE_ARNUMBER}/", "optica": f"{OPTICA_BASE}/"}.get(site.name, login_url)
    with RunLog(f"lit_fetch_browser_{site.name}_login") as rl, sync_playwright() as p:
        ctx = open_ctx(p, browser, site)
        page = main_page(ctx)
        page.goto(start, wait_until="domcontentloaded", timeout=NAV_TIMEOUT_MS)
        print(
            f"Sign in ({'Institutional Sign In' if site.name == 'ieee' else 'institutional login'}) in the opened "
            f"window, then press Enter here (access is also probed every 15 s, up to 30 min).",
            flush=True,
        )
        q = stdin_waiter()
        deadline = time.monotonic() + 1800
        rc = 1
        while time.monotonic() < deadline:
            try:
                line = q.get(timeout=15)
            except queue.Empty:
                line = None
            if line:  # Enter pressed ("" = stdin closed: keep probing only)
                st = access(ctx, site)
                rl.info(f"user confirmed in terminal; access probe {st}")
                rl.event("login", "confirmed", access=st)
                rc = 0
                break
            try:
                st = access(ctx, site)
            except Exception as exc:  # noqa: BLE001  mid-navigation during SSO
                print(f"(waiting: {str(exc)[:80]})", flush=True)
                continue
            if st.get("ok"):
                rl.info(f"access detected {st}; profile saved")
                rl.event("login", "detected", access=st)
                rc = 0
                break
        ctx.close()
        if rc:
            rl.info("no confirmation or access within 30 min")
        return rc


def run(site: Site, a: argparse.Namespace) -> int:
    ids = [s.strip() for s in (a.paper_ids or "").split(",") if s.strip()] or None
    qrows = read_csv(QUEUE_CSV)
    if not ids and not qrows:
        print(f"{QUEUE_CSV} does not exist yet; use --paper-ids", file=sys.stderr)
        return 2
    targets, warns = select_targets(qrows, read_csv(CACHE_LIST), site, a.day, a.session, ids)
    max_n = a.max or site.default_max
    with RunLog(f"lit_fetch_browser_{site.name}", dry_run=a.dry_run) as rl:
        for msg in warns:
            rl.info(f"skip {msg}")
        todo = [t for t in targets if not (REFS / t["paper_id"] / "source.pdf").exists()]
        rl.info(
            f"{len(targets)} targets, {len(targets) - len(todo)} already have source.pdf, {len(todo)} to fetch, "
            f"max {max_n} this run"
        )
        rl.event("plan", targets=len(targets), todo=len(todo), max=max_n, site=site.name, browser=a.browser)
        if site.name != "publisher" and breaker_path(site).exists():
            rl.info(f"BREAKER set: {breaker_path(site).read_text()} -- inspect, then remove the file by hand")
            return 3
        blocked_hosts = sorted(
            {h for t in todo if (h := breaker_key(site, t["doi"])) and breaker_path(site, h).exists()}
        )
        if blocked_hosts:
            rl.info(f"BREAKER set for {blocked_hosts}: those papers are skipped (remove the files by hand to reset)")
        if a.dry_run:
            for t in todo[:max_n]:
                rl.info(f"would fetch {t['paper_id']} {t['doi']} {t['route_url']}")
            return 0
        if not todo:
            return 0
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            ctx = open_ctx(p, a.browser, site)
            f = Fetcher(ctx, site, rl)
            if site.name == "ieee":
                f.page.goto(IEEE_BASE + "/Xplore/home.jsp", wait_until="domcontentloaded", timeout=NAV_TIMEOUT_MS)
                f.page.wait_for_timeout(5000)
                st = ieee_access(ctx)
                rl.info(f"access {st}")
                if not st.get("ok") and a.wait_login:
                    # Institutional session cookies do not survive a context close, so sign in in this window.
                    print("Sign in (Institutional Sign In) in the opened window; access is probed every 15 s (30 min).")
                    deadline = time.monotonic() + 1800
                    while not st.get("ok") and time.monotonic() < deadline:
                        f.page.wait_for_timeout(15000)
                        try:
                            st = ieee_access(ctx)
                        except Exception as exc:  # noqa: BLE001  mid-navigation during SSO
                            rl.info(f"(waiting: {str(exc)[:80]})")
                    rl.info(f"access after sign-in wait {st}")
                    if st.get("ok"):
                        rl.event("login", "detected", access=st)
                        f.page.wait_for_timeout(5000)
                if not st.get("ok"):
                    rl.info("NOT SIGNED IN: rerun with --wait-login and sign in in the window")
                    ctx.close()
                    return 2
            done = 0
            prev = ""
            misses: dict[str | None, int] = {}
            counts: dict[str, int] = {}
            for t in todo:
                if done >= max_n:
                    break
                host = breaker_key(site, t["doi"])
                if breaker_path(site, host).exists():
                    if host is None:
                        rl.info("BREAKER set; stopping")
                        break
                    rl.info(f"skip {t['paper_id']}: breaker set for {host}")
                    continue
                while True:
                    now = dt.datetime.now(dt.UTC)
                    w = cap_wait_s(
                        saved_times(status_lines(), site_routes(site), now, CAP_WINDOW_H), CAP, CAP_WINDOW_H, now
                    )
                    if w <= 0:
                        break
                    w += random.uniform(30, 120)
                    rl.info(f"cap {CAP} per {CAP_WINDOW_H:g} h reached; sleeping {w / 60:.0f} min")
                    time.sleep(w)
                if done:
                    gap = random.uniform(*(SEARCH_GAP_S if prev == "no_ieee_copy" else GAP_S))
                    rl.info(f"spacing {gap:.0f} s")
                    time.sleep(gap)
                pid = t["paper_id"]
                try:
                    kind, body, detail = f.fetch(t)
                except Exception as exc:  # noqa: BLE001  navigation timeout etc.: logged, no retry loop
                    kind, body, detail = "error", b"", f"{type(exc).__name__}: {str(exc)[:200]}"
                done += 1
                res = save_pdf(t, site, body, detail, f.extra) if kind == "pdf" else kind
                if res == "blocked":
                    set_breaker(site, detail, pid, host)
                prev = res
                append_status(
                    pid, t["route"], res, body if res == "ok" else b"", "" if res == "ok" else detail, f.extra
                )
                rl.event(
                    "fetch",
                    res,
                    paper_id=pid,
                    doi=t["doi"],
                    bytes=len(body) if res == "ok" else 0,
                    detail=detail,
                    **f.extra,
                )
                rl.info(f"[{done}/{max_n}] {res} {pid} {detail[:140]}")
                counts[res] = counts.get(res, 0) + 1
                if res == "blocked":
                    rl.info(f"challenge: breaker {breaker_path(site, host)} set (manual reset)")
                    if host is None:
                        break
                    continue
                soft = ("not_pdf", "no_access") if site.name == "ieee" else ("not_pdf",)
                misses[host] = misses.get(host, 0) + 1 if res in soft else 0
                if misses[host] >= 2:
                    if site.name == "ieee":
                        st = ieee_access(ctx)
                        if not st.get("ok"):
                            rl.info(f"SESSION LOST {st}: stopping; run --login again")
                            rl.event("session_lost", "stop", access=st)
                            break
                    else:
                        set_breaker(site, "two consecutive HTML-instead-of-PDF answers", pid, host)
                        rl.info(f"two consecutive HTML-instead-of-PDF answers: breaker {breaker_path(site, host)} set")
                        if host is None:
                            break
            rl.info(f"summary {counts}")
            rl.event("summary", "ok", counts=counts)
            ctx.close()
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0] if __doc__ else None)
    ap.add_argument("--site", choices=sorted(SITES), required=True)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--login", action="store_true")
    mode.add_argument("--run", action="store_true")
    ap.add_argument("--day", type=int)
    ap.add_argument("--session")
    ap.add_argument("--paper-ids", help="comma-separated paper_ids (queue or cache_list rows)")
    ap.add_argument("--max", type=int, help="max papers attempted this run (default 30 IEEE, 20 Optica / publisher)")
    ap.add_argument("--login-url", default="https://www.nature.com", help="--site publisher --login start page")
    ap.add_argument("--browser", choices=["chromium", "firefox"], default="chromium")
    ap.add_argument(
        "--wait-login",
        action="store_true",
        help="--site ieee --run: if not signed in, wait in the same window for the user's sign-in (session cookies "
        "are lost when a separate --login window closes)",
    )
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    site = SITES[a.site]
    if a.login:
        return login(site, a.browser, a.login_url)
    if (a.day is None) == (a.paper_ids is None):
        ap.error("--run needs exactly one of --day N or --paper-ids a,b")
    if a.session is not None and a.day is None:
        ap.error("--session needs --day")
    if a.max is not None and not 1 <= a.max <= site.max_cap:
        ap.error(f"--max must be 1..{site.max_cap} for --site {site.name} (session cap)")
    return run(site, a)


if __name__ == "__main__":
    sys.exit(main())
