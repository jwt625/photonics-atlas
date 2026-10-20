"""People atlas (DevLog-004): merge rules on synthetic slots, the real people tables, and one mutation test per
rules_people rule on a temp copy of the data (as tests/test_validate.py)."""

from __future__ import annotations

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
    # every input affiliation row once: EO 2880 + PK 1996 + OFC minus the 54 presentations already in EO
    # (joint_printed strings add one row per extra org: suffix .k after author.order)
    rows = {
        o["obs_id"].rsplit(".", 1)[0] if o["obs_id"].rsplit("#a", 1)[1].count(".") == 2 else o["obs_id"] for o in obs
    }
    base = Counter(r.split(":")[0] for r in rows)
    assert base == {"eo": 2880, "pk": 1996, "ofc2026": 6056 - 532}
    sources = {r["source_id"]: r for r in read_csv(ROOT / "data" / "registry" / "sources.csv")}
    assert not any(sources[o["source_id"]]["same_as"] for o in obs)
    assert {(o["kind"], o["evidence_grade"]) for o in obs} == {("publication", "A"), ("conference", "B")}


@needs_inputs
def test_local_review_queue_hides_its_people() -> None:
    q = ROOT / "data" / "_local" / "people" / "review_queue.csv"
    if not q.exists():
        pytest.skip("local review queue not built")
    queue = read_csv(q)
    obs = read_csv(PEOPLE / "affiliation_observations.csv")
    people = {r["person_id"]: r for r in read_csv(PEOPLE / "people.csv")}
    n_obs = Counter(o["person_id"] for o in obs)
    demoted = P.demoted_by_queue(queue, dict(n_obs))
    assert demoted and all(o["visibility"] == "review" for o in obs if o["person_id"] in demoted)
    assert all(
        o["visibility"] == "public"
        for o in obs
        if o["person_id"] not in demoted and people[o["person_id"]]["visibility"] == "public"
    )
    # D64 ruling: a partner without observations (LIN-only record) keeps the pair queued but demotes nothing
    assert P.demoted_by_queue([{"person_id_a": "person_a", "person_id_b": "person_b"}], {"person_a": 3}) == {"person_b"}
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
