"""Slow overnight Optica OA-journal fetch (owner 2026-11-24: "keep your optica session running, and slowly cache them
overnight"). One paper per browser launch, 4-6 min apart; Optica's rate-limit page -> 30 min back-off and the same
paper again; any other non-ok row (standalone case) is logged and skipped; stops when every paper is saved or after
MAX_RL rate limits in a row. A breaker file the fetcher arms is moved aside (no breakers, owner 2026-11-20).
Run from the repo root in tmux: uv run python .claude/skills/pic-component-distill/scripts/optica_overnight.py <day>[,<day>...]
"""

import csv
import datetime as dt
import json
import random
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path.cwd()
DAYS = sys.argv[1].split(",")
LOGS = ROOT / "logs"
STATUS = LOGS / "lit_fetch_status.jsonl"
BREAKER = LOGS / ".lit_browser_blocked_optica.json"
STAMP = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
LOG = LOGS / f"lit_optica_overnight_d{'-'.join(DAYS)}_{STAMP}.log"
OA_RE = re.compile(r"10\.1364/(oe|opex|optica|ome)\.")
GAP_S = (240, 360)
RL_WAIT_S = 1800
MAX_RL = 8


def log(msg: str) -> None:
    line = f"{dt.datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with LOG.open("a") as f:
        f.write(line + "\n")


def todo() -> list[str]:
    rows = csv.DictReader((ROOT / "data/_staging/literature/retrieval_queue.csv").open(encoding="utf-8"))
    by_day = {d: [] for d in DAYS}
    for r in rows:
        if (
            r["day"] in by_day
            and r["route"] == "optica_browser"
            and OA_RE.match(r["doi"].lower())
            and not (ROOT / "references" / r["paper_id"] / "source.pdf").exists()
        ):
            by_day[r["day"]].append(r["paper_id"])
    return [p for d in DAYS for p in by_day[d]]


def clear_breaker() -> None:
    if BREAKER.exists():
        dest = LOGS / f"lit_browser_blocked_optica_cleared_{dt.datetime.now():%Y%m%dT%H%M%S}.json"
        BREAKER.rename(dest)
        log(f"fetcher breaker moved aside: {dest.name}")


def is_rate_limit(pid: str) -> bool:
    snaps = sorted(LOGS.glob(f"lit_browser_optica_{pid}_*.html"))
    if not snaps:
        return False
    return bool(re.search(r"downloading timeout|heavy usage", snaps[-1].read_text(errors="replace"), re.I))


def fetch_one(pid: str) -> str:
    offset = STATUS.stat().st_size
    with (LOGS / f"lit_optica_overnight_fetch_{STAMP}.log").open("a") as fl:
        subprocess.run(
            ["uv", "run", "python", "scripts/lit_fetch_browser.py", "--site", "optica", "--run", "--paper-ids", pid,
             "--max", "1"],
            cwd=ROOT, stdout=fl, stderr=subprocess.STDOUT, check=False, timeout=900,
        )
    status = "none"
    with STATUS.open("rb") as f:
        f.seek(offset)
        for raw in f.read().decode("utf-8", "replace").splitlines():
            try:
                d = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if d.get("paper_id") == pid and d.get("route") == "optica_browser":
                status = str(d.get("status"))
    return status


def main() -> int:
    clear_breaker()
    queue = todo()
    log(f"{len(queue)} papers: {','.join(queue)}")
    skipped: list[tuple[str, str]] = []
    rl_run = 0
    saved = 0
    i = 0
    while i < len(queue):
        pid = queue[i]
        st = fetch_one(pid)
        clear_breaker()
        if st == "ok":
            saved += 1
            rl_run = 0
            log(f"ok {pid} ({saved} saved, {len(queue) - i - 1} left)")
            i += 1
        elif is_rate_limit(pid):
            rl_run += 1
            log(f"RATE_LIMIT on {pid} ({rl_run} in a row); waiting {RL_WAIT_S // 60} min")
            if rl_run >= MAX_RL:
                log(f"stopping: {MAX_RL} rate limits in a row")
                break
            time.sleep(RL_WAIT_S)
            continue
        else:
            skipped.append((pid, st))
            log(f"standalone {st} on {pid}: skipped (snapshot logs/lit_browser_optica_{pid}_*.html)")
            i += 1
        if i < len(queue):
            time.sleep(random.uniform(*GAP_S))
    log(f"done: saved {saved}, skipped {skipped}, not attempted {queue[i:] if i < len(queue) else []}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
