# lit_254 batch report

Papers: lit:zhu2018 (IEEE Photonics J.), lit:alboresmejia2010 (JLT), lit:park2011 (Optics Express), lit:stabile2016
(IEEE PTL), lit:fan2021a (ICOCN 2021). Page-1 titles match the source rows; no garbled text layers. verified_on
2026-11-22. Dry run: +19 components, +141 metrics, 0 errors (the only warning is a pre-existing ni2025b duplicate,
not in this batch). No existing rows for these sources. Values are only what each paper reports itself; comparison
tables of other works (fan2021a Table 2, park2011 Table 1 silica-AWG column) are not entered.

## Components / metric rows

| paper | component | class | metrics |
|---|---|---|---|
| zhu2018 | cmp_lit_zhu2018_mzi_to_switch | switch_fabric.other | 17 (ER: best 35, > 30 all four paths at 1628 nm, Fig. 4 bar 18.5 / 30.3 (text) and figure reads, Fig. 2 bar / cross reads; switching power 33.7 mW; 500 / 220 nm, 2 um BOX, 300 nm DC gap) |
| zhu2018 | cmp_lit_zhu2018_tin_heater | phase_shifter.thermo_optic | 4 (350 ohm; 100 x 4 um; 2 um oxide gap) |
| alboresmejia2010 | cmp_lit_alboresmejia2010_soa_crossbar_4x4 | switch_fabric.other | 18 (4 / 4 ports; 12 per-path on-chip IL from Table III circuit gain; ER 41.2 dB; 1.2 ns 20-80 % transition; 0.17 W per crossbar estimate; 15 mm2) |
| alboresmejia2010 | cmp_lit_alboresmejia2010_soa_gate_1mm | amplifier.soa | 11 (Table II gain at 44 / 66 / 88 / 110 mA; 3-dB width 38.6 nm; in-circuit gain per stage 5.3-10.1 dB; 4-6 ohm; 0.49-0.53 V at 1 mA; 2 x 1000 um; 250 um island pitch) |
| alboresmejia2010 | cmp_lit_alboresmejia2010_mmi_1x1_mode_filter | mode_converter.other | 1 (0.5 dB) |
| alboresmejia2010 | cmp_lit_alboresmejia2010_mmi_1x2 | splitter.mmi | 1 (excess 0.49 dB from -3.5 dB) |
| alboresmejia2010 | cmp_lit_alboresmejia2010_deep_shallow_transformer | waveguide_platform.other | 1 (0.16 dB, cutback fit) |
| alboresmejia2010 | cmp_lit_alboresmejia2010_shallow_wg_2um | waveguide_platform.straight | 2 (5.5 dB/cm; 2 um) |
| alboresmejia2010 | cmp_lit_alboresmejia2010_deep_wg_1p5um | waveguide_platform.straight | 3 (8.0 dB/cm; 1.5 um; 100 um min bend radius) |
| alboresmejia2010 | cmp_lit_alboresmejia2010_lensed_fiber_facet | fiber_chip_coupler.edge | 1 (6.0 dB per facet, estimate) |
| park2011 | cmp_lit_park2011_mrr3_32ch | wdm.mrr | 20 (32 ch; 50 / 100 GHz grids; FSR 12.8 nm; ng 3.1; adjacent XT ~20 dB; 3-dB 0.56 nm; 1-dB 0.3 nm; IL ~5 dB; sigma 0.237 / 0.185 nm; 43.35 pm/K; R 9 um; 2 um coupling region; gaps 400 / 500 nm; width 1000 design / 984 SEM; height 190 design / 196 SEM) |
| park2011 | cmp_lit_park2011_facet_taper_10um | fiber_chip_coupler.edge | 2 (~3 dB per facet typical; 10 um facet width) |
| stabile2016 | cmp_lit_stabile2016_ring_switch_4x4 | switch_fabric.other | 12 (4 / 4 ports; on-chip path IL 24.7 / 29.1 / 30.0 / 33.4 dB; fiber-to-fiber 17.9 / 32.5 dB; Table II extinction 14.3 / 14.2 / 15.0 / 14.5 dB) |
| stabile2016 | cmp_lit_stabile2016_switch_element | switch_fabric.other | 7 (ER 15 measured / 36 design; 3-dB 11.25 GHz measured / 12.5 design; 79 uW; rise / fall < 10 ns) |
| stabile2016 | cmp_lit_stabile2016_third_order_ring | resonator.coupled_rings | 12 (FSR 62.5 GHz; coupling 78 / 15 % fitted, 50 / 9 % design; 28.75 pm/V; 0.23 nm range; 20 um bend radius; 450 um coupler; 2 um width; gaps 1100 / 1560 nm) |
| stabile2016 | cmp_lit_stabile2016_soa_500um | amplifier.soa | 2 (3 dB at 20 mA; 500 um) |
| stabile2016 | cmp_lit_stabile2016_deep_shallow_taper | waveguide_platform.other | 1 (~0.2 dB simulated) |
| stabile2016 | cmp_lit_stabile2016_wg_bend_180 | waveguide_platform.bend | 2 (~0.2 dB per 180-degree bend simulated; 20 um) |
| fan2021a | cmp_lit_fan2021a_cyclic_awgr_16x16 | wdm.awg | 24 (16 ch / 16 x 16; 100 GHz; 1542.12 nm design; order 120; 80 arms; dL 125.94 um; 2500 um bend; 4.4 x 4.4 um; 12.5 / 21 um clads; 15 x 24 mm; IL 1.64-6.46 dB all ports, center / edge input ranges; adjacent / non-adjacent XT 39.12 / 33.18 (center) and 36.48 / 28.28 (edge, worst); 3-dB > 0.4 nm; PDL < 0.39 dB; +/-0.056 nm grid offset) |

Per paper: zhu2018 2 / 21, alboresmejia2010 8 / 38, park2011 2 / 22, stabile2016 6 / 36, fan2021a 1 / 24.

## Values not entered and why

zhu2018
- Phase tuning efficiency about 0.09 rad/mW (p.6): no parameter (rad/mW); not converted to a second P_pi.
- Measured ER-optimal wavelength 1628 nm vs 1550 nm design (p.6): no center_wavelength parameter for switch_fabric.
- DC length 45 um (p.3): coupling_length_um not allowed for switch_fabric (notes).
- Simulated ER 19.8 -> 32.7 dB (1600-1625 nm) for the hypothesized w2 = 503 nm / h2 = 222.3 nm geometry and the Fig. 3
  / Fig. 6 sensitivity results (p.4-8): models of assumed dimensions, not the device design.
- Insertion loss: Fig. 2 / Fig. 5 are normalized transmissions, reference not stated.
- "Bar ER lower by up to 20 dB", "< 5 dB between the two bar paths", FIB/SEM "< 5 nm" width / height differences:
  differences, no parameter (notes).

alboresmejia2010
- Table III passive losses (20.8-43.4 dB per path): budgets computed from Table II and Table I counts, not measurements.
- OSNR (23.0-39.5 dB/0.06 nm), power penalties (0.6 / 1.2 / 0.8 / 2.0-2.2 dB), 1.6 pJ/bit, BER and input dynamic range
  (dBm values lost in the text layer): no parameters / system level.
- Facet reflectivity "expected to be 34 %" (p.3): an expectation, and reflectivity_pct is not allowed for the coupler.
- Peak modal gain about 40 cm-1 (Fig. 5): cm-1 is not dB/cm; not converted.
- Laser oscillation currents (122 / 95 mA) and the six-quantum-well active layer: notes only.
- Waveguide crossings (shallow-etched, orthogonal): no value printed, no row.

park2011
- Transfer-matrix design inputs t2 = 0.3 / 0.07, alpha 0.995 for 2 dB/cm (p.3): the sentence ends in ref. [13]
  (D80i) and they are model inputs.
- Error-source decomposition (pattern density 0.364 -> 0.005 nm, photomask ~0.023 nm, width ~0.091 nm, Si thickness
  0.992 nm/cm): rough contribution estimates, no parameter.
- 2-dB passband 0.5 nm, 120 of 160 channels inside it: no 2-dB width parameter.
- TE-mode comparison statements (> 10 % missing channels, ~0.08 nm/C cited [16]): cited or qualitative.
- First-order ring filters with 600-1200 nm gaps (p.3): fabricated, no values.

stabile2016
- VpiL 5.5 V mm (p.3): electro-optic modulator metric (EO-atlas candidate, campenhout2009 precedent).
- Waveguide loss 6 dB/cm (cited ref. [17]) and the 1.7 dB per ring / 5.1 dB per element round-trip losses resting on
  it (rule 3).
- "Worst case 5.3 dB losses between the paths" (p.2): does not match the printed path losses (spread 8.7 dB); notes.
- Fiber-chip coupling 2 x 6 dB: origin and coupler type not stated; no coupler row (notes).
- Element pitches 850 / 250 um, 4 x 4.6 mm2 generic cell, 1305 um circumference, power penalties: no parameter for
  the class or system level (notes).
- Output SOA transparency current 10 mA: no parameter.

fan2021a
- Abstract "worst crosstalk about 30 dB" / Table 2 "> 30" / conclusion "most channels": conflicts with the printed
  edge-input non-adjacent -28.28 dB (entered); D417 note.
- Polarization-dependent wavelength shift < 0.03 nm (p.3): registry gap (below).
- Rowland circle radius 2912.99 um and arrayed-waveguide pitch 12 um (Table 1): no role parameter (fpr_length_um /
  pitch_um have other meanings).
- SSC with segmented sub-wavelength grating, FPR tapers: designed, no values.

## Missing fab / facility orgs

None missing from the registry. Orgs used: org_jeppix (alboresmejia2010, "The device was provided through the Photonic
Integration Platform JePPIX", p.8), org_smart_photonics (stabile2016, p.2), org_electronics_and_telecommunications_research_institute
(park2011, first-person fabrication, p.4). Fab left empty: zhu2018 ("fabricated in a CMOS foundry", p.3, foundry not
named), fan2021a (first-person "we used conventional silica-based PLC technology", p.2, authors at Zhejiang University
and Lightip Technologies (Hangzhou); site not stated). Lightip Technologies is not in the registry, but it is not used
here (affiliation only; header batches cover it).

## Judgment calls

- (a) fan2021a IL rows scope `fiber_to_fiber`: measured on the SMF-pigtailed module, coupling removal not stated
  (palmer2026 pigtailed precedent); alternative is `unspecified`.
- (b) alboresmejia2010 fab = org_jeppix only ("provided through" JePPIX next to "fabricated on a multi-project
  wafer"), treated as the MPW access provider (D398, Contract v7 brokers); the foundry is not named.
- (c) alboresmejia2010 Table III circuit gains entered as positive `insertion_loss_db` (de_embedded,
  author_estimate): the removed coupling is the 6.0 dB estimate (p.5). The in-circuit gain per stage 5.3-10.1 dB is
  one range row on the SOA (author_estimate).
- (d) alboresmejia2010 Table II SOA gains `derived` (1 mm gate gain estimated from VSL modal gain); FP waveguide losses
  `measured` (D394) although the facet reflectance used is not stated; transformer 0.16 dB from the text fit
  (Table II rounds to 0.2).
- (e) zhu2018 heater row split from the switch (D396; alexander2024 precedent) with the 33.7 mW switching power on
  the switch row as p_pi_mw (abediasl2015 / guo2017a precedent), not duplicated on the heater.
- (f) zhu2018 figure reads: Fig. 2 bar ER about 9 / 13 dB (1550 / 1580 nm, both inputs), cross about 34 dB; Fig. 4
  input-2 bar and input-1 cross markers. Fig. 4 text values (18.5 / 30.3 dB) kept measured with statistic empty
  (whether means is not printed).
- (g) park2011 one wdm.mrr row for the 32-channel filter; Table 1 ("16 channel ring filters") values carry the
  condition "odd channels of the 32-channel filter" because p.6 says Table 1 uses the odd channels of Fig. 2(b).
  Design grids 50 / 100 GHz as author_estimate (D82a). SEM labels 984 / 196 nm entered `measured` next to the
  design 1000 / 190 nm.
- (h) stabile2016 split into matrix, element (D407), coupled-ring resonator (D396), SOA, taper and bend rows
  (dasmahapatra2014 sibling layout in lit_252). FSR 62.5 GHz `author_estimate` (circumference-derived, same value in
  both Table I columns); fitted coupling 78 / 15 % `derived` (8 % etch-lag model matched to the measured response).
  "Taper loss and 180-degree bend loss of order of 0.2 dB" read as each (simulated, approx).
- (i) stabile2016 on-chip path IL `author_estimate` (subtracted 2 x 6 dB coupling of unstated origin, D428);
  fiber-to-fiber 17.9 / 32.5 dB measured. Rise / fall "< 10 ns" from the abstract as `lt` rows (derived, unit
  conversion).
- (j) alboresmejia2010 1.2 ns transition entered as rise_time_us (0 -> 115 mA step, 20-80 % noted).

## Registry gaps

- `pd_wavelength_shift_nm` (polarization-dependent wavelength shift of a filter passband): fan2021a < 0.03 nm, p.3
  Sec. 3. Proposed: wdm / polarization, "shift of the passband center between TE and TM inputs".
- `center_wavelength_nm` for switch_fabric: zhu2018 ER-optimal wavelength 1628 nm, p.6.
- `coupling_length_um` and `pitch_um` for switch_fabric: zhu2018 DC 45 um (p.3); stabile2016 element pitch 850 /
  250 um (p.2).
- Phase-shifter tuning efficiency in rad/mW (zhu2018 0.09 rad/mW, p.6): single value, low priority.
