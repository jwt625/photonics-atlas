# lit_154 batch report

Distilled 2026-11-15 (contract v7, skill `pic-component-distill`). Papers: bogaerts2010, bucio2017, gao2017,
harris2017, shang2017a, liu2020c. Page-1 titles match the source rows (harris2017 is the arXiv v3 text of the Nature
Photonics paper; supplement not cached). No correction / erratum, no garbled text layer; gao2017 p.7 text layer is
interleaved (two-column overlap), values read from `figures/page_07.png`.

Totals: 36 components, 315 metric rows. `merge_component_staging.py --dry-run`: 0 errors (one WARN on an unrelated
merged row, cmp_lit_ni2025b_pimmwc).

| paper | components | metrics |
|---|---|---|
| shang2017a | 6 | 63 |
| liu2020c | 2 | 30 |
| gao2017 | 4 | 64 |
| bucio2017 | 9 | 89 |
| harris2017 | 4 | 12 |
| bogaerts2010 | 11 | 57 |

## shang2017a (Si3N4 AWGs, UC Davis)

- Rows: four `wdm.awg` (8x200, 16x100, 16x50, 16x25 GHz), reference straight waveguide, polished-facet edge coupling.
- AWG IL is the spectrum normalized to the on-chip reference straight waveguide: `de_embedded` + `reference_structure`.
  C band `wavelength_inferred` from the Fig. 3 axes. Crosstalk type not stated -> `crosstalk_db`.
- Conflict (D417): 16x25 GHz IL is 2.7 dB in abstract, text and conclusion, 2.1 dB in Table 1; entered 2.7 with note.
- Channel spacing entered as `author_estimate` (design; the paper says the measured spacing matches, no number).
- Reference waveguide: 3.5 dB fiber-to-fiber `measured`; the 1.5 dB per facet and 0.5 dB/cm budget terms
  `author_estimate` (origin not stated, rule 4).
- Not entered: FSR "1.8 / 0.9 / 0.45 THz" (three values for four AWGs, assignment ambiguous, D156); RMS phase errors
  pi/40 and pi/6 (no parameter); design typo "16 x 5 GHz" noted.
- Fab `org_university_of_california_davis` (first-person "We patterned", "We polished", all authors UC Davis);
  facility Marvell Nanofabrication Laboratory + Center for Nano-MicroManufacturing (p.6; fu2023 precedent).

## liu2020c (O-band CWDM, cascaded multimode waveguide gratings, Zhejiang University)

- Rows: `wdm.bragg_cdc` 4-channel filter (eo:liu2023 MWG WDM precedent), `mode_converter.mdm_mux` adiabatic dual-core
  taper (fabricated sub-element, simulated values only, D80e).
- Measured: per-channel excess loss 0.8 / 0.3 / 0.9 / 0.7 dB (normalized to a straight waveguide with GCs:
  `de_embedded`), 1-dB bandwidth ~15 nm, spacing ~18 nm, crosstalk < -20 dB within 11 nm, 46 pm/C (channel 3).
- Simulated: 16.5 nm 1-dB width, < 0.15 dB, adjacent / non-adjacent crosstalk > 20 / > 34 dB, SLSR > 20 dB.
- Judgment call: `period_nm` 250-268 nm range from the Fig. 3(c) set that the text calls "all the channels".
- Not entered: BW1dB / BW20dB ratios 0.56 / 0.75 / 0.77 / 0.72 (no parameter); duty cycle 0.5 (`fill_factor` not
  allowed on wdm); corrugation depth 170 nm (no parameter); mode-demux gaps 1.2 / 0.2 / 0.5 um (`gap_nm` not allowed
  on mode_converter); grating couplers (70 nm etch only, no value); Table I other works.
- Fab empty (passive sentence, D80b).

## gao2017 (SiN cascaded-MZI O-band demux, HUST / WRI)

- Rows: Type-I (LR4) and Type-II (CWDM4) `wdm.cascaded_mzi`, apodized GC, channel waveguide.
- Tables 1-2 entered per channel: IL, center wavelength, XT_center, XT_1dB (both `crosstalk_db`, wording in
  condition), 1-dB bandwidth; thermal drift 18.4 / 18.7 pm/C (channel 1 fits).
- IL rows `author_estimate` + `loss_breakdown`: the subtracted GC loss "assessed to be about 7 dB" has no stated
  origin and no stated per-coupler / per-pair scope (D428). GC row: 7 dB `scope unspecified`, `author_estimate`.
- Waveguide 2.8 dB/cm `measured`, method unspecified, O band inferred; group index 2.05 simulated at 1302 nm.
- Not entered: footprint ~1 x 0.6 mm2 (printed once for both types, D254 / D559, in notes); grid offsets
  Delta lambda ITU (no parameter); effective index 1.60.
- Fab empty (passive, D80b).

## bucio2017 (SiNx angled-MMI triplexers, University of Southampton)

- Rows: six `wdm.other` AMMIs (O / C band x stoichiometric / N-rich / Si-rich layer; same design on three wafers =
  sibling physical devices, rule 9), three `waveguide_platform.straight` (Table 2 per layer, 1310 / 1550 nm cutback).
- Table 3 per device: channel spacing, IL bound (`lt`, "+/-" term undefined, in notes), 3-dB BW, crosstalk; Table 5
  thermal drift; stoichiometric IL non-uniformity < 1 dB.
- Judgment calls: crosstalk printed as positive "XT < 18 dB" with larger = better (p.8) -> suppression magnitude
  `gt`. Table 2 propagation losses entered as `measured` cutback although the caption says "as described in [9]"
  (authors' layer paper; the citation is on the method) - flagged D80i borderline for the audit.
- Not entered: channel-wavelength offsets Delta lambda_i (no parameter); sensitivity to W_MDW errors ~100 pm/nm
  (registry gap); theta_t and output positions L1-L3 (no parameter); refractive indices (no parameter); simulated
  design targets.
- Fab `org_university_of_southampton` (acknowledgment names the fabrication place, D448).

## harris2017 (programmable nanophotonic processor, MIT / Elenion; arXiv v3)

- Rows: `switch_fabric.mzi_mesh` 26x26 PNP (8 dB fiber-to-fiber, 1.0 dB de-embedded `derived` = 8 - 2 x 3.5, the
  paper prints 80 %), `switch_fabric.other` RBS / MZI unit (extinction ~66.3 dB), `phase_shifter.thermo_optic`
  (> 2 pi), `fiber_chip_coupler.edge` inverse taper to glass PIC (3.5 dB per facet incl. glass PIC and
  connectorization, `measured` per D167 + Methods per-channel measurement).
- Not entered: phase-shifter 3-dB bandwidth 130.0 kHz (cited to the authors' ref. [36], rule 3); mean RBS extinction
  ratio 0.9996 (no dB form printed); thermal crosstalk 1 % (no parameter); supplement values (not cached).
- Wavelength 1570 nm from the Methods measurement description.
- Fab empty: the Methods name the "Optoelectronic Systems Integration in Silicon foundry" (OpSIS, missing from the
  registry). Coordinator question: author contributions say "T.B.J. and M.H. fabricated the system", both printed at
  Elenion Technologies; D395 would give `org_elenion`, but the foundry named for the run is OpSIS - left empty.

## bogaerts2010 (invited overview, Ghent University / IMEC)

- Rows: photonic wire (2.7 dB/cm spiral cutback), bend series (Fig. 6 labels 0.071 / 0.039 / 0.02 / 0.009 dB/90 deg at
  r = 1 / 2 / 3 / 5 um), shallow-etch crossing (0.15 dB, -40 dB, < 36 um2), shallow MMI 1x2 (<= 0.2 dB excess,
  < 0.02 dB imbalance), single-stage AMZI (IL < 1 dB, figure-read extinction 15-39 dB and FSR ~4.9 nm), add-drop ring
  filter (Q 15600 / 15400 fits, ~90 % drop), bistable ring (Q 9500, different g2), 30-ch DBR-facet echelle,
  8 x 400 GHz AWG, shallow GC (33 % / 5 dB, `author_estimate`, origin not stated, velha2016 D544), MZI uniformity
  set (dip spread <= 1 nm).
- Review rule: values in sentences citing refs. [1], [12], [16], [38], [39], [42] not entered (248 nm 7 dB/cm wire
  loss, Fresnel-facet 30 %, 0.2 dB crossing of ref. [16], small-ring Q ~5000 / FSR 50 nm, DBR facet > 80 %).
  Weak point: the crossing concept cites the authors' own ref. [15]; the loss / crosstalk sentence and Fig. 8 carry
  no citation, kept (D408).
- Conflicts (D417): AWG text / caption 1.1 dB center and 2.4 dB outer vs Fig. 16 marks 1.1 / 1.3 dB; MMI Fig. 9 trace
  reaches ~0.24 dB vs the printed "-0.2 dB or less".
- Not entered: abrupt Fig. 2 splitter ~1.5 dB (lithography generation not stated, D159); AMZI arm imbalance 45/55 ->
  50/50 (coupling and loss not separated); CD reproducibility 1 % (no parameter); generic 80-90 pm/C, n_g 3.4-4.0.
- Fab `org_imec`: first-person "We fabricate our devices" at IMEC research facilities plus "the people of the IMEC
  p-line for the processing of the devices" (bogaerts2007a P-line precedent, D448 / D84b). process_name: printed
  193 nm lithography on 200 mm 130 / 90 nm CMOS tools with 70 nm shallow + deep etch. Cladding not stated (empty).

## Missing fab / facility orgs (name as printed + locator)

- "Southampton Nanofabrication Centre, University of Southampton" - facility, lit:bucio2017 p.11 Acknowledgments
  (9 rows; same string already reported for croce2026, perez2017, skandalos2026).
- "Optoelectronic Systems Integration in Silicon foundry" (OpSIS) - fab (foundry / MPW service), lit:harris2017 p.7
  Methods (4 rows; OpSIS org-round item already open, D418 / D439 / D458).
- "ePIXfab" - fab (MPW service, "support in design and fabrication"), lit:bogaerts2010 p.10 Acknowledgment (11 rows;
  also reported for lindenmann2012).

## Registry gaps (skipped value + locator + proposed definition)

- `bw_ratio_1db_20db` (wdm): liu2020c 0.56 / 0.75 / 0.77 / 0.72 (p.4); "ratio of 1-dB to 20-dB passband width"
  (D443 candidate).
- `fabrication_sensitivity_pm_per_nm` (wdm): bucio2017 ~100 pm/nm, Table 4 p.9; "channel-wavelength shift per nm of
  width error of the stated feature".
- `rms_phase_error_rad` (wdm.awg): shang2017a pi/40, pi/6 (p.6, Fig. 4); "RMS phase error over the arrayed arms".
- `gap_nm` on mode_converter: liu2020c 1.2 / 0.2 / 0.5 um (p.2) (D533 candidate).
- `fill_factor` / corrugation depth on wdm: liu2020c duty 0.5, depth 170 nm (p.3) (D540 candidate for fill_factor).
- `wavelength_offset_nm` (wdm): gao2017 Delta lambda ITU per channel (Tables 1-2), bucio2017 Delta lambda_i (Table 3);
  "offset of the measured channel center from its design / grid wavelength".
