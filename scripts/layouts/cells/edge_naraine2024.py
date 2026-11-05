"""Naraine 2024 SiO2-clad SiN inverse taper, 350 nm tip, 100 um long, Applied Nanotools platform (Sec. II-B, Sec. III-A, Sec. III-B, Table III).

The paper shows no image of this strip coupler (the only coupler SEM, Fig. 8(a), is the SWG variant, another device): the geometry
is entirely in the text. Waveguide widths are at half height with an 83.5 deg sidewall. The facet is RIE-etched through cladding,
SiN and BOX, then the Si handle is etched back 250 um by DRIE so a fiber reaches the facet.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, assumed, circle, row, stated  # noqa: E402

ID = "cmp_lit_naraine2024_ec_tip350"


def _solve(f, a: float, b: float) -> float:  # type: ignore[no-untyped-def]
    for _ in range(80):
        m = (a + b) / 2
        if f(m) > 0:
            a = m
        else:
            b = m
    return (a + b) / 2


def slab_te0(n_core: float, n_low: float, n_top: float, t_um: float, lam_um: float) -> float:
    """TE0 index of the vertical three-layer slab."""
    k0 = 2 * math.pi / lam_um

    def f(n: float) -> float:
        kt = k0 * math.sqrt(n_core**2 - n**2)
        return kt * t_um - math.atan(k0 * math.sqrt(n**2 - n_low**2) / kt) - math.atan(k0 * math.sqrt(n**2 - n_top**2) / kt)

    return _solve(f, max(n_low, n_top) + 1e-6, n_core - 1e-6)


def slab_tm_like(n_core: float, n_clad: float, w_um: float, lam_um: float) -> float:
    """Lateral step of the effective-index method: E normal to the walls, symmetric cladding."""
    k0 = 2 * math.pi / lam_um

    def f(n: float) -> float:
        kt = k0 * math.sqrt(n_core**2 - n**2)
        return kt * w_um - 2 * math.atan((n_core / n_clad) ** 2 * k0 * math.sqrt(n**2 - n_clad**2) / kt)

    return _solve(f, n_clad + 1e-6, n_core - 1e-6)


def build() -> Cell:
    c = Cell(
        ID,
        ["Sec. II-A (film, oxide)", "Sec. II-B (cladding, facet etch, DRIE)", "Sec. III-A (sidewall, half-height width)", "Sec. III-B (taper, MFD)", "Fig. 2(d)", "Fig. 5(b)", "Table I", "Table III", "Fig. 8(a) read: SWG coupler, not this device; no image of this strip coupler in the paper"],
        "Linear inverse taper 0.75 to 0.35 um over 100 um to an RIE facet, 250 um DRIE recess in the handle, trapezoid core; text-defined",
    )
    tip = c.um("m5")
    l_t = c.um("m6")
    w_wg = c.um("m7")
    t = c.um("m8")
    t_box = 4.5  # Sec. II-A
    t_clad = 3.0  # Sec. II-B
    d_drie = 250.0  # Sec. II-B
    side = 83.5  # Sec. III-A, sidewall angle
    mfd = 2.5  # Sec. III-B, lensed fiber at 1550 nm; the row condition states the same
    inset = (t / 2) / math.tan(math.radians(side))  # half height to top or bottom edge
    src_film = stated("Sec. II-A", "LPCVD SiN on 4.5 um thermal SiO2") + row("m8")
    src_box = stated("Sec. II-A", "4.5 um thermal SiO2")
    src_clad = stated("Sec. II-B", "3 um PECVD SiO2")
    src_facet = stated("Sec. II-B", "cladding, SiN and BOX RIE-etched at the facet; Si handle DRIE 250 um deep")
    src_trench = src_facet + assumed("recess reach beyond the facet not stated; the handle is drawn flush with the facet")

    # x = 0 at the facet, the chip on the -x side
    x_wg = -l_t - 25.0
    x_tr = 35.0
    top = c.view("top", "plan: inverse taper to the etched facet, true scale")
    yb = 8.0
    top.rect(x_wg, -yb, 0, yb, "sio2", "SiO2 cladding over the chip", src_clad, layer="oxide", alpha=0.3)
    top.rect(0, -yb, x_tr, yb, "air", "recess: handle etched 250 um, oxide removed", src_trench, layer="trench", alpha=0.4)
    top.poly([(-l_t, -w_wg / 2), (0, -tip / 2), (0, tip / 2), (-l_t, w_wg / 2)], "sin", "linear inverse taper", row("m5", "m6", "m7") + stated("Sec. III-B", "linearly and inversely tapered until the chip edge"), layer="waveguide")
    top.rect(x_wg, -w_wg / 2, -l_t, w_wg / 2, "sin", "0.75 um straight, truncated", row("m7"), layer="waveguide")
    top.line([(0, -yb), (0, yb)], "RIE facet", src_facet)
    top.dim("h", -l_t, 0, w_wg / 2, px=22, ext=(w_wg / 2, tip / 2), row_id="m6")
    top.label((x_tr, 0), "lensed fiber side", anchor="end", dy=-10, tip="Tapered lensed fiber with 2.5 um spot at 1550 nm")
    top.label((x_wg, 0), "0.75 um", anchor="start", dy=-10, row_id="m7")
    top.note("Test structure: two couplers joined by a 0.75 um straight; straight truncated here.")
    top.note("A 0.4 um width change over 100 um: half angle 0.11 deg. The zoom views show it.")

    g = c.view("tip", "detail: the 350 nm tip at the facet", like="top", window=(-13, -1.6, 3, 1.6))
    g.dim("v", -tip / 2, tip / 2, 0, px=-10, ext=(0, 0), row_id="m5")
    g.note("Tip width sits at half height, the designed width of the platform (Sec. III-A).")
    w = c.view("start", "detail: start of the taper, 0.75 um straight", like="top", window=(-l_t - 10, -1.6, -l_t + 6, 1.6))
    w.dim("v", -w_wg / 2, w_wg / 2, -l_t - 5, px=-8, ext=(-l_t - 5, -l_t - 5), row_id="m7")

    # long section at true scale, shown twice: the stack, and the deep recess
    s = c.view("section", "section along the taper at the facet, true scale", "xsec", window=(-26, -t_box - 3.5, 12, t + t_clad + 1.2))
    y_top = t + t_clad
    y_floor = -t_box - d_drie
    x_far = -l_t - 25.0
    y_chip = y_floor - 40.0
    s.rect(x_far, y_chip, 0, -t_box, "si", "Si handle (bottom truncated)", stated("Sec. II-A", "4-inch Si wafer") + assumed("wafer thickness not stated: truncated 40 um below the recess floor"), layer="substrate", alpha=0.8)
    s.rect(0, y_chip, x_tr, y_floor, "si", "Si handle at the recess floor", src_facet + assumed("recess reach not stated"), layer="substrate", alpha=0.8)
    s.rect(x_far, -t_box, 0, 0, "sio2", "thermal SiO2", src_box, layer="oxide")
    s.rect(x_far, 0, 0, y_top, "sio2", "PECVD SiO2 cladding", src_clad, layer="oxide", alpha=0.55)
    s.rect(x_far, 0, 0, t, "sin", "SiN core", src_film, layer="waveguide")
    s.line([(0, y_top + 0.4), (0, -t_box)], "RIE facet", src_facet)
    s.line([(0, t / 2), (x_tr, t / 2)], "fiber axis", assumed("fiber axis at the core centre"))
    s.dim("v", -t_box, 0, -18, px=-8, ext=(-18, -18), text="4.5 um", src=src_box)
    s.dim("v", 0, t, -20.8, px=-2, ext=(-20.8, -20.8), row_id="m8")
    s.dim("v", t, y_top, -18, px=-8, ext=(-18, -18), text="3 um", src=src_clad)
    s.label((-7, 2.3), "PECVD SiO2", anchor="middle")
    s.label((-7, -2.2), "thermal SiO2", anchor="middle")
    s.label((-7, -t_box - 1.6), "Si handle", anchor="middle")
    s.label((6, t / 2), "recess", anchor="middle", dy=-10, tip="Handle etched 250 um below the BOX, Sec. II-B")
    s.note("Facet plane through cladding, SiN and BOX in one RIE step, so the core ends flush with the oxide.")

    d = c.view("recess", "section: the 250 um handle recess and a 125 um fiber, true scale", "xsec", like="section", window=(-130, y_chip, 95, 90))
    r_f = 62.5
    xf0 = 2.0
    src_fib = assumed("125 um glass diameter: standard value, not stated; lensed-fiber nose not drawn")
    d.line([(xf0, t / 2 - r_f), (90, t / 2 - r_f)], "fiber outline, lower edge", src_fib)
    d.line([(xf0, t / 2 + r_f), (90, t / 2 + r_f)], "fiber outline, upper edge", src_fib)
    d.line([(xf0, t / 2 - r_f), (xf0, t / 2 + r_f)], "fiber end", src_fib)
    d.dim("v", y_floor, -t_box, x_tr, px=10, ext=(0, 0), text="250 um", src=src_facet)
    d.note("The 250 um depth clears the fiber radius so the fiber end can reach the facet; the top surface here is the chip's, the fiber is free above it.")

    def xsec(vid: str, title: str, w_half: float, row_id: str) -> None:
        x = c.view(vid, title, "xsec")
        xw = 3.6
        x.rect(-xw, -t_box - 0.8, xw, -t_box, "si", "Si handle (truncated)", stated("Sec. II-A", "Si wafer") + assumed("truncated"), layer="substrate", alpha=0.8)
        x.rect(-xw, -t_box, xw, 0, "sio2", "thermal SiO2", src_box, layer="oxide")
        x.rect(-xw, 0, xw, y_top, "sio2", "PECVD SiO2 cladding", src_clad, layer="oxide", alpha=0.55)
        x.poly([(-w_half - inset, 0), (w_half + inset, 0), (w_half - inset, t), (-w_half + inset, t)], "sin", "SiN core, 83.5 deg sidewall", src_film + row(row_id) + stated("Sec. III-A", "83.5 deg sidewall, width at half height"), layer="waveguide")
        x.dim("h", -w_half, w_half, t / 2, px=26, ext=(t / 2, t / 2), row_id=row_id)
        x.dim("v", 0, t, xw, px=8, ext=(w_half, w_half), row_id="m8")
        x.dim("v", -t_box, 0, xw, px=8, ext=(xw, xw), text="4.5 um", src=src_box)
        x.dim("v", t, y_top, xw, px=8, ext=(xw, xw), text="3 um", src=src_clad)

    xsec("facet", "cross-section at the facet: 350 nm tip, 2.5 um fiber spot", tip / 2, "m5")
    c.views[-1].line(circle((0, t / 2), mfd / 2, tol=0.02) + [(mfd / 2, t / 2)], "lensed fiber mode, 2.5 um MFD", stated("Sec. III-B", "MFD 2.5 um at 1550 nm") + assumed("vertical alignment of the fiber is in no source: centred on the core"))
    c.views[-1].label((0, t / 2 + mfd / 2), "2.5 um MFD", anchor="middle", dy=-5, tip="Lensed fiber mode of the row's condition; simulated overlap loss 0.32 dB TE, 0.35 dB TM")
    c.views[-1].note("The mode circle is dashed: its size is stated, its vertical alignment is in no source. Width at half height of the trapezoid (Sec. III-A). Simulated with square sidewalls in the paper; the angle is named as a reason for the shift of the measured optimum.")
    xsec("wg", "cross-section at the 0.75 um straight", w_wg / 2, "m7")

    # no check: the one independent test, the stack and width against the Fig. 2(d) mode index, does not close (note below)
    n_core, n_bot, n_clad = 1.997, 1.444, 1.47  # n SiN Sec. II-A at 1550 nm, n clad Sec. III-A; n thermal SiO2 assumed
    n_s = slab_te0(n_core, n_bot, n_clad, t, 1.55)
    n_eim = slab_tm_like(n_s, n_clad, w_wg, 1.55)
    c.views[-1].note(f"Not closed: effective-index method for this 0.75 um x 400 nm core at 1550 nm gives TE0 {n_eim:.3f}, Fig. 2(d) reads 1.60 +-0.01, so {n_eim - 1.60:.3f} high; the method is too rough to confirm the stack.")
    c.thumb = {"view": "section", "window": [-26.0, -t_box - 2.0, 12.0, y_top + 0.8]}
    return c
