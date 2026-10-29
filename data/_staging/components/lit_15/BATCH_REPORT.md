# Batch lit_15 report (distill subagent, 2026-10-29)

Dry-run `batch lit_15: +36 components, +173 metrics; errors 0`. ASCII, no e-mail, no quotes (only isichenko2023 is
open_license_ok; none used). Not yet audited or merged.

## Per paper (components / metrics)

- boust2020 (6 / 36): InP DFB pump (threshold 81 mA, >200 mW, SMSR 59 dB, cavity-mode FSR 24.6 GHz, 20 x 60 deg
  divergence, free-running Lorentzian 60 kHz, <3 W with TEC), Si3N4 rings A (70 MHz FWHM, Q_L 2.8e6, Q_i 5.6e6
  author_estimate as 2 Q_L, FSR 113.5 GHz / 0.94 nm, finesse ~1500, geometry) and B (Q_L ~1e6), DFB-Si3N4 butt coupling
  (~0.6 dB per_interface author_estimate from far-field overlap, 0.5 dB input reflection in notes), comb A (113.5 GHz as
  repetition_rate_ghz: abstract wording, D83b; 120 lines; 11 mW in fiber; 300 uW threshold simulated) and SIL comb B
  (2.04 THz line spacing derived; SIL linewidth <= 1 kHz, setup floor). Not entered: 10 dB/m Si3N4 loss (stated with the
  co-authors' process paper [19], D259), 80 dB/m [5] (cited), 30-dB comb span 13.6 THz, RF beat 6.3 MHz, injection
  powers 110 / 133 mW (estimates, no parameter). Fab empty (passive voice, four orgs).
- gao2019 (5 / 19): packaged SiPh Vernier tunable laser (laser.tunable, platform other: 21.5-21.9 dBm fiber over 27
  channels, 150 mW max, 0.2 W/A, 65 nm, SMSR >50 dB, Lorentzian <60 / <80 kHz, RIN <-150 dB/Hz, sub-assembly length,
  package footprint derived), dual-ring filter wdm.mrr (0.4 dB mean / <1 dB 3-sigma per ring, <2 dB round trip derived,
  FWHM <10 GHz, ~60 mW per 2 pi), gain chip-SiN SSC butt (~1 dB measured, 94 % simulated), gain chip-SOA lens (<1 dB
  author_estimate), passive flip-chip gain chip-SOA (<2 dB, printed as 1-sigma). Not entered: frequency error +/-1 /
  +/-0.5 GHz and drifts, EVM, tolerances, facet reflectivity 30 %. Fab org_neophotonics on laser and couplings is
  borderline (D84b: all authors NeoPhotonics, own staff thanked for optical assembly); SiPh chip from an unnamed
  commercial foundry (filter row fab empty).
- isichenko2023 (2 / 13): 780 nm Si3N4 ring R 5.84 mm (Q_i 145e6, Q_L 65e6, 6 MHz Fig. 1(c) label, ER 30 dB, 0.36 dB/m
  -> 0.0036 dB/cm derived, TM, 40 nm x 4 um, 15 / 6 um claddings) and FP-diode SIL laser (fundamental 0.64 Hz derived,
  integral 732 Hz, 1.5 mW at the tap). Fab org_honeywell borderline (D84b, heim2025 precedent: Honeywell staff thanked
  for the fabrication). Not entered: FN floor 0.2 Hz2/Hz, Table 1 application limits (calculated).
- notaros2019 (8 / 37): Al2O3:Er3+ DFB laser (1599 nm, SMSR 30 dB, 40 mW launched pump threshold, 2 cm, 509 nm period,
  0.5 duty, segment width, film 1170 nm), Er film background loss <0.1 dB/cm, Si (~3 dB/cm) and Si3N4 (~1.5 dB/cm)
  waveguides (band unspecified), Si3N4-to-Si layer transition (<0.1 dB measured, 200 um, bilayer geometry), pump/signal
  DC filter wdm.other (simulated ~500 nm 3-dB band, ~30 dB tap extinction), 980 nm edge facet (6.2 dB per_facet,
  "estimated from experiment"), 49-antenna OPA (0.85 x 0.20 deg FWHM measured, 0.80 x 0.16 expected, 15 deg at 0.5 W,
  ~8 dB author_estimate share of the 48 dB system loss, geometry). Fab: "fabricated at CNSE SUNY" -> 
  org_suny_polytechnic_institute (judgment: CNSE is the co-author unit of SUNY Polytechnic Institute); Er film
  "performed at MIT" -> org_mit added on laser and film rows. Not entered: slope efficiency 0.01 %, 30 deg/W, confinement
  factors (simulated), 600 um gain-waveguide transition (no value, not a row).
- fard2021 (4 / 15): Si3N4-to-SU-8 polymer adiabatic taper as waveguide_platform.transition (D48, same interposer;
  platform other): 0.73 dB derived from Table I, 0.52 dB author_estimate (assumed 1.73 dB/cm material loss), 0.22 dB
  simulated, full bilayer geometry; PWG loss 1.83 dB/cm and Si3N4 1.63 dB/cm (cutback), PWG facet coupling 2.44 dB
  (scope device_total: fiber in + objective out; Fig. 6 caption prints dB/cm, typo). Fab org_aim_photonics (interposer
  "fabricated at AIM Photonics foundry"); polymer steps passive voice, not attributed. Tolerance +/-4 um not entered.
- loi2019 (2 / 15): micro-transfer-printed InP etched-facet FP laser (threshold ~17 / ~23 mA, ~14 ohm, Z 116 K/W
  measured / 99 K/W simulated, ~1340 nm, simulated MFD 3.25 x 1.156 um = 2 w0 from Table I, 500 um, 2 um ridge) and a
  design row for the simulated 1 x 3.2 um SU-8 butt coupling (90.5 % / ~75 % TM0). Not entered: fabricated 7.5 um SU-8
  waveguide, SOI taper and laser-to-polymer coupling (no measured value), 132 / 49 K/W configurations not built,
  reflectivities. Inconsistencies noted: recess 1.54 (abstract) vs 1.57 um, Fig. 3 caption 90 / 45 vs 99 / 49 K/W. Fab
  empty (three orgs).
- lu2016 (5 / 16): standard SOI GC (11.7 dB fiber_to_fiber, 5.9 dB loopback_half derived, 630 nm / 0.5 / 70 nm / ~11 um
  geometry from the FDTD description of the GC used), VCSEL-GC active alignment (10.4 dB derived) and flip-chip bonded
  (11.8 dB typical, derived; all printed negative), bare VCSEL (1546.15 nm, 37 dB suppression) and VCSEL on PIC (-8.6 dBm
  injected, author_estimate; 1547.15 nm; 35 dB). Not entered: excess penalties 4.5 / 5.9 dB (relative), +/-1.6 um
  tolerance, ~1 dB fabrication tolerance, optimized 15 um GC (simulation, relative value only), slope efficiency 1.6 %,
  10 deg tilt (no chip_chip_coupler angle parameter). Fab empty.
- dostart2020 (4 / 22): SOPA tile with nitride-bar gratings (free_space_emitter.other, si_sin_multilayer: 0.11 x 0.2 deg
  FWHM, 0.1 x 0.16 deg diffraction limit, 35.8 deg slow-axis span over 1450-1650 nm, 5.5 deg fast-axis FOV, 32 rows,
  16 um pitch, 460 nm period, geometry), Euler U-bend (0.003 dB measured / 0.001 dB design per 180 deg, as
  insertion_loss_db), adiabatic width taper (0.07 / 0.05 dB), 2 um Si waveguide (~0.06 dB/cm). Fab org_aim_photonics (MPW
  run, Supp. p.12). Not entered: 16,470 spots, 41.3 / 1.53 GHz steering steps, 0.15 dB/cm grating strength, fill factors,
  next-gen design losses (later design), two-tile tiled-aperture demo (fringe visibility only; not a row).

## Fab / facility organizations missing from the registry

- VERTILAS GmbH (lu2016 p.4 Sec. 2: vendor of the purchased 1550 nm VCSEL; would be fab_org_ids of vcsel_bare and
  vcsel_on_pic).
- Not needed (affiliations only, no fabrication statement): X-Celeprint Limited (loi2019 p.1), Cork Institute of
  Technology (loi2019 p.1).

## Judgment calls for the coordinator

1. gao2019 org_neophotonics (D84b assembly-staff thanks) and isichenko2023 org_honeywell (staff thanked "for the
   fabrication") kept as borderline.
2. notaros2019 "CNSE SUNY" -> org_suny_polytechnic_institute (no CNSE org in the registry; no precedent row).
3. boust2020 113.5 GHz as repetition_rate_ghz (abstract "repetition rate") although the comb is an unstable MMS comb.
4. Hybrid pump-plus-resonator sources (boust2020 combs, gao2019 laser) platform `other`; couplings take the receiving
   waveguide layer.
5. dostart2020 180-deg bend loss as insertion_loss_db per_component (bend_loss_db_per_90 would need halving).

## Registry gaps

| gap | skipped value (locator) | proposed definition |
|---|---|---|
| `current_tuning_pm_per_ma` (laser) | boust2020 5 pm/mA at ~25 C, ~700 mA (p.2) | static lasing-wavelength shift per mA of drive current (D83g keeps it out of fm_efficiency) |
| `slope_efficiency_pct` (laser) | notaros2019 0.01 % signal per launched pump (p.4); lu2016 1.6 % of injected power (p.8 Fig. 9) | optical or normalized slope efficiency in %, definition and reference plane in condition |
| beam_divergence_deg for chip_chip_coupler / fiber_chip_coupler | boust2020 passive-waveguide far field 22 x 34 deg full 1/e2 (p.3) | facet far-field divergence of the on-chip side of a coupler |
| tilt angle for chip_chip_coupler (widen fiber_angle_deg or `source_angle_deg`) | lu2016 VCSEL tilt 10 deg (p.7) | tilt of the emitting die / beam from the chip normal |
| `steering_efficiency_deg_per_w` (free_space_emitter) | notaros2019 30 deg/W (p.1, p.5) | thermo-optic steering angle per W of phase-shifter power |
| `steering_step_ghz` (free_space_emitter) | dostart2020 41.3 GHz slow / 1.53 GHz fast at 1550 nm (p.6) | optical frequency step to the next addressable / resolvable spot (axis in condition) |
| `grating_strength_db_per_cm` (free_space_emitter) | dostart2020 0.15 dB/cm weak nitride grating, estimated (p.11 Supp.) | radiated power per unit grating length |
| `n_spots` (free_space_emitter) | dostart2020 16,470 addressable spots (p.6) | number of addressable / resolvable beam positions as stated |
| `frequency_error_ghz` (laser) | gao2019 +/-1 GHz (SOA current steps), +/-0.5 GHz (10-80 C) (p.5-6) | max lasing-frequency deviation from target under the stated disturbance |
| reflectivity_pct for laser | gao2019 front facet 30 % (p.2); loi2019 32 % air / 15.5 % with polymer (p.6, estimated) | laser facet / mirror power reflectivity |
| comb span (rejected D81) | boust2020 30-dB bandwidth 13.6 THz / 113 nm (p.4) | re-proposal only if the coordinator reopens D81 |
