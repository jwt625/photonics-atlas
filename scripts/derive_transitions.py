"""Derive publication-sequence transitions from affiliation observations (DevLog-004 D68/D69, assessment C.1).

Local only: writes data/_local/people/{transitions,name_only_candidates}.csv and funnel.json (git-ignored; grade X
derived signals about living people are never committed or shown, D10/D64).

Per person: observations with a registry org are grouped by root org (parent chain collapsed). A -> B when the last A
observation ends before the first B observation starts and no source lists both; gap >= 90 days when both dates have
day precision, else a later calendar year. Overlapping groups are co-affiliations (counted, no arrow). An org event
whose participants' roots are A and B, dated on or before the first B observation (or undated), makes the pair an
acquisition_continuation (not a person transition). EO present_address rows give explicit_move_statement rows.
D69: the same derivation on persons joined through review-queue exact-name pairs gives name-only candidates.

Usage: uv run python scripts/derive_transitions.py [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass

from photonics_atlas import people as P
from photonics_atlas.csvio import read_csv, write_csv
from photonics_atlas.paths import REGISTRY, ROOT
from photonics_atlas.runlog import RunLog
from photonics_atlas.validate import pdate_hi, pdate_lo

PEOPLE = ROOT / "data" / "people"
LOCAL = ROOT / "data" / "_local" / "people"
GAP_DAYS = 90
COLS = [
    "transition_id",
    "person_id",
    "from_org_id",
    "to_org_id",
    "from_last_on",
    "to_first_on",
    "gap_days",
    "basis",
    "direction_status",
    "directness",
    "grade",
    "identity_support",
    "org_class",
    "source_pair",
    "event_id",
    "from_obs_ids",
    "to_obs_ids",
]


@dataclass
class Group:
    root: str
    obs: list[dict[str, str]]

    @property
    def last(self) -> dict[str, str]:
        return max(self.obs, key=lambda o: (pdate_hi(o["active_on"]), o["obs_id"]))

    @property
    def first(self) -> dict[str, str]:
        return min(self.obs, key=lambda o: (pdate_lo(o["active_on"]), o["obs_id"]))

    @property
    def sources(self) -> set[str]:
        return {o["source_id"] for o in self.obs}


def slot_sid(obs_id: str) -> str:
    src, _, rest = obs_id.partition("#a")
    return f"{src}#{rest.split('.')[0]}"


def org_class(org: dict[str, str]) -> str:
    t = org.get("org_type", "unknown")
    return "uni" if t in P.UNI_TYPES else ("unk" if t == "unknown" else "ind")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    with RunLog("derive_transitions", args.dry_run) as log:
        orgs = {r["org_id"]: r for r in read_csv(REGISTRY / "organizations.csv")}
        root = {o: P.org_root(orgs, o) for o in orgs}
        events = {r["event_id"]: r for r in read_csv(REGISTRY / "org_events.csv")}
        ev_roots: dict[str, set[str]] = defaultdict(set)
        for p in read_csv(REGISTRY / "org_event_participants.csv"):
            ev_roots[p["event_id"]].add(root.get(p["org_id"], p["org_id"]))
        obs = read_csv(PEOPLE / "affiliation_observations.csv")
        queue = P.read_optional(LOCAL / "review_queue.csv")
        inp = P.load_inputs()
        slots = {s.sid: s for s in inp.slots}

        def continuation(a: str, b: str, first_b: str) -> str:
            for eid in sorted(ev_roots):
                if {a, b} <= ev_roots[eid]:
                    e = events[eid]
                    d = e["effective_on"] or e["announced_on"]
                    if not d or pdate_lo(d) <= pdate_hi(first_b):
                        return eid
            return ""

        def identity(ga: Group, gb: Group) -> str:
            sa = [slots[slot_sid(o["obs_id"])] for o in ga.obs if slot_sid(o["obs_id"]) in slots]
            sb = [slots[slot_sid(o["obs_id"])] for o in gb.obs if slot_sid(o["obs_id"]) in slots]
            if any(x.orcid and x.orcid == y.orcid for x in sa for y in sb):
                return "orcid"
            if any((x.coauthors & y.coauthors) - x.selfkeys - y.selfkeys for x in sa for y in sb):
                return "shared_coauthor"
            return "name_and_org_chain"

        def derive(
            pid: str, rows: list[dict[str, str]], f: Counter[str], who: dict[str, set[str]]
        ) -> list[dict[str, str]]:
            by: dict[str, list[dict[str, str]]] = defaultdict(list)
            for o in rows:
                if o["org_id"]:
                    by[root[o["org_id"]]].append(o)
            groups = [Group(r, by[r]) for r in sorted(by)]
            if len(groups) < 2:
                return []
            who["ge2_org_groups"].add(pid)
            out = []
            for ga in groups:
                for gb in groups:
                    if ga.root == gb.root:
                        continue
                    la, fb = ga.last, gb.first
                    if ga.sources & gb.sources:
                        f["pairs_co_listed"] += 1
                        continue
                    if not pdate_hi(la["active_on"]) < pdate_lo(fb["active_on"]):
                        if ga.root < gb.root and not pdate_hi(gb.last["active_on"]) < pdate_lo(ga.first["active_on"]):
                            f["pairs_overlapping_co_affiliation"] += 1
                        continue
                    f["strict_ordered"] += 1
                    who["strict_ordered"].add(pid)
                    day = len(la["active_on"]) == 10 and len(fb["active_on"]) == 10
                    gap = (
                        dt.date.fromisoformat(pdate_lo(fb["active_on"]))
                        - dt.date.fromisoformat(pdate_hi(la["active_on"]))
                    ).days
                    if day and gap < GAP_DAYS or not day and fb["active_on"][:4] <= la["active_on"][:4]:
                        f["removed_by_gap"] += 1
                        continue
                    f["after_gap"] += 1
                    who["after_gap"].add(pid)
                    eid = continuation(ga.root, gb.root, fb["active_on"])
                    basis = "acquisition_continuation" if eid else "publication_sequence"
                    f[basis] += 1
                    out.append(
                        {
                            "transition_id": f"transition_{pid.removeprefix('person_')}__{ga.root.removeprefix('org_')}__{gb.root.removeprefix('org_')}",
                            "person_id": pid,
                            "from_org_id": ga.root,
                            "to_org_id": gb.root,
                            "from_last_on": la["active_on"],
                            "to_first_on": fb["active_on"],
                            "gap_days": str(gap),
                            "basis": basis,
                            "direction_status": "confirmed" if not eid else "unknown",
                            "directness": "unknown",
                            "grade": "X",
                            "identity_support": identity(ga, gb),
                            "org_class": f"{org_class(orgs[ga.root])}->{org_class(orgs[gb.root])}",
                            "source_pair": f"{la['source_id'].split(':')[0]}->{fb['source_id'].split(':')[0]}",
                            "event_id": eid,
                            "from_obs_ids": ";".join(sorted(o["obs_id"] for o in ga.obs)),
                            "to_obs_ids": ";".join(sorted(o["obs_id"] for o in gb.obs)),
                        }
                    )
            return out

        by_person: dict[str, list[dict[str, str]]] = defaultdict(list)
        for o in obs:
            by_person[o["person_id"]].append(o)
        funnel: Counter[str] = Counter()
        funnel["persons_with_observations"] = len(by_person)
        who: dict[str, set[str]] = defaultdict(set)
        rows: list[dict[str, str]] = []
        for pid in sorted(by_person):
            rows += derive(pid, by_person[pid], funnel, who)
        # Explicit move statements: present_address rows (primary org of the same slot -> present-address org).
        by_slot: dict[str, list[dict[str, str]]] = defaultdict(list)
        for o in obs:
            by_slot[slot_sid(o["obs_id"])].append(o)
        for _sid, os_ in sorted(by_slot.items()):
            pres = [o for o in os_ if o["aff_role"] == "present_address" and o["org_id"]]
            prim = [o for o in os_ if o["aff_role"] == "primary" and o["org_id"]]
            for pa in pres:
                for pr in prim:
                    a, b = root[pr["org_id"]], root[pa["org_id"]]
                    if a == b:
                        continue
                    funnel["explicit_move_statement"] += 1
                    rows.append(
                        {
                            "transition_id": f"transition_{pr['person_id'].removeprefix('person_')}__{a.removeprefix('org_')}__{b.removeprefix('org_')}__stmt",
                            "person_id": pr["person_id"],
                            "from_org_id": a,
                            "to_org_id": b,
                            "from_last_on": pr["active_on"],
                            "to_first_on": pa["active_on"],
                            "gap_days": "",
                            "basis": "explicit_move_statement",
                            "direction_status": "confirmed",
                            "directness": "unknown",
                            "grade": "A",
                            "identity_support": "same_record",
                            "org_class": f"{org_class(orgs[a])}->{org_class(orgs[b])}",
                            "source_pair": f"{pr['source_id'].split(':')[0]}->{pa['source_id'].split(':')[0]}",
                            "event_id": "",
                            "from_obs_ids": pr["obs_id"],
                            "to_obs_ids": pa["obs_id"],
                        }
                    )
        moves = [r for r in rows if r["basis"] == "publication_sequence"]
        summary: dict[str, object] = {
            "funnel": dict(funnel),
            "persons": {k: len(v) for k, v in sorted(who.items())},
            "candidate_moves": len(moves),
            "candidate_move_persons": len({r["person_id"] for r in moves}),
            "by_class": dict(Counter(r["org_class"] for r in moves)),
            "by_identity": dict(Counter(r["identity_support"] for r in moves)),
            "by_source_pair": dict(Counter(r["source_pair"] for r in moves)),
            "continuation_events": dict(Counter(r["event_id"] for r in rows if r["event_id"])),
        }

        # D69: persons joined through exact-name review pairs (name-only identity), transitions needing such a link.
        uf: dict[str, str] = {}

        def find(x: str) -> str:
            uf.setdefault(x, x)
            while uf[x] != x:
                uf[x] = uf[uf[x]]
                x = uf[x]
            return x

        flags_of: dict[tuple[str, str], str] = {}
        for q in queue:
            if "exact_name" in q["flags"].split(";"):  # exact-name pairs, any reason (D69)
                ra, rb = find(q["person_id_a"]), find(q["person_id_b"])
                uf[max(ra, rb)] = min(ra, rb)
                flags_of[(q["person_id_a"], q["person_id_b"])] = q["flags"]
        comps: dict[str, list[str]] = defaultdict(list)
        for pid in list(uf):
            comps[find(pid)].append(pid)
        nf: Counter[str] = Counter()
        nwho: dict[str, set[str]] = defaultdict(set)
        cand: list[dict[str, str]] = []
        common_risk = 0
        for c, pids in sorted(comps.items()):
            if len(pids) < 2:
                continue
            merged = [o for p in pids for o in by_person.get(p, [])]
            for r in derive(c, merged, nf, nwho):
                fo, to = set(r["from_obs_ids"].split(";")), set(r["to_obs_ids"].split(";"))
                owners_from = {o["person_id"] for o in merged if o["obs_id"] in fo}
                owners_to = {o["person_id"] for o in merged if o["obs_id"] in to}
                if owners_from & owners_to:
                    continue  # already derivable inside one registry person
                if r["basis"] != "publication_sequence":
                    nf["name_only_continuations"] += 1
                    continue
                fl = " ".join(flags_of.get((min(a, b), max(a, b)), "") for a in owners_from for b in owners_to)
                r["identity_support"] = "name_shared_coauthor" if "shared_coauthor" in fl else "name_only"
                common_risk += "common_family_name" in fl
                r["person_id"] = ";".join(sorted(owners_from | owners_to))
                r["transition_id"] = "candidate_" + r["transition_id"].removeprefix("transition_")
                cand.append(r)
        summary["name_only"] = {
            "components": sum(1 for p in comps.values() if len(p) > 1),
            "funnel_on_joined_components": dict(nf),
            "persons_on_joined_components": {k: len(v) for k, v in sorted(nwho.items())},
            "candidate_moves": len(cand),
            "candidate_move_components": len({r["person_id"] for r in cand}),
            "by_identity": dict(Counter(r["identity_support"] for r in cand)),
            "by_class": dict(Counter(r["org_class"] for r in cand)),
            "by_source_pair": dict(Counter(r["source_pair"] for r in cand)),
            "common_family_name_pairs": common_risk,
        }
        for k, v in summary.items():
            log.info(f"{k}: {v}")
        log.event("funnel", "ok", summary=summary)
        if not args.dry_run:
            rows.sort(key=lambda r: r["transition_id"])
            cand.sort(key=lambda r: r["transition_id"])
            write_csv(LOCAL / "transitions.csv", COLS, rows)
            write_csv(LOCAL / "name_only_candidates.csv", COLS, cand)
            (LOCAL / "funnel.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
            log.info(
                f"wrote data/_local/people/ transitions {len(rows)}, name-only candidates {len(cand)} (local only)"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
