# lit_199 batch report

Distilled 2026-11-18 (verified_on 2026-11-18). Papers: lit:lu2017, lit:tsarev2011, lit:yamaguchi2022, lit:liang2005.
Validation: `uv run --offline python scripts/merge_component_staging.py data/_staging/components/lit_199 --dry-run`
-> +10 components, +69 metrics, 0 errors (the only warning is a pre-existing merged row, cmp_lit_ni2025b_pimmwc).
Page-1 titles match all four source rows; IEEE download stamps ignored.

| paper | components | metric rows |
|---|---|---|
| lu2017 | 4 (3 fabricated star-crossings, 1 design) | 36 |
| tsarev2011 | 1 (design) | 11 |
| yamaguchi2022 | 4 | 14 |
| liang2005 | 1 | 8 |
| total | 10 | 69 |

## lit:lu2017 (inverse-designed PhC-like subwavelength star-crossings, 220 nm SOI)

Rows: `star_4x4`, `star_5x5`, `star_6x6` (crossing.other, soi_strip, fabricated, test_structure) and
`star_4x4_140nm_design` (row_kind design). Per fabricated device: measured mean crossing loss (0.75 / 0.9 / 1.5 dB,
1520-1580 nm, cutback with GC reference, measured), measured crosstalk (about 22.5 / 20 / 18 dB), simulated mean
IL and crosstalk bound over the 80 nm design span, coupling-region length, hole periods, 220 nm core, 200 nm hole
etch depth (design), n_inputs / n_outputs; 4 x 4 also the simulated 0.4 dB at 1550 nm and the 500 nm access width.

Not entered:
- port density (7.1 / 5.83 / 7.3 um2/port, p.1 / p.4 / p.7): no registry parameter; footprint not computed.
- hole radius 45 nm, line spacing y (99.5 / 97.5 / 92 nm), 33 periods, grey-wall thickness (p.4, p.7): no crossing
  parameter (hole radius, n_periods on crossing).
- hole-radius series 39-51 nm, average IL +0.6 / +0.9 dB for +/-2.5 / +/-5 nm (p.9): increments only, the text does
  not say which star-crossing (D159).
- random-initial 4 x 4 pattern (Fig. 3(d), "0.7 dB in average more", p.5): relative value only.
- simulated reflections and the 160 / 180 nm etch-depth intermediate designs (Fig. 5(a)-(b), p.6): curves only.
- 0.02 dB / -40 dB and other crossing values in the introduction (p.2): cited work (rule 3).

Fab / facility: passive fabrication sentence; the acknowledgments (p.10) thank named engineers of CMFC, WNLO for
support in EBL and ICP etching -> borderline fab `org_huazhong_university_of_science_and_technology` on the four rows
(D84b; xu2025 / D573 precedent), no facility (staff thanks). No missing org.

## lit:tsarev2011 (Si wire crossing via inverse tapers and an SU-8 polymer bridge; 3D FDTD only)

Row: `si_polymer_vertical_crossing` (crossing.multilevel, row_kind design, platform other per D71 Si-polymer hybrid).
Metrics (all simulated): through-pass loss < 0.1 dB at 1550 nm; 0.088 dB (98 %) over 1540-1560 nm and 0.132 dB
(97 %) over 1520-1580 nm (arithmetic on simulated values stays simulated, D83f); cross-pass < 0.002 dB; crosstalk
about 70 dB; geometry length 70 um, Si wire 450 x 220 nm, BOX 2 um, taper length 30 um, vertical FOX gap 180 nm.

Not entered: back reflection about -50 dB (and -53 dB for 16 wires; back_reflection_db not allowed on crossing);
taper tip width 160 nm (tip_width_nm not allowed on crossing); polymer strip W 1.5 um / H 1.7 um and index 1.56 (no
crossing parameter for the second layer); tip-width tolerances (+/-6 nm for < 0.2 dB, +/-20 nm for < 0.4 dB, p.5);
16-wire totals (0.01 dB, bound 0.04 dB, p.6); "effective per length" 14 dB/cm (p.6); 340 x 340 nm Si wire variant
(only an optimum index, Fig. 1(b)); 0.2 dB / -0.2 dB values of refs. [1] / [19] (cited, rule 3).

Fab / facility: none (simulation paper). No missing org.

## lit:yamaguchi2022 (3D polymer waveguide fan-in/out for a 4-core MCF, Mosquito method)

Rows (fiber_interface.fan_out, polymer, process_name "Mosquito method"): `fifo_10mm_cosine` (lowest IL 1.09 dB at
1310 nm, `best`, fiber_to_fiber SMF launch / 105 um MMF detection; Fig. 10(b) per-channel range 1.07-1.24 dB
extracted_from_figure; length, 4 channels, pitches 250 um / 60 um), `fifo_25mm_rotated` (printed 2-3 dB, wavelength
and configuration not stated, scope unspecified), `fifo_25mm_conventional` (Fig. 4(b) range 2.7-3.35 dB,
extracted_from_figure), and `straight_ref_10mm` (waveguide_platform.straight, test structure; Fig. 10(b) range
0.91-0.99 dB at 1310 nm).

Not entered: Table 1 preliminary straight-core study (0.475 dB vs 1.54e-3 dB "average loss value", text 0.473 dB
lower-vs-upper core difference at 1550 nm, p.2): a process study with no component parameter; loss reduction
0.2-0.8 dB (p.2): a difference between two rows; core position accuracy +/-3 um and labelled spacings 252.7 / 248.6
/ 250.2 um (p.3, Fig. 8): no parameter (figure-labelled spacings are measured positions, not entered as pitch); BPM
S-bend length thresholds (about 2.8 mm arc vs 2.2 mm cosine, p.3, Fig. 6) and assumed indices 1.575 / 1.547 and 7 um
GI core (design inputs); 1100 um needle-start offset (process setting); NFP (qualitative); 500 um cladding layer
(total coated layer, not a cladding above the core).

Fab / facility: "fabricated applying the Mosquito method we developed [5]" plus passive sentences, authors at Keio
University and Sumitomo Electric Industries -> fab empty (D80b, D154); process_name kept as printed with fab empty
(Contract v7). No facility. No missing org.

## lit:liang2005 (MZI polarization beam splitter, 5.1 um SOI rib)

Row: `mzi_pbs_w3p2_w2p5` (polarization.pbs, soi_rib, fabricated): per_db > 13 dB over 1520-1565 nm (TE and TM
ports); insertion loss < 6.3 dB over 1520-1565 nm (`device_total`, includes lensed-fiber coupling and 3-dB facet
Fresnel loss); excess loss 1.1 dB for the two MMIs and tapers as insertion_loss_db `de_embedded`,
`reference_structure` (straight reference waveguide; wu2017 / D595 precedent), wavelength inferred from the ASE
measurement band; arm widths 3.2 / 2.5 um, 5.1 um core, 2.5 um etch (derived unit rescales), 0.4 um BOX.

Not entered: Fig. 5 width series (D159: the same nominal 2.5 / 3.5 um pair reads differently in Fig. 5(a) and 5(b),
the 3.2 / 2.5 um pair in Fig. 5(b) disagrees with Fig. 4 at 1550 nm, and Fig. 5(b) plots 3.8 um outside the printed
3.2-3.5 um range; readings in component notes); MZI arm length (6 mm on p.2 vs 3 mm on p.3, D417) and the about 1 cm
device length; MMI 36 x 2000 um (mmi_* not allowed on polarization); Fig. 2 computed birefringence; 0.1 dB/cm SOI
loss in the introduction (cited, rule 3).

Fab / facility: passive "was fabricated on an SOI wafer", both authors at CUHK -> fab empty (D80b). No missing org.

## Judgment calls

(a) lu2017 measured ILs entered as `mean` 0.75 / 0.9 / 1.5 dB from the body / conclusion "0.75 +/- 0.2 dB" form,
without a qualifier; the abstract's "less than" wording and the +/-0.2 dB are in notes. Method `cutback` (single and
5-cascade test structures plus a GC reference), basis `measured` (no total or division printed; D167 / D452 / D567).
(b) lu2017 5 x 5 length: the p.7 coupling-region length 5.41 um is entered; the p.3 "6.63 um" star-crossing length is
a conflict noted on the component (D417).
(c) lu2017 platform `soi_strip` (fully etched 220 nm access waveguides, p.7; han2018 / su2017 precedent); the
crossing region is a slab with 200 nm-deep holes, stated in core_material.
(d) lu2017 fab HUST as borderline staff-thanks fab (D84b, same wording as merged xu2025), no CMFC facility.
(e) lu2017 140 nm-depth 4 x 4 pattern kept as a design row (an optimized design with its own simulated IL; no
fabrication of it stated).
(f) tsarev2011 98 % / 97 % band values converted to dB (0.088 / 0.132 dB) as `simulated` with qualifier `le`, band
edges read from "within 20 nm / 60 nm bandwidth around 1.55 um"; the optimum vertical gap 180 nm is taken from the
Fig. 6 ("optimum cross coupler") caption, not the 200 nm of Figs. 2-5.
(g) yamaguchi2022 25 mm rows: scope `unspecified` and band `unspecified` (Fig. 4(b) configuration and wavelength not
stated); the printed "2 to 3 dB" kept as a range with the Ch. 4 ~3.15 dB reading noted (D417). The conventional
cross-section FIFO and the 10 mm straight reference get their own rows with figure reads only (rule 9 siblings).
(h) yamaguchi2022 10 mm IL scope `fiber_to_fiber` (SMF in, 105 um MMF out) with the output fiber named in the condition.
(i) yamaguchi2022 process_name "Mosquito method" as printed (named fabrication method, no foundry).
(j) liang2005 IL < 6.3 dB and 1.1 dB excess put on the 3.2 / 2.5 um device row: the paragraph reports one device and
says "the polarization splitter"; excess loss scope `de_embedded` (straight reference removes coupling, Fresnel and
propagation).

## Missing fab / facility orgs

None needed by a row. (CMFC of WNLO exists as `org_center_of_micro_fabrication_and_characterization`; not used, staff
thanks only.)

## Registry gaps (skipped value + locator, proposed definition)

1. `back_reflection_db` on crossing: tsarev2011 about -50 dB (p.1 abstract, p.5 Sec. 3, p.6 Sec. 4); already listed in
   D573 / D639.
2. `tip_width_nm` on crossing: tsarev2011 taper tip 160 nm (p.4, Fig. 6 caption) - taper-based multilevel crossings.
3. `layer2_thickness_nm` (and a second-layer width) on crossing: tsarev2011 SU-8 strip H 1.7 um, W 1.5 um (Fig. 6
   caption) - thickness / width of the upper guiding layer of a multilevel crossing.
4. `hole_radius_nm` / `n_periods` on crossing: lu2017 r = 45 nm, 33 periods (p.4) - pixel hole radius and period count of
   subwavelength / PhC-like crossings (hole_radius_nm already a candidate in D430 / D566).
5. `mmi_width_um` / `mmi_length_um` on polarization: liang2005 MMI 36 um x 2000 um (p.2 Sec. II) - multimode section of
   MMI-based PBS / PSR.
6. Core position accuracy on fiber_interface: yamaguchi2022 +/-3 um (p.3, Fig. 8) - maximum deviation of fabricated core
   positions from design at the fiber-facing end, as stated (candidate `core_position_error_um`).
