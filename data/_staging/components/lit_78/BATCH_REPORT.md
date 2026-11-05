# lit_78 batch report (2026-11-04)

Classes: laser, chip_chip_coupler. 5 papers, 12 components, 80 metric rows. Dry-run: 0 errors. All cached texts match their source rows; gundavarapu2018 carries the arXiv title form (same first author, treated as the same work, as briefed); no correction / erratum file.

| Paper | Components | Metric rows |
|---|---|---|
| gundavarapu2018 | 2 (laser.other, waveguide_platform.straight) | 9 |
| shui2026 | 3 (laser.other, resonator.ring, fiber_chip_coupler.edge) | 22 |
| zhuang2025 | 3 (laser.sil, laser.dfb, resonator.ring) | 18 |
| mnaymneh2018 | 3 (2 waveguide_platform.transition, one design; fiber_chip_coupler.edge) | 20 |
| su2024 | 1 (waveguide_platform.transition) | 11 |

## Values not entered, per paper

### gundavarapu2018
- Q_T / Q_E 28.5 / 63.5 million (p.7 Table 1, p.8): p.7 attributes the cold-cavity Qs to the authors' ref. 26 (D259 / rule 3). Eq. (1) linewidths 1.78 / 5.28 Hz computed from them: same. The p.2 bound on loaded Q (> 28 million) is left out with them.
- No parameter: Brillouin shift 10.93 GHz, gain bandwidth 200 MHz (p.5), L*Aeff 2.07e-12 m3 (p.4), hot-to-cold coupling ratio 0.39 (p.8). On-chip pump 125 mW is a condition; no threshold is stated.
- Geometry of the waveguide (thickness, width) is not stated.

### shui2026
- Optical slope efficiency 2.76 % (p.6, Fig. 3(d)): `slope_efficiency_w_per_a` is W/A; this is W/W for an optically pumped laser.
- Emission FWHM 9.5 pm (p.6): limited by the OSA resolution (D250).
- PL center 1530 nm, lifetime 1.89 ms (p.3, film property); pump-signal overlap > 90 % (p.4, simulated, no parameter).
- 48 C multimode peaks (p.6): in component notes. Temperature "tuning" is a mode hop between about 1529 and 1556 nm, so no `tuning_range_nm`; per-temperature wavelengths are entered.
- Ring radius and width: scale bar only.

### zhuang2025
- White frequency-noise floors 13.4 and 27273 Hz2/Hz (p.4); frequency drift about 0.67 and 4.6 MHz/min (p.5): no parameter.
- Table I other-work rows; thermo-optic coefficient (ref. [33]); HR / AR reflectivities are in text only and in core_material (no laser parameter).
- OSA peak levels in Fig. 2(e, f): plane not stated.
- System results (800 Gb/s, 667 Gb/s, mismatch tolerance, BER): not component metrics. ITLA, LSFL, modulator, receiver: measurement setup (rule 13).
- Taper, 1x2 MMI, thermal phase shifters: mentioned without values; no rows. No DFB-to-Si3N4 coupling loss is stated, so no chip_chip_coupler row.

### mnaymneh2018
- The QD single-photon source has no row: not a laser, and its figures of merit have no parameter (source efficiency 28 %; count rate 417 kHz at Psat; purity 89 % cw and pulsed, 97 % corrected cw, 76 % evanescent pumping; lifetime 1.3 ns; Psat 800 nW; resolution-limited 60 ueV; p.2-3).
- Purity > 99 %, linewidth < 4 ueV (refs. 29, 30): cited.
- Waveguide propagation throughput 69.2 % (Table I): calculated in a supplement that is not cached; length not stated.

### su2024
- Simulated 1-dB tolerance +/- 1.5 um in Y and over +/- 0.5 deg rotation (p.1, p.3, Fig. 2(e, g)): `tol_1db_lateral_um` is not allowed on waveguide_platform (D250 deferred it). In component notes.
- MTP placement accuracy 3 sigma: X 1.19 um, Y 0.90 um (p.3) / 0.91 um (p.1, p.4), 52 dummies (Fig. 4(a)): no parameter.
- Values from refs. [7], [9], [10, 11] (0.1, 2, 1.35 dB/facet): cited. Power overlaps Fig. 2(c, d): design curves, not entered.

## Printed-value conflicts kept with notes (D417)
- shui2026: SMSR 53.3 dB (text) vs about 53.5 dB (Fig. 3(b)); peak 1556.27 nm (text) vs about 1556.37 nm (Fig. 3(b, c, e)); ring wavelength near 1530 nm (text) vs 1542.32-1542.36 nm (Fig. 1(e) axis).
- zhuang2025: RIN below -130 dBc/Hz beyond 1 kHz (text) vs about -123 dBc/Hz at 1 kHz on Fig. 3(b); 15 kHz vs 270 kHz at -20 dB, where the free-running divisor of 20 gives 13.5 kHz. Fig. 4 caption says self-homodyne, the text self-heterodyne.
- gundavarapu2018: S1 / S3 powers coupled to fiber (text) vs on-chip axis label (Fig. 3(a)).
- mnaymneh2018: throughput 1.85 % (text) vs 1.86 % (Table I).

## Judgment calls
1. mnaymneh2018 and su2024 couplers are `waveguide_platform.transition`, not `chip_chip_coupler`: nanowire and printed coupon end up on one chip (rule 10; maeda2023, liu2025 precedents). chip_chip_coupler.evanescent would admit the su2024 tolerance row.
2. su2024 0.1 dB/facet is `author_estimate` + `loss_breakdown`: the subtracted grating-coupler term is unprinted and of unstated origin (D428). D441 kept a similar no-number case `measured`.
3. shui2026 threshold and on-chip output are `author_estimate`: coupled powers rest on "estimated" coupling losses of unstated origin (rule 4; not a D394 case).
4. mnaymneh2018 45.7 % is `measured` (table titled experimental, D167); nader2025 (D418) went the other way for unstated origin.
5. zhuang2025 linewidths 42 Hz / 85.63 kHz `derived` (pi f0 from the measured floor).
6. zhuang2025 fab org_amf on the MRR row only; the assembled laser stays empty (D399 logic, assembly site not stated).
7. Fab from first-person statements with all authors at one org: su2024 SJTU, mnaymneh2018 NRC Canada, on the assembled transition rows only (D399 / D419). D80b could argue for empty.
8. gundavarapu2018 facility org_ucsb_nanofabrication_facility from thanks for sample processing "in" the facility (work performed there, not generic staff thanks). Honeywell (cladding deposition, anneal, thanked on p.9): note only, fab empty.
9. shui2026 q_intrinsic and the loss from it `author_estimate` (D403); FSR 7.12 nm `simulated`.
10. zhuang2025 extinction 4 dB and free-running RIN -141 dBc/Hz, mnaymneh2018 99 % at 20 um: figure reads, `extracted_from_figure`.

## Missing organizations (facility / fab not entered)
- Northwestern Polytechnical University, Xi'an, China (shui2026 p.1).
- Analytical & Testing Center, Northwestern Polytechnical University (shui2026 p.1, p.7 acknowledgment: EBL, ICP, AFM, SEM): facility, would go on all 3 shui2026 rows.

## Registry gaps (skipped value + locator -> proposed definition)
- `optical_slope_efficiency_pct` (laser; unit %): shui2026 2.76 %, p.6 Fig. 3(d). Output power per coupled pump power of an optically pumped laser; plane in condition.
- `frequency_noise_hz2_per_hz` (laser; D431 candidate): zhuang2025 13.4, 27273, p.4 Fig. 3(a). White frequency-noise floor.
- `frequency_drift_mhz_per_min` (laser): zhuang2025 0.67, 4.6, p.5 Fig. 5(b). Free-running drift rate, duration in condition.
- `tol_1db_lateral_um` widened to waveguide_platform.transition, `tol_rotation_deg`: su2024, p.3 Fig. 2(e, g).
- `placement_accuracy_um` (3 sigma; transition, chip_chip_coupler): su2024 1.19 / 0.90, p.3 Fig. 4(a).
- `brillouin_shift_ghz`, `brillouin_gain_bw_mhz` (laser): gundavarapu2018 10.93, 200, p.5.
- Non-laser quantum emitters: `single_photon_purity_pct`, `source_efficiency_pct`, `radiative_lifetime_ns` under a light-source subtype: mnaymneh2018 p.2-3.
