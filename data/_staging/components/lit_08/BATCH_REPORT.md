# Batch lit_08 report (distill subagent, 2026-10-23, condensed by the coordinator)

Dry-run `batch lit_08: +36 components, +246 metrics; errors 0`. ASCII, no "@". Quotes: none (only koninck2025 is
open_license_ok). Unit conversions derived with printed values in notes (D157 / D256). Not yet audited or merged (paused).

## Per paper (components / metrics)

- jafarlou2026 (2 / 19): cpmll and cmll2 (laser.comb, inp): threshold, power, repetition rate, jitter, Lorentzian
  linewidth, pulse width, far-field FWHM, length. Fab empty (passive; HHI authors, D80b). Not entered: RF linewidth, rep-rate
  tuning, phase noise, calculated peak power, spectral widths (criterion), cited SA values. CMLL-2 far field from
  "identical" statement.
- keyvaninia2013 (3 / 28): ring tunable laser (laser.heterogeneous), racetrack filter (resonator.ring), front DBR
  (reflector.bragg, ~50 % author_estimate). Fab org_cea_leti (Si circuit, p.4). Two cleave configurations on one laser row
  (condition); some values "configuration not stated". Not entered: SMSR abstract, 20 ohm heater, back DBR, taper geometry.
- koninck2025 (5 / 35): nano-ridge lasers laser.other on iii_v_on_si_epi, fab org_imec: two cleaved die-level rows, three
  etched-facet wafer-level rows (power / slope / WPE author_estimate: cited PD responsivity + simulated coupling;
  thresholds measured); 2 mm row T1, pm/K, SMSR, 55 C values. Conflicts noted (4.5 vs 4.1 mA; Fig. 3 device attribution;
  6.1 mA vs 7.1 mA minimum). Earlier OFC W2A.10 nano-ridge row used platform gaas (consistency).
- nie2024 (1 / 16): mp_mwl laser.soa_dfb (8 channels, 100 GHz, SMSR, > 15 mW, RIN, pm/K, spacing fit, geometry). Fab empty.
- tran2022 (6 / 32): FP lasers (two rows, D159), Vernier tunable laser, SOA, PD, SiN waveguide. Fab org_nexus_photonics,
  facility UCSB nanofab. EO-atlas candidate: GaAs phase shifter Vpi 2.4 V, MZM ER at 1060 nm.
- vaskasi2022 (3 / 22): 180 um DFB laser.heterogeneous (thresholds, power, kappa derived / simulated, WPE, linewidths, RIN);
  III-V/Si taper transition > 90 % author_estimate; output GC 9 dB. Fab empty.
- sun2011 (1 / 9): cantilever vertical coupler chip_chip_coupler.other (2.5 TE / 1.1 TM dB per_interface, D167), geometry.
- yu2023 (2 / 15): freeform reflector micro_optics.other (0.5 dB loopback_half derived, 1-dB bandwidth > 300 nm,
  tolerances, simulated, geometry); PCF design row (simulated). Fab org_mit + org_aim_photonics +
  org_research_foundation_for_the_state_university_of_new_york (D80b; question below).
- zhang2024a (6 / 31): four 45 deg mirror rows micro_optics.vertical_taper (smoothed / untreated, upper / lower; Table 1
  ranges derived), two polymer waveguide rows. Fab empty.
- fowler2025 (7 / 39): 905 nm tapered laser (fab III-V Lab), laser-OPA butt coupler (~8 dB derived, tolerances), 24-ch OPA
  free_space_emitter.other (steering 30 deg, divergence, 0.6 deg author_estimate per D80i), Table 1 parts (TiN phase
  shifter, SiN waveguide, star combiner, output GC). PIC fab org_cea_leti (D84a).

## Orgs missing

None (all printed fabricators resolved).

## Registry gaps proposed

laser: rf_linewidth_hz, peak_power_w, mode_hop_free_tuning_ghz, max_operating_temperature_k, heater_resistance_ohm,
facet reflectivity; chip_chip_coupler wdl_db; micro_optics tip_width_nm; length-normalized series resistance.

## Open questions

1. keyvaninia2013 one laser row with cleave configuration in condition vs two rows.
2. zhang2024a vertical_taper vs other for 45 deg mirrors.
3. yu2023 three fab orgs under D80b.
