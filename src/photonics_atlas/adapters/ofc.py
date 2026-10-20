"""OFC 2026 presentation metadata (read-only): PlayGround/ofc-2026/ofc_full_metadata.json.

D24: one author row per authors_json element, date = local date of session_start, emails stripped from every text
field before it leaves this module. presenter_affiliation is empty on all records and is ignored.
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel

from ..paths import input_path
from ..textnorm import strip_emails


class OfcAuthor(BaseModel):
    index: int
    name: str
    affiliation: str


class OfcPresentation(BaseModel):
    code: str
    title: str
    session_code: str
    session_title: str
    session_date: str
    authors: list[OfcAuthor]
    text_cached: bool


def presentations(metadata: Path | None = None, text_dir: Path | None = None) -> list[OfcPresentation]:
    path = metadata or input_path("ofc_metadata")
    tdir = text_dir or input_path("ofc_text_dir")
    cached = {p.name.split("-", 1)[0] for p in tdir.glob("*.md")} if tdir.is_dir() else set()
    with path.open() as f:
        recs = json.load(f)
    out = []
    for r in recs:
        if r.get("record_kind") != "presentation":
            continue
        authors = [
            OfcAuthor(
                index=i + 1,
                name=strip_emails(a.get("name") or ""),
                affiliation=strip_emails(a.get("affiliation") or ""),
            )
            for i, a in enumerate(json.loads(r.get("authors_json") or "[]"))
        ]
        code = r["presentation_code"]
        out.append(
            OfcPresentation(
                code=code,
                title=strip_emails(r.get("presentation_title") or ""),
                session_code=r.get("session_code") or "",
                session_title=strip_emails(r.get("session_title") or ""),
                session_date=(r.get("session_start") or "")[:10],
                authors=authors,
                text_cached=code in cached,
            )
        )
    return out
