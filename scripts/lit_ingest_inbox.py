"""Ingest user-downloaded PDFs from references/_inbox/ (DevLog-006 S7, D124; adapted from advanced-packaging-atlas
scripts/ingest_inbox.py), then extract them with scripts/lit_extract.py.

Names: references/_inbox/<paper_id>.pdf (main text) and references/_inbox/<paper_id>_supplement.pdf (optional), with
paper_id from data/_staging/literature/cache_list.csv (the manual list is data/_staging/literature/manual_downloads.md).
A file is moved to references/<paper_id>/source.pdf (supplement: references/<paper_id>/supplement/source.pdf) only
after the %PDF magic and >= 20 kB checks. Nothing in the inbox is ever deleted: a file that fails a check, has an
unknown paper_id, or whose target already exists stays in place and is reported. source.json gets route manual
(unless an acquiring script already set a route), sha256, bytes, retrieved_on; redistribution is then computed by
lit_extract.py (manual copies: restricted_local_only).

Usage: uv run python scripts/lit_ingest_inbox.py [--dry-run] [--no-extract]
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Any

from lit_extract import run as extract_run
from lit_fetch_oa import CACHE_LIST, MIN_PDF_BYTES, REFS, read_rows

from photonics_atlas.paths import ROOT
from photonics_atlas.runlog import RunLog

INBOX = REFS / "_inbox"
SUFFIX = "_supplement"


def split_name(stem: str) -> tuple[str, bool]:
    """('<paper_id>', is_supplement) from an inbox file stem."""
    if stem.endswith(SUFFIX):
        return stem[: -len(SUFFIX)], True
    return stem, False


def check_pdf(path: Path) -> str:
    """'' when the file looks like a complete PDF, else the reason."""
    with path.open("rb") as f:
        head = f.read(5)
    if head != b"%PDF-":
        return "not a PDF (no %PDF magic)"
    if path.stat().st_size < MIN_PDF_BYTES:
        return f"too small ({path.stat().st_size} B)"
    return ""


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_meta(pid: str, row: dict[str, str], dest: Path, supplement: bool) -> None:
    path = REFS / pid / "source.json"
    meta: dict[str, Any] = json.loads(path.read_text()) if path.exists() else {}
    if supplement:
        meta["supplement_retrieved_on"] = dt.datetime.now(dt.UTC).date().isoformat()
        meta["supplement_acquisition"] = "manual download by the user (references/_inbox)"
    else:
        doi = row.get("doi", "")
        meta.update(
            paper_id=pid,
            uid=meta.get("uid") or row.get("uid", ""),
            doi=meta.get("doi") or doi,
            url=meta.get("url") or (f"https://doi.org/{doi}" if doi else row.get("oa_url", "")),
            route=meta.get("route") or "manual",
            acquisition="manual download by the user (references/_inbox)",
            retrieved_on=dt.datetime.now(dt.UTC).date().isoformat(),
            bytes=dest.stat().st_size,
            sha256=sha256(dest),
        )
    path.write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-extract", action="store_true")
    a = ap.parse_args()
    cl = {r["paper_id"]: r for r in read_rows(CACHE_LIST)}
    ingested: list[str] = []
    left = 0
    with RunLog("lit_ingest_inbox", a.dry_run) as log:
        files = sorted(INBOX.glob("*.pdf")) if INBOX.exists() else []
        log.info(f"{len(files)} PDF(s) in {INBOX.relative_to(ROOT)}")
        for f in files:
            pid, supplement = split_name(f.stem)
            dest = REFS / pid / ("supplement/source.pdf" if supplement else "source.pdf")
            problem = ""
            if pid not in cl:
                problem = "paper_id not in cache_list.csv"
            elif dest.exists():
                problem = f"{dest.relative_to(ROOT)} already exists"
            else:
                problem = check_pdf(f)
            if problem:
                left += 1
                log.info(f"LEFT IN INBOX {f.name}: {problem}")
                log.event("ingest", "left_in_inbox", file=f.name, reason=problem)
                continue
            if a.dry_run:
                log.info(f"would ingest {f.name} -> {dest.relative_to(ROOT)}")
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), dest)
            write_meta(pid, cl[pid], dest, supplement)
            log.info(f"ingested {f.name} -> {dest.relative_to(ROOT)}")
            log.event("ingest", "ok", paper_id=pid, supplement=supplement, bytes=dest.stat().st_size)
            if pid not in ingested:
                ingested.append(pid)
        rc = 0
        if ingested and not a.no_extract:
            rc = extract_run(ingested, force=True, dry_run=False, log=log)
        log.info(f"ingested {len(ingested)} paper(s); {left} file(s) left in the inbox")
    return rc or (1 if left else 0)


if __name__ == "__main__":
    sys.exit(main())
