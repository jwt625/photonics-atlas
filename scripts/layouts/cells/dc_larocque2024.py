"""Larocque 2024: 2x2 directional coupler of the PhC Michelson IQ modulator, TFLN rib (Fig. 2(a), Supp. Fig. 3(a), Supp. Sec. IV B).

Topology from Fig. 2(a): on the left two S-bends join the coupler to the PhC waveguides between the electrodes; on the right
the two arms part in near-circular 90 deg bends, up to the output and down to the input. Scale: the 20 um bar of Fig. 2(a)
against the embedded micrograph gives 0.258 um per image pixel. All in-plane curves are figure readings, the coupler itself
is the table. Not stated, so dashed: the plane of the 660 nm (Supp. Fig. 3(a) marks it in plan only; placed between ridge tops,
where the width is drawn in Supp. Fig. 2(c)), and the wall angle in the gap (35 deg is for waveguides generally; the text reports
steeper walls in narrow gaps).
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, assumed, fig, row, stated  # noqa: E402

ID = "cmp_larocque2024_dc_michelson"


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 2(a) micrograph", "Supp. Fig. 3(a) sketch", "Fig. 2(e) cross-section", "Supp. Fig. 2(c)", "p.6 Methods", "p.14 Supp. Sec. IV B"],
        "TFLN rib coupler: S-bends to the two PhC waveguides, 90 deg bends to input and output; electrodes and PhC truncated at their ends",
    )
    gap = c.um("m2")
    l0 = c.um("m3")
    w0 = c.um("m4")
    etch = c.um("m6")
    slab = c.um("m7")
    side = c.num("m8")  # to the film plane
    foot = etch / math.tan(math.radians(side))  # lateral run of one sidewall
    ww = 0.8  # p.6: nominal waveguide width
    um_px = 20.0 / 77.6  # 20 um bar is 50 page px; the electrode end-to-end gives 1.553 image px per page px
    y_c = (gap + w0) / 2
    why_gap = assumed("plane of the gap not stated: placed between ridge tops; wall angle in the gap not stated: 35 deg taken from the outer walls, while the text reports 17 deg in Bragg gaps")
    y_phc = 61.0 / 2 * um_px  # PhC waveguides 61 image px apart
    s_dx = 182.5 * um_px  # left S-bend, image px 717 to the start of the flat section
    r_b = 54.0  # right bends: circle through image points of both arms, +-3 um
    stub_l = 22.0  # PhC waveguide shown past the bend start, truncated
    stub_v = 18.0  # after the 90 deg bends, truncated

    src_fig_s = fig("Fig. 2(a)", "S-bend span and PhC waveguide spacing against the 20 um bar", "5 %")
    src_fig_b = fig("Fig. 2(a)", "bend radius 54 um against the 20 um bar", "3 um")
    src_taper = stated("p.14 Supp. Sec. IV B", "tapered from 800 nm to the coupling width") + fig("Supp. Fig. 3(a)", "taper runs along the bends")
    tp = c.view("top", "top view: coupler, S-bends, 90 deg bends")

    def arm(sign: float) -> list[tuple[Route, list[str], str]]:
        """sign +1: upper waveguide. Returns the pieces (route, source, role) of one arm, left to right."""
        out = []
        # left S-bend, drawn from the coupler outwards so the taper starts at w0
        s = Route((-l0 / 2, sign * y_c), 180.0, w0, tol=0.02)
        s.sbend(s_dx, -sign * (y_phc - y_c), n=60)  # heading 180: positive across is -y
        n = len(s.ws)
        for k in range(n):
            s.ws[k] = w0 + (ww - w0) * k / (n - 1)
        s.width = ww
        s.straight(stub_l)
        out.append((s, row("m4") + src_fig_s + src_taper, "S-bend to the PhC waveguide (truncated)"))
        cp = Route((-l0 / 2, sign * y_c), 0.0, w0).straight(l0)
        out.append((cp, row("m2", "m3", "m4") + why_gap, "coupling section"))
        t_deg = math.degrees(s_dx / r_b)  # taper over the same arc length as on the left
        b = Route((l0 / 2, sign * y_c), 0.0, w0, tol=0.02)
        b.arc(r_b, sign * t_deg, w_end=ww).arc(r_b, sign * (90.0 - t_deg)).straight(stub_v)
        out.append((b, row("m4") + src_fig_b + src_taper, "90 deg bend to the output" if sign > 0 else "90 deg bend to the input"))
        return out

    x_left = -l0 / 2 - s_dx - stub_l
    x_right = l0 / 2 + r_b
    y_top = y_c + r_b + stub_v
    margin = 6.0
    tp.rect(x_left - 12, -y_top - margin, x_right + margin, y_top + margin, "ln", "LN slab", row("m5", "m6", "m7"), layer="slab", alpha=0.35)
    pieces = arm(1.0) + arm(-1.0)

    def foot_poly(rt: Route) -> list[tuple[float, float]]:
        keep = rt.ws
        rt.ws = [w + 2 * foot for w in keep]
        poly = rt.polygon()
        rt.ws = keep
        return poly

    for rt, src, role in pieces:
        tp.poly(foot_poly(rt), "ln", "ridge foot: " + role, src + row("m6", "m8"), layer="overlay", alpha=0.45)
    for rt, src, role in pieces:
        tp.route(rt, "ln", "ridge top: " + role, src, layer="waveguide")

    # electrodes of Fig. 2(a): three bars ending just left of the S-bends, truncated
    x_e = (703.0 - 966.5) * um_px
    x_e0 = x_left - 12
    src_e = fig("Fig. 2(a)", "bar ends and edges against the 20 um bar, image px", "1 um") + stated("p.6 Methods", "500 nm gold")
    half_mid = 3.9
    half_out = 11.6
    bar = 7.7
    for y0, y1, role in ((half_out, half_out + bar, "upper electrode"), (-half_mid, half_mid, "centre electrode"), (-half_out - bar, -half_out, "lower electrode")):
        tp.rect(x_e0, y0, x_e, y1, "metal", role + " (truncated)", src_e, layer="metal")
    c.check("waveguide centred in the electrode gap: y_phc against the mid gap, um", y_phc, (half_mid + half_out) / 2, 0.02)

    tp.dim("h", -l0 / 2, l0 / 2, y_c + w0 / 2, px=-34, ext=(y_c, y_c), row_id="m3")
    tp.dim("v", -y_phc, y_phc, x_e + 6, px=0, ext=(x_e + 6, x_e + 6), text="15.7 um", src=src_fig_s)
    tp.label((x_right - 3, y_top - 6), "output", anchor="end", dx=-8)
    tp.label((x_right - 3, -y_top + 6), "input", anchor="end", dx=-8)
    tp.label((x_e + 3, y_phc), "PhC 1", anchor="start", dy=-9)
    tp.label((x_e + 3, -y_phc), "PhC 2", anchor="start", dy=13)
    tp.note("PhC cavities and electrodes continue left, and the arms continue up and down: truncated (Fig. 2(a)).")
    tp.note("Slab is everywhere in the window; darker band is the sidewall run of the ridge, 280 nm each side.")
    c.thumb = {"view": "top", "window": [-64, -21, 42, 21]}

    det = c.view("coupling", "detail: end of the coupling section, ridge tops and feet", like="top", window=(l0 / 2 - 7.5, -3.0, l0 / 2 + 7.5, 3.0))
    det.dim("v", y_c - w0 / 2, y_c + w0 / 2, l0 / 2 - 6.5, px=-14, ext=(l0 / 2 - 6.5, l0 / 2 - 6.5), row_id="m4")
    det.dim("v", -y_c + w0 / 2, y_c - w0 / 2, l0 / 2 - 4.0, px=-14, ext=(l0 / 2 - 4.0, l0 / 2 - 4.0), row_id="m2")
    det.note("Dashed: the source marks the 660 nm in plan only and gives no wall angle for this gap. The drawn space between feet follows from the two choices (ridge tops, 35 deg) and is not a source value; with steeper walls, as the text reports in narrow gaps, it is wider.")

    bend = c.view("sbend", "detail: left S-bend, taper from 800 nm to 600 nm", like="top", window=(-l0 / 2 - s_dx - 3, -10, -l0 / 2 + 3, 10))
    bend.note("S-bend shape read from Fig. 2(a); the sketch Supp. Fig. 3(a) shows the taper along it. Exact curve family not stated.")

    x = c.view("xsec", "cross-section at the coupler mid plane", "xsec")
    box = 2.0
    span = 3.0
    x.rect(-span, -slab - box - 0.6, span, -slab - box, "si", "Si substrate", assumed("substrate: truncated"), alpha=0.5, layer="substrate")
    x.rect(-span, -slab - box, span, -slab, "sio2", "buried oxide", assumed("insulator thickness not stated"), layer="oxide")
    x.rect(-span, -slab, span, 0.0, "ln", "LN slab", row("m5", "m6", "m7"), layer="slab")
    for s in (1.0, -1.0):
        xc = s * y_c
        x.poly([(xc - w0 / 2 - foot, 0.0), (xc + w0 / 2 + foot, 0.0), (xc + w0 / 2, etch), (xc - w0 / 2, etch)], "ln", "LN ridge", row("m4", "m6", "m8") + why_gap, layer="waveguide")
    x.dim("h", y_c - w0 / 2, y_c + w0 / 2, etch, px=14, ext=(etch, etch), row_id="m4")
    x.dim("h", -y_c + w0 / 2, y_c - w0 / 2, etch, px=30, ext=(etch, etch), row_id="m2")
    x.dim("v", 0.0, etch, y_c + w0 / 2 + foot, px=40, ext=(y_c + w0 / 2 + foot, y_c + w0 / 2 + foot), row_id="m6")
    x.dim("v", -slab, 0.0, -span, px=-14, ext=(-span, -span), row_id="m7")
    x.dim("v", -slab, etch, span, px=16, ext=(span, span), row_id="m5")
    x.note("Air above: no cladding stated for the coupler. Outer walls 35 deg from the normal (row: 55 deg from the plane). Gap plane and inner wall angle are assumptions, see the coupling detail.")
    return c
