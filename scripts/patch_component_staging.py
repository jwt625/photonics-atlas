"""Apply a coordinator patch (audit corrections, schema migrations) to a component staging batch.

Patch file (YAML) keys, applied in this order; every op carries a `why`:
  rename_columns: {old: new}            schema migrations (also adds missing schema columns, empty)
  components:     {component_id: {field: value, ...}}
  metrics:        {metric_id: {field: value, ...}}
  delete_metrics: [{id: metric_id, why: ...}]
  delete_components: [{id: component_id, why: ...}]  (also drops its metric rows)
  add_components: [{...row..., why: ...}]
  add_metrics:    [{...row..., why: ...}]
Idempotent: re-applying a patch changes nothing. Writes the batch CSVs in schema column order; logs every change.

Usage: uv run python scripts/patch_component_staging.py data/_staging/components/<batch> <patch.yaml> [--dry-run]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

from photonics_atlas.csvio import read_csv, write_csv
from photonics_atlas.paths import ROOT
from photonics_atlas.runlog import RunLog
from photonics_atlas.schema import columns


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("batch", type=Path)
    ap.add_argument("patch", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    batch = args.batch if args.batch.is_absolute() else ROOT / args.batch
    patch: dict[str, Any] = yaml.safe_load((args.patch if args.patch.is_absolute() else ROOT / args.patch).read_text())
    with RunLog("patch_component_staging", args.dry_run) as log:
        comps = read_csv(batch / "components.csv")
        mets = read_csv(batch / "component_metrics.csv")
        n = 0
        for old, new in (patch.get("rename_columns") or {}).items():
            for r in [*comps, *mets]:
                if old in r:
                    r[new] = r.pop(old)
                    n += 1
        for rows, table in ((comps, "components"), (mets, "component_metrics")):
            for r in rows:
                for c in columns(table):
                    r.setdefault(c, "")
        cid = {c["component_id"]: c for c in comps}
        mid = {m["metric_id"]: m for m in mets}
        for key, rows_by, cols in (
            ("components", cid, columns("components")),
            ("metrics", mid, columns("component_metrics")),
        ):
            for rid, spec in (patch.get(key) or {}).items():
                if rid not in rows_by:
                    raise SystemExit(f"{key}: unknown id {rid}")
                for f, v in spec.items():
                    if f == "why":
                        continue
                    if f not in cols:
                        raise SystemExit(f"{rid}: unknown column {f}")
                    if rows_by[rid][f] != str(v):
                        log.event(key, "set", id=rid, field=f, old=rows_by[rid][f], new=str(v), why=spec.get("why", ""))
                        rows_by[rid][f] = str(v)
                        n += 1
        for d in patch.get("delete_metrics") or []:
            if d["id"] in mid:
                mets = [m for m in mets if m["metric_id"] != d["id"]]
                log.event("metrics", "delete", id=d["id"], why=d.get("why", ""))
                n += 1
        for d in patch.get("delete_components") or []:
            if d["id"] in cid:
                comps = [c for c in comps if c["component_id"] != d["id"]]
                dropped = [m["metric_id"] for m in mets if m["component_id"] == d["id"]]
                mets = [m for m in mets if m["component_id"] != d["id"]]
                log.event("components", "delete", id=d["id"], metrics=dropped, why=d.get("why", ""))
                n += 1 + len(dropped)
        for row in patch.get("add_components") or []:
            if row["component_id"] not in cid:
                comps.append({c: str(row.get(c, "")) for c in columns("components")})
                log.event("components", "add", id=row["component_id"], why=row.get("why", ""))
                n += 1
        have = {m["metric_id"] for m in mets}
        for row in patch.get("add_metrics") or []:
            if row["metric_id"] not in have:
                mets.append({c: str(row.get(c, "")) for c in columns("component_metrics")})
                log.event("metrics", "add", id=row["metric_id"], why=row.get("why", ""))
                n += 1
        log.info(f"{batch.name}: {n} changes")
        if not args.dry_run:
            write_csv(batch / "components.csv", columns("components"), comps)
            write_csv(batch / "component_metrics.csv", columns("component_metrics"), mets)
    return 0


if __name__ == "__main__":
    sys.exit(main())
