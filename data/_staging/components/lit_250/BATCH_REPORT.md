# Batch lit_250 report

Papers: lit:ai2024, lit:guo2023a, lit:chen2015c, lit:xiao2013 (D712 batch D family). verified_on 2026-11-22.
Total 25 components / 152 metric rows; `merge_component_staging.py --dry-run`: 0 errors, no warnings on these rows.
Page-1 titles match the source rows for all four papers; no correction / erratum; no garbled text layer.

## lit:ai2024 (Broadband 2x2 SWG MMI on Si3N4) - 3 components / 24 metrics

- `swg_mmi_2x2_paired` (splitter.mmi, sin, fabricated): IL (sum of both outputs, stored as `excess_loss_db`) and power
  imbalance < 1 dB over 1375-1675 nm and < 0.5 dB over a > 50 nm span near 1450 nm (p.11, Fig. 12, Table 1); 1-dB
  bandwidth 300 nm (both criteria); geometry 12 x 90 um, 2.5 um ports, 1 um access waveguide, SWG period 400 nm,
  21.2 um taper (simulation optimum), 300 nm Si3N4, 5 um BOX / cladding, 2 x 2 ports.
- `swg_mmi_2x2_nonpaired` (splitter.mmi): IL < 1.5 dB over 1450-1640 nm (p.11 Fig. 11); 12 x 280 um, 5.5 um ports.
- `sin_inverse_taper_edge` (fiber_chip_coupler.edge): about 3 dB/facet (p.8), tip 0.3 um.
- Not entered: simulated spectra of SWG and conventional MMIs (Fig. 6, curves only, no printed values); simulated
  102 um MMI length / 204 um beat length (design steps, fabricated length 90 um entered); port separation 4.1 um
  (W'MMI/3, not a channel pitch); duty cycle 50 % (fill_factor not registered for splitter); chirped-SWG variant and
  oscillation amplitude about 5 dB (artifact of routing-waveguide coupling, not a device metric); TM filter (no value);
  Bragg drop near 1260 nm (Fig. 13, no parameter); Table 1 rows of other works (rule 3).
- Fab / facility: fab `org_university_of_maryland_college_park` (first-person "we first fabricate" / "we fabricate",
  p.11; all authors UMD). No facility acknowledged. No missing orgs.

## lit:guo2023a (SWG-sandwiched taper mode-order converters, SOI) - 11 components / 81 metrics

- Five fabricated `mode_converter.converter` rows (TE0-TE1, TE0-TE2, TE0-TE3, TE1-TE2, TE1-TE3): measured IL / CT at
  1550 nm (text p.11 and Table 2; TE0-TE2 and TE0-TE3 point values only in Table 2), measured IL < 1.8 dB and CT bound
  over the stated bands, simulated (3D-FDTD) IL / CT at 1550 nm, simulated IL < 0.55 dB / CT > 20 dB bands for TE0-TE1
  (1470-1620 nm) and TE0-TE2 (1510-1610 nm); geometry length (Table 2 / Fig. 4), SWG period count N_pq, tip 100 nm,
  220 nm Si / 2 um BOX / 2.2 um cladding. IL `per_component`, `reference_structure` (reference set without the converter,
  halved, p.9-10).
- One design row TE2-TE5 (simulated only, p.9): IL 0.98 dB / CT 16.1 dB, length 12.271 um, N25 39.
- Five design rows: the same converters without the fully etched SWG arrays (simulated ablation, p.9), IL / CT at
  1550 nm.
- Not entered: simulated bandwidths for CT < -15 dB and IL < 0.8 dB (200 / 180 / 120 / 200 / 160 nm, p.8; Table 2
  prints 100 nm for TE0-TE2) - no band edges printed and no criterion-bandwidth parameter; SWG pitches 250 / 200 nm
  (subwavelength_period_nm not registered for mode_converter); input / output taper widths and lengths (wI, wO, LIT,
  LOT, roles not separable into one registry parameter; in component notes); Table 2 rows of other works (rule 3);
  the grating couplers and TEi (de)MUXes of the test circuits (no values).
- Fab / facility: fab empty (passive "are fabricated", p.9, no org); no acknowledgment of a facility. No missing orgs.

## lit:chen2015c (compact-taper mode-order converters, simulation only) - 7 components / 20 metrics

- All `row_kind design` (no fabrication; "can be readily fabricated" with a 180 nm CMOS process, p.8):
  TE1-TE0 initial three-section design (2D FDTD mean 0.386 dB), optimized TE1-TE0 (2D < 0.044 dB, 3D 0.061 dB),
  TE2-TE0 (0.052 dB), TE3-TE0 (0.11 dB; < 0.5 dB mean with +/-50 nm width deviation), combined TE2-TE1 (0.119 dB),
  TE3-TE1 (0.168 dB), TE3-TE2 (0.154 dB). All values are average conversion efficiency over 1520-1580 nm
  (`statistic mean`), printed as % and dB; stored as `insertion_loss_db` (positive), % in notes.
- Lengths derived: L1 + L2 + L3 (TE1-TE0 18.616 um, TE2-TE0 19.317 um; Fig. 1 caption defines total length) and the
  x-extent of the Table 1 vertices (TE3-TE0 22.711 um); core 220 nm.
- Not entered: tolerance curves of Fig. 6 for TE1 / TE2 converters ("negligible", no number); W1 / W3 input / output
  widths (roles; in notes); process_name (no fabrication; the 180 nm CMOS statement is a feasibility remark).
- Fab / facility: none. No missing orgs.

## lit:xiao2013 (ultra-compact polarization-insensitive MMI splitter, SOI) - 4 components / 27 metrics

- `compact_mmi_1x2` (splitter.mmi, soi, Wt 540 nm): excess loss 0.11 dB TE / 0.18 dB TM / 0.14 dB unpolarized at
  1.55 um from the five-splitter cascade fit (`cutback`, measured, p.6 Fig. 6(a)-(c)); geometry 1.5 x 1.8 um, port
  0.54 um, 500 nm waveguides, 300 nm Si, 2 um BOX, 1.1 um cladding, 1 x 2 ports.
- Two sibling rows `_wt500` / `_wt580`: Fig. 6(d) measured markers (TE about 0.24 / 0.15 dB, TM about 0.27 /
  0.38 dB), `extracted_from_figure` +/-0.02 dB, 1550 nm inferred.
- `ssc` (fiber_chip_coupler.edge): cascade-fit intercepts 5.488 / 2.654 / 4.2 dB (TE / TM / unpolarized), scope
  `fiber_to_fiber` (two facets plus residual waveguide, normalized to direct lensed fiber-to-fiber coupling; not
  halved); length 200 um, tip 180 nm.
- Not entered: cascaded Y-junction splitters YI-YIII (measured fringe FSR about 20 / 25 / 28 nm and calculated 21 /
  24.5 / 26.8 nm, p.3: a property of the cascade, no splitter parameter; bend radii 20 / 10 / 5 um geometry only, so no
  rows); tolerance "0.1 dB extra loss for +/-100 nm length or +/-20 nm width" (p.6, origin not stated, no parameter);
  simulated excess-loss curves of Fig. 6(d); multimode width window 1.49-1.95 um (design range); Y-junction values of
  other works (rule 3).
- Fab: `org_astar_ime`, process_name "IME CMOS fabrication process" ("We fabricated ... through Institute of Micro
  Electronics (IME) CMOS fabrication process", p.5). Acknowledgment (NTU grant, A*STAR IME, SERC grant) is
  grant-level, no facility. No missing orgs.

## Judgment calls

- (a) ai2024 edge coupler: fab set to UMD although the first-person fabrication sentence names the MMI devices; the
  coupler is on the same chip.
- (b) ai2024 IL defined as 10log(I3 + I4) entered as `excess_loss_db` (2x2 coupler, sum of both outputs), scope
  `de_embedded`, method `unspecified` (normalized to the port-1 input; Fig. 13 names a reference line, Fig. 11 / 12 do
  not; paredes2021 D708 pattern). Broadband-source rows leave polarization empty.
- (c) ai2024 1-dB bandwidth: the paper's absolute criterion (IL and PI below 1 dB) stored in `bw_1db_nm` with the
  criterion in condition.
- (d) ai2024 edge-coupler wavelength 1450-1640 nm `wavelength_inferred` (TSL range of the same paragraph).
- (e) guo2023a TE0-TE2 simulated point: Table 2 and the conclusion (0.28 dB / -28.6 dB) entered, the p.7 text values
  (0.27 dB / -33.7 dB) in notes (D417 conflict-note pattern).
- (f) guo2023a TE1-TE2 band: only CT > 17 dB entered (stronger stated bound over the same 1515-1560 nm band); TE0-TE3
  IL < 1.8 dB tied to the 1538-1563 nm band of the same sentence.
- (g) guo2023a and chen2015c sibling design rows (TE2-TE5, five no-array ablations, TE1-TE0 initial design, three
  combined converters) entered as `row_kind design` (rule 9).
- (h) chen2015c values printed both as % and dB: stored once as `insertion_loss_db` (mean over 1520-1580 nm), %
  in notes; the 2D "above 99 % (-0.044 dB)" as `lt` 0.044.
- (i) chen2015c lengths derived (sum of printed L1-L3; TE3-TE0 vertex x-extent).
- (j) xiao2013 headline excess losses tied to Wt = 540 nm via the Fig. 6(d) markers; cascade-fit losses `measured`
  (standard fit, D80a); the Wt 500 / 580 nm sibling rows from figure markers.
- (k) xiao2013 SSC intercepts entered as `fiber_to_fiber` two-facet loss (the paper attributes the intercept mainly to
  facet coupling); not halved.
- (l) Platform `soi` for xiao2013 (channel waveguides etched to the BOX) and guo2023a, matching merged practice for
  single-layer SOI splitters / converters.

## Registry gaps (skipped value + locator, proposed definition)

- `subwavelength_period_nm` on mode_converter: guo2023a 250 nm (SWG-wires) and 200 nm (SWG arrays), p.5 (already
  listed D708).
- `fill_factor` on splitter: ai2024 SWG duty cycle 50 %, p.5 ("SWG tooth fraction of a metamaterial splitter").
- Criterion bandwidth on mode_converter (already listed D708): guo2023a simulated 200 / 180 / 120 / 200 / 160 nm for
  IL < 0.8 dB and CT < -15 dB, p.8 (band edges not printed).
- Fabrication-tolerance loss increment: xiao2013 0.1 dB for +/-100 nm length or +/-20 nm width, p.6 (rejected class in
  D77 / D81; listed for completeness).

## Missing orgs

None (UMD and A*STAR IME are in the registry; guo2023a and chen2015c have no fab / facility statement).
