"""Build staged products / product_usage rows from a reviewed scanner batch (DevLog-003 D206-D209).

Input: data/_staging/supply/products/<batch>/review.csv, one line per fact the reviewer confirmed on the page
(columns REVIEW_COLUMNS), and candidates.csv (scanner candidates with the reviewer's verdict, for the precision report).
Each line: org = org_id (explicit) or the registry match of vendor_printed; lines whose vendor has no registry org are
held (not built) and staged as kind `vendor` requests in data/_staging/supply/org_requests.csv (D208). Checks against
the cached text: the model and (basis stated) the printed vendor occur on a cited page (NFKC, whitespace and
line-break hyphens normalized). Rows whose usage_id already exists in data/supply/ are skipped (logged).

Writes <batch>/products.csv and <batch>/product_usage.csv (schema columns, rebuilt on every run), then validates
data/ + the staged rows on a temporary copy with the full validator; exit 1 on errors the batch introduces.
--merge appends the staged rows to data/supply/ (append-only; for the coordinator after the audit, D206).

Usage:
  uv run python scripts/build_supply_staging.py pilot_01 --dry-run
  uv run python scripts/build_supply_staging.py pilot_01
  uv run python scripts/build_supply_staging.py pilot_01 --merge     (coordinator only, after audit)
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

from photonics_atlas.csvio import read_csv, read_header, split_list, write_csv
from photonics_atlas.orgmatch import load_matcher
from photonics_atlas.paths import REGISTRY, ROOT, STAGING
from photonics_atlas.rules_supply import (
    QUOTES,
    ROLE_SUBCATEGORY,
    ROLE_TOPS,
    STATED_SPEC_MAX,
    canonical_model,
    load_categories,
    product_id,
    usage_id,
)
from photonics_atlas.runlog import RunLog
from photonics_atlas.schema import columns
from photonics_atlas.supply_scan import Vendor, load_dictionary, norm_ws, page_text, printed_on, text_path
from photonics_atlas.textnorm import norm_key
from photonics_atlas.validate import validate

SUPPLY = ROOT / "data" / "supply"
BATCHES = STAGING / "supply" / "products"
REQUESTS = STAGING / "supply" / "org_requests.csv"
REVIEW_COLUMNS = [
    "source_id",
    "vendor_printed",
    "org_id",
    "model",
    "product_line",
    "category_id",
    "role",
    "basis",
    "locator",
    "stated_spec",
    "notes",
    "cand_ids",
    "reviewed_on",
]
# Review format v2 (D328): every candidate gets a verdict through review.csv alone. line_kind `fact` = one usage fact
# (its cand_ids are true); line_kind `verdict` = cand_ids that are not facts of their own, with `reason` one of
# VERDICT_REASONS (true: covered, no_vendor, dup; false: the rest).
REVIEW_COLUMNS_V2 = [*REVIEW_COLUMNS, "line_kind", "reason"]
TRUE_REASONS = {"covered", "no_vendor", "dup"}
FALSE_REASONS = {
    "affiliation",
    "acknowledgement",
    "funding",
    "coi",
    "own_org",
    "collaboration",
    "citation",
    "generic",
    "word_fragment",
    "not_this_work",
    "other",
}
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
CURATED_MARK = "; curated: "
GENERATED_NOTE = re.compile(r"scan_vendor_models batch \S+: [^;|]*(; gazetteer vendor [^;|]+)?")


def vendor_surfaces(gazetteer: list[Vendor]) -> dict[str, list[re.Pattern[str]]]:
    """Registry org -> regexes of its gazetteer vendors (to strip a leading vendor or brand token from a model)."""
    out: dict[str, list[re.Pattern[str]]] = {}
    for v in gazetteer:
        if v.org_id:
            out.setdefault(v.org_id, []).append(v.rx)
    return out


GENERIC_REST = {"optics", "software", "system", "systems", "tools", "tool", "suite", "studio", "solutions", "solver"}
MODEL_PREFIX = re.compile(r"^(model|type|series)\s+(?=\S)", re.I)
GENERIC_TAIL = re.compile(r"\s+(system|systems|series)$", re.I)


def strip_vendor(model: str, rxs: list[re.Pattern[str]]) -> str:
    """Product model from a printed model (D290, D317): a leading vendor / brand token of its own vendor is dropped
    (COMSOL Multiphysics -> Multiphysics, EPO-TEK 301-2 -> 301-2) unless only a generic word would remain (Ansys
    Optics stays Ansys Optics); a leading Model / Type / Series word and a trailing System / Series word are dropped
    (Model 110 -> 110, Multiprep System -> Multiprep)."""
    out = model
    for rx in rxs:
        mm = rx.match(out)
        if mm and mm.end() < len(out):
            rest = out[mm.end() :].lstrip(" -,")
            if rest and rest.lower() not in GENERIC_REST:
                out = rest
                break
    out = MODEL_PREFIX.sub("", out)
    return GENERIC_TAIL.sub("", out) if GENERIC_TAIL.sub("", out) else out


def gazetteer_hit(gazetteer: list[Vendor], printed: str, model: str) -> Vendor | None:
    text = f"{printed} {model}".strip()
    for v in gazetteer:
        mm = v.rx.search(text)
        if mm and mm.start() == 0:
            return v
    return None


class _Print:
    """Log to stdout only (--check-review writes no log files)."""

    def info(self, msg: str) -> None:
        print(msg)

    def event(self, *a: object, **k: object) -> None:
        pass

    def __enter__(self) -> _Print:
        return self

    def __exit__(self, *a: object) -> None:
        pass


BASES = {"stated", "inferred_from_model"}
PAGE_FORM = {"eo": re.compile(r"^p\.[0-9]+"), "pk": re.compile(r"^p\.[0-9]+"), "lit": re.compile(r"^p\.[0-9]+")}
PAGE_FORM["ofc2026"] = re.compile(r"^(p\.~[0-9]+|pNA)")


def lint_line(r: Row, cats: dict[str, dict[str, Any]], restricted: bool) -> list[str]:
    """Rules a review line must meet before any staging (also for held lines, which the validator never sees)."""
    out = []
    cid, role = r["category_id"], r["role"]
    if cid not in cats:
        out.append(f"category {cid!r} not in supply_categories.yaml")
    if role not in ROLE_TOPS:
        out.append(f"role {role!r} unknown")
    elif cid[:1] not in ROLE_TOPS[role]:
        out.append(f"role {role} does not allow category {cid} (D54)")
    elif role in ROLE_SUBCATEGORY and not ROLE_SUBCATEGORY[role].match(cid):
        out.append(f"{role} does not allow subcategory {cid} (D54)")
    if role == "facility_use" and cid != "B7":
        out.append("facility_use rows are B7")
    if r["basis"] not in BASES:
        out.append(f"basis {r['basis']!r} not in {sorted(BASES)}")
    if (
        len(cid) == 1
        and not r["notes"].startswith("category:")
        and any(str(c.get("parent") or "") == cid for c in cats.values())
    ):
        out.append("top-level category needs a note starting with 'category:'")
    corpus = r["source_id"].split(":", 1)[0]
    form = PAGE_FORM.get(corpus)
    if form and not form.match(r["locator"]):
        out.append(f"locator {r['locator']!r} not in the {corpus} page form")
    if not r["stated_spec"] or len(r["stated_spec"]) > STATED_SPEC_MAX:
        out.append(f"stated_spec empty or longer than {STATED_SPEC_MAX} characters")
    if re.search(r"acknowledge?ment|\bper the\b|\bp\.\s?~?\d", r["stated_spec"], re.I):
        out.append("locator words in stated_spec (acknowledgements, page); put them in notes / locator (D53 am.)")
    if restricted and any(q in r["stated_spec"] + r["notes"] for q in QUOTES):
        out.append("quotation marks in a restricted source's line (D53, D297)")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["reviewed_on"]):
        out.append("reviewed_on must be an ISO date")
    return out


def held_lines(m: Any, gazetteer: list[Vendor]) -> list[tuple[str, Row]]:
    """Fact lines of every batch whose vendor has no registry org (explicit org_id, registry name / alias, gazetteer)."""
    out = []
    for rp in sorted(BATCHES.glob("*/review.csv")):
        for r in read_csv(rp):
            if r.get("line_kind", "fact") not in ("fact", "") or r["org_id"]:
                continue
            ids, _ = m.match(r["vendor_printed"], r["source_id"].split(":", 1)[0])
            if len(ids) == 1:
                continue
            gz = gazetteer_hit(gazetteer, r["vendor_printed"], r["model"])
            if gz and gz.org_id:
                continue
            out.append((rp.parent.name, r))
    return out


def vendor_requests(reqs: list[Row], m: Any, gazetteer: list[Vendor], log: Any) -> list[Row]:
    groups: dict[str, dict[str, Any]] = {}
    for batch, r in held_lines(m, gazetteer):
        gz = gazetteer_hit(gazetteer, r["vendor_printed"], r["model"])
        key = gz.name if gz else norm_key(r["vendor_printed"])
        g = groups.setdefault(
            key,
            {
                "name": gz.name if gz else "",
                "printed": Counter(),
                "corpora": set(),
                "sources": set(),
                "cats": set(),
                "batches": set(),
            },
        )
        g["printed"][norm_ws(r["vendor_printed"])] += 1
        g["corpora"].add(r["source_id"].split(":", 1)[0])
        g["sources"].add(r["source_id"])
        g["cats"].add(f"{r['category_id']} {r['role']}")
        g["batches"].add(batch)
    old_vendor = [q for q in reqs if q["kind"] == "vendor"]
    curated: dict[str, list[str]] = {}
    for q in old_vendor:  # keep note text the build did not generate (e.g. the D278 TFS ruling)
        note = q["notes"]
        if CURATED_MARK in note:
            cur = note.split(CURATED_MARK, 1)[1]
        elif note.startswith("scan_vendor_models batches "):
            cur = ""
        else:  # legacy per-batch notes: drop the generated segments
            segs = [x.strip() for x in note.split("; ")]
            cur = "; ".join(x for x in segs if x and not x.startswith(("scan_vendor_models", "gazetteer vendor")))
        if cur:
            curated.setdefault(norm_key(q["printed"]), []).append(cur)
    out = [q for q in reqs if q["kind"] != "vendor"]
    grouped = {norm_key(v) for g in groups.values() for v in [*g["printed"], g["name"]] if v}
    out += [q for q in old_vendor if norm_key(q["printed"]) not in grouped]  # resolved / no longer held: kept as record
    for _key, g in sorted(groups.items()):
        printed = g["name"] or g["printed"].most_common(1)[0][0]
        variants = sorted(g["printed"])
        keep = [n for v in variants for n in curated.get(norm_key(v), [])]
        keep += curated.get(norm_key(printed), []) if norm_key(printed) not in {norm_key(v) for v in variants} else []
        note = (
            f"scan_vendor_models batches {', '.join(sorted(g['batches']))}: {', '.join(sorted(g['cats']))}; "
            f"printed variants: {' + '.join(variants)}" + (f"; gazetteer vendor {g['name']}" if g["name"] else "")
        )
        if keep:
            note += CURATED_MARK + " | ".join(dict.fromkeys(keep))
        ids: list[str] = []
        for v in [printed, *variants]:
            ids, _ = m.match(v, "")
            if len(ids) == 1:
                break
        out.append(
            {
                "corpus": ";".join(sorted(g["corpora"])),
                "kind": "vendor",
                "printed": printed,
                "column": "text",
                "alias_of_org_id": "",
                "status": "resolved" if len(ids) == 1 else "open",
                "resolved_org_id": ids[0] if len(ids) == 1 else "",
                "source_ids": ";".join(sorted(g["sources"])),
                "notes": note,
            }
        )
    log.info(
        f"vendor requests: {len(groups)} vendors from {sum(sum(g['printed'].values()) for g in groups.values())} held lines"
    )
    return out


def pages_of(locator: str) -> list[str]:
    """Page tokens of a locator such as 'p.14; p.17 Fig. 3' -> ['p.14', 'p.17']."""
    return [t.rstrip(";,") for t in locator.replace(";", " ; ").split() if t.startswith(("p.", "pNA"))]


def precision(cands: list[Row]) -> dict[str, object]:
    n = len(cands)
    t = sum(c["verdict"] == "true" for c in cands)
    out: dict[str, object] = {"candidates": n, "true": t, "false": n - t, "precision": round(t / n, 3) if n else None}
    for key in ("zone", "cue", "kind"):
        groups: dict[str, Counter[str]] = {}
        for c in cands:
            groups.setdefault(c[key], Counter())[c["verdict"]] += 1
        out[key] = {k: f"{v['true']}/{sum(v.values())}" for k, v in sorted(groups.items())}
    out["reasons"] = dict(Counter(c["reason"] for c in cands).most_common())
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("batch")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--merge", action="store_true", help="append the staged rows to data/supply/ (coordinator)")
    ap.add_argument(
        "--replace-ids",
        default="",
        help="with --merge: product / usage ids already in data/supply that are replaced by their rebuilt rows "
        "(mutable fields only; ids are immutable, D8, D326); comma list or @file",
    )
    ap.add_argument(
        "--check-review",
        action="store_true",
        help="validate review.csv only (page checks, verdict coverage, rules, temp-copy validation); writes nothing "
        "shared: no log files, no batch files, no org_requests (for parallel reviewers, D328)",
    )
    args = ap.parse_args()
    bdir = BATCHES / args.batch
    check = args.check_review
    with _Print() if check else RunLog("build_supply_staging", args.dry_run) as log:
        rpath = bdir / "review.csv"
        header = read_header(rpath) if rpath.exists() else []
        if header not in (REVIEW_COLUMNS, REVIEW_COLUMNS_V2):
            log.info(f"ERROR {rpath.relative_to(ROOT)} missing or header not {REVIEW_COLUMNS_V2}")
            return 1
        rows_all = read_csv(rpath)
        v2 = header == REVIEW_COLUMNS_V2
        review = [r for r in rows_all if not v2 or r["line_kind"] in ("fact", "")]
        cpath = bdir / "candidates.csv"
        cands = read_csv(cpath) if cpath.exists() else []
        derived: dict[str, tuple[str, str]] = {}
        if v2:
            known = {c["cand_id"] for c in cands}
            bad_lines = []
            for i, r in enumerate(rows_all, start=2):
                kind = r["line_kind"] or "fact"
                ids = split_list(r["cand_ids"])
                if kind not in ("fact", "verdict"):
                    bad_lines.append(f"line {i}: line_kind {kind!r}")
                elif kind == "verdict":
                    if r["reason"] not in TRUE_REASONS | FALSE_REASONS or not ids:
                        bad_lines.append(
                            f"line {i}: verdict line needs cand_ids and a reason in {sorted(TRUE_REASONS | FALSE_REASONS)}"
                        )
                    for x in ids:
                        v = ("true" if r["reason"] in TRUE_REASONS else "false", r["reason"])
                        if derived.get(x, v) != v:
                            bad_lines.append(f"line {i}: candidate {x} has two different verdicts")
                        derived[x] = v
                for x in ids:
                    if x not in known:
                        bad_lines.append(f"line {i}: unknown cand_id {x}")
            for r in review:
                for x in split_list(r["cand_ids"]):
                    if derived.get(x, ("true", ""))[0] == "false":
                        bad_lines.append(f"{r['source_id']} {r['model']}: candidate {x} is a fact and false")
                    derived.setdefault(x, ("true", ""))
            if missing := sorted(known - set(derived)):
                bad_lines.append(f"{len(missing)} candidates without a verdict: {missing[:20]}")
            for e in bad_lines:
                log.info(f"ERROR {e}")
            if bad_lines:
                return 1
            for c in cands:
                c["verdict"], c["reason"] = derived[c["cand_id"]]
        if cands:
            if unreviewed := [c["cand_id"] for c in cands if c["verdict"] not in ("true", "false")]:
                log.info(f"ERROR {len(unreviewed)} candidates without a verdict: {unreviewed[:10]}")
                return 1
            known = {c["cand_id"] for c in cands}
            for r in review:
                if bad := [x for x in split_list(r["cand_ids"]) if x not in known]:
                    log.info(f"ERROR review line {r['source_id']} {r['model']}: unknown cand_ids {bad}")
                    return 1
            log.info(f"raw scanner precision: {precision(cands)}")
            log.event("precision", "ok", **precision(cands))
        orgs = {o["org_id"] for o in read_csv(REGISTRY / "organizations.csv")}
        sources = {s["source_id"]: s for s in read_csv(REGISTRY / "sources.csv")}
        tree = load_categories()
        org_types = {o["org_id"]: o["org_type"] for o in read_csv(REGISTRY / "organizations.csv")}
        m = load_matcher(with_ror=False)
        gazetteer = [v for v in load_dictionary().vendors if v.origin == "gazetteer"]
        surfaces = vendor_surfaces(gazetteer)
        have_usage = {u["usage_id"] for u in read_csv(SUPPLY / "product_usage.csv")}
        have_products = {p["product_id"]: p for p in read_csv(SUPPLY / "products.csv")}
        texts: dict[str, str] = {}
        errors: list[str] = []
        products: dict[str, Row] = {}
        rebuilt_p: dict[str, Row] = {}
        rebuilt_u: dict[str, Row] = {}
        usage: list[Row] = []
        held: list[Row] = []
        skipped = 0
        for r in review:
            sid, oid, model = r["source_id"], r["org_id"], r["model"]
            tag = f"{sid} {r['vendor_printed']} {model or '(no model)'}"
            if sid not in sources:
                errors.append(f"{tag}: source not in sources.csv")
                continue
            corpus = sid.split(":", 1)[0]
            for e in lint_line(r, tree, sources[sid]["redistribution"] == "restricted_local_only"):
                errors.append(f"{tag}: {e}")
            if oid and oid not in orgs:
                errors.append(f"{tag}: org {oid} not in the registry")
                continue
            if not oid:
                ids, _ = m.match(r["vendor_printed"], corpus)
                oid = ids[0] if len(ids) == 1 else ""
            if not oid:  # brand or printed form of a gazetteer vendor with a registry org (D293)
                gz = gazetteer_hit(gazetteer, r["vendor_printed"], model)
                oid = gz.org_id if gz else ""
            # Page checks against the cached text (never a model or vendor that is not printed, D206).
            if sid not in texts:
                tp = text_path(sid)
                texts[sid] = tp.read_text(encoding="utf-8", errors="ignore") if tp else ""
            text = texts[sid]
            pl_printed = True
            if not text:
                log.info(f"WARN {tag}: no cached text, page checks skipped")
            else:
                pages = [page_text(text, corpus, p) for p in pages_of(r["locator"])]
                if not pages or not all(pages):
                    errors.append(f"{tag}: locator {r['locator']!r} names a page not in the text")
                    continue
                if model and not any(printed_on(model, pg) for pg in pages):
                    if all(any(printed_on(tok, pg) for pg in pages) for tok in model.split()):
                        log.info(f"WARN {tag}: model tokens printed on {r['locator']} but not contiguous (see notes)")
                    else:
                        errors.append(f"{tag}: model {model!r} not printed on {r['locator']}")
                if r["basis"] == "stated" and not any(printed_on(r["vendor_printed"], pg) for pg in pages):
                    errors.append(f"{tag}: vendor {r['vendor_printed']!r} not printed on {r['locator']} (basis stated)")
                if r["product_line"]:
                    pl_printed = any(printed_on(r["product_line"], pg) for pg in pages)
                if r["basis"] == "inferred_from_model" and not model:
                    errors.append(f"{tag}: inferred_from_model needs a model")
            if not oid:
                held.append(r)
                continue
            pmodel = strip_vendor(model, surfaces.get(oid, []))
            # (the D317 family-prefix auto rule was dropped by D348: product_line comes only from the review line, D326)
            pid = product_id(oid, pmodel) if pmodel else ""
            note = r["notes"]
            if pmodel and pmodel != model:
                note = "; ".join(x for x in (note, f"printed model: {model}") if x)
            if pid:
                prow = {
                    "product_id": pid,
                    "org_id": oid,
                    "category_id": r["category_id"],
                    "model": pmodel,
                    "product_line": r["product_line"],
                    "status": "unknown",
                    "datasheet_source_id": "",
                    "verified_on": r["reviewed_on"],
                    # a top-level category needs its reason on the product too (D52)
                    "notes": (r["notes"] if r["notes"].startswith("category:") else "")
                    if len(r["category_id"]) == 1
                    else "",
                }
                prev = products.get(pid) or have_products.get(pid)
                # D326: product_line only when the family is printed on a cited page, or an earlier merged row of the
                # same product carries it (its source printed it).
                if (
                    prow["product_line"]
                    and not pl_printed
                    and (not prev or prev["product_line"] != prow["product_line"])
                ):
                    errors.append(f"{tag}: product_line {prow['product_line']!r} not printed on {r['locator']} (D326)")
                    continue
                rebuilt_p.setdefault(pid, prow)
                if prev and prev["category_id"] != prow["category_id"]:
                    errors.append(f"{tag}: product {pid} already category {prev['category_id']}")
                    continue
                if (
                    prev
                    and prow["product_line"]
                    and canonical_model(prev["product_line"]) not in ("", canonical_model(prow["product_line"]))
                ):
                    errors.append(f"{tag}: product {pid} already product_line {prev['product_line']!r}")
                    continue
                if prev and prev["model"] != pmodel and f"printed model: {model}" not in note:
                    note = "; ".join(x for x in (note, f"printed model: {model}") if x)  # same canonical model (D290)
                if pid in products and not products[pid]["product_line"]:
                    products[pid]["product_line"] = prow["product_line"]
                if pid not in have_products:
                    products.setdefault(pid, prow)
            uid = usage_id(sid, oid, r["role"], pid)
            if any(u["usage_id"] == uid for u in usage):
                errors.append(f"{tag}: duplicate usage {uid} in the batch (one row per source, org, role, product)")
                continue
            urow = {
                "usage_id": uid,
                "source_id": sid,
                "org_id": oid,
                "product_id": pid,
                "category_id": r["category_id"],
                "role": r["role"],
                "stated_spec": r["stated_spec"],
                "locator": r["locator"],
                "extraction": "scan_review",
                "basis": r["basis"],
                "verified_on": r["reviewed_on"],
                "notes": note,
            }
            if uid in have_usage:
                rebuilt_u[uid] = urow
                skipped += 1
                log.info(f"exists in data/supply, skipped: {uid}")
                continue
            usage.append(urow)
        for e in errors:
            log.info(f"ERROR {e}")
        log.info(
            f"review lines {len(review)}: staged usage {len(usage)}, products {len(products)}, held (no registry org) "
            f"{len(held)}, already in data/supply {skipped}"
        )
        cats = Counter(u["category_id"] for u in usage)
        log.info(f"staged usage by category: {dict(sorted(cats.items()))}")
        log.event("build", "ok" if not errors else "failed", usage=len(usage), products=len(products), held=len(held))
        if errors:
            return 1

        # Org requests for held vendors (D208, R17 / D347): one request per vendor over all batches, rebuilt from the
        # held fact lines of every batch review.csv (vendor = gazetteer vendor of the printed form, else the printed
        # name key); printed variants, corpora, sources and category / role pairs are listed. Other request kinds are
        # untouched; curated notes of earlier vendor rows are kept.
        reqs = read_csv(REQUESTS) if REQUESTS.exists() else []
        before = sum(q["kind"] == "vendor" for q in reqs)
        reqs = vendor_requests(reqs, m, gazetteer, log)
        log.info(f"org requests: vendor requests {before} -> {sum(q['kind'] == 'vendor' for q in reqs)}")

        for r in held:  # facility_use rows need a registry facility; held rows are checked here too
            if r["role"] == "facility_use" and org_types.get(r["org_id"], "facility") != "facility":
                log.info(f"ERROR {r['source_id']} {r['vendor_printed']}: facility_use org is not typed facility")
                return 1
        pcols, ucols = columns("products"), columns("product_usage")
        prods = sorted(products.values(), key=lambda p: p["product_id"])
        usage.sort(key=lambda u: u["usage_id"])
        # Validate data/ + staged rows on a temporary copy; only errors the batch introduces fail the build.
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            shutil.copytree(ROOT / "data", tmp / "data")
            write_csv(tmp / "data/supply/products.csv", pcols, [*read_csv(SUPPLY / "products.csv"), *prods])
            write_csv(tmp / "data/supply/product_usage.csv", ucols, [*read_csv(SUPPLY / "product_usage.csv"), *usage])
            rep = validate(tmp)
        baseline = set(validate(ROOT).errors)
        new_errors = [e for e in rep.errors if e not in baseline]
        for e in new_errors:
            log.info(f"ERROR validate: {e}")
        log.info(f"validation of data + staged rows: {len(new_errors)} new errors ({len(baseline)} pre-existing)")
        if new_errors:
            return 1
        if check:
            log.info(
                f"CHECK OK {args.batch}: {len(rows_all)} review lines ({len(review)} facts), {len(cands)} candidates "
                f"with a verdict; would stage {len(usage)} usage rows, {len(products)} products; held (no registry "
                f"org, would be org requests) {len(held)}: {sorted({r['vendor_printed'] for r in held})}"
            )
            return 0
        if args.dry_run:
            log.info("dry run: nothing written")
            return 0
        # Batch files hold every row this batch builds (also rows already merged), so they stay the batch record.
        write_csv(bdir / "products.csv", pcols, sorted(rebuilt_p.values(), key=lambda p: str(p["product_id"])))
        write_csv(
            bdir / "product_usage.csv", ucols, sorted([*usage, *rebuilt_u.values()], key=lambda u: str(u["usage_id"]))
        )
        write_csv(REQUESTS, REQUEST_COLUMNS, sorted(reqs, key=lambda q: (q["corpus"], q["kind"], q["printed"])))
        if v2 and cands:  # D328: candidate verdicts come from review.csv; fact reasons from the build
            staged_keys = {(u["source_id"], u["locator"], u["stated_spec"]) for u in [*usage, *rebuilt_u.values()]}
            first: dict[str, str] = {}
            for r in review:
                st = "row" if (r["source_id"], r["locator"], r["stated_spec"]) in staged_keys else "org_gap"
                for i, x in enumerate(split_list(r["cand_ids"])):
                    first.setdefault(x, st if i == 0 else "dup")
            for c in cands:
                if c["cand_id"] in first and c["verdict"] == "true" and not c["reason"]:
                    c["reason"] = first[c["cand_id"]]
            write_csv(cpath, read_header(cpath), cands)
        log.info(
            f"wrote {bdir.relative_to(ROOT)}/products.csv ({len(rebuilt_p)}), product_usage.csv "
            f"({len(usage) + len(rebuilt_u)}); new for data/supply: {len(prods)} products, {len(usage)} usage rows"
        )
        if args.merge:
            rep_ids = (
                split_list(Path(args.replace_ids[1:]).read_text().replace("\n", ";"))
                if args.replace_ids.startswith("@")
                else [x.strip() for x in args.replace_ids.split(",") if x.strip()]
            )
            cur_p = read_csv(SUPPLY / "products.csv")
            cur_u = read_csv(SUPPLY / "product_usage.csv")
            for rid in rep_ids:
                if rid not in rebuilt_p and rid not in rebuilt_u:
                    log.info(f"ERROR --replace-ids {rid}: not rebuilt by this batch")
                    return 1
            cur_p = [rebuilt_p[x["product_id"]] if x["product_id"] in rep_ids else x for x in cur_p]
            cur_u = [rebuilt_u[x["usage_id"]] if x["usage_id"] in rep_ids else x for x in cur_u]
            for rid in rep_ids:
                log.info(f"replaced in data/supply/: {rid}")
            write_csv(SUPPLY / "products.csv", pcols, [*cur_p, *prods])
            write_csv(SUPPLY / "product_usage.csv", ucols, [*cur_u, *usage])
            log.info(
                f"merged into data/supply/: +{len(prods)} products, +{len(usage)} usage rows, {len(rep_ids)} replaced"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
