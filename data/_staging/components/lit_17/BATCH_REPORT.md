# Batch lit_17 report (distill subagent, 2026-10-29)

Dry-run `batch lit_17: +28 components, +158 metrics; errors 0`. ASCII, no e-mail, no quotes (all sources
restricted_local_only). Not yet audited or merged.

## Per paper (components / metrics)

- chen2023 (4 / 33): hybrid Thorlabs gain chip + Ligentec Si3N4 dual-MRR Vernier ECL with booster SOA in a butterfly
  (laser.tunable, platform other: tuning 55 nm, SMSR, threshold, 226.3 mW, linewidths 2.37 kHz / 2-8 kHz / 995 Hz, RIN at
  3 wavelengths, mode spacing measured 24.2 pm and design 29.0 pm, power consumption), Si3N4 dual-MRR filter (wdm.mrr,
  fab org_ligentec: Vernier FSR 54 measured / 53 simulated, simulated Q, design coupling 8%), Si3N4 strip waveguide
  (0.1 dB/cm author_estimate), ShiJia SOA (amplifier.soa). Not entered: frequency drift and Allan variance (no parameter),
  Vernier side-mode difference 2 dB / 3 dB sim (no parameter), SOA "saturation > 240 mW" (no compression criterion),
  80% coupling (simulation input), heater gap 1.7 um (cited, not allowed for wdm), Table 2. Laser fab empty (assembly
  site not stated; four orgs). Judgment: gain-chip and SOA part properties as `specification`; output power ref_plane
  unspecified (module output, plane not stated).
- ibrahimi2021 (6 / 27): R-SOA + Si3N4 Bragg MLL (laser.comb: 360 MHz, harmonic 2.539 GHz, threshold, 250 ps filtered pulse,
  263.1 mm delay), R-SOA (fab org_iii_v_lab), Bragg mirror (85% / 2.82 nm measured, simulated R / BW / SLSR, period),
  Si3N4 waveguide 0.05-0.06 dB/cm cutback derived, R-SOA-to-Si3N4 butt coupling (2 dB author_estimate, 65% / 1.87 dB
  simulated, SSC mode), Si3N4-to-lensed-fiber facet (5 dB author_estimate). Si3N4 rows fab org_cea_leti; laser both orgs.
  Not entered: comb 30-dB width 2.8 nm (349 GHz) and -3 dB 62 GHz (no comb-width parameter), R-SOA gain "20 dBm" (unit
  error), confinement factors, in-cavity 80% reflection statement. Flag: 2.539 GHz is called the 6th harmonic but is
  about 7x 360 MHz; entered as printed with note.
- liu2025b (1 / 18): micro-transfer-printed double-ridge SOA Vernier tunable laser on imec 400 nm SOI (laser.tunable, fab
  org_imec + org_ghent_university per niels2026: tuning > 51 nm, SMSR ~40 dB, threshold 66-72 mA derived (halved),
  6.9 / 10.1 mW on-chip, 1671 Hz best (Fig. 4(c) legend wavelengths), RIN ~-140, f_r ~1 GHz, 8-9 ohm, 684 mW, WPE 1.46%,
  tuning 0-46 mW, geometry). Not entered: 9-of-14 population bounds, simulated confinement, effective cavity lengths.
- wang2026e (5 / 25): E-band printed InP SOA tunable laser (fab org_iii_v_lab + org_imec: 41 nm, SMSR > 45 / > 50,
  ~70 mA, 18 ohm, 3 mW on-chip derived, RIN < -145, single-ring tuning slopes 440 / -610 pm/mW derived), standalone
  test ring (wdm.mrr: Q_L 8500-9800, 78 mW per FSR, FSR 3.9 nm, width / gap), Si rib waveguide (~1 dB/cm
  author_estimate), Passives+ GC (8-10 dB loopback_half derived), loop-mirror MZI heater (P_pi 21 mW derived from
  42 mW per 2 pi). Not entered: printing misalignment < 500 nm (no parameter), Fig. 7(a) / 8(b) maps.
- zhang2023d (2 / 15): printed DFB with co-integrated PA (laser.soa_dfb, fab org_imec only: threshold < 80 mA, 9 ohm,
  4 dBm stand-alone / 14 dBm with PA on-chip derived, SMSR 34 / 28 dB, ~1540 nm, grating geometry incl. duty 0.75
  derived with D253 note), imec GC (8 dB per_coupler measured per D167). Not entered: threshold current density
  2.36 kA/cm2 (no parameter). D259: nothing restated from the authors' earlier work entered (coupon process ref [5]).
- juvert2018 (3 / 13): etched-facet FP laser printed in a SOI trench (laser.heterogeneous, inp: < 1 mW on-chip best,
  thresholds 34 / 58 mA at 20 / 35 C, 2.3 / 0.9 uW fiber, mode spacing 0.8 nm), same coupon on a dummy Si substrate
  (> 10 mW best, 25-50 ohm), GC (-5 dB efficiency author_estimate). Not entered: SSC coupling loss (authors disclaim the
  apparent -10 dB), 300 uW fiber power (computed from assumed -5 dB), placement statistics and FIB vertical offset (no
  parameter). SSC (100 um inverse tapers, tips 100-175 nm, tridents s 800-1000 nm) geometry-only, not a row. Fab empty
  (three author orgs); epi from Smart Photonics is a note.
- mangal2019a (3 / 15): backside Si microlens expanded-beam interface (micro_optics.integrated_lens: 11 dB fiber-to-fiber,
  3 dB drop vs SMF reference derived, Fresnel 1.85 author_estimate, 1.15 derived, 1-dB lateral 7 um and 2.5 um, 1-dB
  longitudinal 700 um, beam 34 um simulated, TEC40 MFD spec, ROC 480 measured / 475 design, sag 18.3 um; fab
  org_centre_for_microsystems_technology borderline D84b from staff thanks for lens RIE), downward-directionality GC
  (3.5 dB, Table I, author_estimate; fab org_imec), fiber-attached input GC (4.5 dB author_estimate). Not entered:
  angular 1-dB tolerance +/-0.5 deg, 3-dB lateral +/-12.5 um, Table I post-optimization projections.
- psaila2024 (2 / 6): Intel glass micro-optic bridge (micro_optics.other, glass: single-pass excess loss mean 1.32 dB and
  range 1.13-1.62 over 4 assemblies, loopback_half derived with the subtracted terms in excludes; beam ~30 um derived from
  roll-off model, 35 um design; 16 channels), PIC edge coupler (MFD ~7 um author_estimate, platform empty). Fab empty
  (passive wording, all Intel, D80b). Judgment: the laser-written glass waveguide bridge used to probe the assembly is
  treated as setup equipment (D160) and not a row; its measured beam 34.7 x 31.6 um is in the bridge note.
- uddin2023 (2 / 6): dispensed UV-epoxy microlens on a GC (micro_optics.integrated_lens, polymer: simulated 35%,
  R ~100 um derived), bare GC reference (simulated 15%, 10 um length, layer thicknesses). Not entered: NA 0.36 and
  angular contrast < 1 dB vs ~5 dB (no parameter), 20 / 36 / 42% peaks (simulated vs measured ambiguous, D156),
  FWHM statement, lens heights (Fig. 3(c) nm axis vs 2.75 um in Fig. 4). Fab empty.

## Orgs missing

ShiJia Photons (printed "ShiJia Photons", chen2023 p.3 Sec. 2.1): developer / vendor of the booster SOA; would be
fab_org_ids of `cmp_lit_chen2023_soa` (vendor of a purchased part) if added.

## Registry gaps (value actually skipped, locator, proposed definition)

- laser `frequency_drift_mhz` (+ duration in condition): chen2023 < 50 MHz / 5 min, < 200 MHz / 120 min (p.10 Fig. 12).
  Def: peak-to-peak free-running optical frequency drift over the stated time.
- laser `comb_bandwidth_ghz` (or bw_3db_ghz / bw_30db_nm for laser): ibrahimi2021 -3 dB 62 GHz, 30 dB 2.8 nm / 349 GHz
  (p.4, abstract). Def: optical comb envelope width at the stated level.
- laser `threshold_current_density_ka_per_cm2`: zhang2023d 2.36 kA/cm2 (p.3).
- micro_optics `tol_1db_angular_deg`: mangal2019a +/-0.5 deg (p.4 Fig. 8(b)). Def: angular misalignment for 1 dB excess
  loss (half-width).
- micro_optics `numerical_aperture`: uddin2023 NA ~0.36 (p.2 Fig. 1(d)). Def: NA of the lens as stated.
- wdm `heater_gap_um`: chen2023 heater 1.7 um above the ring waveguide (p.3; cited justification).
- chip_chip_coupler placement offset (`placement_offset_um`, mean / std): juvert2018 lateral 420 +/- 400 nm,
  longitudinal 750 +/- 130 nm (p.8 Fig. 10); wang2026e < 500 nm (p.4). Def: printed / placed component offset from
  its target position.
