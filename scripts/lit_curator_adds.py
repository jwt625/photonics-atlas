"""Resolve curator `adds` (DevLog-006 S4) into pool records for the selection step.

Input:  config/literature/curation/*.yaml `adds: [{doi | arxiv_id, title, year, class, subtype, reason}]`.
Lookup: the merged pool (cache/literature/merged.jsonl) by DOI / arXiv id first; otherwise one free OpenAlex singleton
        get (`/works/doi:<doi>` or the arXiv DOI 10.48550/arXiv.<id>) through photonics_atlas.litfetch.
Check:  the API title must match the curator's title (difflib >= 0.9) or the add is rejected (logged), so an add can
        never point at a different paper.
Output: cache/literature/curator_adds.jsonl: one litpool record per accepted add plus `curator_add` {group, class,
        subtype, reason}; rejected / unresolved adds are listed in the log. Re-runnable (resolved uids are reused).

Usage: uv run python scripts/lit_curator_adds.py [--dry-run] [--offline]
"""

from __future__ import annotations

import argparse
import difflib
import json
from pathlib import Path
from typing import Any

import yaml

from photonics_atlas import litfetch, litpool
from photonics_atlas.paths import CACHE, ROOT
from photonics_atlas.runlog import RunLog

LIT = CACHE / "literature"
OUT = LIT / "curator_adds.jsonl"


def load_adds() -> list[dict[str, Any]]:
    adds = []
    for p in sorted((ROOT / "config" / "literature" / "curation").glob("*.yaml")):
        y = yaml.safe_load(p.read_text()) or {}
        for a in y.get("adds") or []:
            adds.append({**a, "group": y.get("group") or p.stem})
    return adds


def index_merged(path: Path, dois: set[str], arxivs: set[str]) -> dict[str, dict[str, Any]]:
    hit: dict[str, dict[str, Any]] = {}
    if not path.exists():
        return hit
    with path.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            keys = {litpool.norm_doi(r.get("doi"))} | {litpool.norm_doi(d) for d in r.get("alt_dois") or []}
            for k in keys & dois:
                hit[k] = r
            a = (r.get("arxiv_id") or "").lower()
            if a and a in arxivs:
                hit["arxiv:" + a] = r
    return hit


def title_ok(a: str, b: str) -> bool:
    return difflib.SequenceMatcher(None, litpool.norm_title(a), litpool.norm_title(b)).ratio() >= 0.9


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--offline", action="store_true", help="no API gets; only adds found in the merged pool")
    args = ap.parse_args()
    adds = load_adds()
    with RunLog("lit_curator_adds", dry_run=args.dry_run) as log:
        dois = {litpool.norm_doi(a.get("doi")) for a in adds if a.get("doi")}
        arxivs = {str(a.get("arxiv_id")).lower() for a in adds if a.get("arxiv_id")}
        merged = index_merged(LIT / "merged.jsonl", dois, arxivs)
        prev = {r["curator_add"]["key"]: r for r in litpool.read(OUT)} if OUT.exists() else {}
        out, rejected = [], 0
        for a in adds:
            doi = litpool.norm_doi(a.get("doi"))
            arx = str(a.get("arxiv_id") or "").lower()
            key = doi or f"arxiv:{arx}"
            rec = prev.get(key) or merged.get(doi) or merged.get(f"arxiv:{arx}")
            source = "cache" if key in prev else "merged" if rec else ""
            if rec is None and not args.offline:
                url = f"https://api.openalex.org/works/doi:{doi or '10.48550/arxiv.' + arx}"
                try:
                    rec = litpool.from_openalex(litfetch.get_json(url), "curator", f"curator_add:{a['group']}")
                    source = "openalex"
                except Exception as e:  # noqa: BLE001 - log and continue with the other adds
                    log.event("add", "unresolved", key=key, error=str(e)[:200])
            if rec is None:
                rejected += 1
                log.info(f"unresolved {key} ({a['group']})")
                continue
            if a.get("title") and not title_ok(a["title"], rec.get("title", "")):
                rejected += 1
                log.info(f"title mismatch {key}: curator {a['title']!r} vs api {rec.get('title')!r}")
                log.event("add", "title_mismatch", key=key)
                continue
            rec = {k: v for k, v in rec.items() if k != "curator_add"}
            rec["curator_add"] = {
                "key": key, "group": a["group"], "class": a["class"], "subtype": a.get("subtype") or "",
                "reason": a.get("reason") or "",
            }  # fmt: skip
            out.append(rec)
            log.event("add", "ok", key=key, uid=rec["uid"], source=source)
        log.info(f"adds {len(adds)}, accepted {len(out)}, rejected / unresolved {rejected}")
        if not args.dry_run:
            tmp = OUT.with_suffix(".jsonl.part")
            tmp.unlink(missing_ok=True)
            litpool.append(tmp, out)
            tmp.replace(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
