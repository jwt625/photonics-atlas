"""B3 + B5 of DevLog-019: resolve cited reference strings to DOI / arXiv ids, then enrich with OpenAlex metadata.

Input: cache/literature/bench/extract/*.jsonl (`item` records from the extraction agents).
Steps per unique reference string:
  1. DOI / arXiv id printed in the string;
  2. quoted title -> exact normalized-title match in the OpenAlex pool (cache/literature/merged.jsonl) or sources.csv;
  3. Crossref `query.bibliographic` (free, via litfetch: per-host lock, 1 s spacing, breaker), accepted only when
     verified: first-author surname in the string, year within 1, and title similarity >= 0.8 (quoted title) or
     volume / first page printed in the string (no title).
Enrichment: DOIs not in the pool are fetched from OpenAlex with `filter=doi:a|b|...` (50 per page, filter-only list
cost) -> OA status, venue, type, abstract.

Outputs (git-ignored, resumable): cache/literature/bench/resolve_cache.jsonl (one line per reference string key),
cache/literature/bench/openalex_cache.jsonl (one OpenAlex record per DOI), log logs/bench_resolve_<ts>.log.
Use --limit N for a pilot, --no-network to stop after the local steps, --dry-run to count only.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from photonics_atlas import litfetch  # noqa: E402
from photonics_atlas.litpool import from_openalex, norm_doi, norm_title  # noqa: E402

BENCH = ROOT / "cache" / "literature" / "bench"
RESOLVE_CACHE = BENCH / "resolve_cache.jsonl"
OA_CACHE = BENCH / "openalex_cache.jsonl"
CROSSREF = "https://api.crossref.org/works"
OPENALEX = "https://api.openalex.org/works"

DOI_RE = re.compile(r"\b(10\.\d{4,9}/[^\s\"<>,;]+[^\s\"<>,;.)\]])", re.I)
ARXIV_RE = re.compile(r"arxiv(?:\.org/abs/|:\s*|\s+)(\d{4}\.\d{4,5})", re.I)
TITLE_RE = re.compile(r"[\"“”„«]([^\"“”„»]{12,300}?)[,.]?[\"“”»]")
YEAR_RE = re.compile(r"\b(19[5-9]\d|20[0-3]\d)\b")


def ref_key(ref: str) -> str:
    return hashlib.sha1(re.sub(r"\s+", " ", ref.strip().lower()).encode()).hexdigest()[:16]


def fold(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def parse_ref(ref: str) -> dict[str, Any]:
    out: dict[str, Any] = {}
    m = DOI_RE.search(ref)
    if m:
        out["doi"] = norm_doi(m.group(1))
    m = ARXIV_RE.search(ref)
    if m:
        out["arxiv_id"] = m.group(1)
    m = TITLE_RE.search(ref)
    if m:
        out["title"] = m.group(1).strip()
    years = [int(y) for y in YEAR_RE.findall(ref)]
    if years:
        out["year"] = years[-1]
    return out


def verify(cand: dict[str, Any], ref: str, parsed: dict[str, Any]) -> tuple[bool, float, str]:
    fref = fold(ref)
    authors = cand.get("author") or []
    fam = fold(authors[0].get("family") or authors[0].get("name") or "") if authors else ""
    if not fam or fam.split()[-1] not in fref:
        return False, 0.0, "author"
    issued = ((cand.get("issued") or {}).get("date-parts") or [[None]])[0][0]
    if parsed.get("year") and issued and abs(int(issued) - int(parsed["year"])) > 1:
        return False, 0.0, "year"
    ctitle = norm_title((cand.get("title") or [""])[0])
    if parsed.get("title"):
        sim = SequenceMatcher(None, norm_title(parsed["title"]), ctitle).ratio()
        return sim >= 0.8, sim, "title"
    # unquoted titles (IOP / Nature styles): the candidate's title words appear in the reference string
    words = [w for w in ctitle.split() if len(w) > 3]
    nref = norm_title(fold(ref))
    if len(words) >= 3 and sum(w in nref for w in words) >= 0.85 * len(words):
        return True, 0.85, "title_in_ref"
    page = str(cand.get("page") or "").split("-")[0].strip()
    vol = str(cand.get("volume") or "").strip()
    nums = set(re.findall(r"\b[A-Za-z]?\d+[A-Za-z]?\b", ref))
    if page and page in nums:
        return True, 0.9, "page"
    if vol and vol in nums and issued and parsed.get("year") == int(issued):
        return True, 0.75, "volume+year"
    return False, 0.0, "no_page_volume"


def load_jsonl(p: Path) -> list[dict[str, Any]]:
    """Rows of a JSONL file; a partial last line (file still being written by an agent) is skipped."""
    out: list[dict[str, Any]] = []
    if p.exists():
        for x in p.read_text().splitlines():
            try:
                out.append(json.loads(x))
            except json.JSONDecodeError:
                continue
    return out


def build_local_index() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    by_title: dict[str, dict[str, Any]] = {}
    by_doi: dict[str, dict[str, Any]] = {}
    with open(ROOT / "cache" / "literature" / "merged.jsonl") as f:
        for line in f:
            r = json.loads(line)
            rec = {
                k: r.get(k)
                for k in (
                    "uid",
                    "doi",
                    "arxiv_id",
                    "openalex_id",
                    "title",
                    "year",
                    "venue",
                    "venue_type",
                    "type",
                    "is_oa",
                    "oa_status",
                    "oa_url",
                    "license",
                    "cited_by_count",
                    "authors",
                    "abstract",
                )
            }
            t = norm_title(r.get("title"))
            if len(t) > 25:
                by_title.setdefault(t, rec)
            if r.get("doi"):
                by_doi.setdefault(norm_doi(r["doi"]), rec)
    with open(ROOT / "data" / "registry" / "sources.csv", newline="") as f:
        for r in csv.DictReader(f):
            rec = {
                "doi": norm_doi(r["doi"]),
                "arxiv_id": r["arxiv_id"],
                "title": r["title"],
                "year": r["year"],
                "venue": r["venue"],
                "source_id": r["source_id"],
            }
            t = norm_title(r["title"])
            if len(t) > 25:
                by_title.setdefault(t, rec)
    return by_title, by_doi


def crossref_lookup(ref: str, parsed: dict[str, Any]) -> dict[str, Any]:
    q = re.sub(r"\s+", " ", ref)[:300]
    data = litfetch.get_json(
        CROSSREF,
        {"query.bibliographic": q, "rows": 3, "select": "DOI,title,author,issued,container-title,page,volume,type"},
    )
    best: dict[str, Any] = {"method": "crossref", "status": "unresolved"}
    for cand in (data.get("message") or {}).get("items") or []:
        ok, score, why = verify(cand, ref, parsed)
        if ok:
            return {
                "method": f"crossref_{why}",
                "status": "resolved",
                "doi": norm_doi(cand.get("DOI")),
                "score": round(score, 3),
                "cr_title": (cand.get("title") or [""])[0],
                "cr_year": ((cand.get("issued") or {}).get("date-parts") or [[None]])[0][0],
                "cr_venue": (cand.get("container-title") or [""])[0],
                "cr_type": cand.get("type"),
            }
        best.setdefault("reject", []).append(why)
    return best


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--limit", type=int, default=0, help="max new Crossref queries this run (pilot)")
    ap.add_argument("--no-network", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    log = open(ROOT / "logs" / f"bench_resolve_{ts}.log", "w")

    refs: dict[str, str] = {}
    for p in sorted((BENCH / "extract").glob("*.jsonl")):
        for r in load_jsonl(p):
            if r.get("type") == "item" and (r.get("ref") or "").strip():
                refs.setdefault(ref_key(r["ref"]), r["ref"].strip())
    done = {r["key"]: r for r in load_jsonl(RESOLVE_CACHE)}
    todo = {k: v for k, v in refs.items() if k not in done or done[k].get("status") == "error"}
    print(f"unique refs {len(refs)}, cached {len(done)}, todo {len(todo)}", file=log, flush=True)
    print(f"unique refs {len(refs)}, cached {len(done)}, todo {len(todo)}")
    if a.dry_run:
        return
    by_title, by_doi = build_local_index()
    n_cr = 0
    with RESOLVE_CACHE.open("a") as out:
        for k, ref in todo.items():
            parsed = parse_ref(ref)
            res: dict[str, Any] = {"key": k, "ref": ref, **{f"p_{x}": y for x, y in parsed.items()}}
            if parsed.get("doi"):
                res.update(method="printed_doi", status="resolved", doi=parsed["doi"])
            elif parsed.get("arxiv_id"):
                res.update(method="printed_arxiv", status="resolved", arxiv_id=parsed["arxiv_id"])
            elif parsed.get("title") and norm_title(parsed["title"]) in by_title:
                hit = by_title[norm_title(parsed["title"])]
                res.update(
                    method="local_title",
                    status="resolved",
                    doi=hit.get("doi") or "",
                    arxiv_id=hit.get("arxiv_id") or "",
                    source_id=hit.get("source_id", ""),
                )
            elif a.no_network or (a.limit and n_cr >= a.limit):
                continue
            else:
                n_cr += 1
                try:
                    res.update(crossref_lookup(ref, parsed))
                except litfetch.BlockedError as e:
                    print(f"blocked: {e}", file=log, flush=True)
                    break
                except Exception as e:  # network / parse error: record and retry next run
                    res.update(method="crossref", status="error", error=str(e)[:200])
            out.write(json.dumps(res, ensure_ascii=False) + "\n")
            out.flush()
            print(f"{k} {res.get('status')} {res.get('method')} {res.get('doi', '')}", file=log, flush=True)

    # Enrichment: OpenAlex records for resolved DOIs not in the pool.
    if a.no_network:
        return
    resolved = load_jsonl(RESOLVE_CACHE)
    have = {r["doi"] for r in load_jsonl(OA_CACHE)}
    need = sorted({r["doi"] for r in resolved if r.get("doi")} - set(by_doi) - have)
    print(f"openalex enrich: {len(need)} DOIs", file=log, flush=True)
    with OA_CACHE.open("a") as out:
        for i in range(0, len(need), 50):
            chunk = need[i : i + 50]
            try:
                data = litfetch.get_json(OPENALEX, {"filter": "doi:" + "|".join(chunk), "per-page": 50})
            except litfetch.BlockedError as e:
                print(f"blocked: {e}", file=log, flush=True)
                break
            got = set()
            for w in data.get("results") or []:
                rec = from_openalex(w, "bench", "bench_resolve")
                rec["doi"] = rec["doi"] or norm_doi(w.get("doi"))
                got.add(rec["doi"])
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            for d in set(chunk) - got:
                out.write(json.dumps({"doi": d, "missing": True}) + "\n")
            out.flush()
    print(f"cost today {litfetch.openalex_cost_today():.4f} USD", file=log)
    log.close()


if __name__ == "__main__":
    main()
