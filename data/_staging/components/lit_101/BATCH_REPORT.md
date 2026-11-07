# lit_101 batch report (2026-11-06)

All eight cached texts match their source rows (page-1 title); none is a correction, erratum or another paper. No garbled text layer flagged (dumais2016 prints the micro sign as "P", values unambiguous). arXiv texts: xie2022 (IEEE PJ), cabo2024 (Nanophotonics) and krumrein2026 (npj Nanophotonics) are arXiv v1 preprints whose titles match the journal records; journal versions unread (D430 / D433). stone2026 is an arXiv-only source row. Dry-run: +22 components, +138 metrics, 0 errors (the one warning, ni2025b m18 / m4, is an existing merged row).

| paper | components | metrics |
|---|---|---|
| stone2026 | 3 (resonator.ring: 2; frequency_converter.other: 1) | 11 |
| dumais2016 | 1 (splitter.mmi) | 15 |
| kandil2024 | 2 (splitter.mmi; splitter.hybrid_90) | 22 |
| xie2022 | 7 (switch_fabric.other: 2; splitter.mmi: 2, of which 1 design; polarization.other; reflector.bragg; fiber_chip_coupler.edge) | 30 |
| cabo2024 | 1 (mode_converter.converter) | 18 |
| li2021 | 2 (mode_converter.other; waveguide_platform.other) | 9 |
| krumrein2026 | 2 (reflector.phc_mirror) | 13 |
| sun2021 | 4 (reflector.bragg; waveguide_platform.straight: 2; fiber_chip_coupler.edge) | 20 |

## Not entered, and why

stone2026
- Intrinsic TE0 Q approaching 30 million at 1300 nm (p.1): device not named (D159), in notes.
- Simulated Q > 50 / 100 million and the Supp. 1550 nm values (60.74 / 123.21 / 173.03 million): rest on assumed roughness parameters.
- Gap-free signal tuning 894.5-895.9 nm, on-chip signal power about 10 mW / > 10 mW / > 5 mW: no tuning-range or output-power parameter on frequency_converter (registry gaps).
- Theoretical CE about 20 % from OPO theory (p.4): the measured on-chip ratio (10 mW / 50 mW) is entered instead.
- Heater calibration (Fig. 3(a)): slope not printed. Facet losses: not printed. Fig. 4 OPO states (795 nm pump, TM): no printed values. Ring radius of the fabricated devices: not stated (250 um is a simulation radius).

dumais2016
- Loss increase of the fully processed wafer, 0.03 +/- 0.02 dB: increment, no parameter (in notes).
- Number of die: not stated.

kandil2024
- Measured power imbalance < 0.5 dB (one die) and simulated imbalance about 0 / 0.01 dB: the paper defines imbalance as the deviation of each port's power from the mean, a split deviation (D401 / D454); in notes.
- 1x2 MMI splitter and the unbalanced MZI (dL 67.5 um, FSR 5 nm): test-circuit parts without own values.

xie2022
- 3-dB bandwidth of the high-ER MZI about 60 nm (p.6, Table 1): no bw_3db_nm on switch_fabric (registry gap).
- Maximum ER at other wavelengths (Fig. 5(d), about 56.6-61.2 dB): figure only, not read.
- ER gain from the TM filter > 10 dB: difference, no parameter.
- Simulated bend loss TM 4.8 dB / TE < 0.01 dB per 360 deg at R = 50 um; bend radius 50 um: no fitting parameter on polarization (min_bend_radius_um is a D439 candidate); in notes.
- MMI port separation d = 3.2 um: Fig. 1(a) does not fix pitch vs edge gap; not entered.
- Table 1 rows [5], [8]-[10], [19]-[23]: other works (rule 3).

cabo2024
- SWG period 200 nm, duty cycles 47 % / 65 %, W0 1.52 um, WF 2.6 um, S 1.8 um: no parameter on mode_converter (subwavelength_period_nm is not allowed there); in notes.
- 200 nm / 149 nm operational bandwidths: span definitions (IL and ER criteria) without a fitting bandwidth parameter; carried as the wavelength ranges of the IL / ER rows.
- Table 2 rows [15], [23]-[25], [37]-[42]: other works (rule 3). Mode multiplexer of the test circuit: authors' ref. [7].

li2021
- -20 dB bandwidth about 2.5 nm: no bw_20db parameter.
- EO tuning 0.182 nm/V and the 1545.8-1557 nm span: no tuning parameter on mode_converter (registry gap).
- SMW / TMW widths (6.0 / 11.6 um), gap 4.0 um, corrugation depth 1.2 um, electrode gap 15 um: no unambiguous role parameter (gap_nm not on mode_converter); in notes.
- Prism-coupler effective indices of trial waveguides (2.1409 / 2.1428 / 2.1393 at 1538.3 nm): trial structures, no parameter.

krumrein2026
- TWTF coupling > 90 %: cited (refs. 13-14, rule 3).
- V2 colour-centre metrics (saturation 103.8 / 124.3 kcps, PLE linewidths, ODMR, SSR fidelity): emitter properties, no component class.
- Simulated band structure gaps and the SEM-parameter simulation (62 THz): design / model values; in notes.
- Sidewall angle delta = 54 deg: angle convention (to plane vs. half-angle of the triangle) not fixed by the text; in core_material only.

sun2021
- Group delay 628 ps, dispersion -27.7 ps/nm, average group delay ripple +/- 17.23 ps (unapodized) and +/- 12.83 ps (apodized), simulated 660 ps / -28 ps/nm: no parameters (registry gaps). Hence no apodized row.
- 0.7 dB/cm derived by the paper from the grating's 3.8 dB round trip: same value as the plain spiral row; in notes.
- Min bend radius 40 um, waveguide gap 8 um, outer radius 272 um: no such parameters on reflector; in notes.
- Table I: other works (rule 3).

## Missing fab / facility orgs

- Maryland NanoCenter (xie2022 p.8 Ack.: its engineering team acknowledged for fabrication support): facility candidate, parent org_university_of_maryland_college_park; would go on the 7 xie2022 rows if the coordinator counts the acknowledgment as fabrication support rather than staff thanks.
- Plateforme de Micro-Nano-Technologie / C2N (cabo2024 p.7: work done within the C2N micro nanotechnologies platforms): facility candidate (already an org-round item, D430), parent org_centre_de_nanosciences_et_de_nanotechnologies; 1 cabo2024 row.
- Beacon Photonics (stone2026 p.1 affiliation, Arlington, VA): not entered as fab (helpers only, D395); not needed unless the coordinator rules otherwise.
- Used orgs all exist: org_astar_ime, org_cmc_microsystems, org_imec, org_university_of_maryland_college_park, org_uestc, org_applied_nanotools, org_university_of_stuttgart.

## Judgment calls

1. dumais2016: one row for both wafers (one physical design; passive-split vs fully processed wafer as conditions, rule 9). Loss in `excess_loss_db` (2x2, sum of both outputs vs reference; Fig. 2(a) caption "Excess loss"), method reference_structure, basis `derived` (N = 84 chain divided by N, rule 4). Statistic `wafer_map` with `le` for the all-die bound; 0.18 dB as `typical`. Fab IME A*STAR + CMC Microsystems (CMC acknowledged for "silicon photonics fabrication support", D398).
2. kandil2024: 3x3 120-degree hybrid as `splitter.mmi` (hybrid_90 is defined for 90-degree hybrids), 4x4 as `splitter.hybrid_90`. Wafer medians as `phase_error_deg` statistic median, n 52, method wafer_prober, wavelength = the 845-865 nm scan (inferred). The 4 dB circuit IL is on the 3x3 row as `de_embedded` with the 1x2 MMI and MZI waveguides in `includes`. Alternative for the 3x3: `splitter.other`.
3. xie2022: the tunable single-stage MMI-MZI is `switch_fabric.other` (D158; switching shown in Fig. 5(f)); its no-TM-filter sibling is a separate row (rule 9). 200 mW tuning power entered as `power_consumption_w` 0.2 derived (not P_pi: the sweep does not start at 0 mW). Fab UMD from the first-person overlay step plus all authors at one org (D399); alternative: empty (D80b).
4. xie2022 TM filter as `polarization.other` with the 25 dB TM suppression in `extinction_db` (`gt`, the paper says the stopband depth limits it). Test Bragg grating as its own `reflector.bragg` row: 20 dB TM-limited rejection (text) and about 48 dB with the filter read off Fig. 3(d) (`extracted_from_figure`, +/- 2 dB). Edge coupler 4 dB per facet `measured` (D167).
5. cabo2024: IL scope `per_component` with method reference_structure (MUX-exchanger-DEMUX normalized to the same circuit with a plain multimode waveguide). Body values entered over the abstract's "as low as 0.5 dB". The TE1 pass-through IL / ER are on the same row with `mode` TE1.
6. li2021: APE waveguides in bulk x-cut LiNbO3 treated as an integrated chip (in scope, platform `other`, suntsov2021 precedent). Filter as `mode_converter.other`; the cut-back losses of the grating-loaded TMW as a separate `waveguide_platform.other` row (D396). Pre-electrode (1550.1 nm) and 0 V post-electrode (1551.8 nm) 29 dB values are separate operating-point rows; the abstract's 1551.7 nm is noted (D417). Period 818 um stored as 818000 nm `derived` (D157).
7. sun2021: chirped SBGW as `reflector.bragg` (works in reflection, merged chirped-grating precedents). Its only allowed performance value is the 3.8 dB round-trip reflection difference as `insertion_loss_db` per_component (condition says what it is); alternative: `waveguide_platform.slow_light` with the derived 0.7 dB/cm. Spiral test waveguides as `waveguide_platform.straight` (the paper calls them bent; spiral radius not stated). Edge coupler 10 dB with scope `unspecified` (per facet vs both facets not stated).
8. stone2026: one ring as `resonator.ring` (Q values) plus `frequency_converter.other` (OPO), D396. Unqualified Q values as `q_loaded` with the coupling regime in the condition. The RW 3.5 um maximum (18 +/- 2) x 10^6 is `q_intrinsic` (p.1 calls the TE0 values intrinsic) but `author_estimate` (D403: Lorentzian fit, regime not shown to be fixed by the data). Threshold and CE `derived` (fiber powers de-embedded with the own measured facet loss and path calibration, D394).
9. krumrein2026: platform `other` (4H-SiC); fab org_university_of_stuttgart from the author contributions (M.K. fabricated; D395 / D439). Reflectivity values at THz-printed frequencies with wavelengths derived as c / f in the conditions; the 59 THz operating range converted to `stopband_width_nm` 177 nm `derived` (printed THz in notes). Untapered sibling: measured maximum about 50 % and simulated mean 63 % with `band` nir_below_o (edges not printed).

## Registry gaps (skipped value, locator, proposed definition)

- `group_delay_ps` on reflector (and waveguide_platform.slow_light): sun2021 628 ps over 1544.5-1567 nm (p.3, Fig. 6), simulated 660 ps (p.2). Total group delay across the stated band.
- `dispersion_ps_per_nm` on reflector / waveguide_platform: sun2021 -27.7 ps/nm measured, -28 ps/nm simulated (p.3, p.2). Linear group-delay slope, sign as printed.
- `group_delay_ripple_ps` on reflector: sun2021 +/- 17.23 ps (unapodized), +/- 12.83 ps (apodized) (p.4, Eq. (4)). Average ripple as defined by the paper (definition in condition).
- `min_bend_radius_um` on reflector and polarization: sun2021 R0 = 40 um (p.2); xie2022 TM filter R = 50 um (p.4). Already a candidate (D430, D439).
- `bw_3db_nm` on switch_fabric: xie2022 MZI about 60 nm (p.6, Table 1).
- `tuning_efficiency_pm_per_v` / `tuning_range_nm` on mode_converter: li2021 0.182 nm/V, 1545.8-1557 nm (p.6-7, Fig. 6(c)) (D419 widening of tuning_range not yet in the schema).
- `bw_20db_nm` (or a generic `bw_level_nm` with level in condition) on mode_converter: li2021 about 2.5 nm at -20 dB (p.2, p.3).
- `subwavelength_period_nm` widened to mode_converter: cabo2024 200 nm (p.3); `fill_factor` widened to mode_converter for SWG duty cycles (47 % / 65 %, p.4 Table 1).
- `tuning_range_nm` and an output-power parameter (`output_power_mw`) on frequency_converter: stone2026 894.5-895.9 nm gap-free tuning, about 10 mW on-chip signal (p.1, p.4-5). Candidates already raised (D419, D462).
- `split_deviation_db` (D401): kandil2024 per-port deviation < 0.5 dB (p.2 Fig. 2(c.2)).
