# lit_77 batch report (amplifier, frequency_converter, nonreciprocal), 2026-11-04

All six cached texts match their source rows (page-1 title); none is a correction or another paper. Dry-run: +19 components, +166 metrics, 0 errors (one existing warning on merged row ni2025b, not from this batch). Supplements are absent for lu2019, chang2026 and lorenzen2026; kim2026 and yang2026 carry supplementary pages in the cached file; shi2026 has none cited.

| paper | components | metrics |
|---|---|---|
| lu2019 | 2 (frequency_converter.shg, resonator.ring) | 24 |
| chang2026 | 3 (amplifier.parametric, frequency_converter.shg, fiber_chip_coupler.edge) | 30 |
| kim2026 | 2 (nonreciprocal.isolator, resonator.coupled_rings) | 26 |
| yang2026 | 2 (frequency_converter.sfg_dfg, waveguide_platform.straight) | 21 |
| lorenzen2026 | 7 (amplifier.rare_earth x3, fiber_chip_coupler.edge x2, waveguide_platform.straight x2) | 39 |
| shi2026 | 3 (amplifier.rare_earth, waveguide_platform.straight, fiber_chip_coupler.edge) | 26 |

## Not entered, and why

lu2019
- Duty cycle ~35 % (p.3), temperature FWHM 0.30 C measured / 0.35 C calculated (p.4), external SHG 280 nW at 360 uW (p.4), pulley angle 60 deg (Fig. 1(b)), Q_L/Q_c 0.53 / 0.82 (p.5): no parameter, in notes.
- d31 ~3.2 and d33 ~19.5 pm/V: cited ref. [46]. TM00-to-TM00 period ~2.87 um: alternative not built. Calculated g, chi(2)eff, overlap: not registry quantities.
- Fig. 3(d) SHG spectra: only relative, no value read. Fabrication process itself: previous work [36].

chang2026
- Waveguide loss 0.1 and 0.4 dB/cm (p.3, p.14): the sentence and caption attribute them to the authors' refs. [15, 16] (D259 / D408). No waveguide row.
- 1.3 dB/m, 6 dB/m (cited) and the 7774.72 %/W and 19.73 dB projections computed from them (p.7-8): rule 3.
- Normalized gain 1.21 dB/(W mm) (p.3, p.7): no parameter; also does not reproduce from the printed numbers (10.79 / (0.17 x 16) = 3.97). 56 THz stays a note on bw_3db_nm. Dispersion beta2 / beta4 simulated: no parameter.
- Gain per wavelength in Fig. 3(e-g) and 4(e-g): printed spectra points only taken from the text (1360, 1550, 1690 nm); curves not read. Poling period never stated (adaptive).

kim2026
- LN propagation loss < 0.1 dB/cm, transparency, r33: cited [30, 31]. Sohn / Tian etc. in Supp. Table 1: other works.
- Stokes sideband -17.8 dB, IC/IL 32.9, drive and consumed RF power (28 dBm, 12.9 mW), 5 mW optical power, 8 nm tuning, electrode pitch 150 um, Geo 0.89 GHz, gap dispersion 4.1 GHz/THz: no parameter on nonreciprocal / resonator, in notes.
- Speculated range 180-194.5 THz (p.12), +/-100 V fine tuning (in principle): not measured.

yang2026
- Noise 35 cps, 3-fold noise reduction, SNR ~120:1, QPM temperature slopes, defect-count model values, Fig. 1(b) relative efficiencies (relative only): no parameter.
- Fabry-Perot filter (40 MHz, 45 GHz FSR), VBG (10 GHz), bulk filters, 80 % fiber collection, 79 % filter stage, SNSPD 85 %: setup parts (rule 13, D411); they enter only inside the 28.8 % definition.
- Lossless fit 1141 %/W/cm2 (p.10): a rejected model; in notes. Table I other works: not entered.

lorenzen2026
- PDG values (0 dB tuned points, < 1 dB, < +/-0.1 dB, up to 8 dB): no amplifier parameter. p.8 "below 0.1 dB" conflicts with p.7 "below 1 dB"; in notes. Fig. 4(c-d): caption and panel labels assign line styles to pump states oppositely, so curves not read (D156).
- SiO2 spacer 300 nm: gap_nm not allowed on amplifier. Mode areas: no parameter. Thulium concentration, film data: notes. Vertical SiN-Al2O3 taper: no value, no row.
- 0.2 dB per facet (p.6): cited [71]. Projected fiber-to-fiber NF < 4.0 dB: rests on the cited value. > 50 % / ~60 % efficiency: cited [51, 52]. Thin-film PDG > 15 dB: projection.
- Fig. 2(b-c) gain and power curves at 1833-1889 nm: only printed values taken.

shi2026
- DMG 0.8 / 3.1 / 5.4 dB: no parameter, power_uniformity_db is defined on output power and the coupling loss differs per mode, so it is not equivalent; in notes, reproducible from per-mode rows.
- Crosstalk with device better than -13 dB (Fig. 4(c)): crosstalk_db not allowed on amplifier and the value includes the lanterns. Lanterns and few-mode WDM: setup equipment (D160).
- Table I overlap factors, Delta Gamma, index design values: not registry quantities. Refractive indices in core_material.

## Missing fab / facility orgs (checked organizations.csv and org_aliases.csv)

- lu2019 facility: "Yale SEAS cleanroom", "Yale Institute for Nanoscience and Quantum Engineering" (p.5).
- chang2026 facility: "University of California Los Angeles Nanolab", "Molecular Foundry at Lawrence Berkeley National Laboratory" (p.13). Owners not entered as facilities.

## Judgment calls

1. chang2026 fab org_university_of_california_berkeley: the two named fabricators (p.13) share that affiliation, each with a second one (USC, LBNL); D395 reading. Alternative: empty as hiratani2024 (D433). Three facilities at other sites are acknowledged too.
2. kim2026 fab UIUC (first-person sentence p.6, all authors one university, contributions p.17; D399). HMNTL staff thanks not a facility.
3. lu2019 Q0 and Qc `author_estimate` (D403): the paper states the regime but its extraction is in the uncached Supplement Sec. 2.
4. kim2026 tuning efficiency converted from GHz/V with nominal 1550 nm because the pair's wavelength is not stated: `author_estimate`. Isolation widths converted at the stated 1545.5 nm: `derived`.
5. kim2026 kappa values taken as `linewidth_mhz` (the paper says loss rates; 2 pi convention not printed; TE odd critically coupled means loaded width, as the registry definition asks).
6. yang2026 839 %/W/cm2 `author_estimate` because it rests on a correction whose ratio matches the simulated 111 %; 703 stays `measured` (fit in range). 28.8 % `measured` (Fig. 4(b) filled points; Eq. (4) product agrees); could be read as `derived`. Platform lnoi_rib for a 5 um film with a 1.5 um slab.
7. yang2026 T_WG 49 % and 60 % entered as `insertion_loss_db` on the converter with scope device_total, since eta_int is defined at the waveguide output, so T_WG spans lens coupling and propagation.
8. lorenzen2026 per-facet losses `loopback_half` + `derived`: Methods state they come from the total loss of a 2.2 cm passive waveguide, unlike a bare D167 statement. Paper calls them per facet.
9. lorenzen2026 gain layer `t = 1100 um` read as 1100 nm (typo per "slightly thicker" than 1000 nm), flagged. Two `core_thickness_nm` rows (gain layer, SiN) and two `width_nm` rows (LMA, confined) with the role in condition; platform al2o3 (garciablanco2025 precedent).
10. lorenzen2026 tunable-PDG gain read from the circled Fig. 4(b) points (the only unambiguous gain values for that device), +/- 0.3 dB.
11. lorenzen2026 6.7 cm device kept as a row only for the 1650-2050 nm span (`gain_bandwidth_nm` 400 derived, gain level not printed); delete if the audit finds the criterion too weak.
12. shi2026 gain definition is not stated; left without ref_plane, noted. Fig. 4(a) losses exceed the gain, so not fiber-to-fiber net. fmf facet values may include lantern terms, noted. Fabricated dimensions assumed width x height from the printed order.
13. chang2026 max-gain rows `band: unspecified`: the probe wavelength of the maximum is not stated; 10.81 dB at 1690 nm exceeds the stated maximum 10.79 dB, flagged.
14. Text vs figure: kim2026 1545.50 nm (text) vs 1545.70 nm (Fig. 3(c)): text used, flagged.

## Registry gaps (skipped value + locator, proposed definition)

- `pdg_db` on amplifier: lorenzen2026 < 1 dB, < +/-0.1 dB, 0 dB (p.7). Polarization-dependent gain as G_TE - G_TM.
- `differential_modal_gain_db` on amplifier: shi2026 0.8 dB (p.7). Max minus min modal gain.
- `crosstalk_db` on amplifier: shi2026 13 dB (p.5). Mode or channel crosstalk through the amplifier, includes in condition.
- `noise_counts_cps` on frequency_converter: yang2026 35 cps (p.4). Output noise count rate at the operating point.
- `temperature_acceptance_c` on frequency_converter: lu2019 0.30 C (p.4). FWHM of efficiency vs temperature.
- `duty_cycle` on frequency_converter: lu2019 ~35 % (p.3). Inverted-domain fraction of the poling period.
- `radius_um`, `gap_nm` stay on the resonator row (D396 works); no change needed.
- `sideband_suppression_db` on nonreciprocal (D419 candidate): kim2026 17.8 dB (p.10).
- `tuning_range_nm` on nonreciprocal: kim2026 ~8 nm (p.10). `power_consumption_w` on nonreciprocal: kim2026 12.9 mW upper limit (p.9). `isolation_loss_ratio_db_per_db`: kim2026 32.9 (p.9).
- `gap_nm` on amplifier: lorenzen2026 300 nm spacer (p.8). `mode_area_um2` on amplifier: lorenzen2026 21-57 um2 (p.2, p.6).
- `normalized_gain_db_per_w_mm` on amplifier: chang2026 1.21 (p.3), value inconsistent, re-check first.
- `bw_3db_ghz` or THz form on amplifier: chang2026 about 56 THz (p.1), held as a note.
