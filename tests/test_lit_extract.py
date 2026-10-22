"""Pure-function tests for the S7 extraction / registration helpers (DevLog-006). No network, no PDFs."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import lit_extract as e  # noqa: E402
import lit_ingest_inbox as ib  # noqa: E402
import lit_register_sources as rs  # noqa: E402


def test_normalize_license() -> None:
    assert e.normalize_license("http://creativecommons.org/licenses/by/4.0/") == "cc-by-4.0"
    assert e.normalize_license("https://creativecommons.org/licenses/by-nc-nd/4.0/") == "cc-by-nc-nd-4.0"
    assert e.normalize_license("http://creativecommons.org/publicdomain/zero/1.0/") == "cc0-1.0"
    assert e.normalize_license("http://arxiv.org/licenses/nonexclusive-distrib/1.0/") == (
        "arxiv-nonexclusive-distrib-1.0"
    )
    assert e.normalize_license("CC-BY") == "cc-by"
    assert e.normalize_license("") == ""


def test_redistribution_rules() -> None:
    r = e.redistribution
    # arXiv copy: only the arXiv license counts (publisher access / OA status do not)
    assert r("arxiv", "cc-by-4.0", "paywalled", "closed", False) == "open_license_ok"
    assert r("arxiv", "arxiv-nonexclusive-distrib-1.0", "oa", "gold", False) == "restricted_local_only"
    assert r("arxiv", "", "oa", "gold", False) == "unknown"
    # publisher / repository copy
    assert r("oa_publisher", "cc-by", "oa", "gold", False) == "open_license_ok"
    assert r("oa_publisher", "cc-by", "oa", "bronze", False) == "restricted_local_only"
    assert r("oa_publisher", "other-oa", "oa", "green", False) == "restricted_local_only"
    assert r("oa_publisher", "", "oa", "green", False) == "unknown"
    assert r("optica_browser", "cc-by", "paywalled", "closed", False) == "restricted_local_only"
    assert r("manual", "cc-by", "oa", "gold", False) == "restricted_local_only"
    assert r("oa_publisher", "cc-by", "oa", "gold", True) == "restricted_local_only"


def test_most_restrictive_and_access() -> None:
    assert e.most_restrictive("open_license_ok", "restricted_local_only") == "restricted_local_only"
    assert e.most_restrictive("open_license_ok", "unknown") == "unknown"
    assert e.most_restrictive("open_license_ok", "") == "open_license_ok"
    assert e.registry_access("arxiv", "paywalled") == "arxiv"
    assert e.registry_access("oa_publisher", "oa") == "open_access"
    assert e.registry_access("manual", "paywalled") == "paywalled"


def test_text_quality_flags_garbled_page() -> None:
    good = "The device is made of silicon and the loss of the waveguide was measured in the lab. " * 10
    bad = "\x01\x02 #$% 1234 ()*+ ,-./ 5678 " * 40
    shifted = "Wkh ghylfh lv pdgh ri vlolfrq dqg wkh orvv zdv phdvxuhg " * 20
    table = "Si\n1540-1560\n20\n0.2\n-40\n[10]\nLNOI\n1500-1680\n180\n0.12\n-40\n[6]\n" * 12
    q = e.text_quality([good, bad, "short", shifted, table])
    assert q["garbled_pages"] == [2, 4] and q["garbled_text_layer"]
    assert not e.text_quality([good, table])["garbled_text_layer"]


def test_captions_and_header() -> None:
    assert e.captions_of("Fig. 1. Layout\nbody\nFIGURE S2 x\nTable II: y\nfigures are nice") == [
        "Fig. 1. Layout",
        "FIGURE S2 x",
        "Table II: y",
    ]
    h = e.yaml_header({"paper_id": "xu2026", "url": "https://arxiv.org/pdf/2511.22820"})
    assert h.startswith('---\npaper_id: "xu2026"\n') and h.endswith("---\n\n")


def test_inbox_names() -> None:
    assert ib.split_name("xu2026") == ("xu2026", False)
    assert ib.split_name("xu2026_supplement") == ("xu2026", True)


def test_register_helpers() -> None:
    assert rs.source_type("review", "journal", "") == "review"
    assert rs.source_type("article", "conference", "") == "conference"
    assert rs.source_type("preprint", "repository", "2512.04886") == "arxiv_preprint"
    assert rs.source_type("", "other", "") == "other"
    assert rs.registry_url("10.1/x", "1", "u") == "https://doi.org/10.1/x"
    assert rs.registry_url("", "2512.04886", "u") == "https://arxiv.org/abs/2512.04886"
    row = rs.lit_row(
        "nan2025",
        {
            "sha256": "x",
            "access": "arxiv",
            "redistribution": "unknown",
            "retrieved_on": "2026-10-22T01:02:03+00:00",
            "text_chars": 10,
            "route": "arxiv",
            "publication_date": "2025-12-04",
        },
        {"title": "T", "year": "2025", "venue": "arXiv", "venue_type": "repository", "arxiv_id": "2512.04886"},
        {},
    )
    assert row["source_id"] == "lit:nan2025" and row["accessed_on"] == "2026-10-22"
    assert row["source_type"] == "arxiv_preprint" and row["text_cached"] is True and row["same_as"] == ""
