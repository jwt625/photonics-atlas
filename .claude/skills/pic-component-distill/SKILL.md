---
name: pic-component-distill
description: Distill photonic integrated circuit component data (couplers, splitters, resonators, WDM filters, reflectors, polarization devices, phase shifters, photodetectors, lasers, amplifiers, isolators, waveguide loss and inter-layer transitions) from a paper into component rows and long-format metric rows with conditions, scope, basis and locator. Use when adding or auditing component data in this repo.
---

# PIC component distillation

Input: one source already in the registry (`data/registry/sources.csv`, e.g. `eo:<paper_id>`) and its cached text.
Output: rows for `components.csv` and `component_metrics.csv` (staging directory named by the task), plus a short
per-paper report. Read before first use: `data/schema/components.schema.yaml` (columns, enums, rules c1-c6),
`data/schema/component_parameters.yaml` (classes, subtypes, parameters, units, conventions),
`DevLog/DevLog-002-p1-component-atlas.md` (decisions D30-D50).

## Repo layout you need

- `data/registry/`: shared registry. `sources.csv` (source_id, access, redistribution), `organizations.csv` +
  `org_aliases.csv` (org ids for `fab_org_ids` / `facility_org_ids`). Read-only for you.
- `data/components/`: merged component tables. Read-only for you; write only in your staging directory.
- EO atlas inputs (sibling repo `../eo-modulator-atlas`, read-only): `references/<paper_id>/text.md` (page-delimited by
  `<!-- page N -->`), `references/<paper_id>/figures/page_NN.png` and `img_pNN_k.png`, `data/devices.csv` (EO device
  rows: device_id, physical_device_id, waveguide_platform, wavelength_nm and loss / Q / geometry columns).

## Hard rules

1. Empty = not reported. Never estimate, never use memory, a review, another paper's table or another version of the
   paper. A value comes from this source's text, table or figure, with a locator, or it is not entered.
2. Do not duplicate the EO atlas. Modulator metrics (Vpi, EO bandwidth, modulator IL/ER, VpiL) stay there. Enter the
   other components the paper characterizes and list the EO device rows they belong to in `host_device_ids` (all of
   them when one component serves several rows, e.g. every row of one `physical_device_id`). A value the linked EO row
   already holds in a column with the same meaning (`prop_loss_db_per_cm`, `q_loaded`, `fsr_nm`, `il_onchip_db`,
   `il_fiber_to_fiber_db`, `optical_power_handling_dbm`, `capacitance_ff`, and geometry columns such as film
   thickness, rib width, etch depth) is not re-entered unless the component's value differs. Values the EO row holds
   only in its `notes` are entered.
3. Values cited from earlier work (reference number, "previously reported") are not entered, and neither are values
   computed from them.
4. Basis by how the number was obtained, not by the paper's verb:
   - `measured`: read directly from the source's own measurement, including a dedicated test structure (even if the
     paper says "estimated from test-structure measurements"; quote the word in notes).
   - `derived`: arithmetic on the source's own stated measurements (difference of two structures, cascade divided by
     N, halving); formula in notes.
   - `author_estimate`: the result rests on an assumed, nominal or cited input, or a loss-budget term whose origin the
     paper does not state (note "origin not stated").
   - `simulated`, `design_target` (dimensions stated as design unless SEM/AFM-measured), `extracted_from_figure` (read
     off a plot; note the figure and reading uncertainty), `specification` (datasheet / nominal value of a purchased
     part, e.g. the MFD of the fiber a coupler is designed for).
5. Registry conventions are binding: loss positive dB (quote the source sign in notes); crosstalk, isolation and
   extinction as positive suppression magnitudes; 1-dB vs 3-dB vs FWHM widths never converted; linear % kept in %
   parameters; angles as printed.
6. Scope is mandatory on loss parameters and says what the number refers to; `method` says how it was isolated;
   `excludes` says what was subtracted:
   - `per_component`: one instance of an on-chip component (splitter, MMI, converter, crossing) isolated from a
     cascade or reference structure. A 1xN or 2x2 value below the ideal split is `excess_loss_db`.
   - `per_coupler` / `per_facet`: a fiber coupler or facet isolated individually (cutback, de-embedding).
   - `loopback_half`: half of a two-coupler (loopback, back-to-back) measurement.
   - `per_interface` (chip-chip), `fiber_to_fiber`, `on_chip_excess`, `device_total`, `de_embedded` (a device-level
     value with the couplers removed), `unspecified` (the paper does not say; note, never a guess).
7. Bounds and approximations: `over`, `>`, `below`, `<`, `about`, `~`, `up to` -> number + `qualifier`
   (gt / lt / approx / le); "as low as" -> `statistic: best`; "typical" -> `statistic: typical`. Ranges: `value` and
   `value_max`. Spectral values: one metric row per wavelength, or `wavelength_nm` + `wavelength_max_nm` when one
   value holds over a range. One value stated once for several bands is one row (`band: unspecified` + note), not one
   row per band.
8. Wavelength conditions: when the value has no stated wavelength but the device's operating band is stated, enter that
   band with `wavelength_inferred: true` and the reason in notes; when nothing is stated, `band: unspecified` + note.
9. Row granularity: one component row per physical design; operating points are metric conditions; a sibling design
   (different length) is a new row. Every component row needs at least one performance metric: geometry-only items
   are not rows (mention them in the report). Simulated or design-only components: `row_kind: design`.
10. Classes: on-chip inter-layer / inter-material transitions (Si-SiN, SiN-BTO, Si-TFLN couplers, monolithic or bonded
    on the same chip) are `waveguide_platform.transition` with `transition_loss_db`; `chip_chip_coupler` is between
    separate dies (laser-to-PIC butt, die-to-wafer, photonic wire bond). A ring used as a channel filter is
    `wdm.mrr`; a ring for loss extraction `resonator.ring`; band-stop / Bragg / photonic-crystal mirrors `reflector`.
11. Platform = the stack that guides light in this component (not blindly the EO host's): single-layer parts take
    their layer's value (`soi`, `sin`, `lnoi_strip` for fully etched TFLN, `suspended_gaas`), inter-layer transitions
    the hybrid value, with details in `core_material`. Report EO platform values that look wrong.
12. Organizations: `fab_org_ids` = the org the paper states fabricated this component (foundry, company, MPW service,
    "fabricated by X"), or the authors' own org when the paper says the authors fabricated it and that org is
    unambiguous (all authors at one company or institution); the vendor of a purchased device under test; a company
    that only supplied a wafer or film is a note. `facility_org_ids` = a shared facility
    where the work was performed or whose use or fabrication support is acknowledged ("performed at", "made use of",
    "support for the fabrication"); thanks to staff, operations teams or for training are not entered. Use registry org ids; an org missing from
    the registry goes in the report (name as printed + locator).
13. Measurement equipment (lasers, detectors, amplifiers of the setup) is not a component row.
14. Locators: `p.N` = page of the EO `text.md` (packaging atlas texts the same), plus `Fig. 3(b)` / `Table I` /
    `Sec. 2`; OFC extracted text has no page markers: `p.~N` (nearest preceding `_page_K_` image reference, N = K + 1)
    or `pNA` before the first one, always followed by the section / figure (D4). Rights: most sources are not
    open-licence: facts and locators only, no quotes beyond a few words in notes, never figures or text. Never copy
    e-mail addresses. No emoji. ISO dates. No network requests.

## Contract v4 additions (D80-D82, 2026-10-20)

- Basis: explicit arithmetic or any value that differs from the printed number -> `derived`; standard fit of own data ->
  `measured`; design-stated performance -> `simulated` if computed / simulated, else `author_estimate`.
- fab_org_ids needs an explicit fabrication statement naming the authors or an org; "we developed" / passive
  "fabricated" / all authors at one org are not enough. Grant / program acknowledgements are not facilities; the owner
  of a named facility is not a facility.
- Pre-merger papers point to the time-correct facility orgs (SNSF / SNF, not nano@stanford).
- Supplement locators: `p.N Supp. <label>` (N = page in text.md). Fiber-only passive parts in scope; fiber amplifiers /
  lasers not. On-chip mirror couplers between layers = `waveguide_platform.transition`.
- New parameters and allowances: see D81 in DevLog-002 (wdm.other, statistic `std`, avalanche_gain, gbp_ghz,
  breakdown_voltage_v, saturation_photocurrent_ma, relaxation_oscillation_ghz, fm_efficiency_ghz_per_ma,
  forward_voltage_v, pump_to_comb_efficiency_pct, beam_divergence_deg, phase_shift_pi, retention_time_s,
  mech_resonance_khz).

## Contract v5 additions: layout geometry (DevLog-005 D102-D107, 2026-10-20)

- Layout templates: `data/schema/component_layouts.yaml` (which subtypes each template serves, the dimensions its top
  view and cross-section need, the primary metric). Use the role-specific geometry parameters (`mmi_width_um` vs
  `width_nm`, `bus_width_nm` vs ring `width_nm`, `heater_*`, `absorber_*`, `lower_tip_width_nm` vs `tip_width_nm`,
  `layer2_thickness_nm`, `box_thickness_um`, `cladding_thickness_um`, ...): a drawing must never guess which width is
  which.
- Geometry pass for showcase components: every template dimension from text, tables and figure annotations. A figure
  dimension only when the figure labels it (`extracted_from_figure`, reading uncertainty in notes); never measured off
  a micrograph or a scale bar. Design dimensions `design_target`, SEM / AFM-measured `measured`. For showcase
  components the cross-section may restate an EO row's geometry when verified at the paper locator (cross-note).
- Showcase rows (`data/components/component_showcase.csv`): per template up to 2 `typical` (foundry / PDK / MPW
  component with measured performance, or the median performer when the subtype has >= 5 rows) and up to 2 `hero`
  (best measured primary metric with enough geometry for a to-scale top view), across >= 2 platforms where possible;
  record the criterion, rank and rationale.

## Contract v6 additions: `lit` corpus batches (DevLog-007 D150-D421, 2026-10-30)

- Inputs: `references/<paper_id>/text.md` (`<!-- page N -->`), `figures/page_NN.png`, `source.json`; source rows
  `lit:<paper_id>`; ids `cmp_lit_<paper_id>_<label>`; `host_device_ids` empty. `garbled_text_layer` in source.json:
  values only from clean passages or page renders. A cached file that is another paper or only a correction / erratum:
  stop on it and report (D397 / D409). Do not mention how a PDF was obtained in any output.
- Most-hit rulings (read the DevLog-007 tables for the rest): D159 ambiguous sample identity -> value not entered,
  bound in component notes; D259 / D259a / D408 values (and figures) the paper reproduces from the authors' own
  earlier work are removed, a journal extension of their conference paper keeps its values; D393 "around 1550 nm" is a
  stated wavelength; D396 one physical device used in several classes = one row per class with a cross-note; D400
  rings inside laser cavities and test / radius-series rings are `resonator.ring`, `wdm.mrr` only for channel filters
  in a WDM path; D401 per-port "3 +/- x dB" is a split deviation, not imbalance / IL; D402 purchased-wafer and foundry
  thicknesses `design_target`; D403 `q_intrinsic` (and finesse / Q_c from it) `author_estimate` unless the coupling
  regime is determined from the data; D404 pure rotator = `polarization.psr`; D158 / D407 single switch element =
  `switch_fabric.other`; D411 scope = integrated / chip-scale parts and fiber-coupled passive parts (bulk crystal parts
  out; D424: free-space switch fabrics with fiber I/O built on lithographic MEMS / LCoS chips stay in as
  `switch_fabric`, platform `other`); D422 / D423 a platform the paper does not state is left empty, never defaulted;
  D259 / D408 also cover a figure or value the paper assigns to another (even forthcoming) paper of the authors; D398 MPW access providers named for fabrication support are fab orgs; D395 / D399 fab = the org of the
  authors the fabrication sentence names.
- Figure-labelled dimensions only (`extracted_from_figure`), never scale-bar measurements; figure-read performance
  values `extracted_from_figure` with the reading uncertainty in notes.
- Report: write `<batch>/BATCH_REPORT.md` yourself (D392): per paper components / metric rows, values not entered and
  why, missing fab / facility orgs (check `organizations.csv` / `org_aliases.csv` first; name as printed + locator),
  judgment calls, registry gaps with the skipped value + locator and a proposed definition. Final message 5-10 lines.

## Audit workflow (fresh context, per batch; D50, D391)

- Read-only on the real batch. Confirm each cached text is its source row's paper (page-1 title). Check every metric
  row at its locator (figure renders for figure values): class / subtype, platform, scope / method / excludes, basis
  (rule 4, D80-D82, D157 / D256 unit conversions, D403), conditions, fab / facility orgs, D159 / D259 / D408, D411;
  look for misses (stated performance, D153 geometry). Verify the distiller's report; do not trust it.
- Output: `DevLog/audits/<date>-<batch>-audit.md` (front matter title / date / mode / patch; per-paper findings with
  locators; counts ok / imprecise / wrong per metric and component; misses; numbered coordinator questions with a
  recommendation; registry gaps confirmed; missing orgs) and `<batch>/patch.yaml` (`components` / `metrics` changes,
  `delete_components`, `delete_metrics`, `add_metrics`; every op with `why` + locator).
- Validate on a scratchpad copy only: `patch_component_staging.py <copy> <batch>/patch.yaml`, re-run (0 changes),
  `merge_component_staging.py <copy> --dry-run` (0 errors). Privacy grep of the outputs before finishing.

## Coordinator workflow (D390, D391, D415, D421)

1. New cached PDFs: `lit_extract.py --pending` (or `--paper-ids`), page-1 title / correction check,
   `lit_register_sources.py`, `validate_db.py`.
2. Batches `lit_NN` of <= 8-10 papers grouped by `primary_class` family (amplifier / frequency_converter /
   nonreciprocal; laser / chip_chip_coupler / micro_optics / free_space_emitter; phase_shifter / photodetector /
   waveguide_platform; resonator / splitter / mode_converter / reflector; crossing / fiber_chip_coupler /
   fiber_interface / polarization; wdm / switch_fabric), balanced by pages; table + decision in DevLog-007 before
   dispatch. Header batches `ofc_headers.py queue --corpus lit` (DevLog-011 contract) in parallel.
3. One distill subagent per batch, then one fresh-context audit per batch, coordinator rulings recorded as decisions,
   then per batch: backup zip of `data/components/` (once), `patch_component_staging.py` (re-run 0 changes),
   `merge_component_staging.py --dry-run`, merge; merges serialized. At most 10 subagents at once.
4. After the last merge: `build_views.py`, app `pnpm build` + `pnpm test` (the git-ignored `app/build` is checked by
   `test_no_review_ids_in_committed_views`), `validate_db.py`, ruff, mypy, pytest, privacy scan (e-mail, street,
   postal / P.O. box, local paths) of every changed file.

## Workflow (per paper)

1. Find the source row (`eo:<paper_id>`) in `sources.csv`; check `data/components/components.csv` for existing rows.
2. Read the whole `text.md` (methods, results, appendices, captions, acknowledgments, author contributions). List
   every non-EO component with a quantitative result.
3. For each component: `class.subtype`, `platform`, `core_material`, `cladding` (only if stated), `test_structure`,
   `host_device_ids`, `fab_org_ids`, `facility_org_ids`.
4. Metric rows: parameter (exact registry name), value, unit (exact registry unit), conditions (wavelength_nm or band,
   wavelength_inferred, polarization, temperature_k, bias_v, ref_plane, condition text incl. test fiber), scope /
   includes / excludes, statistic + n_samples, method, basis, locator, notes.
5. Ids: `component_id = cmp_<paper_id>_<short_label_slug>` for EO and packaging sources and
   `cmp_<corpus>_<native id slug>_<label>` for other corpora (e.g. `cmp_ofc2026_w1b3_tosa`), lowercase ascii, `_`;
   `metric_id = <component_id>-m1, -m2, ...`. A value you compute (radius from a diameter, dB from %) is `derived`. `verified_on` = today (ISO).
6. Validate: `uv run python scripts/merge_component_staging.py data/_staging/components/<batch> --dry-run` until it
   reports 0 errors. Report per paper what you did not enter and why.

Helper scripts: keep them in a private subfolder of the scratchpad named after your batch; other agents share the
scratchpad. Some text.md files contain stray bytes: use `grep -a`.

## Common pitfalls

Halved loopback values scoped `per_coupler`; fiber-to-fiber totals entered as per-coupler; GC efficiency in % entered
as dB; FWHM of a field (not power) profile taken as 3-dB width; loaded vs intrinsic Q (unqualified Q -> q_loaded with a
note); dB/m or dB/mm (convert to dB/cm, basis derived); values from comparison tables of other works; simulated loss in
the abstract and the measured value later; PD responsivity internal vs fiber-referred (`ref_plane`); thermo-optic
power per 2 pi vs per pi; pre- vs post-processing values not distinguished (say "not stated"); a test-pair spacing
entered as a pitch.
