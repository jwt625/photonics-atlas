# lit_249 batch report

Papers: lit:xiao2019, lit:zou2014, lit:cheng2019, lit:yao2012 (all Optics Express; page-1 titles match the source
rows). verified_on 2026-11-22. Dry run: +15 components, +128 metrics, 0 errors. No existing rows for these sources.

## Components / metric rows

| paper | component | class | row_kind | metrics |
|---|---|---|---|---|
| cheng2019 | cmp_lit_cheng2019_swg_te0_te1 | mode_converter.converter | design | 11 (97.9 % at 1550, 0.09 dB, < 0.25 dB / > 94.4 % and crosstalk > 15.33 dB over 1500-1600 nm; geometry) |
| cheng2019 | cmp_lit_cheng2019_swg_te0_te2 | mode_converter.converter | design | 11 (98.6 %, 0.06 dB, < 0.19 dB / > 95.7 %, > 17.36 dB; geometry) |
| cheng2019 | cmp_lit_cheng2019_swg_te0_te3 | mode_converter.converter | design | 13 (89.8 %, < 0.77 dB / > 83.7 %, crosstalk > 15.65 dB (TE0) / > 11.48 dB (TE1); geometry incl. two widths and 1 um taper) |
| xiao2019 | cmp_lit_xiao2019_g01_sim | mode_converter.converter | design | 10 (3-dB 29.5 nm, reflection crosstalk > 23.5 dB, TE2 pass-through loss < 0.2 dB, transmission crosstalk > 20 dB; period 300.1 nm, 200 periods, 60 um, cross-section) |
| xiao2019 | cmp_lit_xiao2019_g02_sim | mode_converter.converter | design | 10 (24.5 nm, > 21 dB, TE1 loss < 0.3 dB, > 50 dB; 326.6 nm, 200, 65.3 um, cross-section) |
| xiao2019 | cmp_lit_xiao2019_g12_sim | mode_converter.converter | design | 10 (23 nm, > 24 dB, ~18 dB, > 38 dB; 343.8 nm, 200, 68.8 um, cross-section) |
| xiao2019 | cmp_lit_xiao2019_g01_g12_te2_te0 | mode_converter.converter | design | 6 (peak 0.2 dB, 3-dB 20.2 nm, crosstalk > 19.7 dB; cross-section) |
| xiao2019 | cmp_lit_xiao2019_g12_g02_te0_te1 | mode_converter.converter | design | 6 (0.2 dB, 23.5 nm, > 22.5 dB; cross-section) |
| xiao2019 | cmp_lit_xiao2019_g02_g01_te1_te2 | mode_converter.converter | design | 6 (0.2 dB, 23.0 nm, > 23.2 dB; cross-section) |
| xiao2019 | cmp_lit_xiao2019_pmma_g01_g02_te2_te1 | mode_converter.converter | fabricated | 9 (measured T21 passband 3-dB 8.3 nm near 1525 nm, T11 notch ~6.9 nm, T00 notch ~9.0 nm; periods 290 / 316 nm, 2 x 350 um, 1200 nm width, 220 nm core / full etch) |
| zou2014 | cmp_lit_zou2014_lcbg | reflector.bragg | design | 8 (reflection bandwidth 20 nm; chirp 285.5-290.5 nm, FF 0.5, 5760 um, mask / space widths, rib / slab) |
| zou2014 | cmp_lit_zou2014_alcbg | reflector.bragg | design | 5 (reflection bandwidth 17.4 nm = 20 - 2.6; period, length, rib / slab) |
| zou2014 | cmp_lit_zou2014_comb_lcbg | wdm.other | design | 6 (channel spacing 3.29 / 1.63 / 0.81 nm and 5 / 11 / 23 passbands at three index changes) |
| zou2014 | cmp_lit_zou2014_comb_alcbg_pip | wdm.other | design | 5 (spacing 0.19-8.21 nm, 1-65 passbands, 21 passbands at 3.2e-3, rejection > 30 dB, heater power 54-2470 mW) |
| yao2012 | cmp_lit_yao2012_stack_cavity | resonator.photonic_crystal | fabricated | 12 (Q ~27,000 and FWHM ~58 pm measured, Q 1.74e7 FDTD, thermal drift ~-25 pm/K; a 400 nm, NG 20, Wy(0) / Wy(20) / Wx, 2 um I/O waveguide, 220 nm / 2 um BOX) |

Per paper: cheng2019 3 / 35, xiao2019 7 / 57, zou2014 4 / 24, yao2012 1 / 12.

## Values not entered and why

cheng2019 (simulation-only; no fabrication, no acknowledgment of a facility)
- Duty cycles 0.3 / 0.45 / 0.3 (defined as etched-strip width / period, i.e. gap fraction): `fill_factor` not allowed
  for mode_converter (gap open since D533); strip heights h0 / delta-h and intervals L2 / L3 have no parameter (notes).
- Fabrication tolerance (Fig. 13, +/- 20 nm width / height / thickness): no printed numbers; the "accuracy in 10 nm"
  sentence is a recommendation.
- Fig. 3 / Fig. 7 sweep maps: figure only.

xiao2019
- Side-lobe levels (G01 < -17.0, G02 < -16.5, G12 < -16.0, cascades < -20.0 / -29.8 / -36.5 dB): `slsr_db` not
  allowed for mode_converter (component notes).
- MTMM parametric bandwidths of G01 (2.1 / 4.0 / 7.2 nm "between nearest nulls" for kappa / L pairs, p.6, Fig. 6):
  null-to-null width, no parameter; parametric study, no design row.
- Fabricated gratings: coupling coefficients 180 / 160 cm-1 (p.11, calculated; Fig. 18(c) 180.2 / 160.1 cm-1) and
  Fig. 18 simulated tolerance (full bandwidths 7.02 / 6.34 / 6.12 nm at zero alignment error, conversion-wavelength
  shifts -7.1..6.4 to -22..20 nm vs width, +/- 22 nm vs height): `kappa_per_cm`, null-to-null bandwidth and
  wavelength shift not allowed for mode_converter.
- G12 TE0 notch about -0.4 dB near 1565 nm (TE0-TM0 coupling, Fig. 8(f)): parasitic feature, no clean parameter.
- Fabricated device conversion loss: Fig. 15(b) T21 passband sits around -6 to -8 dB "normalized power"; the
  normalization reference is not stated and the path includes ADCs and grating couplers: not entered.
- T21 with vs without gratings "crosstalks up to -7.0 dB" (p.13, Fig. 16(a)): attributed to ADC imperfection, not a
  converter value. Ripple period 0.610 nm measured (0.625 nm calculated): no parameter (component notes).
- ADC01 SEM widths 860 / 392 nm and gap 191 nm (Fig. 12(c)): geometry only, no ADC performance value -> no row.
  Photonic-crystal grating couplers: no values -> no row.
- pi-phase-shifted G02 + G12 design (Fig. 17, MTMM): no printed numbers.

zou2014 (theory / simulation; no fabricated device)
- Propagation loss 1.5 dB/cm: assumed, cited (ref. [25]; rule 3).
- Group-delay ripple ~15 ps peak to peak (unapodized), group-delay differences 2.5 / 5 / 10 ps: no parameter (notes).
- Apodization a = 5, delta-n_eff0 = 0.008: notes only.
- p-i-p heater: resistance ~600 kOhm*um (unit per length, parameters "same as our previous paper [32]"), simulated
  index change 0.013 and excess loss < 0.3 dB/cm at 2.47 W: no clean parameter on any class; no phase_shifter row.
- Free-carrier tuning example (index change 1.1e-3, ~21 dB/cm, rejection down to 5 dB): alternative actuator the
  paper rejects; not entered (note on the comb row).
- Fig. 6(b) rejection-ratio curve (about 62 dB at the lowest power): figure only; only the printed > 30 dB bound is
  entered.

yao2012
- Sensitivity 269 nm/RIU (measured, linear fit) and 273 nm/RIU (FDTD): no registry parameter.
- Effective mode volume 1.48 (lambda/n_Si)^3, ~35 % field fraction in the void: no parameter.
- Fig. 2 parameter sweeps (Q and sensitivity vs Wx, Wy(0), NG, background index): figure only.
- Grating couplers (70 nm shallow etch): no values -> no row.

## Missing fab / facility orgs

None. yao2012 fab = org_zhejiang_university (exists). zou2014 "IME Singapore" (p.10 acknowledgment, "for device
fabrication") would map to org_astar_ime, but no device is fabricated in the paper (see judgment call c).

## Judgment calls for the auditor

a) xiao2019 single gratings G01 / G02 / G12 entered as separate `mode_converter.converter` design rows
   (contra-directional mode-converting Bragg gratings with their own simulated spectra), not `reflector.bragg`:
   the class keeps crosstalk and pass-through loss; it loses side-lobe and kappa values (registry gap below).
   Alternative: reflector.bragg rows (kappa / slsr allowed, crosstalk not).
b) xiao2019 fabricated row fab empty: "When we fabricated the cladded PMMA surface grating" (p.11) is first person,
   but authors span Nanjing University (7) and University of Miami (1; one author at both). D154 / D433 applied;
   alternative org_nanjing_university. Waveguide fabrication sentence is passive.
c) zou2014: all four rows `design` with fab empty although IME Singapore is acknowledged "for device fabrication":
   the paper reports no fabricated device or measurement (likely a later paper's device). The acknowledgment is in
   the component notes.
d) zou2014 grating reflection bandwidth ("reflection bandwidth", level not defined) entered as `stopband_width_nm`
   with "level not defined" (giuntoni2009 precedent, D82g); the apodized 17.4 nm is 20 - 2.6 nm (printed narrowing),
   kept `simulated` (D83f). Band `c_band` inferred from the plot axes on the spectral rows.
e) zou2014 comb filter class `wdm.other` (jiang2016 tunable comb-filter precedent); out-of-band rejection ratio as
   `extinction_db`; passband counts as `n_channels` (basis simulated). Tuning power 2.47 W stored as 2470 mW in
   value_max, kept simulated.
f) cheng2019: transmissivity in dB entered as `insertion_loss_db` per_component and the printed efficiency in % as
   `coupling_efficiency_pct`; both forms of the same 1500-1600 nm bounds are printed, so both are entered (flag if
   one is to be dropped). "Up to 97.9 % / 98.6 %" -> qualifier `le` (rule 7). The 0.09 / 0.06 dB design-point rows
   carry 1550 nm `wavelength_inferred` (the wavelength sits in the next sentence). The TE0-TE2 section prints "TE1"
   / "TE0-to-TE1" twice; entered on the TE0-TE2 row per the section and figures (noted).
g) cheng2019 / xiao2019 SWG and grating period in `period_nm` (subwavelength_period_nm not allowed for
   mode_converter); cheng2019 0.2 um printed -> 200 nm `derived`.
h) xiao2019 cascaded peak transmission -0.2 dB entered as insertion_loss_db `best` at 1550 nm inferred (peak position
   not printed). Reflection crosstalk sentences print "from the TE0 and TE2" for G02 / G12, where TE2 is the
   converted mode; kept as printed in the condition. G12 "transmission modal crosstalk from the TE1 about -18.0 dB and
   that to the TE2 lower than -38.0 dB" entered as two rows as printed (incident mode not named).
i) xiao2019 fabricated row: the three measured 3-dB widths (T21 passband, T11 and T00 notches) on one component row
   with the notch identity in the condition (one physical device, rule 9); T00 notch wavelength 1525 nm inferred.
   Core thickness 220 nm from Sec. 5.2 ("consistent with the experimental structures").
j) yao2012: one fabricated row; the FDTD Q 1.74e7 of the design (Wx 0.3a = 120 nm, Wy(0) 2.5a = 1000 nm) is kept on
   it (D80e) although the fabrication section prints 126 / 1017 / 2012 nm. Measured Q 27,000 `approx` + `best`
   (abstract "as high as"); wavelengths 1583.5 nm read off Fig. 4(a) (`wavelength_inferred`); FDTD Q band `l_band`
   inferred from the measured resonances. Thermal drift -0.025 nm/C -> -25 pm/K `derived`, sign as printed; analyte
   during the temperature run not stated (Fig. 4(d) resonance near 1559.5 nm, different from the 5 % mixture). Block
   size Wx entered as a third `width_nm` row with "along the propagation axis" in the condition; I/O waveguide 2 um
   as `bus_width_nm`.

## Registry gaps (skipped value + locator + proposed definition)

- `slsr_db` on mode_converter: xiao2019 side lobes < -17.0 / -16.5 / -16.0 dB (p.7-8), cascades < -20.0 / -29.8 /
  -36.5 dB (p.9-10). Definition as for wdm / reflector (sidelobe suppression of the conversion / reflection spectrum).
- `kappa_per_cm` on mode_converter: xiao2019 180 / 160 cm-1 (p.11; p.15 Fig. 18(c)). Grating coupling coefficient
  between the two coupled modes.
- `fill_factor` on mode_converter (open since D533): cheng2019 duty cycles 0.3 / 0.45 / 0.3 (gap fraction; tooth
  fraction 0.7 / 0.55 / 0.7), p.3-5.
- `center_wavelength_nm` on mode_converter (D419 candidate): xiao2019 fabricated passband near 1525 nm (p.13); design
  conversion wavelength 1550.0 nm (p.7).
- Refractive-index sensitivity `sensitivity_nm_per_riu` (resonator): yao2012 269 nm/RIU measured, 273 nm/RIU FDTD
  (p.5). Resonance shift per refractive-index unit of the cladding / analyte.
- Effective mode volume `mode_volume_cubic_lambda_over_n` (resonator): yao2012 1.48 (lambda/n_Si)^3 (p.3).
- Null-to-null grating bandwidth (`bw_null_nm`): xiao2019 2.1 / 4.0 / 7.2 nm (p.6), 7.02 / 6.34 / 6.12 nm (p.15).
