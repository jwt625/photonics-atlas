# lit_132 batch report (distill, 2026-11-14)

Papers: chowdhury2022, wang2026h, zhang2026d, wang2026j, zhang2025e, perezarmenta2023. All six cached texts are the
source-row papers (page-1 titles match the `lit:` rows); none is a correction / erratum; no garbled text layer; no
supplement cached (wang2026h and zhang2026d cite Supporting Information that is not in the cache). Figure values were
checked on the page renders (chowdhury2022 p.2; wang2026h p.4-5; zhang2026d p.4-8; wang2026j p.7). Validation:
`merge_component_staging.py data/_staging/components/lit_132 --dry-run` -> +19 components, +110 metrics, 0 errors (the
one warning printed concerns merged row `cmp_lit_ni2025b_pimmwc`, not this batch).

## Per paper

| paper | components | metric rows | notes |
|---|---|---|---|
| chowdhury2022 | 1 | 29 | waveguide Ge/Si APD (OFC 2022, 3 pages); 24 of the rows are the printed Fig. 3(b) bandwidth labels (4 input powers x 6 biases) |
| wang2026h | 3 | 14 | all-Si tandem-microring PD, reference single-ring PD, GC (~6 dB per interface) |
| zhang2026d | 9 | 33 | hexagonal mesh (switch_fabric.mzi_mesh) + undercut TO phase shifter + gate MMI + 6 programmed functions (ring, 1x8 splitter, interleaver, coupled two-ring, Vernier, dual-injection), D396 |
| wang2026j | 5 | 17 | DTDC (switch_fabric.other), CMWG (reflector.bragg), CMWG-path propagation loss (waveguide_platform.other), MZS, mode (de)mux |
| zhang2025e | 0 | 0 | out of scope under D411 (see judgment call 1) |
| perezarmenta2023 | 1 | 17 | SWG-metamaterial polarization-insensitive 2x2 MMI (fabricated NMMI = 135 variant) |
| total | 19 | 110 | |

## Values deliberately not entered

- chowdhury2022: responsivity-bandwidth product 839.8 (A/W) GHz (p.1, Table 1; product of entered values, no
  parameter); Table 1 "lowest power" -35 dBm (DC sensitivity figure, no parameter); Fig. 2(b)-(c) curves without printed
  values; Table 1 other works (cited). GC (peak coupling at 1310 nm, p.1) has no performance value: no row. No avalanche
  gain printed.
- wang2026h: ring power coupling ratio ~0.09 (p.3; `power_coupling_pct` not allowed for photodetector, registry gap
  below); contact offset 750 nm (no parameter); RC-limited simulated bandwidth > 100 GHz (circuit model, not the
  device bandwidth, p.6); pad / substrate / BOX circuit elements of Fig. 5(d) (Cp 14.68 fF, Cox 5.89 fF, Rsub 1097
  ohm, Lp 30 pH, Rp 2.4 ohm); simulated relative improvements (~70 % responsivity, ~33 % bandwidth, p.4); data rates
  128 Gb/s NRZ / 200 Gb/s PAM-4 (link results); theoretical 6-channel WDM with < -30 dB crosstalk (p.5); breakdown
  voltage (not printed); Table 1 other works.
- zhang2026d: group delay 5.5 ps per gate (no parameter; p.4, Table 1); 42 gates / 84 tuners (no gate-count
  parameter; in notes); three-channel add-drop multiplexer (Fig. 7: only programmed coupling set points k1 0.44 /
  k2 0.19 and unlabelled spectra; no row); coupled two-ring passband widths 3-9 GHz (0.1-0.3 FSR; width definition not
  stated, in condition); dual-injection FSR 0.75 nm (stated as the expected value that "matches" the measurement, p.8);
  distance between the two phase shifters 100 um (no parameter); DC-replacement estimate (23 um DC, 60 um shorter gate,
  p.9); Table 1 other meshes (cited); MMI width (not stated).
- wang2026j: dispersion 0-49.72 ps/nm, step 1.60 ps/nm, group delay up to 1304 ps (42.06 ps per CMWG), GDR +/-14.70 ps
  (1.14 %) (p.6-7; no parameters, registry gap below); simulated 1.74 ps/nm, 0-53.94 ps/nm, GDR +/-0.48 / +/-1.02 ps
  (p.3-5); thermal shift ~0.2 nm per 10 deg C of 10 CMWGs (p.6, Fig. 5(d); `thermal_drift_pm_per_k` not allowed for
  reflector); corrugation depth 250 nm, apodization ratio 0.10, width variation 400 nm (no parameters; notes); mode-mux
  segment widths / gaps / taper lengths (gap_nm not allowed for mode_converter; three taper segments not mapped to one
  `taper_length_um`; notes); maximum power 6 P0 (formula only); "ultra-low" excess loss of MZS and mode mux (no
  number); design sweeps (200 / 600 nm width variation, 150 / 350 nm corrugation, tooth shapes); earlier SOI values
  (cited).
- perezarmenta2023: footprint 3.5 x 47.25 um (abstract / conclusion) - it equals the nominal NMMI = 129 length (32.25 um)
  plus two 30-period tapers, not the measured NMMI = 135 device (D159, notes); nominal NMMI = 129 design (3D FDTD
  field plots only, no number); Table 1 tolerance period counts; hole size 100 nm (no parameter); test-MZI FSR 5 / 7 nm.
- zhang2025e: everything (see judgment call 1). Values that would apply if the coordinator overrules D411: loaded Q
  about 3.2e7 near 1064 nm, undercoupled (p.3-4, Fig. 4(b)); cascaded OPO threshold 32.7 mW at 36 C (p.1 abstract),
  single OPO1 threshold about 4.32 mW (21.6 mW on the prism face, coupling efficiency about 19.6 %, p.4); total
  conversion efficiencies 11.5 % (36 C, 58.9 mW effective), 12.6 % (28 C, 62.4 mW), 9.2 % (4802.9 nm cascade);
  idler efficiency 4.7 % (36 C) / 3.2 % (28 C) (p.4-5); major / minor radius about 2 / 0.3 mm (p.3); 3-inch z-cut CLT
  wafer, 500 um, poled with M1 = 450 / M2 = 410 domain patterns (p.3).

## Missing fab / facility orgs

None missing. Used: `org_imec` (zhang2026d, all 9 rows: "fabricated in IMEC's iSiPP200 process", p.2 / p.9),
`org_sitri` (wang2026j, all 5 rows: fabricated "by Shanghai Industrial uTechnology Research Institute (SITRI)", p.5-6).
Fab left empty: chowdhury2022 (passive "fabricated in a standard 12-inch wafer", no org named; all authors at
GlobalFoundries, D80b / Contract v7), wang2026h ("a commercial foundry", p.4, no org), perezarmenta2023 (passive, EBL,
no org; authors at Universidad de Malaga and NRC Canada). No facility statements in any of the six papers.

## Judgment calls (for the audit)

1. zhang2025e: 0 rows. The resonator is a mm-scale crystalline whispering-gallery disk ground and polished from a
   diced 3-inch CLT wafer (major radius about 2 mm, minor radius 0.3 mm, glued to a brass rod, prism-coupled with free-
   space optics; p.3 Sec. 3, p.4 Fig. 4(a)). D411 puts "a discrete bulk (mm-scale polished crystalline) resonator" out
   of scope (tebeneva2024 precedent), although the dispatch note listed the "OPO resonator" as in scope. Values for a
   possible overrule are listed above (frequency_converter.other would be the class; platform `other`).
2. chowdhury2022: fab empty although every author is at GlobalFoundries (D80b). `process_name` holds only the cited
   platform "(45CLO, ref. 2 cited ...)" because p.1 says the APD uses the same Si device layer as ref. 2, whose title
   names 45CLO; the body never names the process. Fig. 3(b) labels entered as `measured` (printed numbers, series tied by
   legend colour; the -23 dBm / -5 V label reproduces the printed 32.3 GHz and the -15 dBm series the Fig. 3(a) text
   values). Responsivity `ref_plane on_chip` because the input power is quoted "at the APD" (p.1); the GC
   de-embedding method is not stated. Subtype `apd`, platform `soi` (Ge on the Si device layer over BOX).
3. wang2026h: subtype `photodetector.other` (all-Si sub-bandgap PAT + avalanche in a Si PN ring; the paper also calls it
   a microring-based all-silicon APD, p.6), kramnik2024 precedent; `apd` is the alternative. Cj 8.4 fF / Rs 92.8 ohm
   entered from the Fig. 5(d) S11 fit as `measured` (D76 S11 fit), with the per-branch vs total ambiguity in the
   condition (two branches drawn, one value printed). Bandwidth row uses the Fig. 5(b) label 40.2 GHz (text ~40 GHz);
   reference ring 29.8 GHz (label; text ~30 GHz). Responsivity wavelength 1554.2 nm marked inferred (the paper's single
   measurement wavelength; peak wavelength not printed); ref_plane unspecified. GC platform empty (layer not stated).
4. zhang2026d: one mesh row (D158: gate characterized as part of the mesh -> `mzi_mesh`) carrying gate IL / ER / length,
   with the phase shifter, MMI and six programmed functions as separate rows (D396, perez2017 precedent). Gate IL 0.28
   dB `measured` (cascade-slope fit, D80a) and 0.27 dB `derived` (from Q, ring_extraction). Q 52 000 `derived`
   (lambda / FWHM, authors' arithmetic). MMI split 49.6 % `derived` (inferred by the authors from the ERs). Classes for
   programmed filters: coupled two-ring and Vernier `resonator.coupled_rings`, dual-injection `resonator.other`,
   interleaver `wdm.interleaver`, 1x8 tree `splitter.other` (D400: not channel filters in a WDM path); the
   `wdm.mrr` alternative applies to the coupled two-ring / Vernier band-pass filters. 1x8 IL 10 dB `measured` (approx,
   de_embedded vs the shunt waveguide) rests on "about -10 dB ... matches the measurement" plus Fig. 6(c); the -10 dB
   is also the authors' expected sum. Dual-injection 93 GHz rests on the abstract / discussion (no Fig. 11(c) label).
   p_pi spread "+/- 0.4" stored as `std` (statistic not defined). Gate ER single-gate sweeps have no printed wavelength
   (left empty, not required).
5. wang2026j: DTDC classed `switch_fabric.other` (roeloffzen2018 switched-delay precedent); CMWG `reflector.bragg`
   (li2023a precedent); the 0.22 dB/cm put on a `waveguide_platform.other` row (path loss inside the grating) with
   basis `derived` and method `loss_breakdown` ((14.01 - 8.55) dB / 24.8 cm = 0.220; the paper does not print the
   arithmetic and calls the value "estimated" in the abstract). The 26 nm operational bandwidth is entered on the CMWG
   row as `stopband_width_nm` (level not stated); the abstract assigns it to a single CMWG, p.6 to the fabricated
   DTDC. DTDC losses 14.01 / 8.55 dB scope `unspecified` (normalization of Fig. 5(e) not stated). MZS / mux wavelength
   spans 1530-1570 nm are the Fig. 5(b) / 5(c) axes (`wavelength_inferred`).
6. perezarmenta2023: extraction from unbalanced-MZI interferograms with a two-identical-MMI model entered as
   `measured` (halir2016 precedent; D80a would make model-parameter extraction `derived`); paper's IL (sum of both
   outputs) -> `excess_loss_db` (xu2023a precedent); taper length 7.5 um `derived` (30 periods x 250 nm, confirmed by the
   47.25 um footprint arithmetic); MMI length 33.75 um `derived` (135 x 250 nm).

## Registry gaps (skipped value + locator, proposed definition)

- `dispersion_ps_per_nm` (reflector, switch_fabric, waveguide_platform): wang2026j 1.60 ps/nm per CMWG, 49.72 ps/nm
  maximum (p.6-7); "group-delay dispersion of the device as reported (sign as printed)". Also `group_delay_ps`
  (wang2026j 1304 ps / 42.06 ps per CMWG; zhang2026d 5.5 ps per gate) and `group_delay_ripple_ps` (wang2026j +/-14.70
  ps). li2023a reported the same gap.
- `thermal_drift_pm_per_k` for reflector: wang2026j ~0.2 nm per 10 deg C (p.6, Fig. 5(d)).
- `power_coupling_pct` for photodetector (resonant PDs): wang2026h ring coupling ratio ~0.09 (p.3).
- `gap_nm` for mode_converter (also raised in D428): wang2026j mode-mux gaps 1.5 / 0.25 / 1.5 um (p.3).
- `responsivity_bandwidth_product` (photodetector): chowdhury2022 839.8 (A/W) GHz (p.1, Table 1); low priority
  (product of two entered values).
