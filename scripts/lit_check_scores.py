"""Validate LLM scoring outputs against their batches (DevLog-006 S3). No network.

Input:  cache/literature/scoring/<group>_bNNN.jsonl (batch) and out_<group>_bNNN.jsonl (scores written by a scoring
        subagent following config/literature/scoring_prompt.md).
Checks per output: every batch uid scored exactly once and no foreign uid; JSON fields and types; class / subtype ids
        in data/schema/component_parameters.yaml; platform / band enums; score in 0-10 and consistent with the point
        components (clamp of the sum, D122 rubric); rationale <= 20 words.
Prints one line per batch (ok / errors) and exits 1 when any output has errors. Missing outputs are listed, not errors.

Usage: uv run python scripts/lit_check_scores.py [--only G1_b001,...] [--verbose]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

from photonics_atlas.paths import CACHE, ROOT

SCORING = CACHE / "literature" / "scoring"
BATCH_RE = re.compile(r"^(G\d+_b\d{3})\.jsonl$")
PLATFORMS = {
    "soi", "sin", "tfln", "lt", "inp", "gaas_algaas", "aln", "ta2o5", "sic", "diamond", "polymer", "al2o3",
    "silica_plc", "ge_sige", "bto", "chalcogenide", "hybrid", "other", "unstated",
}  # fmt: skip
BANDS = {"O", "C", "L", "multi", "visible", "uv", "mid_ir", "nir_other", "unstated"}
POINTS = {"measured": 3, "dedicated": 2, "numbers": 2, "conditions": 1, "industrial": 1, "record": 1}
PENALTIES = {"sim_only": -3, "review": -4, "system_level": -2, "out_of_scope": -10}


def load_classes() -> dict[str, set[str]]:
    with (ROOT / "data" / "schema" / "component_parameters.yaml").open() as f:
        reg = yaml.safe_load(f)
    return {c: set((v.get("subtypes") or {}).keys()) for c, v in reg["classes"].items()}


def read_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    rows, errs = [], []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as e:
            errs.append(f"line {i}: invalid JSON ({e})")
    return rows, errs


def check_row(r: dict[str, Any], classes: dict[str, set[str]]) -> list[str]:
    e: list[str] = []
    cls = r.get("classes")
    if not isinstance(cls, list) or any(c not in classes for c in cls):
        e.append(f"classes {cls!r}")
    for st in r.get("subtypes") or []:
        c, _, s = str(st).partition(".")
        if c not in classes or (s and s not in classes[c]):
            e.append(f"subtype {st!r}")
    if r.get("platform") not in PLATFORMS:
        e.append(f"platform {r.get('platform')!r}")
    if r.get("band") not in BANDS:
        e.append(f"band {r.get('band')!r}")
    score, comp = r.get("score"), r.get("c")
    if not isinstance(score, int) or not 0 <= score <= 10:
        e.append(f"score {score!r}")
    if not isinstance(comp, dict) or set(comp) != set(POINTS) | set(PENALTIES):
        e.append("c keys")
    elif isinstance(score, int):
        total = sum(POINTS[k] * bool(comp[k]) for k in POINTS) + sum(PENALTIES[k] * bool(comp[k]) for k in PENALTIES)
        if max(0, min(10, total)) != score:
            e.append(f"score {score} != clamp(sum {total})")
    if len(str(r.get("rationale", "")).split()) > 20:
        e.append("rationale > 20 words")
    for k in ("is_review", "eo_modulator_main", "industrial"):
        if not isinstance(r.get(k), bool):
            e.append(f"{k} not bool")
    return e


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", default="")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()
    only = {x for x in args.only.split(",") if x}
    classes = load_classes()
    bad, missing, ok = 0, [], 0
    for bp in sorted(SCORING.glob("G*_b*.jsonl")):
        m = BATCH_RE.match(bp.name)
        if not m or (only and m.group(1) not in only):
            continue
        name = m.group(1)
        op = SCORING / f"out_{name}.jsonl"
        if not op.exists():
            missing.append(name)
            continue
        batch, _ = read_jsonl(bp)
        out, errs = read_jsonl(op)
        want = [b["uid"] for b in batch]
        got = [o.get("uid") for o in out]
        if sorted(want) != sorted(str(g) for g in got):
            errs.append(f"uid mismatch: missing {len(set(want) - set(got))}, extra {len(set(got) - set(want))}, "
                        f"rows {len(got)} vs {len(want)}")  # fmt: skip
        for o in out:
            for x in check_row(o, classes):
                errs.append(f"{o.get('uid')}: {x}")
        if errs:
            bad += 1
            print(f"{name}: {len(errs)} errors")
            for x in errs[: (len(errs) if args.verbose else 5)]:
                print(f"  {x}")
        else:
            ok += 1
            print(f"{name}: ok ({len(out)})")
    print(f"ok {ok}, with errors {bad}, missing outputs {len(missing)}{': ' + ','.join(missing) if missing else ''}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
