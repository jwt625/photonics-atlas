"""Normalized literature pool records (DevLog-006 S1): one JSON object per work, shared by every scouting lane.

Pool files: cache/literature/pool/<lane>_<name>.jsonl (git-ignored; abstracts are publisher text). Fields:
  uid             doi (lowercase, no prefix) | "arxiv:<id without version>" | "openalex:W..."
  doi, arxiv_id, openalex_id, title, year, publication_date, type (OpenAlex type: article, review, preprint, ...)
  venue, venue_type   source display name; journal | conference | repository | other
  authors         display names in order (first 30), n_authors, last_author
  institutions    institution display names of the first and last author (deduped)
  abstract        reconstructed from OpenAlex abstract_inverted_index (or Crossref JATS stripped), "" if absent
  is_oa, oa_status, oa_url, license
  cited_by_count
  lane, discovered_via, harvested_on (ISO date)
"""

from __future__ import annotations

import datetime as dt
import json
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from .paths import CACHE

POOL = CACHE / "literature" / "pool"

# Pass as `select=` on OpenAlex list requests so pages stay small.
OPENALEX_SELECT = (
    "id,doi,title,publication_year,publication_date,type,primary_location,authorships,abstract_inverted_index,"
    "open_access,best_oa_location,cited_by_count,ids"
)

_ARXIV_DOI = re.compile(r"^10\.48550/arxiv\.(.+)$", re.I)
_TAGS = re.compile(r"<[^>]+>")


def abstract_from_inverted(inv: dict[str, list[int]] | None) -> str:
    if not inv:
        return ""
    pos = {i: w for w, idx in inv.items() for i in idx}
    return " ".join(pos[i] for i in sorted(pos))


def strip_jats(text: str | None) -> str:
    return re.sub(r"\s+", " ", _TAGS.sub(" ", text or "")).strip()


def norm_doi(doi: str | None) -> str:
    d = (doi or "").strip().lower()
    for p in ("https://doi.org/", "http://doi.org/", "doi:"):
        if d.startswith(p):
            d = d[len(p) :]
    return d


def norm_title(title: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (title or "").lower()).strip()


def make_uid(doi: str, arxiv_id: str, openalex_id: str) -> str:
    if doi and not _ARXIV_DOI.match(doi):
        return doi
    if arxiv_id:
        return f"arxiv:{arxiv_id}"
    if doi:
        return doi
    return f"openalex:{openalex_id}"


def from_openalex(w: dict[str, Any], lane: str, discovered_via: str) -> dict[str, Any]:
    doi = norm_doi(w.get("doi"))
    arxiv_id = ""
    m = _ARXIV_DOI.match(doi)
    if m:
        arxiv_id = re.sub(r"v\d+$", "", m.group(1))
    oa_id = (w.get("id") or "").rsplit("/", 1)[-1]
    loc = w.get("primary_location") or {}
    src = loc.get("source") or {}
    auths = w.get("authorships") or []
    names = [((a.get("author") or {}).get("display_name") or "") for a in auths]
    inst: list[str] = []
    for a in auths[:1] + auths[-1:]:
        for i in a.get("institutions") or []:
            n = i.get("display_name") or ""
            if n and n not in inst:
                inst.append(n)
    oa = w.get("open_access") or {}
    best = w.get("best_oa_location") or {}
    stype = src.get("type") or ""
    return {
        "uid": make_uid(doi, arxiv_id, oa_id),
        "doi": "" if arxiv_id else doi,
        "arxiv_id": arxiv_id,
        "openalex_id": oa_id,
        "title": (w.get("title") or "").strip(),
        "year": w.get("publication_year"),
        "publication_date": w.get("publication_date") or "",
        "type": w.get("type") or "",
        "venue": src.get("display_name") or "",
        "venue_type": stype if stype in ("journal", "conference", "repository") else "other",
        "authors": names[:30],
        "n_authors": len(names),
        "last_author": names[-1] if names else "",
        "institutions": inst,
        "abstract": abstract_from_inverted(w.get("abstract_inverted_index")),
        "is_oa": bool(oa.get("is_oa")),
        "oa_status": oa.get("oa_status") or "",
        "oa_url": oa.get("oa_url") or best.get("pdf_url") or "",
        "license": best.get("license") or loc.get("license") or "",
        "cited_by_count": w.get("cited_by_count") or 0,
        "lane": lane,
        "discovered_via": discovered_via,
        "harvested_on": dt.date.today().isoformat(),
    }


def append(path: Path, records: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("a", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            n += 1
    return n


def read(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]
