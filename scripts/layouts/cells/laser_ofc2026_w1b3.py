"""OFC 2026 W1B.3 SOA-integrated DFB-LD, 1.8 mm, on an AlN carrier. Text and captions only: Fig. 3 (TOSA schematic) not available.

What the text fixes: one chip with a DFB and an integrated SOA, 1.8 mm long; junction-down on AlN (Sec. 3 for the TOSA, the CoS
is AlN too); output from the SOA end through a lens-integrated isolator to fibre; monitor photodiode on the back facet. Section
split, width, stack, material and wavelength are not stated. The paper plots a single bias current, so whether the two sections
have separate electrodes is also unknown. All such geometry is dashed and has no dimension.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, assumed, rect, row, stated  # noqa: E402

ID = "cmp_ofc2026_w1b3_soa_dfb_1p8mm"


def build() -> Cell:
    c = Cell(
        ID,
        ["Text and captions only: Fig. 3 TOSA schematic not available; Fig. 1, 2 are curves", "Sec. 2", "Sec. 3"],
        "One chip: DFB section with grating and SOA section without, junction-down on AlN; 1.8 mm stated, section split and all transverse geometry assumed",
    )
    length = c.um("m8")
    why = "not stated in this text-only source"
    w_chip = 350.0
    l_dfb = length / 2  # split not stated
    gap = 20.0
    w_stripe = 4.0
    al_m = 150.0  # AlN margin

    # stack from the junction side downward onto AlN; z = 0 at the AlN top
    t_solder, t_p_m, t_p_cl, t_act, t_grating = 3.0, 1.0, 2.0, 0.2, 0.1
    z_pm = t_solder
    z_pcl = z_pm + t_p_m
    z_g = z_pcl + t_p_cl  # grating on the p side, junction down so above p-cladding here
    z_a = z_g + t_grating
    z_n = z_a + t_act
    t_aln = 100.0

    c.check("drawn chip length against the printed 1.8 mm, um", length, 1800.0, 1e-9)

    top = c.view("top", "top view (text only), seen through the chip because the junction faces the AlN")
    top.rect(-al_m, -w_chip / 2 - al_m, length + al_m, w_chip / 2 + al_m, "other", "AlN carrier", stated("p.1 Sec. 2", "AlN substrate, chip-on-substrate") + assumed(f"carrier size: {why}"), alpha=0.5, layer="substrate")
    top.rect(0, -w_chip / 2, length, w_chip / 2, "unknown", "semiconductor chip, material not stated", row("m8") + assumed(f"width: {why}"), alpha=0.45, layer="slab")
    src_e = assumed(f"section split and electrode separation: {why}; only one LD bias current is reported")
    top.rect(0, -w_chip / 2 + 40, l_dfb - gap / 2, w_chip / 2 - 40, "metal", "DFB electrode", src_e, layer="metal", alpha=0.55)
    top.rect(l_dfb + gap / 2, -w_chip / 2 + 40, length, w_chip / 2 - 40, "metal", "SOA electrode", src_e, layer="metal", alpha=0.55)
    top.rect(0, -w_stripe / 2, l_dfb, w_stripe / 2, "active", "DFB active stripe with grating", stated("p.1 Sec. 1", "SOA-integrated DFB") + src_e, layer="waveguide")
    top.rect(l_dfb, -w_stripe / 2, length, w_stripe / 2, "active", "SOA active stripe, no grating", stated("p.1 Sec. 1", "SOA-integrated DFB") + src_e, layer="waveguide", alpha=0.6)
    top.line([(0, -w_chip / 2 - 20), (0, w_chip / 2 + 20)], "back facet: light goes to the monitor photodiode", stated("p.2 Sec. 3", "photodiodes monitor the power from the back facets"))
    top.line([(length, -w_chip / 2 - 20), (length, w_chip / 2 + 20)], "output facet: to the lens-integrated isolator and fibre", stated("p.2 Sec. 3"))
    top.dim("h", 0, length, -w_chip / 2, px=-30, ext=(-w_chip / 2, -w_chip / 2), row_id="m8")
    top.label((l_dfb / 2, w_chip / 2 - 90), "DFB, grating", anchor="middle")
    top.label((l_dfb + (length - l_dfb) / 2, w_chip / 2 - 90), "SOA", anchor="middle")
    top.label((0, 0), "back, to monitor PD", anchor="end", dx=-6)
    top.label((length, 0), "output, to isolator", anchor="start", dx=6)
    top.note("Whole-chip length is the row. Text and captions only: the boundary between DFB and SOA is at an arbitrary place.")
    top.note("The text attaches the 1.8 mm both to the cavity and to the integrated device, so DFB alone or DFB plus SOA is ambiguous; it is drawn as the whole chip.")
    c.thumb = {"view": "top"}

    x = c.view("xsec", "cross-section in the DFB, junction down on AlN (text only)", "xsec")
    u = 25.0
    x.rect(-u, -t_aln / 10, u, 0, "other", "AlN carrier", stated("p.1 Sec. 2", "AlN") + assumed("truncated"), alpha=0.6, layer="substrate")
    x.rect(-u, 0, u, t_solder, "metal", "die attach", stated("p.2 Sec. 3", "junction-down") + assumed(f"material and thickness: {why}"), layer="metal", alpha=0.7)
    x.rect(-u, z_pm, u, z_pcl, "metal", "p-side metal", assumed(why), layer="metal")
    x.rect(-u, z_pcl, u, z_g, "sio2", "insulator around the stripe", assumed(why), alpha=0.5, layer="oxide")
    x.rect(-w_stripe / 2, z_pcl, w_stripe / 2, z_g, "unknown", "p-side stripe, ridge or buried not stated", assumed(why), layer="waveguide")
    x.rect(-u, z_g, u, z_a, "unknown", "grating layer", stated("p.1 Sec. 1", "DFB") + assumed(f"position and depth: {why}"), alpha=0.8, layer="slab")
    x.rect(-u, z_a, u, z_n, "active", "active layer", assumed(f"material, thickness and QW count: {why}"), layer="absorber")
    x.rect(-u, z_n, u, z_n + 12.0, "unknown", "n-side substrate, truncated", assumed(f"thickness: {why}"), alpha=0.6, layer="substrate")
    x.label((0, z_n + 6), "n-side substrate, truncated")
    x.label((-u + 3, z_a + t_act / 2), "active", anchor="start", dy=4)
    x.label((0, z_pcl + 1), "stripe")
    x.label((0, t_solder / 2), "die attach")
    x.label((0, -t_aln / 20), "AlN")
    x.note("Text and captions only. Junction-down stated in Sec. 3 for the TOSA; the CoS of Sec. 2 is mounted on AlN too. Ridge or buried heterostructure, layer thicknesses and materials are not stated: placeholders.")

    ls = c.view("lsec", "section along the stripe at the DFB to SOA boundary (text only)", "xsec")
    x0, x1 = l_dfb - 25.0, l_dfb + 25.0
    ls.rect(x0, -3.0, x1, 0, "other", "AlN carrier", stated("p.1 Sec. 2", "AlN") + assumed("truncated"), alpha=0.6, layer="substrate")
    ls.rect(x0, 0, x1, t_solder, "metal", "die attach", stated("p.2 Sec. 3", "junction-down") + assumed(why), layer="metal", alpha=0.7)
    ls.rect(x0, z_pm, l_dfb - gap / 2, z_pcl, "metal", "DFB electrode", src_e, layer="metal")
    ls.rect(l_dfb + gap / 2, z_pm, x1, z_pcl, "metal", "SOA electrode", src_e, layer="metal")
    ls.rect(x0, z_pcl, x1, z_g, "unknown", "p-side stripe", assumed(why), layer="waveguide")
    p_sch = 0.24  # schematic: no wavelength in the paper
    ls.rect(x0, z_g, l_dfb, z_a, "unknown", "grating region", stated("p.1 Sec. 1", "DFB") + src_e, alpha=0.8, layer="slab")
    n_t = int((l_dfb - x0) / p_sch)
    ls.rings([rect(l_dfb - (i + 0.75) * p_sch, z_g, l_dfb - (i + 0.25) * p_sch, z_a) for i in range(n_t)], "active", "grating teeth, schematic pitch", assumed("the wavelength and the period are not stated: the pitch is a drawing device, not a value"), layer="absorber", lod=p_sch / 2)
    ls.rect(l_dfb, z_g, x1, z_a, "unknown", "no grating in the SOA", stated("p.1 Sec. 1") + src_e, alpha=0.6, layer="slab")
    ls.rect(x0, z_a, x1, z_n, "active", "active layer", assumed(why), layer="absorber")
    ls.rect(x0, z_n, x1, z_n + 8.0, "unknown", "n-side substrate, truncated", assumed(why), alpha=0.6, layer="substrate")
    ls.label((x0 + 12, z_n + 4), "n-side substrate")
    ls.label((l_dfb - 13, z_g), "DFB: grating", dy=-14)
    ls.label((l_dfb + 13, z_g), "SOA: no grating", dy=-14)
    ls.label((l_dfb - 12, z_pm), "DFB electrode", dy=-3)
    ls.label((l_dfb + 12, z_pm), "SOA electrode", dy=-3)
    ls.label((l_dfb, -1.5), "AlN")
    ls.note("Period not stated and cannot be checked: the paper does not give the wavelength or the material (Bragg check not possible).")
    g = c.view("grating", "detail: grating ends at the assumed section boundary (text only)", "xsec", like="lsec", window=(l_dfb - 2.0, z_g - 0.5, l_dfb + 2.0, z_n + 0.5))
    g.label((l_dfb - 1.2, z_g), "DFB teeth, schematic pitch", dy=10)
    g.label((l_dfb + 1.2, z_g), "SOA", dy=10)
    g.label((l_dfb, z_n), "active", dy=-4)
    return c
