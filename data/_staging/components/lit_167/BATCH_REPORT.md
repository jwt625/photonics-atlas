# lit_167 batch report

Distilled 2026-11-16 under the pic-component-distill skill (Contracts v4-v7). Papers: lit:catalalahoz2026a,
lit:zheng2024. Totals: 9 components, 47 metric rows. `merge_component_staging.py --dry-run`: +9 components,
+47 metrics, 0 errors (the one warning printed belongs to merged row cmp_lit_ni2025b_pimmwc, not this batch).

Page-1 title check: both cached texts are their source rows' papers (arXiv 2502.19080 v1 "Non-uniform programmable
photonic waveguide meshes"; arXiv 2402.16513 v1 "Photonic Neural Network Fabricated on Thin Film Lithium Niobate for
High-Fidelity and Power-Efficient Matrix Computation"). Both are arXiv preprints of the Laser & Photonics Reviews
versions; the journal versions were not read. Neither is a correction / erratum; no garbled text layer.

## lit:catalalahoz2026a - 8 components, 40 metric rows

Overlap check with lit:catalalahoz2026 (same group, merged, 11 rows): no overlap. catalalahoz2026 is the non-volatile
Si-BTO FPPGA on a CEA-Leti / Lumiphase chip; catalalahoz2026a is a separate AMF-fabricated thermo-optic SOI mesh
(21 TBUs, TiN heaters). No device or value appears in both; every row carries a cross-note to that effect. The
conference version of this work (Catala-Lahoz and Capmany, IEEE SUM 2024, Supp. ref. [2]) is not in data/components.

| component | class | metrics |
|---|---|---|
| cmp_lit_catalalahoz2026a_tbu | switch_fabric.other | 3 (about 0.48 dB per TBU, author_estimate; MZI extinction about 51 dB read off Supp. Fig. 16; 900 um side) |
| cmp_lit_catalalahoz2026a_heater_ps | phase_shifter.thermo_optic | 3 (P_pi 1.26 mW, author_estimate; TiN 120 nm; Si 220 nm) |
| cmp_lit_catalalahoz2026a_mmi | splitter.mmi | 3 (foundry-spec 0.15 dB, `specification`; 2x2) |
| cmp_lit_catalalahoz2026a_wg | waveguide_platform.straight | 3 (foundry-spec 1.1 dB/cm, `specification`; 500 x 220 nm) |
| cmp_lit_catalalahoz2026a_edge_coupler | fiber_chip_coupler.edge | 4 (7 dB loop measured, 3.5 dB loopback_half derived, foundry-spec 1.3 dB per coupler, 24 ports) |
| cmp_lit_catalalahoz2026a_vernier_x3p6 | resonator.coupled_rings | 8 (FSR 47.84 GHz total, 11.96 / 15.95 GHz single rings, kappa 32.85 / 11.22 %, 7.45 mW, round trips 6000 / 4500 um) |
| cmp_lit_catalalahoz2026a_vernier_x6 | resonator.coupled_rings | 8 (79.74 / 13.29 / 15.95 GHz, kappa 37.14 / 15.3 %, 8.92 mW, 5400 / 4500 um) |
| cmp_lit_catalalahoz2026a_vernier_x10 | resonator.coupled_rings | 8 (132.9 / 13.29 / 14.76 GHz, kappa 22.82 / 14.28 %, 10.15 mW, 5400 / 4860 um) |

Values not entered and why:
- Phase-shifter "tuning speed of 3 kHz" (p.5): not defined (no 3-dB / rise-time wording), so not `bw3db_khz`; in
  component notes.
- Breakdown current 8.39 mA of the phase shifter (p.6): no parameter.
- Half-round-trip loss factors alpha (Table 1) and alpha = 0.85 for a hexagonal ring (p.7): model inputs, no parameter.
- Sampling times T of single and coupled cavities (62.69-83.61 ps, 20.90 / 12.54 / 7.52 ps; Fig. 6, Table 1): equal
  to 1 / FSR, no parameter; in notes.
- Coarse tuning steps 15.95 / 14.76 GHz and fine steps 3.2 GHz per 0.35 mW per phase shifter (p.6-7): Vernier-filter
  tuning steps, no parameter (a pm/mW value would need an assumed wavelength); in notes.
- Phase settings phi_CT / phi_FT (Table 1): programmed set points.
- Chip size 2.8 x 4.3 mm2 (p.10) and Fig. 3(b) labels 3.9 mm x 2.1 mm: no mesh row (no mesh-level performance value,
  rule 9); in TBU notes.
- Projections: ~0.08 dB per TBU (ref. 46), ~100 um TBU, 120 GHz / 1.2 THz bandwidths (refs. 28, 45), 450-900 um
  state-of-the-art cell lengths (refs. 1, 2): cited.

Judgment calls:
1. Foundry specifications (waveguide 1.1 dB/cm, MMI 0.15 dB, edge coupler 1.3 dB at 1550 nm, p.5) entered with basis
   `specification` and condition "foundry specification" on their own rows. They are AMF nominal values, not
   measurements of this chip; the coordinator may prefer to drop the waveguide / MMI rows (they have no other
   performance metric) or exclude them from the foundry benchmark (`exclude_values`). The MMI value is printed as
   "insertion losses" and stored as `excess_loss_db` (D43).
2. TBU loss 0.48 dB and P_pi 1.26 mW: `author_estimate` (origin not stated; no method or figure tied to the numbers).
   Supp. Fig. 16 (one heater) shows nulls about 2.34 mW apart, i.e. about 1.17 mW per pi, noted on the phase-shifter
   row, not entered.
3. TBU extinction 51 dB (approx): figure read of the deepest data point of the first null of Supp. Fig. 16 (+/-1 dB;
   fit dips to about -58 dB, second null data about -44.5 dB); sampling-limited, so a lower estimate of the true
   extinction. The panel is titled "PUC 21 - PS 34" (paper's own label).
4. TBU classed `switch_fabric.other` (catalalahoz2026 `nv_puc` precedent, D158) rather than `mzi_mesh`.
5. Vernier filters as `resonator.coupled_rings` (not `wdm`, D400: not channel filters in a WDM path). Single-ring FSRs
   (Table 1) `measured`: they match the measured single-cavity pulse periods (Fig. 6(a)-(d)). Coupling values kappa
   (Table 1) entered as `power_coupling_pct`, basis `simulated`: chosen by the paper's optimization routine and used as
   simulation inputs (D82a / D83f). Total circuit power P_T as `tuning_power_mw`, `author_estimate` (origin not
   stated). Round-trip lengths `length_um` derived from the printed mm (D157; cui2023a ring-length precedent).
6. Cavity labels conflict inside the paper: p.6 pairs LC2+LC3 (x3.6), hexagon+LC3 (x6), hexagon+LC1 (x10); p.5 says
   LC1 and LC2 give x10 and x6; Supp. Note 6 (p.25) pairs LC2 / LC1 with the hexagon for 6 / 10. Rows are labelled by
   the Table 1 ring lengths only; conflict in notes.
7. Edge coupler: 7 dB loop measured (fiber_to_fiber, includes loop waveguide), 3.5 dB per input as printed
   (loopback_half, derived). Wavelength 1550 nm inferred (calibration laser) on the 7 / 3.5 dB, TBU and P_pi rows.

Missing fab / facility orgs: none (Advanced Micro Foundry = `org_amf`, p.10 Sec. 6.1). No facility acknowledged
(funding only: ERC, NextGenerationEU / Spanish ministry, Generalitat Valenciana, p.11).

Registry gaps:
- None blocking. Possible candidate: `tuning_step_ghz` for programmable / Vernier filters (coarse 15.95 / 14.76 GHz, fine 3.2 GHz; p.6-7), definition "frequency step of the filter response per
  programmed tuning operation (operation in condition)". Low priority.

## lit:zheng2024 - 1 component, 7 metric rows

| component | class | metrics |
|---|---|---|
| cmp_lit_zheng2024_zen1_mesh | switch_fabric.mzi_mesh | 7 (MZI ER 41.2 dB bar / 38.4 dB cross, measured; on-chip loss ~3.1 dB author_estimate de_embedded; 4 x 4 ports; 500 nm TFLN; 1.5 um SiO2 cladding) |

Values not entered and why:
- EO phase shifter / MZI modulator values (rule 2, modulator metrics stay with the EO atlas; lit:wu2023a precedent,
  same group): V_pi 7.33 V (p.6, Fig. 3(a)), rise / fall time 180 ps limited by the < 5 GHz AWG (p.6, Fig. 3(b)), EO
  S21 3-dB bandwidth over 20 GHz (p.6, Fig. 3(c)), phase-shifter capacitance 15 fF (simulated, p.7), 5 mm
  phase-shifter length (p.6). EO-atlas candidate: zheng2024 is not in `../eo-modulator-atlas`.
- Fidelity <F> = 0.985 +/- 0.003 over 1000 random SU(4) targets (p.9, Fig. 3(g)): no parameter (registry gap below).
- 0.64 TOPS (computed from the 20 GHz bandwidth), 33.5 fJ/OP and 134 fJ per charge (calculated from the simulated
  15 fF): estimates with no parameter.
- Classification accuracies (Circle 96.25 / 99.00 %, Moons 94.50 / 92.00 %, Iris 88.33 / 90.0 %, MNIST 88.5 / 89.3 %):
  application level.
- DC split-ratio fluctuation of about 10 % (p.20): stated for PLACE directional couplers in general, not a measurement
  of this chip; 30:70 split ratio of the Fig. S2 simulation: simulation setting. No DC row (no measured DC value).
- Waveguide loss 0.027 dB/cm (Supp. ref. [1]) and ~3 dB/m (refs. 24, 25), 0.1 nm CMP roughness (ref. [1]): cited.
- "Extinction ratio of approximately -40 dB" (p.4): design intent; the measured 41.2 / 38.4 dB are entered.
- Total waveguide path about 20 cm (p.6): not a component dimension; in notes.

Judgment calls:
1. Fab empty. "Our device is fabricated using a home-developed technology" (PLACE, p.19 Supp.) is an own-process
   statement (D84a), but the authors are at East China Normal University (`org_east_china_normal_university`) and
   SIOM (`org_shanghai_institute_of_optics_and_fine_mechanics`) plus collaborative centers; the fabricating org is
   not unambiguous (D80b / D154). Coordinator question: accept empty (as merged lit:wu2023a) or set ECNU (7 of 8
   authors, PLACE group) under D84a.
2. `process_name` "PLACE" as printed (Contract v7: named process without a named foundry; fab empty). lit:wu2023a
   left `process_name` empty for the same process; the coordinator may align one way.
3. Platform empty: the waveguide cross-section (rib / strip, etch depth) is not stated (D422 / D423), as wu2023a.
4. ER rows and the 3.1 dB row: wavelength 1550 nm and TE inferred from the setup (p.20 Supp.). The 3.1 dB "on-chip
   loss" (conclusion, p.10) is `author_estimate`, scope `de_embedded`, method `unspecified`: no measurement or
   coupling-loss subtraction is described.
5. ER on the mesh row with "representative MZI" in the condition (wu2023a precedent); the paper does not say which MZI
   type (3-DC mesh MZI or 4-DC generator / analyzer MZI).

Missing fab / facility orgs: none needed (fab empty by ruling; no facility acknowledged, funding only, p.11). NANOLN
(wafer supplier, p.19 Supp.) in component notes only.

Registry gaps:
- `fidelity` (switch_fabric, unit 1): mean matrix fidelity F = Tr(|U_target^dagger U_exp|) / N of a programmable
  unitary processor over a stated set of targets (n_samples, statistic mean / std in condition). Skipped value:
  zheng2024 0.985 +/- 0.003, 1000 targets, p.9 / Fig. 3(g). The merged wu2023a notes also hold a matrix-deviation
  figure without a parameter.
