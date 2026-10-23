"""Checker tests for scripts/ofc_headers.py (DevLog-008 D173-D176, D240-D249): the committed pilot passes, and each
mutation of it (invented or moved fields, grade inflation, contact or address data, broken markers, slot gaps; the
19 mutations of the 2026-10-22 audit included) is an error. Uses the local OFC 2026 text; skips without it."""

from __future__ import annotations

import importlib.util
import shutil
import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
import yaml

from photonics_atlas.paths import ROOT, input_path

from .conftest import needs_inputs

PILOT = ROOT / "data" / "_staging" / "people" / "ofc_headers" / "pilot"
H01 = PILOT.parent / "ofc_h01"
needs_text = pytest.mark.skipif(not input_path("ofc_text_dir").is_dir(), reason="OFC 2026 text not present")
Mut = Callable[[list[dict[str, Any]]], Any]


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("ofc_headers", ROOT / "scripts" / "ofc_headers.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["ofc_headers"] = mod  # pydantic resolves the models' annotations through the module
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def env() -> dict[str, Any]:
    from photonics_atlas.adapters import ofc
    from photonics_atlas.csvio import read_csv, split_list
    from photonics_atlas.orgmatch import load_matcher
    from photonics_atlas.paths import CROSSWALK, REGISTRY

    oh = _load()
    return {
        "oh": oh,
        "meta": {p.code: p for p in ofc.presentations()},
        "texts": oh.text_files(),
        "pdfs": oh.pdf_files(),
        "eo": oh.eo_duplicates(),
        "m": load_matcher(),
        "orgs": {r["org_id"]: r for r in read_csv(REGISTRY / "organizations.csv")},
        "xw": {
            (r["corpus"], r["printed"]): split_list(r["org_ids"]) for r in read_csv(CROSSWALK / "org_crosswalk.csv")
        },
    }


def _run(
    env: dict[str, Any],
    tmp: Path,
    mutate: Mut | None,
    raw: Callable[[str], str] | None = None,
    src: Path = PILOT,
    only: str = "",
) -> tuple[list[str], Path]:
    oh = env["oh"]
    d = tmp / src.name
    d.mkdir()
    shutil.copy(src / "papers.csv", d / "papers.csv")
    data = oh.load_yaml((src / "headers.yaml").read_text(encoding="utf-8"))
    if only:  # one paper of the batch (the others count as not extracted yet: warnings only)
        data = [x for x in data if x["source_id"] == f"ofc2026:{only}"]
    if mutate:
        mutate(data)
    text = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
    (d / "headers.yaml").write_text(raw(text) if raw else text, encoding="utf-8")
    log = oh.RunLog("ofc_headers_test", True, log_dir=tmp / "logs")
    with log:
        ck = oh.Check(log)
        oh.check_batch(d, ck, env["meta"], env["texts"], env["pdfs"], env["eo"], env["m"], env["orgs"], env["xw"], True)
    return list(ck.errors), d


def _p(data: list[dict[str, Any]], code: str) -> dict[str, Any]:
    return next(p for p in data if p["source_id"] == f"ofc2026:{code}")


def _aff(data: list[dict[str, Any]], code: str, i: int) -> dict[str, Any]:
    return _p(data, code)["affiliations"][i]  # type: ignore[no-any-return]


def _au(data: list[dict[str, Any]], code: str, i: int) -> dict[str, Any]:
    return _p(data, code)["authors"][i]  # type: ignore[no-any-return]


@needs_inputs
@needs_text
def test_pilot_is_clean_and_stamped(env: dict[str, Any], tmp_path: Path) -> None:
    errors, d = _run(env, tmp_path, None)
    assert errors == []
    assert env["oh"].stamp_ok(d)


MUTATIONS: dict[str, tuple[Mut, str]] = {
    # first round (DevLog-008 22:10)
    "invented author": (lambda d: _p(d, "M1A.3")["authors"].append({"name": "Ada Example", "markers": ["1"]}), "D246"),
    "undefined marker": (lambda d: _au(d, "M1A.3", 0).update(markers=["3"]), "has no block"),
    "unused block": (lambda d: _au(d, "Th1A.2", 1).update(markers=["1"]), "used by no author"),
    "address in note": (lambda d: _p(d, "M1A.3").update(note="ada@example.org"), "at sign"),
    "spelled address": (lambda d: _p(d, "M1A.3").update(note="ada at example dot org"), "spelled e-mail"),
    "phone": (lambda d: _p(d, "M1A.3").update(note="Tel: +81 46 859 1234"), "phone"),
    "missing slot": (lambda d: _p(d, "M1A.3")["authors"].pop(), "unmatched"),
    "listing order": (lambda d: _au(d, "M1A.1", 2).update(markers=["2", "7"]), "listing_order needs"),
    "locator": (lambda d: _aff(d, "M1A.3", 0).update(locator="page 1"), "locator"),
    "marker in name": (lambda d: _au(d, "M1A.3", 0).update(name="Sae Kojima1"), "carries a marker"),
    "unreadable with rows": (lambda d: _p(d, "M1A.3").update(status="unreadable"), "must carry no"),
    "pdf basis without pdf": (lambda d: _aff(d, "M1A.3", 0).update(basis="pdf"), "without a local PDF"),
    "paper not in batch": (
        lambda d: d.append({"source_id": "ofc2026:M1C.1", "status": "unreadable", "note": "x"}),
        "not in this batch",
    ),
    "locality beyond the city": (lambda d: _aff(d, "M1A.1", 0).update(locality="Nagoya, Aichi"), "city only"),
    "postal code": (lambda d: _aff(d, "M1A.1", 0).update(locality="Nagoya 464-8601"), "postal code"),
    "verbatim block field": (lambda d: _aff(d, "M1A.3", 0).update(text="NTT, Inc."), "Extra inputs are not permitted"),
    # audit 2026-10-22, mutations 1-18 (19 below)
    "a1 invented country": (lambda d: _aff(d, "W3E.7", 1).update(country="US"), "not printed in this block"),
    "a2 wrong country": (lambda d: _aff(d, "M1F.7", 3).update(country="FR"), "not printed in this block"),
    "a3 cross-block locality": (lambda d: _aff(d, "M1A.3", 0).update(locality="Dublin"), "D246"),
    "a4 marker reassigned": (lambda d: _au(d, "Th1D.1", 19).update(markers=["3"]), "printed markers differ"),
    "a5 grade inflation": (
        lambda d: [a.update(basis="printed") for a in _p(d, "M1A.1")["affiliations"]],
        "marker + first field",
    ),
    "a6 org from the title": (
        lambda d: _aff(d, "M1B.2", 3).update(org="Silicon Photonic Microring Transmitter"),
        "not printed after the author line",
    ),
    "a7 joint org from another block": (
        lambda d: _aff(d, "M4E.6", 0).update(
            more_orgs=["National Institute of Information and Communications Technology"]
        ),
        "D246",
    ),
    "a8 present address relabelled": (lambda d: _aff(d, "M3F.4", 2).update(role="affiliation"), "present-address cue"),
    "a9 street name as unit": (lambda d: _aff(d, "Th4A.1", 0).update(unit="Morinosato Wakamiya"), "D246"),
    "a10 NL postal code": (lambda d: _p(d, "M1A.3").update(note="printed with 5612 AZ Eindhoven"), "postal code"),
    "a11 CA postal code": (lambda d: _p(d, "M1A.3").update(note="printed with K1A 0R6"), "postal code"),
    "a12 truncated name": (lambda d: _au(d, "M4B.3", 0).update(name="Anand"), "matches 0 metadata slots"),
    "a13 swapped markers": (
        lambda d: (_au(d, "W1E.3", 2).update(markers=["1", "3"]), _au(d, "W1E.3", 3).update(markers=["2"])),
        "printed markers differ",
    ),
    "a14 layout without note": (
        lambda d: [a.update(basis="layout") for a in _p(d, "Th1A.2")["affiliations"]],
        "layout needs a paper note",
    ),
    "a15 partial without unreadable": (lambda d: _p(d, "M1A.3").update(status="partial"), "status partial needs"),
    "a16 non-org footnote block": (
        lambda d: (
            _p(d, "Th1A.2")["affiliations"].append(
                {"marker": "3", "basis": "printed", "role": "present_address", "org": "Optical Systems Division"}
            ),
            _au(d, "Th1A.2", 0).update(markers=["1", "3"]),
        ),
        "D246",
    ),
    "a17 house number after street": (lambda d: _aff(d, "M1A.3", 0).update(unit="Kapeldreef 75"), "street"),
    "a18 building number": (lambda d: _aff(d, "Th1D.1", 0).update(unit="Kinesis #09-11"), "street number"),
    # D249 extras
    "status footnote as org": (lambda d: _aff(d, "Th1A.2", 1).update(org="no longer affiliated"), "status footnote"),
    "ok with unreadable author": (lambda d: _au(d, "M1A.3", 0).update(unreadable=True), "use partial"),
}


@needs_inputs
@needs_text
@pytest.mark.parametrize("name", sorted(MUTATIONS))
def test_mutation_is_caught(env: dict[str, Any], tmp_path: Path, name: str) -> None:
    mutate, expect = MUTATIONS[name]
    errors, d = _run(env, tmp_path, mutate)
    assert any(expect in e for e in errors), (name, errors)
    assert not (d / "header_rows.csv").exists()  # D248: no derived files on errors


@needs_inputs
@needs_text
def test_a19_unquoted_norway_is_a_string(env: dict[str, Any], tmp_path: Path) -> None:
    """Audit mutation 19: `country: NO` stays the string NO (no YAML 1.1 boolean); in a UK block it is wrong."""
    errors, _ = _run(env, tmp_path, None, raw=lambda t: t.replace("country: GB", "country: NO", 1))
    assert any("country 'NO' is not printed" in e for e in errors), errors


@needs_inputs
@needs_text
def test_grades_by_basis(env: dict[str, Any], tmp_path: Path) -> None:
    """D240 / D246: listing_order and layout rows grade B with a note; printed / single / pdf grade A."""
    from photonics_atlas.csvio import read_csv

    errors, d = _run(env, tmp_path, None)
    assert errors == []
    rows = read_csv(d / "header_rows.csv")
    assert "aff_text" not in rows[0]  # D244
    for r in rows:
        lo = r["marker_basis"] == "listing_order"
        assert r["evidence_grade"] == ("B" if lo else "A")
        assert (r["grade_note"] == "affiliation marker inferred from block order") == lo
    assert sum(r["marker_basis"] == "listing_order" for r in rows) == 10


@needs_inputs
@needs_text
def test_aggregate_skips_stale_batches(env: dict[str, Any], tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """D248: aggregates come only from batches whose derived files match the current YAML."""
    oh = env["oh"]
    errors, d = _run(env, tmp_path, None)
    assert errors == []
    monkeypatch.setattr(oh, "BASE", tmp_path)
    monkeypatch.setattr(oh, "LOCAL", tmp_path / "_local")
    log = oh.RunLog("ofc_headers_test_agg", True, log_dir=tmp_path / "logs")
    with log:
        assert oh.write_aggregates(log, env["meta"], env["orgs"]) == 0
        assert (tmp_path / "org_requests.csv").exists()
        (d / "headers.yaml").write_text((d / "headers.yaml").read_text() + "\n# edited\n", encoding="utf-8")
        assert oh.write_aggregates(log, env["meta"], env["orgs"]) == 1


def test_name_compatibility() -> None:
    oh = _load()
    assert oh.compatible("F. Masahisa", "Masahisa Fujino")  # family-name initial + given name
    assert oh.compatible("L. Gifre", "Lluis Gifre Renom")  # compound family name
    assert oh.compatible("Pablo Armingol Robles", "Pablo Robles")
    assert oh.compatible("Dae-Won Rho", "Daewon Rho")
    assert oh.compatible("H.-T. Peng", "Hsuan-Tung Peng")
    assert oh.compatible("Wen Qi Tan", "Wenqi Tan")
    assert not oh.compatible("Andrea Marotta", "Andrea Sgambelluri")
    assert not oh.compatible("Y. Li", "Yongchao Liu")
    # audit finding 5 (fictitious-style pairs)
    assert not oh.compatible("Yi Wang", "Yu Wang")
    assert not oh.compatible("Jun Li", "Jian Li")
    assert not oh.compatible("Zhang Wei", "Wei Zhao")
    assert not oh.compatible("Liuyan Han", "Han Li")
    assert not oh.compatible("Anand", "Rishi Anand")
    assert not oh.compatible("Dong Cheon Kim", "Dongheon Kim")


def test_fold_artefacts() -> None:
    """D282: dotless i and a spacing acute from the text extraction fold like the composed letter."""
    oh = _load()
    assert oh.alnum("Ruben S. Lu\u00b4\u0131s") == oh.alnum("Ruben S. Lu\u00eds") == "rubensluis"
    assert oh._norm_map("Lu\u00b4\u0131s,1")[0] == "luis1"


needs_h01 = pytest.mark.skipif(not (H01 / "headers.yaml").exists(), reason="batch ofc_h01 not extracted")


@needs_inputs
@needs_text
@needs_h01
def test_h01_is_clean(env: dict[str, Any], tmp_path: Path) -> None:
    errors, _ = _run(env, tmp_path, None, src=H01)
    assert errors == []


@needs_inputs
@needs_text
@needs_h01
@pytest.mark.parametrize(
    ("name", "mutate", "expect"),
    [
        ("prefix org not printed", lambda d: _aff(d, "M1I.5", 0).update(org="NOAA"), "not printed as a prefix"),
        ("prefix flag dropped", lambda d: _aff(d, "M1I.5", 1).update(org_from_prefix=False), "D246"),
        ("prefixed city moved", lambda d: _aff(d, "M1I.5", 0).update(locality="Golden"), "D246"),
    ],
)
def test_org_from_prefix(env: dict[str, Any], tmp_path: Path, name: str, mutate: Mut, expect: str) -> None:
    """D283: a block may inherit its org from a printed prefix, verified against the text."""
    errors, _ = _run(env, tmp_path, mutate, src=H01)
    assert any(expect in e for e in errors), (name, errors)


@needs_inputs
@needs_text
def test_unreadable_author_needs_slot_not_name(env: dict[str, Any], tmp_path: Path) -> None:
    """D284: an unreadable author is not checked against the printed text but must still map to a slot."""

    def garble(d: list[dict[str, Any]]) -> None:
        _p(d, "M1A.3").update(status="partial")
        _au(d, "M1A.3", 0).update(name="Sae Kojimx", markers=[], unreadable=True, slot=1)

    errors, _ = _run(env, tmp_path, garble)
    assert errors == []

    def no_slot(d: list[dict[str, Any]]) -> None:
        _p(d, "M1A.3").update(status="partial")
        _au(d, "M1A.3", 0).update(name="Ada Example", markers=[], unreadable=True)

    (tmp_path / "b").mkdir()
    errors, _ = _run(env, tmp_path / "b", no_slot)
    assert any("matches 0 metadata slots" in e for e in errors), errors


BATCHES = PILOT.parent


def _b(name: str) -> Path:
    return BATCHES / name


needs_batches = pytest.mark.skipif(not (BATCHES / "ofc_h15" / "headers.yaml").exists(), reason="batches not extracted")

# D286: (batch, paper, mutation or None for the clean record, expected error fragment)
D286_CASES: dict[str, tuple[str, str, Mut | None, str]] = {
    "a uruguay clean": ("ofc_h14", "Th2A.40", None, ""),
    "a unknown code": ("ofc_h14", "Th2A.40", lambda d: _aff(d, "Th2A.40", 1).update(country="XX"), "known ISO"),
    "b orcid links clean": ("ofc_h04", "M4A.3", None, ""),
    "b orcid link marker checked": (
        "ofc_h04",
        "M4A.3",
        lambda d: _au(d, "M4A.3", 3).update(markers=["2"]),
        "printed markers differ",
    ),
    "c whole words clean": ("ofc_h10", "W3K.6", None, ""),
    "c part of a word": ("ofc_h10", "W3K.6", lambda d: _aff(d, "W3K.6", 2).update(org="BITECH"), "not printed after"),
    "c unit first clean": ("ofc_h08", "W1G.1", None, ""),
    "c blocks out of order": (
        "ofc_h09",
        "W2A.56",
        lambda d: _p(d, "W2A.56")["affiliations"].insert(2, _p(d, "W2A.56")["affiliations"].pop(3)),
        "D2",
    ),
    "d dropped marker missing": (
        "ofc_h03",
        "M3D.6",
        lambda d: _au(d, "M3D.6", 0).pop("dropped_markers"),
        "printed markers differ",
    ),
    "d recorded marker missing": (
        "ofc_h06",
        "Tu2J.5",
        lambda d: _au(d, "Tu2J.5", 1).update(markers=["2"]),
        "printed markers differ",
    ),
    "d dropped marker is a block": (
        "ofc_h03",
        "M3D.6",
        lambda d: _au(d, "M3D.6", 0).update(dropped_markers=[{"marker": "1", "reason": "x"}]),
        "is a recorded block",
    ),
    "e trailing clean": ("ofc_h09", "W3A.3", None, ""),
    "e trailing flag dropped": (
        "ofc_h09",
        "W3A.3",
        lambda d: [a.update(marker_trailing=False) for a in _p(d, "W3A.3")["affiliations"]],
        "not printed after",
    ),
    "e trailing markers swapped": (
        "ofc_h09",
        "W3A.3",
        lambda d: (_aff(d, "W3A.3", 0).update(marker="3"), _aff(d, "W3A.3", 2).update(marker="1")),
        "D2",
    ),
    "f layout clean": ("ofc_h03", "M3D.3", None, ""),
    "f unmarked block not layout": (
        "ofc_h03",
        "M3D.3",
        lambda d: _aff(d, "M3D.3", 0).update(basis="printed"),
        "needs basis layout",
    ),
    "D287 slot zero clean": ("ofc_h13", "Th2A.8", None, ""),
}


@needs_inputs
@needs_text
@needs_batches
@pytest.mark.parametrize("name", sorted(D286_CASES))
def test_d286(env: dict[str, Any], tmp_path: Path, name: str) -> None:
    batch, code, mutate, expect = D286_CASES[name]
    errors, _ = _run(env, tmp_path, mutate, src=_b(batch), only=code)
    if mutate is None:
        assert errors == [], errors
    else:
        assert any(expect in e for e in errors), (name, errors)


def test_no_fold_for_lookalikes() -> None:
    """D286g: an "l" or a stray digit is not read as marker 1."""
    oh = _load()
    au = oh.AuthorIn(name="Ada Example", markers=["1"])
    assert oh._author_marks(au, "1", set(), True)
    assert not oh._author_marks(au, "l", set(), True)
    assert not oh._author_marks(au, "17", set(), True)


# D300-D305 (batch audit 2026-10-23)
D30X_CASES: dict[str, tuple[str, str, Mut | None, str]] = {
    "D301 campus clean": ("ofc_h07", "W1B.5", None, ""),
    "D301 campus not printed": (
        "ofc_h07",
        "W1B.5",
        lambda d: _aff(d, "W1B.5", 2).update(campus="Guangzhou"),
        "campus 'Guangzhou' not inside",
    ),
    "D302 slot 0 for a metadata author": (
        "ofc_h09",
        "W2A.39",
        lambda d: (_au(d, "W2A.39", 5).update(slot=0), _p(d, "W2A.39").update(author_list_differs=True)),
        "has slot 0 but matches",
    ),
    "D302 clean": ("ofc_h09", "W2A.39", None, ""),
}


@needs_inputs
@needs_text
@needs_batches
@pytest.mark.parametrize("name", sorted(D30X_CASES))
def test_d30x(env: dict[str, Any], tmp_path: Path, name: str) -> None:
    batch, code, mutate, expect = D30X_CASES[name]
    errors, _ = _run(env, tmp_path, mutate, src=_b(batch), only=code)
    if mutate is None:
        assert errors == [], errors
    else:
        assert any(expect in e for e in errors), (name, errors)


@needs_inputs
@needs_text
@needs_batches
def test_campus_row_is_not_the_parent(env: dict[str, Any], tmp_path: Path) -> None:
    """D301: "the Chinese University of Hong Kong, Shenzhen" never maps to CUHK (Hong Kong)."""
    from photonics_atlas.csvio import read_csv

    errors, d = _run(env, tmp_path, None, src=_b("ofc_h07"), only="W1B.5")
    assert errors == []
    rows = [r for r in read_csv(d / "header_rows.csv") if r["org_name"].startswith("the Chinese University")]
    assert rows and all(r["org_name"].endswith(", Shenzhen") for r in rows)
    assert all("org_chinese_university_of_hong_kong" not in r["org_ids"].split(";") for r in rows)


@needs_inputs
@needs_text
def test_parenthesized_place_is_kept(env: dict[str, Any]) -> None:
    """D301: the matcher drops a parenthesized acronym, never a parenthesized place."""
    oh = env["oh"]
    a = oh.AffIn(org="Example Institute (Guangzhou)", locality="Guangzhou", basis="printed")
    assert oh.map_org(env["m"], a) == ([], "unmapped")
    b = oh.AffIn(org="National Institute of Information and Communications Technology (NICT)", basis="printed")
    assert oh.map_org(env["m"], b)[1] == "name:no_parenthetical"


@needs_inputs
@needs_text
def test_org_requests_carry_place(env: dict[str, Any], tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """D303 / D305: org requests per (printed org, city, country) with units and curation notes."""
    import copy

    from photonics_atlas.csvio import read_csv
    from photonics_atlas.textnorm import norm_key

    oh = env["oh"]
    # Org round 6 (DevLog-001 D336) gave the lab its own org, so the pilot string maps; the matcher copy without it
    # keeps the request path (place columns, D305 note) under test.
    m = copy.deepcopy(env["m"])
    m.by_name.pop(norm_key("State Key Laboratory of Optical Fiber and Cable Manufacture Technology"), None)
    errors, _ = _run({**env, "m": m}, tmp_path, None)
    assert errors == []
    monkeypatch.setattr(oh, "BASE", tmp_path)
    monkeypatch.setattr(oh, "LOCAL", tmp_path / "_local")
    with oh.RunLog("ofc_headers_test_req", True, log_dir=tmp_path / "logs") as log:
        oh.write_aggregates(log, env["meta"], env["orgs"])
    rows = read_csv(tmp_path / "org_requests.csv")
    assert set(oh.REQUEST_COLS) <= set(rows[0])
    skl = [r for r in rows if r["printed_org"].startswith("State Key Laboratory of Optical Fiber and Cable")]
    assert skl and all("org_yofc" in r["curation_note"] for r in skl)
