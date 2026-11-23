# lit_257 batch report

Papers: lit:su2022 (JLT 2022), lit:blascosolvas2024 (JLT 2024), lit:pruessner2007 (Optics Express 2007), lit:lin2024
(IEEE PTL 2024), lit:ahmad2002 (IEEE PTL 2002). Page-1 titles match the source rows; no garbled text layers;
institutional download stamps in su2022 / lin2024 / ahmad2002 ignored. verified_on 2026-11-23. Dry run: +22 components,
+147 metrics, 0 errors (the only warning is the pre-existing ni2025b duplicate, not in this batch). No existing rows
for these sources. Only values each paper reports for its own devices are entered; comparison tables of other works
(su2022 Table IV, blascosolvas2024 Table II except its own row) are not entered.

## Components / metric rows

| paper | component | class | metrics |
|---|---|---|---|
| ahmad2002 | cmp_lit_ahmad2002_corner_mirror | waveguide_platform.bend | 6 (best 1.4 dB per mirror TE; area range 1.49-2.96 um2; simulated optimum 1.85 um2; 0.4 um width, 0.34 um Si, 1 um BOX) |
| ahmad2002 | cmp_lit_ahmad2002_double_mirror | waveguide_platform.bend | 6 (best 1.0 dB TE; simulated < 0.088 dB from > 98 %; area range 0.69-2.66 um2; optimum ~1.5 um2 simulated; width, Si) |
| ahmad2002 | cmp_lit_ahmad2002_t_branch | splitter.other | 6 (excess ~1.5 dB measured, ~0.5 dB simulated; 2.4 um2; 1 in / 2 out; width) |
| ahmad2002 | cmp_lit_ahmad2002_t_branch_45deg_design | splitter.other (design) | 2 (0.86 dB simulated from T = 0.82; 3.16 um2) |
| ahmad2002 | cmp_lit_ahmad2002_access_taper | waveguide_platform.other | 4 (< 0.1 dB simulated; 10 um; 3.0 / 0.4 um ends) |
| su2022 | cmp_lit_su2022_ge_wpd_long_electrode | photodetector.ge_waveguide | 15 (0.79 A/W on-chip estimate; 120 nA; Vbr > 4 V; 3-dB 17.9 GHz heterodyne / 17.2 GHz FFT; C_J and R_S at 0 / -1 / -2 / -3 V; 40 um; 400 um2) |
| su2022 | cmp_lit_su2022_ge_wpd_short_electrode | photodetector.ge_waveguide | 15 (0.63 A/W fiber-referred; < 100 nA at -0.5 V, 1890 nA at -3 V; 3-dB 25.4 / 20.3 GHz; C_J, R_S x4; 40 um; 400 um2) |
| su2022 | cmp_lit_su2022_awg_4ch_oband | wdm.awg | 2 (IL > 10 dB, origin not stated; 4 channels) |
| lin2024 | cmp_lit_lin2024_switch_varsplit_spiral | switch_fabric.other | 11 (ER 47 cross / 45 bar best, > 38 dB 1520-1580 nm all paths, > 45 dB near 1560 nm; power 8.97 / 17.32 / 13.14 mW; IL ~13.8 dB f2f, ~2.3 dB on chip; 2 x 2) |
| lin2024 | cmp_lit_lin2024_switch_conventional | switch_fabric.other | 9 (ER 28 bar / 42 cross; power 1.59 / 25.27 / 13.43 mW; IL ~12.5 dB f2f, ~1 dB on chip; 2 x 2) |
| lin2024 | cmp_lit_lin2024_spiral_ps | phase_shifter.thermo_optic | 10 (P_pi 8.35 mW measured / 9.0 simulated; rise 15 / fall 16 us; ~0.25 dB excess per spiral; heater 10 um; 450 x 220 nm; 2 um BOX; 1 um cladding) |
| lin2024 | cmp_lit_lin2024_straight_ps | phase_shifter.thermo_optic | 4 (P_pi 23.68 mW measured / 22 simulated; heater 200 x 2 um) |
| lin2024 | cmp_lit_lin2024_mmi_2x2 | splitter.mmi | 1 (excess ~0.3 dB, PDK value) |
| lin2024 | cmp_lit_lin2024_spiral_bend_r10 | waveguide_platform.bend | 3 (< 0.0015 dB per 90 deg simulated; R 10 um; 450 nm) |
| pruessner2007 | cmp_lit_pruessner2007_fp_cavity_w6 | resonator.photonic_crystal | 9 (Q 4,584 / 2,626 / 4,417; F 82; FSR 28 nm; tuning 2 nm; L_C 12 um; W 6 um; t_Si ~4.7 um) |
| pruessner2007 | cmp_lit_pruessner2007_fp_cavity_w5 | resonator.photonic_crystal | 3 (Q ~4,600 at 1614.5 nm; L_C 12 um; W 5 um) |
| pruessner2007 | cmp_lit_pruessner2007_fp_to_switch | switch_fabric.other | 10 (25 dB at 40 mW; 10 dB at 8.4 / 17.7 mW; rise / fall 1.9 / 9.0 us probe 1, 7.3 / 3.5 us probe 2, 0.64 / 22.4 us overdriven; tau 3.2 us calculated) |
| pruessner2007 | cmp_lit_pruessner2007_lensed_fiber_facet | fiber_chip_coupler.edge | 1 (~5 dB per facet) |
| blascosolvas2024 | cmp_lit_blascosolvas2024_rib_wg | waveguide_platform.straight | 8 (3.6 dB/cm mean, 3-4.8 dB/cm chip range; 400 nm width / core, 150 nm slab, 250 nm etch, 3.2 um BOX, 1 um cladding) |
| blascosolvas2024 | cmp_lit_blascosolvas2024_bend_r60 | waveguide_platform.bend | 4 (0.2 dB per 90 deg mean; < 0.05 dB simulated; R 60 um; 400 nm) |
| blascosolvas2024 | cmp_lit_blascosolvas2024_gc_633 | fiber_chip_coupler.grating | 9 (11.7 dB per coupler derived; 31.5 % / 14.9 nm simulated; period 400 nm; FF 0.5; 14 deg; 10 um; 700 um taper; fiber MFD 3.6-5.3 um) |
| blascosolvas2024 | cmp_lit_blascosolvas2024_mmi_1x2_633 | splitter.mmi | 9 (excess 0.2 dB mean; imbalance 0.065 dB from P1/P2 1.015; 5 x 41 um; 2 um ports; 60 um tapers; 805 um2; 1 in / 2 out) |

Per paper: ahmad2002 5 / 24, su2022 3 / 32, lin2024 6 / 38, pruessner2007 4 / 23, blascosolvas2024 4 / 30.

## Values not entered and why

ahmad2002
- Reference-waveguide total insertion loss 11 +/- 0.25 dB (p.2): lensed fiber in, NA 0.8 objective out; no single component (coupling-dominated path).
- Mirror sidewall up to 14 deg from vertical "in some of the samples" (SEM, p.2): sample not named (D159), in notes.
- Corner-mirror facet length 1.2 um, double-mirror facets 0.6 um at 30 / 60 deg, mirror thickness tau ranges: no registry parameter (notes); simulated optimum tau 0.65 um in notes.
- Simulated corner-mirror optimum transmission (curve only, Fig. 2(a)) and TM values: not printed as numbers.
- Comparison "0.8- to 3-dB loss observed by other groups" (refs. [6], [7]): cited.

su2022
- Ge WPD cross-section (1 um Ge width, 0.45 um intrinsic height, ~400 nm Ge thickness, 220 nm Si, 2 um BOX, doping levels, 13.4 um electrode separation): the paper says the PDK gives no cross-section and the structure "is followed by the design shown in the previous work [29]" (another group's thesis): rule 3, notes. Ref. [29] simulated > 1 A/W, > 67 GHz, < 5 nA: cited.
- NEP < 0.11 / < 0.2 pW/Hz^0.5 (0.4-0.7 GHz, p.5, p.10): no registry parameter (gap below).
- 6-dB bandwidths 29.5 / 44.3 GHz (heterodyne) and 24.5 / 28.5 GHz (FFT): no registry parameter (gap below); in component notes.
- Impulse FWHM 23.14 / 19.92 ps and rise / fall 11.34 / 46.4 ps, 8.79 / 37.87 ps: no photodetector parameter; 0.35 / t_rise bandwidths 30.9 / 39.8 GHz (the paper equates them with the 6-dB bandwidth, not a 3-dB value): notes.
- Max photocurrent 0.54 mA at 13 dBm (Fig. 3(c)): not a saturation photocurrent as defined; notes.
- Equivalent-circuit R_J, C_box, R_sub, L_P, C_t, L_t, R_t, C_P (Table I): no parameters; Lt + Lp in notes.
- Data-rate / eye results (53 / 56 / 60 Gbit/s, SNR, jitter; Tables II, III): link-level, notes only.
- Commercial InGaAs reference PD (Finisar XPDV2320R: 36 / 43 GHz heterodyne, 35.6 / 43.8 GHz FFT, 8.31 ps rise) and the Thorlabs PDB460C NEP 6 pW/Hz^0.5: reference instruments of the setup (rule 13), not rows.
- 15 dB total (AWG IL + lensed-fiber coupling) used to calibrate the long-electrode responsivity: two components in one term, origin not stated; in notes.

lin2024
- Straight reference waveguide 11.5 dB fiber to fiber (Fig. 4(d)): coupler type never stated; used only as the subtracted reference (excludes on the de-embedded rows).
- MMI imbalance "less than 10%" per the PDK: percent definition not stated, not converted to dB (notes).
- Spiral inner radius 10 um, 4 um spiral gap, heated turn lengths 150.72 / 175.84 / 200.96 um: no phase-shifter parameter for spiral radius / turn spacing (gap_nm not used: it is a coupling-gap parameter); notes.
- Simulated bar-port ER vs imbalance (Fig. 1(c), 45 dB needs < 0.05 dB): model curve, notes on the MMI row.
- Phase-error compensation powers PM 1.59 / 3.28 mW: inside the power-consumption conditions.

pruessner2007
- Cavity resistance 125 kOhm and Delta T 23.5 K at 42 mW (p.4): no resonator / switch_fabric parameter (heater_resistance_ohm is phase_shifter only; gap below).
- DBR "R > 99 %" with "a few mirror periods" (p.2): general design claim, not measured; period count not printed; DBR period not computed from the printed ~390 / ~550 nm widths.
- "A typical Fabry-Perot cavity introduces an additional 5-6 dB" (ref. [11], authors' earlier paper) and 15 nm tuning of a Q ~700 cavity (ref. [12]): D259.
- Projected tau 800 / 130 ns for W_C 25 / 10 um: proposals, not devices.
- Tuning efficiency (pm/mW) and index change ~0.005: only readable off Fig. 3(b); not entered.

blascosolvas2024
- Confinement factor 90.5 % (abstract, Table II): no registry parameter (gap below).
- MMIs designed for 520 nm (L 49 um) and 480 nm (L 54 um): geometry only, simulated curves without printed values; not rows (rule 9).
- Simulated MMI insertion-loss curves (Fig. 4(d)-(f)): no printed values.
- Taper loss 0.5 dB (700 um x 3.6 dB/cm, "the highest losses this component will experience"): a computed subtraction term for two tapers; kept in the grating-coupler excludes, not a row.
- SiN uniformity 5 %: notes.

## Missing fab / facility orgs (name as printed + locator)

- "Nanjing Normal University" (School of Computer and Electronic Information / Jiangsu Key Laboratory on Opto-Electronic Technology), lit:lin2024 p.1 affiliation + p.1 abstract / p.4 Sec. IV "we designed and fabricated": fab role for all six lin2024 rows (left empty).
- "Naval Research Laboratory (NRL)", lit:pruessner2007 p.1 affiliation and p.7 Acknowledgments "The devices were fabricated in the Nanoscience Institute (NSI) cleanroom facility at NRL": fab role for all four pruessner2007 rows (left empty; same gap as pruessner2016).
- "Nanoscience Institute (NSI) cleanroom facility at NRL", lit:pruessner2007 p.7 Acknowledgments: facility role (left empty).

## Judgment calls

1. su2022 fab org_imec + process_name "IMEC PDK (Ge waveguide PD layout cell)": no "fabricated by" sentence; the paper calls imec "the manufacturer" (p.2, p.4) of a PDK cell. The AWG on the same chip keeps fab empty (the manufacturer sentences refer to the photodiode).
2. su2022 responsivities: long electrode 0.79 A/W `author_estimate` on_chip (15 dB calibration of unstated origin; the printed end points give a ~0.39 A/W two-point slope); short electrode 0.63 A/W `measured` fiber-referred (conclusion 0.64, abstract 0.63-0.74; conflict notes).
3. su2022 Table I C_J / R_S as `measured` (equivalent-circuit S11 fit, D80a; series_resistance definition lists the S11 fit); the paper also calls them the values "used for the numerical modeling".
4. su2022 cross-section geometry withheld as cited from ref. [29]; only the 40 um active length and the 40 x 10 um footprint (stated as "our design") entered.
5. ahmad2002 per-mirror bend losses (1.4 / 1.0 dB) `measured`, scope per_component, no division shown although the SEM'd structure has two mirrors in series.
6. ahmad2002 T-branch ~1.5 dB as `excess_loss_db` per_component; the two output corner mirrors are in the path and their removal is not stated; Fig. 3 points (~0.66 at 2.4 um2) read slightly worse than 1.5 dB.
7. ahmad2002 simulated transmissions converted to dB (> 98 % -> < 0.088 dB, 0.82 -> 0.86 dB) and kept `simulated` (D83f); the 45-deg T-branch entered as a design row.
8. ahmad2002 facility org_cornell_nanoscale_facility for "Cornell Nanofabrication Facilities ... for assistance with electron beam lithography" (D80c borderline, almeida2003 precedent); fab org_columbia_university from "we have designed and fabricated" with all authors at Columbia.
9. pruessner2007 tuning / attenuation / switching values assigned to the W 6 um device by matching resonances (1604.32 nm Q 4,584 and 1575.73 nm Q 2,626 in Fig. 1(b), Fig. 4); the text names only "our L_C = 12 um long cavity" (D159 judged not to apply). One device = resonator row + switch_fabric.other row (D396). Polarization TM from "E-field perpendicular to the substrate" for all measurements.
10. pruessner2007 Q 4,417 (Fig. 1(b) label) entered with the wavelength read off the axis (~1636 nm, inferred); FSR 28 nm from the figure label as `measured`.
11. pruessner2007 switching powers for 10 dB attenuation (8.4 / 17.7 mW) in `power_consumption_w` (no switch-power parameter other than p_pi_mw).
12. lin2024 MMI 0.3 dB and spiral excess 0.25 dB `author_estimate` (PDK value / PDK term subtracted); 0.3 dB stored as excess_loss_db (D43).
13. lin2024 P_pi 8.35 / 23.68 mW with C band inferred (probe wavelength of the Fig. 5 sweeps not printed); ER rows from Fig. 5 have band unspecified.
14. blascosolvas2024 grating 11.7 dB `derived` (own y-intercept minus own bend and propagation-based taper terms; the taper term assumes no adiabatic loss), scope per_coupler with the set-up loss included. Could be argued `author_estimate`.
15. blascosolvas2024 geometry `design_target` although SEM shows it "in line with the design" (no separate SEM values printed); the simulated < 0.05 dB bend value stated once for 480 / 520 / 633 nm entered once at 633 nm.

## Registry gaps (skipped value + locator + proposed definition)

- `nep_pw_per_rthz` (photodetector, pW/Hz^0.5): noise-equivalent power over the stated frequency band (band and bias in condition). su2022 long < 0.11, short < 0.2 pW/Hz^0.5, 0.4-0.7 GHz (p.5 Sec. III-B, p.10).
- `bw6db_ghz` (photodetector, GHz): 6-dB electrical bandwidth as stated. su2022 29.5 / 44.3 GHz heterodyne (p.7, Fig. 9(a)), 24.5 / 28.5 GHz FFT (p.8, Fig. 9(c)).
- `heater_resistance_ohm` widened to resonator / switch_fabric for self-heated devices: pruessner2007 cavity resistance 125 kOhm (p.4 Sec. 3.1).
- `confinement_factor_pct` (waveguide_platform, %): core confinement factor as stated (method in notes). blascosolvas2024 90.5 % at 633 nm TE (p.1 abstract, p.6 Table II).
