"""advanced-packaging-atlas (read-only): metrics.csv rows and the test-vehicle -> paper map (P2 reliability tests)."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from ..csvio import read_csv
from ..paths import input_path


class PkMetric(BaseModel):
    metric_id: str
    tv_id: str
    category: str
    parameter: str
    variant: str
    value: str
    value_text: str
    unit: str
    statistic: str
    n_samples: str
    condition: str
    test_standard: str
    pass_criterion: str
    result: str
    scope: str
    basis: str
    locator: str
    notes: str


def _data(root: Path | None) -> Path:
    return (root or input_path("pk_atlas")) / "data"


def metrics(root: Path | None = None) -> list[PkMetric]:
    keep = PkMetric.model_fields.keys()
    return [PkMetric(**{k: r[k] for k in keep}) for r in read_csv(_data(root) / "metrics.csv")]


def tv_papers(root: Path | None = None) -> dict[str, str]:
    """tv_id -> paper_id from test_vehicles.csv."""
    return {r["tv_id"]: r["paper_id"] for r in read_csv(_data(root) / "test_vehicles.csv")}
