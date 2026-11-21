# lit_236 batch report

Distilled 2026-11-20. Papers: lit:raptakis2021, lit:luo2015, lit:komatsu2021, lit:fowler2023, lit:poulton2018.
Page-1 titles match the source rows; no correction / erratum; no garbled text layer.
Totals: 23 components, 103 metric rows. `merge_component_staging.py --dry-run`: 0 errors, no warnings on batch rows.
Selected because other papers cite them in benchmark tables; only values each paper reports for its own devices are entered.

## raptakis2021 (JLT 2021, 3D PolyBoard polymer OPAs): 10 components / 48 metrics

- Rows: end-fire waveguide antenna element (simulated 12.7 deg FWHM, 3.2 x 3.2 um); six OPAs, one per fabricated design
  (single-layer 1 x 4 and 2-layer 2 x 4 at 6 / 8 / 10 um lateral pitch; vertical pitch 7.2 um): measured azimuth /
  elevation beam FWHM at 1563 nm (Fig. 15), measured main-to-grating-lobe spacing (10.7 deg lateral at 8 um, about
  9.9 deg vertical at 6 and 8 um), demonstrated scan spans (-6..+6 deg azimuth, -4..+4 deg elevation, Fig. 18),
  simulated 14.0 deg and 3 / 6 / 10 dB clearances 10.8 / 7.6 / 2.8 deg (4 elements, 6 um) on the 2 x 4 6 um row,
  simulated 2.3 dB main / grating ratio on the 1 x 4 8 um row; lateral 1:4 and 1:2 MMI couplers (typical imbalance
  <= 0.2 dB, TE and TM); thermal phase shifter (20 ohm, about 15 ms reconfiguration time).
- Not entered: PolyBoard 0.7 dB/cm (platform value with refs. [36]-[38]); vertical MMI coupler insertion loss about
  1 dB (previous test-structure measurements, ref. [32]; rule 3), so the vertical MMI (1350 um x 10.4 um) has no row
  (geometry only, in the 2 x 4 notes); PIC-level average lower-layer loss about 2 dB and the 3 dB upper-limit /
  about 30 % throughput estimate (stated once for the three 2-layer PICs, D254; throughput has no parameter); 1.4 dB
  worst-case power deviation (estimate; power_uniformity_db not allowed on free_space_emitter); phase-shifter drive
  currents (no mA parameter; p.8-9 print 16 / 20 mA for pi, p.11 prints 16 / 20 mA for 2 pi: conflict, so no P_pi
  computed); experimental 3 dB clearance "much larger than 8 deg, smaller than 12 deg" (no single number); BPM
  crosstalk 11.6 % / 6.6 deg at 7 um (simulated generic pair, pitch not fabricated); earlier few-ms reconfiguration
  (ref. [47]).
- Fab / facility: fab empty. "we design and fabricate" with authors at NTUA / ICCS, Fraunhofer HHI and Optagon
  Photonics; no sentence names the fabricating org (D154). No facility statement. Missing org (affiliation only, no
  fab / facility role): Optagon Photonics (p.1 author footnote).

## luo2015 (OE 2015, 2150 nm InAs/InGaAs/InP QW FP lasers): 5 components / 19 metrics

- Rows: population row for the cavity-length series (D165: > 160 mW per facet CW for each length, n = 4; lasing
  range 2142-2154 nm) and one row per cavity length 0.8 / 1.5 / 2.2 / 3.0 mm (rule 9). Thresholds 172 mA (0.8 mm) and
  302 mA (3 mm) derived from printed Jth x 30 um x length (D431 precedent; both agree with the Fig. 2(a) onsets);
  1.5 mm: 1350 mW peak pulsed (printed 1.35 W, derived) and 0.24 W/A; 3 mm: 2154 nm, T0 50 K (20-70 C);
  0.8 / 1.5 / 2.2 mm peak wavelengths read off Fig. 4(b) (2143 / 2148 / 2152 nm, +/-1 nm).
- Not entered: Jinf 180.8 A/cm2 (90.4 per QW) and Jth 718 / 336 A/cm2 as such (no threshold-current-density
  parameter); internal efficiency 37.6 % and internal loss 8.2 /cm (rest on assumed R = 0.35; no parameters);
  T1 132 K (no parameter); maximum operating temperature 100 C (no parameter); PL uniformity values (material).
- Conflict (D417): text says the peak goes 2154 -> 2142 nm from 3 to 1.5 mm; Fig. 4(b) shows about 2148 nm at 1.5 mm
  and about 2143 nm at 0.8 mm. 2142 nm is not put on the 1.5 mm row; the abstract range 2142-2154 nm is on the
  population row.
- Fab: org_institute_of_semiconductors_chinese_academy_of_sciences (borderline): first-person growth sentence "we use
  500 C to grow both the InAs QW layers and ... barriers" (p.3), all authors at that institute; ridge processing is
  passive. No facility statement.

## komatsu2021 (PTL 2021, 100-channel monolithic InP OPA): 4 components / 20 metrics

- Rows: OPA (100 channels, 10 um pitch, measured FWHM 0.108 deg and 0.098-0.111 deg range, SLSR 6.3 dB, calculated
  FSR 8.88 deg, on-chip loss 12-15 dB author_estimate loss_breakdown, 35 mm2 footprint); p-i-n phase shifter (48 mW
  per 2 pi measured, about 14 pF estimated, 800 um x 4 um); passive ridge waveguide (about 5 dB/cm from a reference
  sample, 0.3 dB/cm absorption estimate, 2 um wide, 500 nm core); two-stage 1 x 10 star-coupler splitter (7 dB and
  < 2.2 dB variation, design estimates; 700 um).
- Not entered: main-lobe power 18 % of the FSR power (no parameter); > 80 resolvable points (derived ratio); response
  time < 16 ns (fitted exponential time constant limited by the DAC; no electrical time-constant parameter); 2.4 W
  average drive power (derived, no free_space_emitter power parameter); 2.1 dB/cm phase-shifter absorption estimate
  (no loss-per-length parameter on phase_shifter); 25 um phase-shifter separation (pitch_um not on phase_shifter);
  RC > 1 GHz expectation; 18 deg FSR for a 5 um pitch (not fabricated).
- The printed loss terms (3 + 7 + 1-2 dB) sum to 11-12 dB while the total is printed as 12-15 dB: kept as printed with
  a note. Measurement wavelength of the far-field data not printed: 1550 nm with wavelength_inferred.
- Fab: org_the_university_of_tokyo ("we design and fabricate", all authors at one org, D72). No facility.

## fowler2023 (IPC 2023, 2-page, 905 nm SiN switched OPA): 3 components / 9 metrics

- Rows: switched 7 x 32 OPA circuit (measured -17..+17 deg azimuth scan stored as 34 deg derived, elevations about
  8-20 deg in about 2 deg steps measured, 1.3 / 0.2 deg divergence author_estimate, 32 channels per OPA, 1.5 um
  pitch, about 21 mm x 1 mm from Fig. 1(a) labels); air-cavity SiN thermo-optic phase shifter (P_pi about 30 mW);
  laser-to-chip multi-waveguide coupling structure (about 10 dB, per_interface, preliminary).
- Not entered: P_pi about 90 mW of earlier devices (ref. [3]); 1x8 MZI commutator (no values, not a row); sub-2 um
  phase-shifter pitch (no parameter on phase_shifter); Fig. 3(b) labels < ~5 um and ~100 um; system targets (> 1 W,
  40 m).
- Fab empty (no fabrication statement for this chip). The 7 W tapered GaInAsP laser was provided by III-V Lab
  (org_iii_v_lab, in the registry); it is the demonstration source, not a component row.

## poulton2018 (GFP 2018 invited, 2-page): 1 component / 7 metrics

- Row: 512-element OPA (512 elements, 1.65 um pitch, FWHM < 0.04 deg, SLSR 12 dB, 56 deg phase-shifter steering and
  15 deg wavelength steering, grating antennas > 5 mm).
- Not entered: < 1 mW total power and < 2 uW per phase shifter, 10 ns phase-shifter time constants (no
  free_space_emitter power parameter; the electro-optic phase shifters have no row and no fitting parameter); 25 us
  point-to-point speed (FPGA / DAC limit); > 95 % expected phase-shifter yield; SG-DBR laser co-package with a
  two-ball-lens bench and the PM-fiber input (no values).
- Platform empty (silicon photonics, SOI / stack never stated, D423); wavelength never stated (band unspecified on
  all performance rows). Fab empty (Analog Photonics authors, no fabrication statement).
- D408 check: ref. [3] is the authors' own CLEO 2018 paper, but no value sentence or figure attributes its values to
  it; kept.

## Judgment calls for the auditor

1. luo2015 fab from a first-person epitaxial-growth sentence with all authors at one institute (D399 / D429 vs the
   cao2014 precedent of passive growth -> empty).
2. luo2015 1.5 mm row: Fig. 4(b) reading (about 2148 nm) entered despite the text assigning 2142 nm to 1.5 mm; the
   alternative is to drop it under D159.
3. raptakis2021 typical MMI imbalance (<= 0.2 dB) entered on both the 1x2 and 1x4 rows (statement covers both types)
   rather than kept as a family note under D254.
4. raptakis2021 demonstrated scan spans (12 deg / 8 deg) stored as steering_range_deg derived next to the measured
   main-to-grating-lobe spacings; fowler2023 -17..+17 deg stored as 34 deg derived.
5. raptakis2021 "reconfiguration time about 15 ms" stored as rise_time_us 15000 author_estimate (definition not
   given); drop if the parameter definition is taken strictly.
6. komatsu2021 star-coupler "total insertion loss 7 dB" entered as excess_loss_db (loss beyond the 1:100 split, D43).
7. fowler2023 laser coupler platform left empty although the paper's OPA chips are SiN (separate demonstration,
   layer not stated); classed chip_chip_coupler.butt (laser die to PIC, no optics).
8. fowler2023 beam divergence 1.3 / 0.2 deg as author_estimate (stated as what the design provides; origin not
   stated).

## Registry gaps (value skipped + locator + proposed definition)

- `main_lobe_efficiency_pct` (free_space_emitter): main-lobe power as a fraction of the stated reference (power in the
  FSR or input power). komatsu2021 18 % of the FSR power (p.3 Sec. IV); raptakis2021 about 30 % throughput estimate
  for the 2 x 4 6 um OPA (p.9).
- `response_time_ns` / electrical time constant (phase_shifter, free_space_emitter, switch_fabric): fitted exponential
  or stated time constant of a non-thermal actuator. komatsu2021 < 16 ns (p.3 Fig. 6, DAC limited); poulton2018 10 ns
  (p.1).
- `power_consumption_w` on free_space_emitter: poulton2018 < 1 mW total (p.1); komatsu2021 about 2.4 W average (p.3,
  derived).
- `threshold_current_density_a_per_cm2` (laser; candidate already in D431 / D433): luo2015 Jth 718 / 336 A/cm2 and
  Jinf 180.8 A/cm2 (p.4 Fig. 3).
- `internal_loss_per_cm`, `internal_efficiency_pct` (laser; candidates in D431): luo2015 8.2 /cm and 37.6 % (p.4).
- `characteristic_temperature_t1_k` (laser): T1 of the slope efficiency; luo2015 132 K over 20-70 C (p.6).
- `max_operating_temperature_k` (laser; candidate in D431): luo2015 100 C, pulsed (p.5-6).
- `drive_current_ma` for a pi / 2 pi shift (phase_shifter; candidate in D439): raptakis2021 16 / 20 mA (p.8-9, p.11,
  conflicting pi vs 2 pi).

## Missing orgs

- Optagon Photonics (raptakis2021 p.1 author footnote): affiliation only, no fab or facility role in this batch.
- No missing fab / facility orgs.
