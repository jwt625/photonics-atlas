"""Write lit header batches (papers.csv) for every paper of a batch plan, split into near-equal batches of <= 30.

Usage (repo root): uv run python .claude/skills/pic-component-distill/scripts/write_header_batches.py <batches.json>
<first hNN> [<more batches.json> ...]. Also prints the `lit:` id list for scan_vendor_models.py --only.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "scripts"))
import ofc_headers as oh  # noqa: E402

plan = json.load(open(sys.argv[1]))
first = int(sys.argv[2])
for extra in sys.argv[3:]:
    plan.update(json.load(open(extra)))
ids = [c for v in plan.values() for c in v]
taken = {r["code"] for d in oh.batch_dirs(oh.LIT) for r in oh.read_csv(d / "papers.csv")}
assert not (set(ids) & taken), set(ids) & taken
meta = oh.lit_papers()
n = -(-len(ids) // 30)
size = -(-len(ids) // n)
for k in range(n):
    name = f"lit_h{first + k}"
    codes = ids[k * size : (k + 1) * size]
    d = oh.LIT_BASE / name
    assert not d.exists(), d
    rows = [
        {
            "source_id": f"lit:{c}",
            "code": c,
            "n_authors_meta": len(meta[c].authors),
            "local_pdf": (oh.REFS / c / "source.pdf").exists(),
        }
        for c in codes
    ]
    oh.write_csv(d / "papers.csv", oh.PAPER_COLS, rows)
    print(
        name,
        len(rows),
        "authors",
        sum(r["n_authors_meta"] for r in rows),
        "zero-author-meta",
        [r["code"] for r in rows if not r["n_authors_meta"]],
    )
print("VENDOR_ONLY=" + ",".join("lit:" + c for c in ids))
