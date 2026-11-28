# Batch lit_316 report

Papers: lit:rogers2021, lit:doylend2011, lit:he2019a, lit:papp2014, lit:hulme2013. Distilled 2026-11-28.
Validation: `merge_component_staging.py data/_staging/components/lit_316 --dry-run` -> +19 components, +92 metrics,
0 errors (the 2 warnings are in other batches: guo2024a, ni2025b).

Page-1 title checks: all five texts match their source rows; none is a correction / erratum; no garbled text layer.
lit:rogers2021 is the arXiv preprint (2008.02411v3, 18 p, dated 2020-07-27, v3 2020-11-11) of the Nature 2021 paper:
all values come from the preprint only (Nature version not read), locators are preprint text.md pages; this is stated in
every rogers2021 component note. The other four are Optica open-access publisher copies. rogers2021 Extended Data Fig. 1
has no page render in `figures/`; page 14 was rendered from the cached PDF into the batch scratch folder to read it
(heater-power axis in arbitrary units, so nothing was read off it).

## lit:hulme2013 (5 components / 36 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_hulme2013_vernier_ring_laser | laser.tunable | other | tuning > 40 nm and SMSR > 35 dB over it; SMSR > 45 dB at 1575 nm; linewidth 338 kHz (derived, Hz); max on-chip 3.3 mW (derived, coupling loss subtracted); threshold 160 mA; > 0.45 mW over the tuning range; fine tuning 2.5 nm; FSR passive full cavity 0.16 nm (measured) / 0.21 nm (calculated); Vernier FSR > 32 nm (measured) / 37 nm (calculated); gain length 1360 um. All active rows at the 100 C chuck (373.15 K) |
| cmp_lit_hulme2013_ring1_400um / ring2_420um | resonator.ring | soi_rib | FSR 1.60 / 1.53 nm measured, 1.74 / 1.66 nm expected (author_estimate); loss 5.1 / 3.5 dB/cm (derived from 0.20 / 0.15 dB round trip, ring_extraction, 1550-1590 nm inferred from the Fig. 3(a) span); power coupling 2.6 / 1.7 %; length 400 / 420 um; width 700 nm (derived), 500 nm Si, 260 nm etch, 1 um BOX |
| cmp_lit_hulme2013_si_rib_wg | waveguide_platform.straight | soi_rib | 2.52 dB/cm derived from the printed 0.58 cm-1 (cutback); 500 nm / 260 nm / 1 um BOX |
| cmp_lit_hulme2013_lensed_fiber_facet | fiber_chip_coupler.edge | soi_rib | 11.5 dB, scope unspecified (cutback intercept; per facet or total not stated) |

Fab empty on all rows: passive fabrication voice (p.3), "designed and fabricated" (p.1), no first-person statement
(D80b). No facility (acknowledgment = discussions + DARPA grant).

Values not entered and why:
- Si / III-V transition loss 10 dB per transition and gain-section loss 11.7 cm-1 (p.4): the sentence attributes them to
  Davenport et al. [10] (the group's CLEO 2013 poster), rule 3 / D259.
- Total intracavity loss 45 dB (p.4): calculated from the cited terms; no laser parameter.
- Threshold current density 2350 A/cm2 (p.4): no parameter (registry candidate already listed in D433).
- Ring fit FWHM 0.022 / 0.020 rad (Fig. 3(b), (c)): no parameter in phase units.
- Heater tuning vs power (Fig. 5(b)): no slope printed; Heater 2 has no clear trend (thermal crosstalk).
- Design assumptions of Fig. 2 (3 dB/cm, 10 % coupling): simulation inputs.
- Full round-trip cavity length 3.3 mm (p.2): kept in the 0.21 nm row condition, not a second length_um row.

Judgment calls:
1. 0.58 cm-1 converted to 2.52 dB/cm as a power attenuation coefficient (x 4.343), basis derived, printed value and
   assumption in notes. Alternative: leave it in notes only.
2. Ring rows `test_structure: true` (the passive values were measured on separate polished, AR-coated passive devices,
   p.3) while the rows represent the intracavity rings.
3. Printed 5.1 / 3.5 dB/cm kept although 0.20 dB / 0.04 cm = 5.0 and 0.15 dB / 0.042 cm = 3.57 dB/cm; basis derived
   (the paper's own conversion, D80a).

## lit:doylend2011 (5 components / 26 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_doylend2011_opa_16ch | free_space_emitter.other | soi_rib | FOV 20 deg (psi, phase) and 14 deg (theta, wavelength); beam width 1.6 deg psi FWHM at 1555 nm, 0.6 deg theta (abstract) and 0.7 deg theta (p.10, theta = 35 deg) with conflict notes; 10 dB background suppression (slsr_db); emission angle 31 deg at 1555 nm; "grating efficiency" -14.1 dB entered as insertion_loss_db 14.1 de_embedded (derived); 1.9 dB MMI-tree + grating-array excess (author_estimate, rests on two calculated terms); 16 channels, 3.5 um pitch, 200 um grating, fill factor 0.5 (derived from 50 %), 75 nm grating etch |
| cmp_lit_doylend2011_test_grating_600nm | free_space_emitter.grating_emitter | soi_rib | 0.14 +/- 0.01 deg/nm over 1525-1625 nm (measured); 600 nm period; 75 nm etch |
| cmp_lit_doylend2011_to_phase_shifter | phase_shifter.thermo_optic | soi_rib | P_pi 215 +/- 15 mW (MZI test structure); 65 +/- 5 ohm (author_estimate: design vs measured not stated); heater 470 um |
| cmp_lit_doylend2011_si_rib_wg | waveguide_platform.straight | soi_rib | 3.0 +/- 0.2 dB/cm (Fabry-Perot fringes, method unspecified); 1000 nm (derived), 500 nm, 280 nm etch, 1 um BOX |
| cmp_lit_doylend2011_facet_lensed_fiber | fiber_chip_coupler.edge | soi_rib | 10.1 +/- 0.2 dB per facet, 1.7 um spot lensed fiber |

All optical rows TE (p.3). Wavelength-free loss rows carry `cl_band` inferred from the 1525-1625 nm operating span
(rule 8). Fab empty (passive voice, D80b); no facility.

Values not entered and why:
- Calculated side-lobe coupling 6.4 dB and substrate emission 5.8 dB (p.10): simulated loss-budget terms of the OPA
  with no matching parameter; in the OPA notes and in the 1.9 dB condition.
- Angular deviation > 2 deg (20-80 % duty cycle) and > 1.5 deg (100-900 nm grating width), Fig. 5 / p.5; Fig. 6
  far-field widths of the duty-cycle / width series: families of sibling test gratings, figure-only, no parameter for
  angular deviation.
- Secondary peaks at +/- 26 deg, +/- 10 deg usable range (p.8-9): the range is in the FOV condition.
- 430 mW per channel for 2 pi (p.7): twice the measured P_pi (a requirement). Thermal crosstalk (Fig. 7): relative
  temperatures, no parameter. Heater offset 6.5 um: reference points (edge / centre) not stated, so neither
  heater_offset_um nor heater_gap_um. NiCr/Au 72 / 75 nm: in core_material only.
- 1x2 MMI tree: no value of its own (only inside the 1.9 dB combined excess), no row.
- Hill-climber timing (100 iterations, 1.3 s per vector, < 2.5 min per point): control-system values.

Judgment calls:
1. The 0.14 deg/nm tuning efficiency is placed on the single test grating: p.4 says the individual-grating test
   structures were characterized "to assess wavelength tuning"; Fig. 4(c) also plots the array with a similar slope. If
   the auditor reads it as ambiguous (D159), move it to notes.
2. Grating efficiency -14.1 dB stored as insertion_loss_db 14.1, scope de_embedded (facet and 4 mm propagation
   subtracted, both measured on the Fabry-Perot test waveguide), method reference_structure, basis derived.
3. The 0.6 vs 0.7 deg theta beam-width conflict is kept as two rows with D417 notes.

## lit:he2019a (2 components / 6 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_he2019a_ln_microring_r100 | resonator.ring | lnoi_rib | loaded Q 2.2e6 (C band inferred, quasi-TE); FSR 199.7 GHz (measured dispersion); R 100 um |
| cmp_lit_he2019a_soliton_microcomb | laser.comb | lnoi_rib | repetition rate 199.7 GHz (single soliton, FROG period 5 ps); sech2 3-dB bandwidth ~27.9 nm; soliton-crystal line spacing 6.4 nm |

Facilities `org_cornell_nanoscale_facility` and `org_cornell_center_for_materials_research` ("performed in part at",
p.6). Fab empty: the main text has no fabrication statement (Supplement 1 not cached). Platform lnoi_rib from the
Fig. 1(c) cross-section schematic (rib with slab on SiO2, air above; yan2025 / D514 precedent); film thickness, width
and etch depth not in the main text.

Values not entered and why:
- D2/2pi = 1.76 MHz (dispersion; D81 rejected).
- Intracavity second-harmonic (bi-chromatic) comb near 778-786 nm, ~200 / 800 GHz line spacing (Fig. 2): no
  efficiency or power printed and no frequency_converter parameter for line spacing; no SHG row.
- Heterodyne beat SNR > 40 dB, two-soliton modulation period 12 nm, Raman shock time 6.3 fs (material fit),
  photorefractive switching behaviour: no parameters.
- Pump powers 33 / 23 mW on chip: conditions only.

Judgment call: repetition_rate_ghz 199.7 = the printed resonator FSR, because the paper says the single-soliton mode
spacing matches the FSR and characterizes the pulses by FROG (D83b; ding2026 precedent). Alternative: channel spacing
or notes only.

## lit:papp2014 (2 components / 4 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_papp2014_silica_wedge_disk | resonator.disk | silica | unloaded Q 63e6 (author_estimate, D403; C band inferred); radius 1000 um (derived from 2 mm diameter) |
| cmp_lit_papp2014_microcomb | laser.comb | silica | line spacing 32.9819213 GHz (measured clock output); ~2 ps waveform as pulse_width_fs 2000 approx (author_estimate, origin not stated) |

Fab empty ("fabricated on a silicon chip using conventional semiconductor fabrication techniques [21]", passive, process
cited). No facility: Kavli NanoScience Institute at Caltech appears only in the funding list (D80c / D83e, yi2015
precedent in D803).

Values not entered and why: 10 deg wedge angle (reference plane not stated, so not sidewall_angle_deg); resonator FSR
(not printed apart from the 33 GHz line spacing); ~20 nm microcomb bandwidth and the off-chip HNLF broadening to 200 nm /
25 THz (comb span rejected, D81; broadening is off-chip); 400 kHz injection-locking range, > 40 dB subcomb suppression,
Allan deviations (5e-9 at 1 s, < 2e-14 microcomb contribution, 1e-12 at 10,000 s corrected), 271 Hz RMS, > 24 h
operation, 108.0002(59) correlation slope: system / clock values without parameters. Seeding sideband levels and the
140 mW pump: setup conditions. Tapered-fiber coupler: setup, no value.

## lit:rogers2021 (5 components / 20 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_rogers2021_to_mzi_switch | switch_fabric.other | soi | 2.1 dB per switch layer (estimated, author_estimate); 9.1 us on / 12.1 us off transient (printed "90% - 10%"); 40 mW average power (derived, W); heater length 1000 um (derived from 1 mm) |
| cmp_lit_rogers2021_tx_switch_tree_1x16 | switch_fabric.other | soi | 10.9 dB total on-chip loss (4 x 2.1 + 1 routing + 1.5 grating; author_estimate); extra 2 dB two-photon absorption (on_chip_excess); ~160 mW; 1 x 16 |
| cmp_lit_rogers2021_rx_lo_switch_tree_1x8 | switch_fabric.other | soi | ~120 mW; 1 x 8 |
| cmp_lit_rogers2021_tx_grating_coupler | free_space_emitter.grating_emitter | soi | 1.5 dB loss-budget term (author_estimate) |
| cmp_lit_rogers2021_rx_pixel_balanced_ge_pd | photodetector.ge_waveguide | soi | receiver readout-chain bandwidth 0.28 GHz (derived from 280 MHz, packaged chip, setup-limited per the paper); 1.5 fF parasitic capacitance (author_estimate); 512 pixels; pitch 80 and 100 um (axes not stated); receiver chip 0.25 W |

Fab `org_globalfoundries` on all 5 rows ("fabricated using GlobalFoundries' CMS90WG 300 mm silicon photonics process",
p.10, multi-project wafer shuttle, broker not named; GF team thanked for assistance in device fabrication, p.7);
`process_name` "CMS90WG (GlobalFoundries 300 mm silicon photonics process, monolithic 90 nm SOI RF CMOS)". No facility.
Loss rows: 1550 nm `wavelength_inferred` (system seed laser at 1550 nm, no wavelength with the loss terms).

Values not entered and why:
- Silicon-photonic IQ MZM fabricated at the University of Southampton (p.10): modulator, EO-atlas candidate (rule 2);
  no value printed anyway.
- 32 x 16 microlens array (PowerPhotonic, off-chip) and its 24x signal improvement (p.5, p.10): off-chip optic, system
  value (D411 / D558). Field of view, beam sizes (11 x 16 mm mode at the 25 mm lens): set by bulk optics.
- 50/50 directional coupler (custom, non-PDK): no value, no row. Fiber V-groove coupling: no value.
- Electronics / system values without parameters: 20 kOhm gain, noise floor, shot-noise parity at 5 uW LO, CMRR 30-40 dB
  (cmrr rejected, D81), simulated 750 MHz amplifier chain, depth precision 3.1 mm at 75 m / 1.8 mm at 17 m, 1.0 mm/s,
  detection probabilities, 0.2 uJ/point, imaging contrast > 25 / > 50 dB, point rates.
- Proposed improvements from cited work (0.06 dB couplers [40], 0.23 dB phase shifters [41], 0.35 dB per switch,
  35 um phase shifters [42], 3 x 3 um2 grating couplers [48], 3 x 1 um2 couplers [49]) and the ~1 W transmitter of
  [30]: rule 3.
- Feasible 8 x 5 um2 pixel, QVGA / 4500 x 4800 resolutions: projections.

Judgment calls:
1. capacitance_ff 1.5 fF entered as author_estimate with the paper's "parasitic capacitance" wording; it may be the
   PD-TIA node rather than the junction. Alternative: notes only (the row keeps bw3db_ghz and power anyway).
2. The 0.28 GHz receiver bandwidth sits on the pixel (PD) row although it is the whole readout chain; condition says so.
3. The 0.25 W receiver-chip power sits on the pixel row (photodetector allows power_consumption_w); whether it includes
   the LO switch tree is not stated (noted).
4. Rise / fall: the paper prints "90% - 10% switching times" for both on and off transients; entered as rise_time_us
   (on) and fall_time_us (off) with the printed definition in condition.

## Missing fab / facility orgs

None. All needed ids exist (`org_globalfoundries`, `org_cornell_nanoscale_facility`,
`org_cornell_center_for_materials_research`). Printed orgs without a component role here: University of Southampton
(IQ modulator fab, no row), PowerPhotonic (microlens-array vendor, off-chip, no row).

## Registry gaps

- Free-space-emitter loss-budget terms (side-lobe / grating-lobe power fraction 6.4 dB, substrate emission 5.8 dB;
  doylend2011 p.10, calculated): no parameter; proposed `sidelobe_loss_db` / `substrate_loss_db` (free_space_emitter,
  dB, scope required). Low priority (simulated only here).
- Grating-emitter angular deviation vs duty cycle / width (doylend2011 Fig. 5, measured family): no parameter; not
  proposed (sibling-test sensitivity, not a device property).
- Resonance FWHM in phase units (hulme2013 0.022 / 0.020 rad): no parameter; not proposed (linewidth_pm covers
  wavelength widths).
- Registry metadata: lit:hulme2013 has no publication_date (text p.1: published 2013-08-14, issue 2013-08-26);
  lit:he2019a title prints "LiNbO 3" with a space (page-1 title "LiNbO3").
