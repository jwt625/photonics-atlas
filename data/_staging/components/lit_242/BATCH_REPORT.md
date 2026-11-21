# lit_242 batch report

Paper: lit:rombouts2024 (JLT 43(7), 2025; O-band InP monolithic 4x4 SOA broadcast-and-select switch). Page-1 title
matches the source row. verified_on 2026-11-20. Dry run: +9 components, +35 metrics, 0 errors.

## Components / metric rows

| component | class | metrics |
|---|---|---|
| cmp_lit_rombouts2024_switch_4x4 | switch_fabric.other | 9 (IL 10 dB mean, 5 on/off rows 60 / 53 / 50 / 70 / >=29 dB, 4x4 ports, footprint) |
| cmp_lit_rombouts2024_gate_soa_600um | amplifier.soa | 6 (gain 13.7 / 8.5 dB, psat_in > -4.1 dBm, path 3-dB bandwidth 37.4 nm, Vf 1.5 V, length) |
| cmp_lit_rombouts2024_mmi_2x2 | splitter.mmi | 5 (excess 0.9 dB, IL 3.9 dB, single-MMI 3-dB width > 100 nm, four-MMI path widths 59.8 / 62.1 nm) |
| cmp_lit_rombouts2024_shallow_crossing | crossing.other | 1 (0.13 dB/crossing) |
| cmp_lit_rombouts2024_lensed_fiber_edge | fiber_chip_coupler.edge | 1 (2.2 dB/facet) |
| cmp_lit_rombouts2024_deep_wg | waveguide_platform.straight | 3 (3 dB/cm specification, 400 nm core, 100 um min bend) |
| cmp_lit_rombouts2024_shallow_wg | waveguide_platform.straight | 2 (5 dB/cm specification, 400 nm core) |
| cmp_lit_rombouts2024_test_1x8_path | switch_fabric.other (test structure) | 4 (IL 6.8 / 5.9 dB, rise 15 ns, fall 2.5 ns) |
| cmp_lit_rombouts2024_test_1x8_soas | amplifier.soa (test structure) | 4 (output -9.5 / -7.5 dBm, lengths 500 / 450 um) |

Fab on every row: org_smart_photonics ("All growth and processing steps are performed by SMART Photonics", p.3
Sec. II); process_name "SMART Photonics O-band PDK" (printed "open-access SMART Photonics O-band PDK", p.3 Sec. II).
No facility statement; no acknowledgments section (grants only, p.1 footnote).

## Values not entered and why

- OSNR (38 dB at -5 dBm, 37.9-39 dB at 1285 nm, 35.4 / 34.0 / 31.4 dB PAM-4 paths, 1x8 values 46.4 / 38.4, 37.5 /
  32.7, 47.5 / 38.7, 42 / 30 dB): no registry parameter (rombouts2025 / zali2026 precedent).
- Power penalties and BER results (10 Gb/s NRZ, 100 Gb/s PAM-4, LWDM LR4, emulated 8x8): system metrics. The 10 Gb/s and
  PAM-4 results are also the subject of the authors' refs. [38] / [39] (p.2 Sec. I).
- Gain temperature dependence: 7.5 dB drop from 20 to 50 C, path i1o1 (p.5, Fig. 8): no registry parameter.
- ASE / gain peak blue-shift to 1285 nm (p.4): center_wavelength_nm not allowed for amplifier.
- Per-SOA gain, 3-dB bandwidth, OSNR and on/off versus SOA length (Fig. 9, Fig. 10) and per-path gain / loss bars
  (Fig. 11): figure-only values for other SOA lengths; one component per length would be needed (rule 9).
- Fig. 3 bar heights of the test structures (fiber-to-fiber loss of wg c0, wg c5, MMI p1 / p2, i4o1, i4o3): figure
  only; the extracted per-component values are entered instead. 2.5 dB extra loss of path i4o3 (p.4): a path
  difference with mixed causes, not a component value.
- SOA saturation input power about -2 dBm: cited (ref. [41], rule 3). On-chip SOA input -7.5 dBm (p.8): estimate of
  an operating point, no parameter.
- Scaling projections (Fig. 25: 32 dB extra loss for 16 ports, five 600 um SOAs, 37 -> 21 nm, OSNR about 35 dB via
  ref. [51], 38 dB crosstalk): model / projection, no device.
- Doping levels (3e17 / 1e18 cm-3), minimal SOA spacing 250 um (layout rule), 200 um SOA of the 1x8 structure
  (geometry only, no metric): notes only.

## Missing fab / facility orgs

None (org_smart_photonics exists).

## Judgment calls for the auditor

1. Fig. 12(a) conflict: text prints a 60 dB on/off ratio for path i3o1, the caption 65 dB. Text value entered, conflict
   in notes (render reads about 60 dB peak to peak).
2. switch_4x4-m1 (10 dB mean fiber-to-fiber IL): conditions not stated with the value; band O inferred. By-eye
   reading of Fig. 11 (passive loss about 22-23 dB minus SOA gain bars 4-13.5 dB at 1285 nm, 100 mA) gives roughly
   13 dB average over 14 SOA paths, so the 10 dB may come from other conditions; not resolved, not noted in the row.
3. Basis of the Sec. III-A breakdown values (coupling 2.2 dB/facet, crossing 0.13 dB, MMI 0.9 / 3.9 dB, SOA gain
   13.7 / 8.5 dB): `author_estimate`, because each rests on the waveguide loss computed from mask lengths and the
   specified (not measured) 3 / 5 dB/cm. Alternative: `derived` if a PDK specification input is ruled acceptable.
4. Four-MMI SOA-less path 3-dB widths (59.8 / 62.1 nm) placed on the MMI row as cascade values (switch_fabric does not
   allow bw_3db_nm); condition says cascade incl. facets, waveguides, crossings.
5. Single-MMI bw_3db_nm > 100 nm: bound = plotted span 1260-1360 nm (Fig. 4), `extracted_from_figure`; text says only
   "extends beyond the O-band spectrum".
6. psat_in_dbm > -4.1 dBm (fiber input): "gain saturation is not visible" up to the highest available input; entered
   as a lower bound, ref_plane fiber.
7. 1x8 test-structure IL 6.8 / 5.9 dB: printed as negative "insertion loss" of the PIC; Fig. 21 places the external
   VOA (3 x 3.9 dB combiner emulation) inside the measured path, but the text does not say whether the printed value
   includes it. Entered with includes naming the VOA and an explicit not-stated note. Output powers -9.5 / -7.5 dBm
   likewise at the OSA plane of Fig. 21.
8. Rise / fall times (15 / 2.5 ns) were measured on the 1x8 test structure ("An on-chip test structure (Fig. 21) is
   used with a second integrated SOA", p.6), so they sit on test_1x8_path, not the 4x4 row. `derived` for ns -> us
   (D256).
9. One amplifier row for the 600 um i3o1 SOA (the paper's reference SOA); the all-SOA average forward voltage (1.5 V
   at 100 mA) is placed on it with a condition saying so.
10. switch_4x4-m6: on/off >= 29 dB derived from the LWDM spectrum statement (-21 dBm on, -50 dBm or lower off, path
    i3o3 per Fig. 18).
11. D408: this JLT paper extends the authors' ECOC 2023 [38] and OFC 2024 [39] papers; only the transmission results
    are attributed to them (not entered anyway). Component values kept.
12. Waveguide rows carry the PDK-specified losses (`specification`, catalalahoz2026a / chen2024 precedent), since the
    paper uses them as stated inputs.

## Registry gaps

- `osnr_db` (amplifier, switch_fabric): optical signal-to-noise ratio at the stated resolution bandwidth and input
  power (resolution and input in condition). Skipped values: 38 dB at -5 dBm (p.2), 37.9-39 dB at 1285 nm, 0.1 nm RBW,
  -4.1 dBm (p.5 Fig. 7), 46.4 / 38.4 dB (p.9 Fig. 22), 47.5 / 38.7 dB (p.10). Same gap noted on rombouts2025 / zali2026.
- `gain_temperature_coefficient` or gain change over a temperature span (amplifier): 7.5 dB over 20-50 C (p.5 Fig. 8).
- `center_wavelength_nm` for amplifier (gain / ASE peak): 1285 nm gain peak at 100 mA (p.4).
