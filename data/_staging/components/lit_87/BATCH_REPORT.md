# lit_87 batch report (phase_shifter, waveguide_platform), 2026-11-06

All four cached texts match their source rows (page-1 title); no correction, erratum or wrong paper; no garbled text layer. dutta2025, harris2014 and miller2017 are arXiv texts (`arxiv_id` on the source row); journal versions unread (D430, D433). dutta2025 includes its supplement (p.40-42; locators `p.N Supp.` not needed: no value entered from it). Dry-run: +11 components, +55 metrics, 0 errors (the one warning is on merged row `cmp_lit_ni2025b_pimmwc-m18`, not this batch).

| paper | components | metrics |
|---|---|---|
| dutta2025 | 3 (phase_shifter.other x2: 1 um and 7 um electrode separation; resonator.ring) | 25 |
| harris2014 | 2 (phase_shifter.thermo_optic x2: doped-Si phase shifter, n-doped resistor of the thermal-crosstalk test structure) | 10 |
| fan2021 | 2 (waveguide_platform.straight, fiber_chip_coupler.edge) | 7 |
| miller2017 | 4 (resonator.ring, frequency_converter.other (OPO), waveguide_platform.straight, fiber_chip_coupler.edge) | 13 |

## Not entered, and why

dutta2025
- LC excess loss 0.08 / 0.34 dB/um (1 um, 0 / 7 V) and 0.02 / 0.18 dB/um (7 um): per-length phase-shifter loss has no parameter (D250); a total over 40 um would be an unprinted product. In component notes.
- Vpi*L 0.014 V cm: no parameter (candidate `vpi_l_v_cm`, D438).
- Fig. 4(a) intermediate separations (about 3 and 5 um): separations not printed, only plot positions; no rows.
- Q before / after LC and at 7 V: not printed. Extinction of the Fig. 4(b) notches: not printed.
- Simulated delta n_eff, 26 um length for 2 pi (Fig. 3), buffer-oxide study (Supp. Fig. 1): no parameter / design study, notes only.
- Table 1 and Table 2 (other works): cited. Grating couplers: no values.
- "Off" state stable for several hours (p.19): no number.

harris2014
- Table I other works: cited. MZI FSR 6.4 nm (test MZI, not the phase shifter), MMI Y-junctions [23] and grating couplers [24]: no values here / cited.
- Sheet resistances, doping levels, heat-channel width 800 nm and pitch 2.44 um, Ppi*tau product: no parameter (notes). Waveguide width not printed (1.0 um is the p-doped section, Fig. 1(b) "1x1.5 um2" unexplained).
- Thermal-crosstalk structure: power-law exponent 0.937 and Fig. 4 phase curves: no parameter / log-scale curves; separations 1-32 um in notes (population row, D165).
- Extinction: "deep extinction" with no number.

fan2021
- Supercontinuum span 842-1462 nm, octave fractions, dispersive-wave positions: no parameter.
- Calculated GVD, Table 1 beta2-beta4, gamma 6.61 /W/m: simulated, no parameter (D250).
- Air-clad results of the authors' 2019 paper (ref. 46): cited.

miller2017
- Intrinsic Q about 1e6 at 3.5-3.8 um (abstract, Fig. 3(b)): several devices with varying coupling gaps, not identified per device (D159); notes.
- Oxide-clad 500 x 1400 nm resonators (ref. [49] devices, Fig. 3(b) only) and the simulated oxide-clad loss: comparison, not entered.
- Measured total loss at 3.8 um: not printed. OPO sideband spacing (10 FSR), GVD (Fig. 5(a)): no parameter.
- Ring radius, coupling gap, taper length: not printed (scale bars only).

## Judgment calls

1. harris2014 fab `org_astar_ime`: "fabricated in the OpSIS process" (p.2) plus fabrication support from the IME team (p.5); same construction as merged ma2013 / simard2013 / sacher2014. OpSIS not in the registry.
2. harris2014 insertion loss 0.23 dB `author_estimate` + `loss_breakdown`: adjacent GCs are measured, but the subtracted MMI and waveguide terms are of unstated origin (D428 / D437 line). Wavelength inferred from the 1520-1570 nm sweep of the same structure.
3. harris2014 Table I tau 2.69 us entered as `rise_time_us` `author_estimate`: computed by the paper as 0.35 / f3dB (single-pole assumption), not a time-domain measurement. Vpi 4.36 V `derived` (sqrt(Ppi R), the paper's own conversion). Platform `soi_rib` (ridge with 90 nm slab).
4. harris2014 n-doped resistor: kept as a test-structure phase_shifter row with only its measured resistance (D165 population of six separations). Drop it if a resistance-only row is judged too thin.
5. dutta2025 Vpi 3.5 V `author_estimate` with a conflict note (D417): it is half of the 7 V used for about 2 pi; Fig. 4(c) shows about 1.05 pi at 5 V and 0.68 pi at 3 V.
6. dutta2025 phase shift: printed ~2 pi kept (`measured`, approx), the 0.8872 / 0.91 nm reading (1.95 pi) in notes. `retention_time_s` 4 s entered next to `fall_time_us` (the paper frames the relaxation as quasi-static memory). `endurance_cycles` 5 from the five averaged switching cycles (Fig. 4(b)), Fig. 5(a) 10 cycles in notes.
7. dutta2025 electrode-to-waveguide separation as `gap_nm` (derived from um), following the iseghem2022 LC and grottke2020 electrode-gap precedents, not `heater_gap_um` (no heater).
8. dutta2025 one ring row for all devices (FSR printed for "our devices", same ring design), cross-noted to both phase-shifter rows (D396).
9. dutta2025 and miller2017 fab empty: first-person process, authors at unrelated orgs, no named fabricator (D154).
10. fan2021 fab `org_national_sun_yat_sen_university` from the author contributions (D395, D439): three named fabricators have NSYSU as sole affiliation; H.-C.K. (National Chiao Tung University) and M.-H.S.'s second affiliation (Academia Sinica) are missing from the registry; "C.-R.L." matches no author and is not used.
11. fan2021 one waveguide row for both widths: the < 1 dB/cm sentence names no width (D159 / D165); widths as a design range row. The free-space objective-to-facet coupling is a `fiber_chip_coupler.edge` row (berman2026 / feng2022 precedents), 23.5 dB `author_estimate` (printed as an estimate, no method), the 5 deg misalignment > 0.2 % higher-order-mode coupling `simulated`.
12. miller2017 q_intrinsic 1.1e6 `author_estimate` (D403: under-coupling assumed). OPO threshold 5.2 mW `author_estimate` on a `frequency_converter.other` row (mckenna2022 / D252 precedent; the bus power is assumed equal to the measured output). Propagation-loss bounds from the Fig. 4 total-Q model and the 0.2 dB/cm scattering estimate `author_estimate` (model anchored on an unprinted measurement with an assumed lambda^-2 scaling). Inverse-taper 8 dB per facet `measured` (D167), band mid_ir inferred.

## Missing orgs (registry)

- OpSIS: harris2014 p.2 (process), p.5 acknowledgment; MPW access next to IME (D398 / D418 / D439). Would join `org_astar_ime` on the 2 harris2014 rows.
- National Chiao Tung University (Hsinchu; pre-merger name, D80d): fan2021 p.1 affiliation 5, p.9 author contributions (H.-C.K. device fabrication). Fab on the 2 fan2021 rows.
- Academia Sinica, Research Center for Applied Sciences: fan2021 p.1 affiliation 7 (second affiliation of fabricator M.-H.S.); not proposed as fab (dual affiliation, hiratani2024 / D433 line).
- Washington Nanofabrication Facility / Molecular Analysis Facility (University of Washington): dutta2025 p.28 acknowledgment (work conducted in part there). Facility on the 3 dutta2025 rows; already listed in D418 / D420.
- Supplier notes only: Rogue Valley (SiN wafer, dutta2025 p.25), Ultrasil Corporation (SOI wafer, miller2017 p.3).

## Registry gaps (skipped value, locator, proposed definition)

- `vpi_l_v_cm` (phase_shifter; candidate in D438): dutta2025 0.014 V cm (p.2, p.16). Voltage-length product for a pi shift.
- `loss_db_per_um` or `insertion_loss_db_per_um` (phase_shifter): dutta2025 0.08 / 0.34 dB/um (p.12-14), 0.02 / 0.18 dB/um (p.14). Excess propagation loss per unit length of the actuated section, actuation state in condition (D250 deferred this; another two values here).
- `nonlinear_coefficient_per_w_m` (waveguide_platform): fan2021 6.61 /W/m (p.8 Table 1, calculated). Effective Kerr nonlinear parameter gamma.
- `sc_span_nm` (waveguide_platform or frequency_converter): fan2021 842-1462 nm at -30 dB (p.1, p.4). Supercontinuum span with the level in condition.
- `thermal_crosstalk_exponent` not proposed (single value, harris2014 0.937, p.5).
