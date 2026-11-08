"""Pure-function tests for scripts/lit_select.py: paper_id pinning (D230) and the increment delta (D231). No files."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import lit_select as ls  # noqa: E402

CFG = {"max_per_senior_author": 4, "paywalled_min_score": 8, "oa_target_fraction": 0.8}


def rec(uid: str, cls: str = "laser", score: int = 9, year: int = 2024, **kw: Any) -> dict[str, Any]:
    r: dict[str, Any] = {
        "uid": uid,
        "authors": [kw.pop("first", "Ann Smith")],
        "year": year,
        "is_oa": True,
        "_cls": cls,
        "_sub": f"{cls}.other",
        "_la": kw.pop("la", uid),
        "_s": {"score": score, "classes": [cls]},
        "_reason": "rank",
        "_alts": [],
    }
    r.update(kw)
    return r


def prev_row(r: dict[str, Any], pid: str, reason: str = "rank") -> dict[str, str]:
    return {
        "uid": r["uid"],
        "paper_id": pid,
        "primary_class": r["_cls"],
        "score": str(r["_s"]["score"]),
        "access": "oa",
        "year": str(r["year"]),
        "selection_reason": reason,
        "last_author": r["_la"],
        "title": r["uid"],
    }


def test_assign_paper_ids_pins_uid_alt_and_reserves_previous_ids() -> None:
    a = rec("u-a", first="X Isichenko", year=2024)  # previously isichenko2023 under the same uid
    b = rec("u-b", first="Y Gao", year=2021, _alts=["u-old"])  # family member u-old was gao2021
    c = rec("u-c", first="Z Gao", year=2021)  # new work: must not take gao2021 or gao2021a
    pins = {"u-a": "isichenko2023", "u-old": "gao2021", "u-gone": "gao2021a"}
    assert ls.assign_paper_ids([c, a, b], pins) == ["gao2021b", "isichenko2023", "gao2021"]


def test_delta_select_frozen_curator_class_and_cap() -> None:
    inc = {u: rec(u, score=8, year=2010) for u in ("i1", "i2", "i3", "i4")}
    inc["w1"] = rec("w1", cls="wdm", score=8, year=2010)
    prev = [
        prev_row(inc["i1"], "p1"),  # dropped, frozen (cached / day 1-2)
        prev_row(inc["i2"], "p2", reason="curator: benchmark"),  # dropped, curator pick
        prev_row(inc["i3"], "p3"),  # dropped, displaceable
        prev_row(inc["i4"], "p4"),  # kept by the rules
        prev_row(inc["w1"], "p5"),  # dropped, displaceable, other class
    ]
    n1 = rec("n1", score=10)  # enters, displaces p3
    n2 = rec("n2", score=9)  # no laser slot left -> blocked (may not take the wdm slot)
    selected = {"i4": {**inc["i4"], "_reason": "rank"}, "n1": n1, "n2": n2}
    elig = {**inc, "n1": n1, "n2": n2}
    final, rep = ls.delta_select(selected, elig, {}, prev, {"p1": "cached"}, set(), CFG, {"laser": 4, "wdm": 1})
    assert [(r["uid"], i["uid"]) for r, i in rep["swaps"]] == [("n1", "i3")]
    assert [r["uid"] for r, _ in rep["blocked"]] == ["n2"]
    assert {p["uid"] for p, _ in rep["kept_frozen"]} == {"i1", "i2"}
    assert set(final) == {"i1", "i2", "i4", "w1", "n1"}
    assert final["i1"]["_reason"] == "rank"  # a frozen row keeps its previous reason

    # senior-author cap: 4 incumbents of one senior author stay, a fifth from the same author may not enter
    same = {u: rec(u, la="dai") for u in ("a1", "a2", "a3", "a4")}
    prev2 = [prev_row(r, f"q{i}") for i, r in enumerate(same.values())] + [prev_row(inc["i3"], "p3")]
    n3 = rec("n3", la="dai", score=10)
    sel2 = {**{u: {**r} for u, r in same.items()}, "n3": n3}
    _, rep2 = ls.delta_select(sel2, {**same, "i3": inc["i3"], "n3": n3}, {}, prev2, {}, set(), CFG, {"laser": 5})
    assert not rep2["swaps"] and "senior-author cap" in rep2["blocked"][0][1]


def test_delta_select_curator_pick_without_slot_enters_beyond_budget() -> None:
    w1 = rec("w1", cls="wdm", score=9, year=2010)
    prev = [prev_row(w1, "p1")]  # kept by the rules: no displaceable wdm slot
    pick = rec("np", cls="wdm", score=8, _reason="curator: owner add")
    plain = rec("nr", cls="wdm", score=10)
    selected = {"w1": {**w1, "_reason": "rank"}, "np": pick, "nr": plain}
    final, rep = ls.delta_select(selected, {"w1": w1, "np": pick, "nr": plain}, {}, prev, {}, {"np"}, CFG, {"wdm": 1})
    assert [r["uid"] for r in rep["added"]] == ["np"] and not rep["swaps"]
    assert [r["uid"] for r, _ in rep["blocked"]] == ["nr"]  # a rule pick stays blocked
    assert set(final) == {"w1", "np"}


def test_delta_select_beyond_budget_adds_append_without_swap_or_caps() -> None:
    """D926: beyond_budget adds are appended; displaceable incumbents stay; caps do not bind; listed works skip."""
    inc = rec("i1", score=7, year=2010)  # dropped by the rules, displaceable
    keep = rec("k1", la="dai")
    prev = [prev_row(inc, "p1"), prev_row(keep, "p2")]
    selected = {"k1": {**keep, "_reason": "rank"}}
    pw = {f"b{i}": rec(f"b{i}", is_oa=False, score=8, la="dai", _reason="curator: add: owner") for i in range(5)}
    listed = rec("k1", _reason="curator: add: owner")  # same work as a previous row: not added twice
    beyond = [*pw.values(), listed]
    cfg = {**CFG, "max_per_senior_author": 1}  # the senior-author and paywalled caps would block every one
    final, rep = ls.delta_select(selected, {"i1": inc, "k1": keep}, {}, prev, {}, set(), cfg, {"laser": 2}, beyond)
    assert not rep["swaps"]
    assert [r["uid"] for r in rep["added"]] == list(pw)
    assert [(r["uid"], why) for r, why in rep["blocked"]] == [("k1", "beyond_budget add already in the list")]
    assert set(final) == {"i1", "k1", *pw}  # the displaceable incumbent stays
    assert final["i1"]["_reason"] == "rank" and final["k1"]["_reason"] == "rank"


def test_delta_select_beyond_budget_add_selected_by_rules_is_not_a_swap() -> None:
    """D926: a beyond_budget add that the unconstrained run also selects does not take a displaceable slot."""
    inc = rec("i1", score=7, year=2010)
    prev = [prev_row(inc, "p1")]
    bb = rec("b1", score=10, _reason="curator: add: owner")
    selected = {"b1": {**bb, "_reason": "rank"}}
    final, rep = ls.delta_select(selected, {"i1": inc, "b1": bb}, {}, prev, {}, set(), CFG, {"laser": 1}, [bb])
    assert not rep["swaps"] and [r["uid"] for r in rep["added"]] == ["b1"] and not rep["entering"]
    assert set(final) == {"i1", "b1"} and final["b1"]["_reason"] == "curator: add: owner"


def test_delta_select_keeps_previous_beyond_budget_row_verbatim_except_rank() -> None:
    """A previous beyond_budget add whose scored record now says another class / subtype keeps its row."""
    bb = rec("b1", cls="resonator", score=9, _sub="resonator.ring")  # LLM class differs from the curator class
    row = {**prev_row(bb, "liu2018a", reason="curator: add: owner"), "primary_class": "laser",
           "subtype": "laser.dfb", "rank": "17", "classes": "resonator"}  # fmt: skip
    keep = rec("k1", cls="laser")
    prev = [row, prev_row(keep, "p2")]
    selected = {"k1": {**keep, "_reason": "rank"}, "b1": {**bb, "_reason": "rank"}}
    final, rep = ls.delta_select(
        selected, {"b1": bb, "k1": keep}, {}, prev, {}, set(), CFG, {"laser": 1, "resonator": 1}, [bb]
    )
    assert not rep["swaps"] and not rep["added"]
    assert final["b1"]["_verbatim"] == row and final["b1"]["_cls"] == "laser"
    assert final["b1"]["_reason"] == "curator: add: owner"


def test_delta_select_keeps_previous_arxiv_id() -> None:
    """A previous row's arxiv_id survives although the current record (DOI-only curator add) has none."""
    r = rec("10.1038/x", cls="waveguide_platform", arxiv_id="", doi="10.1038/x")
    row = {**prev_row(r, "alexander2024", reason="curator: add: coordinator"), "arxiv_id": "2404.17570"}
    selected = {r["uid"]: {**r, "_reason": "curator: add: coordinator"}}
    final, _ = ls.delta_select(selected, {r["uid"]: r}, {}, [row], {}, {r["uid"]}, CFG, {"waveguide_platform": 1})
    assert final[r["uid"]]["_verbatim"]["arxiv_id"] == "2404.17570"
    assert final[r["uid"]]["_verbatim"] == row
