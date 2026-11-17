# lit_176 batch report

Distilled 2026-11-16 under the pic-component-distill skill (Contracts v4-v7, DevLog-007 rulings through D615).
Papers: lit:bozzola2015, lit:liu2022e, lit:laere2007, lit:chen2010. Page-1 titles of all four cached texts match their
source rows; no correction / erratum; no garbled text layer flagged. Figure values read from the page renders.

Validation: `uv run --offline python scripts/merge_component_staging.py data/_staging/components/lit_176 --dry-run`
-> +18 components, +110 metrics, 0 errors (the only warning is on an unrelated merged row, ni2025b).

| paper | components | metric rows |
|---|---|---|
| chen2010 | 2 | 18 |
| laere2007 | 4 (3 fabricated, 1 design) | 31 |
| bozzola2015 | 9 (all design) | 56 |
| liu2022e | 3 | 5 |
| total | 18 | 110 |

## chen2010 (apodized shallow-etched GC, 340 nm SOI, CUHK)

- `cmp_lit_chen2010_apodized_gc_340nm`: 1.2 dB per interface at 1533 nm (`loopback_half`, measured: halving not
  shown, D167 / D452, statistic best from "Up to -1.2 dB"); 75.8 % as the authors' printed conversion (derived);
  < 2 dB over 10 samples with varied exposure (n_samples 10, C band inferred); 3-dB bandwidth about 45 nm; centre
  1533 nm; simulated 84 % (peak wavelength about 1549 nm read off the Fig. 3 calculated curve, inferred). Geometry:
  340 nm Si / 2 um BOX (D402), 200 nm etch, period sequence 548-610 nm (set in condition), fill factor 0.60-0.92
  (paper's f = groove fraction 0.08-0.4 converted to tooth fraction, D253), 10.4 um grating width, 500 um taper,
  450 nm waveguide, fiber tilt 10 deg, fiber MFD 10.4 um (specification).
- `cmp_lit_chen2010_uniform_gc_f02`: uniform reference grating of Fig. 3, about 3.4 dB per coupler read off the plot
  (fringes -3.0 to -3.8 dB, +/-0.4 dB, peak near 1536 nm), fill factor 0.8 (1 - f).
- Not entered: simulated directionality ~0.9 (no parameter); measured grating strengths alpha 0.013 / 0.074 / 0.19 /
  0.31 um^-1 of uniform test gratings f = 0.1-0.4 (p.3, Fig. 4; no GC parameter); Fabry-Perot ripple < 0.3 dB
  (indirect back-reflection indicator, not a reflection value); 1.6 dB of ref. [8] and other intro values (cited).
- Fab: empty ("They were fabricated", passive, p.2; D80b). No facility.
- Judgment: the uniform-grating curve is scoped `loopback_half` because the paper describes one two-GC
  characterization for its fabricated couplers and plots both curves on the per-coupler axis; the uniform grating's
  thickness / etch / period are not stated, so only its fill factor is entered.

## laere2007 (GCs with Au bottom mirror in bonded SOI and InP membrane, Ghent University-IMEC / St Andrews)

- `cmp_lit_laere2007_soi_gc_au_mirror`: 69 % measured (`per_coupler`, method reference_structure: output reference GC
  26 % and setup divided out; best-fit Gaussian = fit of own data, D80a), simulated 72 %; geometry 220 nm Si, 50 nm
  etch, 610 nm period, duty 50 % (0.5, D253), 20 periods, BCB buffer 0.84 um as `box_thickness_um` (lower cladding to
  the mirror; derived from 840 nm), former BOX 1 um on top as `cladding_thickness_um`, fiber 10 deg.
- `cmp_lit_laere2007_soi_gc_bonded_nomirror`: reference structure, 26 % (`loopback_half`, identical couplers assumed,
  arithmetic not shown).
- `cmp_lit_laere2007_soi_gc_regular_design`: unbonded starting design on 1 um BOX, simulated 30 % (row_kind design:
  only simulated in this paper; the die was measured after bonding).
- `cmp_lit_laere2007_inp_membrane_gc_au_mirror` (platform inp_membrane): 56 % (`loopback_half`), 1-dB bandwidth about
  45 nm, simulated 78 % (BCB 1.23 um); 300 nm InP, 660 nm period, 70 nm etch, duty 0.5, BCB 1.23 um (design_target).
- Wavelengths: no value is printed with a wavelength; peaks read off Fig. 6 / 8 / 11 and entered with
  `wavelength_inferred` true and the reading uncertainty in notes (ding2014 precedent).
- Not entered: 45 % substrate radiation of the regular design and the 900 nm optimal BOX (no parameter / design
  sweep); intro values 33 %, 40 %, 57 %, 30 % and the 1-dB 40 nm / +/-2 um tolerances (refs. [4]-[8], cited, incl. the
  authors' own ref. [8], D259); Fig. 6 bonded-without-mirror simulated peak (not printed).
- Fab: empty. "We have designed and fabricated" (p.4) names no org and the authors sit at Ghent University-IMEC and
  the University of St Andrews (D154 / D80b). Alcatel-Thales III-V laboratory provided the InP epiwafers (supplier,
  note only). No facility named. Registry orgs exist for Ghent University / imec if the coordinator rules otherwise;
  no org entry found for "University of St Andrews" or "Alcatel-Thales III-V laboratory" (both only author /
  supplier roles here, not fab / facility, so no request is needed).

## bozzola2015 (apodized GC optimisation, pure SOI, design only, Pavia / Tyndall)

- Nine `design` rows (platform soi, 2D FDTD, TE, fiber 10 deg, CE at the 1550 nm target), each with the printed %
  and dB pair (both simulated): 220 nm uniform 53.7 % / 2.7 dB; 220 nm chirp unconstrained 61.6 % / 2.1 dB and
  constrained 59.4 % / 2.26 dB; 220 nm apodized unconstrained 64.65 % / 1.9 dB and constrained (fully etched)
  61.9 % / 2.08 dB; 340 nm apodized from linear chirp 88.2 % / 0.55 dB, from the ref. [5] layout 89.3 % / 0.49 dB,
  DUV-constrained 84.8 % / 0.72 dB; 340 nm uniform 66 %. Geometry as printed (core, etch E, BOX B converted nm -> um
  as derived, period p0, DC 0.5 as tooth fraction).
- 340 nm uniform vs apodized (Fig. 6 comparison): 1-dB bandwidths 41 / 33 nm; reflection losses 13.4 % / 4.2 % entered
  as `back_reflection_db` 8.73 / 13.77 dB (simulated, D83f; benedikovic2015 / croce2026 precedent).
- Judgment: the Fig. 6 apodized design is the red (linear-chirp) one per the Fig. 6 caption and p.10 text, so its
  33 nm and 4.2 % go on `gc_340_apod_chirp`; the p.11 text calls its CE "89 %" while p.9 prints 88.2 % for it (noted;
  88.2 % entered).
- Not entered: the 340 nm fabrication-tolerance statements (etch +/-20 nm -> up to 5 % absolute CE drop, 10 nm
  redshift per 10 nm etch reduction, -1 dB fiber-position window 4.5 um, 11 nm shift for 10 % bar-width change; p.12)
  refer to "the un-constrained apodized design in 340 nm SOI", which cannot be tied to one of the two unconstrained
  340 nm designs (D159; noted on both rows). 420 nm uniform 73.1 % (sentence cites the authors' ref. [21], Fig. 5(a)
  uniform curve attributed to [21]; D259). The unmodified ref. [5] design at 84 % (chen2010's own number, cited).
  Fig. 1 state-of-the-art values (other works). Transmission losses 18.5 % / 7.1 % (no parameter). Fiber offsets
  4.1-6.95 um and trench widths w_min / w_max (no parameter; notes). n_periods not entered: Table 1 lists 24-28
  trenches per design including zero-width entries, so a period count would be an interpretation. Fig. 8 mesh
  convergence (notes only).
- Fab / facility: none (simulation paper).

## liu2022e (polarimeter-assisted Si polarization stabilizer, HUST)

- `cmp_lit_liu2022e_pol_stabilizer` (polarization.compensator): tracking time about 30 us (feed-forward step,
  measured, Fig. 6(e) inset), fiber-to-fiber loss about 9.8 dB (packaged, incl. both SSC couplings), footprint
  2.24e6 um2 (derived from about 2.8 mm x 0.8 mm).
- `cmp_lit_liu2022e_psr` (polarization.psr): PER about 20 dB, author_estimate (stated as the limit of the minimum error
  power, no PSR measurement shown).
- `cmp_lit_liu2022e_tin_tps` (phase_shifter.thermo_optic): response time about 23 us as `rise_time_us`,
  author_estimate (definition and origin not stated).
- Fab: `org_huazhong_university_of_science_and_technology` on all three rows ("We fabricated the proposed device on
  the commercial SOI wafer", p.5; all authors at WNLO, HUST; D72). SOI wafer vendor not named. No facility.
- Not entered: chip power consumption about 144 mW (power_consumption_w not allowed for polarization); TE0 conversion
  efficiency 99 % / normalized error power about -20 dB (no parameter); in-line polarimeter accuracy (RMS 1.26 deg,
  max 4.42 deg, input > -25 dBm for RMS < 5 deg; no parameter, so no polarimeter row); > 40 nm measuring bandwidth by
  recalibration (cited [20], [32]); theoretical tracking speed 21.45 krad/s (estimate, no parameter); Table I
  comparison (other works).
- Judgment: `tracking_time_us` is defined for closed-loop tracking; the 30 us is the open-loop feed-forward step that
  precedes the closed-loop GLD stage (noted on the row).

## Registry gaps (proposed)

1. `power_consumption_w` for `polarization` (liu2022e 144 mW chip average, p.2 / p.7).
2. `conversion_efficiency_pct` for polarization controllers / stabilizers: fraction of power in the target SOP
   (liu2022e 99 %, p.6-7; D551 listed the same gap).
3. `sop_error_deg` for polarimeters: RMS / max SOP deviation on the Poincare sphere vs a reference instrument
   (liu2022e 1.26 / 4.42 deg, p.5 Fig. 5(b)).
4. `directionality_pct` / `substrate_loss_pct` for GCs: share of diffracted power going up / into the substrate
   (chen2010 ~0.9 simulated p.2; laere2007 45 % substrate p.2; bozzola2015 transmission losses 18.5 % / 7.1 % p.11).
5. GC leakage factor `grating_strength_per_um` (alpha, um^-1; distinct from `kappa_per_cm`): chen2010 measured
   0.013-0.31 um^-1 for f = 0.1-0.4 (p.3, Fig. 4).
6. GC design `fiber_offset_um` (fiber-centre position along the grating; bozzola2015 4.1-6.95 um) and
   `min_feature_nm` (lithography constraint, w_min 100 nm).

## Missing orgs

None needed for fab / facility roles in this batch.
