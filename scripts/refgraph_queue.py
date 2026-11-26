"""Queue the reference-graph list for the existing lit pipeline (DevLog-020 stage 3, pattern of bench_prepare.py).

Input: data/_staging/literature/refgraph_cache_list.csv (written by scripts/refgraph_prepare.py). Rows with status
`new` (errata / editorials left out), ranked by n_citing (descending, stable). Route and route_url as stage 2 set them.
Each row gets a `paper_id` (`firstauthorYEAR[a-z]`, unique against references/, cache_list.csv, retrieval_queue.csv
and every registry native id) and is appended, once, to:
  - data/_staging/literature/cache_list.csv (selection_reason = refgraph_cite, rationale = citing count + classes);
  - data/_staging/literature/retrieval_queue.csv, per-route first days and per-day caps (owner 2026-11-25):
    ieee_browser + ieee_search 30 from --ieee-day (not on --ieee-skip-days); optica_browser 30, arxiv 15, oa_publisher 5, publisher_browser 10
    from --oa-day; manual rows on --manual-day (owner download list only).
Both CSVs are zip-backed-up to cache/literature/backup/ before the write. Idempotent: rows whose uid is already in
cache_list.csv are skipped.

Usage: uv run python scripts/refgraph_queue.py [--ieee-day 212] [--oa-day 213] [--manual-day 200] [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from bench_prepare import CACHE_LIST, QUEUE, SOURCES, backup, read, ref_surname, surname, write  # noqa: E402

from photonics_atlas.litpool import norm_doi  # noqa: E402

REFGRAPH_LIST = ROOT / "data" / "_staging" / "literature" / "refgraph_cache_list.csv"
DAY_CAP = {"arxiv": 15, "oa_publisher": 5, "ieee": 30, "optica_browser": 30, "publisher_browser": 10}
SESSION_CAP = {"ieee": 30, "optica_browser": 12, "publisher_browser": 10}
SKIP_TYPES = {"erratum", "editorial"}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ieee-day", type=int, default=212)
    ap.add_argument("--oa-day", type=int, default=213)
    ap.add_argument("--manual-day", type=int, default=200)
    ap.add_argument("--ieee-skip-days", default="213,214,215", help="days without an IEEE session (owner away)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    ieee_skip = {int(x) for x in a.ieee_skip_days.split(",") if x}
    ts = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    log = open(ROOT / "logs" / f"refgraph_queue_{ts}.log", "w")

    _, rg = read(REFGRAPH_LIST)
    rows = [r for r in rg if r["status"] == "new" and r["type"] not in SKIP_TYPES]
    n_type_skip = sum(1 for r in rg if r["status"] == "new" and r["type"] in SKIP_TYPES)
    rows.sort(key=lambda r: -int(r["n_citing"] or 0))
    cl_fields, cl = read(CACHE_LIST)
    q_fields, q = read(QUEUE)
    _, src = read(SOURCES)
    taken = (
        {p.name for p in (ROOT / "references").iterdir()}
        | {x["paper_id"] for x in cl}
        | {x["paper_id"] for x in q}
        | {x["native_id"] for x in src}
    )
    have_uid = (
        {x["uid"] for x in cl}
        | {norm_doi(x["doi"]) for x in cl if x["doi"]}
        | {norm_doi(x["doi"]) for x in q if x["doi"]}
        | {f"arxiv:{x['arxiv_id']}" for x in q if x["arxiv_id"]}
    )
    sessions = {
        "ieee": max((int(x["session"]) for x in q if x["route"].startswith("ieee") and x["session"]), default=0),
        "optica_browser": max(
            (int(x["session"]) for x in q if x["route"] == "optica_browser" and x["session"]), default=0
        ),
        "publisher_browser": max(
            (int(x["session"]) for x in q if x["route"] == "publisher_browser" and x["session"]), default=0
        ),
    }
    date0 = dt.date.today()
    per_day: dict[int, Counter[str]] = defaultdict(Counter)
    sess_fill: dict[tuple[int, str], tuple[int, int]] = {}
    add_cl, add_q = [], []
    skipped = 0
    for rank, r in enumerate(rows, 1):
        doi = norm_doi(r["doi"])
        uid = doi or f"arxiv:{r['arxiv_id']}"
        if uid in have_uid or uid == "arxiv:":
            skipped += 1
            continue
        have_uid.add(uid)
        base = (surname(r["first_author"]) or ref_surname(r["example"]) or "anon") + str(r["year"] or "")
        pid, k = base, 0
        while pid in taken:
            pid = base + "abcdefghijklmnopqrstuvwxyz"[k] if k < 26 else f"{base}z{k}"
            k += 1
        taken.add(pid)
        route, url = r["route"], r["route_url"]
        access = "oa" if route in ("arxiv", "oa_publisher", "optica_browser", "publisher_browser") else "paywalled"
        cls = r["class_hint"] if r["class_hint"] not in ("", "none") else ""
        rationale = f"cited by {r['n_citing']} corpus papers (reference graph; {r['citing_classes']})"[:160]
        add_cl.append(
            {f: "" for f in cl_fields}
            | {
                "rank": str(rank), "primary_class": cls, "subtype": "", "classes": r["citing_classes"], "uid": uid,
                "doi": doi, "arxiv_id": r["arxiv_id"], "paper_id": pid, "title": r["title"],
                "first_author": r["first_author"], "last_author": r["last_author"], "venue": r["venue"],
                "venue_type": "conference" if "conference" in r["type"] else "journal", "year": r["year"],
                "access": access, "oa_url": url if access == "oa" else "", "selection_reason": "refgraph_cite",
                "rationale": rationale,
            }
        )  # fmt: skip
        cap_key = "ieee" if route.startswith("ieee") else route
        if route == "manual":
            day = a.manual_day
        else:
            day = a.ieee_day if cap_key == "ieee" else a.oa_day
            while per_day[day][cap_key] >= DAY_CAP[cap_key] or (cap_key == "ieee" and day in ieee_skip):
                day += 1
            per_day[day][cap_key] += 1
        session = ""
        if cap_key in SESSION_CAP:
            cur = sess_fill.get((day, cap_key))
            if cur is None or cur[1] >= SESSION_CAP[cap_key]:
                sessions[cap_key] += 1
                cur = (sessions[cap_key], 0)
            sess_fill[(day, cap_key)] = (cur[0], cur[1] + 1)
            session = str(cur[0])
        add_q.append(
            {f: "" for f in q_fields}
            | {
                "day": str(day),
                "date": (date0 + dt.timedelta(days=max(0, day - a.ieee_day))).isoformat() if route != "manual"
                else date0.isoformat(),
                "route": route, "session": session, "paper_id": pid, "uid": uid, "doi": doi,
                "arxiv_id": r["arxiv_id"], "route_url": url, "access": access, "primary_class": cls,
                "score": r["n_citing"], "title": r["title"],
            }
        )  # fmt: skip
    days = Counter(x["day"] for x in add_q)
    routes = Counter(x["route"] for x in add_q)
    msg = (
        f"rows new {len(rows)} (+{n_type_skip} errata / editorials left out), already queued {skipped}, "
        f"+{len(add_cl)} cache_list, +{len(add_q)} queue; routes {dict(routes)}; "
        f"days {dict(sorted(days.items(), key=lambda kv: int(kv[0])))}"
    )
    print(msg)
    print(msg, file=log)
    for d in sorted(days, key=int)[:8]:
        print(d, dict(Counter(x["route"] for x in add_q if x["day"] == d)))
    for d in sorted(days, key=int):
        print(d, dict(Counter(x["route"] for x in add_q if x["day"] == d)), file=log)
    if a.dry_run or not add_cl:
        return
    print(f"backup {backup([CACHE_LIST, QUEUE]).relative_to(ROOT)}", file=log)
    write(CACHE_LIST, cl_fields, cl + add_cl)
    write(QUEUE, q_fields, q + add_q)
    log.close()


if __name__ == "__main__":
    main()
