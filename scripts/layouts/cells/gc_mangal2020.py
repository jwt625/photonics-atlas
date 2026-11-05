"""Mangal 2020 downward Si grating coupler with Ti/Al top reflector, thinned substrate and SiN backside AR (Fig. 3(a), Sec. III-A).

The paper has no plan view: Fig. 3(a) is a section, so the section is the drawing. The plan is computed here but not published
(build.py NOT_DRAWN). In Fig. 3(a)
the rays lean along the propagation direction both up to the reflector and down into the BOX, which is forward diffraction:
n_eff = lambda / period + sin(10 deg), checked here against the fill-weighted slab index of the 220 / 150 nm grating.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, assumed, circle, fig, row, stated  # noqa: E402

ID = "cmp_lit_mangal2020_downward_gc_reflector"


def slab_te0(n_core: float, n_low: float, n_top: float, t_um: float, lam_um: float) -> float:
    """TE0 effective index of a three-layer slab, by bisection on the dispersion relation."""

    def f(n: float) -> float:
        kt = 2 * math.pi / lam_um * math.sqrt(n_core**2 - n**2)
        return kt * t_um - math.atan(math.sqrt(n**2 - n_low**2) / math.sqrt(n_core**2 - n**2)) - math.atan(math.sqrt(n**2 - n_top**2) / math.sqrt(n_core**2 - n**2))

    a, b = max(n_low, n_top) + 1e-6, n_core - 1e-6
    for _ in range(80):
        m = (a + b) / 2
        if f(m) > 0:  # phase left over: the mode index is higher
            a = m
        else:
            b = m
    return (a + b) / 2


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 2 (concept section)", "Fig. 3(a) (stack section)", "Fig. 3(b)", "Fig. 12 inset", "Sec. III-A", "Sec. III-B", "Sec. IV-A", "p.7 Sec. V (Ti thickness)"],
        "Downward GC section: 70 nm etch in 220 nm Si, 2 um oxide to Ti/Al reflector, 2 um BOX, 100 um thinned Si, 170 nm SiN AR, beam through the substrate",
    )
    p = c.um("m4")
    ff = c.num("m5")
    etch = c.um("m6")
    t_si = c.um("m7")
    t_box = c.um("m8")
    t_ox = c.um("m9")
    theta_air = c.num("m10")
    mfd = c.um("m3")
    t_sub = 100.0  # Fig. 3(a) and Sec. III-A, no row
    t_ar = 0.170  # Fig. 3(a) and p.3, no row
    t_ti = 0.005  # p.7: the Fig. 3(b) device has the 5 nm Ti adhesion layer (later reduced to 2 nm)
    lam = 1.31  # p.7: primary O-band wavelength
    theta_si = 2.81  # p.3 Sec. III-A
    n_ox, n_si = 1.447, 3.50
    theta_ox = math.degrees(math.asin(math.sin(math.radians(theta_air)) / n_ox))

    n_per = 30  # the paper gives no period count; Fig. 3(a) is a schematic with six teeth
    w_grating = 12.0  # beam MFD 9.2 um; grating width not stated
    l_taper = 60.0
    w_wg = 0.45
    lg = n_per * p
    tooth = ff * p

    src_teeth_top = row("m4", "m5") + assumed("plan not in the paper: teeth drawn straight, count and width chosen to hold the stated 9.2 um beam")
    src_plan = assumed("plan not in the paper: waveguide width, taper length and grating footprint not stated")

    # --- section first: this is what the paper shows
    s = c.view("section", "section along the waveguide, as Fig. 3(a), true scale", "xsec", window=(-3.5, -3.0 - t_box + 1.0, lg + 3.5, t_si + t_ox + 0.9))
    x0, x1 = -8.0, lg + 8.0
    y_top_si = t_si
    y_ox = y_top_si + t_ox
    y_box = -t_box
    s.rect(x0, y_box - 8, x1, y_box, "si", "bulk Si substrate (truncated here, 100 um in the next view)", stated("p.3 Sec. III-A", "100 um after thinning"), layer="substrate")
    s.rect(x0, y_box, x1, 0, "sio2", "BOX", row("m8"), layer="oxide")
    s.rect(x0, 0, x1, y_ox, "sio2", "PECVD SiO2 cladding", row("m9") + fig("Fig. 3(a)", "PECVD SiO2 fills the grooves"), layer="oxide", alpha=0.6)
    s.rect(x0, 0, 0, t_si, "si", "Si waveguide, 220 nm", row("m7"), layer="waveguide")
    s.rect(0, 0, x1, t_si - etch, "si", "partially etched Si, 150 nm under the grooves", row("m6", "m7"), layer="slab")
    for i in range(n_per):
        xa = i * p + (p - tooth)
        extra = [] if i < 6 else assumed("period count not in the paper: Fig. 3(a) draws six teeth, drafted out to hold the 9.2 um beam")
        s.rect(xa, t_si - etch, xa + tooth, t_si, "si", f"tooth {i + 1}", row("m4", "m5", "m6") + fig("Fig. 3(a)", "rectangular teeth standing on the partially etched Si") + extra, layer="waveguide", lod=tooth)
    s.rect(x0, y_ox, x1, y_ox + t_ti, "metal", "Ti adhesion layer, 5 nm", stated("p.7 Sec. V", "5 nm Ti of this device, 2 nm in the later improved one"), layer="metal")
    s.rect(x0, y_ox + t_ti, x1, y_ox + t_ti + 0.25, "metal", "Al reflector", fig("Fig. 3(a)", "Al over the oxide above the grating") + assumed("Al thickness not stated"), layer="metal")

    # rays as in Fig. 3(a): up to the reflector and back, and straight down; forward leaning
    tan_ox, tan_si = math.tan(math.radians(theta_ox)), math.tan(math.radians(theta_si))
    src_ray = row("m10") + fig("Fig. 3(a)", "ray topology") + stated("p.3 Sec. III-A", "2.81 deg in Si") + assumed("angle in oxide by Snell, n 1.447")
    for k, xs in enumerate((lg * 0.25, lg * 0.5, lg * 0.75)):
        up = (xs + (y_ox - t_si / 2) * tan_ox, y_ox)
        down = (up[0] + (y_ox - y_box) * tan_ox, y_box)
        s.line([(xs, t_si / 2), up, down, (down[0] + 2.2 * tan_si, y_box - 2.2)], f"reflected ray {k + 1}", src_ray)
        d2 = (xs + (t_si / 2 - y_box) * tan_ox, y_box)
        s.line([(xs, t_si / 2), d2, (d2[0] + 2.2 * tan_si, y_box - 2.2)], f"direct downward ray {k + 1}", src_ray)
    s.dim("v", 0, t_si, -3.3, px=-8, ext=(0, 0), row_id="m7")
    s.dim("v", y_box, 0, lg + 3.2, px=10, ext=(lg, lg), row_id="m8")
    s.dim("v", t_si, y_ox, lg + 3.2, px=10, ext=(lg, lg), row_id="m9")
    s.label((-3.2, y_ox - 0.5), "PECVD SiO2", anchor="start")
    s.label((-3.2, -1.0), "BOX", anchor="start")
    s.label((lg + 3.2, y_ox + 0.3), "Ti/Al reflector", anchor="end", dy=-6)
    s.label((lg / 2, y_box - 1.2), "Si substrate, thinned to 100 um", anchor="middle")
    s.label((-1.8, t_si / 2), "input", anchor="middle", dy=-9, tip="Input waveguide on the left, as in Fig. 3(a)")
    s.note("Fig. 3(a) is a schematic with six teeth (solid here); the dashed teeth carry the table period, fill and etch, their count is drafted to hold the 9.2 um beam.")
    s.note("Rays show the Fig. 3(a) topology at the real angles. Oxide angle by Snell from 10 deg in air.")

    t = c.view("teeth", "detail: teeth, period and etch at the start of the grating", "xsec", like="section", window=(-0.9, -0.25, 3.3, t_si + 0.30))
    t.dim("h", p - tooth, p + p - tooth, t_si, px=18, ext=(t_si, t_si), row_id="m4")
    t.dim("v", t_si - etch, t_si, p + 0.03, px=20, ext=(t_si, t_si), row_id="m6")
    t.dim("v", 0, t_si, -0.1, px=-8, ext=(0, 0), row_id="m7")
    t.note("Tooth width is fill 0.5 x 490 nm; the paper defines fill only in the Fig. 3 caption, the tooth / groove convention does not change the 0.5.")

    ti = c.view("reflector", "detail: Ti adhesion layer under the Al reflector", "xsec", like="section", window=(0.0, y_ox - 0.03, 0.16, y_ox + 0.04))
    ti.dim("v", y_ox, y_ox + t_ti, 0.08, px=14, ext=(0.08, 0.08), text="5 nm Ti", src=stated("p.7 Sec. V", "Ti adhesion layer between Al and top oxide"))
    ti.label((0.03, y_ox + 0.025), "Al", anchor="middle")
    ti.label((0.03, y_ox - 0.015), "SiO2", anchor="middle")
    ti.note("Ti absorbs: the same paper reports better directionality with 2 nm Ti; that improved device is not this row.")

    # --- whole chip thickness, true scale: the beam crosses 100 um of Si
    th = c.view("through", "section through the chip: beam from grating to backside, true scale", "xsec")
    xa, xb = -22.0, 40.0
    y_back = y_box - t_sub
    xc = lg / 2
    th.rect(xa, y_back, xb, y_box, "si", "bulk Si substrate, thinned and polished", stated("p.3 Sec. III-A", "100 um") + fig("Fig. 3(a)", "100 um arrow"), layer="substrate")
    th.rect(xa, y_box, xb, y_ox, "sio2", "BOX and top oxide", row("m8", "m9"), layer="oxide")
    th.rect(xa, 0, xb, t_si, "si", "Si device layer", row("m7"), layer="waveguide")
    th.rect(xa, y_ox, xb, y_ox + t_ti + 0.25, "metal", "Ti/Al reflector", fig("Fig. 3(a)") + assumed("Al thickness not stated"), layer="metal")
    th.rect(xa, y_back - t_ar, xb, y_back, "sin", "SiN AR coating", stated("p.3 Sec. III-A", "170 nm") + fig("Fig. 3(a)"), layer="overlay")

    # Gaussian expansion in Si: the paper quotes 9.2 um at the grating and 10.4 um at the backside
    w0 = mfd / 2
    zr = math.pi * w0**2 * n_si / lam
    d_back = 2 * w0 * math.sqrt(1 + (t_sub / zr) ** 2)
    c.check("beam diameter at the backside um, Gaussian from row MFD through 100 um of Si (n 3.50 assumed)", d_back, 10.4, 0.03)
    src_beam = row("m3", "m10") + stated("p.3 Sec. III-B", "9.2 um at the grating, 10.4 um at 100 um") + stated("p.3 Sec. III-A", "2.81 deg in Si")
    x_enter = xc + (0 - y_box) * tan_ox
    x_back = x_enter + t_sub * tan_si
    pts_l, pts_r = [], []
    for i in range(0, 21):
        z = t_sub * i / 20
        w = w0 * math.sqrt(1 + (z / zr) ** 2)
        xm = x_enter + z * tan_si
        pts_l.append((xm - w, y_box - z))
        pts_r.append((xm + w, y_box - z))
    th.line(pts_l, "1/e2 beam edge in Si", src_beam)
    th.line(pts_r, "1/e2 beam edge in Si", src_beam)
    tan_air = math.tan(math.radians(theta_air))
    th.line([(x_enter, y_box), (x_back, y_back), (x_back + 24 * tan_air, y_back - 24)], "beam axis: 2.81 deg in Si, 10 deg in air", row("m10") + stated("p.3 Sec. III-A", "2.81 deg in Si"))
    th.dim("v", y_back, y_box, xa, px=-14, ext=(xa, xa), text="100 um", src=stated("p.3 Sec. III-A", "thinned Si substrate"))
    th.dim("h", x_back - d_back / 2, x_back + d_back / 2, y_back, px=-16, ext=(y_back, y_back), text="10.4 um", src=stated("p.3 Sec. III-B", "beam diameter at the end of the substrate"))
    th.dim("h", xc - mfd / 2, xc + mfd / 2, y_ox, px=16, ext=(y_ox, y_ox), row_id="m3")
    th.label((x_back + 24 * tan_air, y_back - 22), "10 deg in air", anchor="start", dx=8, row_id="m10", tip="To a backside fiber (Fig. 3(b)) or the ball lens (Fig. 2)")
    th.note("Light leaves through the polished backside; the ball lens, package via and polymer waveguide of Fig. 2 follow below and are not this component.")

    ar = c.view("backside", "detail: 170 nm SiN AR coating at the polished backside", "xsec", like="through", window=(xa, y_back - 0.6, xa + 3.0, y_back + 0.5))
    ar.dim("v", y_back - t_ar, y_back, xa + 1.5, px=14, ext=(xa + 1.5, xa + 1.5), text="170 nm", src=stated("p.3 Sec. III-A", "SiN AR coating"))
    ar.note("With the coating the Fresnel ripple drops and the peak improves by 1.5 dB (Fig. 3(b)).")

    # --- plan, drafted around the section
    top = c.view("top", "plan view: not in the paper, drafted (dashed) with table period and fill")
    ym = w_grating / 2
    top.rect(0, -ym, lg + 1.0, ym, "si", "partially etched grating area, 150 nm Si", row("m6", "m7") + src_plan, layer="slab", alpha=0.6)
    for i in range(n_per):
        xa2 = i * p + (p - tooth)
        top.rect(xa2, -ym, xa2 + tooth, ym, "si", f"tooth {i + 1} of {n_per}", src_teeth_top, layer="waveguide", lod=tooth)
    taper = [(-l_taper, -w_wg / 2), (0, -ym), (0, ym), (-l_taper, w_wg / 2)]
    top.poly(taper, "si", "linear taper", src_plan, layer="waveguide")
    top.rect(-l_taper - 16, -w_wg / 2, -l_taper, w_wg / 2, "si", "input waveguide, truncated", src_plan, layer="waveguide")
    top.rect(-5, -14, lg + 5, 14, "metal", "Ti/Al reflector over the output grating", stated("p.5 Sec. IV-A", "reflector post-processed over the grating; not on the fiber-attached input grating") + assumed("patch extent not stated"), layer="metal", alpha=0.18)
    xb0 = lg / 2
    top.line(circle((xb0, 0), mfd / 2, tol=0.05) + [(xb0 + mfd / 2, 0)], "beam at the grating, 9.2 um MFD", row("m3"))
    top.label((xb0, mfd / 2), "beam", anchor="middle", dy=-6, row_id="m3")
    top.note("The paper has no plan view and does not say straight or focusing: teeth are drawn straight and every plan dimension except period and fill is dashed.")
    top.note("Fiber-attached input grating and Si routing are not this component.")
    det = c.view("grating", "plan detail: grating and beam footprint", like="top", window=(-4, -9, lg + 4, 9))
    det.note("Period and fill from the table; extent drafted to hold the beam.")

    # closure
    c.check("implied angle in Si from Snell, 10 deg in air, Si n 3.50 (deg)", math.degrees(math.asin(math.sin(math.radians(theta_air)) / n_si)), theta_si, 0.02)
    n_full = slab_te0(n_si, n_ox, n_ox, t_si, lam)
    n_etch = slab_te0(n_si, n_ox, n_ox, t_si - etch, lam)
    implied = lam / p + math.sin(math.radians(theta_air))
    c.check("forward-diffraction n_eff from period and 10 deg at 1310 nm, against fill-weighted TE slab index (n Si 3.50, SiO2 1.447 assumed)", implied, ff * n_full + (1 - ff) * n_etch, 0.03)
    c.thumb = {"view": "section", "window": [-1.5, y_box - 1.2, 18.0, y_ox + 0.9]}
    return c
