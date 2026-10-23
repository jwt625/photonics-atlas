"""Vendor / model scanner (DevLog-003 D205-D209): text handling, candidates, product ids, staged pilot batch, and
validator mutations for scan_review rows."""

from __future__ import annotations

import importlib.util
import shutil
import sys
from pathlib import Path
from types import ModuleType

import pytest

from photonics_atlas import rules_supply
from photonics_atlas.csvio import read_csv, read_header, split_list, write_csv
from photonics_atlas.paths import ROOT, STAGING
from photonics_atlas.schema import columns
from photonics_atlas.supply_scan import (
    flex_spaces,
    load_dictionary,
    locator_at,
    page_marks,
    page_text,
    printed_on,
    regions,
    scan_text,
)
from photonics_atlas.validate import validate


def _load_build() -> ModuleType:
    spec = importlib.util.spec_from_file_location("build_supply_staging", ROOT / "scripts" / "build_supply_staging.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["build_supply_staging"] = mod
    spec.loader.exec_module(mod)
    return mod


BUILD = _load_build()

PILOT = STAGING / "supply" / "products" / "pilot_01"
DICT = load_dictionary()

TEXT = """---
paper_id: demo
---

<!-- page 1 -->
Demo Author (1) Keysight Technologies, 1400 Fountaingrove Parkway, Santa Rosa, CA 95403, USA
Abstract
We report a modulator.
<!-- page 2 -->
The chip was fabricated at Advanced
Micro Foundry on 200 mm wafers. The spectra were recorded with an optical spectrum analyzer (Yokogawa AQ6374).
The probe was a 67 GHz RF probe (FormFactor, I67-A-GSG). A tunable laser (TSL-570) was used.
Acknowledgements
We thank Thorlabs for a loan.
References
[1] A. Author, measured with a Santec TSL-550, Opt. Express (2020).
[2] B. Author, Keysight M8199B, J. Lightwave Technol. (2021).
Methods
The electrodes were written by electron beam lithography (Raith EBPG 5200+).
"""


def _cands() -> list[dict[str, object]]:
    return scan_text(TEXT, "eo", "eo:demo", DICT)


def test_page_markers_and_ofc_locators() -> None:
    marks = page_marks(TEXT, "eo")
    assert locator_at(marks, TEXT.index("Abstract")) == "p.1"
    assert locator_at(marks, TEXT.index("Yokogawa")) == "p.2"
    assert locator_at(marks, 0) == "pNA"
    ofc = "Title\nAffil\n![](_page_0_Figure_1.jpeg)\ntext A\n![](_page_1_Picture_2.jpeg)\ntext B"
    om = page_marks(ofc, "ofc2026")
    assert locator_at(om, ofc.index("Affil")) == "pNA"
    assert locator_at(om, ofc.index("text A")) == "p.~1"
    assert locator_at(om, ofc.index("text B")) == "p.~2"
    assert "text B" in page_text(ofc, "ofc2026", "p.~2 Fig. 3") and "text A" not in page_text(ofc, "ofc2026", "p.~2")


def test_regions_skip_references_but_not_methods_after_them() -> None:
    kinds = {k: TEXT[s:e] for s, e, k in regions(TEXT) if k != "body"}
    assert "Santec TSL-550" in kinds["refs"] and "Raith" not in kinds["refs"]
    assert "Thorlabs" in kinds["ack"]
    assert "Demo Author" in kinds["front"]
    # No References heading: a [1] ... [2] run late in the text starts the reference list.
    body = "x " * 400 + "\nResults\nWe used a Santec TSL-570.\n"
    refs = "[1] A. B., Santec TSL-550 paper.\n[2] C. D., another.\n"
    txt = body + refs
    rk = [(k, txt[s:e]) for s, e, k in regions(txt)]
    assert any(k == "refs" and "TSL-550" in t for k, t in rk)


def test_candidates() -> None:
    cs = _cands()
    by = {(c["vendor"], c["model"]): c for c in cs}
    yk = by[("Yokogawa", "AQ6374")]
    assert yk["kind"] == "vendor+model" and yk["org_id"] == "org_yokogawa_electric" and yk["locator"] == "p.2"
    ff = by[("FormFactor", "I67-A-GSG")]
    assert ff["kind"] == "vendor+model" and ff["cat_hint"] == "H9"
    # Model only: vendor from the config pattern, not printed.
    ts = by[("Santec", "TSL-570")]
    assert ts["kind"] == "model" and ts["vendor_printed"] == "" and ts["infer_ok"] is True
    # Line-wrapped vendor names match (flex spaces); text after the reference list (Methods) is scanned.
    assert ("Advanced Micro Foundry", "") in by and by[("Raith", "EBPG 5200+")]["zone"] == "body"
    # Reference-list mentions are never candidates; acknowledgement and affiliation mentions are flagged by zone.
    assert ("Santec", "TSL-550") not in by and ("Keysight", "M8199B") not in by
    assert by[("Thorlabs", "")]["zone"] == "ack"
    assert by[("Keysight", "")]["zone"] in ("front", "affil")
    assert all(c["context"] and len(str(c["context"])) <= 300 for c in cs)
    assert len({c["cand_id"] for c in cs}) == len(cs)
    assert [c["cand_id"] for c in _cands()] == [c["cand_id"] for c in cs]  # deterministic ids


def test_flex_spaces_and_printed_on() -> None:
    assert flex_spaces("Advanced Micro Foundry") == r"Advanced\s+Micro\s+Foundry"
    assert flex_spaces("Shin[- ]?Etsu") == "Shin[- ]?Etsu"
    page = "an EDFA (Amo- nics, AEDFA-40) and a molding machine (VCM- 330MS) with a GS Inﬁnity probe"
    assert printed_on("Amonics", page) and printed_on("VCM-330MS", page) and printed_on("GS Infinity", page)
    assert not printed_on("AEDFA-41", page) and not printed_on("", page)


def test_model_slug_and_product_id() -> None:
    pid = rules_supply.product_id
    assert pid("org_raith", "EBPG 5200+") == "product_raith-ebpg5200plus"
    assert pid("org_raith", "EBPG 5200") == pid("org_raith", "EBPG5200") == "product_raith-ebpg5200"
    assert pid("org_x", "MLA 150") == pid("org_x", "MLA-150") == pid("org_x", "MLA150")
    assert pid("org_x", "COMSOL Multiphysics") == pid("org_x", "Comsol Multiphysics")
    assert pid("org_x", "N4372") != pid("org_x", "N4372E")
    assert pid("org_newport", "818-SL/DB") == "product_newport-818sldb"
    assert pid("org_x", "NRP110T.02") == "product_x-nrp110t.02"
    assert pid("org_x", "Model 110.") == "product_x-model110"


def test_strip_vendor_prefix() -> None:
    gz = [v for v in DICT.vendors if v.origin == "gazetteer" and v.org_id]
    surf = BUILD.vendor_surfaces(gz)
    comsol = next(v.org_id for v in gz if v.name == "COMSOL")
    assert BUILD.strip_vendor("COMSOL Multiphysics", surf[comsol]) == "Multiphysics"
    assert BUILD.strip_vendor("Comsol Multiphysics", surf[comsol]) == "Multiphysics"
    assert BUILD.strip_vendor("COMSOL", surf[comsol]) == "COMSOL"


def test_config_integrity() -> None:
    orgs = {o["org_id"] for o in read_csv(ROOT / "data" / "registry" / "organizations.csv")}
    assert all(v.org_id in orgs for v in DICT.vendors if v.org_id)
    cats = rules_supply.load_categories()
    assert all(v.cat in cats for v in DICT.vendors if v.origin == "gazetteer")
    assert all(m.cat in cats and m.vendor in DICT.by_name for m in DICT.models)
    # Lineage-ambiguous models never allow an inferred vendor.
    assert not next(m for m in DICT.models if m.rx.search("AQ6317B")).infer
    assert not next(m for m in DICT.models if m.rx.search("XPDV2120R")).infer
    # D295: vendors that changed over time never allow an inferred vendor (Lumerical, HFSS, CST, RSoft, Savannah,
    # Dektak, EXFO Yenista-era, Agilent-era Keysight models).
    for model in (
        "Lumerical",
        "HFSS",
        "CST Studio Suite",
        "RSoft",
        "Savannah S200",
        "Dektak XT",
        "T100S-HP",
        "XTA-50",
        "N5227B",
        "N4373E",
        "B2912A",
        "DSOX4054A",
        "E5071C",
        "PNA-X",
    ):
        assert not next(m for m in DICT.models if m.rx.fullmatch(model)).infer, model


# --------------------------------------------------------------------------- pilot batch on disk


@pytest.mark.parametrize("batch", ["pilot_01", "pilot_02"])
def test_pilot_batch_files(batch: str) -> None:
    pilot = PILOT.parent / batch
    cands = read_csv(pilot / "candidates.csv")
    review = read_csv(pilot / "review.csv")
    assert cands and all(c["verdict"] in ("true", "false") and c["reason"] for c in cands)
    ids = {c["cand_id"]: c for c in cands}
    for r in review:
        for x in split_list(r["cand_ids"]):
            assert ids[x]["verdict"] == "true"
    # Every true candidate is a review line or a recorded non-row reason.
    linked = {x for r in review for x in split_list(r["cand_ids"])}
    for c in cands:
        if c["verdict"] == "true" and c["cand_id"] not in linked:
            assert c["reason"] in ("covered", "no_vendor", "dup"), c
    assert read_header(pilot / "products.csv") == columns("products")
    assert read_header(pilot / "product_usage.csv") == columns("product_usage")
    prods = {p["product_id"]: p for p in read_csv(pilot / "products.csv")}
    prods |= {p["product_id"]: p for p in read_csv(ROOT / "data" / "supply" / "products.csv")}
    for p in prods.values():
        assert p["product_id"] == rules_supply.product_id(p["org_id"], p["model"])
    for u in read_csv(pilot / "product_usage.csv"):
        assert u["extraction"] == "scan_review" and u["locator"].startswith(("p.", "pNA"))
        assert u["usage_id"] == rules_supply.usage_id(u["source_id"], u["org_id"], u["role"], u["product_id"])
        if u["product_id"]:
            assert prods[u["product_id"]]["org_id"] == u["org_id"]


def test_pilot_batches_merged() -> None:
    """pilot_01 and pilot_02 were merged with --merge (2026-10-23, D299): every staged row is in data/supply."""
    have_u = {u["usage_id"]: u for u in read_csv(ROOT / "data" / "supply" / "product_usage.csv")}
    have_p = {p["product_id"] for p in read_csv(ROOT / "data" / "supply" / "products.csv")}
    merged = sorted(x.parent.name for x in PILOT.parent.glob("*/product_usage.csv"))
    assert {"pilot_01", "pilot_02", "full_01", "full_02", "full_13"} <= set(merged)
    for batch in merged:
        for u in read_csv(PILOT.parent / batch / "product_usage.csv"):
            assert have_u[u["usage_id"]] == u
        assert {p["product_id"] for p in read_csv(PILOT.parent / batch / "products.csv")} <= have_p
    scan = [u for u in have_u.values() if u["extraction"] == "scan_review"]
    assert scan and all(u["locator"].startswith(("p.", "pNA")) for u in scan)


# --------------------------------------------------------------------------- validator mutations


@pytest.fixture()
def staged(tmp_path: Path) -> Path:
    shutil.copytree(ROOT / "data", tmp_path / "data")  # pilot rows are merged into data/supply (D299)
    return tmp_path


def _mutate(root: Path, table: str, uid: str, **kv: str) -> list[str]:
    path = root / "data" / "supply" / f"{table}.csv"
    rows = read_csv(path)
    key = "product_id" if table == "products" else "usage_id"
    next(r for r in rows if r[key] == uid).update(kv)
    write_csv(path, columns(table), rows)
    return validate(root).errors


def test_mutation_product_id_must_match_model(staged: Path) -> None:
    errs = _mutate(staged, "products", "product_raith-ebpg5200plus", model="EBPG 5200")
    assert any("org + canonical model" in e for e in errs)


def test_mutation_scan_review_locators(staged: Path) -> None:
    pk = next(u for u in read_csv(PILOT / "product_usage.csv") if u["source_id"].startswith("pk:"))
    errs = _mutate(staged, "product_usage", pk["usage_id"], locator="p.~2")
    assert any("pk: page locators are p.N" in e for e in errs)
    lit = next(u for u in read_csv(PILOT / "product_usage.csv") if u["source_id"].startswith("lit:"))
    errs = _mutate(staged, "product_usage", lit["usage_id"], locator=f"eo-atlas:papers.csv#{lit['source_id']}/x")
    assert any("need a page locator" in e or "page locators are p.N" in e for e in errs)


def test_mutation_scan_review_quotes_and_category(staged: Path) -> None:
    restricted = next(u for u in read_csv(PILOT / "product_usage.csv") if u["source_id"] == "eo:valdez2023a")
    errs = _mutate(staged, "product_usage", restricted["usage_id"], stated_spec='"verbatim text"')
    assert any("quotation marks" in e for e in errs)
    errs = _mutate(staged, "product_usage", restricted["usage_id"], stated_spec="x", category_id="G1")
    assert any("product" in e and "category" in e for e in errs)


# --------------------------------------------------------------------------- audit fixes (D292-D295)


def _scan(body: str, corpus: str = "eo") -> list[dict[str, object]]:
    text = "<!-- page 1 -->\nAbstract\nx.\n<!-- page 2 -->\n" + body
    return scan_text(text, corpus, "eo:demo", DICT)


def test_optional_spaces_match_both_forms() -> None:
    for pat, hits in (
        ("New ?Focus", ("NewFocus", "New Focus", "New\nFocus")),
        ("Menlo ?Systems", ("MenloSystems", "Menlo Systems")),
        ("Lake ?Shore", ("LakeShore", "Lake Shore")),
        ("Master ?Bond", ("MasterBond", "Master Bond")),
    ):
        import re

        rx = re.compile(flex_spaces(pat))
        assert all(rx.fullmatch(h) for h in hits), pat


def test_model_tails_and_cleaning() -> None:
    from photonics_atlas.supply_scan import clean_model

    cs = _scan("Films of Titanium and a titanate were grown. We used Lumerical and COMSOL for the modes.\n")
    assert not any(str(c["model"]).startswith("Titan") for c in cs)
    assert all(c["model"] != "Lumerical and" for c in cs)
    assert clean_model("AEDFA-40)") == "AEDFA-40"
    assert clean_model("TSL- 510") == "TSL-510"
    assert clean_model("Lumerical simulations") == "Lumerical"
    cs = _scan("An EDFA (Amonics, AEDFA-40) and a laser (Santec TSL- 510) were used.\n")
    assert {"AEDFA-40", "TSL-510"} <= {str(c["model"]) for c in cs}


def test_acronym_over_matches() -> None:
    cs = _scan(
        "A spatial light modulator (SLM) and interdigital transducers (IDT) were used with AGC enabled. Funded by the "
        "TITAN grant. Hewlett Packard Enterprise provided servers. The Dow Corning sealant was applied.\n"
    )
    names = {str(c["vendor"]) for c in cs}
    assert not names & {
        "Silicon Light Machines",
        "Integrated Device Technology",
        "AGC",
        "MPI",
        "Hewlett-Packard",
        "Dow",
    }
    assert "Dow Corning" in names


def test_reference_lists_and_inline_labels() -> None:
    n = "body text. " * 300
    ofc = n + '\n## <span id="page-2-0"></span>References\n- [1] A. B., Santec TSL-550 study.\n- [2] C. D.\n'
    assert any(k == "refs" and "TSL-550" in ofc[s:e] for s, e, k in regions(ofc))
    singular = n + "\nReference\n[1] A. B., Keysight M8199B.\n[2] C.\n"
    assert any(k == "refs" and "M8199B" in singular[s:e] for s, e, k in regions(singular))
    table = n + "\nReference\nLD type\nThis work\n" + n
    assert not any(k == "refs" for _, _, k in regions(table))
    bullets = n + "\n- [1] A. B., Santec TSL-550.\n- [2] C. D.\n"
    assert any(k == "refs" and "TSL-550" in bullets[s:e] for s, e, k in regions(bullets))
    inline = n + "\n**Acknowledgements:** We thank Thorlabs for lending a PDA36A2.\n\nNext paragraph.\n"
    rk = {inline[s:e].strip()[:20]: k for s, e, k in regions(inline)}
    assert any(k == "ack" and "Thorlabs" in inline[s:e] for s, e, k in regions(inline)), rk
    coi = n + "\nCompeting interests\nA. B. works on lasers at Lumentum.\n"
    assert any(k == "coi" and "Lumentum" in coi[s:e] for s, e, k in regions(coi))


def test_ofc_span_anchors_and_sentences() -> None:
    t = 'Intro text\n<span id="page-1-0"></span>more text on page two'
    assert locator_at(page_marks(t, "ofc2026"), t.index("more")) == "p.~2"
    cs = _scan("A laser (784 nm; ThorLabs, Inc.) was used. Probes from Cascade Microtech, Inc. Were fine.\n")
    tl = next(c for c in cs if c["vendor"] == "Thorlabs")
    assert "784 nm" in str(tl["context"])


def test_one_candidate_per_org_and_stable_ids() -> None:
    from photonics_atlas.supply_scan import Vendor, _cand

    cs = _scan("The detector (Thorlabs PDA36A2) and Thorlabs mounts were used.\n")
    keys = [(c["org_id"] or c["vendor"]) for c in cs if c["kind"] in ("vendor", "vendor+model")]
    assert len(keys) == len(set(keys))
    import re

    t = "x Thorlabs y"
    m = re.search("Thorlabs", t)
    assert m
    a = Vendor("Thorlabs", "", "H", re.compile("Thorlabs"), "gazetteer")
    b = Vendor("Thorlabs Inc.", "org_thorlabs", "", re.compile("Thorlabs"), "registry")
    marks = page_marks(t, "eo")
    ca = _cand(t, "eo", "eo:x", marks, 0, len(t), 2, "body", True, a, (a, m), None, "")
    cb = _cand(t, "eo", "eo:x", marks, 0, len(t), 2, "body", True, b, (b, m), None, "")
    assert ca["cand_id"] == cb["cand_id"]


def test_unlisted_case_and_lineage() -> None:
    cs = _scan(
        "The signal was recorded with a detector (Zorblax ZX-4000) and a stage from Quuxtronic GmbH. Use is limited "
        "to Stanford. See (Fig. 3a). A tunable laser (Agilent 8164B) was swept. Balls were jetted by a PACTECH SB2.\n"
    )
    un = {(c["vendor"], c["model"]) for c in cs if c["kind"] == "unlisted"}
    assert ("Zorblax", "ZX-4000") in un and ("Quuxtronic", "") in un
    assert not any("limited" in str(v).lower() or v == "Fig" for v, _ in un)
    ag = [c for c in cs if c["model"] == "8164B"]
    assert len(ag) == 1 and ag[0]["vendor"] == "Agilent" and ag[0]["kind"] == "vendor+model"
    assert not any(c["vendor"] == "Agilent" and c["kind"] == "vendor" for c in cs)
    assert any(c["vendor"] == "PacTech" for c in cs)
    assert not any(c["vendor"] == "CORNERSTONE" for c in _scan("This is the cornerstone of the method.\n"))


def test_coordinator_rulings_d299() -> None:
    n = "body text. " * 300
    # D299a: facilities are candidates in methods and acknowledgement text, not in author affiliations.
    text = (
        "<!-- page 1 -->\nA. Author, Marvell Nanofabrication Laboratory, Berkeley, CA, USA\nAbstract\nx.\n"
        "<!-- page 2 -->\nThe chips were patterned in the Marvell Nanofabrication Laboratory. " + n + "\n"
        "Acknowledgements\nDevices were fabricated at the Center for Nano-Micro Manufacturing.\n"
    )
    cs = scan_text(text, "eo", "eo:demo", DICT)
    fac = [(c["zone"], c["org_id"]) for c in cs if c["vendor_origin"] == "facility"]
    assert ("body", "org_marvell_nanofabrication_laboratory") in fac
    assert ("ack", "org_center_for_nano_micro_manufacturing") in fac
    assert not any(z in ("front", "affil") for z, _ in fac)
    # D299b: bare VDI (a funding agency) is not Virginia Diodes; the full name and extender models are.
    cs = _scan(
        "The project is managed by the VDI Technology Center. A WR3.4 VNAX extender (Virginia Diodes) was used.\n"
    )
    vd = [c for c in cs if c["vendor"] == "Virginia Diodes"]
    assert vd and all(c["vendor_printed"] == "Virginia Diodes" or c["model"] for c in vd)
    assert not any(c["vendor_printed"] == "VDI" for c in cs)
    # D299c: unlisted candidates only in body text.
    ack = n + "\nAcknowledgements\nWe thank the partners Quuxtronic GmbH and Zorblax AG for collaboration.\n"
    assert not any(c["kind"] == "unlisted" for c in scan_text(ack, "eo", "eo:demo", DICT))


def test_second_audit_rules() -> None:
    # D320 accents fold; D317 model normalization.
    pid = rules_supply.product_id
    assert pid("org_x", "TherMoiré AXP") == pid("org_x", "TherMoire AXP")
    gz = [v for v in DICT.vendors if v.origin == "gazetteer" and v.org_id]
    surf = BUILD.vendor_surfaces(gz)
    ansys = next(v.org_id for v in gz if v.name == "Ansys")
    epo = next(v.org_id for v in gz if v.name == "Epoxy Technology")
    assert BUILD.strip_vendor("Ansys Optics", surf[ansys]) == "Ansys Optics"
    assert BUILD.strip_vendor("EPO-TEK 301-2", surf[epo]) == "301-2"
    assert BUILD.strip_vendor("Model 110", []) == "110"
    assert BUILD.strip_vendor("Multiprep System", []) == "Multiprep"
    # D318: no gazetteer vendor without org silently matches a registry org name.
    assert DICT.warnings == []
    shf = next(v for v in DICT.vendors if v.name == "SHF")
    assert shf.org_id
    # D321: unlisted noise filters.
    n = "body text. " * 300
    noisy = (
        n + "\nThe layers were patterned (Steps 1-2) and etched.\n"
        "© 2023 Wiley-VCH GmbH\n"
        "This work was supported by Quuxtronic GmbH under a grant.\n"
        "The index was measured with a prism coupler (Zorblax 2010).\n"
    )
    un = [c for c in scan_text(noisy, "eo", "eo:demo", DICT) if c["kind"] == "unlisted"]
    assert un == []
    cs = _scan("The index was measured by a prism coupler (Metricon 2010) at 1536 nm.\n")
    assert any(c["vendor"] == "Metricon" and c["model"] == "2010" for c in cs)
    assert any(c["vendor"] == "SMART Photonics" for c in _scan("The chips were fabricated at SMART photonics.\n"))


def test_d326_rules() -> None:
    # D326: product_line only when printed; the merged I67-A-GSG row was corrected through the build replace path.
    prods = {p["product_id"]: p for p in read_csv(ROOT / "data" / "supply" / "products.csv")}
    assert prods["product_formfactor-i67agsg"]["product_line"] == ""
    # D326a: OE-format reference lists right after the abstract are not scanned; the body after them is.
    n = "body text. " * 50
    oe = (
        "Title\nAbstract\nWe show a device.\nReferences and links\n1. A. B., Santec TSL-550, Opt. Express (2010).\n"
        "2. C. D.\nIntroduction\n" + n + "We used a Santec TSL-570 laser.\n" + n
    )
    kinds = [(k, oe[s:e]) for s, e, k in regions(oe)]
    assert any(k == "refs" and "TSL-550" in t for k, t in kinds)
    assert any(k == "body" and "TSL-570" in t for k, t in kinds)
    cs = _scan(
        "Circuits were simulated in Keysight ADS and measured with an N5291A VNA and a Thorlabs APD410A detector. "
        "The CST of the device and the dy- namics were studied.\n"
    )
    models = {str(c["model"]) for c in cs}
    assert {"ADS", "N5291A", "APD410A"} <= models
    assert not any(c["vendor"] in ("Dassault CST", "Namics") for c in cs)
    t = "body text. " * 300 + "\nConﬂict of interest\nF. E. is involved at Lumiphase AG.\n"
    assert any(k == "coi" and "Lumiphase" in t[s:e] for s, e, k in regions(t))


def test_check_review_v2(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    """D328: review-only check of a v2 review.csv (verdicts from review.csv alone); writes nothing outside tmp_path."""
    src = PILOT.parent / "pilot_02"
    b = tmp_path / "t_02"
    b.mkdir()
    cands = read_csv(src / "candidates.csv")
    for c in cands:
        c["verdict"] = c["reason"] = ""
    write_csv(b / "candidates.csv", read_header(src / "candidates.csv"), cands)
    facts = read_csv(src / "review.csv")
    linked = {x for r in facts for x in split_list(r["cand_ids"])}
    rows = [{**r, "line_kind": "fact", "reason": ""} for r in facts]
    rest = [c["cand_id"] for c in cands if c["cand_id"] not in linked]
    verdict = {c: "affiliation" for c in rest}
    verdict.update({c["cand_id"]: "covered" for c in cands if c["cand_id"] in rest and c["source_id"] == "eo:yin2026"})
    for cid, reason in verdict.items():
        rows.append(
            {k: "" for k in BUILD.REVIEW_COLUMNS_V2}
            | {"source_id": "x", "cand_ids": cid, "line_kind": "verdict", "reason": reason, "reviewed_on": "2026-10-23"}
        )
    write_csv(b / "review.csv", BUILD.REVIEW_COLUMNS_V2, rows)
    monkeypatch.setattr(BUILD, "BATCHES", tmp_path)
    monkeypatch.setattr(sys, "argv", ["build_supply_staging.py", "t_02", "--check-review"])
    before = sorted(p.name for p in (ROOT / "logs").glob("build_supply_staging_*")) if (ROOT / "logs").exists() else []
    assert BUILD.main() == 0
    assert "CHECK OK t_02" in capsys.readouterr().out
    after = sorted(p.name for p in (ROOT / "logs").glob("build_supply_staging_*")) if (ROOT / "logs").exists() else []
    assert before == after and sorted(p.name for p in b.iterdir()) == ["candidates.csv", "review.csv"]
    # A candidate left without a verdict fails the check.
    write_csv(b / "review.csv", BUILD.REVIEW_COLUMNS_V2, rows[:-1])
    assert BUILD.main() == 1


def test_split_order_deterministic() -> None:
    spec = importlib.util.spec_from_file_location("scan_vendor_models", ROOT / "scripts" / "scan_vendor_models.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    ids = [f"eo:p{i}" for i in range(20)] + [f"pk:q{i}" for i in range(20)]
    assert mod.split_order(ids) == mod.split_order(list(reversed(ids)))
    first = mod.split_order(ids)[:10]
    assert any(x.startswith("eo:") for x in first) and any(x.startswith("pk:") for x in first)


def test_r9_supplementary_after_references() -> None:
    """D343 (R9): supplementary material appended after the reference list is scanned again; a later Supplementary
    References heading does not suppress the [1] ... [2] fallback of the main list."""
    n = "body text. " * 300
    t = (
        n + "\n[1] A. B., Santec TSL-550, Opt. Express (2010).\n[2] C. D.\n"
        "Supplementary Information for: A modulator\nThe device was etched in an Oxford Instruments PlasmaPro 100.\n"
        "Supplementary References\n[1] E. F., Keysight M8199B.\n[2] G.\n"
    )
    kinds = [(k, t[s:e]) for s, e, k in regions(t)]
    assert any(k == "refs" and "TSL-550" in x for k, x in kinds)
    assert any(k == "body" and "PlasmaPro 100" in x for k, x in kinds)
    assert any(k == "refs" and "M8199B" in x for k, x in kinds)
    # A body line starting "[1]" before a real References heading is not a reference list.
    t2 = n + "\n[1] is cited here.\n[2] also.\n" + n + "\nREFERENCES\n[1] A. B.\n"
    assert not any(k == "refs" and "is cited here" in t2[s:e] for s, e, k in regions(t2))
