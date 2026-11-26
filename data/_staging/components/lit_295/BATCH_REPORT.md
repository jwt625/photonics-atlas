# lit_295 batch report

Batch lit_295 (family F, DevLog-007 D780): lit:smit1996, lit:selvaraja2009, lit:selvaraja2009a. Distilled 2026-11-26
(verified_on). Totals: 9 components, 43 metric rows. Validation: `merge_component_staging.py
data/_staging/components/lit_295 --dry-run` -> +9 components, +43 metrics, errors 0 (the two warnings it prints are on
merged guo2024a / ni2025b rows, not this batch).

Page-1 title check: all three cached texts match their source rows (smit1996 "PHASAR-Based WDM-Devices: Principles,
Design and Applications", JSTQE 2(2) 1996; selvaraja2009 "Subnanometer Linewidth Uniformity ...", JSTQE 16(1) 2010
issue; selvaraja2009a "Fabrication of Photonic Wire and Crystal Circuits in Silicon-on-Insulator Using 193-nm Optical
Lithography", JLT 27(18) 2009). None is a correction or erratum. No garbled text layer; tables of selvaraja2009 read from
the page renders (Tables III / IV p.6-7).

## lit:smit1996 (invited tutorial / review of PHASAR (AWG) devices): 0 components, 0 metrics

The paper is a design tutorial plus literature overview; it reports no device of its own with a measured value.
Not entered:

- Every experimental number is credited to cited work (rules 1 / 3, D259): best semiconductor total loss "order of
  2 dB" [77] (p.3 Sec. II-C); 3 dB on-chip loss 8-channel receiver with 10 GHz per channel [77] (p.10 Sec. IV-B);
  MW-laser fiber power 0.15 mW [70], [73] (p.10); ADM fiber-to-fiber 3-4 dB / 6-8 dB (Tachikawa et al. [80], [82],
  [85], p.11); MMI-PHASAR footprint 2800 x 100 um2 [22] (p.12; ref. [22] is the second author's own ECIO'95 paper,
  D259 / D408); polarization-dispersion change 7-12 nm by strained MQW [98] (p.6); typical crosstalk "order of -25 dB"
  (InP) to "better than -30 dB" (silica) for PHASARs in the literature (p.5 Sec. II-E).
- "Recent experiments in our laboratory show crosstalk levels better than -30 dB also for good semiconductor devices"
  (p.5 Sec. II-E): own-lab statement with no device, design, wavelength or locator of a measurement; sample identity
  not determinable (D159), not entered.
- Analytical / design values for a generic PHASAR (not a component of this paper): 1-dB bandwidth 0.31 of the channel
  spacing (31 GHz at 100 GHz spacing, p.4 Sec. II-D), more than 65 % with multimode receivers (p.8), truncation
  crosstalk below -35 dB (p.4), outer-channel excess loss about 3 dB for routers (p.3, p.10), InGaAsP-InP polarization
  dispersion 4-5 nm (p.5, p.7). Figs. 2, 3, 9, 10 are calculated curves; Figs. 1, 4-8, 11-14 schematics.

Fab / facility orgs: none (no fabricated component). Registry gaps: none.

## lit:selvaraja2009 (uniformity of wavelength-selective SOI devices, 193 vs 248 nm lithography): 4 components, 24 metrics

| component | class | metrics |
|---|---|---|
| cmp_lit_selvaraja2009_rtr_r4 | resonator.ring | 8: wavelength_spread_nm 0.15 / 0.55 (within die, 25 / 1700 um, Table III), 1.3 / 1.8 (die-to-die, 10,000 / 20,000 um, Table IV); radius 4, coupling length 4 um, gap 180 nm, etch depth 220 nm (design) |
| cmp_lit_selvaraja2009_mzi_193nm | wdm.cascaded_mzi | 6: spread 0.2 / 0.6 (Table III), 1.08 / 1.73 (Table IV); 50 um delay, etch 220 nm |
| cmp_lit_selvaraja2009_mzi_248nm | wdm.cascaded_mzi | 3: average shift 0.7 / 7.3 nm (short / long distance, p.7, Fig. 14); 50 um delay (same mask) |
| cmp_lit_selvaraja2009_awg_8ch_400ghz | wdm.awg | 8: spread 0.54 / 0.52 (Table III, 275 / 770 um), 0.57 mean within die (text), 0.4 die-to-die std (Table IV, text); 8 channels, 400 GHz design spacing (author_estimate, D82a), footprint 7000 um2 (derived from 200 x 35), etch 220 nm |

Values not entered and why:

- "minimum variation of 20 pm (Fig. 11)" (p.6 Sec. VI-A): the sentence is about the MZIs 25 um apart, Fig. 11 shows two
  RTRs 25 um apart with a 0.02 nm label; device ambiguous (D159), noted on both rows.
- "<0.6 nm within chip", "<2 nm chip-to-chip" summaries (abstract, p.7, conclusion): pooled over device types; the
  per-type Table III / IV values are entered.
- Process metrology (Table I Si 219.1 nm mean / 2 nm std, BARC, resist; Table II and Figs. 6-7: 450 nm test-wire
  linewidth 0.45 % / 0.76 % std, +19 nm etch bias; Fig. 8 within-die linewidth): done on characterization wafers
  "before fabricating the devices" (p.3 Sec. IV); not a component metric and not tied to the device wafer (D159), noted
  in component notes.
- Simulated dNeff/dW 0.013 / nm, dNeff/dh 0.05 / nm, about 1 nm/nm and 2 nm/nm resonance shift (p.2, Figs. 1-2, from
  the authors' thesis ref. [10]): generic sensitivity, no registry parameter.
- AWG Fig. 12 normalized transmission (reference not stated) and Figs. 13 / 16 per-die wavelengths: figure-only, no
  stated insertion loss / crosstalk / center wavelength.
- Dose-compensation proposal (Figs. 17-18): process proposal, no device result.

Fab / facility orgs: fab empty on all 4 rows. The devices are "fabricated ... in a 200 mm CMOS fabrication facility"
(p.1) that is not named; all authors at the joint affiliation "Ghent University-Interuniversity Microelectronics Centre
(IMEC)" (p.1); the process details are cited to ref. [11] = lit:selvaraja2009a (p.3), which names the IMEC pilot line;
the acknowledgment (p.8) thanks people for discussions only. Missing org: none (org_imec exists; not set).

## lit:selvaraja2009a (193 nm lithography and etch process for SOI photonic wires and crystals): 5 components, 19 metrics

| component | class | metrics |
|---|---|---|
| cmp_lit_selvaraja2009a_wire_w500 | waveguide_platform.straight | 6: prop loss 2.7 dB/cm (+/- 0.06, fit over 0.5-5 cm and 50-550 bends, TE, band unspecified); width 500 nm, Si 220 nm, BOX 2 um, etch 220 nm (design); sidewall 82 deg (derived from printed 8 deg slope) |
| cmp_lit_selvaraja2009a_bend_r1 / _r2 / _r3 / _r5 | waveguide_platform.bend | 3 each: bend_loss_db_per_90 0.071 / 0.039 / 0.02 (Fig. 17 labels, extracted_from_figure) and 0.009 (R 5 um, conclusion + Fig. 17, measured); min_bend_radius_um; width 500 nm |

Values not entered and why:

- Abstract "0.013 dB/90 deg bend of 5 um radius" (p.1) conflicts with the conclusion (p.7) and the Fig. 17 label
  (0.009 dB/90 deg); 0.009 entered, the conflict noted on the R 5 um row.
- "maximum variation 0.2 dB/cm" for 450-500 nm wires (p.6): no per-width values; note on the wire row.
- Photonic crystals (pitch 300-550 nm, hole diameters, process windows 1 % / 2 %, OPE 5 nm vs 40 nm at 248 nm, mask
  bias 27 / 8 nm, Figs. 4-13, Tables I-II): lithography / geometry results with no optical performance; not rows (D49,
  rule 9). The 248 nm OPE of 40 nm is cited to Bogaerts et al. [2] (rule 3).
- Exposure latitude 5 % at 0.3 um depth of focus (p.4): process metric, no registry parameter.

Fab / facility orgs: fab org_imec on all 5 rows ("All our experiments were performed in the pilot-line of the advanced
microelectronics research facility of IMEC, Belgium", p.2 Sec. II, plus first-person fabrication p.6; D448). Facility
empty: the IMEC pilot line is imec's own line, no separate registry facility (owner is not a facility, D82c). Wafer
supplier SOITEC (UNIBOND) in notes only (org_soitec exists; supplier role, D428). Missing orgs: none.

## Judgment calls for the auditor

1. selvaraja2009 fab empty although its process is cited to selvaraja2009a, which places all experiments in the IMEC
   pilot line (D433 cited-process reading, bogaerts2007 / brouckaert2007 joint-affiliation precedent). Alternative:
   org_imec on the 193 nm rows via the companion paper; not done because the source itself names no place.
2. selvaraja2009 MZI class `wdm.cascaded_mzi` (bogaerts2010 uniformity-MZI precedent) and ring `resonator.ring`
   (D400 test ring). The 248 nm run is a separate row (different process, same mask); its 0.7 / 7.3 nm values are
   assigned to the MZI from the Fig. 14 caption, the text naming no device type.
3. Table III / IV "mean standard deviation of lambda_res" stored as statistic `std` with the averaging in condition;
   AWG text value 0.57 nm entered as a separate `mean` row beside the per-distance 0.54 / 0.52 nm table values.
4. 20 pm minimum variation not entered (text says MZI, figure shows RTRs; D159).
5. selvaraja2009a bend values at R 1 / 2 / 3 um from printed Fig. 17 data labels: `extracted_from_figure` with no
   reading uncertainty (selvaraja2014 label precedent); R 5 um `measured` (also printed in the conclusion).
6. No wavelength is stated for the selvaraja2009a loss values (broadband source; only a generic "1300 nm/1500 nm"
   telecom mention in the introduction): band `unspecified`, not inferred.
7. smit1996 0 rows (tutorial; own-lab crosstalk statement without a device, D159).

## Registry gaps

None needed for entered values. Candidates seen but not proposed (process-level, no component parameter):
linewidth uniformity (% std over wafer), lithography exposure latitude / process window, optical proximity effect (nm).
