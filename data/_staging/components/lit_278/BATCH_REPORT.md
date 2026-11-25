# Batch lit_278 report

Distilled 2026-11-25. Papers: lit:debevc2022, lit:ma2020, lit:lee2014a, lit:an2019, lit:shinobu2010. Page-1 titles
match the source rows (shinobu2010: repository copy of the Electronics Letters paper, 4 p, figures on pp.3-4).
Totals: 14 components, 57 metric rows. `merge_component_staging.py --dry-run`: 0 errors (2 pre-existing warnings in
other batches). Generator: scratchpad `lit_278/gen.py`.

## lit:debevc2022 (metamaterial-cladding PBS, 220 nm SOI) - 7 components / 36 metrics

| component | kind | metrics |
|---|---|---|
| pbs2_70nm (PBS-2 as fabricated, 70 nm min. feature) | fabricated | per_db > 30 measured (1450-1590 nm, both pol.), IL < 2 dB measured (de-referenced to GCs, authors' bracketed value), simulated ER 33 dB / IL < 1 dB of the modified structure, length 82 um, width 500 nm, Si 220 nm, BOX 2 um |
| pbs2_100nm (100 nm min. feature variant) | fabricated | Table 1 only: ER_exp 32, IL_exp < 2, ER_sim 34, length 108 um |
| pbs2_design (50 nm design) | design | FDTD IL_TE < 0.4 (1200-1700), IL_TM < 1 (1356-1656), ER_TE > 35 (1200-1642), ER_TM > 35 (1379-1680), length 82 um, width, thickness |
| pbs1_design | design | FDTD IL_TE < 0.4, IL_TM < 1 (1481-1644), ER_TE > 35 (1200-1667), ER_TM > 35 (1462-1693), width, thickness |
| te_polarizer_design (bent metamaterial TE polarizer) | design | FDTD IL_TE < 0.4 (1200-1700), ER_TM 17-28 dB |
| swg_gc_te / swg_gc_tm (I/O grating couplers) | fabricated | peak coupling loss 5.92 dB at 1540 (5 deg) / 4.60 dB at 1500 (12 deg) TE; 14.55 dB at 1557 (5 deg) / 8.05 dB at 1500 (12 deg) TM; centre wavelengths |

Fab: org_applied_nanotools (p.11 Sec. 4 "at Applied Nanotools"; p.15 acknowledgment "for fabrication of the devices
using the NanoSOI Fabrication Service"), process_name "Applied Nanotools NanoSOI Fabrication Service (100 keV EBL,
ICP-RIE, single etch)". No facility.

Not entered:
- Measured BW "at least 140 nm" (ER > 30 dB) and simulated BW 263 / 163 / 273 / 229 nm (IL < 1 dB and ER > 35 dB):
  no registry parameter for a combined IL / ER criterion bandwidth; the wavelength ranges sit on the per_db / IL rows.
- Measured per-port transmissions TE Thru > -1.5 dB, TM Cross > -1.3 dB (p.12-13): kept in the IL note; the paper
  says IL was not accurately determined (normalized transmission exceeds 0 dB, up to +1.3 dB) and summarizes IL as
  "most likely below 2 dB", which is the entered value.
- Leakage relative to input (TE Cross < -32 dB, TM Thru < -33 dB measured; simulated -30 / -34 / -52 dB): D424
  (wrong-input leakage is not per_db; no crosstalk_db for polarization).
- Table 1 sim values of the "70 nm" row (35 dB / 263 nm / IL 1) equal the unmodified 50 nm design, whereas Sec. 4
  gives 33 dB / 273 nm for the modified structure: entered on the design row from the text; inconsistency noted on
  the fabricated row.
- Partial-structure TMM results (PBS-1 ER > 15 dB over 58 nm, > 35 dB over 10 nm; PBS-2 IL < 1 dB over 342 nm, ER about
  15 dB) and coupling lengths (TM 12.6 um, TE > 2.3 mm): notes only (sub-structures, no component of their own).
- Geometry without a registry parameter on polarization rows: SWG period P 150 / 300 nm, fill factor 0.55 / 0.53,
  N, Wgap 518 nm, L1 / L2 / phi, R_dL 20 um, Rp 2.5 um, straight DC 8.23 um (notes).
- Table 1 comparison rows [14]-[53]: other works (rule 3).

Judgment calls:
- Fabricated PBS-2 and its unmodified FDTD design are separate rows (the fabricated design differs: ff 0.53, polarizer
  ff 0.23-0.76, N 9); the polarizer is a design row because its simulated values belong to the unmodified design.
- IL entered as the paper's summary bound (< 2 dB, measured, scope per_component, excludes GCs), not the per-port
  readings.
- GC losses: scope / method unspecified (the paper does not say how the per-coupler peak was isolated); fiber tilt in
  condition, not as fiber_angle_deg (tilt was a measurement setting chosen per wavelength band).
- pbs2_100nm IL wavelength range inferred from the 70 nm measurement (same laser, BW_exp > 140 nm); its curves are in
  Supplement 1 (not cached).

## lit:ma2020 (automated control algorithms, SOI polarization receiver) - 1 component / 2 metrics

- pol_receiver (polarization.compensator, soi): extinction_db >= 30 (output over feedback port after automated
  control, p.7 Fig. 6(b)), pdl_db about 1.5 derived (from the fitted BER curves of states 1 and 4, p.8 Fig. 7(a)).
- Fab: org_astar_ime ("fabricated using 193 nm optical lithography at the Institute of Microelectronics (IME),
  Singapore", p.6) + org_cmc_microsystems ("providing access to the fabrication", p.11; D83d / D398). process_name as
  printed.
- Not entered: iterations to convergence (GLD 19, GD 6, B-B GD 3, ISTM 1; no registry parameter); BER levels
  (system); input PER ~15 dB of the setup; PSR / adiabatic coupler / phase shifter / edge coupler values (none stated;
  designs cited refs. [24], [25]).
- Judgment calls: PDL basis `derived` (extracted from the authors' own fits, D80a), band unspecified (no wavelength
  anywhere in the text; EDFA in the setup not used to infer a band, rule 8); the 30 dB ratio stored as extinction_db
  (port on / off ratio after adaptation, not a PER of a polarizer).

## lit:lee2014a (resonant-grating GMR polarizers) - 0 components / 0 metrics (stopped on scope)

Free-space guided-mode-resonance polarizers: 5 x 5 mm grating films (Si3N4 / TiO2 on glass, Si on patterned quartz)
illuminated by a collimated supercontinuum beam at normal incidence, transmission measured with an OSA (p.6-7). No
waveguide, no fiber I/O. Left out under D411 / D642 (integrated / chip-scale parts and fiber-coupled passive parts;
free-space parts without fiber I/O out). Candidate values if the coordinator rules them in (all from the authors' own
measurement / RCWA):
- PECVD Si3N4 (p.7-8, Fig. 8): TE resonance ~1565 nm, T_TM ~97 %, T_TE ~2 %; AFM period 1017 nm, grating 310 nm, d2
  260 nm, F 0.42 (design 1006 / 324 / 270 nm, 0.43); design ~4 nm BW, theoretical ER ~7e6 at 1550 nm (p.2-3, Fig. 1).
- Sputtered Si3N4 (p.8-9, Fig. 9): resonance ~1584 nm, ER 160:1 at 1584 nm, T > 95 % / < 3 % over ~1580-1589 nm (the
  text swaps TE / TM in this sentence, p.8); period 1021 nm, d1 302, d2 155 nm, F 0.45; design ~9 nm BW, ER ~4e6
  (Table 1 p.4: 1550.6 nm, 9.1 nm).
- TiO2 (p.9-10, Fig. 11): resonance ~1711 nm, T_TM ~86 %, T_TE ~1 %; SEM period 974 nm, d1 238 nm, d2 150 nm; design
  ~17 nm BW, ER ~2.9e5.
- Si on quartz (p.10-11, Fig. 12): T_TM > 97 % over ~1445-1700 nm, T_TE < 3 % over ~1415-1572 nm, overlap ~130 nm
  (~1445-1575 nm), resonance ~1499 nm, ER 360:1 at 1499 nm; SEM d1 117 nm, d3 88 nm; design ~200 nm BW, ER ~2.5e4.
- No fabrication org or facility stated (process described in first person / passive, authors at UT Arlington,
  Stanford, Sikorsky, Clemson).

## lit:an2019 (InP polarization controller, QCSE + plasmonic eigenmode rotation) - 3 components / 10 metrics

- pol_controller (polarization.compensator, inp): device loss about 5.5 dB (scope unspecified), length 510 um, core
  width 1.1 um, core height 634 nm.
- ps1_rotated (phase_shifter.other): Vpi 2.7 V (TE input, bias -2.7 V) and 2.3 V (right-circular elliptical input),
  length 240 um, Au-via partial etch 150 nm.
- ps2_normal (phase_shifter.other): phase_shift_pi 2 at -1.95 V, length 240 um.
- Wavelength 1550 nm (ECL 1.55 um, p.7), temperature 298.15 K (TEC "25 degree", p.8).
- Fab empty: process described in the passive voice, no org named, both authors at ETRI (D80b). No facility.
- Not entered: "operation loss is below -2 dB" (p.9; not defined); simulated eigenmode rotation angle and eigenmode
  propagation-loss maps (Fig. 3; no parameter, contour maps only); -14 V of the earlier device (ref. [20], rule 3);
  ridge height ~2.3 um SEM (not stated as an etch depth); Au-via lateral shift 290 nm design / ~240 nm SEM (no
  parameter, notes).
- Judgment calls: the QCSE phase shifters are entered as phase_shifter.other (gagino2024 InP EO phase-shifter
  precedent) because they are elements of a polarization controller, not modulators; the coordinator may prefer to
  list them for the EO atlas instead (question 2). The phase is the relative (birefringent) phase between eigenmodes,
  noted on both rows. v_pi_v stored as a magnitude with the reverse bias in bias_v.

## lit:shinobu2010 (low-loss elliptical-taper Si wire intersection) - 3 components / 9 metrics

- ellipse_crossing_ntt (crossing.other, fabricated, EB writing): mean 0.24 dB per crossing by cutback (N 5-30, 1550
  nm, TE), FDTD 0.23 dB, wire 400 x 220 nm.
- ellipse_crossing_ime (crossing.other, fabricated, IME optical lithography): lowest 0.12 dB measured (cutback), FDTD
  0.14 dB for the optimum a 3.60 / b 1.00 / x 5.36 um, < 0.1 dB FDTD with end-point smoothing. Fab org_astar_ime.
- simple_crossing (design): 1.2 dB loss, 11.5 dB crosstalk, author_estimate (introduction, no citation, origin not
  stated).
- Not entered: 0.4 dB elliptical taper (ref. [1]) and 0.14 dB double-etch crossing (ref. [4]) - cited (rule 3);
  13 um FP cavity length (inferred with a cited group index); 50 um intersection period (test-pair spacing, not a
  pitch); 1.50-1.63 um broadband statement (no number).
- Judgment calls: the IME device is identified with the FDTD optimum ("the optimally designed structure"), dimensions
  not restated for it; the NTT-ATN row is the a = 5.67 um sample (Fig. 2 caption says a = 5.76 um, noted); subtype
  crossing.other (elliptical taper expander, not an MMI design in the paper's terms; bogaerts2007 precedent).

## Missing fab / facility orgs

- NTT-ATN (printed "foundry service NTT-ATN"), lit:shinobu2010 p.1, fab role for cmp_lit_shinobu2010_ellipse_crossing_ntt.
  No registry row or alias (org_ntt is the parent group, not this foundry service; not mapped).

## Registry gaps

- Criterion bandwidth for polarization devices (e.g. `pol_bw_nm`: full width over which the stated ER / IL criterion
  holds, criterion in condition): debevc2022 measured >= 140 nm (ER > 30 dB, p.13) and simulated 263 / 163 / 273 /
  229 nm (IL < 1 dB and ER > 35 dB, p.11, p.14 Table 1).
- Geometry on polarization rows: subwavelength_period_nm, fill_factor, gap_nm, coupling_length_um,
  min_bend_radius_um not allowed for `polarization` (debevc2022 P 150 nm, ff 0.53, Wgap 518 nm, straight DC 8.23 um,
  Rp 2.5 um).
- Iterations to convergence of a control loop (ma2020 GLD 19 / GD 6 / B-B GD 3 / ISTM 1, p.7): low priority, single
  source.

## Coordinator questions

1. lee2014a: free-space GMR polarizers (no waveguide, no fiber) left at 0 rows under D411 / D642. Recommendation: keep
   0 rows; if ruled in, the candidate values above map to a new polarization subtype or micro_optics.other.
2. an2019: QCSE PIN phase shifters of the polarization controller entered as phase_shifter.other with Vpi / 2 pi
   values. Recommendation: keep (gagino2024 precedent; they are not modulators); optionally list as an EO-atlas
   candidate.
