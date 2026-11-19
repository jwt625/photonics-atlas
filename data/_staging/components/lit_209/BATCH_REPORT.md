# Batch lit_209 report

Distilled 2026-11-18 (verified_on 2026-11-18). Four papers. Dry run: `merge_component_staging.py data/_staging/components/lit_209 --dry-run` -> +12 components, +123 metrics, 0 errors (the one WARN concerns an already merged row of another paper, cmp_lit_ni2025b_pimmwc).

Totals: xu2017 3 / 39, shi2009 1 / 38, goh1999 5 / 27, wenger1997 3 / 19 (components / metric rows).

## lit:xu2017 (IEEE PTL 29(15), 2017, 4 pages)

Page-1 title matches. Text layer clean; Figs. 3-5 checked on the p.3 render (port mapping O1 1.49 / O2 1.55 / O3 1.31 um, shaded 3-dB bands match 70 / 30 / 20 nm).

| component | class | metrics |
|---|---|---|
| cmp_lit_xu2017_adc_triplexer | wdm.other | 37: measured 3-dB widths 70 / 30 / 20 nm, excess loss 0.98 / 0.69 / 0.76 dB (per_component, reference_structure: straight waveguide with the same gratings), crosstalk 27.07 / 23.03 / 25.84 dB; simulated 3D-FDTD widths 130 / 80 / 50 nm, excess loss 0.78 / 0.28 / 0.67 dB, crosstalk 23.81 / 20.84 / 25.63 dB, > 20 dB with 10 nm width deviation; geometry (six ADC widths, three gaps, three coupling lengths, 3 um radiation taper, ~150 um length, 220 nm Si, 2 um BOX, 0.3 um PMMA) |
| cmp_lit_xu2017_gc_1310 | fiber_chip_coupler.grating | 1: stated centre 1310 nm (author_estimate) |
| cmp_lit_xu2017_gc_1520 | fiber_chip_coupler.grating | 1: stated centre 1520 nm (author_estimate) |

Platform soi_strip (fully etched 220 nm). Fab empty: passive fabrication sentences only (p.3; D80b); both authors at Zhejiang University; no facility or acknowledgment of a facility.

Values not entered and why:
- Abstract "excess losses less than 1 dB for all three channels": summary of the per-channel rows.
- Grating bandwidths "~80 nm" / "~100 nm" (p.3): definition (1-dB / 3-dB) not stated; in component notes. No grating coupling efficiency printed.
- Fig. 1(b), (c) dispersion / delta n_eff values (> 0.02, -0.045, -0.05): design curves, no component parameter.
- Fig. 2 transmittance vs gap: design sweep.

Missing fab / facility orgs: none needed.

## lit:shi2009 (JLT 27(11), 2009, 5 pages)

Page-1 title matches. The text layer drops most symbols (H, h, w, d, L values): all values read from the p.1-4 renders.

| component | class | metrics |
|---|---|---|
| cmp_lit_shi2009_dc_triplexer_design | wdm.other, row_kind design | 38: Table II simulated (3D BPM) insertion loss per channel TE / TM (1310 nm port #2 0.35 / 0.1, 1490 nm port #3 0.51 / 0.08, 1550 nm port #1 0.29 / 0.16 dB, device_total), 12 crosstalk rows (each input wavelength into each unwanted port, TE and TM), 3-dB widths about 40 / 20 / 30 nm for ports #1 / #2 / #3, extinction ratio over the 3-dB band 11 / 10 / 12 dB TE and 12 / 10 / 13 dB TM; geometry (H 500 nm, slab 200 nm, w 500 / 550 nm, gaps 120 / 140 nm, coupling lengths 136.2 / 48.2 um, 50 um width taper, ~400 um total) |

Design-only paper (no fabrication); platform soi_rib; fab empty.

Values not entered and why:
- Text summary IL "around 0.5 dB TE / 0.1 dB TM" (p.3): Table II per-channel rows entered instead (summary in notes).
- Table I optimized lengths for other (w, d1) pairs and Fig. 3 coupling length vs gap: design exploration, not the chosen device.
- "10 nm fabrication error -> 1 um coupling-length deviation" (p.3), index difference 0.025 -> 0.3 um (p.2): sensitivity statements, no parameter.
- Etch depth (H - h = 300 nm): not printed, not computed.

Missing fab / facility orgs: none.

## lit:goh1999 (JLT 17(7), 1999, 8 pages; 1990s scan)

Page-1 title matches. Text layer readable; Table I, Table II, Fig. 6-8 values read on the p.3-5 renders.

| component | class | metrics |
|---|---|---|
| cmp_lit_goh1999_8x8_double_mzi_matrix | switch_fabric.mzi_mesh | 21: extinction 60.3 dB mean (n 64), range 49-76 dB, std 4.2 dB, example path 70.8 dB, worst >= 47.6 dB over 1530-1560 nm; IL (fiber_to_fiber) 5.1 dB mean, 4.7-5.9 dB, std 0.3 dB, example 5.3 dB, worst <= 6.4 dB over 1530-1560 nm; PDL 0.3 dB mean; MXR 43.3-48.4 dB / mean 46.0 dB (author_estimate, Eq. (1) with assumed uniform inputs); xt_bandwidth > 130 nm / 100 nm (average ER > 50 dB); total power 16.0 W; 8 x 8 ports; footprint 68 x 68 mm (derived); core 7 x 7 um (derived) |
| cmp_lit_goh1999_double_mzi_unit | switch_fabric.mzi_mesh | 2: mean ON 1.06 W, OFF 0.134 W per unit |
| cmp_lit_goh1999_cr_heater_mzi | phase_shifter.thermo_optic | 2: P_pi 456 / 426 mW derived (ON minus OFF heater power of the first / second MZI, Fig. 6 example) |
| cmp_lit_goh1999_dc_3db | splitter.directional_coupler | 1: coupling ratio 33 % at 1.55 um (author_estimate, stated set value) |
| cmp_lit_goh1999_intersection | crossing.other | 1: intersection crosstalk about 63.6 dB (measured on test waveguides, test_structure) |

Platform ge_silica. Fab org_ntt on all 5 rows: p.3 "We fabricated this silica-based 8 x 8 thermooptic matrix switch", all authors at NTT laboratories (NTT Photonics Laboratories, NTT Network Innovation Laboratories; D154 parent, D72); PLC-fabrication staff thanks (p.6) agree. No facility.

Values not entered and why:
- Conventional single-MZI crossbar columns of Tables I-II and the commercial switch (~30 dB / ~7 dB, p.1): earlier or other work (rule 3).
- Switching time "around 2 ms" (p.1): generic statement about the authors' earlier thermo-optic switches (ref. [10]), not measured here.
- Minimum bend radius 5 mm, intersection angle about 30 deg, total waveguide length 290 mm, unit length 23 mm: no switch_fabric / crossing parameter (`min_bend_radius_um` on switch_fabric is an open gap, D596); in notes.
- Loss penalty 1.1 dB from k = 33 % (p.4): model estimate, in notes.
- Thermal crosstalk (Fig. 9): 0.04 dB ON-state and up to 4 dB OFF-state transmittance variation; no parameter. Light-obstructor improvements 2.5 / 0.4 dB; average loss degradation 0.1 dB with different-wavelength optimization: in notes.
- 2 % TE / TM coupling-ratio difference: no parameter (coupling_variation is over wavelength); in notes.
- MXR requirement (-26 dB) and 17 dB margin: system statements.

Missing fab / facility orgs: none (org_ntt exists).

## lit:wenger1997 (IEEE JSTQE 3(6), 1997, 12 pages, invited; 1990s scan)

Page-1 title matches. Page renders exist only for p.3-10 (pp. 1-2 and 11-12 are text-only); those pages have no tables or figures with values. Tables II-III and Figs. 4, 9, 14-16 read on the renders.

| component | class | metrics |
|---|---|---|
| cmp_lit_wenger1997_8x8_matrix | switch_fabric.other | 8: IL 20.2 dB mean (n 64, fiber_to_fiber incl. interfaces, splices, connectors, shuffle), std 1.6 dB, range 17.1-25.2 dB; crosstalk suppression 28 dB mean, 13-37 dB worst / best; PDL about 3 dB; 8 x 8 ports |
| cmp_lit_wenger1997_most | fiber_chip_coupler.edge | 7 (simulated / geometry): > 90 % butt coupling into the fiber-matched rib, 1-dB tolerance 2.1 um, overall loss slightly above 1 dB per facet; rib width 12 um and step 5 um (Fig. 4(c) labels, derived), vertical / lateral taper 1000 / 500 um |
| cmp_lit_wenger1997_selfaligned_fiber_array | fiber_interface.v_groove | 4: array-coupling excess 0.5 dB typical (measured vs two optimally aligned fibers), fiber-chip interface 0.5 dB per interface (Table III, author_estimate, loss budget), 250 um pitch, 16 signal fibers |

Platform inp on the matrix and MOST rows; the fiber-array row has no stated guiding platform (empty, D422). Fab empty everywhere (see missing orgs).

Values not entered and why:
- Sec. III-B (1x8 switch results: TE / TM IL 6.8 / 6.3 dB, +/-0.3 dB homogeneity, +/-0.7 dB polarization, crosstalk 24 / 25 dB, > 19 dB, Table II loss analysis 1x2 switch 1.6 dB, tapered waveguide 1.0 dB, waveguide 1.5 dB/cm, bends 0.3 dB, MOST 1-dB tolerances +/-2 / +/-3 um, Fig. 9, device size 10.4 x 2.0 mm, 250 um output pitch): the subsection opens "we give performance results for the 1x8 switches and their subcomponents [17]", the authors' JLT 1996 paper; removed under D259a. No 1x8 switch, 1x2 switch, waveguide or bend rows result.
- Table III 1x8 switch term 8.7 dB: the same [17] value. Fusion splice 0.1 dB, fiber connector 0.2 dB, shuffle 0.0 dB: purchased fiber parts in a loss budget, in notes.
- Crosstalk levels -38 to -54 dB (std 3.0 dB): absolute levels, not suppression; in notes.
- 3-dB excess-loss window 1.45-1.60 um (Fig. 16): no wavelength-window parameter on switch_fabric (registry gap below).
- Switching time about 100 ns: limited by the driver transistors, not the device.
- Conclusion: improved 1x2 switches 0.6-1.0 dB lower loss (delta only), predicted 0.5 dB 1x2 switch and 10 dB 64 x 64 matrix, ~100-fiber array limit: projections / estimates for other devices.
- Temperature stability of the packaged 1x8 module (within 1 dB to 100 C, Fig. 14): no parameter; in notes.
- MOST simulated section terms (0.3 / 0.6 / 0.1 / 0.1 dB) and Fig. 8 loss vs taper length: terms in notes, the sum is the row.
- Fiber spot size 5 um (p.1): generic fiber statement.

Missing fab / facility orgs:
- Siemens (fab; parent of the printed units "Siemens HL", "Siemens ZT", "Siemens ON" [O-umlaut], p.1 author footnote). First-person chip-process sentences (p.7 Sec. III-C "we use projection lithography", "we use CH4-H2 reactive ion etching", "we have developed a technique ... ion beam shadow etching"), packaging (p.7-8 Sec. IV) and assembly (p.9 Sec. V "we use multiple splicing equipment"); all authors at Siemens units -> fab Siemens on all 3 rows by D72 / D154 once the org exists.

## Judgment calls

- (a) wenger1997: Sec. III-B is attributed as a whole to ref. [17] (the authors' earlier 1x8 switch paper) by its opening sentence, so all 1x8 switch, sub-component and MOST measured values there are left out (D259a); Sec. VI (8x8 results) cites nothing and is kept although ref. [19] reports the same matrix (D408). The coordinator may read the [17] sentence more narrowly.
- (b) wenger1997: the Table III fiber-chip interface 0.5 dB and the Sec. IV array-coupling penalty 0.5 dB are put on a `fiber_interface.v_groove` row (the self-aligned array attach), not on the MOST row: the MOST taper loss sits inside the 1x8 switch term of the budget. Interface term `author_estimate` (loss-budget term of unstated origin), scope per_facet; the penalty `measured` typical, scope unspecified (module excess over two optimally aligned fibers, both array interfaces).
- (c) wenger1997 MOST "alignment tolerances of 2.1 um" (simulated, direction not split) entered in `tol_1db_lateral_um` as the +/- half-width with the wording in notes; figure-labelled MOST dimensions stored in nm / um as `derived` (D157).
- (d) goh1999: the 8x8 matrix is `switch_fabric.mzi_mesh` (NxN MZI fabric, D158) and the double-MZI unit a separate `mzi_mesh` cell row (characterized inside the matrix). Heater P_pi entered as ON minus OFF heater power of each MZI (bar to cross), `derived`.
- (e) goh1999: "average extinction ratio > 50 dB over > 130 nm (100 nm with normal optimization)" entered as `xt_bandwidth_nm` with the extinction-ratio level in the condition (the paper ties OFF-state ER to switch crosstalk). Worst-case values over 1530-1560 nm stored as bounds (ER `ge` 47.6 dB, IL `le` 6.4 dB). MXR rows `author_estimate` (Eq. (1) with an assumed uniform input power).
- (f) goh1999: IL scope fiber_to_fiber (PM fiber and SMF butted to the chip; no de-embedding printed). The 64-path range kept as the text prints it (49-76 dB) with Table II's 49.4 dB worst value in notes.
- (g) xu2017: the two grating-coupler sets entered as rows with only their stated centre wavelengths (`author_estimate`); their bandwidths are in notes because the definition is not printed. The coordinator may drop these rows as thin.
- (h) shi2009: Table II per-channel IL and crosstalk entered (24 rows) instead of the rounded text summary; the printed 3-dB widths per port (40 / 20 / 30 nm) kept as printed with a Fig. 5 conflict note (D417): Fig. 5 shows wider TE passbands for ports #1 and #2.

## Registry gaps

- `bw_3db_nm` (or a criterion wavelength window) on switch_fabric: wenger1997 3-dB excess-loss margins 1.45 and 1.60 um (p.10, Fig. 16); proposed definition "full wavelength width over which the switched-path insertion loss stays within 3 dB of its minimum".
- `min_bend_radius_um` on switch_fabric (open since D596): goh1999 5 mm (p.3).
- Crossing angle parameter (`crossing_angle_deg`): goh1999 intersection about 30 deg (p.3); "angle between the crossing waveguides".
- Loss / transmittance variation under neighbouring-unit heating (thermal crosstalk) on switch_fabric: goh1999 0.04 dB ON / up to 4 dB OFF (p.6, Fig. 9).
- Insertion-loss stability vs temperature on fiber_interface: wenger1997 within 1 dB up to 100 C (p.9, Fig. 14) (D71 rejected "il temperature change" earlier; listed for the record).
