# Batch lit_48 report (distill subagent, 2026-10-29)

Dry-run `batch lit_48: +14 components, +69 metrics; errors 0` (the only warning is pre-existing, ni2025b, another batch).
ASCII only, no e-mail / street / postal text, no quotes beyond a few words (all four sources `restricted_local_only`).
Page-1 title / authors of all four cached texts match their source rows (no D397 / D409 case); no garbled text layers.
Values in figures read from page renders (muthuganesan2023 Table 1 / Fig. 3, bauters2011 Fig. 4 / 6 / 8 / 9,
xiao2022 Fig. 1 / 3 / 4, pospischil2013 Fig. 3).

## Per paper (components / metrics)

- muthuganesan2023 (4 / 26): micro-transfer-printed InGaAs PD coupons on 500 nm SOI in three coupling schemes as
  `photodetector.iii_v_on_platform` (platform `other`, arafat2024 precedent): butt (19 x 9 um2 mesa; 0.13 A/W, 400 nA,
  100 fF at 2 MHz), grating (0.3 A/W, 47 nA, 17.5 GHz at -0.6 V / 1547 nm), evanescent (0.54 A/W, 48 nA, 7.5 GHz);
  Table 1 simulated responsivities (0.3 / 0.45 / 0.61 A/W) as `simulated`; absorber 400 nm, Si 500 nm, BOX 3 um.
  CORNERSTONE MPW TE GC (5 dB loopback_half derived, 30 um grating, 14 deg). Responsivities `derived` (on-chip power
  calculated from fiber power and the own GC loss; liao2011 precedent), ref_plane on_chip.
  Not entered: the 1.3 mW operating point (0.2 / 0.4 / 0.8 mA, 0.13 / 0.3 / 0.6 A/W) and Fig. 4 (I-V, responsivity, QE)
  because the sentence cites and the figure is reprinted from the authors' own ref. [17] (D259 / D259a / D408); this
  removes the abstract headline 0.6 A/W. Simulated power fractions coupled to the PD (40 / 62 / 94 %; no photodetector
  parameter), 250 ohm n-layer lateral resistance (origin not stated, not a device series resistance), mesa length /
  width (17 x 7 vs "19 um long" on p.4 inconsistent, orientation not stated), calculated transit time 1.7 ps, MTP
  placement tolerance +/- 1.5 um, eye diagrams / data rates, Supplement 1 (not cached).
- pospischil2013 (3 / 9): bilayer-graphene Si-waveguide PD L = 24 um, W = 180 nm (`photodetector.graphene`, soi):
  ~0.03 A/W at 1550 nm, zero bias, Pin "estimated" from reference waveguides (measured, reference_structure); 18 GHz
  (derived, 0.441 / 25 ps, setup-limited); L, waveguide 600 nm x 270 nm, BOX 3 um. Tri-layer best device: ~0.05 A/W
  (best; wavelength inferred 1550 nm) and internal QE ~10 % (author_estimate, rests on simulated absorption). Cleaved
  facet + lensed fiber reference: 15 dB (printed 15 +/- 1 dB), scope unspecified. The "18 pages incl. supplementary" are
  the arXiv preprint with figure pages 12-15 and references 16-18: no supplement in the cached text.
  Not entered: Fig. 3(b) wavelength dependence 1310-1650 nm (photocurrent only, input power not stated), absorbed
  fraction ~44 % (simulation, no parameter), signal-electrode width W (no parameter), simulated design points, footprint
  "down to 50 um2" (not tied to a device).
- bauters2011 (4 / 22): UCSB / LioniX ultra-low-loss Si3N4-core silica waveguides (`waveguide_platform.straight`,
  `sin`): 40 nm x 13 um bonded-thermal-oxide cladding 0.045 dB/m near 1580 nm (best, stored 0.00045 dB/cm derived) and
  0.33 dB/m near 1.3 um; 40 nm x 6.0 um bonded 1.032 m spiral group index 1.4815 at 1600 nm; 50 nm x 6.5 um PECVD
  cladding 0.45 dB/m near 1.29 um and 0.05 dB/m at the longest wavelengths of 1530-1605 nm (L band inferred); facet
  of a 50 nm x 10 um PECVD waveguide to cleaved SMF-28 with gel 0.91 dB per facet (derived from Eq. 5, OFDR). Geometry:
  widths (um -> nm derived), core thickness, 15 um BOX, 9.8 mm s-bend radius of the spiral, 1.032232 m spiral length.
  Not entered: critical bend radius per width (Fig. 6(b), plot only, no parameter), coupling loss vs width (Fig. 4(b)),
  group index vs width (Fig. 3(b)), ellipsometry 39.4 nm / SEM ~35 nm core thickness (sample cladding not stated,
  D159), upper-cladding thickness above the core (TEOS height after CMP not stated), 0.01 dB s-bend propagation term.
- xiao2022 (3 / 12): AIM Photonics MPW W1 photonic-crystal waveguides suspended by BOE undercut
  (`waveguide_platform.slow_light`, soi): r = 135 nm (2.5 dB) and r = 140 nm (2 dB) chiplet-I devices, 0.2 mm,
  GC-normalized (scope de_embedded, includes both channel-PhC couplers; Fig. 3 labels), > 10 dB before undercut; the
  channel-WG -> supported PhC -> suspended PhC coupler as `waveguide_platform.transition` (< 1 dB, scope unspecified;
  channel width 500 nm design / 455 nm SEM). Fab AIM Photonics + University of Delaware (authors performed the
  post-processing).
  Not entered: extinction ratios 42 / 40 dB and the family statements "2 (+/- 1) dB" / "40 (+/- 4) dB across dies"
  (extinction_db not allowed for waveguide_platform; D254 for the family values), lattice constant 440 nm / hole radii
  (no parameter), SEM a = 430 / r = 122 nm (text repeats the same pair for r = 140 nm), chiplet II r = 150 / 155 nm
  (fiber-to-fiber spectra without labels), undercut depth ~1 um (estimate), Fig. 4(c) literature comparison.

## Missing orgs (name as printed + locator)

- "Tyndall fabrication facility" (muthuganesan2023 p.8 Acknowledgments): facility of Tyndall National Institute;
  `org_tyndall_national_institute` exists as the institute only (owner of a facility is not a facility, D80b).
- Vienna University of Technology, Institute of Photonics (pospischil2013 p.1 affiliation; p.10 author contributions:
  A.P. fabricated the samples) -> fab org for the graphene PD rows.
- Johannes Kepler University Linz, Institut fuer Halbleiter- und Festkoerperphysik (pospischil2013 p.1; p.10: M.H.
  fabricated, R.G. and T.F. contributed) -> fab org for the graphene PD rows.
- University of Delaware Nanofabrication Facility (xiao2022 p.8 Acknowledgments: post-processing) -> facility for all
  three xiao2022 rows.

## Judgment calls for the auditor

1. muthuganesan2023: D259 / D408 applied to the 1.3 mW values (sentence cites own ref. [17], Fig. 4 reprinted from it)
   while Table 1 (no attribution) is entered; the alternative reading keeps the 1.3 mW values as journal-extension data.
2. muthuganesan2023 responsivities `derived` (on-chip power calculated with the own 5 dB GC loss and an assumed
   negligible waveguide loss; author_estimate is the alternative). Butt row: Table 1 prints 0.13 A/W although
   0.077 mA / 0.65 mW = 0.118 A/W (kept as printed, noted).
3. muthuganesan2023 GC 5 dB as loopback_half `derived` (authors assume negligible waveguide / taper loss).
4. pospischil2013 fab: named fabricating authors at two orgs (TU Wien, JKU Linz) -> both would be fab orgs once in the
   registry (jiang2020 "named authors" precedent); left empty now.
5. pospischil2013 18 GHz as `derived` from the Gaussian time-bandwidth product (author_estimate if the pulse-shape
   assumption counts as an assumed input); trilayer row wavelength inferred (1550 nm characterization).
6. pospischil2013 facet row: "total losses 15 +/- 1 dB" of the reference waveguides, one vs two facets not stated ->
   scope unspecified.
7. bauters2011: the same Sec. 3.4 spiral layout (9.8 mm s-bend) assumed for the bonded 13 um and PECVD 6.5 um
   waveguides (Sec. 3.4 states the spiral is used for the OFDR loss measurement; the bonded Fig. 3(a) spiral has the
   same 1.032 m length). Values are minima of loss spectra (`statistic best`).
8. xiao2022: W1 PhC waveguide as `waveguide_platform.slow_light` (alternatives: straight); channel-PhC coupler as
   `waveguide_platform.transition` (inter-material: oxide-clad strip to suspended membrane; alternative
   mode_converter.converter). Per-radius rows from Fig. 3 labels (`measured`, printed labels) with the pass-band span
   read off the figure (wavelength inferred); org_university_of_delaware as fab org from the author-contribution
   post-processing statement (all authors at Delaware).
9. xiao2022 coupler < 1 dB: the Fig. 1(b) micrograph is of an EBL device made in the university cleanroom, but p.3 ties
   the < 1 dB to the MPW devices with the designed undercut; entered on the MPW-fabricated transition row.

## Registry gaps (proposed definitions)

- `extinction_db` for `waveguide_platform` (or a new `passband_stopband_contrast_db`): transmission contrast between the
  pass band and the stop band of a band-edge waveguide (xiao2022 42 / 40 dB, p.13 Fig. 3).
- `critical_bend_radius_um` (waveguide_platform, performance): bend radius at which bend loss equals the stated
  criterion (criterion in condition, e.g. 0.1 dB/m; bauters2011 Fig. 6(b), plot only).
- `lattice_constant_nm` and `hole_radius_nm` (waveguide_platform, resonator, reflector; geometry): photonic-crystal
  lattice constant and air-hole radius (xiao2022 440 nm, 135-170 nm; SEM 430 / 122 nm).
- `absorption_fraction_pct` (photodetector, performance): fraction of the guided power absorbed in the active layer
  (simulated or estimated; muthuganesan2023 40 / 62 / 94 %, pospischil2013 ~44 %).
