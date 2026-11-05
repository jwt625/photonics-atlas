"""OFC 2026 Tu2D.4: TiN thermal phase shifter of the STMicroelectronics PIC100G back-side platform. Text only: Fig. 1, Fig. 2 not available.

What the text fixes: a TiN resistance sits between metal 1 and metal 2, in the BEOL built on the front of a 300 nm SOI on
200 nm BOX; via 1, metal 2, via 2 and metal 3 follow; thick planar oxide; bonded to a high-resistivity carrier; handle removed;
SiN and pads built on the back. So in the finished chip the BEOL lies below the silicon: carrier, thick oxide above 5 um with
the metals in it, Si, original BOX. The heater is under the waveguide side, between it and the carrier, and the paper credits
the very thick BOX for the 15.5 mW. Plan, heater length and width, waveguide type and all level heights are not stated: every
one of those is assumed and carries no dimension. Same orientation as the Si / SiN transition cell of this paper.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, Route, assumed, stated  # noqa: E402

ID = "cmp_ofc2026_tu2d4_tin_heater_ps"


def build() -> Cell:
    c = Cell(ID, ["Sec. 2 (text only)", "Sec. 3, Table 2 (text only)", "Fig. 1, Fig. 2 not available"], "Finished-chip stack: carrier, thick oxide with M3, M2, TiN, M1, Si, 200 nm BOX; plan view and level heights assumed")
    t_si, t_box, t_thick = 0.3, 0.2, 5.0  # Sec. 2: 300 nm SOI, 200 nm BOX; Sec. 1: reconstructed BOX above 5 um, drawn at the bound
    # drafting values, no labels
    length, w_wg, w_h, stub, lead_w = 60.0, 0.5, 2.0, 12.0, 3.0
    clad = 2.0
    why_plan = assumed("no plan information in the text: waveguide type, heater length, width, offset and lead routing are drafted")

    top = c.view("top", "top view: assumed, no dimension is from the source")
    top.rect(-length / 2 - stub - 2, -14, length / 2 + stub + 2, 14, "sio2", "oxide", assumed("extent drafted"), layer="oxide", alpha=0.6)
    top.route(Route((-length / 2 - stub, 0.0), 0.0, w_wg).straight(length + 2 * stub), "si", "Si waveguide; type not stated", why_plan, layer="waveguide")
    top.rect(-length / 2, -w_h / 2, length / 2, w_h / 2, "metal", "TiN heater, between M1 and M2", stated("Sec. 2", "TiN resistance between metal 1 and metal 2") + why_plan, layer="metal", alpha=0.6)
    for s in (-1, 1):
        x0, x1 = sorted((s * length / 2, s * (length / 2 - lead_w)))
        top.rect(x0, -w_h / 2, x1, 12.0, "metal", "metal lead to the TiN", why_plan, layer="metal")
    top.label((0.0, w_h / 2), "TiN heater", dy=-8)
    top.label((-length / 2 - stub, 0.0), "Si waveguide (type not stated)", anchor="start", dy=-8)
    top.note("Text only: no figure was available and the text gives no plan dimension. This plan view is a placeholder for the words 'TiN heater'; do not read a length or a width from it.")
    top.note("Seen from the SiN side of the finished chip: the heater lies below the Si.")
    top.label((0.0, -8.0), "P_pi", row_id="m1", tip="Table 2, O band at 25 C")
    c.thumb = {"view": "xsec", "window": [-6.5, -t_thick - 0.5, 6.5, t_si + t_box + 0.4]}

    half = 8.0
    x = c.view("xsec", "cross-section, finished chip orientation: carrier below, heater between M1 and M2 under the Si", "xsec", window=(-half, -t_thick - 1.4, half, t_si + t_box + clad + 0.2))
    z_m1, z_tin, z_m2, z_m3 = -0.65, -1.15, -1.75, -2.75  # underside of each level: order is stated, heights are drafted
    t_m, t_tin = 0.25, 0.08
    drafted = assumed("order stated; height, thickness and lateral position of each BEOL level not stated")
    x.rect(-half, -t_thick - 1.4, half, -t_thick, "si", "high-resistivity Si carrier: truncated", stated("Sec. 2", "bonded HR carrier") + assumed("thickness not stated: truncated"), layer="substrate", alpha=0.5)
    x.rect(-half, -t_thick, half, 0.0, "sio2", "BEOL plus thick planar oxide: reconstructed BOX", stated("Sec. 1, Sec. 2", "above 5 um; drawn at 5 um"), layer="oxide")
    x.rect(-half, 0.0, half, t_si, "sio2", "oxide around the patterned Si", stated("Sec. 2", "patterned before the BEOL"), layer="oxide", alpha=0.7)
    x.rect(-half, t_si, half, t_si + t_box, "sio2", "original buried oxide of the SOI", stated("Sec. 2", "200 nm BOX"), layer="oxide", alpha=0.5)
    x.rect(-half, t_si + t_box, half, t_si + t_box + clad, "sio2", "oxide on the back side, with the SiN levels (not at this device)", assumed("back-side cladding thickness not stated"), layer="oxide", alpha=0.3)
    x.rect(-w_wg / 2, 0.0, w_wg / 2, t_si, "si", "Si waveguide, 300 nm SOI layer, etched face down", stated("Sec. 2", "300 nm SOI") + assumed("the text does not say which waveguide is heated: Si strip drafted; width not stated"), layer="waveguide")
    x.rect(-w_h / 2, z_tin, w_h / 2, z_tin + t_tin, "metal", "TiN heater", stated("Sec. 2", "TiN resistance between metal 1 and metal 2") + drafted, layer="metal")
    for s in (-1, 1):
        x0, x1 = sorted((s * 3.0, s * 6.0))
        xv0, xv1 = sorted((s * 4.3, s * 4.7))
        x.rect(x0, z_m1, x1, z_m1 + t_m, "metal", "metal 1", stated("Sec. 2", "contact and metal 1") + drafted, layer="metal")
        x.rect(x0, z_m2, x1, z_m2 + t_m, "metal", "metal 2", stated("Sec. 2", "via 1, metal 2") + drafted, layer="metal")
        x.rect(x0, z_m3, x1, z_m3 + t_m, "metal", "metal 3", stated("Sec. 2", "via 2, metal 3") + drafted, layer="metal")
        x.rect(xv0, z_m2 + t_m, xv1, z_m1, "metal", "via 1", stated("Sec. 2", "via 1") + drafted, layer="via")
        x.rect(xv0, z_m3 + t_m, xv1, z_m2, "metal", "via 2", stated("Sec. 2", "via 2") + drafted, layer="via")
    x.dim("v", 0.0, t_si, w_wg / 2, px=22, ext=(w_wg / 2, w_wg / 2), text="300 nm", src=stated("Sec. 2", "SOI layer"))
    x.dim("v", t_si, t_si + t_box, -2.0, px=0, ext=(-2.0, -2.0), text="200 nm BOX", src=stated("Sec. 2", "BOX of the SOI"))
    x.dim("v", -t_thick, 0.0, -7.0, px=0, ext=(-7.0, -7.0), text="> 5 um", src=stated("Sec. 1", "reconstructed BOX above 5 um"))
    x.label((3.0, z_m1 + t_m / 2), "M1", anchor="end", dx=-4)
    x.label((-w_h / 2, z_tin), "TiN", anchor="end", dx=-4)
    x.label((3.0, z_m2 + t_m / 2), "M2", anchor="end", dx=-4)
    x.label((3.0, z_m3 + t_m / 2), "M3", anchor="end", dx=-4)
    x.label((0.0, -4.0), "thick planar oxide, bond", tip="Sec. 2: thick planar oxide for bonding on the carrier")
    x.label((0.0, -t_thick - 0.7), "HR carrier")
    x.note("Text only. Upward from the carrier, as the process leaves it: thick oxide, M3, M2, TiN, M1, Si, BOX. The order is stated; every BEOL height, thickness and lateral position is drafted.")
    x.note("Whether M1 or M2 contacts the TiN is not stated, so no contact is drawn at this plane. Heater offset from the waveguide not stated. The heated waveguide (Si or SiN) is not stated either: Si strip drafted.")
    x.note("The paper credits the very thick BOX for the 15.5 mW per pi; no thermal design data is given.")
    assert 0 > z_m1 > z_tin > z_m2 > z_m3 > -t_thick  # stated order, inside the thick oxide
    return c
