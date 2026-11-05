# lit_80 batch report (phase_shifter, photodetector, waveguide_platform), 2026-11-04

All seven cached texts match their source rows (page-1 title); no correction, erratum or wrong paper. No garbled text layer. stanfield2019 and blundell2025 are preprint texts (`arxiv_id` on the source row); journal versions unread (D430, D433). Dry-run: +42 components, +231 metrics, 0 errors (the one warning is on merged row `cmp_lit_ni2025b_pimmwc-m18`, not this batch).

| paper | components | metrics |
|---|---|---|
| stanfield2019 | 9 (phase_shifter.other x5 incl. 1 design row, resonator.ring x2, waveguide_platform.bend, waveguide_platform.straight) | 45 |
| blundell2025 | 14 (phase_shifter.phase_change x5, waveguide_platform.straight x5, splitter.mmi x4) | 34 |
| srinivasan2020 | 4 (photodetector.apd, fiber_chip_coupler.grating x2, waveguide_platform.transition) | 27 |
| vines2019 | 4 (photodetector.spad x4) | 40 |
| shahin2025 | 1 (photodetector.apd) | 31 |
| akritidis2026 | 9 (waveguide_platform.straight x3, waveguide_platform.transition x3, reflector.loop_mirror x2, laser.heterogeneous) | 47 |
| wang2023d | 1 (waveguide_platform.straight) | 7 |

## Not entered, and why

stanfield2019
- Thermo-optic comparisons (0.62 mW p.12, 38 mW p.13, 19.7 mW p.15): cited coefficient of ref. 14. AlN and PZT values of other works: cited.
- Rings with > 20 dB extinction and lower Q (p.9): no sample identity (D159). 0.5 GHz photon-lifetime cutoff and half-diameter scaling (p.11), 1.3 cm / 18 V MZM (p.12): projections.
- Fig. 4(b), Fig. 11(c) simulated curves: no parameter, no single printed design point except 233 MHz (entered). Grating couplers and MMIs: no values, no rows.
- 7 K values: 0.26 GHz/V on a separate row because the paper does not say which release state was cooled. Resistance values, leakage, relative path-length shift, LVpi, energy per bit: no parameter, in component notes.

blundell2025
- Phase shift per um and FOM of Table 1: no parameter, in notes per row. Phase_shift_pi not used: the paper gives no total shift, and 50 um x rad/um would be an unprinted product.
- Amorphous-state loss: near zero or negative (Fig. 1(d), (e)), no printed value; loss is stored positive.
- Amorphous-pixel MMIs (Fig. 3): T / T0 rises against the crystalline start (about +0.4 to +1.6 dB), no loss row; port contrast (Figs 3-5) has no parameter, last-pixel reading in notes of the crystalline-pixel rows. 60 nm MMIs and 10 / 20 nm buffer samples: supplement not cached. Text prints the buffer as 10 nm (p.9) and 20 nm (p.19).
- Waveguide width, MMI dimensions: not stated (pixel-map axes are not dimensions, skill rule on figure labels).

srinivasan2020
- ~0.86 A/W and > 50 GHz p-i-n of ref. [1], absorbed fractions 95 / 99 % (ref. [1]), Table II other works: cited. Coupling efficiency 0.74: same value as the 1.3 dB row, in notes. Failure beyond -13 V: no breakdown criterion, in notes. Eye SNR: no parameter.

vines2019
- NEP, cut-off wavelength, activation energy, yield, punchthrough voltage, dead-time reduction: no parameter, in notes. Warburton and Martinez values: cited. 2 um Ge and 10 um device predictions: projections. Normalised SPDE vs wavelength (Fig. 5(a)): no absolute values.

shahin2025
- Eye SNR, BER, total jitter, k_eff about 0.1: no parameter, in notes. Reliability values (p.1): attributed to ref. [12]. Table I other works: cited. Doping and E-field values: no parameter. Fig. 7 five-die scatter: not per-device identifiable; in notes.

akritidis2026
- 17 dB/cm at 970 nm and 0.17 dB (p.5): the authors' ref. 32. 50 % reduction against ref. 32 (p.10): cited. 800 nm lasers of ref. 24: cited. Fig. 1 devices: micrographs from ongoing work, no values. Grating couplers: no isolated value, no row. 60 nm SiN: geometry only (rule 9). Recess sidewall 85.24 deg (p.8): not a waveguide; ellipsometry n / k curves: no parameter.

wang2023d
- Grating couplers GC-1 to GC-5 and rings: Fig. 4(a) shows only total path loss; no coupler value printed, intercepts not read. Slab thickness not printed (400 - 100 nm not entered). Table 1 other works: cited.

## Missing orgs (registry)

- University of Glasgow (School of Engineering): vines2019 p.9 author contributions name three fabricators at this org, p.1 affiliation. fab_org_ids empty on the 3 Ge-on-Si rows; add alias and set fab after the org round (he2025 / D439 construction).
- Ferdinand-Braun-Institut (FBH), Berlin: akritidis2026 p.13 acknowledgment (growth and processing of the III-V gain chips), p.1 affiliation. Would go on `gaas_on_sin_fp_laser` and `asi_to_iiiv_taper`.
- NANOLN: wang2023d p.1, wafer supplier, note only (rule 12), no row effect.

## Registry gaps (skipped value, locator, proposed definition)

- `phase_shift_rad_per_um` (phase_shifter): blundell2025 Table 1 (0.116 to 0.600 rad/um), chen2024a precedent. Phase shift per unit length of the switched PCM.
- `vpi_l_v_cm` (phase_shifter; candidate already in D438): stanfield2019 24 V cm (p.12), Fig. 11(c).
- `energy_per_bit_pj` (phase_shifter; khope2019 candidate for switch_fabric): stanfield2019 0.52 pJ/bit and 6.6 nJ/bit.
- `leakage_resistance_ohm` (phase_shifter): stanfield2019 500 GOhm and 40 GOhm at room temperature, > 20 TOhm at cryogenic temperature.
- `port_contrast` (splitter, unitless): blundell2025 Figs 3-5, with the definition in condition.
- `nep_w_per_rthz` (photodetector): vines2019 1.9e-16 to 7e-16 W/Hz^0.5 (p.4), 7e-17 (p.6). Noise-equivalent power of a single-photon detector.
- `cutoff_wavelength_nm` (photodetector): vines2019 1468 / 1495 nm (p.5). Wavelength at the stated fraction of a reference response.
- `ionization_ratio_k` (photodetector): shahin2025 about 0.1 (p.7).
- `fsr_nm` already allows photodetector, not phase_shifter: blundell2025 MZI FSR 3.208 nm, 0.41385 THz (p.9), a test-MZI value in the row notes only if ruled; not entered.

## Judgment calls for the auditor

1. Piezo-optomechanical AlN actuators as `phase_shifter.other` (dong2021 precedent), not `.mems`. stanfield2019 rings: one phase_shifter row and one resonator row per device (D396).
2. stanfield2019 q_intrinsic: 1.5e6 and 1.8e6 `author_estimate` (D403; regime stated, or assumed with stated ambiguity). 2.2e6 `measured` from the doublet fit (D80a); downgrade if the fit is held not to fix the regime.
3. stanfield2019 v_pi_v 20 V: the paper's own arithmetic for LVpi (24 V cm) uses 40 V across 6 mm, so 20 V is a per-arm amplitude; condition says so. Tuning efficiencies converted from MHz/V at 780 nm, cross-checked against the Fig. 8(b) and Fig. 9(b) upper axes (0.4 and 0.96 pm/V). 0.4 dB/cm as a separate `waveguide_platform.straight` row, `author_estimate`, instead of notes (stated for the rings in general).
4. stanfield2019 p.15 200 fW combines a 7 K resistance of an unspecified ring with the non-undercut hold voltage, as the paper does; `derived` on the non-undercut row.
5. blundell2025 `length_um` = calculated L_pi (derived, not a physical length) so the series stays comparable; 50 um patch in notes. IL rows: 0.08 and 0.62 dB printed, the other three computed alpha x L_pi as the same arithmetic. Fab org_cornerstone from Methods (p.19) for the waveguides; PCM deposition on chips is passive, no extra org.
6. blundell2025 MMI rows have only figure-read T / T0 loss, scope `on_chip_excess` relative to the device before writing; wavelength inferred 1550 nm.
7. srinivasan2020 Fig. 5 caption attaches ref. [14] (authors' ECOC 2019) after "(b) 1550 nm". Under D259 / D408 the 1550 nm RF rows may be the earlier paper's: `bw3db_ghz` 32 and 5.5 (Fig. 5(c) reads), `avalanche_gain` 8.5. Kept because the text sentence and Fig. 5(c), (d) carry no attribution. Coordinator ruling requested. Fab org_imec from the acknowledgment naming the 200 mm pilot line as contributing to fabrication.
8. srinivasan2020 grating coupler 6 / 8.5 dB `unspecified` scope (per coupler or pair not stated). Dark current: text about 10 nA at -2 V against Fig. 3(c) median about 60 nA; both entered.
9. Fab consistency. shahin2025 (fabricated on imec's 300-mm platform, passive): empty, per D84a / D433 szelag2017. akritidis2026 (wafers fabricated on a 200 mm pilot line at imec): org_imec, because the sentence places fabrication at the org rather than naming a platform. These two are close; rule on both together. wang2023d: empty, foundry unnamed.
10. vines2019 commercial InGaAs/InP SPAD kept as a comparison row (D155, reference structure with own numbers), vendor unnamed; delete if comparison devices are held to be setup equipment (rule 13). SPDE stored in `quantum_efficiency_pct` (qi2024 precedent). 24 SPDE / DCR points of Fig. 3 entered as operating points; DCR at the two printed density values `derived` with the area, excess bias paired by the SPDE reading. Platform empty: no guided stack (D423).
11. akritidis2026 transition platform `si_sin_multilayer` for a-Si:H on SiN, `other` for the a-Si:H waveguide (chiles2017 used `other`) and for the a-Si:H to III-V taper. Mirror transmission stored as `extinction_db`; `reflectivity_pct` only as design-stated `author_estimate`. n_samples 49 for 0.23 dB/cm is 51 minus the 2 unmeasurable dies. Laser on-chip powers `derived` (D394).
12. Statistic `wafer_map` on values printed with +/- across dies (srinivasan2020 17 dies, shahin2025 15 dies); the kind of spread is not stated, so no `std` rows.
