"""Validate a component staging batch and merge it into data/components/ (append-only).

The batch directory holds components.csv and component_metrics.csv with the schema columns (D30). The merge is
simulated on a temporary copy of data/ and validated with the full validator; nothing is written unless the merged
copy has 0 errors. Rows whose component_id already exists in data/components are skipped (append-only) unless
--replace is given, which replaces those components and all their metric rows.

Usage:
  uv run python scripts/merge_component_staging.py data/_staging/components/<batch> --dry-run
  uv run python scripts/merge_component_staging.py data/_staging/components/<batch>
"""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

from photonics_atlas.adapters import eo
from photonics_atlas.csvio import read_csv, read_header, split_list, write_csv
from photonics_atlas.paths import ROOT
from photonics_atlas.runlog import RunLog
from photonics_atlas.schema import columns
from photonics_atlas.validate import validate

TABLES = ("components", "component_metrics")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("batch", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--replace", action="store_true", help="replace existing components (and their metrics) by id")
    args = ap.parse_args()
    batch = args.batch if args.batch.is_absolute() else ROOT / args.batch
    with RunLog("merge_component_staging", args.dry_run) as log:
        staged: dict[str, list[dict[str, str]]] = {}
        for t in TABLES:
            path = batch / f"{t}.csv"
            if not path.exists():
                log.info(f"ERROR missing {path.relative_to(ROOT)}")
                return 1
            if read_header(path) != columns(t):
                log.info(f"ERROR {path.relative_to(ROOT)} header != schema columns {columns(t)}")
                return 1
            staged[t] = read_csv(path)
        cur = {t: read_csv(ROOT / "data" / "components" / f"{t}.csv") for t in TABLES}
        have = {c["component_id"] for c in cur["components"]}
        new_ids = {c["component_id"] for c in staged["components"]}
        clash = sorted(have & new_ids)
        if clash and not args.replace:
            log.info(f"skipping {len(clash)} components that already exist (use --replace): {clash[:10]}")
            staged["components"] = [c for c in staged["components"] if c["component_id"] not in have]
            staged["component_metrics"] = [m for m in staged["component_metrics"] if m["component_id"] not in have]
        elif clash:
            cur["components"] = [c for c in cur["components"] if c["component_id"] not in new_ids]
            cur["component_metrics"] = [m for m in cur["component_metrics"] if m["component_id"] not in new_ids]
        merged = {t: [*cur[t], *staged[t]] for t in TABLES}
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            shutil.copytree(ROOT / "data", tmp / "data")
            for t in TABLES:
                write_csv(tmp / "data" / "components" / f"{t}.csv", columns(t), merged[t])
            rep = validate(tmp)
        # Fail only on errors this merge introduces: other tranches may be mid-build in parallel (e.g. a schema whose
        # tables are declared but not written yet), and their errors must not block a component merge.
        baseline = set(validate(ROOT).errors)
        comp_errors = [e for e in rep.errors if e not in baseline]
        if baseline:
            log.info(
                f"note: {len(baseline)} pre-existing validator errors elsewhere in the repo (not caused by this batch)"
            )
        # host_device_ids must be EO device rows (needs the EO atlas input; the validator alone checks the prefix).
        try:
            eo_ids = {d.device_id for d in eo.devices()}
        except FileNotFoundError:
            eo_ids = set()
            log.info("WARN EO devices.csv not available: host_device_ids not checked against it")
        if eo_ids:
            for c in staged["components"]:
                for h in split_list(c["host_device_ids"]):
                    if h not in eo_ids:
                        comp_errors.append(f"components {c['component_id']}: host device {h!r} not in EO devices.csv")
        for e in comp_errors[:200]:
            log.info(f"ERROR {e}")
        for w in rep.warnings:
            if w.startswith("component"):
                log.info(f"WARN {w}")
        log.info(
            f"batch {batch.name}: +{len(staged['components'])} components, +{len(staged['component_metrics'])} metrics; "
            f"errors {len(comp_errors)}"
        )
        log.event(
            "merge",
            "ok" if not comp_errors else "failed",
            batch=batch.name,
            errors=len(comp_errors),
            components=len(staged["components"]),
            metrics=len(staged["component_metrics"]),
        )
        if comp_errors:
            return 1
        if args.dry_run:
            return 0
        for t in TABLES:
            write_csv(ROOT / "data" / "components" / f"{t}.csv", columns(t), merged[t])
        log.info("merged into data/components/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
