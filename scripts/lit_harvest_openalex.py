"""Enumerate every work of a venue list per venue-year from OpenAlex filter lists into the literature pool (DevLog-006 S1).

Generic over lanes: the config (config/literature/venues_<lane>.yaml) names the lane (pool file prefix), the work types
kept, and per venue an OpenAlex source id (resolved from the ISSN with a free singleton get when empty), a year range
and an optional filter-only extra term. Per venue-year the filter is
    primary_location.source.id:<id>,publication_year:<y>,type:<types>[,<extra_filter>]
paged with page=N (cursor paging needs an API key), per_page=200, select=OPENALEX_SELECT ($0.0001 per page). Each venue first costs one
group_by=publication_year request (per-year expected counts; years with 0 works are skipped without a file). Output per
venue-year: cache/literature/pool/<lane>_<key>_<year>.jsonl, written as <file>.part and renamed when complete, so
reruns skip finished units. Harvested count is checked against meta.count (mismatch logged, file kept).

--dry-run sends only the per-venue group_by request and prints expected works, pages and cost.

Usage: uv run python scripts/lit_harvest_openalex.py --config config/literature/venues_journals.yaml
           [--only key,...] [--years 2020-2026] [--max-pages N] [--stop-at-usd 0.07] [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

import yaml

from photonics_atlas import litpool
from photonics_atlas.litfetch import BlockedError, get_json, openalex_cost_today
from photonics_atlas.paths import ROOT
from photonics_atlas.runlog import RunLog

API = "https://api.openalex.org"
PER_PAGE = 200
PAGE_COST_USD = 0.0001
DEFAULT_TYPES = "article|review|letter"
MAX_PAGED = 10_000


def load_config(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        cfg: dict[str, Any] = yaml.safe_load(f)
    if not cfg.get("lane") or not isinstance(cfg.get("venues"), list):
        raise ValueError(f"{path}: needs 'lane' and a 'venues' list")
    keys = [v["key"] for v in cfg["venues"]]
    if len(keys) != len(set(keys)):
        raise ValueError(f"{path}: duplicate venue keys")
    return cfg


def parse_years(spec: str | None) -> tuple[int, int] | None:
    if not spec:
        return None
    a, _, b = spec.partition("-")
    lo, hi = int(a), int(b or a)
    return (min(lo, hi), max(lo, hi))


def venue_years(venue: dict[str, Any], override: tuple[int, int] | None) -> list[int]:
    """Years to harvest, newest first: the venue range intersected with the --years override."""
    lo, hi = int(venue["years"][0]), int(venue["years"][1])
    if override:
        lo, hi = max(lo, override[0]), min(hi, override[1])
    return list(range(hi, lo - 1, -1))


def base_filter(source_id: str, types: str, extra: str) -> str:
    parts = [f"primary_location.source.id:{source_id}"]
    if types:
        parts.append(f"type:{types}")
    if extra.strip():
        parts.append(extra.strip())
    return ",".join(parts)


def unit_filter(source_id: str, year: int, types: str, extra: str) -> str:
    return base_filter(source_id, types, extra) + f",publication_year:{year}"


def pages_for(count: int) -> int:
    return max(1, math.ceil(count / PER_PAGE))


def unit_path(lane: str, key: str, year: int) -> Path:
    return litpool.POOL / f"{lane}_{key}_{year}.jsonl"


def order_venues(venues: list[dict[str, Any]], only: set[str] | None) -> list[dict[str, Any]]:
    """Priority ascending, config order within a priority; --only restricts to the listed keys."""
    sel = [v for v in venues if not only or v["key"] in only]
    return sorted(sel, key=lambda v: (int(v.get("priority", 9)), venues.index(v)))


def resolve_source(venue: dict[str, Any], log: RunLog) -> str:
    sid = str(venue.get("openalex_source_id") or "").strip()
    if sid:
        return sid
    s = get_json(f"{API}/sources/issn:{venue['issn']}")
    sid = str(s["id"]).rsplit("/", 1)[-1]
    log.info(
        f"{venue['key']}: resolved issn {venue['issn']} -> {sid} ({s.get('display_name')}); record it in the config"
    )
    log.event("resolve_source", key=venue["key"], issn=venue["issn"], source_id=sid, name=s.get("display_name"))
    return sid


def year_counts(source_id: str, types: str, extra: str, years: list[int]) -> dict[int, int]:
    """One group_by=publication_year request for the venue's whole year range."""
    f = base_filter(source_id, types, extra) + f",publication_year:{min(years)}-{max(years)}"
    r = get_json(f"{API}/works", {"filter": f, "group_by": "publication_year"})
    got = {int(g["key"]): int(g["count"]) for g in r.get("group_by") or []}
    return {y: got.get(y, 0) for y in years}


def harvest_unit(lane: str, key: str, year: int, flt: str, max_pages: int | None) -> tuple[int, int, bool]:
    """Page one venue-year into <file>.part; rename when complete. Returns (expected, written, complete).

    Uses page=N paging (cursor paging beyond page 1 returned HTTP 401 without an API key, 2026-10-21); page paging
    reaches the first 10,000 results, so a larger unit raises and must be split (e.g. by publication_date range).
    """
    out = unit_path(lane, key, year)
    part = out.with_name(out.name + ".part")
    part.parent.mkdir(parents=True, exist_ok=True)
    part.write_text("", encoding="utf-8")
    expected, written, page = -1, 0, 1
    seen: set[str] = set()
    via = f"openalex:source-year:{key}:{year}"
    while expected < 0 or (page - 1) * PER_PAGE < expected:
        if max_pages is not None and page > max_pages:
            return expected, written, False
        r = get_json(
            f"{API}/works",
            {"filter": flt, "per_page": PER_PAGE, "page": page, "select": litpool.OPENALEX_SELECT},
        )
        if expected < 0:
            expected = int(r["meta"]["count"])
            if expected > MAX_PAGED:
                raise ValueError(f"{key} {year}: {expected} works > {MAX_PAGED}; split the unit")
        results = r.get("results") or []
        recs = []
        for w in results:
            wid = str(w.get("id") or "")
            if wid in seen:
                continue
            seen.add(wid)
            recs.append(litpool.from_openalex(w, lane, via))
        written += litpool.append(part, recs)
        if not results:
            break
        page += 1
    part.rename(out)
    return expected, written, True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True, type=Path)
    ap.add_argument("--only", default="", help="comma-separated venue keys")
    ap.add_argument("--years", default="", help="e.g. 2020-2026 or 2024 (intersected with each venue's range)")
    ap.add_argument(
        "--max-pages", type=int, default=None, help="pages per venue-year (pilot); truncated units stay .part"
    )
    ap.add_argument(
        "--stop-at-usd", type=float, default=None, help="stop before a unit once today's OpenAlex cost >= this"
    )
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    cfg_path = args.config if args.config.is_absolute() else ROOT / args.config
    cfg = load_config(cfg_path)
    lane = str(cfg["lane"])
    default_types = str(cfg.get("types") or DEFAULT_TYPES)
    only = {k.strip() for k in args.only.split(",") if k.strip()} or None
    yrs = parse_years(args.years)
    venues = order_venues(cfg["venues"], only)
    if only and len(venues) != len(only):
        print(f"unknown venue keys: {sorted(only - {v['key'] for v in venues})}", file=sys.stderr)
        return 2
    with RunLog(f"lit_harvest_openalex_{lane}", args.dry_run) as log:
        tot_works = tot_pages = 0
        try:
            for v in venues:
                key = v["key"]
                years = venue_years(v, yrs)
                if not years:
                    continue
                types = str(v.get("types") or default_types)
                extra = str(v.get("extra_filter") or "")
                todo = [y for y in years if not unit_path(lane, key, y).exists()]
                if not args.dry_run and not todo:
                    log.info(f"{key}: all {len(years)} years done, skip")
                    continue
                if args.stop_at_usd is not None and openalex_cost_today() >= args.stop_at_usd:
                    log.info(f"stop: OpenAlex cost today {openalex_cost_today():.4f} >= {args.stop_at_usd}")
                    log.event("stop", reason="stop_at_usd", cost=openalex_cost_today())
                    break
                sid = resolve_source(v, log)
                counts = year_counts(sid, types, extra, years)
                pages = {y: (pages_for(c) if c else 0) for y, c in counts.items()}
                n, p = sum(counts.values()), sum(pages.values())
                log.info(f"{key} {sid}: {n} works in {years[-1]}-{years[0]}, {p} pages, est ${p * PAGE_COST_USD:.4f}")
                log.event(
                    "counts",
                    key=key,
                    source_id=sid,
                    counts=counts,
                    pages=pages,
                    works=n,
                    filter_types=types,
                    extra_filter=extra,
                )
                if args.dry_run:
                    tot_works += n
                    tot_pages += p
                    continue
                todo_pages = sum(pages[y] for y in todo)
                log.info(f"{key}: {len(todo)} years to harvest, {todo_pages} pages")
                for y in todo:
                    if counts[y] == 0:
                        log.event("unit", key=key, year=y, status="empty")
                        continue
                    if args.stop_at_usd is not None and openalex_cost_today() >= args.stop_at_usd:
                        raise BlockedError(f"--stop-at-usd {args.stop_at_usd} reached")
                    exp, got, complete = harvest_unit(lane, key, y, unit_filter(sid, y, types, extra), args.max_pages)
                    status = "done" if complete and got == exp else ("truncated" if not complete else "count_mismatch")
                    log.info(f"{key} {y}: expected {exp} group_by {counts[y]} written {got} {status}")
                    log.event(
                        "unit",
                        key=key,
                        year=y,
                        status=status,
                        expected=exp,
                        group_by=counts[y],
                        written=got,
                        cost_today=openalex_cost_today(),
                    )
        except BlockedError as e:
            log.info(f"blocked: {e}; rerun the same command after the breaker / cap clears")
            log.event("blocked", "blocked", error=str(e), cost_today=openalex_cost_today())
            return 3
        if args.dry_run:
            log.info(f"dry-run total: {tot_works} works, {tot_pages} pages, est ${tot_pages * PAGE_COST_USD:.4f}")
            log.event("dry_run_total", works=tot_works, pages=tot_pages, usd=round(tot_pages * PAGE_COST_USD, 4))
        log.info(f"OpenAlex cost today (all agents): ${openalex_cost_today():.4f}")
        print(json.dumps({"lane": lane, "cost_today_usd": openalex_cost_today()}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
