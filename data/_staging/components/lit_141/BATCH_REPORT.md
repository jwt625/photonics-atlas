---
batch: lit_141
date: 2026-11-15
papers: lit:chen2022c, lit:baumgartner2020, lit:morgan2021
totals: 16 components, 68 metric rows
validation: merge_component_staging.py --dry-run, 0 errors (1 unrelated warning on cmp_lit_ni2025b)
---

# lit_141 batch report

Page-1 check: all three cached texts are their source rows' papers. chen2022c is the arXiv v1 preprint, titled
"Broadband nonvolatile electrically programmable silicon photonic switches" (the source row carries the ACS Photonics
title); same authors, DOI and arXiv id, treated as the same work (D430 / D433). Its `garbled_text_layer` page is p.15
(reference list only); all values come from clean passages and page renders.

## lit:chen2022c (5 components, 36 metric rows)

| component | class | metrics |
|---|---|---|
| switch_2x2 | switch_fabric.other | 22 (IL ~2 dB at 1550 nm per state, IL < 2 dB over 1530-1565 nm, ER > 10 dB per state, crosstalk > 8 dB over the C-band, endurance-test contrasts 7.4 / 10.6 dB and 6 dB at event 2,750, endurance-test IL 3.5 / 4.0 dB, retention 720 h, simulated IL 0.33 / 0.65 dB, geometry) |
| switch_2x2_gst | phase_shifter.phase_change | 1 (endurance > 2,800 cycles) |
| switch_1x2 | switch_fabric.other | 8 (ER 9 dB per state at 1550 nm, IL 4 dB, simulated IL < 0.5 dB, geometry) |
| switch_1x2_gst | phase_shifter.phase_change | 1 (endurance > 4,000 cycles) |
| wg_switch_1x1 | phase_shifter.phase_change | 4 (ER 15 dB, 10 levels, endurance > 1,000 cycles, length 10 um) |

Not entered and why:
- Pulse energies 380 nJ / 6.83 uJ and switching energy density 0.95 / 1.63 fJ/nm3 (p.4-5): no parameter (switching
  energy rejected in D81); in component notes.
- Table 1 "This work" row (p.10): restates ER 10 / IL 2 dB, plus footprint length 50 um (conflicts with the 64 um
  coupling length, p.1 / p.3 / p.9; 64 um entered, conflict noted, D417) and optical bandwidth > 30 nm (no definition;
  the crosstalk row covers 1530-1565 nm). Other Table 1 rows are other works (rule 3).
- Simulated FDTD IL "around 1.0 dB" (p.25): stated once for the 1x2 and 2x2 designs together (D254); note only.
- Simulated c-GST hybrid-waveguide loss 5.5 dB/um and the 23.1 dB MZI example (p.20): mode-solver illustration of
  c-GST loss for a hypothetical MZI, not a component of the chip.
- Thermal stability 25-35 C "no significant spectrum shift" (p.8-9, Fig. S15): qualitative.
- Heater simulation pulse conditions (p.29): simulated drive values, in notes only.
- Retention of the c-GST state: only the a-GST state was tracked over 720 h.
- Prior-work comparisons (ref. 28 energy density 0.2 / 1.95 fJ/nm3, ~500 cycles): cited work (rule 3).

Judgment calls:
- 2x2 and 1x2 switches classed `switch_fabric.other` (single switch elements, D158 / D407, ros2022 precedent). The same
  group's later chen2024a coupler was merged as `splitter.directional_coupler`; that row is a multi-level tunable coupler,
  this paper calls its devices switches. Endurance counts sit on sibling `phase_shifter.phase_change` rows (D396,
  chen2024a pattern) because `endurance_cycles` is phase_shifter-only.
- 1x1 waveguide switch (amplitude only) classed `phase_shifter.phase_change` (D155).
- ER "over 10 dB" rows carry `band: c_band` + `wavelength_inferred` (no wavelength printed; Fig. 2(a) markers near
  1545-1550 nm). The Fig. 3 endurance contrasts are entered as the figure labels 7.4 (+/- 1.99) and 10.6 (+/- 1.66) dB
  (statistic mean); the text rounds to 8 / 11 dB (notes).
- Retention 720 h converted to 2,592,000 s (`derived`, D256).
- Simulated IL rows: wavelength not printed for the mode simulations; `c_band` inferred (GST data discussed at 1550 nm).
- HW widths 409 / 408 nm are simulated phase-matching optima, entered as `design_target` (dimensions, D82a).

Fab / facility: fab `org_university_washington` (author contributions name R.C. and Z.F. as fabricators, both UW).
Missing facility org: "Washington Nanofabrication Facility / Molecular Analysis Facility, a National Nanotechnology
Coordinated Infrastructure (NNCI) site at the University of Washington" (p.17 acknowledgments, "Part of this work was
conducted at"), role facility; not in `organizations.csv` / `org_aliases.csv` (also reported for chen2024a).

Registry gaps:
- `coupling_length_um` is not allowed for `switch_fabric` (the 64 um / 42 um coupling lengths went to `length_um` with
  the meaning in condition). Proposed: allow `coupling_length_um` for switch_fabric (coupler-based switch elements).
- PCM film thickness (20 nm GST) has no switch_fabric / phase_shifter parameter; in core_material. Proposed:
  `pcm_thickness_nm` (phase_shifter, switch_fabric, splitter): thickness of the phase-change film.
- `endurance_cycles` only on phase_shifter, which forces a sibling row for PCM switches. Proposed: allow on
  switch_fabric.

## lit:baumgartner2020 (7 components, 22 metric rows)

| component | class | metrics |
|---|---|---|
| pd_l2_w300 (Fig. 3 DC device, contact shape not stated) | photodetector.iii_v_on_platform | 6 (dark 0.2 nA at -4 V, 0.7 A/W at -6 V, EQE 69 %, 0.5 A/W at 1260 nm from the Fig. 3(b) inset, length, width) |
| pd_l2_w300_butterfly | photodetector.iii_v_on_platform | 3 (bw 8.5 GHz, geometry) |
| pd_l2_w300_straight | photodetector.iii_v_on_platform | 3 (bw 1.5 GHz, geometry) |
| pd_l2_w200_butterfly | photodetector.iii_v_on_platform | 4 (bw ~65 GHz author_estimate, 0.4 A/W at 1260 nm, geometry) |
| pd_w300_length_series | photodetector.iii_v_on_platform | 1 (capacitance 0.3-5.3 fF at -5 V over 2-20 um) |
| si_iii_v_adiabatic_coupler | waveguide_platform.transition | 4 (0.25 dB/coupler at 1310 nm, 10 um, ~100 nm vertical gap, 220 nm Si) |
| mqw_inp_butt_joint | waveguide_platform.transition | 1 (1.3 dB/coupler at 1350 nm) |

Not entered and why:
- Data reception (100 Gbit/s OOK BER 1.9e-3, 112 Gbit/s PAM-4 BER 9.8e-3 at 1295 nm, p.6): no parameter; notes.
- "Potentially going up to 100 GHz" (p.6): projection.
- Fig. 3(a) 85 C dark current and per-length capacitances of Fig. 3(d): figure reads not entered because the figure
  disagrees with the printed values (25 C trace reads about 1 nA at -4 V vs printed 0.2 nA; the printed "0.3-5.3 fF
  at -5 V" mixes the -8 V and -3 V points of Fig. 3(d)); conflicts in notes, printed values kept (D417).
- "Sub-nanoampere dark currents and sub-femtofarad capacitances" (p.2) and "devices as thin as 300 nm" (p.2): restate
  the entered values or are not a registry parameter.
- Earlier results of refs. 34 / 35 (same authors): not quoted with values; nothing entered from them.

Judgment calls:
- The 65 GHz bandwidth is `author_estimate`: the response was measured only to 50 GHz (p.5), so 65 GHz lies beyond the
  data range (D435).
- Three 2 um designs from Fig. 4(a) (300 nm straight, 300 nm butterfly, 200 nm butterfly) are separate rows; the Fig. 3
  DC device (2 um x 300 nm) gets its own row because its contact shape is not stated (D159 spirit: no assignment of its
  DC values to a bandwidth row).
- The 0.7 A/W / 69 % values: wavelength not printed (`o_band` inferred) and the absorber variant (MQW1 / MQW2 of
  Fig. 3(c)) not stated; both curves peak near 0.7 A/W, so the values stay on the DC-device row with the ambiguity
  noted. Reference plane `on_chip` (the paper calls it external responsivity including the adiabatic and butt coupler
  losses, p.4). EQE `derived` (computed by the authors from R, D80a; wen2022 precedent).
- Capacitance range entered on a family row (shen2016 precedent) because only the 2-20 um range is printed.
- Both couplers are `waveguide_platform.transition` (on-chip inter-material transitions, D48); per-coupler losses from
  cascade slope fits (`cutback`, `measured`, D80a). Platform `other` for PDs and transitions (bonded III-V membrane on
  SOI has no enum value; ofc2026 m4d3 / muthuganesan2023 precedent; `inp_membrane` considered but kept for IMOS-type
  rows).
- Fab (coordinator question 1): set to `org_binnig_and_rohrer_nanotechnology_center` on all 7 rows, borderline under
  D84b ("We thank ... the BRNC OpTeam for support in fabricating the devices", p.6) plus a first-person fabrication
  account (p.3-4) by authors spread over IBM Research - Zurich, ETH Zurich and IBM T. J. Watson (no single own org,
  D154). Alternatives: empty fab (iadanza2024 precedent, where the BRNC operations team was thanked without the
  fabrication wording) or `org_ibm_research_zurich` (would need the BRNC-IBM relation, which the paper does not print).
  Facility empty (staff thanks, D72).

Fab / facility orgs: none missing (BRNC, IBM Research - Zurich are in the registry).

Registry gaps: none blocking. Candidate: data-reception BER at a stated symbol rate on photodetector rows (no
parameter; skipped values above, p.6 Fig. 4(b)).

## lit:morgan2021 (4 components, 10 metric rows)

| component | class | metrics |
|---|---|---|
| pd_type1_100um | photodetector.other | 3 (0.24 A/W at 405 nm, dark < 1 nA, length 100 um) |
| pd_type2_100um | photodetector.other | 4 (0.25 A/W, EQE 76 %, dark ~90.8 uA, length 100 um) |
| al2o3_wg_600nm | waveguide_platform.straight | 2 (2.9 dB/cm at 405 nm, width 600 nm) |
| input_coupler | fiber_chip_coupler.edge | 1 (8.4 dB input coupling loss at 405 nm) |

Not entered and why:
- Responsivities at 4-32 um lengths and the backward-direction values (Fig. 2(b), (c)): figure series with
  Fabry-Perot artifacts; only the 100 um values are printed. Not read off the plot.
- Back-reflection reduction of Type II (Fig. 2(a)): qualitative image.
- 0.326 A/W photon-limited maximum: physical constant-based bound, not a device value.
- Speed and other figures of merit: announced for the talk, not in the paper.

Judgment calls:
- Responsivities `derived`, `ref_plane on_chip`: de-embedded with the paper's own 8.4 dB coupling and 2.9 dB/cm
  propagation loss (wen2022 precedent). Value wording varies (Type I "in excess of 0.24" / "up to 0.24"; Type II "0.25",
  "up to 0.25", abstract "above 0.25"): entered as printed with `statistic: best`, wording in notes.
- Dark-current bias (coordinator question 2): not printed; `bias_v -2` taken from the reverse end of the Fig. 2(d)
  sweep (axis -2 to 1 V), where the Type II curve reads about 0.09 mA, matching 90.8 uA; Type I "< 1 nA" set at the same
  bias. If the coordinator prefers, both rows can be deleted (bias required by the registry).
- Propagation and coupling loss treated as the paper's own measurement (paperclip devices "fabricated on the same run";
  the citation [4] sits on the preceding sentence about the platform, D80i): coordinator question 3 if the audit reads
  it as cited.
- Coupler class `fiber_chip_coupler.edge` inferred from the Fabry-Perot cavity "between the detector and the chip facet"
  (p.2); the coupler itself is not described. Scope `per_facet` (input coupling loss of one facet, from the paperclip
  calibration).
- PD platform `other` (Al2O3 waveguide feeding Si diodes); waveguide and coupler `al2o3`.
- Fab `org_mit_lincoln_laboratory` on all rows ("fabricated using MITLL's 200 mm CMOS foundry line", p.1; calibration
  devices "fabricated on the same run", p.2); `process_name` from the printed wording.

Fab / facility orgs: none missing.

Registry gaps: none.

## Coordinator questions

1. baumgartner2020 fab: BRNC (as entered, D84b literal), empty (iadanza2024), or IBM Research - Zurich?
2. morgan2021 dark currents: keep `bias_v -2` from the Fig. 2(d) sweep end, or delete both rows (bias not printed)?
3. morgan2021 2.9 dB/cm and 8.4 dB: own measurement (as entered) or cited from ref. [4]?
4. chen2022c: confirm `switch_fabric.other` over `splitter.directional_coupler` for the PCM coupler switches (chen2024a
   was merged as a splitter).
