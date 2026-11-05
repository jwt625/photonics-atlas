"""Isichenko 2023 ultra-high-Q Si3N4 ring, R 5.84 mm, 40 nm x 4 um core at 780 nm (Fig. 1(b), Fig. 1(d), Fig. 2(a), p.3).

Topology from the infrared image Fig. 1(d) and the schematic Fig. 2(a): a circular ring and one straight bus running from
the left facet across the whole frame, tangent at the top of the ring. Circular, one bus, no pulley, no heater.
Facet and chip edge positions are read off Fig. 1(d) against the ring radius (least-squares circle: centre 1139.5, 925.7, R 292.3 px, rms 0.5 px).
Gap and bus width are not stated anywhere: assumed, dashed. No gap value is labelled.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, assumed, circle, fig, row  # noqa: E402

ID = "cmp_lit_isichenko2023_sin_ring_780"


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 1(b)", "Fig. 1(c)", "Fig. 1(d)", "Fig. 2(a)", "p.3 text"],
        "Circular all-pass ring with one straight facet-to-facet bus as in Fig. 1(d); hairline at true scale, coupler and core in detail views; gap and bus width assumed",
    )
    r = c.um("m6")
    w = c.um("m8")
    t = c.um("m7")
    box = c.um("m9")
    clad = c.um("m10")
    gap = 4.0  # not stated: drafting value, never labelled
    wb = w  # not stated: same as the ring
    y_bus = r + w / 2 + gap + wb / 2
    um_per = r / 292.3  # Fig. 1(d), circle fit in image px
    x_facet = -(1139.5 - 837) * um_per  # ring centre to the left facet, image column 837
    y_edge = y_bus + (632 - 592) * um_per  # bus to the top chip edge, image rows 632 and 592
    x_frame = (1358 - 1139.5) * um_per  # ring centre to the right end of the image

    src_ring = row("m6", "m8") + fig("Fig. 1(d)", "circular ring, no racetrack section visible")
    src_bus = assumed("bus width and gap not stated; drawn at the ring width with a drafting gap") + fig("Fig. 1(d), Fig. 2(a)", "one straight bus tangent at the ring")
    src_edge = fig("Fig. 1(d)", "chip edges by ratio to the ring radius", "5 %")

    top = c.view("top", "top view: ring and bus at true scale, as in the infrared image of Fig. 1(d)")
    top.rings([circle((0, 0), r + w / 2, tol=0.05), circle((0, 0), r - w / 2, tol=0.05)], "sin", "ring, 4 um wide: a hairline at this scale", src_ring, layer="waveguide")
    bus = Route((x_facet, y_bus), 0.0, wb)
    bus.straight(x_frame - x_facet + 1400.0)
    top.route(bus, "sin", "bus waveguide", src_bus, layer="waveguide")
    top.line([(x_facet, y_edge), (x_facet, -r)], "left chip facet", src_edge)
    top.line([(x_facet, y_edge), (x_frame, y_edge)], "top chip edge", src_edge)
    top.line([(0, 0), (r * math.cos(math.radians(125)), r * math.sin(math.radians(125)))], "radius", row("m6"))
    top.label((r * 0.5 * math.cos(math.radians(125)), r * 0.5 * math.sin(math.radians(125))), "R", anchor="start", dx=6, row_id="m6")
    top.label((x_facet, y_bus), "laser in", anchor="start", dx=4, dy=14)
    top.label(bus.pos, "to PD", anchor="end", dy=14)
    top.dim("h", x_facet, 0, y_edge, px=12, ext=(y_edge, y_edge), text=f"{-x_facet / 1e3:.1f} mm", src=src_edge)
    top.note("Ring 36.7 mm long and 4 um wide: a hairline at true scale, as in the image. The bus right of the frame of Fig. 1(d) is extended only to show it leaves the ring.")
    top.note("In Fig. 1(d) the bus, tilted 0.3 deg in the image, crosses image row 633.1 at the tangent point and the ring top is at 633.2: tangent, but at 20 um per pixel the gap is not resolved.")
    top.note("Fig. 1(d) also shows a faint smaller circle inside the ring, a neighbouring structure: not drawn. Lower half and bottom chip edge are outside that figure.")
    c.thumb = {"view": "top"}

    wide = c.view("wide", "detail: coupling region, ring and bus converging", like="top", window=(-260, r - 25, 260, r + 24))
    wide.label((0, y_bus), "gap and bus width not stated", dy=-12)
    wide.note("Separation grows as x^2 / 2R: 5 um at 230 um from the tangent point (from the row radius alone).")

    close = c.view("close", "detail: coupler at the tangent point", like="top", window=(-25, r - 5, 25, y_bus + 5))
    close.dim("v", r - w / 2, r + w / 2, 0.0, px=-30, ext=(0.0, 0.0), row_id="m8")
    close.label((0, y_bus), "bus (dashed: width and gap assumed)", dy=-20)

    half = 12.0
    x = c.view("xsec", "cross-section, Fig. 1(b), at the coupler", "xsec")
    x.rect(-half, -box - 3.0, half, -box, "si", "Si substrate", assumed("thickness not stated: truncated"), layer="substrate", alpha=0.5)
    x.rect(-half, -box, half, 0, "sio2", "SiO2 lower cladding", row("m9"), layer="oxide")
    x.rect(-half, 0, half, clad, "sio2", "SiO2 upper cladding", row("m10"), layer="oxide", alpha=0.45)
    x.rect(-w / 2, 0, w / 2, t, "sin", "Si3N4 ring core", row("m7", "m8"), layer="waveguide")
    x.rect(w / 2 + gap, 0, w / 2 + gap + wb, t, "sin", "Si3N4 bus core", assumed("bus width and gap not stated"), layer="waveguide")
    x.dim("h", -w / 2, w / 2, clad, px=12, ext=(t, t), row_id="m8")
    x.dim("v", 0, clad, -half, px=-10, ext=(-half, -half), row_id="m10")
    x.dim("v", -box, 0, -half, px=-10, ext=(-half, -half), row_id="m9")
    x.note("TM mode is the one used (p.3).")

    z = c.view("xcore", "detail: core edge, 40 nm thick", "xsec", like="xsec", window=(-w / 2 - 0.2, -0.07, -w / 2 + 0.2, 0.11))
    z.dim("v", 0, t, -w / 2 + 0.1, px=12, ext=(-w / 2, -w / 2 + 0.1), row_id="m7")

    c.check("drawn ring radius against the Fig. 1(d) label 5.8 mm, um", r, 5800.0, 0.01)
    c.check("drawn ring is a circle: Fig. 1(d) circle fit to the top arc against the left arc, px", 291.5, 296.0, 0.02)
    c0 = 299792.458  # um GHz
    lam = 0.78
    c.check("rows only, nothing drawn: loaded Q from the 6 MHz linewidth against the row", c0 / lam / (c.num("m3") * 1e-3), c.num("m2"), 0.02)
    # alpha = 2 pi ng / (lambda Qi): group index implied by the 0.36 dB/m and 145 M rows; mode mostly in SiO2 (assumed about 1.47)
    alpha_per_um = c.num("m5") / 4.343 * 1e-4
    c.check("rows only, nothing drawn: group index implied by the loss and Qi rows against about 1.47 (mode mostly in SiO2)", alpha_per_um * lam * c.num("m1") / (2 * math.pi), 1.47, 0.03)
    return c
