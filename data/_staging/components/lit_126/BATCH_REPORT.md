# lit_126 batch report (distill, 2026-11-12)

Papers: beeck2020, gasse2019, kumar2025, souleiman2024, lee2022, thai2018 (family amplifier / laser /
chip_chip_coupler). Totals: 37 components, 166 metric rows. Validator
(`merge_component_staging.py data/_staging/components/lit_126 --dry-run`): 0 errors (one warning on the
already-merged row `cmp_lit_ni2025b_pimmwc-m18`, not this batch).

Identity check: every cached text is the paper of its source row (page-1 title matches; lee2022 is the
correct paper now, D397 history), none is a correction / erratum. thai2018 text layer interleaves the two
columns on pp.6 and 8 (`garbled_text_layer` is false in source.json): values there read from the page renders.

## beeck2020 (9 components, 42 metrics)

- `soa_1148um` amplifier.soa (9): on-chip gain 13.7 dB at 1570 nm / 120 mA (measured, reference-waveguide GC
  calibration), max on-chip output 8.81 dBm (printed 7.6 mW, derived, D394), Psat 9.03 dBm (printed 8 mW,
  derived), NF 10.6 / 12.3 dB (100 / 120 mA), 3-dB gain bandwidth 28 nm, 10 ohm, length 1148 um, ridge 3.2 um.
- `ring_laser` laser.heterogeneous (8): thresholds 59 / 63 / 69 mA at 15 / 20 / 25 C, slope 0.015 W/A (derived,
  on-chip de-embedded), up to 0.35 mW (derived), SMSR about 18 dB, FSR 10.7 GHz (simulated: calculation in
  Supplement 1), 10 ohm.
- `sin_asi_taper_tip120` / `_tip100` waveguide_platform.transition (10 / 2): 0.66 / 0.52 dB per transition
  (cutback, Fig. 2 labels), > 99 % simulated, stack geometry (SiN 300 nm, a-Si:H 370 nm, SiO2 100 nm, BOX 3.3 um).
- `asi_iiiv_taper` transition (5): simulated 93 % / 75 % (0 / 1 um misalignment), III-V tip 500 nm, 224 um.
- `sin_wg_processed` 0.8 dB/cm and `sin_wg_reference` 0.61 dB/cm at 1570 nm (cutback); `asi_wg_3um` about
  5 dB/cm (author_estimate, origin not stated).
- `sin_gc` grating (3): 7.8 dB at 1545 nm (loopback_half), 3-dB bandwidth 60 nm, back-reflection > 20 dB (simulated).

Not entered: SOA confinement 0.93 %/QW and 2.11 kA/cm2 (no parameter); gain-peak shift 1564.4 -> 1569.7 nm (no
amplifier peak-wavelength parameter); 17 % output-coupler fraction (design, laser notes); thermal roll-off near
230 mW and CW / CCW 7 dB (Supplement 1, not cached); simulated tip reflections -50 / -41 / -47 / -21 dB (no
transition back-reflection parameter); lasing wavelength (only "around 1550 nm" in the abstract, Fig. 9 peaks
unlabelled); FIB-observed 650 nm misalignment (one sample).
Fab / facility: empty on all rows (passive fabrication text; authors at Ghent University - imec and Tyndall,
"our current process" does not pick one org). No missing orgs.
Judgment calls: Psat (Eq. (1) fit parameter, paper says only "saturation power") entered as `psat_out_dbm`
with the model in condition (in Eq. (1) the output at 3-dB compression tends to Psat/2); on-chip gain kept
`measured` + `reference_structure` (beeck2021 precedent) while de-embedded on-chip powers / slope are `derived`
(D394); NF wavelength 1570 nm inferred.

## gasse2019 (8 components, 48 metrics)

- Five SOA rows (0.95 / 1.2 / 1.45 / 1.6 / 1.85 mm; 6 / 11 / 11 / 4 / 5): length, mesa 5 um, forward voltage at
  the 4.9 kA/cm2 bias; G0 25 / 27 dB and Ps 16.72 / 17.24 dBm (Eq. (2) fits, 1575 nm), 14 dB at 3 dBm input,
  max on-chip output 17.2 / 17.5 dBm (derived, D394), 0.41 / 0.54 W, NF about 9 dB (> 0 dBm input) and < 8 dB
  (< -15 dBm input) derived (Eq. (4), D166); 1.2 mm 1-dB bandwidth 20 nm; 1.45 mm gain ripple < 1 dB over 20 nm
  (entered as bw_1db_nm >= 20); 0.95 mm 20 dB / 16 dBm / 3.4 ohm; 1.6 / 1.85 mm > 17 dBm; 1.85 mm 1.7 ohm.
- `si_iiiv_taper` transition (9): about 0.5 dB per taper at 1575 nm (cutback at transparency, measured) and
  < 0.5 dB simulated, geometry (tip 0.6 um, 180 um, Si rib 4 um, BCB 40 nm, Si 400 nm / 180 nm etch, BOX 2 um).
- `hybrid_wg_loss` straight (1): 78.17 dB/cm derived from printed 18 cm-1 (read as power coefficient, D420
  precedent; definition not printed).
- `si_gc_lowrefl` (1): 9.5 dB per coupler at 1575 nm (loopback_half).

Not entered: 24.7 dB (p.2) beside the fitted 25 dB for the 1.2 mm SOA (notes); GC back-reflection < -40 dB
(cited from ref. [17]); simulated taper reflection < -40 dB (no transition parameter); confinement 0.7 %/well;
transparency current density vs wavelength (Fig. 6, no parameter); parasitic lasing of the 1.6 / 1.85 mm SOAs.
Fab / facility: empty (presentation sentence plus passive process description, all authors at Ghent University -
imec; no acknowledgment section). No missing orgs.
Judgment calls: Ps as `psat_out_dbm` (same convention as beeck2020); NF bias conflict (p.8 gives 237 / 175 mA,
pp.5-6 give 300 / 237 mA for the same 4.9 kA/cm2) noted, NF rows carry the current density only; Ps kept
`measured` (fit printed in dBm) while de-embedded output powers are `derived`.

## kumar2025 (2 components, 17 metrics)

- `pic_pic_oxide_align` chip_chip_coupler.butt (13): PIC-to-PIC loss per interface 2.3 dB best / 2.7 dB mean /
  0.3 dB std (derived: Lt - L1A - L1B), misalignment-only 0.2 best / 0.6 mean (author_estimate: minus the
  simulated gap loss), simulated 2.1 dB at 10 um gap and 1-dB lateral tolerance 2.5 um, gap 10 um, MFD 10 um,
  SiN tip 250 nm, SiN 300 nm, 5.5 / 5.5 um oxide.
- `pic_pic_si_align` (4): 2.5 dB best / 3.1 dB mean / 0.36 dB std, misalignment-only 0.4 dB.

Not entered: lateral alignment 260 nm (+/-100 nm) and height 238 nm mean / 66.1 nm std over 15 reassemblies (no
assembly-accuracy parameter); simulated 1-dB height tolerance 1.8 um (no vertical-tolerance parameter); abstract
"-2.4 dB" link loss (assembly not named; matches the Fig. 6 oxide minimum, in notes); individual fiber-to-PIC
losses L1A / L1B (not printed); alignment-structure dimensions (notes). No wavelength anywhere in the paper:
`band: unspecified` on every loss row.
Fab / facility: fab `org_university_of_rochester` ("We fabricate the devices", both authors at Rochester;
li2019 / ling2024 precedent), facility `org_cornell_nanoscale_facility` (p.10 acknowledgment).
Missing org: "Integrated Nanosystems Center at University of Rochester" (p.10 Acknowledgment; facility role,
named as a place where device fabrication was performed).
Judgment calls: printed -2.3 dB (oxide) and -2.5 dB (Si) read as best ports and kept although Fig. 6 left axis
gives about -2.38 dB and -2.85 dB minima (D417); the printed values equal the -0.2 / -0.4 dB misalignment
estimates plus the simulated -2.1 dB gap loss. Class `chip_chip_coupler.butt` for PIC-to-PIC edge coupling
across a 10 um gap (registry text says laser-to-PIC; `other` is the alternative); platform `silica` (oxide mode
converter, nauriyal2019 / nauriyal2023 precedent). Simulated values on the oxide row only (shared design).

## souleiman2024 (6 components, 14 metrics)

- `tunable_laser_soa` laser.tunable (7): tuning about 40 nm, SMSR >= 50 dB, about 5 mW on-chip at laser 100 mA /
  SOA 80 mA (author_estimate: de-embedded with a stated 3-4 dB coupler loss of unstated origin), 2-3 mW modulated,
  7.5 ohm at 100 mA, Vernier FSR 43.56 nm (design), gain section 670 um.
- `vernier_ring_1` / `_2` resonator.ring (D400): design FSR 2.52 / 2.68 nm.
- `bragg_mirror` reflector.bragg: 20 % (simulated per Fig. 1 caption), 12 um, 242 nm period.
- `sagnac_mirror` reflector.loop_mirror: 100 % (design).
- `si_gc` grating: 3-4 dB with a 3 um-waist lensed fiber (author_estimate).

Not entered: EAM values (ER 16 dB at 1556 nm / 14.5 dB at 1542 nm, -6 dB EO bandwidth 38 / 20 GHz, DER
4-8.5 dB; modulator, no component class here; EO-atlas candidate if the coordinator wants it); SOA booster
(920 um, confinement 10.95 %) has no standalone metric, so no SOA row (geometry only, rule 9); heater resistance
about 175 ohm and about 2.7 nm per heater step (no laser parameter); threshold (Fig. 3(a) unlabelled, depends on
SOA current); Fig. 1 simulated GC inset (unlabelled in the caption); ring field transmission about 0.93 (notes).
Fab / facility: empty. The first-person bonding sentence does not name an org and the authors are at III-V Lab,
Telecom SudParis and CEA-Leti (all in the registry); fabrication otherwise points to ref. [21]. No missing orgs.
Judgment calls: one laser row carries the transmitter output (SOA and EAM in `includes`).

## lee2022 (11 components, 39 metrics)

- `sgdbr_laser_1` / `_2` laser.tunable (11 each): threshold 41 / 43 mA (pulsed), about 3 mW at the facet and
  about 2.2 V at 100 mA (stated once for both, Fig. 3 confirms both), measured tuning 24 nm (1526-1550) / 22 nm
  (1547-1569), SMSR >= 37 dB, Lorentzian linewidth 2.69-4.07 / 3.02-4.26 MHz and 3.08 / 3.17 MHz single points
  (derived, MHz -> Hz), design centre 1538 / 1562 nm, design tuning 27 nm, design comb spacings 3.5 / 3.1 nm.
- Four SG DBR mirror rows reflector.bragg (3 each): expected max reflection 25 % (front) / 70 % (rear) from TMM
  (simulated), section length 500 / 800 um, kappa 120 /cm (design).
- `soa1` amplifier.soa: > 10 dB at 60 mA (author_estimate, how determined not stated).
- `mmi` 3.5 dB, `topm` 1 dB, `ssc` 3 dB per coupler, `butt_joint` transition 2 dB: printed "predicted" building-block
  losses (author_estimate).

Not entered: max SMSR 48 dB (laser not named, D159); combined 43 nm / 5.36 THz and THz power 1.8-320 uW (PIC /
system values with an external photodiode emitter); expected THz linewidth < 6 MHz (computed); SG burst period /
length / count (Table 2, notes; no parameter).
Fab: `org_fraunhofer_heinrich_hertz_institute` on all rows (generic InP foundry platform of HHI, MPW, p.2 and
p.8; Contract v7 passive-with-org), process_name "Fraunhofer HHI generic InP foundry platform (MPW)". No
facility. No missing orgs.
Judgment calls: Fig. 3 caption 6 mA vs text 60 mA SOA current (text used, conflict in notes); MMI 3.5 dB entered
as `insertion_loss_db` (whether the 3 dB split is included is not stated, so not `excess_loss_db`).

## thai2018 (1 component, 6 metrics)

- `gesn_microdisk_10um` laser.other, platform `other`: lasing 2720-2890 nm at 15 K and 3200 nm at 230 K, T0 117 K
  (fit of the pump-density threshold), radius 5 um (derived from 10 um diameter), disk 850 nm (SEM) and active
  layer 418 nm (TEM).

Not entered: optical pump threshold densities 134 / 375 / 640 kW/cm2 (15 / 135 / 190 K), 503 kW/cm2 extrapolated
and <= 790 kW/cm2 at 230 K; maximum lasing temperature 230 K (no parameters, see gaps); simulated confinement 63 %.
Fab / facility: empty (passive verbs, no fabricator named; no acknowledgment section). No missing orgs.
Judgment call: `characteristic_temperature_k` used for the T0 of an optical pump threshold density (registry
definition says threshold current); delete if the coordinator keeps the definition strict.

## Registry gaps (skipped value + locator + proposed definition)

1. `pump_threshold_density_kw_per_cm2` (laser, amplifier): thai2018 134 kW/cm2 at 15 K (p.4 Sec. 3.1), 375 /
   640 / 503 / <= 790. Proposed: "optical pump threshold power density (pulse peak or average and spot in
   condition)".
2. `max_operating_temperature_k` (laser): thai2018 230 K maximum lasing temperature (p.1, p.4). Proposed: "highest
   heat-sink / stage temperature at which lasing (or the stated criterion) is observed".
3. Assembly placement accuracy, e.g. `alignment_error_um` (chip_chip_coupler, fiber_interface, micro_optics):
   kumar2025 0.26 um lateral (+/-0.1), 0.238 um height mean / 0.0661 um std over 15 reassemblies (p.8). Proposed:
   "measured residual misalignment after passive / active assembly (axis and statistic in condition)".
4. `tol_1db_vertical_um` (chip_chip_coupler, fiber_chip_coupler, micro_optics): kumar2025 1.8 um simulated
   (p.4). Proposed: "out-of-plane (height) misalignment for 1 dB excess loss (half-width)".
5. `back_reflection_db` on waveguide_platform.transition: beeck2020 -50 / -41 / -47 dB (p.2-3), gasse2019 < -40 dB
   (p.3), all simulated.
6. Amplifier gain-peak wavelength (`center_wavelength_nm` widened to amplifier): beeck2020 1564.4 nm at 80 mA,
   1569.7 nm at 120 mA (p.6).
7. `heater_resistance_ohm` widened to laser: souleiman2024 about 175 ohm (p.5).
8. `transparency_current_density_a_per_cm2` (amplifier): gasse2019 Fig. 6 (values only in the plot, p.8).
9. Sampled-grating geometry (`sampling_period_um`, `burst_length_um`, `n_bursts`; reflector, laser): lee2022 Table 2
   (p.4), e.g. laser 1 front Z0 93.9 um, Z1 7.63 um, 6 bursts.
10. `confinement_factor_pct` (amplifier, laser): beeck2020 0.93 %/QW, gasse2019 0.7 %/well, souleiman2024 13.5 /
   10.95 %, thai2018 63 % (all simulated).

## Missing orgs

- "Integrated Nanosystems Center at University of Rochester" (kumar2025 p.10 Acknowledgment) - facility role.
