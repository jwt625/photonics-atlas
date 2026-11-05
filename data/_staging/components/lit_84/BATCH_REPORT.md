# lit_84 batch report (verified_on 2026-11-04)

All five cached texts match their source rows (page-1 titles checked); none is a correction or another paper.
Dry run: +39 components, +277 metrics, 0 errors (one WARN on an already merged row, `cmp_lit_ni2025b_pimmwc-m18`, not this batch).

| Paper | Components | Metric rows |
|---|---|---|
| boerma2026 | 5 | 21 |
| heermeier2025 | 19 | 105 |
| bai2023 | 3 | 52 |
| hossain2026 | 3 | 49 |
| hoffman2016 | 9 | 50 |

## boerma2026

- Rows: Sagnac SGDBR SIL, its intracavity ring (`resonator.ring`, D400), Sagnac DFB SIL, MMI DFB SIL, reference DFB.
- Not entered: FMCW chirp range, rms error, residual frequency error, nonlinearity (registry gap below; values in component notes). Table I other-work rows and refs [11]-[14] (cited). MMI / Sagnac reflectors and on-chip photodiodes (no performance number; Fig. 6 photocurrent is a tuning trace).
- Paper inconsistencies, flagged in notes: MMI DFB chirp range 6.29 GHz (p.5, Fig. 11) vs 6.85 GHz (p.6 Table I, conclusion) vs 6.8 GHz (p.1); SGDBR tuning range 30 nm (text) vs 32 nm (Fig. 4 caption, and the printed 1550-1582 nm span). Entered 30 nm with the span.
- Judgment calls: ring Q (about 10000, the paper's word is "estimated") and FSR (about 25 GHz, no measurement shown) `author_estimate`. Reference DFB: platform and fab empty (D422; the paper does not say which chip). Thresholds and free-running power read from Fig. 3, `extracted_from_figure`. DFB rows `band: unspecified` (no DFB wavelength printed).
- Fab: `org_fraunhofer_heinrich_hertz_institute` ("HHI's MPW foundry runs", p.2). Facility: none.

## heermeier2025

- Rows: Table I devices (8 distinct designs), the devices the text ties to values (Fig. 9/22, 15, 20, 23, 24), a population row for values with no device, the 15.5-pair double-DBR reference, and two top-DBR `reflector.bragg` rows (15.5 pairs on the reference, 14.5 pairs calculated, `row_kind: design`).
- Not entered:
  - R_G group values and ref. [16] / [19] values (1.44 mW, 1.3-1.5 mA, Rth 0.63 K/mW): earlier work, D259a. Rth > 3 K/mW and 0.078 nm/K: cited.
  - Rth 2.34 / 2.45 K/mW and slopes 0.21 / 0.22 nm/mW: the small and medium devices have no stated F, D159, kept in the population row notes.
  - SMSR 43-46 dB "commonly measured" and WPE 6-7% mid-cluster: family statements, D254, notes.
  - Fig. 8 / 17 / 21 maps (colour only), Fig. 12 / 13 sweep ranges (values span designs), simulated Q maps, Q 6774.
- Paper inconsistencies, flagged in notes (please weigh these in audit):
  - Lowest threshold: 0.25 mA (abstract, p.14) vs 0.27 mA (p.9, p.20, Table I). Entered 0.27.
  - Table I devices 1 and 3 share P, H, aperture, Ith, Pmax but list F 68% / 64%; p.7 gives F 68% for the 33 dB OPSR device. Entered as one row, F 68%.
  - Rth 2.46 K/mW: Table I assigns it to one device (F 60%); p.16 calls it the 6 um average (2.34, 2.45, 2.6 do average 2.46). Entered on the Table I device with the note.
  - Large-tuning device: slope 0.24 nm/mW (p.16) vs 0.22 +/- 0.008 (Fig. 19(b)). Both entered with cross-notes.
  - Device 6: F 62% / H 329 nm (Table I) vs F 63% / H 328 nm for the single-mode column (p.18). Kept as printed, separate rows.
  - 85 C (text) vs 80 C (Fig. 18 caption). Top-DBR reflectance: 99.43% at 14.5 pairs, 99.3% at 15.5 pairs, about 93% on p.9. Entered 99.43 and 99.3 as printed, `simulated`; the two are not monotonic with pair count.
- Judgment calls: grating height H as `etch_depth_nm` (H < 341 nm MHCG layer, per-device), basis `measured` with "estimated" quoted (etch-rate calibration plus top-view SEM; rule 4 test-structure clause; `author_estimate` is the alternative). Population row uses D165. Rth from K/mW and slopes from nm/mW `derived` (D256). Oxide aperture only in the label (registry gap). Bands inferred from the 980 nm design resonance.
- Fab: not entered. "We ... fabricated" with authors at TU Berlin and Lodz University of Technology and no split stated (D395 needs an unambiguous org). Lodz University of Technology is not in the registry (name as printed, p.1) but no row needs it.

## bai2023

- Rows: AWG (measured + simulated + geometry), parabolic wedge taper (`waveguide_platform.other`, simulated, on the chip), linear taper (`row_kind: design`, simulated comparison).
- Not entered: measured channel crosstalk (not stated; Fig. 8 overlap makes a per-channel read unreliable; leakage levels in notes), measured 3-dB widths (not stated, rippled spectra), simulated channel spacing (paper says the simulation accuracy is insufficient for it; the per-channel wavelengths are kept as conditions of simulated IL), simulated taper crosstalk (registry gap), 16-channel footprint projection, TE / TM input grating couplers (no performance stated), ref. [17] EDG.
- Judgment calls: IL scope `unspecified` (spectra "normalized", reference not stated; Fig. 6(a) shows a reference grating, not used as evidence). Per-channel IL from Fig. 8 `extracted_from_figure` +/-0.3 dB, on top of the < 3 dB statement. Simulated PER entered as `extinction_db` because `per_db` is not allowed on `wdm`. No second `polarization.pbs` row (D396): the only polarization number is simulated.
- Fab and facility: none. Thanks to named staff at SJTU AEMD and a Zhejiang University training platform are staff thanks, not entered.

## hossain2026

- Rows: 1x13 AWG, bilayer GC (loopback), FN waveguide (cutback).
- Not entered: Table I other-work rows; 1x16 extension (projection); spiral waveguide width (not stated separately).
- Paper inconsistencies, flagged in notes: crosstalk range 31-41 dB (text) vs Fig. 5(c) labels reaching -45 dB; center-die bandwidth 118.6 GHz (text) vs 121 GHz label at die 0-0 in Fig. 5(e). Operating range 1500-1620 nm (abstract) vs plotted 1500-1600 nm.
- Judgment calls: AWG IL `derived`, scope `de_embedded` (measured minus the loopback GC loss). GC 6.0 dB `derived`, `loopback_half` (halved from 12 dB total). 0.59 dB total and 0.14 dB array `author_estimate` (nominal 0.25 cm length). `crosstalk_db` rather than `crosstalk_adjacent_db` (type not stated). Fig. 5(a) values at 1520 / 1580 nm `extracted_from_figure`. Fig. 2 labels used for 2.32 um oxide and SN thickness.
- Fab: `org_aim_photonics`. **Missing org:** "Albany Nanotech Complex" (p.1 abstract, p.3 Sec. IV), not in `organizations.csv` / `org_aliases.csv`; `facility_org_ids` left empty, named in `process_name` and notes.

## hoffman2016

- Rows: straight waveguides (average row + widths 1-5 um), bends (1 um, 5 um), grating coupler.
- Not entered: Gorin et al. and ref. [12] losses (cited; 0.9 dB/cm is an extrapolation of ref. [1]), Fig. 9 power density and 12 uW output (registry gap, notes), Fig. 11(b) per-radius A values (mixed coupling and transition terms; only the grey system-efficiency band entered), Fig. 12 decay length and Fig. 5 extraction length (registry gap, notes), Eq. 1 cut-off height as a metric (only the chosen 180 nm).
- Paper inconsistency: fiber-setup mean 1.23 dB/cm (text) vs Fig. 8(b) dashed line about 1.35; Fig. 11(a) rightmost points sit beyond the 1000 um tick while the text gives 25-1000 um; coupler 5 x 9 um vs 5 x 10 um (p.9). Notes carry these.
- Judgment calls: 0.045 dB bend loss and 0.2 dB transition `derived` (own average subtracted). The 0.2 dB goes in `insertion_loss_db` `per_component`, not `bend_loss_db_per_90`, because Sec. 3.4 defines it as a straight-to-bend transition term; the abstract calls it bend insertion loss per 90 deg. Uncompensated alpha per radius entered as `prop_loss_db_per_cm` `extracted_from_figure` +/-15%. `fill_factor` 0.5 is 1 - 0.5 per D253 (paper defines the groove fraction). `fiber_angle_deg` 10 is an angle in the oxide, condition says so. Coupler used with a fiber and a laser diode; one `fiber_chip_coupler.grating` row.
- Fab: not entered (passive sentence; authors at imec, KU Leuven, Ghent University). No facility.

## Registry gaps (values skipped, proposed definitions)

1. `chirp_range_ghz` (laser, GHz): peak-to-peak optical frequency excursion of a direct FMCW sweep at the stated period. boerma2026 p.5 Sec. IV: 1.8 GHz (SGDBR, 32 us), 6.29 GHz (MMI DFB), 3.34 GHz (8 us); p.6 Table I 6.85 GHz.
2. `chirp_rms_error_pct` (laser, %): rms frequency error relative to chirp range in the stated ROI. boerma2026 p.5: 2.61%, 0.12%, 0.23%.
3. `threshold_current_density_ka_per_cm2` (laser, kA/cm2). heermeier2025 p.19 Table I 0.79; p.12 0.78.
4. `oxide_aperture_diameter_um` (laser, geometry): oxide-confined VCSEL aperture. heermeier2025 throughout (label only for now).
5. `rollover_current_ma` (laser, mA): current at thermal rollover. heermeier2025 p.9 Fig. 8(d) maps, p.11 6-11 mA across designs.
6. `decay_length_um` (fiber_chip_coupler / free_space_emitter, um): 1/e out-coupling length of a grating. hoffman2016 p.11 Sec. 3.5: 3.78 +/- 0.76 um; p.6 simulated 90% extraction length 10.91 um.
7. `output_power_density_mw_per_mm2` (free_space_emitter / fiber_chip_coupler). hoffman2016 p.9 Fig. 9: 241-261 mW/mm2; abstract 240.
8. `crosstalk_db` not allowed on `waveguide_platform`: bai2023 p.3 Fig. 4(e),(f) wedge-taper coupling, simulated, about 35 / 32 dB (parabolic) and 28 / 25 dB (linear).

## For the coordinator

- Whether the heermeier2025 population row (D165 reading) and the two top-DBR reflector rows stay, and whether H goes as `etch_depth_nm` `measured`.
- Add the Albany Nanotech Complex org and fill `facility_org_ids` on the three hossain2026 rows (no fabrication statement beyond AIM's process there, p.1 and p.3).
