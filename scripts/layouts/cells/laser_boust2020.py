"""Boust 2020 InGaAsP/InP DFB, 1.75 mm, HR back / AR output, shallow ridge between two channels, butt-coupled pump (Fig. 1(a,b), Fig. 2, Sec. II).

Plan from the photograph of Fig. 1(b) against its 250 um bar: long bar chip, output facet at the right facing the Si3N4 chip,
top metal an elongated hexagon with its points on the ridge axis, ridge seen as a thin line along the axis, four and three wire
bond balls below and above the ridge, a dark patterned block in the metal near the output end, too blurred to resolve inside.
The paper gives no ridge width, stack or grating period (it defers to its reference [16]): the sections stay unpublished.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, assumed, circle, fig, rect, row, stated  # noqa: E402

ID = "cmp_lit_boust2020_dfb_laser"


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 1(a)", "Fig. 1(b) photograph, 250 um bar", "Fig. 2(a,b)", "Sec. II", "Sec. IV-A"],
        "DFB bar from the Fig. 1(b) photograph: hexagonal top metal, ridge axis, wire bonds, patterned block, HR back and AR output facets; stack and grating are in a reference not read",
    )
    length = c.um("m11")
    lam = c.num("m12") * 1e-3  # um
    fsr_nm = c.um("m13") * 1e3  # m13 is in nm; um() gives um, nm here
    fsr_ghz = c.num("m6")

    # Fig. 1(b), native image pixels: 76 px bar = 250 um. Chip 532 px along, 104 px across; the metal 92 px across
    um_px = 250 / 76
    c.check("chip length in Fig. 1(b) (532 px at the 250 um bar) against the row, um", 532 * um_px, length, 0.05)
    w_chip = 104 * um_px
    hw_pad = 92 / 2 * um_px
    tip0, sh0 = 26.0, 125.0  # back end of the metal: point, shoulder
    sh1 = 1671.0  # output end: shoulder; the point reaches the facet
    src_photo = fig("Fig. 1(b)", "photograph against the 250 um bar", "10 %")

    # closure: spectrum and cavity
    c.check("FSR: 0.203 nm at the lasing wavelength against the 24.6 GHz row, GHz", 299792.458 * (fsr_nm * 1e-3) / lam**2, fsr_ghz, 0.01)
    n_eff = 3.2  # not stated: drafting value for the unpublished longitudinal section
    period = lam / (2 * n_eff)

    w_r, w_ch = 4.0, 12.0  # ridge, channel: values in the reference, not in this paper
    t_act, t_dil, t_p_stop, t_ridge, t_diel, t_met = 0.2, 1.5, 0.2, 1.8, 0.2, 0.5
    src_ridge = stated("p.2 Sec. II", "shallow ridge with a channel on each side") + fig("Fig. 1(b)", "thin line along the chip axis") + assumed("ridge width and channel width are in the cited reference, not in this paper")

    top = c.view("top", "top view, Fig. 1(b): whole chip")
    top.rect(0, -w_chip / 2, length, w_chip / 2, "inp", "InGaAsP/InP chip", row("m11") + src_photo + stated("p.2 Sec. II", "InGaAsP/InP"), layer="waveguide")
    top.rect(0, w_r / 2, length, w_r / 2 + w_ch, "air", "channel", src_ridge, layer="trench", alpha=0.8)
    top.rect(0, -w_r / 2 - w_ch, length, -w_r / 2, "air", "channel", src_ridge, layer="trench", alpha=0.8)
    pad = [(tip0, 0.0), (sh0, -hw_pad), (sh1, -hw_pad), (length, 0.0), (sh1, hw_pad), (sh0, hw_pad)]
    top.poly(pad, "metal", "top metal, elongated hexagon with its points on the ridge", src_photo, layer="metal", alpha=0.55)
    top.rect(0, -w_r / 2, length, w_r / 2, "inp", "ridge, under the metal", row("m11") + src_ridge, layer="waveguide")
    # dark block near the output end, upper part of the metal
    bx0, bx1, by0, by1 = 1276.0, 1671.0, 0.55 * hw_pad, hw_pad
    top.rect(bx0, by0, bx1, by1, "other", "dark patterned block in the metal, purpose not stated", src_photo + assumed("too blurred in the photograph to resolve its pattern: outline only"), layer="metal", alpha=0.75)
    balls = [(375.0, 110.0), (776.0, 124.0), (1105.0, 105.0), (368.0, -67.0), (743.0, -82.0), (1000.0, -75.0), (1520.0, -83.0)]
    src_b = fig("Fig. 1(b)", "bond positions against the bar; the photograph is oblique, so the two rows are not symmetric", "15 %")
    for bx, by in balls:
        s = 1 if by > 0 else -1
        top.rect(bx - 8, by, bx + 8, s * (w_chip / 2 + 70), "metal", "bond wire, truncated", src_b, layer="metal")
    top.rings([circle(b, 30, tol=1.0) for b in balls], "metal", "wire bond balls", src_b, layer="metal")
    top.line([(0, -w_chip / 2 - 15), (0, w_chip / 2 + 15)], "back facet, high-reflection coating", stated("p.2 Sec. II", "back facet HR, output facet AR") + fig("Fig. 1(b)", "output faces the Si3N4 chip"))
    top.line([(length, -w_chip / 2 - 15), (length, w_chip / 2 + 15)], "output facet, anti-reflection coating", stated("p.2 Sec. II") + fig("Fig. 1(b)", "output faces the Si3N4 chip"))
    top.dim("h", 0, length, -w_chip / 2, px=-34, ext=(-w_chip / 2, -w_chip / 2), row_id="m11")
    top.dim("v", -w_chip / 2, w_chip / 2, 0, px=-36, ext=(0, 0), text="~340 um", src=src_photo)
    top.label((0, w_chip / 2 + 15), "HR", dy=-6)
    top.label((length, w_chip / 2 + 15), "AR", dy=-6)
    top.label((length, 20), "to Si3N4 chip", anchor="end", dx=-6, tip="Air gap to the Si3N4 chip set with translation stages (Sec. IV-A); output collected by butt coupling")
    top.label((850, 0), "ridge", dy=-6)
    top.note("The grating is buried and is not drawn: its period and stack are in a reference not read. Submount, wire far ends and the Si3N4 chip of Fig. 1(b) are not drawn.")
    top.note("Chip size, metal outline and bond positions read from the Fig. 1(b) photograph; ridge line is seen in the same photograph, width not stated.")
    c.thumb = {"view": "top"}

    tip = c.view("output", "detail: output end, ridge and channels between the metal point", like="top", window=(length - 110, -55, length + 40, 55))
    tip.label((length - 60, w_r / 2 + w_ch / 2), "channel", dy=-3)
    tip.label((length - 60, -w_r / 2 - w_ch / 2), "channel", dy=3)
    tip.label((length - 60, 0), "ridge", dy=4)
    tip.note("Channel and ridge widths assumed (two channels stated, values not).")

    # transverse section: dual-channel shallow ridge. z = 0 at the substrate top
    z_d = t_dil
    z_a = z_d + t_act
    z_e = z_a + t_p_stop  # the etch stops here: shallow, above the active layer
    z_r = z_e + t_ridge
    u1 = w_r / 2 + w_ch + 4.0
    x = c.view("xsec", "cross-section: shallow ridge between two channels", "xsec")
    x.rect(-u1, -3.0, u1, 0, "inp", "n-InP substrate", stated("p.2 Sec. II", "InP") + assumed("truncated"), alpha=0.7, layer="substrate")
    x.rect(-u1, 0, u1, z_d, "inp", "dilute waveguide below the active layer", stated("reference [16] title", "dilute mode DFB") + assumed("thickness and composition in the reference, not in this paper"), alpha=0.5, layer="slab")
    x.rect(-u1, z_d, u1, z_a, "active", "InGaAsP active layer", stated("p.2 Sec. II", "InGaAsP/InP") + assumed("thickness and QW count not stated"), layer="absorber")
    x.rect(-u1, z_a, u1, z_e, "inp", "p-InP left under the channels", assumed("shallow ridge: etch stops above the active layer; thickness not stated"), layer="slab")
    x.rect(-w_r / 2, z_e, w_r / 2, z_r, "inp", "ridge", src_ridge + assumed("height not stated"), layer="waveguide")
    for s in (-1, 1):
        a, b = sorted((s * (w_r / 2 + w_ch), s * u1))
        x.rect(a, z_e, b, z_r, "inp", "outer field beyond the channel", src_ridge + assumed("height not stated"), layer="waveguide")
        a2, b2 = sorted((s * w_r / 2, s * (w_r / 2 + w_ch)))
        x.rect(a2, z_e, b2, z_e + t_diel, "sin", "dielectric in the channel", assumed("not stated"), layer="overlay")
        x.rect(a, z_r, b, z_r + t_diel, "sin", "dielectric on the field", assumed("not stated"), layer="overlay")
        x.rect(a2, z_e + t_diel, b2, z_e + t_diel + t_met, "metal", "top metal in the channel", fig("Fig. 1(b)", "metal covers ridge and channels") + assumed("thickness not stated"), layer="metal", alpha=0.7)
    x.rect(-u1, z_r + t_diel, u1, z_r + t_diel + t_met, "metal", "top metal", fig("Fig. 1(b)", "continuous over the ridge and well beyond") + assumed("thickness not stated"), layer="metal", alpha=0.85)
    x.label((0, z_e + 0.8), "ridge")
    x.label((-w_r / 2 - w_ch / 2, z_e), "channel", dy=-4)
    x.label((w_r / 2 + w_ch / 2, z_e), "channel", dy=-4)
    x.label((-u1 + 2, z_d + t_act / 2), "active", anchor="start", dy=4)
    x.label((u1 - 2, z_d / 2), "dilute waveguide", anchor="end", dy=4)
    x.label((0, -1.5), "n-InP substrate")
    x.note("Only the materials, the two channels and the shallow ridge are from this paper; ridge width, channel width and stack thicknesses are in reference [16], which is not read here.")

    rd = c.view("ridge", "detail: ridge", "xsec", like="xsec", window=(-7.0, -1.2, 7.0, z_r + 1.4))
    rd.label((0, z_e + 1.0), "ridge")
    rd.label((4.5, z_e + 0.1), "channel", dy=-6)
    rd.label((6.8, z_a), "active", anchor="end", dy=-2)

    # longitudinal section: grating on the stripe, HR facet, first-order period from an assumed n_eff
    ls = c.view("lsec", "section along the ridge at the output end: grating, AR facet", "xsec")
    x0 = length - 8.0
    ls.rect(x0, -1.0, length, 0, "inp", "n-InP substrate", stated("p.2 Sec. II", "InP") + assumed("truncated"), alpha=0.7, layer="substrate")
    ls.rect(x0, 0, length, z_d, "inp", "dilute waveguide", assumed("in the reference"), alpha=0.5, layer="slab")
    ls.rect(x0, z_d, length, z_a, "active", "InGaAsP active layer", assumed("thickness not stated"), layer="absorber")
    ls.rect(x0, z_a, length, z_r, "inp", "p-InP in the ridge", assumed("height not stated"), layer="waveguide")
    t_gr, z_g = 0.06, z_a + 0.08
    ls.rect(x0, z_g, length, z_g + t_gr, "inp", "grating layer, unresolved", stated("p.2 Sec. II", "DFB") + assumed("position, depth not stated; uniform assumed"), alpha=0.5, layer="slab")
    n_t = int((length - x0) / period)
    ls.rings([rect(length - (i + 0.75) * period, z_g, length - (i + 0.25) * period, z_g + t_gr) for i in range(n_t)], "active", "grating teeth: first-order period from an assumed n_eff", assumed("period and depth not stated; first-order against the row wavelength with n_eff 3.2"), layer="absorber", lod=period / 2)
    ls.rect(x0, z_r, length, z_r + t_met, "metal", "top metal", fig("Fig. 1(b)") + assumed("thickness not stated"), layer="metal", alpha=0.85)
    ls.line([(length, -1.0), (length, z_r + t_met)], "output facet, AR", stated("p.2 Sec. II"))
    ls.label((length - 4, z_d + t_act / 2), "active", dy=4)
    ls.label((length - 4, z_d / 2), "dilute waveguide")
    ls.label((length - 4, z_r / 2 + z_a / 2 + 0.2), "p-InP ridge")
    ls.label((length, z_d), "AR", anchor="start", dx=6)
    ls.note("The paper gives neither period nor order; period here comes from an assumed n_eff.")
    c.view("grating", "detail: teeth above the active layer at the AR facet", "xsec", like="lsec", window=(length - 1.6, z_d - 0.15, length + 0.1, z_g + 0.55))
    return c
