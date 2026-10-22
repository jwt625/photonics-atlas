"""Enumerate conference (or any) venue-years from Crossref filter lists into the literature pool (DevLog-006 S1, L2).

Reads the venues with `api: crossref` from a lane config (config/literature/venues_<lane>.yaml). Per venue:
  crossref_filter          filter-only Crossref query; `from-pub-date:<y>,until-pub-date:<y>` is appended per year
                           unless the filter already has from-pub-date
  crossref_filter_by_year  {year: filter} instead, for venues whose container title changes per year
  doi_regex / container_regex / item_match {field: value}   local routing of the items a filter returns
  enrich: openalex         records without a Crossref abstract are looked up in OpenAlex by DOI-batch filter lists
                           (doi:<a>|<b>|..., 100 DOIs per $0.0001 request) for abstract, affiliations, OA fields
Venues with the same filter and year share one cursor pass (rows=1000), so e.g. all Optica proceedings of a year are
paged once and split into OFC / CLEO / ACP / ... units. Before paging, one rows=0 request gives total-results; after
paging the number of items seen is checked against it (mismatch logged). Items whose DOI carries a year
(10.1364/ofc.2026.xxx) outside the venue's year range are dropped (keeps OFC 2026 out) unless the venue sets
doi_year_check: false (IET Conference Proceedings DOIs carry the registration year, not the conference year).

Output per venue-year: cache/literature/pool/<lane>_<key>_<year>.jsonl with the litpool fields, written as
<file>.part and renamed when complete, so reruns skip finished units. A venue-year with no matching item gets an empty
file (so the shared pass is not repeated).
--dry-run sends only the rows=0 count requests (total and has-abstract) per filter-year.

Usage: uv run python scripts/lit_harvest_crossref.py --config config/literature/venues_conferences.yaml
           [--only key,...] [--years 2020-2025] [--no-enrich] [--stop-at-usd 0.07] [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

from photonics_atlas import litpool
from photonics_atlas.litfetch import BlockedError, get_json, openalex_cost_today
from photonics_atlas.paths import ROOT
from photonics_atlas.runlog import RunLog

CROSSREF = "https://api.crossref.org/works"
OPENALEX = "https://api.openalex.org/works"
ROWS = 1000
DOI_BATCH = 100
SELECT = "DOI,title,author,container-title,published,issued,abstract,type,license,volume,issue,is-referenced-by-count"
_DOI_YEAR = re.compile(r"^10\.\d+/[a-z0-9_\-]+\.((?:19|20)\d\d)\.", re.I)
_SUP = re.compile(r"<(?:jats:)?sup\b[^<>]*>", re.I)
_INLINE = re.compile(r"</?(?:jats:)?(?:i|b|u|em|strong|sub|sup|sc|italic|bold)\b[^<>]*>", re.I)
_MARKUP = re.compile(r"</?(?:i|b|u|em|strong|sub|sup|sc|span|p|br|mml:[a-z]+|jats:[a-z\-]+)\b[^<>]*>", re.I)
_ABSTRACT_HEAD = re.compile(r"^(abstract|summary)[\s.:]+", re.I)


def load_config(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        cfg: dict[str, Any] = yaml.safe_load(f)
    if not cfg.get("lane") or not isinstance(cfg.get("venues"), list):
        raise ValueError(f"{path}: needs 'lane' and a 'venues' list")
    keys = [v["key"] for v in cfg["venues"]]
    if len(keys) != len(set(keys)):
        raise ValueError(f"{path}: duplicate venue keys")
    for v in cfg["venues"]:
        if v.get("api") == "crossref" and not (v.get("crossref_filter") or v.get("crossref_filter_by_year")):
            raise ValueError(f"{path}: crossref venue {v['key']} needs crossref_filter or crossref_filter_by_year")
    return cfg


def parse_years(spec: str | None) -> tuple[int, int] | None:
    if not spec:
        return None
    a, _, b = spec.partition("-")
    lo, hi = int(a), int(b or a)
    return (min(lo, hi), max(lo, hi))


def venue_years(venue: dict[str, Any], override: tuple[int, int] | None) -> list[int]:
    lo, hi = int(venue["years"][0]), int(venue["years"][1])
    if override:
        lo, hi = max(lo, override[0]), min(hi, override[1])
    by_year = venue.get("crossref_filter_by_year")
    years = list(range(hi, lo - 1, -1))
    return [y for y in years if not by_year or y in {int(k) for k in by_year}]


def unit_filter(venue: dict[str, Any], year: int) -> str:
    by_year = venue.get("crossref_filter_by_year")
    flt = str({int(k): v for k, v in by_year.items()}[year] if by_year else venue["crossref_filter"]).strip()
    if "from-pub-date" not in flt:
        flt += f",from-pub-date:{year},until-pub-date:{year}"
    return flt


def unit_path(lane: str, key: str, year: int) -> Path:
    return litpool.POOL / f"{lane}_{key}_{year}.jsonl"


def doi_year(doi: str) -> int | None:
    m = _DOI_YEAR.match(doi)
    return int(m.group(1)) if m else None


def first(xs: Any) -> str:
    return str(xs[0]) if isinstance(xs, list) and xs else ""


def clean(text: str | None) -> str:
    """Strip JATS / HTML tags (inline ones joined, <sup> -> ^), unescape entities, then strip double-escaped markup."""
    s = html.unescape(litpool.strip_jats(_INLINE.sub("", _SUP.sub("^", text or ""))))
    s = _MARKUP.sub(" ", _INLINE.sub("", _SUP.sub("^", s)))
    return re.sub(r"\s+", " ", s).strip()


def date_of(item: dict[str, Any]) -> str:
    for k in ("published", "issued"):
        parts = ((item.get(k) or {}).get("date-parts") or [[]])[0]
        parts = [p for p in parts if p is not None]
        if parts:
            return "-".join(f"{int(p):02d}" if i else str(int(p)) for i, p in enumerate(parts))
    return ""


def matches(venue: dict[str, Any], item: dict[str, Any]) -> bool:
    doi = litpool.norm_doi(item.get("DOI"))
    if venue.get("doi_regex") and not re.search(str(venue["doi_regex"]), doi, re.I):
        return False
    container = clean(first(item.get("container-title")))
    if venue.get("container_regex") and not re.search(str(venue["container_regex"]), container, re.I):
        return False
    for field, want in (venue.get("item_match") or {}).items():
        if str(item.get(field) or "") != str(want):
            return False
    if venue.get("doi_year_check", True) is False:
        return True
    y = doi_year(doi)
    lo, hi = int(venue["years"][0]), int(venue["years"][1])
    return y is None or lo <= y <= hi


def author_name(a: dict[str, Any]) -> str:
    return " ".join(x for x in (a.get("given"), a.get("family")) if x).strip() or str(a.get("name") or "")


def from_crossref(item: dict[str, Any], lane: str, discovered_via: str, year: int) -> dict[str, Any]:
    """Crossref work -> litpool record (same fields as litpool.from_openalex)."""
    doi = litpool.norm_doi(item.get("DOI"))
    auths = item.get("author") or []
    names = [author_name(a) for a in auths]
    inst: list[str] = []
    for a in auths[:1] + auths[-1:]:
        for af in a.get("affiliation") or []:
            n = clean(af.get("name"))
            if n and n not in inst:
                inst.append(n)
    lic = [str(x.get("URL") or "") for x in item.get("license") or []]
    cc = [u for u in lic if "creativecommons.org" in u]
    ctype = str(item.get("type") or "")
    return {
        "uid": doi,
        "doi": doi,
        "arxiv_id": "",
        "openalex_id": "",
        "title": clean(first(item.get("title"))),
        "year": year,
        "publication_date": date_of(item),
        "type": "conference-paper" if ctype == "proceedings-article" else ctype,
        "venue": clean(first(item.get("container-title"))),
        "venue_type": "conference",
        "authors": names[:30],
        "n_authors": len(names),
        "last_author": names[-1] if names else "",
        "institutions": inst,
        "abstract": _ABSTRACT_HEAD.sub("", clean(item.get("abstract"))),
        "is_oa": bool(cc),
        "oa_status": "",
        "oa_url": "",
        "license": (cc or lic or [""])[0],
        "cited_by_count": int(item.get("is-referenced-by-count") or 0),
        "lane": lane,
        "discovered_via": discovered_via,
        "harvested_on": dt.date.today().isoformat(),
    }


def merge_openalex(rec: dict[str, Any], oa: dict[str, Any]) -> dict[str, Any]:
    """Fill a Crossref record from the OpenAlex record of the same DOI; Crossref values win where present."""
    out = dict(rec)
    out["openalex_id"] = oa["openalex_id"]
    for k in ("abstract", "institutions", "oa_url"):
        if not out[k] and oa[k]:
            out[k] = oa[k]
    out["is_oa"] = bool(rec["is_oa"] or oa["is_oa"])
    out["oa_status"] = oa["oa_status"]
    out["license"] = rec["license"] or oa["license"]
    out["cited_by_count"] = max(int(rec["cited_by_count"]), int(oa["cited_by_count"]))
    out["discovered_via"] = rec["discovered_via"] + "+openalex:doi"
    return out


def enrich(recs: list[dict[str, Any]], lane: str, stop_at_usd: float | None) -> tuple[int, int]:
    """OpenAlex doi-batch lists for records without abstract. Returns (looked_up, filled). Raises BlockedError."""
    todo = [r for r in recs if not r["abstract"] and r["doi"] and "|" not in r["doi"] and "," not in r["doi"]]
    found: dict[str, dict[str, Any]] = {}
    for i in range(0, len(todo), DOI_BATCH):
        if stop_at_usd is not None and openalex_cost_today() >= stop_at_usd:
            raise BlockedError(f"--stop-at-usd {stop_at_usd} reached")
        batch = [r["doi"] for r in todo[i : i + DOI_BATCH]]
        res = get_json_retry(
            OPENALEX,
            {"filter": "doi:" + "|".join(batch), "per_page": DOI_BATCH, "select": litpool.OPENALEX_SELECT},
        )
        for w in res.get("results") or []:
            o = litpool.from_openalex(w, lane, "")
            if o["doi"]:
                found[o["doi"]] = o
    filled = 0
    for j, r in enumerate(recs):
        hit = found.get(r["doi"])
        if hit:
            recs[j] = merge_openalex(r, hit)
            filled += bool(recs[j]["abstract"])
    return len(todo), filled


def get_json_retry(url: str, params: dict[str, Any], attempts: int = 3) -> Any:
    """get_json with retries on a truncated body (HTTP 200 with incomplete JSON, seen 2026-10-22 on OpenAlex)."""
    for i in range(attempts):
        try:
            return get_json(url, params)
        except json.JSONDecodeError:
            if i == attempts - 1:
                raise
    return None


def count(flt: str) -> tuple[int, int]:
    tot = get_json(CROSSREF, {"filter": flt, "rows": 0})["message"]["total-results"]
    ab = get_json(CROSSREF, {"filter": flt + ",has-abstract:true", "rows": 0})["message"]["total-results"]
    return int(tot), int(ab)


def page_all(flt: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    cursor = "*"
    while cursor:
        m = get_json_retry(CROSSREF, {"filter": flt, "rows": ROWS, "cursor": cursor, "select": SELECT})["message"]
        got = m.get("items") or []
        items += got
        cursor = str(m.get("next-cursor") or "") if got else ""
    return items


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True, type=Path)
    ap.add_argument("--only", default="", help="comma-separated venue keys (crossref venues only)")
    ap.add_argument("--years", default="", help="e.g. 2020-2025 or 2023 (intersected with each venue's range)")
    ap.add_argument("--no-enrich", action="store_true", help="skip OpenAlex DOI enrichment")
    ap.add_argument("--stop-at-usd", type=float, default=None, help="stop enrichment once OpenAlex cost today >= this")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    cfg_path = args.config if args.config.is_absolute() else ROOT / args.config
    cfg = load_config(cfg_path)
    lane = str(cfg["lane"])
    only = {k.strip() for k in args.only.split(",") if k.strip()} or None
    venues = [v for v in cfg["venues"] if v.get("api") == "crossref" and (not only or v["key"] in only)]
    if only and len(venues) != len(only):
        print(f"unknown or non-crossref venue keys: {sorted(only - {v['key'] for v in venues})}", file=sys.stderr)
        return 2
    venues.sort(key=lambda v: int(v.get("priority", 9)))
    yrs = parse_years(args.years)
    # group venue-years by (filter, year): one cursor pass per group
    groups: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for v in venues:
        for y in venue_years(v, yrs):
            groups[(unit_filter(v, y), y)].append(v)
    with RunLog(f"lit_harvest_crossref_{lane}", args.dry_run) as log:
        try:
            for (flt, year), members in groups.items():
                keys = [v["key"] for v in members]
                pending = [v for v in members if not unit_path(lane, v["key"], year).exists()]
                if not args.dry_run and not pending:
                    log.info(f"{year} {keys}: done, skip")
                    continue
                total, with_abs = count(flt)
                log.info(f"{year} {keys}: filter {flt}: total {total}, with abstract {with_abs}")
                log.event("counts", year=year, keys=keys, filter=flt, total=total, with_abstract=with_abs)
                if args.dry_run or total == 0:
                    continue
                items = page_all(flt)
                if len(items) != total:
                    log.info(f"{year} {keys}: count mismatch, seen {len(items)} of {total}")
                    log.event("count_mismatch", year=year, keys=keys, seen=len(items), total=total)
                for v in pending:
                    key = v["key"]
                    via = f"crossref:{key}:{year}"
                    hits = [it for it in items if matches(v, it)]
                    off_year = sum(1 for it in hits if (doi_year(litpool.norm_doi(it.get("DOI"))) or year) != year)
                    recs = [from_crossref(it, lane, via, year) for it in hits]
                    looked = filled = 0
                    if v.get("enrich") == "openalex" and not args.no_enrich and recs:
                        looked, filled = enrich(recs, lane, args.stop_at_usd)
                    n_abs = sum(1 for r in recs if r["abstract"])
                    n_aff = sum(1 for r in recs if r["institutions"])
                    status = "done" if recs else "empty"
                    out = unit_path(lane, key, year)
                    part = out.with_name(out.name + ".part")
                    part.parent.mkdir(parents=True, exist_ok=True)
                    part.write_text("", encoding="utf-8")
                    litpool.append(part, recs)
                    part.rename(out)
                    log.info(
                        f"{key} {year}: {len(recs)} records, abstract {n_abs}, affiliations {n_aff}, "
                        f"doi-year != pub-year {off_year}, enrich looked {looked} filled {filled} ({status})"
                    )
                    log.event(
                        "unit",
                        status,
                        key=key,
                        year=year,
                        written=len(recs),
                        abstract=n_abs,
                        affiliations=n_aff,
                        off_year=off_year,
                        enrich_looked=looked,
                        enrich_filled=filled,
                        cost_today=openalex_cost_today(),
                    )
        except BlockedError as e:
            log.info(f"blocked: {e}; rerun the same command after the breaker / cap clears")
            log.event("blocked", "blocked", error=str(e), cost_today=openalex_cost_today())
            return 3
        log.info(f"OpenAlex cost today (all agents): ${openalex_cost_today():.4f}")
        print(json.dumps({"lane": lane, "cost_today_usd": openalex_cost_today()}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
