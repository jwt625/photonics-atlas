"""OFC 2026 M1D.2 single-section DFB, 600 um, reference laser for a two-section device. Text and captions only.

What the text fixes: 600 um; structure identical to the two-section laser, whose two 300 um sections are separated by a gap etched in
its ternary contact layer (Fig. 1(a), not available). So this device has that contact layer unbroken along the cavity and one
electrode. Material, wavelength, width, stack, ridge type, facets are not stated: dashed, with no dimension.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, assumed, rect, row, stated  # noqa: E402

ID = "cmp_ofc2026_m1d2_single_section_dfb_600um"


def build() -> Cell:
    c = Cell(
        ID,
        ["Text and captions only: Fig. 1(a) cross-section schematic of the two-section sibling not available", "Sec. 2", "Sec. 3", "Table 1"],
        "Single electrode and unbroken ternary contact over 600 um (sibling has an etched gap at 300 um); grating, stack and width assumed",
    )
    length = c.um("m2")
    l_sec = 300.0  # Sec. 2: length of each part of the sibling
    why = "not stated in this text-only source"
    c.check("sibling sections 2 x 300 um against the single-section length, um", 2 * l_sec, length, 1e-9)
    c.check("Table 1: 2.9 GHz / 40 mA against the FM efficiency row, GHz/mA", 2.9 / 40, c.num("m3"), 0.05)

    w_chip = 250.0
    w_s = 3.0
    t_n, t_act, t_g, t_p, t_ter, t_m = 0.5, 0.2, 0.1, 1.8, 0.2, 0.5
    z_a = t_n
    z_g = z_a + t_act
    z_p = z_g + t_g
    z_t = z_p + t_p
    z_m = z_t + t_ter

    top = c.view("top", "top view (text only): one electrode along the 600 um")
    top.rect(0, -w_chip / 2, length, w_chip / 2, "unknown", "chip, material not stated", row("m2") + assumed(f"width: {why}"), alpha=0.6, layer="slab")
    top.rect(0, -w_s / 2, length, w_s / 2, "unknown", "waveguide stripe, ridge or buried not stated", row("m2") + assumed(f"width and type: {why}"), layer="waveguide")
    top.rect(0, -w_s / 2 - 25, length, w_s / 2 + 25, "metal", "single electrode, no gap", row("m2") + stated("p.2 Sec. 2", "the sibling's isolation is an etched gap in the ternary contact; this device has one section") + assumed(f"width: {why}"), layer="metal", alpha=0.5)
    top.line([(l_sec, -w_chip / 2), (l_sec, w_chip / 2)], "position of the sibling's etched contact gap; not present here", stated("p.2 Sec. 2", "both sections of the two-section laser are 300 um"))
    top.line([(0, -w_chip / 2 - 10), (0, w_chip / 2 + 10)], "facet: coating not stated", assumed(why))
    top.line([(length, -w_chip / 2 - 10), (length, w_chip / 2 + 10)], "facet: coating not stated", assumed(why))
    top.dim("h", 0, length, -w_chip / 2, px=-30, ext=(-w_chip / 2, -w_chip / 2), row_id="m2")
    top.label((l_sec, w_chip / 2), "no gap: sibling has one here", dy=-6)
    top.label((l_sec / 2, 45), "one electrode")
    top.note("Text and captions only. Which facet is the output is not stated. The sibling's cross-section in Fig. 1(a) is not available.")
    c.thumb = {"view": "top"}

    x = c.view("xsec", "transverse cross-section (text only)", "xsec")
    u = 15.0
    x.rect(-u, -8.0, u, 0, "unknown", "substrate, truncated", assumed(f"material and thickness: {why}"), alpha=0.6, layer="substrate")
    x.rect(-u, 0, u, z_a, "unknown", "lower cladding", assumed(why), alpha=0.8, layer="slab")
    x.rect(-u, z_a, u, z_g, "active", "active layer", assumed(f"material, thickness, QW count: {why}"), layer="absorber")
    x.rect(-u, z_g, u, z_p, "unknown", "grating layer", stated("title", "DFB") + assumed(f"position and depth: {why}"), alpha=0.9, layer="slab")
    x.rect(-w_s / 2, z_p, w_s / 2, z_t, "unknown", "stripe", assumed(f"ridge or buried not stated: {why}"), layer="waveguide")
    x.rect(-w_s / 2, z_t, w_s / 2, z_m, "contact", "ternary contact layer", stated("p.2 Sec. 2", "ternary contact layer") + assumed(f"composition, thickness: {why}"), layer="doped")
    x.rect(-u, z_p, -w_s / 2, z_t, "sio2", "insulator", assumed(why), alpha=0.5, layer="oxide")
    x.rect(w_s / 2, z_p, u, z_t, "sio2", "insulator", assumed(why), alpha=0.5, layer="oxide")
    x.rect(-w_s / 2 - 5, z_m, w_s / 2 + 5, z_m + t_m, "metal", "electrode", assumed(f"width and thickness: {why}"), layer="metal")
    x.label((-u + 3, z_a + t_act / 2), "active", dy=4)
    x.label((0, (z_p + z_t) / 2), "stripe")
    x.label((-u + 5, -4), "substrate")
    x.label((w_s / 2 + 0.6, z_t), "ternary contact", anchor="start", dy=2)
    x.note("All thicknesses and the stripe type are placeholders: the paper states only that the contact layer is ternary.")

    ls = c.view("lsec", "section along the stripe at mid cavity (text only)", "xsec")
    x0, x1 = l_sec - 15.0, l_sec + 15.0
    ls.rect(x0, -4.0, x1, 0, "unknown", "substrate, truncated", assumed(why), alpha=0.6, layer="substrate")
    ls.rect(x0, 0, x1, z_a, "unknown", "lower cladding", assumed(why), alpha=0.8, layer="slab")
    ls.rect(x0, z_a, x1, z_g, "active", "active layer", assumed(why), layer="absorber")
    ls.rect(x0, z_g, x1, z_p, "unknown", "grating region", stated("title", "DFB") + assumed(why), alpha=0.8, layer="slab")
    p_sch = 0.24  # no wavelength in the paper
    n_t = int((x1 - x0) / p_sch)
    ls.rings([rect(x0 + (i + 0.25) * p_sch, z_g, x0 + (i + 0.75) * p_sch, z_p) for i in range(n_t)], "active", "grating teeth, schematic pitch", assumed("wavelength and period not stated: the pitch is a drawing device, not a value"), layer="absorber", lod=p_sch / 2)
    ls.rect(x0, z_p, x1, z_t, "unknown", "stripe", assumed(why), layer="waveguide")
    ls.rect(x0, z_t, x1, z_m, "contact", "ternary contact layer, unbroken", stated("p.2 Sec. 2", "ternary contact layer; etched only in the two-section sibling"), layer="doped")
    ls.rect(x0, z_m, x1, z_m + t_m, "metal", "electrode", assumed(why), layer="metal")
    ls.line([(l_sec, -4.0), (l_sec, z_m + t_m)], "mid cavity: sibling's etched contact gap would be here", stated("p.2 Sec. 2"))
    ls.label((x0 + 7, z_m + t_m), "electrode", dy=-5)
    ls.label((x0 + 21, z_m), "ternary", dy=-6)
    ls.label((x0 + 7, z_a + t_act / 2), "active", dy=4)
    ls.label((x0 + 15, -2), "substrate")
    ls.note("Period not stated and cannot be checked: neither the wavelength nor the material is in the paper. Fig. 1(a) of the paper shows the sibling, not this device.")
    g = c.view("grating", "detail: grating and unbroken contact at mid cavity (text only)", "xsec", like="lsec", window=(l_sec - 2.0, z_a - 0.3, l_sec + 2.0, z_m + t_m + 0.2))
    g.label((l_sec - 1.0, z_p), "teeth, schematic pitch", dy=-8)
    g.label((l_sec - 1.0, z_t), "ternary, unbroken", dy=-3)
    g.label((l_sec + 1.0, z_a), "active", dy=-3)
    return c
