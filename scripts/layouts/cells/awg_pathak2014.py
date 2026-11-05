"""Pathak 2014: 8 x 400 GHz SOI AWG on a 1 nm mask grid: cross-sections only (Sec. II-III, ref. [8] Sec. 3 and Fig. 3(b), (c)).

The paper has no plan view of this device: only the schematic Fig. 1. The plan views below (top, fan, corner, aperture) scale the
mask layout of ref. [8], a different 16-channel device with no scale bar, so they are withheld at build (NOT_DRAWN) and only kept
as a record. Published: two sections. The stack is this paper's; which section sits where comes from ref. [8], and says so.
Delta L here is inferred from Table I and the 2:1 delay of Sec. III (19.64 um), not printed; it feeds only the withheld views.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Pt, Route, arc, assumed, fig, row, stated  # noqa: E402

ID = "cmp_lit_pathak2014_awg_8x400_grid1nm"


def build() -> Cell:
    c = Cell(
        ID,
        ["Sec. II (800 nm, 450 nm)", "Sec. III (stack)", "Ref. [8] Sec. 3, Fig. 3(b), (c): where each section sits, from a different 16-channel device"],
        "Cross-sections only: this paper has no plan view of the device. Stack from Sec. III; the broad arm and 2 um aperture roles are from ref. [8], a different device",
    )
    n_arm = int(c.num("m8"))
    n_ch = int(c.num("m6"))
    fsr = c.num("m4") * 1e-3
    t_si = c.um("m9")
    box = c.um("m11")
    shallow = 0.07  # p.3 Sec. III
    height, width = 490.0, 307.0  # Table I, first number is the height (see module note)
    w_b, w_n = 0.8, 0.45  # p.2 Sec. II widths; roles from ref. [8] Fig. 3(b)
    w_ap = 2.0  # ref. [8] Sec. 3
    r_b = 4.5  # ref. [8] Fig. 3(b): about half the level pitch of its 16-channel mask
    l_t = 5.0  # ref. [8] Fig. 3(b): taper about as long as the bend radius
    dl = (873.0 - 490.0) * 2 / (n_arm - 1)  # Table I, 8 x 200 less 8 x 400 height; the 200 GHz delay is twice the 400 GHz one (Sec. III)
    r_fpr = 170.0  # ref. [8] Fig. 3(a) ratios, see the checks
    d_a = 2.9  # array aperture pitch at the star: same ratio
    delta = d_a / r_fpr
    d_io = 0.0032 * (1550.0 / c.num("m4")) / (2.85 * delta)  # grating equation, 3.2 nm channel, slab index 2.85
    l_ap = 32.0  # ref. [8] Fig. 3(a): aperture taper 19 % of R
    x_in0 = 12.0  # ref. [8] Fig. 3(a): shortest arm sits over the gap between the stars
    x_out = width / 2 - w_b / 2
    y_top_out = height - w_b / 2
    px = (x_out - x_in0) / (n_arm - 1)
    py = dl / 2 - px
    y_top0 = y_top_out - (n_arm - 1) * py
    x_c = (x_in0 + x_out) / 2
    y_a = y_top0 - 1.26 * r_fpr  # ref. [8] Fig. 3(a): shortest arm top is 1.26 R above the port arc
    r0 = r_fpr + l_ap

    src_arm = row("m5", "m8") + fig("Fig. 1", "nested rectangular delay lines") + stated("p.1 Sec. II", "3 sides of a rectangle, Manhattan") + stated("p.2 Sec. II", "800 and 450 nm") + fig("Ref. [8] Fig. 3(a)", "arm landing on the star, 16-channel sibling, ratios", "15 %")
    src_ap = stated("Ref. [8] Sec. 3", "2 um aperture, 70 nm etched trench") + fig("Ref. [8] Fig. 3(c)", "aperture taper to 0.45 um") + fig("Ref. [8] Fig. 3(a)", "length 19 % of R", "20 %")
    tp = c.view("top", "top view: both stars and the array at true scale, after the mask layout of ref. [8]")

    def run(rt: Route, s: float) -> None:
        if s < -1e-6:
            raise ValueError(f"negative run {s}")
        if s >= 2 * l_t + 1.0:
            rt.straight(l_t, w_b).straight(s - 2 * l_t).straight(l_t, w_n)
        else:
            rt.straight(max(s, 0.0))

    def arm(i: int, y_top: float) -> Route:
        """Arm i, left star to right star (i = 0 is the shortest). th > 0 leans outwards going up."""
        th = (i - (n_arm - 1) / 2) * delta
        th_deg = math.degrees(th)
        p = (-x_c - r0 * math.sin(th), y_a + r0 * math.cos(th))
        rt = Route(p, 90.0 + th_deg, w_n, tol=0.05)
        x_v = -(x_in0 + i * px)
        s = (p[0] - x_v - math.copysign(r_b * (1 - math.cos(th)), th)) / math.sin(th)
        if s < -1e-6:
            raise ValueError(f"arm {i}: fan run {s}")
        rt.straight(max(s, 0.0)).arc(r_b, -th_deg)
        y_v = rt.pos[1]
        run(rt, y_top - r_b - y_v)
        rt.arc(r_b, -90.0)
        run(rt, -2 * x_v - 2 * r_b)
        rt.arc(r_b, -90.0)
        run(rt, y_top - r_b - y_v)
        rt.arc(r_b, -th_deg)
        rt.straight(max(s, 0.0))
        return rt

    routes = [arm(0, y_top0)]
    l0 = routes[0].length
    y_tops = [y_top0]
    for i in range(1, n_arm):
        probe = arm(i, y_top0 + i * py)
        y = y_top0 + i * py + (l0 + i * dl - probe.length) / 2
        routes.append(arm(i, y))
        y_tops.append(y)
    for i, rt in enumerate(routes):
        tp.route(rt, "si", f"arrayed waveguide {i + 1} of {n_arm}", src_arm, layer="waveguide")

    alpha = (n_arm - 1) / 2 * delta

    def star(cx: float) -> list[Pt]:
        a = math.degrees(alpha + 0.6 * delta)
        hw = 1.14 * (n_arm * d_a / 2)  # ref. [8] Fig. 3(a): body 1.14 x the array chord
        b = math.degrees(math.asin(0.515 * hw / (r_fpr / 2)))  # ref. [8] Fig. 3(a): port-side flat 0.515 x body width
        return arc((cx, y_a), r_fpr, 90.0 - a, 90.0 + a, tol=0.05) + [(cx - hw, y_a + 0.93 * r_fpr), (cx - hw, y_a + 0.06 * r_fpr)] + arc((cx, y_a + r_fpr / 2), r_fpr / 2, 270.0 - b, 270.0 + b, tol=0.05) + [(cx + hw, y_a + 0.06 * r_fpr), (cx + hw, y_a + 0.93 * r_fpr)]

    src_star = row("m8") + fig("Ref. [8] Fig. 3(a)", "star outline, ratios to R") + assumed("star radius not stated for this device: scaled from ref. [8] and the grating equation")
    for cx, name in ((-x_c, "input"), (x_c, "output")):
        tp.poly(star(cx), "si", f"{name} star coupler, unetched Si", src_star, layer="waveguide", alpha=0.75)
        for i in range(n_arm):
            th = (-1.0 if cx > 0 else 1.0) * (i - (n_arm - 1) / 2) * delta
            sn, cs = math.sin(th), math.cos(th)

            def pt(r: float, u: float, sn: float = sn, cs: float = cs, cx: float = cx) -> Pt:
                return (cx - r * sn + u * cs, y_a + r * cs + u * sn)

            # 70 nm trench of ref. [8] Fig. 3(c): a wide strip at the star, stepping in to a thin wedge along the taper
            h0 = d_a * 0.49
            h1 = (r_fpr + 0.5 * l_ap) * delta * 0.49
            shoulder = [pt(r_fpr, -h0), pt(r_fpr, h0), pt(r_fpr + 0.5 * l_ap, h1), pt(r_fpr + 0.5 * l_ap, h1 * 0.55), pt(r_fpr + 0.95 * l_ap, w_n / 2), pt(r_fpr + 0.95 * l_ap, -w_n / 2), pt(r_fpr + 0.5 * l_ap, -h1 * 0.55), pt(r_fpr + 0.5 * l_ap, -h1)]
            tp.poly(shoulder, "si", "shallow etched shoulder, 150 nm Si", src_ap, layer="slab", alpha=0.45, lod=1.0)
            ap = Route(pt(r_fpr, 0.0), 90.0 + math.degrees(th), w_ap, tol=0.05).straight(l_ap, w_n)
            tp.route(ap, "si", "array aperture, 2 um tapering to 0.45 um", src_ap, layer="waveguide")
        # ports on the Rowland circle, radial stubs as in ref. [8] Fig. 3(a), truncated
        for k in range(n_ch):
            phi = (k - (n_ch - 1) / 2) * d_io / r_fpr
            q = (cx + r_fpr * math.cos(phi) * math.sin(phi), y_a + r_fpr - r_fpr * math.cos(phi) ** 2)
            rt = Route(q, -90.0 + math.degrees(phi), w_ap, tol=0.05)
            l_port = q[1] / math.cos(phi)
            rt.straight(0.7 * l_port, w_n).straight(0.3 * l_port)
            tp.route(rt, "si", f"{name} waveguide {k + 1} of {n_ch} (truncated)", row("m6") + stated("Ref. [8] Sec. 3", "2 um apertures") + assumed("port pitch from the grating equation; ports on both stars as in ref. [8]; routing to the grating couplers truncated"), layer="waveguide")

    x_max = max(max(p[0] for p in rt.pts) for rt in routes) + w_b / 2
    y_max = y_tops[-1] + w_b / 2
    # internal only: the plan views are withheld, so these closures are not published as checks
    if abs((y_max * 2 * x_max) / c.num("m5") - 1) > 1e-3 or abs(1.55**2 / (fsr * dl) / 3.93 - 1) > 0.04:
        raise ValueError("withheld plan views no longer close against Table I")

    tp.dim("h", -x_out, x_out, y_top_out, px=14, ext=(y_top_out, y_top_out), text="307 um", src=stated("Table I", "area 490 x 307 um2, second number"))
    tp.dim("v", 0.0, y_max, x_max, px=16, ext=(x_max, x_max), text="490 um", src=stated("Table I", "area 490 x 307 um2, first number"))
    tp.label((-x_c, y_a + r_fpr / 2), "star", anchor="middle")
    tp.label((x_c, y_a + r_fpr / 2), "star", anchor="middle")
    tp.note(f"delta L = {dl:.2f} um from Table I and the 2:1 delay of Sec. III, not printed for this device; arm lengths solved to it. No micrograph in the paper.")
    tp.note("The 1 nm grid snapping (arm length within +-3 nm, Sec. II) is far below the drawing tolerance and is not drawn.")
    tp.note("Stars dashed: their radius is scaled from the sibling mask of ref. [8]. Ports continue to grating couplers: truncated.")
    c.thumb = {"view": "xsec2"}

    fan = c.view("fan", "detail: apertures, fan bends and the shortest arm", like="top", window=(-130, y_a + r_fpr - 10, 20, y_top0 + 15))
    fan.dim("h", -x_in0, x_in0, y_top0, px=12, ext=(y_top0, y_top0), text="24 um", src=fig("Ref. [8] Fig. 3(a)", "shortest arm, ratio", "20 %"))
    fan.note("Layout of ref. [8] Fig. 3(a): radial out of the star, one short bend to vertical. Bend sections are the same on every arm (Sec. II).")

    cor = c.view("corner", "detail: outer corners, 800 nm straights tapering to 450 nm in the bends", like="top", window=(-x_out - 2, y_top_out - 32, -x_out + 40, y_top_out + 2))
    cor.note("As ref. [8] Fig. 3(b). Bend radius about 4.5 um read from its level pitch, 20 %.")

    ap_v = c.view("aperture", "detail: 2 um apertures, 70 nm trench and taper to 450 nm", like="top", window=(-x_c - 22, y_a + r_fpr - 8, -x_c + 22, y_a + r_fpr + l_ap + 4))
    ap_v.note("As ref. [8] Fig. 3(c). The same etch makes the grating couplers.")

    x = c.view("xsec", "cross-section: 800 nm wire; broad arm role from ref. [8]", "xsec")
    span = 2.2
    x.rect(-span, -box - 0.5, span, -box, "si", "Si handle", assumed("handle: truncated"), alpha=0.5, layer="substrate")
    x.rect(-span, -box, span, 0.0, "sio2", "oxide", row("m11"), layer="oxide")
    x.rect(-w_b / 2, 0.0, w_b / 2, t_si, "si", "Si wire", row("m9", "m10") + stated("p.2 Sec. II", "800 nm"), layer="waveguide")
    x.dim("h", -w_b / 2, w_b / 2, t_si, px=14, ext=(t_si, t_si), text="800 nm", src=stated("p.2 Sec. II"))
    x.dim("v", 0.0, t_si, w_b / 2, px=18, ext=(w_b / 2, w_b / 2), row_id="m9")
    x.dim("v", -box, 0.0, -span, px=-14, ext=(-span, -span), row_id="m11")
    x.note("This paper prints 800 nm and 450 nm without roles; ref. [8], a different device of the same group, uses 800 nm in the straights of the array and 450 nm in the bends. Top cladding not stated in this paper; none drawn.")

    x2 = c.view("xsec2", "cross-section: 2 um aperture in the 70 nm etch, from ref. [8]", "xsec")
    x2.rect(-span, -box - 0.5, span, -box, "si", "Si handle", assumed("handle: truncated"), alpha=0.5, layer="substrate")
    x2.rect(-span, -box, span, 0.0, "sio2", "oxide", row("m11"), layer="oxide")
    x2.rect(-span, 0.0, span, t_si - shallow, "si", "shallow etched Si, 150 nm", stated("p.3 Sec. III", "70 nm shallow etch") + row("m9"), layer="slab")
    x2.rect(-w_ap / 2, 0.0, w_ap / 2, t_si, "si", "aperture, from ref. [8]", row("m9") + stated("Ref. [8] Sec. 3", "2 um, a different device"), layer="waveguide")
    x2.dim("h", -w_ap / 2, w_ap / 2, t_si, px=14, ext=(t_si, t_si), text="2 um", src=stated("Ref. [8] Sec. 3", "a different device"))
    x2.dim("v", t_si - shallow, t_si, w_ap / 2, px=18, ext=(w_ap / 2, w_ap / 2), text="70 nm", src=stated("p.3 Sec. III"))
    x2.dim("v", 0.0, t_si, -w_ap / 2, px=-16, ext=(-w_ap / 2, -w_ap / 2), row_id="m9")
    x2.note("The 70 nm etch and 220 nm film are this paper's (Sec. III). The 2 um aperture and its place at the star are from ref. [8] Sec. 3 and Fig. 3(c), a different device of the same group: this paper does not state an aperture width.")
    return c
