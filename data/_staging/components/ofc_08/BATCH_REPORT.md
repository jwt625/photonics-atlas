# Batch report ofc_08 (OFC 2026, facts only, 2026-10-20)

Transcribed by the coordinator from the batch agent's final report. Dry run: 0 errors; 19 components, 48 metrics from
8 of 11 papers. host_device_ids empty; no e-mail addresses.

## Per paper (components / metrics)

- Tu3C.2 (2/7, fab org_intel: acknowledgment of Intel Fab11x for chip fabrication, p.~3 Sec. 4): 60 um ring FSR
  201 GHz measured, radius 60 um design; 8-ch III-V/Si DFB array: 8 channels, spacing 200 GHz free-running at 50 mA
  (+/-15 GHz in notes), 201 GHz locked to the ring FSR (+/-4 GHz in notes), power variation < 2 dB free-running and
  after VOA equalization. Array first reported in [10]; these are this paper's own measurements.
- Th2A.29 (1/2): QD micro-ring laser threshold < 1 mA, 1309 nm at 10 mA; 25 um radius in notes (radius_um not allowed
  for lasers). Fab empty.
- W1G.5: no rows (system paper).
- Th1D.3 (6/9, fab org_corning_research_and_development, D72): Euler and circular glass fan-outs 0.62 / 0.65 dB
  fiber-to-fiber, 16 channels (1310 nm inferred); facet to SMF-28 Ultra < 0.3 dB per facet; straight waveguide
  0.04 dB/cm (author_estimate); localized-high-delta-n bend 0.0123 dB/cm at R = 6 mm (simulated), min bend radius
  6 mm; standard-delta-n bend design row 15 dB/cm simulated. Pitch / S-bend length not entered (mapping unclear).
- Th3F.7 (3/8): graphene PD on hybrid plasmonic slot 0.583 A/W best at -1 V, 1550 nm, -9 dBm, on-chip; > 110 GHz;
  geometry; slot waveguide metal loss 1750 dB/cm (derived from 0.175 dB/um, cutback); Si-to-slot mode converter
  0.64 dB per_component. Fab empty (ambiguous).
- M4D.3 (3/9): InGaAs PD test structure 3 nA at -5 V ("reverse 5 V"), ~0.6 A/W fiber-referred over C+L; Si 90-deg
  hybrid phase deviation <= 7.5 deg over L band; coherent-receiver PIC 0.13 A/W (mean of 4, 1590 nm), > 0.1 A/W over L,
  > 70 GHz (assembled ICR with TIAs, in condition), footprint 1.2e6 um2, 4 channels. Fab empty.
- W2A.10 (1/4, fab org_imec, 300 mm pilot line): GaAs nano-ridge laser threshold 13 mA CW 25 C, ~1048 nm, > 10 mW
  single-facet (author_estimate: cited coupling efficiency), FIN width 150 nm.
- Th1C.2: no rows (Si Gires-Tournois etalon; no fitting parameter).
- Th2A.6: no rows (non-volatile phase shifter; no fitting parameter).
- Th4A.7 (2/10, unnamed 200 mm fab): Bragg-grating MUX (wdm.bragg_cdc) IL 0.6-0.9 dB (scope unspecified), 1-dB BW
  16-20 nm, crosstalk 25 dB, 4 channels, footprint 64,000 um2 (Table 1) and ~56,000 um2 (text), both entered;
  cascaded-MZI reference IL 0.9-1.0 dB, BW 11-14 nm, crosstalk 15 dB, footprint 880,000 um2. Table "flat-top BW" vs
  text "1-dB bandwidth" flagged.
- W2A.2 (1/1, fab org_fraunhofer_heinrich_hertz_institute, PolyBoard + InP): hybrid InP/polymer DBR laser continuous
  tuning > 4.22 nm at 160 mA, 45 C.

## Judgment calls

Th1D.3 bend-loss coefficient into prop_loss_db_per_cm on bend rows with radius in condition; M4D.3 module bandwidth on
the PIC row (labelled); Tu3C.2 own measurements of a previously reported array entered; W1G.5 DFB as setup equipment.

## Registry gaps reported

Orgs: "ARIM (JPMXP 1224IT0013)" (M4D.3 p.~3 Sec. 5); alias "Intel Fab11x" -> org_intel (Tu3C.2 p.~3 Sec. 4).
Parameters: radius_um for laser; bend_loss_db_per_cm; channel_spacing_error_ghz; responsivity_imbalance_db;
absorber_loss_db_per_um; phase_shift_pi; retention_time_s; dispersion_ps_per_nm; thermal_drift_ghz_per_k.
