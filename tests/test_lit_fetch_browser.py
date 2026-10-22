"""Pure-function tests for scripts/lit_fetch_browser.py (URL / arnumber / uri parsing, challenge and paywall
classification, rolling-window cap arithmetic, target selection); no browser, no network."""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
import sys
from types import ModuleType

from photonics_atlas.paths import ROOT


def _mod() -> ModuleType:
    spec = importlib.util.spec_from_file_location("lit_fetch_browser", ROOT / "scripts" / "lit_fetch_browser.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["lit_fetch_browser"] = mod
    spec.loader.exec_module(mod)
    return mod


m = _mod()
IEEE = m.SITES["ieee"]
OPTICA = m.SITES["optica"]
UTC = dt.UTC


def test_doi_ok() -> None:
    assert m.doi_ok(IEEE, "10.1109/JLT.2018.2870128")
    assert m.doi_ok(IEEE, "10.23919/ofc.2020.123")
    assert not m.doi_ok(IEEE, "10.1364/oe.562888")
    assert m.doi_ok(OPTICA, " 10.1364/OE.562888")
    assert not m.doi_ok(OPTICA, "10.1038/s41586-020-1234-5")


def test_arnumber_from_url() -> None:
    assert m.arnumber_from_url("https://ieeexplore.ieee.org/document/8464270/") == "8464270"
    assert m.arnumber_from_url("https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8464270") == "8464270"
    assert m.arnumber_from_url("https://ieeexplore.ieee.org/ielx7/50/8643941/08464270.pdf") is None
    assert m.arnumber_from_url("") is None


def test_optica_uri_from_url() -> None:
    assert m.optica_uri_from_url("https://opg.optica.org/oe/fulltext.cfm?uri=oe-31-25-41570&id=541234") == (
        "oe",
        "oe-31-25-41570",
    )
    assert m.optica_uri_from_url("https://opg.optica.org/optica/abstract.cfm?uri=optica-7-4-1234") == (
        "optica",
        "optica-7-4-1234",
    )
    assert m.optica_uri_from_url("https://opg.optica.org/viewmedia.cfm?uri=oe-31-25-41570&seq=0") == (
        None,
        "oe-31-25-41570",
    )
    assert m.optica_uri_from_url("https://example.org/oe/fulltext.cfm?uri=x") == (None, None)
    assert m.optica_uri_from_url("https://opg.optica.org/oe/home.cfm") == (None, None)


def test_optica_pdf_url_meta_link_and_fallback() -> None:
    page = "https://opg.optica.org/oe/fulltext.cfm?uri=oe-31-25-41570&id=1"
    meta = (
        '<meta name="citation_pdf_url" content="https://opg.optica.org/oe/viewmedia.cfm?uri=oe-31-25-41570&amp;seq=0">'
    )
    assert m.optica_pdf_url(meta, page) == "https://opg.optica.org/oe/viewmedia.cfm?uri=oe-31-25-41570&seq=0"
    rev = '<meta content="/oe/viewmedia.cfm?uri=oe-1-1-1&amp;seq=0" name="citation_pdf_url">'
    assert m.optica_pdf_url(rev, page) == "https://opg.optica.org/oe/viewmedia.cfm?uri=oe-1-1-1&seq=0"
    link = '<a class="pdf" href="/oe/viewmedia.cfm?uri=oe-31-25-41570&amp;seq=0&amp;html=true">PDF</a>'
    assert m.optica_pdf_url(link, page) == (
        "https://opg.optica.org/oe/viewmedia.cfm?uri=oe-31-25-41570&seq=0&html=true"
    )
    assert m.optica_pdf_url("<html></html>", page) == (
        "https://opg.optica.org/oe/viewmedia.cfm?uri=oe-31-25-41570&seq=0"
    )
    assert m.optica_pdf_url("<html></html>", "https://doi.org/10.1364/oe.1") is None


def test_embedded_pdf_url() -> None:
    base = "https://opg.optica.org/oe/viewmedia.cfm?uri=x&seq=0"
    html = '<iframe src="/directpdfaccess/abc/oe-1-1-1.pdf?da=1&amp;seq=0"></iframe>'
    assert m.embedded_pdf_url(html, base) == "https://opg.optica.org/directpdfaccess/abc/oe-1-1-1.pdf?da=1&seq=0"
    assert m.embedded_pdf_url('<iframe src="/ads/banner.html"></iframe>', base) is None
    assert m.embedded_pdf_url('<a href="/directpdfaccess/q/x.pdf">x</a>', base) == (
        "https://opg.optica.org/directpdfaccess/q/x.pdf"
    )


def test_ieee_pdf_url() -> None:
    html = '<iframe src="/stampPDF/getPDF.jsp?tp=&amp;arnumber=8464270&amp;ref=abc"></iframe>'
    assert (
        m.ieee_pdf_url(html, "8464270")
        == "https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber=8464270&ref=abc"
    )
    assert m.ieee_pdf_url("<html/>", "1") == "https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber=1&ref="


def test_challenge_detection() -> None:
    for html in (
        "<html><head><title>Just a moment...</title></head><body>cf_chl_opt</body></html>",
        "<script>window.awsWafCookieDomainList = [];</script>",
        '<div id="challenge-container"></div>',
        "<title>Access Denied</title> You don't have permission to access this server. Reference #18.1",
        "<div class='g-recaptcha'>please solve the captcha</div>",
        "Our systems have detected unusual traffic from your network",
    ):
        assert m.is_challenge(html), html
        assert m.classify_html(html) == "challenge"
    assert m.is_challenge("<html>ok</html>", status=429)
    assert m.is_challenge("", status=403)
    # captcha script on a real article page is not a challenge
    article = '<meta name="citation_title" content="X"><script src="recaptcha/api.js"></script>'
    assert not m.is_challenge(article)
    assert not m.is_challenge("<html><body>Integrated photonics</body></html>", status=200)


def test_classify_paywall_and_other() -> None:
    assert m.classify_html("<html>Purchase this article ... Get Access</html>") == "no_access"
    assert m.classify_html("<html>Login to access this content</html>") == "no_access"
    assert m.classify_html("<html><body>Something else</body></html>") == "not_pdf"


def test_is_pdf() -> None:
    assert m.is_pdf(b"%PDF-1.7\n" + b"0" * 30000)
    assert not m.is_pdf(b"%PDF-1.7\n" + b"0" * 100)
    assert not m.is_pdf(b"<html>" + b"0" * 30000)
    assert m.is_pdf(b"%PDF-1.4", min_bytes=1)


def _line(ts: str, route: str = "optica_browser", status: str = "saved") -> str:
    return json.dumps({"ts": ts, "paper_id": "p", "route": route, "status": status, "bytes": 1, "sha256": ""})


def test_saved_times_filters_route_status_window() -> None:
    now = dt.datetime(2026, 10, 22, 12, 0, tzinfo=UTC)
    lines = [
        _line("2026-10-22T09:59:00+00:00"),  # outside 2 h
        _line("2026-10-22T10:00:00+00:00"),  # boundary: inside
        _line("2026-10-22T11:00:00+00:00", route="ieee_browser"),
        _line("2026-10-22T11:10:00+00:00", status="no_access"),
        _line("2026-10-22T11:30:00"),  # naive: read as UTC
        _line("2026-10-22T11:45:00+00:00", status="ok"),  # stream R2 convention
        "not json",
        json.dumps({"route": "optica_browser", "status": "saved"}),
    ]
    got = m.saved_times(lines, "optica_browser", now, 2.0)
    assert got == [
        dt.datetime(2026, 10, 22, 10, 0, tzinfo=UTC),
        dt.datetime(2026, 10, 22, 11, 30, tzinfo=UTC),
        dt.datetime(2026, 10, 22, 11, 45, tzinfo=UTC),
    ]


def test_cap_wait_s() -> None:
    now = dt.datetime(2026, 10, 22, 12, 0, tzinfo=UTC)
    times = [now - dt.timedelta(minutes=110 - i) for i in range(60)]  # oldest 110 min ago
    assert m.cap_wait_s(times[:59], 60, 2.0, now) == 0.0
    assert m.cap_wait_s(times, 60, 2.0, now) == 600.0  # oldest frees in 10 min
    more = [now - dt.timedelta(minutes=115), *times]  # 61 in window: the 2nd oldest must age out
    assert m.cap_wait_s(more, 60, 2.0, now) == 600.0
    assert m.cap_wait_s([now - dt.timedelta(hours=3)] * 60, 60, 2.0, now) == 0.0
    assert m.cap_wait_s([], 60, 2.0, now) == 0.0


def test_select_targets_queue_day_session_and_ids() -> None:
    q = [
        {
            "day": "1",
            "route": "optica_browser",
            "session": "1",
            "paper_id": "a",
            "doi": "10.1364/oe.1",
            "route_url": "",
        },
        {
            "day": "1",
            "route": "optica_browser",
            "session": "2",
            "paper_id": "b",
            "doi": "10.1364/oe.2",
            "route_url": "u",
        },
        {"day": "1", "route": "ieee_browser", "session": "1", "paper_id": "c", "doi": "10.1109/jlt.3", "route_url": ""},
        {
            "day": "2",
            "route": "optica_browser",
            "session": "1",
            "paper_id": "d",
            "doi": "10.1364/oe.4",
            "route_url": "",
        },
        {"day": "1", "route": "arxiv", "session": "1", "paper_id": "e", "doi": "10.1364/oe.5", "route_url": ""},
    ]
    c = [{"paper_id": "z", "doi": "10.1364/OE.9"}, {"paper_id": "y", "doi": "10.1038/x"}]
    t, w = m.select_targets(q, c, OPTICA, 1, None, None)
    assert [x["paper_id"] for x in t] == ["a", "b"] and not w
    t, _ = m.select_targets(q, c, OPTICA, 1, "2", None)
    assert [(x["paper_id"], x["route_url"]) for x in t] == [("b", "u")]
    t, _ = m.select_targets(q, c, IEEE, 1, None, None)
    assert [x["paper_id"] for x in t] == ["c"]
    t, w = m.select_targets(q, c, OPTICA, None, None, ["z", "a", "y", "missing"])
    assert [(x["paper_id"], x["doi"]) for x in t] == [("z", "10.1364/oe.9"), ("a", "10.1364/oe.1")]
    assert len(w) == 2


def test_classify_nav_page() -> None:
    interstitial = (
        "<head><title>OPG</title></head><body><p>Please wait...</p>"
        "<script>fetch('/checkjs.cfm?s=1%7CAB&x=1').then(function(){window.location.replace('/viewmedia.cfm?r=1');});"
        "</script></body>"
    )
    assert m.JSCHECK_RE.search(interstitial)
    assert m.classify_nav_page(interstitial) == "challenge"
    assert m.classify_nav_page("<title>Just a moment...</title>") == "challenge"
    abstract = '<meta name="citation_title" content="Grating coupler"><meta name="citation_pdf_url" content="x">'
    assert m.classify_nav_page(abstract) == "no_access"
    assert m.classify_nav_page("<html>Purchase this article</html>") == "no_access"
    assert m.classify_nav_page("<html>unexpected</html>") == "not_pdf"


PUB = m.SITES["publisher"]


def test_publisher_host_and_breaker_paths() -> None:
    assert m.publisher_host("10.1038/s41586-025-08824-3") == "www.nature.com"
    assert m.publisher_host("10.1002/LPOR.201900364") == "onlinelibrary.wiley.com"
    assert m.publisher_host("10.1063/5.0194677") == "pubs.aip.org"
    assert m.publisher_host("10.1021/acsphotonics.3c00834") == "pubs.acs.org"
    assert m.publisher_host("10.1088/2631-7990/abc674") == "iopscience.iop.org"
    assert m.publisher_host("10.1515/nanoph-2023-0524") == "www.degruyterbrill.com"
    assert m.publisher_host("10.1364/oe.1") is None
    assert m.doi_ok(PUB, "10.1038/x") and not m.doi_ok(PUB, "10.1364/oe.1")
    assert m.breaker_key(PUB, "10.1038/x") == "www.nature.com"
    assert m.breaker_key(OPTICA, "10.1364/oe.1") is None
    assert m.breaker_path(PUB, "www.nature.com").name == ".lit_browser_blocked_publisher_www.nature.com.json"
    assert m.breaker_path(OPTICA).name == ".lit_browser_blocked_optica.json"


def test_publisher_pdf_url_meta_first() -> None:
    meta = '<meta name="citation_pdf_url" content="https://pubs.aip.org/aip/app/article-pdf/doi/10.1063/5.0194677/1989509/016105_1_5.0194677.pdf">'
    url = "https://pubs.aip.org/aip/app/article/9/1/016105/3000000/Title"
    assert m.publisher_pdf_url(meta, url, "10.1063/5.0194677") == (
        "https://pubs.aip.org/aip/app/article-pdf/doi/10.1063/5.0194677/1989509/016105_1_5.0194677.pdf"
    )
    nat = '<meta name="citation_pdf_url" content="https://www.nature.com/articles/s41467-019-08369-w.pdf"/>'
    assert m.publisher_pdf_url(
        nat, "https://www.nature.com/articles/s41467-019-08369-w", "10.1038/s41467-019-08369-w"
    ) == ("https://www.nature.com/articles/s41467-019-08369-w.pdf")


def test_publisher_pdf_url_patterns_without_meta() -> None:
    f = m.publisher_pdf_url
    assert f("", "https://www.nature.com/articles/s41586-025-08824-3", "10.1038/s41586-025-08824-3") == (
        "https://www.nature.com/articles/s41586-025-08824-3.pdf"
    )
    assert f("", "https://www.nature.com/search?q=x", "10.1038/x") is None
    # Wiley: always pdfdirect, on the landing host, even when the meta points at the /doi/pdf/ reader
    wmeta = '<meta name="citation_pdf_url" content="https://onlinelibrary.wiley.com/doi/pdf/10.1002/lpor.201900364">'
    assert f(wmeta, "https://onlinelibrary.wiley.com/doi/full/10.1002/lpor.201900364", "10.1002/LPOR.201900364") == (
        "https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/lpor.201900364"
    )
    assert f("", "https://advanced.onlinelibrary.wiley.com/doi/10.1002/adem.202402095", "10.1002/adem.202402095") == (
        "https://advanced.onlinelibrary.wiley.com/doi/pdfdirect/10.1002/adem.202402095"
    )
    assert f("", "https://pubs.acs.org/doi/10.1021/acsphotonics.3c00834", "10.1021/acsphotonics.3c00834") == (
        "https://pubs.acs.org/doi/pdf/10.1021/acsphotonics.3c00834"
    )
    assert f("", "https://iopscience.iop.org/article/10.1088/2631-7990/abc674", "10.1088/2631-7990/abc674") == (
        "https://iopscience.iop.org/article/10.1088/2631-7990/abc674/pdf"
    )
    assert f(
        "", "https://www.degruyterbrill.com/document/doi/10.1515/nanoph-2024-0320/html", "10.1515/nanoph-2024-0320"
    ) == ("https://www.degruyterbrill.com/document/doi/10.1515/nanoph-2024-0320/pdf")
    aip = '<a class="pdf" href="/aip/apl/article-pdf/doi/10.1063/5.0221309/2008242/x.pdf">PDF</a>'
    assert f(aip, "https://pubs.aip.org/aip/apl/article/125/1/1/1/T", "10.1063/5.0221309") == (
        "https://pubs.aip.org/aip/apl/article-pdf/doi/10.1063/5.0221309/2008242/x.pdf"
    )
    assert f("", "https://pubs.aip.org/aip/apl/article/125/1/1/1/T", "10.1063/5.0221309") is None
    assert f("", "https://example.org/a", "10.1038/x") is None


def test_challenge_signatures_ignored_on_article_pages() -> None:
    # Cloudflare bot-management script and WAF SDK on an ordinary article page are not a challenge
    page = (
        '<meta name="citation_doi" content="10.1002/x"><script src="/cdn-cgi/challenge-platform/scripts/jsd/main.js">'
    )
    assert not m.is_challenge(page + "<script>AwsWafIntegration</script>")
    assert m.is_challenge('<script>window.gokuProps = {"key": "x"}</script><script src="challenge.js"></script>')


TITLE = "Compact Silicon Photonic Waveguide Crossings with Sub- 10-mdB Loss"


def _rec(an: str, title: str, *names: str) -> dict[str, object]:
    return {"articleNumber": an, "articleTitle": title, "authors": [{"preferredName": n} for n in names]}


def test_norm_and_similarity() -> None:
    assert m.norm_match_title("Sub-10-mdB <i>Loss</i> &amp; Rönn") == "sub 10 mdb loss ronn"
    assert m.title_similarity(TITLE, "Compact silicon photonic waveguide crossings with sub-10-mdB loss") == 1.0
    assert m.title_similarity(TITLE, "") == 0.0
    assert m.title_similarity(TITLE, "Low-loss silicon nitride waveguide crossings") < 0.93


def test_surnames() -> None:
    assert m.surnames("Yingying Peng", "Daoxin Dai") == {"peng", "dai"}
    assert m.surnames("Takeshi MATSUMOTO") == {"matsumoto"}
    assert m.surnames("MATSUMOTO Takeshi") == {"takeshi", "matsumoto"}
    assert m.surnames("John Rönn", "") == {"ronn"}
    assert m.surnames("") == set()


def test_search_body() -> None:
    b = m.search_body('A "quoted"  title\n here')
    assert b["queryText"] == '"A quoted title here"'
    assert b["rowsPerPage"] == 10 and b["newsearch"] is True


def test_best_xplore_hit() -> None:
    names = m.surnames("Yingying Peng", "Daoxin Dai")
    good = _rec(
        "9738431", "Compact Silicon Photonic Waveguide Crossings with Sub-10-mdB Loss", "Yingying Peng", "D. Dai"
    )
    other_auth = _rec("1111111", "Compact Silicon Photonic Waveguide Crossings with Sub-10-mdB Loss", "A. Smith")
    near = _rec("2222222", "Compact Silicon Photonic Waveguide Crossings", "Yingying Peng")
    an, score = m.best_xplore_hit([other_auth, near, good], TITLE, names)
    assert an == "9738431" and score == 1.0
    # title match without a shared surname is rejected; the best similarity seen is still reported
    an, score = m.best_xplore_hit([other_auth], TITLE, names)
    assert an is None and score == 1.0
    # shared surname but similarity < 0.93 is rejected
    an, score = m.best_xplore_hit([near], TITLE, names)
    assert an is None and 0 < score < 0.93
    assert m.best_xplore_hit([], TITLE, names) == (None, 0.0)
    assert m.best_xplore_hit([good], TITLE, set()) == (None, 1.0)


def test_select_targets_ieee_search_and_ieee_doi() -> None:
    q = [
        {
            "day": "3",
            "route": "ieee_search",
            "session": "1",
            "paper_id": "peng2021",
            "doi": "10.1364/acpc.2021.t4a.130",
            "title": TITLE,
            "route_url": "",
        },
        {
            "day": "3",
            "route": "ieee_browser",
            "session": "1",
            "paper_id": "wang2023d",
            "doi": "10.1364/ofc.2023.w2b.1",
            "ieee_doi": "10.23919/ofc49934.2023.10117020",
            "title": "T",
            "route_url": "",
        },
        {
            "day": "3",
            "route": "ieee_search",
            "session": "1",
            "paper_id": "notitle",
            "doi": "10.1364/x",
            "title": "",
            "route_url": "",
        },
    ]
    c = [{"paper_id": "peng2021", "first_author": "Yingying Peng", "last_author": "Daoxin Dai", "title": TITLE}]
    t, w = m.select_targets(q, c, IEEE, 3, None, None)
    assert [(x["paper_id"], x["route"], x["doi"]) for x in t] == [
        ("peng2021", "ieee_search", "10.1364/acpc.2021.t4a.130"),
        ("wang2023d", "ieee_browser", "10.23919/ofc49934.2023.10117020"),
    ]
    assert t[0]["first_author"] == "Yingying Peng" and t[0]["last_author"] == "Daoxin Dai"
    assert w == ["notitle: no title for the Xplore search"]
    t, w = m.select_targets(q, c, OPTICA, None, None, ["peng2021"])
    assert not t and "needs --site ieee" in w[0]
    t, _ = m.select_targets(q, c, IEEE, None, None, ["peng2021"])
    assert t[0]["route"] == "ieee_search"


def test_saved_times_route_tuple() -> None:
    now = dt.datetime(2026, 10, 22, 12, 0, tzinfo=UTC)
    lines = [
        _line("2026-10-22T11:00:00+00:00", route="ieee_search", status="ok"),
        _line("2026-10-22T11:10:00+00:00", route="ieee_browser"),
    ]
    assert len(m.saved_times(lines, m.site_routes(IEEE), now, 2.0)) == 2
    assert len(m.saved_times(lines, "ieee_browser", now, 2.0)) == 1
