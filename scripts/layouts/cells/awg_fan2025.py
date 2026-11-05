"""Fan 2025 AWG2: 6 x 6, 25 arms, rectangular-type array on 800 nm SiN (Fig. 1(a)-(d), Fig. 2 inset, Table I, Sec. II).

Topology from Fig. 1(a): two FPRs translated (not mirrored), both tilted, array sides facing the same way; each arm leaves
FPR1, turns to +x, turns down, turns to -x and enters FPR2. Tilt 25 deg exceeds the half fan 21.5 deg, so every arm bends
one way at each FPR and the sum of the FPR-side bends is 2 x tilt for all arms: the paper's constant bent length.
Arm lengths are solved so the drawn increment is exactly the Table I path length difference.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, arc, assumed, fig, row, stated  # noqa: E402

ID = "cmp_lit_fan2025_awg2_6x6_demux"


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 1(a)", "Fig. 1(b)", "Fig. 1(c)", "Fig. 1(d)", "Fig. 2 inset", "Table I", "Sec. II"],
        "Rectangular-type AWG: both FPRs, 25 arms with solved lengths, mode converters, I/O tapers; facet routing truncated",
    )
    r_fpr = c.um("m15")  # FPR length
    n_arm = int(c.num("m14"))
    d_a = c.um("m16")  # array and I/O pitch at the FPR
    w_broad = c.um("m18")
    w_port = c.um("m19")
    l_taper = c.um("m20")
    r_bend = c.um("m21")
    dl = c.um("m13")
    n_io = int(c.num("m1"))
    w_sm = 1.0  # stated single-mode width
    tilt = 25.0  # Fig. 1(b): R arrow about 25 deg from the x axis
    pitch_bundle = 4.2  # Fig. 1(d): arm pitch in the bundle against the 20 um bar
    y0 = 9.0  # Fig. 1(b): the first arm settles just above the FPR axis level
    outer_height = 300.0  # text: footprint height 0.3 mm
    sep = outer_height - (n_arm - 1) * pitch_bundle  # FPR1 to FPR2, from the outer arm height
    fpr2_dx = 20.0  # Fig. 1(a): FPR2 apex to the right of the FPR1 apex
    conv_w, conv_l, par_l = 3.2, 2.8, 4.5  # Fig. 2 inset
    src_arm = row("m13", "m14", "m16", "m18", "m21") + fig("Fig. 1(a)", "rectangular topology") + stated("p.3 Sec. II", "broad straight, narrow bends, 10 um tapers")
    tilt_src = fig("Fig. 1(b)", "FPR axis angle", "3 deg")

    top = c.view("top", "top view: phase region at true scale")
    c1 = (0.0, 0.0)
    c2 = (fpr2_dx, -sep)
    delta = math.degrees(d_a / r_fpr)

    def ang(i: int, sign: int) -> float:
        return tilt + sign * (i - (n_arm - 1) / 2) * delta

    def arm_route(i: int, x_turn: float) -> Route:
        """Arm i, FPR1 to FPR2 (i = 0 is the shortest). x_turn: x of the first vertical run."""
        a1, a2 = ang(i, +1), ang(i, -1)
        p1 = (c1[0] + r_fpr * math.cos(math.radians(a1)), c1[1] + r_fpr * math.sin(math.radians(a1)))
        rt = Route(p1, a1, conv_w)
        rt.straight(conv_l).taper(par_l, w_sm, power=0.5)
        conv = conv_l + par_l
        s1a = math.radians(a1)
        y_top = c1[1] + y0 + i * pitch_bundle
        fan1 = (y_top - p1[1] - conv * math.sin(s1a) - r_bend * (1 - math.cos(s1a))) / math.sin(s1a)
        _fan(rt, fan1)
        rt.arc(r_bend, -a1)
        # lower bundle level: from the FPR2 side, mirrored in the arm order
        a2r = math.radians(a2)
        p2 = (c2[0] + r_fpr * math.cos(a2r), c2[1] + r_fpr * math.sin(a2r))
        y_low = c2[1] + y0 + (n_arm - 1 - i) * pitch_bundle
        fan2 = (y_low - p2[1] - conv * math.sin(a2r) - r_bend * (1 - math.cos(a2r))) / math.sin(a2r)
        end2 = (p2[0] + (conv + fan2) * math.cos(a2r) + r_bend * math.sin(a2r), y_low)
        # upper run to the turn, down, lower run back
        _run(rt, x_turn - r_bend - rt.pos[0])
        rt.arc(r_bend, -90)
        _run(rt, (y_top - r_bend) - (y_low + r_bend))
        rt.arc(r_bend, -90)
        _run(rt, (x_turn - r_bend) - end2[0])
        rt.arc(r_bend, a2)
        _fan(rt, fan2)
        rt.taper(par_l, conv_w, power=2.0).straight(conv_l)
        return rt

    def _fan(rt: Route, s: float) -> None:
        if s < -1e-6:
            raise ValueError(f"negative fan run {s}")
        _run(rt, s)

    def _run(rt: Route, s: float) -> None:
        if s < -1e-6:
            raise ValueError(f"negative run {s}")
        if s >= 2 * l_taper:
            rt.straight(l_taper, w_broad).straight(s - 2 * l_taper).straight(l_taper, w_sm)
        else:
            rt.straight(max(s, 0.0))

    # first arm: its turn sits close to the fan end, as in Fig. 1(a); each next arm is solved for the exact increment
    x_first = 210.0
    routes = [arm_route(0, x_first)]
    target0 = routes[0].length
    for i in range(1, n_arm):
        probe = arm_route(i, x_first + i * dl / 2)
        x = x_first + i * dl / 2 + (target0 + i * dl - probe.length) / 2
        routes.append(arm_route(i, x))
    for i, rt in enumerate(routes):
        top.route(rt, "sin", f"arrayed waveguide {i + 1} of {n_arm}", src_arm, layer="waveguide")
    x_right = max(max(p[0] for p in rt.pts) for rt in routes)
    # arm lengths are solved to dl, and the bundle geometry is read from Fig. 1, so only the footprint can fail here
    c.check("drawn phase region area against the stated 1.3 x 0.3 mm, um2", x_right * outer_height, c.num("m10"), 0.05)
    if not 1200.0 <= x_right <= 1300.0:
        raise ValueError(f"phase region length {x_right} is outside the printed 1.2 (Table I) to 1.3 mm (text)")

    # FPRs: array arc at R around the apex, input arc on the Rowland circle of diameter R
    def fpr(center: tuple[float, float]) -> list[tuple[float, float]]:
        half = (n_arm - 1) / 2 * delta + 0.6 * delta
        out = arc(center, r_fpr, tilt - half, tilt + half, tol=0.02)
        cr = (center[0] + r_fpr / 2 * math.cos(math.radians(tilt)), center[1] + r_fpr / 2 * math.sin(math.radians(tilt)))
        hb = math.degrees((n_io / 2 + 1) * d_a / (r_fpr / 2))
        return out + arc(cr, r_fpr / 2, tilt + 180 - hb, tilt + 180 + hb, tol=0.02)

    src_fpr = row("m15", "m16", "m14") + tilt_src + fig("Fig. 1(b)", "sector outline")
    top.poly(fpr(c1), "sin", "input FPR", src_fpr, layer="waveguide", alpha=0.55)
    top.poly(fpr(c2), "sin", "output FPR", src_fpr, layer="waveguide", alpha=0.55)

    # I/O: 6 ports, 3.5 um pitch at the FPR, linear taper 2.5 to 1 um; routing to the facets truncated
    src_io = row("m16", "m19") + stated("p.3 Sec. II", "linear taper 1 to 2.5 um") + assumed("taper length and stub routing not stated; facet routing truncated")
    for center, name, u_turn in ((c1, "input", False), (c2, "output", True)):
        cr = (center[0] + r_fpr / 2 * math.cos(math.radians(tilt)), center[1] + r_fpr / 2 * math.sin(math.radians(tilt)))
        for k in range(n_io):
            beta = (k - (n_io - 1) / 2) * math.degrees(d_a / (r_fpr / 2))
            b = math.radians(tilt + 180 + beta)
            p = (cr[0] + r_fpr / 2 * math.cos(b), cr[1] + r_fpr / 2 * math.sin(b))
            head = tilt + 180 + beta / 2
            rt = Route(p, head, w_port)
            rt.straight(30.0, w_sm).straight(8.0)
            if u_turn:
                rad = 35.0 + (n_io - 1 - k) * 4.0
                rt.arc(rad, 270 - head)
                rt.straight(20.0 + k * 3.0)
                rt.arc(rad, 90).straight(420.0)
            else:
                rad = 35.0 + k * 4.0
                rt.arc(rad, 180 - head)
                rt.straight(180.0)
            top.route(rt, "sin", f"{name} waveguide {k + 1} of {n_io}", src_io, layer="waveguide")
    top.note("Input and output routing to the edge couplers truncated (Fig. 1(a) continues to the facets).")
    top.note("Arm lengths solved to the Table I increment; bundle pitch, FPR tilt and spacing read from Fig. 1.")

    top.dim("h", 0, x_right, -sep - 2, px=-22, ext=(c2[1], routes[-1].pts[len(routes[-1].pts) // 2][1]), text="1.3 mm", src=stated("p.3 Sec. II", "phase region length; Table I prints 1.2 mm"))
    top.dim("v", -sep + y0 + 0, y0 + (n_arm - 1) * pitch_bundle, x_right, px=12, ext=(x_right, x_right), text="0.3 mm", src=stated("p.3 Sec. II", "phase region height"))
    top.line([c1, (c1[0] + r_fpr * math.cos(math.radians(tilt)), r_fpr * math.sin(math.radians(tilt)))], "FPR length R", row("m15"))
    top.label((r_fpr / 2 * math.cos(math.radians(tilt)), r_fpr / 2 * math.sin(math.radians(tilt))), "R", anchor="start", dx=6, dy=-4, row_id="m15")
    c.thumb = {"view": "top"}

    # detail: same geometry, zoomed on the FPR; dimensions at this scale
    det = c.view("fpr", "detail: input FPR, array aperture, mode converters", like="top", window=(-40, -35, 175, 125))
    det.line([c1, (r_fpr * math.cos(math.radians(tilt)), r_fpr * math.sin(math.radians(tilt)))], "FPR length R", row("m15"))
    det.label((r_fpr / 2 * math.cos(math.radians(tilt)), r_fpr / 2 * math.sin(math.radians(tilt))), "R", anchor="start", dx=6, dy=-4, row_id="m15")
    det.note("Mode converter at each arm: 3.2 x 2.8 um MMI plus 4.5 um parabolic taper to 1 um (Fig. 2 inset).")

    conv = c.view("bend", "detail: arm turn, broad straight and narrow bend", like="top", window=(x_first - 70, -sep + 90, x_first + 70, y0 + 25))
    conv.note("Broad 2 um straights, 10 um tapers, 1 um x 0.8 um bends of radius 20 um (Sec. II, Fig. 1(d)).")

    # cross-section: broad straight section in oxide (BOX and top cladding thickness not in this paper)
    x = c.view("xsec", "cross-section: broad arrayed waveguide", "xsec")
    t = c.um("m22")
    w = w_broad
    box, clad = 4.0, 3.0
    x.rect(-6, -box - 1.5, 6, -box, "si", "substrate", assumed("substrate thickness not stated: truncated"), alpha=0.5, layer="substrate")
    x.rect(-6, -box, 6, 0, "sio2", "lower oxide", assumed("BOX thickness not stated in this paper"), layer="oxide")
    x.rect(-6, 0, 6, t + clad, "sio2", "SiO2 top cladding", assumed("top cladding thickness not stated in this paper"), alpha=0.45, layer="oxide")
    x.rect(-w / 2, 0, w / 2, t, "sin", "Si3N4 core", row("m18", "m22"), layer="waveguide")
    x.dim("h", -w / 2, w / 2, t, px=14, ext=(t, t), row_id="m18")
    x.dim("v", 0, t, w / 2, px=18, ext=(w / 2, w / 2), row_id="m22")
    return c
