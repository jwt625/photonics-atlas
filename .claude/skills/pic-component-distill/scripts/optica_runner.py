"""Optica OA-journal runner for one queue day (OE / Optica / OME DOIs only). Probe 3, chunk 11, 15 min pause, rest.

Kills the fetcher at the first status row that is not `ok` (no_access / challenge / error / not_pdf / ...) and stops
with the paper, status and newest page snapshot in the log. No breaker file (owner 2026-11-20): the coordinator
checks the snapshot by hand. Optica's rate-limit page ("downloading timeout based on heavy usage") is named in the
log as RATE_LIMIT; anything else is checked as a possible standalone case. A breaker the fetcher itself arms is moved
aside to logs/lit_browser_blocked_optica_cleared_<stamp>.json.
Run from the repo root in tmux: uv run python .claude/skills/pic-component-distill/scripts/optica_runner.py <day>
"""

import csv
import datetime as dt
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path.cwd()
DAY = sys.argv[1]
LOGS = ROOT / "logs"
STATUS = LOGS / "lit_fetch_status.jsonl"
BREAKER = LOGS / ".lit_browser_blocked_optica.json"
STAMP = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
LOG = LOGS / f"lit_optica_oa_d{DAY}_{STAMP}.log"

_IDS = [
    r["paper_id"]
    for r in csv.DictReader((ROOT / "data/_staging/literature/retrieval_queue.csv").open())
    if r["day"] == DAY
    and r["route"] == "optica_browser"
    and re.match(r"10\.1364/(oe|optica|ome)\.", r["doi"].lower())
    and not (ROOT / "references" / r["paper_id"] / "source.pdf").exists()  # relaunch: saved papers skipped
]
CHUNKS = [("probe", _IDS[:3]), ("daily", _IDS[3:14]), ("daily", _IDS[14:])]
CHUNKS = [c for c in CHUNKS if c[1]]
PAUSE_AFTER = {1: 900}  # seconds, after chunk index


def log(msg: str) -> None:
    line = f"{dt.datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with LOG.open("a") as f:
        f.write(line + "\n")


def new_rows(offset: int, ids: set[str]) -> list[dict]:
    with STATUS.open("rb") as f:
        f.seek(offset)
        out = []
        for raw in f.read().decode("utf-8", "replace").splitlines():
            try:
                d = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if d.get("paper_id") in ids and d.get("route") == "optica_browser":
                out.append(d)
        return out


def clear_breaker() -> None:
    if BREAKER.exists():
        dest = LOGS / f"lit_browser_blocked_optica_cleared_{dt.datetime.now():%Y%m%dT%H%M%S}.json"
        BREAKER.rename(dest)
        log(f"fetcher breaker moved aside: {dest.name}")


def explain(pid: str) -> str:
    snaps = sorted(LOGS.glob(f"lit_browser_optica_{pid}_*.html"))
    if not snaps:
        return "no snapshot"
    text = snaps[-1].read_text(encoding="utf-8", errors="replace")
    kind = "RATE_LIMIT" if re.search(r"downloading timeout|heavy usage", text, re.I) else "CHECK"
    return f"{kind} snapshot {snaps[-1].name}"


def main() -> int:
    clear_breaker()
    for i, (kind, ids) in enumerate(CHUNKS):
        log(f"chunk {i} ({kind}): {','.join(ids)}")
        offset = STATUS.stat().st_size
        fetch_log = LOGS / f"lit_optica_oa_d{DAY}_fetch_chunk{i}_{STAMP}.log"
        with fetch_log.open("w") as fl:
            proc = subprocess.Popen(
                [
                    "uv",
                    "run",
                    "python",
                    "scripts/lit_fetch_browser.py",
                    "--site",
                    "optica",
                    "--run",
                    "--paper-ids",
                    ",".join(ids),
                    "--max",
                    str(len(ids)),
                ],
                cwd=ROOT,
                stdout=fl,
                stderr=subprocess.STDOUT,
            )
            bad = None
            while proc.poll() is None:
                time.sleep(5)
                bad = next((r for r in new_rows(offset, set(ids)) if r.get("status") != "ok"), None)
                if bad:
                    proc.terminate()
                    try:
                        proc.wait(30)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                    break
        rows = new_rows(offset, set(ids))
        bad = bad or next((r for r in rows if r.get("status") != "ok"), None)
        saved = [r["paper_id"] for r in rows if r.get("status") == "ok"]
        log(
            f"chunk {i} rc={proc.returncode} saved={len(saved)} {saved} other={[(r['paper_id'], r['status']) for r in rows if r.get('status') != 'ok']}"
        )
        clear_breaker()
        if bad:
            log(f"stopped on non-ok row: {bad['paper_id']} {bad['status']} {explain(bad['paper_id'])}")
            return 1
        if not saved:
            log("chunk saved 0; stopping")
            return 1
        if i in PAUSE_AFTER and i + 1 < len(CHUNKS):
            log(f"pause {PAUSE_AFTER[i]}s")
            time.sleep(PAUSE_AFTER[i])
    log("round done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
