# lit_197 batch report

Distilled 2026-11-18. Papers: lit:wang2018c, lit:zamek2011, lit:zheng2017, lit:chung2023 (page-1 titles match the
source rows). Totals: 13 components, 82 metric rows. Validation: `merge_component_staging.py
data/_staging/components/lit_197 --dry-run` -> +13 components, +82 metrics, 0 errors (the one warning printed concerns
merged row cmp_lit_ni2025b_pimmwc-m18, not this batch).

## lit:wang2018c (1 component / 15 metrics)

- `cmp_lit_wang2018c_pi_mode_evolution_3db` (splitter.adiabatic, soi, fab org_applied_nanotools): measured TE / TM
  imbalance as figure reads of the port difference of the Fig. 8(b) / 8(d) K curves (PDF vector data), simulated TE / TM
  imbalance from the FDTD curves, Table 2 IL < 1 dB (as excess_loss_db) and PDL ~1 dB (both author_estimate), 9 design
  dimensions (Table 1, p.8 stack).
- Not entered: printed "3 +/- 0.6 dB, i.e., a power imbalance of 1.2 dB" (TE) and "3 +/- 0.1 dB, i.e., 0.2 dB" (TM)
  as imbalance_db (split deviations, D401 / D454 wang2016a precedent; kept in component notes; the curves give a port
  difference up to about 1.30 / 0.19 dB). Table 2 bandwidth "100 nm" (no criterion stated; equals the TE sweep range).
  Simulated segment ILs Figs. 2-6 (sub-section design sweeps). Table 2 rows of refs. 24-26 (cited work, rule 3).
- Fab / facility: "fabricated using electron beam lithography at Applied Nanotools Inc" (p.8) -> org_applied_nanotools
  (in the registry). process_name "Applied Nanotools electron beam lithography" (printed wording). No missing orgs.

## lit:zamek2011 (2 components / 22 metrics)

- `cmp_lit_zamek2011_au_mirror_fp_resonator` (resonator.photonic_crystal = Fabry-Perot cavity, soi_strip): measured FSR
  ~21 nm and ER ~10 dB; fabricated-device Q0 900 / QC 360 / total Q 260 and IL ~0.7 dB (author_estimate: model values,
  extraction not shown); design Q0 2100, QC ~300, ER ~20 dB, group index 4.27 (simulated); geometry incl. Lc = 7.5 um
  from the Fig. 5(a) label.
- `cmp_lit_zamek2011_au_waveguide_mirror` (reflector.other): Au plug mirror, R = 0.9 simulated (W = 400 nm) and R ~0.8
  attributed to the fabricated mirrors (author_estimate); width / thickness.
- Not entered: coupling coefficient kappa 1400 cm^-1 (design) / ~1200 cm^-1 (fabricated) (no resonator parameter, see
  registry gaps); Fig. 3(b) reflectance sweep values for other widths (0.78 at W = 280 nm, 0.95 / 0.975 limits); mirror
  tilt ~7 deg and roughness ~10 nm (notes); 2D FEM check parameters (p.4-p.5, normalized, generic model).
- Fab / facility: first-person fabrication sequence (p.7) with all authors at UCSD -> fab
  org_university_of_california_san_diego; "The fabrication was performed at UCSB Nanofab and UCSD Nano3 facilities"
  (p.9) -> facility org_ucsb_nanofabrication_facility.
- Missing org: "UCSD Nano3" (facility, lit:zamek2011 p.9 Acknowledgements; both rows). Not mapped to the registry's
  San Diego Nanotechnology Infrastructure (later successor; D80d time-correct rule).

## lit:zheng2017 (7 components / 30 metrics)

- `cmp_lit_zheng2017_fano_mrr_slm_fp` (resonator.other, coupled system): measured Fano ER 23.22 dB maximum (1.8 mW) and
  11.20-17.65 dB range (0-0.9 mW); simulated maximum 24.17 dB.
- `cmp_lit_zheng2017_eit_overcoupled_design` (resonator.other, row_kind design): simulated EIT-like ER 12.69 dB and FWHM
  0.031 nm (over-coupled t1 = 0.90, not fabricated).
- `cmp_lit_zheng2017_mrr_heater` (resonator.ring): Q ~7600 and FSR ~9.5 nm (author_estimate, origin not stated),
  heater tuning 233.5 pm/mW (derived from printed 0.2335 nm/mW), 3.6 nm over 0-16 mW, power coupling 1.32 % (derived
  from the fitted t1 = 0.9934), model nMRR 4.05, geometry.
- `cmp_lit_zheng2017_slm_fp_cavity` (resonator.photonic_crystal): measured FSR ("channel spacing") 2.04 nm, linewidth
  59 pm (derived from 0.059 nm), Q ~26000 (derived), cavity length 39.62 um.
- `cmp_lit_zheng2017_slm_dc` (splitter.directional_coupler): bar split 46.24 % (derived from fitted t = 0.68), coupling
  length 13.5 um.
- `cmp_lit_zheng2017_fan_gc` (fiber_chip_coupler.grating): ~12 dB vertical coupling loss (scope unspecified), 70 nm etch.
- `cmp_lit_zheng2017_si_strip_wg` (waveguide_platform.straight): model loss 10.16 dB/cm and ng 4.2 (author_estimate).
- Not entered: Fano slope rates 252 dB/nm and 179.4 dB/nm (no parameter, registry gap). SLM "reflection ~0.95" (power vs
  field not stated, no measurement; in notes; so no reflector row). Fitted loss factors a1 = 0.97, a2 = 0.99, alpha =
  0.9923 (notes; converting alpha to a ring loss would rest on an unprinted length convention). Simulated Fig. 2(c),(d) /
  3(c),(d) alpha t2 sweeps. Values of refs. 15-17 (rule 3).
- Fab / facility: passive "fabricated by the electron beam lithography (EBL) and inductively coupled plasma (ICP)
  etching" (p.7), no org -> fab empty (D80b); no facility named. No missing orgs.

## lit:chung2023 (3 components / 15 metrics)

- `cmp_lit_chung2023_mpae_pi_3db` (splitter.adiabatic, soi): maximum-deviation bar split TE 44 % at 1270 nm and TM 56 %
  at 1295 nm (bar / cross order confirmed on Fig. 6), imbalance <= 1.05 dB per polarization (derived), polarization-
  independent 3 +/- 0.5 dB bandwidth > 70 nm in bw_1db_nm with the criterion in the condition (chen2022a precedent),
  8 design dimensions.
- `cmp_lit_chung2023_te_gc`, `cmp_lit_chung2023_tm_gc` (fiber_chip_coupler.grating): 3.93 / 4.14 dB per coupler.
- Not entered: insertion / excess loss of the coupler (not reported; spectra normalized); simulated L = 63 um linear
  reference design (no performance value); MPAE weights (design-method parameters).
- Fab / facility: "MPW foundry service on an 8-inch SOI wafer ... ArF 193-nm DUV" (p.4) + "chip fabrication support
  provided by Taiwan Semiconductor Research Institute (TSRI)" (p.5) -> fab org_taiwan_semiconductor_research_institute
  (D398 / hung2020); foundry not named. process_name as printed. No missing orgs.

## Judgment calls

- (a) wang2018c: printed "power imbalance 1.2 / 0.2 dB" treated as split deviations (D401 / D454); imbalance_db holds the
  vector-read port difference ranges 0.43-1.30 dB (TE) and 0.05-0.19 dB (TM). Table 2 "IL < 1 dB" stored as
  excess_loss_db, author_estimate (no IL measurement described).
- (b) zamek2011: fabricated Q0 900 / QC 360 / Q 260 and IL 0.7 dB author_estimate (model values with attributed R ~0.8
  and kappa ~1200 cm^-1; no fit shown; D403); abstract's "exhibits Q0 ~2100" kept as the simulated design value with a
  conflict note (D417). Fab = UCSD by the first-person fabrication sequence; UCSB Nanofab as facility only (D634: a
  facility's owner is not fab).
- (c) zamek2011: Au mirror given its own reflector.other row (fabricated, simulated R 0.9 + author_estimate R ~0.8);
  FP resonator classed resonator.photonic_crystal (registry definition includes Fabry-Perot cavities).
- (d) zheng2017: coupled system split into parts (D396): Fano system resonator.other (arianfard2020 precedent), MRR
  resonator.ring (D400), SLM FP cavity resonator.photonic_crystal (wu2018 precedent), SLM coupler splitter, GC,
  waveguide; EIT over-coupled case as a design row.
- (e) zheng2017: the 11.20-17.65 dB ER set entered as one range row (heater 0-0.9 mW, wavelengths 1529.829-1530.016 nm),
  per-step pairing only in notes; split ratio and power coupling derived from the fitted field coefficients (D80a).
- (f) zheng2017: the 12 dB "vertical coupling loss" scope unspecified (per coupler vs pair not stated); MRR Q 7600 and
  FSR 9.5 nm author_estimate (origin not stated).
- (g) chung2023: GC "a pair of grating couplers having a coupler efficiency of -3.93/-4.14 dB for the TE and TM
  polarizations" read as per-coupler values of the TE and TM designs (scope per_coupler, measured, D167); wavelength
  1270-1340 nm inferred.
- (h) chung2023: bw_1db_nm 70 with qualifier gt from "over 70 nm" (p.2), criterion 3 +/- 0.5 dB in the condition.

## Registry gaps

- Fano / resonance slope rate (dB/nm): zheng2017 252 dB/nm (0-0.9 mW) and 179.4 dB/nm (1.8 mW), p.7 Sec. 4. Proposed
  `slope_rate_db_per_nm` (resonator, wdm): maximum spectral slope of a resonance line shape as stated.
- Split deviation (D401 open item): wang2018c 3 +/- 0.6 dB (TE) / 3 +/- 0.1 dB (TM), p.9; chung2023 3 +/- 0.5 dB, p.5.
  Proposed `split_deviation_db` (splitter): largest deviation of a port transmission from the ideal split, +/- value.
- Waveguide-resonator coupling coefficient (cm^-1) on resonators: zamek2011 1400 cm^-1 design / ~1200 cm^-1 fabricated,
  p.7-p.8 (kappa_per_cm allows reflector, laser, wdm only). Proposed widening of `kappa_per_cm` to resonator (coupling
  coefficient between bus and resonator waveguides, design or fitted in condition).
