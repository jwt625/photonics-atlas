# lit_259 batch report

Distilled 2026-11-23. Papers: lit:hao2019, lit:gupta2017, lit:morino2014, lit:abuelmaaty2018. Page-1 titles match
the source rows; the institutional download stamp in the text layer of gupta2017, morino2014 and abuelmaaty2018 was
ignored. Validation: `merge_component_staging.py data/_staging/components/lit_259 --dry-run` -> +20 components,
+118 metrics, 0 errors (the one warning printed is a merged ni2025b row, not this batch).

| paper | components | metric rows | kind |
|---|---|---|---|
| hao2019 | 3 | 28 | design (3D-FDTD only) |
| gupta2017 | 10 | 47 | fabricated, measured |
| morino2014 | 3 | 19 | design (2D FDTD only) |
| abuelmaaty2018 | 4 | 24 | design (2D / 3D FDTD only) |
| total | 20 | 118 | |

## hao2019 (polygonal-slot TE mode-order converters, SOI)

Rows: tilted-slot TE0-TE1, bi-tilted-slot TE0-TE2, tri-tilted-slot TE0-TE1 (all `mode_converter.converter`,
`row_kind: design`, platform `soi`). Conversion efficiency in `coupling_efficiency_pct` per_component and modal
crosstalk in `crosstalk_db` (cheng2019 precedent). Table 1 values (p.7) at 1550 nm, 1500-1600 nm bounds (p.7),
TE0-TE2 fabrication-tolerance bounds from Fig. 7 text (p.8-9) as conditions on the TE0-TE2 row, Table 1 / Table 2
etch depths, W0 2.0 um (derived) and H0 220 nm.

Not entered:
- Reflection below -35.0 dB over 1500-1600 nm for both converters (p.7, Fig. 5(c) / (d)): `back_reflection_db` is not
  allowed for mode_converter (registry gap, already listed in D551 / D567).
- Slot angles alpha1 / alpha2 and slot spacing d_slot (Table 1 / Table 2): no registry parameter; in component notes.
- TE1-TE3 bi-tilted slot and TE2-TE1 cascaded slots (Table 2, Fig. 8(a) / (c)): geometry only, no performance value
  (rule 9).
- Fig. 6(b) design-space statement (>= 96.0 % for alpha1 74.0-80.5 deg, alpha2 72.5-83.5 deg with d_slot re-optimized):
  describes other designs (note on the TE0-TE2 row).
- Beat length 3.16 um, slot effective indices 2.46 / 2.22, self-imaging period ~6.40 um (p.8): analysis quantities.
- "Low insertion loss" (conclusion): no number.

Fab / facility: none (no fabrication).

## gupta2017 (wavelength-independent directional couplers, 220 nm SOI, IIT Madras)

Rows (all `fabricated`, fab `org_indian_institute_of_technology_madras`):
- `widc_shallow_access` (splitter.directional_coupler, soi_rib, family row D165): EL 1-1.5 dB range (reference
  structure), measured 3-dB coupling length ~5 um and simulated ~4.5 um, D2 design geometry (W 350 / h 160 / G 150 nm,
  H 220 nm, BOX ~2 um, R 180 um), SEM W ~360 nm / G ~150 nm.
- `widc_deep_access_l8`: average EL ~0.8 dB (headline, abstract / conclusion), lDC 8 um.
- `ps1x4_shallow_access` / `ps1x4_deep_access` (1x4 tree of three 3-dB WIDCs, classed by element like the merged MMI /
  Y-branch trees): split ratio ~25 % per port, average EL 3 dB / 2 dB, lDC 7 um, R 180 um, 1 in / 4 out.
- `umzi_shallow_access` / `umzi_deep_access` (wdm.cascaded_mzi, single-stage precedent): extinction ranges read off
  Fig. 16(c) / (d), design FSR ~1 nm (author_estimate, D82a), dL 350 um, 1 stage; SEM labels lDC 5 um and R 125 um
  (Fig. 16(b), shallow variant only).
- `ring_r25_widc`, `ring_r25_deep_dc`, `ring_shallow_widc` (resonator.ring): notch depths and resonance spacings read
  off Fig. 17(c) / (d) and Fig. 18(b) / (c) (no number printed in the text), R 25 um, lDC 4 um.
- `gc_shallow` (fiber_chip_coupler.grating): reference-waveguide fiber-chip-fiber loss 11 +/- 0.1 dB, scope
  fiber_to_fiber (two GCs plus 2-5 mm waveguide), 1550 nm inferred.

Not entered:
- D1 / D2 lDC = 500 um test DCs: FSR 118 nm and |Delta n_g| 0.036 (D2, p.5) and the Fig. 12 spectra: `fsr_nm` is not
  allowed for splitter and there is no differential-group-index parameter (registry gap); no row.
- DC4 design (W 375 / h 160 nm; Delta n_g within +/-0.02 over 1525-1625 nm; 3-dB length 4 um, p.3) and DC1-DC3
  (Fig. 2-5): no allowed performance parameter; no rows.
- Simulated bend loss (Fig. 8; "negligibly small" above R 90 um): no number.
- ~2-5 % split-ratio variation from fiber-GC coupling uncertainty (p.6): measurement uncertainty, in notes.
- 1x4 "about +/-5 %" ratio variation: absolute vs relative not stated; in notes.
- Deeply etched conventional DC (lDC 8 um, Fig. 14(b)): no printed value; no row.
- Ring Q values ("very high Q", "high Q"): not printed. Ring radius of the Fig. 18 shallow-etched ring: the text says
  "larger ring radii (e.g., 100 um) were fabricated" without tying a radius to the Fig. 18 device (D159); not entered.
- Fig. 14(a) / Fig. 17(b) SEM labels (150 / 50 / 75 um; 35 / 4 / 12 um): roles not stated.
- Fig. 13 per-length split ratios: figure-only, not read.

Missing org (facility candidate): "Centre for NEMS and Nanophotonics (CNNP) at IIT Madras", p.1 footnote ("This
research has been carried out within the scope of the Centre for NEMS and Nanophotonics (CNNP) at IIT Madras,
sponsored by MeitY"). Not set as facility here: the wording reads as a program / sponsorship statement (D80c); CNNP is
already reported missing by the priyadarshini2024 rows.

## morino2014 (curved directional coupler, Si wire, Kanazawa University)

Rows (splitter.directional_coupler, `row_kind: design`, platform empty): curved DC R 21 um / LC 7.40 um (theta
20.2 deg), curved DC R 26 um / LC 8.75 um, conventional DC LS 2.10 um. Each carries the -3 +/- 0.1 dB bandwidth as
`split_ratio_pct` 48.98-51.29 % over the printed wavelength span (1524-1586, 1476-1534, 1551-1560 nm; D83f simulated),
plus gap 200 nm, width 400 nm, Si 210 nm and the coupling-region geometry (coupling_length_um, coupling_angle_deg,
min_bend_radius_um as the bent-DC precedent bayoumi2025). The conventional DC also carries the 0-200 C cross-port
coupling range 43.5-50.5 % (Fig. 7).

Not entered:
- Curved DC coupling-efficiency change below 1.0 % over 0-200 C (p.4, conclusion): `coupling_variation` is defined over
  wavelength; temperature-variation parameter is a registry gap. In component notes.
- Fig. 4 / Fig. 5 coupling-angle series (theta 18.5-21.0 deg; LC 6.78-7.70 um), slopes -11.0 %/um and -0.035 um/um;
  Fig. 6 radius series (only R 26 um printed); Fig. 8 (Gap, W) tolerance curves: figure-only or no parameter.
- "Sevenfold" bandwidth enhancement: a ratio of two entered spans.

Fab / facility: none (no fabrication).

## abuelmaaty2018 (Si-Si3N4 phase-plate mode converter, ICTON 2018)

Rows (mode_converter.converter, `row_kind: design`, platform `soi`): 2D-FDTD model (2W 2 um, d 0.6 um; TE and TM
results), 3D TE design (1 um x 220 nm, d ~0.8 um, notch r 125 nm; headline -1.5 dB / -12.81 dB), 3D TM design (1.5 um,
d 1.6 um, notch r 225 nm), dual-polarization design (2.8 um, d 1.8 um, notch r 120 nm). Insertion loss per_component
and crosstalk per target mode at 1550 nm.

Not entered:
- Notch-circle radii 125 / 225 / 120 nm and positions: `radius_um` is not allowed for mode_converter (registry gap);
  in labels / core_material.
- Dual-polarization crosstalks: Fig. 8 only, not printed; not read.
- Ref. [7] / ref. [8] device values in the introduction (88 %, 23 um; < 2 dB, > 9.5 dB): cited work (rule 3).
- Si thickness of the 3D TM and dual-polarization designs: not restated (no core_thickness row on those two).

Fab / facility: none.

## Judgment calls for the auditor

1. hao2019 tri-tilted crosstalk "higher than -15 dB" entered as printed: `crosstalk_db` 15 `lt` (suppression below
   15 dB). It may be a typo for "lower"; alternative is to keep it out (D159-style ambiguity).
2. hao2019 Fig. 7 fabrication-tolerance bounds (8 rows) entered as conditions on the TE0-TE2 design row with 1550 nm
   inferred (Fig. 7 prints no wavelength), rather than as separate sibling rows or left out.
3. hao2019 "as high as 90%" -> `statistic: best` (rule 7 analogue of "as low as").
4. gupta2017 EL "varying between 1 dB to 1.5 dB" for "individual devices" put on the WIDC family row; the sentence
   follows the D1 / D2 discussion, but the next sentence ties the EL to WIDCs.
5. gupta2017 Fig. 11 SEM width ~360 nm / gap ~150 nm put on the WIDC family row (the SEM device is "a fabricated DC";
   W matches the 350 nm design, not the 550 nm D1).
6. gupta2017 fab IIT Madras on all 10 rows: the first-person fabrication sentence names the DC test structures; the
   1x4, MZI and ring sentences are passive but say "as described earlier" / same two-step process (D656 / D709
   one-flow precedent).
7. gupta2017 1x4 split ratio 0.25 stated once for both variants -> entered on both rows (approx); +/-5 % left in notes.
8. gupta2017 single-stage unbalanced MZI as `wdm.cascaded_mzi` (arafat2024 / bayoumi2025 precedent) and the 1x4 tree
   as `splitter.directional_coupler` (tree-by-element precedent).
9. gupta2017 figure reads (MZI extinction ranges, ring notch depths, ring spacings 4.2 / 0.73 nm) from low-resolution
   rasters; uncertainties in notes. The 0.73 nm spacing of the Fig. 18 ring is not cross-checked against any radius
   (radius not tied to that device).
10. gupta2017 measured 3-dB coupling length ~5 um entered in `coupling_length_um` with basis measured (an experimental
    result, not a drawn dimension).
11. morino2014 -3 +/- 0.1 dB bandwidth converted to a per-port `split_ratio_pct` range (48.98-51.29 %, simulated per
    D83f) instead of `bw_1db_nm` (the chen2022a / chung2023 precedent stored +/-0.5 dB windows there; a 0.2 dB window
    is not a 1-dB width). Platform left empty (Si wire in SiO2, SOI never stated, D423).
12. morino2014 conventional-DC temperature range (Fig. 7) tied to the LS 2.10 um design ("designed for 50 % coupling"
    at ~1.55 um; LS not restated).
13. abuelmaaty2018 2D-FDTD TE and TM results on one row (same 2D structure); dual-polarization design simulation
    dimension not restated (listed under the 3D-FDTD section).

## Registry gaps (skipped value + locator + proposed definition)

- `back_reflection_db` on mode_converter: hao2019 < -35.0 dB, 1500-1600 nm, both converters (p.7, Fig. 5(c) / (d)).
  Use the existing definition (back-reflection magnitude, positive dB).
- Differential group index of DC supermodes (`delta_group_index`, unit 1, splitter): gupta2017 D2 |Delta n_g| 0.036
  measured (p.5), DC4 -0.02..+0.02 simulated (p.3). Definition: n_g(symmetric) - n_g(antisymmetric) supermode
  difference as reported. Also `fsr_nm` on splitter for long-DC spectra (D2 118 nm, p.5).
- Criterion bandwidth (`criterion_bw_nm`, already a candidate in D539 / D716): morino2014 62 nm (1524-1586 nm), 58 nm
  (1476-1534 nm), 9 nm (1551-1560 nm) for transmittance within -3 +/- 0.1 dB (p.3-4).
- Temperature variation of the coupling ratio (`coupling_variation_temp`, unit 1, splitter): morino2014 curved DC
  < 0.010 over 0-200 C (p.4 Sec. III-D, Fig. 7). Definition: max minus min power coupling coefficient over the stated
  temperature span.
- `radius_um` on mode_converter (or a notch-radius parameter): abuelmaaty2018 notch radii 125 / 225 / 120 nm (p.2-4).
- Slot / boundary-surface angle and slot spacing for mode_converter: hao2019 Table 1 / Table 2 (p.7, p.10); low
  priority (single paper).
