# lit_272 batch report

Papers: lit:riemensberger2012, lit:pan2020, lit:yang2025a, lit:spencer2012. Page-1 titles match the source rows; no
garbled text layer. Total 18 components / 98 metric rows. `merge_component_staging.py --dry-run`: +18 components,
+98 metrics, 0 errors (two pre-existing duplicate-value warnings on other batches: guo2024a, ni2025b).
verified_on 2026-11-24. Figures checked on the page renders (spencer2012 p.1-2, pan2020 p.6, yang2025a p.3-5).

## lit:spencer2012 (11 components / 42 metrics)

- `cmp_lit_spencer2012_ring_r9p8mm` (resonator.ring, sin, 45 nm x 7 um, R 9.8 mm, 8 metrics): Q_L 35 M at 1550 nm
  (measured), Q_i 55 M at 1620 nm (author_estimate, D403: extraction model cited to ref. [8], regime determination
  not stated), ring loss 0.5 dB/m -> 0.005 dB/cm at 1620 nm inferred (author_estimate, rests on Q_i), coupling < 1 %,
  radius / width (derived from mm / um), 45 nm core, 15 um BOX.
- `cmp_lit_spencer2012_dc_r9p8mm` (splitter.directional_coupler, 1 metric): excess loss 0.007 dB per coupler
  (author_estimate, reference_structure).
- `cmp_lit_spencer2012_ring_r1p59mm_g{2p6,2p4,1p8,1p6}` (resonator.ring, 6 metrics each): Table 1 coupling
  0.9 / 1.4 / 5.3 / 8.4 % at 1580 nm, gap, radius, width, 100 nm core, BOX.
- `cmp_lit_spencer2012_dc_r1p59mm_g{...}` (splitter.directional_coupler, 2 metrics each): Table 1 excess loss
  0.07 / 0.09 / 0.22 / 0.31 dB per coupler at 1580 nm, gap.
- `cmp_lit_spencer2012_spiral_100nm` (waveguide_platform.straight, 1 metric): OBR spiral loss 2.5 dB/m -> 0.025 dB/cm
  (derived), 1580 nm inferred, method ofdr.

Not entered: Table 1 round-trip losses 0.30 / 0.33 / 0.60 / 0.78 dB (no parameter; registry gap below); Fig. 3 ring
loss curves (the round-trip losses over the 1 cm circumference imply about 30-78 dB/m while the panels read about
5-12 dB/m at 1580 nm: conflict, not resolved by the text); Fig. 2 per-wavelength curves beyond the printed values;
the 45 nm spiral OBR loss and its 1.1 cm bend-radius fit (attributed to ref. [7], rule 3); the 7 M earlier result
(ref. [9]); Q of the 1.59 mm rings (not printed).

Fab: 45 nm devices "fabricated at LioniX BV, the Netherlands" (p.2 acknowledgment) -> fab left empty (LioniX BV not in
the registry; kept apart from LioniX International BV per D278 / D545). 100 nm devices "by Aurrion, Inc." ->
`org_aurrion` (rings, couplers and the 100 nm spiral; the spiral is assigned to the 100 nm devices by its shared
cross-section). No facility.

## lit:riemensberger2012 (3 components / 19 metrics)

- `cmp_lit_riemensberger2012_ring_r301_hfo2` (resonator.ring, sin, 7 metrics): FSR D1/2pi 75.04 GHz, TM11 (linear
  fit over 120 FSRs, measured), R 301 um, 1700 x 750 nm, 4 um BOX, 3 um SiO2 top cladding, sidewall ~78 deg.
- `cmp_lit_riemensberger2012_rings_uncoated` / `_rings_hfo2` (resonator.ring, population rows, 6 metrics each):
  "critically coupled" Q up to 1e6 (uncoated) and up to ~6e5 (HfO2-coated) as q_loaded with qualifier le, wavelength
  1545-1615 nm inferred; shared geometry.

Not entered: all dispersion results (D2/2pi 350 kHz TM11 coated; TE11 340 -> 490 kHz at 1.58 um with 55 nm HfO2;
TM11 -180 kHz uncoated; Fig. 3 / Fig. 4 measured and simulated D1, D2; ZDP shift rates), since the registry has no
dispersion parameter (D81 rejected dispersion; registry gap below); the bus inverse taper (150 nm tip, 6 um from the
facet; geometry only, no performance); Fig. 3(a)-(d) measured D1 symbols.

Fab `org_epfl`, facility `org_center_of_micronanotechnology`: "samples ... fabricated at the Center for
Microfabrication (CMi) at EPFL" (p.9 Acknowledgments; D448 stated place, cai2025 precedent). The printed expansion
"Center for Microfabrication (CMi)" differs from the registry name "Center of MicroNanoTechnology": alias proposed.

## lit:pan2020 (3 components / 18 metrics; all `row_kind: design`)

Theory / simulation paper; no fabricated device.

- `cmp_lit_pan2020_racetrack_reff18` (resonator.ring, lnoi_strip, 10 metrics): FSR ~5.8 nm and loaded Q ~6.5e5 at
  ~1550 nm (TE0, simulated; Q assumes 1 dB/cm loss cited from ref. [5]), footprint < 2000 um2, Reff 18 um, Rmin
  10 um, top gap 720 nm, coupling-region length ~36 um, top width 1.4 um (derived), 600 nm core, 2 um BOX.
- `cmp_lit_pan2020_euler_bend_180` (waveguide_platform.bend, 4 metrics): excess loss < 0.01 dB per 180 deg bend at
  1550 nm (3D-FDTD), Rmin 10 um, width, core.
- `cmp_lit_pan2020_arc_bend_r9p7` (waveguide_platform.bend, 4 metrics): straight-to-bend mode-mismatch loss up to
  1.3 dB (overlap 74 %) at R 9.7 um, radius, width, core.

Not entered: inter-mode crosstalk values (-50 dB loop, -53 dB Euler bend, -60 dB arc at R0 9.7 um, < -20 dB over
60 nm for |dtheta| <= 3 deg, < -25 dB for R > 45 um, < -20 dB over 100 nm for the 300/300 nm rib at R0 ~26 um), since
crosstalk_db is not allowed for waveguide_platform / resonator (registry gap below); taper excess loss < 0.001 dB
(a design criterion for the taper lengths 24.5 / 17.5 / 9.5 / 10 um); 0.004 dB Euler-junction mismatch (part of the
bend value); 30 deg sidewall angle (cited from ref. [5], and measured from vertical in Fig. 1(a), opposite to the
registry convention); LN indices; Table I rows of other works (rule 3). Fab: none (design).

## lit:yang2025a (1 component / 19 metrics)

- `cmp_lit_yang2025a_ring_r150` (resonator.ring, platform other: Ta2O5 on SiO2, 19 metrics; one device measured
  before and after a 600 C / 10 h anneal, the state in `condition`): before: Q_L ~3.1e5, FWHM 5 pm, ER ~6 dB at
  1550.655 nm (measured), Q_i 4.3e5 and 1.33 dB/cm (author_estimate), FSR ~0.805 nm; after: Q_L 5.2e5, ER 12 dB at
  1549.725 nm (measured), Q_i 8.5e5 and 0.6 dB/cm (author_estimate); band values over 1520-1580 nm: Q_i ~4e5 / ~8e5
  and ~1.3 / ~0.6 dB/cm (typical, author_estimate); R 150 um, ring width 2000 nm, gap 600 nm, 400 nm core, 2 um BOX.

Not entered: NaCl bulk sensitivity ~279 nm/RIU and intrinsic LOD 1.78e-5 RIU (p.4; registry gap below); Fig. 1(a)
1000 x 400 nm SEM cross-section (role not stated); Ta2O5 film index / roughness (material data); Tables II / III rows
of other works (rule 3).

Fab empty: "We fabricated the Ta2O5 photonic device" (p.2) with authors spread over the SINANO Nanofabrication
Facility, Ningbo University, ShanghaiTech University and Peking University (D154 / D80b: no single unambiguous org);
no acknowledgment names a facility (the SINANO Nanofabrication Facility appears only as an affiliation).

## Judgment calls for the auditor

1. spencer2012 coupler excess losses (0.007 dB and Table 1) as `splitter.directional_coupler` rows next to the ring
   rows (D396 cross-notes), basis author_estimate: the paper calls the attribution to the couplers a hypothesis, the
   arithmetic is not shown, and the 0.007 dB rests on the OBR spiral fit attributed to ref. [7] (D80i borderline;
   the alternative is dropping it under rule 3).
2. spencer2012 coupling % and Q_i as author_estimate (D403: extraction model cited, regime determination not stated),
   although the add-drop through and drop spectra were both recorded.
3. spencer2012 1620 nm on the 0.5 dB/m and 0.007 dB rows and 1580 nm on the 2.5 dB/m spiral row are inferred from
   the surrounding sentences (`wavelength_inferred: true`).
4. riemensberger2012 population rows for the Q bounds (D165 array-level form) instead of D159 / D254 notes: the
   bounds are stated for all uncoated / all coated resonators, not for one device. If D254 is preferred, the two
   population rows lose their only performance metric and should be deleted with the bounds moved to the 301 um
   ring notes.
5. riemensberger2012 "critically coupled optical quality factors" entered as q_loaded (unqualified Q rule); sidewall
   ~78 deg basis measured (method not stated).
6. yang2025a Q_i / loss author_estimate under D403: the under-coupled regime is stated from a gap sweep whose data are
   not shown. Printed T0 = 0.065 does not reproduce the pre-anneal Q_i 4.3e5 (it gives about 4.9e5; it matches the
   annealed 12 dB resonance): kept as printed with a conflict note.
7. yang2025a one row for both anneal states (same physical device; atsumi2018 precedent) rather than two rows
   (huang2026 used two rows for two different samples).
8. pan2020 Q 6.5e5 basis simulated although it rests on the assumed 1 dB/cm loss (design-row precedent: all merged
   design-row Q values are simulated); coupling_length_um 36 is the total coupling region including two tapers.

## Missing fab / facility orgs

- LioniX BV (2012 entity), fab of the spencer2012 45 nm devices: "The 45nm devices were fabricated at LioniX BV, the
  Netherlands" (lit:spencer2012 p.2 acknowledgment). Same pending org as a2011, bauters2013, mu2016, zhuang2016
  (D545); re-point `cmp_lit_spencer2012_ring_r9p8mm` and `cmp_lit_spencer2012_dc_r9p8mm` once it exists.
- Alias: "Center for Microfabrication (CMi)" at EPFL -> `org_center_of_micronanotechnology` (lit:riemensberger2012
  p.9 Acknowledgments; facility role, used on 3 rows).

## Registry gaps

- `roundtrip_loss_db` (resonator): ring round-trip loss in dB as printed (spencer2012 Table 1, 0.30 / 0.33 / 0.60 /
  0.78 dB at 1580 nm, p.2); already listed under D420 / D540.
- `dispersion_d2_khz` (resonator): resonator dispersion D2/2pi = omega(l-1) - 2 omega(l) + omega(l+1) over 2 pi, sign
  as printed (riemensberger2012 p.5 Fig. 2(c) 350 kHz TM11; p.6 340 / 490 kHz TE11, -180 kHz TM11).
- `crosstalk_db` for waveguide_platform (bend inter-mode crosstalk, TE0 -> TM0, positive dB): pan2020 p.4-5 Fig. 8
  about 53 dB, p.3 Fig. 5 60 dB at R 9.7 um.
- `bulk_sensitivity_nm_per_riu` and `ilod_riu` (resonator sensing): yang2025a p.4 ~279 nm/RIU, 1.78e-5 RIU (NaCl).
