"""Tests for scripts/lit_refgraph.py (DevLog-020): reference splitting, squashed-title matching, cluster keys."""

from __future__ import annotations

import importlib.util
import sys
from types import ModuleType

from photonics_atlas.paths import ROOT


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("lit_refgraph", ROOT / "scripts" / "lit_refgraph.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["lit_refgraph"] = mod
    spec.loader.exec_module(mod)
    return mod


m = _load()

IEEE_TEXT = """1. Introduction
Body text cites [1] and [2].
2. Results
More body.
REFERENCES
[1] P. Dumon, G. Roelkens, and R. Baets, "Basic photonic wire components in
silicon-on-insulator," in Proc. GFP, 2005, Paper WA1.
<!-- page 4 -->
[2] T. Tsuchizawa et al., "Mi-
crophotonics devices based on silicon microfabrication technology,"
IEEE J. Sel. Topics Quantum Electron., vol. 11, no. 1, pp. 232-240, 2005.
[3] M. K. Smit, "A normalized approach," J. Lightw. Technol., vol. 9, pp. 1-8, 1991.
"""


def test_split_references_bracket_style_ignores_section_numbers() -> None:
    ents = m.split_references(IEEE_TEXT)
    assert [n for n, _ in ents] == [1, 2, 3]
    assert "Microphotonics devices" in ents[1][1]  # hyphenation across the line break joined
    assert "page" not in ents[1][1]


def test_split_references_dot_style_and_too_short() -> None:
    text = "\n".join(
        [
            "References and links",
            "1. C. R. Doerr and K. Okamoto, Advances in silica planar lightwave circuits, JLT 24, 4763 (2006).",
            "2. B. Jalali and S. Fathpour, Silicon photonics, JLT 24, 4600 (2006).",
            "3. R. Soref, The past, present, and future of silicon photonics, JSTQE 12, 1678 (2006).",
            "1. Introduction",
        ]
    )
    assert [n for n, _ in m.split_references(text)] == [1, 2, 3]
    assert m.split_references("1. Intro\n2. Methods\n") == []


def test_squash_and_containment() -> None:
    t = m.squash("Low-loss, low-cross-talk crossings for SOI nanophotonic waveguides")
    e = m.squash(
        'W. Bogaerts et al., "Low-loss, low-crosstalk crossings for SOI nano-\nphotonic waveguides," OL (2007).'
    )
    assert m.containment(t, e) == 1.0
    assert m.squash("efﬁciency") == "efficiency"  # ligature
    assert m.containment(m.squash("Completely different title words"), e) < 0.5


def test_match_requires_year_and_surname_for_short_titles() -> None:
    corpus = [
        m.Work("lit:jalali2006", "Silicon photonics", 2006, surname="jalali"),
        m.Work("lit:doerr2006", "Advances in silica planar lightwave circuits", 2006, surname="doerr"),
    ]
    idx = m.Index(corpus)
    r = m.match("C. R. Doerr and K. Okamoto, Advances in silica planar lightwave circuits, JLT 24 (2006).", idx)
    assert r and r["accepted"] and r["id"] == "lit:doerr2006"
    # short generic title inside another work's citation: no surname -> not accepted
    r = m.match('M. Hochberg, "Towards fabless silicon photonics devices," Nat. Photonics 4 (2006).', idx)
    assert not (r and r["accepted"])
    # wrong year -> no candidate accepted
    r = m.match("Doerr, C. R. Advances in silica planar lightwave circuits. JLT 24 (2015).", idx)
    assert not (r and r["accepted"])


def test_doi_match_and_truncated_doi() -> None:
    idx = m.Index([m.Work("lit:x", "A sufficiently long title for indexing", 2010, doi="10.1364/oe.18.001234")])
    r = m.match("A. B. Author, Opt. Express 18, 1234 (2010), doi:10.1364/OE.18.001234.", idx)
    assert r and r["method"] == "doi" and r["accepted"]
    assert m.entry_dois("see 10.1117/12. 2251234 and 10.1063/1") == []


def test_unmatched_keys_merge_across_styles() -> None:
    ieee, _ = m.unmatched_keys('R. Soref, "Enabling 2 um communications," Nat. Photonics, vol. 9, pp. 358-359, 2015.')
    nature, _ = m.unmatched_keys("Soref, R. Enabling 2 um communications. Nat. Photonics 9, 358-359 (2015).")
    assert "bib:soref|2015|358" in ieee and "bib:soref|2015|358" in nature
    two, title = m.unmatched_keys(
        'A. X, "First title of the entry," J. 1, 101 (2001); B. Y, "Second title here," doi:10.1/x'
    )
    assert title == "First title of the entry" and two == ["title:firsttitleoftheentry"]


def test_optica_footer_removed() -> None:
    e = m.clean_entry(
        "T. J. Kippenberg, Microresonator-based optical frequency combs, Science 332, 555 (2011). #255179 "
        "Received 14 Dec 2015; published 27 Jan 2016 (C) 2016 OSA | Vol. 24, No. 3 | DOI:10.1364/OE.24.002183 | "
        "OPTICS EXPRESS 2183"
    )
    assert "OE.24.002183" not in e and e.endswith("(2011).")


def test_union_find() -> None:
    uf = m.UnionFind()
    uf.union("a", "b")
    uf.union("c", "b")
    assert uf.find("c") == uf.find("a")


def test_split_prefers_latest_run_and_new_styles() -> None:
    body = ["1. Introduction", "Text.", "2. Design", "Text.", "3. Results", "Text."]
    refs = [f"{k}. A. Author{k}, Title number {k}, Opt. Express {k}, {100 + k} (2010)." for k in range(1, 7)]
    ents = m.split_references("\n".join(body + ["References"] + refs))
    assert [n for n, _ in ents] == [1, 2, 3, 4, 5, 6] and "Author1" in ents[0][1]
    glued = "\n".join(f"{k}M. Hochberg, Fabless photonics part {k}, Nat. Photon. 4, {k}0 (2010)." for k in range(1, 5))
    assert len(m.split_references(glued)) == 4


def test_built_dois() -> None:
    assert m.built_dois("C. Doerr, Advances, Opt. Express 20(10), 11665-11673 (2012).") == ["10.1364/oe.20.011665"]
    assert m.built_dois("Q. P. U, Damping, Phys. Rev. Lett. 105(2), 027205 (2010).") == [
        "10.1103/physrevlett.105.027205"
    ]
    assert m.built_dois("X. Y, Title, Phys. Rev. A 85, 053829 (2012).") == ["10.1103/physreva.85.053829"]
    assert m.built_dois("X, Title, Opt. Lett., vol. 32, no. 19, pp. 2801-2803, 2007.") == ["10.1364/ol.32.002801"]
    assert m.built_dois("A, B, Optics express, 18(2):1756-1761, 2010.") == ["10.1364/oe.18.001756"]
    assert m.built_dois("M. F, Title, Optics Express vol.19, (23) 23153-23161 (2011).") == ["10.1364/oe.19.023153"]
    assert m.built_dois("W. G, Title, Opt. Express, vol. 15, no. 25, pp. 17 106-17 113, 2007.") == [
        "10.1364/oe.15.017106"
    ]
    assert m.built_dois("O. B and B. J, Silicon Raman laser, Opt. Express 12, 5269 (2004).") == [
        "10.1364/opex.12.005269"
    ]
    assert m.built_dois("S. B. Papp and S. A. Diddams, Physical Review A 84, 53833 (2011).") == [
        "10.1103/physreva.84.053833"
    ]


def test_title_author_needs_first_author_and_085() -> None:
    w = m.Work("lit:b", "Compact low-loss waveguide crossing for silicon nitride photonic platforms", 2007)
    w.surname = "bogaerts"
    idx = m.Index([w])
    ok = "W. Bogaerts, P. Dumon, Compact low-loss waveguide crossing for the silicon nitride photonic platform, OL (2007)."
    r = m.match(ok, idx)
    assert r and 0.85 <= r["score"] < 0.9 and r["accepted"] and r["method"] == "title_author"
    swapped = "P. Dumon, W. Bogaerts, Compact low-loss waveguide crossing for the silicon nitride photonic platform, OL (2007)."
    r = m.match(swapped, idx)
    assert not (r and r["accepted"])
