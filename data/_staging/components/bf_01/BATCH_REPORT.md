# Batch report bf_01 (2026-10-20)

Transcribed by the coordinator. Dry-run 0 errors: +24 components, +64 metrics. No figure images opened.

- huang2026a (0): review / modelling; all device numbers cited or assumed.
- kim2025 (5/14): 200 um racetrack, 50 um ring, straight waveguide, 50 / 200 um bends: Qi / QL, loss from Qi (derived; ng not stated), fit-extrapolated straight and bend losses (dB/cm), 60 deg sidewall (AFM). Standalone test devices, no host. 50 um ring Qi 0.84e6 text vs 0.85e6 Table S1 (text used, noted).
- boynton2020 (6/12, fab Sandia MESA): lensed-fiber facet, air/TFLN-edge transition, bi-layer SiN vertical coupler, MMI, routing bends, passive-waveguide test structure; mostly simulated Table 2 element losses; measured 7.75 dB for the passive test structure (scope unspecified). Not entered: 1.28 dB propagation (cited [21]), phase-modulator test structure (EO), 3.5 um spot (setup condition), PD / EDFA / laser (setup).
- li2024 (1/1): GC ~5 dB per coupler (author_estimate; band unspecified, stated once for both bands). Not entered: EC ~1.5 dB/facet (hypothetical), BTO DC tuner < 100 uW (EO).
- niels2025a (2/2): coupon-facet transition 1.8 +/- 0.2 dB (cutback, measured); GC + reference-path 16.9 dB (fiber_to_fiber). Not entered: 0.9 dB/cm (EO column).
- tiberi2025 (1/1): GC ~6 dB per coupler (half of a reference waveguide, loopback_half; C-band inferred); hosts -a, -b (O-band -c excluded).
- liu2023 (3/14, facility Westlake Center): MWG WDM filter (wdm.bragg_cdc: excess < 0.8 dB, crosstalk > 22 dB, 20 nm spacing, 16 nm 1-dB width measured / 16.5 nm simulated, ~0.15 dB per stage as printed, periods, N); dual-core mode (de)mux (simulated 0.05 dB, crosstalk > 20 dB); FP-cavity MWG reflectors (theory: 85 %, < 0.015 dB, N = 180). Channel wavelengths = design centers (wavelength_inferred). Not entered: SLSR > 35 dB and simulated 99.5 % reflectivity (gaps), FP-cavity Q / FSR / ER (EO).
- kohli2023 (3/10, facility BRNC): a-Si overlay GC ~3.5 dB scope unspecified (budget 2 x 3.5 + 2 x 0.75 + 20.5 = 29 dB consistent with per coupler, noted); SiN-BTO vertical coupler 0.75 dB measured (reference devices), < 0.1 dB simulated, geometry; photonic-plasmonic converter excess 6.5 dB derived ((20.5 - 7.5) / 2), ~1 dB simulated (own FEM). Not entered: 0.5 dB/um plasmonic loss (EO).
- luan2026a (3/10): GC at 2 um (6 dB) and at 1.55 um (4 dB), scope unspecified, 8 deg design angle, geometry; strip-to-slot MMI converter 0.3 / 0.45 dB (two bands). DTU Nanolab thanked for training only: not entered.
- kawahara2025 (0): TiN bias heater <= 3.3 mW for pi/2 (no fitting parameter; in EO notes).

Judgment calls: BRNC "cleanroom operations team" thanks entered as facility (inconsistent with the pilot's kohli2025 exclusion of BRNC: to settle in the consolidated audit); Holonyak and DTU Nanolab (staff / training thanks) not entered; simulated-only parts on fabricated chips row_kind fabricated; bend loss per length as prop_loss_db_per_cm on waveguide_platform.bend; niels2025a test-target values linked to niels2025a-a with a note; kohli2023 converter as excess_loss_db (paper wording) vs kohli2025 insertion_loss_db.
Gaps: tuning_power_mw for phase_shifter (phase in condition); slsr_db (wdm, reflector); reflectivity_pct for wdm.
