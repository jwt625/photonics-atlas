"""PS3 of a 2021 visible-light SiN thermo-optic phase shifter: suspended SiO2 bridge, 7 folded passes, 10 um TiN heater (Table I, Fig. 2(c) XTEM of PS3, Appendix).

The plan figures of the paper, Fig. 1(a) and the micrograph Fig. 2(a), show PS1 only (3 passes, 4.2 um heater, 500 um). PS3 has no
plan view, so the plan here is only what PS3 sources fix: the suspended region 15.4 x 984 um, the heater 983.8 x 10 um and the 7
passes, cut where they leave the region. Loopbacks, leads, pads, MMIs and the reference arm are not drawn.

Trench rows and undercut are dashed context: PS3 has deep trenches and anchors (Appendix), but their size is labelled for PS1 only.
Their count, 18 per row, is a drafting choice, not a result. The sections come from the XTEM of PS3.
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, arc, assumed, fig, row, stated  # noqa: E402

ID = "cmp_lit_yong2021_ps3_suspended_7pass"

UM_PX = 500.0 / 324.0  # Fig. 2(a) 500 um bar: 324 px


def rounded(x0: float, y0: float, x1: float, y1: float, r: float) -> list[tuple[float, float]]:
    return arc((x1 - r, y0 + r), r, -90, 0, tol=0.2) + arc((x1 - r, y1 - r), r, 0, 90, tol=0.2) + arc((x0 + r, y1 - r), r, 90, 180, tol=0.2) + arc((x0 + r, y0 + r), r, 180, 270, tol=0.2)


def build() -> Cell:
    c = Cell(
        ID,
        ["Table I", "Fig. 2(c) XTEM of PS3", "Sec. II-III", "Appendix", "Fig. 1(a), Fig. 1(b), Fig. 2(a): PS1, dashed context only"],
        "15.4 x 984 um suspended bridge, 983.8 x 10 um TiN heater, 7 passes cut at the bridge ends; trapezoid section over the undercut Si. Routing outside the bridge not shown: no PS3 plan view in the paper",
    )
    L_h = c.um("m20")
    w_h = c.um("m21")
    t_sin = c.um("m24")
    h_gap = c.um("m23")
    L_wg = c.um("m22")
    m = re.findall(r"\d+", c.metric("m25")["condition"].split("among")[1])
    cycle = [float(x) / 1000 for x in m[:3]]  # 600, 650, 550 in Fig. 1(b) order
    n = 7
    ws = [cycle[i % 3] for i in range(n)]
    gap = 1.2  # Sec. II, design gap; the XTEM of PS3 reads it about 100 nm larger with narrower cores
    margin = 2.0  # Sec. III: edge waveguide to bridge edge, as designed, from the XTEM of PS3
    w_br, L_br = 15.4, 984.0  # Table I
    l_tr, g_tr, w_tr = 46.0, 6.0, 8.0  # Fig. 1(a) labels, PS1: dashed context, no label on this drawing
    n_tr = 18  # per row: not stated for PS3, drafting choice
    und = 8.0  # Appendix: undercut extends 8 um laterally beyond the trench
    und_z = 18.0  # Sec. II: 18 um vertically, same conditions for PS3 (Appendix)
    t_tin = 0.15  # Fig. 1(b)
    t_bot = 3.25  # p.8: bottom cladding of the wafer of the XTEM
    t_above, t_plat = 0.62, 0.30  # Fig. 2(c): oxide above the TiN and plateau step, against the 5 um bar
    b_bot, b_top = 16.2, 14.65  # Fig. 2(c): bridge width at bottom and top, 885 and 800 px at 54.6 px/um
    w_plat = 10.25  # Fig. 2(c): plateau over the TiN, 560 px

    array = sum(ws) + (n - 1) * gap
    ys: list[float] = []
    y = array / 2
    for w in ws:  # first in Table order on top in plan; which end is pass 1 of the fold is not known
        ys.append(y - w / 2)
        y -= w + gap
    xe = L_br / 2

    src_pass = row("m20", "m22", "m25") + stated("Table I", "7 passes") + stated("p.5", "1.2 um design gap") + fig("Fig. 2(c)", "XTEM of PS3: 7 cores at 1.83 um pitch", "2 %")
    src_tr = fig("Fig. 1(a)", "PS1 trench and anchor size") + assumed("trench count and size not stated for PS3: PS1 size, 18 per row, context only")
    src_und = stated("Appendix p.15", "undercut extends about 8 um laterally beyond each trench") + assumed("outline follows the assumed trench rows")

    top = c.view("top", "top view: only what PS3 sources fix. Bridge, heater, 7 passes cut at the bridge ends")
    row_len = n_tr * l_tr + (n_tr - 1) * g_tr
    y_tr = w_br / 2 + w_tr
    top.rect(-xe - 40, -42, xe + 40, 42, "sio2", "SiO2 cladding, extent drafted", stated("Sec. III", "PECVD SiO2 bottom and top cladding"), layer="oxide", alpha=0.8)
    top.poly(rounded(-row_len / 2 - und, -y_tr - und, row_len / 2 + und, y_tr + und, und), "air", "Si undercut under the oxide (seen through it)", src_und, layer="trench", alpha=0.3)
    for s in (-1, 1):
        for i in range(n_tr):
            x0 = -row_len / 2 + i * (l_tr + g_tr)
            y0, y1 = (w_br / 2, y_tr) if s > 0 else (-y_tr, -w_br / 2)
            top.rect(x0, y0, x0 + l_tr, y1, "air", f"deep trench {'upper' if s > 0 else 'lower'} row: size and count from PS1, context", src_tr, layer="trench")
    src_post = stated("Appendix p.15-16", "incomplete undercut modelled with 2 x 2 um posts between the anchors") + assumed("position follows the assumed trench rows")
    for i in range(n_tr - 1):
        xp = -row_len / 2 + i * (l_tr + g_tr) + l_tr + g_tr / 2
        top.rect(xp - 1, -1, xp + 1, 1, "si", "Si post between the anchors, as modelled by the authors", src_post, layer="substrate", lod=2.0)
    top.line([(-xe, -w_br / 2), (xe, -w_br / 2), (xe, w_br / 2), (-xe, w_br / 2), (-xe, -w_br / 2)], "suspended region, 15.4 x 984 um (Table I)", stated("Table I", "suspended region area"))
    for i, (yy, w) in enumerate(zip(ys, ws, strict=True)):
        top.rect(-xe, yy - w / 2, xe, yy + w / 2, "sin", f"pass {i + 1} of 7 under the heater, {w * 1000:.0f} nm, cut at the bridge end", src_pass, layer="waveguide")
    top.rect(-L_h / 2, -w_h / 2, L_h / 2, w_h / 2, "metal", "TiN heater", row("m20", "m21"), layer="metal", alpha=0.45)
    top.dim("h", -L_h / 2, L_h / 2, -y_tr - und, px=-18, ext=(-w_h / 2, -w_h / 2), row_id="m20")
    top.dim("h", -xe, xe, y_tr + und, px=16, ext=(w_br / 2, w_br / 2), text="984 um", src=stated("Table I", "suspended region length"))
    top.note("Routing outside the bridge is not shown: the paper has no plan view of PS3 (Fig. 1(a) and Fig. 2(a) are PS1). So no loopbacks, leads, pads, MMIs or reference arm; the passes are cut where they leave the bridge.")
    top.note("Dashed: trench rows, undercut outline and posts are context. PS3 has trenches and anchors, but their size is given for PS1 and their count for PS3 is not given.")
    c.thumb = {"view": "top", "window": [-520, -60, -220, 60]}

    an = c.view("end", "detail: left end of the bridge, heater narrower than the seven passes", like="top", window=(-xe - 30, -30, -xe + 110, 30))
    an.dim("v", -w_br / 2, w_br / 2, -xe + 95, px=0, ext=(-xe + 95, -xe + 95), text="15.4 um", src=stated("Table I", "suspended region width"))
    an.dim("v", -w_h / 2, w_h / 2, -xe + 60, px=0, ext=(-xe + 60, -xe + 60), row_id="m21")
    an.note("The heater (10 um) is narrower than the array (11.4 um): the outer passes run past its edges, as in the XTEM of PS3. Gaps in the dashed trench rows are the SiO2 anchors.")

    # section at a trench centre; plan +y on the left, the first pass on the left as Fig. 1(b)
    def bridge_poly() -> list[tuple[float, float]]:
        z_flank = t_bot + t_sin + h_gap + t_tin + t_above
        z_top = z_flank + t_plat
        chamfer = 0.3
        return [(-b_bot / 2, 0), (b_bot / 2, 0), (b_top / 2, z_flank), (w_plat / 2 + chamfer, z_flank), (w_plat / 2, z_top), (-w_plat / 2, z_top), (-w_plat / 2 - chamfer, z_flank), (-b_top / 2, z_flank)]

    def half_ellipse(cx: float, a: float, b: float) -> list[tuple[float, float]]:
        return [(cx + a * math.cos(math.radians(t)), b * math.sin(math.radians(t))) for t in range(180, 361, 6)]

    z_core = t_bot
    z_tin = z_core + t_sin + h_gap
    z_flank = z_tin + t_tin + t_above
    half_x = 30.0
    x = c.view("xsec", "cross-section through a trench: trapezoid bridge over the undercut Si (XTEM wafer)", "xsec", window=(-half_x, -22.5, half_x, z_flank + 2.5))
    src_ox = stated("p.8", "3.25 um bottom cladding on the XTEM wafer; trapezoidal section")
    x.rect(-half_x, -22.5, half_x, 0, "si", "Si substrate: truncated", stated("Sec. III", "Si substrate") + assumed("thickness not stated: truncated"), layer="substrate", alpha=0.55)
    cx_und = w_br / 2 + w_tr / 2
    a_und = w_tr / 2 + und
    src_ell = stated("Sec. II p.5, Appendix", "elliptical channels on the trench rows, 8 um lateral and 18 um vertical from the trench edges") + assumed("channel centre follows the PS1 trench width")
    for s in (-1, 1):
        x.poly(half_ellipse(s * cx_und, a_und, und_z), "air", "undercut channel in the Si", src_ell, layer="trench")
    for s in (-1, 1):
        x.rect(s * (w_br / 2 + w_tr), 0, s * half_x, z_flank, "sio2", "oxide beyond the trench: outer wall not in the XTEM, placed at the PS1 trench width", src_ox + assumed("the XTEM lamella does not reach the outer wall; PS1 trench width used, not labelled"), layer="oxide")
    x.poly(bridge_poly(), "sio2", "suspended SiO2 bridge: trapezoid", fig("Fig. 2(c)", "outline against the 5 um bar: 16.2 um at the base, 14.65 um at the top, plateau 10.25 um", "3 %") + src_ox, layer="oxide")
    for i, (yy, w) in enumerate(zip(ys, ws, strict=True)):
        x.rect(-yy - w / 2, z_core, -yy + w / 2, z_core + t_sin, "sin", f"pass {i + 1}, {w * 1000:.0f} nm design", row("m24", "m25") + stated("p.6, p.8", "design width; XTEM about 100 nm narrower"), layer="waveguide")
    x.rect(-w_h / 2, z_tin, w_h / 2, z_tin + t_tin, "metal", "TiN heater", row("m21", "m23") + fig("Fig. 1(b)", "150 nm label, PS1"), layer="metal")
    x.dim("h", -w_br / 2, w_br / 2, z_flank + t_plat, px=16, ext=(z_flank, z_flank), text="15.4 um (mean)", src=stated("Table I", "suspended region width"))
    x.dim("v", -und_z, 0, cx_und, px=0, ext=(cx_und, cx_und), text="18 um", src=stated("Sec. II p.5, Appendix", "model undercut depth"))
    x.label((0.0, -8.0), "Si", tip="Si left between the two channels")
    x.note("Trapezoid and plateau from the XTEM of PS3. The lamella does not reach the outer trench wall: oxide beyond the trench is dashed, at the PS1 width, not labelled.")
    x.note("Undercut as the authors' thermal model: elliptical channels. They just meet on the axis at the Si surface: 15.4 um bridge against 2 x 8 um lateral reach.")

    xa = c.view("xsec_anchor", "cross-section at an anchor: oxide continuous, 2 x 2 um Si post on the axis", "xsec", window=(-half_x, -22.5, half_x, z_flank + 2.5))
    xa.rect(-half_x, -22.5, half_x, 0, "si", "Si substrate: truncated", stated("Sec. III", "Si substrate") + assumed("thickness not stated: truncated"), layer="substrate", alpha=0.55)
    src_ell_a = stated("Appendix p.15-16", "incomplete undercut directly between the anchors") + assumed("channel shape at the anchor plane not stated: same depth, inner edge at the post")
    a_a = (w_br / 2 + w_tr + und - 1.0) / 2
    for s in (-1, 1):
        xa.poly(half_ellipse(s * (1.0 + a_a), a_a, und_z), "air", "undercut channel, anchor plane", src_ell_a, layer="trench")
    xa.rect(-half_x, 0, half_x, z_flank, "sio2", "SiO2 anchor: oxide continuous across", stated("Appendix p.15", "SiO2 anchors of PS3") + src_ox, layer="oxide")
    for i, (yy, w) in enumerate(zip(ys, ws, strict=True)):
        xa.rect(-yy - w / 2, z_core, -yy + w / 2, z_core + t_sin, "sin", f"pass {i + 1}", row("m24", "m25"), layer="waveguide")
    xa.rect(-w_h / 2, z_tin, w_h / 2, z_tin + t_tin, "metal", "TiN heater", row("m21", "m23"), layer="metal")
    xa.rect(-1, -6, 1, 0, "si", "Si post between the anchors, 2 x 2 um in the authors' model", stated("Appendix p.15-16", "2 x 2 um Si posts connect the beam to the substrate"), layer="substrate")
    xa.dim("h", -1, 1, 0, px=-14, ext=(0, 0), text="2 um", src=stated("Appendix", "post size, modelled"))
    xa.note("With the PS1 anchor gap, the bridge axis lies 8.26 um from the nearest trench corner, just past the 8 um undercut reach, so Si survives here in PS3; in PS1 it is 5.1 um and clears. The posts are the authors' model, not an observation.")

    core = c.view("core", "detail: seven passes under the TiN heater, XTEM values", "xsec", like="xsec", window=(-8.6, z_core - 0.8, 8.6, z_flank + 0.7))
    core.dim("v", z_core + t_sin, z_tin, 6.4, px=0, ext=(6.4, 6.4), row_id="m23")
    x_last = -ys[-1] + ws[-1] / 2
    core.dim("v", z_core, z_core + t_sin, x_last, px=14, ext=(x_last, x_last), row_id="m24")
    core.dim("h", -w_h / 2, w_h / 2, z_tin + t_tin, px=14, ext=(z_tin + t_tin, z_tin + t_tin), row_id="m21")
    x_0 = -ys[0] + ws[0] / 2
    core.dim("h", x_0, x_0 + gap, z_core, px=-14, ext=(z_core, z_core), text="1.2 um", src=stated("p.5 Sec. II", "design gap; XTEM about 100 nm larger"))
    x_e = -ys[0] - ws[0] / 2
    core.dim("h", -w_br / 2, x_e, z_core, px=-30, ext=(z_core, z_core), text="2 um", src=stated("p.8", "edge waveguide to bridge edge, as designed"))
    for i, (yy, w) in enumerate(zip(ys, ws, strict=True)):
        core.label((-yy, z_core + t_sin), f"{w * 1000:.0f}", dy=-6, tip=f"pass {i + 1} design width, nm")
    core.note("Thickness and heater separation are the XTEM values of the rows (second wafer, 3.25 um cladding); widths are design values, about 100 nm wider than the XTEM (p.8). Alternation order 600 / 650 / 550 repeated from Fig. 1(b), starting at 600: the only start giving 15.4 um.")

    # closure
    c.check("total waveguide under the heater, 7 x heater length against the row, um", n * L_h, L_wg, 0.005)
    c.check("heater length against the stated region length, um", L_h, L_br, 0.001)
    c.check("bridge width from array and margins, array + 2 x 2 um against Table I, um", array + 2 * margin, w_br, 0.001)
    c.check("XTEM bridge, mean of top and bottom against Table I, um", (b_bot + b_top) / 2, w_br, 0.005)
    c.check("XTEM pass pitch, 598 px / 6 at 54.6 px/um against design centre pitch (reading +- 1.5 %), um", 598 / 6 / 54.6, sum(cycle) / 3 + gap, 0.02)
    c.check("XTEM TiN width, 548 px at 54.6 px/um against the row, um", 548 / 54.6, w_h, 0.01)
    c.check("XTEM SiN centre to TiN underside, 105 px against the row, um", 105 / 54.6, h_gap + t_sin / 2, 0.03)
    c.check("heater resistance at the assumed 10 ohm/sq x 98.38 squares against the simulation value, ohm", 10.0 * L_h / w_h, 983.8, 0.001)
    c.check("measured over simulated resistance: PS3 864/983.8 against PS1 1050/1190", c.num("m19") / 983.8, 1050.0 / 1190.0, 0.01)
    c.check("PS1 undercut length, 9 x 46 + 8 x 6 + 16 against 481 um in Fig. 2(a), um", 9 * l_tr + 8 * g_tr + 2 * und, 312 * UM_PX, 0.01)
    c.check("axis to trench corner in PS3 against the 8 um reach (slightly beyond: Si remains), um", math.hypot(w_br / 2, g_tr / 2), und, 0.05)
    c.check("oxide stack on the XTEM wafer, cladding + SiN + separation + TiN + 0.62 um against 6.17 um in Fig. 2(c), um", z_flank, 6.17, 0.05)
    return c
