"""Offline ROR index from the cached data dump (CC0; cache/ror/). Exact normalized-name lookup only (D25)."""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from ..paths import ROOT, input_path
from ..textnorm import norm_key

_LANG = re.compile(r"^[a-z_]+:\s*")


@dataclass
class RorRecord:
    ror_id: str
    name: str
    country: str
    types: list[str]
    status: str
    website: str
    wikidata: str
    established: str
    labels: list[str]
    aliases: list[str]
    acronyms: list[str]
    parents: list[str]


@dataclass
class RorIndex:
    version: str
    records: dict[str, RorRecord] = field(default_factory=dict)
    by_key: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    by_alias_key: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))

    def lookup(self, name: str, aliases: bool = False) -> list[RorRecord]:
        """Active records whose display name or label (or, with aliases=True, alias) has the same normalized key.

        Alias fields of ROR subsidiary records often carry the parent's brand (e.g. a regional subsidiary listing the
        group name), so alias hits are review candidates, not automatic matches.
        """
        k = norm_key(name)
        if " " not in k and len(k) <= 4:
            return []  # bare acronyms (TI, IDT, CNRS) hit unrelated records; resolved by curation instead
        ids = self.by_alias_key.get(k, set()) if aliases else self.by_key.get(k, set())
        return [self.records[i] for i in sorted(ids) if self.records[i].status == "active"]


def _names(cell: str) -> list[str]:
    return [_LANG.sub("", p).strip() for p in cell.split("; ") if p.strip()]


def ror_version() -> str:
    with (ROOT / "config" / "inputs.yaml").open() as f:
        return str(yaml.safe_load(f)["ror_version"])


def load(cache_dir: Path | None = None) -> RorIndex:
    d = cache_dir or input_path("ror_cache")
    path = d / f"{ror_version()}-ror-data.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} missing: download the pinned ROR dump (config/inputs.yaml ror_version, README)"
        )
    idx = RorIndex(version=path.stem)
    csv.field_size_limit(10_000_000)
    with path.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rel = r.get("relationships") or ""
            parents = []
            for part in rel.split("; "):
                if part.startswith("parent:"):
                    parents += [x.strip() for x in part[len("parent:") :].split(",") if x.strip()]
            rec = RorRecord(
                ror_id=r["id"],
                name=r["names.types.ror_display"],
                country=r["locations.geonames_details.country_code"].split(";")[0].strip(),
                types=[t.strip() for t in r["types"].split(";") if t.strip()],
                status=r["status"],
                website=r["links.type.website"],
                wikidata=(r["external_ids.type.wikidata.preferred"] or r["external_ids.type.wikidata.all"])
                .split(";")[0]
                .strip(),
                established=r["established"].strip().zfill(4) if r["established"].strip() else "",
                labels=_names(r["names.types.label"]),
                aliases=_names(r["names.types.alias"]),
                acronyms=_names(r["names.types.acronym"]),
                parents=parents,
            )
            idx.records[rec.ror_id] = rec
            for n in [rec.name, *rec.labels]:
                k = norm_key(n)
                if k:
                    idx.by_key[k].add(rec.ror_id)
            for n in rec.aliases:
                k = norm_key(n)
                if k:
                    idx.by_alias_key[k].add(rec.ror_id)
    return idx
