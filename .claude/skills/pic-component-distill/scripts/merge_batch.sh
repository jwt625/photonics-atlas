#!/bin/zsh
# usage: merge_batch.sh <batch>   (run from repo root) patch, re-run, dry-run, merge; log under logs/
B=$1; TS=$(date +%Y%m%dT%H%M%S); L=logs/lit_merge_${B}_$TS.log
{ uv run --offline python scripts/patch_component_staging.py data/_staging/components/$B data/_staging/components/$B/patch.yaml
  uv run --offline python scripts/patch_component_staging.py data/_staging/components/$B data/_staging/components/$B/patch.yaml
  uv run --offline python scripts/merge_component_staging.py data/_staging/components/$B --dry-run || exit 1
  uv run --offline python scripts/merge_component_staging.py data/_staging/components/$B; } > $L 2>&1
echo "log $L"; grep -E "changes|batch $B|merged|ERROR|error" $L | tail -6
