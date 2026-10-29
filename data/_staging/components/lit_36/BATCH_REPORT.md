# Batch lit_36 report (distill subagent, 2026-10-29)

Dry-run `batch lit_36: +33 components, +211 metrics; errors 0`. ASCII, no e-mail, no quotes. Page-1 title / authors of
all 8 cached texts match their source rows; no garbled text layers. Table / figure values read from page renders where
the text layer lacks them (lischke2021a Table 1, wilmart2020 Table I and Fig. 3-5, jiang2020 Fig. 2 / 17, gallacher2018
Fig. 4).

## Per paper (components / metrics)

- jiang2020 (5 / 13): piezoelectric nanobender-tuned Y-cut LN zipper photonic-crystal cavities as
  `resonator.photonic_crystal` (tuned cavity, abdulla2011 MEMS-ring precedent; the phase shifter / coupler of Fig. 5 is
  simulated outlook only): L = 15 um tethered device (DC 5 nm/V, AC ~50 nm/V on mechanical resonance and 25 / 46 nm/V at
  550 / 750 kHz, all nm -> pm derived; Q ~1.7e4, linewidth ~90 pm, wavelength read off the Fig. 2(c) axis, inferred),
  L = 22 um device (63 nm tuning range at 4.5 V), 90-deg rotated control (0.04 nm/V), cryo device (194 pm RT -> 16 pm at
  ~4 K), lensed-fiber edge coupler (~50% typical, per_facet, C band inferred). Fab Stanford (author contributions),
  facilities SNSF + SNF. Not entered: mechanical Q ~20 / 18 / ~1000 at 5 mbar, mechanical resonances ~1 MHz (no resonator
  parameter), Vpi ~1 mV (author formula), Fig. 2(e) L-sweep (plot), phi = 0 comparison ~1 nm/V (device not tied),
  simulated displacements / zigzag table.
- de2020 (3 / 14): SiGe resonant ring PD in 45 nm SOI CMOS (`photodetector.ge_waveguide`: 0.043 / 0.068 A/W at 0 / -2 V,
  1274 nm, ref_plane on_chip from the "input power into the photodetector" caption; 17.8 / 14.5 GHz; dark < 10 pA derived;
  ring / SiGe geometry), the same ring as `resonator.ring` (D396: Q_L 5000, ER ~15 dB), broadband GC (~10 dB,
  per_coupler, author_estimate, O band inferred). Not entered: projected ~0.5 A/W near 1180 nm, Q ~9000 and 2-5 GHz of
  standard-doping devices (ref. [5] data).
- hu2021a (3 / 14): lateral Si3N4-waveguide-coupled Ge PD (0.61 A/W at 1550 nm, best ~0.9 A/W at 1480-1485 nm, simulated
  0.92 A/W and QE 98% at 1410 nm, 54 / 27 GHz at -3.3 / -1.1 V, Ge / Si geometry), Si3N4 1x2 MMI (-1.1 dB "insertion
  loss" entered as excess_loss_db 1.1, both outputs feed the PD; author_estimate, origin not stated), Si3N4 waveguide
  (< 3 dB/cm typical, author_estimate). Fab empty (commercial 90 nm platform, foundry not named). Not entered: SSC
  -2.5 dB/facet (cited [29]), type A 32% / 0.36 A/W (own earlier work [28]), simulated design variants A / B / D and
  sweeps, eye diagrams.
- liao2011 (2 / 35): Kotura evanescent vertical p-i-n Ge PDs type A (1.6 x 10 um) and B (6 x 10 um): responsivity at
  1550 / 1530 / 1620 nm and type A mean over 1520-1570 nm (derived: detector power calculated from measured coupling /
  propagation loss and a nominal 1% tap), dark current, dark-current density (derived; printed values not reproducible
  from current / area, noted), bandwidth 22 / 36 GHz (A) and 20 GHz (B), R and C, geometry. Fab empty (passive; Kotura +
  Oracle authors). Conclusion's 4.6 nA vs body 2.6 nA noted (body entered). Not entered: BeamPROP absorption fractions,
  computed RC / transit limits, earlier 0.56 A/W device [11].
- lischke2021a (3 / 35): IHP Ge-fin PDs Ge100_10 / Ge150_10 (265 / 240 GHz heterodyne at -2 V, 1 mA; > 70 GHz at 0 V;
  C at -2 V (and 0 V for Ge100_10); series R 8.3-9.2 ohm (range printed jointly for both, entered on both); internal
  (derived, GC loss removed) and external responsivity, internal / external QE (fraction -> % derived); dark < 200 nA RT
  and < 1 uA at 85 C (stated for both diodes); fin geometry), uniform 1D GC test structure (3.9 dB loopback_half derived,
  ~40%, 6 chips). Fab IHP (author contributions + own pilot line; no facility). Not entered: Table 1 calculated fRC /
  fTT / f3dB, bandwidth-efficiency product, 1-dB bandwidths, "no saturation up to 2.5 mA" (device not tied),
  Supplementary Fig. 2 (not cached).
- desiatov2019 (4 / 26): visible X-cut TFLN pulley ring (Q_L at 637 / 730 / 800 nm and 1450-1650 nm; Q_i as
  author_estimate per D403; linewidths 61 MHz / 1.2 GHz / 2.7 GHz from Fig. 3 labels), rib waveguide (<= 6 dB/m at 635 nm
  -> 0.06 dB/cm, ring_extraction, author_estimate; geometry incl. sidewall 62 deg derived from 28 deg off vertical),
  Y-splitter (0.21 dB excess derived from the 3.21 dB/splitter cascade slope; MZI ER ~30 dB best, > 15 dB), facet / lensed
  fiber edge coupling (6-10 dB per facet typical). Facility CNS; fab empty ("we fabricated", authors at Harvard,
  HyperLight, CityU). Text Q wavelengths 730 / 800 nm vs figure labels 733 / 803 nm noted.
- gallacher2018 (1 / 9): Ge-on-Si rib waveguide 4 um (long-wave mid-IR): < 5 dB/cm TE 7.5-11 um and TM 7.5-10 um, ~1 dB/cm
  TE 10-11 um, < 3 dB/cm 9.25-11 um (polarization unspecified); FP-fringe method with modeled Fresnel reflectance =
  measured (D394); geometry. Platform `other` (Ge-on-Si). Fab empty (see missing orgs); IQE Silicon grew the Ge film
  (note only).
- wilmart2020 (12 / 65): CEA-Leti 200 mm platform with / without H2 smoothing anneal: rib 350 (O), strip 400 (O + C),
  deep rib 320 (O), rib 450 (C) waveguides as separate smoothed / unsmoothed rows (Table I medians + std, Fig. 3(c) / 3(g) /
  4(a) single-die fit labels, geometry), rib bends R = 25 um (0.02 vs 0.04 dB/90, band unspecified), O- and C-band GCs
  (median center 1314 / 1554 nm from Fig. 5 maps; IL ~2 dB and 1-dB BW ~20 nm stated once for "the" GCs, entered on
  both GC rows with a note). Fab org_cea_leti (pilot line stated). Not entered: DC split ratio (only a relative 3%
  median shift), MMI / transition "no impact" statements, outer-ring wafer region values.

## EO-atlas candidates (not entered here, skill rule 2)

desiatov2019 visible TFLN MZM: Vpi 8 V for 2 mm at 850 nm, VpiL 1.6 V cm, EO bandwidth 10 GHz (detector limited),
electrical S21 17 GHz (p.4 Fig. 5). wilmart2020 Si depletion MZM 1 mm: median IL 1.7 dB smoothed vs 3.3 dB unsmoothed
(GC de-embedded), VpiL 1.62 vs 1.58 V cm, doped deep-rib loss 7 vs 8.8 dB/cm (p.5 Fig. 7). Neither paper is in the EO
atlas.

## Missing orgs

- University of Glasgow (gallacher2018 p.8 acknowledgements: staff of the James Watt Nanofabrication Centre thanked for
  assistance with the fabrication -> D84b borderline fab org; also reported for zhang2017). fab_org_ids left empty.

## Judgment calls for the auditor

1. jiang2020: tuned zipper cavity as resonator (not phase_shifter.mems); AC tuning coefficients in
   tuning_efficiency_pm_per_v with the drive frequency in condition.
2. de2020: fab org_globalfoundries borderline ("fabricated in the same 45 nm SOI platform" = GlobalFoundries 45 nm SOI).
3. liao2011 responsivities `derived` (calculated detector power with a nominal 1% tap); author_estimate is the
   alternative if the tap ratio counts as an assumed input.
4. lischke2021a: series resistance range and dark-current bounds printed jointly for both diodes entered on both rows.
5. wilmart2020: GC IL / 1-dB BW stated once for O- and C-band GCs entered on both rows (alternative: note only, D254).
6. hu2021a MMI "insertion loss" 1.1 dB stored as excess_loss_db.

## Registry gaps

| parameter / enum | class | skipped value, locator | proposed definition |
|---|---|---|---|
| mech_resonance_khz (allow) | resonator | jiang2020 bender-zipper mechanical resonances 550 / 750 kHz (p.24 Fig. 17), ~1 MHz (p.5) | mechanical resonance frequency of an opto-mechanically actuated resonator |
| mechanical_q | resonator, phase_shifter | jiang2020 Qm ~20 in air (p.5), 18 at atmosphere and ~1000 at 5 mbar (p.21) | quality factor of the mechanical actuator / resonator mode (pressure, temperature in condition) |
| bandwidth_efficiency_product_ghz | photodetector | lischke2021a 63 / 86 GHz (p.4 Table 1) | 3-dB bandwidth x quantum efficiency as reported (internal / external in condition); not gbp_ghz |
| bw1db_ghz | photodetector | lischke2021a 1-dB bandwidth > 60 GHz at -0.25 V and > 67 GHz up to 3.2 mA (p.4-5) | 1-dB electrical / OE bandwidth (bias, photocurrent in condition) |
| sidewall_roughness_nm | waveguide_platform | desiatov2019 0.7 nm RMS over 3 x 0.1 um (AFM, p.2) | RMS sidewall roughness (method, area / correlation length in condition) |
| platform enum ge_on_si | - | gallacher2018 Ge-on-Si rib (platform `other`) | Ge epitaxial guiding layer on Si substrate |
