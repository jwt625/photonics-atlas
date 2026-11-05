"""El-Saeed 2024: straight symmetric 0.5:0.5 directional coupler, the reference device (Fig. 1(a), Fig. 1 caption, Fig. 8 caption).

The straight DC itself appears only as the schematic Fig. 1(a): four ports, two S-bends per side made of circular bends of
radius 5 um, straight coupling length L. Fig. 1(a) has no scale and the port pitch of the straight DC is not printed. The only
scaled view is the SEM of the bent DC next to it, Fig. 1(c): its ports are 164-166 px apart against a 123-125 px bar for 5 um,
so about 6.7 um. That sibling value is used as an assumption and sets the sweep of the arcs: arcs and stubs are dashed and the
pitch carries no label. The cross-section takes its shape from the SEM Fig. 1(d)
of the coupling region and its dimensions from the table.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, assumed, fig, row, stated  # noqa: E402

ID = "cmp_lit_elsaeed2024_straight_dc_50"


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 1(a) schematic", "Fig. 1(c) SEM of the bent DC, for the port pitch only", "Fig. 1(d) SEM cross-section", "Fig. 1 caption", "Fig. 5 and Fig. 8 captions"],
        "Straight DC: 5.228 um coupling section, four ports, S-bends of two circular 5 um arcs; port pitch assumed from the bent DC SEM",
    )
    gap = c.um("m4")
    l_c = c.um("m5")
    w = c.um("m6")
    t = c.um("m7")
    r_b = c.um("m8")
    pitch = 6.7  # assumption: ports of the bent DC, Fig. 1(c), 6.6 to 6.75 um
    y_c = (gap + w) / 2
    h = pitch / 2 - y_c
    theta = math.degrees(math.acos(1 - h / (2 * r_b)))
    stub = 2.5
    src_bend = row("m6", "m8") + stated("Fig. 1 caption", "traditional circular bends") + fig("Fig. 1(a)", "two arcs per S-bend, four ports") + assumed("port pitch of the straight DC not printed: about 6.7 um from the SEM of the bent DC, Fig. 1(c), a sibling device, sets the arc sweep; end stub length is a drafting choice")
    src_c = row("m4", "m5", "m6")

    tp = c.view("top", "top view: coupling section, S-bends, four ports")
    for s in (1.0, -1.0):
        tp.route(Route((-l_c / 2, s * y_c), 0.0, w).straight(l_c), "si", "coupling section", src_c, layer="waveguide")
        right = Route((l_c / 2, s * y_c), 0.0, w, tol=0.004)
        right.arc(r_b, s * theta).arc(r_b, -s * theta).straight(stub)
        tp.route(right, "si", "S-bend to the " + ("through port" if s > 0 else "cross port"), src_bend, layer="waveguide")
        left = Route((-l_c / 2, s * y_c), 180.0, w, tol=0.004)
        left.arc(r_b, -s * theta).arc(r_b, s * theta).straight(stub)
        tp.route(left, "si", "S-bend to the " + ("input port" if s > 0 else "fourth port"), src_bend, layer="waveguide")
    x_end = l_c / 2 + 2 * r_b * math.sin(math.radians(theta)) + stub
    tp.dim("h", -l_c / 2, l_c / 2, y_c + w / 2, px=28, ext=(y_c, y_c), row_id="m5")
    tp.label((-x_end, pitch / 2), "input", anchor="start", dy=-9)
    tp.label((x_end, pitch / 2), "through", anchor="end", dy=-9)
    tp.label((x_end, -pitch / 2), "cross", anchor="end", dy=16)
    r_at = (l_c / 2 + r_b * math.sin(math.radians(theta)), y_c + r_b * (1 - math.cos(math.radians(theta))))
    tp.label(r_at, "bend radius", anchor="start", dx=10, dy=-6, row_id="m8")
    tp.note("Ports continue to the test structures, truncated. Sweep of the arcs and end stubs follow from an assumed port pitch: no dimension can be read from them.")
    tp.note("Fig. 7(a) puts the 0.5 crossing near 4.75 um at 1.31 um wavelength; at this L it reads 0.56. Fig. 8(a) crosses 0.5 near 1.275 um.")
    c.thumb = {"view": "top"}

    det = c.view("gap", "detail: coupling section, width and gap", like="top", window=(-l_c / 2 - 0.8, -0.8, l_c / 2 + 0.8, 0.8))
    det.dim("v", y_c - w / 2, y_c + w / 2, -l_c / 2 + 0.4, px=-16, ext=(-l_c / 2 + 0.4, -l_c / 2 + 0.4), row_id="m6")
    det.dim("v", -gap / 2, gap / 2, l_c / 2 - 0.4, px=16, ext=(l_c / 2 - 0.4, l_c / 2 - 0.4), row_id="m4")
    det.dim("h", -l_c / 2, l_c / 2, -y_c - w / 2, px=-22, ext=(-y_c, -y_c), row_id="m5")

    x = c.view("xsec", "cross-section in the coupling section", "xsec")
    box, clad, span = 1.2, 0.5, 1.2
    x.rect(-span, -box - 0.25, span, -box, "si", "Si substrate", assumed("substrate: truncated"), alpha=0.5, layer="substrate")
    x.rect(-span, -box, span, 0.0, "sio2", "buried oxide", assumed("BOX thickness not stated in this paper"), layer="oxide")
    x.rect(-span, 0.0, span, t + clad, "sio2", "SiO2 top cladding", stated("Fig. 1 caption", "silicon oxide top cladding") + assumed("cladding thickness not stated"), alpha=0.45, layer="oxide")
    for s in (1.0, -1.0):
        x.rect(s * y_c - w / 2, 0.0, s * y_c + w / 2, t, "si", "Si strip", row("m4", "m6", "m7") + fig("Fig. 1(d)", "near-vertical sidewalls"), layer="waveguide")
    x.dim("h", y_c - w / 2, y_c + w / 2, t, px=14, ext=(t, t), row_id="m6")
    x.dim("h", -gap / 2, gap / 2, t, px=32, ext=(t, t), row_id="m4")
    x.dim("v", 0.0, t, y_c + w / 2, px=18, ext=(y_c + w / 2, y_c + w / 2), row_id="m7")
    x.note("Fig. 1(d) shows the bent DC in its coupling region, reading 0.36 um wide with a 0.12 um gap edge to edge against its 0.2 um bar; the drawing is the nominal row values (Fig. 1 caption: all DCs).")
    return c
