# lit_240 batch report

Papers: lit:paredes2021, lit:wang2022c, lit:jiang2021, lit:liao2016. Page-1 titles match the source rows; no garbled
text layer; none is a correction. verified_on 2026-11-20. Dry run of `merge_component_staging.py`: +9 components,
+131 metrics, 0 errors; the one warning names the merged row cmp_lit_ni2025b_pimmwc, not in this batch.

| paper | components | metric rows |
|---|---|---|
| paredes2021 | 1 | 15 |
| wang2022c | 2 | 48 |
| jiang2021 | 4 | 53 |
| liao2016 | 2 | 15 |

All mode (de)multiplexers and mode splitters are `mode_converter.mdm_mux` (liao2024 / yu2025 mode-splitter precedent).

## paredes2021 (dual-band O + C two-mode tapered-ADC (de)MUX, IEEE Photonics J. 2021)

Rows:
- `mode_converter.mdm_mux` back-to-back link (fabricated, `soi_strip`: "conventional strip waveguide", single etch).
  Measured: IL < 1.2 dB (1260-1360 nm), < 0.8 dB (1500-1600 nm); crosstalk > 17 dB (O), > 16 dB (C / near L).
  Simulated (one MUX): TE0-TE0 crosstalk > 30 dB in both bands (one row, band unspecified), access-path IL < 0.1 dB
  (1550) / < 0.5 dB (1310), conversion loss < 0.7 dB under +/-10 nm width error. Geometry: Wa 500 nm, bus taper
  950-1100 nm, L 70 um, 5 um taper, 75 um length, 220 nm core, 2.2 um cladding.

Not entered:
- Coupling gap g 100 nm (p.5): `gap_nm` not allowed for mode_converter.
- Table 1 "This work" row: repeats the text values; other rows are cited works.

Fab / facility:
- Fab `org_applied_nanotools` ("fabricated using electron-beam lithography with plasma etching at Applied Nanotools
  (Canada)", p.5).
- Missing facility org: "Core Technology Platform Facility (CTP)" of NYUAD (p.9 Acknowledgment, thanked "for the
  analytical and material characterization"); borderline facility (characterization use), left empty. "NYUAD
  Photonics Lab" (same sentence) is a group lab, not entered.

Judgment calls:
1. Measured IL scope `de_embedded`, method `unspecified`: the paper calls Fig. 7 "normalized transmission" (curves sit
   at 0 dB) but never names the normalization reference. Alternative: `unspecified`.
2. Printed crosstalk kept with D417 conflict notes: the Fig. 7(a) I2-O1 trace peaks near -13.5 dB (around 1.285 and
   1.325 um), above the printed "lower than 17.0 dB" O-band bound and the "better than 16 dB" headline.
3. Simulated tolerance "< 0.7 dB" kept with a conflict note: Fig. 5 shows the 1310 nm curve at about -1.25 dB for a
   -10 nm deviation.

## wang2022c (multi-band four-mode counter-tapered ADC (de)MUX, Opt. Express 2022)

Rows:
- `mode_converter.mdm_mux` four-mode link (fabricated, `soi_strip`: "fully etched"): per-mode measured IL and
  crosstalk for TE0-TE3 in 1290-1360 nm and 1510-1580 nm (16 rows, `de_embedded`, normalized to identical GCs,
  `reference_structure`); simulated per-ADC ILs at 1310 / 1550 nm for TE1-TE3 (6), Fig. 3 all-channel bounds (4),
  TE1 width / gap tolerance (4, band unspecified); Table 2 geometry per mode (9), Table 3 length 66 um, 220 nm core,
  3 um BOX, 1 um cladding.
- `mode_converter.mdm_mux` conventional (untapered) TE1 ADC, `row_kind design`: simulated IL 0.35 / 1.02 dB at
  1310 / 1550 nm, 350 / 730 nm widths, Lc 13.5 um.

Not entered:
- Gap 100 nm (all ADCs): `gap_nm` not allowed for mode_converter.
- Total bandwidth 140 nm (two 70 nm windows; conclusion, Table 3): no parameter fits a combined two-window span.
- Table 1 calculated optimal bus widths (MODE solver) per mode and wavelength: design inputs, not a component.
- Simulated minimum coupling lengths L01 13.2 um / L02 4.9 um: in the design-row notes only.
- Aggregate abstract values (< 4.7 / < 3.5 dB, < -10.1 / < -11.8 dB): the maxima of the per-mode rows.

Fab / facility: fab empty (passive "were fabricated", all authors Shanghai Jiao Tong University, D80b); facility
`org_center_for_advanced_electronic_materials_and_devices` (AEMD thanked "for the support in device fabrications",
cai2021 precedent).

Judgment calls:
4. C-band IL conflict: p.2 introduction says "lower than 3.2 dB" for all modes; abstract says < 3.5 dB and p.6 gives
   3.5 dB for TE2. Per-mode values entered, conflict in notes (D417).
5. Two identical link instances with O-band and C-band GCs are one design: one component row with band conditions.

## jiang2021 (bridged-SWG mode splitting, TM0 / TM1, JLT 2021)

Rows:
- `mode_converter.mdm_mux` mode-splitting circuit (MUX + BSWG splitter + DeMUX): measured IL 0.99 / 1.8 dB and
  crosstalk 21.8 / 22.1 dB at ports I1 / I2 (center wavelength, 1550 nm inferred), 3-dB bandwidths 73 nm
  (1500-1573 nm) and ~100 nm; simulated circuit IL 0.81 / 0.43 dB and +/-20 nm tolerance bounds (IL < 3.9 / 1.1 dB,
  crosstalk > 18.4 / 18.8 dB); stack geometry.
- `mode_converter.mdm_mux` TWC MUX-DeMUX link (Fig. 8): measured crosstalk > 13.5 dB (I1) and > 24 dB (I2), IL
  2.25 dB (I1, center) and < 4.86 dB (I2, 100 nm), 3-dB bandwidth > 45 nm (1513-1558 nm); simulated single-(De)MUX
  IL / crosstalk (access and bus inputs, at 1550 and over 1500-1600 nm); Table I widths / taper.
- `mode_converter.mdm_mux` BSWG ADC mode splitter (de-embedded from the circuit, Fig. 9): crosstalk > 22.2 dB over
  1500-1588 nm and 3-dB bandwidth > 88 nm for TM1; crosstalk > 10 dB and IL < 3 dB (scope unspecified) for TM0;
  bridge widths, Lc 5.75 um, four taper lengths.
- `fiber_chip_coupler.grating` TM grating coupler: 9.2 dB per port at 1550 nm; Fig. 7 labels 18.4 / 27.2 / 40.6 dB;
  period 980 nm, duty cycle 0.46 (undefined, D253), etch 70 nm.

Not entered:
- Simulated splitter IL 0.41 / 0.53 dB, crosstalk -19.6 / -27.8 dB, bandwidths 430 / 372 nm: the authors' ref. [7]
  (D259).
- Operating bandwidths for XT < -15 dB, 84 nm (1500-1584 nm) and 100 nm (p.5): no mode_converter parameter
  (`xt_bandwidth_nm` is switch_fabric only).
- Gaps g 200 nm (TWC and BSWG ADC), BSWG pitch 250 nm and a 125 nm: `gap_nm` and `subwavelength_period_nm` not
  allowed for mode_converter; in notes.
- La 29.5 um / Lm 46.25 um (Table I): roles not defined in the text; in notes. S-bend sizes: no parameter.
- Table II "This work" row: repeats measured values.

Fab / facility: empty on all rows (passive fabrication sentences; both authors at Nanjing University of Posts and
Telecommunications, D80b). No facility named.

Judgment calls:
6. Port vs mode labels conflict: p.5 ties 0.99 / 1.8 dB and 84 / 100 nm to ports I1 / I2, while the abstract and
   conclusion call them fundamental / first-order; by the p.2 description port I1 is the TM1 (first-order) path.
   Values entered by port with the conflict in the component notes.
7. GC 9.2 dB/port as `loopback_half` (measured, method loopback): the Fig. 7 peak label -18.4 dB is twice 9.2 dB; the
   paper does not describe the measurement. The three Fig. 7 labels are `unspecified` scope (caption says "the
   grating coupler", value matches two couplers). The auditor may prefer `per_coupler` / `unspecified` for 9.2 dB.
8. Fig. 8 link losses scope `unspecified` (normalization stated only for Fig. 6). Splitter TM0 IL < 3 dB scope
   `unspecified` (the paper says O1 was not normalized, so the MUX bus path may be included).
9. Platform `soi`, not `soi_strip`: the device-layer etch depth is not stated (only the 70 nm GC etch).
10. Center-wavelength values entered at 1550 nm with `wavelength_inferred: true` (the paper defines the center
    wavelength as 1.55 um for the design, p.3, and does not restate it for the measurement).

## liao2016 (strip-slot DC mode splitter without mode-order change, PTL 2016; simulation only)

Rows:
- `mode_converter.mdm_mux` strip-slot DC splitter, `row_kind design`: TE0 through loss about 0.1 dB, crosstalk > 35
  / > 25 dB (TE0 input), TE1 coupling loss < 1 dB, TE1 -> TE0 crosstalk > 16 dB, residual TE1 in the strip > 8 dB
  (`extinction_db`, mode-rejection), +/-10 nm tolerance (TE1 loss < 1 dB, crosstalk > 18 dB); widths 860 / 432 /
  50 / 914 nm, Lc 24.4 um, 220 nm core. Spectral rows carry 1500-1600 nm inferred from the Fig. 7 axis; tolerance
  rows 1550 nm inferred.
- `mode_converter.converter` slot-to-strip converter, `row_kind design`: simulated conversion efficiency 98.68 %
  (1550 nm inferred).

Not entered:
- "Insertion loss less than -0.1 dB" under +/-10 nm error (p.4) and in the conclusion for TE1: the path is ambiguous
  (TE1 coupling is only > -1 dB; the TE0 through path gives about 0.1 dB), D159.
- Gap 100 nm (`gap_nm` not allowed), S-bend radius 45 um (`min_bend_radius_um` not allowed for mode_converter),
  angle 10 deg, end separation 2.35 um, calculated Lc 29.6 um: notes only.

Fab / facility: none (design-only letter).

Judgment calls:
11. Residual through-port TE1 (< -8 dB) stored as `extinction_db` (mode-rejection) rather than crosstalk.
12. Platform `soi` for the strip + slot pair (alternative `soi_slot`); cladding recorded as the model's air.
13. Printed TE0 -> slot TE1 crosstalk "< -25 dB" kept with a conflict note (Fig. 7(a) trace near -23 to -25 dB).

## Registry gaps (proposed)

- `gap_nm` for mode_converter: paredes2021 100 nm (p.5), wang2022c 100 nm (p.5 Table 2), jiang2021 200 nm (TWC and
  BSWG ADC, p.3 Table I), liao2016 100 nm (p.3). Definition: coupling gap between access and bus guides of a mode
  (de)MUX / splitter (already confirmed in D533).
- `subwavelength_period_nm` for mode_converter: jiang2021 BSWG pitch 250 nm (p.3 Table I).
- A crosstalk-criterion bandwidth for mode_converter (`xt_bandwidth_nm` widened from switch_fabric): jiang2021 84 nm
  (1500-1584 nm, I1) and 100 nm (I2) for XT < -15 dB (p.5).
- `min_bend_radius_um` for mode_converter: liao2016 S-bend radius 45 um (p.3).

## Missing orgs

- NYUAD "Core Technology Platform Facility (CTP)", facility role (borderline: characterization), paredes2021 p.9
  Acknowledgment.
