"""Build curated layouts: runs scripts/layouts/cells/*.py, writes app/static/data/layouts/<component_id>.json + index.json.

Each cell module defines build() -> Cell or list[Cell].  uv run python scripts/layouts/build.py [--only substring]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import ROOT, Cell  # noqa: E402

# DevLog-013 D510: views the source does not fix. A cell may compute them for checks; they are not published, because a
# drawing whose layout is a drafting guess is not a drawing of that device. Reviewed one by one; figures would lift these.
NO_FIG = "figures not available here; the text does not fix the layout"
NOT_DRAWN: dict[str, dict[str, str]] = {
    "cmp_ofc2026_th2a9_awg_16ch_1p6nm": {v: NO_FIG for v in ("top", "taper", "bends", "xsec")},
    "cmp_ofc2026_tu2d3_gc_1d_si": {v: NO_FIG for v in ("top", "grating", "section", "teeth")},
    "cmp_ofc2026_tu2d3_gc_1d_sin": {v: NO_FIG for v in ("top", "grating", "section", "teeth")},
    "cmp_ofc2026_tu2d3_si_sin_transition": {"top": NO_FIG},
    "cmp_ofc2026_tu2d4_si_sin_transition": {"top": NO_FIG},
    "cmp_ofc2026_tu2d3_sin_strip_wg": {"top": "no test structure in the text"},
    "cmp_ofc2026_tu2d4_sin_edge_coupler": {v: NO_FIG for v in ("top", "tip", "trans", "levels")},
    "cmp_ofc2026_tu2d4_tin_heater_ps": {"top": NO_FIG},
    "cmp_ofc2026_m1d2_single_section_dfb_600um": {v: NO_FIG for v in ("top", "xsec", "lsec", "grating")},
    "cmp_ofc2026_w1b3_soa_dfb_1p8mm": {v: NO_FIG for v in ("top", "xsec", "lsec", "grating")},
    "cmp_lit_mangal2020_downward_gc_reflector": {v: "the paper has no plan view of this grating" for v in ("top", "grating")},
    "cmp_ectc51909_2023_00230_rib_waveguide": {"top": "the paper shows no test structure"},
    "cmp_lit_song2024a_wg_2p5um": {"top": "the paper shows no test structure for this waveguide"},
    "cmp_lit_neutens2025_wg_w1000": {v: "the layout of this set is in a supplement not read here; the figure shown is a sibling set" for v in ("top", "centre", "arms", "width")},
    "cmp_lit_pathak2014_awg_8x400_grid1nm": {v: "the paper has no plan view of this device; its layout is known only from a different device of the same group" for v in ("top", "fan", "corner", "aperture")},
    "cmp_ofc2026_m1e6_sin_ring_r75um": {v: NO_FIG for v in ("top", "wide", "gap")},
    # audit 2026-11-04: a section extruded is not a plan view; the paper has no plan or axial drawing of the device
    "cmp_liu2026a_ge_pd": {v: "the paper has no plan view of this detector" for v in ("top", "input", "lsec")},
    "cmp_ectc51909_2023_00009_ge_pd": {v: "the paper has no labelled plan view of this detector" for v in ("top", "input")},
    "cmp_ofc2026_th3f1_ge_pd_w600_l40": {v: NO_FIG for v in ("top", "input")},
    "cmp_ofc2026_th3f3_ge_pd_w300_l10": {v: NO_FIG for v in ("top", "input", "lsec")},
    "cmp_lit_boust2020_dfb_laser": {v: "the epitaxial stack and grating are in a reference not read here" for v in ("xsec", "ridge", "lsec", "grating")},
}

OUT = ROOT / "app" / "static" / "data" / "layouts"
CELLS = Path(__file__).resolve().parent / "cells"


def write_atomic(path: Path, text: str) -> None:
    """Several cell authors build at once: a reader never sees a partial file."""
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    tmp.write_text(text)
    tmp.replace(path)


def load(path: Path) -> list[Cell]:
    spec = importlib.util.spec_from_file_location("cell_" + path.stem, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    got = mod.build()
    return got if isinstance(got, list) else [got]


def publishable(cell: Cell) -> dict[str, Any]:
    """The cell's output without its unpublished views (D510)."""
    out = cell.out()
    hide = NOT_DRAWN.get(cell.id, {})
    unknown = set(hide) - {v["id"] for v in out["views"]}
    if unknown:
        raise ValueError(f"{cell.id}: NOT_DRAWN names unknown views {sorted(unknown)}")
    shown = [v for v in out["views"] if v["id"] not in hide]
    for v in shown:
        if v.get("like") in hide:
            raise ValueError(f"{cell.id}: view {v['id']} reuses the unpublished view {v['like']}")
    out["views"] = shown
    if not shown:  # nothing published: no description of a drawing that is not there, no checks on it
        out["summary"] = ""
        out["checks"] = []
    out["not_drawn"] = sorted(set(hide.values()))
    if out["thumb"].get("view") in hide or not out["thumb"].get("view"):
        out["thumb"] = {}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="build only cell files whose name contains this")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    failed = 0
    built = 0
    for path in sorted(CELLS.glob("*.py")):
        if path.name.startswith("_") or args.only not in path.name:
            continue
        try:
            cells = load(path)
        except Exception as e:  # report every failing cell, not only the first
            print(f"FAIL {path.name}: {type(e).__name__}: {e}")
            failed += 1
            continue
        for cell in cells:
            raw = json.dumps(publishable(cell), separators=(",", ":"), ensure_ascii=False)
            write_atomic(OUT / f"{cell.id}.json", raw + "\n")
            n = sum(len(r) for v in cell.views if v.id not in NOT_DRAWN.get(cell.id, {}) for s in v.shapes for r in s["r"])
            print(f"ok   {cell.id}: {len(cell.views) - len(NOT_DRAWN.get(cell.id, {}))} views, {n} points, {len(raw) / 1024:.0f} KB; " + "; ".join(cell.checks))
            built += 1
    index = {}
    for f in sorted(OUT.glob("*.json")):
        if f.name == "index.json":
            continue
        d = json.loads(f.read_text())
        index[d["component_id"]] = {"sources": d["sources"], "summary": d["summary"], "drawn": bool(d["views"]), "not_drawn": d["not_drawn"]}
    write_atomic(OUT / "index.json", json.dumps(index, indent=1, ensure_ascii=False) + "\n")
    print(f"built {built}, failed {failed}, index {len(index)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
