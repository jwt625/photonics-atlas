"""Build app/static/data/history.json, the input of the /history timeline (DevLog-016 D963, D974).

Inputs (read only): data/history/milestones.csv (merged milestone rows), data/_staging/literature/history_candidates.csv
(title, topic, venue, DOI, institutions, DRI, significance), data/registry/sources.csv (publication record) and
data/components/components.csv + component_metrics.csv (rows whose source is `lit:<paper_id>`: platform / core
material, class, metric count). Only values present in these files are emitted; empty stays empty.

Key figures come from licensed PDFs and are never published. `--figures` (local only) writes downscaled copies (max
900 px wide) of references/<paper_id>/figures/<key_figure_file> to app/static/data/history_figs/<paper_id>.png (git
ignored) and marks `has_local_figure`; without it every milestone has `has_local_figure: false`, so the committed view
never points at an image.

Usage: uv run python scripts/build_history_view.py [--figures] [--dry-run]
"""

from __future__ import annotations

import argparse
import importlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from photonics_atlas.csvio import read_csv
from photonics_atlas.paths import ROOT
from photonics_atlas.runlog import RunLog

MILESTONES = ROOT / "data" / "history" / "milestones.csv"
CANDIDATES = ROOT / "data" / "_staging" / "literature" / "history_candidates.csv"
SOURCES = ROOT / "data" / "registry" / "sources.csv"
COMPONENTS = ROOT / "data" / "components" / "components.csv"
METRICS = ROOT / "data" / "components" / "component_metrics.csv"
STATIC = ROOT / "app" / "static" / "data"
OUT = STATIC / "history.json"
FIGS = STATIC / "history_figs"
FIG_MAX_W = 900
NO_DEVICE = "theory / no device"

# Era intros copied from the DevLog-016 era table ("what changed"); no new claims here.
ERAS: list[dict[str, str]] = [
    {"id": "E0", "years": "1842-1959", "intro": "light guided in water jets and glass, field theory, dielectric-rod and metal waveguides at Bell Labs, coupled-wave theory, fiberscopes, maser"},
    {"id": "E1", "years": "1960-1969", "intro": "ruby / HeNe / Nd lasers, resonator and Gaussian-beam theory, SHG and parametric optics, diode lasers (four 1962 groups), heterostructure proposal, Kao-Hockham, Bell Labs integrated-optics program (Miller, Marcatili, Tien, Kogelnik)"},
    {"id": "E2", "years": "1970-1979", "intro": "20 dB/km then 0.2 dB/km fiber, MCVD / OVD / VAD, CW room-temperature DH lasers, DFB, Ti:LiNbO3, switched couplers, COBRA, MMI self-imaging, FBG, VCSEL concept, Si V-groove fiber arrays, first field systems"},
    {"id": "E3", "years": "1980-1989", "intro": "long-wavelength single-mode systems, QW / QD / strained lasers, QW electroabsorption, silica PLC at NTT, MT connector, phasar, EDFA, photonic bandgap, Si and SiN as waveguide materials"},
    {"id": "E4", "years": "1990-1999", "intro": "AWG and PLC products, QPM / PPLN, Tb/s WDM, MMI theory, thick-SOI ribs, Smart Cut, flip-chip MQW-on-CMOS I/O, microrings, PCF, photonic-crystal cavities and lasers, UTC-PD, Ge-on-Si"},
    {"id": "E5", "years": "2000-2009", "intro": "GHz Si modulators, Si Raman and hybrid lasers, grating couplers and tapers, CMOS photonics (Luxtera, imec), LN-on-insulator, frequency combs and microcombs, coherent DSP, waveguide quantum circuits"},
    {"id": "E6", "years": "2010-2020", "intro": "foundry Si photonics and PDKs, Ge lasers / detectors, QD lasers on Si, ultra-low-loss SiN, TFLN, soliton microcombs, PWB and printed micro-optics, MZI meshes, OPAs, nonreciprocal / Brillouin, parallel optical modules and CPO origins (TeraPHY, 45CLO)"},
]  # fmt: skip

# Grouping key for the institution color mode only (the printed affiliations are served unchanged).
INST_ALIAS = {"Bell Telephone Laboratories": "Bell Labs", "Bell Laboratories": "Bell Labs"}


# curation note some candidate rows start with; not viewer text (build_views.py viewer rules)
CURATION = re.compile(r"^Owner seed\.\s*")


def split_semi(s: str) -> list[str]:
    return [p.strip() for p in s.split(";") if p.strip()]


UNIT = re.compile(r"^(Department|Dept\.?|School|Faculty|Division|Group|Laboratory of|Lab of)\b", re.I)


def inst_key(name: str) -> str:
    """First comma part that is not a sub-unit, without parentheticals, e.g. 'Bell Laboratories, Holmdel' -> 'Bell Labs',
    'Department of Information Technology (INTEC), Ghent University' -> 'Ghent University'."""
    parts = [p.strip() for p in re.sub(r"\s*\([^)]*\)", "", name).split(",") if p.strip()]
    k = next((p for p in parts if not UNIT.match(p)), parts[0] if parts else "")
    return INST_ALIAS.get(k, k)


def write_figure(src: Path, dst: Path) -> None:
    pymupdf: Any = importlib.import_module("pymupdf")  # optional dependency (extra 'fetch'), only for --figures

    pix = pymupdf.Pixmap(str(src))
    if pix.colorspace and pix.colorspace.n > 3:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    if pix.width > FIG_MAX_W:
        pix = pymupdf.Pixmap(pix, FIG_MAX_W, round(pix.height * FIG_MAX_W / pix.width), None)
    dst.parent.mkdir(parents=True, exist_ok=True)
    pix.save(str(dst))


def build(root: Path = ROOT, figures: bool = False, log: RunLog | None = None) -> dict[str, Any]:
    def rel(p: Path) -> Path:
        return root / p.relative_to(ROOT)

    miles = read_csv(rel(MILESTONES))
    cands = {r["paper_id"]: r for r in read_csv(rel(CANDIDATES))}
    srcs = {r["source_id"]: r for r in read_csv(rel(SOURCES))}
    comps: dict[str, list[dict[str, str]]] = defaultdict(list)
    for c in read_csv(rel(COMPONENTS)):
        if c["source_id"].startswith("lit:"):
            comps[c["source_id"]].append(c)
    n_metric: Counter[str] = Counter(m["component_id"] for m in read_csv(rel(METRICS)))
    figs_dir = rel(FIGS)

    out: list[dict[str, Any]] = []
    for m in miles:
        pid = m["paper_id"]
        sid = m["source_id"] or f"lit:{pid}"
        cand = cands.get(pid, {})
        src = srcs.get(sid, {})
        rows = comps.get(sid, [])
        mats = Counter(c["platform"] or c["core_material"] for c in rows if c["platform"] or c["core_material"])
        insts = split_semi(cand.get("institutions", ""))
        printed = m["orgs_printed"]
        key0 = insts[0] if insts else (printed.split(";")[0] if printed else "")
        date = m["date"]
        year = date[:4] or src.get("year", "") or cand.get("year", "")
        has_fig = False
        if m["key_figure_file"] and figures:
            fsrc = root / "references" / pid / "figures" / m["key_figure_file"]
            if fsrc.is_file():
                write_figure(fsrc, figs_dir / f"{pid}.png")
                has_fig = True
            elif log:
                log.info(f"{pid}: key figure file not on this machine ({fsrc.relative_to(root)})")
        out.append(
            {
                "id": pid,
                "year": int(year) if year.isdigit() else None,
                "date": date,
                "era": m["era"].split(" ")[0] if m["era"] else cand.get("era", "").split(" ")[0],
                "thread": m["thread"] or cand.get("thread", ""),
                "topic": cand.get("topic", ""),
                "event": m["event"],
                "significance": CURATION.sub("", cand.get("significance", "")),
                "title": src.get("title", "") or cand.get("title", ""),
                "venue": src.get("venue", "") or cand.get("venue", ""),
                "doi": src.get("doi", "") or cand.get("doi", ""),
                "dri": m["dri"] or cand.get("dri", ""),
                "orgs_printed": printed,
                "institutions": insts,
                "inst": inst_key(key0) if key0 else "",
                "material": mats.most_common(1)[0][0] if mats else NO_DEVICE,
                "materials": sorted(mats),
                "components": [
                    {
                        "id": c["component_id"],
                        "class": c["class"],
                        "label": c["label"],
                        "n": n_metric[c["component_id"]],
                    }
                    for c in rows
                ],
                "n_metrics": sum(n_metric[c["component_id"]] for c in rows),
                "fig": (
                    {
                        "label": m["key_figure_label"],
                        "page": m["key_figure_page"],
                        "caption": m["key_figure_caption"],
                        "reason": m["key_figure_reason"],
                    }
                    if m["key_figure_label"]
                    else None
                ),
                "has_local_figure": has_fig,
            }
        )
    out.sort(key=lambda r: (r["date"] or str(r["year"] or 9999), r["id"]))
    return {"eras": ERAS, "milestones": out}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--figures", action="store_true", help="write local key-figure thumbnails (never committed)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    return write(figures=args.figures, dry_run=args.dry_run)


def write(figures: bool = False, dry_run: bool = False) -> int:
    with RunLog("build_history_view", dry_run) as log:
        view = build(figures=figures and not dry_run, log=log)
        ms = view["milestones"]
        log.info(f"milestones {len(ms)}; local figures {sum(m['has_local_figure'] for m in ms)}")
        if not dry_run:
            STATIC.mkdir(parents=True, exist_ok=True)
            OUT.write_text(json.dumps(view, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            log.info(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
