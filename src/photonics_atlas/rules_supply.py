"""Supply-chain table rules (DevLog-003 D51-D60), called by validate.py as a tranche module.

Checks: category tree well-formed (ids, parents = id prefix); every category id used exists; top-level ids carry a
note; role -> allowed top-level categories (D54), facility_use only for registry facilities; product id = vendor slug,
usage rows bound to their product's org and category; deterministic ids (usage, process, standard, test); locator form
vs extraction and basis (D55); atlas anchors point at the source's own record and an allowed column; short facts
without quotation marks for restricted sources (D53); spec value and datasheet rules; process broker / wafer size
sanity; standards without revision letters, cited designations present in the printed string (D59); test anchors
(metric of the row's source and test vehicle), temperature / humidity ranges and the parsed-field-per-test-type table
(D60). Id helpers and the D60 type sets are shared with scripts/build_supply_seed.py.
"""

from __future__ import annotations

import datetime as dt
import re
from collections import Counter
from pathlib import Path
from typing import Any, Protocol

import yaml

from .csvio import split_list
from .paths import ROOT

CATEGORIES = ROOT / "data" / "schema" / "supply_categories.yaml"
CATEGORY_ID = re.compile(r"^[A-K]([0-9]+(\.[0-9]+)?)?$")
PAGE = re.compile(r"^(p\.~?[0-9]+|pNA)")
EO_PAGE = re.compile(r"^p\.[0-9]+")
OFC_PAGE = re.compile(r"^(p\.~[0-9]+|pNA)")
ATLAS_CORPORA = {"eo", "pk"}
# D54: role -> allowed top-level categories.
ROLE_TOPS: dict[str, set[str]] = {
    "fabrication": {"B"},
    "facility_use": {"B"},
    "mpw_access": {"B"},
    "post_processing": {"B"},
    "wafer_supply": {"A", "B"},
    "material_supply": {"A", "E"},
    "fab_tool": {"G"},
    "test_instrument": {"H"},
    "packaging_material": {"E"},
    "assembly_tool": {"F"},
    "fiber_component": {"D"},
    "laser_source": {"C", "H"},
    "software": {"J"},
    "standard_reference": {"I", "K"},
}
STATED_SPEC_MAX = 120
WAFER_MM = {50, 75, 100, 150, 200, 300, 450}
QUOTES = ('"', "\u201c", "\u201d", "\u2018", "\u2019")
# D55: atlas anchors of imported rows: corpus -> table -> file -> allowed column.
ANCHOR_COLUMNS: dict[str, dict[str, dict[str, set[str]]]] = {
    "product_usage": {"eo": {"papers.csv": {"foundry_or_fab", "wafer_supplier"}}},
    "foundry_processes": {"eo": {"papers.csv": {"process_name"}}},
}
ANCHOR = re.compile(r"^(?P<corpus>[a-z]+)-atlas:(?P<file>[a-z_]+\.csv)#(?P<id>[^/\s]+)(?:/(?P<col>[a-z_]+))?$")
# D60 parsed-field-per-test-type table (amended 2026-10-20): t_min_c / t_max_c only for cycling / shock; rh_pct only
# for humidity tests and preconditioning; temp_c for storage and humidity tests, and for preconditioning only as the
# temperature of a temperature / RH soak pair (never a reflow peak).
RANGE_T_TYPES = {"temperature_cycling", "thermal_shock"}
HUMID_TYPES = {"damp_heat", "temp_humidity_bias", "hast", "uhast", "msl_preconditioning"}
SINGLE_T_TYPES = {"high_temp_storage", "low_temp_storage", *(HUMID_TYPES - {"msl_preconditioning"})}
# D59: standard ids are designation level; a trailing revision letter after the number is not part of them.
REVISION_LETTER = re.compile(r"[0-9][A-Za-z](\.[0-9]+)?$")  # JESD47K, JESD22-A118B.01
# D54 (am. round 2): imported usage rows: role -> EO column it may come from.
ROLE_ANCHOR_COLUMNS: dict[str, set[str]] = {
    "fabrication": {"foundry_or_fab"},
    "facility_use": {"foundry_or_fab"},
    "mpw_access": {"foundry_or_fab"},
    "post_processing": {"foundry_or_fab", "wafer_supplier"},
    "wafer_supply": {"wafer_supplier"},
    "material_supply": {"wafer_supplier"},
}
# D54 (am. round 2): role -> allowed subcategories (top-level A stays allowed when no subcategory is stated, D52).
ROLE_SUBCATEGORY = {
    "wafer_supply": re.compile(r"^(A|A[1-3](\.[0-9]+)?|A[67](\.[0-9]+)?|B2(\.[0-9]+)?)$"),
    "material_supply": re.compile(r"^(A|A[45](\.[0-9]+)?|E[0-9.]*)$"),
}
# D60: measurement test types (test_type of rows with no stress); their measurand is the same type or empty.
MEASUREMENT_TYPES = {"optical_loss", "die_shear", "adhesion", "thermal_resistance", "warpage", "leak"}
HUMIDITY_WORDS = re.compile(r"damp heat|humid|%\s*RH|\bRH\b|\bDH\b|85\s*°?\s*C?\s*/\s*85", re.I)
NUMBER = re.compile(r"-?[0-9]+(?:\.[0-9]+)?")
RT_TEXT_COLUMNS = ("parameter", "variant", "condition", "standard_printed", "value_text", "pass_criterion", "scope")


class _Report(Protocol):
    def err(self, msg: str) -> None: ...

    def warn(self, msg: str) -> None: ...


Rows = list[dict[str, str]]


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def usage_id(source_id: str, org_id: str, role: str, product_id: str = "") -> str:
    base = f"use_{slug(source_id)}_{org_id.removeprefix('org_')}_{role}"
    return base + (f"_{slug(product_id.removeprefix('product_'))}" if product_id else "")


def process_id(org_id: str, source_id: str) -> str:
    return f"proc_{org_id.removeprefix('org_')}_{slug(source_id)}"


def standard_id(designation: str) -> str:
    return f"std_{slug(designation)}"


def test_id(corpus: str, native_id: str) -> str:
    return f"rt_{slug(corpus)}_{slug(native_id)}"


def atlas_anchor(corpus: str, file: str, row_id: str, column: str = "") -> str:
    return f"{corpus}-atlas:{file}#{row_id}" + (f"/{column}" if column else "")


def norm_designation(s: str) -> str:
    """Case- and separator-insensitive form used to find a designation in a printed standard string (D59)."""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def load_categories(path: Path | None = None) -> dict[str, dict[str, Any]]:
    with (path or CATEGORIES).open() as f:
        data: dict[str, Any] = yaml.safe_load(f)
    return {str(c["id"]): c for c in data.get("categories") or []}


def tree_errors(path: Path | None = None) -> list[str]:
    with (path or CATEGORIES).open() as f:
        data: dict[str, Any] = yaml.safe_load(f)
    cats = data.get("categories") or []
    out: list[str] = []
    ids = Counter(str(c.get("id", "")) for c in cats)
    for k, n in ids.items():
        if n > 1:
            out.append(f"supply_categories: duplicate id {k!r}")
    known = set(ids)
    for c in cats:
        cid, parent = str(c.get("id", "")), str(c.get("parent") or "")
        if not CATEGORY_ID.match(cid):
            out.append(f"supply_categories: bad id {cid!r}")
            continue
        if not c.get("label"):
            out.append(f"supply_categories {cid}: no label")
        want = "" if len(cid) == 1 else (cid.rsplit(".", 1)[0] if "." in cid else cid[0])
        if parent != want:
            out.append(f"supply_categories {cid}: parent {parent!r} != id prefix {want!r}")
        elif parent and parent not in known:
            out.append(f"supply_categories {cid}: parent {parent!r} not defined")
    return out


def _category(table: str, rid: str, r: dict[str, str], cats: dict[str, dict[str, Any]], rep: _Report) -> None:
    cid = r["category_id"]
    if cid not in cats:
        rep.err(f"{table} {rid}: category_id {cid!r} not in supply_categories.yaml")
    elif len(cid) == 1 and not r.get("notes"):
        rep.warn(f"{table} {rid}: top-level category {cid} without a note (subcategory not stated?)")


def _evidence(table: str, rid: str, r: dict[str, str], corpus: str, native: str, rep: _Report) -> None:
    """D55: locator form vs extraction / basis and the source's corpus; atlas anchors name the source's own record
    (native id) and a column allowed for the table."""
    loc, ext = r["locator"], r["extraction"]
    if ext == "atlas_import":
        if r["basis"] != "stated":
            rep.err(f"{table} {rid}: atlas_import rows have basis stated")
        if corpus not in ATLAS_CORPORA or not loc.startswith(f"{corpus}-atlas:"):
            rep.err(f"{table} {rid}: atlas_import locator must be a {corpus}-atlas: anchor of the source's own atlas")
            return
        m = ANCHOR.match(loc)
        allowed = ANCHOR_COLUMNS.get(table, {}).get(corpus, {})
        if not m:
            rep.err(f"{table} {rid}: atlas anchor {loc!r} is not <corpus>-atlas:<file>.csv#<id>/<column>")
        elif m["id"] != native:
            rep.err(f"{table} {rid}: atlas anchor id {m['id']!r} != source native_id {native!r}")
        elif m["file"] not in allowed or m["col"] not in allowed[m["file"]]:
            ok = sorted(f"{f}/{c}" for f, cs in allowed.items() for c in cs)
            rep.err(f"{table} {rid}: atlas anchor {m['file']}/{m['col']} not allowed for {table} (allowed: {ok})")
    elif not PAGE.match(loc):
        rep.err(f"{table} {rid}: {ext} rows need a page locator (p.N / p.~N / pNA)")
    elif corpus == "eo" and not EO_PAGE.match(loc):
        rep.err(f"{table} {rid}: eo: page locators are p.N (EO text.md page)")
    elif corpus == "ofc2026" and not OFC_PAGE.match(loc):
        rep.err(f"{table} {rid}: ofc2026 page locators are p.~N or pNA (D4)")


def rules(ok: dict[str, Rows], full: dict[str, Rows], rep: _Report) -> None:
    if "products" not in full:  # supply schema not loaded
        return
    for e in tree_errors():
        rep.err(e)
    cats = load_categories()
    orgs = {r["org_id"]: r for r in full.get("organizations", [])}
    src = {r["source_id"]: r for r in full.get("sources", [])}
    products = {r["product_id"]: r for r in full.get("products", [])}

    def corpus_of(sid: str) -> str:
        return src[sid]["corpus"] if sid in src else ""

    def native_of(sid: str) -> str:
        return src[sid]["native_id"] if sid in src else ""

    def restricted(sid: str) -> bool:
        return sid in src and src[sid]["redistribution"] == "restricted_local_only"

    for r in ok.get("products", []):
        pid, oid = r["product_id"], r["org_id"]
        _category("products", pid, r, cats, rep)
        if not pid.startswith(f"product_{oid.removeprefix('org_')}-"):
            rep.err(f"products {pid}: id must start with product_{oid.removeprefix('org_')}- (vendor slug, D8)")
        ds = r["datasheet_source_id"]
        if ds and corpus_of(ds) not in ("ds", ""):
            rep.err(f"products {pid}: datasheet_source_id {ds} is not a ds: source")

    today = dt.date.today().isoformat()
    for table in ("products", "product_usage", "product_specs", "foundry_processes"):
        for r in ok.get(table, []):
            if r.get("verified_on", "") > today:
                rep.err(f"{table} {next(iter(r.values()))}: verified_on {r['verified_on']} is in the future")

    seen: Counter[tuple[str, str, str, str]] = Counter()
    fab_pairs: set[tuple[str, str]] = set()
    b2_rows: list[tuple[str, str, str]] = []
    for r in ok.get("product_usage", []):
        uid, role, oid, pid, sid = r["usage_id"], r["role"], r["org_id"], r["product_id"], r["source_id"]
        seen[(sid, oid, role, pid)] += 1
        _category("product_usage", uid, r, cats, rep)
        if uid != usage_id(sid, oid, role, pid):
            rep.err(f"product_usage {uid}: id must be {usage_id(sid, oid, role, pid)} (D53)")
        top = r["category_id"][:1]
        if top not in ROLE_TOPS[role]:
            rep.err(f"product_usage {uid}: role {role} does not allow category {r['category_id']} (D54)")
        if role == "facility_use":
            if r["category_id"] != "B7":
                rep.err(f"product_usage {uid}: facility_use rows are category B7")
            if oid in orgs and orgs[oid]["org_type"] != "facility":
                rep.err(f"product_usage {uid}: facility_use org {oid} is not typed facility in the registry")
        elif r["category_id"] == "B7":
            rep.err(f"product_usage {uid}: category B7 (shared cleanroom) needs role facility_use")
        elif top == "B" and oid in orgs and orgs[oid]["org_type"] == "facility":
            rep.err(f"product_usage {uid}: org {oid} is typed facility: B-category rows are facility_use / B7 (D54)")
        sub = ROLE_SUBCATEGORY.get(role)
        if sub and not sub.match(r["category_id"]):
            rep.err(f"product_usage {uid}: {role} does not allow subcategory {r['category_id']} (D54)")
        if role == "fabrication":
            fab_pairs.add((sid, oid))
        elif role == "wafer_supply" and r["category_id"].startswith("B2"):
            b2_rows.append((uid, sid, oid))
        am = ANCHOR.match(r["locator"]) if r["extraction"] == "atlas_import" else None
        if am and am["col"] and role in ROLE_ANCHOR_COLUMNS and am["col"] not in ROLE_ANCHOR_COLUMNS[role]:
            rep.err(f"product_usage {uid}: role {role} cannot come from EO column {am['col']} (D54)")
        p = products.get(pid)
        if p:
            if p["org_id"] != oid:
                rep.err(f"product_usage {uid}: org {oid} != product {pid} org {p['org_id']}")
            if p["category_id"] != r["category_id"]:
                rep.err(f"product_usage {uid}: category {r['category_id']} != product category {p['category_id']}")
        if (r["basis"] == "inferred_from_model" or r["extraction"] == "auto_regex") and not pid:
            rep.err(f"product_usage {uid}: {r['basis']}/{r['extraction']} needs a product_id")
        _evidence("product_usage", uid, r, corpus_of(sid), native_of(sid), rep)
        spec = r["stated_spec"]
        if len(spec) > STATED_SPEC_MAX:
            rep.err(f"product_usage {uid}: stated_spec longer than {STATED_SPEC_MAX} chars (facts only, D53)")
        if restricted(sid) and any(q in spec + r["notes"] for q in QUOTES):
            rep.err(f"product_usage {uid}: quotation marks in a restricted source's row (no verbatim text, D53)")
    for k, n in seen.items():
        if n > 1:
            rep.err(f"product_usage: {n} rows for (source, org, role, product) {k}")
    for uid, sid, oid in b2_rows:
        if (sid, oid) in fab_pairs:
            rep.err(f"product_usage {uid}: {oid} also fabricated for {sid}: B2 wafers from the fab are one fact (D57)")

    for r in ok.get("product_specs", []):
        sp, pid = r["spec_id"], r["product_id"]
        if not re.match(rf"^{re.escape(pid)}-s[0-9]+$", sp):
            rep.err(f"product_specs {sp}: id must be {pid}-s<N>")
        if not r["value"] and not r["value_text"]:
            rep.err(f"product_specs {sp}: value or value_text required")
        if r["value_max"] and (not r["value"] or float(r["value_max"]) < float(r["value"])):
            rep.err(f"product_specs {sp}: value_max needs a smaller value")
        if r["basis"].startswith("datasheet_") and corpus_of(r["source_id"]) != "ds":
            rep.err(f"product_specs {sp}: basis {r['basis']} needs a ds: source")
        if restricted(r["source_id"]) and any(q in r["value_text"] + r["notes"] for q in QUOTES):
            rep.err(f"product_specs {sp}: quotation marks in a restricted source's row (D53)")

    for r in ok.get("foundry_processes", []):
        prid, oid, sid = r["process_id"], r["org_id"], r["source_id"]
        if prid != process_id(oid, sid):
            rep.err(f"foundry_processes {prid}: id must be {process_id(oid, sid)} (D58)")
        if r["broker_org_id"] == oid:
            rep.err(f"foundry_processes {prid}: broker_org_id is the foundry itself")
        if r["broker_org_id"] and r["access_route"] != "mpw_via_broker":
            rep.err(f"foundry_processes {prid}: broker_org_id needs access_route mpw_via_broker")
        if r["wafer_mm"] and int(r["wafer_mm"]) not in WAFER_MM:
            rep.warn(f"foundry_processes {prid}: unusual wafer_mm {r['wafer_mm']}")
        if r["pdk_open"] == "true" and not r["pdk_name"]:
            rep.err(f"foundry_processes {prid}: pdk_open without pdk_name")
        _evidence("foundry_processes", prid, r, corpus_of(sid), native_of(sid), rep)

    designations = {r["standard_id"]: r["designation"] for r in full.get("standards", [])}
    for r in ok.get("standards", []):
        if r["standard_id"] != standard_id(r["designation"]):
            rep.err(f"standards {r['standard_id']}: id must be {standard_id(r['designation'])} (D59)")
        if REVISION_LETTER.search(r["designation"]):
            rep.err(f"standards {r['standard_id']}: designation {r['designation']!r} ends in a revision letter (D59)")

    for r in ok.get("reliability_tests", []):
        tid, sid = r["test_id"], r["source_id"]
        corpus = corpus_of(sid)
        if corpus and not tid.startswith(f"rt_{slug(corpus)}_"):
            rep.err(f"reliability_tests {tid}: id must start with rt_{slug(corpus)}_ (D60)")
        ttype = r["test_type"]
        if (r["t_min_c"] or r["t_max_c"]) and ttype not in RANGE_T_TYPES:
            rep.err(f"reliability_tests {tid}: t_min_c / t_max_c only for {sorted(RANGE_T_TYPES)}, not {ttype} (D60)")
        if r["rh_pct"] and ttype not in HUMID_TYPES:
            rep.err(f"reliability_tests {tid}: rh_pct only for {sorted(HUMID_TYPES)}, not {ttype} (D60)")
        if r["temp_c"] and ttype not in SINGLE_T_TYPES and not (ttype in HUMID_TYPES and r["rh_pct"]):
            rep.err(f"reliability_tests {tid}: temp_c not parsed for {ttype} (D60; precon only with its RH soak)")
        if ttype in MEASUREMENT_TYPES and r["measurand"] not in ("", ttype):
            rep.err(f"reliability_tests {tid}: measurement test_type {ttype} with measurand {r['measurand']} (D60)")
        if r["qualifier"] and not r["value"]:
            rep.err(f"reliability_tests {tid}: qualifier {r['qualifier']} without a value")
        if ttype == "damp_heat" and not HUMIDITY_WORDS.search(" ".join((r["parameter"], r["variant"], r["condition"]))):
            rep.err(f"reliability_tests {tid}: damp_heat without a humidity keyword in parameter / variant / condition")
        nums = {float(x) for x in NUMBER.findall(r["condition"])}
        for col in ("t_min_c", "t_max_c", "temp_c", "rh_pct"):
            if r[col] and float(r[col]) not in nums and -float(r[col]) not in nums:
                rep.err(f"reliability_tests {tid}: {col} {r[col]} does not occur in the condition text (D60)")
        if restricted(sid) and any(q in r[c] for c in (*RT_TEXT_COLUMNS, "notes") for q in QUOTES):
            rep.err(f"reliability_tests {tid}: quotation marks in a restricted source's row (no verbatim text, D53)")
        printed = norm_designation(r["standard_printed"])
        for st in split_list(r["standard_ids"]):
            des = designations.get(st)
            if des is not None and norm_designation(des) not in printed:
                rep.err(f"reliability_tests {tid}: designation {des!r} ({st}) not in standard_printed (D59)")
        lo, hi = r["t_min_c"], r["t_max_c"]
        if lo and hi and float(lo) > float(hi):
            rep.err(f"reliability_tests {tid}: t_min_c > t_max_c")
        for col, a, b in (("t_min_c", -273.15, 1000.0), ("t_max_c", -273.15, 1000.0), ("temp_c", -273.15, 1000.0)):
            if r[col] and not a <= float(r[col]) <= b:
                rep.err(f"reliability_tests {tid}: {col} {r[col]} out of range")
        if r["rh_pct"] and not 0 <= float(r["rh_pct"]) <= 100:
            rep.err(f"reliability_tests {tid}: rh_pct {r['rh_pct']} outside 0..100")
        ref = r["atlas_ref"]
        if corpus in ATLAS_CORPORA and not ref:
            rep.err(f"reliability_tests {tid}: {corpus} rows need atlas_ref (D60)")
        if ref and not ref.startswith(f"{corpus}-atlas:"):
            rep.err(f"reliability_tests {tid}: atlas_ref {ref!r} is not an anchor of the source's atlas")
        elif ref and corpus == "pk":
            m = ANCHOR.match(ref)
            native, tv = native_of(sid), r["tv_ref"]
            if not m or m["file"] != "metrics.csv" or m["col"]:
                rep.err(f"reliability_tests {tid}: pk atlas_ref must be pk-atlas:metrics.csv#<metric_id> (D60)")
            else:
                mid = m["id"]
                if tid != test_id(corpus, mid):
                    rep.err(f"reliability_tests {tid}: id must be {test_id(corpus, mid)} (from atlas_ref, D60)")
                if not tv.startswith(f"{native}-") or not mid.startswith(f"{tv}-"):
                    rep.err(f"reliability_tests {tid}: metric {mid} is not of test vehicle {tv!r} of {sid} (D60)")
        if not r["value"] and not r["value_text"] and not r["result"]:
            rep.warn(f"reliability_tests {tid}: no value, value_text or result")
        if corpus == "eo" and not EO_PAGE.match(r["locator"]):
            rep.err(f"reliability_tests {tid}: eo: page locators are p.N")
        if corpus == "ofc2026" and not OFC_PAGE.match(r["locator"]):
            rep.err(f"reliability_tests {tid}: ofc2026 page locators are p.~N or pNA (D4)")
        if len(split_list(r["standard_ids"])) == 0 and not r["notes"]:
            rep.warn(f"reliability_tests {tid}: no parsed standard and no note")
