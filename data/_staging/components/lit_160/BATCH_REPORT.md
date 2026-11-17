# lit_160 batch report

Papers: lit:siddharth2024, lit:wei2023, lit:tang2021, lit:aflatouni2015. Distilled 2026-11-16 (verified_on 2026-11-16).
Validation: `merge_component_staging.py data/_staging/components/lit_160 --dry-run` -> +29 components, +126 metrics,
0 errors, no warnings on batch rows.

| paper | components | metric rows |
|---|---|---|
| siddharth2024 | 15 | 64 |
| wei2023 | 6 | 27 |
| tang2021 | 5 | 24 |
| aflatouni2015 | 3 | 11 |
| total | 29 | 126 |

Cached-copy identity (page-1 title check): siddharth2024 is arXiv 2306.03184v2, preprint title "Hertz-linewidth and
frequency-agile photonic integrated extended-DBR lasers" (17 pages incl. Supplementary Information), of the listed
Optica paper "Piezoelectrically tunable, narrow linewidth photonic integrated extended-DBR lasers"; every row
distills what the preprint reports and says so in its component notes (D430 / D433). wei2023 (arXiv 2207.07914v1)
and tang2021 (arXiv 2104.07309v1) are preprints with the journal titles; aflatouni2015 is the Optics Express PDF.
No correction / erratum, no other paper.

## siddharth2024 (15 components, 64 metrics)

Rows: 8 mm piezo E-DBR laser without kappa assignment (`edbr_8mm_piezo`: threshold, 25 mW fiber power, SMSR,
1549.5 nm, current tuning, three piezo chirp ranges); three per-kappa 8 mm E-DBR lasers (intrinsic linewidth only);
three 8 mm post Bragg gratings (figure-read peak reflectivity, simulated kappa, geometry); 6.5 mm kappa 0.6 grating;
800 MHz spiral resonator (kappa_0, kappa_ex, Q_L, 2.5 dB/m, all author_estimate per D403); SIL laser (3.8 Hz,
10.5 / 15 mW, SMSR, RIN, figure-read wavelength, 20 mm2 footprint); heater-tuned E-DBR laser (0.5 nm at 446.3 mW);
RSOA horn-taper butt coupler (simulated > 80 % overlap, 1 dB); lensed-fiber inverse taper (1 dB, author_estimate);
200 nm Si3N4 OFDR waveguide; AlN piezo actuator (400 kHz / 17 MHz chip modes).

Not entered and why:
- Mode hops at 110 / 200 / 240 / 278 / 320 mA (no parameter); chirp RMS nonlinearity 0.33 / 0.55 / 1.09 % and
  abstract < 0.4 % (no parameter, registry gap 2).
- Table S1 (p.13) "this work" row (> 25 mW, 1.5 x 10^3 Hz, > 0.5 nm / < 1.5 GHz, < 0.01 / 10 MHz): summary table,
  the 1.5 kHz linewidth conflicts with 2.5 / 3.45 kHz in the text; noted only.
- 10 GHz FWHM reflection bandwidth of the 6.5 mm grating (p.6) and the "15 GHz width of the grating" (p.4): no GHz
  bandwidth parameter on reflector and no printed grating wavelength for a conversion (registry gap 1). The 15 GHz
  is used only as the laser current-tuning range (converted at the printed 1549.5 nm).
- SIL frequency-noise floor < 1.5 Hz2/Hz and the > 20 dB noise reduction (no parameter, gap 3); the unlocked 60 dB
  SMSR in the SIL sentence (p.6) belongs to the Fig. 2(f) 8 mm chip, not the SIL chip.
- Histogram "Max: 17 MHz" label (meaning unclear); number of resonances in the histogram not stated.
- Post diameter 350 nm (no reflector parameter, gap 6); taper angle 12.4 / 12 deg (no parameter on chip_chip_coupler).
- Simulated metal-induced loss 0.1 dB/m (partial loss term) and bend-loss curves (Fig. S4); dispersion 2000 fs/mm.
- Fig. 1(b) piezo shift of the kappa 0.6 grating at +/-150 V (shift not printed; not read).
- Cited values (refs. [2], [32]: > 10 MHz actuation bandwidth, earlier lasers) not entered (rule 3).

Fab / facility: fab `org_epfl` (R.N.W., Z.Q. fabricated the device) plus `org_purdue_university` (A.A. fabricated
the integrated actuators, p.7) on the rows of the AlN piezo chip (8 mm lasers, 8 mm gratings, actuator); `org_epfl`
only on rows of chips with no actuator stated (SIL chip, spiral, 6.5 mm grating, heater laser, tapers, OFDR
waveguide). Facility `org_center_of_micronanotechnology` + `org_birck_nanotechnology_center` on all rows ("chip
samples were fabricated in the EPFL CMi, and in the Birck Nanotechnology Center at Purdue University", p.8;
liu2020a precedent). No missing org. RSOA vendor not stated (core_material note).

Judgment calls:
1. Kappa identity (D159 / D165): Sec. III, Fig. 2(d), (f) and the Fig. 3(f) piezo chirps are on an 8 mm piezo
   E-DBR laser whose grating kappa is never stated; the per-kappa intrinsic linewidths (3.45 / 3.45 / 2.5 kHz) are
   tied to gratings. I kept one kappa-unassigned row (chip D116_02_F9_C9) for the headline values plus three
   per-kappa sibling rows carrying only the linewidths. One sibling may be the same physical laser as the
   unassigned row. Alternative for the coordinator: fold the linewidths onto the unassigned row with kappa in the
   condition (fewer rows, breaks rule 9), or move the headline values to notes (strict D159, loses them).
2. OFDR loss unit conflict (D417): Supp. Sec. 5 text prints "1 dB/cm ... around 2 dB/cm", the Fig. S5(c) axis is
   dB/m and the main text gives 2.5 dB/m for the spiral. Entered 0.01 / 0.02 dB/cm (about 1 / 2 dB/m) as
   `extracted_from_figure` with the printed text in notes. Sample label also differs (C8 in text, C6 on the figure).
3. The heater-tuned laser is a separate row: p.5-6 say the first laser grating carries Ti/Pt heaters and a separate
   PIC was fabricated with AlN actuators for fast tuning. Its 8 mm length comes only from Table S1 (noted).
4. Intrinsic linewidths computed as pi x S0 are `derived` (explicit arithmetic, D80a), kHz values also by D256.
5. Hybrid RSOA / DFB + Si3N4 lasers use platform `other` (primiani2019, fan2020 precedent; rule 11: two guiding
   stacks); note that merged SIL rows of lihachev2022 / jin2021 use `sin`.
6. The spiral resonator is `resonator.other` (three Archimedean spirals with spline bends, not a ring / racetrack).
7. Fig. 4 caption letters are shifted by one against the panel letters (caption "(b)" = histogram panel d); locators
   use the panel letters, which match the text's figure references.
8. Fig. 2(b) gratings peak at about 1546.4-1546.5 nm while the 8 mm laser lases at 1549.5 nm, so the measured
   gratings may not be the lasing devices; reflectivity rows carry the plot-axis wavelength (`wavelength_inferred`).

## wei2023 (6 components, 27 metrics)

Rows: WG-coupled embedded QD laser with FIB facet (65 mA, 6.8 mW, 0.025 W/A, T0 108.1 / 33.7 K, ridge / length /
etch); same with wet-etched facet (92 mA, 5.3 mW); double-cleaved reference laser (about 50 mA, 37 mW, 0.148 W/A,
T0 282.4 / 51 K); laser-to-Si-waveguide monolithic interface (`waveguide_platform.transition`, skandalos2026
precedent: 7.35 dB author_estimate, simulated 76 % overlap); fork edge coupler test structure (simulated 85 % to
SMF, MFD 10 um specification, geometry); HR facet coating (95 % measured, 8 pairs).

Not entered and why: maximum CW lasing temperature 85 C (integrated) / 95 C (reference) (no parameter, gap 4);
lasing wavelengths (Fig. 5(e), (f) are 3D perspective plots, no printed value; D156); laser-waveguide offset
+/-250 nm / < 500 nm (no parameter); fork tip gap 3.4 um (gap_nm not allowed on fiber_chip_coupler, gap 5);
cladding thickness (3.5 um on p.3 vs 3 um in Methods p.12, conflicting, kept in the cladding text only); material
metrics (TDD 2.6e7 cm-2, RMS 0.8 nm, PL FWHM 33 nm at 1293 nm, dot density) are not component metrics; measured
edge-coupler results are not printed (refs. 41, 42 cited, rule 3).

Fab / facility: author contributions (p.14): Y. Bo (Institute of Physics CAS) fabricated the integrated laser,
A. He (Shanghai Jiao Tong University) designed and fabricated the SOI template, W. Q. Wei / D. Han (IOP CAS) grew
the III-V, M. Ming (IOP CAS) did the FIB polishing -> fab `org_institute_of_physics_chinese_academy_of_sciences` +
`org_shanghai_jiao_tong_university` on laser and interface rows (D395 / D439); fork coupler SJTU only; HR coating
IOP only (borderline: the coating sentence is passive, it is part of the laser process credited to Y. Bo). No
facility named. No missing org.

Judgment calls:
1. 7.35 dB coupling loss is `author_estimate`: "estimated", method not described; it equals 10 log10(6.8 / 37),
   the maximum powers of the WG-coupled laser (210 mA) and of the separate reference laser (250 mA), so it rests on
   another device as reference. Stored positive (printed -7.35 dB).
2. Wet-etched facet laser is a separate row: the paper does not say whether the inset compares one device before and
   after FIB polishing.
3. HR coating as `reflector.other` with platform empty (a facet coating, not a guiding stack).
4. Fork coupler platform `soi_strip` (fully etched 220 nm, p.3), row_kind fabricated with only simulated values (D80e).

## tang2021 (5 components, 24 metrics)

Rows: SIL laser (49.86 Hz intrinsic, 2.57 kHz integral, 0 dBm fiber, SMSR 50 dB, 1548.6 nm, static tuning
0.297 nm, dynamic FMCW ranges at 100 Hz / 500 Hz / 1 kHz converted from 10.25 / 8.63 / 5.56 GHz); free-running
commercial DFB (102.16 kHz intrinsic, 69.98 kHz integral, 10 dBm author_estimate); Si3N4 add-drop MRR (FSR 0.40 nm,
310 MHz FWHM, Q 6.19e5 derived, figure-read notch about 13.5 dB, geometry); DFB-SSC butt coupling (< 2.5 dB,
author_estimate); chip-to-SMF output path (1 dB loss-budget term, author_estimate).

Not entered and why: chirp linearity 1 - R^2, residual RMS frequency, chirp rates (Table 1), TBWP 5.1e7, ranging
results (system level, no parameter; gap 2); bus-to-ring 3 dB and add-port 3 dB loss-budget items (no fitting
component parameter); DFB cold-cavity FWHM 50 GHz (cited, ref. [10]); drop-port reflection spectrum (calculated);
heater voltages of Fig. 5 (no printed values); frequency-noise levels S0 (gap 3).

Fab / facility: empty. The Si3N4 platform is "used as our previous work [19]" and fabrication is passive
(p.4-5, D80b); DFB commercial, vendor not stated. No facility named. No missing org.

Judgment calls:
1. Static tuning range entered as 0.297 nm from the printed endpoints 1548.631-1548.928 nm; the paper calls it
   "equivalent to 42 GHz", which is about 0.336 nm (0.297 nm is about 37 GHz). Conflict in notes (D417).
2. Free-running power 10 dBm `author_estimate` with ref_plane unspecified (measurement not described).
3. Q 6.19e5 `derived` ("calculated" from the 310 MHz FWHM), entered as q_loaded (unqualified Q).

## aflatouni2015 (3 components, 11 metrics)

Rows: grating-coupler pixel array of the 4x4 OPA (about 40 % coupling efficiency, author_estimate; pitch 50 um;
16 elements); forward-biased p-i-n phase shifter (> 200 MHz bandwidth from the 0.7 ns carrier lifetime,
author_estimate; mean excess attenuation about 2.8 dB at I_pi read off Fig. 4(c); figure-labelled 500 nm rib /
90 nm slab; 220 nm Si); 500 x 220 nm Si waveguide (about 1.8 dB/cm average, author_estimate).

Not entered and why: OPA-level row (only geometry: < 1 mm2 area, 50 um pitch; steering shown without angles,
D49 performance rule; pitch and element count placed on the pixel row); I_pi about 10 mA (no drive-current
parameter, gap 7); phase-to-amplitude coupling factor 1/(8 pi) rad^-1 (no parameter); input grating coupler and
Y-junction tree (no values); 3 mW DFB source (setup equipment, rule 13); Fig. 2 array-factor simulations.

Fab / facility: fab `org_astar_ime` ("fabricated in IME silicon-on-insulator technology node", p.9),
`process_name` "IME silicon-on-insulator technology node". Missing org: "OpSIS foundry" (p.11 acknowledgments: "We
thank OpSIS foundry for the fabrication of the chips"), fab role (MPW access next to IME, D398 / D439 / D458); not
in organizations.csv or org_aliases.csv. No facility.

Judgment calls: p-i-n phase shifter kept as `phase_shifter.other` (lu2016a precedent; not in the EO atlas);
platform `soi_rib` from the Fig. 4(a) strip-loaded cross-section with 90 nm slab; the routing waveguide stays
`soi` (etch not stated, D422); 40 % pixel efficiency `author_estimate` (design vs measurement not stated).

## Missing organizations

| name as printed | paper | locator | role |
|---|---|---|---|
| OpSIS foundry | lit:aflatouni2015 | p.11 Acknowledgments | fab (MPW access, next to org_astar_ime) |

## Registry gaps (skipped value, locator, proposed definition)

1. `bw_fwhm_ghz` (or `bw_3db_ghz`) on reflector: siddharth2024 6.5 mm grating 10 GHz FWHM (p.6), 8 mm grating
   15 GHz width (p.4). Definition: reflection-band full width in frequency as the source states it.
2. `chirp_nonlinearity_pct` / `chirp_rms_nonlinearity_mhz` on laser (D431 candidate): siddharth2024 0.33 / 0.55 /
   1.09 % and 3.04 / 5.57 / 7.94 MHz at 10 / 100 / 500 kHz (p.4 Fig. 3(f)); tang2021 residual RMS 0.21-1.19 MHz
   (p.9 Table 1). Definition: RMS deviation of the measured chirp from an ideal linear ramp (chirp rate, excursion
   and predistortion in condition).
3. `frequency_noise_hz2_per_hz` on laser (D431 candidate): siddharth2024 white floor < 1.5 Hz2/Hz (p.6); tang2021
   S0 15.87 / 32520 Hz2/Hz (p.6). Definition: single-sided white frequency-noise level S0.
4. `max_operating_temperature_k` on laser (D431 candidate): wei2023 CW lasing up to 85 C (WG-coupled) / 95 C
   (reference) (p.8). Definition: highest heat-sink temperature with CW lasing as stated.
5. `gap_nm` on fiber_chip_coupler: wei2023 fork tip gap 3.4 um (p.3). Definition: gap between the tips of a
   multi-tip edge coupler.
6. `hole_diameter_nm` widened to reflector (D431 candidate): siddharth2024 post diameter 350 nm (p.2).
7. `i_pi_ma` on phase_shifter (D439 candidate): aflatouni2015 I_pi about 10 mA (p.6). Definition: drive current for
   a pi phase shift of a current-driven (carrier-injection) phase shifter.
