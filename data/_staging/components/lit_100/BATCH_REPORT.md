# lit_100 batch report (2026-11-06)

All four cached texts match their source rows (page-1 title); none is a correction, erratum or another paper. No garbled text layer flagged. brunetta2026 (arXiv v1, 2025-11-07) and wang2024 (arXiv v2, 2024-06-12) are preprint texts with the same title and authors as the journal records (ACS Photonics 2026, APL Photonics 2024): same works (D430 / D433), journal versions unread. Dry-run: +44 components, +285 metrics, 0 errors (the one warning, ni2025b m18 / m4, is an existing merged row, not this batch).

| paper | components | metrics |
|---|---|---|
| denicola2013 | 1 (waveguide_platform.straight) | 3 |
| song2020 | 29 (waveguide_platform.bend: 27; waveguide_platform.straight: 1; fiber_chip_coupler.grating: 1) | 171 |
| wang2024 | 3 (resonator.ring) | 22 |
| brunetta2026 | 11 (waveguide_platform.straight: 1 fabricated + 2 design; resonator.ring: 7; frequency_converter.shg: 1) | 89 |

Helper scripts (scratchpad only): `gen.py` (row generator), `render.py` (page renders).

## Judgment calls

- Platform `other` for bulk LiNbO3 implanted ridges (denicola2013), ScAlN on oxide (wang2024) and AlN on sapphire (brunetta2026): no enum value fits (merged bulk-LN precedent uses `other`).
- song2020: one row per physical bend design (shape x radius x platform, plus the 60 / 20 nm offset variants of Fig. 11), rule 9. Bend loss = slope of transmission vs bend count (cutback, `measured`); Fig. 11 printed fit labels `measured` (caption says they are the measured bend loss; merged printed-label practice). R = 1 um advanced bend: Table VII 0.38 entered, Table VI prints 0.35 +/- 0.05 (conflict noted, D417). The 0.13 -> 0.04 dB/90 deg headline is R = 15 um in the abstract and Table IV but R = 20 um in the conclusion (noted on both rows, D417). Advanced Si R = 1 um: `min_bend_radius_um` 0.951 (Table V Rk at 45 deg, k2 > 0 shrinks the radius); all other rows carry the nominal R. Si fab org_imec (named standard process, D455); SiN rows fab empty (passive PECVD sentence, D80b). SiN 0.3 dB/cm platform loss and GC "over 50 %" `author_estimate` (origin not stated).
- wang2024: one population row for the 12 gap-varied R 140 um rings (D165; the 1.47e5 resonance is "a similar device", the gap of the Fig. 3 devices is not printed). All Q_i `author_estimate` (D403: Q_i from loaded Q + extinction with near-critical coupling assumed, not determined from data); 2.4 dB/cm `author_estimate` (rests on that Q_i). Anneal series (Fig. 4(c) printed labels 36 / 46 / 102 / 77 / 67 k) and the unpolished-film reference (0.5e5) as separate rows; their ring geometry is not restated, so no geometry copied. Fab org_astar: the acknowledgment names the A*STAR Cleanroom as the fabrication site (authors at A*STAR IMRE / IME, D154 parent); facility empty (own-org cleanroom, D404).
- brunetta2026: all Q_int and alpha `author_estimate` (D403: undercoupled regime asserted / ensured by gap choice, not shown from data; alpha also uses a simulated group index); loaded Q (Lorentzian fit) `measured`; sample A WG cutback 33.4 dB/cm `measured`. Table 2 means tied to the Fig. 4 rings: sample A (only ring described, TM mean equals Fig. 4(b)), sample B (Fig. 5 1.8 um set matches Table 2), sample C (only design described; D458). Sample B width series (Fig. 5, 1.2 / 1.4 / 2.3 / 2.9 um) added as rows with figure-read mean Q_int (+/- 0.03e6, `author_estimate`) and figure-read widths (`extracted_from_figure`). FDTD void losses: 21.8 / 12.9 dB/cm on the fabricated sample A 1.4 um WG row (same geometry, `simulated`, D80e); small-void cases (a) 1.2 x 1.0 um at 1550 nm and (b) 0.5 x 0.4 um at 650 nm as `design` rows. SHG waveguide: only normalized efficiency is shown; one `thermal_drift_pm_per_k` 51 pm/K `derived` from figure-read peaks (1558.8 / 1562.0 nm, +/- 0.3 nm, over 63 K). Fab empty (passive fabrication sentence, all authors at EPFL; D80b); Evatec AG (sputtered buffer) and DOWA (sample B epilayer) are supplier notes.
- denicola2013: one population row for the two waveguide widths (5 and 7.1 um; the 0.23 +/- 0.09 dB/cm mean is printed for both sets together, D165); width stored as the 5000-7100 nm span with the two discrete widths in condition. Fab org_oclaro for the masking-layer patterning it performed (named org performing a fabrication step); borderline, the implantation / etch performer is not named. Polarization `unspecified` (extraordinary only; propagation axis not stated).

## Not entered, and why

denicola2013
- Index-profile depth 2.75 um and plateau ne 2.2094 at 632.8 nm: attributed to the authors' earlier work [16] (rule 3).
- Table I (other works' etch techniques), Table III (mask features), Au / positive-PR relief structures (no waveguides), mask contraction 25-30 %, 2.3 um PR relief height: process data, no component metric.
- Near-field mode profile agreement (Fig. 6): no number.

song2020
- Simulated bend losses (Fig. 4, Fig. 9, Fig. 12 offset study incl. 10 nm optimum for R = 2 um advanced Si, 30 nm for a normal bend): curves only, not read.
- Maximum width of the advanced Si bends (645 / 531 / 575 nm, Table V / VI): no registry parameter (in labels / notes); SiN advanced-bend maximum widths not printed (Fig. 3 curves).
- Junction offsets 60 / 20 nm: no parameter (in labels / conditions). k1 / k2 coefficients: notes.
- Table VI rows [11]-[18]: other works (rule 3). R = 1 um loss vs wavelength (Fig. 10(b)): curves only.
- SiN grating couplers (850 nm, 10 deg fibers): no performance value, no row.

wang2024
- Grating coupler (8 deg fiber array, TE, 1550 nm): no performance value (Fig. 3(a) transmission in a.u.), no row.
- d31 of ScAlN 10 % / 30 % and AlN (about 1.0 / 1.8 / 0.2 pm/V), film roughness 5.2 nm, grain size 30 nm, XRD rocking-curve FWHM 1.8 deg, Sc content 11 %: material properties, no component parameter.
- Fig. 4(b) per-mode mean Q_i vs anneal temperature (error bars): figure only; Fig. 4(c) printed labels entered instead.
- Ref. [26] 2.26 / 1.6 dB/cm and ref. [47] 1.4e5: other works (rule 3).

brunetta2026
- Void density / size, roughness, XRD, SIMS, Raman stress, hillock densities (Table 1, Supp. S1): material properties.
- "Q_int up to 1.8e6 in sample B" (TE00 maximum over all widths): population statement; in the 1.8 um row notes.
- TE loss "about 10 dB/cm above TM" for sample A: relative statement; Table 2 TE ~41 dB/cm entered.
- Fig. 6(d)-(f) simulated loss vs void diameter / height / density, Table S1 convergence values: simulation-parameter sweeps of the defect model, not component designs; only the stated d = 30 nm values entered.
- SHG normalized efficiency (no absolute value); SCG spectra and dispersive-wave positions (Fig. 8(b)): no parameter.
- Sample A ring radius: not printed (60 um is stated for the Fig. 4(c)-(f) rings); left empty.
- Bus-ring gaps 500-800 nm (Supp. S2, "most" rings of samples B and C): not tied to one ring; in notes.
- Ref. 30 (Sun et al.) Q_int 2.8e6, ref. 15 3.7e6, ref. 16 8e5: other works (rule 3).

## Organizations

- denicola2013: Cu implantation performed at the 1.7 MV Tandetron accelerator of the CNR-IMM Laboratory, Bologna (p.2 Sec. II-A): "Institute for Microelectronics and Microsystems, National Research Council (CNR-IMM)" is not in the registry (parent org_national_research_council exists); facility candidate. Printed "Oclaro North America Inc." mapped to org_oclaro (alias candidate).
- wang2024: "A*STAR Cleanroom" (p.5) -> org_astar used as fab; no separate facility id needed.
- brunetta2026, song2020: no missing org needed by a row.

## Registry gaps (proposed)

- `max_width_nm` (waveguide_platform.bend): maximum waveguide width inside a widened / tapered bend (song2020 Table V: 645 / 531 / 575 nm for R = 1 / 2 / 3 um).
- `junction_offset_nm` (waveguide_platform.bend): lateral offset between straight and bent waveguide at the junction (song2020 Fig. 11: 60 nm at R = 5 um, 20 nm at R = 10 um).
- `coupling_angle_deg` widened to resonator / wdm (pulley coupling angle; wang2024 5 deg).
- `center_wavelength_nm` or a phase-matching wavelength on frequency_converter (brunetta2026 SH peak pump wavelength about 1558.8 nm at 20 C; already a D419 candidate).
