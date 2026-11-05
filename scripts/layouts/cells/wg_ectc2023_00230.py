"""Sirbu 2023 (ECTC): Si rib waveguide of the CEA-Leti platform: 300 nm SOI, 160 nm slab, 2 um BOX (Sec. III.A, Fig. 4).

Fig. 4 shows the rib as a stepped block among the Si waveguides, with oxide all round and the TiN heater directly over it
(page render, 5x crop: heater x 471-716, slab 405-733, rib 503-638 px); the SiN sits over another device, the strip at the right.
Sec. III.A places TiN 600 nm above the Si waveguides. Heater width and thickness are not stated, its width is drawn at the
figure's ratio and it is dashed. Whether the loss test waveguide carries a heater is not stated.
The figure is a simplified schematic and is not to scale: against 63 px for the 300 nm Si, the BOX reads 103 px, so 490 nm rather
than 2 um, and the heater sits 340 nm above the rib rather than 600 nm. No width in it can be taken as a dimension. The waveguide
width is not stated; rib and slab widths are drawn at the figure's ratios and marked assumed.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, assumed, fig, row, stated  # noqa: E402

ID = "cmp_ectc51909_2023_00230_rib_waveguide"


def build() -> Cell:
    c = Cell(ID, ["Fig. 4", "p.2-3 Sec. III.A"], "Si rib section, 300 nm with a 160 nm slab on 2 um BOX; rib and slab widths assumed; TiN heater of Fig. 4 dashed, 600 nm above the Si")
    t = c.um("m4")
    slab = c.um("m3")
    box = c.um("m5")
    px = t / 63.0  # Fig. 4, 2.8x crop: Si height 63 px
    w_rib = 77.0 * px  # 77 px in Fig. 4
    w_slab = 184.0 * px  # 184 px in Fig. 4
    clad = 3.0  # oxide above: not stated
    run = 8.0
    half = 2.0
    h_gap = 0.6  # Sec. III.A: TiN 600 nm above the Si waveguides
    w_heat = 245.0 / 112.0 * t  # Fig. 4, 5x crop: heater 245 px, Si 112 px
    t_heat = 37.0 / 112.0 * t  # same crop: 37 px

    src_w = fig("Fig. 4", "width ratio to the Si thickness; simplified schematic, not to scale", "50 %") + assumed("waveguide width not stated; drawn at the figure's ratio")
    top = c.view("top", "top view: straight rib on its slab (widths assumed)")
    top.rect(0, -w_slab / 2, run, w_slab / 2, "si", "Si slab, 160 nm", row("m3") + src_w, layer="slab", alpha=0.55)
    top.rect(0, -w_rib / 2, run, w_rib / 2, "si", "Si rib, 300 nm", row("m4") + src_w, layer="waveguide")
    top.label((run / 2, w_rib / 2), "rib", dy=-6)
    top.label((run / 2, w_slab / 2), "slab", dy=-6)
    top.note("Length arbitrary, truncated both ends. The paper describes no test structure: median of at least 10 dies from a semi-automatic wafer probe station (Sec. III.A).")
    c.thumb = {"view": "xsec", "window": [-1.8, -0.2, 1.8, 1.1]}

    x = c.view("xsec", "cross-section: rib in the platform stack (substrate truncated)", "xsec")
    x.rect(-half, -box - 1.0, half, -box, "si", "Si substrate", assumed("substrate truncated; 725 um wafer, thinned to 100 um where TSVs are post-processed, Sec. II.B"), layer="substrate", alpha=0.5)
    x.rect(-half, -box, half, 0, "sio2", "buried oxide", row("m5"), layer="oxide")
    x.rect(-half, 0, half, t + clad, "sio2", "oxide encapsulation", fig("Fig. 4", "oxide all round the Si waveguides") + assumed("thickness above the Si not stated"), layer="oxide", alpha=0.45)
    x.poly([(-w_slab / 2, 0), (w_slab / 2, 0), (w_slab / 2, slab), (w_rib / 2, slab), (w_rib / 2, t), (-w_rib / 2, t), (-w_rib / 2, slab), (-w_slab / 2, slab)], "si", "Si rib and slab", row("m3", "m4") + src_w, layer="waveguide")
    x.dim("v", -box, 0, -half + 0.5, px=0, ext=(-half + 0.5, -half + 0.5), row_id="m5")
    x.note("Sidewalls drawn vertical: not stated. Smoothing anneal after waveguide patterning (Sec. III.A) rounds corners by an amount not stated.")
    x.rect(-w_heat / 2, t + h_gap, w_heat / 2, t + h_gap + t_heat, "metal", "TiN heater over the rib", stated("Sec. III.A", "TiN 600 nm above the Si waveguides") + fig("Fig. 4", "directly over this rib; width and thickness by ratio, not to scale", "50 %") + assumed("heater width and thickness not stated; whether the loss test waveguide carries one is not stated"), layer="metal")
    x.note("Fig. 4 has the TiN heater directly over this rib, contacted by two vias (not drawn, heights not stated). The SiN, 600 nm thick (Sec. III.A), sits over another device there.")
    y = c.view("rib", "detail: rib, etch depth 140 nm, heater above", "xsec", like="xsec", window=(-0.8, -0.2, 0.8, 1.15))
    y.label((0.0, t), "rib width not in the source", dy=-10)
    y.dim("v", t, t + h_gap, w_heat / 2, px=14, ext=(w_rib / 2, w_heat / 2), text="600 nm", src=stated("Sec. III.A", "TiN above the Si waveguides"))
    y.label((0.0, t + h_gap + t_heat), "TiN heater, dashed: size not stated", dy=-6)
    y.dim("v", slab, t, -w_rib / 2, px=-20, ext=(-w_rib / 2, -w_rib / 2), text="140 nm", src=stated("Sec. III.A", "300 nm Si, 160 nm slab"))
    y.dim("v", 0, slab, w_slab / 2, px=16, ext=(w_slab / 2, w_slab / 2), row_id="m3")
    y.dim("v", 0, t, -w_slab / 2, px=-16, ext=(-w_slab / 2, -w_rib / 2), row_id="m4")
    return c
