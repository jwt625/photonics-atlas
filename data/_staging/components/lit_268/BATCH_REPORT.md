# lit_268 batch report

Papers: lit:bucio2019, lit:chrysostomidis2025, lit:frigg2019, lit:tsuchizawa2003. Page-1 titles match the source
rows; no garbled text layer. Total 21 components / 108 metric rows. `merge_component_staging.py --dry-run`:
+21 components, +108 metrics, 0 errors (two pre-existing warnings on other batches: cmp_lit_guo2024a_exc02,
cmp_lit_ni2025b_pimmwc). verified_on 2026-11-24.

## lit:bucio2019 (7 components / 28 metrics)

Invited review of the group's own SiN platform (JSTQE 2020). Values attributed to the authors' earlier papers are
out (D259 / D408); what is left is what this paper reports without attribution.

- `cmp_lit_bucio2019_iammi_8ch` (wdm.other, 10 metrics): 8-channel interleaved AMMI, ~9.8 nm spacing, 8.0 nm 3-dB BW,
  XT ~12-20 dB (type not stated), IL ~3.5 dB (scope unspecified, O band inferred), non-uniformity ~0.5 dB,
  ~20 pm/K, 8 channels, footprint 0.06 x 3.00 mm2 (Table V, derived), W_MDW 18 um and Wa 7.5 um (Table IV).
- `cmp_lit_bucio2019_mzi_interleaver` (wdm.interleaver, 3): stand-alone MZI, mean FSR 19.6 nm, 15 pm/K, dL 46 um.
- `cmp_lit_bucio2019_gst_mzi_switch` (switch_fabric.other, 4): 5 um GST patch MZI, ER 10.7 dB at 1295 nm,
  5.5 dB IL relative to the amorphous state, 700 x 600 nm arms.
- `cmp_lit_bucio2019_sirich_wg_w700` (waveguide_platform.straight, 4): 1 dB/cm (Fabry-Perot method), 700 x 700 nm,
  10 mm.
- `cmp_lit_bucio2019_sirich_linear_taper` (fiber_chip_coupler.edge, 1): 6 dB per facet to tapered fibres.
- `cmp_lit_bucio2019_nrich_2um_air` / `_sio2` (waveguide_platform.straight, 3 each): 3.0 / ~1.5 dB/cm cut-back at
  2 um (wavelength inferred from the design wavelength), 1000 nm SiN, 3 um BOX.

Not entered:
- Sec. II-A: NH3-free PECVD losses < 1 dB/cm (1310 nm) and ~1.2 dB/cm (1550 nm), Fig. 3: the text sentence and the
  Fig. 3 caption cite ref. [19] (authors' 2017 J. Phys. D paper). Table I prints the same 1000 x 300 nm row (1.20 /
  1.00 dB/cm) marked "*This work" (p.3). Judged a restatement (D259 / D408: the value sentence attributes it to [19]);
  see question 1.
- Sec. II-B: Fig. 4 width-dependent losses (approaching 1.5 dB/cm, Layer 03 ~6 dB/cm): caption "Figure taken from
  [28]". Table III Im(gamma) and Fig. 6 Re(gamma): method cited to [28], and no registry parameter.
- Stand-alone 4-channel AMMIs (IL ~1.0-1.5 dB, 3-dB BW 11 +/- 0.5 nm, XT 15-30 dB, 114 pm/nm, 18 pm/C; p.5): Table V
  lists this device as "AMMI [37]" (the authors' 2018 paper) with the same values; IAMMI row has no citation (entered).
- Sec. V photonic crystals (all values): the section opens with "we employed this material for the fabrication of
  PhC waveguides [48] and high-Q PhC microcavities [49], [50]" (Debnath 2017 x2, Clementi 2019, own group), the W1
  values are introduced as "was reported", the cavity design is "our PhC cavities [49]" and the harmonic part is a
  "brief review". Out: W1 ng > 110 (> 100 dB/cm), ng 37 at 53 dB/cm, 4.6 dB/cm at ng 7.4 over > 70 nm (p.8);
  A1 cavity simulated Q 520,000 and V 0.77 (lambda/n)^3, measured intrinsic Q 71,000-122,000 (p.8, Fig. 12(c)); HG
  cavity Q 12,000, coupling efficiency 30 %, rho_SH 4.7e-7 /W, rho_TH 5.9e-5 /W^2 (p.8). See question 2.
- MZI-interleaver 1x2 / 2x2 MMIs: "optimised ... IL < 0.1 dB" (simulated design statement for both, no geometry).
- Wavelength converter: Re(gamma) 12.5 /W/m, conversion efficiency -24 dB, flat conversion bandwidth 40 nm, BER
  power penalty < 1 dB (no parameters); dispersion design values.
- Fig. 16 inset "800 nm" on the 2 um waveguide ridge (text says a 1000 nm layer; role unclear).
- Table V rows of other works.

Fab / facility: fabrication in passive voice throughout; no org named, no facility; fab empty on all rows (D80b).

## lit:chrysostomidis2025 (6 components / 27 metrics)

Si3N4 MZIs with hybrid Si3N4/BTO EO phase shifters. EO metrics are left to the EO atlas (rule 2); the paper is not in
`../eo-modulator-atlas/data/devices.csv`.

- `cmp_lit_chrysostomidis2025_sin_bto_transition_atl70` (waveguide_platform.transition, bto_on_sin, 7 metrics):
  1.55 dB per interface at 1550 nm (author_estimate: paper's arithmetic on the cut-back intercept 3.54 dB minus two
  nominal 0.22 dB PDK MMIs, waveguide loss neglected), ATL 70 um, Winp 2 um, Wout 500 nm, BTO 220 nm, Si3N4 800 nm,
  100 nm SiO2 interlayer.
- `cmp_lit_chrysostomidis2025_sin_bto_transition_atl90` (7): simulated 1.65 dB (3D-FDTD, TE; 1.66 dB at the
  Fig. 3(c) plateau), same geometry with ATL 90 um (fabricated as MZI3, D80e).
- `cmp_lit_chrysostomidis2025_ps_hybrid_w500` (waveguide_platform.straight, 5): 5.4 dB/cm derived from the printed
  0.54 dB/mm cut-back slope (MZI A-E), simulated 5.7 dB/cm (0.57 dB/mm), 500 nm Si3N4 / 800 nm / BTO 220 nm.
- `cmp_lit_chrysostomidis2025_ps_hybrid_w700` (4): simulated 0.7 dB/cm (0.07 dB/mm), 700 nm width (MZI5, MZI6).
- `cmp_lit_chrysostomidis2025_mmi_1x2` (splitter.mmi, 3): Ligentec PDK 1x2 MMI, nominal 0.22 dB (specification,
  chen2024 PDK precedent), process_name "Ligentec PDK".
- `cmp_lit_chrysostomidis2025_ssc` (fiber_chip_coupler.edge, 1): 6.7 dB fiber-to-fiber of the 5 mm reference
  waveguide (PMF in, SMF out) at 1550 nm.

Not entered:
- EO-atlas candidates (phase shifter / MZI): Vpi x L 2.52 V mm (MZI1, -0.8 to +2.8 V, ER 25 dB; MZID at 9.2-10.4 V),
  2.93 / 2.94 V mm (MZI2), 3.36 (MZI3), 3.64 (MZI4, MZI6), 3.92 V mm (MZI5) (Tables II-III, p.7-8); ER > 27 dB
  (abstract), > 18 dB all MZIs; 121 nW per pi (MZI2, Table IV, p.9); rise / fall < 20 ns with 5 MHz pulses
  (instrument-limited, p.10); r_eff 783 / 542 pm/V (p.8; the conclusion attributes 783 pm/V to MZI4, Sec. III-E to
  MZI1); coercive field 6.75-9.25 kV/cm (p.8); MZI IL at 1550 nm 4.65 / 4.05 / 4.51 / 4.43 / 3.5 / 4.2 dB (MZI1-6),
  minima 3.57 / 3.00 / 3.42 / 3.6 dB near 1510-1514 nm (p.6-8); TM +6.6 dB loss and ER 5 dB (p.9).
- "Interface < 1.3 dB near 1510 nm" for MZI1-4 (p.6): one statement for four ATL designs (D254), in component notes.
- Fig. 3 parametric simulations (end-fire 1.52 dB at 2 um, < 1.3 dB beyond 5 um; adiabatic taper 0.096-0.56 dB;
  1.61 dB at Winp 5 um; 1.52 dB at Wout 700 nm / ATL 90 um, not fabricated): design curves (shoji2002 precedent).
- Sec. IV second-generation BTO-rib design (0.18 dB per interface, 0.1 dB/mm, < 0.95 / 0.47 dB total MZI loss): not
  fabricated, values are design projections; could be `row_kind design` rows if wanted (question 4).
- Facet ripple 0.2 dB with 0.115 nm FSR (no parameter).

Fab / facility: "Ligentec S.A. and Lumiphase fabricated eleven MZIs" (p.5) -> org_ligentec;org_lumiphase on all six
rows (both in the registry). The sentence covers the whole MZI chip, so the pure-SiN rows (MMI, SSC) also carry
Lumiphase (question 3). No facility.

## lit:frigg2019 (5 components / 41 metrics)

- `cmp_lit_frigg2019_film_as_deposited` / `_film_annealed` (waveguide_platform.other, 3 each): prism-coupler slab
  loss 1 dB/cm as deposited and 0.25 dB/cm after the 400 C anneal at 1550 nm, 400 nm film, 3 um BOX.
- `cmp_lit_frigg2019_ring_sm_w1000_r90` (resonator.ring, 16): Q_loaded 1.71e5 and FWHM 9.1 pm at 1553 nm, FSR
  2.14 nm, extinction 6.78 dB (derived from T0 = 0.21), Q_int 2.33e5 (1553 nm) and 2.68e5 (1580 nm), losses 1.5
  (1550, Table 1), 1.3 (1580, introduction) and worst case <= 3.1 dB/cm (1510-1600 nm), ng 1.93, geometry.
- `cmp_lit_frigg2019_ring_mm_w2000_r90` (resonator.ring, 16): Q_int 4.18e5 (1548) and 5.81e5 (1579), widths 5.0 /
  4.3 pm (figure labels), FSR 2.12 nm, losses 0.8 (1550), 0.6 (1580), 0.62 (1550-1600), 1.4 (1510-1550), worst case
  <= 2.1 dB/cm, ng 2.00, geometry.
- `cmp_lit_frigg2019_inverse_taper` (fiber_chip_coupler.edge, 2): mean 3 dB per facet to lensed fibres, 300 nm tip.

Not entered: Table 1 rows of other works; film refractive index, roughness Rq 1.2 nm, stress -25 MPa, uniformity
+/- 0.5 % (no parameters); Fig. 6 point-by-point losses / Q_int (only the printed summary values entered); rings
R = 30 / 60 / 120 um (no values).

Fab / facility: fab empty: "we also fabricated microring resonators" (p.2), authors at RMIT University, ANU and Evatec
(first author at RMIT and Evatec), not an unambiguous org (D80b). Missing facility orgs (acknowledgment, p.9):
- "Micro Nano Research Facility (MNRF)" at RMIT University: facility (use acknowledged).
- "Australian Microscopy & Microanalysis Research Facility at RMIT University": facility (use acknowledged).
- "Melbourne Centre for Nanofabrication (MCN) in the Victorian Node of the Australian National Fabrication Facility
  (ANFF)": facility ("This work was performed in part at"); ANFF is the network owner (D82c, not a facility).
- RMIT University itself is also not in the registry (only needed if the coordinator rules fab = RMIT, question 6).
Evatec (org_evatec, equipment vendor of the sputter tool; two Evatec co-authors) is not a fab org.

## lit:tsuchizawa2003 (3 components / 12 metrics)

- `cmp_lit_tsuchizawa2003_si_wire_conventional` / `_improved` / `_oxidized` (waveguide_platform.straight, soi,
  4 each): 60 / 13 / 6 dB/cm at 1.55 um (improved and oxidized by cut-back over 3.5-16 mm, Fig. 5), 300 nm square
  target, 3 um BOX. Text layer drops "dB" ("60 &/cm", "6 &/cm"); values confirmed on the page-2 render labels.

Not entered:
- Polymer spot-size converter (60 nm Si tip, 3 x 3 um polymer core, 300 um taper region in Fig. 1): no loss printed.
  The Fig. 5 zero-length intercept would give the converter-pair loss, but the scanned figure's y tick labels sit
  about half a division below the gridlines, so the intercept reads either ~9.6 or ~12 dB (D156); geometry-only, not
  a row.
- Fig. 6 bend loss (24 x 90 deg bends): "no bend-related loss" at R >= 5 um (no number); the per-bend loss at 2 um
  would need the same ambiguous axis. Sidewall roughness ~20 nm / <= 5 nm (no parameter, in labels).

Fab: org_ntt (D72): "we fabricated smooth-sidewall Si wire waveguides" (p.1), all authors at "NTT Microsystem
Integration Laboratories" (p.1). This printed lab name is not in `org_aliases.csv` (alias gap only; org_ntt is the
registry org, shoji2002 precedent). No facility.

## Judgment calls for the auditor

1. bucio2019 NH3-free PECVD loss (Table I "*This work", 1.20 dB/cm at 1550 / 1.00 dB/cm at 1310 nm, 1000 x 300 nm):
   excluded because the text and Fig. 3 caption cite ref. [19]. Recommendation: keep out (D259 / D408); if the
   Table I label is taken as this paper's own claim, enter as author_estimate per D80i.
2. bucio2019 Sec. V PhC values excluded as a review of refs [48]-[50]. Fig. 12(c) itself carries no "taken from"
   label (unlike Fig. 4), so the measured intrinsic Q 71,000-122,000 is the most borderline item.
3. chrysostomidis2025: Lumiphase on the SiN-only MMI and SSC rows (literal reading of the fab sentence) vs
   Ligentec only (the MMI is "from Ligentec's PDK").
4. chrysostomidis2025: 1.55 dB interface loss as author_estimate (nominal PDK MMI loss as input) rather than
   derived; 1.65 dB simulated value placed on the 90 um ATL row, not on the measured 70 um row.
5. frigg2019: all Q_int and ring losses author_estimate (D403): Eq. (1) assumes under-coupling; the paper asserts
   "slightly under-coupled" for the single-mode ring without showing how it was determined. Single-mode loss at
   1580 nm entered as 1.3 dB/cm (introduction, with its Q_int) although Table 1 prints 1.1 dB/cm (conflict noted).
   Printed ng 1.93 does not reproduce from FSR 2.14 nm, R 90 um, 1553 nm (about 1.99; note only).
6. frigg2019 fab left empty although the acknowledgment names RMIT facilities and five of seven authors are at RMIT.
7. tsuchizawa2003 three process variants as three rows (west2019 film precedent); platform soi (SOI wafer stated,
   etch depth not stated, so not soi_strip).
8. bucio2019 2 um waveguide: air- and SiO2-clad states as two rows (cladding differs) with wavelength 2000 nm
   inferred from the design wavelength.

## Registry gaps (value skipped, locator, proposed definition)

- `nonlinear_parameter_per_w_m` (waveguide_platform): bucio2019 Re(gamma) 12.5 /W/m at 1550 nm (p.6 Sec. IV,
  Fig. 10(a)); "real part of the waveguide nonlinear parameter gamma (Kerr), /W/m, method in condition".
- `fwm_conversion_efficiency_db` (frequency_converter): bucio2019 -24 dB at 26 dBm coupled pump (p.7, Fig. 11(a));
  "idler-to-signal power ratio at the waveguide output, dB as printed (negative), pump power in condition".
- `conversion_bandwidth_nm` (frequency_converter): bucio2019 flat over 40 nm (p.6, Fig. 10(b)); "detuning span with
  flat (criterion in condition) conversion efficiency".
- `channel_wavelength_sensitivity_pm_per_nm` (wdm): bucio2019 stand-alone AMMI 114 pm/nm (p.5; out under D259 here,
  also the bucio2017 gap): "channel-wavelength shift per nm of a dimension error, dimension in condition".
- `free_space_coupling_efficiency_pct` for resonator (bucio2019 eta_c 30 %, out under D259 here): only if Sec. V is
  ruled in.
