# lit_82 batch report (2026-11-04)

All five cached texts match their source rows (page-1 title); no correction, erratum or wrong paper. georgieva2022 is the arXiv version (source row carries the journal DOI; journal version unread). Dry-run: +28 components, +162 metrics, 0 errors (the one warning, ni2025b m18 / m4, is an existing merged row, not this batch).

| paper | components | metrics |
|---|---|---|
| barwicz2018 | 7 (fiber_chip_coupler.edge: 5 fabricated, 2 design) | 43 |
| georgieva2022 | 10 (fiber_chip_coupler.grating: 4 fabricated, 4 design; waveguide_platform.straight: 2) | 66 |
| lu2025 | 7 (fiber_chip_coupler.photonic_wire_bond: 5; micro_optics.facet_lens: 2) | 33 |
| sundaram2024 | 2 (polarization.pbs, polarization.psr) | 11 |
| peng2020a | 2 (fiber_chip_coupler.edge) | 9 |

## Not entered, and why

barwicz2018
- Fig. 6(b) four other converter lengths: the axis does not label them and the text names only 542 and 1084 um, so no sibling rows. Best TE point reads about 1.9 dB near 810 um including MT loss (p.6).
- MT connection loss, typically about 0.5 dB (p.5-6): generic for standard-grade connectors, no measured part; appears in `includes`.
- Monte Carlo residual misalignment, 3 sigma under 1.3 um and just under 1 um (p.2 Fig. 1, Table I): no parameter; tolerance inputs re-used from the authors' ref. [11].
- V-groove dimensions in Fig. 1(a) (145 / 125 / 75 um): a generic diagram, geometry only, no separate fiber_interface row.
- MFD 9-10 um (p.10): stated for full fiber modes in general, not tied to one design (D254); no row. Merged giewont2019 enters it from its own text.
- Mode-overlap penalty about 10 % by design (p.5), index asymmetry computation (Fig. 6(c)-(f)), band diagrams (Fig. 9(a)): no parameter, or illustrative.
- On-chip distributed reflection about -30 dB/mm (p.9-10): cited, ref. [38].

georgieva2022
- 2D and 1D GC 1-dB / 3-dB widths and peak values: Fig. 10 / 11 show exemplary dies only, no population statistic; the paper prints values at 1580 and 1530 nm only.
- Alignment penalties, imbalance, arm orthogonality, 5 nm/deg shift: no parameter on fiber_chip_coupler; in component notes.
- Sheet resistance of Metal3 55 mOhm (p.6): not a component metric.

lu2025
- 2.18 dB fiber-to-TFLN (p.4): assigned to the authors' ref. [31] (D259). 1.8 dB fiber-to-TFLN and 1.7 dB / 2.3 dB laser-to-SiN (p.4-5): by unnamed partners / users, no org, method or reference (rule 3 / D159); in TFLN notes only for the first.
- Table I (p.2): typical best-case comparison across solutions, family-level (D254), not tied to a device; PWB min pitch 10 um, MFD 2-12 um, FaML min pitch 30 um, MFD 2-40 um not entered.
- FaML on InP laser (p.6 Fig. 6): laser MFD 3 um sits in a sentence cited to the authors' ref. [26] (D259); < 0.5 dB fluctuation over 5000 h at 200 mW / 25 C and 100 mW / 75 C has no parameter. No row (no performance metric, rule 9). See registry gaps.
- FaML on InP in Gold Box (p.7): attributed to ref. [18]. Laser spectrum Fig. 3(c): no device metric. OAWM module 26 PWBs: ref. [33]. Offsets up to +/- 30 um and alignment up to +/- 15 um (p.3): generic capability statements.
- Fig. S1 / S2: supplement not cached.

sundaram2024
- 75 and 100 nm slot variants: no numbers. Difference in IL 0.06 dB (p.1): `imbalance_db` is splitter-only; in notes. Rotator tip widths, 2 um escalator, offset, gap: no parameter on polarization.

peng2020a
- Reliability drifts (< 0.3 dB, < 0.2 dB, p.3): no parameter, module design not named. Fig. 4(b),(d) spectra labelled per coupler: design of the module not named (D159). Coupler and V-groove geometry not printed. ORL value not printed.

## Missing fab / facility orgs

None. All used orgs exist in the registry (org_ibm_watson, org_globalfoundries, org_amf, org_aim_photonics, org_csem, org_fraunhofer_heinrich_hertz_institute, org_jeppix).

## Judgment calls

1. barwicz2018 -1.6 dB (p.5): the sentence names no length or polarization. Tied to the 542 um row because Fig. 5(a) is the only panel without MT loss and the text then doubles the length; Fig. 5(b) minus the typical 0.5 dB would also give about 1.5 dB. Alternative is D159 (delete, note only).
2. barwicz2018 Sec. V 1.3 dB is `author_estimate`: the 4 mm routing loss came from other wafer runs because the on-chip calibration site failed (p.7). Its roll-off and PDL stay `measured` (relative quantities).
3. barwicz2018 fab: IBM Watson (Sec. IV chips) and GlobalFoundries (Sec. V, VI chips) from explicit acknowledgment sentences (p.11). Assembly at IBM Bromont is not a fab org here.
4. barwicz2018 preliminary conference reports refs. [28], [31]: values kept (D408). Sec. V row taper length 800 um is an "expected optimal" value, entered as design_target approx.
5. barwicz2018 / peng2020a / giewont2019 describe one coupler family: separate rows per source and design generation, values not reconciled.
6. georgieva2022 fab empty: first-person process text, authors at TU Berlin and IHP, no org named as fabricator (D80b / D154). The platform is the one of refs. [22], [23]. p.8 describes 200 mm Si test wafers while p.9 says all structures sit at Metal2; noted.
7. georgieva2022 platform `other` for a-Si:H (chiles2017 precedent). Printed a-Si:H index differs across the paper (3.57 design, 3.6082 ellipsometry, 3.63 on p.11): noted, no parameter.
8. georgieva2022 cross-polarization entered in `crosstalk_db`; it is relative to input power, stated in condition. O-band "maximal" -4 dB at 1300 nm kept as printed; Fig. 6 peaks near 1305 nm (noted).
9. georgieva2022 c-Si rows: period, fill factor and etch depth entered from "the same couplers" (p.11), locators cite both pages. SOI rib 3 dB/cm row is `specification` with an inferred C band.
10. lu2025 PWB fab: the paper names chip foundries (AMF, AIM, HHI + JePPIX per D398, CSEM), and not who printed the PWB (Vanguard tool text only, D80b); taghavi2026 precedent. Fiber-to-fiber and FaML rows empty. Coordinator could add org_vanguard_automation if "our" results count as a statement.
11. lu2025 1.44 dB is `author_estimate` because the 0.2 dB fiber-array term subtracted is a manufacturer specification (rule 4); fiber-to-fiber 1.1 dB stays `measured` (no subtraction stated). Fiber-PWB-fiber stays in fiber_chip_coupler.photonic_wire_bond with scope fiber_to_fiber (rasel2026 precedent).
12. lu2025 590 h (text) vs 250 h (caption, table): table used, conflict noted. Fig. 7 printed table values `measured`, no reference given by the paper although ref. [26] has a matching title; if the coordinator reads Fig. 7 as reproduced from [26], D259 removes the row.
13. sundaram2024 printed splitter TM IL 0.42 / 1.68 dB appear referenced to the ideal 3 dB split (Fig. 1(b) shows about -3.5 / -4.5 dB), entered as printed with a note. Rotator IL prints "dBm", taken as dB. Text range 646-656 nm vs abstract 647-657 nm vs plot axis 648-656 nm: text value on the splitter, abstract on the rotator.
14. peng2020a -0.9 / -1.3 / -1.5 dB: statistic `typical` (histogram peak, D434 precedent), n = 100 per design (Fig. 3 caption); scope per_coupler with method unspecified because the text says fiber pairs without saying how one coupler was isolated (giewont2019 precedent). PDL 0.2 dB `derived`. Fig. 2 colorbar ends entered as `wafer_map` with a note; TM panel shares the scale, so no TM row.

## Registry gaps (skipped value, locator, proposed definition)

- `residual_misalignment_um` on fiber_interface / fiber_chip_coupler: 1.3 / 1 um 3 sigma (barwicz2018 p.2). Computed self-alignment residual, with the statistic in condition.
- `offset_compensation_um` on fiber_chip_coupler / chip_chip_coupler: lateral > 20, vertical up to 40 um (lu2025 p.5 Fig. 4(f)). Component offset with no loss penalty.
- `power_handling_dbm` widened to micro_optics: FaML on InP laser 200 mW for 5000 h at < 0.5 dB fluctuation (lu2025 p.6 Fig. 6).
- `il_drift_db` (or a reliability link) on fiber_chip_coupler: < 0.3 dB after 1000 h, < 0.2 dB after 500 cycles (peng2020a p.3); < 0.5 dB after 2000 h (lu2025 p.6). Stress in condition.
- `imbalance_db` widened to polarization: 0.06 dB (sundaram2024 p.1).
- `gap_nm`, `tip_width_nm`, `layer2_thickness_nm` widened to polarization: slot 50 nm, tips 300 to 150 nm, second layer 150 nm (sundaram2024 p.1-2; joins D439 candidates).
- `arm_orthogonality_deg` on fiber_chip_coupler: 95 / 96 / 89.6 / 92.7 / 91.8 deg (georgieva2022 p.4, p.6). Angle between the far-field polarizations of the two 2D GC arms.
- `hole_diameter_nm` widened to fiber_chip_coupler: 400 / 280 nm (georgieva2022 p.4, p.6; joins D431 candidate).
