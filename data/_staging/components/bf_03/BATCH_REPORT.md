# Batch report bf_03 (2026-10-20)

Transcribed by the coordinator. Dry-run 0 errors: 12 components, 30 metrics.

- nelan2022 (2/2): facet fiber coupler 4.44 dB per facet author_estimate (origin not stated); TO bias heater P_pi 92 mW (1550 nm inferred; held only in EO notes). Not entered: 0.64 dB/cm (EO column), 2.02 dB fiber-array alignment loss (setup term), 1x2 MMI and crossing (prior work / no number), simulated electrode absorption, 2x2 MMI geometry-only (1.4 % splitting difference is simulated, no parameter; transfer-matrix fit inputs).
- montifiore2026 (2/4): rings c (493 nm) and d (780 nm): q_intrinsic 3.4 M / 1.9 M, radius 750 um. Not entered: Q_L and loss (EO columns), notch ER 18.7 / 12.1 dB (modulator ER), FWHM 324 / 539 MHz (no MHz-linewidth parameter).
- lin2026b (0): review; all values cited.
- porto2026 (2/6, fab org_nokia): DFB array (SMSR > 50 dB, n = 4, 60 C; 4 channels); SOA (NF 6.5 dB typical; +5 dBm fiber-coupled per channel n = 8; gain 6.9-10.6 dB and 1-dB psat_in 3.1-5.8 dBm over 40-160 mA from Fig. 2(a)). Not entered: integrated RIN 0.4 % (no parameter), -20 dBm shuttering, OSFP 2.8-3.0 dBm (module), MMI tap and SSC (no numbers).
- shamsansari2021 (3/7, facility CNS): flip-chip DFB (laser.heterogeneous; 60 mW on-chip derived, ~25 mW after the MZI author_estimate, linewidth < 1 MHz); DFB-TFLN butt coupler ~5 dB per_interface author_estimate, horn width 8.2 um, sidewall ~85 deg (SEM); output facet into an NA 0.4 lens 4.8 dB measured (fiber_chip_coupler.edge; no host). Band unspecified (no wavelength stated). Not entered: ~500 nm minimum gap (gap_nm not allowed for chip_chip_coupler), simulated curves, pre-integration laser power.
- xu2026a (0): GCs and MMI without numbers.
- rahman2025 (2/5, fab org_ligentec): SiN1 ring (Q_L ~1.2 M, 0.2 dB/cm ring_extraction derived, FSR 150 GHz design_target (design vs measured not stated), width 1.7 um); SiN2 spirals 0.3-1.0 dB/cm at 1560 nm (cutback). Hosts all three EOM rows. Not entered: 1 dB per facet EC (prior / unpublished), transitions and MMI (no data).
- park2026 (0): PPLN SHG section has no registry class; MMIs no numbers; PD setup equipment.
- tan2024 (0): ring is the modulator; GCs no number.
- li2025a (1/6): apodized slow-light Bragg waveguide (resonator.bragg): ~6 dB/cm excess over a straight reference (from 0.6 dB/mm, derived, cutback Np 10/50/80, C-band inferred), 3-dB BW ~6 nm (1550.3-1556.6), simulated 3 dB/cm and 5.5 nm, N 40, w0 600 nm. Fab only in the supplement (not read).

Not entered as fabricators: NanoLN (wafer), Freedom Photonics (disclosure only).
Gaps: linewidth_mhz; rin_integrated_pct; shutter_extinction_db; split_imbalance_pct; class frequency_converter (ppln_shg; shg_efficiency_pct_per_w, poling_period_um); waveguide_platform.slow_light; gap_nm for chip_chip_coupler.
