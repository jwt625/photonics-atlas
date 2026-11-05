"""Luke 2020 x-cut TFLN micro-ring, R 80 um, 2.0 um wide, 400 nm etch (Sec. II, Sec. III, Fig. 2(h), Fig. 4(a)).

The paper has no layout figure: Fig. 1 is wafer photographs and a sidewall SEM, Fig. 2 the process, Fig. 4 spectra. The ring
radius, width and stack are stated. One grating-coupled bus is implied (transmission dips, a single coupling gap in Sec.
III); bus shape, width and gap are not stated: assumed, dashed. FSR read off Fig. 4(a) closes the circumference.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, assumed, circle, fig, row, stated  # noqa: E402

ID = "cmp_lit_luke2020_ring_r80_w2_etch400"


def build() -> Cell:
    c = Cell(
        ID,
        ["Sec. II", "Sec. III", "Fig. 2(h)", "Fig. 4(a)", "no layout figure in the paper"],
        "Ring from stated R and width, single bus assumed (no layout figure); rib stack from the stated film, etch and cladding",
    )
    r = c.um("m3")
    w = c.um("m4")
    t = c.um("m6")
    slab = c.um("m7")
    box = c.um("m8")
    clad = c.um("m9")
    gap = 1.0  # not stated: drafting value, never labelled
    wb = w  # not stated: same as the ring
    y_bus = r + w / 2 + gap + wb / 2

    src_ring = row("m3", "m4") + stated("p.3 Sec. III", "micro-ring")
    src_bus = assumed("no layout figure: single straight bus, width and gap not stated; the text says the rings are grating-coupled and measured in transmission")

    top = c.view("top", "top view: R 80 um ring, 2 um wide; bus assumed")
    top.rings([circle((0, 0), r + w / 2, tol=0.005), circle((0, 0), r - w / 2, tol=0.005)], "ln", "LN ring rib", src_ring, layer="waveguide")
    bus = Route((-130.0, y_bus), 0.0, wb)
    bus.straight(260.0)
    top.route(bus, "ln", "bus rib", src_bus, layer="waveguide")
    top.line([(0, 0), (r * math.cos(math.radians(-40)), r * math.sin(math.radians(-40)))], "radius", row("m3"))
    top.label((r * 0.5 * math.cos(math.radians(-40)), r * 0.5 * math.sin(math.radians(-40))), "R", anchor="start", dy=-6, row_id="m3")
    top.label((-130.0, y_bus), "to grating coupler", anchor="start", dy=-8)
    top.label((130.0, y_bus), "to grating coupler", anchor="end", dy=-8)
    top.note("Text only for the layout: the paper shows no drawing or micrograph of this ring. Dashed bus and gap are a drafting assumption.")
    top.note("The 200 nm LN slab covers the whole wafer and is shown in the cross-section only. Grating couplers truncated.")
    c.thumb = {"view": "top", "window": [-120, -86, 120, 90]}

    half = 6.0
    x = c.view("xsec", "cross-section through the coupler: rib in x-cut LN, Fig. 2(h)", "xsec")
    x.rect(-half, -box - 1.0, half, -box, "si", "Si handle (500 um, truncated)", stated("p.2 Sec. II", "500 um Si handle"), layer="substrate", alpha=0.5)
    x.rect(-half, -box, half, 0, "sio2", "thermal SiO2", row("m8"), layer="oxide")
    x.rect(-half, slab, half, slab + clad, "sio2", "PECVD SiO2", row("m9") + fig("Fig. 2(h)", "flat top on the schematic"), layer="oxide", alpha=0.45)
    x.rect(-half, 0, half, slab, "ln", "LN slab", row("m7"), layer="slab")
    x.rect(-w / 2, slab, w / 2, t, "ln", "LN ring rib", row("m4", "m5", "m6"), layer="waveguide")
    x.rect(w / 2 + gap, slab, w / 2 + gap + wb, t, "ln", "LN bus rib", assumed("bus width and gap not stated"), layer="waveguide")
    x.dim("h", -w / 2, w / 2, t, px=14, ext=(t, t), row_id="m4")
    x.dim("v", slab, t, -w / 2, px=-10, ext=(-w / 2, -w / 2), row_id="m5")
    x.dim("v", 0, slab, -half, px=-10, ext=(-half, -half), row_id="m7")
    x.dim("v", -box, 0, half, px=10, ext=(half, half), row_id="m8")
    x.dim("v", slab, slab + clad, half, px=10, ext=(half, half), row_id="m9")
    x.dim("v", 0, t, -half, px=-54, ext=(-half, -w / 2), row_id="m6")

    # closure: Fig. 4(a) main family at 1591.2, 1593.4, 1595.7, 1597.9 nm (axis ticks 51.75 px/nm, 342 px over three periods)
    fsr_nm = 342 / 3 / 51.75
    lam = 1.595
    ng_fsr = lam**2 / (fsr_nm * 1e-3 * 2 * math.pi * r)
    alpha_per_um = c.num("m2") / 4.343 * 1e-4
    ng_q = alpha_per_um * lam * c.num("m1") / (2 * math.pi)
    c.check("group index from the FSR of Fig. 4(a), assuming that typical ring is this R 80 um device, against the Qi and loss rows", ng_fsr, ng_q, 0.05)
    top.note(f"Assumption in the closure: Fig. 4(a) is captioned only as a typical grating-coupled ring. Taken as this R 80 um device, its FSR {fsr_nm:.2f} nm gives group index {ng_fsr:.2f}, against {ng_q:.2f} from the Qi and loss rows.")
    return c
