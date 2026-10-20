"""Blog-hosted PDFs listed by the 2026-10-20 blog harvest (DevLog/research/blog_harvest/local_pdfs.csv)."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from ..csvio import read_csv
from ..paths import input_path


class BlogPdf(BaseModel):
    path: str
    filename_title: str
    topic_guess: str
    title_source: str


def pdfs(path: Path | None = None) -> list[BlogPdf]:
    return [BlogPdf(**r) for r in read_csv(path or input_path("blog_local_pdfs"))]
