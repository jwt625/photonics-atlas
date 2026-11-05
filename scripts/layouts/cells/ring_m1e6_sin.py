"""OFC 2026 M1E.6 two-bus SiN microring, R 75 um, 840 x 400 nm, gap 700 nm, imec iSiPP200 (Sec. 2, Sec. 4).

Text and captions only: the layout of Fig. 2(c)-(d) is not available. Only the cross-section at the coupler is published;
the text gives the bus count, gap, radius and widths and does not fix drop and add positions, so the plan views (top, wide,
gap) are unpublished (NOT_DRAWN in build.py) and kept here only as drafts.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, assumed, circle, row, stated  # noqa: E402

ID = "cmp_ofc2026_m1e6_sin_ring_r75um"


def build() -> Cell:
    c = Cell(
        ID,
        ["Sec. 2 text", "Sec. 4 text", "text and captions only: figures not available"],
        "Coupler cross-section from the stated widths, thickness and gap; oxide stack assumed. No plan view: the layout figure is not available",
    )
    r = c.um("m4")
    w = c.um("m5")
    gap = c.um("m6")
    t = c.um("m7")
    wb = c.um("m8")
    y_bus = r + w / 2 + gap + wb / 2
    src_ring = row("m4", "m5") + stated("p.~1 Sec. 2", "ring")
    src_bus = row("m6", "m8") + stated("p.~1 Sec. 2", "2-bus design, one gap") + assumed("bus shape not stated, layout figure not available: drawn straight")

    top = c.view("top", "top view: two-bus ring at true scale")
    top.rings([circle((0, 0), r + w / 2, tol=0.002), circle((0, 0), r - w / 2, tol=0.002)], "sin", "SiN ring", src_ring, layer="waveguide")
    span = 110.0
    upper = Route((-span, y_bus), 0.0, wb)
    upper.straight(2 * span)
    lower = Route((-span, -y_bus), 0.0, wb)
    lower.straight(2 * span)
    top.route(upper, "sin", "SiN bus, input to through", src_bus, layer="waveguide")
    top.route(lower, "sin", "SiN bus, drop side", src_bus, layer="waveguide")
    top.line([(0, 0), (r * math.cos(math.radians(30)), r * math.sin(math.radians(30)))], "radius", row("m4"))
    top.label((r * 0.5 * math.cos(math.radians(30)), r * 0.5 * math.sin(math.radians(30))), "R", dy=-6, row_id="m4")
    top.label((-span, y_bus), "in, from Si-SiN transition", anchor="start", dy=-8)
    top.label((span, y_bus), "through (measured)", anchor="end", dy=-8)
    top.label((-span, -y_bus), "drop", anchor="start", dy=16)
    top.label((span, -y_bus), "add", anchor="end", dy=16)
    top.note("Text and captions only: Fig. 2(c)-(d) of the paper was not available. Input: focusing grating coupler, 450 x 220 nm Si waveguide, transition to SiN (truncated).")
    c.thumb = {"view": "xsec"}

    d = c.view("gap", "detail: bus-ring gap at the tangent point", like="top", window=(-6, r - 1.2, 6, y_bus + 1.2))
    d.dim("v", r + w / 2, r + w / 2 + gap, 0.0, px=-12, ext=(0.0, 0.0), row_id="m6")
    d.dim("v", r - w / 2, r + w / 2, 1.8, px=-12, ext=(1.8, 1.8), row_id="m5")
    d.dim("v", y_bus - wb / 2, y_bus + wb / 2, 3.6, px=-12, ext=(3.6, 3.6), row_id="m8")

    wide = c.view("wide", "detail: coupling region, buses straight (assumed)", like="top", window=(-30, r - 5, 30, y_bus + 5))
    wide.note("Separation from a straight bus grows as x^2 / 2R, 1 um at 12 um from the tangent point.")

    half, box, clad = 2.6, 3.0, 2.0
    x = c.view("xsec", "cross-section through the coupler", "xsec")
    x.rect(-half, -box - 0.6, half, -box, "si", "Si substrate", assumed("not stated: truncated"), layer="substrate", alpha=0.5)
    x.rect(-half, -box, half, 0, "sio2", "lower oxide", assumed("oxide stack of the platform not stated in this paper"), layer="oxide")
    x.rect(-half, 0, half, clad, "sio2", "top oxide", assumed("cladding not stated in this paper"), layer="oxide", alpha=0.45)
    x.rect(-gap / 2 - w, 0, -gap / 2, t, "sin", "SiN ring", row("m5", "m7"), layer="waveguide")
    x.rect(gap / 2, 0, gap / 2 + wb, t, "sin", "SiN bus", row("m8", "m7"), layer="waveguide")
    x.dim("h", -gap / 2 - w, -gap / 2, t, px=12, ext=(t, t), row_id="m5")
    x.dim("h", gap / 2, gap / 2 + wb, t, px=12, ext=(t, t), row_id="m8")
    x.dim("h", -gap / 2, gap / 2, 0, px=-14, ext=(0, 0), row_id="m6")
    x.dim("v", 0, t, gap / 2 + wb, px=10, ext=(gap / 2 + wb, gap / 2 + wb), row_id="m7")
    x.note("Si level and its transition (450 x 220 nm) are not at this plane.")

    c0 = 299792.458  # um GHz
    x.note(f"Group index implied by the FSR and radius rows: {c0 / (c.num('m1') * 2 * math.pi * r):.2f}. Not stated in the paper.")
    return c
