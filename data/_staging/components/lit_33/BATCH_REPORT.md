# Batch lit_33 report (distill subagent, 2026-10-29)

Dry-run `batch lit_33: +23 components, +102 metrics; errors 0`. ASCII, no e-mail, no quotes from restricted sources. Page-1
title / authors match the source row for all 8 papers. Not yet audited or merged. Build helper (data per paper):
scratchpad `distill_lit_33/build.py` + `p_<paper>.py`.

## Per paper (components / metrics)

- shimizu2023 (2 / 9): cascaded polarization-diverse PPLN OPA with reused SH pump and the conventional one-module OPA
  (amplifier.parametric, fiber-pigtailed modules, platform empty as in abe2025). Module gain > 15 dB over 1545.32-1618.86 nm,
  gain_bandwidth_nm 73.54 (derived from the printed band edges); conventional 7.8 THz converted to 64.7 nm (derived, c / f);
  peak gain ~21 dB and NF ranges (4.6-6.1 / 4.6-4.9 dB) read off Fig. 5; WDM total output 14.7 dBm at -5.0 dBm input.
  Not entered: refs. [18], [19] waveguide length / loss / SHG efficiency (own earlier work, D259); NF penalty 1.4 dB
  (relative); simulated gain variation 4.9 / 6.2 / 12.7 dB; simulated 2nd-module gain ~10 dB; simulated poling period
  ~18.6 um; "1st PPLN in proposed OPA" gain curve (sub-stage operating point). Fab empty (all NTT, passive).
- ye2021 (4 / 18): Si3N4 1.42 m spiral (one waveguide, D396): amplifier.parametric (PIA 6.4 dB, PSA 9.5 dB on chip, PSA
  fiber-to-fiber 4.5 dB, NF 1.2 / 3.3 dB on chip and 3.7 dB fiber-to-fiber, 28 nm gain span, 20 dB phase-sensitive
  extinction, length, footprint), frequency_converter.other (CE 5.3 dB -> 339 %, 78 % in the 10 Gbps conversion),
  waveguide_platform.straight (OFDR 1.4 / mean 1.7 dB/m -> dB/cm, 7.0 dB fiber-to-fiber), lensed-fiber facet
  (2.5 dB/facet derived). On-chip gain / NF / CE derived (D166). Fab Chalmers (author contributions). Not entered: GVD
  -36 / -45 ps2/km, BER penalties, theory NF curves, width / thickness (printed only as 690 nm x 2000 nm without saying
  which is the thickness).
- carpenter2020 (2 / 15): Zn-indiffused MgO:PPLN diced ridge SHG 1560 -> 780 nm, 4.0 cm, 12 um ridge
  (frequency_converter.shg: device 58 % and crystal 74 % efficiency, IL 1.2 dB, poling 18.5 um, length, width) and the same
  waveguide as waveguide_platform.straight (fit losses 0.12 / 0.58 dB/cm and fit coupling 88 % derived, D80a; MFDs x / y
  at both wavelengths). Not entered: 2.50 W SHG output, phase-matching FWHM 0.28 / 0.18 nm and 35.7 % narrowing (registry
  gaps), d_eff 7.6 pm/V, damage beyond 4.5 W incident (threshold not characterized).
- stone2022 (1 / 6): population row (D165) for 16 pulley-coupled Si3N4 microring Kerr OPOs (frequency_converter.other,
  mckenna2022 precedent): best CE ~14.5 % (signal 454 THz) and ~12 % (idler 315 THz), range 3.5-14.5 % over 590-1150 nm;
  RW 825 nm, H 500 nm, BOX 3 um. Fab NIST (authors fabricate; all authors JQI + NIST, JQI's registry parent = NIST, D154).
  Not entered: on-chip output powers (best 5 / 4 mW; Table II), radius 25 um, gap, pulley length, bus width (registry
  gaps); measured kappa (log-scale scatter only). Table II pump powers 36 / 35 mW vs 34 mW in the text: text used, noted.
- wang2026c (1 / 4): 4H-SiC microring OPO R 120 um, RW 5 um (frequency_converter.other: Q ~5e6 near 1550 nm as q_loaded,
  width, etch ~580 nm, slab ~450 nm). Fab DTU (authors fabricate, all DTU). Garbled pages 8-9 hold only acknowledgements and
  references (no values used). Not entered: OPO tuning 1205-1378 nm and slopes 5.06 / 9.21, SFG ~678 nm at about -35 dBm
  on chip, radius (registry gaps); threshold (Supporting Information not cached). Sibling R 90 um dual-pair OPO: no
  performance parameter, no row.
- ghosh2012a (3 / 14): Ce:YIG/SOI bonded MZI isolator (25 dB at ~1495.6 nm from Fig. 9, IL 8-9 dB constructive / ~14 dB
  at max isolation, scope unspecified: normalization not stated; L 920 um, 900 nm x 220 nm, BOX 2 um); Ce:YIG-covered SOI
  waveguide (4 dB excess vs plain SOI measured; 12 and 14.5 dB/cm author_estimate, resting on the simulated transition loss
  and a 2.5 dB/cm SOI value of unstated origin); SOI / Ce:YIG-SOI interface (waveguide_platform.transition, 0.8 dB
  simulated). Different paper from merged ghosh2012 (PTL); no overlap. Fab empty (unnamed CMOS pilot line, passive
  bonding). Not entered: FSR 7.6 nm, NRPS 0.987 rad/mm, 1.1 nm shift, remanent 0.6 nm shift over three months, MMI
  geometry (no row: geometry only), loss-budget estimates 8.1 / 3.9 dB.
- karki2019 (7 / 23): bias-magnet-free latching-garnet isolators: ridge waveguide (>= 25 dB, <= 3.5 dB over 1520-1580 nm),
  slab (29 dB, 1.5 dB), bulk UV-epoxy (> 30 dB 1522-1565, < 0.7 dB), bulk BCB (> 25 dB, 38 dB at 1580, < 0.5 dB), 60 um film
  (25-30 dB, 0.6-1 dB); ridge Faraday rotator (< 2 dB) and Faraday rotator mirror (< 0.2 dB) as nonreciprocal.other
  (lapointe2025 precedent). Not entered: ridge isolator width (Fig. 8 caption 12 um vs p.5 text 15 um), Faraday rotation
  angles, double-pass PER > 25 dB and ~30 dB extinction (no nonreciprocal parameter), Ag / Au coating reflectance on glass
  (coating trials). Fab empty (Michigan Tech + SRICO, passive).
- sohn2018 (3 / 13): acoustically pumped AlN racetrack (D396): nonreciprocal.isolator (frequency-shifted-output contrast
  ~15 dB), mode_converter.converter (sideband conversion 17 % as coupling_efficiency_pct, de_embedded; cheng2025 precedent
  for the class), resonator.ring (Q_loaded ~170k TE00 / ~102k TE10, FSR 140.5 / 136 GHz, geometry incl. R 100 um, 968 um,
  2.2 um ridge, 200 nm etch, 800 nm bus). Fab UIUC (authors fabricate). Not entered: 1.14 GHz modulation bandwidth, 45 dB
  Stokes suppression, beta 0.209 (0.204 Supp.) GHz/nm, Gph, IDT efficiency 3.9 %, theoretical isolator / AOFS (Supp. S5-S6).

## Missing fab / facility orgs

- Myfab Chalmers (facility; ye2021 p.6 Acknowledgments: Si3N4 samples fabricated there).
- Michigan Tech microfabrication facility (MFF) and Michigan Tech applied chemical and morphological analysis laboratory
  (ACMAL) (facilities; karki2019 p.7 Acknowledgment).
- Not needed (supplier notes only): Covesion Ltd (carpenter2020 wafers, p.3), SRICO, Inc. (karki2019 author affiliation).

## Judgment calls

- carpenter2020 fab Southampton borderline (D84a: own manufacturing approach referred to earlier work, passive steps,
  staff cleanroom help D84b).
- stone2022 fab = NIST via JQI parent (D154); no facility named.
- shimizu2023 / ye2021 / stone2022 / sohn2018 wavelengths converted from printed THz values (c / f), noted per row.
- sohn2018 isolation_db holds the frequency-shifted-output contrast (the paper's frequency-shifting isolator), not a
  transmission isolation; 17 % conversion kept linear in coupling_efficiency_pct (alternative: insertion_loss_db 7.7 dB
  derived as in cheng2025).
- ye2021 PSA fiber-to-fiber gain / NF measured (the paper records fiber-to-fiber values); on-chip values derived (D166).
- karki2019 bulk isolators entered as reference structures (measured with the same lensed-fiber setup).
- wang2026c Q ~5e6 on the frequency_converter row (no separate resonator row, mckenna2022 / D250 precedent).

## Registry gaps

- output_power_dbm (or _mw) for frequency_converter: carpenter2020 2.50 W SHG (p.5), stone2022 5 mW signal / 4 mW idler on
  chip (p.5), wang2026c SFG about -35 dBm (p.7). Def: generated (SH / signal / idler / SFG) output power, reference plane
  in ref_plane.
- Phase-matching acceptance bandwidth for frequency_converter (bw_fwhm_nm): carpenter2020 0.28 / 0.18 nm FWHM (p.7 Fig. 4).
- OPO tuning range / slope for frequency_converter: wang2026c 1205-1378 nm signal for 1553-1587 nm pump, slopes 5.06 /
  9.21 (p.4).
- radius_um, gap_nm, coupling_length_um, bus_width_nm for frequency_converter (ring OPOs): stone2022 R 25 um, G 125-135 nm,
  Lp 3 um, WW 375-400 nm (p.3, p.5); wang2026c R 120 um (p.3).
- Gain-flatness parameter for amplifier (max - min gain over a stated band): shimizu2023 simulated 4.9 / 6.2 / 12.7 dB (p.5).
- poling_period_um for amplifier.parametric: shimizu2023 ~18.6 um (calculation input, p.3).
- fsr_nm for nonreciprocal (MZI isolators): ghosh2012a FSR 7.6 nm (p.5).
- NRPS parameter (rad/mm) for nonreciprocal: ghosh2012a 0.987 rad/mm (p.7).
- per_db / extinction for nonreciprocal Faraday rotators: karki2019 > 25 dB (p.5), ~30 dB (p.6).
- bw_3db_ghz for nonreciprocal: sohn2018 ~1.14 GHz modulation FWHM (p.10).
- Sideband suppression ratio for nonreciprocal / mode_converter frequency shifters: sohn2018 45 dB (p.10).
