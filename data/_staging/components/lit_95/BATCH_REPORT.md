# lit_95 batch report (2026-11-06)

Both cached texts are arXiv preprints of their source rows (page-1 title and authors); neither is a correction, erratum or another paper. Dry-run: +21 components, +51 metrics, 0 errors (the one warning, ni2025b m18 / m4, is an existing merged row, not this batch).

| paper | components | metrics |
|---|---|---|
| qu2024 | 16 (amplifier.parametric: 11 = GO-0, GO-1 / GO-2 at 1.4 mm, 8 GO-length siblings; waveguide_platform.straight: 4; fiber_chip_coupler.edge: 1) | 34 |
| kittlaus2018 | 5 (mode_converter.converter: 3 width-asymmetry devices; waveguide_platform.straight: 1; fiber_chip_coupler.grating: 1) | 17 |

## Preprint vs journal record (D430 / D433)

- qu2024: arXiv v1 (2024-01-14), same title as the source row (Light: Advanced Manufacturing, doi 10.37188/lam.2023.039). Journal version not read; values from the preprint.
- kittlaus2018: arXiv v1 dated 2018-08-30, title printed "Nonreciprocal Inter-band Brillouin Modulation" vs registry "Non-reciprocal interband Brillouin modulation" (Nature Photonics); same authors and work. Journal version not read. The text includes the Supplementary Information (pp.9-34). `garbled_text_layer` page 23 holds only equations (Supp. Sec. II); no value taken from it. Figure values were checked on the page renders (pp.2, 5, 17).

## Not entered, and why

qu2024
- Nonlinear parameter gamma (~1.11 /W/m uncoated; 14.5x and 27.3x for GO-1 / GO-2), GO and Si3N4 n2, GO mode overlap 0.07 / 0.15 %, dispersion (Fig. 1(f)): no registry parameter (gamma is a registry gap, below).
- Gain improvement dPG (max ~12.2 dB, GO-2) and the Fig. 4(c) / Fig. 5(a), (b) operating-point curves: improvement has no parameter; the curves are operating points of the entered devices (only the printed 180 W / -22 nm points entered).
- Saturable-absorption excess loss vs peak power (Fig. 2(d), figure only): no parameter.
- "No significant variation in insertion loss below 30 mW" (p.12): Fig. 2(b) plots CW power only up to ~21 mW, so the 30 mW bound is not supported by the shown data; not entered as `power_handling_dbm`.
- Simulated optima at other GO lengths (26.3 / 27.0 dB at L_GO ~7 / ~3.3 mm, Fig. 8(b)), both-optimized and 400 W cases (37.4-43.8 dB, Supp. Figs. S4 / S5, supplement not cached), uniformly coated waveguides (10.5 / 15.6 dB at L = 1.4 mm, Fig. 6(e)) and the graphene comparison (3.6 dB): hypothetical designs without a fabricated row; not entered. Simulated optima for the fabricated 1.4 mm devices (Fig. 7 at 400 W / 1 mW, Fig. 8(a) vs detuning) are entered as `simulated`.
- Picosecond-pump results (Supp. Fig. S2): supplement not cached.
- GO film thickness ~2 nm per layer (AFM) and window position (~0.7 mm from the input): no parameter for a coating thickness on these classes; in core_material.

kittlaus2018
- Nonreciprocity 38 dB (δ = 5 nm), > 19 dB over the FWHM (δ = 15 nm), 20-40 dB range; Stokes / anti-Stokes asymmetry 37 dB: no registry parameter (D419 candidates `conversion_contrast_db`, `sideband_suppression_db`); in component notes.
- FWHM in frequency (125 / 150 GHz): `bw_3db_ghz` not allowed on mode_converter. Tuning of the operating wavelength over 35 nm (pump 1530-1565 nm): `tuning_range_nm` not allowed on mode_converter (D419 widening candidate).
- Acoustic resonance 5.7 GHz, 17 MHz width, phonon Q 335, Brillouin coupling G = 195 W^-1 m^-1, TPA / FCA coefficients (Supp. Table I): no parameter; Table I and the 0.9 % at 104 mW point (Supp. Fig. 7) are for "one device" not identified (D159).
- Group indices 4.0595 / 4.1853: cited to the authors' ref. [5] (rule 3).
- Mode multiplexers M1-M4: design in the authors' ref. [30], no value of their own (crosstalk mentioned without a number).
- Supp. Sec. I.F / Fig. 3(c), (d) alternative weakly guiding design (Δn_g 0.01, tenfold bandwidth): simulation of a hypothetical design; no row.

## Missing fab / facility orgs

None needed. Both papers have no fabrication statement naming an org: qu2024 "we fabricated" across Swinburne, CEA-LETI, INL Lyon and RMIT authors with a passive Methods text (D154 / D468); kittlaus2018 passive Methods, all authors at Yale (D80b). Neither acknowledges a facility.

## Judgment calls

1. kittlaus2018 class: `mode_converter.converter`, not `nonreciprocal` (cache-list hint), per D419 (kittlaus2020a / sohn2018): the device is a single-sideband mode-converting modulator; its "nonreciprocity" is a forward / backward scattering-efficiency contrast, no isolation of a transmitted signal is measured.
2. kittlaus2018 efficiency "around 1% for all tested devices": entered on each of the three device rows (`coupling_efficiency_pct`, scope `de_embedded`, kittlaus2020a precedent), as a statement about every device (D465), not a typical value on one representative (D254). Band C inferred.
3. kittlaus2018 "< 1 dB total insertion loss for this L = 2.39 cm long device": put on the main-text device (δ = 5 nm; Methods name a single "device under test"), `derived` from the paper's own loss arithmetic, scope `de_embedded`, method `loss_breakdown`. Sibling rows carry length 2.4 cm from the Supp. statement for all current devices. Alternative: no IL row (if the auditor reads "this device" as unidentified, D159).
4. kittlaus2018 losses 0.2 / 0.4 dB/cm: `measured` (printed "estimated", but Supp. p.32 states the non-simulated Table I values are measured; rule 4 quote kept), method unspecified, on a separate waveguide row (D396 cross-note).
5. kittlaus2018 geometry: 215 nm top layer `design_target` (Methods text); width 1500 nm, ridge 80 nm, slab 135 nm `extracted_from_figure` (labels in Fig. 1(b) and Supp. Fig. 3(a)); 80 nm entered as `etch_depth_nm` (ridge height above the slab; 80 + 135 = 215).
6. qu2024 net PG (11.8 / 20.4 / 24.0 dB): `derived`, ref_plane on_chip (powers referenced to the waveguide with the ~4.2 dB/facet coupling excluded; D166, ye2021); on/off gains `measured` (pump-on / pump-off ratio at the same plane). Signal wavelength 1535 nm computed from the pump centre ~1557 nm and Δλ ~-22 nm (matches the Fig. 4(a) signal line); `wavelength_inferred` left empty since both terms are stated conditions. Alternative: set it true.
7. qu2024 GO-length series (Fig. 5(c), 0.2-1.1 mm): sibling fabricated devices (rule 9, p.17 "by measuring devices with various GO film lengths"), one row each with a figure-read PG (+/- 0.2 dB). The implied uncoated reference differs per length (13.1 / 13.3 / 12.0 / 12.2 vs 11.8 dB, from Fig. 5(c-i) minus (c-ii)); noted.
8. qu2024 GO-section losses: printed GO-induced excess (3.1 / 6.3 dB/cm, `excludes` the 3.0 dB/cm window loss) plus the summed section totals 6.1 / 9.3 dB/cm (`derived`), ghosh2012a precedent. Window-section 3.0 dB/cm `derived` (difference of structures); buried 0.5 dB/cm `measured` (cutback). Band C inferred on all loss rows.
9. qu2024 device fiber-to-fiber IL read off Fig. 2(a) (9.7 / 10.2 / 10.6 dB over 1500-1600 nm, +/- 0.1 dB) entered on the amplifier rows as `extracted_from_figure`.
10. qu2024 cross-section 1.60 x 0.72 um assigned width x height by print order and the Fig. 1(c) sketch; um -> nm `derived` (D82d).

## Registry gaps (skipped value + locator, proposed definition)

- `nonlinear_parameter_per_w_m` (amplifier, frequency_converter, waveguide_platform): Kerr nonlinear parameter gamma in /W/m, fit method in notes. qu2024 ~1.11 /W/m uncoated (p.19), GO-1 / GO-2 as multiples (p.19, Fig. 6(a)).
- `gain_improvement_db` (amplifier): gain increase over a stated reference device at the same operating point. qu2024 ~12.2 dB (p.16, Fig. 4(c-ii)). Low priority (relative quantity).
- Confirms D419 candidates: `conversion_contrast_db` (kittlaus2018 38 dB, p.6 Fig. 3(d)i; > 19 dB over FWHM, p.6), `sideband_suppression_db` (37 dB, p.6 Fig. 3(e)), `tuning_range_nm` and `bw_3db_ghz` on mode_converter (35 nm, p.6 / Supp. p.29; 125 / 150 GHz, p.6).
- Brillouin / acousto-optic set (low priority, only a few rows): acoustic resonance frequency and linewidth (5.7 GHz, 17 MHz, Fig. 3(b)), Brillouin gain coefficient (195 W^-1 m^-1, Supp. p.32).
