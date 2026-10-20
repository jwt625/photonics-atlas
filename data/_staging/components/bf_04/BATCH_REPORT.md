# Batch report bf_04 (2026-10-20)

Transcribed by the coordinator. Dry-run 0 errors: +14 components, +29 metrics. tiberi2026, lin2025: no rows.

- hu2026a (4/10): 1x2 MMI stage, 1x8 MMI tree (simulated excess loss 0.026 dB, < 0.087 dB within tolerance, ~0.084 dB; paper says insertion loss); SiON SSC (bare-chip fiber-to-fiber 15.19-16.55 dB, includes tree and MZM path); DFB butt coupling (chip_chip_coupler.butt; ~5 dB derived increase over fiber-coupled input, per_interface; hybrid total 20.19-21.55 dB device_total). Not entered: 9.7 % output-power deviation and 1.36 dB inter-channel IL spread (no parameter), SSC > 300 um taper result (no number), 0.02 dB/cm electrode absorption (simulated, EO), commercial DFB (no metrics).
- pan2021 (1/1): lensed-fiber butt facet ~5 dB/facet at 1957 nm, author_estimate (budget split, origin not stated). Not entered: totals in the EO row; MMI geometry + simulated plot only.
- mao2022 (1/1): end-face coupling to high-NA fiber ~4 dB/facet, author_estimate. Not entered: 1.5 dB/cm (EO column), 1.8 dB "other passive" (not assignable), 200 um taper (geometry only).
- powell2024 (3/10): GC 15.7 dB loopback_half from a two-GC test chip, 3-dB BW 35 nm (visible, wavelength_inferred); DC split ratio 49.5 % derived from the 29.6 dB ER assuming identical couplers; ring Q_L 2.8e5, linewidth 2.7 pm, FSR 205 pm, 0.5 dB/cm author_estimate, radius 119.5 um (half the stated diameter), width 1 um at 638 nm. Source inconsistencies noted (638 nm / 2.7 pm gives ~2.4e5; strongly overcoupled yet loaded Q treated as ~intrinsic). Not entered: projected 30 % GC efficiency.
- wu2022 (1/2): SiON/LN-taper SSC with UHNA7 array: 2.0 dB fiber-to-fiber on a 1 mm reference waveguide (measured), 1.0 dB/facet (derived); c_band inferred.
- li2026ba (1/1): double-layer-taper EC at an unpolished stealth-diced facet ~12 dB fiber-to-fiber, c_band inferred; facility CMi + EPFL IPHYS cleanroom. Not entered: facet topography +/- 5 um (no parameter).
- shen2026 (2/4): GaAs-on-TFLN DFB (SMSR > 50 dB, threshold 27 mA, on-chip power > 10 mW; not linked to shen2026-a); Vernier tunable laser (tuning range > 20 nm; host shen2026-a). Fab not stated.
- renaud2023 (1/1): lensed-fiber facet ~7 dB/facet, author_estimate, band unspecified; hosts all five renaud2023-3um rows; facility CNS. Not entered: Y-splitter 0.2 dB (cited [30]); EO-column values.
- tiberi2026 (0): PD, SOA, EDFA are setup equipment. lin2025 (0): MMI and taper without numbers; Cu CPW is an RF test structure.

Judgment calls: platform sion for SiON-over-LN SSCs (hu2026a, wu2022); other for GaAs-on-TFLN lasers; wafer suppliers as notes.
Gaps proposed: output_uniformity_pct (splitter); il_nonuniformity_db for splitter; facet_roughness_um; laser subtype for Vernier tunable lasers.
