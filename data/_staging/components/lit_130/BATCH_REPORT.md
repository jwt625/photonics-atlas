# lit_130 batch report (distill, 2026-11-14)

Papers: wang2023, xia2024, zhao2025b, li2025b, wang2023a, yokokawa2022 (family amplifier / laser /
frequency converter). Totals: 17 components, 123 metric rows. Validator
(`merge_component_staging.py data/_staging/components/lit_130 --dry-run`): 0 errors (one warning on the
already-merged row `cmp_lit_ni2025b_pimmwc-m18`, not this batch).

Identity check: every cached text is the paper of its source row (page-1 title and authors match), none is a
correction / erratum. wang2023 `garbled_text_layer` covers only p.8 (reference list); values come from the clean
pp.1-7 text and were checked on the page renders (pp.5-6). li2025b (lit) is the Nanophotonics 2025 III-V / TFLN
laser paper, not the pilot `eo:li2025b`. No supplement is cached for any paper (wang2023, xia2024 cite Supporting
Information for the film study, the threshold curve and the fabrication).

## wang2023 (4 components, 22 metrics)

- `edwa_spiral_4p6cm` amplifier.rare_earth (10): internal net gain 6.27 dB at 1533 nm and 3.56 dB at 1550 nm
  (80 mW bidirectional 1480 nm pump, -45 dBm signal; derived, D166), 1.363 dB/cm (Table 1, derived), net-gain
  span > 40 nm (1520-1560 nm, derived), length 4.6 cm, footprint 0.9 x 0.9 mm2, GeSbS 2 um x 235 nm (SEM),
  PMMA 0.7 um, BOX 3 um.
- `gesbs_er_waveguide` straight (7): background loss 1.05 dB/cm at 1640 nm (cutback), straight 0.865 dB/cm
  (cutback, 1640 nm inferred), Er absorption only 2.20 / 1.05 dB/cm at 1533 / 1550 nm (derived by subtraction),
  geometry, min bend radius 100 um.
- `gesbs_spiral_bends` bend (3): about 0.238 dB/cm average spiral bending loss (radii 100-445 um), 3.6 cm.
- `butt_facet` fiber_chip_coupler.edge (2): 3.75 dB / 3.96 dB per facet at 1533 / 1480 nm (average, cutback).

Not entered: signal enhancement 21.22 / 13.22 dB (component notes; net gain rows carry the device); simulated
overlap 30.2 / 30.9 %; GeSbS < 0.2 dB/cm and damage threshold (cited ref. [30]); < 0.6 dB/facet expectation
(cited ref. [37]); Er doping 4.9e20 cm-3 and PL / lifetime study (no parameter; sample films, not components);
gain saturation above -20 dBm signal (no compression point printed); Table 1 rows of other works.
Fab / facility: empty (passive device-fabrication text; authors at Sun Yat-sen University, Peng Cheng Laboratory,
South China Normal University). No missing orgs.
Judgment calls: Er-absorption-only losses stored as `prop_loss_db_per_cm` with the condition saying so (total
loss is not printed separately); 0.865 dB/cm and 0.238 dB/cm wavelength inferred 1640 nm from the paragraph;
bend loss kept per cm of spiral on a `waveguide_platform.bend` row (D81 kim2025 precedent); gain bandwidth `gt` 40
with the note that the data end at the span limits.

## xia2024 (4 components, 19 metrics)

- `wopo_pulley_gap650` frequency_converter.other (2): wOPO threshold as low as 8.1 mW (measured; conclusion
  8.13 mW), conversion efficiency 0.12 % (11.3 uW at 9.4 mW estimated on-chip pump, author_estimate).
- `wopo_pulley_gap600` frequency_converter.other (1): 2.0 % (308 uW at 15.4 mW, author_estimate).
- `ring_pulley_gap650` (Device II) and `ring_straight_gap350` (Device I) resonator.ring (8 each): Q_L about
  (5-7)e5 measured, Q_0 about (1-2)e6 author_estimate (D403), R 100 um, RW 2.5 um, H 800 nm, bus 1.18 um, gap
  650 / 350 nm, BCB 3 um.

Not entered: OPO sideband span 1250-2130 nm (99 THz) and sideband pairs 1267 / 2003 nm, 1314 / 1895 nm (no
parameter for an OPO signal-idler span; `tuning_range_nm` is not allowed on frequency_converter); OPO output
powers 11.3 / 308 uW (no converter output-power parameter, D514); calculated threshold ratios 0.90 / 1.40 /
1.68 / 1.51 / 1.07 and simulated Qc / dispersion (model values); RW 2.4 / 2.6 / 2.7 um sideband-tuning devices
(no metric); gap 700 nm device (no metric); material n0 / n2 (cited); 4.5 W intracavity power.
Fab: org_sun_yat_sen_university on the three gap-series rows (p.4 "we fabricated three pulley-coupled devices",
all authors at SYSU, D72); Device I ring row empty (passive "also fabricated", D515). No facility. No missing orgs.
Judgment calls: Device II (gap 0.65 um, 9.4 mW pump in Fig. 2(c)) and the 650 nm gap device of p.3 / Fig. 4(b)
treated as one design; 8.1 mW threshold tied to Device II by paragraph context (Supp. Fig. S5 not cached); the
Q range stated once "for both devices" entered on both ring rows; gap_nm / radius not allowed on
frequency_converter, so geometry sits on the resonator rows (D396 cross-notes).

## zhao2025b (2 components, 27 metrics)

- `dfb_array_8ch_flipchip` laser.dfb (23): 8 channels, spacing 398.719 GHz / 2.273 nm (linear fit), max
  deviation 0.09 nm (1.579 GHz), wavelengths 1294.35-1310.94 nm, SMSR > 50 dB (array at 110 mA; unit 25-60 C),
  threshold < 15 mA, about 4 ohm, 0.368 W/A (derived from mW/mA), > 80 mW at 250 mA, divergence 25.8 x 30.1 deg
  (110 mA) and 26.3 x 29.5 deg (150 mA), simulated 25.2 / 30.7 deg, Lorentzian linewidth 3.28 MHz at 150 mA,
  RIN -138.7 to -135.3 dB/Hz, drift 89.9 pm/K (Fig. 9(c) label), current shift 2.44 nm (50-250 mA), pitch 250 um,
  length 500 um.
- `dfb_unit_psideup` laser.dfb (4): SMSR > 50 dB, 90.7 pm/K, current shift 3.38 nm, about 68 mW at 250 mA
  (Fig. 10(c) read).

Not entered: 28 % junction-temperature / thermal-resistance reduction and 20 % power gain (relative values; no
absolute thermal resistance printed), simulated 4.08 C difference, APS single-mode yield 90 % vs 13 % (simulated
design statistic), p-side-up threshold (Fig. 10(c) inset too coarse), Fig. 1 architecture (cited).
Fab / facility: empty (passive fabrication and bonding text; authors at Nanjing University incl. its Tongding joint
lab, China Unicom Nanjing Branch, Jiangsu University of Science and Technology). No missing orgs.
Judgment calls: Fig. 9-10 flip-chip "laser array unit" values kept on the flip-chip array row (same chip design,
condition names the unit); beam-divergence axes assigned from the Fig. 13 curves (horizontal = narrower curve),
not printed in the text; simulated pair left unassigned (first / second value); RIN printed range kept with a D417
note (Fig. 15 per-channel maxima read about -136 to -143 dB/Hz); current-induced shift entered as
`tuning_range_nm` (chowdhury2024 / heermeier2025 precedent).

## li2025b (4 components, 19 metrics)

- `dfb_sil_tfln` laser.sil (6): threshold 150 mA, 4.0 mW fiber-coupled at 700 mA, 1559.0 nm, SMSR > 50 dB,
  intrinsic linewidth 11.0 kHz locked / 1.0 MHz free-running (pi x white-noise floor, derived).
- `tfln_sil_ring` resonator.ring (5): loaded Q 3e5 (1559 nm inferred), LN 600 nm, 320 nm etch, BOX 4.7 um,
  SiO2 0.6 um.
- `vernier_ring_laser` laser.tunable (5): threshold 110 mA, 0.43 mW fiber-coupled, 44 nm tuning 1533-1577 nm,
  SMSR > 40 dB over the range, about 200 kHz free-running linewidth.
- `si_vernier_rings` resonator.ring (3): loaded Q 4e4 (one value for both rings), FSR 215 / 208 GHz
  (author_estimate, design-or-measured not stated).

Not entered: 6.7 dB chip-to-fiber coupling loss and on-chip powers 18.7 / 2.01 mW (the sentence cites the
authors' ref. [31]; rule 3 / D259, judgment call); frequency-noise floors 0.33 MHz2/Hz and 3.5 kHz2/Hz (no
parameter; linewidth rows carry them); kappa L = 3 design (grating length not stated, no kappa_per_cm); Si-TFLN and
III-V/Si tapers (simulated mode images only, no values); phase shifter (no values).
Fab: org_ucsb + org_university_of_rochester on all rows (author contributions name nine fabricators at the two
universities, D80b / D395). Facility: org_ucsb_nanofabrication_facility, org_cornell_nanoscale_facility (both
"performed at" statements). Staff thanks for fabrication help name no org (not entered). No missing orgs.
Judgment calls: platform `other` for the III-V/Si/TFLN lasers and the Si rings, `lnoi_rib` for the TFLN ring;
TFLN ring and Si ring Q entered `measured` although no trace is shown (stated device values, D167 analogue; the
auditor may prefer author_estimate per D544); abstract "continuous" vs text "coarse" tuning noted.

## wang2023a (1 component, 23 metrics)

- `qd_lcdfb` laser.dfb (23): > 100 mW single-mode output 25-85 C, threshold 39.14 mA and slope 0.242 W/A at 55 C
  (best), SMSR 55.7 / 62.0 / 62.4 dB at 25 / 55 / 85 C (300 mA) and 62.6 dB at 85 C / 450 mA, lasing
  1339.4 / 1342.2 / 1344.9 nm, 90 pm/K, intrinsic linewidth 1.62 kHz (55 C, 250 mA), about 20 kHz (25 C),
  8.22 kHz (85 C, 400 mA), averaged RIN -166 / about -160 / -163 dB/Hz, cavity 1500 um, ridge 2.1 um, etch
  1500 nm, period 203 nm, duty about 0.5, kappa about 10 /cm (author_estimate from kappa L about 1.5).

Not entered: alpha factor 0.34 (same-wafer FP lasers, no laser metric for them), Ith / slope variation < 9 mA /
< 0.012 W/A, threshold current density 1243 A/cm2, critical feedback -14 / -11 / -8 dB, current tuning
0.0087 nm/mA, HR 93 % / AR < 0.1 % facet reflectivities (no laser parameter), QD density / PL width (material),
Table 1 rows of other works.
Fab / facility: empty (passive growth / fabrication text; authors at the Institute of Semiconductors CAS / UCAS and
Zhejiang University / Zhejiang Lab). No missing orgs.
Judgment calls: grating etch 50 nm (process text) vs 60 nm (design sentence) conflict left in notes, no
etch_depth row for the grating; platform `gaas`.

## yokokawa2022 (2 components, 13 metrics)

- `soa_dfb` laser.soa_dfb (9): > 200 mW at 20 C and > 100 mW at 80 C (500 mA), threshold about 50 mA (temperature
  not stated), 1307 / 1312 nm at 20 / 80 C, SMSR > 40 dB 20-80 C, FWHM linewidth < 500 kHz (6 samples, 50 mW,
  up to 50 C), RIN < -150 dB/Hz with feedback up to -25 dB, length 1 mm.
- `soa_dfb_ssc_series` laser.soa_dfb (4): far-field FWHM about 27.8 / 20.1 deg (V / H, width 1, no SSC) and
  18.8 / 11.7 deg (width 0.2), Fig. 5 reads.

Not entered: aging 15 samples about 82-91 mW over 700 h at 80 C / 300 mA (no lifetime parameter; notes), Fig. 9
power points (current not stated), feedback tolerance about -25 dB (no parameter), 20 % amplification design
statement, AR < 0.1 %.
Fab / facility: empty (passive text; all authors at Lumentum Japan, alias of org_lumentum exists). No missing orgs.
Judgment calls: RIN bound kept as printed with a D417 note (Fig. 7 peak about -147.6 dB/Hz at -25 dB feedback);
far-field values on a separate SSC-series row because the headline laser's SSC width is not stated (D159 / D165).

## Registry gaps (proposed)

- `opo_span_nm` (frequency_converter): wavelength span between the generated signal and idler of an OPO
  (xia2024 1250-2130 nm at 1575 nm pump, p.4 Sec. 2.3 / Fig. 3(b)); or allow `tuning_range_nm` on
  frequency_converter.
- `output_power_mw` on frequency_converter (D514 candidate; xia2024 11.3 / 308 uW, p.3 Sec. 2.2).
- `feedback_tolerance_db` (laser): critical external feedback level before coherence collapse (wang2023a
  -14 / -11 / -8 dB, p.7; yokokawa2022 about -25 dB, p.3), previously deferred in D77 / D81.
- `threshold_current_density_a_per_cm2` (laser, D431 candidate): wang2023a 1243 A/cm2 (p.7 Table 1).
- `linewidth_enhancement_factor` (laser): wang2023a alpha 0.34 (p.2).
