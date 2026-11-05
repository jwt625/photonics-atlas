"""OFC 2026 Tu2D.4, PIC100G back-side SiN edge coupler: text and captions only, images not available.

Text fixes: 200 nm SiN strip for the inverted taper, a 200-to-400 nm SiN transition to the 400 nm strip at the bottom SiN level,
SiN on the backside of a 300 nm SOI / 200 nm BOX wafer, bonded on an HR carrier through thick planar oxide so the reconstructed BOX
under the waveguide exceeds 5 um; a BEOL cavity at the edge; FEOL / BEOL SiN removed locally. Everything else is dashed: no plan
dimension of this coupler is stated (the 150-200 nm tip is a general requirement in Sec. 1, not this design).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, assumed, row, stated  # noqa: E402

ID = "cmp_ofc2026_tu2d4_sin_edge_coupler"


def build() -> Cell:
    c = Cell(
        ID,
        ["text and captions only: Sec. 1", "Sec. 2 (process)", "Sec. 3", "Table 1", "captions of Fig. 1, Fig. 2, Fig. 3; images not available"],
        "Back-side SiN coupler: 200 nm inverted taper, transition down to the 400 nm strip, > 5 um reconstructed BOX on the carrier; plan dimensions assumed",
    )
    t_rbox = c.um("m5")
    t_upper, t_lower = 0.200, 0.400  # Sec. 2: edge coupler strip and bottom-level strip
    t_si, t_oxbox = 0.300, 0.200  # Sec. 2: SOI and original BOX
    # no value of these in the text
    tip = 0.175  # mid of the 150-200 nm of Sec. 1, which the paper gives as a general requirement
    w_upper = 0.70
    w_lower = 0.70
    l_taper, l_trans = 100.0, 30.0
    gap = 0.15  # between SiN levels
    t_top = 2.5  # over the upper SiN

    no_plan = assumed("text only: no plan dimension of this coupler stated, shape drafted")
    src_upper = stated("Sec. 2", "edge coupler made of the 200 nm SiN strip") + no_plan
    src_lower = stated("Sec. 2", "400 nm SiN strip at the bottom level, adiabatic to Si") + no_plan
    src_trans = stated("Sec. 3", "200 nm to 400 nm transition in SiN; Fig. 3(a) caption") + no_plan

    top = c.view("top", "plan: inverted taper and 200-to-400 nm SiN transition (dashed: no plan dimension in the text)")
    x_t = l_taper
    x_tr = l_taper + l_trans
    x_end = x_tr + 25.0
    yb = 7.0
    top.rect(0, -yb, x_end, yb, "sio2", "oxide over the SiN, local FEOL / BEOL SiN removed", stated("Sec. 2", "parasitic FEOL and BEOL SiN removed locally") + no_plan, layer="oxide", alpha=0.25)
    top.rect(-18, -yb, 0, yb, "air", "BEOL cavity at the die edge", stated("Sec. 2", "cavity for wafer-level test or sawing, keeping an optical interface") + assumed("cavity extent not stated"), layer="trench", alpha=0.4)
    top.poly([(x_t, -w_lower / 2 * 0.2), (x_tr, -w_lower / 2), (x_end, -w_lower / 2), (x_end, w_lower / 2), (x_tr, w_lower / 2), (x_t, w_lower / 2 * 0.2)], "sin", "400 nm SiN strip, bottom level, opens under the upper strip", src_lower + src_trans, layer="waveguide", alpha=0.75)
    top.poly([(0, -tip / 2), (x_t, -w_upper / 2), (x_tr, -w_upper / 2 * 0.2), (x_tr, w_upper / 2 * 0.2), (x_t, w_upper / 2), (0, tip / 2)], "sin", "200 nm SiN strip, upper level: inverted taper, then counter-taper of the transition", src_upper, layer="overlay")
    top.line([(0, -yb), (0, yb)], "facet at the cavity", stated("Sec. 2", "coupling from the die edge") + assumed("position in the cavity not stated"))
    top.label((x_t / 2, 0), "inverted taper", anchor="middle", dy=-14, tip="Sec. 3: taper plus transition is the main loss; simulated mode overlap below 0.15 dB")
    top.label((x_t + l_trans / 2, 0), "transition", anchor="middle", dy=-14, tip="200 to 400 nm SiN, Fig. 3(a) caption")
    top.label((x_end, 0), "400 nm SiN", anchor="end", dy=-14, tip="Then an adiabatic transition to Si; truncated")
    top.label((0, yb), "facet", anchor="middle", dy=-6)
    top.note("Text and captions only; images not available. The taper, transition and widths are drafted: only their existence and the two SiN thicknesses are in the text.")
    top.note("Whether the two levels overlap as a counter-taper or join another way is not stated.")
    g = c.view("tip", "detail: inverted taper tip at the die edge", like="top", window=(-5, -1.3, 18, 1.3))
    g.note("Tip width is dashed: Sec. 1 gives 150-200 nm as a general requirement; the value for this coupler is not stated.")

    # stack, from the carrier up: bonded wafer is flipped, so Si is below its BOX and SiN sits on the BOX side
    y_si1 = t_si
    y_box1 = y_si1 + t_oxbox
    y_low1 = y_box1 + t_lower
    y_up0 = y_low1 + gap
    y_up1 = y_up0 + t_upper
    y_tp = y_up1 + t_top
    y_carrier = -t_rbox

    x = c.view("xsec", "cross-section in the inverted taper: stack from the HR carrier up", "xsec")
    xw = 4.0
    x.rect(-xw, y_carrier - 1.6, xw, y_carrier, "si", "HR carrier (truncated)", stated("Sec. 2", "HR substrate as carrier") + assumed("thickness not stated"), layer="substrate", alpha=0.7)
    x.rect(-xw, y_carrier, xw, 0.0, "sio2", "reconstructed BOX: bonded thick planar oxide and the flipped BEOL dielectric", row("m5") + stated("Sec. 1-2", "above 5 um between waveguide and substrate"), layer="oxide")
    x.rect(-xw, 0.0, xw, y_box1, "sio2", "level of the 300 nm Si and 200 nm original BOX", stated("Sec. 2", "300 nm SOI, 200 nm BOX") + assumed("no Si drawn under the coupler: its presence there is not stated"), layer="oxide", alpha=0.75)
    x.rect(-xw, y_box1, xw, y_tp, "sio2", "oxide around the SiN levels", no_plan, layer="oxide", alpha=0.5)
    x.rect(-w_upper / 2, y_up0, w_upper / 2, y_up1, "sin", "200 nm SiN strip", src_upper, layer="overlay")
    x.dim("v", y_carrier, 0.0, -xw, px=-10, ext=(-xw, -xw), row_id="m5")
    x.dim("v", y_up0, y_up1, w_upper / 2, px=14, ext=(w_upper / 2, w_upper / 2), text="200 nm", src=stated("Sec. 2", "edge coupler strip"))
    x.note("The bar is the stated lower bound, 5 um, carrier to the Si level; the text says only between waveguide and substrate, so the real value is above this.")
    x.note("Above it the 300 nm Si / 200 nm BOX level, 0.5 um, dashed: no Si is drawn under the coupler, its presence there is not stated.")

    v = c.view("stack", "section at the die edge, from the carrier up, true scale", "xsec", window=(-14, y_carrier - 1.0, 28, y_tp + 0.8))
    x_a, x_b = -18.0, x_end
    v.rect(x_a, y_carrier - 1.6, x_b, y_carrier, "si", "HR carrier (truncated)", stated("Sec. 2", "HR substrate as carrier") + assumed("thickness not stated"), layer="substrate", alpha=0.7)
    v.rect(0, y_carrier, x_b, 0.0, "sio2", "reconstructed BOX", row("m5"), layer="oxide", alpha=0.7)
    v.rect(0, 0.0, x_b, y_box1, "sio2", "level of the 300 nm Si and 200 nm original BOX", stated("Sec. 2", "300 nm SOI, 200 nm BOX") + assumed("no Si drawn under the coupler: its presence there is not stated"), layer="oxide", alpha=0.7)
    v.rect(0, y_box1, x_b, y_tp, "sio2", "oxide around and above the SiN", no_plan, layer="oxide", alpha=0.45)
    v.rect(x_a, y_carrier, 0, y_tp, "air", "BEOL cavity at the die edge", stated("Sec. 2", "BEOL cavity") + assumed("depth and extent not stated; the floor is drawn at the carrier"), layer="trench", alpha=0.45)
    v.rect(0, y_up0, x_tr, y_up1, "sin", "200 nm SiN strip", src_upper, layer="overlay")
    v.rect(x_t, y_box1, x_end, y_low1, "sin", "400 nm SiN strip at the bottom level", src_lower, layer="waveguide")
    v.line([(0, y_carrier), (0, y_tp)], "facet", stated("Sec. 2", "coupling from the die edge") + assumed("position in the cavity not stated"))
    v.dim("v", y_carrier, 0.0, 22, px=-6, ext=(22, 22), row_id="m5")
    v.label((12, y_up1), "200 nm SiN", anchor="middle", dy=-6)
    v.label((-7, 1.0), "cavity", anchor="middle")
    v.label((9, -2.5), "reconstructed BOX", anchor="middle", tip="Thick planar oxide bonded to the carrier, plus the flipped BEOL")
    v.note("The bar is the stated lower bound, 5 um, carrier to the Si level. The 400 nm SiN at the bottom SiN level (Sec. 2) starts further along, outside this window; the 200 nm strip above it is inferred; oxide above the SiN and the gap are assumed.")

    w = c.view("trans", "section at the transition: the 400 nm strip starts below the 200 nm strip", "xsec", like="stack", window=(x_t - 12, y_carrier - 1.0, x_end, y_tp + 0.8))
    w.label((x_t - 6, y_up1), "200 nm SiN", anchor="middle", dy=-6)
    w.label((x_end - 12, y_low1), "400 nm SiN", anchor="middle", dy=12)
    d = c.view("levels", "detail: SiN levels in the transition", "xsec", like="stack", window=(x_t - 3, y_box1 - 0.25, x_t + 5, y_up1 + 0.35))
    d.dim("v", y_box1, y_low1, x_t + 3, px=10, ext=(x_t + 3, x_t + 3), text="400 nm", src=stated("Sec. 2", "bottom-level strip"))
    d.dim("v", y_up0, y_up1, x_t - 1.5, px=-10, ext=(x_t - 1.5, x_t - 1.5), text="200 nm", src=stated("Sec. 2", "edge coupler strip"))

    c.thumb = {"view": "stack", "window": [-12.0, y_carrier - 0.5, 18.0, y_tp + 0.5]}
    return c
