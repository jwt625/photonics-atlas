# lit_103 batch report (2026-11-06)

All six cached texts match their source rows (page-1 title). None is a correction, an erratum or another paper. All six are publisher PDFs, so no arXiv preprint check (D430 / D433) was needed. No garbled text layer is flagged. Figure values were read from page renders: the cached `page_NN.png` files, and 300-600 dpi crops rendered from `source.pdf` into the scratchpad. Dry-run: +30 components, +199 metrics, 0 errors. The one warning (ni2025b m18 / m4) is on an existing merged row, not from this batch.

| paper | components | metrics |
|---|---|---|
| manganelli2017 | 14 (fiber_chip_coupler.grating 1; waveguide_platform.bend 4; wdm.mrr 9) | 87 |
| zhang2022b | 1 (wdm.other) | 23 |
| zhong2025 | 5 (wdm.cascaded_mzi 4; fiber_chip_coupler.grating 1) | 42 |
| perez2017 | 3 (switch_fabric.mzi_mesh 1; wdm.cascaded_mzi 1; fiber_chip_coupler.grating 1) | 14 |
| suzuki2020 | 6 (switch_fabric.mzi_mesh 2; waveguide_platform.straight 1; crossing.other 1; fiber_chip_coupler.edge 2, of which 1 design) | 26 |
| yu2023a | 1 (switch_fabric.wss) | 7 |

## Not entered, and why

manganelli2017
- p.3 says the demonstrated filters have "2.4 THz FSR and a 3 dB bandwidth of about 100 GHz (0.8 nm)". This statement names no device. It also disagrees with the Fig. 7 double-ring reading: about 145 GHz at 3 dB and about 95 GHz at 1 dB. Not entered (D159); the conflict is noted on the Fig. 7 row (D417).
- The abstract gives an FSR "up to 2.4 THz (19 nm)" and "non-adjacent channel rejection higher than 35 dB" but names no device. The 19 nm agrees with the 450 nm Fig. 6(b) reading (19.5 nm, entered as a figure read). The > 35 dB is reached in Fig. 7 only from about +600 GHz; at +400 GHz the reading is about 31 dB. Both claims are in notes only.
- Simulated design maps (Fig. 2, Fig. 3: IL, BW, ripple, rejection vs K1 / K2): design-space plots with no device. Not read.
- Ring perimeter and R_eff of the rings are not printed (only "about 30 um" and "below 4 um" as design limits), so there is no radius_um. Heater geometry beyond the distance is not printed.
- Heater resistances 870 / 980 ohm: heater_resistance_ohm is phase_shifter-only (in notes). Sheet resistance 480 ohm/sq: process value, no parameter.
- Fig. 8(a) FSR of the heated devices (about 18.7 nm): not entered. The width of the Fig. 8 devices is in conflict (text 410 nm, caption 450 nm), and the FSR depends on it.
- Cited: double-ring FSR 12 nm of ref. [8], and the >10x improvement from substrate removal in ref. [31] (rule 3).

zhang2022b
- Simulated 15-dB-ER windows 65 / 50 nm (p.4): no band edges printed. Simulated tolerance cases (fill factor 0.31-0.43, slot 45 nm, unfilled SWG holes): perturbed designs, in notes only. Table I rows of other works (rule 3).
- SWG pitch 200 nm, fill factor 0.37, SWG slot width 60 nm, port offset 0.1 um: no registry parameter on wdm (see registry gaps). These are in core_material / notes.

zhong2025
- Si-SiN inter-layer coupler: the paper gives geometry only (Si taper 500 -> 150 nm over 75 um, SiN 800 -> 180 nm over 45 um, 35 um overlap, 150 nm oxide; p.3) and a simulated field plot with no value (Fig. 1(a) inset). It has no performance metric, so it gets no row (skill rule 9). The geometry is in the GC row's core_material.
- IL variation "within +/- 0.5 dB" across dies: not a max-min value. Not entered.
- Table I arm-length values: the table image gives formulas only. Table III comparison rows (rule 3).

perez2017
- The Supplementary Notes are not cached. Propagation, bend and MMI losses, heater phase calibration and thermal crosstalk are reported there only, so none is entered.
- Ring (6 / 12 / 18 BUL), CROW, SCISSOR and ring-loaded MZI configurations: no value is printed in the main text (spectra only).
- Chip area 15 x 20 mm2 includes the auxiliary test cell, and the mesh footprint is not printed: notes only. BUL 975 um (13.5 ps) is in label / notes; there is no parameter for a unit-cell length.

suzuki2020
- 32 x 32 power extrapolation 3.67 W: projection. Leakage to non-target ports below -60 dB: absolute transmission level, not a suppression ratio (in notes).
- Turbo-pulse switching about 3 us (ref. [18]), C-band intersection 0.022 dB and C-band waveguide loss (ref. [10]), C-band 8 x 8 switch power 312 mW (ref. [10]): cited (rule 3).
- Simulated < 1 dB/facet edge coupling (p.5): no design is named. Projected 5 dB and < 10 dB fiber-to-fiber totals: projections.
- FWM idler -36 dB at 11 dBm/ch: no parameter (in notes of the waveguide row).
- Table I per-path terms (2 x 1.3 dB propagation, 0.8 dB MZ switches, 0.3 dB intersections): budget terms for the minimum path. The number of elements per path is not printed, so no per-element value. In the switch row notes.

yu2023a
- Spectral resolution 1 GHz (8 +/- 1 pm per pixel) and 3-dB bandwidth tuning step 0.875 GHz (7 pm): no parameter (registry gap).
- Table I optics values (focal lengths etc.), blazed-grating period 193.125 um / 52 pixels, deflection 0.46 deg: design / setup values with no parameter.
- 12 x 12 extension: proposal.

## Missing fab / facility orgs

- Southampton Nanofabrication Centre (perez2017 p.8 Methods: "The device was fabricated at the Southampton Nanofabrication Centre at the University of Southampton"). Facility candidate, parent org_university_of_southampton. If registered, it goes on the 3 perez2017 rows. Not in organizations.csv / org_aliases.csv.
- AIST TIA Super Clean-Room (suzuki2020 p.1 footnote: the device fabrication was supported by the TIA Super Clean-Room of AIST). Facility candidate, parent org_national_institute_of_advanced_industrial_science_and_technology. It is already queued for the org round as "AIST SCR" (konoike2022, D453). If registered, it goes on the 5 fabricated suzuki2020 rows.
- Ids used, all in the registry: org_cea_leti, org_applied_nanotools, org_sitri, org_university_of_southampton.

## Judgment calls

1. manganelli2017 row structure: one wdm.mrr row per measured passive design.
   - 410 nm with normalized node distance 1.7 / 2.0 / 2.4 (Fig. 6(a)) and 450 nm with 2.0 (Fig. 6(b)), each with its figure reads (FSR where two peaks are in view, peak drop loss).
   - The Fig. 7 double ring (410 nm, K1 20 % / K2 1.23 %) does not state its node distance, so it gets a separate unnamed-device row (D422 matsuo2013 precedent).
   - The heater study is entered as three heater-distance rows (0.5 / 0.75 / 0.92 um). Width (410 / 450 nm) is in the condition (D165 family rows), because Fig. 9 gives both widths and the Fig. 8 / Table 1 devices have a width conflict (text 410, caption 450; D417).
   - The paper says heaters sit on all passive structures, so the heater rows and the passive rows describe overlapping hardware along different design axes (cross-referenced in notes).
   - Alternative: one row per width with node distance and heater distance in the condition.
2. manganelli2017 headline 36 mW/FSR per ring: entered on the 0.5 um heater row as `measured`, approx, mean.
   - It equals the mean of the two Fig. 9 points at 0.5 um (32.6 and 39.3 mW).
   - 72 mW/FSR is entered as `derived` (the authors doubled it).
   - 0.69 nm/mW is entered as 690 pm/mW `derived` (D256).
   - The printed pair (36 mW/FSR at 0.69 nm/mW) implies an FSR of about 25 nm, which matches none of the measured 17-19.5 nm FSRs (noted, D417).
3. manganelli2017 bends: entered as `insertion_loss_db` per_component per 180-deg bend, cutback, extracted_from_figure ranges over 1520-1575 nm (deng2024 precedent). They are not halved into bend_loss_db_per_90: the Bezier bend is one 180-deg curve, not two 90-deg bends. The chung2017 / cheung2019 halving precedent is the alternative.
4. manganelli2017 platform soi_strip on the bends and rings: the design section says fully etched waveguides are used to cut bend loss (p.5); no etch depth is printed. The GC is `soi`. Fab org_cea_leti: "fabricated at CEA-LETI" names the org (rule 12).
5. manganelli2017 K2 = 1.23 % is `simulated`: it is computed from the maximally flat condition, Eq. (3) (D82a). K1 = 20 % and the single-ring K = 7 % are `author_estimate` (design choices).
6. zhang2022b:
   - wdm.other: a band diplexer built on a two-mode interference coupler.
   - Measured IL is de_embedded with reference_structure (directly connected GC pairs). The IL < 2 dB and ER > 15 dB windows are entered as bound rows with wavelength_nm..wavelength_max_nm.
   - Simulated IL / ER / 1-dB widths are entered as `simulated`. Simulated IL scope per_component.
   - Taper length 9 um is the preset value of the design study, flagged in notes. Platform `soi` (etch not stated, D422 / D423).
7. zhong2025:
   - Channel crosstalk goes in `crosstalk_db`: the paper defines it as the extinction ratio at the channel centre and gives no adjacent / non-adjacent type. Table II prints "< -x dB", so the rows carry qualifier gt.
   - The wafer-level worst crosstalk 14.8 dB has no statistic, with "maximum (worst) over 13 dies" in the condition.
   - The GC curve is "single-ended coupling efficiency of the reference waveguide" and includes one Si-SiN coupler. It is entered as loopback_half / loopback with the transition in `includes`.
   - Fab org_sitri: "fabricated on the silicon photonic platform at SITRI".
   - The three stage reference filters are separate test-structure rows carrying measured and design FSR.
8. perez2017:
   - The mesh is entered twice (D396): as switch_fabric.mzi_mesh for routing (crosstalk > 25 dB, about 40 dB) and as wdm.cascaded_mzi for its FIR filter function. The FSRs 18.4 / 9.2 / 18.4 GHz are entered as configuration operating points, `measured`. The text describes them as the measured periodicity; they match 1 / (N x 13.5 ps) within 0.5 %. Alternative: author_estimate.
   - The 40 dB "measured optical crosstalk" sentence names no element (condition says so).
   - Platform soi_rib: 120 nm etch of 220 nm Si.
   - Fab org_university_of_southampton: the author contributions name the fabricator (D395).
9. suzuki2020:
   - JLT extension of the authors' conference paper ref. [14]. The introduction sentence with 16.6 dB / 70 nm / -30 dB cites [14], but the results section presents these as this paper's measurements without a citation, so the values are kept (D408). This is the weak point, as in D468.
   - Fab empty: passive "was fabricated ... at a CMOS pilot line" with the pilot line unnamed (D80b). konoike2022 had a first-person sentence; this paper does not.
   - The 5.6 dB per facet is printed as "estimated from a guide waveguide" and is entered as `measured` (skill rule 4, test structure), with the subtraction not shown.
   - On-chip 3.7 dB is `derived` (14.9 - 2 x 5.6).
   - 9.6 mW P_pi is `author_estimate`: a budget term of unstated origin.
   - The 30 us switching time goes in rise_time_us with "definition not stated".
   - The O-band library edge coupler (2.3 dB/facet, 140 nm, 100 um) is a `design` row (not on this chip) with author_estimate loss.
   - Fig. 2 x axis is labelled um but the data are in cm (noted).
   - Crosstalk window 1290-1360 nm read off the Fig. 7(b) arrow (`wavelength_inferred`).
10. yu2023a:
    - In scope per D424 (LCOS chip with fiber collimator I/O; yamaguchi2016 precedent): switch_fabric.wss, platform `other`, fab empty (the system "was built", passive).
    - IL < 13.2 dB is scoped device_total. The paper does not say whether the circulators are de-embedded.
    - The 16.25 GHz minimum bandwidth is `measured` / best. The 3750 GHz upper end of the tuning range is `author_estimate` (no measurement shown).

## Registry gaps (skipped value, locator, proposed definition)

- `heater_gap_um` (or a heater-distance parameter) on wdm / resonator: manganelli2017 heater-to-ring distance 0.5 / 0.75 / 0.92 um (p.6, Fig. 9). Edge-to-waveguide distance of an in-plane heater (heater_offset_um is a centre offset). Currently in labels and conditions.
- `heater_resistance_ohm` on wdm (already a candidate in D440): manganelli2017 870 / 980 ohm (p.8).
- `subwavelength_period_nm` and `fill_factor` on wdm, plus a slot width (`slot_width_nm`) and port offset: zhang2022b SWG pitch 200 nm, ff 0.37, slot 60 nm, offset 0.1 um (p.2-3).
- `operating_range_nm` on wdm (as proposed in lit_94): zhang2022b ER > 15 dB over 82 / 56 nm and IL < 2 dB over 88 / 99 nm. Entered here as bound rows over a wavelength range; a span parameter would make them comparable.
- `spectral_resolution_ghz` / `center_tuning_step_ghz` and `bandwidth_tuning_step_ghz` on switch_fabric (WSS): yu2023a 1 GHz (8 +/- 1 pm) and 0.875 GHz (7 pm) (p.4-5). These are the smallest steps for channel centre and channel width.
- `unit_cell_length_um` / delay on switch_fabric (programmable meshes): perez2017 BUL 975 um, 13.5 ps (p.4). Lower priority.
