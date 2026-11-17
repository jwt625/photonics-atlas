# lit_174 batch report

Distilled 2026-11-16 under the pic-component-distill skill (Contracts v4-v7, DevLog-007 rulings through D615).
Papers: lit:chen2015, lit:chauhan2022, lit:liu2020d, lit:adar1994. Totals: 25 components, 196 metric rows.
`merge_component_staging.py data/_staging/components/lit_174 --dry-run`: +25 components, +196 metrics, 0 errors (the
one warning printed belongs to merged row cmp_lit_ni2025b_pimmwc, not this batch).

Page-1 title check: all four cached texts are their source rows' papers (titles match `sources.csv`). None is a
correction / erratum; no garbled text layer. adar1994 is a 1994 scan with a noisy text layer (Table I and the
layer-structure paragraph read from page renders: index delta 0.7 %). No component rows existed for these sources.

## lit:chen2015 - 12 components, 80 metric rows

| component | class | performance metrics |
|---|---|---|
| cmp_lit_chen2015_spiral_wg | waveguide_platform.straight | TM 2.6 / TE 6 dB/cm, cutback 0.5-3 cm, C-band average (measured) |
| cmp_lit_chen2015_ubg_p432_wc40 / wc60 / wc80 / wc100 / wc160 | reflector.bragg | Fig. 10(b) measured kappa reads 35 / 65 / 120 / 170 / 465 1/cm; wc60 also Fig. 8(a) notch ~44 dB |
| cmp_lit_chen2015_ubg_wc120 / wc140 | reflector.bragg | Fig. 10(b) kappa reads 255 / 360 1/cm (period and length not printed) |
| cmp_lit_chen2015_ubg_p438_wc60 | reflector.bragg | ER 52 dB (printed, statistic best) |
| cmp_lit_chen2015_ubg_p444_wc60 | reflector.bragg | notch ~48 dB (Fig. 8(a) read) at the printed 1549.3 nm |
| cmp_lit_chen2015_ubg_p444_wc20_4mm | reflector.bragg | 3-dB reflection width 0.09 nm (printed, best) |
| cmp_lit_chen2015_cbg_wc60_4mm | reflector.bragg | 3-dB reflection width 11.7 nm near 1548 nm |

Geometry (D153): period, grating length (mm -> um derived), 50 % duty cycle (U-SBGWs only), 220 nm Si / 3 um BOX /
2 um SiO2, 131 x 131 um2 footprint on both 4 mm rows.

Values not entered and why:
- Centre wavelength 1549.3 nm (p.11) and the C-SBGW centre near 1548 nm: `center_wavelength_nm` not allowed on
  reflector (registry gap; entered as the wavelength condition).
- C-SBGW group-delay slope -11 ps/nm (measured, p.13 Fig. 12; also the TMM design, Fig. 4): no group-delay /
  dispersion parameter (registry gap).
- Centre-wavelength shift vs period "1.7" (p.10-11), simulated delta n_eff 0.78e-3 and < 0.27 nm period correction
  (p.7), S-bend mode-mismatch reflection < -28.4 dB (simulated, p.7), simulated FDTD kappa points and the printed
  polynomial fit (Fig. 10(b)), simulated Fig. 10(a) centre wavelengths: no parameter or simulated-only side data.
- Fig. 9 stopband widths / notch depths of the W_corr series: level not stated, overlapping noise-floor-limited
  curves; not read.
- Ref. [36] (authors' CLEO 2015) 1 dB/cm TM / 2.5 dB/cm TE DUV spirals, ref. [55] 0.14 nm, ref. [56] 5 ps/nm: cited
  values (rule 3).
- GCs and Y-junction: cited designs (refs. [52], [53]), no values.

Judgment calls:
- One spiral row for TE and TM (shared waveguide design, polarization as condition); spiral width not printed.
- kappa reads: `extracted_from_figure` (naghdi2016 precedent; Eq. (4) extraction with an n_g of unstated origin noted),
  wavelength = the Fig. 10(a) measured centre wavelength (`wavelength_inferred`). Fig. 10 shows W_corr 120 / 140 nm
  points absent from Fig. 9; their rows carry no period or length (identity with the 432 nm series is only an
  inference from Fig. 10(a), noted).
- The 52 dB arrow of Fig. 8(a) ends at the 438 nm dip (deepest curve, about -53 dB): assigned to that row.
- Fab `org_university_washington` from "fabricated using eBeam lithography at the University of Washington" (p.9;
  simard2015 / eid2016 precedent).

Missing org: Washington Nanofabrication Facility (WNF), printed "University of Washington, Washington Nanofabrication
Facility (WNF)", acknowledgment p.13 (facility role, all 12 rows; already queued for the org round, D420 / D579 /
D604).

## lit:chauhan2022 - 6 components, 45 metric rows

| component | class | performance metrics |
|---|---|---|
| cmp_lit_chauhan2022_ring_r3mm_461 | resonator.ring | Q_L 1.65 M, 395 MHz, Q_i 9.5 M (derived), 0.09 dB/cm, kappa^2 ~16 % |
| cmp_lit_chauhan2022_ring_r8p9mm_674 | resonator.ring | Q_L 27.7 M, 16.1 MHz, Q_i 54.4 M (measured, critical), 0.01 dB/cm, kappa^2 1.5 %, absorption 0.17 dB/m, 14.1 pm/K |
| cmp_lit_chauhan2022_ring_r9p4mm_698 | resonator.ring | Q_L 34.4 M, 12.7 MHz, Q_i 60 M (derived), 0.01 dB/cm, kappa^2 1 % |
| cmp_lit_chauhan2022_ring_r10mm_802 | resonator.ring | Q_L 0.81 M, 460 MHz, Q_i 28.3 M (derived), 0.02 dB/cm, kappa^2 57 % |
| cmp_lit_chauhan2022_facet_461 | fiber_chip_coupler.edge | 3 dB/facet |
| cmp_lit_chauhan2022_facet_red_nir | fiber_chip_coupler.edge | 4.5 dB/facet (674 nm), 3.5 dB/facet (802 nm) |

Values not entered and why:
- 2 m coil losses 0.03 dB/cm at 698 nm and 0.08 dB/cm at 450 nm (p.6): p.2 attributes the coil losses to the
  authors' CLEO 2020 paper [28] ("losses from 2 m coils [28]"), whose title names both wavelengths, and the 450 nm
  sentence itself cites [28] (D259 / D408). Recorded in the 698 nm ring notes. Judgment call for the 698 nm value (its
  own sentence carries no citation); the audit may restore it as `author_estimate` (D80i borderline).
- Absorption-limited Q ~340 M at 674 nm (hypothetical limit, puckett2021 precedent); 5.4 MHz/mW resonance shift per
  on-chip optical power and 38.0 MHz/mW per absorbed power (no parameter for an optical-power-induced shift).
- Simulated bend-design thresholds (< 1e-4 dB/cm for R > 0.33 / 2.3 / 5.5 mm), mode areas and confinement factors
  (Fig. 2): simulated design data without a parameter.
- Fig. 6 comparison values of other platforms: cited (rule 3).

Judgment calls:
- Q_i basis per D403: 674 nm `measured` (dip to about zero, Q_i about 2 Q_L); 461 / 698 / 802 nm `derived` (regime
  fixed by the independently measured kappa^2 test structures, p.4). Losses from Q `author_estimate` (group index not
  printed, D76). 802 nm Q_i 28.3 M (text) vs 28 M (caption) noted (D417).
- `thermal_drift_pm_per_k` 14.1 derived from the printed 9.31 GHz/K at 674 nm (dlambda = lambda^2 df / c).
- Polarization left empty on all rows (the paper states the waveguides' mode content, not the measurement
  polarization).
- Fab `org_honeywell` borderline (D84b; isichenko2023 / puckett2021 precedent): acknowledgment thanks Honeywell staff
  for upper-cladding deposition and annealing of devices; no first-person fabrication sentence, UCSB not entered.

Missing orgs: none.

## lit:liu2020d - 2 components, 31 metric rows

| component | class | performance metrics |
|---|---|---|
| cmp_lit_liu2020d_dual_mode_mmi | splitter.mmi | measured 1530-1590 nm averages: EL < 0.44 / 0.76 dB, XT < -21.7 / -20.5 dB, imbalance < 0.12 / 0.9 dB (TE0 / TE1); simulated EL 0.23 / 0.39 dB at 1550 nm, 0.24 / 0.63 dB averages, XT < -22.9 dB, imbalance < 0.04 / 0.4 dB, 0.01 dB at L = 86.5 um, +/-25 nm width tolerance EL < 0.5 dB / XT < -25 dB |
| cmp_lit_liu2020d_mmi_unoptimized_design | splitter.mmi (design) | simulated comparison device without tapers: average EL 2.16 / 4.12 dB |

Geometry: MMI 5 x 86.5 um, 5.2 um tapers 2.24 um wide at the MMI, 1 um access waveguides, input pitch 2.76 um
(derived, 1 um + 1.76 um gap = 2 y_in), 220 nm / 2 um BOX / 1.2 um SiO2, footprint 432.5 um2 (derived).

Values not entered and why: mode-excitation power ratios 95.9 / 94.2 % and 65.9 / 33.8 % (simulated, no parameter);
input offset y_in 1.38 um (no parameter; in notes and in the derived pitch); Fig. 5 u = 3 / 5 designs (figure-only
simulated curves); 0.26 dB difference of the two modes' average powers (no parameter).

Judgment calls: platform `soi_strip` from the Fig. 1(c) cross-section (no slab drawn); imbalance kept as printed
although p.4 says only the lower arm was characterized (Fig. 8 shows both arm outputs per input; noted);
crosstalk is intermodal (condition); fab `org_huazhong_university_of_science_and_technology` ("We fabricated", "same
as our previous work [15]", all authors at one HUST laboratory; D80b / D84a). Missing orgs: none.

## lit:adar1994 - 5 components, 40 metric rows

| component | class | performance metrics |
|---|---|---|
| cmp_lit_adar1994_ring_r30mm | resonator.ring | finesse 132, T_min 0.21 (6.78 dB derived), 8.3 MHz, ring loss TE 0.85 dB/m, TM 1.1 dB/m, FSR 1.1 GHz |
| cmp_lit_adar1994_ring_r20mm | resonator.ring | finesse 108, 13.47 dB, 15.2 MHz, 1.22 dB/m, 1.65 GHz |
| cmp_lit_adar1994_ring_r10mm | resonator.ring | finesse 68.3, 11.14 dB, 48.2 MHz, 4.72 dB/m, 3.3 GHz |
| cmp_lit_adar1994_ring_r5mm | resonator.ring | finesse 4.7, 1.25 dB, 173 dB/m, 6.6 GHz |
| cmp_lit_adar1994_bend_series | waveguide_platform.bend | Fig. 3 net bend loss reads, TE / TM at R = 5, 10, 20, 30 mm |

Values not entered and why:
- R = 5 mm resonance width: Table I prints 1.46 in the MHz column, FSR / finesse gives 1.40 GHz (unit inconsistent).
- Earlier own results (6 cm ring, finesse 46, 2.6 dB/m; 0.1-0.25 dB fiber-to-fiber through 6 cm, ref. [9]) and other
  groups' ring losses: cited (rule 3). Assumed propagation loss 0.8 / 1.0 dB/m (TE / TM) is an assumption used for
  Fig. 3, kept in notes. Fiber grating laser, isolator, WDMs: setup equipment (rule 13).

Judgment calls:
- Ring losses `author_estimate`: Loss = 4.34 / (F R (1 + y)) with the smaller y root always chosen (assumed branch,
  D403 analogue); dB/m -> dB/cm with the basis kept (D256a). The printed formula with Table I F and T_min gives about
  0.80 dB/m (R 30) and 4.06 dB/m (R 10) instead of the printed 0.85 / 4.72 dB/m: printed values kept, noted (D417).
- Resonance widths `author_estimate`: traces are recorded against time (arb. units) and each width equals the stated
  FSR / finesse; FSRs `author_estimate` (origin not stated).
- Net bend loss as one array-level `waveguide_platform.bend` row (D165) with `prop_loss_db_per_cm` per radius and
  polarization (bend-row convention, D81), `extracted_from_figure` off the scanned log axis (+/-20 %).
- Wavelength 1558 nm on all rows (source "around 1558 nm", D393). Fab empty (no fabrication statement; AT&T Bell
  Laboratories authors). Missing orgs: none.

## Registry gaps (skipped value + locator + proposed definition)

1. `center_wavelength_nm` on reflector: chen2015 1549.3 nm (p.11), C-SBGW near 1548 nm (p.13). Same definition as
   the existing parameter (peak / centre of the stopband). Also listed in D433 / D538.
2. `group_delay_slope_ps_per_nm` on reflector: chen2015 C-SBGW -11 ps/nm measured (p.13 Fig. 12) and designed
   (p.8 Fig. 4). "Average slope of the reflection group delay over the passband, sign as printed" (D574 family).
3. `corrugation_width_nm` on reflector: chen2015 W_corr 20-160 nm (p.8, Figs. 8-11). "Sidewall corrugation
   amplitude (Wmax - Wmin) / 2 as defined by the source" (D540 "corrugation depth").
4. `min_bend_radius_um` and `gap_nm` on reflector: chen2015 spiral R0 15 um and 2 um spiral spacing (p.6-7) (D541).
5. Optical-power-induced resonance shift (MHz/mW of on-chip power): chauhan2022 5.4 MHz/mW (p.6 Fig. 5(b)).
6. Absorption-limited Q (`q_absorption`, D430 candidate): chauhan2022 ~340 M at 674 nm (p.6).
7. Mode-excitation power fraction (%): liu2020d 95.9 / 94.2 % (p.3, simulated); low priority.
