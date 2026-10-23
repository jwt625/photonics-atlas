# Batch lit_06 report (distill subagent, 2026-10-22, transcribed by the coordinator)

Dry-run `batch lit_06: +57 components, +312 metrics; errors 0`. No emoji, e-mail or non-ASCII.

## Per paper

- deng2026 (5 / 22, imec iSiPP300, fab org_imec): 16x400 GHz ring-MZI (wdm.mrr), 64x100 GHz composite (wdm.mrr),
  half-ring MZI (wdm.cascaded_mzi), TOPIC ring (wdm.mrr), 4-ch interleaver. Not entered: FWHM 68+/-8 and 50+/-10 GHz
  (no GHz FWHM parameter), synthesized isolation >= 18.9 dB and 28.1 dB MZI ER (unfabricated, ref. 21), analytical IL
  0.54 / 4.21 / 0.62 dB, d-lambda/dL slopes, ~0.8 x 0.7 mm2 projection. Calls: heater 1.50 / 5.85 mW/pi
  author_estimate (heater design from ref. 8; D80i borderline); IL scope unspecified (normalization reference not
  stated).
- fu2023 (5 / 41, Si3N4 five-layer): 32x32 Thin-CLOS AWGR, 16x16 test AWGR, tri-layer vertical coupler
  (waveguide_platform.transition), interlayer crossing (crossing.multilevel, simulated only), 60 deg 150 um bend. Fab
  org_university_of_california_davis; facilities org_marvell_nanofabrication_laboratory and
  org_center_for_nano_micro_manufacturing (p.10). Calls: fab D80b borderline ("We fabricated", one co-author
  Politecnico di Torino); spectral roll-off as il_nonuniformity_db; coupler W0 / W2 / L1 / L2 roles from Fig. 3(c)
  labels, W1 = 1.4 um not entered (role ambiguous). Not entered: 4 um top cladding (ambiguous), ~1 dB system
  penalty.
- bogaerts2006 (8 / 44, imec 248 nm DUV, fab org_imec): GC, photonic-wire bends, 8x400 GHz AWG, 16x200 GHz AWG, 5-stage
  MZLF, racetracks R = 1 and 5 um, bend-coupled ring R = 5 um. Not entered: straight 0.24 dB/mm (cited), 8-ch AWG
  footprint (ref. 13), MZLF "bandwidth 2.6 nm" (undefined), "nearly 100 %" coupling, drop efficiency 50-70 %, "Q up to
  12000 for radii down to 2 um", 4-ch racetrack demux (geometry only), AWG transition 15-30 um (not allowed). Calls:
  fab org_imec (imec CMOS research environment + P-line operators, D84b); 8-ch AWG 8 dB / -7 dB entered (first
  reported 2004, stated here with figure, no citation); GC 33 % / 5 dB author_estimate; MZLF widths 565 / 535 nm
  measured (as fabricated); 220 nm gap design-or-measured not explicit.
- fujisawa2020 (4 / 30, fab org_hokkaido_university): two 4-lambda LAN-WDM MUX (wdm.other), excess loss per port
  with Table I lane wavelengths; two ADC TE0-TE1 mode muxes (mode_converter.mdm_mux). Not entered: MMI dims ("13 and
  3 um" order inconsistent), TE1-TM0 converter (ref. 13), 8-lambda average 1.86 dB (two components), ADC LB 35.4 /
  30.3 um (not allowed; notes), +/-2 / +/-5 nm tolerance (simulated). Call: ADC "about 2 dB / 1.7 dB" scope
  unspecified (two cascaded ADCs, per-ADC not stated).
- papadovasilakis2023a (11 / 44, fab org_globalfoundries MPW): 90 deg bend, three phase-balanced tapers (300 -> 500 /
  575 / 600 nm), five WICs (SR 0.50 / 0.29 / 0.20 / 0.08 / 0.04, simulated split only), CWDM FT500 and FT575. Bend
  and taper losses = per-component slopes in Fig. 10(a); FT575 IL 3.8 dB and crosstalk 22.1 dB from Table II "This
  work". Not entered: 2.72 dB budget, WIC normalized lengths, simulated spectral shifts. Calls: mean max channel
  shift over 5 wafer sites as wavelength_spread_nm; bend geometry (w 300 nm, R 10 um) from the WIC design (paper says
  WIC / routing bends).
- qiao2017 (9 / 49, fab org_semiconductor_manufacturing_international, SMIC 180 nm, 340 nm SOI): 32x32 and 8x8 Benes
  EO (carrier injection) switches, phase-bias and unbiased MZI units, 2x2 MMI, crossing, 10 % tap, GC, rib WG 5.3
  dB/cm (derived from 0.53 dB/mm). Not entered: Cross/Bar crosstalk difference, optimum voltages, crossing dims.
  Calls: PIN switch units in switch_fabric; MMI "insertion loss" as excess_loss_db (D43); MMI dims
  extracted_from_figure (caption says (e), render says (c)); worst-case IL 22.6 / 24.3 dB author_estimate.
- tanizawa2015 (4 / 19, fab org_national_institute_of_advanced_industrial_science_and_technology): 32x32 PILOSS TO
  switch, TM MZ element, 0-dB-DC intersection (FDTD only), TiN heater 281 ohm. Not entered: < -35 dB crosstalk
  bandwidths 4.3 / 2.3 nm, trimming 1.5 mW, DC gap 430 nm (not allowed; notes), CD-SEM sigma 0.9 nm, modeled sigma
  0.083 nm. Calls: fab D80b borderline (13/15 AIST, 2 Furukawa); total 2.93 W derived; fabric crosstalk >= 20 dB
  author_estimate (model).
- iwama2015 (2 / 13, fab empty: Furukawa, no statement): 1x93 LCOS WSS (switch_fabric.wss), PLC SSC array
  (micro_optics.other). Not entered: 0.5-dB / 3-dB passbands 37.0 / 45.5 GHz, super-Gaussian order 4.7, theoretical
  4.3 dB. Call: SSC 0.3 dB round trip scope unspecified.
- nakamura2020 (5 / 29, fab AIST, pilot line p.7): 1x2 fold-back WSS, fold-back AWG (Table III design), 1x4
  interleaver, 1x2 MZI switch, crossing; test-circuit losses Table IV. Not entered: Table IV optimized column,
  projected 7.83 dB, Tables I / II simulations, 0.024 / 0.028 dB intersections and 32x32 6.4 dB (refs. 16, 21),
  heater currents.
- ye2023 (4 / 21): 100 GHz Si3N4 ring 810 nm x 2.40 um (kappa0 14 / 17 MHz most probable, Q0, 2.6 dB/m -> 0.026 dB/cm
  derived), two soliton combs (laser.comb 100.17 and 19.975 GHz; pulse widths derived per D84c), inverse-taper edge
  coupler ~60 % author_estimate. Not entered: D2-D4, coupling ideality, kappa0 vs width plot, line count (117 text vs
  137 caption). Fab empty: Qaleido Photonics missing.

## Orgs missing from the registry

- Qaleido Photonics, Hangzhou (ye2023 p.1 affiliation; p.12 contributions "fabricated the samples") -> proposed
  fab_org_ids for all 4 ye2023 rows.

## Registry gaps (proposed)

bw_fwhm_ghz (wdm, resonator; deng2026); bw_0p5db_ghz and bw_3db_ghz for switch_fabric (WSS passband; iwama2015);
xt_bandwidth_nm (switch_fabric; tanizawa2015); drop_efficiency_pct (wdm, resonator; bogaerts2006); gap_nm for
switch_fabric and crossing; coupling_length_um for mode_converter; taper_length_um for wdm.
