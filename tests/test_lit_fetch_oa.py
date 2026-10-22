"""Pure-function tests for the S7 open-access fetcher (DevLog-006). No network, no files."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import lit_fetch_oa as f  # noqa: E402

PDF = b"%PDF-1.7\n" + b"x" * 30_000


def test_spacing_and_exclusion() -> None:
    assert f.spacing_for("arxiv.org") == (5.0, 3.0)
    assert f.spacing_for("www.nature.com")[0] >= 15.0
    assert f.spacing_for("biblio.ugent.be")[0] >= 15.0
    for h in ("opg.optica.org", "www.osapublishing.org", "ieeexplore.ieee.org", "optica.org"):
        assert f.excluded_host(h)
    for h in ("preprints.opticaopen.org", "www.nature.com", "notieee.org.example.com"):
        assert not f.excluded_host(h)


def test_browser_only() -> None:
    assert f.browser_only("https://doi.org/10.1364/oe.1.000001", "10.1364/oe.1.000001")
    assert f.browser_only("https://doi.org/10.1109/jlt.2020.1", "10.1109/jlt.2020.1")
    assert f.browser_only("https://opg.optica.org/x.pdf", "")
    # green repository copy of an Optica paper is fine
    assert not f.browser_only("https://biblio.ugent.be/publication/1/file/2.pdf", "10.1364/ol.32.002801")
    assert not f.browser_only("https://doi.org/10.1063/1.5000384", "10.1063/1.5000384")


def test_arxiv_url_latest_version() -> None:
    assert f.arxiv_pdf_url("2511.22820v3") == "https://arxiv.org/pdf/2511.22820"
    assert f.arxiv_pdf_url("2511.22820") == "https://arxiv.org/pdf/2511.22820"


def test_derive_route() -> None:
    base = {"arxiv_id": "", "doi": "", "access": "oa", "oa_url": ""}
    assert f.derive_route({**base, "arxiv_id": "1802.03454", "doi": "10.1364/optica.5.000876"}) == "arxiv"
    assert f.derive_route({**base, "doi": "10.1364/oe.1", "oa_url": "https://doi.org/10.1364/oe.1"}) == "optica_browser"
    assert f.derive_route({**base, "oa_url": "https://ieeexplore.ieee.org/x.pdf"}) == "ieee_browser"
    assert f.derive_route({**base, "oa_url": "https://www.nature.com/articles/a.pdf"}) == "oa_publisher"
    assert f.derive_route({**base, "access": "paywalled", "oa_url": ""}) == "manual"


def test_pdf_checks() -> None:
    assert f.pdf_problem(200, PDF, {"content-length": str(len(PDF))}) == ""
    assert f.pdf_problem(200, PDF, {}) == ""
    assert f.pdf_problem(200, PDF, {"content-length": "999999"}).startswith("truncated")
    assert f.pdf_problem(200, PDF, {"content-length": "999999", "content-encoding": "gzip"}) == ""
    assert f.pdf_problem(200, b"%PDF-1.4 tiny", {}).startswith("too small")
    assert f.pdf_problem(200, b"<html>no</html>", {}) == "not %PDF"
    assert f.pdf_problem(404, PDF, {}) == "HTTP 404"


def test_html_and_challenge() -> None:
    assert f.looks_like_html(b"<!DOCTYPE html><html>", "")
    assert f.looks_like_html(b"whatever", "text/html; charset=utf-8")
    assert not f.looks_like_html(PDF, "application/pdf")
    assert f.is_challenge("<title>Just a moment...</title><script src='/cdn-cgi/challenge-platform/x'>")
    assert f.is_challenge('<title>Client Challenge</title><link href="/_fs-ch-1T1w/assets/styles.css">')
    assert not f.is_challenge("<html><head><title>Article</title></head></html>")


def test_citation_pdf_url() -> None:
    html = (
        '<html><head><meta name="citation_title" content="T">'
        '<meta content="/doi/pdf/10.1063/1.5000384" name="citation_pdf_url"></head></html>'
    )
    assert f.citation_pdf_url(html, "https://pubs.aip.org/app/article/2/1/1") == (
        "https://pubs.aip.org/doi/pdf/10.1063/1.5000384"
    )
    assert f.citation_pdf_url("<meta NAME='CITATION_PDF_URL' CONTENT='https://x.org/a.pdf'>", "https://y") == (
        "https://x.org/a.pdf"
    )
    assert f.citation_pdf_url("<html><head></head></html>", "https://y") == ""


def test_round_robin_interleaves_hosts() -> None:
    def j(pid: str, url: str, doi: str = "") -> f.Job:
        return f.Job(pid, "", doi, "", "oa_publisher", url, "oa")

    jobs = [
        j("a1", "https://arxiv.org/pdf/1"),
        j("a2", "https://arxiv.org/pdf/2"),
        j("n1", "https://www.nature.com/1.pdf"),
        j("d1", "https://doi.org/10.1063/x", "10.1063/x"),
    ]
    order = [x.paper_id for x in f.round_robin(jobs)]
    assert order == ["a1", "n1", "d1", "a2"]


def test_parse_arxiv_raw() -> None:
    xml = b"""<?xml version="1.0"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"><GetRecord><record><metadata>
<arXivRaw xmlns="http://arxiv.org/OAI/arXivRaw/"><id>2511.22820</id>
<version version="v1"><date>x</date></version><version version="v2"><date>y</date></version>
<license>http://creativecommons.org/licenses/by/4.0/</license></arXivRaw>
</metadata></record></GetRecord></OAI-PMH>"""
    assert f.parse_arxiv_raw(xml) == {
        "arxiv_license": "http://creativecommons.org/licenses/by/4.0/",
        "arxiv_version": "v2",
    }
    assert f.parse_arxiv_raw(b'<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"/>') == {}


def test_pdf_like_and_next_hop() -> None:
    assert f.pdf_like_url("https://www.nature.com/articles/s41467-019-08369-w.pdf")
    assert f.pdf_like_url("https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/lpor.201900364")
    assert f.pdf_like_url("https://pubs.acs.org/doi/pdf/10.1021/acsphotonics.3c00945")
    assert not f.pdf_like_url("https://doi.org/10.1063/1.5000384")
    assert not f.pdf_like_url("https://onlinelibrary.wiley.com/doi/epdf/10.1002/x")
    refresh = '<meta http-equiv="refresh" content="0; url=/articles/a.pdf?x=1">'
    assert f.next_pdf_hop(refresh, "https://www.nature.com/articles/a.pdf") == (
        "https://www.nature.com/articles/a.pdf?x=1"
    )
    both = refresh + '<meta name="citation_pdf_url" content="https://h.org/c.pdf">'
    assert f.next_pdf_hop(both, "https://h.org/") == "https://h.org/c.pdf"
    assert f.next_pdf_hop("<html></html>", "https://h.org/") == ""


def test_waf_challenge() -> None:
    assert f.waf_challenge(202, {})
    assert f.waf_challenge(200, {"x-amzn-waf-action": "challenge"})
    assert f.waf_challenge(403, {"cf-mitigated": "challenge"})
    assert not f.waf_challenge(200, {"content-type": "application/pdf"})
