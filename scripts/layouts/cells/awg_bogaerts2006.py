"""Bogaerts 2006: 16 x 200 GHz SOI AWG, rectangular layout, broadened arms, two-step star couplers (Fig. 4, Sec. V).

Topology from the Fig. 4 SEM: two stars side by side at the bottom, 36 arms rising out of them, nested inverted U: each arm goes
up, across and down, with the shortest arm between the stars. Scale: the 100 um bar spans 194 px of the embedded image, 0.5155
um/px. Read off it: 36 verticals at 3.08 um (x), 36 levels averaging 8.65 um (y), hence delta L = 2(px + py) = 23.5 um, which the
FSR row and the paper's group index range confirm. Arm lengths are solved to that increment; the resulting level pitch grows from
the longest to the shortest arm because the fan bends sit lower on outer arms, and the SEM shows the same trend.
I/O: nested, the port farthest out on its star turns first at the highest level, on both stars, no crossings. A build-time test
holds every waveguide polygon of this cell apart. The star outline is not resolved in the SEM: see the star view note.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Pt, Route, arc, assumed, fig, row, stated  # noqa: E402

ID = "cmp_lit_bogaerts2006_awg_16x200ghz"


def build() -> Cell:
    c = Cell(
        ID,
        ["Fig. 4 SEM and its four details", "Sec. V", "Sec. II (stack, group index)", "Fig. 5 (FSR)"],
        "Rectangular AWG: both stars, 36 solved arms, 0.8 um straights and 0.5 um bends, shallow-deep transitions, I/O routing truncated",
    )
    n_arm = int(c.num("m2"))
    n_out = int(c.num("m1"))
    n_in = 10  # Fig. 4: 10 verticals at the left star, 16 at the right (peak count across the bundle)
    n_dummy = 3  # Fig. 4 lower detail: 3 shallow lines left of the first deep tip end in the field
    r_b = c.um("m6")
    l_t = c.um("m14")  # transition length, the row's range midpoint
    fsr = c.num("m4") * 1e-3
    etch = c.um("m7")
    w_b, w_n = 0.8, 0.5  # Fig. 4 corner detail labels
    w_ap = 1.1  # aperture width at the star, not stated
    t_si = 0.22  # p.1 Sec. II
    box = 1.0  # p.1 Sec. II
    l_arm_taper = 6.0  # Fig. 4 corner detail: width changes over 5 to 8 um
    um_px = 100.0 / 194.0  # Fig. 4: 100 um bar, embedded image
    y_px0 = 1008.0  # image row of y = 0: mean of the two port arcs, see y_port
    px, py = 5.97 * um_px, (606.0 - 18.0) / 35 * um_px  # Fig. 4: 36 verticals x 64 to 273 px; 36 levels y 18 to 606 px
    x_in0 = 10.0 * um_px  # Fig. 4: half distance between the two legs of the shortest arm
    y_top0 = (y_px0 - 606.0) * um_px  # Fig. 4: top of the shortest arm
    r_s = (y_px0 - 672.0) * um_px  # Fig. 4: deep-shallow boundary at the star axis, image row 672
    delta = 2.65 / r_s  # rad, array angular pitch: 2.65 um at r_s, array detail, 18.8 px of 0.143 um/px
    r_fpr = 105.0  # the I/O lines of the lower detail converge at 105 um, +-15 um
    d_io = 2.2  # Fig. 4 lower detail: pitch of the shallow lines at their top ends, 15 px of 0.148 um/px
    l_shallow = 12.6  # Fig. 4 lower detail: top of the shallow lines to the deep-etch tips
    l_dummy = 18.0  # Fig. 4 lower detail: length of the shallow lines with no deep tip
    t_io = 19.0  # Fig. 4 lower detail: deep tips to the first bend of the outer port, inside the row's 15-30 um
    y_port = {-1.0: (y_px0 - (1026.0 - l_shallow / um_px)) * um_px, 1.0: (y_px0 - (1041.0 - l_shallow / um_px)) * um_px}  # Fig. 4: lines appear at rows 1026 (left), 1041 (right)
    x_pitch_io = 3.0  # Fig. 4: verticals of the I/O bundles, 5.8 px
    levels = {  # Fig. 4: image rows of the horizontal runs, highest first
        -1.0: [1072.5 + 2.72 * k for k in range(n_in)],
        1.0: [1079.0, 1085.0] + [1089.0 + 3.0 * k for k in range(n_out - 2)],
    }
    x_stop = {-1.0: 144.0, 1.0: 138.0}  # the frame of Fig. 4 on each side
    diag = 38.0  # Fig. 4: I/O bundles leave at this angle from x
    x_c = x_in0 + (n_arm - 1) * px / 2  # star centres at +-x_c: the fan is symmetric about the array half
    dl = 2 * (px + py)
    wgs: list[tuple[str, list[Pt]]] = []  # (waveguide, polygon) for the crossing test

    def draw(group: str, rt: Route, role: str, src: list[str]) -> None:
        wgs.append((group, rt.polygon()))
        tp.route(rt, "si", role, src, layer="waveguide")

    src_arm = row("m2", "m6") + fig("Fig. 4", "nested rectangular arms, pitches against the 100 um bar", "2 %") + stated("Fig. 4 detail", "0.8 um straight, 0.5 um at the bend")
    src_st = fig("Fig. 4 array detail", "radial lines, 10 um bar", "10 %")
    tp = c.view("top", "top view: both stars and the array at true scale")

    def run(rt: Route, s: float) -> None:
        if s < -1e-6:
            raise ValueError(f"negative run {s}")
        if s >= 2 * l_arm_taper + 1.0:
            rt.straight(l_arm_taper, w_b).straight(s - 2 * l_arm_taper).straight(l_arm_taper, w_n)
        else:
            rt.straight(max(s, 0.0))

    r0 = r_s + l_t  # arm routes start where the transition ends; all arms alike from here to the star

    def arm(i: int, y_top: float) -> Route:
        """Arm i, left star to right star (i = 0 is the shortest). th > 0 leans outwards going up."""
        th = (i - (n_arm - 1) / 2) * delta
        th_deg = math.degrees(th)
        p = (-x_c - r0 * math.sin(th), r0 * math.cos(th))
        rt = Route(p, 90.0 + th_deg, w_n, tol=0.05)
        x_v = -(x_in0 + i * px)
        # radial run until the fan bend lands on this arm's vertical at x_v
        s = (p[0] - x_v - math.copysign(r_b * (1 - math.cos(th)), th)) / math.sin(th)
        if s < -1e-6:
            raise ValueError(f"arm {i}: fan run {s}")
        rt.straight(max(s, 0.0)).arc(r_b, -th_deg)
        y_v = rt.pos[1]
        run(rt, y_top - r_b - y_v)
        rt.arc(r_b, -90.0)
        run(rt, -2 * x_v - 2 * r_b)
        rt.arc(r_b, -90.0)
        run(rt, y_top - r_b - y_v)
        rt.arc(r_b, -th_deg)
        rt.straight(max(s, 0.0))
        return rt

    routes = [arm(0, y_top0)]
    l0 = routes[0].length
    y_tops = [y_top0]
    for i in range(1, n_arm):
        probe = arm(i, y_top0 + i * py)
        y = y_top0 + i * py + (l0 + i * dl - probe.length) / 2
        routes.append(arm(i, y))
        y_tops.append(y)
    for i, rt in enumerate(routes):
        draw(f"arm {i}", rt, f"arrayed waveguide {i + 1} of {n_arm}", src_arm)

    alpha = (n_arm - 1) / 2 * delta

    def port_xy(cx: float, y_p: float, off: float) -> tuple[Pt, float]:
        """Position and outgoing lean (rad) of a line at offset off along the port arc: Rowland circle, aimed at the array pole."""
        rr = r_fpr - y_p
        phi = off / rr
        return (cx + rr * math.cos(phi) * math.sin(phi), r_fpr - rr * math.cos(phi) ** 2), phi

    def fpr(cx: float, y_p: float, half_off: float) -> list[Pt]:
        a = math.degrees(alpha + 0.8 * delta)
        rr = r_fpr - y_p
        beta = math.degrees(2 * (half_off + d_io) / rr)
        return arc((cx, 0.0), r_fpr, 90.0 - a, 90.0 + a, tol=0.05) + arc((cx, y_p + rr / 2), rr / 2, 270.0 - beta, 270.0 + beta, tol=0.05)

    src_field = row("m7") + fig("Fig. 4", "boundary arc of the shallow field, array and I/O details", "10 um") + assumed("field outline at the sides not visible in the SEM")
    src_io = fig("Fig. 4 lower details", "line count, pitch, turn levels, 38 deg bundle, against the bars", "10 %") + row("m1", "m6")
    src_tr = row("m7", "m14") + fig("Fig. 4 lower detail", "deep-etch tips 12.6 um below the top of the lines, wedges 19 um to the first bend", "10 %")
    ports = {-1.0: n_in, 1.0: n_out}
    for sgn, n_p in ports.items():
        cx = sgn * x_c
        y_p = y_port[sgn]
        n_all = n_p + (2 * n_dummy if sgn < 0 else 0)
        half_all = (n_all + 1) / 2 * d_io * (r_fpr - y_p + l_dummy) / (r_fpr - y_p)
        half_con = (n_p + 1) / 2 * d_io * (r_fpr - y_p + l_shallow) / (r_fpr - y_p)
        a_f = math.degrees(alpha + 1.5 * delta)
        y_tip, y_dum = y_p - l_shallow, y_p - l_dummy - 0.5
        field = arc((cx, 0.0), r_s, 90.0 - a_f, 90.0 + a_f, tol=0.1)
        field += [(cx - half_all, y_dum), (cx - half_con, y_dum), (cx - half_con, y_tip), (cx + half_con, y_tip), (cx + half_con, y_dum), (cx + half_all, y_dum)] if sgn < 0 else [(cx - half_con, y_tip), (cx + half_con, y_tip)]
        tp.poly(field, "si", "shallow-etched field (150 nm Si)", src_field, layer="slab", alpha=0.3)
        # shoulders of the shallow etch around each arm: the wedges between them are the deep etch tips
        for i in range(n_arm):
            th = sgn * -1.0 * (i - (n_arm - 1) / 2) * delta  # outward arms lean away from the device centre on both sides
            sn, cs = math.sin(th), math.cos(th)

            def pt(r: float, u: float, sn: float = sn, cs: float = cs, cx: float = cx) -> Pt:
                return (cx - r * sn + u * cs, r * cs + u * sn)

            hw = r_s * delta / 2
            tp.poly([pt(r_s, -hw), pt(r_s, hw), pt(r0, w_n / 2), pt(r0, -w_n / 2)], "si", "shallow shoulder, deep-shallow transition", row("m7", "m14") + src_st, layer="slab", alpha=0.3, lod=0.8)
            head = 90.0 + math.degrees(th)
            draw(f"arm {i}", Route(pt(r_fpr + 10.0, 0.0), head, w_n, tol=0.05).straight(r0 - r_fpr - 10.0), "waveguide in the shallow field", src_st)
            draw(f"arm {i}", Route(pt(r_fpr, 0.0), head, w_ap, tol=0.05).straight(10.0, w_n), "aperture flare at the star", src_st + assumed("aperture width and flare length not stated"))
        half_off = (n_all - 1) / 2 * d_io
        tp.poly(fpr(cx, y_p, half_off), "si", "free propagation region, unetched Si", row("m2") + fig("Fig. 4 details", "centre and radius from where the array and I/O lines converge", "15 um") + assumed("star outline itself not resolved in the SEM"), layer="waveguide", alpha=0.75)

        # connected ports: shallow section, wedge transition, then down and out; the outermost turns first at the highest level
        lv = levels[sgn]
        for k in range(n_p):
            u = k - (n_p - 1) / 2
            q, phi = port_xy(cx, y_p, u * d_io)
            head = -90.0 + math.degrees(phi)
            rt = Route(q, head, w_n, tol=0.05)
            lvl = round((n_p - 1) / 2 - sgn * u)  # 0 for the port farthest out on this star
            y_run = (y_px0 - lv[lvl]) * um_px
            x_v = cx + u * x_pitch_io
            # shoulder of this port
            sn, cs = math.sin(phi), math.cos(phi)
            rr = r_fpr - y_p
            hw = d_io * (rr + l_shallow) / rr / 2
            r1 = l_shallow
            cen = (q[0] + r1 * sn, q[1] - r1 * cs)
            r2 = r1 + t_io
            end = (q[0] + r2 * sn, q[1] - r2 * cs)
            tp.poly([(cen[0] - hw * cs, cen[1] - hw * sn), (cen[0] + hw * cs, cen[1] + hw * sn), (end[0] + w_n / 2 * cs, end[1] + w_n / 2 * sn), (end[0] - w_n / 2 * cs, end[1] - w_n / 2 * sn)], "si", "shallow shoulder, deep-shallow transition at the port", src_tr, layer="slab", alpha=0.3, lod=0.8)
            # radial until the line either reaches its vertical or has to turn straight into its level
            turn = sgn * 90.0  # final bend from vertical to outward horizontal
            lat = math.copysign(r_b * (1 - cs), phi)
            s_v = (x_v - q[0] - lat) / sn
            y_after = q[1] - s_v * cs - r_b * abs(sn)
            if s_v > 0 and y_after > y_run + r_b:
                rt.straight(s_v).arc(r_b, -math.degrees(phi))
                rt.straight(rt.pos[1] - (y_run + r_b)).arc(r_b, turn)
            else:
                sweep = (0.0 if sgn > 0 else -180.0) - head  # lean straight into the outward run
                probe = Route((0.0, 0.0), head, w_n, tol=0.05).arc(r_b, sweep)
                rt.straight((q[1] + probe.pos[1] - y_run) / cs).arc(r_b, sweep)
            x_b = 92.0 + lvl * 9.2  # Fig. 4: where each run turns up, 9.2 um per level
            if x_b + 2.5 < x_stop[sgn]:
                rt.straight(max(x_b - abs(rt.pos[0]), 0.0))
                rt.arc(r_b, sgn * diag)
                rt.straight(max((x_stop[sgn] - abs(rt.pos[0])) / math.cos(math.radians(diag)), 0.0))
            else:
                rt.straight(x_stop[sgn] - abs(rt.pos[0]))
            draw(f"port {sgn} {k}", rt, ("input" if sgn < 0 else "output") + f" waveguide {k + 1} of {n_p} (truncated)", src_io)
        # dummies: left star only, the one star with a detail in the paper
        if sgn < 0:
            for j in range(n_dummy):
                for side in (-1.0, 1.0):
                    off = side * ((n_p - 1) / 2 + 1 + j) * d_io
                    q, phi = port_xy(cx, y_p, off)
                    dm = Route(q, -90.0 + math.degrees(phi), w_n, tol=0.05).straight(l_dummy)
                    why = fig("Fig. 4 lower detail", "shallow line with no deep-etch tip", "10 %") if side < 0 else assumed("cut by the frame of the detail: taken as the mirror of the 3 lines seen on the other side")
                    draw(f"dummy {side} {j}", dm, "shallow line ending in the field, no connection", why)

    # no waveguide polygon may touch another: a bucket grid of edges, then a point-in-polygon test for one inside another
    def crossings() -> list[tuple[str, str]]:
        def seg_hit(a: Pt, b: Pt, c2: Pt, d: Pt) -> bool:
            def o(p: Pt, q: Pt, r: Pt) -> float:
                return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

            def on(p: Pt, q: Pt, r: Pt) -> bool:  # r, collinear with pq, within pq
                return min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= r[1] <= max(p[1], q[1])

            d1, d2, d3, d4 = o(a, b, c2), o(a, b, d), o(c2, d, a), o(c2, d, b)
            if d1 * d2 < 0 and d3 * d4 < 0:
                return True
            return (d1 == 0 and on(a, b, c2)) or (d2 == 0 and on(a, b, d)) or (d3 == 0 and on(c2, d, a)) or (d4 == 0 and on(c2, d, b))

        def inside(p: Pt, poly: list[Pt]) -> bool:
            hit = False
            for k in range(len(poly)):
                a, b = poly[k], poly[(k + 1) % len(poly)]
                if (a[1] > p[1]) != (b[1] > p[1]) and p[0] < a[0] + (p[1] - a[1]) / (b[1] - a[1]) * (b[0] - a[0]):
                    hit = not hit
            return hit

        cell = 8.0
        buckets: dict[tuple[int, int], list[tuple[int, Pt, Pt]]] = {}
        for n, (_, poly) in enumerate(wgs):
            for k in range(len(poly)):
                a, b = poly[k], poly[(k + 1) % len(poly)]
                x0, x1 = sorted((a[0], b[0]))
                y0, y1 = sorted((a[1], b[1]))
                for ix in range(int(x0 // cell), int(x1 // cell) + 1):
                    for iy in range(int(y0 // cell), int(y1 // cell) + 1):
                        buckets.setdefault((ix, iy), []).append((n, a, b))
        bad: set[tuple[int, int]] = set()
        for segs in buckets.values():
            for ka in range(len(segs)):
                na, a, b = segs[ka]
                for kb in range(ka + 1, len(segs)):
                    nb, c2, d = segs[kb]
                    if na != nb and wgs[na][0] != wgs[nb][0] and (min(na, nb), max(na, nb)) not in bad and seg_hit(a, b, c2, d):
                        bad.add((min(na, nb), max(na, nb)))
        for na, (ga, pa) in enumerate(wgs):
            for nb, (gb, pb) in enumerate(wgs):
                if ga != gb and na != nb and (min(na, nb), max(na, nb)) not in bad:
                    xa, ya = [p[0] for p in pa], [p[1] for p in pa]
                    xb, yb = [p[0] for p in pb], [p[1] for p in pb]
                    if min(xb) <= min(xa) and max(xa) <= max(xb) and min(yb) <= min(ya) and max(ya) <= max(yb) and inside(pa[0], pb):
                        bad.add((min(na, nb), max(na, nb)))
        return [(wgs[a][0], wgs[b][0]) for a, b in sorted(bad)]

    hits = crossings()
    if hits:
        raise ValueError(f"{len(hits)} waveguide polygon pairs intersect: {sorted(set(hits))[:12]}")
    c.check(f"waveguide polygon pairs intersecting, of {len(wgs)} polygons", 0.0, 0.0)

    x_out = x_in0 + (n_arm - 1) * px
    y_out = y_tops[-1]
    pitch = [y_tops[i + 1] - y_tops[i] for i in range(n_arm - 1)]
    c.check("level pitch, 5 shortest arms, solved um, against Fig. 4 (rows 516 to 606)", sum(pitch[:5]) / 5, 90.0 / 5 * um_px, 0.04)
    c.check("level pitch, 8 longest arms, solved um, against Fig. 4 (rows 18 to 144)", sum(pitch[-8:]) / 8, 126.0 / 8 * um_px, 0.04)
    c.check("group index from FSR and delta L, 1.55 um, against the lower end of the stated 4-4.7", 1.55**2 / (fsr * dl), 4.0, 0.03)
    n_s = 2.85  # slab index of 220 nm Si, not stated
    c.check("I/O pitch from the grating equation (n_s 2.85, not stated) against the lower detail um", (1550 / c.num("m4")) * c.num("m3") * 1e-3 / (n_s * delta), d_io, 0.08)
    c.check("line pitch at the deep tips, from the radial fan of radius 105 um, against the 16.8 px of the lower detail um", d_io * (r_fpr + l_shallow) / r_fpr, 16.8 * 0.148, 0.03)
    c.check("drawn height um, stars to top, against the stated 500", y_out, 500.0, 0.05)

    tp.dim("h", -x_out, x_out, y_out, px=14, ext=(y_out, y_out), text=f"{2 * x_out:.0f} um", src=fig("Fig. 4", "outer arm against the 100 um bar", "2 %"))
    tp.dim("v", 0.0, y_out, x_out, px=16, ext=(x_out, x_out), text=f"{y_out:.0f} um", src=fig("Fig. 4", "star axis origin to the top arm against the 100 um bar", "4 %"))
    tp.label((-x_c, r_fpr / 2), "star", anchor="middle")
    tp.label((x_c, r_fpr / 2), "star", anchor="middle")
    tp.label((-x_stop[-1.0], 12.0), "input ports", anchor="start")
    tp.label((x_stop[1.0], 12.0), "output ports", anchor="end")
    tp.note("Bundles continue up and outwards to the couplers: truncated at the frame of Fig. 4.")
    tp.note(f"delta L = 2(px + py) = {dl:.1f} um from the figure; arm lengths solved to it. No delta L is printed for this AWG. Stated footprint: 500 x 200 um.")
    c.thumb = {"view": "top", "window": [-122, 178, 122, 276]}

    fan = c.view("fan", "detail: fan bends, deep-shallow transition and the shortest arm", like="top", window=(-75, 160, 25, 230))
    fan.dim("h", -x_in0, x_in0, y_top0, px=12, ext=(y_top0, y_top0), text=f"{2 * x_in0:.0f} um", src=fig("Fig. 4", "legs of the shortest arm, 20 px, against the 100 um bar", "1 um"))
    fan.label((-x_c, r_s), "deep-shallow boundary", anchor="middle", dy=16, tip="shallow field below, deep etched above; the wedges between shoulders are the deep etch tips of Fig. 4")
    fan.note("Transition length is the midpoint of the row's 15-30 um; Fig. 4 array detail shows 20 um.")

    cor = c.view("corner", "detail: outer corners, 0.8 um straights tapering to 0.5 um in the 4 um bends", like="top", window=(-x_out - 3, y_out - 34, -x_out + 37, y_out + 3))
    cor.label((-x_out + r_b, y_out), "bend radius", anchor="start", dx=8, dy=-6, row_id="m6")
    cor.note("Fig. 4 corner detail labels 0.8 um and 0.5 um; taper length read as 5 to 8 um against its 5 um bar.")

    star = c.view("star", "detail: left star, I/O apertures, dummies, deep-etch wedges, nested routing", like="top", window=(-x_c - 62, -52, -x_c + 28, 112))
    star.note("Star outline is not resolved in the SEM (dashed). Inferred: its centre where the radial array lines of the array detail converge, its radius 105 +- 15 um where the I/O lines of the lower detail converge, confirmed by the line pitch growing 2.2 to 2.5 um over 12.6 um.")
    pl = c.view("ports", "detail: left star ports as the lower detail of Fig. 4 shows them", like="top", window=(-x_c - 26, -46, -x_c + 26, 8))
    pl.note("16 shallow positions at 2.2 um: 14 lines are in the frame of the detail, 3 on the left end with no deep tip; the 3 on the right are taken as their mirror (dashed). 10 connect to deep wires: the peak count across the bundle in the main panel is 10.")
    pl.note("At this resolution the SEM does not tell whether a bright shallow line is a wire or the trench between wires; drawn as wires.")
    pr = c.view("ports_r", "detail: right star, 16 outputs, nested: the rightmost turns first and highest", like="top", window=(x_c - 30, -62, x_c + 62, 2))
    pr.note("No detail of this star in the paper: dummies not read, none drawn. 16 verticals counted in the main panel, equal to the row.")

    x = c.view("xsec", "cross-section: broadened arm in the deep-etched array", "xsec")
    span = 1.6
    x.rect(-span, -box - 0.4, span, -box, "si", "Si wafer", assumed("wafer: truncated"), alpha=0.5, layer="substrate")
    x.rect(-span, -box, span, 0.0, "sio2", "oxide buffer", stated("p.1 Sec. II", "1 um oxide"), layer="oxide")
    x.rect(-w_b / 2, 0.0, w_b / 2, t_si, "si", "Si wire", stated("p.1 Sec. II", "220 nm") + stated("Fig. 4 detail", "0.8 um"), layer="waveguide")
    x.dim("h", -w_b / 2, w_b / 2, t_si, px=14, ext=(t_si, t_si), text="0.8 um", src=stated("Fig. 4 detail", "broadened wire"))
    x.dim("v", 0.0, t_si, w_b / 2, px=18, ext=(w_b / 2, w_b / 2), text="220 nm", src=stated("p.1 Sec. II"))
    x.dim("v", -box, 0.0, -span, px=-14, ext=(-span, -span), text="1 um", src=stated("p.1 Sec. II"))
    x.note("No top cladding is stated for these devices; none drawn.")

    x2 = c.view("xsec2", "cross-section: waveguide in the shallow field near a star", "xsec")
    x2.rect(-span, -box - 0.4, span, -box, "si", "Si wafer", assumed("wafer: truncated"), alpha=0.5, layer="substrate")
    x2.rect(-span, -box, span, 0.0, "sio2", "oxide buffer", stated("p.1 Sec. II", "1 um oxide"), layer="oxide")
    x2.rect(-span, 0.0, span, t_si - etch, "si", "shallow-etched Si, 150 nm left", row("m7") + stated("p.1 Sec. II", "220 nm"), layer="slab")
    x2.rect(-w_ap / 2, 0.0, w_ap / 2, t_si, "si", "waveguide near the aperture", row("m7") + assumed("width near the aperture not stated"), layer="waveguide")
    x2.dim("v", t_si - etch, t_si, w_ap / 2, px=18, ext=(w_ap / 2, w_ap / 2), row_id="m7")
    x2.dim("v", 0.0, t_si, -w_ap / 2, px=-16, ext=(-w_ap / 2, -w_ap / 2), text="220 nm", src=stated("p.1 Sec. II"))
    return c
