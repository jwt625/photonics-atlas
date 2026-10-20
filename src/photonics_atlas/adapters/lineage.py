"""PlayGround/20260823_photonics_lineage canonical YAML (read-only): organizations, events, sources."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel

from ..paths import input_path


class LinAlias(BaseModel):
    name: str
    language: str | None = None
    alias_type: str


class LinOrg(BaseModel):
    id: str
    name: str
    aliases: list[LinAlias]
    organization_type: str
    parent_organization_id: str | None = None
    predecessor_ids: list[str] = []
    successor_ids: list[str] = []
    founded_date: str | None = None
    dissolved_date: str | None = None
    status: str
    website: str | None = None
    countries: list[str] = []
    notes: str | None = None


class LinParticipant(BaseModel):
    entity_id: str
    role: str


class LinSourceRef(BaseModel):
    source_id: str
    supports: str | None = None
    locator: str | None = None


class LinEvent(BaseModel):
    id: str
    event_type: str
    name: str
    participants: list[LinParticipant]
    announced_date: str | None
    effective_date: str | None
    grade: str
    sources: list[LinSourceRef]
    rationale: str | None = None
    notes: str | None = None


class LinSource(BaseModel):
    id: str
    url: str
    title: str
    publisher: str
    publication_date: str | None
    accessed_date: str
    source_type: str
    evidence_grade: str
    notes: str | None = None


def _load(name: str, root: Path | None) -> list[dict[str, Any]]:
    path = (root or input_path("lineage")) / "canonical" / f"{name}.yaml"
    with path.open() as f:
        data: dict[str, Any] = yaml.safe_load(f)
    items: list[dict[str, Any]] = data[name]
    return items


def _date(v: dict[str, Any] | None) -> str | None:
    """LIN date_value -> ISO partial string (precision kept by length)."""
    if not v or v.get("value") in (None, ""):
        return None
    return str(v["value"])


def orgs(root: Path | None = None) -> list[LinOrg]:
    out = []
    for o in _load("organizations", root):
        out.append(
            LinOrg(
                id=o["id"],
                name=o["name"],
                aliases=[LinAlias(**a) for a in o.get("aliases") or []],
                organization_type=o["organization_type"],
                parent_organization_id=o.get("parent_organization_id"),
                predecessor_ids=o.get("predecessor_ids") or [],
                successor_ids=o.get("successor_ids") or [],
                founded_date=_date(o.get("founded_date")),
                dissolved_date=_date(o.get("dissolved_date")),
                status=o["status"],
                website=o.get("website"),
                countries=[g["country_code"] for g in o.get("geographies") or [] if g.get("country_code")],
                notes=o.get("notes"),
            )
        )
    return out


def events(root: Path | None = None) -> list[LinEvent]:
    out = []
    for e in _load("events", root):
        ev = e["evidence"]
        out.append(
            LinEvent(
                id=e["id"],
                event_type=e["event_type"],
                name=e["name"],
                participants=[LinParticipant(**p) for p in e["participants"]],
                announced_date=_date(e.get("announced_date")),
                effective_date=_date(e.get("effective_date")),
                grade=ev["grade"],
                sources=[
                    LinSourceRef(**{k: s.get(k) for k in ("source_id", "supports", "locator")}) for s in ev["sources"]
                ],
                rationale=ev.get("rationale"),
                notes=e.get("notes"),
            )
        )
    return out


def sources(root: Path | None = None) -> list[LinSource]:
    out = []
    for s in _load("sources", root):
        out.append(
            LinSource(
                id=s["id"],
                url=s["url"],
                title=s["title"],
                publisher=s["publisher"],
                publication_date=_date(s.get("publication_date")),
                accessed_date=str(s["accessed_date"]),
                source_type=s["source_type"],
                evidence_grade=s["evidence_grade"],
                notes=s.get("notes"),
            )
        )
    return out
