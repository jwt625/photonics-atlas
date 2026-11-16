# lit_153 batch report

Distilled 2026-11-15 under the pic-component-distill skill (Contracts v4-v7, DevLog-007 D150-D588). Six papers
selected from benchmark-table citations; only values each paper reports itself are entered.
`merge_component_staging.py data/_staging/components/lit_153 --dry-run`: +47 components, +306 metrics, 0 errors
(the one warning printed is on merged row cmp_lit_ni2025b_pimmwc, not this batch).

Page-1 titles match the source rows for all six papers. No correction / erratum-only file (yi2022 is the corrected
version of the full paper, "Corrected 17 August 2022" on p.1). wang2024c text is the arXiv version of the Advanced
Photonics Research paper (D430). No garbled text layer flagged.

| paper | components | metrics |
|---|---|---|
| lit:wang2024c | 2 | 21 |
| lit:naghdi2016 | 22 | 111 |
| lit:yi2022 | 8 | 61 |
| lit:pathak2012a | 5 | 40 |
| lit:qiu2018 | 8 | 50 |
| lit:sciancalepore2014 | 2 | 23 |
| total | 47 | 306 |

## lit:wang2024c (8-channel TFLN AWG, PLACE)

- Rows: `awg_8ch` (wdm.awg, lnoi_rib, 20 metrics: on-chip IL 3.32 dB best and 3.1-6.2 dB range, adjacent > 7.01 dB /
  non-adjacent > 15 dB crosstalk, 8 measured channel centres, design spacing, simulated BPM IL 2.8-5.4 dB and > 10 dB
  crosstalk, AWG and stack geometry, footprint); `lensed_fiber_facet` (fiber_chip_coupler.edge, 8.67 dB, scope
  unspecified).
- Basis: on-chip IL `author_estimate` + `loss_breakdown` (coupling loss "calculated to be 8.67 dB", origin and
  per-facet basis not stated; D428).
- Not entered: "single-channel bandwidth" about 1.6 nm (definition not stated, equals the design spacing);
  "total-channel bandwidth" 12.8 nm and simulated operating range 12.8 nm (no parameter); centre-wavelength deviation
  within 0.3 nm from simulation; calculated effective index 1.75158.
- Printed conflicts (D417, in notes): adjacent crosstalk -7.01 dB (abstract, p.3) vs -7.1 dB (p.7); lowest channel
  loss 3.32 dB (p.7) vs conclusion range starting at 3.1 dB (p.9).
- Fab: empty. First-person "fabricate" sentences, but authors span East China Normal University (most authors),
  SIOM-CAS / UCAS and further affiliations of the corresponding author: own org not unambiguous (D72, D154). Candidate
  `org_east_china_normal_university` if the coordinator reads it otherwise. Wafer supplier NANOLN (Jinan Jingzheng
  Electronics Co. Ltd.) in notes only.

## lit:naghdi2016 (SWG contra-directional couplers)

- Rows: `swg_cdc_family` (array-level row, D165: IL "up to 1.2 dB at lambda_C for the devices" `le`, coupling
  coefficient 20-800 /cm read off Fig. 5(b), stack geometry); 16 per-device rows `cdc_lc<LC>_g<g>` of the period-378 nm
  series (3-dB bandwidth from Fig. 5(a), extinction from Fig. 6(a), gap / LC / period); 4 period-series rows
  `cdc_period366/372/388/398` (Table 1 measured and 3D-FDTD centre wavelengths); `vgc_test_pair`
  (fiber_chip_coupler.grating, 15 dB fiber-to-fiber, 30 nm FWHM).
- Printed values tied to devices: abstract 18.2 nm -> LC 200 um / g 100 nm (only curve at that value in Fig. 5(a));
  0.9 nm -> LC 400 um / g 500 nm (only LC plotted at 500 nm); > 35 dB codirectional suppression -> the Fig. 6(b)
  device (LC 200 um, g 250 nm). Table 1 period-378 nm device = the LC 400 / g 400 per-device row (same design).
- Figure reads: 30 rows `extracted_from_figure` (+/-0.3 nm bandwidth, +/-1 dB extinction, +/-15 % kappa). LC 400 um /
  g 150 nm: extinction from Fig. 3 only; no bandwidth (the paper excludes its FWHM from the study, p.8).
- Not entered: input-power reflection suppression about 15 dB (no back-reflection parameter for wdm); simulated
  -16 dB reflection and 200 nm span of the Fig. 2 design; "> 120 nm operating range" (no parameter); model
  (average-permittivity / average-index) centre wavelengths of Table 1; chip area 90 x 400 um (LC 50 um layout);
  SWG taper geometry (geometry-only, no performance metric).
- Fab `org_university_washington` ("fabricated by Richard Bojko at the University of Washington, Washington
  Nanofabrication Facility", p.10; p.4); facility empty: WNF missing in the registry (below).

## lit:yi2022 (2 um band flat-top cascaded-MZI demultiplexer)

- Rows: `cmzi_8ch_2um` (wdm.cascaded_mzi, soi_strip, 28 metrics: per-channel IL 0.68-0.89 dB and crosstalk > 20.65-22.65
  dB from Table 3, 1-dB 2.3 nm / 3-dB 3 nm widths, design spacing 3.2 nm, simulated crosstalk > 26.5 dB, total heater
  power 196.4 mW, geometry, footprint); `tin_heater` (phase_shifter.thermo_optic, 248 ohm mean); `gc_2um`
  (fiber_chip_coupler.grating, about 7 dB per facet, Fig. 5(e) 1-dB / 3-dB widths, period / duty / etch); five
  `dc_k50/k29/k20/k08/k04` directional-coupler rows (simulated cross-coupling at 1970 nm, FDTD coupling lengths, gap,
  width, bend radius; fabricated, D80e).
- Wavelength: channel wavelengths are not printed, only the 1955-1985 nm operating range: per-channel rows carry
  `band nir_above_u` with `wavelength_inferred` (rule 8). GC value at the Fig. 5(e) peak near 1996 nm (inferred).
- Scope: Table 3 IL `de_embedded`, method unspecified (spectra "normalized", reference not stated).
- Not entered: stopband width > 1.3 nm at the 15 dB extinction level (stopband_width_nm is reflector-only); per-heater
  powers (Table 2, in the condition); Table 4 footprint 1.9 mm2 (noted against 0.5 x 0.9 mm2 without electrodes);
  DC width-tolerance curves (Fig. 7, no printed value).
- Fab empty; `process_name` "commercial silicon photonics MPW, 248 nm DUV lithography, 180 nm node" (printed node,
  no foundry named; D536).

## lit:pathak2012a (12 x 400 GHz MMI-aperture flat-top Si AWG)

- Rows: `mmi_awg_12x400_56wg` (optimized device, 24 metrics: central-channel IL 3.29 dB measured and 2.07 dB
  simulated, IL non-uniformity 1.55 / 0.8 dB, mean spacing 391 GHz and design 400 GHz, 12 labelled channel centres,
  1-dB / 3-dB / 10-dB width spreads read off Fig. 15, geometry, footprint); four array-size siblings
  `mmi_awg_12x400_44wg / 47wg / 50wg / 53wg` (measured neighbouring-channel crosstalk read off Fig. 11: 8.8 / 12.5 /
  14.0 / 14.1 dB).
- Judgment call (coordinator question 1): measured crosstalk 17.0 dB and simulated 19.5 dB of the optimized device are
  NOT entered: the value sentence reads "a crosstalk of 17.0 dB [16]", [16] being the authors' own GFP 2011 paper with
  nearly the same title (D408 value-sentence clause; pathak2012 precedent D424). The loss and non-uniformity in the same
  sentence carry no citation, Fig. 13 / Fig. 11 captions cite nothing, and the abstract states 17.0 dB uncited, so a
  coordinator may prefer to keep it (D80i "clearly reports it as its own result": "Experimentally we find (Fig. 13)").
  If kept: crosstalk_adjacent_db 17.0, measured, p.5-6 Sec. V-C (the paper says it is set by the phase-error level).
- Not entered: aspect ratio (1-dB / 10-dB width) 0.52 measured, 0.49 / 0.33 simulated (no parameter); bandwidth
  non-uniformities 0.23 / 0.17 / 0.15 nm (covered by the range rows); grating-coupler efficiency about 30 % (cited
  ref. [15]); MMI-length series 13-19 um (qualitative only); normalized passband widths of Fig. 10(a) (no parameter).
- Fab empty: "fabricated through ePIXfab" (p.7) names an MPW access service, which is fab by D398, but ePIXfab is not
  in the registry (below). `process_name` "ePIXfab, 200 mm SOI, 193 nm deep UV lithography, double etch (220 nm /
  70 nm)". Platform `soi` (deep-etched wires plus shallow-etched star-coupler apertures).

## lit:qiu2018 (phase-apodized grating-assisted contra-DC filters)

- Rows: three fabricated single-stage contra-DCs (Fig. 5(a)-(c): IL, SLSR 17 / 18 / 16.8 dB from the text / figure
  labels, Fig. 5(a) centre 1572.8 nm and 3-dB 1 nm, geometry); `dual_stage_cdc` (IL 1.2 dB at 1542.5 nm, 0.6 dB per
  contra-DC `derived` from the paper's own halving, 3-dB 0.5 nm, SLSR 23 dB); `tiw_heater`
  (phase_shifter.thermo_optic, 17.2 pm/mW `derived` from the printed 58 mW/nm); three simulated design rows (Fig. 4,
  600 periods: SLSR > 28 / ~26 / ~31 dB, IL 5.7 / ~2 dB, kappa 5-48 /cm from Fig. 2).
- Judgment calls: abstract "single-stage ... 3-dB bandwidth of 0.9 nm and an SLSR of 18 dB" not entered (body gives
  1 nm for Fig. 5(a) and no 3-dB width for Fig. 5(b): device not identified, D159). Fig. 6 tuning is on a separate
  heater row because the tuned contra-DC is not identified while the heater design (4 x 1000 um Ti/W) is stated
  (coordinator question 2). Fig. 5(b) / (c) IL wavelengths read off the drop-band peaks (1570.7 / 1571.2 nm,
  inferred).
- Not entered: 17 / 18 / 16 / 20 dB bandwidths (2.4 / 2.2 / 1.7 / 0.8 nm; no parameter for a width at the SLSR level);
  corrugation widths dWA / dWB (no parameter; in labels and notes); local effective-index variation 1e-4 (Fig. 3).
- Fab empty (passive "were fabricated using electron-beam lithography on a standard commercial SOI wafer").

## lit:sciancalepore2014 (O-band echelle grating demultiplexers, CEA-LETI)

- Rows: `tpsg_eg` (wdm.eg, 20th order, 82 teeth: IL 3-3.8 dB, non-uniformity 0.8 dB, average isolation > 27 dB,
  spacing 800 GHz, geometry); `pcg_mmi_eg` (wdm.eg, 15th order with MMI input: IL 5-5.8 dB, 1-dB width 2.3 nm,
  crosstalk > 25 dB, MMI 8.1 x 3.1 um).
- Judgment call (D159): the wafer-level statistics over 25 dies (average crosstalk -30 dB, worst -22 dB, isolation
  22-47 dB, centre-wavelength dispersion 0.8 nm, Fig. 4) and the thermal coefficient about 60 pm/C of "the
  demonstrator" are not tied to the TPSG or the PCG design: in notes on both rows, not entered (coordinator
  question 3).
- Printed conflicts (D417, in notes): Si thickness 300 nm (abstract) vs 310 nm (p.3); TPSG IL 3-3.5 dB / uniformity
  0.7 dB (abstract) vs 3-3.8 dB / 0.8 dB (p.3).
- Not entered: Rowland radius 250 um (not an FPR length, D444) and the 2.5 um waveguide "distance" (gap vs pitch
  unstated); DBR facet fill factor 56 % (fill_factor not allowed for wdm); simulated flattening penalty 2-3 dB;
  TPSG-with-MMI curves of Fig. 3(b) (no printed values); grating-equation example angles and slab index.
- Fab empty ("CMOS 200-mm pilot lines processing tools" names no org, D80b / D433); `process_name` empty (description,
  D588). Vistec Electron Beam (co-author org, e-beam tool) is a note only.

## Missing fab / facility orgs (name as printed + locator)

- Washington Nanofabrication Facility (WNF), University of Washington: facility, lit:naghdi2016 p.4 Sec. 2 and p.10
  Acknowledgments (all 22 rows). Already reported in D579 / D586 as "Washington Nanofabrication Facility / Molecular
  Analysis Facility".
- ePIXfab: fab (MPW access service named for fabrication, D398), lit:pathak2012a p.7 Acknowledgment (all 5 rows).

## Registry gaps (skipped value + locator + proposed definition)

- `back_reflection_db` on wdm: naghdi2016 input reflection suppression about 15 dB (p.9-10), simulated -16 dB
  (p.5, Fig. 2). Definition as for couplers (reflection to the input port, positive dB below the input).
- Width at an SLSR / crosstalk level for wdm (e.g. `bw_20db_nm`, already a D443 candidate as bw_20db_ghz): qiu2018
  20-dB 0.8 nm (p.4), 17 / 18 / 16-dB widths 2.4 / 2.2 / 1.7 nm (p.3). Proposed: `bw_at_level_nm` with the level in
  the condition.
- Passband aspect ratio (1-dB / 10-dB width): pathak2012a 0.52 measured (p.7), 0.49 / 0.33 simulated (p.5); D443
  candidate `bw_ratio_1db_20db` is a sibling. Proposed `passband_aspect_ratio` (unit 1, levels in condition).
- `stopband_width_nm` on wdm: yi2022 suppressed-channel stopband > 1.3 nm at 15 dB extinction (p.7).
- `fill_factor` on wdm (DBR facets of echelle gratings): sciancalepore2014 56 % Si (p.3).
- Grating corrugation width (contra-DC / Bragg sidewall corrugation): qiu2018 dWA 20-30 nm, dWB 35-50 nm (p.2-4).
  Proposed `corrugation_width_nm` (geometry, wdm / reflector).

## Coordinator questions

1. pathak2012a: keep the measured 17.0 dB crosstalk out (D408 value-sentence clause, pathak2012 / D424) or enter it
   (uncited in the abstract, own Fig. 13 / Fig. 11)? Recommendation: keep out for consistency with D424, unless the
   GFP 2011 paper [16] is cached and shows a different device.
2. qiu2018: Fig. 6 tuning on the separate `phase_shifter.thermo_optic` heater row (identity of the tuned contra-DC not
   stated) vs not entered at all. Recommendation: keep the heater row (the heater design is stated and identical on
   every contra-DC).
3. sciancalepore2014: wafer statistics / thermal coefficient kept out by D159. Recommendation: keep out.
