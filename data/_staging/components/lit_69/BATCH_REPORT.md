# Batch lit_69 report (2026-11-02)

Totals: 76 components, 396 metric rows. Dry-run: `batch lit_69: +76 components, +396 metrics; errors 0`. No paper stopped: all seven cached texts are the source-row papers and none is a correction.

| paper | components | metric rows |
|---|---:|---:|
| romerogarcia2013 | 11 | 53 |
| giewont2019 | 7 | 29 |
| cherchi2013 | 10 | 46 |
| veiga2026 | 18 | 124 |
| thiel2026 | 16 | 56 |
| hiraki2017 | 4 | 27 |
| chen2022b | 10 | 61 |

## Per paper: values not entered and why

- **romerogarcia2013**: Fig. 6 R 75 / 100 um have no per-bend label (only R 35 printed, R 55 labelled). MMI imbalance below 10 % is (max - min) / mean: not `imbalance_db`. Simulated MMI efficiency and Table 2 stay in notes. Decay length, overlap, input-grating reflected power 8.4 %, angular tolerance, directionality and Table 1 tolerances have no parameter.
- **giewont2019**: all MZM values (EO-atlas candidate: 10 / 25 / 50 Gb/s MZMs, p.3). PSR: p.6 attributes the performance to ref. [16], and Fig. 12(c) goes with it, so no metric and no row (D259 / D408). Coupler -1.3 dB, 0.8 dB penalty, -16 dB and -35 dB reflections: assigned to refs. [13] / [11] (rule 3). LER / CD sigma Table I, FETs, TIA, test head and reliability plan out of scope. cWDM MUX has no own value (geometry only, no row).
- **cherchi2013**: abstract bound (radii below 10 um, below 0.02 dB per 90 deg) is not tied to one device (D159; note on the 16.8 um row). L-bend W 1 um, Reff 13.1 um (Fig. 5(b)) and W 2 um, Reff 7.5 um have no per-bend number: no row. TIR mirror ~0.3 dB and rib-strip converter << 0.1 dB recalled from earlier work. Matched Euler bends (Fig. 4) have no stated loss.
- **veiga2026**: LER, correlation length, H-bond contents, index tables have no parameter (notes where useful). Conclusion range 0.18-0.24 dB/cm (annealed, widths 700-900 nm) is a family statement: note on the annealed SiN2 row. Fig. 6 / 7 model maps and the 0.1-0.2 dB/cm target are predictions: not entered. Table V comparison rows from other works not entered. Error bars not transcribed.
- **thiel2026**: main text only; the supplement is not in the cached file. Waveguide 5000 %/W, 61 %, 50 mW are from ref. [14] (rule 3). Kilohertz / hertz laser linewidths have no number, so the self-injection-locked laser has no row. SOA / seed-laser chip, beam splitters and crossers have no value. RIN appears only as a modelling input and a 30 dB comparison.
- **hiraki2017**: ring loss 0.1 dB (computed by the authors from 2.7 dB) in notes. SiN:H reference spectrum has no number. Film composition Table 1 out of scope.
- **chen2022b**: delay ns/cm, ns/mm2, dB/ns, stop band width and grating period have no parameter on this class (notes / core_material). Fig. 3 / 9 spectra not read. Si waveguide 2.2-2.5 dB/cm and ng 4.2 are cited.

## Missing or unset orgs

- VTT Technical Research Centre of Finland, Espoo (cherchi2013 p.1; first-person fabrication statement, p.3 / p.8-9): not in `organizations.csv` / `org_aliases.csv`. Fab empty on 7 fabricated rows; proposed fab org once registered.
- UCSB Nanofabrication Facility: registered, used. Brightlight Photonics (thiel2026 p.7, MZI and facet polishing): note only.

## Judgment calls for the auditor

1. giewont2019 fab `org_globalfoundries` on all rows from foundry and manufacturing statements, no literal fabrication sentence (rule 12, v4 D80b). `sin_wg` kept as a roadmap item with `measured` (D167).
2. giewont2019 histogram peaks entered as `median` + `approx`: the mode is what is read, the enum has no mode.
3. giewont2019 text / figure conflicts: 350 nm better than 1.5 dB/cm vs Fig. 1 peak about 1.65; silicide gain above 1 dB/cm vs Fig. 2 about 0.5; dark current 35-70 nA vs Fig. 8 newPOR about 15-50 nA. Printed values kept, flagged in notes.
4. giewont2019 cWDM and heater platform empty (layer not stated, D422 / D423); coupler and PD `soi` from the Si / SOI text.
5. romerogarcia2013 free-space grating as `fiber_chip_coupler.grating` (radulaski2018 precedent). 38-44 % one `author_estimate` row. Width 1.2 um (Table 3) vs 1.5 um (method text) kept as tabulated. TSMC thanks not a fab statement.
6. romerogarcia2013 SiO2-to-water taper entered as a `waveguide_platform.transition` design row, though it is a cladding change on one layer.
7. cherchi2013 Rmin computed from Reff with the paper's ratios (`derived`); Reff kept in condition. U-bend per-180 values in `insertion_loss_db` (dostart2020 precedent). Group value 0.02-0.03 dB entered on each of the four named bends (not D254: stated for each). Rib 0.1 dB/cm and < 0.1 dB/90 kept as present-tense `measured` without a citation: check against D259.
8. veiga2026 18 rows from the material x cap x anneal x cure x width matrix. Printed bar labels `extracted_from_figure`; Payne-Lacey rows `simulated` on fabricated rows. Width mapping: nominal 700 -> Table III values, nominal 800 -> 700 nm caption. Table V 3.16 / 3.85 mapped to nominal 800 / 1100 from Fig. 11(b). Fab empty. Text says correlation length 78 nm, conclusion 60 nm (not entered).
9. thiel2026 fab `org_nexus_photonics` on lasers, detectors and MZI from the acknowledgment (development, fabrication, testing of the platform); the MZI part is a reading. UCSB facility set only on InGaP rows ("a portion of this work" is not tied to rows); InGaP fab left empty.
10. thiel2026 conflicts kept with both values: InGaP 8 dB/cm vs Fig. 1(b) about 1.6 dB/cm near 780 nm; MZI 10 vs 6 mdB; photoreceiver 510 MHz vs 3 GHz; ring 1.50 um text vs Fig. 2(c) x positions. 0.5 dB printed with 90 % transmission. SiN < 1 dB/m entered on both thickness rows; Fig. 1(b) 300 nm reads about 0.0107 dB/cm at 1560 nm.
11. thiel2026 single MZI as `switch_fabric.other` (D158); `p_pi_mw` 200 read from null spacing. `saturation_photocurrent_ma` 7 is highest tested, not saturation. PD classes as family rows (D165); QE ranges read from Fig. 4(e).
12. hiraki2017 `sion_wg` 0.29 dB/cm: single-layer vs multi-layer core not separated by the sentence. AWG IL band `wavelength_inferred`. Ring in `wdm.mrr` (filter in the WDM title, D400).
13. chen2022b `group_index` `derived` (from delay and length, chen2023 precedent) with `statistic` best; polarization TE from the design section and setup. Sample H and Si spiral loss `derived` from Table III (dB/ns x ns/cm), wavelength read from Fig. 10 with its printed shift. Sample E numbers disagree internally (see row note). Table II loss vs Fig. 4 band-edge readings disagree for D / E.

## Registry gaps (skipped value, locator, proposed definition)

- `effective_bend_radius_um` (cherchi2013 p.9; wang2026b precedent in notes): radius of the equivalent arc joining a variable-curvature bend's end points.
- `period_nm`, `fill_factor`, `stopband_width_nm`, `delay_ns_per_cm`, `delay_ns_per_mm2`, `loss_per_delay_db_per_ns` on `waveguide_platform.slow_light` (chen2022b Tables I-III): grating period; duty; stop band width; group delay per length / area; loss per unit delay.
- `imbalance_pct` on splitter (romerogarcia2013 p.8, p.11): port imbalance as (max - min) / mean, linear.
- `tol_3db_angular_deg` / `tol_angular_deg` (romerogarcia2013 p.5, p.9): angular misalignment at the stated excess loss.
- `grating_decay_length_um`, `directionality_pct` (romerogarcia2013 p.6, p.10).
- `polarization_peak_shift_nm` on wdm (hiraki2017 p.7, < 0.1 nm): TE-TM peak-wavelength difference.
- `pair_brightness`, `car`, `entanglement_fidelity_pct` on frequency_converter (thiel2026 p.3): nearly 1e8 pairs/s/GHz at 10 uW (Fig. 2(f) plots about 7e6), CAR above 1e4, 99.9 %.
- `phase_noise_mrad_rms` / `cmrr_db` on switch_fabric and photodetector (thiel2026 p.4, p.6): < 0.4 mrad, -62 dB bound; 50.4 dB.
- `transimpedance_ohm`, `input_noise_pa_rthz`, `shot_noise_clearance_db` (thiel2026 p.6): 5.9 kohm, 1.9 pA/rtHz, above 30 dB.
- `roughness_ler_nm`, `correlation_length_nm` (giewont2019 Table I; veiga2026 Table IV): already raised in D418 for RMS roughness.
- `bw_flat_top_nm` (giewont2019 p.6): 13 nm, level not stated, simulated.
