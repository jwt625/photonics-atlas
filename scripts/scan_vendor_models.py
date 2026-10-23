"""Scan cached paper texts for vendor / model candidates (DevLog-003 D205). Proposes candidates only.

Corpora: eo (EO atlas references/<id>/text.md), pk (packaging atlas references/<id>/text.md), lit (this repo
references/<id>/text.md), ofc2026 (config/inputs.yaml ofc_text_dir/<code>-*.md; codes whose source has same_as are
skipped). Only sources registered in data/registry/sources.csv. Dictionary: config/supply_scanner.yaml + registry
vendor-like orgs (src/photonics_atlas/supply_scan.py).

Output: data/_local/supply/scan/candidates.jsonl (git-ignored: it holds sentence context, also from restricted texts);
one `source` record per scanned source and one `candidate` record per candidate. Sources already in the JSONL are
skipped (--force rescans them: their old records are dropped). --batch <name> also writes
data/_staging/supply/products/<name>/candidates.csv for the selected sources (no text; verdict / reason columns kept
from an existing file). Writes logs/scan_vendor_models_<ts>.log / .jsonl.

Usage:
  uv run python scripts/scan_vendor_models.py --only eo:mao2024,pk:ectc51846.2026.00176 --dry-run
  uv run python scripts/scan_vendor_models.py --only <ids> --batch pilot_01
  uv run python scripts/scan_vendor_models.py --corpus eo --limit 20
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from photonics_atlas.csvio import read_csv, write_csv
from photonics_atlas.paths import REGISTRY, ROOT, STAGING, input_path
from photonics_atlas.runlog import RunLog
from photonics_atlas.supply_scan import load_dictionary, scan_text, text_path

OUT = ROOT / "data" / "_local" / "supply" / "scan" / "candidates.jsonl"
BATCHES = STAGING / "supply" / "products"
CORPORA = ("eo", "pk", "lit", "ofc2026")
CAND_COLUMNS = [
    "cand_id",
    "source_id",
    "locator",
    "zone",
    "kind",
    "cue",
    "vendor",
    "vendor_printed",
    "org_id",
    "model",
    "model_type",
    "cat_hint",
    "infer_ok",
    "verdict",
    "reason",
]


def documents(corpora: set[str]) -> list[tuple[str, str, Path]]:
    """(source_id, corpus, text path) of every registered source with a cached text, sorted by source id."""
    src = {s["source_id"]: s for s in read_csv(REGISTRY / "sources.csv")}
    found: dict[str, tuple[str, Path]] = {}
    dirs = {"eo": input_path("eo_atlas") / "references", "pk": input_path("pk_atlas") / "references"}
    dirs["lit"] = ROOT / "references"
    for corpus, d in dirs.items():
        if corpus in corpora and d.is_dir():
            for p in sorted(d.glob("*/text.md")):
                found.setdefault(f"{corpus}:{p.parent.name}", (corpus, p))
    if "ofc2026" in corpora:
        od = input_path("ofc_text_dir")
        for p in sorted(od.glob("*.md")) if od.is_dir() else []:
            found.setdefault(f"ofc2026:{p.name.split('-')[0]}", ("ofc2026", p))
    out = []
    for sid, (corpus, p) in sorted(found.items()):
        s = src.get(sid)
        if s is None or (corpus == "ofc2026" and s["same_as"]):
            continue
        out.append((sid, corpus, p))
    return out


def batched_sources() -> set[str]:
    """Source ids already in a batch dir (candidates.csv or sources.csv of any batch)."""
    out: set[str] = set()
    for b in sorted(BATCHES.glob("*/")):
        for f in ("candidates.csv", "sources.csv"):
            if (b / f).exists():
                out |= {r["source_id"] for r in read_csv(b / f)}
    return out


def split_order(sids: list[str]) -> list[str]:
    """Deterministic corpus-mixed order: by sha1 of the source id."""
    return sorted(sids, key=lambda x: hashlib.sha1(x.encode()).hexdigest())


def candidate_rows(recs: list[dict[str, Any]], sel: set[str]) -> list[dict[str, str]]:
    rows = []
    for r in sorted(
        (r for r in recs if r["type"] == "candidate" and r["source_id"] in sel),
        key=lambda r: (r["source_id"], r["offset"]),
    ):
        row = {c: str(r.get(c, "")) for c in CAND_COLUMNS}
        row["cue"] = "true" if r["cue"] else "false"
        row["infer_ok"] = "true" if r["infer_ok"] else "false"
        row["verdict"] = row["reason"] = ""
        rows.append(row)
    return rows


def write_split(
    args: argparse.Namespace, docs: list[tuple[str, str, Path]], recs: list[dict[str, Any]], log: RunLog
) -> int:
    corpus = {sid: c for sid, c, _ in docs}
    order = split_order(list(corpus))
    if not order:
        log.info("split mode: nothing to batch")
        return 0
    n = max(1, round(len(order) / args.split_size))
    counts = {r["source_id"]: r["n_candidates"] for r in recs if r["type"] == "source"}
    for i in range(n):
        part = order[i::n]
        name = f"{args.split_prefix}_{args.split_start + i:02d}"
        bdir = BATCHES / name
        if (bdir / "candidates.csv").exists() or (bdir / "sources.csv").exists():
            log.info(f"ERROR {name} already exists; refusing to overwrite a batch")
            return 1
        cands = candidate_rows(recs, set(part))
        srcs = [{"source_id": s, "corpus": corpus[s], "n_candidates": counts.get(s, 0)} for s in sorted(part)]
        mix = Counter(corpus[s] for s in part)
        log.info(f"{name}: {len(part)} papers {dict(sorted(mix.items()))}, {len(cands)} candidates")
        log.event("split", "ok", batch=name, papers=len(part), candidates=len(cands), corpora=dict(mix))
        if not args.dry_run:
            write_csv(bdir / "candidates.csv", CAND_COLUMNS, cands)
            write_csv(bdir / "sources.csv", ["source_id", "corpus", "n_candidates"], srcs)
    return 0


def print_only(args: argparse.Namespace) -> int:
    """Read-only helpers for reviewers (no log files, nothing written)."""
    if args.print_source:
        tp = text_path(args.print_source)
        if tp is None:
            print(f"no cached text for {args.print_source}", file=sys.stderr)
            return 1
        print(tp.read_text(encoding="utf-8", errors="ignore"))
        return 0
    ctx = {r["cand_id"]: r for r in read_jsonl(args.out) if r["type"] == "candidate"}
    for c in read_csv(BATCHES / args.print_batch / "candidates.csv"):
        r = ctx.get(c["cand_id"], {})
        print(
            f"{c['cand_id']} {c['source_id']} {c['locator']} zone={c['zone']} kind={c['kind']} "
            f"vendor={c['vendor']} printed={c['vendor_printed']!r} org={c['org_id']} model={c['model']!r} "
            f"hint={c['cat_hint']} infer_ok={c['infer_ok']}\n    {r.get('context', '(no context in the local JSONL)')}"
        )
    return 0


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--corpus", default=",".join(CORPORA), help="comma list of eo,pk,lit,ofc2026")
    ap.add_argument("--only", default="", help="comma list of source ids (eo:<id>, pk:<id>, lit:<id>, ofc2026:<code>)")
    ap.add_argument("--limit", type=int, default=0, help="scan at most N new sources")
    ap.add_argument("--force", action="store_true", help="rescan sources already in the JSONL")
    ap.add_argument("--batch", default="", help="write data/_staging/supply/products/<batch>/candidates.csv")
    ap.add_argument(
        "--drop-reviewed", action="store_true", help="allow dropping reviewed candidates no longer produced (logged)"
    )
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--split-prefix",
        default="",
        help="full-corpus mode (D328): every source not yet in a batch dir, split into <prefix>_NN batches",
    )
    ap.add_argument("--split-start", type=int, default=2, help="first batch number of --split-prefix")
    ap.add_argument("--split-size", type=int, default=100, help="target papers per batch of --split-prefix")
    ap.add_argument(
        "--batch-new-only",
        action="store_true",
        help="with --batch: only candidates whose id is in no other batch dir (targeted rescans, D343); also writes "
        "sources.csv",
    )
    ap.add_argument("--print-batch", default="", help="read-only: print a batch's candidates with their context")
    ap.add_argument("--print-source", default="", help="read-only: print a source's cached text (page markers kept)")
    args = ap.parse_args()
    if args.print_batch or args.print_source:
        return print_only(args)
    corpora = {c.strip() for c in args.corpus.split(",") if c.strip()}
    if bad := corpora - set(CORPORA):
        print(f"unknown corpus {sorted(bad)}", file=sys.stderr)
        return 2
    only = [x.strip() for x in args.only.split(",") if x.strip()]
    with RunLog("scan_vendor_models", args.dry_run) as log:
        d = load_dictionary()
        nreg = sum(v.origin == "registry" for v in d.vendors)
        log.info(f"dictionary: {len(d.vendors) - nreg} gazetteer vendors, {nreg} registry orgs, {len(d.models)} models")
        for w in d.warnings:
            log.info(f"WARN {w}")
        docs = documents(corpora)
        if args.split_prefix:
            taken = batched_sources()
            docs = [x for x in docs if x[0] not in taken]
            log.info(f"split mode: {len(taken)} sources already in batches, {len(docs)} to batch")
        if only:
            have = {sid for sid, _, _ in docs}
            if missing := [x for x in only if x not in have]:
                log.info(f"ERROR not found (no cached text or no registered source): {missing}")
                return 1
            docs = [x for x in docs if x[0] in set(only)]
        recs = read_jsonl(args.out)
        done = {r["source_id"] for r in recs if r["type"] == "source"}
        todo = [x for x in docs if args.force or x[0] not in done]
        if args.limit:
            todo = todo[: args.limit]
        log.info(
            f"sources selected {len(docs)}, already scanned {len(done & {x[0] for x in docs})}, to scan {len(todo)}"
        )
        today = dt.date.today().isoformat()
        new: list[dict[str, Any]] = []
        for sid, corpus, path in todo:
            cands = scan_text(path.read_text(encoding="utf-8", errors="ignore"), corpus, sid, d)
            new.append(
                {
                    "type": "source",
                    "source_id": sid,
                    "corpus": corpus,
                    "n_candidates": len(cands),
                    "scanned_on": today,
                    "config_sha": d.config_sha,
                }
            )
            new.extend({"type": "candidate", **c} for c in cands)
            kinds = Counter(c["kind"] for c in cands)
            log.info(f"{sid}: {len(cands)} candidates {dict(kinds)}")
            log.event("scan", "ok", source_id=sid, n=len(cands))
        rescanned = {x[0] for x in todo}
        merged = [r for r in recs if r["source_id"] not in rescanned] + new
        ncand = sum(r["type"] == "candidate" for r in new)
        log.info(f"scanned {len(todo)} sources, {ncand} candidates")
        if not args.dry_run and todo:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            tmp = args.out.with_suffix(".tmp")
            tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in merged), encoding="utf-8")
            tmp.replace(args.out)
            log.info(f"wrote {args.out.relative_to(ROOT)} ({len(merged)} records)")
        if args.split_prefix:
            return write_split(args, docs, merged, log)
        if args.batch:
            sel = {x[0] for x in docs}
            rows = [r for r in merged if r["type"] == "candidate" and r["source_id"] in sel]
            if args.batch_new_only:
                seen: set[str] = set()
                for b in BATCHES.glob("*/candidates.csv"):
                    if b.parent.name != args.batch:
                        seen |= {r["cand_id"] for r in read_csv(b)}
                rows = [r for r in rows if r["cand_id"] not in seen]
                if not args.dry_run:
                    n_new = Counter(r["source_id"] for r in rows)
                    srcs = [{"source_id": x, "corpus": x.split(":")[0], "n_candidates": n_new[x]} for x in sorted(sel)]
                    write_csv(BATCHES / args.batch / "sources.csv", ["source_id", "corpus", "n_candidates"], srcs)
                log.info(f"batch-new-only: {len(rows)} candidates not in another batch")
            path = STAGING / "supply" / "products" / args.batch / "candidates.csv"
            old = {r["cand_id"]: r for r in read_csv(path)} if path.exists() else {}
            out = []
            for r in sorted(rows, key=lambda r: (r["source_id"], r["offset"])):
                row = {c: str(r.get(c, "")) for c in CAND_COLUMNS}
                row["cue"] = "true" if r["cue"] else "false"
                row["infer_ok"] = "true" if r["infer_ok"] else "false"
                row["verdict"] = old.get(r["cand_id"], {}).get("verdict", "")
                row["reason"] = old.get(r["cand_id"], {}).get("reason", "")
                out.append(row)
            if lost := set(old) - {r["cand_id"] for r in out}:
                reviewed = sorted(c for c in lost if old[c]["verdict"])
                log.info(f"note: {len(lost)} candidates of the existing batch file are no longer produced")
                if reviewed and not args.drop_reviewed:
                    log.info(f"ERROR reviewed candidates would be dropped (not written): {reviewed}")
                    return 1
                if reviewed:
                    log.info(f"dropping {len(reviewed)} reviewed candidates (--drop-reviewed): {reviewed}")
            if args.dry_run:
                log.info(f"dry run: would write {len(out)} rows to {path.relative_to(ROOT)}")
            else:
                write_csv(path, CAND_COLUMNS, out)
                log.info(f"wrote {path.relative_to(ROOT)} ({len(out)} candidates)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
