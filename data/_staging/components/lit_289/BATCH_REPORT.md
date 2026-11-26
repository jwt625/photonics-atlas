# lit_289 batch report

Distilled 2026-11-26. Papers: lit:blumenthal2018, lit:sacher2018, lit:pfeiffer2018a, lit:masood2013 (reference-graph
batch C, D780; two Proc. IEEE reviews, one JSTQE invited paper, one Group IV Photonics conference paper). Page-1 titles
match the source rows; no correction / erratum; no garbled text layer. Total 23 components / 108 metric rows.
`merge_component_staging.py --dry-run`: 0 errors (2 warnings belong to other batches: guo2024a, ni2025b).

Rule applied throughout (rules 1 and 3, D259 / D259a / D408, D780): values quoted from other works or from the authors'
earlier papers (reference numbers, "reported in", figures marked "reprinted / taken / adapted from [N]") are not
entered; only results the paper presents as its own new work are.

Fab / facility: fab org_imec on the 8 masood2013 rows, org_epfl on the 4 pfeiffer2018a rows; sacher2018 rows have fab
empty (no fabricating org named for the platforms). No facility_org_ids anywhere (none named).

## lit:blumenthal2018 (0 components / 0 metrics)

Review ("This review paper covers the history ... and a survey of worldwide research", p.1). Every device value is
credited to a cited work, and every figure is reprinted from or credited to a cited work (Figs. 2-20; Fig. 1
summarizes published data, refs. [13]-[15]); Tables 1-2 are qualitative with references. 0 rows.

- Not entered: e.g. 0.045 dB/m spiral (ref. [35]), 80 dB ER / < 1.3 dB third-order CROW filter (ref. [14]), 0.78 dB/m
  coil with 0.0156 dB/crossing (ref. [97]), 12.35 ns / 0.85 ns delay (ref. [99]), Q 42 million / 0.3 dB/m (ref. [57]),
  13 kHz / < 300 Hz hybrid lasers (refs. [82], [83]); all cited (rule 3, D259). The unreferenced mode-field-area
  sentence (about 28 um2 for a 40 nm core, about 4.5 um2 for a 175 nm core, p.6) describes generic core designs, not a
  component the paper characterizes: not entered.

## lit:sacher2018 (11 components / 47 metrics)

Review of the authors' trilayer SiN-SiN-Si platforms "with additional details" (p.1). Figure-level attribution is
explicit (Fig. 1(b),(c), 2, 4, 5(a),(b),(d), 11, 12, 13 reprinted / taken from refs. [20], [39], [40]; Fig. 3(a) adapted
from [20]; FEOL panels of Fig. 3(b), (c), (e) reprinted). Entered only what is not so attributed:

- BEOL platform (O-band, PECVD SiN): `beol_trans_si_sin1` (simulated < 110 mdB, 1260-1360 nm), `beol_trans_sin1_sin2`
  (simulated < 30 mdB), `beol_crossing` (simulated overpass < 7 mdB, underpass < 0.06 mdB) from the unattributed BEOL
  panels of Fig. 3(b), (d); `beol_gc_bilevel` (SiN-on-SiN TE GC: measured 3.5 dB at 1320 nm, 1-dB BW 53 nm; simulated
  2.1 dB at 1313 nm, 76 nm; 19 deg fiber, 450 nm SiN layers; Table 2 "this work"); `beol_gc_trilevel` (polarization-
  independent SiN-SiN-Si GC: measured TE / TM 5.6 / 5.5 dB at 1305 nm, 1-dB BW 47 / > 100 nm, PDL < 0.5 dB over 44 nm
  and < 1 dB over 80 nm; simulated 2.3 / 2.0 dB, 37 / 65 nm, PDL bandwidths 25 / 67 nm; 14 periods, 34 deg fiber,
  450 nm SiN, 65 nm Si slab, 2 um BOX; Table 2 "this work"); `beol_tin_heater` (TiN heater on a Si strip MZI, P_pi
  14 mW, 213 um).
- FEOL platform, new O-band data (Fig. 6, not marked reprinted; lit:sacher2017 = ref. [20] holds only C-band rows):
  `feol_trans_si_sin1` 302 mdB and `feol_trans_sin1_sin2` 25 mdB at 1310 nm; `feol_trans_trilayer` < 560 mdB over
  1262-1360 nm; `feol_crossing_w0p9` (Fig. 6(b) read 0.27-0.51 mdB, crosstalk < -53 dB) and `feol_crossing_w1p5`
  (Fig. 6(b) read 0.11-0.26 mdB).
- Not entered: PECVD / LPCVD SiN waveguide losses ("As reported in [32]", p.3); XTEM thicknesses (Fig. 2, reprinted from
  [20]); FEOL simulated transitions and crossings (Fig. 3(b) FEOL, 3(e), reprinted from [20]); BEOL measured crossings
  (< 3.4 / < 3.1 mdB, < -52 / < -58 dB; Fig. 4 "as taken from [39]"); FEOL C-band transitions (< 107 / < 69 / < 150 mdB,
  Fig. 5(a)), overpass < 2.6 mdB and crosstalk < -56 dB (Fig. 5(b), (d) reprinted from [20]; Table 1 lists them under
  "FEOL Platform [20]"); Table 2 GCs of refs. [43], [32], [37]; all comparison values of other groups (refs. [44], [46],
  [48], [54], [55], [65], [66], [67]); U-shaped PN modulators (EO atlas scope, rule 2, and reviewed from ref. [40]:
  Figs. 11-13 taken / reprinted from [40]); Ge PD (0.6-0.85 A/W, 2 uA at -2 V, about 29 GHz; Sec. IV opens "Here we
  briefly review the performance of modulators and PDs ... [39]"); Fig. 3(a) taper lengths and tip widths (adapted from
  [20], D259a); 15 um trench width (no parameter, in notes); the FEOL O-band overpass bound "< 0.6 mdB with a 90 %
  confidence interval" (does not say which SiN2 width; D159, notes on both crossing rows).
- Judgment calls for the auditor:
  1. BEOL measured transition losses 0.13 dB (Si-SiN1) and about 2.5 dB (SiN1-SiN2) at 1310 nm (p.5) not entered: the
     2.5 dB sentence cites [39] (D80i), both sit in the BEOL measurement paragraph with Fig. 4 "taken from [39]", and
     Table 1 lists them under "BEOL Platform (O band) [39], [40]". The 0.13 dB sentence itself has no citation; if the
     auditor reads D408 literally, it can be added to `beol_trans_si_sin1` (measured, 1310 nm, cutback).
  2. TiN heater P_pi = 14 mW entered although Table 1 lists it under the same "[39], [40]" header: that header also
     covers the two GCs that Table 2 marks "this work", Sec. III.C and Fig. 10 carry no citation (D408).
  3. Ge PD values left out on the Sec. IV "briefly review ... [39]" sentence although Fig. 14 is not marked reprinted;
     the auditor may rule them in (photodetector.vertical, IME MPW fab, see org note below).
  4. BEOL simulated rows (Fig. 3(b), (d) BEOL panels) entered as `fabricated` rows with simulated values only (D80e),
     their measured values being out under call 1 / D259a.
  5. GC peak efficiencies entered as insertion_loss_db `per_coupler`, method `unspecified` (isolation not stated).
  6. PDL bandwidths entered as `pdl_db` < 0.5 / < 1 dB with the bandwidth in `condition`, band o_band inferred.
  7. Platforms: SiN1-SiN2 transitions and the bilevel SiN-on-SiN GC `sin` (both layers SiN; lin2021 / sacher2017
     precedent); Si-SiN1, trilayer transitions, crossings and the trilevel GC `si_sin_multilayer`; TiN heater `soi`
     (MZI in Si strip waveguides).
- Orgs: no fab org named for the platforms (p.2 passive "were fabricated on 200-mm diameter SOI wafers"). IME (A*STAR
  Institute of Microelectronics, `org_astar_ime`) is named only for the Ge PD ("fabricated using the standard growth
  and patterning process in the IME multiproject wafer shuttle service", p.11), which is not entered.

## lit:pfeiffer2018a (4 components / 37 metrics)

Invited paper; the Damascene process discussion and the loss analysis (Figs. 9-11) are presented as the authors' own
work in this paper (no attribution to an earlier paper; the companion arXiv work, ref. [50], is cited only for the AFM
roughness).

- `ring_r230_gap950` (Fig. 9 device, R 230 um, 0.87 x 2 um, gap 950 nm): loaded linewidth 45 MHz and Q 4.1 x 10^6
  (measured, Lorentzian fit), kappa_0/2pi 31.3 MHz (measured; regime fixed by the gap series, D403 / D465), Q0 about
  6 x 10^6 (derived), 5.5 dB/m = 0.055 dB/cm (author_estimate, n_e not stated, D76), splitting 63 MHz (0.063 GHz,
  derived), FSR 100 GHz (nominal), geometry.
- `ring_r230_gap_series` (Fig. 10, gaps 575-950 nm, D165 family row): lowest mean kappa_0/2pi about 40 MHz and 6.7 dB/m
  (0.067 dB/cm, author_estimate), per-device means read 41-67 MHz, geometry.
- `ring_r23_reflow` / `ring_r23_noreflow` (Fig. 11, 1-THz FSR, R 23 um, 0.85 x 1.5 um): "around 100 MHz" intrinsic
  linewidth after reflow (text), Fig. 11 reads of kappa_0 (reflow TE 88-101, TM 96-117; no reflow TE 107-130, TM
  116-165 MHz) and backscatter coupling rate kappa_c (reflow TE 67-108, TM 186-242; no reflow TE 81-156, TM 292-456 MHz,
  entered as mode_splitting_ghz), nominal FSR, geometry.
- Not entered: 3 dB per facet of 3D inverse tapers ("typical samples ... [26], [42]", cited); AFM roughness 1.2 nm rms /
  155 nm (ref. [50]); 0.1 dB/m, 0.2 dB/km and other literature values (cited); filler-pattern crack-free deposition up
  to 1.52 um, ARDE fit (a = 1.61 um, b = 0.22 um, c = 1.28), 200 nm trench -> 300 nm high waveguide, 85 / about 80 deg
  sidewall angles, CMP top roughness about 0.3 nm RMS, wafer bow about 90 um, largest waveguide 1.75 x 1.425 um (process
  results without a component performance metric; sidewall angles in notes because they are process-level SEM
  statements, not measured on the rings); Fig. 10 model line kappa_0/2pi = 60 MHz (model curve); TM FSR about 10 GHz
  below TE (notes).
- Judgment calls: (1) the caption's "lowest mean ~40 MHz" stays on the family row because the 800 nm and 950 nm means
  read about 43 and 41 MHz (not separable, D159 / D165); (2) the Fig. 9 ring (gap 950 nm) kept as its own row, not
  merged into the family (not stated to be one of the Fig. 10 devices); (3) Fig. 9 resonance band `l_band` inferred
  from the Fig. 9(b) markers (about 185.9 / 187.7 THz); (4) Fig. 11 kappa_c entered as mode_splitting_ghz (the paper
  calls the Fig. 9(d) kappa_c the "splitting rate"); (5) fab org_epfl from first-person process sentences with all
  authors at EPFL at the time (D80b); no CMi acknowledgment, so facility empty (unlike lit:pfeiffer2018); (6) the Fig.
  10 / Fig. 11 polarization: Fig. 10 entered as quasi-TE by the Fig. 9 description of the same ring type.

## lit:masood2013 (8 components / 24 metrics)

Own one-to-one comparison of heaters in one platform (2-page conference paper). Four heater types (doped Si beside the
waveguide, silicide line, W line above, doped waveguide) x without / with thermal insulation (trenches + substrate
undercut) = 8 `phase_shifter.thermo_optic` rows (platform soi, fab org_imec, test_structure true), each with P_pi and
the 1/e heating / cooling time constants from Table I.

- Not entered: line resistivities (ohm/um, Table I; no registry parameter, values in notes); 80 pm/K Si thermo-optic
  shift (generic material statement); "10-20 times" / "factor of 20" efficiency ratios (derivable from the rows); MZI
  FSR about 13 nm (test-structure property); refs. [1]-[3] (cited).
- Judgment calls: (1) fab org_imec from "The devices were fabricated in imec's silicon photonics platform [4]" (passive
  sentence naming the org, Contract v7); the authors' own trench / undercut post-processing ("we processed", Ghent
  University - imec and IMEC vzw authors) adds no second fab org (D154); (2) p_pi_mw band `unspecified` (probe
  wavelength not stated; no operating band named); (3) Table I gives one value per heater type without saying which
  of the five heaters (3 lengths, 3 offsets) or a fit over them; one row per type and insulation, noted.

## Missing orgs

None: org_imec, org_epfl and org_astar_ime exist in `organizations.csv`.

## Registry gaps

- `heater_line_resistance_ohm_per_um` (phase_shifter): heater line resistance per unit length from the I-V slope. Skipped
  values: masood2013 Table I (p.2) 293 / 317 (doped Si), 27.3 / 28.0 (silicide), 1.1 / 1.3 (W) ohm/um without / with
  insulation.
- `pdl_bandwidth_nm` (fiber_chip_coupler, polarization): full width over which PDL stays below the stated level (level
  in condition). Skipped values: sacher2018 trilevel GC 1-dB PDL bandwidth 80 nm measured / 67 nm simulated, 0.5-dB PDL
  bandwidth 44 nm measured / 25 nm simulated (p.8, Table 2 p.7); entered meanwhile as pdl_db bounds with the bandwidth
  in the condition.
