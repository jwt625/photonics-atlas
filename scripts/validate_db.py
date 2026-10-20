"""Validate the registry against data/schema/registry.schema.yaml.

Usage: uv run python scripts/validate_db.py [--quiet]
Exit 1 when any error is found. Writes logs/validate_db_<ts>.log.
"""

from __future__ import annotations

import argparse
import sys

from photonics_atlas.runlog import RunLog
from photonics_atlas.validate import validate


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--quiet", action="store_true", help="print counts and totals only")
    args = ap.parse_args()
    with RunLog("validate_db") as log:
        rep = validate()
        for k, v in rep.counts.items():
            log.info(f"rows {k}: {v}")
        for e in rep.errors if not args.quiet else rep.errors[:20]:
            log.info(f"ERROR {e}")
        for w in rep.warnings if not args.quiet else []:
            log.info(f"WARN {w}")
        log.info(f"errors {len(rep.errors)}, warnings {len(rep.warnings)}")
        log.event(
            "validate",
            "ok" if not rep.errors else "failed",
            errors=len(rep.errors),
            warnings=len(rep.warnings),
            counts=rep.counts,
        )
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
