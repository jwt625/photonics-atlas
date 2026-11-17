# lit_156 batch report

Distilled 2026-11-16 (contract v7, skill `pic-component-distill`). Papers: hwang2023, gaafar2024, zhao2020, luo2018.
All four cached texts are arXiv versions of the journal papers on their source rows (hwang2023 v1 / Optica, gaafar2024
v2 / Nature Communications, zhao2020 v1 / PRL, luo2018 v1 / Optica); authors and numbers match the source rows, same
works (D430 / D433), journal versions unread. zhao2020's arXiv title differs in wording ("Entangled photon-pair
generation in periodically-poled thin-film lithium niobate waveguides" vs "High Quality Entangled Photon Pair
Generation ..."). No correction / erratum, no garbled text layer.

Totals: 12 components, 76 metric rows. `merge_component_staging.py --dry-run`: 0 errors (one WARN on an unrelated
merged row, cmp_lit_ni2025b_pimmwc).

| paper | components | metrics |
|---|---|---|
| hwang2023 | 5 | 32 |
| gaafar2024 | 2 | 12 |
| zhao2020 | 2 | 12 |
| luo2018 | 3 | 20 |

## hwang2023 (TFLN-on-sapphire pump-enhanced singly resonant MIR OPO, Stanford / NTT Research)

- Rows: OPO `frequency_converter.other` (mckenna2022 precedent, D252), adjacent straight poled OPA / DFG calibration
  waveguide `frequency_converter.sfg_dfg` (test structure), stealth-diced facet `fiber_chip_coupler.edge`, output
  `splitter.directional_coupler`, intracavity `splitter.adiabatic`. Platform `lnos_rib` (x-cut MgO:LN 878 nm on
  sapphire, 600 nm etch).
- OPO: threshold 80 mW and 15 % pump-to-idler efficiency on-chip `derived` (on-chip via own measured coupling, D394);
  Q_tot 1.3-1.6e6 range and 1.6e6 single mode `measured`; Q_i 1.35-1.7e6 `author_estimate` (D403: undercoupled
  regime stated from design, not shown from data); pump FSR 5.5 GHz `measured` (text cites "Fig. 2a", resonances are in
  Fig. 2(b) top), signal FSR ~5.6 GHz `author_estimate` (origin not stated; also printed ~45 pm); geometry (878 nm
  film, 600 nm etch, 1.95 um gain width, 1 um bends, 22.3 mm cavity, 9.3 mm poled, 6.72 um electrode period).
- Straight waveguide: eta_DFG 43.5 %/(W cm2) `derived` (model fit with on-chip pump from the measured coupling);
  simulated ~300 %/(W cm2).
- Facet: 33 % per edge at 1046-1056 nm and 30 % at 1550 nm `loopback_half` `measured` (D167 / D452; the 33 % assumes
  negligible pump propagation loss, in condition); MIR chip-to-fiber collection ~3 % `derived` (0.16 % with OD1 filter
  and beamsplitter divided out).
- Couplers: design split ratios only (DC ~100 % MIR / ~1 % telecom `author_estimate`, D82a; adiabatic ~100 % telecom
  `simulated`, coupled-mode design stated); rows `fabricated` (on the chip, D80e) with the Methods A geometry.
- Not entered (registry gaps unless noted): idler output 29 +/- 3 mW on-chip at 3.2 um (abstract > 25 mW; no
  frequency_converter output-power parameter); 45 % quantum efficiency (not a power efficiency); Q_ex ~20e6
  (`q_external` resonator only); pump finesse 2.4 / 2.5-3.5 (`finesse` resonator only); pump recirculation 8-14 %,
  build-up 1.75-2.15; ~12 % signal round-trip loss (roundtrip_loss_db candidate, D420 / D540); coarse tuning
  1.5-3.3 um, idler up to 3.315 um at 200 C, 1.3 um span at 80 C, 60-80 pm gap-free fine tuning, dlambda_i/dlambda_p
  -2 to -4.2 (no tuning-range / centre-wavelength parameter on frequency_converter); 70-80 % high-NA collection
  "measured on a different chip/setup" (D159); telecom chip-to-detector 2 % (includes the detection chain); OPA
  calibration data (3.28 % gain, 17.8 nW).
- Printed differences noted, not conflicts: poling electrodes 6.72 um vs simulated Lambda0 6.57 / 6.58 um; film 878 nm
  design vs 875 nm nominal in the simulation; model efficiencies 40 / 41 %/(W cm2) vs measured 43.5 (43 in the
  conclusion).
- Fab `org_stanford_university` (author contributions p.14 name three Stanford fabricators, D395); facility
  `org_stanford_nano_shared_facilities` (p.14, 2023 SNSF name). Wafer NGK (supplier note).

## gaafar2024 (femtosecond pulse amplification, Tm:Al2O3 on Si3N4, DESY / Twente / LIGENTEC / MPL)

- Rows: `amplifier.rare_earth` (platform `al2o3`, lorenzen2026 precedent), Si3N4 inverse-taper `fiber_chip_coupler.edge`.
- Amplifier: on-chip net gain 17 dB (factor 52) at 700 mW on-chip pump, 1815 nm signal `derived` (D166, calibrated with
  coupling losses measured on passive waveguides); on-chip average output 95 mW -> 19.78 dBm `derived`; lengths 12 cm
  total / ~10 cm gain, footprint < 15 mm2, widths 300 / 1000 / 2000 nm, Si3N4 800 nm, gain layer 1000 nm.
- Coupler: 2.9 dB (pump 1610 nm) and 4.2 dB (signal 1815 nm) per facet, `loopback_half`, `measured`,
  `reference_structure` (lorenzen2026 rows).
- Not entered: output pulse 116 fs, peak power > 800 W, pulse energy 95 pJ, spectral bandwidth 5.1 vs 3.5 THz (no
  amplifier pulse parameters; pulse_energy / peak_power candidates, D429); GDD 7.79e-26 s2 (dispersion, D81); simulated
  A_eff / gamma; Euler-bend minimum radius 200 um (`min_bend_radius_um` not allowed on amplifier); Tm concentration
  3.5e20 cm-3 (estimated, in core_material). Polarization of the experiment not stated (design for TM), left empty.
- Fab: amplifier `org_ligentec;org_university_of_twente` (Methods "fabricated by Ligentec SA"; contributions: LIGENTEC
  authors fabricated the Si3N4 chip, Twente authors deposited the gain medium); coupler `org_ligentec` only (passive
  section, Contract v7 per-part fab). No facility (DESY Maxwell is computing).

## zhao2020 (PPLN TFLN photon-pair source, UC San Diego)

- Rows: periodically poled x-cut MgO:TFLN ridge `frequency_converter.shg` (lnoi_rib, 300 nm film, 50 nm etch), diced
  facet `fiber_chip_coupler.edge`.
- SHG: ~2000 %/(W cm2) at 1569 nm `author_estimate` (Fig. 1(d) axis "Estimated eta_norm"; on-chip normalization
  needs facet losses of unstated origin); poling period 2.8 um (calculated, `design_target`); lengths 7 / 5 mm; etch,
  sidewall, film, BOX.
- Facet: 5 dB (1570 nm) and 15 dB (785 nm) per facet `author_estimate` (origin not stated; the propagation losses in
  the same paragraph are cited from ref. 17; D418 nader2025); simulated mode-mismatch 3 / 6.6 dB.
- Not entered: SHG FWHM 1.25 nm (`bw_fwhm_nm` not allowed on frequency_converter); propagation < 1 / < 3 dB/cm (cited,
  rule 3); all photon-pair metrics (PGR slope 23 MHz/mW, brightness, CAR 67,224, g2(0) 0.022, visibility; D250);
  ~-14 dB fiber-plus-filter loss (setup); simulated A_eff / overlap.
- Judgment call: the paper says a detailed SHG study "will be presented elsewhere" but reports the measured efficiency
  and Fig. 1(d) here as its own data; kept (D259 / D408 cover values assigned to another paper, this one is not).
- Fab `org_university_of_rochester` on both rows ("waveguide structure fabricated in collaboration with the
  University of Rochester", p.1; p.8 acknowledgment). UCSD not entered: poling stated passively, authors at UCSD and
  TU Dresden (D80b). No facility.

## luo2018 (z-cut TFLN type-I modal-phase-matched SHG, University of Rochester)

- Rows: SHG waveguide `frequency_converter.shg`, cutback rib waveguide `waveguide_platform.straight`, polished facet
  `fiber_chip_coupler.edge`; all `lnoi_rib` (w_t 1200 nm, h1 460 nm, h2 100 nm, 75 deg; Fig. 1(a) labels checked on
  the page render).
- SHG: 4.7 %/W on-chip at 1559.06 nm, 18.7 C `author_estimate` (judgment call: fit of own data, but on-chip
  referencing needs a visible output coupling loss the paper never states); 14.2 %/W and 22.2 %/(W cm2) `simulated`;
  tuning slope 0.84 nm/K -> 840 pm/K `derived`, simulated 0.69 nm/K -> 690 pm/K `simulated`; length ~8 mm.
- Waveguide 0.54 dB/cm `measured` cutback; facet ~5 dB per facet `measured` (D167 / D452, no total printed). Both
  carry `band: cl_band` `wavelength_inferred` (paper says "telecom band"; Fig. 2(f) spectrum ~1525-1630 nm).
- Not entered: phase-matched wavelength 1559 -> ~1619 nm over 18.7-90.0 C and simulated 1540 / 1574 nm (no
  frequency_converter tuning-range / centre-wavelength parameter); A_eff 1.46 um2, overlap 0.32. Fig. 3(b) tick labels
  (776 / 778 / 800 / 802 / 804 nm) disagree with the printed 779.53 nm SH; label typo noted, not used.
- Fab `org_university_of_rochester` ("we fabricated waveguides", all authors Rochester, D72 / D154); facilities
  `org_cornell_nanoscale_facility` + `org_cornell_center_for_materials_research` ("performed in part at", p.6).
  NANOLN wafer (supplier note).

## Missing fab / facility orgs

None: every fab / facility org named for these rows is in the registry. Suppliers named only in notes: NGK (hwang2023
p.9), NANOLN / Jinan Jingzheng Electronics (luo2018 p.4, zhao2020 p.1; registry has org_jinan_jingzheng_electronics),
La Verre Fluore (hwang2023 p.10, setup fiber).

## Registry gaps (skipped value + locator, proposed definition)

- frequency_converter output power: hwang2023 29 +/- 3 mW idler at 3.2 um (p.3); proposed `output_power_mw`
  (generated output at the stated plane and wavelength) widened to frequency_converter.
- frequency_converter tuning range / phase-matching centre wavelength: luo2018 1559 -> ~1619 nm over 18.7-90 C (p.3,
  Fig. 4(b)); hwang2023 1.5-3.3 um (p.1, p.4); proposed `tuning_range_nm` and `center_wavelength_nm` on
  frequency_converter (D419 candidate).
- frequency_converter acceptance bandwidth: zhao2020 SHG FWHM 1.25 nm (p.2); proposed `bw_fwhm_nm` on
  frequency_converter (D429 candidate).
- frequency_converter cavity terms: hwang2023 Q_ex ~20e6 (p.3) -> `q_external`; pump finesse 2.4 / 2.5-3.5 (p.3,
  p.11) -> `finesse`; signal round-trip loss ~12 % (p.2-3) -> `roundtrip_loss_pct` or `roundtrip_loss_db`.
- amplifier pulse metrics: gaafar2024 116 fs, > 800 W peak, 95 pJ (p.5); proposed `pulse_width_fs`, `peak_power_w`,
  `pulse_energy_pj` widened to amplifier.
- amplifier bend radius: gaafar2024 Euler-bend minimum radius 200 um (p.3); `min_bend_radius_um` on amplifier.
