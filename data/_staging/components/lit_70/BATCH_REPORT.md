# lit_70 batch report (2026-11-02)

Classes: reflector, resonator (plus the waveguide, coupler and laser parts these papers characterize). Values are facts and locators only.

| Paper | Components | Metrics | Classes |
|---|---|---|---|
| liang2017 | 1 | 13 | resonator.photonic_crystal |
| saghaei2026 | 4 | 36 | resonator.bragg x3 (N = 50, 150, 300), fiber_chip_coupler.grating |
| cheng2022 | 1 | 16 | resonator.coupled_rings |
| asano2017 | 1 | 19 | resonator.photonic_crystal |
| oser2019 | 12 | 103 | reflector.band_stop (6 single-section, 6 cascaded) |
| marin2023 | 3 | 42 | resonator.ring x2, waveguide_platform.straight |
| wu2023 | 1 | 11 | resonator.disk |
| primiani2019 | 4 | 25 | reflector.bragg, waveguide_platform.straight, chip_chip_coupler.butt, laser.ecl |

## Identity check and versions

All eight cached texts are the source-row papers; none is another paper or only a correction; no paper stopped on.
- oser2019: cached text is arXiv v1 (1806.08833), titled "surpassing on-chip rejection limitations" where the source row says "Overcoming On-Chip Rejection Limitations". Same arXiv id and DOI in `source.json`, same subject; author list on p.1 (Oser ... Alonso-Ramos) fits, the source row carries no authors to compare. Distilled as the same work. Values are the preprint's: the journal version was not read and could differ (see the 80 dB check below).
- wu2023 (not in the known flags): cached text is arXiv v1 (2303.17814), titled "OH absorption" where the source row says "Hydroxyl ion absorption". Same arXiv id and DOI, same subject. Distilled as the same work.
- liang2017: arXiv v2 with the source-row title; no flag needed.

## Not entered, and why

- saghaei2026: propagation loss 2.45-4.6 dB/cm. The abstract words it as measured here; p.10 and p.13 attribute it to the authors' earlier work [40] (D259). Table I comparison rows. N = 1 is only the coupler reference. Fig. 7 de-embedded curves have no labels.
- cheng2022: Table 2 comparison rows; DC and heaters without measured values; fitted t1-t3 kept in notes rather than computed to power coupling.
- asano2017: per-cavity Table 2 values condensed to two range rows (n = 8); the earlier 4.4 and 9 million Q values are the authors' earlier work [15].
- oser2019: Fig. 3 devices (4-16 x 25, 4 x 100, 8 x 50 repeats) have no labelled values and the figure serves bandwidth trends: no rows. Fig. 2 bandwidths unlabelled. Off-band insertion loss stated only as negligible.
- marin2023: TOX rib 0.1 dB/cm [3], strip about 4 dB/m [23], converter about 0.014 dB [14] (cited); Euler-bend transmission 99.98 / 99.91 % simulated (notes only: a 180 deg bend, bend_loss_db_per_90 would need a conversion).
- wu2023: Table I literature rows; absorption series of Fig. 2 other than the two Table I points.
- primiani2019: targets (1 dB/m, 0.5 dB, below 17 kHz); threshold only visible in Fig. 7(a).
- liang2017: Fig. 4(d) resonance-vs-geometry series (no Q).

## Missing organizations (checked in `organizations.csv` and `org_aliases.csv`; fields left empty)

| As printed | Locator | Would go in |
|---|---|---|
| University of Alberta | saghaei2026 p.1, p.8 Sec. V-A ("we fabricated") | fab on 4 rows |
| VTT Technical Research Centre of Finland | marin2023 p.1, p.3 Sec. III (MPW run at VTT) | fab on 3 rows |
| Plateforme de Micro-Nano-Technologie/C2N | oser2019 p.8 | facility on 12 rows |
| RENATECH network | oser2019 p.8 ("partly supported") | facility, or a program acknowledgement: coordinator's call |
| Kavli Nanoscience Institute (KNI) at Caltech | wu2023 p.3 | facility |
| Caltech Microanalysis Center | wu2023 p.3 (SIMS support) | facility, if counted |

## Registry gaps (skipped value + locator + proposed definition)

1. reflector: `thermal_drift_pm_per_k` (primiani2019 15 pm/C, p.2), `tuning_range_nm` (about 1.5 nm, p.1, Fig. 4), `tuning_power_mw` (1.98 W, p.3; entered only on the laser row), `center_wavelength_nm` (about 1543.93 nm, Fig. 3), heater geometry `heater_*` (10 nm Ti + 100 nm TiN, 6 um; p.2). Proposal: allow these for reflector.
2. resonator `stopband_width_nm` (saghaei2026 N = 300 simulated about 13 nm, p.7). Proposal: allow for resonator.bragg, level in condition.
3. `mode_volume_lambda_n3`: effective mode volume in (lambda/n)^3 (liang2017 1.03 / 1.80, p.4) and cubic material wavelengths (asano2017 1.4, p.3). Proposal: resonator, performance, normalization in condition.
4. `q_absorption`: absorption-limited Q (wu2023 8e9, p.2-3; asano2017 Avg(1/Qabs) about 5.8e-8, p.9). Proposal: resonator, method in notes.
5. `slope_rate_db_per_nm`: Fano slope (cheng2022 about 8.1e4 dB/nm, p.7, Fig. 5(b)).
6. `photon_lifetime_ns` (asano2017 9.2 ns, p.6). Optional: equivalent to Q.
7. Hole radius of a photonic-crystal lattice (asano2017 110 nm, p.3): `radius_um` is a ring / disk radius. Proposal: `hole_radius_nm` for resonator and reflector.
8. Optomechanical and photorefractive values (liang2017 1.003 GHz, Qm 1465, g0/2pi 71 kHz, p.10; 0.64 GHz/aJ, p.9): single paper, no proposal.
9. Resonance shift per drive current (cheng2022 about 0.23 pm per 0.1 mA, p.8): single value, no proposal.

## Judgment calls for the auditor

1. oser2019 "at least 80 dB" (p.6) vs Fig. 4: reference waveguide near -13.5 dBm, PD B floor near -88 dBm, about 74.5 dB apart. Entered as stated with the discrepancy in notes.
2. oser2019 class `reflector.band_stop`, not `reflector.bragg`: the TE1 back-reflection is radiated, so the part works as a notch (merged baghban2017 band-rejection filters are `reflector.bragg`). Rejection on the 11 Fig. 2 rows is figure-read (+/- 1 dB); the three noise-floor points carry qualifier `ge`.
3. oser2019 fab org_centre_de_nanosciences_et_de_nanotechnologies from the contribution statement (D.O., X.L.R.; both at C2N).
4. saghaei2026 class `resonator.bragg` although the title says filter (D400 keeps `wdm` for channel filters in a WDM path). Platform `soi` as the paper calls it, though Sec. V-A describes amorphous Si on PECVD oxide. N = 300 "exceeding 60 dB" has no stated reference level, and Fig. 6(e)'s floor is absolute. N = 50 row exists only through a figure read of Fig. 6(c).
5. cheng2022 fab org_lionix_international from a fabrication sentence naming the TriPleX ADS technology of LioniX (p.5). Merged theurer2020 stays empty (its text attributes no fabrication); empty here is defensible if the sentence is read as naming a platform only.
6. asano2017 Qexp entered as `q_loaded` (photon lifetime includes the excitation-waveguide load) with band `cl_band` inferred for cavities whose wavelength is not stated. Merged ashida2017 derives q_intrinsic through a transmission model; this paper gives no such relation.
7. marin2023 q_intrinsic `measured`: Qext comes from the same drop-port fit, so D403 is taken as satisfied; the model assumes symmetric couplers. Rib loss 2.7 dB/m gets its own `waveguide_platform.straight` row (`author_estimate`) because the paper ties it to both racetracks. TE mean on the large racetrack takes the wavelength range from the TM half of the sentence (`wavelength_inferred`). Fig. 11(b) 32.63 MHz is a figure label, entered `measured`.
8. wu2023 all Q rows `author_estimate` (D403: regime not stated). The Q list at 685, 780, 1064 nm is unqualified in its sentence; entered as q_intrinsic because Fig. 1 contours follow the Q0 formula, contrary to the plain unqualified -> q_loaded default. Absorption-only loss entered under `prop_loss_db_per_cm` with the condition saying so (merged wang2024b precedent).
9. primiani2019 laser row carries the 1.98 W heater power measured for the grating chip (gap 1). Coupler 2.5 dB `simulated` (computed overlap), though the paper says estimate. Fab of the grating from the acknowledgment sentence that names the LETI platform as fabricating the passive devices (thanks wording, but a fabrication statement).
10. liang2017 Q values `q_loaded` per the default; geometry is nominal because the device width behind Fig. 4(a)-(c) is not stated. Facility CNF; fab empty (D80b).

## Text inconsistencies noted in rows

asano2017 6.3 vs 6.2 million and 1565.30 vs 1565.33 nm (p.5 vs p.7). marin2023 Qi 14 vs 14.3 x 10^6 (abstract vs body), anneal 70 vs 80 Torr (p.3-4). oser2019 text p.6 lists 4, 6, 8 sections where Fig. 3(b) has 4, 8, 16. primiani2019 tuning "nearly" vs "more than" 1.5 nm (p.3 vs p.4). saghaei2026 SOI vs amorphous Si (p.3 vs p.8).
