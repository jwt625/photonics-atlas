"""Feng 2022 2x2 MMI that over-couples a racetrack to one MZI arm, x-cut LN rib (Fig. 1(a), Fig. 2(c), Fig. 2(d), Methods).

Topology from Fig. 1(a) and the SEM of Fig. 2(c): the MMI lies in one straight lane of the racetrack, the MZI arm in the
other. Bus enters one lane; the racetrack leaves from the other lane and returns to it (the crossed path carries 92 %).
Port outer edges are flush with the MMI walls (no shoulder in Fig. 2(c), (d)), so the port offset follows from W and the
port width. The tapers keep their axes parallel to the MMI axis; only a narrow slot separates the ports.

Scale of the racetrack is a conflict in the source, so the racetrack is dashed and carries no dimension: Fig. 1(a) by its
printed 50 um bar (90 px) reads 239 x 69 um, while the stated FSR (50 GHz, about 0.4 nm) needs a round trip about four times
longer. Aspect ratio is from Fig. 1(a); scale solved from the FSR with the group index of the paper's own MZI.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Pt, Route, View, assumed, fig, rect, row, turn  # noqa: E402

ID = "cmp_feng2022_mmi_2x2"


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 1(a)", "Fig. 1(a) inset", "Fig. 2(c) SEM", "Fig. 2(d)", "Methods p.9", "Results p.4-6"],
        "2x2 MMI in the racetrack: MMI, parallel-axis tapers with outer edges flush to the walls, racetrack and MZI arm dashed (aspect from Fig. 1(a), scale from the stated FSR, in conflict with the printed bar)",
    )
    lm = c.um("m3")
    w = c.um("m4")
    wp = c.um("m5")
    lt = c.um("m6")
    wa = c.um("m7")
    t = c.um("m10")
    slab = c.um("m12")
    clad = c.um("m13")
    cc = w - wp  # port centre to centre: outer edges flush with the walls, Fig. 2(c), (d)
    gap_p = cc - wp  # slot between the wide ends

    # racetrack: stated FSR, group index from the stated MZI
    c_um_ghz = 299792.458  # c in um GHz
    lam, fsr_ghz, dl, fsr_mzi = 1.59, 50.0, 50.0, 0.020  # um, GHz, um, um: p.4, p.9
    ng = lam**2 / (fsr_mzi * dl)
    l_rt = c_um_ghz / (ng * fsr_ghz)
    # Fig. 1(a) readings, in pixels of a 3x crop: R 107, height 375, width 1290, used only as ratios
    k = l_rt / (2 * (1290 - 2 * 107) + 2 * math.pi * 107 + 2 * (375 - 2 * 107))
    r_bend, s_long, v_side = 107 * k, (1290 - 2 * 107) * k, (375 - 2 * 107) * k
    s_stub = (v_side - lm - 2 * lt) / 2

    src_mmi = row("m3", "m4") + fig("Fig. 2(c)", "rectangular core, walls continuous with the port outer edges")
    src_port = row("m5", "m6", "m7", "m4") + fig("Fig. 2(c), Fig. 2(d)", "outer edges flush with the walls; taper axes parallel, port centre shift under 5 % of the width")
    src_rt = row("m7") + fig("Fig. 1(a)", "racetrack topology and aspect ratio", "5 %") + assumed("absolute scale: solved from the stated FSR 50 GHz with ng from the stated MZI; the printed 50 um bar gives about four times less")
    src_bus = row("m7") + fig("Fig. 1(a)", "bus routing, by ratio to the racetrack", "10 %") + assumed("absolute scale as for the racetrack")

    def mmi_parts() -> list[tuple[list[Pt], str]]:
        """MMI and four tapers in the flow frame of Fig. 2(c): x along the flow, +y the racetrack lane."""
        out: list[tuple[list[Pt], str]] = [(rect(-lm / 2, -w / 2, lm / 2, w / 2), "core")]
        for sy in (1, -1):
            for sx in (1, -1):
                y0 = sy * cc / 2
                x0, x1 = sx * lm / 2, sx * (lm / 2 + lt)
                out.append(([(x0, y0 - wp / 2), (x1, y0 - wa / 2), (x1, y0 + wa / 2), (x0, y0 + wp / 2)], "taper"))
        return out

    def add_mmi(v: View, rotate: bool) -> None:
        for pts, kind in mmi_parts():
            p = turn(pts, -90.0) if rotate else pts
            if kind == "core":
                v.poly(p, "ln", "2x2 MMI core", src_mmi, layer="waveguide")
            else:
                v.poly(p, "ln", "port taper", src_port, layer="waveguide")

    # top: orientation of Fig. 1(a), flow down the page, racetrack to the right of the MMI
    top = c.view("top", "top view: MMI in the racetrack, orientation of Fig. 1(a); racetrack scale assumed")
    add_mmi(top, True)
    ring = Route((cc / 2, lm / 2 + lt), 90.0, wa, tol=0.02)
    ring.straight(s_stub).arc(r_bend, -90.0).straight(s_long).arc(r_bend, -90.0).straight(v_side).arc(r_bend, -90.0).straight(s_long).arc(r_bend, -90.0).straight(s_stub)
    top.route(ring, "ln", "racetrack", src_rt, layer="waveguide")
    arm_in = Route((-cc / 2, lm / 2 + lt), 90.0, wa, tol=0.02)
    arm_in.straight(v_side + r_bend)
    top.route(arm_in, "ln", "MZI arm, input side", src_bus, layer="waveguide")
    arm_out = Route((-cc / 2, -lm / 2 - lt), -90.0, wa, tol=0.02)
    r_bus = 110 * k
    arm_out.straight(240 * k - lm / 2 - lt).arc(r_bus, 90.0).straight(1150 * k)
    top.route(arm_out, "ln", "MZI arm, output side", src_bus, layer="waveguide")

    top.label(arm_in.pos, "MZI arm from the input splitter", anchor="start", dx=6, dy=8)
    top.label(arm_out.pos, "to the output combiner", anchor="end", dy=-8)
    y_top = ring.pts[0][1] + s_stub + r_bend
    x_right = cc / 2 + 2 * r_bend + s_long
    top.label((s_long / 2 + r_bend, y_top), "racetrack: scale assumed, see the note", dy=-8)
    bar_um_px = 50.0 / 270.0  # Fig. 1(a): 50 um bar is 90 px, the pixel readings above are of a 3x crop
    rt_bar = l_rt / k * bar_um_px
    fsr_bar = c_um_ghz / (ng * rt_bar)
    top.note(f"Source conflict. Printed bar of Fig. 1(a), 50 um = 90 px: racetrack {1290 * bar_um_px:.0f} x {375 * bar_um_px:.0f} um, round trip {rt_bar / 1e3:.2f} mm, bends {107 * bar_um_px:.0f} um, FSR about {fsr_bar:.0f} GHz. Stated FSR: {fsr_ghz:.0f} GHz, about 0.4 nm, round trip about {l_rt / 1e3:.1f} mm with ng {ng:.2f} from the stated MZI (50 um, 20 nm).")
    top.note(f"The racetrack and MZI arm are dashed: aspect ratio from Fig. 1(a), scale solved from the stated FSR, {l_rt / rt_bar:.1f} times the printed bar. A computed drawing, not a figure reading: no dimension is given. MMI and tapers are from the rows.")
    top.note("Second MZI arm, Y-junctions, RF electrodes along the straights and the facets are not part of this component and are not drawn.")
    c.thumb = {"view": "top", "window": [-15, -y_top - 12, x_right + 10, y_top + 12]}

    west = c.view("west", "detail: MMI at the end of the racetrack", like="top", window=(-110, -190, 200, 190))
    west.label((-1, 0), "2x2 MMI", anchor="end", dx=-8)
    west.note("Dashed racetrack and arm: scale assumed, see the note on the top view.")

    # orientation of the SEM of Fig. 2(c): flow to the right, racetrack lane up
    d = c.view("mmi", "detail: MMI at true scale, orientation of Fig. 2(c), flow to the right")
    add_mmi(d, False)
    stub = 6.0
    for sy, name in ((1, "racetrack lane"), (-1, "bus lane")):
        for sx in (1, -1):
            d.rect(min(sx * (lm / 2 + lt), sx * (lm / 2 + lt + stub)), sy * cc / 2 - wa / 2, max(sx * (lm / 2 + lt), sx * (lm / 2 + lt + stub)), sy * cc / 2 + wa / 2, "ln", name, row("m7") + fig("Fig. 2(c)", "lanes stay parallel across the frame"), layer="waveguide")
    xe = lm / 2 + lt + stub
    d.label((-xe, cc / 2), "from racetrack", anchor="start", dy=-8)
    d.label((-xe, -cc / 2), "bus in", anchor="start", dy=16)
    d.label((xe, cc / 2), "to racetrack", anchor="end", dy=-8)
    d.label((xe, -cc / 2), "bus out", anchor="end", dy=46)
    d.dim("h", -lm / 2, lm / 2, w / 2, px=14, ext=(w / 2, w / 2), row_id="m3")
    d.dim("h", lm / 2, lm / 2 + lt, -cc / 2 - wa / 2, px=-16, ext=(-cc / 2 - wp / 2, -cc / 2 - wa / 2), row_id="m6")
    d.dim("v", -w / 2, w / 2, 0.0, px=-10, ext=(0.0, 0.0), row_id="m4")
    d.note("Fig. 2(c) by its 10 um bar reads about 25.6 x 6.3 um with port centres 3.5 um apart; the Methods give 31.4 x 4.8 um. The rows are drawn. Topology (flush walls, narrow slot, parallel lanes) is from the SEM.")

    ports = c.view("ports", "detail: slot between the wide ends", like="mmi", window=(lm / 2 - 2, -3.3, lm / 2 + 7, 3.3))
    ports.dim("v", cc / 2 - wp / 2, cc / 2 + wp / 2, lm / 2 + 0.3, px=-14, ext=(lm / 2 + 0.3, lm / 2 + 0.3), row_id="m5")
    ports.dim("v", -gap_p / 2, gap_p / 2, lm / 2 + 2.0, px=-18, ext=(lm / 2, lm / 2 + 2.0), text=f"{gap_p:.2f} um", src=row("m4", "m5") + fig("Fig. 2(c)", "port outer edges flush with the walls: W - 2 x port width", "0.2 um"))

    box = 2.0

    def stack(vid: str, title: str, half: float, ribs: list[tuple[float, float]], role: str, src: list[str]) -> View:
        v = c.view(vid, title, "xsec")
        v.rect(-half, -box - 0.6, half, -box, "si", "Si substrate", assumed("thickness not stated: truncated"), layer="substrate", alpha=0.5)
        v.rect(-half, -box, half, 0, "sio2", "buried oxide", assumed("buried oxide thickness not stated"), layer="oxide")
        # cladding follows the rib, as in the Fig. 1(a) inset
        x0, x1 = ribs[0][0], ribs[-1][1]
        v.poly([(-half, slab), (half, slab), (half, slab + clad), (x1 + 0.3, slab + clad), (x1, t + clad), (x0, t + clad), (x0 - 0.3, slab + clad), (-half, slab + clad)], "sio2", "PECVD SiO2", row("m13") + fig("Fig. 1(a) inset", "follows the rib"), layer="oxide", alpha=0.45)
        v.rect(-half, 0, half, slab, "ln", "LN slab", row("m12"), layer="slab")
        for a, b in ribs:
            v.rect(a, slab, b, t, "ln", role, src, layer="waveguide")
        return v

    x = stack("xsec", "cross-section: multimode region", 4.0, [(-w / 2, w / 2)], "LN rib", row("m4", "m10", "m11"))
    x.dim("h", -w / 2, w / 2, t, px=44, ext=(t, t), row_id="m4")
    x.dim("v", slab, t, w / 2, px=10, ext=(w / 2, w / 2), row_id="m11")
    x.dim("v", 0, slab, -w / 2, px=-10, ext=(-w / 2, -w / 2), row_id="m12")
    x.dim("v", t, t + clad, 3.2, px=10, ext=(w / 2, 3.2), row_id="m13")
    x.note("Rib drawn with vertical sidewalls: the Fig. 1(a) inset shows a slope, the angle is not stated.")

    y = stack("xports", "cross-section: two ports at the wide end", 4.0, [(-cc / 2 - wp / 2, -cc / 2 + wp / 2), (cc / 2 - wp / 2, cc / 2 + wp / 2)], "port rib", row("m5", "m10", "m11"))
    y.dim("h", cc / 2 - wp / 2, cc / 2 + wp / 2, t, px=14, ext=(t, t), row_id="m5")
    y.dim("h", -cc / 2 - wp / 2, cc / 2 + wp / 2, t, px=44, ext=(t, t), row_id="m4")

    # closure between two independent statements; neither enters the drawn scale through the other
    c.check("group index x round trip, Q 1.1e6 and tau 0.988 against c / FSR, um", 1.1e6 * lam * (1 - 0.988**2) / (2 * math.pi), c_um_ghz / fsr_ghz, 0.15)
    c.check("FSR 50 GHz converted to nm against the stated 0.4 nm", 1e3 * lam**2 * fsr_ghz / c_um_ghz, 0.4, 0.1)
    # two-mode beat, ports this close to the wall excite mostly modes 0 and 1: first order only, so a note and not a check
    lpi = 4 * 2.05 * w**2 / (3 * 1.55)
    d.note(f"First order, not a check: two-mode beat with an assumed TE slab index 2.05 gives a cross fraction of {100 * math.sin(math.pi * lm / (2 * lpi)) ** 2:.0f} % at the drawn length; the design value is {c.num('m2'):.0f} %.")
    return c
