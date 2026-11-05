"""POPSTAR photonic interposer butt-coupled lateral Si/Ge/Si PD, 1 um x 15 um (Fig. 5, 6(a,b), 9, 10, 15, Sec. III.A-C, IV.A).

One process stage is drawn: at metal 1, where the paper characterises the device (Sec. IV.A). Sec. III.A opens the dielectric to
the doped Si before silicide, and Fig. 10 shows silicide over the doped width up to the Ge with nitride left only on undoped Si.
Sec. III.B polishes the SiO2/SiN stack away down to the W contacts before the back end, so the 60 nm SiN is not there beside M1.
Fig. 6(b), FIB, gives the Ge outline, seen before silicide. Fig. 9, FIB: three W contacts per side, landing below the Si-top line.
The FIB images are foreshortened (the 300 nm Si reads 253 nm in Fig. 6(b), 162 nm in Fig. 9), so heights are ratios to the
stated Si thickness; widths use the scale bar. No plan view of the PD is identified in the paper.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, arc, assumed, circle, fig, row, stated  # noqa: E402

ID = "cmp_ectc51909_2023_00009_ge_pd"


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 5", "Fig. 6(a)", "Fig. 6(b) FIB", "Fig. 9 FIB", "Fig. 10", "Fig. 14 (contact diameter)", "Fig. 15(a)", "Sec. III.A", "Sec. III.B", "Sec. III.C", "Sec. IV.A"],
        "At metal 1: butt-coupled Si-p / Ge / Si-n on a thin Si cavity bottom, silicide over the doped Si, nitride on undoped Si only, three W contacts per side, M1; plan not identified in the paper",
    )
    w_ge = c.um("m7")
    l_ge = c.um("m6")
    t_si = c.um("m8")
    t_box = c.um("m9")
    t_ox1 = c.um("m10")  # planarized SiO2 over the Si
    t_ox2 = 0.3  # heater encapsulation oxide, Sec. III.A
    t_sil = 0.02  # silicide, Sec. III.A
    t_m1 = 0.54  # M1 stack, Sec. III.C

    # Fig. 6(b), 5.75 nm per image pixel: the Si reads 253 nm, vertical scale 0.843; Ge 71 px high
    k6 = 253 / 300
    h_ge6 = 71 * 5.75 / k6 / 1000
    # Fig. 9, half-max on the embedded image, bar 33.7 px = 8.90 nm per pixel. Si 18.2 px (161 nm), so vertical scale 0.54
    nm9 = 300 / 33.7
    k9 = 18.2 * nm9 / 300
    h_ge9 = 29.5 * nm9 / k9 / 1000  # Ge, rows 85.5 to 115
    h_ge = (h_ge6 + h_ge9) / 2
    z_cav = 0.06  # bottom Si: 68 nm Fig. 6(b), 82 nm Fig. 9, 55 nm Fig. 6(a); blurred
    t_hm = t_si * 19 / 60  # nitride hard mask, Fig. 6(a), ratio to the Si
    # W in Fig. 9: 36.1 px wide 8 rows below the top, 26.8 px 6 rows above the bottom, 32.1 px at mid height, pitch 61.3 px
    d_top, d_bot, d_mid, p_c = 36.1 * nm9 / 1000, 26.8 * nm9 / 1000, 32.1 * nm9 / 1000, 61.3 * nm9 / 1000
    gap_c = 0.34  # Ge edge to first contact edge at the bottom: 375 nm left, 313 nm right in Fig. 9
    # W bottom at row 106, Si-top line at row 102: 4 px below the line, scaled by 0.54
    w_sink = 4 * nm9 / k9 / 1000
    z_ox = t_si + t_ox1 + t_ox2
    c.check("Ge width at the Si level, Fig. 6(b) against the 500 nm bar (176.5 px at 5.75 nm), against the row, um", 176.5 * 5.75 / 1000, w_ge, 0.05)
    c.check("W contact width at mid height, Fig. 9 against its bar, against the stated 300 nm, um", d_mid, 0.3, 0.08)
    c.check("oxide stack 600 + 300 nm, against the W from its top to the Si-top line in Fig. 9 (55 px at 8.90 nm / 0.54), um", t_ox1 + t_ox2, 55 * nm9 / k9 / 1000, 0.08)
    c.check("Ge height: Fig. 6(b) against Fig. 9, both scaled by the 300 nm Si, um", h_ge6, h_ge9, 0.10)

    rows_u = [w_ge / 2 + gap_c + d_bot / 2 + i * p_c for i in range(3)]
    e_doped = rows_u[-1] + d_bot / 2 + 0.24  # assumed: Fig. 9 has no doping contrast
    e_si = e_doped + 0.8

    src_ge = row("m7") + fig("Fig. 6(b)", "outline; width by bar, height as ratio to the 300 nm Si", "15 %") + fig("Fig. 9", "height check", "15 %")
    src_doped = row("m8") + fig("Fig. 6(a)", "Si-p and Si-n abut the Ge") + assumed("outer doping edge: Fig. 9 has no doping contrast, drawn just past the outer contact")
    src_c = fig("Fig. 9", "three contacts per side; half-max widths, pitch and landing depth against the 300 nm bar", "10 %") + stated("p.3 Sec. III.A", "W fill, oxide stack height")
    src_sil = stated("p.3 Sec. III.A", "dielectric opened to the doped Si, 20 nm TiSi2") + fig("Fig. 10", "silicide over the doped width, up to the Ge, schematic") + assumed("outer end follows the assumed doping edge")
    src_hm = fig("Fig. 6(a)", "nitride layer on the Si, ratio to the Si height", "30 %") + stated("p.3 Sec. III.A", "SiO2/Si3N4 stack is the cavity hard mask")

    x = c.view("xsec", "cross-section at mid Ge, at metal 1: Fig. 6(b), 9, 10, Sec. III.A-C", "xsec")
    u1 = e_si + 0.3
    x.rect(-u1, -t_box - 0.4, u1, -t_box, "si", "Si bulk", assumed("truncated"), alpha=0.6, layer="substrate")
    x.rect(-u1, -t_box, u1, 0, "sio2", "BOX", row("m9"), layer="oxide")
    x.rect(-u1, 0, u1, z_ox, "sio2", "SiO2 cap and interlayer, polished to the W tops", row("m10") + stated("p.3 Sec. III.A", "300 nm planarized SiO2 over the heater level") + stated("p.4 Sec. III.B", "polish stops on the W contacts, no SiN left here"), alpha=0.45, layer="oxide")
    x.rect(-u1, z_ox, u1, z_ox + t_m1, "sio2", "SiO2 interlayer around M1", stated("p.4 Sec. III.C", "PECVD SiO2 interlayer") + assumed("truncated above M1"), alpha=0.3, layer="oxide")
    for s, name, mat in ((-1, "Si-p", "doped_p"), (1, "Si-n", "doped_n")):
        x.poly([(s * w_ge * 0.445, 0.0), (s * e_doped, 0.0), (s * e_doped, t_si), (s * w_ge * 0.5, t_si), (s * w_ge * 0.445, z_cav)], mat, name, src_doped, layer="doped")
        a2, b2 = sorted((s * e_doped, s * e_si))
        x.rect(a2, 0, b2, t_si, "si", "undoped Si", row("m8") + fig("Fig. 10", "undoped Si beyond the doped region, schematic") + assumed("extent not stated"), layer="waveguide")
        x.rect(a2, t_si, b2, t_si + t_hm, "sin", "Si3N4 hard mask, on undoped Si only", src_hm + fig("Fig. 10", "nitride ends where the silicide starts") + assumed("position follows the assumed doping edge"), layer="overlay")
        a4, b4 = sorted((s * w_ge * 0.5, s * e_doped))
        x.rect(a4, t_si - t_sil, b4, t_si, "metal", "TiSi2 silicide, up to the Ge", src_sil, layer="metal")
        for u in rows_u:
            uc = s * u
            x.poly([(uc - d_bot / 2, t_si - w_sink), (uc + d_bot / 2, t_si - w_sink), (uc + d_top / 2, z_ox), (uc - d_top / 2, z_ox)], "contact", "W contact, bottom below the Si-top line", src_c, layer="via")
        a5, b5 = sorted((s * (rows_u[0] - d_top / 2 - 0.1), s * (rows_u[-1] + d_top / 2 + 0.1)))
        x.rect(a5, z_ox, b5, z_ox + t_m1, "metal", "M1, Ti-TiN / AlCu / Ti-TiN", stated("p.4 Sec. III.C", "540 nm stack") + fig("Fig. 15(a)", "M1 directly over the contact") + assumed("M1 width not stated: drawn over the contact rows"), layer="metal")
        x.label((s * (rows_u[1]), t_si * 0.42), name)
    x.rect(-w_ge * 0.445, 0, w_ge * 0.445, z_cav, "si", "bottom Si cavity", fig("Fig. 6(a)", "labelled") + fig("Fig. 6(b)", "ratio to the 300 nm Si; 55 to 82 nm across Fig. 6(a), 6(b), 9", "40 %"), layer="waveguide")

    hw0, hw1, hw2, hw3 = 0.445 * w_ge, 0.5 * w_ge, 0.525 * w_ge, 0.53 * w_ge  # Fig. 6(b): base, Si level, wing, top
    z_t = z_cav + h_ge
    corner = 0.05
    ge = arc((-hw0 + corner, z_cav + corner), corner, 180, 270, tol=0.004) + arc((hw0 - corner, z_cav + corner), corner, 270, 360, tol=0.004)
    ge += [(hw1, t_si), (hw2, t_si + 0.075), (hw3, z_t), (-hw3, z_t), (-hw2, t_si + 0.075), (-hw1, t_si)]
    x.poly(ge, "ge", "intrinsic Ge", src_ge, layer="absorber")
    x.label((0, -t_box / 2), "BOX")
    x.label((0, -t_box - 0.2), "Si bulk")
    x.label((-u1 + 0.45, z_ox - 0.3), "SiO2")
    x.label((rows_u[1], z_ox + t_m1), "M1", dy=-6)
    x.label((-rows_u[1], z_ox + t_m1), "M1", dy=-6)
    x.label((rows_u[1], t_si + 0.5), "W", anchor="middle", dx=0)
    x.label((e_si - 0.4, t_si + t_hm), "Si3N4", dy=-5)
    x.dim("h", -w_ge / 2, w_ge / 2, z_t, px=8, ext=(z_t, z_t), row_id="m7")
    x.dim("v", 0, t_si, -u1, px=-14, ext=(-e_si, -e_si), row_id="m8")
    x.dim("v", -t_box, 0, u1, px=-14, ext=(u1, u1), row_id="m9")
    x.note("Stage drawn: at metal 1 (Sec. IV.A). Fig. 6 is before silicide and shows nitride on the doped Si; Sec. III.A and Fig. 10 remove it there. Sec. III.B polishes the SiO2/SiN down to the W tops, so the 60 nm SiN is not beside M1. Dielectric above M1 truncated.")
    x.note("Fig. 9 reads a Ge width of 0.66 to 0.72 um against its bar, narrower than the 1 um row and Fig. 6(b): another width on the wafer, or a slice off centre. Fig. 10 draws one contact per side, Fig. 9 three.")
    x.note("FIB heights are scaled by the stated 300 nm Si because the views are foreshortened; film stated 310 nm, waveguide 300 nm. Fig. 9 has no doping contrast: the outer doping edge is assumed.")

    zoom = c.view("ge", "detail: Ge outline, Si cavity bottom, silicide up to the Ge", "xsec", like="xsec", window=(-1.05, -0.12, 1.05, 0.72))
    zoom.dim("h", -w_ge / 2, w_ge / 2, z_t, px=16, ext=(t_si, z_t), row_id="m7")
    zoom.dim("v", z_cav, z_t, hw3, px=14, ext=(hw3, hw3), text=f"~{h_ge:.2f} um", src=fig("Fig. 6(b)", "ratio to the 300 nm Si", "15 %") + fig("Fig. 9", "same ratio", "15 %"))
    zoom.dim("v", 0, z_cav, -hw0, px=-40, ext=(-hw0, -hw0), text=f"~{z_cav * 1000:.0f} nm", src=fig("Fig. 6(b)", "ratio to the 300 nm Si; 55 to 82 nm across Fig. 6(a), 6(b), 9", "40 %"))
    zoom.label((0, 0.28), "Ge")
    zoom.label((-0.85, 0.2), "Si-p")
    zoom.label((0.85, 0.2), "Si-n")
    zoom.label((-0.8, t_si), "TiSi2", dy=-3)

    # plan: x along the absorber; y reversed from the section so Si-p is on +y looking along +x
    top = c.view("top", "top view: section extruded over the stated intrinsic Ge length")
    src_plan = assumed("no plan view of the PD identified in the paper: Fig. 6 and Fig. 9 section extruded along the row length")
    top.rect(-1.0, -e_si, l_ge + 1.0, e_si, "si", "Si mesa", src_plan, layer="waveguide")
    for s, name, mat in ((1, "Si-p", "doped_p"), (-1, "Si-n", "doped_n")):
        a, b = sorted((s * w_ge / 2, s * e_doped))
        top.rect(0, a, l_ge, b, mat, name, src_doped + src_plan, layer="doped")
        n = int(l_ge // p_c)
        x0 = (l_ge - (n - 1) * p_c) / 2
        rings = [circle((x0 + i * p_c, s * u), d_top / 2, tol=0.015) for i in range(n) for u in rows_u]
        top.rings(rings, "contact", f"W contacts on {name}, three rows", src_c + stated("p.4 Fig. 14", "contact diameter 300 nm") + assumed("along-length pitch not stated: same as the Fig. 9 lateral pitch"), layer="via")
        a5, b5 = sorted((s * (rows_u[0] - d_top / 2 - 0.1), s * (rows_u[-1] + d_top / 2 + 0.1)))
        top.rect(0, a5, l_ge, b5, "metal", f"M1 over {name}", stated("p.4 Sec. III.C") + src_plan, layer="metal", alpha=0.3)
    wg = Route((-9.0, 0.0), 0.0, 0.4)
    wg.straight(3.0).taper(6.0, w_ge)
    top.route(wg, "si", "Si access waveguide and taper to the Ge", stated("p.3 Sec. III.A", "PD butt-coupled to the Si waveguide; 300 nm thick") + assumed("widths and taper length not stated"), layer="waveguide")
    top.rect(0, -w_ge / 2, l_ge, w_ge / 2, "ge", "intrinsic Ge", row("m6", "m7"), layer="absorber")
    top.dim("h", 0, l_ge, -e_si, px=-16, ext=(-w_ge / 2, -e_si), row_id="m6")
    top.dim("v", -w_ge / 2, w_ge / 2, l_ge, px=20, ext=(l_ge, l_ge), row_id="m7")
    top.label((l_ge / 2, 0), "Ge", dy=-4)
    top.label((l_ge / 2, e_doped), "Si-p", dy=-5)
    top.label((l_ge / 2, -e_doped), "Si-n", dy=14)
    top.label((-9.0, 0), "from drop port", anchor="start", dy=-8, tip="Fig. 7(a) labels a microring drop port as leading to the photodiode")
    top.note("Fig. 7(a) sends the ring drop port to the photodiode; the block at the waveguide end in the Fig. 14 micrograph is unlabelled and too coarse to read, so it is not used.")
    top.note("Contact rows from Fig. 9; along-length pitch, access waveguide, taper and M1 outline are assumed.")
    c.thumb = {"view": "xsec", "window": [-3.6, -0.5, 3.6, 2.38]}

    det = c.view("input", "detail: butt-coupled end and contact rows", like="top", window=(-3.0, -3.6, 5.0, 3.6))
    det.dim("v", rows_u[0], rows_u[1], 4.6, px=0, ext=(4.6, 4.6), text="~0.55 um", src=fig("Fig. 9", "pitch against the 300 nm bar", "10 %"))
    det.note("Contact diameter 300 nm (Fig. 14 caption); three rows per side as in Fig. 9.")

    ls = c.view("lsec", "section along the axis at the butt joint", "xsec")
    x0, x1 = -3.0, 3.0
    ls.rect(x0, -t_box - 0.3, x1, -t_box, "si", "Si bulk", assumed("truncated"), alpha=0.6, layer="substrate")
    ls.rect(x0, -t_box, x1, 0, "sio2", "BOX", row("m9"), layer="oxide")
    ls.rect(x0, 0, x1, z_ox, "sio2", "SiO2, polished to the W tops", row("m10") + stated("p.3 Sec. III.A") + stated("p.4 Sec. III.B"), alpha=0.45, layer="oxide")
    ls.rect(x0, 0, 0, t_si, "si", "Si waveguide", row("m8"), layer="waveguide")
    ls.rect(x0, t_si, 0, t_si + t_hm, "sin", "Si3N4 hard mask", src_hm, layer="overlay")
    ls.rect(0, 0, x1, z_cav, "si", "bottom Si cavity", fig("Fig. 6", "thin Si left under the Ge"), layer="waveguide")
    ls.rect(0, z_cav, x1, z_t, "ge", "Ge", src_ge + assumed("Ge end wall is not drawn in the paper: vertical, from the butt-coupling statement"), layer="absorber")
    ls.dim("v", 0, t_si, x0, px=-14, ext=(x0, x0), row_id="m8")
    ls.label((-1.5, t_si / 2), "Si waveguide")
    ls.label((1.5, z_cav + h_ge / 2), "Ge")
    ls.label((0, -t_box / 2), "BOX")
    ls.note("Ge continues to its stated 15 um length (truncated).")
    return c
