# Batch lit_319 report

Papers: lit:xu2019b, lit:ros2019, lit:densmore2009, lit:dong2010a. Distilled 2026-11-28. Validation:
`merge_component_staging.py data/_staging/components/lit_319 --dry-run` -> +13 components, +107 metrics, 0 errors
(the 2 warnings are in other batches: guo2024a, ni2025b).

Page-1 title check: all four cached texts match their source rows; none is a correction / erratum; text layers clean
(`garbled_text_layer` false). No existing component rows for these four sources.

Version note: lit:xu2019b (ACS Photonics 2019) and lit:ros2019 (Science Advances 2019) are cached as arXiv preprints
(xu2019b arXiv v2 incl. Supporting Information; ros2019 arXiv v1). Values come from the preprint only; the journal
versions were not consulted. lit:densmore2009 and lit:dong2010a are the Optica open-access publisher copies.

All four papers were picked because later papers cite them in benchmark tables; only what each paper reports for its
own devices is entered (rule 1, rule 3). Cited prior-art values (e.g. dong2010a Table 1 rows for refs. 15, 18, 21,
22; densmore2009 "45 and 90 mW" of refs. 12-13; ros2019 comparisons to ref. 15) are not entered.

## lit:xu2019b (2 components / 32 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_xu2019b_dc_switch_1x2 | switch_fabric.other | soi | IL ~1 dB both states, 1520-1550 nm, per_component vs straight reference waveguide (p.6); CT > 10 dB a-GST / > 22 dB c-GST (p.6); simulated IL < 1 / < 0.6 dB, CT 11-23 / > 29 dB (p.4-5); calculated coupling length ~24 um; widths 450 / 420 / 320 (GST, derived) nm, gap 150 nm, 220 nm Si, 3 um BOX, 1 in / 2 out |
| cmp_lit_xu2019b_dc_switch_2x2 | switch_fabric.other | soi | IL ~1 dB a-GST (1510-1540 nm), 1-2 dB c-GST (inferred range); CT > 15 dB a-GST, > 10 dB c-GST, CT < -10 dB bandwidth > 30 nm (p.8); simulated IL < 1 dB, CT bandwidth > 25 nm (p.7); calculated coupling length 35 um; widths 450 / 422 / 322 nm, gap 150 nm, stack, 2 in / 2 out |

Values not entered and why:
- Reconfiguration energy ~2 nJ (p.8): estimated from the GST volume with ref. 15; no parameter.
- "~30 um" compact coupling length (abstract, p.3, conclusion): one value stated for both switches (D254); the
  calculated per-design lengths (24 um, 35 um) are entered instead (as `length_um`, since `coupling_length_um` is not
  allowed on switch_fabric; chen2022c precedent).
- L_cGST 516 um and the ratio 14.7 (p.7): calculated beat length of the crystalline state, not a device dimension
  (noted on the component).
- Fig. S2 / S4 gap sweeps (supplement): curves without printed values.
- Focusing sub-wavelength grating couplers (p.9): no performance printed; no row.
- No phase-shifter row: the GST state is set by annealing the whole chip (RTA 200 C, 10 min), no on-chip actuator.

Fab / facility: fab empty (passive "were fabricated", p.5 / p.8; authors at University of Washington, Ningbo
University, Intel; D80b). Missing facility org: "Washington Nanofabrication Facility / Molecular Analysis Facility"
(p.9 Acknowledgements, "Part of this work was conducted at ..."), role facility; not in `organizations.csv` /
`org_aliases.csv` (already reported for lit:chen2022c, D604).

Judgment calls:
- Classed as two `switch_fabric.other` rows (D158 / D407, chen2022c precedent), platform `soi` (paper calls the Si
  waveguides strip waveguides; etch to the BOX implied, not printed as a depth).
- 1x2 IL "approximately 1 dB for both states" is one row with both states in the condition (rule 7).
- 2x2 c-GST IL and CT carry the Fig. 4(e) axis range 1510-1540 nm with `wavelength_inferred` true.
- Simulated 2x2 bandwidth "> 25 nm" for two criteria (a-GST < -15 dB, c-GST < -20 dB) is one row.

## lit:ros2019 (2 components / 9 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_ros2019_gst_cell_2um | phase_shifter.phase_change | sin | 13 levels (single-shot Write / Erase, p.5, Fig. 2(d)); retention 10^4 s without measurable drift, 0.1 mW probe on (p.7); L_GST 2 um, W 1300 nm (derived), etch 165 nm, Si3N4 330 nm, SiO2 3.3 um |
| cmp_lit_ros2019_gc | fiber_chip_coupler.grating | sin | coupling efficiency ~20 % per coupler (author_estimate, origin not stated), peak 1598 nm (p.12) |

Values not entered and why (no registry parameter unless noted):
- Erase double-step pulse 14.1 mW / 25 ns + 5.64 mW / 100 ns, about 577 pJ total (p.5, Fig. 2(b)); Write/Erase
  settling ~200 ns, 2.5 MHz operation, 125 ns Erase time (p.5, p.11); switching energies 120-220 pJ and 350-600 /
  200-360 pJ (Fig. 2(c), Fig. 3).
- Level error standard deviation 0.35 % over 600 transitions (p.6, Fig. 2(e)); the 600 transitions are not entered as
  `endurance_cycles` (level-to-level transitions, not set / reset cycles; the paper does not equate them).
- Transmission change Delta T up to 0.143 (about 15 %, Fig. 2(d)): not converted to an extinction (li2018
  precedent).
- Probe-off drift of nearly 9 % (Fig. 3(b)) and its cure at 0.05 mW (Fig. 3(c)).
- 1 um GST cell (Fig. 2(a): saturation above 45 ns, 25 ns pulses reach 75 % of the maximum change): no registry
  metric, so no component row (rule 9).
- Scalar multiplication results (429 products, error statistics, Fig. 4): system-level, not a component value.

Fab / facility: fab empty (passive "were fabricated", p.12; authors at University of Oxford, IBM Research - Zurich,
University of Muenster, University of Exeter; D80b). No facility named; "homebuilt RF sputtering system (Nordiko)" is
equipment (note only). No missing org.

Judgment calls:
- Amplitude-only PCM memory kept as `phase_shifter.phase_change` (D155, li2018 precedent).
- One row for the 2 um design although several 2 um cells are measured (Fig. 2, Fig. 3(a)-(b), Fig. 3(c)); population
  noted on the component. Retention entered as the printed 10^4 s; the Fig. 3(a) caption mentions ~8.5 h of constant
  measurement (time axis to about 31,700 s), noted on the row.
- Grating coupler efficiency "~20%" scoped `per_coupler`, method unspecified, `author_estimate` (origin not stated).

## lit:densmore2009 (6 components / 35 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_densmore2009_spiral_heater | phase_shifter.thermo_optic | soi | P_pi ~6.5 mW measured (1550 nm, TM), 6.1 mW simulated; heater ~80 ohm; rise 14 us; 3-dB cutoff ~25 kHz (derived from rise time); L_H 6300 um, heater 10 um wide, 1355 um long, 80 nm Cr/Au, cladding 1.5 um, wire 450 x 260 nm, BOX 2 um |
| cmp_lit_densmore2009_spiral_mzi_switch | switch_fabric.other | soi | ER ~22 dB (p.6, Fig. 5); IL ~6 dB de_embedded (splitting + propagation, excl. fiber coupling, p.6); 1 in / 1 out |
| cmp_lit_densmore2009_straight_heater | phase_shifter.thermo_optic | soi | P_pi 36 mW mean over the straight series (Fig. 4), 31 mW simulated (6.3 mm); rise ~12 us (6.6 mm device); heater 10 um, stack |
| cmp_lit_densmore2009_wire_wg | waveguide_platform.straight | soi | 5 dB/cm (printed 0.5 +/- 0.1 dB/mm, Fabry-Perot method with simulated ~20 % facet reflectivity: author_estimate) |
| cmp_lit_densmore2009_spiral_bends | waveguide_platform.bend | soi | bend-loss penalty of the double spiral < 0.5 dB (on_chip_excess), min bend radius 4 um |
| cmp_lit_densmore2009_inverse_taper | fiber_chip_coupler.edge | soi | ~3 dB per facet to a lensed fiber (D167); tip 150 nm, start width 450 nm (derived) |

Values not entered and why:
- Calculated 14.1 mW for an infinitely narrow heater (p.8): hypothetical design, no device.
- Calculated pi-shift temperature 0.67 K and dNeff/dT 1.82e-4 (p.3): design inputs, no parameter.
- Spiral geometry: wire pitch 2 um, electrode pitch 12 um, 65 um circular radius (p.3-4, p.7, p.9): `pitch_um` /
  `radius_um` are not allowed on phase_shifter / switch_fabric (noted on the component).
- Fig. 4 individual P_pi points of the spiral and straight series: only the 6.3 mm spiral value and the straight
  average are printed; not read off the figure.
- Minimum lower-cladding thickness ~0.7 um for low substrate leakage (p.8): design remark.
- Si thermo-optic coefficient 1.86e-4 /K (p.2): cited material constant.

Fab / facility: fab empty (passive "devices were fabricated on unibond SOI wafers obtained from SOITEC", p.6; "we have
developed" p.3 does not qualify, D80b; all authors at NRC Institute for Microstructural Sciences). SOITEC = wafer
supplier (notes). No facility. No missing org.

Judgment calls:
- Spiral MZI split into a switch row (ER, IL) and an actuator row (P_pi, rise time, heater) (D396, chang2026a
  precedent); the straight design gets an actuator row only (no switch-level values printed).
- IL ~6 dB of "the longest 6.3 mm MZI device" assigned to the spiral switch: the straight devices extend to about
  7.6 mm in Fig. 4, so the longest-at-6.3-mm device is the spiral one (reasoning noted on the row).
- Loss-breakdown terms stated directly without a method (IL ~6 dB, coupling ~3 dB, bend penalty < 0.5 dB) entered as
  `measured`, method unspecified (D167 analogue); the propagation loss is `author_estimate` because it rests on a
  simulated facet reflectivity.
- 25 kHz cutoff `derived` (authors' conversion of the rise time; chang2026a precedent).
- Polarization `tm` for all measured rows: the paper states the quasi-TM mode is used in this work (p.3-4).

## lit:dong2010a (3 components / 31 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_dong2010a_ring_mux_2ch | wdm.mrr | soi | FSR 19 nm, Q ~8000 (loaded, unqualified), 3-dB bandwidth ~0.2 nm (C band inferred from Fig. 4 axes); 2 channels; radius 4 um, coupling length 2 um, gap 170 nm (derived), wire 450 x 250 nm, BOX 3 um, cladding 1.2 um |
| cmp_lit_dong2010a_heater_trench | phase_shifter.thermo_optic | soi | 21 mW per FSR (derived, 1.10 mW/nm x 19 nm); 909 pm/mW (derived reciprocal of 1.10 mW/nm); 14 mW simulated; thermal time constants 9 us rise / 6 us fall; heater 1 um x 100 nm Ti, stack |
| cmp_lit_dong2010a_heater_no_trench | phase_shifter.thermo_optic | soi | 27 mW per FSR (derived), 704 pm/mW (derived), 25 mW simulated; heater, stack |

Values not entered and why:
- Thermal crosstalk: measured < 0.5 % between rings 15 um apart (0.03 nm vs 7.75 nm shift, p.6); simulated 1.5 % /
  3.0 % for a probe waveguide 15 um away with / without trenches (p.4). No registry parameter (gap below).
- Edge-to-edge ring distance 15 um (p.4): not a centre pitch, so not `pitch_um` (pitfall: spacing entered as pitch).
- Trench geometry (2 um from the waveguide edge, 2 um into the substrate, p.3-4): no parameter.
- Drop-port peak levels and extinction in Fig. 4: not stated in the text and normalization not described; not read.
- 25 Gbps / ~1 dB power penalty (p.5): cited (ref. 25). 5 um-diameter-ring scaling, 2.5 mW / 100 fJ/bit (p.6-7):
  projections.
- Table 1 rows of refs. 15, 18, 21, 22: cited work.

Fab / facility: `org_kotura` on all 3 rows, borderline (D84b): acknowledgment thanks three Kotura Inc. staff "for
their work in fabricating of the device" (p.7); first-person fabrication text (p.4) by authors at Kotura and Sun Labs /
Oracle; same ruling as the sister paper lit:dong2010. No facility. No missing org.

Judgment calls:
- One `wdm.mrr` row for the ring design shared by the trench and no-trench devices: FSR, Q and bandwidth are stated
  once for "the ring spectra" of Fig. 4 (both devices); the trench / no-trench difference is carried by two heater
  rows (rule 9: the heater structure, not the ring, differs).
- Tuning efficiency printed in mW/nm converted to the registry unit pm/mW as a reciprocal (`derived`, printed value
  in notes, D256).
- Time constants from exponential fits entered as `thermal_time_constant_us` (not rise / fall times) on the heater
  row (`thermal_time_constant_us` is not allowed on wdm).
- Platform `soi`: the paper does not name strip vs rib, but the Fig. 1(b) cross-section shows a channel waveguide
  (noted in core_material).

## Registry gaps

- Thermal crosstalk between adjacent thermally tuned elements (lit:dong2010a: measured < 0.5 %, p.6; simulated 1.5 %
  / 3.0 %, p.4). Proposed `thermal_crosstalk_pct` (unit %, classes phase_shifter, wdm, resonator, switch_fabric):
  "phase or resonance shift induced in a neighbouring unheated element as a percentage of the shift of the heated
  element, at the stated separation (separation and definition in condition)".
- `coupling_length_um` on switch_fabric (lit:xu2019b calculated coupling lengths 24 / 35 um entered as `length_um`;
  chen2022c precedent). Proposed: allow `coupling_length_um` for switch_fabric (directional-coupler switches).
- `pitch_um` / a spiral-area radius for phase_shifter (lit:densmore2009 wire pitch 2 um, heater pitch 12 um, 65 um
  radius area). Low priority; single paper.

## Missing orgs

| name as printed | locator | role |
|---|---|---|
| Washington Nanofabrication Facility / Molecular Analysis Facility | lit:xu2019b p.9 Acknowledgements | facility |
