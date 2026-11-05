"""OFC 2026 Th2A.9: 16 x 16 overlapping Si AWG, 1.6 nm spacing, 550 x 590 um (text and captions only, figures not available).

Stated: overlapping architecture, 16 + 16 ports, 2 um arrays, parabolic tapers at both ends of each array section joined by
0.45 um curved waveguides, broadened 45 and 90 deg Euler bends in two bending sections, footprint. Everything else is assumed
and dashed: the shared slab with star axes crossing at 90 deg (the usual overlapped layout, the paper's ref. [6]), the number
of arms (between 3 and 3.5 x channels), the delta L (FSR = 16 x 1.6 nm, group index 3.7), star radius, pitches, Euler radius. The bend
sequence 45, 90, 90, 45 is what the two bending sections require for those crossing axes. lib.py has no Euler bend: helper here.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Pt, Route, arc, assumed, row, stated  # noqa: E402

ID = "cmp_ofc2026_th2a9_awg_16ch_1p6nm"


def euler(rt: Route, sweep_deg: float, r_min: float, n: int = 5) -> Route:
    """Symmetric Euler bend: curvature linear from 0 to 1 / r_min at mid sweep and back. Effective length 2 |sweep| r_min."""
    th = math.radians(abs(sweep_deg))
    sign = 1.0 if sweep_deg > 0 else -1.0
    length = 2 * th * r_min
    h = math.radians(rt.heading)
    x, y = rt.pos
    ds = length / (2 * n)
    k_max = 1 / r_min
    substeps = 6
    s = 0.0
    for _step in range(2 * n):
        for _ in range(substeps):
            d = ds / substeps
            mid = s + d / 2
            kap = k_max * (mid / (length / 2)) if mid <= length / 2 else k_max * ((length - mid) / (length / 2))
            h += sign * kap * d
            x += d * math.cos(h)
            y += d * math.sin(h)
            s += d
        rt._add((x, y), rt.width, math.degrees(h))
    rt.heading += sweep_deg
    rt.length += length
    return rt


def build() -> Cell:
    c = Cell(
        ID,
        ["text and captions only, figures not available: Sec. 1, Sec. 2, Sec. 3, captions of Fig. 1 and Fig. 2"],
        "Overlapped AWG from the text only: every in-plane shape is a drafting assumption; only widths, port count and footprint are stated",
    )
    w_b = c.um("m9")
    n_io = int(c.num("m7"))
    w_n = 0.45  # Sec. 2
    width, height = 550.0, 590.0  # m8 is the product; which is which is not stated
    t_si = 0.22
    n_arm = 52
    fsr = n_io * c.num("m6") * 1e-3
    n_g = 3.7
    dl = 1.55**2 / (n_g * fsr)
    r_fpr = 170.0
    d_a = 2.4
    delta = d_a / r_fpr
    d_io = (1550.0 / (fsr * 1e3)) * c.num("m6") * 1e-3 / (2.85 * delta)  # grating equation, slab index 2.85 assumed
    r_e = 18.0  # Euler minimum radius
    l_t1 = 20.0  # parabolic taper at the star, and after the curved section
    r_n = 12.0  # curved 0.45 um section
    p_par = 2.8  # pitch of the parallel 45 deg legs
    x_in0 = 56.0  # inner arm verticals
    x_out = width / 2 - w_b / 2
    px = (x_out - x_in0) / (n_arm - 1)
    r0 = r_fpr + l_t1
    a = r_fpr / 2 * math.cos(math.radians(45.0))
    y_o = 86.0  # centre of the shared slab above the bottom of the footprint
    src = row("m9") + stated("Sec. 2", "2 um array, parabolic tapers, 0.45 um curved waveguides, 45 and 90 deg Euler bends") + assumed("layout not stated, figures not available: axes crossing at 90 deg, arm count, delta L, radii and pitches are drafting choices; only the footprint closes it")
    tp = c.view("top", "top view: assumed overlapped layout at true scale, text and captions only")

    def half_probe(i: int) -> tuple[float, float, float, float]:
        """Left half geometry of arm i: th, radial run s, leg length, y after the 45 deg bend."""
        th = ((n_arm - 1) / 2 - i) * delta  # th > 0: towards the device centre
        ax = (a, y_o - a)
        d0 = math.radians(135.0 - math.degrees(th))
        u_t = ((n_arm - 1) / 2 - i) * p_par
        s = (u_t - r0 * math.sin(th) - math.copysign(r_n * (1 - math.cos(th)), th)) / math.sin(th)
        if s < -1e-6:
            raise ValueError(f"arm {i}: radial run {s}")
        rt = Route((ax[0] + r0 * math.cos(d0), ax[1] + r0 * math.sin(d0)), 135.0 - math.degrees(th), w_n, tol=0.05)
        rt.straight(max(s, 0.0)).arc(r_n, math.degrees(th)).taper(l_t1, w_b, power=0.5, n=8)
        px0, py0 = rt.pos
        e = euler(Route((0.0, 0.0), 135.0, w_b), -45.0, r_e)
        x_v = -(x_in0 + i * px)
        leg = (x_v - px0 - e.pos[0]) / math.cos(math.radians(135.0))
        if leg < -1e-6:
            raise ValueError(f"arm {i}: leg {leg}")
        return th, s, leg, py0 + leg * math.sin(math.radians(135.0)) + e.pos[1]

    e90 = euler(Route((0.0, 0.0), 90.0, w_b), -90.0, r_e)
    d90 = e90.pos[0]

    def arm(i: int, y_top: float) -> Route:
        th, s, leg, y_v = half_probe(i)
        th_deg = math.degrees(th)
        d0 = math.radians(135.0 - th_deg)
        x_v = -(x_in0 + i * px)
        rt = Route((a + r0 * math.cos(d0), y_o - a + r0 * math.sin(d0)), 135.0 - th_deg, w_n, tol=0.05)
        rt.straight(max(s, 0.0)).arc(r_n, th_deg).taper(l_t1, w_b, power=0.5, n=8)
        rt.straight(max(leg, 0.0))
        euler(rt, -45.0, r_e)
        rt.straight(y_top - d90 - y_v)
        euler(rt, -90.0, r_e)
        rt.straight(-2 * x_v - 2 * d90)
        euler(rt, -90.0, r_e)
        rt.straight(y_top - d90 - y_v)
        euler(rt, -45.0, r_e)
        rt.straight(max(leg, 0.0))
        rt.taper(l_t1, w_n, power=2.0, n=8).arc(r_n, th_deg).straight(max(s, 0.0))
        return rt

    y_top_out = height - w_b / 2
    # L(i, y) = base(i) + 2 y: the outer arm lands on the footprint, the shortest arm follows from delta L
    base0 = arm(0, 2000.0).length - 4000.0
    base_o = arm(n_arm - 1, 2000.0).length - 4000.0
    y_top0 = y_top_out + (base_o - base0 - (n_arm - 1) * dl) / 2
    if y_top0 - d90 - half_probe(0)[3] < 5.0:
        raise ValueError(f"shortest arm too low: top {y_top0}, bend start {half_probe(0)[3]}")
    routes = [arm(0, y_top0)]
    l0 = routes[0].length
    y_tops = [y_top0]
    for i in range(1, n_arm):
        guess = y_top0 + (y_top_out - y_top0) * i / (n_arm - 1)
        probe = arm(i, guess)
        y = guess + (l0 + i * dl - probe.length) / 2
        routes.append(arm(i, y))
        y_tops.append(y)
    for i, rt in enumerate(routes):
        tp.route(rt, "si", f"arrayed waveguide {i + 1} of {n_arm} (arm count assumed)", src, layer="waveguide")

    # both stars share one slab; array arcs upper left and upper right, ports lower right and lower left
    half = math.degrees((n_arm / 2 + 0.6) * delta)

    def star(axis_deg: float, ax: Pt) -> list[Pt]:
        pole_arc = arc(ax, r_fpr, axis_deg - half, axis_deg + half, tol=0.1)
        cr = (ax[0] + r_fpr / 2 * math.cos(math.radians(axis_deg)), ax[1] + r_fpr / 2 * math.sin(math.radians(axis_deg)))
        b = math.degrees(2 * (n_io / 2 + 1.5) * d_io / r_fpr)
        return pole_arc + arc(cr, r_fpr / 2, axis_deg + 180.0 - b, axis_deg + 180.0 + b, tol=0.1)

    axis = ((135.0, (a, y_o - a)), (45.0, (-a, y_o - a)))
    for axis_deg, ax in axis:
        tp.poly(star(axis_deg, ax), "si", "star coupler of the shared slab", row("m7") + assumed("star radius and outline not stated; two stars overlapped with axes at 90 deg"), layer="waveguide", alpha=0.6)
        for i in range(n_arm):
            th = ((n_arm - 1) / 2 - i) * delta * (1.0 if axis_deg == 135.0 else -1.0)
            d = axis_deg - math.degrees(th)
            p = (ax[0] + r_fpr * math.cos(math.radians(d)), ax[1] + r_fpr * math.sin(math.radians(d)))
            ap = Route(p, d, w_b, tol=0.05).taper(l_t1, w_n, power=0.5, n=8)
            tp.route(ap, "si", "parabolic taper at the star", src, layer="waveguide")
        for k in range(n_io):
            phi = (k - (n_io - 1) / 2) * d_io / r_fpr
            ang = axis_deg + 180.0
            cp = math.radians(ang + math.degrees(phi))
            q = (ax[0] + r_fpr * math.cos(math.radians(axis_deg)) + r_fpr * math.cos(phi) * math.cos(cp), ax[1] + r_fpr * math.sin(math.radians(axis_deg)) + r_fpr * math.cos(phi) * math.sin(cp))
            rt = Route(q, ang + math.degrees(phi), w_b, tol=0.05).taper(l_t1, w_n, power=0.5, n=8).straight(16.0)
            tp.route(rt, "si", f"port {k + 1} of {n_io} (routing to grating couplers truncated)", row("m7") + stated("Sec. 3", "16 input and 16 output ports, TE grating couplers") + assumed("pitch, position and stub length not stated"), layer="waveguide")

    x_max = x_out + w_b / 2
    y_max = y_tops[-1] + w_b / 2
    c.check("arm length increment um against the assumed delta L", (routes[-1].length - routes[0].length) / (n_arm - 1), dl, 1e-6)
    c.check("drawn footprint against the row, um2", 2 * x_max * y_max, c.num("m8"), 1e-3)

    tp.dim("h", -x_out, x_out, y_top_out, px=14, ext=(y_top_out, y_top_out), text="550 um", src=stated("Sec. 3", "footprint 550 x 590 um2; abstract prints 540; orientation not stated"))
    tp.dim("v", 0.0, y_max, x_max, px=16, ext=(x_max, x_max), text="590 um", src=stated("Sec. 3", "footprint 550 x 590 um2; orientation not stated"))
    tp.label((0.0, y_o), "shared slab", anchor="middle")
    tp.note("Text and captions only: the figures of this paper are not available. Only the widths, port count, Euler bend angles and footprint are the paper's.")
    tp.note(f"Assumed, not in the paper: {n_arm} arms, delta L {dl:.1f} um, axes crossing at 90 deg, star radius, Euler radius. Do not read dimensions off the arms.")
    c.thumb = {"view": "top", "window": [-280, 40, 280, 264]}

    det = c.view("taper", "detail: parabolic tapers joined by 0.45 um curved sections, as the text describes", like="top", window=(-118, 112, -48, 172))
    det.note("Shape order from Sec. 2 and the Fig. 1(b) caption: 2 um taper, 0.45 um curve, taper to 2 um. Lengths and radii assumed.")
    bend = c.view("bends", "detail: broadened 45 and 90 deg Euler bends", like="top", window=(-x_out - 6, y_top_out - 70, -x_out + 80, y_top_out + 4))
    bend.note("Fig. 1(c), (d) captions name the angles; minimum radius assumed. Width stays 2 um through the bend (caption: broadened).")

    x = c.view("xsec", "cross-section: arrayed waveguide, stack assumed", "xsec")
    box, clad, span = 2.0, 1.0, 3.2
    x.rect(-span, -box - 0.5, span, -box, "si", "Si substrate", assumed("substrate: truncated"), alpha=0.5, layer="substrate")
    x.rect(-span, -box, span, 0.0, "sio2", "buried oxide", assumed("not stated"), layer="oxide")
    x.rect(-span, 0.0, span, t_si + clad, "sio2", "top cladding", assumed("not stated"), alpha=0.45, layer="oxide")
    x.rect(-w_b / 2, 0.0, w_b / 2, t_si, "si", "Si core, thickness assumed", row("m9") + assumed("Si thickness not stated"), layer="waveguide")
    x.dim("h", -w_b / 2, w_b / 2, t_si, px=14, ext=(t_si, t_si), row_id="m9")
    x.note("Only the 2 um width is the paper's. Thicknesses are drafting values, unlabelled.")
    return c
