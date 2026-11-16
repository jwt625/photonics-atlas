# lit_151 batch report

Paper: lit:hu2025a, "Silicon photonic MEMS switches based on split waveguide crossings" (Nature Communications 2025;
cached text = arXiv v3 manuscript, 52 pages incl. 27-page Supplement from p.26). Page-1 title matches the source row.
Not a review, not a correction. `garbled_text_layer`: page 28 (Supp. Table 1, comparison table); nothing taken from it.
Values come from clean text passages and page renders (Fig. 2, 3, 4, S4, S13, S15 checked on the renders).
Validation: `merge_component_staging.py data/_staging/components/lit_151 --dry-run` -> +15 components, +78 metrics,
0 errors (the only warning concerns a merged ni2025b row, not this batch).

## Components / metric rows

| component | class | rows | content |
|---|---|---|---|
| swx_switch_2x2 | switch_fabric.mems | 34 | measured OFF / ON excess loss and crosstalk 1420-1600 nm (ten-cascade average), rise / fall ~3.5 / ~1.2 us, -20 dB crosstalk bandwidth > 180 nm, 1550 nm 900 nm-gap crosstalk > 54.5 dB, 82-switch statistics (T11 / T22 mean, std, range), simulated OFF / ON values, 20 nm-gap simulation, mechanical resonance (0.14 / 0.152 MHz), standby (< 4 nW) and theoretical max power (54.2 nW), gaps 900 / ~15 nm, footprints, geometry |
| swx_switch_gap500 | switch_fabric.mems | 2 | 500 nm initial-gap sibling: OFF crosstalk > 29.3 dB at 1550 nm |
| swx_flat_facet_test | switch_fabric.mems (test) | 2 | flat-facet, stictioned test device: ~3 dB reflection, ~20 nm wedge gap |
| swx_switch_swt200_design | switch_fabric.mems (design) | 3 | 200 nm SWT, 10 nm gap foundry variant, simulated |
| mmi_crossing_unsplit_design | crossing.mmi (design) | 8 | base self-imaging crossing of the SWX, simulated |
| vw_mmi_crossing | crossing.mmi (test) | 5 | 28 mdB measured per crossing (cutback), 4 mdB / < -38 dB simulated |
| euler_sbend | waveguide_platform.bend | 5 | 26 mdB measured per S-bend, 3 mdB simulated, w 1.2 um, Rmin 20 um |
| circular_bend_90 | waveguide_platform.bend | 1 | 62 mdB per 90-degree bend |
| mode_converter_pair | waveguide_platform.other | 1 | 0.14 dB per converter pair |
| routing_wg_w600 / w1200 / w3000 | waveguide_platform.straight | 2 each | 8.9 / 2.8 / 1.7 dB/cm (spiral cutback) |
| benes_64x64 | switch_fabric.mems | 8 | 64x64 ports, 10 x 5.3 mm, all-OFF excess loss 8.0-12.6 dB (58 paths), loss-budget estimate 5.2-11.7 dB, single-ON 9.04-13.30 dB (28 paths, Table 3), crosstalk > 35 dB, extinction > 38 dB (C band) |
| gc_switch_chip | fiber_chip_coupler.grating | 1 | ~5 dB fiber-to-chip coupling loss, scope unspecified |
| gc_array_chip | fiber_chip_coupler.grating | 2 | calibration paths -20 to -24.5 dB (std 0.92 dB, 60 paths), fiber_to_fiber |

Total: 15 components, 78 metric rows.

## Values not entered and why

- Threshold voltage 20 V measured / 22 V simulated, maximum drive rating > 30 V (p.11; p.6 prints ~24 V), switching
  energy 542 fJ, durability > 1e9 cycles, ~0.1 dB repeatability, ON hold > 1 h: no switch_fabric parameter
  (registry gaps below); kept in the component notes.
- Spring constants (0.33 N/m total, per-part values), comb forces, strain, shock displacement (< 3.2 nm at 100 g),
  potential-well analysis: mechanical design values, no parameter.
- SWT period / depth (290 / 285 nm measured, 290 / 300 nm design): `period_nm` / `subwavelength_period_nm` are not
  allowed on switch_fabric; in notes.
- Supp. Sec. 2 intermediate design sweeps (Fig. S2: T11 0.11-0.52 dB, T12 0.12-0.55 dB at an assumed 20 nm gap; period
  and depth sweeps) and tolerance analyses (Fig. S3, S17): design-space sweeps, not a component design; only the
  20 nm-gap 0.15 dB / 21 dB point at 1550 nm is entered (simulated).
- Fig. S13(b) 700 nm-gap sibling: no printed value (D156 / never read a value the text does not give when the main
  values are printed). Fig. S13(a) transmission vs voltage curve: no parameter.
- Projected 64x64 loss 6.3 dB (4.1-8.2 dB) and 128x128 9.1 dB (4.9-11.4 dB) with improved fabrication: hypothetical
  devices resting on assumed inputs (0.1 dB/cm, 10 mdB).
- 1.1 dB/cm commercial-foundry waveguide loss (p.15) and 6 mdB / sub-10-mdB crossings of the authors' earlier work
  (ref. 51 / Supp. ref. 16): cited (rule 3, D259).
- Supp. Table 1 (p.28): garbled layer; it also repeats this paper's own headline values and other works' values.
- Table 2 per-path estimated / measured losses (64 paths): summarized by the printed 8.0-12.6 dB and 5.2-11.7 dB
  ranges; per-path values not entered.
- Euler S-bend high-order-mode excitation < -30 dB (simulated): no parameter for waveguide_platform.
- Durability-test T12 at 1550 nm (Fig. 3(g)) and Fig. S14: no printed values beyond "no degradation".

## Fab / facility orgs

- Fab `org_zhejiang_university` on all fabricated rows: author contributions (p.21) "Y. H. fabricated the devices";
  all authors at Zhejiang University (D72 / D395).
- Facility `org_zju_micro_nano_fabrication_center` and `org_westlake_center_for_micro_nano_fabrication`: "thank the
  ZJU Micro-Nano Fabrication Center and the Westlake Center for Micro/Nano Fabrication and Instrumentation for the
  facility support" (p.21). Same pairing as merged lit:sun2026a.
- `process_name` empty: EBL with PEC in the authors' process, no named PDK / foundry flow. SOITEC SOI wafer in notes
  (wafer supplier, D428). No missing orgs.

## Judgment calls

1. OFF / ON excess-loss rows (Fig. 3(c, d)) are `measured`, scope `per_component`, method `cutback`, statistic `mean`,
   n 10: the paper prints the per-switch value from ten cascaded switches "measured and averaged" without a cascade
   total (D567 precedent). The sentence precedes both panels; the ON-state isolation is not described separately
   (note on the ON row).
2. Crosstalk ranges use the Fig. 3(c, d) labels (44.0-56.7 dB OFF, 24.1-30.0 dB ON) as value / value_max; the text
   bounds are in notes.
3. The 82-switch statistics (Fig. S15(j, k)) are attached to the main 2x2 component (same design, array chip), method
   `unspecified` because normalization to the 60 calibration waveguides is implied but not stated.
4. Mechanical resonance 0.14 / 0.152 MHz entered as `derived` (unit rescale, D82d / D157) with notes that the inputs
   are simulated; the 54.2 nW maximum power `author_estimate` (assumed 100 kHz rate); the < 4 nW standby power
   `derived` (0.2 nA bound x 20 V).
5. Array path losses: `excess_loss_db` scope `de_embedded` (seok2019 precedent uses insertion_loss_db de_embedded;
   the paper calls it excess loss); single-ON range 9.04-13.30 dB is `derived` (min / max of Table 3 excluding the
   four defective paths the paper names).
6. Mode-converter pair classed `waveguide_platform.other`: the paper never describes what the converters convert
   (placed between suspended spring waveguides and fixed waveguides, p.33); a coordinator may prefer
   `mode_converter.converter`.
7. Test-structure wavelengths (crossing, bends, converters, spirals) set to 1550 nm `wavelength_inferred` (the paper
   uses them for its 1550 nm array-loss estimate, p.45); no wavelength is printed with them.
8. Routing waveguides recorded as ridge (150 nm partial etch) from the array description (p.42); the spiral
   cross-section is not stated separately (core_material note). Platform `soi` (not `soi_rib`) because the suspended
   SWX / strip parts and the ridge routing share one row family; coordinator may switch the waveguide rows to `soi_rib`.
9. Grating couplers: two rows (elementary-switch chip ~5 dB, scope `unspecified`; array chip calibration paths
   fiber_to_fiber) because the paper does not say they are the same design (D159 caution).
10. Flat-facet test device kept as its own `switch_fabric.mems` test row (different wafer, no SWT, no stoppers).

## Registry gaps (proposed)

- `actuation_voltage_v` (switch_fabric): threshold / pull-in drive voltage of a MEMS switch; hu2025a 20 V measured
  (p.11, Fig. 3(e)); also D440 candidate list.
- `switching_energy_pj` (switch_fabric, phase_shifter): energy per switching event; hu2025a 0.54 pJ theoretical
  (p.39 Supp. Sec. 8).
- `endurance_cycles` on switch_fabric (today phase_shifter only): hu2025a > 1e9 cycles without degradation (p.12,
  Fig. 3(g)).
- `subwavelength_period_nm` / `period_nm` on switch_fabric: SWT period 290 nm measured (p.10, Fig. 3(b)).
