"""The generated crosswalk is current, consistent with the seed clusters, and meets the P0 acceptance criteria."""

from __future__ import annotations

from collections import Counter

from photonics_atlas.csvio import read_csv, split_list
from photonics_atlas.orgmatch import load_matcher
from photonics_atlas.paths import CROSSWALK, REGISTRY

from .conftest import needs_inputs


def _xw() -> list[dict[str, str]]:
    return read_csv(CROSSWALK / "org_crosswalk.csv")


def test_acceptance_eo_pk_lin_all_map_and_ofc_rows_90pct() -> None:
    rows = _xw()
    for c in ("eo", "pk", "lin"):
        assert all(r["org_ids"] for r in rows if r["corpus"] == c), c
    ofc = [r for r in rows if r["corpus"] == "ofc2026"]
    total = sum(int(r["n_rows"]) for r in ofc) + 1  # + the one author row with an empty affiliation
    mapped = sum(int(r["n_rows"]) for r in ofc if r["org_ids"])
    assert mapped / total >= 0.90


@needs_inputs
def test_crosswalk_is_current() -> None:
    m = load_matcher()
    for r in _xw():
        if r["corpus"] == "lin":
            continue
        ids, basis = m.match(r["printed"], r["corpus"])
        assert (ids, basis) == (split_list(r["org_ids"]), r["match_basis"]), r["printed"]


def test_eo_and_pk_names_map_to_orgs_seeded_from_them() -> None:
    orgs = {o["org_id"]: o for o in read_csv(REGISTRY / "organizations.csv")}
    for r in _xw():
        if r["corpus"] in ("eo", "pk"):
            ids = split_list(r["org_ids"])
            assert len(ids) == 1, r
            assert r["corpus"] in split_list(orgs[ids[0]]["origin"]), r


def test_known_identities() -> None:
    by = {(r["corpus"], r["printed"]): split_list(r["org_ids"]) for r in _xw()}
    assert by[("eo", "Intel Corporation")] == by[("pk", "Intel")] == ["org_intel"]
    assert (
        by[("eo", "Institute of Microelectronics")]
        == by[("pk", "A*STAR Institute of Microelectronics")]
        == ["org_astar_ime"]
    )
    assert by[("eo", "Coherent Corp.")] == ["org_coherent"]
    assert by[("eo", "Nokia Bell Labs")] == ["org_nokia_bell_labs"]


def test_lin_ids_are_registry_ids() -> None:
    orgs = {o["org_id"] for o in read_csv(REGISTRY / "organizations.csv")}
    lin = [r["printed"] for r in _xw() if r["corpus"] == "lin"]
    assert len(lin) == 172 and set(lin) <= orgs


def test_no_org_name_key_collision_among_matchable() -> None:
    from photonics_atlas.textnorm import norm_key

    keys = Counter(
        norm_key(o["name"]) for o in read_csv(REGISTRY / "organizations.csv") if o["no_name_match"] != "true"
    )
    assert [k for k, n in keys.items() if n > 1] == []


def test_no_name_match_org_not_routed_by_ror_display() -> None:
    """D310: a no_name_match org is matched only through its aliases, also not through its ROR display / label
    (Italy's CNR, ROR display "National Research Council")."""
    m = load_matcher()
    assert m.match("National Research Council", "ofc2026") == ([], "unmapped")
    assert m.match("Consiglio Nazionale delle Ricerche", "ofc2026") == (["org_national_research_council"], "alias")
    assert m.match("ams", "ofc2026") == ([], "unmapped")
    assert m.match("ams AG", "lit") == (["org_ams_ag"], "alias")


def test_ror_labels_split_from_json_dump() -> None:
    """D313: ROR labels come one per name from the JSON dump (the CSV joins variants of one language with ", ")."""
    from photonics_atlas.adapters import ror

    idx = ror.load()
    rec = idx.records["https://ror.org/04mte1k06"]
    assert "National Research Council of Canada" in rec.labels
    assert "Senju Metal Industry Co., Ltd." in idx.records["https://ror.org/009571x53"].labels
    m = load_matcher()
    assert m.match("National Research Council of Canada", "ofc2026") == (
        ["org_national_research_council_canada"],
        "ror",
    )
