# lit_231 batch report

Distilled 2026-11-20. Papers: lit:fontaine2022, lit:yi2024b. Page-1 titles match the source rows. Dry run
`merge_component_staging.py data/_staging/components/lit_231 --dry-run`: +3 components, +40 metrics, 0 errors.

| paper | components | metric rows |
|---|---|---|
| fontaine2022 | 0 | 0 |
| yi2024b | 3 | 40 |

## lit:fontaine2022 (Proc. IEEE 2022, review: photonic lanterns, ULI 3-D waveguides, micro-optic SDM parts, MPLC)

No rows. Every quantitative device value in the paper is credited to cited work, most of it the authors' own
earlier papers (rule 3, D259 / D259a):

- p.4 Fig. 3 three- and six-mode-selective lanterns: "reported in [45]" / "[47]"; core diameters and the 27 / 29 um
  multimode-end cores are geometry of cited devices.
- p.5-6 ten / 15-mode lanterns [48], 7-core x 3 / 6-mode lanterns [53], [54], graded-index lanterns [46], [55].
- p.7 ULI waveguides: propagation loss < 0.5 dB/cm [64], ~0.1 dB/cm [65], [66]; birefringence [67], [68]; fan-outs
  4-121 cores [69]-[72] with "close to 1 dB or even less" [71]; tapered couplers > 100 nm, > 20 dB extinction [79];
  multicore few-mode fan-outs [52], [81]-[83].
- p.8 Fig. 7 FMF isolator coupling loss vs collimator distance and the "MDL 0.2-0.4 dB, average IL < 1 dB" statement:
  the measurement is attributed to [88] (Jung et al., APL Photonics 2019, authors' own); Fig. 7 reproduces it (D259a).
- p.9 Fig. 8 32-core MCF isolator: average IL 1.5 dB, core-to-core variation 1.5 dB, crosstalk < -40 dB, "initial
  measured device performance for a 32-core MCF isolator [88]" (D259a). Rotational alignment < 1 deg for < 0.2 dB
  core-dependent loss is credited to [92].
- p.10 Fig. 10 assembled 45-HG-mode MPLC: no loss, MDL or bandwidth printed; only mode counts (45; 210 and 325 modes
  on an SLM; designs to 1035 modes [101]). A mode count alone is geometry (rule 9: no performance metric, no row).
- p.11 Table 1: technology-level comparison (lantern < 1 dB, MPLC > 3 dB, 3-D waveguide 1 dB; bandwidths, sizes), not
  a specific device; comparison-table values are not entered. p.3 / p.12 generic statements (MPLC "typically 3-5 dB",
  "around 3 dB" fiber-to-fiber for < 10 planes) are likewise not device results.

Missing orgs: none needed. Registry gaps: none.

## lit:yi2024b (JLT 2024, dual-band 1.55 / 2 um four-mode MDM on 220 nm SOI)

Components:
- `cmp_lit_yi2024b_adc_mdm_4mode` (mode_converter.mdm_mux, soi): 38 rows. Measured Table II: 8 insertion_loss_db
  (TE0-TE3 x two bands) + 8 crosstalk_db; simulated single-ADC IL (TE1-TE3 at 1550 / 1970 nm, 6 rows) and CT > 18 dB
  (1 row); geometry: Wa 500 nm, Wb1 / Wb2 per ADC (6 rows), coupling length per ADC (3), Si 220 nm, BOX 2 um, cladding
  1 um, 4 inputs / 4 outputs.
- `cmp_lit_yi2024b_gc_1p55um`, `cmp_lit_yi2024b_gc_2um` (fiber_chip_coupler.grating, soi): one IL row each
  (~6 / 8 dB per facet, author_estimate, origin not stated).

Values not entered and why:
- Abstract / conclusion "< 2.2 dB / < -13.0 dB" and "< 3.1 dB / < -10.6 dB": maxima of the Table II per-mode values
  already entered.
- Access-bus gap g = 100 nm (p.2, Table I): `gap_nm` is not allowed for mode_converter (registry gap, below).
- Phase-matching bus widths read from the n_eff curves (1.03 / 1.06, 1.56 / 1.63, 2.1 / 2.19 um at 1550 / 1970 nm,
  p.3): design intermediates; the drawn taper ends Wb1 / Wb2 are entered.
- Link results (4 x 114 Gb/s PAM8 at 1.55 um, 4 x 84 Gb/s at 2 um, BTB BER values, ROP penalty < 1 / < 1.5 dB,
  p.5 Fig. 8): system results. The 12 GHz commercial 2 um PD, MZM, EDFA / TDFA are setup equipment (rule 13).
- Grating-coupler periods: not printed ("chirp subwavelength structures with different periods", p.3).

Fab / facility:
- facility_org_ids = `org_center_of_optoelectronic_micro_and_nano_fabrication_and_characterizing_facility` (p.5
  Acknowledgment: Center of Optoelectronic Micro&Nano Fabrication and Characterizing Facility, WNLO of HUST, "for the
  support in device fabrication"), all three rows.
- fab_org_ids empty: the fabrication sentence is passive with no org named ("The device is fabricated using electron
  beam lithography", p.3 Sec. III; D80b). Same handling as the merged cheng2023a rows from the same HUST group; HUST
  (`org_huazhong_university_of_science_and_technology`) is the borderline candidate if the acknowledgment is read as
  naming the place of processing (D448).
- Commercial SOI wafer, vendor not stated. No process_name printed.

Judgment calls for the auditor:
1. Measured IL rows: `author_estimate`, method `loss_breakdown`, scope `de_embedded` (not halved per device), because
   the spectra are extracted by subtracting a GC loss "estimated to be ~6 dB/facet and 8 dB/facet" of unstated origin
   (p.4). Same convention as lit:sun2025 (same group, same setup). Crosstalk rows stay `measured` / `direct` (a port
   ratio, independent of the subtracted GC term).
2. Crosstalk condition reads Table II CT(TEn) as the highest leakage from input n into the other three outputs
   (Fig. 6 panels annotate the gap between the wanted trace and the highest unwanted one).
3. The `~` in "~6 dB/facet and 8 dB/facet" is applied to both values (qualifier approx on both GC rows); wavelength =
   the printed waveband names (1.55 um -> 1550 nm, 2 um -> 2000 nm, D393).
4. Simulated single-ADC values sit on the MDM row (one row per physical design; a2013 / sun2025 precedent) with the
   ADC in the condition and scope `per_component`. The simulated CT "< -18 dB in the operation wavelength range" uses
   the Fig. 3 axis span 1500-2000 nm with `wavelength_inferred`.
5. Wb1 / Wb2 printed in um (Table I) -> `derived` (D157 / D256); Wa keeps `design_target` (500 nm printed on p.2).
6. Ref. [40] (ACP 2023) is the authors' conference version; the journal values are not attributed to it, kept (D408).

Missing orgs: none (facility and HUST are in the registry).

Registry gaps:
- `gap_nm` for `mode_converter` (skipped: yi2024b g = 100 nm, p.2 Sec. II and p.3 Table I; also reported for a2013).
  Proposed definition: access-to-bus coupling gap of a directional-coupler-type mode converter / multiplexer.
