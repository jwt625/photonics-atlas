# lit_208 batch report

Distilled 2026-11-18 (verified_on). Papers: lit:kim2017, lit:noe2016, lit:chen2010a, lit:celo2017, lit:chen2012. All five cached texts
match their source rows (page-1 title). Validation: `merge_component_staging.py data/_staging/components/lit_208 --dry-run` ->
+9 components, +85 metrics, 0 errors.

| paper | components | metric rows | row_kind |
|---|---|---|---|
| kim2017 | 1 | 14 | design |
| noe2016 | 1 | 1 | fabricated (purchased) |
| chen2010a | 4 | 46 | design |
| celo2017 | 2 | 13 | fabricated |
| chen2012 | 1 | 11 | design |
| total | 9 | 85 | |

## kim2017 (IEEE Photonics J. 2017, Si slot-waveguide intersection, simulation only)

- 1 component `crossing.mmi`, platform `soi_slot` (Si pattern embedded in SiO2; badri2019 slot-crossing precedent), row_kind design.
- 14 metrics: 3D FDTD throughput -0.078 dB and crosstalk -41 dB at 1550 nm; 1500-1600 nm bounds (loss < 0.18 dB, crosstalk > 40 dB);
  1520-1570 nm loss range 0.078-0.15 dB; width-tolerance bounds (delta-w -30 to +10 nm: loss < 0.1 dB, crosstalk > 39 dB; 1550 nm
  inferred as the design wavelength); footprint 79.2 um2 (printed); geometry (250 nm Si, 260 nm rails, 100 nm slot as `gap_nm`,
  wM 1.7 um, lM 2.9 um, lT 3.0 um), all design_target.
- Not entered: reflectance -30 dB at 1550 nm (Table 3, p.9) and < -29 dB over 1500-1600 nm (p.9): registry gap (below). Table 1
  (lT / lS sweep at wM 1.7 um) and Table 2 (wM 1.4-1.9 um peak linear throughputs 0.956-0.987) optimization points (judgment (a)).
  Blunt-corner deltas (p.9-10, Fig. 6(c)). Comparison values of refs. [19]-[21] (rule 3).
- Conflict noted: Table 2 throughput 0.984 for the chosen design (= -0.070 dB) vs the printed -0.078 dB headline; headline kept.
- Fab / facility: none (design).

## noe2016 (NOC 2016, LiNbO3 endless polarization control, review of the authors' own work)

- 1 component `polarization.compensator`: the commercial EOSPACE Ti:LiNbO3 polarization transformer (8 Soleil-Babinet
  compensators, X-cut Z-propagation), platform `other` (Ti-indiffused LiNbO3; D515 precedent for LiNbO3 outside the LNOI enums).
- 1 metric: insertion loss "~3 dB" (p.6 Sec. IV), `author_estimate` (origin not stated: own measurement or datasheet), scope
  `unspecified`, band `unspecified` (no wavelength with the value; experiments in the C band).
- Not entered: every tracking result (100 / 140 krad/s, > 350 Grad, -40 dB average extinction at 1 krad/s, wavelength and temperature
  independence, 0.08 dB Q penalty at 40 krad/s, 3-DOF polarization errors) is attributed to the authors' refs. [6], [7], [11]-[15]
  (rule 3, D259); tracking speed in rad/s also has no registry parameter. Fig. 1 "7 um" label not tied to a dimension (D156).
  Novoptel EPS1000 scrambler, lasers and receivers are setup equipment (rule 13).
- Missing fab org: EOSPACE, vendor of the purchased device under test (printed "a commercial polarization transformer (EOSPACE)",
  p.1 Sec. II.A); fab role (rule 12). fab_org_ids left empty until the org exists.

## chen2010a (IEEE JQE 2010, taper-integrated MMI crossing, simulation only)

- 4 components `crossing.mmi` (radical, linear, quadratic, Gaussian taper designs of Table I), platform `soi` (Si on SiO2 on Si
  substrate, Fig. 1; chen2006 precedent), row_kind design.
- 46 metrics: per design Table I insertion loss and crosstalk at 1550 nm, 1500-1600 nm insertion-loss fluctuation (`wdl_db` < 0.3 dB;
  Gaussian "roughly 0.24 dB") and worst crosstalk (> 38 dB), taper length, MMI length, MMI width 1.2 um (nm printed -> derived),
  Wg 500 nm, H 220 nm, footprint (derived from the printed crossing dimension). Gaussian design adds 6 tolerance bounds (Sec. II.E,
  Fig. 7: lengths / widths / both within +/-10 %; 1550 nm inferred as lambda0).
- Not entered: Fig. 2 bare MMI crossing vs power ratio (idealized two-mode input, minimum ~0.175 dB; notes); MMI-lens taper coupling
  losses 0.081 / 0.061 / 0.046 / 0.034 dB, phase differences and effective beat lengths (sub-part values, in each row's notes); abstract
  summary bounds (< 0.3 dB, < -40 dB) restate Table I.
- Fab / facility: none (design).

## celo2017 (GFP 2017, OPC on MMI crossings, Huawei Canada)

- 2 components `crossing.mmi`, platform `soi` (220 nm fully etched Si, 2 um BOX, SiO2 cladding), fabricated, test_structure true:
  wgx (no serifs) and wgxs (OPC serifs).
- 13 metrics: wgx mean C-band loss 0.043 dB (193 nm) / 0.049 dB (248 nm); wgxs mean 0.026 dB (both lithographies), 0.019 dB at the
  1545 nm optimum, 0.029 dB at 1550 nm over 6 dies; maximum C-band crosstalk 39 / 42 dB (193 nm, qualifier ge); 220 nm core,
  2 um BOX, 500 nm access width. Loss values printed in mdB -> dB, basis `derived` (D256).
- Not entered: simulated 32 mdB "for a perfectly fabricated crossing" (p.2 Sec. IV; not tied to wgx or wgxs, D159; notes);
  abstract "< 30 mdB" (summary of the same data); wavelength dependence "around +/-5 mdB" over the C band (+/- half-span; no clean
  `wdl_db` form without converting); printed energy-loss percentages (inconsistent with the dB values); early-generation crossing
  of ref. [7] (Fig. 2, SEM corner radius 400 nm; cited work); minimum gap 150 nm inside the opening (no matching parameter; notes).
- Fab: empty. Printed "a multi-project wafer of a silicon photonics research foundry" names no foundry (D433, dumais2017 precedent);
  `process_name` kept as the printed flow ("MPW runs, 200 mm SOI, 193 nm and 248 nm non-immersion lithography", D536). No facility.

## chen2012 (WOCC 2012, cascaded multimode-taper crossing, simulation only)

- 1 component `crossing.mmi` (judgment (d)), platform `soi`, row_kind design.
- 11 metrics: 0.187 dB / 47.58 dB at 1550 nm; 1500-1600 nm fluctuation < 0.20 dB (`wdl_db`) and crosstalk > 35 dB; footprint (derived
  from 3920 x 3920 nm); Wg 500 nm, H 220 nm; uniform multimode section w1 1.1 um / Lt2 0.86 um as `mmi_width_um` / `mmi_length_um`;
  taper lengths Lt1 0.45 um and Lt3 0.05 um (conditions name the taper).
- Not entered: loss minimum "roughly at 1560 nm" (no value); intersection width w2 1200 nm (notes; no second width parameter
  without ambiguity).
- Conflicts noted: "crossing width of 1300 nm" (p.2) vs w2 = 1200 nm; Fig. 2 / Fig. 3 captions swapped against the text.
- Fab / facility: none (design).

## Judgment calls

- (a) kim2017: only the selected wM 1.7 um design is a row; the Table 1 / Table 2 sweep points are optimization intermediates kept in
  notes (unlike chen2010a, whose four taper designs are the paper's compared results in Table I).
- (b) celo2017: one row per layout (wgx, wgxs) with the lithography (193 / 248 nm) as a metric condition, not four rows; the 6-die
  29 +/- 8 mdB and 19 mdB optimum values are assigned to wgxs (they follow the OPC sentences; the abstract gives the OPC loss as
  < 30 mdB); lithography for them not stated.
- (c) celo2017: crosstalk "maximum values ... -42 dB and -39 dB" stored as 42 / 39 dB with qualifier `ge` (worst case over the band).
- (d) chen2012 classed `crossing.mmi` (uniform multimode section between Gaussian tapers; the paper presents it as the extension of
  its taper-integrated MMI crossing); `crossing.other` is the alternative.
- (e) noe2016: the only own, uncited number is the "~3 dB" loss in the conclusion; kept as author_estimate with scope / band
  unspecified rather than inferring the C band.
- (f) Tolerance bounds (kim2017 delta-w, chen2010a zeta1-3) entered as metric rows with the perturbation in `condition` and
  1550 nm inferred (design wavelength).

## Registry gaps

- `back_reflection_db` for `crossing` (already reported for badri2019 / D567): kim2017 reflectance -30 dB at 1550 nm (p.9 Table 3)
  and < -29 dB over 1500-1600 nm (p.9, Fig. 6(a)). Proposed: allow `back_reflection_db` (positive dB below the input) on crossing.
- Polarization-tracking speed (rad/s) for `polarization.compensator`: no own value in noe2016 (all cited), recorded only as context.

## Missing orgs

- EOSPACE (fab, vendor of the purchased LiNbO3 polarization transformer), lit:noe2016 p.1 Sec. II.A.
