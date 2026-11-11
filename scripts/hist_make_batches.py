"""Cut the next historical batches hist_NN (DevLog-016 D969) from papers that are ready.

Ready = a history_candidates.csv row of --tier, registered as lit:<paper_id> in data/registry/sources.csv, with
references/<paper_id>/text.md, and not a scan still waiting for OCR (source.json low_text / garbled_text_layer without
ocr_on). Papers already in any data/_staging/history/hist_*/papers.csv are skipped. mode = milestone_only for papers that
were cached before this DevLog (already_in_repo lit: / eo:, their component rows exist), else full. Batches are filled in
year order, separately per mode, up to --size papers each.

Usage: uv run python scripts/hist_make_batches.py [--tier core] [--size 8] [--max-batches N] [--dry-run]
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from photonics_atlas.paths import ROOT, STAGING
from photonics_atlas.runlog import RunLog

HIST = STAGING / "history"
COLS = [
    "paper_id", "source_id", "mode", "year", "era", "thread", "title", "venue", "doi", "dri", "dri_basis",
    "dri_source", "significance", "component_class", "has_device_metrics",
]  # fmt: skip


def read(p: Path) -> list[dict[str, str]]:
    with p.open(newline="", encoding="utf-8") as f:
        return [dict(r) for r in csv.DictReader(f)]


def ready(pid: str, sources: set[str]) -> bool:
    d = ROOT / "references" / pid
    if f"lit:{pid}" not in sources or not (d / "text.md").exists() or not (d / "source.json").exists():
        return False
    m = json.loads((d / "source.json").read_text())
    return not ((m.get("low_text") or m.get("garbled_text_layer")) and not m.get("ocr_on"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tier", default="core")
    ap.add_argument("--size", type=int, default=8)
    ap.add_argument("--max-batches", type=int, default=99)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    sources = {r["source_id"] for r in read(ROOT / "data" / "registry" / "sources.csv")}
    done: set[str] = set()
    nums = [0]
    for p in HIST.glob("hist_*/papers.csv"):
        done |= {r["paper_id"] for r in read(p)}
        nums.append(int(re.sub(r"\D", "", p.parent.name) or 0))
    cand = [r for r in read(STAGING / "literature" / "history_candidates.csv") if r["tier"] == a.tier]
    todo = [r for r in cand if r["paper_id"] not in done and ready(r["paper_id"], sources)]
    waiting = [r["paper_id"] for r in cand if r["paper_id"] not in done and r not in todo]
    n = max(nums)
    made = 0
    with RunLog("hist_make_batches", a.dry_run) as log:
        log.info(f"{len(todo)} ready, {len(waiting)} not ready, {len(done)} already batched")
        for mode in ("full", "milestone_only"):
            rows = [
                r
                for r in todo
                if ("milestone_only" if r["already_in_repo"].startswith(("lit:", "eo:")) else "full") == mode
            ]
            rows.sort(key=lambda r: (int(r["year"]), r["paper_id"]))
            for i in range(0, len(rows), a.size):
                if made >= a.max_batches:
                    break
                n += 1
                made += 1
                name = f"hist_{n:02d}"
                chunk = rows[i : i + a.size]
                log.info(f"{name} ({mode}): {', '.join(r['paper_id'] for r in chunk)}")
                if a.dry_run:
                    continue
                (HIST / name).mkdir(parents=True, exist_ok=True)
                with (HIST / name / "papers.csv").open("w", newline="", encoding="utf-8") as f:
                    w = csv.DictWriter(f, fieldnames=COLS)
                    w.writeheader()
                    for r in chunk:
                        w.writerow(
                            {c: r.get(c, "") for c in COLS} | {"source_id": f"lit:{r['paper_id']}", "mode": mode}
                        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
