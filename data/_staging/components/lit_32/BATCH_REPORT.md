# Batch lit_32 report (distill subagent, 2026-10-29)

Dry-run `batch lit_32: +26 components, +246 metrics; errors 0`. ASCII, no e-mail, no addresses. Quotes only on the
open-licence source (hulyal2025); all other notes paraphrased. Page-1 title / authors checked for all 10 texts: all match
their source rows (ryf2002 = OFC 2001 PD28, as the DOI says).

## Per paper (components / metrics)

- akiyama2022 (3 / 19): 32-ch 50 GHz cascaded-AMZ-triplet DWDM demux with EIC calibration (wdm.cascaded_mzi; total
  crosstalk 38.5 dB worst port, 1-ch crosstalk 44.5 dB from the Fig. 8 label, mean loss 9.8 dB scope unspecified, triplet
  estimate 1.02 dB, design periods and arm-length increments per depth), single AMZ (0.4 dB derived), 2x2 MMI (0.2 dB).
  O-band inferred from the 1305-1315 nm plot axes (no wavelength in the text). Not entered: EIC power 1270 mW / 13.7 mW
  per CE (power_consumption_w not allowed for wdm), 440 ohm heaters (phase_shifter-only parameter), 43.8 dB peak-to-crosstalk
  contrast (extremum ambiguous), ~2 dB projection, Fig. 13 model. Fab empty (PIC process named without an org; EIC TSMC
  180 nm is electronics).
- bogaerts2007a (2 / 26): bidirectional polarization-diversity AWG duplexer (wdm.awg; IL 2.1-6.9 dB de_embedded,
  intra-band non-uniformity 4.8 dB, inter-band crosstalk 15 dB best, PDL 0.66 dB, 48 arms, 275 GHz / 3.85 THz design,
  delay-line widths 800 / 900 / 500 nm, 70 nm shallow etch) and 2-D grating coupler (6.7 dB / 21 % loopback_half derived,
  60 nm 3-dB, 605 nm period). Fab org_imec: authors state they fabricated + P-line processing thanks (D84b borderline,
  bogaerts2006 precedent). Not entered: hole diameter 390 nm, 3.1 deg waveguide angle, Fig. 4 / 5 labels (roles unclear),
  Fig. 8 11.5 nm label.
- brouckaert2007 (1 / 21): 1x4 SOI PCG / echelle demux (wdm.eg; 7.5 dB de_embedded central channels, crosstalk > 30 dB,
  0.6 dB non-uniformity, simulated 0.7 / 0.9 dB, FSR 115 nm simulated, order 10, 31 facets, d 4.35 um, slab ng 3.7,
  280 x 150 um, 5 um port pitch, 2 um ports, sidewall 79.5 deg from 10.5 deg non-verticality). Fab empty: single joint
  Ghent University / IMEC affiliation, no acknowledgment (mangal2018 precedent). Not entered: loss breakdown 4.6 / 0.3 /
  4.9 / 0.7 / 1.9 dB (CAMFR / inferred), Rowland radius 94 um (no parameter), 2.9 dB projection.
- hulyal2025 (4 / 60): Confocal and Rowland 8x100 GHz LTOI AWGs (ltoi_rib; single-device and three-field wafer means for
  IL, 3-dB width, adjacent crosstalk, channel spacing, sd in notes; Table S1 geometry: m 160, N 13, dL, R_a 75 um, w_a,
  w_o, d_o), loss-extraction ring (kappa0/2pi 32.7 MHz mean; 5.95 dB/m author_estimate, ng not stated, D76), double-layer
  edge taper (3.7 dB fiber_to_fiber author_estimate, measured or designed unclear; 0.16 um tips, 160 / 100 um tapers).
  Wavelengths inferred from the Fig. 3 frequency axes (L-band Confocal, S-band Rowland). Fab org_epfl (author
  contributions), facility org_center_of_micronanotechnology. Not entered: MUX/DEMUX AWG pair (5 channels, no number),
  arrayed aperture spacing d_a, 250 um height-transition statement (inconsistent with 160 + 100 um).
- mikkelsen2018 (3 / 21): polarization-insensitive 4-ch CWDM SiN MZI lattice demux (best device IL 0.9-2.8 dB
  de_embedded, crosstalk > 11.5 dB, PDL < 0.9 / < 1.3 dB, wafer means over 9 dies, center-wavelength sd 0.9-1.0 nm,
  simulated > 21 dB, ng 1.904, 2.5 x 0.9 mm, SEM thickness ~630 nm), SiN 600 nm square waveguide (< 0.9 dB/cm at 1310,
  < 1.9 dB/cm 1270-1370), inverse-taper edge coupler (~4.5 dB, per-coupler vs pair not stated -> unspecified). Fab
  org_cea_leti (fabrication stated at CEA-LETI, p.4). Not entered: passband ripple, TE/TM passband shift (no parameters), fitted
  model 1.85 / 13.2 dB.
- sattari2020 (1 / 17): MEMS suspended-ring add-drop filter in iSiPP50G (wdm.mrr; FSR ~5 nm, Q ~25000, port extinction
  20 dB passive / > 20 dB at 27 V, port isolation ~50 / 57 dB, drop extra loss ~7 dB, FDTD IL <= 0.4 dB, geometry).
  Fab org_imec + org_epfl (release post-processing at CMi, D83c), facility CMi. The conclusion's > 50 dB active-state extinction
  conflicts with the results (> 20 dB): results entered, conflict noted. Not entered: 0.5 nm resonance shift at 27 V,
  actuation voltage (no wdm parameter).
- sun2026a (4 / 32): DC-FPR FSR-free Bragg add-drop unit (wdm.bragg_cdc; IL < 0.5 dB one value for O/S/C devices,
  3-dB 15-118 GHz design family, ER ~25 dB Table 1, 16.7 nm tuning, 70 pm/mW derived, simulated ER / crosstalk / SLSR),
  20-ch 400 GHz DEMUX (< 2.5 dB, > 25 dB, ~36 GHz), 9-ch O-to-C triplexer (< 2 dB, > 20 dB), 9-ch processor as WSS
  (switch_fabric.wss, > 20 dB on/off OSNR contrast). Fab org_westlake_university + org_zhejiang_university (contributions
  name fabricators at both, D80b); Crealights staff assisted only (D395, not fab); facilities Westlake Center for Micro/Nano
  Fabrication and ZJU Micro-Nano Fabrication Center. Not entered: FSR-free bandwidth > 300 nm (no parameter), spectral
  coverage 61.3 / 64 / > 150 nm, 6-dB width ~60 GHz, 16-ch accelerator (no performance parameter: 32 weight levels,
  1.5 nm source grid), Fig. 4 dB labels (D156), supplement (not cached).
- suzuki2021 (4 / 17): assembled PLC-AWG + 8x8 Si switch (switch_fabric.other; fiber-to-fiber IL 12.6 mean / 11.6-14.4,
  PDL 0.57 / 0.01-1.88, leakage > 40 dB, homo-wavelength crosstalk > 20 dB), 5.5 %-Delta PLC AWG (< 2 dB, > 20 dB, PDL
  < 0.2 dB), PLC-fiber-array facet (~0.3 dB/facet), Si SSC to PLC (chip_chip_coupler.butt, 3.8 dB expected for two
  facets, 160 nm tip). Fab empty (authors at AIST and Furukawa). Not entered: Si on-chip 6.2 dB, PDL < 0.4 dB, DGD,
  -30 dB crosstalk (cited from ref. [10], D259), loss breakdown, AWG polarization-dependent wavelength shift 0.3 nm.
- ryf2002 (1 / 7): 1296-port 3D MEMS optical crossconnect (switch_fabric.mems; 5.1 dB mean fiber_to_fiber, adjacent-port
  crosstalk 58 dB with a garbled bound glyph -> no qualifier, worst-case > 38 dB, 5 ms rise / fall derived). Fab empty.
  Not entered: 1 dB / 1 h stability, 200 V max electrode voltage, 2.07 Pb/s extrapolation.
- yang2020 (3 / 26): 24 x [1x12] LCoS WSS module with LCoS device A and with device B (two rows; Table I typical and
  min-max IL, intra-WSS isolation, inter-WSS > 45 dB, 3-dB passband; Table II budget 5.82 / 7.04 dB author_estimate),
  fs-laser-written 312-port glass waveguide array (fiber_interface.fan_out; 1.69 dB mean, 3.04 dB calculated pair,
  80 / 680 um pitches). Fab empty. Not entered: IL ripple +/-0.5 dB, glass 0.2 dB/cm, position / pointing error,
  ellipticity, M2, 64 % LCoS reflectivity, LCoS pixel data.

## Fab / facility organizations missing from the registry

- Service Center for Physical Sciences at Westlake University (sun2026a p.17 Acknowledgements; facility statement).
- Crealights Technology Co., Ltd. (sun2026a p.1 affiliation 4, p.17; not needed: assistance only, D395).
- ROADMap Systems Ltd. (yang2020 p.1; not needed: no fabrication statement).

## Judgment calls for the audit

- akiyama2022 O-band inferred from plot axes only; sattari2020 printed 70 nm ridge height entered as etch_depth_nm.
- bogaerts2007a fab org_imec (D84b) vs brouckaert2007 fab empty (same group, no acknowledgment).
- sun2026a DC-FPR family classed wdm.bragg_cdc; processor as switch_fabric.wss (configured as hitless WSS).
- suzuki2021 hybrid device classed switch_fabric.other; Si 8x8 switch chip has no own-measured value (no row).
- yang2020 LCoS devices A / B as two component rows (different SLM, switch count).

## Registry gaps (value actually skipped)

| proposal | skipped value | locator |
|---|---|---|
| power_consumption_w allowed for wdm (electrical power of the filter control / tuning) | 1270 mW EIC, 13.7 mW per CE | akiyama2022 p.3-4 Sec. IV |
| passband_ripple_db (wdm, switch_fabric): max-min transmission within the stated passband | < 0.8 dB / 0.8 +/- 0.1 dB; +/-0.5 dB | mikkelsen2018 p.5-6; yang2020 p.5 Table I |
| pd_wavelength_shift_nm (wdm): passband / channel shift between orthogonal polarizations | < 1.5 / < 1.6 nm; ~0.3 nm | mikkelsen2018 p.5; suzuki2021 p.2 |
| fsr_free_bandwidth_nm (wdm, resonator): span with a single resonance (no other order) | > 300 nm | sun2026a p.6, Table 1 |
| hole_diameter_nm (fiber_chip_coupler): hole diameter of a 2-D / photonic-crystal grating | 390 nm | bogaerts2007a p.5, p.8 |
| actuation_voltage_v allowed for wdm (voltage for the stated tuning / switching state) | 27 V | sattari2020 p.3 |
