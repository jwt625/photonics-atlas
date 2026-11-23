# lit_261 batch report

Papers: lit:zhao2016a (Optics Express 2016), lit:yu2023b (JLT 2024), lit:zhang2020b (JLT 2020). Page-1 titles match the
source rows; no garbled text layers. verified_on 2026-11-23. Dry run: +13 components, +97 metrics, 0 errors (the only
warning is the pre-existing ni2025b duplicate, not in this batch). No existing rows for these sources. Values are only
what each paper reports itself; yu2023b Table I rows of other works and the cited-work ranges in zhao2016a (20-23 dB,
p.9) are not entered.

## Components / metric rows

| paper | component | class | metrics |
|---|---|---|---|
| zhao2016a | cmp_lit_zhao2016a_mrr_fcw_fano | resonator.other | 17 (Fano ER 30.8 dB best at V = 1.26 V; 25.8 dB at VR = 1.38 V; 8 more labelled ERs by heater bias, Figs. 4-5; off-resonance IL ~20 dB figure read; FCW 642.3 um; rib 400 / 220 / 90 nm; 2 um BOX; 150 nm TiN) |
| zhao2016a | cmp_lit_zhao2016a_mrr_r10 | resonator.ring | 9 (FSR 9.912 nm; power coupling 0.40 % derived from model t = 0.998; R 10 um; gap 450 nm; rib 400 / 220 / 90 nm; 150 nm TiN; 2 um BOX) |
| yu2023b | cmp_lit_yu2023b_bent_dc_1550 | splitter.directional_coupler | 14 (EL < 0.05 dB measured, < 0.026 dB simulated; 45-55 % bandwidth 80 nm measured, ~130 / 120 nm simulated (dw 0 / +20); MZI ER ~16 dB measured, > 24.9 dB simulated; 440 nm; ~110 nm gap; ~28.8 um2; 16 um; 220 nm / 2 um BOX / 2.2 um clad) |
| yu2023b | cmp_lit_yu2023b_bent_dc_2000 | splitter.directional_coupler | 16 (EL < 0.05 dB measured, < 0.03 dB simulated; bandwidth 100 nm measured, ~160 / 160 / 80 / 130 nm simulated (dw 0 / +-10 / -30 / +20); MZI ER ~20 dB measured, > 28 dB simulated; 640 nm; ~100 nm gap; ~60 um2; 24 um; stack) |
| yu2023b | cmp_lit_yu2023b_bent_dc_1550_dw_m10 / _dw_p10 | splitter.directional_coupler | 2 each (MZI ER ~16 / ~16 dB, Fig. 10(a); width 430 / 450 nm derived) |
| yu2023b | cmp_lit_yu2023b_bent_dc_2000_dw_m10 / _dw_p10 | splitter.directional_coupler | 2 each (MZI ER ~16 / ~18 dB, Fig. 10(b); width 630 / 650 nm derived) |
| yu2023b | cmp_lit_yu2023b_mzs_1550 | switch_fabric.other | 4 (EL < 0.4 dB; ER > 17 dB, 1520-1610 nm; P_pi 61.89 mW derived; 2.6 V) |
| yu2023b | cmp_lit_yu2023b_mzs_2000 | switch_fabric.other | 4 (EL < 0.6 dB; ER > 18 dB, 1900-2000 nm; P_pi 96.1 mW derived; 3.08 V) |
| zhang2020b | cmp_lit_zhang2020b_angled_pi_mmi_family | splitter.mmi | 12 (excess loss < 1.2 dB at 1550 nm all designs, worst case 1.5 dB over 1525-1575 nm; coupling variation < 0.023; Table I geometry: 4.8 um body, 24.3-24.5 um segments, 1.3 um ports, 10 um tapers, 450 nm access, 75 um length, 220 nm full etch, 3 um BOX) |
| zhang2020b | cmp_lit_zhang2020b_angled_pi_mmi_50 | splitter.mmi | 12 (cross ratio ~49 % and excess loss ~0.63 dB at 1550 nm, Fig. 8 reads, mean of 5; +-1 dB ratio bandwidth > 250 nm simulated; same geometry) |
| zhang2020b | cmp_lit_zhang2020b_vertical_gc | fiber_chip_coupler.grating | 1 (7 dB GC-to-fiber loss at 1550 nm, loopback_half derived) |

Per paper: zhao2016a 2 / 26, yu2023b 8 / 46, zhang2020b 3 / 25.

## Values not entered and why

zhao2016a
- Average spectral slopes 101.3 dB/nm (p.6) and 226.5 dB/nm (p.9, also abstract-level claim in the conclusion): no parameter.
- Resonance red shifts 0.260 nm at VR = 1.16 V and 1.148 nm at VR = 2.44 V (p.6-7): heater drive given in volts only (no
  power, no resistance); `tuning_efficiency_pm_per_v` is defined for non-thermal actuators; not a tuning range limit.
- Simulated free-carrier concentration 3.45e18 cm-3 at 1.26 V (p.9, model of the authors' ref. [35]); simulated MRR / RTR
  shift ratio 17.5 (p.5); red (simulated) labels in Figs. 4-5 (Delta n, phase, alpha_L); Fig. 3 model curves.
- Ring round-trip amplitude alpha = 0.983 (model, p.6): not converted to a propagation loss (not printed).
- FCW as a lateral p-i-n variable attenuator: no quantitative loss-vs-bias value printed; no row.
- TiN heaters as phase shifters: only bias voltages, no power or resistance; no phase_shifter row (heater thickness on
  the device rows).

yu2023b
- Table I other-work rows (refs. [7], [9], [11], [12], [20]-[27]): cited values (rule 3).
- Fabrication tolerance "+/-10 nm" (Table I, abstract): generic tolerance, no parameter (D49); the measured dw = +-10 nm
  devices are entered as sibling rows instead.
- Design-region length "as short as 8 um" (p.5 conclusion): role relative to the 16 / 24 um footprints not defined.
- Fig. 2 optimization FOM (0.148 / 0.122 dB) and run times: design-process metrics.
- Fig. 4 measured split-ratio curves: no printed values beyond the Table I bandwidths.
- Table I MZI EL "~0" (sim. and exp.): not a usable value; MZS EL rows carry the body-text bounds.
- Heater resistance (2.6 V / 23.802 mA, 3.08 V / 31.2 mA): heater not described; no phase_shifter row.
- Abstract / conclusion MZS claims (EL < 0.3 dB, ER ~18 / 20 dB, ER > 15 / 20 dB) and Fig. 6 per-state labels: kept in
  component notes as D417 conflicts; rows use the Sec. III results.

zhang2020b
- Simulated fabrication-corner deviations of the 50 % design: delta-eta < 1.3 % (0.1 dB) and delta-IL 0.3 dB at 1550 nm,
  maximum delta-eta 0.58 % (width) / 0.99 % (thickness), 2.1 % (0.17 dB) and 1.4 % (0.11 dB) over the extended C band for
  the -10 / +10 nm corners (p.6, Fig. 10): no registry parameter (registry gap below).
- Per-angle Fig. 8 / Fig. 9 reads for the 11 other bend-angle designs (only the 50 % design is entered).
- Simulated conventional designs CON1 / CON2 and the 3.3x / 3x / factor-2 comparisons (Figs. 4-6): no printed values.
- Model-vs-measurement loss discrepancy < 0.4 dB (p.6); 1.17 % imaging-length shift per 10 nm partial-etch change (p.4,
  rib variant not built); +-10 nm width / thickness give 0.42 % / 0.74 % imaging-length terms (p.4, analysis inputs).
- Bend angle theta, theta_cut 75 deg, Ls 5 um: no splitter parameter (`coupling_angle_deg` is the bent-DC arc angle, a
  different quantity); in notes / labels.

## Missing fab / facility orgs

None. yu2023b fab `org_applied_nanotools` (registry). zhao2016a ("standard CMOS process", passive) and zhang2020b
("commercial 180 nm foundry process", no foundry named) leave fab empty; no facility statements in any paper.

## Judgment calls (for the auditor)

1. zhao2016a class `resonator.other` for the MRR + feedback-waveguide Fano system with the MRR as a separate
   `resonator.ring` row (zheng2017 / du2019 precedents, D396 cross-note); FSR 9.912 nm placed on the ring row because the
   paper equates it with the MRR FSR.
2. zhao2016a: ten ER rows, one per labelled bias state (D651 split-by-operating-point precedent), all `measured` from
   printed black labels; dip wavelengths are figure reads with `wavelength_inferred` true (+/- 0.05 nm). The 16.2 dB label
   appears in both Fig. 4(b) and Fig. 5(a) (same unbiased state): entered once.
3. zhao2016a off-resonance "IL" ~20 dB (Fig. 4(a)) entered as `insertion_loss_db`, scope unspecified, extracted_from_figure
   (lensed-fiber input; coupling elements and output path not described). Drop if the auditor considers a baseline read
   too weak.
4. zhao2016a power coupling 0.40 % `derived` from the simulation parameter t = 0.998 chosen to reproduce the measured
   spectra (zheng2017 m6 precedent, D80a).
5. yu2023b dw = -10 / +10 nm devices as separate component rows (rule 9: intentional design-width siblings), each with the
   Fig. 10 labelled MZI ER and a derived width; simulated width-deviation bandwidths (dw +-10 / -30 / +20) kept as
   conditions on the dw = 0 design rows (tolerance analysis of one design). Auditor may prefer either both as conditions or
   both as siblings.
6. yu2023b 45-55 % split bandwidths stored in `bw_1db_nm` with the criterion in the condition (chen2022a / chung2023 /
   lu2015a precedent); measured 80 / 100 nm are near or equal to the measured spans.
7. yu2023b MZI extinction on the DC rows (D74); printed conflict for the 1.55 um dw = 0 MZI: ~16 dB (text, Fig. 5(d)) vs
   15 dB (Table I) vs ~18 dB (Fig. 10(a)); the text value is entered, the others in notes (D417).
8. yu2023b loss rows: "normalized" transmissions with no stated reference -> scope de_embedded, method unspecified
   (paredes2021 / D708); simulated EL rows per_component.
9. yu2023b `process_name` "NanoSOI fabrication service (Applied Nanotools, ref. 19)": the fabrication sentence cites ref. [19],
   whose title names the service (precedent rows "Applied Nanotools NanoSOI").
10. yu2023b MZS switching power `p_pi_mw` derived from the printed on-state V x I (on-state = bar / cross swap of a
    symmetric MZI, i.e. pi); `v_pi_v` = printed on-state voltage.
11. zhang2020b family row (D165) for the family-level bounds plus one member row for the 50 % design; the paper's
    "insertion loss" (total output / input) stored as `excess_loss_db` (D43); scope per_component with method
    reference_structure (GC loss from back-to-back GCs subtracted). Fig. 8(b) shows the 9 deg average at about 1.24 dB,
    slightly above the printed "below 1.2 dB" (noted, printed bound kept).
12. zhang2020b 50 % design at 4.9 deg (text, Figs. 8-9) despite the Fig. 10 caption's 4.4 deg (D417 note).
13. zhang2020b GC 7 dB as `loopback_half` derived (pair value not printed; doerr2010 precedent).
14. Platforms: zhao2016a `soi_rib` (90 nm slab in Fig. 1 inset); yu2023b `soi` (etch depth not stated); zhang2020b MMI
    `soi_strip` (fully etched body stated), GC `soi`.

## Registry gaps

- `fab_tolerance_coupling_deviation_pct` (or similar) for splitters: deviation of the coupling ratio from the design value
  under stated fabrication corners (width / thickness +-N nm), at one wavelength or maximum over a band. zhang2020b p.6
  Fig. 10: < 1.3 %, 0.58 %, 0.99 %, 2.1 %, 1.4 % (simulated); companion `fab_tolerance_loss_db` (0.3 dB).
- `criterion_bw_nm` (already a candidate, D539): bandwidth over which a split ratio stays within a stated window
  (yu2023b 45-55 %, zhang2020b +-1 dB); currently in `bw_1db_nm` with the criterion in the condition.
- `spectral_slope_db_per_nm` for Fano / sharp-edge resonators: zhao2016a 101.3 dB/nm (p.6) and 226.5 dB/nm (p.9)
  (zheng2017 179.4 / 252 dB/nm also left in notes).
- `tuning_efficiency_pm_per_v` limited to non-thermal actuators: thermo-optic shifts reported only per volt (zhao2016a
  0.260 nm at 1.16 V, 1.148 nm at 2.44 V) have no home.
