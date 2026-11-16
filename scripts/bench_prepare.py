"""Queue the benchmark-citation list for the existing lit pipeline (DevLog-019 B8, pattern of hist_prepare.py D964).

Input: data/_staging/literature/bench_cache_list.csv (rows with above_cut = True, written by scripts/bench_curate.py).
Each row gets a `paper_id` (`firstauthorYEAR[a-z]`, unique against references/, cache_list.csv, retrieval_queue.csv
and every registry native id) and is appended, once, to:
  - data/_staging/literature/cache_list.csv (selection_reason = benchmark_cite, rationale = citing count + topics);
  - data/_staging/literature/retrieval_queue.csv, days --first-day, --first-day + 1, ... in rank order, with per-day
    caps per route (arxiv 40, oa_publisher 20, ieee_browser / ieee_search 30 = one IEEE session, optica_browser 24 in
    sessions of <= 12, publisher_browser 10); `manual` rows go to day --manual-day (owner download list only).
Routes: arXiv id -> arxiv; Optica OA journals (10.1364/oe|optica|ome) -> optica_browser; other 10.1364 -> manual
(Optics Letters / Photonics Research / conference papers are not fetched, owner rule); 10.1109 / 10.23919 ->
ieee_browser; 10.1049 -> ieee_search; open copy at Nature / Wiley / AIP / De Gruyter / ACS / IOP -> publisher_browser;
Science / PNAS -> manual; other open copy -> oa_publisher; everything else -> manual.
Both CSVs are zip-backed-up to cache/literature/backup/ before the write. Idempotent: rows whose uid is already in
cache_list.csv are skipped.

Usage: uv run python scripts/bench_prepare.py [--first-day 201] [--manual-day 200] [--dry-run]
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
import unicodedata
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from photonics_atlas.litpool import norm_doi  # noqa: E402

LITS = ROOT / "data" / "_staging" / "literature"
BENCH_LIST = LITS / "bench_cache_list.csv"
CACHE_LIST = LITS / "cache_list.csv"
QUEUE = LITS / "retrieval_queue.csv"
SOURCES = ROOT / "data" / "registry" / "sources.csv"
BACKUP = ROOT / "cache" / "literature" / "backup"
OPTICA_OA = re.compile(r"^10\.1364/(oe|opex|optica|ome)\.")
PUBLISHER_HOSTS = ("nature.com", "wiley.com", "aip.org", "degruyterbrill.com", "degruyter.com", "acs.org", "iop.org")
DAY_CAP = {"arxiv": 40, "oa_publisher": 20, "ieee": 30, "optica_browser": 24, "publisher_browser": 10}
SESSION_CAP = {"ieee": 30, "optica_browser": 12, "publisher_browser": 10}


def read(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return list(r.fieldnames or []), [dict(x) for x in r]


def write(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    tmp = path.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)  # csv default CRLF, as the existing files
        w.writeheader()
        w.writerows(rows)
    tmp.replace(path)


def backup(paths: list[Path]) -> Path:
    BACKUP.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%SZ")
    out = BACKUP / f"bench_queue_{ts}.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in paths:
            z.write(p, p.relative_to(ROOT))
    return out


def surname(name: str) -> str:
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    toks = [t for t in re.split(r"[\s,]+", s) if len(re.sub(r"[^a-z]", "", t)) >= 2]  # skip initials ("Dai A")
    if not toks:
        return ""
    if "," in name:  # "Surname, G."
        return re.sub(r"[^a-z]", "", toks[0])
    return re.sub(r"[^a-z]", "", toks[-1])


def ref_surname(ref: str) -> str:
    """First-author surname from a printed reference: 'C. R. Doerr and ...', 'Doerr, C. R., ...', 'Doerr C R 2006'."""
    s = unicodedata.normalize("NFKD", ref).encode("ascii", "ignore").decode()
    m = re.match(r"\s*(?:[A-Z][a-z]?\.[\s-]*)+([A-Z][A-Za-z'\-]+)", s)  # initials first
    if m:
        return re.sub(r"[^a-z]", "", m.group(1).lower())
    m = re.match(r"\s*([A-Z][A-Za-z'\-]+)", s)  # surname first
    return re.sub(r"[^a-z]", "", m.group(1).lower()) if m else ""


def route_of(r: dict[str, str]) -> tuple[str, str]:
    doi = norm_doi(r["doi"])
    if r["arxiv_id"]:
        return "arxiv", f"https://arxiv.org/pdf/{r['arxiv_id']}"
    if OPTICA_OA.match(doi):
        return "optica_browser", f"https://doi.org/{doi}"
    if doi.startswith("10.1364/"):
        return "manual", f"https://doi.org/{doi}"
    if doi.startswith(("10.1109/", "10.23919/")):
        return "ieee_browser", f"https://doi.org/{doi}"
    if doi.startswith("10.1049/"):
        return "ieee_search", f"https://doi.org/{doi}"
    url = r["oa_url"]
    if url and r["tier"] == "1":
        host = re.sub(r"^https?://([^/]+).*$", r"\1", url).lower()
        if "arxiv.org" in host:
            m = re.search(r"arxiv\.org/(?:pdf|abs)/([0-9]{4}\.[0-9]{4,5})", url)
            if m:
                return "arxiv", f"https://arxiv.org/pdf/{m.group(1)}"
        if host.endswith(PUBLISHER_HOSTS):
            return "publisher_browser", f"https://doi.org/{doi}" if doi else url
        if host.endswith(("science.org", "pnas.org")):
            return "manual", f"https://doi.org/{doi}"
        return "oa_publisher", url
    return "manual", f"https://doi.org/{doi}" if doi else ""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--first-day", type=int, default=201)
    ap.add_argument("--manual-day", type=int, default=200)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    ts = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    log = open(ROOT / "logs" / f"bench_prepare_{ts}.log", "w")

    _, bench = read(BENCH_LIST)
    rows = [r for r in bench if r["above_cut"] == "True"]
    # printed reference of each work (local works.jsonl, not committed): author fallback for the paper_id
    ref_ex = {}
    for line in (ROOT / "cache" / "literature" / "bench" / "works.jsonl").read_text().splitlines():
        w = json.loads(line)
        ref_ex[w["work_id"]] = w.get("ref_example") or ""
    cl_fields, cl = read(CACHE_LIST)
    q_fields, q = read(QUEUE)
    _, src = read(SOURCES)
    taken = (
        {p.name for p in (ROOT / "references").iterdir()}
        | {x["paper_id"] for x in cl}
        | {x["paper_id"] for x in q}
        | {x["native_id"] for x in src}
    )
    have_uid = {x["uid"] for x in cl} | {norm_doi(x["doi"]) for x in cl if x["doi"]}
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
    for r in rows:
        uid = norm_doi(r["doi"]) or f"arxiv:{r['arxiv_id']}"
        if uid in have_uid:
            skipped += 1
            continue
        base = (surname(r["first_author"]) or ref_surname(ref_ex.get(r["work_id"], "")) or "anon") + str(
            r["year"] or ""
        )
        pid, k = base, 0
        while pid in taken:
            pid = base + "abcdefghijklmnopqrstuvwxyz"[k] if k < 26 else f"{base}z{k}"
            k += 1
        taken.add(pid)
        route, url = route_of(r)
        access = "oa" if route in ("arxiv", "oa_publisher", "optica_browser", "publisher_browser") else "paywalled"
        topics = r["topics"].replace("|", "; ")
        rationale = f"cited in {r['n_citing']} benchmark tables / plots ({topics})"[:160]
        add_cl.append(
            {f: "" for f in cl_fields}
            | {
                "rank": r["rank"], "primary_class": r["class"].split(".")[0], "subtype": r["class"],
                "classes": r["classes"], "uid": uid,
                "doi": norm_doi(r["doi"]), "arxiv_id": r["arxiv_id"], "paper_id": pid, "title": r["title"],
                "first_author": r["first_author"], "last_author": r["last_author"], "venue": r["venue"],
                "venue_type": "conference" if "proceedings" in r["type"] else "journal", "year": r["year"],
                "access": access, "oa_url": url if access == "oa" else "", "selection_reason": "benchmark_cite",
                "rationale": rationale,
            }
        )  # fmt: skip
        # day assignment
        cap_key = "ieee" if route.startswith("ieee") else route
        if route == "manual":
            day = a.manual_day
        else:
            day = a.first_day
            while per_day[day][cap_key] >= DAY_CAP[cap_key]:
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
                "day": str(day), "date": (date0 + dt.timedelta(days=max(0, day - a.first_day))).isoformat(),
                "route": route, "session": session, "paper_id": pid, "uid": uid, "doi": norm_doi(r["doi"]),
                "arxiv_id": r["arxiv_id"], "route_url": url, "access": access,
                "primary_class": r["class"].split(".")[0], "score": r["n_citing"], "title": r["title"],
            }
        )  # fmt: skip
    days = Counter(x["day"] for x in add_q)
    routes = Counter(x["route"] for x in add_q)
    msg = (
        f"rows above cut {len(rows)}, already in cache_list {skipped}, +{len(add_cl)} cache_list, +{len(add_q)} queue; "
        f"routes {dict(routes)}; days {dict(sorted(days.items(), key=lambda kv: int(kv[0])))}"
    )
    print(msg)
    print(msg, file=log)
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
