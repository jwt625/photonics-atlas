"""Build the foundry PDK benchmark view (DevLog-014): app/static/data/benchmark.json.

Columns are (foundry, platform family); rows are PDK building-block metrics; a cell is the best value among the metric
rows that pass the row's filters (config/benchmark.yaml, D900-D903). Inputs are read-only: data/components/,
data/registry/sources.csv, data/crosswalk/org_crosswalk.csv and the EO modulator atlas (config/inputs.yaml eo_atlas).
Ranking and emphasis are done by the renderer (app/src/lib/benchmark/render.js), which can rank across all columns or
within a family.

Usage: uv run python scripts/build_benchmark.py [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType
from typing import Any

import yaml

from photonics_atlas.csvio import read_csv, split_list
from photonics_atlas.paths import ROOT, input_path
from photonics_atlas.runlog import RunLog

CONFIG = ROOT / "config" / "benchmark.yaml"
OUT = ROOT / "app" / "static" / "data" / "benchmark.json"
BASIS_ORDER = {"measured": 0, "extracted_from_figure": 1, "derived": 2, "private_communication": 5}
PRIVATE = "private_communication"


def _load_views() -> ModuleType:
    spec = importlib.util.spec_from_file_location("build_views", ROOT / "scripts" / "build_views.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _num(s: str) -> float | None:
    try:
        return float(s) if s.strip() != "" else None
    except ValueError:
        return None


@dataclass
class Candidate:
    """One metric value that may fill a cell."""

    col: str
    rank: float  # the value, or the midpoint of a range (D908)
    value: float
    value_max: float | None
    qualifier: str
    basis: str
    source_id: str
    year: str
    info: dict[str, str] = field(default_factory=dict)


def in_window(cfg: dict[str, Any], row: dict[str, Any], wl: float | None, band: str) -> bool:
    """Telecom-window rule of a row (D902)."""
    if row.get("wavelength") != "telecom":
        return True
    lo, hi = cfg["telecom_window_nm"]
    if wl is not None:
        return bool(lo <= wl <= hi)
    if band and band != "unspecified":
        return band in cfg["telecom_bands"]
    return bool(row.get("unknown_wavelength", "keep") == "keep")


def bound_ok(better: str, qualifier: str) -> bool:
    """A bound pointing the wrong way is not an achieved value (D901): '> x' on lower-is-better, '< x' on higher."""
    if better == "lower":
        return qualifier not in ("gt", "ge")
    return qualifier not in ("lt", "le")


def rank_value(v: float, vmax: float | None) -> float:
    """Ranking value (D908): a range (spread over dies, channels or a band) ranks at its midpoint, not its best end."""
    return v if vmax is None else (v + vmax) / 2


def pick(cands: list[Candidate], better: str) -> Candidate:
    """Best candidate: rank value, then basis order (measured first), then newest year, then source id (stable)."""
    sign = 1.0 if better == "lower" else -1.0
    return min(cands, key=lambda c: (sign * c.rank, BASIS_ORDER.get(c.basis, 9), -int(c.year or 0), c.source_id))


class Builder:
    def __init__(self, cfg: dict[str, Any], root: Path = ROOT, eo_root: Path | None = None) -> None:
        self.cfg = cfg
        self.root = root
        views = _load_views()
        self.pubs = views.Pubs(root)
        self.plain_locator = views.plain_locator
        self.fam_of_platform: dict[str, str] = {}
        self.fam_of_eo_platform: dict[str, str] = {}
        self.fam_of_eo_material: dict[str, str] = {}
        self.eo_native: dict[str, set[str]] = {}
        for f in cfg["families"]:
            for p in f["platforms"]:
                self.fam_of_platform[p] = f["id"]
            for p in f["eo_platforms"]:
                self.fam_of_eo_platform[p] = f["id"]
            for m in f["eo_materials"]:
                self.fam_of_eo_material[m] = f["id"]
            self.eo_native[f["id"]] = set(f["eo_native"])
        self.unset_family: dict[str, str] = cfg.get("unset_platform_family") or {}
        self.family_override: dict[str, str] = {k: v["family"] for k, v in (cfg.get("family_override") or {}).items()}
        self.foundry_of_org: dict[str, str] = {}
        for fd in cfg["foundries"]:
            for o in fd["orgs"]:
                self.foundry_of_org[o] = fd["id"]
        self.org_name = {r["org_id"]: r["name"] for r in read_csv(root / "data" / "registry" / "organizations.csv")}
        self.comps = {r["component_id"]: r for r in read_csv(root / "data" / "components" / "components.csv")}
        self.metrics = read_csv(root / "data" / "components" / "component_metrics.csv")
        eo = eo_root or input_path("eo_atlas")
        self.eo_devices = read_csv(eo / "data" / "devices.csv")
        self.eo_papers = {r["paper_id"]: r for r in read_csv(eo / "data" / "papers.csv")}
        self.eo_org: dict[str, list[str]] = {}
        for r in read_csv(root / "data" / "crosswalk" / "org_crosswalk.csv"):
            if r["corpus"] == "eo":
                self.eo_org[r["printed"]] = split_list(r["org_ids"])
        self.exclude: dict[str, str] = cfg.get("exclude_values") or {}
        self.eo_exclude_integration = set(cfg.get("eo_exclude_integration") or [])
        # component wavelength fallback (D907): a metric row with no wavelength or band takes the wavelength span of
        # the component's other metric rows, so e.g. an AWG crosstalk row of a 1 um AWG is not read as telecom
        self.comp_wl: dict[str, list[float]] = defaultdict(list)
        for m in self.metrics:
            w = _num(m["wavelength_nm"])
            if w is not None:
                self.comp_wl[m["component_id"]].append(w)
        self.dropped: Counter[str] = Counter()
        self.col_meta: dict[str, dict[str, Any]] = defaultdict(
            lambda: {"orgs": Counter(), "processes": Counter(), "sources": set()}
        )

    # ---------- candidates ----------

    def _foundries(self, org_ids: list[str]) -> list[tuple[str, str]]:
        """(foundry id, org id) pairs of the candidate foundries among the org ids; merged orgs give one foundry."""
        seen: dict[str, str] = {}
        for o in org_ids:
            fid = self.foundry_of_org.get(o)
            if fid and fid not in seen:
                seen[fid] = o
        return list(seen.items())

    def component_candidates(self, row: dict[str, Any]) -> list[Candidate]:
        out: list[Candidate] = []
        classes = set(row["classes"])
        scopes = set(row.get("scopes") or [])
        excl = set(row.get("exclude_platforms") or [])
        allowed_basis = set(self.cfg["basis"])
        for m in self.metrics:
            if m["parameter"] != row["parameter"]:
                continue
            c = self.comps.get(m["component_id"])
            if not c or c["class"] not in classes:
                continue
            why = self._component_reject(row, m, c, scopes, excl, allowed_basis)
            if why:
                self.dropped[f"{row['id']}:{why}"] += 1
                continue
            fam = self._family(c)
            v = _num(m["value"])
            assert v is not None
            vmax = _num(m["value_max"])
            for fid, org in self._foundries(split_list(c["fab_org_ids"])):
                col = f"{fid}.{fam}"
                info = {
                    "org": self.org_name.get(org, org),
                    "component": self.pubs.scrub(c["label"]),
                    "platform": c["platform"],
                    "core": self.pubs.scrub(c["core_material"]),
                    "process": self.pubs.scrub(c["process_name"]),
                    "condition": self.pubs.scrub(m["condition"]),
                    "scope": m["scope"],
                    "wavelength_nm": m["wavelength_nm"],
                    "band": m["band"],
                    "polarization": m["polarization"],
                    "statistic": m["statistic"],
                    "temperature_k": m["temperature_k"],
                    "bias_v": m["bias_v"],
                    "method": m["method"],
                    "locator": self.plain_locator(m["locator"]),
                }
                year = self.pubs.src.get(c["source_id"], {}).get("year", "")
                out.append(
                    Candidate(col, rank_value(v, vmax), v, vmax, m["qualifier"], m["basis"],
                              c["source_id"], year, {k: x for k, x in info.items() if x})
                )
                self._note_col(col, org, c["process_name"], c["source_id"])
        return out

    def _component_reject(self, row: dict[str, Any], m: dict[str, str], c: dict[str, str], scopes: set[str],
                          excl: set[str], allowed_basis: set[str]) -> str:
        if m["metric_id"] in self.exclude:
            return "excluded"
        if c["row_kind"] != "fabricated":
            return "row_kind"
        if m["basis"] not in allowed_basis:
            return f"basis_{m['basis']}"
        if m["statistic"] == "std":
            return "std"
        if _num(m["value"]) is None:
            return "no_value"
        if not self._family(c) or c["platform"] in excl:
            return "platform"
        if scopes and m["scope"] not in scopes:
            return f"scope_{m['scope'] or 'empty'}"
        if not bound_ok(row["better"], m["qualifier"]):
            return "bound"
        t = _num(m["temperature_k"])
        if t is not None and t < self.cfg["min_temperature_k"]:
            return "cryogenic"
        if not in_window(self.cfg, row, _num(m["wavelength_nm"]), m["band"]):
            return "wavelength"
        sib = self.comp_wl.get(m["component_id"], [])
        if not m["wavelength_nm"] and (not m["band"] or m["band"] == "unspecified") and sib:
            if not all(in_window(self.cfg, row, w, "") for w in sib):
                return "wavelength_component"
        if not self._foundries(split_list(c["fab_org_ids"])):
            return "not_a_foundry_column"
        return ""

    def _family(self, c: dict[str, str]) -> str:
        if c["component_id"] in self.family_override:
            return self.family_override[c["component_id"]]
        if c["platform"]:
            return self.fam_of_platform.get(c["platform"], "")
        return self.unset_family.get(c["class"], "")

    def _eo_family(self, d: dict[str, str]) -> str:
        if d["waveguide_platform"]:
            return self.fam_of_eo_platform.get(d["waveguide_platform"], "")
        return self.fam_of_eo_material.get(d["eo_material"], "")

    def eo_candidates(self, row: dict[str, Any]) -> list[Candidate]:
        out: list[Candidate] = []
        allowed_basis = set(self.cfg["basis"])
        for d in self.eo_devices:
            if d["device_class"] not in row["device_classes"]:
                continue
            v = _num(d[row["field"]])
            if v is None:
                continue
            p = self.eo_papers.get(d["paper_id"], {})
            orgs: list[str] = []
            for printed in (p.get("foundry_or_fab") or "").split(";"):
                orgs += self.eo_org.get(printed.strip(), [])
            fam = self._eo_family(d)
            why = ""
            if f"{d['device_id']}:{row['field']}" in self.exclude:
                why = "excluded"
            elif d["row_kind"] != "device":
                why = "row_kind"
            elif d["integration"] in self.eo_exclude_integration:
                why = "integration"
            elif d[row["basis_field"]] not in allowed_basis:
                why = f"basis_{d[row['basis_field']] or 'empty'}"
            elif d["statistic"] == "std":
                why = "std"
            elif not fam:
                why = "platform"
            elif d["eo_material"] not in self.eo_native[fam]:
                why = "not_native"
            elif d["temperature_class"] == "cryogenic" or (
                (_num(d["temperature_k"]) or 999.0) < self.cfg["min_temperature_k"]
            ):
                why = "cryogenic"
            elif not in_window(self.cfg, row, _num(d["wavelength_nm"]), d["band"]):
                why = "wavelength"
            elif not self._foundries(orgs):
                why = "not_a_foundry_column"
            if why:
                self.dropped[f"{row['id']}:{why}"] += 1
                continue
            sid = f"eo:{d['paper_id']}"
            year = p.get("year", "")
            for fid, org in self._foundries(orgs):
                col = f"{fid}.{fam}"
                info = {
                    "org": self.org_name.get(org, org),
                    "component": self.pubs.scrub(d["device_label"]),
                    "platform": d["waveguide_platform"],
                    "effect": d["eo_material"].replace("_", " "),
                    "process": self.pubs.scrub(p.get("process_name", "")),
                    "convention": d["vpi_convention"].replace("_", " ") if row["field"].startswith("vpi") else "",
                    "length_mm": d["length_mm"],
                    "wavelength_nm": d["wavelength_nm"],
                    "band": d["band"],
                    "bw_reference": d["bw3db_reference"] if row["field"] == "bw3db_ghz" else "",
                    "statistic": d["statistic"],
                    "locator": "device record (EO modulator atlas)",
                }
                out.append(Candidate(col, v, v, None, "", d[row["basis_field"]], sid, year,
                                     {k: x for k, x in info.items() if x}))
                self._note_col(col, org, p.get("process_name", ""), sid)
        return out

    def private_candidates(self, row: dict[str, Any]) -> list[Candidate]:
        """Values from private communication (config `private_values`, D910): unpublished, marked in the view, ranked
        like any value. A value whose column or bound does not fit the row is an error in the config, not a drop."""
        out: list[Candidate] = []
        fd_label = {f["id"]: f["label"] for f in self.cfg["foundries"]}
        for pv in self.cfg.get("private_values") or []:
            if pv["row"] != row["id"]:
                continue
            fid, fam = pv["column"].split(".")
            if fid not in fd_label or fam not in self.eo_native:
                raise ValueError(f"private_values: unknown column {pv['column']}")
            q = pv.get("qualifier", "")
            if not bound_ok(row["better"], q):
                raise ValueError(f"private_values: bound {q} on {row['id']} points the wrong way")
            v = float(pv["value"])
            vmax = float(pv["value_max"]) if pv.get("value_max") is not None else None
            sid = f"pc:{pv['date']}"
            info = {"org": fd_label[fid], "component": pv["component"], "scope": pv.get("scope", ""),
                    "band": pv.get("band", ""), "locator": f"private communication, {pv['date']}"}
            out.append(Candidate(pv["column"], rank_value(v, vmax), v, vmax, q, PRIVATE, sid, pv["date"][:4],
                                 {k: x for k, x in info.items() if x}))
            self.col_meta[pv["column"]]["sources"].add(sid)
        return out

    def _note_col(self, col: str, org: str, process: str, sid: str) -> None:
        meta = self.col_meta[col]
        meta["orgs"][self.org_name.get(org, org)] += 1
        if process:
            meta["processes"][self.pubs.scrub(process)] += 1
        meta["sources"].add(sid)

    # ---------- view ----------

    def build(self) -> dict[str, Any]:
        rows_out: list[tuple[str, dict[str, Any]]] = []
        for cat in self.cfg["categories"]:
            for row in cat["rows"]:
                cands = self.eo_candidates(row) if row["source"] == "eo" else self.component_candidates(row)
                cands += self.private_candidates(row)
                by_col: dict[str, list[Candidate]] = defaultdict(list)
                for c in cands:
                    by_col[c.col].append(c)
                cells: dict[str, dict[str, Any]] = {}
                for col, cs in by_col.items():
                    best = pick(cs, row["better"])
                    cell: dict[str, Any] = {"r": best.rank, "v": best.value, "basis": best.basis, "source_id": best.source_id,
                                            "n": len(cs), "n_src": len({c.source_id for c in cs}), **best.info}
                    if best.value_max is not None:
                        cell["vmax"] = best.value_max
                    if best.qualifier:
                        cell["q"] = best.qualifier
                    if best.basis == PRIVATE:
                        cell["date"] = best.source_id.removeprefix("pc:")
                    cells[col] = cell
                rows_out.append((cat["id"], {"row": row, "cells": cells}))

        # thresholds (D900, D902): drop thin columns, then thin rows; repeat until stable. Pinned columns (D909) are
        # always shown, filled or not, and count toward a row's column threshold like any shown column.
        pinned = list(self.cfg.get("pinned_columns") or [])
        cols = {c for _, r in rows_out for c in r["cells"]} | set(pinned)
        rows_keep = list(rows_out)
        while True:
            fill = Counter(c for _, r in rows_keep for c in r["cells"] if c in cols)
            cols2 = {c for c in cols if fill[c] >= self.cfg["min_rows_per_column"] or c in pinned}
            rows2 = [(k, r) for k, r in rows_keep
                     if sum(1 for c in r["cells"] if c in cols2) >= self.cfg["min_columns_per_row"]]
            if cols2 == cols and len(rows2) == len(rows_keep):
                break
            cols, rows_keep = cols2, rows2

        fam_order = [f["id"] for f in self.cfg["families"]]
        fd_order = [f["id"] for f in self.cfg["foundries"]]
        fd_label = {f["id"]: f["label"] for f in self.cfg["foundries"]}
        fill = Counter(c for _, r in rows_keep for c in r["cells"] if c in cols)

        def col_key(c: str) -> tuple[int, int, str]:
            fid, fam = c.split(".")
            return (fam_order.index(fam), -fill[c], fid)

        columns = []
        for c in sorted(cols, key=col_key):
            fid, fam = c.split(".")
            meta = self.col_meta[c]
            columns.append({
                "id": c, "family": fam, "foundry": fid, "label": fd_label[fid],
                "orgs": [o for o, _ in meta["orgs"].most_common()],
                "processes": [p for p, _ in meta["processes"].most_common(4)],
                "n_rows": fill[c],
                **({"pinned": True} if c in pinned else {}),
            })
        _ = fd_order
        used_sources: set[str] = set()
        private_sources: set[str] = set()
        categories = []
        for cat in self.cfg["categories"]:
            rows = []
            for k, r in rows_keep:
                if k != cat["id"]:
                    continue
                row = r["row"]
                cells = {c: v for c, v in r["cells"].items() if c in cols}
                used_sources |= {v["source_id"] for v in cells.values() if v["basis"] != PRIVATE}
                private_sources |= {v["source_id"] for v in cells.values() if v["basis"] == PRIVATE}
                rows.append({
                    "id": row["id"], "label": row["label"], "unit": row["unit"], "better": row["better"],
                    "fmt": row.get("fmt", "auto"), "sub": row["sub"], "note": row["note"], "cells": cells,
                })
            if rows:
                categories.append({"id": cat["id"], "label": cat["label"], "rows": rows})
        all_rows = {r["row"]["id"] for _, r in rows_out}
        shown = {r["id"] for c in categories for r in c["rows"]}
        return {
            "generated_on": dt.date.today().isoformat(),
            "families": [{k: f[k] for k in ("id", "label", "tip")} for f in self.cfg["families"]
                         if any(c["family"] == f["id"] for c in columns)],
            "columns": columns,
            "categories": categories,
            "sources": {**self.pubs.records(used_sources),
                        **{s: {"title": "Private communication (unpublished)", "year": s[3:7]}
                           for s in sorted(private_sources)}},
            "rules": {
                "basis": self.cfg["basis"],
                "min_rows_per_column": self.cfg["min_rows_per_column"],
                "min_columns_per_row": self.cfg["min_columns_per_row"],
                "telecom_window_nm": self.cfg["telecom_window_nm"],
                "min_temperature_k": self.cfg["min_temperature_k"],
            },
            "rows_not_shown": sorted(all_rows - shown),
        }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    with RunLog("build_benchmark", args.dry_run) as log:
        b = Builder(cfg)
        view = b.build()
        for k, n in sorted(b.dropped.items()):
            log.event("dropped", reason=k, n=n)
        log.info(f"columns {len(view['columns'])}: {', '.join(c['id'] + '(' + str(c['n_rows']) + ')' for c in view['columns'])}")
        for cat in view["categories"]:
            for r in cat["rows"]:
                log.info(f"row {r['id']}: {len(r['cells'])} cells")
                log.event("row", id=r["id"], cells={c: [v["r"], v["source_id"], v["n"]] for c, v in r["cells"].items()})
        log.info(f"rows not shown: {view['rows_not_shown']}; sources {len(view['sources'])}")
        if not args.dry_run:
            OUT.write_text(json.dumps(view, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            log.info(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
