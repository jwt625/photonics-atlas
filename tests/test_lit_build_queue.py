"""Pure-function tests for scripts/lit_build_queue.py (title / author matching, Atom parsing, routes, schedule); no
network."""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from types import ModuleType
from typing import Any

from photonics_atlas.paths import ROOT


def _mod() -> ModuleType:
    spec = importlib.util.spec_from_file_location("lit_build_queue", ROOT / "scripts" / "lit_build_queue.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["lit_build_queue"] = mod
    spec.loader.exec_module(mod)
    return mod


q = _mod()

FEED = b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2404.08609v2</id>
    <published>2024-04-12T00:00:00Z</published>
    <title>An ultra-broadband photonic-chip-based
      traveling-wave parametric amplifier</title>
    <author><name>Nikolai Kuznetsov</name></author>
    <author><name>Tobias J. Kippenberg</name></author>
    <arxiv:doi>10.1038/S41586-024-08192-0</arxiv:doi>
    <arxiv:primary_category term="physics.optics"/>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2101.00001v1</id>
    <title>An ultra-broadband photonic-chip-based traveling-wave parametric amplifier</title>
    <author><name>Someone Else</name></author>
  </entry>
</feed>"""


def _row(**kw: str) -> dict[str, Any]:
    base = {
        "paper_id": "p",
        "uid": "",
        "doi": "",
        "arxiv_id": "",
        "title": "",
        "first_author": "",
        "last_author": "",
        "access": "oa",
        "oa_url": "",
        "primary_class": "laser",
        "score": "9",
        "rank": "1",
        "selection_reason": "rank",
    }
    base.update(kw)
    return base


def test_norm_title_tex_and_unicode() -> None:
    assert q.norm_title("Er:Gd$_2$O$_3$ films") == "er gd2o3 films"
    assert q.norm_title("Erbium‐Doped Single‐Crystal") == "erbium doped single crystal"
    assert q.title_sim("Coherency‐Broken Bragg Filters", "Coherency-broken Bragg filters") == 1.0


def test_surnames_share() -> None:
    assert q.surnames_share(["Takeshi MATSUMOTO"], ["T. Matsumoto", "A. B"])
    assert q.surnames_share(["Dorian Oser"], ["D. Oser"])
    assert q.surnames_share(["Xu Xuejun"], ["Xuejun Xu"])  # reversed name order
    assert not q.surnames_share(["Dileep V. Reddy"], ["Guang-Zhao Xu"])
    assert q.surnames_share(["Mateus Corato‐Zanarella"], ["Mateus Corato-Zanarella"])


def test_arxiv_id_from_url_and_given() -> None:
    assert q.arxiv_id_from_url("https://arxiv.org/pdf/1806.08833") == "1806.08833"
    assert q.arxiv_id_from_url("http://arxiv.org/abs/2101.00001v3") == "2101.00001"
    assert q.arxiv_id_from_url("https://doi.org/10.1364/oe.1") == ""
    m = q.given_match(_row(oa_url="https://arxiv.org/pdf/1806.08833"))
    assert m is not None and (m.arxiv_id, m.kind) == ("1806.08833", "given")
    assert q.given_match(_row()) is None


def _index() -> Any:
    recs = [
        q.PoolRec("2404.08609", {"10.1038/s41586-024-08192-0"}, "T1", q.norm_title("T1"), ["N. Kuznetsov"]),
        q.PoolRec(
            "2009.02855",
            set(),
            "High-efficient coupler for thin-film lithium niobate waveguide devices",
            q.norm_title("High-efficient coupler for thin-film lithium niobate waveguide devices"),
            ["Changran Hu", "Bin Wang"],
        ),
    ]
    return q.PoolIndex(recs)


def test_local_match_doi_then_title() -> None:
    idx = _index()
    m = q.local_match(_row(doi="10.1038/S41586-024-08192-0", title="Other"), idx)
    assert m is not None and (m.arxiv_id, m.kind) == ("2404.08609", "doi")
    t = "High-efficient coupler for thin-film lithium niobate waveguide devices."
    m = q.local_match(_row(title=t, first_author="Changran Hu"), idx)
    assert m is not None and m.kind == "title" and (m.score or 0) >= 0.93
    assert q.local_match(_row(title=t, first_author="Nobody Here", last_author="Also Nobody"), idx) is None


def test_parse_and_pick_api_hit() -> None:
    hits = q.parse_hits(FEED)
    assert [h["arxiv_id"] for h in hits] == ["2404.08609", "2101.00001"]
    assert hits[0]["doi"] == "10.1038/s41586-024-08192-0"
    row = _row(
        title="An ultra-broadband photonic-chip-based traveling-wave parametric amplifier",
        first_author="Nikolai Kuznetsov",
        last_author="Tobias J. Kippenberg",
    )
    m = q.pick_api_hit(row, hits)
    assert m is not None and (m.arxiv_id, m.kind) == ("2404.08609", "api")
    # retitled journal version: similarity 0.887 < 0.93, rejected
    row2 = dict(row, title="An ultra-broadband photonic-chip-based parametric amplifier")
    assert q.pick_api_hit(row2, hits) is None
    assert q.query_title("Er:Gd$_2$O$_3$ on Si (100)") == "Er Gd2O3 on Si 100"


def test_route_for() -> None:
    assert q.route_for(_row(doi="10.1364/oe.1"), "2101.00001") == ("arxiv", "https://arxiv.org/pdf/2101.00001")
    assert q.route_for(_row(doi="10.1364/oe.1", access="paywalled"), "")[0] == "optica_browser"
    assert q.route_for(_row(doi="10.1364/oe.1", oa_url="https://doi.org/10.1364/oe.1"), "")[0] == "optica_browser"
    assert q.route_for(_row(doi="10.23919/ecoc.1", access="paywalled"), "") == (
        "ieee_browser",
        "https://doi.org/10.23919/ecoc.1",
    )
    assert q.route_for(_row(doi="10.1038/x", oa_url="https://hal.science/x.pdf"), "")[0] == "oa_publisher"
    assert q.route_for(_row(doi="10.1038/x", access="paywalled"), "") == ("manual", "https://doi.org/10.1038/x")


def _synthetic_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    classes = ["a", "b", "c", "d"]
    for i in range(437):
        rows.append(
            dict(
                _row(paper_id=f"o{i}", primary_class=classes[i % 4], score=str(i % 10)),
                route="optica_browser" if i < 237 else "ieee_browser" if i < 337 else "arxiv",
            )
        )
    return rows


def test_assign_days_balanced_and_capped() -> None:
    rows = _synthetic_rows()
    n = q.assign_days(rows, 5, {"optica_browser": 40})
    assert n == 6  # 237 optica > 40 x 5: tail of 37 on 1 extra day
    per = Counter((r["route"], r["day"]) for r in rows)
    assert max(v for (rt, d), v in per.items() if rt == "optica_browser") <= 40
    for rt in ("ieee_browser", "arxiv"):
        counts = [per[(rt, d)] for d in range(1, 6)]
        assert max(counts) - min(counts) <= 1
    per_cls = Counter((r["primary_class"], r["day"]) for r in rows if r["route"] == "ieee_browser")
    for c in "abcd":
        counts = [per_cls[(c, d)] for d in range(1, 6)]
        assert max(counts) - min(counts) <= 1


def test_split_sessions_and_order() -> None:
    assert q.split_sessions(0, 20) == []
    assert q.split_sessions(20, 20) == [20]
    assert q.split_sessions(33, 20) == [17, 16]
    assert q.split_sessions(61, 30) == [21, 20, 20]
    rows = _synthetic_rows()
    n = q.assign_days(rows, 5, {"optica_browser": 40})
    out = q.order_and_sessions(rows, n)
    assert len(out) == len(rows)
    sess = Counter((q.SITE[r["route"]], r["session"]) for r in out if r["route"] in q.SITE)
    for (site, _s), v in sess.items():
        assert v <= q.SESSION_CAP[site]
    # class round-robin inside a (day, route) group
    d1 = [r["primary_class"] for r in out if r["day"] == 1 and r["route"] == "ieee_browser"]
    assert len(set(d1[:4])) == 4


def test_priority_curator_first() -> None:
    a = _row(paper_id="a", score="10", selection_reason="rank")
    b = _row(paper_id="b", score="7", selection_reason="curator: benchmark")
    assert sorted([a, b], key=q.priority)[0]["paper_id"] == "b"


CROSSREF_MSG: dict[str, Any] = {
    "message": {
        "items": [
            {
                "DOI": "10.23919/OFC49934.2023.10117440",
                "title": ["8-Channel CWDM TOSA for CPO External Laser Sources"],
                "author": [{"given": "Hiroshi", "family": "Sawamura"}],
                "issued": {"date-parts": [[2023, 3]]},
                "container-title": ["2023 Optical Fiber Communications Conference and Exhibition (OFC)"],
            },
            {"DOI": "10.1109/jphot.2017.1", "title": ["Unrelated"], "issued": {"date-parts": [[2017]]}},
        ]
    }
}


def test_crossref_ieee_twin() -> None:
    hits = q.crossref_hits(CROSSREF_MSG)
    assert hits[0]["doi"] == "10.23919/ofc49934.2023.10117440" and hits[0]["year"] == 2023
    assert hits[0]["authors"] == ["Hiroshi Sawamura"]
    row = _row(
        doi="10.1364/ofc.2023.w4b.1",
        access="paywalled",
        venue_type="conference",
        year="2023",
        title="8-Channel CWDM TOSA for CPO External Laser Sources",
        first_author="H. Sawamura",
    )
    assert q.pick_ieee_hit(row, hits) == ("10.23919/ofc49934.2023.10117440", 1.0)
    assert q.pick_ieee_hit(dict(row, year="2026"), hits) is None  # year outside +-1
    assert q.pick_ieee_hit(dict(row, venue_type="journal"), hits) is None  # journal: conference paper is not a copy
    assert (
        q.needs_ieee_twin(row)
        and not q.needs_ieee_twin(dict(row, doi="10.1109/x"))
        and not q.needs_ieee_twin(dict(row, access="oa"))
    )
    assert q.route_for(row, "", "10.23919/ofc49934.2023.10117440") == (
        "ieee_browser",
        "https://doi.org/10.23919/ofc49934.2023.10117440",
    )
    assert q.route_for(row, "2101.00001", "10.23919/x")[0] == "arxiv"  # arXiv copy preferred


def test_publisher_browser_route() -> None:
    nat = _row(doi="10.1038/s41566-1", oa_url="https://www.nature.com/articles/s41566-1.pdf")
    assert q.route_for(nat, "") == ("publisher_browser", "https://www.nature.com/articles/s41566-1.pdf")
    assert q.route_for(dict(nat, oa_url="https://doi.org/10.1038/s41566-1"), "")[0] == "publisher_browser"
    assert q.route_for(dict(nat, oa_url="https://biblio.ugent.be/x.pdf"), "")[0] == "oa_publisher"  # repository
    assert q.route_for(_row(doi="10.1016/j.x", oa_url="https://doi.org/10.1016/j.x"), "")[0] == "oa_publisher"
    assert q.route_for(_row(doi="10.1088/x", oa_url="https://iopscience.iop.org/x/pdf"), "")[0] == "publisher_browser"
    assert q.route_for(nat, "2101.00001")[0] == "arxiv"


def test_ieee_search_and_aip_manual() -> None:
    conf = _row(doi="10.1364/acpc.2021.t4a.130", access="paywalled", venue_type="conference")
    assert q.route_for(conf, "") == ("ieee_search", "https://doi.org/10.1364/acpc.2021.t4a.130")
    assert q.route_for(dict(conf, venue_type=""), "")[0] == "ieee_search"  # conference DOI pattern
    assert q.route_for(dict(conf, doi="10.1364/ol.1", venue_type="journal"), "")[0] == "optica_browser"
    assert q.route_for(dict(conf, access="oa"), "")[0] == "optica_browser"
    assert q.route_for(conf, "", "10.23919/ofc.1")[0] == "ieee_browser"  # Crossref twin first
    assert q.route_for(conf, "2101.00001")[0] == "arxiv"
    aip = _row(doi="10.1063/5.1", oa_url="https://pubs.aip.org/x.pdf")
    assert q.route_for(aip, "") == ("manual", "https://pubs.aip.org/x.pdf")
    assert q.route_for(dict(aip, oa_url="https://doi.org/10.1063/5.1"), "")[0] == "manual"


def test_ieee_routes_share_sessions() -> None:
    rows = [dict(_row(paper_id=f"b{i}", primary_class="ab"[i % 2]), route="ieee_browser", day=1) for i in range(20)] + [
        dict(_row(paper_id=f"s{i}", primary_class="ab"[i % 2]), route="ieee_search", day=1) for i in range(15)
    ]
    out = q.order_and_sessions(rows, 1)
    assert Counter(r["session"] for r in out) == Counter({1: 18, 2: 17})


def test_delta_slots_keeps_rows_and_hands_over_day_slots() -> None:
    def qrow(pid: str, day: int, route: str, session: str, cls: str) -> dict[str, str]:
        return {
            "day": str(day), "date": f"d{day}", "route": route, "session": session, "paper_id": pid, "uid": pid,
            "doi": "", "arxiv_id": "", "arxiv_match": "", "arxiv_match_score": "", "ieee_doi": "",
            "ieee_match_score": "", "route_url": "", "access": "oa", "primary_class": cls, "score": "9",
            "title": pid, "status": "",
        }  # fmt: skip

    old = [
        qrow("a", 1, "optica_browser", "1", "laser"),
        qrow("b", 3, "optica_browser", "5", "laser"),
        qrow("c", 3, "arxiv", "", "wdm"),
        qrow("d", 3, "ieee_browser", "3", "wdm"),
    ]

    def new(pid: str, route: str, cls: str) -> dict[str, Any]:
        return {"paper_id": pid, "uid": pid, "route": route, "primary_class": cls, "score": "9", "rank": "1",
                "selection_reason": "rank", "arxiv_id_q": "", "arxiv_match": ""}  # fmt: skip

    rows = [
        new("a", "arxiv", "laser"),
        new("x", "arxiv", "laser"),
        new("c", "arxiv", "wdm"),
        new("y", "ieee_browser", "wdm"),
    ]
    out = q.delta_slots(rows, old, 2)
    assert [r["paper_id"] for r in out] == ["a", "x", "c", "y"]
    assert out[0]["_verbatim"] is old[0] and out[0]["route"] == "optica_browser"  # kept as queued
    assert (out[1]["day"], out[1]["session"]) == (3, "")  # arxiv takes the optica slot's day, no session
    assert (out[3]["day"], out[3]["session"]) == (3, 3)  # same site: the displaced row's session
    try:
        q.delta_slots([new("x", "arxiv", "laser"), *rows[1:]], old, 2)  # displaces day-1 row a
    except ValueError as e:
        assert "frozen" in str(e)
    else:
        raise AssertionError("frozen displacement not rejected")
