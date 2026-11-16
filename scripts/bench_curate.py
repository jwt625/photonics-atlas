"""B4 + B6 of DevLog-019: dedup the resolved benchmark citations and rank them into the next cache list.

Inputs: cache/literature/bench/extract/*.jsonl (items), resolve_cache.jsonl, openalex_cache.jsonl, the OpenAlex pool
(cache/literature/merged.jsonl), data/registry/sources.csv (library), data/_staging/literature/cache_list.csv
(already queued), EO atlas data/papers.csv + data/candidates.csv (read-only).

Work identity: DOI (non-arXiv) > arXiv id > normalized title; works sharing a normalized title (> 25 chars) merge,
which joins arXiv preprints to their journal versions. A work is `in_library` when its DOI / arXiv id / title is in
sources.csv, `queued` when it is in cache_list.csv, `eo_atlas` when it is in the EO atlas tables.

Access tier (owner answer 4): 1 = arXiv copy or OpenAlex OA copy (Optics Letters / Photonics Research publisher copies
excluded), 2 = IEEE (DOI prefix 10.1109) without an OA copy, 3 = other paywalled.
Rank (new, in-scope, non-modulator works): tiers 1-2 first, by distinct citing papers, then class need (fewer atlas
components in the class first), then year; per-subtype cap above the cut line; tier-3 works cited by >= TIER3_PROMOTE
papers join the ranked block. Cut line at --target.

Outputs: data/_staging/literature/bench_cache_list.csv (ranked, new works), bench_eo_candidates.csv (modulators),
cache/literature/bench/works.jsonl (every work incl. library / queued / out of scope), report printed and logged to
logs/bench_curate_<ts>.log.
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from bench_resolve import load_jsonl, ref_key  # noqa: E402

from photonics_atlas.litpool import norm_doi, norm_title  # noqa: E402

BENCH = ROOT / "cache" / "literature" / "bench"
STAGE = ROOT / "data" / "_staging" / "literature"
EO = ROOT.parent / "eo-modulator-atlas" / "data"
TIER3_PROMOTE = 3
SUBTYPE_CAP = 70
EXCLUDED_OA_PREFIX = ("10.1364/ol.", "10.1364/prj.")


def tier_of(w: dict[str, Any]) -> tuple[int, str]:
    doi = w.get("doi") or ""
    if w.get("arxiv_id") or "arxiv.org" in (w.get("oa_url") or ""):
        return 1, "arxiv"
    if w.get("is_oa") and w.get("oa_url") and not doi.startswith(EXCLUDED_OA_PREFIX):
        return 1, f"oa_{w.get('oa_status') or 'unknown'}"
    if doi.startswith("10.1109/"):
        return 2, "ieee"
    return 3, "paywalled"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--target", type=int, default=1200)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")

    items = [r for p in sorted((BENCH / "extract").glob("*.jsonl")) for r in load_jsonl(p) if r.get("type") == "item"]
    res = {r["key"]: r for r in load_jsonl(BENCH / "resolve_cache.jsonl")}
    oa = {r["doi"]: r for r in load_jsonl(BENCH / "openalex_cache.jsonl") if not r.get("missing")}

    pool_doi: dict[str, dict[str, Any]] = {}
    pool_arx: dict[str, dict[str, Any]] = {}
    with open(ROOT / "cache" / "literature" / "merged.jsonl") as f:
        for line in f:
            r = json.loads(line)
            if r.get("doi"):
                pool_doi.setdefault(norm_doi(r["doi"]), r)
            if r.get("arxiv_id"):
                pool_arx.setdefault(r["arxiv_id"], r)

    def idx(rows: list[dict[str, str]], key: str) -> dict[str, str]:
        out: dict[str, str] = {}
        for r in rows:
            for k in (norm_doi(r.get("doi")), (r.get("arxiv_id") or "").strip(), norm_title(r.get("title"))):
                if k and (len(k) > 25 or "/" in k or re.match(r"\d{4}\.\d{4,5}$", k)):
                    out.setdefault(k, r[key])
        return out

    with open(ROOT / "data" / "registry" / "sources.csv", newline="") as f:
        src_rows = list(csv.DictReader(f))
    lib = idx(src_rows, "source_id")
    # one citing paper may sit in two corpora (EO atlas copy of an OFC 2026 paper, same_as links): count it once
    canon: dict[str, str] = {}
    for r in src_rows:
        m = re.search(r"paper ([A-Za-z0-9]+\.[0-9]+)", r["venue"]) if r["corpus"] == "eo" else None
        if m and "(OFC) 2026" in r["venue"]:
            canon[r["source_id"]] = f"ofc2026:{m.group(1)}"
        elif r.get("same_as"):
            canon[r["source_id"]] = r["same_as"]
    for it in items:
        it["citing"] = canon.get(it["citing"], it["citing"])
    with open(STAGE / "cache_list.csv", newline="") as f:
        queued = idx(list(csv.DictReader(f)), "paper_id")
    eo_rows: list[dict[str, str]] = []
    for name in ("papers.csv", "candidates.csv"):
        if (EO / name).exists():
            with open(EO / name, newline="") as f:
                eo_rows += list(csv.DictReader(f))
    eo = idx(eo_rows, "paper_id")
    with open(ROOT / "data" / "components" / "components.csv", newline="") as f:
        class_n = collections.Counter(r["class"] for r in csv.DictReader(f))

    # group items into works
    works: dict[str, dict[str, Any]] = {}
    unresolved: dict[str, dict[str, Any]] = {}
    for it in items:
        r = res.get(ref_key(it.get("ref") or "")) if it.get("ref") else None
        doi = norm_doi((r or {}).get("doi"))
        arx = ((r or {}).get("arxiv_id") or "").strip()
        meta = oa.get(doi) or pool_doi.get(doi) or (pool_arx.get(arx) if arx else None) or {}
        if doi.startswith("10.48550/arxiv."):
            arx, doi = arx or doi.split("arxiv.")[-1], ""
        title = meta.get("title") or (r or {}).get("cr_title") or (r or {}).get("p_title") or ""
        wid = doi or (f"arxiv:{arx}" if arx else "")
        if not wid:
            k = ref_key(it.get("ref") or it.get("row_label") or "")
            u = unresolved.setdefault(
                k,
                {
                    "ref": it.get("ref", ""),
                    "label": it.get("row_label", ""),
                    "citing": set(),
                    "classes": collections.Counter(),
                },
            )
            u["citing"].add(it["citing"])
            u["classes"][it.get("class", "")] += 1
            continue
        w = works.setdefault(
            wid,
            {
                "work_id": wid,
                "doi": doi,
                "arxiv_id": arx or meta.get("arxiv_id") or "",
                "title": title,
                "year": meta.get("year") or (r or {}).get("cr_year") or (r or {}).get("p_year"),
                "venue": meta.get("venue") or (r or {}).get("cr_venue") or "",
                "venue_type": meta.get("venue_type", ""),
                "type": meta.get("type") or (r or {}).get("cr_type") or "",
                "is_oa": meta.get("is_oa", False),
                "oa_status": meta.get("oa_status", ""),
                "oa_url": meta.get("oa_url", "") or meta.get("preprint_oa_url", ""),
                "first_author": (meta.get("authors") or [""])[0],
                "last_author": meta.get("last_author", ""),
                "cited_by_count": meta.get("cited_by_count", 0),
                "citing": set(),
                "classes": collections.Counter(),
                "topics": collections.Counter(),
                "n_items": 0,
                "n_values": 0,
                "ref_example": it.get("ref", ""),
            },
        )
        w["citing"].add(it["citing"])
        w["classes"][it.get("class", "")] += 1
        w["topics"][it.get("topic", "")] += 1
        w["n_items"] += 1
        w["n_values"] += len(it.get("values") or [])

    # merge works sharing a normalized title (preprint + journal version)
    by_t: dict[str, str] = {}
    for wid in list(works):
        t = norm_title(works[wid]["title"])
        if len(t) <= 25:
            continue
        if t in by_t and by_t[t] in works:
            keep, drop = works[by_t[t]], works.pop(wid)
            if not keep["doi"] and drop["doi"]:
                keep, drop = drop, keep
                works[wid] = keep
                works.pop(by_t[t])
                by_t[t] = wid
            keep["arxiv_id"] = keep["arxiv_id"] or drop["arxiv_id"]
            keep["oa_url"] = keep["oa_url"] or drop["oa_url"]
            keep["is_oa"] = keep["is_oa"] or drop["is_oa"]
            keep["citing"] |= drop["citing"]
            keep["classes"] += drop["classes"]
            keep["topics"] += drop["topics"]
            keep["n_items"] += drop["n_items"]
            keep["n_values"] += drop["n_values"]
        else:
            by_t[t] = wid

    for w in works.values():
        keys = [w["doi"], w["arxiv_id"], norm_title(w["title"])]
        w["in_library"] = next((lib[k] for k in keys if k and k in lib), "")
        w["queued"] = next((queued[k] for k in keys if k and k in queued), "")
        w["eo_atlas"] = next((eo[k] for k in keys if k and k in eo), "")
        cls = w["classes"].most_common(1)[0][0] if w["classes"] else ""
        w["class"] = cls
        w["family"] = cls.split(".")[0]
        w["tier"], w["route"] = tier_of(w)
        w["n_citing"] = len(w["citing"])
        try:
            w["history_flag"] = int(w["year"] or 0) < 2000 and int(w["year"] or 0) > 0
        except (TypeError, ValueError):
            w["history_flag"] = False
        w["status"] = (
            "in_library"
            if w["in_library"]
            else "queued"
            if w["queued"]
            else "out_of_scope"
            if w["family"] == "out_of_scope"
            else "eo_atlas"
            if w["eo_atlas"]
            else "modulator"
            if w["family"] == "modulator"
            else "new"
        )

    new = [w for w in works.values() if w["status"] == "new"]

    def need(w: dict[str, Any]) -> int:
        return class_n.get(w["class"], 0)

    ranked_pool = [w for w in new if w["tier"] <= 2 or w["n_citing"] >= TIER3_PROMOTE]
    ranked_pool.sort(key=lambda w: (-w["n_citing"], need(w), -(int(w["year"] or 0))))
    above: list[dict[str, Any]] = []
    below: list[dict[str, Any]] = []
    per_sub: collections.Counter[str] = collections.Counter()
    for w in ranked_pool:
        if len(above) < a.target and per_sub[w["class"]] < SUBTYPE_CAP:
            above.append(w)
            per_sub[w["class"]] += 1
        else:
            below.append(w)
    rest = sorted(
        (w for w in new if w not in ranked_pool), key=lambda w: (-w["n_citing"], need(w), -(int(w["year"] or 0)))
    )
    final = [(w, True) for w in above] + [(w, False) for w in below + rest]

    lines = []
    st = collections.Counter(w["status"] for w in works.values())
    lines.append(f"items {len(items)}; works {len(works)}; unresolved refs {len(unresolved)}; status {dict(st)}")
    lines.append(f"new {len(new)}: tiers {dict(collections.Counter(w['tier'] for w in new))}; above cut {len(above)}")
    lines.append(
        f"above-cut tiers {dict(collections.Counter(w['tier'] for w in above))}; "
        f"families {collections.Counter(w['family'] for w in above).most_common()}"
    )
    report = "\n".join(lines)
    print(report)
    with open(ROOT / "logs" / f"bench_curate_{ts}.log", "w") as f:
        f.write(report + "\n")
    if a.dry_run:
        return

    cols = [
        "rank",
        "above_cut",
        "work_id",
        "doi",
        "arxiv_id",
        "title",
        "first_author",
        "last_author",
        "year",
        "venue",
        "type",
        "class",
        "classes",
        "n_citing",
        "n_items",
        "n_values",
        "tier",
        "route",
        "oa_url",
        "history_flag",
        "citing",
        "topics",
    ]

    def row(i: int, w: dict[str, Any], cut: bool) -> dict[str, Any]:
        return {
            "rank": i,
            "above_cut": cut,
            **{k: w.get(k, "") for k in cols[2:19]},
            "classes": "|".join(c for c, _ in w["classes"].most_common()),
            "history_flag": w["history_flag"],
            "citing": "|".join(sorted(w["citing"])[:12]),
            "topics": "|".join(t for t, _ in w["topics"].most_common(3)),
        }

    with open(STAGE / "bench_cache_list.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=cols)
        wr.writeheader()
        for i, (w, cut) in enumerate(final, 1):
            wr.writerow(row(i, w, cut))
    eo_new = sorted((w for w in works.values() if w["status"] == "modulator"), key=lambda w: -w["n_citing"])
    with open(STAGE / "bench_eo_candidates.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=cols)
        wr.writeheader()
        for i, w in enumerate(eo_new, 1):
            wr.writerow(row(i, w, False))
    with open(BENCH / "works.jsonl", "w") as f:
        for w in works.values():
            f.write(
                json.dumps(
                    {
                        k: (sorted(v) if isinstance(v, set) else dict(v) if isinstance(v, collections.Counter) else v)
                        for k, v in w.items()
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
        for k, u in unresolved.items():
            f.write(
                json.dumps(
                    {
                        "work_id": f"unresolved:{k}",
                        "status": "unresolved",
                        "ref": u["ref"],
                        "label": u["label"],
                        "citing": sorted(u["citing"]),
                        "classes": dict(u["classes"]),
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )


if __name__ == "__main__":
    main()
