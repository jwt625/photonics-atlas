"""Wu 2025 SiN inverse-taper edge coupler on the Si/SiN stack of the BEOL TFLN platform (Fig. 1(a), Fig. 1(b), Fig. 1(c), Fig. 2(c), p.5-6, Methods).

Fig. 1(b) draws the SiN as a spindle at the chip edge with the Si feeding its far end. Text: from the Si side, a 35 um counter-taper
(Si 450 to 160 nm, SiN 350 nm to 1 um), then an inverse taper of the SiN from 1 um back to the 350 nm tip at the facet. The inverse
taper length is not stated. Stack from the Methods: 3 um BOX, 220 nm Si, 180 nm SiO2, 300 nm SiN, about 5 um over-cladding.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, assumed, circle, fig, row, stated  # noqa: E402

ID = "cmp_wu2025_sin_edge_coupler"


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 1(a) edge-coupler micrograph", "Fig. 1(b)", "Fig. 1(c)", "Fig. 2(c)", "p.5-6 Interlayer and fiber-to-chip coupling", "p.11-12 Methods"],
        "SiN spindle at the facet: 1 um to 350 nm inverse taper, 35 um Si-SiN counter-taper from the 450 nm Si waveguide; true Si/SiN stack",
    )
    tip = c.um("m2")
    t_sin = c.um("m3")
    w_sin = c.um("m4")
    l_vac = 35.0  # p.5
    w_si, w_si_tip = 0.45, 0.16  # p.5
    t_si = 0.22  # Methods
    t_box = 3.0  # Methods
    gap = 0.18  # Methods: SiO2 above the Si waveguides, ~180 nm
    t_over = 5.0  # Methods: about 5 um
    mfd = 7.5  # p.6, the row's condition too
    l_inv = 105.0  # not stated. Fig. 1(b) schematic: left part about 3 x the right part; not to scale
    x_vac0 = l_inv
    x_vac1 = l_inv + l_vac
    x_end = x_vac1 + 25.0

    src_inv = row("m2", "m4") + stated("p.6", "inverse taper 1 um to 350 nm") + fig("Fig. 1(b)", "spindle tip at the chip edge") + assumed("taper length not stated; 3 x the 35 um counter-taper, ratio of the Fig. 1(b) schematic")
    src_overlap = assumed("p.5 gives one 35 um length and no offset: full overlap of the two tapers, linear, is drafted")
    src_vac = row("m2", "m4") + stated("p.5", "SiN expands 350 nm to 1 um; taper length 35 um") + src_overlap
    src_si = stated("p.5", "Si taper 450 to 160 nm; taper length 35 um") + fig("Fig. 1(b)", "Si feeds the far end of the spindle") + src_overlap

    top = c.view("top", "plan: SiN spindle and Si feed, facet on the left, true scale")
    yb = 6.0
    top.rect(0, -yb, x_end, yb, "sio2", "SiO2 cladding", stated("Methods", "SiO2 over-cladding"), layer="oxide", alpha=0.25)
    # Si below: the wide end is on the far side of the spindle, the 160 nm tip under the 1 um SiN
    top.poly([(x_vac0, -w_si_tip / 2), (x_vac1, -w_si / 2), (x_end, -w_si / 2), (x_end, w_si / 2), (x_vac1, w_si / 2), (x_vac0, w_si_tip / 2)], "si", "Si waveguide, tapering under the SiN", src_si, layer="waveguide")
    top.poly([(0, -tip / 2), (x_vac0, -w_sin / 2), (x_vac0, w_sin / 2), (0, tip / 2)], "sin", "SiN inverse taper to the facet", src_inv, layer="overlay", alpha=0.85)
    top.poly([(x_vac0, -w_sin / 2), (x_vac1, -tip / 2), (x_vac1, tip / 2), (x_vac0, w_sin / 2)], "sin", "SiN end of the Si-SiN counter-taper", src_vac, layer="overlay", alpha=0.7)
    top.line([(0, -yb), (0, yb)], "chip facet", fig("Fig. 1(b)", "SiN runs to the chip edge"))
    top.dim("h", x_vac0, x_vac1, w_sin / 2, px=18, ext=(w_sin / 2, w_sin / 2), text="35 um", src=stated("p.5", "Si-SiN taper length"))
    top.label((0, yb), "facet", anchor="middle", dy=-6)
    top.label((x_end, 0), "Si 450 nm", anchor="end", dy=-10, tip="To the Si circuit; truncated")
    top.note("Same order as the Fig. 1(b) spindle: tip at the edge, widest where the Si tip ends, narrowing onto the Si.")
    top.note("Fig. 1(a) micrograph shows the coupler in a rectangular dummy-free window; it has no scale bar, so the window is not drawn.")

    a = c.view("tip", "detail: 350 nm SiN tip at the facet", like="top", window=(-2.5, -1.3, 13, 1.3))
    a.dim("v", -tip / 2, tip / 2, 0, px=-12, ext=(0, 0), row_id="m2")
    b = c.view("vac", "detail: Si-SiN counter-taper, Si tip under the 1 um SiN", like="top", window=(x_vac0 - 4, -1.5, x_vac1 + 4, 1.5))
    b.dim("v", -w_sin / 2, w_sin / 2, x_vac0 + 1.5, px=-14, ext=(x_vac0 + 1.5, x_vac0 + 1.5), row_id="m4")
    b.dim("h", x_vac0, x_vac1, -w_sin / 2, px=-18, ext=(-w_si_tip / 2, -w_si / 2), text="35 um", src=stated("p.5", "Si-SiN taper length"))
    b.label((x_vac0, 0), "Si tip 160 nm", anchor="start", dx=8, dy=-22, tip="p.5: Si taper ends at 160 nm")
    b.label((x_vac1, 0), "Si 450 nm, SiN 350 nm", anchor="end", dy=-22, tip="p.5: taper start")

    # long section at true scale
    y_si0 = 0.0
    y_si1 = t_si
    y_sin0 = y_si1 + gap
    y_sin1 = y_sin0 + t_sin
    y_top = y_sin0 + t_over
    s = c.view("section", "section along the waveguide at the counter-taper: SiN above Si, true scale", "xsec", window=(x_vac0 - 18, -t_box - 1.0, x_end, y_top + 1.0))
    s.rect(0, -t_box - 1.2, x_end, -t_box, "si", "Si substrate (truncated)", assumed("substrate thickness not stated"), layer="substrate", alpha=0.7)
    s.rect(0, -t_box, x_end, y_top, "sio2", "BOX, planarization and over-cladding SiO2", stated("Methods", "3 um BOX, ~180 nm over Si, ~5 um over-cladding"), layer="oxide", alpha=0.7)
    s.rect(x_vac0, y_si0, x_end, y_si1, "si", "Si waveguide, 220 nm; position of its tip under the SiN drafted", stated("Methods", "220 nm top Si") + src_si, layer="waveguide")
    s.rect(0, y_sin0, x_vac1, y_sin1, "sin", "SiN, 300 nm", row("m3") + fig("Fig. 1(c)", "SiN level above the Si level"), layer="overlay")
    s.line([(0, -t_box - 1.2), (0, y_top)], "chip facet", fig("Fig. 1(b)"))
    s.dim("h", x_vac0, x_vac1, y_sin1, px=16, ext=(y_sin1, y_sin1), text="35 um", src=stated("p.5", "Si-SiN taper"))
    s.dim("v", -t_box, 0, x_end, px=8, ext=(x_end, x_end), text="3 um", src=stated("Methods", "BOX"))
    s.dim("v", y_sin0, y_top, x_end, px=8, ext=(x_end, x_end), text="~5 um", src=stated("Methods", "over-cladding, about 5 um"))
    s.label((x_end - 14, y_top - 1.4), "SiO2 over-cladding", anchor="middle")
    s.label((x_vac0 - 9, -1.5), "BOX", anchor="middle")
    s.label((x_vac0 - 9, y_sin1), "SiN", anchor="middle", dy=-6)
    s.label((x_end - 12, y_si0), "Si", anchor="middle", dy=12)
    s.note("The SiO2 thickness is stated for the modulation regions; the same layers run to the facet (Fig. 2(c)). Facet treatment (polished or etched, trench) not stated.")

    e = c.view("edge", "section at the facet: SiN only, no Si under it", "xsec", like="section", window=(-5, -t_box - 1.0, 30, y_top + 0.8))
    e.dim("v", y_sin0, y_sin1, 28, px=-6, ext=(28, 28), row_id="m3")
    e.label((0, y_top), "facet", anchor="middle", dy=-6)
    d = c.view("levels", "detail: vertical levels at the Si tip", "xsec", like="section", window=(x_vac0 - 2.5, -0.35, x_vac0 + 4.5, y_sin1 + 0.45))
    d.dim("v", y_si0, y_si1, x_vac0 + 3.5, px=8, ext=(x_vac0 + 3.5, x_vac0 + 3.5), text="220 nm", src=stated("Methods", "top Si"))
    d.dim("v", y_si1, y_sin0, x_vac0 + 3.5, px=8, ext=(x_vac0 + 3.5, x_vac0 + 3.5), text="~180 nm", src=stated("Methods", "SiO2 on the Si waveguides"))
    d.dim("v", y_sin0, y_sin1, x_vac0 + 3.5, px=8, ext=(x_vac0 + 3.5, x_vac0 + 3.5), row_id="m3")

    def xs(vid: str, title: str, w_n: float, w_s: float, extra: list[str]) -> None:
        x = c.view(vid, title, "xsec")
        xw = 5.5
        x.rect(-xw, -t_box - 0.8, xw, -t_box, "si", "Si substrate (truncated)", assumed("substrate thickness not stated"), layer="substrate", alpha=0.7)
        x.rect(-xw, -t_box, xw, y_top, "sio2", "SiO2", stated("Methods", "3 um BOX, ~180 nm over Si, ~5 um over-cladding"), layer="oxide", alpha=0.7)
        if w_s > 0:
            x.rect(-w_s / 2, y_si0, w_s / 2, y_si1, "si", "Si waveguide, 220 nm", src_si + stated("Methods", "220 nm") + extra, layer="waveguide")
        x.rect(-w_n / 2, y_sin0, w_n / 2, y_sin1, "sin", "SiN core", row("m3", "m2", "m4") + extra, layer="overlay")
        x.dim("v", y_sin0, y_sin1, w_n / 2, px=12, ext=(w_n / 2, w_n / 2), row_id="m3")
        x.dim("v", -t_box, 0, xw, px=8, ext=(xw, xw), text="3 um", src=stated("Methods", "BOX"))
        x.dim("v", y_sin0, y_top, xw, px=8, ext=(xw, xw), text="~5 um", src=stated("Methods", "over-cladding"))

    xs("facet", "cross-section at the facet: 350 nm tip, 7.5 um fiber mode", tip, 0.0, [])
    f = c.views[-1]
    yc = (y_sin0 + y_sin1) / 2
    f.line(circle((0, yc), mfd / 2, tol=0.02) + [(mfd / 2, yc)], "fiber mode, 7.5 um MFD", stated("p.6", "single-mode fiber with 7.5 um MFD") + assumed("vertical alignment of the fiber is in no source: centred on the core"))
    f.dim("h", -tip / 2, tip / 2, y_sin1, px=18, ext=(y_sin1, y_sin1), row_id="m2")
    f.label((0, yc + mfd / 2), "7.5 um MFD", anchor="middle", dy=-5)
    f.note("At true scale: 3.4 um of oxide under the core against a 3.75 um mode radius, so with the mode centred on the core the circle reaches the substrate. No substrate undercut is stated. The circle is dashed: its vertical alignment is in no source.")
    xs("mid", "cross-section inside the counter-taper (widths drafted)", (tip + w_sin) / 2, (w_si + w_si_tip) / 2, assumed("widths at this plane are midpoints of an assumed linear, fully overlapped profile: p.5 gives only the end widths"))
    c.views[-1].note("Level order and thicknesses are stated (Methods). The widths at this plane are not: midpoints of an assumed linear profile, dashed, no labels.")

    c.thumb = {"view": "vac"}
    return c
