# lit_248 batch report

Papers: lit:priyadarshini2024, lit:yao2018, lit:xu2007 (page-1 titles match the source rows). verified_on 2026-11-22.
Totals: 23 components, 198 metric rows. `merge_component_staging.py --dry-run`: +23 / +198, 0 errors (the one
warning is on an already-merged row of another paper, cmp_lit_ni2025b_pimmwc).

## lit:priyadarshini2024 (9 components, 85 metrics)

Apodized-DBR Fabry-Perot pump / ASE filter on 220 nm SOI rib (70 nm etch), IIT Madras in-house process.

- `dbr_cavity_d1` .. `_d4` (resonator.bragg, D539): Table 1 devices D1-D3 (Wm 1.5 um, N 61 / 71 / 81) and D4
  (Wm 1.0 um, N 61). Table 2 resonance wavelength, Q ~17,000 / ~40,000 / ~51,000 and IL ~2.3 / ~7 / ~16 dB
  (p.16); D4 Q ~4000 (p.16) with its resonance ~1540 nm read off Fig. 13(b). D1 also: FWHM ~80 pm (abstract),
  out-of-band extinction > 40 dB over 1525-1575 nm (p.21; ~40 dB abstract), thermo-optic 96 pm/mW, 4.32 nm range at
  46.75 mW (p.18), bistability onset 0.5 mW as `power_handling_dbm` -3.0 lt (derived), simulated Q ~1e5 and design
  resonance 1551.35 nm (p.12), 35.76 um length, SEM W0 437 nm; shared stack geometry on all four.
- `dbr_mirror_n61_wm1p5`, `dbr_mirror_n61_wm1p0` (reflector.bragg, fabricated per D80e as the mirrors of D1 / D4):
  CMT-aided-TMM stopband ~88 / ~81 nm, extinction 64.46 / ~52 dB, kappa_m 0.372 / 0.331 um^-1 (as 3720 / 3310 1/cm,
  simulated, D83f); the measured ~60 nm rejection band on the Wm 1.5 mirror row (cross-note to D1). Grating
  geometry (292 nm period, N, Lg, Wm, 50 % duty cycle; SEM Wm ~1.5 um).
- `dbr_mirror_n101_wm1p5` (design): 120 dB calculated extinction for N = 101 (p.9).
- `d1_microheater` (phase_shifter.thermo_optic, D396 cross-note): rise ~3.67 us, fall ~0.6 us, typical ~1 kOhm,
  heater ~5 um x ~1 um x ~100 nm Ti.
- `grating_coupler`: ~7 dB per coupler, ~30 nm 3-dB width, centred ~1550 nm, all `author_estimate` (origin not
  stated).

Not entered: resonance width ~2.8 nm at ~35 dB down (p.16; no width-at-level parameter for resonators); stopband
red shift 3.44 nm at 46.75 mW (p.18; no reflector tuning parameter); ASE suppression ~40 dB / ~15 dB visible (p.18,
p.21; instrument-limited demo, the device value is the extinction row); simulated field enhancement ~9; series
statement "stopband ~80 nm" for N = 61-101 (p.9, stated once for a family, D254, conflicts with the 88 nm point);
stopband ~60 nm for D1-D3 entered only once (abstract ties it to the ~35 um device); D2 / D3 / D4 mirrors (N = 71 / 81)
have no printed values; heater lateral distance ~2.5 um (p.13) vs ~3 um (Fig. 11(d)), edge vs centre not stated, so
no `heater_offset_um`; TEC stability +/- 0.15 pm (setup).

Orgs: fab `org_indian_institute_of_technology_madras` on all fabricated rows ("we have fabricated devices using our
in-house process technology developed at the Center for NEMS and Nanophotonics (CNNP), IIT Madras", p.13; p.21).
Missing facility org: "Center for NEMS and Nanophotonics (CNNP), IIT Madras" (also printed "Centre for NEMS and
Nanophotonics (CNNP)"), lit:priyadarshini2024 p.13 Sec. 3 and p.21 Sec. 5, role facility (work performed there).
The acknowledgment (MeitY sponsorship of CoE-CPPICS and CNNP) is a program acknowledgement, not used.

## lit:yao2018 (7 components, 44 metrics)

Design-only BPM study of a 1x2 MMI splitter in O-ion-implanted z-cut LiNbO3 with fs-laser-ablated grooves; no
fabrication, no measurement. Seven `splitter.mmi` design rows, one per Table 1 groove tilt angle (0-12 deg), each
with the optimized Lmmi, sidewall angle (90 - theta, derived) and the simulated "insertion loss" for E11y / E12y /
E13y input modes as `excess_loss_db` (total of both outputs). The 8 deg row (main design, Sec. 3.2) adds Wmmi 21 um,
w1 2 um, output pitch 10.7 um (2 x Out_x), 1:1 split, and the tolerance-window loss bounds (< 10 % for Lmmi
-3.6..+3.3 um -> < 0.46 dB, < 20 % for Wmmi +/- 0.2 um -> < 0.97 dB, < 0.65 dB for w2 +/- 0.6 um).

Not entered: E13y leaky-mode loss ~0.1 dB over 500 um (p.4); tolerance windows themselves (no splitter tolerance
parameter; D250); "sub-100 um" MMI length (no design); groove width 3 um (notes; no parameter); implantation index
profile (cited input, ref. [19]). No fab / facility org (design only). Platform `other`.

## lit:xu2007 (7 components, 69 metrics)

SOI photonic-wire (0.26 um Si, 2 um BOX, SU8 2 um) rings coupled by compact 2x2 MMIs, NRC Canada.

- `mmi_2x2_3x9` (stand-alone, test_structure): measured cross-port ratio 43-53 % over 1470-1500 nm and ~64 % at
  1550 nm, read off Fig. 2(b) (+/- 3 pp); geometry 3 x 9 um, D = 1 um.
- `mmi_2x2_3x8p5`: splitting-ratio variation < 15 % over 1470-1500 nm (`coupling_variation` 0.15 lt, derived).
- `mmi_ring_r50`: Q ~6000 (1470-1500 nm, TM), FWHM 0.25 nm at 1470 / 0.5 nm at 1550 nm, extinction ~15 dB and
  ~12 dB (both printed for the same spectrum, D417 note), fiber-to-fiber IL ~11 dB, FSR 1.28 / 1.60 nm at
  1470 / 1570 nm, finesse 5.4.
- `mmi_ring_r20`, `mmi_ring_r5`: Q ~3500 / ~2000, FWHM 0.4 / 0.8 nm, finesse 7.5 / 9.8.
- `mmi45_ring_r50` (4.5 x 20 um MMI): Q ~7000, resonance depth up to ~28 dB, 0.22 nm width label at 1540.6 nm.
- `dc_ring_r50` (reference DC ring, 0.2 um gap, 10 um coupling length): Q max ~22,000 at 1570 nm, ~10,000 and
  FWHM ~0.2 nm near critical coupling.

Not entered: hypothetical lossless maximum Q ~10,000 (p.7, calculation); simulated "close to 50:50 within ~15 nm"
(no number); "10 nm gap change -> 25 nm spectral shift" of the DC (p.4, origin not stated, no parameter); MMI excess
loss (not quantified, p.5); inverse-taper converters (0.15 um tip, geometry only); 18 modes in the MMI (simulated).
Fab empty: "were fabricated on unibond SOI wafers" (p.4) is passive with no org (D80b), all authors NRC Canada;
no facility named.

## Judgment calls

(a) priyadarshini2024: measured ~60 nm rejection band put on the Wm 1.5 um mirror row (stopband is a reflector
parameter) with a cross-note to the D1 cavity; level not stated, entered under `stopband_width_nm` with
"contrast level not stated" (merged precedent rows do the same).
(b) priyadarshini2024: cavity IL (peak minus the device's own passband level) scoped `de_embedded`, method `direct`.
(c) priyadarshini2024: bistability onset 0.5 mW entered as `power_handling_dbm` -3.0 lt (derived).
(d) priyadarshini2024: microheater given its own phase_shifter row (rise / fall / resistance), tuning slope kept
only on the cavity row; rise / fall kept although the sentence says they "closely follow" ref. [28] (measured here,
D80i).
(e) priyadarshini2024: h = 150 nm entered as `slab_thickness_nm` (Fig. 2(c) arrow and 220 - 70 nm etch), although
the legend calls h "rib height".
(f) yao2018: one design row per Table 1 tilt angle (seven rows) rather than only the main 8 deg design (each tilt has
its own optimized Lmmi and loss triple); % tolerance bounds converted to dB as simulated (D83f).
(g) yao2018: platform `other` (bulk-crystal implanted ridge), "total insertion loss" -> `excess_loss_db`.
(h) xu2007: platform `soi` (photonic wire, etch depth not stated; D422); resonator widths in `linewidth_pm`
(nm -> pm, derived) following the merged convention; finesse `derived` (computed by the authors, Eq. (3)).
(i) xu2007: R = 20 / 5 um values given 1470 nm inferred (R = 5 um as 1470-1494 nm, since its Fig. 4(b) spectrum is
at 1482-1494 nm).
(j) xu2007: Fig. 2(b) split-ratio reads entered as `extracted_from_figure` ranges; the 3 x 8.5 um coupler treated
as stand-alone (context of the p.5 paragraph).

## Registry gaps

- Resonance width at a stated depth below the peak (priyadarshini2024 ~2.8 nm at ~35 dB down, p.16): proposed
  `bw_at_level_nm` for resonator / wdm with the level in condition.
- Reflector stopband / Bragg-wavelength shift and centre: `center_wavelength_nm` and `tuning_range_nm` for
  reflector (priyadarshini2024 calculated stopband centre 1560.56 / 1553.34 nm, p.9; stopband shift 3.44 nm at
  46.75 mW, p.18).
- Splitter dimensional tolerance window (yao2018 Lmmi -3.6..+3.3 um for < 10 % loss, Wmmi +/- 0.2 um for < 20 %,
  w2 +/- 0.6 um for < 0.65 dB, p.7): `tol_dimension_um` with the loss criterion in condition (D250 deferred
  tolerances; re-proposed only with these values).
