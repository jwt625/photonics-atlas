# lit_280 batch report

Distilled 2026-11-25. Papers: lit:zhang2021c, lit:kudalippalliyalil2020, lit:lin2022b, lit:zhan2021,
lit:herrerobermello2020 (all Optics Express, polarization family). Page-1 titles match the source rows; no correction /
erratum; no garbled text layer. Total 17 components / 127 metric rows. `merge_component_staging.py --dry-run`: 0 errors
(2 warnings belong to other batches: guo2024a, ni2025b).

Fab / facility: every row has `fab_org_ids` and `facility_org_ids` empty. No acknowledgment of a shared facility in any
paper; no org missing from the registry is needed.

## lit:zhang2021c (2 components / 24 metrics)

- `cmp_lit_zhang2021c_am_pbs` (fabricated, polarization.pbs, soi): measured IL < 1 dB (max transmission > 80 %,
  authors' conversion, derived), PER > 20 dB 1520-1595 nm both polarizations (Input A), peak PER > 50 dB TE / > 30 dB
  TM; simulated final design (Fig. 4(d)(e), Fig. 7 with S-bends, Fig. 8 3 um S-bend offset, conclusion < 0.9 dB);
  geometry (220 nm / 2 um BOX, 500 nm arms, 60 nm strips, Lc 14 um, footprint 35 um2 derived).
- `cmp_lit_zhang2021c_am_pbs_t100_design` (design): intermediate design T 100 nm / w 50 nm / Lc 14 um: PER 46 / 32 dB,
  IL < 0.2 dB (sweep wavelength not printed: 1550 nm inferred from the stated 1.55 um centre wavelength).
- Not entered: conclusion "PER > 30 dB TE / > 20 dB TM with 80 nm bandwidth" (p.11) - the window is not identifiable
  in Fig. 6(d) (TE ~20-28 dB at 1520-1530 nm, < 20 dB above ~1600 nm), in component notes; coupled-mode coupling
  lengths 7110 / 14.6 um and idealized PER 63 / 85 dB / infinite (p.4-5); sweep bounds (transmission > 99 % / 94 %);
  gap 500 nm, period 120 nm, N 4 (registry gap below).
- Conflicts noted (D417): abstract 33 dB vs body 32 dB TM PER; abstract / Table 2 bandwidth 80 nm vs the stated
  1520-1595 nm (75 nm); abstract "< 0.2 dB within 70 nm" not shown in the body.
- Fab: "we fabricate the device" (p.7) but four unrelated author orgs (Jiangsu University, DTU Fotonik, NUDT,
  AMS Beijing): empty (D72 / D80b).
- Judgment calls: measured IL scope `per_component` with method `unspecified` (the paper says "normalized
  transmission" without naming the reference); upper cladding left empty (not stated for the fabricated chip); the
  Fig. 8 3 um S-bend values kept on the fabricated row with the condition saying the fabricated offset is not stated.

## lit:kudalippalliyalil2020 (6 components / 33 metrics)

- `cmp_lit_kudalippalliyalil2020_ammi_ps` (fabricated, polarization.pbs, sin): IL < 1 dB 1525-1625 nm (reference
  waveguide), IL < 1 dB at ~100 mW, cascade-fit IL 0.6-0.85 dB TE / 0.74-0.92 dB TM (derived: per-device slope rests on
  the stated identical-splitter / combiner assumption), summary ~0.7 / ~0.8 dB, Fig. 12(b) Delta L1 = 0 reads at
  1550 nm; geometry (450 nm SiN, 2.5 um BOX / cladding, W1 900 nm, W2 1250 nm derived, L1 20.85 um, 80 um length,
  footprint 1040 um2 derived).
- Four tolerance siblings `..._ammi_ps_dl_m1p0 / m0p5 / p0p5 / p1p0` (L1 offset -1.0 / -0.5 / +0.5 / +1.0 um;
  test_structure true): IL TE / TM read off Fig. 12(b) (+/- 0.05 dB) and L1 derived.
- `cmp_lit_kudalippalliyalil2020_inverse_taper` (fiber_chip_coupler.edge): ~4.5 dB TE / ~5.3 dB TM per facet
  ("estimated", no arithmetic shown: measured per D167; C+L inferred), tip 450 nm, length 400 um.
- Not entered (D424): all crosstalk values. CT_TE = P1(TM)/Pin(TM) and CT_TM = P2(TE)/Pin(TE) (p.5, Fig. 6 caption)
  are wrong-input leakage relative to the input power; crosstalk_db is not allowed for polarization. Values for the
  coordinator: measured CT <~ -18 dB TE / <~ -19 dB TM over 1525-1625 nm (p.9, Fig. 11(a)); abstract < -18 / < -20 dB;
  high power CT <~ -16 dB (Fig. 11(b)); simulated CT < -17 / < -18 dB C+L (p.5); Fig. 12(b) reads CT_TE / CT_TM about
  -7 / -9, -14 / -13, -18.4 / -21.3, -16 / -14.6, -11 / -9.3 dB at Delta L1 -1.0 / -0.5 / 0 / +0.5 / +1.0 um; cascaded
  PS-PC "CT negligible (-15 dB)" (p.9).
- Also not entered: angles 5 / 7 deg and the 35 um TM-port taper (no polarization parameter); Fig. 13(a) cascaded
  PS-PC transmission (pair, not a component).
- Conflict (D417): TM IL ~0.8 dB (abstract, introduction) vs ~1.0 dB (conclusion), both noted.
- Fab: "We fabricate the designed AMMI" (p.7), authors at University of Maryland (IREAP) and Laboratory for Physical
  Sciences, first author at both, place not stated: empty (D72 / D83c).

## lit:lin2022b (2 components / 25 metrics)

- `cmp_lit_lin2022b_te_polarizer_air` (fabricated, polarization.other, soi_strip: full etch stated): measured IL
  < 0.8 dB (1260-1360 nm) and < 0.71 dB (1520-1580 nm), PER > 23 dB in both windows; IL rows `derived` + `cutback`
  (averaged over ten cascaded devices, arithmetic not shown; xu2019 precedent); simulated Fig. 3 values and tolerance
  rows (Delta w +10 nm, sidewall 87.5 / 85 deg); geometry (220 nm, 3 um BOX, 430 / 100 / 1000 nm widths derived from
  um, footprint 219.3 um2 derived); sidewall ~85 deg `author_estimate` (process value "in our lab", not measured on
  the device).
- `cmp_lit_lin2022b_te_polarizer_sio2_design` (design, SiO2 clad): simulated IL < 0.3 dB, PER > 25 dB (1260-1680 nm)
  and > 30 dB (1260-1580 nm); Table 2 geometry; footprint 263.29 um2 derived.
- Not entered: SWG periods 200 nm, duty cycles 0.4 / 0.6, N 23 / 26, lstep, lN, taper length 4 um (registry gap);
  Table 3 "BW(PER > 20 dB) > 160 nm" (sum of the measured windows); parameter sweeps of Fig. 2.
- Fab: passive "was fabricated" (p.8), no org: empty (D80b).
- Judgment call: `lmid` (Fig. 1(b), the transverse size of the middle-SWG segments) entered as `width_nm` with the
  role in condition.

## lit:zhan2021 (3 components / 23 metrics)

- `cmp_lit_zhan2021_pbs_pimmi_abg` (fabricated, polarization.pbs, sin): PER > 30 dB both polarizations over ~22 nm
  (span 1548-1570 nm read off the Fig. 6 dashed markers), IL ~0.6 dB TE / ~1.1 dB TM (reference waveguide), ~820 um
  length.
- `cmp_lit_zhan2021_pi_mmi` (splitter.mmi, test_structure true): measured excess loss < 1 dB 1526-1580 nm for the
  two-MMI MZI (scope `device_total`, not per MMI); simulated per-port excess loss < 0.23 / < 0.6 dB, imbalance
  < 0.1 / < 0.18 dB, phase error 0.45 / 1.116 deg (printed 0.0025 pi / 0.0062 pi) for 1535-1565 / 1500-1600 nm;
  Table 1 geometry (10 x 75.2 um, w 2.4 um as port_width_um).
- `cmp_lit_zhan2021_abg` (reflector.bragg): TM SLSR ~30 dB measured (authors' inference from port-2 level vs the
  ~-40 dB MMI-MZI floor; basis `measured` with the reasoning in condition), ~60 dB transfer-matrix, ~30 dB simulated
  with truncated ends; grating length ~440 um from the Fig. 1 label.
- Not entered: MZI port-2 level ~-40 dB (a normalized port level, not an extinction ratio); input offset d 3.4 um (no
  parameter); butt-coupler "simulated > 90 %" (carries ref. [25], D80i); grating period / widths (not printed).
- Fab: passive "was fabricated using the following procedures" (p.5), no org: empty (D80b).

## lit:herrerobermello2020 (4 components / 22 metrics)

- `cmp_lit_herrerobermello2020_pbs_tilt15_n400` (fabricated, main device): IL < 1 dB and ER > 13 dB both
  polarizations 1520-1640 nm (ER = output-port ratio, so per_db); simulated (55 nm air gap) ER > 20 dB / IL < 1 dB in
  "the full 130-nm bandwidth" (band edges not printed: band unspecified); geometry (220 nm, 2 um BOX, 3 um cladding,
  WMMI 4000 nm and Wt 1500 nm derived, 110 nm segments, LMMI 91.1 um).
- `..._tilt15_n400_dc60` (duty cycle 60 %, 132 nm segments): IL ~2 dB TM / ~2.5 dB TE (no wavelength: C+L inferred).
- `..._tilt15_n395` (395 periods): TM IL <= 1.5 dB ("of to 1.5 dB") and TM ER > 13 dB over 100 nm (span 1540-1640 nm
  read off Fig. 4(a), +/- 5 nm).
- `..._tilt7_n417` (nominal 7 deg design, fabricated): measured TM ER > 20 dB (no range: C+L inferred); simulated
  Fig. 2(a) (filled gaps) IL < 1 dB / ER > 20 dB and Fig. 2(b) (55 nm air) TM ER > 20 dB / TM IL < 1.6 dB (band edges
  not printed).
- Not entered: measured back reflection < -30 dB (setup-limited) and simulated < -53 dB (back_reflection_db not
  allowed for polarization); thickness-tolerance bandwidths 129 / 118 nm; 395-period / 60 % device (Fig. 4(b),
  qualitative text only, no row); tilt angle, period, N, taper length 13 um (no polarization parameter).
- Judgment call (D408 borderline): the 7 deg design and its dimensions come from the authors' earlier theoretical paper
  (ref. [26]); kept because this paper fabricates and measures it, lists it in its own Table 1, and the Fig. 2(a)
  simulation is new (130 nm here vs 128 nm in [26], p.6). The coordinator may prefer to drop the 7 deg simulated rows.
- Fab: passive "were fabricated" (p.5), no org: empty (D80b).

## Registry gaps (proposed, with skipped values)

1. `crosstalk_db` on polarization (D424 open): kudalippalliyalil2020 CT values listed above (wrong-input leakage
   relative to the input power). Definition: wrong-polarization power at an output port relative to the input power of
   that polarization, positive dB.
2. `back_reflection_db` on polarization: herrerobermello2020 < -30 dB measured (p.6), < -53 dB simulated (p.5).
3. `gap_nm`, `period_nm` / `subwavelength_period_nm`, `n_periods`, `fill_factor`, `taper_length_um` and
   `mmi_width_um` / `mmi_length_um` on polarization: zhang2021c gap 500 nm, strip period 120 nm, N 4 (p.7 Table 1);
   lin2022b SWG period 200 nm, duty 0.4 / 0.6, N 23 / 26, taper 4 um (Tables 1-2); herrerobermello2020 period 220 nm,
   duty 50 %, N 400 / 395 / 417, taper 13 um (Table 1); kudalippalliyalil2020 35 um TM taper (p.4). WMMI / W2 / lmid
   were entered as `width_nm` with the role in condition.
4. PER / ER bandwidth on polarization (e.g. `per_bw_nm`, criterion in condition): zhang2021c > 80 nm (abstract),
   zhan2021 ~22 nm at PER > 30 dB, herrerobermello2020 120 / 130 / 129 / 118 nm, lin2022b > 160 nm (Table 3). Precedent
   cheng2023 (not entered).
5. Tilt angle of SWG segments (`swg_tilt_deg`, geometry): herrerobermello2020 7 / 15 deg (Table 1); AMMI port angles
   5 / 7 deg (kudalippalliyalil2020 p.4).
