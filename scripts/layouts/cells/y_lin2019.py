"""Lin 2019: parameterized asymmetric Y-junction family (Sec. 2 Eq. (2)-(3), Fig. 1(b)-(c), Table 1, Fig. 2(a)-(e)).

Boundaries are the paper's construction. Bottom: two S-curves of radius R1 then R2, each S two equal arcs, rising from w0/2 to
w then falling to w0 + D/2. Top: the same rises with r1 and r2 of Table 1, the r1 S-curve ending where the R1 one does, then the
straight l of Eq. (3), so the r2 S-curve is centred on the R2 one. Fig. 1(c) shows this order; the closure 2 R1 sin + 2 R2 sin
= L confirms it. For r1 below (w - w0/2)/2 the arc sweeps past 90 deg and the outline overhangs: the hook seen in the SEMs.
Arms: 500 nm, S-bends read against the 2 um bars of Fig. 2.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Pt, Route, View, assumed, fig, row, stated  # noqa: E402

ID = "cmp_lit_lin2019_asym_y_junction_family"
TABLE = [(0.12, 0.06), (0.22, 0.11), (0.32, 0.17), (0.42, 0.23), (0.52, 0.29), (0.72, 0.41), (0.92, 0.53), (1.12, 0.65), (1.32, 0.77), (1.52, 0.89), (1.7, 1.0)]  # Table 1


def s_curve(x0: float, y0: float, rad: float, dy: float, rising: bool, n: int = 14) -> list[Pt]:
    """Two equal arcs of radius rad moving y by dy over the curve, tangent to x at both ends. dy > 0 only; rising or falling."""
    th = math.acos((rad - dy / 2) / rad)
    s = 1.0 if rising else -1.0
    pts: list[Pt] = []
    for k in range(n + 1):
        p = th * k / n
        pts.append((x0 + rad * math.sin(p), y0 + s * rad * (1 - math.cos(p))))
    xc = x0 + 2 * rad * math.sin(th)
    yc = y0 + s * dy
    for k in range(n - 1, -1, -1):
        p = th * k / n
        pts.append((xc - rad * math.sin(p), yc - s * rad * (1 - math.cos(p))))
    return pts


def half_dx(rad: float, dy: float) -> float:
    return rad * math.sin(math.acos((rad - dy / 2) / rad))


def junction(r1: float, r2: float, ln: float, w: float, w0: float, d: float, big1: float, big2: float, x_in: float) -> list[Pt]:
    """Closed outline: input stub, top boundary (r1, r2), right edge with the rounded slot tip, bottom boundary (R1, R2)."""
    rise = w - w0 / 2
    fall = w - w0 - d / 2
    x_j = 2 * half_dx(big1, rise)
    ell = half_dx(big2, fall) - half_dx(r2, fall)  # Eq. (3)
    top = [(x_in, w0 / 2)] + s_curve(x_j - 2 * half_dx(r1, rise), w0 / 2, r1, rise, True) + s_curve(x_j + ell, w, r2, fall, False) + [(ln, w0 + d / 2), (ln, d / 2)]
    tip = [(ln + d / 2 * math.cos(math.radians(a)) - d / 2, d / 2 * math.sin(math.radians(a))) for a in range(90, 271, 15)]
    bottom = s_curve(0.0, w0 / 2, big1, rise, True) + s_curve(x_j, w, big2, fall, False)
    low = [(x, -y) for x, y in bottom]
    return top + tip + [(ln, -d / 2), (ln, -w0 - d / 2)] + low[::-1] + [(x_in, -w0 / 2)]


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 1(a)-(c) geometry", "Table 1 (r1, r2)", "Eq. (2), Eq. (3)", "Fig. 2(a)-(e) SEMs", "Fig. 2(f)-(i) test layout", "Sec. 2", "Sec. 3"],
        "Y-junction family computed from Eqs. (2)-(3) and Table 1: top boundary r1, r2, bottom R1, R2; hook at small r1; S-bend arms",
    )
    ln = c.um("m5")
    w0 = c.um("m7")
    d = c.um("m8")
    t = c.um("m9")
    box = c.um("m10")
    w, big1, big2 = 0.7, 1.7, 1.0  # Sec. 2
    x_in = -1.5
    arm_dx, arm_dy = 11.4, 2.4  # Fig. 2: arms settle 5.5 um apart centre to centre, 11.4 um from the slot tip
    src_core = row("m5", "m7", "m8") + stated("p.2 Sec. 2", "w, R1, R2, Eqs. (2)-(3)") + stated("Table 1", "r1, r2") + fig("Fig. 1(c)", "order of the curves")
    src_arm = row("m7") + fig("Fig. 2(a)-(e)", "arm span against the 2 um bars", "10 %")

    def draw(v: View, r1: float, r2: float, dy: float, tag: str) -> None:
        v.poly([(x, y + dy) for x, y in junction(r1, r2, ln, w, w0, d, big1, big2, x_in)], "si", f"splitting region {tag}", src_core, layer="waveguide")
        for s in (1.0, -1.0):
            arm = Route((ln, dy + s * (w0 + d) / 2), 0.0, w0, tol=0.005).sbend(arm_dx, s * arm_dy, n=40).straight(1.0)
            v.route(arm, "si", f"output arm {tag}" + (" (weak)" if s > 0 else " (strong)"), src_arm, layer="waveguide")

    r1m, r2m = TABLE[3]  # device 4, the r1 of Fig. 2(c)
    tp = c.view("top", "top view: device 4, r1 = 0.42 um, r2 = 0.23 um")
    draw(tp, r1m, r2m, 0.0, "r1 0.42")
    x_end = ln + arm_dx + 1.0
    tp.dim("v", -(arm_dy + (w0 + d) / 2), arm_dy + (w0 + d) / 2, x_end, px=14, ext=(x_end, x_end), text="5.5 um", src=src_arm)
    tp.dim("h", ln, ln + arm_dx, -(arm_dy + (w0 + d) / 2) - w0 / 2, px=20, ext=(-(arm_dy + (w0 + d) / 2), -(arm_dy + (w0 + d) / 2)), text="11.4 um", src=src_arm)
    tp.label((x_in, 0), "in", anchor="end", dx=-6)
    tp.label((x_end, arm_dy + (w0 + d) / 2), "PR (weak)", anchor="end", dy=-9)
    tp.label((x_end, -arm_dy - (w0 + d) / 2), "1 - PR (strong)", anchor="end", dy=16)
    tp.note("Arms continue to the cascaded devices and grating couplers: truncated (Fig. 2(f)-(i)).")
    tp.note("Weak arm assignment: smaller r1 makes the top boundary steeper; the paper's Fig. 1(a) labels the upper arm PR.")
    c.thumb = {"view": "top", "window": [-1.5, -3.0, 13.5, 3.0]}

    det = c.view("junction", "detail: splitting region of device 4, the parameters of Fig. 1(b)-(c)", like="top", window=(-1.0, -1.25, ln + 0.9, 1.25))
    det.dim("h", 0.0, ln, -w, px=-24, ext=(-w0 / 2, -w0 - d / 2), row_id="m5")
    det.dim("v", -w, w, 2 * half_dx(big1, w - w0 / 2), px=0, ext=(2 * half_dx(big1, w - w0 / 2), 2 * half_dx(big1, w - w0 / 2)), text="2w = 1.4 um", src=stated("p.2 Sec. 2", "w = 0.7 um"))
    det.dim("v", -w0 / 2, w0 / 2, -0.75, px=0, ext=(-0.75, -0.75), row_id="m7")
    det.dim("v", -d / 2, d / 2, ln + 0.4, px=16, ext=(ln + 0.4, ln + 0.4), row_id="m8")
    det.label((0.9, -0.65), "R1", anchor="middle", tip="bottom boundary: R1 = 1.7 um, two arcs")
    det.label((2.0, -0.82), "R2", anchor="middle", tip="bottom boundary: R2 = 1 um, two arcs")
    det.label((1.45, 0.63), "r1", anchor="end", dx=-6, dy=-6, tip="top boundary: r1 = 0.42 um, two arcs")
    det.label((1.95, 0.8), "r2", anchor="middle", tip="top boundary: r2 = 0.23 um, two arcs")

    pitch_x, pitch_y = 5.2, 2.8
    fam = c.view("family", "all 11 designs of Table 1, true scale, on a reading grid", window=(-1.7, -1.1, 3 * pitch_x - 1.7, 4 * pitch_y - 1.1))
    for k, (r1, r2) in enumerate(TABLE):
        dx, dy = (k % 3) * pitch_x, (3 - k // 3) * pitch_y
        fam.poly([(x + dx, y + dy) for x, y in junction(r1, r2, ln, w, w0, d, big1, big2, x_in)], "si", f"device {k + 1}: r1 {r1}, r2 {r2}", src_core, layer="waveguide")
        for s in (1.0, -1.0):
            arm = Route((ln + dx, dy + s * (w0 + d) / 2), 0.0, w0, tol=0.004).straight(0.9)
            fam.route(arm, "si", f"device {k + 1} arm stub", row("m7"), layer="waveguide")
        fam.label((x_in + dx, dy - 1.0), f"#{k + 1} r1 {r1}", anchor="start", dx=2)
    fam.note("r1 = 1.7 um is the symmetric 50:50 design. r1 = 0.12 and 0.22 um have arcs sweeping past 90 deg: the overhang of Fig. 2(a)-(b).")
    fam.note("Grid for reading only, arms cut at 0.9 um: on the chip these are separate devices.")

    # closure
    rise, fall = w - w0 / 2, w - w0 - d / 2
    c.check("L from the arcs, 2 R1 sin + 2 R2 sin, against the row um", 2 * half_dx(big1, rise) + 2 * half_dx(big2, fall), ln, 0.005)
    c.check("footprint 2w x L against the row um2", 2 * w * ln, c.num("m6"), 0.01)

    def eq2(r1: float) -> float:
        a = (w - w0 / 2) / 4
        return (r1 - a) / (big1 - a) * (big2 - fall / 2) + fall / 2

    for r1, r2 in TABLE[1:]:  # Table 1 prints two decimals: half a unit is the limit
        c.check(f"Eq. (2) r2 at r1 {r1} against Table 1", eq2(r1), r2, 0.005 / r2)
    c.check("Eq. (2) r2 at r1 0.12 against Table 1 (printed 0.06, the equation gives 0.055)", eq2(0.12), 0.06, 0.1)

    x = c.view("xsec", "cross-section at the widest plane of the splitting region", "xsec")
    span = 1.4
    x.rect(-span, -box - 0.4, span, -box, "si", "Si handle", assumed("handle: truncated"), alpha=0.5, layer="substrate")
    x.rect(-span, -box, span, 0.0, "sio2", "buried oxide", row("m10"), layer="oxide")
    x.rect(-w, 0.0, w, t, "si", "Si core", row("m9") + stated("p.2 Sec. 2", "2w = 1.4 um"), layer="waveguide")
    x.dim("h", -w, w, t, px=14, ext=(t, t), text="1.4 um", src=stated("p.2 Sec. 2", "2w"))
    x.dim("v", 0.0, t, w, px=18, ext=(w, w), row_id="m9")
    x.dim("v", -box, 0.0, -span, px=-14, ext=(-span, -span), row_id="m10")
    x.note("No top cladding stated in the paper; the SEMs of Fig. 2 show bare silicon, so none is drawn.")
    return c
