# lit_246 batch report

Papers: lit:chung2019a (Opt. Express 27(9), 2019; low-power thermo-optic Si modulator, 30 pages, flagged
`garbled_text_layer` on p.12 / 14 / 18), lit:fujisawa2017 (Opt. Express 25(8), 2017; clothoid 90-deg Si-wire bends),
lit:deng2016 (Opt. Express 24(7), 2016; polarization-insensitive MMI strip-slot converter), lit:novack2013 (Opt.
Express 21(23), 2013; Ge PD with inductive gain peaking). Page-1 titles match the source rows. verified_on 2026-11-22.
Dry run: +21 components, +105 metrics, 0 errors (the one warning printed concerns merged ni2025b rows, not this batch).

chung2019a: the garbled pages hold only equations (Appendix A-2 / A-3); every value comes from clean text pages or
page renders (p.6 Fig. 3, p.8 Fig. 4, p.17 Fig. 6, p.19 Table 4 checked on renders).

## Components / metric rows

| component | class | metrics |
|---|---|---|
| cmp_lit_chung2019a_tops_n14 | phase_shifter.thermo_optic | 19 (P_pi 2.56 mW, IL 1.23 dB mean of 3, 10.1 kHz, rise / fall 34.8 / 34.4 us MZI intensity, phase rise 58.5 us, simulated rise 37.5 us, heater R 243.7 / 249.5 ohm, heater 60 x 3 um x 110 nm, gap 0.9 um, path 1220 um, footprint 2300 um2, 220 nm / 2 um BOX, widths 400 / 500 nm) |
| cmp_lit_chung2019a_tops_single_wg_design | phase_shifter.thermo_optic (design) | 2 (simulated 24.4 mW, 27.6 us) |
| cmp_lit_chung2019a_tops_n26_p800_design | phase_shifter.thermo_optic (design) | 3 (simulated 1.97 mW, widths 400 / 600 nm) |
| cmp_lit_chung2019a_mcb180_avg | waveguide_platform.bend | 2 (0.077 dB mean, 0.014 dB std, 5 samples) |
| cmp_lit_chung2019a_mcb180_type_a | waveguide_platform.bend | 5 (simulated 0.099 dB, R 1.522 um, widths, 2 um taper) |
| cmp_lit_chung2019a_mcb180_type_b | waveguide_platform.bend | 5 (simulated 0.033 dB, R 1.522 um, widths, 2 um taper) |
| cmp_lit_chung2019a_mcb180_type_a_improved_design | waveguide_platform.bend (design) | 1 (simulated 0.05 dB, Fig. 6(c) label) |
| cmp_lit_chung2019a_circ180_r0p5 / r1p5 / r2 / r4 _design | waveguide_platform.bend (design) x 4 | 2 each (simulated 4.23 / 0.87 / 0.15 / 0.08 dB per 180-deg bend; radius) |
| cmp_lit_fujisawa2017_normal_r4 | waveguide_platform.bend | 5 (0.019 dB/90 measured, ~0.024 simulated, R 4 um, 400 x 210 nm) |
| cmp_lit_fujisawa2017_clothoid_a_r4 | waveguide_platform.bend | 4 (0.016 measured, ~0.021 simulated, geometry) |
| cmp_lit_fujisawa2017_clothoid_b_r4 | waveguide_platform.bend | 4 (0.002 measured, ~0.0047 simulated, geometry) |
| cmp_lit_fujisawa2017_clothoid_c_r4 | waveguide_platform.bend | 4 (0.006 measured, ~0.0094 simulated, geometry) |
| cmp_lit_fujisawa2017_offset_bend_r4_design | waveguide_platform.bend (design) | 3 (~0.005 dB/90 simulated at dx 15 nm, geometry) |
| cmp_lit_deng2016_mmi_strip_slot_l4 | mode_converter.converter | 14 (95.9 % TE0 / 96.6 % TM0 measured, > 92 % over 1475-1600 nm, 96 % simulated, L 4 um, MMI 1.22 x 1.46 design / 1.21 x 1.41 SEM, strip 400 / slot 620 nm SEM, 250 nm / 2 um BOX / 1 um cladding) |
| cmp_lit_deng2016_mmi_strip_slot_l2 / l3 / l5 | mode_converter.converter x 3 | 3 each (TE0 / TM0 efficiency read off Fig. 7(b), length) |
| cmp_lit_novack2013_ge_pd | photodetector.ge_waveguide | 17 (3-dB bandwidth ~30 / ~60 / ~50 GHz without / 360 pH / 580 pH inductor at -2 V, 0.75 A/W, 3 uA, junction C ~15 fF, fit Cpd 17 / 14 / 15 fF, Rpd ~125 ohm measured / 140 ohm fit, Ge 8 x 10 um x 500 nm, 220 nm Si, 90 nm slab, 2 um BOX) |

Per paper: chung2019a 11 components / 45 metrics; fujisawa2017 5 / 20; deng2016 4 / 23; novack2013 1 / 17.

## Fab / facility

- chung2019a: org_tower_semiconductor on all 5 fabricated-chip rows (borderline D84b: p.28 thanks named TowerJazz staff
  "for the chip fabrication and technical support"; TowerJazz also under Funding; p.3 names only "a commercial foundry
  silicon photonics process"). process_name empty (no node or flow printed). Design rows have no fab.
- fujisawa2017: fab empty ("fabricated in CMOS platform", no org; all authors Hokkaido University; D80b).
- deng2016: fab empty (passive EBL / ICP / PECVD sentence, no org; authors Peking University + MIT).
- novack2013: org_astar_ime ("fabricated at the Institute of Microelectronics (IME) ... as part of the OpSIS-IME MPW
  service", p.5); process_name "OpSIS-IME MPW service".
- No facility statements in any paper.

## Values not entered and why

chung2019a
- Fig. 1 and Table 1 rows of other works (cited, rule 3).
- MZI static extinction ratio 23.03 dB (test-structure value; the basis of the 1.23 dB IL row) and MZI FSR 550 pm.
- 1-dB optical bandwidth "much larger than 80 nm" over 1520-1600 nm (p.7): bw_1db_nm not allowed for phase_shifter.
  Also, the Fig. 4(d) point near 1520 nm sits about 1.1 dB below the maximum, so the printed bound is not fully
  supported at the band edge (noted on the row).
- dT for pi 7.4 K (Table 1): no parameter.
- Simulated thermal crosstalk (+3.2 dB vs single waveguide; 47 um minimum pitch for -30 dB, 40 um for N = 0; Fig. 3(d)):
  no phase_shifter crosstalk parameter.
- Optical crosstalk below -40 dB at 1000 nm (400 / 500 nm) vs 2550 nm (500 / 500 nm) waveguide pitch (p.3): design rule;
  pitch_um not allowed for phase_shifter.
- 2 um linear taper "less than 0.01 dB" (p.15, p.19): sub-segment of the U-turn, kept in the bend notes.
- Measured 0.099 -> 0.048 dB improved Clothoid and the projected 0.82 dB modulator loss: rest on the authors' ref. [57]
  (rule 3 / D259).
- Analytical-model values (54.2 us, 42.8 us, Appendix B), simulated rise times for N = 4 / 28 (29.8 / 44.6 us), Fig. 3(b)
  sweep points, poly-Si routing projection (1 mW), 1,000-modulator projection: model / projection or sweep points.
- 14-bend total 1.08 dB (= 14 x 0.077, arithmetic), 2 pi power 5.12 mW (Fig. 4(c), = 2 x P_pi; in notes).
- Footprint per Table 1 109 x 21 um2 kept in the notes of the 0.0023 mm2 row.

fujisawa2017
- Fig. 8 min / max bars (slopes of the 10-chip extremes) and Fig. 9 single-chip spectra (Nb = 398, 1520-1620 nm):
  notes only.
- Simulated Reff = 2 / 3 / 5 um normal and clothoid design curves (Fig. 3, Fig. 4) and the optimum ratios 68 / 60 / 50 %:
  design-space sweeps with no printed loss values; not entered as rows.
- Fig. 11 calculated transmission spectra and Fig. 12 width-tolerance curves (besides the dw = 0 checks in notes).
- Typical normal-bend loss "on the order of 0.01 dB" (p.2): cited (ref. [2]).

deng2016
- Slot width 100 nm design / 90 nm SEM: gap_nm not allowed for mode_converter (registry gap, as ou2021).
- Simulated mode-overlap ratios (> 98 % TE0, > 97 % TM0, Fig. 3), slot-taper efficiency > 99 % for cot(theta) >= 8
  (Fig. 4), +/-1 % TE0 - TM0 tolerance for +/-15 nm Wmmi / Lmmi (Fig. 6(c), p.9): sub-element or no parameter.
- Simulated efficiency curves vs L (Fig. 7(b) lines) not read.
- Efficiency differences < 4.5 % over 125 nm: in notes of the > 92 % row.

novack2013
- Group delay variation at 40 GHz -1.5 / 2.1 / 12.3 ps (from the circuit-model fit): no parameter.
- Inductor parameters (360 / 580 pH, 9.7 / 19.8 fF, ~1 ohm/GHz^0.5, fitted Cind / Rind), pad capacitance 13 fF and the
  large-inductor response peak near 35 GHz: circuit elements, notes only.
- Capacitance per unit area vs bias (Fig. 1, test structures): not entered (no per-area capacitance parameter; the
  derived 15 fF junction value is entered).

## Missing fab / facility orgs

- OpSIS (MPW access provider, fab role): novack2013 p.5 Sec. 4 "as part of the OpSIS-IME MPW service" (already
  requested by earlier batches: D422, D439, D458; harris2014 / aflatouni2015 precedent).

## Judgment calls for the auditor

(a) chung2019a bandwidth / rise / fall (10.1 kHz, 34.8 / 34.4 us) are the test MZI's output-intensity response at null
    bias (D470 removed such a value for chung2017). Kept because the paper reports 10.1 kHz as the modulator bandwidth
    in Table 1 and prints no other bandwidth; the optical-phase rise time 58.5 us (Appendix B-2) is entered as its own
    row. A first-order phase response sampled by a null-biased 0-pi MZI gives an intensity 10-90 % edge of about 0.63x
    the phase 10-90 % time, consistent with 34.8 vs 58.5 us. Delete m3-m5 if D470 is to be applied strictly.
(b) chung2019a 1.23 dB IL: basis derived (authors' ER-to-loss conversion; reproduces exactly with ideal 50:50
    splitters, an unstated assumption). Alternative author_estimate if the unstated splitter assumption counts as an
    assumed input.
(c) chung2019a fab org_tower_semiconductor as D84b borderline (staff thanked "for the chip fabrication"); TowerJazz
    alias from D912.
(d) chung2019a U-turn rows: per-180-deg loss as insertion_loss_db per_component (manganelli2017 precedent), not halved
    into bend_loss_db_per_90 (chung2017 halved simple 180-deg bends; here each U-turn is a composite of four Clothoids,
    a taper and a straight). The measured 0.077 dB averages types A and B -> population row (D165) plus two per-type
    rows with simulated values only. Wavelength 1550 nm inferred on all bend rows.
(e) chung2019a simulated comparison structures entered as design rows: single-waveguide and N = 26 phase shifters
    (values printed in text), improved type-A U-turn and four circular 180-deg bends (Fig. 6(c) labels, simulated).
    test_structure true on the fabricated modulator (characterized in an on-chip MZI test structure).
(f) fujisawa2017 platform soi_strip: "SOI" is not printed, but the Si wire (400 x 210 nm) is stated to be surrounded by
    silica (p.4); D422 / D423 emptied platforms only where no insulator was stated. Empty platform is the alternative.
(g) fujisawa2017 measured slopes: wavelength 1550 nm inferred (not printed with the values); statistic mean with
    n_samples 10 (slope of the 10-chip averages), method cutback. Simulated values read off Fig. 3 / Fig. 8 (+/- 0.0005
    dB); Fig. 12 / Fig. 13 give 0.021-0.022 dB (normal) and about 0.0016 dB (clothoid) at nominal width, noted as D417
    conflicts. Reff is not stored as a bend radius on the clothoid rows (D619); the normal bend gets R = 4 um.
(h) deng2016: one row per converter length L (rule 9); L = 2 / 3 / 5 um efficiencies read off Fig. 7(b) markers
    (600 dpi render, frame calibration, +/- 0.5 %; L = 2 um TE0 square partly hidden behind the TM0 dot). Efficiency in
    coupling_efficiency_pct per_component, method reference_structure (normalized to a strip waveguide; per-converter
    value of 10 cascaded converters, no division shown, so measured, D567). Platform soi_slot (luan2026 /
    kieninger2020 precedent; poulsen2025 used soi).
(i) novack2013: the three measured detectors share one PD design; one component row with the inductor as a condition
    (fard2016 precedent), so the once-printed 0.75 A/W and 3 uA (n_samples 3) sit on that row without a D254 conflict.
    Junction capacitance 15 fF basis measured (Table 1 marks it measured directly; p.3 derives it from the per-area
    curve). Circuit-fit Cpd / Rpd derived (D80a). Responsivity band unspecified (no wavelength printed anywhere).

## Registry gaps

- gap_nm (slot width) on mode_converter: deng2016 slot 100 nm design / 90 nm SEM (p.6). Proposed: allow gap_nm for
  mode_converter ("slot / coupling gap").
- bw_1db_nm on phase_shifter: chung2019a "1-dB optical bandwidth much larger than 80 nm (1520-1600 nm)" (p.7, Fig. 4(d)).
  Proposed definition: "optical bandwidth over which the insertion loss stays within 1 dB of its minimum".
- Thermal crosstalk on phase_shifter: chung2019a simulated minimum modulator pitch 47 um for -30 dB (p.7, Fig. 3(d)).
  Proposed: `thermal_crosstalk_db` (phase change induced in a neighbour per unit phase change, at the stated pitch).
- Temperature rise for pi on phase_shifter: chung2019a dT 7.4 K (Table 1). Proposed: `delta_t_pi_k`.
- Group-delay variation on photodetector: novack2013 -1.5 / 2.1 / 12.3 ps at 40 GHz (p.7, Fig. 7(b), model fit).
  Low priority.
