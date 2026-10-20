"""eo-modulator-atlas (read-only): organizations, sites, author affiliations, papers."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from ..csvio import read_csv, split_list
from ..paths import input_path


class EoOrg(BaseModel):
    org_name: str
    org_type: str
    country: str
    region: str
    parent_org: str
    notes: str
    ror_id: str
    name_source: str


class EoSite(BaseModel):
    org_name: str
    locality: str
    country: str
    source: str
    source_ref: str


class EoAffiliation(BaseModel):
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


class EoPaper(BaseModel):
    paper_id: str
    title: str
    authors: list[str]
    year: int
    published_on: str
    venue: str
    doi: str
    arxiv_id: str
    url: str
    source_type: str
    access: str
    license: str
    redistribution: str
    cache_status: str
    foundry_or_fab: list[str]
    wafer_supplier: str
    process_name: str


def _data(root: Path | None) -> Path:
    return (root or input_path("eo_atlas")) / "data"


def orgs(root: Path | None = None) -> list[EoOrg]:
    return [EoOrg(**r) for r in read_csv(_data(root) / "organizations.csv")]


def sites(root: Path | None = None) -> list[EoSite]:
    keep = EoSite.model_fields.keys()
    return [EoSite(**{k: r[k] for k in keep}) for r in read_csv(_data(root) / "org_sites.csv")]


def affiliations(root: Path | None = None) -> list[EoAffiliation]:
    keep = EoAffiliation.model_fields.keys()
    return [
        EoAffiliation.model_validate({k: r[k] for k in keep}) for r in read_csv(_data(root) / "author_affiliations.csv")
    ]


def papers(root: Path | None = None) -> list[EoPaper]:
    out = []
    for r in read_csv(_data(root) / "papers.csv"):
        out.append(
            EoPaper(
                **{k: r[k] for k in EoPaper.model_fields if k not in {"authors", "foundry_or_fab", "year"}},
                authors=split_list(r["authors"]),
                foundry_or_fab=split_list(r["foundry_or_fab"]),
                year=int(r["year"]),
            )
        )
    return out


class EoDevice(BaseModel):
    device_id: str
    paper_id: str
    device_label: str
    device_class: str
    row_kind: str
    waveguide_platform: str
    band: str
    wavelength_nm: str


def devices(root: Path | None = None) -> list[EoDevice]:
    keep = EoDevice.model_fields.keys()
    return [EoDevice(**{k: r[k] for k in keep}) for r in read_csv(_data(root) / "devices.csv")]


def reference_dir(paper_id: str, root: Path | None = None) -> Path:
    """references/<paper_id>/ of the EO atlas (text.md + figures; read-only, local-only for restricted sources)."""
    return (root or input_path("eo_atlas")) / "references" / paper_id
