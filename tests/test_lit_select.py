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
