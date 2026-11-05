"""Liu 2026 (OFC M2B.2) lateral Ge PD, 550 nm x 30 um, 300 mm SOI (Fig. 2(a), Sec. 2, Sec. 2.2).

The paper draws one thing: the cross-section of Fig. 2(a). Reading it left to right: N++ pillar at full Si height with via
and metal, thinned N+ slab, N slab rising to a full-height N ridge, Ge with a flat base, near-vertical walls and a domed top,
N and P shoulders running under the Ge edges, a narrow column between them under the Ge, then the mirror image P, P+, P++. Fig. 2(a) is a schematic, not to scale: lateral values are
ratios to the stated Ge width, heights ratios to the stated Si and Ge thicknesses. No plan view, taper, or pads are in the
paper: the plan is that section extruded over the stated length and is dashed apart from the Ge.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, assumed, fig, row  # noqa: E402

ID = "cmp_liu2026a_ge_pd"


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 2(a) (cross-section schematic, the only device drawing)", "Sec. 2", "Sec. 2.2"],
        "Lateral P-i-N, Fig. 2(a) section: graded N/P slabs, full-height ridges and contact pillars, flat-based domed Ge on N and P shoulders; plan not in the paper",
    )
    w_ge = c.um("m5")
    l_ge = c.um("m6")
    t_ge = c.um("m7")
    t_si = c.um("m8")
    t_box = c.um("m9")

    # Fig. 2(a), lateral, pixel widths at 12x against the Ge's 179 px: all edges as ratios to the 550 nm Ge width
    w_base = 0.352 * w_ge  # column under the Ge, between the N and P shoulders (63 px)
    w_bot = 0.72 * w_ge  # flat Ge base (129 px)
    w_top = 0.86 * w_ge  # Ge width where it crosses the Si top (154 px)
    e_ridge = 0.673 * w_ge  # outer edge of the full-height N / P ridge
    e_n = 1.50 * w_ge  # N to N+ boundary
    e_np = 2.90 * w_ge  # N+ to N++ boundary
    e_npp = 4.49 * w_ge  # outer edge of N++
    v_c = 3.69 * w_ge  # via centre
    v_w = 0.70 * w_ge  # via width
    # Fig. 2(a), vertical: slab is 0.60 of the Si height; 0.40 of the Ge thickness lies below the Si top; widest at 0.62
    t_slab = 0.60 * t_si
    embed = 0.40 * t_ge
    z_bot = t_si - embed
    z_sh = z_bot + 0.62 * t_ge
    z_top = z_bot + t_ge
    via_h, m_h = 2.09 * t_ge, 0.41 * t_ge  # ratio to the Ge only: Fig. 2(a) is not to scale and these have no stated value

    src_w = fig("Fig. 2(a)", "lateral edge, ratio to the 550 nm Ge width; schematic, not to scale", "50 %")
    src_h = fig("Fig. 2(a)", "slab height, ratio to the 220 nm Si", "25 %")
    src_ge = row("m5", "m7") + fig("Fig. 2(a)", "flat base, near-vertical walls, dome; ratio to stated width and thickness", "25 %")
    src_plan = assumed("no plan view in the paper: Fig. 2(a) section extruded along the stated Ge length")

    c.check("Fig. 2(a) symmetry: P++ outer edge against N++ outer edge from the Ge centre, px", 805, 803, 0.03)

    x = c.view("xsec", "cross-section at mid Ge, Fig. 2(a)", "xsec")
    u0, u1 = -e_npp - 0.35, e_npp + 0.35
    x.rect(u0, -t_box - 0.5, u1, -t_box, "si", "substrate Si", assumed("substrate thickness not relevant: truncated"), alpha=0.6, layer="substrate")
    x.rect(u0, -t_box, u1, 0, "sio2", "SiO2 BOX", row("m9"), layer="oxide")
    z_clad = t_si + via_h
    x.rect(u0, 0, u1, z_clad, "sio2", "SiO2 cladding", assumed("Fig. 2(a) leaves the region above Si blank; a cladding is assumed around the via"), alpha=0.35, layer="oxide")
    x.rect(-w_base / 2, 0, w_base / 2, z_bot, "unknown", "column under the Ge: oxide or undoped Si, not resolved", fig("Fig. 2(a)", "position and width; fill identical to the SiO2 band, not to the substrate Si", "50 %") + assumed("material: the text has the Ge on recessed Si, the figure colour says SiO2"), layer="waveguide")

    def grades(sign: int) -> None:
        name = "N" if sign < 0 else "P"
        mat = "doped_n" if sign < 0 else "doped_p"
        s = sign
        ridge = [(s * w_base / 2, 0.0), (s * e_n, 0.0), (s * e_n, t_slab), (s * e_ridge, t_slab), (s * e_ridge, t_si), (s * w_top / 2, t_si), (s * w_bot / 2, z_bot), (s * w_base / 2, z_bot)]
        x.poly(ridge, mat, f"{name} Si: slab, full-height ridge and shoulder under the Ge edge", src_w + src_h + row("m8"), layer="doped", alpha=0.45)
        x.rect(min(s * e_n, s * e_np), 0, max(s * e_n, s * e_np), t_slab, mat, f"{name}+ Si slab", src_w + src_h, layer="doped", alpha=0.72)
        x.rect(min(s * e_np, s * e_npp), 0, max(s * e_np, s * e_npp), t_si, mat, f"{name}++ Si contact pillar, full Si height", src_w + row("m8"), layer="doped")
        vc = s * v_c
        x.rect(vc - v_w / 2, t_si, vc + v_w / 2, t_si + via_h, "contact", f"via on {name}++", src_w + assumed("via height not stated"), layer="via")
        x.rect(min(s * e_np, s * e_npp), t_si + via_h, max(s * e_np, s * e_npp), t_si + via_h + m_h, "metal", f"metal over {name}++", src_w + assumed("metal thickness not stated"), layer="metal")
        x.label((s * (e_n + e_ridge) / 2 + (0.05 * s), t_slab / 2), name)
        x.label((s * (e_n + e_np) / 2, t_slab / 2), name + "+")
        x.label((s * (e_np + e_npp) / 2, t_si / 2), name + "++")
        x.label((vc, t_si + via_h / 2), "via", anchor="start", dx=10)
        x.label((s * (e_np + e_npp) / 2, t_si + via_h + m_h), "metal", dy=-6)

    grades(-1)
    grades(1)

    ge = [(-w_bot / 2, z_bot), (w_bot / 2, z_bot), (w_top / 2, t_si), (w_ge / 2, z_sh)]
    n = 24
    for i in range(1, n):
        a = math.pi * i / n
        ge.append((w_ge / 2 * math.cos(a), z_sh + (z_top - z_sh) * math.sin(a)))
    ge += [(-w_ge / 2, z_sh), (-w_top / 2, t_si)]
    x.poly(ge, "ge", "Ge, base below the Si top, on the N and P shoulders", src_ge, layer="absorber")
    x.label((0, z_top), "Ge", dy=-6)
    x.label((0, -t_box / 2), "SiO2 BOX")
    x.label((0, -t_box - 0.25), "substrate Si")
    x.dim("h", -w_ge / 2, w_ge / 2, z_top, px=22, ext=(z_top, z_top), row_id="m5")
    x.dim("v", 0, t_si, -e_npp, px=-16, ext=(-e_npp, -e_npp), row_id="m8")
    x.dim("v", -t_box, 0, u1, px=-16, ext=(u1, u1), row_id="m9")
    x.note("Fig. 2(a) is a schematic: lateral extents come from ratios to the 550 nm Ge width, so doping widths are good to about 50 %.")
    x.note("Column under the Ge, dashed: its fill in Fig. 2(a) is identical to the SiO2 band, not the substrate Si, while the text has the Ge on recessed Si. Oxide or undoped Si, not resolved.")
    x.note("Recess depth is not stated (row m7 note); it is the 0.40 embedded fraction read from Fig. 2(a).")

    zoom = c.view("ge", "detail: Ge base on the N and P shoulders, column between them", "xsec", like="xsec", window=(-0.62, -0.1, 0.62, 0.6))
    zoom.dim("v", z_bot, z_top, w_ge / 2, px=44, ext=(w_ge / 2, w_ge / 2), row_id="m7")
    zoom.dim("h", -w_ge / 2, w_ge / 2, z_top, px=20, ext=(z_top, z_top), row_id="m5")
    zoom.label((-0.3, t_slab / 2), "N")
    zoom.label((0.3, t_slab / 2), "P")
    zoom.label((0, z_bot / 2), "Si or SiO2?")
    zoom.label((0, z_top), "Ge", dy=-6)

    # plan: x along the absorber, y = section coordinate reversed so that N is on +y when looking along +x
    top = c.view("top", "top view: Fig. 2(a) section extruded over the Ge length")
    l_stub, l_tp, w_wg = 3.0, 4.0, 0.4
    top.rect(0, -e_ridge, l_ge, e_ridge, "si", "ridge region around the Ge", src_plan, layer="waveguide")
    for sign, name, mat in ((1, "N", "doped_n"), (-1, "P", "doped_p")):
        for a, b, label, al in ((w_base / 2, e_n, name, 0.45), (e_n, e_np, name + "+", 0.72), (e_np, e_npp, name + "++", None)):
            y0, y1 = sorted((sign * a, sign * b))
            top.rect(0, y0, l_ge, y1, mat, f"{label} Si", src_w + src_plan, layer="doped", alpha=al)
        y0, y1 = sorted((sign * e_np, sign * e_npp))
        top.rect(0, sign * v_c - v_w / 2, l_ge, sign * v_c + v_w / 2, "contact", f"via line on {name}++ (bar or array not known)", src_w + src_plan, layer="via")
        top.rect(0, y0, l_ge, y1, "metal", f"metal over {name}++", src_w + src_plan, layer="metal", alpha=0.45)
    wg = Route((-l_stub - l_tp, 0.0), 0.0, w_wg)
    wg.straight(l_stub).taper(l_tp, 2 * e_ridge)
    top.route(wg, "si", "access Si waveguide and taper", assumed("taper and waveguide width not in this paper; the two are on separate chips fiber-connected, grating or edge coupler not stated"), layer="waveguide")
    top.rect(0, -w_ge / 2, l_ge, w_ge / 2, "ge", "Ge absorber, widest extent", row("m5", "m6"), layer="absorber")
    top.dim("h", 0, l_ge, -e_npp, px=-16, ext=(-w_ge / 2, -e_npp), row_id="m6")
    top.label((l_ge / 2, 0), "Ge", dy=-5)
    top.label((-l_tp - l_stub, 0), "Si waveguide", anchor="end", dx=-4)
    top.note("Plan not in the paper: only the Ge width and length are stated. Doping, via and metal lines are Fig. 2(a) extruded; pads are not in the source and are not drawn.")
    c.thumb = {"view": "xsec", "window": [-2.9, -0.5, 2.9, 1.82]}

    tip = c.view("input", "detail: input end of the Ge", like="top", window=(-8.0, -3.0, 6.0, 3.0))
    tip.dim("v", -w_ge / 2, w_ge / 2, 0, px=-18, ext=(0, 0), row_id="m5")
    for sign, name in ((1, "N"), (-1, "P")):
        for a, b, label in ((w_base / 2, e_n, name), (e_n, e_np, name + "+"), (e_np, e_npp, name + "++")):
            tip.label((3.5, sign * (a + b) / 2 + (sign * 0.12 if label == name else 0)), label)
    tip.note("Access waveguide, taper and the step from it to the Ge are assumed.")

    ls = c.view("lsec", "section along the axis: Si waveguide into the recessed Ge", "xsec")
    x0, x1 = -2.5, 3.5
    ls.rect(x0, -t_box - 0.3, x1, -t_box, "si", "substrate Si", assumed("truncated"), alpha=0.6, layer="substrate")
    ls.rect(x0, -t_box, x1, 0, "sio2", "SiO2 BOX", row("m9"), layer="oxide")
    ls.rect(x0, 0, x1, z_clad, "sio2", "SiO2 cladding", assumed("Fig. 2(a) leaves it blank"), alpha=0.35, layer="oxide")
    ls.rect(x0, 0, 0, t_si, "si", "Si waveguide", row("m8"), layer="waveguide")
    ls.rect(0, 0, x1, z_bot, "si", "Si under the recess", row("m8", "m7") + fig("Fig. 2(a)", "embedded fraction", "25 %"), layer="waveguide")
    ls.rect(0, z_bot, x1, z_top, "ge", "Ge on the centre line", row("m7") + assumed("the Ge start is not drawn in the paper: a vertical wall is assumed"), layer="absorber")
    ls.dim("v", z_bot, z_top, x1, px=-16, ext=(x1, x1), row_id="m7")
    ls.dim("v", 0, t_si, x0, px=-16, ext=(x0, x0), row_id="m8")
    ls.label((1.75, (z_bot + z_top) / 2), "Ge")
    ls.label((-1.25, t_si / 2), "Si waveguide")
    ls.label((0.5, -t_box / 2), "SiO2 BOX")
    ls.note("Ge continues to its stated 30 um length (truncated). The Si waveguide and Ge bottom follow the stated recess; the end wall shape is assumed.")
    return c
