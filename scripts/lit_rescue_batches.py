"""Rescue batches for highly cited papers cut by the prefilter caps (DevLog-006 D135). No network.

The S2 per-class caps rank by rule score, which cut landmark papers (curators G1 / G2 / G5 found several). This adds,
per class, the most-cited prefilter candidates that were not kept for scoring, have a TITLE class hit and are not
known: top ceil(fraction x class budget) by cited_by_count (records without a count are skipped). Written as scoring
batches of group G9 (`cache/literature/scoring/G9_bNNN.jsonl`, same fields as lit_make_score_batches.py), scored with
the same rubric, then selected like any other record.

Usage: uv run python scripts/lit_rescue_batches.py [--fraction 0.6] [--size 150] [--dry-run]
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import math
from pathlib import Path
from typing import Any

import yaml

from photonics_atlas.paths import CACHE, ROOT
from photonics_atlas.runlog import RunLog

LIT = CACHE / "literature"
SCORING = LIT / "scoring"


def _batch_record_fn() -> Any:
    spec = importlib.util.spec_from_file_location("lmsb", Path(__file__).with_name("lit_make_score_batches.py"))
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.batch_record


def as_obj(v: Any) -> Any:
    if isinstance(v, str) and v[:1] in "[{":
        try:
            return ast.literal_eval(v)
        except (ValueError, SyntaxError):
            return v
    return v


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fraction", type=float, default=0.6)
    ap.add_argument("--size", type=int, default=150)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    budget: dict[str, int] = yaml.safe_load((ROOT / "config" / "literature" / "selection.yaml").read_text())["budget"]
    batched: set[str] = set()
    for p in SCORING.glob("G*_b*.jsonl"):
        batched |= {json.loads(x)["uid"] for x in p.read_text(encoding="utf-8").splitlines() if x.strip()}
    with RunLog("lit_rescue_batches", dry_run=args.dry_run) as log:
        pool: dict[str, list[tuple[int, dict[str, Any]]]] = {c: [] for c in budget}
        with (LIT / "prefiltered.jsonl").open(encoding="utf-8") as f:
            for line in f:
                r = json.loads(line)
                if str(r.get("score_keep")) == "True" or r["uid"] in batched or as_obj(r.get("known_in")):
                    continue
                cites = r.get("cited_by_count")
                if cites in (None, "", "None"):
                    continue
                where = as_obj(r.get("class_hit_where")) or {}
                for cls, w in where.items():
                    if w == "title" and cls in pool:
                        pool[cls].append((int(cites), r))
        chosen: dict[str, dict[str, Any]] = {}
        for cls in sorted(budget):
            n = math.ceil(args.fraction * budget[cls])
            got = 0
            for _c, r in sorted(pool[cls], key=lambda x: -x[0]):
                if got >= n:
                    break
                if r["uid"] not in chosen:
                    chosen[r["uid"]] = r
                    got += 1
            log.info(f"  {cls:22s} title-hit unscored {len(pool[cls]):6d}, rescued {got}")
        rows = list(chosen.values())
        log.info(f"rescued {len(rows)} records -> {math.ceil(len(rows) / args.size)} G9 batches")
        if args.dry_run:
            return 0
        batch_record = _batch_record_fn()
        start = 1 + max((int(p.stem.split("_b")[1]) for p in SCORING.glob("G9_b*.jsonl")), default=0)
        for i in range(0, len(rows), args.size):
            name = f"G9_b{start + i // args.size:03d}.jsonl"
            with (SCORING / name).open("w", encoding="utf-8") as f:
                for r in rows[i : i + args.size]:
                    f.write(json.dumps(batch_record(r), ensure_ascii=False) + "\n")
            log.event("batch", name=name, n=len(rows[i : i + args.size]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
