"""advanced-packaging-atlas (read-only): organizations, sites, author affiliations, papers, org alias map."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel

from ..csvio import read_csv
from ..paths import input_path


class PkOrg(BaseModel):
    org_name: str
    org_type: str
    country: str
    region: str
    parent_org: str
    notes: str


class PkSite(BaseModel):
    org_name: str
    locality: str
    country: str
    source: str
    source_ref: str


class PkAffiliation(BaseModel):
    aff_id: str
    paper_id: str
    author_index: int
    author: str
    aff_order: int
    kind: str
    org_name: str
    unit: str
    locality: str
    country: str
    source: str
    locator: str


class PkPaper(BaseModel):
    paper_id: str
    doi: str
    title: str
    year: int
    venue: str
    first_author: str
    source_status: str


def _root(root: Path | None) -> Path:
    return root or input_path("pk_atlas")


def orgs(root: Path | None = None) -> list[PkOrg]:
    return [PkOrg(**r) for r in read_csv(_root(root) / "data" / "organizations.csv")]


def sites(root: Path | None = None) -> list[PkSite]:
    keep = PkSite.model_fields.keys()
    return [PkSite(**{k: r[k] for k in keep}) for r in read_csv(_root(root) / "data" / "org_sites.csv")]


def affiliations(root: Path | None = None) -> list[PkAffiliation]:
    keep = PkAffiliation.model_fields.keys()
    return [
        PkAffiliation.model_validate({k: r[k] for k in keep})
        for r in read_csv(_root(root) / "data" / "author_affiliations.csv")
    ]


def papers(root: Path | None = None) -> list[PkPaper]:
    keep = PkPaper.model_fields.keys()
    return [PkPaper.model_validate({k: r[k] for k in keep}) for r in read_csv(_root(root) / "data" / "papers.csv")]


def alias_map(root: Path | None = None) -> dict[str, list[str]]:
    """config/org_aliases.yaml: canonical PK org_name -> printed names merged into it."""
    with (_root(root) / "config" / "org_aliases.yaml").open() as f:
        data: dict[str, list[str]] = yaml.safe_load(f)
    return {k: [str(v) for v in vs] for k, vs in data.items()}
