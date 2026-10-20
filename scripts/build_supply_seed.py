"""Build the P2 supply-chain seed tables from local structured inputs (DevLog-003 D53-D60). No network.

Steps:
  eo  EO papers.csv foundry_or_fab / wafer_supplier -> data/supply/product_usage.csv;
      curated process observations (data/supply/curation.yaml) -> data/supply/foundry_processes.csv
  pk  PK metrics.csv rows with a test_standard -> data/supply/standards.csv + data/supply/reliability_tests.csv
Unmapped org names (suppliers, brokers, standards bodies) are merged into data/_staging/supply/org_requests.csv; the
registry is never touched. Tables are append-only: rows whose id exists are kept as they are (a differing rebuilt row
is logged as `differs`, not written; an id on disk that the rebuild no longer produces is logged as `stale`). Explicit
corrections go through --replace-ids: each listed id that exists is replaced by its rebuilt row, or removed when the
rebuild no longer produces it (logged as `replaced` / `removed`). Zip-backup data/supply/ before a replace run.
Pilot with --only / --limit, inspect, then run without them.

Usage:
  uv run python scripts/build_supply_seed.py --dry-run
  uv run python scripts/build_supply_seed.py --only johnson2025,ectc51906.2022.00072
  uv run python scripts/build_supply_seed.py --limit 5 --steps pk
  uv run python scripts/build_supply_seed.py --replace-ids @ids.txt   (one id per line, or a comma-separated list)
  uv run python scripts/build_supply_seed.py
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from collections.abc import Callable
from typing import Any

import yaml

from photonics_atlas.adapters import eo, pk_metrics
from photonics_atlas.csvio import read_csv, read_header, split_list, write_csv
from photonics_atlas.orgmatch import Matcher, load_matcher
from photonics_atlas.paths import REGISTRY, ROOT, STAGING, input_path
from photonics_atlas.rules_supply import (
    HUMID_TYPES,
    RANGE_T_TYPES,
    SINGLE_T_TYPES,
    atlas_anchor,
    process_id,
    standard_id,
    test_id,
    usage_id,
)
from photonics_atlas.runlog import RunLog
from photonics_atlas.schema import columns

SUPPLY = ROOT / "data" / "supply"
CURATION = SUPPLY / "curation.yaml"
REQUESTS = STAGING / "supply" / "org_requests.csv"
REQUEST_COLUMNS = [
    "corpus",
    "kind",
    "printed",
    "column",
    "alias_of_org_id",
    "status",
    "resolved_org_id",
    "source_ids",
    "notes",
]
Row = dict[str, str]
Requests = dict[tuple[str, str, str, str], set[str]]

# D57: wafer_supplier parts that name no supplier.
NO_SUPPLIER = re.compile(r"not named|not stated|fabricated by the authors", re.I)
# D57: qualifier / name keywords -> category (first match wins).
WAFER_KEYWORDS: list[tuple[str, str]] = [
    (r"\bsoi (substrate|wafer)s?\b", "A1"),
    # growth / integration / deposition on someone else's wafer is a post-processing service (D54, D57 amended)
    (r"\bgrowth\b|\bintegration\b|\bdeposition\b", "B5"),
    (r"ln-on-sapphire", "A2.3"),
    (r"\bltoi\b|\btflt\b|lithium tantalate|litao3", "A2.2"),
    (r"\blnoi\b|\btfln\b|ln-on-insulator|lithium niobate", "A2.1"),
    (r"\bbto\b|batio3", "A2.4"),
    (r"\bgaas\b|\binp\b", "A3"),
    (r"chromophore|eo material|\boeo\b|fn-lc|polymer", "A4"),
    (r"graphene|\bhbn\b", "A5"),
    (r"gdsco3|\blsat\b|srtio3", "A6"),
    (r"\bsin wafers?\b|si3n4 wafers?", "B2"),
    (r"\bsoi\b", "A1"),
]
# D57: EO device waveguide_platform prefix -> category (fallback).
PLATFORM_CATEGORY: list[tuple[str, str]] = [
    ("lnoi_", "A2.1"),
    ("suspended_lnoi", "A2.1"),
    ("ltoi_", "A2.2"),
    ("lnos_", "A2.3"),
    ("bto_", "A2.4"),
    ("algaas", "A3"),
    ("gaas", "A3"),
    ("suspended_gaas", "A3"),
]
# D60 (amended 2026-10-20): test_type is the stress; the measurand is a separate column. Stress keywords are searched
# in the PK parameter, then the condition, then the printed standard string; in each text the preconditioning clauses
# (from an MSL / precon keyword to the end of its ';' segment, incl. their bake, soak and reflow steps) are split off
# first. The first text with a stress outside those clauses decides (uhast wins over hast; two or more stresses ->
# other: sequences claim no single type); a text with only a preconditioning clause -> msl_preconditioning. With no
# stress in any text the row is a measurement test: test_type = its measurement type (MEASURANDS), else other.
# A leak (hermeticity) test is a measurement, not a stress: "He leak after multiple reflow" = reflow / leak.
STRESS_TYPES: list[tuple[str, str]] = [
    (r"\bdrops?\b", "drop"),
    (r"thermal shock|\bts\b", "thermal_shock"),
    (r"vibration", "vibration"),
    (r"(?<!thermal )\bshocks?\b", "mechanical_shock"),
    (r"u-?hast|unbiased hast|un-biased hast", "uhast"),
    (r"(?<![-u])\bhast\b", "hast"),
    (r"\bthb\b|temperature-humidity bias", "temp_humidity_bias"),
    (r"damp heat", "damp_heat"),
    (r"temperature cycl|thermal cycl|\btc[tbgcj]?\b|\btct|\bdtc\b|\bt/c\b|\btc[-_(/]", "temperature_cycling"),
    (r"\bhts|high[- ]temperature storage|\bbake\b", "high_temp_storage"),
    (r"\blts\b|low temperature storage", "low_temp_storage"),
    (r"reflow|\bmr6x\b|\bmr\)", "reflow"),
]
PRECON = re.compile(r"\bmsl|pre-?con|preconditioning|\bmst l3|\bmrtl", re.I)
# D60: measurement keywords on the PK parameter -> measurand (also the test_type of rows without a stress).
MEASURANDS: list[tuple[str, str]] = [
    (r"shear", "die_shear"),
    (r"adhesion|peel|cross-cut|tape test|stud-pull|bond strength", "adhesion"),
    (r"thermal resistance|thetajc", "thermal_resistance"),
    (r"(?<!thermal )\bresistance\b|continuity|(?<!thermal )conductivity", "electrical_resistance"),
    (r"\bil\b|insertion loss", "optical_loss"),
    (r"warpage", "warpage"),
    (r"leak|pressure test", "leak"),
]
# D57 / D53 (amended): locator words at the end of an EO wafer_supplier qualifier go to notes, not stated_spec.
LOCATOR_WORDS = re.compile(
    r"^(?:(?:per|as written in|in|see)\s+)?(?:the\s+)?(?:acknowledge?ments?|methods|main text|supplementary\b.*)$", re.I
)
# D59: designation patterns on the PK test_standard string -> (designation, body token for org requests).
STD_PATTERNS: list[tuple[str, Callable[[re.Match[str]], str], str]] = [
    (r"JESD22-?([AB])-?(\d{3})", lambda m: f"JESD22-{m[1].upper()}{m[2]}", "JEDEC"),
    (r"JESD(?!22)(\d+)(-\d+)?", lambda m: f"JESD{m[1]}{m[2] or ''}", "JEDEC"),
    (r"J-STD-0?(\d{2,3})", lambda m: f"J-STD-{int(m[1]):03d}", ""),
    (r"AEC-Q(\d{3})", lambda m: f"AEC-Q{m[1]}", "AEC"),
    (r"\bIEC[- ]?(\d{5}(?:-\d+)*)", lambda m: f"IEC {m[1]}", "IEC"),
    (r"MIL-STD[- ]?883(?![-\d])", lambda m: "MIL-STD-883", ""),
    (r"Telcordia GR-(\d+)", lambda m: f"Telcordia GR-{m[1]}", "Telcordia"),
    (r"\bASTM[- ]?([A-Z])(\d+)", lambda m: f"ASTM {m[1].upper()}{m[2]}", "ASTM"),
    (r"\bISO (\d+)", lambda m: f"ISO {m[1]}", "ISO"),
    (r"\bIPC-?(\d{4})", lambda m: f"IPC-{m[1]}", "IPC"),
    (r"\bIPC[- ]TM[- ]650", lambda m: "IPC-TM-650", "IPC"),
    (r"\bJEDEC SPP-(\d+)", lambda m: f"JEDEC SPP-{m[1]}", "JEDEC"),
    (r"\bASME B(\d+\.\d+)", lambda m: f"ASME B{m[1]}", "ASME"),
]
NUM = r"(-?\d+(?:\.\d+)?)"
T_RANGE = re.compile(rf"(?<![\w.]){NUM}\s*(?:°\s*)?C?\s*(?:to|/|~)\s*\+?{NUM}\s*°?\s*C\b")
T_RH = re.compile(rf"(?<![\w.]){NUM}\s*°?\s*C\s*[/,]\s*{NUM}\s*%\s*RH", re.I)
# D60 (am. round 2): in humidity-type rows "110 C / 85 %" (RH not written) is the same temperature / RH pair.
T_PCT = re.compile(rf"(?<![\w.]){NUM}\s*°?\s*C\s*[/,]\s*{NUM}\s*%(?!\s*RH)", re.I)
RH = re.compile(rf"(?<![\w.]){NUM}\s*%\s*RH", re.I)
T_ONE = re.compile(rf"(?<![\w.]){NUM}\s*°?\s*C\b")
# D60: which parsed fields apply to which test type: RANGE_T_TYPES, HUMID_TYPES, SINGLE_T_TYPES (rules_supply).


# --------------------------------------------------------------------------- helpers


def num(s: str) -> str:
    """Normalize a parsed number (drop a trailing .0)."""
    v = float(s)
    return str(int(v)) if v == int(v) else str(v)


def split_top(cell: str) -> list[str]:
    """Split on ';' outside parentheses."""
    parts, depth, cur = [], 0, ""
    for ch in cell:
        depth += (ch == "(") - (ch == ")")
        if ch == ";" and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    parts.append(cur.strip())
    return [p for p in parts if p]


def parse_wafer_part(part: str) -> tuple[list[str], str]:
    """(name candidates, qualifier): trailing parenthetical = qualifier; candidates = name and its first comma part."""
    name, qual = part, ""
    i = part.find("(")
    if i > 0 and part.endswith(")"):
        name, qual = part[:i].strip(), part[i + 1 : -1].strip()
    cands = [name]
    first = name.split(",")[0].strip()
    if first and first != name:
        cands.append(first)
    return cands, qual


def split_locator_words(qual: str) -> tuple[str, str]:
    """(stated spec, locator words): trailing ',' / ';' segments that only say where the fact is printed."""
    parts = re.split(r"(\s*[,;]\s*)", qual)  # [segment, separator, segment, ...]
    loc: list[str] = []
    while parts and LOCATOR_WORDS.match(parts[-1].strip()):
        loc.insert(0, parts[-1].strip())
        parts = parts[:-2]
    return "".join(parts).strip(), "; ".join(loc)


def wafer_category(text: str, name: bool = False) -> str:
    """Keyword category of a qualifier; `name` = text is an org name (service words such as "Integration" in
    "Novel Si Integration Technology" are then not a B5 service)."""
    low = text.lower()
    for pat, cat in WAFER_KEYWORDS:
        if name and cat == "B5":
            continue
        if re.search(pat, low):
            return cat
    return ""


def platform_category(platforms: set[str]) -> tuple[str, str]:
    cats = set()
    for p in platforms:
        for pre, cat in PLATFORM_CATEGORY:
            if p.startswith(pre):
                cats.add(cat)
                break
        else:
            cats.add("")
    if len(cats) == 1 and "" not in cats:
        return cats.pop(), ";".join(sorted(platforms))
    return "", ""


def wafer_role(category: str) -> str:
    if category[:2] in ("A4", "A5"):
        return "material_supply"
    if category == "B5":
        return "post_processing"
    return "wafer_supply"


STEP_SEP = re.compile(r"\s+\+\s+|,?\s+then\s+|,?\s+followed by\s+", re.I)


def split_steps(text: str) -> list[str]:
    """Split a step sequence on top-level ' + ' / 'then' / 'followed by' (not inside parentheses)."""
    depth = [0] * (len(text) + 1)
    d = 0
    for i, ch in enumerate(text):
        d += (ch == "(") - (ch == ")")
        depth[i + 1] = d
    parts, last = [], 0
    for m in STEP_SEP.finditer(text):
        if depth[m.start()] == 0:
            parts.append(text[last : m.start()].strip())
            last = m.end()
    parts.append(text[last:].strip())
    return [x for x in parts if x]


def split_precon(text: str) -> tuple[str, str]:
    """(main, preconditioning). In each top-level ';' segment the preconditioning clause starts at an MSL / precon
    keyword and runs over the following ' + ' / 'then' steps that name no stress other than reflow (bake, soak, THS
    and reflow steps belong to it); the first step naming another stress (TC, uHAST, HTS, ...) and the steps after
    it are the row's main stress text again, as is the text before the keyword."""
    main: list[str] = []
    pre: list[str] = []
    for seg in split_top(text):
        m = PRECON.search(seg)
        if not m:
            main.append(seg)
            continue
        main.append(seg[: m.start()].strip(" +,"))
        steps = split_steps(seg[m.start() :])
        k = 1
        while k < len(steps) and set(_stresses(steps[k])) <= {"reflow"}:
            k += 1
        pre.append(" + ".join(steps[:k]))
        main.append(" + ".join(steps[k:]))
    return "; ".join(x for x in main if x), "; ".join(pre)


def _stresses(text: str, condition: bool = False, measurand: str = "") -> list[str]:
    """Stress types named in a text; uhast wins over hast; reflow is dropped when another stress is named (a reflow
    step before a stress is assembly or preconditioning). In condition text, cycling / shock keywords count only with
    a stated temperature range or the word cycle (TCB = thermocompression bonding, Tc = case temperature). For warpage
    rows, reflow names the temperature profile along which warpage is measured (or a flatness requirement), not a
    stress."""
    low = text.lower()
    found = list(dict.fromkeys(t for pat, t in STRESS_TYPES if re.search(pat, low)))
    if measurand == "warpage" and "reflow" in found:
        found.remove("reflow")
    if condition and not (T_RANGE.search(text) or "cycl" in low):
        found = [t for t in found if t not in RANGE_T_TYPES]
    if "uhast" in found and "hast" in found:
        found.remove("hast")
    if len(found) > 1 and "reflow" in found:
        found.remove("reflow")
    return found


def classify_measurand(parameter: str) -> str:
    low = parameter.lower()
    found = list(dict.fromkeys(t for pat, t in MEASURANDS if re.search(pat, low)))
    return found[0] if len(found) == 1 else ""


def classify_test(parameter: str, standard: str, condition: str = "", variant: str = "") -> str:
    """D60 (amended): stress from parameter, then condition, then PK variant (not one starting with "before": a
    baseline), then printed standard; else the measurement type."""
    meas = classify_measurand(parameter)
    if variant.strip().lower().startswith("before"):
        variant = ""
    for text, is_cond in ((parameter, False), (condition, True), (variant, False), (standard, False)):
        main, pre = split_precon(text)
        found = _stresses(main, is_cond, meas)
        if len(found) == 1:
            return found[0]
        if len(found) > 1:
            return "other"
        if pre:
            return "msl_preconditioning"
    return meas or "other"


def parse_standards(printed: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for pat, fmt, body in STD_PATTERNS:
        for m in re.finditer(pat, printed, re.I):
            d = (fmt(m), body)
            if d not in out:
                out.append(d)
    return out


def printed_body_prefixes(printed: str) -> dict[str, str]:
    """Designations whose pattern names no body -> a body prefix printed right before them (e.g. IPC/JEDEC)."""
    out: dict[str, str] = {}
    for pat, fmt, body in STD_PATTERNS:
        if body:
            continue
        for m in re.finditer(pat, printed, re.I):
            words = printed[: m.start()].split()
            if words and re.fullmatch(r"[A-Z]{2,}(?:/[A-Z]{2,})*", words[-1]):
                out[fmt(m)] = words[-1]
    return out


def parse_conditions(cond: str, test_type: str) -> dict[str, str]:
    """D60: a field is parsed only for test types where it is the stress (range: cycling / shock; temperature + RH:
    humidity and preconditioning; single temperature: storage and humidity tests, never preconditioning) and only when
    the pattern occurs exactly once in the relevant text; otherwise the field stays empty and the text keeps the
    information. The relevant text is the preconditioning clause for msl_preconditioning rows and the condition
    without its preconditioning clauses for every other type (a precon soak, bake or reflow is not the row's stress)."""
    out = {"t_min_c": "", "t_max_c": "", "temp_c": "", "rh_pct": ""}
    main, pre = split_precon(cond)
    if test_type == "msl_preconditioning":
        cond = pre or cond  # a condition without a precon keyword describes the preconditioning itself
    else:
        cond = main
    rh_pairs = {(num(a), num(b)) for a, b in T_RH.findall(cond)}
    if test_type in HUMID_TYPES:
        rh_pairs |= {(num(a), num(b)) for a, b in T_PCT.findall(cond)}
    if test_type in RANGE_T_TYPES:
        rng = {(num(a), num(b)) for a, b in T_RANGE.findall(cond)} - rh_pairs
        if len(rng) == 1:
            lo, hi = next(iter(rng))
            if float(lo) < float(hi):
                out["t_min_c"], out["t_max_c"] = lo, hi
    if test_type in HUMID_TYPES:
        if len(rh_pairs) == 1:
            out["temp_c"], out["rh_pct"] = next(iter(rh_pairs))
        elif not rh_pairs:
            rhs = {num(a) for a in RH.findall(cond)}
            if len(rhs) == 1:
                out["rh_pct"] = rhs.pop()
    if test_type in SINGLE_T_TYPES and not out["temp_c"] and not rh_pairs:
        temps = {num(a) for a in T_ONE.findall(cond)}
        if len(temps) == 1:
            out["temp_c"] = temps.pop()
    return out


def merge_table(
    table: str, new: list[Row], key: str, dry: bool, log: RunLog, replace: set[str] | None = None, full: bool = False
) -> list[Row]:
    """Append rows whose key is new; existing rows stay untouched (differences are logged), except ids in `replace`:
    replaced by the rebuilt row, or removed when the rebuild has no row with that id. `full` = the rebuild covered all
    inputs (no --only / --limit), so ids on disk it did not produce are reported as stale."""
    replace = replace or set()
    path = ROOT / "data" / "supply" / f"{table}.csv"
    cur = read_csv(path) if path.exists() else []
    cols = columns(table)
    built = {r[key]: r for r in new}
    have = {r[key] for r in cur}
    out: list[Row] = []
    replaced = removed = differ = unchanged = 0
    for old in cur:
        rid = old[key]
        r = built.get(rid)
        if rid in replace:
            if r is None:
                if full:
                    removed += 1
                    log.event("removed", table=table, id=rid)
                    continue
                log.info(f"WARN {table} {rid}: in --replace-ids but not rebuilt in this partial run: kept")
            elif any(old.get(c, "") != r.get(c, "") for c in cols):
                replaced += 1
                log.event("replaced", table=table, id=rid)
                out.append(r)
                continue
        if r is None:
            if full:
                log.event("stale", "kept", table=table, id=rid)
        elif any(old.get(c, "") != r.get(c, "") for c in cols):
            differ += 1
            log.event("differs", "skipped", table=table, id=rid)
        else:
            unchanged += 1
        out.append(old)
    add = [r for rid, r in built.items() if rid not in have]
    stale = sum(1 for rid in have if rid not in built) - removed if full else 0
    log.info(
        f"{table}: {len(cur)} existing, {len(add)} new, {unchanged} unchanged, {differ} differ (kept), "
        f"{replaced} replaced, {removed} removed, {stale} stale (kept)"
    )
    log.event("merge", table=table, existing=len(cur), new=len(add), differ=differ, replaced=replaced, removed=removed)
    header_ok = path.exists() and read_header(path) == cols
    if not dry and (add or replaced or removed or not header_ok):
        write_csv(path, cols, [*out, *add])
    return add


def merge_requests(reqs: Requests, cur_yaml: dict[str, Any], m: Matcher, dry: bool, log: RunLog) -> None:
    """Merge requests into the staging file. Printed names curated as aliases of a registry org (`alias_requests`) are
    alias requests (kind alias, alias_of_org_id set), never new-org requests; `request_notes` annotate printed
    variants of one org. Existing rows are kept (source ids are unioned); a row whose printed name the registry now
    matches is status resolved with resolved_org_id (the rebuild then appends its rows), else open."""
    aliases: dict[str, dict[str, str]] = cur_yaml.get("alias_requests") or {}
    notes: dict[str, str] = cur_yaml.get("request_notes") or {}
    cur = read_csv(REQUESTS) if REQUESTS.exists() else []
    rows: dict[tuple[str, str, str, str], Row] = {}
    for r in cur:
        if r["printed"] in aliases and r["kind"] != "alias":
            log.event("request_now_alias", "removed", printed=r["printed"], kind=r["kind"])
            k = (r["corpus"], "alias", r["printed"], r["column"])
            reqs.setdefault(k, set()).update(split_list(r["source_ids"]))
            continue
        rows[(r["corpus"], r["kind"], r["printed"], r["column"])] = {c: r.get(c, "") for c in REQUEST_COLUMNS}
    for k, sids in reqs.items():
        r = rows.setdefault(k, {"corpus": k[0], "kind": k[1], "printed": k[2], "column": k[3]})
        for c in REQUEST_COLUMNS:
            r.setdefault(c, "")
        r["source_ids"] = ";".join(sorted(set(split_list(r["source_ids"])) | sids))
        if k[1] == "standards_body" and not r["notes"]:
            r["notes"] = "body named in or implied by the designation prefix of the cited standards"
    for r in rows.values():
        if r["kind"] == "alias" and r["printed"] in aliases:
            r["alias_of_org_id"] = aliases[r["printed"]]["org"]
            r["notes"] = aliases[r["printed"]]["why"]
        elif r["printed"] in notes:
            r["notes"] = notes[r["printed"]]
        oids, _ = m.match(r["printed"], r["corpus"])
        r["status"] = "resolved" if oids else "open"
        r["resolved_org_id"] = ";".join(oids)
    log.info(f"org requests: {sum(r['status'] == 'resolved' for r in rows.values())} resolved by the registry")
    out = sorted(rows.values(), key=lambda r: (r["corpus"], r["kind"], r["printed"]))
    log.info(f"org requests: {len(cur)} existing, {len(out)} after merge")
    if not dry:
        write_csv(REQUESTS, REQUEST_COLUMNS, out)


def _select(ids: list[str], only: set[str], limit: int | None) -> list[str]:
    sel = [i for i in ids if not only or i in only]
    return sel[:limit] if limit else sel


def usage_row(pid: str, ver: str, org: str, role: str, cat: str, column: str, spec: str, note: str) -> Row:
    sid = f"eo:{pid}"
    return {
        "usage_id": usage_id(sid, org, role),
        "source_id": sid,
        "org_id": org,
        "product_id": "",
        "category_id": cat,
        "role": role,
        "stated_spec": spec,
        "locator": atlas_anchor("eo", "papers.csv", pid, column),
        "extraction": "atlas_import",
        "basis": "stated",
        "verified_on": ver,
        "notes": note,
    }


# --------------------------------------------------------------------------- EO step


def build_eo(
    m: Matcher, cur: dict[str, Any], orgs: dict[str, Row], sources: set[str], args: argparse.Namespace, log: RunLog
) -> tuple[list[Row], list[Row], Requests]:
    papers = {p.paper_id: p for p in eo.papers()}
    raw = {r["paper_id"]: r for r in read_csv(input_path("eo_atlas") / "data" / "papers.csv")}
    plats: dict[str, set[str]] = defaultdict(set)
    for d in eo.devices():
        plats[d.paper_id].add(d.waveguide_platform)
    fab_roles: dict[str, dict[str, str]] = cur.get("fab_org_roles") or {}
    fab_cat = {(e["paper"], e["org"]): e for e in cur.get("fab_categories") or []}
    wafer_parts: dict[str, list[dict[str, str]]] = cur.get("wafer_parts") or {}
    wafer_defaults: dict[str, dict[str, str]] = cur.get("wafer_org_defaults") or {}
    wafer_cats = {(e["paper"], e["org"]): e for e in cur.get("wafer_categories") or []}
    aliases: dict[str, dict[str, str]] = cur.get("alias_requests") or {}
    procs_by_paper: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for e in cur.get("processes") or []:
        procs_by_paper[e["paper"]].append(e)
    used_fab_cat: set[tuple[str, str]] = set()

    ids = [pid for pid, p in papers.items() if p.foundry_or_fab or p.wafer_supplier or procs_by_paper.get(pid)]
    sel = _select(sorted(ids), args.only, args.limit)
    usage: list[Row] = []
    procs: list[Row] = []
    reqs: Requests = defaultdict(set)
    for pid in sel:
        p = papers[pid]
        sid = f"eo:{pid}"
        if sid not in sources:
            log.info(f"WARN {sid} not in sources.csv: paper skipped")
            continue
        ver = raw[pid]["verified_on"]

        for name in p.foundry_or_fab:
            oids, basis = m.match(name, "eo")
            if not oids:
                reqs[("eo", "foundry_or_fab", name, "foundry_or_fab")].add(sid)
                log.event("unmapped", "request", paper=pid, column="foundry_or_fab", printed=name)
                continue
            for oid in oids:
                note = f"printed {name} ({basis} match)" if basis != "name" else ""
                if orgs[oid]["org_type"] == "facility":
                    role, cat = "facility_use", "B7"
                elif oid in fab_roles:
                    role, cat = fab_roles[oid]["role"], fab_roles[oid]["category"]
                elif (pid, oid) in fab_cat:
                    e = fab_cat[(pid, oid)]
                    used_fab_cat.add((pid, oid))
                    role, cat = e.get("role", "fabrication"), e["category"]
                    if cat == "B":
                        note = "; ".join(x for x in (note, "B subcategory not stated in the EO record") if x)
                    note = "; ".join(x for x in (note, e.get("note", "")) if x)
                else:
                    role, cat = "fabrication", "B"
                    note = "; ".join(x for x in (note, "B subcategory not stated in the EO record") if x)
                usage.append(usage_row(pid, ver, oid, role, cat, "foundry_or_fab", "", note))

        # D57 (amended): an org of this paper's foundry_or_fab whose wafer_supplier part has a B category (SiN wafers,
        # growth / integration service) states the same fact: one row, the foundry_or_fab one.
        fab_rows = {
            u["org_id"]: u
            for u in usage
            if u["source_id"] == sid and u["role"] in ("fabrication", "post_processing", "mpw_access")
        }
        parts: list[tuple[list[str], str, str]] = []
        if pid in wafer_parts:
            parts = [([e["printed"]], e.get("qualifier", ""), e.get("note", "")) for e in wafer_parts[pid]]
        elif p.wafer_supplier:
            for part in split_top(p.wafer_supplier):
                if NO_SUPPLIER.search(part):
                    log.event("no_supplier", "skipped", paper=pid, part=part)
                    continue
                parts.append((*parse_wafer_part(part), ""))
        for cands, qual, pnote in parts:
            spec, locw = split_locator_words(qual)
            oids, basis, printed = [], "unmapped", cands[0]
            for c in cands:
                oids, basis = m.match(c, "eo")
                if oids:
                    printed = c
                    break
            if not oids:
                kind = "alias" if cands[0] in aliases else "wafer_supplier"
                reqs[("eo", kind, cands[0], "wafer_supplier")].add(sid)
                log.event("unmapped", "request", paper=pid, column="wafer_supplier", printed=cands[0], kind=kind)
                continue
            for oid in oids:
                notes = [f"printed {printed} ({basis} match)"] if basis != "name" else []
                notes += [x for x in (pnote, f"EO cell locator words: {locw}" if locw else "") if x]
                cat = ""
                if (pid, oid) in wafer_cats:  # D57: per-(paper, org) override first
                    cat = wafer_cats[(pid, oid)]["category"]
                    notes.append(f"category: curation per-paper override ({wafer_cats[(pid, oid)]['basis']})")
                cat = cat or wafer_category(spec) or wafer_category(printed, name=True)
                if cat.startswith("B") and oid in fab_rows:
                    f = fab_rows[oid]
                    if spec and not f["stated_spec"]:
                        f["stated_spec"] = spec
                    same = (
                        f"same fact as EO wafer_supplier part {printed} ({qual}): one row, stated_spec from that cell"
                    )
                    f["notes"] = "; ".join(x for x in (f["notes"], same, *notes) if x)
                    log.event("same_fact", "merged", paper=pid, org=oid, role=f["role"], wafer_category=cat)
                    continue
                if not cat and oid in wafer_defaults:
                    cat = wafer_defaults[oid]["category"]
                    notes.append("category: curation org default")
                if not cat:
                    cat, pl = platform_category(plats.get(pid, set()))
                    if cat:
                        notes.append(f"category from EO device platform {pl}")
                if not cat:
                    cat = "A"
                    notes.append("A subcategory not stated in the EO record")
                usage.append(usage_row(pid, ver, oid, wafer_role(cat), cat, "wafer_supplier", spec, "; ".join(notes)))

        for e in procs_by_paper.get(pid, []):
            oid = e["org"]
            broker = e.get("broker_org_id", "")
            note = e.get("notes", "")
            if e.get("broker_printed"):
                bids, _ = m.match(e["broker_printed"], "eo")
                if len(bids) == 1:
                    broker = bids[0]
                else:
                    reqs[("eo", "broker", e["broker_printed"], "process_name")].add(sid)
                    note = "; ".join(x for x in (note, f"broker {e['broker_printed']} named; not a registry org") if x)
            procs.append(
                {
                    "process_id": process_id(oid, sid),
                    "org_id": oid,
                    "process_name": e["process_name"],
                    "platform": e.get("platform", ""),
                    "wafer_mm": str(e.get("wafer_mm", "")),
                    "pdk_name": e.get("pdk_name", ""),
                    "pdk_open": "true" if e.get("pdk_open") else "",
                    "access_route": e.get("access_route", ""),
                    "broker_org_id": broker,
                    "source_id": sid,
                    "locator": atlas_anchor("eo", "papers.csv", pid, "process_name"),
                    "extraction": "atlas_import",
                    "basis": "stated",
                    "verified_on": ver,
                    "notes": note,
                }
            )
    if not args.only and not args.limit:
        unused = sorted(set(fab_cat) - used_fab_cat)
        if unused:
            log.info(f"WARN curation fab_categories entries not used: {unused}")
    log.info(f"eo: {len(sel)} papers, {len(usage)} usage rows, {len(procs)} process rows, {len(reqs)} requests")
    return usage, procs, reqs


# --------------------------------------------------------------------------- PK step


def build_pk(
    m: Matcher, sources: set[str], args: argparse.Namespace, log: RunLog
) -> tuple[list[Row], list[Row], Requests]:
    tvp = pk_metrics.tv_papers()
    rows = [r for r in pk_metrics.metrics() if r.test_standard.strip()]
    papers = sorted({tvp[r.tv_id] for r in rows if r.tv_id in tvp})
    sel = set(_select(papers, args.only, args.limit))
    stds: dict[str, Row] = {}
    prefixes: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    tests: list[Row] = []
    reqs: Requests = defaultdict(set)
    stat_ok = {"single", "mean", "min", "max", "range", "percentile", "other"}
    qual_ok = {"lt", "gt", "le", "ge", "approx"}
    pk_quals = {q["metric_id"]: q["qualifiers"] for q in read_csv(input_path("pk_atlas") / "data" / "metrics.csv")}
    for r in rows:
        paper = tvp.get(r.tv_id)
        if paper is None:
            log.info(f"WARN {r.metric_id}: tv_id {r.tv_id} not in PK test_vehicles.csv")
            continue
        if paper not in sel:
            continue
        sid = f"pk:{paper}"
        if sid not in sources:
            log.info(f"WARN {sid} not in sources.csv: {r.metric_id} skipped")
            continue
        printed = r.test_standard.strip()
        parsed = parse_standards(printed)
        for des, body in parsed:
            st = standard_id(des)
            if st not in stds:
                body_id = ""
                if body:
                    bids, _ = m.match(body, "pk")
                    if len(bids) == 1:
                        body_id = bids[0]
                    else:
                        reqs[("pk", "standards_body", body, "test_standard")].add(sid)
                stds[st] = {
                    "standard_id": st,
                    "designation": des,
                    "body_org_id": body_id,
                    "title": "",
                    "edition": "",
                    "scope": "",
                    "access": "unknown",
                    "notes": "" if body else "issuing body not named by the designation",
                }
            elif body and not stds[st]["body_org_id"]:
                reqs[("pk", "standards_body", body, "test_standard")].add(sid)
        for des, pre in printed_body_prefixes(printed).items():
            prefixes[standard_id(des)][pre].add(sid)
        ttype = classify_test(r.parameter, printed, r.condition, r.variant)
        measurand = classify_measurand(r.parameter)
        cond = parse_conditions(r.condition, ttype)
        notes = [] if parsed else ["printed standard string names no parsed designation"]
        val = r.value.strip()
        qualifier = ""
        for tok in split_list(pk_quals.get(r.metric_id, "")):
            q = tok.removeprefix("value:")
            if tok.startswith("value:") and q in qual_ok and not qualifier:
                qualifier = q
            else:
                notes.append(f"PK qualifier {tok} not mapped")
        if measurand == "optical_loss" and val.startswith("-"):
            notes.append("value sign as printed (negative IL); component tables store loss positive (D33), not flipped")
        tests.append(
            {
                "test_id": test_id("pk", r.metric_id),
                "source_id": sid,
                "tv_ref": r.tv_id,
                "parameter": r.parameter,
                "variant": r.variant.strip(),
                "test_type": ttype,
                "measurand": measurand,
                "standard_ids": ";".join(standard_id(d) for d, _ in parsed),
                "standard_printed": printed,
                "condition": r.condition.strip(),
                **cond,
                "value": val,
                "qualifier": qualifier,
                "value_text": r.value_text.strip(),
                "unit": r.unit.strip(),
                "statistic": r.statistic if r.statistic in stat_ok else "",
                "n_samples": r.n_samples.strip(),
                "pass_criterion": r.pass_criterion.strip(),
                "result": r.result.strip(),
                "scope": r.scope.strip(),
                "locator": r.locator.strip(),
                "atlas_ref": atlas_anchor("pk", "metrics.csv", r.metric_id),
                "basis": r.basis,
                "notes": "; ".join(notes),
            }
        )
    for st, pres in prefixes.items():
        if st in stds and not stds[st]["body_org_id"]:
            printed_as = "; ".join(f"{pre} in {', '.join(sorted(sids))}" for pre, sids in sorted(pres.items()))
            stds[st]["notes"] += f"; printed with body prefix {printed_as} (joint or unparsed body: no body_org_id)"
    log.info(f"pk: {len(sel)} papers, {len(tests)} test rows, {len(stds)} standards, {len(reqs)} requests")
    return list(stds.values()), tests, reqs


# --------------------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="compute and report, write nothing")
    ap.add_argument("--limit", type=int, default=None, help="pilot: first N papers per step (sorted ids)")
    ap.add_argument("--only", default="", help="pilot: comma-separated EO / PK paper ids")
    ap.add_argument("--steps", default="eo,pk", help="comma-separated steps: eo, pk")
    ap.add_argument(
        "--replace-ids",
        default="",
        help="ids whose rows on disk are replaced by the rebuilt row (or removed when no longer rebuilt): "
        "comma-separated, or @file with one id per line",
    )
    args = ap.parse_args()
    args.only = {s.strip() for s in args.only.split(",") if s.strip()}
    rid_arg: str = args.replace_ids
    if rid_arg.startswith("@"):
        with open(rid_arg[1:], encoding="utf-8") as f:
            rid_arg = ",".join(line.strip() for line in f if line.strip() and not line.startswith("#"))
    replace = {s.strip() for s in rid_arg.split(",") if s.strip()}
    full = not args.only and not args.limit
    steps = {s.strip() for s in args.steps.split(",") if s.strip()}
    with RunLog("build_supply_seed", args.dry_run) as log:
        with CURATION.open() as f:
            cur: dict[str, Any] = yaml.safe_load(f)
        orgs = {r["org_id"]: r for r in read_csv(REGISTRY / "organizations.csv")}
        sources = {r["source_id"] for r in read_csv(REGISTRY / "sources.csv")}
        bad = [
            e["org"]
            for e in [*(cur.get("fab_categories") or []), *(cur.get("processes") or [])]
            if e["org"] not in orgs
        ]
        bad += [o for o in [*(cur.get("fab_org_roles") or {}), *(cur.get("wafer_org_defaults") or {})] if o not in orgs]
        if bad:
            log.info(f"ERROR curation names org ids not in the registry: {sorted(set(bad))}")
            return 1
        m = load_matcher()
        reqs: Requests = defaultdict(set)
        if replace:
            log.info(f"replace ids: {len(replace)}")
            log.event("replace_ids", n=len(replace))
        if "eo" in steps:
            usage, procs, r1 = build_eo(m, cur, orgs, sources, args, log)
            merge_table("product_usage", usage, "usage_id", args.dry_run, log, replace, full)
            merge_table("foundry_processes", procs, "process_id", args.dry_run, log, replace, full)
            for k, v in r1.items():
                reqs[k] |= v
        if "pk" in steps:
            stds, tests, r2 = build_pk(m, sources, args, log)
            merge_table("standards", stds, "standard_id", args.dry_run, log, replace, full)
            merge_table("reliability_tests", tests, "test_id", args.dry_run, log, replace, full)
            for k, v in r2.items():
                reqs[k] |= v
        merge_requests(reqs, cur, m, args.dry_run, log)
        log.event("done", dry_run=args.dry_run, steps=sorted(steps), only=sorted(args.only), limit=args.limit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
