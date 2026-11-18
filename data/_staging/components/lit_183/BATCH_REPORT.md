# lit_183 batch report

Distilled 2026-11-18 under the pic-component-distill skill (Contract v4-v7, DevLog-007 rulings through D631).
Papers: lit:helgason2021, lit:xiang2019, lit:liu2024c, lit:kim2019a, lit:nejadriahi2023.
Totals: 17 components, 95 metric rows. `merge_component_staging.py --dry-run`: 0 errors (the only warning is in
another batch, cmp_lit_ni2025b_pimmwc).

All five cached copies are arXiv preprints of the listed journal papers. Page-1 titles match the source rows.
helgason2021 is v1 titled "Dissipative Kerr solitons in photonic molecules" (the journal title drops "Kerr") and
includes its Supplementary Materials (p.7-15). xiang2019, liu2024c and kim2019a are v1. Supplements they cite are
not in the cache: xiang2019 SI, liu2024c Supplementary Notes 1-12. All values come from the preprint text as cached;
the journal versions were not read.

## lit:helgason2021 (Nature Photonics 2021, arXiv 2007.02608 v1): 4 components / 23 metrics

- `device1_molecule` (resonator.coupled_rings, 9 rows): FSR main 227.32 / aux 236.7 GHz, Q_i 7.5 M and Q_ex 3.8 M
  (both author_estimate under D403), splitting 1.46 GHz (derived: 2 x kappa/2pi 730 MHz), 600 x 1650 nm, R 100 / 96 um.
- `device1_dks_comb` (laser.comb, 2): repetition rate 227.318 GHz (derived from 9 x 25.146 GHz + 1.004 GHz),
  conversion efficiency 36 % at 2.5 mW on-chip pump.
- `device2_molecule` (resonator.coupled_rings, 10): FSR 104.84 / 106.9 GHz, mean Q_i 5.7 M over 3 devices, Q_ex
  3.1 M (mean of 7) and 2-4 M over 1530-1570 nm, splitting 0.97 GHz (derived), geometry, R 217 / 213 um.
- `device2_dks_comb` (laser.comb, 2): tuning range 40 nm (1530-1570 nm), efficiency 32-49 %.
- Not entered:
  - D2/2pi, D3/2pi, beta2 65 ps2/km and gamma 1.1 /W/m: no registry parameter.
  - Group indices and Q_i 6.6 M: simulation inputs (Table S2).
  - Power per line > 12 uW, net conversion efficiency and the selected line counts (Table S3): no parameter.
  - Table S3 "Comb in Fig. S8" (eta 0.46, 17.8 mW): D159. Fig. S8 shows device-1 traces, while S6 / Fig. S9 show
    device-2 combs at two wavelengths, so the comb cannot be identified.
  - Fulop et al. column: the authors' earlier work (D259).
  - Heater tuning in Fig. 1(C): device not identified, and no tuning rate is printed.
- Judgment calls:
  - Fab `org_chalmers_university_of_technology` per D84a, borderline. The devices use the authors' own subtractive
    process (ref. 28, all co-authors), with the first-person "we can fabricate" and all authors at Chalmers. Supp. S2
    is passive. Overrule to empty if D84a is read narrowly.
  - Supp. S3 assigns the 227.318 GHz beat to "Fig. 3", but the value is device 1's FSR. The main text puts the beat in
    Fig. 2(D), so it is assigned to device 1 (noted).
  - Q values are author_estimate (D403): the paper states the coupling regime but does not derive it from the data.
- Missing orgs: none (no facility acknowledged).

## lit:xiang2019 (Optica 2020, arXiv 1911.06780 v1): 4 components / 20 metrics

- `iii_v_si_sin_dbr_laser` (laser.heterogeneous, platform other, 10):
  - threshold 75 mA; > 0.5 mW on-chip; differential resistance about 2.5 ohm.
  - Mode spacing about 0.025 nm; SMSR > 58 dB; 10.46 pm/C.
  - Lorentzian linewidth about 6 kHz and 4 kHz (derived as pi x S0).
  - Lasing 1546.00-1546.04 nm (figure read).
- `sin_spiral_dbr` (reflector.bragg, 6, test_structure true: performance comes from the passive grating of identical
  design): sidelobe extinction > 20 dB, period 526 nm, 20 mm long, 3.5 x 3.6 mm footprint, 2.8 um x 90 nm.
- `sin_waveguide` (waveguide_platform.straight, 4): 0.43 dB/cm (author_estimate, method not stated), spacer oxide
  about 0.66 um after CMP.
- `si_loop_mirror` (reflector.loop_mirror, 1): about 30 % reflectivity untuned (author_estimate, origin not stated).
- Not entered:
  - Fig. 3(a) InP/Si extended-DBR laser (73.18 pm/C, 3.3 nm): the group's laser from ref. 25 (D259 / D408).
  - 320 Hz: ref. 18.
  - 0.001-0.01 dB/cm "in the future": ref. 9.
  - Si-Si3N4 dual-level taper: only simulated mode overlap and index curves, no loss value. Geometry-only, not a row
    (200 um long; Fig. 1(d) labels 3 um, 400 nm, 800 nm, 200 nm, 150 nm cannot be assigned to layers with
    certainty).
  - Thermo-optic phase tuner: hysteresis only.
  - Spiral gap 920-944 nm, radii R1 2 mm / R2 1.445 mm, and peak "near 1550 nm": no reflector parameter.
- Judgment calls:
  - Fab `org_ucsb` from the author contributions (C.X. led the fabrication; J.P., M.J., W.J. assisted; all UCSB),
    following the beals2026 precedent.
  - Si loop mirror platform `soi_rib`. The 500 nm Si and 250 nm shallow-etch ridge are stated for the simulation of
    all Si waveguides, and the Si layer is bonded onto oxide.
  - Cladding thickness 0.66 um entered as measured; how it was measured is not stated.
- Missing orgs: none. Morton Photonics (affiliation of P.A. Morton) did not fabricate.

## lit:liu2024c (Nature Photonics 2024, arXiv 2305.03652 v1): 4 components / 28 metrics

- `er_sin_vernier_laser` (laser.tunable, sin, 17):
  - Intrinsic linewidth 50.1 Hz (derived) and <= 194.8 Hz (masked by the ECDL floor); integrated FWHM 82.2 kHz.
  - RIN < -155 dBc/Hz above 10 MHz, and down to -130 dBc/Hz at 10 kHz-1 MHz.
  - About 17 mW fiber-coupled at 1585 nm; > 4 mW over 1548.1-1585.8 nm.
  - SMSR 72 dB, and > 70 dB over tuning.
  - Tuning range 37.7 nm (derived) and > 40 nm.
  - Pump threshold about 20 mW; relaxation oscillation 0.3-2.4 MHz.
  - Cavity mode spacing 164 MHz (author_estimate); footprint; spiral cross-section.
- `vernier_filter` (resonator.ring, D400, 9): ring FSRs 98 / 100 GHz, Vernier FSR 4.65 THz / 37.1 nm, design 5 THz;
  kappa_ex 411 MHz and kappa_0 42.5 MHz (author_estimate, D403), 3-dB 636 MHz, IL 3.2 dB (author_estimate, Supp.
  Note 5 not cached).
- `output_fiber_attach` (fiber_chip_coupler.edge, 1): 2.7 dB at 1550 nm per coupler, including the UHNA-7 to SMF-28
  splice.
- `pump_ld_coupling` (chip_chip_coupler.butt, 1): < 3 dB, simulated.
- Not entered:
  - 1.9 dB/cm net gain: ref. 15 (rule 3).
  - On-chip slope efficiency 6.7 %: optical %, no parameter.
  - Frequency drift < 20 MHz / 4 h and < 140 MHz / 24 h: no parameter.
  - Design mode spacing ca. 200 MHz (Supp. Note 2), coupling ideality 0.87, Er concentration 3.25e20 /cm3.
  - The packaged laser's "comparable" linewidth: no number.
  - Reference-laser values (ECDL 166.6 kHz, fiber laser 2.4 kHz).
- Judgment calls:
  - Fab `org_epfl` from the author contributions (passive Si3N4 samples, packaging).
  - Facility `org_center_of_micronanotechnology` from "fabricated in the EPFL CMi".
  - The Er implantation site is not stated (noted).
  - `process_name` "photonic Damascene process (ref. 41)" is kept as the printed process, without a foundry.
  - The abstract (< -150 dBc/Hz) and text (< -155 dBc/Hz) disagree; the text value is entered and the conflict is
    noted.
  - EDWL1 (VL2.0) and EDWL2 / EDWL3 (VL2.1) are treated as one design, with the device IDs in conditions. Their
    differences are not described.
  - The 3SP Technologies pump diode (purchased) is noted on the laser row, not as its own row: it has no performance
    value of its own.
- Missing orgs: none for fab / facility. 3SP Technologies is a vendor of an assembly part, not entered as an org.

## lit:kim2019a (Optics Letters 2019, arXiv 1907.07164 v1): 2 components / 12 metrics

- `coupled_rings` (resonator.coupled_rings, 7): FSR 200 / 206 GHz and splitting 7.1 GHz (author_estimate: stated with
  the design, origin not stated); ring gap and bus gap 525 nm; 730 x 1000 nm.
- `normal_gvd_comb` (laser.comb, 5): line spacing 201.6 GHz (channel_spacing_ghz, D83b); pump-to-comb efficiency
  40.6 % (abstract 41 %) at 180 mW in the bus waveguide and 1559.79 nm; 51 / 38 / 18 lines above 50 uW / 100 uW /
  1 mW.
- Not entered:
  - Minimum coherence 94 %: no parameter.
  - Heater windows.
  - The 475 nm-gap sibling device and the 1540.56 nm and 115 mW spectra: no values.
- Judgment calls:
  - Fab empty: no fabrication statement, and the authors are split between Columbia and Cornell.
  - Facility `org_cornell_nanoscale_facility` ("performed in part at").
- Missing orgs: none.

## lit:nejadriahi2023 (Optics Letters 2023, arXiv 2209.13229): 3 components / 12 metrics

- `opa_16` (free_space_emitter.other, sin, 8): steering > 115 deg, spot size about 0.11 deg at boresight and about
  0.22 deg at +/-57.5 deg (derived from "doubled"), peak-to-sidelobe 11.5 dB, 16 elements, 0.775 um pitch, widths
  300-500 nm, 320 nm thick.
- `mmi_1x2` and `mmi_1x8` (splitter.mmi, 2 each): simulated excess loss 0.021 dB and 0.55 dB; the paper says
  "insertion loss", but for 1xN splitters this is loss beyond the ideal split. n_outputs.
- Not entered:
  - > 80 % power in the main beam: no parameter.
  - Neighbour-waveguide coupling -18 to -22 dB over several mm: crosstalk_db is not allowed for free_space_emitter
    or waveguide_platform.
  - 1.2 mm phase shifter: performance only in refs. 8-11, geometry only.
  - Bend radii 15-85 um.
  - Table 1: typical literature values.
- Judgment calls:
  - Fab `org_university_of_california_san_diego` from the first-person "designing and fabricating" (all authors UCSD).
  - The UCSD Nano3 staff thanks are noted but not used as a facility (D84b).
  - SRN platform `sin` (bucio2017 precedent).
  - Wavelength of the MMI values: 1525 nm, inferred.
- Missing orgs: "UCSD's Nano3 cleanroom" (p.4 Acknowledgments) is not in the registry under that name.
  `org_san_diego_nanotechnology_infrastructure` exists but is a different name. It is a staff thank-you only, so no
  facility role is proposed.

## Registry gaps (skipped value + locator + proposed definition)

1. `gvd_d2_mhz` / `beta2_ps2_per_km` (resonator, laser.comb): helgason2021 Table S1 D2/2pi -3 / -0.6 MHz, beta2
   65 ps2/km (p.8). Proposed: "second-order integrated dispersion D2/2pi of the resonator mode family as reported".
2. `net_conversion_efficiency_pct` or `comb_line_power_min_uw` (laser.comb): helgason2021 power per line > 12 uW (p.4),
   Table S3 net efficiency (p.15). Proposed: "lowest comb-line power within the stated line count".
3. `slope_efficiency_pct` (laser, optically pumped): liu2024c on-chip slope efficiency 6.7 % (p.4). Proposed: "optical
   output vs optical pump slope, reference plane in ref_plane".
4. `frequency_drift_mhz` (laser): liu2024c < 20 MHz over 4 h and < 140 MHz over 24 h (p.4). Proposed: "free-running
   optical frequency drift over the stated time".
5. `coherence_min_pct` (laser.comb): kim2019a minimum comb-line coherence 94 % (p.3, Fig. 3(a)).
6. `beam_efficiency_pct` (free_space_emitter): nejadriahi2023 > 80 % of power in the main beam (p.1).
7. `crosstalk_db` allowed for free_space_emitter / waveguide_platform: nejadriahi2023 emitter-array coupling below
   -18 to -22 dB (p.2).
8. Reflector geometry `gap_nm` and `radius_um`, plus `center_wavelength_nm`: xiang2019 post gap 920-944 nm, spiral
   radii 2 / 1.445 mm, peak near 1550 nm (p.3, Fig. 1(c)); candidates already listed in D430.
