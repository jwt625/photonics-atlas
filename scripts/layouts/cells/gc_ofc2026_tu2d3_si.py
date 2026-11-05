"""OFC 2026 Tu2D.3, Samsung 300-mm platform, 1D Si grating coupler: text and captions only, images not available.

Text fixes: 305 nm top Si on 2 um BOX, Si patterned in three etch steps for GCs and waveguides, O band, oxide over the Si; BEOL
liners removed and the cavity oxide-filled to help fiber coupling. Period, etch, fill, footprint, straight or focusing, fiber angle:
not stated. The teeth drawn here follow from the grating equation at assumed values, so the scale of the period is physical even
though no dimension of it is reported; all of it is dashed and none of it carries a dimension label.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, assumed, row, stated  # noqa: E402

ID = "cmp_ofc2026_tu2d3_gc_1d_si"


def slab_te0(n_core: float, n_low: float, n_top: float, t_um: float, lam_um: float) -> float:
    """TE0 effective index of a three-layer slab, by bisection on the dispersion relation."""

    def f(n: float) -> float:
        kt = 2 * math.pi / lam_um * math.sqrt(n_core**2 - n**2)
        return kt * t_um - math.atan(math.sqrt(n**2 - n_low**2) / math.sqrt(n_core**2 - n**2)) - math.atan(math.sqrt(n**2 - n_top**2) / math.sqrt(n_core**2 - n**2))

    a, b = max(n_low, n_top) + 1e-6, n_core - 1e-6
    for _ in range(80):
        m = (a + b) / 2
        if f(m) > 0:
            a = m
        else:
            b = m
    return (a + b) / 2


def build() -> Cell:
    c = Cell(
        ID,
        ["text and captions only: Sec. 1", "Sec. 2 (stack, three Si etch steps)", "Sec. 3 (loss, 1-dB bandwidth)", "captions of Fig. 1, Fig. 2(a); Table 1 and images not available"],
        "1D Si GC on 305 nm Si / 2 um BOX; stack from the text, teeth and outline drafted from the grating equation at assumed values",
    )
    t_si = c.um("m3")
    t_box = c.um("m4")
    # not in the text: drafting values
    lam, theta, ff, etch = 1.31, 10.0, 0.5, 0.15
    n_si, n_ox = 3.50, 1.447
    n_per, w_gr, l_taper, w_wg = 28, 12.0, 50.0, 0.40
    t_top = 3.0
    n_avg = ff * slab_te0(n_si, n_ox, n_ox, t_si, lam) + (1 - ff) * slab_te0(n_si, n_ox, n_ox, t_si - etch, lam)
    p = lam / (n_avg - math.sin(math.radians(theta)))
    tooth = ff * p
    lg = n_per * p

    no_plan = assumed("text only: period, fill, etch, count and outline not stated; period from the grating equation at 1310 nm and 10 deg, 150 nm etch, fill 0.5; straight teeth because the text does not say focusing")
    src_si = stated("Sec. 2", "305 nm Si, three etch steps for GCs and waveguides") + row("m3") + no_plan

    top = c.view("top", "plan: drafted outline (dashed: no plan dimension in the text)")
    top.rect(0, -w_gr / 2, lg + 1.0, w_gr / 2, "si", "etched grating area", no_plan, layer="slab", alpha=0.45)
    for i in range(n_per):
        xa = i * p + (p - tooth)
        top.rect(xa, -w_gr / 2, xa + tooth, w_gr / 2, "si", f"tooth {i + 1} of {n_per}", src_si, layer="waveguide", lod=tooth)
    top.poly([(-l_taper, -w_wg / 2), (0, -w_gr / 2), (0, w_gr / 2), (-l_taper, w_wg / 2)], "si", "taper", no_plan, layer="waveguide")
    top.rect(-l_taper - 12, -w_wg / 2, -l_taper, w_wg / 2, "si", "Si waveguide, truncated", no_plan, layer="waveguide")
    top.note("Text and captions only; images not available. The paper states 1D, Si, 305 nm, loss and bandwidth. Everything in this plan is a drafting assumption.")
    top.note("Whether the teeth are straight or focusing is not stated: drawn straight, not a claim.")
    g = c.view("grating", "plan detail: drafted grating", like="top", window=(-4.0, -8.0, lg + 3.0, 8.0))
    g.note("Period from the grating equation at assumed 1310 nm, 10 deg, fill 0.5, 150 nm etch: order of magnitude only.")

    s = c.view("section", "section along the waveguide: the stack the text states, drafted teeth", "xsec", window=(-3.5, -t_box - 1.1, lg + 3.5, t_si + t_top + 0.5))
    xa0, xb0 = -6.0, lg + 6.0
    s.rect(xa0, -t_box - 3.0, xb0, -t_box, "si", "Si substrate (truncated)", stated("Sec. 2", "SOI wafer") + assumed("thickness not stated"), layer="substrate", alpha=0.7)
    s.rect(xa0, -t_box, xb0, 0, "sio2", "buried oxide", row("m4"), layer="oxide")
    s.rect(xa0, 0, xb0, t_si + t_top, "sio2", "oxide over the Si", stated("Sec. 2", "BEOL liners removed, cavity filled with oxide") + assumed("thickness not stated; that the liner removal applies over the GC is not stated"), layer="oxide", alpha=0.55)
    s.rect(xa0, 0, 0, t_si, "si", "Si waveguide", row("m3"), layer="waveguide")
    s.rect(0, 0, xb0, t_si - etch, "si", "etched Si", src_si, layer="slab")
    for i in range(n_per):
        xa = i * p + (p - tooth)
        s.rect(xa, t_si - etch, xa + tooth, t_si, "si", f"tooth {i + 1}", src_si, layer="waveguide", lod=tooth)
    s.dim("v", -t_box, 0, lg + 3.2, px=10, ext=(lg + 3.2, lg + 3.2), row_id="m4")
    s.dim("v", 0, t_si, -3.3, px=-8, ext=(0, 0), row_id="m3")
    s.note("Stack from Sec. 2. Etch depths of the three steps are not stated: one 150 nm step drafted. Oxide thickness over the Si is not stated.")
    t = c.view("teeth", "detail: 305 nm Si with drafted teeth", "xsec", like="section", window=(-0.9, -0.3, 2.6, t_si + 0.3))
    t.dim("v", 0, t_si, -0.15, px=-8, ext=(0, 0), row_id="m3")

    c.thumb = {"view": "section", "window": [-1.5, -t_box - 0.6, 11.5, t_si + 1.8]}
    return c
