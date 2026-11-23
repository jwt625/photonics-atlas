# lit_265 batch report

Date: 2026-11-23. Papers: lit:rawat2023, lit:watanabe2020, lit:ruiz2021, lit:xue2019, lit:wang2017c (fiber-chip
grating couplers: thin-film SiN, few-mode / 2D, perfectly vertical). Page-1 titles match the source rows; no
correction / erratum. rawat2023 has a garbled text layer (pp.4-6, 9): the garbled parts are figure-internal glyphs;
every value from those pages (Sec. 2.2 prose, Fig. 4 caption, Table 1) was checked on the page renders.
Validation: `merge_component_staging.py data/_staging/components/lit_265 --dry-run`: +22 components, +158 metrics,
0 errors (the two warnings name rows of other sources: guo2024a, ni2025b).

| paper | components | metric rows | fab org | facility |
|---|---|---|---|---|
| rawat2023 | 9 (6 fabricated, 3 design) | 49 | empty | missing from registry (NNfC, MNCF) |
| watanabe2020 | 4 (fabricated) | 27 | org_eth_zurich | none |
| ruiz2021 | 3 (fabricated) | 27 | org_applied_nanotools | none |
| xue2019 | 3 (fabricated) | 28 | empty | none |
| wang2017c | 3 (fabricated) | 27 | empty | none |

## rawat2023 (embedded a-Si strip gratings on 125 nm thin-film SiN, a-Si/SiO2 DBR)

- Fabricated uniform period series `asi_uniform_gc_p940 / p950 / p960`: printed peaks 3.58 / 2.37 / 2.22 dB at
  1561 / 1570 / 1601 nm (loopback_half, measured; "dB/coupler" in the abstract, halving not printed, D167 / D452),
  1-dB bandwidths 39 / 50 / 49 nm, periods. Stack geometry (125 nm SiN, 70 nm a-Si strips, 1.8 um BOX, 1.9 um top
  oxide) on p950 and on the apodized rows.
- `asi_apodized_gc_p890`: 2.12 dB measured incl. taper / waveguide / bend (wavelength 1570 nm inferred from the Fig. 14(a)
  peak); 1.84 dB/coupler `derived` (after the authors deduct a minimum bend + taper excess loss; subtracted value not
  printed, 0.28 dB = 2 x 0.14 dB/90 deg); 1-dB 46 nm from Table 1.
- `asi_apodized_gc_p900` (fabricated, D80e; only simulated values printed): 92.7 % at 1544 nm, -4 deg, N 27, fill factor
  0.55 -> 0.07 (a-Si strip fraction).
- Design rows: uniform 970 nm with DBR (74 % at 1546 nm, 1-dB 85 nm, N 21, fill factor 0.40), 70 nm a-Si without DBR
  (55 %), standalone SiN grating (< 20 %, optimum period 1.17 um).
- `tfsin_bend_r200` (waveguide_platform.bend): 0.14 dB/90 deg at R 200 um, `derived` (difference of measured test
  circuits, Fig. 13; arithmetic not printed), C-L band inferred.
- Not entered: Fig. 12(b) / Fig. 14 angle and period sweeps (curves only); Fig. 2 simulated bend / taper losses (no
  printed values; "taper over 60 um nearly loss-less"); Fig. 6 BOX sweep; Fig. 8 field overlap; dB forms of the
  simulated % values (one form entered; -1.3 / -0.28 dB in notes); Table 1 rows of refs. [5], [15] (rule 3); "no
  additional loss due to the tapers" (no number); grating width (the 17 um broad waveguide is only named in the taper
  study, p.3).
- Conflicts kept as printed with notes: Fig. 12(a) peaks read about 0.3 dB lower than the printed -3.58 / -2.37 /
  -2.22 dB (D417); abstract "-1.7 dB/coupler" optimal uniform design vs 74 % (-1.3 dB) in Sec. 2.2 / Table 1.
- Fab / facility: passive fabrication sentence (p.7), fab empty. Acknowledgment (p.10): "NNfC (National Nano
  fabrication Centre) and MNCF (Micro and Nano Characterisation Facility) at CeNSE, IISc for the facility support":
  facility role, both missing from organizations.csv / org_aliases.csv (no IISc / CeNSE entry either).

## watanabe2020 (coherent few-mode demultiplexer, 2x2 array of perfectly vertical 2D GCs, 220 nm SOI)

- `fm_2dgc_array`: estimated coupling loss 5.2 dB (LP01) / 9.0 dB (LP11) at 1570 nm, `author_estimate`, method
  loss_breakdown (subtracted mode-multiplexer loss 3.1 / 3.0 dB and 0.39 dB/mm propagation of unstated origin);
  estimated-CL 3-dB widths 33 / 31 nm (`author_estimate`, read from the same estimated curves); simulated 44 % / 47 %
  at ~1550 nm (CE = 4 x eta), 3-dB 40 / 39 nm; n_periods 8, etch 70 nm (text) and 200 nm full-etch label (Fig. 2(a)),
  stack, 100 um tapers, vertical fiber.
- `output_gc` (2.7 dB at 1562 nm, author_estimate, origin not stated; 16 GCs at 250 um pitch), `routing_wg`
  (0.39 dB/mm -> 3.9 dB/cm, author_estimate, D256a), `4x4_mmi_hybrid` (simulated excess loss 0.26 dB at 1560 nm;
  Fig. 3(a) labelled Wm 10 / Lm 175 / Wt 1.7 / Lt 40 um).
- Not entered: Fig. 5 fiber-to-fiber loss of the demultiplexer (includes the external CAILabs multiplexer); Fig. 6 MMI
  transmission spectra (include GC and waveguide losses); MDM transmission results (system level); dB forms of the
  simulated % values (-3.6 / -3.3 dB in notes); 2D GC gap g = 0.096 um (no parameter for fiber_chip_coupler); 1x2 LO
  splitters (no values).
- Fab: "We fabricated the mode demultiplexer" (p.5), all authors at IEF, ETH Zurich -> org_eth_zurich (merged ETH rows
  use the parent org). No facility named. SOI wafer vendor not named.

## ruiz2021 (tri-modal FMF vertical coupler, 250 nm SOI)

- `trimodal_fmf_coupler` (grating + 700 um tapers + two mode-selective DCs): 3.0 / 3.6 / 3.4 dB at 1516 / 1515 /
  1512 nm for LP01x / LP11ax / LP11bx (per_coupler, method reference_structure, measured: port powers summed and the
  SMF output-coupler loss discounted, subtracted value not printed, D167 / D448); 3-dB widths 13 nm (LP01x) and 25 nm
  (LP11ax); back reflection <= 4 % -> >= 13.98 dB `derived` (from the measured ripple); FMF MFD 12.1 um
  (`specification`), stack, taper, vertical fiber.
- `bidirectional_grating` (grating block): simulated 3D 2.5 / 3.0 / 2.2 dB and 2D 1.5 / 1.4 dB; 22 x 22 um, 120 nm etch.
- `mode_selective_dc` (mode_converter.mdm_mux): simulated IL 0.02 dB (TE0) / 0.08 dB (TE1), crosstalk > 45 dB,
  3-dB > 100 nm; widths 930 / 450 nm.
- Not entered: MDL 0.6 dB (`mdl_db` allowed only for fiber_interface; registry gap below); LP11bx 3-dB width (not
  printed); ripple 0.2-0.7 dB (no parameter); Table 1 / Fig. 4(b) values of refs. [10], [21]-[24] (rule 3).
- Fab: "fabricated at Applied Nanotools (ANT) rapid fabrication service" (p.5) -> org_applied_nanotools on all three
  rows; process_name empty (no named process; the printed service name is generic).

## xue2019 (low-PDL 2D GC with elliptical-like cells, 220 nm SOI)

- `2dgc_elliptical`: measured PDL < 0.2 dB over 1525-1560 nm, peak CE 4.2 dB at 1530 nm (loopback_half, measured,
  halving not printed), centre wavelength; simulated ~3.4 dB at 1535 nm, PDL 0.2 dB, tolerance PDLs < 0.4 / < 0.5 /
  0.6 dB (E / dL / R2 +/-20 nm, Fig. 4); period 625 nm design and 621 nm SEM, 150 nm etch, stack, 11 x 11 um, 12 deg,
  300 um tapers.
- `2dgc_conventional`: measured PDL 3.05 dB (band maximum) and 4.1 dB peak CE (C band inferred, Fig. 7(a) peak near
  1548 nm); simulated 45 % at 1535 nm and PDL 2.6 dB.
- `2dgc_cell_variants` (population row, D165): measured PDL < 0.9 dB for the three off-optimum R2 / dL variants
  (Fig. 7(b)).
- Not entered: cell radius R2 / R1, rectangle length dL (design and SEM; no parameter), minimum feature size 310 nm,
  fabrication tolerance +/-10 nm (no parameter); Table 1 values of refs. [21], [23], [26], [30]-[32] (rule 3).
- Conflicts: Fig. 7(b) legend labels the conventional GC R1 = 150 nm vs 175 nm in the design (p.2); p.5 compares with
  "the 2.6 dB PDL value of the conventional 2D GC", which is the simulated value (measured 3.05 dB). Both in notes.
- Fab: passive "The structures are fabricated on an SOI wafer" (p.4), fab empty (all authors at WNLO / HUST, D80b).

## wang2017c (perfectly vertical focusing GC on a tilted Si membrane, 340 nm SOI, O band)

- `tilted_membrane_gc_p454`: measured 57 % peak at 1286 nm (loopback_half, measured), centre 1286 nm (derived from
  1.286 um), 1-dB > 28 nm (abstract); simulated 66.2 % (3D, ~1310 nm inferred), 68.7 % (2D at 1.31 um), 1-dB 33 nm,
  back reflections ~1 % (-> ~20 dB, simulated, w-w and f-f); geometry (p 454 nm, fill factor 0.32 from g = 0.68p,
  200 nm teeth, 340 / 140 nm Si, 2 um BOX, 10 um membrane, 30 um taper, 600 nm output, ~60 um length, vertical fiber).
- `tilted_membrane_gc_p474`: measured peak at 1327 nm (derived from 1.327 um); peak CE ~51 % read off Fig. 7(a).
- `tilted_membrane_gc_p454_oxide` (same sample after ~1 um SOG + PECVD oxide): peak ~1320 nm (1286 + ~34 nm, derived),
  CE ~51 % (Fig. 7(b) read), simulated 1360 nm.
- Not entered: membrane tilt 11 deg design / 11.3 deg mean, sigma 0.183 deg (no parameter; registry gap below); peak
  shift rates 6 nm/deg and 2.1 nm/nm (no parameter); upward diffraction > 84 %, 81 % overlap (no parameter);
  "28nm-39nm" measured 1-dB range per device (D159, see judgment 4).
- Fab: passive "was fully fabricated using conventional ..." (p.6), fab empty (authors at SCNU, SYSU, ZJU).

## Judgment calls for the auditor

1. Peak values ("maximum CE") entered without `statistic` and with "spectral peak" in the condition (lit_264 used
   `best` for chen2020b); harmonize either way.
2. Per-coupler values printed from two-GC test structures (rawat2023, xue2019, wang2017c): `loopback_half`, `measured`
   (D167 / D452). rawat2023 1.84 dB is `derived` (authors deduct an unprinted excess loss from the measured 2.12 dB,
   D394 analogue); ruiz2021 per-mode losses stay `measured` with method reference_structure (summing / de-embedding
   described, subtracted SMF-coupler loss not printed, D448); watanabe2020 losses `author_estimate` (subtracted
   multiplexer / propagation terms of unstated origin).
3. watanabe2020 estimated-CL 3-dB widths (33 / 31 nm) marked `author_estimate` like the loss rows, although a constant
   subtraction would not change a width; `measured` is defensible if the subtracted terms are wavelength-flat.
4. wang2017c bandwidth: abstract ">28nm" entered on the 57 % (454 nm) row as `gt` 28; the p.6 range "about
   28nm-39nm" is not split by device (D159). Alternative: notes only.
5. wang2017c oxide-clad measurement as a separate component row (cladding changes the design) rather than a condition
   on the air-clad row.
6. ruiz2021 split into three rows (full coupler measured; grating block and mode-selective DC with their simulated
   values, D396 cross-notes); full coupler classed fiber_chip_coupler.grating, DC mode_converter.mdm_mux.
7. rawat2023 apodized 900 nm row kept `fabricated` (a 900 nm apodized grating is in the measured series, D80e) although
   its only printed values are simulated; uniform 970 nm optimum is `design` (not among the fabricated periods).
8. rawat2023 bend loss 0.14 dB/90 deg `derived` (difference of measured circuits) despite no printed arithmetic (D452
   would give `measured`).
9. xue2019 measured conventional PDL 3.05 dB ("3.05dB between 1525nm and 1560nm") entered
   as a band-maximum value without a qualifier.
10. watanabe2020 Fig. 2(a) "Full-etched: 200nm-deep" label entered as a second etch_depth_nm row
    (`extracted_from_figure`) despite the 220 nm device layer.

## Registry gaps

- `mdl_db` for fiber_chip_coupler: ruiz2021 MDL 0.6 dB (p.2, p.6; LP01x / LP11ax / LP11bx peak spread). Proposed:
  widen `mdl_db` (spread of coupling loss over the guided fiber modes) to fiber_chip_coupler (also mode_converter per
  the D533 note).
- `gap_nm` for fiber_chip_coupler: watanabe2020 gap between the arrayed 2D GCs 0.096 um (p.4). Proposed: allow
  `gap_nm` for fiber_chip_coupler (gap between array elements).
- Membrane / grating tilt angle: wang2017c 11 deg design, 11.3 +/- 0.183 deg measured on 140 nm x 10 um test membranes
  (p.3, p.5 Fig. 5(a)). Proposed `grating_tilt_deg` (fiber_chip_coupler, geometry): tilt of the grating plane to the
  substrate.
- Hole / cell radius of 2D GCs: xue2019 R1 175 nm, R2 140 nm (SEM 143.2 nm) and dL 30 nm (SEM 34.3 nm) (p.2-4).
  Proposed `hole_radius_nm` (fiber_chip_coupler, geometry); dL has no general meaning (notes).
- Minimum feature size: xue2019 310 nm, ruiz2021 100 nm. Proposed `min_feature_nm` (geometry, `*`), low priority.

## Missing organizations

- "NNfC (National Nano fabricaiton Centre)" at CeNSE, IISc - facility (rawat2023 p.10 Acknowledgement; spelling as
  printed).
- "MNCF (Micro and Nano Characterisation Facility)" at CeNSE, IISc - facility (rawat2023 p.10 Acknowledgement).
- Parent "Center for Nano Science and Engineering, Indian Institute of Science" / "Indian Institute of Science" not in
  the registry (affiliation, rawat2023 p.1; header batches handle affiliations).
