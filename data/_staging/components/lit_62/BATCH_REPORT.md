# Batch lit_62 report (distill subagent, 2026-11-02)

Dry-run: `batch lit_62: +31 components, +163 metrics; errors 0` (one WARN on another batch's row, cmp_lit_ni2025b_pimmwc-m18).
Page-1 title check: all 6 texts match their source rows; none is a correction or another paper. zeng2026 `garbled_text_layer`
(pages 21, 22 only): Tables S1 / S2 read from the renders, every other value from clean text. Rows built by one scratchpad spec
script. Renders checked: zeng2026 pp.3, 4, 19, 21, 22; zhao2026 pp.7, 18, 21; yan2020 pp.4, 8, 9, 11; stanton2020 pp.7, 8;
kazama2021 pp.4, 7, 9; ahmadi2022 pp.2, 4.

## Per paper (components / metrics)

- zeng2026 (9 / 40; arXiv v1, no peer-reviewed version in the row): 55 mm Yb:AlOx amplifier (amplifier.rare_earth, al2o3): gain 26.5 dB
  at 1015 nm, 28.6 on-chip / 26.6 off-chip and 18.7 large-signal at 1030 nm, 18.9 pulsed at 1050 nm, 5.2 dB/cm, 80 nm gain
  span, 590 mW (27.71 dBm), 71 % efficiency, NF 3.3 on-chip / 4.3 off-chip. Waveguide 9.7 dB/m (0.097 dB/cm, cutback, 1060 nm).
  3D inverse taper 1.0 dB per facet plus overlap 92.0 / 87.9 % TE / TM. Ring R = 100 um Q0 3.06 M, 14.4 dB/m. DFB laser 8.7 mW,
  SMSR 60.9 dB, 1019.8 nm, FSR 0.17 nm; Bragg mirror 93.9 %, 0.7 nm; cavity Q0 301 k (D396). Supercontinuum chips: facet tapers
  only, Si3N4 6.3 dB and SiO2:Ta2O5 3.7 dB per facet.
  Not entered: Si3N4 and tantala waveguide supercontinuum (no parameter, no other performance); 2.1 dB short-device IL (taper
  widths differ, note); Table S1 / S2 other rows (other works); cross sections, ETU coefficient, lifetime, saturation energy
  and power, pulse energy, peak power (no parameter, in notes).
- zhao2026 (2 / 14; open licence): PPLN SHG 2021 %/W, 64.6 % at 86.09 mW, 45.4 % at 50.93 mW, geometry. Same-process racetrack:
  Q_int 7.98e6 and 0.042 dB/cm, both author_estimate (D403). Not entered: other works' values in the introduction (3 dB/cm,
  0.25 dB/cm etc.), simulated indices (condition text only), roughness and SHG FWHM (no parameter).
- yan2020 (7 / 26): TM and TE MZI isolators, TM and TE circulators, TM racetrack isolator plus its resonator row (D396), TE-TM
  rotator pair (polarization.psr, D404). Not entered: Table 2 other-work rows; 2 dB / 0.3 dB loss budget (notes only, junction
  count not stated); 4 nm drift over 20-70 C and Faraday rotation (no parameter); per-path Table 1 values (component notes;
  range rows kept).
- stanton2020 (7 / 28): 2.9, 6.3, 9.7 mm SHG rows, simulated-optimum design row, waveguide loss (pump, signal, three Fig. 6
  readings), input taper and output facet (measured and simulated). Not entered: Fig. 1 other works, signal FWHM (no parameter),
  Fig. 3 tolerances, bond energy and roughness (notes).
- kazama2021 (4 / 31): OPA module as PSA / PIA (gain 30.6 / 24.7 dB, 68 nm, NF rows), SHG view (about 1200 %/W), ridge waveguide
  (6.4 dB butt, 0.222 dB/cm), SSC facet (2.7 simulated, 0.6 and 0.7 estimated, 1 mm taper, MFD). Not entered: PPLN-1 / PPLN-4
  unit values (see judgment 3); 21.9 dB, 2.1 dB NF and earlier-module values (cited from earlier work, D259).
- ahmadi2022 (2 / 24): 3.25 and 1.2 cm Si Raman amplifiers (amplifier.other): SRS gain 5.5 and 2.6 dB, calculated net gain 0.5 dB
  each, zero-net pump 100 and 60 mW, Fig. 3 readings, SEM geometry. Not entered: see judgment 1; Fig. 6 simulated net gain
  (curves, no printed value for a device).

Stopped on: none. Fab orgs: org_amf (ahmadi2022 only). Facilities: org_center_for_nanoscale_systems (zeng2026 alumina and Si3N4).

## Missing orgs

- MIT.nano, printed "MIT.nano cleanrooms", zeng2026 p.7 Acknowledgments: no registry org or alias (org_mit exists; the owner of a
  named facility is not a facility, so facility_org_ids holds Harvard CNS only).

## Judgment calls for the auditor

1. ahmadi2022: 1.1 dB/cm is attributed to a ring on the same sample (p.4) and to the Q-factor reported in [14] (p.7). Sample
   identity is ambiguous: not entered (D159), and the 4.5-4.6 dB fiber-to-edge loss computed from it is not entered either (rule
   3), so no coupler row. If the same-sample wording wins: straight waveguide row 1.1 dB/cm and edge coupler 4.6 dB per facet
   (author_estimate, 12.7 dB loopback at about 13 dBm, p.7). Net gain rows rest on the same input: author_estimate.
2. ahmadi2022 zero-net-gain pump as pump_threshold_mw (ronn2019 precedent), not gain_db = 0. Fig. 3 readings: bias and configuration
   of the printed 2.6 dB taken from the top traces.
3. kazama2021: the module row is treated as PPLN-3. Values for PPLN-1 (idler generator gain) and PPLN-4 (1.3 W SH from 2.6 W) are in
   notes because the text does not tie those units to the characterized waveguide (D159). The two-stage 50 % would be a derived
   power_conversion_efficiency_pct if the coordinator treats them as one design. Fab left empty ("developed"; D80b).
4. kazama2021 platform `other` (umeki2010 precedent; shimizu2023 merged empty). Optical NFs and electrical NFs `derived` (Eq. 3 and
   reference-EDFA arithmetic); signal wavelength 1550.3 nm read from Fig. 4(a), wavelength_inferred.
5. yan2020: IL `measured` / reference_structure / de_embedded (normalized spectra printed as a number; liu2023 used `derived`,
   lapointe2025 `measured`). Text crosstalk ranges (-15.7 to -32, -25.3 to -30 dB) differ from Table 1 (19.4-34.4, 28.4-33.5 dB): both
   entered with their locators. Fab empty: unnamed foundry; CUMEC only an author affiliation (yan2024 precedent).
6. zeng2026 on-chip gain, pulsed gain, NF and output power `derived` (D166 / D394); efficiency 71 % `measured`, reference plane not
   printed. 26.5 dB ref_plane unspecified. DFB 8.7 mW on-chip `author_estimate`: lensed-fiber correction not printed. Coupler 1.0 dB
   assumed symmetric; paper notes asymmetry (p.20). Bragg 0.7 nm `author_estimate`: origin not stated.
7. stanton2020 simulated W-1 values kept `simulated` after the x 100 conversion to %/W, with the printed value in notes (D256 reads
   `derived`; I kept the simulated origin). 2.9 mm wavelengths read from Fig. 7(b); 6.3 / 9.7 mm rows use the stated 2.0 um pump.
8. zhao2026: 'telecom band' mapped to c_band (cheng2024 precedent). Fig. 5(c)(d) SH peaks sit near 765 nm while the text gives 762.5 nm
   / pump 1525 nm: flagged in notes, 1525 kept. Racetrack bend radius 100 um from the printed sum, `derived`.

## Registry gaps (skipped value + locator + proposed definition)

- frequency_converter bandwidth: stanton2020 148 GHz / 0.5 nm signal FWHM (p.1, p.3, p.9), zhao2026 about 1 nm pump-side sinc2 FWHM
  (p.10). Propose `bw_fwhm_nm` and `bw_fwhm_ghz` allowances for frequency_converter (which wave in condition).
- Pulse amplifier: zeng2026 5.3 nJ output, 14 kW compressed peak (p.4, p.6, p.22). Propose `pulse_energy_nj`, `peak_power_kw` for amplifier.
- Saturation energy: zeng2026 730 nJ calculated (p.12). Propose `saturation_energy_nj` for amplifier.
- Raman: ahmadi2022 60 GHz gain bandwidth (p.3; `bw3db_ghz` is electrical). Propose `gain_bw_ghz` for amplifier. Gain coefficient
  6.2-6.3 cm/GW (p.5) and free-carrier lifetime 0.5 ns at -2.7 V (p.4): `raman_gain_cm_per_gw`, `carrier_lifetime_ns`, waveguide_platform.
- Upper-state lifetime: zeng2026 250 us (p.3, p.18). Propose `upper_state_lifetime_us` for amplifier.
- Supercontinuum: zeng2026 about 600-1700 nm at 610 pJ, dispersive waves 476-644 nm (p.6, p.15). Propose `spectral_span_nm` and
  `pump_pulse_energy_pj` for frequency_converter.other.
- Nonreciprocal thermal: yan2020 drift within 4 nm over 20-70 C (p.9). Propose `thermal_drift_pm_per_k` allowance for nonreciprocal.
