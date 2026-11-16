# lit_135 batch report

Distilled 2026-11-15 under the pic-component-distill skill (Contracts v4-v7, DevLog-002 D30-D84, DevLog-007 D150-D577).
Totals: 20 components, 80 metric rows. `merge_component_staging.py data/_staging/components/lit_135 --dry-run`:
+20 components, +80 metrics, 0 errors (the one warning printed concerns a merged ni2025b row, not this batch).
Page-1 check: every cached text is its source row's work; yang2024c and dostart2020a are arXiv v1 texts (yang2024c
preprint title "Titanium:Sapphire-on-insulator for broadband tunable lasers and high-power amplifiers on chip"
differs from the Nature title; same authors and work, D430 / D433). Figures read on the page renders.

## Per paper

| paper | components | metrics | classes |
|---|---|---|---|
| chang2018a | 4 | 17 | frequency_converter.shg, waveguide_platform.straight, fiber_chip_coupler.edge x2 |
| yang2024c | 9 | 37 | resonator.disk, laser.other, amplifier.other x3, laser.tunable x4 |
| akiyama2007 | 3 | 9 | amplifier.soa x3 (Fig. 17 only) |
| dostart2020a | 3 | 6 | nonreciprocal.other, resonator.coupled_rings, resonator.ring |
| kaspar2015 | 1 | 11 | amplifier.soa |

### chang2018a (GaAs-on-insulator SHG, LPR 2018)
- Rows: SHG waveguide 1.4 mm (13,000 %/W/cm2, 250 / ~300 %/W, simulated 32,000 %/W/cm2, geometry), waveguide loss
  1-2 dB/cm (FP method, measured), input inverse-taper port (3.5 dB), output facet (6 dB pump, 5.2 dB SH).
- Efficiencies `author_estimate`: the plotted in-waveguide powers rest on coupling losses the paper calls estimated
  (p.7; rule 4, nikolai2025 / li2025a precedents). Coupling losses `author_estimate` (origin not stated, D418).
- Not entered: sinc2 FWHM 0.93 nm (theory 0.90 nm) - no acceptance-bandwidth parameter for frequency_converter;
  calculated 1,000,000 %/W with HR coatings (hypothetical); simulated phase-matching sensitivities (Fig. 5); surface
  roughness 0.3 / 0.2 nm RMS; bonding yield > 95 %; Table 1 (cited material constants).
- Printed inconsistency noted (D417): input coupling printed as "0.45 (3.5 dB)" (coupled fraction) while the output
  terms "0.75 (6 dB)" / "0.7 (5.2 dB)" are loss fractions.
- Fab / facility: none stated (passive process text; acknowledgment thanks named people for help in fabrication,
  no org).

### yang2024c (Ti:sapphire-on-insulator lasers and amplifiers, Nature 2024; arXiv v1 text)
- Rows: 50 um microdisk (Q 1.3 M at 805 nm, 0.5 dB/cm), microdisk laser (290 uW threshold), straight 0.485 mm
  amplifier (64 dB/cm), 8 mm spiral amplifier (> 20 dB, figure peak ~24.5 dB, passive loss 4.9 / 3.9 dB at
  700 / 950 nm from Fig. 2(c), 60 mW = 17.8 dBm on-chip CW output, footprint, geometry, 79 deg sidewall), pulsed
  amplifier of unnamed length (17 dB), tunable ring laser design row (59 nm and > 50 nm single-mode tuning, SMSR 30.6 /
  23.2 / 22.2 dB, -7.3 / up to -6.8 dBm, 140 kHz, footprint < 0.15 mm2, ring radius, gain-section geometry) and three
  coupling-gap siblings (325 nm: 6.9 mW best threshold; 375 / 425 nm: inset threshold ranges; 425 nm: 1.8 mW).
- Judgment calls: Q 1.3 M entered as `q_loaded` (Fig. 1(e) label Q_L) although p.3 calls it intrinsic (conflict in
  notes, D417); 0.5 dB/cm `author_estimate` (n_g not stated, D76); 60 mW output assigned to the 8 mm spiral (p.4
  paragraph, Fig. 2(a) both-end pumping, Methods double-side pumping for Fig. 2(d)); pulsed result on its own row
  because 3.4 mm and 8.1 mm spirals were studied and the pulsed device is not named (D159 / D422); single-mode laser
  metrics on a design-level row because the characterized device's gap is not stated; amplifiers `amplifier.other`
  (Ti3+ is not a rare-earth dopant).
- Not entered (registry gaps, values with locators): pulse energy 2.3 nJ and peak power 1.0 kW (p.5, Fig. 2(f));
  laser optical slope efficiency 2.9 % (p.5, Fig. 3(b); D538 candidate); mode-hop-free tuning 91 pm / 36.4 GHz (p.5;
  D538 candidate); fluorescence lifetime 3.09 us (p.3; upper-state lifetime candidate, D429 / D448); "> 30 dB/cm
  across a 100 THz bandwidth" (p.4; span printed only in THz); ASE bandwidth > 100 THz (p.4); stabilization
  0.073 pm RMS (p.5); surface roughness 1.6 A RMS (p.3); simulated overlaps 98.8 / 99.5 / 96.5 %; effective mode
  area 0.62 um2; abstract "700 - 950 nm" bandwidth (criterion not stated).
- Fab: `org_stanford_university` only on the two microdisk rows ("we fabricate whispering gallery mode resonators",
  p.3; all authors at Stanford, D72). EBL amplifier and laser rows fab empty (passive Methods; "we develop a pattern
  transfer process" is not a fabrication statement, D80b). Facility on all 9 rows: `org_stanford_nano_shared_facilities`
  + `org_stanford_nanofabrication_facility` ("Part of this work was performed at the Stanford Nano Shared Facilities
  (SNSF)/Stanford Nanofabrication Facility (SNF)", p.8; printed names, D440).

### akiyama2007 (Quantum-dot SOAs, invited review, Proc. IEEE 2007)
- Stopped on the headline device: the 6.15 mm, 2.2 um stripe QD SOA (gain > 25 dB, NF < 5 dB, Psat > 20 dBm over
  90 nm, Figs. 3-4; 22.8 / 23.1 dBm distortion-free / penalty-free output, Figs. 6-7; QW comparison SOA Psat 17 dBm)
  is attributed to the authors' ref. [21] (OFC 2004 PDP12): Sec. II device sentence "... respectively [21]" (p.2),
  Fig. 2 caption "[21]", p.1-2 bandwidth sentence "[21]", and Fig. 8 labels these points "Fujitsu[21] (QD / 2004)".
  Not entered (rule 3, D259 / D408 figure clause). Coordinator question 1 below.
- Entered: Fig. 17 gain spectra (no citation in caption or text; ref. [52] "unpublished" exists but is not cited in
  the text): standard SK QD SOA 3.15 mm at 1 A (TE ~14 dB, TM ~-2 dB), 22-fold columnar QD SOAs 6.15 mm at 2 A with
  2-ML spacers (TE ~40, TM ~23.5 dB) and 2.5-ML spacers (TE ~27, TM ~43 dB); all `extracted_from_figure`, reading
  +/- 1 dB / +/- 5 nm, reference plane not stated.
- Platform: `inp` on the columnar rows (Sec. VI: MOVPE InAs QDs on InP in the SOA structure); empty on the standard
  SK row (substrate not restated for that device, D422).
- Not entered: Sec. V regenerator (4 dB receiver-sensitivity gain at BER 1e-9, 40 Gb/s; link-level), FWM alpha
  parameter ~3 (Fig. 19(b); no parameter), PL spectra (Figs. 15-16).
- Fab: empty ("We have realized ... columnar QDs", authors at Fujitsu Laboratories / QD Laser Inc. and the
  University of Tokyo; D154).

### dostart2020a (Optical isolation using microring modulators, OL 2020; arXiv v1 text)
- Rows: non-reciprocal section (`nonreciprocal.other`: 18.1 dB insertion loss, < 20 dB over the ~2 GHz contrast
  bandwidth, footprint 300 x 50 um), dual-ring converter (`resonator.coupled_rings`: 26.3 GHz supermode splitting,
  6.5 GHz linewidth), all-pass phase-shifter ring (`resonator.ring`: 7.4 GHz linewidth).
- Not entered: the printed 13.1 dB "isolation" and ~2 GHz 3-dB "isolation bandwidth" - the paper builds only the
  non-reciprocal section and assumes ideal filters, so the number is a forward / backward converted-sideband ratio,
  not a port-to-port isolation (sohn2018 / kittlaus2020a ruling, D419, D513). Coordinator question 2 below.
- Modulator drive metrics (1 GHz/V resonance shift, 0.21 Vpp) are EO-atlas scope (rule 2): conditions only.
  4 Gb/s OOK transmission: link-level.
- No wavelength is printed anywhere: `band: unspecified` with a note (EDFA in the data setup suggests C band).
- Platform empty (SOI never stated, D423). Fab `org_imec` ("We fabricated ... in an active silicon photonics process
  (IMEC)", p.3; D455); `process_name` "active silicon photonics process (IMEC)" as printed. Authors' orgs (CU
  Boulder, Boston University) not added (two orgs).

### kaspar2015 (Hybrid III-V/Si SOA, PTL 2015)
- One row (packaged hybrid SOA): fiber-to-fiber gain 10 dB (1540 nm, 90 mA, 20 C) and 3-dB bandwidth 26 nm
  (measured); internal gain up to 28 +/- 2 dB and its 30 nm bandwidth (`author_estimate`); 7.5 dB at 1550 nm /
  75 mA; fiber Psat_in -2.5 dBm and Psat_out 2 dBm (75 mA); on-chip output-waveguide Psat ~9.3 dBm at 80 mA (Fig. 2
  read, `author_estimate`); fiber-referred NF ~17 dB (`derived`, stated TE assumption) and internal NF ~10 dB
  (`author_estimate`); active length ~1.1 mm.
- Judgment calls: the paper says it "first give[s] the static performance of a hybrid III-V/silicon SOA that we
  have previously presented in [14]" (ECOC 2014, same packaged device), but the gain / saturation / NF sentences and
  Figs. 2-4 cite nothing, so they are kept (D408). The per-side insertion-loss estimate (9 +/- 1 dB = 7 dB grating
  couplers + 2 dB transition, GC 3-dB bandwidth 60 nm) ends with "[14]": not entered (rule 3, D259); values
  computed with it are `author_estimate` (rule 4, D429 ahmadi2022 precedent). Coordinator question 3 below.
- Not entered: transmission-loop results (link-level), "-3 dBm vicinity" (restates the -2.5 dBm row).
- Fab empty: passive "was fabricated" (p.1), authors at III-V Lab, Bell Labs (Alcatel-Lucent), Tyndall National
  Institute and CEA-Leti; packager not named.

## Missing fab / facility orgs

None needed by a row. All org ids used exist in the registry (`org_stanford_university`,
`org_stanford_nano_shared_facilities`, `org_stanford_nanofabrication_facility`, `org_imec`).

## Coordinator questions

1. akiyama2007: keep the headline QD SOA values out (recommended: yes; Fig. 8 assigns them to "Fujitsu[21]
   (QD / 2004)", the D455 / D465 figure-attribution clause). If the coordinator reads the review as re-presenting
   the measurements, the values with locators are: gain > 25 dB, NF < 5 dB, Psat > 20 dBm over 90 nm (p.3, Fig. 4;
   2 A), Fig. 3(b) 3-dB saturation output ~25 dBm at 1550 nm, 22.8 dBm waveform output and 23.1 dBm penalty-free
   output at 2.5 A, 40 / 10 Gb/s, 1550 nm (p.3, Figs. 6-7); device 6.15 mm, 2.2 um stripe, 5 QD layers, 8 deg tilt.
2. dostart2020a: keep the 13.1 dB contrast out of `isolation_db` (recommended: yes, consistent with D419 / D513);
   it fits the open registry candidate `conversion_contrast_db` (nonreciprocal) when that is added.
3. kaspar2015: internal gain 28 +/- 2 dB and internal NF ~10 dB kept as `author_estimate` on the cited loss estimate
   (D429); the alternative strict reading of rule 3 ("values computed from cited values are not entered") would
   delete m3, m4, m8, m10.

## Registry gaps (skipped value + locator + proposed definition)

- `bw_fwhm_nm` (or an acceptance-bandwidth parameter) on frequency_converter: chang2018a sinc2 FWHM 0.93 nm, p.7-8
  ("phase-matching acceptance full width of the conversion-efficiency spectrum, fundamental wavelength").
- `pulse_energy_nj`, `peak_power_kw` on amplifier: yang2024c 2.3 nJ / 1.0 kW, p.5 (already candidates, D429).
- Laser optical slope efficiency in %: yang2024c 2.9 %, p.5 (D538 candidate).
- Mode-hop-free tuning range in GHz on laser: yang2024c 36.4 GHz (91 pm), p.5 (D538 candidate).
- `upper_state_lifetime_us` (gain medium): yang2024c 3.09 us, p.3 (D429 / D448 candidate).
- `conversion_contrast_db` on nonreciprocal: dostart2020a 13.1 dB, p.4 (D419 candidate).
- `isolation_bw_ghz` / contrast bandwidth in GHz on nonreciprocal: dostart2020a ~2 GHz, p.5 (only nm exists).
- `rms_roughness_nm`: chang2018a 0.3 nm (p.6), yang2024c 0.16 nm (p.3) (D432 candidate).
