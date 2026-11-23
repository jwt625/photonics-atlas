# lit_266 batch report

Papers: lit:cheung2014, lit:yang2011, lit:zheng2013. Page-1 titles match the source rows. Total 9 components / 102
metric rows. `merge_component_staging.py --dry-run`: +9 components, +102 metrics, 0 errors (one pre-existing warning
on another batch, cmp_lit_ni2025b_pimmwc). verified_on 2026-11-23.

## lit:cheung2014 (3 components / 27 metrics)

- `cmp_lit_cheung2014_awgr_512x512` (wdm.awg, soi_rib, 21 metrics): crosstalk ~4 dB (type not stated, input #323),
  measured 25 GHz spacing; Table II design values (0.2 nm spacing, 1.55 um centre, 512 channels, 1200 arms, order 11,
  dL 6.011 um, slab radius f 2796.531 um, R_min 85 um, 950 nm arm width, 1.55 um input width at the slab, 3 um I/O
  width, 250 nm Si / 150 nm slab / 100 nm etch / 2 um BOX, 1 um LPCVD cladding), footprint 11 x 16 mm.
- `cmp_lit_cheung2014_si_rib_w750` (waveguide_platform.straight, 4 metrics): 2.78 dB/cm (Fabry-Perot method), width,
  thickness, BOX.
- `cmp_lit_cheung2014_polished_facet` (fiber_chip_coupler.edge, 2 metrics): 11.3 dB per facet (author_estimate),
  31 % FDTD facet reflection as back_reflection_db 5.09 dB (simulated).

Not entered: Table II arrayed WG pitch d = 450 nm and input WG pitch D = 450 nm (smaller than the printed 950 nm /
1.55 um widths, role unclear; p.3 Table II); AWGR insertion loss (Fig. 6 is raw transmission near -45 dB, no IL
printed); Fig. 7 phase-error simulation (contrast below 10 dB at rms dn 7.7e-5, a tolerance with no parameter);
simulated effective indices (Fig. 2(b), Fig. 3); 0.92 dB/cm HSQ loss (cited, ref. [48]); Table I rows of other works.

Fab: org_university_of_california_davis (borderline): first-person "we design, fabricate" (p.1) and "we employ
photoresist reflow" (p.4 Sec. III); three of four authors at UC Davis, the fourth printed at the Aidi Corporation.
Same group and sentence as merged cheung2015 (UC Davis fab by audit Q2). SOITEC is the wafer supplier (note only).
No facility named.

## lit:yang2011 (4 components / 55 metrics)

- `cmp_lit_yang2011_awg_100ghz_r100` (wdm.awg, polymer, 15 metrics): excess loss ~9 dB at 1543.5 nm (de_embedded,
  straight-waveguide normalization), fabricated core 2.05 x 1.5 um, R 100 um, footprint 0.22 x 0.47 cm2, shared
  100 GHz design values (48 x 48, 100 GHz / 0.8 nm, 120 arms, order 36, L_FPR 700 um, d_g 1.5 um, 6 um buffer).
- `cmp_lit_yang2011_awg_100ghz_r150` (wdm.awg, 18 metrics): excess loss ~5 dB (Fig. 4(b)) and best 3.7 dB at
  1551.1 nm TE (Fig. 5), FSR 38.9 nm, adjacent crosstalk > 15 dB, output non-uniformity 4.5 dB, core 2.2 x 1.57 um,
  R 150 um, shared design values.
- `cmp_lit_yang2011_awg_400ghz_r1000` (wdm.awg, 20 metrics): best excess loss 4.3 dB, non-uniformity 2.2 dB,
  crosstalk > 20 dB, PDL ~1 dB at 1559.6 nm, thermal drift -131 pm/K (printed -0.131 nm/C), tuning range ~12 nm over
  25-115 C, core 2.0 x 1.44 um, design values (23 x 23, 400 GHz / 3.2 nm, 70 arms, order 20, L_FPR 320 um,
  R 1000 um), footprint ~0.55 x 0.27 cm2.
- `cmp_lit_yang2011_su8_facet_lensed` (fiber_chip_coupler.edge, 2 metrics): ~6 dB per facet (author_estimate),
  ~14 dB fiber-to-fiber of the 0.22 cm straight reference waveguide (measured).

Not entered: 0.17 dB/mm cut-back propagation loss (cited, ref. [17]; p.2); polarization-dependent wavelengths 0.24 /
0.72 / 0.02 nm and their theoretical values (no parameter, see gaps); thermo-optic coefficient -1.21e-4 per C (material
constant, no parameter); 400 GHz output waveguide separation ~4.5 um (pitch or gap not stated, p.2); R = 100 um
crosstalk (only "much larger", p.3); generic "excess loss about 5-10 dB" (p.2; per-device values entered). Abstract
values were read from a page-1 render of the cached PDF (text layer drops minus signs and exponents).

Fab: org_zhejiang_university (D72): "we design and fabricate" (p.1) and all authors at Zhejiang University. SEM
labels "ZJU MOI" are image annotations, not a facility statement (no facility entered).

## lit:zheng2013 (2 components / 20 metrics)

- `cmp_lit_zheng2013_ring_mux_1x8_g240` (wdm.mrr, soi_rib, 14 metrics): IL < 2.5 dB per channel (scope unspecified),
  3-dB passband > 0.3 nm, FSR ~12.4 nm measured and ~12.8 nm design, spacing ~2 nm, channel isolation > 18 dB,
  8 channels, 7.5 um nominal radius, 390 nm ring / 300 nm bus width, 220 nm etch, 300 nm SOI, 240 nm gap, ~45 um
  ring-to-ring separation.
- `cmp_lit_zheng2013_ring_mux_1x8_substrate_removed` (wdm.mrr, 6 metrics): 4.13 mW/FSR (Fig. 2(a) ring),
  2877 pm/mW derived (4.2 nm / 1.46 mW), other 7 rings 4.2-4.7 mW/FSR, total 4.1 mW to a 1.6 nm grid, 1.6 nm spacing
  after tuning, FSR 12.4 nm (Fig. 2(a) label).

Not entered: "< 3 uW/GHz" (frequency-form tuning efficiency; conversion needs an assumed wavelength); "4.7 mW/FSR"
(p.1, equals the largest per-ring value already in the range row); values of refs. [1]-[6] (80 mW, 3.9 / 2.4 mW/FSR,
28 / 4.4 uW/GHz, 56 / 18 mW/FSR; cited); Fig. 1(a) labels 340 / 17 / 16 um (roles not stated); wafer-scale resonance
spread < 1.6 nm (platform study, p.1); Fig. 2(b)-(c) through-port depths (no printed values).

Fab: empty. "taped out using a 130 nm SOI CMOS process" names no foundry (process_name kept, D536). The back-side
substrate removal is first person ("We used a back side substrate removal technique", p.2 Sec. 3) and all authors are
at Oracle Labs, but Oracle Labs is not in the registry (see missing orgs).

## Missing fab / facility orgs

- "Oracle Labs" (p.1 affiliation; fab candidate for the substrate-removal post-processing on
  `cmp_lit_zheng2013_ring_mux_1x8_substrate_removed` only, first-person p.2 Sec. 3; D440). No `oracle` id or alias in
  `organizations.csv` / `org_aliases.csv`.
- "Aidi Corporation" (p.1 affiliation of K. Okamoto, cheung2014): not a fab statement, listed only in case the
  coordinator prefers a two-org fab; no fab role proposed.

## Judgment calls for the auditor

1. cheung2014 fab = UC Davis with one co-author printed at another company (borderline; cheung2015 precedent).
2. cheung2014 2.78 dB/cm `author_estimate`: the Fabry-Perot method needs the facet reflectivity and the only one
   printed is the 3D-FDTD 31 % (D608). The merged cheung2015 rows (same group, same method, FDTD 42.2 %) are
   `measured`: one of the two should be aligned.
3. cheung2014 Table II pitches (450 nm) left out as inconsistent with the printed widths; Table II slab radius f
   entered as `fpr_length_um` (akca2018 focal-length precedent).
4. cheung2014 crosstalk ~4 dB `measured` although Sec. IV says "estimated" (read from the measured spectrum).
5. yang2011 400 GHz excess loss scoped `de_embedded` / `reference_structure`: the normalization reference is
   described only for the 100 GHz AWGs; Fig. 7 is labelled normalized and the text calls it excess loss.
6. yang2011 fabricated core sizes (2.05 x 1.5, 2.2 x 1.57, 2.0 x 1.44 um) entered as width / thickness `derived`
   (um -> nm of a fabricated, not design, dimension; measurement method not stated). The 2.0 x 1.5 um design core is
   only in core_material.
7. yang2011 100 GHz shared design values (48 x 48, arms, order, FPR, gap) on both bend-radius rows; 48 x 48 is
   printed for the design (abstract, Fig. 3 caption for R = 100 um).
8. yang2011 abstract "crosstalk between adjacent channels is less than -15 dB" assigned to the R = 150 um row as
   `crosstalk_adjacent_db` (body: "channel crosstalk ... lower than -15 dB", Fig. 5 = R = 150 um).
9. zheng2013 split into two rows: the 240 nm gap device (spectral values) and the substrate-removed device of the
   tuning section, whose gap is not stated (D159). Whether the Fig. 1(c) values are pre- or post-removal is not
   stated. Channel isolation > 18 dB (introduction only) put on the 240 nm row.
10. zheng2013 4.13 mW/FSR kept as printed although Fig. 2(a) labels (1.46 mW, 4.2 nm, FSR 12.4 nm) give 4.31 mW
    (D417 note).
11. zheng2013 ~45 um "ring-to-ring spatial separation" entered as `pitch_um`.

## Registry gaps

- Polarization-dependent wavelength shift on `wdm` (confirmed again; D667 gap): yang2011 0.24 nm (R = 100 um, Fig.
  4(a), p.3-4), 0.72 nm (R = 150 um, abstract, p.3-4), 0.02 nm at 1559.6 nm (400 GHz, Fig. 6, p.4). Proposed
  `pd_wavelength_nm` (nm, wdm / resonator / polarization): "TE-TM shift of the channel peak wavelength, magnitude as
  printed".
- Tuning efficiency in frequency per power (zheng2013 "< 3 uW/GHz", p.1, p.2): proposed `tuning_power_uw_per_ghz`
  (uW/GHz, wdm / resonator / phase_shifter) to avoid a wavelength-dependent conversion.
- Material thermo-optic coefficient (yang2011 -1.21e-4 per C, p.5): low priority, material rather than component.
