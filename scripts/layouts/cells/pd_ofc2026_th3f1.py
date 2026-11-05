"""OFC 2026 Th3F.1 Ge lateral P-i-N PD in recessed Si, w 600 nm, L 40 um. Text and captions only: Fig. 1(a)-(c) not available.

What the text fixes: lateral Si / i-Ge / Si diode; Ge epitaxy in selected areas through an oxide mask, embedded by a recess
etch in the 220 nm SOI waveguide; separate high-dose implants for the junction regions and for the contact regions of each
polarity; 3 um BOX; SiO2 cladding; two metal levels; butt coupling from the Si waveguide; grating coupler input. All other
geometry is assumed, drawn dashed and carries no dimension.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, assumed, row, stated  # noqa: E402

ID = "cmp_ofc2026_th3f1_ge_pd_w600_l40"


def build() -> Cell:
    c = Cell(
        ID,
        ["Text and captions only: Fig. 1(a) schematic, 1(b) TEM, 1(c) micrograph not available", "Sec. 2", "Sec. 3"],
        "Lateral P-i-N in recessed Si: Ge size, Si and BOX stated; recess depth, doping extents, contacts, metal outline assumed",
    )
    w_ge = c.um("m10")
    l_ge = c.um("m11")
    t_si = c.um("m12")
    t_box = c.um("m13")

    why = "Fig. 1 not available and the text gives no value"
    t_ge = 0.35  # no stated thickness
    z_bot = 0.08  # no stated recess depth
    e_j, e_c = 1.0, 2.2  # junction and contact implant edges
    v_u, v_w = 1.7, 0.35  # contact position and width
    h1, t1, h2, t2 = 0.8, 0.4, 0.5, 0.6  # V1, M1, V2, M2
    z_v1 = t_si + h1
    z_m1 = z_v1 + t1
    z_m2 = z_m1 + h2 + t2

    x = c.view("xsec", "cross-section at mid Ge (text only)", "xsec")
    u1 = e_c + 0.5
    x.rect(-u1, -t_box - 0.5, u1, -t_box, "si", "Si substrate", assumed("truncated"), alpha=0.6, layer="substrate")
    x.rect(-u1, -t_box, u1, 0, "sio2", "buried oxide", row("m13"), layer="oxide")
    x.rect(-u1, 0, u1, z_m2 + 0.3, "sio2", "SiO2 cladding", stated("p.1 Sec. 2", "SiO2 cladding") + assumed(f"thickness: {why}"), alpha=0.4, layer="oxide")
    x.rect(-w_ge / 2, 0, w_ge / 2, z_bot, "si", "Si under the recess", row("m12") + assumed(f"recess depth: {why}"), layer="waveguide")
    for s, name, mat in ((-1, "P", "doped_p"), (1, "N", "doped_n")):
        a, b = sorted((s * w_ge / 2, s * e_j))
        x.rect(a, 0, b, t_si, mat, f"{name} junction implant", stated("p.1 Sec. 2", "B / P implant forms the junctions") + row("m12") + assumed(f"extent: {why}"), layer="doped", alpha=0.55)
        a2, b2 = sorted((s * e_j, s * e_c))
        x.rect(a2, 0, b2, t_si, mat, f"{name} contact implant", stated("p.1 Sec. 2", "B / P implant forms the contact regions") + row("m12") + assumed(f"extent: {why}"), layer="doped")
        vc = s * v_u
        x.rect(vc - v_w / 2, t_si, vc + v_w / 2, z_v1, "contact", f"contact on {name}", assumed(f"size: {why}"), layer="via")
        a3, b3 = sorted((s * e_j, s * e_c))
        x.rect(a3, z_v1, b3, z_m1, "metal", f"metal 1 ({name})", stated("p.1 Sec. 2", "two-layer BEOL") + assumed(f"outline and thickness: {why}"), layer="metal")
        x.rect(vc - v_w / 2, z_m1, vc + v_w / 2, z_m1 + h2, "contact", f"via 2 ({name})", assumed(f"size: {why}"), layer="via")
        x.rect(a3, z_m1 + h2, b3, z_m2, "metal", f"metal 2 ({name})", stated("p.1 Sec. 2", "two-layer BEOL") + assumed(f"outline and thickness: {why}"), layer="metal")
        x.label((s * (e_j + w_ge / 2) / 2, t_si / 2), name)
        x.label((s * (e_c + e_j) / 2, t_si / 2), f"{name}+")
        x.label((s * (e_c + e_j) / 2, z_m1), "M1", dy=-5)
        x.label((s * (e_c + e_j) / 2, z_m2), "M2", dy=-5)
    x.rect(-w_ge / 2, z_bot, w_ge / 2, z_bot + t_ge, "ge", "intrinsic Ge, width from the row", row("m10") + assumed(f"thickness and recess depth: {why}; the text only places its base inside the 220 nm Si"), layer="absorber")
    x.label((0, z_bot + t_ge), "Ge", dy=-6)
    x.label((0, -t_box / 2), "buried oxide")
    x.dim("h", -w_ge / 2, w_ge / 2, z_bot + t_ge, px=24, ext=(z_bot + t_ge, z_bot + t_ge), row_id="m10")
    x.dim("v", 0, t_si, -e_c, px=-14, ext=(-e_c, -e_c), row_id="m12")
    x.dim("v", -t_box, 0, u1, px=-14, ext=(u1, u1), row_id="m13")
    x.note("Text and captions only (Fig. 1 not available): dashed geometry is a placeholder for the topology the text states, not the paper's dimensions.")
    x.note("P on the left is arbitrary; the text does not fix the polarity side. Simulated mode overlap with the Ge about 80 % (Sec. 3).")

    d = c.view("ge", "detail: Ge in the Si recess", "xsec", like="xsec", window=(-1.2, -0.1, 1.2, 0.65))
    d.dim("h", -w_ge / 2, w_ge / 2, z_bot + t_ge, px=20, ext=(z_bot + t_ge, z_bot + t_ge), row_id="m10")
    d.label((0, z_bot + t_ge / 2), "Ge")
    d.label((-0.75, t_si / 2), "P")
    d.label((0.75, t_si / 2), "N")

    top = c.view("top", "top view (text only): diode extruded along the stated length")
    src_plan = assumed("Fig. 1(a), 1(c) not available: extents along the device and the plan of implants, contacts and metal are not stated")
    for s, name, mat in ((1, "P", "doped_p"), (-1, "N", "doped_n")):
        a, b = sorted((s * w_ge / 2, s * e_j))
        top.rect(0, a, l_ge, b, mat, f"{name} junction implant", src_plan, layer="doped", alpha=0.55)
        a2, b2 = sorted((s * e_j, s * e_c))
        top.rect(0, a2, l_ge, b2, mat, f"{name} contact implant", src_plan, layer="doped")
        top.rect(0, s * v_u - v_w / 2, l_ge, s * v_u + v_w / 2, "contact", f"contact line on {name}", src_plan, layer="via")
        top.rect(0, a2, l_ge, b2, "metal", f"metal over {name}", src_plan, layer="metal", alpha=0.4)
    wg = Route((-8.0, 0.0), 0.0, 0.45)
    wg.straight(3.0).taper(5.0, w_ge)
    top.route(wg, "si", "Si waveguide from the grating coupler", stated("p.1 Sec. 3", "C-band grating coupler input; waveguide butts against the Ge") + assumed(f"waveguide width and taper: {why}"), layer="waveguide")
    top.rect(0, -w_ge / 2, l_ge, w_ge / 2, "ge", "Ge", row("m10", "m11"), layer="absorber")
    top.dim("h", 0, l_ge, -e_c, px=-16, ext=(-w_ge / 2, -e_c), row_id="m11")
    top.label((l_ge / 2, 0), "Ge", dy=-5)
    top.label((-8.0, 0), "from GC", anchor="end", dx=-4, tip="Grating coupler truncated")
    top.note("Fig. 1(c) micrograph not available: pads, metal routing and footprint are not drawn. The diode was probed with a 110 GHz LCA, so RF pads exist but their layout is not stated.")
    c.thumb = {"view": "xsec"}

    t2_ = c.view("input", "detail: input end (text only)", like="top", window=(-9.0, -2.8, 5.0, 2.8))
    t2_.dim("v", -w_ge / 2, w_ge / 2, 2.0, px=0, ext=(2.0, 2.0), row_id="m10")
    t2_.label((3.5, 0.8), "P")
    t2_.label((3.5, -0.8), "N")
    t2_.label((3.5, 1.6), "P+")
    t2_.label((3.5, -1.6), "N+")

    ls = c.view("lsec", "section along the axis: butt coupling from the Si waveguide (text only)", "xsec")
    x0, x1 = -2.5, 3.5
    ls.rect(x0, -t_box - 0.3, x1, -t_box, "si", "Si substrate", assumed("truncated"), alpha=0.6, layer="substrate")
    ls.rect(x0, -t_box, x1, 0, "sio2", "buried oxide", row("m13"), layer="oxide")
    ls.rect(x0, 0, x1, 0.9, "sio2", "SiO2 cladding", stated("p.1 Sec. 2") + assumed("thickness"), alpha=0.4, layer="oxide")
    ls.rect(x0, 0, 0, t_si, "si", "Si waveguide", row("m12"), layer="waveguide")
    ls.rect(0, 0, x1, z_bot, "si", "Si under the recess", row("m12") + assumed(f"recess depth: {why}"), layer="waveguide")
    ls.rect(0, z_bot, x1, z_bot + t_ge, "ge", "Ge", assumed(f"thickness, recess depth, end wall: {why}"), layer="absorber")
    ls.dim("v", 0, t_si, x0, px=-14, ext=(x0, x0), row_id="m12")
    ls.label((-1.25, t_si / 2), "Si waveguide")
    ls.label((1.75, z_bot + t_ge / 2), "Ge")
    ls.note("Ge continues to its stated 40 um length (truncated).")
    return c
