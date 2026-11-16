# lit_148 batch report

Distilled 2026-11-15. Six papers, 37 components, 360 metric rows. `merge_component_staging.py --dry-run`: 0 errors (the
one warning concerns `cmp_lit_ni2025b_pimmwc`, another batch). Page-1 titles match the source rows for all six papers;
no correction / erratum, no garbled text layer.

| paper | components | metrics |
|---|---|---|
| lit:chen2006 | 4 | 23 |
| lit:lu2024a | 3 | 15 |
| lit:sun2017 | 1 | 16 |
| lit:wu2020a | 1 | 20 |
| lit:li2018a | 4 | 39 |
| lit:sacher2019 | 24 | 247 |

## lit:chen2006 (IEEE PTL 2006, MMI crossing on 340 nm SOI)

- Rows: fabricated optimized MMI crossing (Lm ~4.3 um), fabricated plain crossing used as the control, and two 2D-FDTD design rows (MMI design Lm 4.9 / Lt 3 / Wb 0.3 um, plain 0.3 um crossing).
- Per-crossing losses 0.4 / 1.3 dB are `derived` (printed cascade excess ~4 / ~13 dB over 10 crossings, divided by 10). The ~0.2 dB wavelength dependence (wdl) is `derived` in the same way.
- Not entered: Fig. 2(e) cascade transmissions at 1570 nm (plot only), the 6-8 dB average cascade improvement and the 1-3 dB excess for a 0.2 um Lm deviation (both cascade-level comparisons), and measured crosstalk (qualitative CCD images only).
- Judgment calls: the simulated design (Lm 4.9, Lt 3, Wb 0.3 um) differs from the fabricated dimensions (Lt ~4, Wb ~0.35 um), so it is a separate `design` row and is not attached to the fabricated Lm 4.9 sweep member. The "~" fabricated widths and slab height are `derived` (um -> nm), with a note that no measurement method is stated.
- Fab: org_the_hong_kong_university_of_science_and_technology (first-person "we ... fabricate", both authors HKUST; D72).

## lit:lu2024a (IEEE PJ 2024, elliptical Si3N4 crossing on an MWP chip)

- Rows: elliptical crossing (fabricated, measured and 3D-FDTD values on one row, D80e), direct crossing (design, simulated 0.7 dB), and the MRR filter arrays (`wdm.mrr`, 300 mW heater power for > 40 GHz tuning).
- 0.086 dB per crossing is `measured`: a linear fit over 0-15 crossings (D80a). The wavelength span 1540-1560 nm is from p.1.
- Not entered: reflection (< -44 dB measured, < -50 dB simulated), because the registry has no reflection parameter for crossings. Also not entered: the 1.2 dB / 14-crossing difference (same measurement as the fit), the Lcr / Wcr sweep (~0.07 dB, < 0.04 dB change), the 200 x 80 um area of two crossings, and the ~9.8 dB direct-crossing RF loss (a theoretical system estimate).
- Stack geometry comes from the Fig. 1(b) labels, entered as `extracted_from_figure`. The 1.4 um width is `derived`.
- Fab empty: "We design and fabricate" with authors at Tsinghua University and China Mobile Research Institute (not unambiguous, D80b).

## lit:sun2017 (OE 2017, ALIG asymmetric-MMI PBS)

- One row, `polarization.pbs` on platform `si_sin_multilayer`. Measured: IL < 1 dB for TE and TM (one statement, `pol both`, C-band) and PER ~17-18 dB (Bar) / ~25 dB (Cross). Simulated: IL < 0.4 dB.
- Not entered: measured undesired transmissions (these are the inputs to the PER rows), simulated undesired-port transmissions (no suppression parameter for polarization devices besides PER), and the fabrication-tolerance study (in ref. [22]).
- Fab: org_university_of_toronto. Fabrication sentences are passive, but the acknowledgment thanks the Toronto Nanofabrication Centre (TNFC) "in device fabrications" (p.10), which names the place of fabrication (D448). The facility belongs in `facility_org_ids`, but TNFC is not in the registry.

## lit:wu2020a (OE 2020, SWG-MMI polarization-insensitive crossing)

- One row, `crossing.swg`, platform `soi_strip` (full 220 nm etch, D434).
- The paper's measured values conflict with each other:
  - p.7 / Fig. 7: TE ~1.1 dB (averaged) and TM < 3 dB.
  - p.8 conclusion: TE 1 dB and TM 1.6 dB.
  - Abstract: IL < 1 dB for both polarizations and PDL < 0.6 dB.
- All of these are entered with conflict notes (D417) except the abstract's IL < 1 dB, which conflicts with the TM values. The conclusion values and the PDL have no stated wavelength, so they carry `band c_band` with `wavelength_inferred`.
- Not entered: the focused TE / TM grating couplers. They have geometry only (period 640 / 1020 nm, duty 50 %, 70 nm etch) and a design centre of 1550 nm with the design attributed to ref. [22]. Also not entered: the 20 um bends (geometry only) and the beat length of 3.1 um (MMI length not printed).
- Fab empty: passive wording, authors at three unrelated orgs.

## lit:li2018a (Optica 2018, transformation-optics multimode star crossing)

- Rows:
  - 4-channel 3-mode TF-MWC (fabricated): measured and simulated losses per mode (TE0 / TE1 / TE2) and crosstalk, plus a simulated 1308-1702 nm envelope.
  - D-MWC direct-crossing control (fabricated): measured and simulated values.
  - 5-channel 4-mode TF-MWC (`design`): simulated only.
  - 1D chirped grating coupler: 3-dB bandwidth ~40 nm `author_estimate` (no spectrum shown), fiber angle 10 deg.
- Not entered:
  - D-MWC TE2 crosstalk printed as +9.08 dB measured and +12.01 dB simulated. The crosstalk exceeds the through transmission and the reference power is not defined, so the suppression would be negative. It is kept in the notes.
  - Fisheye radius R = 25 / 34 um (`radius_um` is not allowed for crossings).
  - The 5x4 crossing's 1-dB bandwidth of 1241-1720 nm (no bandwidth parameter for crossings).
  - The ADC mode multiplexers: geometry only (46.2 / 57.5 um long, 0.5 / 1.05 / 1.55 um widths, 130 nm gap), no performance.
  - The supplement (S1-S5), which is not in the cached text.
- Fab empty: passive / first-person wording with four unrelated orgs.

## lit:sacher2019 (OE 2019, visible SiN on thinned 200 mm wafers, AMF)

- Rows:
  - 8 straight waveguides (3 wafers x widths). All 76 Table 3 cells are entered as `prop_loss_db_per_cm` ranges over each wavelength span. They are die-averaged (statistic mean, n = dies), and the footnote truncations are applied (502-540, 552-570 nm).
  - 5 bend designs (bend loss upper bounds per polarization span).
  - 3 edge couplers (per facet, `loopback_half` measured with the 1.798 mm waveguide included, D452).
  - 3 MMI crossings (one per wafer, same design).
  - 4 MMI 1x2 dividers (W1-D1, W3-D1, W1-D2, W2-D3).
  - The Wafer 2 neurophotonic-probe grating emitter (fiber-to-free-space transmission, second-order suppression as `slsr_db`, FWHM divergences).
- Fab: org_amf on every row ("using the Advanced Micro Foundry (AMF) foundry process", p.2). `process_name` is left empty because no process name is printed.
- Judgment calls (family-level statements):
  - Crossings: "minimum loss per crossing ranged from 0.07-0.09 dB" holds for every wafer and polarization. It is entered on each crossing row as a best-value range, with a note.
  - Dividers: the minimum excess loss 0.19-0.47 dB, the < 1 dB excess-loss bandwidth 70-172 nm (`bw_1db_nm`, definition in condition, D539) and the split ratio within 1.1 dB of 50:50 are printed once for all four combinations. They are entered on each row as envelopes with notes.
  - Per-device minima were not read off Figs. 8 and 11 (low resolution). The coordinator may prefer notes-only under D254 / D541.
- Width basis: straight waveguide widths are `measured` (X-TEM / X-SEM, p.6). Bend widths are `measured` where the same width was measured on that wafer. The W1 340 nm bend width is `design_target` (no measured straight waveguide of that width).
- Not entered:
  - Text restatements of Table 3 upper bounds (abstract <= 2.8 / <= 1.9 dB/cm; Wafer 2 340 nm <= 4.1 / 2.8 / 3.3 / 2.3 dB/cm; Wafer 1 <= 8.8; Wafer 3 / Wafer 1 <= 3.4 / <= 4.4).
  - Measured SiN refractive indices, simulated single-mode cutoff widths (Table 2) and the setup fiber PER > 20 dB.
  - Crossing loss < 0.1 dB over >= 58 nm and < 0.2 dB over >= 138 nm (no bandwidth parameter for crossings).
  - Divider aperture spacing dap (760 / 860 nm; centre vs gap not defined).
  - Probe far-field background < -23 dB (camera-limited) and the ~50 um wafers (not characterized).

## Missing fab / facility orgs

- Toronto Nanofabrication Centre (TNFC): facility, lit:sun2017 p.10 Acknowledgments ("We thank the Toronto Nanofabrication Centre (TNFC) in device fabrications"). Parent: University of Toronto.

## Registry gaps (skipped values, proposed definitions)

- `back_reflection_db` for `crossing`:
  - lu2024a reflection < -44 dB measured (p.3-4, Fig. 7) and < -50 dB simulated (p.2, Fig. 2(c)).
  - wu2020a simulated back reflection < -13 dB (p.4, Fig. 3).
  - Proposal: widen `back_reflection_db` to crossing.
- Crossing bandwidth:
  - sacher2019 loss < 0.1 dB over >= 58 nm and < 0.2 dB over >= 138 nm (p.10).
  - li2018a 5x4 1-dB bandwidth 1241-1720 nm (p.4).
  - Proposal: allow `bw_1db_nm` for crossing (a criterion bandwidth needs the definition in the condition).
- `fill_factor` and `tip_width_nm` for `crossing`: wu2020a SWG duty cycle 80 % and SWG taper tip 100 nm (p.2, p.4).
- `gap_nm` and `min_bend_radius_um` for `polarization`: sun2017 g = 100 nm, R = 10 um (p.5). `layer2_thickness_nm` for polarization would also suit the ALIG Si3N4 layer (sun2017 t2 = 350 nm; entered as a second `core_thickness_nm` row with a condition).
- `radius_um` for `crossing`: li2018a fisheye radius 25 / 34 um (p.2-3).
- `tuning_range_ghz` (wdm / resonator): lu2024a MRR tuning > 40 GHz at <= 300 mW (p.3, Fig. 4(c)); kept in the condition of the `tuning_power_mw` row.
