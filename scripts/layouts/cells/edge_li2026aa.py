"""Li 2026 bi-layer LN taper under a SiON rib: spot-size converter to UHNA4 fiber (Fig. 2(a), Fig. 2(b), Table 1, Fig. 1(b), Methods).

Topology from Fig. 2(b), whose x axis is to scale with Table 1 and whose y axis is not:
s1: the 120 nm LN slab layer widens from the 0.2 um tip to w3 = 2.1 um; no ridge yet.
s2: slab constant at w3; the upper 180 nm ridge starts at its own 0.2 um tip and widens to w4 = 0.8 um.
s3: ridge constant at w4; the slab flares from w3 to w5 = 5 um and meets the full LN film.
The SiON rib (w6 4.4 um, 1 um slab + 3.2 um rib) runs over all of it; all outside the outline is etched to the BOX.
Widths are top widths: p.3 gives 0.8 um as a top width in the SSC region and p.2 a 60 deg sidewall, so the 180 nm ridge has a 1.0 um foot.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, assumed, circle, fig, row, stated  # noqa: E402

ID = "cmp_li2026aa_ssc"


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 1(b) SEM and micrograph", "Fig. 2(a)", "Fig. 2(a) inset", "Fig. 2(b)", "Table 1", "p.2 text", "p.8 Methods"],
        "Bi-layer LN taper (slab tip, ridge tip, flare) under the SiON rib: Table 1 lengths and widths, four cross-sections at their planes",
    )
    w1 = c.um("m12")  # both tips
    s1, s2, s3 = c.um("m13"), c.um("m14"), c.um("m15")
    w6 = c.um("m16")
    t_sion = c.um("m17")
    t_ln = c.um("m21")
    t_slab = c.um("m22")
    w4 = c.um("m23")
    t_box = c.um("m24")
    t_clad = c.um("m25")
    h2 = c.um("m26")
    h1 = t_sion - h2
    w3, w5 = 2.1, 5.0  # Table 1, no rows
    # Fig. 2(a) inset, pixels at 900 dpi render: rib width 430, slab width 790, rib height 300, slab height 85 (the inset is to scale)
    w_sion_slab = 790.0 / 430.0 * w6
    x_facet = -49.0  # Fig. 2(b): the panel ends 150 px left of the tip at 3.06 px/um; a panel edge, no facet is marked there
    inset_r = (t_ln - t_slab) / math.tan(math.radians(60.0))  # p.2: 60 deg sidewall, upper 180 nm
    inset_s = t_slab / math.tan(math.radians(60.0))  # lower 120 nm, same angle assumed
    x_lnedge = s1 + s2 + s3
    x_end = x_lnedge + 40.0
    x_sion_end = x_lnedge + 15.0  # no source: Fig. 2(a) shows the rib running a little past the LN edge

    src_t1 = stated("p.4 Table 1", "w3 2.1, w5 5 um")
    src_outline = row("m12", "m13", "m14", "m15", "m23") + src_t1 + fig("Fig. 2(b)", "outline of the slab layer")
    slab_outline = [
        (0.0, -w1 / 2), (s1, -w3 / 2), (s1 + s2, -w3 / 2), (x_lnedge, -w5 / 2),
        (x_lnedge, w5 / 2), (s1 + s2, w3 / 2), (s1, w3 / 2), (0.0, w1 / 2),
    ]  # fmt: skip
    ridge = [(s1, -w1 / 2), (s1 + s2, -w4 / 2), (x_end, -w4 / 2), (x_end, w4 / 2), (s1 + s2, w4 / 2), (s1, w1 / 2)]

    top = c.view("top", "plan: SSC at true scale, 500 um taper under the 4.4 um SiON rib")
    ybg = 10.0
    src_sslab = row("m26") + fig("Fig. 2(a) inset", "slab width against w6", "10 %")
    src_srib = row("m16", "m17") + fig("Fig. 2(a)", "rib runs over the whole taper")
    no_start = assumed("SiON start: Fig. 2(b) panel edge, 49 um before the tip; no facet is marked there and the distance is not stated")
    no_end = assumed("SiON end past the LN edge: Fig. 2(a) shows it going a little past, the length has no source")
    top.rect(0, -w_sion_slab / 2, x_lnedge, w_sion_slab / 2, "sion", "SiON slab, 1 um", src_sslab, layer="overlay", alpha=0.35)
    top.rect(0, -w6 / 2, x_lnedge, w6 / 2, "sion", "SiON rib", src_srib, layer="overlay", alpha=0.55)
    for xa, xb, why in ((x_facet, 0.0, no_start), (x_lnedge, x_sion_end, no_end)):
        top.rect(xa, -w_sion_slab / 2, xb, w_sion_slab / 2, "sion", "SiON slab, extent not stated", src_sslab + why, layer="overlay", alpha=0.35)
        top.rect(xa, -w6 / 2, xb, w6 / 2, "sion", "SiON rib, extent not stated", src_srib + why, layer="overlay", alpha=0.55)
    top.rect(x_lnedge, -ybg, x_end, ybg, "ln", "full LN slab after the taper", row("m22") + fig("Fig. 2(b)", "full film begins at the end of s3") + fig("Fig. 1(b) SEM", "vertical film edge at the wide end"), layer="slab", alpha=0.55)
    top.poly(slab_outline, "ln", "LN lower layer: 120 nm slab, tip w1, width w3, flare to w5", src_outline, layer="slab", alpha=0.7)
    top.poly(ridge, "ln", "LN upper layer: ridge tip w2 to w4", row("m12", "m14", "m23") + fig("Fig. 2(b)", "ridge starts at the end of s1"), layer="waveguide")
    top.line([(x_facet, -ybg), (x_facet, ybg)], "end of the drawn SiON: the panel edge of Fig. 2(b); the facet position is not stated", no_start)
    top.dim("h", 0, s1, ybg, px=16, ext=(0, 0), row_id="m13")
    top.dim("h", s1, s1 + s2, ybg, px=16, ext=(0, 0), row_id="m14")
    top.dim("h", s1 + s2, x_lnedge, ybg, px=16, ext=(0, 0), row_id="m15")
    top.label((x_facet, ybg), "panel edge", anchor="middle", dy=-6, tip="Fig. 2(b) stops here; the chip facet is not marked and its distance from the tip is not stated")
    top.label((x_end, 0), "to modulator", anchor="end", dy=-14, tip="LN ridge continues at 0.8 um to the splitter; truncated here")
    top.note("Fig. 2(b) stretches y for legibility; here both axes are equal, so the widths need the zoom views below.")
    top.note("Fig. 1(b) SEM inset, against its 5 um bar: wide end about 5.3 um (w5 5 um) but tip to wide end only about 8.5 um against Table 1 s1 + s2 + s3 = 500 um. Its kink splits that into 7.0 : 1.6 um (ratio 4.3) against s2 / s3 = 1.5, so the SEM is not a uniformly compressed Table 1. The Table 1 values are drawn.")
    top.note("Plan widths are top widths (p.3 for the ridge; the slab layer read the same way).")

    v = c.view("tip", "detail: the 0.2 um LN slab tip inside the SiON rib (start of s1)", like="top", window=(-3.0, -6.0, 24.0, 6.0))
    v.dim("v", -w6 / 2, w6 / 2, 20.0, px=10, ext=(20.0, 20.0), row_id="m16")
    v.label((0, 0), "tip", anchor="middle", dy=-16, row_id="m12")
    v.note("The tip sits inside the rib; light reaches the bare SiON rib first. How far behind the facet is not stated.")

    v2 = c.view("ridge", "detail: ridge tip w2 inside the slab at the end of s1, width w3", like="top", window=(s1 - 6.0, -6.0, s1 + 27.0, 6.0))
    v2.dim("v", -w3 / 2, w3 / 2, s1 + 22.0, px=10, ext=(s1 + 22.0, s1 + 22.0), text="2.1 um", src=src_t1)
    v2.label((s1, 0), "ridge tip", anchor="end", dx=-4, dy=-12, row_id="m12")

    v3 = c.view("flare", "detail: end of s3, 0.8 um ridge, slab flare to w5, full LN film", like="top", window=(x_lnedge - 32.0, -6.2, x_lnedge + 22.0, 6.2))
    v3.dim("v", -w5 / 2, w5 / 2, x_lnedge, px=-10, ext=(x_lnedge, x_lnedge), text="5 um", src=src_t1)
    v3.dim("v", -w4 / 2, w4 / 2, x_lnedge - 24.0, px=10, ext=(x_lnedge - 24.0, x_lnedge - 24.0), row_id="m23")
    v3.note("Full LN film starts where the flare ends (Fig. 2(b)); Fig. 1(b) SEM shows the same vertical film edge with dark notches beside the wide end, not drawn. The SiON end past it is dashed: its length has no source.")

    def section(vid: str, title: str, x_at: float, w_slab: float, w_ridge: float, has_lnfilm: bool = False) -> None:
        xs = c.view(vid, title, "xsec")
        xw = 7.0
        y_sub = -t_box - 1.0
        xs.rect(-xw, y_sub, xw, -t_box, "si", "Si substrate (truncated)", assumed("substrate thickness not stated"), layer="substrate", alpha=0.6)
        xs.rect(-xw, -t_box, xw, 0, "sio2", "thermal SiO2 BOX", row("m24"), layer="oxide")
        sl = w_sion_slab / 2
        ws = w6 / 2
        rib = [(-sl, 0), (sl, 0), (sl, h2), (ws, h2), (ws, t_sion), (-ws, t_sion), (-ws, h2), (-sl, h2)]
        over = [(-xw, 0), (-sl, 0), (-sl, h2), (-ws, h2), (-ws, t_sion), (ws, t_sion), (ws, h2), (sl, h2), (sl, 0), (xw, 0), (xw, t_clad), (sl + t_clad, t_clad), (sl + t_clad, h2 + t_clad), (ws + t_clad, h2 + t_clad), (ws + t_clad, t_sion + t_clad), (-ws - t_clad, t_sion + t_clad), (-ws - t_clad, h2 + t_clad), (-sl - t_clad, h2 + t_clad), (-sl - t_clad, t_clad), (-xw, t_clad)]
        xs.poly(over, "sio2", "protective PECVD SiO2", row("m25") + assumed("conformal profile not stated; Methods give only the 2 um"), layer="oxide", alpha=0.45)
        xs.poly(rib, "sion", "PECVD SiON rib and slab", row("m16", "m17", "m26") + fig("Fig. 2(a) inset", "rib on a wider slab, slab width against w6", "10 %"), layer="overlay", alpha=0.75)
        if has_lnfilm:
            xs.rect(-xw, 0, xw, t_slab, "ln", "LN film, 120 nm", row("m22"), layer="slab")
        elif w_slab > 0:
            hw = w_slab / 2
            xs.poly([(-hw - inset_s, 0), (hw + inset_s, 0), (hw, t_slab), (-hw, t_slab)], "ln", "LN lower layer, 120 nm", row("m22") + src_outline + assumed("flank of the second etch taken at the 60 deg of p.2, and this width read as a top width like w4: neither is stated for this layer"), layer="slab")
        if w_ridge > 0:
            hr = w_ridge / 2
            xs.poly([(-hr - inset_r, t_slab), (hr + inset_r, t_slab), (hr, t_ln), (-hr, t_ln)], "ln", "LN ridge, upper 180 nm, 60 deg flanks", row("m21", "m22") + src_outline + stated("p.2", "60 deg sidewall") + stated("p.3", "0.8 um is a top width in the SSC region"), layer="waveguide")
        xs.dim("h", -ws, ws, t_sion, px=14, ext=(t_sion, t_sion), row_id="m16")
        xs.dim("v", h2, t_sion, -ws, px=-10, ext=(-ws, -ws), text="3.2 um", src=stated("p.4 Table 1", "h1"))
        xs.dim("v", 0, h2, sl, px=8, ext=(sl, sl), row_id="m26")
        xs.dim("v", -t_box, 0, xw, px=8, ext=(xw, xw), row_id="m24")
        xs.dim("v", t_sion, t_sion + t_clad, ws + t_clad, px=8, ext=(ws, ws), row_id="m25")
        if w_slab > 0 and not has_lnfilm:
            xs.dim("h", -w_slab / 2, w_slab / 2, 0, px=-14, ext=(0, 0), text=f"{w_slab:.2f} um", src=src_outline)
        xs.note(f"Plane at {x_at:.0f} um from the slab tip. Ridge flanks 60 deg (p.2), width at the top (p.3); the lower layer's flank is taken the same and dashed.")

    fac_r = c.view("facet", "cross-section of the bare SiON rib before the tip, UHNA4 mode at 1550 nm", "xsec")
    xw = 7.0
    sl = w_sion_slab / 2
    ws = w6 / 2
    fac_r.rect(-xw, -t_box - 1.0, xw, -t_box, "si", "Si substrate (truncated)", assumed("substrate thickness not stated"), layer="substrate", alpha=0.6)
    fac_r.rect(-xw, -t_box, xw, 0, "sio2", "thermal SiO2 BOX", row("m24"), layer="oxide")
    over = [(-xw, 0), (-sl, 0), (-sl, h2), (-ws, h2), (-ws, t_sion), (ws, t_sion), (ws, h2), (sl, h2), (sl, 0), (xw, 0), (xw, t_clad), (sl + t_clad, t_clad), (sl + t_clad, h2 + t_clad), (ws + t_clad, h2 + t_clad), (ws + t_clad, t_sion + t_clad), (-ws - t_clad, t_sion + t_clad), (-ws - t_clad, h2 + t_clad), (-sl - t_clad, h2 + t_clad), (-sl - t_clad, t_clad), (-xw, t_clad)]
    fac_r.poly(over, "sio2", "protective PECVD SiO2", row("m25") + assumed("conformal profile not stated; Methods give only the 2 um"), layer="oxide", alpha=0.45)
    fac_r.poly([(-sl, 0), (sl, 0), (sl, h2), (ws, h2), (ws, t_sion), (-ws, t_sion), (-ws, h2), (-sl, h2)], "sion", "PECVD SiON rib and slab", row("m16", "m17", "m26") + fig("Fig. 2(a) inset"), layer="overlay", alpha=0.75)
    rm = c.um("m19") / 2
    yc = t_sion / 2
    fac_r.line(circle((0, yc), rm, tol=0.03) + [(rm, yc)], "UHNA4 mode, 4.0 um MFD at 1550 nm", row("m19") + assumed("vertical alignment of the fiber is in no source: centred on the rib"))
    fac_r.dim("h", -ws, ws, t_sion, px=14, ext=(t_sion, t_sion), row_id="m16")
    fac_r.dim("v", h2, t_sion, -ws, px=-10, ext=(-ws, -ws), text="3.2 um", src=stated("p.4 Table 1", "h1"))
    fac_r.dim("v", 0, h2, sl, px=8, ext=(sl, sl), row_id="m26")
    fac_r.dim("v", -t_box, 0, xw, px=8, ext=(xw, xw), row_id="m24")
    fac_r.dim("v", t_sion, t_sion + t_clad, ws + t_clad, px=8, ext=(ws, ws), row_id="m25")
    fac_r.label((0, yc), "MFD", anchor="middle", row_id="m19")
    fac_r.note("Same outline as the Fig. 2(a) inset. The mode circle is dashed: its size is the row, its vertical alignment is in no source, centred on the rib here.")

    section("s1", "cross-section in s1, halfway: slab layer only", s1 / 2, w1 + (w3 - w1) / 2, 0.0)
    section("s2", "cross-section in s2, halfway: ridge on the slab", s1 + s2 / 2, w3, w1 + (w4 - w1) / 2)
    section("s3", "cross-section at the end of s3: wide slab, 0.8 um ridge", x_lnedge - 0.5, w5, w4)
    dtl = c.view("ln", "detail: LN in the s3 section, 180 nm ridge on 120 nm slab", "xsec", like="s3", window=(-1.2, -0.25, 1.2, 0.55))
    dtl.dim("v", 0, t_slab, 0.9, px=8, ext=(0.9, 0.9), row_id="m22")
    dtl.dim("v", 0, t_ln, 0.4, px=8, ext=(0.4, 0.4), row_id="m21")
    dtl.dim("h", -w4 / 2, w4 / 2, t_ln, px=14, ext=(t_ln, t_ln), row_id="m23")
    dtl.note("0.8 um is the ridge top width (p.3); with the 60 deg flank of p.2 the foot is 1.0 um.")

    # closure
    c.check("SiON rib + slab um: Table 1 h1 3.2 + h2 1 against the 4.2 um as grown", h1 + h2, 3.2 + 1.0, 1e-6)
    c.check("LN film um: 180 nm ridge etch + 120 nm slab", 0.18 + t_slab, t_ln, 1e-6)
    c.check("Fig. 2(b) x axis to scale: s2 / s1 from 445 / 766 px against Table 1", s2 / s1, 445.0 / 766.0, 0.05)
    c.check("Fig. 2(b) x axis to scale: s3 / s1 from 305 / 766 px against Table 1", s3 / s1, 305.0 / 766.0, 0.05)
    c.check("Fig. 2(a) inset to scale: h1 / w6 from 300 / 430 px against Table 1", h1 / w6, 300.0 / 430.0, 0.06)
    c.check("Fig. 1(b) SEM wide end against its 5 um bar um, against w5", 265.0 / 248.0 * 5.0, w5, 0.10)
    c.thumb = {"view": "ridge"}
    return c
