# lit_169 batch report

Distilled 2026-11-16 under the pic-component-distill skill (Contracts v4-v7, DevLog-007 D150-D615). Papers: lit:zhang2025g,
lit:zhou2022c, lit:zhang2023f, lit:liu2021b. Page-1 titles match the source rows (all four). Totals: 12 components, 39 metric
rows. Dry-run `merge_component_staging.py data/_staging/components/lit_169 --dry-run`: +12 / +39, 0 errors, no warning on
this batch.

D411 scope: all four papers are chip-scale. zhang2025g is an EBL-patterned 1 x 1 mm metasurface in a liquid-crystal cell
(LCoS-like, D424 analogue); zhou2022c and liu2021b are simulated metasurface lenses of tens of um over integrated antennas;
zhang2023f is a heterogeneous GaAs-on-SiN PIC platform. No bulk part.

## lit:zhang2025g (LC-tuned metasurface, Optics Express 2025)

- 1 component / 9 metrics: `cmp_lit_zhang2025g_lc_metasurface_phase_modulator`, `phase_shifter.other`, platform `other`
  (a-Si nanodisks on SiO2 spacer over an Al mirror, LC cell). Measured peak phase depth 7.23 rad = 2.30 pi at 1545.65 nm
  (derived, rad -> pi), simulated 7.08 rad = 2.25 pi at 1544 nm, rise 0.7 ms / fall 3.5 ms (derived ms -> us, 22 C),
  simulated reflectance above 60 % as insertion_loss_db < 2.22 dB (device_total, simulated), geometry (disk height 280 nm,
  220 nm spacer, 2.5 um LC, 1 mm2 area).
- Not entered (no parameter): measured > 2 pi bandwidth 6 nm (p.11 Fig. 9(c)); 2 pi kept up to +/-2.5 deg incidence and
  resonance shift 1545.65 -> 1553.75 nm (p.11); threshold about 1.2 V and about 4.10 rad at 4.5 V (p.9); phase uniformity
  0.018 pi rad (p.8, scaled from a 543 nm measurement); disk radius 265 nm and lattice 900 nm (no phase_shifter geometry
  parameter; in core_material). Measured reflectance is only qualitative (p.9 Fig. 8(c)).
- Judgment calls: class by function (non-EO phase shifter, iseghem2022 LC precedent) rather than micro_optics.metalens;
  rise / fall definitions not printed (condition says so); response-time wavelength C band inferred; the abstract
  "reflectance exceeding 60%" is entered as simulated because the only body statement is in the simulation section (p.5).
  Printed conflict: 7.23 rad at 1545.65 nm (p.9) vs 1546.5 nm (conclusion p.11), kept as p.9 with a note (D417).
- Fab: empty (passive fabrication sentences, p.7; all authors University of Cambridge CPDS; D80b).
- Missing org (facility, borderline D80c): "Henry Royce Institute for advanced materials ... Equipment Access Scheme enabling
  access to the RAITH - EBPG 5200 Electron-beam Lithography System at Cambridge" (p.12 Acknowledgment). Not in the registry.

## lit:zhou2022c (metasurface Fourier lens + plasmonic antennas, Optics Express 2022)

- 2 components / 12 metrics, both `row_kind: design` (simulation only, p.2 "designed and numerically demonstrated"):
  - `cmp_lit_zhou2022c_metasurface_fourier_lens_steerer`, `free_space_emitter.metasurface`, platform `other`: steering
    +/-50 deg (11 feeds, 10 deg steps), first sidelobe below -15 dB (slsr_db 15 gt), 11 feeds, 600 nm period, 1100 nm
    pillar height, 41 x 41 cells, 24.6 x 24.6 um2 aperture (derived area).
  - `cmp_lit_zhou2022c_plasmonic_slot_antenna`, `free_space_emitter.other`, platform `plasmonic_mim` (Ag slot waveguide,
    merged plasmonic-slot precedents): radiation efficiency > 80 % at 1550 nm (coupling_efficiency_pct, abediasl2015
    precedent), footprint 0.77 x 1.4 lambda = 2.59 um2 (derived), Ag 100 nm, stripe 200 nm, modulation period 900 nm.
- Not entered (no parameter): directivity 21.5 dB (device), 18.8 dB with the Yagi-Uda feed, 27.8 dB at F/D = 1, antenna
  directivity 9.6 dB / 8.36-10.2 dB, gain variation < 2.83 dB, cross-polarization < -20 dB, S11 < -13.8 dB (back_reflection_db
  not allowed on free_space_emitter), realized gain 6.88 dB / +1.69 dB, slot width 340 nm and reflector gap 200 nm (gap_nm not
  allowed on free_space_emitter), focal length 10 um, F/D 0.41. Unit-cell transmission > 90 % / > 85 % at 40 deg not entered
  (periodic-array element value, D460). Yagi-Uda feed: no row (design of ref. [26], only a directivity value).
- Judgment calls: steering stored as the printed one-sided 50 deg with "+/-" and full span in the condition (abediasl2015
  style); nanopillar height in core_thickness_nm (he2026 precedent); the 11 elliptic-pillar a / b dimensions kept in
  core_material (x / y roles per element, no single width).
- Fab / facility: none (design). No missing org.

## lit:zhang2023f (Nexus Photonics GaAs-on-SiN 780 nm platform, Optica Memorandum 2023)

- 8 components / 13 metrics:
  - `fp_laser` (laser.heterogeneous): > 12 mW on-chip at 90 mA, WPE 6 % (20 C per the Fig. 1(b) axis, text "room
    temperature"), threshold 29.5-34.5 mA over 140 devices (Fig. 1(c) read, n 140, D165).
  - `vernier_tunable_laser` (laser.tunable): tuning about 18 nm per epitaxial stack (Fig. 1(f) labels), intrinsic
    linewidth about 4.35 kHz (text, derived kHz -> Hz).
  - `mopa` (laser.tunable, laser + SOA + monitor PD): intrinsic linewidth 4.15 kHz (Fig. 1(i) legend, derived).
  - `sil_highq_ring` (laser.sil): 92.4 Hz fundamental linewidth self-injection locked (measured).
  - `highq_sin_ring` (resonator.ring, sin): intrinsic Q about 1e7, author_estimate (D403: no regime data).
  - `soa` (amplifier.soa): > 15 dB on-chip gain at 774 nm (Fig. 1(d) seed label, input -13.44 dBm).
  - `sld` (laser.other): about 10.7 mW at about 180 mA, peak about 787 nm, 3-dB width about 7 nm (all Fig. 1(e) reads).
  - `sin_waveguide` (waveguide_platform.straight, sin): about 5 dB/cm, author_estimate (origin not stated).
- Not entered: PD dark current "100 pA range" (text) and about 0.25-0.29 nA over 140 PDs (Fig. 1(c) right axis): no bias
  printed, and `dark_current_na` requires bias_v; the PD therefore has no row. SMSR in Fig. 1(f): only one labelled tick
  (40), scale unreadable (D156). Lasing up to 110 C (no maximum-temperature parameter). "< 1 dB/cm demonstrated previously"
  cites ref. [3] (rule 3). SOA figure peak about 16 dB near 51 mA kept in notes (text bound entered).
- Judgment calls: (1) fab empty on all rows: "our platform" and first-person "We bond ..." (p.1), but authors at Nexus
  Photonics and UCSB and no contribution statement (D154, D80b, D84a; itoh2024 / D468 precedent); `org_nexus_photonics`
  exists if the coordinator reads "We bond" plus 10 / 12 Nexus authors as sufficient. (2) The text 4.35 kHz ("such lasers")
  and the legend 4.15 kHz (MOPA) may be the same measurement; kept on two rows (tunable laser design vs MOPA) with
  cross-notes (D417); alternative is to drop the text value (D159). (3) Platform `other` with the stack in core_material
  (tran2022 / thiel2026 precedent). (4) Wavelength: band `nir_below_o` inferred on rows without a printed wavelength
  (components optimized around 780 / 795 nm, p.1); 774 nm (SOA) is in the `visible` band by the validator's edges, so that row
  carries only wavelength_nm. (5) FP threshold population read at +/-0.5 mA; temperature of Fig. 1(c) not stated.
- Missing orgs: none needed (no fab statement).

## lit:liu2021b (Si metalens for beam steering, IEEE GFP 2021)

- 1 component / 5 metrics: `cmp_lit_liu2021b_metalens_square_pillars`, `free_space_emitter.metasurface`, `row_kind:
  design`, platform `soi` (as printed, "700-nm silicon-on-insulator platform"): steering +/-40 deg (simulated), steered-beam
  divergence about 10 deg FWHM, pillar height 700 nm, period 600 nm, widths 100-450 nm.
- Not entered: focal distance 11.0 -> 9.8 um over 1500-1600 nm (square pillars) and constant 10 um (achromatic design); lens
  diameter 30 um. The achromatic rectangular-pillar design has no row (its only result is the focal distance, no
  parameter).
- Judgment calls: steering and divergence tied to the square-pillar design by the Fig. 1(c)-(e) caption; class
  `free_space_emitter.metasurface` (he2026 precedent; `micro_optics.metalens` does not allow steering_range_deg).
- Fab / facility: none (design). No missing org.

## Registry gaps (skipped value + locator, proposed definition)

- `directivity_db` (free_space_emitter): zhou2022c 21.5 dB device / 9.6 dB antenna (p.8, p.1); "peak antenna directivity
  in dBi as stated".
- `back_reflection_db` on free_space_emitter: zhou2022c S11 < -13.8 dB over 1500-1613 nm (p.7 Fig. 4(a)).
- `gap_nm` on free_space_emitter (also D554): zhou2022c slot 340 nm, reflector gap 200 nm (p.6).
- `focal_length_um` (micro_optics / free_space_emitter, D432 / D554 candidates): zhou2022c 10 um (p.4); liu2021b 10 um and
  11.0-9.8 um over 1500-1600 nm (p.1-2 Fig. 1(h)).
- `aperture_diameter_um` / lens radius on free_space_emitter (D433 candidate): liu2021b 30 um (p.1).
- Phase-modulation bandwidth above 2 pi (`phase_bw_2pi_nm`, phase_shifter): zhang2025g 6 nm measured (p.11 Fig. 9(c)).
- Phase_shifter metasurface geometry (`radius_um`, `pitch_um` on phase_shifter): zhang2025g radius 265 nm, lattice 900 nm (p.3).
- Maximum operating temperature (laser, D431 candidate): zhang2023f 110 C (p.1).
- Photodetector dark current with unstated bias: zhang2023f "100 pA range" (p.2); needs either a bias or a ruling to allow
  `bias_v` empty with a note.
