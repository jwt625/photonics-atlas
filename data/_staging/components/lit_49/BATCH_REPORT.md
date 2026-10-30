# Batch lit_49 report (distill subagent, 2026-10-29)

Dry-run `batch lit_49: +20 components, +141 metrics; errors 0` (one WARN from another batch, ni2025b m18 / m4). ASCII, no
e-mail. Rights: he2023 open_license_ok; the other four restricted_local_only (facts and locators, at most a few words quoted).
Page-1 title / authors match the source rows for all five papers; no garbled text layers; no supplement cached (ji2017 refers
to Supplement 1, not available). Generator: scratchpad `lit_49/gen.py`.

## Per paper (components / metrics)

- ding2013 (2 / 14): tapered-DC TE0/TE1 MDM circuit (MUX + 750 nm bus + DEMUX, mode_converter.mdm_mux, soi) as an
  array-level row (D165) over the three measured variants (w1 360 / 380 nm, L 30 / 50 um): lowest IL 0.3 dB `de_embedded`
  (normalized to a straight waveguide, MUX + DEMUX path), crosstalk > 16 dB over 1480-1580 nm, > 20 dB at 1553.06 nm in the
  system test, SEM narrow width 355 nm, variant widths / lengths, 250 nm / 3 um SOI. Design row (row_kind design): EME crosstalk
  > 22 dB (1450-1650 nm), TE0-TM0 > 30 dB, > 25 dB over ~40 nm width deviation; w1 390 nm, L 50 um. Not entered: gap 100 nm and
  wide-taper widths 748-848 nm (no mode_converter parameter), > 20 nm fabrication tolerance (no parameter), power penalties
  1.6 / 1.8 dB (link), per-variant curves (Fig. 5 overlapping, not read), SU8 coupler (no performance).
- he2023 (2 / 22): ALD-alumina rings R 400 um, 4.5 um wide, 100 nm shallow etch, air-clad (resonator.ring, al2o3), one row per
  chip (390 nm, 500 C anneal; 488.5 nm, 600 C anneal): Q_L 1.2 M / 1.4 M measured, ER 2.4 / 3.2 dB, Q_int 1.5 M / 1.9 M
  author_estimate (under-coupled formula, D403), FSR TE00 / TE10 65.6 / 66.3 and 68.5 / 68.6 GHz, loss 0.84 / 0.51 dB/cm
  author_estimate, film 420 nm measured (reflectometry), etch 100 nm and radius design. Not entered: bus width / gap (stated as
  the optimal coupling condition while rings with smaller gaps were also measured; the reported ring's gap not stated, D159),
  radiation-loss and radiation-limited-Q simulations (loss terms), Fig. 3 comparison (other works).
- ji2017 (6 / 44): four R 115 um, 730 x 2500 nm Si3N4 rings, one per process (standard, new etch, + CMP, + multipass EBL):
  Q_int 5.6 / 16.2 / 28 / 37 M, FWHM 47 / 12.8 / 7.6 / 5.6 MHz, loss 5.2 / 1.8 / 1.1 / 0.8 dB/m (stored dB/cm); the process-4 row
  also holds the Sec. 5 same-wafer 2.5 um ring (TE 6.2 / TM 6.8 MHz, 0.79 dB/m). 10 um wide ring R 369 um: Q_int TE 67 M, TM 59 M,
  ring-down 63 M, FWHM 3.3 / 5.8 MHz, 0.43 dB/m. Kerr OPO row (frequency_converter.other, D396 cross-note): threshold 330 uW
  (mean, derived to mW), theory 206 uW (author_estimate), Q_L 35 M at ~1557 nm. All Q_int and loss rows author_estimate (regime
  stated as under-coupled, not determined from data, D403). Facilities: ASRC NanoFabrication Facility (CUNY) + Cornell NanoScale
  Facility ("partially fabricated at"). Not entered: bulk-absorption 0.13 dB/m and Q_abs >= 170 M, sidewall / top / bottom
  scattering terms (model-based decomposition with simulated eta factors and Payne-Lacey estimates), AFM roughness and correlation
  lengths, ring-down lifetime 25.6 ns (no parameter), Fig. 4(b) threshold vs Q_L (devices not identified), Supplement comparisons.
- ye2019 (6 / 33): normal-dispersion 600 x 1850 nm ring (array-level, D165: FSR ~105.2 GHz, mean Q_int 11.4 M, ~3 dB/m,
  most probable intrinsic linewidth 15-18 MHz over 6 rings, representative critical resonance FWHM 23.4 / intrinsic 11.7 MHz /
  Qi ~16 M, sidewall ~85 deg); anomalous 740 x 2000 nm ring (FSR 100 GHz, mean Q_int 12.5 M, ~15 MHz typical, 19.8 / 11.7 MHz
  representative); 0.9 THz ring R 25 um, 740 x 1500 nm, 800 nm bus, 700 nm gap (Q_L ~1 M at 1540 nm). Three laser.comb rows
  (ye2023 precedent): dark-pulse comb 210 GHz, 23 % pump-to-comb; soliton ~0.9 THz; heater-initiated soliton 100 GHz, 0.8 %. Fab
  org_chalmers_university_of_technology ("we" fabricated, all authors Chalmers MC2). Not entered: beta2 / D2 / D3 and avoided
  mode crossings (D250), comb spans 1300-2200 / 1470-1700 nm (no parameter), surface / line-edge roughness, FIB gap ~400 nm (ring
  not identified), radius of the 105 / 100 GHz rings (not stated).
- simard2013 (4 / 28): spiral SOI IBGs (reflector.bragg): uncompensated, phase-compensated (SLSR ~10 dB measured), one of three
  interleaved spirals, Gaussian phase-apodized; peak reflectivity read off the OFDR spectra (-12.5 / -10.5 / -11 / -17 dB ->
  5.6 / 8.9 / 7.9 / 2.0 %, derived, approx, Bragg wavelength ~1557.8 nm inferred from the lambda_B axis); geometry 1200 nm x
  220 nm, period 858.24 nm (3rd order), duty 0.25, 2 mm length, footprints 38000 / 49450 um2 (derived). Fab org_astar_ime
  ("fabricated using the OpSIS service through IME A*STAR"). Not entered: SLSR comparison with a straight grating (ref. [16]),
  ~1.15 pi distributed phase shift (simulation analogy, no parameter), Delta-n ~0.07e-3 (no parameter; kappa not computed),
  apodization FWHM 1 mm / 17.5 um modulation period (no parameter), > 20 dB SLSR improvement (calculated curve).

## Missing orgs (name as printed + locator)

- "OpSIS service" (simard2013 p.11 Acknowledgments): MPW access service through IME A*STAR; not in the registry (D398 would make
  it a fab org next to org_astar_ime). Coordinator: add an OpSIS org (MPW service, as printed) or keep IME only.
- No other missing orgs. Entegris (he2023 co-author company, ALD coating, p.2) is a film supplier: note only. CMC Microsystems
  (simard2013) appears only as a funder.

## Judgment calls

- ding2013: headline IL / crosstalk stated once for three variants -> one array-level circuit row (D165) rather than one
  representative variant (D254); IL scoped `de_embedded` (normalized to a straight waveguide) and wavelength given as the measured
  span 1480-1580 nm with "wavelength of the minimum not stated" in condition. Variant widths 360 / 380 nm entered as design_target
  (SEM of one device shows 355 nm).
- he2023: p.4 text calls the 488.5 nm 1.9 M value "loaded Q"; Fig. 2(b) inset and the conclusion make it intrinsic: entered as
  q_intrinsic with the note.
- ji2017: process variants are separate rows (different fabrication); the Sec. 5 2.5 um ring sits on the process-4 row ("the
  optimized fabrication process", same design; 0.79 vs 0.8 dB/m). Wavelengths of the Q measurements are not stated: band c_band
  inferred from the only stated operating wavelength (OPO pump near 1557 nm). Ring-down Q_int 63 M author_estimate (conversion from
  lifetime not detailed). fab empty (authors over Cornell / Columbia / Georgia Tech).
- ye2019: fitted Q_int / intrinsic linewidths `measured` (fit of own data, ye2023 precedent) with a note that the coupling-regime
  assignment is not stated; the authors' ~3 dB/m equivalent loss `derived`; sidewall ~85 deg `measured` (method not stated).
- simard2013: reflectivity from figure readings converted dB -> % (derived, +/- 0.5 dB reading uncertainty); TE assumed from the
  single-TE access waveguides (noted); fill_factor 0.25 kept as printed because the paper calls the corrugation both "added on the
  side" and a "recess" (D253).

## Registry gaps (proposed definitions)

- gap_nm for mode_converter (again; lit_38 yang2014): ding2013 tapered-DC gap 100 nm design and SEM (p.3, p.4). Definition as for
  splitter.
- Secondary-waveguide width for asymmetric / tapered DC mode converters (e.g. `wide_width_nm` start / end): ding2013 750-850 nm
  design, 748-848 nm SEM (p.3, p.4).
- Comb span (`comb_span_nm`, laser.comb: full spectral extent as stated, criterion in condition): ye2019 1300-2200 nm and
  1470-1700 nm (p.6-7).
- Surface roughness (`rms_roughness_nm`, waveguide_platform / resonator, surface and method in condition): ji2017 0.38 -> 0.08 nm
  (p.2), ye2019 0.18 nm top, ~1 nm line edge (p.3).
- Photon lifetime (`photon_lifetime_ns`, resonator, ring-down): ji2017 25.6 +/- 1.3 ns (p.4).
- Index-modulation amplitude / apodization profile width for Bragg gratings: simard2013 Delta-n ~0.07e-3 (figures), 1 mm FWHM
  Gaussian (p.11) -- low priority, figure-only values.
