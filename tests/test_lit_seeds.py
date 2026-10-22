"""Pure-function tests for scripts/lit_seeds.py (identifier mapping, title match, filters, table parse); no network."""

from __future__ import annotations

import importlib.util
import sys
from types import ModuleType

import yaml

from photonics_atlas.paths import ROOT


def _mod() -> ModuleType:
    spec = importlib.util.spec_from_file_location("lit_seeds", ROOT / "scripts" / "lit_seeds.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["lit_seeds"] = mod
    spec.loader.exec_module(mod)
    return mod


m = _mod()


def test_optica_uri_to_doi() -> None:
    assert m.optica_uri_to_doi("oe-18-14-14439") == "10.1364/oe.18.014439"
    assert m.optica_uri_to_doi("optica-6-9-1244") == "10.1364/optica.6.001244"
    assert m.optica_uri_to_doi("not-a-uri") == ""


def test_title_ratio() -> None:
    a = "Coupling strategies for silicon photonics integrated chips [Invited]"
    assert m.title_ratio(a, "Coupling Strategies for Silicon Photonics Integrated Chips") >= m.TITLE_MATCH_MIN
    assert m.title_ratio(a, "Edge couplers in silicon photonic integrated circuits: a review") < m.TITLE_MATCH_MIN
    assert m.title_ratio("", a) == 0.0


def test_eo_is_component() -> None:
    assert m.eo_is_component("Integrated electro-optic circulator on thin-film lithium niobate")
    assert m.eo_is_component("Monolithically integrated 4 x 128 Gb/s silicon photonic transceiver for CPO")
    assert not m.eo_is_component("Thin-film lithium niobate modulators with 170 GHz bandwidth")
    assert not m.eo_is_component("Cavity electro-optics in thin-film lithium niobate for microwave-to-optical transduction")


def test_parse_taxonomy_seeds() -> None:
    md = (
        "## 5. Gaps and seed references\n\n| class | title | venue, year | DOI / arXiv | seen in |\n|---|---|---|---|---|\n"
        "| PWB | Photonic wire bonding | Opt. Express 2012 | 10.1364/OE.20.017667 | yeh2026 |\n\n## 6. Open\n| x | y |\n"
    )
    rows = m.parse_taxonomy_seeds(md)
    assert len(rows) == 1 and rows[0]["class"] == "PWB" and m.DOI_RE.search(rows[0]["ids"])


def test_chunks_and_safe_name() -> None:
    assert [len(c) for c in m.chunks([str(i) for i in range(250)], 100)] == [100, 100, 50]
    n = m.safe_name("doi:10.1364/PRJ.7.000201")
    assert "/" not in n and n == m.safe_name("doi:10.1364/PRJ.7.000201")


def test_config_reviews_well_formed() -> None:
    cfg = yaml.safe_load((ROOT / "config" / "literature" / "seed_reviews.yaml").read_text())
    classes = set(yaml.safe_load((ROOT / "data" / "schema" / "component_parameters.yaml").read_text())["classes"])
    for r in cfg["reviews"]:
        assert r["class"] in classes and r["doi"].startswith("10.") and r["how_found"]
    assert {r["class"] for r in cfg["reviews"]} == classes
