# lit_131 batch report (distill, 2026-11-14)

Papers: ma2024, ren2025, kim2023, morenopozas2026, sun2026. All five cached texts are the source-row papers (page-1 titles
match the `lit:` rows); none is a correction / erratum. ren2025 has `garbled_text_layer` (page 8 only, references): no value
was taken from page 8; the values used come from clean passages (p.1-7) and the Fig. 1 / Fig. 2 renders. No supplement is cached
for any paper (kim2023, ren2025 and sun2026 point to Supporting Information for some values; not entered). Figure values were
checked on the page / embedded-image renders: ma2024 Figs. 7, 8, 11-13; ren2025 Fig. 1; morenopozas2026 Figs. 7-8; sun2026
Figs. 2, 4. Validation: `merge_component_staging.py data/_staging/components/lit_131 --dry-run` -> +21 components, +131
metrics, 0 errors (the one warning printed concerns merged row `cmp_lit_ni2025b_pimmwc`, not this batch).

## Per paper

| paper | components | metric rows | notes |
|---|---|---|---|
| ma2024 | 5 | 24 | REC DML laser array (`laser.dfb`), laser-to-PLC photonic wire bonds, two Z-scan PWB test samples (chip to fiber array), purchased pigtailed PLC combiner (`wdm.other`, specification) |
| ren2025 | 3 | 14 | InGaAs/InP SPAD fed by a PWB (`photodetector.spad`), TFLN-DLCS-to-SPAD PWB (`chip_chip_coupler.photonic_wire_bond`), TFLN edge coupler (calibration) |
| kim2023 | 2 | 7 | three-layer PMMA metalens and OAM metasurface on a fiber facet (`micro_optics.metalens`) |
| morenopozas2026 | 2 | 20 | Cassegrain spot-size converter (`mode_converter.converter`, as the authors' 2025 parabolic SSC), SWG grating antenna it feeds |
| sun2026 | 9 | 66 | eight SiN OPA designs S1-S8 (`free_space_emitter.other`) + one 168-device population row (D165) |
| total | 21 | 131 | |

## Values deliberately not entered

- ma2024: grating coupling coefficients about 93 / 30 /cm and kL 0.75 (p.3; the kappa sentence carries ref. [24], rule 3);
  facet reflectivities AR < 1 % / HR > 97 % (reflectivity_pct not allowed for laser); theoretical single-mode yield 90 % /
  43.1 % (NTGM calculation, p.2 Fig. 1, no parameter); dynamic extinction ratio > 5 dB and mask margin > 20 % (p.6;
  extinction_db not allowed for laser); simulated PWB overlap factors (Fig. 7 panels disagree at the chosen point, about 0.908
  vs 0.867); DML mode profile (Fig. 6, no MFD number); PLC-end (12 x 10 um) and linking-section (1.2 x 0.8 um) PWB
  cross-sections (orientation not stated); Z-scan points other than the optimum.
- ren2025: dark count about 6e-4 'Hz/gate' (p.5, abstract; Table 1 prints 1e-4): a per-gate probability, `dark_count_rate_hz`
  is counts per second and the paper gives no conversion (registry gap below); simulated PWB bending loss < 1e-2 dB/cm for r
  > 90 um (p.3 Fig. 1(d); no bend parameter on chip_chip_coupler) and the Fig. 1(e) coupling-loss curve vs residual oxide;
  bend radius 100 um (min_bend_radius_um not allowed for chip_chip_coupler); DLCS widths w1 / w2 / L1-L3 (not printed); the
  12.3 dB input-to-monitor chip loss (no isolated component; on-chip beam splitter assumed 50:50); DCR before / after PWB
  (Supporting Information, not cached); Table 1 rows of refs. [26], [27].
- kim2023: measured focus about 135 um vs designed 130 / 131 um (no focal-distance parameter); alignment error < 500 nm;
  simulated > 85 % relative efficiency within about 1 um misalignment (Supp. Note 6, relative); hole diameters, 1200 nm
  lattice and ring / tether geometry (no micro_optics role parameter; in core_material / notes); 635 nm single-layer
  results (Supp. Notes 7-8, not cached); OAM pattern error < 5 % (SEM, notes).
- morenopozas2026: design output MFD about 118 um (mfd_chip_um not allowed for mode_converter, as in morenopozas2025);
  input taper loss < 0.1 dB (design statement, origin not stated); parabolic-analog area 3.76e4 um2 and 200 um MFD design
  area 7.46e4 um2 (design comparisons); reflector design values (F, d0, e, beta, c, angles; Table I, in core_material);
  grating radiation strength 6.8 (design) / 5.8 (measured) Np/mm (registry gap below); a1 / a2 / b labels of Fig. 8(a)
  (roles only drawn).
- sun2026: PER 26.1 dB and DOLP 99.5 % of the packaged S5 beam (per_db not allowed for free_space_emitter, registry gap
  below); about 6 percentage-point efficiency drop of the best packaged device (design not stated); effective apertures
  about 64 / 24 um (design arithmetic / approximate); simulated grating efficiency vs wavelength (Fig. 2(h), grating
  parameters of the curve not stated); grating periods of the fabricated designs (only the design calculation, about 486
  nm, is printed); loss budget Notes S4-S6 (not cached); magnetometer sensitivities 8 / 9 fT/Hz^1/2 (system values).

## Missing fab / facility orgs

- Henan Shijia Photonics Technology Co., Ltd.: fab of the pigtailed PLC combiner (ma2024 p.5 Sec. 3, "fabricated in");
  not in `organizations.csv` / `org_aliases.csv`; `cmp_lit_ma2024_plc_combiner` fab left empty.
- Yunnan University: provider of the InGaAs/InP SPAD chip (ren2025 p.3, p.4 Fig. 2 caption, "provided by"); not in the
  registry; fab left empty also because "provided" is not a fabrication statement (coordinator: fab or note?).
- Used: `org_applied_nanotools` (morenopozas2026 both rows, p.6 Sec. V / VI). Fab empty elsewhere: ma2024 laser and PWBs
  (no fabrication sentence; Vanguard Automation only thanked for PWB support, D450); ren2025 PWB / edge coupler (passive
  sentences, authors at Tsinghua, BAQIS, Yunnan University); kim2023 (first-person sentence, authors at Korea University,
  KIST, ETRI, UST); sun2026 (first-person sentence, authors at Beihang University and Zhejiang Laboratory; DUV + ICP, no
  named process). No facility acknowledged in any of the five papers.

## Judgment calls (for the audit)

1. ren2025 on-chip PDE 13.8 % stored `author_estimate`: the mean photon number rests on an estimated 8.3 dB chip loss
   (12.3 dB measured minus 4 dB per facet taken as half of an 8 dB two-coupler reference; equal facets and equal splitter
   arms assumed, p.6), li2025a / D462 precedent. The alternative is `measured` (alexander2026 used a measured cutback IL).
   APP and jitter stay `measured`.
2. ren2025 SPAD platform `inp` (qi2024 precedent for a vertically illuminated InGaAs/InP chip); PDE `ref_plane` on_chip with
   the PWB coupling in `condition`.
3. ma2024 PWB loss 2-3 dB `author_estimate` (rests on the producer-provided 10 dB PLC loss); the 12-13 dB laser-to-fiber
   total `derived` (before / after comparison of own measurements) on the PWB row with scope `device_total`.
4. ma2024 PLC combiner class `wdm.other` (paper calls it a PLC mux / combiner; type not stated; Fig. 5(a) draws a branching
   tree, which could argue for `splitter.other`); IL `specification` (producer value), O-band inferred.
5. ma2024 Z-scan test samples entered as two `fiber_chip_coupler.photonic_wire_bond` test rows with the best Fig. 8 points
   (`extracted_from_figure`, scope `unspecified`: how the laser-side loss is referenced is not stated).
6. ma2024 bandwidth 21.9 GHz: text says 40-100 mA, Fig. 13 caption / legend 40-70 mA; printed value kept with the conflict
   in the condition (D417). Lasing wavelengths 1309.1-1341.2 nm `author_estimate` (design section, "as a result"; the
   sentence says "four lasers" but lists eight). Laser platform left empty (substrate not stated, D422).
7. ma2024 PWB laser-end width 1.5 um / height 4.5 um taken from the Fig. 7 panel titles (text prints "4.5 um x 1.5 um").
8. kim2023 transmittance 83 % stored as `coupling_efficiency_pct` scope `per_component` (lim2026 / lai2025 precedents);
   focal spot FWHM 3.67 um as `beam_diameter_um` (yang2018 precedent).
9. morenopozas2026 grating antenna: measured transverse MFD 116 um `measured`, longitudinal 235 um `derived` (equivalent
   MFD from the fitted decay constant); design 200 um MFD and -8.5 deg angle `author_estimate` (D82a). Measurement
   wavelength of the near field not stated: wavelength left empty (no required condition).
10. sun2026: one row per OPA design (S1-S8, 21 devices each). Means and standard deviations read off Fig. 4(a) (+/-0.3 %);
    S1-S4, S6, S7 geometry from the Fig. 4 axis labels (`extracted_from_figure`, unit not printed in the label); pitch =
    W + gap `derived` (p.3 definition). 26.5 % assigned to S5 (p.2 names S5; S5 column of Fig. 4(b)). "More than half of
    168 devices above 15 %" stored as a median bound (`gt`, `median`, n 168) on the population row. Efficiency
    wavelength not stated: 795 nm design target, inferred. Scope `device_total` (lensed fiber to free-space power).

## Registry gaps (proposed)

- `dark_count_probability_per_gate` (unit "1", photodetector): dark-count probability per gate of a gated SPAD as printed
  (ren2025 6e-4 'Hz/gate' at 63.2 V, -30 C, 1.25 GHz gating, p.5; qi2024 Table I 7.2e-6 per gate also in notes only).
- `per_db` for `free_space_emitter`: polarization extinction ratio of the emitted beam (sun2026 26.1 dB, p.8).
- `radiation_strength_np_per_mm` (unit 1/mm or Np/mm, free_space_emitter): grating leakage constant alpha
  (morenopozas2026 design 6.8, measured 5.8 Np/mm, p.6 Sec. VI, Fig. 8(b)).
- `focal_distance_um` (micro_optics): measured / designed focal distance of a lens or metalens (kim2023 about 135 um
  measured, 130 / 131 um design, p.7).
- `mfd_chip_um` for `mode_converter` (already noted for morenopozas2025): output MFD of an on-chip spot-size expander
  (morenopozas2026 about 118 um design, p.5).
