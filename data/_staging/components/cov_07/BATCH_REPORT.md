---
title: cov_07 batch report (Kerr soliton microcombs, SiN phased array)
date: 2026-11-07
batch: cov_07
contract: pic-component-distill v4-v6
validation: merge_component_staging.py --dry-run, 0 errors (+38 components, +145 metrics)
---

# cov_07 batch report

Sources: `lit:dutt2018`, `lit:liu2018a`, `lit:liu2020a`, `lit:poulton2016`, `lit:raja2019`, `lit:shen2020`,
`lit:xiang2021`. No existing rows in `data/components/` for any of them. Page-1 titles match the registry titles;
dutt2018, liu2018a, liu2020a, raja2019, shen2020 and xiang2021 are arXiv versions of the journal papers (same works,
D430 / D433; shen2020 and xiang2021 arXiv titles differ slightly from the journal titles). No erratum-only file.

| paper | components | metrics | fab_org_ids | facility_org_ids |
|---|---|---|---|---|
| dutt2018 | 4 | 20 | empty (passive fabrication sentence) | org_cornell_nanoscale_facility |
| liu2018a | 5 | 25 | org_epfl | org_center_of_micronanotechnology |
| liu2020a | 4 | 10 | org_epfl; org_purdue_university | org_center_of_micronanotechnology |
| poulton2016 | 7 | 32 | org_suny_polytechnic_institute | none |
| raja2019 | 9 | 31 | org_epfl (Si3N4 parts) | org_center_of_micronanotechnology |
| shen2020 | 5 | 9 | org_epfl; org_freedom_photonics | none |
| xiang2021 | 4 | 18 | org_epfl; org_ucsb | none |

## Per paper

### dutt2018 (On-chip dual-comb source)
- Rows: rings R1 / R2 (`resonator.ring`: radius, width, height, gap, BOX, Q > 6e5, mode linewidths 230 / 310 MHz),
  Pt microheater (`phase_shifter.thermo_optic`: rise 24 us, fall 22 us, width, thickness), dual comb (`laser.comb`:
  repetition rates 451.4 / 452.8 GHz, one row for the two-ring source, R1 / R2 in condition).
- Q > 600,000 and the 230 / 310 MHz linewidths are stated without a shown measurement: `author_estimate` (D460).
- Not entered: comb span 51 THz (no parameter), RF beat-note linewidth 10 kHz and spacing 1.12 GHz, the Fig. 4 device
  (1 um radius difference, 8.6 GHz beat spacing only), heater-to-waveguide gap (not stated as such; 3 um of cladding).
- Fab empty: "fabricated using a process similar to" refs. 47 / 50 (passive, D80b). Facility: Cornell NanoScale
  Facility. Missing org: Cornell Center for Materials Research Shared Facilities (p.6 Acknowledgements).

### liu2018a (Ultralow-power soliton microcombs)
- Rows: 88 GHz ring and its soliton comb, 99 GHz ring and its soliton comb, double-inverse nanotaper edge coupler.
- 88 GHz ring: loaded linewidths 30.3 / 28.7 MHz (measured), kappa_0 23.3 / 17.3 MHz and Q0 > 8.2e6 / 10.7e6
  `author_estimate` (under-coupling stated, not shown, D403), TE00 / TM00 FSR.
- 99 GHz ring: the 1621.8 nm resonance is critically coupled with the dip near zero in the Fig. 3(a) render, so its
  kappa_0 13.7 MHz is `measured` (D463); histogram most probable kappa_0 13-14 MHz and Q0 > 15e6 entered as
  `statistic: typical`, n_samples 8, `author_estimate`.
- Combs: repetition rates 88 / 99 GHz (rounded as printed), parametric oscillation onset about 1.7 mW (chip input),
  pump-to-comb efficiencies about 1.5 % / 1.7 % (`author_estimate`, operating points ambiguous, see notes).
- Coupler: 40 % fiber-chip-fiber (measured), 63 % per facet (derived, square root).
- Not entered: D2 values (dispersion, D81), single-soliton access powers 48.6 / 9.8 mW (operating points; no
  parameter), power per line 20 uW, the second 99 GHz sample of Fig. 5 (same design, FSR repeats), taper-width
  statement tied to ref. 43.
- Fab org_epfl ("our fabrication process" D84a + CMi D83c); LIGENTEC appears only as one author's affiliation.
  kappa_0 at 1558 nm: text 23.3 MHz vs Fig. 1(b) caption 23.2 MHz (text value entered, conflict in notes).

### liu2020a (Monolithic piezoelectric control)
- Rows: 191 GHz ring (FSR, Q0 > 15e6, about 1 dB/m loss, cladding 2.4 um), AlN actuator (`phase_shifter.other`:
  0.127 pm/V derived from 15.7 MHz/V at 1556 nm, 3.3 pF calculated, mechanical modes 246 kHz and about 17 MHz),
  soliton comb (191 GHz, `author_estimate`: stated not directly measurable), facet coupling 60 % per facet.
- Q0 > 15e6: resonances stated critically coupled but no dip shown (`author_estimate`, D403).
- Not entered (registry gaps, see below): leakage < 2 nA / power < 300 nW at 150 V, resonant tuning 219 and
  133 MHz/V (no pump wavelength for a pm/V conversion), flat S21 to about 800 kHz, locking bandwidth 0.6 MHz,
  soliton existence range about 400 MHz.
- Fab org_epfl + org_purdue_university (author contributions name EPFL and Purdue fabricators, D80b two orgs).
  Missing org: Birck Nanotechnology Center, Purdue University (p.6 Acknowledgments; facility).

### poulton2016 (Large-scale SiN phased arrays)
- Rows: IR OPA 4 x 4 mm (FWHM spot 0.021 deg, SLSR about 10 dB, overall -13.6 dB derived, antenna emission loss 9 dB,
  design geometry), visible OPA 0.5 x 0.5 mm (0.064 / 0.074 deg, SLSR 8.7 dB, 2 um pitch), 1x1024 MMI tree (1.3 dB
  MMI and 0.5 dB linear loss shares), three MMIs (large: 0.04 dB sim / < 0.1 dB meas; small: 0.27 sim / 0.35 meas;
  visible: 0.03 dB sim), IR inverse-taper edge coupler (2.8 dB loss-breakdown term, 6.5 um lensed fiber).
- Loss-breakdown terms `author_estimate` + `loss_breakdown` (origin not stated). MMI "insertion loss" of a 1x2 entered
  as `excess_loss_db` (rule 6).
- Not entered: main-beam power 400 mW (no output-power parameter on free_space_emitter), grating-lobe angles,
  theoretical diffraction limits, beam size at 10 m, visible edge coupler (no performance number).
- Fab: "fabricated at the CNSE in the SUNY Polytechnic Institute" (p.1) -> org_suny_polytechnic_institute. Missing
  org: College of Nanoscale Science and Engineering (CNSE), SUNY Polytechnic Institute (p.1) as a child unit.

### raja2019 (Electrically pumped soliton microcomb)
- Rows: commercial InP FP laser diode (`laser.other`: 1530 nm, 35 GHz mode spacing, about 100 mW, < 1 W electrical,
  Gaussian 60 MHz / short-time 2 MHz), rings 1.02 THz / 149 GHz / 88.6 GHz / 92.4 GHz (`resonator.ring`), SIL laser
  on the 1.02 THz ring (`laser.sil`: 186 kHz Gaussian, 0.7 kHz Lorentzian), SIL combs at 149 GHz and 92.4 GHz
  (`laser.comb`, `channel_spacing_ghz` per D83b; 11 mW fiber output for 92.4 GHz), butt-coupled path
  (`chip_chip_coupler.butt`: about 6 dB overall, 6.6 dB / 22 % at the soliton operating point, scope device_total).
- Q0 values (6e6, 6.5e6, 8.2e6) extracted on highly under-coupled resonators: `author_estimate` (D403); 92.4 GHz
  loaded linewidth about 110 MHz (typical), Q_L 1.8e6 derived, kappa_0 < 30 MHz `author_estimate`.
- Not entered: Fig. 4(c) soliton beat (201 kHz / 1 kHz) - text attaches it to the 149 GHz soliton, figure to the
  92.4 GHz device (D159, bound in component notes); theoretical 0.1 kHz linewidth, > 30 GHz locking range and 0.62 mW
  threshold (calculations with assumed / manufacturer inputs); backscatter rate 118 MHz; D2 values; breather 490 MHz.
- Fab org_epfl on all rows with the Si3N4 chip (J.L. designed and fabricated, CMi); laser diode vendor not named.

### shen2020 (Integrated turnkey soliton microcombs)
- Rows: Freedom Photonics DFB (`laser.dfb`: threshold 50 mA, 120 mW, 0.24 W/A, WPE > 20 % `author_estimate`,
  1554.5-1556.5 nm), one resonator row for the Fig. 1(B) resonance (Q0 16e6, device not identified), turnkey combs at
  40 / 19.787 / 15.056 GHz (`laser.comb`).
- DFB platform empty (material not stated; D422 / D423).
- Not entered: current tuning about -1.4 GHz/mA (D83g), frequency-noise suppression about 30 dB, locking bandwidth
  5 GHz (estimated), turnkey success probabilities, launched power up to 30 mW.

### xiang2021 (Laser soliton microcombs on silicon)
- Rows: heterogeneous InP/Si DFB (`laser.heterogeneous`: threshold 64 mA, 8 mW in fiber, about 20 mW on chip
  `author_estimate`, SMSR 60 / 57 dB, free-running linewidth about 60 kHz, 238 nm pitch, 1.8 mm gain section), ring
  in the final chip (FSR 100 GHz, most probable kappa_0 29 MHz, Q0 about 6.8e6), passive reference ring (19.5 MHz,
  10.2e6; `test_structure`), laser soliton comb (100 GHz, calculated threshold about 3 mW `simulated`, pump-line
  linewidth about 25 Hz, neighbor lines 200-300 Hz).
- Not entered: phase tuner (no performance number), Si-Si3N4 taper (geometry only: 400 -> 200 nm on 269 nm Si),
  AFM roughness 0.27 nm, soliton-crystal 200 GHz state, on-chip pump > 16 mW.
- Passive-ring kappa_0: text 19.5 MHz vs Supp. Fig. 2 caption 19 MHz (text value entered, conflict in notes).

## Judgment calls

1. liu2018a, raja2019, shen2020: rings and the combs they host are separate rows (D396); dutt2018 keeps one comb row
   for the two-ring dual comb (one physical source), with per-ring repetition rates.
2. Soliton comb line spacing: `repetition_rate_ghz` where the paper says repetition rate of a soliton comb (dutt2018,
   liu2018a, liu2020a, shen2020, xiang2021); `channel_spacing_ghz` for raja2019, which calls 149 GHz a mode spacing
   (D82g / D83b).
3. Histogram "most probable value" entered as `statistic: typical` (giewont2019 precedent): liu2018a 99 GHz, raja2019
   92.4 GHz, xiang2021 final and passive rings.
4. liu2020a AlN actuator as `phase_shifter.other` (piezoelectric stress-optic actuator) rather than `mems`.
5. poulton2016 tree loss split into the MMI share (`excess_loss_db` 1.3) and the linear share (`insertion_loss_db`
   0.5) on one `splitter.other` row.
6. shen2020: packaging by UCSB / Caltech authors not added to fab_org_ids on the comb rows (packaged vs bench
   measurements not separable).

## Questions for the coordinator

1. raja2019 Fig. 4(d) ring (Q0 8.2e6, FSR 88.6 GHz, D2/2pi 1.10 MHz) repeats the liu2018a 88 GHz device numbers
   (same group; raja2019 cites liu2018a as ref. 26 in nearby sentences, not in the Methods line). Kept under D408;
   delete the raja2019 row as reproduced own work instead?
2. liu2018a 99 GHz histogram: 8 under-coupled samples with different gaps. Does a gap series fix the regime as in
   lee2012 (D425, `measured`), or stay `author_estimate` (D403) as entered?
3. shen2020 comb rows: add org_ucsb and org_caltech as fab orgs for the butterfly packaging (D399 assembly rule), given
   the paper does not say which measurements were packaged?
4. xiang2021 final-chip ring: fab EPFL + UCSB (UCSB back-end processing degrades Q) entered; keep EPFL only?
5. liu2020a 191 GHz repetition rate (`author_estimate`, stated not directly measurable): move to `channel_spacing_ghz`
   or keep?

## Registry gaps (skipped value + locator + proposed definition)

- `tuning_efficiency_mhz_per_v` (phase_shifter, resonator): liu2020a 219 / 133 MHz/V at 18.308 / 18.322 MHz drive
  (p.6) - resonance shift per volt in frequency units, drive frequency in condition.
- `power_consumption_w` widened to phase_shifter: liu2020a < 300 nW at 150 V (p.2).
- `output_power_mw` widened to free_space_emitter: poulton2016 400 mW main beam (p.3) - optical power in the main lobe.
- `comb_span_thz` (laser): dutt2018 51 THz / 400 nm (p.2), deferred in D81 (repeat candidate).
- `rf_linewidth_hz` (laser): dutt2018 10 kHz dual-comb beat (p.3), already a D431 candidate.
- `locking_bandwidth_ghz` (laser.sil / comb): shen2020 5 GHz estimated (p.3), raja2019 > 30 GHz theoretical (p.5).
- `rms_roughness_nm`: xiang2021 0.27 nm AFM wafer surface (p.4), already a D432 candidate.

## Missing organizations (name as printed + locator)

- Cornell Center for Materials Research Shared Facilities - dutt2018 p.6 Acknowledgements (facility).
- Birck Nanotechnology Center at Purdue University - liu2020a p.6 Acknowledgments (facility; also a D431 candidate).
- College of Nanoscale Science and Engineering (CNSE), SUNY Polytechnic Institute - poulton2016 p.1 (fab site; parent
  org_suny_polytechnic_institute used).
