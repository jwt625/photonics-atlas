# Batch lit_01 report (distill subagent, 2026-10-22, transcribed by the coordinator)

Dry-run `batch lit_01: +47 components, +237 metrics; errors 0` (it also printed "115 pre-existing validator errors
elsewhere in the repo", from concurrent work; checked by the coordinator). ASCII only. Restricted sources: no quotes
beyond "begins to be amplified" (zhang2023a-m3); quotes only for open-licence li2025, shi2024, cheng2025.

## Per paper

- garciablanco2025 (5 / 30): Al2O3:Er EDWA (amplifier.rare_earth), TriPleX inverse-taper edge coupler, TriPleX WG
  loss, DC pump/signal WDM (wdm.other), Si3N4-to-Al2O3 vertical coupler (waveguide_platform.transition, simulated
  only). Not entered: ~80 nm gain bandwidth, Er concentration, spiral bend radius / spacing, ~1 um offset, Fig. 8
  spectral reads, Table 1 other works. Missing orgs (no fab statement): LioniX International BV (p.1, TriPleX p.4),
  University of Twente MESA+ (p.1), ALUVIA Photonics (p.1), CMAM UAM (p.11, RBS beam time). Calls: fab empty (chip
  "based on" TriPleX); ADS double-stripe core thickness not one number.
- zhang2023 (4 / 14): uTP InP SOA, III-V/Si taper (chip_chip_coupler.evanescent, > 90 % author_estimate), Vernier
  laser (laser.tunable), 1x2 MZI switch with SOAs (switch_fabric.other, crosstalk 20 dB). fab org_imec (SiPh at imec
  p.10) + org_ev_group (BCB spray coating p.5; could be note only). Not entered: switch IL 1.4 dB (cited [30]), 56 dB
  crosstalk reduction (improvement), differential resistances, ring FSR ~4 nm (fsr_nm not allowed for laser), BER.
- ronn2019 (7 / 15): three hybrid Er:Al2O3-Si3N4 slot amplifiers (250 / 700 / 1200 um rows), pump threshold 1.5-2.0
  mW, 1.98 dB overall net modal gain on 1200 um (derived); uncoated slot WG 4.49 dB/cm cutback; unpumped hybrid WG
  35.83 dB/cm; multimode strip edge coupler ~15 dB (author_estimate, scope unspecified); strip-to-slot converter <=
  0.5 dB author_estimate. Not entered: 20.1 / 52.4 / 63.8 dB/cm gain per length (no parameter), signal enhancement,
  confinement, ALD film 0.62 dB/cm. Missing: C2N (CNRS / Paris-Sud; p.1, p.9 contributions, WG fabrication),
  Micronova Nanofabrication Centre (p.9 ack, facilities). Call: fab org_aalto_university borderline.
- kuznetsov2025 (4 / 31): GaP OPA 780 nm width fiber-to-fiber net gain up to 25 dB, internal 35 dB, IL 10-12 dB; GaP
  OPA 790 nm width output > 125 mW (20.97 dBm derived), 220 mW on-chip, NF ~6 dB off-chip, < 4 dB on-chip
  (author_estimate), comb gain > 20 dB, internal > 30 dB; GaP spiral 0.8 dB/cm (OFDR, S-L); inverse taper 2.5 dB per
  facet derived. fab org_ibm_research_zurich, facility BRNC. Not entered: > 10 dB net-gain bandwidth 70 / 140 nm,
  beta2, gamma, 9 % conversion, dynamic range. Platform other (GaP).
- li2025 (2 / 17): Er:TFLN EDWA fiber-to-fiber net gain 18.1 dB, NF 4.9 dB, output ~13 dBm, threshold ~10 mW,
  simulated on-chip 24 dB; SiON SSC < 2 dB per facet, > 90 % overlap derived, 3 x 3 um (SEM). fab empty (passive);
  NanoLN wafer supplier note. Not entered: 78 dB enhancement, lumped 3 dB/facet incl. splice. Platform lnoi_rib.
- vazquezcordova2014 (4 / 27): spirals 12.91 cm (1.92e20) and 24.45 cm (0.95e20), ~20 dB internal net gain, Psat_out
  -4.27 / -7.75 dBm, NF 4.58 / 3.75 dB; channel WG 0.19 dB/cm mean, 0.08-0.41, 0.16 / 0.17 per sample at 1320 nm
  (scattered-light, direct); butt coupling ~10 / 8 / 16 % per facet (derived). Not entered: -4.05e-3 dB/C, other 21
  spirals. Length printed 24.4 / 24.5 / 24.45 cm.
- zhang2023a (3 / 18): Er/Yb LNOI amplifier 7.85 / 6.46 dB net internal gain, ~0.1 mW onset (ambiguous, noted); R100
  ring Q_L / Q_i at 974 and 1531 nm, 0.73 / 0.95 dB/cm derived; cleaved facet 9.73 / 8.66 dB per facet derived. fab
  empty ("we manufactured"; Nankai + JUST; org_nankai_university exists). Not entered: 15.70 dB/cm, 10 % conversion.
- mckenna2022 (3 / 26): PPLN racetrack SHG as resonator.ring (Q_L / Q_i FH and SH, FSR ~17 GHz); PPLN OPO as
  laser.other threshold 0.073 mW at 765.8 nm; laser-diced facet typical 25-40 % / 10-20 %, devices 13 / 37 / 26 / 11
  % (derived). fab org_stanford_university, facility org_stanford_nano_shared_facilities. Call: not
  frequency_converter (class allows no Q, threshold, absolute efficiency). Not entered: 12 % SHG at 390 uW,
  cascaded OPO 690 uW, 11 % OPO, OPO-mode Qs, poling 3.7 um.
- shi2024 (2 / 7): LPLN SHG (frequency_converter.shg) 4615 %/W/cm2 -> 288.4 %/W (derived, x L^2); lensed-fiber
  coupling 4.9 dB per facet. fab org_a_star_institute_of_materials_research_and_engineering. Not entered: 0.18
  nm/C, -0.32 nm/nm, photon-pair source metrics.
- cheng2025 (7 / 12): AO isolators A / B isolation 12.4 / 28.1 dB, IL 2.16 / 8.09 dB (de_embedded); AOM frequency
  shifter as mode_converter.converter 4.6 dB conversion loss; two-ridge WG loss per mode (liquid / vapor HF);
  AOM-to-two-ridge transition 0.65 dB (waveguide_platform.other); DC mode mux crosstalk > 40 dB (narrow window). fab
  org_sandia_national_laboratories. Not entered: 10-dB isolation bandwidth 5.8 / 16 nm, 31 nm nonreciprocal band,
  contrast 61 / 48.7 dB, dual-waveguide device. Conflicts: Supp. Table III vs main text (5.6 vs 5.8 nm; -12.29 dB
  AOM efficiency vs IL).
- song2025a (3 / 20): three nonreciprocal.circulator rows with measured + simulated isolation / IL: 3-port 19 dB / 12
  dB, 4-port router 12 / 15 dB, 5x5 router 16 dB isolation. fab empty. Not entered: crosstalk -19 / -16 / -18 dB (not
  allowed). Calls: routers as circulators; IL scope unspecified.
- starnault2026 (3 / 20): C+L circulator (13 mm MZMs, AM-AM) 25.8 dB peak, >= 23, >= 15 fixed, 39.3 dB carrier;
  O-band circulator (10 mm, AM-FM) 37.4 / > 30 / >= 15 / 41.3 dB; HyperLight edge coupler < 1.5 dB per facet
  author_estimate. Excess losses on_chip_excess, passive / total unspecified. fab org_hyperlight; platform empty. Not
  entered: MZM Vpi / EO bandwidth, RF drive, BiDi link. Conflicts: 102 vs 104 GHz; 5.8 vs 6.57 dB.

## Registry gaps (proposed)

gain_db_per_cm (amplifier); gain_bandwidth_nm (amplifier); isolation_bw_nm (nonreciprocal) + crosstalk_db for
nonreciprocal; power_conversion_efficiency_pct (amplifier, frequency_converter, laser); frequency_converter: q_loaded,
q_intrinsic, fsr_ghz, pump_threshold_mw, thermal_drift_pm_per_k, conversion_efficiency_pct_per_w_cm2; poling_period_um
for resonator and laser (then mckenna2022 -> frequency_converter); q_loaded / q_intrinsic for laser; fsr_nm for laser;
photon-pair source parameters; subtype nonreciprocal.other; modulator metrics on non-EO lit papers (starnault2026).
