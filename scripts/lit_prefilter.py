"""Literature pool merge, dedupe, known-id exclusion and regex prefilter (DevLog-006 S2).

Steps (each re-runnable over the growing pool; outputs are rewritten from scratch each run):
  merge      cache/literature/pool/*.jsonl -> cache/literature/merged.jsonl
             one record per work (keys: DOI, arXiv id, OpenAlex id, normalized title + first-author surname);
             published version's metadata preferred, arxiv_id + preprint oa_url kept, lane / discovered_via /
             seed_class unioned into lists, longest abstract kept; dropped types (erratum, editorial, ...) removed;
             known_in = corpora that already hold the work (sources.csv, EO atlas, packaging atlas, OFC 2026).
  prefilter  merged.jsonl -> cache/literature/prefiltered.jsonl (candidates with class hits, rule score, cap flag
             score_keep) + cache/literature/prefilter_rejects.jsonl (uid, title, status) +
             data/_staging/literature/prefilter_stats.md (committed counts only)
  all        merge then prefilter (default)
  sample     print titles of one class bucket (or one reject status) for precision checks

Config: config/literature/buckets.yaml (regexes, cues, exclusions, caps), config/literature/selection.yaml (budget).
Usage: uv run python scripts/lit_prefilter.py [all|merge|prefilter] [--dry-run]
       uv run python scripts/lit_prefilter.py sample --cls wdm [--subtype awg] [--where title] [--n 40] [--kept]
       uv run python scripts/lit_prefilter.py sample --status excluded:led_display [--n 40]
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import html
import json
import multiprocessing
import random
import re
import sys
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from photonics_atlas.csvio import read_csv
from photonics_atlas.litpool import POOL, norm_doi, norm_title
from photonics_atlas.paths import CACHE, REGISTRY, ROOT, STAGING, input_path
from photonics_atlas.runlog import RunLog
from photonics_atlas.textnorm import ascii_fold

LIT = CACHE / "literature"
MERGED = LIT / "merged.jsonl"
PREFILTERED = LIT / "prefiltered.jsonl"
REJECTS = LIT / "prefilter_rejects.jsonl"
STATS = STAGING / "literature" / "prefilter_stats.md"
BUCKETS_YAML = ROOT / "config" / "literature" / "buckets.yaml"
SELECTION_YAML = ROOT / "config" / "literature" / "selection.yaml"

ABSTRACT_MIN = 100  # shorter abstracts (placeholders such as "International audience") count as missing
TITLE_KEY_MIN = 25  # normalized titles shorter than this never key a merge or a known-id match
_ARXIV_DOI = re.compile(r"^10\.48550/arxiv\.(.+)$", re.I)
_VER = re.compile(r"v\d+$")
_TAGS = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")


# ---------------------------------------------------------------- normalization


def clean_text(s: str | None) -> str:
    """Unescape HTML entities, strip tags (JATS / MathML / <i>), collapse whitespace."""
    t = html.unescape(s or "")
    t = _TAGS.sub(" ", t)
    return _WS.sub(" ", t).strip()


def norm_arxiv(a: str | None) -> str:
    a = (a or "").strip().lower()
    for p in ("arxiv:", "https://arxiv.org/abs/", "http://arxiv.org/abs/"):
        if a.startswith(p):
            a = a[len(p) :]
    return _VER.sub("", a)


def split_doi(d: str | None) -> tuple[str, str]:
    """Normalized DOI -> (doi, arxiv_id); an arXiv DOI (10.48550/arxiv.X) becomes an arXiv id."""
    nd = norm_doi(d)
    m = _ARXIV_DOI.match(nd)
    return ("", norm_arxiv(m.group(1))) if m else (nd, "")


def name_tokens(name: str | None) -> set[str]:
    """First and last token of an author name, ASCII-folded (covers given-family and family-given order)."""
    toks = re.findall(r"[a-z]+", ascii_fold(name or "").lower())
    toks = [t for t in toks if len(t) > 1] or toks
    return {toks[0], toks[-1]} if toks else set()


def title_key(title: str | None) -> str:
    t = norm_title(clean_text(title))
    return t if len(t) >= TITLE_KEY_MIN and len(t.split()) >= 4 else ""


def as_list(v: Any) -> list[str]:
    if v is None or v == "":
        return []
    if isinstance(v, list):
        return [str(x) for x in v if x not in (None, "")]
    return [str(v)]


def rec_dois(r: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for d in [r.get("doi"), r.get("journal_doi"), *as_list(r.get("arxiv_dois")), *as_list(r.get("alt_dois"))]:
        nd, _ = split_doi(d)
        if nd and nd not in out:
            out.append(nd)
    uid = str(r.get("uid") or "")
    if uid and ":" not in uid.split("/")[0]:
        nd, _ = split_doi(uid)
        if nd and nd not in out:
            out.append(nd)
    return out


def rec_arxiv(r: dict[str, Any]) -> str:
    a = norm_arxiv(r.get("arxiv_id"))
    if a:
        return a
    uid = str(r.get("uid") or "")
    if uid.startswith("arxiv:"):
        return norm_arxiv(uid)
    _, a = split_doi(r.get("doi"))
    return a


def work_keys(r: dict[str, Any]) -> list[str]:
    keys = [f"doi:{d}" for d in rec_dois(r)]
    a = rec_arxiv(r)
    if a:
        keys.append(f"arxiv:{a}")
    oa = str(r.get("openalex_id") or "")
    if oa:
        keys.append(f"oa:{oa.rsplit('/', 1)[-1].upper()}")
    tk = title_key(r.get("title"))
    authors = as_list(r.get("authors"))
    if tk and authors:
        keys += [f"t:{tk}|{tok}" for tok in sorted(name_tokens(authors[0]))]
    return keys


# ---------------------------------------------------------------- merge


def is_preprint(r: dict[str, Any]) -> bool:
    return r.get("type") == "preprint" or r.get("venue_type") == "repository"


def version_rank(r: dict[str, Any]) -> tuple[int, int, int, int]:
    """Higher = better primary record: journal > conference > other > preprint; then DOI, abstract, citations."""
    if is_preprint(r):
        pub = 0
    elif r.get("venue_type") == "journal":
        pub = 3
    elif r.get("venue_type") == "conference":
        pub = 2
    else:
        pub = 1
    has_doi = 1 if rec_dois(r) and not is_preprint(r) else 0
    return (
        pub,
        has_doi,
        1 if len(clean_text(r.get("abstract"))) >= ABSTRACT_MIN else 0,
        int(r.get("cited_by_count") or 0),
    )


class _UF:
    def __init__(self, n: int) -> None:
        self.p = list(range(n))

    def find(self, i: int) -> int:
        while self.p[i] != i:
            self.p[i] = self.p[self.p[i]]
            i = self.p[i]
        return i

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[max(ra, rb)] = min(ra, rb)


def group_records(recs: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    uf = _UF(len(recs))
    first: dict[str, int] = {}
    for i, r in enumerate(recs):
        for k in work_keys(r):
            if k in first:
                uf.union(first[k], i)
            else:
                first[k] = i
    groups: dict[int, list[dict[str, Any]]] = collections.defaultdict(list)
    for i, r in enumerate(recs):
        groups[uf.find(i)].append(r)
    return [groups[k] for k in sorted(groups)]


def _union(members: list[dict[str, Any]], key: str) -> list[str]:
    out: list[str] = []
    for m in members:
        for v in as_list(m.get(key)):
            if v not in out:
                out.append(v)
    return sorted(out)


def merge_group(members: list[dict[str, Any]]) -> dict[str, Any]:
    prim = max(members, key=version_rank)
    out = dict(prim)
    out["title"] = clean_text(prim.get("title"))
    dois: list[str] = []
    for m in [prim, *members]:
        for d in rec_dois(m):
            if d not in dois:
                dois.append(d)
    pd = [d for d in rec_dois(prim)] if not is_preprint(prim) else []
    out["doi"] = pd[0] if pd else (dois[0] if dois else "")
    arx = [a for a in (rec_arxiv(m) for m in [prim, *members]) if a]
    out["arxiv_id"] = arx[0] if arx else ""
    pre = [m for m in members if rec_arxiv(m) and is_preprint(m) and m.get("oa_url")]
    out["preprint_oa_url"] = str(pre[0]["oa_url"]) if pre else ""
    if not out.get("oa_url"):
        oa = [m for m in members if m.get("oa_url")]
        out["oa_url"] = str(oa[0]["oa_url"]) if oa else ""
    out["is_oa"] = any(bool(m.get("is_oa")) for m in members) or bool(out["preprint_oa_url"])
    abstracts = sorted((clean_text(m.get("abstract")) for m in members), key=len, reverse=True)
    out["abstract"] = abstracts[0] if abstracts else ""
    if not as_list(out.get("authors")):
        best = max(members, key=lambda m: len(as_list(m.get("authors"))))
        for k in ("authors", "n_authors", "last_author"):
            out[k] = best.get(k)
    if not as_list(out.get("institutions")):
        out["institutions"] = max((as_list(m.get("institutions")) for m in members), key=len)
    if not out.get("year"):
        years = [int(m["year"]) for m in members if m.get("year")]
        out["year"] = min(years) if years else None
    out["cited_by_count"] = max(int(m.get("cited_by_count") or 0) for m in members)
    for k in ("lane", "discovered_via", "seed_class", "pool_file", "refs_of_all"):
        out[k] = _union(members, k)
    out["is_review_seed"] = any(bool(m.get("is_review_seed")) for m in members)
    # per-file seed provenance, so tiers (config seed_tiers) can be told apart after the merge
    out["seed_members"] = sorted(
        (
            {"pool_file": str(m.get("pool_file") or ""), "seed_class": str(m.get("seed_class") or "")}
            for m in members
            if str(m.get("pool_file") or "").startswith("seeds_")
        ),
        key=lambda d: (d["pool_file"], d["seed_class"]),
    )
    out["alt_uids"] = sorted({str(m.get("uid")) for m in members} - {str(prim.get("uid"))})
    out["alt_dois"] = [d for d in dois if d != out["doi"]]
    out["alt_titles"] = sorted({clean_text(m.get("title")) for m in members} - {out["title"]})
    out["n_versions"] = len(members)
    return out


# ---------------------------------------------------------------- known-id exclusion


@dataclass
class KnownIndex:
    doi: dict[str, set[str]] = field(default_factory=lambda: collections.defaultdict(set))
    arxiv: dict[str, set[str]] = field(default_factory=lambda: collections.defaultdict(set))
    title: dict[str, set[str]] = field(default_factory=lambda: collections.defaultdict(set))
    sizes: dict[str, int] = field(default_factory=dict)

    def add(self, label: str, doi: str | None = None, arxiv: str | None = None, title: str | None = None) -> None:
        d, a = split_doi(doi)
        a = norm_arxiv(arxiv) or a
        if d:
            self.doi[d].add(label)
        if a:
            self.arxiv[a].add(label)
        tk = title_key(title)
        if tk:
            self.title[tk].add(label)
        self.sizes[label] = self.sizes.get(label, 0) + 1

    def match(self, r: dict[str, Any]) -> list[str]:
        hit: set[str] = set()
        for d in rec_dois(r):
            hit |= self.doi.get(d, set())
        a = rec_arxiv(r)
        if a:
            hit |= self.arxiv.get(a, set())
        for t in [r.get("title"), *as_list(r.get("alt_titles"))]:
            tk = title_key(t)
            if tk:
                hit |= self.title.get(tk, set())
        return sorted(hit)


def build_known(log: RunLog | None = None) -> KnownIndex:
    k = KnownIndex()

    def note(msg: str) -> None:
        if log:
            log.info(msg)

    src = REGISTRY / "sources.csv"
    if src.exists():
        for row in read_csv(src):
            if row.get("corpus") == "lit":  # this pipeline's own selections (S7), never "known" to it (D148)
                continue
            k.add(f"sources:{row.get('corpus') or 'other'}", row.get("doi"), row.get("arxiv_id"), row.get("title"))
    else:
        note(f"known: missing {src.relative_to(ROOT)}")
    eo, pk = input_path("eo_atlas"), input_path("pk_atlas")
    for label, p in (
        ("eo_papers", eo / "data" / "papers.csv"),
        ("eo_candidates", eo / "data" / "candidates.csv"),
        ("pk_papers", pk / "data" / "papers.csv"),
        ("pk_cache_list", pk / "outputs" / "cache_list.csv"),
    ):
        if p.exists():
            for row in read_csv(p):
                k.add(label, row.get("doi"), row.get("arxiv_id"), row.get("title"))
        else:
            note(f"known: missing input {label}")
    ofc = input_path("ofc_metadata")
    if ofc.exists():
        for row in json.loads(ofc.read_text(encoding="utf-8")):
            if row.get("record_kind") == "presentation" and row.get("presentation_title"):
                k.add("ofc2026", title=row["presentation_title"])
    else:
        note("known: missing input ofc_metadata")
    return k


# ---------------------------------------------------------------- pool reading


def read_pool(pool: Path, stats: collections.Counter[str]) -> Iterator[dict[str, Any]]:
    """Every *.jsonl under the pool dir (*.part files are in-progress and skipped); a torn last line is skipped."""
    for p in sorted(pool.glob("*.jsonl")):
        prefix = p.stem.split("_", 1)[0]
        with p.open(encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    stats["bad_lines"] += 1
                    continue
                if not isinstance(r, dict) or not (r.get("title") or r.get("uid")):
                    stats["bad_lines"] += 1
                    continue
                r.setdefault("lane", prefix)
                if not r.get("lane"):
                    r["lane"] = prefix
                r["pool_file"] = p.name
                stats[f"raw_lane:{as_list(r['lane'])[0]}"] += 1
                stats[f"raw_file:{p.name}"] += 1
                yield r


def merge_pool(
    records: Iterable[dict[str, Any]], drop_types: set[str], known: KnownIndex | None
) -> tuple[list[dict[str, Any]], collections.Counter[str]]:
    st: collections.Counter[str] = collections.Counter()
    keep: list[dict[str, Any]] = []
    for r in records:
        st["raw"] += 1
        t = str(r.get("type") or "").lower()
        if t in drop_types:
            st[f"dropped_type:{t}"] += 1
            continue
        keep.append(r)
    merged = []
    for g in group_records(keep):
        m = merge_group(g)
        if len(g) > 1:
            st["groups_multi"] += 1
            st["duplicates_merged"] += len(g) - 1
            lanes = sorted({as_list(x.get("lane"))[0] for x in g if as_list(x.get("lane"))})
            if len(lanes) > 1:
                st["groups_cross_lane"] += 1
            if any(is_preprint(x) for x in g) and any(not is_preprint(x) for x in g):
                st["groups_preprint_published"] += 1
        m["known_in"] = known.match(m) if known else []
        merged.append(m)
    merged.sort(key=lambda m: str(m.get("uid")))
    st["merged"] = len(merged)
    return merged, st


# ---------------------------------------------------------------- buckets


_UPPER_ESC = re.compile(r"\\[A-Z]")


def _rx(patterns: list[str] | str | None) -> re.Pattern[str] | None:
    """Compile a pattern list for lowercased text: the source is lowercased (2x faster than re.I in CPython), so
    upper-case escapes (\\B, \\D, \\S, \\W, \\A, \\Z) are not allowed in buckets.yaml."""
    pats = [patterns] if isinstance(patterns, str) else list(patterns or [])
    if not pats:
        return None
    src = "|".join(f"(?:{p})" for p in pats)
    if _UPPER_ESC.search(src) or "\\\\" in src:
        raise ValueError(f"upper-case or doubled backslash escape in buckets.yaml: {src[:80]}")
    return re.compile(src.lower())


def _req(p: str) -> re.Pattern[str]:
    rx = _rx(p)
    assert rx is not None
    return rx


@dataclass
class Subtype:
    name: str
    title: re.Pattern[str] | None
    abstract: re.Pattern[str] | None


@dataclass
class ClassRules:
    name: str
    subtypes: list[Subtype]
    title_any: re.Pattern[str] | None
    abstract_any: re.Pattern[str] | None
    require: re.Pattern[str] | None
    exclude_title: re.Pattern[str] | None
    require_all: bool = False  # False: a title hit on a specific subtype (not other / _class) skips `require`


GENERIC_SUBTYPES = {"other", "_class"}


@dataclass
class Exclusion:
    name: str
    title: re.Pattern[str] | None
    unless_title: re.Pattern[str] | None
    unless_text: re.Pattern[str] | None
    unless_class_title_hit: bool
    ignore_classes: set[str]
    require_no_text: re.Pattern[str] | None
    require_abstract: bool


@dataclass
class Buckets:
    classes: list[ClassRules]
    exclusions: list[Exclusion]
    platforms: dict[str, re.Pattern[str]]
    cues: dict[str, re.Pattern[str]]
    non_paper: re.Pattern[str]
    groups: dict[str, str]  # class -> group
    caps: dict[str, Any]
    seed_tiers: dict[str, Any]
    drop_types: set[str]
    strict_files: tuple[str, ...] = ()


def is_strict(r: dict[str, Any], b: Buckets) -> bool:
    """True when every pool file of the record starts with a `strict_files` prefix (e.g. off-topic-prone arXiv sets)."""
    files = as_list(r.get("pool_file"))
    return bool(files and b.strict_files) and all(f.startswith(b.strict_files) for f in files)


def load_buckets(path: Path = BUCKETS_YAML) -> Buckets:
    cfg = yaml.safe_load(path.read_text(encoding="utf-8"))
    ctx = cfg.get("context_default") or []
    classes = []
    for cname, c in cfg["classes"].items():
        subs, tall, aall = [], [], []
        for sname, s in c["subtypes"].items():
            tp = list(s.get("title") or [])
            ap = list(s.get("abstract") or tp)
            subs.append(Subtype(sname, _rx(tp), _rx(ap)))
            tall += tp
            aall += ap
        req = c.get("require", ctx)  # absent -> context_default; [] -> no check
        classes.append(
            ClassRules(
                cname,
                subs,
                _rx(tall),
                _rx(aall),
                _rx(req),
                _rx(c.get("exclude_title")),
                c.get("require_scope") == "all",
            )
        )
    excl = []
    for ename, e in (cfg.get("exclusions") or {}).items():
        excl.append(
            Exclusion(
                ename,
                _rx(e.get("title")),
                _rx(e.get("unless_title")),
                _rx(e.get("unless_text")),
                bool(e.get("unless_class_title_hit")),
                set(e.get("ignore_classes") or []),
                _rx(e.get("require_no_text")),
                bool(e.get("require_abstract")),
            )
        )
    groups = {c: g for g, cs in cfg["groups"].items() for c in cs}
    plats = {k: _req(v) for k, v in cfg["platforms"].items()}
    cues = {k: _req(v) for k, v in cfg["cues"].items()}
    return Buckets(
        classes,
        excl,
        plats,
        cues,
        _req(cfg["non_paper_title"]),
        groups,
        dict(cfg["caps"]),
        dict(cfg["seed_tiers"]),
        set(cfg.get("drop_types") or []),
        tuple(cfg.get("strict_files") or []),
    )


@dataclass
class Hit:
    cls: str
    subtypes: list[str]
    where: str  # title | abstract | seed
    n_title: int
    n_abstract: int
    pos: int  # first title match position (specific subtypes first; large when none)
    specific: bool = False  # a specific subtype (not other / _class) hit the title

    def order(self) -> tuple[int, int, int, int, int]:
        strength = {"title": 2, "abstract": 1, "seed": 0}[self.where]
        return (-strength, -int(self.specific), self.pos, -self.n_title, -self.n_abstract)


def class_hits(
    title: str, abstract: str, b: Buckets, seed_classes: Iterable[str] = (), strict: bool = False
) -> list[Hit]:
    """Regex class hits, best first. Seed classes (seeds lane) count as the weakest hit when no regex hits that class.
    strict (records only from `strict_files`): a class needs a title hit, and `require` applies to every hit."""
    title, abstract = title.lower(), abstract.lower()
    text = f"{title}. {abstract}"
    hits: list[Hit] = []
    for c in b.classes:
        t_any = bool(c.title_any and c.title_any.search(title))
        if strict and not t_any:
            continue
        a_any = bool(abstract and c.abstract_any and c.abstract_any.search(abstract))
        if not (t_any or a_any):
            continue
        if c.exclude_title and c.exclude_title.search(title):
            continue
        subs, nt, na, pos, gpos, specific = [], 0, 0, 10**6, 10**6, False
        for s in c.subtypes:
            mt = s.title.search(title) if (t_any and s.title) else None
            ma = s.abstract.search(abstract) if (a_any and s.abstract) else None
            if mt:
                nt += 1
                if s.name in GENERIC_SUBTYPES:
                    gpos = min(gpos, mt.start())
                else:
                    specific = True
                    pos = min(pos, mt.start())
            if ma:
                na += 1
            if (mt or ma) and s.name != "_class":
                subs.append(s.name)
        if c.require and not c.require.search(text) and (c.require_all or strict or not specific):
            continue
        if nt or na:
            hits.append(Hit(c.name, subs, "title" if nt else "abstract", nt, na, pos if specific else gpos, specific))
    have = {h.cls for h in hits}
    known_cls = {c.name for c in b.classes}
    for sc in seed_classes:
        cl = sc.split(".", 1)[0]
        if cl in known_cls and cl not in have:
            sub = [sc.split(".", 1)[1]] if "." in sc else []
            hits.append(Hit(cl, sub, "seed", 0, 0, 10**6))
            have.add(cl)
    hits.sort(key=Hit.order)
    return hits


def exclusion(title: str, abstract: str, hits: list[Hit], b: Buckets) -> str:
    title, abstract = title.lower(), abstract.lower()
    text = f"{title}. {abstract}"
    for e in b.exclusions:
        if not (e.title and e.title.search(title)):
            continue
        if e.unless_title and e.unless_title.search(title):
            continue
        if e.unless_text and e.unless_text.search(text):
            continue
        if e.unless_class_title_hit and any(h.where == "title" and h.cls not in e.ignore_classes for h in hits):
            continue
        if e.require_abstract and len(abstract) < ABSTRACT_MIN:
            continue
        if e.require_no_text and e.require_no_text.search(text):
            continue
        return e.name
    return ""


def platform_hits(title: str, abstract: str, b: Buckets) -> list[str]:
    text = f"{title}. {abstract}".lower()
    return [k for k, rx in b.platforms.items() if rx.search(text)]


def is_conference(r: dict[str, Any]) -> bool:
    return r.get("venue_type") == "conference" or "proceed" in str(r.get("type") or "").lower()


def rule_score(
    title: str,
    abstract: str,
    best: Hit,
    plats: list[str],
    is_review: bool,
    conference: bool,
    seed_bonus: dict[str, int],
    b: Buckets,
) -> tuple[int, dict[str, int], list[str], int]:
    """0-10 provisional score from title / abstract cues; returns (score, components, flags, n distinct numbers)."""
    c: dict[str, int] = {}
    flags: list[str] = []
    title, abstract = title.lower(), abstract.lower()
    text = f"{title}. {abstract}"
    has_abs = len(abstract) >= ABSTRACT_MIN
    c["title_class"] = 4 if best.where == "title" else 1
    if best.where == "title" and best.n_abstract:
        c["abstract_support"] = 1
    exp = bool(abstract and b.cues["experimental"].search(abstract))
    if exp:
        c["experimental"] = 2
    nq = len({m.group(0).lower() for m in b.cues["quantitative"].finditer(text)})
    if nq:
        c["quantitative"] = 2 if nq >= 2 else 1
    if plats or b.cues["integrated"].search(text):
        c["integrated"] = 1
    if is_review or b.cues["review_title"].search(title):
        c["review"] = -4
    if has_abs and not exp and b.cues["simulation"].search(text):
        c["sim_only"] = -3
    if not has_abs:
        flags.append("abstract_missing")
        if not conference:
            c["abstract_missing"] = -1
    c.update({k: v for k, v in seed_bonus.items() if v})
    return max(0, min(10, sum(c.values()))), c, flags, nq


@dataclass
class SeedInfo:
    tier: str  # "A" | "B" | ""
    lane_found: bool  # some non-seed pool file (journals / conferences / arxiv) also holds the work
    classes_a: list[str]
    multi: bool  # tier B cited by reviews of >= 2 classes or by >= 2 reviews


def seed_info(r: dict[str, Any], b: Buckets) -> SeedInfo:
    """Seed tiers (D131 as revised 2026-10-21): A = curated local seeds, B = review references / forward citations."""
    t = b.seed_tiers
    a_pre, b_pre = tuple(t["a_files"]), tuple(t["b_files"])
    seed_pre = str(t.get("seed_prefix", "seeds_"))
    files = as_list(r.get("pool_file"))
    lane_found = any(not f.startswith(seed_pre) for f in files)
    mem = r.get("seed_members") or []
    a_cls = sorted({m["seed_class"] for m in mem if m["pool_file"].startswith(a_pre) and m["seed_class"]})
    is_a = any(f.startswith(a_pre) for f in files)
    is_b = any(f.startswith(b_pre) for f in files)
    b_cls = {m["seed_class"] for m in mem if m["pool_file"].startswith(b_pre) and m["seed_class"]}
    multi = is_b and (len(b_cls) >= 2 or len(as_list(r.get("refs_of_all"))) >= 2)
    return SeedInfo("A" if is_a else "B" if is_b else "", lane_found, a_cls, multi)


def analyse(r: dict[str, Any], b: Buckets) -> dict[str, Any]:
    """Status + class hits + score for one merged record (pure; no I/O)."""
    title = clean_text(r.get("title"))
    abstract = clean_text(r.get("abstract"))
    si = seed_info(r, b)
    t = b.seed_tiers
    b_only = si.tier == "B" and not si.lane_found
    out: dict[str, Any] = {"status": "", "seed": si.tier == "A", "seed_tier": si.tier, "lane_found": si.lane_found}
    if r.get("known_in"):
        out["status"] = "known"
        return out
    if r.get("is_review_seed"):
        out["status"] = "review_seed"
        return out
    if b.non_paper.search(title.lower()) or len(title) < 8:
        out["status"] = "non_paper"
        return out
    hits = class_hits(title, abstract, b, si.classes_a if si.tier == "A" else (), strict=is_strict(r, b))
    rule = exclusion(title, abstract, hits, b)
    if rule:
        out["status"] = f"excluded:{rule}"
        out["hits"] = hits
        return out
    if not hits:
        out["status"] = "no_class_hit"
        return out
    if b_only and hits[0].where != "title":
        out["status"] = "seed_b_no_title_hit"
        out["hits"] = hits
        return out
    if b_only and int(r.get("year") or 0) < int(t["b_old_year"]):
        tl, al = title.lower(), abstract.lower()
        if not (b.cues["experimental"].search(al) or b.cues["quantitative"].search(f"{tl}. {al}")):
            out["status"] = f"seed_b_pre{t['b_old_year']}_no_cue"
            out["hits"] = hits
            return out
    bonus = {
        "seed_a": int(t["a_bonus"]) if si.tier == "A" else 0,
        "seed_b": int(t["b_bonus"]) if si.tier == "B" else 0,
        "seed_b_multi": int(t["b_multi_bonus"]) if si.tier == "B" and si.multi else 0,
    }
    plats = platform_hits(title, abstract, b)
    is_review = str(r.get("type") or "").lower() == "review"
    score, comp, flags, nq = rule_score(title, abstract, hits[0], plats, is_review, is_conference(r), bonus, b)
    out.update(status="candidate", hits=hits, platforms=plats, score=score, components=comp, flags=flags, n_quant=nq)
    return out


def hit_labels(hits: list[Hit]) -> list[str]:
    out: list[str] = []
    for h in hits:
        out += [f"{h.cls}.{s}" for s in h.subtypes] or [h.cls]
    return out


def load_budget(path: Path = SELECTION_YAML) -> dict[str, int]:
    return {k: int(v) for k, v in yaml.safe_load(path.read_text(encoding="utf-8"))["budget"].items()}


def apply_caps(cands: list[dict[str, Any]], budget: dict[str, int], b: Buckets) -> dict[str, dict[str, int]]:
    """Mark score_keep / cap_rank in place; returns per-class {candidates, kept, cap, seeds, below_min}.

    Rank inside a class: seeds first, rule score, title hit, abstract present, distinct numbers in title + abstract
    (capped at 8), year (newer first), uid."""
    cap_min, mult = int(b.caps["cap_min"]), float(b.caps["cap_mult"])
    min_score = int(b.caps.get("min_rule_score", 0))
    weak_min = int(b.caps.get("weak_min_rule_score", min_score))
    by: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for r in cands:
        by[r["best_class"]].append(r)
    eff: dict[str, dict[str, int]] = {}
    for cls in sorted(set(budget) | set(by)):
        rows = by.get(cls, [])
        cap = max(cap_min, int(round(mult * budget.get(cls, 0))))
        rows.sort(
            key=lambda r: (
                -int(r["seed"]),
                -r["rule_score"],
                -int(r["hit_where"] == "title"),
                -int("abstract_missing" not in r["flags"]),
                -min(int(r.get("n_quant") or 0), 8),
                -(r.get("year") or 0),
                str(r["uid"]),
            )
        )
        kept = seeds = below = 0
        for i, r in enumerate(rows):
            r["cap_rank"] = i + 1
            floor = min_score if r["hit_where"] == "title" else weak_min
            ok = r["seed"] or (kept < cap and r["rule_score"] >= floor)
            if not r["seed"] and r["rule_score"] < floor:
                below += 1
            r["score_keep"] = bool(ok)
            if ok:
                kept += 1
                seeds += int(r["seed"])
        eff[cls] = {"candidates": len(rows), "kept": kept, "cap": cap, "seeds": seeds, "below_min": below}
    return eff


# ---------------------------------------------------------------- stats


def _pct(a: int, n: int) -> str:
    return f"{100.0 * a / n:.1f}" if n else "N/A"


def write_stats(
    path: Path,
    merge_st: collections.Counter[str],
    merged: list[dict[str, Any]],
    status: collections.Counter[str],
    cands: list[dict[str, Any]],
    eff: dict[str, dict[str, int]],
    budget: dict[str, int],
    b: Buckets,
    known: KnownIndex | None,
) -> str:
    today = dt.date.today().isoformat()
    L: list[str] = [
        "# Literature prefilter statistics (DevLog-006 S2)",
        "",
        f"Generated {today} by `scripts/lit_prefilter.py` from `cache/literature/pool/*.jsonl` (git-ignored). Counts only.",
        "Re-run over the growing pool rewrites this file.",
        "",
        "## Pool by lane (raw records)",
        "",
        "| lane | pool files | raw records |",
        "|---|---|---|",
    ]
    lanes = sorted({k.split(":", 1)[1] for k in merge_st if k.startswith("raw_lane:")})
    for ln in lanes:
        nf = sum(1 for k in merge_st if k.startswith("raw_file:") and k.split(":", 1)[1].split("_", 1)[0] == ln)
        L.append(f"| {ln} | {nf} | {merge_st[f'raw_lane:{ln}']} |")
    L += [f"| total | {sum(1 for k in merge_st if k.startswith('raw_file:'))} | {merge_st['raw']} |", ""]
    L += [
        "## Merge",
        "",
        "| step | n |",
        "|---|---|",
        f"| raw records | {merge_st['raw']} |",
        f"| unreadable lines skipped | {merge_st['bad_lines']} |",
    ]
    for k in sorted(k for k in merge_st if k.startswith("dropped_type:")):
        L.append(f"| dropped type {k.split(':', 1)[1]} | {merge_st[k]} |")
    L += [
        f"| works after merge | {merge_st['merged']} |",
        f"| duplicate records merged | {merge_st['duplicates_merged']} |",
        f"| works with more than one record | {merge_st['groups_multi']} |",
        f"| of which across lanes | {merge_st['groups_cross_lane']} |",
        f"| of which preprint + published version | {merge_st['groups_preprint_published']} |",
        "",
        "## Known-id exclusion (work already in a local corpus; a work can be in several)",
        "",
        "| corpus | index entries | works matched |",
        "|---|---|---|",
    ]
    kc: collections.Counter[str] = collections.Counter(lbl for m in merged for lbl in m.get("known_in") or [])
    for lbl in sorted(set(kc) | set(known.sizes if known else {})):
        L.append(f"| {lbl} | {known.sizes.get(lbl, 0) if known else 'N/A'} | {kc[lbl]} |")
    L += [f"| works excluded as known | | {status['known']} |", ""]
    L += ["## Prefilter status (works)", "", "| status | n |", "|---|---|"]
    for k, v in sorted(status.items(), key=lambda kv: (-kv[1], kv[0])):
        L.append(f"| {k} | {v} |")
    L += ["", f"Candidates (class hit, not known / excluded): {len(cands)}.", ""]
    kept = [r for r in cands if r["score_keep"]]
    L += [
        "## Per class (best class; cap = max(cap_min, cap_mult x budget))",
        "",
        f"cap_min {b.caps['cap_min']}, cap_mult {b.caps['cap_mult']}, min_rule_score {b.caps.get('min_rule_score')} "
        f"(abstract-only hits {b.caps.get('weak_min_rule_score', b.caps.get('min_rule_score'))}), "
        f"seed tiers: A +{b.seed_tiers['a_bonus']} (always kept), B +{b.seed_tiers['b_bonus']} "
        f"(+{b.seed_tiers['b_multi_bonus']} multi-review, within cap). Any-hit = works with this class among their hits. "
        "Kept by source: A = tier-A seed; B only = tier-B seed found by no lane; lanes = found by a harvest lane "
        "(lanes+B = of which also a tier-B seed).",
        "",
        "| group | class | budget | any-hit | best-class candidates | title-hit | below min score | cap | kept | "
        "kept A | kept B only | kept lanes | kept lanes+B |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]

    def src(r: dict[str, Any]) -> str:
        if r.get("seed_tier") == "A":
            return "A"
        if not r.get("lane_found"):
            return "B"
        return "LB" if r.get("seed_tier") == "B" else "L"

    ks: collections.Counter[tuple[str, str]] = collections.Counter((r["best_class"], src(r)) for r in kept)
    anyhit: collections.Counter[str] = collections.Counter(
        c for r in cands for c in {h.split(".")[0] for h in r["class_hits"]}
    )
    th: collections.Counter[str] = collections.Counter(r["best_class"] for r in cands if r["hit_where"] == "title")
    for cls in sorted(eff, key=lambda c: (b.groups.get(c, "Z"), c)):
        e = eff[cls]
        L.append(
            f"| {b.groups.get(cls, '')} | {cls} | {budget.get(cls, 0)} | {anyhit[cls]} | {e['candidates']} | {th[cls]} | "
            f"{e['below_min']} | {e['cap']} | {e['kept']} | {ks[(cls, 'A')]} | {ks[(cls, 'B')]} | "
            f"{ks[(cls, 'L')] + ks[(cls, 'LB')]} | {ks[(cls, 'LB')]} |"
        )
    tot = collections.Counter(src(r) for r in kept)
    L += [
        f"| | total | {sum(budget.values())} | | {len(cands)} | {sum(th.values())} | | | {len(kept)} | "
        f"{tot['A']} | {tot['B']} | {tot['L'] + tot['LB']} | {tot['LB']} |",
        "",
    ]
    L += [
        "## Kept per subtype (kept works whose best class has this subtype hit)",
        "",
        "| class.subtype | kept | candidates |",
        "|---|---|---|",
    ]
    sk: collections.Counter[str] = collections.Counter()
    sc: collections.Counter[str] = collections.Counter()
    for r in cands:
        for lbl in r["class_hits"]:
            if lbl.split(".")[0] == r["best_class"]:
                sc[lbl] += 1
                if r["score_keep"]:
                    sk[lbl] += 1
    for lbl in sorted(sc, key=lambda x: (b.groups.get(x.split(".")[0], "Z"), x)):
        L.append(f"| {lbl} | {sk[lbl]} | {sc[lbl]} |")
    L += ["", "## Kept per group (scoring batches)", "", "| group | kept |", "|---|---|"]
    gk: collections.Counter[str] = collections.Counter(b.groups.get(r["best_class"], "") for r in kept)
    for g in sorted(gk):
        L.append(f"| {g} | {gk[g]} |")
    L += ["", "## Per-lane contribution and abstract coverage (a work counts for every lane that found it)", ""]
    L += [
        "| lane | works merged | abstract % (merged) | candidates | kept | abstract % (kept) | only this lane (kept) |",
        "|---|---|---|---|---|---|---|",
    ]
    lane_m: collections.Counter[str] = collections.Counter()
    lane_ma: collections.Counter[str] = collections.Counter()
    for m in merged:
        ha = len(clean_text(m.get("abstract"))) >= ABSTRACT_MIN
        for ln in as_list(m.get("lane")):
            lane_m[ln] += 1
            lane_ma[ln] += int(ha)
    lane_c: collections.Counter[str] = collections.Counter(ln for r in cands for ln in r["lane"])
    lane_k: collections.Counter[str] = collections.Counter(ln for r in kept for ln in r["lane"])
    lane_ka: collections.Counter[str] = collections.Counter(
        ln for r in kept if "abstract_missing" not in r["flags"] for ln in r["lane"]
    )
    lane_only: collections.Counter[str] = collections.Counter(r["lane"][0] for r in kept if len(r["lane"]) == 1)
    for ln in sorted(lane_m):
        L.append(
            f"| {ln} | {lane_m[ln]} | {_pct(lane_ma[ln], lane_m[ln])} | {lane_c[ln]} | {lane_k[ln]} | "
            f"{_pct(lane_ka[ln], lane_k[ln])} | {lane_only[ln]} |"
        )
    nm_a = sum(1 for m in merged if len(clean_text(m.get("abstract"))) >= ABSTRACT_MIN)
    nk_a = sum(1 for r in kept if "abstract_missing" not in r["flags"])
    L += [
        f"| all | {len(merged)} | {_pct(nm_a, len(merged))} | {len(cands)} | {len(kept)} | {_pct(nk_a, len(kept))} | |",
        "",
        f"Abstract = at least {ABSTRACT_MIN} characters after tag stripping.",
        "",
        "## Rule-score distribution (kept)",
        "",
        "| score | kept | candidates |",
        "|---|---|---|",
    ]
    for s in range(10, -1, -1):
        L.append(
            f"| {s} | {sum(1 for r in kept if r['rule_score'] == s)} | {sum(1 for r in cands if r['rule_score'] == s)} |"
        )
    L.append("")
    text = "\n".join(L)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return text


# ---------------------------------------------------------------- steps


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".part")
    n = 0
    with tmp.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            n += 1
    tmp.replace(path)
    return n


def step_merge(log: RunLog, b: Buckets, dry: bool) -> tuple[list[dict[str, Any]], collections.Counter[str], KnownIndex]:
    rst: collections.Counter[str] = collections.Counter()
    recs = list(read_pool(POOL, rst))
    log.info(f"pool: {len(recs)} records from {sum(1 for k in rst if k.startswith('raw_file:'))} files")
    known = build_known(log)
    log.info("known index: " + ", ".join(f"{k} {v}" for k, v in sorted(known.sizes.items())))
    merged, st = merge_pool(recs, b.drop_types, known)
    st.update(rst)
    log.info(
        f"merged: {st['merged']} works, {st['duplicates_merged']} duplicates merged, "
        f"known {sum(1 for m in merged if m['known_in'])}"
    )
    log.event("merge", raw=st["raw"], merged=st["merged"], duplicates=st["duplicates_merged"])
    if not dry:
        write_jsonl(MERGED, merged)
        (LIT / "merge_stats.json").write_text(json.dumps(dict(st), indent=1, sort_keys=True), encoding="utf-8")
        log.info(f"wrote {MERGED.relative_to(ROOT)}")
    return merged, st, known


_WB: Buckets | None = None


def _init_worker() -> None:
    global _WB
    _WB = load_buckets()


def _analyse_worker(r: dict[str, Any]) -> dict[str, Any]:
    assert _WB is not None
    return analyse(r, _WB)


def analyse_all(merged: list[dict[str, Any]], b: Buckets, jobs: int) -> list[dict[str, Any]]:
    """analyse() over all records; jobs > 1 uses worker processes (each loads buckets.yaml itself)."""
    if jobs <= 1 or len(merged) < 2000:
        return [analyse(m, b) for m in merged]
    with multiprocessing.get_context("spawn").Pool(jobs, initializer=_init_worker) as pool:
        return pool.map(_analyse_worker, merged, chunksize=500)


def prefilter(
    merged: list[dict[str, Any]], b: Buckets, budget: dict[str, int], jobs: int = 1
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], collections.Counter[str], dict[str, dict[str, int]]]:
    status: collections.Counter[str] = collections.Counter()
    cands: list[dict[str, Any]] = []
    rejects: list[dict[str, Any]] = []
    for m, a in zip(merged, analyse_all(merged, b, jobs), strict=True):
        status[a["status"]] += 1
        if a["status"] != "candidate":
            rej = {"uid": m["uid"], "status": a["status"], "title": m.get("title"), "known_in": m.get("known_in") or []}
            if a.get("hits"):
                rej["class_hits"] = hit_labels(a["hits"])
            rejects.append(rej)
            continue
        hits: list[Hit] = a["hits"]
        r = dict(m)
        r.update(
            title=clean_text(m.get("title")),
            best_class=hits[0].cls,
            group=b.groups.get(hits[0].cls, ""),
            hit_where=hits[0].where,
            class_hits=hit_labels(hits),
            class_hit_where={h.cls: h.where for h in hits},
            platform_hits=a["platforms"],
            rule_score=a["score"],
            rule_components=a["components"],
            n_quant=a["n_quant"],
            flags=a["flags"],
            seed=a["seed"],
            seed_tier=a["seed_tier"],
            lane_found=a["lane_found"],
            lane=as_list(m.get("lane")),
        )
        cands.append(r)
    eff = apply_caps(cands, budget, b)
    return cands, rejects, status, eff


def step_prefilter(
    log: RunLog,
    b: Buckets,
    dry: bool,
    merged: list[dict[str, Any]] | None = None,
    merge_st: collections.Counter[str] | None = None,
    known: KnownIndex | None = None,
    jobs: int = 1,
) -> None:
    if merged is None:
        if not MERGED.exists():
            raise SystemExit(f"missing {MERGED.relative_to(ROOT)}; run the merge step first")
        merged = [json.loads(x) for x in MERGED.read_text(encoding="utf-8").splitlines() if x.strip()]
        sp = LIT / "merge_stats.json"
        merge_st = collections.Counter(json.loads(sp.read_text())) if sp.exists() else collections.Counter()
    budget = load_budget()
    cands, rejects, status, eff = prefilter(merged, b, budget, jobs)
    kept = sum(1 for r in cands if r["score_keep"])
    log.info(f"prefilter: {dict(status)}; candidates {len(cands)}, kept for scoring {kept}")
    for cls, e in sorted(eff.items()):
        log.info(f"  {cls:20s} cand {e['candidates']:6d} cap {e['cap']:4d} kept {e['kept']:4d} seeds {e['seeds']}")
    log.event("prefilter", candidates=len(cands), kept=kept, status_counts=dict(status), caps=eff)
    if dry:
        return
    cands.sort(key=lambda r: (r["group"], r["best_class"], r["cap_rank"]))
    write_jsonl(PREFILTERED, cands)
    write_jsonl(REJECTS, rejects)
    write_stats(STATS, merge_st or collections.Counter(), merged, status, cands, eff, budget, b, known)
    log.info(f"wrote {PREFILTERED.relative_to(ROOT)}, {REJECTS.relative_to(ROOT)}, {STATS.relative_to(ROOT)}")


def step_sample(args: argparse.Namespace) -> None:
    rng = random.Random(args.seed)
    if args.status:
        rows = [json.loads(x) for x in REJECTS.read_text(encoding="utf-8").splitlines() if x.strip()]
        rows = [r for r in rows if r["status"] == args.status]
        pick = rng.sample(rows, min(args.n, len(rows)))
        print(f"# {args.status}: {len(rows)}")
        for r in pick:
            print(f"- {r['title']}  [{','.join(r.get('class_hits') or [])}]")
        return
    rows = [json.loads(x) for x in PREFILTERED.read_text(encoding="utf-8").splitlines() if x.strip()]
    sel = []
    for r in rows:
        if args.best and r["best_class"] != args.cls:
            continue
        lbls = [x for x in r["class_hits"] if x.split(".")[0] == args.cls]
        if not lbls:
            continue
        if args.subtype and f"{args.cls}.{args.subtype}" not in lbls:
            continue
        if args.where and r["class_hit_where"].get(args.cls) != args.where:
            continue
        if args.kept and not r["score_keep"]:
            continue
        sel.append(r)
    pick = rng.sample(sel, min(args.n, len(sel)))
    print(f"# {args.cls}{'.' + args.subtype if args.subtype else ''} where={args.where or 'any'}: {len(sel)}")
    for r in sorted(pick, key=lambda r: -r["rule_score"]):
        print(f"- [{r['rule_score']}] {r['title']}  ({r['venue']} {r['year']}) [{','.join(r['class_hits'][:4])}]")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", nargs="?", default="all", choices=["all", "merge", "prefilter", "sample"])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--cls", default="")
    ap.add_argument("--subtype", default="")
    ap.add_argument("--where", default="", choices=["", "title", "abstract", "seed"])
    ap.add_argument("--status", default="")
    ap.add_argument("--best", action="store_true", help="sample: only records whose best class is --cls")
    ap.add_argument("--kept", action="store_true")
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--jobs", type=int, default=4, help="worker processes for the regex pass (default 4)")
    args = ap.parse_args()
    if args.step == "sample":
        if not (args.cls or args.status):
            ap.error("sample needs --cls or --status")
        step_sample(args)
        return 0
    b = load_buckets()
    with RunLog("lit_prefilter", dry_run=args.dry_run) as log:
        if args.step in ("all", "merge"):
            merged, st, known = step_merge(log, b, args.dry_run)
            if args.step == "all":
                step_prefilter(log, b, args.dry_run, merged, st, known, jobs=args.jobs)
        else:
            step_prefilter(log, b, args.dry_run, known=build_known(log), jobs=args.jobs)
    return 0


if __name__ == "__main__":
    sys.exit(main())
