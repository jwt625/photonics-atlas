# Batch lit_05 report (distill subagent, 2026-10-22, transcribed by the coordinator)

Dry-run `batch lit_05: +47 components, +297 metrics; errors 0`.

## Per paper

- nan2025 (1 / 6): crossing.multilevel (Ta2O5 over LN): 0.0017 dB mean of 5 ports at 1550 nm (Fig. 5(b); text
  "<0.002 dB"), crosstalk > 62 dB 1510-1630 nm plus 63 / 62 dB per direction; LN pitch 10 um, Ta2O5 300 nm. Not
  entered: interlayer coupler (simulated only; Fig. 3 contradicts caption / text), "Couple Loss" 13.13 / 15.21 dB
  (unexplained), p.6 "0.02 dB" vs Table 1 0.002 dB (typo). Call: fab East China Normal University borderline (D84a).
  Gap: 1.5 um SEM interlayer gap (gap_nm not allowed for crossing).
- bock2010 (6 / 31): SWG crossing B (pitch 300 nm) TE 0.023 / TM 0.037 dB (ASE), TE 0.025 / TM 0.045 dB at 1545 nm
  (laser), crosstalk > 40 dB; SWG crossing A (400 nm) TE 0.070 / TM 0.067 dB; direct wire crossing TE 0.975 / TM 0.763
  dB plus simulated 1.35 dB / 10.9 dB; SWG taper (mode_converter.converter) TE 0.296 / TM 0.485 dB cutback; Si wire
  TE 3.1 / TM 3.2 dB/cm; FDTD design crossing TE 0.36 / TM 0.21 dB; SEM pitch 300 nm, wire 400 nm. Not entered: PDL
  < 0.02 / < 0.005 dB, loss variation over wavelength, relative wire-crossing crosstalk. Fab none (NRC Canada / U
  Ottawa split). Missing: National Research Council Canada (org_national_research_council is Italian CNR).
- nevlacsil2020 (6 / 37): MMI crossings TE/TE, TM/TM, TE/TM ~0.05 dB at 840 nm (stated once, entered on each), < 0.16
  dB 790-890 nm, simulated crosstalk ~60 dB, Table 2 geometry; single-mode crossing reference TE ~0.45 / TM ~0.28 dB
  (Fig. 4, +/-0.02 dB), simulated crosstalk ~40 dB; arrayed crossings TE <= 0.05, TM <= 0.02 dB, simulated optimum
  spacing 6.65 / 13.05 um as pitch_um. Missing fab org: ams AG, Premstaetten (p.6 Sec. 3) -> fab empty.
- wang2026 (2 / 31): telecom crossing mean 0.07 dB 1260-1625 nm, <= 0.2 dB, best 0.03 dB near 1400 nm, crosstalk > 40
  dB 1500-1625 nm, simulated rows; visible crossing mean 0.063 dB (Table III measured), best 0.03 dB near 639 nm,
  crosstalk > 35 dB, simulated 0.048 / < 0.1 dB / > 44 dB; Table I/II geometry (W1 port_width_um, W2 mmi_width_um, L1
  taper_length_um, L2 mmi_length_um); derived footprints. Fab org_hangzhou_qoretek. Calls: abstract "-0.048 dB" is
  sim. in Table III; per-crossing "excess loss" as crossing_loss_db. Gap: crossing bandwidth (0.1-dB > 80 nm sim.).
- elsaeed2024 (5 / 37, fab org_imec iSiPP300): bent DC 0.5:0.5 (R 25 um, 8.5 deg) excess 0.003 +/- 0.013 dB cross,
  0.007 +/- 0.018 dB through (derived, from fitted At / Ac), coupling variation 0.051 over 80 nm, 0.023 over 50 nm;
  wafer map 0.055-0.081 (9 central dies), <= 0.112 (63 dies); simulated width tolerance 0.061 / 0.058; split ~50 %;
  straight DC 0.126 / 0.070 dB, variation 0.391; bent DCs 0.4 / 0.6 / 0.7 variation 0.023 / 0.038 / 0.034 over 50 nm.
  Spans read as 1260-1340 / 1270-1320 nm from axes (wavelength_inferred). Gap: coupling_angle_deg (splitter geometry).
- sheng2012 (3 / 14): 1x2 MMI 0.06 dB at 1550 nm (cascade), < 0.1 dB 1530-1570 nm, simulated 0.04 dB, 3.6 x 11.5 um,
  port 1.2 um; Si WG 2.4 dB/cm cutback (1550 nm inferred from GCs); GC pair 11.1 dB fiber-to-fiber, 5.55 dB half
  (derived). Fab none ("0.13-um CMOS line" unnamed; SIMIT + Grace). Missing: Grace Semiconductor Manufacturing Corp.
- xu2023a (2 / 12, fab org_globalfoundries 45CLO): SiN 2x2 MMI v1 / v2: paper IL -10log(Pbar + Pcross) as excess
  loss, median 0.07 dB at 1310 nm (14 and 8 wafers), < 0.25 dB O band (13 dies); median split 52.8 / 49.5 % (derived);
  footprints 1221 / 469 um2.
- huang2019a (2 / 10): polymer mode filter (mode_converter.other) IL at 1550 nm 29.7 dB (E11), 11.3 (E21), 12.8 (E12)
  fiber-to-fiber, geometry; TMF butt coupling (fiber_chip_coupler.edge) 1.9 (E21) / 1.7 dB (E12) per facet. Fab
  CityU borderline ("in-house"; one UESTC author). Gaps: mode_converter extinction_db (mode rejection 18.4 / 16.9 dB),
  bw_10db_nm (~190 / ~140 nm), RW2 -10 / -15 dB bandwidths 197 / 97 -> 182 / 90 nm at 66 C, period_nm 302 um, n_periods
  42.
- qi2025 (6 / 27): FP cavity between two Sagnac reflectors Q_i 2.0e6, FSR 19 GHz, intrinsic loss rate ~150 MHz;
  Sagnac extinction > 27 dB (derived from fitted Q_ext); MZI beamsplitter <= 0.07 dB per MZI (derived bound), 0.06 dB
  (author_estimate, subtracts cited 3 dB/m); 180 um DC 80 % (model fit); standard TOPS P_pi ~80 mW, 6 pm/mW, 25 ohm;
  undercut TOPS 2.5 mW, ~70 pm/mW. Not entered: Q_ext 40e6, 3 % round-trip loss, reflector "about 10 nm", TOPS
  bandwidth. Fab org_stanford_university ("We fabricate"; one Sandia co-author); facilities
  org_stanford_nano_shared_facilities, org_stanford_nanofabrication_facility. Gap: q_external.
- jayatilleka2021 (3 / 18, fab org_intel "We fabricated" + Fab11x thanks): trimmed ring (soi_rib, R 10 um) Q 4200 mean
  of 58, FSR 6.8 nm, post-trim spread <= 0.032 nm, std 0.009 nm (derived from pm), trim range 8.5 nm, 63 pm/K; ring
  without implant Q 6600; Ge-implant trimmer (phase_shifter.other) 0.3 dB excess (derived), 2.5 pi (derived). Not
  entered: VpiLpi 0.94 / 0.79 V cm, trim speed, anneal time, 55 GHz, 15 h bake (not retention, D83g).
- xu2022 (5 / 32, fab org_applied_nanotools): cavity series Q_i 3.4e6 (derived), best Q_L 2.1e6, finesse > 100, FSR
  < 0.16 nm, 0.18 dB/cm (derived), ER 2.6-5.7 dB, 60 pm/K, 5.6 pm/mW, simulated Q_i 4.1e6; 1.5 mm / 4.0 mm taper cavities
  Q_L 1.1e6 / 1.9e6, 1.4 / 0.8 pm; retroreflector ~99 %, 0.05 dB (derived), simulated 99.3 %, 0.01-0.07 dB; asymmetric
  TE0-TE1 coupler (splitter.directional_coupler) 1.7 % (derived), simulated values, geometry. Calls: series row from
  the whole array (max-Q cavity not identified); TE0-TE1 coupler classed splitter for gap / length.
- song2021a (6 / 42, fab org_imec): racetrack advanced bends R 2 um Q ~7800, 200 pm, finesse 175, FSR ~35 nm, ER > 11
  dB, simulated; R 3 um Q 19000, 80 pm, finesse 287, FSR 23 nm, ER > 10 dB; normal-bend racetrack Q 1900, 800 pm; bend
  loss R 2 um 0.012 (advanced) / 0.078 dB (normal) per 90 deg; poly-overlay GC > 50 % at ~1560 nm, 1-dB 28 nm
  (author_estimate), 10 deg. Not entered: R 3 um bend losses (cited). Calls: R 2 um bend losses measured (match Fig.
  2 measured points, note); nm -> pm derived.

## Cross-batch calls

crossing_loss_db for every per-crossing loss; unqualified Q -> q_loaded with note; fraction -> % derived (simulated
stays simulated).

## Registry gaps (proposed)

gap_nm for crossing; pdl_db for crossing; coupling_angle_deg (splitter); mode_converter extinction_db, bw_10db_nm,
period_nm, n_periods; q_external (resonator, wdm); bw_* for crossing.

## Orgs missing from the registry

ams AG, Premstaetten (nevlacsil2020 p.1, p.6 Sec. 3, fab role); National Research Council Canada (bock2010 p.1);
Grace Semiconductor Manufacturing Corporation (sheng2012 p.2).
