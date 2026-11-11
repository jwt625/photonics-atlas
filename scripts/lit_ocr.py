"""OCR for cached literature PDFs without a usable text layer (scans: archive.org BSTJ, pre-1990 publisher scans)
(DevLog-016 D958 / D965). macOS Vision (VNRecognizeTextRequest, accurate, language correction), the approach of the
blog repo's scripts/ofc2026_ocr.py.

Per paper: every page rendered at --dpi (default 200) to cache/literature/ocr/<paper_id>/page_NNN.png, OCR by a
Swift helper compiled once to cache/literature/ocr/vision_ocr, then references/<paper_id>/text.md rewritten with the
lit_extract.py layout (YAML header + "<!-- page N -->" markers); a non-empty PyMuPDF text layer is kept as
references/<paper_id>/text_pymupdf.md. source.json gets text_chars, ocr_on, ocr_method, ocr_languages, and the
low_text / garbled_text_layer flags are kept for the record. Figures are not touched (lit_extract.py made them).
Do not run lit_extract.py --force on an OCR'd paper without re-running this script.

Selection: --paper-ids a,b or --pending (source.json flags low_text or garbled_text_layer, no ocr_on). Languages:
en-US by default; --lang adds e.g. de-DE / fr-FR for German / French originals.

Usage: uv run python scripts/lit_ocr.py (--paper-ids a,b | --pending) [--lang de-DE,fr-FR] [--dpi 200] [--force]
       [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import pymupdf

from photonics_atlas.paths import CACHE, ROOT
from photonics_atlas.runlog import RunLog

fitz: Any = pymupdf
REFS = ROOT / "references"
OCR_DIR = CACHE / "literature" / "ocr"
BIN = OCR_DIR / "vision_ocr"
FLAGS = ("low_text", "garbled_text_layer")
BATCH = 40  # pages per Swift call

SWIFT_SOURCE = r"""
import AppKit
import Foundation
import Vision

struct OCRResult: Codable {
    let imagePath: String
    let lines: [String]
    let error: String?
}

let args = Array(CommandLine.arguments.dropFirst())
let langs = args.first.map { $0.split(separator: ",").map(String.init) } ?? ["en-US"]
let paths = Array(args.dropFirst())

func recognize(_ path: String) -> OCRResult {
    let url = URL(fileURLWithPath: path)
    guard let image = NSImage(contentsOf: url), let tiff = image.tiffRepresentation,
          let bitmap = NSBitmapImageRep(data: tiff), let cg = bitmap.cgImage else {
        return OCRResult(imagePath: path, lines: [], error: "image load failed")
    }
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = true
    request.recognitionLanguages = langs
    do {
        try VNImageRequestHandler(cgImage: cg, options: [:]).perform([request])
        let obs = (request.results ?? []).sorted {
            // top-to-bottom, then left-to-right (Vision origin is bottom-left)
            abs($0.boundingBox.midY - $1.boundingBox.midY) > 0.01
                ? $0.boundingBox.midY > $1.boundingBox.midY : $0.boundingBox.minX < $1.boundingBox.minX
        }
        return OCRResult(imagePath: path, lines: obs.compactMap { $0.topCandidates(1).first?.string }, error: nil)
    } catch {
        return OCRResult(imagePath: path, lines: [], error: String(describing: error))
    }
}

let data = try JSONEncoder().encode(paths.map(recognize))
FileHandle.standardOutput.write(data)
"""


def build_helper(log: RunLog) -> None:
    OCR_DIR.mkdir(parents=True, exist_ok=True)
    src = OCR_DIR / "vision_ocr.swift"
    if BIN.exists() and src.exists() and src.read_text() == SWIFT_SOURCE:
        return
    src.write_text(SWIFT_SOURCE)
    log.info("compiling the Vision OCR helper")
    subprocess.run(["swiftc", "-O", str(src), "-o", str(BIN)], check=True)


def ocr_pages(images: list[Path], langs: str) -> list[list[str]]:
    out: list[list[str]] = []
    for i in range(0, len(images), BATCH):
        chunk = images[i : i + BATCH]
        res = subprocess.run([str(BIN), langs, *map(str, chunk)], capture_output=True, text=True, check=True)
        items = json.loads(res.stdout)
        for it in items:
            if it.get("error"):
                raise RuntimeError(f"{it['imagePath']}: {it['error']}")
            out.append([str(x) for x in it["lines"]])
    return out


CAPTION = re.compile(r"^\s*(Fig\.?|FIG\.?|Figure|FIGURE|Table|TABLE)\s*[\dIVX]+")


def add_caption_pages(pid: str, log: RunLog) -> int:
    """Render (150 dpi) every page whose OCR text has a figure / table caption and has no figures/page_NN.png yet, and
    add it to figures/figures.json (the lit_extract.py layout), so a key figure can be chosen on scanned papers."""
    d = REFS / pid
    text = (d / "text.md").read_text(encoding="utf-8")
    fig_dir = d / "figures"
    fig_dir.mkdir(exist_ok=True)
    index_path = fig_dir / "figures.json"
    index: list[dict[str, Any]] = json.loads(index_path.read_text()) if index_path.exists() else []
    doc = fitz.open(d / "source.pdf")
    added = 0
    for chunk in text.split("<!-- page ")[1:]:
        num_s, _, body = chunk.partition(" -->")
        page = int(num_s)
        caps = [ln.strip() for ln in body.splitlines() if CAPTION.match(ln)]
        name = f"page_{page:02d}.png"
        if not caps or (fig_dir / name).exists():
            continue
        doc[page - 1].get_pixmap(dpi=150).save(fig_dir / name)
        index.append({"kind": "page_render", "file": name, "page": page, "captions": caps, "source": "lit_ocr"})
        added += 1
    if added:
        index.sort(key=lambda e: (e.get("page", 0), e.get("kind") != "page_render", e.get("file", "")))
        index_path.write_text(json.dumps(index, indent=1) + "\n")
        log.info(f"{pid}: {added} caption page render(s) added")
    return added


def pending() -> list[str]:
    ids = []
    for meta in sorted(REFS.glob("*/source.json")):
        m = json.loads(meta.read_text())
        flagged = any(m.get(f) for f in FLAGS)
        if flagged and not m.get("ocr_on") and (meta.parent / "source.pdf").exists():
            ids.append(meta.parent.name)
    return ids


def run_one(pid: str, langs: str, dpi: int, force: bool, dry: bool, log: RunLog) -> None:
    d = REFS / pid
    meta_path = d / "source.json"
    pdf = d / "source.pdf"
    if not pdf.exists() or not meta_path.exists():
        log.info(f"{pid}: no source.pdf / source.json (run lit_extract.py first)")
        log.event("ocr", "missing", paper_id=pid)
        return
    meta = json.loads(meta_path.read_text())
    if meta.get("ocr_on") and not force:
        log.event("ocr", "skip_done", paper_id=pid)
        return
    doc = fitz.open(pdf)
    n = doc.page_count
    log.info(f"{pid}: {n} pages at {dpi} dpi, languages {langs}")
    if dry:
        return
    work = OCR_DIR / pid
    work.mkdir(parents=True, exist_ok=True)
    images = []
    for i, page in enumerate(doc, 1):
        img = work / f"page_{i:03d}.png"
        if not img.exists():
            page.get_pixmap(dpi=dpi).save(img)
        images.append(img)
    pages = ocr_pages(images, langs)
    text_md = d / "text.md"
    if text_md.exists():
        old = text_md.read_text(encoding="utf-8")
        body = old.split("<!-- page 1 -->", 1)[-1]
        if len(body.strip()) > 200 and not (d / "text_pymupdf.md").exists():
            (d / "text_pymupdf.md").write_text(old, encoding="utf-8")
    today = dt.date.today().isoformat()
    head = [
        "---",
        f'paper_id: "{pid}"',
        f'uid: "{meta.get("uid", "")}"',
        f'doi: "{meta.get("doi", "")}"',
        f'arxiv_id: "{meta.get("arxiv_id", "")}"',
        f'url: "{meta.get("url", "")}"',
        f'route: "{meta.get("route", "")}"',
        f'license: "{meta.get("license", "")}"',
        f'sha256: "{meta.get("sha256", "")}"',
        f"pages: {n}",
        f'extracted_on: "{today}"',
        f'extraction_method: "macOS Vision OCR (accurate, {langs}) of {dpi} dpi page renders; line order '
        'top-to-bottom, columns may interleave; read figures and equations from the page renders"',
        "---",
        "",
    ]
    parts = [f"<!-- page {i} -->\n" + "\n".join(lines) + "\n" for i, lines in enumerate(pages, 1)]
    text = "\n".join(head) + "\n".join(parts)
    text_md.write_text(text, encoding="utf-8")
    chars = sum(len(" ".join(p)) for p in pages)
    meta.update(
        text_chars=chars,
        ocr_on=today,
        ocr_method=f"macOS Vision VNRecognizeTextRequest accurate, {dpi} dpi",
        ocr_languages=langs,
    )
    meta_path.write_text(json.dumps(meta, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    log.info(f"{pid}: OCR {chars} chars over {n} pages")
    add_caption_pages(pid, log)
    log.event("ocr", "ok", paper_id=pid, pages=n, chars=chars, languages=langs)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sel = ap.add_mutually_exclusive_group(required=True)
    sel.add_argument("--paper-ids")
    sel.add_argument("--pending", action="store_true")
    ap.add_argument("--lang", default="", help="extra Vision languages, comma separated (en-US always first)")
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--figures-only", action="store_true", help="only add caption page renders (OCR'd papers)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    langs = ",".join(["en-US", *[x for x in a.lang.split(",") if x]])
    ids = pending() if a.pending else [x.strip() for x in a.paper_ids.split(",") if x.strip()]
    rc = 0
    with RunLog("lit_ocr", a.dry_run) as log:
        log.info(f"{len(ids)} paper(s): {', '.join(ids)}")
        if not a.dry_run:
            build_helper(log)
        for pid in ids:
            if a.figures_only:
                if not a.dry_run:
                    add_caption_pages(pid, log)
                continue
            try:
                run_one(pid, langs, a.dpi, a.force, a.dry_run, log)
            except (subprocess.CalledProcessError, RuntimeError, json.JSONDecodeError) as e:
                rc = 2
                log.info(f"{pid}: FAILED {e}")
                log.event("ocr", "failed", paper_id=pid, error=str(e)[:300])
    return rc


if __name__ == "__main__":
    sys.exit(main())
