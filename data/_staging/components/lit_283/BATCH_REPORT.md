# lit_283 batch report

Distilled 2026-11-25 (verified_on 2026-11-25). Papers: lit:shtyrkova2019, lit:zhang2017b, lit:chu2023, lit:wan2019a.
Page-1 titles match the source rows; no garbled text layer. shtyrkova2019 pages 5, 8 and 13 have a two-column text
layer that interleaves lines, so those pages were read from the page renders (`figures/page_05.png`, `page_08.png`,
`page_13.png`).

Totals: 30 components, 132 metric rows. `merge_component_staging.py --dry-run`: 0 errors (the 2 warnings are in older
batches).

| paper | components | metric rows |
|---|---|---|
| shtyrkova2019 | 12 | 40 |
| zhang2017b | 10 | 50 |
| chu2023 | 4 | 16 |
| wan2019a | 4 | 26 |

## lit:shtyrkova2019 (Tm:Al2O3-on-Si3N4 Q-switched mode-locked laser, 1.9 um, Optics Express 2019)

Components: `qsml_laser` (laser.comb, al2o3), `pump_signal_combiner` (wdm.other), `combiner_dc`
(splitter.directional_coupler), `gain_waveguide_test` (amplifier.rare_earth, test structure), `fn_bn_transition`
(waveguide_platform.transition), `euler_bend_180` (waveguide_platform.bend), `chirped_grating_gdd46000` /
`gdd38000` / `gdd30000` (reflector.bragg, simulated reflectivity), `nli_loop_mirror` (reflector.loop_mirror),
`nli_input_coupler` (splitter.other), `nli_heater` (phase_shifter.thermo_optic).

Laser values: CW threshold about 45 mW of on-chip pump power, QSML onset about 170 mW, 9 mW maximum on-chip average output, about 1880 nm, 17 nm sech2-fit 3-dB
bandwidth, 1.2 GHz repetition rate, and 215 fs transform-limited duration (derived, D84c). Other rows: pump/signal combiner
0.6 dB (pump, 1600 nm as printed) and 0.35 dB (signal, 1900 nm) per component; FN-to-BN transition 0.02 dB at 1900 nm (cutback);
Euler bend < 0.04 dB per 180 deg bend (both wavelengths, one row); gain waveguide net gain read off Fig. 4(c).

Not entered and why:
- Q-switching rate 720 kHz (500 kHz to about 1 MHz with pump power; p.13 Fig. 11(a)): no registry parameter.
- NLI modulation depth / self-amplitude-modulation coefficient: simulated 12.3 % / 3.7e-4 1/W (23 mm) and 19.2 % /
  2.8e-4 1/W (9.8 mm), measured 9 % / 7e-5 1/W on the 23 mm test structure (p.10; the 7e-5 sentence carries ref. [16],
  a Moss et al. review). No registry parameter, so the NLI as a whole and the 23 mm test structure have no rows.
- Chirped-grating GDD -46,000 / -38,000 / -30,000 fs2 (p.8, Fig. 6(c)): no parameter.
- Table 2 film spectroscopy (lifetime 568 +/- 48 us, absorption cross-sections, 0.1 dB/cm background loss measured
  at 633 nm as an upper bound, Tm 2.9e20 cm-3; p.6): these are material values, and the characterization paragraph cites the authors'
  ref. [29]. The film loss is left out as a material upper bound at a wavelength the device does not use.
- Simulated confinement 83 % / 79 % and 60 % pump-signal overlap (p.6): no parameter.
- Footprint printed three ways (23.6 x 0.6 x 0.78 mm p.1; 23.5 x 0.78 mm p.2; 23.6 x 0.6 mm p.14): conflicting, not
  entered (D417).
- Combiner design transmissions 89 % / 100 % (simulated, p.5) and authors' linear 86 % / 92.5 %: notes only.
- Authors' sum of 0.16 dB for 4 bends: notes only. Table 3 dispersion and nonlinearity values: model inputs.
- Earlier 2017 laser of the group (ref. [25]): cited values, rule 3.
- Segmented gain-waveguide piece widths (Fig. 4(a) labels 500 nm / 350 nm): the labels cannot be tied to piece width or gap without
  guessing (D156).
- Ring-resonator test structures for the layer losses (p.4): no values printed.

Orgs: fab `org_college_of_nanoscale_science_and_engineering` on all rows. The p.3 sentence says all lasers and test
structures except the gain film were fabricated at CNSE at SUNY Polytechnic Institute on a 65nm CMOS 300mm wafer
platform; `process_name` "65nm CMOS 300mm wafer platform" as printed. On the gain-bearing rows (`qsml_laser`,
`gain_waveguide_test`) the fab also includes `org_mit`, with facility `org_mit_microsystems_technology_laboratory`: the
p.3 text says the gain film was deposited at MIT's Microsystems Technology Laboratories (a stated place, D448).
- Alias gap (org round): printed plural form "Colleges of Nanoscale Science and Engineering (CNSE) at SUNY Polytechnic
  Institute" (p.3 Sec. 2), mapped here to the registry singular `org_college_of_nanoscale_science_and_engineering`.
  Proposed: add it as a printed_variant alias. Batch_7 skipped the same plural string for kim2019, which was an
  affiliation only.

## lit:zhang2017b (unidirectional widely tunable III-V-on-Si ring laser, Optics Express 2017)

Components: `vernier_ring_laser` (laser.tunable, platform other per the heterogeneous III-V-on-SOI precedent),
`ring_laser_no_dbr` (laser.tunable, reference without the DBR), `ring_r25um` / `ring_r27um` (resonator.ring, D400),
`dbr_reflector` (reflector.bragg, simulated), `output_dc` (splitter.directional_coupler), `grating_coupler`
(fiber_chip_coupler.grating, back reflection only), `phase_heater` / `ring_heaters` (phase_shifter.thermo_optic,
resistance only), `si_rib_waveguide` (waveguide_platform.straight, ~1 dB/cm author_estimate).

Laser values (20 C stage, 100 mA): 40 nm tuning (1560-1600 nm), 1.5-3.3 mW waveguide-coupled, SMSR > 40 dB (38 dB at
1600 nm, best ~50 dB read off Fig. 6(b)), linewidth < 1 MHz and 550 kHz best (Hz, derived), gain-section series
resistance 10 ohm, combined Vernier FSR ~40 nm, < 50 mW per micro-heater, geometry.

Not entered and why:
- CW-mode suppression about 10 dB (CCW/CW ratio; p.1, p.7 Fig. 7, p.8): no registry parameter.
- Threshold: not printed. The Fig. 8 onsets vary with wavelength and mode hops (about 60-90 mA), so no single value.
- Adiabatic III-V/Si taper: only a simulated tip reflectivity below -40 dB (500 nm tip, 180 um taper, p.4 / p.7), and
  back_reflection_db is not allowed for waveguide_platform. Geometry only, so no row.
- Abstract "above 0 dBm" duplicates the 1.5-3.3 mW range. Simulated ring Q 17000 in the Fig. 5(c) model (p.5) is an
  assumption.
- Adiabatic coupler details cite ref. [12]; the bonding process cites ref. [24] (no values taken).

Orgs: fab `org_ghent_university` on all rows. Basis: the first-person statement "We report on the design, fabrication and
characterization" (p.3), and every author is in a Ghent University unit (D72 / D154; D697 accepted the same wording for
wang1998). imec is not named for fabrication, and the 193 nm DUV lithography sentence is passive. No facility. No
missing orgs.

## lit:chu2023 (2 um InAs/InP quantum-dash ridge lasers, Optics Express 2024)

Components: `qdash_laser_7p1um_3mm`, `qdash_laser_13um_3mm`, `qdash_laser_8p7um_2p5mm`, `qdash_laser_wider_family`
(all laser.other, inp).

Values: thresholds 140 / 252 / 414 mA (SPW / QCW / CW, 20 C); T0 43 K (SPW) and 34 K (QCW); 15 mW peak SPW power
(7.1 um); 32 mW peak at 15 C (13 um); emission at about 1.97 um (8.7 x 2.5 mm, derived um to nm); T0 ranges 42-45 K
(SPW) and 34-40 K (QCW) for the wider ridges; SEM-measured ridge widths; lengths.

Not entered and why:
- Threshold current densities 657 / 1183 / 1944 A/cm2 (131 / 237 / 389 per layer) and transparency current densities
  278 / 301 A/cm2 (p.4-5): no parameter.
- Fig. 3(b) threshold densities at other widths and lengths: density only.
- CW operation only up to 25 C (p.5): no parameter.
- Emission FWHM 4.5 nm at 0.3 A and 22 nm at 3 A (p.6): bw_fwhm_nm is not allowed on lasers. The modes were not resolved.
- PL peak 1.94 um and FWHM 302 nm, PG vs CG PL 1.6x: material values, not a device.
- CW voltage curve in Fig. 3(a): no printed value.

Orgs: fab empty. The growth and fabrication sentences are passive. The authors are at KIST, KIST School UST and ETRI.
The thanks for "discussions on device fabrication" and for wire-bonding help are not fabrication statements. No
facility. No missing orgs.

## lit:wan2019a (tunable QD laser grown on Si, Optica 2019)

Components: `tunable_qd_laser` (laser.tunable, iii_v_on_si_epi), `half_wave_coupler` (splitter.other, simulated
cross-coupling), `ring_r1` (resonator.ring, design FSR 0.7 nm), `fp_reference_laser` (laser.other).

Values: threshold 33 mA; 2.7 mW per facet maximum; 5.6 ohm differential series resistance; 1 V turn-on voltage; SMSR
> 45 dB at the single-mode point, >= 45 dB over 11 channels and >= 30 dB over 37 channels; 16 nm tuning; 0.75 nm line
spacing; channel counts; lasing ~1230 nm (Fig. 5(b) read); design combined FSR 21 nm (simulated) and FP mode spacing
~0.2 nm; geometry. Reference FP laser: 47 mA threshold.

Not entered and why:
- Transparency current 11 mA of the FP laser (p.4): no parameter.
- Isolation resistance about 15 kOhm between sections (p.4): no parameter.
- Current tuning (Fig. 6 inset, Fig. 7(b)): no printed rate.
- 0.35 nm/C gain-peak shift (material statement) and the projected 42 nm over 80 C (p.5): projection.
- Design coupler space 40-60 um and 0.7-1.2 um: design range, not the built device.
- R2 perimeter 563 um: geometry only, so no row (noted on `ring_r1`).
- PL FWHM 127 nm and peak ~1240 nm: material values. Threading dislocation density 7e6 cm-2 (cites [48]).

Orgs: fab and facility empty. The processing sentences are passive. The thanks to the UCSB nanofabrication clean room staff for
"helpful discussions and assistance" (p.6) are staff thanks, which set no facility (D72 / D84b). NAsP III/V GmbH
supplied the GaP/Si wafer (supplier note on the component rows; not in the registry, no role).

## Judgment calls for the auditor

1. shtyrkova2019 laser: class `laser.comb` (mode-locked, D695) and platform `al2o3` (gain stack). This follows the merged
   Tm / Er Al2O3-on-SiN amplifier and DFB rows. The passive Si3N4 parts are `sin`.
2. shtyrkova2019 fab split:
   - CNSE + `org_mit` (fab) + MIT MTL (facility) on the two gain-bearing rows (D448 stated place);
   - CNSE alone on the passive rows;
   - CNSE on the NLI heater. The p.3 sentence covers everything except the gain film, but the heaters were deposited
     after the gain film and the paper does not name a site for that step.
3. shtyrkova2019 `pulse_width_fs` 215 entered as `derived` per D84c, although the paper says only "could support"
   (transform limit; no pulse measurement). The condition says so. The alternative is to drop the row.
4. shtyrkova2019 chirped gratings: three rows (one per GDD design), `fabricated` under the p.3 sentence. The paper does
   not say which design the measured laser carries; the model uses -38,000 fs2.
5. shtyrkova2019 gain waveguide: Fig. 4(c) is read as internal net gain per cm, because the no-pump trace is negative
   (so it is not a pump-on/off enhancement, D674). Values are about 1.20 dB/cm at 1885 nm and 1.14 dB/cm at 1900 nm
   (29.5 dBm pump).
6. shtyrkova2019 FN-BN transition platform `sin`: both layers are Si3N4, but the start mode sits largely in the Tm film.
7. shtyrkova2019 combiner wavelength: 1600 nm as printed, although the pump is at 1614 nm. The DC measured ratios
   (~2 % / ~63 %) were read off Fig. 3(b).
8. zhang2017b: the jointly stated ring values (Q ~17000, drop loss ~1 dB, ER ~20 dB) are entered on both ring rows.
   Ring FSR band `c_band` is inferred from the "1550 nm wavelength range" phrase.
9. zhang2017b: the `ring_laser_no_dbr` reference row exists only for the "> 5 dB" power-fluctuation sentence.
10. chu2023: the 1.97 um emission is placed on the 8.7 x 2.5 mm laser, because Fig. 5(b) says its LI curves come
    from the same diode as the spectra. The "wider cavities" T0 ranges sit on an array-level row (D165), with lengths
    and count not stated.
11. wan2019a: the turn-on voltage is entered as `forward_voltage_v` (no current stated; alboresmejia2010 / fang2006
    precedents). The cross-coupling coefficient 0.16 is entered as `split_ratio_pct` 16 `simulated`. The abstract's
    "exceeding 2.7 mW per tuning wavelength" is not a separate row (Sec. 4 says 2.7 mW maximum per facet).

## Registry gaps (skipped value, locator, proposed definition)

| proposed parameter | class | skipped value(s) | locator | definition |
|---|---|---|---|---|
| q_switching_rate_khz | laser | 720 kHz (500 kHz to ~1 MHz vs pump) | shtyrkova2019 p.13 Fig. 11(a) | Q-switched envelope repetition rate (pump power in condition) |
| modulation_depth_pct, sam_coefficient_per_w | reflector / other (saturable absorber) | 9 % and 7e-5 1/W measured; 12.3 % / 19.2 % and 3.7e-4 / 2.8e-4 1/W simulated | shtyrkova2019 p.10 | saturable-absorber modulation depth; slope of reflection vs peak power |
| gdd_fs2 | reflector | -46,000 / -38,000 / -30,000 fs2 (design) | shtyrkova2019 p.8 Fig. 6(c) | group-delay dispersion of a chirped mirror (sign as printed) |
| confinement_factor_pct | amplifier / laser | 83 % pump, 79 % signal (simulated) | shtyrkova2019 p.6 | modal power fraction in the gain layer (open since D581) |
| threshold_current_density_a_per_cm2 | laser | 657 / 1183 / 1944 A/cm2 | chu2023 p.1, p.4 | threshold current over the pumped area (recurring candidate, D431 / D677) |
| transparency current (density) | laser | 278 / 301 A/cm2; 11 mA | chu2023 p.5; wan2019a p.4 | current (density) at transparency, extraction method in notes |
| max_cw_temperature_k | laser | CW up to 25 C | chu2023 p.5 | highest stage temperature with CW lasing (recurring, D431 / D704) |
| bw_fwhm_nm on laser | laser | 4.5 nm at 0.3 A, 22 nm at 3 A | chu2023 p.6 | multimode emission FWHM (open since D697) |
| counter_propagating_suppression_db | laser | ~10 dB CW-mode suppression | zhang2017b p.7 Fig. 7 | power ratio of the lasing to the suppressed direction of a ring laser |
| back_reflection_db on waveguide_platform | waveguide_platform | < -40 dB taper-tip reflectivity (simulated) | zhang2017b p.7 | reflection at an inter-layer transition |
| isolation_resistance_kohm | laser | ~15 kOhm between sections | wan2019a p.4 | electrical isolation between laser sections |
