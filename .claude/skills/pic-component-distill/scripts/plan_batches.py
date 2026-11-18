"""Plan lit_NN distill batches for one queue day: registered papers grouped by primary_class family, ~48 pages and
<= --max papers (default 8) per batch. Usage (repo root): uv run python <skill>/scripts/plan_batches.py <day> <first NN>
<out.json> [--max=N] [exclude.json ...]. Prints the batch table and writes {batch: [paper ids]}."""

import collections
import csv
import json
import sys

args = [a for a in sys.argv[1:] if not a.startswith("--max=")]
MAXP = int(next((a[6:] for a in sys.argv[1:] if a.startswith("--max=")), "8"))
day, start, out = args[0], int(args[1]), args[2]
exclude = set()
for f in args[3:]:
    exclude |= {c for v in json.load(open(f)).values() for c in v}
q = [r for r in csv.DictReader(open("data/_staging/literature/retrieval_queue.csv")) if r["day"] == day]
src = {r["native_id"] for r in csv.DictReader(open("data/registry/sources.csv")) if r["corpus"] == "lit"}
cl = {r["paper_id"]: r for r in csv.DictReader(open("data/_staging/literature/cache_list.csv"))}
FAM = {
    "amplifier": "A",
    "frequency_converter": "A",
    "nonreciprocal": "A",
    "laser": "B",
    "chip_chip_coupler": "B",
    "micro_optics": "B",
    "free_space_emitter": "B",
    "phase_shifter": "C",
    "photodetector": "C",
    "waveguide_platform": "C",
    "resonator": "D",
    "splitter": "D",
    "mode_converter": "D",
    "reflector": "D",
    "crossing": "E",
    "fiber_chip_coupler": "E",
    "fiber_interface": "E",
    "polarization": "E",
    "wdm": "F",
    "switch_fabric": "F",
}
papers = []
for r in q:
    p = r["paper_id"]
    if p not in src or p in exclude:
        continue
    sj = json.load(open(f"references/{p}/source.json"))
    papers.append((FAM.get(cl[p]["primary_class"], "B"), p, sj.get("pages", 0), cl[p]["primary_class"]))
print(len(papers), sum(x[2] for x in papers))
by = collections.defaultdict(list)
for f, p, n, c in papers:
    by[f].append((p, n, c))
batches = []
for f in sorted(by):
    items = sorted(by[f], key=lambda x: -x[1])
    tot = sum(n for _, n, _ in items)
    k = max(1, round(tot / 48), -(-len(items) // MAXP))
    bins = [[] for _ in range(k)]
    for it in items:
        b = min(bins, key=lambda b: (sum(x[1] for x in b), len(b)))
        b.append(it)
    for b in bins:
        batches.append((f, b))
for i, (f, b) in enumerate(batches):
    print(f"lit_{start + i}", f, len(b), sum(x[1] for x in b), ", ".join(f"{x[0]}({x[1]})" for x in b))
json.dump({f"lit_{start + i}": [x[0] for x in b] for i, (f, b) in enumerate(batches)}, open(out, "w"), indent=1)
