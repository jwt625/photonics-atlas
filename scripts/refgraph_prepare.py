"""Stage 2 of DevLog-020: metadata for the missing works cited by >= N corpus papers (reference graph).

Input: cache/literature/refgraph/<run>/missing.csv + refs.jsonl (scripts/lit_refgraph.py).
  - pool-resolved rows: metadata from the OpenAlex pool record (cache/literature/merged.jsonl);
  - unresolved rows: member entries of the cluster (union-find rebuilt from refs.jsonl in file order, as in the run);
    a printed / built DOI first, else Crossref query.bibliographic on the best two entries (quoted title, longest),
    accepted only through bench_resolve.verify (first-author surname, year within 1, title or page);
  - resolved DOIs outside the pool: OpenAlex filter=doi batches of 50 (OA status, venue, type, authors).
All network traffic goes through photonics_atlas.litfetch (generic User-Agent, per-host spacing, breakers); results
are cached and resumable: cache/literature/refgraph/resolve_cache.jsonl (by cluster root), openalex_cache.jsonl.
Then: dedup by DOI / arXiv id against sources.csv, cache_list.csv, the retrieval queue and the EO atlas
(../eo-modulator-atlas/data/papers.csv); books / chapters / theses flagged; class hint = most frequent primary class
of the citing papers; access tier (bench_curate.tier_of) and route (bench_prepare.route_of).
Output: data/_staging/literature/refgraph_cache_list.csv (not queued), log logs/refgraph_prepare_<ts>.log.

Usage (repo root): uv run python scripts/refgraph_prepare.py --run run_20261124T235543 [--min-citing 3]
                   [--limit N (new Crossref queries)] [--no-network]
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from bench_curate import tier_of  # noqa: E402
from bench_prepare import route_of  # noqa: E402
from bench_resolve import OPENALEX, crossref_lookup, load_jsonl, parse_ref  # noqa: E402
from lit_refgraph import QUOTED_RE, UnionFind  # noqa: E402

from photonics_atlas import litfetch  # noqa: E402
from photonics_atlas.litpool import from_openalex, norm_doi  # noqa: E402

RG = ROOT / "cache" / "literature" / "refgraph"
RESOLVE_CACHE = RG / "resolve_cache.jsonl"
OA_CACHE = RG / "openalex_cache.jsonl"
LITS = ROOT / "data" / "_staging" / "literature"
OUT = LITS / "refgraph_cache_list.csv"
EO_PAPERS = ROOT.parent / "eo-modulator-atlas" / "data" / "papers.csv"
NOT_PAPER = {"book", "book-chapter", "monograph", "dissertation", "edited-book", "reference-book", "book-review"}
POOL_KEYS = (
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
    "preprint_oa_url",
    "authors",
    "last_author",
    "cited_by_count",
)


def members_by_root(refs_path: Path) -> dict[str, list[str]]:
    rows = [json.loads(x) for x in refs_path.read_text(encoding="utf-8").splitlines()]
    un = [r for r in rows if r.get("cluster_keys")]
    uf = UnionFind()
    for r in un:
        for k in r["cluster_keys"][1:]:
            uf.union(r["cluster_keys"][0], k)
    out: dict[str, list[str]] = collections.defaultdict(list)
    for r in un:
        out[uf.find(r["cluster_keys"][0])].append(r["entry"])
    return out


def best_entries(entries: list[str], k: int = 2) -> list[str]:
    uniq = list(dict.fromkeys(entries))
    return sorted(uniq, key=lambda e: (QUOTED_RE.search(e) is None, -len(e)))[:k]


def load_pool(dois: set[str], uids: set[str]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    with (ROOT / "cache" / "literature" / "merged.jsonl").open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            d = norm_doi(r.get("doi"))
            if d in dois or r.get("uid") in uids:
                rec = {k: r.get(k) for k in POOL_KEYS}
                for key in (d, r.get("uid")):
                    if key:
                        out[key] = rec
    return out


def resolve_unresolved(
    rows: list[dict[str, str]], members: dict[str, list[str]], a: argparse.Namespace, log: Any
) -> None:
    done = {r["root"]: r for r in load_jsonl(RESOLVE_CACHE)}
    n_cr = 0
    with RESOLVE_CACHE.open("a", encoding="utf-8") as out:
        for x in rows:
            root = x["key"]
            if root in done and done[root].get("status") != "error":
                continue
            ents = best_entries(members.get(root, [x["example"]]))
            res: dict[str, Any] = {"root": root, "entries": ents}
            if x["doi"]:
                res.update(status="resolved", method="printed_or_built_doi", doi=norm_doi(x["doi"]))
            else:
                parsed0 = parse_ref(ents[0]) if ents else {}
                if parsed0.get("arxiv_id"):
                    res.update(status="resolved", method="printed_arxiv", arxiv_id=parsed0["arxiv_id"])
                elif a.no_network or (a.limit and n_cr >= a.limit):
                    continue
                else:
                    res.update(status="unresolved", method="crossref")
                    for e in ents:
                        n_cr += 1
                        try:
                            got = crossref_lookup(e, parse_ref(e))
                        except litfetch.BlockedError as exc:
                            print(f"blocked: {exc}", file=log, flush=True)
                            return
                        except Exception as exc:  # network / parse error: recorded, retried next run
                            res.update(status="error", error=str(exc)[:200])
                            break
                        if got.get("status") == "resolved":
                            res.update(got)
                            break
                        res.setdefault("reject", []).extend(got.get("reject", []))
            out.write(json.dumps(res, ensure_ascii=False) + "\n")
            out.flush()
            print(f"{root[:60]} {res.get('status')} {res.get('method')} {res.get('doi', '')}", file=log, flush=True)


def enrich(dois: list[str], log: Any) -> None:
    have = {r["doi"] for r in load_jsonl(OA_CACHE)}
    need = sorted(set(dois) - have)
    print(f"openalex enrich: {len(need)} DOIs", file=log, flush=True)
    with OA_CACHE.open("a", encoding="utf-8") as out:
        for i in range(0, len(need), 50):
            chunk = need[i : i + 50]
            try:
                data = litfetch.get_json(OPENALEX, {"filter": "doi:" + "|".join(chunk), "per-page": 50})
            except litfetch.BlockedError as exc:
                print(f"blocked: {exc}", file=log, flush=True)
                return
            got = set()
            for w in data.get("results") or []:
                rec = from_openalex(w, "refgraph", "refgraph_prepare")
                rec["doi"] = rec["doi"] or norm_doi(w.get("doi"))
                got.add(rec["doi"])
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            for d in set(chunk) - got:
                out.write(json.dumps({"doi": d, "missing": True}) + "\n")
            out.flush()


def known_ids() -> dict[str, str]:
    """DOI / arXiv id -> status for works already in the library, the cache list / queue or the EO atlas."""
    out: dict[str, str] = {}
    for r in csv.DictReader((ROOT / "data" / "registry" / "sources.csv").open(encoding="utf-8")):
        for v in (norm_doi(r["doi"]), r["arxiv_id"].strip()):
            if v:
                out.setdefault(v, f"in_library ({r['source_id']})")
    for name in ("cache_list.csv", "retrieval_queue.csv"):
        for r in csv.DictReader((LITS / name).open(encoding="utf-8")):
            for v in (norm_doi(r.get("doi")), (r.get("arxiv_id") or "").strip(), norm_doi(r.get("uid"))):
                if v:
                    out.setdefault(v, f"queued (lit:{r['paper_id']})")
    if EO_PAPERS.exists():
        for r in csv.DictReader(EO_PAPERS.open(encoding="utf-8")):
            for v in (norm_doi(r.get("doi")), (r.get("arxiv_id") or "").strip()):
                if v:
                    out.setdefault(v, f"eo_atlas (eo:{r['paper_id']})")
    return out


def merge_same_work(rows: list[dict[str, Any]], pclass: dict[str, str]) -> list[dict[str, Any]]:
    """Rows resolving to one DOI / arXiv id (a pool row and a title-less cluster of the same paper) become one row:
    the row with the most citing papers is kept, citing papers are unioned and the counts recomputed."""
    groups: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for x in rows:
        groups[x["doi"] or x["arxiv_id"] or f"key:{x['cluster_key']}"].append(x)
    out = []
    for g in groups.values():
        g.sort(key=lambda x: -int(x["n_citing"]))
        keep = dict(g[0])
        if len(g) > 1:
            citing = list(dict.fromkeys(c for x in g for c in str(x["citing"]).split(";") if c))
            cc = collections.Counter(pclass.get(c, "") for c in citing if pclass.get(c))
            keep.update(
                n_citing=len(citing),
                citing=";".join(citing),
                citing_classes=";".join(f"{k}:{v}" for k, v in cc.most_common()),
                class_hint=cc.most_common(1)[0][0] if cc else keep["class_hint"],
                cluster_key=" | ".join(str(x["cluster_key"]) for x in g),
            )
        out.append(keep)
    return sorted(out, key=lambda x: (-int(x["n_citing"]), str(x["doi"])))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0] if __doc__ else None)
    ap.add_argument("--run", required=True)
    ap.add_argument("--min-citing", type=int, default=3)
    ap.add_argument("--limit", type=int, default=0, help="max new Crossref queries this run (pilot)")
    ap.add_argument("--no-network", action="store_true")
    a = ap.parse_args()
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    log = (ROOT / "logs" / f"refgraph_prepare_{ts}.log").open("w", encoding="utf-8")
    rdir = RG / a.run
    rows = [
        r for r in csv.DictReader((rdir / "missing.csv").open(encoding="utf-8")) if int(r["n_citing"]) >= a.min_citing
    ]
    unres = [r for r in rows if r["resolved"] == "unresolved"]
    print(f"{len(rows)} works cited by >= {a.min_citing}; unresolved {len(unres)}", file=log, flush=True)
    resolve_unresolved(unres, members_by_root(rdir / "refs.jsonl"), a, log)
    res = {r["root"]: r for r in load_jsonl(RESOLVE_CACHE)}
    want_doi = {norm_doi(r["doi"]) for r in rows if r["doi"]} | {
        norm_doi(res[r["key"]].get("doi")) for r in unres if res.get(r["key"], {}).get("doi")
    }
    pool = load_pool(want_doi, {r["key"] for r in rows if r["resolved"] == "pool"})
    if not a.no_network:
        enrich(sorted(d for d in want_doi if d and d not in pool), log)
    oa = {r["doi"]: r for r in load_jsonl(OA_CACHE) if not r.get("missing")}
    if not a.no_network:  # printed / built DOIs nobody knows: Crossref on the cluster's entries instead
        unver = [
            {**r, "key": r["key"] + "|cr", "doi": ""}
            for r in unres
            if r["doi"] and norm_doi(r["doi"]) not in pool and norm_doi(r["doi"]) not in oa
        ]
        members = members_by_root(rdir / "refs.jsonl")
        for x in unver:
            members[x["key"]] = members.get(x["key"][:-3], [x["example"]])
        resolve_unresolved(unver, members, a, log)
        res = {r["root"]: r for r in load_jsonl(RESOLVE_CACHE)}
        extra = [norm_doi(res[x["key"]]["doi"]) for x in unver if res.get(x["key"], {}).get("doi")]
        pool.update(load_pool(set(extra), set()))
        enrich(sorted(d for d in extra if d not in pool), log)
        oa = {r["doi"]: r for r in load_jsonl(OA_CACHE) if not r.get("missing")}
        for x in unver:
            if res.get(x["key"], {}).get("doi"):
                res[x["key"][:-3]] = {**res[x["key"]], "root": x["key"][:-3]}
    known = known_ids()
    pclass = {
        r["paper_id"]: r["primary_class"] for r in csv.DictReader((LITS / "cache_list.csv").open(encoding="utf-8"))
    }
    out_rows = []
    for r in rows:
        rr = res.get(r["key"], {}) if r["resolved"] == "unresolved" else {}
        doi = norm_doi(
            rr.get("doi") if str(rr.get("method", "")).startswith("crossref") else (r["doi"] or rr.get("doi"))
        )
        meta = pool.get(r["key"]) or pool.get(doi) or oa.get(doi) or {}
        authors = meta.get("authors") or []
        arxiv = (meta.get("arxiv_id") or rr.get("arxiv_id") or "").strip()
        w = {
            "doi": doi,
            "arxiv_id": arxiv,
            "oa_url": meta.get("oa_url") or meta.get("preprint_oa_url") or "",
            "is_oa": meta.get("is_oa"),
            "oa_status": meta.get("oa_status") or "",
        }
        tier, access = tier_of(w)
        route, route_url = route_of(
            {"doi": doi, "arxiv_id": arxiv, "oa_url": str(w["oa_url"] or ""), "tier": str(tier)}
        )
        typ = meta.get("type") or rr.get("cr_type") or r["type"] or ""
        status = next((known[v] for v in (doi, arxiv) if v and v in known), "")
        if not status:
            if typ in NOT_PAPER:
                status = "not_paper"
            elif doi and not meta and not arxiv:
                status = "doi_unverified"  # printed / built DOI that neither the pool nor OpenAlex knows
            else:
                status = "new" if (doi or arxiv) else "unresolved"
        cc = collections.Counter(pclass.get(c, "") for c in r["citing"].split(";") if pclass.get(c))
        out_rows.append(
            {
                "n_citing": r["n_citing"],
                "status": status,
                "resolved_via": r["resolved"] if r["resolved"] != "unresolved" else (rr.get("method") or "unresolved"),
                "doi": doi,
                "arxiv_id": arxiv,
                "title": meta.get("title") or rr.get("cr_title") or r["title"],
                "first_author": authors[0] if authors else "",
                "last_author": meta.get("last_author") or (authors[-1] if authors else ""),
                "year": meta.get("year") or rr.get("cr_year") or r["year"],
                "venue": meta.get("venue") or rr.get("cr_venue") or r["venue"],
                "type": typ,
                "class_hint": cc.most_common(1)[0][0] if cc else "",
                "citing_classes": r["citing_classes"],
                "tier": tier,
                "access": access,
                "route": route,
                "route_url": route_url,
                "oa_status": w["oa_status"],
                "cluster_key": r["key"],
                "citing": r["citing"],
                "example": r["example"],
            }
        )
    out_rows = merge_same_work(out_rows, pclass)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(out_rows[0]))
        wr.writeheader()
        wr.writerows(out_rows)
    st = collections.Counter(str(x["status"]).split(" ")[0] for x in out_rows)
    new = [x for x in out_rows if x["status"] == "new"]
    summary = {
        "works": len(out_rows),
        "status": dict(st),
        "new_by_route": dict(collections.Counter(x["route"] for x in new)),
        "new_by_tier": dict(collections.Counter(x["tier"] for x in new)),
        "resolved_via": dict(collections.Counter(x["resolved_via"] for x in out_rows)),
    }
    print(json.dumps(summary, indent=1), file=log, flush=True)
    print(json.dumps(summary, indent=1))
    print(f"-> {OUT.relative_to(ROOT)}; log {log.name}")
    log.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
