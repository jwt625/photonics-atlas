"""Register cached literature papers as corpus `lit` rows in data/registry/sources.csv (DevLog-006 S7, D127).

One row `lit:<paper_id>` per references/<paper_id>/source.json that records a retrieved PDF (sha256 present) and was
written by lit_extract.py (extracted_on present; others are listed as pending), so the
registry is reproducible from the committed source.json files on a machine without the local PDFs. Fields: corpus lit,
native_id, title, year, published_on, venue, doi, arxiv_id, url (doi.org when a DOI exists, else arXiv abs, else the
fetched URL), source_type (review / journal / conference / arxiv_preprint / other from the pool work type and the
selection venue_type), access, license, redistribution (as computed by lit_extract.py), text_cached (text extracted),
same_as (an existing non-lit row with the same DOI), accessed_on (retrieval date), notes.
Rows of every other corpus are written back unchanged and in place; existing lit rows are updated in place, new ones
appended in paper_id order; a lit row whose source.json disappeared is kept and reported. Idempotent.

Usage: uv run python scripts/lit_register_sources.py [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

from lit_fetch_oa import CACHE_LIST, REFS, read_rows

from photonics_atlas.csvio import read_csv, write_csv
from photonics_atlas.paths import REGISTRY, ROOT
from photonics_atlas.runlog import RunLog
from photonics_atlas.schema import columns, load_schema

SOURCES = REGISTRY / "sources.csv"
PDATE = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")


def source_type(work_type: str, venue_type: str, arxiv_id: str) -> str:
    if work_type == "review":
        return "review"
    if venue_type in ("journal", "conference"):
        return venue_type
    if venue_type == "repository" and arxiv_id:
        return "arxiv_preprint"
    return "other"


def registry_url(doi: str, arxiv_id: str, fetched: str) -> str:
    if doi:
        return f"https://doi.org/{doi}"
    if arxiv_id:
        return f"https://arxiv.org/abs/{arxiv_id}"
    return fetched


def lit_row(pid: str, meta: dict[str, Any], cache_row: dict[str, str], doi_owner: dict[str, str]) -> dict[str, Any]:
    doi = str(meta.get("doi") or cache_row.get("doi", ""))
    arxiv_id = str(meta.get("arxiv_id") or cache_row.get("arxiv_id", ""))
    pub = str(meta.get("publication_date", ""))
    acc = str(meta.get("retrieved_on", ""))[:10]
    return {
        "source_id": f"lit:{pid}",
        "corpus": "lit",
        "native_id": pid,
        "title": meta.get("title") or cache_row.get("title", ""),
        "year": cache_row.get("year") or meta.get("year", ""),
        "published_on": pub if PDATE.match(pub) else "",
        "venue": cache_row.get("venue") or meta.get("venue", ""),
        "doi": doi,
        "arxiv_id": arxiv_id,
        "url": registry_url(doi, arxiv_id, str(meta.get("url", ""))),
        "source_type": source_type(str(meta.get("work_type", "")), cache_row.get("venue_type", ""), arxiv_id),
        "access": meta.get("access") or "unknown",
        "license": meta.get("license", ""),
        "redistribution": meta.get("redistribution") or "unknown",
        "evidence_grade": "",
        "text_cached": bool(meta.get("text_chars")),
        "same_as": doi_owner.get(doi.lower(), "") if doi else "",
        "accessed_on": acc if PDATE.match(acc) else "",
        "notes": f"DevLog-006 S7 literature corpus; route {meta.get('route', '')}; references/{pid}/source.json",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    cols = columns("sources")
    enums = load_schema()["enums"]
    cl = {r["paper_id"]: r for r in read_rows(CACHE_LIST)}
    with RunLog("lit_register_sources", a.dry_run) as log:
        rows = read_csv(SOURCES)
        doi_owner = {
            r["doi"].lower(): r["source_id"] for r in rows if r["corpus"] != "lit" and r["doi"] and not r["same_as"]
        }
        new: dict[str, dict[str, Any]] = {}
        not_extracted: list[str] = []
        errors = 0
        for path in sorted(REFS.glob("*/source.json")) if REFS.exists() else []:
            pid = path.parent.name
            if pid.startswith("_"):
                continue
            meta = json.loads(path.read_text())
            if not meta.get("sha256"):
                log.event("register", "skip_no_pdf", paper_id=pid)
                continue
            if not meta.get("extracted_on"):
                not_extracted.append(pid)
                log.event("register", "skip_not_extracted", paper_id=pid)
                continue
            r = lit_row(pid, meta, cl.get(pid, {}), doi_owner)
            bad = [f"{f}={r[f]!r}" for f in ("source_type", "access", "redistribution") if r[f] not in enums[f]]
            if bad:
                log.info(f"ERROR {pid}: {', '.join(bad)} not in the schema enums; not registered")
                log.event("register", "bad_enum", paper_id=pid, fields=bad)
                errors += 1
                continue
            if not r["title"]:
                log.info(f"warning: {pid} has no title (not in cache_list.csv?)")
            new[r["source_id"]] = r
        out: list[dict[str, Any]] = []
        updated = unchanged = kept_orphan = 0
        for r in rows:
            sid = r["source_id"]
            if r["corpus"] != "lit":
                out.append(r)
            elif sid in new:
                nr = new.pop(sid)
                same = all(str(r.get(c, "")) == _cell(nr.get(c)) for c in cols)
                unchanged += same
                updated += not same
                out.append(nr)
            else:
                kept_orphan += 1
                log.info(f"warning: {sid} has no source.json any more; row kept unchanged")
                out.append(r)
        added = [new[k] for k in sorted(new)]
        out.extend(added)
        log.info(
            f"lit rows: {len(added)} new, {updated} updated, {unchanged} unchanged, {kept_orphan} orphan kept; "
            f"same_as set on {sum(1 for r in out if r['corpus'] == 'lit' and r['same_as'])}"
        )
        log.event("register", "ok", added=len(added), updated=updated, unchanged=unchanged, orphan=kept_orphan)
        for r in added:
            log.info(f"  + {r['source_id']} {r['source_type']} {r['access']} {r['redistribution']} {r['url']}")
        if not_extracted:
            log.info(
                f"{len(not_extracted)} cached paper(s) not extracted yet (run lit_extract.py --pending first): "
                + ", ".join(not_extracted[:20])
            )
        if a.dry_run:
            log.info("dry run: sources.csv not written")
        elif added or updated:
            write_csv(SOURCES, cols, out)
            log.info(f"wrote {SOURCES.relative_to(ROOT)} ({len(out)} rows)")
    return 1 if errors else 0


def _cell(v: object) -> str:
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    return str(v)


if __name__ == "__main__":
    sys.exit(main())
