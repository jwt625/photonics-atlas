# lit_223 batch report

Papers: lit:chen2015a, lit:suzuki2017, lit:yang2018b, lit:kashyap1993. Page-1 titles match the source rows (kashyap1993:
page 1 of the cached text opens with the end of the preceding paper in the issue, the listed letter follows on the same
page). verified_on 2026-11-20. Dry run of `merge_component_staging.py`: +19 components, +101 metrics, 0 errors; the one
warning names the merged row cmp_lit_ni2025b_pimmwc, not in this batch.

| paper | components | metric rows |
|---|---|---|
| chen2015a | 6 | 42 |
| suzuki2017 | 9 | 27 |
| yang2018b | 2 | 18 |
| kashyap1993 | 2 | 14 |

## chen2015a (Si hybrid PDM-WDM (de)multiplexer: bi-directional AWG + PBS + PR, Optics Express 2015)

Rows:
- `wdm.awg` hybrid demux (whole structure: PBC + PBS + PR + 10x10 bi-directional AWG): excess loss ~7 dB (central
  channel #6, ~1545 nm, both polarizations, de_embedded against a straight waveguide with grating couplers, measured);
  AWG share 5-6 dB (author_estimate, loss_breakdown); crosstalk ~13 dB as `crosstalk_db` (type not stated); 3-dB width
  ~1.16 nm; PDL ~0.1 dB at ~1530 nm and ~0.4 dB at ~1560 nm (author_estimate: "It is estimated" from the PBS / PR test
  data, arithmetic not shown); design spacing 3.2 nm / 400 GHz (author_estimate, D82a); design geometry (m = 30,
  dL 19.64 um, Ra 100 um, 300 nm arrayed-waveguide gap, 3.69 um output separation as `pitch_um`, 500 x 220 nm wire,
  PMMA 300 nm); footprint 530 x 210 um (derived).
- `polarization.pbs` bent-DC test PBS: TE through-port IL ~1 dB and PER ~10 dB over 1530-1580 nm; TM PER as high as
  20 dB at ~1575 nm (best); TM cross-port IL "almost zero" entered as a Fig. 5(b) read 0.2-0.5 dB
  (extracted_from_figure, +/- 0.2 dB); w1 / w2 widths, ~10 um length.
- `polarization.psr` cut-corner rotator (D404): IL < 1 dB at 1530-1550 nm and ~2 dB at > 1560 nm (TM in, TE out,
  normalized by a PBS with grating couplers); W 200 nm, I/O 500 nm, H 220 nm, Lc 22 um.
- `fiber_chip_coupler.grating` TE and TM: 4.5 / 5.0 dB per coupler at the peak (D167 measured), 3-dB widths ~45 / ~60 nm
  ("estimated", measured).
- `waveguide_platform.straight` 500 x 220 nm: ~2.2 dB/cm TE, ~1.6 dB/cm TM.

Not entered:
- AWG FSR printed "about 29μm" (p.4): the context (FSR > N x 3.2 nm) implies nm; unit misprint, left out.
- PR TM-to-TE conversion efficiency ~85 % and residual TM ~-8 dB relative to the input (p.8, p.10): no polarization
  conversion-efficiency parameter; the residual is input-referenced, not an output-port ratio (D424).
- PBS R1 20 um / R2 19.3 um, gap 205 nm, coupling length 5.39 um; PR cut-corner We 50 nm / He 70 nm and 10 um taper:
  no polarization parameter (registry gaps below; He role vs etch depth not stated).
- PBS siblings theta = 13 / 15 / 17 deg (Fig. 6): raw spectra, no printed values; theta of the Fig. 5 device not stated.
- Grating-coupler PER > 20 dB (cited to ref. [28], rule 3). Polarization-diversity-circuit excess 1-2 dB and TM-group
  < 1 dB / 1-2 dB (restatements of the PBS / PR results). AWG-part footprint 440 x 190 um. PDλ "nearly zero".

Fab / facility: empty. Passive fabrication sentences (p.5), all authors Zhejiang University (D80b); no facility
acknowledged (funding only).

## suzuki2017 (Si 8 x 8 double-MZ PILOSS switch, Optics Express 2017)

Rows (fab AIST on all 9):
- `switch_fabric.mzi_mesh` 8 x 8 PILOSS: fiber-to-fiber IL 11.2 dB mean (64 paths, 1535 nm, TM-like, measured);
  `il_nonuniformity_db` 1.7 dB (printed +/-0.85 dB, derived); on-chip 6.2 dB and switch fabric 3.2 dB (author_estimate,
  rest on the 2.5 dB/facet estimate); -20 dB crosstalk bandwidth > 30 nm and -30 dB bandwidth 17 nm (xt_bandwidth_nm,
  worst-case path 8-7'); minimum crosstalk ~38 dB near 1535 nm (Fig. 6(b) read, +/- 1 dB); total power ~0.8 W
  (author_estimate: 0.16 W term of unstated origin); 8 x 8 ports; footprint 1.7 x 7.7 mm (derived); 430 x 220 nm wire
  (unit rescales derived), 1.5 um over-cladding.
- `switch_fabric.mzi_mesh` polarization-diversity assembly (two chips + fiber PBSs): PDL ~0.5 dB at 1525-1550 nm
  (summary "less than 0.5 dB", Fig. 8(a) traces exceed 0.5 dB beyond 1550 nm; D417 note).
- `switch_fabric.other` double-MZ element: cross-state -30 dB crosstalk bandwidth > 40 nm.
- `phase_shifter.thermo_optic` TiN heater: P_pi ~40 mW (C band inferred), 10-90 % switching time ~30 us, heater gap
  1.5 um.
- `switch_fabric.other` single MZ switch 0.2 dB, `crossing.other` DC intersection 0.1 dB, `polarization.other`
  polarization cleaner 0.2 dB, `waveguide_platform.straight` routing waveguide 1.4 dB per side: all loss-budget terms,
  author_estimate.
- `fiber_chip_coupler.edge` inverse taper: 2.5 dB per facet (author_estimate: "estimated", no reference structure or
  arithmetic named), tip 150 nm (derived), 100 um taper, fiber MFD 4.5 um (specification).

Not entered:
- C-band loss wavelength dependence "less than 3 dB" (wdl_db not allowed on switch_fabric). DGD < 8 ps of the
  polarization-diversity switch (dgd_ps not allowed on switch_fabric). Projected 20 mW TE design. +/-0.65 / +/-0.2 dB
  shares of the IL variation (authors' attribution). 32-Gbaud DP-QPSK WDM results (no parameter).

Fab / facility: fab AIST from "We fabricated and characterized" (abstract, all authors AIST) plus the acknowledgment
"device fabrication was supported by the TIA Super Clean-Room of AIST" (D84a / D448; suzuki2018 precedent, D666).
`process_name` "300-mm SOI, CMOS process line with immersion ArF scanner" (printed wording, suzuki2018 form).
Missing facility org: "TIA Super Clean-Room of AIST" (facility, p.9 Acknowledgments; already queued in D453 / D666).

## yang2018b (polarization-insensitive Si MZI switch, Optics Express 2018)

Rows:
- `switch_fabric.other` (D158) 2x2 TO MZI switch, platform `soi_strip` ("All the silicon patterns are fully etched",
  p.3): P_pi 14.57 mW TE / 14.85 mW TM at 1550 nm (printed reads of Fig. 6(a), measured); extinction ~20 dB at 1550 nm
  (power sweep) and ~15 dB in the C band at Ph 4.2 / 18.2 mW; IL ~2.5 dB (grating couplers and PBSs normalized out,
  method unspecified); simulated ER > 25 dB and IL < 0.6 dB over the C band (row_kind fabricated, D80e); 2 x 2 ports;
  120 um heated delay-line length, 380 nm delay-line width, 340 nm Si, 2 um BOX, ~700 nm oxide (derived).
- `waveguide_platform.straight` delay line: simulated DGD ~40 fs (0.04 ps, simulated, D83f) for 120 um.

Not entered:
- MMI 3-dB coupler (win 750 nm, gap 500 nm, wmmi 2.0 um, Lmmi 15.5 um): only simulated curves, no printed splitter
  value apart from a DGD of ~25 fs (dgd_ps not allowed on splitter): geometry-only, no row.
- Whole-MZI DGD < 100 fs (dgd_ps not allowed on switch_fabric); ideal-coupler ER > 45 dB for wd 360-400 nm; dn_eff/dT
  difference within 0.4 %; on-chip bent-DC PBSs and grating couplers (no values).

Fab / facility: empty (passive "is then fabricated", authors at South China Normal University and Sun Yat-sen
University; D80b). No facility acknowledged.

## kashyap1993 (laser-trimmed four-port MZI-Bragg bandpass filter, Ge:silica, IEEE PTL 1993)

Rows:
- `wdm.bragg_cdc` four-port filter, platform `ge_silica`: fiber-to-fiber IL Port 1 -> 3 1.35 dB (C band inferred);
  looped-through Port 2 bandpass 58.8 % after / 24.6 % before trimming (fiber-referenced) and 80.3 % / 28.9 % relative
  to the total output (`drop_efficiency_pct`, Table I); Port 3 bandstop rejection 13.5 dB before trimming (Table I
  ratio gives 14.0 dB, D417 note) and 96.8 % "reflection at the output port" after trimming (`reflectivity_pct`,
  abstract; conclusion "96 %"); MZI extinction 21.65 dB before grating writing; centre 1555.8 nm; arm length 10 mm
  (derived).
- `reflector.bragg` grating pair (D396 cross-row): 95.5 % reflection (measured through the Port 3 dip), > 90 % per
  grating (author_estimate, "estimated from previous writing times"), band width ~1 nm as `stopband_width_nm` with
  "level not stated" (merged reflector precedents), grating length 2 mm from the abstract (Sec. II says "around 3 mm"
  typical; D417 note).

Not entered:
- Port 1 bandpass reflection (54.3 % -> 9.8 %) and Port 4 levels (Table I): no parameter for unwanted-port levels.
- UV-induced index change ~4.4e-4 (estimate); trimming steps of ~5 dB / > 2 dB (Fig. 2).
- Abstract text layer "135 dB": decimal point lost in extraction (body and Table I note print 1.35 dB).

Fab / facility: empty. Passive "were manufactured" / "were written" (p.2); acknowledgment thanks a named person for
fabrication of the planar guides without an org (D84b needs the org). All authors at BT Laboratories:
not in the registry (only relevant if a ruling sets fab).

## Judgment calls for the auditor

1. chen2015a: one `wdm.awg` row for the whole hybrid demux (PBC + PBS + PR + AWG) carrying the AWG design geometry; the
   AWG-only 5-6 dB estimate is a second excess-loss row on it (scope per_component, author_estimate) instead of a
   separate AWG row.
2. chen2015a PDL 0.1 / 0.4 dB as author_estimate ("It is estimated" from component tests, said to agree with Fig. 9);
   could be argued derived if the auditor reads it as arithmetic on own measurements.
3. chen2015a TM PBS cross-port IL entered as a figure read (0.2-0.5 dB) for the printed "almost zero".
4. chen2015a PBS / PR test structures are tied to the design of p.4-5 (the paper says the test PBSs have identical
   design); the theta of the Fig. 5 device is not stated (Fig. 6 siblings 13 / 15 / 17 deg).
5. suzuki2017: fab AIST on every row (first-person abstract + TIA SCR acknowledgment, suzuki2018 / D666); on the
   polarization-diversity row by the first-person assembly sentence (D399).
6. suzuki2017 2.5 dB/facet as author_estimate (no reference structure named), unlike suzuki2020 (5.6 dB from a named
   guide waveguide, measured); the 6.2 / 3.2 / 1.4 / 0.2 / 0.1 dB budget terms follow it.
7. suzuki2017 P_pi ~40 mW on the heater row: the paper does not say whether 40 mW is per MZ switch or per double-MZ
   element; the p.4 budget (2 x 8 x 40 mW) is noted, no value derived from it.
8. suzuki2017 double-MZ element as `switch_fabric.other` (test element vs in-matrix cell not stated; D158).
9. yang2018b IL ~2.5 dB kept as printed although the normalized Fig. 6(b)(c) on-state traces sit at ~0 to -2 dB.
10. kashyap1993 class `wdm.bragg_cdc` (MZI with Bragg gratings as channel-drop filter) plus a `reflector.bragg` row for
    the grating pair (D396); 95.5 % appears on the reflector row and its 13.5 dB form on the filter row.
11. kashyap1993 before- and after-trimming values as conditions on one row (same physical device, permanent trim).
12. kashyap1993 ~1 nm band width as `stopband_width_nm` (level not stated) on the reflector rather than a bw_* row on
    the filter (no level printed, rule 5).

## Registry gaps (skipped value + locator + proposed definition)

- `gap_nm`, `coupling_length_um`, `radius_um` on polarization: chen2015a PBS gap 205 nm, L 5.39 um, R1 20 / R2 19.3 um
  (p.5); already candidates in D439 / D559.
- `taper_length_um` on polarization: chen2015a PR 10 um taper (p.5); D439 candidate.
- Polarization conversion efficiency (%) on polarization: chen2015a PR ~85 % (p.8, p.10); D420 / D551 candidate.
- `wdl_db` on switch_fabric: suzuki2017 C-band loss variation < 3 dB (p.5); "wavelength-dependent loss over the stated
  range".
- `dgd_ps` on switch_fabric and splitter: suzuki2017 polarization-diversity switch < 8 ps in the C band (p.7, Fig. 8(b));
  yang2018b MZI < 100 fs and MMI ~25 fs (simulated, p.3-4); "differential group delay between polarization eigenstates
  of the device".
- Undefined-level bandwidth on wdm (criterion bandwidth, D539 / D559): kashyap1993 ~1 nm band-stop / band-pass width
  (p.3), entered on the reflector row only.

## Missing orgs

- TIA Super Clean-Room of AIST: facility, suzuki2017 p.9 Acknowledgments (9 rows; queued in D453 / D666).
- BT Laboratories: author affiliation of kashyap1993 p.1; no fab role set (D84b), listed only in case
  a ruling assigns fab.
