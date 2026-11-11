# lit_122 batch report (2026-11-11)

All six cached texts match their source rows (page-1 title); none is another paper or only a correction / erratum; no
garbled text layer. Supplements are not cached. Figure values were read from the cached `page_NN.png` / `img_pNN_k.png`
renders. Dry-run: +21 components, +138 metrics, 0 errors; the one warning (ni2025b m18 / m4) is on an existing merged row,
not from this batch. All sources are `restricted_local_only`: no quotes in the output.

| paper | components | metrics |
|---|---|---|
| zhang2026 | 3 (amplifier.rare_earth; waveguide_platform.straight; fiber_chip_coupler.edge facet; one chip, D396) | 12 |
| cao2025 | 2 (amplifier.soa, single- and dual-pass as conditions; fiber_chip_coupler.edge facet, D396) | 19 |
| yang2021 | 10 (waveguide_platform.transition; fiber_chip_coupler.edge x2 (SiN1 / SiN2); chip_chip_coupler.butt x2 fabricated (bonded DFB) + 1 design (monolithic EEL); laser.dfb x2 (commercial die; monolithic EEL design); crossing.multilevel (simulated only); waveguide_platform.straight) | 48 |
| moodie2024 | 3 (laser.pcsel headline d = 0.25a / a = 477 nm; 2 array-level sibling design families from Fig. 5(a), D165) | 22 |
| zhang2024 | 1 (laser.dfb, 16-channel array, array-level row, D165) | 20 |
| mangal2021 | 2 (fiber_chip_coupler.grating, uniform O-band GC; micro_optics.integrated_lens, backside Si microlens interface) | 17 |
| total | 21 | 138 |

## Fab / facility orgs

- zhang2026: fab `org_jilin_university` on all 3 rows, borderline (rule 12 / D72): all authors at Jilin University;
  first-person "we fabricated" the TBY-Er glass (p.2, p.10) and "we ... optimized the PLD fabrication process" (p.5-6);
  the waveguide patterning sentence is passive (p.4). Auditor: confirm or empty per D80b.
- cao2025: fab empty (passive "was fabricated into ... ridge waveguide devices", p.2). Acknowledgment (p.8) thanks two
  National Information Optoelectronics Innovation Center staff for device packaging: packaging, not fabrication, so not
  used (org exists as `org_national_information_optoelectronics_innovation_center` if the coordinator rules otherwise).
- yang2021: SiN chip fab empty (passive, p.6; "our E-beam lithography" and "foundry processes" name no org). Fab
  `org_beijing_university_of_posts_and_telecommunications` only on the two fabricated chip_chip_coupler.butt rows
  (first-person die bonding "we attached ... by die-bonding", all authors at BUPT; D399). Commercial DFB laser die vendor
  printed as "APPLIED OPTOELECTRONICS" (p.8): missing from the registry, so the laser.dfb device-under-test row has fab
  empty (vendor = fab by rule 12 once the org exists).
- moodie2024: fab empty (all authors Huawei Ipswich Research Centre, passive fabrication; D80b).
- zhang2024: fab empty (passive "is fabricated", p.4; authors HUST + Ningbo Ori-Chip).
- mangal2021: GC fab `org_imec`, borderline D84b (acknowledgment p.13 thanks imec's SiPh integration team for the dies
  "fabricated from 200-mm wafer-scale processing"); `process_name` "200-mm wafer-scale processing" (printed wording,
  imec in notes). Microlens fab `org_centre_for_microsystems_technology`, borderline D84b (CMST staff thanked for microlens
  RIE and die lapping, p.13; mangal2019a precedent); facility `org_ghent_photonics_research_group` (SiN AR deposition,
  p.13; D470 mangal2019 precedent).

## Missing orgs

- "APPLIED OPTOELECTRONICS" (vendor of the commercial 1550 nm DFB laser die; lit:yang2021 p.8): fab role on
  `cmp_lit_yang2021_commercial_dfb_die` (rule 12 vendor of a device under test).

## Values not entered and why

- zhang2026: signal enhancement 13 / 10.89 dB (-15 dBm) and 11 / 9.59 dB (-10 dBm) (no parameter; in notes); fluorescence
  lifetime 4.42 ms, PL FWHM ~52 nm, n = 1.841 (bulk glass material properties, no parameter); simulated overlap factors;
  film roughness Ra; Table 1 comparison values (other works, rule 3); 1.8 dB/cm cited SU-8 device.
- cao2025: beam divergence half-angles 15.6 / 27.7 deg (beam_divergence_deg not allowed on amplifier or fiber_chip_coupler:
  registry gap); AR reflectivity ~0.3 % (calibration sample, no amplifier parameter); gain enhancement differences
  (11.2 / 14.6 / 13.2 / 5.9 dB) and SOP reductions (2.98 / 4.08 dB) (differences, notes); gain-peak shift 0.6 nm/mA vs ASE
  0.06 nm/mA printed as consistent (conflict, D417, notes); temperature shift ~10 nm / 20 C (thermal_drift not allowed on
  amplifier); PL / QD dimensions (material).
- yang2021: grating period 650 nm, duty cycle 61.5 %, 20 periods, offset -20 nm of the interlayer coupler (period_nm /
  fill_factor / n_periods not allowed on waveguide_platform; subwavelength_period_nm not used because the paper also states
  a Bragg diffraction condition, so which parameter applies is ambiguous); measured 1-dB bandwidth > 76 nm of the interlayer
  coupler (bw_1db_nm not allowed on waveguide_platform); simulated 124.8 nm bandwidth (definition not stated); system
  total 9.5 dB / > 58.1 nm (sum of two rows, in notes); measured SiN2-coupler-with-crossing penalty ~1.5 dB (not an
  isolated crossing loss, notes); DFB threshold from Fig. 5(a) (not labelled).
- moodie2024: PC fill factors 11.3-17.4 % (hole-area fraction, not the registry fill_factor); 120 um contact / 300 um
  aperture diameters (no aperture parameter); Rq roughness; PL ratio 73 %; Fig. 9 curves at 35-75 C (only printed points
  entered).
- zhang2024: center-frequency deviation < 2 GHz after alignment (no frequency-offset parameter; notes); TDTW model inputs
  (gain, internal loss 8.53 /cm, injection efficiency, confinement; notes); LWEF (Fig. 8(c)); per-channel threshold / slope
  points of Fig. 5(b) (range entered instead); channel frequencies 189.2-192.2 THz (figure read, notes only).
- mangal2021: angular 1-dB tolerance +/- 0.6 deg (no parameter: registry gap); simulated ROC tolerance -100 / +180 um; 2 dB
  AR improvement (in notes); projected < 2.8 / < 2 dB (projections for hypothetical reflector gratings); 1.85 dB expected
  Fresnel loss (calculated expectation, also in mangal2019a); 2.3 / 1.5 dB reflector / apodized GC efficiencies and the
  0.5 dB misplacement penalty (cited, rule 3); lens sag (not labelled); intro +/- 2.5 um standard-GC tolerance (cited).

## Judgment calls

- zhang2026 internal net gain `derived` (SE minus 1.92 dB/cm x 0.4 cm, D166); the paper uses the 1550 nm loss at 1538 nm
  too (13 - 12.23 = 0.77). Net-gain span 1510-1570 nm entered as gain_bandwidth_nm 60 `ge` (measured range is the limit).
  "exceeds 25 mW" for net gain entered as pump_threshold_mw (kuyken2011 / li2025 transparency precedent).
- cao2025 on-chip gain / NF / SOP kept `measured` (on-chip referencing not shown as arithmetic; beeck2021 / davenport2016
  precedents) while the facet losses are `derived` (paper describes them as the difference of two L-I curves). Single- and
  dual-pass kept on one SOA row (same chip, configuration in condition, rule 9); ASE output powers converted mW -> dBm
  (`derived`).
- yang2021 per-coupler losses `measured`, method unspecified (setup calibration stated, subtraction not printed, D167);
  laser-to-chip losses `derived` (de-embedded, D394). Design-only monolithic EEL and its SiN-filled interface kept as
  `row_kind: design` rows (simulated threshold 3.6 mA, SMSR > 40 dB, mode 2.6 x 1.2 um, 3.0 dB coupling). Abstract /
  conclusion "gap 1.4 um" vs body spacer 1 um: gap_nm 1000 with the conflict in notes (D417). DFB spot size 3 x 1.7 um
  (IR camera, level not stated) entered as mfd_chip_um approx with that caveat. Commercial DFB platform left empty
  (material not stated, D422 / D423).
- moodie2024 "up to 81 mW" and "up to 7.8 %" -> `le` (rule 7); CW threshold ~130 mA read off Fig. 6(a) (+/- 10 mA);
  sibling lattice designs as two array-level rows from Fig. 5(a) markers (+/- 1 mW).
- zhang2024 slope efficiency kept `measured` in W/A (Fig. 5(b) axis prints W/A; text 0.3 mW/mA, D256); linewidths kHz ->
  Hz `derived`; kappa 10 /cm `author_estimate` (design-model input); thermal resistance 27 K/W kept as own measurement
  although the sentence adds "as same as in [19]" (D80i borderline, noted).
- mangal2021 GC 7.5 dB per grating `loopback_half` `measured` (Table 2 value of a fiber-to-fiber spectrum, no halving step
  printed; D452). Single-interface 8.5 dB `derived` (two-interface spectrum and the 2 dB AR step), 3 dB lens / substrate
  penalty `derived` de_embedded (mangal2019a m2 precedent), 0.5-1 dB lens-only contribution `author_estimate`. Per-lens
  1-dB longitudinal tolerances ~580 / ~810 um interpolated from Fig. 11 points (`extracted_from_figure`, +/- 30 um). Substrate
  600 um (body) vs 580 um (Table 2, Figs. 10-11) noted (D417).

## Registry gaps (skipped value + locator + proposed definition)

- `bw_1db_nm` on waveguide_platform (transition): yang2021 interlayer coupler > 76 nm (p.1, p.7). Proposed: allow the
  existing definition for waveguide_platform.
- `period_nm`, `fill_factor`, `n_periods` on waveguide_platform (grating-assisted transitions): yang2021 650 nm / 0.615 / 20
  (p.4-5). Proposed: allow the existing definitions (period of a diffractive grating inside a transition).
- `beam_divergence_deg` on amplifier and fiber_chip_coupler: cao2025 15.6 / 27.7 deg half-angles (p.4; D437 listed it for
  fiber_chip_coupler). Proposed: allow the existing definition (half / full and level in condition).
- `tol_1db_angular_deg` (micro_optics, fiber_chip_coupler, fiber_interface): mangal2021 +/- 0.6 deg (p.1, p.12; p.11 Fig. 10(b);
  D551 also lists angular tolerances). Proposed: angular misalignment for 1 dB excess loss, half-width +/- value.
- `signal_enhancement_db` (amplifier): zhang2026 13 / 10.89 / 11 / 9.59 dB (p.8). Proposed: pump-on / pump-off signal
  ratio as measured (fiber-to-fiber), no loss correction; internal net gain stays in gain_db.
- `upper_state_lifetime_us` (amplifier; already a candidate, D429 / D448): zhang2026 4.42 ms bulk-glass fluorescence
  lifetime (p.3 Fig. 1(d)).
- `frequency_offset_ghz` (laser / wdm; D443 candidate): zhang2024 < 2 GHz channel deviation from the 200 GHz grid
  (p.6 Fig. 6(b)).
- `aperture_diameter_um` (laser; D433 candidate): moodie2024 120 um p-contact window, 300 um n-side emission aperture (p.4).

## Coordinator decisions

1. zhang2026 Jilin University fab (first-person glass / PLD-film statements, passive waveguide step): keep or empty.
2. Org round: add APPLIED OPTOELECTRONICS (vendor), then set it as fab on `cmp_lit_yang2021_commercial_dfb_die`.
3. yang2021 grating parameters: registry extension (period / fill / n_periods on transitions) vs `subwavelength_period_nm`.
