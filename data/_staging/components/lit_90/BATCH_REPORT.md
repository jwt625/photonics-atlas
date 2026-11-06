# lit_90 batch report (2026-11-06)

All four cached texts match their source rows (page-1 title); no correction, erratum or wrong paper. su2017 is the arXiv version of the ACS Photonics source row (same title; journal version unread, D430 / D433). jung2026 is an arXiv preprint (source row is the arXiv record). Dry-run: +10 components, +87 metrics, 0 errors (the one warning, ni2025b m18 / m4, is an existing merged row, not this batch).

| paper | components | metrics |
|---|---|---|
| jung2026 | 5 (fiber_chip_coupler.other: 2; resonator.ring: 1; waveguide_platform.straight: 2) | 32 |
| watanabe2025 | 2 (fiber_interface.connector) | 15 |
| hsu2023 | 2 (wdm.mrr) | 17 |
| su2017 | 1 (wdm.other) | 23 |

## Not entered, and why

jung2026
- Table 1 rows [23], [30]-[39]: other works (rule 3).
- Rib coupler under 150 mW broadband white light: failed within one minute (p.7, Fig. 5(b) II); a failure, not a handling level. In component notes.
- Rib coupler at 750 nm about 2 dB below its peak (p.8): no wavelength-specific loss row; in notes.
- About 3 dB unpolarized vs polarized difference (p.5): not a PDL (unpolarized is not a polarization extreme); in notes. The unpolarized per-coupler levels at 1550 nm are entered as figure reads.
- Placement tolerance sub-200 nm (p.10), polymer indices (1.525, 1.59, 1.52-1.59), LiTaO3 index 2.12, overlap-integral simulations (Fig. 2(b), Fig. 3(b) inset): no parameter or illustrative.
- Mode-transfer taper length: only the simulation axis (0-80 um, Fig. 2(b)) and a scale in Fig. 3(a); not a labelled dimension. Expansion-taper length and TIR angle not printed.
- Fig. 4(d) per-width losses: kept as readings in the notes of the two regime rows, not as separate width rows (widths only readable off the axis).
- Ring FSR: not printed. Histogram statistics per width: supplement not cached.

watanabe2025
- Loss variation within +/- 0.2 dB in the temperature cycle (p.2, Fig. 5) and within +/- 0.03 dB over 50 matings without cleaning (p.3, Fig. 9): no parameter (il_drift / mating_repeatability candidates, see gaps).
- Misalignment for 0.2 dB extra loss about 6.5 um (design; about 1 um for SMF butt coupling, p.1): no 0.2-dB tolerance parameter; not converted to 1 dB.
- Magnetic force about 2.2 N (design), terminal height / width (2.5 / 8.4 mm): no parameter; in notes. Terminal length 5.7 mm entered as length_um.
- 260 C reflow compatibility: from the authors' ref. [5] (rule 3).

hsu2023
- Capacitance 540 fF at -4 V (p.2): `capacitance_ff` is not allowed on wdm / resonator; also calculated from the density of a separate MOS test capacitor (area not printed). In notes.
- VpiL 0.050 V cm (p.1-2): no parameter on wdm (vpi_l candidate D438 is phase_shifter only).
- Power consumption pW/nm to nW/nm (Fig. 2(d)), leakage current, capacitance density 10.48 fF/um2, optical field-effect mobility 40-70 cm2/V/s (another ring, Fig. 3), Hall mobility 44: no parameter.
- Earlier ITO / ITiO ring values (271 pm/V, Q 1000, Q 12000, 130 pm/V, p.2): authors' own earlier works (D259).
- Insertion loss of the filter: off-resonance level not 0 dB from imperfect normalization (p.3); not entered. Channel spacings: not printed, non-uniform at 0 V.
- Fig. 1(c), (d) simulated Q / tunability vs width and mobility: design-trend simulations of hypothetical widths, not entered.
- Grating couplers (10 deg tilt, p.6): no metrics, no row.

su2017
- 3-dB / 1-dB channel widths: not printed; not read off Fig. 3.
- Measured channel spacing (41 / 39 nm from 1471 / 1512 / 1551 nm): my arithmetic; in the spacing-row note only.
- Design constraints (40 nm minimum radius of curvature, 90 nm minimum hole width, 40 nm FDFD step), optimizer settings, runtime: no parameter; constraints in notes.

## Missing fab / facility orgs

- "Electron Microscopy Facility at Oregon State University" (hsu2023 p.7 Ack., thanked with MaSC for device fabrication): facility, parent org_oregon_state_university. Not in the registry; would go on both hsu2023 rows next to org_materials_synthesis_and_characterization_facility.
- All other orgs used exist: org_furukawa_electric, org_materials_synthesis_and_characterization_facility, org_stanford_nanofabrication_facility, org_stanford_nano_shared_facilities.

## Judgment calls

1. jung2026 coupler losses 0.9 / 1.25 dB: `loopback_half`, method loopback, basis `measured`. The paper measures backloops with two couplers, plots transmission per coupler and shows no halving (D452, lorenzen2026 precedent). Fiber-array and Fresnel losses are included (p.10); connectors and polarization controller are calibrated out; the backloop waveguide is not subtracted (in `includes`). Polarization TE (polarization controller, p.10); the peak wavelength is not printed, so the row carries the 1480-1620 nm sweep range.
2. jung2026 3-dB bandwidth: printed edges 850-1740 nm (abstract) and 850-1750 nm (p.8), and "beyond 900 nm" (p.8), while the measured range ends at 1730 nm. Entered as 900 nm `gt`, `author_estimate` (D435), with the conflict in notes. Alternative: drop the row.
3. jung2026 1 W handling: 30 dBm `gt` `derived` (unit conversion, he2019 precedent): the highest EDFA power, not a damage threshold. Strip coupler also gets a 150 mW broadband row (21.76 dBm, `gt`).
4. jung2026 ring: kappa_0 rows `measured` (fits; coupling regime from a gap sweep, p.6). The 0.08 / 0.24 dB/cm and the group indices are `author_estimate`: the group indices are printed but their origin (measured FSR or simulation) is not stated, so the losses rest on an input of unstated origin (rule 4). They reproduce from the printed inputs (43 MHz and n_g 1.958 give about 0.077 dB/cm). Alternative: `measured` for the losses (standard conversion with printed inputs). Ring statistics carry the laser sweep range with `wavelength_inferred` (resonance span not stated).
5. jung2026 0.11 and 0.06 dB/cm: regime rows (D165) as `waveguide_platform.straight`, `author_estimate` (D76: group indices for these widths not printed). The 0.06 value is printed "for the multimode waveguide" without a width; the Fig. 4(d) points at 3, 4 and 5 um all read about 0.06, so the row is the regime and not one width.
6. jung2026 platform: printed couplers `polymer` (yu2023 precedent for two-photon TIR reflectors); fully etched LTOI ring and waveguides `other` (no ltoi_strip enum; `ltoi_rib` would misstate the etch). Fab and facility empty: no fabrication sentence names an org; the Munster Center for Nanotechnology appears only as an affiliation.
7. jung2026 unpolarized coupler levels (about 3.3 / 4.3 dB at 1550 nm, Fig. 3(c)) added as `extracted_from_figure` rows with polarization `unpolarized`, so the 1-dB and 3-dB widths (unpolarized measurement) have a matching level.
8. watanabe2025: two connector rows, FA/FA (randomly mated, 300 channels) and PLC/FA (60 channels), because the mated terminals differ (fiber array vs PLC behind the lens array). Scope `per_interface` (sutherland2019 / merged connector precedent); method unspecified for FA/FA (reference not described), direct for PLC/FA (reference at the PLC-side terminal). Fig. 3 / 4 / 8 inset-table statistics (mean, min-max range, std) entered as printed. Fab org_furukawa_electric: the authors state they fabricate the connector, all at Furukawa Electric (D399). Platform empty (D422).
9. watanabe2025 return loss entered as `back_reflection_db` (positive dB below the input).
10. hsu2023: the Fig. 2 single ring gets its own `wdm.mrr` row. Fig. 5(b) calls it the individual ring of the WDM filters, so it is a channel filter (D400), but the paper does not say which channel; its 0 V resonance (about 1544.7 nm) and 1.5 nm shift at -4 V match ch1 of Fig. 4(c). Ring geometry (radii, height, slab) is on the filter row only; the single-ring row carries the 300 nm width the paper states for the design. Alternative: fold its values into the filter row as ch1 (would rest on an inference).
11. hsu2023 Q 5200: unqualified, `q_loaded` with a note; wavelength read off Fig. 2(a) (`wavelength_inferred`). Polarization not stated (`unspecified`). The -4 V Q (about 2300) and the 0 V extinction (about 21.5 dB) are figure reads.
12. hsu2023 tuning range 5 nm `derived` from the printed 1543-1548 nm coverage; FSR 11 nm `measured` (printed). Fab empty (no fabricator named); facility MaSC (in the registry) plus the missing OSU Electron Microscopy Facility.
13. su2017: measured losses scope `de_embedded` with method reference_structure (normalized to an adjacent waveguide; piggott2015 precedent, same group and process). Simulated FDTD transmissions are `device_total` / simulated. Ports from the Fig. 3 curves (S21 1471 / 1500 nm, S41 1512 / 1540 nm, S31 1551 / 1580 nm). Crosstalk in `crosstalk_db` (type not stated). Platform `soi` (piggott2015 precedent; the I/O waveguides are 500 nm strips). Fab empty: "fabricated at SNF and SNSF" names facilities, not a fabricator (D80b); facilities are the pre-merger names (D80d).

## Registry gaps (skipped value, locator, proposed definition)

- Platform enum `ltoi_strip` (fully etched thin-film lithium tantalate, analogue of lnoi_strip): jung2026 ring and waveguide rows (p.3, p.6), now `other`.
- `capacitance_ff` widened to wdm / resonator: hsu2023 540 fF at -4 V (p.2). Device capacitance of a gate-tuned ring.
- `vpi_l_v_cm` (D438 candidate) widened to wdm / resonator: hsu2023 0.050 V cm (p.1-2).
- `tuning_power_per_nm_w` (or a power_consumption parameter on wdm): hsu2023 pW/nm to nW/nm (p.2, Fig. 2(d)). Electrical power per nm of resonance shift.
- `il_drift_db` (lit_82 candidate) on fiber_interface: watanabe2025 +/- 0.2 dB over -10 to 60 C, 5 cycles (p.2, Fig. 5). Peak loss change under the stated stress.
- `mating_repeatability_db` (D441 candidate): watanabe2025 +/- 0.03 dB over 50 matings without cleaning (p.3, Fig. 9).
- `tol_0p2db_lateral_um` or a tolerance parameter with the level in condition: watanabe2025 about 6.5 um for 0.2 dB (design, p.1).
- `mating_force_n` on fiber_interface: watanabe2025 about 2.2 N (design, p.1). Lower priority.
