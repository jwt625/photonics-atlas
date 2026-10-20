# Batch report ofc_01 (OFC 2026, facts only, 2026-10-20)

Transcribed (condensed) by the coordinator. Dry-run 0 errors: 22 components, 67 metrics from 9 papers; no rows: Th4C.3, Tu2E.1 (rack-level protection switch, not a PIC component), W3F.2.

- Th2A.10 (2/4, fab AMF): Si ring Q 27,000 (q_loaded), R 10 um, W 500 nm; PWB DFB-to-PIC back-reflection 20 dB; band unspecified. Not entered: stabilized-laser figures (no parameters).
- Th1G.4 (5/16): backside-emitting VCSEL 19-ch subarray (threshold ~1 mA, 4-5 mW at 9 mA, > 10 GHz, pitch 43 um, 19 / 57 ch, drift < 100 pm/K author_estimate); backside-illuminated PD (0.5 A/W author_estimate, > 10 GHz, < 1 nA at -2 V); PD microlens ~2 dB; VCSEL-to-MCF ~2 dB, 1-dB tolerance > 5 um; MCF connector pair 0.5 dB (budget terms, author_estimate); nir_below_o inferred. Not entered: slope efficiency 0.5 W/A, capacitance < 0.2 pF (now D77), MCF core spacing.
- W2A.11 (1/8): 12-arm MCI tunable laser (laser.tunable): 93 nm (1475-1568 nm), SMSR > 49 dB mean, > 9 dBm mean, power fluctuation < 1.5 dB, linewidth 48.5 kHz best / < 100 kHz; SiN 400 x 1000 nm design.
- Th1F.6 (2/7, facility EPFL CMi): Er:Si3N4 mode-locked laser (laser.comb: <= 22.5 mW on-chip, 1.2 GHz repetition rate as channel_spacing_ghz (now repetition_rate_ghz, D77), Lorentzian linewidth 3.6 kHz best, cavity ~7 cm, 200 nm Si3N4); chirped Bragg grating 26.1 nm 3-dB reflection band (stopband_width_nm), 2000-3000 periods. Not entered: pump threshold 27.3 mW, 9.5 nm bandwidth, 300 fs, 46.9 fs jitter, GDD (now partly D77).
- M2D.1 (4/10; fab SITRI not in registry): TO phase shifter P_pi 2.52 mW, IL 0.4 dB per_component cutback, footprint 3675 um2 derived; 1x2 MZI switch ER > 23 dB, rise 28.18 us, fall 25.31 us; 1x8 switch IL 1.96 dB mean de-embedded (Sec. 3; abstract calls it fiber-to-fiber), crosstalk > 20 dB, 8 ports; superlattice waveguide 0.25 dB/cm. Not entered: "< 1 V for 2 pi", +/- 0.34 dB port variation (now il_nonuniformity_db for switch_fabric), 2 dB/cm benchmark.
- W3E.7 (1/4): vertical-illumination InGaAs/InP PD 0.55 A/W at 1310 nm, > 0.47 A/W over the O band, ~210 GHz at -2 V (table header 205 GHz), 300 nm absorber. Fab empty (not stated).
- Th1A.3 (1/7): cryogenic VCSEL at 3 K: 17.1 mW at 34.5 mA; intrinsic BW > 50 GHz at 2 mA, 30 GHz at 1.4 mA; 849.04-851.12 nm vs current.
- Th3C.1 (5/6, fab UC Davis per D72): Si3N4 AWGR IL 4 dB, crosstalk 22 dB (not tied to a size; scope / type / wavelength not stated); ULI waveguide 2.75 dB/cm (derived); three ULI chip-to-chip interconnect variants 25.2 / 12.8 / 17.3 dB (scope unspecified).
- Tu3C.5 (1/5): athermal Ta2O5 AMZI with PZT (wdm.cascaded_mzi, other): 1.98 pm/K at 1550 nm, IL 3.2 dB excluding facets, core 90 nm, arms 2.8 / 7 um. Not entered: -36.9 pm/V (now tuning_efficiency_pm_per_v, D77).

Orgs missing: SITRI (fab, M2D.1), Marvell Nanofabrication Laboratory and Center for Nano-Micro Manufacturing (facilities, Th3C.1), SUSTech Core Research Facilities (borderline).
Gaps proposed: listed in D77 (added); max tolerated feedback, sweep bandwidth, GDD, lifetime not added.
