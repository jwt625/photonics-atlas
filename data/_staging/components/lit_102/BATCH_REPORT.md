# lit_102 batch report (2026-11-06)

All four cached texts match their source rows (page-1 title); none is a correction, erratum or another paper. No garbled
text layer flagged. jung2025 is an arXiv preprint whose source row is the preprint itself (`arxiv_preprint`, v1, no DOI
in the row): no journal record to compare (D430 / D433 not triggered). Dry-run: +12 components, +103 metrics, 0 errors
(the one warning, ni2025b m18 / m4, is an existing merged row, not this batch).

| paper | components | metrics |
|---|---|---|
| jung2025 | 4 (fiber_chip_coupler.other TIR coupler; waveguide_platform.transition; fiber_interface.connector; fiber_chip_coupler.grating reference) | 23 |
| marchetti2017 | 4 (fiber_chip_coupler.grating: 1 fabricated + 2 design; waveguide_platform.straight) | 40 |
| zhou2022 | 1 (fiber_chip_coupler.grating) | 21 |
| cai2024 | 3 (mode_converter.mdm_mux; waveguide_platform.straight; fiber_chip_coupler.edge) | 19 |

## Not entered, and why

jung2025
- Printed "-1 dB alignment tolerance of 4 um" (p.10): definition not stated; Fig. 4(d) gives a 1-dB half-width of about
  1.7 um from the data points (about 1.3 um from the Gaussian fit), a full width of about 2.6-3.4 um. Entered instead as a
  figure read (`tol_1db_lateral_um` 1.7 approx, extracted_from_figure); 4 um in notes.
- "Within +/-1.5 um, misalignment loss below 0.3 dB" (p.10): no 0.3-dB tolerance parameter; in connector notes.
- Abstract "-0.5 dB bandwidth greater than 100 nm": no 0.5-dB bandwidth on fiber_chip_coupler / fiber_interface; note.
- Simulated optimum (Fig. 2(c), about -0.13 dB) and simulation-experiment offset -0.35 dB: not printed as a coupler
  value / not a component metric; offset in notes.
- Fiber-coupler gap 40-50 um, focal length 40-55 um, MFD at focus 8-11 um: optimization ranges, no single design value
  (no working-distance parameter; candidate already listed in D437).
- 16x1 GST matrix, Y-combiners, SLED, 17.6 GBaud eye: no quantitative component values.
- Table 1 values of other works (Wan, Jimenez, Bundalo, Barwicz, Scarcella, Nair): rule 3.

marchetti2017
- Simulated sweep points (e = 100 nm: 73 %; e = 230 nm: 68 %), directionality 85 % (about 10 % above uniform),
  reflectivity curves (Fig. 4): sweep points / no directionality parameter.
- Per-unit trench and tooth lengths (Table 3): summarized as the derived period range 600-667 nm, F0 0.9 and 24 units.
- Table 1 rows of other works: rule 3. 340 nm comparison value 83 % (-0.8 dB) of ref. 19: rule 3.
- Per-structure Table 2 values not entered one by one (range, mean and the best device are entered).

zhou2022
- Simulated fabrication tolerances (CE above 80 % within poly-Si thickness -60 / +43 nm, shift +/-40 nm, etch -30 /
  +18 nm, width +/-60 nm): no parameter; in notes.
- Shift ds 116 nm, minimum features 181 / 171 nm, per-tooth widths (Fig. 2, plot only): no parameter / plot only.
- "About 0.2 dB" improvement with index-matching fluid: follows from the entered rows.

cai2024
- Polarization-dependent loss below 0.2 dB, mode-dependent loss below 0.3 dB, IL fluctuation below 1.4 dB over
  1480-1640 nm: no `pdl_db` / `mdl_db` / `wdl_db` on mode_converter (registry gap below). Note: the printed per-mode
  losses (1.14 / 1.19 / 0.84 dB) span 0.35 dB, above the printed MDL bound (D417 note on the row).
- "Average insertion losses as low as 1 dB" (abstract): the per-mode rows carry it (mean of the three is 1.06 dB).
- Waveguides written at 54 and 87 mW (Fig. 3 only, 6.3 / 10.5 um): figure-only, not the device of the paper.
- RI contrast about 0.3 % (from measured NA), waveguide spacing 6.0 um, few-mode core 15.0 um, bend lengths: no
  parameter on mode_converter (gap / index contrast); in core_material.
- System results (IL below 5 dB, 4 dB power penalty, OSNR penalties, BER): link / system values.
- Fiber PBSs (about 0.8 dB): purchased setup parts (rule 13).

## Missing fab / facility orgs

None needed by a row. Used: org_university_of_southampton (alias "Optoelectronics Research Centre"), org_imec,
org_huazhong_university_of_science_and_technology,
org_center_of_optoelectronic_micro_and_nano_fabrication_and_characterizing_facility (exact name printed, p.9).

## Judgment calls

1. jung2025 Fresnel subtraction: every absolute loss is printed after subtracting a 0.15 dB Fresnel term that the paper
   does not measure (p.7; per coupler or per loop not stated). Absolute IL rows are `author_estimate`; differences and
   standard deviations (0.37 dB packaging loss `derived`, 0.15 / 0.36 dB `wdl_db`, 0.05 / 0.11 / 0.14 dB std) keep
   measured / derived because a constant offset cancels. Alternative: `measured` as for jung2026 (whose values include
   the Fresnel term).
2. jung2025 classes: TIR coupler `fiber_chip_coupler.other`, platform polymer (jung2026 / yu2023 precedent); the stated
   0.12 dB Si3N4-to-polymer mode transfer as its own `waveguide_platform.transition` row (platform other, no hybrid
   enum; D396 cross-note); MTP plug-and-play as `fiber_interface.connector` with platform empty; the 0.37 dB packaging
   loss `per_interface` (D441 connector practice). The coupler `bw_1db_nm` > 100 nm comes from Table 1 for the packaged
   path (D163).
3. jung2025 fab empty: first-person printing, but authors at Heidelberg University and University of Munster (D468
   itoh2024 / D154). Reference grating coupler (Fig. 4(c) only) entered as a figure-read row with platform empty (D422).
4. jung2025 0.78 dB (16 matrix ports): scope `per_coupler` as the Fig. 5(b) axis states, method unspecified (how the
   per-coupler value is isolated in the 16x1 matrix is not stated).
5. marchetti2017 / zhou2022 GC losses: `loopback_half`, basis `derived` (the papers describe the subtraction of the
   measured propagation loss and / or the halving; cheben2015 precedent). Bandwidths `measured`.
6. marchetti2017 fab org_university_of_southampton: author contributions name C.L. as the fabricator (D395).
   Best-device wavelength 1560 nm read off Fig. 5 (`wavelength_inferred`). Cladding 0.68 um is the simulation layout
   value (deposited thickness not stated), derived per D157.
7. zhou2022 back reflections from the Fabry-Perot contrast: `measured` with "estimated" quoted (rule 4, D394); they
   are reflections into the waveguide. TM loss > 22 dB entered as simulated `insertion_loss_db`, polarization tm.
8. cai2024 class `mode_converter.mdm_mux` (photonic lantern, anelli2024 / leonsaval2014 precedents), platform
   `silica` (fs-written fused quartz, amorim2017 precedent); in scope per D411 (glass chip, dolgaleva2011). Fab
   org_huazhong_university_of_science_and_technology: abstract first-person "fabricated", all authors at WNLO / HUST and
   Optics Valley Laboratory, whose registry parent is HUST (D154 parent rule); borderline against D433 (dual
   affiliations). Crosstalk rows are link-level worst-case values (two lantern chips + FMF), conditions say so.
9. cai2024 0.1 dB/cm `derived` (authors' calculation from IL and cutback coupling loss, reproduces 0.105 dB/cm); facet
   0.21 dB `measured` (truncation method); facet class `fiber_chip_coupler.edge` (kurczveil2013 facet precedent, D469).

## Registry gaps (skipped value + locator, proposed definition)

- `pdl_db`, `mdl_db`, `wdl_db` on mode_converter: cai2024 PDL < 0.2 dB (p.6), MDL < 0.3 dB (p.1), IL fluctuation
  < 1.4 dB over 1480-1640 nm (p.6). Same definitions as on fiber_interface / fiber_chip_coupler (D428 already lists
  wdl_db on mode_converter as a candidate).
- `bw_0p5db_nm` on fiber_chip_coupler / fiber_interface: jung2025 -0.5 dB bandwidth > 100 nm (p.1). "Full width where
  transmission stays within 0.5 dB of its peak" (D443 / D444 list it for wdm).
- `directionality_pct` on fiber_chip_coupler: marchetti2017 simulated 85 % (p.4, Fig. 4). "Fraction of the guided
  power diffracted toward the fiber side (simulated or measured as stated)".
- `index_contrast_pct` on waveguide_platform / mode_converter: cai2024 about 0.3 % (p.5, from measured NA). "Core-
  cladding refractive-index contrast as stated, method in notes".
- `bw_1db_nm` on fiber_interface: jung2025 Table 1 "-1 dB threshold >> 100 nm" for the packaged solution (entered on
  the coupler row per D163).
