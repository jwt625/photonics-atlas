"""Write LLM-scoring batches from the prefiltered pool (DevLog-006 S2 -> S3). Does not score.

Input:  cache/literature/prefiltered.jsonl (records with score_keep = true; scripts/lit_prefilter.py)
Output: cache/literature/scoring/<group>_bNNN.jsonl (group G1-G7 of the record's best class, config/literature/
        buckets.yaml), and cache/literature/scoring/manifest.json (batch -> uids, aliases).
Fields per record: uid, title, authors (first 3 + last), institutions, venue, year, type, abstract (<= 2500 chars),
        class_hits, platform_hits.
Re-runnable: works already in a batch (uid or any alias uid in the manifest or in an existing batch file) are
skipped; numbering continues per group. By default only full batches are written and each group's remainder waits
for the next run; --flush also writes the remainders (use once the lanes are complete).

Usage: uv run python scripts/lit_make_score_batches.py [--size 150] [--flush] [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

from photonics_atlas.paths import CACHE, ROOT
from photonics_atlas.runlog import RunLog

LIT = CACHE / "literature"
PREFILTERED = LIT / "prefiltered.jsonl"
SCORING = LIT / "scoring"
ABSTRACT_MAX = 2500
BATCH_RE = re.compile(r"^(G\d+)_b(\d{3})\.jsonl$")
FIELDS = ["uid", "title", "authors", "institutions", "venue", "year", "type", "abstract", "class_hits", "platform_hits"]


def short_authors(authors: list[str], last: str = "") -> list[str]:
    """First 3 + last author (the last from `last_author` when the stored list is truncated)."""
    a = [x for x in authors if x]
    last = last or (a[-1] if a else "")
    if len(a) <= 4 and (not last or last == a[-1]):
        return a
    head = a[:3]
    return head + [last] if last and last not in head else head


def truncate(text: str, n: int = ABSTRACT_MAX) -> str:
    if len(text) <= n:
        return text
    cut = text[:n]
    sp = cut.rfind(" ")
    return (cut[:sp] if sp > n * 0.8 else cut).rstrip() + " ..."


def batch_record(r: dict[str, Any]) -> dict[str, Any]:
    out = {
        "uid": r["uid"],
        "title": r.get("title") or "",
        "authors": short_authors(list(r.get("authors") or []), r.get("last_author") or ""),
        "institutions": list(r.get("institutions") or []),
        "venue": r.get("venue") or "",
        "year": r.get("year"),
        "type": r.get("type") or "",
        "abstract": truncate(r.get("abstract") or ""),
        "class_hits": list(r.get("class_hits") or []),
        "platform_hits": list(r.get("platform_hits") or []),
    }
    return {k: out[k] for k in FIELDS}


def load_manifest(scoring: Path) -> dict[str, Any]:
    mpath = scoring / "manifest.json"
    man: dict[str, Any] = json.loads(mpath.read_text(encoding="utf-8")) if mpath.exists() else {"batches": []}
    listed = {b["file"] for b in man["batches"]}
    for p in sorted(scoring.glob("G*_b*.jsonl")):  # batch files without a manifest entry (manifest lost)
        m = BATCH_RE.match(p.name)
        if m and p.name not in listed:
            uids = [json.loads(x)["uid"] for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
            man["batches"].append({"file": p.name, "group": m.group(1), "n": len(uids), "uids": uids, "aliases": []})
    return man


def plan_batches(
    keep: list[dict[str, Any]], man: dict[str, Any], size: int, flush: bool
) -> tuple[list[tuple[str, list[dict[str, Any]]]], dict[str, int], int]:
    """-> ([(file name, records)], held-back count per group, already-batched count)."""
    assigned: set[str] = set()
    next_no: dict[str, int] = {}
    for b in man["batches"]:
        assigned |= set(b.get("uids") or []) | set(b.get("aliases") or [])
        m = BATCH_RE.match(b["file"])
        if m:
            next_no[m.group(1)] = max(next_no.get(m.group(1), 0), int(m.group(2)))
    todo: dict[str, list[dict[str, Any]]] = {}
    done = 0
    for r in keep:
        ids = {r["uid"], *(r.get("alt_uids") or [])}
        if ids & assigned:
            done += 1
            continue
        todo.setdefault(r["group"], []).append(r)
    plans: list[tuple[str, list[dict[str, Any]]]] = []
    held: dict[str, int] = {}
    for g in sorted(todo):
        rows = sorted(todo[g], key=lambda r: (r["best_class"], r.get("cap_rank", 0), r["uid"]))
        n_full = len(rows) // size
        chunks = [rows[i * size : (i + 1) * size] for i in range(n_full)]
        rest = rows[n_full * size :]
        if rest and flush:
            chunks.append(rest)
        elif rest:
            held[g] = len(rest)
        for ch in chunks:
            next_no[g] = next_no.get(g, 0) + 1
            plans.append((f"{g}_b{next_no[g]:03d}.jsonl", ch))
    return plans, held, done


def write_batch(scoring: Path, name: str, rows: list[dict[str, Any]]) -> None:
    tmp = scoring / (name + ".part")
    with tmp.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(batch_record(r), ensure_ascii=False) + "\n")
    tmp.replace(scoring / name)


def save_manifest(scoring: Path, man: dict[str, Any]) -> None:
    tmp = scoring / "manifest.json.part"
    tmp.write_text(json.dumps(man, indent=1, ensure_ascii=False), encoding="utf-8")
    tmp.replace(scoring / "manifest.json")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--size", type=int, default=150)
    ap.add_argument("--flush", action="store_true", help="also write each group's partial last batch")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out-dir", type=Path, default=SCORING, help="batch directory (default cache/literature/scoring)")
    args = ap.parse_args()
    scoring: Path = args.out_dir
    if not PREFILTERED.exists():
        print(f"missing {PREFILTERED.relative_to(ROOT)}; run scripts/lit_prefilter.py first", file=sys.stderr)
        return 1
    with RunLog("lit_make_score_batches", dry_run=args.dry_run) as log:
        rows = [json.loads(x) for x in PREFILTERED.read_text(encoding="utf-8").splitlines() if x.strip()]
        keep = [r for r in rows if r.get("score_keep")]
        scoring.mkdir(parents=True, exist_ok=True)
        man = load_manifest(scoring)
        keep_ids = {i for r in keep for i in [r["uid"], *(r.get("alt_uids") or [])]}
        stale = sum(1 for b in man["batches"] for u in b.get("uids") or [] if u not in keep_ids)
        plans, held, done = plan_batches(keep, man, args.size, args.flush)
        log.info(
            f"kept {len(keep)}, already batched {done}, new batches {len(plans)} "
            f"({sum(len(c) for _, c in plans)} records), held back {held or 'none'}, "
            f"batched earlier but no longer kept {stale}"
        )
        for name, ch in plans:
            log.info(f"  {name}: {len(ch)}")
        if args.dry_run:
            return 0
        today = dt.date.today().isoformat()
        for name, ch in plans:
            write_batch(scoring, name, ch)
            man["batches"].append(
                {
                    "file": name,
                    "group": name.split("_", 1)[0],
                    "n": len(ch),
                    "created": today,
                    "uids": [r["uid"] for r in ch],
                    "aliases": sorted({a for r in ch for a in r.get("alt_uids") or []}),
                }
            )
            save_manifest(scoring, man)
            log.event("batch", file=name, n=len(ch))
        if not plans:
            save_manifest(scoring, man)
        log.info(f"manifest {scoring / 'manifest.json'}: {len(man['batches'])} batches")
    return 0


if __name__ == "__main__":
    sys.exit(main())
