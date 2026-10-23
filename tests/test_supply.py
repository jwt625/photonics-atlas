"""P2 supply-chain tables (DevLog-003): real data, parser units, and one mutation per rules_supply rule on a temp copy."""

from __future__ import annotations

import importlib.util
import shutil
import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType

import pytest

from photonics_atlas import rules_supply
from photonics_atlas.csvio import read_csv, write_csv
from photonics_atlas.paths import ROOT
from photonics_atlas.schema import columns
from photonics_atlas.validate import validate

from .conftest import needs_inputs

Rows = list[dict[str, str]]
SUPPLY_TABLES = ("products", "product_usage", "product_specs", "foundry_processes", "standards", "reliability_tests")


def _seed() -> ModuleType:
    spec = importlib.util.spec_from_file_location("build_supply_seed", ROOT / "scripts" / "build_supply_seed.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["build_supply_seed"] = mod
    spec.loader.exec_module(mod)
    return mod


seed = _seed()


def _supply_errors(errors: list[str]) -> list[str]:
    keys = (*SUPPLY_TABLES, "supply_categories", "data/supply")
    return [e for e in errors if e.startswith(keys)]


# --------------------------------------------------------------------------- real data


def test_real_supply_tables_have_no_errors() -> None:
    rep = validate()
    assert _supply_errors(rep.errors) == []
    assert rep.counts["product_usage"] > 0 and rep.counts["reliability_tests"] > 0


def test_category_tree() -> None:
    assert rules_supply.tree_errors() == []
    cats = rules_supply.load_categories()
    assert set("ABCDEFGHIJK") <= set(cats)
    for cid in ("A2.4", "B7", "E8", "F9", "G7", "H17", "I3"):
        assert cid in cats
    assert cats["A2.1"]["parent"] == "A2" and cats["H17"]["parent"] == "H"


def test_usage_rows_are_atlas_imports_with_anchors() -> None:
    for r in read_csv(ROOT / "data" / "supply" / "product_usage.csv"):
        if r["extraction"] == "scan_review":  # merged scanner batches (D206) carry page locators instead
            assert r["locator"].startswith(("p.", "pNA"))
            continue
        assert r["extraction"] == "atlas_import" and r["basis"] == "stated"
        pid = r["source_id"].removeprefix("eo:")
        assert r["locator"] in (
            f"eo-atlas:papers.csv#{pid}/foundry_or_fab",
            f"eo-atlas:papers.csv#{pid}/wafer_supplier",
        )


@needs_inputs
def test_rebuild_reproduces_tables() -> None:
    """The seed script rebuilt from the inputs gives exactly the rows on disk (append-only data stays reproducible)."""
    import argparse

    import yaml

    from photonics_atlas.orgmatch import load_matcher

    cur = yaml.safe_load((ROOT / "data" / "supply" / "curation.yaml").read_text())
    orgs = {r["org_id"]: r for r in read_csv(ROOT / "data" / "registry" / "organizations.csv")}
    sources = {r["source_id"] for r in read_csv(ROOT / "data" / "registry" / "sources.csv")}
    m = load_matcher()
    args = argparse.Namespace(only=set(), limit=None)

    class _Log:
        def info(self, msg: str) -> None:
            pass

        def event(self, *a: object, **k: object) -> None:
            pass

    usage, procs, _ = seed.build_eo(m, cur, orgs, sources, args, _Log())
    stds, tests, _ = seed.build_pk(m, sources, args, _Log())
    for table, rows, key in (
        ("product_usage", usage, "usage_id"),
        ("foundry_processes", procs, "process_id"),
        ("standards", stds, "standard_id"),
        ("reliability_tests", tests, "test_id"),
    ):
        # merged scanner batches (extraction scan_review, D206 / D299) are not seed rows
        disk = {
            r[key]: r
            for r in read_csv(ROOT / "data" / "supply" / f"{table}.csv")
            if r.get("extraction") != "scan_review"
        }
        built = {r[key]: {c: r.get(c, "") for c in columns(table)} for r in rows}
        assert built == disk, table


@needs_inputs
def test_every_pk_test_standard_row_is_imported() -> None:
    from photonics_atlas.adapters import pk_metrics

    n = sum(1 for r in pk_metrics.metrics() if r.test_standard.strip())
    assert len(read_csv(ROOT / "data" / "supply" / "reliability_tests.csv")) == n


# --------------------------------------------------------------------------- parser units


def test_split_and_parse_wafer_parts() -> None:
    assert seed.split_top("LIGENTEC (SiN wafers); Lumiphase (BTO growth; integration)") == [
        "LIGENTEC (SiN wafers)",
        "Lumiphase (BTO growth; integration)",
    ]
    cands, qual = seed.parse_wafer_part("CrysTec GmbH (GdScO3 (110)o substrate)")
    assert cands == ["CrysTec GmbH"] and qual == "GdScO3 (110)o substrate"
    cands, _ = seed.parse_wafer_part("NanoLN, Jinan Jingzheng Electronics Co., Ltd. (LNOI)")
    assert cands == ["NanoLN, Jinan Jingzheng Electronics Co., Ltd.", "NanoLN"]
    assert seed.NO_SUPPLIER.search("customized TFLN wafer (supplier not named)")


def test_wafer_category_keywords() -> None:
    assert seed.wafer_category("x-cut 300 nm lithium tantalate on insulator NanoLN") == "A2.2"
    assert seed.wafer_category("x-cut LN-on-sapphire wafers") == "A2.3"
    assert seed.wafer_category("SOI substrates for BTO growth Soitec") == "A1"
    assert seed.wafer_category("BTO thin film, acknowledgements") == "A2.4"
    assert seed.wafer_category("6-inch CVD graphene") == "A5"
    assert seed.wafer_category("") == ""
    assert seed.platform_category({"lnoi_rib", "lnoi_loaded_sin"})[0] == "A2.1"
    assert seed.platform_category({"lnoi_rib", "ltoi_rib"}) == ("", "")
    assert seed.wafer_role("A4") == "material_supply" and seed.wafer_role("A2.1") == "wafer_supply"
    # D57 amended: growth / integration services are B5 post_processing; a service word in an org name is not
    assert seed.wafer_category("BTO growth and integration") == "B5" and seed.wafer_role("B5") == "post_processing"
    assert seed.wafer_category("Shanghai Novel Si Integration Technology", name=True) == ""
    # locator words leave stated_spec (audit #7)
    assert seed.split_locator_words("BTO thin film, acknowledgements") == ("BTO thin film", "acknowledgements")
    assert seed.split_locator_words("x-cut LN-on-sapphire wafers, 0.9 and 1.5 um films; as written in Methods") == (
        "x-cut LN-on-sapphire wafers, 0.9 and 1.5 um films",
        "as written in Methods",
    )
    assert seed.split_locator_words("GaAs wafers, per acknowledgements") == ("GaAs wafers", "per acknowledgements")
    assert seed.split_locator_words("x-cut LNOI wafer") == ("x-cut LNOI wafer", "")


def test_parse_standards() -> None:
    p = seed.parse_standards
    assert p("JESD22A-104F") == [("JESD22-A104", "JEDEC")]
    assert p("JESD47K (ref [2]); precon JESD22-A113D MSL4 (ref [3])") == [
        ("JESD22-A113", "JEDEC"),
        ("JESD47", "JEDEC"),
    ]
    assert p("AEC-Q100; AEC-Q104") == [("AEC-Q100", "AEC"), ("AEC-Q104", "AEC")]
    assert p("Mil-STD 883 method 2002 B (shock), 2026F (vibration)") == [("MIL-STD-883", "")]
    assert p("ISO 2409; ASTM D3359") == [("ASTM D3359", "ASTM"), ("ISO 2409", "ISO")]
    # Typos and ambiguous strings are not corrected (D59).
    for s in ("MIL Standard 833", "JEDEC ESD22-B111", "IPD/JEDEC-9704A", "MIL-STD-883-2 (as labelled)", "JEDEC"):
        assert p(s) == [], s


def test_classify_and_conditions() -> None:
    c = seed.classify_test
    pc = seed.parse_conditions
    assert c("unbiased HAST", "") == "uhast"
    assert c("biased HAST duration", "") == "hast"
    assert c("TC(B) after Pre-con L3 failures", "") == "temperature_cycling"
    assert c("thermal shock of singulated units", "") == "thermal_shock"
    assert c("shocks to first daisy-chain failure", "") == "mechanical_shock"
    assert c("IL shift after TC, DH, HTS, LTS", "") == "other"
    assert c("pass rate", "JEDEC uHAST") == "uhast"
    # D60 amended (audit #1, #11, #14, #15): condition before standard; precon clauses split off; stress vs measurand
    ts = "TS -55/125 C; precondition MSL Lv.3A: HTS 125 C x 24 h + THS 60 C/60% RH x 40 h + reflow 260 C x 3; 1000 cycles"
    assert c("pass rate", "MSL Lv.3A preconditioning", ts) == "thermal_shock"
    assert pc(ts, "thermal_shock") == {"t_min_c": "-55", "t_max_c": "125", "temp_c": "", "rh_pct": ""}
    assert c("preconditioning MSL", "JEDEC (as written)", "MSL4, reflow x3 at 260 C") == "msl_preconditioning"
    assert pc("MSL4, reflow x3 at 260 C", "msl_preconditioning")["temp_c"] == ""  # reflow peak is not a soak
    m10 = "125 C/24 h bake + 30 C/60%RH/192 h, then 260 C reflow x3"
    assert c("MSL3 preconditioning + reflow", "IPC/JEDEC J-STD-020", m10) == "msl_preconditioning"
    assert pc(m10, "msl_preconditioning") == {"t_min_c": "", "t_max_c": "", "temp_c": "30", "rh_pct": "60"}
    precon_tc = "Precon (multiple solder reflow, MSL4 soak) + TC condition C, -65 to 150 C"
    assert c("TCC temperature cycling", "", precon_tc) == "temperature_cycling"
    assert pc(precon_tc, "temperature_cycling")["t_min_c"] == "-65"
    assert c("HTS", "", "Precon (multiple solder reflow, MSL4 soak) + HTS 150 C") == "high_temp_storage"
    assert c("IL per facet", "JEDEC HTS", "HTS 150 C, 168 h, after 3x SAC reflow") == "high_temp_storage"
    assert seed.classify_measurand("IL per facet") == "optical_loss"
    assert c("die shear force", "MIL-STD-883", "2x2 mm die; TCB 250 C, 100 MPa, 15 s") == "die_shear"  # bonding
    assert c("He leak after multiple reflow", "", "reflow 3x 260 C") == "reflow"
    assert seed.classify_measurand("He leak after multiple reflow") == "leak"
    assert c("MST L3 + unbiased HAST", "", "") == "uhast"
    # round 2: stress named only in the PK variant; "before ..." variants are baselines; warpage along a reflow profile
    assert c("stiffener adhesive coverage (SAT)", "JESD22-A104F", "-55 to 125 C", "FCF with MCJ; TC/B 0 cycles") == (
        "temperature_cycling"
    )
    assert c("core refractive index", "JESD22-A103 (ref [7])", "150 C, 500 h", "after HTS 500 h") == "high_temp_storage"
    assert c("die shear force", "MIL-STD-883-2", "", "before UHAST") == "die_shear"
    assert c("daisy-chain conductivity after TCT", "", "TCT -55/125 C", "ball/paste LTS / LTS") == "temperature_cycling"
    assert (
        c("warpage vs JEDEC reflow flatness requirement", "JEDEC SPP-024 Issue A", "shadow moire 25-260 C") == "warpage"
    )
    assert c("package warpage", "JEDEC (reflow; number not given)", "JEDEC reflow profile, RT to 260 C") == "warpage"
    assert seed.classify_measurand("daisy chain continuity") == "electrical_resistance"
    assert pc("110 C / 85 %, 168 h", "uhast") == {"t_min_c": "", "t_max_c": "", "temp_c": "110", "rh_pct": "85"}
    assert pc("TC condition G, -40 to 125 C", "temperature_cycling")["t_min_c"] == "-40"
    assert pc("85 C / 85 %RH, 500 h", "damp_heat") == {"t_min_c": "", "t_max_c": "", "temp_c": "85", "rh_pct": "85"}
    # A preconditioning soak inside a storage or cycling row is not the row's stress (the precon clause is split off,
    # so the storage temperature itself is parsed, D60 amended).
    assert pc("150 C; Level-3 precon (30 C/60%RH/192 h + 260 C reflow x3)", "high_temp_storage")["temp_c"] == "150"
    assert pc("-55 to 125 C; precon (30 C/60%RH/192 h)", "temperature_cycling")["rh_pct"] == ""
    assert pc("UHAST 130 C / 85%RH / 96 h", "die_shear") == {"t_min_c": "", "t_max_c": "", "temp_c": "", "rh_pct": ""}


def test_audit_rows_on_disk() -> None:
    """Rows corrected by the 2026-10-20 audit stay corrected (DevLog-003 Audit corrections)."""
    rt = {r["test_id"]: r for r in read_csv(ROOT / "data" / "supply" / "reliability_tests.csv")}
    for k in range(1, 5):
        r = rt[f"rt_pk_001c_147203_b_m{k}"]
        assert (r["test_type"], r["t_min_c"], r["t_max_c"], r["temp_c"], r["rh_pct"]) == (
            "thermal_shock",
            "-55",
            "125",
            "",
            "",
        )
    assert rt["rt_pk_ectc51687_2025_00048_a_m14"]["temp_c"] == ""
    neg = rt["rt_pk_ectc51687_2025_00012_a_m1"]
    assert neg["value"] == "-2.46" and "sign as printed" in neg["scope"] and "D33" in neg["notes"]
    use = {r["usage_id"]: r for r in read_csv(ROOT / "data" / "supply" / "product_usage.csv")}
    kohli = {k for k in use if k.startswith("use_eo_kohli2025_")}
    assert kohli == {
        "use_eo_kohli2025_ligentec_fabrication",
        "use_eo_kohli2025_lumiphase_post_processing",
        "use_eo_kohli2025_binnig_and_rohrer_nanotechnology_center_facility_use",
    }
    assert not any("acknowledgements" in r["stated_spec"] for r in use.values())
    # round 2
    assert "use_eo_witmer2020_soluxra_material_supply" in use and "use_eo_witmer2020_soluxra_wafer_supply" not in use
    assert use["use_eo_chen2024_jinan_jingzheng_electronics_wafer_supply"]["category_id"] == "A2.1"
    assert rt["rt_pk_tcpmt_2026_3672227_a_m40"]["test_type"] == "temperature_cycling"
    assert rt["rt_pk_ectc51909_2023_00274_a_m1"]["test_type"] == "die_shear"
    assert rt["rt_pk_eptc67330_2025_11392108_a_m6"]["test_type"] == "warpage"
    assert rt["rt_pk_ectc51687_2025_00007_b_m2"]["rh_pct"] == "85"
    req = {(r["kind"], r["printed"]): r for r in read_csv(ROOT / "data" / "_staging" / "supply" / "org_requests.csv")}
    assert ("alias", "SIMIT-CAS") in req and ("wafer_supplier", "SIMIT-CAS") not in req
    assert (
        req[("alias", "SIMIT-CAS")]["alias_of_org_id"]
        == "org_shanghai_institute_of_microsystem_and_information_technology"
    )


def test_merge_table_replace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Append-only by default; --replace-ids replaces a rebuilt row or removes one the rebuild no longer produces."""
    monkeypatch.setattr(seed, "ROOT", tmp_path)
    cols = columns("standards")

    def row(sid: str, notes: str = "") -> dict[str, str]:
        return {c: "" for c in cols} | {"standard_id": sid, "designation": sid, "access": "unknown", "notes": notes}

    path = tmp_path / "data" / "supply" / "standards.csv"
    write_csv(path, cols, [row("a"), row("b"), row("c"), row("d")])
    events: list[tuple[str, str]] = []

    class _Log:
        def info(self, msg: str) -> None:
            pass

        def event(self, step: str, status: str = "ok", **k: object) -> None:
            events.append((step, str(k.get("id", ""))))

    new = [row("a", "changed"), row("b", "changed"), row("c"), row("e")]
    seed.merge_table("standards", new, "standard_id", False, _Log(), {"a", "d"}, True)
    got = {r["standard_id"]: r["notes"] for r in read_csv(path)}
    assert got == {"a": "changed", "b": "", "c": "", "e": ""}  # a replaced, b kept (differs), d removed, e appended
    assert ("replaced", "a") in events and ("differs", "b") in events and ("removed", "d") in events


def test_ids() -> None:
    assert rules_supply.usage_id("eo:johnson2025", "org_amf", "fabrication") == "use_eo_johnson2025_amf_fabrication"
    assert rules_supply.process_id("org_amf", "eo:johnson2025") == "proc_amf_eo_johnson2025"
    assert rules_supply.standard_id("IEC 61300-3-4") == "std_iec_61300_3_4"
    assert rules_supply.test_id("pk", "ectc32696.2021.00125-a-m1") == "rt_pk_ectc32696_2021_00125_a_m1"


# --------------------------------------------------------------------------- mutations


@pytest.fixture()
def reg(tmp_path: Path) -> Path:
    for d in ("data/registry", "data/crosswalk", "data/supply"):
        shutil.copytree(ROOT / d, tmp_path / d)
    return tmp_path


def _edit(root: Path, table: str, fn: Callable[[Rows], None]) -> None:
    path = root / "data" / "supply" / f"{table}.csv"
    rows = read_csv(path)
    fn(rows)
    write_csv(path, columns(table), rows)


def _row(rows: Rows, **match: str) -> dict[str, str]:
    return next(r for r in rows if all(r[k] == v for k, v in match.items()))


def _errs(root: Path) -> list[str]:
    return _supply_errors(validate(root).errors)


def _has(root: Path, text: str) -> bool:
    return any(text in e for e in _errs(root))


def test_mutation_unknown_category(reg: Path) -> None:
    _edit(reg, "product_usage", lambda rows: rows[0].update(category_id="B9"))
    assert _has(reg, "not in supply_categories.yaml")


def test_mutation_role_category(reg: Path) -> None:
    def bad(rows: Rows) -> None:
        _row(rows, role="facility_use").update(category_id="B1")
        _row(rows, role="fabrication", category_id="B1").update(category_id="B7")
        _row(rows, role="wafer_supply").update(category_id="H5")

    _edit(reg, "product_usage", bad)
    assert _has(reg, "facility_use rows are category B7")
    assert _has(reg, "needs role facility_use")
    assert _has(reg, "does not allow category H5")


def test_mutation_facility_org_type(reg: Path) -> None:
    _edit(
        reg, "product_usage", lambda rows: _row(rows, role="fabrication", org_id="org_amf").update(role="facility_use")
    )
    errs = _errs(reg)
    assert any("not typed facility" in e for e in errs)
    assert any("id must be" in e for e in errs)  # role is part of the deterministic id


def test_mutation_evidence_consistency(reg: Path) -> None:
    def bad(rows: Rows) -> None:
        rows[0].update(locator="p.3 Methods")  # atlas_import with a page locator
        rows[1].update(extraction="manual")  # manual with an atlas anchor
        rows[2].update(basis="inferred_from_model")  # no product_id
        rows[3].update(locator="eo-atlas:papers.csv#x/foundry_or_fab", source_id="pk:ectc32696.2021.00125")

    _edit(reg, "product_usage", bad)
    errs = _errs(reg)
    assert any("atlas_import locator must be" in e for e in errs)
    assert any("need a page locator" in e for e in errs)
    assert any("needs a product_id" in e for e in errs)
    assert any("atlas_import rows have basis stated" in e for e in errs)


def test_mutation_locator_pattern(reg: Path) -> None:
    _edit(reg, "product_usage", lambda rows: rows[0].update(locator="page 3"))
    assert any("does not match pattern supply_locator" in e for e in validate(reg).errors)


def test_mutation_rights_and_length(reg: Path) -> None:
    def bad(rows: Rows) -> None:
        r = _row(rows, source_id="eo:gupta2023")  # IEEE accepted manuscript, restricted_local_only
        r.update(notes='"quoted sentence from the paper"')
        rows[0].update(stated_spec="x" * 121)

    _edit(reg, "product_usage", bad)
    assert _has(reg, "quotation marks in a restricted source's row")
    assert _has(reg, "stated_spec longer than")


def test_mutation_duplicate_fact(reg: Path) -> None:
    _edit(reg, "product_usage", lambda rows: rows.append({**rows[0], "usage_id": rows[0]["usage_id"] + "_dup"}))
    assert _has(reg, "rows for (source, org, role, product)")


def test_mutation_product_binding(reg: Path) -> None:
    prod = {c: "" for c in columns("products")}
    prod.update(
        product_id="product_keysight-m8199b",
        org_id="org_amf",
        category_id="H6",
        model="M8199B",
        status="unknown",
        verified_on="2026-10-20",
    )
    _edit(reg, "products", lambda rows: rows.append(prod))

    def use(rows: Rows) -> None:
        r = _row(rows, role="fabrication", org_id="org_amf", source_id="eo:johnson2025")
        r.update(product_id="product_keysight-m8199b", usage_id=r["usage_id"] + "_keysight_m8199b")

    _edit(reg, "product_usage", use)
    errs = _errs(reg)
    assert any("id must start with product_amf-" in e for e in errs)
    assert any("!= product category H6" in e for e in errs)


def test_mutation_product_specs(reg: Path) -> None:
    prod = {c: "" for c in columns("products")}
    prod.update(
        product_id="product_amf-x1",
        org_id="org_amf",
        category_id="B1",
        model="X1",
        status="unknown",
        verified_on="2026",
    )
    _edit(reg, "products", lambda rows: rows.append(prod))
    spec = {c: "" for c in columns("product_specs")}
    spec.update(
        spec_id="product_amf-x1-s1",
        product_id="product_amf-x1",
        parameter="wg_loss_db_per_cm",
        basis="datasheet_spec",
        source_id="eo:johnson2025",
        locator="p.1",
        verified_on="2026-10-20",
    )
    _edit(reg, "product_specs", lambda rows: rows.append(spec))
    errs = _errs(reg)
    assert any("value or value_text required" in e for e in errs)
    assert any("needs a ds: source" in e for e in errs)


def test_mutation_processes(reg: Path) -> None:
    def bad(rows: Rows) -> None:
        _row(rows, process_id="proc_amf_eo_geravand2025").update(broker_org_id="org_amf")
        _row(rows, process_id="proc_amf_eo_johnson2025").update(broker_org_id="org_cmc_microsystems")
        _row(rows, process_id="proc_imec_eo_li2026b").update(process_id="proc_imec_x")
        _row(rows, process_id="proc_luxtelligence_eo_kari2025").update(pdk_name="")

    _edit(reg, "foundry_processes", bad)
    errs = _errs(reg)
    assert any("broker_org_id is the foundry itself" in e for e in errs)
    assert any("needs access_route mpw_via_broker" in e for e in errs)
    assert any("id must be proc_imec_eo_li2026b" in e for e in errs)
    assert any("pdk_open without pdk_name" in e for e in errs)


def test_mutation_standards(reg: Path) -> None:
    _edit(reg, "standards", lambda rows: _row(rows, standard_id="std_jesd47").update(designation="JESD47K"))
    assert _has(reg, "id must be std_jesd47k")


def test_mutation_tests(reg: Path) -> None:
    def bad(rows: Rows) -> None:
        rows[0].update(t_min_c="200", t_max_c="100")
        rows[1].update(rh_pct="120")
        rows[2].update(atlas_ref="")
        rows[3].update(atlas_ref="eo-atlas:papers.csv#x")
        rows[4].update(test_id="rt_eo_" + rows[4]["test_id"].removeprefix("rt_pk_"))

    _edit(reg, "reliability_tests", bad)
    errs = _errs(reg)
    assert any("t_min_c > t_max_c" in e for e in errs)
    assert any("outside 0..100" in e for e in errs)
    assert any("rows need atlas_ref" in e for e in errs)
    assert any("is not an anchor of the source's atlas" in e for e in errs)
    assert any("id must start with rt_pk_" in e for e in errs)


def test_mutation_test_ids_and_anchors(reg: Path) -> None:
    def bad(rows: Rows) -> None:
        rows[0].update(test_id=rows[0]["test_id"] + "x")  # not test_id('pk', metric id of atlas_ref)
        rows[1].update(tv_ref=rows[1]["tv_ref"] + "z")  # metric not of this test vehicle
        r = _row(rows, test_id="rt_pk_001c_147203_b_m1")
        r.update(source_id="pk:ectc32696.2021.00125")  # metric not of the row's source

    _edit(reg, "reliability_tests", bad)
    errs = _errs(reg)
    assert any("(from atlas_ref, D60)" in e for e in errs)
    assert sum("is not of test vehicle" in e for e in errs) >= 2


def test_mutation_usage_and_process_anchors(reg: Path) -> None:
    def use(rows: Rows) -> None:
        r = _row(rows, usage_id="use_eo_johnson2025_amf_fabrication")
        r.update(locator="eo-atlas:papers.csv#shen2021/foundry_or_fab")  # another paper's record
        r = _row(rows, usage_id="use_eo_geravand2025_amf_fabrication")
        r.update(locator="eo-atlas:papers.csv#geravand2025/process_name")  # column not allowed for usage

    _edit(reg, "product_usage", use)
    _edit(
        reg,
        "foundry_processes",
        lambda rows: _row(rows, process_id="proc_amf_eo_johnson2025").update(
            locator="eo-atlas:papers.csv#johnson2025/foundry_or_fab"
        ),
    )
    errs = _errs(reg)
    assert any("atlas anchor id 'shen2021' != source native_id 'johnson2025'" in e for e in errs)
    assert any("not allowed for product_usage" in e for e in errs)
    assert any("not allowed for foundry_processes" in e for e in errs)


def test_mutation_designation_and_revision(reg: Path) -> None:
    _edit(
        reg,
        "reliability_tests",
        lambda rows: _row(rows, standard_ids="std_jesd22_a104").update(standard_printed="JEDEC condition G"),
    )

    def std(rows: Rows) -> None:
        rows.append({**rows[0], "standard_id": "std_jesd22_a104f", "designation": "JESD22-A104F"})

    _edit(reg, "standards", std)
    errs = _errs(reg)
    assert any("designation 'JESD22-A104' (std_jesd22_a104) not in standard_printed" in e for e in errs)
    assert any("ends in a revision letter" in e for e in errs)


def test_mutation_fields_per_test_type(reg: Path) -> None:
    def bad(rows: Rows) -> None:
        _row(rows, test_type="high_temp_storage").update(t_min_c="-40", t_max_c="125", rh_pct="85")
        _row(rows, test_type="msl_preconditioning", temp_c="").update(temp_c="260")
        _row(rows, test_type="die_shear").update(temp_c="130")

    _edit(reg, "reliability_tests", bad)
    errs = _errs(reg)
    assert any("t_min_c / t_max_c only for" in e for e in errs)
    assert any("rh_pct only for" in e for e in errs)
    assert any("temp_c not parsed for msl_preconditioning" in e for e in errs)
    assert any("temp_c not parsed for die_shear" in e for e in errs)


def test_mutation_facility_wafer_and_quotes(reg: Path) -> None:
    def bad(rows: Rows) -> None:
        r = _row(rows, role="facility_use")
        r.update(
            role="fabrication",
            category_id="B1",
            usage_id=rules_supply.usage_id(r["source_id"], r["org_id"], "fabrication"),
        )
        r = _row(rows, role="wafer_supply", category_id="A2.1")
        r.update(category_id="B1")
        r = _row(rows, source_id="eo:gupta2023")  # restricted_local_only
        r.update(notes="\u2018quoted\u2019")

    _edit(reg, "product_usage", bad)
    errs = _errs(reg)
    assert any("is typed facility: B-category rows are facility_use" in e for e in errs)
    assert any("wafer_supply does not allow subcategory B1" in e for e in errs)
    assert any("quotation marks in a restricted source's row" in e for e in errs)


def test_mutation_round2_usage(reg: Path) -> None:
    import datetime as dt

    future = (dt.date.today() + dt.timedelta(days=30)).isoformat()

    def bad(rows: Rows) -> None:
        r = _row(rows, usage_id="use_eo_chelladurai2025_la_luce_cristallina_wafer_supply")
        r.update(locator="eo-atlas:papers.csv#chelladurai2025/foundry_or_fab")  # wafer role from the fab column
        r = _row(rows, usage_id="use_eo_hess2026_lightwave_logic_material_supply")
        r.update(category_id="A2.1")  # material_supply only A4 / A5 / E
        r = _row(rows, role="wafer_supply", category_id="A2.2")
        r.update(category_id="A4")  # wafer_supply not A4
        r = _row(rows, usage_id="use_eo_kohli2025_ligentec_fabrication")
        rows.append(
            {
                **r,
                "usage_id": "use_eo_kohli2025_ligentec_wafer_supply",
                "role": "wafer_supply",
                "locator": "eo-atlas:papers.csv#kohli2025/wafer_supplier",
            }
        )
        _row(rows, usage_id="use_eo_johnson2025_amf_fabrication").update(verified_on=future)

    _edit(reg, "product_usage", bad)
    errs = _errs(reg)
    assert any("role wafer_supply cannot come from EO column foundry_or_fab" in e for e in errs)
    assert any("material_supply does not allow subcategory A2.1" in e for e in errs)
    assert any("wafer_supply does not allow subcategory A4" in e for e in errs)
    assert any("B2 wafers from the fab are one fact" in e for e in errs)
    assert any("is in the future" in e for e in errs)


def test_mutation_round2_tests_and_standards(reg: Path) -> None:
    def bad(rows: Rows) -> None:
        _row(rows, test_type="high_temp_storage", temp_c="150").update(temp_c="151")  # not in the condition
        _row(rows, test_type="optical_loss", measurand="optical_loss").update(measurand="die_shear")
        _row(rows, qualifier="approx").update(value="")
        r = _row(rows, test_type="uhast", rh_pct="85")
        r.update(test_type="damp_heat", parameter="x", variant="", condition="500 h", temp_c="", rh_pct="")
        _row(rows, test_id="rt_pk_001c_147203_b_m1").update(notes="\u2018quoted\u2019")  # pk = restricted

    _edit(reg, "reliability_tests", bad)
    _edit(
        reg,
        "standards",
        lambda rows: rows.append({**rows[0], "standard_id": "std_jesd22_a118b_01", "designation": "JESD22-A118B.01"}),
    )
    errs = _errs(reg)
    assert any("temp_c 151 does not occur in the condition text" in e for e in errs)
    assert any("measurement test_type optical_loss with measurand die_shear" in e for e in errs)
    assert any("qualifier approx without a value" in e for e in errs)
    assert any("damp_heat without a humidity keyword" in e for e in errs)
    assert any("rt_pk_001c_147203_b_m1: quotation marks in a restricted source's row" in e for e in errs)
    assert any("JESD22-A118B.01' ends in a revision letter" in e for e in errs)


def test_mutation_category_tree(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    bad = tmp_path / "cats.yaml"
    bad.write_text(
        "categories:\n"
        "  - {id: A, label: a}\n"
        "  - {id: A1, parent: B, label: wrong parent}\n"
        "  - {id: A2.1, parent: A2, label: missing parent}\n"
        "  - {id: A, label: duplicate}\n"
        "  - {id: Z9, parent: Z, label: bad id}\n"
    )
    monkeypatch.setattr(rules_supply, "CATEGORIES", bad)
    errs = rules_supply.tree_errors()
    assert any("duplicate id 'A'" in e for e in errs)
    assert any("A1: parent 'B' != id prefix 'A'" in e for e in errs)
    assert any("A2.1: parent 'A2' not defined" in e for e in errs)
    assert any("bad id 'Z9'" in e for e in errs)
