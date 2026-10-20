from photonics_atlas.textnorm import norm_key, slug, strip_emails


def test_norm_key_drops_legal_forms_accents_and_punctuation() -> None:
    assert norm_key("Intel Corporation") == norm_key("Intel") == "intel"
    assert norm_key("Technische Universität Berlin") == "technische universitat berlin"
    assert norm_key("Beijing University of Posts & Telecom") == "beijing university of posts and telecom"
    assert norm_key("NTT, Inc.") == "ntt"
    assert norm_key("Huazhong Univ of Science and Technology") != norm_key(
        "Huazhong University of Science and Technology"
    )


def test_slug() -> None:
    assert slug("A*STAR Institute of Microelectronics") == "a_star_institute_of_microelectronics"


def test_strip_emails_plain_grouped_obfuscated() -> None:
    for s in ("Jane Doe, jane.doe@example.org", "{alice,bob}@mit.edu", "alice [at] mit [dot] edu", "bob(at)uni-x.de"):
        out = strip_emails(s)
        assert "@" not in out and "[at]" not in out and "(at)" not in out, out
    # Affiliation text is left alone.
    for s in ("NTT, Inc.", "Univ. of Sci. & Tech.", "M. C. Yew (at) TSMC"):
        assert strip_emails(s) == s
