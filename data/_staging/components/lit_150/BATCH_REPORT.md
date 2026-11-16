# lit_150 batch report

Distilled 2026-11-15 (contract v7). 6 papers, 13 components, 142 metric rows. `merge_component_staging.py --dry-run`: +13 components, +142 metrics, 0 errors (the one warning is on merged row `cmp_lit_ni2025b_pimmwc-m18`, not this batch). Page-1 titles match the source rows for all 6 papers; no correction / erratum, no garbled text layer. chen2023b is the arXiv text of the Optics Letters paper (same title and authors).

| paper | components | metrics |
|---|---|---|
| chen2023b | 3 (2 crossing.mmi, 1 resonator.ring) | 27 |
| xu2019a | 1 (polarization.pbs) | 20 |
| ma2023 | 4 (2 crossing.other fabricated, 1 crossing.other design, 1 mode_converter.mdm_mux) | 36 |
| han2018 | 2 (crossing.other fabricated + design) | 12 |
| wu2017 | 1 (polarization.pbs) | 10 |
| xu2025b | 2 (crossing.swg fabricated, crossing.other design) | 37 |

## chen2023b (x-cut TFLN MMI crossings, resonator-assisted characterization)

- Rows: symmetric 45 deg crossing, asymmetric 0 / 90 deg (z / y) crossing, reference ring.
- Resonator-assisted IL (0.051 / 0.065 / 0.070 dB) and crosstalk (-50.1 / -58.0 / -56.2 dB) are `author_estimate`, method `ring_extraction`. Eq. (1) and Eq. (5) need the group index and ring circumference, and the paper prints neither (D76). The printed +/- uncertainties go in `condition`. Values are assigned to directions in the printed order 45 / 90 / 0 deg (p.4-5).
- Cut-back IL (0.022 / 0.109 / 0.122 dB) `measured`, method `cutback`. Its uncertainty (+/-0.055-0.064 dB) is larger than the 45 deg value, as the paper says.
- Reference ring: Q_L about 300,000 (p.4) and the Fig. 4(a) label 5.2 pm. The wavelength (about 1559.2 nm) is read from the plot axis, so `wavelength_inferred` is true.
- Not entered:
  - Traditional single-crossing crosstalk of about -40 dB (p.4). The paper attributes it to scattered light and a noise floor of about -45 dB.
  - Simulated crosstalk "about -60 dB", stated generically and inconsistent with the 45 deg Fig. 4(d) simulated curve (about -50 to -55 dB).
  - Crossing-embedded ring Q_L 226,000 (kept in the crossing notes).
  - The printed "rib waveguide thickness 250 nm": its role is not stated beyond that wording, so it is not stored as etch depth or film thickness.
- Fab empty: the fabrication sentence is passive. Facility `org_nanosystem_fabrication_facility` ("ASML UV Stepper lithography system (NFF, HKUST)", p.3; xie2024 precedent).

## xu2019a (PC-MMI PBS, SOI)

- Measured at 1550 nm (Fig. 11, p.8):
  - IL TE 0.68 dB, TM 0.81 dB. Scope `per_component`, with grating couplers excluded ("calibrated out", method not described, `unspecified`).
  - ER (`per_db`) TE 32.6 dB, TM 36.7 dB.
- Measured over ranges: TM ER > 23.9 dB over 1500-1630 nm; ER > 20 dB and IL < 2 dB over 1522-1599 nm, one row each for both polarizations.
- Simulated: 0.35 / 0.64 dB IL and 42.9 / 52.1 dB ER at 1550 nm; ER > 20 / IL < 3 dB over 1486-1640 nm (nominal) and over 1486-1616 nm (worst case of fill factor +/-0.02).
- Fab `org_applied_nanotools` ("single-etch electron beam lithography at Applied Nanotools Inc.", p.8). Platform `soi_strip`: single etch plus 500 nm strip interconnects.
- Not entered (registry gaps, values in notes): PC period 390 nm, fill factor 0.3, P_L 11 / P_T 10 periods, W_A 1.5 um, W_S 2 um, L_T 10 um, L_R 44.25 um, minimum feature about 150 nm, and the Fig. 12 bandwidth-vs-minimum-ER curve.

## ma2023 (inverse-designed 3- and 4-channel dual-mode crossings)

- Measured crossing IL:
  - 3-channel: < 1.8 dB (TE0 and TE1).
  - 4-channel: < 1.8 dB (TE0) and < 2.5 dB (TE1).
  - All three are `derived`: the authors subtract the < 2.7 dB back-to-back mode (de)MUX reference circuit from the device totals (4.5 / 4.5 / 5.2 dB; p.6). This arithmetic subtracts one bound from another, as the paper does.
- Measured crosstalk: > 18.4 dB and > 17.0 dB, through the whole device including both (de)MUXs; the paper does not print a crosstalk definition.
- The mode (de)MUX has its own `mode_converter.mdm_mux` test-structure row: < 1.4 dB per (de)MUX (back-to-back value halved, `derived`) and crosstalk > 17.2 dB.
- Simulated values (nominal design and hole-diameter tolerance) are entered as stated. The three-channel direct crossing (Fig. 9) is a `design` row; its 1540-1560 nm span is read from the plot axis.
- Footprints are `derived` from the Table 1 "4.32 x 4.32" and "6.68 x 6.68" values (design-region width squared). n_inputs / n_outputs come from the Table 1 channel count (3 x 3, 4 x 4).
- Conflict (D417 note): the conclusion says the 4-channel device has "three 0.9 um-wide waveguides" (p.9); p.3 says four.
- Not entered (registry gap): hole diameter 90 nm, hole row / column spacing 104 / 120 nm (3-channel) and 99.4 / 160 nm (4-channel).
- Platform `soi`: the etch of the access waveguides is not stated.
- Missing fab org: **National University of Defense Technology** (fab). Author contributions: "Hansi Ma and Junbo Yang fabricated the devices" (p.9); both authors at NUDT (p.1). Fab is left empty until the org exists.

## han2018 (ultra-compact SOI crossing, lens-like etched structures)

- Measured (cut-back, 1528-1567 nm, Fig. 8(b)): IL < 0.28 dB `measured`; crosstalk about -30 dB.
- Simulated:
  - IL < 0.175 dB and crosstalk < -37 dB over the C band.
  - Crosstalk dip about -48 dB near 1550 nm.
  - Worst-case crosstalk < -32.8 dB for +/-10 nm deviations at 1550 nm.
- The first, hole-based PSO design (Table 1) is a `design` row (mean IL about 0.22 dB, simulated). Fig. 7 shows the lens-like design as the fabricated one, and fabrication of the hole design is not stated. Its C band is inferred from the C-band figure of merit.
- Not entered:
  - "About 0.25 dB for longer wavelengths" (no span).
  - Table 1 / Table 2 taper and lens parameters (C1 / C2 roles only shown in a sketch; lens offset and radii have no parameter).
  - Over-exposure 6.4 nm (notes).
- Fab empty: passive sentence; the authors are at Nanjing University and NUDT.

## wu2017 (PBS with three cascaded bent directional couplers)

- Measured:
  - ER about 40 dB at about 1551 nm for both polarizations (p.5). The > 35 dB headline in the abstract / Table 1 is in the notes.
  - Excess loss < 0.35 dB (TE) and < 0.1 dB (TM) at the central wavelength, from the ten-PBS cascade. Stored in `insertion_loss_db` with the paper's term in notes, because `excess_loss_db` is not allowed on polarization. Basis `measured`, method `cutback`: no cascade total or division is printed (D167 / D452).
  - TM EL < 1 dB over 1490-1630 nm.
- Simulated: TE EL < 1 dB over 1400-1650 nm (l1 = 6 um).
- Fab `org_zhejiang_university`: first-person "we fabricated" (p.5, p.6) and all three authors at Zhejiang University (D554 precedent).
- Not entered (registry gaps):
  - ER criterion bandwidths: measured TM > 20 / 25 / 30 dB over about 135 / 95 / 70 nm; simulated 145 / 110 / about 70 nm.
  - EL criterion bandwidths: about 140 / 85 nm.
  - Bend radius R2 15 um, gaps 257.5 / 320 nm, DC #3 length 6 um, coupling angles 28 / 32 deg.
  - Core-width sibling devices (dw = +/-20, +/-40 nm): summarized only as ER > 20 dB over > 100 nm. No row, because there is no metric outside the criterion-bandwidth gap.

## xu2025b (polarization-insensitive SWG crossing, SOI)

- Measured (cut-back over 3 / 5 / 7 crossings):
  - IL 0.52 dB (TE0) and 0.31 dB (TM0) at 1550 nm.
  - IL < 0.78 / < 0.43 dB over 1500-1600 nm.
  - Crosstalk < -31 / < -33 dB.
- Simulated values at 1550 nm and over 1400-1700 nm are entered, plus three tolerance cases (width, hole size, both: +/-10 nm).
- The direct 800 nm crossing reference is a `design` row.
- Fab empty: passive fabrication sentences and a single author, with no org named.
- Not entered (registry gaps): duty cycles eta1-eta11 (0.35-0.65; `fill_factor` is not allowed on crossing), and simulated reflection < -7 dB (TE0) / < -18 dB (TM0) (`back_reflection_db` is not allowed on crossing; D561 / D573).

## Judgment calls

1. chen2023b resonator-assisted IL / crosstalk are `author_estimate` (D76: unprinted n_g and L), although they are the paper's headline measured result. The alternative is `derived`, if the coordinator holds that the ratio of the two rings cancels most of the dependence on n_g and L.
2. chen2023b crosstalk rows carry `wavelength_nm` 1550: the per-direction values are printed without a wavelength, and the conclusion ties the "< -50 dB" summary to 1550 nm.
3. ma2023 crossing IL is `derived` from the authors' own subtraction of bounds. A bound minus a bound is not strictly a bound, but the paper states it that way.
4. wu2017 excess loss is stored as `insertion_loss_db` (class allowance). The merged PBS precedent uses `insertion_loss_db` throughout.
5. Platforms:
   - `soi_strip` for xu2019a (single etch, strip interconnects), wu2017 ("etch through the silicon core layer"), xu2025b ("fully" etched) and han2018 (500 x 220 nm air-clad waveguides).
   - `soi` for ma2023 (etch of the access waveguides not stated).
6. Simulated-only reference designs (ma2023 and xu2025b direct crossings, han2018 hole design) are `design` rows with simulated metrics.

## Registry gaps (skipped value + locator + proposed definition)

- `criterion_bw_nm` (polarization, splitter; D539 candidate): full width over which a stated ER / EL criterion holds, criterion in condition. Skipped values: wu2017 135 / 95 / 70 nm (p.5) and 140 / 85 nm (p.6); xu2019a Fig. 12 curve (p.8).
- `period_nm`, `n_periods`, `fill_factor` on polarization (D439 candidate): photonic-crystal / grating geometry inside a PBS. Skipped: xu2019a 390 nm, P_L 11 / P_T 10, f = r / period 0.3 (p.6 Table I).
- `gap_nm`, `radius_um` / `min_bend_radius_um`, `coupling_length_um`, `coupling_angle_deg`, `taper_length_um`, `port_width_um` on polarization (D439 candidates). Skipped: wu2017 257.5 / 320 nm, R2 15 um, l1 6 um, 28 / 32 deg (p.3-4); xu2019a L_T 10 um, W_A 1.5 um (p.6 Table I).
- `fill_factor` on crossing (D573 candidate). Skipped: xu2025b eta1-eta11 (p.2 Table I).
- `back_reflection_db` on crossing (D561 / D567 candidate). Skipped: xu2025b simulated < -7 / < -18 dB (p.3).
- `hole_diameter_nm` on crossing (D430 / D431 candidates name it for other classes). Skipped: ma2023 90 nm (p.3, p.5); han2018 hole radius 40 nm (p.3 Table 1).
- `min_feature_size_nm` (D566 / D573 candidate). Skipped: xu2019a about 150 nm (p.3).

## Missing orgs

- National University of Defense Technology: fab, ma2023 (p.9 author contributions; p.1 affiliations).
