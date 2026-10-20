"""Resolve unmapped OFC 2026 affiliation strings through the offline ROR index (D25) and stage the rest for curation.

For each OFC string the matcher cannot map: if exactly one active ROR record has the same normalized display name or
label (aliases excluded, bare acronyms excluded), then
  - its ror_id is already on a registry org -> add the printed string as an alias (basis ror_record), or
  - otherwise add a new org built from the ROR record (name_basis ror; country, type, founding year, Wikidata id,
    website and parent from the record) plus the printed string as an alias when its key differs.
Strings still unmapped go to data/_staging/org_curation/unmapped_<run timestamp>.csv with ROR alias-field candidates as review hints.
Append-only for the registry (existing rows untouched).

Usage: uv run python scripts/add_ror_orgs.py [--dry-run] [--limit N]
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter

from photonics_atlas.adapters import ofc, ror
from photonics_atlas.csvio import read_csv, write_csv
from photonics_atlas.orgmatch import load_matcher
from photonics_atlas.paths import REGISTRY, ROOT, STAGING
from photonics_atlas.runlog import RunLog
from photonics_atlas.schema import columns
from photonics_atlas.textnorm import norm_key, slug

# ROR "facility" covers research labs and centres; the registry's `facility` means shared fabs / cleanrooms (EO usage),
# so ROR facility maps to research_institute (P0 data audit 6.4).
ROR_TYPE_ORDER = [
    ("education", "university"),
    ("company", "company"),
    ("facility", "research_institute"),
    ("government", "government_lab"),
]


def ror_type(rec: ror.RorRecord) -> str:
    for t, mapped in ROR_TYPE_ORDER:
        if t in rec.types:
            return mapped
    return "other"


def display_name(rec: ror.RorRecord) -> str:
    """ROR company records append ' (Country)' as a disambiguator; it is not part of the organization's name."""
    return re.sub(r"\s+\([^()]*\)$", "", rec.name) if "company" in rec.types else rec.name


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="pilot: only the N most frequent unmapped strings")
    args = ap.parse_args()
    with RunLog("add_ror_orgs", args.dry_run) as log:
        m = load_matcher()
        assert m.ridx is not None
        ridx = m.ridx
        orgs = read_csv(REGISTRY / "organizations.csv")
        aliases = read_csv(REGISTRY / "org_aliases.csv")
        ids = {o["org_id"] for o in orgs}
        counts = Counter(a.affiliation for p in ofc.presentations() for a in p.authors if a.affiliation)
        todo = [(s, n) for s, n in counts.most_common() if not m.match(s, "ofc2026")[0]]
        if args.limit:
            todo = todo[: args.limit]
        log.info(f"unmapped OFC strings: {len(todo)} ({sum(n for _, n in todo)} rows)")
        new_orgs: dict[str, dict[str, str]] = {}
        new_aliases: list[dict[str, str]] = []
        unmapped: list[dict[str, object]] = []
        ror2org = dict(m.by_ror)
        for printed, n in todo:
            hits = ridx.lookup(printed)
            if len(hits) != 1:
                cands = [] if hits else ridx.lookup(printed, aliases=True)
                unmapped.append(
                    {
                        "printed": printed,
                        "n_rows": n,
                        "ror_hits": ";".join(f"{h.ror_id} {h.name} ({h.country})" for h in (hits or cands)[:5]),
                        "ror_hit_kind": "ambiguous_name" if hits else ("alias_only" if cands else "none"),
                    }
                )
                continue
            rec = hits[0]
            oid = ror2org.get(rec.ror_id)
            brand = display_name(rec)
            if oid is None and brand != rec.name:
                # Country subsidiary record of a company already in the registry under its brand name (D19).
                bids, _ = m.match(brand, "ofc2026")
                if len(bids) == 1:
                    new_aliases.append(
                        {
                            "org_id": bids[0],
                            "alias": printed,
                            "alias_type": "subsidiary_printed",
                            "lang": "",
                            "valid_from": "",
                            "valid_to": "",
                            "origin": "ofc2026",
                            "scope": "",
                            "basis": "ror_record",
                            "notes": f"ROR subsidiary record {rec.ror_id} ({rec.name})",
                        }
                    )
                    log.event(
                        "alias", "new", org_id=bids[0], alias=printed, ror_id=rec.ror_id, n_rows=n, kind="subsidiary"
                    )
                    continue
            if oid is None:
                name = display_name(rec)
                oid = f"org_{slug(norm_key(name)) or slug(name)}"
                base, k = oid, 2
                while oid in ids:
                    oid = f"{base}_{k}"
                    k += 1
                ids.add(oid)
                ror2org[rec.ror_id] = oid
                new_orgs[oid] = {
                    "org_id": oid,
                    "name": name,
                    "name_basis": "ror",
                    "name_source": rec.ror_id,
                    "org_type": ror_type(rec),
                    "supply_roles": "",
                    "country": rec.country,
                    "parent_org_id": "",
                    "status": "active",
                    "founded_on": rec.established,
                    "dissolved_on": "",
                    "ror_id": rec.ror_id,
                    "wikidata_qid": rec.wikidata if rec.wikidata.startswith("Q") else "",
                    "website": rec.website,
                    "origin": "ofc2026;ror",
                    "notes": f"ROR types: {', '.join(rec.types)}; {ridx.version}",
                }
                log.event("org", "new", org_id=oid, name=name, ror_id=rec.ror_id, printed=printed, n_rows=n)
            if norm_key(printed) != norm_key(display_name(rec)) or oid not in new_orgs:
                new_aliases.append(
                    {
                        "org_id": oid,
                        "alias": printed,
                        "alias_type": "printed_variant",
                        "lang": "",
                        "valid_from": "",
                        "valid_to": "",
                        "origin": "ofc2026",
                        "scope": "",
                        "basis": "ror_record",
                        "notes": f"ROR display/label exact match {rec.ror_id}",
                    }
                )
                log.event("alias", "new", org_id=oid, alias=printed, ror_id=rec.ror_id, n_rows=n)
        # ROR parents for new orgs (only when the parent is already a registry org).
        for o in new_orgs.values():
            rec = ridx.records[o["ror_id"]]
            for par in rec.parents:
                if par in ror2org and ror2org[par] != o["org_id"]:
                    o["parent_org_id"] = ror2org[par]
                    break
        log.info(
            f"new orgs {len(new_orgs)}, new aliases {len(new_aliases)}, still unmapped {len(unmapped)} strings "
            f"({sum(int(str(u['n_rows'])) for u in unmapped)} rows)"
        )
        if args.dry_run:
            for o in list(new_orgs.values())[:20]:
                log.info(f"  would add {o['org_id']} | {o['name']} | {o['country']} | {o['org_type']}")
            return 0
        write_csv(
            REGISTRY / "organizations.csv",
            columns("organizations"),
            [*orgs, *sorted(new_orgs.values(), key=lambda r: r["org_id"])],
        )
        have = {(a["org_id"], a["alias"]) for a in aliases}
        add = [a for a in new_aliases if (a["org_id"], a["alias"]) not in have]
        write_csv(REGISTRY / "org_aliases.csv", columns("org_aliases"), [*aliases, *add])
        # Timestamped: a rerun must not overwrite the record of an earlier run (P0 code audit S1).
        out = STAGING / "org_curation" / f"unmapped_{log.log_path.stem.rsplit('_', 1)[-1]}.csv"
        write_csv(out, ["printed", "n_rows", "ror_hit_kind", "ror_hits"], unmapped)
        log.info(f"wrote registry (+{len(new_orgs)} orgs, +{len(add)} aliases) and {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
