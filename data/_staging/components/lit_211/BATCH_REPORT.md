# Batch lit_211 report

Distilled 2026-11-18 (verified_on 2026-11-18). Four papers. Dry run: `merge_component_staging.py data/_staging/components/lit_211 --dry-run` -> +15 components, +98 metrics, 0 errors (one WARN concerns an already merged row of another paper, cmp_lit_ni2025b_pimmwc).

All four cached texts match their source rows (page-1 titles); text layers clean; figures and tables read from the page renders. No paper is a correction or another paper.

## lit:liu2017 (IEEE PTL 29(22), 2017, 4 pages)

Components / metric rows: 1 / 14

| component | class | metrics |
|---|---|---|
| cmp_lit_liu2017_swg_mmi_diplexer | wdm.other (row_kind design) | 14: simulated IL 0.09 dB (1310, bar) / 0.08 dB (1550, cross), ER 22.18 / 20.10 dB, 1-dB bandwidth about 150 nm (bar, around 1310) / about 120 nm (cross, around 1550); MMI length 43.4 um, MMI width 2 um, waveguide width 450 nm, taper width 0.9 um, taper length 5 um, Si 220 nm, 1 input / 2 outputs |

Design-only paper (3D FEM Bloch-mode + 3D FDTD); no fabrication or measurement. Class wdm.other and extinction_db follow the zhang2022b TMI diplexer precedent. No fab / facility.

Values not entered and why:
- SWG period 180 nm (p.2): `subwavelength_period_nm` is not allowed for class wdm (registry gap, below). In component notes.
- SWG groove a = 60 nm and SWG width ws = 60 nm (p.3): no registry parameter. In notes.
- Fabrication tolerances (Figs. 7-8: IL < 1 dB / ER > 6.8, 8.0, 10.8 dB windows for groove, width, MMI width and length variations): tolerance parameters rejected (D81 / D250).
- Conventional MMI counterpart (146 um, beat lengths 36.5 / 29.5 um, simulated comparison) and the SWG-MMI beat lengths 21.7 / 14.5 um: no performance row / no parameter.
- Preliminary results in the authors' conference paper ref. [19]: this letter is the extended version; values kept (D408).

Missing fab / facility orgs: none (no fabrication).

## lit:shokraneh2020 (JLT 38(6), 2020, 10 pages)

Components / metric rows: 4 / 22

| component | class | metrics |
|---|---|---|
| cmp_lit_shokraneh2020_mzi_2x2_test | switch_fabric.other | 6: ER about 43 dB (worst case, input I2), ER 45 dB (input I1, Fig. 7(b) label), IL about 1.5 dB (scope unspecified, normalization reference not stated), switching power about 21 mW (p_pi_mw, derived by the authors from the 170 ohm resistance), 2 x 2 ports |
| cmp_lit_shokraneh2020_doped_si_heater | phase_shifter.thermo_optic | 8: resistance about 170 ohm, simulated Vpi 1.92 V, thermal stabilization < 30 us (rise_time_us, definition note), 27 um per resistor (x5), rib 420 nm x 220 nm, 90 nm slab, 130 nm etch (figure label) |
| cmp_lit_shokraneh2020_dc_3db | splitter.directional_coupler | 3: simulated split 50 % at 1310 nm, coupling length 9.13 um, gap 200 nm (derived from 0.2 um) |
| cmp_lit_shokraneh2020_mzi_mesh_4x4 | switch_fabric.mzi_mesh | 5: crosstalk > 35 dB between output ports, path I4-O4 IL about 3 dB (unspecified scope), total configuration power about 0.507 W (derived from 507 mW), 4 x 4 ports |

Fab: org_astar_ime + org_cmc_microsystems on all four rows ("fabricated using 193 nm DUV lithography at the Institute of Microelectronics (A*STAR IME) through a multi-project wafer (MPW) service managed by Canadian Microelectronic Corporation (CMC)", p.5; acknowledgment p.10). process_name "193 nm DUV lithography, A*STAR IME multi-project wafer service managed by CMC". Platform soi_rib (220 x 420 nm ridge, 90 nm slab). No facility statement.

Values not entered and why:
- Path ILs of Fig. 11 for I4-O3, I4-O2, I4-O1: the text sentence that should give them ends without numbers ("are in good agreement with ..."), and the noisy spectra give no single reading point. Not read off.
- Table I cross / bar bias voltages (VC.S. 2.25-3.02 V, VB.S. 3.0-3.7 V; test structure 2.7 / 3.45 V) and Table II programming voltages: no registry parameter (bias states, not Vpi). In notes.
- Grating couplers (vertical GC input, p.6): no value.
- dn/dT 1.94e-4 /K: material constant.
- Simulated 2 pi / 3 pi / 4 pi voltages 2.73 / 3.38 / 4 V: in the Vpi row notes.

Missing fab / facility orgs: none (org_astar_ime, org_cmc_microsystems exist).

## lit:guo2017a (JLT 36(2), 2018, 8 pages; DOI year 2017)

Components / metric rows: 4 / 27

| component | class | metrics |
|---|---|---|
| cmp_lit_guo2017a_benes_16x16 | switch_fabric.mzi_mesh | 7: IL about 16.2 dB mean of 16 paths (de_embedded with a reference waveguide, includes 5.6 dB taps, measured), IL about 10.6 dB (taps also excluded, author_estimate), crosstalk about 20.5 dB (worst path I1-O7), average EO switching power 0.34 mW (p_pi_mw, mean of 15 SEs, Table I), 16 x 16 ports, chip footprint 12.1 x 4.6 mm (derived) |
| cmp_lit_guo2017a_dr_mzi_se | switch_fabric.other | 8: on-off ER about 30 dB (after TO alignment), crosstalk > 27 dB upon EO switching, EO switching power 0.28 mW (p_pi_mw), rise 450 ps / fall 1.65 ns (us, derived), per-SE IL about 1.5 dB (author_estimate, 10.6 dB / 7), 2 x 2 ports |
| cmp_lit_guo2017a_racetrack_mrr | resonator.ring | 11: TO power 6.7 mW for about 0.82 nm shift, tuning efficiency 122 pm/mW (derived from printed 8.2 mW/nm), TO alignment power 3.8-37.5 mW per ring heater (Table I, 36 heaters), R 10 um, coupling length 4.2 um, gap 200 nm, width 500 nm, Si 220 nm, etch 160 nm, BOX 2 um, TiN 120 nm |
| cmp_lit_guo2017a_gc_uniform | fiber_chip_coupler.grating | 1: about 6.4 dB per coupler at 1550 nm after fiber-array attach (D167 measured) |

Fab: org_astar_ime on all rows ("The fabrication of the 16 x 16 switch chip was carried out using CMOS compatible processes in IME Singapore", p.4 Sec. III). process_name "CMOS compatible processes in IME Singapore, 248-nm DUV photolithography". Packaging by the authors ("home-packaged"), no separate org. No facility statement; acknowledgments are grants only. Platform soi_rib (160 nm etch rib) except the GC (soi; grating etch not stated).

Values not entered and why:
- 3-dB optical bandwidth about 0.45 nm (SE, p.5) and about 0.33 nm (narrowest path I1-O8, p.6): `bw_3db_nm` is not allowed for switch_fabric; nm -> GHz conversion would need a wavelength-dependent formula (not done). Registry gap.
- Group delay about 45 ps (all paths) and maximum GDD 300 ps/nm (all-cross path), p.6: no parameter (dispersion rejected, D81 / D250).
- About 1.1 dB cross-path dip at the 1558.98 nm resonance (p.5) and the 7.9 dB accumulated dip of the all-cross path (p.5): resonance dips, not ILs.
- +/- 1.7 dB IL variation: kept in the condition of the IL rows (kind of spread not stated; not converted to il_nonuniformity_db).
- 5.6 dB tap loss and 1:10 tap design ratio: loss-budget term of unstated origin; used only in notes of the author_estimate rows.
- Ring model values a = 0.9905, t = 0.86 ("assumed ... to match", p.4) and Fig. 2 model values t = 0.9, a = 0.998: assumed model inputs.
- EVM values (system level); 90-deg crossed MMIs (design ref. [27], no value); 2 um connection waveguides (no loss value).
- Earlier 2 x 2 and 4 x 4 DR-MZI switches [28], [29]: not used (all entered values are this chip's measurements).

Missing fab / facility orgs: none (org_astar_ime exists; printed "IME Singapore", p.4).

## lit:suzuki2018 (JLT 37(1), 2019, 7 pages; DOI year 2018)

Components / metric rows: 6 / 35

| component | class | metrics |
|---|---|---|
| cmp_lit_suzuki2018_piloss_32x32 | switch_fabric.mzi_mesh | 14: fiber-to-fiber IL 10.8 dB mean, 8.9-12.8 dB range, 0.54 dB std (1024 paths, 1547 nm, with PLC connectors), on-chip IL 6.1 dB (min path, author_estimate), crosstalk 26.6 dB best (worst-case state), -20 dB crosstalk bandwidth 3.5 nm, trimming power total 1.3 W, full-operation power 1.9 W (derived), 32 x 32 ports, chip 10 x 26 mm (derived), Si 225 nm, BOX 3 um, over-cladding 1.5 um |
| cmp_lit_suzuki2018_piloss_32x32_pe | switch_fabric.mzi_mesh | 4: -20 dB crosstalk bandwidth 14.2 nm, crosstalk 26.6 dB best, 32 x 32 ports |
| cmp_lit_suzuki2018_tin_heater | phase_shifter.thermo_optic | 9: switching power 18.1 mW mean / 0.78 mW std (p_pi_mw), trimming power 1.3 mW mean / 1.52 mW std (tuning_power_mw), resistance 395 ohm mean / 11.2 ohm std, response about 30 kHz (bw3db_khz, author_estimate), heater 5 um x 70 um |
| cmp_lit_suzuki2018_adiabatic_intersection | crossing.other | 1: 0.024 dB per intersection (author_estimate, estimate input) |
| cmp_lit_suzuki2018_si_waveguide | waveguide_platform.straight | 3: 1.2 dB/cm (author_estimate, origin not stated), Table I routing-waveguide terms 0.70 / 0.63 dB (author_estimate) |
| cmp_lit_suzuki2018_edge_coupler | fiber_chip_coupler.edge | 4: design MFD about 3 um of the PLC waveguide (mfd_fiber_um, author_estimate), tip 175 nm, start width 430 nm, pitch 50 um |

Fab: org_national_institute_of_advanced_industrial_science_and_technology on all rows: "We fabricate ... by using our complementary metal-oxide-semiconductor pilot line equipped with an immersion ArF scanner" (p.1 abstract, p.2 Sec. II) plus the footnote "The device fabrication was supported by TIA Super Clean-Room of the National Institute of Advanced Industrial Science and Technology" (p.1). See judgment call (a). process_name "300-mm SOI, CMOS pilot line with immersion ArF scanner". Platform soi (waveguide type not stated).

Values not entered and why:
- PLC connector coupling loss 1.4 dB/facet (Table I, p.4): stated as an assumption ("we assumed the minimum coupling loss of the current PLC connector to be 1.4 dB/facet") tied to the authors' connector paper ref. [10] (1.4-1.6 dB/facet, p.1): rule 3. No PLC connector row (no value of its own measured here); extremely-high-Delta 5.5 % from ref. [10].
- Leakage to non-target ports below -30 dB (p.3): absolute fiber-to-fiber transmission, not a crosstalk ratio.
- Table I MZ-switch sum 4.0 dB and intersections 0.74 dB for the minimum-loss path: path sums; no per-element value printed for the MZ switches (not divided by an assumed count). Intersections entered via the printed 0.024 dB/intersection.
- 0.4 dB loss difference between longest and shortest routes, propagation length > 2.6 cm and >= 3.1 dB on-chip propagation loss, 1.8 dB / 0.8 dB / 6.3 dB / about 6 dB improvement projections, +0.77 dB for the port-exchanged switch, < 1 dB double-MZ estimate: estimates or projections.
- Previous-work values (28.4 dB, 14.5 / 13.9 dB, 8.7 W, 6.9 W, 1.8 W, 54.4 mW, 8.73 mW) from ref. [8]: rule 3.
- Electrode pad pitch 180 um, LGA 2112 pins at 0.5 mm, 127 -> 50 um PLC pitch conversion: packaging geometry with no matching parameter on a row.

Missing fab / facility orgs:
- "TIA Super Clean-Room of the National Institute of Advanced Industrial Science and Technology" (facility, p.1 footnote): not in organizations.csv / org_aliases.csv (same gap as konoike2020 / konoike2022 / ikeda2020 / suzuki2020, D453); facility_org_ids left empty on all suzuki2018 rows.
- Furukawa Electric Co., Ltd. (one author affiliation, p.1): not a fab or facility statement; affiliation only (header batches).

## Judgment calls

- (a) suzuki2018 fab = AIST. The abstract's first-person "We fabricate ... using our CMOS pilot line" names the authors' own process (D84a), and the footnote names AIST's TIA Super Clean-Room as where device fabrication was supported (D448). Borderline: one of eight authors is at Furukawa Electric, so "our" is not strictly one org; suzuki2020 (passive voice) kept fab empty. Flagged in component notes; the coordinator may empty it.
- (b) guo2017a 2 x 2 DR-MZI = `switch_fabric.other` (D158): the paper characterizes "the as-fabricated 2 x 2 DR-MZI" and a "stand-alone SE" without saying whether they sit inside the 16 x 16 fabric.
- (c) EO tuning powers of the DR-MZI (0.28 mW single SE, 0.34 mW fabric average) entered as `p_pi_mw`: the paper states the EO tuning sets the pi phase difference between the MZI arms (p.2); campenhout2009 precedent for EO p_pi on switch rows. Alternative would be `power_consumption_w`.
- (d) guo2017a 10.6 dB (abstract value) and 1.5 dB per SE are `author_estimate`: both subtract the 5.6 dB tap loss, whose origin is not stated. The measured 16.2 dB average (reference-waveguide normalized) is the measured row.
- (e) suzuki2018 on-chip 6.1 dB entered as `author_estimate` (rule 4, assumed coupling input) rather than dropped under rule 3: it is this paper's own measurement minus an assumed per-facet value, not a cited result.
- (f) shokraneh2020 "approximately 21 mW switching power" on the 2 x 2 row as `p_pi_mw` `derived` (authors computed it from the measured 170 ohm resistance; voltage not printed). Placed on the switch row (patel2014 precedent, same group's heater design).
- (g) shokraneh2020 "thermal stabilization time ... less than 30 us" as `rise_time_us` lt 30 with the definition note (suzuki2020 precedent for a switching time of unstated definition); suzuki2018 "response speed of the heater is ~30 kHz" as `bw3db_khz` about 30 `author_estimate` with the criterion note.
- (h) shokraneh2020 3-dB DC kept as a fabricated row with only a simulated 50 % split (D80e, D82a) plus its design geometry.
- (i) suzuki2018 heater trimming power stored as `tuning_power_mw` (konoike2022 precedent) and cross-to-bar switching power as `p_pi_mw` on the heater row; the switch matrix row carries the chip totals in `power_consumption_w`.
- (j) suzuki2018 1.3 W total trimming power `derived` (sum of the measured per-element powers), 1.9 W `derived` (paper calls it an estimate from the measured distributions).

## Registry gaps

- `subwavelength_period_nm` for class wdm: liu2017 SWG period 180 nm in the MMI section of the diplexer (p.2 Sec. II). Proposed: allow the existing parameter for wdm (definition unchanged).
- `bw_3db_nm` for class switch_fabric: guo2017a 3-dB optical passband about 0.45 nm (single DR-MZI upon EO switching, p.5 Sec. IV-A) and about 0.33 nm (narrowest path I1-O8 of the 16 x 16 switch, p.6 Sec. IV-B; also p.1, p.7). Proposed: allow `bw_3db_nm` for switch_fabric, "3-dB optical passband of a resonant / wavelength-selective switch path" (bw_3db_ghz is already allowed).
- SWG groove length and SWG width (liu2017, 60 nm / 60 nm, p.3): no parameter; low priority (single design-only row).
