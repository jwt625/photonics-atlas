#!/bin/zsh
# Unattended open-access night run (owner away 2026-11-26..28, DevLog-020 stage 3). Runs inside tmux, started by a
# launchd agent at 22:03 through a launcher outside ~/Documents (launchd has no access to ~/Documents; the running
# tmux server does). Usage: night_oa_session.sh run|test. Interactive claude (background notifications need a live
# session, not -p); the shell stays open afterwards for inspection.
set -u
ROOT="${0:A:h:h}"
cd "$ROOT" || exit 1
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
TS=$(date +%Y%m%dT%H%M%S)
if [[ "${1:-}" == test ]]; then
  PROMPT="Timer test: run the bash command 'date' and write its output to logs/night_oa_test_$TS.txt, then stop. Do nothing else."
else
  PROMPT="Unattended night run, the owner is away and cannot answer. Read .claude/skills/pic-component-distill/SKILL.md and daily-run.md, then run tonight's caching and ingestion exactly as the section 'Unattended open-access night' of daily-run.md says (open-access routes only: arXiv, open-access publishers, Optica OA journals; no IEEE, no publisher browser; at most about 50 papers), then commit and push. Last step after the push: rm logs/.night_oa_active."
fi
SL="logs/night_oa_session_$TS.log"
# one coordinator at a time: wait while another run's lock is younger than 20 h (the run removes it after its push)
LOCK=logs/.night_oa_active
while [[ "${1:-}" != test && -f $LOCK ]] && (( $(date +%s) - $(stat -f %m $LOCK) < 72000 )); do
  echo "$(date +%Y%m%dT%H%M%S) waiting for lock $(cat $LOCK)" >> "$SL"; sleep 600
done
[[ "${1:-}" != test ]] && echo "$TS" > $LOCK
echo "$TS start mode=${1:-run}" >> "$SL"
claude --permission-mode auto -n "lit_night_$TS" "$PROMPT"
rc=$?
echo "$(date +%Y%m%dT%H%M%S) claude exit $rc" >> "$SL"
exec zsh
