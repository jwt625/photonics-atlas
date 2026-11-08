# cov_06 batch report (2026-11-07)

All seven cached texts match their source rows (page-1 title); none is a correction, erratum or another paper; no garbled text layer flagged. guo2023 (arXiv 2306.05314 v2), li2022 (arXiv 2204.12078 v1) and zhou2025 (preprint layout, arXiv 2406.12217) are preprint texts of the source rows' works; journal versions unread. No existing rows for these sources in `data/components/` (the merged `zhou2025a` rows are a different paper). Dry-run: +29 components, +132 metrics, 0 errors (the one warning, ni2025b m18 / m4, is an existing merged row).

| paper | components | metrics |
|---|---|---|
| babichev2025 | 3 (laser.other) | 9 |
| chen2020 | 2 (laser.tunable; phase_shifter.thermo_optic) | 17 |
| fan2025a | 6 (laser.tunable 2; resonator.coupled_rings; splitter.directional_coupler; chip_chip_coupler.butt; waveguide_platform.straight) | 32 |
| guo2023 | 3 (laser.comb; chip_chip_coupler.butt; fiber_chip_coupler.edge) | 12 |
| li2022 | 3 (laser.tunable; resonator.coupled_rings; chip_chip_coupler.butt) | 16 |
| xiang2021a | 10 (laser.heterogeneous 4; laser.sil; resonator.ring; reflector.bragg; waveguide_platform.transition; fiber_chip_coupler.edge; chip_chip_coupler.butt) | 39 |
| zhou2025 | 2 (laser.tunable; reflector.loop_mirror) | 7 |

## Fab / facility orgs

| paper | fab_org_ids | facility_org_ids | basis |
|---|---|---|---|
| babichev2025 | empty | empty | passive fabrication / growth; authors at four orgs (D80b) |
| chen2020 | empty | empty | passive voice, all authors HUST WNLO (D80b, D84a); SEM-use thanks to a staff member is not a facility basis |
| fan2025a | empty | empty | Si3N4 from an unnamed MPW foundry; RSOAs commercial, vendor not named |
| guo2023 | org_caltech | empty | contributions name Q.G. as fabricator (Caltech + CUNY affiliations); fabrication at KNI Caltech (D83c, D395) |
| li2022 | org_university_of_rochester | org_cornell_nanoscale_facility | contributions name four Rochester fabricators; "performed in part at" CNF |
| xiang2021a | org_ucsb (laser chip, taper, grating, facet taper, SIL row) | empty | contributions: C.X. and J.P. (UCSB) fabricated the laser; ring chip only "provided" (fab empty) |
| zhou2025 | empty | empty | passive "is fabricated ... using PLACE" (see question 2) |

Missing from the registry (name as printed + locator):
- Kavli Nanoscience Institute (KNI) at Caltech: guo2023 p.8 Acknowledgements ("device nanofabrication was performed at"); facility left empty (ledezma2022 precedent).
- Cornell Center for Materials Research: li2022 p.11 Acknowledgements ("performed in part at ... and at the Cornell Center for Materials Research"); facility candidate.
- Micro and Nano Fabrication and Measurement Laboratory (HUST WNLO): chen2020 p.6 Acknowledgment, SEM-use thanks to a staff member only; not needed by a row.
- Wafer / part suppliers noted only: NANOLN / NanoLN (guo2023 p.4, li2022 p.7), Anritsu RSOA AE5T315BY20P (zhou2025 p.3; org_anritsu exists, used as a note).

## Not entered, and why

babichev2025
- Table I (p.2): threshold modal gain 45 / 46 / 49 /cm, transparency current density 590 / 500 / 640 A/cm2, internal efficiency 54 / 53 / 43 %, internal loss 8 / 6 / 10 /cm (multi-length fits; mirror loss from an assumed facet reflectivity 0.32): no laser parameter (registry candidates: internal_loss_per_cm, transparency_current_density_a_per_cm2, internal_quantum_efficiency_pct, modal_gain_per_cm).
- Maximum external quantum efficiency 37 % (No. 2, 1 mm, p.3): no laser EQE / differential-efficiency % parameter (same gap as ji2026).
- T1 about 100 K (No. 2) and 86 K (No. 1 / No. 3, Fig. 2 labels): no parameter (candidate characteristic_temperature_t1_k).
- Threshold current densities vs temperature (Fig. 2) and differential gain (Fig. 1): no parameter; jth candidate threshold_current_density_a_per_cm2 (already listed in D431).
- Calculated miniband positions, hole subband spacing, VCSEL G0 estimate for the authors' earlier VCSEL [35]: model / cited.

chen2020
- 114 wavelengths on a 0.4 nm (50 GHz) grid: characterization grid, not a channel plan (no channel_spacing / n_channels row).
- Lorentzian linewidth below 100 kHz at the short-wavelength end: no wavelength printed (in notes).
- Simulated tenfold thermal-resistance increase (p.3): no parameter.
- 1x8 MMI, MIRs, shallow-deep transition: no values.

fan2025a
- Vernier mode suppression ratio about 13.5 dB measured / about 15 dB simulated (main Vernier peak over the next one): no parameter (candidate `msr_db` on resonator / wdm / laser, "main-to-adjacent Vernier peak suppression of a coupled-ring filter").
- WASR reflector: simulated bandwidth "exceeding 100 nm" with no level, no measured reflectivity: no reflector row (bent-DC row carries the simulated split).
- RSOA facet reflectance < 0.01 %, 3-dB gain bandwidth about 80 nm, 1 mm gain length: purchased-part properties with no vendor; in core_material.
- Table 1 values of other works (rule 3).

guo2023
- Pulse energy at least 2.6 pJ, peak power above 0.51 W (p.6): no parameter (candidates pulse_energy_pj, peak_power_w).
- Time-bandwidth product 0.445; pulse-width limit about 2.3 ps (Haus master-equation estimate, Supp. IV not cached); carrier blueshift about 0.3 nm over 140-200 mA; mode-locking current window 140-205 mA.
- Heterodyne beat-note FWHM 3.95 / 3.91 MHz against a 10 kHz reference: a beat linewidth limited by carrier drift, not the laser linewidth; in notes.
- Phase modulator (simulated VpiL 1.1 V cm, 4 um gap): EO-atlas item. Broadband loop mirror design: Supp. Sec. II (not cached), no values in the main text.

li2022
- EO laser-frequency tuning efficiency 0.26-0.34 GHz/V (Fig. 3(c), p.4): see question 1.
- Frequency-modulation rate 2.0 EHz/s, linearity < 10 % / 3 %, switching rise / fall about 3 ns (driver-limited), mode switching at 4 V, photon lifetime about 0.2 ns (estimate): no parameter.
- 41 kHz linewidth of "another laser device" with loaded Q about 2.5e4 (p.9): different, unnamed device (D159), in notes.
- PPLN SHG: no conversion value (15 % is a projection for 10x higher Qext); visible tunability over 10 nm, 20 nm theoretical phase-matching window: no frequency_converter row.
- Spot-size converter mode match: FEM figure, no number; coupling efficiency "relatively low", no number.

xiang2021a
- Threshold current densities 580 / 680 / 700 A/cm2 (p.3): no parameter.
- InP/Si-to-Si taper loss below 1 dB (p.2): sentence points to the authors' earlier work [44] (rule 3 / D80i).
- Si loop mirror "designed to provide 100 %" reflectivity: design statement only, no measurement; no reflector row. Loop-mirror and MZI dimensions are figure labels only.
- Gratings with 0.75 / 0.875 / 1.5 /cm: no printed reflection values (only the 0.25 /cm grating's 3.5 dB side-lobe suppression); kappa entered on the laser rows instead.
- Frequency-noise reduction 20-30 dB under self-injection locking; operation up to 75 C stage temperature; RIN at or below -165 dBc/Hz below 5 GHz (stated for the Fig. 2(f) traces together, in notes).
- Comb from a low-coherence FP-state laser locked to a 30 GHz ring (Fig. 3(d)): only the ring's nominal spacing printed; no comb row.
- SiN waveguide effective index 1.46 and mode area 5.3 um2: no matching parameter (group_index is not effective index).

zhou2025
- Fine-tuning resolution 0.014 nm (OSA-limited) and coarse step 0.07 nm: no parameter.
- EDFA-amplified 70 mW: external fiber amplifier output.
- 1x8 MMI: "proven to exhibit uniform 8-path splitting" with no number; geometry-only (100 um x 1680 um, 1 um ports, design): not a row.
- EO phase shifters: no Vpi / tuning efficiency printed; supplement not cached.

## Judgment calls

- babichev2025: broad-area FP edge emitters as `laser.other`, platform `inp`; one row per active-region structure at the 1 mm length used for T0 (the multi-length series has no per-length metric). Lasing wavelengths read off the Fig. 2 inset (+/-1 nm).
- chen2020: heater 2 pi round-trip powers kept in `tuning_power_mw` on the phase-shifter row (not converted to p_pi_mw); total heater power < 50 mW `derived` (authors computed it from heater settings).
- fan2025a: one laser row per gain chip (same Si3N4 cavity, two assemblies); the combined 17.5-23.8 kHz range statement entered on both with a cross-note. The RSOA1 17.5 kHz does not follow exactly from pi x 5807 Hz2/Hz (18.2 kHz); printed value kept, discrepancy in notes. Fig. 4 caption wavelength 1578.56 nm treated as a typo of 1568.52 nm (text, figure peak, Fig. 6(b)). Vernier pair as `resonator.coupled_rings` (one row, ring in condition), D400. Aligned-peak wavelength 1568.26 nm from the Fig. 2(d) axis (`wavelength_inferred`).
- guo2023: MLL as `laser.comb` (precedent: merged hybrid MLL rows); repetition rate entered (pulses characterized, D83b). On-chip powers `derived` (fiber power + measured 11 dB facet loss). fab org_caltech also on the laser row (TFLN cavity chip by the authors; heim2025 precedent).
- li2022: q_intrinsic / q_external `author_estimate` (D403); q_loaded 7.0e4 `measured` on the Vernier-pair row with "which racetrack not stated". Back-reflection 10 % simulated entered as 10 dB `simulated` (D83f). On-chip powers entered as `measured` with "referencing not described" (kumar2022a precedent).
- xiang2021a: grating gap widths mapped to kappa by listing order (1.783 / 1.338 / 1.276 um to 0.25 / 0.75 / 0.875 /cm; consistent with weaker kappa at larger gap). Figure reads of thresholds (blue about 68 mA, red about 58 mA, +/-3 mA) and maximum SiN-waveguide powers (24.5 / 14.5 / 12.8 mW, +/-0.5 mW). SIL row `laser.sil` with fab org_ucsb for the laser chip only (ring chip provided, fab not stated). Ring 42 M `author_estimate` (D403); 5 GHz FSR `author_estimate` (design vs measured not stated). Wavelength 1548 nm inferred for the facet, chip-chip and taper losses.
- zhou2025: SLR platform left empty (PLACE etch profile not stated, D422 / D423), laser platform `other` (hybrid). SMSR "is 30 dB" (p.10) vs "exceeding 30 dB" (abstract): entered as 30 `gt`.

## Questions for the coordinator

1. li2022 EO tuning efficiency 0.26-0.34 GHz/V of the Pockels laser: convert to `tuning_efficiency_pm_per_v` at the stated 1581.12 nm lasing wavelength (about 2.1-2.8 pm/V, `derived`), or add a frequency-unit parameter (`tuning_efficiency_ghz_per_v`; also would take ji2026's 620.6 GHz/W as `tuning_efficiency_ghz_per_w`)? Recommendation: add the GHz parameters, since the paper's quantity is a frequency shift and conversion adds a wavelength assumption across a tuning range.
2. zhou2025 fab: the MCI chip "is fabricated ... using the PLACE method", with method details in "our previous work"; authors at East China Normal University (one also SIOM). D84a counts "our process" statements, but the verb is passive and the reference is to a method paper. Recommendation: keep empty (li2026a / li2024a PLACE precedents), unless D84a is read to cover method-paper references (then org_east_china_normal_university, as nan2025).
3. xiang2021a SIL row fab org_ucsb: keep (laser chip made by UCSB authors; assembly is stage butt-coupling) or empty (the composite includes a ring chip whose fabrication is not stated)? Recommendation: keep with the note, as heim2026 laser rows.
4. Registry candidates with skipped values: laser `msr_db` (fan2025a 13.5 dB), laser EQE / differential efficiency % (babichev2025 37 %), `internal_loss_per_cm` and `transparency_current_density_a_per_cm2` (babichev2025 Table I), `characteristic_temperature_t1_k` (babichev2025 100 K), `pulse_energy_pj` / `peak_power_w` (guo2023 2.6 pJ / 0.51 W).
