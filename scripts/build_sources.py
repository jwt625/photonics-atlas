"""Build data/registry/sources.csv from the corpora (D23): eo:, pk:, ofc2026:, blog:, lin: (web: rows come from
scripts/merge_org_events.py and are kept as they are).

- eo: EO papers.csv as recorded there (access, licence, redistribution unchanged); text_cached = cache_status full_extract.
- pk: PK papers.csv + references/<id>/source.json (access text "institutional subscription (local-only)" -> paywalled,
  "manual download (local-only)" -> unknown; redistribution from source.json); source_type journal for T-CPMT DOIs,
  conference otherwise.
- ofc2026: 830 presentations; access paywalled_conference, redistribution restricted_local_only (D4); the 54 papers
  already in EO (DOI 10.1364/ofc.2026.<code>) get same_as = eo:<paper_id> and the EO DOI.
- blog: 128 PDFs hosted in the blog repo assets/doc; url derived from the repo path (not fetched).
- lin: LIN canonical sources (282) with their grade.
No PDF or text is copied. Rows are regenerated per corpus; web: rows are preserved.

Usage: uv run python scripts/build_sources.py [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
from collections import Counter
from pathlib import Path

from photonics_atlas.adapters import blog, eo, lineage, ofc, pk
from photonics_atlas.csvio import read_csv, write_csv
from photonics_atlas.paths import REGISTRY, ROOT, input_path
from photonics_atlas.runlog import RunLog
from photonics_atlas.schema import columns, load_schema
from photonics_atlas.textnorm import slug

BLOG_BASE = "https://outside5sigma.com/"
PK_ACCESS = {"institutional subscription (local-only)": "paywalled", "manual download (local-only)": "unknown"}


def eo_rows() -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for p in eo.papers():
        out.append(
            {
                "source_id": f"eo:{p.paper_id}",
                "corpus": "eo",
                "native_id": p.paper_id,
                "title": p.title,
                "year": p.year,
                "published_on": p.published_on,
                "venue": p.venue,
                "doi": p.doi,
                "arxiv_id": p.arxiv_id,
                "url": p.url,
                "source_type": p.source_type,
                "access": p.access,
                "license": p.license,
                "redistribution": p.redistribution,
                "text_cached": p.cache_status == "full_extract",
                "notes": "fields as recorded in eo-modulator-atlas data/papers.csv",
            }
        )
    return out


def pk_rows(log: RunLog) -> list[dict[str, object]]:
    refs = input_path("pk_atlas") / "references"
    out: list[dict[str, object]] = []
    for p in pk.papers():
        sj = refs / p.paper_id / "source.json"
        meta = json.loads(sj.read_text()) if sj.exists() else {}
        acc = str(meta.get("access", ""))
        if acc and acc not in PK_ACCESS:
            log.event("pk_access", "unknown_value", paper_id=p.paper_id, access=acc)
        out.append(
            {
                "source_id": f"pk:{p.paper_id}",
                "corpus": "pk",
                "native_id": p.paper_id,
                "title": p.title,
                "year": p.year,
                "venue": p.venue,
                "doi": p.doi,
                "url": meta.get("url") or (f"https://doi.org/{p.doi}" if p.doi else ""),
                "source_type": "journal" if "/tcpmt" in p.doi.lower() else "conference",
                "access": PK_ACCESS.get(acc, "unknown"),
                "redistribution": meta.get("redistribution") or "restricted_local_only",
                "text_cached": p.source_status == "full_text",
                "notes": f"PK source.json access: {acc}" if acc else "no PK source.json",
            }
        )
    return out


def ofc_rows(log: RunLog) -> list[dict[str, object]]:
    eo_ofc = {}
    for p in eo.papers():
        d = p.doi.lower()
        if d.startswith("10.1364/ofc.2026."):
            eo_ofc[d.removeprefix("10.1364/ofc.2026.")] = p
    out: list[dict[str, object]] = []
    seen = set()
    for pr in ofc.presentations():
        dup = eo_ofc.get(pr.code.lower())
        if dup:
            seen.add(pr.code.lower())
        out.append(
            {
                "source_id": f"ofc2026:{pr.code}",
                "corpus": "ofc2026",
                "native_id": pr.code,
                "title": pr.title,
                "year": 2026,
                "venue": f"Optical Fiber Communication Conference (OFC) 2026, paper {pr.code}",
                "doi": dup.doi if dup else "",
                "url": dup.url if dup else "",
                "source_type": "conference",
                "access": "paywalled_conference",
                "redistribution": "restricted_local_only",
                "text_cached": pr.text_cached,
                "same_as": f"eo:{dup.paper_id}" if dup else "",
                "notes": f"session {pr.session_code} {pr.session_date}"
                + ("; duplicate of the EO row (canonical, exact PDF-page locators, D4)" if dup else ""),
            }
        )
    missing = sorted(set(eo_ofc) - seen)
    log.info(f"OFC duplicates of EO papers: {len(seen)} matched; EO OFC DOIs without a presentation record: {missing}")
    return out


def blog_rows() -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    used: Counter[str] = Counter()
    for b in blog.pdfs():
        rel = b.path.split("/", 1)[1] if "/" in b.path else b.path  # strip the repo folder name
        stem = Path(rel).stem
        sid = slug(stem) or "pdf"
        used[sid] += 1
        if used[sid] > 1:
            sid = f"{sid}_{used[sid]}"
        out.append(
            {
                "source_id": f"blog:{sid}",
                "corpus": "blog",
                "native_id": rel,
                "title": b.filename_title,
                "url": BLOG_BASE + urllib.parse.quote(rel),
                "source_type": "other",
                "access": "public_web",
                "redistribution": "unknown",
                "text_cached": False,
                "notes": f"hosted in the blog repo; url derived from the repo path, not fetched; title from {b.title_source}; topic guess {b.topic_guess}",
            }
        )
    return out


def lin_rows() -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for s in lineage.sources():
        out.append(
            {
                "source_id": f"lin:{s.id}",
                "corpus": "lin",
                "native_id": s.id,
                "title": s.title,
                "published_on": s.publication_date or "",
                "year": (s.publication_date or "")[:4],
                "venue": s.publisher,
                "url": s.url,
                "source_type": s.source_type,
                "access": "public_web",
                "redistribution": "unknown",
                "evidence_grade": s.evidence_grade,
                "accessed_on": s.accessed_date,
                "notes": s.notes or "",
            }
        )
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    with RunLog("build_sources", args.dry_run) as log:
        path = REGISTRY / "sources.csv"
        built = {"eo", "pk", "ofc2026", "blog", "lin"}
        keep = [r for r in read_csv(path) if r["corpus"] not in built] if path.exists() else []
        rows: list[dict[str, object]] = [*eo_rows(), *pk_rows(log), *ofc_rows(log), *blog_rows(), *lin_rows()]
        enums = load_schema()["enums"]
        for r in rows:
            if r["source_type"] not in enums["source_type"]:
                log.event("source_type", "unknown_value", source_id=r["source_id"], value=r["source_type"])
        counts = Counter(str(r["corpus"]) for r in rows)
        log.info(f"rows by corpus: {dict(counts)}; rows of other corpora kept: {len(keep)}")
        log.info(f"ofc2026 rows with same_as: {sum(1 for r in rows if r.get('same_as'))}")
        log.event("sources", "ok", counts=dict(counts))
        if not args.dry_run:
            write_csv(path, columns("sources"), [*rows, *keep])
            log.info(f"wrote {path.relative_to(ROOT)} ({len(rows) + len(keep)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
