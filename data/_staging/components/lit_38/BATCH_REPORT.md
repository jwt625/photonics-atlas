# Batch lit_38 report (distill subagent, 2026-10-29)

Dry-run `batch lit_38: +29 components, +183 metrics; errors 0` (one WARN from another batch, ni2025b m18 / m4). ASCII, no
e-mail, no quotes (all five sources restricted_local_only). Page-1 title / authors match the source rows for all five
papers; no garbled text layers.

## Per paper (components / metrics)

- leonsaval2014 (1 / 8): 3x1 mode-selective photonic lantern (mode_converter.mdm_mux, platform other, huang2018 precedent).
  Lantern loss < 0.3 dB typical per_component (cutback); 2 dB mean device_total into GI FMF via a 3.7x telescope
  (wavelength inferred 1550); mode selectivity 3 dB (LP01 launch) / 6.5 dB (LP11 launch) as extinction_db, plus
  >= 5.5 dB from the near-field valley depth (author_estimate); transition 21.5 mm (derived). Not entered: MDL < 0.5 dB
  (mdl_db not allowed for mode_converter), abstract / conclusion selectivity summaries, conventional lantern (images only),
  6-fiber lantern (simulation without numbers). Fab org_the_university_of_sydney (acknowledgment places manufacture of all
  devices in the Astrophotonics facilities of the University of Sydney; facility not entered: group lab, not shared).
- yang2014 (6 / 66): ADC three-mode MUX (mode_converter.mdm_mux: per-input transmissions device_total -19 / -28 / -28 dB,
  3-dB bandwidth > 16 nm, design and SEM widths, tapers, stack); three DeMUX racetrack drop rings as wdm.mrr (D2-type
  rows per coupler design: linewidth 0.50 / 0.40 / 0.39 nm derived to pm, drop loss 1 dB derived by the authors,
  R / Lc / bus width / gap / heater); MDM-WDM circuit row (six modal crosstalks 10-31 dB, circuit transmissions -20 /
  -29 / -29 dB device_total, ~2 mm); 1 um SiN waveguide 2 dB/cm cutback (wavelength inferred). Not entered: collective
  Q 3000-4000, TM Q ~700 and 30 pm/mW tuning efficiency (not tied to one ring, D159 / D254), field coupling coefficients
  (no parameter; Table 4 field values not power_coupling_pct), simulated bend losses (radius not stated), eye ER (link).
  Fab / facility empty (see orgs).
- ashida2018 (1 / 16): array-level PhC double-heterostructure nanocavity row (resonator.photonic_crystal, D165): D5_4
  q_loaded 2.50e6 + 0.63 pm; q_intrinsic (paper's Qexp, T0 = 1.0 from measured transmittance, derived) best 2.50e6, mean
  1.89e6 (n 30), range 1.14-2.50e6, mean 1.97e6 (n 27 without A8); simulated Qideal 3.31e7 and 1577.0 nm; mean wavelength
  1574.5 nm, wavelength spread std 2.47 nm / chip-average max 8.0 nm / within-chip < 2 nm; geometry. Fab org_national_
  institute_of_advanced_industrial_science_and_technology (lithography and etching performed at the AIST R&D lab).
  Fig. 3 caption D4_4 vs text / Table I D5_4: D5_4 used.
- takata2023 (8 / 34): H1 hexapole PhC nanocavities, fab org_ntt (authors state they fabricated; all at NTT, one also
  Tokyo Tech). Rows: measured series a = 434 nm (8 of 26 > 1e6 loaded, duplicate-pair wavelength std 0.848 nm measured,
  0.600 nm derived); best sample s1 = 96.5 nm (Q_L 1.2e6, 160.4 MHz, set-1 duplicate 3.0e5, Qi 1.5e6 author_estimate
  from simulated Q_WG, simulated Q_WG 6.6e6 as q_external, Q_th,L 5.9e6, Q_th 5.9e7); Fig. 4(c) sample s1 = 99.5 nm (1.1e6,
  173.8 MHz, 1575.370 nm); four design rows (Qth 1.41e8 manual, 3.1e8 / 4.5e8 Nelder-Mead s2 = 23 / 26 nm, 2.0e6 reference
  design re-simulated here); 8 um slab-waveguide facet ~10 dB typical per_facet (fiber_chip_coupler.edge).
- shang2017 (13 / 59): asymmetric 50 / 150 nm Si3N4 vertical coupler (waveguide_platform.transition 0.185 dB measured
  cascade fit, < 0.1 dB simulated); 150 nm (0.4-0.6 dB/cm cutback) and 50 nm (3.5 dB/m -> 0.035 dB/cm OFDR, derived)
  waveguides; non-neighbouring-layer crossing (design: < 0.1 dB, crosstalk > 34.5 dB); vertical Y-junctions as
  splitter.other (gaps 600/600, 600/780, 600/860, 600/600 + 500 nm offset: split 1:1 / 3:2 converted to %; simulated
  excess 0.18 TE / 0.3 TM on 600/600); fabricated 1x3 symmetric (1:1:4 -> %, Port 1 / 3 imbalance 0.3 dB) and 2 um offset
  (imbalance 1.0 dB); design rows 1x3 (two top ports, 0.03 / 0.08 dB), 1x4 (0.16 / 0.21 dB), 1x3 1:1:1. Fab
  org_university_of_california_davis; facilities org_marvell_nanofabrication_laboratory, org_center_for_nano_micro_
  manufacturing. Not entered: 0.230 dB / < 0.25 dB Y-junction excess loss (family value, design not named), per-port 1x3
  transmissions as IL (D401 analogue), 1:22:27 ratio (device not named), CMP / thickness figures (cited [18]).

## Missing orgs (name as printed + locator)

- "Nanoelectronics Fabrication Facilities (NFF) of HKUST" (yang2014 p.12 Acknowledgments, support in device
  fabrication): not in the registry; the registry's org_nanosystem_fabrication_facility (HKUST NFF) is not mapped by name
  (rename rule). Coordinator: decide whether it is the same facility under its earlier name (would give facility on all
  six yang2014 rows; fab would then still be empty or borderline HKUST, authors split HKUST / CAS IoS).
- "Astrophotonics facilities at the University of Sydney" (leonsaval2014 p.9): group lab, not proposed as a facility.

## Judgment calls

- yang2014 rings as wdm.mrr (channel drop filters of a WDM-compatible mode DeMUX, skill rule 10), one row per coupler
  design (c1); MUX and whole circuit as mode_converter.mdm_mux; MUX / circuit transmissions kept device_total (lensed fiber
  in, objective out), no de-embedding arithmetic (the paper's own lossless-coupler kappa extraction conflicts with I1 = bus).
- ashida2018 Qexp entered as q_intrinsic derived (T0 measured ~1, coupling regime from data, D403 "derived" branch).
- takata2023 wavelengths for the best sample read from the Fig. 5(b) inset frequency axis / Fig. 5(a) (inferred);
  design-row wavelengths inferred 1550 (telecom target ~1.55 um). Text vs Fig. 3 lattice constant (426 vs 435 nm) noted.
- shang2017 vertical Y-junction as splitter.other (vertical inverse-taper splitter; y_branch template would draw a planar
  Y); 2-um-offset 1x3 port labels conflict between text and Fig. 11: imbalance only.
- leonsaval2014 fab = University of Sydney (named place of manufacture, D83c-style), not a facility.

## Registry gaps

- gap_nm for mode_converter: yang2014 ADC MUX gaps 500 / 450 / 400 nm design, 490 / 430 / 340 nm SEM (p.5, p.8)
  (also zhou2022a precedent). Definition as for splitter.
- mdl_db for mode_converter: leonsaval2014 MDL < 0.5 dB (p.9); huang2018 precedent. Definition as for fiber_interface.
- tip_width_nm for splitter: shang2017 Y-junction inverse-taper tips 250 nm (p.5).
- hole_radius_nm (resonator, reflector; photonic-crystal hole radius, SEM or design): ashida2018 ~113 nm (p.2, Table II);
  takata2023 R1 ~106.8 / R0 ~133.1 nm SEM, design R0 131 / R1 102 nm (p.4, p.7).
- mode_volume_lambda_n3 (resonator, Purcell mode volume in (lambda/n)^3): takata2023 0.72 / 0.71 / 0.74 / 0.66 (p.5,
  p.10, p.13).
- back_reflection_db for crossing (already proposed in lit_11): shang2017 simulated < -33.5 dB (p.4 Fig. 3(c)).
- field_coupling_coefficient (mode_converter / wdm, field amplitude coupling as reported): yang2014 Table 1 / 2 / 4.
