"""Generated app views (scripts/build_views.py; DevLog-010 D190-D199). The privacy tests are binding (DevLog-004, D192):
no review-visibility person or observation id may appear anywhere in the emitted JSON, neither in a fresh in-memory build
nor in the committed files under app/static/data/."""

from __future__ import annotations

import ast
import importlib.util
import json
import re
import shutil
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from photonics_atlas.csvio import read_csv, write_csv
from photonics_atlas.paths import ROOT

PEOPLE = ROOT / "data" / "people"
STATIC = ROOT / "app" / "static" / "data"


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("build_views", ROOT / "scripts" / "build_views.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bv = _load()


def _strings(x: Any) -> set[str]:
    """Every string value and key in a JSON document."""
    out: set[str] = set()
    stack = [x]
    while stack:
        v = stack.pop()
        if isinstance(v, str):
            out.add(v)
        elif isinstance(v, dict):
            out.update(v.keys())
            stack.extend(v.values())
        elif isinstance(v, list):
            stack.extend(v)
    return out


def _review_ids(root: Path = ROOT) -> tuple[set[str], set[str]]:
    persons = read_csv(root / "data" / "people" / "people.csv")
    obs = read_csv(root / "data" / "people" / "affiliation_observations.csv")
    pub = {p["person_id"] for p in persons if p["visibility"] == "public"}
    review_p = {p["person_id"] for p in persons if p["visibility"] != "public"}
    # an observation is review when its own visibility is, or when its person is not public
    review_o = {o["obs_id"] for o in obs if o["visibility"] != "public" or o["person_id"] not in pub}
    return review_p, review_o


def _assert_no_review(docs: list[Any], root: Path = ROOT) -> None:
    review_p, review_o = _review_ids(root)
    assert review_p and review_o, "fixture: the people tables are expected to hold review rows"
    for doc in docs:
        s = _strings(doc)
        assert not (s & review_p), f"review person ids emitted: {sorted(s & review_p)[:5]}"
        assert not (s & review_o), f"review observation ids emitted: {sorted(s & review_o)[:5]}"


def test_no_review_ids_in_fresh_build() -> None:
    _assert_no_review([bv.build(), bv.build_components(), bv.build_supply(), bv.build_people_view()])


def test_no_review_ids_in_committed_views() -> None:
    """Committed views, plus the local build output when present (app/build is git-ignored but `vite preview` or a manual
    upload would serve it; DevLog-010 D199a)."""
    files = sorted(STATIC.glob("*.json")) + sorted((ROOT / "app" / "build" / "data").glob("*.json"))
    if not any(f.name == "people.json" for f in files):
        pytest.skip("people.json not built yet")
    _assert_no_review([json.loads(f.read_text(encoding="utf-8")) for f in files])


def test_people_view_public_only() -> None:
    v = bv.build_people_view()
    persons = {p["person_id"]: p for p in read_csv(PEOPLE / "people.csv")}
    obs = {o["obs_id"]: o for o in read_csv(PEOPLE / "affiliation_observations.csv")}
    assert v["person_fields"] == ["id", "name", "orcid", "disambiguator", "lin_grade", "lin_sources"]
    for row in v["persons"]:
        for sid in filter(None, row[5].split(";")):
            assert sid.startswith("lin:") and sid in v["sources"]
    for row in v["persons"]:
        assert persons[row[0]]["visibility"] == "public"
    pid = [r[0] for r in v["persons"]]
    for row in v["obs"]:
        o = obs[row[0]]
        assert o["visibility"] == "public" and pid[row[1]] == o["person_id"]
    n_pub = sum(
        1 for o in obs.values() if o["visibility"] == "public" and persons[o["person_id"]]["visibility"] == "public"
    )
    assert len(v["obs"]) == v["counts"]["obs_public"] == n_pub
    assert sum(t["public"] for t in v["totals_by_type"].values()) == n_pub
    assert sum(t["all"] for t in v["totals_by_type"].values()) == len(obs)


def test_person_flipped_to_review_disappears(tmp_path: Path) -> None:
    """Mutation: a public person turned review (and one public observation of another person turned review) must vanish
    from people.json and from the registry lens counts."""
    for d in ("data/people", "data/registry", "data/components", "data/supply", "data/schema"):
        shutil.copytree(ROOT / d, tmp_path / d)
    pp = tmp_path / "data" / "people" / "people.csv"
    op = tmp_path / "data" / "people" / "affiliation_observations.csv"
    persons, obs = read_csv(pp), read_csv(op)
    by_p: dict[str, int] = {}
    for o in obs:
        if o["visibility"] == "public":
            by_p[o["person_id"]] = by_p.get(o["person_id"], 0) + 1
    victim = max(sorted(by_p), key=lambda k: by_p[k])
    for p in persons:
        if p["person_id"] == victim:
            p["visibility"] = "review"
    other = next(o for o in obs if o["visibility"] == "public" and o["person_id"] != victim)
    other["visibility"] = "review"
    write_csv(pp, list(persons[0].keys()), persons)
    write_csv(op, list(obs[0].keys()), obs)
    v = bv.build_people_view(tmp_path)
    s = _strings(v)
    assert victim not in s and other["obs_id"] not in s
    assert v["counts"]["obs_public"] == bv.build_people_view()["counts"]["obs_public"] - by_p[victim] - 1
    _assert_no_review([v], tmp_path)


def test_build_never_reads_local() -> None:
    """No code string literal of build_views.py (docstrings excluded) names data/_local or its local-only files."""
    tree = ast.parse((ROOT / "scripts" / "build_views.py").read_text(encoding="utf-8"))
    docs = {
        id(n.body[0].value)
        for n in ast.walk(tree)
        if isinstance(n, ast.Module | ast.FunctionDef | ast.ClassDef)
        and n.body
        and isinstance(n.body[0], ast.Expr)
        and isinstance(n.body[0].value, ast.Constant)
    }
    lits = [
        n.value
        for n in ast.walk(tree)
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docs
    ]
    bad = ("_local", "transitions", "review_queue", "name_only", "funnel")
    assert not [s for s in lits for b in bad if b in s]


def test_views_deterministic() -> None:
    assert json.dumps(bv.build_supply()) == json.dumps(bv.build_supply())
    assert json.dumps(bv.build_people_view()) == json.dumps(bv.build_people_view())
    assert bv.lens_counts() == bv.lens_counts()


def test_supply_view_matches_tables() -> None:
    v = bv.build_supply()
    d = ROOT / "data" / "supply"
    for key, name in (
        ("usage", "product_usage"),
        ("processes", "foundry_processes"),
        ("standards", "standards"),
        ("tests", "reliability_tests"),
        ("products", "products"),
        ("specs", "product_specs"),
    ):
        assert len(v[key]) == len(read_csv(d / f"{name}.csv")), key
    cats = {c["id"] for c in v["categories"]}
    assert {"A", "B7", "A2.1", "K"} <= cats
    assert all(u["category_id"] in cats for u in v["usage"])
    assert all(u["source_id"] in v["sources"] for u in v["usage"])
    assert all(c.get("parent", c["id"][:1]) in cats for c in v["categories"])


def test_lens_counts() -> None:
    lens = bv.lens_counts()
    comps = read_csv(ROOT / "data" / "components" / "components.csv")
    n_fab = sum(len([o for o in c["fab_org_ids"].split(";") if o.strip()]) for c in comps)
    assert sum(v.get("cmp_fab", 0) for v in lens.values()) == n_fab
    usage = read_csv(ROOT / "data" / "supply" / "product_usage.csv")
    assert sum(v.get("sup", 0) for v in lens.values()) == len(usage)
    assert sum(v.get("obs", 0) for v in lens.values()) <= bv.build_people_view()["counts"]["obs_public"]
    assert all(all(n > 0 for n in v.values()) for v in lens.values())


# ---------- viewer-facing served data (DevLog-010 D199g-D199z) ----------

FORBIDDEN_KEYS = {
    "access",
    "license",
    "redistribution",
    "corpus",
    "corpora",
    "sources_duplicate",
    "sources_by_corpus",
    "coverage",
    "text_cached",
    "same_as",
    "extraction",
    "verified_on",
    "atlas_ref",
    "tv_ref",
    "name_basis",
    "name_source",
    "origin",
    "evidence_grade",
    "selected_on",
    "host_device_ids",
    "totals_by_corpus",
}
PREFIXED = re.compile(r"\b(?:eo|pk|ofc2026|lit|lin|blog|web|ds):[A-Za-z0-9]")
INTERNAL = re.compile(r"\bD\d{2,3}[a-z]?\b|DevLog|eo-atlas:|pk-atlas:|authors_json|batch_\d|_staging|data/_local")


def _viewer_issues(doc: Any, path: str = "") -> list[str]:
    """Forbidden keys anywhere; corpus-prefixed ids only as values of join keys (bv.JOIN_KEYS) or as keys of a
    `sources` map; no decision ids, pipeline paths or atlas anchors in any served string."""
    out: list[str] = []
    stack: list[tuple[Any, str, str]] = [(doc, path, "")]
    while stack:
        v, p, key = stack.pop()
        if isinstance(v, dict):
            for k, x in v.items():
                if k in FORBIDDEN_KEYS:
                    out.append(f"{p}.{k}: forbidden key")
                if PREFIXED.search(k) and not p.endswith(".sources"):
                    out.append(f"{p}: prefixed key {k}")
                stack.append((x, f"{p}.{k}", k))
        elif isinstance(v, list):
            stack.extend((x, f"{p}[]", key) for x in v)
        elif isinstance(v, str):
            if INTERNAL.search(v):
                out.append(f"{p}: internal text {v[:80]!r}")
            if PREFIXED.search(v) and key not in bv.JOIN_KEYS and not _join_column(p):
                out.append(f"{p}: prefixed id {v[:80]!r}")
    return out


def _join_column(path: str) -> bool:
    """people.json column arrays: obs_id and source_id columns, lin_sources column (positional, no key)."""
    return path in (".obs[][]", ".persons[][]")


def test_served_views_viewer_facing_fresh() -> None:
    pubs = bv.Pubs()
    for name, doc in (
        ("registry", bv.build(pubs=pubs)),
        ("components", bv.build_components(pubs=pubs)),
        ("supply", bv.build_supply(pubs=pubs)),
        ("people", bv.build_people_view(pubs=pubs)),
    ):
        issues = _viewer_issues(doc)
        assert not issues, f"{name}: {issues[:5]}"


def test_people_columns_hold_prefixed_ids_only_in_join_columns() -> None:
    v = bv.build_people_view()
    join = {v["obs_fields"].index("obs_id"), v["obs_fields"].index("source_id")}
    for row in v["obs"]:
        for i, x in enumerate(row):
            if isinstance(x, str) and PREFIXED.search(x):
                assert i in join, (v["obs_fields"][i], x)
    lin = v["person_fields"].index("lin_sources")
    for row in v["persons"]:
        for i, x in enumerate(row):
            if isinstance(x, str) and PREFIXED.search(x):
                assert i == lin, (v["person_fields"][i], x)


def test_served_views_viewer_facing_committed() -> None:
    files = sorted(STATIC.glob("*.json"))
    docs = {f.name: json.loads(f.read_text(encoding="utf-8")) for f in files}
    if "registry.json" not in docs or "overview" not in docs["registry.json"]:
        pytest.skip("views not rebuilt with the viewer-facing build yet")
    for name, doc in docs.items():
        issues = _viewer_issues(doc)
        assert not issues, f"{name}: {issues[:5]}"


def test_publication_records() -> None:
    v = bv.build_supply()
    for sid, m in v["sources"].items():
        assert m.get("title") and m.get("type"), sid
        assert set(m) <= {"title", "venue", "year", "type", "url", "doi", "arxiv", "atlas"}, sid
    ov = bv.build()["overview"]
    comps = read_csv(ROOT / "data" / "components" / "components.csv")
    assert ov["components"]["n"] == len(comps)
    assert ov["components"]["publications"] == len({c["source_id"] for c in comps})
    pubs = ov["publications"]
    assert sum(sum(c) for c in pubs["by_type"].values()) + pubs["no_year"] == pubs["n"]
