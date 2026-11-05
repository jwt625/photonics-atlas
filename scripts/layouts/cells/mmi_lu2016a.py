"""Lu 2016 2x2 MMI 3 dB coupler of the MZI switch element, Si rib (Fig. 1(c) and its lower inset, Fig. 4(a), Sec. 2, Sec. 3).

Topology from the Fig. 1(c) inset: two inputs and two outputs, axes parallel, each port a linear taper 0.5 to 1.2 um. The
stated 1.72 um pitch puts the outer edge of each wide end inside the MMI wall.
Past the tapers, Fig. 1(c) and Fig. 4(a): S-bends fan out to the 127 um grating-coupler pitch on one side, to the MZI arms
on the other. Fan lengths read from Fig. 4(a) against the stated 127 um pitch.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, assumed, fig, row, stated  # noqa: E402

ID = "cmp_lit_lu2016a_mmi_2x2"


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 1(c) and lower inset", "Fig. 3(b)", "Fig. 4(a)", "Sec. 2", "Sec. 3"],
        "2x2 MMI, 1.72 um port pitch, linear tapers, S-bends fanning out to the grating couplers and the MZI arms",
    )
    w = c.um("m3")
    lm = c.um("m4")
    pitch = c.um("m5")
    wp = c.um("m6")
    lt = c.um("m7")
    wa = c.um("m10")
    off = pitch / 2
    gc_pitch = 127.0  # p.5 Sec. 3
    arm_sep = 140.0  # Fig. 4(a): MZI arm separation against the 127 um pitch
    fan_gc = 93.0  # Fig. 4(a): S-bend length on the grating-coupler side
    fan_arm = 80.0  # Fig. 4(a): S-bend length on the MZI side
    stub = 5.0  # Fig. 1(c) inset: straight past the taper, by ratio to the 10 um taper
    run = 30.0

    src_t = row("m5", "m6", "m7", "m10") + fig("Fig. 1(c) inset", "taper wide end at the MMI, axes parallel")
    src_gc = row("m10") + stated("p.5 Sec. 3", "grating couplers on a 127 um pitch") + fig("Fig. 4(a)", "S-bend length against the 127 um pitch", "15 %")
    src_arm = row("m10") + fig("Fig. 4(a)", "arm separation and S-bend length against the 127 um pitch", "15 %")

    top = c.view("top", "top view: 2x2 MMI with the S-bends of the switch element")
    top.rect(0, -w / 2, lm, w / 2, "si", "multimode region", row("m3", "m4"), layer="waveguide")
    ends = {}
    for sign in (1, -1):
        rt = Route((0.0, sign * off), 180.0, wp, tol=0.02)
        # heading 180: a positive across-offset is -y
        rt.straight(lt, wa).straight(stub).sbend(fan_gc, -sign * (gc_pitch / 2 - off)).straight(run)
        top.route(rt, "si", f"input port {1 if sign > 0 else 2}", src_t + src_gc, layer="waveguide")
        ends[("in", sign)] = rt
        ro = Route((lm, sign * off), 0.0, wp, tol=0.02)
        ro.straight(lt, wa).straight(stub).sbend(fan_arm, sign * (arm_sep / 2 - off)).straight(run)
        top.route(ro, "si", f"output port {3 if sign > 0 else 4}", src_t + src_arm, layer="waveguide")
        ends[("out", sign)] = ro
    top.label(ends[("in", 1)].pos, "1: to grating coupler", anchor="start", dy=-8)
    top.label(ends[("in", -1)].pos, "2: to grating coupler", anchor="start", dy=16)
    top.label(ends[("out", 1)].pos, "to MZI arm", anchor="end", dy=-8)
    top.label(ends[("out", -1)].pos, "to MZI arm", anchor="end", dy=16)
    x_l, x_r = ends[("in", 1)].pos[0], ends[("out", 1)].pos[0]
    top.dim("v", -gc_pitch / 2, gc_pitch / 2, x_l, px=-14, ext=(x_l, x_l), text="127 um", src=stated("p.5 Sec. 3", "grating-coupler pitch"))
    top.dim("v", -arm_sep / 2, arm_sep / 2, x_r, px=14, ext=(x_r, x_r), text="140 um", src=fig("Fig. 4(a)", "against the 127 um pitch", "15 %"))
    top.note("Fan-out read from the micrograph of Fig. 4(a). Grating couplers, the 2 um widened straights with their 200 um tapers (Sec. 3), the taps of Fig. 1(c) and the MZI are truncated.")
    top.note("The cascaded test structure of Fig. 3(b), used for the loss rows, has the same fan-out shape: one output to the next MMI, the other to a grating coupler.")
    c.thumb = {"view": "top", "window": [-lt - stub - 2, -8, lm + lt + stub + 2, 8]}

    det = c.view("det", "detail: MMI and tapers", like="top", window=(-lt - stub, -7, lm + lt + stub, 7))
    det.dim("h", 0, lm, w / 2, px=14, ext=(w / 2, w / 2), row_id="m4")
    det.dim("h", lm, lm + lt, off + wp / 2, px=32, ext=(off + wp / 2, off + wa / 2), row_id="m7")
    det.dim("v", -w / 2, w / 2, lm / 2, px=-18, ext=(lm / 2, lm / 2), row_id="m3")
    det.label((-lt - stub / 2, off), "access", dy=-12, row_id="m10")

    ports = c.view("ports", "detail: port wide ends at the MMI wall", like="top", window=(-4.5, -3.3, 4.2, 3.3))
    ports.dim("v", off - wp / 2, off + wp / 2, -3.0, px=-12, ext=(-3.0, -3.0), row_id="m6")
    ports.dim("v", -off, off, 0.5, px=10, ext=(0.0, 0.5), row_id="m5")
    ports.dim("v", -w / 2, w / 2, 3.2, px=6, ext=(3.2, 3.2), row_id="m3")

    def stack(vid: str, title: str, half: float) -> tuple:
        v = c.view(vid, title, "xsec")
        v.rect(-half, -2.0 - 0.5, half, -2.0, "si", "Si substrate", assumed("handle thickness not stated: truncated"), layer="substrate", alpha=0.5)
        v.rect(-half, -2.0, half, 0, "sio2", "buried oxide 2 um", stated("p.5 Sec. 3", "2 um BOX"), layer="oxide")
        v.rect(-half, 0, half, 2.23, "sio2", "PECVD oxide 1.5 um + 0.73 um", stated("p.5 Sec. 3", "1.5 um PECVD, then 0.73 um over the TiN level"), layer="oxide", alpha=0.45)
        v.rect(-half, 0, half, 0.06, "si", "Si slab 60 nm", stated("p.4 Sec. 2", "60 nm slab"), layer="slab")
        return v, half

    x, half = stack("xsec", "cross-section: 0.5 um access rib", 2.5)
    src_rib = row("m10") + stated("p.5 Sec. 3", "220 nm top Si, about 160 nm etch")
    x.rect(-wa / 2, 0, wa / 2, 0.22, "si", "Si rib", src_rib, layer="waveguide")
    x.dim("h", -wa / 2, wa / 2, 0.22, px=14, ext=(0.22, 0.22), row_id="m10")
    x.dim("v", 0, 0.22, wa / 2, px=14, ext=(wa / 2, wa / 2), text="220 nm", src=stated("p.5 Sec. 3", "top Si"))
    x.dim("v", 0, 0.06, -wa / 2, px=-14, ext=(-wa / 2, -wa / 2), text="60 nm", src=stated("p.4 Sec. 2", "slab"))
    x.dim("v", -2.0, 0, half, px=8, ext=(half, half), text="2 um", src=stated("p.5 Sec. 3", "BOX"))

    p, half = stack("xports", "cross-section: port wide ends at the MMI wall", 3.0)
    for s in (1, -1):
        p.rect(s * off - wp / 2, 0, s * off + wp / 2, 0.22, "si", "port taper, wide end", row("m5", "m6") + stated("p.5 Sec. 3", "220 nm top Si"), layer="waveguide")
    p.dim("h", off - wp / 2, off + wp / 2, 0.22, px=12, ext=(0.22, 0.22), row_id="m6")
    p.dim("h", -off, off, 0.22, px=-22, ext=(0.22, 0.22), row_id="m5")

    m, half = stack("xmmi", "cross-section: multimode region", 3.5)
    m.rect(-w / 2, 0, w / 2, 0.22, "si", "multimode rib", row("m3") + stated("p.5 Sec. 3", "220 nm top Si"), layer="waveguide")
    m.dim("h", -w / 2, w / 2, 0.22, px=14, ext=(0.22, 0.22), row_id="m3")

    # first order only: a note and not a check. 3 dB at L = Lpi / 2 holds for ports near W/6: that reading is an inference here, the paper does not state a mechanism
    n_r = 2.85
    we = w + 1.56 / math.pi / math.sqrt(n_r**2 - 1.444**2)
    lf = 4 * n_r * we**2 / (3 * 1.56) / 2
    det.note(f"Inference here, not in the paper: the port offset {off:.2f} um is near W/6 = {w / 6:.2f} um, where a 3 dB image falls at Lpi / 2. First order with an assumed slab index {n_r}: {lf:.1f} um, {100 * (lf - lm) / lm:.1f} % above the drawn {lm} um.")
    return c
