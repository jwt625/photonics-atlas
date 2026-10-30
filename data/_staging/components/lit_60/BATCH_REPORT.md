# Batch lit_60 report (distill subagent, 2026-10-30)

Classes switch_fabric, wdm. Papers: campenhout2009, xia2007, a2011, feng2011, shoji2010 (all Optics Express,
`restricted_local_only`: facts and locators only, no quotes beyond a few words). Dry-run
`batch lit_60: +14 components, +148 metrics; errors 0` (only the pre-existing WARN on cmp_lit_ni2025b_pimmwc-m18).
Page-1 titles and authors match the source rows; every text has its full page count (10 / 8 / 7 / 6 / 5); none is a
correction or erratum; no `garbled_text_layer` flag. Renders read: campenhout2009 p.6 (Fig. 3, Table 2), xia2007 p.6
(Fig. 3 SEM), a2011 p.7 (Fig. 5), feng2011 p.5 (Figs. 4-5 axes), shoji2010 p.3 (Fig. 2(b) labels) and p.4 (Figs. 3-4).
Rows built by a scratchpad script. ASCII only, no e-mail, no addresses.

## Per paper (components / metrics)

- campenhout2009 (2 / 37): WIMZ 2x2 carrier-injection switch (switch_fabric.other, D158): off-state 110 nm bandwidth at
  < -18 dB crosstalk (1530 +/- 55 nm, both inputs), on-state crosstalk < -23 dB (a1) / < -17 dB (a2), passive IL 1.1 dB
  (1480 nm) and 2.0 dB (1590 nm) vs an on-chip reference waveguide, on-state total IL 2.0 / 2.9 dB (derived, authors'
  sum), pulsed on-state crosstalk < -20 dB at 1518 nm, 3.1 mW on-state power (p_pi_mw, derived from Von x Ion),
  switching times 4 / 1.8 ns (off-on, 20 / 10 dB) and 0.65 / 0.5 ns (on-off) as rise / fall_time_us (derived, ns -> us,
  extinction-level definition in condition), temperature (30 C -18 dB, 50 C -17 dB) and duty-cycle (10 / 50 / 83 %:
  18 / 17 / 16 dB, < -14 dB long messages) crosstalk, footprint 50 x 400 um2, rib stack (500 nm, 220 / 50 nm, 170 nm
  etch, 2 um BOX), simulated 110 nm and < -19 dB. Conventional MZ reference as a design row (simulated 35 nm, ~-20 dB on
  state, 300 nm gap, 50 x 330 um2).
- xia2007 (3 / 29): 5-ring and 3-ring coupled-racetrack flat-top filters (wdm.mrr, D400 channel filters for a WDM
  device; jeong2013 precedent): IL 1.8 / 1.0 dB (de_embedded vs off-resonance through port), 1-dB band 310 GHz
  (5-ring), out-of-band rejection >= 40 / 35 dB as crosstalk_db, FSR 18 nm measured / 17.8 nm design, designed 330 GHz,
  R 4 um, LC 3.5 um, ring-ring gaps 90 / 110 nm, 45 % bus coupling (BPM), 0.0007 mm2; photonic wire 3 dB/cm on the same
  wafer (waveguide_platform.straight).
- a2011 (2 / 25): 16-ch 200 GHz Si3N4 nano-core AWG (wdm.awg, sin): on-chip loss ~< 0.5 dB (Table 1), FSR 25.3 / 18.4 nm,
  spacing 1.58 / 1.34 nm, adjacent / non-adjacent crosstalk ~25 / 30 (best) dB at 1550 and > 30 / ~40 dB at 1310 nm,
  10.8 pm/K (Fig. 5(b) fit), design 16 ch, 150 arms, order 60, FPR 3000 um, dg 20 um, 5.5 um x 50 nm core, 15 / 15 um
  claddings, 2 x 1.5 cm. Lensed-fiber facet < 2 dB/facet (fiber_chip_coupler.edge).
- feng2011 (2 / 18): 40-ch 100 GHz flat-top echelle (wdm.eg, soi_rib 3 um): on-chip loss < 5.0 dB, 1-dB 50 GHz, 100 GHz
  spacing, isolation > 30 dB (crosstalk_db, type not stated), PDL < 0.3 dB, 85 pm/K (author_estimate, origin not
  stated), order 16, pitch 12.3 um, stack, facet sidewall >= 88.5 deg, chip 25 x 10 mm. p-i-n VOA (phase_shifter.other,
  morichetti2021 precedent): 20 dB at ~25 mA, 3 MHz small-signal bandwidth at 5 dB attenuation.
- shoji2010 (5 / 39): 2x2 MZI-array (dilated) TO switch (switch_fabric.other): best crosstalk 50 dB bar (1550 nm) /
  30 dB cross (1570 nm), 20 dB fiber-to-fiber IL, <= 160 mW; single MZI element reference (switch_fabric.other,
  test structure): 25 / 20 dB, 16 dB IL, 4 dB excess (derived, loss breakdown), 40 mW, 30 us response, 200 x 200 um2;
  vertically aligned DC intersection (crossing.other): best crosstalk 35 dB at 1560 nm; Si wire 8 dB/cm; narrowed-wire
  SSC 4.5 dB/facet. Geometry 450 x 220 nm, 3 um BOX, 2.5 um cover, 40 um Pt heater, Fig. 2(b) labels 5.0 um / 50 nm
  (extracted_from_figure).

## Values deliberately not entered

- campenhout2009: Von 1 V / 1.02 V, 0.3 V swing on 0.87 V bias, VpiL ~0.06 V mm (modulator metrics, EO atlas per the
  coordinator brief); on-state FCA-only loss 0.9 +/- 0.2 / 0.9 +/- 0.4 dB measured and 0.8 dB simulated (EO
  phase-shifter loss, lu2016a precedent); series resistance 8 ohm / 1.6 ohm mm (series_resistance_ohm not allowed for
  switch_fabric); 6 fJ/bit (rests on an assumed WDM load); center wavelength 1530 nm vs 1550 nm design (no
  center_wavelength_nm for switch_fabric); broadband-coupler DC lengths 15 / 24.5 um, kappa 0.4 / 0.8, 160 nm imbalance,
  200 um phase-shifter length (no role parameter; coupler not characterized alone). All values in component notes.
- xia2007: ripple < 0.4 dB measured / < +/-0.15 dB simulated and 1- to 20-dB shape factors 0.7 / 0.35 (no parameter);
  inter-ring kappa^2 9 % / 5 % (power_coupling_pct is bus-to-resonator); MMI width ("about 100 nm wider than" the two
  access waveguides, reference ambiguous); 0.035 dB round trip (cited [7, 8]); n_g 4.25 (assumed, cited); 3-ring 1-dB
  bandwidth (only "25 % larger than simulation", simulated value plotted only); FSR not repeated on the 3-ring row (stated
  once, Fig. 5 is the 5-ring filter).
- a2011: 0.4-0.8 dB/m and 0.03 dB/cm (cited from the authors' refs [17] / [16], D259); ~1 um array gap (not a coupling
  gap); Table 1 rows of other works; 13 usable channels at 1310 nm.
- feng2011: PDF < 2.5 GHz measured, 35 GHz intrinsic (no parameter); simulated ~0.1 dB compensator penalty and
  < 0.5 dB diffraction-envelope loss (design); abstract 5.0 dB and conclusion 4.5 dB loss and conclusion "20 dB at 20 mA"
  (inconsistent restatements, in notes); array angles 17 / 16.4 deg, facet width 11.7 um.
- shoji2010: intersection insertion loss (plotted only); -40 dB cross-state target; Fig. 2(a) 700 um (scale label).

## Organizations

- campenhout2009: fab org_ibm_watson ("staff of the MRL at the IBM T. J. Watson Research Center, where the devices were
  fabricated", p.10, plus IBM CMOS modules p.5; all authors IBM Watson). MRL is IBM's internal lab: no facility.
- a2011: "The optical waveguides were fabricated by LioniX BV, Netherlands" (p.7 Acknowledgements; p.4 TriPleX).
  Missing from the registry: LioniX BV (Enschede, NL); org_lionix_international is the later LioniX International BV and
  is not mapped (hosseini2015 precedent). Fab empty.
- shoji2010: "IBEC Innovation Platform at the Nano-Processing Facility, AIST" (p.5 Acknowledgments, support statement):
  facility missing from the registry (AIST Nano-Processing Facility, Tsukuba, JP; parent org_national_institute_of_
  advanced_industrial_science_and_technology). Fab empty (passive "were fabricated", all authors AIST, D80b).
- xia2007: fab empty (process "similar to" earlier refs, wafers from SOITEC = supplier note). feng2011: fab empty
  (passive "was fabricated", all authors Kotura; org_kotura exists).

## Judgment calls

1. shoji2010 2x2 MZI array as switch_fabric.other (one 2x2 switch built from four MZIs in a dilated / double-MZI
   arrangement; dheer2018 dilated-element analogue) rather than mzi_mesh; the stand-alone single MZI is a separate
   switch_fabric.other test-structure row.
2. campenhout2009 switch scope: crosstalk, bandwidth, switch IL, on-state power and switching times entered; Von / VpiL
   and the FCA-only on-state loss kept out (brief + lu2016a). The on-state total IL is the authors' sum of the measured
   passive and FCA losses (derived, loss_breakdown).
3. campenhout2009 switching times stored in rise_time_us / fall_time_us although they are 10-dB / 20-dB extinction times
   (definition in condition and notes); alternative: keep them in notes until a switching-time parameter exists.
4. campenhout2009 crosstalk span 1475-1585 nm = 1530 +/- 55 nm (text "110 nm centered around 1530 nm", matches the
   Fig. 3 markers); the 30 / 50 C labels entered without qualifier (worst level in the window).
5. xia2007 out-of-band rejection as crosstalk_db (jeong2013 / morichetti2021 precedent); 5-ring 40 dB with qualifier ge
   ("can be larger", setup-limited).
6. a2011 pitch_um 20 from the printed output-waveguide "end separation dg" (standard AWG notation; reviewer may prefer
   notes only); thermal drift from the Fig. 5(b) fit label 0.0108 nm/C rather than the text's rounded 0.011.
7. shoji2010 element excess loss 4 dB `derived` (authors' estimate from their own 16 dB IL and measured 4.5 dB/facet and
   8 dB/cm; path length not stated); fiber-to-fiber ILs and losses without a stated wavelength get cl_band inferred from
   the 1520-1630 nm tunable laser.
8. feng2011 on-chip loss band c_band inferred from the Fig. 4 axis (about 1523-1556 nm); the loss covers the VMUX path
   including the unbiased VOA.

## Registry gaps (proposed)

- switch_fabric `center_wavelength_nm`: campenhout2009 1530 nm measured vs 1550 nm design (p.6).
- switch_fabric / phase_shifter `series_resistance_ohm`: campenhout2009 8 +/- 2 ohm, 1.6 +/- 0.4 ohm mm (p.7).
- switch_fabric `switching_time_ns` (time to a stated extinction level): campenhout2009 4 / 1.8 / 0.65 / 0.5 ns (p.8);
  entered in rise / fall_time_us for now.
- wdm `passband_ripple_db`: xia2007 < 0.4 dB (p.8); `shape_factor` (1- to 20-dB): 0.7 / 0.35 simulated (p.3-4).
- wdm `pdf_ghz` (polarization-dependent frequency shift): feng2011 < 2.5 GHz measured, 35 GHz intrinsic (p.3-4).
