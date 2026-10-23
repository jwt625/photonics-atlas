"""Build app/static/data/registry.json and components.json, the generated views the app reads. CSVs stay authoritative.

Contents: counts, crosswalk coverage per corpus, organizations (with aliases, parent, children, per-corpus row counts
from the crosswalk, events, per-lens counts), org events with participants, and source counts by corpus x access.
Also supply.json (DevLog-010 D191) and people.json (public persons and observations only, D192; data/_local/ is never
read).

Usage: uv run python scripts/build_views.py [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from photonics_atlas.csvio import read_csv, split_list
from photonics_atlas.paths import CROSSWALK, REGISTRY, ROOT
from photonics_atlas.runlog import RunLog

OUT = ROOT / "app" / "static" / "data" / "registry.json"
OUT_COMPONENTS = ROOT / "app" / "static" / "data" / "components.json"
OUT_SUPPLY = ROOT / "app" / "static" / "data" / "supply.json"
OUT_PEOPLE = ROOT / "app" / "static" / "data" / "people.json"

PUBLIC = "public"
SOURCE_FIELDS = ("title", "year", "venue", "url", "access")


def _nonempty(r: dict[str, str], drop: tuple[str, ...] = ()) -> dict[str, str]:
    return {k: v for k, v in r.items() if v != "" and k not in drop}


def _sources(root: Path, ids: set[str]) -> dict[str, dict[str, str]]:
    """Metadata of the cited sources only (title, year, venue, url, access), keyed and ordered by source id."""
    src = {s["source_id"]: s for s in read_csv(root / "data" / "registry" / "sources.csv")}
    return {i: _nonempty({k: src[i][k] for k in SOURCE_FIELDS}) for i in sorted(ids) if i in src}


def build_supply(root: Path = ROOT) -> dict[str, Any]:
    """Supply tables (DevLog-003) as-is, non-empty fields only, ordered by id, plus the category tree and the metadata of
    the cited sources (DevLog-010 D191). products / product_specs are emitted as they are (empty on 2026-10-22, D195)."""
    from photonics_atlas.rules_supply import load_categories

    d = root / "data" / "supply"
    cats = load_categories(root / "data" / "schema" / "supply_categories.yaml")

    def table(name: str, key: str) -> list[dict[str, str]]:
        return sorted((_nonempty(r) for r in read_csv(d / f"{name}.csv")), key=lambda r: r[key])

    usage = table("product_usage", "usage_id")
    procs = table("foundry_processes", "process_id")
    stds = table("standards", "standard_id")
    tests = table("reliability_tests", "test_id")
    products = table("products", "product_id")
    specs = table("product_specs", "spec_id")
    cited = {r["source_id"] for t in (usage, procs, tests, specs) for r in t if r.get("source_id")}
    cited |= {r["datasheet_source_id"] for r in products if r.get("datasheet_source_id")}
    return {
        "generated_on": dt.date.today().isoformat(),
        "categories": [
            {"id": k, "label": str(v["label"]), **({"parent": str(v["parent"])} if v.get("parent") else {})}
            for k, v in cats.items()
        ],
        "usage": usage,
        "processes": procs,
        "standards": stds,
        "tests": tests,
        "products": products,
        "specs": specs,
        "sources": _sources(root, cited),
    }


# lin_grade / lin_sources: the person's lineage (LIN) record, so a person public through LIN alone (D94) shows its
# evidence (DevLog-010 D199d); empty for persons without a LIN record.
PERSON_FIELDS = ["id", "name", "orcid", "disambiguator", "lin_grade", "lin_sources"]
OBS_FIELDS = [
    "obs_id",
    "p",
    "printed_name",
    "org_id",
    "printed_org",
    "unit",
    "country",
    "kind",
    "aff_role",
    "active_on",
    "source_id",
    "locator",
    "grade",
]


def corpus_of(source_id: str) -> str:
    return source_id.split(":", 1)[0]


def public_people(root: Path = ROOT) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Public persons and the public observations of public persons (DevLog-004 D70, D94; DevLog-010 D192). Reads the
    committed tables in data/people/ only, never data/_local/."""
    d = root / "data" / "people"
    persons = [p for p in read_csv(d / "people.csv") if p["visibility"] == PUBLIC]
    ids = {p["person_id"] for p in persons}
    obs = [
        o for o in read_csv(d / "affiliation_observations.csv") if o["visibility"] == PUBLIC and o["person_id"] in ids
    ]
    return persons, obs


def build_people_view(root: Path = ROOT) -> dict[str, Any]:
    """people.json: public persons (whitelisted fields) and their public observations as column arrays (`p` = index into
    persons), cited-source metadata, and aggregate totals (all vs public) per corpus. No review rows, no aliases, no xref
    rows, nothing derived from data/_local/ (D192)."""
    persons, obs = public_people(root)
    persons.sort(key=lambda p: p["person_id"])
    pub = {p["person_id"] for p in persons}
    lin: dict[str, tuple[str, list[str]]] = {}
    for x in read_csv(root / "data" / "people" / "person_xref.csv"):
        if x["scheme"] == "lin_id" and x["person_id"] in pub:
            note = x["notes"]
            srcs = split_list(note.removeprefix("lin sources:")) if note.startswith("lin sources:") else []
            lin[x["person_id"]] = (x["grade"], sorted(srcs))
    idx = {p["person_id"]: i for i, p in enumerate(persons)}
    obs.sort(key=lambda o: (o["person_id"], o["active_on"], o["obs_id"]))
    all_people = read_csv(root / "data" / "people" / "people.csv")
    all_obs = read_csv(root / "data" / "people" / "affiliation_observations.csv")
    totals: dict[str, dict[str, int]] = defaultdict(lambda: {"all": 0, "public": 0})
    for o in all_obs:
        totals[corpus_of(o["source_id"])]["all"] += 1
    for o in obs:
        totals[corpus_of(o["source_id"])]["public"] += 1
    return {
        "generated_on": dt.date.today().isoformat(),
        "counts": {
            "persons_all": len(all_people),
            "persons_public": len(persons),
            "obs_all": len(all_obs),
            "obs_public": len(obs),
        },
        "totals_by_corpus": {k: totals[k] for k in sorted(totals)},
        "person_fields": PERSON_FIELDS,
        "persons": [
            [
                p["person_id"],
                p["display_name"],
                p["orcid"],
                p["disambiguator"],
                lin.get(p["person_id"], ("", []))[0],
                ";".join(lin.get(p["person_id"], ("", []))[1]),
            ]
            for p in persons
        ],
        "obs_fields": OBS_FIELDS,
        "obs": [
            [
                o["obs_id"],
                idx[o["person_id"]],
                o["printed_name"],
                o["org_id"],
                o["printed_org"],
                o["unit"],
                o["country"],
                o["kind"],
                o["aff_role"],
                o["active_on"],
                o["source_id"],
                o["locator"],
                o["evidence_grade"],
            ]
            for o in obs
        ],
        "sources": _sources(root, {o["source_id"] for o in obs} | {sid for _, ss in lin.values() for sid in ss}),
    }


def lens_counts(root: Path = ROOT) -> dict[str, dict[str, int]]:
    """Per-org counts across the lenses (DevLog-010 D191): components fabricated (cmp_fab) / facility (cmp_fac), supply
    usage rows (sup), foundry process observations incl. as broker (proc), standards as body (std), public persons (ppl)
    and public observations (obs). Non-zero keys only."""
    out: dict[str, Counter[str]] = defaultdict(Counter)
    for c in read_csv(root / "data" / "components" / "components.csv"):
        for o in split_list(c["fab_org_ids"]):
            out[o]["cmp_fab"] += 1
        for o in split_list(c["facility_org_ids"]):
            out[o]["cmp_fac"] += 1
    sd = root / "data" / "supply"
    for u in read_csv(sd / "product_usage.csv"):
        out[u["org_id"]]["sup"] += 1
    for p in read_csv(sd / "foundry_processes.csv"):
        for o in {p["org_id"], p["broker_org_id"]} - {""}:
            out[o]["proc"] += 1
    for s in read_csv(sd / "standards.csv"):
        if s["body_org_id"]:
            out[s["body_org_id"]]["std"] += 1
    _, obs = public_people(root)
    ppl: dict[str, set[str]] = defaultdict(set)
    for ob in obs:
        if ob["org_id"]:
            out[ob["org_id"]]["obs"] += 1
            ppl[ob["org_id"]].add(ob["person_id"])
    for k, v in ppl.items():
        out[k]["ppl"] = len(v)
    return {k: dict(sorted(v.items())) for k, v in out.items() if v}


def build_components() -> dict[str, Any]:
    """Component rows with their metric rows, source labels and org names (no source text), plus the layout templates
    (component_layouts.yaml) and the showcase rows (component_showcase.csv) the layout viewer reads (DevLog-005)."""
    from photonics_atlas.schema import load_layouts, load_parameters

    comp_dir = ROOT / "data" / "components"
    comps = read_csv(comp_dir / "components.csv")
    mets = read_csv(comp_dir / "component_metrics.csv")
    src = {s["source_id"]: s for s in read_csv(REGISTRY / "sources.csv")}
    orgs = {o["org_id"]: o["name"] for o in read_csv(REGISTRY / "organizations.csv")}
    reg = load_parameters()
    layouts = (load_layouts() or {}).get("templates", {})
    show_path = comp_dir / "component_showcase.csv"
    showcase = [{k: v for k, v in r.items() if v != ""} for r in read_csv(show_path)] if show_path.exists() else []
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
        "layouts": layouts,
        "showcase": showcase,
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
    lens = lens_counts()
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
                "lens": lens.get(oid, {}),
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
            log.info(
                f"wrote {OUT_COMPONENTS.relative_to(ROOT)} ({len(comp['components'])} components, "
                f"{len(comp['layouts'])} layout templates, {len(comp['showcase'])} showcase rows)"
            )
            sup = build_supply()
            OUT_SUPPLY.write_text(json.dumps(sup, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            log.info(
                f"wrote {OUT_SUPPLY.relative_to(ROOT)} ({OUT_SUPPLY.stat().st_size} bytes; {len(sup['usage'])} usage, "
                f"{len(sup['processes'])} processes, {len(sup['standards'])} standards, {len(sup['tests'])} tests, "
                f"{len(sup['products'])} products)"
            )
            ppl = build_people_view()
            OUT_PEOPLE.write_text(json.dumps(ppl, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            log.info(
                f"wrote {OUT_PEOPLE.relative_to(ROOT)} ({OUT_PEOPLE.stat().st_size} bytes; counts {ppl['counts']})"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
