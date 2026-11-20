# Batch lit_217 report

Distilled 2026-11-20 (verified_on 2026-11-20). Five photodetector papers. Dry run: `merge_component_staging.py data/_staging/components/lit_217 --dry-run` -> +20 components, +105 metrics, 0 errors (the one WARN concerns an already merged row of another paper, cmp_lit_ni2025b_pimmwc).

All five cached texts match their source rows (page-1 titles); no correction or erratum. kinsey2001 and yasuoka2005 text layers carry garbled symbols (mu, kappa, OCR-like noise): every value was checked on the page renders. Figure reads use the embedded high-resolution figure images (`img_pNN_k.png`) and the page renders.

Bias convention: reverse bias stored negative (merged convention, runge2015 / beckerwerth2021); nada2020 prints reverse bias positive (noted per row).

## tossoun2018 / tossoun2018a: relation (D259 / D259a / D408)

- lit:tossoun2018 (IEEE PTL 30(4), Feb. 2018) and lit:tossoun2018a (JLT 36(20), Oct. 2018) are two different papers, not conference and journal versions of one work. The PTL letter extends the authors' SUM 2017 conference paper (its ref. [6], not cached); only the 2.2 um absorption edge is attributed to [6] there, so the PTL keeps all its values (D408).
- The JLT paper adds two new epitaxial designs (samples B and C, dual-integrated waveguide-depletion layer) and uses "Sample A ... on which we have previously reported [11]", where [11] is the PTL letter. The JLT reproduces the PTL Sample A data: Fig. 7 0.6 A/W at 200 um with the same 3.5 dB coupling + reflection loss, Fig. 8 Sample A points (0.080 / 0.064 / 0.044 / 0.012 A/W at -3 / -2 / -1 / 0 V, identical to the PTL Fig. 8 10 x 50 um external points but labelled internal), Fig. 11 (the PTL Fig. 9 bias set and 530 uA photocurrent) with 3.5 GHz / 2.2 GHz, and the 45 % collection efficiency cited to [11].
- What I did: all these Sample A values are kept only on the tossoun2018 rows (primary source) and are not entered for tossoun2018a (D259 / D259a). Exception for the auditor: the JLT Fig. 6 Sample A dark-current trace is not attributed to [11] and differs from PTL Fig. 3 (about 1.1e-7 / 2.7e-7 A vs about 1.9e-7 / 3.8e-7 A at -1 / -3 V), so it is entered on a JLT Sample A row (cmp_lit_tossoun2018a_sample_a_10x50, 2 figure reads) with a cross-note (D408 strict reading).
- Conflict noted: PTL p.4 gives 3.5 GHz at -0.3 V for the 10 x 50 um device, the JLT p.5 gives the same device's maximum 3.5 GHz at -1 V. Kept as printed in the PTL row, with a cross-note.

## lit:tossoun2018 (IEEE PTL 30(4), 2018, 4 pages)

Components / metric rows: 8 / 41

| component | class | metrics |
|---|---|---|
| cmp_lit_tossoun2018_wgpd_10x10 | photodetector.other | dark < 100 nA at -2 V (printed), about 280 nA at -5 V (Fig. 3); geometry 10 / 10 um, 960 nm MQW |
| cmp_lit_tossoun2018_wgpd_10x50 | photodetector.other | bw3db 3.5 GHz (-0.3 V), 2.2 GHz (-7 V), 3 GHz (-3 V, summary); dark about 600 nA at -5 V (Fig. 4); external responsivity about 0.109 / 0.080 A/W at -7 / -3 V (Fig. 8); geometry |
| cmp_lit_tossoun2018_wgpd_20x50 | photodetector.other | dark about 2.9 uA at -5 V (Fig. 4); geometry |
| cmp_lit_tossoun2018_wgpd_20x75 | photodetector.other | dark about 5.8 uA at -5 V (Fig. 4); geometry |
| cmp_lit_tossoun2018_wgpd_20x100 | photodetector.other | external responsivity 0.15 A/W (2 um) and 0.23 A/W (1.55 um) at -7 V, about 0.120 A/W at -3 V (Fig. 8); geometry |
| cmp_lit_tossoun2018_wgpd_20x200 | photodetector.other | external 0.27 A/W (2 um, -7 V), internal 0.6 A/W (author_estimate, 3.5 dB origin not stated), QE about 17 % (Fig. 6 star), about 0.215 A/W at -3 V (Fig. 8); geometry |
| cmp_lit_tossoun2018_ti_pd_d250 | photodetector.vertical | external 0.3 A/W (1.55 um), 0.05 A/W (2 um); 250 um diameter, 960 nm MQW |
| cmp_lit_tossoun2018_input_facet | fiber_chip_coupler.edge | 3.5 dB per facet incl. fiber coupling + facet reflection (author_estimate); width 5 um (derived) |

Values not entered and why:
- Summary (p.4 Sec. IV) "0.49 A/W internal responsivity" at -3 V: no device named (D159); close to 20 x 200 um Fig. 8 (-3 V) x 3.5 dB, but the paper does not say so. In component notes.
- Fig. 6 measured QE points of the "500 um diameter" top-illuminated PD: the text gives 250 um for the 0.3 / 0.05 A/W values; device identity conflict (D159). In notes.
- Fig. 5 dark current vs temperature (250 um diameter, 77-300 K): temperature series, not entered.
- Fig. 7 simulated internal QE vs PD length (400 um design, not fabricated) and the absorption coefficients (cited ref. [9]); RC-limited bandwidth 19 GHz (calculated, no Cj / Rs printed); 2.2 um absorption edge (cited to the authors' SUM 2017 paper [6], rule 3).
- "500 nm thick" input rib: thickness vs etch depth not distinguished (layout rule: no guessed role).
- Fab / facility: none (passive "were fabricated" / "was grown", D80b; tool names only).

Judgment calls:
- 3 GHz at -3 V (summary) assigned to the 10 x 50 um row: Fig. 9 (10 x 50 um, includes -3 V) is the only bandwidth measurement. Auditor may prefer notes only.
- 10 x 10 um "< 100 nA at -2 V" kept as printed; Fig. 3 reads about 160 nA at -2 V (conflict in notes, D417).
- 20 x 100 um 0.15 A/W kept as printed; Fig. 8 reads about 0.165 A/W at -7 V (D417).
- Waveguide PDs `photodetector.other` (D152), top-illuminated PD `photodetector.vertical` (chen2019 / arabhavi2020 precedent); external responsivity of the waveguide PDs `ref_plane: fiber` (the paper removes fiber coupling + facet reflection to get the internal value); top-illuminated `unspecified`.
- Width x length naming: the 20 x 200 um device is the 200 um long PD (p.3-4), so the first number is the width.

## lit:tossoun2018a (JLT 36(20), 2018, 7 pages)

Components / metric rows: 6 / 30

| component | class | metrics |
|---|---|---|
| cmp_lit_tossoun2018a_sample_b_10x50 | photodetector.other | bw3db 4.5 GHz at -3 V (1.1 mW); dark about 9.6 / 86 nA at -1 / -3 V (Fig. 6); internal about 0.24 A/W at -3 V (Fig. 8); geometry 10 / 50 um, 280 nm MQW |
| cmp_lit_tossoun2018a_sample_b_20x200 | photodetector.other | internal 0.81 A/W at 2 um, 5 V (author_estimate); geometry |
| cmp_lit_tossoun2018a_sample_c_10x50 | photodetector.other | bw3db > 10 GHz at -3 V; dark 1 nA at -1 V (best, printed), about 4.8 nA at -3 V (Fig. 6); internal about 0.335 A/W at -3 V (Fig. 8); geometry, 300 nm MQW |
| cmp_lit_tossoun2018a_sample_c_20x200 | photodetector.other | internal 0.84 A/W at 2 um, 5 V (author_estimate); geometry |
| cmp_lit_tossoun2018a_sample_a_10x50 | photodetector.other | dark about 113 / 270 nA at -1 / -3 V (Fig. 6 only); geometry |
| cmp_lit_tossoun2018a_input_facet_bc | fiber_chip_coupler.edge | about 7 dB per facet incl. coupling + reflection (simulated, "calculated"); width 4 um (derived), InGaAs core 1000 nm |

Values not entered and why:
- Sample A values reproduced from lit:tossoun2018 (see the relation section): 0.6 A/W, 3.5 dB, 45 %, Fig. 8 Sample A, Fig. 11, 3.5 / 2.2 GHz.
- Rs 33 ohm, Cj 0.1 pF, RC limit about 19 GHz (p.5): stated "for a 10 um x 50 um PD" without the sample (D159 / D254); in notes on both 10 x 50 um B / C rows.
- Transit-time limited bandwidth 37 GHz (sample C, calculated), Fig. 12 / Table I nextnano model values, Fig. 4 calculated absorption coefficients, Fig. 3 band structure, simulated confinement factor 0.87.
- Fig. 10 curve crossings at -1 V / -5 V (sample B) and -1 V (sample C): the curves are Eq. (6) calculations through the dots, not printed values.
- Fig. 7 markers at 50 / 100 um length: device width not stated (D159).
- Collection efficiency 45 / 55 % (calculated, cited to [11]).
- 10 Gb/s eye diagrams at -8 V (Fig. 13): no registry parameter (gap below).
- Fab / facility: none (passive process description; acknowledgment thanks staff for clean-room assistance, no facility named, D72).

Judgment calls:
- "1 nA at -1 V" (abstract, conclusion, no device named) assigned to sample C 10 x 50 um: the Fig. 6 sample C trace is the only one near 1 nA (reads about 1.2 nA). Statistic best.
- Sample B 4.5 GHz assigned to -3 V: the sentence puts "at -3 V" after both devices and the Fig. 10 sample B (-3 V) curve crosses -3 dB near 4.4 GHz.
- Internal responsivities (0.81 / 0.84 A/W and the Fig. 8 reads) rest on the calculated 7 dB coupling + reflection loss: 0.81 / 0.84 `author_estimate`; Fig. 8 reads `extracted_from_figure` with that dependence in notes (auditor may prefer `author_estimate`).
- One coupler row for the B / C facet (one value stated for both samples, same waveguide-depletion design).
- Sample A Fig. 6 row entered (see relation section); auditor ruling welcome.

## lit:nada2020 (ECOC 2020, 4 pages)

Components / metric rows: 2 / 15

| component | class | metrics |
|---|---|---|
| cmp_lit_nada2020_inverted_pdown_pin_d10 | photodetector.vertical | 0.61 A/W at 1300 nm, -2 V; dark 0.52 nA (-2 V), 0.84 nA (-10 V); bw3db > 49.8 GHz measured (-2 V); 70.1 (-2 V), 70.9 (-2.4 V), 69.9 (-3.3 V) GHz author_estimate; 10 um diameter, 450 nm absorber |
| cmp_lit_nada2020_inverted_pdown_pin_d14 | photodetector.vertical | bw3db 39.0 (-2 V), 40.4 (-4.2 V), 40.3 (-3.3 V), 37.2 (-10.2 V) GHz measured; 14 um diameter, 450 nm absorber |

Fab org_ntt on both rows: p.3 "We designed and fabricated", all authors at NTT units of NTT Corporation (D154 parent; renamed org maps to org_ntt, contract v7).

Values not entered and why:
- Fig. 3 dark current vs active area (four areas): only 10 and 14 um diameters are named; the other areas map to unnamed diameters (D159). The 10 um dark currents are entered from the text.
- Estimated electric field about 60 kV/cm; design discussion of drift velocities (cited refs.).

Judgment calls:
- 10 um bandwidths above 49.8 GHz are single-pole fits extrapolated beyond the instrument range -> `author_estimate` (D435); the 14 um values lie inside the range -> `measured`. Fig. 5 values above 49.8 GHz (70.9, 69.9) treated the same way; wavelength 1300 nm inferred for the Fig. 5 values (stated only for Fig. 2 / Fig. 4).
- Active-area diameter (top n-contact mesa) entered as `absorber_width_um` (chen2019 precedent).
- Responsivity ref_plane unspecified (input plane not stated).

## lit:kinsey2001 (IEEE PTL 13(8), 2001, 3 pages)

Components / metric rows: 3 / 15

| component | class | metrics |
|---|---|---|
| cmp_lit_kinsey2001_sacm_wgapd_10x10 | photodetector.apd | bw3db 28 GHz (gain up to 6, n 3); GBP 270-340 GHz (3 devices, linear fit) and "at least 320 GHz" (author_estimate); forward differential resistance 47 ohm; 59 fF at 0 V; external QE < 5 % at 1.55 um; geometry 10 / 10 um, 200 nm InGaAs |
| cmp_lit_kinsey2001_sacm_wgapd_cleaved_40um | photodetector.apd | external QE 16 % at 1.55 um; length 40 um, 200 nm InGaAs |
| cmp_lit_kinsey2001_large_area_mesa | photodetector.apd (test_structure) | QE 11.8 % at 1.55 um (author_estimate, coupling assumed 100 %), theoretical 9.2 % (simulated), excess noise factor about 5.2 at M about 23 (Fig. 4) |

Values not entered and why:
- Breakdown "below 25 V" and dark current "below 1 uA/mm2 at 90 % of breakdown": from a "typical" I-V of an unnamed device (D254); the density also has no printed bias (dark_current_density_ma_per_cm2 requires bias).
- Highest gain 17 and gain at punch-through "at least 1.28": no bias printed (avalanche_gain requires bias); 1.28 also rests on the assumed coupling and cited absorption coefficient.
- RC limit 57 GHz and transit-time limit about 30 GHz (calculated); ionization ratio k = 0.15 (no parameter; gap below); 290 GHz of ref. [11] (cited work, rule 3).
- Fab / facility: none (passive growth / processing, no org named, D80b).

Judgment calls:
- Bandwidth and GBP wavelength left empty / band unspecified: the frequency response used a Ti-sapphire mode-locked laser whose wavelength is not printed; inferring the 1.55 um band would be wrong for this measurement (rule 8).
- "At least 320 GHz" entered as `ge` `author_estimate` beside the measured 270-340 GHz range (the arithmetic behind 320 is not shown). Auditor may prefer notes only.
- 47 ohm forward differential resistance in `series_resistance_ohm` (D254 I-V-slope precedent); 59 fF assigned to the 10 x 10 um device (same sentence, "for a mounted device").
- Large-area mesa test row created for the QE / noise data (same wafer, normal incidence, size not stated).

## lit:yasuoka2005 (LEOS annual meeting, ThZ5, 2 pages)

Components / metric rows: 1 / 4

| component | class | metrics |
|---|---|---|
| cmp_lit_yasuoka2005_sagcm_apd_inp80 | photodetector.apd | bw3db 21 GHz max at M = 2; MB product 170 GHz at M = 12 (measured); 390 GHz intrinsic limit from the 0.4 ps build-up time (author_estimate); junction radius 4.5 um |

Fab org_fujitsu: p.2 "we have fabricated an APD", all authors at Fujitsu Laboratories Ltd. / Fujitsu Quantum Devices Ltd. (D154 parent).

Values not entered and why:
- Dark current "below 200 nA at a breakdown voltage of 90 %": breakdown voltage not printed (Fig. 2 / 3 suggest about 16 V, not read into a bias); dark_current_na requires bias.
- "Maximum multiplication factors are over 10": no bias printed.
- Tunnel-current bound (p.1; unit printed oddly as "0.5A/cm-2"), 0.4 ps intrinsic build-up time and 0.9 ps Emmons prediction (no parameter), 80 nm multiplication-layer thickness (no parameter).

Judgment calls:
- Bandwidth / MB-product wavelength 1550 nm inferred (DFB wavelength not stated; photocurrent and multiplication measured at 1.55 um).
- 390 GHz entered as `author_estimate` (model extraction projected beyond the measured gains, D435); auditor may prefer notes only.
- Junction radius in `radius_um` as printed (no conversion to a diameter).

## Missing fab / facility orgs (name as printed + locator)

- "Fujitsu Laboratories LTD." (yasuoka2005 p.1 affiliation; fab role via p.2 "we have fabricated") and "Fujitsu Quantum Devices LTD." (yasuoka2005 p.1): alias candidates for org_fujitsu (no new id). Row uses org_fujitsu.
- "NTT Device Innovation Center, NTT Corporation" and "NTT Device Technology Laboratories, NTT Corporation" (nada2020 p.1): alias candidates for org_ntt (existing aliases cover the "NTT, Inc." forms). Rows use org_ntt.
- No facility orgs in this batch.

## Registry gaps (skipped value + locator, proposed definition)

- `data_rate_gbps` (photodetector): tossoun2018a 10 Gb/s open eye at -8 V, 2 um (p.6-7 Fig. 13); "highest data rate demonstrated with an open eye / stated BER (criterion in condition)". Already a D534 candidate.
- `ionization_ratio_k` (photodetector): kinsey2001 k = 0.15 for M up to 23 (p.2 Fig. 4); "effective impact-ionization coefficient ratio from the excess-noise fit (McIntyre), gain range in condition". Already a D436 candidate.
- `multiplication_thickness_nm` (photodetector, geometry): kinsey2001 150 nm InAlAs (p.1), yasuoka2005 80 nm InP (p.1); "APD multiplication-layer thickness".
- `avalanche_buildup_time_ps` (photodetector): yasuoka2005 0.4 ps (p.2); "intrinsic avalanche build-up time from the response-time decomposition (method in notes)".

## Source registry note

- lit:yasuoka2005: registry year 2005, but the page-1 footer prints the 2003 IEEE copyright and the DOI is 10.1109/leos.2003.1253144 (LEOS 2003 annual meeting); the year field looks wrong. Title matches.
