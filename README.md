# Photonics Atlas

A shared, traceable registry of organizations, org events and source documents for integrated photonics, and the
atlases built on it:

- **PIC components** (couplers, splitters, resonators, WDM as its own category, lasers, detectors, ...), per-class specs;
- **supply chain / vendors** (wafers, foundries, lasers, fiber and connectors, packaging materials and tools, test
  instruments, reliability standards);
- **people / affiliations / career moves** (absorbs the photonics lineage graph).

All of it is one SvelteKit static app, live at https://outside5sigma.com/photonics-atlas/ (GitHub Pages, built by
`.github/workflows/deploy.yml` on every push to `main`). The [EO modulator atlas](https://github.com/jwt625/eo-modulator-atlas) and the
[advanced packaging atlas](https://github.com/jwt625/advanced-packaging-atlas) stay canonical for their own tables;
this repo reads them through read-only adapters and maps their organizations into the shared registry.

## Current state (2026-10-20)

- P0 foundation done ([DevLog-001](DevLog/DevLog-001-p0-foundation.md)): shared registry of organizations (aliases,
  parents, ROR / Wikidata ids), org events (acquisitions, renames, spin-offs, mergers, with sources and locators) and
  source documents (`eo:`, `pk:`, `ofc2026:`, `blog:`, `lin:`, `web:`); generated crosswalk mapping every EO / packaging
  org, lineage org id and OFC 2026 affiliation string (99.8 % of author rows) to registry orgs.
- P1 component atlas ([DevLog-002](DevLog/DevLog-002-p1-component-atlas.md)): per-class parameter registry (20
  classes incl. WDM), long-format `data/components/component_metrics.csv` (554 components, 1791 values on 2026-10-20);
  back-filled from the EO atlas papers, packaging-atlas papers and OFC 2026 component papers (facts only), every batch
  audited. Corrections are replayable per batch: `patch.yaml` (audit), `sweep.yaml` (conventions), `gapfill.yaml`
  (registry additions) and later audit addenda (`addendum.yaml`), applied in that order with
  `scripts/patch_component_staging.py`, then
  `scripts/merge_component_staging.py --replace`.
- P2 supply chain foundation ([DevLog-003](DevLog/DevLog-003-p2-supply-chain.md)): category tree A-K,
  `data/supply/` (foundry / facility / wafer usage from EO papers, foundry processes, standards, reliability tests from
  the packaging atlas); products and datasheet specs not started.
- P3 people foundation ([DevLog-004](DevLog/DevLog-004-p3-people.md)): person registry, ID crosswalk and dated
  affiliation observations (`data/people/`, grade A paper-printed, B conference metadata); review queue and derived
  transitions stay local (git-ignored `data/_local/`), never published.
- App (`app/`): dashboard, organizations, components. Not yet: supply-chain and people views, org hub page.

## Data conventions

Schema and binding rules: [data/schema/registry.schema.yaml](data/schema/registry.schema.yaml). In short: empty cell =
not stated by any source; renames, spin-offs, acquisitions and mergers are events between separate organizations,
never aliases; printed strings map by normalized name, curated alias or exact ROR name match (no fuzzy matching);
ISO dates (`YYYY`, `YYYY-MM`, `YYYY-MM-DD`); evidence grades A-D, X. Non-open-access corpora (OFC 2026, packaging
atlas papers) contribute facts and locators only; no PDF or text from them is stored here.

## Workflow

Python 3.12 with [uv](https://docs.astral.sh/uv/):

```sh
uv sync --extra dev
uv run python scripts/validate_db.py
uv run pytest -q
uv run ruff check . && uv run mypy
```

Building the registry needs the input repos next to this one (paths in `config/inputs.yaml`, relative to the parent
directory; override with `PHOTONICS_ATLAS_INPUTS_ROOT`) and the pinned ROR data dump (CC0; version in
`config/inputs.yaml`, Zenodo record 23500708) unpacked in `cache/ror/`. Writers support `--dry-run` and write
timestamped logs plus JSONL progress to `logs/`. The registry is curated data, not a from-scratch build: every hand
decision lives in a config file (`config/org_seed_overrides.yaml`, `config/org_curation_overrides.yaml`,
`config/event_participant_map.yaml`, `config/registry_corrections.yaml`). Run in this order:

| step | script | writes |
|---|---|---|
| 1 | `seed_org_registry.py` | appends new EO / packaging / lineage orgs and aliases (existing rows untouched) |
| 2 | `add_ror_orgs.py` | appends orgs/aliases resolved through ROR; writes the unmapped OFC strings to `data/_staging/org_curation/unmapped_<run>.csv` |
| 3 | `merge_org_curation.py` | appends reviewed curation decisions (`data/_staging/org_curation/batch_*/decisions.csv`); regenerates `skipped.csv` |
| 4 | `build_sources.py` | regenerates the eo/pk/ofc2026/blog/lin rows of `sources.csv`; keeps rows of other corpora (web, ds) |
| 5 | `merge_org_events.py` | regenerates `org_events.csv` / participants from lineage + staged research (hand-added event ids are kept), appends orgs it needs, replaces the web rows of `sources.csv` (cited sources only); needs step 4 |
| 6 | `apply_registry_corrections.py` | applies `config/registry_corrections.yaml` in place (idempotent) |
| 7 | `build_org_crosswalk.py` | regenerates `data/crosswalk/org_crosswalk.csv`; exit 1 when the P0 acceptance fails |
| 8 | `build_views.py` | regenerates `app/static/data/registry.json` and `components.json` (committed; the Pages build serves them) |

Atlas tranches on top of the registry (each validated by `validate_db.py` through its schema file and rules module):

| script | writes |
|---|---|
| `scan_component_candidates.py`, `scan_ofc_candidates.py` | candidate lists and batch files in `data/_staging/components/` |
| `merge_component_staging.py <batch>` | appends a validated distillation batch to `data/components/` (`--replace` for patched batches) |
| `patch_component_staging.py <batch> <patch.yaml>` | applies coordinator / audit corrections to a staging batch (idempotent) |
| `build_supply_seed.py` | append-only supply tables in `data/supply/` from EO papers and packaging metrics (`data/supply/curation.yaml`) |
| `build_people.py`, then `derive_transitions.py` | people tables in `data/people/`; review queue and transitions in git-ignored `data/_local/people/` |

`validate_db.py` (reader) checks everything against the schema.

App (Node 22+, pnpm):

```sh
cd app
pnpm install
pnpm dev        # or: pnpm check && pnpm test && pnpm build
```

## Rights

Registry data: facts with source locators. ROR data is CC0. Source documents keep their own rights; see `access`,
`license` and `redistribution` in `sources.csv`.
