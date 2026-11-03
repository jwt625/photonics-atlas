# Batch lit_65 report

Distilled 2026-11-02 under contract v6. Dry-run: `batch lit_65: +35 components, +200 metrics; errors 0`.
All seven cached texts are the expected paper (page-1 title); none is a correction or another paper.

| paper | components | metrics | classes |
|---|---|---|---|
| yoo2022 | 5 | 15 | chip_chip_coupler.butt, laser.dfb, splitter.mmi x2, splitter.directional_coupler |
| asch2025 | 7 | 41 | waveguide_platform.transition x3, chip_chip_coupler.evanescent, waveguide_platform.straight x2, fiber_chip_coupler.edge |
| kasztelanic2018 | 1 | 5 | micro_optics.facet_lens |
| blaicher2020 | 5 | 21 | chip_chip_coupler.photonic_wire_bond x3, fiber_chip_coupler.photonic_wire_bond, laser.dfb |
| ropp2021 | 4 | 35 | free_space_emitter.grating_emitter x4 (2 fabricated, 2 design) |
| lim2021 | 6 | 56 | fiber_chip_coupler.grating x4, free_space_emitter.grating_emitter x2 |
| theurer2019 | 7 | 27 | chip_chip_coupler.butt x3, laser.dfb x3, fiber_chip_coupler.edge |

## Values not entered, per paper

- yoo2022: all MZM values (VpiL 1.63-1.77 V cm, MZM IL 4.20-4.53 dB, PN-PS loss, E/O bandwidth about 20-22.6 GHz, ER, TDECQ; p.8-15): EO-atlas candidate. Undoped PN-PS waveguide 1.61 dB, 1 dB of it from the meander (p.9): part of the modulator, not a row. Threshold and slope of Fig. 5(b) not read. Monte-Carlo bonding success above 0.97 (p.7), recess about 10 um: notes. Heterogeneous and ball-lens values on p.2 are cited.
- asch2025: flip-chip per-interface loss has no breakdown (attempt failed, p.11); only the authors' about 1 dB entered, author_estimate. Simulated 1 dB at 750 um and PDL below 1 dB above 1000 um (p.5 Fig. 4): note. Peak wavelengths 1320 / 1350 nm: note (parameter not allowed). 1 um offset gives 10 dB (simulated, p.12): note.
- kasztelanic2018: working distance, NA, gradient constant, pitch: no parameter, see gaps. Half-pitch simulations (351 / 355 um, p.2) and Fig. 8 future-lens map not entered.
- blaicher2020: SOH MZM UpiL 1.3 V mm (p.8): EO-atlas candidate. HCSEL MFD 3.5 um and 0.4 dB PWB (ref. 17), 1300-1600 nm (ref. 16): cited, not entered (D259). 19 dBm power test, 25 um pitch, 35 um bend radius: notes. Module footprint 4 x 1.5 mm: not a component value.
- ropp2021: outcoupling strength and its dynamic range, Fig. 2(c)-(d) data: no parameter or no printed values, notes. 10 / 20 nm etch outcoupling (about 42 / 95 %): note on the design row. EVC not a separate row (its only result is wy on the emitter rows).
- lim2021: waveguide loss about 1.15 dB/cm cited from the authors' earlier work. C12 / C15 beam widths not printed (Fig. 8 multi-peak): no emitter rows for them. Addressable-ion counts: application statement.
- theurer2019: Table I rows of other works: not entered. Calculated air-gap curves of Fig. 4 beyond the printed 6 um value not read. Pulsed power curves not read.

## Missing or open orgs

- Missing: Institute of Electronic Materials Technology (Department of Glass), Warsaw, Poland (kasztelanic2018 p.1): fabricating org per author contributions; not in `organizations.csv` / `org_aliases.csv`; fab empty until registered.
- Registered and used: org_amf, org_neophotonics, org_imec, org_karlsruhe_institute_of_technology, org_karlsruhe_nano_micro_facility, org_national_institute_of_standards_and_technology, org_center_for_nanoscale_science_and_technology.

## Judgment calls for the auditor

1. lim2021 split under D396: losses, simulated efficiency and fiber angle on `fiber_chip_coupler.grating` (4 rows), beam widths on `free_space_emitter.grating_emitter` (C25, C30). No merged free-space row holds a fiber-to-fiber value, so this follows that pattern. Alternative: all on free-space rows.
2. lim2021 beam widths in `beam_diameter_um`: paper says beam width and beam waist interchangeably, criterion not printed; `beam_waist_um` (1/e2 radius) would be a guess.
3. lim2021 fab empty: MPW stated, no fabricator named; A*STAR IME (one author's org) and AMF only as support on p.1 (D398 not applied).
4. asch2025 lithography approach = `waveguide_platform.transition`, flip-chip = `chip_chip_coupler.evanescent`, platform other (dangel2018 precedent), although the batch family is chip-chip.
5. asch2025 adiabatic 0.56 / 1.04 dB `derived`, method loss_breakdown (arithmetic closes to the printed 4.3 dB total with the SiN term read from Fig. 9(b)); cut-back propagation and per-facet values `measured` (D167).
6. asch2025 fab org_imec under D154 (every author lists imec; CMST is imec and Ghent University); CMST cleanroom support staff thanks not entered as a facility. SiN waveguide row fab empty.
7. asch2025 one range (0.3-1.2 dB) printed for 2 mm and 3 mm together is on both rows; wavelength span from the Fig. 13(b) axis. Sub-2 dB chip-to-chip and chip-to-fiber figures entered as author_estimate, scope device_total.
8. blaicher2020 per-PWB estimates are author_estimate (rest on a typical MZM loss; coherent-module method details only in Supp. S3). The IM/DD 3.6-5.3 dB covers the laser-side and fiber-side PWB of each pair: one chip_chip row. Band unspecified on module rows: no HCSEL wavelength printed (1550 nm applies only to the test chips and fiber data).
9. blaicher2020 facility org_karlsruhe_nano_micro_facility from the support acknowledgement (p.10), first merged use of this org in `facility_org_ids`: check against the grant / program rule. HCSEL fab empty (U.T., M.M. "contributed", no fabrication wording).
10. blaicher2020 launch powers on the HCSEL laser row with ref_plane fiber and includes: module-level, kept because they are the only laser output values.
11. kasztelanic2018 class `micro_optics.facet_lens` (glued stack-and-draw GRIN on a fiber facet; definition mentions 3D-printed); `micro_optics.other` is the alternative. Water spot about 7.5 um author_estimate: all measurements were in air (p.10). Scope D411: fiber-coupled passive part.
12. ropp2021 fab NIST under D399 (first-person fabrication account, all authors list NIST, two also University of Maryland). Thicknesses of the fabricated rows come from the simulated device and the stated experimental geometry.
13. ropp2021 design rows: `apodized_design_30nm` and `uniform_grating_50nm` kept to carry simulated values and geometry; uniform gratings were also fabricated but printed no values.
14. theurer2019 per-sample split: `interface_design` (piezo), `bonded_active`, `bonded_visual`; `dfb_bare`, `dfb_active`, `dfb_visual`. 36 mW cw: text value, Fig. 5 cw 20 C curve reads about 34 mW at the axis limit. Wavelength inferred (C band) from Fig. 6 / 8 for all coupling losses. 2.35 dB chip-to-fiber author_estimate (origin not stated, D418). Fab empty (no explicit statement; HHI and LioniX by affiliation only). Platform other on the bonded rows (theurer2020 precedent).
15. yoo2022 splitter rows are about-50 % and about-90 % statements, author_estimate; fab org_amf from the foundry sentence, applied to the coupler row with the assembly org unstated. LD platform empty (D422 / D423). 6 dB `measured` (printed as measured separately; method unspecified).

## Registry gaps (skipped value, locator, proposed definition)

- `working_distance_um` (micro_optics): kasztelanic2018 54 +/- 2 um air, measured, p.4. Distance from the lens facet to the focal plane, medium in condition.
- `numerical_aperture` (micro_optics, fiber_interface): kasztelanic2018 0.16, p.9. Numerical aperture as stated, definition in notes.
- `power_handling_dbm` widened to chip_chip_coupler: blaicher2020 about 19 dBm on-chip without PWB damage, p.5 (value with `gt`).
- `pitch_um` widened to chip_chip_coupler: blaicher2020 25 um, p.4; D250 rejected it for waveguide_platform only.
- `center_wavelength_nm` widened to waveguide_platform.transition / chip_chip_coupler: asch2025 1320 / 1350 nm, p.11.
- `grating_radius_um` (fiber_chip_coupler, free_space_emitter): lim2021 12-30 um, p.1-2. Radius of curvature of the focusing grating lines.
- `outcoupling_strength_per_um` and `outcoupling_dynamic_range_db` (free_space_emitter): ropp2021 0.014 um-1 p.3, 22.8 +/- 0.3 dB p.5. Radiation decay rate and range of achievable values.
