# lit_180 batch report

Papers: lit:zhou2023a, lit:bino2018. verified_on 2026-11-18. Both cached texts match their source rows by page-1
title and authors; neither is a correction. Both are arXiv preprints (details per paper). Dry-run: +7 components,
+29 metrics, 0 errors (the one WARN is a merged ni2025b row, not this batch).

## lit:zhou2023a (arXiv 2211.05864 v1 of the CLEO 2023 source row; Si acousto-optic AOM and isolator)

Cached copy: arXiv v1 preprint (manuscript dated 2022-11-14, 8-page main text plus 17-page supplement, pp.9-25). The
source row says CLEO 2023 with no DOI; the conference version was not read and may be shorter. Everything below is
from the preprint.

Components 4 / metric rows 21:

| component | metrics | content |
|---|---|---|
| cmp_lit_zhou2023a_triridge_wg_loss (`waveguide_platform.straight`) | 7 | symmetric / anti-symmetric mode loss 0.304 / 0.869 dB/cm (from alpha 7.0 / 20.0 m^-1, derived, C band inferred); ridge widths 1500 / 1495 nm, slab 150 nm, ridge height 80 nm, BOX 3 um |
| cmp_lit_zhou2023a_multipass_aom (`mode_converter.converter`) | 4 | conversion -2.08 dB at 1539.2 nm (de_embedded, GCs factored out), 62 % (Table S2 own row), 3-dB optical bandwidth 1.7 nm, L_tot 9950 um |
| cmp_lit_zhou2023a_ao_isolator (`nonreciprocal.isolator`) | 4 | isolation 14.37 dB and IL 0.74 dB at 1532.01 nm, 10-dB isolation bandwidth 0.462 nm (59 GHz converted, D256), L_tot 9950 um |
| cmp_lit_zhou2023a_mode_mux (`mode_converter.mdm_mux`) | 6 | per-multiplexer IL ~0 dB (symmetric) / < 0.2 dB (anti-symmetric) from a two-multiplexer reference, crosstalk > 20 dB (two in series), coupling length 33 um, widths 600 / 1500 nm (Fig. S2(a) labels) |

Fab `org_sandia_national_laboratories` on all 4 rows: Supp. p.9 "fabricated on ... SOI wafers using Sandia's ...
(MESA) CMOS production and research facilities" (a passive sentence that names the org, Contract v7). process_name
empty: "a CMOS foundry process" (p.1) names no node, flow or PDK. Facility empty.

Not entered and why:
- Carrier-suppression ratio 55.3 dB and single-sideband selectivity 32.1 dB (p.4 Fig. 3(b)): no parameter
  (kittlaus2020a precedent; registry gap below). In AOM notes.
- RF power for unity conversion 22.16 dBm (device 2) / 29.49 dBm (device 3), P_pi/2 164.4 mW, acoustic resonance
  3.13 / 3.02 GHz, acoustic Q ~200, IDT S11 and linewidths, 20.9 dB multi-pass vs single-pass enhancement (theory
  23.52 dB), electro-acoustic xi gamma 2.06 kHz: no parameters or not optical-component metrics. In notes where
  relevant.
- Device 1 (single-pass vs multi-pass comparison, Fig. 2(d), (e); power robustness ~2 dB drop at 100 mW, Supp.
  Fig. S1(c)) and the single-pass reference device: no absolute optical value printed, no rows; in AOM notes.
- Reverse-direction isolation window at omega_b (46 GHz, Fig. 4(d)): its centre wavelength is not printed; in
  isolator notes.
- "> 40 dB transmission contrast" from the heterodyne measurement that ignores cross-talk tones (p.6, Supp. p.24):
  not a total-power isolation (D419 / D602 form); in isolator notes.
- Simulated / projected values: 30-50 dB isolation, 12-25 nm and > 6 nm bandwidths, 20 dB over ~0.21 nm, 0.206 nm
  (26.3 GHz), ~5 nm / > 18 nm modulation bandwidth, 1.52 / 1.78 nm calculated bandwidth. Predictions for modified
  designs, not rows.
- Loss budget terms of the AOM (1.01 dB propagation, ~0.2 dB multiplexers, ~0.8 dB evanescent coupling, p.4): in AOM
  notes; the multiplexer term matches the entered < 0.2 dB.
- COMSOL group / effective indices, coupling rates kappa / mu (Table S1 footnotes d / e): simulated or estimated model
  inputs.
- Table S2 / Fig. S9 values of other works: rule 3.
- Grating couplers: no value printed (loss "factored out", p.4), no row.
- Multiplexer gap 0.3 um (Fig. S2(a)): `gap_nm` is not allowed on mode_converter (registry gap below).

Judgment calls:
- Waveguide loss: alpha_1 / alpha_2 are fit parameters of the device-2 Rabi data (Table S1 footnote c) and the fit
  assumes them constant over the whole 9.95 mm spiral (bends, tapers, suspended and unsuspended sections). Entered as
  `waveguide_platform.straight` (cheng2025 two-ridge precedent) with method `unspecified`, basis `derived` (fit +
  m^-1 -> dB/cm), approx. The footnote's "consistent with our previous measurements [15]" is a comparison, so the
  values are this paper's (not D259).
- AOM: kept in `mode_converter.converter` (kittlaus2020a / cheng2025). Both the printed -2.08 dB and the Table S2 62 %
  are entered (two printed forms of one operating point, different locators); the audit may drop m2.
- Isolator IL 0.74 dB scope `unspecified`: Fig. 4(d) is a normalized transmission whose reference is not stated (the
  AOM data on p.4 are explicitly normalized to on-chip power, but the isolator text does not say so).
- Isolation wavelength: 1532.01 nm (main text) entered; Supp. p.24 prints 1531.95 nm for the same 14.37 dB (D417 note).
- Isolation bandwidth 59 GHz converted to 0.462 nm at 1532.01 nm, derived (kim2026 / sohn2021 precedent, D256).
- Multiplexer IL per device is the authors' halving of a two-multiplexer reference: `derived`, `per_component`,
  `reference_structure`, test_structure true; wavelength span 1500-1580 nm is the Fig. S2(b) axis (inferred). Crosstalk
  "< -20 dB" C band inferred, with a note that the plotted 2 -> 1 trace reaches about -15 dB near the span edges.
- Supp. p.19 says 3.6 mm of a "9.35 mm" total length is active, against L_tot = 9.95 mm in Table S1 and Supp. p.19
  elsewhere: 9.95 mm entered, conflict noted.
- Platform `soi_rib` for the tri-ridge rows (Fig. 1(c): 80 nm ridges on a 150 nm slab); multiplexer `soi` only
  (cross-section not stated).

Missing fab / facility orgs:
- "Sandia's Microsystems and Engineering, Sciences and Applications (MESA) CMOS production and research facilities"
  (p.9 Supp. Sec. I.A): possible facility org (child of org_sandia_national_laboratories); not in organizations.csv /
  org_aliases.csv. Not entered as facility because Sandia is already the fab and no MESA id exists; the coordinator may
  decide whether an in-house fab line counts as a shared facility.

Registry gaps (skipped value + locator + proposed definition):
- `carrier_suppression_db` (mode_converter, frequency_converter): 55.3 dB, p.4 Fig. 3(b); "suppression of the residual
  optical carrier relative to the wanted shifted sideband at the output port, positive dB".
- `sideband_suppression_db` (mode_converter, frequency_converter; already a D419 candidate): 32.1 dB, p.4 Fig. 3(b);
  "suppression of the unwanted sideband relative to the wanted one, positive dB".
- `gap_nm` on mode_converter: 300 nm, p.11 Supp. Fig. S2(a) (directional-coupler mode multiplexer gap).
- RF drive power for full conversion (`rf_power_full_conversion_dbm`, mode_converter / nonreciprocal): 22.16 dBm and
  29.49 dBm, p.12 Supp. Table S1 (P_pi/2 164.4 mW, Table S2). Low priority.

## lit:bino2018 (arXiv 1801.09918 v1 of the Optica 2018 source row; Kerr-nonreciprocity isolator and circulator)

Cached copy: arXiv v1 preprint (2018-01-30) with the supplement on pp.10-11; same title and results as the Optica
article in the source row (journal version not read).

Components 3 / metric rows 8:

| component | metrics | content |
|---|---|---|
| cmp_lit_bino2018_silica_microrod (`resonator.disk`) | 3 | raw Q 1.5e8 (`q_intrinsic`, author_estimate, D403), loaded Q ~3e7 with both tapers (author_estimate, origin not stated), radius 500 um (from 1 mm diameter) |
| cmp_lit_bino2018_kerr_isolator (`nonreciprocal.isolator`) | 2 | isolation > 24 dB (best, 1550 nm, fiber-mirror worst case), insertion loss ~7 dB device_total (both tapered fibers) |
| cmp_lit_bino2018_kerr_circulator (`nonreciprocal.circulator`) | 3 | IL 3.3 dB (47 % port 1 -> 2, derived), directivity T23/T21 > 19 dB as `isolation_db`, unwanted T13 -33 dB as `crosstalk_db` (derived from the oscillation amplitude); 1550 nm inferred |

Fab / facility empty: no fabrication statement for the rod and no facility in the acknowledgments (funding only).

Not entered and why:
- Threshold input power ~10 mW (p.4, p.6): `pump_threshold_mw` is not allowed on nonreciprocal (registry gap).
- Kerr-induced cw / ccw resonance splitting ~50 MHz (~10 linewidths, p.5) and 54 MHz calculated from the fitted
  P0 = 10.8 mW (Supp. p.10): no nonreciprocal splitting parameter (the D535 "nonreciprocal resonance split" gap);
  `mode_splitting_ghz` is defined for supermode splitting, so not used.
- Half linewidth gamma ~2 pi x 3 MHz (Supp. p.10): computed from the loaded Q, not a separate measurement.
- Fig. 2(c) predicted isolation curves for 100 um SiO2 / Si3N4 / CaF2 / MgF2 resonators: calculated with parameters
  taken from other works (Supp. Table 1 refs.), no single values; not rows.
- Isolation vs power data points of Fig. 2(a), (b): only the stated extremes entered.

Judgment calls:
- Scope (D411): the device is a 1 mm diameter fused-silica microrod coupled by two tapered fibers. D411 excludes
  "discrete bulk (mm-scale polished crystalline)" resonators; this rod is amorphous silica and the paper presents it as
  a fiber-coupled isolator / circulator, so it is kept as a fiber-coupled passive part (ilchenko1999 silica
  microsphere, 405-470 um, precedent; fiber-pigtailed bulk garnet isolators of karki2019 are also in). The coordinator
  may rule it out as mm-scale; then all 3 rows go.
- Isolation > 24 dB kept as printed (abstract, caption, p.4) although the conclusion says "more than 20 dB" and the
  Fig. 2(b) points reach about -21 dB (D417 note on the row).
- Isolator IL: caption "around 7 dB" entered (matches the fit line in Fig. 2(b)); the p.4 text says "around -5 dB"
  (conflict noted; data points span about 5.5-8.7 dB).
- Circulator directivity T23/T21 entered as `isolation_db` with the definition in the condition (suppression of the
  port 2 -> port 1 path relative to the wanted port 2 -> port 3 path); T13 as `crosstalk_db`.
- D396: one row per class (resonator, isolator, circulator). The paper does not say explicitly that the isolator and
  circulator used the same rod; the supplement compares the circulator's Q_L with the 1.5e8 rod Q. Cross-noted.
- Resonator subtype `resonator.disk` (microdisk / whispering gallery), platform `silica` (ilchenko1999 precedent).

Missing fab / facility orgs: none (no fabrication or facility statement).

Registry gaps:
- Threshold power on nonreciprocal (`pump_threshold_mw` widened to nonreciprocal): ~10 mW, p.4 / p.6; "input power
  at which an optically biased nonreciprocal device starts to isolate".
- Nonreciprocal resonance splitting (`nonreciprocal_splitting_mhz`, resonator / nonreciprocal): ~50 MHz, p.5;
  54 MHz calculated, Supp. p.10; "frequency difference between counter-propagating resonances under bias".
