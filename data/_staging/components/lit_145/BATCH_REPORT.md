# lit_145 batch report

Distilled 2026-11-15. Papers: shu2026, fard2017, sun2018, poot2014. Page-1 titles match the source rows (all four).
Totals: 22 components, 133 metric rows. `merge_component_staging.py --dry-run`: 0 errors (the one warning is on
`cmp_lit_ni2025b_pimmwc`, an already merged row outside this batch).

## shu2026 (PhotoniX 2026, thin-film PZT 4x4 MRR programmable optical matrix): 3 components / 22 metrics

- `cmp_lit_shu2026_pzt_mrr_test_ring` (resonator.ring, test structure): FSR ~2.5 nm, non-volatile trimming range
  ~2.5 nm at Vset 25 V, R 60 um, PZT 300 nm, etch 150 nm.
- `cmp_lit_shu2026_pzt_mrr_tuner` (phase_shifter.ferroelectric_nonvolatile): EO tuning ~17.7 pm/V, rise / fall
  45 / 37 ps (stored in us, derived), 40 non-volatile levels (ISPP), geometry.
- `cmp_lit_shu2026_matrix_4x4` (switch_fabric.other): 4 x 4 ports, excess loss 0.75-4.0 dB and crosstalk
  22.9-43.2 dB at 1552 nm, through-port notch ~40 dB after trimming, WSS ER 21-39 dB / 18-35 dB and adjacent-channel
  crosstalk ~20 dB (1536.32-1538.18 nm), identity weight matrix ER 21.3-40.4 dB, geometry.
- Not entered: 100,000-cycle endurance, ~30 pm/C temperature stability and ~0.1 nm retention shift after 3 weeks
  (p.5-6, attributed to the authors' ref. [46]); capacitance ~1200 fF and programming energies 120 pJ / 1.08 nJ /
  17.28 nJ (computed from a cited 3.2 fF/um, p.17); transmitter eye ER 3.105-5.768 dB (mean 4.37, std 0.87) and
  40 Gb/s (modulator metrics, rule 2); W1 / W3 normalized powers -0.95 +/- 0.49 and -28.47 +/- 4.54 dB (no
  parameter); residual misalignment < 50 pm and initial 590 pm (no switch_fabric parameter; in notes); DC drift
  < 40 pm over 30 min at 5 V (no parameter); Vth ~10 V (no parameter); CNN accuracy 96.98 % (system simulation);
  Fig. 7 / Table S2 comparison (other works). Supplementary (Fig. S1-S6, Table S1-S2) is not in the cache.
- Fab: `org_zhejiang_university` from the author-contributions fabrication sentence (p.18: T.S., Z.Y., H.Y.).
  Missing org: "Hangzhou Institute for Advanced Study, University of Chinese Academy of Sciences" (H.Y.'s
  affiliation 2, p.1; fab role, p.18). Proposed: child of `org_university_of_chinese_academy_of_sciences`, then a
  fab fix on the 3 rows. AFM help thanked to a staff member of "The Micro-Nano Fab Fabrication Center, Zhejiang
  University" (p.18): staff thanks, no facility (D84b).
- Judgment calls: (1) one test MRR as two rows (ring + ferroelectric tuner, D396, chen2022 precedent); EO pm/V and
  rise / fall times kept on the tuner row as switching-element data, not modulator metrics (the paper is a switch
  paper; coordinator may move them out under rule 2). (2) WSS and weight-matrix configurations kept as conditions on
  the one switch_fabric.other row (rule 9) instead of a separate switch_fabric.wss row. (3) Excess loss scope
  `unspecified` (normalization not stated). (4) The 40-level MRR is not identified as the test MRR or a matrix MRR;
  entered on the tuner row (same 60 um design), noted. (5) Platform `other` (no PZT enum value).

## fard2017 (Opt. Express 2017, grating-assisted all-Si 850 nm PDs): 7 components / 48 metrics

- Four grating-assisted lateral p-i-n Si PDs (`pd1_gc_wi5um`, `pd2_gc_wi2um`, `pd3_gc_wi1um_3finger`,
  `pd4_fgc_wi0p3um`; photodetector.other), two no-GC references (`pd1_nogc`, `pd3_nogc`; photodetector.vertical),
  and the straight 850 nm grating coupler (`gc_850_straight`, fiber_chip_coupler.grating, simulated 62 % only).
- PD metrics: responsivity vs bias at 848.2 nm (ref_plane fiber), dark current, S21 3-dB bandwidth, avalanche gain 6
  (no. 4), Table 1 capacitance and the parasitic resistance (author_estimate, "estimated from dimensions"), lengths,
  220 nm Si, BOX 2 um, rib width 500 nm (no. 4).
- Not entered: p.3 sentence values of the authors' ref. [21] (0.15 A/W, 0.4 nA at 12 V, 35 Gb/s; rule 3 / D259);
  Table 1 and Sec. 3 values of no. 2 kept (no attribution; journal extension, D408); 0.425 A/W and 0.013 A/W
  calculated maxima; transit / RC time constants; 17 % fraction reaching the no. 4 diode; FoM; BER sensitivities;
  Fig. 2(c) grating labels 335 / 200 nm (period vs tooth not identifiable, D156); FGC labels 18 / 11.8 / 23.9 um
  (no FGC row: no FGC performance stated); doping concentrations (notes only).
- Fab: `org_astar_ime` ("fabricated at the Institute of Microelectronics IME-A*Star", p.6). CMC acknowledged for
  "contributions and technical support" (p.12), not for fabrication or MPW access: not entered (judgment call; D83d /
  D398 would make it a fab org if the coordinator reads the acknowledgement as MPW access). process_name "0.12 um SOI,
  0.22 um Si thickness (IME, Table 1)".
- Judgment calls: class `photodetector.other` for the GC-fed lateral p-i-n PDs (vertical fiber illumination through
  an integrated grating; not Ge, not bare vertical illumination); no-GC references `photodetector.vertical`.
  Avalanche gain 6 `measured` with the note that it equals 0.3 / 0.05 A/W (method not stated). Reverse biases stored
  negative.

## sun2018 (Opt. Express 2018, III-V PDs on Si by heteroepitaxy): 9 components / 39 metrics

- Five 30 um mesa top-illuminated PDs (photodetector.vertical): A MUTC on InP-on-Si, B MUTC on n+ InP, C PIN-1 on
  InP-on-Si, D PIN-1 on n+ InP, E PIN-2 (MOCVD) on InP-on-Si; platforms `iii_v_on_si_epi` / `inp`. Metrics:
  responsivity at 1550 nm (Fig. 6 labels), dark current (< 10 nA at -3 V for A / C / D / E; B 100 pA), B dark
  current density 1.6 uA/cm2 (label), 3-dB bandwidth (9 / 9 / 7 / 7 GHz), Cj and Rs from the S11 fit (Table 1),
  mesa diameter as `absorber_width_um`, 1.3 um absorber (PIN rows).
- Four 40 um siblings (A-D) for the RF saturation test: saturation photocurrent > 10 mA at -5 V.
- Not entered: 0.8 mA/cm2 dark-current density (abstract, Table 2, Fig. 4 label): the label circle spans the
  overlapping A / C / D / E curves, half blue (C) half magenta (E) - device ambiguous (D159), in component notes;
  1-dB RF saturation output power 2.6 dBm and OIP3 > 15 dBm / > 20 dBm (device D) (registry gaps); Ls and Cst
  (Table 1); Fig. 5 LCR capacitance points and Fig. 4 inset (diameter series); Table 2 other works.
- Conflicts noted (D417): device C responsivity 0.76 A/W (Fig. 6 label, entered) vs text 0.79 A/W for C and D;
  device B 1.6 uA/cm2 label vs 100 pA at -3 V over a 30 um mesa (about 14 uA/cm2); Fig. 8(c) panel label for
  device A reads Iph = 6 mA vs text 5 mA for MUTC PDs.
- Fab empty (passive "were fabricated", no org; D80b). Si templates from IQE Inc. (wafer supplier, notes).
  Facilities: none acknowledged.
- Judgment calls: InP-substrate reference devices B / D kept as rows (same paper's measured devices, D155 scope);
  the "all PDs < 10 nA" bound entered on each 30 um row it covers (not a typical value on one representative row,
  D254); ref_plane `unspecified` (illumination optics not stated).

## poot2014 (APL 2014, arXiv text; SiN optomechanical phase shifter): 3 components / 24 metrics

- Three phase_shifter.mems rows by gap design: dopt 125 / delec 175 nm (phase shift > 0.5 pi derived from "more than
  90 deg"; Vpi ~10 V author_estimate, extrapolated, D435), dopt 125 / delec 225 nm (3-dB bandwidth 1000 kHz and
  fundamental mode 580 kHz, derived from MHz; simulated ~1.0 pi at 10 V), dopt 158 / delec 225 nm (~0.16 pi at
  +/-10 V read off Fig. 2(c), extracted_from_figure). Geometry on each: gap, Li 170 um, 1000 nm waveguide, 330 nm SiN,
  3.3 um oxide, ~30 nm SiN slab.
- Not entered: wavelength-shift curvature -133 pm/V2 and phase curvature -60 / -174 mrad/V2 (no parameter); 710 ns
  pulse FWHM (no pulse-width parameter); 6 urad/Hz^0.5 noise floor (laser / detector); no power dependence up to
  6.9 dBm (device of the panel not named; no phase_shifter power-handling parameter); 70 mW / 7 W gradient-force
  equivalents (calculation); force 1.0 uN, displacements 134 / 75 / 200 nm, spring constant 4.6 N/m (design
  calculations); arm width 500 nm / length 100 um and electrode gap delec (no role parameter; in notes / gap note);
  MZI fringe period 12.6 nm and 90 um arm offset (test interferometer, no row); grating couplers (no values).
- Fab empty (passive; both authors Yale, D80b). Missing facility org: "Yale Institute for Nanoscience and Quantum
  Engineering" ("Facilities used were supported by ...", p.4 Acknowledgments; facility role; also reported by an
  earlier batch for guo2016). NSF MRSEC DMR 1119826 is a grant (not entered).
- Judgment calls: 90 deg statement assigned to the 125 / 175 device (only its curve passes 90 deg on the right axis);
  printed gaps kept as `design_target` although the paper says actual gaps differ from the designed ones.

## Registry gaps (skipped value + locator + proposed definition)

- `dc_drift_pm` (phase_shifter / resonator): resonance drift under constant bias over a stated time; shu2026 < 40 pm
  over 30 min at 5 V (p.6, Fig. 2(g)).
- `wavelength_spread_nm` for switch_fabric (or `trim_precision_pm`): residual resonance misalignment after trimming;
  shu2026 < 50 pm over 16 MRRs (p.6), 590 pm before (p.6).
- `rf_output_power_1db_dbm` (photodetector): RF output power at 1-dB compression; sun2018 2.6 dBm at 9 GHz, -5 V,
  40 um (p.9, Table 2, Fig. 9).
- `oip3_dbm` (photodetector): third-order output intercept point; sun2018 > 15 dBm over 1-9 GHz at 8 mA, -5 V
  (p.9, Fig. 10).
- `power_handling_dbm` for phase_shifter: highest optical power without effect; poot2014 6.9 dBm (p.4, Fig. 2(c)).
- `tuning_curvature_pm_per_v2` (phase_shifter.mems): quadratic electrostatic tuning coefficient; poot2014
  -133 pm/V2 (p.3).
- `pulse_width_ns` / optical response FWHM (phase_shifter): poot2014 710 ns (p.3, Fig. 3(c)).
