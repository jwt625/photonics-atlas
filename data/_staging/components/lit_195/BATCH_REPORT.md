# lit_195 batch report

Papers: `lit:ahmmed2020` (Optics Express 28(19), 2020), `lit:du2019` (Optics Express 27(5), 2019), `lit:song2024b`
(JLT 42(23), 2024), `lit:qiu2017` (JLT 35(9), 2017), `lit:liu2024b` (IEEE PTL 36(10), 2024). Page-1 titles match the
source rows; no `garbled_text_layer`; the IEEE copies carry an institutional download stamp (ignored). Figure values
were read on the page renders and on PyMuPDF crops of the cached PDFs. verified_on 2026-11-18.

Dry run: `merge_component_staging.py data/_staging/components/lit_195 --dry-run` -> +19 components, +149 metrics,
0 errors (the one WARN is on an existing ni2025b row, not this batch).

## Components / metric rows

| paper | component_id | class | metrics |
|---|---|---|---|
| ahmmed2020 | cmp_lit_ahmmed2020_te2_pass_filter_3mode | mode_converter.other | 24: measured extinction TE2-to-TE0 / TE1 20.57 / 21.59 dB and TM2 18.91 / 18.06 dB at 1550 nm, C-band bounds > 17.05 / 20.87 / 16.34 / 17.52 dB; IL 6.70 (TE2) / 6.91 (TM2) dB device_total (fiber input included, multiplexer deducted); excess ~1.30 dB (author_estimate, budget term); simulated EL 0.42 / 0.33 dB and rejections > 19.82 / 31.68 / 19.44 / 27.21 dB; geometry (core 4.53 um, claddings, W2, W0, L1, total length) |
| ahmmed2020 | cmp_lit_ahmmed2020_te3_pass_filter_4mode | mode_converter.other | 30: same structure (6 extinction at 1550 nm, 6 C-band bounds, IL 7.32 / 7.25 dB, ~1.35 dB excess, simulated EL 0.47 / 0.37 dB and 6 rejections, geometry) |
| ahmmed2020 | cmp_lit_ahmmed2020_mux_3mode | mode_converter.mdm_mux | 2: ~4.28 dB loss, extinction > 21 dB over C band (reference device) |
| ahmmed2020 | cmp_lit_ahmmed2020_mux_4mode | mode_converter.mdm_mux | 2: ~3.45 dB loss, extinction > 20 dB over C band |
| ahmmed2020 | cmp_lit_ahmmed2020_epocore_channel_wg | waveguide_platform.straight | 3: material loss 2.75 / 2.95 dB/cm (author_estimate, budget terms), core 4.53 um |
| ahmmed2020 | cmp_lit_ahmmed2020_lensed_fiber_input | fiber_chip_coupler.edge | 2: input coupling 2.65 / 2.90 dB per facet (author_estimate, budget terms) |
| du2019 | cmp_lit_du2019_fano_device_a | resonator.other | 6: extinction 22.3 dB within 54 pm and 16.45 dB over the 23 pm fit range (near 1552.4 nm, Fig. 5(d) axis), 420 nm width, 340 nm Si, loop radii 20 / 10 um (halved Fig. 4(a) diameter labels) |
| du2019 | cmp_lit_du2019_fano_qc170 / _qc450 | resonator.other | 2 each: estimated Qc 170 / 450 (author_estimate), averaged maximum extinction ~13.0 / ~19.2 dB (Fig. 5(f) bars) |
| du2019 | cmp_lit_du2019_highq_fp_device_b | resonator.photonic_crystal | 3: Q ~13000 (q_loaded, typical), width, Si thickness |
| du2019 | cmp_lit_du2019_pte_device_c | reflector.loop_mirror | 3: PTE reflection 35 % at 1552 nm (derived from the printed 0.35), width, Si thickness |
| song2024b | cmp_lit_song2024b_mzs_2x2 | switch_fabric.other (D158) | 17: measured EL ~0.25 dB / ER > 17 dB over 1460-1625 nm, EL ~0.2 dB / ER > 20 dB over 1470-1617 nm, ER > 25 dB C band (Table III), 20.8 dB uncalibrated at 1550 nm, > 20 dB in the heater sweeps at 1455 / 1550 / 1630 nm; simulated EL < 0.13 / < 0.21 dB and ER > 22.6 / > 19.5 dB; ports, stack |
| song2024b | cmp_lit_song2024b_fac_3db | splitter.adiabatic | 10: simulated split 47.5-52.5 % and EL 0.020-0.054 dB over 1460-1625 nm, Table IV experimental ~0.125 dB (author_estimate), L 30 um, gap 205 nm, w1 / w2 / w3, stack |
| song2024b | cmp_lit_song2024b_to_ps_1um | phase_shifter.thermo_optic | 5: Q_pi ~16.1 mW at 1550 nm (derived, 17.6 - 1.5 mW), simulated 12.0-13.75 mW over 1450-1650 nm (Fig. 4 read), wco 1 um, Lco 100 um, Si 220 nm |
| qiu2017 | cmp_lit_qiu2017_adf_te1_w1200 | wdm.bragg_cdc | 10: through notch 35 dB at 1551.5 nm, centre 1551.5 nm, drop loss 0.6 dB, add -> through 1.3 dB, period 310 nm, W 1.2 um, length 500 um, stack |
| qiu2017 | cmp_lit_qiu2017_adf_te2_w1300 | wdm.bragg_cdc | 6: notch 21 dB at 1564 nm, centre, drop loss 2 dB, period 330 nm, W 1.3 um, Si 220 nm |
| qiu2017 | cmp_lit_qiu2017_adiabatic_coupler_pair | mode_converter.converter | 4: drop -> add 1.0 dB and input -> through 0.2 dB at 1550 nm (device_total), worst crosstalk ~13.7 dB (Fig. 5 read), L 300 um |
| qiu2017 | cmp_lit_qiu2017_phc_gc | fiber_chip_coupler.grating | 2: coupling loss 20 dB (scope unspecified, C band inferred), 3-dB bandwidth 12.8 nm |
| liu2024b | cmp_lit_liu2024b_rib_adc_3db | splitter.adiabatic | 16: EL < 0.18 dB over 1450-1600 nm (cascade regression), Fig. 7 regression 0.03-0.19 dB, simulated < 0.15 dB, coupling variation 0.052 (printed 5.2 %), cross-port split 46.7-54.6 % (Fig. 6(d)), L 78 um, G2 100 nm, W1 / W2 / W3 = W4, Lt 10 um, stack (220 / 160 / 60 nm, 2 um BOX and cladding) |

Totals: ahmmed2020 6 / 63, du2019 5 / 16, song2024b 3 / 32, qiu2017 4 / 22, liu2024b 1 / 16 (components / metrics).

## Values not entered and why

- du2019: maximum slope 0.77 dB/pm (p.2, p.6, p.7) and the Fig. 5(e) averaged slopes (~0.39 / ~0.45 dB/pm): no
  registry parameter (gap below). Device B FSR: not printed. MMI 34 x 6 um (Fig. 4(a)): no mmi parameter on resonator
  (notes). Comparison values of other works (17 dB over 56 pm, 8.5 dB over 22 pm, refs. [11], [7]): cited (rule 3).
  Fig. 3(e) CMT predictions: model curves with no printed values.
- song2024b: random phase imbalance 0.09 pi and calibration power Q0 ~1.5 mW (no parameter; Q0 used only for the
  Q_pi arithmetic); 16 x 16 crosstalk below -15 dB (theoretical projection); Table II tilt angles (notes only);
  Tables III / IV values of other works (rule 3); Fig. 2 coupling-coefficient map (arbitrary units).
- qiu2017: measured bandwidths 3 / 4.4 / 5.8 nm (W = 1.2 / 1.1 / 1.0 um) and 2.9 nm (TE0-TE2): the level is not
  stated and the paper's Eq. (5) is the null-to-null Bragg bandwidth, so neither bw_3db_nm nor any wdm parameter fits
  (registry gap); the W = 1.0 / 1.1 um devices therefore have no row (rule 9), values in component notes. Calculated
  16-2 nm and 26 nm bandwidths (Fig. 3, abstract): simulated with no device row. BPM conversion efficiency over 95 %
  (Fig. 4): a 200 um design with other widths than the fabricated 300 um test coupler. Corrugation width 100 nm, duty
  cycle 50 %: no parameter on wdm. Drop-loss improvement of 1.5 dB over ref. [17] (authors' earlier filter): cited.
- liu2024b: "150 nm bandwidth" for 3-dB splitting (no criterion; equals the 1450-1600 nm laser range; liu2023a handled
  the same way); simulated +/-50 nm width / +/-10 nm height tolerance (Fig. 4, no printed values, no parameter); Fig. 2
  design sweep; Table II values of other works (rule 3).
- ahmmed2020: Table 1 core separations D (4.70 / 3.58 um; gap_nm not allowed on mode_converter), CW / MMFW lengths and
  Taper3 separations (notes); the TE1-pass and TE2-pass design variants (simulated widths only); effective indices.

## Missing fab / facility orgs

None needed. Fab ids used exist: `org_city_university_of_hong_kong` (ahmmed2020), `org_cornerstone` (du2019, p.7
acknowledgment), `org_shanghai_institute_of_microsystem_and_information_technology` (liu2024b). song2024b ("standard
180-nm silicon photonics foundry processes", p.4) and qiu2017 (passive EBL sentence, p.3) name no fabricator. No shared
facility is named in any of the five papers. Material supplier only: micro resist technology GmbH (EpoCore / EpoClad,
ahmmed2020 p.8; in notes).

## Judgment calls

- (a) liu2024b is the same group, stack and Table I design (L = 78 um) as merged lit:liu2023a (its ref. [16]); the
  measured values here are not attributed to ref. [16] and differ (EL < 0.18 vs < 0.22 dB), so kept (D408) with a
  cross-note. Fab SIMIT from first-person EBL / etch sentences with all authors at SIMIT (also UCAS), as liu2023a.
  Region III length stored as `coupling_length_um` (dc template field) while merged liu2023a uses `taper_length_um`
  for the same L: coordinator may align one way.
- (b) du2019 fab `org_cornerstone` on device A and the two Qc-study devices (the acknowledgment names "the prototype
  device"); devices B and C ("also fabricated", passive) left empty. Qc 170 / 450 devices as sibling rows (whether
  either is device A is not stated); their Qc values `author_estimate` ("estimated", method not stated). PTE 0.35
  "reflection coefficient" stored as power reflectivity 35 % (the formula uses measured port powers). Device A
  wavelength 1552.4 nm read off the Fig. 5(d) axis (`wavelength_inferred`).
- (c) song2024b FAC experimental ~0.125 dB (Table IV only) `author_estimate`: it equals half the MZS ~0.25 dB with no
  FAC test structure or arithmetic shown. Split ratio stored as the 47.5-52.5 % span of both printed extreme ratios
  (port order not stated). Q_pi 16.1 mW `derived` from the two printed heater powers (patel2014, D619). The "> 20 dB"
  heater-sweep extinction at 1455 / 1630 nm kept as printed with a note: outside the 1470-1617 nm span where the
  stitched spectra give > 20 dB (single-wavelength sweep vs stitched spectra, D417). Measured-row polarization left
  empty (not stated in Sec. III).
- (d) qiu2017 bandwidths not entered (see above); the corrugation-free coupler pair as `mode_converter.converter`
  (li2023a drop coupler, D540) with `device_total` scope (path through both couplers); GC 20 dB "coupling loss" scope
  `unspecified` (per coupler vs pair not stated), C band inferred; 35 dB notch kept although the Fig. 6 axis clips at
  -30 dB.
- (e) ahmmed2020 fab CityU from first-person fabrication sentences with all authors at CityU (first author also
  University of Chittagong). Filter insertion losses `measured` + `reference_structure` (normalized to the launched
  power with the reference multiplexer loss deducted), scope `device_total` including the input fiber coupling. The
  loss-budget terms (excess ~1.30 / ~1.35 dB, material 2.75 / 2.95 dB/cm, coupling 2.65 / 2.90 dB) are
  `author_estimate` (origin not stated). Reference multiplexers entered as `mode_converter.mdm_mux` rows: designs cited
  (refs. [21], [22]) but the loss / extinction are this paper's measurements; fab CityU on both ("we fabricated a
  three-mode multiplexer", p.9; the four-mode one on the same substrate as the first-person-fabricated filter).

## Registry gaps (skipped value + locator, proposed definition)

- `max_slope_db_per_pm` (resonator): maximum transmission slope of a resonance line shape (fit range in condition).
  du2019 0.77 dB/pm over 23 pm (p.6, Fig. 5(d)); averaged ~0.39 / ~0.45 dB/pm for Qc 170 / 450 (Fig. 5(e)).
- Bragg bandwidth with unstated level / null-to-null on wdm (`stopband_width_nm` widened to wdm, D552 gap, or
  `bw_null_nm`): qiu2017 3 / 4.4 / 5.8 nm (p.4, Fig. 7) and 2.9 nm (p.4, Fig. 8).
- `fill_factor` and a `corrugation_width_nm` (sidewall-grating corrugation) on wdm: qiu2017 duty cycle 50 %,
  corrugation 100 nm (p.3).
- `gap_nm` on mode_converter (D428 / D533): qiu2017 coupler gap 200 nm (p.3); ahmmed2020 ADC core separation 4.70 /
  3.58 um (p.6 Table 1).
- `phase_imbalance_pi` (switch_fabric, D453 candidate): song2024b random phase imbalance 0.09 pi at 1550 nm (p.4).
