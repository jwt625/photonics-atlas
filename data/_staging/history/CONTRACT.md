# Historical batches `hist_NN`: contract (DevLog-016 D963, D965)

One batch = up to 8 historical papers listed in `data/_staging/history/hist_NN/papers.csv` (columns: paper_id,
source_id, year, era, thread, title, venue, doi, dri, dri_basis, dri_source, significance, component_class,
has_device_metrics). You produce three things per batch. Write only inside `data/_staging/history/hist_NN/` and
`data/_staging/components/hist_NN/`; everything else in the repo is read-only for you. No network.

`mode` in papers.csv: `full` = milestone row + component rows (section 2) + report; `milestone_only` = the paper was
distilled for components in an earlier `lit` batch (its rows are already in `data/components/`), so write only the
milestone row and the report, no component rows.

Pilot lessons (hist_01 audit): when an embedded image `img_pNN_k.png` is a full-page scan, use the page render
`page_NN.png` instead; check `figures.json` before writing that no render exists; when the paper prints the measurement
wavelength (e.g. a He-Ne line), put it in `wavelength_nm` instead of an inferred band; give every loss row a band or
wavelength; `includes` / `excludes` must name every loss term the paper attributes.

## Inputs per paper

- `references/<paper_id>/text.md`: page-delimited text (`<!-- page N -->`). Scanned papers carry OCR text
  (`extraction_method` in the header says so): superscripts, subscripts, Greek letters and equations are unreliable
  (e.g. "10-3" for 10^-3); read every number you enter from the page render, not from the OCR line.
- `references/<paper_id>/figures/`: `figures.json` (page renders with detected captions, embedded images),
  `page_NN.png` (150 dpi page renders; for scans every page), `img_pNN_k.png` (embedded images).
- `data/_staging/literature/history_candidates.csv`: the selection record (significance, evidence_url, notes with
  priority disputes). Use it as a pointer only: every value you write comes from the paper itself.

## 1. Milestone row (`hist_NN/milestones.csv`, one row per paper)

| column | rule |
|---|---|
| paper_id, source_id | as in papers.csv |
| date | publication date as printed in the paper (YYYY-MM-DD, YYYY-MM or YYYY); received / accepted dates go to notes; empty if the paper prints none (then the year in papers.csv is used downstream) |
| era, thread | copy from papers.csv |
| event | <= 25 words: what this paper reports, in the paper's own terms. "first" only when the paper itself claims it (quote the claim's page in `event_locator`); no superlatives the paper does not make |
| event_locator | page(s) supporting the event, e.g. `p.1 abstract; p.3` |
| dri | the person(s) credited with the result. Start from papers.csv `dri`; confirm against the byline, footnotes, acknowledgments, "work done by / suggested by" statements. Change it only with evidence from the paper (put the old value and the reason in notes). Empty when papers.csv says unresolved and the paper does not settle it |
| dri_locator | page of the evidence (byline counts for single-author papers) |
| orgs_printed | affiliations exactly as printed in the paper, `;` separated, in byline order (no registry ids; header extraction maps them later) |
| key_figure_label | the paper's own label of the one figure that best shows the result (e.g. `Fig. 2`): the device / experiment the paper is remembered for, or the key measured curve. Prefer the figure the abstract or conclusion relies on. Empty if the paper has no figure (say so in notes) |
| key_figure_page | page number of that figure |
| key_figure_file | an existing file under `references/<paper_id>/figures/` that shows that figure: the embedded image `img_pNN_k.png` when it is the figure itself, else the page render `page_NN.png`. Open that image once to confirm it shows the figure (this is the one case where you view an image) |
| key_figure_caption | <= 30 words, paraphrase of the printed caption (not a copy) |
| key_figure_reason | <= 15 words: why this figure |
| notes | received date, DRI changes, OCR problems, anything a reviewer must know |

## 2. Component and metric rows (`data/components/` staging)

Only when the paper reports a measured (or derived from measured) value of a device in the component taxonomy
(`data/schema/component_parameters.yaml`): follow the `pic-component-distill` skill (`.claude/skills/pic-component-
distill/SKILL.md`) exactly, writing `data/_staging/components/hist_NN/components.csv` and `component_metrics.csv`, and
validate with `uv run --offline python scripts/merge_component_staging.py data/_staging/components/hist_NN --dry-run`
until 0 errors. Historic specifics: values in the units printed, converted to the registry unit as `derived` with the
formula in notes (e.g. dB/km to dB/cm); theory-only papers, proposals and reviews get no component rows; a demonstration
whose only number is a threshold or output power of a bulk / gas laser is out of the component taxonomy (say so in the
report). Do not create rows for fibers (not a component class) unless the skill's classes cover the device.

## 3. Report (`hist_NN/report.txt`; subagents cannot write .md files here)

Per paper: milestone written (yes / no and why), key figure chosen (or why none), component rows entered (ids) and
what was not entered and why, OCR or identity problems (wrong PDF, missing pages, supplement needed).

## Rules

- Never invent: empty = not stated. No memory, no other paper, no review.
- No emoji. ISO dates. ASCII-safe CSV (UTF-8), comma separated, quoted where needed.
- Run Python as `uv run --offline`; helper scripts in a scratchpad subfolder named after your batch.
- Validate the milestone file with `uv run --offline python scripts/hist_merge_milestones.py data/_staging/history/hist_NN --dry-run` until it reports 0 errors.
