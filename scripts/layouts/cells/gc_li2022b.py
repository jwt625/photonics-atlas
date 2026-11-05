"""TFLN uniform grating coupler for 532 nm (Fig. 1(a), Fig. 1(b), Fig. 2(a), Fig. 2(d), p.2 text).

Fig. 2(d) SEM: straight teeth with rounded ends, free-standing on the etched slab (the field around them has the same contrast
as the gaps), so the bright stadiums are the unetched LN ridges and the labelled 172.4 nm is the tooth: 0.6 x 288. 21 teeth are
in the frame; it does not show either end of the grating along the propagation, so the drawing breaks there.
Layout follows Fig. 1(b) and the SEM: teeth along x, light leaves along -y through the taper, a long straight (Fig. 1(a), about
370 um in Fig. 1(b)), then the 90 deg Euler bend toward the MMI. The grating width is read against the labelled period, not the
scale bar: the bar gives a period of 357 nm against the 288.0 nm label and the table.
The sources do not agree on the taper mouth: text 5 um, SEM teeth 8.0 um, Fig. 1(a) mouth equal to the grating. The piece from
the grating width to 5 um is a dashed bridge on the same slope, not a published shape.
Forward diffraction (n_eff = lambda / p + sin 10 deg) puts the fiber leaning away from the waveguide, as Fig. 2(a).
The GC run is at 90 deg to the modulator (the Euler bend), so on x-cut LN the TE field here lies along y: ordinary index.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Pt, Route, arc, assumed, fig, rect, row, stated  # noqa: E402

ID = "cmp_li2022b_gc_532"


def slab_te0(n_core: float, n_low: float, n_top: float, t_um: float, lam_um: float) -> float:
    """TE0 effective index of a three-layer slab, by bisection on the dispersion relation."""

    def f(n: float) -> float:
        kt = 2 * math.pi / lam_um * math.sqrt(n_core**2 - n**2)
        return kt * t_um - math.atan(math.sqrt(n**2 - n_low**2) / math.sqrt(n_core**2 - n**2)) - math.atan(math.sqrt(n**2 - n_top**2) / math.sqrt(n_core**2 - n**2))

    a, b = max(n_low, n_top) + 1e-6, n_core - 1e-6
    for _ in range(80):
        m = (a + b) / 2
        if f(m) > 0:
            a = m
        else:
            b = m
    return (a + b) / 2


def stadium(xc: float, yc: float, length: float, width: float, tol: float = 0.004) -> list[Pt]:
    """A bar along x with semicircular ends, centred at (xc, yc)."""
    r = width / 2
    return arc((xc + length / 2 - r, yc), r, -90, 90, tol) + arc((xc - length / 2 + r, yc), r, 90, 270, tol)


def euler_90(rt: Route, r_max: float, r_min: float, sweep_deg: float, n: int = 60) -> float:
    """Clothoid pair: curvature linear from 1/r_max to 1/r_min at mid sweep, then back. Returns the path length added."""
    k0, k1 = 1 / r_max, 1 / r_min
    half = math.radians(abs(sweep_deg)) / 2 / ((k0 + k1) / 2)  # length of one half, angle = length x mean curvature
    sign = 1.0 if sweep_deg > 0 else -1.0
    ds = 2 * half / n
    start = rt.length
    for i in range(n):
        s = (i + 0.5) * ds
        k = k0 + (k1 - k0) * (s / half if s <= half else (2 * half - s) / half)
        rt.arc(1 / k, sign * math.degrees(k * ds))
    return rt.length - start


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 1(a)", "Fig. 1(b)", "Fig. 2(a)", "Fig. 2(d) SEM", "Fig. 4(a)", "Fig. 5(a)", "p.2 Sec. 2"],
        "Uniform TFLN GC: rounded free-standing teeth (21 in the SEM frame, ends not shown), taper to 0.3 um, long straight, 90 deg Euler bend; 60 deg teeth in the section",
    )
    p = c.um("m4")
    ff = c.num("m5")
    etch = c.um("m8")
    t_ln = c.um("m9")
    t_box = c.um("m10")
    w_wg = c.um("m11")
    t_slab = c.um("m12")
    mfd = c.um("m7")
    theta = abs(c.num("m6"))
    lam = 0.532
    alpha = 60.0  # p.2: flank angle used for the LN etch
    w_taper = 5.0  # p.2: taper starts at 5 um
    t_clad = 0.3  # p.2: SiO2 over the film, removed at the GC ports
    n_teeth = 21  # Fig. 2(d): count in the frame, not the total
    # Fig. 2(d), pixels of the embedded image: tooth rows repeat every 16.25 px, tooth length 449 px, scale bar 45.5 px
    px_period, px_len = 16.25, 449.0
    w_gr = px_len / px_period * p
    px_um = 3300.0 / 370.0  # Fig. 1(b): the 3.3 mm electrode straight spans 370 px, 8.9 um/px
    l_run = 41.5 * px_um  # Fig. 1(b): GC box edge to the start of the bend, 41.5 px
    l_taper_all = l_run / 3.2  # Fig. 1(a): taper to long straight about 1 : 2.2, a schematic; length not stated
    l_bridge = l_taper_all * (w_gr - w_taper) / (w_gr - w_wg)  # same slope from the grating width down to the stated 5 um
    l_taper = l_taper_all - l_bridge
    band = 1.0  # break drawn past each frame edge of Fig. 2(d)
    tooth = ff * p  # at mid height: in the SEM the bright sidewall rings are centred about 0.54 p apart, outer edge about 0.71 p
    inset = etch / math.tan(math.radians(alpha))  # per sidewall
    top_w = tooth - inset
    foot = tooth + inset
    lg = n_teeth * p

    src_tooth = row("m4", "m5") + fig("Fig. 2(d)", f"{n_teeth} rounded teeth in the frame; length against the labelled period, 8.0 um; by the scale bar it would be 9.9 um", "25 %")
    src_top_flat = src_tooth + stated("p.2", "60 deg sidewall, 100 nm etch: top narrower than the foot by 115 nm")
    src_taper = row("m11") + stated("p.2 Sec. 2", "taper 5 to 0.3 um after the GC") + fig("Fig. 1(a)") + assumed("taper length not stated; 1 : 2.2 against the straight, ratio of the Fig. 1(a) schematic")
    src_bridge = assumed("no source: text mouth 5 um, SEM teeth 8.0 um (9.9 um by the bar), Fig. 1(a) draws the mouth equal to the grating; bridged on the taper slope")
    src_straight = row("m11") + fig("Fig. 1(a)", "taper, long straight, then bend") + fig("Fig. 1(b)", f"GC box edge to bend 41.5 px at {px_um:.1f} um/px against the 3.3 mm electrode: {l_run:.0f} um", "15 %")
    src_beyond = assumed("past the Fig. 2(d) frame: the frame shows no end of the grating along the propagation")
    src_euler = row("m11") + stated("p.2 Sec. 2", "90 deg Euler bend, R max 150 um, R min 50 um, width 0.3 um") + fig("Fig. 1(b)", "bend turns from the GC run toward the MMI")

    top = c.view("top", "plan: grating, taper, Euler bend, true scale (orientation of Fig. 1(b) and Fig. 2(d))")
    y_gr0 = band  # first tooth in the frame, on the taper side
    # bridge, taper and straight from the grating down, then the bend toward +x
    rt_b = Route((0.0, 0.0), -90.0, w_gr, tol=0.01)
    rt_b.straight(l_bridge, w_taper)
    rt_t = Route(rt_b.pos, -90.0, w_taper, tol=0.01)
    rt_t.straight(l_taper, w_wg)
    rt_s = Route(rt_t.pos, -90.0, w_wg, tol=0.01)
    rt_s.to((0.0, -l_run))
    rt = Route(rt_s.pos, -90.0, w_wg, tol=0.01)
    euler_90(rt, 150.0, 50.0, 90.0)
    x_bend = rt.pos[0]
    y_bend1 = rt.pos[1]
    rt.straight(25.0)

    xr0, xr1, yr0, yr1 = -20.0, max(q[0] for q in rt.pts) + 2.0, min(q[1] for q in rt.pts) - 20.0, 2 * band + lg + 18.0
    top.rect(xr0, yr0, xr1, yr1, "ln", "LN slab, 100 nm left by the 100 nm etch", row("m12") + fig("Fig. 2(a)", "continuous film under the grating"), layer="slab", alpha=0.28)
    win = rect(-9.0, -3.0, 9.0, 2 * band + lg + 5.0)
    top.rings([rect(xr0, yr0, xr1, yr1), win], "sio2", "300 nm SiO2 over-cladding, opened above the GC", stated("p.2-3", "300 nm SiO2; removed over the GC ports by wet etching") + assumed("window outline not stated"), layer="oxide", alpha=0.3)
    top.route(rt_b, "ln", "bridge from the grating width to 5 um", src_bridge, layer="waveguide", alpha=0.6)
    top.route(rt_t, "ln", "taper, 5 to 0.3 um", src_taper, layer="waveguide")
    top.route(rt_s, "ln", "0.3 um straight between the taper and the bend", src_straight, layer="waveguide")
    top.route(rt, "ln", "90 deg Euler bend, then the truncated 0.3 um waveguide", src_euler, layer="waveguide")
    gr_fill = rect(-w_gr / 2, y_gr0, w_gr / 2, y_gr0 + lg)
    top.rect(-w_gr / 2, 0, w_gr / 2, band, "ln", "past the frame, toward the taper: not shown in any figure", src_beyond, layer="slab", alpha=0.1)
    top.rect(-w_gr / 2, y_gr0 + lg, w_gr / 2, y_gr0 + lg + band, "ln", "past the frame, far end: not shown in any figure", src_beyond, layer="slab", alpha=0.1)
    for y_edge in (y_gr0, y_gr0 + lg):
        top.line([(-w_gr / 2 - 0.6, y_edge), (w_gr / 2 + 0.6, y_edge)], "edge of the Fig. 2(d) frame", fig("Fig. 2(d)", "top tooth about 3.7 px below the frame edge, bottom tooth against the banner"))
    top.poly(gr_fill, "ln", "grating area, 100 nm etched between the teeth", row("m8") + src_tooth, layer="slab", alpha=0.12)
    for i in range(n_teeth):
        yc = y_gr0 + (p - foot) + foot / 2 + i * p  # a groove separates the first tooth from the taper
        top.poly(stadium(0.0, yc, w_gr, foot), "ln", f"tooth {i + 1} of {n_teeth} in the frame: foot", src_tooth, layer="waveguide", alpha=0.55, lod=foot)
        top.poly(stadium(0.0, yc, w_gr - 2 * inset, top_w), "ln", f"tooth {i + 1}: flat top", src_top_flat, layer="waveguide", alpha=1.0, lod=top_w)
    top.note("Taper length is not stated; bend and width are. The straight is read off Fig. 1(b) from the GC box edge, about 370 um; where the grating sits in that box is unknown. Routing past the bend to the MMI truncated.")
    top.note("Fig. 2(d) rotated with the drawing as in Fig. 1(b): teeth along x, propagation along y.")
    top.label((rt.pts[-1][0], rt.pts[-1][1]), "0.3 um to the MMI", anchor="end", dy=-8, row_id="m11")

    g = c.view("grating", "detail: the grating as in the SEM of Fig. 2(d): 21 teeth in the frame", like="top", window=(-w_gr / 2 - 1.2, -0.9, w_gr / 2 + 1.2, 2 * band + lg + 0.6))
    g.dim("v", y_gr0, y_gr0 + lg, -w_gr / 2, px=-16, ext=(-w_gr / 2, -w_gr / 2), text="21 in the frame", src=fig("Fig. 2(d)", "teeth counted in the frame"))
    g.dim("h", -w_gr / 2, w_gr / 2, y_gr0 + lg, px=30, ext=(y_gr0 + lg, y_gr0 + lg), text="8.0 um", src=fig("Fig. 2(d)", "449 / 16.25 periods against the 288.0 nm label; 9.9 um by the scale bar", "25 %"))
    g.dim("v", y_gr0 + 10 * p, y_gr0 + 11 * p, w_gr / 2, px=12, ext=(w_gr / 2, w_gr / 2), row_id="m4")
    g.note("Lines mark the frame edges: top tooth about 3.7 px below the frame edge, bottom tooth against the banner. The frame shows no end of the grating along the propagation, so the total count is unknown; the pale bands stand for what lies past it.")
    g.note("SEM: period labelled 288.0 nm and tooth labelled 172.4 nm. Against the scale bar the same period reads 357 nm; the label and the table are drawn.")

    e = c.view("ends", "detail: rounded tooth ends, 60 deg flanks, as the left edge of Fig. 2(d)", like="top", window=(-w_gr / 2 - 0.5, 2.0, -w_gr / 2 + 1.9, 3.5))
    e.dim("v", y_gr0 + (p - foot) + 4 * p, y_gr0 + (p - foot) + 5 * p, -w_gr / 2 + 1.5, px=8, ext=(-w_gr / 2 + 1.5, -w_gr / 2 + 1.5), row_id="m4")
    e.note("The dark band between the teeth is the etched 58 nm floor; the field past the tooth ends is the same etched slab, as in the SEM.")

    m = c.view("mouth", "detail: grating width to taper mouth: the sources disagree, dashed", like="top", window=(-8.0, -l_bridge - 16.0, 8.0, 2 * band + lg + 2.0))
    m.dim("h", -w_taper / 2, w_taper / 2, -l_bridge, px=-40, ext=(-l_bridge, -l_bridge), text="5 um", src=stated("p.2 Sec. 2", "taper start"))
    m.note("Text: taper starts at 5 um. SEM: teeth 8.0 um against the period label, 9.9 um by the bar; at 5 um the SEM period would read 181 nm. Fig. 1(a) draws the mouth equal to the grating. Unresolved: no step and no bridge is published.")
    b = c.view("bend", "detail: 90 deg Euler bend, R max 150 um, R min 50 um", like="top", window=(-30.0, y_bend1 - 15.0, x_bend + 30.0, -l_run + 15.0))
    b.note("Clothoid pair, curvature from 1/150 to 1/50 um-1 and back. 0.3 um wide (p.2).")

    # the section as Fig. 2(a): fiber on the left leaning away from the waveguide on the right
    s = c.view("section", "section along the propagation, as Fig. 2(a), true scale", "xsec", window=(-3.0, -t_box - 0.7, 2 * band + lg + 7.0, 5.2))
    xa, xb = -6.0, 2 * band + lg + 12.0
    x_g0 = band
    x_g1 = band + lg
    s.rect(xa, -t_box - 3.0, xb, -t_box, "si", "Si substrate (truncated)", assumed("thickness not stated"), layer="substrate", alpha=0.6)
    s.rect(xa, -t_box, xb, 0.0, "sio2", "thermal oxide", row("m10"), layer="oxide")
    s.rect(xa, 0.0, xb, t_slab, "ln", "LN, 100 nm remaining", row("m12"), layer="slab")
    s.rect(xa, t_slab, 0.0, t_ln, "ln", "LN film beyond the far end", fig("Fig. 2(a)", "full film beyond the teeth in the sketch") + src_beyond, layer="waveguide", alpha=0.5)
    s.rect(x_g1 + band, t_slab, xb, t_ln, "ln", "LN taper, unetched", row("m9") + stated("p.2 Sec. 2", "taper to the waveguide"), layer="waveguide")
    for x_edge in (x_g0, x_g1):
        s.line([(x_edge, 0.0), (x_edge, t_ln + 0.5)], "edge of the Fig. 2(d) frame", fig("Fig. 2(d)"))
    for i in range(n_teeth):
        xs = x_g0 + i * p
        s.poly([(xs, t_slab), (xs + foot, t_slab), (xs + foot - inset, t_ln), (xs + inset, t_ln)], "ln", f"tooth {i + 1} in the frame: 60 deg sidewalls", row("m4", "m5", "m8") + stated("p.2", "sidewall angle 60 deg"), layer="waveguide", lod=foot)
    x_open = x_g1 + band + 3.0
    s.rect(x_open, t_ln, xb, t_ln + t_clad, "sio2", "300 nm SiO2 over-cladding, removed over the GC", stated("p.2-3", "300 nm; wet-etched open over the ports") + assumed("edge of the opening not stated"), layer="oxide", alpha=0.75)
    xf = x_g0 + lg / 2
    th = math.radians(theta)
    far = 5.0 / math.cos(th)
    src_beam = row("m6", "m7") + fig("Fig. 2(a)", "fiber axis leaning left of the normal")
    s.line([(xf, t_ln), (xf - far * math.sin(th), t_ln + far * math.cos(th))], "fiber axis, 10 deg from the normal", src_beam)
    s.line([(xf, t_ln), (xf, t_ln + far)], "chip normal", fig("Fig. 2(a)", "normal drawn as in the figure"))
    for side in (-1, 1):
        p0 = (xf + side * mfd / 2 / math.cos(th), t_ln)  # 3.6 um across the beam, measured square to the axis
        s.line([p0, (p0[0] - far * math.sin(th), p0[1] + far * math.cos(th))], "Gaussian beam edge, 3.6 um diameter", row("m7"))
    s.dim("v", -t_box, 0, x_g1 + band + 6.0, px=8, ext=(x_g1 + band + 6.0, x_g1 + band + 6.0), row_id="m10")
    s.label((xf - far * math.sin(th) - 2.0, t_ln + far * math.cos(th) - 0.5), "fiber", anchor="end", row_id="m6")
    s.label((x_g1 + band + 5.0, t_ln + t_clad), "SiO2", anchor="middle", dy=-6)
    s.label((xf, -t_box / 2), "thermal oxide", anchor="middle")
    s.note("21 teeth in the frame of Fig. 2(d), between the two lines; what lies past each line is not shown in any figure and Fig. 2(a) is a sketch.")
    s.note("Waveguide on the right so that 10 deg is forward diffraction: backward would need n_eff 1.67, below the 100 nm slab index.")

    t = c.view("teeth", "detail: teeth, 100 nm etch, 60 deg sidewalls", "xsec", like="section", window=(x_g0 - 0.45, -0.18, x_g0 + 1.5, t_ln + 0.14))
    t.dim("h", x_g0 + p, x_g0 + 2 * p, t_ln, px=16, ext=(t_ln, t_ln), row_id="m4")
    t.dim("v", 0, t_slab, x_g0 + 1.45, px=-6, ext=(x_g0 + 1.45, x_g0 + 1.45), row_id="m12")
    t.dim("v", t_slab, t_ln, x_g0 + 3 * p + foot / 2, px=20, ext=(x_g0 + 3 * p + foot / 2, x_g0 + 3 * p + foot / 2), row_id="m8")
    t.note("Duty 0.6 taken at mid height (173 nm, the SEM label 172.4 nm): foot 231 nm, flat top 115 nm, floor 58 nm. The paper does not say where it is measured; the SEM edge rings fit mid height.")

    # waveguide cross-section after the taper
    w = c.view("xsec", "cross-section: 0.3 um LN ridge after the taper", "xsec")
    xw = 2.2
    w.rect(-xw, -t_box - 0.5, xw, -t_box, "si", "Si substrate (truncated)", assumed("thickness not stated"), layer="substrate", alpha=0.6)
    w.rect(-xw, -t_box, xw, 0, "sio2", "thermal oxide", row("m10"), layer="oxide")
    foot_r = w_wg / 2
    top_r = w_wg / 2 - inset
    w.poly([(-xw, 0), (xw, 0), (xw, t_slab), (foot_r, t_slab), (top_r, t_ln), (-top_r, t_ln), (-foot_r, t_slab), (-xw, t_slab)], "ln", "LN ridge and slab", row("m9", "m11", "m12") + stated("p.2", "60 deg sidewall"), layer="waveguide")
    w.poly([(-xw, t_slab), (-foot_r, t_slab), (-top_r, t_ln), (top_r, t_ln), (foot_r, t_slab), (xw, t_slab), (xw, t_slab + t_clad), (foot_r + 0.0, t_slab + t_clad), (top_r, t_ln + t_clad), (-top_r, t_ln + t_clad), (-foot_r, t_slab + t_clad), (-xw, t_slab + t_clad)], "sio2", "300 nm SiO2 over-cladding", stated("p.2", "300 nm") + fig("Fig. 4(a)", "over-cladding follows the ridge in the modulator section"), layer="oxide", alpha=0.7)
    w.dim("h", -foot_r, foot_r, t_slab, px=-22, ext=(t_slab, t_slab), row_id="m11")
    w.dim("v", 0, t_slab, -xw, px=-8, ext=(-xw, -xw), row_id="m12")
    w.dim("v", t_slab, t_ln, top_r + 0.5, px=8, ext=(top_r, top_r), row_id="m8")
    w.dim("v", -t_box, 0, xw, px=8, ext=(xw, xw), row_id="m10")
    w.note("0.3 um taken at the ridge foot: Fig. 4(a) puts the w arrow just under the foot, tip to tip about the foot width (modulator section). The 60 deg flank then leaves 185 nm at the top.")

    # closure
    c.check("tooth width um, 0.6 x 288 nm, against the SEM label 172.4 nm", tooth, 0.1724, 0.005)
    c.check("Euler bend extent along x um (R 150 to 50 um) against Fig. 1(b), 8 px at 8.9 um/px, blurred", x_bend, 8.0 * px_um, 0.2)
    implied = lam / p + math.sin(math.radians(theta))
    n_ln, n_ox = 2.323, 1.46  # ordinary index at 532 nm: GC run along z of the x-cut film, TE along y
    n_full = slab_te0(n_ln, n_ox, 1.0, t_ln, lam)
    n_etch = slab_te0(n_ln, n_ox, 1.0, t_slab, lam)
    c.check("forward-diffraction n_eff at 532 nm, 288 nm, 10 deg, against fill-weighted TE slab index (n LN ordinary 2.323, SiO2 1.46 assumed; air above)", implied, ff * n_full + (1 - ff) * n_etch, 0.03)
    assert lam / p - math.sin(math.radians(theta)) < n_etch, "backward diffraction would need an index below the slab"
    c.thumb = {"view": "ends", "window": [-w_gr / 2 - 0.6, 2.0, -w_gr / 2 + 2.4, 3.2]}
    return c
