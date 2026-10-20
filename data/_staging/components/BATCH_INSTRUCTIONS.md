# Component distillation batch contract (DevLog-002, 2026-10-20)

You distill PIC component data from papers into staging rows. Work from the repo root. No emoji. Never invent: empty
means not reported. Do not use git. No network requests of any kind.

## Read first (in order)

1. `.claude/skills/pic-component-distill/SKILL.md` (binding).
2. `data/schema/component_parameters.yaml` (classes, parameters, units, conventions) and
   `data/schema/components.schema.yaml` (columns, enums, rules).
3. `DevLog/DevLog-002-p1-component-atlas.md` (decisions D30-D40).

## Your batch

The task message names your batch directory `data/_staging/components/<batch>/` and its papers. For each paper the
text is `../eo-modulator-atlas/references/<paper_id>/text.md` (page markers `<!-- page N -->`) with figure renders in
`.../figures/page_NN.png` (read-only). The EO device rows are in `../eo-modulator-atlas/data/devices.csv`. Process one
paper completely before the next.

## Output (only inside your batch directory)

- `components.csv` and `component_metrics.csv`: header exactly as `data/components/*.csv` (copy the header line).
- Validate with `uv run python scripts/merge_component_staging.py data/_staging/components/<batch> --dry-run` until 0
  errors. Never run it without `--dry-run`; the coordinator merges.
- Final message (the coordinator saves it as the batch report): per paper, components and metric rows written,
  values deliberately not entered (cited from prior work, already in the EO device row, unreadable figure), fab
  organizations missing from the registry (name as printed + locator), judgment calls, and any registry gap
  (missing parameter, class or enum value) with a proposed definition. Do not write report files.

## Boundaries

Write only in your batch directory. Never edit `data/components/`, `data/registry/`, `data/schema/`, scripts, the
skill, or any sibling repo. Never copy e-mail addresses, figures or more than a few words of text from a source.
