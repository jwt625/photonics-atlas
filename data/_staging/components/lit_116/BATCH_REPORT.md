# lit_116 batch report (2026-11-08)

All five cached texts match their source rows (page-1 title); none is a correction, an erratum or another paper. Figure values were checked on the cached `page_NN.png` renders (xie2017 p.9; song2013 p.5, p.7 (plus `img_p07_13.png`), p.8; suzuki2014 p.5; suzuki2015 p.6; shi2013 p.13-15). Dry-run: +19 components, +133 metrics, 0 errors; the one warning (ni2025b m18 / m4) is on an existing merged row, not from this batch. Helper script: scratchpad `lit_116/gen.py` (not in the repo).

| paper | components | metrics |
|---|---|---|
| xie2017 | 1 (switch_fabric.wss) | 7 |
| song2013 | 4 (switch_fabric.other 2; resonator.ring 1; fiber_chip_coupler.edge 1) | 33 |
| suzuki2014 | 5 (switch_fabric.mzi_mesh 1; switch_fabric.other 1; crossing.other 1; fiber_chip_coupler.edge 1; waveguide_platform.straight 1) | 27 |
| suzuki2015 | 6 (switch_fabric.other 4; phase_shifter.thermo_optic 1; polarization.pbs 1) | 30 |
| shi2013 | 3 (wdm.bragg_cdc 2, of which 1 design; resonator.bragg 1) | 36 |

## Fab / facility orgs

- xie2017: fab empty. No fabrication / assembly statement; authors at HUST (WNLO) and WRI (D80b). Free-space LCOS WSS with fiber I/O stays in scope (D424), platform `other`.
- song2013: fab empty. "we design and implement" with a CMOS-compatible process (p.3 Sec. 2.1); authors at IME A*STAR, first author also at Jilin University: no fabrication sentence naming an org (D80b, D395). `org_astar_ime` exists if the coordinator reads this as the authors' own process (D84a).
- suzuki2014: fab empty. Passive "was fabricated by using e-beam lithography and CMOS-compatible process" (p.2 Sec. 2); the acknowledgment (p.8) thanks two named persons for technical assistance in device fabrication without naming their org (D84b needs the org). All authors at AIST.
- suzuki2015: fab empty, same pattern (passive, p.4 Sec. 3; one named person thanked for fabrication assistance, p.7).
- shi2013: fab empty in the rows, but the paper names the fabricator: "fabricated by BAE Systems via the OpSIS foundry service" (p.10 Sec. 6.1). Neither org is in `organizations.csv` / `org_aliases.csv`. `process_name` "OpSIS foundry service (BAE Systems)" on the two fabricated rows.
- No facility acknowledged in any paper.

Missing orgs (for the org round):

| name as printed | paper | locator | role |
|---|---|---|---|
| BAE Systems | shi2013 | p.10 Sec. 6.1 | fab (foundry) |
| OpSIS foundry service | shi2013 | p.10 Sec. 6.1 | fab (MPW access provider, D398; already queued from D458) |

Once both exist, `cmp_lit_shi2013_cdc_uniform` and `cmp_lit_shi2013_cdc_phase_shifted` take both as fab (not the design row).

## Not entered, and why

xie2017
- Attenuation tuning range up to 35 dB (p.1, p.9 Fig. 5(d)): no parameter (gap below).
- Bandwidth step 6.25 GHz (p.9 Fig. 5(b); p.3 "less than 7 GHz"): no parameter (gap).
- 0.5-to-10 dB passband roll-off 16.3 GHz (p.9): no parameter (gap).
- 28 / 40.5 GHz widths and 14.5 GHz roll-off of ref. [19] (p.9): cited (rule 3).
- 3-dB widths in nm of the switched channels (p.9-13, Figs. 6-13) and the attenuation values set in Figs. 7 / 11: operating settings; `bw_3db_nm` is not allowed for switch_fabric anyway.
- 10 x 20 extension, 2 deg deflection, 0.7 / 1.4 / 0.5 / 1.9 dB extra-IL estimates (p.6-7): projections.
- Per-port IL values (12, p.8): entered as one range row (8.4-12.5 dB) with the per-port list in component notes.
- LCOS chip specification (Table 1): purchased part, vendor not named; lens focal lengths and beam waists are design values without a switch_fabric parameter.

song2013
- 1-dB bandwidth about 1.3 nm (160 GHz) (p.5 Fig. 4(b), abstract): no 1-dB width parameter on switch_fabric (gap). The 3-dB width is entered as `bw_3db_ghz` 200 (printed in GHz).
- "Transmission loss of waveguide only ~0.4 dB" (p.5): reads either as the reference-waveguide loss or as the switch excess loss over the reference; not entered (D159), noted on the switch and edge-coupler rows.
- Wavelength tolerance +/-80 GHz, temperature tolerance +/-6 deg C (p.5, p.8): author estimates from the 1-dB width, no parameter.
- +/-10 mW electrical tolerance (p.6 Fig. 6), triangle-drive rise / fall 6.5 / 5.5 us (p.7 Fig. 8, drive-limited), thermo-optic coefficient 2.84e-4 per deg C (p.7, computed; no parameter).
- Summed switching times (TO about 7 us, EO about 0.7 ns): individual edges entered instead.
- Theoretical 1-dB / 3-dB widths 0.4 / 0.5 FSR and the 8 nm / 20 nm FSR example (p.5): ref. [14] (rule 3).
- Edge coupler: per-coupler loss not derived (the waveguide term is ambiguous, see above).

suzuki2014
- Switch-to-switch variation of the minimum-crosstalk wavelength about 5 nm (p.6): `wavelength_spread_nm` not allowed for switch_fabric (gap).
- Ideal cascade crosstalk -29 dB (p.6): computed from the element values, not a device measurement.
- 43-Gbps QPSK BER (no significant penalty) and EVM about 13.4 % (p.7-8): no parameter.
- Footprint comparisons (1/550, 1/4) and the -25 dB thick-rib value (p.3): cited (rule 3).
- Heater power, switching time: not stated.

suzuki2015
- Transmission bandwidth 3.1 nm for a 30-dB extinction ratio (p.6): stated after the three-design comparison without naming the device (D159); in the 50:50 row notes.
- Cross-state heater powers per design (Fig. 8 bottom: 18.7 / 57.7, 0.32 / 40.6, 17.3 / 55.6 mW): operating points, in the extinction-row conditions.
- Simulated curves (Figs. 3-4) and the +/-100 nm fabrication-error mapping (p.3): simulation, no device value.
- TE / TM coupling-length ratio about 8.6 (p.6): no parameter.
- Silicon intersection crosstalk about -40 dB (p.5): cited refs. [12-14].

shi2013
- Bandwidth between the first two nulls beside lambda_D about 3.8 nm (predicted 4.4 nm) (p.13): no null-to-null width parameter (gap).
- Tuning coefficient -0.73 nm/mA (p.14, Fig. 10(b)): no per-current tuning parameter for resonator (gap).
- Small-signal modulation 3-dB bandwidth 90 MHz (p.15, Fig. 10(d)): no bandwidth parameter on resonator (gap).
- Photon-lifetime-limited bandwidth over 25 GHz (p.16): estimate from the Q range.
- Corrugation amplitudes 50 / 30 nm and 50 % duty cycle (p.8): no parameter on wdm / resonator (gap); in notes / condition.
- Simulated spectra (Figs. 6-7, 5 dB/cm assumed loss) and mode-transition coefficients k_a1 ... k_b2 (Table 1): model inputs, no device metric.
- Fiber grating couplers (ref. [33]): used for normalization, no performance printed.

## Judgment calls

1. suzuki2015 device identity: the 50.4 dB device of Fig. 7(b) is assigned to the 50:50 design because its PS1 label (0.32 mW) equals the Fig. 8(b) cross-state PS1 power; the Sec. 4 values that describe that device (cross-port 50 dB, about 0.5 dB on-chip loss, about 30 mW switching power, about 10 us switching time) go on the same row. If the coordinator reads this as D159-ambiguous, move those five rows to notes.
2. suzuki2015 three DC designs (coupling length 2.5 / 3.5 / 4.5 um) are three rows (rule 9), each with its Fig. 8 extinction annotation (46 / 50 / 48 dB) entered as `measured` (printed figure annotations, no axis reading).
3. song2013 TO switch rise / fall times (4.3 / 3.0 us at 1599.2 nm, 3.2 / 3.7 us at 1600.8 nm) are printed figure annotations in Fig. 7; the rise / fall assignment follows the edge direction of each trace, consistent with the text's "changed in the opposite way" and the about 7 us sums. Basis `measured`.
4. song2013 ring metrics (FSR, ng, thermal drift, heater tuning efficiency) sit on a `resonator.ring` row of the same physical device (D396), because `thermal_drift_pm_per_k`, `fsr_nm` and `tuning_efficiency_pm_per_mw` are not allowed on switch_fabric. The tuning efficiency is the passband-centre shift per heater mW (condition).
5. song2013 / suzuki2015 "switching power" -> `power_consumption_w` (derived mW -> W), "switching time" (definition not stated) -> `rise_time_us` (precedents in merged rows).
6. suzuki2014 on-chip loss 6.5 dB, PILOSS 4.7 dB, per-element 0.5 / 0.2 dB and 3.6 dB/facet are `author_estimate` (rest on the 3.2 dB/cm reference-waveguide loss of unstated origin, and for the elements on the assumed L_MZ = 3 L_int). The measured fiber-to-fiber mean is entered as 13.7 dB `derived` (6.5 + 2 x 3.6 as labelled in Fig. 5). Crosstalk statistics are `derived` (computed from measured leak / main powers).
7. suzuki2014 element rows: the test MZ switch is `switch_fabric.other` (D158, standalone test element); the DC intersection is `crossing.other`. The estimated per-element losses for the MZ switches / intersections inside the matrix go on these rows (same design), with notes.
8. suzuki2015 on-chip loss about 0.5 dB `author_estimate` (coupling-loss subtraction method not stated); on-chip PBS 20 dB `author_estimate` (budget term of an estimated total).
9. shi2013 phase-shifted contra-DC classed `resonator.bragg` (single 4-port resonator characterized as a device, not a channel filter in a WDM path; D400 analogue); uniform and apodized contra-DCs are `wdm.bragg_cdc`. Table 1 kappas: fit values `derived` (model fit of measured spectra, m-1 -> cm-1), computed values `simulated`; all on the uniform row. Q about 7,000 `derived` (printed "corresponding to" the 0.2 nm width).
10. xie2017 3-dB bandwidth tuning range entered as one `bw_3db_ghz` range row 25-5000 GHz (printed range; Fig. 5(c) shows settings up to 575 GHz), plus the 22.5 / 42 GHz widths at 50 GHz spacing.

## Registry gaps (skipped value + locator + proposed definition)

| proposed parameter | classes | skipped value | definition |
|---|---|---|---|
| `attenuation_range_db` | switch_fabric | xie2017 35 dB (p.9 Fig. 5(d)) | maximum settable per-channel attenuation of a WSS / VOA function, positive dB |
| `bw_step_ghz` | switch_fabric, wdm | xie2017 6.25 GHz (p.9 Fig. 5(b)) | passband-width / centre setting granularity of a flexible-grid filter |
| `passband_rolloff_ghz` | switch_fabric, wdm | xie2017 16.3 GHz (p.9) | frequency span between two stated attenuation levels of the passband edge (levels in condition) |
| `bw_1db_ghz` (extend) | switch_fabric | song2013 160 GHz (p.5 Fig. 4(b)) | add switch_fabric to the existing parameter |
| `bw_3db_nm` / `bw_1db_nm` (extend) | switch_fabric | song2013 1.6 / 1.3 nm (p.5); xie2017 channel widths | add switch_fabric (already raised for ikeda2020) |
| `wavelength_spread_nm` (extend) | switch_fabric | suzuki2014 about 5 nm (p.6) | add switch_fabric (spread of the element minimum-crosstalk wavelength) |
| `tuning_efficiency_pm_per_ma` | resonator, wdm, phase_shifter | shi2013 -0.73 nm/mA (p.14 Fig. 10(b)) | resonance shift per mA of injected current (sign as printed) |
| `bw3db_ghz` (extend) or `mod_bw3db_mhz` | resonator | shi2013 90 MHz (p.15 Fig. 10(d)) | small-signal modulation 3-dB bandwidth of an electrically tuned resonator |
| `bw_null_nm` | wdm, reflector | shi2013 about 3.8 nm (p.13) | full width between the first nulls beside the passband / stopband |
| `fill_factor` (extend), `corrugation_amplitude_nm` | wdm, resonator | shi2013 50 % duty, 50 / 30 nm (p.8) | grating duty cycle; sidewall corrugation amplitude per waveguide (waveguide in condition) |
| `thermo_optic_coefficient_per_k` | resonator, waveguide_platform | song2013 2.84e-4 per deg C (p.7) | effective-index thermo-optic coefficient dn_eff/dT (computed / measured as stated) |

## Coordinator questions

1. suzuki2015 device identification (judgment call 1): accept the 50:50 assignment, or move the five rows to notes (D159)?
2. song2013 fab: leave empty (no sentence naming the fabricator) or `org_astar_ime` under D84a ("we design and implement" with a CMOS-compatible process, all but one author at IME)?
3. suzuki2014 / suzuki2015: the fabrication-assistance thanks name persons but no org; with all authors at AIST, does D84b apply (fab `org_national_institute_of_advanced_industrial_science_and_technology`) or stay empty?
4. shi2013: add BAE Systems and OpSIS in the org round, then a fix batch sets fab on the two fabricated rows.
