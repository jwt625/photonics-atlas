"""Wu 2025: Si to SiN interlayer adiabatic coupler in the SiN edge-coupler path (p.5-6 text, p.11-12 Methods, Fig. 1(b), 1(c), 2(c)).

Bilayer of opposed tapers: the Si inverse taper narrows toward the facet while the SiN above it widens toward the facet.
Fig. 1(b) shows the SiN as a spindle at the chip edge with the Si waveguide leaving on the circuit side; Fig. 1(c) and 2(c)
show the SiN level above the Si level, overlapping it, on the facet side. The facet is on the left here, as in Fig. 1(c).
The supplement (Sec. II, the coupler characterisation) is not cached, so the overlap and taper profile are not read from a
device figure. p.5 gives one 35 um length and no offset: both tapers are drawn linear over the same 35 um, and every view
that depends on that carries it as an assumption (dashed): the plan, the long sections and the three cross-sections.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, assumed, fig, row, stated  # noqa: E402

ID = "cmp_wu2025_vac_si_sin"


def build() -> Cell:
    c = Cell(
        ID,
        ["p.5-6 Interlayer and fiber-to-chip coupling", "p.11-12 Methods Fabrication", "Fig. 1(b)", "Fig. 1(c)", "Fig. 2(c)"],
        "Opposed Si and SiN inverse tapers, SiN about 180 nm above the Si; end widths, length and stack stated, full overlap and linear profile assumed",
    )
    length = c.um("m2")
    w_si_wide, w_si_tip = c.um("m10"), c.um("m4")
    w_sin_tip, w_sin_wide = c.um("m3"), c.um("m5")
    t_si, t_sin, gap, box = c.um("m6"), c.um("m7"), c.um("m8"), c.um("m9")
    clad_top = 5.0  # p.12: overcladding about 5 um above the level that carries the SiN
    stub = 15.0  # access runs, drawn short
    y_sin = t_si + gap

    overlap = assumed("full overlap of the two tapers: p.5 gives one 35 um length and no offset")
    profile = assumed("linear taper profile: not stated")
    src_si = row("m2", "m4", "m10") + stated("p.5", "Si inverse taper") + profile
    src_sin = row("m2", "m3", "m5") + fig("Fig. 1(c)", "SiN level overlaps the Si on the facet side") + overlap + profile
    src_si_stub = row("m10") + fig("Fig. 1(b)", "Si waveguide leaves on the circuit side")
    src_sin_stub = row("m5") + fig("Fig. 1(b)", "SiN continues to the edge coupler at the chip corner") + stated("p.6", "1 um then inverse taper to 350 nm at the fiber")

    top = c.view("top", "top view: Si taper under SiN taper (facet to the left)")
    si = Route((0.0, 0.0), 0.0, w_si_tip).straight(length, w_si_wide)
    sin = Route((0.0, 0.0), 0.0, w_sin_wide).straight(length, w_sin_tip)
    top.route(si, "si", "Si inverse taper (lower layer)", src_si, layer="waveguide")
    top.route(Route((length, 0.0), 0.0, w_si_wide).straight(stub), "si", "Si access waveguide", src_si_stub, layer="waveguide")
    top.route(sin, "sin", "SiN taper (upper layer)", src_sin, layer="overlay", alpha=0.6)
    top.route(Route((-stub, 0.0), 0.0, w_sin_wide).straight(stub), "sin", "SiN waveguide toward the edge coupler", src_sin_stub, layer="overlay", alpha=0.6)
    top.dim("h", 0, length, -0.6, px=-14, ext=(-w_sin_wide / 2, -w_si_wide / 2), row_id="m2")
    top.label((-stub, 0.9), "to edge coupler", anchor="start")
    top.label((length + stub, 0.9), "to Si circuit", anchor="end")
    top.note("Access runs truncated. The SiN goes on to the edge coupler inverse taper, 1 um to 350 nm (p.6, length not stated).")
    top.note("Coupler measured through a supplement that is not cached: taper profile and overlap are drawn, not read.")
    c.thumb = {"view": "top", "window": [-5.0, -1.5, length + 5.0, 1.5]}

    d0 = c.view("tip_si", "detail: Si tip under the wide SiN end", like="top", window=(-2.0, -1.0, 4.0, 1.0))
    d0.dim("v", -w_si_tip / 2, w_si_tip / 2, 0, px=-16, ext=(0, 0), row_id="m4")
    d0.dim("v", -w_sin_wide / 2, w_sin_wide / 2, -1.6, px=-10, ext=(-1.6, -1.6), row_id="m5")
    d1 = c.view("tip_sin", "detail: SiN tip over the wide Si end", like="top", window=(length - 4.0, -1.0, length + 2.0, 1.0))
    d1.dim("v", -w_sin_tip / 2, w_sin_tip / 2, length, px=14, ext=(length, length), row_id="m3")
    d1.dim("v", -w_si_wide / 2, w_si_wide / 2, length + 1.4, px=10, ext=(length + 1.4, length + 1.4), row_id="m10")

    # long section on the axis: thicknesses at true scale, so the two tips sit one above the other at the ends of the overlap
    lg = c.view("long", "long section on the waveguide axis, overlap assumed", "xsec", window=(-stub - 2.0, -1.2, length + stub + 2.0, 2.0))
    x0, x1 = -stub - 3.0, length + stub + 3.0
    lg.rect(x0, -box, x1, 0, "sio2", "buried oxide", row("m9"), layer="oxide")
    lg.rect(x0, 0, x1, y_sin, "sio2", "planarized SiO2", row("m8", "m6"), layer="oxide", alpha=0.6)
    lg.rect(x0, y_sin, x1, y_sin + clad_top, "sio2", "SiO2 overcladding", stated("p.12", "about 5 um"), layer="oxide", alpha=0.35)
    lg.rect(0, 0, length + stub, t_si, "si", "Si layer", row("m6", "m2"), layer="waveguide")
    lg.rect(-stub, y_sin, length, y_sin + t_sin, "sin", "SiN layer", row("m7", "m8", "m2") + fig("Fig. 2(c)", "SiN above the Si, on the planarized oxide") + overlap, layer="overlay")
    lg.dim("h", 0, length, y_sin + t_sin, px=14, ext=(y_sin + t_sin, y_sin + t_sin), row_id="m2")
    lg.note("Both axes at the same scale. Tips: Si at x = 0, SiN at x = 35 um, assuming the two tapers span the same length.")
    e0 = c.view("long_si_tip", "long section: Si tip below the SiN, overlap assumed", "xsec", like="long", window=(-3.0, -0.45, 3.0, 1.15))
    e0.dim("v", 0, t_si, 2.4, px=0, ext=(2.4, 2.4), row_id="m6")
    e0.dim("v", t_si, y_sin, 0.5, px=0, ext=(0.5, 0.5), row_id="m8")
    e0.dim("v", y_sin, y_sin + t_sin, -2.0, px=0, ext=(-2.0, -2.0), row_id="m7")
    e0.label((-0.1, 0.11), "Si ends at the 160 nm tip", anchor="end")
    e1 = c.view("long_sin_tip", "long section: SiN tip above the Si, overlap assumed", "xsec", like="long", window=(length - 3.0, -0.45, length + 3.0, 1.15))
    e1.label((length + 1.5, y_sin + t_sin / 2), "SiN ends at the 350 nm tip")

    def section(vid: str, title: str, w_si: float, w_sin: float, half: float, window: tuple[float, float, float, float] | None, *, dims: bool, tip: tuple[str, str]) -> None:
        x = c.view(vid, title, "xsec", window=window)
        x.rect(-half, -box - 1.5, half, -box, "si", "Si substrate", assumed("handle thickness: truncated"), layer="substrate", alpha=0.5)
        x.rect(-half, -box, half, 0, "sio2", "buried oxide", row("m9"), layer="oxide")
        x.rect(-half, 0, half, y_sin, "sio2", "planarized SiO2", row("m8", "m6"), layer="oxide", alpha=0.6)
        x.rect(-half, y_sin, half, y_sin + clad_top, "sio2", "SiO2 overcladding", stated("p.12", "about 5 um"), layer="oxide", alpha=0.35)
        x.rect(-w_si / 2, 0, w_si / 2, t_si, "si", "Si core", row(tip[0], "m6") if tip[0] else row("m4", "m10", "m6") + profile, layer="waveguide")
        x.rect(-w_sin / 2, y_sin, w_sin / 2, y_sin + t_sin, "sin", "SiN core", (row(tip[1], "m7", "m8") if tip[1] else row("m3", "m5", "m7", "m8") + profile) + overlap, layer="overlay")
        if tip[0]:
            x.dim("h", -w_si / 2, w_si / 2, 0, px=-14, ext=(0, 0), row_id=tip[0])
        if tip[1]:
            x.dim("h", -w_sin / 2, w_sin / 2, y_sin + t_sin, px=14, ext=(y_sin + t_sin, y_sin + t_sin), row_id=tip[1])
        if dims:
            xr = max(w_si, w_sin) / 2 + 0.05
            x.dim("v", 0, t_si, xr, px=14, ext=(w_si / 2, w_si / 2), row_id="m6")
            x.dim("v", t_si, y_sin, xr, px=14, ext=(w_si / 2, w_si / 2), row_id="m8")
            x.dim("v", y_sin, y_sin + t_sin, xr, px=14, ext=(w_sin / 2, w_sin / 2), row_id="m7")
        x.note("Pairing these two widths at one plane assumes full overlap. Sidewalls drawn vertical: not stated.")

    w_mid_si, w_mid_sin = (w_si_tip + w_si_wide) / 2, (w_sin_tip + w_sin_wide) / 2
    section("xsec", "cross-section at mid taper: full stack (substrate truncated)", w_mid_si, w_mid_sin, 4.0, None, dims=False, tip=("", ""))
    section("xsec_si_tip", "cross-section at the Si tip (x = 0)", w_si_tip, w_sin_wide, 4.0, (-1.0, -0.25, 1.0, 1.05), dims=True, tip=("m4", "m5"))
    section("xsec_sin_tip", "cross-section at the SiN tip (x = 35 um)", w_si_wide, w_sin_tip, 4.0, (-1.0, -0.25, 1.0, 1.05), dims=True, tip=("m10", "m3"))
    return c
