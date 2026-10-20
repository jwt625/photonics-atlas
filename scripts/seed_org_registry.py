"""Seed data/registry/organizations.csv and org_aliases.csv from the EO, PK and LIN organization tables.

Append-only (D14): rows whose org_id (or (org_id, alias)) already exists are left untouched; only new rows are added.
Clustering: one cluster per real organization; members are linked by a shared normalized name/alias key (D18) or a
shared ROR id, at most one member per input (two EO, PK or LIN orgs are never merged), plus the manual decisions in
config/org_seed_overrides.yaml. Field priority: EO > LIN > PK > ROR record (D16).

Usage:
  uv run python scripts/seed_org_registry.py --dry-run
  uv run python scripts/seed_org_registry.py --only "eo:Intel Corporation" --only lin:org_coherent   # pilot
  uv run python scripts/seed_org_registry.py
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

import yaml

from photonics_atlas.adapters import eo, lineage, pk, ror
from photonics_atlas.csvio import read_csv, write_csv
from photonics_atlas.paths import REGISTRY, ROOT
from photonics_atlas.runlog import RunLog
from photonics_atlas.schema import columns
from photonics_atlas.textnorm import norm_key, slug

LIN_TYPE = {  # LIN organization_type -> registry org_type (D15); identical names map to themselves
    "acquired_business_unit": "business_unit",
}
LIN_ALIAS_TYPE = {
    "short_name": "short_name",
    "native_name": "native_name",
    "common_name": "printed_variant",
    "legal_name": "legal_name",
    "former_name": "printed_variant",
    "brand": "brand",
    "acronym": "abbreviation",
}
LIN_STATUS = {"active", "acquired", "merged", "defunct", "historical", "unknown"}
ROR_TYPE_ORDER = [
    ("education", "university"),
    ("company", "company"),
    ("facility", "facility"),
    ("government", "government_lab"),
]


@dataclass
class Member:
    ref: str  # eo:<name> | pk:<name> | lin:<id>
    src: str
    name: str
    keys: set[str]
    rec: Any


@dataclass
class Cluster:
    members: list[Member] = field(default_factory=list)

    def by(self, src: str) -> Member | None:
        return next((m for m in self.members if m.src == src), None)


def ror_type(rec: ror.RorRecord) -> str:
    for t, mapped in ROR_TYPE_ORDER:
        if t in rec.types:
            return mapped
    return "other"


def member_names(m: Member) -> list[str]:
    if m.src == "lin":
        return [m.name, *(a.name for a in m.rec.aliases)]
    if m.src == "pk":
        return [m.name, *pk.alias_map().get(m.name, [])]
    return [m.name]


def load_members() -> list[Member]:
    out: list[Member] = []
    for o in eo.orgs():
        out.append(Member(f"eo:{o.org_name}", "eo", o.org_name, {norm_key(o.org_name)}, o))
    amap = pk.alias_map()
    for p in pk.orgs():
        keys = {norm_key(p.org_name)} | {norm_key(v) for v in amap.get(p.org_name, [])}
        out.append(Member(f"pk:{p.org_name}", "pk", p.org_name, keys, p))
    for lo in lineage.orgs():
        keys = {norm_key(lo.name)} | {norm_key(a.name) for a in lo.aliases}
        out.append(Member(f"lin:{lo.id}", "lin", lo.name, keys, lo))
    for m in out:
        m.keys.discard("")
    return out


def cluster(members: list[Member], overrides: dict[str, Any], log: RunLog) -> list[Cluster]:
    idx = {m.ref: i for i, m in enumerate(members)}
    parent = list(range(len(members)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def srcs(root: int) -> set[str]:
        return {members[j].src for j in range(len(members)) if find(j) == root}

    never = {frozenset(p) for p in overrides.get("never_merge", [])}

    def union(a: int, b: int, why: str) -> None:
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if frozenset((members[a].ref, members[b].ref)) in never:
            log.event("cluster", "skipped", reason="never_merge", a=members[a].ref, b=members[b].ref)
            return
        if srcs(ra) & srcs(rb):
            log.event("cluster", "conflict", reason=f"same-input members via {why}", a=members[a].ref, b=members[b].ref)
            return
        parent[rb] = ra
        log.event("cluster", "merged", via=why, a=members[a].ref, b=members[b].ref)

    for a, b in overrides.get("force_merge", []):
        union(idx[a], idx[b], "force_merge")
    by_key: dict[str, list[int]] = defaultdict(list)
    by_ror: dict[str, list[int]] = defaultdict(list)
    for i, m in enumerate(members):
        for k in m.keys:
            by_key[k].append(i)
        if m.src == "eo" and m.rec.ror_id:
            by_ror[m.rec.ror_id].append(i)
    # Name keys first, in input order (EO, PK, LIN), then ROR.
    for k, ids in by_key.items():
        for j in ids[1:]:
            union(ids[0], j, f"key:{k}")
    for r, ids in by_ror.items():
        for j in ids[1:]:
            union(ids[0], j, f"ror:{r}")
    groups: dict[int, Cluster] = defaultdict(Cluster)
    for i, m in enumerate(members):
        groups[find(i)].members.append(m)
    return list(groups.values())


def name_member(c: Cluster, overrides: dict[str, Any]) -> Member:
    for m in c.members:
        src = overrides.get("name_from", {}).get(m.ref)
        if src and c.by(src):
            found = c.by(src)
            assert found is not None
            return found
    nm = c.by("eo") or c.by("lin") or c.by("pk")
    assert nm is not None
    return nm


def build_rows(
    clusters: list[Cluster], ridx: ror.RorIndex, overrides: dict[str, Any], log: RunLog
) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, str]]:
    """Return org rows, alias rows and member-ref -> org_id."""
    ref2id: dict[str, str] = {}
    used: set[str] = set()
    orgs: list[dict[str, str]] = []
    # Pass 1: ids.
    for c in clusters:
        lin_m = c.by("lin")
        name_m = name_member(c, overrides)
        oid = lin_m.rec.id if lin_m else f"org_{slug(norm_key(name_m.name)) or slug(name_m.name)}"
        base, n = oid, 2
        while oid in used:
            oid = f"{base}_{n}"
            n += 1
        used.add(oid)
        for m in c.members:
            ref2id[m.ref] = oid
    # Pass 2: fields.
    name_owner = {}
    for c in clusters:
        nm = name_member(c, overrides)
        name_owner[norm_key(nm.name)] = ref2id[nm.ref]
    aliases: list[dict[str, str]] = []
    for c in clusters:
        e, li, p = c.by("eo"), c.by("lin"), c.by("pk")
        name_m = name_member(c, overrides)
        oid = ref2id[name_m.ref]
        name = name_m.name
        basis = {"eo": "eo_atlas", "lin": "lineage", "pk": "pk_atlas"}[name_m.src]
        note: list[str] = []
        ror_id = e.rec.ror_id if e and e.rec.ror_id else ""
        for m in c.members:
            if not ror_id and m.ref in overrides.get("ror_ids", {}):
                ror_id = overrides["ror_ids"][m.ref]
                note.append("ror_id from config/org_seed_overrides.yaml")
        if not ror_id:
            known_cc = {x for x in ((e.rec.country if e else ""), (p.rec.country if p else "")) if x}
            hit_ids = {
                h.ror_id
                for k in {n for m in c.members for n in member_names(m)}
                for h in ridx.lookup(k)
                if not known_cc or h.country in known_cc
            }
            if len(hit_ids) == 1:
                ror_id = hit_ids.pop()
                note.append("ror_id by exact name match")
            elif len(hit_ids) > 1:
                log.event("ror", "ambiguous", org=oid, ror_ids=sorted(hit_ids))
        rrec = ridx.records.get(ror_id) if ror_id else None
        if e:
            otype = e.rec.org_type
        elif li:
            otype = LIN_TYPE.get(li.rec.organization_type, li.rec.organization_type)
        else:
            otype = p.rec.org_type if p else "unknown"
        types = {
            m.src: (
                m.rec.org_type if m.src != "lin" else LIN_TYPE.get(m.rec.organization_type, m.rec.organization_type)
            )
            for m in c.members
        }
        if len(set(types.values())) > 1:
            note.append("types: " + ", ".join(f"{k} {v}" for k, v in sorted(types.items())))
        country = (e.rec.country if e else "") or (p.rec.country if p else "")
        if not country and li and len(li.rec.countries) == 1:
            country = li.rec.countries[0]
        if not country and rrec:
            country = rrec.country
        parent_ref = ""
        if e and e.rec.parent_org:
            parent_ref = f"eo:{e.rec.parent_org}"
        elif li and li.rec.parent_organization_id:
            parent_ref = f"lin:{li.rec.parent_organization_id}"
        elif p and p.rec.parent_org:
            parent_ref = f"pk:{p.rec.parent_org}"
        for m in c.members:
            if m.ref in overrides.get("parents", {}) and not parent_ref:
                parent_ref = overrides["parents"][m.ref]
                note.append("parent from own name (config/org_seed_overrides.yaml)")
        parent_id = ref2id.get(parent_ref, "")
        if parent_ref and not parent_id:
            log.event("parent", "unresolved", org=oid, parent=parent_ref)
        status = li.rec.status if li and li.rec.status in LIN_STATUS else ""
        if not status:
            status = "active" if rrec and rrec.status == "active" and not li else "unknown"
        founded = (li.rec.founded_date if li else None) or ""
        if not founded and rrec and rrec.established:
            founded = rrec.established
        website = (li.rec.website if li and li.rec.website else "") or (rrec.website if rrec else "")
        name_source = ""
        if e:
            name_source = e.rec.name_source
        elif li:
            name_source = li.rec.website or f"lin:{li.rec.id}"
        else:
            name_source = "pk:data/organizations.csv"
        orgs.append(
            {
                "org_id": oid,
                "name": name,
                "name_basis": basis,
                "name_source": name_source,
                "org_type": otype,
                "supply_roles": "",
                "country": country,
                "parent_org_id": parent_id,
                "status": status,
                "founded_on": founded,
                "dissolved_on": (li.rec.dissolved_date if li else None) or "",
                "ror_id": ror_id,
                "wikidata_qid": rrec.wikidata if rrec and rrec.wikidata.startswith("Q") else "",
                "website": website,
                "origin": ";".join(s for s in ("eo", "pk", "lin") if c.by(s)),
                "notes": "; ".join(note),
            }
        )
        # Aliases: other members' names and their own aliases, when the key differs from the registry name.
        nk = norm_key(name)
        seen = {nk}

        def add(
            alias: str, atype: str, origin: str, abasis: str, anote: str = "", oid: str = oid, seen: set[str] = seen
        ) -> None:
            k = norm_key(alias)
            if not k or k in seen:
                return
            if name_owner.get(k, oid) != oid:
                log.event(
                    "alias", "skipped", reason="equals another org's name", org=oid, alias=alias, owner=name_owner[k]
                )
                return
            seen.add(k)
            aliases.append(
                {
                    "org_id": oid,
                    "alias": alias,
                    "alias_type": atype,
                    "lang": "",
                    "valid_from": "",
                    "valid_to": "",
                    "origin": origin,
                    "scope": overrides.get("alias_scope", {}).get(alias, ""),
                    "basis": abasis,
                    "notes": anote,
                }
            )

        if e:
            add(e.name, "printed_variant", "eo", "eo_name")
        if li:
            add(li.name, "printed_variant", "lin", "lineage_name")
            for a in li.rec.aliases:
                add(
                    a.name,
                    LIN_ALIAS_TYPE.get(a.alias_type, "printed_variant"),
                    "lin",
                    "lineage_alias",
                    f"LIN alias_type {a.alias_type}"
                    if a.alias_type not in ("short_name", "native_name", "legal_name", "brand")
                    else "",
                )
                if a.language and a.language != "en" and aliases and aliases[-1]["alias"] == a.name:
                    aliases[-1]["lang"] = a.language
        if p:
            add(p.name, "printed_variant", "pk", "pk_name")
            for v in pk.alias_map().get(p.name, []):
                add(v, "printed_variant", "pk", "pk_alias_map")
    return orgs, aliases, ref2id


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--only",
        action="append",
        default=[],
        help="pilot: member refs (eo:<name>, pk:<name>, lin:<id>); clusters containing them",
    )
    args = ap.parse_args()
    with RunLog("seed_org_registry", args.dry_run) as log:
        with (ROOT / "config" / "org_seed_overrides.yaml").open() as f:
            overrides: dict[str, Any] = yaml.safe_load(f) or {}
        members = load_members()
        log.info(
            f"members: {len(members)} (eo {sum(m.src == 'eo' for m in members)}, pk {sum(m.src == 'pk' for m in members)}, lin {sum(m.src == 'lin' for m in members)})"
        )
        ridx = ror.load()
        log.info(f"ROR {ridx.version}: {len(ridx.records)} records")
        clusters = cluster(members, overrides, log)
        orgs, aliases, ref2id = build_rows(clusters, ridx, overrides, log)
        log.info(f"clusters/orgs: {len(orgs)}; alias rows: {len(aliases)}")
        multi = [c for c in clusters if len(c.members) > 1]
        log.info(f"multi-member clusters: {len(multi)}")
        if args.only:
            keep = {ref2id[r] for r in args.only if r in ref2id}
            missing = [r for r in args.only if r not in ref2id]
            if missing:
                log.info(f"--only refs not found: {missing}")
            orgs = [o for o in orgs if o["org_id"] in keep]
            aliases = [a for a in aliases if a["org_id"] in keep]
        org_path, al_path = REGISTRY / "organizations.csv", REGISTRY / "org_aliases.csv"
        old_orgs = read_csv(org_path) if org_path.exists() else []
        old_al = read_csv(al_path) if al_path.exists() else []
        have = {o["org_id"] for o in old_orgs}
        have_al = {(a["org_id"], a["alias"]) for a in old_al}
        new_orgs = [o for o in orgs if o["org_id"] not in have]
        new_al = [a for a in aliases if (a["org_id"], a["alias"]) not in have_al]
        # Parents must exist: a pilot subset may reference parents outside it.
        all_ids = have | {o["org_id"] for o in new_orgs}
        for o in new_orgs:
            if o["parent_org_id"] and o["parent_org_id"] not in all_ids:
                log.event("parent", "deferred", org=o["org_id"], parent=o["parent_org_id"])
                o["parent_org_id"] = ""
                o["notes"] = "; ".join(x for x in (o["notes"], "parent deferred (pilot subset)") if x)
        for o in new_orgs:
            log.event("org", "new", org_id=o["org_id"], name=o["name"], origin=o["origin"])
        log.info(
            f"new orgs {len(new_orgs)} (existing kept {len(old_orgs)}); new aliases {len(new_al)} (existing kept {len(old_al)})"
        )
        if args.dry_run:
            for o in new_orgs[:15]:
                log.info(f"  would add {o['org_id']} | {o['name']} | {o['origin']} | {o['country']} | {o['ror_id']}")
            return 0
        write_csv(org_path, columns("organizations"), [*old_orgs, *sorted(new_orgs, key=lambda r: r["org_id"])])
        write_csv(al_path, columns("org_aliases"), [*old_al, *sorted(new_al, key=lambda r: (r["org_id"], r["alias"]))])
        log.info(f"wrote {org_path.relative_to(ROOT)} and {al_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
