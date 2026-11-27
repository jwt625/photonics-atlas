# lit_299 batch report

Batch lit_299 (DevLog-007 D792, open-access night 1): lit:xue2015, lit:dong2025, lit:suh2016. Distilled 2026-11-27
(verified_on). Totals: 13 components, 44 metric rows. Validation: `merge_component_staging.py
data/_staging/components/lit_299 --dry-run` -> +13 components, +44 metrics, errors 0 (the two warnings it prints are on
merged guo2024a / ni2025b rows, not this batch).

Page-1 title check: dong2025 matches its source row (Optica 12(8) 2025, "Sub-hertz-linewidth hybrid-integrated laser for
isolator-free silicon photonics"). suh2016 is arXiv 1607.08222v1 "Microresonator Soliton Dual-Comb Spectroscopy" (same
title as the Science paper). xue2015 is arXiv 1404.2865, titled "Mode interaction aided excitation of dark solitons in
microresonators constructed of normal dispersion waveguides" (the preprint title of the Nature Photonics paper "Mode-locked
dark pulse Kerr combs in normal-dispersion microresonators"; same authors, same devices). Both preprints: values from the
preprint only, journal versions unread (noted on every component). None is a correction or erratum.
xue2015 `garbled_text_layer`: equations and exponents are garbled across the text layer (not only the flagged pp.19 / 24);
the two Q values were read from the page renders (p.2 `figures/page_02.png`; p.5 rendered from `source.pdf` into the
scratch folder, no `page_05.png` exists), all other values are from clean prose.

## lit:xue2015 (dark-pulse Kerr combs in normal-dispersion SiN microrings): 6 components, 31 metrics

| component | class | metrics |
|---|---|---|
| cmp_lit_xue2015_ring_a_heater | resonator.ring | 11: FSR 231.3 GHz, loaded width 250 MHz, Q_L 7.7e5, width ~2 pm FWHM (all at the ~1548.4 nm comb mode, p.2-3); R 100 um, 2 um x 550 nm (width derived), bus 1 um (derived), gap 300 nm, BOX 3 um, LTO 3.5 um (p.7 Methods) |
| cmp_lit_xue2015_ring_a_microheater | phase_shifter.thermo_optic | 4: 291 ohm; 0.82 / 0.79 pm/mW (pumped / second mode family; printed nm/W, derived D256); Au 300 nm (Cr 5 nm) |
| cmp_lit_xue2015_ring_a_comb | laser.comb | 2: comb tuning range 1.4 nm (1549-1550.4 nm pump, derived); simulated dark-pulse width ~1.1 ps (Fig. S10) |
| cmp_lit_xue2015_ring_a_facet | fiber_chip_coupler.edge | 1: ~3 dB per facet (p.2, measured per D167, method unspecified, 1549.3 nm inferred) |
| cmp_lit_xue2015_ring_b_drop | resonator.ring | 8: Q_L 8.6e5 (C band inferred); R 100 um, 2 um x 550 nm, bus 1 um, gap 500 nm, BOX / LTO |
| cmp_lit_xue2015_ring_b_comb | laser.comb | 2: dark-pulse cross-correlation width ~700 fs measured (1-FSR and 2-FSR combs), ~800 fs simulated |

Not entered:
- Dispersion beta2 = 190.7 +/- 8.4 ps2/km (ring A, p.2) and 186.9 +/- 7.3 ps2/km (ring B, p.5), D2 ~ -2pi x 10 MHz: no
  dispersion parameter (D81 / D250 rejected dispersion).
- Ring A line-by-line shaped pulse (~318 fs autocorrelation, "~220 fs pulse width", 21 lines shaped to a Gaussian,
  p.4): a property of the external pulse shaper output, kept in the comb-row notes rather than as `pulse_width_fs`
  (judgment call; an auditor may prefer a `pulse_width_fs` row with that condition, D84c style).
- Comb line spacing / repetition rate: no comb spacing is printed; ring A only has the mode FSR (231.3 GHz, entered on the
  ring row); ring B's FSR is not printed. Pump powers (1.7 W off-chip, ~1 W, 0.6 W, 0.8 W) have no parameter (no
  thresholds are reported); they are in conditions / notes.
- Cavity parameters used in the simulations and the pump correction (round-trip loss 3.10e-3 and coupling 1.93e-3 for
  ring B, p.8; 3.3978e-3 / 5.3613e-3 for ring A, p.24; symbols garbled): model inputs, no registry parameter; Q_i not
  printed.
- Differential thermal shift of the two mode families (~37 pm per 1 nm, p.3), primary-comb pinning (2.76 THz pump shift,
  <= 15 GHz sideband variation, p.3), reconstruction power fractions (82 % / 91 % / 99.9 %), heater voltages: not
  component performance parameters.
- Supplement L-L simulations of generic normalized cases (Figs. S3-S5, S11): no device.

Judgment calls:
- Ring B "fabricated with both through port and drop port [41]" cites the authors' 2013 drop-port paper; the Q and
  dispersion are presented as this paper's measurements (Fig. 3b), so entered (D259 not triggered). Flag for the audit.
- The Methods sentence "The radius of the SiN microring is 100 um. The cross-section ... 2 um X 550 nm. The width of the
  bus waveguide is 1 um" is general (both rings); p.5 states R 100 um and "nominally the same dimensions" for ring B, so
  geometry is entered on both rings.
- Ring A Q_L 7.7e5 entered as measured (the paper's conversion of its measured 250 MHz width, printed); the 2 pm FWHM is
  the same resonance in wavelength units (entered as printed, approx).
- Facet loss "around 3 dB" per facet entered as `measured` per D167 (directly stated, no arithmetic); an auditor applying
  D418 would make it author_estimate.

Fab / facility orgs: fab `org_purdue_university` on all rows (author contributions "Y.X. fabricated the microring";
all authors at Purdue, D72 / D395). Facility empty: Birck Nanotechnology Center appears only as an affiliation
(p.1), not as a place where the work was performed (registry has `org_birck_nanotechnology_center`). Missing orgs: none.

Registry gaps: dispersion beta2 / D2 (rejected D81, re-listed only as a skipped value: 190.7 and 186.9 ps2/km, p.2 / p.5).

## lit:dong2025 (sub-hertz delayed-DBR hybrid laser, isolator-free): 5 components, 11 metrics

| component | class | metrics |
|---|---|---|
| cmp_lit_dong2025_sil_dbr_4m | laser.sil | 6: Lorentzian linewidth 0.45 Hz best; 0.45-10 Hz across the -3 dB locking band; SMSR 73 dB at 215 mA; mode-hop-free current tuning 0.5 nm (50-300 mA, derived); fiber-coupled power ~0.43 mW at 300 mA (Fig. 2(b), extracted); DBR period 600 nm |
| cmp_lit_dong2025_sin_spiral_4m | waveguide_platform.straight | 2: 0.0017 dB/cm (printed -0.17 dB/m, author_estimate: budget input, origin not stated); length 4 m |
| cmp_lit_dong2025_commercial_dfb | laser.dfb | 1: > 70 mW at 1558 nm (author_estimate: datasheet vs measured not stated) |
| cmp_lit_dong2025_het_qw_dfb | laser.heterogeneous | 1: Lorentzian linewidth 3 Hz under optimal external feedback (16 m fiber + back-reflector loop), 2x threshold |
| cmp_lit_dong2025_het_edbr | laser.heterogeneous | 2: free-running linewidth 12 kHz (derived, kHz -> Hz); Lorentzian 9.5 Hz under feedback stabilization, 3x threshold |

Not entered:
- DBR -3 dB reflection bandwidth 25.7 GHz around 1558 nm and external-cavity Q 5700 (design values, p.2 Sec. 2): no
  frequency-width or Q parameter for `reflector` (registry gap below); the DBR itself (3.179 mm, 600 nm period, kappa L
  ~ 1) is therefore not a row (geometry only, rule 9); its period is on the laser row, length and kappa L in notes. The
  two printed numbers are not consistent with Q = lambda / delta-lambda (25.7 GHz ~ 0.21 nm gives ~7500), so no
  conversion was attempted.
- Noise reduction factors 51.3 dB (4 m) and 38.5 dB (0.7 m) over 1 kHz-10 MHz (p.3), NRF 43.8 / 31.1 / 41 dB, and the
  theoretical 51 / 58 / 65 / 55 dB values: no NRF parameter.
- Feedback tolerance (stable to -11.8 dB external feedback, sub-hertz at -8.1 dB, p.5; critical feedback -24 dB of the
  heterogeneous DFB, -33 dB for commercial QW lasers from the supplement; feedback regime boundaries): feedback tolerance
  stays out of the registry (D77 / D81 / D250).
- Linewidth enhancement factor 2.3 (heterogeneous DFB, p.5): no parameter.
- Estimated laser-to-external-cavity coupling efficiency ~-34 dB (p.4): a composite budget (chip-to-chip coupling,
  spiral loss, ~3 dB directional coupler), not separable into a chip_chip_coupler or splitter value; the ~3 dB
  directional coupler is a nominal design part with no value of its own, not a row.
- The 0.7 m spiral design (Fig. 2(c), (g)): only an NRF is reported, no registry parameter -> not a row.
- Fiber back-reflector (BKR) locking with 15.8 m fiber (NRF 41 dB measured, p.6): fiber external cavity of the same pump
  laser, no chip component.
- 30 GHz MRR with Q 50 million (Fig. 4(c)): data "reported in Ref. [8]" (Xiang et al. 2023, co-author W. Jin) -> D259,
  not entered; MRR feedback tolerances -14 / -6.9 dB from ref. [8] likewise.
- E-DBR design (20 mm grating, kappa L = 1.75) cited from ref. [29]: rule 3; DFB free-running linewidth is printed only
  as "7.7 dB" above 12 kHz (not computed).
- Calculated linewidth projections (100 mHz level, < 100 mHz at 58 dB NRF; Fig. 2(e), Fig. 4(a)-(b), (d)-(e)).

Judgment calls:
- Class `laser.sil`: the paper says "external-cavity locked (ECL) laser" and "our SIL-DBR laser"; a free-running DFB
  locked by broadband delayed-DBR feedback; `laser.ecl` would also be defensible. Platform `other` (hybrid DFB + Si3N4;
  siddharth2024 E-DBR spiral SIL and tang2021 precedent).
- Sample identity: Sec. 3 figures (Fig. 2(b), (d), (f)) say "the ECL laser" without naming the delay length; the paper
  defines its laser by the 4 m spiral (p.2) and shows the 0.7 m design only in Fig. 2(g), so the values are on the 4 m
  row (noted). An auditor applying D159 strictly would move them to notes.
- Text vs figure (D417): tuning "1558 to 1558.5 nm" vs Fig. 2(b) ending near 1558.4 nm; linewidth range "0.45 to 10 Hz"
  vs Fig. 2(f) squares up to ~30 Hz at the band edges. Printed values kept, readings in notes.
- The heterogeneous DFB (3 Hz) and E-DBR (9.5 Hz) linewidths are with a lab fiber feedback loop (16 m fiber + BKR,
  Fig. 3(d) / (f) legends); entered with that condition (chip lasers, D80f excludes only fiber lasers / amplifiers).

Fab / facility orgs: no fabrication statement for any part -> fab empty everywhere ("homemade" heterogeneous DFB does not
name an org; authors at UCSB, KAUST, Universite Laval, Sandia). Missing org (facility, not entered, borderline): "Center
for Integrated Nanotechnologies, an Office of Science User Facility operated by the U.S. Department of Energy (DOE)
Office of Science", p.8 Acknowledgment, inside the Sandia management boilerplate ("... and in part by the Center for
Integrated Nanotechnologies ..."); no statement that work was performed there; not in `organizations.csv` /
`org_aliases.csv`.

Registry gaps:
- `bw_3db_ghz` (and a Q parameter) for `reflector`: skipped DBR -3 dB reflection bandwidth 25.7 GHz around 1558 nm and
  external-cavity Q 5700 (p.2 Sec. 2, design). Proposed: widen `bw_3db_ghz` to reflector ("3-dB reflection band in
  frequency").
- Noise reduction factor (`noise_reduction_db`, laser): skipped 51.3 / 38.5 / 43.8 / 31.1 dB (p.3, p.5). Proposed
  definition: "frequency-noise suppression of a locked laser relative to free running, dB, offset range in condition".
- Feedback tolerance / critical feedback level (laser): -8.1 / -11.8 / -24 dB (p.5); rejected in D77 / D81 / D250, listed
  only as skipped values.

## lit:suh2016 (microresonator soliton dual-comb spectroscopy): 2 components, 4 metrics

| component | class | metrics |
|---|---|---|
| cmp_lit_suh2016_wedge_disk_3mm | resonator.disk | 2: unloaded Q > 3e8 (both disks, author_estimate D403, C band inferred); radius 1500 um (3 mm diameter, derived) |
| cmp_lit_suh2016_dual_soliton_comb | laser.comb | 2: repetition rates 21.9842 GHz (soliton I) and 21.9815 GHz (soliton II), Fig. 2(d)-(e) legends |

Not entered:
- Repetition-rate difference 2.6 MHz (386 ns interferogram period, p.4): no parameter; the legends differ by 2.7 MHz
  (noted, D417). "< 100 kHz" matched disks: no data shown.
- Spectral spans (soliton spectra over 60 nm; dual-comb span 1535-1567 nm, "over 30 nm", 4 THz in 500 MHz): no comb-span
  parameter (D81). Pump-to-disk assignment of 1549.736 / 1549.916 nm is not stated (both in notes).
- Interferogram SNR > 30 dB, RF comb-line FWHM < 50 kHz (set by the pump lasers' mutual coherence), rep-rate tone SNR
  > 75 dB, absorption residual sigma 0.0254: system / spectroscopy metrics, not component parameters.
- Tapered-fiber couplers: no value reported, not a row. Non-soliton 2.4 GHz combs (ref. 23) cited: rule 3.

Judgment calls: one disk row for the two disks of the same design (the Q statement covers both; the rep rates differ only
through etch time) and one dual-comb row with one repetition rate per soliton (dutt2018 precedent). Silica wedge disks on
a Si chip are chip-scale (lee2012 precedent; D411 not triggered).

Fab / facility orgs: fab `org_caltech` (author contributions "KYY fabricated devices"; all authors at Caltech). Facility
empty: the Kavli Nanoscience Institute is named only in the support list beside DARPA and NASA (D83e; yang2018a ruling in
D611). Missing orgs: none. Registry gaps: none new (comb span rejected D81).
