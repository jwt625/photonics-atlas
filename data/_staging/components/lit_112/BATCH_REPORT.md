# lit_112 batch report (D392)

Date: 2026-11-08. Papers: saber2017, zhang2015, lu2015a, fu2026, guan2017, halir2016, ortegamonux2013.
Output: 37 components / 353 metric rows. Dry-run: `merge_component_staging.py data/_staging/components/lit_112 --dry-run`
-> +37 components, +353 metrics, 0 errors (one pre-existing warning on cmp_lit_ni2025b_pimmwc, not this batch).
All seven cached texts match their source rows (page-1 titles checked); none is a correction or another paper.

## Per paper

### saber2017 (transversely coupled FP resonators with Bragg mirrors, Opt. Lett. 43, 13)
- 14 components `resonator.bragg` (type I and type II x 7 effective cavity lengths, Table 1), 117 metrics.
- Per row: `extinction_db` and `insertion_loss_db` (de_embedded, GC loss calibrated out with calibration GCs, p.2) from
  p.3 Table 1; shared design geometry (period 320 nm, 1500 periods per mirror, 500 x 220 nm waveguide, 2 um BOX,
  2.2 um cladding). Type I Leff 110 um: Q 3356, FSR 2.58 nm. Type I Leff 943 um: Q 23642, FSR 0.3 nm, FWHM 66 pm
  (Fig. 4(b) inset label, nm -> pm derived).
- Fab org_applied_nanotools ("fabricated at Applied Nanotools", p.4). CMC Microsystems for design tools only.
- Not entered: Fig. 5 Q / FSR vs Leff for the other 12 devices (small plot, overlapping series; Leff itself is computed
  from the measured FSR, Eq. 3); Fig. 6 / 7 simulated kappa sweeps (generic designs); 3-dB DC 1-dB bandwidth > 100 nm
  (cited, ref. 21 = lu2015a) and SWG GC 90 nm 1-dB bandwidth (cited, ref. 20); Table 2 values of other works;
  Leff as a metric (derived label, not a length).
- Text conflicts (noted on rows): type I 943 um IL 1.43 dB (abstract, p.2, Table 1) vs 1.48 dB (p.3 text); ER 8.69 dB vs
  8.6 dB (p.3 text). Table values entered.

### zhang2015 (electrically tunable sidewall-Bragg-grating FP filter, Opt. Lett. 40, 3153)
- 2 components, 24 metrics: `resonator.bragg` filter (soi_rib) and `fiber_chip_coupler.grating` I/O pair (reference
  waveguide, 15.6 dB fiber-to-fiber).
- Filter: 3-dB notch width 46 pm, Q 33,500 / 25,700 (forward -1.0 V, 6.070 mA) / 44,000 (reverse 17.5 V), ER 16.4 / 5 /
  25 dB, total IL 19 dB fiber-to-fiber, grating-induced 2.1 dB (reference grating), implantation about 1.3 dB (derived
  remainder), implantation excess loss 10.3 dB/cm (derived by the authors), Bragg wavelength 1541.75 nm, shift rates
  -1150 pm/V (forward, derived from -1.15 nm/V) and 4.2 pm/V (reverse), shifts 0.345 nm / 0.0736 nm, geometry (rib 500 /
  220 / 90 nm, period 310 nm, cavity 24.025 um, 2 um BOX, footprint 0.205 mm2 -> um2 derived).
- Fab org_cmc_microsystems: acknowledged for "enabling the fabrication" (p.4), MPW-access fab org per D398; foundry not
  named.
- Not entered: EO 3-dB modulation bandwidth about 5.6 GHz (1.5 / 3.1 GHz at other detunings, Fig. 5) and 3.5 Gb/s eye
  (modulator metrics; EO-atlas candidate, not in `../eo-modulator-atlas`); calculated photon-lifetime cutoff 6.3 GHz;
  turn-on about -0.7 V and breakdown about 16 V; grating length 1240 um and corrugation depth 75 nm (no resonator-class
  parameter); GC / Y-branch designs (refs. 10, 11); strip-rib taper 50 um (geometry only).

### lu2015a (broadband DC with asymmetric-waveguide phase control, Opt. Express 23, 3795)
- 10 components `splitter.directional_coupler` (TE / TM x 10/90 ... 50/50, Table 1), 114 metrics.
- Per row: average measured cross `split_ratio_pct` (mean), the paper's "+/- 1 dB bandwidth" as `bw_1db_nm` with the
  definition in condition (see registry gap 1), excess loss < 1 dB (TE) / < 0.7 dB (TM) as `on_chip_excess` including
  the MZI test circuit (stated for all couplers, p.11; D465 analogue), L1 as `coupling_length_um`, widths / gap / bend
  radius / thicknesses, footprint (product of the printed dimensions, derived). 50/50 rows add MZI ER > 20 dB (TE) /
  > 30 dB (TM, 1500-1590 nm) and FDTD deviation +/- 3.5 % / +/- 1.5 % as `coupling_variation` (derived, % -> fraction).
- Fab org_university_washington: a named person at the University of Washington WNF fabricated the devices (p.12;
  D395 / D399). Facility: Washington Nanofabrication Facility missing from the registry (see below).
- Not entered: GC ripples 0.3 / 0.15 dB (cited, ref. 19), 2.7 dB/cm TMM loss (cited, ref. 14), conventional DC
  (simulation only, no number), TM 50/50 +/- 0.15 dB ratio deviation (no parameter; in notes).

### fu2026 (STIRAP coupler and mode-order converter on EpoCore-loaded etchless TFLN, Opt. Express 34, 28227)
- 2 components, 20 metrics: `splitter.adiabatic` TM0-TM0 three-waveguide coupler and `mode_converter.converter`
  TM0-TM1 converter.
- Measured (1500-1630 nm): IL < 3.52 / < 4.11 dB (scope unspecified: normalization of Fig. 9 not stated), CT < -15.81 /
  < -15.34 dB. Simulated (1450-1650 nm): IL < 0.2 / < 0.3 dB, CT < -16.32 / < -17.93 dB; coupler IL < 0.5 dB under
  +/- 100 nm deviations. Geometry: W1 2.2 um, L1 2.2 mm, Sab(0) 1.65 um; W2 2.35 um, W3 5.4 um, L2 4 mm; TFLN 300 nm,
  EpoCore 400 nm, SiO2 4.7 um.
- Fab org_jilin_university ("we fabricated", in-house facilities, all authors Jilin University; D399). Platform `other`
  (registry gap 3).
- Not entered: conventional DC / MC (fabricated, Fig. 9(b), (d), no stated values; simulated 0.2-dB / 0.3-dB bandwidths
  90 / 60 nm have no parameter); simulated supermode losses (0.8 dB/cm, 21 dB/cm); MC IL deterioration < 0.35 dB (a
  change); Sde(0) 1.45 um (gap_nm not allowed on mode_converter, registry gap 4).
- Text issues (in notes): simulated CT < -16.5 dB in abstract / p.2 vs -16.32 dB (p.5); p.4 says Sab(0) = 0 then sets
  Sab(0) = 1.65 um; the MC text calls the figures Fig. 5 / Fig. 6 while the captions number them Fig. 6 / Fig. 5.

### guan2017 (compact 90-degree hybrid on SOI, Opt. Express 25, 28957)
- 3 components, 22 metrics: `splitter.hybrid_90` hybrid, `splitter.mmi` PSO 2x2 MMI sub-block, `splitter.y_branch`.
- Hybrid (22 dies, one 8-inch wafer): total loss < 0.5 dB mean, < 0.6 dB mean + 1 sigma, < 0.45 dB single die
  (entered as `excess_loss_db`, rule 6: the paper's IL is input minus the sum of the four outputs); imbalance < 0.25 /
  < 0.35 dB; phase error mean 0 to -1 deg, 1-sigma band within +/- 3 deg, < 2 deg single die, < 3 deg packaged receiver;
  simulated loss < 0.3 (LO) / < 0.45 dB (signal); footprint 602 um2, bend radius 4 um.
- MMI: simulated phase error < 1.2 deg; Table 1 geometry (width W3 1.6 um, length 8 um derived from the Fig. 2(a)
  segment sequence, access 0.7 um, taper 1 um, gap 0.2 um, interconnect 0.5 um).
- Y-junction: excess loss < 0.1 dB across the C band as `author_estimate` (origin not stated).
- Fab empty: "fabricated in a 220-nm SOI platform [34]" names no org (D433); process_name empty.
- Not entered: CMRR (> 31 dB mean, > 28 dB worst case, > 30 dB single die, 30 dB simulated; registry gap 2); 90-degree
  bend loss about 0.01 dB (cited, ref. 31); bend phase uncertainty 6.4 deg (estimate from a cited coherence length);
  simulated per-port MMI loss Fig. 2(c) (includes the intrinsic 3 dB); Table 2 values of other works.

### halir2016 (ultra-broadband SWG-metamaterial MMI, Laser Photonics Rev. 10, 1039)
- 4 components, 29 metrics: 74-period SWG MMI (headline), 72- and 76-period length siblings (Fig. 7 figure reads), and
  the optimized conventional MMI (`row_kind: design`, simulated).
- 74 periods: measured EL / imbalance < 1 dB and phase error < 5 deg over 1375-1700 nm; simulated same criteria over a
  500 nm span (1250-1750 nm inferred from the axis and p.4); Table 1 geometry (3.25 x 14 um, WA 1.7 um, taper 5.7 um,
  s 0.3 um, period 190 nm, 220 nm Si).
- 72 / 76 periods: EL maxima about 0.6 / 0.8 dB, |imbalance| 0.1-1.0 / 0.6-1.8 dB, phase error -2 to +5 / -10 to -1 deg
  (Fig. 7, 1400-1600 nm, reading uncertainty in notes); lengths derived as N x 190 nm.
- Conventional design: simulated minimum EL about 0.3 dB near 1570 nm (Fig. 5(a) read), Table 1 geometry.
- Fab org_national_research_council_canada as borderline (D84b): NRC staff thanked for preparing the e-beam lithography
  files (p.6); no fabrication org in the text. Coordinator may empty it if file preparation is not "help with device
  fabrication".
- Not entered: composite-criterion bandwidths (> 300 nm measured, 500 nm simulated, < 200 nm conventional; registry gap
  6); duty cycle 50 % and 74 periods (no fill_factor / n_periods on splitter, registry gap 7); fabrication tolerances
  (+/- 7 % duty cycle, +/- 50 nm width, simulated); beat lengths; setup agreement (5 deg / 0.5 dB / 1 dB).

### ortegamonux2013 (MMI with SWG slot, Laser Photonics Rev. 7, L12)
- 2 components, 27 metrics: SWG-slotted 2x2 MMI (22.85 um) and the conventional 47 um reference MMI.
- Measured back-to-back ER > 15 dB / > 12 dB (1530-1570 nm); imbalance about 1.3 / 1.7 dB and phase error about 5 / 6 deg
  as `author_estimate` (assumption of equal contributions, Eq. 3); simulated IL (entered as excess loss) / imbalance <
  0.4 / 0.4 dB, phase error < 1 deg (slotted) and < 0.8 / 0.8 dB, < 3 deg (reference, 1.5-1.6 um); geometry.
- Fab empty (passive "were fabricated", authors at two orgs). Commercial SOI substrate (supplier not named).
- Not entered: hole size ws = G = 50 nm and N = 96 (no splitter parameter; in notes), Bragg-limit pitch 258 nm (design
  bound), SWG facet couplers (ref. 9).

## Missing fab / facility orgs

- Washington Nanofabrication Facility (WNF), University of Washington, Seattle, US (part of NSF NNIN at the time):
  lu2015a p.12 Acknowledgments, facility role (fabrication performed there). Same gap reported by lit_21 / lit_22 /
  lit_42 / lit_46 / lit_47.

## Judgment calls (coordinator)

1. lu2015a "+/- 1 dB bandwidth" (split ratio within +/- 1 dB of the design value) entered as `bw_1db_nm` with the
   definition in condition; alternative: drop to notes until a split-ratio bandwidth parameter exists.
2. lu2015a excess-loss bounds (< 1 dB TE, < 0.7 dB TM) entered on every coupler of the type: the sentence states them
   for all couplers (D465 analogue, not a D254 typical value).
3. halir2016 fab NRC Canada borderline (D84b) from staff thanks for e-beam file preparation.
4. guan2017 Y-junction < 0.1 dB kept as `author_estimate`: the value is attached to the "improved design" of ref. 28 in
   this paper; if read as the ref. 28 value it should be deleted (D259).
5. guan2017 single-die row: Fig. 6 caption says "typical die", Table 2 says "best"; entered as `statistic: single`.
6. saber2017 and zhang2015 FP cavities with Bragg-grating mirrors classed `resonator.bragg` (chowdhury2024 precedent).
7. zhang2015 forward-bias rows keep the paper's sign convention (forward written as -1.0 V).
8. saber2017 process_name empty: the SiEPIC EBeam PDK is named only for simulations (p.3); fab is Applied Nanotools.
9. Brief vs skill file name: the report is written as `lit_112_REPORT.md` per the task brief (the skill names
   `BATCH_REPORT.md`).

## Registry gaps (proposed definitions)

1. `split_ratio_bw_nm` (splitter): wavelength span over which the split ratio stays within a stated tolerance of its
   design value (tolerance in condition). lu2015a Table 1 p.11 (75-100 nm).
2. `cmrr_db` (splitter.hybrid_90, photodetector): common-mode rejection ratio, positive dB. guan2017 p.9-10 Fig. 5(c),
   6(c), p.7 Fig. 3(d): > 31 dB mean, > 28 dB worst case, > 30 dB single die, 30 dB simulated.
3. Platform enum `lnoi_loaded_polymer` (polymer-strip-loaded etchless TFLN). fu2026 p.3 Fig. 1(d) (EpoCore 400 nm on
   300 nm x-cut TFLN).
4. `gap_nm` on mode_converter. fu2026 p.7 Sde(0) 1.45 um.
5. `layer2_thickness_nm` on splitter (loading-layer thickness). fu2026 p.3 EpoCore 400 nm on the coupler row.
6. `bw_composite_nm` (splitter): bandwidth meeting a composite criterion stated in condition (e.g. EL and imbalance < 1 dB,
   phase error < 5 deg). halir2016 p.2 / p.5-6: > 300 nm measured, 500 nm simulated, < 200 nm conventional.
7. `n_periods` and `fill_factor` on splitter (SWG MMIs). halir2016 p.3 Table 1 (74 periods, 50 %); ortegamonux2013 p.3
   (96 periods); `grating_length_um` and a `corrugation_width_nm` on resonator: saber2017 p.2 (480 um mirrors, 100 nm
   corrugation), zhang2015 p.2 (1240 um grating, 75 nm corrugation depth).
8. `bw3db_ghz` and `breakdown_voltage_v` on resonator (PN-tuned cavities), or route to the EO atlas: zhang2015 p.3-4
   (5.6 GHz) and p.2 (breakdown about 16 V).
