# lit_322 batch report

Distilled 2026-11-28. Papers: lit:dai2012c, lit:dai2010, lit:dai2011 (Optics Express open-access copies, Dai / Bowers
group, UCSB with Zhejiang University). Result: 13 components, 72 metric rows (dai2010 5 / 28, dai2011 3 / 15,
dai2012c 5 / 29). `merge_component_staging.py data/_staging/components/lit_322 --dry-run`: 0 errors (2 warnings, both
on merged rows of other batches: guo2024a, ni2025b). Helper: scratchpad `lit_322/build.py` (writes both CSVs).

Page-1 titles match the source rows for all three; none is a correction / erratum; `garbled_text_layer` false for
all. Equations and figure-embedded numbers are garbled in the text layer: figure values read on the page renders.

## Own-earlier-work and sibling checks (D259 / D259a / D408)

- dai2012c (15 pages, a research article with a review-style introduction, not a review) cites the group's own
  dai2010 (ref. [27]), dai2011 (ref. [30]) and dai2012 (ref. [35], IEEE PTL MZI-PBS, merged as lit:dai2012). It does
  not reproduce values from them: the "almost 100%" TM0-TE1 conversion of the dai2011 nanowire taper (p.3, "in our
  previous paper") is not entered on dai2012c; the bi-level taper design "used in a MZI-based PBS successfully in our
  previous paper [35]" (p.15) has no value in dai2012c (Fig. 20 spectra are in absolute dBm) and no row, so nothing
  can double-enter cmp_lit_dai2012_bilevel_taper (that taper: 250 nm rib height, only an author_estimate < 0.5 dB).
- dai2011 and dai2010 restate no own earlier values (dai2011 cites the group's AWG / bend / rotator papers only
  as background).
- The dai2012c bi-level TM0-TE1 converter (wco 1.0 um, 400 nm rib SOI) and the dai2011 nanowire taper (220 nm strip,
  SiN cladding) are different designs; each paper's own simulation is entered once on its own source.
- dai2011a (bent-DC PBS, same group) is not in this batch; no overlap with these three papers.

## lit:dai2010 (Opt. Express 18(26) 27404, 2010): 5 components / 28 metrics

Compact broadband TE-pass polarizer: straight ridge between two trenches in 700 nm SOI, shallow etch hr 140 nm.

- 4 fabricated rows (polarization.other, soi_rib), one per ridge width of Fig. 12(c): wco 0.8 / 1.0 / 1.2 / 1.6 um,
  all wtr 2 um, 1 mm, hr 140 nm.
  - wco 1.2 um: per_db 25 dB `measured`, statistic best (printed "as high as 25dB over a 100nm wavelength range",
    abstract p.1 and conclusion p.12), tied to 1.2 um by the text (maximum around wco = 1.2 um, p.10) and the
    Fig. 12(c) point; TE insertion loss 1.5-5 dB from Fig. 12(b), scope de_embedded ("coupling loss is excluded",
    p.10; method not stated).
  - wco 1.0 um: per_db 20.3 dB and TE loss 0-5.5 dB from Fig. 12(a) / (c) (`extracted_from_figure`).
  - wco 0.8 / 1.6 um: per_db 5.5 / 2.3 dB from Fig. 12(c) only.
  - Geometry per row: width (derived from um), length 1 mm (derived), Si 700 nm and hr 140 nm (design_target).
- 1 design row: optimized wco 1.1 um, wtr 3 um, 1 mm: per_db > 64 dB (p.9, Fig. 8; 1550 nm inferred from the Fig. 7
  basis) and > 50 dB over 1450-1650 nm (p.9, Fig. 9), `simulated`.

Not entered:
- TM transmission curves of Fig. 12(a)-(b) (captured by the ER rows); the calculated ER curve of Fig. 12(c)
  (simulated curve for the fabricated widths; peak about 37 dB) and Figs. 2, 5, 7 leakage-loss sweeps (mode-solver
  parameter studies, no design row); "maximal leakage loss close to 120dB/mm" (p.5, a calculated TM0 leakage over a
  sweep, not a component); trench-period formula values 1.51 / 1.39 um (p.7, analysis).
- Design TE loss: only the requirement L_TE < 0.1 dB (p.8-9), no computed value printed.
- "over 60dB" (p.8) for the design: superseded by the more specific > 64 dB on the same design (note).
- Input polarization extinction 40 dB of the setup (p.10): setup value (rule 13).
- Trench width wtr (2 / 3 um): no registry parameter for the trench of a polarizer (in core_material / label).

Fab / facility: fab `org_ucsb` on the 4 fabricated rows (first-person "We use standard processes ... for the
fabrication of the present SOI polarizer", p.9; all four authors print UCSB only; site not printed, same basis as the
merged cmp_lit_dai2012_mzi_pbs). No facility named; acknowledgment is a DARPA contract (p.12). No missing org.

Judgment calls:
- The 25 dB headline is placed on the wco 1.2 um row (text + Fig. 12(c)); the abstract itself names no width.
- Wavelength of the Fig. 12(c) ER points is not printed: the Fig. 12(a)-(b) measurement span 1520-1620 nm is entered
  with `wavelength_inferred: true`. The meaning of the Fig. 12(c) error bars is not stated (noted).
- wco 1.0 um TE loss lower end about 0 dB (curve touches 0 near 1.59-1.60 um) entered as printed on the axis.
- Upper cladding not stated: `cladding` empty.

Registry gaps: none proposed (trench width is design detail; D81 / D250 keep tolerance-type parameters out).

## lit:dai2011 (Opt. Express 19(11) 10940, 2011): 3 components / 15 metrics

Concept / design paper for a PSR (adiabatic TM0-to-TE1 taper + asymmetric DC) on 220 nm SOI nanowires with a Si3N4
upper cladding. No fabrication, no measurement: all rows `row_kind: design`, fab empty.

- cmp_lit_dai2011_psr_ltp1_4um (polarization.psr, soi_strip): per_db > 10 dB over 1490-1570 nm (printed bandwidth
  "more than 70nm for an extinction ratio of 10dB", p.7; edges read off Fig. 7(a), +/-10 nm), length 71 um (Fig. 6
  label; "about 71um"), Si 220 nm, widths w0 0.54 / w3 0.9 / w4 0.405 um (derived).
- cmp_lit_dai2011_psr_ltp1_10um (polarization.psr): longer-taper variant, per_db > 10 dB over 1470-1600 nm (printed
  "more than 130nm", p.9; edges from Fig. 9(a)), Si 220 nm, widths.
- cmp_lit_dai2011_tm0_te1_taper_ltp1_4um (mode_converter.converter, D396 cross-note to the PSR row): TM0-to-TE1
  conversion efficiency 100 % approx (printed "close to 100%", p.6 / abstract; 1550 nm inferred from the DC design
  wavelength, p.7), Ltp2 44 um, widths 0.54 / 0.9 um, Si 220 nm.

Not entered:
- Width-deviation tolerances for ER 10 dB: -10 to +20 nm (Fig. 8(a), p.9) and -40 to +30 nm (Fig. 9(b), p.9): no
  tolerance parameter (D81 / D250 rejected generic tolerances).
- PSR insertion loss / cross-port power (Fig. 7(a) peak about 0.96) and ER at 1550 nm: not printed as numbers; not
  derived from the plot.
- DC coupling-efficiency sweep (Fig. 5) and its gap / Ldc choice (0.15 um, 7.0 um): design curve; gap_nm and
  coupling_length_um are not allowed for the polarization class (geometry in notes).
- Fig. 1 effective-index curves (hybridization near w = 0.76 um): mode-solver analysis.
- Taper of the longer PSR (Ltp1 10 / Ltp2 69 um): no separate row (same "close to 100%" statement, Fig. 3).

Fab / facility: none (design only). Acknowledgment: DARPA contract, thanks for discussions (p.10). No missing org.

Judgment calls:
- ER definition is not printed; the per_db rows use the Fig. 7(a) / 9(a) TM0-input cross / thru ratio (noted).
- Platform `soi_strip` (nanowire, single full etch, SiN upper cladding in `cladding`).
- The taper is entered as its own mode_converter row because its function (TM0-to-TE1 conversion) has a stated
  efficiency, as the merged dai2012 sub-part rows (MMI, bi-level taper).

Registry gaps: none new (tolerance rejected by D81 / D250).

## lit:dai2012c (Opt. Express 20(12) 13425, 2012): 5 components / 29 metrics

Mode conversion (TM0 to higher-order TE) in lateral and bi-level tapers of 400 nm SOI rib waveguides; simulation plus
an experimental observation. All 5 rows are design rows (`simulated` FIMMPROP results); simulation wavelength is
never stated (`band: unspecified` + note on every efficiency row).

- cmp_lit_dai2012c_lateral_taper_tm0_te3_1500um (mode_converter.converter, soi_rib): TM0-to-TE3 > 90 % (p.6, Fig. 5;
  Fig. 5 about 0.95 at 1500 um noted), Ltp 1500 um, widths 2.7 / 2.0 um, Si 400 nm, het 200 nm (0.5H, derived).
- cmp_lit_dai2012c_lateral_taper_short_10um (waveguide_platform.other): TE0 power kept in TE0 99.66 % (TE2 0.26 %),
  p.7; TM0-to-TE3 "about 5% only" in notes.
- cmp_lit_dai2012c_lateral_taper_tm0_te1_215um (mode_converter.converter): TM0-to-TE1 100 % approx ("close 100%",
  p.7, Fig. 8), Ltp 215 um, widths 1.5 / 0.8 um.
- cmp_lit_dai2012c_bilevel_taper_wco1p0_300um (mode_converter.converter, soi): TM0-to-TE1 100 % approx ("close 100%
  ... (e.g., >300um)", p.11, Fig. 15), Ltp 300 um, central rib 1.0 um, side rib 3.0 um at the input.
- cmp_lit_dai2012c_bilevel_taper_wco1p2_100um (waveguide_platform.other, soi): TM0 kept in TM0 about 98 % read off
  Fig. 17(b) at Ltp 100 um (+/-1 %); text "no mode conversion observed" (p.12).

Not entered:
- Fabricated structures (Sec. 2 "Experimental observation", pp.13-15): (a) lateral-taper series (3 -> 1.5 -> 1 um,
  Ltp 100 um, 1 um straight section L1 0-1020 um, het 0.5H): the only numbers are the quasi-FSR of the TM0 / TE1
  two-mode beating vs L1 (Fig. 19(d), about 75 / 52 / 29 / 22 / 15 / 13 nm), which characterize the mode mixing, not a
  performance parameter of the taper (fsr_nm is not allowed for waveguide_platform / mode_converter; no registry gap
  proposed); spectra (Fig. 19(b)-(c)) are in absolute dBm, no loss derivable. (b) Bi-level tapers het 0.6H, wco 1 um
  (Fig. 20): spectra in dBm, "quite smooth", no number. Both: no component row (D49: no performance metric).
- Points on the length sweeps that are not proposed designs: Ltp 22.4 um about 50 % and Ltp 0 about 25 % TM0-to-TE1
  (pp.7-8, Fig. 10), 350 um partial conversion (p.6), wco 0.85 um bi-level curve (Fig. 17(a)); in notes where relevant.
- Effective-index / hybridization analysis (Figs. 2, 12: hybridization widths 0.9-2.55 um, low-loss end-width window
  0.95 < w < 2.35 um for het 0.4H, TM0 leaky below 0.95 um): mode-solver design guidance, no component.
- The dai2011 nanowire taper "almost 100%" restated on p.3 (own earlier work, D259).

Fab / facility (for the record; no fabricated row): "We fabricated some straight waveguides" (p.13) by authors at
Zhejiang University and UCSB (first author both) and thanks to Jon Peters "for fabrication" (p.15; his org is not
printed). Site ambiguous (D154 / D83c), so fab would stay empty. No facility named; acknowledgments are grants (DARPA,
NSFC, 863, Zhejiang provincial grant, Fundamental Research Funds). No missing org.

Judgment calls:
- The 15 pages are a research article (own simulations and own experiment), not a review: the introduction cites
  others but the body reports the authors' own new results, which are entered.
- Tapers designed for TM0-to-TE(n) conversion -> mode_converter.converter with coupling_efficiency_pct (precedent
  chang2018c / akritidis2026); tapers designed to avoid conversion -> waveguide_platform.other (one Si layer;
  cmp_lit_dai2012_bilevel_taper precedent).
- Bi-level rows platform `soi` (shallow side ribs to deeply etched central rib in one layer, as the merged dai2012
  bi-level taper); lateral tapers `soi_rib`.
- Taper end widths entered as two width_nm rows with the end in `condition` (no role-specific parameter for the wide
  end of a non-tip taper); het = 0.5H entered as 200 nm `derived`.

Registry gaps: none proposed.
