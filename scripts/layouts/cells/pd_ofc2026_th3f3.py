"""OFC 2026 Th3F.3 deep-recessed Ge/Si PD, w 300 nm, L 10 um, imec 300 mm. Text and captions only: Fig. 1(a), (b) not available.

What the text fixes: Ge epitaxy in a deep Si recess with heavily doped walls, its top level with the Si surface; the
surrounding Si was implanted n and p and annealed before Ge growth, so the doped Si meets the Ge; 220 nm SOI, 2 um BOX; light
from a Si waveguide. The TEM height is given for a sibling device 200 nm wide; this device has none, so the drawn height is assumed
and carries no label. Contacts, metal, doping extents and waveguide are assumed, dashed, with no dimension.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, assumed, row, stated  # noqa: E402

ID = "cmp_ofc2026_th3f3_ge_pd_w300_l10"


def build() -> Cell:
    c = Cell(
        ID,
        ["Text and captions only: Fig. 1(a) schematic, 1(b) TEM not available", "Sec. 2", "Sec. 3"],
        "Ge flush with the top Si in a deep recess between heavily doped n-type and p-type Si; Ge width, Si, BOX stated; Ge height and the rest assumed",
    )
    w_ge = c.um("m5")
    l_ge = c.um("m6")
    t_si = c.um("m7")
    t_box = c.um("m8")
    h_ge = 0.193  # p.1 Sec. 2: TEM of the 200 nm wide sibling
    z_bot = t_si - h_ge  # flush with the top Si
    why = "Fig. 1 not available and the text gives no value"
    e_d = 1.2  # outer edge of the doped Si
    v_u, v_w = 0.85, 0.3
    h1, t1 = 0.8, 0.4
    z_v1 = t_si + h1
    z_m1 = z_v1 + t1

    src_h = assumed("the Ge height of this 300 nm wide device is not stated: drawn at the TEM height of the 200 nm wide sibling, p.1 Sec. 2")

    x = c.view("xsec", "cross-section at mid Ge (text only)", "xsec")
    u1 = e_d + 0.4
    x.rect(-u1, -t_box - 0.4, u1, -t_box, "si", "Si substrate", assumed("truncated"), alpha=0.6, layer="substrate")
    x.rect(-u1, -t_box, u1, 0, "sio2", "BOX", row("m8"), layer="oxide")
    x.rect(-u1, 0, u1, z_m1 + 0.25, "sio2", "SiO2 cladding", assumed(f"not stated: {why}"), alpha=0.4, layer="oxide")
    x.rect(-w_ge / 2, 0, w_ge / 2, z_bot, "si", "Si below the deep recess", row("m7") + src_h, layer="waveguide")
    for s, name, mat in ((-1, "n", "doped_n"), (1, "p", "doped_p")):
        a, b = sorted((s * w_ge / 2, s * e_d))
        x.rect(a, 0, b, t_si, mat, f"highly doped {name} Si, meets the Ge", row("m7") + stated("p.1 Sec. 2", "both polarities implanted and annealed before Ge growth") + assumed(f"lateral extent and side: {why}"), layer="doped")
        vc = s * v_u
        x.rect(vc - v_w / 2, t_si, vc + v_w / 2, z_v1, "contact", f"contact on {name}", assumed(f"not stated: {why}"), layer="via")
        a2, b2 = sorted((s * (v_u - v_w), s * (e_d)))
        x.rect(a2, z_v1, b2, z_m1, "metal", f"metal on {name}", assumed(f"not stated: {why}"), layer="metal")
        x.label((s * (w_ge / 2 + 0.17), t_si / 2), name, tip="Highly doped; level not stated")
    x.rect(-w_ge / 2, z_bot, w_ge / 2, t_si, "ge", "Ge in the deep recess, flush with the top Si", row("m5") + src_h + stated("p.1 Sec. 2", "Ge top level with the Si surface"), layer="absorber")
    x.label((0, t_si), "Ge", dy=-5)
    x.label((0, -t_box / 2), "BOX")
    x.dim("h", -w_ge / 2, w_ge / 2, t_si, px=26, ext=(t_si, t_si), row_id="m5")
    x.dim("v", 0, t_si, -e_d, px=-14, ext=(-e_d, -e_d), row_id="m7")
    x.dim("v", -t_box, 0, u1, px=-14, ext=(u1, u1), row_id="m8")
    x.note("Text and captions only (Fig. 1 not available). Which side is n is arbitrary.")
    x.note("The text gives a Ge height only for the TEM of a sibling 200 nm in width. This device has none: the height and the Si left under the Ge are assumed and have no label.")

    d = c.view("ge", "detail: deep recess, Ge flush with the Si", "xsec", like="xsec", window=(-0.7, -0.08, 0.7, 0.42))
    d.dim("h", -w_ge / 2, w_ge / 2, t_si, px=20, ext=(t_si, t_si), row_id="m5")
    d.dim("v", 0, t_si, -w_ge / 2 - 0.3, px=-10, ext=(-w_ge / 2 - 0.3, -w_ge / 2 - 0.3), row_id="m7")
    d.label((0, (z_bot + t_si) / 2), "Ge")
    d.label((-0.28, t_si / 2), "n", tip="Highly doped; level not stated")
    d.label((0.45, t_si / 2), "p", tip="Highly doped; level not stated")

    top = c.view("top", "top view (text only): diode along the stated length")
    src_plan = assumed("Fig. 1 not available: plan of the doped regions, contacts and metal not stated")
    for s, name, mat in ((1, "n", "doped_n"), (-1, "p", "doped_p")):
        a, b = sorted((s * w_ge / 2, s * e_d))
        top.rect(0, a, l_ge, b, mat, f"highly doped {name} Si", src_plan, layer="doped")
        top.rect(0, s * v_u - v_w / 2, l_ge, s * v_u + v_w / 2, "contact", f"contact line on {name}", src_plan, layer="via")
        a2, b2 = sorted((s * (v_u - v_w), s * e_d))
        top.rect(0, a2, l_ge, b2, "metal", f"metal over {name}", src_plan, layer="metal", alpha=0.4)
    wg = Route((-5.0, 0.0), 0.0, 0.4)
    wg.straight(1.5).taper(3.5, w_ge)
    top.route(wg, "si", "Si waveguide from the grating coupler", stated("p.1 Sec. 3", "grating-coupled Si waveguide feeds the PD") + assumed(f"width and taper: {why}"), layer="waveguide")
    top.rect(0, -w_ge / 2, l_ge, w_ge / 2, "ge", "Ge", row("m5", "m6"), layer="absorber")
    top.dim("h", 0, l_ge, -e_d, px=-16, ext=(-w_ge / 2, -e_d), row_id="m6")
    top.dim("v", -w_ge / 2, w_ge / 2, l_ge, px=18, ext=(l_ge, l_ge), row_id="m5")
    top.label((l_ge / 2, 0), "Ge", dy=-3)
    top.note("Pads and metal routing not stated, not drawn. S-parameter measured to 110 GHz, so RF pads exist but their layout is not in the text.")
    c.thumb = {"view": "xsec"}

    t2_ = c.view("input", "detail: input end (text only)", like="top", window=(-5.5, -1.8, 3.0, 1.8))
    t2_.label((1.5, 0.45), "n")
    t2_.label((1.5, -0.45), "p")
    t2_.dim("v", -w_ge / 2, w_ge / 2, 2.6, px=0, ext=(2.6, 2.6), row_id="m5")

    ls = c.view("lsec", "section along the axis (text only)", "xsec")
    x0, x1 = -1.5, 2.0
    ls.rect(x0, -t_box - 0.2, x1, -t_box, "si", "Si substrate", assumed("truncated"), alpha=0.6, layer="substrate")
    ls.rect(x0, -t_box, x1, 0, "sio2", "BOX", row("m8"), layer="oxide")
    ls.rect(x0, 0, x1, 0.6, "sio2", "SiO2 cladding", assumed(f"not stated: {why}"), alpha=0.4, layer="oxide")
    ls.rect(x0, 0, 0, t_si, "si", "Si waveguide", row("m7"), layer="waveguide")
    ls.rect(0, 0, x1, z_bot, "si", "Si below the deep recess", row("m7") + src_h, layer="waveguide")
    ls.rect(0, z_bot, x1, t_si, "ge", "Ge, flush with the top Si", src_h + stated("p.1 Sec. 2", "Ge top level with the Si surface"), layer="absorber")
    ls.dim("v", 0, t_si, x0, px=-14, ext=(x0, x0), row_id="m7")
    ls.label((-0.75, t_si / 2), "Si")
    ls.label((1.0, (z_bot + t_si) / 2), "Ge")
    ls.note("Ge continues to its stated 10 um length (truncated). The end wall is assumed vertical.")
    return c
