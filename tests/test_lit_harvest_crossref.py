"""Pure-function tests for scripts/lit_harvest_crossref.py (routing, filters, record mapping, config); no network."""

from __future__ import annotations

import importlib.util
import sys
from types import ModuleType
from typing import Any

from photonics_atlas.paths import ROOT


def _mod() -> ModuleType:
    spec = importlib.util.spec_from_file_location("lit_harvest_crossref", ROOT / "scripts" / "lit_harvest_crossref.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["lit_harvest_crossref"] = mod
    spec.loader.exec_module(mod)
    return mod


m = _mod()

ITEM: dict[str, Any] = {
    "DOI": "10.1364/OFC.2020.M1A.4",
    "title": ["Low-loss <i>SiN</i> edge coupler"],
    "container-title": ["Optical Fiber Communication Conference (OFC) 2020"],
    "author": [
        {"given": "A.", "family": "One", "affiliation": [{"name": "Univ X"}]},
        {"given": "B.", "family": "Two", "affiliation": [{"name": "Univ X"}, {"name": "Lab &amp; Y"}]},
    ],
    "abstract": "<jats:title>Abstract</jats:title><jats:p>We show 0.5 dB &lt; loss.</jats:p>",
    "published": {"date-parts": [[2020, 3, 8]]},
    "type": "proceedings-article",
    "license": [{"URL": "https://doi.org/10.1364/OA_License_v1"}],
    "is-referenced-by-count": 3,
}


def test_doi_year() -> None:
    assert m.doi_year("10.1364/ofc.2026.m1a.1") == 2026
    assert m.doi_year("10.1364/cleo_si.2016.sf1e.3") == 2016
    assert m.doi_year("10.1109/ecoc.2017.8346000") == 2017
    assert m.doi_year("10.1049/icp.2023.1833") == 2023
    assert m.doi_year("10.1109/acp55869.2022.10088643") == 2022
    assert m.doi_year("10.1109/acp/poem59049.2023.10369425") is None


def test_clean() -> None:
    assert m.clean("a &lt; b and <i>c</i>") == "a < b and c"
    assert m.clean("&lt;i&gt;Si&lt;/i&gt; &amp;amp; SiN") == "Si &amp; SiN"
    assert m.clean("Si<sub>3</sub>N<jats:sub>4</jats:sub> ring") == "Si3N4 ring"
    assert m.clean("&lt;p&gt;x&lt;/p&gt;") == "x"
    assert m.clean("Q of 8 × 10<sup>4</sup>, Er<jats:sup>3+</jats:sup>") == "Q of 8 × 10^4, Er^3+"
    assert m.clean(None) == ""


def test_matches_routing_and_year_range() -> None:
    ofc = {"key": "ofc_cr", "doi_regex": r"^10\.1364/ofc\.", "years": [2020, 2025]}
    cleo = {"key": "cleo_cr", "doi_regex": r"^10\.1364/cleo_(si|at|qels|fs)\.", "years": [2020, 2025]}
    assert m.matches(ofc, ITEM)
    assert not m.matches(cleo, ITEM)
    assert not m.matches(ofc, {**ITEM, "DOI": "10.1364/OFC.2026.M1A.4"})
    apc = {"key": "apc_cr", "container_regex": "Advanced Photonics", "years": [2020, 2025]}
    assert not m.matches(apc, ITEM)
    iet = {"key": "e", "item_match": {"volume": "2023", "issue": "34"}, "years": [2023, 2023]}
    assert m.matches(iet, {"DOI": "10.1049/icp.2023.1833", "volume": "2023", "issue": "34"})
    assert not m.matches(iet, {"DOI": "10.1049/icp.2023.1833", "volume": "2023", "issue": "20"})
    assert not m.matches(iet, {"DOI": "10.1049/icp.2024.1804", "volume": "2023", "issue": "34"})
    assert m.matches(
        {**iet, "doi_year_check": False}, {"DOI": "10.1049/icp.2024.1804", "volume": "2023", "issue": "34"}
    )


def test_unit_filter_and_years() -> None:
    v = {"crossref_filter": "prefix:10.1364,type:proceedings-article", "years": [2020, 2022]}
    assert m.unit_filter(v, 2021) == "prefix:10.1364,type:proceedings-article,from-pub-date:2021,until-pub-date:2021"
    assert m.venue_years(v, None) == [2022, 2021, 2020]
    assert m.venue_years(v, (2021, 2030)) == [2022, 2021]
    w = {"crossref_filter_by_year": {2023: "container-title:A,from-pub-date:2023-11-13"}, "years": [2022, 2024]}
    assert m.venue_years(w, None) == [2023]
    assert m.unit_filter(w, 2023) == "container-title:A,from-pub-date:2023-11-13"


def test_from_crossref_fields() -> None:
    r = m.from_crossref(ITEM, "conferences", "crossref:ofc_cr:2020", 2020)
    assert r["uid"] == r["doi"] == "10.1364/ofc.2020.m1a.4"
    assert r["title"] == "Low-loss SiN edge coupler"
    assert r["abstract"] == "We show 0.5 dB < loss."
    assert r["authors"] == ["A. One", "B. Two"] and r["last_author"] == "B. Two" and r["n_authors"] == 2
    assert r["institutions"] == ["Univ X", "Lab & Y"]
    assert r["publication_date"] == "2020-03-08" and r["type"] == "conference-paper"
    assert r["is_oa"] is False and r["cited_by_count"] == 3 and r["venue_type"] == "conference"
    cc = m.from_crossref({**ITEM, "license": [{"URL": "http://creativecommons.org/licenses/by/4.0/"}]}, "c", "v", 2020)
    assert cc["is_oa"] is True and cc["license"].startswith("http://creativecommons.org")


def test_merge_openalex_fills_only_missing() -> None:
    r = m.from_crossref({**ITEM, "abstract": None, "author": []}, "c", "crossref:x:2020", 2020)
    oa = {
        "openalex_id": "W1",
        "abstract": "OA abstract",
        "institutions": ["Inst"],
        "oa_url": "",
        "is_oa": False,
        "oa_status": "closed",
        "license": "",
        "cited_by_count": 9,
    }
    out = m.merge_openalex(r, oa)
    assert out["abstract"] == "OA abstract" and out["institutions"] == ["Inst"] and out["openalex_id"] == "W1"
    assert out["cited_by_count"] == 9 and out["discovered_via"].endswith("+openalex:doi")


def test_config_loads() -> None:
    cfg = m.load_config(ROOT / "config" / "literature" / "venues_conferences.yaml")
    assert cfg["lane"] == "conferences"
    assert all(int(v["years"][1]) <= 2025 for v in cfg["venues"])
