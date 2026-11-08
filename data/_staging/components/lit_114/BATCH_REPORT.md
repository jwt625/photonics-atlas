# lit_114 batch report (2026-11-08)

All seven cached texts match their source rows (page-1 title). None is a correction, an erratum or another paper. No
`garbled_text_layer` flag is set, but the lacava2016 text layer on p.3-p.6 is two-column interleaved: its values were
read from the page renders (`page_03/05/06.png`; there is no `page_04.png`, so the p.4 test-structure text was read from
the garbled text only). Figure values were read from the cached page renders. Dry-run: +20 components, +116 metrics,
0 errors. The one warning (ni2025b m18 / m4) is on an existing merged row, not from this batch.

| paper | components | metrics |
|---|---|---|
| gehring2019 | 1 (fiber_chip_coupler.other) | 18 |
| lacava2016 | 1 (fiber_chip_coupler.grating) | 15 |
| zhang2014 | 3 (fiber_chip_coupler.grating 2; waveguide_platform.straight 1) | 19 |
| ding2014 | 3 (fiber_chip_coupler.grating 2; waveguide_platform.straight 1) | 15 |
| zhong2026 | 3 (waveguide_platform.straight 1; fiber_chip_coupler.edge 1; fiber_interface.fan_out 1) | 16 |
| jung2020 | 6 (micro_optics.other 2; nonreciprocal.isolator 1; wdm.tff 2; splitter.other 1) | 13 |
| ma2015 | 3 (polarization.psr 2, of which 1 design; wdm.cascaded_mzi 1) | 20 |

## Not entered, and why

gehring2019
- SiN propagation loss 0.2 dB/cm (p.4): cited from the authors' earlier work (ref. 36), rule 3.
- Lens curvature 12 um (p.4): `lens_radius_um` is not allowed for fiber_chip_coupler (registry gap below); in notes.
- Round-section diameter 21 um and the 50 um shape transition (p.4): no parameter; in notes.
- Fig. 4 MZI / ring spectra: no values printed.

lacava2016
- Hole radius 179 nm (Table 1, p.3): no parameter (registry gap below).
- Port 2 (orthogonal output) level in Fig. 4 (about 25-50 dB under port 1): no value printed, not read.
- Simulation source MFD 10.4 um (p.2): a simulation input, not entered.

zhang2014
- Bottom DBR simulated reflectivity (> 94.8 % over 1400-1600 nm; > 90 % with 30 nm a-Si variation, p.3): the mirror is
  part of the coupler and `reflectivity_pct` is not allowed on fiber_chip_coupler. Notes only. No separate reflector row,
  because the mirror is a layer stack with no measured value.
- Coupling efficiency 56.0 % (p.6): this is the paper's conversion of the -2.5 dB row. Not entered twice.
- Simulated no-DBR coupling loss (2.72 dB worse than with the DBR, p.4): relative value only.
- Table 1 rows of refs. 17, 21, 22 (cited, rule 3).

ding2014
- Designs with D_hole,min 100 / 150 nm (Fig. 3, p.2): relative simulated degradation only.
- The variant with an 8 nm larger hole (Fig. 4(c)): it shifts the peak by 23 nm with no CE change. This is in notes; no
  separate row (no absolute value printed).
- The PhC lattice constant (2 d0 / 3 = 230 nm) and the slot width d0 345 nm: not entered. `subwavelength_period_nm` would
  need a unit conversion the paper does not print. In notes.
- Table 1 comparison rows (cited, rule 3).

zhong2026
- More than 90 % of the 16 devices have an average IL below 0.4 dB (p.5, Fig. 3(f)): a population fraction, not a value.
  In notes.
- Thermal IL variation over 30-75 C, PDL details and the ICXT matrices over C + L: Supplement 1 is not cached.
- Waveguide refractive-index contrast (1.9e-3 / 5.6e-3) and the diameter vs pulse-energy series (9.4-23.5 um): no
  parameter / process series. In notes.
- Transmission results (BER, received power): system results, not component metrics.
- Table 1 comparison rows (cited).

jung2020
- Modal purity / HOM content: SMF-HCF -21.2 dB LP11, -22.1 dB LP02 (p.3); HCF-HCF > 20 dB (p.4); splitter ports
  about 8.4 dB / 12 dB, > 20 dB after bending (p.6). No parameter for these classes (registry gap below).
- Back reflection of the isolator (-47 dB, p.3) and of the 3-port splitter (< -45 dB, p.6): `back_reflection_db` is
  not allowed for nonreciprocal / splitter (registry gap below). In notes.
- HCF attenuations (3.9 dB/km PBGF, 2.8 dB/km NANF): these are fiber properties, not components.
- Dichroic-chip band edges (1500-1564 / 1570-1620 nm): commercial design values. In notes.
- Abstract summary ranges (0.5-2 dB, -45 dB, > 20 dB): these cover all devices and are restated per device.

ma2015
- Total receiver passive loss about 6.2 dB (p.8): rests on a typical 0.75 A/W responsivity cited from ref. 39 and
  covers the edge coupler, the PSR, the DeMUX and routing. Not entered (no single component). In the PSR notes.
- Table 1 "+/-0.5 nm" and "entire spectrum" PDL rows (avg 0.68 / 0.72 dB): only the eye-diagram (mean, std) and
  peak-wavelength (mean) rows are entered. The other two rows are alternative readings of the same sweep.
- Improved-design wavelength dependence < 0.05 dB over 50 nm (p.10): `wdl_db` is not allowed for polarization (registry
  gap below).
- Bi-layer taper of the improved design (9 um, 97 % PCE): taken from the authors' earlier rotator (ref. 25), cited.
- Si edge coupler and bi-directional Ge PD of the receiver: no own values (the 0.75 A/W responsivity is cited).
- Time-skew estimate (0.2 ps for a hypothetical 100 um device): a hypothetical example, not a component.

## Fab / facility orgs

- lacava2016: CEA-Leti, `org_cea_leti` (p.1 abstract "fabricated by CEA-Leti"; p.3 cleanroom).
- zhang2014: IME A*STAR, `org_astar_ime` (Table 1 p.6 "IME's platform"; all authors IME, one also Jilin).
- ma2015: `org_astar_ime` on the prototype PSR and the DeMUX (p.6 "through an OpSIS-IME multi-project-wafer (MPW) run").
  process_name "OpSIS-IME MPW, 248 nm lithography, 8-inch SOI".
- jung2020: University of Southampton, `org_university_of_southampton` (all authors ORC Southampton; first-person
  fabrication account on p.2-5).
- Empty: gehring2019 (first-person fabrication, but the authors are at Muenster, KIT and HU Berlin and no org is named),
  ding2014 (passive "was fabricated", DTU + Rennes 1), zhong2026 ("we designed and fabricated", authors at six orgs).
- No facility is acknowledged in any of the seven papers. zhong2026 thanks a Shanghai University team for
  refractive-index characterization. This is measurement support, not a facility, so it is not entered.

Missing from the registry:
- "OpSIS" (MPW access provider; fab role), ma2015 p.6 Sec. 2 ("OpSIS-IME multi-project-wafer (MPW) run"). This one is
  already queued for the org round (D458 / D521).

Supplier notes only (not orgs to add): Corning Eagle XG glass (zhong2026 p.3); Hengtong Optical Fiber, the MCF
(zhong2026 p.5); Nanoscribe IP-Dip resist (gehring2019 p.4); commercial LPCVD SiN film and commercial SOI wafers, no
supplier named.

## Judgment calls

1. gehring2019 -2.07 dB mean (19 devices) and 0.35 dB std, scope `unspecified`. The text says neither per coupler nor
   per pair. The per-coupler reading fits Fig. 2(a): the best device is about -1.65 dB at 1550 nm, so a per-pair -2.07
   would beat it. The scope was not guessed (rule 6). Coordinator: accept `loopback_half` if you consider this
   deduction sufficient.
2. gehring2019 x / y tolerance. The printed "-1 dB range about 5 um" is the full window. Fig. 3(c) crosses at about
   +/-2.4 um, so it was halved to 2.5 um, `derived` (caillaud2021 / D469 precedent). The z value of 34 um is kept as
   printed: the text phrases it as a displacement, and the Fig. 3(b) contours are illegible.
3. gehring2019 platform `polymer` (light is guided in the IP-Dip coupler; the SiN feed is in core_material), class
   `fiber_chip_coupler.other` (3D-printed out-of-plane coupler, D138). The 1.6 dB best value is a figure read added
   next to the printed "< 1.8 dB". `fiber_angle_deg` 12 is the coupler beam angle from vertical (the fiber array is
   8-deg polished), with a note.
4. lacava2016 and gehring2019 per-coupler values printed by the paper as half of a two-coupler measurement:
   `loopback_half`, basis `measured` (the paper prints the halved number). The lacava2016 peak wavelength is not
   printed. 1560 nm (the 3-dB band centre) was used with `wavelength_inferred`. The 44 nm 3-dB BW is kept on the GC row.
   The abstract gives 43 nm and the conclusion ties it to the closed loop; both are noted.
5. ding2014: the simulated -0.43 dB / 76 nm (D_hole,min 70 nm design) are kept on the fabricated row, because the
   Fig. 4(c) "As designed" curve is that design. Back reflection < 1.4 % was converted to > 18.5 dB, `derived`. Upper
   cladding = BOX thinned to 1 um (after flip bonding). Lower cladding hd 1.6 um goes in `box_thickness_um`.
   The reference GC without the mirror (-5.6 dB) is a figure read.
6. zhong2026: one physical waveguide is split into two rows, `waveguide_platform.straight` (propagation loss) and
   `fiber_chip_coupler.edge` (per-facet coupling and +/-2 um tolerance), with cross-notes (D396). This is because
   `tol_1db_*` is not allowed on waveguide_platform. FIFO IL scope `device_total`: the main text does not describe the
   measurement configuration. The ICXT after 115 km (-39 dB) includes link crosstalk; the condition says so.
7. jung2020: in scope as fiber-coupled passive parts (D411). Platform `other` (fiber + free-space micro-optics; the
   guiding media are stated). The interconnects are `micro_optics.other`. The BPF and the dichroic WDM are `wdm.tff`.
   The 50/50 splitter is `splitter.other`, with `excess_loss_db` scoped `device_total` and the chip IL in `includes`.
   The BPF 7 nm / 1548 nm are `specification`: they are stated as properties of the inserted chip.
8. ma2015: the receiver-level PDL (Table 1, 10 Gb/s and 40 Gb/s) is entered on the prototype PSR row. The paper uses
   it to prove the PSR, and the condition lists every component in the path. The 6.2 dB receiver loss is not entered.
   Coordinator: move the PDL rows to notes if a system-level PDL should not rank a PSR. The improved PSR is
   `row_kind: design`. Its polarization crosstalk of about -17 dB is stored as `per_db` (merged precedent chen2021,
   gao2026).

## Registry gaps (skipped value + locator + proposed definition)

- `hole_diameter_nm` (already a candidate, D431), widen to fiber_chip_coupler: lacava2016 radius 179 nm (p.3 Table 1),
  ding2014 D_hole,min 70 nm (p.2). Definition: "diameter of photonic-crystal / 2D-grating holes (radius values
  doubled, derived)".
- `lens_radius_um` widen to fiber_chip_coupler: gehring2019 12 um lens curvature (p.4) on a 3D-printed coupler.
- `mode_purity_db` (micro_optics, fiber_interface, splitter, mode_converter): jung2020 HOM content -21.2 / -22.1 dB
  (p.3), > 20 dB (p.4), 8.4 / 12 dB (p.6). Definition: "power ratio of the fundamental mode to the strongest (or total)
  higher-order mode at the output, positive dB (method, e.g. time-of-flight, and fiber length in condition)".
- `back_reflection_db` widen to nonreciprocal and splitter: jung2020 isolator -47 dB (p.3), 3-port splitter < -45 dB
  (p.6).
- `wdl_db` widen to polarization: ma2015 improved PSR < 0.05 dB over 50 nm (p.10, simulated).
