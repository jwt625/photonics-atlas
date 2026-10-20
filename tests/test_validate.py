"""Validator rules, each checked on a copy of the real registry with one deliberate defect (P0 code audit probes)."""

from __future__ import annotations

import shutil
from collections.abc import Callable
from pathlib import Path

import pytest

from photonics_atlas.csvio import read_csv, write_csv
from photonics_atlas.paths import ROOT
from photonics_atlas.schema import columns
from photonics_atlas.validate import pdate_hi, pdate_ok, validate

Rows = list[dict[str, str]]


def test_real_registry_has_no_errors() -> None:
    assert validate().errors == []


@pytest.fixture()
def reg(tmp_path: Path) -> Path:
    for d in ("data/registry", "data/crosswalk"):
        shutil.copytree(ROOT / d, tmp_path / d)
    return tmp_path


def _edit(root: Path, table: str, fn: Callable[[Rows], None]) -> None:
    sub = "crosswalk" if table == "org_crosswalk" else "registry"
    path = root / "data" / sub / f"{table}.csv"
    rows = read_csv(path)
    fn(rows)
    write_csv(path, columns(table), rows)


def _row(rows: Rows, **match: str) -> dict[str, str]:
    return next(r for r in rows if all(r[k] == v for k, v in match.items()))


def _errors(root: Path) -> list[str]:
    return validate(root).errors


def test_orphan_parent(reg: Path) -> None:
    _edit(reg, "organizations", lambda rows: rows[0].update(parent_org_id="org_does_not_exist"))
    assert any("orphan" in e for e in _errors(reg))


def test_date_order_format_and_bounds(reg: Path) -> None:
    def bad(rows: Rows) -> None:
        rows[0].update(founded_on="2020", dissolved_on="2019-05")
        rows[1].update(founded_on="20-01-2020")
        rows[2].update(founded_on="0000")
        rows[3].update(founded_on="2020-1", dissolved_on="2021")  # used to crash pdate_lo

    _edit(reg, "organizations", bad)
    errs = _errors(reg)
    assert any("after dissolved_on" in e for e in errs)
    assert sum("not an ISO date" in e for e in errs) == 3


def test_unknown_grade_reports_instead_of_crashing(reg: Path) -> None:
    _edit(reg, "org_events", lambda rows: rows[0].update(grade="E"))
    assert any("not in enum grade" in e for e in _errors(reg))


def test_grade_status_and_locator(reg: Path) -> None:
    def bad(rows: Rows) -> None:
        rows[0].update(grade="C", status="validated")
        _row(rows, basis="stated_in_source").update(locator="-")
        [r for r in rows if r["basis"] == "stated_in_source"][1].update(locator="x" * 400)

    _edit(reg, "org_events", bad)
    errs = _errors(reg)
    assert any("incompatible with grade C" in e for e in errs)
    assert sum("locator must be a quote" in e for e in errs) == 2


def test_roles_per_event_type(reg: Path) -> None:
    def bad(rows: Rows) -> None:
        p = _row(rows, event_id="event_acquisition_finisar_ii_vi_2019", role="acquirer")
        rows.append({**p, "role": "spun_off"})

    _edit(reg, "org_event_participants", bad)
    assert any("not allowed for acquisition" in e for e in _errors(reg))


def test_event_grade_not_better_than_sources(reg: Path) -> None:
    def bad(rows: Rows) -> None:
        for r in rows:
            if r["corpus"] == "web":
                r["evidence_grade"] = "D"

    _edit(reg, "sources", bad)
    assert any("better than its best cited source grade" in e for e in _errors(reg))


def test_event_sources_must_be_documents(reg: Path) -> None:
    _edit(reg, "org_events", lambda rows: _row(rows, basis="stated_in_source").update(source_ids="eo:aihara2026"))
    assert any("event sources must be" in e for e in _errors(reg))


def test_imported_lineage_anchor(reg: Path) -> None:
    def bad(rows: Rows) -> None:
        _row(rows, basis="imported_lineage").update(locator="lin:canonical/events.yaml#event_other")

    _edit(reg, "org_events", bad)
    assert any("imported_lineage locator must be" in e for e in _errors(reg))


def test_missing_built_table_is_an_error(reg: Path) -> None:
    (reg / "data" / "registry" / "org_events.csv").unlink()
    assert any("org_events.csv: missing" in e for e in _errors(reg))


def test_list_int_country_cells(reg: Path) -> None:
    _edit(reg, "organizations", lambda rows: rows[0].update(origin=";", country="XX"))
    _edit(reg, "org_crosswalk", lambda rows: rows[0].update(n_rows="1_000"))
    errs = _errors(reg)
    assert any("empty list" in e for e in errs)
    assert any("not a known ISO 3166-1" in e for e in errs)
    assert any("not an int" in e for e in errs)


def test_rights_rule_for_non_oa_corpora(reg: Path) -> None:
    _edit(reg, "sources", lambda rows: _row(rows, corpus="ofc2026").update(redistribution="open_license_ok"))
    assert any("restricted_local_only" in e for e in _errors(reg))


def test_crosswalk_acceptance_and_staleness(reg: Path) -> None:
    def bad(rows: Rows) -> None:
        _row(rows, corpus="eo").update(org_ids="", match_basis="unmapped")
        _row(rows, corpus="ofc2026", match_basis="name").update(org_ids="org_coherent_inc")

    _edit(reg, "org_crosswalk", bad)
    errs = _errors(reg)
    assert any("unmapped (P0 acceptance)" in e for e in errs)
    assert any("is stale" in e for e in errs)


def test_alias_collision_and_scope_order(reg: Path) -> None:
    orgs = read_csv(reg / "data" / "registry" / "organizations.csv")

    def bad(rows: Rows) -> None:
        rows[0].update(alias_type="nickname")
        rows.append({**rows[1], "alias": orgs[5]["name"], "org_id": orgs[6]["org_id"], "scope": ""})
        rows.append(
            {
                **rows[1],
                "alias": "Zq Test Lab",
                "org_id": orgs[7]["org_id"],
                "scope": "ofc2026;eo",
                "alias_type": "printed_variant",
            }
        )
        rows.append(
            {
                **rows[1],
                "alias": "Zq Test Lab",
                "org_id": orgs[8]["org_id"],
                "scope": "eo;ofc2026",
                "alias_type": "printed_variant",
            }
        )

    _edit(reg, "org_aliases", bad)
    errs = _errors(reg)
    assert any("not in enum alias_type" in e for e in errs)
    assert any("collides with the name of" in e for e in errs)
    assert any("'zq test lab'" in e and "joint_printed" in e for e in errs)


def test_name_basis_vs_origin(reg: Path) -> None:
    _edit(reg, "organizations", lambda rows: _row(rows, origin="ofc2026").update(name_basis="eo_atlas"))
    assert any("lacks ['eo']" in e for e in _errors(reg))


def test_partial_dates() -> None:
    assert pdate_ok("2025") and pdate_ok("2025-04") and pdate_ok("2025-04-01") and pdate_ok("0976")
    assert not pdate_ok("2025-13") and not pdate_ok("2025-02-30") and not pdate_ok("976") and not pdate_ok("2999")
    assert pdate_hi("2024-02") == "2024-02-29"
