"""Prepare the historical literature selection for the existing lit pipeline (DevLog-016 D964).

Input: data/_staging/literature/history_candidates.csv (rows of one --tier).
Steps (each idempotent; rows whose paper_id is already present are left untouched):
  queue    append the rows to data/_staging/literature/cache_list.csv (selection_reason = history, uid = DOI or
           hist:<paper_id>) and to data/_staging/literature/retrieval_queue.csv as day --day; cached papers
           (already_in_repo lit: / eo:) get neither. Both CSVs are zip-backed-up to cache/literature/backup/ before
           the first write of a run. Routes: blog copy -> blog_copy (handled by `blog`), BSTJ -> oa_publisher with the
           archive.org PDF URL (resolved by `bstj`), arXiv -> arxiv, open copy -> oa_publisher, OE / Optica / OME ->
           optica_browser, 10.1109 -> ieee_browser, 10.1049 (IET DOIs resolve outside Xplore) -> ieee_search,
           everything else -> manual. Browser rows get new session numbers (<= 30 IEEE, <= 20 Optica per session).
  authors  write cache/literature/history_adds.jsonl (uid, doi, title, year, venue, authors, last_author,
           institutions) for header extraction (read by people.py and ofc_headers.py next to curator_adds.jsonl).
  bstj     resolve archive.org item ids `bstj<vol>-<issue>-<page>` (from the row URL or the Crossref record) to the
           item's PDF through the archive.org metadata API (photonics_atlas.litfetch: spacing, breaker, generic UA);
           cached in cache/literature/history_bstj.json; sets route_url of the queue rows.
  blog     copy the PDFs of `blog:` duplicates from the blog repo (--blog-root, read-only) to references/_inbox/
           <paper_id>.pdf; then run scripts/lit_ingest_inbox.py. Never touches the blog repo.
  manual   write data/_staging/literature/history_manual_downloads.md (owner download list: route manual / ieee rows
           that later fail are added by scripts/lit_manual_list.py).

Usage: uv run python scripts/hist_prepare.py STEP [STEP ...] [--tier core] [--day 101] [--blog-root PATH] [--dry-run]
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import shutil
import sys
import urllib.error
import urllib.parse
import zipfile
from pathlib import Path
from typing import Any

from photonics_atlas import litfetch
from photonics_atlas.paths import CACHE, ROOT, STAGING
from photonics_atlas.runlog import RunLog

LITS = STAGING / "literature"
CANDIDATES = LITS / "history_candidates.csv"
CACHE_LIST = LITS / "cache_list.csv"
QUEUE = LITS / "retrieval_queue.csv"
MANUAL = LITS / "history_manual_downloads.md"
ADDS = CACHE / "literature" / "history_adds.jsonl"
BSTJ_CACHE = CACHE / "literature" / "history_bstj.json"
CR_CACHE = CACHE / "literature" / "history_crossref"
BACKUP = CACHE / "literature" / "backup"
INBOX = ROOT / "references" / "_inbox"
SOURCES = ROOT / "data" / "registry" / "sources.csv"
BLOG_URL_PREFIX = "https://outside5sigma.com/"
# Blog-repo copies of core papers that the candidate list does not tag as blog duplicates.
BLOG_EXTRA = {"kao1966": "blog:kao1966_ip_j_1986_0030"}  # IEE Proc. J 1986 reprint of the 1966 paper (same text)
# Blog copies that are not the paper itself (page-1 check): kept aside under cache/literature/secondary/.
BLOG_NOT_SOURCE = {"colladon1842": "Geneva Musee d'histoire des sciences booklet, not the 1842 Comptes rendus note"}
OPTICA_OA = re.compile(r"^10\.1364/(oe|opex|optica|ome)\.")
CLASSES = {
    "fiber_chip_coupler", "micro_optics", "fiber_interface", "free_space_emitter", "splitter", "crossing",
    "mode_converter", "polarization", "resonator", "wdm", "reflector", "phase_shifter", "switch_fabric",
    "nonreciprocal", "photodetector", "laser", "amplifier", "frequency_converter", "waveguide_platform",
}  # fmt: skip
SESSION_CAP = {"ieee": 30, "optica": 20}


def read(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return list(r.fieldnames or []), [dict(x) for x in r]


def write(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    tmp = path.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)  # csv default CRLF, as the existing files
        w.writeheader()
        w.writerows(rows)
    tmp.replace(path)


def backup(paths: list[Path], tag: str) -> Path:
    BACKUP.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%SZ")
    out = BACKUP / f"hist_{tag}_{ts}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in paths:
            z.write(p, p.relative_to(ROOT))
    return out


def candidates(tier: str) -> list[dict[str, str]]:
    return [r for r in read(CANDIDATES)[1] if r["tier"] == tier]


def is_cached(r: dict[str, str]) -> bool:
    return r["already_in_repo"].startswith(("lit:", "eo:"))


def blog_source(r: dict[str, str]) -> str:
    if r["paper_id"] in BLOG_NOT_SOURCE:
        return ""
    if r["already_in_repo"].startswith("blog:"):
        return r["already_in_repo"]
    return BLOG_EXTRA.get(r["paper_id"], "")


def is_bstj(r: dict[str, str]) -> bool:
    return "bell system technical journal" in r["venue"].lower() or r["doi"].startswith("10.1002/j.1538-7305.")


def arxiv_id_of(url: str) -> str:
    m = re.search(r"arxiv\.org/(?:pdf|abs)/([0-9]{4}\.[0-9]{4,5}|[a-z\-]+/[0-9]{7})", url)
    return m.group(1) if m else ""


def route_of(r: dict[str, str]) -> tuple[str, str]:
    """(queue route, route_url)."""
    doi = r["doi"]
    if blog_source(r):
        return "blog_copy", ""
    if is_bstj(r):
        return "oa_publisher", ""  # route_url set by the bstj step
    if r["route"] == "arxiv" and arxiv_id_of(r["oa_pdf"]):
        return "arxiv", f"https://arxiv.org/pdf/{arxiv_id_of(r['oa_pdf'])}"
    if OPTICA_OA.match(doi):
        return "optica_browser", f"https://doi.org/{doi}"
    if r["route"] == "oa_publisher" and r["oa_pdf"]:
        host = re.sub(r"^https?://([^/]+).*$", r"\1", r["oa_pdf"]).lower()
        if host.endswith("iop.org"):  # IOP answers HTML to non-browser clients (pilot 2026-11-11)
            return "publisher_browser", f"https://doi.org/{doi}"
        if host.endswith(("science.org", "pnas.org")):  # not on the publisher browser route
            return "manual", f"https://doi.org/{doi}"
        return "oa_publisher", r["oa_pdf"]
    if doi.startswith("10.1109/"):
        return "ieee_browser", f"https://doi.org/{doi}"
    if doi.startswith("10.1049/"):
        return "ieee_search", f"https://doi.org/{doi}"
    return "manual", f"https://doi.org/{doi}" if doi else r["url"]


def venue_type(r: dict[str, str]) -> str:
    v = r["venue"].lower()
    if "patent" in v:
        return "other"
    if any(k in v for k in ("conference", "ofc", "cleo", "proceedings", "digest", "ecoc", "iooc", "symposium")):
        return "conference"
    if r["paper_type"] == "retrospective" or "telecommunications" in v:
        return "other"
    return "journal"


def authors_of(r: dict[str, str]) -> list[str]:
    return [a.strip() for a in r["authors"].split(";") if a.strip() and "et al" not in a]


def step_queue(rows: list[dict[str, str]], day: int, log: RunLog, dry: bool) -> None:
    cl_fields, cl = read(CACHE_LIST)
    q_fields, q = read(QUEUE)
    have_cl = {x["paper_id"] for x in cl}
    have_q = {x["paper_id"] for x in q}
    sessions = {
        "ieee": max((int(x["session"]) for x in q if x["route"].startswith("ieee") and x["session"]), default=0),
        "optica": max((int(x["session"]) for x in q if x["route"] == "optica_browser" and x["session"]), default=0),
    }
    counts = {"ieee": SESSION_CAP["ieee"], "optica": SESSION_CAP["optica"]}  # forces a new session on first use
    date = dt.date.today().isoformat()
    add_cl, add_q = [], []
    for r in rows:
        pid = r["paper_id"]
        if is_cached(r):
            log.event("queue", "skip_cached", paper_id=pid, source=r["already_in_repo"])
            continue
        route, url = route_of(r)
        au = authors_of(r)
        access = "oa" if route in ("arxiv", "oa_publisher", "optica_browser", "blog_copy") else "paywalled"
        if pid not in have_cl:
            add_cl.append(
                {f: "" for f in cl_fields}
                | {
                    "primary_class": r["component_class"] if r["component_class"] in CLASSES else "history",
                    "classes": r["component_class"],
                    "uid": r["doi"] or f"hist:{pid}",
                    "doi": r["doi"],
                    "arxiv_id": arxiv_id_of(r["oa_pdf"]) if route == "arxiv" else "",
                    "paper_id": pid,
                    "title": r["title"],
                    "first_author": au[0] if au else "",
                    "last_author": au[-1] if au else "",
                    "venue": r["venue"],
                    "venue_type": venue_type(r),
                    "year": r["year"],
                    "access": access,
                    "oa_url": url if access == "oa" else "",
                    "selection_reason": "history",
                    "rationale": r["significance"],
                }
            )
        if pid not in have_q:
            site = "ieee" if route.startswith("ieee") else ("optica" if route == "optica_browser" else "")
            session = ""
            if site:
                if counts[site] >= SESSION_CAP[site]:
                    sessions[site] += 1
                    counts[site] = 0
                counts[site] += 1
                session = str(sessions[site])
            add_q.append(
                {f: "" for f in q_fields}
                | {
                    "day": str(day), "date": date, "route": route, "session": session, "paper_id": pid,
                    "uid": r["doi"] or f"hist:{pid}", "doi": r["doi"],
                    "arxiv_id": arxiv_id_of(r["oa_pdf"]) if route == "arxiv" else "",
                    "route_url": url, "access": access,
                    "primary_class": r["component_class"] if r["component_class"] in CLASSES else "history",
                    "title": r["title"],
                }
            )  # fmt: skip
    # Re-route rows of this day that are not cached yet when the routing rule changed (e.g. IOP -> publisher_browser).
    by_pid = {r["paper_id"]: r for r in rows}
    pub_session = max((int(x["session"]) for x in q if x["route"] == "publisher_browser" and x["session"]), default=0)
    rerouted = 0
    for x in q:
        cand = by_pid.get(x["paper_id"])
        if cand is None or x["day"] != str(day) or (ROOT / "references" / x["paper_id"] / "source.pdf").exists():
            continue
        route, url = route_of(cand)
        if route == x["route"] or x["route"] == "oa_publisher" and is_bstj(cand):
            continue
        if route == "publisher_browser":
            if not rerouted or counts.get("publisher", 0) >= SESSION_CAP["optica"]:
                pub_session += 1
                counts["publisher"] = 0
            counts["publisher"] = counts.get("publisher", 0) + 1
        log.event("queue", "reroute", paper_id=x["paper_id"], old=x["route"], new=route)
        x.update(route=route, route_url=url, session=str(pub_session) if route == "publisher_browser" else "")
        x["access"] = "paywalled" if route == "manual" else x["access"]
        rerouted += 1
    log.info(f"queue: +{len(add_cl)} cache_list rows, +{len(add_q)} queue rows (day {day}), {rerouted} rerouted")
    if rerouted and not (add_cl or add_q) and not dry:
        log.info(f"backup {backup([CACHE_LIST, QUEUE], 'reroute').relative_to(ROOT)}")
        write(QUEUE, q_fields, q)
        return
    for x in add_q:
        log.event("queue", "add", paper_id=x["paper_id"], route=x["route"], session=x["session"])
    if dry or not (add_cl or add_q):
        return
    log.info(f"backup {backup([CACHE_LIST, QUEUE], 'queue').relative_to(ROOT)}")
    write(CACHE_LIST, cl_fields, cl + add_cl)
    write(QUEUE, q_fields, q + add_q)


def step_authors(rows: list[dict[str, str]], log: RunLog, dry: bool) -> None:
    have: dict[str, dict[str, Any]] = {}
    if ADDS.exists():
        for line in ADDS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                d = json.loads(line)
                have[d["uid"]] = d
    cl_uid = {x["paper_id"]: x["uid"] for x in read(CACHE_LIST)[1]}  # the cache_list uid is the join key
    n = 0
    for r in rows:
        if is_cached(r):
            continue
        uid = cl_uid.get(r["paper_id"]) or r["doi"] or f"hist:{r['paper_id']}"
        au = authors_of(r)
        rec = {
            "uid": uid, "doi": r["doi"], "paper_id": r["paper_id"], "title": r["title"], "year": int(r["year"]),
            "venue": r["venue"], "venue_type": venue_type(r), "authors": au, "n_authors": len(au),
            "last_author": au[-1] if au else "",
            "institutions": [x.strip() for x in r["institutions"].split(";") if x.strip()],
            "source": "history_candidates.csv (Crossref author list; DevLog-016)",
        }  # fmt: skip
        if have.get(uid) != rec:
            have[uid] = rec
            n += 1
    log.info(f"authors: {n} new / changed records ({len(have)} total)")
    if not dry and n:
        ADDS.parent.mkdir(parents=True, exist_ok=True)
        ADDS.write_text("".join(json.dumps(v, ensure_ascii=False) + "\n" for v in have.values()), encoding="utf-8")


def crossref(doi: str) -> dict[str, Any]:
    CR_CACHE.mkdir(parents=True, exist_ok=True)
    f = CR_CACHE / (re.sub(r"[^A-Za-z0-9]+", "_", doi) + ".json")
    if f.exists():
        return dict(json.loads(f.read_text()))
    msg = litfetch.get_json(f"https://api.crossref.org/works/{doi}")["message"]
    f.write_text(json.dumps(msg))
    return dict(msg)


def step_bstj(rows: list[dict[str, str]], log: RunLog, dry: bool) -> None:
    cache: dict[str, Any] = json.loads(BSTJ_CACHE.read_text()) if BSTJ_CACHE.exists() else {}
    for r in rows:
        if not is_bstj(r) or blog_source(r) or is_cached(r):
            continue
        pid = r["paper_id"]
        if cache.get(pid, {}).get("pdf_url"):
            continue
        m = re.search(r"archive\.org/details/(bstj[\d\-]+)", r["url"])
        item = m.group(1) if m else ""
        if not item and r["doi"]:
            cr = crossref(r["doi"])
            first = str(cr.get("page", "")).split("-")[0]
            item = f"bstj{cr.get('volume', '')}-{cr.get('issue', '')}-{first}"
        try:
            meta = litfetch.get_json(f"https://archive.org/metadata/{item}")
        except (litfetch.BlockedError, urllib.error.URLError) as e:
            log.info(f"bstj {pid}: {item} metadata failed: {e}; stop")
            log.event("bstj", "failed", paper_id=pid, item=item, error=str(e))
            break
        pdfs = [f["name"] for f in meta.get("files", []) if str(f.get("name", "")).lower().endswith(".pdf")]
        title = str((meta.get("metadata") or {}).get("title", ""))
        if not pdfs:
            log.info(f"bstj {pid}: no PDF in archive.org item {item!r} (title {title!r})")
            log.event("bstj", "no_pdf", paper_id=pid, item=item)
            cache[pid] = {"item": item, "pdf_url": "", "ia_title": title}
            continue
        url = f"https://archive.org/download/{item}/{pdfs[0]}"
        cache[pid] = {"item": item, "pdf_url": url, "ia_title": title}
        log.info(f"bstj {pid}: {item} -> {pdfs[0]} (ia title {title!r})")
        log.event("bstj", "ok", paper_id=pid, item=item, pdf=url, ia_title=title)
    if dry:
        return
    BSTJ_CACHE.write_text(json.dumps(cache, indent=1))
    q_fields, q = read(QUEUE)
    changed = 0
    for x in q:
        c = cache.get(x["paper_id"])
        if c and c.get("pdf_url") and x["route"] == "oa_publisher" and x["route_url"] != c["pdf_url"]:
            x["route_url"] = c["pdf_url"]
            changed += 1
    if changed:
        log.info(f"backup {backup([QUEUE], 'bstj').relative_to(ROOT)}; {changed} queue route_url(s) set")
        write(QUEUE, q_fields, q)


def step_blog(rows: list[dict[str, str]], blog_root: Path | None, log: RunLog, dry: bool) -> None:
    if blog_root is None:
        raise SystemExit("blog step needs --blog-root (the local blog repo)")
    src = {x["source_id"]: x for x in read(SOURCES)[1]}
    INBOX.mkdir(parents=True, exist_ok=True)
    for r in rows:
        sid = blog_source(r)
        if not sid or is_cached(r):
            continue
        pid = r["paper_id"]
        if (ROOT / "references" / pid / "source.pdf").exists() or (INBOX / f"{pid}.pdf").exists():
            log.event("blog", "skip_present", paper_id=pid)
            continue
        url = src.get(sid, {}).get("url", "")
        if not url.startswith(BLOG_URL_PREFIX):
            log.info(f"blog {pid}: {sid} has no blog-repo URL ({url!r})")
            log.event("blog", "no_url", paper_id=pid, source=sid)
            continue
        f = blog_root / urllib.parse.unquote(url[len(BLOG_URL_PREFIX) :])
        if not f.is_file():
            log.info(f"blog {pid}: file missing in the blog repo: {url[len(BLOG_URL_PREFIX) :]}")
            log.event("blog", "missing", paper_id=pid, source=sid)
            continue
        log.info(f"blog {pid}: copy {url[len(BLOG_URL_PREFIX) :]} -> references/_inbox/{pid}.pdf")
        log.event("blog", "copy", paper_id=pid, source=sid, bytes=f.stat().st_size)
        if not dry:
            shutil.copy2(f, INBOX / f"{pid}.pdf")


def step_manual(rows: list[dict[str, str]], log: RunLog, dry: bool) -> None:
    out = []
    for r in rows:
        if is_cached(r) or (ROOT / "references" / r["paper_id"] / "source.pdf").exists():
            continue
        route, _ = route_of(r)
        if route != "manual":
            continue
        out.append(r)
    out.sort(key=lambda r: (r["era"][:2], int(r["year"]), r["paper_id"]))
    lines = [
        "# Historical papers: owner downloads (DevLog-016)",
        "",
        f"Generated {dt.date.today().isoformat()} by `scripts/hist_prepare.py manual` from `history_candidates.csv` "
        "(core rows routed `manual`; IEEE / Optica rows that fail later are added to `manual_downloads.md` by "
        "`scripts/lit_manual_list.py`). Save each PDF as `references/_inbox/<save_as>`, then run "
        "`uv run python scripts/lit_ingest_inbox.py`.",
        "",
        f"Total: {len(out)}",
        "",
        "| # | era | save_as | year | venue | title | doi or url |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(out, 1):
        title = r["title"].replace("|", "/")
        ref = r["doi"] or r["url"] or "(no DOI, no URL)"
        lines.append(f"| {i} | {r['era'][:2]} | {r['paper_id']}.pdf | {r['year']} | {r['venue']} | {title} | {ref} |")
    log.info(f"manual: {len(out)} rows")
    if not dry:
        MANUAL.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("steps", nargs="+", choices=["queue", "authors", "bstj", "blog", "manual"])
    ap.add_argument("--tier", default="core", choices=["core", "reserve"])
    ap.add_argument("--day", type=int, default=101)
    ap.add_argument("--blog-root", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    rows = candidates(a.tier)
    with RunLog("hist_prepare", a.dry_run) as log:
        log.info(f"{len(rows)} {a.tier} rows; steps {a.steps}")
        for s in a.steps:
            if s == "queue":
                step_queue(rows, a.day, log, a.dry_run)
            elif s == "authors":
                step_authors(rows, log, a.dry_run)
            elif s == "bstj":
                step_bstj(rows, log, a.dry_run)
            elif s == "blog":
                step_blog(rows, a.blog_root, log, a.dry_run)
            elif s == "manual":
                step_manual(rows, log, a.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
