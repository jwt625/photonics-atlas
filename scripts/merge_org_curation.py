"""Merge reviewed curation decisions (data/_staging/org_curation/batch_*/decisions.csv) into the registry.

Per decision row (contract: data/_staging/org_curation/INSTRUCTIONS.md):
  alias   -> org_aliases row (basis curated, origin ofc2026, notes = evidence)
  new_org -> organizations row (once per org; cross-batch duplicates unified by ROR id or normalized name, and a
             proposed org that already exists in the registry under its name/ROR becomes an alias of it) + alias row
             when the printed string differs from the name
  joint   -> one joint_printed alias row per org
  skip    -> data/_staging/org_curation/skipped.csv (review queue)
Optional decision columns (D270, org round 5): origin (input where the string was seen; default ofc2026), scope
(alias corpora), valid_from (alias), name_source (new org; default the ROR id or "<origin> printed (<batch>)"),
supply_roles and no_name_match (new org).
Coordinator corrections are applied from config/org_curation_overrides.yaml before merging. Append-only: existing
registry rows are not modified.

Usage: uv run python scripts/merge_org_curation.py [--dry-run]
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import yaml

from photonics_atlas.adapters import ror
from photonics_atlas.csvio import read_csv, split_list, write_csv
from photonics_atlas.paths import REGISTRY, ROOT, STAGING
from photonics_atlas.runlog import RunLog
from photonics_atlas.schema import columns, load_schema
from photonics_atlas.textnorm import norm_key

DEC_COLS = [
    "printed",
    "n_rows",
    "action",
    "org_id",
    "alias_type",
    "new_name",
    "name_basis",
    "ror_id",
    "org_type",
    "country",
    "parent_org_id",
    "evidence",
    "notes",
]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    with RunLog("merge_org_curation", args.dry_run) as log:
        enums = load_schema()["enums"]
        ov_path = ROOT / "config" / "org_curation_overrides.yaml"
        ov: dict[str, Any] = (yaml.safe_load(ov_path.read_text()) or {}) if ov_path.exists() else {}
        row_ov: dict[str, dict[str, str]] = ov.get("rows", {})
        id_ov: dict[str, str] = ov.get("unify_ids", {})
        org_ov: dict[str, dict[str, str]] = ov.get("orgs", {})
        ridx = ror.load()
        orgs = read_csv(REGISTRY / "organizations.csv")
        aliases = read_csv(REGISTRY / "org_aliases.csv")
        have = {o["org_id"]: o for o in orgs}
        name2id = {norm_key(o["name"]): o["org_id"] for o in orgs if o["no_name_match"] != "true"}
        alias2id = {norm_key(a["alias"]): a["org_id"] for a in aliases if not a["scope"]}
        ror2id = {o["ror_id"]: o["org_id"] for o in orgs if o["ror_id"]}

        decisions: list[dict[str, str]] = []
        for d in sorted(STAGING.glob("org_curation/batch_*/decisions.csv")):
            for r in read_csv(d):
                missing = [c for c in DEC_COLS if c not in r]
                if missing:
                    raise SystemExit(f"{d}: missing columns {missing}")
                r["batch"] = d.parent.name
                r.update(row_ov.get(r["printed"], {}))
                decisions.append(r)
        log.info(f"decisions: {len(decisions)} from {len({r['batch'] for r in decisions})} batches")

        # Pass 1: unify new-org ids (overrides, then existing registry orgs, then cross-batch by ROR id / name).
        remap: dict[str, str] = dict(id_ov)
        first_spec: dict[str, dict[str, str]] = {}
        key_owner: dict[str, str] = {}
        for r in decisions:
            if r["action"] != "new_org":
                continue
            pid = remap.get(r["org_id"], r["org_id"])
            k = norm_key(r["new_name"])
            # An id already in the registry is that org (no_name_match orgs have no name key to unify by, D270).
            existing = (
                (pid if pid in have else "")
                or (r["ror_id"] and ror2id.get(r["ror_id"]))
                or name2id.get(k)
                or alias2id.get(k)
            )
            if existing:
                remap[r["org_id"]] = existing
                log.event("unify", "to_existing", proposed=r["org_id"], existing=existing, batch=r["batch"])
                continue
            other = key_owner.get(f"ror:{r['ror_id']}") if r["ror_id"] else None
            other = other or key_owner.get(f"name:{k}")
            if other and other != pid:
                remap[r["org_id"]] = other
                log.event("unify", "cross_batch", proposed=r["org_id"], to=other, batch=r["batch"])
                continue
            if r["ror_id"]:
                key_owner[f"ror:{r['ror_id']}"] = pid
            key_owner[f"name:{k}"] = pid
            first_spec.setdefault(pid, r)

        def rid(x: str) -> str:
            seen = set()
            while x in remap and x not in seen:
                seen.add(x)
                x = remap[x]
            return x

        new_orgs: dict[str, dict[str, str]] = {}
        for pid, r in first_spec.items():
            if rid(pid) != pid:
                continue
            if r["ror_id"] and r["ror_id"] not in ridx.records:
                raise SystemExit(f"{pid}: ror_id {r['ror_id']} not in the ROR dump")
            if r["org_type"] not in enums["org_type"] or r["name_basis"] not in enums["name_basis"]:
                raise SystemExit(f"{pid}: bad org_type/name_basis {r['org_type']!r}/{r['name_basis']!r}")
            if bad := [x for x in split_list(r.get("supply_roles", "")) if x not in enums["supply_role"]]:
                raise SystemExit(f"{pid}: bad supply_roles {bad}")
            rec = ridx.records.get(r["ror_id"]) if r["ror_id"] else None
            o = {
                "org_id": pid,
                "name": r["new_name"],
                "name_basis": r["name_basis"],
                "name_source": r.get("name_source")
                or r["ror_id"]
                or f"{r.get('origin') or 'ofc2026'} printed ({r['batch']})",
                "org_type": r["org_type"],
                "supply_roles": r.get("supply_roles", ""),
                "country": r["country"],
                "parent_org_id": r["parent_org_id"],
                "status": "active" if rec and rec.status == "active" else "unknown",
                "founded_on": rec.established if rec else "",
                "ror_id": r["ror_id"],
                "wikidata_qid": rec.wikidata if rec and rec.wikidata.startswith("Q") else "",
                "website": rec.website if rec else "",
                "origin": ";".join(
                    sorted(
                        set(split_list(r.get("origin") or "ofc2026")) | ({"ror"} if rec else set()),
                        key=enums["origin"].index,
                    )
                ),
                "no_name_match": r.get("no_name_match", ""),
                "notes": f"curated ({r['batch']}): {r['evidence']}" + (f"; {r['notes']}" if r["notes"] else ""),
            }
            o.update(org_ov.get(pid, {}))
            new_orgs[pid] = o
        all_ids = set(have) | set(new_orgs)
        for o in new_orgs.values():
            if o["parent_org_id"]:
                o["parent_org_id"] = rid(o["parent_org_id"])
                if o["parent_org_id"] not in all_ids:
                    log.event("parent", "unresolved", org=o["org_id"], parent=o["parent_org_id"])
                    o["parent_org_id"] = ""

        # Pass 2: alias rows.
        new_al: list[dict[str, str]] = []
        skipped: list[dict[str, str]] = []
        have_al = {(a["org_id"], a["alias"]) for a in aliases}

        def add_alias(oid: str, r: dict[str, str], atype: str) -> None:
            oid = rid(oid)
            if oid not in all_ids:
                raise SystemExit(f"{r['batch']}: {r['printed']!r} -> unknown org {oid}")
            target_name = new_orgs[oid]["name"] if oid in new_orgs else have[oid]["name"]
            # A string equal to the org name needs no alias, except a scoped one (no_name_match orgs, D201 / D270).
            same = norm_key(r["printed"]) == norm_key(target_name) and not r.get("scope")
            if same or (oid, r["printed"]) in have_al:
                return
            if atype not in enums["alias_type"]:
                raise SystemExit(f"{r['batch']}: bad alias_type {atype!r} for {r['printed']!r}")
            have_al.add((oid, r["printed"]))
            new_al.append(
                {
                    "org_id": oid,
                    "alias": r["printed"],
                    "alias_type": atype,
                    "lang": "",
                    "valid_from": r.get("valid_from", ""),
                    "valid_to": "",
                    "origin": split_list(r.get("origin") or "ofc2026")[0],
                    "scope": r.get("scope", ""),
                    "basis": "curated",
                    "notes": f"{r['batch']}: {r['evidence']}" + (f"; {r['notes']}" if r["notes"] else ""),
                }
            )

        for r in decisions:
            a = r["action"]
            if a == "alias":
                add_alias(r["org_id"], r, r["alias_type"] or "printed_variant")
            elif a == "new_org":
                add_alias(r["org_id"], r, r["alias_type"] or "printed_variant")
            elif a == "joint":
                for oid in split_list(r["org_id"]):
                    add_alias(oid, r, "joint_printed")
            elif a == "skip":
                skipped.append(
                    {
                        "printed": r["printed"],
                        "n_rows": r["n_rows"],
                        "batch": r["batch"],
                        "reason": r["evidence"] + (f"; {r['notes']}" if r["notes"] else ""),
                    }
                )
            else:
                raise SystemExit(f"{r['batch']}: unknown action {a!r}")
        log.info(
            f"new orgs {len(new_orgs)}, new aliases {len(new_al)}, skipped strings {len(skipped)} "
            f"({sum(int(s['n_rows']) for s in skipped)} rows)"
        )
        for o in new_orgs.values():
            log.event(
                "org",
                "new",
                org_id=o["org_id"],
                name=o["name"],
                country=o["country"],
                type=o["org_type"],
                ror=o["ror_id"],
            )
        if args.dry_run:
            return 0
        write_csv(
            REGISTRY / "organizations.csv",
            columns("organizations"),
            [*orgs, *sorted(new_orgs.values(), key=lambda r: r["org_id"])],
        )
        write_csv(REGISTRY / "org_aliases.csv", columns("org_aliases"), [*aliases, *new_al])
        write_csv(STAGING / "org_curation" / "skipped.csv", ["printed", "n_rows", "batch", "reason"], skipped)
        log.info("wrote organizations.csv, org_aliases.csv, org_curation/skipped.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
