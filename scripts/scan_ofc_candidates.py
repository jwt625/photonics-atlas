"""Rank OFC 2026 presentations for component distillation (DevLog-002) from title + abstract (metadata only).

Keyword classes per component class; papers already in the EO atlas (sources.csv same_as) and papers already
distilled are skipped; only papers with a cached text are kept. Writes data/_staging/components/ofc_candidates.csv and
batch files batches/ofc_NN.csv (round-robin by score).

Usage: uv run python scripts/scan_ofc_candidates.py [--dry-run] [--batch-size 12] [--min-score 2]
"""

from __future__ import annotations

import argparse
import json
import re
import sys

from photonics_atlas.csvio import read_csv, write_csv
from photonics_atlas.paths import REGISTRY, ROOT, STAGING, input_path
from photonics_atlas.runlog import RunLog

CLASSES = {
    "laser": r"\blaser|DFB|DBR|PCSEL|VCSEL|external (?:laser|light) source|\bELS\b|ELSFP|comb source|light source",
    "amplifier": r"\bSOA\b|semiconductor optical amplifier|waveguide amplifier",
    "wdm": r"\bAWG\b|arrayed waveguide|echelle|\b(?:de)?multiplexer|\bmux\b|\bdemux\b|interleaver|WDM filter|CWDM|LAN-WDM|DWDM filter",
    "photodetector": r"photodetector|photodiode|\bAPD\b|\bPD\b|receiver chip|responsivity",
    "coupler": r"grating coupler|edge coupler|fiber[- ]to[- ]chip|fiber coupling|spot[- ]size|micro-?lens|fiber array|\bFAU\b|wire bond|connector|expanded beam|fan-?out",
    "polarization": r"polari[sz]ation (?:splitter|rotator|controller|compensat|diversity|beam)|\bPSR\b|\bPBS\b",
    "phase_switch": r"thermo-?optic|phase shifter|optical switch|switch fabric|\bMEMS\b|phase[- ]change",
    "isolator": r"isolator|circulator|non-?reciprocal",
    "platform": r"waveguide loss|low[- ]loss waveguide|silicon nitride platform|platform|PDK|foundry",
    "resonator": r"micro-?ring|resonator|high-?Q",
}
EXCLUDE = r"transmission experiment|field trial|network|\bDSP\b|coherent detection algorithm|machine learning|routing|fiber sensing"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--batch-size", type=int, default=12)
    ap.add_argument("--min-score", type=int, default=2)
    args = ap.parse_args()
    with RunLog("scan_ofc_candidates", args.dry_run) as log:
        src = {s["native_id"]: s for s in read_csv(REGISTRY / "sources.csv") if s["corpus"] == "ofc2026"}
        done = {
            c["source_id"].removeprefix("ofc2026:")
            for c in read_csv(ROOT / "data" / "components" / "components.csv")
            if c["source_id"].startswith("ofc2026:")
        }
        recs = [r for r in json.loads(input_path("ofc_metadata").read_text()) if r.get("record_kind") == "presentation"]
        rows = []
        for r in recs:
            code = r["presentation_code"]
            s = src.get(code)
            if not s or s["same_as"] or s["text_cached"] != "true" or code in done:
                continue
            title = r.get("presentation_title") or ""
            text = title + " " + (r.get("abstract_text") or "")
            hits = {k: len(re.findall(p, text, re.IGNORECASE)) for k, p in CLASSES.items()}
            title_hits = sum(1 for p in CLASSES.values() if re.search(p, title, re.IGNORECASE))
            score = sum(min(v, 3) for v in hits.values()) + 2 * title_hits
            if re.search(EXCLUDE, title, re.IGNORECASE):
                score -= 3
            rows.append(
                {
                    "code": code,
                    "score": score,
                    "classes": ";".join(f"{k}:{v}" for k, v in hits.items() if v),
                    "session": r.get("session_track", ""),
                    "title": title,
                }
            )
        rows.sort(key=lambda x: -int(x["score"]))
        keep = [x for x in rows if int(x["score"]) >= args.min_score]
        log.info(f"OFC presentations considered {len(rows)}; candidates (score >= {args.min_score}) {len(keep)}")
        n = max(1, -(-len(keep) // args.batch_size))
        if not args.dry_run:
            cols = ["code", "score", "classes", "session", "title"]
            write_csv(STAGING / "components" / "ofc_candidates.csv", cols, rows)
            for i in range(n):
                write_csv(STAGING / "components" / "batches" / f"ofc_{i + 1:02d}.csv", cols, keep[i::n])
            log.info(f"wrote ofc_candidates.csv and {n} batch files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
