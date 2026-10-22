"""Literature scouting lane L4 (DevLog-006 S1): local seeds, per-class review seeds and their reference lists.

Subcommands (all resumable; raw API responses cached under cache/literature/seeds/, pool files under
cache/literature/pool/seeds_*.jsonl written atomically via <file>.part):

  local         seeds from local files (no discovery): blog harvest OA photonics rows in neither atlas, taxonomy
                report section 5 seed table, EO atlas candidates whose title names a non-modulator component.
                DOIs / arXiv ids -> OpenAlex singleton gets (free); titles without ids -> Crossref query.bibliographic
                (free; accepted only on a near-exact normalized-title match, ratio recorded) -> OpenAlex get.
                -> seeds_local.jsonl (+ cache/literature/seeds/local_unresolved.jsonl)
  anchor-reviews  the 200 most-cited 2018-2026 works citing each `anchors:` landmark paper (filter cites:W,
                filter-only, $0.0001 each); review-like titles cached and printed (--show) for manual choice.
  find-reviews  Crossref review queries listed under `queries:` in config/literature/seed_reviews.yaml; hits cached
                in cache/literature/seeds/review_candidates/ and printed for manual choice. `--openalex-search`
                runs `openalex_queries:` (title.search, most cited first; $0.001 each, lane cap 20, counted on disk).
  reviews       chosen reviews (`reviews:` in the YAML) -> singleton gets with referenced_works -> seeds_reviews.jsonl
                (is_review_seed true); referenced works fetched with `openalex_id:W1|...` filter pages (100 ids,
                filter-only) -> seeds_refs_<class>.jsonl (discovered_via refs_of:<review doi>, seed_class).
  cites         optional forward citations for `cites:` entries (filter cites:W, newest first, <= 2 pages each)
                -> seeds_cites_<class>.jsonl.

Usage: uv run python scripts/lit_seeds.py {local|find-reviews|anchor-reviews|reviews|cites} [--dry-run] [--only CLASS]
"""

from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import json
import re
import sys
import urllib.error
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import yaml

from photonics_atlas import litfetch, litpool
from photonics_atlas.paths import CACHE, ROOT, inputs_root
from photonics_atlas.runlog import RunLog

LANE = "seeds"
OA = "https://api.openalex.org/works"
CR = "https://api.crossref.org/works"
SEEDS = CACHE / "literature" / "seeds"
CONFIG = ROOT / "config" / "literature" / "seed_reviews.yaml"
SELECT_REFS = litpool.OPENALEX_SELECT + ",referenced_works"
BLOG_CSV = ROOT / "DevLog" / "research" / "blog_harvest" / "candidates.csv"
TAXONOMY_MD = ROOT / "DevLog" / "research" / "2026-10-20-component-atlas-taxonomy.md"
OA_CLASSES = {"arxiv", "optica_oa_journal", "nature_comms_or_lsa", "other_oa_journal", "other_oa_repository"}
TITLE_MATCH_MIN = 0.93
OPENALEX_SEARCH_CAP = 20
BATCH_IDS = 100

DOI_RE = re.compile(r"10\.\d{4,9}/[^\s;,|]+", re.I)
ARXIV_RE = re.compile(r"arXiv:\s*(\d{4}\.\d{4,5})", re.I)
OPTICA_URI = re.compile(r"^([a-z]+)-(\d+)-(\d+)-(\d+)$")

# EO atlas candidates: a title that names a non-modulator component. A title that also says "modulat" or
# "transduc" must name a strongly non-modulator device (laser, detector, receiver, amplifier, isolator, comb, WDM, coupler).
EO_COMPONENT = re.compile(
    r"\blaser|\bDFB\b|photodetector|photodiode|\bPD\b|detector|receiver|transceiver|amplifier|\bSOA\b|isolator|"
    r"circulator|coupler|wire bond|multiplex|\bWDM\b|\bAWG\b|arrayed waveguide|filter|resonator|microring|\bcavity|"
    r"\bcomb\b|second[- ]harmonic|frequency conversion|crossing|splitter|polarization|low[- ]loss|quality factor|"
    r"packag|switch|quantum computing|\breview\b",
    re.I,
)
EO_STRONG = re.compile(
    r"\blaser|\bDFB\b|photodetector|photodiode|\bPD\b|receiver|transceiver|amplifier|\bSOA\b|isolator|circulator|"
    r"\bcomb\b|\bWDM\b|multiplex|coupler",
    re.I,
)

TAXONOMY_CLASS = {
    "couplers (review)": "fiber_chip_coupler",
    "edge coupler (review)": "fiber_chip_coupler",
    "GC benchmark": "fiber_chip_coupler",
    "PWB": "fiber_chip_coupler",
    "AMO emitter": "free_space_emitter",
    "visible/UV platform": "waveguide_platform",
    "visible platform + lasers": "waveguide_platform",
    "quantum (roadmap)": "waveguide_platform",
    "isolator": "nonreciprocal",
    "TO phase shifter": "phase_shifter",
    "MEMS": "switch_fabric",
    "PCM": "phase_shifter",
    "crossing": "crossing",
    "SWG devices (review)": "splitter",
    "ring (review)": "resonator",
    "high-Q SiN": "resonator",
    "SiN platform (review)": "waveguide_platform",
    "TFLN platform (review)": "waveguide_platform",
    "Si platform (review)": "waveguide_platform",
    "Si roadmap": "waveguide_platform",
    "lasers (review)": "laser",
    "Er amplifier": "amplifier",
}


# ---------- pure helpers (tested) ----------


def title_ratio(a: str, b: str) -> float:
    na, nb = litpool.norm_title(a), litpool.norm_title(b)
    if not na or not nb:
        return 0.0
    return round(difflib.SequenceMatcher(None, na, nb).ratio(), 4)


def optica_uri_to_doi(uri: str) -> str:
    """'oe-18-14-14439' -> '10.1364/oe.18.014439' (Optica DOI pattern journal.volume.page6); '' if not parseable."""
    m = OPTICA_URI.match(uri.strip().lower())
    if not m:
        return ""
    j, vol, _issue, page = m.groups()
    return f"10.1364/{j}.{vol}.{int(page):06d}"


def clean_doi(doi: str) -> str:
    d = litpool.norm_doi(doi).rstrip(".)")
    return d


def safe_name(key: str) -> str:
    return re.sub(r"[^a-z0-9._-]+", "_", key.lower())[:120] + "_" + hashlib.sha1(key.encode()).hexdigest()[:8]


def chunks(xs: list[str], n: int) -> Iterable[list[str]]:
    for i in range(0, len(xs), n):
        yield xs[i : i + n]


def eo_is_component(title: str) -> bool:
    if not EO_COMPONENT.search(title):
        return False
    t = title.lower()
    return ("modulat" not in t and "transduc" not in t) or bool(EO_STRONG.search(title))


def parse_taxonomy_seeds(md: str) -> list[dict[str, str]]:
    """Rows of the section 5 seed table: class, title, venue, id text, seen_in."""
    sec = md.split("## 5. Gaps and seed references", 1)[-1].split("\n## 6.", 1)[0]
    rows = []
    for line in sec.splitlines():
        if not line.startswith("| ") or line.startswith("| class") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        rows.append({"class": cells[0], "title": cells[1], "venue": cells[2], "ids": cells[3], "seen_in": cells[4]})
    return rows


# ---------- IO helpers ----------


def write_atomic(path: Path, records: list[dict[str, Any]]) -> int:
    part = path.with_name(path.name + ".part")
    if part.exists():
        part.unlink()
    n = litpool.append(part, records)
    part.replace(path)
    return n


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return litpool.read(path) if path.exists() else []


def get_json_retry(url: str, params: dict[str, Any], tries: int = 3) -> Any:
    """litfetch.get_json, retried when the body arrives truncated (JSONDecodeError seen on large OpenAlex pages)."""
    for i in range(tries):
        try:
            return litfetch.get_json(url, params)
        except json.JSONDecodeError:
            if i == tries - 1:
                raise
    raise AssertionError("unreachable")


def oa_single(key: str, select: str = SELECT_REFS) -> dict[str, Any] | None:
    try:
        w: dict[str, Any] = litfetch.get_json(f"{OA}/{key}", {"select": select})
        return w
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


class ResolveCache:
    """key ('doi:<doi>' | 'arxiv:<id>' | 'title:<norm>') -> resolved OpenAlex work or a miss; append-only JSONL."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.data: dict[str, dict[str, Any]] = {r["key"]: r for r in load_jsonl(path)}

    def put(self, key: str, rec: dict[str, Any]) -> None:
        rec = {"key": key, **rec}
        self.data[key] = rec
        litpool.append(self.path, [rec])


def crossref_title(title: str, hint: str = "") -> dict[str, Any]:
    """Best Crossref hit for a title (optionally with venue/year hint); returns doi, ratio, cr_score, cr_title."""
    q = f"{title} {hint}".strip()
    j = litfetch.get_json(CR, {"query.bibliographic": q, "rows": "5", "select": "DOI,title,score,type,container-title"})
    best: dict[str, Any] = {"doi": "", "ratio": 0.0, "cr_score": 0.0, "cr_title": ""}
    for it in j["message"]["items"]:
        t = (it.get("title") or [""])[0]
        r = title_ratio(title, t)
        if r > best["ratio"]:
            best = {"doi": clean_doi(it.get("DOI", "")), "ratio": r, "cr_score": it.get("score", 0.0), "cr_title": t}
    return best


OPTICA_ISSN = {"oe": "1094-4087", "optica": "2334-2536", "ome": "2159-3930", "boe": "2156-7085", "osac": "2578-7519",
               "optcon": "2770-0208", "opticaq": "2837-6714"}


def crossref_optica(uri: str) -> str:
    """'oe-32-17-30344' -> DOI of the Crossref record with that ISSN, volume, issue and first page; '' if none."""
    m = OPTICA_URI.match(uri)
    if not m or m.group(1) not in OPTICA_ISSN:
        return ""
    j, vol, issue, page = m.groups()
    res = litfetch.get_json(CR, {"filter": f"issn:{OPTICA_ISSN[j]}", "query.bibliographic": f"{vol} {issue} {page}",
                                 "rows": "20", "select": "DOI,volume,issue,page"})
    for it in res["message"]["items"]:
        if str(it.get("volume")) == vol and str(it.get("issue")) == issue and \
                str(it.get("page", "")).split("-")[0] == page:
            return clean_doi(it.get("DOI", ""))
    return ""


def resolve(cache: ResolveCache, kind: str, value: str, hint: str = "") -> dict[str, Any]:
    """kind doi | arxiv | title. Returns the cache record ({'work': {...}} or {'miss': reason}, plus match info)."""
    key = f"{kind}:{litpool.norm_title(value) if kind == 'title' else value.lower()}"
    if key in cache.data:
        return cache.data[key]
    rec: dict[str, Any]
    if kind == "doi":
        w = oa_single(f"doi:{value}")
        rec = {"work": w} if w else {"miss": "openalex 404"}
    elif kind == "optica":  # legacy DOI pattern first; newer Optica DOIs are opaque -> Crossref journal/volume/page
        w = oa_single(f"doi:{optica_uri_to_doi(value)}")
        if w:
            rec = {"work": w}
        else:
            cr_doi = crossref_optica(value)
            w = oa_single(f"doi:{cr_doi}") if cr_doi else None
            rec = {"work": w, "crossref_doi": cr_doi} if w else {"miss": "optica uri unresolved", "crossref_doi": cr_doi}
    elif kind == "arxiv":
        w = oa_single(f"doi:10.48550/arXiv.{value}")
        rec = {"work": w} if w else {"miss": "openalex 404"}
    else:
        hit = crossref_title(value, hint)
        match = {k: hit[k] for k in ("ratio", "cr_score", "cr_title")}
        if hit["doi"] and hit["ratio"] >= TITLE_MATCH_MIN:
            w = oa_single(f"doi:{hit['doi']}")
            rec = {"work": w, "crossref_doi": hit["doi"], "match": match} if w else {
                "miss": "openalex 404 after crossref", "crossref_doi": hit["doi"], "match": match}
        else:
            rec = {"miss": "no near-exact crossref title", "match": match, "crossref_doi": hit["doi"]}
    cache.put(key, rec)
    return rec


# ---------- local seeds ----------


def local_inputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """(seed inputs with kind/value, skipped url rows)."""
    seeds: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    with BLOG_CSV.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["access_class"] not in OA_CLASSES or r["topic_guess"].startswith("other"):
                continue
            if r["in_eo_atlas"] != "N" or r["in_packaging_atlas"] != "N":
                continue
            base = {"seed_source": "blog", "seed_reason": f"blog {r['post_file']} topic={r['topic_guess']}",
                    "seed_input_id": f"{r['id_type']}:{r['identifier']}"}
            if r["id_type"] == "doi":
                seeds.append({**base, "kind": "doi", "value": clean_doi(r["identifier"])})
            elif r["id_type"] == "arxiv":
                seeds.append({**base, "kind": "arxiv", "value": r["identifier"]})
            elif r["id_type"] == "optica_uri" and optica_uri_to_doi(r["identifier"]):
                seeds.append({**base, "kind": "optica", "value": r["identifier"].lower()})
            else:
                skipped.append({**base, "url": r["url"]})
    for r in parse_taxonomy_seeds(TAXONOMY_MD.read_text(encoding="utf-8")):
        base = {"seed_source": "taxonomy_s5", "seed_reason": f"taxonomy s5 {r['class']}; seen in {r['seen_in']}",
                "seed_input_id": r["title"], "seed_class": TAXONOMY_CLASS.get(r["class"], "")}
        dm, am = DOI_RE.search(r["ids"]), ARXIV_RE.search(r["ids"])
        if dm:
            seeds.append({**base, "kind": "doi", "value": clean_doi(dm.group(0))})
        elif am:
            seeds.append({**base, "kind": "arxiv", "value": am.group(1)})
        else:
            seeds.append({**base, "kind": "title", "value": r["title"], "hint": r["venue"]})
    eo_csv = inputs_root() / "eo-modulator-atlas" / "data" / "candidates.csv"
    with eo_csv.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if not eo_is_component(r["title"]):
                continue
            base = {"seed_source": "eo_candidates", "seed_input_id": f"eo:{r['paper_id']}",
                    "seed_reason": f"eo candidates {r['paper_id']} title names a non-modulator component"}
            if r["doi"]:
                seeds.append({**base, "kind": "doi", "value": clean_doi(r["doi"])})
            elif r["arxiv_id"]:
                seeds.append({**base, "kind": "arxiv", "value": re.sub(r"v\d+$", "", r["arxiv_id"])})
            else:
                seeds.append({**base, "kind": "title", "value": r["title"], "hint": f"{r['venue']} {r['year']}"})
    return seeds, skipped


def cmd_local(args: argparse.Namespace, log: RunLog) -> None:
    seeds, skipped = local_inputs()
    by_src: dict[str, int] = {}
    for s in seeds:
        by_src[s["seed_source"]] = by_src.get(s["seed_source"], 0) + 1
    log.info(f"local seed inputs {len(seeds)} {by_src}; skipped url rows {len(skipped)}")
    if args.dry_run:
        for s in seeds[:5] + [x for x in seeds if x["kind"] == "title"][:10]:
            log.info(f"  {s['seed_source']} {s['kind']} {s['value'][:90]}")
        return
    cache = ResolveCache(SEEDS / "resolve_local.jsonl")
    out: dict[str, dict[str, Any]] = {}
    unresolved: list[dict[str, Any]] = []
    for i, s in enumerate(seeds):
        try:
            rec = resolve(cache, s["kind"], s["value"], s.get("hint", ""))
        except litfetch.BlockedError as e:
            log.info(f"blocked at seed {i}: {e}; rerun to resume")
            log.event("local", "blocked", at=i, error=str(e))
            break
        except urllib.error.HTTPError as e:  # transient (e.g. 504): not cached, retried on the next run
            log.info(f"  http {e.code} for {s['kind']} {s['value'][:60]}; left for rerun")
            unresolved.append({**s, "miss": f"transient http {e.code}"})
            continue
        if i % 50 == 0:
            log.info(f"  {i}/{len(seeds)}")
        if "work" not in rec:
            unresolved.append({**{k: v for k, v in s.items()}, "miss": rec.get("miss", ""), "match": rec.get("match")})
            continue
        p = litpool.from_openalex(rec["work"], LANE, f"local:{s['seed_source']}")
        extra = {"seed_source": s["seed_source"], "seed_reason": s["seed_reason"], "seed_input_id": s["seed_input_id"],
                 "seed_class": s.get("seed_class", "")}
        if s["kind"] == "arxiv" and not p["arxiv_id"]:
            extra["seed_arxiv_id"] = s["value"]
        if "match" in rec:
            extra["title_match"] = rec["match"]
        if p["uid"] in out:
            prev = out[p["uid"]]
            prev["seed_reason"] += " | " + extra["seed_reason"]
            prev["seed_source"] = ",".join(sorted(set(prev["seed_source"].split(",")) | {s["seed_source"]}))
            prev["seed_class"] = prev["seed_class"] or extra["seed_class"]
            continue
        out[p["uid"]] = {**p, **extra}
    n = write_atomic(litpool.POOL / "seeds_local.jsonl", list(out.values()))
    write_atomic(SEEDS / "local_unresolved.jsonl", unresolved + [{**x, "miss": "url row, no identifier"} for x in skipped])
    log.info(f"seeds_local.jsonl {n} records; unresolved {len(unresolved)}; url rows {len(skipped)}")
    log.event("local", records=n, unresolved=len(unresolved), url_rows=len(skipped))


# ---------- review discovery ----------


def load_config() -> dict[str, Any]:
    with CONFIG.open(encoding="utf-8") as f:
        cfg: dict[str, Any] = yaml.safe_load(f) or {}
    return cfg


def _search_count_path() -> Path:
    return SEEDS / "openalex_search_count.json"


def cmd_find_reviews(args: argparse.Namespace, log: RunLog) -> None:
    cfg = load_config()
    outdir = SEEDS / "review_candidates"
    outdir.mkdir(parents=True, exist_ok=True)
    key = "openalex_queries" if args.openalex_search else "queries"
    for q in cfg.get(key) or []:
        if args.only and q["class"] != args.only:
            continue
        name = f"{'oa' if args.openalex_search else 'cr'}_{safe_name(q['q'])}.json"
        path = outdir / name
        if not path.exists() and not args.dry_run:
            if args.openalex_search:
                cp = _search_count_path()
                used = int(json.loads(cp.read_text())["n"]) if cp.exists() else 0
                if used >= OPENALEX_SEARCH_CAP:
                    log.info(f"openalex search cap {OPENALEX_SEARCH_CAP} reached; skip {q['q']}")
                    continue
                j = litfetch.get_json(OA, {
                    "filter": f"title.search:{q['q']},publication_year:2018-2026",
                    "sort": "cited_by_count:desc", "per_page": "25",
                    "select": "id,doi,title,publication_year,type,primary_location,cited_by_count"})
                cp.parent.mkdir(parents=True, exist_ok=True)
                cp.write_text(json.dumps({"n": used + 1}))
                items = [{"doi": litpool.norm_doi(w.get("doi")), "title": w.get("title") or "",
                          "year": w.get("publication_year"), "type": w.get("type"),
                          "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name", ""),
                          "cited_by": w.get("cited_by_count")} for w in j["results"]]
            else:
                j = litfetch.get_json(CR, {
                    "query.bibliographic": q["q"], "rows": str(q.get("rows", 20)),
                    "filter": "type:journal-article,from-pub-date:2018-01-01",
                    "select": "DOI,title,score,container-title,issued,is-referenced-by-count,type"})
                items = [{"doi": clean_doi(it.get("DOI", "")), "title": (it.get("title") or [""])[0],
                          "year": ((it.get("issued") or {}).get("date-parts") or [[None]])[0][0],
                          "venue": (it.get("container-title") or [""])[0],
                          "cited_by": it.get("is-referenced-by-count"), "score": it.get("score")}
                         for it in j["message"]["items"]]
            path.write_text(json.dumps({"query": q, "items": items}, ensure_ascii=False, indent=1))
            log.event("find_reviews", query=q["q"], n=len(items), file=str(path.relative_to(ROOT)))
        if path.exists() and args.show:
            d = json.loads(path.read_text())
            print(f"\n## {q['class']} / {q.get('subtype', '')}: {q['q']}")
            for it in d["items"]:
                if args.review_only and not REVIEW_TITLE.search(it["title"]):
                    continue
                print(f"  {it['year']} | {it['cited_by']} | {it['venue'][:30]} | {it['doi']} | {it['title'][:110]}")


REVIEW_TITLE = re.compile(
    r"\breview|tutorial|progress|roadmap|perspective|advances|overview|recent|challenges|state[- ]of[- ]the[- ]art|"
    r"trends|prospects|outlook|opportunit|primer|survey|introduction to",
    re.I,
)


def anchor_work(a: dict[str, Any], cache: ResolveCache) -> dict[str, Any] | None:
    """Anchor by `doi` (singleton get) or by `title` (+ `hint`) through Crossref near-exact match."""
    rec = resolve(cache, "doi", a["doi"]) if a.get("doi") else resolve(cache, "title", a["title"], a.get("hint", ""))
    w: dict[str, Any] | None = rec.get("work")
    return w


def cmd_anchor_reviews(args: argparse.Namespace, log: RunLog) -> None:
    """Most-cited works (2018-2026) citing a landmark anchor paper (filter cites:W, filter-only, one 200-record page);
    review-like ones (OpenAlex type review or a review word in the title) are shown for manual choice."""
    cfg = load_config()
    outdir = SEEDS / "review_candidates"
    outdir.mkdir(parents=True, exist_ok=True)
    cache = ResolveCache(SEEDS / "resolve_anchors.jsonl")
    for a in cfg.get("anchors") or []:
        if args.only and a["class"] != args.only:
            continue
        akey = a.get("doi") or a.get("title", "")
        path = outdir / f"anchorcites_{safe_name(akey)}.json"
        if not path.exists() and not args.dry_run:
            w = anchor_work(a, cache)
            if w is None:
                log.info(f"anchor not resolved: {akey}")
                log.event("anchor_reviews", "missing", anchor=akey)
                continue
            wid = w["id"].rsplit("/", 1)[-1]
            j = litfetch.get_json(OA, {
                "filter": f"cites:{wid},publication_year:2018-2026", "sort": "cited_by_count:desc",
                "per_page": "200", "select": "id,doi,title,publication_year,type,primary_location,cited_by_count"})
            items = [{"doi": litpool.norm_doi(x.get("doi")), "title": x.get("title") or "",
                      "year": x.get("publication_year"), "type": x.get("type"),
                      "venue": ((x.get("primary_location") or {}).get("source") or {}).get("display_name", ""),
                      "cited_by": x.get("cited_by_count")} for x in j["results"]]
            items = [x for x in items if x["type"] == "review" or REVIEW_TITLE.search(x["title"])]
            aw = {k: w.get(k) for k in ("id", "doi", "title", "publication_year", "cited_by_count")}
            path.write_text(json.dumps({"anchor": a, "anchor_work": aw, "n_citing": j["meta"]["count"],
                                        "items": items}, ensure_ascii=False, indent=1))
            log.event("anchor_reviews", anchor=akey, wid=wid, n_citing=j["meta"]["count"], n_review_like=len(items))
        if path.exists() and args.show:
            d = json.loads(path.read_text())
            aw = d["anchor_work"]
            print(f"\n## {a['class']} / {a.get('subtype', '')}: anchor {aw['doi']} = {(aw['title'] or '')[:90]} "
                  f"({aw['publication_year']}, {aw['cited_by_count']} cites); citing 2018+ {d['n_citing']}")
            for it in d["items"][: args.top]:
                print(f"  {it['year']} | {it['cited_by']} | {(it['venue'] or '')[:30]} | {it['doi']} | {it['title'][:110]}")


# ---------- reviews and references ----------


class WorkCache:
    """OpenAlex works by W id (selected fields), or {'id': W, 'missing': True}; append-only JSONL."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.data: dict[str, dict[str, Any]] = {}
        for r in load_jsonl(path):
            self.data[r["id"].rsplit("/", 1)[-1]] = r

    def add(self, recs: list[dict[str, Any]]) -> None:
        for r in recs:
            self.data[r["id"].rsplit("/", 1)[-1]] = r
        litpool.append(self.path, recs)


def fetch_works(ids: list[str], wc: WorkCache, log: RunLog) -> None:
    todo = sorted({i for i in ids if i not in wc.data})
    log.info(f"  fetch {len(todo)} uncached works in {(len(todo) + BATCH_IDS - 1) // BATCH_IDS} filter pages")
    for batch in chunks(todo, BATCH_IDS):
        j = get_json_retry(OA, {"filter": "openalex_id:" + "|".join(batch), "per_page": "200",
                                "select": litpool.OPENALEX_SELECT})
        got = list(j["results"])
        seen = {w["id"].rsplit("/", 1)[-1] for w in got}
        missing = [{"id": i, "missing": True} for i in batch if i not in seen]
        wc.add(got + missing)


def review_key(r: dict[str, Any]) -> str:
    return f"doi:{r['doi']}" if r.get("doi") else f"doi:10.48550/arXiv.{r['arxiv_id']}"


def cmd_reviews(args: argparse.Namespace, log: RunLog) -> None:
    cfg = load_config()
    reviews = [r for r in cfg.get("reviews") or [] if not args.only or r["class"] == args.only]
    log.info(f"reviews in config {len(reviews)}")
    if args.dry_run:
        return
    rdir = SEEDS / "reviews"
    rdir.mkdir(parents=True, exist_ok=True)
    raw: dict[str, dict[str, Any]] = {}
    for r in reviews:
        key = review_key(r)
        path = rdir / f"{safe_name(key)}.json"
        if path.exists():
            raw[key] = json.loads(path.read_text())
            continue
        w = oa_single(key)
        if w is None:
            log.info(f"review not in OpenAlex: {key}")
            log.event("review", "missing", key=key)
            continue
        path.write_text(json.dumps(w, ensure_ascii=False))
        raw[key] = w
    # seeds_reviews.jsonl: one record per review (a review chosen for two classes keeps both in seed_classes)
    recs: dict[str, dict[str, Any]] = {}
    for r in cfg.get("reviews") or []:
        w = raw.get(review_key(r))
        if w is None:
            continue
        p = litpool.from_openalex(w, LANE, f"review_seed:{r['how_found']}")
        cls = f"{r['class']}/{r.get('subtype') or ''}".rstrip("/")
        if p["uid"] in recs:
            recs[p["uid"]]["seed_classes"].append(cls)
            continue
        recs[p["uid"]] = {**p, "is_review_seed": True, "seed_class": r["class"], "seed_classes": [cls],
                          "n_referenced_works": len(w.get("referenced_works") or [])}
    if not args.only:
        n = write_atomic(litpool.POOL / "seeds_reviews.jsonl", list(recs.values()))
        log.info(f"seeds_reviews.jsonl {n} records")
    # references per class
    wc = WorkCache(SEEDS / "works_cache.jsonl")
    classes = sorted({r["class"] for r in reviews})
    summary: dict[str, Any] = {}
    for cls in classes:
        out_path = litpool.POOL / f"seeds_refs_{cls}.jsonl"
        crev = [r for r in reviews if r["class"] == cls and review_key(r) in raw]
        refs: dict[str, list[str]] = {}
        for r in crev:
            doi = litpool.norm_doi(raw[review_key(r)].get("doi")) or review_key(r).removeprefix("doi:")
            for wid in raw[review_key(r)].get("referenced_works") or []:
                refs.setdefault(wid.rsplit("/", 1)[-1], []).append(doi)
        log.info(f"{cls}: {len(crev)} reviews, {len(refs)} distinct referenced works")
        try:
            fetch_works(list(refs), wc, log)
        except litfetch.BlockedError as e:
            log.info(f"blocked during {cls}: {e}; rerun to resume")
            log.event("refs", "blocked", cls=cls, error=str(e))
            break
        out: list[dict[str, Any]] = []
        for wid, dois in refs.items():
            w = wc.data.get(wid)
            if not w or w.get("missing"):
                continue
            p = litpool.from_openalex(w, LANE, f"refs_of:{dois[0]}")
            out.append({**p, "seed_class": cls, "refs_of_all": sorted(set(dois))})
        n = write_atomic(out_path, out)
        years = [x["year"] for x in out if x["year"]]
        summary[cls] = {"reviews": len(crev), "refs": len(refs), "records": n,
                        "years": [min(years), max(years)] if years else []}
        log.info(f"  seeds_refs_{cls}.jsonl {n} records years {summary[cls]['years']}")
        log.event("refs", cls=cls, **summary[cls])
    (SEEDS / "refs_summary.json").write_text(json.dumps(summary, indent=1))


def cmd_cites(args: argparse.Namespace, log: RunLog) -> None:
    cfg = load_config()
    entries = [c for c in cfg.get("cites") or [] if not args.only or c["class"] == args.only]
    log.info(f"cites entries {len(entries)}")
    if args.dry_run:
        return
    cdir = SEEDS / "cites"
    cdir.mkdir(parents=True, exist_ok=True)
    by_cls: dict[str, dict[str, dict[str, Any]]] = {}
    for c in entries:
        w = oa_single(f"doi:{c['doi']}", select="id,doi")
        if not w:
            log.info(f"cites seed not in OpenAlex: {c['doi']}")
            continue
        wid = w["id"].rsplit("/", 1)[-1]
        for page in range(int(c.get("pages", 2))):
            path = cdir / f"{wid}_p{page}.json"
            if path.exists():
                j = json.loads(path.read_text())
            else:
                j = get_json_retry(OA, {"filter": f"cites:{wid}", "sort": "publication_date:desc",
                                        "per_page": "200", "page": str(page + 1),  # cursor page 2 gave HTTP 401
                                        "select": litpool.OPENALEX_SELECT})
                path.write_text(json.dumps(j, ensure_ascii=False))
            for x in j["results"]:
                p = litpool.from_openalex(x, LANE, f"cites:{wid}")
                by_cls.setdefault(c["class"], {}).setdefault(p["uid"], {**p, "seed_class": c["class"],
                                                                        "cites_seed_doi": c["doi"]})
            if (page + 1) * 200 >= int((j.get("meta") or {}).get("count") or 0):
                break
    for cls, recs in by_cls.items():
        n = write_atomic(litpool.POOL / f"seeds_cites_{cls}.jsonl", list(recs.values()))
        log.info(f"seeds_cites_{cls}.jsonl {n}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["local", "find-reviews", "anchor-reviews", "reviews", "cites"])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", default="", help="restrict to one class")
    ap.add_argument("--openalex-search", action="store_true", help="find-reviews: run openalex_queries (paid)")
    ap.add_argument("--review-only", action="store_true", help="find-reviews --show: only review-like titles")
    ap.add_argument("--top", type=int, default=15, help="anchor-reviews --show: rows per anchor")
    ap.add_argument("--show", action="store_true", help="find-reviews / anchor-reviews: print cached hits")
    args = ap.parse_args()
    SEEDS.mkdir(parents=True, exist_ok=True)
    with RunLog(f"lit_seeds_{args.cmd.replace('-', '_')}", args.dry_run) as log:
        cmds = {"local": cmd_local, "find-reviews": cmd_find_reviews, "anchor-reviews": cmd_anchor_reviews,
                "reviews": cmd_reviews, "cites": cmd_cites}
        cmds[args.cmd](args, log)
    return 0


if __name__ == "__main__":
    sys.exit(main())
