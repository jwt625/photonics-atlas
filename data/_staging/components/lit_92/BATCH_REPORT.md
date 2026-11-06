# Batch report: lit_92 (free_space_emitter, fiber_chip_coupler)

Date: 2026-11-06. Result: 20 components, 95 metric rows; `merge_component_staging.py --dry-run`: 0 errors (one pre-existing warning on merged ni2025b rows, unrelated). Page-1 titles match the source rows for all three papers; none is a correction or erratum; no garbled text layer.

| paper | components | metric rows |
|---|---|---|
| chung2017 | 14 | 66 |
| poulton2017 | 2 | 11 |
| mangal2019 | 4 | 18 |

## chung2017 (JSSC, 22 pages; journal extension of the ISSCC 2017 demonstration, D408)

Rows (all platform `soi`, fab `org_globalfoundries`, process GlobalFoundries 7RFSOI 180 nm SOI CMOS):
- `opa_1024` (free_space_emitter.other): 0.03 deg beamwidth (Fig. 29), 0.05 deg at +5 C (Table II), side-lobe level 10.54 / 10.47 dB (Table II), 45 deg steering (abstract, Table III), 21.9 dB array loss excluding the input GC (author_estimate, origin not stated), n_channels, pitch, chip footprint.
- `opa_32` (sub-array chip): 45 deg steering, 9 dB SLSR, 1.2 deg beamwidth (Fig. 26), footprint.
- `grating_antenna` (grating_emitter, the paper calls it a focusing grating coupler): simulated about 50 % to air and 17 deg (Fig. 17); 1 um width; Fig. 16(b) labels period 700 nm, gap 350 nm (fill factor 0.5 derived), length 3.55 um.
- `si_strip_wg`: 1.27 dB/mm -> 12.7 dB/cm (derived), 1-dB extra-loss input powers 220 / 190 mW (300 / 500 um) as dBm (derived), width 540 nm, Si 145 nm, BOX 1 um.
- `si_bends`: 0.7 / 0.2 dB per 180 deg at R = 2 / 5 um, halved to per-90 (derived).
- `dc_lc5` ... `dc_lc25` (5 directional couplers, Fig. 11(a) series): split ratio read off the plot at 1550 nm (5, 18, 38, 50, 79 %, +/- 2 %), 18 um coupler 46-53.5 % over 1530-1570 nm (Fig. 11(b)); gap 260 nm from the Fig. 10(a) label.
- `tops_folded`: P_pi 24 mW (48 mW per 2 pi, halved), IL 2.3 dB, 3-dB bandwidth 5 kHz (phase) and 50 kHz (MZI intensity), rise / fall 66 / 28 us, heater 330 ohm, lateral gap 0.5 um, 110 um length, 500 um2.
- `tops_straight_testchip`: P_pi 42.5 mW (85 mW per 2 pi, halved), standalone test chip.
- `voa` (thermo-optic MZI attenuator, phase_shifter.thermo_optic per D155 / morichetti2021): 15 dB at 70 mW, IL 1.2 dB, 40 us rise, 500 ohm, 40 um heated length, 475 um2.
- `mmi_1x2`: 0.4 dB printed as "insertion loss" for a 1x2 MMI -> excess_loss_db, author_estimate (origin not stated); footprint 5.5 um2.

Not entered:
- All CMOS circuits (DACs, INL / DNL, settling, bias) and system-level numbers: not components.
- Input fiber grating coupler: no performance number (fiber 18-20 deg in a quartz V-groove is setup); no row.
- Optical 3-dB bandwidth of the 1024 OPA on three dies: 3.2 nm (402 GHz), 3.3 nm (416 GHz), 3.1 nm (388 GHz) (p.20 Fig. 33): `bw_3db_nm` / `bw_3db_ghz` not registered for free_space_emitter.
- Power consumption per antenna 54 mW (p.19 Table III); radiated 0 dBm estimate and 160 mW deliverable (p.20, estimate): no free_space_emitter parameter.
- Simulated L_pi = 18 um of the directional coupler (p.9): no parameter. Conflict noted: with Eq. (7) 50 % would fall at 9 um, measured 50 % is at 18 um.
- Phase coherence length 2.8 mm, rms phase error 43.6 deg, noise floor -11.3 dB (p.17, simulation-fit derived), average side lobe 10.3 dB (p.16): no parameter.
- 803 deg maximum phase shift at 107 mW (computed capability), heater temperature / current limits (p.9-10).
- 165 nm polysilicon tooth thickness and the 30 um array-element size: stated with the authors' earlier ref. [19] (D259). Lcoh about 4 mm (ref. [24], cited).
- Fig. 16(b) 380 nm label (meaning not stated); Fig. 10(b) asymmetric-coupler design lengths 6.2-18.1 um (design only, no measured value each).

Printed conflicts (D417): chip area 37.48 mm2 vs 5.7 x 6.4 mm = 36.48 mm2 (footprint entered from the dimensions, note); gap "260 um" in text vs 260 nm figure label; Table III side-lobe suppression 9 dB for "This Work" (the 32-element value) vs Table II 10.54 dB for the 1024 array (Table II entered); "66-ums" / "40-ums" typos.

Judgment calls:
1. 1024-array steering 45 deg entered as measured from the abstract / Table III, although the steering sweep shown is the 32-element chip (note on the row). Alternative: author_estimate or notes only.
2. Fig. 11(a) points entered as five sibling DC rows (rule 9) with `test_structure` true (test chip carries the building-block test structures, p.14).
3. MZI intensity bandwidth 50 kHz kept as a second `bw3db_khz` row with the condition stating it is not the phase response.

Missing org: The MOSIS Service ("for supporting the chip fabrication", p.21): MPW access provider, fab org under D398 once registered (all 14 rows).

## poulton2017 (CLEO, 2 pages)

Rows: `opa_ir_1024` (1024 antennas, 0.021 deg FWHM on both axes, 10 dB SLSR, 13.6 dB main-beam loss derived from 400 mW at 9.1 W, 4 x 4 mm aperture) and `opa_vis_635` (0.064-0.074 deg as a range because the axis assignment is not printed, 8.7 dB SLSR array axis, 0.5 x 0.5 mm aperture). Platform `sin`; fab empty (passive 300 mm wafer statement, no org; D80b).

Not entered: 400 mW main-beam power (no output-power parameter for free_space_emitter; used in the derived loss), theoretical diffraction limits, Fig. 2(b) spots at +/-19 / +/-40 deg (diffraction orders of a passive array), 10-level MMI tree (no number), visible antenna count (not stated), SiN thickness (not stated).

Judgment call: the derived insertion_loss_db (device_total, main beam only) follows the merged poulton2022 m6 convention.

## mangal2019 (IEEE Photonics Journal, 12 pages)

Rows (all `fiber_chip_coupler.grating`, platform `soi`, fab `org_imec`, test_structure true):
- `backside_gc_opt` (Fig. 8 sample, "optimized reflector"): -2.3 dB SMF (loopback_half, measured), 55 nm 3-dB bandwidth, -1.7 dB output into 50 um MMF (per_coupler, loss_breakdown, derived), 1-dB lateral tolerances about 2.2 um SMF and 13 um MMF (Fig. 8(b) reads), simulated -1 dB / 45 nm, geometry (490 nm, 0.5, 70 nm, 220 nm, BOX 2 um, top oxide 2 um, 10 deg).
- `backside_gc_ti0`, `backside_gc_ti2`: Fig. 6(a) peak reads about -2.5 and -3.1 dB (AR state not stated).
- `backside_gc_ti5`: -5 dB before AR (Fig. 5(a)), -3.5 dB after the SiN AR (Fig. 5(b) label).

Not entered: Table 1 (other works); simulated directionality about 90 % and back-reflection about 10 % (no parameter); 0.32 dB calculated mode mismatch and 9.2 / 10.4 um beam sizes (calculation inputs); top-oxide series 1.0-1.8 um (Fig. 5(a), overlapping noisy curves, only 2 um printed); 0.5 dB peak drop per 50 nm oxide change (sensitivity, Fig. 7); Ti film absorption (Fig. 6(b), not a component); Ti transmittance values (cited ref. [33]).

Judgment calls (coordinator questions):
1. Sample identity of -2.3 / -1.7 dB / 55 nm. The abstract ties them to the "optimized reflector"; p.8 says pure Al gives the improvement but also that pure Al vs 2 nm Ti shows no significant difference and pure Al is not favoured in a CMOS flow. The Fig. 8(a) curve matches neither Fig. 6(a) curve. I kept these values on a separate row for the Fig. 8 sample with the stack stated as not named (0 or 2 nm Ti), rather than on the 0 nm or 2 nm row (D159 logic). Cross-check: the merged `cmp_lit_mangal2020_downward_gc_reflector` notes attribute the 2.3 / 1.7 dB values to a 2 nm Ti grating (from that later paper); not used here (rule 1). Alternative: move the opt row values to the 2 nm row, or apply D159 and keep them in notes.
2. Facility `org_ghent_photonics_research_group` from the acknowledgment ("assistance in the deposition ... at intec Photonics, Ghent University", p.11): a stated processing place (D448), but the thanks name staff and the first author is also Ghent-affiliated (CMST). Merged mangal2020 left facility empty on its GC row. Alternative: empty.
3. Printed conflict: Fig. 6(a) label 1.7 dB (0 nm vs 5 nm Ti) vs conclusion "1.5 dB drop" (p.10); Fig. 5(b) -3.5 dB vs Fig. 6(a) 5 nm curve about -4.0 dB. Noted on the ti5 row.

## Registry gaps (skipped value + locator + proposed definition)

| proposal | skipped value | locator |
|---|---|---|
| `bw_3db_nm` / `bw_3db_ghz` widened to free_space_emitter (optical passband of an OPA / emitter) | 3.1-3.3 nm, 388-416 GHz on three dies | chung2017 p.20 Fig. 33 |
| `power_consumption_w` on free_space_emitter (D432 candidate) | 54 mW per antenna | chung2017 p.19 Table III |
| `output_power_dbm` on free_space_emitter (lit_79 candidate) | 400 mW main beam at 9.1 W input | poulton2017 p.2 |
| `l_pi_um` on splitter (cross-over length of a directional coupler) | 18 um simulated | chung2017 p.9 |
| `phase_coherence_length_mm` on waveguide_platform (length for e^-1 phase coherence, method in notes) | 2.8 mm | chung2017 p.17 |
| `directionality_pct` on fiber_chip_coupler / free_space_emitter (fraction diffracted toward the intended side) | about 90 % downward, simulated | mangal2019 p.5 Fig. 2(b) |

## Missing organizations

- The MOSIS Service (name as printed), chip fabrication support, chung2017 p.21: fab org (D398) on 14 rows.
