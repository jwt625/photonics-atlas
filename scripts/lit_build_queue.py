"""Build the S7 retrieval queue and the 10-day schedule for the 1000 selected papers (DevLog-006 S7, D141-D143).

Steps:
  1. arXiv copies for selected rows without arxiv_id (the journal DOI stays the identity; the arXiv copy is only the
     retrieval route):
       given  arxiv_id in cache_list, or an arxiv.org oa_url there;
       doi    local arXiv pool (cache/literature/pool/arxiv_*.jsonl) record whose doi / arxiv_dois equals the DOI;
       title  local pool record with normalized-title similarity (difflib) >= 0.93 and a shared first- or
              last-author surname;
       api    one arXiv API query per still-unmatched row (`ti:"<title words>"`, max_results 5) through
              photonics_atlas.litfetch (>= 3.5 s spacing, breaker on 403/429/503); same acceptance rule. Results are
              cached per paper in cache/literature/arxiv_match/api/<paper_id>.json (resumable, skip-existing); the API
              part stops at the first BlockedError / HTTP / network error and the build continues with what is cached.
  2. IEEE twins (--ieee-twins) of paywalled non-IEEE rows (Optica first, then other publishers): one Crossref query
     each (query.bibliographic=<title>, filter prefix 10.1109 / 10.23919, rows 5) through litfetch; accepted with title
     similarity >= 0.93, a shared surname and |year difference| <= 1; cached in cache/literature/arxiv_match/ieee_twin/.
  3. Route per paper (preference order): arxiv (arXiv copy) | ieee_browser via the IEEE twin (paywalled rows; route_url
     https://doi.org/<ieee_doi>, the original DOI stays the identity) | ieee_search (paywalled Optica conference rows:
     Xplore title search in the IEEE sessions, runtime fallback optica_browser) | optica_browser (10.1364) |
     ieee_browser (10.1109, 10.23919) | manual (AIP OA rows: 403 to browsers too) | publisher_browser (OA rows whose oa_url host is Nature / Wiley / AIP / De Gruyter / ACS / IOP,
     or doi.org with one of their DOI prefixes: these sites block non-browser clients) | oa_publisher (other OA with
     oa_url: repositories, MDPI, other publishers) | manual (remaining paywalled).
  4. Schedule: N days from --start (default 2026-10-22, 10 days). Every route is spread evenly over the days: inside a
     route the rows are taken class by class (each class ordered curator picks first, then score, then rank) and dealt
     to consecutive days with one running counter, so each (route, class) and each route differ by <= 1 between days.
     Browser rows are split into sessions per day and site (ieee <= 30 incl. ieee_search, optica <= 20, publisher
     <= 20; global integer session numbers per site). Optica is capped at --optica-day-cap per day (default 45); a
     tail beyond cap x days would go to extra days after day N.
  --delta (D232): after an increment selection, keep every previous queue row verbatim and give each incoming paper
     the day slot (and, same site, the session) of a displaced paper of its primary class; displaced rows on days
     <= --freeze-days abort the run.
Outputs: data/_staging/literature/retrieval_queue.csv, data/_staging/literature/retrieval_schedule.md,
         cache/literature/arxiv_match/local_matches.jsonl.

Usage: uv run python scripts/lit_build_queue.py [--dry-run] [--api] [--max-queries N] [--max-minutes M] [--ieee-twins]
         [--max-ieee-queries N] [--optica-day-cap 45] [--start 2026-10-22] [--days 10] [--delta [--freeze-days 2]]
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import difflib
import json
import math
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from photonics_atlas import litfetch
from photonics_atlas.litpool import POOL, norm_doi
from photonics_atlas.paths import CACHE, STAGING
from photonics_atlas.runlog import RunLog
from photonics_atlas.textnorm import ascii_fold

LIT = STAGING / "literature"
CACHE_LIST = LIT / "cache_list.csv"
QUEUE = LIT / "retrieval_queue.csv"
SCHEDULE = LIT / "retrieval_schedule.md"
MATCH_DIR = CACHE / "literature" / "arxiv_match"
API_DIR = MATCH_DIR / "api"
API = "http://export.arxiv.org/api/query"
IEEE_DIR = MATCH_DIR / "ieee_twin"
CROSSREF = "https://api.crossref.org/works"

TITLE_MIN = 0.93
ROUTES = ("arxiv", "oa_publisher", "publisher_browser", "optica_browser", "ieee_browser", "ieee_search", "manual")
OPTICA_PREFIXES = ("10.1364",)
IEEE_PREFIXES = ("10.1109", "10.23919")
# Publishers whose sites block non-browser clients (R2 pilot 2026-10-22: Nature JS challenge, Wiley 403, AIP 403,
# De Gruyter AWS WAF 202; ACS and IOP treated the same): their OA rows go to a headed browser session.
# AIP also returns 403 to the browser: its OA rows go to manual (coordinator 2026-10-22).
BROWSER_PUBLISHER_PREFIXES = ("10.1038", "10.1002", "10.1111", "10.1515", "10.1021", "10.1088")
BROWSER_PUBLISHER_HOSTS = (
    "nature.com",
    "wiley.com",
    "degruyter.com",
    "degruyterbrill.com",
    "acs.org",
    "iop.org",
)
MANUAL_PREFIXES = ("10.1063",)
MANUAL_HOSTS = ("aip.org", "scitation.org")
# Paywalled Optica conference papers (OFC, CLEO, ACP, IPR, ...) are often on IEEE Xplore under the Optica DOI only
# (10.1364/ACPC.2021.T4A.130 = Xplore 9738431): route ieee_search, an Xplore title search inside the IEEE sessions;
# the fetcher falls back to optica_browser at runtime when Xplore has no copy.
OPTICA_CONF_DOI = re.compile(
    r"^10\.1364/(ofc|cleo|cleo_at|cleo_si|cleo_qels|acpc|acp|iprsn|ipr|noma|sppcom|fio)[._]", re.I
)
SESSION_CAP = {"ieee": 30, "optica": 20, "publisher": 20}
DAY_CAP = {"optica_browser": 45}
SITE = {"optica_browser": "optica", "ieee_browser": "ieee", "ieee_search": "ieee", "publisher_browser": "publisher"}
SITES = ("optica", "ieee", "publisher")
COLUMNS = [
    "day",
    "date",
    "route",
    "session",
    "paper_id",
    "uid",
    "doi",
    "arxiv_id",
    "arxiv_match",
    "arxiv_match_score",
    "ieee_doi",
    "ieee_match_score",
    "route_url",
    "access",
    "primary_class",
    "score",
    "title",
    "status",
]
NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
_TEX = re.compile(r"[$_^{}\\]")
_NONALNUM = re.compile(r"[^a-z0-9]+")
_VER = re.compile(r"v\d+$")
_ARXIV_URL = re.compile(r"arxiv\.org/(?:abs|pdf)/([^?#\s]+?)(?:\.pdf)?$", re.I)
_WS = re.compile(r"\s+")


# ---------------------------------------------------------------------------------------------- matching primitives


def fold(s: str) -> str:
    """ascii_fold after mapping non-ASCII punctuation, symbols and spaces (U+2010 hyphen, en dash, NBSP) to a space, so
    they separate words instead of vanishing."""
    return ascii_fold("".join(" " if ord(c) > 127 and unicodedata.category(c)[0] in "PSZ" else c for c in s))


def norm_title(title: str) -> str:
    """ASCII-fold, drop TeX markup characters ($ _ ^ { } \\) without a space (Gd$_2$O$_3$ -> gd2o3), lowercase,
    punctuation -> single space."""
    s = _TEX.sub("", fold(title or "")).lower()
    return _NONALNUM.sub(" ", s).strip()


def title_sim(a: str, b: str) -> float:
    na, nb = norm_title(a), norm_title(b)
    if not na or not nb:
        return 0.0
    return difflib.SequenceMatcher(None, na, nb).ratio()


def name_tokens(name: str) -> list[str]:
    return [t for t in _NONALNUM.sub(" ", fold(name or "").lower()).split() if len(t) >= 2]


def surnames_share(row_names: list[str], cand_names: list[str]) -> bool:
    """True when the first- or last-author surname of the row (last token; first token too, for reversed name order)
    equals the surname (last token) of any candidate author, or the row's last token equals a candidate's first token."""
    row_last = {t[-1] for t in map(name_tokens, row_names) if t}
    row_first = {t[0] for t in map(name_tokens, row_names) if t}
    cand_last = {t[-1] for t in map(name_tokens, cand_names) if t}
    cand_first = {t[0] for t in map(name_tokens, cand_names) if t}
    return bool((row_last | row_first) & cand_last or row_last & cand_first)


def arxiv_id_from_url(url: str) -> str:
    """https://arxiv.org/pdf/2101.00001v2 or http://arxiv.org/abs/2101.00001 -> 2101.00001 ('' if not arXiv)."""
    m = _ARXIV_URL.search((url or "").strip())
    return _VER.sub("", m.group(1)) if m else ""


@dataclass
class Match:
    arxiv_id: str
    kind: str  # given | doi | title | api
    score: float | None  # title similarity (None for given)
    arxiv_title: str = ""


@dataclass
class PoolRec:
    arxiv_id: str
    dois: set[str]
    title: str
    ntitle: str
    authors: list[str]


class PoolIndex:
    """arXiv pool records with a DOI map and a title-token inverted index for candidate generation."""

    def __init__(self, recs: list[PoolRec]) -> None:
        self.recs = recs
        self.by_doi: dict[str, list[int]] = defaultdict(list)
        self.by_tok: dict[str, list[int]] = defaultdict(list)
        for i, r in enumerate(recs):
            for d in r.dois:
                self.by_doi[d].append(i)
            for t in set(r.ntitle.split()):
                self.by_tok[t].append(i)

    def candidates(self, ntitle: str, min_frac: float = 0.6, limit: int = 25) -> list[int]:
        toks = set(ntitle.split())
        if not toks:
            return []
        hits: Counter[int] = Counter()
        for t in toks:
            hits.update(self.by_tok.get(t, ()))
        need = math.ceil(min_frac * len(toks))
        return [i for i, n in hits.most_common(limit) if n >= need]


def load_pool(pool_dir: Path = POOL) -> list[PoolRec]:
    seen: dict[str, PoolRec] = {}
    for p in sorted(pool_dir.glob("arxiv_*.jsonl")):
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            aid = r.get("arxiv_id") or ""
            if not aid or aid in seen:
                continue
            dois = {norm_doi(d) for d in [r.get("doi") or "", *(r.get("arxiv_dois") or [])] if d}
            authors = list(r.get("authors") or [])
            if r.get("last_author") and r["last_author"] not in authors:
                authors.append(r["last_author"])
            seen[aid] = PoolRec(aid, dois, r.get("title") or "", norm_title(r.get("title") or ""), authors)
    return list(seen.values())


def row_names(row: dict[str, str]) -> list[str]:
    return [n for n in (row.get("first_author", ""), row.get("last_author", "")) if n]


def given_match(row: dict[str, str]) -> Match | None:
    if row.get("arxiv_id"):
        return Match(row["arxiv_id"], "given", None)
    aid = arxiv_id_from_url(row.get("oa_url", ""))
    return Match(aid, "given", None) if aid else None


def local_match(row: dict[str, str], idx: PoolIndex) -> Match | None:
    """DOI equality first, then title similarity >= TITLE_MIN with a shared surname (best similarity wins)."""
    doi = norm_doi(row.get("doi"))
    if doi and doi in idx.by_doi:
        best = max(idx.by_doi[doi], key=lambda i: title_sim(row["title"], idx.recs[i].title))
        r = idx.recs[best]
        return Match(r.arxiv_id, "doi", round(title_sim(row["title"], r.title), 4), r.title)
    nt = norm_title(row.get("title", ""))
    names = row_names(row)
    found: Match | None = None
    for i in idx.candidates(nt):
        r = idx.recs[i]
        s = difflib.SequenceMatcher(None, nt, r.ntitle).ratio()
        if s >= TITLE_MIN and surnames_share(names, r.authors) and (found is None or s > (found.score or 0.0)):
            found = Match(r.arxiv_id, "title", round(s, 4), r.title)
    return found


# --------------------------------------------------------------------------------------------------------- arXiv API


def query_title(title: str) -> str:
    """Title words for ti:"..." (TeX markup and punctuation stripped, ASCII-folded, original case)."""
    s = _TEX.sub("", fold(title or ""))
    return _WS.sub(" ", re.sub(r"[^A-Za-z0-9]+", " ", s)).strip()


def _text(el: ET.Element | None) -> str:
    return _WS.sub(" ", el.text or "").strip() if el is not None and el.text else ""


def parse_hits(xml: bytes) -> list[dict[str, Any]]:
    """Atom feed -> [{arxiv_id, title, authors, doi, primary, published}]. Raises ValueError on an API error entry."""
    root = ET.fromstring(xml)
    out: list[dict[str, Any]] = []
    for e in root.findall("a:entry", NS):
        url = _text(e.find("a:id", NS))
        if "/api/errors" in url:
            raise ValueError(f"arXiv API error: {_text(e.find('a:summary', NS))}")
        prim = e.find("arxiv:primary_category", NS)
        out.append(
            {
                "arxiv_id": _VER.sub("", url.split("/abs/", 1)[-1].strip()),
                "title": _text(e.find("a:title", NS)),
                "authors": [_text(a.find("a:name", NS)) for a in e.findall("a:author", NS)],
                "doi": norm_doi(_text(e.find("arxiv:doi", NS))),
                "primary": prim.get("term", "") if prim is not None else "",
                "published": _text(e.find("a:published", NS))[:10],
            }
        )
    return out


def pick_api_hit(row: dict[str, str], hits: list[dict[str, Any]]) -> Match | None:
    names = row_names(row)
    best: Match | None = None
    for h in hits:
        s = title_sim(row["title"], h["title"])
        if s >= TITLE_MIN and surnames_share(names, h["authors"]) and (best is None or s > (best.score or 0.0)):
            best = Match(h["arxiv_id"], "api", round(s, 4), h["title"])
    return best


def api_cache_path(paper_id: str) -> Path:
    return API_DIR / f"{paper_id}.json"


def api_query(row: dict[str, str]) -> dict[str, Any]:
    q = f'ti:"{query_title(row["title"])}"'
    body = litfetch.get(API, {"search_query": q, "start": 0, "max_results": 5})
    hits = parse_hits(body)
    m = pick_api_hit(row, hits)
    return {
        "paper_id": row["paper_id"],
        "doi": row["doi"],
        "query": q,
        "queried_at": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
        "hits": [{**h, "title_sim": round(title_sim(row["title"], h["title"]), 4)} for h in hits],
        "match": None if m is None else {"arxiv_id": m.arxiv_id, "score": m.score, "arxiv_title": m.arxiv_title},
    }


def cached_api_match(paper_id: str) -> Match | None:
    p = api_cache_path(paper_id)
    if not p.exists():
        return None
    m = json.loads(p.read_text(encoding="utf-8")).get("match")
    return Match(m["arxiv_id"], "api", m["score"], m.get("arxiv_title", "")) if m else None


# ------------------------------------------------------------------------------------ IEEE twins (Crossref, 10.1109)


def needs_ieee_twin(row: dict[str, str]) -> bool:
    """Paywalled rows outside IEEE: Optica (the main case) and other publishers (cheap: one Crossref query each)."""
    doi = norm_doi(row.get("doi"))
    return row.get("access") == "paywalled" and bool(doi) and not doi.startswith(tuple(p + "/" for p in IEEE_PREFIXES))


def crossref_hits(msg: dict[str, Any]) -> list[dict[str, Any]]:
    """Crossref /works items -> [{doi, title, authors ('given family'), year, venue}]."""
    out: list[dict[str, Any]] = []
    for it in msg.get("message", {}).get("items", []):
        parts = (it.get("issued") or {}).get("date-parts") or [[None]]
        year = parts[0][0] if parts and parts[0] else None
        out.append(
            {
                "doi": norm_doi(it.get("DOI")),
                "title": " ".join(it.get("title") or []),
                "authors": [
                    " ".join(x for x in (a.get("given", ""), a.get("family", "")) if x) for a in it.get("author") or []
                ],
                "year": int(year) if year else None,
                "venue": " ".join(it.get("container-title") or []),
            }
        )
    return out


def pick_ieee_hit(row: dict[str, str], hits: list[dict[str, Any]]) -> tuple[str, float] | None:
    """Best hit with an IEEE DOI prefix, title similarity >= TITLE_MIN, shared surname and |year - row year| <= 1.
    Only conference rows qualify: for a journal row (Optics Letters, Photonics Research) a same-title IEEE conference
    paper is a different, shorter publication, not a copy (biberman2012 / cheung2021 vs GFP, 2026-10-22)."""
    if row.get("venue_type") != "conference":
        return None
    names = row_names(row)
    try:
        year: int | None = int(row.get("year") or 0) or None
    except ValueError:
        year = None
    best: tuple[str, float] | None = None
    for h in hits:
        if not h["doi"].startswith(tuple(p + "/" for p in IEEE_PREFIXES)):
            continue
        if year is None or h["year"] is None or abs(h["year"] - year) > 1:
            continue
        s = title_sim(row["title"], h["title"])
        if s >= TITLE_MIN and surnames_share(names, h["authors"]) and (best is None or s > best[1]):
            best = (h["doi"], round(s, 4))
    return best


def ieee_cache_path(paper_id: str) -> Path:
    return IEEE_DIR / f"{paper_id}.json"


def ieee_query(row: dict[str, str]) -> dict[str, Any]:
    params = {
        "query.bibliographic": row["title"],
        "filter": "prefix:10.1109,prefix:10.23919",
        "rows": 5,
        "select": "DOI,title,author,issued,container-title",
    }
    hits = crossref_hits(litfetch.get_json(CROSSREF, params))
    m = pick_ieee_hit(row, hits)
    return {
        "paper_id": row["paper_id"],
        "doi": row["doi"],
        "queried_at": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
        "hits": [{**h, "title_sim": round(title_sim(row["title"], h["title"]), 4)} for h in hits],
        "match": None if m is None else {"ieee_doi": m[0], "score": m[1]},
    }


def cached_ieee_match(row: dict[str, str]) -> tuple[str, float] | None:
    """Re-applies pick_ieee_hit to the cached Crossref hits (so a rule change needs no new query)."""
    p = ieee_cache_path(row["paper_id"])
    if not p.exists():
        return None
    return pick_ieee_hit(row, json.loads(p.read_text(encoding="utf-8")).get("hits") or [])


# ----------------------------------------------------------------------------------------------- routes / schedule


def route_for(row: dict[str, str], arxiv_id: str, ieee_doi: str = "") -> tuple[str, str]:
    """(route, route_url). Preference: arXiv copy, then an IEEE twin of a paywalled non-IEEE row, then by DOI prefix."""
    doi = norm_doi(row.get("doi"))
    doi_url = f"https://doi.org/{doi}" if doi else ""
    if arxiv_id:
        return "arxiv", f"https://arxiv.org/pdf/{arxiv_id}"
    if ieee_doi and row.get("access") == "paywalled":
        return "ieee_browser", f"https://doi.org/{ieee_doi}"
    if (
        doi.startswith(tuple(p + "/" for p in OPTICA_PREFIXES))
        and row.get("access") == "paywalled"
        and (row.get("venue_type") == "conference" or OPTICA_CONF_DOI.match(doi))
    ):
        return "ieee_search", doi_url
    if doi.startswith(tuple(p + "/" for p in OPTICA_PREFIXES)):
        return "optica_browser", row.get("oa_url") or doi_url
    if doi.startswith(tuple(p + "/" for p in IEEE_PREFIXES)):
        return "ieee_browser", row.get("oa_url") or doi_url
    if row.get("access") == "oa" and row.get("oa_url"):
        host = urllib.parse.urlsplit(row["oa_url"]).netloc.lower()
        is_doi_host = host in ("doi.org", "dx.doi.org")
        if any(host == h or host.endswith("." + h) for h in MANUAL_HOSTS) or (
            is_doi_host and doi.startswith(tuple(p + "/" for p in MANUAL_PREFIXES))
        ):
            return "manual", row["oa_url"]
        blocked_host = any(host == h or host.endswith("." + h) for h in BROWSER_PUBLISHER_HOSTS)
        blocked_doi = doi.startswith(tuple(p + "/" for p in BROWSER_PUBLISHER_PREFIXES))
        if blocked_host or (blocked_doi and is_doi_host):
            return "publisher_browser", row["oa_url"]
        return "oa_publisher", row["oa_url"]
    return "manual", doi_url or row.get("oa_url", "")


def priority(row: dict[str, Any]) -> tuple[int, float, int, str]:
    """Curator picks first, then score (desc), then per-class rank, then paper_id."""
    cur = 0 if "curator" in str(row.get("selection_reason", "")) else 1
    try:
        rank = int(row.get("rank") or 10**6)
    except ValueError:
        rank = 10**6
    return (cur, -float(row.get("score") or 0), rank, str(row["paper_id"]))


def assign_days(rows: list[dict[str, Any]], n_days: int, day_cap: dict[str, int] | None = None) -> int:
    """Set row['day']: per route, class by class (classes by name, rows by priority), dealt to consecutive days 1..n_days
    with one running counter across all routes and classes. A capped route with more than cap * n_days rows keeps the
    first cap * n_days of its class round-robin order in the main days; the tail goes evenly to extra days after
    n_days (<= cap each). Returns the total number of days."""
    day_cap = DAY_CAP if day_cap is None else day_cap
    k = 0
    overflow: list[dict[str, Any]] = []
    for route in ROUTES:
        sel = [r for r in rows if r["route"] == route]
        cap = day_cap.get(route)
        if cap is not None and len(sel) > cap * n_days:
            ordered = class_round_robin(sel)
            sel, tail = ordered[: cap * n_days], ordered[cap * n_days :]
            overflow.extend(tail)
        by_cls: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for r in sel:
            by_cls[r["primary_class"]].append(r)
        for cls in sorted(by_cls):
            for r in sorted(by_cls[cls], key=priority):
                r["day"] = k % n_days + 1
                k += 1
    if not overflow:
        return n_days
    cap_min = min(day_cap[r["route"]] for r in overflow)
    extra = math.ceil(len(overflow) / cap_min)
    for j, r in enumerate(sorted(overflow, key=lambda r: (r["primary_class"], priority(r)))):
        r["day"] = n_days + j % extra + 1
    return n_days + extra


def class_round_robin(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Interleave classes (class order by its best row), each class in priority order."""
    by_cls: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in sorted(rows, key=priority):
        by_cls[r["primary_class"]].append(r)
    order = sorted(by_cls, key=lambda c: (priority(by_cls[c][0]), c))
    out: list[dict[str, Any]] = []
    for i in range(max((len(v) for v in by_cls.values()), default=0)):
        out.extend(by_cls[c][i] for c in order if i < len(by_cls[c]))
    return out


def split_sessions(n: int, cap: int) -> list[int]:
    """Near-equal session sizes, each <= cap (e.g. 33, 20 -> [17, 16])."""
    if n <= 0:
        return []
    k = math.ceil(n / cap)
    return [n // k + (1 if i < n % k else 0) for i in range(k)]


def order_and_sessions(rows: list[dict[str, Any]], n_days: int) -> list[dict[str, Any]]:
    """Final row order (day, route, class round-robin) and global per-site session numbers; routes of one site
    (ieee_browser + ieee_search) share that site's sessions."""
    out: list[dict[str, Any]] = []
    sess_no: Counter[str] = Counter()
    for day in range(1, n_days + 1):
        done: set[str] = set()
        for route in ROUTES:
            site = SITE.get(route)
            if site in done:
                continue
            members = [rt for rt in ROUTES if SITE.get(rt) == site] if site else [route]
            grp = class_round_robin([r for r in rows if r["day"] == day and r["route"] in members])
            if site:
                done.add(site)
                pos = 0
                for size in split_sessions(len(grp), SESSION_CAP[site]):
                    sess_no[site] += 1
                    for r in grp[pos : pos + size]:
                        r["session"] = sess_no[site]
                    pos += size
            else:
                for r in grp:
                    r["session"] = ""
            out.extend(grp)
    return out


def delta_slots(rows: list[dict[str, Any]], old_q: list[dict[str, str]], freeze_days: int) -> list[dict[str, Any]]:
    """Increment rebuild (D232). `rows` = new cache_list rows with computed matches / route; `old_q` = previous queue
    rows in file order. A retained paper keeps its previous queue row verbatim (`_verbatim`; route, day, session and
    match columns copied into the row for the schedule). An incoming paper takes the day slot of a displaced paper of
    the same primary class (same route first, then same site, then any; incoming in priority order), in that row's
    file position; its session is the slot's when the site matches, else the least-loaded session of its site on that
    day, '' for non-browser routes. Raises ValueError when a displaced row is on a frozen day (<= freeze_days), a uid
    changed under a kept paper_id, or the incoming and displaced class counts differ."""
    new_by = {r["paper_id"]: r for r in rows}
    old_ids = {q["paper_id"] for q in old_q}
    for q in old_q:
        r = new_by.get(q["paper_id"])
        if r is not None and r["uid"] != q["uid"]:
            raise ValueError(f"{q['paper_id']}: uid changed {q['uid']} -> {r['uid']}")
    displaced = [q for q in old_q if q["paper_id"] not in new_by]
    frozen = [q["paper_id"] for q in displaced if int(q["day"]) <= freeze_days]
    if frozen:
        raise ValueError(f"displaced rows on frozen days: {frozen}")
    incoming = [r for r in rows if r["paper_id"] not in old_ids]
    if Counter(r["primary_class"] for r in incoming) != Counter(q["primary_class"] for q in displaced):
        raise ValueError("incoming / displaced class counts differ")
    copy = ("route", "route_url", "session", "arxiv_match", "arxiv_match_score", "ieee_doi", "ieee_match_score")
    out: list[dict[str, Any]] = []
    for q in old_q:
        r = new_by.get(q["paper_id"])
        if r is not None:
            out.append({**r, **{k: q[k] for k in copy}, "day": int(q["day"]), "arxiv_id_q": q["arxiv_id"],
                        "_verbatim": q})  # fmt: skip
    load: Counter[tuple[int, str, int]] = Counter(
        (r["day"], SITE[r["route"]], int(r["session"])) for r in out if SITE.get(r["route"])
    )
    slot_of: dict[str, dict[str, Any]] = {}
    free = list(displaced)
    for r in sorted(incoming, key=priority):
        same = [q for q in free if q["primary_class"] == r["primary_class"]]
        site = SITE.get(r["route"])
        q = next(
            (x for x in same if x["route"] == r["route"]),
            next((x for x in same if site and SITE.get(x["route"]) == site), same[0]),
        )
        free.remove(q)
        r["day"] = int(q["day"])
        if site and SITE.get(q["route"]) == site:
            r["session"] = int(q["session"])
        elif site:
            cands = [k for k in load if k[0] == r["day"] and k[1] == site]
            if not cands:
                raise ValueError(f"no {site} session on day {r['day']} for {r['paper_id']}")
            r["session"] = min(cands, key=lambda k: (load[k], k[2]))[2]
        else:
            r["session"] = ""
        if site:
            load[(r["day"], site, int(r["session"]))] += 1
        slot_of[q["paper_id"]] = r
    final: list[dict[str, Any]] = []
    it = iter(out)
    for q in old_q:
        final.append(slot_of[q["paper_id"]] if q["paper_id"] in slot_of else next(it))
    return final


# --------------------------------------------------------------------------------------------------------- outputs


def schedule_md(rows: list[dict[str, Any]], dates: list[str], gains: dict[str, Any]) -> str:
    n_days = len(dates)
    L: list[str] = []
    L.append("# Retrieval schedule (DevLog-006 S7)")
    L.append("")
    L.append(
        f"Generated {dt.date.today().isoformat()} by `scripts/lit_build_queue.py` from `cache_list.csv`; queue: "
        "`data/_staging/literature/retrieval_queue.csv`. Each route is spread evenly over the days; inside a "
        "(day, route) the rows are ordered by class round-robin (curator picks, then score). arXiv copies are "
        "preprints: the journal DOI stays the identity; the arXiv copy is the retrieval route."
    )
    L.append("")
    L.append("## Totals")
    L.append("")
    tot = Counter(r["route"] for r in rows)
    L.append("| route | papers |")
    L.append("|---|---:|")
    for rt in ROUTES:
        L.append(f"| {rt} | {tot[rt]} |")
    L.append(f"| total | {len(rows)} |")
    L.append("")
    mk = Counter(r["arxiv_match"] for r in rows if r["arxiv_match"])
    L.append("arXiv copy source: " + ", ".join(f"{k} {mk[k]}" for k in ("given", "doi", "title", "api")) + ".")
    L.append("")
    L.append(
        f"arXiv route gained by matching (rows without arXiv id in cache_list): {gains['gained']} of "
        f"{gains['without']}; paywalled {gains['paywalled_gained']} of {gains['paywalled']}, Optica "
        f"{gains['optica_gained']} of {gains['optica']}, IEEE {gains['ieee_gained']} of {gains['ieee']}. API queries "
        f"cached {gains['api_cached']} of {gains['api_needed']} needed"
        + ("." if gains["api_cached"] >= gains["api_needed"] else " (rerun with --api to finish).")
    )
    L.append("")
    if gains.get("n_days", n_days) > gains.get("planned_days", n_days):
        L.append(
            f"Optica browser cap {gains['optica_day_cap']} per day x {gains['planned_days']} days is below the "
            f"Optica rows without an arXiv copy: the lowest-priority tail (class round-robin order) is on "
            f"{gains['n_days'] - gains['planned_days']} extra day(s) after day {gains['planned_days']}."
        )
        L.append("")
    L.append(
        f"IEEE twins (Crossref, prefix 10.1109 / 10.23919, title similarity >= {TITLE_MIN}, shared surname, year "
        f"within 1) of paywalled non-IEEE rows: {gains['twin_found']} found in {gains['twin_cached']} of "
        f"{gains['twin_needed']} lookups (only the {gains['twin_conference_rows']} conference rows qualify); paywalled Optica rows routed to ieee_browser via a twin: "
        f"{gains['optica_paywalled_twin_routed']} of {gains['optica_paywalled']}; other publishers: "
        f"{gains['other_paywalled_twin_routed']}. The Optica / journal DOI stays the identity (uid unchanged)."
    )
    L.append("")
    L.append("## Per day and route")
    L.append("")
    L.append("| day | date | " + " | ".join(ROUTES) + " | total | sessions (optica / ieee / publisher) |")
    L.append("|---:|---|" + "---:|" * len(ROUTES) + "---:|---|")
    for d in range(1, n_days + 1):
        dr = [r for r in rows if r["day"] == d]
        c = Counter(r["route"] for r in dr)
        ses = {
            st: sorted({int(r["session"]) for r in dr if SITE.get(r["route"]) == st and r["session"] != ""})
            for st in SITES
        }
        sdesc = " / ".join(",".join(map(str, ses[st])) or "-" for st in SITES)
        L.append(f"| {d} | {dates[d - 1]} | " + " | ".join(str(c[rt]) for rt in ROUTES) + f" | {len(dr)} | {sdesc} |")
    L.append("")
    L.append("## Per class and day")
    L.append("")
    classes = sorted({r["primary_class"] for r in rows})
    L.append("| class | " + " | ".join(f"d{d}" for d in range(1, n_days + 1)) + " | total |")
    L.append("|---|" + "---:|" * (n_days + 1))
    for cls in classes:
        c = Counter(r["day"] for r in rows if r["primary_class"] == cls)
        L.append(f"| {cls} | " + " | ".join(str(c[d]) for d in range(1, n_days + 1)) + f" | {sum(c.values())} |")
    L.append("")
    L.append("## Daily runbook")
    L.append("")
    L.append(
        "Fetchers update their own status log, not the queue. Browser sessions: one login per session "
        f"(IEEE <= 30 papers incl. ieee_search, Optica and publisher <= 20 papers, <= {gains['optica_day_cap']} Optica "
        "papers per day). ieee_search rows: Xplore title search for an IEEE copy of a paywalled Optica conference "
        "paper; without a hit the fetcher falls back to optica_browser at runtime. Manual papers: save the PDF as "
        "`references/_inbox/<paper_id>.pdf`."
    )
    for d in range(1, n_days + 1):
        dr = [r for r in rows if r["day"] == d]
        c = Counter(r["route"] for r in dr)
        L.append("")
        L.append(f"### Day {d} ({dates[d - 1]}): {len(dr)} papers")
        L.append("")
        L.append("```")
        L.append(
            f"uv run python scripts/lit_fetch_oa.py --day {d}   # arxiv {c['arxiv']} + oa_publisher {c['oa_publisher']}"
        )
        for st in SITES:
            for s in sorted({int(r["session"]) for r in dr if SITE.get(r["route"]) == st}):
                c_s = Counter(r["route"] for r in dr if SITE.get(r["route"]) == st and int(r["session"]) == s)
                note = " + ".join(f"{rt} {c_s[rt]}" for rt in ROUTES if c_s[rt])
                L.append(f"uv run python scripts/lit_fetch_browser.py --site {st} --day {d} --session {s}   # {note}")
        L.append("```")
        man = [r for r in dr if r["route"] == "manual"]
        if man:
            L.append("")
            L.append(f"Manual ({len(man)}):")
            L.append("")
            L.append("| paper_id | class | score | link | title |")
            L.append("|---|---|---:|---|---|")
            for r in man:
                t = r["title"].replace("|", "/")
                L.append(f"| {r['paper_id']} | {r['primary_class']} | {r['score']} | {r['route_url']} | {t} |")
    L.append("")
    return "\n".join(L)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="match and schedule, write nothing, send no request")
    ap.add_argument("--api", action="store_true", help="query the arXiv API for rows still unmatched")
    ap.add_argument("--max-queries", type=int, default=0, help="cap on API queries this run (0 = no cap)")
    ap.add_argument("--max-minutes", type=float, default=0.0, help="stop the API part after M minutes (0 = no cap)")
    ap.add_argument("--ieee-twins", action="store_true", help="Crossref lookup of IEEE twins for paywalled rows")
    ap.add_argument("--max-ieee-queries", type=int, default=0, help="cap on Crossref queries this run (0 = no cap)")
    ap.add_argument("--start", default="2026-10-22", help="date of day 1 (ISO)")
    ap.add_argument("--days", type=int, default=10)
    ap.add_argument(
        "--optica-day-cap",
        type=int,
        default=DAY_CAP["optica_browser"],
        help="max optica_browser papers per day; the tail goes to extra days (0 = no cap)",
    )
    ap.add_argument(
        "--delta",
        action="store_true",
        help="increment rebuild: keep previous queue rows verbatim, incoming papers take displaced rows' day slots",
    )
    ap.add_argument("--freeze-days", type=int, default=2, help="--delta: displaced rows on days <= N are an error")
    args = ap.parse_args()

    with RunLog("lit_build_queue", dry_run=args.dry_run) as log:
        with CACHE_LIST.open(encoding="utf-8", newline="") as f:
            rows: list[dict[str, Any]] = list(csv.DictReader(f))
        log.info(f"cache_list rows={len(rows)}")
        t0 = time.time()
        idx = PoolIndex(load_pool())
        log.info(f"arXiv pool records={len(idx.recs)} dois={len(idx.by_doi)} ({time.time() - t0:.1f} s)")

        matches: dict[str, Match | None] = {}
        local_out: list[dict[str, Any]] = []
        for r in rows:
            m = given_match(r) or local_match(r, idx)
            matches[r["paper_id"]] = m
            if m is not None and m.kind in ("doi", "title"):
                local_out.append({"paper_id": r["paper_id"], "doi": r["doi"], **m.__dict__})
        log.info("local: " + ", ".join(f"{k}={v}" for k, v in Counter(m.kind for m in matches.values() if m).items()))

        need = [r for r in rows if matches[r["paper_id"]] is None]
        todo = [r for r in need if not api_cache_path(r["paper_id"]).exists()]
        log.info(f"API needed={len(need)} cached={len(need) - len(todo)} todo={len(todo)}")
        if args.api and not args.dry_run and todo:
            API_DIR.mkdir(parents=True, exist_ok=True)
            todo = sorted(todo, key=priority)
            if args.max_queries:
                todo = todo[: args.max_queries]
            t_api = time.time()
            for i, r in enumerate(todo, 1):
                if args.max_minutes and time.time() - t_api > args.max_minutes * 60:
                    log.info(f"max-minutes reached after {i - 1} queries")
                    break
                try:
                    res = api_query(r)
                except litfetch.BlockedError as e:
                    log.info(f"API stopped (breaker): {e}")
                    log.event("api", "blocked", paper_id=r["paper_id"], error=str(e))
                    break
                except (urllib.error.URLError, TimeoutError, ET.ParseError, ValueError) as e:
                    log.info(f"API stopped ({type(e).__name__}): {e}")
                    log.event("api", "error", paper_id=r["paper_id"], error=str(e))
                    break
                p = api_cache_path(r["paper_id"])
                p.with_suffix(".part").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
                p.with_suffix(".part").rename(p)
                hit = res["match"]
                log.event("api", "match" if hit else "nomatch", paper_id=r["paper_id"], n_hits=len(res["hits"]))
                log.info(
                    f"  [{i}/{len(todo)}] {r['paper_id']}: hits={len(res['hits'])} "
                    + (f"match {hit['arxiv_id']} {hit['score']}" if hit else "no match")
                )
        for r in need:
            matches[r["paper_id"]] = cached_api_match(r["paper_id"])
        api_cached = sum(1 for r in need if api_cache_path(r["paper_id"]).exists())

        twin_rows = sorted(
            (r for r in rows if needs_ieee_twin(r)),
            key=lambda r: (not norm_doi(r["doi"]).startswith(tuple(p + "/" for p in OPTICA_PREFIXES)), priority(r)),
        )
        twin_todo = [r for r in twin_rows if not ieee_cache_path(r["paper_id"]).exists()]
        log.info(f"IEEE twin lookups needed={len(twin_rows)} todo={len(twin_todo)}")
        if args.ieee_twins and not args.dry_run and twin_todo:
            IEEE_DIR.mkdir(parents=True, exist_ok=True)
            if args.max_ieee_queries:
                twin_todo = twin_todo[: args.max_ieee_queries]
            for i, r in enumerate(twin_todo, 1):
                try:
                    res = ieee_query(r)
                except litfetch.BlockedError as e:
                    log.info(f"Crossref stopped (breaker): {e}")
                    log.event("ieee_twin", "blocked", paper_id=r["paper_id"], error=str(e))
                    break
                except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as e:
                    log.info(f"Crossref stopped ({type(e).__name__}): {e}")
                    log.event("ieee_twin", "error", paper_id=r["paper_id"], error=str(e))
                    break
                p = ieee_cache_path(r["paper_id"])
                p.with_suffix(".part").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
                p.with_suffix(".part").rename(p)
                hit = res["match"]
                log.event("ieee_twin", "match" if hit else "nomatch", paper_id=r["paper_id"], n_hits=len(res["hits"]))
                log.info(
                    f"  [ieee {i}/{len(twin_todo)}] {r['paper_id']}: hits={len(res['hits'])} "
                    + (f"twin {hit['ieee_doi']} {hit['score']}" if hit else "no twin")
                )
        twins = {r["paper_id"]: cached_ieee_match(r) for r in twin_rows}
        twin_cached = sum(1 for r in twin_rows if ieee_cache_path(r["paper_id"]).exists())

        # duplicate arXiv ids across rows (two journal papers mapped to one preprint) are reported, kept
        ids = Counter(m.arxiv_id for m in matches.values() if m)
        dups = {a: n for a, n in ids.items() if n > 1}
        if dups:
            log.info(f"warning: arXiv ids shared by several rows: {dups}")

        for r in rows:
            m = matches[r["paper_id"]]
            r["arxiv_id_q"] = m.arxiv_id if m else ""
            r["arxiv_match"] = m.kind if m else ""
            r["arxiv_match_score"] = "" if m is None or m.score is None else f"{m.score:.4f}"
            t = twins.get(r["paper_id"])
            r["ieee_doi"] = t[0] if t else ""
            r["ieee_match_score"] = f"{t[1]:.4f}" if t else ""
            r["route"], r["route_url"] = route_for(r, r["arxiv_id_q"], r["ieee_doi"])
        day_cap = {"optica_browser": args.optica_day_cap} if args.optica_day_cap > 0 else {}
        if args.delta:
            with QUEUE.open(encoding="utf-8", newline="") as f:
                old_q = list(csv.DictReader(f))
            computed = {r["paper_id"]: r["route"] for r in rows}
            rows = delta_slots(rows, old_q, args.freeze_days)
            n_days = max(r["day"] for r in rows)
            moved = [r["paper_id"] for r in rows if "_verbatim" in r and r["route"] != computed[r["paper_id"]]]
            new_ids = [r["paper_id"] for r in rows if "_verbatim" not in r]
            log.info(f"delta: kept {len(rows) - len(new_ids)} rows verbatim, incoming {new_ids}")
            log.info(f"delta: kept rows whose recomputed route differs (kept as queued): {moved}")
            for r in rows:
                if "_verbatim" not in r:
                    log.info(f"  incoming {r['paper_id']} {r['primary_class']} day {r['day']} {r['route']} "
                             f"session {r['session']!r} arxiv {r['arxiv_id_q'] or '-'}")  # fmt: skip
        else:
            n_days = assign_days(rows, args.days, day_cap)
            if n_days > args.days:
                log.info(f"warning: daily caps {day_cap} need {n_days - args.days} extra day(s) after day {args.days}")
            rows = order_and_sessions(rows, n_days)
        start = dt.date.fromisoformat(args.start)
        dates = [(start + dt.timedelta(days=i)).isoformat() for i in range(n_days)]
        for rt, cap in day_cap.items():
            over = {d: n for d, n in Counter(r["day"] for r in rows if r["route"] == rt).items() if n > cap}
            if over:
                log.info(f"warning: {rt} over {cap} per day on days {over}")

        def pre(r: dict[str, Any]) -> str:
            d = norm_doi(r["doi"])
            if d.startswith(tuple(p + "/" for p in OPTICA_PREFIXES)):
                return "optica"
            if d.startswith(tuple(p + "/" for p in IEEE_PREFIXES)):
                return "ieee"
            return "other"

        base = [r for r in rows if not r["arxiv_id"]]
        gained = [r for r in base if r["route"] == "arxiv"]
        gains = {
            "without": len(base),
            "gained": len(gained),
            "paywalled": sum(1 for r in base if r["access"] == "paywalled"),
            "paywalled_gained": sum(1 for r in gained if r["access"] == "paywalled"),
            "optica": sum(1 for r in base if pre(r) == "optica"),
            "optica_gained": sum(1 for r in gained if pre(r) == "optica"),
            "ieee": sum(1 for r in base if pre(r) == "ieee"),
            "ieee_gained": sum(1 for r in gained if pre(r) == "ieee"),
            "api_needed": len(need),
            "api_cached": api_cached,
            "by_kind": dict(Counter(r["arxiv_match"] for r in gained)),
            "twin_needed": len(twin_rows),
            "twin_cached": twin_cached,
            "twin_found": sum(1 for r in rows if r["ieee_doi"]),
            "twin_conference_rows": sum(1 for r in twin_rows if r.get("venue_type") == "conference"),
            "optica_paywalled": sum(1 for r in base if pre(r) == "optica" and r["access"] == "paywalled"),
            "optica_paywalled_twin": sum(1 for r in rows if r["ieee_doi"] and pre(r) == "optica"),
            "optica_paywalled_twin_routed": sum(
                1 for r in rows if r["ieee_doi"] and pre(r) == "optica" and r["route"] == "ieee_browser"
            ),
            "other_paywalled_twin_routed": sum(
                1 for r in rows if r["ieee_doi"] and pre(r) == "other" and r["route"] == "ieee_browser"
            ),
        }
        log.info(f"routes: {dict(Counter(r['route'] for r in rows))}")
        log.info(f"gains: {gains}")
        gains["n_days"], gains["planned_days"] = n_days, args.days
        gains["optica_day_cap"] = args.optica_day_cap
        log.event("summary", "ok", routes=dict(Counter(r["route"] for r in rows)), gains=gains)

        out_rows = [
            r["_verbatim"]
            if "_verbatim" in r
            else {
                **{k: r.get(k, "") for k in COLUMNS},
                "date": dates[r["day"] - 1],
                "arxiv_id": r["arxiv_id_q"],
                "status": "",
            }
            for r in rows
        ]
        if args.dry_run:
            log.info("dry-run: nothing written")
            return
        MATCH_DIR.mkdir(parents=True, exist_ok=True)
        (MATCH_DIR / "local_matches.jsonl").write_text(
            "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in local_out), encoding="utf-8"
        )
        with QUEUE.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLUMNS)
            w.writeheader()
            w.writerows(out_rows)
        SCHEDULE.write_text(schedule_md(rows, dates, gains), encoding="utf-8")
        log.info(f"wrote {QUEUE} ({len(out_rows)} rows), {SCHEDULE}")


if __name__ == "__main__":
    main()
