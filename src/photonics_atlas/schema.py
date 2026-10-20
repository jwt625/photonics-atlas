"""Load and merge data/schema/*.schema.yaml (registry + component atlas) and the component parameter registry."""

from __future__ import annotations

from typing import Any

import yaml

from .paths import ROOT, SCHEMA

# Registry first; each atlas tranche adds its own schema file (missing files are skipped).
SCHEMA_FILES = [
    SCHEMA,
    ROOT / "data" / "schema" / "components.schema.yaml",
    ROOT / "data" / "schema" / "supply.schema.yaml",
    ROOT / "data" / "schema" / "people.schema.yaml",
]
PARAMETERS = ROOT / "data" / "schema" / "component_parameters.yaml"


def load_schema() -> dict[str, Any]:
    """Registry schema with the component schema merged in (patterns, enums and tables must not collide)."""
    merged: dict[str, Any] = {"patterns": {}, "enums": {}, "tables": {}}
    for path in SCHEMA_FILES:
        if not path.exists():
            continue
        with path.open() as f:
            data: dict[str, Any] = yaml.safe_load(f)
        for part in ("patterns", "enums", "tables"):
            for k, v in (data.get(part) or {}).items():
                if k in merged[part] and merged[part][k] != v:
                    raise ValueError(f"{path.name}: {part}.{k} collides with another schema file")
                merged[part][k] = v
    return merged


def columns(table: str) -> list[str]:
    return [c["name"] for c in load_schema()["tables"][table]["columns"]]


def load_parameters() -> dict[str, Any]:
    with PARAMETERS.open() as f:
        data: dict[str, Any] = yaml.safe_load(f)
    return data
