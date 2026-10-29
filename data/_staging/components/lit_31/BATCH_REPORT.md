# Batch lit_31 report (distill subagent, 2026-10-29)

Dry-run `batch lit_31: +49 components, +409 metrics; errors 0`. ASCII, no e-mail, no verbatim quotes (all ten sources
`restricted_local_only`). Page-1 title / authors checked for all ten texts: each matches its source row. No
`garbled_text_layer` flags. Tables read from page renders (pathak2014 Table I and dheer2018 Table I re-rendered at 220-300
dpi from `source.pdf`; liu2020 Table 1 from `page_05.png`).

## Per paper (components / metrics)

- arafat2024 (3 / 31): single-stage asymmetric MZI 2-channel filter on 400 nm SOI at 2 um (wdm.cascaded_mzi: FSR 13.45
  measured / 13.69 design, ER 25 dB max, 11 / 9.5 dB port suppression with printed PDs, MMI 62 x 6 um, dL 60 um, ng 4.63
  simulated), 2 um GC (6 dB fiber-to-fiber, 4.5 dB input GC author_estimate from a simulated 1.5 dB output term, 3 dB
  simulated, geometry), transfer-printed InGaAs QW PD (photodetector.iii_v_on_platform: 15 nA / 0.76 mA/cm2 at -2 V,
  0.4 A/W top-illuminated, QE ~25 % derived, 0.1 A/W system). Not entered: GC simulated 100 nm bandwidth (width
  definition not stated), 2x2 MMI (equal splitting, no number; geometry put on the MZI row), PD 28 % / 25 % absorption
  split (no parameter), simulated 69 % / 43 % InterVia coupling. Fab: Tyndall on the PD row only (authors transfer
  printed the PDs, D399); SOI circuit fab not stated.
- gebregiorgis2023 (2 / 37): apodized straight and curved contra-DC filters (wdm.bragg_cdc): IL / SLSR mean and SD over 4
  wafer sites (Table 1), crosstalk 32 / 25 dB, channel spacing 15.8 nm, spectral-position SD as wavelength_spread_nm,
  3D-FDTD channel centres and SLSR (simulated), geometry (bus 250 / drop 400 nm, G0 250 nm, periods 307 / 314 nm, LC,
  footprint per channel, CDBR N = 450). Not entered: BW 7.2 / 7.1 nm (width definition not stated), mean shift vs
  simulation 0.7 / 1.3 nm (no parameter), apodization factor. Fab org_globalfoundries (MPW university program); KU HPC
  facility not a fab facility.
- liu2020 (4 / 35): 8-ch thermo-optic SOI AWG at 2 um (IL 6.1-7.8 dB, 1.6 nm spacing, 6.4 pm/mW derived from 6.4 nm/W,
  2.3 nm shift at 360 mW, Table 1 design values), TiN heater array (4400 ohm measured, 3630 ohm calculated, geometry),
  20 um bend (0.012 dB/90 deg simulated), focusing GC (~7 dB per facet, -4.5 dB simulated, period / fill factor).
  Not entered: Rowland diameter 120 um and 1.5 um array spacing (fpr_length / pitch roles not stated), measured centre
  offset 27 nm (sign not stated), COMSOL 0.125 K/mW. Fab empty (unnamed MPW shuttle).
- pathak2014 (12 / 136): six AWG configurations (4 / 8 / 16 ch x 200 / 400 GHz) each on a 5 nm and a 1 nm mask grid =
  12 sibling rows (grid snapping changes the layout, rule 9), each with Table I IL range (de_embedded, normalized to a
  straight waveguide with the same GCs), crosstalk floor (crosstalk_db, paper definition), cumulative crosstalk, FSR,
  footprint, design counts; 16-ch rows also the delay length. Not entered: abstract averages over devices (D254),
  simulated 12 dB improvement (a difference), 800 / 450 nm widths (roles not stated). Fab org_imec (authors state they
  fabricated on 200 mm SOI in imec's platform; bogaerts2006 precedent, borderline).
- dheer2018 (6 / 32): 16x16 liquid-controlled non-volatile switch, dilated switch element, 820 um LCC (all
  switch_fabric.other, D158), rib crossover (crossing.other), interconnect waveguide, SiON-overlay edge coupler. Table I
  per-unit losses at 1550 nm entered as measured (test structures) except SE bar 0.4 dB (sum, derived) and SE cross 0.6
  dB (origin not stated). Fab empty (fabricating org not stated; thanks to a person for fabrication help without
  affiliation).
- gao2025a (9 / 52): 2x2 MZI switch with PIN phase shifters (switch_fabric.other: TE0 / TM0 IL per state and path,
  crosstalk, PDL < 1.87 dB derived, rise / fall in us derived from ns), polarization-insensitive adiabatic 3-dB coupler
  plus four deliberate-deviation siblings (Table 1 split-ratio ranges), PIN phase shifter, TM0-TE1 converter and taper
  (simulated only, row_kind fabricated per D80e). Fab org_amf.
- han2015 (4 / 30): 50x50 MEMS crossbar switch (27.5 dB longest path), unit cell (ER 26 / 25 / 22 dB, -20 dB through-port
  width 13 nm as xt_bandwidth_nm, rise / fall 2.5 / 3.8 us, 179 kHz calculated), movable DC (geometry, 430 nm measured
  width, simulated ER), MMI crossing (0.04 dB cutback, 0.015 dB / 66 dB simulated). Not entered: projected 4 dB IL,
  pull-in 24 V, 14 V actuation. Fab org_university_of_california_berkeley (authors fabricated, all UCB); no facility
  statement.
- xia2026 (4 / 20): 1x8 InP SOA multicast-and-select switch (ER > 35 dB, 23 dB passive system loss derived, PDL < 1.8 /
  2.5 dB), the switch path as amplifier.soa (D396: net fiber gain 5.5 / 0 dB, on-chip 30 / 23 dB author_estimate, NF 6.6
  dB, Psat out 9.5 dBm / in -10.5 dBm, output power), 1x8 MMI tree (11 dB incl. 9 dB split), lensed-fiber facet (~6 dB).
  Not entered: conclusion ER > 60 dB (contradicts > 35 dB), OSNR / penalty / cascadability (system). Fab empty
  (foundry not named; MCS design attributed to ref. 8).
- yamaguchi2024 (2 / 19): single 64x4 and twin 32x4 silica-PLC multicast switches (switch_fabric.other): mean IL at
  1500 / 1568 / 1612 nm, < 8 dB all paths, ER > 40 dB (also 1400-1700 nm spectra), PDL, port counts, chip area. Not
  entered: WDL (registry gap), Fig. 4 model losses. Fab empty (FHD + RIE stated passively, D80b).
- zali2026 (3 / 17): 8x8 InP SOA broadcast-and-select switch (ER > 55 / ~50 / 52 dB, ports, chip area), the path SOAs as
  amplifier.soa (path gains as author_estimate because the gain uses passive losses partly from literature; ASE 3-dB
  width 74-86 nm; 60 um pitch), InP crossing ~0.25 dB (author_estimate). Not entered: PDG (gap), OSNR, BER penalties /
  dynamic range, conclusion 20-25 dB gain (family statement). Fab org_smart_photonics (authors fabricated with the SMART
  Photonics platform, two Smart Photonics co-authors). Supplement 1 not cached.

## Missing organizations

None needed for fab / facility fields. Named only in acknowledgments, not entered: Munster Technological University
(arafat2024 p.4, person thanked), Bartels Mikrotechnik GmbH and Technische Universitat Ilmenau (dheer2018 p.4, EWOD design
rules).

## Judgment calls

- arafat2024: printed GC duty cycle 4 % kept as 0.04 (derived, D253) and flagged as atypical (possible typo); port
  suppression 11 / 9.5 dB entered as extinction_db because the paper compares it directly with the 25 dB ER.
- gebregiorgis2023: SDBR IL wavelength 1290 nm from the text although the Table 1 caption says lambda1; one row per
  configuration with the two channel periods as conditions (the per-channel devices have no separate measurements).
- pathak2014: grid-variant siblings as separate rows; Table I XT entered as crosstalk_db (crosstalk floor, not adjacent /
  non-adjacent by definition); 4- and 8-ch rows `band unspecified` (only the 16-ch spectra are plotted).
- dheer2018 / gao2025a: single 2x2 elements and the LCC as switch_fabric.other (D158); PIN phase shifter as
  phase_shifter.other (carrier injection, simulated only; qiao2017 precedent keeps PIN switches out of the EO atlas).
- xia2026 / zali2026: SOA switch paths duplicated as amplifier.soa rows (D396) to hold gain / NF / Psat; zali2026 gains
  author_estimate (passive losses partly from literature, D44).
- han2015: through-port -20 dB width entered as xt_bandwidth_nm (level and state in condition).
- gao2025a PDL < 1.87 dB derived (equals the 2.79 - 0.92 dB IL difference).

## Registry gaps

| proposal | skipped value(s) and locator | proposed definition |
|---|---|---|
| pdg_db (amplifier, switch_fabric) | zali2026 PDG < 3 dB over the C band (p.1 Abstract), 1-1.9 dB path 1I-5O 1520-1570 nm (p.6 Fig. 3(b)), 2.1 / 3.4 dB path 2I-8O (p.6) | polarization-dependent gain: max - min output power over input polarization states of an amplifying path, positive dB (conditions: input power, bias) |
| wdl_db for switch_fabric | yamaguchi2024 WDL 0.03-0.60 dB over all paths of the 64x4 (p.5 Fig. 8(d)), max 0.73 dB twin 32x4 (p.6 Fig. 10(d)) | existing wdl_db definition (max - min loss over the stated wavelengths) |
| dgd_ps for switch_fabric | gao2025a simulated DGD < 0.08 ps, 1520-1580 nm (p.7 Fig. 3(b)) | existing dgd_ps definition, path and switch state in condition |
| corrugation_width_nm (wdm, reflector) | gebregiorgis2023 maximum corrugation width dW0 = 80 nm (p.8 Sec. 2.2, p.9 Fig. 5 caption) | sidewall grating corrugation (perturbation) width of a Bragg / contra-DC grating; maximum value for apodized gratings |
| fill_factor for wdm | gebregiorgis2023 grating duty cycle 50 % (p.4 Sec. 2) | existing fill_factor definition extended to wdm gratings (contra-DC, Bragg) |
| center_wavelength_nm for amplifier | zali2026 ASE centre 1535-1545 nm at 100 mA (p.5 Sec. 4.1) | peak / centre wavelength of the ASE or gain spectrum |
| switch_voltage_v (switch_fabric) | han2015 drop-state actuation near 14 V (p.4 Sec. 3.B), calculated pull-in 24 V (p.3); gao2025a operating biases 1.01 / 0.91 V (p.9) | electrical drive voltage that sets the stated switch state (actuation / pull-in / operating bias; definition in condition) |
| osnr_db (amplifier, switch_fabric) | zali2026 OSNR 44-54 dB at 1530 nm and 50-55 dB at 1570 nm over paths (p.9 Fig. 8(i)); xia2026 33.85-35.14 dB (p.6 Fig. 7(a)) | output optical signal-to-noise ratio at the stated input power, bias and reference bandwidth |
