"""Orange/red design of a 2026 visible TFLN MZM: thermo-optic bias section, 0.75 mm gold wire heater (Fig. 1(b), 1(c), 1(d), Fig. 3(a) inset, Methods).

Fig. 1(b) gives the wire topology: four passes, out along the far side from one pad and back to the other, on the outer side
of one arm; unconnected dummy bars on the outer side of the other arm. Micrograph Fig. 1(c) (device No. 2, this design) gives the
pads, the lead strip beside the lower pad, and the band widths: gold FWHM 13.4 and 13.7 um for the heater, 7.5 and 7.7 um for the
dummy (red minus blue, averaged along the section; two embedded images at 2.055 um/px). Three dark slots resolve in the heater band,
so four wires. Fig. 3(a) inset is the simulated section of the 488 nm design: wire 1.22 um, centre pitch 3.31 um mean, band 11.2 um,
2.2 um to the waveguide. Its band misses device No. 1's own 12.7 um FWHM and this device's 13.5 um, so the inset is not the layout.
With a pitch of 3.31 um a 13.5 um band needs 3.5 um wires, about 23 ohm in bulk gold against 80 ohm measured: rejected. So the wire
width is transferred from the inset and the pitch follows from the band of this device. The heater sits in a shallow trench of the
1.6 um cladding, recessed below the surface.
"""

from __future__ import annotations

import math
import sys
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, assumed, fig, row, stated  # noqa: E402

ID = "cmp_liu2026d_tops_or"

INSET = 54.5  # Fig. 3(a) inset: px/um, 109 px for the 2 um bar at 800 dpi
WIRE = 66.5 / INSET  # Fig. 3(a) inset, 488 nm design: 1.22 um, transferred
UM_PX = 300.0 / 146.0  # embedded micrograph at 543 ppi: the 300 um bar spans 146 px
BAND = 13.5  # Fig. 1(c), device No. 2: heater band gold FWHM, 6.50 and 6.68 px
BAND_D = 7.6  # Fig. 1(c), device No. 2: dummy band gold FWHM, 3.65 and 3.76 px
N_DUMMY = 3  # Fig. 1(c): two dark slots at this resolution; Fig. 1(b) schematic draws four
PITCH = (BAND - WIRE) / 3
PITCH_D = (BAND_D - WIRE) / (N_DUMMY - 1)
ARM = 11.5  # half arm separation: 11.2 px between the waveguide clearings in Fig. 1(c), 23 um
EDGE = (20.3 * UM_PX - 2 * ARM - (BAND + BAND_D) / 2) / 2  # heater to dummy band centres 20.3 px, less the arms and half bands


def honeycomb(a: float, x0: float, x1: float, y0: float, y1: float, keep: Callable[[float, float], bool]) -> list[list[tuple[float, float]]]:
    """Edges of a flat-top honeycomb of side a in a window; keep(x, y) filters on both end points."""
    h = math.sqrt(3) * a
    out: list[list[tuple[float, float]]] = []
    i = 0
    x = x0
    while x < x1 + 3 * a:
        y = y0 + (h / 2 if i % 2 else 0.0)
        while y < y1 + h:
            v = [(x + a * math.cos(math.radians(60 * k)), y + a * math.sin(math.radians(60 * k))) for k in range(6)]
            for p, q in ((v[0], v[1]), (v[1], v[2]), (v[2], v[3])):
                if keep(*p) and keep(*q):
                    out.append([p, q])
            y += h
        x += 1.5 * a
        i += 1
    return out


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 1(b)", "Fig. 1(c) micrograph, device No. 2", "Fig. 1(d)", "Fig. 3(a) inset", "Methods p.3-4", "Results p.6"],
        "Four-pass gold wire meander beside one arm with two pads, narrower dummy band at the other arm, MMI end of the MZM; section with wires in cladding trenches",
    )
    L = c.um("m3")
    w_wg = c.um("m4")
    t_ln = c.um("m6")
    t_box = c.um("m7")
    t_clad = c.um("m8")
    t_au = c.um("m9")
    h_gap = c.um("m10")

    y_d = ARM + EDGE + WIRE / 2
    ys = [y_d + i * PITCH for i in range(4)]  # D, C, B, A: nearest the waveguide first
    yD, yC, yB, yA = ys
    hw = WIRE / 2
    x1 = L - 17.0  # Fig. 1(c): inner U ends 8 px before the band end; Fig. 1(b) same order

    src_wire = fig("Fig. 3(a) inset, 488 nm design", "wire width transferred to this design", "10 %") + fig("Fig. 1(c), device No. 2", "band gold FWHM sets the pitch; three dark slots", "1 um") + fig("Fig. 1(b)", "four-pass path, one pad at each outer pass") + row("m3", "m9")
    src_tag = fig("Fig. 3(a) inset, 488 nm design", "transferred to this orange / red design", "10 %")
    src_band = fig("Fig. 1(c), device No. 2", "from the band gold FWHM", "1 um")
    top = c.view("top", "top view: thermo-optic section at true scale, EO section and outputs truncated")
    # cladding and its honeycomb lines, as they appear in the micrograph
    x_c0, x_c1, y_c0, y_c1 = -70.0, L + 190.0, -115.0, 205.0
    top.rect(x_c0, y_c0, x_c1, y_c1, "sio2", "SiO2 cladding", row("m8"), layer="oxide", alpha=0.8)
    pad_w, pad_h, pad_gap = 121.6, 80.6, 19.8  # Fig. 1(c): 178 x 118 px and 29 px at 3x against 2.05 um/px
    y_g0 = yD - hw
    y_v0 = y_g0 + pad_h + pad_gap

    def keep(x: float, y: float) -> bool:
        if not (x_c0 < x < x_c1 and y_c0 < y < y_c1):
            return False
        if -ARM - EDGE - BAND_D - 6 < y < yA + hw + 6 and -60 < x < L + 80:
            return False
        if x > L - 12 and x < L + pad_w + 6 and y_g0 - 6 < y < y_v0 + pad_h + 6:
            return False
        return True

    edges = honeycomb(20.5, x_c0, x_c1, y_c0, y_c1, keep)
    bars = []
    for (xa, ya), (xb, yb) in edges:
        d = math.hypot(xb - xa, yb - ya)
        nx, ny = -(yb - ya) / d * 1.0, (xb - xa) / d * 1.0  # 2 um line: 1 px in the micrograph
        bars.append([(xa + nx, ya + ny), (xb + nx, yb + ny), (xb - nx, yb - ny), (xa - nx, ya - ny)])
    top.rings(bars, "unknown", "honeycomb lines in the cladding: what they are is not stated", fig("Fig. 1(c)", "side 20.5 um against the 300 um bar", "10 %") + assumed("the paper does not say what these lines are; material left unknown, phase not matched"), alpha=0.5)

    # waveguides: S-bends from the EO section at the left, into the MMI at the right
    src_wg = row("m4") + fig("Fig. 1(c)", "arm spacing and S-bends", "3 um")
    port = 1.0
    src_mmi = assumed("MMI width, length and port offset not given in the paper body (Supporting Information not available); 2 x 2 from Fig. 1(b)")
    mmi_x0 = L + 53.0  # Fig. 1(c): arms meet 26 px after the section
    mmi_l, mmi_w = 40.0, 4.0
    for s in (1, -1):
        r = Route((-59.0, s * (ARM + 36.0)), 0.0, w_wg, tol=0.02)
        r.sbend(59.0, -s * 36.0)
        r.straight(L)
        r.sbend(53.0, -s * (ARM - port))
        top.route(r, "ln", "upper arm: heated" if s > 0 else "lower arm: beside the dummy", src_wg, layer="waveguide")
        r2 = Route((mmi_x0 + mmi_l, s * port), 0.0, w_wg, tol=0.02)
        r2.sbend(50.0, s * 12.0).straight(40.0)
        top.route(r2, "ln", "output to the edge coupler: truncated", assumed("routing to the facet truncated; offsets drafted"), layer="waveguide")
    top.rect(mmi_x0, -mmi_w / 2, mmi_x0 + mmi_l, mmi_w / 2, "ln", "2 x 2 MMI", src_mmi, layer="waveguide")

    # heater: one continuous gold path
    x_a = L - 2.0
    meander = [
        (0.0, yA + hw), (x_a, yA + hw), (x_a, yA - hw), (WIRE, yA - hw), (WIRE, yB + hw), (x1, yB + hw), (x1, yC - hw), (WIRE, yC - hw),
        (WIRE, yD + hw), (L, yD + hw), (L, yD - hw), (0.0, yD - hw), (0.0, yC + hw), (x1 - WIRE, yC + hw), (x1 - WIRE, yB - hw), (0.0, yB - hw),
    ]  # fmt: skip
    top.poly(meander, "metal", "gold heater wire, four passes in a cladding trench", src_wire, layer="metal")
    # lead strip beside the lower pad, up to the upper pad: only the micrograph has it
    strip = [(x_a - 7.0, yA + hw), (x_a, yA + hw), (x_a, y_v0), (L, y_v0), (L, y_v0 + 4.8), (x_a - 7.0, y_v0 + 4.8)]
    top.poly(strip, "metal", "lead strip from the outer pass past the G pad to the VTO pad", fig("Fig. 1(c)", "3.3 px wide, 1 px clear of the G pad", "2 um"), layer="metal")
    src_pad = fig("Fig. 1(c)", "pads against the 300 um bar; lower edge flush with the near pass", "3 um")
    top.rect(L, y_g0, L + pad_w, y_g0 + pad_h, "metal", "G pad", src_pad, layer="metal")
    top.rect(L, y_v0, L + pad_w, y_v0 + pad_h, "metal", "VTO pad", src_pad, layer="metal")
    # dummy: same spacing at the other arm, no contacts
    src_dummy = stated("p.4", "unheated copy at the other arm, equal offset from its waveguide") + fig("Fig. 1(c), device No. 2", "band gold FWHM 7.6 um, full section length", "1 um") + assumed("three bars from two dark slots at 2 um/px; Fig. 1(b) schematic draws four, Fig. 1(a) one")
    ys_d = [ARM + EDGE + WIRE / 2 + i * PITCH_D for i in range(N_DUMMY)]
    for i, yy in enumerate(ys_d):
        top.rect(0.0, -yy - hw, L, -yy + hw, "metal", f"dummy bar {i + 1} of {N_DUMMY}, no contact", src_dummy, layer="metal")

    top.dim("h", 0.0, L, -ys_d[-1] - hw, px=-30, ext=(-ys_d[-1] - hw, -ys_d[-1] - hw), row_id="m3")
    top.label((L + pad_w / 2, y_v0 + pad_h / 2), "VTO")
    top.label((L + pad_w / 2, y_g0 + pad_h / 2), "G")
    top.label((L / 2, yA + hw), "4-pass heater", dy=-8)
    top.label((L / 2, -ys_d[-1] - hw), "dummy", dy=12)
    top.label((mmi_x0 + mmi_l / 2, -mmi_w / 2), "2 x 2 MMI", dy=16)
    top.label((-59.0, 0.0), "from EO section", anchor="start", tip="The 1.35 mm EO section, its CPW and the 1 x 2 MMI lie to the left")
    top.note("Same gold layer as the CPW, so the wire is 900 nm thick and has to be long: four passes of the 0.75 mm section (Methods). Fig. 1(c) shows two neighbouring modulators; the pads of the next device below the dummy are not drawn.")
    top.note("Honeycomb lines in the cladding are in the micrograph; the paper does not say what they are, so they are dashed in a neutral material. Their phase is not matched and they are left out near the wires; the micrograph runs them up to the waveguide clearing.")
    top.note("Dummy band is narrower than the heater band in the micrograph (7.6 against 13.5 um), though Fig. 1(b) draws them alike. Three bars is the reading at 2 um/px: dashed.")
    c.thumb = {"view": "top", "window": [-20, -40, L + 140, 120]}

    e = c.view("end", "detail: pad end, lead strip, wire D straight into the G pad, inner U", like="top", window=(L - 55, -32, L + 135, 130))
    e.dim("h", L, L + pad_w, y_v0 + pad_h, px=14, ext=(y_v0 + pad_h, y_v0 + pad_h), text="122 um", src=src_pad)
    e.dim("v", y_g0, y_g0 + pad_h, L + pad_w, px=14, ext=(L + pad_w, L + pad_w), text="81 um", src=src_pad)
    e.dim("v", y_g0, y_v0, L + pad_w, px=52, ext=(L + pad_w, L + pad_w), text="100 um pitch", src=src_pad)
    e.note("Fig. 1(b) draws the pads against the outer passes without the strip; the micrograph has the upper pad lifted by one pitch and reached by this strip.")
    z = c.view("left", "detail: left ends of the passes, the two U turns at the left", like="top", window=(-6.0, ARM - 1.5, 26.0, yA + 2.5))
    z.dim("v", yD - hw, yD + hw, 0.0, px=-14, ext=(0.0, 0.0), text="1.22 um, from the 488 nm inset", src=src_tag)
    z.dim("v", yD, yC, 26.0, px=-16, ext=(26.0, 26.0), text="4.1 um", src=src_band)
    z.dim("v", ARM, yD - hw, 8.0, px=0, ext=(8.0, 8.0), text="4.0 um", src=src_band)
    z.note("Near pass D and pass C join at the left, as do B and A; B and C join at the right, 17 um before the section end. The waveguide runs just below the near pass.")

    # section at mid length: seen from the output end, heater on the right as in Fig. 3(a) inset
    half = 34.0
    x = c.view("xsec", "cross-section at mid section, seen from the output end: wires in cladding trenches", "xsec", window=(-half, -2.0, half, t_box + t_clad + 1.6))
    x.rect(-half, -2.0, half, 0.0, "si", "Si substrate: truncated", assumed("substrate thickness not stated: truncated"), layer="substrate", alpha=0.5)
    x.rect(-half, 0.0, half, t_box, "sio2", "buried oxide", row("m7"), layer="oxide")
    z_top = t_box + t_clad
    x.rect(-half, t_box, half, z_top, "sio2", "SiO2 cladding", row("m8"), layer="oxide", alpha=0.65)
    for s in (1, -1):
        x.rect(s * ARM - w_wg / 2, t_box, s * ARM + w_wg / 2, t_box + t_ln, "ln", "LiNbO3 strip, fully etched" + (", heated arm" if s > 0 else ""), row("m4", "m6"), layer="waveguide")
    z_h0 = t_box + t_ln + h_gap
    z_h1 = z_h0 + t_au
    src_x = row("m9", "m10") + src_tag + src_band + fig("Fig. 1(d)", "wire below the surface, in a trench")
    for i, yy in enumerate(ys):
        x.rect(yy - hw, z_h0, yy + hw, z_h1, "metal", f"gold heater wire, pass {i + 1} from the waveguide", src_x, layer="metal")
        x.rect(yy - hw, z_h1, yy + hw, z_top, "air", "air: trench above the wire", src_x[1:], layer="trench")
    for i, yy in enumerate(ys_d):
        x.rect(-yy - hw, z_h0, -yy + hw, z_h1, "metal", f"gold dummy bar {i + 1}", row("m9", "m10") + src_dummy, layer="metal")
        x.rect(-yy - hw, z_h1, -yy + hw, z_top, "air", "air: trench above the bar", src_dummy, layer="trench")
    x.dim("v", 0.0, t_box, -half + 1, px=0, ext=(-half + 1, -half + 1), row_id="m7")
    x.dim("v", t_box, z_top, 0.0, px=0, ext=(0.0, 0.0), row_id="m8")
    x.label((ARM, t_box), "heated arm", dy=16)
    x.label((-ARM, t_box), "other arm", dy=16)
    x.label((y_d + 1.5 * PITCH, z_top), "heater", dy=-8)
    x.label((-y_d - PITCH_D, z_top), "dummy", dy=-8)
    x.note("Fig. 3(a) inset and Fig. 1(b) have four heater wires, and the micrograph resolves three slots. Fig. 1(d) draws three wires in its platform schematic.")

    w = c.view("xsec_near", "detail: waveguide, near wires, 250 nm above the LiNbO3", "xsec", like="xsec", window=(ARM - 2.0, t_box - 1.0, y_d + 2 * PITCH + 1.5, z_top + 0.9))
    w.dim("v", t_box + t_ln, z_h0, y_d, px=0, ext=(y_d, y_d), row_id="m10")
    w.dim("v", z_h0, z_h1, y_d + hw + PITCH, px=14, ext=(y_d + hw + PITCH, y_d + hw + PITCH), row_id="m9")
    w.dim("h", ARM - w_wg / 2, ARM + w_wg / 2, t_box, px=-16, ext=(t_box, t_box), row_id="m4")
    w.dim("v", t_box, t_box + t_ln, ARM + w_wg / 2, px=12, ext=(ARM + w_wg / 2, ARM + w_wg / 2), row_id="m6")
    w.dim("h", ARM, y_d - hw, z_top, px=14, ext=(z_top, z_top), text="4.0 um", src=src_band)
    w.dim("h", y_d - hw, y_d + hw, z_top, px=30, ext=(z_top, z_top), text="1.22 um, from the 488 nm inset", src=src_tag)
    w.note("Wire trench walls as Fig. 3(a) inset: the trench width equals the wire. The paper does not state the lateral spacing. The inset shows 2.2 um for the 488 nm design; device No. 2 reads about 4 um (+- 1.5) from band centres and clearings, drawn here.")

    # closure
    c.check("heater path, 4 passes of the section: bulk Au 2.44e-8 ohm m at 1.22 um x 900 nm against the measured 80 ohm (a film runs above bulk), ohm", 2.44e-8 * (4 * L * 1e-6) / (WIRE * 1e-6 * t_au * 1e-6), 80.0, 0.25)
    c.check("recess: cladding - LN - 250 nm gap - 900 nm wire, against 17 px (+- 1 px) in Fig. 3(a) inset, um", t_clad - t_ln - h_gap - t_au, 17 / INSET, 0.06)
    c.check("cladding, 89 px in Fig. 3(a) inset against the row, um", 89 / INSET, t_clad, 0.03)
    c.check("wire thickness, 49 px in Fig. 3(a) inset against the row, um", 49 / INSET, t_au, 0.02)
    c.check("waveguide width, 20 px in Fig. 3(a) inset against the row (reading +- 2 px), um", 20 / INSET, w_wg, 0.15)
    c.check("section length, 371 px in the embedded micrograph against the row, um", 371 * UM_PX, L, 0.03)
    c.check("drawn pitch against the dark-slot spacing in the heater band, Nos. 2 and 3: 2.33 px mean (reading +- 0.5 px), um", PITCH, 2.33 * UM_PX, 0.25)
    c.check("waveguide to near wire: from band centres and clearings, against the direct clearing to band edge reading 4.3 um, um", EDGE, 4.3, 0.2)
    c.check("pad pitch, 49 px in Fig. 1(c) against G + gap drawn, um", 49 * UM_PX, pad_h + pad_gap, 0.01)
    return c
