# lit_138 batch report (distiller, 2026-11-15)

Family: laser (hybrid / heterogeneous ring-filter lasers). Three papers from the benchmark-citation list, all
`restricted_local_only` in `sources.csv` (facts and locators only). Page-1 titles match the source rows; none is a
correction / erratum. boller2019 `garbled_text_layer` covers page 19 only (Fig. 15 graphics); every boller2019 value
comes from clean text, and the figure-read wavelength spans were taken from the page renders (p.10, p.19, p.20).
Validator: `merge_component_staging.py data/_staging/components/lit_138 --dry-run` -> +14 components, +68 metrics,
0 errors (only warning: the existing merged cmp_lit_ni2025b_pimmwc-m18).

| paper | components | metric rows |
|---|---|---|
| boller2019 | 5 | 23 |
| rees2020 | 5 | 23 |
| morton2021 | 4 | 22 |
| total | 14 | 68 |

Each paper's own reported values only (rules 1 and 3); values in the comparison text (other groups' lasers, Fig. 1
of boller2019) are not entered.

## boller2019 (overview of hybrid InP-Si3N4 lasers with Si3N4 feedback circuits, Photonics 2020; arXiv v2 text)

- Rows: `two_ring_laser` (laser.tunable, Sec. 4: 24 mW fiber, threshold 8-19 mA vs outcoupling, slope 0.13 W/A,
  SMSR 63 dB, 120 nm coverage, 2.2 kHz intrinsic, Vernier FSR 50 nm); `dual_gain_laser` (laser.tunable, Sec. 5:
  105 mW fiber / 117 mW on-chip, > 70 mW and SMSR > 50 dB over 1470-1570 nm, about 320 Hz, RIN about -170 dB/Hz,
  ring FSRs 208 / 215 GHz); `dual_gain_output_coupling` (fiber_chip_coupler.edge, 0.5 dB per facet);
  `dual_wavelength_laser` (laser.tunable, Sec. 7.2: SMSR 40-50 dB); `visible_vernier_rings` (resonator.ring,
  Sec. 7.3: Vernier FSR about 10 nm, about 1.5 pm peak width estimated, R 1200 / 1205 um, specified 5 % coupling).
- Not entered (rule 3 / D259a, values reproduced from the authors' own earlier papers):
  - Sec. 6 three-ring record-linewidth laser: introduced as "the improved version presented here [108]" (Fan et al.,
    arXiv 2019, co-authors); the 40 Hz sentence and the intracavity-power estimate cite [108]. All Sec. 6 values out:
    40 Hz, 210 Hz at 3 mW, threshold about 42 mA, 23 mW at 320 mA, > 70 nm with > 1 mW, SMSR > 60 dB, ring radii
    99 / 102 / 1485 um, FSR 278 / 18.6 GHz, Q about 2000 / 290000, 1000 um gain section, 90 % back facet, 0.5 m
    roundtrip, 2 / 0.15 nm hop steps.
  - Sec. 7.1 comb laser: "as shown in Fig. 12 [168]" (Mak et al., Opt. Express 2019, co-authors); Fig. 13 caption
    also points to [168]. Out: 17 lines, 5.5 GHz spacing, 18 kHz beat linewidth, 34 kHz average comb-line linewidth,
    2 mW, about 6 cm roundtrip, ring radii 136.5 / 140.9 um, 10 % coupling, 90 % HR.
  - Table 1 / Fig. 3 linewidth-model inputs and predictions (calculation, not a device).
  - Cited values: 0.2 dB Si3N4 coupling (ref. [124]), < 0.1 dB/m Si3N4 loss (ref. [141]), earlier 1.7 / 7.4 / 10 mW
    and 24 kHz values (refs. [140], [82], [144], [87]).
- Also not entered: "meanwhile ... reliably above 40 mW, sometimes above 50 mW" (p.9) describes the laser type, not
  this device (D254); 10 % ring coupling of the dual-gain laser (no parameter on laser rows; note); dual-wavelength
  operating points (12 nm / 1.5 THz separation, 0.09 nm / about 11 GHz beat) are settings, not performance; the
  -172 dBc/Hz shot-noise level is a calculation.
- Fab empty on all rows: "lasers that we have fabricated and characterized" (p.8) with authors at the University of
  Twente and LioniX International (D154: no single own org). No facility acknowledged.
- Judgment calls: (1) Sec. 5 dual-gain values kept although the record-power sentence (p.12) cites the co-authors'
  ASSL 2019 conference paper [149]: the "we achieve" sentence and Fig. 9 / Fig. 10 carry no citation, so this is read
  as a journal re-presentation (D408); if the coordinator reads [149] as attribution (D259a strict), delete the
  dual_gain_laser and dual_gain_output_coupling rows. (2) Sec. 4 two-ring laser kept: no value there carries a
  citation; the same numbers appear in lit:rees2020 (cross-note in component notes; threshold there 14 mA at 80 %
  outcoupling and 20 C vs 8-19 mA here). (3) The 0.5 dB fiber coupling is a separate `fiber_chip_coupler.edge` row
  (D167 measured, per_facet); coupling geometry unstated, wavelength `unspecified` (laser range 1470-1570 nm in
  notes). (4) 117 mW on-chip `derived` (fiber power + stated 0.5 dB, D394). (5) Visible two-ring Vernier as one
  `resonator.ring` row (fan2025a precedent), fabricated test circuit without a laser.

## rees2020 (ring-resonator enhanced mode-hop-free tuning of a hybrid InP-Si3N4 laser, Opt. Express 2020; arXiv text)

- Rows: `ecl` (laser.tunable: 24 mW fiber, threshold 14 mA (20 C), 120 nm coverage, SMSR 63 dB, 2.2 kHz intrinsic,
  laser-cavity FSR 0.034 nm, mode-hop-free range 0.22 nm, tuning 0.31 / 0.11 pm/mW measured and 0.29 pm/mW from
  Eq. 1); `vernier_mrrs` (resonator.ring: Vernier FSR 50.5 nm, kappa^2 7.1 % measured and 10 % design,
  circumferences 885.1 / 857.4 um, bend radius >= 100 um); `triplex_wg` (waveguide_platform.straight: about
  0.1 dB/cm, bend radius 100 um); `phase_heater_1mm` (phase_shifter.thermo_optic: P_pi 290 mW, >= 2.5 pi, 1 mm);
  `ring_heater` (phase_shifter.thermo_optic: P_pi about 380 mW, 1.6 pi reached).
- Not entered: InP gain chip as an amplifier row: its only performance value (gain bandwidth >= 120 nm around
  1540 nm) sits in the sentence citing the chip reference [30] (rule 3); the chip's HR about 90 % (no reflector part),
  9 deg / 19.85 deg interface angles (geometry only, no coupling loss reported, so no chip_chip_coupler row);
  10 kHz earlier linewidth (ref. [26]); tuning ratios 0.107 / 0.103 and model 0.108 / 0.105 (no parameter);
  tuning sensitivity 10 / 28 pm/rad (no parameter); tuning resolution about 0.12 pm (about 15 MHz) per 0.37 mW
  (no parameter); effective optical cavity length 3.5 cm and length enhancement 13.7 (no parameter); projected
  1.6 nm / > 2 nm ranges (hypothetical); acetylene line data (reference gas, setup).
- Fab empty on all rows. The gain chip "is fabricated by the Fraunhofer Heinrich Hertz Institute" (p.3), but there is
  no gain-chip row (see above) and Contract v7 keeps a part's fab off the assembled laser row; recorded in the laser
  notes. No fabrication statement for the TriPleX feedback chip; "mask design" thanks name a person only (no org).
- `process_name` "TriPleX" on the Si3N4 rows: printed only as the Fig. 2(a) label "Si3N4 / SiO2 (TriPleX)"; named
  process without a named fabricator (fab empty, said in notes).
- Judgment calls: (1) 0.1 dB/cm and the 100 um bend radius follow the sentence "as described by Roeloffzen et al
  [31]" with no measurement shown: kept as `author_estimate` with the note (D80i borderline); delete if the
  coordinator reads them as cited. (2) Heater P_pi 290 / 380 mW and the phase ranges are `author_estimate` (origin not
  stated; D167 is limited to coupling loss). (3) Temperature 25 C (default TEC setting, p.4) set on the rows whose
  measurement does not state another temperature; 20 C on the Fig. 3 rows. (4) kappa^2 0.071 stored as 7.1 %
  `derived` (fraction -> %, D256).

## morton2021 (Integrated Coherent Tunable Laser, JLT 2022)

- Rows: `ictl` (laser.tunable: 118 nm tuning at 500 mA, threshold about 125 mA, SMSR > 50 dB close-in and > 40 dB
  wide over 1490-1600 nm, 1.54 mW fiber at 1555 nm, about 15 mW on-chip (author_estimate), Lorentzian < 95 Hz at
  400 mA, 410 Hz at 300 mA, 360 Hz at 500 mA, RIN about -160 dB/Hz (no EDFA, 3 GHz) and about -155 dB/Hz worst case
  (EDFA + assumed 5 dB NF, author_estimate), chip 9.5 x 1.7 mm footprint derived); `three_ring_reflector`
  (reflector.loop_mirror: simulated sidelobe suppression >= 8.4 dB over 120 nm and >= 20 dB within +/- 100 GHz; SOI
  500 nm / 56 nm etch / 1 um BOX); `mrr1` (resonator.ring: R 599.967 um, FSR 22.1 GHz and group index 3.6064
  simulated); `output_facet` (fiber_chip_coupler.edge: about 10 dB per facet, author_estimate).
- Not entered: -3 dB gain bandwidth about 69 nm ("described in [24]"), taper transitions about 0.5 dB and -33 dB
  reflection (sentence cites [24], [25]), ULL Si 0.16 dB/cm (ref. [20]), Si3N4 reflector sidelobe 15 / 20 dB
  (ref. [17]), FBG E-DBR 15 Hz / 150 mW / -165 dB/Hz (refs. [13], [14]); assumed ULL Si loss 0.25 dB/cm (design
  input); peak reflectivity 0.5 (text says amplitude; Fig. 3(a)-(c) peaks near -3 dB / 0.5 read as power: definition
  conflict, not entered either way); design FWHM 0.36 GHz, effective length 108 mm / 1.3 ns, single-ring reflection
  bandwidth 0.74 GHz (width definition unstated), ring delay 409 ps; ring 2 radius 600.856 um (no performance value of
  its own, in notes); "above 60 dB at longer wavelengths" (range not stated, Fig. 9 dips below 60 dB near
  1555-1560 nm); facet reflectivity R about 0.32 (natural, not measured); "closer to 1 dB" inverse-taper coupling
  (hypothetical); MRR heater powers for the tuning extremes (settings).
- Fab `org_ucsb` on all four rows: "ICTL devices were fabricated on the UCSB heterogeneous silicon photonics platform"
  (p.4, passive sentence naming the org, Contract v7 / D455); `process_name` "UCSB heterogeneous silicon photonics
  platform" as printed. No facility acknowledged. Facet dicing / polishing maker not stated (note on the facet row).
- Judgment calls: (1) JLT extension of the authors' OFC 2021 paper (ref. [4]); no value or figure is attributed to it,
  values kept (D408). (2) Reflector and ring values are design simulations of parts on the fabricated chip:
  `row_kind` fabricated, basis simulated (D80e, D82a); MRR1 FSR and group index `simulated` (Sec. II states all
  designs come from the reflector simulation tool). (3) Platform `soi_rib` for the ULL shallow-etch rings / reflector
  and `soi_strip` for the polished strip output (D434); the laser row `other` (heterogeneous III-V/Si, merged
  xiang2021a precedent). (4) 360 Hz at 500 mA entered without a qualifier as printed; the paper says the floor was
  not reached.

## Missing fab / facility orgs

None needed: `org_ucsb` exists. For reference only (not entered as fab per rules): Fraunhofer Heinrich Hertz
Institute (gain chip maker, rees2020 p.3) exists as `org_fraunhofer_heinrich_hertz_institute`; it would apply only if
a gain-chip row is added.

## Registry gaps (skipped value + locator, proposed definition)

- `effective_cavity_length_mm` (laser): rees2020 3.5 cm (p.4 Sec. 2), morton2021 108 mm (p.3 Sec. II, design);
  "effective optical cavity length including resonant ring enhancement, as stated".
- `tuning_sensitivity_pm_per_rad` (laser): rees2020 10 / 28 pm/rad (p.8 Sec. 4); "lasing-wavelength shift per radian
  of phase-section phase".
- `tuning_resolution_pm` (laser): rees2020 about 0.12 pm per 0.37 mW (p.7 Sec. 3.3); "smallest demonstrated
  continuous wavelength step".
- `bw_fwhm_ghz` widened to reflector: morton2021 design FWHM 0.36 GHz (p.3 Sec. II).
- `group_delay_ps` (reflector / resonator): morton2021 1.3 ns reflector, 409 ps ring (p.2-3 Sec. II).
- `power_coupling_pct` widened to laser (intracavity ring coupling stated without a ring row): boller2019 10 %
  (p.12 Sec. 5).
