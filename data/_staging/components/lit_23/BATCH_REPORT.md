# Batch lit_23 report (distill subagent, 2026-10-29)

Dry-run `batch lit_23: +20 components, +152 metrics; errors 0`. ASCII only, no e-mail addresses, quotes limited to a few
words. Not yet audited or merged.

## Per paper (components / metrics)

- taddei2019 (4 / 13): 8-ring CROW flat-top bandpass filter as wdm.mrr (jeong2013 precedent): 3-dB bandwidth 72 MHz
  -> 0.072 GHz derived (D256), out-of-band rejection >= 51 dB as crosstalk_db (noise-floor limited), overall IL 13 dB
  (scope unspecified: whether the ~3 dB/facet coupling is included is not stated), design FSR 1.4 GHz, Table I
  Butterworth coupling coefficients chi0..chi8 as simulated power_coupling_pct. Ring 1 in the first-order notch setting
  (separate resonator.ring row so finesse can be entered): FWHM 14 MHz, finesse ~100 derived. Waveguide loss 0.014
  dB/cm author_estimate (model fit to the filter IL). Fiber-array facet ~3 dB/facet (D167). No measurement wavelength
  stated anywhere: band unspecified + note. Not entered: shape factor 1.93 and group-delay variation ~2 ns (no
  parameter), 0.7 GHz retuning demo, 21 cm optical roundtrip (optical, not physical length), chip 55 x 35 mm. Fab
  empty ("we have fabricated", authors over MESA+ / Twente, LioniX, Monash).
- teng2009 (2 / 18): 350 nm SOI racetrack (R 15 um, Lc 2 um, gap 180 nm) as two rows, air-clad and PSQ-LH polymer
  overlay (shen2024 precedent): drift 54.2 / -4.9 pm/K (linear fit, measured), bend-waveguide loss ~300 / ~50 dB/cm
  and coupling 50 / 75% (Lorentzian fit extraction, derived, D76), geometry. Wavelengths read from Fig. 4 / 5 axes
  (wavelength_inferred). Not entered: simulated ideal width 306 nm and +60 pm/C for 500 nm (design curves), loss values
  of [15,16,18,19] (cited), athermal MZIs (no numbers), shallow-etch GCs (geometry only). Fab org_cea_leti
  (acknowledgement: fabricated by CEA-LETI through ePIXfab).
- zheng2026a (2 / 9): Ta2O5 PLACE microring R 300 um (platform other): QL 2.74e6 measured, Qi 4.47e6 and 0.0732 dB/cm
  derived (stated formulas, n_eff 1.86), geometry (4.0 um / 1.2 um widths um -> nm derived). Lensed-fiber butt coupling
  ~13% per facet. Resonance wavelength ~1552.4 nm read from the Fig. 4(a) zoom box. Not entered: AFM rms roughness 0.46
  nm (intro prints 0.47 nm; no parameter), 8.7 um gap (only in the coupling simulation), TF 95% (inconsistent with the
  ~0.09 dip in Fig. 4(b)), Table 1 rows of other works. Fab empty (ECNU / SIOM authors, passive wording).
- kim2021 (2 / 15): 2x2 3-dB adiabatic coupler (220 nm SOI rib, 110 nm etch): EL < 0.23 / < 0.17 dB (I1 / I2, 16-stage
  cascade / 16, derived), simulated EL < 0.1 dB, unbalanced-MZI extinction > 25 dB (I1), 23 dB (I2), > 30 dB
  (1500-1540 nm), geometry (Lc 23.2 um, total 46.7 um, gaps 200 / 640 nm, widths 400 / 550 nm). TE GC 6 dB/unit
  (loopback_half, D167). Not entered: splitting ratio 3 +/- 0.25 / 0.3 / 0.13 dB and simulated +/- 0.18 dB (registry
  gap below). Facility: National Nanofab Center (NNFC) missing from the registry; fab empty (GIST / DGIST).
- lin2026 (2 / 22): 34-port WDM 90-degree hybrid chip as wdm.cascaded_mzi (four identical 1x8 three-stage MZI lattices):
  3-dB width 120 GHz, adjacent / non-adjacent crosstalk 9.3 / 14.2 dB, per-channel IL 1.37-2.44 dB (excess_loss_db,
  de_embedded, 6 dB hybrid split removed by the authors: derived), uniformity 1.07 dB, ISP and ISW ranges (Table 1,
  il_nonuniformity_db), design grid 200 GHz, stage FSRs and arm increments, port counts, footprint 18.6 mm2. 90-degree
  hybrid (splitter.hybrid_90): phase error < 4 deg (1540.5-1552.5 nm per caption / text; abstract 1539-1552.5 nm and
  Fig. 2(b) axis 1530-1565 nm noted), 2.5 mW compensation power, 70 um bends. Channel span 1540-1553 nm from the Fig.
  2(c) axis. Not entered: simulated MMI IL / imbalance variations (< 0.3 / 0.5 dB, no splitter parameter for a
  wavelength variation), system metrics (SFDR, IMRR, BER, data rate). Fab org_applied_nanotools (MPW).
- singh2021 (1 / 6): adiabatic magic T in GF 45CLO as splitter.other: EL < 0.8 dB at 1550 nm and < 1.2 dB over
  1530-1600 nm (TE11 and TM11 inputs, GC-calibrated), simulated 0.3 dB, lengths 60 / 25 um, 100 nm exit gap. Not
  entered: 3 +/- 0.25 dB splitting (gap below), poly-Si 50-100 dB/cm (expectation), 45CLO edge coupling 0.7-1.4 dB
  (cited [11]). Fab org_globalfoundries (Pico test vehicle); Ayar Labs support thanks not a fab statement.
- tian2018 (5 / 54): 1x3 cascaded step-size MMIs S = 33 / 50 / 90% (split_ratio_pct approx, measured device
  designation; Port 2 / Port 1 imbalance 3.2 and 12 dB annotated in Fig. 7(b)/(c); IL < 1 dB over 1520-1570 nm),
  fabricated-series family row (S 25-90%, lowest IL ~0.2 dB at 1550 nm with the device unidentified, D165), Table 1
  geometry on each MMI row, SSC 2 dB/facet (200 nm tip, 200 um). Not entered: MMI1st sizes of the three selected
  devices (not stated; Table 2 is simulated D vs L1 / W1), simulated tolerances and 60 nm band, footprint < 15 x 15 um.
  Fab empty (BUPT / SIMIT, passive wording).
- frellsen2016 (2 / 15): topology-optimized TE0 / TE1 mux (2.6 x 4.22 um): IL < 1.2 dB per device over 1520-1620 nm
  (halved mux + demux, derived), crosstalk > 12 dB (cascade value), extinction ~17 dB at 1570 nm and > 14 dB C-band
  (mode-image line scans), simulated ER > 18 dB and loss < 1 dB, geometry. Three-mode mux (6.08 x 4.93 um): lowest loss
  ~1.7 dB (scope unspecified: halving not stated), 3-dB bandwidth ~80 nm, TE1 extinction > 14 dB. Fab empty (all
  authors DTU, passive wording).

## Orgs missing

- ePIXfab (teng2009 p.7 Acknowledgements: fabrication by CEA-LETI through ePIXfab; fab_org_ids set to org_cea_leti only).
- National Nanofab Center (NNFC), South Korea (kim2021 p.4 Sec. III: fabrication facilities used; facility_org_ids
  left empty).

## Judgment calls

- taddei2019 notch-configuration ring as a separate resonator.ring row on the same chip (finesse is resonator-only).
- taddei2019 / lin2026 / tian2018 / frellsen2016 conversions and authors' arithmetic entered as derived (D80a, D256).
- teng2009 and zheng2026a resonance wavelengths read from plot axes marked wavelength_inferred (schema "plot axis").
- lin2026 port-imbalance (ISW) kept on the WDM-OH row, not the hybrid row, because it is measured through the filters.
- tian2018 designed-unequal Port 2 / Port 1 ratios entered as imbalance_db (ghosh2012 precedent).

## Registry gaps

- split_deviation_db (splitter): maximum deviation of each output from the ideal split, +/- value as printed. Skipped:
  kim2021 3 +/- 0.25 dB (I1), 3 +/- 0.3 dB (I2), 3 +/- 0.13 dB (1500-1540 nm), p.5 Sec. III; singh2021 3 +/- 0.25 dB,
  p.1 Abstract / p.2. imbalance_db (|P1/P2|) would double-count or misstate these.
- shape_factor (wdm): ratio of the 40-dB to the 6-dB bandwidth as defined by the paper. Skipped: taddei2019 1.93
  (p.3 Sec. III).
- group_delay_ripple_ns (wdm): peak-to-peak group-delay variation in the passband. Skipped: taddei2019 ~2 ns (p.3
  Sec. III, Fig. 5(b)).
- surface_roughness_nm (waveguide_platform, resonator): rms surface / sidewall roughness, measurement (AFM / SEM) in
  notes. Skipped: zheng2026a 0.46 nm rms (p.5 Fig. 2(c)).
