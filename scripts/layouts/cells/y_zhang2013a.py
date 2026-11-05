"""Zhang 2013: PSO-optimized Y-junction (Table 1, Fig. 1(a), Fig. 1(b), Fig. 3, Sec. 2.1-2.2).

The outline is the paper's: widths w1-w13 of Table 1 joined by a cubic spline, the interpolation the paper names, with w1 at
the start and w13 at the end of the 2 um taper as the bracket of Fig. 1(a) shows. The end condition is not stated: zero slope,
because both ends join straight waveguides. Output arms: 0.5 um each with a 0.2 um gap; then bends of radius 5 um (Sec. 3 for
connecting waveguides), and the first micron agrees with the field lobes of Fig. 1(b), which part by about 0.1 um per arm.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Pt, Route, assumed, fig, row, stated  # noqa: E402

ID = "cmp_lit_zhang2013a_pso_y_junction"
WIDTHS = [0.5, 0.5, 0.6, 0.7, 0.9, 1.26, 1.4, 1.4, 1.4, 1.4, 1.31, 1.2, 1.2]  # Table 1


def clamped_spline(xs: list[float], ys: list[float]) -> list[tuple[float, float, float, float]]:
    """Cubic spline with zero end slopes (lib.py has none). Returns (a, b, c, d) per interval, in s = x - x_i."""
    n = len(xs) - 1
    h = [xs[i + 1] - xs[i] for i in range(n)]
    al = [0.0] * (n + 1)
    al[0] = 3 * (ys[1] - ys[0]) / h[0]
    al[n] = -3 * (ys[n] - ys[n - 1]) / h[n - 1]
    for i in range(1, n):
        al[i] = 3 * (ys[i + 1] - ys[i]) / h[i] - 3 * (ys[i] - ys[i - 1]) / h[i - 1]
    lo, mu, z = [0.0] * (n + 1), [0.0] * (n + 1), [0.0] * (n + 1)
    lo[0], mu[0], z[0] = 2 * h[0], 0.5, al[0] / (2 * h[0])
    for i in range(1, n):
        lo[i] = 2 * (xs[i + 1] - xs[i - 1]) - h[i - 1] * mu[i - 1]
        mu[i] = h[i] / lo[i]
        z[i] = (al[i] - h[i - 1] * z[i - 1]) / lo[i]
    lo[n] = h[n - 1] * (2 - mu[n - 1])
    z[n] = (al[n] - h[n - 1] * z[n - 1]) / lo[n]
    cs = [0.0] * (n + 1)
    cs[n] = z[n]
    out = [(0.0, 0.0, 0.0, 0.0)] * n
    for j in range(n - 1, -1, -1):
        cs[j] = z[j] - mu[j] * cs[j + 1]
        b = (ys[j + 1] - ys[j]) / h[j] - h[j] * (cs[j + 1] + 2 * cs[j]) / 3
        d = (cs[j + 1] - cs[j]) / (3 * h[j])
        out[j] = (ys[j], b, cs[j], d)
    return out


def build() -> Cell:
    c = Cell(
        ID,
        ["Table 1 (w1-w13)", "Fig. 1(a) layout", "Fig. 1(b) field map", "Fig. 3 test structures", "Sec. 2.1", "Sec. 2.2", "Sec. 3"],
        "Y-junction outline from the 13 PSO widths of Table 1, spline-joined; output arms with 0.2 um gap and 5 um bends",
    )
    length = c.um("m9")
    w0 = c.um("m10")
    t = c.um("m12")
    box = c.um("m13")
    clad = c.um("m14")
    gap = 0.2  # Fig. 1(a) label, also the stated minimum feature
    r_b = 5.0  # Sec. 3: bends of the connecting waveguides
    xs = [length * i / 12 for i in range(13)]
    coef = clamped_spline(xs, WIDTHS)
    tab = stated("Table 1", "taper widths w1-w13") + stated("Fig. 1(a) caption", "spline interpolation") + row("m9")

    def width(x: float) -> float:
        i = min(int(x / (length / 12)), 11)
        s = x - xs[i]
        a, b, cc, d = coef[i]
        return a + b * s + cc * s**2 + d * s**3

    n = 144
    outer: list[Pt] = [(length * k / n, width(length * k / n) / 2) for k in range(n + 1)]
    l_in = 1.5
    poly: list[Pt] = [(-l_in, w0 / 2)] + outer + [(x, -y) for x, y in reversed(outer)] + [(-l_in, -w0 / 2)]

    tp = c.view("top", "top view: PSO outline at true scale, w1-w13 marked as in Fig. 1(a)")
    tp.poly(poly, "si", "input waveguide and PSO taper", tab + row("m10"), layer="waveguide")
    # output arms: first the part that the field map shows, then the rest of the bend to a parallel stub
    a_fig = math.degrees(math.asin(1.0 / r_b))
    a_rest = 30.0 - a_fig
    for s in (1.0, -1.0):
        y0 = s * (gap + w0) / 2
        first = Route((length, y0), 0.0, w0, tol=0.003).arc(r_b, s * a_fig)
        tp.route(first, "si", "output arm, first micron", row("m10") + stated("Fig. 1(a)", "0.5 um arms, 0.2 um gap") + stated("p.5 Sec. 3", "bend radius 5 um") + fig("Fig. 1(b)", "lobes part about 0.1 um over the first micron", "0.03 um"), layer="waveguide")
        rest = Route(first.pos, first.heading, w0, tol=0.003).arc(r_b, s * a_rest).arc(r_b, -s * 30.0).straight(1.0)
        tp.route(rest, "si", "output arm, rest of the bend (truncated)", row("m10") + stated("p.5 Sec. 3", "bend radius 5 um") + assumed("sweep of the bend not stated: 30 deg, stub truncated"), layer="waveguide")
    for i, (x, w) in enumerate(zip(xs, WIDTHS, strict=True)):
        tp.line([(x, -w / 2), (x, w / 2)], f"w{i + 1} = {w} um", stated("Table 1"))
        if i % 2 == 0 or i == 11:
            tp.label((x, -w / 2), f"w{i + 1}", dy=13)
    tp.dim("h", 0.0, length, -0.7, px=-34, ext=(-w0 / 2, -0.6), row_id="m9")
    tp.dim("v", -w0 / 2, w0 / 2, -l_in, px=-6, ext=(-l_in, -l_in), row_id="m10")
    tp.dim("v", -0.7, 0.7, (xs[7] + xs[8]) / 2, px=0, ext=((xs[7] + xs[8]) / 2, (xs[7] + xs[8]) / 2), text="1.4 um", src=stated("Table 1", "w7-w10"))
    tp.note("Input and output waveguides continue to the grating couplers at 127 um pitch: truncated (Fig. 3).")
    tp.note("w1-w13 are knots of the spline; end slopes zero, not stated in the paper.")
    tp.note("The footprint row (paper: less than 1.2 x 2 um) counts the output width; Table 1 peaks at 1.4 um, so the drawn envelope is 1.4 x 2 um.")
    c.thumb = {"view": "top"}

    tip = c.view("outputs", "detail: taper end, arms and gap", like="top", window=(length - 0.5, -0.85, length + 0.85, 0.85))
    tip.dim("v", -gap / 2, gap / 2, length + 0.3, px=24, ext=(length + 0.3, length + 0.3), text="0.2 um", src=stated("Fig. 1(a)", "gap between arms; stated minimum feature"))
    tip.dim("v", gap / 2, gap / 2 + w0, length + 0.1, px=-30, ext=(length + 0.1, length + 0.1), row_id="m10")
    tip.dim("v", -0.6, 0.6, length - 0.08, px=-14, ext=(length - 0.08, length - 0.08), text="1.2 um", src=stated("Table 1", "w13"))

    peak = max(width(length * k / 1000) for k in range(1001))
    c.check("w13 against 2 arms + gap um", WIDTHS[-1], 2 * w0 + gap, 1e-9)
    c.check("spline overshoot against w7-w10 um", peak, 1.4, 0.03)
    c.check("first micron of the arm bend against Fig. 1(b) um", r_b * (1 - math.cos(math.radians(a_fig))), 0.1, 0.05)

    def stack(vid: str, title: str, x_at: float, cores: list[tuple[float, float]], labels: bool) -> None:
        x = c.view(vid, title, "xsec")
        span = 1.5
        x.rect(-span, -box - 0.4, span, -box, "si", "Si handle", assumed("handle: truncated"), alpha=0.5, layer="substrate")
        x.rect(-span, -box, span, 0.0, "sio2", "buried oxide", row("m13"), layer="oxide")
        x.rect(-span, 0.0, span, clad, "sio2", "deposited oxide top cladding", row("m14"), alpha=0.45, layer="oxide")
        for y0, y1 in cores:
            x.rect(y0, 0.0, y1, t, "si", "Si core", row("m12") + stated("Table 1"), layer="waveguide")
        x.dim("v", 0.0, t, cores[-1][1], px=20, ext=(cores[-1][1], cores[-1][1]), row_id="m12")
        x.dim("v", -box, 0.0, -span, px=-14, ext=(-span, -span), row_id="m13")
        x.dim("v", 0.0, clad, span, px=14, ext=(span, span), row_id="m14")
        if labels:
            x.dim("h", -0.7, 0.7, t, px=16, ext=(t, t), text="1.4 um", src=stated("Table 1", "w8"))
        else:
            x.dim("h", gap / 2, gap / 2 + w0, t, px=16, ext=(t, t), row_id="m10")
            x.dim("h", -gap / 2, gap / 2, t, px=34, ext=(t, t), text="0.2 um", src=stated("Fig. 1(a)", "gap"))
        x.note(f"Plane x = {x_at:.2f} um from the taper start.")

    stack("xsec", "cross-section at w8, the widest part", xs[7], [(-0.7, 0.7)], True)
    stack("xsec2", "cross-section at the output arms", length, [(-gap / 2 - w0, -gap / 2), (gap / 2, gap / 2 + w0)], False)
    return c
