# lit_255 batch report

Papers: lit:bogaerts2011 (IEEE Photonics J.), lit:schall2016 (Optics Express), lit:luyssaert2005 (JLT), lit:gao2021a
(IEEE PTL), lit:acoleyen2011b (GFP 2011). Page-1 titles match the source rows; the download stamp in the gao2021a,
acoleyen2011b and luyssaert2005 text layers was ignored. acoleyen2011b has OCR-style character errors in the text layer
("O.S-2dB", "SdB", "SOOnm"); every value from it was checked against the page renders (p.2, p.3). verified_on
2026-11-23. Dry run: +32 components, +136 metrics, 0 errors (the only warning is the pre-existing ni2025b duplicate, not
in this batch). No existing rows for these sources. Comparison values the papers cite (schall2016 Table 1 metal-heater
columns, gao2021a refs. [9] / [18], bogaerts2011 refs. [13]-[16]) are not entered.

## Components / metric rows

| paper | component | class | metrics |
|---|---|---|---|
| bogaerts2011 | cmp_lit_bogaerts2011_wire_wg_460 | waveguide_platform.straight | 5 (1.36 dB/cm at 1550 nm; 1.2-1.5 dB/cm over 1500-1580 nm; 460 / 220 nm, 2 um BOX) |
| bogaerts2011 | cmp_lit_bogaerts2011_wire_bend_r{2,3,4p5}_a{...} (10 rows) | waveguide_platform.bend | 3 each (bend loss per 90 deg; radius; width): r 2 um alpha 0 / 5 / 10 / 25 / 45 deg; r 3 um alpha 0 / 5 / 10; r 4.5 um alpha 0 / 45 |
| bogaerts2011 | cmp_lit_bogaerts2011_rib_wg_700 | waveguide_platform.straight | 8 (0.2718 dB/cm bilinear fit; Table 1 0.271 / 0.286 / 0.33 per wire-width die; 700 nm, 70 nm etch, 220 nm, 2 um BOX) |
| bogaerts2011 | cmp_lit_bogaerts2011_hybrid_bend | waveguide_platform.bend | 5 (0.0273 dB/90 deg incl. two transitions; Table 1 0.027 / 0.032 / 0.068; R 5 um) |
| bogaerts2011 | cmp_lit_bogaerts2011_rib_wire_taper | waveguide_platform.other | 4 (0.012 dB per transition, author_estimate; 15 um; 460 nm wire end; 70 nm etch) |
| schall2016 | cmp_lit_schall2016_graphene_heater | phase_shifter.thermo_optic | 7 (330 pm/mW; 22 mW per FSR; rise 3.0 / fall 3.6 us; 4 kOhm; 3.5 um wide; 0.24 um gap) |
| schall2016 | cmp_lit_schall2016_si_ring | resonator.ring | 8 (Q 20,000; FSR 7.2 nm; R 9 um derived; 350 nm rib, 180 nm etch, 40 nm slab, 220 nm, 2 um BOX) |
| luyssaert2005 | cmp_lit_luyssaert2005_seg_taper_14sec_1p5um | waveguide_platform.other (design) | 3 (99 % 2-D; > 98 % over 1500-1600 nm; 1.5 um) |
| luyssaert2005 | cmp_lit_luyssaert2005_linear_taper_1p5um / _parabolic_taper_1p5um | waveguide_platform.other (design) | 2 each (84 % / 80 % 2-D; 1.5 um) |
| luyssaert2005 | cmp_lit_luyssaert2005_spline_taper_3d_1um | waveguide_platform.other (design) | 2 (85 % 3-D bidirectional; 1.0 um) |
| gao2021a | cmp_lit_gao2021a_sin_{advanced,normal}_bend_r{30,40,50} (6 rows) | waveguide_platform.bend | 4 each, 6 for r 30 (bend loss at 1550 nm; r 30 wafer mean / std over 54 dies; radius, 1000 nm, 400 nm) |
| gao2021a | cmp_lit_gao2021a_si_advanced_bend_r3 / _r4, _si_normal_bend_r5 | waveguide_platform.bend | 8 / 5 / 5 (0.0065 / 0.0027 / 0.012 dB/90 deg; r 3 wafer mean 0.0069, std 0.00171, median 0.0065 over 25 dies; radius, 500 / 220 nm, 3 um BOX) |
| acoleyen2011b | cmp_lit_acoleyen2011b_lens_taper_te_r5 | waveguide_platform.other | 8 (0.5-2 dB measured, f 16-22 um; > 95 % 2-D, ~87 % 3-D simulated; f 16-22 um, 450 nm, 70 nm, 220 nm, 2 um) |
| acoleyen2011b | cmp_lit_acoleyen2011b_lens_taper_tm_r6 | waveguide_platform.other | 4 (~4-5 dB per taper, derived from the two-taper structure; f 9-15 um; 500 nm; 70 nm) |
| acoleyen2011b | cmp_lit_acoleyen2011b_lens_taper_tm_r5_design | waveguide_platform.other (design) | 2 (85 % 2-D, ~34 % 3-D) |

Per paper: bogaerts2011 14 / 52, schall2016 2 / 15, luyssaert2005 4 / 9, gao2021a 9 / 46, acoleyen2011b 3 / 14.

## Values not entered and why

- bogaerts2011: grating-coupler efficiency 31 % (p.6; sentence cites refs. [25], [26], D80i). Fig. 7 points r 3 um
  alpha 25 / 45 deg and r 4.5 um alpha 5 / 10 / 25 deg (overlapping markers near 0.004-0.006 dB, D156). Wafer-level
  variation 0.016 dB/cm and 0.001 dB/90 deg over five chips (p.11; statistic not defined, Fig. 14 chip values span about
  0.26-0.30 dB/cm, so neither std nor range fits). Fig. 14 per-chip values (figure-only). Fig. 3 / Fig. 4 footprint
  penalties and Fig. 9 single-mode cut-off (simulation / geometry, no parameter).
- schall2016: thermal breakdown at 33 mW heater power (p.5; registry gap below); 48 h endurance (resistance 5.5 -> 4.8
  kOhm, resonance 1357.89 / 1357.91 nm; not cycles); FOM 73 nWs (Table 1; no parameter); simulated graphene absorption
  5.8e-4 dB/um (per-length phase-shifter loss rejected, D250); 4-6 kOhm across heaters (family statement, D254; the
  measured device's 4 kOhm is entered); graphene mobility / Fermi level (material, reference samples); 40 pm
  post-fabrication shift (attributed by the authors to a 0.8 K ambient change, not a device property).
- luyssaert2005: all Fig. 2 / 6 / 11 / 12 curves except the text-stated points (figure-only design curves); "up to 20 %"
  improvement (relative). No measured device (Fig. 10 is a resist image).
- gao2021a: Fig. 2 simulated bend losses and mode fractions (3-D FDTD, figure-only); Fig. 3(c) / Fig. 5 C-band spectra
  (figure-only; text says flat); SiN advanced-bend median (printed equal to the mean, 0.037); 95 % confidence intervals
  (in notes). Clothoid / Euler values 0.002 / 0.0018 dB (cited refs. [18], [9]).
- acoleyen2011b: Table I effective indices and thin-lens focal lengths 21.4 / 11.8 um (calculations); TM 2-D "up to
  90 %" (not tied to one radius, D156); simulated "few percent over 100 nm"; conclusion summaries "about 1 dB" (TE) and
  "about 5 dB" (TM) kept in notes rather than as second rows; per-f values (the paper says the lengths are not
  distinguishable within the measurement error).

## Fab / facility orgs

- bogaerts2011: fab org_imec ("fabricated in the imec 200 mm CMOS pilot line", p.6; acknowledgment p.11). Missing org:
  **ePIXfab** (fab role, MPW service): printed "the ePIXfab MPW", p.11 Acknowledgment ("for the fabrication of their
  devices"). Same string is already queued from D616 (acoleyen2012).
- schall2016: fab empty (passive e-beam / transfer steps, all authors AMO GmbH, no first-person sentence, D80b); no
  facility (grants only). AMO GmbH exists as org_amo should the auditor read the affiliation "Advanced Microelectronic
  Center Aachen (AMICA), AMO GmbH" plus the methods as sufficient.
- luyssaert2005: no fabrication, no orgs.
- gao2021a: fab org_amf ("we fabricate both Si and SiN waveguide bends in the same wafer", p.2, on the "standard
  SiN-on-SOI platform in Advanced Micro Foundry (AMF)", p.1; all authors AMF). process_name "AMF standard multi-layer
  SiN-on-SOI platform (200 mm)".
- acoleyen2011b: fab org_imec ("fabricated on SOI at imec, Leuven", p.1); ePIXfab only cited for the process (ref. [3]):
  process_name "(ePIXfab silicon photonics platform cited, ref. 3)" (acoleyen2011 precedent, D616). The Stevin
  Supercomputer Infrastructure (Ghent University) acknowledgment is compute, not a facility.

## Judgment calls (for the auditor)

1. bogaerts2011 wire bends: one row per (minimum radius, spline coverage) design (song2020 / sun2022a precedent), not one
   radius-series row as in bogaerts2010; Fig. 7 values `extracted_from_figure` (+/-0.002 dB). The r 3 um circular bend
   uses the conclusion's printed 0.037 dB (`measured`) although the Fig. 7 marker reads about 0.032 (D417 note).
   Fig. 7 wavelength not printed: `c_band` inferred.
2. bogaerts2011 rib loss and hybrid-bend loss: 1550 nm `wavelength_inferred` from the Fig. 14 "at 1550 nm" wafer
   measurement; Table 1 wire-width dies kept as conditions on the rib and hybrid-bend rows (dose sweep of one design),
   not as separate components.
3. bogaerts2011 rib/wire transition 0.012 dB: `author_estimate` (rests on the authors' 0.004 dB spline-bend estimate at
   r 5 um, a radius Fig. 7 does not contain); class waveguide_platform.other with insertion_loss_db (same-layer
   rib-to-strip taper, dai2012 / wang2014b precedent) rather than waveguide_platform.transition.
4. bogaerts2011 hybrid-bend radius 5 um taken from the estimate sentence (p.10); platform `soi` because the unit spans
   rib and strip.
5. gao2021a: the "+/-" wafer terms (0.0034, 0.0072, 0.00171 dB) entered as `statistic: std` (paragraph names standard
   deviation; Minitab statistics). If the auditor reads them otherwise, delete the three std rows. Si Sec. V values
   (0.0065 / 0.0027 / 0.012) at 1550 nm `wavelength_inferred` (r 3 value equals the 1550 nm wafer median).
6. schall2016: 0.33 nm/mW -> 330 pm/mW and 22 mW per FSR both `derived`; heater_gap_um 0.24 = cladding stack thickness
   (`derived` unit rescale); ring radius 9 um derived from "perimeter diameter of 18 um" (wording could mean outer
   diameter); Q unqualified -> q_loaded, O band inferred from the Fig. 1(d) span.
7. acoleyen2011b: family rows (D165) for the TE (f 16-22 um) and TM (f 9-15 um) measured sets; TM per-taper loss
   `derived` (per-taper share of a two-taper structure) with `approx` + range; simulated TE values on the fabricated
   R = 5 um row (D80e), TM R = 5 um simulation as a separate design row since the fabricated TM tapers use R = 6 um.
8. luyssaert2005: all rows `design`; 3-D row wavelength 1550 nm inferred, polarization left empty (not restated for the
   3-D runs); the printed 85 % kept over the Fig. 12 marker (~0.87, D417 note).

## Registry gaps

- schall2016 thermal breakdown power of a heater: 33 mW (p.5, "thermal breakdown power threshold of the device").
  Proposed `heater_breakdown_power_mw` (phase_shifter; electrical heater power at which the heater fails, as stated).
- schall2016 tuning figure of merit (power per FSR x mean of rise / fall time): 73 nWs (p.6 Table 1). Proposed
  `tuning_fom_nws` (phase_shifter; definition in condition). Low priority (single paper-specific definition).
- Spline / Euler coverage angle of a bend (bogaerts2011 alpha 0-45 deg; kept in label and condition). No new parameter
  proposed; noted for the bend layout template if it gains a transition-shape field.
