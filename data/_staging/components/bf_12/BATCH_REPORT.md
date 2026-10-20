# Batch report bf_12 (2026-10-20)

Transcribed by the coordinator. Dry-run 0 errors: 17 components, 38 metrics; every paper has rows.

- weigel2018 (3/7, facility SDNI from the funding statement): Si-LN adiabatic transition 0.1 dB simulated (details in earlier work [20]), widths 650 / 320 nm; Si rib 1.3 dB/cm measured (C band inferred); Si edge taper ~3 dB per facet author_estimate. Not entered: EO-row values, simulated electrode loss, DC ER > 15 dB / ~30 dB (now extinction_db for splitter, D74). Fab empty ("a foundry Si photonics process [4]").
- zhang2026b (2/5): 1.0 um ridge < 0.5 dB/cm mean over 1280-1360 nm (cutback); microring Q_L ~4e5, Q_i ~1.65e6, ~0.3 dB/cm ring-extracted (O band inferred). Not entered: 0.37 dB/cm (EO row -a); MMI / GC no numbers. Fab empty (NSTIC + A*STAR IME on every author).
- chen2022 (1/1): GC 4.0 dB loopback_half derived ((8.2 - 0.2) / 2), band unspecified.
- kholeif2026 (1/1): GC 5.5 dB per coupler ~1560 nm author_estimate. Not entered: racetrack fit kappa 0.379, round-trip loss 0.86 dB (modulator cavity).
- su2026 (3/5): GC 5.45 dB per coupler at 1550 nm author_estimate (paper's numbers do not add up: 11.81 - 2 x 5.45 = 0.91 vs stated 0.86 dB); rings air-clad (FWHM 13 pm, Q 1.3e5) and CaTiO3-clad (8 pm, Q_L up to 2.0e5), C band inferred. Not entered: 8.2 dB/cm (EO), RMS roughness.
- kieninger2020 (4/18, fab A*STAR IME; hosts all 21 EO rows): GC aGC 4 dies measured + aGC,2 4 dies derived (MMI-cascade fit) at 1560 nm; MMI excess 0.27-0.28 dB (4 dies); strip-slot converter 0.10 dB; strip access 0.32 dB author_estimate (foundry spec). Converter / strip at 1510-1580 nm inferred. MMI port count "2?2" (symbol-font byte; likely 2x2, unconfirmed).
- khalil2026 (1/2): racetrack Q_i ~70k at 1550.142 nm, 5 K (Fig. 3(d) label checked), linewidth 5630 MHz; EO row holds them only in notes. Fab empty (imec + Ghent); Xplore staff thanks not entered.
- eltes2023 (1/1): GC ~5 dB per coupler (1550 nm inferred, author_estimate); platform empty. Not entered: BTO DC tuner < 100 uW (EO).
- datta2024 (1/3, fab Columbia University; facilities CNI + CUNY ASRC NanoFab by judgment): bare SiN 50 um ring Q0 ~112k, 5.98 dB/cm derived, band unspecified (1538-1646 nm).

Gaps: extinction_db for splitter (added, D74); tuning_power_mw for phase_shifter (already D71).
