# Batch report ofc_07 (OFC 2026, facts only, 2026-10-20)

Transcribed by the coordinator from the batch agent's final report. Dry run: 0 errors; 11 components, 67 metrics from
7 papers (4 without rows). Ids cmp_ofc2026_*; host_device_ids empty; no e-mail addresses.

## Per paper (components / metrics)

- M4D.5 (3/11, fab org_ntt on laser and PD): SiN waveguide 0.8 x 0.8 um ~0.2 dB/cm by cutback on a same-wafer test
  sample, 50 um bend radius (commercial foundry not named, fab empty; band unspecified). Membrane DML 140 um: threshold
  ~2.4 mA at 50 C; on-chip power ~-1.0 dBm (author_estimate, "estimated"); 17 GHz E-O-E bandwidth at 7 mA (whole link,
  noted); 11.6 mW static power for laser + PD (noted). Membrane PD 110 um ~30 GHz at 1295 nm, bias 3.0 V as printed
  (sign not stated). Not entered: InP-to-SiN taper (only a simulated misalignment penalty; geometry only).
- W4D.6: no rows (purchased DFB set point only).
- W1B.5 (1/7): 940 nm back-emitting VCSEL with metalens: threshold ~0.85 mA, 3.5 mW at 8 mA (typical), ~934.5 nm;
  integrated RIN 1-30 GHz < -146.5 dB/Hz; 20.5 GHz bandwidth, intrinsic > 30 GHz (derived, three-pole de-embedding);
  71 pm/K (derived). Fab empty (all authors Berxel, fabricator not stated). No metalens row (no fitting parameter).
- W4E.5 (1/9): membrane SEL on Si, 70 um, 25 C: threshold 1.6 mA; 1.88 mW max at 13 mA; SMSR 54 dB; SSMF coupling
  loss 9.6 dB per_coupler (printed -9.6 dB; O band inferred); self-heating 71 pm/mW (derived); 25.0 GHz at 15 mA;
  32.9 mW at 13 mA. Fab empty (NTT and Institute of Science Tokyo). Not entered: simulated upward efficiency, bottom
  reflectance, target MFD, slope efficiency, MCEF, D-factor.
- Th3F.4 (2/22): distributed-absorption Ge PD: dark 2.61 nA at -1 V and 5.67 nA at -3 V (statistic best); 1.0 A/W at
  1550 nm with 40 mW input (GC loss excluded); saturation > 16.0 dBm (derived from no saturation up to 40 mW);
  8 bandwidth points 92 GHz at 0.1 mA to 12 GHz at 10 mA; Ge 4.5 x 4.5 um. Conventional reference PD 4.5 x 13.5 um:
  0.475 A/W at -2.5 V; 5 bandwidth points 71 to 15 GHz. Fab not stated.
- M4B.3: no rows (link paper; filters design values only).
- W2A.1 (1/2): waveguide MUTC-PD 170 GHz; 0.56 A/W (C band inferred). Platform and fab empty.
- Th1G.5: no rows (system paper).
- Th2A.21 (2/10): Er:Si3N4 waveguide amplifier 17.5 cm: off-chip gain > 10 dB at 1550 nm; Psat 12.5 dBm; NF 6.4 dB at
  0 dBm input; Psat > 9 dBm across the C band to 1570 nm; 11.5 dBm output at 10 dBm input; 200 x 5000 nm,
  2.5 x 3 mm2. Facet coupler 6.5 dB per_facet at 1630 nm with 2.5 um MFD lensed fiber. Fab empty.
- Th4A.3 (1/6, fab org_sony_semiconductor_solutions: "our MOCVD reactor / our process fab", all authors Sony):
  850 nm oxide VCSEL ~7.2 / 6.3 mW at 8 mA (25 / 70 C); bandwidth > 40 / 37 / 36 GHz at 25 / 70 / 80 C (criterion and
  bias not stated); mean RIN <= -150 dB/Hz (N=10, 70 C, 8 mA).
- M4J.4: no rows (fiber sensing field trial).

## Judgment calls

J1 membrane devices platform inp_membrane; DML and SEL laser.heterogeneous (SEL on Si substrate, noted). J2 M4D.5
link-level bandwidth and combined power on the laser row with scope in condition. J3 W4E.5 self-heating shift under
tuning_efficiency_pm_per_mw (per mW electrical input, noted). J4 Th3F.4 saturation lower bound from the input-power
ceiling. J5 D72 strictly: fab empty when authors span several orgs or the fabricator is not stated.

## Registry gaps reported

tol_3db_lateral_um / tol_3db_longitudinal_um; beam_divergence_deg; mcef / d_factor; relaxation_oscillation_ghz;
saturation_photocurrent_ma; rf_output_power_dbm; forward_voltage_v; lifetime_years; misalignment_excess_loss_db;
slope_efficiency_w_per_a exists since D77 (sweep W4E.5). No missing orgs.
