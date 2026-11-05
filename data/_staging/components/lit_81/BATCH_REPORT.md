# lit_81 batch report

Distilled 2026-11-04. Classes: reflector, resonator, splitter, mode_converter. Dry-run: 0 errors (the one WARN is the merged row ni2025b, not this batch).

| Paper | Components | Metric rows | Content |
|---|---|---:|---|
| wu2018 | 16 | 136 | 15 Si cascaded Sagnac loop reflector resonators (N = 3, 4, 8), 1 grating coupler |
| yasui2026 | 12 | 56 | 11 Si microrings (R / W series), 1 grating coupler |
| zhang2026c | 2 | 24 | TFLN single-ring photonic molecule racetrack, 1 grating coupler |
| reniers2019 | 18 | 106 | 7 PhC reflectors 700 nm, 6 Fabry-Perot cavities, 4 PhC reflector designs 400 nm, 1 waveguide |
| wang2016a | 5 | 31 | 4 fabricated SWG directional couplers, 1 design row |
| probst2023 | 3 | 15 | 2 SiN mode converters, 1 SiN width taper |
| Total | 56 | 368 | |

## Boundary event

One helper call used `uv run --with pillow` to crop a figure. The uv cache timestamp for the pillow index entry (`simple-v16/pypi/pillow.rkyv`, 2026-11-04 18:26:27, about a minute before it was checked) indicates a package-index metadata request, against the no-network rule. It carried no paper data and no personal identifier. Every later uv call used `--offline`; no data in this batch depends on that crop tool beyond the Fig. 3(f) view of yasui2026, which is a crop of the cached page render.

## Per paper

### wu2018

Page-1 title reads "Silicon photonic filters based on cascaded Sagnac loop resonators" (arXiv text); the source row carries the APL Photonics title. Same authors and work by arXiv id on the row; the journal version was not read (oser2019 / wu2023 precedent, D430).

Not entered:
- Assumed ng = 4.3350 and alpha = 55 /m (2.4 dB/cm): from the authors' earlier devices, rule 3.
- Peak insertion loss off Figs. 7-9: spectra are normalized after removing the ~6 dB per coupler term, so the 0 dB level rests on that estimate.
- Sagnac loop reflector as `reflector.loop_mirror` and the directional coupler as `splitter`: only fit field coefficients t, no reflectivity or coupling value printed; t values are in component notes.
- Sec. II calculated filter sweeps (Figs. 2-5), apart from the over 10 dB of the Fig. 5(f) design on the Fig. 9(d) row. Group delay ratio 2.1: no parameter (notes).

Judgment calls:
- Class `resonator.photonic_crystal`: the registry definition includes Fabry-Perot cavities and the paper describes N - 1 cascaded FP cavities. `resonator.other` is the alternative.
- Fit alpha and ng `measured` (standard fit of own data, D80a). Method `ring_extraction` for a standing-wave resonator fit, the nearest enum.
- Fab org_swinburne_university_of_technology from "We fabricated", single affiliation (D399), next to the MCN fabrication-support acknowledgment.
- GC ~6 dB `author_estimate`: only a subtraction term (D418, D444).
- Extinction and FSR read off the figures (`extracted_from_figure`); extinction defined as highest peak to deepest valley in condition.

Source inconsistencies kept in notes: L2 = 295.33 um (caption, text) vs 259.33 um (Table II) for Fig. 8(b); p.12 text says "Fig. 8(b)" for the Fig. 9(b) device; the Fig. 8(a) L2 = 100 um device has the same nominal t as Fig. 7(a-ii), identity not stated, kept as its own row.

### yasui2026

Supporting Information is not cached: A1 per-ring spectra and fits, A3 loss correction, A6 comparison not read.

Not entered:
- SNSPD, WDM couplers and filters of the setup (rule 13).
- Qs from earlier work in the introduction (rule 3).
- Extinction off Fig. 3(d): wide scan, sampling of narrow resonances unknown.
- Micrograph labels on the embedded image (gap and period text on the layout, Fig. 3(a) source image): layout text, not dimensions the paper states. Gap G has no printed value.

Judgment calls:
- `q_intrinsic`, `q_external` and the 0.526 dB/cm `author_estimate` (D403): the resonances are "close to critical coupling" and the fit form does not separate under- from over-coupling. Coordinator may prefer `measured` because Q_int and Q_c are both fit and nearly equal. `q_loaded` and FWHM stay `measured`.
- Fit wavelength left as `c_band`, inferred: the value is not tied to one of the three resonances of Fig. 3(e).
- GC 32 % (5 dB) `measured` under D167, stated directly per coupler; Fig. 3(d) baseline supports it. Could be `author_estimate` under D437 since it also corrects the pair rates.
- Fig. 3(f) rows read off a log axis (+/-15 %); the read of the R 40, W 1.5 point is below the printed 0.526 dB/cm by about the same margin.
- Fab empty: first-person statement, authors at NTT and Hokkaido University, site not stated.
- Table 1 brightness coefficient 3962 vs text 3692 for R = 40: flagged in notes.

### zhang2026c

Not entered:
- Photorefractive and mmWave figures without a parameter (listed under registry gaps, values in the racetrack notes).
- Representative doublet fits 1.60 / 3.39 / 5.09 GHz (Supp. Fig. S7): examples of the same series.
- Simulated group indices and the TE2 absorption-limited Q ~3e5: simulated for a mode the paper excludes.
- Cited literature values of the introduction (rule 3).

Judgment calls:
- `resonator.ring`: one racetrack, not `resonator.coupled_rings`.
- 2g_inf = 2.38 GHz `author_estimate` (D435, asymptote past the two-hour data window). 2g0 = 5.69 GHz `measured`, peak of a fit inside the data range.
- FSR 35.3 GHz `derived` from the printed "three FSRs ~106 GHz".
- Fig. S8(a) splittings `measured`: printed as figure labels.
- Etch depth and sidewall angle `design_target` with `approx`: process results, measurement not stated.
- Fab org_epfl (author contributions, D395); facility org_center_of_micronanotechnology.
- GC platform lnoi_rib taken from the chip's photonic layer; grating etch not stated.

### reniers2019

Not entered:
- Fig. 12 / 13 / 15 points at other wavelengths: 1532 nm chosen to match Table II and because it holds the Q maximum.
- MMI power coefficient ~0.5 (model input, p.4) and grating couplers (no value).
- 400 nm reflector below 50 % for a 40 nm hole deviation: N not stated (D159), in component notes.
- Quality factors from earlier work (rule 3).

Judgment calls:
- D396: each N is one reflector row and one cavity row, cross-noted.
- 15,911 +/- 511 is printed without N: tied to N = 10 by the highest point of Fig. 13, wavelength inferred. Reflector length 4 um tied to N = 10 the same way.
- Table II measured R -> % as `derived` (D256); simulated R keeps `simulated` with the printed fraction in notes (thiessen2020 precedent).
- FP and direct values are lower and upper bounds per the paper; both kept with the bound stated in notes.
- 400 nm designs `row_kind: design`: the paper gives measurements only for 700 nm and does not say 400 nm reflectors were on the chip (D80e would flip them if they were).
- Fab org_eindhoven_university_of_technology: first-person process account, all authors at TU/e IPI (D399).
- Cladding: air above and SiO2 / BCB below from Fig. 1.

### wang2016a

Not entered:
- Conventional DC simulated with w = 450 nm, g = 220 nm: only L_pi and neff curves, no registry parameter.
- Fig. 8 IL at fill factors other than 0.28: design sweep.
- Waveguide width w of the SWG couplers: not stated. NG and gap of the 40/60, 30/70, 20/80 couplers: not stated.
- Fill factor 0.28, NG = 47, t = 500 nm: not allowed on splitter, in component notes (registry gaps).

Judgment calls:
- Printed "imbalance of +/-0.7 dB" and "+/-0.55 dB" entered as `imbalance_db`. Fig. 10(b) shows the +/- sits around -3 dB (port separation about 1.4 dB at 1600 nm), which is close to the D401 split deviation. The paper calls it imbalance, and merged gonzalezandrade2019 imbalance rows with +/- values exist. Coordinator question 1.
- Actual Si thickness 206 nm `measured` as printed; method not stated.
- Fig. 7(b) / Fig. 8 simulated IL entered as `excess_loss_db` read from the figure, a 2x2 value beyond the split; note says simulated.
- Fab empty: "fabricated by the Washington Nanofabrication Facility at the University of Washington"; facility missing from the registry (org round per D420). org_university_washington exists but is the owner, not the named fabricator.

### probst2023

Not entered:
- Below 0.15 dB transmission difference across the band: `wdl_db` not allowed on mode_converter (D428 candidate), in notes.
- Crosstalk: the paper says it is not measured.
- Fig. 1(b) structure totals: per-structure, slope entered instead.
- Si grating couplers, Si-SiN tapers, bends: no values. Fiber-array pitch: setup.

Judgment calls:
- p.1 labels both simulated converters TE00 to TE01; the 0.26 dB value goes on the TE02 row, tied by Fig. 3(b) and the sentence order, flagged in notes.
- 0.32 / 0.52 dB at wavelength 1550 from Fig. 1(b), which labels the slope at 1550 nm; Figs. 2(b) / 3(b) peak near 1550-1580 nm with slightly different readings. Statistic `best` per "peak".
- Taper as `waveguide_platform.other` (same layer, width change, TE00 preserved).
- Fab org_globalfoundries: process named for the devices (rule 12 foundry clause, D434).

## Missing organizations

- Melbourne Centre for Nanofabrication (MCN): wu2018 p.13, fabrication support, facility, 16 rows.
- Swinburne Nano Lab: wu2018 p.13, characterisation support, facility candidate, 16 rows.
- Nanolab at TU/e (printed with an at-sign, spelled out here so e-mail scans stay clean): reniers2019 p.6, cleanroom use, facility, 14 fabricated rows.
- Washington Nanofabrication Facility: wang2016a p.9, "fabricated by", fab, 4 rows (already on the D417 / D420 org-round list).

## Registry gaps

| Proposed parameter | Definition | Skipped value | Locator |
|---|---|---|---|
| `pair_generation_rate_mhz` | photon-pair rate on chip at the stated pump | 9.19 MHz @ 240 uW | yasui2026 p.8 Table 1 |
| `pair_rate_coefficient_mhz_per_mw2` | low-power quadratic coefficient | 1286.7 +/- 21 | yasui2026 p.8 Table 1 |
| `pair_brightness_mhz_per_ghz` | pair rate per bandwidth | 22.0 @ 240 uW | yasui2026 p.8 Table 1 |
| `car`, `two_photon_visibility_pct` | coincidence-to-accidental ratio; Franson visibility | 2175 +/- 100; 98.0 +/- 0.2 | yasui2026 p.7, p.9 |
| `coupling_bandwidth_ghz` (resonator) | FWHM of an intermodal coupling envelope | 0.71 +/- 0.02 THz | zhang2026c p.8 Fig. 2(c) |
| `retention_time_s`, `endurance_cycles` widened to resonator | relaxation of a written state; write cycles | 65.2 +/- 0.8 min; 7 cycles | zhang2026c p.9 |
| `sideband_suppression_db` | single-sideband suppression of a transducer | 16.1 / 25.8 / 22.2 dB | zhang2026c p.12 |
| `hole_diameter_nm` widened to reflector (D431 candidate) | hole size along a stated axis | 270 x 180 nm; 173 x 248 nm | reniers2019 p.2 Table I |
| `fill_factor`, `n_periods` widened to splitter | SWG fill factor; grating periods | 0.28; 47 | wang2016a p.8 |
| `wdl_db` widened to mode_converter (D428 candidate) | wavelength-dependent loss | below 0.15 dB | probst2023 p.2 |

## Coordinator questions

1. wang2016a printed "imbalance of +/-x dB", which Fig. 10(b) shows as a deviation around -3 dB: keep as `imbalance_db` (recommended, the paper's own term, with the note) or remove under D401 into notes?
2. yasui2026 q_intrinsic / q_external / 0.526 dB/cm near critical coupling: keep `author_estimate` under D403 (recommended, strict reading) or `measured`?
3. wu2018 class for cascaded Sagnac resonators: `resonator.photonic_crystal` (recommended) or `resonator.other`?
