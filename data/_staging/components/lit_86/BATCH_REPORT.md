# Batch report: lit_86 (laser, chip_chip_coupler, micro_optics, free_space_emitter)

Date: 2026-11-06. Result: 20 components, 133 metric rows; `merge_component_staging.py --dry-run`: 0 errors (the one
warning printed is on merged ni2025b, not this batch). Page-1 titles of all six cached texts match their source rows;
no correction / erratum. franken2025 is the arXiv v2 text (2024-07-05) of the registered APL Photonics article (same
title and authors; D430 / D433 precedent); yang2018 is the journal text (Nanophotonics 2019; 8(3)), registry year 2018.

| paper | components | metric rows |
|---|---|---|
| romerogarcia2014 | 4 (2 fabricated, 2 design) | 38 |
| mehta2017 | 1 | 13 |
| franken2025 | 6 | 16 |
| heim2026 | 6 | 45 |
| sawamura2023 | 1 | 9 |
| yang2018 | 2 | 12 |

## romerogarcia2014

Rows: type I (2 tips) and type II (5 tips) multimode SOI edge couplers for FP laser diodes (`chip_chip_coupler.butt`,
platform `soi`), plus two simulated design rows (type I with L = 16 um; type II higher-bandwidth variant with 30 um
central taper). Laser-diode values at 1537 nm (Table I), lensed-fiber values at 1550 nm, design values simulated.
Fab `org_imec` ("fabricated within the ePIXfab Network in the 200 mm wafer IMEC CMOS pilot line", p.6 Sec. III-A).

Not entered:
- Simulated vertical tolerance +/-0.5 um and +/-0.6 um single-mode reference (p.3, p.4): generic statements, not a device row.
- Full-to-shallow etch transition 0.8 dB (p.5, design section, origin not stated) and taper / Y-junction losses below 0.1 dB: notes.
- Type II improved design "0.2 dB of additional loss" (relative value): notes.
- Lp/2 22.8 um simulated, about 23.5 um measured half beat length; Lp 54.2 um, 4.65 um: notes / not entered (no parameter).
- The FP laser's own 2.04 dBm, 1537 nm, 27 dB side-lobe suppression: measurement equipment (rule 13).

## mehta2017

Row: Si3N4 focusing grating emitter at 674 nm (`free_space_emitter.grating_emitter`, `sin`). Fab `org_mit` from the
author contributions (K.K.M. designed, fabricated and characterized; D395). MIT Nanostructures Lab staff thanked: not a
facility entry (rule 12).

Not entered:
- Focal heights of the minimum waists about 54 um (y) and 40 um (x) (p.4): no focal-height parameter.
- Polarization impurity < 3e-4 relative intensity (p.5), sidelobe levels (below 1e-3 beyond 10 um along y; characterized to 5e-6): no parameter on `free_space_emitter`.
- Simulated 36 % efficiency without the Si reflector (p.2): a design variant without a row.
- Design period (about 300-334 nm) and etched-fraction duty cycle (about 0.1-0.42) along y: read only from design curves (Fig. 2(e)-(f)), not labels; not entered.
- y-axis waist "corresponds also to w = 2.0 um after accounting for propagation": the 2.3 um fit is entered, the conversion is in notes.

## franken2025

Rows: dual-gain InP / TFLN Vernier ECL (`laser.tunable`, platform `other`), InP-to-TFLN PWB
(`chip_chip_coupler.photonic_wire_bond`, `polymer`), TFLN-to-fiber PWB (`fiber_chip_coupler.photonic_wire_bond`,
`polymer`), Vernier rings (`resonator.ring`, D400), TFLN waveguide (`waveguide_platform.straight`), thermo-optic phase
shifter on an MZI test structure. TFLN rows: platform empty (film thickness and etch not stated; D422 / D423).
Facility `org_center_for_nanoscale_systems` on the TFLN rows and the laser ("Lithium niobate fabrication was performed
in the Center for Nanoscale Systems", p.8). Fab empty everywhere: unnamed InP foundry, no named TFLN fabricator, no
named PWB writer (D80b, D450).

Not entered:
- 1 W PWB power handling (p.7): bond not identified (D159); `power_handling_dbm` also not registered on `chip_chip_coupler`.
- 58 h mode-hop-free operation, 4.4 MHz/h drift, < +/-0.2 mW power variation, 24 cm effective cavity length, calculated 100 Hz intrinsic linewidth: no parameter / not a measurement.
- 21.3 mW and 2.6 mW on-chip powers: operating points of the linewidth and long-term measurements, kept in condition.
- Q changes from cladding and aging (20 %, 15 %, > 50 %): relative, notes.
- Commercial bulk laser benchmark (p.2): not this device.

## heim2026

Rows: stabilized Vernier ECTL (`laser.tunable`, `other`), its intracavity Vernier rings (`resonator.ring`), 4 m coil
resonator of the coil-loaded MZI (`resonator.other`, heim2025 precedent), SBS laser (`laser.other`), SBS ring
(`resonator.ring`, D396 cross-note), Stokes / pump add-drop filter ring (`wdm.mrr`). Fab empty ("fabricated in a CMOS
foundry", p.9, unnamed).

Not entered:
- ECTL self-isolation over -30 dB: cited to ref. 52 (heim2025), rule 3.
- ADEV values, frequency drift (225 kHz/s, 5 kHz/s), lock bandwidths, error-signal slopes, frequency-noise suppression orders, SBS self-isolation 25 dB, 23 dB back-reflected pump suppression, feedback-resilience range: no parameters (notes).
- p.7 platform loss "< 1 dB/m at 1550 nm": same platform as the SBS ring 0.8 dB/m; no separate waveguide row.
- 80/20 splitter, Sagnac loop mirror, tunable MZI, RSOA butt coupling: no measured value, no rows (geometry of the 18 um / 13.1 deg facet in the ECTL notes).
- 21 x 26 mm chip footprint: chip level, not a component.

## sawamura2023

Row: 8-channel CWDM TOSA (`laser.els_module`, platform empty: laser material not stated). Fab
`org_furukawa_electric` ("We designed and fabricated", p.3, all authors at Furukawa Electric; D399).

Not entered:
- Introduction values of the authors' earlier TOSA / QSFP ELS (ref. [4]: > 20 dBm 25-55 C, 0.7 C case-to-housing): rule 3 / D259. The same > 20 dBm claim for this TOSA is covered by the Sec. 3 measurements entered.
- PMF rotational angle error target +/-3 deg, PMF bend radius 7.5 mm (>= 6 mm required), pigtail length 95 mm, TOSA height 4.0 mm: no parameter (core_material / notes).
- dBm duplicates of the mW powers.

## yang2018

Rows: two Au geometric-phase metalenses on an LMA-25 photonic crystal fiber facet, NA 0.37 and NA 0.23
(`micro_optics.metalens`, platform `other`). D411: a FIB-patterned metasurface on a fiber facet is a fiber-coupled
passive part (lit_79 gissibl2016 fiber-tip lenses precedent), in scope. Fab empty (first-person process, authors at
Baylor, Academia Sinica and Caltech, fabricator not named). Baylor CMI thanked for microscopy support: not entered.

Not entered:
- Focal lengths (measured 26.7-28.0 / 40.0-41.3 um, simulated 28.5 / 40.0-41.0 um, design 30 / 50 um): no focal-length parameter.
- Maximum operating efficiencies 16.1 % (1530 nm) and 16.4 % (1540 nm): "respectively" follows the text order NA 0.37 / 0.23, but Fig. 5(b) readings do not confirm that order (the NA 0.37 curve appears higher near 1510 nm); D159, values in notes.
- Enhanced optical intensity 234 % at 1540 nm: lens not named in the text, no parameter.
- Optimized unit cell simulated 1482.6 nm / 17 % (design before fabrication) and the Si-nanoantenna 91 % proposal (supplement): notes / not entered.
- Supplement (Table S1 fabricated dimensions, S2-S6) not cached.

## Missing organizations

- ePIXfab (romerogarcia2014, p.6 Sec. III-A, MPW access next to the IMEC pilot line; D398 would make it a fab org on the 2 fabricated rows). Already queued for the org round (D422).
- None else needed by a row (Freedom Photonics, HyperLight, Baylor CMI appear in the texts without a fab / facility role).

## Judgment calls (for the audit)

1. romerogarcia2014: one row per coupler type although the chip carries a series of interference-section lengths; the length of each measured device is in the metric condition when printed (62.7 um, 60.7 um), and the Table I laser-diode values sit on the type row ("best structure in terms of imbalance", length not stated). Alternative: split per length and drop the laser-diode values under D159.
2. romerogarcia2014 vertical 1 dB tolerances (+/-0.35, +/-0.5 um) stored in `tol_1db_lateral_um` with "vertical (y)" in condition (merged tanaka2012 precedent); `tol_1db_vertical_um` is an open registry candidate.
3. romerogarcia2014 type II lensed-fiber value printed as "total coupling efficiency of -2.8 dB" stored as excess `insertion_loss_db` 2.8, because p.9 compares it with the 3.1 dB excess loss. Laser-diode and lensed-fiber IL rows measured + reference_structure (GC loops subtracted, no arithmetic printed; D167).
4. romerogarcia2014 type I back-reflection taken from the abstract / conclusion ("both devices"), band C-band inferred; data shown only for type II.
5. franken2025 78 mW on-chip power kept `measured` (printed as on-chip; the referencing method is not described). Alternative: author_estimate as for de-embedded powers without a printed term.
6. franken2025 PWB losses with `wavelength_nm` 1530 inferred from the laser operation; ring heater 150 mW/pi stored as `tuning_power_mw` with "per pi" in condition (`p_pi_mw` is not allowed on `resonator`).
7. heim2026 ECTL ring loaded Q 1.65 M entered as this paper's value although the sentence ends with ref. 52 (the citation reads as covering the self-isolation; heim2025 prints 0.65 M).
8. heim2026 Stokes filter ring as `wdm.mrr` (extracavity drop filter); alternative `resonator.ring`. SBS ring q_intrinsic and 0.8 dB/m `author_estimate` (D403: over-coupling is a design statement).
9. heim2026 fundamental linewidth range 1.65-10.48 Hz: the supplement measures it free-running, the main text quotes it for the stabilized ECTL; one row, condition says so.
10. sawamura2023 "lowest 143 mW" and "110 mW and higher" stored with qualifier `ge`; the 300 / 400 mA operating points stored as 100 mW rows; 110 mW vs conclusion 20.3 dBm conflict kept in notes (D417).
11. mehta2017 locators follow the figure's own panel labels (Fig. 1(a) top view, 1(b) cross-section); the caption letters the panels differently. Design angle -30 deg entered as author_estimate.
12. yang2018 unit-cell simulated resonance and conversion efficiency entered (`center_wavelength_nm`, `coupling_efficiency_pct` scope per_component) with "unit cell, not lens efficiency" in condition; `lens_radius_um` 12.5 derived from the core diameter as the aperture.

## Registry gaps (skipped value + locator; proposed definition)

- `focal_length_um` (micro_optics, free_space_emitter): yang2018 28.0 / 40.0 um at 1550 nm (p.5, Fig. 5(a)); mehta2017 focus heights 54 / 40 um (p.4). Definition: distance from the optic (or emitting plane) to the measured focus, axis in condition. Also proposed by D432 / D443.
- `tol_1db_vertical_um` (chip_chip_coupler, fiber_chip_coupler): romerogarcia2014 +/-0.35 / +/-0.5 um (p.9 Table I); currently stored per precedent in the lateral parameter.
- `frequency_drift_hz_per_s` (laser): franken2025 4.4 MHz/h (p.7), heim2026 225 kHz/s and 5 kHz/s (p.7). Definition: linear drift rate of the optical frequency over the stated window.
- `allan_deviation` (laser, dimensionless, tau in condition): heim2026 6.5e-13 at 0.08 ms, 2.8e-13 at 5.12 ms (p.7).
- `polarization_purity` or `per_db` on free_space_emitter: mehta2017 < 3e-4 relative intensity (p.5).
- `self_isolation_db` / optical feedback tolerance on laser: heim2026 SBS 25 dB (p.5).
- `power_handling_dbm` on chip_chip_coupler (D437 candidate): franken2025 1 W, but the bond is not identified here.
