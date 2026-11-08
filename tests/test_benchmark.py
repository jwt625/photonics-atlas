"""Tests for scripts/build_benchmark.py (DevLog-014): selection rules as pure functions, then the built view against
the repo tables and config/benchmark.yaml."""

from __future__ import annotations

import importlib.util
import sys
from functools import cache
from types import ModuleType
from typing import Any

import yaml

from photonics_atlas.paths import ROOT


def _mod() -> ModuleType:
    spec = importlib.util.spec_from_file_location("build_benchmark", ROOT / "scripts" / "build_benchmark.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["build_benchmark"] = mod  # dataclasses need the module registered
    spec.loader.exec_module(mod)
    return mod


bb = _mod()
CFG: dict[str, Any] = yaml.safe_load((ROOT / "config" / "benchmark.yaml").read_text(encoding="utf-8"))


def _cand(rank: float, basis: str = "measured", year: str = "2020", src: str = "lit:a") -> Any:
    return bb.Candidate("x.siph", rank, rank, None, "", basis, src, year)


def test_bounds_pointing_the_wrong_way_are_not_values() -> None:
    assert bb.bound_ok("lower", "lt") and bb.bound_ok("lower", "approx") and bb.bound_ok("lower", "")
    assert not bb.bound_ok("lower", "gt") and not bb.bound_ok("lower", "ge")
    assert bb.bound_ok("higher", "gt") and not bb.bound_ok("higher", "lt") and not bb.bound_ok("higher", "le")


def test_range_ranks_at_midpoint() -> None:  # D908
    assert bb.rank_value(1.3, 2.7) == 2.0
    assert bb.rank_value(0.5, None) == 0.5


def test_pick_order_value_then_basis_then_year() -> None:
    assert bb.pick([_cand(2.0), _cand(1.0)], "lower").rank == 1.0
    assert bb.pick([_cand(2.0), _cand(1.0)], "higher").rank == 2.0
    tie = [_cand(1.0, "derived"), _cand(1.0, "measured")]
    assert bb.pick(tie, "lower").basis == "measured"
    assert bb.pick([_cand(1.0, year="2019", src="lit:b"), _cand(1.0, year="2024")], "lower").year == "2024"


def test_telecom_window() -> None:
    row = {"wavelength": "telecom", "unknown_wavelength": "drop"}
    assert bb.in_window(CFG, row, 1550.0, "")
    assert not bb.in_window(CFG, row, 1064.0, "c_band")
    assert bb.in_window(CFG, row, None, "o_band")
    assert not bb.in_window(CFG, row, None, "")
    assert bb.in_window(CFG, {**row, "unknown_wavelength": "keep"}, None, "unspecified")
    assert bb.in_window(CFG, {"wavelength": "any"}, 780.0, "")


@cache
def _view() -> dict[str, Any]:
    return dict(bb.Builder(CFG).build())


def test_view_cells_follow_the_rules() -> None:
    view = _view()
    allowed = set(CFG["basis"]) | {bb.PRIVATE}
    cols = {c["id"] for c in view["columns"]}
    for cat in view["categories"]:
        for row in cat["rows"]:
            assert set(row["cells"]) <= cols
            for cell in row["cells"].values():
                assert cell["basis"] in allowed
                assert bb.bound_ok(row["better"], cell.get("q", ""))
                assert cell["source_id"] in view["sources"]


def test_thresholds_and_pinned_columns() -> None:  # D900, D902, D909
    view = _view()
    fill = {c["id"]: c["n_rows"] for c in view["columns"]}
    for c in view["columns"]:
        assert c.get("pinned") or fill[c["id"]] >= CFG["min_rows_per_column"]
    for p in CFG["pinned_columns"]:
        assert p in fill
    for cat in view["categories"]:
        for row in cat["rows"]:
            assert len(row["cells"]) >= CFG["min_columns_per_row"]


def test_private_values_are_marked() -> None:  # D910
    view = _view()
    cells = {(r["id"], c): v for cat in view["categories"] for r in cat["rows"] for c, v in r["cells"].items()}
    for pv in CFG["private_values"]:
        cell = cells.get((pv["row"], pv["column"]))
        if cell is None or cell["basis"] != bb.PRIVATE:
            continue  # a published value in the same cell won
        assert cell["date"] == pv["date"] and cell["source_id"] == f"pc:{pv['date']}"
        assert "url" not in view["sources"][cell["source_id"]]


def test_cumec_pd_uses_the_text_value() -> None:  # D911
    assert {"cmp_wu2025_ge_pd-m3", "cmp_wu2025_ge_pd-m4"} <= set(CFG["exclude_values"])
    pd = next(r for cat in _view()["categories"] for r in cat["rows"] if r["id"] == "pd_resp")
    cell = pd["cells"].get("cumec.siph")
    assert cell is None or (cell["v"] == 0.8 and cell.get("q") == "gt")


def test_family_overrides_name_existing_components_with_empty_platform() -> None:  # D914
    from photonics_atlas.csvio import read_csv

    comps = {r["component_id"]: r for r in read_csv(ROOT / "data" / "components" / "components.csv")}
    fams = {f["id"] for f in CFG["families"]}
    for cid, o in (CFG.get("family_override") or {}).items():
        assert cid in comps and comps[cid]["platform"] == "" and o["family"] in fams and o["why"]
