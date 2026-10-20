"""Rank EO atlas papers for component back-fill (DevLog-002 TODO 8) and write distillation batches.

Regex scan of ../eo-modulator-atlas/references/<paper_id>/text.md (read-only): per component class, count windows
where a class keyword appears within 200 characters of a number with a component unit (dB, %, A/W, dB/cm, nA, GHz,
mW, Q). Counts are candidate signals, not values. Papers already in data/components are skipped. Batches mix classes
and platforms by round-robin over the score order.

Usage: uv run python scripts/scan_component_candidates.py [--dry-run] [--batch-size 10] [--min-hits 1]
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter

from photonics_atlas.adapters import eo
from photonics_atlas.csvio import read_csv, write_csv
from photonics_atlas.paths import ROOT, STAGING
from photonics_atlas.runlog import RunLog

CLASSES = {
    "grating_coupler": r"grating coupler|\bGCs?\b",
    "edge_coupler": r"edge coupler|spot[- ]size converter|\bSSC\b|inverse taper|facet loss|coupling loss",
    "splitter": r"\bMMI\b|multimode interference|directional coupler|Y[- ]branch|Y[- ]splitter|adiabatic coupler|splitter",
    "crossing": r"crossing",
    "resonator": r"intrinsic Q|loaded Q|quality factor|Q[_ ]?(?:i|int|L|load)",
    "wdm": r"\bAWG\b|arrayed waveguide|echelle|demultiplex|multiplexer|\bWDM\b|interleaver",
    "polarization": r"polarization (?:beam )?splitter|\bPBS\b|\bPSR\b|rotator",
    "phase_shifter": r"thermo-?optic|heater|P_?\\?pi|Ppi|Pπ",
    "photodetector": r"photodetector|photodiode|responsivity|dark current",
    "laser": r"\blaser\b.*(?:output power|threshold|linewidth|SMSR)|\bDFB\b|side-mode",
    "amplifier": r"\bSOA\b|optical amplifier|gain",
    "waveguide_loss": r"propagation loss|waveguide loss|dB/cm|dB/m\b",
    "transition": r"transition loss|interlayer|inter-layer|vertical coupler|adiabatic taper",
}
NUM = re.compile(r"\d+(?:\.\d+)?\s*(?:dB|%|A/W|nA|GHz|mW|dB/cm|dB/m)\b|\bQ\w*\s*(?:of|=|~|>)?\s*\d")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--batch-size", type=int, default=10)
    ap.add_argument("--min-hits", type=int, default=1)
    args = ap.parse_args()
    with RunLog("scan_component_candidates", args.dry_run) as log:
        done = {c["source_id"].removeprefix("eo:") for c in read_csv(ROOT / "data" / "components" / "components.csv")}
        papers = {p.paper_id: p for p in eo.papers()}
        rows: list[dict[str, object]] = []
        for pid, p in sorted(papers.items()):
            t = eo.reference_dir(pid) / "text.md"
            if pid in done or not t.exists():
                continue
            text = t.read_text(errors="ignore")
            cut = re.search(r"\n#+\s*References\b|\nReferences\n", text)
            body = text[: cut.start()] if cut else text
            hits: Counter[str] = Counter()
            for cls, pat in CLASSES.items():
                for m in re.finditer(pat, body, re.IGNORECASE):
                    w = body[max(0, m.start() - 200) : m.end() + 200]
                    if NUM.search(w):
                        hits[cls] += 1
            score = sum(min(v, 10) for v in hits.values())
            rows.append(
                {
                    "paper_id": pid,
                    "score": score,
                    "classes": ";".join(f"{k}:{v}" for k, v in hits.most_common()),
                    "access": p.access,
                    "redistribution": p.redistribution,
                    "year": p.year,
                }
            )
            log.event("paper", "scanned", paper_id=pid, score=score)
        rows.sort(key=lambda r: -int(str(r["score"])))
        keep = [r for r in rows if int(str(r["score"])) >= args.min_hits]
        log.info(f"scanned {len(rows)} papers (skipped {len(done)} already distilled); candidates {len(keep)}")
        n_b = max(1, -(-len(keep) // args.batch_size))
        batches: list[list[dict[str, object]]] = [[] for _ in range(n_b)]
        for i, r in enumerate(keep):  # round-robin: each batch gets a spread of scores
            batches[i % n_b].append(r)
        if args.dry_run:
            return 0
        cols = ["paper_id", "score", "classes", "access", "redistribution", "year"]
        write_csv(STAGING / "components" / "backfill_candidates.csv", cols, rows)
        for i, b in enumerate(batches, start=1):
            write_csv(STAGING / "components" / "batches" / f"bf_{i:02d}.csv", cols, b)
        log.info(f"wrote backfill_candidates.csv and {n_b} batch files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
