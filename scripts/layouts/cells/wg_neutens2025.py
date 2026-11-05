"""Neutens 2025: 1000 nm x 110 nm SiO2-clad Al2O3 waveguide, 532 nm set: cutback spirals of 3.7 to 12.9 cm, bend radius 150 um (Sec. IV-C, Fig. 2, Fig. 6(a)).

The layout of the 532 nm spirals is in a supplement that is not cached. The only spiral shown in the paper is Fig. 6(a), the
266 nm set, at the same wafer level. It is a rounded-rectangle double spiral with a central S, and on the 1100 nm panel
(embedded image, 200 um bar = 80 px, 2.5 um/px) every arm can be followed: from the entry at the lower left up and around
clockwise at 100 um per turn, through the S at the centre, and out counter-clockwise between the inbound turns to an exit
beside the entry. Arm pitch 20 px = 50 um; top levels 456, 476, 496, 516, 536 px, bottom 676, 696, 716, 738 px, left 30, 47, 67,
87, 107 px, right 907, 927, 947, 967 px; inner opening 140 px = 350 um high; the S is two quarter arcs joined by a short vertical.
That topology and pitch are carried over to the 532 nm set at its stated radius 150 um, and the straights are solved so the
drawn length is the stated 3.7 cm, the shortest of the set: same turns and same height as the figure, only the long straights
differ. Turn count and pitch for this set are assumptions.

Fig. 6(a) corners read 155 to 175 um, but the text states 300 um for the 266 nm set: reported, not used.

Those spiral views are unpublished (NOT_DRAWN in build.py): the figure is a sibling set. Published views are the sections and
depend on nothing above.

Section: Fig. 2(a) stack with the 1.06 um cladding of the text. Fig. 2(b), SEM of a 150 nm CD line (200 nm bar = 270 px):
contrast in the core puts the Al2O3 between y = 278 and 428 px, 150 px = 111 nm, 22 nm above the etched oxide surface at
y = 458 px, so the etch stops about 22 nm into the thermal oxide; the oxide hard mask left on top reaches about 193 nm above
the core. The 165 and 213 nm arrows are not at the core top and bottom: they sit about 23 px above the core top and 30 px below
the core bottom. The sidewall is therefore read directly from the outline over the core band: threshold width 238 px at y = 278
and 305 px at y = 428, so 67 px, 25 nm per side, atan(110 / 25) = 77 deg.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, assumed, fig, row, stated  # noqa: E402

ID = "cmp_lit_neutens2025_wg_w1000"


def fillet(start: tuple[float, float], heading: float, corners: list[tuple[float, float]], r: float, w: float, tol: float) -> Route:
    """Route through rectilinear corners with counter-clockwise quarter arcs of radius r."""
    rt = Route(start, heading, w, tol=tol)
    prev = start
    for k, q in enumerate(corners):
        run = abs(q[0] - prev[0]) + abs(q[1] - prev[1])
        before = r if k == 0 else 2 * r
        if run < before - 1e-9:
            raise ValueError(f"side {k} too short: {run} for radius {r}")
        rt.straight(run - before)
        rt.arc(r, 90.0)
        prev = q
    return rt


def arms(r: float, a0: float, h: float, p: float, n: int, w: float, tol: float) -> tuple[Route, Route]:
    """Both arms from the centre outward, levels as read on Fig. 6(a). Left sides: outbound a1, a3, ...; inbound a0, a2, ...

    Outbound: bottom -h, right a0, top h + p, left a1, bottom -(h + 2p), right a2, ...
    Inbound, its point reflection plus one more half turn: top h, left a0, bottom -(h + p), right a1, top h + 2p, left a2, ...
    a_k = a0 + k p. Both end heading -y on the left, the inbound arm one pitch further out, as the entry and exit in the figure.
    """
    out: list[tuple[float, float]] = [(0.0, -h)]
    y = -h
    k = 0
    for j in range(n):
        out += [(a0 + k * p, y), (a0 + k * p, h + (k + 1) * p), (-(a0 + (k + 1) * p), h + (k + 1) * p)]
        k += 2
        y = -(h + k * p)
        if j < n - 1:
            out.append((-(a0 + (k - 1) * p), y))
    inn: list[tuple[float, float]] = [(0.0, h), (-a0, h)]
    k = 0
    for _ in range(n):
        inn += [(-(a0 + k * p), -(h + (k + 1) * p)), (a0 + (k + 1) * p, -(h + (k + 1) * p)), (a0 + (k + 1) * p, h + (k + 2) * p), (-(a0 + (k + 2) * p), h + (k + 2) * p)]
        k += 2
    return fillet((0.0, 0.0), 90.0, inn, r, w, tol), fillet((0.0, 0.0), -90.0, out, r, w, tol)


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 2(a)", "Fig. 2(b)", "Sec. II", "Sec. III"],
        "Fully etched 1000 x 110 nm Al2O3 strip in 2 um and 1.06 um SiO2; sidewall, hard mask and oxide pedestal read from the SEM of a 150 nm line",
    )
    w = c.um("m2")
    r = c.um("m6")
    t = c.um("m3")
    box, clad = c.um("m4"), c.um("m5")
    target = 3.7e4  # Sec. IV-C: shortest of the 3.7, 4.5, 5.8, 12.9 cm set
    p = 50.0  # Fig. 6(a), 1100 nm panel: 20 px at 2.5 um/px
    h = 175.0  # Fig. 6(a): inner opening 350 um high
    n_turns = 2  # outbound left sides, as Fig. 6(a); not stated for the 532 nm set
    exit_margin = 150.0
    tol = 0.15

    def probe(a0: float) -> tuple[Route, Route, float]:
        inb, outb = arms(r, a0, h, p, n_turns, w, tol)
        y_end = min(min(q[1] for q in inb.pts), min(q[1] for q in outb.pts)) - exit_margin
        for rt in (inb, outb):
            if abs(rt.heading % 360.0 - 270.0) > 1e-6:
                raise ValueError(f"exit heading {rt.heading}")
            rt.straight(rt.pos[1] - y_end)
        return inb, outb, y_end

    # the length is linear in a0: solve from two probes
    a_lo, a_hi = 1000.0, 3000.0
    l_lo = sum(rt.length for rt in probe(a_lo)[:2])
    l_hi = sum(rt.length for rt in probe(a_hi)[:2])
    a0 = a_lo + (target - l_lo) * (a_hi - a_lo) / (l_hi - l_lo)
    b, a, y_end = probe(a0)
    xs = [q[0] for rt in (a, b) for q in rt.pts]
    y_t = max(q[1] for rt in (a, b) for q in rt.pts)
    y_b = -h - (2 * n_turns - 1) * p
    x_l, x_r = min(xs), max(xs)

    src = row("m2", "m6") + stated("Sec. IV-C", "3.7 cm spiral of the 532 nm set, circular bends") + fig("Fig. 6(a)", "double spiral with central S, 266 nm set, same wafer") + assumed("arm pitch 50 um and turn count carried over from Fig. 6(a); layout of this set is in the uncached supplement")
    top = c.view("top", "top view: 3.7 cm double spiral, 1000 nm wide, R = 150 um")
    top.route(b, "other", "inbound arm, Al2O3", src, layer="waveguide")
    top.route(a, "other", "outbound arm, Al2O3", src, layer="waveguide")
    top.label((a.pts[-1][0], y_end), "out", anchor="start", dx=6, dy=2)
    top.label((b.pts[-1][0], y_end), "in", anchor="end", dx=-6, dy=2)
    top.label((0.0, 0.0), "S", anchor="start", dx=8)
    top.note(f"Outer outline {(x_r - x_l) / 1000:.2f} x {(y_t - y_b) / 1000:.2f} mm follows from the assumed pitch and turn count. The 4.5, 5.8 and 12.9 cm spirals of the set (Sec. IV-C) are not drawn.")
    top.note("Access runs to the grating couplers truncated. Spirals measured on a wafer-scale fiber setup with TE grating couplers (Sec. II, III).")
    c.thumb = {"view": "edge"}

    cn = c.view("centre", "detail: central S and inner turns", like="top", window=(-420, -310, 420, 310))
    cn.dim("v", -h, h, -320, px=0, ext=(-320, -320), text="350 um, Fig. 6(a)", src=fig("Fig. 6(a)", "inner opening 140 px against the 200 um bar", "10 %"))
    cn.note("Two quarter arcs of R = 150 um joined by a 50 um vertical run, as in Fig. 6(a).")
    # top left outer corner region, where the arms run close: width visible
    x_corner = x_l
    co = c.view("arms", "detail: adjacent arms at the left side", like="top", window=(x_corner - 20, -40, x_corner + 240, 60))
    co.dim("h", x_corner + 50 - 25, x_corner + 50 + 25, 40, px=8, ext=(40, 40), text="50 um, Fig. 6(a)", src=fig("Fig. 6(a)", "arm pitch of the 266 nm set", "10 %"))
    wi = c.view("width", "detail: waveguide width", like="top", window=(x_corner - 6, 10, x_corner + 6, 14))
    wi.dim("h", x_corner - w / 2, x_corner + w / 2, 12, px=12, ext=(12, 12), row_id="m2")

    # section: core with the SEM sidewall; 1000 nm width at mid height of the core
    c.check("SEM calibration: 213 nm arrow, 290 px at 1.35 px/nm, nm", 290 / 1.35, 213.0, 0.02)
    c.check("core thickness: contrast band of Fig. 2(b), 150 px at 1.35 px/nm against the row, nm", 150 / 1.35, t * 1000, 0.05)
    dx = 0.025  # Fig. 2(b): outline over the core band, 67 px of width growth at 1.35 px/nm, per side
    top_half, foot_half = w / 2 - dx / 2, w / 2 + dx / 2
    over = 0.022  # Fig. 2(b): etch into the thermal oxide
    hm = 0.193  # Fig. 2(b): hard mask above the core on a 150 nm line, 260 px
    round_h = 0.06
    half = 3.0
    src_wall = fig("Fig. 2(b)", "sidewall read directly from the outline over the core band of a 150 nm CD line, 25 nm per side over 110 nm, applied here at mid-height width 1000 nm", "5 deg")
    x = c.view("xsec", "cross-section: full stack (substrate truncated)", "xsec")
    x.rect(-half, -box - 1.5, half, -box, "si", "Si substrate", row("m4") + assumed("substrate thickness: truncated, bare 200 mm wafer"), layer="substrate", alpha=0.5)
    x.rect(-half, -box, half, 0, "sio2", "thermal SiO2", row("m4"), layer="oxide")
    x.rect(-half, 0, half, t + clad, "sio2", "SiO2 cladding: hard mask plus HDP oxide, CMP", row("m5"), layer="oxide", alpha=0.45)
    x.poly([(-foot_half, 0), (foot_half, 0), (top_half, t), (-top_half, t)], "other", "Al2O3 core, ALD", row("m2", "m3") + src_wall, layer="waveguide")
    x.dim("h", -w / 2, w / 2, t, px=14, ext=(t, t), row_id="m2")
    x.dim("v", 0, t, w / 2, px=18, ext=(w / 2, w / 2), row_id="m3")
    x.dim("v", -box, 0, -half + 0.6, px=0, ext=(-half + 0.6, -half + 0.6), row_id="m4")
    x.dim("v", t, t + clad, half - 0.6, px=0, ext=(half - 0.6, half - 0.6), row_id="m5")
    x.note("Fully etched strip, Fig. 2(a): no slab. Sec. IV-C says rib, Fig. 2 shows strip.")
    x.note("Cladding measured from the core top, as the arrow in Fig. 2(a), which prints 1000 nm; the text gives 1.06 um.")
    x.note("Facet etch above 100 um at the chip edge (Fig. 2(a)): not in this plane.")

    d = c.view("edge", "detail: core edge as in the SEM: sidewall, hard mask, oxide foot", "xsec", window=(w / 2 - 0.33, -0.08, w / 2 + 0.17, 0.36))
    d.rect(w / 2 - 0.6, -0.3, w / 2 + 0.8, -over, "sio2", "thermal SiO2", row("m4"), layer="oxide")
    d.rect(w / 2 - 0.6, -over, w / 2 + 0.8, 0.6, "sio2", "HDP oxide fill", row("m5"), layer="oxide", alpha=0.3)
    d.poly([(w / 2 - 0.6, -over), (foot_half + 0.015, -over), (foot_half, 0), (w / 2 - 0.6, 0)], "sio2", "thermal SiO2 pedestal under the core: the etch stops about 22 nm below the core bottom", fig("Fig. 2(b)", "contrast step at the core bottom, 30 px against the 200 nm bar", "40 %"), layer="oxide")
    d.poly([(w / 2 - 0.6, t), (top_half, t), (top_half - 0.012, t + hm - round_h), (top_half - 0.05, t + hm), (w / 2 - 0.6, t + hm)], "sio2", "SiO2 hard mask left in place", stated("Sec. III", "hard mask stays as part of the cladding") + fig("Fig. 2(b)", "260 px above the core on a 150 nm line, rounded top", "30 %") + assumed("height on a 1000 nm line not shown"), layer="oxide", alpha=0.8)
    d.poly([(w / 2 - 0.6, 0), (foot_half, 0), (top_half, t), (w / 2 - 0.6, t)], "other", "Al2O3 core, 110 nm", row("m3") + src_wall, layer="waveguide")
    d.dim("v", 0, t, foot_half, px=16, ext=(foot_half, foot_half), row_id="m3")
    d.dim("h", top_half, foot_half, t, px=14, ext=(t, 0), text="25 nm", src=fig("Fig. 2(b)", "outline over the core band, 67 px of width growth per two sides"))
    d.label((w / 2 - 0.21, t + hm / 2), "oxide hard mask")
    d.label((w / 2 - 0.21, t / 2), "Al2O3")
    d.label((top_half + 0.02, t + 0.05), "wall 77 deg", anchor="start", dx=44)
    d.label((foot_half + 0.03, -over), "22 nm oxide pedestal", anchor="start", dy=12)
    d.note("Sidewall, foot and hard mask read on the 150 nm line of Fig. 2(b); the paper shows no section of the 1000 nm line.")
    return c
