# lit_94 batch report (2026-11-06)

All five cached texts match their source rows (page-1 title); none is a correction, erratum or another paper. No garbled text layer flagged. Dry-run: +26 components, +128 metrics, 0 errors (the one warning, ni2025b m18 / m4, is an existing merged row, not this batch).

| paper | components | metrics |
|---|---|---|
| bayoumi2025 | 6 (splitter.directional_coupler: 2; wdm.cascaded_mzi: 4, of which 2 design) | 36 |
| bolk2018 | 5 (wdm.awg: 4 fabricated gap-series rows + 1 design row) | 23 |
| sun2023 | 11 (wdm.bragg_cdc) | 43 |
| feyisa2022 | 2 (switch_fabric.other; amplifier.soa) | 14 |
| yamaguchi2016 | 2 (switch_fabric.wss) | 12 |

## Not entered, and why

bayoumi2025
- Operating range (ER >= 18.4 dB over at least 100 nm vs 36.7 nm, 2.7x): no operating-range parameter on wdm; in MZI notes. The 36.7 nm window position is not printed.
- Table I rows [2]-[7]: other works (rule 3).
- Straight-DC loss: not stated. MZI arm length difference: not printed.

bolk2018
- Wafer flatness / CDU results (level-sensor range 8-12, 3-4, about 2, below 1 um; CDU about 30 / 20 / below 10 nm; p.2 Sec. III, Fig. 2), lithography constants (NA 0.75, k1 0.4, k2 0.9), resist uniformity: process metrics, not component metrics.
- Etch lag 12 % at 1250 nm trench, at least 30 % at 250 nm, expected at least 35 % at 100 nm (p.4 Sec. VI, Fig. 6): process metrics; in no row.
- Side lobes at about -20 dB in Fig. 4 (attributed to polarization rotation, ref. [14]): reference level of the -20 dB not stated (Fig. 4 axis is absolute power); not entered as slsr / crosstalk.
- Simulated Fig. 3 channel-by-channel losses beyond the printed 2.6 / 3.9 dB: not read.
- Earlier ECOC 2017 paper of the authors (ref. [9]) is cited as background only; no value is attributed to it (D408: values kept).

sun2023
- dl series (dl 0.65 / 0.7 / 0.8 / 0.85 um, fabricated, Fig. 10): only spectra, no printed values; simulated bandwidth / IL vs dl readable from Fig. 4(a) (about 53.5 / 51.1 / 44.3 / 40.0 nm). No rows (a row would carry only figure-read simulated values).
- du series (0.40 / 0.50 / 0.55 um, Fig. 3(e)-(h), Fig. 4(b)): simulation only, not fabricated; no rows.
- Nanohole-shape series (rectangular, circular, diamond, sinusoidal; Fig. 8 simulated, Fig. 14 measured): only a design-target bandwidth range of 35-45 nm for the whole set and spectra; no per-device value; no rows.
- Simulated bandwidth / IL of the a and b series (Fig. 6) and the simulated IL of the main design (Fig. 4 / 6, about 0.7 dB): figure reads of simulations, not entered; measured Fig. 12 reads are entered instead.
- Effective index of the middle medium (about 2.49) and system-mode indices 2.18 / 2.61: calculations, no parameter on wdm.bragg_cdc for effective index.
- Hole width a, hole height b, hole-to-edge distances du / dl: no registry parameter (in labels and notes).
- Table I rows [12], [14]-[16], [21]: other works (rule 3). Bandwidth-to-length ratio 2.19e-3 (Table I): no parameter.
- Measured Fig. 13 (g series) spectra: no printed values; only the printed simulated ERs are entered.

feyisa2022
- Average end-to-end fiber-to-chip coupling loss 9 dB (p.4 Sec. III-A): the facet coupler is not described and the value is obtained by subtraction of the net on-chip gain; no coupler row; in switch notes.
- OSNR > 40 dB, power penalties 1.5 / 2 dB, input power dynamic range 10 dB (the latter from the authors' ref. [28], rule 3): system metrics / cited.
- Switching energy 9 pJ/bit, 2.25 pJ/bit with 4 WDM channels: no parameter.
- Crosstalk about -26.5 dB: estimated from the authors' prior work and the cited -35 dB crossing value (rule 3).
- Table II component losses (0.2 dB per bend, 0.25 dB per crossing, 3.5 dB per MMI, 3 dB/cm, refs. [18]-[20]) and the Fig. 4 loss breakdown built on them (21 dB from 6 MMIs, up to 24.5 dB from crossings, etc.): cited values (rule 3). Hence no bend, crossing or MMI rows.
- Foundry improvements (1.5 dB/cm or 1.5 dB/mm, 0.1 dB bends, 30 dB/mm SOA gain; ref. [23]): cited. Note the paper prints the waveguide loss as 1.5 dB/cm (p.5) and 1.5 dB/mm (p.7).
- SOA output saturation power: only a relative 2 dB improvement from the 3 um width; transparency current 14 mA (estimated): no parameter.

yamaguchi2016
- Absolute transmittance levels in Fig. 8 / Fig. 9 (peaks near -20 dB): normalization not stated; not entered as insertion loss.
- Principal beam-splitting losses 6 dB and 3 dB: theoretical design values; in notes and as the excluded / included terms.
- Focal lengths 12 / 150 / 100 mm: no parameter on switch_fabric; in core_material.

## Missing fab / facility orgs

- NanoLab@TU/e (bolk2018 p.1 Sec. I: the ASML PAS5500/1100 DUV scanner used for this work is installed at the NanoLab@TU/e cleanroom; p.4 Ack. thanks its technical staff): candidate facility, parent org_eindhoven_university_of_technology. Not in the registry. If added, it would go on the 4 fabricated bolk2018 AWG rows (the staff thanks alone would not qualify; the facility claim rests on the p.1 statement that the scanner of the process sits there).
- Used orgs all exist: org_imec, org_applied_nanotools, org_smart_photonics.

## Judgment calls

1. bayoumi2025 bent DC loss 0.03 +/- 0.03 dB: `excess_loss_db` (Table I column "splitter excess loss"), per_component, method cutback, basis `derived` (sinusoidal fit across DCs of different coupling lengths; elsaeed2024 precedent from the same group). The design method is from the authors' ref. [8] (elsaeed2024, merged), but that paper's 0.5:0.5 bent DC is a different design (380 nm width, R 25 um, 8.5 deg) and the citation is attached to the method, so the value stays (D408). No wavelength is printed with the loss: c_band with `wavelength_inferred`. Alternative: `measured` (standard fit, D80a).
2. bayoumi2025 platforms: DCs `soi_strip` (caption: all DCs on strip waveguides, D434); MZIs `soi` (arm waveguide type not stated). Fab org_imec from "fabrication is done using imec's iSiPP300 platform" (D455 precedent).
3. bayoumi2025 MZI ER: minimum ER over the span (18.40 / 5.45 dB, Fig. 3 labels) entered without statistic and the condition saying "minimum over the span"; maximum ER labels as `best`; wafer maps as `wafer_map` ranges, n 63. Span 1490-1590 nm read off the axes (`wavelength_inferred`).
4. bayoumi2025 16-channel systems: two `row_kind: design` rows (transfer-matrix calculation on measured DC data), basis `simulated`; "worst channel isolation" in `crosstalk_db` (type not stated); n_stages 4 counted from the Fig. 5 stage labels.
5. bolk2018: one row per inter-waveguide gap (100 / 200 / 300 / 400 nm; sibling designs, rule 9). Measured excess loss scope per_component, method reference_structure (normalized to the maximum of reference waveguides). Only the 100 nm best value (0.15 dB) is printed; the per-gap ranges are Fig. 5 reads. The simulated star-coupler losses (1.1 dB at 100 nm, 1.8 dB improvement from 400 nm) sit on the fabricated gap rows (D80e: Fig. 5 compares them on the same gap axis); 200 / 300 nm simulated values are curve reads (D454).
6. bolk2018 Sec. IV 8x8 cyclic AWG (200 GHz, FSR 1600 GHz, 1500 nm waveguides, 2.6 / 3.9 dB uncoupled model): kept on a separate `design` row because the paper does not state that the fabricated AWGs are this design (D159 spirit); Fig. 4 is consistent with it (eight channels per FSR) but that is an inference. Alternative: move these values to the 100 nm fabricated row.
7. bolk2018 fab empty: passive "were fabricated" and "we have developed a process flow" (D80b); authors spread over TU/e, SMART Photonics, InPACT, ASML, so D154 / D399 do not apply. The generic-platform note in the task (D398 / D399) does not change this: no foundry or MPW provider is named for these devices.
8. sun2023: 11 rows: main design, four hole-width siblings, three hole-height siblings (the a = 0.24 / b = 0.30 points are the main design), three gap siblings (g = 0.1 is the main design). Measured bandwidth / IL of the width / height siblings are Fig. 12 reads (`extracted_from_figure`); the reads reproduce the printed main-design 43.2 nm and the Table I 48.8 nm / 0.2 dB, which supports the readings. b = 0.35 um carries the printed Table I values (48.8 nm, 23.4 dB, 0.2 dB, 22.3 um) as `measured`.
9. sun2023 conflicts kept with notes: simulated bandwidth 47.8 nm (p.3) vs 47.3 nm (p.7); simulated maximum ER 51 dB (p.3, p.6) vs 45 dB for the identical g = 0.1 um filter (p.5); coupling length 22.3 um (Table I, abstract) vs N x period = 22.4 um (p.3).
10. sun2023 IL scope `de_embedded`, method reference_structure (GC-waveguide-GC calibration circuit). Main-device IL 1.1 dB `measured` (the paper's average over its own measured passband). The a = 0.26 um IL reads about 0 dB (entered as 0.0 approx). Access-waveguide widths: wu (input) as `bus_width_nm`, wl (drop) as `width_nm` (davis2020 / gebregiorgis2023 precedents). Fab org_applied_nanotools (named EBL fabrication; valdez2025 precedent, D420). Platform `soi_strip` (220 nm strip, single etch).
11. feyisa2022: switch row `switch_fabric.other` (B&S SOA switch; rombouts2025 / zali2026 precedents) plus an `amplifier.soa` row for the 3 um SOA (D396). The 31 dB gain is the total of three cascaded SOAs (G1+G2+G3), `derived` (difference of fiber-to-fiber losses at operating current and at transparency, D166), with the cascade in condition; per-SOA gain is not printed. Worst-case net on-chip loss 12 dB as `insertion_loss_db` on_chip_excess incl. SOA gain; il_nonuniformity 20 dB `derived` from the printed best-case 8 dB gain and worst-case 12 dB loss. Average F2F loss 18.54 dB `measured`, SOA bias not stated with it. Power 315 mW / 2.52 W `derived` (stated bias x voltage; rombouts2025 precedent); 1.5 V `forward_voltage_v` author_estimate (origin not stated). Rise / fall 4.2 / 6.4 ns converted to us, `derived` (D256).
12. yamaguchi2016: in scope per D424 (LCOS free-space WSS, platform `other`), although the I/O ports are not named as fibers (Fig. 7 shows a port array with collimating lenses). Two rows (B&S CGH 4x4 without MPMT; multicast MPMT 4x4 for the 2-degree ROADM): same optics, different port arrangement and phase patterns. The loss increase over the optics' own 1 x N operation is `excess_loss_db`, scope `on_chip_excess` with the 1 x N insertion loss in `excludes` (melati2022 precedent for an excess over a baseline structure); the printed maxima 9.1 / 7.1 dB `measured`; the CGH-imperfection parts 0.9-3.1 / 3-4.1 dB `author_estimate` (split with the theoretical 6 / 3 dB splitting term, rule 4). "Maximum port crosstalk -20.0 dB" -> crosstalk_db 20.0 `ge`. Fab empty (no fabrication statement).

## Registry gaps (skipped value, locator, proposed definition)

- `operating_range_nm` on wdm (and splitter): bayoumi2025 >= 100 nm vs 36.7 nm span with ER >= 18.4 dB (p.2 Sec. II). Full wavelength span over which a stated figure of merit (ER / coupling) stays above the stated level (level in condition).
- Photonic-crystal hole dimensions on wdm.bragg_cdc (`hole_width_nm`, `hole_height_nm`) and hole offset (`hole_edge_distance_nm`): sun2023 a 200-280 nm, b 200-350 nm, du 0.40-0.55 um, dl 0.65-0.85 um (p.3-5). Needed to draw the APhC top view.
- `effective_index` on wdm: sun2023 2.49 / 2.18 / 2.61 (p.3, calculated). Lower priority.
- `osnr_db` on switch_fabric / amplifier: feyisa2022 > 40 dB best case (p.1, p.5 Fig. 3) (also rombouts2025 52 / 44 dB, zali2026 > 40 dB in merged notes). Optical signal-to-noise ratio at the stated resolution bandwidth (bandwidth in condition).
- `switching_energy_pj_per_bit` on switch_fabric: feyisa2022 9 pJ/bit, 2.25 pJ/bit for 4 WDM channels (p.7 Sec. IV-D). Electrical energy per switched bit at the stated line rate.
- `focal_length_mm` on switch_fabric (free-space optics): yamaguchi2016 12 / 150 / 100 mm (p.7 Sec. 4.2). Lower priority.
