"""Song 2024: SiN strip waveguide 2.5 um wide, 400 nm LPCVD, C-band (p.3 Sec. II, Sec. III).

The paper gives one sentence for this waveguide: 2.5 um wide, propagation loss below 0.05 dB/cm. No test structure, no figure
and no method are given for it; the bend and ring cells it does show (Fig. 1, Fig. 2, Fig. 5(c), Fig. 6) are 1 um and belong to
other rows. So the top view is a straight run only, with arbitrary drawn length. The stack is in the text.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, assumed, row, stated  # noqa: E402

ID = "cmp_lit_song2024a_wg_2p5um"


def build() -> Cell:
    c = Cell(ID, ["p.3 Sec. II", "p.3 Sec. III", "Fig. 1, 2, 5(c), 6: read, 1 um structures, not this row"], "Section of the 2.5 um x 400 nm SiN waveguide in about 2.7 um under and 2.0 um top SiO2; sidewall not shown in the paper")
    w = c.um("m2")
    t = c.um("m3")
    under, over = 2.7, 2.0  # Sec. III: top and under cladding, printed approximately
    run = 40.0  # drawn length, no meaning
    half = 4.0

    top = c.view("top", "top view: straight waveguide (no test structure in the source)")
    rt = Route((0.0, 0.0), 0.0, w).straight(run)
    top.route(rt, "sin", "SiN strip, 2.5 um", row("m2") + stated("p.3 Sec. III", "2.5 um wide waveguide; length arbitrary, truncated both ends"), layer="waveguide")
    top.dim("v", -w / 2, w / 2, run, px=14, ext=(run, run), row_id="m2")
    top.note("The paper does not describe the structure that gave this value: no spiral, length or method. Length drawn is arbitrary; truncated both ends.")
    c.thumb = {"view": "xsec", "window": [-3.0, -0.8, 3.0, 1.6]}

    x = c.view("xsec", "cross-section: full stack (substrate truncated)", "xsec")
    x.rect(-half, -under - 1.2, half, -under, "si", "Si substrate", assumed("substrate thickness not stated: truncated"), layer="substrate", alpha=0.5)
    x.rect(-half, -under, half, 0, "sio2", "SiO2 under cladding", stated("p.3 Sec. III", "about 2.7 um, n about 1.44"), layer="oxide")
    x.rect(-half, 0, half, over, "sio2", "SiO2 top cladding", stated("p.3 Sec. III", "about 2.0 um; drawn from the top of the under cladding"), layer="oxide", alpha=0.45)
    x.rect(-w / 2, 0, w / 2, t, "sin", "LPCVD SiN core", row("m2", "m3"), layer="waveguide")
    x.dim("h", -w / 2, w / 2, t, px=14, ext=(t, t), row_id="m2")
    x.dim("v", 0, t, w / 2, px=18, ext=(w / 2, w / 2), row_id="m3")
    x.dim("v", -under, 0, -half + 0.8, px=0, ext=(-half + 0.8, -half + 0.8), text="~2.7 um", src=stated("p.3 Sec. III", "under cladding"))
    x.dim("v", 0, over, half - 0.8, px=0, ext=(half - 0.8, half - 0.8), text="~2.0 um", src=stated("p.3 Sec. III", "top cladding"))
    x.note("Thicknesses printed with a tilde (Sec. III). Whether top cladding counts from the core top is not stated. Sidewalls drawn vertical: no section shown.")
    x.note("Variation between wafers comes from differences in layer stack (Sec. III), so the bands are nominal.")
    return c
