# lit_206 batch report

Distilled 2026-11-18. Papers: lit:yanikgonul2022, lit:okimoto2023, lit:yuan2021, lit:cao2023 (all photodetector APD
papers; page-1 titles match the source rows; IEEE download stamp ignored). Validation:
`merge_component_staging.py data/_staging/components/lit_206 --dry-run` -> +24 components, +168 metrics, 0 errors,
no warnings on these rows. Reverse bias is stored negative throughout (yanikgonul2022 and okimoto2023 print positive
reverse-bias values; noted on the rows).

| paper | components | metric rows |
|---|---|---|
| yanikgonul2022 | 14 | 116 |
| okimoto2023 | 4 | 15 |
| yuan2021 | 4 | 16 |
| cao2023 | 2 | 21 |
| total | 24 | 168 |

## yanikgonul2022 (JLT 2023, SiN-on-SOI APDs at 850 nm, AMF)

Components: 9 APD design variants (W 1.1 / 1.3 / 1.5 um x L 100 / 300 / 500 um, Table I), the 220 nm slab baseline
APD (App. B), SiN inverse-taper edge coupler, 400 nm SiN routing waveguide, nitrogen-rich 250 nm SiN waveguide
(App. C), SiN routing to SiN-on-rib transition (simulated loss only).

- Table I (p.3, page render): per variant dark current, responsivity, gain, 3-dB bandwidth, GBP at VB = 0.9 Vbr; plus
  layout geometry (L, W, 150 nm rib, 90 nm slab, 60 nm etch). Dark current printed in uA -> nA `derived`, except 3 / 8
  nA which p.6 prints in nA (`measured`, D256).
- Text-only values: 18.6 GHz at 15 V (W1.1 L100), "up to 18 GHz" (W1.1 L300), "around 13 GHz" (W1.5 L300),
  responsivity > 1.0 A/W near breakdown for all 300 um variations, 75.2 / 18.5 mA/W primary responsivity at 4 V
  (rib vs slab), edge coupler 7.00 dB/facet (cutback) and the "expected" 6.0-7.6 dB, SiN loss 11.05 and 0.36 dB/cm,
  transition < 0.01 / < 0.03 dB (simulated).
- Not entered: conclusion "120 GHz with G 10.9, 11.0 GHz at VB = 37 V" for "L = 100 um and L = 1.3 um" (p.6)
  conflicts with p.5 / Fig. 5(b) (W 1.1, L 300) and Table I (D159; the p.5 "120 Gbps" bound is entered on W1.1 L300
  with the conflict in notes); gain "up to 20 near breakdown" (Fig. 2(c); bias not printed, avalanche_gain needs bias);
  per-device breakdown voltages (only VB = 0.9 Vbr printed; not back-computed); unity-gain voltage 2.4-4.4 V (no
  parameter); Fig. 8 simulated absorption vs taper end width (no parameter); P_in 0.57 mW (measurement input);
  related-work values in Table I rows [29], [31], [32] and p.2 (cited, rule 3); eye diagrams / SNR (no parameter).
- Fab: org_amf on all chip rows ("fabricated using the standard MPW flow of Advanced Micro Foundry (AMF)", p.3);
  process_name "AMF standard MPW flow, PECVD SiN-on-SOI platform". The nitrogen-rich SiN waveguide has no fab
  statement: fab empty. No facility.

## okimoto2023 (JLT 2024, InP butt-joint waveguide APDs, Sumitomo)

Components: InP-multiplication BJ APD (Sec. III-A device, also Fig. 8-10), C-band-SSC APD, O-band-SSC APD,
AlInAs-multiplication BJ APD.

- Entered: Vbreak 21.6 V, 1.9 nA at 0.9 Vbreak, 0.72 A/W at 9 V (unity gain), max M = 68, 21 GHz at M = 3.3, MB
  product 173 GHz (fit, `derived`), Vbreak at 55 / 85 C read off Fig. 9, chip 500 x 550 um footprint (`derived`);
  0.84 A/W at 1550 nm and > 0.75 A/W over about 1510-1610 nm (C-band SSC); 0.69 A/W at 1310 nm (O-band SSC);
  AlInAs device Vbreak at 25 / 55 / 85 C read off Fig. 9.
- Not entered: AlInAs MB product 265 GHz and 38 GHz at M = 4 (the device sentence cites the authors' own OFC 2022
  paper, ref. [24], and the Fig. 5 legend cites ref. [14]; D259 / D408); PDL < 0.05 dB on both SSC APDs (pdl_db not
  allowed on photodetector, as caillaud2021 / runge2015); Vbreak temperature coefficients 23.3 and 11.7 mV/K (no
  parameter); linearity (< 1 dB photocurrent degradation below -4 dBm, 1.5 dB at 0 dBm, 17 V; the paper defines no
  saturation power); aging (18 APDs, 5000 h at 175 C, Vbreak drift < 0.5 V, dark-current increase < 0.5 nA);
  ROSA sensitivity -22.9 dBm (module level); O-band Fig. 6(b) spectrum (only the 1310 nm value printed).
- Fab: empty (see judgment call (c)).

## yuan2021 (JSTQE 2022, Si-Ge waveguide APD with loop reflector, HPE)

Components: loop-reflector (LR) APD, Normal APD (no reflector), SOI loop reflector, 1550 nm TM grating coupler.

- Entered: LR 1.12 A/W and IQE 89.6 % at -3.6 V, gain about 23.6, about 25 GHz, GBP about 296 GHz (asymptote) and
  about 497 GHz (gain 19.4), Ge 400 nm, mesa area 40 um2, 220 nm Si; Normal 0.75 A/W, IQE 60 % at -3.0 V; loop
  reflector simulated 85.5 % at 1550 nm TM and the 1280-1600 nm simulated span from Fig. 2(b); fiber + GC loss about
  15 dB.
- Responsivity / IQE rows are `author_estimate`: all powers are referenced to the waveguide by removing a fiber + GC
  loss of "~-15 dB" of unstated origin (D428 / D437 precedent).
- Not entered: impulse FWHM about 14.4 ps, Q-factor about 14, BER sensitivities -15.7 / -13.4 / -10.8 dBm (no
  parameter); arc radius 10 um and Y-branch D = 1 um (radius_um / min_bend_radius_um not allowed on reflector);
  dark current curve of Fig. 4(a) (no printed value); Normal / DBR APD BER and FWHM values from the authors' ref. [18]
  (D259); 1.49x ratio. 4 x 10 um mesa: which side is the length is not stated, so only the area is entered.
- Fab: empty (no fabrication statement; all authors Hewlett Packard Labs).

## cao2023 (ACP/POEM 2023, lateral reach-through Ge/Si APD, Zhejiang University)

Components: lateral reach-through APD, reference Ge/Si PD (no light-doped P region).

- Entered: dark current 310 nA at -11 V and 51 uA at -14 V, breakdown -14.5 V (100 uA criterion), maximum gains at
  -15 / -18 / -21 / -24 / -27 / -29 dBm, bandwidth > 40 GHz measured and about 45 GHz expected at -14 V, GBP 533 /
  918 / 1440 GHz, Ge 5 um x 500 nm x 260 nm, 220 nm Si, 150 nm slab, 70 nm etch; reference PD 0.93 A/W.
- GBP rows are `author_estimate`: each equals gain x the about 45 GHz bandwidth that lies beyond the VNA range
  (D435); at -21 dBm no bandwidth was measured at all.
- Not entered: dark current < 1 nA "at low voltage" (bias not printed); 100 uA at -14.5 V (kept as the breakdown
  criterion in the condition); about 20 GHz at low voltage (bias not printed); Wo 70 nm, Wp 150 nm (no parameter);
  eye diagrams (no parameter).
- Wavelength: the paper states operation at 1310 nm but never the measurement wavelength: 1310 nm with
  `wavelength_inferred: true`. Platform soi from the BOX labelled in Fig. 1(b) (D423 checked: the figure names a
  buried oxide). process_name "standard 180nm MPW silicon photonics foundry" as printed, fab empty (no org named).

## Judgment calls

- (a) yanikgonul2022 responsivities kept `measured` with `method: loss_breakdown`, `ref_plane: on_chip`: the paper
  prints them as its result, with P_in taken from its own measured cutback losses (not an assumed or cited term); gain
  and GBP `derived` (normalization to the 4 V unity-gain photocurrent; GBP computed by the authors, govdeli2025 /
  lin2022a precedent).
- (b) okimoto2023 AlInAs Fig. 5 values out (D259 / D408: attributed to the authors' ref. [24] in the text and ref.
  [14] in the legend); its Fig. 9 breakdown points kept (no attribution), so the AlInAs row exists with Fig. 9 reads
  only.
- (c) okimoto2023 fab empty: first-person "we have fabricated", but authors at Sumitomo Electric Industries and
  Sumitomo Electric Device Innovations, two registry orgs with no parent link (D72 "unambiguous own org" not met).
  If the coordinator treats SEDI as a unit of SEI (D154 analogue), fab = org_sumitomo_electric_industries on all 4
  rows.
- (d) Two avalanche_gain rows carry a bias read off the figure because the parameter requires a bias and the text
  gives none: okimoto2023 M = 68 (about -21.4 V, Fig. 4) and yuan2021 about 23.6 (about -10.1 V, Fig. 4(a)); the
  reading uncertainty is in notes. Drop the rows if figure-read conditions are not acceptable.
- (e) okimoto2023 Sec. III-A device, C-band-SSC device and O-band-SSC device kept as three rows: the paper does not
  say whether the Sec. III-A device is the C-band one (0.72 vs 0.84 A/W at 1550 nm, different input powers).
- (f) cao2023 0.93 A/W put on a separate reference-PD row (p.2 says it was measured on the reference PD), although
  the abstract / intro phrase it as the APD's unity-gain responsivity; gain rows use bias -14.5 V from the text
  ("around -14.5V"), the abstract's -14 V is noted.
- (g) yanikgonul2022 W1.1 L300 "120 Gbps" entered as gbp_ghz 120 `le` (unit slip, Fig. 5(b) confirms GHz and the
  device), conclusion's conflicting attribution in notes on both candidate rows.

## Missing fab / facility orgs

None missing: org_amf exists. Sumitomo entities exist (org_sumitomo_electric_industries,
org_sumitomo_electric_device_innovations); registry gap: no parent link between them (okimoto2023 p.1 affiliations),
relevant to judgment call (c).

## Registry gaps (skipped value + locator, proposed definition)

- `pdl_db` on photodetector: okimoto2023 PDL < 0.05 dB at 1310 / 1550 nm (p.5, Fig. 7). Proposal: allow pdl_db for
  photodetector ("responsivity difference between TE and TM input, positive dB").
- `breakdown_temp_coeff_mv_per_k` (photodetector): okimoto2023 23.3 mV/K (InP) and 11.7 mV/K (AlInAs) (p.5, Fig. 9).
  Proposal: "temperature coefficient of the breakdown voltage, mV/K, temperature range in condition".
- `radius_um` or `min_bend_radius_um` on reflector: yuan2021 loop-reflector arc radius 10 um (p.2). Proposal: allow
  min_bend_radius_um (or radius_um) for reflector.loop_mirror.
- Photodetector linearity / compression point as printed: okimoto2023 < 1 dB degradation below -4 dBm at 17 V (p.5,
  Fig. 8). Proposal: `compression_1db_input_dbm` ("input power at 1-dB photocurrent compression as stated").
