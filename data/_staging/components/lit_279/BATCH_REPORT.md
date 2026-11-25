# lit_279 batch report

Papers: lit:wu2021, lit:wu2022a, lit:zafar2018, lit:zhang2021d, lit:zhang2016a (all Optics Express). Page-1 titles
match the source rows; no correction / erratum; no garbled text layer. Total 22 components / 155 metric rows.
`merge_component_staging.py --dry-run`: +22 components, +155 metrics, 0 errors (two pre-existing warnings on other
batches: cmp_lit_guo2024a_exc02, cmp_lit_ni2025b_pimmwc). verified_on 2026-11-25. Generator script in the session
scratchpad `lit_279/gen.py`. No existing rows for these sources in `data/components/`.

All five papers are polarization devices. Polarizer extinction ratio is stored as `per_db` (wang2014 / chen2022a /
cheng2023 precedent); PBS output-port ratios as `per_db` with the input polarization (dai2012 precedent). "ER > X dB
over a band" is one `per_db` row with `wavelength_nm` / `wavelength_max_nm` (no ER-bandwidth parameter on
polarization).

## lit:wu2021 (1 component / 16 metrics)

Simulation-only design paper (3D FDTD; fabrication flow only proposed, p.10).

- `cmp_lit_wu2021_tm_pass_cmc_bragg_polarizer` (polarization.other, row_kind design, soi_strip): ER 51.83 dB and IL
  0.08 dB at 1550 nm; ER > 30 dB and IL < 0.13 dB over 1521-1582 nm (Fig. 7); tolerance results (pitch +/-10 nm: ER >
  42.6 dB, IL < 0.11 dB; duty +/-30 nm: IL < 0.10 dB; W3 +30 nm: ER ~49.8 dB, IL ~0.09 dB; W4 45-130 nm: ER > 45 dB);
  W1 340 / W2 1000 / W4 60 nm, length 30 um, grating section ~20 um, Si 220 nm.

Not entered: TE back-reflection -12.6 dB at 1550 nm and < -8.1 dB over the span, plus RL bounds of the tolerance
sweeps (registry gap below); period 361.8 nm, duty 1/2, taper L1 5 um, hole-row separation W3 540 nm (no parameter
on polarization); Fig. 11 TE0-TE0 / TE0-TE1 variants (bar chart only); Fig. 5 / Fig. 6 intermediate sweeps; Table 1
other works (rule 3).

Judgment: Fig. 9 / Fig. 10 tolerance values carry wavelength 1550 nm `wavelength_inferred` (sweep wavelength not
restated; Fig. 11 states the centre wavelength for the same quantities).

## lit:wu2022a (2 components / 23 metrics)

- `cmp_lit_wu2022a_tm_pass_coupled_nanowire_polarizer` (polarization.other, fabricated, soi_strip, 16): measured ER
  > 15 dB over 1300-1600 nm, average IL ~1 dB over 1300-1600 nm, IL < 1 dB over 1360-1580 nm (Fig. 11; TM on a
  10-device cascade normalized to straight GC waveguides, method reference_structure, basis measured: per-device
  value printed, division not shown, D167); simulated ER > 21 dB and IL < 1 dB over ~1317-1680 nm (endpoints read off
  the labelled 362.5 nm arrow in Fig. 7(a), +/-5 nm), IL < 3 dB over 1300-1800 nm; w1 500 / w2 100 nm, w5 1.3 um
  (derived), length 13.6 um, L2 ~6.825 um, L1 3.4 um, footprint 17.68 um2 (derived), Si 220 nm, BOX 2 um, SiO2 2.2 um.
- `cmp_lit_wu2022a_swg_trident_splitter` (splitter.other, fabricated, soi, 7): stand-alone SWG trident beam splitter
  used as the mode converter; measured average excess loss < 0.5 dB over 1480-1580 nm, TM (Fig. 4); SWG period 200
  nm, taper 2 um, 100 / 500 nm ends, grating width 1.3 um, Si 220 nm.

Not entered: simulated converter IL < 0.2 dB and the simulated Fig. 4 trace (ref. [26], the co-authors' earlier
design paper; rule 3 / D259); ~449 nm band for ER > 19 dB / IL < 3 dB (band endpoints not stated); TE transmission <
-22 dB (rejection level, not the ER); ~2.5 band-shift rate (unit not defined); Fig. 9 tolerance band widths; periods
200 / ~350 nm, duty 0.5 and separation 730 nm on the polarizer (no parameter on polarization). Table 1 row [25] is
lit:wu2021 (cited, not re-entered here).

Judgment calls: the converter's measured "IL" stored as `excess_loss_db` (1x2 splitter, value below the ideal split,
D43; the paper does not say how the two outputs were combined, noted); class splitter.other rather than
mode_converter (the fabricated test device is a 1-in / 2-out beam splitter, Fig. 4 inset). Fab: devices made "by a
fab providing MPW service" with no name -> fab empty (D80b); no facility.

## lit:zafar2018 (8 components / 59 metrics)

- Fabricated (fab org_astar_ime, "fabricated at the Institute of Microelectronics (Singapore)", p.7): design A
  (Rmin 1 um, 105 deg, N 8), design C (Rmin 1.5 um, 105 deg, N 10) and the three Rmin 1 um / N 8 siblings at theta 30
  / 45 / 90 deg (Fig. 7, Table 1). Each: Table 1 simulated and measured TE loss (min / max as `range`, average as
  `mean`, 1500-1600 nm; measured from 20-cascade structures vs mean of 4 straight references, reference_structure,
  measured as printed), width 500 nm, Si 220 nm, BOX 2 um, cladding 2 um. A and C also: Table 2 ER >= (simulated 29.6
  / 28.4, measured 27.0 / 27.6 dB), footprint 221 / 598.5 um2 (derived from 34 x 6.5 / 63 x 9.5 um); C also measured
  average ER 36.0 dB (abstract, conclusion).
- Design rows: design B (Rmin 1.3 um, not fabricated: IL <= 0.39 dB, ER >= 30.2 dB, footprint 360.8 um2) and two
  constant-radius comparison designs (|R| 2 um N 8: IL up to 2 dB, ER 30 dB; |R| 3 um N 10: ~1.2 dB, 30 dB over
  1530-1600 nm, footprint 910 um2).

Not entered: Table 1 TM losses of the rejected polarization (all five devices, kept in component notes; no
parameter, registry gap below); Table 2 IL maxima (identical to Table 1 max, not duplicated); Rmin / theta / N
(min_bend_radius_um not allowed on polarization); single-bend building block (Rmin 2.5 um / 105 deg: loss ratio ~700,
ER 2 dB, ~15 bends for 30 dB; Fig. 3 parameter study, not a design); 1.5-2.5 dB/cm "typical" Si propagation loss
(generic, not measured); effective width 8.5 um with keep-out; the inverse-taper SSCs (no values).

Judgment calls: ER rows only where printed (Table 2, abstract), not computed from Table 1 TM - TE; the |R| 2 um
constant-radius statements carry 1500-1600 nm inferred (Fig. 5 span; band not stated in the sentence).

## lit:zhang2021d (1 component / 14 metrics)

- `cmp_lit_zhang2021d_tm_pass_multiband_grating_polarizer` (polarization.other, fabricated, soi_strip, fab
  org_applied_nanotools, process_name "NanoSOI"): measured IL <= 1.6 dB (1265-1360 nm) and < 0.6 dB (1500-1630 nm),
  basis derived (authors divide the 20-copy cascade loss by 20, D80a), method reference_structure (back-to-back GC
  pairs); measured PER > 20 dB over 1265-1360 and 1500-1617 nm; simulated PER > 20 dB over 1245-1372 and 1410-1626 nm,
  PER > 7.5 dB and IL < 0.4 dB over 1245-1635 nm; Wa 350 nm, W 1300 nm, length 21.942 um, Si 220 nm, BOX 2 um, top
  oxide 2.2 um.

Not entered: period 318 nm, fill factor 0.675, Nt 25 / N 20 (no parameter on polarization); We 110 nm (set in the
initial sweep, not restated for the final design; notes only); Fig. 2 width-sweep values of intermediate designs;
measured Bragg edge at 1265 nm and 9 nm PER-cutoff gap (notes). CMC Microsystems is thanked only for design tools (no
fab role).

## lit:zhang2016a (10 components / 43 metrics)

- `cmp_lit_zhang2016a_gacc_pbs_n80` (polarization.pbs, soi_strip, air clad): TE-input PER > 30 dB over 1517-1538 nm
  and TM-input PER > 30 dB over 1517-1544 nm, IL < 1 dB for both (Fig. 4; normalized to a grating-coupled straight
  waveguide, per_component / reference_structure); Lc 27.52 um, WA 600 / WB 450 nm, Si 220 nm, BOX 3 um (derived from
  3000 nm).
- Seven fabricated siblings (one row per coupling length / width offset, rule 9): N 70 with width +10 nm (Fig. 5(a)),
  -10 nm (Fig. 5(b)) and nominal (Fig. 6(b)); N 90, 60, 50, 40 (Fig. 6(a), (c)-(e)); PER and IL bounds with their
  wavelength spans as printed (polarization `both` where one value is printed for both polarizations), coupling length.
- `cmp_lit_zhang2016a_te_gc` / `_tm_gc` (fiber_chip_coupler.grating, soi): 7.7 / 8.7 dB per port at the gratings'
  central wavelength (C band inferred, centre not printed; method unspecified), period 630 / 1080 nm, fill factor 0.5
  / 0.48 (derived from %, definition not stated), etch 70 nm, Si 220 nm.

Facility: org_center_for_advanced_electronic_materials_and_devices on all 10 rows (acknowledged "support in device
fabrications", p.8); fab empty (passive fabrication sentences, hu2020 precedent).

Not entered: gap 65 nm, period 344 nm, duty 52 %, corrugation widths 137 / 123 nm, bend radius 18 um, S-bend
offsets (no parameter on polarization; notes); Fig. 7 simulated PER vs thickness / corrugation width (no printed
values); Table 1 other works (rule 3). Judgment: printed Lc 17.02 um for N 50 kept although N x 344 nm = 17.2 um
(conflict noted; other N match). Ref. [25] is the authors' OFC 2016 conference version; this journal paper keeps its
values (D259a).

## Missing fab / facility orgs

None. All named orgs exist: org_astar_ime (zafar2018, fab), org_applied_nanotools (zhang2021d, fab),
org_center_for_advanced_electronic_materials_and_devices (zhang2016a, facility). wu2022a names no MPW fab (p.9).

## Registry gaps (skipped value + locator + proposed definition)

1. `back_reflection_db` on polarization: wu2021 TE reflection -12.6 dB at 1550 nm, < -8.1 dB over the Fig. 7 span
   (p.8 Sec. 4); wu2022a Fig. 7(b) reflection spectra. Proposed: allow back_reflection_db (reflection of the rejected
   or passed polarization back to the input, positive dB below the input, polarization in `polarization`).
2. Loss of the rejected polarization on polarization devices: zafar2018 Table 1 TM loss min / max / avg for five
   devices (p.8). Proposed `rejection_loss_db`: transmission loss of the blocked polarization, positive dB, scope as
   insertion_loss_db; ER stays `per_db`.
3. Geometry on polarization (repeats D439 candidates): period_nm / fill_factor (wu2021 361.8 nm / 0.5; wu2022a ~350 /
   200 nm; zhang2021d 318 nm / 0.675; zhang2016a 344 nm / 52 %), gap_nm (zhang2016a 65 nm), min_bend_radius_um
   (zafar2018 Rmin 1 / 1.3 / 1.5 um; zhang2016a 18 um), taper_length_um (wu2021 5 um), n_periods (zhang2021d Nt 25 /
   N 20; zhang2016a N 40-90).
