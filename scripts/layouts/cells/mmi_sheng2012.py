"""Sheng 2012 1x2 MMI on 220 nm SOI (Fig. 1(a), Fig. 1(b), Table 1, Fig. 4 SEM, Fig. 5 cascade, Sec. 2).

Topology from Fig. 1(b) and the SEM: one centred input, two parallel outputs at +-(Wt + Wg)/2, every port a linear taper
with its axis parallel to the MMI axis, wide end at the MMI. theta in Fig. 1(b) is the half angle (edge to axis); the SEM
confirms it: the width changes by 0.034 per um against the 10 um bar (28.3 px/um), 2 tan(1 deg) = 0.035.
Past the tapers, Fig. 5: the two outputs turn up and down by 90 deg; the upper goes to a grating coupler, the lower to the
next cascade stage.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, assumed, fig, row, stated  # noqa: E402

ID = "cmp_lit_sheng2012_mmi_1x2"


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 1(a)", "Fig. 1(b)", "Table 1", "Fig. 4 SEM", "Fig. 5 micrograph", "Sec. 2"],
        "1x2 MMI: centred input, two parallel outputs, 1 deg half-angle linear tapers, 90 deg output bends of the cascade",
    )
    w = c.um("m4")
    lm = c.um("m5")
    wt = c.um("m6")
    wco = c.um("m7")
    t = c.um("m8")
    box = c.um("m9")
    theta = 1.0  # p.4 Sec. 2: taper angle
    wg = w / 2 - wt  # p.4: Wg = WMMI/2 - Wt
    lt = (wt - wco) / 2 / math.tan(math.radians(theta))
    off = (wt + wg) / 2
    r_bend = 4.0  # Fig. 5: against the MMI length
    rise = 23.4  # Fig. 5: output height change against the MMI length (a stage drops by the same amount)
    stub = 12.0

    src_t = row("m6", "m7") + stated("p.4 Sec. 2", "linear taper, half angle 1 deg; length follows") + fig("Fig. 1(b)", "taper axis parallel to the MMI axis")
    src_b = row("m7") + fig("Fig. 5", "bend radius and rise by ratio to the 11.5 um MMI length", "20 %")

    top = c.view("top", "top view: 1x2 MMI, tapers and the first bends of the cascade of Fig. 5")
    rin = Route((-lt - stub, 0.0), 0.0, wco, tol=0.003)
    rin.straight(stub).straight(lt, wt)
    top.route(rin, "si", "input waveguide and taper", src_t, layer="waveguide")
    top.rect(0, -w / 2, lm, w / 2, "si", "multimode region", row("m4", "m5") + fig("Fig. 4", "rectangular, with a shoulder at every port: wall to port edge 8.6 px = 0.30 um at 28.3 px/um"), layer="waveguide")
    arms = []
    for sign, name in ((1, "output to grating coupler"), (-1, "output to next stage")):
        rt = Route((lm, sign * off), 0.0, wt, tol=0.003)
        rt.straight(lt, wco)
        rt.arc(r_bend, sign * 90.0).straight(rise - 2 * r_bend).arc(r_bend, -sign * 90.0).straight(stub)
        top.route(rt, "si", name, src_t + src_b, layer="waveguide")
        arms.append(rt)
    top.label((arms[0].pos[0], arms[0].pos[1]), "to grating coupler", anchor="end", dy=-8)
    top.label((arms[1].pos[0], arms[1].pos[1]), "to next MMI", anchor="end", dy=16)
    top.label((-lt - stub, 0.0), "in", anchor="start", dy=-8)
    top.dim("h", 0, lm, w / 2, px=14, ext=(w / 2, w / 2), row_id="m5")
    top.dim("v", off, arms[0].pos[1], arms[0].pos[0], px=10, ext=(lm + lt, arms[0].pos[0]), text="23 um", src=fig("Fig. 5", "rise by ratio to the MMI length", "20 %"))
    top.note("Fig. 5 has the bends about 10 um past the MMI by ratio, inside the 20 um a 1 deg taper needs (SEM: still narrowing at 9.5 um). The stated taper is drawn in full, so the bends sit further out than in Fig. 5.")
    top.note("Cascade truncated: the upper output continues to a grating coupler, the lower to the next MMI, 44 um along and 24 um down in Fig. 5.")
    c.thumb = {"view": "top", "window": [-lt - 2, -8, lm + lt + 2, 8]}

    # same crop as the SEM frame of Fig. 4
    sem = c.view("sem", "detail: the frame of the SEM of Fig. 4", like="top", window=(-10.3, -9.8, lm + 9.5, 9.8))
    sem.dim("h", 0, lm, w / 2, px=12, ext=(w / 2, w / 2), row_id="m5")
    sem.dim("v", -w / 2, w / 2, lm, px=-14, ext=(lm, lm), row_id="m4")

    det = c.view("det", "detail: full tapers, 0.5 to 1.2 um", like="top", window=(-lt - 4, -6, lm + lt + 4, 6))
    det.dim("h", -lt, 0, wt / 2, px=26, ext=(wco / 2, wt / 2), text="20 um", src=stated("p.4 Sec. 2", "1 deg half angle, 0.5 to 1.2 um"))
    det.label((-lt - 1.0, 0.0), "width", dy=16, row_id="m7")
    det.label((-lt / 2, 0), "half angle 1 deg", dy=34, tip="p.4 Sec. 2, Fig. 1(b)")

    ports = c.view("ports", "detail: output ports at the MMI", like="top", window=(lm - 1.6, -2.5, lm + 6.5, 2.5))
    ports.dim("v", off - wt / 2, off + wt / 2, lm + 0.0, px=-16, ext=(lm, lm), row_id="m6")
    ports.dim("v", -wg / 2, wg / 2, lm + 0.7, px=6, ext=(lm + 0.7, lm + 0.7), text="0.6 um", src=stated("p.4 Sec. 2", "Wg, Table 1"))
    ports.dim("v", -w / 2, w / 2, lm - 1.1, px=-8, ext=(lm - 1.1, lm - 1.1), row_id="m4")

    # cross-section Fig. 1(a): channel, no slab
    x = c.view("xsec", "cross-section: 500 nm x 220 nm access waveguide", "xsec")
    clad = 2.0
    x.rect(-2, -box - 0.6, 2, -box, "si", "Si substrate", assumed("handle thickness not stated: truncated"), layer="substrate", alpha=0.5)
    x.rect(-2, -box, 2, 0, "sio2", "buried oxide", row("m9"), layer="oxide")
    x.rect(-2, 0, 2, clad, "sio2", "deposited SiO2 cladding", assumed("the paper says thick; thickness not stated"), layer="oxide", alpha=0.45)
    x.rect(-wco / 2, 0, wco / 2, t, "si", "Si channel core", row("m7", "m8"), layer="waveguide")
    x.dim("h", -wco / 2, wco / 2, t, px=14, ext=(t, t), row_id="m7")
    x.dim("v", 0, t, wco / 2, px=16, ext=(wco / 2, wco / 2), row_id="m8")
    x.dim("v", -box, 0, 2, px=10, ext=(2, 2), row_id="m9")

    # plane at the output side of the multimode region: same stack, the two tapers at their wide end
    y = c.view("xports", "cross-section: output ports at the MMI end", "xsec")
    y.rect(-2.2, -0.7, 2.2, 0, "sio2", "buried oxide (2 um, truncated)", row("m9"), layer="oxide")
    y.rect(-2.2, 0, 2.2, 0.8, "sio2", "deposited SiO2 cladding", assumed("the paper says thick; thickness not stated"), layer="oxide", alpha=0.45)
    y.rect(off - wt / 2, 0, off + wt / 2, t, "si", "upper port", row("m6", "m8"), layer="waveguide")
    y.rect(-off - wt / 2, 0, -off + wt / 2, t, "si", "lower port", row("m6", "m8"), layer="waveguide")
    y.dim("h", off - wt / 2, off + wt / 2, t, px=12, ext=(t, t), row_id="m6")
    y.dim("h", -wg / 2, wg / 2, t, px=12, ext=(t, t), text="0.6 um", src=stated("p.4 Sec. 2", "Wg"))

    c.check("drawn taper width slope against the SEM, 25.1 to 34.0 px over 260 px, per um", 2 * math.tan(math.radians(theta)), (34.0 - 25.1) / 260, 0.05)
    c.check("drawn port width against the SEM, 33.9 px at 28.3 px/um, um", wt, 33.9 / 28.3, 0.03)
    c.check("drawn MMI length against the SEM, 336 px at 28.3 px/um, um", lm, 336 / 28.3, 0.05)
    c.check("drawn MMI width against the SEM, 103 px at 28.3 px/um, um", w, 103 / 28.3, 0.03)
    # first-order self-imaging only: a note and not a check. L = 3 Lpi / 8, Lpi = 4 n W_e^2 / (3 lambda), assumed slab index
    n_r = 2.85
    we = w + 1.55 / math.pi / math.sqrt(n_r**2 - 1.444**2)
    lf = 3 / 8 * 4 * n_r * we**2 / (3 * 1.55)
    top.note(f"First order, not a check: 3 Lpi / 8 with an assumed slab index {n_r} gives {lf:.1f} um, {100 * (lf - lm) / lm:.1f} % above the drawn {lm} um. The paper finds L by mode-matching simulation for each taper width.")
    return c
