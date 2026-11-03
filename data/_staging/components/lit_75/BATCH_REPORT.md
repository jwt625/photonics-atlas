# Batch lit_75 report (distill subagent, 2026-11-02)

Class wdm (awg, tff, cascaded_mzi, bragg_cdc) plus the other components the papers hold (micro_optics.other, photodetector.apd,
fiber_chip_coupler.edge / grating, waveguide_platform.straight / bend / other, splitter.directional_coupler). Papers: yi2024a,
huh2016, cheung2019, palmer2026, xie2023, afzal2020. Page-1 titles match the source rows; no wrong paper, no correction.
Totals: 28 components, 352 metric rows. Dry run: 0 errors.

## Per paper

| paper | components | metrics | contents |
|---|---|---|---|
| yi2024a | 4 | 96 | X-cut TFLN AWGs: Design-1, -2, -3, 8x8 router Design-4 |
| huh2016 | 4 | 29 | TFF DEMUX in APD-ROSA; collimating lens; focusing array lens; APD block |
| cheung2019 | 14 | 152 | Gaussian and flat-top AWG; lattice Designs 1-3; waveguide; bend; edge coupler; 5 bent DCs + straight DC (design) |
| palmer2026 | 2 | 41 | 8x400 GHz cascaded silica AWG; spot-size converter / FAU interface |
| xie2023 | 3 | 29 | 32x100 GHz SOI AWG; slab-array taper (design); grating coupler |
| afzal2020 | 1 | 5 | GF 90WG SWG contra-directional add / drop filter |

## Values not entered, and why

- yi2024a: bend mode rejection (TE2, TM1 below -45 dB, simulated, p.4), phase error +/-0.05 pi (p.6), FPR modal powers (Fig. 2c): no
  parameter, in notes where relevant. Data-transmission penalties (system level, notes). Table 2 other works. alpha = 90 deg AWG: no
  value (note on Design-3). Lab-made TFLN modulator Vpi 4.5 V, 40 GHz (p.10): EO-atlas candidate, no EO row checked here.
- huh2016: 0.5-dB alignment tolerances of receptacle, lens, APD block, DMUX (p.5-9): no parameter (D250 rejected 0.5-dB tolerances),
  in component notes. 510 um pitch: value sentence cites the authors' ref. [7] (D408), note only. Receiver sensitivities (gap below).
  TIA values (electronics). Comparison with PLC AWG none numeric.
- cheung2019: dlambda per channel of Tables IV / V: width level not stated (gap below), in component notes. Table I other works.
  Table I / abstract summary values for the lattices (XT < -15 / < -20 in the abstract and conclusion; < -21 / < -23 in the intro and
  Table I; IL 0.1-2 and 0.1-1 dB): they disagree with each other and with the channel tables, so channel-table values are entered
  and the conflict is flagged. Sidewall 89 deg cites ref. [25] (rule 3). dneff/dw, dneff/dt, confinement: no parameter. Heater (800 nm
  Al, ratings only): geometry-only, no row. Hypothetical XT values ("if dispersion is neglected", "with broadband couplers"): out.
- palmer2026: Table I targets, Fig. 3-5 system simulations, Table II target wavelengths (specification of the grid, not a measurement).
  Table VI other works. 20-dB bandwidth, bandwidth ratio, frequency offset (gaps below, notes). Comparison AWG (Fig. 9a) and no-iris
  variant (Fig. 9b): no printed value, no row; side lobes not read off.
- xie2023: Table II other works. Bend transmission Fig. 3(c), GC response Fig. 7(c): no printed value. Effective index 2.7: no parameter.
- afzal2020: center wavelength not entered: Fig. 1(b) and 1(c) show different passband positions, no labelled value. Min feature ~150 nm
  (note).

## Missing orgs

None: org_zhejiang_university, org_electronics_and_telecommunications_research_institute, org_ligentec, org_broadex,
org_chongqing_united_microelectronics_center, org_globalfoundries are in the registry. Suppliers in notes only: Novel Si Integration
Technology (yi2024a).

## Judgment calls for the auditor

1. huh2016 wdm.tff fab = ETRI on the ROSA assembly statement (p.2, D399); filter / block maker not stated. Lens and APD rows fab empty.
2. huh2016 IL 0.5-0.8 dB author_estimate (rests on typical 0.8 A/W and approximate gain 1.4); bias_v stored negative from printed
   "reverse bias" values.
3. palmer2026 thermal drift: printed -1.8 GHz/K converted to +10.2 pm/K at 1303.5 nm (derived, inferred wavelength); alternative is to
   drop the row until a GHz/K parameter exists.
4. palmer2026 0.4 dB per interface: measured under D167, method unspecified; stated once with no derivation. Scope per_coupler on a new
   fiber_chip_coupler.edge row (the paper has spot-size converters + FAU; could be fiber_interface.fau). fpr_length_um holds focal length.
5. palmer2026 PDL: body 0.2 dB average (entered) vs "below 0.2 dB" in abstract and conclusion (note).
6. yi2024a and afzal2020 IL scope unspecified: GCs / couplers normalized out in the figures, method never stated.
7. yi2024a Design-2 and -4 crosstalk in crosstalk_db (Table 2 does not say adjacent, unlike Designs 1 and 3).
8. cheung2019 Gaussian crosstalk: three conflicting statements entered as three rows (< -25, ~ -30, < -35 dB). BOX 3.0 um (Table II) vs
   4 um (p.2) kept on separate rows. Lattice footprints abstract vs Fig. 9 labels conflict (notes); Design 1 uses the figure labels.
9. cheung2019 row_kind design for parts on the chips with only simulated values (edge coupler, bend, lattice Design 1, straight DC).
   coupling_variation from printed 2 % / 7 % read as coupling-ratio points from the Fig. 14 axis.
10. xie2023 grating coupler < 4 dB author_estimate (origin not stated; D418, D167 not extended). Footprint: Sec. III two AWGs vs Table II.
11. afzal2020 platform empty (SOI not stated, D422 / D423); yi2024a platform lnoi_rib.

## Registry gaps (skipped value, locator, proposed definition)

| parameter | value | locator | definition |
|---|---|---|---|
| bw_20db_ghz (wdm) | 479.5 +/- 20.0 GHz | palmer2026 p.7 Sec. VI | full passband width at -20 dB in frequency |
| bw_ratio_1db_20db (wdm) | 0.63 +/- 0.03, 0.67 best | palmer2026 p.7, p.8 Table VI | 1-dB / 20-dB bandwidth ratio |
| thermal_drift_ghz_per_k (wdm) | -1.8 +/- 0.3 GHz/K | palmer2026 p.8 | passband center frequency drift per kelvin, sign as printed |
| frequency_offset_ghz (wdm) | below 40 GHz | palmer2026 p.7 | passband offset from the target grid |
| bw_0p5db_nm (wdm; also lit_11, lit_27) | > 3 nm | huh2016 p.10 | full width within 0.5 dB of peak |
| rx_sensitivity_dbm (photodetector; also lit_68) | -22.4, -22.7, -22.7, -22.2 dBm at 1e-12, 25.78 Gb/s NRZ | huh2016 p.10 | optical input at a stated BER and rate |
| passband_width_nm, level unstated (wdm) | 8.97-17.40 and 10.039-18.89 nm | cheung2019 p.7 Tables IV, V | channel passband width where the level is not stated |
| angle_of_incidence_deg (wdm.tff) | 8 deg | huh2016 p.3 | filter angle of incidence |
