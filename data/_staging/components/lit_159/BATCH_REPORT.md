# lit_159 batch report

Papers: lit:herrmann2022, lit:che2024, lit:javid2021, lit:poulvellarie2021. verified_on 2026-11-16.
Validation: `merge_component_staging.py data/_staging/components/lit_159 --dry-run` -> +10 components, +58 metrics, 0 errors
(the one warning, cmp_lit_ni2025b_pimmwc, belongs to merged data, not this batch).

All four cached texts are arXiv copies; page-1 titles and authors match the source rows. herrmann2022 (arXiv v1, Nature
Photonics 2022), javid2021 (arXiv v1, PRL 2021) and poulvellarie2021 (arXiv v1, Optics Letters 2021) are preprints of the
listed journal papers: rows distill what the cached preprints report; journal versions unread (D430 / D433 precedent).
che2024's source row is the arXiv preprint itself.

## herrmann2022: 2 components / 15 metrics

- `cmp_lit_herrmann2022_freq_circulator` (nonreciprocal.circulator, 8): isolation nearly 40 dB (p.6, abstract) with
  4.4 dB IL (de_embedded, |S31|^2 = 0.36, Supp. Eq. 12) at P1 73.2 mW / P2 59.0 mW; > 25 dB with ~16 dB IL at
  7.32 / 0.74 mW; IL as low as 3 dB; Fig. 2(c) reads I23 ~26 dB, I12 ~27 dB (+/- 1 dB); film 500 nm.
- `cmp_lit_herrmann2022_triple_racetrack` (resonator.coupled_rings, 7, D396): Supp. Table S1 fit: kappa_e 847 MHz,
  kappa_i 404 MHz (measured; amplitude + phase fit separates them, D403), bare-mode total rates 1251 / 198 / 225 MHz
  (linewidth_mhz), dressed-mode spacing 2.63 GHz (mean), EO tuning 2.61 pm/V (derived from 328.5 MHz/V at 1543.6 nm).
- Not entered: mu12 / mu23 coupling rates 1.864 / 1.861 GHz (no parameter); 330 MHz/V RF rate (theory-inferred
  duplicate); Fig. 4 isolation maps (colour scale); isolation bandwidth ("more than a few hundred megahertz", no number);
  fiber coupling efficiency 8.14 % per facet (Supp. p.15, rests on an equal-facet assumption, coupler type never stated, so
  no class can be chosen); Table S2 circulating powers; RF-induced mode drift (Supp. Figs. S6-S7).
- Judgment calls (coordinator questions):
  1. Class / isolation: I_ij = |S_ij|^2 / |S_ji|^2 between frequency channels of one bus, both conversions measured with
     left-to-right input. Entered as `isolation_db` on a circulator row (the paper's isolation parameter for a
     frequency-port circulator; mirror symmetry checked in Fig. S5). Contrast with dostart2020a (D581: |S32|^2/|S23|^2
     "assuming perfect filtering", kept out) and D419 / D513: here the full circulator is built and characterized,
     no filtering assumption is stated. If the coordinator prefers `conversion_contrast_db`, move the 4 isolation rows.
  2. D417: printed "nearly 40 dB" vs the Fig. 2(b) / 2(c) I31 curve at the same RF powers, which peaks at about 35 dB.
     Printed value kept, conflict in notes.
  3. Platform `lnos_rib`: LN on sapphire stated, etch depth not stated (rib vs fully etched unknown); `lnos_rib` is the only
     LN-on-sapphire value. Alternative: empty (D422 / D423).
  4. Wavelength 1543.6 nm (Methods laser lock; Table S1 1543.605 nm) on the Fig. 2 operating point; the > 25 dB and 3 dB
     statements carry no wavelength: c_band inferred (abstract "near 1550 nm").
- Fab / facility: fab org_stanford_university (contributions "J.F.H. fabricated the device", all authors Stanford, D395).
  Facility org_stanford_nano_shared_facilities (p.6). Missing / unmapped: "nano@stanford labs" (p.6, "Work was performed
  in part in the nano@stanford labs ... NNCI"), facility role. Registry `org_nano_stanford` is described as the 2026 merged
  successor (D80d), so it was not used for this 2021 print; coordinator to decide (map to org_nano_stanford, or treat the
  2021 NNCI site name as an alias of SNSF / SNF).

## che2024: 4 components / 26 metrics

- `cmp_lit_che2024_edwa1_22p2cm` (amplifier.rare_earth, 11) and `cmp_lit_che2024_edwa2_12p5cm` (12): Fig. 2 statements
  (gain 12-24 dB off-chip, output about 12 dBm at -12 dBm input and > 14.5 dBm at 2.8 dBm, 1560 nm probe) entered on both
  rows because the text states them for both EDWAs ("almost the same performance"; lin2023 precedent), per-device figure
  reads in component notes; on-chip gain 17.8-29.8 dB and output > 17.4 dBm derived (+2 x 2.9 / +2.9 dB, D166 / D394).
  EDWA #1: Experiment 1 off-chip gain about 11 dB over 191.4-195.6 THz (on-chip 16.8 dB derived, Fig. 3(d) caption 5.8 dB).
  EDWA #2: Experiment 2 off-chip 10 dB, on-chip 16 dB (derived, printed), about 14 dBm total fiber output over 16
  channels. Lengths 22.2 / 12.5 cm, footprints ~1.8 / ~1.0 mm2, core 0.7 x 2.1 um (all derived, D157).
- `cmp_lit_che2024_inverse_taper_uhna7` (fiber_chip_coupler.edge, 2): about 2.9 dB per facet in the C band (measured,
  D167), UHNA7 MFD about 3.2 um (specification).
- `cmp_lit_che2024_er_sin_waveguide` (waveguide_platform.straight, 1): "minimum background loss below 5 dB/m" (TE) as
  < 0.05 dB/cm `author_estimate` (no citation in the sentence, origin and wavelength not stated; D80i borderline).
- Not entered: cited ref. 12 values (> 30 dB gain, 145 mW, NF 7.1 dB / about 7 dB average) and the damascene "< 3 dB/m"
  (ref. 17), rule 3; on-chip "about 20 dBm" (p.6, no device or operating point; likely ref. 12, D159); parasitic lasing
  threshold "gain > 20 dB / on-chip net > 26 dB" (inconsistent with the 24 dB Fig. 2 points, in notes); Er concentration
  3.25e20 cm-3 and simulated 50 % overlap (no parameter); system metrics (NGMI, 25.6 Tb/s, spectral efficiency), setup
  parts (LiNbO3 I/Q modulator, BPDs, WSS, EDFA: rule 13).
- Fab empty (passive "was fabricated using the photonic damascene process [17]", authors at Nokia Bell Labs, EPFL, UCF;
  D80b). `process_name` "photonic damascene process (ref. 17)" (named flow, cited). No facility named.
- D408: the preprint extends the authors' OFC 2023 Th4B.3 (ref. 14); no value or figure is attributed to it, all kept.

## javid2021: 1 component / 4 metrics

- `cmp_lit_javid2021_lensed_fiber_facet` (fiber_chip_coupler.edge, 4): chip-to-lensed-fiber out-coupling loss 6.9 dB
  per facet (App. B, measured, D167; band unspecified, photons span 1.2-2 um); film 600 nm, etch 300 nm, BOX 4.7 um
  (design_target, D402). Platform lnoi_rib.
- No SPDC converter row: the frequency_converter class has no parameter for any reported value (rule 9). Registry gap
  (photon-pair metrics, D250 / D454 candidates), values with locators: SPDC bandwidth 100 THz total / 50 THz 3-dB
  half-bandwidth from the measured signal side (p.4, Fig. 4(a), pump 770.4 nm, centre 1540.8 nm); generation efficiency
  13 GHz/mW (spectrometer, p.4), 7.8 GHz/mW (SNSPD, p.5 Fig. 5(b)), 778 MHz/mW and 38 MHz/mW/nm in 17 nm WDM channels
  (p.5); CAR 20,248 +/- 5,204 full spectrum and 152,710 +/- 32,772 filtered (p.5-6); CAR x PGR 19 / 0.8 GHz (p.6);
  two-photon interference visibility 98.8 % (p.6); non-degenerate point ~70 nm signal width at 1250 nm (p.4). Proposed
  definitions: `pair_generation_efficiency_hz_per_mw` (on-chip pair rate per pump power, detection path in condition),
  `spdc_bandwidth_thz` (criterion in condition), `car` (coincidence-to-accidental ratio, PGR in condition),
  `two_photon_visibility_pct`. Also a phase-matching wavelength on frequency_converter (D419 widening not yet in the
  registry).
- Not entered: waveguide width (not printed for the fabricated device; Fig. 1 design sweeps 1-2 um), poled length 5 mm
  (only geometry of the absent converter row; noted), poling period (not printed), pump rejection 120 dB (setup filters).
- Fab empty (passive "The device was fabricated ...", all authors University of Rochester, D80b). Facility
  org_cornell_nanoscale_facility (p.9 "performed in part at the Cornell NanoScale Facility"). LNOI from NanoLN (note).

## poulvellarie2021: 3 components / 13 metrics

- `cmp_lit_poulvellarie2021_ingap_type2_shg` (frequency_converter.shg, 8): 2500 %/(W cm2) and 12 %/W at a 1536 nm
  TE00 + TM00 pump, both `gt` `author_estimate` (lower bound by the paper's statement, all SH output assumed collected;
  input power rests on the estimated 6 dB coupling loss); theoretical limit 102400 %/(W cm2) `simulated`; width 850 nm
  (SEM, measured), InGaP 320 nm, 1.4 mm crystal-axis section, BOX 3 um, HSQ 0.2 um.
- `cmp_lit_poulvellarie2021_ingap_wire_wg` (waveguide_platform.straight, 2, D396): 12 dB/cm pump modes (1.2 dB/mm),
  64 dB/cm SH TM01 (6.4 dB/mm), derived unit conversions, wavelengths 1536 / 768 nm inferred.
- `cmp_lit_poulvellarie2021_input_taper` (fiber_chip_coupler.edge, 3): 6 dB coupling loss `author_estimate` ("estimated",
  origin not stated), C band inferred; taper 200 um long; "5 um wide" stored as `width_nm` 5000 (end not stated, D523).
- Platform `other` (InGaP on insulator; akin2024 / thiel2026 precedent). Etch depth of the wire not stated.
- Not entered: kappa_exp > 500 (W^0.5 m)^-1 and kappa values (no parameter; converted efficiencies entered); simulated
  design optimum 620 x 300 nm (kappa_max i3675) and the type I comparison 2816 (design-space results, no device);
  phase-matching pump wavelength 1536 nm (no frequency_converter parameter, registry gap); max SH power ~2 uW (Fig. 4, no
  parameter); 45 deg sections' loss; values from refs. 5, 20, 21 (rule 3); chi(2) 220 pm/V (ref. 17).
- Fab empty: "We fabricate ... [19]" with authors at ULB, Ghent University-IMEC, Angers, Thales, C2N; no org named
  (D154 / D395). No facility statement.

## Registry gaps (summary)

- Photon-pair source metrics (javid2021, above).
- Phase-matching / centre wavelength on frequency_converter (poulvellarie2021 1536 nm p.3-4; javid2021 770.4 nm pump).
- Inter-resonator coupling rate (herrmann2022 mu12 / mu23 1.864 / 1.861 GHz, Supp. Table S1).
- `conversion_contrast_db` on nonreciprocal (D419) if the coordinator re-files herrmann2022 isolation (question 1).
- Isolation bandwidth in frequency (herrmann2022 "more than a few hundred megahertz", no number, so no value lost now).

## Missing orgs

- "nano@stanford labs" (herrmann2022 p.6, facility): mapping question above, not a new org request.
- None else: Stanford, SNSF, Cornell NanoScale Facility are registered; che2024 / poulvellarie2021 / javid2021 have no fab org.
