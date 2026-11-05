"""OFC 2026 Tu2D.4: Si / SiN adiabatic transition of the STMicroelectronics PIC100G back-side platform. Text only: Fig. 1 and Fig. 2 not available.

What the text fixes is the orientation, which is the point of this platform. 300 nm SOI on 200 nm BOX is patterned from the
front; BEOL and a thick planar oxide are added; the wafer is bonded front-side down on a high-resistivity carrier; the
original handle is removed; SiN is then built on the back side. In the finished chip, from the carrier upward: thick oxide
above 5 um (reconstructed BOX), Si (its etched face looking down), then the bottom SiN level.
The Si to SiN spacing is not stated. 200 nm is given only for the starting SOI; whether the BOX is kept in full after the handle
is removed is not stated, nor any liner. It is drawn at 200 nm as an inference, dashed, without a dimension.
Taper length, tips and widths are not stated either. "400nm strip" is not said to be a thickness or a width; it is drawn as the
thickness and labelled as printed.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, assumed, row, stated  # noqa: E402

ID = "cmp_ofc2026_tu2d4_si_sin_transition"


def build() -> Cell:
    c = Cell(ID, ["Sec. 2 (text only)", "Sec. 3, Table 1 (text only)", "Fig. 1, Fig. 2, Fig. 3 not available"], "Back-side stack in chip orientation: carrier, thick oxide above 5 um, Si, SiN; the Si to SiN spacing is inferred from the starting BOX, widths not stated")
    t_si = c.um("m5")
    t_box = 0.2  # inferred: Sec. 2 gives 200 nm for the starting SOI only; retention after handle removal not stated
    t_thick = 5.0  # Sec. 1: reconstructed BOX above 5 um, drawn at the lower bound
    t_sin = 0.4  # Sec. 2: "400nm strip", read as thickness
    # drafting values, no label
    length, w_si, w_sin, w_tip, stub, clad = 40.0, 0.4, 1.0, 0.15, 10.0, 2.0
    y_sin = t_si + t_box
    why = assumed("adiabatic is stated; taper length, tip and waveguide widths are not, and which layer tapers which way is the usual opposed pair")

    top = c.view("top", "top view: assumed adiabatic bilayer taper, no dimension is from the source")
    top.route(Route((0.0, 0.0), 0.0, w_tip).straight(length, w_si), "si", "Si waveguide, front-side level", why, layer="waveguide")
    top.route(Route((length, 0.0), 0.0, w_si).straight(stub), "si", "Si waveguide", why, layer="waveguide")
    top.route(Route((0.0, 0.0), 0.0, w_sin).straight(length, w_tip), "sin", "SiN strip, bottom SiN level, back side", why, layer="overlay", alpha=0.6)
    top.route(Route((-stub, 0.0), 0.0, w_sin).straight(stub), "sin", "SiN strip", why, layer="overlay", alpha=0.6)
    top.label((-stub, 0.9), "SiN, back side", anchor="start")
    top.label((length + stub, 0.5), "Si, front side", anchor="end")
    top.note("Text only: adiabatic transition between Si and SiN, using the 400 nm strip at the bottom SiN level. This plan view is a placeholder, not the device.")
    c.thumb = {"view": "xsec", "window": [-3.5, -0.8, 3.5, 2.0]}

    x = c.view("xsec", "cross-section in the overlap, finished chip orientation", "xsec", window=(-3.6, -t_thick - 0.9, 3.6, y_sin + t_sin + clad + 0.1))
    half = 5.0
    x.rect(-half, -t_thick - 2.0, half, -t_thick, "si", "high-resistivity Si carrier", stated("Sec. 2", "bonded carrier") + assumed("carrier thickness: truncated"), layer="substrate", alpha=0.5)
    x.rect(-half, -t_thick, half, 0, "sio2", "BEOL plus bonding oxide: reconstructed BOX", stated("Sec. 1", "thick oxide above 5 um; drawn at 5 um"), layer="oxide")
    x.rect(-half, 0, half, t_si, "sio2", "oxide around the patterned Si", stated("Sec. 2", "patterned before the BEOL oxide fills it"), layer="oxide", alpha=0.7)
    x.rect(-half, t_si, half, y_sin, "sio2", "Si to SiN spacing, inferred from the starting BOX", stated("Sec. 2", "200 nm BOX of the starting SOI") + assumed("spacing inferred: BOX retention after handle removal is not stated, nor any liner"), layer="oxide", alpha=0.55)
    x.rect(-half, y_sin, half, y_sin + t_sin + clad, "sio2", "oxide above the SiN levels", assumed("back-side cladding thickness not stated"), layer="oxide", alpha=0.35)
    w_si_mid, w_sin_mid = (w_tip + w_si) / 2, (w_sin + w_tip) / 2
    x.rect(-w_si_mid / 2, 0, w_si_mid / 2, t_si, "si", "Si, 300 nm SOI layer, etched face down", row("m5") + assumed("strip and width at the transition not stated"), layer="waveguide")
    x.rect(-w_sin_mid / 2, y_sin, w_sin_mid / 2, y_sin + t_sin, "sin", "SiN, bottom level; '400nm strip'", stated("Sec. 2", "400nm strip at the bottom level") + assumed("400 nm read as thickness; width not stated; spacing to the Si inferred"), layer="overlay")
    x.dim("v", -t_thick, 0, -3.0, px=0, ext=(-3.0, -3.0), text="> 5 um", src=stated("Sec. 1", "reconstructed BOX above 5 um"))
    x.label((0.6, -2.5), "BEOL oxide + bond", anchor="start")
    x.label((0.0, -t_thick - 0.9), "HR carrier", dy=-4)
    x.note("Upward from the carrier: thick oxide, Si, then SiN, since the SOI is flipped on the carrier and SiN is built after the handle is removed (Sec. 2).")
    x.note("The 200 nm strip SiN level of the edge coupler (Sec. 2) is not drawn: it is not stated to extend into this transition.")
    x.note("Sidewalls drawn vertical: not stated. Widths have no source. A rib elsewhere on this platform would point down, slab on the BOX side, from the same flip.")
    y = c.view("core", "detail: Si, inferred spacing, bottom SiN level", "xsec", like="xsec", window=(-1.5, -0.35, 1.5, 1.35))
    y.dim("v", 0, t_si, w_si_mid / 2, px=20, ext=(w_si_mid / 2, w_si_mid / 2), row_id="m5")
    y.label((1.45, y_sin - t_box / 2), "spacing inferred: 200 nm starting BOX, retention not stated", anchor="end")
    y.label((w_sin_mid / 2, y_sin + t_sin / 2), "400nm strip (as printed)", anchor="start", dx=8)
    y.label((-1.4, t_si / 2), "Si, etched face down", anchor="start")
    return c
