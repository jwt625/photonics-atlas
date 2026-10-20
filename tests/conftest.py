"""Tests run on the real inputs (sibling repos) and the real registry. Input-dependent tests skip when the sibling
repos are not present (e.g. a fresh clone of this repo alone)."""

from __future__ import annotations

import pytest

from photonics_atlas.paths import input_path


def have_inputs() -> bool:
    return all(input_path(k).exists() for k in ("eo_atlas", "pk_atlas", "lineage", "ofc_metadata"))


needs_inputs = pytest.mark.skipif(not have_inputs(), reason="sibling input repos not present")
