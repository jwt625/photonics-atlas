# Batch lit_118 report (distiller, 2026-11-09)

Papers: zhao2016 (garbled text layer), hsu2025, itoh2024a, li2025c, zhang2023b, deng2020, vocht2024, arsanjani2024,
osorniomartinez2025. All nine cached texts are their source rows' papers (page-1 titles match); none is a correction or
erratum. All sources are `restricted_local_only`: facts and locators only, no quotes.

Validation: `merge_component_staging.py data/_staging/components/lit_118 --dry-run` -> +30 components, +167 metrics,
0 errors, no warnings on this batch.

| Paper | Components | Metric rows |
|---|---|---|
| zhao2016 | 5 | 18 |
| hsu2025 | 2 | 9 |
| itoh2024a | 5 | 24 |
| li2025c | 3 | 26 |
| zhang2023b | 4 | 25 |
| deng2020 | 3 | 15 |
| vocht2024 | 2 | 11 |
| arsanjani2024 | 4 | 17 |
| osorniomartinez2025 | 2 | 22 |
| Total | 30 | 167 |

No paper has 0 rows.

## Per paper

### zhao2016 (GFP 2016, 2 pages; text layer font-garbled)

- Rows: Vernier ECL (`laser.tunable`, platform `other`), two intracavity rings (`resonator.ring`, D400; design FSR
  1.63 / 1.58 nm author_estimate, circumferences as `length_um`), TriPleX double-stripe waveguide
  (`waveguide_platform.straight`, < 0.1 dB/cm author_estimate), HHI SOA gain chip (`amplifier.soa`, 3-dB gain width
  30-35 nm as `bw_3db_nm`, author_estimate).
- All values were read from page renders made from the cached PDF at the scratchpad (the text layer is a constant
  character shift with digits dropped); every entered number was confirmed on the rendered page.
- Fab: empty on the chip and laser rows (passive "are fabricated"; "some of us have fabricated" refers to refs.
  [9]-[11]). SOA row fab `org_fraunhofer_heinrich_hertz_institute` (gain chip "provided by" HHI, rule 12 vendor clause).
  `process_name` "TriPleX double-stripe Si3N4/SiO2" kept with no foundry named (Contract v7 note on the rows).
- Not entered: ring heater 14 V for 2 pi (no power), SSC taper 4.3 um / 35 nm (geometry only, no coupling loss), RF
  beat width 130 kHz (the 65 kHz linewidth row is its half), 28 tuned channels.
- Judgment: the < 0.1 dB/cm sentence has no citation of its own but follows the platform citation [12]; kept as
  author_estimate (D80i borderline), flagged for the audit.

### hsu2025 (850 nm Zn-diffusion SM VCSEL)

- Rows: VCSEL (`laser.vcsel`, `gaas`): 3 mW at 4 mA, Pmax 4.2 mW and 3 V at 6 mA (figure labels), threshold about
  0.7 mA (figure read), BTB 3-dB bandwidths 16 / 22 / 22 GHz at 2 / 4 / 6 mA (Fig. 4(a) legend), lasing peak about
  856.7 nm at 4 mA (figure read). Lensed-fiber coupling row (`fiber_chip_coupler.other`): 60.5 % VCSEL-to-SMF-28 lens
  fiber, per_coupler.
- Not entered: fiber-channel bandwidths after 500 m / 1 km graded-index SMF (25 / 39 GHz) and OM4 MMF values: chirp
  plus dispersion link values (D542 link-value precedent; details in component notes). Coupling efficiency of the
  authors' earlier devices (refs. 17, 18). Eye / BER results (system). Oxide aperture 5 um (no parameter).
- Fab empty: "home-made" with authors at National Central University and Corning; which org fabricated is not stated
  (D80b). Epi grown by Intelligent Epitaxy Technology Inc. (supplier, note only).

### itoh2024a (1.3 um InP PCSEL with metal reflector)

- Rows: +150 nm cladding PCSEL (CW 397 / 188 mW at 25 / 50 C, WPE 20.7 %, 0.13 ohm differential resistance, SMSR
  49 / 51 / 43 dB from Fig. 5(b) labels, 0.10 nm/K as 100 pm/K derived, divergence < 1.6 deg, > 12 W pulsed, slope
  0.4 / 0.43 W/A, pulsed Fig. 3 ranges); three phase-series siblings +0 / +50 / +100 nm (Fig. 3(b), (c) range reads
  only); metal reflector (`reflector.other`, > 30 % and about 40 % around 1.3 um; D396 cross-note).
- Not entered: CW threshold (Fig. 4(a) onset too coarse to read reliably), FWHM divergence values (Fig. 6(b) only),
  contact resistivity, mesa diameter 200 um (no parameter), comparison with refs. [16,17].
- Fab empty (first-person "we fabricated the p-side electrode", authors at Sumitomo Electric and Kyoto University,
  most dual-affiliated; itoh2024 precedent). `process_name` left empty (no named process; Contract v7 "generic"
  rule; the merged itoh2024 rows carry a process description there).
- itoh2024a is a different paper from the merged lit:itoh2024 (1.55 um size series); no overlap.

### li2025c (1.3 um InGaAlAs DFB with MQW passive DBR)

- Rows: 150 um and 200 um DFB + 130 um DBR lasers (`laser.dfb`, `inp`) with thresholds, slopes (printed mW/mA,
  stored W/A derived), > 13 mW, SMSR, series resistance, 3-dB modulation bandwidths at the stated currents, ridge and
  DFB-section length; reference single-section 200 um DFB (17 GHz).
- Judgment: the text cites "Fig. 3(b)" for the 150 um SMSR (8.78 dB at 30 mA, 60.1 dB at 60 mA) while the caption
  assigns (b) to 50 C; the Fig. 3(a) SMSR panel (20 C) matches the printed values, so the rows carry 20 C and Fig.
  3(a) with the conflict in notes.
- Not entered: current-induced red shift 0.07 / 0.04 nm/mA (no parameter; D83g), transmission experiments (system),
  DBR section 130 um (in notes; `length_um` holds the DFB section).
- Fab empty (passive, all authors at one institute, D80b).

### zhang2023b (UC Davis wafer-scale Si3N4 interposer)

- Rows: flip-chip inverse-taper pair inter-chip coupler (`chip_chip_coupler.evanescent`; 0.54 dB coupling, 0.77 dB
  scattering, 1.31 dB total derived, < 1.75 dB 1200-1600 nm, Fig. 8 ranges, full geometry), 1x10 EPS
  (`splitter.other`; 1.56 dB excess, 0.46 dB port variation), wafer-scale 1x100 distribution (`splitter.other`;
  0.85 dB terminal variation with qualifier ge because the authors state the true spread is higher), grating emitter
  (`free_space_emitter.grating_emitter`; about 9 deg and almost 50 % up, author_estimate).
- Fab `org_university_of_california_davis` (first-person fabrication flow, both authors at UC Davis, D72). Facility
  empty: the acknowledgment thanks staff of UC Davis CNM2 and UC Berkeley Marvell Nanofab (D84b), unlike fu2023 which
  states the devices were fabricated there.
- Not entered: +/-3.53 um 3-dB lateral tolerance (no 3-dB tolerance parameter, D81), > 50 um longitudinal tolerance
  (criterion not stated), 0.075 dB stitching loss (per connection vs total unclear; Fig. 11(c) gives about 0.015 dB
  at 100 nm), simulated EPS port losses.

### deng2020 (concave micromirror in polymer ROW)

- Rows: Au-coated R 300 um concave mirror (`micro_optics.vertical_taper`, `polymer`; 1.83 dB / 65.61 % best,
  channel ranges read off Fig. 11 for 62.5 and 50 um MMF receivers, 1.53 dB simulated), 45 deg plane mirror (3.4 dB
  measured, 2.73 / 4.56 dB simulated), 20 mm ROW (0.14 dB, launch included).
- Basis: Lc subtracts calculated Fresnel terms (0.16 / 0.18 dB), so measured-chain values are author_estimate
  (D516 jung2025 precedent); figure ranges extracted_from_figure.
- Not entered: roughness 54.78 / 39.56 nm (no parameter; surface_error_rms_nm candidate, D432), mirror width / depth
  127.65 / 127.72 um, 3.36 dB simulated minimum (R 350 um, other design), excimer process parameters.
- Fab empty (passive, single university; zhang2024a precedent).

### vocht2024 (Si3N4 DFWT metalens, DUV scanner)

- Rows: fabricated metalens (`micro_optics.metalens`, `sin`; 9.4 % focusing efficiency, 13.7 % simulated for the
  realized geometry, 30.3 dB and 33.9 +/- 2.2 dB (n 8) fiber-mirror-fiber link loss, 53 nm 3-dB link bandwidth,
  geometry), original 800 nm design row (`row_kind design`, 63.6 % simulated).
- Not entered (no parameter): focal-plane beam widths 91.8 / 68.5 um, focus 9.28 mm, output angle 0.78 deg, SLSR 3 %,
  mirror angular tolerances 0.7 / 1.2 deg, transmission 26 % / reflection 31 %.
- Fab empty: first-person process with authors at TU/e and SMART Photonics; the running org is not stated (D80b).

### arsanjani2024 (1x32 SiN OPA, LIGENTEC MPW)

- Rows: OPA (`free_space_emitter.other`; FOV 24.28 x 9.46 deg measured, 24.2 / 9.57 deg calculated, FWHM 0.66 /
  0.082 deg, SLSR 8.62 dB, pitch 3.7 um derived), double-folded and single-pass recessed thermo-optic phase shifters
  (65 mW/pi measured; 245 mW/2pi -> 122.5 mW/pi derived), 1 mm antenna (95 % design emission, author_estimate).
- Fab `org_ligentec` with `process_name` "LIGENTEC MPW, 800 nm SiN" on all rows ("fabricated by LIGENTEC in a
  multi-project wafer run"). CamGraPhIC (`org_camgraphic`) bonded the chip and attached the fiber array: assembly
  only, no assembled row with metrics, so not entered as fab (D399); in notes.
- Not entered: antenna crosstalk < -26 dB and gap 2.5 um (parameters not allowed for free_space_emitter, see gaps),
  measured emission 0.6 uW/um (not converted to a percentage: would assume uniform emission), simulated 320 mW/2pi
  unrecessed heater, PDK component performance (proprietary, none printed).

### osorniomartinez2025 (packaged Al2O3:Er3+ EDWA)

- Rows: 50 cm EDWA (`amplifier.rare_earth`, `al2o3`; external net gain 24.3 dB peak / 23.7 dB at 1550 nm / 17 dB at
  95 C, 90 nm gain span, Psat,in about -13 dBm, 17.4 dBm fiber output and 19.44 dBm on-chip derived, PCE 16.3 %
  derived, NF 4.6 dB and 5.4 -> 8.5 dB over 30-95 C, > 13.98 dBm at 95 C derived, geometry); packaged edge coupler with
  fiber array (`fiber_chip_coupler.edge`; 2.8 dB at 1480 nm, 1.74-2.5 dB over 1520-1640 nm, 2.04 dB at 1550 nm,
  loopback_half; tip / taper / fiber MFD).
- Not entered: background loss < 0.1 dB/cm (from the authors' ref. [13], D259); gain-drop decomposition (in notes).
- Fab: EDWA empty (passive; wafer batch of ref. [13]). Coupler row `org_phix_photonics_assembly` (packaging in the
  PHIX B.V. characterization package: facet polish and fiber-array attach); see question 2.

## Missing organizations

None needed for fab / facility roles. Orgs named only as suppliers or co-author affiliations (Intelligent Epitaxy
Technology Inc., Corning, SMART Photonics, Silicon Austria Labs) are not distiller output.

## Registry gaps (with skipped values)

1. `crosstalk_db` for `free_space_emitter`: arsanjani2024 adjacent-antenna power crosstalk < -26 dB (p.6, Fig. 4(f)).
   Proposed: allow crosstalk_db on free_space_emitter (adjacent-emitter coupling, type in condition).
2. `gap_nm` for `free_space_emitter`: arsanjani2024 antenna gap 2.5 um (p.6). Proposed: edge-to-edge gap between array
   emitters.
3. Focal length / focal-spot width for `micro_optics`: vocht2024 focus 9.28 mm and focal-plane widths 91.8 / 68.5 um
   (p.6 Table 1); also wang2023c precedent. Proposed `focal_length_um` (geometry or performance as printed) and
   `focal_spot_width_um` (criterion in condition).
4. Laser static current tuning: li2025c 0.07 / 0.04 nm/mA (p.5). Proposed `current_tuning_pm_per_ma` (static
   wavelength shift per mA of injection current; D83g keeps it out of fm_efficiency).
5. Surface roughness: deng2020 39.56 nm after reflow (p.8); candidate `surface_error_rms_nm` already listed (D432).
6. Aperture / mesa diameter for surface emitters: hsu2025 oxide aperture 5 um (p.2), itoh2024a mesa 200 um (p.4).
   Proposed `aperture_diameter_um` (laser).

## Questions for the coordinator / audit

1. hsu2025: the 39 GHz headline is a VCSEL-plus-1 km-fiber channel bandwidth; kept in notes only. Enter it on the
   VCSEL row with the fiber in condition instead?
2. osorniomartinez2025: PHIX entered as fab on the packaged edge-coupler row (named packaging step, D399 / D450
   reading); the EDWA row left empty. Alternative: PHIX on both packaged rows, or on neither.
3. hsu2025: the VCSEL-to-lens-fiber coupling is a separate `fiber_chip_coupler.other` row with platform `gaas`
   (D82f facet layer); `micro_optics.facet_lens` would also fit if the setup lens fiber is treated as the optic.
4. zhao2016: values were checked on page renders of the cached PDF (scratchpad) because no page renders exist in
   `figures/`; the decoded text layer agreed with the renders everywhere.
