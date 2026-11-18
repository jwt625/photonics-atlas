# lit_200 batch report

Papers: `lit:shang2015` (Opt. Express 23(16) 21334, 2015), `lit:zhao2019` (IEEE Photonics J. 11(4) 4900808, 2019),
`lit:hwang2007` (IEEE PTL 19(6) 411, 2007), `lit:watanabe2013` (IEEE Photonics Conference 2013, TuG2.4). Cached
texts match their source rows (page-1 titles); no `garbled_text_layer`; figure values read on the page renders
(zoomed crops; Fig. 1(c) of shang2015 read by pixel calibration against the axis ticks). verified_on 2026-11-18.

Dry run: `merge_component_staging.py data/_staging/components/lit_200 --dry-run` -> +24 components, +113 metrics,
0 errors (the one WARN is on an existing ni2025b row, not this batch).

## shang2015 (13 components, 52 metrics)

| component_id (cmp_lit_shang2015_) | class | metrics |
|---|---|---|
| vertical_coupler | waveguide_platform.transition | 6: 0.01 dB per coupler (0.2 dB / 20-stage cascade, derived, mean, n 20), taper 100 um, tip 250 nm, gap 700 nm, core 200 nm, footprint 200 um2 (derived) |
| crossing_90deg_gap700 | crossing.multilevel | 4: 0.167 dB per crossing (measured, as printed), crosstalk 52 dB at 1550 nm, gap 700 nm, core 200 nm |
| crossing_60deg_gap500 / 90deg_gap500 / 60deg_gap700 / 60deg_gap900 | crossing.multilevel | 3 each: Fig. 6(d) crosstalk reads 27.9 / 38.4 / 39.3 / 47.5 dB (extracted_from_figure), gap, core |
| waveguide | waveguide_platform.straight | 5: 0.3 dB/cm (printed +/-0.1), 3.2 dB fiber-to-fiber, core 200 nm, width 2000 nm (Fig. 1(a) label, derived), min bend radius 50 um |
| lensed_fiber_facet | fiber_chip_coupler.edge | 1: 1.5 dB per facet (measured, D167) |
| heater_overclad_2um / 5um / 8um_design | phase_shifter.thermo_optic (design) | 6 each: simulated P_pi about 70 / 80 / 83 mW read off Fig. 1(c), heater 1000 x 2 um, overcladding 2 / 5 / 8 um, core 200 nm, width 2000 nm |
| star_coupler_27x32x2_gap800 / gap300 | splitter.other | 3 each: output non-uniformity about 5 dB / > 25 dB, n_inputs 27, n_outputs 64 (32 x 2, derived) |

Not entered:
- Fig. 2 (vertical-coupler simulations; caption cites the authors' OFC 2015 paper ref. [10]) and Fig. 3 (crossing
  transmission / crosstalk / reflection simulations; caption cites the authors' CLEO 2015 paper ref. [11]), including the
  p.3 "lateral misalignment up to 1.2 um" simulation statement: D259a / D408 caption clause.
- Misalignment tolerances 400 nm lateral and 15 um longitudinal (p.7, abstract, conclusion): no loss criterion printed
  (the `tol_1db_*` parameters need 1 dB; the Fig. 5(d) cascade at 0.4 um is about -0.3 dB over 20 couplers, so 1 dB per
  coupler is not implied); in component notes. ASML interlayer alignment < 60 nm: process spec, notes.
- Fig. 5(c)-(e) overlap / misalignment / taper-length series and Fig. 6(a)-(c) cascade transmissions: no per-device
  value printed; slope of the Fig. 6(b) 90 deg reads (about 0.07 dB per crossing) does not reproduce the printed 0.167 dB,
  so I did not derive per-crossing losses for the sibling designs (30 deg rows and the 500 / 900 nm 90 deg crossings
  therefore have no row; 900 nm / 90 deg and all 30 deg designs have no Fig. 6(d) crosstalk point).
- Bend loss: simulated "< 0.1 dB per 90 deg" (p.2 text) vs "< 0.3 dB per 90 deg" (Fig. 1(b) caption) and measured "no
  measurable excess bending loss" at 50 um (no number): no bend row.
- Star-circuit footprint 40 mm2 (from 80 mm2): which gap sample the photo shows is not stated (D159); absolute port
  transmissions in Fig. 7: setup terms not stated. Fig. 1(b) confinement-factor / bend-radius design curve: platform
  design study, not a component. AFM roughness 1 nm RMS: no parameter.
- 3x2 couplers and 9x32 star couplers individually: not characterized alone.
- Introduction values (~1 dB, 0.2 dB, 0.4-0.6 dB, 0.254 dB): cited work (rule 3).

Fab / facility: fab `org_university_of_california_davis` ("We fabricated the devices", p.5, all authors UC Davis);
facility `org_marvell_nanofabrication_laboratory` (p.9 Acknowledgments "Marvell Nanolab facility, University of
California, Berkeley"), as in the fu2023 precedent. Missing: "North California Nanotechnology Center, University of
California, Davis" (p.9 Acknowledgments, facility role) is not in the registry; it may be a former name of
`org_center_for_nano_micro_manufacturing` but nothing in this paper says so, so I left it out (coordinator to check;
alias, never a new id, if confirmed). Alias candidate: "Marvell Nanolab facility" -> `org_marvell_nanofabrication_laboratory`.

## zhao2019 (5 components, 40 metrics)

| component_id (cmp_lit_zhao2019_) | class | metrics |
|---|---|---|
| pbs_tapered_bent_dc | polarization.pbs | 16: measured ER >= 10.94 / 11.98 (TE) and >= 12.25 / 18.93 dB (TM), IL <= 1.61 / 1.39 (TE) and <= 2.22 / 1.22 dB (TM) over 1280-1360 / 1510-1590 nm; simulated ER >= 10.1 (TM) / 10.5 dB (TE), IL <= 1.37 (TM) / 1.33 dB (TE) over 1280-1600 nm; core 220 nm, BOX 3 um, cladding 1 um, length ~32.74 um |
| gc_o_te / gc_o_tm / gc_c_te / gc_c_tm | fiber_chip_coupler.grating | 6 each (Table 1): coupling loss 6.5 / 6.9 / 5.6 / 5.9 dB per coupler at the central wavelength, 3-dB bandwidth 37 / 32 / 45 / 43 nm, period 505 / 720 / 630 / 980 nm, fill factor (printed %, derived), etch 70 nm, core 220 nm |

Not entered: Table 2 rows of other works (cited); "~80 nm" per band and 160 nm total measured spans (set by the
lasers, no criterion bandwidth); Fig. 4 fabrication-tolerance simulation (IL <= 1.5 dB and ER > 10 dB for width
variation -10 to +20 nm; R1 +/- 1 um) - no parameter; Fig. 3 / Fig. 6 curves beyond the printed bounds.
PBS design geometry (widths 720 -> 500 nm and 380 -> 620 nm, gap 100 nm, R1 20 um, R2 20.1 um, R3 3 um, R4 7 um,
theta_max 30 deg, coupling length 13.22 um) is in component notes only (registry gap below).
Fab / facility: none ("were fabricated", passive, no org; no facility named).

## hwang2007 (5 components, 12 metrics)

| component_id (cmp_lit_hwang2007_) | class | metrics |
|---|---|---|
| bent_fiber_block | fiber_interface.other | 2: < 0.5 dB at about 3.5 mm bend radius, pitch 250 um |
| fc_opcb_path | fiber_interface.other | 4: 3.57 dB block-to-block without oil (printed), about 1.5 dB with oil (derived from Fig. 5(a) reads), pitch 250 um, fiber length 75000 um (derived) |
| vcsel_fiber_interface | fiber_chip_coupler.other | 1: 0.8 dB VCSEL to fiber block |
| fiber_pd_interface | fiber_chip_coupler.other | 1: 3 dB fiber block to PD |
| vcsel_pd_link | fiber_interface.other | 4: about 7.37 dB (no oil) and 5.3 dB (oil) VCSEL to PD, layer-to-layer difference < 1 dB, crosstalk > 53 dB (author_estimate, no data shown) |

Not entered: calculated interlayer skew about 6.0 ps (no parameter, notes); flip-chip bonding accuracy +/-3 um and
alignment-mark accuracy (process values); 3 Gb/s eye (system); VCSEL / PD device performance (not reported); board and
block sizes (notes). Wavelength: 850 nm inferred on all loss rows (link driven by the 850-nm VCSEL array).
Fab / facility: empty. "We fabricated three main components" (abstract) with authors at two orgs (D80b). Missing org:
"Isu-Petasys Co." (p.3 Acknowledgment, "manufacture of optical PCBs"; fab role on `fc_opcb_path` and `vcsel_pd_link`),
not in the registry. Author orgs "Information and Communications University" (Daejeon) and "Korea Photonics Technology
Institute" are also absent from the registry (not used as fab; for the header batches).

## watanabe2013 (1 component, 9 metrics)

| component_id | class | metrics |
|---|---|---|
| cmp_lit_watanabe2013_lpw_fanin_19core | fiber_interface.fan_out, polymer | 9: LPW-to-MCF coupling loss 0.2-1.8 dB over 19 cores (author_estimate, per_facet, loss_breakdown), insertion loss about 9.4-20.4 dB over 19 cores (Fig. 4 read, scope unspecified), crosstalk > 40 dB (sum from all neighbors), MCF MFD 9.56-9.85 um and core spacing 35.0 um (specification), 19 channels, core 7.9 x 7.9 um (derived), footprint 32 x 18 mm (derived) |

Not entered: per-core spot sizes of Table I (wx 6.5-10.6 um, wy 4.0-7.8 um; registry gap below); per-core Fig. 4 /
Fig. 5 values beyond the range and bound; design index contrast 0.4 %, 20 mm S-bend radius, theoretical bend loss
< 1e-3 dB (no fitting fiber_interface parameter; notes); max offset 2.8 / 1.1 um (notes). Abstract "< 2.0 dB" is the
same quantity as the 0.2-1.8 dB row.
Fab / facility: empty (passive fabrication sentences; authors at Yokohama National University and NTT Advanced
Technology Corporation). Furukawa Electric supplied the MCF and NTT-AT makes the E3765 epoxy: material / fiber
suppliers, in notes (D428). NTT Advanced Technology Corporation is not in the registry (author org only).

## Judgment calls

- (a) shang2015 0.167 dB per crossing kept as printed, `measured`, method `cutback`, with a conflict note: the Fig. 6(b)
  cascade slope reads about 0.07 dB per crossing (D417, D567 no-division-shown precedent).
- (b) shang2015 crossing siblings (60 deg at 500 / 700 / 900 nm, 90 deg at 500 nm) entered only with their Fig. 6(d)
  crosstalk reads; no per-crossing loss derived for them because the paper's normalization is unclear (a).
- (c) shang2015 heater: three `design` rows for the simulated 2 / 5 / 8 um overcladding designs (P_pi read at
  Delta phi = pi, `simulated`), not `fabricated`: heaters exist on the chip but the fabricated overcladding is not
  stated, so no design can be tied to it (D80e not applicable to a specific design).
- (d) shang2015 fab UC Davis + facility Marvell only; "Devices were fabricated in" the two facilities could also make
  UC Berkeley a fab org (D448), but I followed the fu2023 precedent (same group, same facility pair).
- (e) shang2015 vertical-coupler and crossing rows carry 1550 nm `wavelength_inferred` (the abstract list closes with
  "at 1550 nm wavelength"); the 52 dB crosstalk row is stated at 1550 nm.
- (f) shang2015 star circuits as `splitter.other` with `il_nonuniformity_db`; the 300 nm row's > 25 dB is attributed by
  the paper to the multilayer crossings, kept on that circuit row with the text-figure conflict noted.
- (g) zhao2019 PBS insertion losses scope `per_component`, method `unspecified` (normalization not described);
  simulated per-polarization values from p.5 entered, the abstract's shared "<= 1.33 dB" noted as a conflict.
- (h) hwang2007 in scope as fiber-coupled passive parts (D411, D80f; optical-PCB precedents dangel2013 / shi2023);
  VCSEL-to-fiber and fiber-to-PD interfaces classed `fiber_chip_coupler.other` with scope `per_coupler`; platform empty
  on all fiber rows (no planar stack, D422).
- (i) hwang2007 crosstalk > 53 dB `author_estimate` (no data, method or figure shown).
- (j) watanabe2013 coupling loss `author_estimate`: computed from measured spot sizes and offsets with an MCF MFD of
  unstated origin; scope `per_facet` (LPW facet to MCF butt joint).
- (k) watanabe2013 MCF MFD and core spacing as `specification` on the fan-out row (fiber the component is designed for;
  doerr2010 / bundalo2022 precedent), origin not stated in notes.

## Registry gaps

- `polarization`: no `gap_nm`, `radius_um`, `coupling_length_um` (zhao2019 PBS: gap 100 nm, R1 20 um, coupling length
  13.22 um, p.3-4 Sec. 2). Proposed: allow these geometry parameters for polarization (same definitions as splitter /
  resonator).
- `fiber_interface`: no device-side mode size (watanabe2013 Table I spot sizes wx 6.5-10.6 um, wy 4.0-7.8 um, p.2).
  Proposed: allow `mfd_chip_um` for fiber_interface ("MFD at the device facet", per axis in condition).
- Misalignment tolerance without a loss criterion (shang2015 400 nm lateral, 15 um longitudinal, p.7): no parameter;
  D49 rejected a generic tolerance, so no proposal beyond recording the values.
