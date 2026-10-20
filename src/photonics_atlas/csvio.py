"""CSV read/write with schema column order."""

from __future__ import annotations

import csv
from collections.abc import Iterable, Mapping
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return [dict(r) for r in csv.DictReader(f)]


def read_header(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8") as f:
        return next(csv.reader(f), [])


def write_csv(path: Path, columns: list[str], rows: Iterable[Mapping[str, object]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({c: _cell(r.get(c)) for c in columns})
            n += 1
    return n


def _cell(v: object) -> str:
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (list, tuple)):
        return ";".join(str(x) for x in v)
    return str(v)


def split_list(cell: str) -> list[str]:
    return [p.strip() for p in cell.split(";") if p.strip()]
