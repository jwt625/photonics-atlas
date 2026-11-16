---
batch: lit_146
date: 2026-11-15
papers: lit:west2019, lit:deng2019, lit:liu2018b, lit:xie2020
totals: 23 components, 170 metric rows
validation: merge_component_staging.py --dry-run -> 0 errors (1 pre-existing warning on a merged row, cmp_lit_ni2025b_pimmwc-m18)
---

# lit_146 batch report

All four cached texts match their source rows (page-1 titles checked). No corrections / errata, no garbled text layer.
Selection context (cited in benchmark tables) did not change what was entered: only each paper's own results.

## lit:west2019 (ALD Al2O3 blue / NUV platform): 6 components, 43 metrics

- `cmp_lit_west2019_wg_w600` / `_wg_w500` / `_wg_w400` (`waveguide_platform.straight`, platform `al2o3`): paperclip
  cutback loss. Text values 1.77 / 1.35 dB/cm (TE / TM, 405 nm, 600 nm width) and 3.12 / 2.89 dB/cm (TE / TM, 371 nm,
  500 nm width) `measured`, statistic `best` ("as low as"); width assignment from p.8 (600 nm lowest at 405 / 419 /
  458 nm, 500 nm lowest at 371 nm). 419 / 458 nm points (Fig. 3(a)) and 400 / 500 nm points at 405 nm (Fig. 3(b))
  `extracted_from_figure`. 2.6 dB/cm TE at 405 nm for the 500 nm width (p.8) `measured`. Geometry: widths, 100 nm
  core (target), 3.2 um BOX, 3 um cladding, sidewall about 80 deg, min bend radius 200 um (`derived` from 400 um
  diameter).
- `cmp_lit_west2019_film_slab` (`waveguide_platform.other`): prism-coupling film loss < 0.3 dB/cm, stated for both 633
  and 405 nm -> one row, band unspecified (skill rule 7).
- `cmp_lit_west2019_film_annealed`: films annealed at 900 / 1100 C, loss > 20 dB/cm (no wavelength stated).
- `cmp_lit_west2019_ring_r90` (`resonator.ring`): Q_i 470,200 and Q_c 660,000 `derived` (gap series resolves the
  regime, D403); loaded Q 275k and 2.7 GHz width from Fig. 4(a); 2.35 dB/cm `author_estimate` (simulated n_g 1.648);
  thermal shift 4.13 pm/K `measured`.
- Not entered: effective TO coefficient 1.68e-5 RIU/C and bulk ALD-alumina TO coefficient 2.75e-5 RIU/C (no
  parameter; the bulk value rests on a cited SiO2 coefficient); -7.53 GHz/C (same quantity as 4.13 pm/C); absorption
  fraction alpha_abs / alpha_wg about 1 % upper bound (model fit); self-heating asymmetry about 50 MHz; intracavity
  power 12.5 mW (calculated; not an input-power handling value); film index 1.65-1.72, film roughness 0.34 nm RMS,
  sidewall roughness 1.4 nm RMS / 29 nm correlation length (no parameters); fit uncertainties (< 0.1 dB/cm slope,
  < 0.4 dB intercept, in notes); earlier-group 5.8-6.8 dB/cm (cited ref. 41, rule 3); Fig. 1(a) literature losses.
- Fab: `org_mit` on all rows. Judgment call: first-person fabrication statements (p.4 "Here we realize
  directly-etched waveguides", p.5 "chlorine-based RIE chemistries we use to etch alumina"), authors at MIT EECS and
  MIT Lincoln Laboratory (child of `org_mit` in the registry) -> parent org (D154). Which site processed the 200 mm
  wafers is not stated, so `org_mit_lincoln_laboratory` is not used. No facility acknowledged.
- Judgment call: Fig. 4(a) "slightly undercoupled ring" (loaded Q 275k) is not named by gap; assigned to the 400 nm-gap
  ring because 1/QL = 1/470.2k + 1/660k = 1/274.6k. An auditor may prefer D159 (drop q_loaded / linewidth_mhz).

## lit:deng2019 (Mao et al., SOI adiabatic couplers with design-intended split ratio): 7 components, 18 metrics

- `cmp_lit_deng2019_adc_dw0` ... `_dw25` (`splitter.adiabatic`, 6 rows, one per output width difference 0 / 5 / 10 /
  15 / 20 / 25 nm, all fabricated on the same wafer): measured SR at 1310 nm read off Fig. 13 (46 / 41 / 24 / 13 / 12 /
  7 % for the lower-power port, `extracted_from_figure`, +/- 1 percentage point). 3-dB row: measured Port 3 SR range
  51.5-57.5 % over 1260-1355 nm and simulated 52-53 % (Fig. 14); shared design geometry (w 350 nm, g2 150 nm, L 200 um,
  Lt 5 um, footprint 960 um2 `derived` from Table I 4*240 um2, 220 nm Si). 10 nm row: simulated SR about 21 % and
  simulated SR deviation 1.0292 / 0.6785 % (`coupling_variation`, fractions).
- `cmp_lit_deng2019_gc_pdk` (`fiber_chip_coupler.grating`): "approximately 10 dB loss at 1310 nm", scope unspecified,
  `author_estimate` (per coupler vs pair and origin not stated).
- Not entered: device insertion loss "about 1 dB" over 1260-1320 nm (the authors attribute it mostly to grating-coupler
  uncertainty and call the IL characterization not accurate); Table I "This work" SR 78 %/22 % and maximum variation
  6.2 % (device not named, D159); exponential-fit deviations 6.1 / 2.8 / 6.5 % (fit quality, not a device metric);
  simulated per-region ILs (convergence studies of Figs. 5-9).
- Registry gap: temperature sensitivity of the split ratio. Skipped value: 1.3 % maximum SR variation for stage
  temperature 20-50 C across the O band, measured (simulation 1.6 % for 0-100 C), 3-dB ADC, p.8 Sec. III / Fig. 14 /
  Table I. Proposed parameter `split_ratio_temp_variation_pct` (splitter): largest change of the split ratio in
  percentage points over the stated temperature span (span and wavelength range in condition).
- Fab: none. Passive fabrication sentence (200 mm SOI, 193 nm optical lithography) and "PDK provided by the foundry"
  with the foundry unnamed; process_name empty.

## lit:liu2018b (single-crystalline AlN-on-sapphire UV microrings): 7 components, 88 metrics

- `cmp_lit_liu2018b_ring_w800_g140` (Fig. 2 at 390 nm and Fig. 4(b) at 455 nm), `_ring_w600_g130`, `_ring_w400_g120`
  (Fig. 3), `_ring_w800_g130` / `_ring_w800_g150` (Fig. 4 gap series at 455 nm), `_ring_vis_r60` / `_ring_nir_r100`
  (supplement Fig. S3, 772 nm and 1549 nm). Platform `other` (AlN on sapphire, D515), `resonator.ring`.
- Bases: loaded Q, ER, linewidth `measured` (Lorentzian fits); Q_int at 390 nm and in the supplement `author_estimate`
  (under-coupled regime assumed, D403); Q_int at 455 nm `derived` (over-coupling shown by ER rising with gap, D403);
  alpha_ring at 390 nm / supplement `author_estimate`, 3.5 dB/cm at 455 nm `derived` (measured FSR 675.7 GHz,
  data-determined Q_int). Fig. 3(c)/(d) points not printed in the text entered as `extracted_from_figure` ranges.
- Judgment call: each 390 nm device is a pair of cascaded rings with slightly varied radii on one bus (p.1); which ring
  carries resonance I / II and which FSR is not stated, so one row per (width, gap) design with the resonance in
  `condition` instead of one row per ring. The 455 nm 0.14 um-gap measurement is "the 0.8-um-wide AlN microring"
  (p.4) and is placed on the same design row (same die not stated).
- Printed conflicts (D417, kept with notes): Fig. 3(c) TM00 points at 0.8 um read about 166k / 186k vs printed 156k /
  189k; p.4 attributes the over-coupled TM00 Q_int 226k to "Fig. 2(d)" (a TE panel).
- Supplement rings: presented as measured data in this paper with no citation (D259 does not apply).
- Not entered: Fig. S1 background fluctuation (setup); Fig. S3(c) lambda^-3 fit exponents and the hypothetical
  0.5 / 0.05 dB/cm points; cited values (35k, 24k, 650 / 75 dB/cm, 2.5e6); Fig. 4(d) comparison points; coupler wrap
  angle 20 deg (no resonator parameter for it, in notes).
- Fab / facility: none. Passive process description; acknowledgment thanks two named people "for assistance in the
  device fabrication" with no org printed (p.4); AlN grower (MOCVD) not stated. Possible org for the coordinator
  (not entered): none printed.

## lit:xie2020 (three-mode 3-dB splitter, pixelated meta-structure): 3 components, 21 metrics

- `cmp_lit_xie2020_3mode_splitter` (`splitter.other`, platform `soi`): measured excess loss < 1.5 dB, crosstalk
  > 15 dB, imbalance <= 0.35 dB (TE0 / TE1 / TE2, 1530-1570 nm, one row each since stated once for all modes);
  simulated excess loss < 0.7 dB (TE0) / < 0.9 dB (TE1, TE2), crosstalk > 19 / > 12 (+/-10 nm holes) / > 10 dB
  (400 K); geometry (4.5 x 4 um design region, footprint 18 um2, 1.2 um ports, 160 nm pixel from the Fig. 1 label,
  220 nm Si, 2 um BOX).
- Judgment call: the paper's "insertion loss" is the loss below the ideal 3-dB split (Fig. 2(d)-(f) plot against a
  "-3 dB line") -> `excess_loss_db`, `per_component`, `reference_structure` (normalized to a back-to-back MUX /
  DeMUX). The measured Fig. 5(d)-(f) traces sit about 1-2 dB below 0 dB and the meaning of their 0 dB level is not
  stated (component notes).
- `cmp_lit_xie2020_mux_3mode_ref` (`mode_converter.mdm_mux`): back-to-back MUX / DeMUX reference, IL < 1.3 dB
  (`device_total`, pair, not halved), crosstalk > 16 dB. MUX design from the authors' ref. [16]; the values are this
  paper's own measurements of the reference circuit.
- `cmp_lit_xie2020_gc_te` (`fiber_chip_coupler.grating`): 7 dB/facet measured (C band inferred), 10 deg tilt.
- Not entered: simulated efficiency drop within 1 dB under +/-10 nm hole variation, simulated IL fluctuation < 1 dB
  (TE0, TE1) / within 2 dB (TE2) at 400 K (no parameter for an IL change); computation time.
- Registry gap: nanohole / pixel feature diameter. Skipped value: 130 nm hole diameter, design, p.1-2 Sec. II / Fig. 1.
  Proposed parameter `hole_diameter_nm` (splitter, crossing, mode_converter, reflector, fiber_chip_coupler): diameter of
  etched holes / pixels in a subwavelength or photonic-crystal structure (the existing `hole_radius_nm` candidate from
  D430 would also cover it at half the value).
- Fab: none. First-person "we have fabricated", authors at Harbin Institute of Technology, Shenzhen and Shanghai Jiao
  Tong University (unrelated orgs, D154).

## Missing fab / facility orgs

None to request: no paper names a fabricating org or facility that is absent from the registry. (MIT, MIT Lincoln
Laboratory, McGill University, Yale University, Harbin Institute of Technology Shenzhen, Shanghai Jiao Tong University,
Institute of Semiconductors CAS and Lumentum all exist; only `org_mit` is used.)

## Registry gaps (summary)

| Proposed parameter | Class | Skipped value | Locator |
|---|---|---|---|
| `split_ratio_temp_variation_pct` | splitter | 1.3 % over 20-50 C (measured), 1.6 % over 0-100 C (simulated) | deng2019 p.8 Sec. III, Fig. 14, Table I |
| `thermo_optic_coefficient_riu_per_k` | waveguide_platform, resonator | effective 1.68e-5 RIU/C (from measured shift + simulation), bulk 2.75e-5 RIU/C (author_estimate, cited SiO2 input) | west2019 p.9-10 Sec. IV.B |
| `absorption_loss_fraction_pct` | resonator, waveguide_platform | alpha_abs / alpha_wg about 1 % upper bound | west2019 p.12 Sec. IV.B, Fig. 5(b) |
| `sidewall_roughness_nm` | waveguide_platform | 1.4 nm RMS, 29 nm correlation length (AFM) | west2019 p.6 Fig. 2(c) |
| `hole_diameter_nm` | splitter (and others) | 130 nm | xie2020 p.1-2 Sec. II, Fig. 1 |
