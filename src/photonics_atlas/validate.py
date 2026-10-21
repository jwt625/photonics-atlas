"""Registry validation driven by data/schema/registry.schema.yaml (rules (a)-(g), decisions D13-D29).

Cell level: header = schema columns; required cells (lists need >= 1 item); types (str, int, bool, enum, list, pdate,
fk); patterns; ISO partial dates with a plausible year; country codes (data/schema/country_codes.txt). Table level: key
uniqueness; foreign keys (orphans); a table marked `built` must exist. Rule level (only on rows without cell errors):
date order; org name/origin consistency, name-key collisions, parent cycles; alias scope/joint rules; event roles per
type, grade/status compatibility, event grade vs cited source grades, locator presence and form, imported-lineage
anchors; source prefixes, same_as chains, DOI duplicates, rights of non-OA corpora; crosswalk consistency with the
registry (name/alias basis re-checked) and the P0 acceptance criteria.
"""

from __future__ import annotations

import datetime as dt
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .csvio import read_csv, read_header, split_list
from .paths import ROOT
from .schema import load_layouts, load_parameters, load_schema
from .textnorm import norm_key

PDATE = re.compile(r"^\d{4}(-(0[1-9]|1[0-2])(-(0[1-9]|[12]\d|3[01]))?)?$")
INT = re.compile(r"^-?[0-9]+$")
FLOAT = re.compile(r"^-?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][-+]?[0-9]+)?$")
MIN_YEAR = 500  # oldest institutions in ROR (e.g. Hunan University 976) pass; year 0000 does not
GRADE_STATUS = {
    "A": {"validated", "asserted", "disputed"},
    "B": {"validated", "asserted", "disputed"},
    "C": {"asserted", "disputed"},
    "D": {"asserted", "disputed"},
    "X": {"inferred"},
}
GRADE_RANK = {"A": 0, "B": 1, "C": 2, "D": 3, "X": 4}
# event_type -> (required roles, allowed roles); unit_reorg allows any role.
EVENT_ROLES: dict[str, tuple[set[str], set[str]]] = {
    "acquisition": ({"target", "acquirer"}, {"target", "acquirer"}),
    "merger": ({"merging"}, {"merging", "resulting"}),
    "spin_off": ({"parent", "spun_off"}, {"parent", "spun_off"}),
    "rename": ({"predecessor", "successor"}, {"predecessor", "successor"}),
    "dissolution": ({"target"}, {"target"}),
    "team_formation": ({"successor"}, {"predecessor", "successor"}),
}
EVENT_SOURCE_CORPORA = {"web", "lin", "ds"}
NAME_BASIS_ORIGIN: dict[str, set[str]] = {
    "eo_atlas": {"eo"},
    "lineage": {"lin"},
    "pk_atlas": {"pk"},
    "cited_source": {"web"},
    "printed": {"ofc2026", "eo", "pk"},
}
RESTRICTED_CORPORA = {"ofc2026", "pk"}  # D4, D23: facts and locators only
LOCATOR_MAX = 300  # quote <= 200 chars (D7) plus position text


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def pdate_ok(s: str) -> bool:
    if not PDATE.match(s):
        return False
    if not MIN_YEAR <= int(s[:4]) <= dt.date.today().year + 1:
        return False
    if len(s) == 10:
        try:
            dt.date.fromisoformat(s)
        except ValueError:
            return False
    return True


def pdate_lo(s: str) -> str:
    """Earliest day an ISO partial date can mean (callers pass only pdate_ok values)."""
    return s + {4: "-01-01", 7: "-01", 10: ""}[len(s)]


def pdate_hi(s: str) -> str:
    if len(s) == 4:
        return s + "-12-31"
    if len(s) == 7:
        y, m = int(s[:4]), int(s[5:7])
        nxt = dt.date(y + (m == 12), m % 12 + 1, 1)
        return (nxt - dt.timedelta(days=1)).isoformat()
    return s


def _before(a: str, b: str) -> bool:
    """True when partial date a certainly ends before b starts; False when either is missing or malformed."""
    return bool(a and b and pdate_ok(a) and pdate_ok(b) and pdate_hi(a) < pdate_lo(b))


def _country_codes() -> set[str]:
    path = ROOT / "data" / "schema" / "country_codes.txt"
    return {ln.strip() for ln in path.read_text().splitlines() if ln.strip() and not ln.startswith("#")}


def _cell_error(col: dict[str, Any], cell: str, schema: dict[str, Any], countries: set[str]) -> str | None:
    t = col["type"]
    pats = schema["patterns"]
    enums = schema["enums"]
    if cell != cell.strip():
        return f"leading/trailing whitespace: {cell!r}"
    if t == "int":
        if not INT.match(cell):
            return f"not an int: {cell!r}"
    elif t == "float":
        if not FLOAT.match(cell):
            return f"not a number: {cell!r}"
    elif t == "bool":
        if cell not in ("true", "false"):
            return f"not a bool (true/false): {cell!r}"
    elif t == "enum":
        if cell not in enums[col["enum"]]:
            return f"{cell!r} not in enum {col['enum']}"
    elif t == "pdate":
        if not pdate_ok(cell):
            return f"not an ISO date (YYYY, YYYY-MM, YYYY-MM-DD; year {MIN_YEAR}..next year): {cell!r}"
    elif t == "list":
        items = split_list(cell)
        if not items:
            return f"empty list: {cell!r}"
        if "enum" in col:
            bad = [x for x in items if x not in enums[col["enum"]]]
            if bad:
                return f"{bad} not in enum {col['enum']}"
        if len(items) != len(set(items)):
            return f"duplicate list items: {cell!r}"
    if "pattern" in col and not re.match(pats[col["pattern"]], cell):
        return f"{cell!r} does not match pattern {col['pattern']}"
    if col.get("pattern") == "country" and cell not in countries:
        return f"{cell!r} not a known ISO 3166-1 alpha-2 code (data/schema/country_codes.txt)"
    return None


def validate(root: Path = ROOT) -> Report:
    schema = load_schema()
    countries = _country_codes()
    rep = Report()
    tables: dict[str, list[dict[str, str]]] = {}
    bad: dict[str, set[int]] = defaultdict(set)  # row indexes with cell errors: rule checks skip them
    for name, spec in schema["tables"].items():
        path = root / spec["path"]
        if not path.exists():
            (rep.err if spec.get("built") else rep.warn)(f"{spec['path']}: missing (table {name})")
            tables[name] = []
            continue
        want = [c["name"] for c in spec["columns"]]
        have = read_header(path)
        if have != want:
            rep.err(f"{spec['path']}: header {have} != schema {want}")
            tables[name] = []
            continue
        rows = read_csv(path)
        tables[name] = rows
        rep.counts[name] = len(rows)
        keyc = Counter(tuple(r[k] for k in spec["key"]) for r in rows)
        for k, n in keyc.items():
            if n > 1:
                rep.err(f"{name}: duplicate key {k} ({n} rows)")
        for i, r in enumerate(rows):
            for col in spec["columns"]:
                cell = r[col["name"]]
                if cell == "":
                    if col.get("required"):
                        rep.err(f"{name} line {i + 2}: {col['name']} required")
                        bad[name].add(i)
                    continue
                e = _cell_error(col, cell, schema, countries)
                if e:
                    rep.err(f"{name} line {i + 2}: {col['name']}: {e}")
                    bad[name].add(i)

    # Foreign keys (orphans).
    keysets: dict[str, set[str]] = {}
    for name, spec in schema["tables"].items():
        if len(spec["key"]) == 1:
            keysets[f"{name}.{spec['key'][0]}"] = {r[spec["key"][0]] for r in tables[name]}
    for name, spec in schema["tables"].items():
        for col in spec["columns"]:
            ref = col.get("ref") or col.get("fk")
            if not ref:
                continue
            target = keysets.get(ref, set())
            for i, r in enumerate(tables[name]):
                cell = r[col["name"]]
                vals = split_list(cell) if col["type"] == "list" else ([cell] if cell else [])
                for v in vals:
                    if v not in target:
                        rep.err(f"{name} line {i + 2}: {col['name']} {v!r} not found in {ref} (orphan)")
                        bad[name].add(i)

    ok = {n: [r for i, r in enumerate(rows) if i not in bad[n]] for n, rows in tables.items()}
    _org_rules(ok, tables, rep)
    _alias_rules(ok, tables, rep)
    _event_rules(ok, tables, rep)
    _source_rules(ok, rep)
    _crosswalk_rules(ok, tables, rep)
    _component_rules(ok, tables, rep)
    # Tranche rule modules (P2 supply, P3 people): photonics_atlas/rules_<name>.py with
    # rules(ok_tables, all_tables, report). Each tranche owns its module; this file stays shared.
    import importlib

    for name in ("supply", "people"):
        try:
            mod = importlib.import_module(f"photonics_atlas.rules_{name}")
        except ModuleNotFoundError as e:
            if name == "people":  # P3 audit C3: the people rules are required, never silently skipped
                rep.err(f"photonics_atlas.rules_people not importable ({e}); people rule checks not run")
            continue
        if name == "people":
            mod.rules(ok, tables, rep, root)  # P3 audit 2: the people rules derive their file paths from the root
        else:
            mod.rules(ok, tables, rep)
    return rep


def _org_rules(t: dict[str, list[dict[str, str]]], full: dict[str, list[dict[str, str]]], rep: Report) -> None:
    orgs = {r["org_id"]: r for r in full["organizations"]}
    for r in t["organizations"]:
        oid = r["org_id"]
        if _before(r["dissolved_on"], r["founded_on"]):
            rep.err(f"organizations {oid}: founded_on {r['founded_on']} after dissolved_on {r['dissolved_on']}")
        if r["parent_org_id"] == oid:
            rep.err(f"organizations {oid}: parent_org_id is itself")
        if r["name_basis"] == "ror" and not r["ror_id"]:
            rep.err(f"organizations {oid}: name_basis ror without ror_id")
        need = NAME_BASIS_ORIGIN.get(r["name_basis"])
        if need and not need & set(split_list(r["origin"])):
            rep.err(f"organizations {oid}: name_basis {r['name_basis']} but origin {r['origin']} lacks {sorted(need)}")
    for oid in orgs:
        seen = {oid}
        cur = orgs[oid]["parent_org_id"]
        while cur:
            if cur in seen:
                rep.err(f"organizations {oid}: parent cycle via {cur}")
                break
            seen.add(cur)
            cur = orgs[cur]["parent_org_id"] if cur in orgs else ""
    for col in ("ror_id", "wikidata_qid"):
        c = Counter(r[col] for r in orgs.values() if r[col])
        for v, n in c.items():
            if n > 1:
                ids = sorted(o for o, r in orgs.items() if r[col] == v)
                rep.warn(f"organizations: {col} {v} shared by {ids} (unit vs parent, or a merge to review)")
    targets = {p["org_id"] for p in full["org_event_participants"] if p["role"] in ("target", "merging", "predecessor")}
    for r in t["organizations"]:
        if r["status"] in ("acquired", "merged", "renamed") and r["org_id"] not in targets:
            rep.warn(f"organizations {r['org_id']}: status {r['status']} without an org event")


def _alias_rules(t: dict[str, list[dict[str, str]]], full: dict[str, list[dict[str, str]]], rep: Report) -> None:
    names: dict[str, str] = {}
    own: dict[str, str] = {}
    for r in full["organizations"]:
        own[r["org_id"]] = norm_key(r["name"])
        if r["no_name_match"] == "true":
            continue
        k = norm_key(r["name"])
        if k in names:
            rep.err(
                f"organizations: {r['org_id']} and {names[k]} share the name key {k!r} "
                "(set no_name_match on the historical one)"
            )
        names[k] = r["org_id"]
    by_alias: dict[tuple[str, str], set[str]] = defaultdict(set)
    types: dict[tuple[str, str], set[str]] = defaultdict(set)
    for i, r in enumerate(t["org_aliases"], start=2):
        k = norm_key(r["alias"])
        if not k:
            rep.err(f"org_aliases line {i}: alias normalizes to empty")
            continue
        for sc in split_list(r["scope"]) or ["*"]:
            by_alias[(k, sc)].add(r["org_id"])
            types[(k, sc)].add(r["alias_type"])
        if _before(r["valid_to"], r["valid_from"]):
            rep.err(f"org_aliases line {i}: valid_from after valid_to")
        if k in names and names[k] != r["org_id"] and not r["scope"]:
            rep.err(f"org_aliases line {i}: alias {r['alias']!r} -> {r['org_id']} collides with the name of {names[k]}")
        if k == own.get(r["org_id"]):
            rep.warn(f"org_aliases line {i}: alias {r['alias']!r} has the same key as its org name (redundant)")
    for (k, sc), ids in by_alias.items():
        if len(ids) > 1 and types[(k, sc)] != {"joint_printed"}:
            rep.err(f"org_aliases: {k!r} (scope {sc}) maps to {sorted(ids)} but is not joint_printed on every row")


def _event_rules(t: dict[str, list[dict[str, str]]], full: dict[str, list[dict[str, str]]], rep: Report) -> None:
    orgs = {r["org_id"]: r for r in full["organizations"]}
    src = {r["source_id"]: r for r in full["sources"]}
    parts: dict[str, list[dict[str, str]]] = defaultdict(list)
    for p in full["org_event_participants"]:
        parts[p["event_id"]].append(p)
    for r in t["org_events"]:
        eid = r["event_id"]
        if r["status"] not in GRADE_STATUS[r["grade"]]:
            rep.err(f"org_events {eid}: status {r['status']} incompatible with grade {r['grade']}")
        sids = split_list(r["source_ids"])
        if r["grade"] == "X":
            if not r["notes"]:
                rep.err(f"org_events {eid}: grade X needs a rationale in notes")
        else:
            if not sids:
                rep.err(f"org_events {eid}: grade {r['grade']} needs source_ids")
            if not r["locator"]:
                rep.err(f"org_events {eid}: grade {r['grade']} needs a locator")
        for s in sids:
            sr = src.get(s)
            if sr is None:
                continue  # orphan, reported by the fk check
            if sr["corpus"] not in EVENT_SOURCE_CORPORA:
                rep.err(f"org_events {eid}: cites {s}; event sources must be web:, lin: or ds: documents")
            if sr["same_as"]:
                rep.warn(f"org_events {eid}: cites duplicate {s} (canonical {sr['same_as']})")
        grades = [src[s]["evidence_grade"] for s in sids if s in src and src[s]["evidence_grade"]]
        if grades and r["grade"] != "X" and GRADE_RANK[r["grade"]] < min(GRADE_RANK[g] for g in grades):
            rep.err(f"org_events {eid}: grade {r['grade']} better than its best cited source grade {sorted(grades)[0]}")
        loc = r["locator"]
        if r["basis"] == "imported_lineage":
            if loc != f"lin:canonical/events.yaml#{eid}":
                rep.err(f"org_events {eid}: imported_lineage locator must be lin:canonical/events.yaml#{eid}")
            if any(not s.startswith("lin:") for s in sids):
                rep.err(f"org_events {eid}: imported_lineage events cite lin: sources only")
        elif loc and not (10 <= len(loc) <= LOCATOR_MAX and re.search(r"[A-Za-z]{3}", loc)):
            rep.err(f"org_events {eid}: locator must be a quote (<= 200 chars) plus position, 10..{LOCATOR_MAX} chars")
        if not r["announced_on"] and not r["effective_on"]:
            rep.warn(f"org_events {eid}: no date")
        if (
            _before(r["effective_on"], r["announced_on"])
            and pdate_ok(r["effective_on"])
            and pdate_ok(r["announced_on"])
        ):
            gap = dt.date.fromisoformat(pdate_lo(r["announced_on"])) - dt.date.fromisoformat(
                pdate_hi(r["effective_on"])
            )
            if gap.days > 730:
                rep.warn(f"org_events {eid}: announced_on {gap.days} days after effective_on")
        ps = parts.get(eid, [])
        need, allowed = EVENT_ROLES.get(r["event_type"], (set(), set()))
        got = {p["role"] for p in ps}
        if not ps:
            rep.err(f"org_events {eid}: no participants")
        if need and not need <= got:
            rep.err(f"org_events {eid}: {r['event_type']} needs roles {sorted(need)} (has {sorted(got)})")
        if allowed and not got <= allowed:
            rep.err(f"org_events {eid}: roles {sorted(got - allowed)} not allowed for {r['event_type']}")
        eff = r["effective_on"] or r["announced_on"]
        for p in ps:
            o = orgs.get(p["org_id"])
            if not o or not eff:
                continue
            if _before(eff, o["founded_on"]):
                rep.err(f"org_events {eid}: participant {p['org_id']} founded {o['founded_on']} after event {eff}")
            if _before(o["dissolved_on"], eff):
                msg = f"org_events {eid}: {p['org_id']} ({p['role']}) dissolved {o['dissolved_on']} before event {eff}"
                (rep.err if p["role"] in ("acquirer", "successor", "resulting", "spun_off") else rep.warn)(msg)


def _source_rules(t: dict[str, list[dict[str, str]]], rep: Report) -> None:
    src = {r["source_id"]: r for r in t["sources"]}
    for sid, r in src.items():
        if not sid.startswith(r["corpus"] + ":"):
            rep.err(f"sources {sid}: prefix does not match corpus {r['corpus']}")
        if r["same_as"]:
            tgt = src.get(r["same_as"])
            if r["same_as"] == sid:
                rep.err(f"sources {sid}: same_as itself")
            elif tgt and tgt["same_as"]:
                rep.err(f"sources {sid}: same_as {r['same_as']} which is itself a duplicate (chain)")
        if r["year"] and r["published_on"] and r["published_on"][:4] != r["year"]:
            rep.warn(f"sources {sid}: year {r['year']} vs published_on {r['published_on']}")
        if r["corpus"] in ("web", "lin") and not r["evidence_grade"]:
            rep.err(f"sources {sid}: web/lin source needs evidence_grade")
        if r["corpus"] in ("web", "lin") and not r["url"]:
            rep.err(f"sources {sid}: web/lin source needs url")
        if r["corpus"] in RESTRICTED_CORPORA and r["redistribution"] != "restricted_local_only":
            rep.err(f"sources {sid}: {r['corpus']} sources are restricted_local_only (D4, D23)")
    dois = Counter(r["doi"].lower() for r in src.values() if r["doi"] and not r["same_as"])
    for d, n in dois.items():
        if n > 1:
            rep.err(f"sources: doi {d} on {n} canonical rows (set same_as on duplicates)")


def _crosswalk_rules(t: dict[str, list[dict[str, str]]], full: dict[str, list[dict[str, str]]], rep: Report) -> None:
    orgs = {r["org_id"]: r for r in full["organizations"]}
    alias_keys: dict[str, set[tuple[str, str]]] = defaultdict(set)  # org_id -> {(key, scope)}
    for a in full["org_aliases"]:
        for sc in split_list(a["scope"]) or ["*"]:
            alias_keys[a["org_id"]].add((norm_key(a["alias"]), sc))
    rows_by: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    for i, r in enumerate(t["org_crosswalk"], start=2):
        ids = split_list(r["org_ids"])
        basis, corpus = r["match_basis"], r["corpus"]
        if (basis == "unmapped") != (not ids):
            rep.err(f"org_crosswalk line {i}: match_basis {basis} inconsistent with org_ids {r['org_ids']!r}")
        n = int(r["n_rows"])
        rows_by[corpus][0] += n
        rows_by[corpus][1] += n if ids else 0
        if corpus in ("eo", "pk", "lin") and not ids:
            rep.err(f"org_crosswalk line {i}: {corpus} string {r['printed']!r} unmapped (P0 acceptance)")
        k = norm_key(r["printed"])
        if basis == "name":
            if corpus == "lin":
                continue
            o = orgs.get(ids[0]) if len(ids) == 1 else None
            if o is None or o["no_name_match"] == "true" or norm_key(o["name"]) != k:
                rep.err(f"org_crosswalk line {i}: name match {r['printed']!r} -> {r['org_ids']} is stale")
        elif basis == "alias":
            for oid in ids:
                if (k, corpus) not in alias_keys[oid] and (k, "*") not in alias_keys[oid]:
                    rep.err(f"org_crosswalk line {i}: alias match {r['printed']!r} -> {oid} has no alias row (stale)")
    tot, mapped = rows_by.get("ofc2026", [0, 0])
    if tot and mapped / tot < 0.90:
        rep.err(f"org_crosswalk: OFC 2026 author-row coverage {mapped / tot:.4f} < 0.90 (P0 acceptance)")


# ITU-T G.Sup39 / ISO 20473 bands (EO convention (l)); lower edge inclusive, nm.
BAND_EDGES_NM = [
    ("uv", 0.0, 380.0),
    ("visible", 380.0, 780.0),
    ("nir_below_o", 780.0, 1260.0),
    ("o_band", 1260.0, 1360.0),
    ("e_band", 1360.0, 1460.0),
    ("s_band", 1460.0, 1530.0),
    ("c_band", 1530.0, 1565.0),
    ("l_band", 1565.0, 1625.0),
    ("u_band", 1625.0, 1675.0),
    ("nir_above_u", 1675.0, 3000.0),
    ("mid_ir", 3000.0, 50000.0),
]


def band_for(nm: float) -> str:
    for name, lo, hi in BAND_EDGES_NM:
        if lo <= nm < hi:
            return name
    return "other"


def _component_rules(t: dict[str, list[dict[str, str]]], full: dict[str, list[dict[str, str]]], rep: Report) -> None:
    if not full["components"] and not full["component_metrics"]:
        return
    reg = load_parameters()
    classes: dict[str, dict[str, Any]] = reg["classes"]
    params: dict[str, dict[str, Any]] = reg["parameters"]
    src = {r["source_id"]: r for r in full["sources"]}
    comps = {r["component_id"]: r for r in full["components"]}
    layouts = (load_layouts() or {}).get("templates", {})
    for r in t.get("component_showcase", []):
        tpl = layouts.get(r["template"])
        c = comps.get(r["component_id"])
        if tpl is None:
            rep.err(f"component_showcase {r['component_id']}: unknown template {r['template']!r}")
        elif c is not None and c["class"] not in tpl["applies_to"]:
            rep.err(
                f"component_showcase {r['component_id']}: class {c['class']} not served by template {r['template']}"
            )
    for r in t["components"]:
        cid = r["component_id"]
        top, _, sub = r["class"].partition(".")
        if top not in classes or (sub and sub not in classes[top]["subtypes"]) or not sub:
            rep.err(f"components {cid}: class {r['class']!r} not class.subtype in component_parameters.yaml")
        s = src.get(r["source_id"])
        native = s["native_id"] if s else ""
        for h in split_list(r["host_device_ids"]):
            if not (s and s["corpus"] == "eo" and h.startswith(native + "-")):
                rep.err(f"components {cid}: host device {h!r} is not an EO device of {r['source_id']}")
    perf: dict[str, int] = defaultdict(int)
    for m in full["component_metrics"]:
        if params.get(m["parameter"], {}).get("kind") == "performance":
            perf[m["component_id"]] += 1
    for r in t["components"]:
        if not perf[r["component_id"]]:
            rep.err(f"components {r['component_id']}: no performance metric (geometry-only components are not rows)")
    seen: dict[tuple[str, ...], str] = {}
    for r in t["component_metrics"]:
        mid, cid = r["metric_id"], r["component_id"]
        if not mid.startswith(cid + "-m"):
            rep.err(f"component_metrics {mid}: id does not start with its component_id")
        c = comps.get(cid)
        p = params.get(r["parameter"])
        if p is None:
            rep.err(f"component_metrics {mid}: unknown parameter {r['parameter']!r}")
            continue
        if r["unit"] != str(p["unit"]):
            rep.err(f"component_metrics {mid}: unit {r['unit']!r} != {p['unit']!r} for {r['parameter']}")
        top = c["class"].partition(".")[0] if c else ""
        if c and p["classes"] != "*" and top not in p["classes"]:
            rep.err(f"component_metrics {mid}: parameter {r['parameter']} not allowed for class {c['class']}")
        if p.get("scope") == "required" and not r["scope"]:
            rep.err(f"component_metrics {mid}: {r['parameter']} needs scope")
        for cond in p.get("conditions") or []:
            if cond == "wavelength" and not (r["wavelength_nm"] or r["band"]):
                rep.err(f"component_metrics {mid}: {r['parameter']} needs wavelength_nm or band")
            if cond == "bias" and not r["bias_v"]:
                rep.err(f"component_metrics {mid}: {r['parameter']} needs bias_v")
        if r["band"] == "unspecified" and not r["notes"]:
            rep.err(f"component_metrics {mid}: band unspecified needs a note")
        if r["value_max"] and float(r["value_max"]) < float(r["value"]):
            rep.err(f"component_metrics {mid}: value_max < value")
        if r["wavelength_max_nm"] and (
            not r["wavelength_nm"] or float(r["wavelength_max_nm"]) < float(r["wavelength_nm"])
        ):
            rep.err(f"component_metrics {mid}: wavelength_max_nm needs a smaller wavelength_nm")
        if r["wavelength_nm"] and r["band"] and not r["wavelength_max_nm"]:
            if r["band"] != band_for(float(r["wavelength_nm"])) and r["band"] != "cl_band":
                rep.err(
                    f"component_metrics {mid}: band {r['band']} != {band_for(float(r['wavelength_nm']))} for {r['wavelength_nm']} nm"
                )
        s = src.get(c["source_id"]) if c else None
        if s and s["corpus"] == "eo" and not re.match(r"^p\.[0-9]+", r["locator"]):
            rep.err(f"component_metrics {mid}: eo: locator must start with p.N (EO text.md page)")
        if s and s["corpus"] == "ofc2026" and not re.match(r"^(p\.~[0-9]+|pNA)", r["locator"]):
            rep.err(f"component_metrics {mid}: ofc2026 locator must start with p.~N or pNA (approximate page, D4)")
        key = tuple(
            r[k]
            for k in (
                "component_id",
                "parameter",
                "value",
                "value_max",
                "wavelength_nm",
                "wavelength_max_nm",
                "band",
                "polarization",
                "temperature_k",
                "bias_v",
                "scope",
                "statistic",
                "condition",
                "basis",
            )
        )
        if key in seen:
            rep.warn(f"component_metrics {mid}: same value/conditions as {seen[key]}")
        seen[key] = mid
