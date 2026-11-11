"""Apply a history batch audit patch (DevLog-016 D969): data/_staging/history/<batch>/audit_patch.csv with columns
file,row_key,column,old,new,reason, where file is milestones (data/_staging/history/<batch>/milestones.csv, key
paper_id), components (data/_staging/components/<batch>/components.csv, key component_id) or component_metrics
(.../component_metrics.csv, key metric_id). column DELETE drops the row (and, for a component, its metrics).
Each change is applied only when the current value equals `old` (or the column is new / empty and old is empty);
otherwise it is reported and nothing is written. A zip backup of the batch files is written before the first change.
Idempotent: a second run reports 0 changes.

Usage: uv run python scripts/hist_apply_patch.py <batch> [--dry-run]
"""

from __future__ import annotations

import argparse
import csv
import sys
import zipfile
from pathlib import Path

from photonics_atlas.paths import CACHE, STAGING
from photonics_atlas.runlog import RunLog

KEYS = {"milestones": "paper_id", "components": "component_id", "component_metrics": "metric_id"}


def path_of(batch: str, file: str) -> Path:
    if file == "milestones":
        return STAGING / "history" / batch / "milestones.csv"
    return STAGING / "components" / batch / f"{file}.csv"


def read(p: Path) -> tuple[list[str], list[dict[str, str]]]:
    with p.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return list(r.fieldnames or []), [dict(x) for x in r]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("batch")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    patch = read(STAGING / "history" / a.batch / "audit_patch.csv")[1]
    tables = {f: read(path_of(a.batch, f)) for f in KEYS if path_of(a.batch, f).exists()}
    changes, conflicts = 0, []
    with RunLog("hist_apply_patch", a.dry_run) as log:
        for i, p in enumerate(patch, 2):
            f, key, col = p["file"], p["row_key"], p["column"]
            if f not in tables:
                conflicts.append(f"line {i}: no {f} table in batch {a.batch}")
                continue
            fields, rows = tables[f]
            hit = [r for r in rows if r[KEYS[f]] == key]
            if col == "DELETE":
                if not hit:
                    continue  # already deleted
                rows[:] = [r for r in rows if r[KEYS[f]] != key]
                if f == "components" and "component_metrics" in tables:
                    mf, mrows = tables["component_metrics"]
                    mrows[:] = [m for m in mrows if m.get("component_id") != key]
                changes += 1
                log.event("patch", "delete", file=f, key=key, reason=p["reason"])
                continue
            if not hit:
                conflicts.append(f"line {i}: {f} {key} not found")
                continue
            r = hit[0]
            if col not in fields:
                fields.append(col)
            cur = r.get(col, "")
            if cur == p["new"]:
                continue
            if cur != p["old"]:
                conflicts.append(f"line {i}: {f} {key}.{col} is {cur!r}, patch expects {p['old']!r}")
                continue
            r[col] = p["new"]
            changes += 1
            log.event("patch", "set", file=f, key=key, column=col, reason=p["reason"])
        for c in conflicts:
            log.info(f"CONFLICT {c}")
        log.info(f"{a.batch}: {changes} change(s), {len(conflicts)} conflict(s)")
        if conflicts or a.dry_run or not changes:
            return 1 if conflicts else 0
        bak = CACHE / "history_backup"
        bak.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(bak / f"{a.batch}_before_patch.zip", "w", zipfile.ZIP_DEFLATED) as z:
            for f in tables:
                z.write(path_of(a.batch, f), f"{f}.csv")
        for f, (fields, rows) in tables.items():
            with path_of(a.batch, f).open("w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=fields)
                w.writeheader()
                w.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
