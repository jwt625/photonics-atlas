"""Naraine 2024 1x2 SiO2-clad SiN MMI, 3.9 x 10 um (Fig. 6(a) inset SEM with 5 um bar, Fig. 2(d), Table I, Sec. II, III-C).

Topology and port shapes from the SEM: one centred input, two outputs, wide ends at the MMI with a clear shoulder to the
wall, all tapers with parallel axes and still narrowing at the frame edge. By its 5 um bar (151 image px, 30.2 px/um) the
inset reads L 10.2 um (row 10) and W 4.5 um (row 3.9). The rows are drawn; widths are ratios to W, lengths ratios to L, and
every label gives both scales.
Past the frame the paper shows nothing: only the text mentions sine bends. Those stubs are assumed.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, assumed, fig, row, stated  # noqa: E402

ID = "cmp_lit_naraine2024_mmi_1x2"


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 6(a) inset SEM", "Fig. 2(d)", "Table I", "Sec. II-A, II-B", "Sec. III-A", "Sec. III-C"],
        "1x2 MMI: tapers as in the SEM; sine bends past the SEM frame are assumed",
    )
    w = c.um("m3")
    lm = c.um("m4")
    t = c.um("m7")
    off = w / 4  # 1x2 symmetric images; SEM centre to centre 70 of W 136 px
    # SEM readings in the embedded image, bright-edge centroids: W 136 px, L 308 px, bar 5 um = 151 px
    px_w, px_l, px_um = 136.0, 308.0, 151.0 / 5.0
    w_in0, w_in1 = 40.4 / px_w * w, 30.5 / px_w * w
    l_in = 186 / px_l * lm
    w_out0, w_out1 = 33.0 / px_w * w, 22.5 / px_w * w
    l_out = 190 / px_l * lm
    box, clad = 4.5, 3.0  # Sec. II
    angle = 83.5  # Sec. III-A sidewall; designed width at half height

    src_in = row("m3", "m4") + fig("Fig. 6(a) inset", "input taper width by ratio to W, length by ratio to L", "10 %")
    src_out = row("m3", "m4") + fig("Fig. 6(a) inset", "output taper width by ratio to W, length by ratio to L, centres at W/4", "10 %")
    src_sb = assumed("beyond the SEM frame: the text mentions tapers and sine bends, without dimensions")

    top = c.view("top", "top view: 1x2 MMI; dashed past the SEM frame")
    tin = Route((0.0, 0.0), 180.0, w_in0, tol=0.005)
    tin.straight(l_in, w_in1)
    top.route(tin, "sin", "input taper", src_in, layer="waveguide")
    sin_stub = Route(tin.pos, 180.0, w_in1, tol=0.005)
    sin_stub.straight(30.0)
    top.route(sin_stub, "sin", "input access", src_sb, layer="waveguide")
    top.rect(0, -w / 2, lm, w / 2, "sin", "multimode region", row("m3", "m4") + fig("Fig. 6(a) inset", "rectangle with a shoulder at every port"), layer="waveguide")
    ends = {}
    for sign in (1, -1):
        rt = Route((lm, sign * off), 0.0, w_out0, tol=0.005)
        rt.straight(l_out, w_out1)
        top.route(rt, "sin", "output taper", src_out, layer="waveguide")
        sb = Route(rt.pos, 0.0, w_out1, tol=0.005)
        sb.sbend(50.0, sign * 4.0).straight(10.0)
        top.route(sb, "sin", "output sine bend", src_sb, layer="waveguide")
        ends[sign] = sb
    top.label(sin_stub.pos, "in", anchor="start", dy=-8)
    top.label(ends[1].pos, "out 1", anchor="end", dy=-8)
    top.label(ends[-1].pos, "out 2", anchor="end", dy=16)
    top.dim("h", 0, lm, w / 2, px=14, ext=(w / 2, w / 2), row_id="m4")
    top.note(f"Fig. 6(a) inset by its 5 um bar (30.2 px/um): L {px_l / px_um:.1f} um, W {px_w / px_um:.1f} um; the rows are 10 and 3.9 um. Rows drawn; widths scale with W, lengths with L. Labels give the row-scaled width and the bar reading.")
    top.note("The inset of Fig. 6(a) shows only the MMI and about 6 um of each taper. Access waveguides past it are drafting stubs, at the width read at the frame edge.")
    c.thumb = {"view": "top", "window": [-l_in - 2, -5, lm + l_out + 2, 5]}

    sem = c.view("sem", "detail: the frame of the SEM inset of Fig. 6(a)", like="top", window=(-l_in, -3.27, lm + l_out, 3.27))
    sem.dim("h", 0, lm, w / 2, px=12, ext=(w / 2, w / 2), row_id="m4")
    sem.dim("v", -w / 2, w / 2, lm, px=-12, ext=(lm, lm), row_id="m3")

    def both(px: float) -> str:
        return f"{px / px_w * w:.2f} um by ratio to row W, {px / px_um:.2f} um by the 5 um bar"

    sem.label((-l_in, -w_in0 / 2), f"input taper {w_in0:.2f} to {w_in1:.2f} um (bar {40.4 / px_um:.2f} to {30.5 / px_um:.2f})", anchor="start", dy=36, tip=f"Fig. 6(a) inset, MMI end: {both(40.4)}; frame edge: {both(30.5)}; 1 px each")

    pv = c.view("ports", "detail: output tapers at the MMI", like="top", window=(lm - 1.5, -2.6, lm + l_out, 2.6))
    pv.dim("v", off - w_out0 / 2, off + w_out0 / 2, lm + 0.3, px=-14, ext=(lm + 0.3, lm + 0.3), text=f"{w_out0:.2f} um (bar {33.0 / px_um:.2f})", src=fig("Fig. 6(a) inset", both(33.0), "1 px"))
    pv.label((lm + l_out - 0.6, off + w_out1 / 2), f"{w_out1:.2f} um (bar {22.5 / px_um:.2f}) at the frame edge", anchor="end", dy=-10, tip=f"Fig. 6(a) inset: {both(22.5)}; 1 px")
    pv.dim("v", -off, off, lm + 2.4, px=6, ext=(lm + 2.4, lm + 2.4), text=f"{2 * off:.2f} um (bar {70 / px_um:.2f})", src=row("m3") + fig("Fig. 6(a) inset", f"drawn at W/2; reads {70 / px_w * w:.2f} um by ratio to row W, {70 / px_um:.2f} um by the 5 um bar", "1 px"))

    # cross-section at the middle of the MMI, sidewall 83.5 deg, width at half height
    dw = (t / 2) / math.tan(math.radians(angle))
    half = 4.0
    x = c.view("xsec", "cross-section: multimode region, oxide clad", "xsec")
    x.rect(-half, -box - 0.8, half, -box, "si", "Si substrate", assumed("handle thickness not stated: truncated"), layer="substrate", alpha=0.5)
    x.rect(-half, -box, half, 0, "sio2", "thermal SiO2", stated("p.3 Sec. II-A", "4.5 um"), layer="oxide")
    x.rect(-half, 0, half, clad, "sio2", "PECVD SiO2", stated("p.4 Sec. II-B", "3 um"), layer="oxide", alpha=0.45)
    x.poly([(-w / 2 - dw, 0), (w / 2 + dw, 0), (w / 2 - dw, t), (-w / 2 + dw, t)], "sin", "SiN multimode core", row("m3", "m7") + stated("p.4 Sec. III-A", "sidewall 83.5 deg; designed width at half height"), layer="waveguide")
    x.dim("h", -w / 2, w / 2, t, px=14, ext=(t / 2, t / 2), row_id="m3")
    x.dim("v", 0, t, w / 2 + dw, px=10, ext=(w / 2 + dw, w / 2 - dw), row_id="m7")
    x.dim("v", -box, 0, half, px=8, ext=(half, half), text="4.5 um", src=stated("p.3 Sec. II-A", "thermal SiO2"))
    x.dim("v", 0, clad, half, px=8, ext=(half, half), text="3 um", src=stated("p.4 Sec. II-B", "PECVD SiO2"))

    # corner of the core, to see the stated sidewall
    z = c.view("xcorner", "detail: sidewall 83.5 deg, designed width at half height", "xsec", like="xsec", window=(w / 2 - 0.35, -0.08, w / 2 + 0.25, 0.48))
    z.line([(w / 2, 0), (w / 2, t)], "designed edge, half-height reference", stated("p.4 Sec. III-A", "designed width at half height"))

    c.check("SEM L by its 5 um bar against the row, um", px_l / px_um, lm, 0.03)
    c.check("drawn output centre spacing / W against the SEM ratio", 2 * off / w, 70 / px_w, 0.03)
    # paper: L = 3 Lpi / 8, Lpi from the two lowest modes, FEM. First-order Lpi only: a note and not a check
    n_r = 1.72  # TE slab index read from Fig. 2(d), at width 1.6 um and still rising
    we = w + 1.55 / math.pi / math.sqrt(n_r**2 - 1.46**2)
    lf = 3 / 8 * 4 * n_r * we**2 / (3 * 1.55)
    top.note(f"First order, not a check: 3 Lpi / 8 with slab index {n_r} (Fig. 2(d)) gives {lf:.1f} um, {100 * (lf - lm) / lm:.1f} % above the drawn {lm:.0f} um. The paper's FEM curve in Fig. 6(a) puts W 3.9 um at L 10 um.")
    return c
