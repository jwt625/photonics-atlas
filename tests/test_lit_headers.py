"""Checker tests for the `lit` corpus of scripts/ofc_headers.py (DevLog-011 D350-D358): the committed lit pilot passes,
and mutations of prose statements, header slots, locators and membership designations are errors. Uses the local
literature cache (references/, cache/literature/merged.jsonl); skips without it."""

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

from photonics_atlas.paths import ROOT

PILOT = ROOT / "data" / "_staging" / "people" / "lit_headers" / "pilot"
needs_cache = pytest.mark.skipif(
    not (ROOT / "cache" / "literature" / "merged.jsonl").exists() or not (ROOT / "references" / "kim2019").is_dir(),
    reason="literature cache not present",
)
Mut = Callable[[list[dict[str, Any]]], Any]


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("ofc_headers", ROOT / "scripts" / "ofc_headers.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["ofc_headers"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def env() -> dict[str, Any]:
    from photonics_atlas.csvio import read_csv
    from photonics_atlas.orgmatch import load_matcher
    from photonics_atlas.paths import REGISTRY

    oh = _load()
    return {
        "oh": oh,
        "meta": oh.lit_papers(),
        "dup": oh.lit_duplicates(),
        "m": load_matcher(),
        "orgs": {r["org_id"]: r for r in read_csv(REGISTRY / "organizations.csv")},
    }


def _run(
    env: dict[str, Any], tmp: Path, mutate: Mut | None, only: str = "", src: Path = PILOT
) -> tuple[list[str], Path]:
    oh = env["oh"]
    d = tmp / src.name
    d.mkdir(parents=True)
    shutil.copy(src / "papers.csv", d / "papers.csv")
    data = oh.load_yaml((src / "headers.yaml").read_text(encoding="utf-8"))
    if only:
        data = [x for x in data if x["source_id"] == f"lit:{only}"]
    if mutate:
        mutate(data)
    (d / "headers.yaml").write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    log = oh.RunLog("lit_headers_test", True, log_dir=tmp / "logs")
    with log:
        ck = oh.Check(log)
        oh.check_batch(d, ck, env["meta"], {}, {}, env["dup"], env["m"], env["orgs"], {}, True, spec=oh.LIT)
    return list(ck.errors), d


def _p(data: list[dict[str, Any]], code: str) -> dict[str, Any]:
    return next(p for p in data if p["source_id"] == f"lit:{code}")


def _aff(data: list[dict[str, Any]], code: str, i: int) -> dict[str, Any]:
    return _p(data, code)["affiliations"][i]  # type: ignore[no-any-return]


def _au(data: list[dict[str, Any]], code: str, i: int) -> dict[str, Any]:
    return _p(data, code)["authors"][i]  # type: ignore[no-any-return]


@needs_cache
def test_lit_pilot_is_clean(env: dict[str, Any], tmp_path: Path) -> None:
    errors, d = _run(env, tmp_path, None)
    assert errors == []
    assert env["oh"].stamp_ok(d)


CASES: dict[str, tuple[str, Mut, str]] = {
    "prose author in the wrong statement": (
        "kim2019",
        lambda d: _au(d, "kim2019", 11).update(markers=["P7"]),
        "is not named in the statement subject",
    ),
    "prose author missing from a statement": (
        "shikama2017",
        lambda d: _au(d, "shikama2017", 2).update(markers=["P2"]),
        "carries no 'P1'",
    ),
    "now with as affiliation": (
        "kim2019",
        lambda d: _aff(d, "kim2019", 2).update(role="affiliation"),
        "present-address cue",
    ),
    "prose field from another statement": (
        "kim2019",
        lambda d: _aff(d, "kim2019", 6).update(locality="Cambridge"),
        "not inside this printed block",
    ),
    "printed marker as prose": ("shikama2017", lambda d: _aff(d, "shikama2017", 0).update(marker="1"), "P<n>"),
    "slots_from_header on a paper with a curator list": (
        "virot2014",
        lambda d: _p(d, "virot2014").update(slots_from_header=True),
        "has an author list",
    ),
    "omitted present-address statement (audit M12)": (
        "kim2019",
        lambda d: (_p(d, "kim2019")["affiliations"].pop(5), _au(d, "kim2019", 4).update(markers=["P5"])),
        "names an author but is not recorded",
    ),
    "omitted pronoun statement (audit M13)": (
        "kim2019",
        lambda d: (
            _p(d, "kim2019")["affiliations"].pop(2),
            _au(d, "kim2019", 2).update(markers=["P2"]),
            _au(d, "kim2019", 5).update(markers=["P2"]),
        ),
        "names an author but is not recorded",
    ),
    "continuation dropped": (
        "jayatilleka2021",
        lambda d: _aff(d, "jayatilleka2021", 2).pop("continued"),
        "D354",
    ),
    "continuation not printed": (
        "jayatilleka2021",
        lambda d: _aff(d, "jayatilleka2021", 2).update(continued="Incorporated"),
        "continuation 'Incorporated' not printed",
    ),
    "slots_from_header with an author list": (
        "billah2018",
        lambda d: _p(d, "billah2018").update(slots_from_header=True),
        "has an author list",
    ),
    "ofc-style locator": ("billah2018", lambda d: _aff(d, "billah2018", 0).update(locator="p.~1 header"), "locator"),
    "dropped contact marker missing": (
        "ashida2017",
        lambda d: _au(d, "ashida2017", 1).pop("dropped_markers"),
        "printed markers differ",
    ),
    "campus not printed": (
        "tran2022",
        lambda d: _aff(d, "tran2022", 1).update(campus="Los Angeles"),
        "campus 'Los Angeles' not inside",
    ),
}


@needs_cache
@pytest.mark.parametrize("name", sorted(CASES))
def test_lit_mutation_is_caught(env: dict[str, Any], tmp_path: Path, name: str) -> None:
    code, mutate, expect = CASES[name]
    errors, _ = _run(env, tmp_path, mutate, only=code)
    assert any(expect in e for e in errors), (name, errors)


@needs_cache
def test_lit_rows(env: dict[str, Any], tmp_path: Path) -> None:
    """Grades, slots and the campus rule in the derived rows."""
    from photonics_atlas.csvio import read_csv

    errors, d = _run(env, tmp_path, None)
    assert errors == []
    rows = read_csv(d / "header_rows.csv")
    assert {r["evidence_grade"] for r in rows} == {"A"}
    assert all(r["source_id"].startswith("lit:") and r["locator"].startswith("p.1 ") for r in rows)
    ucsb = [r for r in rows if r["org_name"] == "University of California, Santa Barbara"]
    assert ucsb and all(r["org_ids"] == "org_ucsb" for r in ucsb)
    cmp = read_csv(d / "compare.csv")
    assert {r["outcome"] for r in cmp} == {"recorded"}
    assert len([r for r in cmp if r["source_id"] == "lit:virot2014"]) == 8
    order = {r["source_id"]: r["order_differs"] for r in cmp}
    assert order["lit:kim2019"] == "true" and order["lit:billah2018"] == "false"  # D363
    intel = [r for r in rows if r["source_id"] == "lit:jayatilleka2021" and r["aff_marker"] == "P3"]
    assert intel and all(r["org_name"] == "Intel Corporation" and r["locality"] == "Santa Clara" for r in intel)


def test_membership_designations_are_removed() -> None:
    oh = _load()
    t = oh._prep("Ada Example\n, Member, IEEE, Bea Sample, Senior Member, IEEE, Fellow, OSA,\nand Cy Test", False)
    assert "Member" not in t and "IEEE" not in t and "OSA" not in t
    t2 = oh._prep("Cy Test, Senior Member, IEEE, Fellow OSA. Dee Rest, Member IEEE", False)  # D364: no comma
    assert "Fellow" not in t2 and "OSA" not in t2 and "Member" not in t2
    assert "Ada Example" in t and "Bea Sample" in t and "Cy Test" in t


@needs_cache
def test_lit_author_lists(env: dict[str, Any]) -> None:
    meta = env["meta"]
    assert len(meta["billah2018"].authors) == 13
    assert len(meta["virot2014"].authors) == 8  # not in merged.jsonl: curator_adds.jsonl (D362)


@needs_cache
def test_slots_from_header_without_any_list(env: dict[str, Any], tmp_path: Path) -> None:
    """D352 stays for a paper with no author list in either file."""
    oh = env["oh"]
    meta = dict(env["meta"])
    meta["virot2014"] = oh.LitPaper("virot2014", [])
    errors, _ = _run({**env, "meta": meta}, tmp_path, None, only="virot2014")
    assert any("set slots_from_header" in e for e in errors), errors
    errors, _ = _run(
        {**env, "meta": meta},
        tmp_path / "b",
        lambda d: _p(d, "virot2014").update(slots_from_header=True),
        only="virot2014",
    )
    assert errors == [], errors


LIT = PILOT.parent
needs_batches = pytest.mark.skipif(not (LIT / "lit_h04" / "headers.yaml").exists(), reason="lit batches not extracted")

# D366-D369: (batch, paper, mutation or None = the committed record must be clean, expected error fragment)
D366: dict[str, tuple[str, str, Mut | None, str]] = {
    "cut: period after a name is no boundary (clean)": ("lit_h01", "elsaeed2024", None, ""),
    "cut: name before the period must carry the block": (
        "lit_h01",
        "elsaeed2024",
        lambda d: _au(d, "elsaeed2024", 15).update(markers=["P3"]),
        "carries no 'P2'",
    ),
    "structured more_orgs: wrong city": (
        "lit_h01",
        "elsaeed2024",
        lambda d: _aff(d, "elsaeed2024", 0)["more_orgs"][0].update(locality="Brussels"),
        "more_orgs locality 'Brussels' not inside",
    ),
    "clauses (clean)": ("lit_h03", "qi2024", None, ""),
    "postal box between unit and org (clean, D410)": ("lit_h10", "vandekerckhove2025", None, ""),
    "postal box token without a printed box code (D410)": (
        "lit_h10",
        "vandekerckhove2025",
        lambda d: _aff(d, "vandekerckhove2025", 2).pop("skip_between"),
        "D246",
    ),
    "body text 'and with' after the statement sentence (clean)": ("lit_h11", "zhang2023d", None, ""),
    "omitted clause is caught": (
        "lit_h03",
        "qi2024",
        lambda d: (_p(d, "qi2024")["affiliations"].pop(7), _au(d, "qi2024", 9).update(markers=["P6", "P7"])),
        "names an author but is not recorded",
    ),
    "clause recorded as a statement": (
        "lit_h03",
        "qi2024",
        lambda d: _aff(d, "qi2024", 1).pop("clause"),
        "D354",
    ),
    "skip_prefix (clean)": ("lit_h02", "jahed2022", None, ""),
    "skip_prefix missing": ("lit_h02", "jahed2022", lambda d: _aff(d, "jahed2022", 2).pop("skip_prefix"), "D354"),
    "skip_prefix not printed": (
        "lit_h02",
        "jahed2022",
        lambda d: _aff(d, "jahed2022", 2).update(skip_prefix="Western Gateway Building"),
        "D354",
    ),
    "glued present-address letter (clean)": ("lit_h02", "koninck2025", None, ""),
    "glued present-address letter as affiliation": (
        "lit_h02",
        "koninck2025",
        lambda d: _aff(d, "koninck2025", 3).update(role="affiliation"),
        "present-address cue",
    ),
    "per_author (clean)": ("lit_h02", "liang2025", None, ""),
    "per_author block on the wrong author": (
        "lit_h02",
        "liang2025",
        lambda d: (_au(d, "liang2025", 0).update(markers=["G2"]), _au(d, "liang2025", 1).update(markers=["G1"])),
        "D368",
    ),
    "grouped (clean)": ("lit_h03", "shamsansari2022", None, ""),
    "grouped author in the wrong group": (
        "lit_h03",
        "shamsansari2022",
        lambda d: _au(d, "shamsansari2022", 14).update(markers=["G3"]),
        "D368",
    ),
    "grouped with two names per org (clean)": ("lit_h02", "mu2026", None, ""),
    "skip_between (clean)": ("lit_h03", "sulway2023", None, ""),
    "skip_between missing": ("lit_h03", "sulway2023", lambda d: _aff(d, "sulway2023", 0).pop("skip_between"), "D246"),
    "skip_between not printed": (
        "lit_h03",
        "sulway2023",
        lambda d: _aff(d, "sulway2023", 0).update(skip_between="Western Gateway Building"),
        "D380",
    ),
    "cover page (clean)": ("lit_h03", "sheng2012", None, ""),
    "cover page searched from page 1": (
        "lit_h03",
        "sheng2012",
        lambda d: [a.update(locator="p.1 header") for a in _p(d, "sheng2012")["affiliations"]],
        "printed markers differ",
    ),
}


@needs_cache
@needs_batches
@pytest.mark.parametrize("name", sorted(D366))
def test_d366(env: dict[str, Any], tmp_path: Path, name: str) -> None:
    batch, code, mutate, expect = D366[name]
    errors, _ = _run(env, tmp_path, mutate, only=code, src=LIT / batch)
    if mutate is None:
        assert errors == [], errors
    else:
        assert any(expect in e for e in errors), (name, errors)


def test_strict_initials() -> None:
    """D369: lit slot matching needs every initial explained by the other name form."""
    oh = _load()
    assert not oh.strict_compatible("Siyuan Yu", "S. F. Yu")
    assert not oh.strict_compatible("M. B. Yu", "Ming Yu")
    assert oh.strict_compatible("S. H. Tao", "Shaohua Tao")
    assert oh.strict_compatible("D. L. Kwong", "Dim-Lee Kwong")
    assert oh.strict_compatible("H.-T. Peng", "Hsuan-Tung Peng")
    assert oh.compatible("Siyuan Yu", "S. F. Yu")  # the OFC rule is unchanged


@needs_cache
def test_show_page_separators(env: dict[str, Any]) -> None:
    t = env["oh"].lit_text("sheng2012", {1, 2}, sep=True)
    assert "----- text.md page 1 -----" in t and "----- text.md page 2 -----" in t
