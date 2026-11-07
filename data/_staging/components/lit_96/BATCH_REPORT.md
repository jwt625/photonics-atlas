# lit_96 batch report (2026-11-06)

All four cached texts match their source rows (page-1 title); none is a correction, erratum or another paper.
raghunathan2025 has a garbled text layer on p.10 only (supplementary derivation of the efficiency formula); every value
was taken from the clean pages 1-8. Dry-run: +15 components, +63 metrics, 0 errors (the one warning, ni2025b m18 / m4, is
an existing merged row, not this batch).

| paper | components | metrics |
|---|---|---|
| zhao2025 | 7 (waveguide_platform.straight 2; fiber_chip_coupler.edge 1; amplifier.parametric 1 fabricated + 2 design; frequency_converter.other 1) | 36 |
| nikolai2025 | 3 (frequency_converter.shg; waveguide_platform.straight; fiber_chip_coupler.edge) | 10 |
| raghunathan2025 | 1 (frequency_converter.other) | 5 |
| yan2025 | 4 (frequency_converter.other; amplifier.parametric; waveguide_platform.straight; fiber_chip_coupler.edge) | 12 |

## Preprint vs journal record (D430 / D433)

- nikolai2025: the source row is the arXiv v1 preprint itself (no DOI, no journal record); nothing to compare.
- raghunathan2025: arXiv v1 text; the source row carries the Optica Quantum DOI (10.1364/opticaq.563123). Same title as
  the journal record; journal version unread (no network). Accepted as the same work, as in D430 / D433.
- zhao2025 and yan2025 are the journal PDFs.

## Not entered, and why

zhao2025
- Fitted dispersion beta2 = -2.2 ps2/km, beta4 = 1.9 fs4/um at 1551 nm, design beta2 -4 ps2/km (p.4): no parameter (D81 / D250
  reject beta2). In OPA notes.
- TE10 cutoff below a 1150 um bend radius, TE10 / TM00 cutoff wavelengths 1100 / 1180 / 1820 nm (simulations, p.3, p.8): no
  parameter.
- Fig. 2(a) theoretical bandwidths 270 / 542 / 385 nm for a generic 1 m waveguide with assumed parameters: a parameter study,
  not a device; not entered.
- Conventional 2000 x 690 nm rectangular four-mode waveguide (Fig. 1(a), about 50 cm): only a qualitative fading statement
  (more than 10 dB), no row.
- Wavelength-conversion system results (10 Gbit/s NRZ, 32 GBd 16-QAM, more than 200 nm conversion span): system metrics /
  no conversion-span parameter on frequency_converter; in notes.
- Rib gap (15 / 50 um), slab width (12 / 30 um), spiral unit length, maximum bend radius 450 um (Extended Data Table 1): no
  parameter; in notes.
- Supplementary Information not cached (fabrication tolerance, bend-loss and fluorescence material).

nikolai2025
- Generated on-chip SH power 1.065 W, directly measured off-chip SH more than 0.5 W, about 0.6 W after mirror calibration
  (p.6): no output-power parameter on frequency_converter (registry gap, as zhao2025a in D462). Entered instead: derived
  off-chip ratio > 11.1 % (0.5 W / 4.5 W).
- Waveguide width: the chip carries 1.5 and 1.6 um waveguides; the width of the measured device is not stated (D159).
- Poling electrode geometry (25 um elliptical tips, axis ratio 1:15, duty cycle 40 %, 10 um gap, 1 kV pulse trains),
  coercive-field and poling cross-talk observations: process parameters, not component metrics.
- Pump wavelength shift 1549.3 -> 1553.0 nm with pump power, SH spectra wider than modelled (Fig. 4(d)): notes only.
- Fig. 1(g, h) comparison with a ridge PPLN (ref. [16]) and Fig. 4(e) simulated scaling: other work / simulations.

raghunathan2025
- Noise counts (55 kHz at the idler, 220 kHz inferred on chip, < 3 kHz with the pump imbalance; etalon -15 dB): no
  parameter for a noise count rate of a frequency converter (registry gap).
- Upper bound < 25 % on the achievable efficiency (assumes an undercoupled idler, p.3): speculative, in notes.
- Signal resonance inferred critically coupled, but Q_i is not printed and the sentence does not say which signal wavelength
  (1260 or 1283 nm): no q_intrinsic row.
- Waveguide 730 x 1300 nm: height / width not assigned in the text; in core_material only, no geometry rows.
- Ring radius, FSR, pulley-coupler dimensions: not printed. Photon-pair source ring: no metric.

yan2025
- OPG threshold about 1.1 pJ (figure label 1.14 pJ): no parameter for a threshold pulse energy (pump_threshold_mw is a CW
  power; registry gap, as pulse_energy_pj candidates in D429 / D433).
- Tunable MIR center wavelength 2.06-3.12 um (abstract 2.06-3.09 um) and MIR lines 3.59 / 3.93 / 4.31 / 4.6 um from other
  waveguides: no tuning-range / center-wavelength parameter on frequency_converter (D419 widening not yet in the registry);
  the other waveguides have no printed geometry or performance value, so no rows.
- Facet damage above 650 pJ pump energy: a pulse energy, not a power-handling value in dBm; in notes.
- Waveguide length and film thickness: in Supplementary Note 2 (not cached); not entered.
- Comparison values in Fig. 3(c) and Fig. 4(f): other works (rule 3).

## Missing fab / facility orgs

- Myfab Chalmers (zhao2025 p.7 acknowledgment: work performed in part at Myfab Chalmers): facility, parent
  org_chalmers_university_of_technology. Would go on all 5 fabricated zhao2025 rows. Also reported for merged ye2021.
- UNIL Cellular Imaging Facility (CIF), University of Lausanne (nikolai2025 p.7: two-photon imaging of the poled domains
  performed there): facility candidate only for domain inspection; not entered and probably not a fabrication facility
  under rule 12. Listed for the coordinator.
- All org ids used exist: org_chalmers_university_of_technology, org_epfl, org_center_of_micronanotechnology,
  org_epfl_institute_of_physics_cleanroom, org_cornell_nanoscale_facility.

## Judgment calls

1. zhao2025 net on-chip gain 1 dB: `author_estimate` + loss_breakdown, L band. The paper subtracts "about 1 dB" on-chip
   waveguide loss in the L band whose origin is not stated (the 2.5 dB/m OFDR minimum over 0.56 m would be 1.4 dB). The
   on-off gain itself is not printed, so its peak (about 2.3 dB near 1645 nm) is a figure read of Fig. 2(c).
   Alternative: `derived` (D166) if the coordinator treats the 1 dB as the authors' own measured loss.
2. zhao2025 one physical waveguide WG2 in three classes (waveguide_platform, amplifier.parametric, frequency_converter.other;
   D396); WG1 (another wafer and design, Extended Data Table 1) is its own waveguide row. On-chip conversion efficiency
   -3.4 dB stored as 45.7 % `derived` (ye2021 precedent). Two theoretical OPA designs (W 1600 / 1828 nm, 2 m, Fig. 4(b))
   entered as `row_kind design` with gain about 20 dB `simulated`; the wavelength span is the computed gain band read off
   the figure (`wavelength_inferred`). Alternative: drop the design rows.
3. zhao2025 etch depth 300 nm entered from the printed rib height H1 on the 500 nm slab of the 800 nm film
   (`design_target`); widths printed in um are `derived` (D157).
4. nikolai2025 107 %/W/cm2 `author_estimate`: the calibration assumes identical input and output facet losses and fits the SH
   coupling (li2025a / D462 precedent). The 4 dB per facet coupler value is the same assumption, also `author_estimate`.
   Power handling 36.53 dBm `gt` (4.5 W off-chip, no damage) on a separate waveguide_platform row (D396; riemensberger2022
   precedent). Platform ltoi_rib (x-cut LiTaO3, 200 nm slab). Poling period 4.308 um is the stated target (period of the
   high-power device not stated).
5. raghunathan2025 efficiencies (6 % at 1283 nm, 5 % at 1260 nm) `author_estimate`: the paper calls them on-chip but does not
   describe the coupling-loss correction (D460 precedent). Alternative: `measured` with ref_plane unspecified. Q at the pump
   resonance printed as 780 nm in the text, labelled 778 nm in Fig. 2(a): kept as 780 nm with the conflict in notes
   (D417). Fab empty (no fabrication statement), facility CNF ("performed in part at").
6. yan2025 fab empty: the fabricating author has two affiliations (NTU, Sichuan University) and no site is printed (D433).
   Platform lnoi_rib from the rib-with-slab schematic, mode plots and SEM of Fig. 1 (film thickness not printed); empty
   would also be defensible (D422 / D423). OPG and cascaded efficiencies on one frequency_converter row (same waveguide),
   parametric gain 127.1 dB/cm on an amplifier.parametric row (D396). Propagation losses "for the pump / signal light"
   stored at 1030 / 2060 nm with `wavelength_inferred` (CW test lasers were 980, 1550, 2100 nm; mapping not stated);
   insertion losses 8.46 / 9.42 dB scope `unspecified`. The lensed-fiber facet row carries only a simulated 10.8 %
   coupling efficiency (D80e keeps it `fabricated`).

## Registry gaps (skipped value + locator, proposed definition)

- `sh_output_power_mw` (or `output_power_mw` widened to frequency_converter): nikolai2025 1.065 W on chip, > 0.5 W off chip
  (p.6); yan2025 9.4 / 12.5 uW (p.2, p.4). Definition: generated output power at the converted wavelength, reference plane
  in ref_plane.
- `threshold_pulse_energy_pj` on frequency_converter / amplifier: yan2025 OPG threshold about 1.1 pJ (p.2, p.4).
- `tuning_range_nm` / `center_wavelength_nm` on frequency_converter (D419 widening): yan2025 2.06-3.12 um (p.2, p.4).
- `noise_count_rate_hz` on frequency_converter: raghunathan2025 < 3 kHz total idler noise (p.6), 220 kHz inferred on chip
  without suppression (p.5).
- `conversion_span_nm` (wavelength span over which conversion is demonstrated): zhao2025 more than 200 nm at 100 Gbit/s (p.5).
