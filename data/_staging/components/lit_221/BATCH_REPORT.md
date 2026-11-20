# Batch lit_221 report

Distilled 2026-11-20 (verified_on 2026-11-20). Four papers (Optics Express, Optica OA route). Dry run: `merge_component_staging.py data/_staging/components/lit_221 --dry-run` -> +16 components, +123 metrics, 0 errors (the one WARN is on an already merged row of another paper, cmp_lit_ni2025b_pimmwc).

All four cached texts match their source rows (page-1 titles); no garbled text layer, no correction / erratum. Figure values read from PyMuPDF renders of the cached PDFs at 6-7x zoom (all four papers' plots are raster images).

## lit:nelan2022b (Opt. Express 30(6), 2022, 15 pages)

Components / metric rows: 5 / 30

| component | class | metrics |
|---|---|---|
| cmp_lit_nelan2022b_wg_crossing | crossing.other (fabricated, simulated values) | 6: crossing loss < 0.01 dB (FDTD, 1530-1565 nm), cross-port crosstalk >= 111.5 dB (peak -111.5 dB at 1565 nm), SiN width 2 um, TFLN 300 nm, SiO2 2 um over the crossing, BOX 4.7 um |
| cmp_lit_nelan2022b_mmi_1x2 | splitter.mmi (fabricated, simulated values) | 10: excess loss about 0.21 dB (Fig. 2(c) read 0.952), MMI 15 x 148 um, taper 52.5 um, port width 7 um, output separation 8 um, access width 2 um, TFLN 300 nm, 1 x 2 ports |
| cmp_lit_nelan2022b_sin_loaded_wg | waveguide_platform.straight (test structure) | 6: 0.66 dB/cm at 1550 nm (OFDR), simulated group index 2.21, SiN 2 um x 100 nm on 300 nm TFLN, BOX 4.7 um |
| cmp_lit_nelan2022b_bend_r500 | waveguide_platform.bend (simulated) | 5: < 0.01 dB / 90 deg and < 0.01 dB/cm at 500 um radius, cross-section |
| cmp_lit_nelan2022b_polished_facet | fiber_chip_coupler.edge | 3: about 8.75 dB per facet (author_estimate, equal-facet split of 21.0 - 3.43 dB), simulated overlap about 21 % and 6.84 dB per facet |

Values not entered and why:
- Modulator metrics (rule 2; the paper is not in the EO atlas, EO-atlas candidate by DOI 10.1364/oe.453050): DC Vpi about 4.0 V (10 mm folded MZM with crossing, Fig. 8(a) 4.02 V), VpiL about 4 V cm, reference 5 mm folded MZM without crossing Vpi about 8.17 V (Fig. 8(b)), static ER about 23 dB (Fig. 8(c)), EO 3-dB bandwidth 37.5 GHz with UV15 index-matching fluid, sideband roll-off about 0.3 dB/GHz (to 40 GHz, no fluid) and about 0.08 dB/GHz (to 110 GHz, with UV15), total fiber-to-fiber IL about 21.0 dB, on-chip loss about 3.43 dB over the 52 mm path, RF index 1.94, impedance about 50 ohm, S21 about -6.3 dB at 40 GHz.
- On-chip 3.43 dB: equals 0.66 dB/cm x 5.2 cm; modulator-level, not entered separately.
- Mode confinement 69.5 % in LN, SiN index 1.943, simulated metal absorption vs electrode gap / buffer (Figs. 3(c), 4(d)): no component parameter.
- Misalignment share about 1.95 dB per facet: the authors' attribution; in component notes.
- Crossing: measured evidence is qualitative only (OFDR trace "negligible", ER / Vpi argument), no number.

Printed conflict (D417 note on the row): crossing through loss printed "< 0.01 dB" (p.5) while the Fig. 3(a) curve reads about 0.039-0.044 dB over 1530-1560 nm (axis ends at 1.56 um, text says 1.565 um). Printed value kept.

Missing fab / facility orgs: none needed. Fab empty (passive fabrication narrative with no org; authors at University of Delaware and Phase Sensitive Innovations, D80b). Supplier note only: "NanoLN" (TFLN substrate, p.7 Sec. 3).

Judgment calls:
1. One MMI row for the 1x2 splitter and the 2x1 combiner (the paper presents one MMI design used both ways, p.4-5).
2. S_MMI 8 um entered as `pitch_um` (output-port separation per Fig. 2(d)); auditor may prefer notes only.
3. Facet row as `fiber_chip_coupler.edge` (polished facet, no SSC; D469 angled-facet precedent); 8.75 dB `author_estimate` (equal-facet assumption, D462 / D514).
4. OFDR loss on the "on-chip reference structure" (Fig. 8(d) caption) marked `test_structure` true.

## lit:ma2019 (Opt. Express 27(13), 2019, 11 pages)

Components / metric rows: 2 / 35

| component | class | metrics |
|---|---|---|
| cmp_lit_ma2019_swg_psr_air_ebl | polarization.psr | 17: measured IL < 1.4 dB (1530-1620 nm, GC-calibrated), Table 1 ER > 19 dB (TE00) / > 15 dB (TM00) as per_db, simulated IL < 0.5 dB (TM00 cross) / < 0.4 dB (TE00 through), length 171 um, sections L1-L4, Si 220 nm, six role-labelled widths |
| cmp_lit_ma2019_swg_psr_sio2_ime | polarization.psr | 18: measured IL < 1.3 dB (1500-1620 nm, edge-coupler-calibrated), Table 1 ER > 14 dB (TE00) / > 15 dB (TM00), simulated IL < 0.5 / < 0.3 dB, length 185 um, LA / LB / L4, Si 220 nm, slab 90 nm, seven role-labelled widths |

Fab: air-clad row `org_applied_nanotools` ("fabricated by Applied Nanotools Inc.", p.4); SiO2-clad row `org_astar_ime` ("fabricated ... using 193 nm optical lithography at the Institute of Microelectronics (IME), Singapore", p.6), process_name as printed (shokraneh2020 precedent). CMC Microsystems is thanked for design / simulation software only: not fab, not facility. No facility statement.

Values not entered and why:
- Crosstalk relative to input power (D424, waits for `crosstalk_db` on polarization): simulated air-clad TE00 at the through port < -18 dB (1500-1620 nm), TM00 < -19 dB (1546-1620 nm, about -15 dB below 1530 nm), TE00 at the cross port < -25 dB (p.4); measured air-clad cross-port crosstalk < -20 dB (1500-1620 nm, p.5). In component notes.
- SWG period (200 / 300 nm), fill factor (0.6 / 0.5), coupler gap (100 / 180 nm): `period_nm`, `fill_factor`, `gap_nm` not allowed for polarization (registry gap).
- Simulated 99.8 % TM00-to-TE01 conversion of the bi-level taper at 1550 nm (p.6, Fig. 7(a)): polarization / mode conversion efficiency % not in the registry (D420 candidate).
- Polarization receiver (Sec. 3.3, Figs. 10-11): which PSR it uses is not stated; Fig. 11(a) labels "1.5 dB" / "30.3 dB" have no stated meaning (D156); eye amplitudes 58 / 124.9 mV are system-level. No row.
- Prior-report note: the air-clad PSR was "reported earlier" in the authors' GFP 2018 paper (ref. [20], p.2); no value sentence, figure or caption cites it, so values kept (D408).
- Measurement errors +/-0.5 dB (TE00) / +/-1.0 dB (TM00) in notes; Table 1 row "PSR in [12]" is cited work (rule 3).

Missing fab / facility orgs: none (both fab orgs in the registry).

Judgment calls:
1. Table 1 "Extinction ratio" entered as `per_db` (definition not printed; read as the wanted / unwanted output-port ratio, consistent with IL < 1.4 dB and cross-port crosstalk < -20 dB). If the auditor reads it as leakage relative to input, the four rows move to notes (D424).
2. Measured IL rows: polarization `unspecified` (one IL bound per PSR, input mode not named), scope `de_embedded`, method `reference_structure` (GC / edge-coupler calibration pairs).
3. Simulated IL spans 1500-1620 nm flagged `wavelength_inferred` where the IL clause prints no range (Fig. 3 / Fig. 8 axes).

## lit:tan2016 (Opt. Express 24(13), 2016, 7 pages)

Components / metric rows: 1 / 10

| component | class | metrics |
|---|---|---|
| cmp_lit_tan2016_bend_psr_design | polarization.psr (row_kind design) | 10: simulated CE -0.11 dB (TM to TE cross) / -0.09 dB (TE through) at 1310 nm as insertion_loss_db, ER 27.36 / 30.61 dB as per_db, 3-dB bandwidth >= 100 nm (whole O-band), Si 220 nm, widths W1 400 / W2 210 / W3 285 nm, slab H2 110 nm |

Design-only paper (Lumerical MODE + 3D FDTD); no fabrication. No fab / facility.

Values not entered and why:
- Crosstalk CT (simulated, 1310 nm): cross port -17.92 dB (TM input) / -38.79 dB (TE input), through port -18.97 dB (TM) / -19.77 dB (TE) (p.6): ratios of the unwanted-mode power to the wanted-mode power; `crosstalk_db` not allowed for polarization and `per_db` already holds the paper's ER. In notes; registry gap.
- Bend radius 10 um, gap 0.2 um, 5 um output taper: no polarization parameter (registry gap).
- Fabrication-tolerance curves (Fig. 6, +/-10 nm): tolerance parameters rejected (D81 / D250).

Judgment calls:
1. `bw_3db_nm` 100 nm `ge`: the paper prints only "covers the whole O-band"; the bound is the simulated 1260-1360 nm span (Fig. 5 axis). Auditor may prefer notes only.
2. W2 0.21 um / W3 0.285 um stored in nm as `derived` (D157).

## lit:ding2012 (Opt. Express 20(18), 2012, 7 pages)

Components / metric rows: 8 / 48

| component | class | metrics |
|---|---|---|
| cmp_lit_ding2012_tdc_psr_w310_l140 | polarization.psr | 6: T_c TE0-TM0 about 0.58 dB at 1540 nm (Fig. 6(b)), w1 310 nm, wide-waveguide taper 406-606 nm, L 140 um, Si 250 nm, BOX 3 um |
| cmp_lit_ding2012_tdc_psr_w318_l140 | polarization.psr | 6: about 0.81 dB (w1 318 nm read off the Fig. 6(b) axis) |
| cmp_lit_ding2012_tdc_psr_w323_l140 | polarization.psr | 6: about 0.12 dB (w1 323 nm from the axis) |
| cmp_lit_ding2012_tdc_psr_w324_l140 | polarization.psr | 6: about 0.50 dB |
| cmp_lit_ding2012_tdc_psr_w326_l140 | polarization.psr | 6: about 1.81 dB |
| cmp_lit_ding2012_tdc_psr_w329_l140 | polarization.psr | 6: about 1.97 dB (w1 329 nm from the axis; p.6 range ends at 329 nm) |
| cmp_lit_ding2012_tdc_psr_w324_l120 | polarization.psr | 6: about 0.5 dB at 1540 nm (Fig. 6(c), +/-0.7 dB ripple) |
| cmp_lit_ding2012_tdc_psr_w324_l100 | polarization.psr | 6: about 0.5 dB at 1540 nm (Fig. 6(c), +/-0.7 dB ripple) |

All performance values are `extracted_from_figure` (Fig. 6(b) markers +/-0.03 dB); scope / method `unspecified` (calibration only cited to the authors' ref. [12]; liu2011 precedent). Fab empty: passive "was fabricated", no org named (D80b; authors at DTU Fotonik and South China Normal University); no facility.

Values not entered and why:
- Text bound "T_c above -1 dB for w1 310-324 nm" (14 nm tolerance, "more than 14 nm" in the conclusion): stated once for the sample family; not put on one representative row (D254), in component notes; each row carries its own figure read.
- Gap 100 nm (gap_nm not allowed for polarization).
- Simulations (Figs. 3-4: designed taper 450-650 nm, g 100 / 150 nm, L sweeps; normal-DC comparison from the authors' ref. [13]): qualitative or cited; no design row.
- 1-dB / 3-dB bandwidths: not printed; traces too noisy for a reading.

Printed / figure tension (D417 note on the w326 row): Fig. 6(b) gives about -1.8 dB for w1 = 326 nm at 1540 nm while the Fig. 6(a) 326 nm trace peaks near 0 dB around 1540 nm within its about 2 dB ripple.

Judgment calls:
1. Row granularity: one component row per fabricated w1 / L sample (rule 9, D32; cheng2023 wm60 / wp60 and pita2023 length-series precedents) instead of one family row (D165 is for regressed families). The auditor may prefer a single family row with the bound.
2. w1 318 / 323 / 329 nm are read from the Fig. 6(b) x-axis marker positions (`extracted_from_figure`, +/-0.3 nm); 310 / 324 / 326 nm are printed (legend / caption / text). Whether w1 and the 406 / 606 nm taper widths are drawn or SEM-measured is not stated (`design_target`).
3. L = 100 / 120 um rows kept with a coarse Fig. 6(c) read (about 0.5 dB, +/-0.7 dB) as their only performance metric; text says only "similar conversion coefficients". Delete if the auditor judges the read too coarse.

## Missing fab / facility orgs

None. All fab orgs used (`org_applied_nanotools`, `org_astar_ime`) are in the registry.

## Registry gaps (with skipped values)

| gap | skipped value + locator | proposed definition |
|---|---|---|
| `crosstalk_db` on polarization (D424 / D439 candidate) | tan2016 CT -17.92 / -38.79 / -18.97 / -19.77 dB (p.6); ma2019 simulated -18 / -19 / -25 dB (p.4) and measured -20 dB (p.5) | crosstalk suppression magnitude of a polarization device, positive dB; reference (unwanted-mode / wanted-mode ratio, or leakage relative to input) in condition |
| `gap_nm` on polarization (D439 candidate) | ding2012 100 nm (p.6); tan2016 0.2 um (p.3); ma2019 100 / 180 nm (p.2, p.5) | coupling gap of a PSR / PBS coupler |
| `period_nm` / `fill_factor` (or `subwavelength_period_nm`) on polarization | ma2019 SWG 200 nm / 0.6 (p.2-3) and 300 nm / 0.5 (p.5) | SWG period and tooth fraction of an SWG-assisted polarization device |
| `radius_um` or `min_bend_radius_um` on polarization | tan2016 10 um (p.2-3) | bend radius of a bent-coupler PSR |
| `taper_length_um` on polarization | tan2016 5 um (p.4) | output / input taper length |
| polarization conversion efficiency % (D420 candidate) | ma2019 99.8 % TM00-TE01 (simulated, p.6) | mode / polarization conversion efficiency, linear % |
