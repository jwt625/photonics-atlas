# lit_172 batch report

Distilled 2026-11-16 under the pic-component-distill skill (Contracts v4-v7). Papers: lit:xuan2016, lit:quack2019,
lit:sun2010, lit:nedeljkovic2014, lit:espinola2003. Totals: 33 components, 200 metric rows.
`merge_component_staging.py --dry-run`: +33 components, +200 metrics, 0 errors (the one warning printed belongs to the
merged row cmp_lit_ni2025b_pimmwc, not this batch).

Page-1 title check: all five cached texts are their source rows' papers (Optica 3(11) 1171 2016; IEEE JQE 56(1)
8400210, invited paper; Opt. Express 18(8) 8406 2010; IEEE PTL 26(13) 1352 2014; IEEE PTL 15(10) 1366 2003). None is a
correction / erratum; no garbled text layer. Garbled formulas in espinola2003 (rise time, cutoff, ER sign) were read
from the page renders (p.2-3). Figure reads were checked on 4x / 5x PyMuPDF renders of the cached PDFs (quack2019
Fig. 13, nedeljkovic2014 Fig. 6). No existing rows for these papers in data/components.

## lit:xuan2016 - 12 components, 79 metric rows

| component | class | metrics |
|---|---|---|
| resonator_a | resonator.ring | 35 (FSR TE00/01/02 measured + simulated, TM 3 families; Q_L / Q_i / notch at 1553.8958, 1556.6858, 1553.697, 1564.70 nm; ring-down Q_L / Q_i; TM Q_L / Q_i / notch; ~2.1 dB/m; geometry 7) |
| resonator_a_comb | laser.comb | 8 (threshold 4.2 / 5.0 mW in fiber, 2.36 / 2.8 mW on chip, Eq. (1) 2.2 / 3.8 / 2.7 mW, ~25 GHz single-FSR comb) |
| resonator_b | resonator.ring | 5 (drop-port Q_L 8.25e6, ~24 MHz, Q_i up to 1.1e7, gaps 400 / 700 nm) |
| resonator_b_comb | laser.comb | 1 (24.7 GHz one-FSR comb) |
| edge_coupler | fiber_chip_coupler.edge | 3 (~5 dB fiber-to-fiber, ~2.5 dB per facet, TM-TE 1-2 dB) |
| ring_r100_w3, racetrack_no_upper_clad, ring_t300_unannealed, ring_t750_w2_pieces, ring_r100_w5_purdue_film, ring_t800_w3, ring_t800_w5 | resonator.ring | 3-4 each (Table 1 / p.9 highest Q_i + cross-section, radius) |

Values not entered and why:
- Table 1 "finger-shaped racetracks" 1.7e7: same value as resonator_a m14 (Fig. 7(a)), not entered twice.
- Fitted notch depth "over 40 dB" at 1553.8958 nm (fit prediction, not a measurement): note on m12.
- Fig. 6(b) per-family intrinsic Qs (under-coupling assumed for all, plot only) and the three-family spectrum: not read.
- Ring-down photon lifetimes 6.6 / 7.7 ns: no parameter; they are the inputs of the derived ring-down Q_L rows.
- Simulated dispersion -120 ps/nm/km and Aeff 1.5 um2: no parameter (D81 rejected dispersion).
- 84 deg sidewall angle: a simulation input of unstated origin (not SEM-stated), not entered.
- Single-FSR comb pump powers 27 mW (resonator A) and 24 mW (resonator B): no parameter for a comb-formation pump
  power (registry gap below); in notes.
- Resonator B quasi-TM "similar" Qs and resonator B cross-section: not stated.
- "Without annealing" ring radius: Table 1 prints 200 um, p.3 text 300 um for the same 2.7e6 device; radius not entered
  (D159 / D417), conflict in notes.
- Propagation loss "usually small (< 0.01 dB/mm)" (p.4): general statement, not a measurement of this chip.
- U-groove 145 um x 63 um (Fig. 4(c) labels): no parameter (no fiber_interface row, no performance value).
- Cited values (refs. [15], [23], [34], [35], [36]: Q 2.7e8, 6e9, 20 million, 7 million, 81 million, 3.0 dB/m): rule 3.

Judgment calls:
- D403 applied per resonance: Q_i 1.66e7 (critical coupling argued against a 17 dB measured dip), 1.68e7 (over-coupling
  assumed), 1.55e7 (regime not stated), TM 9.0e6 (under-coupling assumed), all Table 1 / p.9 Q_i and both ring-down Q_i
  -> author_estimate; only Q_i 1.7e7 at 1556.6858 nm (under-coupled regime confirmed on the data with the ref. [27]
  method) -> derived.
- Ring-down Q_L (Q = omega tau from fitted lifetimes) -> derived (arithmetic on a fitted lifetime).
- Per-facet 2.5 dB and the on-chip thresholds 2.36 / 2.8 mW -> author_estimate (equal facets, bus loss neglected on a
  general statement; D462 / D514); the in-fiber thresholds 4.2 / 5.0 mW are measured.
- Kerr comb split into laser.comb rows beside the resonator rows (D396; ji2017 / delhaye2007 precedent).
- Each Table 1 / p.9 process variation is its own resonator row (rule 9, sibling designs); wavelength not stated ->
  C band inferred (`wavelength_inferred`), statistic best.
- Fab org_purdue_university on all rows: first-person process account ("the process steps and variations we have
  attempted", "we ... performed high-temperature annealing"), all authors at Purdue (one dual affiliation). Noel
  Technologies grew the default Si3N4 films only (film supplier, notes). Facility org_birck_nanotechnology_center only
  on ring_r100_w5_purdue_film (the only step the paper places at Birck; D610 siddharth2024 precedent).

## lit:quack2019 - 7 components, 32 metric rows

| component | class | metrics |
|---|---|---|
| gc | fiber_chip_coupler.grating | 1 (~3.1 dB per GC at 1530 nm, loopback_half derived) |
| air_oxide_transition | waveguide_platform.other | 6 (~0.07 dB per transition cutback, ~0.026 dB simulated read off Fig. 6(b), 450 / 214 / 70 nm, 15 um taper) |
| suspended_dc | splitter.directional_coupler | 10 (0.5 dB best drop-port excess loss at 1560 nm, ER 25 / >= 20 / < 10 dB, 300 nm, 10 um taper, 1 um straight, 150 nm gap (figure label), 5 um bends, ~600 um2) |
| disk | resonator.disk | 6 (Q_L up to 3.6e4, ER > 20 dB, R 10 um, 140 nm gap, 450 / 214 nm bus) |
| ring | resonator.ring | 7 (Q_L up to 3.6e4, ER > 20 dB, R 20 um outer, 6 um width derived, 130 nm gap, 450 / 214 nm bus) |
| mems_ps_out_of_plane | phase_shifter.mems | 1 (~1.1 pi at 24 V, Fig. 13(a) read) |
| mems_ps_in_plane | phase_shifter.mems | 1 (~0.55 pi at 30 V, Fig. 13(b) read) |

Values not entered and why:
- Simulated return loss ~37 dB per air-oxide transition (p.5): `back_reflection_db` is not allowed for
  waveguide_platform (registry gap below).
- 42-transition series (excluded by the authors for ripples) and simulated DC spectra (Fig. 8, 5 nm offset): not read.
- "Very low tuning losses" of the MEMS phase shifters (ER and envelope unchanged): no value. Actuation curves were not
  measured (p.7).
- MMI- and photonic-crystal-based transitions: tested types, no values.
- Fig. 14 circuit (2 mm x 1.2 mm, ref. [27]) and Sections II-III (general MEMS mechanisms, cited works): no values of
  this chip.

Judgment calls:
- Invited paper with new measurements on an imec-platform chip; the cited own conference papers (refs. [27], [28],
  [31], [32]) are design / earlier-prototype references and no value sentence or caption attributes a value to them:
  values kept (D408). The coordinator may want to check the DC values against ref. [28] (Sattari et al., OMN 2019) if
  that paper is ever cached.
- Fab org_imec ("designed and fabricated in a simplified version of IMEC's iSiPP50G ... platform", D455) plus
  org_epfl for the release post-processing performed at CMi (D440 / D83c), facility
  org_center_of_micronanotechnology (printed "Center of MicroNanoTechnology (CMi) at EPFL"; release also acknowledged
  p.8). Applied to the GC row too: it is not released but carries the 50 nm ALD alumina of the release process
  (noted); the coordinator may prefer org_imec only on the GC (D933 exclude option exists for post-processed rows).
- Air-oxide transition as waveguide_platform.other with transition_loss_db (one Si layer, cladding change; xiao2022 /
  cheng2025 precedent), test_structure true (22 / 30 / 42-transition series).
- Directional coupler drop-port "insertion loss 0.5 dB" stored as `excess_loss_db` (full-transfer cross output, rule 6).
- Disk / ring Q_L "up to 3.6e4" is printed once for both devices ("Both for the freestanding disk resonator and the
  ring resonator"); entered on both rows (lin2023 "in all cases" precedent), statistic best; caption says "more than"
  (D417 note). The "> 20 dB" ER is labelled on each Fig. 11 panel.
- MEMS phase shifts are figure reads of the authors' delta-phi arrows over the MZI FSR. The text says "more than pi
  phase shifts for actuation voltages below 30V" for "the compact devices"; the in-plane device reads ~0.55 pi at
  30 V (D417 conflict note, shift taken as less than one FSR as drawn). Platform `soi` for all released parts.

## lit:sun2010 - 3 components, 24 metric rows

| component | class | metrics |
|---|---|---|
| released_mzi_switch | switch_fabric.other | 6 (6 dB fiber-to-fiber, ~2.8 dB device IL author_estimate, ER 25 dB, ~8960 um2, 1 in / 2 out) |
| released_arm_heater | phase_shifter.thermo_optic | 12 (P_pi 0.54 mW, 10-90 % rise 141 us, 2.48 kHz, 1.6 kOhm, heater 100 x 2.9 um x 200 nm, 450 x 250 nm core, 1 um BOX, 1.1 um clad, 100 um arm) |
| unreleased_arm_heater | phase_shifter.thermo_optic | 6 (P_pi 31.2 mW, rise 39 us, heater / core geometry) |

Values not entered and why:
- Cantilever-coupler loss 1.6 dB per connection: from the regression of the authors' ref. [14] (rule 3); it is the
  subtracted input of the author_estimate 2.8 dB row.
- Unreleased switch "similar insertion loss and extinction ratio": no values.
- Core index change ~7.7e-3, temperature rise ~41.7 K, Pt resistivity 1-2e-5 ohm m: no parameter.
- Released cladding w 2.9 um, h 2.1 um, trench gap g 4.5 um: no role-specific parameter; in `cladding` text.
- Introduction values (6.5 mW / 14 us, 6 mW / 600 ns, 10 mW / 1.1 kHz): cited works (rule 3).

Judgment calls:
- One switch_fabric.other row (D158) plus phase_shifter rows for the heated arm (D396, chang2026a precedent); the
  unreleased comparison arm is its own row (sibling design).
- 2.48 kHz is computed by the authors from the rise time -> derived (chang2026a / wang2026g precedent); 540 uW and
  1.6 kOhm unit conversions -> derived (D256).
- Fab empty: passive fabrication sentences only, two OSU authors (D80b). No missing org.

## lit:nedeljkovic2014 - 8 components, 43 metric rows

| component | class | metrics |
|---|---|---|
| straight_mzi_family | phase_shifter.thermo_optic | 11 (IL mean 1.3-2.2 dB, ER mean 19.3-22.5 / best 28.2 dB, DC MD mean 24.1 / best 30.5 dB, stack 6) |
| straight_w10_l2250 | phase_shifter.thermo_optic | 4 (245 mW, 23.8 kHz, heater 10 um x 2.25 mm) |
| straight_w10_l3000, straight_w15_l2250, straight_w15_l3000 | phase_shifter.thermo_optic | 3 each (248 / 317 / 318 mW, heater dims) |
| spiral_mzi_family | phase_shifter.thermo_optic | 10 (IL mean 3.1-9.2 dB, max-ER range 7.9-21.0 dB, MD mean 10.9 dB, best P_pi 47 mW, best 21.3 kHz, stack 5) |
| spiral_r27p5_n2 | phase_shifter.thermo_optic | 3 (MD 17.8 dB, P_pi ~98 mW read off Fig. 6, 1.77 mm spiral) |
| rib_wg | waveguide_platform.straight | 6 (3.5 dB/cm author_estimate, 0.6 dB/cm simulated substrate leakage, stack 4) |

Values not entered and why:
- MMI insertion loss 0.10 +/- 0.01 dB and 1.5 dB/cm for W = 1350 nm: cited from the authors' ref. [4] (rule 3).
- Bandwidth range 17.8-23.8 kHz over all devices of both families: stated across families, kept in notes (D254); the
  family maxima 23.8 / 21.3 kHz are entered.
- Fig. 5 simulated metal-absorption loss vs silica thickness, Fig. 7(a)/(b) per-device switching powers: not read.
- Smet = 1 um heater edge to waveguide edge (lateral, edge-to-edge): neither `heater_offset_um` (centre offset) nor
  `heater_gap_um` (vertical) fits; in notes.
- Thermo-optic coefficient 1.70e-4 /C at 3.8 um (from ref. [12]); NIR values of ref. [10]: cited.

Judgment calls:
- Thermo-optic MZI "modulators" classed phase_shifter.thermo_optic carrying the MZI extinction (registry definition;
  abediasl2015 / chung2017 VOA precedent), not switch_fabric (the paper calls them modulators / on-chip choppers).
- Population rows for the two families (D165) beside design rows that carry only the values the text ties to a design;
  family ranges are not copied onto design rows (D552 / D592).
- Spiral IL conflict: Sec. III-A 3.1-9.2 dB entered, conclusion 4.8-11.8 dB in notes (D417).
- rib_wg 3.5 dB/cm: the sentence follows the ref. [4] MMI sentence and carries no citation or chip identification;
  kept as author_estimate (D80i borderline) with `wavelength_inferred` 3.8 um. The coordinator may prefer to drop it.
- Fab org_university_of_southampton (stated place "Southampton Nanofabrication Centre, University of Southampton",
  all authors ORC Southampton; bucio2017 precedent).

## lit:espinola2003 - 3 components, 22 metric rows

| component | class | metrics |
|---|---|---|
| mzi_switch | switch_fabric.other | 4 (32 dB total IL, scope unspecified; ER > 15 dB both polarizations; 1200 um arms; 600 nm) |
| heater_ps | phase_shifter.thermo_optic | 12 (P_pi 50 mW measured / 46 mW model, 1/e rise <= 3.5 us, 100 kHz derived / 49 kHz model, heater 700 x 14 um x 100 nm, 60 ohm, 1 um gap, 600 x 260 nm) |
| si_strip_wg | waveguide_platform.straight | 6 (110 dB/cm cutback from 11 dB/mm, stack 5) |

Values not entered and why:
- Eq. (3) "rise time 7 us" for the modelled 49 kHz: arithmetic on a simulated value; in notes.
- Temperature change 8 K for pi (Eq. (1)): no parameter.
- Y-branch length 160 um, 3.8 deg branching angle, 3 um I/O waveguides with 10 um tapers: no switch_fabric geometry
  parameter (taper_length_um not allowed on switch_fabric); in notes.
- "< 1 dB/cm after wet-oxidation smoothing" (ref. [14], future work): cited.

Judgment calls:
- 1/e rise time from an exponential fit -> `thermal_time_constant_us` (le), not `rise_time_us` (10-90 %), chen2024b
  precedent; the authors' 100 kHz cutoff (0.35 / 3.5 us) -> `bw3db_khz` derived.
- 32 dB total insertion loss scope `unspecified` (lensed fiber in, objective out; whether coupling is included is not
  stated).
- Fab org_columbia_university: "We have designed and fabricated" with all authors at Columbia units (D72 / D80b).
  Unibond (Smart-Cut) SOI wafer supplier: note only. Heater resistance 60 ohm `measured` (device property).

## Missing fab / facility orgs

- Southampton Nanofabrication Centre (facility), printed "Southampton Nanofabrication Centre, University of
  Southampton", lit:nedeljkovic2014 p.2 Sec. III (8 rows; parent org_university_of_southampton). Same string as the
  merged bucio2017 rows, which also left the facility empty.
- Noel Technologies (film supplier only, not a fab org): printed "a CMOS foundry (Noel Technologies, ...)",
  lit:xuan2016 p.2; notes only, no org needed for components.

## Registry gaps (skipped value + locator + proposed definition)

- `back_reflection_db` on waveguide_platform (transition): quack2019 simulated return loss ~37 dB per air-oxide
  transition at 1550 nm (p.5). Proposal: allow back_reflection_db for waveguide_platform.transition / other
  ("reflection of one transition, positive dB below the input").
- Comb-formation pump power: xuan2016 single-FSR comb at 27 mW (resonator A, p.8 Fig. 12) and 24 mW (resonator B, p.8
  Fig. 11). Proposal: `comb_pump_power_mw` on laser.comb ("pump power at which the stated comb state is reached;
  reference plane and comb state in condition").
- Photon lifetime: xuan2016 ring-down tau 6.6 / 7.7 ns (p.6). Proposal: `photon_lifetime_ns` on resonator (low
  priority; Q_L from it is entered as derived).
- Heater edge-to-waveguide lateral gap: nedeljkovic2014 Smet = 1 um (p.2). Proposal: widen `heater_gap_um` definition to
  allow a stated lateral edge-to-edge gap with the geometry in condition, or add `heater_edge_gap_um`.
- Switch-element geometry on switch_fabric (taper_length_um, branching angle): espinola2003 10 um tapers, 3.8 deg (p.1).
  Low priority.
