"""Regenerate the manual-download list from the retrieval queue and the fetch status log (DevLog-006 S7, D147).

Rows: queue route `manual`; `publisher_browser` rows on hosts that answer 403 / WAF to the browser (Wiley, AIP,
De Gruyter, D147); and every other paper whose latest fetch attempt ended blocked / no_access / not_pdf /
no_ieee_copy. Papers already cached (`references/<id>/source.pdf`) are left out.

    uv run python scripts/lit_manual_list.py [--dry-run]
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data/_staging/literature/retrieval_queue.csv"
CACHE_LIST = ROOT / "data/_staging/literature/cache_list.csv"
STATUS = ROOT / "logs/lit_fetch_status.jsonl"
OUT = ROOT / "data/_staging/literature/manual_downloads.md"
D147_PREFIXES = {"10.1002": "Wiley", "10.1063": "AIP", "10.1515": "De Gruyter"}
FAILED = {"blocked", "no_access", "not_pdf", "no_ieee_copy"}


def latest_status() -> dict[str, dict[str, str]]:
    last: dict[str, dict[str, str]] = {}
    if STATUS.exists():
        for line in STATUS.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                last[r["paper_id"]] = r
    return last


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    status = latest_status()
    meta = {r["paper_id"]: r for r in csv.DictReader(CACHE_LIST.open())}
    rows = []
    for r in csv.DictReader(QUEUE.open()):
        pid = r["paper_id"]
        if (ROOT / "references" / pid / "source.pdf").exists():
            continue
        st = status.get(pid, {})
        prefix = r["doi"].split("/")[0]
        if r["route"] == "manual":
            reason = "paywalled, no institutional route"
        elif r["route"] == "publisher_browser" and prefix in D147_PREFIXES:
            reason = f"{D147_PREFIXES[prefix]} blocks the browser (D147)"
        elif st.get("status") in FAILED:
            reason = f"{r['route']}: {st['status']} on {st['ts'][:10]}"
        else:
            continue
        rows.append((int(r["day"]), r["primary_class"], pid, r, reason))
    rows.sort(key=lambda t: (t[0], t[1], t[2]))
    lines = [
        "# Manual downloads (DevLog-006 S7)",
        "",
        f"Generated {date.today().isoformat()} by `scripts/lit_manual_list.py` from `retrieval_queue.csv` and"
        " `logs/lit_fetch_status.jsonl`; papers already cached are left out. Save each PDF as"
        " `references/_inbox/<save_as>` (supplement: `<paper_id>_supplement.pdf`), then run"
        " `uv run python scripts/lit_ingest_inbox.py`.",
        "",
        f"Total: {len(rows)}",
        "",
        "| # | day | class | save_as | year | venue | title | doi | reason |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for i, (day, cls, pid, r, reason) in enumerate(rows, 1):
        m = meta.get(pid, {})
        title = r["title"].replace("|", "/")
        venue = m.get("venue", "").replace("|", "/")
        lines.append(
            f"| {i} | {day} | {cls} | {pid}.pdf | {m.get('year', '')} | {venue} | {title} | {r['doi']} | {reason} |"
        )
    by_reason: dict[str, int] = {}
    for *_, reason in rows:
        key = reason.split(" on ")[0]
        by_reason[key] = by_reason.get(key, 0) + 1
    print(f"{len(rows)} rows: " + "; ".join(f"{k} {v}" for k, v in sorted(by_reason.items())))
    if not args.dry_run:
        OUT.write_text("\n".join(lines) + "\n")
        print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
