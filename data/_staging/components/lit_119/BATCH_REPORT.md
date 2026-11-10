# lit_119 batch report (2026-11-09)

All seven cached texts match their source rows (page-1 title); none is a correction, an erratum or another paper; no
garbled text layer is flagged. Figure values were read from the cached `page_NN.png` renders. All seven sources are
`restricted_local_only`: facts and locators only, no quotes beyond a few words. Dry-run: +28 components, +220 metrics,
0 errors; the one warning (ni2025b m18 / m4) is on an existing merged row, not from this batch.

| paper | components | metrics |
|---|---|---|
| parra2020 | 7 (phase_shifter.thermo_optic: 3 fabricated ITO heaters (TE 150 / 50 um, TM 150 um), 4 design rows (ITO / Ti x TE / TM, Table 2)) | 70 |
| piyush2026 | 3 (phase_shifter.thermo_optic 2: W heater test MZI, diode-assisted microheater; splitter.other 1: programmable 1x4 MZI tree) | 21 |
| fatema2026 | 4 (photodetector.apd 3: 50 x 120 / 50 x 100 / 50 x 80 um; fiber_chip_coupler.edge 1, simulated only) | 22 |
| goyvaerts2020 | 5 (fiber_chip_coupler.grating 2; photodetector.iii_v_on_platform 2; wdm.awg 1) | 51 |
| tabatabaei2026 | 4 (photodetector.iii_v_on_platform 3: 29 x 44, 34 x 34, VGC 80 x 290 um; fiber_chip_coupler.edge 1) | 31 |
| lukin2019 | 3 (resonator.ring 1; frequency_converter.shg 1; resonator.photonic_crystal 1) | 17 |
| liu2024a | 2 (waveguide_platform.straight 1; fiber_chip_coupler.edge 1) | 8 |

## Fab / facility orgs

- parra2020: fab `org_upv` on the 3 fabricated rows ("we propose, design and fabricate", p.2 Sec. 1, first person; all
  authors at the Nanophotonics Technology Center, UPV). Missing org: **Nanophotonics Technology Center (NTC),
  Universitat Politecnica de Valencia** (p.1 affiliation; role fab, child of `org_upv`; same gap as D533
  garciarodriguez2017). Design rows: no fab.
- piyush2026: fab `org_imec`, `process_name` "imec iSiPP50G" on all 3 rows (p.6 Sec. 2.3 and p.18 Sec. 4: fabricated
  using IMEC's iSiPP50G platform). IZMO Microsystems (Bengaluru) is thanked for electrical packaging assistance
  (p.23): note only, not a fab of the photonic parts.
- fatema2026: fab empty (first-person "we spun" SU-8, p.3, by authors at University of Virginia and University of
  Maryland; no fabricating org named, D154).
- goyvaerts2020: fab `org_imec`, `process_name` "imec BioPIX 300 nm" on the 2 GC rows and the AWG ("made in the
  commercially available imec BioPIX-300 nm platform", p.1 Abstract; p.3). PD rows: fab and process empty (coupon
  processing and transfer printing described with passive verbs, no org named; D80b, D450 precedent).
- tabatabaei2026: fab empty on all rows (first-person "we removed the top cladding", p.5, by authors at UVA, UCSB and
  Honeywell; waveguide wafer process passive, no org named; D154 / D80b).
- lukin2019: fab `org_stanford_university` (contributions p.6 name D.M.L. and C.D., both Stanford, for platform and
  fabrication; first-person Methods; D395); facility `org_stanford_nanofabrication_facility;
  org_stanford_nano_shared_facilities` ("performed at" SNF and SNSF, p.6; pre-merger names, D80d). Cree SiC wafer and
  CuttingEdge Ions implantation service in notes.
- liu2024a: fab empty ("we fabricated", p.2, authors at SJTU, Shanghai Optoweave Technology, TTM Technologies and Peng
  Cheng Laboratory; D154).

## Not entered, and why

parra2020
- Driving voltages 14.5 V (150 um) / 9.1 V (50 um) (p.8): the paper does not tie them to the pi phase shift
  explicitly; in component notes, not as `v_pi_v`.
- TM switching time 6.8 us (660 nm cladding, p.9): heater length not stated, both lengths exist on that sample (D159);
  in the TM row notes.
- Pi-tau FOM 52 mW us (p.10): product of entered values, in notes. Fig. 4 / 5 / 6 simulation curves vs gap (TE P_pi
  ranges 8-11 / 19-32 / 120-165 mW per cladding) not entered (curves, not designs).
- Fabricated Si thickness and BOX are only labelled in the Fig. 1(b) design cross-section: entered as
  `extracted_from_figure` with that note.

piyush2026
- Diode metrics (measured series resistance 11-12 ohm, breakdown -13.5 V, leakage about 3.5 nA, cut-in 0.9 V; TCAD
  6-7 ohm, -15 V): no phase_shifter parameter (registry gap below); in the DAM row notes.
- Split deviation after correction: +/-0.15 / +/-0.25 dB (p.18 body) vs +/-0.015 / +/-0.025 dB (abstract, conclusion):
  conflict, and D401 keeps split deviations out of `imbalance_db`; in notes.
- Heater TCR 1.66e-3 /K, dn_eff/dT 1.76e-4 /K: no parameter; notes. Typical 160 ohm heater (p.5) cited (ref. 24).
- P_pi 29 mW (24 devices, p.4) entered on the W heater row with the note that the heater length of those devices is
  not printed; the coordinator may move it to notes if D159 is read strictly.

fatema2026
- Eye diagrams (60 x 150 um APD): no parameter, no row. RC-limited 9 GHz (calculated): notes. Depletion width 1440 nm,
  punch-through -17 V: notes. Table 1 values of other works: not entered.
- Absorber length / width not entered: which mesa side lies along the waveguide is not stated.
- Dark current 5 nA, breakdown -26 V and the about 1e-12 A/um2 density are on the 50 x 120 um row: the Fig. 4(a)
  device is "6000 um2", which among the measured sizes only 50 x 120 um matches (inferred, noted).

goyvaerts2020
- AWG "1 nm channel width" (definition not stated): notes. Measured center offset 6.5 nm (direction not printed):
  notes. The PDs printed on the AWG outputs have no own metric (photocurrent spectra only): no row.
- Dark current / series resistance statistics are pooled over printed PDs of both test sites: entered on both PD rows
  (D465 analogue), flagged in notes.
- EQE 47 % at 860 nm entered as printed although 0.30 A/W at 860 nm corresponds to about 43 % (noted).

tabatabaei2026
- VGC-PD coupling efficiency 48 % (author estimate from a calculated 0.69 A/W): no photodetector coupling-efficiency
  parameter; in notes. VGC geometry (period 3.164 um, 70 x 250 um, duty cycle 92 % -> 50 %) in `core_material` of the
  VGC PD row (chen2018a precedent: PD-on-grating rows keep the grating in core_material).
- Simulated back-reflection < 3 %, etch-stop absorption < 5 %: notes.
- Bottom cladding 15 um (Sec. 3) vs 12 um (Fig. 1(a), Fig. 8(a)): 15 um entered with the conflict note (D417).

lukin2019
- PhC cavity mode volume, Purcell lower bound, lifetimes, intensity enhancement, g2(0): no parameters; notes.
- SHG ring radius 27.5 um: `radius_um` not allowed for frequency_converter; notes (gap below).
- Supplementary Information not cached: the SHG efficiency is waveguide-referred with a coupler correction described
  only there, so 360 %/W is author_estimate.

liu2024a
- PAM4 link results (112 / 120 Gbps, power penalty < 1 dB, TDECQ 0.9 dB), 150 C thermal test, 250 um core pitch: notes.

## Judgment calls

- parra2020 IL "< 0.01 dB": the p.8 sentence mixes "measured ... negligible" with "in agreement with simulations
  (< 0.01 dB)"; entered as author_estimate on every fabricated row. The Table 2 designs (not fabricated at those
  lengths) are 4 `row_kind: design` rows.
- Responsivities referred to the waveguide with the paper's own measured coupling loss (goyvaerts2020 reference GCs,
  tabatabaei2026 2.8 dB) are `derived` (D394 analogue); with a simulated coupling loss (fatema2026 2.94 dB) or an
  unstated correction (tabatabaei2026 VGC PD) `author_estimate`.
- tabatabaei2026 2.8 dB fiber-chip loss: per_facet + measured (stated without arithmetic, D167); the per-facet scope
  follows from its use to correct the input power.
- tabatabaei2026 157 fF assigned to the 34 x 34 um2 PD via the Fig. 6(b) legend ("the smallest PD").
- lukin2019 ring Q wavelengths and liu2024a / goyvaerts2020 band ranges: read off figure axes, `wavelength_inferred`.
- liu2024a board-level polymer waveguide on FR-4 kept in scope as a fiber-coupled passive part (D411).
- piyush2026 1x4 programmable splitter classed `splitter.other` (tuning power and split, not switching).

## Registry gaps (proposed)

- `series_resistance_ohm` and `breakdown_voltage_v` for phase_shifter (diode-assisted heaters): piyush2026 diode
  11-12 ohm (measured, p.10) and -13.5 V (p.10). Definition as for photodetector.
- `radius_um` for frequency_converter (ring-resonator SHG): lukin2019 27.5 um (p.3). Precedent: mckenna2022 SHG
  racetrack reclassed to frequency_converter (D252) also loses its geometry.
- `coupling_efficiency_pct` for photodetector (waveguide-to-PD grating / coupler efficiency): tabatabaei2026 48 %
  (author estimate, p.7); goyvaerts2020 simulated 44 / 56 % entered as `quantum_efficiency_pct` (the paper equates
  EQE with it, Eq. (2)).

## Missing orgs

- Nanophotonics Technology Center (NTC), Universitat Politecnica de Valencia: parra2020 p.1 affiliation and p.2 Sec. 1
  (fab).
