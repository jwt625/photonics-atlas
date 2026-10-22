"""Harvest arXiv preprints into the literature pool (DevLog-006 S1, lane L3), one file per month, newest first.

Sets (each a separate file per month in cache/literature/pool/):
  optics  arxiv_optics_YYYY-MM.jsonl  cat:physics.optics (primary or cross-list), no keyword restriction
  appq    arxiv_appq_YYYY-MM.jsonl    (cat:physics.app-ph OR cat:quant-ph), not cross-listed to physics.optics, restricted to
                                      abstracts matching APPQ_KEYWORDS (integrated-photonics terms)
Windows are by submittedDate (first version); a window with more than SPLIT_AT results is split into day ranges.
Every request goes through photonics_atlas.litfetch (lock, >= 3.5 s spacing, breaker on 403/429/503). The run stops at
the first BlockedError / HTTP error and prints the resume command. Month files are written atomically (.part then
rename) and skipped when present; a month whose fetched count does not reach opensearch:totalResults is not written.

Usage: uv run python scripts/lit_harvest_arxiv.py [--dry-run] [--start 2018-01] [--end 2026-10] [--sets optics,appq]
         [--page-size 500] [--max-minutes 8] [--max-months N]
"""

from __future__ import annotations

import argparse
import calendar
import datetime as dt
import json
import re
import sys
import time
import urllib.error
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from photonics_atlas import litfetch
from photonics_atlas.litpool import POOL, norm_doi
from photonics_atlas.runlog import RunLog

API = "http://export.arxiv.org/api/query"
LANE = "arxiv"
SPLIT_AT = 1900
NS = {
    "a": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
    "os": "http://a9.com/-/spec/opensearch/1.1/",
}
APPQ_KEYWORDS = (
    'abs:waveguide OR abs:waveguides OR abs:"integrated photonic" OR abs:"integrated photonics" '
    'OR abs:"integrated optics" OR abs:"integrated optical" OR abs:"photonic integrated" OR abs:"photonic chip" '
    'OR abs:"silicon photonics" OR abs:"silicon photonic" OR abs:"on-chip" OR abs:microring OR abs:"ring resonator" '
    'OR abs:"lithium niobate" OR abs:"silicon nitride"'
)
SET_QUERY = {
    "optics": "cat:physics.optics AND {date}",
    # ANDNOT must come last: "A ANDNOT B AND (C)" is mis-parsed by the arXiv API (probe 2026-10-21: 189430 hits).
    "appq": f"(cat:physics.app-ph OR cat:quant-ph) AND ({APPQ_KEYWORDS}) AND {{date}} ANDNOT cat:physics.optics",
}
_VER = re.compile(r"v\d+$")
_WS = re.compile(r"\s+")


class HarvestError(RuntimeError):
    """A window could not be fetched completely (short pages after retry, API error entry)."""


@dataclass
class Feed:
    total: int
    entries: list[dict[str, Any]]


def _text(el: ET.Element | None) -> str:
    return _WS.sub(" ", el.text or "").strip() if el is not None and el.text else ""


def arxiv_id_from_url(url: str) -> str:
    """http://arxiv.org/abs/2101.00001v2 -> 2101.00001; old style quant-ph/0101001v1 -> quant-ph/0101001."""
    tail = url.split("/abs/", 1)[-1].strip()
    return _VER.sub("", tail)


def parse_feed(xml: bytes) -> Feed:
    """Parse an arXiv API Atom page into (totalResults, raw entry dicts). Raises HarvestError on an API error entry."""
    root = ET.fromstring(xml)
    total = int(_text(root.find("os:totalResults", NS)) or 0)
    entries: list[dict[str, Any]] = []
    for e in root.findall("a:entry", NS):
        url = _text(e.find("a:id", NS))
        if "/api/errors" in url:
            raise HarvestError(f"arXiv API error: {_text(e.find('a:summary', NS))}")
        authors = []
        for a in e.findall("a:author", NS):
            affs = [_text(x) for x in a.findall("arxiv:affiliation", NS) if _text(x)]
            authors.append({"name": _text(a.find("a:name", NS)), "affiliations": affs})
        prim = e.find("arxiv:primary_category", NS)
        lic = e.find("a:rights", NS)
        entries.append(
            {
                "id_url": url,
                "title": _text(e.find("a:title", NS)),
                "summary": _text(e.find("a:summary", NS)),
                "published": _text(e.find("a:published", NS)),
                "updated": _text(e.find("a:updated", NS)),
                "authors": authors,
                "primary": prim.get("term", "") if prim is not None else "",
                "categories": [c.get("term", "") for c in e.findall("a:category", NS) if c.get("term")],
                "doi": _text(e.find("arxiv:doi", NS)),
                "journal_ref": _text(e.find("arxiv:journal_ref", NS)),
                "comment": _text(e.find("arxiv:comment", NS)),
                "license": _text(lic),
            }
        )
    return Feed(total, entries)


def to_record(e: dict[str, Any], discovered_via: str, today: str) -> dict[str, Any]:
    """Map a parsed entry to the litpool record layout (uid stays arxiv:<id> even when a journal DOI is present)."""
    aid = arxiv_id_from_url(e["id_url"])
    names = [a["name"] for a in e["authors"]]
    inst: list[str] = []
    for a in e["authors"][:1] + e["authors"][-1:]:
        for n in a["affiliations"]:
            if n not in inst:
                inst.append(n)
    dois = e["doi"].split()
    pub = e["published"][:10]
    return {
        "uid": f"arxiv:{aid}",
        "doi": norm_doi(dois[0]) if dois else "",
        "arxiv_id": aid,
        "openalex_id": "",
        "title": e["title"],
        "year": int(pub[:4]) if pub else None,
        "publication_date": pub,
        "type": "preprint",
        "venue": "arXiv",
        "venue_type": "repository",
        "authors": names[:30],
        "n_authors": len(names),
        "last_author": names[-1] if names else "",
        "institutions": inst,
        "abstract": e["summary"],
        "is_oa": True,
        "oa_status": "",
        "oa_url": f"https://arxiv.org/pdf/{aid}",
        "license": e["license"],
        "cited_by_count": None,
        "lane": LANE,
        "discovered_via": discovered_via,
        "harvested_on": today,
        "arxiv_primary": e["primary"],
        "arxiv_categories": e["categories"],
        "arxiv_updated": e["updated"][:10],
        "arxiv_journal_ref": e["journal_ref"],
        "arxiv_comment": e["comment"],
        "arxiv_dois": [norm_doi(d) for d in dois],
    }


def month_list(start: str, end: str) -> list[tuple[int, int]]:
    """Months from end back to start inclusive (newest first); arguments YYYY-MM."""
    y0, m0 = map(int, start.split("-"))
    y, m = map(int, end.split("-"))
    out = []
    while (y, m) >= (y0, m0):
        out.append((y, m))
        y, m = (y, m - 1) if m > 1 else (y - 1, 12)
    return out


def date_query(base: str, d0: dt.date, d1: dt.date) -> str:
    return base.replace("{date}", f"submittedDate:[{d0:%Y%m%d}0000 TO {d1:%Y%m%d}2359]")


def fetch_page(query: str, start: int, size: int) -> Feed:
    body = litfetch.get(
        API,
        {
            "search_query": query,
            "start": start,
            "max_results": size,
            "sortBy": "submittedDate",
            "sortOrder": "ascending",
        },
    )
    return parse_feed(body)


def fetch_window(
    base: str, d0: dt.date, d1: dt.date, size: int, log: RunLog, stats: Counter[str]
) -> list[dict[str, Any]]:
    """All entries of one date window; splits the window in two when it exceeds SPLIT_AT results."""
    q = date_query(base, d0, d1)
    first = fetch_page(q, 0, size)
    stats["requests"] += 1
    if first.total > SPLIT_AT and d0 < d1:
        mid = d0 + (d1 - d0) // 2
        log.info(f"  split {d0}..{d1} total={first.total}")
        return fetch_window(base, d0, mid, size, log, stats) + fetch_window(
            base, mid + dt.timedelta(days=1), d1, size, log, stats
        )
    if first.total > SPLIT_AT:
        log.info(f"  warning: single day {d0} has {first.total} results (> {SPLIT_AT})")
    got = list(first.entries)
    retries = 0
    while len(got) < first.total:
        page = fetch_page(q, len(got), size)
        stats["requests"] += 1
        if not page.entries:
            retries += 1
            stats["empty_page_retries"] += 1
            if retries > 2:
                raise HarvestError(f"window {d0}..{d1}: {len(got)}/{first.total} after {retries - 1} empty retries")
            continue
        got.extend(page.entries)
    if len(got) < first.total:
        raise HarvestError(f"window {d0}..{d1}: {len(got)}/{first.total}")
    log.info(f"  window {d0}..{d1} total={first.total} got={len(got)}")
    return got


def harvest_month(
    set_name: str, y: int, m: int, size: int, log: RunLog, stats: Counter[str], today: str
) -> tuple[Path, int]:
    d0 = dt.date(y, m, 1)
    d1 = dt.date(y, m, calendar.monthrange(y, m)[1])
    base = SET_QUERY[set_name]
    entries = fetch_window(base, d0, d1, size, log, stats)
    via = "arxiv api: " + base.replace("{date}", f"submittedDate {d0}..{d1}")
    seen: set[str] = set()
    recs = []
    for e in entries:
        if set_name == "appq" and "physics.optics" in e["categories"]:
            stats["appq_optics_dropped"] += 1
            continue
        r = to_record(e, via, today)
        if r["uid"] in seen:
            stats["dup_in_month"] += 1
            continue
        seen.add(r["uid"])
        recs.append(r)
    out = POOL / f"arxiv_{set_name}_{y:04d}-{m:02d}.jsonl"
    part = out.with_name(out.name + ".part")
    POOL.mkdir(parents=True, exist_ok=True)
    with part.open("w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    part.rename(out)
    return out, len(recs)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--start", default="2018-01")
    ap.add_argument("--end", default="2026-10")
    ap.add_argument("--sets", default="optics,appq")
    ap.add_argument("--page-size", type=int, default=500)
    ap.add_argument("--max-minutes", type=float, default=8.0, help="do not start a new month after this many minutes")
    ap.add_argument("--max-months", type=int, default=0, help="stop after this many fetched month files (0 = no limit)")
    args = ap.parse_args()
    sets = [s for s in args.sets.split(",") if s]
    for s in sets:
        if s not in SET_QUERY:
            ap.error(f"unknown set {s}")
    today = dt.date.today().isoformat()
    t0 = time.time()
    stats: Counter[str] = Counter()
    with RunLog("lit_harvest_arxiv", args.dry_run) as log:
        for y, m in month_list(args.start, args.end):
            for s in sets:
                out = POOL / f"arxiv_{s}_{y:04d}-{m:02d}.jsonl"
                if out.exists():
                    stats["skipped_existing"] += 1
                    continue
                if args.dry_run:
                    d1 = dt.date(y, m, calendar.monthrange(y, m)[1])
                    log.info(f"dry-run {out.name}: {date_query(SET_QUERY[s], dt.date(y, m, 1), d1)}")
                    continue
                if (time.time() - t0) / 60 > args.max_minutes or (
                    args.max_months and stats["months"] >= args.max_months
                ):
                    log.info(f"time/month budget reached before {s} {y:04d}-{m:02d}; rerun the same command to resume")
                    log.event("budget", "stopped", next=f"{s} {y:04d}-{m:02d}", stats=dict(stats))
                    return 0
                try:
                    path, n = harvest_month(s, y, m, args.page_size, log, stats, today)
                except (litfetch.BlockedError, urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
                    log.info(f"STOP at {s} {y:04d}-{m:02d}: {type(e).__name__}: {e}")
                    log.event("month", "blocked", set=s, month=f"{y:04d}-{m:02d}", error=str(e), stats=dict(stats))
                    log.info("resume: uv run python scripts/lit_harvest_arxiv.py (after the breaker cooldown)")
                    return 2
                except (HarvestError, ET.ParseError) as e:
                    log.info(f"FAIL {s} {y:04d}-{m:02d}: {e} (not written; rerun retries it)")
                    log.event("month", "failed", set=s, month=f"{y:04d}-{m:02d}", error=str(e))
                    stats["failed_months"] += 1
                    continue
                stats["months"] += 1
                stats["records"] += n
                log.info(f"{path.name}: {n} records (requests so far {stats['requests']})")
                log.event("month", set=s, month=f"{y:04d}-{m:02d}", records=n, file=path.name)
        log.info(f"stats {dict(stats)}")
        log.event("summary", stats=dict(stats))
    return 0


if __name__ == "__main__":
    sys.exit(main())
