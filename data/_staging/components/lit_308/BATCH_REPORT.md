# lit_308 batch report

Distilled 2026-11-27. Papers: lit:seidler2013, lit:nozaki2013, lit:chang2018c, lit:singh2015 (Optics Express,
open-access journal versions). Result: 16 component rows, 95 metric rows; `merge_component_staging.py --dry-run`:
0 errors, no warnings on these rows. Page-1 titles match the source rows for all four papers; none is a correction /
erratum; no garbled text layer. Figure values were read on the page renders (`figures/page_NN.png`). Helper script:
scratchpad `lit_308/gen.py` (not part of the repo).

## lit:seidler2013 (IBM Zurich, slotted Si PhC nanobeam cavity)

Components: 7. Metric rows: 51.

- `cmp_lit_seidler2013_slot_nanobeam_n6` / `_n7` / `_n8` / `_n9` / `_n10` (resonator.photonic_crystal, soi): one row
  per number of holes N on either side of the slot (rule 9; deotare2009 per-cavity-length precedent). Fig. 7 printed
  labels Q ~2,000 / 10,000 / 33,000 / 50,000 (measured, approx, D702) with resonance wavelengths read off each panel
  (inferred); 10-hole Q 1.4e5 (text, best). 8- and 9-hole rows also carry the Figs. 10-11 device values: linewidth
  4.25 / 4.55 GHz (-> 4250 / 4550 MHz, derived), peak transmission 0.12 / 0.0018 vs a GC-waveguide-GC test structure
  (-> 9.2 / 27.4 dB insertion_loss_db per_component, derived, approx), Fig. 11 labels 0.0586 / 0.0544 nm/K
  (-> 58.6 / 54.4 pm/K, derived; text -7.6 / -7.0 GHz/K). 10-hole: transmitted intensity below 1e-3 (-> > 30 dB,
  scope unspecified). Shared design geometry on every row (a 510 nm, w 550 nm, 220 nm Si, 3 um BOX, n_periods).
- `cmp_lit_seidler2013_slot_nanobeam_opt_sim`: simulated Q 820,000 at 1562 nm (mode I) and 2800 at 1613 nm (mode II),
  q_loaded (unqualified FDTD Q of the finite structure).
- `cmp_lit_seidler2013_focusing_gc` (fiber_chip_coupler.grating): "about 10 dB or more" (ge, scope unspecified) and
  "roughly 25 nm" 3-dB bandwidth, both author_estimate (no measurement described, D651); 19 lines, 650 nm period,
  duty cycle 88.5 % (fill_factor 0.885 derived, definition not given, D253), 10 deg.

Values not entered and why:
- Mode volume 0.0096 (lambda_vac/n)^3 = 35 aL (simulated), simulated Q/V near 1e8, measured Q/V >= 1e6 and 1.5e7
  (measured Q x simulated V): no parameter.
- Bistability: cavity energy for a one-linewidth shift 78 / 63 aJ (600 / 480 photons), power entering the cavity
  1.7 / 1.8 uW with 79 % / 98 % intracavity loss, fit slopes 1.20e16 / 1.19e17 J-1: no parameter.
- Confinement factor sigma_Si 0.72 / 0.68 (from measured thermal shift) and 0.78 (FDTD); temperature rise <= 4 K /
  ~50 K estimates: no parameter / estimates.
- Fig. 8(a) per-sample measured Q points (sample 2, slot lengths 470 / 486 / 500 nm): figure-only, slot-length
  variants without own rows; the Fig. 7 series is not tied to a sample in the text.
- Fig. 6 (8-hole device, mode I ~1540 nm, mode II ~1590 nm): no printed performance value.
- Slot width 40 nm, slot length 484.5 nm, hole radius 0.365a, taper to 67 %: no role-specific parameter (in
  core_material).

Missing fab / facility orgs: none. Fab borderline `org_ibm_research_zurich` (D84b / D715 analogue): passive
fabrication text (p.7 Sec. 3), staff thanks for assistance with reactive ion etching (p.16 Acknowledgments), all
authors at IBM Research - Zurich (p.1). No facility named.

Judgment calls:
- Per-N rows rather than one family row: each N has its own printed values; instances of the same N from different
  experiments (Fig. 7 vs Figs. 10-11, resonance 1524.3 vs ~1523.2 nm for N = 8) stay on the same design row with the
  instance named in condition.
- Wavelengths of the Fig. 7 Q labels and the 10-hole 1.4e5 value are plot-axis readings (wavelength_inferred true);
  the text does not say the Fig. 7 10-hole panel (Q > 100,000) is the 1.4e5 device.
- Simulated-design row kept `fabricated` (D80e): Fig. 4 says the fabricated geometry is the optimized one.
- GC loss and bandwidth author_estimate (D651) rather than measured (D167 limited to per-facet statements).

Registry gaps: `mode_volume_lambda_n3` (D430 candidate; value 0.0096 simulated, p.5), `q_over_v` (1.5e7 measured
Q / simulated V, p.12; p.11 Fig. 8(c)), bistability threshold energy `bistability_energy_aj` (78 aJ, p.14) or power
(1.7 uW, p.15), `confinement_factor` (0.72, p.16).

## lit:nozaki2013 (NTT, Fano all-optical switch with coupled InGaAsP H0 PhC nanocavities)

Components: 5. Metric rows: 15.

- `cmp_lit_nozaki2013_fano_h0_pair` (resonator.photonic_crystal): Qload 2900 (derived, CMT fit), Qunload 8000 and
  Qcpl 3000 (author_estimate, D403: loading split from the model), footprint < 100 um2 (derived from < 10 x 10 um2),
  slab 200 nm, a 460 nm.
- `cmp_lit_nozaki2013_fano_switch` (switch_fabric.other, D158 / D407, yu2014 precedent; D396 cross-note):
  switching contrast 3 dB at 0.4 fJ and 10 dB at 1 fJ (measured), best ~13.7 dB at ~2.3 fJ (Fig. 4(a) read),
  14 dB simulated (CMT, experimental parameters, 6 fJ, 50 Gb/s).
- `cmp_lit_nozaki2013_single_h0_cavity`: loaded Q 6500 at 1568 nm (measured).
- `cmp_lit_nozaki2013_single_h0_switch`: best contrast ~10.9 dB at ~3.6 fJ (Fig. 4(a) read, -2.5 FWHM series).
- `cmp_lit_nozaki2013_h0_cavity1_only`: Q around 1000 (measured, C band inferred from the stated 1.55 um operation).

Values not entered and why:
- Fano peak-to-bottom contrast "nearly 20 dB when the cavity detuning is small" (p.3-4): stated for the Fig. 1(c)
  series, not one device (D254 / D159); in component notes.
- Switching energy (0.4 / 1 / 6 fJ; kept as conditions), switching time window 18 ps at 1.91 fJ (not a 10-90 % rise /
  fall time), Qcc 1800, Qabs 34700, Qint 10500, photon lifetime 2.4 ps, detuning 0.8 nm, partition ratio 0.71: no
  parameter.
- Modal volume 0.025 um3 (~0.26 (lambda/n)^3): sentence cites refs. [2, 15] (rule 3); simulated carrier lifetime
  3.5 ps cites ref. [2].
- -14 dB insertion loss before the cavity (p.6): input-path loss of the setup / chip used to estimate Up; the
  coupler is not described; kept in the switch-row notes.
- Fig. 5 projections (Qunload 26000, reduced Qcpl / Qcc; > 20 dB, ~1 fJ, ~10 fJ, 0.4 fJ with tau_c 20 ps) and the
  modelled single cavity (Qcpl 12000 / 52000; 50 / 370 / 180 fJ): parameter studies without a design or a fabricated
  device.
- Simulated single-cavity contrast "about 5 dB" (Fig. 2(c), CMT): a modelled cavity with the Fano system's Q values,
  not a device.

Missing fab / facility orgs: none. Fab borderline `org_ntt` (D84b, D715): passive fabrication text (p.3), thanks to
three persons "for support in fabricating the device" (p.12 Acknowledgments), all authors at NTT laboratories (p.1).

Judgment calls:
- Platform left empty on all 5 rows (D422 / D423): the InGaAsP slab is stated, air-bridge or substrate is not
  (nozaki2016 / matsuo2012 rows use `inp_membrane` because those papers state an air-bridge slab).
- q_loaded 2900 `derived` (CMT model fit, D80a, yu2014 precedent); q_intrinsic / q_external `author_estimate`.
- Two figure reads (Fig. 4(a) maxima) added as best contrasts next to the printed 3 / 10 dB points.

Registry gaps: `switching_energy_fj` on switch_fabric (0.4 / 1 fJ, p.7; D579 candidate), `switching_window_ps`
(18 ps, p.7), `q_coupling_intercavity` (Qcc 1800, p.5), `q_absorption` (34700, p.5; D430 / D558 candidate),
`photon_lifetime_ps` (2.4 ps, p.5; D558 candidate).

## lit:chang2018c (HUST, inverse-designed dual-mode 3 dB power splitter)

Components: 3. Metric rows: 22.

- `cmp_lit_chang2018c_dual_mode_splitter` (splitter.other, xie2020 precedent): measured average EL < 1.5 dB
  (per_component, normalized to the on-chip reference MDM system), XT > 20 dB, EL imbalance 0.08 dB (TE0) /
  0.07 dB (TE1); simulated EL < 0.9 dB, XT > 20 dB (TE0) / > 24 dB (TE1); geometry: 2.88 x 2.88 um region
  (mmi_length / mmi_width per the xie2020 convention, footprint 8.2944 um2 derived), 900 nm ports (0.9 um
  derived), 120 nm pixel pitch, 220 nm hole depth and Si, 1 input / 2 outputs.
- `cmp_lit_chang2018c_ref_mdm_system` (mode_converter.mdm_mux, test_structure): MUX + DEMUX back-to-back IL < 1.5 dB
  (de_embedded, method unspecified: normalization not stated, D708 paredes2021) and XT > 24 dB, 1520-1600 nm.
- `cmp_lit_chang2018c_dmc_adiabatic_design` (mode_converter.converter, row_kind design): simulated mode conversion
  up to 98 % for L > 100 um, W0 550 / W1 450 nm.

Values not entered and why:
- Average standard deviations 0.32 / 0.16 / 0.21 / 0.15 dB of the '1-2', '1-3', '2-1', '2-4' traces: the port-to-mode
  mapping of the splitter circuit is not stated.
- Simulated designs of other footprints (2.88 x 2.16, 2.88 x 3.6 um2) and other random initial patterns: curves only.
- Stem effective indices 2.6 / 2.28 (simulated), Wgap > 1 um (design rule), inverse-design runtime: no parameter /
  not a performance value.

Missing fab / facility orgs: none. Fab `org_huazhong_university_of_science_and_technology`: "We fabricated and
experimentally demonstrated" (p.7 Sec. 3), all authors at two HUST units (D154 parent). No facility (funding only).

Judgment calls:
- Range conflict (D417): p.2 says 1540-1580 nm for the measured EL / XT; abstract, p.7 and conclusion say 1520-1580 nm
  (entered); noted on the component.
- The reference MDM system uses the (DE)MUX design of the authors' ref. [28], but its measured values belong to this
  chip and Fig. 6(e) is not attributed to ref. [28] (D408): kept.
- The design-only adiabatic DMC entered as a `design` row (rule 9); band unspecified (calculation wavelength not
  stated).

Registry gaps: none confirmed (std of repeated measurements has `statistic: std`, held back only for the port
mapping).

## lit:singh2015 (USyd / ANU / INL, AMTIR-1 chalcogenide microdisk, photo-tuning)

Components: 1. Metric rows: 7.

- `cmp_lit_singh2015_amtir1_microdisk` (resonator.disk, platform other): loaded Q 1.2e5 at 1550 nm (measured,
  instrument-limited, higher-order radial mode 13 / 362), photo-induced shifts at 1534.5 nm: red ~1 nm and then blue
  ~0.5 nm at 10 mW/mm2, red ~0.4 nm at 1 mW/mm2 (tuning_range_nm, jayatilleka2021 / li2025f trimming precedent);
  R 50 um, 300 nm film, ~2 um pedestal (design_target).

Values not entered and why:
- Silica fiber taper (waist ~1.5 um, insertion loss 0.1 dB, p.3): the authors' measurement probe, not a component
  row (rule 13, D160); in component notes.
- Film / disk index change 0.06 / 0.04 and band-gap shift 0.072 / 0.05 eV (Table 1, calculated material
  properties), film index drop up to 2 %, stretched-exponential fit parameters, calculated < 2 C heating, 24 h
  stability (no retention parameter on resonator): not component metrics / no parameter.

Missing fab / facility orgs: none. Fab empty: first-person "We fabricated microdisks" (p.3) but the authors sit at
the University of Sydney, the Australian National University and INL Lyon (D154: no unambiguous own org); funding
acknowledgments only (p.6).

Judgment calls: shifts entered as three `tuning_range_nm` rows with the direction and exposure in condition; Q kept
without a qualifier (printed value; instrument limit in notes).

Registry gaps: none.
