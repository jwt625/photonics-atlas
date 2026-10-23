"""Build the generated views the app reads (app/static/data/*.json). CSVs stay authoritative.

- registry.json: organizations (aliases, parent / units, printed names, sibling-atlas links, events, per-lens counts),
  org events with participants, the publications the events cite, org types, and the atlas overview of the home page.
- components.json: components with their values, the parameter / class registry, layout templates, showcase rows.
- supply.json: category tree, usage, processes, standards, reliability tests, products, specs.
- people.json: public persons and public observations only (DevLog-004; DevLog-010 D192); data/_local/ is never read.

Viewer-facing rules (DevLog-010 D199g-D199z): every cited source is served as a publication record (title, venue,
year, publication type in plain words, link); no corpus / access / licence / redistribution fields, no pipeline or
curation fields, no decision ids or corpus-prefixed ids in served free text. Source ids and observation ids stay only as
join keys (`source_id`, `obs_id`, the keys of a `sources` map, event `sources`, `lin_sources`, `datasheet_source_id`);
the app never renders them.

Usage: uv run python scripts/build_views.py [--dry-run]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import quote

from photonics_atlas.csvio import read_csv, split_list
from photonics_atlas.paths import ROOT
from photonics_atlas.runlog import RunLog

STATIC = ROOT / "app" / "static" / "data"
OUT = STATIC / "registry.json"
OUT_COMPONENTS = STATIC / "components.json"
OUT_SUPPLY = STATIC / "supply.json"
OUT_PEOPLE = STATIC / "people.json"

PUBLIC = "public"
EO_SITE = "https://outside5sigma.com/eo-modulator-atlas"
PK_SITE = "https://outside5sigma.com/advanced-packaging-atlas"

# Publication type in plain words per registry source_type (D199h). Unknown or new source types fall back to the
# source_type with spaces, so a new type shows up in the app without a code change.
PUB_TYPE = {
    "journal": "Journal article",
    "review": "Journal article",
    "paper": "Journal article",
    "conference": "Conference paper",
    "arxiv_preprint": "Preprint",
    "thesis": "Thesis",
    "patent": "Patent",
    "datasheet": "Datasheet",
    "standard": "Standard",
    "standards_body": "Standard",
    "slides": "Slides",
    "official_press_release": "Press release",
    "promotional_pr": "Press release",
    "regulatory_filing": "Regulatory filing",
    "acquisition_filing": "Regulatory filing",
    "official_company_page": "Company web page",
    "official_company_bio": "Company web page",
    "company_directory": "Company web page",
    "university_bio": "Profile page",
    "conference_bio": "Profile page",
    "cv": "Profile page",
    "professional_society": "Profile page",
    "linkedin": "Profile page",
    "reputable_technical_media": "News article",
    "news_media": "News article",
    "authoritative_interview": "News article",
    "repost": "News article",
    "crunchbase": "Company database",
    "startup_database": "Company database",
    "archived_webpage": "Web page",
    "other": "Web page",
}

# Keys whose values are join ids (may carry a corpus prefix; never rendered by the app).
JOIN_KEYS = frozenset({"source_id", "obs_id", "sources", "lin_sources", "datasheet_source_id"})
CORPUS_ID = re.compile(r"\b(?:eo|pk|ofc2026|lit|lin|blog|web|ds):[A-Za-z0-9][A-Za-z0-9_.\-/#]*")
_DREF = r"D\d{2,3}[a-z]?(?:\([a-z]\))?"
DREF_PAREN = re.compile(rf"\s*\((?:\s*(?:see\s+|per\s+)?{_DREF}\s*(?:[/,;]|and)?\s*)+\)")
DREF_TAIL = re.compile(rf"\s*[;,]\s*(?:see\s+|per\s+)?{_DREF}(?:\s*(?:[/,]|and)\s*{_DREF})*(?=\s*\))")
DREF_LEAD = re.compile(rf"(?<=\()\s*(?:see\s+|per\s+)?{_DREF}(?:\s*(?:[/,]|and)\s*{_DREF})*\s*[;:,]\s*")
DREF_LABEL = re.compile(rf"\b{_DREF}:\s*")
DREF_ANY = re.compile(rf"\s*\b(?:see\s+|per\s+|under\s+|by\s+)?{_DREF}\b")
BATCH_PAREN = re.compile(r"\s*\([^()]*\bbatch_\d+[^()]*\)")
ATLAS_ANCHOR = re.compile(r"^(eo|pk)-atlas:\S+$")


def _nonempty(r: dict[str, str], drop: tuple[str, ...] = ()) -> dict[str, str]:
    return {k: v for k, v in r.items() if v != "" and k not in drop}


class Pubs:
    """Publication records of the registry sources (D199g, D199h)."""

    def __init__(self, root: Path = ROOT) -> None:
        self.src = {s["source_id"]: s for s in read_csv(root / "data" / "registry" / "sources.csv")}

    def type_of(self, sid: str) -> str:
        st = self.src.get(sid, {}).get("source_type", "")
        return PUB_TYPE.get(st, st.replace("_", " ").capitalize() or "Other")

    def meta(self, sid: str) -> dict[str, Any]:
        s = self.src.get(sid)
        if not s:
            return {}
        link = s["url"] or (f"https://doi.org/{s['doi']}" if s["doi"] else "")
        link = link or (f"https://arxiv.org/abs/{s['arxiv_id']}" if s["arxiv_id"] else "")
        m: dict[str, Any] = _nonempty(
            {"title": s["title"], "venue": s["venue"], "year": s["year"], "type": self.type_of(sid), "url": link}
        )
        if s["doi"]:
            m["doi"] = s["doi"]
        if s["arxiv_id"]:
            m["arxiv"] = s["arxiv_id"]
        if s["corpus"] == "eo":
            m["atlas"] = ["EO modulator atlas", f"{EO_SITE}/table#q={quote(s['native_id'], safe='')}"]
        elif s["corpus"] == "pk":
            m["atlas"] = ["Advanced packaging atlas", f"{PK_SITE}/table#q={quote(s['native_id'], safe='')}"]
        return m

    def records(self, ids: set[str]) -> dict[str, dict[str, Any]]:
        return {i: self.meta(i) for i in sorted(ids) if i in self.src}

    def scrub(self, s: str) -> str:
        """Served free text without decision ids and with corpus-prefixed source ids replaced by the publication title
        (curator notes, parameter definitions, showcase rationale; D199i)."""
        if "D" in s:
            s = DREF_PAREN.sub("", s)
            s = DREF_TAIL.sub("", s)
            s = DREF_LEAD.sub("", s)
            s = DREF_LABEL.sub("", s)
            s = DREF_ANY.sub("", s)
        if "batch_" in s:
            s = BATCH_PAREN.sub("", s)
        if ":" in s:
            s = CORPUS_ID.sub(lambda m: self._title_ref(m.group(0)), s)
        return re.sub(r"\(\s*\)", "", s).replace("  ", " ").strip()

    def _title_ref(self, ref: str) -> str:
        sid = ref.split("#", 1)[0].rstrip(".,;)")
        t = self.src.get(sid, {}).get("title", "")
        return f'"{t}"' if t else "the cited source"

    def scrub_tree(self, x: Any, key: str = "") -> Any:
        if key in JOIN_KEYS:
            return x
        if isinstance(x, str):
            return self.scrub(x)
        if isinstance(x, list):
            return [self.scrub_tree(v, key) for v in x]
        if isinstance(x, dict):
            return {k: self.scrub_tree(v, k) for k, v in x.items()}
        return x


def plain_locator(loc: str) -> str:
    """Atlas anchors (paper-level record of a sibling atlas) and program-metadata locators in plain words (D199j)."""
    m = ATLAS_ANCHOR.match(loc)
    if m:
        return "paper record (EO modulator atlas)" if m.group(1) == "eo" else "paper record (advanced packaging atlas)"
    if loc.startswith("program metadata"):
        return "conference program listing"
    return loc


# ---------- supply ----------


def build_supply(root: Path = ROOT, pubs: Pubs | None = None) -> dict[str, Any]:
    """Supply tables (DevLog-003), non-empty viewer fields only, ordered by id, the category tree and the publication
    records of the cited sources. Pipeline / curation fields (extraction, verified_on, notes, atlas_ref, tv_ref,
    access) are not served (D199j)."""
    from photonics_atlas.rules_supply import load_categories

    pubs = pubs or Pubs(root)
    d = root / "data" / "supply"
    cats = load_categories(root / "data" / "schema" / "supply_categories.yaml")

    def table(name: str, key: str, drop: tuple[str, ...]) -> list[dict[str, str]]:
        rows = (_nonempty(r, drop) for r in read_csv(d / f"{name}.csv"))
        out = []
        for r in rows:
            if "locator" in r:
                r["locator"] = plain_locator(r["locator"])
            out.append(r)
        return sorted(out, key=lambda r: r[key])

    usage = table("product_usage", "usage_id", ("extraction", "verified_on", "notes"))
    procs = table("foundry_processes", "process_id", ("extraction", "verified_on", "notes"))
    stds = table("standards", "standard_id", ("access", "notes"))
    tests = table("reliability_tests", "test_id", ("atlas_ref", "tv_ref", "notes"))
    products = [
        {k: v for k, v in r.items() if not (k == "status" and v == "unknown")}
        for r in table("products", "product_id", ("verified_on", "notes"))
    ]
    specs = table("product_specs", "spec_id", ("verified_on", "notes"))
    cited = {r["source_id"] for t in (usage, procs, tests, specs) for r in t if r.get("source_id")}
    cited |= {r["datasheet_source_id"] for r in products if r.get("datasheet_source_id")}
    out = {
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
        "sources": pubs.records(cited),
    }
    scrubbed: dict[str, Any] = pubs.scrub_tree(out)
    return scrubbed


# ---------- people ----------

# lin_grade / lin_sources: the person's lineage record, so a person public through it alone (DevLog-004 D94) shows its
# evidence (D199d); empty for persons without one. The app shows it in plain words, never the grade code.
PERSON_FIELDS = ["id", "name", "orcid", "disambiguator", "lin_grade", "lin_sources"]
# grade: A = affiliation printed in the publication, B = conference program listing (shown in plain words, D199k).
OBS_FIELDS = [
    "obs_id",
    "p",
    "printed_name",
    "org_id",
    "printed_org",
    "unit",
    "country",
    "aff_role",
    "active_on",
    "source_id",
    "locator",
    "grade",
]


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


def build_people_view(root: Path = ROOT, pubs: Pubs | None = None) -> dict[str, Any]:
    """people.json: public persons (whitelisted fields) and their public observations as column arrays (`p` = index into
    persons), publication records of the cited sources, and aggregate totals (all vs public) per publication type. No
    review rows, no aliases, no xref rows, nothing derived from data/_local/ (D192)."""
    pubs = pubs or Pubs(root)
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
        totals[pubs.type_of(o["source_id"])]["all"] += 1
    for o in obs:
        totals[pubs.type_of(o["source_id"])]["public"] += 1
    return {
        "generated_on": dt.date.today().isoformat(),
        "counts": {
            "persons_all": len(all_people),
            "persons_public": len(persons),
            "obs_all": len(all_obs),
            "obs_public": len(obs),
        },
        "totals_by_type": {k: totals[k] for k in sorted(totals)},
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
                o["aff_role"],
                o["active_on"],
                o["source_id"],
                plain_locator(o["locator"]),
                o["evidence_grade"],
            ]
            for o in obs
        ],
        "sources": pubs.records({o["source_id"] for o in obs} | {sid for _, ss in lin.values() for sid in ss}),
    }


# ---------- per-org lens counts and overview ----------


def lens_counts(root: Path = ROOT) -> dict[str, dict[str, int]]:
    """Per-org counts across the lenses: components fabricated (cmp_fab) / made in the org as facility (cmp_fac), supply
    usage rows (sup), foundry process observations incl. as broker (proc), standards as body (std), public persons
    (ppl), public observations (obs), and distinct publications (pub, D199t): every registry source linked to the org
    through any lens (components fab / facility, supply usage, processes as foundry or broker, reliability tests citing
    a standard the org issued, public affiliations, org events it takes part in). The app's hub Publications panel uses
    the same definition (app/src/lib/views.ts orgPublications; vitest checks equality for every org). Non-zero keys
    only."""
    out: dict[str, Counter[str]] = defaultdict(Counter)
    pubs: dict[str, set[str]] = defaultdict(set)
    for c in read_csv(root / "data" / "components" / "components.csv"):
        for o in split_list(c["fab_org_ids"]):
            out[o]["cmp_fab"] += 1
            pubs[o].add(c["source_id"])
        for o in split_list(c["facility_org_ids"]):
            out[o]["cmp_fac"] += 1
            pubs[o].add(c["source_id"])
    sd = root / "data" / "supply"
    for u in read_csv(sd / "product_usage.csv"):
        out[u["org_id"]]["sup"] += 1
        pubs[u["org_id"]].add(u["source_id"])
    for p in read_csv(sd / "foundry_processes.csv"):
        for o in {p["org_id"], p["broker_org_id"]} - {""}:
            out[o]["proc"] += 1
            pubs[o].add(p["source_id"])
    body: dict[str, str] = {}
    for s in read_csv(sd / "standards.csv"):
        if s["body_org_id"]:
            out[s["body_org_id"]]["std"] += 1
            body[s["standard_id"]] = s["body_org_id"]
    for t in read_csv(sd / "reliability_tests.csv"):
        for sid in split_list(t["standard_ids"]):
            if sid in body:
                pubs[body[sid]].add(t["source_id"])
    reg = root / "data" / "registry"
    if (reg / "org_events.csv").exists() and (reg / "org_event_participants.csv").exists():
        ev_src = {e["event_id"]: split_list(e["source_ids"]) for e in read_csv(reg / "org_events.csv")}
        for p in read_csv(reg / "org_event_participants.csv"):
            pubs[p["org_id"]].update(ev_src.get(p["event_id"], []))
    _, obs = public_people(root)
    ppl: dict[str, set[str]] = defaultdict(set)
    for ob in obs:
        if ob["org_id"]:
            out[ob["org_id"]]["obs"] += 1
            ppl[ob["org_id"]].add(ob["person_id"])
            pubs[ob["org_id"]].add(ob["source_id"])
    for k, v in ppl.items():
        out[k]["ppl"] = len(v)
    known = {s["source_id"] for s in read_csv(reg / "sources.csv")}
    for k, ps in pubs.items():
        if ps & known:
            out[k]["pub"] = len(ps & known)
    return {k: dict(sorted(v.items())) for k, v in out.items() if v}


def build_overview(root: Path = ROOT, pubs: Pubs | None = None, top: int = 12) -> dict[str, Any]:
    """Home-page overview (D199l), all computed from the tables: components (count, classes, platforms, publications,
    year span), values (all / measured), organizations by type, public people, supply (usage rows, vendors, products,
    standards, tests), top fabricating orgs by components, top vendors by usage rows (shared-cleanroom use excluded),
    publications per year by publication type over every source the atlases cite (components, supply, public people)."""
    pubs = pubs or Pubs(root)
    comps = read_csv(root / "data" / "components" / "components.csv")
    mets = read_csv(root / "data" / "components" / "component_metrics.csv")
    orgs = read_csv(root / "data" / "registry" / "organizations.csv")
    sd = root / "data" / "supply"
    usage = read_csv(sd / "product_usage.csv")
    procs = read_csv(sd / "foundry_processes.csv")
    tests = read_csv(sd / "reliability_tests.csv")
    products = read_csv(sd / "products.csv")
    persons, obs = public_people(root)
    years = [int(y) for c in comps if (y := pubs.src.get(c["source_id"], {}).get("year", "")).isdigit()]
    fab: Counter[str] = Counter(o for c in comps for o in split_list(c["fab_org_ids"]))
    vend: Counter[str] = Counter(u["org_id"] for u in usage if u["role"] != "facility_use")
    cited = (
        {c["source_id"] for c in comps}
        | {u["source_id"] for u in usage}
        | {p["source_id"] for p in procs}
        | {t["source_id"] for t in tests}
        | {o["source_id"] for o in obs}
    )
    per: dict[str, Counter[int]] = defaultdict(Counter)
    no_year = 0
    for sid in cited:
        y = pubs.src.get(sid, {}).get("year", "")
        if y.isdigit():
            per[pubs.type_of(sid)][int(y)] += 1
        elif sid in pubs.src:
            no_year += 1
    all_years = sorted({y for c in per.values() for y in c})
    span = list(range(all_years[0], all_years[-1] + 1)) if all_years else []

    def top_rank(c: Counter[str]) -> list[list[Any]]:
        return [[k, n] for k, n in sorted(c.items(), key=lambda x: (-x[1], x[0]))[:top]]

    return {
        "components": {
            "n": len(comps),
            "classes": len({c["class"] for c in comps}),
            "class_families": len({c["class"].split(".")[0] for c in comps}),
            "platforms": len({c["platform"] for c in comps if c["platform"]}),
            "publications": len({c["source_id"] for c in comps}),
            "years": [min(years), max(years)] if years else [],
        },
        "values": {"n": len(mets), "measured": sum(1 for m in mets if m["basis"] == "measured")},
        "orgs": {"n": len(orgs), "by_type": dict(sorted(Counter(o["org_type"] for o in orgs).items()))},
        "people": {
            "persons": len(persons),
            "affiliations": len(obs),
            "publications": len({o["source_id"] for o in obs}),
        },
        "supply": {
            "usage": len(usage),
            "vendors": len(vend),
            "products": len(products),
            "processes": len(procs),
            "tests": len(tests),
            "standards": len(read_csv(sd / "standards.csv")),
        },
        "top_fabs": top_rank(fab),
        "top_vendors": top_rank(vend),
        "publications": {
            "n": len([s for s in cited if s in pubs.src]),
            "years": span,
            "by_type": {t: [per[t][y] for y in span] for t in sorted(per)},
            "no_year": no_year,
        },
    }


# ---------- components ----------


def build_components(root: Path = ROOT, pubs: Pubs | None = None) -> dict[str, Any]:
    """Component rows with their metric rows, publication record and org names, the class / parameter registry, the
    layout templates (component_layouts.yaml) and the showcase rows (component_showcase.csv) the layout viewer reads
    (DevLog-005). Not served: verified_on, host_device_ids (EO atlas device ids), showcase selected_on (D199j)."""
    from photonics_atlas.schema import load_layouts, load_parameters

    pubs = pubs or Pubs(root)
    comp_dir = root / "data" / "components"
    comps = read_csv(comp_dir / "components.csv")
    mets = read_csv(comp_dir / "component_metrics.csv")
    orgs = {o["org_id"]: o["name"] for o in read_csv(root / "data" / "registry" / "organizations.csv")}
    reg = load_parameters()
    layouts = (load_layouts() or {}).get("templates", {})
    show_path = comp_dir / "component_showcase.csv"
    showcase = [_nonempty(r, ("selected_on",)) for r in read_csv(show_path)] if show_path.exists() else []
    by_comp: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for m in mets:
        by_comp[m["component_id"]].append(_nonempty(m, ("component_id",)))
    out: list[dict[str, Any]] = []
    for c in comps:
        out.append(
            {
                **_nonempty(c, ("verified_on", "host_device_ids")),
                "fab_orgs": [orgs.get(o, o) for o in split_list(c["fab_org_ids"])],
                "source": pubs.meta(c["source_id"]),
                "metrics": by_comp.get(c["component_id"], []),
            }
        )
    view: dict[str, Any] = {
        "generated_on": dt.date.today().isoformat(),
        "classes": {k: {"label": v["label"], "subtypes": v["subtypes"]} for k, v in reg["classes"].items()},
        "parameters": {
            k: {"unit": v["unit"], "kind": v["kind"], "def": v["def"]} for k, v in reg["parameters"].items()
        },
        "layouts": layouts,
        "showcase": showcase,
        "components": out,
    }
    scrubbed: dict[str, Any] = pubs.scrub_tree(view)
    return scrubbed


# ---------- registry ----------

ALIAS_TYPE = {
    "short_name": "short name",
    "abbreviation": "abbreviation",
    "unit_printed": "printed unit name",
}


def build(root: Path = ROOT, pubs: Pubs | None = None) -> dict[str, Any]:
    """registry.json for the app: organizations, events, the publications events cite, org types, overview."""
    pubs = pubs or Pubs(root)
    reg = root / "data" / "registry"
    orgs = read_csv(reg / "organizations.csv")
    aliases = read_csv(reg / "org_aliases.csv")
    events = read_csv(reg / "org_events.csv") if (reg / "org_events.csv").exists() else []
    parts = read_csv(reg / "org_event_participants.csv") if (reg / "org_event_participants.csv").exists() else []
    xw = read_csv(root / "data" / "crosswalk" / "org_crosswalk.csv")

    al: dict[str, list[dict[str, str]]] = defaultdict(list)
    for a in aliases:
        al[a["org_id"]].append(
            {"alias": a["alias"], "type": ALIAS_TYPE.get(a["alias_type"], a["alias_type"].replace("_", " "))}
        )
    printed: dict[str, set[str]] = defaultdict(set)
    links: dict[str, list[list[str]]] = defaultdict(list)
    for r in sorted(xw, key=lambda r: (r["corpus"], -int(r["n_rows"]), r["printed"])):
        for oid in split_list(r["org_ids"]):
            if r["corpus"] != "lin":
                printed[oid].add(r["printed"])
            if int(r["n_rows"]) > 0 and r["corpus"] == "eo":
                links[oid].append(["EO modulator atlas", f"{EO_SITE}/table#q={quote(r['printed'], safe='')}"])
            elif int(r["n_rows"]) > 0 and r["corpus"] == "pk":
                links[oid].append(["Advanced packaging atlas", f"{PK_SITE}/table#o={quote(r['printed'], safe='')}"])
    ev_by_org: dict[str, list[str]] = defaultdict(list)
    pe: dict[str, list[dict[str, str]]] = defaultdict(list)
    for p in parts:
        ev_by_org[p["org_id"]].append(p["event_id"])
        pe[p["event_id"]].append({"org": p["org_id"], "role": p["role"]})
    lens = lens_counts(root)
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
                "aliases": al.get(oid, []),
                "printed": sorted(printed.get(oid, set()) - {o["name"]}),
                "links": links.get(oid, []),
                "events": ev_by_org.get(oid, []),
                "lens": lens.get(oid, {}),
            }
        )
    out_events: list[dict[str, Any]] = [
        {
            "id": e["event_id"],
            "type": e["event_type"],
            "name": e["name"],
            "announced": e["announced_on"],
            "effective": e["effective_on"],
            "sources": split_list(e["source_ids"]),
            "participants": pe.get(e["event_id"], []),
        }
        for e in events
    ]
    view: dict[str, Any] = {
        "generated_on": dt.date.today().isoformat(),
        "counts": {"organizations": len(orgs), "events": len(events)},
        "org_types": dict(Counter(o["org_type"] for o in orgs)),
        "overview": build_overview(root, pubs),
        "orgs": out_orgs,
        "events": out_events,
        "sources": pubs.records({s for e in out_events for s in e["sources"]}),
    }
    scrubbed: dict[str, Any] = pubs.scrub_tree(view)
    return scrubbed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    with RunLog("build_views", args.dry_run) as log:
        pubs = Pubs()
        views = {
            OUT: build(pubs=pubs),
            OUT_COMPONENTS: build_components(pubs=pubs),
            OUT_SUPPLY: build_supply(pubs=pubs),
            OUT_PEOPLE: build_people_view(pubs=pubs),
        }
        log.info(f"counts {views[OUT]['counts']}; overview {views[OUT]['overview']['components']}")
        if not args.dry_run:
            STATIC.mkdir(parents=True, exist_ok=True)
            for path, data in views.items():
                path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
                log.info(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
