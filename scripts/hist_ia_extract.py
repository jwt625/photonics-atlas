"""Cut historical papers out of archive.org volume scans (DevLog-016 D972).

For each entry in ITEMS: download the item's volume PDF once through photonics_atlas.litfetch (spacing, breaker,
generic User-Agent) to git-ignored cache/literature/ia_volumes/<item>.pdf, copy the leaf range (0-based archive.org
leaf index n = PDF page index) into references/_inbox/<paper_id>.pdf, and print the first line of text of the first
and last cut page so the range can be checked. Then run scripts/lit_ingest_inbox.py and scripts/lit_ocr.py.
Leaf ranges come from the page-image checks recorded in DevLog-016 D972. Skips papers already cached or in the inbox.

Usage: uv run python scripts/hist_ia_extract.py [--paper-ids a,b] [--dry-run]
"""

from __future__ import annotations

import argparse
import sys
from typing import Any

import pymupdf

from photonics_atlas import litfetch
from photonics_atlas.paths import CACHE, ROOT
from photonics_atlas.runlog import RunLog

fitz: Any = pymupdf
VOL = CACHE / "literature" / "ia_volumes"
INBOX = ROOT / "references" / "_inbox"
# paper_id: (archive.org item, first leaf, last leaf)  (pages printed: see DevLog-016 D972)
ITEMS = {
    "colladon1842": ("comptesrendusheb15acad", 813, 815),  # Comptes rendus 15, pp. 800-802
    "pockels1894": ("abhandlungenderk3940knig", 12, 215),  # Abh. Ges. Wiss. Goettingen 39, memoir pp. 1-204
    "fabry1899": ("annalesdechimie47lusgoog", 121, 150),  # Ann. Chim. Phys. (7) 16, pp. 115-144
    "einstein1917": (
        "per_physikalische-zeitschrift_physikalische-zeitschrift_1917-03-15_6",
        4,
        11,
    ),  # Phys. Z. 18, 121-128
}


def first_line(page: Any) -> str:
    lines = [ln.strip() for ln in page.get_text("text").splitlines() if len(ln.strip()) > 3]
    return (lines[0] if lines else "(no text layer)")[:90]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--paper-ids")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    ids = [x for x in (a.paper_ids.split(",") if a.paper_ids else ITEMS) if x in ITEMS]
    VOL.mkdir(parents=True, exist_ok=True)
    INBOX.mkdir(parents=True, exist_ok=True)
    with RunLog("hist_ia_extract", a.dry_run) as log:
        for pid in ids:
            item, lo, hi = ITEMS[pid]
            if (ROOT / "references" / pid / "source.pdf").exists() or (INBOX / f"{pid}.pdf").exists():
                log.info(f"{pid}: already cached or in the inbox")
                continue
            vol = VOL / f"{item}.pdf"
            if not vol.exists():
                log.info(f"{pid}: downloading {item}.pdf")
                if a.dry_run:
                    continue
                body = litfetch.get(f"https://archive.org/download/{item}/{item}.pdf")
                if body[:4] != b"%PDF":
                    log.info(f"{pid}: not a PDF ({len(body)} bytes); stop")
                    return 1
                vol.write_bytes(body)
            src = fitz.open(vol)
            out = fitz.open()
            out.insert_pdf(src, from_page=lo, to_page=hi)
            log.info(
                f"{pid}: leaves {lo}-{hi} ({out.page_count} pages) of {item}; "
                f"first {first_line(out[0])!r}; last {first_line(out[-1])!r}"
            )
            log.event("cut", "ok", paper_id=pid, item=item, first_leaf=lo, last_leaf=hi, pages=out.page_count)
            if not a.dry_run:
                out.save(INBOX / f"{pid}.pdf", garbage=3, deflate=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
