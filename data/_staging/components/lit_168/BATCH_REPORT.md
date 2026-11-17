# lit_168 batch report

Distilled 2026-11-16. Papers: lit:guo2021, lit:liu2022d, lit:kobayashi2014, lit:fan2016 (all hybrid III-V / external-cavity tunable lasers; cited in benchmark tables). Cached texts match their source rows (page-1 titles checked); no garbled text layer, no correction-only files. `merge_component_staging.py --dry-run`: +16 components, +66 metrics, 0 errors.

Totals: 16 components, 66 metric rows.

## lit:guo2021 (4 components / 25 metrics)

Thermally tuned III-V/Si3N4 ECL on 800 nm Si3N4 (IEEE Photonics J. 2021).

- `cmp_lit_guo2021_ecl` (laser.tunable, other; 12 rows): threshold about 53 mA, about 34 mW at about 500 mA (20 C) and about 17 mW at 60 C (Fig. 5(b) read, `extracted_from_figure`), tuning 58.5 nm (1516.5-1575 nm), SMSR > 70 dB, intrinsic linewidth 2530 Hz (derived, 1537 nm, 254 mA) and 3 kHz design (simulated), longitudinal-mode spacing 4.5 GHz measured / 5.4 GHz simulated, 0.24 nm/mW tuning efficiency, 240 mW per Vernier FSR, RSOA length 1.5 mm.
- `cmp_lit_guo2021_vernier_mrrs` (resonator.ring, sin; 4 rows): Vernier FSR 60 nm (simulated), power coupling 7 % (design), 1 um x 800 nm.
- `cmp_lit_guo2021_heater_ps` (phase_shifter.thermo_optic, sin; 8 rows): P_pi about 122 mW simulated, MRR pi power 120 mW (Table 1, derived as half of the measured 240 mW per 2 pi), 10-90 % rise / fall about 47 us (simulated), heater gap 1.7 um, under-cladding 4 um, waveguide geometry.
- `cmp_lit_guo2021_rsoa_sin_butt` (chip_chip_coupler.butt, sin; 1 row): about 2 dB coupling loss per interface (author_estimate, origin not stated).

Not entered: wavelength switching times 24.1 us (heating) / 60.7 us (cooling) (no laser parameter); FMCW sweep range 2.68 GHz at 10 kHz and 1.5 GHz at 20 kHz (no parameter); OSNR 75 / 70 / 72 dB (no parameter); white frequency-noise level 800 Hz2/Hz and kf / kr fit constants; confinement factor 87 % (simulated, no parameter); MRR circumferences 565 / 583 um (shape not stated, no radius); Si3N4 waveguide row (no loss value given, so no row: geometry only); RSOA HR reflectivity about 90 % (no row for the RSOA: no performance metric of its own); Table 1 values of other works (rule 3).

## lit:liu2022d (5 components / 21 metrics)

Hybrid integrated FMCW laser with synchronous tuning (JLT 2022), same group as guo2021, different device (0.5 mm RSOA, power coupling 0.052).

- `cmp_lit_liu2022d_ecl` (laser.tunable, other; 9 rows): 22.5 mW fiber-coupled at 179 mA (1549 nm, 20 C), threshold about 30 mA, tuning 56 nm (1522-1578 nm), best SMSR 73.1 dB, intrinsic linewidth 2900 Hz and integral linewidth 1.12 MHz (both derived, unit conversion), RSOA length 0.5 mm, RSOA spot size 4.5 x 3.5 um (`specification`, part property as stated, chen2023 precedent).
- `cmp_lit_liu2022d_vernier_mrrs` (resonator.ring, sin; 4 rows): Vernier FSR about 60 nm and kappa2 0.052 (author_estimate, design), geometry.
- `cmp_lit_liu2022d_phase_shifter` (phase_shifter.thermo_optic, sin; 3 rows): P_pi about 124 mW and response time about 47 us (author_estimate: no citation, no measurement shown), length 0.75 mm.
- `cmp_lit_liu2022d_sin_wg` (waveguide_platform.straight, sin; 4 rows): about 0.2 dB/cm and group index 2.117 (author_estimate, origin not stated), 1 um x 800 nm.
- `cmp_lit_liu2022d_rsoa_sin_butt` (chip_chip_coupler.butt, sin; 1 row): about 2 dB inter-chip insertion loss (author_estimate).

Fab: "The Si3N4 chip ... was fabricated in the multi-project wafer (MPW) process by LIGENTEC" (p.2 Sec. II.A) -> `org_ligentec`, `process_name` "LIGENTEC MPW" on the three Si3N4-chip rows (rings, phase shifter, waveguide). Laser and butt-coupling rows fab empty (assembly / RSOA maker not named; D515, D450).

Not entered (no parameter): mode-hop-free continuous sweep 56 GHz, phase-shifter-only 6.5 GHz, FMCW chirp bandwidth 7.96 / 7.68 GHz and chirp rate 15.36 GHz/ms, linearity R 99.96 % and 1 - r2 1.02e-7 (Table I), tuning-power ratios 1.077 / 4.31 (measured) and 1.039 / 6.35 (calculated), mode-hop-free TEC window 17.5-20.5 C, output fluctuation within 2 dB, white frequency-noise level 900 Hz2/Hz, effective index 1.74, calculated round-trip length 32.1 mm and estimated round-trip loss about 0.96 dB, length enhancement factor 18.7, ranging resolutions (system results). Cited: tuning speed up to 25 kHz (ref. [25]); earlier FMCW result 99.7 % / 1.5 GHz (ref. [24]); Table II rows of other works.

## lit:kobayashi2014 (6 components / 13 metrics)

SHREC Si-wire ring-filter external-cavity tunable laser with hybrid booster SOA (NEC, JLT 2015 issue; paper dated 2014).

- `cmp_lit_kobayashi2014_shrec_laser` (laser.tunable, other; 7 rows): tuning 65 nm (1510-1575 nm, 25 C), 160 mW chip output (booster 650 mA), > 100 mW fiber-coupled over the C band (module, `ref_plane fiber`), typical module slope efficiency 0.2 W/A vs booster current, SMSR > 45 dB, linewidth < 15 kHz (derived, kHz -> Hz), < 70 mW heater power per ring for the full range.
- `cmp_lit_kobayashi2014_si_wire_wg` (waveguide_platform.straight, soi; 1 row): < 0.5 dB/cm over the C band by cutback (measured; paper says "estimated from" length series).
- `cmp_lit_kobayashi2014_ring_filter` (resonator.ring, soi; 2 rows): FSR about 300 GHz and coupling about 0.25 (design, author_estimate).
- `cmp_lit_kobayashi2014_loop_reflector` (reflector.loop_mirror, soi; 1 row): reflectivity at least 90 % (author_estimate, design statement).
- `cmp_lit_kobayashi2014_gain_si_butt` (chip_chip_coupler.butt, soi; 1 row): at most 1.0 dB per interface incl. misalignment, spot mismatch and gap (author_estimate; the paper says "can be estimated").
- `cmp_lit_kobayashi2014_module_fiber_coupling` (fiber_chip_coupler.other, platform empty; 1 row): module fiber coupling loss < 2.0 dB (measured per D167).

Not entered: passive-alignment placement accuracy (57 chips, std 0.1 um, 3 sigma < 0.3 um; no parameter); misalignment-only loss < 0.2 dB (Fig. 8, kept in notes, partial term); Fig. 5 loss spectrum beyond the text bound (notes); designed 65 nm range (equals the measured row); Fig. 4 modal gain difference (no parameter); booster SOA and gain chip as rows (no own performance metric). Ref. [13] 2.4 dB/cm and ref. [17] comparison not entered (rule 3).

## lit:fan2016 (1 component / 7 metrics)

Optically integrated InP-Si3N4 hybrid laser (2-page IEEE Summer Topicals paper).

- `cmp_lit_fan2016_hybrid_laser` (laser.tunable, other; 7 rows): about 1.7 mW fiber-coupled at 200 mA, threshold 35 mA, tuning 43 nm, narrowest linewidth 300 kHz (best) and < 1 MHz across the range (both derived), typical SMSR 35-40 dB, RIN < -135 dBc/Hz (0-30 GHz).

Not entered: tuning endpoints (not printed; band `cl_band` inferred from "including the entire telecom C-band" and Fig. 2, noted); RIN peaks at 9.6 / 11 GHz; output fiber MFD 6 um (fiber spec, no coupler row since no coupling value); earlier 46.3 nm two-mount laser (refs. [6], [7], rule 3); Si3N4 losses 0.001-0.1 dB/cm (refs. [8], [9]); 90 % mode-mismatch loss (ref. [6]).

## Judgment calls

1. guo2021 SMSR > 70 dB entered `measured` with the OSNR basis in condition: the paper infers the SMSR bound from OSNR traces with no visible side modes.
2. guo2021 Table 1 "MRR pi-phase-shift power" 120 mW entered on the heater row as `derived` (halving of the measured 240 mW per 2 pi, D80a) rather than `measured`.
3. One phase_shifter row per paper for the heater cross-section; guo2021 uses it for both the MRR heaters and the phase section (Fig. 1(a) inset). The 240 mW per Vernier FSR and the 0.24 nm/mW stay on the laser row (lasing-wavelength response).
4. liu2022d P_pi about 124 mW and response time about 47 us are uncited but match the same group's guo2021 simulated values (122 mW, 47 us) for the same cross-section; kept as `author_estimate` (origin not stated, D80i borderline). An auditor may prefer to drop them under D259 if the restatement is judged clear.
5. liu2022d "optimum SMSR of 73.1 dB ... over the whole tuning range": statistic `best` with the ambiguity in notes.
6. kobayashi2014 fiber-coupled > 100 mW kept `measured` (Fig. 12 fiber-coupled L-I curve crosses 100 mW), although the p.4 sentence opens with "Therefore" after the chip power and slope.
7. kobayashi2014 module fiber coupling classed `fiber_chip_coupler.other` with platform empty (booster-SOA substrate and optics not stated, D422).
8. Ring rows are `resonator.ring` (intracavity filters, D400), one row per ring pair (fan2025a / fan2020 precedent).
9. All four papers: no facility statements; fab empty except LIGENTEC on the liu2022d Si3N4-chip rows. guo2021 has a LIGENTEC co-author but no fabrication sentence (D80b).

## Missing fab / facility orgs

None. `org_ligentec` is in the registry. No other org is named for fabrication or as a facility in these four papers.

## Registry gaps (skipped value + locator + proposed definition)

1. `wavelength_switching_time_us` (laser): time for the lasing wavelength to settle after a channel-switch step, criterion (e.g. 90 % / 10 % of the filtered new / old mode) in condition. guo2021 24.1 us (heating) / 60.7 us (cooling), p.9 Sec. 4.2, Fig. 9(b-c).
2. `chirp_bandwidth_ghz` (laser): optical frequency excursion of a frequency-modulated laser at the stated modulation rate and drive (actuator in condition). guo2021 2.68 GHz at 10 kHz / 1.5 GHz at 20 kHz, p.10 Fig. 10(c); liu2022d 7.68 GHz at 1 kHz (linearized; 7.96 GHz before), 1.2 / 3.3 GHz single-actuator, p.7-8 Table I.
3. `mode_hop_free_tuning_ghz` (laser): continuous (mode-hop-free) static frequency tuning range. liu2022d 56 GHz synchronous and 6.5 GHz phase-shifter only, p.5-6 Fig. 6.
4. `chirp_nonlinearity` (laser, dimensionless 1 - r2 or % as printed; D431 candidate `chirp_nonlinearity_pct`): liu2022d 1.02e-7 (R 99.96 %), p.8 Table I.
5. `frequency_noise_hz2_per_hz` (laser; D431 candidate): white frequency-noise level. guo2021 800 Hz2/Hz p.8-9 Fig. 7; liu2022d 900 Hz2/Hz p.6 Fig. 7.
6. `placement_accuracy_um` (chip_chip_coupler): standard deviation of the die placement error of an alignment / bonding process (sample count in n_samples). kobayashi2014 0.1 um (n = 57), p.4 Fig. 7.
