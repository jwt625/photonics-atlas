"""Reference graph from the reference sections of cached `lit` papers (DevLog-020).

Each cached `references/<id>/text.md` is scanned for its numbered reference list (location-agnostic: the longest run
of entries counting up from 1, most of them carrying a year). Every entry is matched, offline, in this order:
  1. DOI / arXiv id exact against the corpus (every registry corpus + cache_list rows);
  2. title containment against the corpus: title and entry squashed to [a-z0-9] (NFKD; no spaces / punctuation, so
     hyphenation, line breaks, ligatures and quotes do not matter); exact substring = 1.0, else the matched-block
     fraction of the title; candidates from a title word-bigram index; year within +/- 1 when the entry has years;
  3. the same against the OpenAlex pool (cache/literature/merged.jsonl) for works outside the corpus;
  4. the rest clustered by a quoted title (IEEE / Optica style) or surname + year + volume + page.
Outputs (git-ignored): cache/literature/refgraph/<out>/refs.jsonl, missing.csv, summary.json.

Usage (repo root): uv run --offline python scripts/lit_refgraph.py [--paper-ids a,b] [--limit N] [--out NAME]
"""

from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import json
import re
import sys
import unicodedata
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from photonics_atlas.litpool import norm_doi  # noqa: E402

REFS = ROOT / "references"
SOURCES = ROOT / "data/registry/sources.csv"
CACHE_LIST = ROOT / "data/_staging/literature/cache_list.csv"
POOL = ROOT / "cache/literature/merged.jsonl"
OUT_ROOT = ROOT / "cache/literature/refgraph"

MATCH_MIN = 0.90  # containment score for a match (pilot-calibrated, DevLog-020)
MIN_SQ_TITLE = 18  # squashed titles shorter than this only match exactly (and with a year check)
BIGRAM_DF_MAX = 400  # bigrams in more titles than this are not used for candidates
MAX_CANDS = 12

STOP = set(
    "a an and the of in on for with by to from at via as is are using based its into or over under between toward "
    "towards".split()
)
START_RE = re.compile(
    r"^\s*(?:\[(\d{1,3})\]|(\d{1,3})\.(?=\s|$)|\((\d{1,3})\)(?=\s)|(\d{1,3})(?=\s+[A-Z])"
    r"|(\d{1,3})(?=[A-Z][a-z]?\.\s)|(\d{1,3})\s\.(?=\s)|(\d{1,3})\s*$)\s*"
)
# START_RE group order; a reference run keeps one style. glued = "1M. Hochberg", spaced_dot = "1 . W.",
# lone = the number alone on its line (the entry starts on the next line)
STYLES = ("bracket", "dot", "paren", "bare", "glued", "spaced_dot", "lone")
SECTION_RE = re.compile(
    r"^(?:introduction|background|results?|methods?|discussion|conclusions?|summary|overview|design|theory|"
    r"experiment|fabrication|simulation|measurement|principle|device|acknowledg)",
    re.I,
)
NEAR_RUN = 0.85  # runs at least this fraction of the longest compete; the latest "1" wins (audit rec 1)
INVITED_RE = re.compile(r"\s*(?:[\[(]\s*invited\s*[\])]|invited paper)\s*", re.I)
HEADER_RES = (  # running headers / footers that leak into entries (audit rec 12)
    re.compile(r"Authorized licensed use limited to.{0,250}?Restrictions apply\.?", re.S),
    re.compile(r"(?m)^[A-Z][A-Z &,.:-]{8,}\bVOL\.\s*\d+.*$"),
    re.compile(r"(?m)^\s*(?:Letter RESEARCH|RESEARCH Letter|RESEARCH ARTICLE|ARTICLE)\s*$"),
)
BLOG_PREFIX_RE = re.compile(r"^[A-Z][^,]{1,40}? (?:et al\.? )?(?:19|20)\d\d[a-z]?, ")
PAPER_CORPORA = ("lit", "eo", "pk", "ofc2026", "blog")
SHORT_SQ = 30  # squashed titles shorter than this also need the surname (or the exact year) in the entry
AUTHOR_MIN = 0.85  # containment accepted below MATCH_MIN when the entry's first author and the exact year agree
LONGEST_MIN = 0.6  # a partial (< 1.0) containment needs one block covering this fraction of the title (audit rec 7)
YEAR_RE = re.compile(r"(?<!\d)(1[89]\d\d|20[0-3]\d)(?!\d)")
DOI_RE = re.compile(r"\b(10\.\d{4,9}/[^\s\"<>]+)", re.I)
ARXIV_RE = re.compile(r"arxiv[:\s/]*(?:abs/)?(\d{4}\.\d{4,5})", re.I)
QUOTED_RE = re.compile(r"[“\"]([^”\"]{12,300})[”\"]")
PAGE_MARK_RE = re.compile(r"<!--\s*page\s+\d+\s*-->")


def squash(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "", s)


def words(s: str) -> list[str]:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).split()


def bigrams(ws: list[str]) -> set[str]:
    ws = [w for w in ws if w not in STOP]
    return {f"{a} {b}" for a, b in zip(ws, ws[1:], strict=False)}


OPTICA_FOOTER_RE = re.compile(
    r"#\d{5,7}\s*(?:-\s*\$\d+\.\d+\s*USD\s*)?Received.{0,260}?"
    r"(?:OPTICS EXPRESS|OPTICAL MATERIALS EXPRESS|BIOMEDICAL OPTICS EXPRESS|OPTICA)\s*\d+",
    re.S,
)


def clean_entry(s: str) -> str:
    s = PAGE_MARK_RE.sub(" ", s)
    for rx in HEADER_RES:
        s = rx.sub(" ", s)
    s = OPTICA_FOOTER_RE.sub(" ", s)  # journal page footer carrying the citing paper's own DOI
    s = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", s)  # line-break hyphenation
    return re.sub(r"\s+", " ", s).strip()


# ---------- reference entries ----------


def _starts(lines: list[str]) -> list[tuple[int, int, int]]:
    """(line index, number, style index) of every numbered line start."""
    out = []
    for i, ln in enumerate(lines):
        m = START_RE.match(ln)
        if m:
            st = next(k for k, g in enumerate(m.groups()) if g)
            out.append((i, int(m.groups()[st]), st))
    return out


def split_references(text: str) -> list[tuple[int, str]]:
    """[(number, cleaned entry)] of the longest run of numbered entries counting up from 1 (most with a year)."""
    lines = PAGE_MARK_RE.sub("", text).split("\n")
    starts = _starts(lines)
    runs: list[list[tuple[int, int, int]]] = []
    for k, (i, n, st) in enumerate(starts):
        if n != 1:
            continue
        nxt = next((s_[0] for s_ in starts[k + 1 :] if s_[2] == st), min(len(lines), i + 8))
        first = START_RE.sub("", "\n".join(lines[i:nxt]), count=1).strip()
        if not YEAR_RE.search(first) and (len(first) > 300 or SECTION_RE.match(first)):
            continue  # a section heading, not a first reference
        run = [starts[k]]
        for j in range(k + 1, len(starts)):
            if starts[j][2] == st and starts[j][1] == run[-1][1] + 1:
                run.append(starts[j])
        runs.append(run)
    if not runs:
        return []
    longest = max(len(r) for r in runs)
    best = max((r for r in runs if len(r) >= NEAR_RUN * longest), key=lambda r: r[0][0])
    if len(best) < 3:
        return []
    ents = []
    for a, (i, n, _st) in enumerate(best):
        end = best[a + 1][0] if a + 1 < len(best) else min(len(lines), i + 12)
        body = "\n".join(lines[i:end])
        body = START_RE.sub("", body, count=1)
        ents.append((n, clean_entry(body)[:1200]))
    with_year = sum(1 for _, e in ents if YEAR_RE.search(e))
    if with_year < 0.5 * len(ents):
        return []
    # the last entry has no successor: cut it after its first year-bearing sentence end
    n, e = ents[-1]
    m = YEAR_RE.search(e)
    if m:
        cut = e.find(".", m.end())
        ents[-1] = (n, e[: cut + 1] if cut > 0 else e[:400])
    return ents


# ---------- corpus / pool records ----------


@dataclass
class Work:
    wid: str
    title: str
    year: int | None
    doi: str = ""
    arxiv: str = ""
    surname: str = ""
    kind: str = "corpus"  # corpus | queued | pool
    extra: dict[str, Any] = field(default_factory=dict)
    sq: str = ""

    def __post_init__(self) -> None:
        self.sq = squash(INVITED_RE.sub(" ", self.title))


def surname_of(name: str) -> str:
    ws = words(name)
    return ws[-1] if ws else ""


def _int(y: Any) -> int | None:
    try:
        return int(str(y)[:4])
    except (TypeError, ValueError):
        return None


def load_corpus() -> list[Work]:
    out: list[Work] = []
    seen: set[str] = set()
    cached = {p.parent.name for p in REFS.glob("*/source.pdf")} | {p.parent.name for p in REFS.glob("*/text.md")}
    cl = {r["paper_id"]: r for r in csv.DictReader(CACHE_LIST.open(encoding="utf-8")) if r.get("paper_id")}
    for r in csv.DictReader(SOURCES.open(encoding="utf-8")):
        if r["corpus"] not in PAPER_CORPORA:
            continue
        sur = surname_of(cl[r["native_id"]]["first_author"]) if r["corpus"] == "lit" and r["native_id"] in cl else ""
        title = BLOG_PREFIX_RE.sub("", r["title"]) if r["corpus"] == "blog" else r["title"]
        kind = "corpus" if r["text_cached"] == "true" else "registry_uncached"
        out.append(Work(r["source_id"], title, _int(r["year"]), norm_doi(r["doi"]), r["arxiv_id"].strip(), sur, kind))
        seen.add(r["source_id"])
    for pid, r in cl.items():
        if f"lit:{pid}" in seen:
            continue
        kind = "corpus" if pid in cached else "queued"
        w = Work(f"lit:{pid}", r["title"], _int(r["year"]), norm_doi(r["doi"]), r["arxiv_id"].strip(), "", kind)
        w.surname = surname_of(r.get("first_author") or "")
        out.append(w)
    return out


def load_pool(path: Path = POOL) -> list[Work]:
    """Pool records; records whose title is a venue name (journal front matter) are dropped (audit rec 8)."""
    works = list(_pool_records(path))
    venues = {squash(w.extra["venue"]) for w in works if w.extra.get("venue")}
    return [w for w in works if w.sq not in venues]


def _pool_records(path: Path) -> Iterator[Work]:
    with path.open(encoding="utf-8") as f:
        for line in f:
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not d.get("title"):
                continue
            au = d.get("authors") or []
            yield Work(
                d.get("uid") or norm_doi(d.get("doi")),
                d["title"],
                _int(d.get("year")),
                norm_doi(d.get("doi")),
                (d.get("arxiv_id") or "").strip(),
                surname_of(au[0]) if au else "",
                "pool",
                {
                    "venue": d.get("venue") or "",
                    "oa_status": d.get("oa_status") or "",
                    "oa_url": d.get("oa_url") or "",
                    "type": d.get("type") or "",
                },
            )


class Index:
    def __init__(self, works: Iterable[Work]) -> None:
        self.works: list[Work] = []
        self.by_doi: dict[str, int] = {}
        self.by_arxiv: dict[str, int] = {}
        self.by_sq: dict[str, list[int]] = collections.defaultdict(list)
        self.by_sur_year: dict[tuple[str, int], list[int]] = collections.defaultdict(list)
        self.nbig: list[int] = []
        post: dict[str, list[int]] = collections.defaultdict(list)
        for w in works:
            if len(w.sq) < 8:
                continue
            k = len(self.works)
            self.works.append(w)
            if w.doi:
                self.by_doi.setdefault(w.doi, k)
            if w.arxiv:
                self.by_arxiv.setdefault(w.arxiv, k)
            if len(w.sq) >= MIN_SQ_TITLE:
                self.by_sq[w.sq].append(k)
            if w.surname and w.year:
                self.by_sur_year[(w.surname, w.year)].append(k)
            bg = sorted(bigrams(words(INVITED_RE.sub(" ", w.title))))
            self.nbig.append(len(bg))
            for b in bg:
                post[b].append(k)
        self.post = {b: v for b, v in post.items() if len(v) <= BIGRAM_DF_MAX}

    def candidates(self, entry_words: list[str]) -> list[int]:
        cnt: collections.Counter[int] = collections.Counter()
        for b in sorted(bigrams(entry_words)):  # sorted: set order follows the per-process string hash
            for k in self.post.get(b, ()):
                cnt[k] += 1
        ranked = sorted(cnt.items(), key=lambda kc: (-kc[1], kc[0]))[: MAX_CANDS * 3]
        # one shared bigram suffices for titles with at most one indexable bigram (audit rec 4)
        return [k for k, c in ranked if c >= min(2, max(1, self.nbig[k])) or len(self.works[k].sq) < 30][:MAX_CANDS]


def containment(title_sq: str, entry_sq: str) -> float:
    if not title_sq:
        return 0.0
    if title_sq in entry_sq:
        return 1.0
    sm = SequenceMatcher(None, title_sq, entry_sq, autojunk=False)
    blocks = [b for b in sm.get_matching_blocks() if b.size >= 4]
    if not blocks or max(b.size for b in blocks) < LONGEST_MIN * len(title_sq):
        return min(sum(b.size for b in blocks) / len(title_sq), MATCH_MIN - 0.01) if blocks else 0.0
    return sum(b.size for b in blocks) / len(title_sq)


def year_ok(w: Work, years: set[int]) -> bool:
    return not years or w.year is None or any(abs(w.year - y) <= 1 for y in years)


def match(entry: str, idx: Index) -> dict[str, Any] | None:
    low = entry.lower()
    for d in entry_dois(entry) + built_dois(entry):
        if d in idx.by_doi:
            w = idx.works[idx.by_doi[d]]
            return {"id": w.wid, "kind": w.kind, "method": "doi", "score": 1.0, "accepted": True, "w": w}
    ma = ARXIV_RE.search(low)
    if ma and ma.group(1) in idx.by_arxiv:
        w = idx.works[idx.by_arxiv[ma.group(1)]]
        return {"id": w.wid, "kind": w.kind, "method": "arxiv", "score": 1.0, "accepted": True, "w": w}
    esq = squash(entry)
    ews = words(entry)
    fsur = first_surname(entry)
    years = {int(y) for y in YEAR_RE.findall(entry)}
    quoted = [q.group(1) for q in QUOTED_RE.finditer(entry)]
    if quoted:  # exact squashed quoted title (audit rec 4)
        hits = [
            idx.works[k]
            for k in idx.by_sq.get(squash(INVITED_RE.sub(" ", quoted[0])), [])
            if year_ok(idx.works[k], years)
        ]
        if hits:
            w = max(hits, key=lambda x: (x.kind == "corpus", x.surname == fsur))
            return {"id": w.wid, "kind": w.kind, "method": "title_exact", "score": 1.0, "accepted": True, "w": w}
    elif fsur and years:  # title-less entry: same first author + year, page / article number inside the DOI
        pg = first_page(entry)
        if len(pg) >= 3:
            rx = re.compile(rf"(?<![0-9]){re.escape(pg)}(?![0-9])")
            hits = [
                idx.works[k]
                for y in sorted(years)
                for k in idx.by_sur_year.get((fsur, y), [])
                if idx.works[k].doi and rx.search(idx.works[k].doi.split("/", 1)[-1].lstrip("0"))
            ]
            if len({w.wid for w in hits}) == 1:
                w = hits[0]
                return {"id": w.wid, "kind": w.kind, "method": "author_page", "score": 1.0, "accepted": True, "w": w}
    best: tuple[int, float, int, Work | None, str] = (0, 0.0, 0, None, "")
    for k in idx.candidates(ews):
        w = idx.works[k]
        if not year_ok(w, years):
            continue
        s = (1.0 if w.sq in esq else 0.0) if len(w.sq) < MIN_SQ_TITLE else containment(w.sq, esq)
        sur = bool(w.surname) and w.surname == fsur
        exact_year = w.year is not None and w.year in years
        if len(w.sq) < SHORT_SQ:  # authorless pool records never pass on the year alone (audit rec 8)
            acc, meth = s >= 1.0 and (sur or (not w.surname and w.kind != "pool" and exact_year)), "title_short"
        elif s >= MATCH_MIN:
            acc, meth = True, "title"
        else:
            acc, meth = s >= AUTHOR_MIN and sur and exact_year, "title_author"
        rank = (int(acc), s, int(w.kind == "corpus"))
        if rank > best[:3]:
            best = (*rank, w, meth)
    acc_i, s, _c, bw, meth = best
    if bw is None:
        return None
    return {"id": bw.wid, "kind": bw.kind, "method": meth, "score": round(s, 4), "accepted": bool(acc_i), "w": bw}


# ---------- unmatched clustering ----------


PAGE_RES = (
    re.compile(r"\b\d{1,4}\s*\(\d{1,3}\)\s*,\s*([A-Za-z]?\d{2,7})"),  # 24(12), 4763-4789
    re.compile(
        r"\b\d{1,4}\s*,\s*([A-Za-z]?\d{2,7})(?:\s*[-\u2013]\s*[A-Za-z]?\d+)?\s*\((?:19|20)\d\d\)"
    ),  # 9, 358 (2015)
    re.compile(r"\bpp?\.\s*([A-Za-z]?\d{1,7})"),  # pp. 2478
    re.compile(r"\bart(?:icle)?\.?\s*(?:no\.?\s*)?([A-Za-z]?\d{3,9})", re.I),  # Art. no. 073003
)


def first_surname(entry: str) -> str:
    """First author's surname token: IEEE / Optica 'D. J. Thomson, ...' or Nature 'Soref, R. ...'."""
    head = re.split(r"[\u201c\"]", entry, maxsplit=1)[0][:120]
    for w in words(head):
        if len(w) > 1 and not w.isdigit():
            return w
    return ""


def first_page(entry: str) -> str:
    for rx in PAGE_RES:
        m = rx.search(entry)
        if m:
            return m.group(1).lower().lstrip("0") or "0"
    return ""


def entry_dois(entry: str) -> list[str]:
    """Normalized DOIs in an entry; a suffix shorter than 6 characters is a DOI cut at a line break, not used."""
    out = []
    for m in DOI_RE.finditer(entry):
        d = norm_doi(m.group(1).rstrip(".,;)]"))
        if len(d.split("/", 1)[-1]) >= 6:
            out.append(d)
    return out


# Venue + volume + first page -> DOI for journals with a fixed DOI pattern (audit rec 3a). Optica legacy journals
# zero-pad the page to 6 digits; APS uses the printed page / article number.
OPTICA_VENUES = (
    (re.compile(r"\bOpt(?:ics)?\.?\s*Express\b", re.I), "oe"),
    (re.compile(r"\bOpt(?:ics)?\.?\s*Lett(?:ers)?\b\.?", re.I), "ol"),
    (re.compile(r"\bAppl(?:ied)?\.?\s*Opt(?:ics)?\b\.?", re.I), "ao"),
    (re.compile(r"\bJ\.?\s*Opt\.?\s*Soc\.?\s*Am\.?\s*B\b", re.I), "josab"),
    (re.compile(r"\bOpt(?:ical)?\.?\s*Mater(?:ials)?\.?\s*Express\b", re.I), "ome"),
    (re.compile(r"\bBiomed(?:ical)?\.?\s*Opt(?:ics)?\.?\s*Express\b", re.I), "boe"),
    (re.compile(r"\bOptica\b(?!\s*(?:Publishing|Open))"), "optica"),
)
APS_VENUES = (
    (re.compile(r"\bPhys(?:ical)?\.?\s*Rev(?:iew)?\.?\s*Lett(?:ers)?\b\.?", re.I), "physrevlett"),
    (re.compile(r"\bPhys(?:ical)?\.?\s*Rev(?:iew)?\.?\s*Appl(?:ied)?\b\.?", re.I), "physrevapplied"),
    (re.compile(r"\bPhys(?:ical)?\.?\s*Rev(?:iew)?\.?\s*X\b", re.I), "physrevx"),
    (re.compile(r"\bPhys(?:ical)?\.?\s*Rev(?:iew)?\.?\s*([ABE])\b"), "physrev"),
    (re.compile(r"\bRev(?:iews)?\.?\s*Mod(?:ern)?\.?\s*Phys(?:ics)?\b\.?", re.I), "revmodphys"),
)
VOL_PAGE_RE = re.compile(
    r"^\W{0,3}(?:vol\.?\s*)?(\d{1,4})(?!\d)\s*,?\s*(?:\(\s*\d{1,3}\s*\))?\s*(?:,?\s*no\.?\s*\d{1,3})?\s*[,:]?\s*"
    r"(?:pp?\.?\s*)?([A-Z]?\d{1,3}(?:[ \u2009]\d{3})+|[A-Z]?\d{1,7})(?!\d)",
    re.I,
)
APS_6DIGIT_FROM = {"physrevlett": 86, "physreva": 63, "physrevb": 63, "physreve": 63}  # article numbers since 2001


def built_dois(entry: str) -> list[str]:
    out = []
    for rx, code in OPTICA_VENUES + APS_VENUES:
        m = rx.search(entry)
        if not m:
            continue
        vp = VOL_PAGE_RE.match(entry[m.end() :])
        if not vp:
            continue
        vol, page = vp.group(1), re.sub(r"[ \u2009]", "", vp.group(2)).lower()
        if int(vol) >= 1000:  # "Opt. Express 2014, 22, 22172": a year, not a volume
            continue
        if code.startswith("physrev") or code == "revmodphys":
            journal = f"physrev{m.group(1).lower()}" if code == "physrev" else code
            if page.isdigit() and len(page) == 5 and int(vol) >= APS_6DIGIT_FROM.get(journal, 10**6):
                page = "0" + page  # printed without the leading zero
            out.append(f"10.1103/{journal}.{vol}.{page}")
        elif page.isdigit():
            jcode = "opex" if code == "oe" and int(vol) <= 13 else code  # Optics Express DOIs before 2006
            out.append(f"10.1364/{jcode}.{vol}.{int(page):06d}")
    return out


def unmatched_keys(entry: str) -> tuple[list[str], str]:
    """Cluster keys of an unmatched entry (DOI, quoted title, surname|year|first page) and its quoted title.
    Entries sharing any key are one work (union-find), so an IEEE-style and a Nature-style citation merge. An entry
    with two or more quoted titles holds several works: only its first title is used as a key."""
    titles = [q.group(1) for q in QUOTED_RE.finditer(entry) if len(squash(q.group(1))) >= MIN_SQ_TITLE]
    keys = []
    title = titles[0].strip().rstrip(",") if titles else ""
    if title:
        keys.append("title:" + squash(title))
    if len(titles) <= 1:
        dois = entry_dois(entry) or built_dois(entry)
        if len(dois) == 1:
            keys.append("doi:" + dois[0])
        yrs = YEAR_RE.findall(entry)
        sur, pg = first_surname(entry), first_page(entry)
        if sur and yrs and len(pg) >= 3:
            keys.append(f"bib:{sur}|{yrs[-1]}|{pg}")
    if not keys:
        keys.append("raw:" + squash(entry)[:80])
    return keys, title


class UnionFind:
    def __init__(self) -> None:
        self.p: dict[str, str] = {}

    def find(self, x: str) -> str:
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


# ---------- run ----------


def run(paper_ids: list[str] | None, limit: int | None, out: str, use_pool: bool) -> dict[str, Any]:
    t0 = dt.datetime.now()
    corpus = load_corpus()
    cidx = Index(corpus)
    print(f"corpus works {len(cidx.works)} ({dt.datetime.now() - t0})", flush=True)
    pidx = Index(load_pool()) if use_pool else None
    if pidx:
        print(f"pool works {len(pidx.works)} ({dt.datetime.now() - t0})", flush=True)
        for w in cidx.works:  # first-author surnames for corpus rows without one (registry has no authors)
            if not w.surname and w.doi in pidx.by_doi:
                w.surname = pidx.works[pidx.by_doi[w.doi]].surname
    lit_ids = sorted(p.parent.name for p in REFS.glob("*/text.md"))
    pclass = {r["paper_id"]: r["primary_class"] for r in csv.DictReader(CACHE_LIST.open(encoding="utf-8"))}
    own_doi = {w.wid[4:]: w.doi for w in corpus if w.wid.startswith("lit:") and w.doi}
    if paper_ids:
        lit_ids = [p for p in paper_ids if p in set(lit_ids)]
    if limit:
        lit_ids = lit_ids[:limit]
    odir = OUT_ROOT / out
    odir.mkdir(parents=True, exist_ok=True)
    stats: collections.Counter[str] = collections.Counter()
    missing: dict[str, dict[str, Any]] = {}
    in_deg: collections.Counter[str] = collections.Counter()
    unmatched: list[tuple[str, str, list[str], str]] = []
    with (odir / "refs.jsonl").open("w", encoding="utf-8") as fo:
        for pid in lit_ids:
            text = (REFS / pid / "text.md").read_text(encoding="utf-8", errors="replace")
            ents = split_references(text)
            stats["papers"] += 1
            stats["papers_with_refs" if ents else "papers_no_refs"] += 1
            seen_targets: set[str] = set()
            own = own_doi.get(pid, "")
            for n, e in ents:
                stats["refs"] += 1
                if own:  # the citing paper's own DOI (page footers) is never a reference
                    e = re.sub(re.escape(own), " ", e, flags=re.I)
                r = match(e, cidx)
                self_hit = bool(r and r["accepted"] and r["id"] == f"lit:{pid}")
                if (self_hit or not (r and r["accepted"])) and pidx is not None:
                    rp = match(e, pidx)
                    if rp and own and rp["w"].doi == own:
                        rp = None  # the pool record of the citing paper itself
                    if rp and (rp["accepted"] or (not self_hit and (not r or rp["score"] > r["score"]))):
                        r, self_hit = rp, False
                ok = bool(r and r["accepted"])
                row: dict[str, Any] = {"citing": pid, "n": n, "entry": e[:500]}
                if r:
                    row.update({k: r[k] for k in ("id", "kind", "method", "score", "accepted")})
                    row["title"] = r["w"].title
                row["matched"] = ok and not self_hit
                if self_hit:  # an earlier version of the citing paper (conference / preprint): not a missing work
                    stats["self_version"] += 1
                    row["self_version"] = True
                elif ok and r is not None:
                    stats[f"match_{r['kind']}_{r['method']}"] += 1
                    key = r["id"]
                    if r["kind"] in ("pool", "registry_uncached"):
                        w = r["w"]
                        mrow = missing.setdefault(
                            key,
                            {
                                "key": key,
                                "doi": w.doi,
                                "title": w.title,
                                "year": w.year or "",
                                "venue": w.extra.get("venue", ""),
                                "oa_status": w.extra.get("oa_status", ""),
                                "type": w.extra.get("type", ""),
                                "resolved": "pool" if r["kind"] == "pool" else f"registry ({w.wid})",
                                "citing": [],
                                "example": e[:300],
                            },
                        )
                        if pid not in mrow["citing"]:
                            mrow["citing"].append(pid)
                    elif key not in seen_targets:
                        in_deg[key] += 1
                    seen_targets.add(key)
                else:
                    stats["unmatched"] += 1
                    keys, title = unmatched_keys(e)
                    row["cluster_keys"] = keys
                    unmatched.append((pid, e, keys, title))
                fo.write(json.dumps(row, ensure_ascii=False) + "\n")
    uf = UnionFind()
    for _pid, _e, keys, _t in unmatched:
        for k in keys[1:]:
            uf.union(keys[0], k)
    for pid, e, keys, title in unmatched:
        root = uf.find(keys[0])
        mrow = missing.setdefault(
            root,
            {
                "key": root,
                "doi": "",
                "title": "",
                "year": (YEAR_RE.findall(e) or [""])[-1],
                "venue": "",
                "oa_status": "",
                "type": "",
                "resolved": "unresolved",
                "citing": [],
                "example": e[:300],
            },
        )
        for k in keys:
            if k.startswith("doi:") and not mrow["doi"]:
                mrow["doi"] = k[4:]
        if title and not mrow["title"]:
            mrow["title"] = title
        if pid not in mrow["citing"]:
            mrow["citing"].append(pid)
    rows = sorted(missing.values(), key=lambda x: (-len(x["citing"]), x["key"]))
    with (odir / "missing.csv").open("w", newline="", encoding="utf-8") as f:
        cols = [
            "n_citing",
            "key",
            "resolved",
            "doi",
            "title",
            "year",
            "venue",
            "type",
            "oa_status",
            "citing_classes",
            "citing",
            "example",
        ]
        wr = csv.DictWriter(f, fieldnames=cols)
        wr.writeheader()
        for x in rows:
            cc = collections.Counter(pclass.get(c, "") for c in x["citing"] if pclass.get(c))
            wr.writerow(
                {
                    **x,
                    "n_citing": len(x["citing"]),
                    "citing": ";".join(x["citing"]),
                    "citing_classes": ";".join(f"{k}:{v}" for k, v in cc.most_common()),
                }
            )
    summary = {
        "run": dt.datetime.now().isoformat(timespec="seconds"),
        "match_min": MATCH_MIN,
        "stats": dict(stats),
        "missing_works": len(rows),
        "missing_pool_resolved": sum(1 for x in rows if x["resolved"] == "pool"),
        "missing_cited_2plus": sum(1 for x in rows if len(x["citing"]) >= 2),
        "corpus_in_degree_top": in_deg.most_common(25),
    }
    (odir / "summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(json.dumps(summary["stats"], indent=1))
    print(f"missing works {len(rows)} -> {odir.relative_to(ROOT)} ({dt.datetime.now() - t0})")
    return summary


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0] if __doc__ else None)
    ap.add_argument("--paper-ids", help="comma-separated lit paper ids")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--out", default=dt.datetime.now().strftime("run_%Y%m%dT%H%M%S"))
    ap.add_argument("--no-pool", action="store_true", help="skip the OpenAlex pool (faster; corpus matches only)")
    a = ap.parse_args()
    ids = [s.strip() for s in (a.paper_ids or "").split(",") if s.strip()] or None
    run(ids, a.limit, a.out, not a.no_pool)
    return 0


if __name__ == "__main__":
    sys.exit(main())
