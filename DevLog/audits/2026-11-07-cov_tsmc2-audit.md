---
title: Fresh-context audit of component batch cov_tsmc2 (TSMC OFC 2025 Th1G.2, SiN building blocks on the TSMC SiPh platform)
date: 2026-11-07
mode: read-only audit subagent; patch validated on a scratchpad copy of the batch (patch_component_staging.py 23 changes, re-apply 0 changes; merge_component_staging.py --dry-run "+12 components, +72 metrics; errors 0", only the pre-existing WARN on merged row cmp_lit_ni2025b_pimmwc-m18). Real batch CSVs not modified, nothing merged
patch: data/_staging/components/cov_tsmc2/patch.yaml
---

# Audit cov_tsmc2 (2026-11-07)

Source: `lit:lu2025a`, `references/lu2025a/text.md` (3 pages, clean text layer) read in full. The page-1 title matches
the source row and the source.json title; the paper is not a correction. No `cmp_lit_lu2025a_*` rows exist in the
merged tables.

Figure reading method:
- Fig. 2(a)-(e) (p.2) and Fig. 3(b) (p.3) are embedded raster images. They were read on 600 dpi page renders. Box,
  median and whisker lines were located per pixel row inside each box column, and calibrated against the plot frame
  rows and, for Fig. 3(b), the y tick rows. Native resolution is about 200 dpi, so one native pixel is about
  0.003 dB/cm in Fig. 2(a).
- Fig. 4(a)-(c) (p.3) are PDF vector paths. Box edges, median lines, whisker caps and the two Fig. 4(a) traces were
  read exactly from the path coordinates against the y tick paths (0 to -2.0 dB, 0.5 dB steps).

## Counts

| | ok | imprecise | wrong | miss (added) |
|---|---|---|---|---|
| metrics (57) | 54 | 3 | 0 | 15 |
| components (10) | 10 | 0 | 0 | 2 |

Imprecise: sm_wg_pecvd_opt-m2 (value), edge_coupler-m1 (scope, Q1), edge_coupler-m12 (notes contradict the basis).
Additive notes, not counted as imprecise: edge_coupler-m2.

## Checks common to all rows

- Fab `org_tsmc`: ok.
  - Platform statement: TSMC's silicon photonics platform (p.1 Abstract). The authors integrated the PECVD film onto
    the existing SiPh platform (p.1 Sec. 1).
  - Additional p.2 Sec. 2 support, not cited in the notes: the closing sentence calls the film "our SiN film
    fabricated by" CMOS-compatible technologies.
  - Thanks to TSMC's module and fabrication teams (p.3). All authors are at TSMC (p.1).
  - D80b + D84a/b are met. No facility.
- Platform: ok.
  - Single-layer SiN parts are `sin` (rule 11; same as the merged AIM SiN-layer row
    `cmp_ectc51909_2023_00048_sin_wg_lowloss`).
  - The SiN-to-Si transition is `si_sin_multilayer`.
  - Benchmark consequence: the SiN rows form a TSMC SiN column. They are never TSMC SiPh: the `wg_loss` row note
    says SiN layers of Si-SiN stacks are not entered in the SiPh column. The transition (SiPh family) has no
    benchmark row.
- Method `unspecified` everywhere: ok. The paper names no cutback, reference structure, die count or wafer count.
  The loopback configuration is printed only for Fig. 4(a), and m1 / m2 carry `loopback`.
- Wavelength: the four CWDM grid points 1271 / 1291 / 1311 / 1331 nm are the plotted x positions. The O-band rows use
  the Fig. 4(a) axis 1260-1360 nm. No inference flags are needed.
- D259 / rule 3: the thermo-optic coefficients and the ~21 dBm power figure are cited ([2]-[4]) and correctly not
  entered. No value is reproduced from the authors' earlier work.

## Findings per component (figure readings by the audit)

| component / rows | entered | audit reading (locator) | verdict |
|---|---|---|---|
| sm_wg_pecvd_opt m1 | 0.16 dB/cm, 1311, text | p.2 Sec. 2 prints 0.16. The Fig. 2(a) box is about 0.145-0.165 (median unresolved, centre about 0.155) | ok |
| sm_wg_pecvd_opt m2 | 0.12 median, 1271 | Three resolved lines: box top 0.135, median 0.126, box bottom 0.116. Whiskers 0.104-0.152 | imprecise -> 0.125 |
| sm_wg_pecvd_opt m3 / m4 | 0.15 / 0.19 | 1291: box 0.145-0.165, median unresolved. 1331: median 0.191 (box 0.18-0.20) | ok |
| mm_wg_pecvd_opt m1 | 0.124, 1311, text | Box 0.120-0.133 | ok |
| mm_wg_pecvd_opt m2 | 0.085 median, 1271 | Median merged with the box top: the merged band spans 0.085-0.093, median line centre about 0.087. Box bottom 0.061, whiskers 0.053-0.106 | ok (within the stated +/- 0.01) |
| mm_wg_pecvd_opt m3 / m4 | 0.12 / 0.14 | 1291: box 0.110-0.127, unresolved. 1331: median 0.141 (box 0.127-0.156) | ok |
| width rows (opt, base) | 800 / 1500 nm, design_target | p.2 Sec. 2: the SM / MM widths are stated in the same sentence as both the baseline and the optimized losses | ok |
| sm / mm_wg_pecvd_base m1 | ~0.4, 1311, text | p.2 Sec. 2 prints ~0.4 for both. Figure medians at 1311: SM about 0.40 (box 0.39-0.41), MM about 0.38 (box 0.37-0.39) | ok |
| bend_r30 m1 | ~0.004 median, 1311, text | p.2 Sec. 2. Fig. 2(b) at 1311: box 0.0035-0.0039, median about 0.0037 | ok |
| bend_r30 m2-m4 | 0.0021 / 0.0030 / 0.0050 | 1271: median about 0.0021 (merged with the box bottom 0.0020, top 0.0023). 1291: box 0.0028-0.0032, unresolved. 1331: median 0.0050 (box 0.0047-0.0053) | ok |
| bend_r30 m5 / m6 | 30 um, 800 nm | p.2 Sec. 2 "30μm radius"; Fig. 2(b) labels 30 um and 800 nm | ok |
| bend_r30 parameter | bend_loss_db_per_90 | Fig. 2(b) draws a quarter-circle. The text gives a median insertion loss with no angle; the assumption is noted | ok |
| taper_sm_mm m1-m4 | 0.0009 / 0.0010 / 0.0010 / 0.0013 | 1271: median 0.0009 (box 0.0008-0.0016). 1291: 0.00105 (box 0.0009-0.0012). 1311: box 0.0008-0.0011, unresolved. 1331: 0.00127 (box 0.0011-0.0015) | ok |
| taper_sm_mm m5-m7 | 50 um, 800 nm, 1.5 um | Fig. 2(c) labels | ok |
| crossing m1-m4 | 0.023 / 0.028 / 0.034 / 0.040 | 1271: median about 0.023 (merged with the box bottom). 1291: 0.028 (box 0.025-0.030). 1311: 0.034 (box 0.031-0.038). 1331: about 0.041 (merged with the box top; box 0.038-0.042) | ok |
| mmi_1x2 m1-m4 | excess 0.076 / 0.043 / 0.031 / 0.048 | 1271: median 0.075 (box 0.072-0.077). 1291: box 0.040-0.046, unresolved. 1311: box 0.029-0.033, unresolved. 1331: 0.048 (box 0.043-0.053) | ok |
| mmi_1x2 parameter | excess_loss_db | The axis says "IL (dB)", but a few hundredths of a dB on a 1x2 excludes the 3 dB split (rule 6) | ok |
| sin_si_transition m1 / m2 | ~0.03 TE / ~0.06 TM, text | p.2 Sec. 3. Fig. 3(b) at 1311: TE box 0.026-0.039 (unresolved), TM median 0.057 | ok |
| sin_si_transition m3-m8 | TE 0.039 / 0.028 / 0.040; TM 0.056 / 0.055 / 0.068 | TE: 1271 median 0.038; 1291 box 0.025-0.031; 1331 box 0.034-0.044 (both unresolved). TM: 1271 0.0565; 1291 about 0.055 (merged with the box bottom); 1331 0.068 | ok |
| sin_si_transition m9 / m10 | PDL < 0.038 (1271-1331); Si tip < 90 nm design_target, lower_tip_width_nm | p.2 Sec. 3. The Si taper is the lower layer | ok |
| edge_coupler m1 | < 1 dB, O-band, loopback, scope unspecified | See Q1. Fig. 4(a) vector traces: TE 0.647-0.969 dB, TM 0.783-0.854 dB over 1260-1360 nm | imprecise -> loopback_half |
| edge_coupler m2 | PDL < 0.2 dB | Vector traces: TE-TM difference up to 0.206 dB at 1260-1263 nm, below 0.2 dB elsewhere. Additive note | ok |
| edge_coupler m3-m6 (TE, per_facet) | 0.74 / 0.79 / 0.84 / 0.89 | Vector medians 0.739 / 0.790 / 0.844 / 0.893 dB. Boxes 0.69-0.81, 0.76-0.86, 0.79-0.90, 0.86-0.96 | ok |
| edge_coupler m7-m10 (TM, per_facet) | 0.83 / 0.81 / 0.75 / 0.70 | Vector medians 0.831 / 0.806 / 0.745 / 0.700 dB. Boxes 0.74-0.96, 0.68-0.87, 0.67-0.82, 0.64-0.78 | ok |
| edge_coupler m3-m10 scope | per_facet | The axis is printed "EC loss per facet". How per facet was isolated is not stated; method unspecified is correct | ok |
| edge_coupler m11 | std 0.1 dB, 1260-1350 nm | p.3 Sec. 4. The population is not stated (noted). Statistic std is never used in the benchmark (D901) | ok |
| edge_coupler m12 | MFD 5 um, specification | Basis ok. The notes said "Design target" | imprecise (notes) |
| components (10) | class, platform, core / cladding, fab, process, notes | Edge-coupler cladding: BEOL films are replaced by oxide, as printed. Taper class waveguide_platform.other follows in-layer taper precedents (dong2021, dumon2004). Crossing.other: the design type is not stated | ok |

Fig. 4(a) panels: caption (b) TE and (c) TM, and the in-panel labels match (TE at x about 313 pt, TM at x about 469 pt).
Fig. 4(a) legend: blue = TE, red = TM.

## Misses (added in the patch)

1. `sin_si_transition-m11` core_thickness_nm 270, design_target. Locators: p.1 Sec. 2 gives the 270 nm top Si. p.2
   Sec. 3 gives the second stage ending in 270 nm Si. The transition_bilayer cross-section requires
   core_thickness_nm. The thin-Si and SiN thicknesses are not printed.
2. PECVD-baseline figure rows at 1271 / 1291 / 1331 nm, one row per wavelength (rule 7):
   - SM 0.31 / 0.40 / 0.46 dB/cm (`sm_wg_pecvd_base-m3..m5`); MM 0.25 / 0.38 / 0.42 dB/cm (`mm_wg_pecvd_base-m3..m5`).
   - The distiller entered the optimized-film figure rows but only the baseline text value.
3. LPCVD baseline (Q3): two components (`sm_wg_lpcvd_base`, `mm_wg_lpcvd_base`), four figure rows each.
   - SM 0.24 / 0.24 / 0.24 / 0.30 dB/cm; MM 0.11 / 0.15 / 0.15 / 0.16 dB/cm.
   - Widths are not entered: the 800 nm / 1.5 um widths are stated for the PECVD waveguides only.

No other miss:
- SiN thickness, the cladding stack, and the MMI and crossing dimensions are not printed.
- The edge-coupler tip width is "optimized" without a value.
- The Si grating coupler, MZM, MRM and Ge PD in Fig. 1 are schematic only.
- The bend 3-sigma value is a registry gap (Q2).

## Rulings on the distiller's questions

1. **Edge coupler "< 1 dB" loopback statement (m1): rule `loopback_half`, basis measured (patch).**
   - The paper does not print the halving, but its own data fixes the scope. The Fig. 4(a) loopback traces sit at the
     per-facet level at every CWDM point:
     - TE 0.66 / 0.71 / 0.79 / 0.85 dB; TM 0.83 / 0.81 / 0.80 / 0.79 dB.
     - All fall inside the whiskers of the per-facet panels Fig. 4(b)-(c).
     - A two-facet total would be about 1.4-1.8 dB.
   - This is the lorenzen2026 case (D452: loopback_half, measured, no total printed, no arithmetic shown, D167).
     It is not the song2026 case: there the two-coupler path itself was unstated. Here "loopback configuration" is
     printed.
   - The per-facet box plots m3-m10 stay `per_facet` as printed (axis label).
   - m2 (PDL) needs no scope.
   - Benchmark: the edge_il row accepts per_facet and loopback_half, and an `lt` bound on a lower-is-better row is
     admissible. The 1 dB bound does not set the cell either way.
2. **3-sigma statistic: registry gap confirmed.**
   - Recommendation: add `three_sigma` to the statistic enum (value = the printed 3-sigma, no conversion), treated
     like `std` in the benchmark (never a cell, D901).
   - Until then the bend's ~0.001 dB 3-sigma (p.2 Sec. 2) stays in the component notes. Converting it to std
     (0.00033) would be a derived row resting on a two-digit printed approximation, so it is not proposed.
3. **LPCVD baseline: enter (patch), fab org_tsmc with a borderline note.**
   - Fig. 2(a) caption: SM and MM SiN waveguides "fabricated by three processes". The LPCVD panel is the paper's own
     measurement of a distinct process, so rule 9 makes it a component row.
   - Identity is clear (SM / MM, LPCVD baseline); only widths and stack are unstated. That is not a D159 case.
   - Fab: same basis as the PECVD rows (all authors TSMC, fabrication-team thanks, D84b). The p.1 platform sentence
     names only the PECVD building blocks. The text explains PECVD by the MEOL thermal budget, so the LPCVD flow may
     not sit on the same wafer.
   - Alternative: fab empty. The D925 affiliation rule would then still place the rows in TSMC SiN once lu2025a is in
     `source_affiliations`.
   - Benchmark effect: none. The LPCVD medians (best 0.11 dB/cm) are above the PECVD-optimized 0.085.
   - To keep them out, drop the two add_components and their eight rows.
4. **Benchmark: figure medians may enter (D901 admits extracted_from_figure).**
   - The text values (1311 nm) agree with the figure at the same wavelength, so D911 (text preferred over a
     conflicting figure reading) does not trigger.
   - The best cells come from other wavelengths, which have no text value.

## Corrected benchmark-relevant values (TSMC SiN column; all fab org_tsmc, platform sin, row_kind fabricated)

| benchmark row | best value after the patch | row | other values |
|---|---|---|---|
| wg_loss (dB/cm) | 0.085 (MM 1.5 um, 1271 nm, Fig. 2(a) median; audit reading about 0.087, range 0.085-0.091) | mm_wg_pecvd_opt-m2 | Text: MM 0.124, SM 0.16 at 1311 nm. SM figure: 0.125 / 0.15 / 0.19 |
| bend_loss (dB per 90 deg) | 0.0021 (R 30 um, 1271 nm, figure median) | bend_r30-m2 | Text: ~0.004 median at 1311 nm |
| edge_il (dB per facet) | 0.70 (TM, 1331 nm, Fig. 4(c) median; vector reading 0.700) | edge_coupler-m10 | TE best 0.74 (1271 nm). Text: < 1 dB over the O-band (loopback_half). 5 um MFD lensed fiber |
| mmi_el (dB) | 0.031 (1311 nm, figure; box 0.029-0.033) | mmi_1x2-m3 | 0.043-0.076 at the other wavelengths |
| crossing (dB) | 0.023 (1271 nm, figure median) | crossing-m1 | 0.028 / 0.034 / 0.041 |

- The TSMC SiN column fills 5 rows, at or above `min_rows_per_column` 3.
- Every best cell is a figure median at a CWDM point. No cell rests on a bound or a std.
- SiN-Si transition: ~0.03 dB TE, ~0.06 dB TM at 1311 nm (text). Platform si_sin_multilayer; no benchmark row.

## Numbered coordinator questions

1. Edge coupler m1 scope: accept `loopback_half` (patch; recommended), or keep `unspecified` by dropping the
   edge_coupler-m1 op.
2. Registry: add statistic `three_sigma` (recommended); benchmark filter to treat it like `std`.
3. LPCVD baseline: keep the added rows with fab org_tsmc (recommended), keep them with fab empty, or drop them.
4. PECVD-baseline figure rows at 1271 / 1291 / 1331 nm: keep (recommended, rule 7 consistency with the optimized
   rows) or drop the six add_metrics.

## Registry gaps confirmed

- Statistic for a printed 3-sigma spread. Skipped value: bend ~0.001 dB 3-sigma at 1311 nm, p.2 Sec. 2.
  Proposed definition: `three_sigma` = three standard deviations of the stated population, as printed.

## Missing organizations

None (org_tsmc exists).
