# Batch lit_21 report (distill subagent, 2026-10-29)

Dry-run `batch lit_21: +53 components, +371 metrics; errors 0`. ASCII only, no e-mail addresses, no quotes beyond a few
words. verified_on 2026-10-29. Not audited or merged.

## Per paper (components / metrics)

- fang2021 (4 / 24): Sb2S3 phase-change tuning on rings. 20 nm Sb2S3 on fully etched Si rings R 20 um (non-volatile
  shift 0.53 nm for 10 um, Q ~5000), 66 nm Sb2S3 rings (0.947 nm), ITO-heater ring switch (SET shift 0.4 nm, contrast
  > 30 dB, 13 mW at SET, rib geometry), SiN ring R 10 um at ~750 nm (8 nm shift). Not entered: per-length shift
  0.060 nm/um and crystalline loss 0.16 dB/um (no parameter, see gaps), thermo-optic coefficients (material), RESET
  pulse (6 V, 200 ns), simulated values, GST reference (cited [11]). Garbled pages p.22-26 are references only.
  Fab org_university_washington (contributions p.21: Z.F. fabricated; all authors UW). Missing facility org (below).
- gebregiorgis2025 (2 / 9): undercut TiN SiN TOPS P_pi 2.7 mW at 650 nm TE; non-undercut sibling 73 mW (650 nm, Fig. 2(a)),
  72 / 51 mW at 637 / 520 nm; heater 200 x 1.5 um, gap 4-5 um. Fab org_aim_photonics ("fabricated ... through AIM
  Photonics", p.2). Not entered: undercut depth 142 um / 92 um pillar (no parameter), simulated thermal values.
- song2016 (5 / 24): floating-gate photonic memory cell (PMC) in a Si MRR R 10 um (resonator row: ON/OFF shift
  0.325 nm, full 0.38 nm, Q 1.3e4 / 9.6e3, notch 14.7 dB, 30-cycle std 2.2 pm, 8.6 dB fiber-to-fiber); PMC cell as
  phase_shifter.other (retention >= 20 h -> 72000 s derived, 30 cycles, C 110 fF measured / 133 fF theoretical); PMC MZI
  (ER ~20-25 dB); 500 nm rib waveguide 2.6 dB/cm (cutback); inverse taper ~3.4 dB/facet. Fab org_astar_ime ("fabricated
  in IME/A*STAR's 8-inch line", p.6). Not entered: program / erase energies 17.2 / 11.4 pJ (switching energy rejected
  D81), shift rates pm/ms, ~50 states (projection), FWHM 117 pm (assumption), 4-bit array (no values), supplement S1-S6
  (not cached). Wavelength of the loss values not stated (band unspecified + note).
- arabhavi2020 (3 / 14): top-illuminated Type-II UTC-PDs on InP (photodetector.vertical), uniform GaInAsSb / uniform
  GaAsSb / graded GaAsSb: external responsivity 0.094 / 0.070 / 0.062 A/W at 1550 nm (Table II), Cj and Rs from the
  S-parameter equivalent-circuit fit (80 um2), absorber 100 nm; GaInAsSb dark current < 10 nA to -5 V, f3dB > 60 GHz
  (<= 80 um2, setup limit). Not entered: transit-limited fT 274 / 107 / 185 GHz (gap), 240 GHz projection for 13 um2,
  Rj / Cp / pad elements, PL bandgaps. Fab empty: passive "were fabricated" (D80b); FIRST Lab staff thanks not a
  facility (D72).
- lischke2020 (3 / 17): Ge-300 waveguide Ge PD (f3dB >= 110 GHz at -2 V, 70 GHz at -0.25 V, >= 100 GHz up to ~1.2 mA,
  ~60 GHz at 3 mA, ext / int responsivity 0.27 / 0.64 A/W, dark ~300 nA, Ge width ~300 nm, length 20 um); Ge-350
  (~100 GHz, 0.32 / 0.74 A/W, 260 nA); 1D grating coupler 3.7 dB mean / 0.18 dB std (used for internal
  responsivity). Internal responsivities derived. Not entered: -1 dB bandwidth wafer map / > 55 GHz (gap), RC
  bandwidth > 400 GHz, C-V curves, Table 1 values of other works.
- li2026a (2 / 11): air-clad Ta2O5 ring R 300 um: Q_L 3.74e6 / Q_i 5.75e6 / 0.066 dB/cm at 1551.11 nm, Q_L 1.70e6 /
  Q_i 1.83e6 / 0.43 dB/cm at 780 nm (author_estimate: ng at 780 nm not stated), ng 2.17; tapered facet (8 um, 200 um)
  with aspheric-lens coupling 7.7 dB. The supercontinuum waveguides (6.5 mm; W 3.05 um, rib 587 nm, H 733 nm, wedge
  4.446 deg; flat-SC W 2.17 um, rib 623 nm) are geometry-only, not rows. Not entered: span 350-3200 nm at 54 pJ,
  -30 dB width 1182.33 nm, pulse compression 126.7 -> 19.2 fs (gap); cited earlier Ta2O5 values. Fab empty (passive,
  authors at several orgs).
- naraine2024 (20 / 205): Applied Nanotools SiN platform. Planar film (prism coupling, 5 wavelengths, mean of 4
  runs); strip 0.75 um and 1.0 um (cutback TE / TM, band bounds and "down to" minima, ring-derived losses, sidewall
  83.5 deg, simulated minimum bend radii); SWG waveguide (1.84 / 1.32 dB/cm); four best-tip edge couplers (Table III,
  measured / IMF / simulated); SWG edge coupler (1.26 / 1.18 dB/coupler); TE grating coupler (9.68 dB, > 23 nm 1-dB,
  simulated 6.2 dB / ~90 nm, period 1.18 um, duty 0.534 undefined); 1x2 MMI (EL 1.22 dB, IB 0.04 dB); 9 ring designs
  (Table IV, one row per width / gap; Q_i, Q_L, ER, FSR, ng per polarization). Fab org_applied_nanotools. Not entered:
  Table II simulated optimal tips, air-clad Table I designs, other MMI geometries (Fig. 6 only), anneal reductions,
  SWG duty cycles (gap), refractive index.
- neutens2025 (12 / 53): imec 200 mm Al2O3 platform. 250 nm film slab loss (406 / 443 / 638 nm); 110 nm waveguides
  450 / 500 / 600 nm (360 nm wafer means), 650 nm (450 nm), 1000 nm (532 nm), 1100 nm and 500 nm (266 nm die-level
  imaging), 1400 nm (< 0.16 dB/cm at 638 nm); 1x2 / 2x2 MMI excess loss 0.014 / 0.074 dB (cascade); grating coupler
  (10 % simulated) and 130 nm-tip edge coupler (2.6 dB simulated), both fabricated rows with simulated values (D80e).
  Fab org_imec. Not entered: coherence length > 2.2 mm (gap), 266 nm values for 600-800 nm widths (Fig. 6(b) only),
  single-mode cut-off widths (simulated), n / roughness. Polarization left empty for patterned waveguides (not stated).
- ou2021 (2 / 14): SiN strip-slot MMI mode converter W_MMI 3.5 um (0.1 dB best at 1580 nm, < 0.25 dB over 1500-1600 nm,
  simulated < 0.17 dB; full geometry) and W_MMI 3.6 um sibling (< 0.36 dB). Fab org_institute_of_microelectronics_
  chinese_academy_of_sciences ("designed, simulated, and fabricated", own process, D84a). Not entered: slot width
  180 / 172 nm (gap), Lst 10 / 15 um siblings (Fig. 8(b) only), Table 1 values of other works.

## Orgs missing from the registry

- Washington Nanofabrication Facility / Molecular Analysis Facility (University of Washington, NNCI site), fang2021
  p.21 acknowledgements ("Part of this work was conducted at"): facility_org_ids for all four fang2021 rows once added.
- Wafer / film suppliers (notes only, not needed): SOITEC (fang2021 p.19), Rogue Valley Microelectronics (fang2021
  p.20), WaferPro (naraine2024 p.3).

## Judgment calls for the coordinator

1. fang2021: all four ring devices, including the ITO-heater ring switch, are `resonator.ring` (jayatilleka2021 /
   cheung2023 precedent: ring-level non-volatile shift in tuning_range_nm); `phase_shifter.phase_change` would allow
   extinction_db / tuning_power_mw but not the shift. Q ~5000 (Fig. 3(c)) entered on the 20 nm series row although the
   fitted ring's length / state is not stated (D159 risk, noted).
2. song2016: one physical device split into the MRR (`resonator.ring`) and the PMC cell (`phase_shifter.other`) for
   retention / endurance / capacitance (jayatilleka2021 trimmer precedent).
3. lischke2020: fab IHP borderline (own prior process, IHP cleanroom-staff thanks, D84a / D84b). GC 3.7 dB entered as
   measured (wafer mean with sigma, origin not described).
4. naraine2024: ring rows per (width, gap) design (9 rows, D32); the paper's ring-extracted waveguide losses sit on the
   strip-waveguide rows (method ring_extraction, derived). Edge-coupler per-coupler values `measured`, method
   unspecified (extraction not detailed). Qi / QL from Lorentzian fits `measured`.
5. li2026a: Q_i "inferred" from Q_L -> derived (zhang2023a precedent); 780 nm loss author_estimate (ng not stated).
6. gebregiorgis2025 73 mW/pi (Fig. 2(a) annotation) and 72 mW at 637 nm both on the non-undercut row.

## Registry gaps (skipped values)

- Per-length phase-change element response (D250 rejected per-length phase-shifter loss / extinction; re-raised with
  new values): fang2021 resonance shift per Sb2S3 length 0.060 +/- 0.006 nm/um and crystalline loss 0.16 +/- 0.02
  dB/um (p.11, Fig. 3(d)-(e)). Proposed `shift_per_length_nm_per_um` / `loss_per_length_db_per_um` (phase_shifter;
  state and thickness in condition).
- `transit_bw_ghz` (photodetector): transit-time-limited bandwidth extracted by RC -> 0 extrapolation (method in notes).
  arabhavi2020 fT 274 / 107 / 185 GHz (p.4 Fig. 7, p.5 Table II).
- `bw1db_ghz` (photodetector): -1 dB OE bandwidth. lischke2020 > 55 GHz (p.4 Fig. 12), wafer map Fig. 13 (62 sites).
- Supercontinuum (frequency_converter subtype `supercontinuum`): `span_min_nm` / `span_max_nm` (level in condition),
  `bw_30db_nm`, `pulse_energy_pj`. li2026a 350-3200 nm at 54.0 pJ (p.6, Fig. 3(a)), -30 dB 1182.33 nm (979.51-2161.84
  nm, p.7, Fig. 3(c)).
- `gap_nm` for mode_converter (slot width of a slot waveguide / converter): ou2021 180 nm design (p.4), 172 nm SEM
  (p.6 Fig. 6(b)).
- `coherence_length_mm` (waveguide_platform): phase coherence length of a waveguide batch (Adar definition).
  neutens2025 > 2.2 mm at 360 nm, 450 x 110 nm (p.5).
- `swg_duty_cycle` (waveguide_platform, fiber_chip_coupler, crossing, splitter): segment fraction of an SWG
  (fill_factor is defined for diffraction gratings). naraine2024 0.5 (SWG waveguide) and 0.7 (SWG edge-coupler tip)
  (p.12 Sec. III-E).
- `undercut_depth_um` (phase_shifter, switch_fabric): substrate undercut / trench depth of a thermally isolated
  heater. gebregiorgis2025 142 um trench, 92 um residual pillar (p.2, Fig. 2(d)-(e)).
