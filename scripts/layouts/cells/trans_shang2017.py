"""Shang 2017: asymmetric Si3N4 vertical coupler, 50 nm middle layer to 150 nm upper layer (Fig. 2, Fig. 4(a), Fig. 9(a), Sec. 2, Sec. 4).

Fig. 9(a) is the device photo: a wide band enters from the left (input port, 50 nm layer) and narrows slowly to the right;
the 150 nm output port starts as a sharp tip on the axis, above the band where it is still about full width, and runs off
the right edge of the image, 43 um past the tip. Sec. 4: the 150 nm tip lies above the 50 nm inverse taper, all tapers 100 um.
Read on the embedded image, scale bar 84.5 px = 10 um:
- input band 36.5 px = 4.3 um, against 4 um printed in Fig. 4(a) for the Y-junction.
- lower edge of the 50 nm band: y 199 px up to z = 3 um, 191 px at z = 40 um, axis 181.5 px: 2.25 um wide there, drawn 2.5 um.
- 150 nm line: 10 px at the tip (fit), 15.3 px at z = 42 um, half-level extent of the bright and dark fringes. This is blur
  dominated. Blur removed, the width at z = 42 um is 0.85 um (linear subtraction) to 1.36 um (quadrature); the linear taper
  drawn gives 0.77 um. Growth 0.120 +- 0.022 px/um against 0.106 px/um drawn. The photo neither fixes the profile nor
  excludes the linear one, so the drawn profile stays an assumption and is not checked against the photo.
The 1.5 um output width (Fig. 4(a), Y-junction) is outside the frame of Fig. 9(a). Tip widths for this coupler are not stated.
The fabricated gap is not stated: drawn at the 600 nm of the Y-junctions in the same run (Sec. 4), and marked assumed.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, assumed, fig, row, stated  # noqa: E402

ID = "cmp_lit_shang2017_vertical_coupler"


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 9(a)", "Fig. 2", "Fig. 4(a)", "Sec. 2", "Sec. 4"],
        "50 nm inverse taper from the 4 um input port under the 150 nm taper, 100 um overlap; tip widths, output width, taper profile and gap assumed",
    )
    length = c.um("m3")
    t_thick, t_thin = c.um("m4"), c.um("m5")
    w_in = 4.0  # Fig. 4(a) label, Fig. 9(a) reading 4.2 um
    w_out = 1.5  # Fig. 4(a) label, Fig. 9(a) reading 1.4 to 1.8 um with blur
    w_tip = 0.25  # Sec. 3: Y-junction tip width, not stated for this coupler
    gap = 0.6  # Sec. 4: fabricated Y-junction lower gap; this coupler's gap not stated
    box, clad = 3.0, 3.0  # oxide bands: not stated
    px_um = 8.45  # Fig. 9(a), embedded image: scale bar 84.5 px = 10 um
    stub_in, stub_out = 11.5, 20.0  # Fig. 9(a): photo left edge 97 px before the tip
    z_edge = 43.0  # Fig. 9(a): photo right edge 364 px past the tip

    src_in = fig("Fig. 9(a)", "band width against the 10 um bar", "10 %") + stated("Fig. 4(a)", "4 um input port, Y-junction")
    src_out = stated("Fig. 4(a)", "1.5 um output port, Y-junction") + assumed("same width on this coupler: that plane is outside the frame of Fig. 9(a)")
    profile = assumed("linear taper profile: not stated; Fig. 9(a) is blur dominated at the line and does not fix it")
    src_tip = assumed("tip width not stated for this coupler: 250 nm of the Y-junction (Sec. 3, Fig. 4(a))")

    top = c.view("top", "top view: input port, 50 nm taper below, 150 nm taper above")
    lower = Route((0.0, 0.0), 0.0, w_in).straight(length, w_tip)
    upper = Route((0.0, 0.0), 0.0, w_tip).straight(length, w_out)
    top.route(Route((-stub_in, 0.0), 0.0, w_in).straight(stub_in), "sin", "input port, 50 nm Si3N4 (middle layer)", row("m5") + src_in, layer="slab", alpha=0.45)
    top.route(lower, "sin", "50 nm Si3N4 inverse taper (middle layer)", row("m3", "m5") + src_in + fig("Fig. 9(a)", "band narrows to the right of the tip") + src_tip + profile, layer="slab", alpha=0.45)
    top.route(upper, "sin", "150 nm Si3N4 taper (upper layer)", row("m3", "m4") + src_out + stated("Sec. 4", "150 nm tip lies above the 50 nm inverse taper") + src_tip + profile, layer="waveguide", alpha=0.9)
    top.route(Route((length, 0.0), 0.0, w_out).straight(stub_out), "sin", "output port, 150 nm Si3N4", row("m4") + src_out, layer="waveguide", alpha=0.9)
    top.dim("h", 0, length, -2.0, px=-14, ext=(-w_in / 2, -w_tip / 2), row_id="m3")
    top.label((-stub_in, 2.4), "input port, 50 nm", anchor="start")
    top.label((length + stub_out, 1.4), "output port, 150 nm", anchor="end")
    top.note("Tapers drawn linear over the stated 100 um, on the same axis (Fig. 9(a), misalignment within 50 nm, Sec. 4). Profile and 250 nm tips not stated for this coupler.")
    top.note("Measured in cascades of 16, 24, 32 and 40 couplers (Fig. 9(c)); the cascade layout is not shown in the paper and is not drawn.")
    c.thumb = {"view": "top", "window": [-stub_in, -9.0, length + stub_out, 9.0]}

    # the window of the device photo: 54.5 um wide, tip 11.5 um from the left edge
    photo = c.view("photo", "window of the device photo, Fig. 9(a); taper profile assumed", like="top", window=(-stub_in, -20.0, z_edge, 20.0))
    photo.dim("v", -w_in / 2, w_in / 2, -6.0, px=0, ext=(-6.0, -6.0), text="4 um", src=src_in)
    photo.label((1.0, 3.2), "150 nm tip above the 50 nm band", anchor="start")
    photo.note("Same topology as Fig. 9(a): band enters at the left, tip on the axis 11.5 um from the frame edge, line runs off the right edge.")
    photo.note("Widths differ at the right edge: the line is drawn 0.77 um there, the photo reads 1.8 um raw, 0.85 to 1.36 um with blur removed by two models. The band is drawn 2.5 um, the photo reads 2.25 um.")

    tip = c.view("tip", "detail: 150 nm tip above the full-width 50 nm band", like="top", window=(-3.0, -2.5, 7.0, 2.5))
    tip.dim("v", -w_in / 2, w_in / 2, -1.5, px=0, ext=(-1.5, -1.5), text="4 um", src=src_in)
    end = c.view("end", "detail: 50 nm tip below the full-width 150 nm line", like="top", window=(length - 7.0, -1.25, length + 3.0, 1.25))
    end.label((length + 1.5, w_out / 2), "1.5 um on the Y-junction, Fig. 4(a); assumed here", dy=-6)

    # closure at planes inside the photo: input port, and the band at z = 40 um (lower edge 191 px, axis 181.5 px)
    c.check("input port width um: drawn against Fig. 9(a), 36.5 px", w_in, 36.5 / px_um, 0.10)
    c.check("50 nm band width at z = 40 um, um: drawn against Fig. 9(a), 2 x 9.5 px", w_in + (w_tip - w_in) * 40.0 / length, 2 * 9.5 / px_um, 0.20)

    y2 = 0.0  # underside of the 50 nm layer
    y3 = t_thin + gap

    def stack(x: object, x0: float, x1: float) -> None:
        x.rect(x0, -box - 1.5, x1, -box, "si", "6-inch Si wafer", assumed("wafer thickness: truncated"), layer="substrate", alpha=0.5)
        x.rect(x0, -box, x1, y2, "sio2", "lower SiO2, LPCVD (with the 150 nm bottom layer buried here, removed at this device)", assumed("lower oxide and lower gap not stated for this device"), layer="oxide")
        x.rect(x0, y2, x1, y3, "sio2", "inter-layer SiO2 gap", assumed("gap of this coupler not stated: 600 nm of the fabricated Y-junctions, Sec. 4; simulated loss below 0.1 dB for gaps below 1.4 um, Sec. 2"), layer="oxide", alpha=0.65)
        x.rect(x0, y3, x1, y3 + t_thick + clad, "sio2", "upper SiO2 cladding", assumed("top cladding not stated"), layer="oxide", alpha=0.35)

    # long section on the axis: thicknesses at true scale
    lg = c.view("long", "long section on the axis, gap assumed", "xsec", window=(-stub_in - 2.0, -1.5, length + stub_out + 2.0, 2.5))
    stack(lg, -stub_in - 4.0, length + stub_out + 4.0)
    lg.rect(-stub_in, y2, length, y2 + t_thin, "sin", "50 nm Si3N4 (middle layer), ends at the taper tip", row("m5", "m3"), layer="slab")
    lg.rect(0, y3, length + stub_out, y3 + t_thick, "sin", "150 nm Si3N4 (upper layer), starts at the taper tip", row("m4", "m3") + stated("Sec. 4", "above the 50 nm layer"), layer="waveguide")
    lg.dim("h", 0, length, y3 + t_thick, px=14, ext=(y3 + t_thick, y3 + t_thick), row_id="m3")
    lg.note("Both axes at the same scale. The 50 nm layer is below a pixel here; see the details.")
    e0 = c.view("long_tip", "long section: start of the overlap", "xsec", like="long", window=(-2.5, -0.35, 2.5, 1.15))
    e0.dim("v", y2, y2 + t_thin, -1.5, px=0, ext=(-1.5, -1.5), row_id="m5")
    e0.dim("v", y3, y3 + t_thick, 1.5, px=0, ext=(1.5, 1.5), row_id="m4")
    e0.label((-1.2, y3 + t_thick / 2), "150 nm layer starts")
    e1 = c.view("long_end", "long section: end of the overlap", "xsec", like="long", window=(length - 2.5, -0.35, length + 2.5, 1.15))
    e1.label((length + 1.2, y2 + t_thin / 2), "50 nm layer ends", dy=-12)

    def section(vid: str, title: str, z: float, window: tuple[float, float, float, float]) -> None:
        w2 = w_in + (w_tip - w_in) * z / length
        w3 = w_tip + (w_out - w_tip) * z / length
        x = c.view(vid, title, "xsec", window=window)
        stack(x, -6.0, 6.0)
        x.rect(-w2 / 2, y2, w2 / 2, y2 + t_thin, "sin", f"50 nm Si3N4, {w2:.2f} um wide here", row("m5") + src_in + src_tip, layer="slab")
        x.rect(-w3 / 2, y3, w3 / 2, y3 + t_thick, "sin", f"150 nm Si3N4, {w3:.2f} um wide here", row("m4") + src_out + src_tip, layer="waveguide")
        x.dim("v", y2, y2 + t_thin, w2 / 2, px=16, ext=(w2 / 2, w2 / 2), row_id="m5")
        x.dim("v", y3, y3 + t_thick, w3 / 2, px=16, ext=(w3 / 2, w3 / 2), row_id="m4")
        x.note("Gap, oxide bands and substrate are assumed (dashed). Sidewalls drawn vertical: not stated.")

    section("xsec", "cross-section at mid taper, z = 50 um", 50.0, (-3.5, -0.5, 3.5, 1.5))
    section("xsec_tip", "cross-section at the 150 nm tip, z = 0", 0.0, (-3.5, -0.5, 3.5, 1.5))
    return c
