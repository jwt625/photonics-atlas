"""Pure-function tests for scripts/lit_harvest_arxiv.py (Atom parsing, record mapping, windows); no network."""

from __future__ import annotations

import datetime as dt
import importlib.util
import sys
from types import ModuleType

import pytest

from photonics_atlas.paths import ROOT


def _mod() -> ModuleType:
    spec = importlib.util.spec_from_file_location("lit_harvest_arxiv", ROOT / "scripts" / "lit_harvest_arxiv.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["lit_harvest_arxiv"] = mod
    spec.loader.exec_module(mod)
    return mod


h = _mod()

FEED = b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/"
      xmlns:arxiv="http://arxiv.org/schemas/atom">
  <opensearch:totalResults>1</opensearch:totalResults>
  <entry>
    <id>http://arxiv.org/abs/2609.00001v3</id>
    <updated>2026-10-01T10:00:00Z</updated>
    <published>2026-09-01T17:59:59Z</published>
    <title>A test
      title</title>
    <summary>  Line one
      line two. </summary>
    <author><name>A. First</name><arxiv:affiliation>Uni X</arxiv:affiliation></author>
    <author><name>B. Last</name></author>
    <arxiv:doi>10.1364/OE.1.000001 10.1364/OE.1.000002</arxiv:doi>
    <arxiv:journal_ref>Opt. Express 1, 1 (2026)</arxiv:journal_ref>
    <arxiv:primary_category term="physics.optics"/>
    <category term="physics.optics"/>
    <category term="quant-ph"/>
  </entry>
</feed>"""


def test_parse_and_record() -> None:
    feed = h.parse_feed(FEED)
    assert feed.total == 1 and len(feed.entries) == 1
    r = h.to_record(feed.entries[0], "via", "2026-10-21")
    assert r["uid"] == "arxiv:2609.00001" and r["arxiv_id"] == "2609.00001"
    assert r["title"] == "A test title" and r["abstract"] == "Line one line two."
    assert r["doi"] == "10.1364/oe.1.000001" and len(r["arxiv_dois"]) == 2
    assert r["publication_date"] == "2026-09-01" and r["year"] == 2026
    assert r["authors"] == ["A. First", "B. Last"] and r["last_author"] == "B. Last"
    assert r["institutions"] == ["Uni X"]
    assert r["arxiv_primary"] == "physics.optics" and r["arxiv_categories"] == ["physics.optics", "quant-ph"]
    assert r["oa_url"] == "https://arxiv.org/pdf/2609.00001" and r["venue_type"] == "repository"


def test_api_error_entry() -> None:
    err = FEED.replace(b"http://arxiv.org/abs/2609.00001v3", b"http://arxiv.org/api/errors#bad")
    with pytest.raises(h.HarvestError):
        h.parse_feed(err)


def test_ids_months_query() -> None:
    assert h.arxiv_id_from_url("http://arxiv.org/abs/quant-ph/0101001v1") == "quant-ph/0101001"
    assert h.month_list("2025-11", "2026-02") == [(2026, 2), (2026, 1), (2025, 12), (2025, 11)]
    q = h.date_query(h.SET_QUERY["appq"], dt.date(2026, 9, 1), dt.date(2026, 9, 30))
    assert q.endswith("submittedDate:[202609010000 TO 202609302359] ANDNOT cat:physics.optics")
