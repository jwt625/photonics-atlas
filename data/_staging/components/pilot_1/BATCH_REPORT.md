# Batch report pilot_1 (2026-10-20)

Transcribed by the coordinator from the subagent's final message (subagents cannot write report files).

Result: 18 components, 83 metric rows; merge dry-run 0 errors, 1 warning (V1). Basis counts: design_target 38, measured 29, simulated 9, derived 5, author_estimate 2. No network, ASCII only, no e-mail addresses.

## Per paper

- valdez2023 (4 components, 14 metrics): C- and O-band 2x2 MMIs (0.2 dB per coupler, derived loss-budget term; design length/width); Si inverse-taper edge coupler (4.2 / 4.8 dB per edge C / O, author_estimate; tip 180 nm, taper 300 um, lensed-fiber spot 4 um); Si feeder crossing the TFLN film edge (~0.1 dB per edge, both bands). Not entered: cited 0.8 dB/cm [21] and 0.6 dB/cm [25] and the 1.2 dB term computed from the cited value; phase-shifter loss and IL (EO rows); hybrid taper and MZI index structure (no number). Fab: not set ("foundry-fabricated"; Sandia thanked for "fabrication assistance", p.16).
- li2026aa (2 components, 27 metrics): SiON + LN bi-layer SSC to UHNA4 (TE per-facet loss at 8 wavelengths 0.56-2.21 dB; simulated transmission 91.4 / 92.2 / 88.4 % at 1310 / 1550 / 2000 nm; Table 1 geometry; UHNA4 MFD at 3 wavelengths); adiabatic 3-dB splitter (16-splitter cascade: 0.23 / 0.11 / 0.42 dB at 1310 / 1550 / 1970 nm; simulated 48.2 / 49.6 / 44.6 % per port; width 0.8 um). Not entered: TOPS and waveguide loss (supplementary notes not cached), cited designs, simulated sweeps and design goals, on-chip IL (EO). Fab: the CAS optoelectronic micro/nano fabrication facility (author contributions + acknowledgments, p.9).
- kohli2025 (5 components, 13 metrics): a-Si overlay GC on SiN (2.8 dB per coupler by cutback; ~2.75 dB scope unspecified in the IQ section); SiN-BTO vertical directional coupler 80 um (0.14 dB per transition by cutback, geometry); BTO photonic waveguide 4.5 dB/cm by cutback (new; EO holds only the plasmonic loss); photonic-plasmonic converters 3.5 dB (150 nm slot, host -mzm) and ~3 dB (100 nm slot, host -iq). Not entered: cited grating and converter values (ref. 56, 12), ideal-budget figures mixing simulation and cited work, EO-held plasmonic loss and fiber-to-fiber IL, the Fig. 1(b) bound restating 0.14 dB, Pt heater / SiN MMIs / O-band VDC (no number). Fab: LIGENTEC (SiN parts), Lumiphase (BTO parts) per author contributions p.9; BRNC only thanked.
- berman2026 (5 components, 17 metrics): racetrack (Q_L 605k best, Q_i ~1.2 M at 1534.14 nm; average Q_L ~300k over 1520-1580 nm; radius, straight length); 1-D photonic crystal high-contrast set (contrast > 40 dB; periods 415-430 nm); three PhC Fabry-Perot cavities (average and maximum Q_L; 230k resonance ~1545.1 nm with IL 8 dB unspecified). Not entered: propagation loss 0.447 dB/cm (EO row), Q 250k racetrack without geometry/wavelength, undefined "power penalties", finesse 50 / 53 / 67 (no parameter, notes), simulated 70 nm bandgap, linewidth annotations 2.5 / 6.7 pm, period sweep (qualitative), EO bandwidths. Fab: NUFAB (first author fabricated; acknowledgments).
- li2022b (2 components, 12 metrics): 532 nm GC (5 dB loopback_half, Fig. 5(b) 10 dB for two; simulated CE 33.6 %, simulated 1-dB BW 12 nm; period 288 nm, fill 0.6, fiber angle -10 deg as printed, SM450 MFD 3.6 um, etch 100 nm); 1x2 MMI (~0.8 dB excess derived from the five-MMI structure, Fig. 5(b) 19 dB for five; simulated 49.8 % per port; W 4 um, L 36.1 um). Not entered: 2.2 dB/mm (EO row), Euler bend and mode-filter taper (geometry only), ref. 18 comparisons. Fab: none stated ("our laboratory"); NanoLN = wafer supplier.

## Judgment calls

1. host_device_id left empty when one component serves several EO rows (EO rows listed in notes); set only for single hosts.
2. Loss-budget terms stated once without a band entered for both C and O rows (valdez2023).
3. valdez2023 edge-coupler loss = author_estimate ("estimated"; the measured total it is subtracted from is not given).
4. li2026aa splitter "IL" ~0.1-0.4 dB entered as excess_loss_db.
5. Single on-chip components scope per_coupler.
6. berman2026 band-stop PhC -> resonator.photonic_crystal (closest); kohli2025 interlayer coupler -> waveguide_platform.transition (taper tips in width_nm because tip_width_nm/gap_nm are not allowed there).
7. One row for a period set (berman2026 PhC).
8. Wavelengths read off figure axes (berman2026), noted.
9. "central 20 nm of the bandgap" average -> band cl_band.
10. Platform: valdez2023 MMIs lnoi_loaded_si; li2026aa SSC lnoi_rib.
11. Fiber MFD / spot-size specs entered as design_target (no specification basis).
12. kohli2025 ~2.75 dB "to the grating couplers": scope unspecified.
13. li2022b fiber angle -10 deg as printed.

## Gaps reported

G1 host_device_id single value (list or physical_device_id link; validator checks prefix only); G2 per_component scope; G3 `specification` basis for vendor / nominal parts; G4 loss-budget terms of unstated origin; G5 grating / reflector class (stopband width, reflectivity, n_periods); G6 finesse, n_periods, linewidth_pm/MHz, slab_thickness_nm, sidewall_angle_deg, port_separation_um, rib_height_nm; G7 taper / gap parameters for interlayer transitions; G8 geometry-only components (skipped); G9 values held only in EO notes (entered); V1 duplicate check ignores band; G10 acknowledgment-level fabrication statements; G11 loopback_half vs per_coupler preference.
