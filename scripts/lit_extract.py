"""Extract page-delimited text and figures from cached literature PDFs and write references/<paper_id>/source.json
(DevLog-006 S7; adapted from advanced-packaging-atlas / eo-modulator-atlas scripts/extract_source.py).

Per paper, in references/<paper_id>/ (git-ignored except source.json):
  text.md                  YAML header + PyMuPDF get_text("text") per page with "<!-- page N -->" markers
  figures/page_NN.png      150 dpi render of every page with a figure / table caption
  figures/img_pNN_k.png    embedded raster images >= 150 px on both sides (deduplicated by xref)
  figures/figures.json     index of the figure files
  supplement/              the same for supplement/source.pdf when present (from lit_ingest_inbox.py)
  source.json              paper_id, uid, doi, arxiv_id, url, route, license, access, redistribution, sha256, pages,
                           text_chars, n_figure_files, retrieved_on, extracted_on, garbled flags (+ fetch fields kept)
Garbled text layers are flagged per page (rules in page_garbled); no OCR is run
(`ocr_available` only records whether tesseract is on PATH).

Redistribution: open_license_ok only for a cc-* license of the fetched version (arXiv copies: the arXiv license from
the OAI-PMH record; publisher / repository copies: the OpenAlex best-location license in the local pool); bronze,
paywalled, manual or institution-stamped copies: restricted_local_only; a known non-CC license: restricted_local_only;
no license known: unknown. A value written by the acquiring script (e.g. the browser fetcher) is never relaxed.

Usage: uv run python scripts/lit_extract.py (--paper-ids a,b | --pending) [--force] [--dry-run]
Exit codes: 0 ok, 2 some paper failed to extract (flags such as garbled_text_layer are logged, not errors).
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path
from typing import Any

import pymupdf
from lit_fetch_oa import CACHE_LIST, QUEUE, REFS, derive_route, queue_by_id, read_rows

from photonics_atlas.paths import CACHE, ROOT
from photonics_atlas.runlog import RunLog

fitz: Any = pymupdf  # pymupdf is only partially typed
MERGED = CACHE / "literature" / "merged.jsonl"
CAPTION_RE = re.compile(r"^\s*(Fig\.?|Figure|FIG\.?|Table|TABLE)\s*(S?[\dIVX]+)", re.IGNORECASE)
WORD = re.compile(r"\b[^\W\d_]{2,}\b")
COMMON = re.compile(r"\b(the|and|of|with|for|is|are|was|were|in|to)\b", re.I)
STAMP_RE = re.compile(r"Authorized licensed use limited to|Downloaded .{0,80} by ")
MIN_IMG_PX = 150
RANK = {"open_license_ok": 0, "unknown": 1, "restricted_local_only": 2}
ACCESS_MAP = {"oa": "open_access", "paywalled": "paywalled"}
POOL_FIELDS = ("license", "oa_status", "type", "publication_date", "venue_type", "oa_url")
KEY_ORDER = (
    "paper_id",
    "uid",
    "doi",
    "arxiv_id",
    "title",
    "url",
    "landing_url",
    "route",
    "access",
    "license",
    "license_source",
    "redistribution",
    "sha256",
    "bytes",
    "pages",
    "text_chars",
    "n_figure_files",
    "retrieved_on",
    "extracted_on",
    "garbled_text_layer",
    "garbled_pages",
    "low_text",
    "ocr_available",
    "institutional_stamp",
)


# ---------------------------------------------------------------- pure helpers (tested)


def utc_date() -> str:
    return dt.datetime.now(dt.UTC).date().isoformat()


def normalize_license(lic: str) -> str:
    """Short lowercase form: cc-by-4.0, cc0-1.0, arxiv-nonexclusive-distrib-1.0, or the input lowercased."""
    s = lic.strip().lower()
    if not s:
        return ""
    m = re.search(r"creativecommons\.org/licenses/([a-z-]+)/([\d.]+)", s)
    if m:
        return f"cc-{m.group(1)}-{m.group(2)}"
    m = re.search(r"creativecommons\.org/publicdomain/zero/([\d.]+)", s)
    if m:
        return f"cc0-{m.group(1)}"
    m = re.search(r"arxiv\.org/licenses/([a-z-]+)/([\d.]+)", s)
    if m:
        return f"arxiv-{m.group(1)}-{m.group(2)}"
    return s


def is_cc(lic: str) -> bool:
    s = normalize_license(lic)
    return s.startswith("cc-") or s.startswith("cc0") or s == "public-domain"


def registry_access(route: str, selection_access: str) -> str:
    if route == "arxiv":
        return "arxiv"
    return ACCESS_MAP.get(selection_access, "unknown")


def redistribution(route: str, lic: str, selection_access: str, oa_status: str, stamped: bool) -> str:
    if stamped or route == "manual":
        return "restricted_local_only"
    if route != "arxiv" and (selection_access == "paywalled" or oa_status == "bronze"):
        return "restricted_local_only"
    if is_cc(lic):
        return "open_license_ok"
    return "restricted_local_only" if lic else "unknown"


def most_restrictive(*values: str) -> str:
    vals = [v for v in values if v in RANK]
    return max(vals, key=lambda v: RANK[v]) if vals else "unknown"


def page_garbled(t: str) -> bool:
    """Font-encoded / shifted text layer on one page (pages with < 300 visible characters are not judged):
    > 5 % control, private-use or replacement characters; or a prose page (>= 80 alphabetic words) with < 3 % common
    English words; or < 30 % letters while < 20 % digits (mostly symbols). Number-dense tables pass (pilot nan2025
    p. 9 was a false positive of the earlier alphabetic-ratio rule)."""
    ns = [c for c in t if not c.isspace()]
    if len(ns) < 300:
        return False
    weird = sum(1 for c in ns if unicodedata.category(c) in ("Cc", "Co", "Cn", "Cs") or c == "\ufffd") / len(ns)
    alpha = sum(c.isalpha() for c in ns) / len(ns)
    digits = sum(c.isdigit() for c in ns) / len(ns)
    words = WORD.findall(t)
    common = len(COMMON.findall(t)) / max(1, len(words))
    return weird > 0.05 or (len(words) >= 80 and common < 0.03) or (alpha < 0.3 and digits < 0.2)


def text_quality(pages: list[str]) -> dict[str, Any]:
    """A document is garbled if any page is (one shifted page is hidden by whole-document averages)."""
    body = "".join(pages)
    n = max(1, len(body))
    bad = [i + 1 for i, t in enumerate(pages) if page_garbled(t)]
    return {
        "digit_ratio": round(sum(c.isdigit() for c in body) / n, 4),
        "common_word_ratio": round(len(COMMON.findall(body)) / max(1, len(WORD.findall(body))), 3),
        "garbled_pages": bad,
        "garbled_text_layer": bool(bad),
    }


def captions_of(text: str) -> list[str]:
    return [ln.strip() for ln in text.splitlines() if CAPTION_RE.match(ln)]


def yaml_header(fields: dict[str, Any]) -> str:
    lines = ["---"] + [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in fields.items()] + ["---", "", ""]
    return "\n".join(lines)


def ordered(meta: dict[str, Any]) -> dict[str, Any]:
    head = {k: meta[k] for k in KEY_ORDER if k in meta}
    return {**head, **{k: v for k, v in meta.items() if k not in head}}


# ---------------------------------------------------------------- inputs


def pool_info(uids: set[str]) -> dict[str, dict[str, Any]]:
    """License / OA status / type / date for the given uids from the local merged pool (git-ignored, may be absent)."""
    out: dict[str, dict[str, Any]] = {}
    if not MERGED.exists() or not uids:
        return out
    with MERGED.open(encoding="utf-8") as f:
        for line in f:
            if not line.startswith('{"uid": "'):
                continue
            end = line.find('"', 9)
            if line[9:end] not in uids:
                continue
            r = json.loads(line)
            out[r["uid"]] = {k: r.get(k) or "" for k in POOL_FIELDS}
            if len(out) == len(uids):
                break
    return out


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------- extraction


def extract_pdf(pdf: Path, out: Path, header: dict[str, Any]) -> dict[str, Any]:
    """text.md + figures/ for one PDF into `out`; returns the extraction statistics."""
    figdir = out / "figures"
    figdir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf)
    texts = [str(page.get_text("text")) for page in doc]
    head = {
        **header,
        "sha256": sha256(pdf),
        "pages": doc.page_count,
        "extracted_on": utc_date(),
        "extraction_method": "pymupdf get_text('text'); tables and equations may be garbled; read figures from "
        "the page renders",
    }
    parts = [yaml_header(head)]
    figures: list[dict[str, Any]] = []
    seen_xref: set[int] = set()
    for pno, (page, text) in enumerate(zip(doc, texts, strict=True), start=1):
        parts.append(f"<!-- page {pno} -->\n{text}\n")
        caps = captions_of(text)
        if caps:
            name = f"page_{pno:02d}.png"
            page.get_pixmap(dpi=150).save(figdir / name)
            figures.append({"kind": "page_render", "file": name, "page": pno, "captions": caps[:12]})
        for n, img in enumerate(page.get_images(full=True), start=1):
            xref = int(img[0])
            if xref in seen_xref:
                continue
            seen_xref.add(xref)
            try:
                pm = fitz.Pixmap(doc, xref)
                if pm.width < MIN_IMG_PX or pm.height < MIN_IMG_PX:
                    continue
                if pm.alpha:
                    pm = fitz.Pixmap(pm, 0)
                if pm.colorspace is None or pm.colorspace.n not in (1, 3):
                    pm = fitz.Pixmap(fitz.csRGB, pm)
                name = f"img_p{pno:02d}_{n}.png"
                pm.save(figdir / name)
                figures.append({"kind": "embedded", "file": name, "page": pno, "width": pm.width, "height": pm.height})
            except Exception as exc:  # noqa: BLE001  pymupdf raises its own error types for unsupported images
                figures.append({"kind": "embedded_failed", "page": pno, "xref": xref, "error": str(exc)[:120]})
    body = "".join(parts)
    (out / "text.md").write_text(body, encoding="utf-8")
    (figdir / "figures.json").write_text(json.dumps(figures, indent=1))
    q = text_quality(texts)
    text_chars = sum(len(t) for t in texts)
    return {
        "sha256": head["sha256"],
        "pages": doc.page_count,
        "text_chars": text_chars,
        "n_figure_files": sum(1 for f in figures if "file" in f),
        "low_text": text_chars < 2000,
        "institutional_stamp": bool(STAMP_RE.search(body)),
        **q,
    }


def build_meta(
    pid: str, existing: dict[str, Any], cache_row: dict[str, str], queue_row: dict[str, str], pool: dict[str, Any]
) -> dict[str, Any]:
    """Identity, route, access and license fields for source.json (no extraction statistics)."""
    route = existing.get("route") or queue_row.get("route") or derive_route(cache_row)
    sel_access = cache_row.get("access", "")
    if route == "arxiv":
        lic = normalize_license(str(existing.get("arxiv_license", "")))
        lic_src = existing.get("license_source", "") if lic else ""
    else:
        lic = normalize_license(str(pool.get("license", "")))
        lic_src = "OpenAlex best OA location license (local pool)" if lic else ""
    arxiv_id = existing.get("arxiv_id") or queue_row.get("arxiv_id") or cache_row.get("arxiv_id", "")
    url = existing.get("url") or queue_row.get("route_url") or cache_row.get("oa_url", "")
    return {
        "paper_id": pid,
        "uid": existing.get("uid") or cache_row.get("uid", ""),
        "doi": existing.get("doi") or cache_row.get("doi", ""),
        "arxiv_id": arxiv_id,
        "title": cache_row.get("title", ""),
        "url": url,
        "route": route,
        "access": registry_access(route, sel_access),
        "selection_access": sel_access,
        "oa_status": pool.get("oa_status", ""),
        "work_type": pool.get("type", ""),
        "venue": cache_row.get("venue", ""),
        "venue_type": cache_row.get("venue_type", ""),
        "year": cache_row.get("year", ""),
        "publication_date": pool.get("publication_date", ""),
        "license": lic,
        "license_source": lic_src,
        "publisher_license": normalize_license(str(pool.get("license", ""))) if route == "arxiv" else "",
    }


def extract(pid: str, cache_row: dict[str, str], queue_row: dict[str, str], pool: dict[str, Any]) -> dict[str, Any]:
    out = REFS / pid
    path = out / "source.json"
    existing: dict[str, Any] = json.loads(path.read_text()) if path.exists() else {}
    if "extracted_on" not in existing and existing.get("redistribution"):
        existing["redistribution_at_fetch"] = existing["redistribution"]
    meta = {**existing, **build_meta(pid, existing, cache_row, queue_row, pool)}
    header = {k: meta.get(k, "") for k in ("paper_id", "uid", "doi", "arxiv_id", "url", "route", "license")}
    stats = extract_pdf(out / "source.pdf", out, header)
    meta.update(stats)
    sup = out / "supplement" / "source.pdf"
    if sup.exists():
        s = extract_pdf(sup, out / "supplement", {**header, "part": "supplement"})
        meta["supplement"] = {
            k: s[k] for k in ("sha256", "pages", "text_chars", "n_figure_files", "garbled_text_layer")
        }
    computed = redistribution(
        meta["route"], meta["license"], meta["selection_access"], meta["oa_status"], bool(stats["institutional_stamp"])
    )
    meta["redistribution"] = most_restrictive(computed, str(meta.get("redistribution_at_fetch", "")) or computed)
    meta["ocr_available"] = shutil.which("tesseract") is not None
    meta["ocr_run"] = False
    meta["extracted_on"] = utc_date()
    meta.setdefault("retrieved_on", "")
    clean = ordered({k: v for k, v in meta.items() if v not in (None, "")})
    path.write_text(json.dumps(clean, indent=1, ensure_ascii=False) + "\n")
    return clean


def pending_ids() -> list[str]:
    if not REFS.exists():
        return []
    out = []
    for pdf in sorted(REFS.glob("*/source.pdf")):
        d = pdf.parent
        if d.name.startswith("_"):
            continue
        sup = d / "supplement" / "source.pdf"
        if not (d / "text.md").exists() or (sup.exists() and not (d / "supplement" / "text.md").exists()):
            out.append(d.name)
    return out


def run(ids: list[str], force: bool, dry_run: bool, log: RunLog) -> int:
    cl = {r["paper_id"]: r for r in read_rows(CACHE_LIST)}
    q = queue_by_id(QUEUE)
    todo = []
    for pid in ids:
        pdf = REFS / pid / "source.pdf"
        if not pdf.exists():
            log.info(f"missing {pdf.relative_to(ROOT)}")
            log.event("extract", "missing_pdf", paper_id=pid)
            continue
        if (REFS / pid / "text.md").exists() and not force and pid not in pending_ids():
            log.event("extract", "skip_existing", paper_id=pid)
            continue
        if pid not in cl:
            log.info(f"warning: {pid} not in cache_list.csv (identity fields from source.json only)")
        todo.append(pid)
    if dry_run:
        for pid in todo:
            log.info(f"would extract {pid}")
        return 0
    pool = pool_info({cl[p]["uid"] for p in todo if p in cl and cl[p].get("uid")})
    bad = 0
    for pid in todo:
        c = cl.get(pid, {})
        try:
            m = extract(pid, c, q.get(pid, {}), pool.get(c.get("uid", ""), {}))
        except Exception as exc:  # noqa: BLE001  a broken PDF must not stop the batch
            bad += 1
            log.info(f"FAILED {pid}: {exc}")
            log.event("extract", "failed", paper_id=pid, error=str(exc)[:300])
            continue
        flags = [f for f in ("garbled_text_layer", "low_text", "institutional_stamp") if m.get(f)]
        log.info(
            f"extracted {pid}: {m['pages']} p, {m['text_chars']} chars, {m['n_figure_files']} figure files, "
            f"{m['redistribution']}" + (f" FLAGS {','.join(flags)}" if flags else "")
        )
        log.event(
            "extract",
            "ok",
            paper_id=pid,
            pages=m["pages"],
            text_chars=m["text_chars"],
            n_figure_files=m["n_figure_files"],
            redistribution=m["redistribution"],
            flags=flags,
        )
    return 2 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--paper-ids", help="comma-separated paper_ids")
    g.add_argument("--pending", action="store_true", help="every references/<id>/source.pdf without text.md")
    ap.add_argument("--force", action="store_true", help="re-extract even when text.md exists")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    ids = pending_ids() if a.pending else [p.strip() for p in a.paper_ids.split(",") if p.strip()]
    with RunLog("lit_extract", a.dry_run) as log:
        log.info(f"{len(ids)} paper(s)")
        return run(ids, a.force, a.dry_run, log)


if __name__ == "__main__":
    sys.exit(main())
