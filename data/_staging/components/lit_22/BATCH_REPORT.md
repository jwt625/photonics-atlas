# Batch lit_22 report (distill subagent, 2026-10-29)

Dry-run `batch lit_22: +49 components, +295 metrics; errors 0`. ASCII, no e-mail, no quotes (ros2022 and yong2021 are
open_license_ok but none were needed). Not audited or merged.

## Per paper (components / metrics)

- chen2024a (7 / 38): Sb2S3 on Intel 300 mm Si with PIN heaters. MRR (Q a/c 5.66e4 / 3.91e4, 0.40 nm shift, FSR 2.7 nm),
  25 um ring phase shifter (0.3 pi derived, 0.11 dB c-state excess from Q, 0.2 dB carrier-migration estimate, 62.5 ohm),
  60 um MZI phase shifter (0.24 / 0.7 pi, 4 levels, >500 events), QC asymmetric DC (IL 0.7 / 1.0 dB, ER 12.1 / 8.6 /
  3.3 / 15.7 dB at 1343 nm, 32 % bar, endurance contrast 8.5 / 4.5 dB), QC MZIs equal (5 levels, 106-185 ohm) and
  unequal (8 levels, 0.059 pi step), oxide window (< 0.01 dB simulated). Fab org_intel + org_university_washington
  (contributions: in-house integration), facility SNSF. Not entered: pi/um and dB/pi figures (gap), Q 1.27e5 -> 1.01e5
  and 0.02 dB integration loss (tied to "20 um-long Sb2S3" vs the 25 um ring: D159), Supp. values (not cached).
- delaney2021 (5 / 24): laser-written Sb2Se3 on Cornerstone 220 nm rib SOI. MZI phase shifters 125 / 250 / 50 um (2 pi,
  10 pi, 0.02 / 0.04 pi per pixel, 17 dB at 1553 nm, MZI IL read off Supp. Fig. S3), endurance row (350 / ~500 / >500
  cycles; device not identified, kept separate), programmable 1x2 MMI (92 % / 97 % sim split, >8 dB, <= 0.5 dB added
  loss). Fab org_cornerstone + org_university_of_southampton (acknowledgement + contributions).
- ros2022 (7 / 22): Sb2Se3 on Lincoln Lab 90 nm-line doped-Si heaters. Bowtie 6 um OPS (pi/2, ~pi MZI, >35 dB, 250
  events, ~1 kohm, geometry), 2x2 MZI switch (switch_fabric.other, D158: 15 / 6.5 dB), 3 um ring OPS (0.28 pi), 6 um
  add-drop OPS (0.47 pi, 10 dB ER modulation), coupling-tuned ring (~20 dB), bridge heater (pi/2, 1025 ohm), trimming
  OPS (retention 4e6 s). Fab org_mit_lincoln_laboratory, facility MIT MTL. Not entered: per-length loss / phase
  (D250), switching energies (D81), 22 dB ER of "a similar" switch (Supp. S4, not identified), Table 1.
- yong2021 (4 / 80): AMF visible SiN suspended TO phase shifters PS1 / PS2 / PS3 (P_pi per wavelength: die-1 Table II /
  III, 5-die means, simulations; MZI IL / ER; rise / fall; heater R; 3.4 / 2.3 dB derived PS loss; geometry incl. XTEM
  of PS3) and 550 nm SiN waveguide cutback (8.2 / 7.0 / 5.5 / 5.8 dB/cm). Fab org_amf. Not entered: projected losses
  (minimum-length design, cited platform loss), simulated 0.2-0.3 dB per MMI (1x2 vs 2x2 not distinguished).
- ozdemir2021 (8 / 39): imec InGaAs/GaAs MQW nano-ridge waveguide PDs on 300 mm Si, rows per p-plug pitch 0.3-4.8 um
  (Fig. 7 median internal responsivity at -1 / -2 V as author_estimate on the simulated 21 % coupling; Fig. 5
  fiber-referred slopes; Fig. 6 Rsat; 79 / 82 % IQE), site-A pooled row (dark current 0.05 pA at -2 V, ~5 fA at -1 V,
  1.98e-8 A/cm2), 150 um RF row (Cj 91 fF, Rs 884 ohm, RC 1.9 GHz derived). Fab org_imec. Conclusion attributes
  1.98e-8 A/cm2 to -1 V, text to -2 V (entered -2 V, noted).
- vivien2012 (1 / 10): butt-coupled lateral p-i-n Ge PD, 10 um (0.8 / 0.78 A/W, ~4 uA and 80 A/cm2 at 1 V, BW > 50 /
  > 67 GHz measured, ~120 GHz author_estimate). Fab empty (pilot line not named; authors at IEF, TU Vienna, CEA-LETI).
- ma2018 (3 / 10): mid-IR 1D grating slow-light waveguides: family row (average ng 9.4-15.5), tuned W 0.70a device (ng
  23 -> 33 at 3902.4 nm), TiN heater (~pi at 1.4 mA). Fab empty (passive voice). Per-variant plotted values not entered.
- morin2021 (3 / 20): 24 nm Si3N4 waveguides 0.8 / 2.8 um (0.93 / 0.9 dB/cm at 405 nm, 0.35 / 0.22 dB/cm at 450 nm),
  R 1531 um ring at 453 nm (Q_L 5.85e6, Q_i 6.0e6, FSR 20 GHz author_estimate). Fab empty (CMOS foundry not named).
- song2024a (11 / 52): imec SiN advanced vs circular bends R 15 / 20 / 25 um (Table III measured, Table II simulated),
  R 50 um circular (0.015-0.032 dB/90), 2.5 um waveguide (< 0.05 dB/cm), rings advanced R 15 (Q 5.8e3, FSR 12.4 nm,
  > 30 dB), circular R 15 (Q 5.4e3, FSR 12.9 nm), advanced R 25 (Q 5.5e4, 0.028 nm, FSR 7.4 nm). Fab org_imec. Cited
  0.08-0.4 dB/cm platform loss not entered.

## Judgment calls

- chen2024a QC-DC as splitter.directional_coupler (registry "tunable" DC, keeps split ratio) rather than
  switch_fabric.other; its endurance and level count then have no parameter (gap below). Coordinator may prefer
  switch_fabric.other by analogy with D158.
- PCM phase-shifter rows hold interferometer / ring-level values measured through their host (phase, ER, IL), as
  phase_shift_pi exists only for phase_shifter; rings with own Q / FSR got separate resonator rows.
- ozdemir2021: one row per plug-pitch design spanning device lengths (D165 population style) plus a pooled site-A row for
  the pitch-independent dark current; internal responsivity / IQE author_estimate (simulated coupling input).
- delaney2021 MZI IL values read off Supp. Fig. S3 (+/- 0.1 dB); figure is non-monotonic vs length, text says flat 2-3 dB.
- Reverse bias stored negative (vivien2012 "1 V" -> -1, ozdemir2021 as printed).

## Missing orgs

- Washington Nanofabrication Facility / Molecular Analysis Facility (chen2024a p.9 acknowledgements, "Part of this work
  was conducted at"): facility_org_ids blocked.
- MIT Materials Research Laboratory (ros2022 p.13, "fabrication facility support"): facility.
- Lincoln Laboratory Microelectronics Laboratory (ros2022 p.13): facility (owner org_mit_lincoln_laboratory is already
  the fab org).

## Registry gaps

- phase_efficiency_pi_per_um (phase_shifter): chen2024a 0.012 pi/um measured, 0.0125 simulated (p.2-3); ros2022
  0.09 pi/um simulated, 0.08 for longer cells (p.3, p.10). Def: phase shift per unit actuator length.
- loss_per_pi_db (phase_shifter): chen2024a ~0.4 dB/pi (p.3); ros2022 0.2 dB/pi excess, 0.3 dB/pi (p.1, p.3). Def:
  insertion loss change per pi of phase shift (distinct from the per-length loss rejected in D250).
- endurance_cycles and n_levels for splitter (or reclass the tunable DC): chen2024a > 5000 events, 52,600 total, 4 levels
  (p.5).
- forward_voltage_v for phase_shifter: chen2024a PIN heater turn-on ~0.8 V (p.2).
- waveguide_platform.slow_light: slow-light bandwidth at +/-10 % group-index variation (ma2018 23-66 nm, p.5), NDBP
  (0.093-0.164, p.5), period_nm and n_periods for waveguide_platform (a = 1.03 um, 303 periods, p.2).
- photodetector absorption coefficient alpha_per_um (ozdemir2021 Fig. 6: 0.124 / 0.21 / 0.272 per um; 0.088 per um
  without plugs, p.5); coupling_efficiency_pct and mfd_chip_um for photodetector facets (21 % and 0.42 um simulated, p.4-5).
- Not proposed (precedent rejections): PCM switching energy (ros2022 176 nJ, 388 nJ; D81), data-rate eye diagrams
  (vivien2012 40 Gb/s at 0 V).
