"""Pure-function tests for scripts/lit_harvest_openalex.py (filters, years, ordering, config); no network."""

from __future__ import annotations

import importlib.util
import sys
from types import ModuleType

from photonics_atlas.paths import ROOT


def _mod() -> ModuleType:
    spec = importlib.util.spec_from_file_location("lit_harvest_openalex", ROOT / "scripts" / "lit_harvest_openalex.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["lit_harvest_openalex"] = mod
    spec.loader.exec_module(mod)
    return mod


m = _mod()


def test_parse_years() -> None:
    assert m.parse_years("") is None
    assert m.parse_years("2020-2026") == (2020, 2026)
    assert m.parse_years("2024") == (2024, 2024)
    assert m.parse_years("2026-2020") == (2020, 2026)


def test_venue_years_newest_first_and_intersected() -> None:
    v = {"years": [2016, 2026]}
    assert m.venue_years(v, None) == list(range(2026, 2015, -1))
    assert m.venue_years(v, (2024, 2030)) == [2026, 2025, 2024]
    assert m.venue_years(v, (2000, 2010)) == []


def test_filters() -> None:
    assert m.base_filter("S1", "article|review", "") == "primary_location.source.id:S1,type:article|review"
    assert (
        m.unit_filter("S1", 2020, "article", " topics.id:T1|T2 ")
        == "primary_location.source.id:S1,type:article,topics.id:T1|T2,publication_year:2020"
    )
    assert m.base_filter("S1", "", "") == "primary_location.source.id:S1"


def test_pages_for() -> None:
    assert [m.pages_for(n) for n in (0, 1, 200, 201, 3968)] == [1, 1, 1, 2, 20]


def test_order_venues() -> None:
    vs = [{"key": "a", "priority": 2}, {"key": "b", "priority": 1}, {"key": "c"}, {"key": "d", "priority": 1}]
    assert [v["key"] for v in m.order_venues(vs, None)] == ["b", "d", "a", "c"]
    assert [v["key"] for v in m.order_venues(vs, {"a", "d"})] == ["d", "a"]


def test_journals_config_valid() -> None:
    cfg = m.load_config(ROOT / "config" / "literature" / "venues_journals.yaml")
    assert cfg["lane"] == "journals"
    for v in cfg["venues"]:
        assert v["key"] and v["issn"] and str(v["openalex_source_id"]).startswith("S")
        assert len(v["years"]) == 2 and v["years"][0] <= v["years"][1]
        assert "search" not in str(v.get("extra_filter") or "")
