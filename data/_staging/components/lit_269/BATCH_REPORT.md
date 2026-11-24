# lit_269 batch report

Papers: lit:evans2015, lit:qiu2018a, lit:tien2011, lit:puckett2019. Page-1 titles match the source rows; no garbled
text layer. Total 25 components / 142 metric rows. `merge_component_staging.py --dry-run`: +25 components, +142
metrics, 0 errors (two pre-existing warnings on other batches: cmp_lit_guo2024a_exc02, cmp_lit_ni2025b_pimmwc).
verified_on 2026-11-24. Figure values of evans2015 Fig. 3(c) and tien2011 Fig. 3 were read from the PDF vector data;
qiu2018a Fig. 5(d) / 6(b) from the embedded figure images (pixel reads, axis ticks calibrated).

## lit:evans2015 (10 components / 59 metrics)

- `cmp_lit_evans2015_tio2_planar_film` (waveguide_platform.other, platform other, 8): prism-coupled slab loss at
  633 / 780 / 850 / 980 / 1310 / 1550 nm (~2.83 / 1.62 / 1.50 / 0.89 / 1.03 / 1.44 dB/cm, Fig. 3(c) reads), 250 nm
  film, 3 um thermal oxide.
- `cmp_lit_evans2015_channel_w250 / _w500 / _w750 / _w1000` (waveguide_platform.straight, 4 each): single-mode
  cutback loss 7.5 dB/cm at 633 nm (printed), ~3.55 at 980 nm and ~1.6 at 1310 nm (Fig. 3(c)), 1.2 dB/cm at 1550 nm
  (printed); mask width, 250 nm thickness, 3 um BOX.
- `cmp_lit_evans2015_rib_w750` (waveguide_platform.straight, 9): multimode rib loss 6.5 (633, printed), ~3.40 (850),
  ~2.55 (980), ~1.50 (1310), 3.2 dB/cm (1550, printed p.8); width 750 nm from the Fig. 3(c) colour key, 250 nm
  first layer, 265 nm secondary slab, BOX.
- `cmp_lit_evans2015_channel_facet` / `_rib_facet` (fiber_chip_coupler.edge, 2 each): 7 / 4 dB per facet
  (author_estimate, origin not stated) and ~2 dB per facet overlap calculation (simulated, "in all cases").
- `cmp_lit_evans2015_ring_r150_w750` (resonator.ring, 12): Q_L 1.5e5 best, FSR 1.052 nm, ng 2.423 (derived from
  FSR), extinction 6.0 dB (derived from T0 = 0.25), Q0 2e5 and 2.1 dB/cm (author_estimate, assumed under-coupled),
  geometry (r 150 um, 750 nm, gap 1.4 um, layers).
- `cmp_lit_evans2015_ring_r150_w500` (resonator.ring, 10): Q_L 1.6e5 best at ~780 nm (top-view scattering), Q0 >= 1.6e5
  (author_estimate lower bound), ng 2.562 (simulated), 5.6 dB/cm (author_estimate), geometry.

Not entered: rms roughness film 1.2 nm / waveguide 3.8 nm (AFM, no parameter); fabricated-width excess 210-280 nm
over the mask width (a range over widths, p.5); refractive index 2.33-2.23 (material); loss-vs-wavelength exponents
2.1 / 2.0 (fit coefficients, no parameter); literature values in the introduction and p.7-8 comparisons (refs. [1],
[2], [19], [25], [28], [29]; rule 3); Fig. 2 simulated mode profiles.

Fab / facility: fab org_cornell_university (first person "We fabricate", author contributions; all authors in Cornell
units, D154 parent). Facilities org_cornell_nanoscale_facility and org_cornell_center_for_materials_research ("This
work was performed at", p.10). No missing orgs.

## lit:qiu2018a (8 components / 31 metrics)

- `cmp_lit_qiu2018a_mrr_gap460` (resonator.ring, soi, 17): MPF / resonance FWHM 170 MHz (best, measured) and
  170-270 MHz over the 2.0-18.4 GHz tuning span (Fig. 5(d)), Q_L 1.14e6 (derived from the FWHM), Q_i 2.67e6 and
  0.25 dB/cm (author_estimate, method not stated), FSR 0.325 nm, ~14 dB fiber-to-fiber through-port IL (two GCs),
  14.4 mW heater power for a 16.4 GHz shift, geometry (20 um half-ring radius, 500 nm / 2 um widths, 850 um straight,
  1.99 mm perimeter, 460 nm gap, 220 nm Si, 2 um BOX), ~0.05 mm2 area.
- `cmp_lit_qiu2018a_mrr_gap250 ... _gap430` (7 gap-series siblings, resonator.ring, 2 each): bw_3db_ghz 1.7 GHz
  (250 nm, printed) and Fig. 6(b) reads ~1.30 / 0.76 / 0.62 / 0.39 / 0.39 / 0.38 GHz (280-430 nm), gap design.

Not entered: MPF rejection ratio 26.5 dB, SNR 23.7 dB, per-gap rejection ratios (Fig. 6(b)), MPF IL ~42 dB (RF
system metrics of the link, not of the ring); Fig. 3(b) OSA notch (resolution-limited per the paper); "Q increased by
9 times" (ratio); 50 um taper length (no taper parameter for resonator); simulated mode profiles (Fig. 1); Table I
rows of other works; phase modulator / PD / EDFA data (setup equipment, rule 13). Main-device Fig. 6(b) point
(~0.17-0.19 GHz) not duplicated (printed 170 MHz entered).

Fab: empty. "We fabricate the MRR" (p.3) but the authors are at HUST / WNLO and at the State Key Laboratory of
Optical Communication Technologies and Networks, Wuhan Research Institute of Posts Telecommunications (two unrelated
orgs, D154). process_name empty: only "standard CMOS fabrication process" + 248 nm DUV + ICP is printed. No facility.

## lit:tien2011 (5 components / 43 metrics)

- `cmp_lit_tien2011_ring_r5mm_t40` (resonator.ring, sin, 9): Q_i 18 M and 0.021 dB/cm at 1060 nm (Table 1), notch
  bandwidth 16 MHz, coupling 0.8 % (author_estimate), notch depth ~10.6 dB (Fig. 3(a) vector read), geometry.
- `cmp_lit_tien2011_ring_r5mm_t50` (resonator.ring, 13): Q_i 1 M / 28 M / 19 M and 0.208 / 0.011 / 0.020 dB/cm at
  1550 / 1310 / 1060 nm, notch bandwidth 38 MHz, coupling 0.55 %, notch depth ~3.8 dB, geometry.
- `cmp_lit_tien2011_ring_r4mm_t50` (resonator.ring, 8): Q_i 21 M / 11 M and 0.015 / 0.035 dB/cm at 1310 / 1060 nm,
  geometry.
- `cmp_lit_tien2011_adddrop_ring_r2mm_t80` (resonator.ring, 8): Q_i 7 M at 1550 nm, 3-dB bandwidth ~300 MHz,
  coupling ~5 %, drop loss 1.2 dB (Fig. 3(c) drop peak -1.21 dB), through notch ~14.2 dB, geometry.
- `cmp_lit_tien2011_sin_wg_5p3um_t50` (waveguide_platform.straight, 5): simulated scattering-limited loss 0.004 /
  0.008 / 0.021 dB/cm at 1550 / 1310 / 1060 nm (Fig. 1 model), geometry.

Not entered: 2.9 dB/m for the 2.8 um x 80 nm waveguide (p.2-3 "We have demonstrated ... [15]" and p.5 "[15]";
Table 1 repeats it on the 80 nm ring row but it matches the cited value and not Q_i 7 M; rule 3, D80i, D259);
"High loss" / "No transmitted power" / "Multi-mode" Table 1 cells (no value); round-trip loss ~1 % (no parameter);
rms roughness 4.75 / 0.175 nm and correlation lengths (model inputs, no parameter); minimum radii for negligible bend
loss 7 / 3 / 2 / 1.5 mm (simulated thresholds); 8 um cladding of the 80 nm ring (upper vs total not stated); laser
linewidths of the setup (rule 13); introduction values of other works (rule 3).

Fab: empty, missing org (see below). No facility.

## lit:puckett2019 (2 components / 9 metrics)

- `cmp_lit_puckett2019_uhq_ring` (resonator.ring, sin, 8): FWHM 1.76 MHz at 1563 nm (measured), 0.00123 dB/cm
  (printed 0.123 dB/m, author_estimate), Q 216 M as q_intrinsic (author_estimate, title only), 9 um / 40 nm / R 11.8 mm,
  15 um BOX, 6 um upper cladding.
- `cmp_lit_puckett2019_sbs_laser` (laser.other, 1): Brillouin lasing threshold 10 mW on-chip (D396 cross-note).

Not entered: theoretical 10 mHz linewidth (possibility, not a result); FSR as "one fourth of the Brillouin shift"
(no number); Fig. 1(b) scattering image. Fab empty ("fabricated as in [5]", passive, no org; no acknowledgment).

## Missing fab / facility orgs

- "LioniX BV" (fab role): lit:tien2011 p.6 Acknowledgments ("LioniX BV for fabrication"), affects all 5 tien2011
  rows. Kept apart from org_lionix_international per D278 / D545 (same open item as a2011, bauters2013, mu2016,
  zhuang2016); once a time-correct org exists, a fix batch should set it on these rows.

## Judgment calls for the auditor

1. Class: tien2011 notch / add-drop rings and the qiu2018a MPF ring entered as `resonator.ring`, not `wdm.mrr`
   (D400: single rings characterized for Q and used as microwave-photonic / notch filters, not channel filters in a WDM
   path). Merged MPF precedents are split (taddei2019 / lu2024a wdm.mrr, burla2015 resonator.ring).
2. puckett2019 216 M (title only, unqualified): entered as `q_intrinsic` author_estimate, because f / 1.76 MHz at
   1563 nm is about 1.09e8 and 216 M is about twice that (critical coupling; the Fig. 1(a) dip reaches near zero). A
   strict reading of the "unqualified Q -> q_loaded" pitfall would store a value that contradicts the printed FWHM.
3. tien2011 q_intrinsic `measured` (paper fixes the regime by comparing rings with various couplings, p.4; D425
   lee2012 precedent), but the printed numbers are internally inconsistent: 1060 nm t40 notch 16 MHz gives f / FWHM
   about 17.7 M, equal to the "intrinsic" 18 M; 1310 nm 38 MHz with a 3.8 dB notch fits over-coupling at Q_i 28 M
   although the text says under-coupled. Notes record this (D417); an auditor may prefer author_estimate.
4. tien2011 80 nm ring radius 2 mm (Table 1 + text) vs 1.5 mm (Fig. 3(c) caption): 2 mm entered with a conflict note.
5. tien2011 dB/m losses converted to dB/cm `derived` (D256) as fit outputs; ring Table 1 rows are one row per
   R / t / w design (coupling gaps not stated), so the Fig. 3 notch filters share the rows with the Table 1 values.
6. qiu2018a: MPF RF FWHM taken as the ring linewidth (the paper does so); Q_L 1.14e6 `derived`; gap-series siblings
   as 7 component rows with `bw_3db_ghz` (axis "FWHM Bandwidth (GHz)", caption "3 dB bandwidth") while the main ring
   keeps `linewidth_mhz` 170 (printed MHz); fab empty under D154 despite first-person fabrication.
7. evans2015: rib width 750 nm taken from the Fig. 3(c) colour key (`extracted_from_figure`); per-facet 7 / 4 dB
   `author_estimate` ("We estimate", origin not stated; D418 nader2025, not D167); the ~2 dB overlap value entered on
   both facet rows (stated "in all cases"); planar film as waveguide_platform.other (jung2021 / neutens2025 precedent);
   CCMR as a facility because the sentence names it as a place where the work was performed (it is also a grant
   program in the support sentence).

## Registry gaps (skipped value + locator + proposed definition)

- `roundtrip_loss_pct` (resonator): tien2011 ~1 % ring round-trip loss from the fit, p.5 Sec. 4. Definition: fraction
  of power lost per round trip inside the resonator (intrinsic), as fitted. (Same candidate as roundtrip_loss_db in
  D420 / D545.)
- `rms_roughness_nm` (waveguide_platform, resonator): tien2011 sidewall 4.75 nm / surface 0.175 nm (p.3, AFM / SEM),
  evans2015 film 1.2 nm / waveguide 3.8 nm (p.5, AFM). Definition: rms roughness of the stated surface and method
  (already a D418 candidate).
- `taper_length_um` on resonator: qiu2018a 50 um half-ring-to-straight linear taper (p.3 Sec. III).
