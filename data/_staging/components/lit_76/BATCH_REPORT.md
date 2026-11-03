# lit_76 batch report (switch_fabric), 2026-11-02

All four cached texts match their source rows (page-1 title); no correction or wrong paper. Dry-run: +11 components, +81 metrics, 0 errors.

| paper | components | metrics |
|---|---|---|
| khope2019 | 5 (switch_fabric.wss, switch_fabric.other, wdm.mrr, crossing.mmi, waveguide_platform.straight) | 33 |
| barazani2023 | 1 (switch_fabric.mems) | 20 |
| rombouts2025 | 3 (switch_fabric.other, amplifier.soa, fiber_chip_coupler.edge) | 21 |
| roy2026 | 2 (switch_fabric.mems unit cell, splitter.adiabatic design row) | 7 |

## Not entered, and why

khope2019
- Zero-bias resonance 1554.74 nm (p.7 text) vs 1555.74 in the Fig. 3(h) fit, same ring: conflict, in notes.
- "Deep etched 400 nm" (p.6): impossible as an etch depth in a 220 nm film; in notes.
- 13 dB test setup loss incl. chip-to-fiber coupling (p.8): setup total, no edge-coupler split, so no coupler row; appears as `excludes`. Edge coupler 127 um pitch is geometry only, no row. 1x2 output splitter: no value.
- Fig. 7 and Sec. 4 scaling values: simulated / projected for other radices. Small-signal < 5 us from ref. [54]: cited. BER: no number. Sumitomo modulator 4 dB: setup equipment.
- n_channels: paper gives L = 2 per crosspoint and M as a free parameter; no fabricated channel count stated.

barazani2023
- Gap-closing benefit about 9 dB (p.9): follows from the entered open / closed rows; in notes. Raw transmission of the reference circuit (Fig. 15): no isolated SGC or Y-branch value, so no rows.
- Earlier-group switch losses (12-15 dB, 4-6 dB, p.11): cited. Simulated displacement, temperature and spring constants: no parameter.

rombouts2025
- 3.9 dB per MMI (p.6): attributed to ref. [11]. Crossing loss stated as unknown (p.4). No MMI or crossing row.
- OSNR, power penalties: no parameter / system metrics (zali2026 precedent). In-band crosstalk -71.5 dBm (p.3): estimated absolute power, not a suppression.
- With-pre-amplifier values (Fig. 5): external discrete SOA of the setup.

roy2026
- 8x8 switch (3.5 mm x 1.8 mm, p.2): geometry only, no performance, so no row; in unit-cell notes.
- Actuator gap about 3 um is not a coupler gap (`gap_nm` not used). About 1 us (p.4): projection. Supplement not in the cached file; crossing and passive data there not available.

## Missing orgs (registry)

- AEPONYX Inc: barazani2023 p.13 acknowledgment (device fabrication), p.6 Sec. III (process flow). fab_org_ids empty. Also reported earlier for sharma2022.
- Collaborative Center for MiQro Innovation (C2MI): barazani2023 p.6 Sec. III (foundry services and installations). facility_org_ids empty.

## Registry gaps (skipped value, locator, proposed definition)

- `actuation_voltage_v` / `pullin_voltage_v` (switch_fabric, phase_shifter): barazani2023 10 V full stroke, pull-in 68 V and 62-64 V (p.9); roy2026 about 32 V OFF (entered as bias_v), pull-in about 40 V (p.3). Definition: drive voltage for the stated switch state; pull-in voltage of an electrostatic actuator.
- `actuator_displacement_um` (switch_fabric, phase_shifter): barazani2023 11.34-12.48 um at 10 V (p.8); roy2026 about 700 nm at 35 V (p.3). Definition: actuator displacement at the stated voltage.
- `heater_resistance_ohm` for wdm / switch_fabric: khope2019 12-20 kOhm over 8-16 V (p.7 Fig. 3(i)).
- `pitch_um` for switch_fabric: barazani2023 4 um waveguide pitch (p.3).
- `endurance_cycles` for switch_fabric: roy2026 Fig. 4(a); cycle total not printed clearly.
- `energy_per_bit_pj` for switch_fabric: khope2019 0.8125 and 0.325 pJ/bit (p.7, calculated).
- `osnr_db` for switch_fabric: rombouts2025 52 dB (Table I), 44 dB (p.5).

## Judgment calls for the auditor

1. khope2019 ring as `wdm.mrr` plus unit cell as `switch_fabric.other` (D396, D400): each input carries WDM channels, so the ring is a channel filter in a WDM path; D407 needs demultiplexed ports and does not fit. Spectral values on wdm.mrr, switching values on the unit cell.
2. khope2019 crossing 0.3, through 0.3 and drop 4.7 dB as `measured`, method loss_breakdown: the paper says measured and prints no formula. The 0.17 dB per ring from the 10 / 20 / 40 series is also `measured` (printed, formula not shown). Both sets kept: paper does not reconcile 0.17 vs 0.3 and 1.9 vs 4.7.
3. khope2019 "multi-mode waveguide crossing" as `crossing.mmi`. n_samples 64 on path loss from the 64-ring statement and the Fig. 4 heatmap.
4. barazani2023 Table II port 2 value 4.3 entered; Abstract prints 4.4. The +/- values (kind not stated) stay in condition, no std rows. Basis `derived` (reference subtraction; sharma2022 precedent).
5. rombouts2025 Table I "Speed" 15 ns as rise_time_us `author_estimate`: "This work" row, undefined, no measurement in the text, same as the ref. [11] row. Delete if D259 should apply.
6. rombouts2025 Table I IL "10 to 17" entered as a range with its meaning not stated; worst path about 26.5 dB read off Fig. 3(b) +/- 1 dB shows it does not span all paths. n_samples 29 counted from Fig. 3(b) labels (28 on/off markers).
7. rombouts2025 subtype `switch_fabric.other` and path values on `amplifier.soa` follow zali2026. psat_in_dbm 5 is a 1-dB level. Fiber coupling 5 dB is per path (scope fiber_to_fiber), `author_estimate`, origin not stated.
8. roy2026 facility: SNF as printed (org_stanford_nanofabrication_facility) although the paper is post-merger; org_nano_stanford is the successor. Fab org_aim_photonics from the MPW tape-out (D398). 600 us as rise_time_us: paper does not separate rise and fall or define the level.
9. roy2026 mech_resonance_khz 300 `author_estimate`: not said to be measured. Fig. 2(b), Fig. 3(c) simulations kept to the coupler row only.
