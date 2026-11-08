# DevLog-014: Foundry PDK benchmark table

| | |
|---|---|
| Date | 2026-11-07 |
| Status | In progress |
| Scope | `config/benchmark.yaml`, `scripts/build_benchmark.py`, `app/static/data/benchmark.json`, `app/src/lib/benchmark/`, `app/src/routes/benchmark/`, `app/scripts/build-benchmark-html.mjs`, standalone `app/static/pdk-benchmark.html`. Reads `data/components/`, `data/registry/`, `data/crosswalk/` and the EO modulator atlas (read-only); edits none of them |
| Decisions | D900-D919 reserved for this DevLog (D5xx is consumed by the daily lit-ingest stream) |

## Request (2026-11-07, Wentao)

1. Inspect component metrics of this repo and the leading foundries with decent data coverage; propose a table like the
   capability-benchmark tables of frontier LLM releases, for foundry PDK building blocks.
2. Make the stylized table, combining the lab styles (row-best and second-best emphasis, highlighted leading column,
   grey sub-labels, footnotes) with the local UI rules (dark default, sharp corners, dense, details on hover).
3. Deliver as a standalone HTML and as a benchmark tab in the app.

Answers to the clarifying questions (2026-11-07):

| question | answer |
|---|---|
| Column unit | foundry x platform family (SiPh, SiN, TFLN, InP), grouped under family headers |
| Cell value | best measured value; n and source on hover; row best and second best emphasised |
| Modulators | include, from the EO modulator atlas (read-only) |
| AMF vs A*STAR IME | merge into one column "AMF / IME"; the tooltip names the org of each value |

## Coverage found (2026-11-07, measured + figure-read values, fabricated components)

Foundries by measured values (all classes): imec 1630, CEA-Leti 621, A*STAR IME 669, AMF 498, Applied Nanotools 752,
AIM Photonics 433, GlobalFoundries 353, LIGENTEC 237, TSMC 74, Samsung (SiPh platform) 11 components, Sandia 271.
No vendor PDK spec sheets exist in the repo (`data/supply/product_specs.csv` has no rows): every cell is a
literature-measured value on a device made in that foundry's process, not a PDK guarantee.

## Decisions

| id | decision | reason |
|---|---|---|
| D900 | Columns = (foundry, platform family). Family from `components.platform` (SiPh: soi, soi_rib, soi_strip, soi_slot, si_sin_multilayer; SiN: sin; TFLN: lnoi_*; InP: inp) and, for EO rows, from `waveguide_platform` or else `eo_material`. AMF and A*STAR IME share one column (answer 4). Candidate foundries are listed in `config/benchmark.yaml`; universities and brokers (CMC) are not columns. A column is shown when it fills at least `min_rows_per_column` rows | answer 1; the registry keeps AMF and IME separate, only the view merges |
| D901 | Cell = best value among rows that pass the row's filters: basis measured, extracted_from_figure or derived (author_estimate rests on an assumed input, D44 / D403, and is excluded with simulated, design_target, specification); row_kind fabricated (EO: device); statistic std never; a bound pointing the wrong way for the ranking (gt on lower-is-better, lt on higher-is-better) never; ranges rank at their favourable end, the full range on hover (superseded by D908); cryogenic rows (T < 250 K, EO temperature_class cryogenic) never | "best measured" (answer 2) without counting bounds or design numbers as achieved |
| D902 | Rows are fixed in config with class(es), parameter, direction, allowed scopes, wavelength window and platform exclusions; a row is shown when at least `min_columns_per_row` columns fill it. Telecom window 1260-1630 nm from `wavelength_nm` or `band`; rows say whether a value with no stated wavelength is kept | per-facet vs fiber-to-fiber and visible vs telecom are different quantities (D503a) |
| D903 | EO rows take the platform's native effect only (SiPh: silicon plasma dispersion, Ge-Si EAM; TFLN: lithium niobate; InP: InP MQW). Polymer-slot, BTO and bonded hybrid modulators on a foundry wafer are not PDK cells of that foundry and are left out | otherwise the AMF / IME SiPh VpiL would be an EO-polymer slot device |
| D904 | Emphasis: row best = bold + accent-tinted cell; second best = underline (open-weight-release convention); leading column (most row bests) = tinted column band and a marker in its header, computed, never chosen. Ranking across all shown columns by default, toggle to rank within each platform family. Ties share the rank | request 2 |
| D905 | One renderer (`app/src/lib/benchmark/render.js`, plain JS with JSDoc types) and one stylesheet serve both the app tab and the standalone file, so they cannot drift. The standalone embeds the data, the renderer, the CSS and a minimal tooltip; no network requests | request 3 |
| D906 | `photodetector.ge_waveguide` rows with an empty `platform` are SiPh (their core_material reads Ge-on-Si / Ge on a Si pedestal with Si feed): Sandia and AIM Ge PDs | 36 Ge PD values were dropped as platform-less |
| D908 | (owner 2026-11-07) A range (spread over dies, channels or a band) is shown as `low-high` and ranked at its midpoint, within a column and across columns | answer to the D907 open question; the favourable end rewarded the widest spread |
| D909 | (owner 2026-11-07) `pinned_columns` are always shown, filled or not: Tower SiPh, GlobalFoundries SiPh, TSMC SiPh. A dash in a pinned column reads as a coverage gap of the atlas | leading production foundries; Tower was invisible below the 3-row threshold |
| D910 | (owner 2026-11-07) `private_values` in the config: unpublished values from private communication to the owner, source not named, dated; basis `private_communication`, marked with a dagger and explained in the tooltip and notes, ranked like any value, last in the basis tie-break. First entries: Tower SiPh edge coupler ~0.6 dB per facet; Tower SiPh MZM EO bandwidth ~100 GHz | owner instruction; kept out of the data tables, which hold published values only |
| D911 | (owner 2026-11-07) CUMEC Ge PD: the text value > 0.8 A/W is used; the figure readings 1.2 A/W (1540 nm, 97 percent of the quantum limit) and 0.85 A/W are excluded from the benchmark | prefer the authors' stated value over a figure reading that conflicts with it |
| D912 | (owner 2026-11-07) `lit:munk2019` fab_org_ids = org_tower_semiconductor (Tower-Jazz, former name; p.4 Sec. III-A names the foundry). Applied as staging batch `fix_bench_munk2019` (copy of the 3 components + 21 metrics, `patch.yaml`, re-run 0 changes, `merge_component_staging.py --replace`); diff: 3 component rows (fab_org_ids, notes), metrics unchanged. Backup zip of data/components in the session scratchpad | data correction through the batch pipeline, not a hand edit |
| D913 | (owner 2026-11-07) Ingest batch `bench_01`: OFC 2026 M1E.4 (Tower thermo-optic P_pi) and PsiQuantum Nature 2025 (main text + SI; GF fab only where the paper names GF). Distill agent, then a fresh-context audit, then merge. Xiang Nature 2023 deferred: its Tower SiN values are Q-derived (D403 author_estimate) and fill no benchmark cell | research agents' top items (`DevLog/research/2026-11-07-*`) |
| D914 | (coordinator 2026-11-07, after the bench_01 audit) Audit ruling 2 applied: the M1E.4 components keep an empty platform (D423, the paper never names SOI / Si waveguides). The benchmark places them in the SiPh family through `family_override` in the config (the paper states a commercial 300 mm silicon photonics platform, fabricated through TowerJazz); the data rows are not changed | keeps the data rule and the stated family; Tower P_pi 8.8 mW stays in the table |
| D907 | (fresh-context audit 2026-11-07: all 113 cells recomputed independently and matched) Exclusions in `config/benchmark.yaml` `exclude_values` with reasons: de2020 SiGe ring PD (not a waveguide Ge PD), niels2026 MMI (two-MMI loss share), han2023-a VpiL (extrapolated estimate). EO rows drop non-native integration routes (bonded, polymer backfill, transfer printed, 2D, bonded III-V). A metric row with no wavelength or band takes its component's other rows' wavelengths (LIGENTEC 1 um AWG crosstalk left out) | audit findings H1, H2, M1, L-latent |

## Follow-ups (data stream, not edited here)

- Reclassify `cmp_lit_de2020_sige_ring_pd` (class photodetector.other or a resonant-PD subtype); set band on `cmp_lit_cheung2019_gaussian_awg_1x4` crosstalk rows; han2023-a vpi basis in the EO atlas; munk2019 `fab_org_ids` = Tower (process name names Tower-Jazz).
- Resolved 2026-11-07: range ranking (D908), CUMEC Ge PD (D911), munk2019 fab (D912).
- PsiQuantum: source row is arXiv v1 (`lit:alexander2024`; the supplement is not in v1). The Nature version (10.1038/s41586-025-08820-7) and its SI need the publisher_browser route or the manual inbox; the next-generation SiN values (0.0039 dB/cm, crossing 0.0016 dB, edge coupler 0.053 dB per coupler) name no fab and enter no column unless the SI names one. arXiv licence lookup timed out (license empty).
- Registry: alias rows Tower-Jazz / TowerJazz for org_tower_semiconductor (bench_01 audit, munk2019).
- Pre-existing mypy errors in scripts/layouts/cells (awg_fan2025, trans_shang2017, mmi_lu2016a; commit 2803a5e), not from this DevLog.
- Data stream: correct `cmp_wu2025_ge_pd-m3` / `-m4` basis or notes if the audit of that batch agrees (D911 only skips them here). Registry alias "Tower-Jazz" / "TowerJazz" for org_tower_semiconductor.
- Coverage: Tower and GF (PsiQuantum flow) under-ingested; research agents dispatched 2026-11-07 (`DevLog/research/2026-11-07-*-siph-*`).

## TODO

- [x] `config/benchmark.yaml` (rows, families, foundries, thresholds)
- [x] `scripts/build_benchmark.py` -> `app/static/data/benchmark.json` with per-cell provenance and a diagnostics log
- [x] Renderer + CSS, `/benchmark` route, nav tab
- [x] Standalone `app/static/pdk-benchmark.html` from `app/scripts/build-benchmark-html.mjs`
- [x] Tests (`tests/test_benchmark.py`, `app/src/lib/benchmark/render.test.ts`), ruff / mypy, pnpm check / test / build
- [x] Screenshots dark + light, app and standalone (incl. the private-value tooltip)
- [x] D908-D912: midpoint ranking, pinned columns, private values, CUMEC text value, munk2019 fab
- [x] bench_01 ingest (M1E.4, PsiQuantum 2025) -> audit -> merge -> rebuild benchmark; full pytest + validate_db after merge
- [x] Fresh-context audit of cell values against the CSVs

## Progress

- 2026-11-07 Coverage inspection, questions answered, plan written.
- 2026-11-07 First draft: 17 columns (13 SiPh, 4 SiN), 17 rows; app tab /benchmark (dev server port 47731, tmux pa-bench), standalone app/static/pdk-benchmark.html; screenshots dark / light / standalone, no console errors. TFLN / InP columns below threshold.
- 2026-11-07 Audit applied (D907): 17 columns, 16 rows (mzm_vpil hidden: one column left). ruff, mypy, svelte-check clean. vitest, pytest, production build not yet run.
- 2026-11-07 Owner answers (all yes; private values for Tower). D908-D913 applied: Tower SiPh column visible (4 rows:
  propagation 1.8 dB/cm and grating coupler 10 dB from munk2019, edge coupler ~0.6 dB and MZM ~100 GHz private),
  TSMC SiPh pinned (2 rows); 19 columns, 16 rows. pytest test_benchmark 8 passed; vitest 654 passed; svelte-check
  0 errors; pnpm build ok. bench_01 distill agent running.
- 2026-11-07 bench_01: distill (M1E.4 2 components / 3 rows; alexander2024 11 / 17; source lit:alexander2024 added as a
  curator add, arXiv v1) -> fresh-context audit (metrics 16 ok / 4 imprecise / 0 wrong; patch 18 ops, re-run 0) ->
  backup zip -> merged (+13 / +20, 0 errors). D914 family override. Tower SiPh 5 rows (adds thermo-optic P_pi 8.8 mW);
  no GF cell from PsiQuantum (baseline-flow values are cryogenic or not benchmark rows). Cell key `src` renamed
  `source_id` (served-view rule). build_views, validate_db 0 errors, ruff clean, full pytest 371 passed + 1 failed (served-view prefixed id), fixed and re-run (test_views + test_benchmark 21 passed),
  vitest 654, svelte-check 0, pnpm build ok, privacy scan clean.
