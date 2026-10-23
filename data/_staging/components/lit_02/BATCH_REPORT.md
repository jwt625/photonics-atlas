# Batch lit_02 report (distill subagent, 2026-10-22, transcribed by the coordinator)

Dry-run `batch lit_02: +33 components, +221 metrics; errors 0`. No '@', no non-ASCII. Quotes only for heim2025 and
mu2026 (open_license_ok); suda2025 and maeda2023 PDFs are CC but registry says restricted_local_only: facts only.

## Per paper

- heim2025 (5 / 35): ectl (laser.tunable), vernier_ring (resonator.ring), coil_resonator (resonator.other, 10 m),
  sagnac_mirror (reflector.loop_mirror), rsoa_butt (chip_chip_coupler.butt). Not entered: Allan deviation 1.8e-13,
  5 kHz/s drift, FN floors, feedback tolerance -10 dB (D77 rejected), RIN (plot), Table 1 other works. Missing org
  "Honeywell" (p.16 ack, coil fabrication help; registry has only org_honeywell_physical_sciences, not named) -> coil
  fab empty. Calls: ECTL fab org_ucsb (contributions "DB designed and fabricated"); 54.5 nm/W -> 54.5 pm/mW derived;
  ring Q_L 0.65 M (main + caption) vs 0.6 M (Supp. Note 2) noted; coil-locked linewidths on the laser row with lock in
  condition; Sagnac ~75 % author_estimate; 4-5 dB butt coupling and 52 % overlap author_estimate.
- lu2024 (1 / 19): pcw_dfb (laser.dfb). Not entered (no parameter): mode spacing 0.29 nm, grating 400 um, turn-on
  0.74 V, series R 1.8 ohm, thermal R 30 K/W, confinement 3.8 %. Fab not stated. mW/mA -> W/A derived; simulated
  threshold / slope simulated; design kappa 10 /cm simulated.
- mu2026 (6 / 32): ingan_ld_flipchip (laser.heterogeneous), inverse_taper_coupler and taper_coupler
  (chip_chip_coupler.butt), to_phase_shifter, mzi_to_switch (switch_fabric.mzi_mesh), power_tap_dc
  (splitter.directional_coupler, ~1 % author_estimate). Si monitor PD not a row (18 GHz cited ref. 26). Not entered:
  simulated 3-dB tolerances (Table 1), emission FWHM 0.05-0.10 nm (OSA-limited), T0 187 K, underfill +12.6 %, bonding
  heat. Missing org "ams OSRAM International GmbH" (p.1, p.4 Sec. 2, p.15; fabricated the LDs) -> laser fab empty. PIC
  rows org_amf (p.3). Calls: laser.heterogeneous for flip-chip hybrid; on-chip powers / coupling losses derived
  (reference subtraction); mean / std powers per coupler design on the laser row; 3 um facet width as width_nm.
- liang2025 (1 / 9): soa_dfb (laser.soa_dfb); PCE 11 % as wpe_pct; 7 deg SOA tilt not entered; fab not stated.
- maeda2023 (2 / 24): membrane_dr_laser (laser.heterogeneous, inp_membrane), si_inp_taper
  (waveguide_platform.transition, niels2025a precedent). Not entered: 700 K/W, 40/50 Gb/s ER and pJ/bit, simulated
  1-dB tolerance 600 nm (not allowed for waveguide_platform). Fab empty (NTT / Keio / U Tokyo). Calls: transition
  < 0.5 dB simulated from Fig. 2(b); self-heating 0.051 nm/mW in tuning_efficiency_pm_per_mw (D80j) derived.
- billah2018 (4 / 25): pwb_hcsel_si (chip_chip_coupler.photonic_wire_bond), hcsel_dfb (laser.dfb), si_gc_ref
  (fiber_chip_coupler.grating), si_nanowire_wg. PWB1-4 per-bond 0.4-1.3 dB derived (reference subtraction);
  simulated 0.3 / 0.03 dB. Not entered: earlier ~4 dB generation (note), emission angle 83 +/- 1 deg, PWB bend
  radius 40 um (not allowed). Fab empty (KIT / Vanguard / HHI; KNMF funding only, D83e). Measured PWB losses band
  unspecified (laser wavelengths not stated).
- jahed2022 (6 / 34): vcsel_gc_flipchip (chip_chip_coupler.other), input_gc_staircase and output_gc_single_etch
  (fiber_chip_coupler.grating), sm_waveguide, vcsel_850 (laser.vcsel), gaas_pd_vis (photodetector.vertical, vendor
  0.4 A/W specification). Fab org_imec, process BioPIX300; PD fab org_vertically_integrated_systems (alias "VI
  Systems GmbH (VIS)"; paper prints "VI Systems"). Not entered: VCSEL beam 3.8 um / 16 deg and > 20 dB polarization
  suppression (attached to ref. 13, D80i), generic GC FDTD study, per-sample 19.1 / 21.5 dB. Calls: link IL 21.9 /
  17.6 / 20.1 dB device_total on the flip-chip row; output GC 9.2 dB loopback_half; WG 0.3 dB author_estimate.
- mangal2020 (4 / 23): ball_lens_via_interface (micro_optics.other), downward_gc_reflector and
  input_gc_fiber_attached (fiber_chip_coupler.grating, org_imec pilot line), polymer_mm_waveguide. Not entered:
  simulated angular tolerance +/-5 deg, improved grating 2.3 / 1.7 dB (ref. 11), projected < 2 dB. Missing org
  "Centre for Microsystems Technology (CMST), Ghent University and IMEC" (p.1, p.9). Calls: polymer WG fab
  org_ghent_university borderline (D84b); tolerance +/-5 um (p.4) vs +/-6 um (Fig. 6 caption) -> 6 with note; ball
  lens radius 150 um derived.
- suda2025 (1 / 9): polymer_sm_wg_fr4 (waveguide_platform.straight): IL TE 1.31 / TM 1.24 dB fiber_to_fiber n=8,
  power handling > +20 dBm 6 h, near-field mode sizes, core dimensions. PDL, DGD, PER, 4.4 C rise not enterable
  (notes). Fab not stated (Nissan Chemical material supplier, note). Furukawa ELS is test equipment.
- dangel2013 (3 / 11): silicone_wg_on_si 0.031 dB/cm n=12; silicone_wg_flex 0.046-0.050 dB/cm, spectral < 0.05
  dB/cm 760-860 nm and < 0.3 dB/cm 600-1100 nm, bend loss, min bend radius 4 mm; flex_mt_connector
  (fiber_interface.connector) 2.2 dB mean of 48. Missing org "Dow Corning Corporation (DCC)" (p.1, p.2 Sec. II-C,
  p.4 Fig. 7 caption, mask patterning at DCC) -> rigid WG fab empty. Flex WG fab org_ibm_research_zurich (Fig. 7(b)
  "performed at IBM"). Calls: spectral rows sample type not stated (attached to flex with caveat); bend < 0.05 dB
  per 360 deg -> < 0.0125 dB per 90 deg derived; connector wavelength inferred nir_below_o.

## Registry gaps (proposed)

pdl_db and per_db for waveguide_platform (suda2025); dgd_ps (waveguide_platform, fiber_interface,
fiber_chip_coupler); tol_3db_* (chip_chip / fiber_chip couplers; mu2026; D81 deferred); tol_1db_lateral_um for
waveguide_platform.transition (maeda2023); laser thermal_resistance_k_per_w, characteristic_temperature_k,
series_resistance_ohm, mode spacing / fsr_nm, bw_fwhm_nm for laser, feedback tolerance (D77 rejected);
facet_angle_deg (chip_chip_coupler, laser, amplifier); pitch_um for waveguide_platform; min_bend_radius_um for
chip_chip_coupler; temperature rise under optical load; post-reflow loss change.

## Open questions

mu2026 laser.heterogeneous vs laser.other for flip-chip hybrid; dangel2013 org_ibm_research_zurich vs org_ibm for
"IBM"; mangal2020 Ghent fab (D84b) keep or drop.
