#!/bin/zsh
# Daily literature retrieval runbook (DevLog-006 S7, D141-D146). Run in tmux: zsh scripts/lit_daily.sh <day>
# Order: arXiv + repository PDFs, 3 Optica browser sessions, 1 publisher browser session, then extraction, inbox
# ingest, `lit` source registration and validation. The IEEE session needs the user's institutional login and is
# printed at the end (one login per session of <= 30 papers). Every fetcher is resumable and skips cached papers;
# a breaker file in logs/ (.lit_blocked_* / .lit_browser_blocked_*) stops that host until it is reviewed.
set -u
DAY=${1:?usage: zsh scripts/lit_daily.sh <day 1-10>}
cd "${0:A:h}/.." || exit 1
LOG=logs/lit_daily_day${DAY}_$(date +%Y%m%dT%H%M%S).log
mkdir -p logs
{
  echo "== day $DAY start $(date -u +%FT%TZ)"
  uv run python scripts/lit_fetch_oa.py --day "$DAY"
  for S in $(uv run python -I -c "
import csv
s = sorted({int(r['session']) for r in csv.DictReader(open('data/_staging/literature/retrieval_queue.csv'))
            if r['day'] == '$DAY' and r['route'] == 'optica_browser' and r['session']})
print(' '.join(map(str, s)))"); do
    uv run python scripts/lit_fetch_browser.py --site optica --run --day "$DAY" --session "$S" --browser chromium
  done
  uv run python scripts/lit_fetch_browser.py --site publisher --run --day "$DAY" --browser chromium
  uv run python scripts/lit_ingest_inbox.py
  uv run python scripts/lit_extract.py --pending
  uv run python scripts/lit_register_sources.py
  uv run python scripts/validate_db.py
  echo "== day $DAY automated part done $(date -u +%FT%TZ)"
  echo "IEEE (needs your login):"
  echo "  uv run python scripts/lit_fetch_browser.py --site ieee --login"
  echo "  uv run python scripts/lit_fetch_browser.py --site ieee --run --day $DAY"
  echo "  uv run python scripts/lit_extract.py --pending && uv run python scripts/lit_register_sources.py"
} 2>&1 | tee "$LOG"
