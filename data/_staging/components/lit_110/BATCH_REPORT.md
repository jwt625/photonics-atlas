# lit_110 batch report

Distilled 2026-11-08. 7 papers, 15 components (9 fabricated, 6 design), 200 metric rows. Validation:
`uv run --offline python scripts/merge_component_staging.py data/_staging/components/lit_110 --dry-run` -> 0 errors
(one pre-existing WARN on `cmp_lit_ni2025b_pimmwc`, not this batch). Every cached text matches its source row title
(page 1 checked); none is a correction / erratum. The brief names this file `lit_110_REPORT.md`; the skill's default
name is `BATCH_REPORT.md`.

## Per paper

### zhang2022a (Opt. Express 2022, backward-mode-conversion grating mode filters, 220 nm SOI)
- Components (5): `te1_pass_filter` (fabricated, 16 rows), `te2_pass_filter` (fabricated, 16), `te3_pass_filter_design`
  (9), `te23_pass_filter_design` (7), `te2_filter_adc_demux_design` (mode_converter.mdm_mux, 4).
- Class: mode filters as `mode_converter.other` (dagostino2015 / song2021b precedent); ER as `extinction_db` (type in
  condition).
- Measured IL / ER normalized to identical configurations without the filter -> `per_component`, `reference_structure`.
  Both the critical-performance bands (1518.3-1569.5 nm, 1518.5-1566.8 nm) and the full 1500-1580 nm span (TE1-pass)
  entered.
- TE2-pass simulated ER at 1550 nm "42.7 dB/31.3 dB": mode assignment (TE0 / TE1) from the Fig. 5(b) label.
- Not entered: duty cycle 0.5 (fill_factor not allowed for mode_converter); simulated fabrication tolerances (no
  parameter); hole-row spacing w23 / w33 / w43 and hole lengths a3 / a4 (no role-specific parameter, in notes);
  TE2,3-pass waveguide width (not printed); per-input demux crosstalk labels in Fig. 13 (text bound entered);
  "~11 um" length for the TE3 / TE2,3 designs (stated only collectively in the conclusion).
- Fab / facility: empty ("are fabricated", passive; authors Hebei University + Southeast University).

### eznaveh2018 (Opt. Express 2018, OAM photonic lantern)
- Components (1): `oam_lantern_5mode` (mode_converter.mdm_mux, platform other, all-fiber; 4 rows). In scope as a
  fiber-coupled passive part (D411; leonsaval2014 / anelli2024 precedent).
- Rows: IL < 3 dB (wavelength and splice inclusion not stated -> `band unspecified`, `scope unspecified`); average
  modal purity > 10 dB as `extinction_db` (statistic mean); n_inputs 5, n_outputs 1.
- Not entered: MDL 1.52 dB of the MUX / DEMUX pair (p.8; `mdl_db` is fiber_interface-only, registry gap below);
  "at least 550 nm" operating range (qualitative, mode images only); multimode-end ring geometry (no parameter);
  ring-core delivery fiber (transmission fiber, not a component).
- Fab / facility: empty (first-person "we follow the same procedure", fabricator not named, six orgs).

### guo2025 (Opt. Express 2025, grooved-waveguide MMI three-mode (de)MUX, InP)
- Components (2): `gw_mmi_3mode_mux` (fabricated, 31 rows), `gw_mmi_4mode_cascade_design` (6).
- Measured IL 2.9 / 7.53 / 4.05 dB (TE0 / TE1 / TE2 at 1550 nm) normalized to an equal-length straight waveguide ->
  `per_component`, `reference_structure`; 3-dB bandwidth > 13.5 nm; SEM dimensions as `measured`, um -> nm
  rescalings `derived` (D157).
- Printed inconsistency: SEM values for WM2 / WM3 (800 nm / 1.42 um, p.5) are swapped against the design (1.4 um /
  820 nm) while the measured W3 / W4 follow the design; the measured WM2 / WM3 were not entered (component notes).
- Not entered: cosine S-bend radius 338 um (min_bend_radius_um not allowed for mode_converter); WMMI (not printed).
- Fab / facility: empty (passive; authors CAS Key Laboratory of Optoelectronic Materials and Devices + UCAS).

### a2017 (Laser Photonics Rev. 2017, 10-channel dual-polarization mode (de)MUX, Dai et al.)
- `garbled_text_layer` flagged on p.9 only (reference list). Ranges whose "~" was lost in the text layer
  ("-15~-25 dB", "0.2~1.8 dB", "~-20 dB") and Table 1 verified on the p.4 / p.6 / p.8 renders.
- Components (1): `dual_core_taper_mux_10ch` (mdm_mux link, soi_strip; 62 rows): per-channel excess loss (10) and max
  crosstalk (10) at 1555 nm for the MUX + bus + DEMUX pair (`de_embedded`, `reference_structure`, as a2013); ranges over
  1525-1610 nm; simulated stage #5 taper crosstalk > 20 dB (1490-1620 nm) and > 99 % target-supermode transmission;
  Table 1 widths (rescaled, `derived`) and taper lengths per stage.
- Not entered: PBS performance (> 30 dB ER, < 0.5 dB EL, 70 nm) is the authors' ref. [40] (rule 3 / D259); Table 1
  gap widths (gap_nm not allowed for mode_converter); data-transmission eye ER (not a component metric); separate
  stage-taper rows (values only for stage #5, kept on the link row with the stage in condition).
- Fab / facility: empty ("was fabricated", passive; Zhejiang University + CUHK).

### frandsen2014 (Opt. Express 2014, topology-optimized PhC-waveguide TE0-TE1 converter, 340 nm SOI)
- Components (2): `phcw_te0_te1_x1` (14 rows), `phcw_te0_te1_te0_x2` (test structure, 2 rows).
- Only X2 (TE0-TE1-TE0) transmission was measured; the paper halves it for X1 ("experimentally estimated",
  halving error < 0.25 dB stated) -> X1 IL rows `derived`, X2 rows `measured`, `device_total`.
- Measured mode extinction ~12 dB (IR-camera line scans, resolution-limited) as `measured`.
- Footprint 6.3 x 3.6 um -> 22.7 um2 `derived`; PhC lattice pitch 420 nm as `period_nm` (condition says lattice pitch).
- Not entered: hole diameters (no parameter); 2D-TopOpt and butt-coupled-output variants (relative values only);
  inverse-taper / SU-8 couplers (ref. [16], no values).
- Fab / facility: empty (passive "were defined"; all authors DTU but v4 rule: not enough).

### garciarodriguez2017 (Opt. Lett. 2017, tolerant ADC mode converter / MUX, 220 nm SOI)
- Components (3): `adc_gap100` (fabricated, 13 rows), `adc_gap200_design` (4), `adc_gap300_design` (3).
- Measured conversion efficiency 90 % at 1550 nm and > 84 % over 1540-1560 nm; the test device has two ADCs in series
  (TE0-TE1-TE0) and the extraction / normalization is not stated -> `per_component`, method `unspecified`, note.
- Simulated values of the nominal d = 0.1 um / L1 = 12.50 um design kept on the fabricated row (D80e). SEM labels
  (454.7 / 99.71 / 955.5 nm, Fig. 6(a)) entered as `measured` widths; gap in notes.
- Fig. 5 tolerance values (82.3 %, ~46 %, ~0 %): wavelength not printed, design wavelength 1550 nm entered with
  `wavelength_inferred`.
- Not entered: d = 0.1 um / L2 = 37.74 um design (only family-wide bounds: > 97.4 %, ER > 28.4 dB; no own value);
  thermal sensitivity < 0.2 % over +/- 20 K (no parameter); "additional 0.35 dB excess loss" (a difference to theory).
- Fab: `org_upv` ("fabricated in the NTC laboratory"; NTC is the authors' UPV unit, all authors there). See
  coordinator question 1.

### xu2016 (Opt. Lett. 2016, 16-channel DPBWA mode (de)MUX, 340 nm SOI)
- Components (1): `dpbwa_16ch_mux` (9 rows): measured IL < 1 dB, CT < -20 dB over 1520-1600 nm (`de_embedded`,
  normalized to a straight waveguide with the same GCs); simulated IL < 0.1 dB, CT < -30 dB over 1520-1620 nm.
- Not entered: bend radii (5-17 um, r1 5 um), wgap 300 nm, port spacing wout 1.5 um (radius / gap parameters not
  allowed for mode_converter; wout printed as a "gap width" but used as a radius increment, so not a pitch_um);
  transition overlap loss "< 0.01" (unit ambiguous).
- Fab / facility: empty ("was fabricated", passive; both authors Zhejiang University).

## Missing fab / facility orgs

| Name as printed | Locator | Role | Note |
| --- | --- | --- | --- |
| NTC laboratory (Nanophotonics Technology Centre, Universitat Politecnica de Valencia) | lit:garciarodriguez2017 p.4 | fab | parent `org_upv` used (lit:aamer2012 rows name "UPV NTC" only in notes); propose a child org of `org_upv` |

No facility orgs are acknowledged in any of the seven papers.

## Judgment calls

1. Mode filters (zhang2022a) -> `mode_converter.other`, not `reflector` (the grating reflects the rejected modes but the
   device function is mode filtering; dagostino2015 / song2021b precedent).
2. a2017 / xu2016 / guo2025 link measurements normalized to a straight waveguide: a2017 values printed as "excess
   losses" -> `excess_loss_db` `de_embedded` (a2013 precedent); xu2016 printed as IL (Eq. 2) -> `insertion_loss_db`
   `de_embedded`; guo2025 (single MMI device, equal-length straight reference) -> `insertion_loss_db` `per_component`.
3. frandsen2014 X1 values derived by halving X2 (the paper's own arithmetic); X2 kept as a separate test-structure row.
4. eznaveh2018 average modal purity stored as `extinction_db` (mode selectivity, leonsaval2014 precedent) rather than
   `crosstalk_db`.
5. garciarodriguez2017 fab mapped to the parent university because the named unit is missing from the registry.
6. a2017 stage #5 simulated values entered on the link row with the stage in `condition` instead of a separate
   design-element row.

## Coordinator questions

1. garciarodriguez2017 fab: keep `org_upv` or leave empty until an NTC (UPV) org exists and re-point it in an org fix
   batch? Recommendation: keep `org_upv` now (correct parent), re-point to the NTC child org if one is added.
2. Registry gaps 1-4 below: four parameters skipped repeatedly for `mode_converter` (gap, MDL, fill factor, bend
   radius); recommendation: extend the class lists, then a gap-fill for this batch.

## Registry gaps (skipped value + locator + proposed definition)

1. `gap_nm` for `mode_converter` (ADC / dual-core / filter gaps): zhang2022a ADC g = 95 nm (p.11 Fig. 12 caption);
   garciarodriguez2017 d = 0.1 um design, 99.71 nm SEM (p.2-4, Fig. 6(a)); a2017 wig1 = wig2 = 120 nm (Table 1);
   xu2016 wgap 300 nm (p.2). Proposal: add `mode_converter` to `gap_nm` classes ("coupling gap of an ADC / dual-core
   / waveguide-array mode (de)MUX").
2. `mdl_db` for `mode_converter`: eznaveh2018 MDL 1.52 dB of the lantern MUX / DEMUX pair (p.8 Sec. 3.3). Proposal:
   allow `mdl_db` for `mode_converter` ("mode-dependent loss of a mode (de)MUX or pair, configuration in condition").
3. `fill_factor` for `mode_converter`: zhang2022a grating duty cycle 0.5 (p.5-6). Proposal: add `mode_converter` to
   `fill_factor` classes.
4. `min_bend_radius_um` / `radius_um` for `mode_converter`: guo2025 S-bend radius 338 um (p.2); xu2016 bend radii
   5-17 um (p.2). Proposal: add `mode_converter` to `min_bend_radius_um` classes.
