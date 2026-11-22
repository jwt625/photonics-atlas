# lit_245 batch report

Distilled 2026-11-22. Papers: lit:faugeron2012, lit:sugg2002, lit:mitsuhara1999, lit:mathur2002, lit:okai1990 (all discrete
InP / InGaAsP laser chips; DFB plus test / comparison lasers). Totals: 16 components, 92 metric rows. Dry run:
`merge_component_staging.py data/_staging/components/lit_245 --dry-run`, 0 errors. No paper stopped on: each cached text
(page images for okai1990) is the listed paper; no correction or erratum.

## faugeron2012 (2 components / 32 metrics)

- `cmp_lit_faugeron2012_dilute_dfb` (laser.dfb, inp, 31 rows): maximum powers 190 / about 180 / 135 / 55 mW at 15 / 25 /
  45 / 75 C, > 30 mW over 15-85 C, 167 / 30 mW at 550 mA (15 / 85 C); T0 50 K; far-field FWHM 12 and 34 deg; series
  resistance 0.95 ohm; thermal resistance 26 K/W; measured kappa 8 /cm; SMSR > 55 dB; around 1550 nm; tuning 8.2 nm
  (450 mA), 9.7 nm (30 mW), 6 nm (100 mW, conclusion, author_estimate); RIN about -170 (0.08-2 GHz), < -161 (0.08-40
  GHz), relaxation-peak levels -161 / -136.5 dB/Hz with peak frequencies 8 / 1.3 GHz, < -155 dB/Hz at 100 mW; linewidth
  270 kHz Lorentzian and 990 kHz Gaussian (200 mA, 25 C), < 500 kHz for 13-115 mW and for 15-65 C; 3 um ridge, 1 mm.
- `cmp_lit_faugeron2012_bulk_q_dfb_ref` (laser.dfb, 1 row): 42 K/W thermal resistance of the ref. [4] design laser,
  measured in this letter.
- Not entered: T1 = 157 K (no parameter); 20 x 40 deg far field of "a comparable design without waveguide" (other
  design); abstract "better than 300 kHz" (same result as 270 kHz); thresholds (not printed; Fig. 1 curves are not
  labelled individually); design confinement factors (notes).
- Conflict noted: the 190 mW maximum at 15 C is not visible in Fig. 1 (traces stop at 550 mA near 165 mW).
- Fab / facility: none stated ("are fabricated using ... process as described in [4]", passive; D80b). Authors at
  Thales Air Systems, III-V Lab and SUPELEC / LMOPS (header batches, not fab).

## sugg2002 (2 components / 13 metrics)

- `cmp_lit_sugg2002_bw_dfb` (laser.dfb, inp, 12 rows): 220 mW at -15 C and 162 mW at 15 C heat sink (single mode);
  threshold 50 mA (15 C); linewidth 750 kHz (73 mW) and 1 MHz (114 mW) at 6 C; RIN <= -165 dB/Hz (instrument floor,
  > 80 mW, > 1 GHz) and RIN peak -130 dB/Hz at about 3 GHz; lasing peaks about 1548.1 / 1551.3 nm read off Fig. 6;
  design kappa about 30 /cm (author_estimate); 3 um ridge, 1 mm.
- `cmp_lit_sugg2002_broad_area_fp` (laser.other, test structure, 1 row): pulsed threshold 305 mA derived from the
  printed 305 A/cm2 x 100 x 1000 um2.
- Not entered: differential quantum efficiencies 33 % / 25 % / 31 % (no parameter); SMSR (not stated; Fig. 6 side
  features about 22-23 dB below the peak are not identified as side modes); Fig. 2 device (207 mW, 43 % DQE, 1.5 mm,
  700 nm active region) and the 326 mW projection: the authors' earlier work (refs. 6-7, D259); Fig. 1 design-space
  curves (simulation, design trade-off only); design index step 0.01.
- Conflicts noted: 73 mW (text) vs 72 mW (Fig. 4 caption); 114 mW (abstract) vs 112 mW at 490 mA (Fig. 5 caption);
  Fig. 6 caption refers to "the device of Fig. 1".
- Fab / facility: none ("were fabricated", passive). Authors at Sensors Unlimited and Sarnoff.

## mitsuhara1999 (4 components / 17 metrics)

- `cmp_lit_mitsuhara1999_dfb_bh_4qw` (laser.dfb, inp, 10 rows): threshold 26 mA (25 C); T0 50 K; 10.5 mW at 200 mA
  (25 C); > 4 mW at 55 C; SMSR 32 dB (50 mA); 2052 nm (derived from 2.052 um); 5 nm thermal tuning (15-55 C); 125 pm/K
  (derived from +0.125 nm/C); 1.5 um BH stripe, 900 um.
- FP test lasers `fp_ridge_2qw`, `fp_ridge_3qw`, `fp_bh_4qw` (laser.other, test structures): peak wavelengths 1997 /
  2034 / 2057 nm (derived from um), 900 um; `fp_bh_4qw` also 480 pm/K (FP mode, Fig. 4).
- Not entered: differential quantum efficiency 22.5 % and the 23.9 / 17.9 / 12.8 % temperature series (no parameter);
  current tuning +0.0025 / -0.002 nm/mA (no parameter; D83g); PL peak (material).
- Fab: `org_ntt` on all 4 rows (first-person "We have fabricated and tested" for the DFB BH lasers, all authors at NTT
  Opto-electronics Laboratories, staff thanked for laser processing). FP rows borderline (see (c)).

## mathur2002 (6 components / 17 metrics)

- FP lasers (laser.other): 1000 um 390 mW at 20 C; 750 um about 350 mW (Fig. 1 read); 500 um slope 0.48 W/A (printed
  mW/mA); lengths.
- `cmp_lit_mathur2002_dfb_1000um` (laser.dfb): > 315 mW; > 150 mW in a lensed SMF; > 65 mW at 90 C / 500 mA; linewidth
  as low as 300 kHz; RIN < -158 dB/Hz (set-up limited); 1000 um.
- `cmp_lit_mathur2002_dfb_500um` (laser.dfb): threshold 25 mA, slope 0.48 W/A, 245 mW at 700 mA, 500 um.
- `cmp_lit_mathur2002_dfb_lensed_smf` (fiber_chip_coupler.other): 53 % coupling efficiency, per_facet, O band inferred.
- Not entered: SMSR ("excellent", no number) and lasing wavelengths (Fig. 3 traces are offset in x and y for display);
  Fig. 2 threshold (not printed); 500 um FP maximum power (trace end ambiguous with its label leader).
- Fab / facility: none ("We have developed" the structure; DFB lasers "were fabricated", passive). Authors at SDL Inc.
  (`org_sdl` exists in the registry; not used, no fab statement).

## okai1990 (2 components / 13 metrics; read from the page images img_p01_1.png / img_p02_1.png)

- `cmp_lit_okai1990_cpm_mqw_dfb` (laser.dfb, inp, 10 rows): linewidth 170 kHz at 25 mW (25 C), extrapolated residual
  150 kHz (author_estimate, D435); threshold 20 mA; slope 0.20 W/A; maximum 26 mW; 1550 nm; SMSR > 45 dB; kappa 35 /cm
  (author_estimate, origin not stated); corrugation pitches 241 / 241.08 nm (Fig. 1 labels); 1200 um.
- `cmp_lit_okai1990_l4_mqw_dfb_400um` (laser.dfb, comparison, 3 rows): minimum linewidth about 730 kHz at about 8 mW
  (Fig. 3) and SMSR about 29 dB at about 28 mW (Fig. 4), both extracted_from_figure; 400 um.
- Not entered: linewidth-power products 400 kHz mW and 4.5 x for the 400 um laser (no parameter); Fig. 2 calculated
  intensity profiles (kappa L 4.0 assumption).
- Fab / facility: none (grating "was fabricated", passive). Authors at the Central Research Laboratory, Hitachi
  (`org_hitachi` exists; not used).

## Missing fab / facility orgs

None needed: the only fab statement (mitsuhara1999) maps to the existing `org_ntt`. No facility statements in any paper.

## Judgment calls

- (a) faugeron2012: separate row for the ref. [4] bulk-quaternary laser, because its 42 K/W is a new measurement in
  this letter (not a cited value); the structure itself is only cited.
- (b) mitsuhara1999: the unidentified "FP laser" of Fig. 4 (+0.48 nm/C) assigned to the 4-QW BH FP row (same 100 mA,
  about 2057 nm at 25 C, text compares with the 4-well gain peak); D159 would drop it if the auditor finds the identity
  insufficient.
- (c) mitsuhara1999: `org_ntt` also on the three FP test lasers (D84b borderline: single-org lab, staff thanked for laser
  processing; the first-person sentence names only the DFB BH lasers).
- (d) sugg2002: broad-area test laser threshold 305 mA derived from the printed current density x contact area (D431
  precedent); drop the row if threshold current density should wait for its own parameter.
- (e) sugg2002 RIN "instrument-limited to -165 dB/Hz" entered with qualifier `le`; mathur2002 "lower than -158 dB/Hz ...
  limited by the measurement set-up" with `lt` as printed.
- (f) faugeron2012 Gaussian 990 kHz entered in linewidth_hz next to the 270 kHz Lorentzian (fit type in condition); the
  conclusion's 6 nm tuning at 100 mW as author_estimate (no data shown).
- (g) Laser temperatures: heat-sink temperatures entered in temperature_k where the paper reports heat-sink values
  (sugg2002, mitsuhara1999), chip temperatures for faugeron2012, as printed.
- (h) mathur2002: lensed-fiber coupling as a fiber_chip_coupler.other row (53 %, per_facet, measured; platform empty);
  the fiber-coupled > 150 mW also on the DFB row with ref_plane fiber.
- (i) Laser performance rows carry no band (no wavelength condition required for laser parameters); only the coupler
  row has an inferred O band.

## Registry gaps (skipped values)

- differential (external) quantum efficiency in %: sugg2002 33 / 25 / 31 % (p.3 Sec. IV), mitsuhara1999 22.5 % and
  23.9 / 17.9 / 12.8 % (p.2 Sec. III). Proposed `differential_quantum_efficiency_pct` (laser; per facet or total and
  current range in condition). Already listed as a gap in DevLog-007.
- characteristic temperature of the slope efficiency T1: faugeron2012 157 K (p.2 Sec. III). Proposed
  `slope_characteristic_temperature_k` (laser).
- current tuning rate in pm/mA: mitsuhara1999 +2.5 / -2.0 pm/mA (p.2 Sec. III). Proposed
  `current_tuning_pm_per_ma` (laser; static, distinct from FM efficiency per D83g).
- linewidth-power product in kHz mW: okai1990 400 kHz mW (p.1-2). Proposed `linewidth_power_product_khz_mw` (laser).
- threshold current density in A/cm2: sugg2002 305 A/cm2 (p.3; entered as derived threshold_ma). Already a D431
  candidate.

## Registry notes

- lit:sugg2002 registry year 2002; the proceedings page header prints 0-7803-6320-5/00 and the DOI is iciprm.2000 (IPRM
  2000).
- lit:mathur2002 registry year 2002; the page footer prints 0-7803-4223-2/98 and the DOI is islc.1998 (ISLC 1998).
