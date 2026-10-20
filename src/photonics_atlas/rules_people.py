"""People atlas rule checks (DevLog-004, D61-D70), called by validate.py as rules(ok_tables, all_tables, report).

Cell types, patterns, enums, keys and foreign keys (people, organizations, sources) are checked by validate.py from
data/schema/people.schema.yaml. This module adds: obs_id / source consistency; canonical sources only (no same_as);
corpus vs kind and kind vs grade (publication A, conference B); active_on vs the source year and not in the future;
public visibility needs A/B; LIN ids reused verbatim; ORCID field vs xref; xref basis vs grade and scheme; manual
xrefs need reviewed_on; no e-mail addresses; and, when the local review queue exists, no public observation of a
person in it. Audit corrections (D90-D94): no LinkedIn / move / career wording; only the four tables in data/people/;
scheme orcid grade A; lin_id grade = best grade of the recorded LIN sources; org_id agrees with the crosswalk; active_on
equals the source date (EO published_on, OFC session date, PK year); printed_name is one of the person's names;
validated only for LIN people; person visibility derived from observations and LIN grades; empty tables are errors.
Round 2 (D96-D97): phone numbers and wider spelled-out e-mail; status wording in notes-type cells; one ORCID per
person; every split EO person queued; queue demotion only through partners with observations; paths from the root.
"""

from __future__ import annotations

import datetime as dt
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from .csvio import read_csv
from .paths import ROOT
from .people import SPELLED_EMAIL_RE, clean_text
from .textnorm import EMAIL_RE

# Paths relative to the validate root (data/_local/ is local-only and git-ignored, D64).
QUEUE_REL = Path("data") / "_local" / "people" / "review_queue.csv"
PEOPLE_REL = Path("data") / "people"
TABLES = ("people", "person_aliases", "person_xref", "affiliation_observations")
KIND_OF_CORPUS = {"eo": "publication", "pk": "publication", "ofc2026": "conference"}
GRADE_OF_KIND = {"publication": "A", "conference": "B"}
RULE_BASES = {"exact_name_shared_org", "compatible_name_shared_org_coauthor"}
ORIGIN_GRADE = {"eo_person_id": "A", "pk_name_key": "A", "ofc_name": "B"}
LINKEDIN_RE = re.compile(r"linked\s*-?\s*in|lnkd\.in", re.IGNORECASE)
MOVE_RE = re.compile(
    r"\b(?:former(?:ly)?|previously|ex-[a-z]+|joined|left|moved\s+to|now\s+(?:at|with)|background|alumn(?:us|a|i|ae))\b",
    re.IGNORECASE,
)
ROLE_RE = re.compile(
    r"\b(?:co-?founder|founder|ceo|cto|coo|cfo|vp|president|chairman|director|professor|engineer|researcher|"
    r"architect|manager|fellow|scientist|chief|head|lead|gm|executive|speaker|student|postdoc)s?\b",
    re.IGNORECASE,
)
SESSION_RE = re.compile(r"\bsession \S+ (\d{4}-\d{2}-\d{2})\b")
# Notes-type cells (curated free text): status / move wording is a career claim there (D97). Not applied to printed
# paper text (printed_org, unit), where present-address rows legitimately print "present address" (D70).
NOTE_CELLS = {("people", "disambiguator"), ("people", "notes"), ("person_aliases", "notes"), ("person_xref", "notes")}
NOTE_MOVE_RE = re.compile(
    r"\b(?:currently|presently|transferred|hired|departed|present\s+address)\b",
    re.IGNORECASE,
)
PHONE_RE = re.compile(
    r"(?:\b(?:tel|phone|fax|mobile)\b\.?\s*:?\s*\+?\d[\d\s().-]{6,}\d)|(?:\+\d{1,3}[\s.-]?\(?\d{1,4}\)?(?:[\s.-]?\d{2,4}){2,4})",
    re.IGNORECASE,
)


def split_sources(notes: str) -> list[str]:
    return [x for x in notes.removeprefix("lin sources: ").split(";") if x]


def rules(
    t: dict[str, list[dict[str, str]]], full: dict[str, list[dict[str, str]]], rep: Any, root: Path | None = None
) -> None:
    missing = [k for k in TABLES if not full.get(k)]
    if missing:
        rep.err(f"people tables empty or unreadable: {missing} (rules_people checks not run)")
        return
    people = {r["person_id"]: r for r in full["people"]}
    src = {r["source_id"]: r for r in full["sources"]}
    today = dt.date.today().isoformat()
    base = ROOT if root is None else root
    people_dir, review_queue = base / PEOPLE_REL, base / QUEUE_REL

    if people_dir.exists():
        want = {f"{k}.csv" for k in TABLES}
        for f in sorted(people_dir.iterdir()):
            if f.name not in want and not f.name.startswith("."):
                rep.err(f"data/people/{f.name}: unknown file (only {sorted(want)}; local layers go to data/_local/)")

    for name in TABLES:
        for i, r in enumerate(full[name], start=2):
            for c, v in r.items():
                if not v:
                    continue
                if EMAIL_RE.search(v) or SPELLED_EMAIL_RE.search(v):
                    rep.err(f"{name} line {i}: {c} contains an e-mail address (p5)")
                if PHONE_RE.search(v):
                    rep.err(f"{name} line {i}: {c} contains a phone number (p5)")
                if LINKEDIN_RE.search(v):
                    rep.err(f"{name} line {i}: {c} mentions LinkedIn (p5: no LinkedIn-derived rows)")
                if (name, c) in NOTE_CELLS:
                    m2 = NOTE_MOVE_RE.search(v)
                    if m2:
                        rep.err(f"{name} line {i}: {c} has status wording {m2.group(0)!r} (D97: career claim)")
                printed = name == "affiliation_observations" and c in ("printed_org", "unit")
                m = None if printed and r.get("aff_role") == "present_address" else MOVE_RE.search(v)
                if m:
                    rep.err(
                        f"{name} line {i}: {c} has move wording {m.group(0)!r} (p1/p7: career claims are LIN claims)"
                    )
    for i, r in enumerate(full["people"], start=2):
        for c in ("disambiguator", "notes"):
            m = ROLE_RE.search(r[c])
            if m:
                rep.err(f"people line {i}: {c} has role wording {m.group(0)!r} (p7, D93)")

    xref_by: dict[str, list[dict[str, str]]] = defaultdict(list)
    for x in full["person_xref"]:
        xref_by[x["person_id"]].append(x)
    for x in t["person_xref"]:
        pid, scheme, basis, grade = x["person_id"], x["scheme"], x["basis"], x["grade"]
        tag = f"person_xref {pid} {scheme}={x['value']}"
        if scheme == "lin_id" and x["value"] != pid:
            rep.err(f"{tag}: LIN ids are reused verbatim as person_id (D65)")
        if scheme == "lin_id":
            notes = x["notes"]
            ids = split_sources(notes)
            if not notes.startswith("lin sources: ") or not ids:
                rep.err(f"{tag}: lin_id xref needs notes 'lin sources: <source_id>;...' (D94)")
            else:
                gs = sorted(src[k]["evidence_grade"] for k in ids if k in src and src[k]["evidence_grade"])
                for k in ids:
                    if k not in src:
                        rep.err(f"{tag}: LIN source {k} not in sources.csv")
                best = gs[0] if gs else "X"
                if basis == "origin" and grade != best:
                    rep.err(f"{tag}: origin lin_id is the best grade of its LIN sources, {best}, not {grade} (D66)")
        if scheme == "orcid":
            if grade != "A":
                rep.err(f"{tag}: an ORCID xref is grade A, not {grade}")
            if basis not in ("orcid", "manual"):
                rep.err(f"{tag}: orcid xref needs basis orcid or manual")
            if people.get(pid, {}).get("orcid") != x["value"]:
                rep.err(f"{tag}: differs from people.orcid {people.get(pid, {}).get('orcid')!r}")
        elif basis == "orcid" and grade != "A":
            rep.err(f"{tag}: basis orcid is grade A")
        if basis == "manual" and not x["reviewed_on"]:
            rep.err(f"{tag}: basis manual needs reviewed_on")
        if basis in RULE_BASES and grade != "X":
            rep.err(f"{tag}: rule-based merge {basis} is an inference, grade X (D66)")
        if basis == "origin":
            og = ORIGIN_GRADE.get(scheme)
            if scheme == "orcid":
                rep.err(f"{tag}: an ORCID is never a person's origin record (ORCID is not the key, D65)")
            elif og and grade != og:
                rep.err(f"{tag}: origin {scheme} is grade {og}, not {grade}")
    for pid, p in people.items():
        if p["orcid"] and not any(x["scheme"] == "orcid" and x["value"] == p["orcid"] for x in xref_by[pid]):
            rep.err(f"people {pid}: orcid {p['orcid']} without an orcid xref")
        if p["orcid"] and pid.removeprefix("person_").replace("_", "-") == p["orcid"].lower():
            rep.err(f"people {pid}: ORCID used as the key (D65)")
    owners: dict[str, set[str]] = defaultdict(set)
    for pid, p in people.items():
        if p["orcid"]:
            owners[p["orcid"]].add(pid)
    for x in full["person_xref"]:
        if x["scheme"] == "orcid":
            owners[x["value"]].add(x["person_id"])
    for o, pids in sorted(owners.items()):
        if len(pids) > 1:
            rep.err(f"ORCID {o} held by {len(pids)} persons {sorted(pids)} (one iD, one person)")
    for pid in people:
        if not xref_by.get(pid):
            rep.warn(f"people {pid}: no person_xref row (person kept without records)")

    # D94: person visibility; research_status validated only for LIN people.
    obs_by: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in full["affiliation_observations"]:
        obs_by[r["person_id"]].append(r)
    for r in t["people"]:
        pid = r["person_id"]
        lin = [x for x in xref_by[pid] if x["scheme"] == "lin_id"]
        if r["research_status"] == "validated" and not lin:
            rep.err(f"people {pid}: research_status validated is a LIN status; this person has no lin_id xref")
        lin_ab = any(x["grade"] in ("A", "B") for x in lin)
        c_only = bool(lin) and not lin_ab
        n_pub = sum(o["visibility"] == "public" for o in obs_by[pid])
        if r["visibility"] == "public" and (c_only or not (n_pub or lin_ab)):
            rep.err(
                f"people {pid}: public needs >= 1 public observation or a LIN A/B source, and no C-only LIN "
                "identity (D94)"
            )
        if c_only and n_pub:
            rep.err(f"people {pid}: LIN identity rests on grade C/X sources only; its observations must be review")
        if r["visibility"] == "review" and n_pub:
            rep.err(f"people {pid}: review person with {n_pub} public observations (D94)")

    for r in t["person_aliases"]:
        if r["alias"] == people.get(r["person_id"], {}).get("display_name"):
            rep.warn(f"person_aliases {r['person_id']}: alias {r['alias']!r} equals the display name")

    names_of: dict[str, set[str]] = defaultdict(set)
    for r in full["person_aliases"]:
        names_of[r["person_id"]].add(r["alias"])
    for pid, p in people.items():
        names_of[pid].add(p["display_name"])
    xw: dict[tuple[str, str], set[str]] = defaultdict(set)
    for r in full.get("org_crosswalk", []):
        xw[(r["corpus"], clean_text(r["printed"]))] |= {x.strip() for x in r["org_ids"].split(";") if x.strip()}
    session = {}
    for r in full["sources"]:
        m = SESSION_RE.search(r["notes"]) if r["corpus"] == "ofc2026" else None
        if m:
            session[r["source_id"]] = m.group(1)
            if r["same_as"]:
                session[r["same_as"]] = m.group(1)  # EO row of an OFC 2026 paper: the session date (D67)

    for r in t["affiliation_observations"]:
        oid, sid = r["obs_id"], r["source_id"]
        if r["printed_name"] not in names_of[r["person_id"]]:
            rep.err(
                f"affiliation_observations {oid}: printed_name {r['printed_name']!r} is not a name of "
                f"{r['person_id']} (display_name / aliases)"
            )
        if not oid.startswith(sid + "#a"):
            rep.err(f"affiliation_observations {oid}: obs_id does not start with its source_id {sid}")
        s = src.get(sid)
        if s is None:
            continue  # orphan, reported by the fk check
        if s["same_as"]:
            rep.err(f"affiliation_observations {oid}: cites duplicate {sid} (canonical {s['same_as']}, p6)")
        want_kind = KIND_OF_CORPUS.get(s["corpus"])
        if want_kind is None:
            rep.err(f"affiliation_observations {oid}: source corpus {s['corpus']} is not eo, pk or ofc2026")
        elif r["kind"] != want_kind:
            rep.err(f"affiliation_observations {oid}: {s['corpus']} source gives kind {want_kind}, not {r['kind']}")
        if GRADE_OF_KIND.get(r["kind"]) != r["evidence_grade"]:
            rep.err(
                f"affiliation_observations {oid}: kind {r['kind']} is grade {GRADE_OF_KIND.get(r['kind'])}, "
                f"not {r['evidence_grade']} (p4)"
            )
        corpus = s["corpus"]
        want_on = {
            "eo": s["published_on"] or session.get(sid, "") or s["year"],
            "pk": s["year"],
            "ofc2026": session.get(sid, ""),
        }.get(corpus, "")
        if want_on and r["active_on"] != want_on:
            rep.err(f"affiliation_observations {oid}: active_on {r['active_on']} != source date {want_on} (D67)")
        key = (corpus, clean_text(r["printed_org"]))
        if key in xw:
            ok_ids = xw[key]
            if (r["org_id"] or "") not in ok_ids and not (r["org_id"] == "" and not ok_ids):
                rep.err(
                    f"affiliation_observations {oid}: org_id {r['org_id']!r} contradicts the crosswalk "
                    f"{sorted(ok_ids)} for {r['printed_org']!r}"
                )
        elif r["org_id"] and r["printed_org"]:
            rep.err(
                f"affiliation_observations {oid}: org_id {r['org_id']} but {r['printed_org']!r} not in the crosswalk"
            )
        years = {s["year"], s["published_on"][:4]} - {""}
        if years and r["active_on"][:4] not in years:
            rep.err(
                f"affiliation_observations {oid}: active_on {r['active_on']} not in the source year {sorted(years)}"
            )
        if r["active_on"] > today:
            rep.err(f"affiliation_observations {oid}: active_on {r['active_on']} is in the future")
        if r["visibility"] == "public" and r["evidence_grade"] not in ("A", "B"):
            rep.err(f"affiliation_observations {oid}: public visibility needs grade A/B (D70)")
        if r["kind"] == "conference" and r["aff_role"] != "primary":
            rep.err(f"affiliation_observations {oid}: OFC metadata has one affiliation per author (aff_role primary)")
        if r["org_id"] == "" and r["printed_org"] and r["visibility"] == "public" and s["corpus"] != "ofc2026":
            rep.warn(f"affiliation_observations {oid}: printed org {r['printed_org']!r} not mapped to the registry")

    if not review_queue.exists():
        rep.warn(f"{review_queue.name} (local review queue) absent: D64 visibility of queued persons not checked")
        return
    queue = read_csv(review_queue)
    n_obs = {pid: len(rows) for pid, rows in obs_by.items()}
    demoted: set[str] = set()
    pairs: set[frozenset[str]] = set()
    for q in queue:
        a, b = q["person_id_a"], q["person_id_b"]
        pairs.add(frozenset((a, b)))
        for k in (a, b):
            if k not in people:
                rep.warn(f"review queue: {k} not in people.csv (stale queue; rebuild)")
        if n_obs.get(b, 0):
            demoted.add(a)
        if n_obs.get(a, 0):
            demoted.add(b)
    for r in full["affiliation_observations"]:
        if r["person_id"] in demoted and r["visibility"] == "public":
            rep.err(
                f"affiliation_observations {r['obs_id']}: person {r['person_id']} is in the review queue with a "
                "partner that has observations, visibility must be review (D64)"
            )
    eo_split: dict[str, set[str]] = defaultdict(set)
    for x in full["person_xref"]:
        if x["scheme"] == "eo_person_id":
            eo_split[x["value"]].add(x["person_id"])
    for v, pids in sorted(eo_split.items()):
        ps = sorted(pids)
        for i, a in enumerate(ps):
            for b in ps[i + 1 :]:
                if frozenset((a, b)) not in pairs:
                    rep.err(f"EO person {v} split into {a} and {b} but the pair is not in the review queue (D64)")
