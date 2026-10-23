from photonics_atlas.adapters import blog, eo, lineage, ofc, pk
from photonics_atlas.textnorm import EMAIL_RE

from .conftest import needs_inputs


@needs_inputs
def test_counts_match_devlog_inventory() -> None:
    assert (len(eo.orgs()), len(eo.affiliations()), len(eo.papers())) == (284, 2880, 233)
    # PK updated 2026-10-22 (advanced-packaging-atlas commit b1daf52, affiliations for 57 more papers): was (144, 1996, 296)
    assert (len(pk.orgs()), len(pk.affiliations()), len(pk.papers())) == (181, 2405, 296)
    assert (len(lineage.orgs()), len(lineage.events()), len(lineage.sources())) == (172, 23, 282)
    pres = ofc.presentations()
    assert len(pres) == 830
    assert sum(len(p.authors) for p in pres) == 6056
    assert sum(p.text_cached for p in pres) == 677
    assert len(blog.pdfs()) == 128


@needs_inputs
def test_ofc_adapter_never_emits_emails() -> None:
    for p in ofc.presentations():
        for text in (p.title, p.session_title, *(a.name for a in p.authors), *(a.affiliation for a in p.authors)):
            assert "@" not in text and not EMAIL_RE.search(text), text


@needs_inputs
def test_ofc_session_dates_are_conference_week() -> None:
    dates = {p.session_date for p in ofc.presentations()}
    assert dates <= {"2026-03-15", "2026-03-16", "2026-03-17", "2026-03-18", "2026-03-19"}
