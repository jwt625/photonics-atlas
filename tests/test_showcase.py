"""Showcase table rules (DevLog-005 D105): template must exist and serve the component's class."""

from __future__ import annotations

import shutil
from pathlib import Path

from photonics_atlas.csvio import read_csv, write_csv
from photonics_atlas.paths import ROOT
from photonics_atlas.schema import columns, load_layouts
from photonics_atlas.validate import validate


def _copy(tmp: Path) -> Path:
    for d in ("data/registry", "data/crosswalk", "data/components"):
        shutil.copytree(ROOT / d, tmp / d)
    return tmp


def _with_row(root: Path, **row: str) -> list[str]:
    path = root / "data" / "components" / "component_showcase.csv"
    rows = read_csv(path)
    rows.append({c: row.get(c, "") for c in columns("component_showcase")})
    write_csv(path, columns("component_showcase"), rows)
    return [e for e in validate(root).errors if e.startswith("component_showcase")]


def _component(cls: str) -> str:
    return next(
        r["component_id"] for r in read_csv(ROOT / "data" / "components" / "components.csv") if r["class"] == cls
    )


BASE = {"role": "typical", "criterion": "test", "rationale": "test", "selected_on": "2026-10-20"}


def test_templates_reference_registry_parameters() -> None:
    from photonics_atlas.schema import load_parameters

    params = load_parameters()["parameters"]
    for tid, t in load_layouts()["templates"].items():
        names = [p for view in ("top", "xsec") for k in ("required", "optional") for p in t[view][k]]
        assert all(p in params for p in names), tid
        assert t["primary"]["parameter"] in params, tid


def test_valid_row_passes(tmp_path: Path) -> None:
    root = _copy(tmp_path)
    assert _with_row(root, component_id=_component("splitter.mmi"), template="mmi", **BASE) == []


def test_unknown_template(tmp_path: Path) -> None:
    root = _copy(tmp_path)
    errs = _with_row(root, component_id=_component("splitter.mmi"), template="no_such_template", **BASE)
    assert any("unknown template" in e for e in errs)


def test_class_not_served(tmp_path: Path) -> None:
    root = _copy(tmp_path)
    errs = _with_row(root, component_id=_component("resonator.ring"), template="mmi", **BASE)
    assert any("not served by template" in e for e in errs)


def test_bad_role(tmp_path: Path) -> None:
    root = _copy(tmp_path)
    errs = _with_row(root, component_id=_component("splitter.mmi"), template="mmi", **{**BASE, "role": "best"})
    assert any("role" in e for e in errs)
