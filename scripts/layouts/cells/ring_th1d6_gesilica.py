"""OFC 2026 Th1D.6 Ge:silica reflowed microring, 1.5 mm diameter, 10 um thick core (text and captions only).

No on-chip bus: the text couples light with a U-shaped fiber taper. Fig. 2(a) (micrograph) and Fig. 1(d) (SEM of a reflowed
waveguide) are not available. Width of the reported resonator is not stated (range 3-30 um): assumed. Reflow reshapes the
ridge towards a near-circular profile; the drawn profile conserves the ridge area.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, arc, assumed, circle, row, stated  # noqa: E402

ID = "cmp_ofc2026_th1d6_gesilica_ring_d1p5mm"


def build() -> Cell:
    c = Cell(
        ID,
        ["p.~2 text", "Fig. 1 caption", "Fig. 2 caption", "text and captions only: figures not available"],
        "Ring only, no on-chip bus: U-shaped fiber taper at the rim. Width and reflowed profile assumed",
    )
    r = c.um("m7")
    t = c.um("m8")
    w = 10.0  # not stated, within the stated 3-30 um: drafting value, never labelled
    d_fib = 1.0  # not stated: drafting value
    # reflowed profile: circular arc on the oxide, area equal to the as-etched ridge; sets the drawn width in top too
    h_over_r = 0.7
    area = w * t
    rho = math.sqrt(area / (math.pi - (math.acos(h_over_r) - h_over_r * math.sqrt(1 - h_over_r**2))))
    h = h_over_r * rho
    src_ring = row("m7") + assumed("waveguide width of this resonator not stated, range 3-30 um; drawn as the reflowed width of a 10 um ridge")
    src_fib = assumed("taper position, waist and routing not stated; the text says a U-shaped fiber taper: off-chip, drawn at the outer rim in both views")

    top = c.view("top", "top view: ring with no bus; fiber taper off-chip")
    top.rings([circle((0, 0), r + rho, tol=0.02), circle((0, 0), r - rho, tol=0.02)], "other", "Ge:silica ring", src_ring, layer="waveguide")
    y_fib = r + rho + d_fib / 2
    fib = Route((-420.0, y_fib), 0.0, d_fib)
    fib.straight(840.0)
    top.route(fib, "glass", "U-shaped fiber taper, waist", src_fib, layer="overlay")
    top.line([(0, 0), (r * math.cos(math.radians(-140)), r * math.sin(math.radians(-140)))], "radius", row("m7"))
    top.label((r * 0.5 * math.cos(math.radians(-140)), r * 0.5 * math.sin(math.radians(-140))), "R", anchor="end", dx=-6, row_id="m7")
    top.label((0, y_fib), "U-shaped fiber taper, not on the chip", dy=-10)
    top.note("Text and captions only: the micrograph of Fig. 2(a) was not available. No bus waveguide exists on the chip for this measurement. Waist and position of the taper are not stated.")
    top.note("Ring width of the reported resonator not stated (range 3-30 um). Drawn dashed as the reflowed width of a 10 um ridge, no value implied. The fiber is at the outer rim in the top view and the cross-section.")
    c.thumb = {"view": "top"}

    half = 22.0
    box = 15.0
    a0 = math.degrees(math.asin(-h_over_r))
    x = c.view("xsec", "cross-section: reflowed Ge:silica ridge on thermal oxide", "xsec")
    x.rect(-half, -box - 4.0, half, -box, "si", "Si wafer", assumed("not stated: truncated"), layer="substrate", alpha=0.5)
    x.rect(-half, -box, half, 0, "sio2", "thermal SiO2", stated("p.~1 text", "8-15 um") + assumed("drawn at 15 um; the value of this device is not given"), layer="oxide")
    x.poly(arc((0, h), rho, a0, 180 - a0, tol=0.01), "other", "reflowed Ge:silica core", row("m8") + assumed("width not stated, profile shape read from text only: near-circular, area of the ridge conserved"), layer="waveguide")
    x.line([(-w / 2, 0), (-w / 2, t), (w / 2, t), (w / 2, 0)], "as-etched ridge before reflow", row("m8") + assumed("width not stated; drawn at 10 um"))
    x.poly(circle((rho + d_fib / 2, h), d_fib / 2, tol=0.01), "glass", "fiber taper waist", src_fib, layer="overlay")
    x.dim("v", 0, t, half, px=8, ext=(w / 2, half), row_id="m8")
    x.dim("v", -box, 0, half, px=8, ext=(half, half), text="8-15 um", src=stated("p.~1 text", "thermal SiO2"))
    x.note("No upper cladding stated; evanescent fiber-taper coupling needs an exposed rim, so none is drawn. Stated core thickness is that of the film before reflow.")

    # alpha = 2 pi ng / (lambda Qi): group index implied by the 0.07 dB/m and 566 M rows against the core index
    alpha_per_um = c.num("m6") / 4.343 * 1e-4
    c.check("rows only, nothing drawn: group index implied by the loss and Q rows at 1064 nm against about 1.5 (Delta n 4 % on silica)", alpha_per_um * 1.064 * c.num("m4") / (2 * math.pi), 1.5, 0.05)
    return c
