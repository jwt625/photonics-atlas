# lit_89 batch report

Distilled 2026-11-06. Classes: reflector, resonator, splitter. Dry-run: 0 errors (the one WARN is the merged row ni2025b, not this batch). All `uv` calls ran with `--offline`; figure crops came from `pdftoppm` / `magick` on the cached PDFs.

| Paper | Components | Metric rows | Content |
|---|---|---:|---|
| perezgalacho2017 | 4 | 29 | Si SWG double-periodicity Bragg pump-rejection filters (dW 5 nm at LF 500 / 1000 um; dW 10 / 15 nm at LF 500 um) |
| zhou2025a | 3 | 40 | Reconfigurable FP filter (4 Sagnac loop mirrors), stand-alone tunable MZI coupler, Sagnac loop mirror |
| puckett2021 | 2 | 26 | Si3N4 40 nm ultra-high-Q ring (DUT with SiN redeposition) and its control |
| hazan2021 | 2 | 11 | InP 2x2 MMIs, W_MMI 12 um, Wio 3 / 2.4 um |
| nevlacsil2019 | 4 | 26 | PECVD SiN MZI-type broadband DCs, 50/50 and 90/10, TE- and TM-like |
| Total | 15 | 132 | |

Page-1 title check: all five are their source rows. puckett2021 is the arXiv text, and its page-1 title adds "3.4 Billion Absorption Limited Q" to the journal title (same authors, arXiv id on the row; journal version not read; wu2018 / D430 precedent). perezgalacho2017 and nevlacsil2019 are arXiv texts with the journal titles. None is a correction.

## Per paper

### perezgalacho2017

Not entered:
- Fig. 3 calculated R, bandwidth, group index and coupling coefficient versus dW: these are for a 25 um 2.5D-FDTD design study that the paper calls qualitative. Fig. 4 curves: only the stated dW 5 nm / 1000 um point is entered (simulated).
- DUV variant (WC 170 nm, period about 400 nm, nBF about 1.94): a design without performance values.
- Back-reflection below 0.1 % at dW = 0: a simulated geometry that was not fabricated.
- LF 100 um (dW 5 nm) of Fig. 6: only a ripple-level dip, so no row. Fabricated designs that have no shown data (dW 10 / 15 nm at LF 100 / 1000 um): no rows.
- Reference waveguide (450 nm, 1000 um): no loss number. Grating couplers: no value.
- Corrugation width W = 150 nm, dW, and the 170 nm sub-wavelength period: no parameter on reflector, so they are in notes (registry gaps).

Judgment calls:
- `reflector.bragg` (baghban2017 band-rejection precedent), not `band_stop`.
- Headline extinction: 42 dB `measured` from the printed Fig. 6 arrow label. The text says "exceeding 40 dB" (in notes).
- 1.1 nm `stopband_width_nm` `measured`: the inset's dashed lines run from the two transmission maxima at the band edges, which matches the paper's null-to-null definition (Eq. 1). That level is in the condition.
- Fig. 5 extinction (+/-1 dB) and -10 dB widths (+/-0.15-0.2 nm) are `extracted_from_figure`. The dW 15 nm width is skipped because of a side dip.
- Wavelengths `wavelength_inferred` from the plot axes (stopband positions). The simulated rows use the stated design wavelength of 1550 nm.
- Fab empty: "we fabricated" is first-person, the authors are at C2N and Institut de Physique de Nice, and the site is not named (yasui2026 precedent). C2N is in the registry as org_centre_de_nanosciences_et_de_nanotechnologies if the coordinator assigns it.

### zhou2025a

Not entered:
- Sec. II simulated spectra (Fig. 5). Table I loss, group index and 0.5 dB MZI IL: simulation inputs, and the multimode-waveguide loss comes from the authors' ref. [31].
- Table II values of other works.
- -8 dB reflection-port leak in the fully transmissive state: no crosstalk parameter on resonator (notes).
- Second-order passband ripple below 0.3 dB: no parameter (gap).
- Configuration heater powers (13.4 / 28.2 / 29.8 mW) are in conditions only. The SLM full-reflection power of 14.7 mW is in notes because `tuning_power_mw` is not allowed on reflector.
- Variable-width MMI: no measured value of its own (only geometry), so it is not its own row. Its geometry is on the MZI coupler row.
- Loop length 125.62 um and connecting-waveguide lengths: given as simulation parameters, so they are in notes.

Judgment calls:
- FP filter `resonator.photonic_crystal` (wu2018 / D454). It is one physical device; the first, second and third order and the notch configurations are conditions (rule 9). The SLM is a separate `reflector.loop_mirror` row and the stand-alone MZI coupler a `splitter.other` row, cross-noted (D396).
- "Bandwidth" is printed without a level. It is stored as `bw_3db_ghz` with a "level not stated" note (davis2020 / dumon2004 precedents); the Fig. 9 traces are consistent with -3 dB by eye.
- MZI coupler `splitter.other`, not `switch_fabric.other` (D158). It is a tunable coupler that sets the SLM reflectivity. Bar / cross crosstalk is stored as `crosstalk_db` (splitter allows it). Coordinator question 2.
- Fab org_chongqing_united_microelectronics_center on the MZI coupler only, from "fabricated on a standard SOI wafer platform provided by CUMEC" (p.7; D455). The filter and SLM rows are left empty: the filter is "designed and fabricated" with no site named. Coordinator question 3.
- SLM reflectivity 0.04-100 % `author_estimate`: it is calculated from the measured K, and the printed end points match 4K(1 - K) with a lossless loop. The SLM -43 dB transmission suppression is stored as `extinction_db` `measured` (Fig. 8(b)).
- Wavelengths: Fig. 9 axes (about 1530.25 nm) and Fig. 8 (1529-1531 nm), inferred. The crosstalk at "around 1530 nm" counts as stated (D393).

### puckett2021

Not entered:
- Absorption-limited Q 3.4e9 and 51 kHz absorption-limited linewidth at 1600 nm (photothermal): no parameter (gap).
- Ring-down time 181 ns.
- Fig. 2(c)-(e) spectra and Fig. 3(c) splitting scatter (96 resonances, 3 devices).
- Fitted effective top roughness (0.24 / 0.35 nm) and scattering-model estimates (assumed roughness).
- Simulated critical bend radius about 6.8 mm.
- Weakly tapered coupler test-structure data (figure only, no number).
- SIMS hydrogen concentrations: material data.

Judgment calls:
- D403: the paper says the Lorentzian fit does not separate the intrinsic rate from the coupling rate. The split comes from a COMSOL coupling simulation fitted to the extracted rate, which agrees with a direct measurement on a coupling test structure (Fig. S3c). So `q_intrinsic` (422 M, ring-down 434 M, control 146 M), the 453 kHz intrinsic linewidth and the 0.060 dB/m loss are `author_estimate`. `q_loaded`, the loaded linewidth and FSR are `measured`; finesse 3005 is `derived` (FSR / loaded linewidth). Coordinator question 1.
- Fab org_honeywell: the acknowledgment thanks named Honeywell staff for "mask design and sample fabrication", and the Honeywell first author conceived the fabrication process. This is staff thanks rather than a site sentence (D448 relied on a stated place). Coordinator question 4.
- The mm / um design dimensions (11 um, 7 um, 11.787 mm, 6.898 um) are `derived` rescales (D157); thicknesses `design_target`.
- Control ring: a separate row (another wafer, different process), with the figure labels Q_L 63 M, Q_in 146 M and 3.03 MHz.

### hazan2021

Not entered:
- Imbalance on the Wio 2.4 um MMI: the text says imbalance does not grow with Wio (<0.1 dB), but the figure trace reaches about 0.16 dB near 1262 nm (D159; in notes).
- Other fabricated MMIs (W_MMI 10-13 um, Wio 2-3 um): no values.
- Earlier-work platform loss (about 2 dB/cm), SOA transparency current and gain bandwidth (rule 3).
- MMI length: not stated.

Judgment calls:
- The printed "insertion loss" is defined as light lost inside the MMI and is referenced to straight waveguides, so it is stored as `excess_loss_db` `per_component` `reference_structure`.
- `imbalance_db` < 0.1 dB kept on the Wio 3 um row. The paper defines imbalance as light deviating from 3-dB behaviour toward the other port: one value per coupler, not the per-port "3 +/- x dB" of D401. The figure peaks about 0.12 dB near 1268 nm (conflict note, D417). Coordinator question 5.
- The Wio 2.4 um measured worst-case about 2.0 dB at 1260 nm is `extracted_from_figure`. The BPM band-edge values (2 dB and 1 dB) are `simulated`.
- Fab empty: the "fabricated" statements are passive and the authors are at TU/e and Smart Photonics. org_smart_photonics exists if the coordinator reads the conclusion's "design, fabrication" as enough.

### nevlacsil2019

Not entered:
- L1 / L2 of the four fabricated designs: shown only as unlabelled dots in Fig. 3.
- The standard symmetric DC "power variation of 40 %" (3D FDTD): TE / TM identity is ambiguous (D159), and the device is a comparison design without its own data. It is in the coupling_variation condition only.
- CMT / FDTD curves of Figs. 3-6 (simulated design maps).
- The bend-radius statement ("no additional bending losses" at 150 um) has no number. 150 um is entered as the design bend radius.

Judgment calls:
- `splitter.directional_coupler`: an MZI-type asymmetric DC with passive phase section.
- The measured split ratios are read off the Fig. 5 markers as cross-port % ranges over 790-890 nm (+/-2 %); the text prints no measured number.
- The FDTD "about 10 %" straight-port window is entered as `coupling_variation` 0.1 `simulated` on both 50/50 rows. The statement covers the 50/50 MZI DC, and Fig. 6(a) shows TE and TM curves.
- Fab org_ams_ag from "fabricated by ams AG using their production line" (p.4).
- Nothing indicates the values are reprinted from the ECIO 2018 conference version (journal extension, D408).

## Missing organizations

None needed for this batch's entries. Candidates only if the coordinator assigns fab:
- C2N exists as org_centre_de_nanosciences_et_de_nanotechnologies (perezgalacho2017).
- Institut de Physique de Nice (Universite Cote d'Azur, CNRS; perezgalacho2017 p.1 affiliation): not checked as a fab candidate, since the fabrication site is not named.

## Registry gaps

| Proposed parameter | Definition | Skipped value | Locator |
|---|---|---|---|
| `corrugation_width_nm` (reflector) | lateral corrugation width / amplitude of a sidewall Bragg grating | W = 150 nm, dW = 5 / 10 / 15 nm | perezgalacho2017 p.3 |
| `subwavelength_period_nm` widened to reflector | sub-period of an SWG-engineered Bragg cell | 170 nm | perezgalacho2017 p.3 |
| `passband_ripple_db` (resonator, wdm) | peak-to-peak ripple inside the passband | below 0.3 dB (second order) | zhou2025a p.10 |
| `crosstalk_db` widened to resonator / reflector | leak to the unwanted port of a reconfigurable filter state | -8 dB (fully transmissive state) | zhou2025a p.8 Fig. 8(a) |
| `tuning_power_mw` widened to reflector | heater power for a stated reflectivity state | 14.7 mW (SLM full reflection) | zhou2025a p.8 |
| `q_absorption_limited` (resonator) | Q limited by absorption alone (photothermal) | 3.4e9 at 1600 nm; 51 kHz linewidth | puckett2021 p.8 Fig. 2(e) |
| `photon_lifetime_ns` (resonator) | ring-down (1/e) time | 181 ns | puckett2021 p.6 Fig. 2(b) |

## Coordinator questions

1. puckett2021 D403: the coupling regime comes from a simulation fit that a direct coupling test-structure measurement corroborates (p.16 Fig. S3c). Entered as `author_estimate`; `measured` is arguable if the test structure counts as determining the regime from data. Recommendation: keep `author_estimate`.
2. zhou2025a MZI coupler `splitter.other` versus `switch_fabric.other` (D158). Recommendation: keep `splitter.other`, since its function is a tunable coupler inside a loop mirror.
3. zhou2025a fab: should CUMEC extend to the FP filter and SLM rows? The platform sentence sits in the stand-alone coupler subsection only. Recommendation: keep empty (D80b strictness).
4. puckett2021 fab org_honeywell from staff thanks for sample fabrication plus the author contribution. Recommendation: keep; drop if staff thanks without a stated place do not qualify.
5. hazan2021 `imbalance_db` < 0.1: not a D401 split deviation by the paper's definition. Recommendation: keep, with the figure conflict noted.
