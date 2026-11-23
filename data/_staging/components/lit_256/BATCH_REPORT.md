# lit_256 batch report

Papers: lit:atabaki2010 (Optics Express 2010), lit:yu2016a (Optica 2016), lit:lin2022c (IEEE Photonics J. 2022),
lit:song2016a (IEEE PTL 2016), lit:koos2007 (IEEE PTL 2007). Page-1 titles match the source rows (atabaki2010 title
text has ligatures / line breaks only); no garbled text layers; the institutional download stamp in song2016a / koos2007
was ignored. verified_on 2026-11-23. Dry run: +31 components, +175 metrics, 0 errors (the only warning is the
pre-existing ni2025b duplicate, not in this batch). No existing rows for these sources. Only values each paper reports
itself; comparison tables of other works (lin2022c Table I) and values cited from earlier work (atabaki2010 ref. [27]
75 ns device, ref. [28] BOX / cladding loss thresholds) are not entered. Tables / equations missing from the text
layer (song2016a Tables I-III, koos2007 symbols) were read from page renders; figure values from 300-400 dpi renders.

## Components / metric rows

| paper | component | class | metrics |
|---|---|---|---|
| atabaki2010 | cmp_lit_atabaki2010_ni_heater_w0p5 | phase_shifter.thermo_optic | 7 (139 kHz; rise / fall ~4 us; 590 ohm; 0.5 um / 75 nm Ni / 1 um gap) |
| atabaki2010 | cmp_lit_atabaki2010_ni_heater_w1 | phase_shifter.thermo_optic | 9 (132 kHz; rise 4.2 us, fall 4.49 us (Fig. 5(b)); pulsed rise < 1 us; 725 ns model limit (simulated); tau_diff 1.5 us; geometry) |
| atabaki2010 | cmp_lit_atabaki2010_ni_heater_w2 | phase_shifter.thermo_optic | 6 (109 kHz; rise 4.84 / fall 5.07 us Fig. 5(b); geometry) |
| atabaki2010 | cmp_lit_atabaki2010_ni_heater_w1_sin_clad | phase_shifter.thermo_optic | 2 (162 kHz; 1 um) |
| atabaki2010 | cmp_lit_atabaki2010_ni_heater_w0p5_trench | phase_shifter.thermo_optic (design) | 3 (rise / fall 6.2 us simulated; 0.5 um) |
| atabaki2010 | cmp_lit_atabaki2010_ring_d20 | resonator.ring | 7 (Q_i ~60k author_estimate; R 10 um; 480 nm ring / bus; 220 nm; 1 um BOX; 1 um cladding) |
| yu2016a | cmp_lit_yu2016a_graphene_heater_rd5 | phase_shifter.thermo_optic | 9 (0.48 nm/mW; rise 12.8 / fall 8.8 us; 1.63 kOhm; simulated 1.06 nm/mW and 8.4 us; w_h 1.2 um; direct contact) |
| yu2016a | cmp_lit_yu2016a_graphene_heater_rd3_rout2p3 | phase_shifter.thermo_optic | 2 (1.13 nm/mW; w_h 0.5 um) |
| yu2016a | cmp_lit_yu2016a_graphene_heater_rd3_rout2p2 | phase_shifter.thermo_optic | 2 (~0.83 nm/mW Fig. 6; w_h 0.8 um label) |
| yu2016a | cmp_lit_yu2016a_graphene_heater_rd2 | phase_shifter.thermo_optic | 2 (1.67 nm/mW best; w_h 0.5 um label) |
| yu2016a | cmp_lit_yu2016a_microdisk_rd5 | resonator.disk | 8 (FSR 22.5 nm; Q ~4000; 5 nm tuning; notch ~16 dB Fig. 2(c); graphene loss 1.6 dB/cm simulated; r 5 um; 250 nm; 3 um BOX) |
| yu2016a | cmp_lit_yu2016a_metal_heater_rd5_sim | phase_shifter.thermo_optic (design) | 4 (0.86 nm/mW, 13.8 us rise / fall simulated; 1 um SiO2 gap) |
| lin2022c | cmp_lit_lin2022c_spiral_to_switch | switch_fabric.other | 6 (switching power 8.73 mW; rise 27 / fall 22 us; 4 / 4 us with optimized pulses; ER ~22 dB Fig. 5(d)) |
| lin2022c | cmp_lit_lin2022c_straight_to_switch | switch_fabric.other | 2 (21.5 mW; ER ~26 dB Fig. 5(e)) |
| lin2022c | cmp_lit_lin2022c_spiral_ps | phase_shifter.thermo_optic | 9 (P_pi 9.0 mW simulated; 235 / 387 ohm; IL ~1.2 dB; 10 um heater; 1 um gap; 450 x 220 nm; 2 um BOX) |
| lin2022c | cmp_lit_lin2022c_straight_ps | phase_shifter.thermo_optic | 4 (P_pi 22 mW simulated; ~870 ohm; 2 um heater; L 200 um Fig. 1(d) label) |
| lin2022c | cmp_lit_lin2022c_mmi_1x2 | splitter.mmi | 1 (< 0.5 dB) |
| lin2022c | cmp_lit_lin2022c_mmi_2x2 | splitter.mmi | 1 (< 0.5 dB) |
| song2016a | cmp_lit_song2016a_adiabatic_offset_638 | waveguide_platform.bend | 15 (Table II mean + std at R 3 / 4 / 5 / 7 / 10 um, 638 nm TE; 0.19 dB/90 simulated R 5; 450 / 220 nm, 2.0 / 2.3 um oxide) |
| song2016a | cmp_lit_song2016a_conventional_offset_638 | waveguide_platform.bend | 14 (Table II mean + std; geometry) |
| song2016a | cmp_lit_song2016a_adiabatic_638 | waveguide_platform.bend | 15 (Table II mean + std; 0.29 dB/90 simulated R 5; geometry) |
| song2016a | cmp_lit_song2016a_conventional_638 | waveguide_platform.bend | 15 (Table II mean + std; 0.39 dB/90 simulated R 5; geometry) |
| song2016a | cmp_lit_song2016a_sin_wg_638 | waveguide_platform.straight | 2 (~1.0 dB/cm at 638 nm, origin not stated; 220 nm) |
| song2016a | 4 x cmp_lit_song2016a_*_r20_1550 | waveguide_platform.bend (design) | 3 each (Table III 0.529 / 0.793 / 0.597 / 0.852 dB/90 simulated at 1550 nm, R 20 um; 1000 / 400 nm) |
| koos2007 | cmp_lit_koos2007_cob_r1p5 | waveguide_platform.bend | 9 (0.35 dB per 180-deg COB cutback, TM; < 0.1 dB over > 100 nm and < 0.2 dB over > 300 nm 3D FDTD; 0.6 % 2D; 0.8 um, 340 nm, 3 um BOX, R1 1.5 um, l_tpr 1.5 um) |
| koos2007 | cmp_lit_koos2007_disc_taper_r1p5 | waveguide_platform.bend (design) | 4 (1.6 % 2D; ~0.35 dB 3D; 0.8 um; l_tpr 1.5 um) |
| koos2007 | cmp_lit_koos2007_offset_circular_r1p5 | waveguide_platform.bend (design) | 3 (4.5 % 2D; 0.2-0.6 dB 3D over 1.3-1.7 um; 0.8 um) |
| koos2007 | cmp_lit_koos2007_corner_mirrors_r1p5 | waveguide_platform.bend (design) | 2 (9.8 % 2D; 0.8 um) |

Per paper (components / metrics): atabaki2010 6 / 34, yu2016a 6 / 27, lin2022c 6 / 23, song2016a 9 / 73, koos2007 4 / 18.

## Values not entered and why

atabaki2010
- Resonance tuning per mW: Fig. 4(a) shows ~1.6 nm shift for 1.45 mW on the printed axis (~1.1 nm/mW), while Fig. 5(a)
  gives ~2.32 K/mW (right axis ~34.6 GHz/mW, ~0.28 nm/mW) for the same 0.5 um heater; a ~4x conflict the paper does not
  explain (Fig. 5(a) is per mW after removing pad / connector dissipation, p.8). No row; component note.
- Fig. 5(a) temperature rise per mW (K/mW), 0.36 K/ohm, 34 ohm/mW resistance slope: no registry parameter.
- Relative results: SiN cladding +23 % bandwidth, SiO2-clad devices 35 % less power, ~20 % speed gain, trench design half
  the power (p.8-12).
- Model delay tau_delay 400 ns and the 725 ns impulse-response peak delay (Fig. 7(b)): no parameter (registry gap).
- Simulated curves of Fig. 2 (BOX thickness study, 0.5 um heater), Fig. 5 simulation lines and Fig. 9 (delay vs cladding
  diffusivity): parametric model studies, not entered.
- 75 ns reconfiguration of ref. [27] and the 700 nm BOX / 800 nm cladding thresholds for 0.08 dB/cm of ref. [28]: cited
  values (rule 3).
- Table 2 material parameters: model inputs.

yu2016a
- Graphene sheet resistance ~1.7 kOhm/sq and contact resistance ~800 ohm um from ribbon test structures (Fig. 3(a)),
  calculated R_circle / R_arm / R_contact: no parameter (registry gap; notes).
- Fig. 4(e) design with w_a = 4 um, L_a = 4 um reaching ~1.34 nm/mW and the Fig. 4 optimization maps: simulated
  parametric study, not a design row.
- Gold heater contacting the Si (Fig. 4(c), ~0.011 dB/um at r_out 4 um, w_h 1.2 um): simulated alternative, notes only.
- Si core ~392 K vs metal heater ~463 K at ~10 mW (p.5): no parameter.
- Q / FSR / extinction of the 3 um and 2 um disks: not printed. Q and ER change with heating power (p.3): not quantified.

lin2022c
- Table I (comparison with other works): rule 1 / 3.
- Extra power of the optimized pulses ~0.76 / ~0.44 / ~1.2 mW at 5 kHz (Eqs. 5-8): computed for an example frequency;
  note only.
- Switch IL "about 2 dB larger" than the straight switch: relative.
- Fig. 2(a)/(b) simulated waveguide temperatures vs power; spiral radii R1-R3 24 / 28 / 32 um, inner radius 10 um, 4 um
  waveguide gaps and heated lengths 150.72 / 175.84 / 200.96 um: radius_um / min_bend_radius_um are not allowed for
  phase_shifter (notes).
- Straight phase shifter stack thicknesses: the H values are printed for the spiral cross-section (Fig. 1(e)) only.

song2016a
- Table I (simulated transmissions of nine R = 5 um bend shapes a-i), Fig. 5 offset optimization and Fig. 6 k
  optimization curves: design exploration, not separate rows.
- Widest bend widths 700 / 650 / 650 / 570 / 493 nm and k values of the Fig. 8 caption: the caption k list
  (120 / 150 / 150 / 250 / 700 for R 3-10) contradicts the text (700 / 150 / 150 / 120 for R 3 / 5 / 7 / 10), and the
  caption offsets (50 / 45 nm at R 4 / 5) differ from the text (40 nm at R 5); geometry tied to k left in notes.
- Simulated TM transmission 80 % (adiabatic, R 5 um) vs 77 % (conventional): % transmission of a bend has no parameter;
  converting to dB/90 would be a derived simulated value; notes left out.
- Confinement factors 0.790 / 0.586, offset-loss difference < 0.03 dB/90: no parameter.
- Fig. 8 simulation curves: only the printed simulated values (p.2) entered.

koos2007
- Fig. 1(b) loss vs R1 curves for the four bend types (R1 0.5-2 um) and the Fig. 3 S-parameter spectra beyond the
  printed bounds: not read.
- COB mode conversion to TM1 below -20 dB (-30 dB), reflection and polarization conversion below -30 dB over > 300 nm
  (3D FDTD): crosstalk_db / back_reflection_db are not allowed for waveguide_platform (registry gap).
- Loss coefficient ~1 dB/mm used in the contour derivation: an input estimated from cited data [1].
- Corner-mirror 3D transmission: not printed (Fig. 3(a) only).
- COB shape parameters w_apex 1.2 um, w_ring 0.677 um, l_str 0.048 um; disc R2 1.695 um, w_ring 0.524 um; offset bend
  R2i 1.16 / R2o 1.84 um; corner a_CM 0.92 / b_CM 1.06 um: no registry parameters (labels / notes).

## Missing fab / facility orgs

None. Fab orgs used: org_georgia_institute_of_technology (atabaki2010, p.6 Sec. 3), org_zhejiang_university (yu2016a,
p.2 Sec. 2), org_southeast_university (lin2022c, p.1 Abstract). No paper names a shared facility, MPW service or
foundry. Wafer suppliers in notes only: Soitec (atabaki2010), SOITEC Smart-Cut (koos2007), unnamed commercial SOI
(yu2016a).

## Judgment calls (for the auditor)

1. atabaki2010 fab = Georgia Tech from "we fabricated 20 um diameter microring resonators" with a single printed
   affiliation (D72 / D80b).
2. atabaki2010 tuning efficiency withheld (Fig. 4(a) vs Fig. 5(a) conflict, above). An auditor with a better reading of
   the Fig. 4(a) axis (labels 1.5512 / 1.5516 / 1.552 / 1.5524 / 1.5527 are unevenly labelled) may resolve it.
3. atabaki2010 "rise-times as low as 725 ns can be achieved" entered as rise_time_us 0.725 `simulated` statistic best
   (prediction of the fitted model, not demonstrated); tau_diff 1.5 us as thermal_time_constant_us `derived` (model fit,
   D80a). The 0.5 um device keeps the printed "around 4 us" (measured) with the Fig. 5(b) reads (~4.27 / ~4.65 us) in
   notes; the 1 um device keeps 4.2 us (p.11) for rise and the Fig. 5(b) read for fall.
4. atabaki2010 trench variant entered as a `design` row (the sentence is followed by "Other simulations", the authors
   avoid trenches); Q_i ~60k `author_estimate` (D403), wavelength from the Fig. 4(a) axis (inferred).
5. yu2016a fab = Zhejiang University: first-person process description ("We use EBL and ICP"), all authors ZJU (S. He
   also KTH; D83c). The rd3 r_out 2.2 um device value (~0.83 nm/mW) is tied by the Fig. 6 inset label position and by
   elimination (the text ties 1.13 nm/mW to r_out 2.3 um); check against D156.
6. yu2016a heater_gap_um 0 for "contact the silicon core directly"; graphene-induced WGM loss 0.00016 dB/um entered as
   prop_loss_db_per_cm 1.6 `simulated` on the disk row (contribution only, C band inferred). Rise / fall times keep the
   printed "90% rising / decaying time" wording (reference level not given); Fig. 2(d) drive axis (~1.5 mW) vs text
   (~4 mW) noted.
7. lin2022c fab = Southeast University from "we designed and fabricated" (D595 / D647 precedents), although p.2 mentions
   "the design manual", which hints at an unnamed foundry flow. Switching power (P_pi) on the switch rows (zhu2018
   precedent, lit_254), simulated P_pi on the phase-shifter rows. MMI "< 0.5 dB ... according to our test" entered as
   `measured` excess loss with method unspecified (not author_estimate); spiral 1.2 dB IL `author_estimate` (isolation not
   described). Wavelength 1550 nm inferred on measured rows (only the simulation states it).
8. song2016a fab empty: passive "fabricated by PECVD", all authors imec, and "silicon nitride platforms provided by
   IMEC [6]" refers to index values (D80b, D433). One component per bend type with the radius in the condition
   (bogaerts2010 precedent), mean (n 4 dies) and std rows from Table II; platform loss ~1.0 dB/cm `author_estimate`
   (origin not stated). Method `reference_structure` (straight reference waveguide per test site, p.3).
9. koos2007 fab empty: "We fabricated" with authors at three unrelated universities (D154). 0.35 dB per 180-degree COB
   entered as insertion_loss_db per_component cutback (cherchi2013 precedent), not halved into bend_loss_db_per_90
   (abediasl2015 precedent); wavelength 1550 nm inferred (spectra 1480-1580 nm). 2D FDTD % losses converted to dB stay
   `simulated` (D83f); the three comparison bends are `design` rows.

## Registry gaps (skipped value + locator + proposed definition)

- `thermal_delay_us` (phase_shifter): heat-propagation delay from heater to waveguide as stated or fitted (atabaki2010
  tau_delay 400 ns, 725 ns impulse peak, p.10 Fig. 7).
- `temperature_rise_k_per_mw` (phase_shifter): waveguide temperature rise per mW of heater power (atabaki2010 Fig. 5(a)
  ~2.32 / ~2.3 / ~2.17 K/mW for 0.5 / 1 / 2 um heaters).
- `sheet_resistance_ohm_per_sq` and `contact_resistance_ohm_um` (phase_shifter): heater film sheet / contact resistance
  (yu2016a 1.7 kOhm/sq, 800 ohm um, p.4 Fig. 3(a)).
- `radius_um` or `min_bend_radius_um` on phase_shifter: folded / spiral heated waveguides (lin2022c inner radius 10 um,
  turns 24 / 28 / 32 um, p.2 Fig. 1(c)).
- `bend_offset_nm` (waveguide_platform): lateral offset at the straight-bend junction (song2016a 40-80 nm, p.2 / Fig. 8).
- crosstalk_db / back_reflection_db for waveguide_platform: mode conversion and reflection of bends (koos2007 COB
  < -20 dB TM1 conversion, < -30 dB reflection, p.2-3 Fig. 3(b)(c)).
