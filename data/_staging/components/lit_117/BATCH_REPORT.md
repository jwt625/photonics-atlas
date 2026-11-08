# lit_117 batch report (2026-11-08)

All five cached texts match their source rows (page-1 title); none is a correction, an erratum or another paper; no
garbled text layer is flagged. Figure values were read from the cached `page_NN.png` / `img_*.png` renders. Dry-run:
+11 components, +93 metrics, 0 errors; the one warning (ni2025b m18 / m4) is on an existing merged row, not from this
batch.

| paper | components | metrics |
|---|---|---|
| xie2026 | 3 (wdm.awg 1; splitter.mmi 1; fiber_chip_coupler.edge 1, reference structure) | 24 |
| zhuang2016 | 2 (wdm.interleaver 1; fiber_chip_coupler.edge 1) | 15 |
| douglass2018 | 2 (wdm.awg 1; waveguide_platform.straight 1) | 15 |
| horst2013 | 1 (wdm.cascaded_mzi) | 16 |
| shi2013a | 3 (wdm.bragg_cdc 3: conventional contra-DC, AR contra-DC, 4-channel CWDM demux) | 23 |

## Fab / facility orgs

- horst2013: fab `org_ibm` (p.5 Sec. 3: fabricated using the IBM CMOS Silicon Nanophotonics process; abstract: 90 nm
  CMOS-integrated technology; p.2: commercial production line). `process_name` "IBM CMOS Silicon Nanophotonics process
  (90 nm CMOS-integrated)". The authors sit at IBM Research Zurich, IBM Watson and IBM Microelectronics (Essex
  Junction); the parent `org_ibm` is used as the process owner (D154 analogue); the coordinator may prefer a sub-unit.
- xie2026: fab empty. p.8 Sec. 3: lithography process with 350 nm resolution "provided by IOPTEE". Missing org:
  **IOPTEE** (as printed, p.8 Sec. 3; role fab). Not a named PDK, so `process_name` is empty.
- zhuang2016: fab empty. p.12 Appendix: fabricated using TriPleX, proprietary to LioniX B.V.; p.13 Acknowledgments:
  chip provided by SATRAX B.V. and LioniX B.V. **LioniX B.V.** is deliberately kept out of the registry (D278; lit_16
  audit mu2016 precedent); **SATRAX B.V.** (Enschede, Netherlands; p.1 affiliation, p.13; role fab, "chip provided by")
  is missing. `process_name` "TriPleX (two-strip geometry)".
- douglass2018: fab empty (passive fabrication description, authors at Macquarie University and Fraunhofer IOF).
  Missing facility: **OptoFab node of the Australian National Fabrication Facility** (p.9 Acknowledgments, "performed in
  part at"; role facility).
- shi2013a: fab and facility empty. p.6 Acknowledgement: fabrication conducted at the **University of Washington
  Microfabrication/Nanotechnology User Facility** (member of the NSF NNIN) - missing; role fab and facility (D448:
  acknowledged processing site). The owner `org_university_washington` is not entered (owner of a named facility is not
  a facility).

## Not entered, and why

xie2026
- FSR: not printed (two FSRs shown in Fig. 10(a)); measured channel spacing not printed (20 GHz entered as the Table 1
  design value, author_estimate). Passband widths not printed.
- Simulated bend transmission 98.5 % (1.2 um wide) / about 96 % (2.5 um wide) at R = 80 um (p.3, Fig. 2(c)-(d)): the
  bend angle of the simulated structure is not stated, so `bend_loss_db_per_90` cannot be used.
- Taper vs straight transition "about 5.6 % higher" slab TE0 coupling (p.5): relative simulated gain, no parameter.
- Anisotropy analysis (delta n_eff 0.00692 at 15.36 deg tilt, 0.685 um equivalent length, 0.19 % of delta L; p.6-7):
  design analysis, no parameter.
- MMI simulated near 50:50 / near 100 % (Fig. 3): no number printed.
- Designed centre wavelength 1.55 um (Table 1): note only (measured response 1553-1559 nm).
- Table 2 values of other works (rule 3).

zhuang2016
- -25 dB bandwidth 13.5 GHz (Fig. 1(d)) and 10-90 % (-0.5 to -10 dB) resolution close to 0.5 GHz (p.6): no registry
  parameter (gap below). 8 % roll-off: no parameter.
- FSR deviation about 0.02 % over 10 FSRs; passband centre deviation about 0.1 % of the FSR (p.7, p.12): no parameter.
- Table 1 coupler / phase settings (kappa 0.5 / 0.87 / 0.32): operating settings of tunable couplers, in notes.
- MZ coupler length 3450 um and the 675 um directional couplers: notes (whether 675 um is the straight coupling section
  is not stated).
- Ring length 1.4 cm: no ring-length parameter (`radius_um` would need a geometry not stated); in notes.
- Propagation loss around 0.1 dB/cm and < 1 dB/facet tapered coupling: cited (refs. [24, 37], [40, 42]).
- System results (OSNR penalties 0.1 dB, < 0.5 dB, < 1 dB; Q values): link-level, not component metrics.
- Strip thickness printed "170 um": evidently 170 nm, kept in `core_material` with the typo noted, not entered as a
  metric.

douglass2018
- Resolving power 468.7 measured vs 532 design (p.6): no registry parameter.
- Central-wavelength shift 7.7 nm (p.5): sign relative to 632.8 nm ambiguous from the text (Fig. 3 compares the 632.8 nm
  output with a 640.5 nm simulation); in notes.
- Bend loss vs radius (Fig. 2, dB/cm, measured R 10-40 mm; simulated 0.050 dB/cm at 26 mm, 0.024 dB total) and the
  1.05 dB total loss of the longest array arm (p.4): no bend-loss-per-length parameter; figure points not labelled.
- Phase error +/- 95 nm equivalent length error, lateral FPZ drift 12-14 um, slab index uniformity 1.97 %, peak index
  contrast 1.5e-3: no parameters (notes).
- Photonic lantern (15 mm, 3 ports, 35 um output spacing) and the lantern-AWG chip: no quantitative performance, no row
  (rule 9). Physical FSR 80.7 um: no parameter.
- Polarization-dependent shift 0.01 nm: expected from a cited birefringence (ref. [21]), not entered.

horst2013
- Passband flat within 0.7 dB over 2.4 nm for all 8 outputs (p.6-7): a 0.7-dB width has no parameter and is not
  converted to `bw_1db_nm` (gap below).
- Stop band wider than 1.9 nm at the 15 dB extinction level (p.7): `stopband_width_nm` is reflector-only (gap below).
- Extinction "limited to about 15 dB" (p.7 discussion): summary of the same data as the 18 dB row, in notes.
- Temperature tolerance > 25 degC (p.7): no parameter.
- Cross-coupling length 66 um (p.5): characteristic transfer length, not `coupling_length_um`.
- Phase error -0.1 delta L_FS in one delay line (p.7): model fit, no parameter.

shi2013a
- AR contra-DC stop-band width 6.5 nm (p.4, Fig. 3(b)) and demux channel bandwidths 11-13 nm (p.5; abstract "up to
  13 nm"): width level not printed (D-precedent: a width with no stated level is not entered); gap below.
- AR contra-DC: single stop band over 180 nm span (no FSR): no parameter. lambda_D of the AR device not printed (about
  1560 nm in Fig. 3(b), not read as a value).
- Predicted drop wavelengths 1530-1590 nm (Fig. 5(b)): in notes; the 20 nm spacing is entered as simulated.
- Temperature swing +/- 60 K: estimate from a cited 0.09 nm/K (ref. [3], rule 3).
- Corrugation widths / amplitudes (20 / 30 nm; 30 / 40 / 50 nm) and 50 % duty cycle: `fill_factor` is not allowed on
  wdm; in notes.

## Judgment calls

1. xie2026 MMI: the printed "insertion loss 0.16 dB after normalization" is entered as `excess_loss_db` (rule 6)
   because Fig. 8(b) shows the output-port trace at about -3.2 dB near 1550 nm; scope `per_component`, method
   `reference_structure`, with a note that the paper does not say how the cascade is reduced to one MMI.
2. xie2026 channel spacing 20 GHz: `author_estimate` (Table 1 design); the paper never prints a measured spacing.
3. xie2026 edge-coupler reference row: fiber-to-fiber loss about 14.5 dB read off Fig. 9(c) at 1550 nm (+/- 0.5 dB);
   coupler geometry not described; platform taken from the chip stack.
4. douglass2018 FSR 22.2 nm: `author_estimate` (D435) - extrapolated from peaks spanning 12.8 nm, less than one FSR,
   although the abstract calls it measured.
5. douglass2018 throughput 3.97 % / 11.5 % converted to 14.01 / 9.39 dB, `author_estimate`: the removed 14.48 %
   coupling loss is a calculated mode overlap (rule 4); scope `de_embedded`.
6. zhuang2016: about 4 dB/facet entered as a separate `fiber_chip_coupler.edge` row (`author_estimate`, origin not
   stated); the 9 dB total stays on the interleaver row as `fiber_to_fiber`. `extinction_db` 25 dB used for the
   passband-stopband extinction (the paper also calls it adjacent-channel extinction); wavelength range converted from
   191.5-196 THz.
7. zhuang2016 heater power about 150 mW/heater: `tuning_power_mw`, `measured`, statistic mean (method not stated).
8. horst2013 centre wavelength: design 1490 nm (`author_estimate`) plus a `derived` 1494.7 nm from the printed 4.7 nm
   measured shift. IL range 0.4-1.6 dB scoped `de_embedded` (normalized to an adjacent straight waveguide).
9. shi2013a is the journal extension of the authors' Group IV Photonics 2012 paper (ref. [13]); Sec. 2 contra-DC values
   kept (D259 journal-extension clause). The Sec. 2 geometry is entered on the AR row only (the text does not state
   which parameters the conventional device shares).
10. Platform: horst2013 `soi` (strip vs rib not stated); shi2013a `soi_strip` (sidewall-corrugated strip waveguides
    stated); xie2026 `lnoi_rib`; zhuang2016 `sin`; douglass2018 `glass`.

## Registry gaps (proposals)

- `bw_level_unspecified_nm` (wdm, reflector): passband / stop-band width as printed when the paper gives no level
  (shi2013a 6.5 nm p.4 Fig. 3(b); 11-13 nm p.5). Alternative: allow `stopband_width_nm` on wdm with the level in
  condition "not stated".
- `bw_xdb_ghz` / generic `bw_at_level_ghz` with the level in condition (wdm): zhuang2016 13.5 GHz at -25 dB (p.6,
  Fig. 1(d)); horst2013 2.4 nm within 0.7 dB (p.6-7) as its nm counterpart.
- `rolloff_ghz` (wdm): 10-90 % transition width as defined by the paper (zhuang2016 close to 0.5 GHz, p.6).
- `stopband_width_nm` extended to wdm (level in condition): horst2013 > 1.9 nm at 15 dB extinction (p.7).
- `bend_loss_db_per_cm` (waveguide_platform.bend): bend loss per unit length at a stated radius (douglass2018 Fig. 2,
  simulated 0.050 dB/cm at 26 mm, p.4).
- `resolving_power` (wdm, unit 1): lambda / delta lambda as printed (douglass2018 468.7 measured, 532 design, p.6).
