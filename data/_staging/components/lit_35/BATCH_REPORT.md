# Batch lit_35 report (distill subagent, 2026-10-29)

Dry-run `batch lit_35: +24 components, +134 metrics; errors 0` (one pre-existing WARN on merged ni2025b, not this
batch). All 8 cached texts match their source rows (title / authors on page 1); no garbled text layers. ASCII, no
e-mail addresses, no quotes. Row builder: scratchpad `distill_lit_35/build.py` + `rows_<paper>.py`.

## Per paper (components / metrics)

- chowdhury2024 (3 / 17): MACOM O-band DFB die in a DRIE trench, PWB to SOI (laser.dfb: threshold ~10 mA, 1.6 V,
  0.42 nm current tuning 25-50 mA, 1308.7 nm at 35 mA); same DFB PWB-to-fiber control (threshold ~7 mA, ~5 mW fiber);
  WBG Fabry-Perot cavity (resonator.bragg: Q ~52,500 benchtop / ~51,500 on-chip SFL, FSR 120 pm measured / 110 pm
  simulated, geometry). Fab: DFB rows org_macom (purchased-die vendor); cavity org_university_of_british_columbia
  (borderline: "SiEPICfab UBC in-house process flow", all authors UBC). Facility
  org_ubc_sbqmi_advanced_nanofabrication_facility (thanks to the facilities for fabrication and assembly). Not entered:
  PWB loss 3 dB (cited from ref. 15), Y-branch 1 dB excess and GC 15 dB (loss-budget guesses the paper itself finds
  15-20 dB short), path-level -65 to -70 dBm, 20 pm OSA-limited width (D250), on-chip FSR 160 pm (thermal-crosstalk
  artifact, note). PWB itself has no isolated value: no row.
- pfister2025 (3 / 12): 330 nm LPCVD SiN waveguide (98.0 % full-length transmission -> 0.088 dB derived), 2x2 MMI
  (94.8 % -> 0.232 dB excess derived; split 57.5:42.5 at 1528.1 nm), 3D-printed lensed side coupler
  (micro_optics.facet_lens, 66.4 %, R = 28 um, 230 um taper). Fab org_university_of_munster (contributions: D.W. made
  the SiN sample and 3D prints; MNF tools, D83c). Wavelength inferred 1528.1 nm (QD line; measurement wavelength not
  stated). Not entered: PWB transfer ratio 28.6 +/- 8.8 % (see gaps; PWB therefore has no row), QD microlens (design
  geometry only), total PIC 61.7 % (product).
- yulaev2024 (3 / 11): MS-PIC emitter (free_space_emitter.metasurface: -6.2 dB fiber-to-surface-normal -1st order
  measured, abstract prints -6.3; metasurface 2.4 dB simulated; 130 um 1/e2 beam; 0th / -2nd orders ~10 / ~13 dB down
  as slsr_db; surface-normal 0 deg), grating emitter (2 dB simulated, ~11.2 deg in glass author_estimate as origin not
  stated, (300 um)^2), SiN edge coupler (2 dB simulated). Fab org_national_institute_of_standards_and_technology
  (borderline: "we fabricated", every author lists NIST, two also UMD); facility
  org_center_for_nanoscale_science_and_technology ("performed in part at"). Not entered: round-trip -16 / -13 / -3 dB
  (system level with vapor cell and mirror).
- fang2006 (2 / 14): hybrid AlGaInAs-Si evanescent FP laser (laser.heterogeneous, platform other: 65 mA, 1.8 mW
  fiber, T0 39 K, 2 V threshold voltage as forward_voltage_v, 7.5 ohm, 40 K/W derived, ~1577 nm, 0.38 nm mode
  spacing, geometry); facet-to-lensed-fiber coupling 6 dB measured (fiber_chip_coupler.edge). Fab empty (UCSB + Intel,
  passive voice; thanks to individuals). Not entered: DQE 12.7 %, max lasing temperature 40 C, modal loss 15 /cm,
  ng 3.68, projections, 36-laser array family values (D254).
- girardi2025 (2 / 19): photonic-molecule soliton microcomb (laser.comb: conversion efficiency mean 50.7 % n = 49,
  range 24-63 %, best 63 %; ~100 GHz; 100 lines) and the coupled rings (resonator.coupled_rings, D396: most probable
  k0 13.5 MHz over > 9000 resonances, Qi 14.2e6 and 0.026 dB/cm derived, FSR 99.7 GHz simulated, design FSR 100 /
  380 GHz author_estimate, R 227.82 / 60 um, 1.8 um width, 3 um BOX / cladding, 200 nm TiPt). Fab
  org_chalmers_university_of_technology (contributions). Not entered: 25th percentile 50.3 % and mode 53.7 % (no
  statistic), rep-rate std 20 MHz, beta2, Fig. 2(c) k0 13.8 MHz (resonance wavelength not stated), histograms.
- hakobyan2025 (1 / 9): double-plasmon QCL comb (laser.comb, inp: 350 mW at -20 C / 70 mW at +50 C, T0 110 K,
  ~1875 cm-1 -> 5333 nm derived, 7.565 GHz intermode beat as channel_spacing_ghz (D83b, not pulsed), 210 modes
  derived, 6 mm x 6.15 um, 1.573 um active). Fab empty (all authors Alpes Lasers, passive processing only). Not
  entered: T1 100 K, ~53 cm-1 span, beatnote < 1 kHz, 1.65 mW per mode, simulated GVD / loss, 4 um design.
- verdier2017 (7 / 32): III-V/Si tunable ECL (laser.tunable: 20 mW fiber, 5-15 dBm facet over the range, 95 mA,
  0.05 W/A derived, 95 nm, ~50 mW heater, SMSR > 35 dB, 550 kHz, WPE 3 %), III-V/SiO2 tunable ECL (10 dBm, 66 nm
  discrete / 62 nm continuous author_estimate, 60 / 180 mW, SMSR ~50 dB, < 5 dB power variation, 1 kHz, 10 pm mode
  spacing author_estimate, 62 nm Vernier FSR simulated), RSOA (amplifier.soa: 27 dB fiber-to-fiber at 400 mA,
  wavelength inferred ~1590 nm from Fig. 7(a), 3 mm x 5 um), RSOA-Si SSC butt coupling (~2 dB simulated read off
  Fig. 6, 150 um, 0.18 um tip), RSOA-PLC butt coupling (~2 dB measured), Si waveguide (~2.5 dB/cm), Si racetrack
  (FSR > 22 nm design, D400). Fab empty (III-V Lab / Nokia Bell Labs / LPCNO, passive). "Laser power efficiency 3 %"
  entered as wpe_pct with the printed wording in notes (judgment).
- chang2022 (3 / 20): fabricated 3D TWC DUT (fiber_chip_coupler.edge: headline ~85 % / ~0.8 dB derived via
  T = sqrt(eta Ttot), wavelength inferred 852 nm; TE > 80 % at 852-935 nm; 780 nm TE 74 / TM 71 % read off Fig. 2(b);
  simulated TE 87 / TM 83 % at 852 nm read off curves; 1-dB tolerance ~1.2 um TM; 50 nm facet, ~170 um taper, BOX
  2.2 / clad 3.5 um, W 6.2 um as overlay_width_um), symmetric 8 um design (row_kind design: ~95 %, 120 nm, 380 um),
  bus waveguide (0.06 dB/mm "estimated" -> 0.6 dB/cm author_estimate, 1 um, 4 mm). Fab org_purdue_university ("we
  fabricated", all Purdue).

## Missing orgs (name as printed + locator)

- SiEPICfab (MPW / in-house process, chowdhury2024 p.3, p.13 Sec. 4): would be a fab org (D83d); UBC entered instead.
- 4D Labs at Simon Fraser University (chowdhury2024 p.13 Acknowledgments): facility.
- Muenster Nanofabrication Facility (MNF) (pfister2025 p.5 Acknowledgments): facility.
- Myfab Chalmers (girardi2025 p.15 Acknowledgments, "fabricated at"): facility.
- Alpes Lasers SA (hakobyan2025 p.1 affiliation): no fab statement, not needed for a row.

## Judgment calls for the coordinator

1. pfister2025 PWB microlens-to-SiN transfer ratio 28.6 +/- 8.8 % (9 bonds, cryogenic) is relative to bare-microlens
   collection into NA 0.6, not a coupled power fraction: not entered as coupling_efficiency_pct; the PWB has no row.
2. chowdhury2024 cavity fab = UBC on the SiEPICfab "UBC in-house" wording (borderline); yulaev2024 fab = NIST (all
   authors list NIST, two also UMD).
3. chowdhury2024 WBG FP cavity class resonator.bragg (not photonic_crystal).
4. yulaev2024 combined measured -6.2 dB (edge coupler + expander + grating + metasurface) placed on the metasurface
   emitter row as device_total with includes; diffraction-order suppression entered as slsr_db.
5. chang2022 headline 85 % / 0.8 dB has no stated wavelength (852 nm inferred); Fig. 2(b) TE symbols are 81-83 %.

## Registry gaps

- relative_coupling_ratio_pct (chip_chip_coupler): transfer efficiency relative to a stated reference collection;
  pfister2025 28.6 +/- 8.8 %, p.5.
- differential_quantum_efficiency_pct (laser): fang2006 12.7 %, p.5.
- max_operating_temperature_k (laser): fang2006 40 C c.w. lasing, p.5; hakobyan2025 comb operation to 50 C, p.7.
- modal_loss_per_cm (laser): fang2006 15 /cm (Hakki-Paoli), p.5.
- slope_efficiency characteristic temperature T1 (laser): hakobyan2025 100 K, p.5.
- beam_divergence_deg for amplifier: verdier2017 RSOA far-field FWHM 16 / 19 deg, p.3 Fig. 5(b).
- group_index for laser: fang2006 3.68, p.7.
- intracavity filter FWHM for laser (bw_fwhm_nm): verdier2017 13 pm simulated, p.3.
- comb spectral span (laser): hakobyan2025 ~53 cm-1, p.5 (D81 deferred).
