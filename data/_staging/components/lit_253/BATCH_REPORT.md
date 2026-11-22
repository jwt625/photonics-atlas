# Batch lit_253 report

Papers: lit:liu2019c, lit:pitris2018, lit:valicourt2015, lit:joo2018, lit:akca2018 (papers cited in other papers'
benchmark tables; only values each paper reports itself are entered). verified_on 2026-11-22.
Total 29 components / 222 metric rows; `merge_component_staging.py --dry-run`: 0 errors, no warnings on these rows.
Page-1 titles match the source rows; no correction / erratum; no garbled text layer. Generator script kept in the
session scratchpad (`lit_253/gen.py`).

## lit:akca2018 (Interleaved Si3N4 AWG spectrometers, PTL 2019) - 9 components / 74 metrics

- `awg_conv_75ch` (wdm.awg, sin): measured excess loss 8 / 17 dB and overall crosstalk -23 / -18 dB (central / outer,
  p.4, Fig. 5), spectra normalized to a curved reference waveguide (`de_embedded`, `reference_structure`); BPM 4 / 16 dB
  and -28 / -25 dB; Table I design (1 nm, 75 nm FSR, order 18, focal length 1554 um, dL 17.9 um, M = N = 75); 4 x 3.5 cm.
- `awg_interleaved_75ch` (wdm.awg): measured excess loss 7 / 10 dB, adjacent crosstalk about -15 dB (p.4, Fig. 6);
  design 1 nm / 75 nm / 75 channels; 2 x 1.5 cm.
- `awg_primary_3ch`, `awg_secondary_s1`, `_s2`, `_s3` (stages of the interleaved device, fabricated, D80e): BPM values for
  the primary (2.7 dB, -28 / -12 dB) and for S2 (centered 1550 nm: -45 / -41 dB, 0.7 / 4.6 dB, -11 dB); Table I design
  per stage.
- `wg_sin_rib_2um` (around 1.5 dB/cm at 1550 nm, geometry), `bend_r150` (calculated 0.1 dB/cm at R = 150 um),
  `facet_no_ssc` (10 dB fiber-to-chip loss "estimated", author_estimate, scope unspecified).
- Not entered: simulated adjacent crosstalk printed "2.3 dB and 1.5 dB" (sign / magnitude unreadable next to the
  overall values); 3.3 nm center-wavelength shift (no parameter); effective index 1.55 (no parameter); "consistent with
  simulation" resolution / FSR (no number).
- Fab / facility: fab empty (passive fabrication sentence; acknowledgment thanks two individuals for support in the
  device fabrication without naming an org, p.4). No missing orgs.

## lit:joo2018 (2x2 SiN MZI thermo-optic switch, PTL 2018) - 7 components / 53 metrics

- `sw_1310`, `sw_1550` (switch_fabric.other, D158): IL per input port (0.23 / 0.39 dB; 0.48 / 0.62 dB) and crosstalk
  (26.79 / 24.46 dB; 24.72 / 23.6 dB) at the printed wavelengths, normalized by a 3 mm straight reference waveguide
  (p.3); rise / fall 9.55 / 7.7 us and 9 / 8.48 us from the Fig. 9 labels (sum = printed switching speed); footprint
  ~0.7 mm2; 2 x 2 ports.
- `heater_1310`, `heater_1550` (phase_shifter.thermo_optic, D396; espinola2003 / patel2014 split): P_pi 55.6 / 64.4 mW
  (Fig. 8), resistance 5.05 / 5.2 kOhm, TiN 1 mm x 3 um, 3 um above the core.
- `dc_1310`, `dc_1550` (splitter.directional_coupler, BPM only): 50:50 design point, gap 0.7 / 0.9 um, length 44 /
  32.6 um, Table II tolerance cases (six per coupler, first number of the printed ratio).
- `wg_sin_0p5`: 0.09 / 0.33 dB/mm -> 0.9 / 3.3 dB/cm (derived), 0.5 x 0.5 um, 3 um claddings, 50 um bend radius.
- Not entered: Table I (other works, rule 3); grating couplers (800 / 950 nm period, 250 nm etch; no performance, no
  row); simulated mode sizes and bend / heater-spacing loss curves (Fig. 2-3); measured SiN indices; delta-T for pi
  (computed from a cited coefficient).
- Fab / facility: fab `org_electronics_and_telecommunications_research_institute` (first-person "we designed and
  fabricated", p.1 / p.4; all authors ETRI). No facility. No missing orgs.

## lit:liu2019c (100-Gb/s TOSA with silica-PLC AWG, IEEE Photonics J. 2019) - 4 components / 30 metrics

- `plc_awg_4ch` (wdm.awg, ge_silica, purchased): IL < 2.5 dB at the lane centers, 1-dB bandwidth > 10 nm (p.4,
  Fig. 2(b)); nominal 20 nm spacing (specification), 4 x 1 ports, 2 mm input pitch, 12 x 7 mm.
- `ld_plc_two_lens` (chip_chip_coupler.other, hu2017 precedent): 1-dB tolerances > +/-25 um (1st lens X / Y), far
  beyond +/-25 um (1st lens Z), > +/-20 um (2nd lens Z); best CE about -2.5 dB on the test setup (scope unspecified);
  per-lane CE -2.77 / -2.99 / -2.96 / -2.38 dB in the TOSA (author_estimate: rests on the "about 0.5 dB" receptacle term).
- `plc_receptacle_lens` (micro_optics.other): tolerances > +/-15 um (Y), > +/-100 um (Z); coupling loss about 0.5 dB
  (author_estimate, origin not stated).
- `dfb_ld_cwdm4` (laser.dfb, one population row for the four lanes): divergence FWHM 35 / 30 deg, threshold ~5 mA,
  bare-die ~6 mW at 30 mA, TOSA outputs 1.58 / 1.5 / 1.52 / 1.74 mW (ref_plane module), SMSR > 40 dB, S21 bandwidth
  > 18.5 GHz at 35 mA, 200 um length.
- Not entered: FPC RF S11 / S21, eye / BER / ER / OMA (package / link level); ray-tracing curves; core size
  "4.25 um x 4.15 um" (which is width not stated); 2nd-lens shift after curing (~1 um, no parameter).
- Fab / facility: fab `org_huazhong_university_of_science_and_technology` on the two lens-coupling rows (authors
  assembled the TOSA: "we aligned the 2nd lenses", "We have sucessfully fabricated a TOSA"; D399, assembled rows only).
  Missing orgs: **Shijia Photons Technology** (vendor of the purchased AWG chip = fab, p.4 Sec. 2, printed "(Shijia
  Photons Technology)"); **"Mitsubishi"** (vendor of the purchased DFB-LDs = fab, p.4 Sec. 2, printed "(Mitsubishi)";
  registry has org_mitsubishi_electric and org_mitsubishi_materials, no alias for the bare name). Fab empty on those rows.

## lit:pitris2018 (Si 8x8 cyclic AWGR for O band, OE 2018) - 2 components / 30 metrics

- `awgr_8x8` (wdm.awg, soi): measured channel IL 2.5-6.045 dB over 64 port combinations (de_embedded: FA, GC and
  waveguide losses extracted, reference straight waveguides), non-uniformity 3.545 dB, channel crosstalk 11 dB (mean,
  type not stated -> crosstalk_db), 3dB-cumulative crosstalk 6.019 dB (mean) / 0.331 dB (std), 3-dB bandwidth 5.5 nm,
  eight measured mean channel wavelengths (std in notes); simulated IL 1.198-3.255 dB, non-uniformity 2.057 dB,
  bandwidth 5.7 nm, crosstalk > 20 dB; Table 2 design (10 nm, 80 nm FSR, 1301 nm, peak deviation < 6 nm, 8 x 8);
  700 x 270 um2.
- `gc_70nm` (fiber_chip_coupler.grating): 4 dB/GC (per_coupler), peak 1285 nm, 70 nm etch, 6.9 deg, 250 um pitch.
- Not entered: per-port values of Tables 3-4 (summary values entered); 25 Gb/s routing penalties (link level); FA loss
  2 dB (setup, rule 13); Table 1 (other works, rule 3).
- Fab / facility: fab `org_imec`, process_name "imec-ePIXfab silicon photonics passives technology" (p.4). Missing
  org: **ePIXfab** (access provider named with imec in the fabrication sentence, p.4 Sec. 2; D398; precedent
  acoleyen2012 / cabezon2012 left it out for the same reason).

## lit:valicourt2015 (Monolithic integrated slot-blocker, JLT 2016) - 7 components / 35 metrics

The paper reviews the authors' slot blockers. Fig. 2 rows 1, 3, 4 (refs [13], [14], [15]) and the experiments run with
those devices (Fig. 7, Fig. 8(a)) are attributed to the earlier papers: not entered (D259 / D408). Sec. III building
blocks carry no attribution and are entered.

- `sb_tx_pdiv_100ghz` (switch_fabric.other, Fig. 2 row 2 "[This work]"): IL ~25 dB (scope unspecified), maximum
  attenuation > 20 dB (extinction_db), switching speed < 10 ns (rise_time_us, definition not stated).
- `voa_pin` (phase_shifter.other; feng2011 / morichetti2021 precedent; one population row over the 100-400 um lengths,
  D165): > 30 dB "expected" at 8e-3 A/um2 for 100 um (author_estimate), E/O bandwidth ranges read from Fig. 3(c)
  (100 um: about 120-330 MHz; 300 um: about 250-520 MHz), rise / fall < 10 ns, rib geometry.
- `vgc_1pol`, `vgc_2pol` (fiber_chip_coupler.grating, CEA-LETI Epixfab PDK building block): around 5 / 7 dB, scope
  unspecified (text says per coupler, Fig. 4 shows the two-VGC link peaking near -4.6 / -6.3 dB), 10 deg, 70 nm etch.
- `awg_200ghz`, `awg_100ghz` (wdm.awg): IL ranges read from the Fig. 5(b) / (c) channel peaks (2.3-4.9 dB, 8.5-10.2
  dB), neighbor crosstalk < -18 dB, design spacing, 5 um bends, 2 um BOX.
- `bgm` (reflector.bragg): TMM 100 % reflection over ~115 nm (simulated), 290 nm period, duty cycle 52 % (definition not
  stated), SEM labels 70 nm etch / 231 nm Si.
- Not entered: Fig. 2 rows 1, 3, 4 and their system results (D259); AWG "cross-talk ... (>15dB) ... (4-5dB)" (type not
  stated, inconsistent with the < -18 dB neighbor crosstalk); simulated VOA absorption coefficient (Fig. 3(a)); OSNR
  penalties of Fig. 8(b) (link level); polarization rotators (no values); SEM groove thickness 163 nm.
- Fab / facility: fab `org_cea_leti` on all rows ("fabricated ... at the CEA-LETI facilities", p.3). No missing orgs.

## Judgment calls

(a) akca2018 "overall crosstalk (combination of non-adjacent receiver waveguide crosstalks)" -> `crosstalk_cumulative_db`
    (summed non-adjacent crosstalk), not `crosstalk_nonadjacent_db`.
(b) akca2018 interleaved device as `wdm.awg` with its four stage AWGs as separate fabricated rows (Table I design,
    BPM values for primary and S2 only); S1 / S3 rows carry design values only (center wavelength, spacing, FSR as
    author_estimate plus geometry).
(c) akca2018 "around 1.5 dB/cm" entered `measured` (stated directly, D167 analogue) although no method is shown; the
    10 dB facet loss is `author_estimate` ("is estimated").
(d) joo2018 footprint ~0.7 mm2 stated for "the fabricated SiN thermo-optic switch" / abstract entered on both switch
    rows (D254 risk); rise vs fall assigned from the Fig. 9 label positions (10 -> 90 % edge = rise).
(e) joo2018 Table II tolerance coupling ratios entered as simulated `split_ratio_pct` with the first number of the
    printed ratio (port not named).
(f) liu2019c DFB-to-PLC two-lens coupling `chip_chip_coupler.other` (hu2017 precedent) and PLC-to-receptacle lens
    `micro_optics.other`; HUST fab only on these assembled rows; the four lane DFB-LDs as one `laser.dfb` population
    row with TOSA-level values at ref_plane module; lane-to-wavelength mapping treated as not stated (O band inferred).
(g) pitris2018 AWGR IL `de_embedded` + `reference_structure` (merged AWG majority); simulated AWG values in this batch
    use scope `per_component`.
(h) valicourt2015 AWG IL taken from the Fig. 5 peak readings (`extracted_from_figure`) because the printed "< -2dB" /
    "<-8dB" bounds have an ambiguous direction; VOA as one population row (D165) so the family-level < 10 ns and
    bandwidth statements can be entered; the "this work" slot blocker switching speed entered as `rise_time_us` with
    the undefined wording in condition.
(i) valicourt2015 Sec. III building blocks kept (no attribution in their sentences, D408) although the 200 GHz AWG and
    BGM serve the devices of refs [13]-[15].

## Registry gaps (skipped value, locator, proposed definition)

- `center_wavelength_offset_nm` (wdm): akca2018 3.3 nm shift of the interleaved AWG (p.4 Sec. III-C); "measured shift
  of the channel center wavelengths from the design".
- `neff` / effective index (waveguide_platform): akca2018 1.55 (BPM, p.2); "effective index of the stated mode".
- `absorption_coefficient_per_cm` (phase_shifter): valicourt2015 Fig. 3(a) simulated alpha vs bias (curve only; no
  printed value, low priority).
- Groove / etched-region thickness for gratings (reflector): valicourt2015 SEM 163 nm (p.5 Fig. 6(b)); `slab_thickness_nm`
  is defined for ribs only.
- None of these blocks a core metric.
