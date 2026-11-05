"""OFC 2026 Tu2D.3, Samsung 300-mm platform, 1D SiN grating coupler: text and captions only, images not available.

Text fixes: one 400 nm SiN layer deposited and patterned after the Si levels, on the SOI wafer with 305 nm Si and 2 um BOX; O band.
Whether the SiN GC sits in that layer is the table's reading (the text names only waveguides and edge couplers for the layer, and
does not place the GC). Period, fill, footprint, level height, straight or focusing: not stated. The teeth follow the grating
equation at assumed values and show why SiN teeth are about twice the Si period; all dashed, no dimension labels.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, assumed, row, stated  # noqa: E402

ID = "cmp_ofc2026_tu2d3_gc_1d_sin"


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
        ["text and captions only: Sec. 1", "Sec. 2 (400 nm SiN layer)", "Sec. 3 (loss, 1-dB bandwidth)", "captions of Fig. 1, Fig. 2(a); Table 1 and images not available"],
        "1D SiN GC in the 400 nm SiN layer above the Si level; stack from the text, teeth and outline drafted from the grating equation at assumed values",
    )
    t_sin = c.um("m3")
    t_si = 0.305  # Sec. 2
    t_box = 2.0  # Sec. 2
    # not in the text: drafting values
    lam, theta, ff = 1.31, 10.0, 0.5
    n_sin, n_ox = 2.0, 1.447
    n_per, w_gr, l_taper, w_wg = 18, 14.0, 60.0, 0.9
    gap = 0.3  # oxide between Si level and SiN
    t_top = 3.0
    n_avg = ff * slab_te0(n_sin, n_ox, n_ox, t_sin, lam) + (1 - ff) * n_ox  # teeth etched through the layer
    p = lam / (n_avg - math.sin(math.radians(theta)))
    tooth = ff * p
    lg = n_per * p

    no_plan = assumed("text only: period, fill, count, outline not stated; period from the grating equation at 1310 nm and 10 deg, full etch, fill 0.5, n SiN 2.0; straight teeth because the text does not say focusing")
    src_sin = stated("Sec. 2", "400 nm SiN layer") + row("m3") + no_plan

    top = c.view("top", "plan: drafted outline (dashed: no plan dimension in the text)")
    for i in range(n_per):
        xa = i * p + (p - tooth)
        top.rect(xa, -w_gr / 2, xa + tooth, w_gr / 2, "sin", f"tooth {i + 1} of {n_per}", src_sin, layer="waveguide")
    top.poly([(-l_taper, -w_wg / 2), (0, -w_gr / 2), (0, w_gr / 2), (-l_taper, w_wg / 2)], "sin", "taper", no_plan, layer="waveguide")
    top.rect(-l_taper - 12, -w_wg / 2, -l_taper, w_wg / 2, "sin", "SiN waveguide, truncated", no_plan, layer="waveguide")
    top.note("Text and captions only; images not available. The paper states 1D, SiN, loss and bandwidth; the layer is 400 nm. Everything in this plan is a drafting assumption.")
    top.note("Whether the teeth are straight or focusing is not stated: drawn straight, not a claim.")
    g = c.view("grating", "plan detail: drafted grating", like="top", window=(-4.0, -9.0, lg + 3.0, 9.0))
    g.note("Period from the grating equation at assumed 1310 nm, 10 deg, full etch, fill 0.5: order of magnitude only.")

    y_sin0 = t_si + gap
    y_sin1 = y_sin0 + t_sin
    y_top = y_sin1 + t_top
    s = c.view("section", "section along the waveguide: the layers the text states, drafted teeth", "xsec", window=(-3.5, -t_box - 1.1, lg + 3.5, y_top + 0.5))
    xa0, xb0 = -6.0, lg + 6.0
    s.rect(xa0, -t_box - 3.0, xb0, -t_box, "si", "Si substrate (truncated)", stated("Sec. 2", "SOI wafer") + assumed("thickness not stated"), layer="substrate", alpha=0.7)
    s.rect(xa0, -t_box, xb0, 0, "sio2", "buried oxide", stated("Sec. 2", "2 um"), layer="oxide")
    s.rect(xa0, 0, xb0, y_top, "sio2", "oxide above the BOX", stated("Sec. 2", "SiN deposited and patterned after the Si levels") + assumed("level height and thickness not stated"), layer="oxide", alpha=0.55)
    s.rect(xa0, y_sin0, 0, y_sin1, "sin", "SiN waveguide", row("m3") + no_plan, layer="waveguide")
    for i in range(n_per):
        xa = i * p + (p - tooth)
        s.rect(xa, y_sin0, xa + tooth, y_sin1, "sin", f"tooth {i + 1}", src_sin, layer="waveguide")
    s.dim("v", -t_box, 0, lg + 3.2, px=10, ext=(lg + 3.2, lg + 3.2), text="2 um", src=stated("Sec. 2", "BOX"))
    s.dim("v", y_sin0, y_sin1, -3.3, px=-8, ext=(0, 0), row_id="m3")
    s.note("The row has no lower-cladding value: the BOX is 2 um and the SiN sits some distance above the Si level. No Si is drawn under the SiN: not stated.")
    t = c.view("teeth", "detail: 400 nm SiN with drafted teeth", "xsec", like="section", window=(-1.2, y_sin0 - 0.4, 3.8, y_sin1 + 0.4))
    t.dim("v", y_sin0, y_sin1, -0.3, px=-8, ext=(0, 0), row_id="m3")

    c.thumb = {"view": "section", "window": [-1.5, -t_box - 0.6, 11.5, y_top - 1.2]}
    return c
