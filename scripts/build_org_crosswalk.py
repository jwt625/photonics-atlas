"""Generate data/crosswalk/org_crosswalk.csv (D25) and report coverage against the P0 acceptance criteria.

Every EO and PK org_name, every LIN org id and every OFC 2026 affiliation string is matched to registry org_ids with
the rules in photonics_atlas.orgmatch. LIN ids map by identity (the registry reuses them, D14).
n_rows: EO/PK = author_affiliations rows printing the org_name (0 for orgs that appear only in organizations.csv);
LIN = 1 per org record; OFC = authors_json rows with that affiliation string.

Usage: uv run python scripts/build_org_crosswalk.py [--dry-run]
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter

from photonics_atlas.adapters import eo, lineage, ofc, pk
from photonics_atlas.csvio import read_csv, write_csv
from photonics_atlas.orgmatch import load_matcher
from photonics_atlas.paths import CROSSWALK, REGISTRY, ROOT
from photonics_atlas.runlog import RunLog
from photonics_atlas.schema import columns


def build(log: RunLog) -> tuple[list[dict[str, object]], dict[str, dict[str, float]]]:
    m = load_matcher()
    reg_ids = {o["org_id"] for o in read_csv(REGISTRY / "organizations.csv")}
    rows: list[dict[str, object]] = []
    stats: dict[str, dict[str, float]] = {}

    def add(corpus: str, counts: Counter[str], names: list[str]) -> None:
        mapped_rows = total_rows = mapped_strings = 0
        for name in names:
            if corpus == "lin":
                ids, basis = ([name], "name") if name in reg_ids else ([], "unmapped")
            else:
                ids, basis = m.match(name, corpus)
            n = counts.get(name, 0)
            rows.append({"corpus": corpus, "printed": name, "org_ids": ids, "match_basis": basis, "n_rows": n})
            total_rows += n
            if ids:
                mapped_rows += n
                mapped_strings += 1
        stats[corpus] = {
            "strings": len(names),
            "strings_mapped": mapped_strings,
            "rows": total_rows,
            "rows_mapped": mapped_rows,
            "row_coverage": round(mapped_rows / total_rows, 4) if total_rows else 1.0,
            "string_coverage": round(mapped_strings / len(names), 4) if names else 1.0,
        }
        log.event("coverage", "ok", corpus=corpus, stats=stats[corpus])

    eo_counts = Counter(a.org_name for a in eo.affiliations())
    add("eo", eo_counts, sorted({o.org_name for o in eo.orgs()} | set(eo_counts)))
    pk_counts = Counter(a.org_name for a in pk.affiliations())
    add("pk", pk_counts, sorted({o.org_name for o in pk.orgs()} | set(pk_counts)))
    lin_ids = [o.id for o in lineage.orgs()]
    add("lin", Counter(lin_ids), sorted(lin_ids))
    ofc_counts = Counter(a.affiliation for p in ofc.presentations() for a in p.authors)
    empty = ofc_counts.pop("", 0)
    add("ofc2026", ofc_counts, sorted(ofc_counts))
    stats["ofc2026"]["rows_with_empty_affiliation"] = empty
    total = stats["ofc2026"]["rows"] + empty
    stats["ofc2026"]["row_coverage_incl_empty"] = round(stats["ofc2026"]["rows_mapped"] / total, 4)
    return rows, stats


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    with RunLog("build_org_crosswalk", args.dry_run) as log:
        rows, stats = build(log)
        for c, s in stats.items():
            log.info(f"{c}: {s}")
        ok = (
            stats["eo"]["string_coverage"] == 1.0
            and stats["pk"]["string_coverage"] == 1.0
            and stats["lin"]["string_coverage"] == 1.0
            and stats["ofc2026"]["row_coverage_incl_empty"] >= 0.90
        )
        log.info(f"P0 acceptance (all EO/PK/LIN orgs map, OFC rows >= 90%): {'PASS' if ok else 'FAIL'}")
        log.event("acceptance", "ok" if ok else "failed")
        if not args.dry_run:
            path = CROSSWALK / "org_crosswalk.csv"
            write_csv(path, columns("org_crosswalk"), sorted(rows, key=lambda r: (str(r["corpus"]), str(r["printed"]))))
            log.info(f"wrote {path.relative_to(ROOT)} ({len(rows)} rows)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
