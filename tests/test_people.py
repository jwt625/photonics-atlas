"""People atlas (DevLog-004): merge rules on synthetic slots, the real people tables, and one mutation test per
rules_people rule on a temp copy of the data (as tests/test_validate.py)."""

from __future__ import annotations

import re
import shutil
from collections import Counter, defaultdict
from collections.abc import Callable, Iterable
from pathlib import Path

import pytest

from photonics_atlas import people as P
from photonics_atlas.csvio import read_csv, write_csv
from photonics_atlas.paths import ROOT, input_path
from photonics_atlas.schema import columns
from photonics_atlas.validate import validate

from .conftest import needs_inputs

Rows = list[dict[str, str]]
PEOPLE = ROOT / "data" / "people"


def _slot(
    sid: str, name: str, roots: set[str], coauthors: Iterable[str] = (), orcid: str = "", eo_pid: str = ""
) -> P.Slot:
    s = P.Slot(sid=sid, corpus="ofc2026", source_id=sid.split("#")[0], index=1, names=[name], orcid=orcid)
    s.eo_pid = eo_pid
    s.variants = [P.parse(name)]
    s.roots = s.lineages = frozenset(roots)
    s.coauthors = frozenset(P.coauthor_key(n, P.EO_COMMON) for n in coauthors)
    s.selfkeys = frozenset({P.coauthor_key(name, P.EO_COMMON)})
    return s


def _basis(a: P.Slot, b: P.Slot, hubs: frozenset[str] = frozenset(), dense: frozenset[str] = frozenset()) -> str | None:
    pr = P.evaluate(a, b, P.EO_COMMON, hubs, dense)
    return None if pr is None else (pr.basis or "review:" + ";".join(pr.flags))


def _slot_of(obs_id: str) -> str:
    m = P.SLOT_OF_OBS_RE.match(obs_id)
    assert m, obs_id
    return m.group(1)


# All names below are fictitious.
CO = ["Daria Quell", "Ivo Brannt"]


def test_merge_rules_on_synthetic_slots() -> None:
    # exact non-common name + shared org: merge
    assert _basis(_slot("s:1#1", "Ada Fennimore", {"org_a"}), _slot("s:2#1", "Ada Fennimore", {"org_a"})) == (
        "exact_name_shared_org"
    )
    # exact name alone (different orgs, no coauthor): review only, never a merge
    r = _basis(_slot("s:1#1", "Ada Fennimore", {"org_a"}), _slot("s:2#1", "Ada Fennimore", {"org_b"}))
    assert r is not None and r.startswith("review:") and "exact_name" in r
    # common family name: shared org alone is not enough
    r = _basis(_slot("s:1#1", "Wei Wang", {"org_a"}), _slot("s:2#1", "Wei Wang", {"org_a"}))
    assert r is not None and r.startswith("review:") and "common_family_name" in r
    # ambiguous full name (D91 b / D96): shared org alone is not enough either
    r = _basis(
        _slot("s:1#1", "Ada Qorvath", {"o"}), _slot("s:2#1", "Ada Qorvath", {"o"}), dense=frozenset({"ada qorvath"})
    )
    assert r is not None and "ambiguous_full_name" in r
    # common family name: shared org + shared coauthor merges
    assert _basis(_slot("s:1#1", "Wei Wang", {"org_a"}, CO), _slot("s:2#1", "Wei Wang", {"org_a"}, CO)) == (
        "compatible_name_shared_org_coauthor"
    )
    # initials vs full name: needs org + coauthor
    assert _basis(_slot("s:1#1", "J. E. Fennimore", {"o"}), _slot("s:2#1", "Jon E. Fennimore", {"o"})) == (
        "review:compatible_name;shared_org"
    )
    assert (
        _basis(_slot("s:1#1", "J. E. Fennimore", {"o"}, CO), _slot("s:2#1", "Jon E. Fennimore", {"o"}, CO))
        == "compatible_name_shared_org_coauthor"
    )
    # two authors of one source are never one person; ORCID beats names
    assert P.evaluate(_slot("s:1#1", "Qiro Wu", {"o"}), _slot("s:1#2", "Qiro Wu", {"o"}), P.EO_COMMON) is None
    x = "0000-0001-2345-6789"
    assert _basis(_slot("s:1#1", "Q. Wu", set(), orcid=x), _slot("s:2#1", "Qiro C. Wu", set(), orcid=x)) == "orcid"
    # incompatible given names: no relation
    assert _basis(_slot("s:1#1", "Anna Fennimore", {"o"}), _slot("s:2#1", "Boris Fennimore", {"o"})) is None


def test_name_folding() -> None:
    assert P.tokens("Ada H. Fenn-Imore") == (("ada", "h"), "fennimore")
    assert P.tokens("Jerry (Qa-Lo) Li") == (("jerry",), "li")
    assert P.tokens("K.-Y. Lee Jr.") == (("k", "y"), "lee")
    assert P.full_key(P.parse("M. C. Yewbank")) == ""
    # hyphenated given syllables give one initial each; capital runs are initials (I1)
    n = P.parse("Qai-Tun Wang")
    assert (n.given, n.inits, n.lead) == (("qaitun",), ("q", "t"), ("qai", "tun"))
    assert P.parse("QT Wang").inits == ("q", "t") and P.parse("QT Wang").abbreviated
    assert P.parse("Q.J. Wang").inits == ("q", "j")
    assert P.parse("QT WANG").given == ("qt",)  # all-caps names: no capital-run reading


def test_given_name_compatibility() -> None:
    c = P.compatible
    assert c(P.parse("Qai-Tun Wang"), P.parse("Q. T. Wang"))
    assert c(P.parse("Qai-Tun Wang"), P.parse("QT Wang"))
    assert c(P.parse("Qaitun Wang"), P.parse("Qai-Tun Wang"))
    assert not c(P.parse("Qai-Tun Wang"), P.parse("Q.J. Wang"))  # full initials sequence compared
    assert not c(P.parse("QT Chen"), P.parse("Q. S. Chen"))
    assert not c(P.parse("Hirotaka Mozu"), P.parse("Hiro Mozu"))  # not a syllable boundary
    assert not c(P.parse("Qeng-Qieh Hsu"), P.parse("Qeng-Qi Hsu"))
    assert c(P.parse("Jon Fennimore"), P.parse("Jon Edgar Fennimore"))
    assert c(P.parse("J. Fennimore"), P.parse("J. E. Fennimore"))


def test_round2_name_rules() -> None:
    c = P.compatible
    # D95: a full given name printed after initials must be one of the other side's full given names
    assert not c(P.parse("Jon Wu"), P.parse("J.Y. Ezra Wu"))
    assert c(P.parse("J. Wu"), P.parse("J.Y. Ezra Wu"))
    assert c(P.parse("J. Y. Ezra Wu"), P.parse("J.Y. Ezra Wu"))
    # D95: for common family names, one-syllable full given name !~ two initials
    assert c(P.parse("Qoz Wang"), P.parse("Q. T. Wang"))
    assert not c(P.parse("Qoz Wang"), P.parse("Q. T. Wang"), common=True)
    assert c(P.parse("Qoz Wang"), P.parse("Q. Wang"), common=True)


def test_joined_given_name_spellings() -> None:
    """D211 (audit 2 F1): hyphen / camel-case / spacing variants of one given name are compatible also under a common
    family name; D95 still holds for initials (D213: also when the leading full name matches)."""
    c = P.compatible
    for a, b in [
        ("Qaitun Ozz", "Qai-Tun Ozz"),
        ("QaiTun Ozz", "Qai-Tun Ozz"),
        ("Qai Tun Ozz", "Qaitun Ozz"),
        ("Qaitun Wang", "Qai-Tun Wang"),
    ]:
        assert c(P.parse(a), P.parse(b), common=True), (a, b)
        assert c(P.parse(b), P.parse(a), common=True), (b, a)
    assert not c(P.parse("Qing Ozz"), P.parse("Q. T. Ozz"), common=True)
    assert not c(P.parse("Qoz Ozz"), P.parse("Qoz Q. T. Ozz"), common=True)  # D213: no change
    assert not c(P.parse("Jon E. Wang"), P.parse("Jone Wang"), common=True)  # an initial is not a syllable
    # one unhyphenated record no longer blocks the rule-3 joins of the hyphenated records (audit F1 pattern)
    co = ["Daria Quell", "Lio Varga", "Ema Szolt"]
    s = [_slot(f"s:{i}#1", "Qai-Tun Wang", {"o"}, co) for i in range(1, 4)] + [_slot("s:4#1", "Qaitun Wang", {"o"}, co)]
    ident = _resolve(s)
    assert len(set(ident.cluster_of)) == 1
    assert not any(f.startswith("blocked_") for p in ident.review for f in p.flags)


def test_same_as_redirects() -> None:
    """D212: an id that lost all records to a merge redirects to the person now holding them; chains collapse."""
    rows = {k: {"person_id": k, "same_as": ""} for k in ("a", "b", "c", "d", "e")}
    old = {"o1": "a", "o2": "a", "o3": "b", "o4": "c", "o5": "c"}
    new = {"o1": "b", "o2": "b", "o3": "b", "o4": "b", "o5": "e"}
    assert P.same_as_redirects(rows, ["a"], old, new) == {"a": "b"}
    assert P.same_as_redirects(rows, ["c"], old, new) == {}  # split over two persons: no single survivor
    rows["d"]["same_as"] = "a"  # kept from an earlier build, then a was absorbed into b
    assert P.same_as_redirects(rows, ["a", "d"], old, new) == {"a": "b", "d": "b"}
    rows["a"]["same_as"], rows["b"]["same_as"] = "b", "a"
    assert P.same_as_redirects(rows, ["a", "b"], {}, {}) == {}  # a cycle holds no surviving person


def _hrow(
    src: str,
    aff_order: int,
    org: str,
    ids: str,
    *,
    k: int = 1,
    role: str = "primary",
    basis: str = "printed",
    name: str = "Ada Fennimore",
) -> dict[str, str]:
    return {
        "source_id": src,
        "author_index": "1",
        "header_pos": "1",
        "printed_name": name,
        "aff_order": str(aff_order),
        "aff_marker": str(aff_order),
        "aff_role": role,
        "org_k": str(k),
        "org_name": org,
        "unit": "",
        "locality": "",
        "country": "",
        "marker_basis": basis,
        "evidence_grade": "B" if basis in P.HEADER_GRADE_B else "A",
        "grade_note": "",
        "locator": "p.~1 header",
        "org_ids": ids,
        "match_basis": "name" if ids else "unmapped",
    }


def test_ofc_header_merge_synthetic() -> None:
    """D214-D218 on a fictitious fixture batch: multi-affiliation, joint-printed block, present address, conflict,
    unmapped, string-confirmed, unreadable paper (no rows) and one printed org mapping to two registry orgs."""
    orgs = {o: {"org_id": o, "parent_org_id": ""} for o in ("org_u", "org_c", "org_d", "org_x")}
    orgs["org_u_lab"] = {"org_id": "org_u_lab", "parent_org_id": "org_u"}
    meta = {
        "P1": ("U Lab", ["org_u_lab"]),
        "P2": ("D Corp", ["org_d"]),
        "P3": ("X Inc", ["org_x"]),
        "P4": ("X Inc", ["org_x"]),
        "P5": ("X Inc", ["org_x"]),
        "P6": ("Lab Q", []),
        "P7": ("U", ["org_u"]),
        "P8": ("U", ["org_u"]),
    }
    slots = []
    for code, (printed, ids) in meta.items():
        s = _slot(f"ofc2026:{code}#1", "Ada Fennimore", {"org_u"})
        s.affs = [P.Aff(1, printed, ids, "", "", "primary", "program metadata authors_json #1")]
        s.kind = "conference"
        slots.append(s)
    rows = [
        _hrow("ofc2026:P1", 1, "U", "org_u"),
        _hrow("ofc2026:P1", 2, "C Univ", "org_c", role="additional"),
        _hrow("ofc2026:P2", 1, "C Univ", "org_c"),
        _hrow("ofc2026:P2", 1, "D Corp", "org_d", k=2),
        _hrow("ofc2026:P3", 1, "U", "org_u"),
        _hrow("ofc2026:P3", 2, "X Inc", "org_x", role="present_address"),
        _hrow("ofc2026:P4", 1, "U", "org_u", basis="listing_order"),
        _hrow("ofc2026:P5", 1, "Unknown Lab", ""),
        _hrow("ofc2026:P6", 1, "Lab Q", ""),
        _hrow("ofc2026:P8", 1, "U-C", "org_u;org_c", name="A. Fennimore"),
    ]
    stats = P.attach_headers(slots, rows, orgs)
    by = {s.source_id.split(":")[1]: s for s in slots}
    status = {c: s.hdr_status for c, s in by.items()}
    assert status == {
        "P1": "confirmed",
        "P2": "confirmed",
        "P3": "confirmed",
        "P4": "conflict",
        "P5": "unmapped",
        "P6": "confirmed",
        "P7": "",
        "P8": "confirmed",
    }
    assert stats["slots confirmed"] == 5 and stats["rows grade B"] == 1
    oids = {c: [oid for oid, _, _ in P.obs_ids(s)] for c, s in by.items()}
    assert oids["P1"] == ["ofc2026:P1#a1.h1.1.m1", "ofc2026:P1#a1.h2.1.m1"]  # metadata row dropped: confirmed
    assert oids["P2"] == ["ofc2026:P2#a1.h1.1.m1", "ofc2026:P2#a1.h1.2.m1"]  # joint-printed block: one id per org
    assert oids["P4"] == ["ofc2026:P4#a1.1", "ofc2026:P4#a1.h1.1.m1"]  # conflict: both kept (D241)
    assert oids["P5"] == ["ofc2026:P5#a1.1", "ofc2026:P5#a1.h1.1.m1"]  # unmapped: metadata kept
    assert oids["P7"] == ["ofc2026:P7#a1.1"]  # unreadable paper: metadata only
    assert oids["P8"] == ["ofc2026:P8#a1.h1.1.m1", "ofc2026:P8#a1.h1.1.m2"]
    # D219e: a later one-to-several mapping adds ids and never renames the existing one
    by["P1"].hdr[0].org_ids = ["org_u", "org_c"]
    assert [o for o, _, _ in P.obs_ids(by["P1"])][:2] == ["ofc2026:P1#a1.h1.1.m1", "ofc2026:P1#a1.h1.1.m2"]
    for oid in oids["P8"]:
        assert P.HEADER_ID_RE.search(oid)
    assert not P.HEADER_ID_RE.search("ofc2026:P4#a1.1")
    # D217: identity is untouched (names and org keys stay the metadata ones); D218: header form is an alias only
    assert all(s.roots == frozenset({"org_u"}) and s.names == ["Ada Fennimore"] for s in slots)
    al = P.alias_rows("person_x", "Ada Fennimore", [by["P8"]])
    assert [(a["alias"], a["alias_type"], a["origin"], a["notes"]) for a in al] == [
        ("A. Fennimore", "abbreviated", "ofc2026", P.HEADER_ALIAS_NOTE)
    ]
    # the slot (not the obs id) carries the old person id (D217): a dropped metadata id still reuses it
    cl = {0: [by["P1"]]}
    assert P.assign_ids(cl, {0: "Ada Fennimore"}, {"ofc2026:P1#a1.1": "person_ada"}, [], {"person_ada"}) == {
        0: "person_ada"
    }


def test_folded_name_match_keeps_a_mapped_metadata_org() -> None:
    """D219a (OFC merge audit F1): fold() drops parenthesized text, so a folded-name match alone must not replace a
    mapped metadata org by an unmapped header string. Names are fictitious."""
    orgs = {
        "org_q": {"org_id": "org_q", "parent_org_id": ""},
        "org_q_lab": {"org_id": "org_q_lab", "parent_org_id": "org_q"},
    }
    hs = P.header_status
    unmapped_hdr = [_hrow("ofc2026:P1", 1, "Qorvath University (Old Qorvath College)", "")]
    assert hs(["org_q"], "Qorvath University", unmapped_hdr, orgs) == "unmapped"  # metadata row kept
    assert hs([], "Qorvath University", unmapped_hdr, orgs) == "confirmed"  # both unmapped: printed strings agree
    rows = unmapped_hdr + [_hrow("ofc2026:P1", 2, "Q Lab", "org_q_lab", role="additional")]
    assert hs(["org_q"], "Qorvath University", rows, orgs) == "confirmed"  # a header row carries the metadata root


def test_lit_slots_and_duplicates(monkeypatch: pytest.MonkeyPatch) -> None:
    """D370-D374 on fictitious lit papers: slots = author-list positions, header rows the only observations (D219e
    ids), printed forms aliases only (D218), duplicate papers of other corpora skipped (D372)."""
    src = {
        "lit:ozz2025": {
            "corpus": "lit",
            "native_id": "ozz2025",
            "doi": "10.9/abc",
            "title": "A Qorvath Waveguide Study",
            "same_as": "",
            "published_on": "2025-03-01",
            "year": "2025",
        },
        "lit:dup2024": {
            "corpus": "lit",
            "native_id": "dup2024",
            "doi": "10.9/X1",
            "title": "Other Title For A Paper",
            "same_as": "",
            "published_on": "",
            "year": "2024",
        },
        "lit:tit2023": {
            "corpus": "lit",
            "native_id": "tit2023",
            "doi": "",
            "title": "On Fennimore Gratings, Again!",
            "same_as": "",
            "published_on": "",
            "year": "2023",
        },
        "eo:x2024": {
            "corpus": "eo",
            "native_id": "x2024",
            "doi": "10.9/x1",
            "title": "Different",
            "same_as": "",
            "published_on": "",
            "year": "2024",
        },
        "pk:y2023": {
            "corpus": "pk",
            "native_id": "y2023",
            "doi": "",
            "title": "on fennimore gratings again",
            "same_as": "",
            "published_on": "",
            "year": "2023",
        },
    }
    assert P.lit_duplicates(src) == {"lit:dup2024": "eo:x2024", "lit:tit2023": "pk:y2023"}
    lists = {"ozz2025": ["Ada Fennimore", "Ivo Brannt"], "dup2024": ["Q. Ozz"], "tit2023": ["R. Ozz"]}
    monkeypatch.setattr(P, "lit_author_lists", lambda codes, root=None: {c: lists[c] for c in codes if c in lists})
    dropped: Counter[str] = Counter()
    slots = P._lit_slots(src, dropped)
    assert [(s.sid, s.name, s.active_on, s.coauthor_names) for s in slots] == [
        ("lit:ozz2025#1", "Ada Fennimore", "2025-03-01", ["Ivo Brannt"]),
        ("lit:ozz2025#2", "Ivo Brannt", "2025-03-01", ["Ada Fennimore"]),
    ]
    assert sum(dropped.values()) == 2 and all("D372" in k for k in dropped)
    rows = [
        dict(_hrow("lit:ozz2025", 1, "U", "org_u", name="A. Fennimore"), author_index="1", locator="p.1 header"),
        dict(_hrow("lit:ozz2025", 1, "U", "org_u;org_c", name="I. Brannt"), author_index="2", locator="p.1 footnote"),
    ]
    stats = P.attach_headers(slots, rows, {})
    assert stats["lit slots with rows"] == 2 and stats["lit rows grade A"] == 2
    assert [o for s in slots for o, _, _ in P.obs_ids(s)] == [
        "lit:ozz2025#a1.h1.1.m1",
        "lit:ozz2025#a2.h1.1.m1",
        "lit:ozz2025#a2.h1.1.m2",
    ]
    assert all(s.hdr_status == "" and not s.affs and s.names == [s.name] for s in slots)  # no metadata row, D217
    al = P.alias_rows("person_x", "Ada Fennimore", [slots[0]])
    assert [(a["alias"], a["origin"], a["notes"]) for a in al] == [("A. Fennimore", "lit", P.LIT_ALIAS_NOTE)]


def test_swapped_name_order_and_case_accent_aliases() -> None:
    """D378: a slot flagged name_order_swapped with a common family-name token joins nobody by name (review), unless
    the join is committed. D379: header forms differing only in case / accents are not added as aliases."""
    co = ["Daria Quell", "Ivo Brannt"]
    a = _slot("s:1#1", "Wei Wang", {"o"}, co)
    b = _slot("s:2#1", "Wei Wang", {"o"}, co)
    assert P.evaluate(a, b, P.EO_COMMON).basis == "compatible_name_shared_org_coauthor"  # type: ignore[union-attr]
    b.name_order_swapped = True
    pr = P.evaluate(a, b, P.EO_COMMON)
    assert pr is not None and "name_order_swapped" in pr.flags and pr.need == (P.NEVER,)
    ident = _resolve_c([a, b])
    assert ident.cluster_of[0] != ident.cluster_of[1]
    assert any("name_order_swapped" in p.flags for p in ident.review)
    ident = _resolve_c([a, b], {"s:1#1": "person_wei_wang", "s:2#1": "person_wei_wang"})
    assert ident.cluster_of[0] == ident.cluster_of[1]  # committed join stands
    # a distinctive name without a common token is not affected
    c, d = _slot("s:3#1", "Ada Fennimore", {"o"}), _slot("s:4#1", "Ada Fennimore", {"o"})
    d.name_order_swapped = True
    assert P.evaluate(c, d, P.EO_COMMON).basis == "exact_name_shared_org"  # type: ignore[union-attr]
    # D379
    s = _slot("lit:ozz2025#1", "Ada Fennimore", {"o"})
    s.hdr = [
        P.Aff(1, "U", [], "", "", "primary", "p.1 header", oid="lit:ozz2025#a1.h1.1", printed_name=n)
        for n in ("ADA FENNIMORE", "Adá Fennimore", "A. Fennimore", "A. FENNIMORE")
    ]
    s.corpus = "lit"
    assert [a["alias"] for a in P.alias_rows("person_x", "Ada Fennimore", [s])] == ["A. Fennimore"]


def test_round2_hub_and_common_rules() -> None:
    hub = P.coauthor_key("Ivo Brannt", P.EO_COMMON)
    hubs = frozenset({hub})
    # common family: two shared hubs are not enough (D96)
    a = _slot("s:1#1", "Wei Wang", {"o"}, ["Ivo Brannt", "Daria Quell"])
    b = _slot("s:2#1", "Wei Wang", {"o"}, ["Ivo Brannt", "Daria Quell"])
    hubs2 = hubs | {P.coauthor_key("Daria Quell", P.EO_COMMON)}
    assert not P.coauthor_support(a, b, hubs2, common=True)
    assert P.coauthor_support(a, b, hubs2, common=False)
    # the hub's own slots: no discount (D96)
    h1 = _slot("s:1#1", "Ivo Brannt", {"o"}, ["Daria Quell"])
    h2 = _slot("s:2#1", "Ivo Brannt", {"o"}, ["Daria Quell"])
    assert P.coauthor_support(h1, h2, hubs2)
    # slot-frequency common rule needs >= 3 distinct full names (D96): one prolific person is not "common"
    many = [_slot(f"s:{i}#1", "Ada Qorvath", {"o"}) for i in range(12)]
    assert "qorvath" not in P.common_families(many, 10)
    mixed = many + [_slot("s:90#1", "Bo Qorvath", {"o"}), _slot("s:91#1", "Cy Qorvath", {"o"})]
    assert "qorvath" in P.common_families(mixed, 10)


def _resolve(slots: list[P.Slot]) -> P.Identity:
    return P.resolve(P.Inputs(slots=slots, orgs={}, sources={}, common=set(P.EO_COMMON), dropped=Counter()))


def test_no_name_chaining_and_ambiguous_initials() -> None:
    """I1 regressions: compatible pairs must not chain incompatible full names into one person."""
    co = CO
    # "Hirotaka" ~ "H." ~ "Hiroki": H. is ambiguous, nothing merges through it; the full names stay apart
    s = [
        _slot("s:1#1", "Hirotaka Mozu", {"o"}, co),
        _slot("s:2#1", "H. Mozu", {"o"}, co),
        _slot("s:3#1", "Hiroki Mozu", {"o"}, co),
    ]
    ident = _resolve(s)
    assert len(set(ident.cluster_of)) == 3
    assert any("blocked_name_ambiguous" in p.flags for p in ident.review)
    # cluster-level check: "Q. T." joins "Qai-Tun", then "Q.J." cannot join that cluster through "Q."
    s = [
        _slot("s:1#1", "Q. T. Wang", {"o"}, co),
        _slot("s:2#1", "Qai-Tun Wang", {"o"}, co),
        _slot("s:3#1", "Q.J. Wang", {"o"}, co),
    ]
    ident = _resolve(s)
    assert ident.cluster_of[0] == ident.cluster_of[1] != ident.cluster_of[2]
    s.append(_slot("s:4#1", "Q. Wang", {"o"}, co))
    cl = P.Clusters(s)
    cl.union(0, 1)
    cl.union(2, 3)
    assert cl.name_conflict(0, 2)


def _resolve_c(slots: list[P.Slot], committed: dict[str, str] | None = None) -> P.Identity:
    inp = P.Inputs(slots=slots, orgs={}, sources={}, common=set(P.EO_COMMON), dropped=Counter())
    inp.committed = committed or {}
    return P.resolve(inp)


def _pair_papers(co_orgs: tuple[str, str], co_orcid: str = "", co_name: str = "Lei Zhang") -> list[P.Slot]:
    """Two papers, each by "Wei Wang" (org o) and a coauthor; fictitious names, common family names (EO list)."""
    s = [
        _slot("s:1#1", "Wei Wang", {"o"}, [co_name]),
        _slot("s:1#2", co_name, {co_orgs[0]}, ["Wei Wang"], orcid=co_orcid),
        _slot("s:2#1", "Wei Wang", {"o"}, [co_name]),
        _slot("s:2#2", co_name, {co_orgs[1]}, ["Wei Wang"], orcid=co_orcid),
    ]
    s[1].index = s[3].index = 2
    return s


def test_common_family_needs_resolved_coauthor_for_new_joins() -> None:
    """D219c / D219d: a new rule-3 join on a common family name needs a shared coauthor that is one person (or has
    a non-common family name); name-key-only and circular support do not count; committed joins stand."""

    def same(ident: P.Identity, a: int, b: int) -> bool:
        return ident.cluster_of[a] == ident.cluster_of[b]

    # coauthor key matches, but its two slots are different persons: no join, review pair
    ident = _resolve_c(_pair_papers(("o2", "o3")))
    assert not same(ident, 0, 2)
    assert any("coauthor_unresolved" in p.flags for p in ident.review)
    # the coauthor is one person (ORCID): the join is made
    ident = _resolve_c(_pair_papers(("o2", "o3"), co_orcid="0000-0001-2345-6789"))
    assert same(ident, 1, 3) and same(ident, 0, 2)
    # a coauthor with a non-common family name supports the join directly
    ident = _resolve_c(_pair_papers(("o2", "o3"), co_name="Ivo Fennimore"))
    assert same(ident, 0, 2)
    # circular support: each pair is supported only by the other one, so neither is joined
    ident = _resolve_c(_pair_papers(("o", "o")))
    assert len(set(ident.cluster_of)) == 4
    # committed path (D219d): the committed join stands, and the coauthor pair then resolves through it
    ident = _resolve_c(_pair_papers(("o", "o")), {"s:1#1": "person_wei_wang", "s:2#1": "person_wei_wang"})
    assert same(ident, 0, 2) and same(ident, 1, 3)
    # committed only when both slots are in the same committed person
    ident = _resolve_c(_pair_papers(("o2", "o3")), {"s:1#1": "person_wei_wang", "s:2#1": "person_wei_wang_2"})
    assert not same(ident, 0, 2)


def test_hub_coauthor_is_not_enough() -> None:
    hub = P.coauthor_key("Ivo Brannt", P.EO_COMMON)
    a = _slot("s:1#1", "Wei Wang", {"o"}, ["Ivo Brannt"])
    b = _slot("s:2#1", "Wei Wang", {"o"}, ["Ivo Brannt"])
    assert _basis(a, b) == "compatible_name_shared_org_coauthor"
    assert (_basis(a, b, hubs=frozenset({hub})) or "").startswith("review:")
    a2 = _slot("s:1#1", "Wei Wang", {"o"}, CO)
    b2 = _slot("s:2#1", "Wei Wang", {"o"}, CO)
    assert _basis(a2, b2, hubs=frozenset({hub})) == "compatible_name_shared_org_coauthor"  # two shared coauthors


def test_eo_person_split_is_queued() -> None:
    s = [
        _slot("eo:p1#1", "Ada R. Fennimore", {"o"}, eo_pid="eo_x"),
        _slot("eo:p2#1", "Ada Fennimore", set(), eo_pid="eo_x"),
    ]
    for x in s:
        x.corpus = "eo"
    ident = _resolve(s)
    assert ident.cluster_of[0] != ident.cluster_of[1]
    assert any("eo_person_split" in p.flags for p in ident.review)


@needs_inputs
def test_real_people_tables() -> None:
    people = {r["person_id"]: r for r in read_csv(PEOPLE / "people.csv")}
    xref = read_csv(PEOPLE / "person_xref.csv")
    obs = read_csv(PEOPLE / "affiliation_observations.csv")
    lin = [x for x in xref if x["scheme"] == "lin_id"]
    assert len(lin) == 288 and all(x["person_id"] == x["value"] and x["value"] in people for x in lin)
    eo_people = read_csv(input_path("eo_atlas") / "data" / "people.csv")
    assert {x["value"] for x in xref if x["scheme"] == "eo_person_id"} == {r["person_id"] for r in eo_people}
    assert {p["orcid"] for p in people.values() if p["orcid"]} == {r["orcid"] for r in eo_people if r["orcid"]}
    assert not any(pid.removeprefix("person_").startswith("000") for pid in people)
    # every input affiliation row once: EO 2880 + PK 2405 + OFC minus the 54 presentations already in EO
    # (joint_printed strings add one row per extra org: suffix .k after author.order)
    meta = [o for o in obs if not P.HEADER_ID_RE.search(o["obs_id"])]
    rows = {
        o["obs_id"].rsplit(".", 1)[0] if o["obs_id"].rsplit("#a", 1)[1].count(".") == 2 else o["obs_id"] for o in meta
    }
    base = Counter(r.split(":")[0] for r in rows)
    # PK 1996 -> 2405 rows on 2026-10-22 (advanced-packaging-atlas commit b1daf52; people rebuilt, DevLog-004 Progress)
    assert base["eo"] == 2880 and base["pk"] == 2405
    # OFC (D214-D215, 2026-10-22): every metadata slot (6056 - 532) keeps observations; the metadata row is dropped
    # only where the paper header confirms it, and every staged header row of a kept slot is one observation (.m per
    # extra org id)
    ofc_slots = {_slot_of(o["obs_id"]) for o in obs if o["source_id"].startswith("ofc2026:")}
    assert len(ofc_slots) == 6056 - 532
    hdr = [o for o in obs if P.HEADER_ID_RE.search(o["obs_id"])]
    sources = {r["source_id"]: r for r in read_csv(ROOT / "data" / "registry" / "sources.csv")}
    lists = P.lit_author_lists([sid.split(":", 1)[1] for sid in sources if sid.startswith("lit:")])

    def has_slot(h: dict[str, str]) -> bool:  # lit: a slot per author-list position (D359, D413); OFC: every row
        if not h["source_id"].startswith("lit:"):
            return True
        names = lists.get(h["source_id"].split(":", 1)[1], [])
        i = int(h["author_index"])
        return 0 < i <= len(names) and P.lit_list_name_ok(names[i - 1])

    staged = {P.header_obs_id(h) for h in P.header_rows() if not sources[h["source_id"]]["same_as"] and has_slot(h)}
    assert {re.sub(r"(\.h\d+\.\d+)\.m\d+$", r"\1", o["obs_id"]) for o in hdr} == staged
    assert all(o["kind"] == "publication" for o in hdr)
    assert not any(sources[o["source_id"]]["same_as"] for o in obs)
    assert {(o["kind"], o["evidence_grade"]) for o in obs} == {
        ("publication", "A"),
        ("publication", "B"),
        ("conference", "B"),
    }
    # grade-B publication rows: OFC header merge, and lit unmarked `layout` blocks (D286f; first in lit_h18, D426)
    assert {o["source_id"].split(":")[0] for o in obs if o["evidence_grade"] == "B" and o["kind"] == "publication"} <= {
        "ofc2026",
        "lit",
    }


@needs_inputs
def test_local_review_queue_hides_its_people() -> None:
    q = ROOT / "data" / "_local" / "people" / "review_queue.csv"
    if not q.exists():
        pytest.skip("local review queue not built")
    queue = read_csv(q)
    obs = read_csv(PEOPLE / "affiliation_observations.csv")
    people = {r["person_id"]: r for r in read_csv(PEOPLE / "people.csv")}
    n_obs = Counter(o["person_id"] for o in obs)
    xs: dict[str, set[str]] = defaultdict(set)
    for x in read_csv(PEOPLE / "person_xref.csv"):
        xs[x["person_id"]].add(x["scheme"])
    lit_only = {p for p, ss in xs.items() if ss == {"lit_name_key"}}
    demoted = P.demoted_by_queue(queue, dict(n_obs), lit_only)
    assert demoted and all(o["visibility"] == "review" for o in obs if o["person_id"] in demoted)
    # D216: a header / metadata conflict slot (header and metadata rows side by side, all review) is the exception
    by_slot: dict[str, list[dict[str, str]]] = defaultdict(list)
    for o in obs:
        by_slot[_slot_of(o["obs_id"])].append(o)
    conflict = {
        k
        for k, os_ in by_slot.items()
        if any(P.HEADER_ID_RE.search(o["obs_id"]) for o in os_)
        and not all(P.HEADER_ID_RE.search(o["obs_id"]) for o in os_)
        and all(o["visibility"] == "review" for o in os_)
    }
    assert all(
        o["visibility"] == "public"
        for o in obs
        if o["person_id"] not in demoted
        and people[o["person_id"]]["visibility"] == "public"
        and _slot_of(o["obs_id"]) not in conflict
    )
    # D64 ruling: a partner without observations (LIN-only record) keeps the pair queued but demotes nothing
    assert P.demoted_by_queue([{"person_id_a": "person_a", "person_id_b": "person_b"}], {"person_a": 3}) == {"person_b"}
    # D377 (b): lit-vs-existing demotes only the lit side; lit-vs-lit as D64
    pair = [{"person_id_a": "person_a", "person_id_b": "person_b"}]
    both = {"person_a": 2, "person_b": 1}
    assert P.demoted_by_queue(pair, both, {"person_b"}) == {"person_b"}
    assert P.demoted_by_queue(pair, both, {"person_a"}) == {"person_a"}
    assert P.demoted_by_queue(pair, both, {"person_a", "person_b"}) == {"person_a", "person_b"}
    # D70/D94 ruling: a queued LIN A/B person row stays public; none of its queued observations is public
    xref = read_csv(PEOPLE / "person_xref.csv")
    lin_ab = {x["person_id"] for x in xref if x["scheme"] == "lin_id" and x["grade"] in ("A", "B")}
    queued = {r["person_id_a"] for r in queue} | {r["person_id_b"] for r in queue}
    assert all(people[p]["visibility"] == "public" for p in lin_ab & queued)


@needs_inputs
def test_person_visibility_and_c_only_lin() -> None:
    """P5 / D94: a LIN person whose sources are all below grade B is never displayable, nor are its observations."""
    people = {r["person_id"]: r for r in read_csv(PEOPLE / "people.csv")}
    xref = read_csv(PEOPLE / "person_xref.csv")
    obs = read_csv(PEOPLE / "affiliation_observations.csv")
    c_only = {x["person_id"] for x in xref if x["scheme"] == "lin_id" and x["grade"] not in ("A", "B")}
    assert len(c_only) == 4
    assert all(people[p]["visibility"] == "review" for p in c_only)
    assert all(o["visibility"] == "review" for o in obs if o["person_id"] in c_only)
    pub_obs = {o["person_id"] for o in obs if o["visibility"] == "public"}
    lin_ab = {x["person_id"] for x in xref if x["scheme"] == "lin_id" and x["grade"] in ("A", "B")}
    assert {p for p, r in people.items() if r["visibility"] == "public"} == pub_obs | lin_ab
    assert not any(r["disambiguator"] for r in people.values())  # D93


@needs_inputs
def test_eo_duplicate_orcid_copy_matches_eo() -> None:
    import ast

    src = (input_path("eo_atlas") / "scripts" / "build_people.py").read_text()
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "DUPLICATE_ORCID" for t in node.targets):
            assert ast.literal_eval(node.value) == P.EO_DUPLICATE_ORCID
            return
    raise AssertionError("DUPLICATE_ORCID not found in the EO build script")


@needs_inputs
def test_build_is_in_sync_with_inputs() -> None:
    """An in-memory rebuild assigns every observation to the committed person_id (stable ids, D65)."""
    inp = P.load_inputs()
    ident = P.resolve(inp)
    clusters: dict[int, list[P.Slot]] = defaultdict(list)
    for i, c in enumerate(ident.cluster_of):
        clusters[c].append(inp.slots[i])
    names = {c: P.display_name(ms) for c, ms in clusters.items()}
    old = {r["obs_id"]: r["person_id"] for r in read_csv(PEOPLE / "affiliation_observations.csv")}
    xref = read_csv(PEOPLE / "person_xref.csv")
    ids = {r["person_id"] for r in read_csv(PEOPLE / "people.csv")}
    pid_of = P.assign_ids(clusters, names, old, xref, ids)
    got = {oid: pid_of[c] for c, ms in clusters.items() for s in ms for oid, _, _ in P.obs_ids(s)}
    assert got == old


# ---------------------------------------------------------------- mutation tests


@pytest.fixture()
def data(tmp_path: Path) -> Path:
    """Temp copy without the local queue; rules_people derives its paths from the validate root (D97)."""
    shutil.copytree(ROOT / "data", tmp_path / "data", ignore=shutil.ignore_patterns("_local", "_staging"))
    for rel in P.HEADER_DIRS_REL:  # D214 / D370: the validator checks header observations against the staged rows
        if (ROOT / rel).exists():
            shutil.copytree(ROOT / rel, tmp_path / rel)
    return tmp_path


@pytest.fixture()
def data_q(data: Path) -> Path:
    """Temp copy with the real local review queue."""
    q = ROOT / "data" / "_local" / "people" / "review_queue.csv"
    if not q.exists():
        pytest.skip("local review queue not built")
    (data / "data" / "_local" / "people").mkdir(parents=True)
    shutil.copy(q, data / "data" / "_local" / "people" / "review_queue.csv")
    return data


def _edit(root: Path, table: str, fn: Callable[[Rows], None]) -> None:
    path = root / "data" / "people" / f"{table}.csv"
    rows = read_csv(path)
    fn(rows)
    write_csv(path, columns(table), rows)


def _row(rows: Rows, **match: str) -> dict[str, str]:
    return next(r for r in rows if all(r[k] == v for k, v in match.items()))


def _errors(root: Path) -> list[str]:
    return validate(root).errors


def test_copy_is_clean(data: Path) -> None:
    assert _errors(data) == []
    assert any("local review queue) absent" in w for w in validate(data).warnings)  # C2: warn, not skip


def test_grade_vs_kind_and_visibility(data: Path) -> None:
    def bad(rows: Rows) -> None:
        _row(rows, kind="conference").update(evidence_grade="A")
        _row(rows, kind="publication").update(evidence_grade="C")

    _edit(data, "affiliation_observations", bad)
    errs = _errors(data)
    assert any("kind conference is grade B" in e for e in errs)
    assert any("public visibility needs grade A/B" in e for e in errs)


def test_duplicate_source_and_corpus_kind(data: Path) -> None:
    srcs = read_csv(data / "data" / "registry" / "sources.csv")
    dup = next(s["source_id"] for s in srcs if s["corpus"] == "ofc2026" and s["same_as"])

    def bad(rows: Rows) -> None:
        r = _row(rows, kind="conference")
        r.update(source_id=dup, obs_id=f"{dup}#a1.1")
        _row(rows, kind="publication").update(kind="conference", evidence_grade="B")

    _edit(data, "affiliation_observations", bad)
    errs = _errors(data)
    assert any("cites duplicate" in e for e in errs)
    assert any("gives kind publication, not conference" in e for e in errs)


def test_obs_id_date_and_orphans(data: Path) -> None:
    def bad(rows: Rows) -> None:
        rows[0].update(obs_id="eo:not_this_source#a1.1")
        rows[1].update(active_on="1999")
        rows[2].update(person_id="person_does_not_exist")
        rows[3].update(org_id="org_does_not_exist")

    _edit(data, "affiliation_observations", bad)
    errs = _errors(data)
    assert any("does not start with its source_id" in e for e in errs)
    assert any("not in the source year" in e for e in errs)
    assert sum("orphan" in e for e in errs) == 2


def test_xref_rules(data: Path) -> None:
    def bad(rows: Rows) -> None:
        _row(rows, scheme="lin_id").update(value="person_someone_else")
        _row(rows, basis="exact_name_shared_org").update(grade="A")
        _row(rows, scheme="ofc_name", basis="origin").update(basis="manual", reviewed_on="")
        _row(rows, scheme="pk_name_key", basis="origin").update(grade="B")

    _edit(data, "person_xref", bad)
    errs = _errors(data)
    assert any("reused verbatim" in e for e in errs)
    assert any("is an inference, grade X" in e for e in errs)
    assert any("basis manual needs reviewed_on" in e for e in errs)
    assert any("origin pk_name_key is grade A" in e for e in errs)


def test_orcid_field_needs_xref(data: Path) -> None:
    _edit(data, "person_xref", lambda rows: rows.remove(_row(rows, scheme="orcid")))
    assert any("without an orcid xref" in e for e in _errors(data))


def test_email_is_rejected(data: Path) -> None:
    _edit(data, "affiliation_observations", lambda rows: rows[0].update(printed_org="Lab, someone@example.edu"))
    assert any("e-mail address" in e for e in _errors(data))


def test_review_queue_person_must_not_be_public(data: Path) -> None:
    obs = read_csv(data / "data" / "people" / "affiliation_observations.csv")
    pub = next(o["person_id"] for o in obs if o["visibility"] == "public")
    q = data / "data" / "_local" / "people" / "review_queue.csv"
    write_csv(
        q, ["person_id_a", "person_id_b", "reason"], [{"person_id_a": pub, "person_id_b": pub, "reason": "name_only"}]
    )
    assert any("is in the review queue with a partner that has observations" in e for e in _errors(data))


def test_copy_with_queue_is_clean(data_q: Path) -> None:
    assert _errors(data_q) == []


def test_queue_rulings_and_eo_split(data_q: Path) -> None:
    q = data_q / "data" / "_local" / "people" / "review_queue.csv"
    queue = read_csv(q)
    split = next(r for r in queue if r["reason"] == "eo_person_split")
    queue.remove(split)
    obs = read_csv(data_q / "data" / "people" / "affiliation_observations.csv")
    pub = next(o["person_id"] for o in obs if o["visibility"] == "public")
    people = read_csv(data_q / "data" / "people" / "people.csv")
    with_obs = {o["person_id"] for o in obs}
    no_obs = next(r["person_id"] for r in people if r["person_id"] not in with_obs)
    queue.append({"person_id_a": pub, "person_id_b": no_obs, "reason": "name_only"})  # partner without observations
    write_csv(q, list(queue[0].keys()), queue)
    errs = _errors(data_q)
    assert any("but the pair is not in the review queue" in e for e in errs)
    assert not any(f"person {pub} is in the review queue" in e for e in errs)  # D64 ruling: no demotion


def test_orcid_held_by_two_persons(data: Path) -> None:
    people = read_csv(data / "data" / "people" / "people.csv")
    o = next(r["orcid"] for r in people if r["orcid"])
    other = next(r["person_id"] for r in people if not r["orcid"])

    def bad(rows: Rows) -> None:
        rows.append({"person_id": other, "scheme": "orcid", "value": o, "basis": "orcid", "grade": "A"})

    _edit(data, "person_xref", bad)
    assert any(f"ORCID {o} held by 2 persons" in e for e in _errors(data))


def test_phone_spelled_email_and_status_words(data: Path) -> None:
    def bad_obs(rows: Rows) -> None:
        rows[0].update(unit="Tel: +1 650 555 0100")
        rows[1].update(printed_org="Lab, jane at example.edu")
        rows[2].update(printed_org="Lab, jane\uff20example.com")
        pa = next(r for r in rows if r["aff_role"] == "present_address")
        pa.update(unit="Present address: Example Lab")  # printed paper text: allowed (D70)

    def bad_people(rows: Rows) -> None:
        rows[0].update(notes="currently at Example Labs")
        rows[1].update(notes="hired 2024")

    _edit(data, "affiliation_observations", bad_obs)
    _edit(data, "people", bad_people)
    errs = _errors(data)
    assert any("contains a phone number" in e for e in errs)
    assert sum("contains an e-mail address" in e for e in errs) >= 2
    assert sum("has status wording" in e for e in errs) == 2
    assert not any("present address" in e.lower() and "unit" in e for e in errs)


def test_text_scans(data: Path) -> None:
    def bad(rows: Rows) -> None:
        rows[0].update(printed_org="Lab, jane at example dot edu")
        rows[1].update(unit="see linkedin profile")
        rows[2].update(unit="formerly at Example Labs")

    _edit(data, "affiliation_observations", bad)
    _edit(data, "people", lambda rows: rows[0].update(disambiguator="Example Corp co-founder"))
    errs = _errors(data)
    assert any("contains an e-mail address" in e for e in errs)
    assert any("mentions LinkedIn" in e for e in errs)
    assert any("move wording" in e for e in errs)
    assert any("role wording" in e for e in errs)


def test_unknown_file_and_empty_table(data: Path) -> None:
    (data / "data" / "people" / "extra.csv").write_text("a\n1\n")
    assert any("unknown file" in e for e in _errors(data))
    (data / "data" / "people" / "extra.csv").unlink()
    _edit(data, "people", lambda rows: rows.clear())
    assert any("people tables empty" in e for e in _errors(data))


def test_xref_grades(data: Path) -> None:
    def bad(rows: Rows) -> None:
        _row(rows, scheme="orcid").update(grade="X")
        c_only = next(r for r in rows if r["scheme"] == "lin_id" and r["grade"] == "C")
        c_only.update(grade="A")
        _row(rows, scheme="lin_id", grade="A").update(notes="")

    _edit(data, "person_xref", bad)
    errs = _errors(data)
    assert any("an ORCID xref is grade A" in e for e in errs)
    assert any("best grade of its LIN sources, C, not A" in e for e in errs)
    assert any("needs notes 'lin sources" in e for e in errs)


def test_observation_consistency(data: Path) -> None:
    obs = read_csv(data / "data" / "people" / "affiliation_observations.csv")
    srcs = {r["source_id"]: r for r in read_csv(data / "data" / "registry" / "sources.csv")}
    other = next(o for o in obs if o["org_id"])["org_id"]

    def bad(rows: Rows) -> None:
        conf = _row(rows, kind="conference")
        conf.update(active_on=conf["active_on"][:8] + ("01" if conf["active_on"][8:] != "01" else "02"))
        eo = next(r for r in rows if r["source_id"].startswith("eo:") and srcs[r["source_id"]]["published_on"])
        eo.update(active_on=eo["active_on"][:4])
        r = next(r for r in rows if r["org_id"] and r["org_id"] != other and r["printed_org"])
        r.update(org_id=other)
        r2 = next(x for x in rows if x["person_id"] != rows[0]["person_id"])
        r2.update(printed_name=rows[0]["printed_name"] + " Other")

    _edit(data, "affiliation_observations", bad)
    errs = _errors(data)
    assert sum("!= source date" in e for e in errs) >= 2
    assert any("contradicts the crosswalk" in e for e in errs)
    assert any("is not a name of" in e for e in errs)


def test_person_status_and_visibility(data: Path) -> None:
    xref = read_csv(data / "data" / "people" / "person_xref.csv")
    lin = {x["person_id"] for x in xref if x["scheme"] == "lin_id"}
    c_only = {x["person_id"] for x in xref if x["scheme"] == "lin_id" and x["grade"] == "C"}

    def bad(rows: Rows) -> None:
        next(r for r in rows if r["person_id"] not in lin).update(research_status="validated")
        next(r for r in rows if r["person_id"] in c_only).update(visibility="public")
        next(r for r in rows if r["visibility"] == "public" and r["person_id"] not in lin).update(visibility="review")

    _edit(data, "people", bad)
    errs = _errors(data)
    assert any("validated is a LIN status" in e for e in errs)
    assert any("public needs >= 1 public observation" in e for e in errs)
    assert any("review person with" in e for e in errs)


@needs_inputs
def test_record_less_ids_are_redirected() -> None:
    """D212: every committed id kept without records points to a surviving person (none on 2026-10-22 is a split)."""
    people = {r["person_id"]: r for r in read_csv(PEOPLE / "people.csv")}
    held = {x["person_id"] for x in read_csv(PEOPLE / "person_xref.csv")}
    empty = set(people) - held
    assert all(people[p]["same_as"] and people[p]["visibility"] == "review" for p in empty)
    assert all(people[r["same_as"]]["same_as"] == "" and r["same_as"] in held for r in people.values() if r["same_as"])


def test_same_as_rules(data: Path) -> None:
    redirected = [r["person_id"] for r in read_csv(data / "data" / "people" / "people.csv") if r["same_as"]]
    if len(redirected) < 2:
        pytest.skip("fixture: needs two redirected ids")
    a, b = redirected[:2]

    def bad(rows: Rows) -> None:
        _row(rows, person_id=a).update(same_as=b)  # target itself redirected
        _row(rows, person_id=b).update(visibility="public")
        held = next(r for r in rows if not r["same_as"] and r["visibility"] == "public")
        held.update(same_as=held["person_id"])  # self redirect on a person with records

    _edit(data, "people", bad)
    errs = _errors(data)
    assert any(f"same_as {b} is itself redirected" in e for e in errs)
    assert any(f"people {b}: redirected" in e and "visibility review" in e for e in errs)
    assert any("is not another person in people.csv" in e for e in errs)
    assert any("still holds person_xref rows" in e for e in errs)


@needs_inputs
def test_ofc_header_rules(data: Path) -> None:
    """D214-D216 validator rules on a copy (staged header rows copied by the fixture)."""
    inp = P.load_inputs()
    conflict = next(f"{s.source_id}#a{s.index}" for s in inp.slots if s.hdr_status == "conflict")
    hdr_path = next((data / P.HEADERS_REL).glob("*/header_rows.csv"))
    staged = read_csv(hdr_path)
    gone = P.header_obs_id(staged[0])
    write_csv(hdr_path, list(staged[0]), staged[1:])
    obs = read_csv(data / "data" / "people" / "affiliation_observations.csv")
    hdr = [  # OFC header rows only (lit header rows have their own rules, D370-D377)
        o
        for o in obs
        if o["obs_id"].startswith("ofc2026:")
        and P.HEADER_ID_RE.search(o["obs_id"])
        and not o["obs_id"].startswith(gone)
    ]
    only_hdr = {_slot_of(o["obs_id"]) for o in hdr}
    only_hdr -= {_slot_of(o["obs_id"]) for o in obs if not P.HEADER_ID_RE.search(o["obs_id"])}
    a_row = next(o for o in hdr if o["evidence_grade"] == "A")
    other = next(o for o in hdr if o["org_id"] and o["org_id"] != a_row["org_id"])
    third = next(o for o in hdr if o["obs_id"] not in (a_row["obs_id"], other["obs_id"]))
    lone = next(
        o
        for o in hdr
        if _slot_of(o["obs_id"]) in only_hdr and o["obs_id"] not in (a_row["obs_id"], other["obs_id"], third["obs_id"])
    )

    def bad(rows: Rows) -> None:
        _row(rows, obs_id=a_row["obs_id"]).update(evidence_grade="B")
        _row(rows, obs_id=other["obs_id"]).update(org_id=a_row["org_id"] or "org_intel")
        _row(rows, obs_id=third["obs_id"]).update(kind="conference")
        next(
            r for r in rows if r["obs_id"].startswith(conflict + ".") and not P.HEADER_ID_RE.search(r["obs_id"])
        ).update(visibility="public")
        slot = _slot_of(lone["obs_id"])
        rows.append(
            dict(
                lone,
                obs_id=f"{slot}.1",
                kind="conference",
                evidence_grade="B",
                aff_role="primary",
                org_id="",
                locator="program metadata authors_json #1",
            )
        )
        rows.sort(key=lambda r: r["obs_id"])

    _edit(data, "affiliation_observations", bad)
    errs = _errors(data)
    assert any(a_row["obs_id"] in e and "is grade A, not B" in e for e in errs)
    assert any(other["obs_id"] in e and "org_id" in e and "!= header row" in e for e in errs)
    assert any(third["obs_id"] in e and "paper-header row" in e for e in errs)
    assert any(conflict in e and "every row must be review (D216)" in e for e in errs)
    assert any("metadata row kept although the paper header confirms it (D215)" in e for e in errs)
    assert any(gone in e and "no staged OFC header row" in e for e in errs)


def test_lit_observation_rules(data: Path) -> None:
    """D370 / D372 validator rules on a copy: a lit observation is a paper-header row of a non-duplicate source."""
    obs = read_csv(data / "data" / "people" / "affiliation_observations.csv")
    lit = [o for o in obs if o["source_id"].startswith("lit:")]
    if len(lit) < 2:
        pytest.skip("no lit observations in the committed tables yet")
    a, b = lit[0], lit[1]

    def bad(rows: Rows) -> None:
        _row(rows, obs_id=a["obs_id"]).update(obs_id=a["obs_id"].rsplit(".h", 1)[0] + ".1")
        _row(rows, obs_id=b["obs_id"]).update(kind="conference", evidence_grade="B")
        rows.sort(key=lambda r: r["obs_id"])

    _edit(data, "affiliation_observations", bad)
    errs = _errors(data)
    assert any("a lit observation is a paper-header row" in e for e in errs)
    assert any(b["obs_id"] in e and "gives kind publication, not conference" in e for e in errs)


def test_rules_people_import_failure_is_an_error(data: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import importlib

    real = importlib.import_module

    def fake(name: str, package: str | None = None) -> object:
        if name == "photonics_atlas.rules_people":
            raise ModuleNotFoundError(name)
        return real(name, package)

    monkeypatch.setattr(importlib, "import_module", fake)
    assert any("rules_people not importable" in e for e in _errors(data))


def test_dense_keys_need_region_and_ambiguity() -> None:
    def sl(sid: str, name: str, country: str) -> P.Slot:
        s = _slot(sid, name, {"o"})
        s.affs = [P.Aff(1, "Lab", ["o"], "", country, "primary", "")]
        return s

    orgs = {"o": {"country": "US"}}
    base = [sl("s:1#1", "Ada Qorvath", "JP"), sl("s:2#1", "Ada Qorvath", "JP"), sl("s:3#1", "Bo Qorvath", "JP")]
    other = [sl("s:4#1", "Ada Zell", "US"), sl("s:5#1", "Bo Zell", "US")]
    keys = P.dense_keys(base + other, orgs, 0.5, 2, 2)
    assert "ada qorvath" in keys  # dense printed country, family and given names both shared
    assert "ada zell" not in keys  # printed country not dense (registry country unused when printed exists)
    assert not P.dense_keys(base, orgs, 0.5, 2, 2)  # given name carried by one full name only: not ambiguous
