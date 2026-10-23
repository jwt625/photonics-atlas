"""Build the person registry and affiliation observations (DevLog-004, D61-D70).

Inputs (read-only): LIN people + edges, EO people / paper_authors / author_affiliations / papers / crossref.json, PK
author_affiliations / papers, OFC 2026 authors_json, OFC 2026 paper-header rows staged by DevLog-008
(data/_staging/people/ofc_headers/*/header_rows.csv, batches with a current check stamp; D214-D219); registry
organizations / sources and the org crosswalk.
Writes data/people/{people,person_aliases,person_xref,affiliation_observations}.csv and the local-only review queue
data/_local/people/review_queue.csv (name-only and other unconfirmed identity pairs; never committed, D64).

Curated rows are kept: existing people.csv rows (new persons appended; derived fields refreshed: visibility, a
display_name no longer printed by any of the person's records, a disambiguator copied from LIN, D93/D94;
same_as of ids kept without records, D212),
person_aliases rows with origin manual, person_xref rows with basis manual. Person ids are reused through obs_id and EO
xrefs and never reassigned (D65).

Usage:
  uv run python scripts/build_people.py [--dry-run]
  uv run python scripts/build_people.py --only "Ada Example" --only "Wei Sample"  # pilot: those family blocks, report only
  uv run python scripts/build_people.py --limit 50                              # pilot: first 50 family blocks, report only
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict

from photonics_atlas import people as P
from photonics_atlas.csvio import write_csv
from photonics_atlas.paths import ROOT
from photonics_atlas.runlog import RunLog
from photonics_atlas.schema import columns

OUT = ROOT / "data" / "people"
LOCAL = ROOT / "data" / "_local" / "people"
QUEUE_COLS = [
    "person_id_a",
    "person_id_b",
    "reason",
    "flags",
    "n_slot_pairs",
    "name_a",
    "name_b",
    "example_a",
    "example_b",
]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="compute and report, write nothing")
    ap.add_argument("--only", action="append", default=[], help="pilot: names whose family blocks are resolved")
    ap.add_argument("--limit", type=int, default=0, help="pilot: resolve only the first N family blocks")
    ap.add_argument(
        "--retire-orphans",
        action="store_true",
        help="drop old ids that no longer hold any record (allowed only before the first commit of data/people, D96)",
    )
    args = ap.parse_args()
    pilot = bool(args.only or args.limit)
    with RunLog("build_people", args.dry_run or pilot) as log:
        inp = P.load_inputs()
        slots = inp.slots
        log.info(f"slots {len(slots)} by corpus {dict(Counter(s.corpus for s in slots))}; dropped {dict(inp.dropped)}")
        log.info(f"common family names {len(inp.common)} (EO list {len(P.EO_COMMON)})")
        _, stale = P.header_batches()
        log.info(f"OFC header merge (D214-D219): {dict(inp.headers)}; stale batches skipped: {[d.name for d in stale]}")
        log.event("inputs", slots=dict(Counter(s.corpus for s in slots)), dropped=dict(inp.dropped))
        blocks: set[str] | None = None
        if args.only:
            blocks = {P.tokens(n)[1] for n in args.only}
        elif args.limit:
            blocks = set(sorted({v.fam for s in slots for v in s.variants})[: args.limit])
        ident = P.resolve(inp, blocks)
        log.info(f"merges {dict(ident.merges)}; review/blocked slot pairs {len(ident.review)}")
        clusters: dict[int, list[P.Slot]] = defaultdict(list)
        for i, c in enumerate(ident.cluster_of):
            clusters[c].append(slots[i])
        names = {c: P.display_name(ms) for c, ms in clusters.items()}

        old_people = P.read_optional(OUT / "people.csv")
        old_obs = {r["obs_id"]: r["person_id"] for r in P.read_optional(OUT / "affiliation_observations.csv")}
        old_xref = P.read_optional(OUT / "person_xref.csv")
        old_alias = P.read_optional(OUT / "person_aliases.csv")
        old_ids = {r["person_id"] for r in old_people}
        pid_of = P.assign_ids(clusters, names, old_obs, old_xref, old_ids)
        queue = P.review_pairs(ident, slots, pid_of)
        queued = {r["person_id_a"] for r in queue} | {r["person_id_b"] for r in queue}
        n_obs = {pid_of[c]: sum(len(P.obs_ids(s)) for s in ms) for c, ms in clusters.items()}
        demoted = P.demoted_by_queue(queue, n_obs)  # D64 ruling: a partner without observations demotes nothing
        idx = {s.sid: i for i, s in enumerate(slots)}

        people_rows = {r["person_id"]: r for r in old_people}
        new_people = 0
        refreshed: Counter[str] = Counter()
        alias_rows: dict[tuple[str, str], dict[str, str]] = {
            (r["person_id"], r["alias"]): r for r in old_alias if r["origin"] == "manual"
        }
        xref_rows: dict[tuple[str, str, str], dict[str, str]] = {
            (r["person_id"], r["scheme"], r["value"]): r for r in old_xref if r["basis"] == "manual"
        }
        obs_rows: list[dict[str, str]] = []
        for c, ms in sorted(clusters.items(), key=lambda kv: pid_of[kv[0]]):
            pid = pid_of[c]
            ms.sort(key=lambda s: s.sid)
            lin = next((s.lin for s in ms if s.lin_id), {})
            orcids = sorted({s.orcid for s in ms if s.orcid})
            if pid not in people_rows:
                new_people += 1
                people_rows[pid] = {
                    "person_id": pid,
                    "display_name": names[c],
                    "orcid": orcids[0] if orcids else "",
                    "disambiguator": "",  # D93: LIN name_disambiguator is a career claim, not copied
                    "research_status": lin.get("research_status") or "not_started",
                    "notes": "",
                }
            else:
                row = people_rows[pid]
                if lin and row["disambiguator"] and row["disambiguator"] == lin.get("name_disambiguator"):
                    row["disambiguator"] = ""  # D93
                    refreshed["disambiguator_cleared"] += 1
                if row["orcid"] != (orcids[0] if orcids else ""):
                    row["orcid"] = orcids[0] if orcids else ""  # derived from the person's records (D90 splits)
                    refreshed["orcid"] += 1
                if not lin and row["display_name"] not in {s.name for s in ms}:
                    row["display_name"] = names[c]  # D90 split: the old form is no longer this person's
                    refreshed["display_name"] += 1
            for a in P.alias_rows(pid, people_rows[pid]["display_name"], ms):
                alias_rows.setdefault((pid, a["alias"]), a)
            xs = P.xref_rows(pid, ms, ident, idx, inp)
            for x in xs:
                xref_rows.setdefault((pid, x["scheme"], x["value"]), x)
            lin_grade = next((x["grade"] for x in xs if x["scheme"] == "lin_id"), "")
            c_only_lin = bool(lin_grade) and lin_grade not in ("A", "B")  # D94: identity rests on grade C/X only
            n_public = 0
            for s in ms:
                for oid, aff, org_id in P.obs_ids(s):
                    kind = aff.kind or s.kind
                    grade = aff.grade or ("A" if kind == "publication" else "B")  # D214: header rows carry their grade
                    conflict = s.hdr_status == "conflict"  # D216 (DevLog-008 D281): both sides review until resolved
                    vis = "review" if pid in demoted or c_only_lin or conflict or grade not in "AB" else "public"
                    n_public += vis == "public"
                    obs_rows.append(
                        {
                            "obs_id": oid,
                            "person_id": pid,
                            "printed_name": aff.printed_name or s.name,
                            "org_id": org_id,
                            "printed_org": aff.printed_org,
                            "unit": aff.unit,
                            "country": aff.country,
                            "kind": kind,
                            "aff_role": aff.role,
                            "active_on": s.active_on,
                            "source_id": s.source_id,
                            "locator": aff.locator,
                            "evidence_grade": grade,
                            "visibility": vis,
                        }
                    )
            people_rows[pid]["visibility"] = (
                "public" if not c_only_lin and (n_public or lin_grade in ("A", "B")) else "review"
            )
        obs_rows.sort(key=lambda r: r["obs_id"])
        orphans = sorted(old_ids - set(pid_of.values()))
        if args.retire_orphans:
            for pid in orphans:
                del people_rows[pid]
            log.info(f"retired {len(orphans)} old ids without records (pre-commit, D96): {orphans}")
            orphans = []
        for pid in orphans:
            people_rows[pid]["visibility"] = "review"  # kept without records (D65): nothing to show
        redirects = P.same_as_redirects(people_rows, orphans, old_obs, {r["obs_id"]: r["person_id"] for r in obs_rows})
        for pid, row in people_rows.items():
            new = redirects.get(pid, "")
            if row.get("same_as", "") != new:
                refreshed["same_as_set" if new else "same_as_cleared"] += 1
            row["same_as"] = new
        unresolved = sorted(set(orphans) - set(redirects))
        if unresolved:
            log.info(f"kept without records and no single surviving person (same_as empty, D212): {unresolved}")
        stats = {
            "people": len(people_rows),
            "people_new": new_people,
            "people_kept_without_records": len(orphans),
            "people_redirected": sum(1 for r in people_rows.values() if r.get("same_as")),
            "people_by_visibility": dict(Counter(r.get("visibility", "") for r in people_rows.values())),
            "people_refreshed": dict(refreshed),
            "xref_by_scheme_basis": dict(Counter(f"{x['scheme']}/{x['basis']}" for x in xref_rows.values())),
            "aliases": len(alias_rows),
            "observations": len(obs_rows),
            "obs_by_kind_grade": dict(Counter(f"{r['kind']}/{r['evidence_grade']}" for r in obs_rows)),
            "obs_by_visibility": dict(Counter(r["visibility"] for r in obs_rows)),
            "obs_unmapped_org": sum(1 for r in obs_rows if not r["org_id"]),
            "obs_ofc_header": sum(1 for r in obs_rows if P.HEADER_ID_RE.search(r["obs_id"])),
            "ofc_header_slots": dict(Counter(s.hdr_status for s in slots if s.hdr_status)),
            "review_pairs": len(queue),
            "review_persons": len(queued),
            "review_persons_demoted": len(demoted),
            "review_by_reason": dict(Counter(r["reason"] for r in queue)),
            "persons_by_corpus_mix": dict(
                Counter("+".join(sorted({s.corpus for s in ms})) for ms in clusters.values())
            ),
        }
        for k, v in stats.items():
            log.info(f"{k}: {v}")
        log.event("stats", "ok", stats=stats)
        if pilot:
            report(log, args.only, clusters, pid_of, names, queue, ident, idx)
            return 0
        if args.dry_run:
            return 0
        write_csv(OUT / "people.csv", columns("people"), [people_rows[k] for k in sorted(people_rows)])
        write_csv(OUT / "person_aliases.csv", columns("person_aliases"), [alias_rows[k] for k in sorted(alias_rows)])
        write_csv(OUT / "person_xref.csv", columns("person_xref"), [xref_rows[k] for k in sorted(xref_rows)])
        write_csv(OUT / "affiliation_observations.csv", columns("affiliation_observations"), obs_rows)
        write_csv(LOCAL / "review_queue.csv", QUEUE_COLS, queue)
        log.info(f"wrote data/people/*.csv and data/_local/people/review_queue.csv ({len(queue)} pairs, local only)")
    return 0


def report(
    log: RunLog,
    only: list[str],
    clusters: dict[int, list[P.Slot]],
    pid_of: dict[int, str],
    names: dict[int, str],
    queue: list[dict[str, str]],
    ident: P.Identity,
    idx: dict[str, int],
) -> None:
    """Pilot report (log file only; logs/ is git-ignored)."""
    keys = {P.name_key(n) for n in only}
    for c, ms in sorted(clusters.items(), key=lambda kv: pid_of[kv[0]]):
        if keys and not any(P.name_key(n) in keys for s in ms for n in s.names):
            continue
        pid = pid_of[c]
        log.info(f"PILOT {pid} '{names[c]}' slots={len(ms)} corpora={dict(Counter(s.corpus for s in ms))}")
        for s in ms:
            log.info(
                f"  {s.sid} {s.name!r} {s.active_on} roots={sorted(s.roots)} orcid={s.orcid or '-'} "
                f"join={ident.join_basis.get(idx[s.sid], 'seed')}"
            )
        for q in queue:
            if pid in (q["person_id_a"], q["person_id_b"]):
                log.info(f"  review {q['person_id_a']} ~ {q['person_id_b']} {q['reason']} [{q['flags']}]")


if __name__ == "__main__":
    sys.exit(main())
