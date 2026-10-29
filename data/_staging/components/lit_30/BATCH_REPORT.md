# Batch lit_30 report (distill subagent, 2026-10-29)

Dry-run `batch lit_30: +36 components, +286 metrics; errors 0`. ASCII only, no e-mail, no quotes beyond a few words (no
source is open_license_ok). Page-1 title / authors checked for all 9 cached texts: all match their source rows. None of
the 9 papers had rows in `data/components/` or another batch. Builder: session scratchpad
`distill_lit_30/build.py` + `p_<paper>.py`.

## Per paper (components / metrics)

- amorim2017 (6 / 26): fs-laser-written fused-silica MZI + Bragg OADM (wdm.bragg_cdc: 0.19 nm 3-dB width, > 30 dB
  intra-channel crosstalk as crosstalk_db, 20 dB adjacent at +/-0.75 nm, ~14 dB port extinction, 4.9 / 3.7 dB
  through / drop fiber_to_fiber, 54 mm, 80 mm bends); BGWs at 40 % and 60 % duty cycle (reflector.bragg: grating
  strength ~31 / ~29 dB as extinction_db, kappa 171 / 161 m^-1 -> 1/cm derived, ~536.1 nm period); waveguide (1.09 dB
  FtF, 0.30 dB PDL, MFD 7.1 / 12.3 um, 0.37 dB/facet calculated and 0.14 dB/cm as author_estimate per D163); DCs
  10 um / 1.48 mm (44/56) and 15 um / 1.77 mm (51/49). Not entered: S-bend loss (Fig. 4 only, "negligible" > 50 mm),
  DC IL (Fig. 7 only), birefringence (figure only), expected 3 dB through loss and ~2 dB radiation-mode loss (general
  statements), BGW excess loss and transition loss (gaps). Fab empty (passive fabrication, no named fabricator); no
  facility.
- sabri2024 (3 / 43): 1x4 SiN RAMZI lattice demux (wdm.cascaded_mzi: 7.12 dB de-embedded, crosstalk > 14 dB whole
  passband, < 0.3 dB non-uniformity, simulated 30 dB crosstalk / extinction, 1576 mW total and 8 per-heater tuning
  powers, ring radii / gaps / coupling lengths, heater geometry); 3-dB MMI (~1 dB each, author_estimate; 163 x 15.5 um);
  SiN waveguide (2 dB/cm measured, cross-section). Not entered: shape factor 0.9 / 0.87 (gap), ring coupling
  coefficients k1-k3 (power vs field not stated). Fab empty: AEPONYX missing (below).
- stanton2017 (2 / 24): 8-channel Si AWG on 500 nm SOI rib (wdm.awg: peak channel loss Lmin..Lmax for the AWG-ring
  extractions Eqs. (6) / (7) / (8) and waveguide normalization (11), all derived de_embedded; mean 3-dB cumulative
  crosstalk 29.08 / 29.09 dB; channel-peak std 138 pm over 3 AWGs; channel spacing 2.0 nm derived from delta-lambda =
  3.0 nm = 3/2 spacing; Table 1 geometry); spiral rib waveguide 70.9 dB/m -> 0.709 dB/cm (OFDR, wavelength inferred).
  Not entered: AWG-ring / UMZI (tau^2 only plotted), Lmin loss contributions, coupling-variation statistics, Rowland
  radius as FPR length. Facility UCSB Nanofabrication Facility (thanked for technical support); fab empty (passive).
- taha2021 (6 / 57): four 4-channel MMI-based AWG designs (L_MMI 80 / 79 / 78 / 77 um; Table IV ranges of channel
  spacing, 3-dB bandwidth, adjacent crosstalk; Design #3 25-GHz-band crosstalk 7.6-11.4 dB and 367 x 67 um2; simulated
  values on Design #2); 4x4 MMI 79 um (simulated 0.66 dB excess, 0.78 dB non-uniformity, geometry) and 80 um (split ~25
  % near 1310 nm). Fab GLOBALFOUNDRIES (silicon fabrication through its MPW university program). Not entered: abstract
  97 GHz (statistic not stated), 0.2 nm channel drift, 79 um measured split (text contradictory), arm lengths (no
  constant delta-L printed).
- zhang2019a (3 / 43): IMOS reflection AWG 8x8 (6.7 dB input 4 / 9.4 dB input 1 de-embedded, crosstalk 10 / 11.4 dB,
  4 nm, FSR 33 nm, 3 dB non-uniformity, footprint); transmission AWG reference (5.6 dB, 11.4 dB, 4 nm, 33 nm); 15-hole
  PhC reflector (simulated > 95 % C-band, > 200 nm span above 90 %; geometry). PCR measurements of 11/8/6-hole
  versions are in ref. [16] (not entered); 1.1 dB R-AWG excess not entered separately. Fab TU/e (IMOS MPW run carried
  out in IPI-TU/e, rule 12 MPW service).
- konoike2020 (3 / 4): only the scaling-model inputs from the authors' "latest fabrication tests": adiabatic
  intersection 0.024 dB (measured), Si waveguide 1.07 dB/cm and 10-um bend 0.0158 dB/180 deg -> 0.0079 dB/90 deg (both
  "assumed", author_estimate). Fab AIST (borderline: "our latest fabrication tests"). All 8x8 PA-SAS results NOT
  entered (D259a, see decision 1). Also not entered: 0.013 dB/90 deg bend (cited [16]), 19 / 38 W power estimates and
  N = 32 path dependence (computed from cited inputs), per-MZI 0.13 / 0.21 dB.
- seok2016 (6 / 32): 64x64 MEMS switch (3.7 dB worst-path on-chip derived from the fit, adjacent-port crosstalk
  > 60 dB, 7 x 7 mm); switch cell (0.47 dB switching loss and 0.026 dB/cell from the fit over 172 cells, 0.025 dB/cell
  from test structures, > 60 dB extinction, simulated > 45 dB, 0.91 / 0.28 us, 0.71 MHz resonance, 125 nm gap);
  vertical adiabatic coupler as waveguide_platform.transition (simulated 0.01 dB, taper geometry); MMI crossing 0.017
  dB measured / 0.011 dB author_estimate; Si rib bus 1.1 dB/cm; GC 6 dB per coupler. Fab UC Berkeley (D83c), facility
  Marvell Nanolab (matches merged seok2019). Not entered: pull-in 42 V / release 24 V, 10^10-cycle endurance (gaps),
  0.13 dB conical-fiber coupling (cited).
- sharma2022 (2 / 21): 1x3 SiN MEMS switch (Table 2 mean ILs for 3 positions with / without gap closer, reference-
  waveguide subtraction -> derived de_embedded; crosstalk > 30 dB; simulated 50 / 100 / 150 us closing times;
  cross-section); SiN waveguide 3.3 dB/cm (process value, author_estimate). Not entered: pull-in 170 / 80 V (gap),
  per-sample Table 2 values, 4.45-6.64 dB span (inconsistent with Table 2), 127 um pitch / 100 um bends / 400 nm tapers
  (not allowed for switch_fabric), MEMS gaps of Table 1. Fab empty: AEPONYX missing.
- testa2018 (5 / 36): IRIS packaged WSS matrix (switch_fabric.wss: ~20 dB, 22 dB and 22.5 dB fiber_to_fiber, 14 dB
  on-chip, > 35 dB isolation, ~6 dB differential path loss, 175 mW EIC heater cells, ~4 us thermal time constant,
  ports / channels / 65 mm2); double-MRR switch element (wdm.mrr: Table I off / on loss, 1-dB width, isolations at
  200-1000+ GHz offsets as crosstalk_db, > 12 nm tuning, FSR 19 nm, <= 9 nm wafer spread); interleaver; 6-channel AWG
  (3-4.5 dB, > 135 GHz 1-dB width, isolations, > 5 nm wafer spread); pigtailed GC (< 4 dB per grating). Fab: PIC
  CEA-Leti ("fabricated in the CEA LETI facilities"); switch row also STMicroelectronics (EIC) and UPV (packaging,
  D399), TU Wien missing. Not entered: interleaver "bandwidth > 150 GHz" (level undefined), +/-75 GHz intra-die MRR
  spread (gap), BER / OSNR system values, EIC TIA / mux power.

## Orgs missing from the registry (3)

- AEPONYX Inc. (fab): sabri2024 p.6 Sec. 4 and p.8 Acknowledgements; sharma2022 p.1 Abstract, p.6 Sec. 3, p.19
  Acknowledgements.
- TIA Super Cleanroom (SCR) of AIST (facility): konoike2020 p.1 (funding note); same org reported by lit_14.
- Technische Universitat Wien (packaging fab): testa2018 p.6 Sec. IV.

## Judgment calls / decisions for the coordinator

1. konoike2020 (D259a): the paper says it analyzes the 8x8 results obtained in its ref. [12] (OFC 2020 Th3B.6, same
   authors). Not entered: FtF 5.7 +/- 0.75 dB over 64 connections at 1.55 um; breakdown fiber-chip ~2.5, waveguiding
   ~0.8, polarization cleaner ~0.6, switch part ~1.8 dB (theory ~1.7); crosstalk < -30 dB over > 90 nm; MZI ON / OFF
   17.4 / 3.88 mW, ~760 mW total (~420 mW ON-only); 112 MZIs; chip 8.5 x 4.5 mm, switch part 3 x 3 mm (all p.4).
   If ruled own-paper data, they go on a switch_fabric.mzi_mesh row (fab AIST, facility TIA SCR).
2. testa2018 MRR switch element classed wdm.mrr (spectral parameters not allowed on switch_fabric); Table I values
   taken as this paper's own (designs in refs [12]-[16]); packaged-switch fab list per D399.
3. zhang2019a fab TU/e as MPW-run provider; stanton2017 facility from a thanks to the facility itself.
4. Isolation at a frequency offset entered as crosstalk_db with the offset in condition (testa2018), not adjacent /
   non-adjacent, because the channel grid seen by each element after interleaving is not stated.

## Registry gaps

- `shape_factor` (wdm, unit 1): 1-dB bandwidth / 10-dB bandwidth. sabri2024 0.9 measured (p.7 Sec. 5, Table 2), 0.87
  simulated (p.5 Sec. 3).
- `actuation_voltage_v` (switch_fabric, phase_shifter): MEMS pull-in / hold / release voltage, type in condition.
  seok2016 42 V pull-in, 24 V release (p.4 Sec. 3, Fig. 5); sharma2022 170 V switching, 80 V gap closing (p.8 Sec.
  4.1).
- `endurance_cycles` widened to switch_fabric: seok2016 10^10 cycles at 100 kHz without degradation (p.5 Sec. 3).
- `prop_loss_db_per_cm` widened to reflector (excess propagation loss of a Bragg grating waveguide over its reference
  waveguide): amorim2017 ~0.3 dB/cm at 60 % duty cycle (p.4 Sec. III-A).
- `transition_loss_db` widened to reflector (waveguide-to-grating transition): amorim2017 0.05 +/- 0.02 dB (p.4).
- `transfer_length_um` (splitter): full power-transfer (coupling) length of a directional coupler. amorim2017 ~0.5 mm
  at 5 um and ~5.6 mm at 15 um separation (p.4 Sec. III-B).
- `wavelength_spread_ghz` (wdm, resonator): spread in frequency. testa2018 MRR channels within +/-75 GHz of nominal
  intra-die (p.4 Sec. II, Fig. 6).
- switch_fabric geometry: `pitch_um`, `min_bend_radius_um`, `tip_width_nm`, `taper_length_um`. sharma2022 127 um
  output pitch, 100 um bends, 400 nm / 20 um inverted tapers at the MEMS air gaps (p.3 Sec. 2.1).
