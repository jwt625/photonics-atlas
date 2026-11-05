"""Device 5 of a 2015 dense dissimilar-waveguide thermo-optic MZI switch on 220 nm SOI, underetched (Fig. 5(a)-(d), Table 1, Sec. 3).

Topology from Fig. 5(a) and the micrograph Fig. 5(b): both arms carry the same N-pass serpentine with side-by-side fingers
that all point up. The input lead feeds the lowest pass; odd passes run right, even passes run left; the last (top) pass
turns up first, runs over all right-hand fingers and comes back down to the output splitter. The reference arm repeats the
folds with its passes in a bundle below; its last pass goes over the right-hand fingers too, then around a U below to the
output splitter.

Fig. 5(a) is drawn for N = 5. Fig. 5(b) has four fingers each side plus the outer exit loop, so N = 9, and its oxide opening
is 90 um long against the scale fixed by the 8 + 12 + 8 um section of Fig. 5(c): device 4 (N = 9, L = 90 um). Device 5 is the
same with L = 290 um, which is the stated footprint difference (600 to 800 um at the same 180 um). Finger positions are
readings from Fig. 5(b), counted from the ends of the opening, so they carry over to L = 290 um.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, arc, assumed, fig, row, stated  # noqa: E402

ID = "cmp_lit_murray2015_dev5_underetched"

# Fig. 5(b): um per pixel of the embedded micrograph, from the 8 + 12 + 8 um band across the opening (106 px, Fig. 5(c)).
UM_PX = 28.0 / 106.0
BEND_R = 5.0  # U bend outer leg to leg 38 px = 10 um; corners read the same
# Right side, counted from the opening end: outer exit loop legs, then finger legs (left, right), and finger tops above the
# heater axis (upper arm) and in the lower group (reference arm). All from Fig. 5(b), +- 1 um.
RIGHT_LEGS = [(7.4, 17.4), (20.5, 30.5), (33.6, 43.6), (46.7, 56.7)]  # F1 .. F4, inner to outer
RIGHT_TOP = [67.3, 65.5, 62.8, 61.2]
RIGHT_TOP_REF = [-13.7, -15.3, -17.7, -19.3]
LEFT_LEGS = [(5.3, 15.3), (18.4, 28.4), (31.5, 41.5), (44.6, 54.6)]  # counted outward from the left end of the opening
LEFT_TOP = [68.1, 66.5, 64.2, 62.6]
LEFT_TOP_REF = [-12.7, -14.5, -16.6, -18.5]
EXIT_IN, EXIT_OUT = 5.3, 59.7  # outer exit loop legs, right side
EXIT_TOP, EXIT_TOP_REF = 72.1, -8.4
TIP_L, TIP_R = 64.7, 76.0  # x of the splitter arm tips from the opening ends
TIP_UP, TIP_DN = -13.2, -76.8  # y of the splitter arm tips
SPLIT_Y = -45.0  # y of the splitter stems
REF_LOW = -84.5  # y of the lowest reference pass
EXIT_REF_LOW = -85.0  # y of the U under the reference exit
ARM_R = 13.0  # splitter arm curve, tip to junction
ARM_W = 1.3  # splitter arm band, half of the 2.6 um stem
TAPER_L = 11.0  # Fig. 5(a) inset: width change along the return leg, 150 px against the 130 px = 10 um finger


def rounded(x0: float, y0: float, x1: float, y1: float, r: float) -> list[tuple[float, float]]:
    return (
        arc((x1 - r, y0 + r), r, -90, 0, tol=0.1)
        + arc((x1 - r, y1 - r), r, 0, 90, tol=0.1)
        + arc((x0 + r, y1 - r), r, 90, 180, tol=0.1)
        + arc((x0 + r, y0 + r), r, 180, 270, tol=0.1)
    )


def arm(L: float, ys: list[float], ws: list[float], top_r: list[float], top_l: list[float], exit_top: float, ref: bool) -> Route:
    """One MZI arm, left splitter tip to right splitter tip. ys, ws: pass y and width, lowest pass first."""
    n = len(ys)
    y1 = ys[0]
    x_tip = -L / 2 - TIP_L
    rt = Route((x_tip, TIP_DN if ref else TIP_UP), -90.0 if ref else 90.0, ws[0], tol=0.01)
    rt.to((x_tip, y1 + BEND_R if ref else y1 - BEND_R))
    rt.arc(BEND_R, 90.0 if ref else -90.0)
    for k in range(1, n):  # k = 1 is the lowest pass; pass k connects to pass k + 1
        y_next = ys[k]
        w_next = ws[k]
        if k % 2 == 1:  # running right: finger on the right, outermost for the lowest pass
            f = (n - 1 - k) // 2
            x_in, x_out = L / 2 + RIGHT_LEGS[f][0], L / 2 + RIGHT_LEGS[f][1]
            top = top_r[f]
            rt.to((x_out - BEND_R, ys[k - 1]))
            rt.arc(BEND_R, 90.0)
            y_now = rt.pos[1]
            rt.straight(top - BEND_R - y_now)
            rt.arc(BEND_R, 180.0)
            rt.straight(top - BEND_R - (y_next + BEND_R) - TAPER_L)
            rt.straight(TAPER_L, w_next)
            rt.arc(BEND_R, -90.0)
            assert abs(rt.pos[0] - (x_in - BEND_R)) < 1e-6
        else:  # running left: finger on the left, outermost for the second pass
            f = (n - 1 - k) // 2
            x_in, x_out = -L / 2 - LEFT_LEGS[f][0], -L / 2 - LEFT_LEGS[f][1]
            top = top_l[f]
            rt.to((x_out + BEND_R, ys[k - 1]))
            rt.arc(BEND_R, -90.0)
            y_now = rt.pos[1]
            rt.straight(top - BEND_R - y_now)
            rt.arc(BEND_R, -180.0)
            rt.straight(top - BEND_R - (y_next + BEND_R) - TAPER_L)
            rt.straight(TAPER_L, w_next)
            rt.arc(BEND_R, 90.0)
            assert abs(rt.pos[0] - (x_in + BEND_R)) < 1e-6
    # last (top) pass: up at once, over the right-hand fingers, down the far side
    rt.to((L / 2 + EXIT_IN - BEND_R, ys[-1]))
    rt.arc(BEND_R, 90.0)
    rt.to((L / 2 + EXIT_IN, exit_top - BEND_R))
    rt.arc(BEND_R, -90.0)
    rt.to((L / 2 + EXIT_OUT - BEND_R, exit_top))
    rt.arc(BEND_R, -90.0)
    if ref:
        rt.to((L / 2 + EXIT_OUT, EXIT_REF_LOW + BEND_R))
        rt.arc(BEND_R, 90.0)
        rt.to((L / 2 + TIP_R - BEND_R, EXIT_REF_LOW))
        rt.arc(BEND_R, 90.0)
        rt.to((L / 2 + TIP_R, TIP_DN))
    else:
        rt.to((L / 2 + EXIT_OUT, y1 + BEND_R))
        rt.arc(BEND_R, 90.0)
        rt.to((L / 2 + TIP_R - BEND_R, y1))
        rt.arc(BEND_R, -90.0)
        rt.to((L / 2 + TIP_R, TIP_UP))
    return rt


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 5(a) with inset", "Fig. 5(b) micrograph (N = 9, L = 90 um)", "Fig. 5(c)", "Fig. 5(d)", "Table 1", "Sec. 3"],
        "9-pass dissimilar serpentine in both MZI arms, 290 um heater on a 12 um bridge between 8 um oxide openings, routing metal, adiabatic splitters",
    )
    L = c.um("m6")
    w_h = c.um("m7")
    gap = c.um("m8")
    t_si = c.um("m9")
    m = re.search(r"pass order ([\d, ]+) nm", c.metric("m11")["condition"])
    assert m
    ws = [float(x) / 1000 for x in m.group(1).split(",")]
    n = len(ws)
    w_bridge, w_open, t_ox = 12.0, 8.0, 6.0  # Fig. 5(c), (d) labels and Sec. 3
    foot = c.num("m10") / 180.0  # 800 um: footprint row over the stated 180 um height

    total = sum(ws) + (n - 1) * gap
    ys: list[float] = []
    y = -total / 2
    for w in ws:
        ys.append(y + w / 2)
        y += w + gap
    ys_ref = [yy - ys[0] + REF_LOW for yy in ys]

    src_fold = row("m6", "m8", "m11") + fig("Fig. 5(b), device 4 micrograph (L = 90 um)", "finger legs and tops against the 8 + 12 + 8 um band, counted from the opening ends", "1 um") + fig("Fig. 5(a)", "serpentine order, all fingers up")
    src_ref = fig("Fig. 5(a); Fig. 5(b), device 4 micrograph (L = 90 um)", "reference arm folds and lower bundle, 1 um pitch", "1 um") + assumed("reference pass widths taken equal to the heated arm: drawn identical in Fig. 5(a), not stated")
    src_taper = fig("Fig. 5(a) inset", "w1 kept through the U bend, tapered to w2 on the return leg just before the corner", "30 %")

    top = c.view("top", "top view: whole switch at true scale, stems to the 800 um footprint")
    # cladding, undercut, openings: paint below the waveguides
    y_top, y_bot = 98.0, -92.0
    x_l_chip = -L / 2 - TIP_L - ARM_R - (foot - (L + TIP_L + TIP_R + 2 * ARM_R)) / 2
    top.rect(x_l_chip, y_bot, x_l_chip + foot, y_top, "sio2", "oxide cladding, drawn to the footprint", stated("Fig. 5(c), (d)", "oxide around the waveguides"), layer="oxide", alpha=0.8)
    und = 8.0  # Fig. 5(b): grey band outside the opening, 30 px
    y_open = w_bridge / 2 + w_open
    top.poly(rounded(-L / 2 - und, -y_open - und, L / 2 + und, y_open + und, und), "air", "Si undercut seen through the oxide", fig("Fig. 5(b), device 4 micrograph (L = 90 um)", "rounded grey outline, 8 um beyond the opening; length carried to L = 290 um", "1 um"), layer="trench", alpha=0.3)
    src_open = stated("Fig. 5(c), (d)", "8 um openings beside the 12 um bridge") + row("m6") + fig("Fig. 5(a); Fig. 5(b), device 4 micrograph (L = 90 um)", "opening length equals L: 89.5 um measured", "2 um")
    top.rect(-L / 2, w_bridge / 2, L / 2, y_open, "air", "oxide opening, upper", src_open, layer="trench")
    top.rect(-L / 2, -y_open, L / 2, -w_bridge / 2, "air", "oxide opening, lower", src_open, layer="trench")

    up = arm(L, ys, ws, RIGHT_TOP, LEFT_TOP, EXIT_TOP, False)
    dn = arm(L, ys_ref, ws, RIGHT_TOP_REF, LEFT_TOP_REF, EXIT_TOP_REF, True)
    top.route(up, "si", "heated arm: 9 passes under the heater, widths 500 to 650 nm", src_fold + src_taper, layer="waveguide")
    top.route(dn, "si", "reference arm: same folds, passes in the lower bundle", src_ref + src_taper, layer="waveguide")

    # adiabatic splitters: arm tip outward; rib and slab of the coupler not resolved, drawn as one band
    src_split = fig("Fig. 5(b), device 4 micrograph (L = 90 um)", "arm curve, tip to junction, band width", "30 %") + stated("Sec. 3", "50-50 adiabatic splitters, details in ref. [22]")
    x_tl, x_tr = -L / 2 - TIP_L, L / 2 + TIP_R
    half = (TIP_UP - TIP_DN) / 2
    stem = (foot - (x_tr + ARM_R - x_tl + ARM_R)) / 2
    for side in (-1, 1):
        x_tip = x_tr if side > 0 else x_tl
        for up_arm in (True, False):
            start_y = TIP_UP if up_arm else TIP_DN
            head = -90.0 if up_arm else 90.0
            r = Route((x_tip, start_y), head, ws[0], tol=0.01)
            r.straight(half - ARM_R - ARM_W / 2, ARM_W)
            sweep = (90.0 if up_arm else -90.0) * side
            r.arc(ARM_R, sweep)
            top.route(r, "si", "adiabatic 50-50 splitter arm", src_split, layer="waveguide")
    x_jl, x_jr = x_tl - ARM_R, x_tr + ARM_R
    vis = 30.0  # Fig. 5(b): stems visible 113 px to the image edge
    for s, x_j in ((-1, x_jl), (1, x_jr)):
        top.rect(min(x_j, x_j + s * vis), SPLIT_Y - ARM_W, max(x_j, x_j + s * vis), SPLIT_Y + ARM_W, "si", "splitter stem", src_split, layer="waveguide")
        top.rect(min(x_j + s * vis, x_j + s * stem), SPLIT_Y - ARM_W, max(x_j + s * vis, x_j + s * stem), SPLIT_Y + ARM_W, "si", "splitter stem beyond the micrograph", assumed("Fig. 5(b) ends here; run to the stated 800 um footprint; coupler region of ref. [22] not detailed"), layer="waveguide")
    # heater and contacts
    src_heater = row("m6", "m7") + fig("Fig. 5(a); Fig. 5(b), device 4 micrograph (L = 90 um)", "centred on the bridge, spans L between the contacts", "2 um")
    top.rect(-L / 2, -w_h / 2, L / 2, w_h / 2, "metal", "heater metal (material not stated)", src_heater, layer="metal", alpha=0.5)
    pad = 10.5  # Fig. 5(b): 40 px square, outer edge flush with the opening end
    via = 5.3  # Fig. 5(b): 20 px inner square
    src_pad = fig("Fig. 5(b), device 4 micrograph (L = 90 um)", "contact square against the 8 + 12 + 8 um band", "1 um")
    for s in (-1, 1):
        cx = s * (L / 2 - pad / 2)
        top.rect(cx - pad / 2, -pad / 2, cx + pad / 2, pad / 2, "metal", "heater contact to routing metal", src_pad, layer="metal")
        top.rect(cx - via / 2, -via / 2, cx + via / 2, via / 2, "contact", "via, heater to routing metal", src_pad, layer="via")
    # routing metal: left lead turns up in Fig. 5(b); right lead runs straight on
    lead = 7.5  # Fig. 5(b): 27 to 30 px
    x_up = -L / 2 - 80.0  # Fig. 5(b): 303 px from the opening end
    y_end = 95.0  # top edge of the micrograph
    x_right = x_jr + stem
    src_lead = fig("Fig. 5(b), device 4 micrograph (L = 90 um)", "routing metal path and width", "1 um") + fig("Fig. 5(a)", "same path: left lead up, right lead on")
    top.poly([(-L / 2 + pad, -lead / 2), (-L / 2 + pad, lead / 2), (x_up + lead / 2, lead / 2), (x_up + lead / 2, y_end), (x_up - lead / 2, y_end), (x_up - lead / 2, -lead / 2)], "metal", "routing metal, left: truncated at the micrograph edge", src_lead, layer="metal")
    top.rect(L / 2 - pad, -lead / 2, x_right, lead / 2, "metal", "routing metal, right: truncated at the footprint edge", src_lead, layer="metal")

    y_low = EXIT_REF_LOW
    top.dim("h", -L / 2, L / 2, y_low, px=-24, ext=(-y_open, -y_open), row_id="m6")
    top.label((x_jl - stem, SPLIT_Y), "input", anchor="start", dy=-10)
    top.label((x_jr + stem, SPLIT_Y), "output", anchor="end", dy=-10)
    top.label((0.0, y_open + und), "heater, 8 um openings, undercut", dy=-10)
    top.label((0.0, ys_ref[-1]), "reference arm", dy=-10)
    top.note("Fig. 5(a) is the N = 5 schematic; finger positions are from the micrograph Fig. 5(b), a 9-pass device with L = 90 um (device 4). The extra 200 um of device 5 is added between the fingers.")
    top.note("Dummy metal fill squares and the unlabelled darker rectangle around the heater in Fig. 5(b) are not drawn: their extent for L = 290 um is not known.")
    top.note("Stems beyond 30 um are not in the micrograph: run out to the stated 800 um. Fig. 5(a) marks a single input and output; the adiabatic coupler region of ref. [22] is not detailed here.")
    c.thumb = {"view": "top", "window": [-L / 2 - 95, -96, L / 2 + 100, 96]}

    det = c.view("right", "detail: right end, finger legs at 2 um spacing, exit loop over the fingers, reference folds", like="top", window=(L / 2 - 22, -92, L / 2 + 100, 78))
    det.note("Heated passes leave the bridge at the top; each finger is a pair of legs 10 um apart with 5 um U bends. The outermost loop carries the last pass to the output.")
    det2 = c.view("left", "detail: left end, input lead under the fingers, routing metal turning up", like="top", window=(-L / 2 - 100, -92, -L / 2 + 22, 78))
    det2.note("The input lead enters as the lowest pass, under all the left-hand fingers.")
    end = c.view("end", "detail: heater end, contact, oxide openings, passes turning up", like="top", window=(L / 2 - 26, -16, L / 2 + 26, 16))
    end.dim("v", -w_h / 2, w_h / 2, L / 2 - 22, px=0, ext=(L / 2 - 22, L / 2 - 22), row_id="m7")
    end.note("Each pass keeps its width through the U bend and tapers to the next pass's width on the return leg, just before the corner (Fig. 5(a) inset). The change is below a pixel at this zoom.")

    # cross-section at mid heater: Fig. 5(d), plan y across, w1 on the left, seen from the output end
    x = c.view("xsec", "cross-section at mid heater (Fig. 5(d)), seen from the output end, w1 on the left", "xsec", window=(-19, -4.5, 19, 7.5))
    half_x = 19.0
    z_core = 2.9  # Fig. 5(d): core bottom above the oxide base, 124 px at 43 px/um
    z_h0, z_h1 = 5.0, 5.53  # Fig. 5(d): heater, 215 and 238 px
    dep = 2.1  # Fig. 5(d): undercut floor below the oxide base, 90 px
    src_ux = fig("Fig. 5(d)", "schematic undercut floor, 90 px against the 6 um label", "30 %")
    x.rect(-half_x, -4.5, half_x, -dep, "si", "Si substrate: truncated", assumed("substrate thickness not stated: truncated"), layer="substrate", alpha=0.5)
    x.rect(-half_x, -dep, -w_bridge / 2 - w_open, 0, "si", "Si substrate beside the undercut", src_ux, layer="substrate", alpha=0.5)
    x.rect(w_bridge / 2 + w_open, -dep, half_x, 0, "si", "Si substrate beside the undercut", src_ux, layer="substrate", alpha=0.5)
    x.rect(-w_bridge / 2 - w_open, -dep, w_bridge / 2 + w_open, 0, "air", "undercut: Si removed under the bridge", src_ux + stated("Sec. 3", "substrate removed under a 12 um bridge"), layer="trench")
    src_ox = stated("Fig. 5(c), (d)", "6 um oxide, 12 um bridge, 8 um openings")
    x.rect(-half_x, 0, -w_bridge / 2 - w_open, t_ox, "sio2", "oxide beyond the opening", src_ox, layer="oxide")
    x.rect(w_bridge / 2 + w_open, 0, half_x, t_ox, "sio2", "oxide beyond the opening", src_ox, layer="oxide")
    x.rect(-w_bridge / 2 - w_open, 0, -w_bridge / 2, t_ox, "air", "oxide opening", src_ox, layer="trench")
    x.rect(w_bridge / 2, 0, w_bridge / 2 + w_open, t_ox, "air", "oxide opening", src_ox, layer="trench")
    x.rect(-w_bridge / 2, 0, w_bridge / 2, t_ox, "sio2", "suspended oxide bridge", src_ox, layer="oxide")
    src_core = row("m8", "m9", "m11") + fig("Fig. 5(d)", "height of the core layer in the oxide, schematic", "20 %")
    for i, (yy, w) in enumerate(zip(ys, ws, strict=True)):
        x.rect(yy - w / 2, z_core, yy + w / 2, z_core + t_si, "si", f"pass {i + 1}: {w * 1000:.0f} nm wide, 220 nm thick", src_core, layer="waveguide")
    x.rect(-w_h / 2, z_h0, w_h / 2, z_h1, "metal", "heater (material not stated)", row("m7") + fig("Fig. 5(d)", "height and thickness in the oxide, schematic", "20 %"), layer="metal")
    x.dim("h", -w_bridge / 2, w_bridge / 2, 0, px=-18, ext=(0, 0), text="12 um bridge", src=stated("p.7 Sec. 3", "bridge width"))
    x.dim("h", w_bridge / 2, w_bridge / 2 + w_open, t_ox, px=14, ext=(t_ox, t_ox), text="8 um", src=stated("Fig. 5(c), (d)", "opening width"))
    x.dim("v", 0, t_ox, -w_bridge / 2, px=-12, ext=(-w_bridge / 2, -w_bridge / 2), text="6 um", src=stated("Fig. 5(c), (d)", "oxide thickness"))
    x.dim("h", -w_h / 2, w_h / 2, z_h1, px=16, ext=(z_h1, z_h1), row_id="m7")
    x.note("Fig. 5(d) is a schematic with labelled 6, 8, 10 and 12 um; core and heater heights and the undercut floor are read from it at 43 px/um and are not to be taken as process values.")
    x.note("Fig. 5(d) shows vertical undercut walls at the outer edge of the openings; the micrograph Fig. 5(b) shows a further 8 um of lateral undercut (see top view). Both are as the paper shows them.")

    xz = c.view("core", "detail: the nine passes under the heater", "xsec", like="xsec", window=(-5.4, 2.2, 5.4, 5.9))
    xz.dim("h", ys[0] + ws[0] / 2, ys[1] - ws[1] / 2, z_core, px=-14, ext=(z_core, z_core), row_id="m8")
    xz.dim("v", z_core, z_core + t_si, ys[-1] + ws[-1] / 2, px=14, ext=(ys[-1] + ws[-1] / 2, ys[-1] + ws[-1] / 2), row_id="m9")
    for i, (yy, w) in enumerate(zip(ys, ws, strict=True)):
        xz.label((yy, z_core + t_si), f"{w * 1000:.0f}", dy=-6, tip=f"pass {i + 1} width, nm (row m11 condition, Table 1)")
    xz.note("Pass order left to right is Table 1 order w1 to w9; which pass is the input is read from Fig. 5(a) (lowest in plan), and the order in the section is the schematic's.")

    # closure
    c.check("micrograph opening length at the 28 um band scale against L = 90 um of device 4, um", 339 * UM_PX, 90.0, 0.02)
    drawn_h = EXIT_TOP - EXIT_REF_LOW
    c.check("drawn height from Fig. 5(b) readings against the stated upper bound 180 um (reading excludes margin)", drawn_h, 180.0, 0.15)
    min_adj = min(abs(ws[i + 1] - ws[i]) for i in range(n - 1))
    min_nxt = min(abs(ws[i + 2] - ws[i]) for i in range(n - 2))
    c.check("adjacent passes differ by at least 100 nm (Sec. 3), nm", min_adj * 1000, 100.0, 1e-6)
    c.check("next-adjacent passes differ by at least 50 nm (Sec. 3), nm", min_nxt * 1000, 50.0, 1e-6)
    c.check("widths against the row range: minimum, um", min(ws), c.um("m11") - (float(c.metric("m11")["value_max"]) - float(c.metric("m11")["value"])) / 2 * 1e-3, 1e-6)
    c.check("arm imbalance from Fig. 5(b) readings, reference over heated arm (no stated value; reading limit 1 %)", dn.length, up.length, 0.01)
    return c
