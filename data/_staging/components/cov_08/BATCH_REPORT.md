# cov_08 batch report (2026-11-07)

All six cached texts match their source rows (page-1 title). None is a correction or an erratum. Notes on the texts:
- ling2024 is the arXiv preprint text (arXiv:2310.20157v1, main text and Supplementary Information). Its title and arXiv id match the source row; the journal version was not read (D430 / D433 precedent).
- helgason2023 p.1 is a cover page. The article runs from p.2; locators use the text.md page numbers.
- wang2025a: `garbled_text_layer` covers p.9 only (references). Every value comes from the clean pp.1-8 text, and Table 1 was checked on the p.8 render.

No paper had component rows in `data/components/components.csv` before this batch. Figure checks used the cached page renders. ling2024 Supp. Fig. S.1 and hu2022 Ext. Data Table 1 were rendered from `source.pdf` into the scratchpad.

Dry-run: +26 components, +143 metrics, 0 errors. The one warning (ni2025b m18 / m4) is on an existing merged row, not from this batch.

| paper | components | metrics |
|---|---|---|
| zhang2019b | 2 (laser.comb 1; resonator.ring 1) | 15 |
| hu2022 | 2 (laser.comb 1; resonator.coupled_rings 1) | 28 |
| ling2024 | 9 (laser.comb 3; resonator.ring 2; reflector.loop_mirror 1; chip_chip_coupler.butt 1; fiber_chip_coupler.edge 1; amplifier.soa 1) | 33 |
| helgason2023 | 5 (laser.comb 2; resonator.coupled_rings 2; fiber_chip_coupler.edge 1) | 34 |
| zhang2024c | 4 (laser.comb 1; resonator.ring 1; laser.dfb 1; amplifier.other 1) | 15 |
| wang2025a | 4 (laser.comb 1; fiber_chip_coupler.edge 1; waveguide_platform.straight 1; phase_shifter.thermo_optic 1) | 18 |

## Not entered, and why

zhang2019b
- Modulator values: Vp 10 V, beta = 1.2 pi (+/-4 %), and the resonance broadening by beta (rule 2).
- Comb span 80 nm, slope about 1 dB/nm, adjacent-line variation < 0.1 dB, SNR > 40 dB: no parameter (comb span was rejected in D81).
- Electrical power about 630 mW, and the 30 / 750 / 45 mW projections. All rest on C ≈ 200 fF, which is cited to ref. 35 (rule 3) or is a projection.
- Simulated dispersion-engineered designs (1.3-octave, octave and 600 nm combs, Ext. Data Fig. 1): simulated comb spans with no parameter.
- Round-trip transmission alpha = 0.95. The racetrack perimeter is not printed, so it cannot be converted to dB/cm (in notes).
- The 25 GHz FSR ring of Fig. 2(a) is an illustration with no values.
- The 0.3 % efficiency of this device appears only in hu2022 Table 1 ("extracted from the raw data"). It is another paper's value and is not entered on either row.

hu2022
- Modulation index 0.48 pi and Omega = 2 pi x 7.4 GHz (rule 2).
- Microwave drive 2.2 W: entered only as an operating condition.
- Comb spans 132 nm / 161 nm and slope -0.7 dB/nm: no parameter.
- Methods 3.75 nm 3-dB bandwidth and 1553.6 nm centre: measured on a device "with similar parameters" (D159).
- Inter-cavity coupling mu = 2 pi x 1.47 GHz: a coupling rate, not the measured splitting, which is not printed.
- Theory values eta_max 38 % / 83 % / 50 %, and the 85 W peak / 0.9 W intracavity powers: inferred from a formula.
- Table 1 rows of other works (rule 3).

ling2024
- Spectral widths not entered: comb optical bandwidth about 20 nm / about 50 nm, and the sech2 "bandwidth" of 7 nm (definition not stated).
- Laser alpha signal values with no parameter: RF beat SNR 79 dB / 65 dB / 77 dB, phase noise, RF beat 3-dB linewidth 1.5 kHz, whole-comb tuning rate 2.4e17 Hz/s, and the < 5 % tuning deviation.
- Feedback-mode "driving current as low as 60 mA": the lowest current for comb operation, not a threshold.
- Racetrack beta (1.5 um wide): Q is stated only as "similar". Its beta2 values (-0.02 / -0.01 / -0.003 ps2/m) have no parameter.
- Laser gamma (passive mode locking): no values.
- Simulation inputs: Q_i 1.5e6, Q_c 3e6, 3x cavity-length ratio, 150 nm simulated span.
- Sagnac coupler gap 0.3 um and taper 0.9 / 0.7 um: no gap or taper parameter on `reflector` (in notes).

helgason2023
- Main text: 35 % state reached at 12.3 dBm without power reduction (p.7). The device is not named (D159).
- Methods and figures: existence-map values (8 % / 80 % peak efficiency) and the Ikeda / coupled-cavity simulation inputs (theta, Q, beta2).
- Device parameters with no parameter: GVD beta2 -81 / -82 ps2/km, nonlinear parameter gamma = 0.9 /(W m) (mode solver), and maximal resonance shift 735 / 440 MHz. The shift is a mode-crossing shift, not a supermode splitting.
- Repetition-rate beat of device 1 (Fig. 3(d) inset): value not printed.

zhang2024c
- Overall electrical-to-optical WPE 18.8 % (abstract: 19 %): a system value spanning the microcomb and the 34 injection-locked DFB lasers (see question 3).
- Noise-floor increment ~0 dB / 4.7 dB / 11.2 dB (Fig. 2(i)): not a noise figure. The EDFA and SOA are setup equipment.
- Free-running slave power around 21 dBm: in notes. OSNR > 70 dB: no parameter.
- SiPh transceiver: EO / OE bandwidth around 50 GHz, PRBC / PRBS, hybrids and BPD/TIA. No component-level values; the IQ modulators are EO (rule 2).
- 7-core fibre loss 0.25 dB/km and crosstalk < -60 dB: a transmission fibre, out of scope.
- System values: data rate, BER and DSP reduction.

wang2025a
- Modulator values (rule 2): RF Vpi 3 V at 25 GHz, 3.35 V at 35 GHz and 2 V DC; simulated VpiL 2.3 V cm; EO bandwidth > 67 GHz (35 GHz packaged); MZM extinction > 50 dB.
- 6.5 dB fibre-to-fibre loss of the MZM + 3 PM cascade: a modulator-chain IL (rule 2; see question 2).
- Span 29.41 nm: no parameter.
- 10 dB power-variation window: the line-counting criterion, not a result.
- Pump tuning 1480-1640 nm (Fig. 7: 1500-1625 nm): the external laser's tuning range.
- Simulated line counts 157 / 151 / 99 vs RF phase error: sensitivity study.
- Table 1 rows of other works (rule 3).

## Missing fab / facility orgs

- Myfab Chalmers (helgason2023 p.11 Acknowledgements: devices "fabricated in part at Myfab Chalmers").
  - Facility, parent org_chalmers_university_of_technology. Already queued for the org round (girardi2025).
  - If registered, it goes on all 5 helgason2023 rows.
- Cornell Center for Materials Research (ling2024 p.9 Acknowledgements: work "performed in part at" CNF and CCMR).
  - Facility, parent org_cornell_university.
  - If registered, it goes on the 7 ling2024 TFLN rows. The RSOA row and the RSOA-LN interface row are excluded.
- Ids used, all in the registry: org_harvard_university, org_center_for_nanoscale_systems, org_university_of_rochester, org_cornell_nanoscale_facility, org_chalmers_university_of_technology.
- Not entered:
  - zhang2024c: Si3N4 made "in a commercial CMOS foundry" with no name. The pump DFB and slave DFBs have no stated source.
  - wang2025a: passive fabrication statement (D80b). Authors are at Sun Yat-sen University and Liobate.
  - NANOLN / NanoLN: wafer supplier, in notes.

## Judgment calls

1. Comb rows use `laser.comb`, as the brief asked: EO comb generators (zhang2019b, hu2022, wang2025a), the hybrid comb lasers (ling2024) and the Kerr microcombs (helgason2023, zhang2024c).
   - Each resonator that hosts a comb is a separate `resonator.*` row with a D396 cross-note.
   - Hybrid two-material comb sources take platform `other` (boust2020 precedent): RSOA + TFLN, and DFB + Si3N4.
2. Comb pitch parameter (D83b):
   - `repetition_rate_ghz` where the paper says repetition rate or characterizes pulses: hu2022, ling2024, wang2025a 25 GHz, helgason2023 49.85 GHz.
   - `channel_spacing_ghz` where it says spacing: zhang2019b 10.453 GHz, wang2025a 48 GHz.
3. D403:
   - Strictly applied (author_estimate): hu2022 kappa_e / kappa_i / Q_i (extracted from linewidth + extinction with no regime test); helgason2023 Q_i / Q_e of all four cavities; zhang2024c Q_i 4.3e7; zhang2019b k = 0.027 and the fitted coupler loss.
   - Kept measured: hu2022 total kappa_2 = 222 MHz, which does not depend on the regime.
   - Kept measured: ling2024 test racetrack Q0 / Qe. The Fig. S.1(b) dip reaches ~0, so critical coupling is fixed by the data (D517 sun2025a precedent).
4. On-chip efficiencies and powers:
   - hu2022 30 % / 32 % / 20 mW: entered as `measured`, `ref_plane: on_chip`. The paper says facet losses were taken into account but does not describe how.
   - ling2024 8.5 mW "on chip": entered as `author_estimate`. It rests on the "around 6 dB" coupling loss, whose origin is not stated.
5. Loss-budget terms with no stated origin are `author_estimate`: wang2025a 1.0-1.25 dB/facet and 0.27 dB/cm; helgason2023 ~2 dB/facet; ling2024 ~6 dB fibre and RSOA interfaces; ling2024 Sagnac > 95 %; ling2024 RSOA 3-dB gain width > 40 nm; zhang2024c DFB 19 dBm.
6. ling2024:
   - wpe 2.8 % is `derived` (the authors' arithmetic). 5.6 % is `author_estimate`: it doubles on the statement that both ports emit equal power, which was not measured (D462 analogue).
   - Tuning efficiency 0.2-0.8 GHz/V was converted to 1.67-6.68 pm/V at 1582 nm (`derived`). The 1.2 GHz excursion was converted to 0.010 nm `tuning_range_nm`.
   - The test racetrack (single bus) and the in-laser racetrack (pulley, two buses) are separate rows: they are different coupler designs.
   - The FP-laser 39.27 GHz (text and caption) disagrees with the Fig. 3(c) inset axis label, 39.22 GHz (D417 note).
7. hu2022:
   - Pulse width 336 fs is `author_estimate`: it rests on the nominal SMF-28 dispersion and an assumed pulse shape.
   - n_channels 533 / 650 are `derived` (span / repetition rate, Table 1 footnote a).
   - Cavity-1 FSR 254.54 GHz is `author_estimate` ("final optimized device FSR values", origin unclear). Cavity-2 FSR is `measured`, because the drive matches it.
   - Heater tuning power ~350 mW per FSR is `derived` (I^2 R with ~50 mA and ~140 ohm). The resistance includes routing.
8. zhang2024c: the injection-locked slave DFB is entered as `amplifier.other`, with gain 61.17 dB and output 21.58 dBm read from the Fig. 2(e) labels. Its free-running laser output is kept in notes; there is no separate laser row.
9. Wavelengths inferred from the operating band where the paper does not tie them to the value (each flagged `wavelength_inferred`):
   - hu2022 Ext. Data Table 1: l_band, from the ~1600 nm pump.
   - zhang2019b Q / linewidth: 1600 nm.
   - wang2025a losses / P_pi: c_band.
   - helgason2023 facets: the pump wavelengths.
   - ling2024 test racetrack: `band: unspecified`. The paper says only "telecom band".

## Coordinator questions

1. Should EO comb generators (resonator-based and cascaded-modulator) stay in `laser.comb`, or get their own subtype, e.g. `laser.eo_comb` or `frequency_converter.other`? `laser.comb` is described as "comb source" and has held only lasers and Kerr combs until now. Recommendation: keep `laser.comb` and tag `eo_comb`.
2. wang2025a 6.5 dB fibre-to-fibre loss of the packaged comb generator: rule 2 (modulator IL) or a comb-source total? Recommendation: leave it out. It is the IL of four modulators in cascade, and its edge-coupler and waveguide parts are entered separately.
3. zhang2024c overall WPE 18.8 % of the microcomb-seeded injection-locked DFB array: enter it on the comb row with a condition, or create a system-level parallel-source row? Recommendation: leave it out (system value) unless the coordinator wants a parallel-source row.
4. hu2022 on-chip efficiency / power with undescribed facet de-embedding: `measured` (as entered) or `author_estimate` (rule 4, origin of the facet loss not stated)? Recommendation: measured. The efficiency is a slope fit of the paper's own data, and the paper states the facet correction.

## Registry gaps (proposals; skipped values with locators)

- `comb_span_nm`: comb span at a stated power level or flatness window.
  - Skipped values: zhang2019b 80 nm (p.2); hu2022 132 nm at -70 dBm / 161 nm (p.3, p.5); wang2025a 29.41 nm within 10 dB (p.5); ling2024 about 20 / 50 nm (p.4, p.6).
  - Proposed definition: "full spectral span of a comb at the stated power level / flatness criterion (criterion in condition)". D81 rejected it earlier; this batch has four sources with a concrete value.
- `resonance_shift_mhz` (resonator): a controllable shift of a selected resonance by an avoided mode crossing. Skipped values: helgason2023 735 / 440 MHz (p.10).
- `gvd_ps2_per_km` (resonator, waveguide_platform): measured group-velocity dispersion. Skipped values: helgason2023 -81 / -82 ps2/km (p.10); ling2024 -0.02 / -0.01 / -0.003 ps2/m (p.10-11 Supp.).
