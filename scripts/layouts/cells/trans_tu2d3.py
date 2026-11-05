"""OFC 2026 Tu2D.3: Si to SiN transition of the Samsung Foundry platform. Text and captions only: Fig. 1 and Table 1 not available.

The text fixes the layers and their order (305 nm Si on 2 um oxide, 400 nm SiN deposited after the Si is patterned) and the
TE loss. It gives no taper length, tip width, waveguide width, gap or even the word adiabatic. The plan view is therefore
a drafting assumption from end to end, drawn dashed with no dimensions; only the thicknesses are from the paper.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, assumed, row  # noqa: E402

ID = "cmp_ofc2026_tu2d3_si_sin_transition"


def build() -> Cell:
    c = Cell(ID, ["Sec. 2 (text only)", "Sec. 3 (text only)", "Fig. 1 and Table 1 not available"], "Layer stack of the transition from the text: 305 nm Si, 400 nm SiN above it, 2 um BOX; widths, gap and cladding not stated")
    t_si, t_sin, box = c.um("m2"), c.um("m3"), c.um("m4")
    # drafting values, no label: the paper states none of them
    length, w_si, w_sin, w_tip, stub, gap, clad = 40.0, 0.4, 1.0, 0.15, 10.0, 0.2, 2.0
    y_sin = t_si + gap
    why = assumed("taper shape, length, widths and overlap not in the text; Fig. 1 not available")

    top = c.view("top", "top view: assumed bilayer taper, no dimension is from the source")
    top.route(Route((0.0, 0.0), 0.0, w_tip).straight(length, w_si), "si", "Si waveguide, lower level", why, layer="waveguide")
    top.route(Route((length, 0.0), 0.0, w_si).straight(stub), "si", "Si waveguide", why, layer="waveguide")
    top.route(Route((0.0, 0.0), 0.0, w_sin).straight(length, w_tip), "sin", "SiN waveguide, upper level", why, layer="overlay", alpha=0.6)
    top.route(Route((-stub, 0.0), 0.0, w_sin).straight(stub), "sin", "SiN waveguide", why, layer="overlay", alpha=0.6)
    top.label((-stub, 0.9), "SiN", anchor="start")
    top.label((length + stub, 0.5), "Si", anchor="end")
    top.note("Text and captions only: the paper states only the layers and the TE-mode loss between Si WG and SiN WG. This plan view is a placeholder for the layer pair, not the device.")
    top.note("Si patterned in three etch steps (Sec. 2); which of them forms the Si end of the transition is not stated. Strip drawn.")
    c.thumb = {"view": "xsec", "window": [-1.6, -0.4, 1.6, 1.0]}

    x = c.view("xsec", "cross-section in the overlap: layer thicknesses from the text", "xsec", window=(-2.2, -box - 0.6, 2.2, y_sin + t_sin + clad + 0.1))
    half = 3.0
    x.rect(-half, -box - 1.5, half, -box, "si", "Si handle", assumed("handle thickness: truncated"), layer="substrate", alpha=0.5)
    x.rect(-half, -box, half, 0, "sio2", "buried oxide", row("m4"), layer="oxide")
    x.rect(-half, 0, half, y_sin, "sio2", "oxide between the Si and SiN levels", assumed("Si to SiN gap not stated"), layer="oxide", alpha=0.65)
    x.rect(-half, y_sin, half, y_sin + t_sin + clad, "sio2", "oxide above the SiN", assumed("cladding thickness not stated"), layer="oxide", alpha=0.35)
    w_si_mid, w_sin_mid = (w_tip + w_si) / 2, (w_sin + w_tip) / 2
    x.rect(-w_si_mid / 2, 0, w_si_mid / 2, t_si, "si", "Si, 305 nm top Si layer", row("m2") + assumed("width not stated"), layer="waveguide")
    x.rect(-w_sin_mid / 2, y_sin, w_sin_mid / 2, y_sin + t_sin, "sin", "SiN, 400 nm", row("m3") + assumed("width and gap not stated"), layer="overlay")
    x.dim("v", -box, 0, -1.6, px=-10, ext=(-1.6, -1.6), row_id="m4")
    x.note("Order from Sec. 2: SiN deposited and patterned after the Si levels, so it lies above the Si. The gap is not stated.")
    x.note("Widths drawn in this section have no source. Sidewalls drawn vertical: not stated.")
    y = c.view("core", "detail: Si and SiN levels", "xsec", like="xsec", window=(-1.5, -0.3, 1.5, 1.2))
    y.dim("v", 0, t_si, w_si_mid / 2, px=20, ext=(w_si_mid / 2, w_si_mid / 2), row_id="m2")
    y.dim("v", y_sin, y_sin + t_sin, w_sin_mid / 2, px=20, ext=(w_sin_mid / 2, w_sin_mid / 2), row_id="m3")
    y.label((-1.4, y_sin - gap / 2), "gap not stated", anchor="start")
    return c
