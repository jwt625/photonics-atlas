"""OFC 2026 Tu2D.3: SiN single-mode strip of the Samsung Foundry platform. Text only: Fig. 1 and Table 1 not available.

Fixed by the text: 400 nm SiN, deposited and patterned after the 305 nm Si levels on a 2 um BOX. Not stated: strip width, gap to
the Si plane, cladding, sidewall, the loss test structure. Width and gap are drawn with no dimension and marked assumed.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import Cell, assumed, row, stated  # noqa: E402

ID = "cmp_ofc2026_tu2d3_sin_strip_wg"


def build() -> Cell:
    c = Cell(ID, ["Sec. 2 (text only)", "Sec. 3 (text only)", "Fig. 1 and Table 1 not available"], "400 nm SiN strip section above the Si plane on 2 um BOX; strip width, gap and cladding not in the text")
    t = c.um("m2")
    box, t_si = 2.0, 0.305  # Sec. 2
    w, gap, clad, run, half = 1.0, 0.2, 2.0, 10.0, 3.0  # drafting values, no label
    y0 = t_si + gap
    why = assumed("single-mode strip width not stated")

    top = c.view("top", "top view: straight strip (width assumed, no test structure in the source)")
    top.rect(0, -w / 2, run, w / 2, "sin", "SiN SM strip", why, layer="waveguide")
    top.note("Text and captions only. Width, length and the loss test structure are not stated. This is a placeholder for a straight strip.")
    c.thumb = {"view": "xsec", "window": [-2.0, -0.3, 2.0, 1.2]}

    x = c.view("xsec", "cross-section: strip in the stated stack (substrate truncated)", "xsec")
    x.rect(-half, -box - 1.2, half, -box, "si", "Si handle", assumed("handle thickness: truncated"), layer="substrate", alpha=0.5)
    x.rect(-half, -box, half, 0, "sio2", "buried oxide", stated("Sec. 2", "2 um BOX"), layer="oxide")
    x.rect(-half, 0, half, y0, "sio2", "oxide over the etched Si level", assumed("gap from the Si plane to the SiN not stated"), layer="oxide", alpha=0.65)
    x.rect(-half, y0, half, y0 + t + clad, "sio2", "oxide above the SiN", assumed("cladding not stated"), layer="oxide", alpha=0.35)
    x.line([(-half, t_si), (half, t_si)], "plane of the top Si surface, 305 nm above the BOX: Si removed here", stated("Sec. 2", "305 nm top Si, patterned before the SiN") + assumed("no Si under this strip"))
    x.rect(-w / 2, y0, w / 2, y0 + t, "sin", "SiN core, 400 nm", row("m2") + why + assumed("gap not stated"), layer="waveguide")
    x.dim("v", y0, y0 + t, w / 2, px=18, ext=(w / 2, w / 2), row_id="m2")
    x.dim("v", -box, 0, -half + 0.5, px=0, ext=(-half + 0.5, -half + 0.5), text="2 um", src=stated("Sec. 2", "BOX"))
    x.dim("v", 0, t_si, half - 0.5, px=0, ext=(half - 0.5, half - 0.5), text="305 nm", src=stated("Sec. 2", "Si layer"))
    x.label((-half + 0.1, t_si), "Si plane", anchor="start", dy=-4)
    x.note("Sidewalls drawn vertical: not stated. Width and gap have no source; only the thicknesses of SiN, Si and BOX are from the paper.")
    return c
