"""Repo paths and read-only input locations (config/inputs.yaml)."""

from __future__ import annotations

import os
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "data" / "schema" / "registry.schema.yaml"
REGISTRY = ROOT / "data" / "registry"
CROSSWALK = ROOT / "data" / "crosswalk"
STAGING = ROOT / "data" / "_staging"
LOGS = ROOT / "logs"
CACHE = ROOT / "cache"

_IN_REPO = {"blog_local_pdfs", "ror_cache"}


def inputs_root() -> Path:
    """Directory holding the sibling input repos (parent of this repo unless overridden)."""
    env = os.environ.get("PHOTONICS_ATLAS_INPUTS_ROOT")
    return Path(env).expanduser().resolve() if env else ROOT.parent


def input_path(key: str) -> Path:
    """Resolve an input named in config/inputs.yaml."""
    with (ROOT / "config" / "inputs.yaml").open() as f:
        cfg: dict[str, str] = yaml.safe_load(f)
    rel = cfg[key]
    return (ROOT / rel) if key in _IN_REPO else (inputs_root() / rel)
