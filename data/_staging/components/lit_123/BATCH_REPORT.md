# lit_123 batch report (2026-11-11)

All five cached texts match their source rows (page-1 title); none is another paper or only a correction / erratum; no
garbled text layer. No supplements cached. Figure values were checked on the cached `page_NN.png` renders (wang2026g
Fig. 4, poulsen2025 Fig. 6). Dry-run: +44 components, +321 metrics, 0 errors (the one warning, ni2025b m18 / m4, is on
an existing merged row). All sources are `restricted_local_only`: no quotes beyond a few words.

| paper | components | metrics |
|---|---|---|
| zhang2021a | 7 (waveguide_platform.straight 2: Si 500 x 220 nm, PECVD SiN 1.5 um x 400 nm; fiber_chip_coupler.edge 2: Si 200 um SSC, SiN OPA input; free_space_emitter.other 1: 64-ch OPA; splitter.y_branch 1: SiN Y tree; waveguide_platform.transition 1: SiN-Si) | 28 |
| wang2026g | 14 (phase_shifter.thermo_optic 12, one per design: 800 um plain / trench / undercut with 0-3 bridges, 400 um plain / trench, 3-bridge undercut 100 / 200 / 300 / 400 um; splitter.mmi 2: 1x2, 2x2) | 138 |
| poulsen2025 | 3 (phase_shifter.mems: PhC slot comb-drive tuner; mode_converter.converter: MMI strip-to-slot, simulated only; waveguide_platform.other: slot-to-PhC junction, simulated only) | 11 |
| sun2022a | 18 (waveguide_platform.bend: Si R 1 / 1.5 / 2 um and SiN R 8 / 10 / 12 um, each modified Bezier / traditional Bezier / circular) | 126 |
| katsura2023 | 2 (resonator.photonic_crystal: binary-mask and phase-shift-mask cavity populations, D165) | 18 |
| total | 44 | 321 |

## Fab / facility orgs

- zhang2021a: fab `org_amf` on all 7 rows (p.5 Sec. 3.1: authors designed and fabricated the OPA with the standard
  silicon photonics integration process in AMF). The Si / SiN damage-test waveguides and the Si SSC are placed on
  "our chip" (p.2), so AMF is kept on them too (judgment call 1). `process_name` empty (no node or flow printed).
- wang2026g: fab `org_imec` on all 14 rows (p.4: waveguide stack in the imec 200 mm CMOS pilot line; p.5: heater /
  trench / undercut post-processing by the authors on diced dies, all at imec). `process_name` "imec 200 mm CMOS
  pilot line". Facility left empty: "imec Xplore lab" (p.5) is probably `org_xplore_multiuser_cleanroom`
  ("Xplore multiuser cleanroom", BE) but the printed name differs; coordinator to confirm an alias.
- poulsen2025: fab `org_amf` + `org_cmc_microsystems` (p.6 Sec. 3: AMF MPW of the standard active 140 nm process;
  p.10: CMC acknowledged for access to foundries, D83d / D398; judgment call 8). Post-processing site missing from the
  registry (below). `process_name` "AMF standard active 140 nm silicon photonics process (MPW)".
- sun2022a: fab empty (passive fabrication sentences, both authors at Zhejiang University, no org named; D80b).
- katsura2023: fab `org_national_institute_of_advanced_industrial_science_and_technology` (p.3: lithography and
  etching "done in the 300-mm pilot line at AIST"; stated place). Dicing, oxidation and HF release: org not stated.
  `process_name` "300-mm pilot line at AIST (193 nm ArF immersion lithography, <mask type>)".

Missing from the registry (name as printed + locator + role):
- "University of Western Ontario" (poulsen2025 p.1 affiliation; p.10 Acknowledgements: devices "post processed at"
  its facility): fab (post-processing, D440 / D448) on the 3 poulsen2025 rows.
- "University of Western Ontario Nanofabrication Facility" (poulsen2025 p.10 Acknowledgements): facility on the 3
  poulsen2025 rows (child of the university).
- "imec Xplore lab" (wang2026g p.5 Sec. 3): facility on the 14 wang2026g rows if confirmed as an alias of
  `org_xplore_multiuser_cleanroom`.

## Values not entered

- zhang2021a: main-lobe peak power about 720 mW at 24 W input (p.8 Fig. 8(d)), 43 W input withstood (p.8), average
  electrical power 1.23 W per steering state (p.7): no free_space_emitter parameter (gaps below). DC low-power
  propagation losses "1.9 dB/cm and 1.7 dB/cm" (p.2; which run each is not stated). Lens loss 0.5 dB and side-lobe
  loss 9.3 dB (bulk lens / far-field terms of the budget; in the OPA total row's notes). Fig. 4 5-um-pitch OPA far
  field (grating lobes +/-18 deg): device not tied to this paper. Fig. 1(c), (d) power-dependent losses (curves).
  TiN heater phase shifters: no per-shifter metric (only the array-level 1.23 W), not a row.
- wang2026g: platform propagation loss 0.60 +/- 0.17 dB/cm (p.2; platform reported in the authors' ref. [18], p.5,
  D259 / D408). MZI insertion loss 0.18 dB (p.2; MZI-level, origin not stated; in the MMI notes). Fig. 2(a) simulated
  Ppi 49.0 / 47.5 / 1.3 mW: text says L = 200 um, caption says L = 400 um with 2 bridges, neither matches a
  fabricated design (D159). IL / ER of the MZIs: curves only (Fig. 4), "similar" for the three 800 um structures.
  Simulated temperatures / 2.75 mW drive of Fig. 1 (not a Ppi).
- poulsen2025: VpiL 20.13 V um, 16x sensitivity enhancement (calculated), simulated comb displacement 22.4 nm at 5 V,
  simulated sensitivity up to 103 rad/nm, comb / spring dimensions, PhC lattice 500 nm and hole diameter 325 nm
  (no parameter for phase_shifter), slot gap 200 nm on the MMI converter (gap_nm not allowed on mode_converter). All in
  component notes.
- sun2022a: Bezier control points (Table 1 / 4), widened inner width W0 (not printed), cascade peak-to-peak loss
  oscillation 0.35 / 0.46 dB (circular) and 0.02 / 0.035 dB (modified) for 2 / 4 bends at R 1.5 um (p.11 Fig. 9;
  no parameter, simulated vs measured not stated), grating couplers (geometry only, no performance).
- katsura2023: photon lifetime 5.54 ns, Table 1 loss-factor estimates (Avg(1/Qscat), 1/Qabs, sigma_hole; model with
  cited FDTD relations), ideal Q 9.48e6 at 88 deg (Fig. 7), pooled 62-cavity average 3.25e6 and "all > 2 million"
  (spans both rows; in notes), hole radius about 115 nm, W1 710 nm (role-ambiguous width), EB-lithography column of
  Table 1 (cited ref. [30]).

## Judgment calls

1. zhang2021a test waveguides / SSC carry fab AMF from "of our chip" (p.2) plus the AMF fabrication sentence (p.5).
2. zhang2021a damage thresholds (Si 2.15 W, SiN 35 W peak, 90 % survival fits) entered as `power_handling_dbm`
   33.32 / 45.44 dBm `derived` with the definition in condition and notes ("damage threshold, not no-degradation").
3. zhang2021a 0.02 deg longitudinal divergence uses a bulk off-chip cylindrical lens; kept on the OPA row as a system
   value with the lens in condition (headline result). Coordinator may drop it under D411.
4. zhang2021a OPA platform `si_sin_multilayer` (SiN input / splitter, Si phase shifters and emitters); SiN-only parts
   `sin`, Si-only `soi`.
5. zhang2021a loss-budget terms (coupler 1.8 dB, Y tree about 2 dB, SiN-Si about 0.2 dB) `author_estimate` +
   `loss_breakdown` (origin not stated). Y tree as one `splitter.y_branch` row with `excess_loss_db` device_total.
6. wang2026g printed bandwidths (Tables 1-2) entered as `bw3db_khz` `author_estimate`: computed from rise / fall
   times (they match 0.35 / mean(rise, fall); relation not printed). The > 68.6 / > 66.0 kHz rows keep `gt`.
7. wang2026g text vs figure / table conflicts kept with notes (D417): Ppi 0.85 mW (text) vs about 0.75 mW (Fig. 4
   caption); 48.7 / 47.4 mW (text) vs P2pi labels 98.5 / 94.4 mW; fall time 6.6 (Table 1) vs 6.8 us (text); 0.85
   (Table 1) vs 0.84 kHz (Table 2); 48.5 (Table 1) vs 48.55 mW (text).
8. wang2026g full cross-section geometry (width, core, heater width / thickness / gap, BOX, top cladding) repeated
   on all 12 phase-shifter rows (one stack for all designs); heater_length_um per row (p.8 calls the series length
   the heater length).
9. wang2026g MMI losses 0.014 / 0.074 dB `author_estimate` (no measurement shown, origin not stated), stored as
   `excess_loss_db` (printed "insertion losses" beyond the ideal split).
10. poulsen2025 CMC Microsystems as fab (access to foundries for an MPW run, D83d / D398); wang2012 (no fabrication
    wording) was the counter-precedent.
11. poulsen2025 Vpi 0.61 V `derived` (model extraction, Eq. (3)-(4)); wavelength 1585 nm and DC bias 8 V read off the
    Fig. 6(c) label position (`wavelength_inferred` true, uncertainty in notes).
12. poulsen2025 MMI converter `mode_converter.converter` and slot-to-PhC junction `waveguide_platform.other`
    (xiao2022 precedent), both `fabricated` with simulated values only (D80e).
13. sun2022a platform `soi` (Si etch depth not stated; only the grating couplers are called fully etched). TE on all
    rows from p.3 and p.11. SiN radii follow text / tables (8 / 10 / 12 um), not the Fig. 6 caption (10 / 15 / 20 um).
14. katsura2023 split into two population rows by photomask (same cavity design, different lithography mask and
    post-processing history); Qexp = omega tau is a total Q: `q_loaded` (asano2017 / ashida precedents). The PM best
    cavity's wavelength is not printed: population mean used with `wavelength_inferred` true.

## Registry gaps (skipped value + locator + proposed definition)

- free_space_emitter output power: zhang2021a main-lobe peak power about 720 mW (p.8, Fig. 8(d)). Proposal: widen
  `output_power_mw` to free_space_emitter ("optical power in the main lobe / emitted beam as stated; reference plane
  and pulse regime in condition").
- `power_handling_dbm` on free_space_emitter: zhang2021a OPA withstood 43 W input peak (p.8).
- `power_consumption_w` on free_space_emitter: zhang2021a 1.23 W average electrical power per steering state (p.7)
  (also D432 candidate).
- `vpi_l_v_um` (or the D438 candidate `vpi_l_v_cm`) on phase_shifter: poulsen2025 VpiL 20.13 V um (p.8, p.10).
- `actuator_displacement_um` on phase_shifter (D440 candidate): poulsen2025 simulated 22.4 nm per comb at 5 V (p.5).
- `gap_nm` on mode_converter (D533 candidate): poulsen2025 MMI slot gap 200 nm (p.2, p.4).
- `period_nm` and `hole_diameter_nm` on phase_shifter: poulsen2025 PhC lattice 500 nm, holes 325 nm (p.2).
- `photon_lifetime_ns` on resonator: katsura2023 5.54 ns (p.4), "photon lifetime from the emission decay".
- `q_absorption` / `q_scattering` on resonator (D430 candidate): katsura2023 Table 1 (p.7) model estimates.
- `hole_radius_nm` on resonator (D430 candidate): katsura2023 about 115 nm (p.2).
