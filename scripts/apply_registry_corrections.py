"""Apply config/registry_corrections.yaml to data/registry/organizations.csv and org_aliases.csv.

Idempotent: applying twice changes nothing the second time. Every applied change is logged with its reason. A
correction whose target row does not exist is an error (nothing is written). Run after the merge scripts and before
build_org_crosswalk (README pipeline order).

Usage: uv run python scripts/apply_registry_corrections.py [--dry-run]
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import yaml

from photonics_atlas.csvio import read_csv, write_csv
from photonics_atlas.paths import REGISTRY, ROOT
from photonics_atlas.runlog import RunLog
from photonics_atlas.schema import columns


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    with RunLog("apply_registry_corrections", args.dry_run) as log:
        cfg: dict[str, Any] = yaml.safe_load((ROOT / "config" / "registry_corrections.yaml").read_text()) or {}
        orgs = read_csv(REGISTRY / "organizations.csv")
        aliases = read_csv(REGISTRY / "org_aliases.csv")
        by_id = {o["org_id"]: o for o in orgs}
        cols_o, cols_a = set(columns("organizations")), set(columns("org_aliases"))
        changed = 0
        for oid, spec in (cfg.get("orgs") or {}).items():
            if oid not in by_id:
                raise SystemExit(f"correction for unknown org {oid}")
            for k, v in spec.items():
                if k == "why":
                    continue
                if k not in cols_o:
                    raise SystemExit(f"{oid}: unknown column {k}")
                if by_id[oid][k] != str(v):
                    log.event("org", "set", org_id=oid, field=k, old=by_id[oid][k], new=str(v), why=spec.get("why", ""))
                    by_id[oid][k] = str(v)
                    changed += 1
        for oid in cfg.get("orgs_retype_facility") or []:
            if oid not in by_id:
                raise SystemExit(f"retype for unknown org {oid}")
            if by_id[oid]["org_type"] == "facility":
                log.event(
                    "org",
                    "set",
                    org_id=oid,
                    field="org_type",
                    old="facility",
                    new="research_institute",
                    why="ROR facility (audit 6.4)",
                )
                by_id[oid]["org_type"] = "research_institute"
                changed += 1
        for c in cfg.get("aliases") or []:
            m = c["match"]
            hits = [a for a in aliases if a["org_id"] == m["org_id"] and a["alias"] == m["alias"]]
            if not hits:
                done = [
                    a
                    for a in aliases
                    if a["alias"] == m["alias"] and all(a.get(k) == str(v) for k, v in c["set"].items())
                ]
                if done:
                    continue  # already applied (org_id was re-pointed on an earlier run)
                raise SystemExit(f"alias correction target not found: {m}")
            for a in hits:
                for k, v in c["set"].items():
                    if k not in cols_a:
                        raise SystemExit(f"alias {m}: unknown column {k}")
                    if a[k] != str(v):
                        log.event("alias", "set", match=m, field=k, old=a[k], new=str(v), why=c.get("why", ""))
                        a[k] = str(v)
                        changed += 1
        have = {(a["org_id"], a["alias"]) for a in aliases}
        for row in cfg.get("add_aliases") or []:
            if (row["org_id"], row["alias"]) in have:
                continue
            if row["org_id"] not in by_id:
                raise SystemExit(f"add_aliases: unknown org {row['org_id']}")
            aliases.append({c: str(row.get(c, "")) for c in columns("org_aliases")})
            log.event("alias", "add", org_id=row["org_id"], alias=row["alias"])
            changed += 1
        log.info(f"changes: {changed}")
        if not args.dry_run and changed:
            write_csv(REGISTRY / "organizations.csv", columns("organizations"), orgs)
            write_csv(REGISTRY / "org_aliases.csv", columns("org_aliases"), aliases)
            log.info("wrote organizations.csv, org_aliases.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
