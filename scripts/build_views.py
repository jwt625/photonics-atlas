"""Build app/static/data/registry.json and components.json, the generated views the app reads. CSVs stay authoritative.

Contents: counts, crosswalk coverage per corpus, organizations (with aliases, parent, children, per-corpus row counts
from the crosswalk, events), org events with participants, and source counts by corpus x access.
No people data in P0.

Usage: uv run python scripts/build_views.py [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from collections import Counter, defaultdict
from typing import Any

from photonics_atlas.csvio import read_csv, split_list
from photonics_atlas.paths import CROSSWALK, REGISTRY, ROOT
from photonics_atlas.runlog import RunLog

OUT = ROOT / "app" / "static" / "data" / "registry.json"
OUT_COMPONENTS = ROOT / "app" / "static" / "data" / "components.json"


def build_components() -> dict[str, Any]:
    """Component rows with their metric rows, source labels and org names (no source text)."""
    from photonics_atlas.schema import load_parameters

    comp_dir = ROOT / "data" / "components"
    comps = read_csv(comp_dir / "components.csv")
    mets = read_csv(comp_dir / "component_metrics.csv")
    src = {s["source_id"]: s for s in read_csv(REGISTRY / "sources.csv")}
    orgs = {o["org_id"]: o["name"] for o in read_csv(REGISTRY / "organizations.csv")}
    reg = load_parameters()
    by_comp: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for m in mets:
        by_comp[m["component_id"]].append({k: v for k, v in m.items() if v != "" and k not in ("component_id",)})
    out = []
    for c in comps:
        s = src.get(c["source_id"], {})
        out.append(
            {
                **{k: v for k, v in c.items() if v != ""},
                "fab_orgs": [orgs.get(o, o) for o in split_list(c["fab_org_ids"])],
                "source": {
                    "id": c["source_id"],
                    "title": s.get("title", ""),
                    "year": s.get("year", ""),
                    "venue": s.get("venue", ""),
                    "url": s.get("url", ""),
                    "access": s.get("access", ""),
                },
                "metrics": by_comp.get(c["component_id"], []),
            }
        )
    return {
        "generated_on": dt.date.today().isoformat(),
        "classes": {k: {"label": v["label"], "subtypes": v["subtypes"]} for k, v in reg["classes"].items()},
        "parameters": {
            k: {"unit": v["unit"], "kind": v["kind"], "def": v["def"]} for k, v in reg["parameters"].items()
        },
        "components": out,
    }


def build() -> dict[str, Any]:
    orgs = read_csv(REGISTRY / "organizations.csv")
    aliases = read_csv(REGISTRY / "org_aliases.csv")
    events = read_csv(REGISTRY / "org_events.csv") if (REGISTRY / "org_events.csv").exists() else []
    parts = (
        read_csv(REGISTRY / "org_event_participants.csv") if (REGISTRY / "org_event_participants.csv").exists() else []
    )
    sources = read_csv(REGISTRY / "sources.csv")
    xw = read_csv(CROSSWALK / "org_crosswalk.csv")

    al: dict[str, list[dict[str, str]]] = defaultdict(list)
    for a in aliases:
        al[a["org_id"]].append({"alias": a["alias"], "type": a["alias_type"], "scope": a["scope"]})
    rows_by_org: dict[str, Counter[str]] = defaultdict(Counter)
    printed_by_org: dict[str, list[dict[str, Any]]] = defaultdict(list)
    cov: dict[str, dict[str, int]] = defaultdict(
        lambda: {"strings": 0, "strings_mapped": 0, "rows": 0, "rows_mapped": 0}
    )
    basis: dict[str, Counter[str]] = defaultdict(Counter)
    for r in xw:
        n = int(r["n_rows"])
        c = cov[r["corpus"]]
        c["strings"] += 1
        c["rows"] += n
        basis[r["corpus"]][r["match_basis"]] += n
        ids = split_list(r["org_ids"])
        if ids:
            c["strings_mapped"] += 1
            c["rows_mapped"] += n
        for oid in ids:
            rows_by_org[oid][r["corpus"]] += n
            if r["corpus"] != "lin":
                printed_by_org[oid].append(
                    {"corpus": r["corpus"], "printed": r["printed"], "n": n, "basis": r["match_basis"]}
                )
    ev_by_org: dict[str, list[str]] = defaultdict(list)
    pe: dict[str, list[dict[str, str]]] = defaultdict(list)
    for p in parts:
        ev_by_org[p["org_id"]].append(p["event_id"])
        pe[p["event_id"]].append({"org": p["org_id"], "role": p["role"], "printed": p["printed_name"]})
    children: dict[str, list[str]] = defaultdict(list)
    for o in orgs:
        if o["parent_org_id"]:
            children[o["parent_org_id"]].append(o["org_id"])

    out_orgs: list[dict[str, Any]] = []
    for o in orgs:
        oid = o["org_id"]
        out_orgs.append(
            {
                "id": oid,
                "name": o["name"],
                "type": o["org_type"],
                "country": o["country"],
                "parent": o["parent_org_id"],
                "children": sorted(children.get(oid, [])),
                "status": o["status"],
                "founded": o["founded_on"],
                "dissolved": o["dissolved_on"],
                "ror": o["ror_id"],
                "qid": o["wikidata_qid"],
                "website": o["website"],
                "name_basis": o["name_basis"],
                "name_source": o["name_source"],
                "origin": split_list(o["origin"]),
                "aliases": al.get(oid, []),
                "rows": dict(rows_by_org.get(oid, {})),
                "printed": sorted(printed_by_org.get(oid, []), key=lambda x: -int(x["n"])),
                "events": ev_by_org.get(oid, []),
                "notes": o["notes"],
            }
        )
    out_events = [
        {
            "id": e["event_id"],
            "type": e["event_type"],
            "name": e["name"],
            "announced": e["announced_on"],
            "effective": e["effective_on"],
            "grade": e["grade"],
            "status": e["status"],
            "basis": e["basis"],
            "sources": split_list(e["source_ids"]),
            "locator": e["locator"],
            "notes": e["notes"],
            "participants": pe.get(e["event_id"], []),
        }
        for e in events
    ]
    src_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for s in sources:
        src_counts[s["corpus"]][s["access"]] += 1
    return {
        "generated_on": dt.date.today().isoformat(),
        "counts": {
            "organizations": len(orgs),
            "aliases": len(aliases),
            "events": len(events),
            "sources": len(sources),
            "sources_duplicate": sum(1 for s in sources if s["same_as"]),
        },
        "coverage": {k: {**v, "by_basis": dict(basis[k])} for k, v in cov.items()},
        "org_types": dict(Counter(o["org_type"] for o in orgs)),
        "sources_by_corpus": {k: dict(v) for k, v in src_counts.items()},
        "orgs": out_orgs,
        "events": out_events,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    with RunLog("build_views", args.dry_run) as log:
        data = build()
        log.info(f"counts {data['counts']}")
        if not args.dry_run:
            OUT.parent.mkdir(parents=True, exist_ok=True)
            OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            log.info(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size} bytes)")
            comp = build_components()
            OUT_COMPONENTS.write_text(json.dumps(comp, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            log.info(f"wrote {OUT_COMPONENTS.relative_to(ROOT)} ({len(comp['components'])} components)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
