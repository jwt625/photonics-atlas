# lit_128 batch report (distiller, 2026-11-12)

Family: mode_converter / resonator / splitter / crossing / wdm. Seven papers, all `restricted_local_only` (facts and
locators only). Page-1 titles checked against the source rows: all seven cached texts are the paper of their row (no
correction / erratum). Validator: `merge_component_staging.py data/_staging/components/lit_128 --dry-run` -> +27
components, +183 metrics, 0 errors (the only warning is a pre-existing one on merged ni2025b rows).

| paper | components | metric rows |
|---|---|---|
| yang2024a | 7 | 33 |
| billet2022 | 2 | 14 |
| kong2025 | 1 | 15 |
| ni2024 | 3 | 36 |
| xu2025a | 5 | 18 |
| li2024b | 4 | 25 |
| li2021a | 5 | 42 |
| total | 27 | 183 |

## yang2024a (TE1 high-order mode pass filter, inverse-designed unidirectional converter, 220 nm SOI)

- Rows: TE0-TE1 unidirectional converter (measured IL < 0.60 dB, TE0-TE0 crosstalk < -16.9 dB; simulated IL, crosstalk;
  footprint; stack), TE1 HOMPF (bend-structured, fabricated: IL < 0.98 dB, ER > 33.0 / mean 36.8 dB, crosstalk
  < -20.5 dB, means 28.5 / 30.6 dB; simulated mean ER 44 dB; Table 1 footprint), 2-cascaded HOMPF (IL < 1.82 dB,
  crosstalk < -17.7 dB, ER > 34.3 / mean 42.1 dB), straight-link HOMPF (design: 0.18 dB, 22.2 dB, mean ER 21 dB),
  Euler bend (fabricated, simulated 0.002 dB / 90 deg, R about 6 um, 10 um), TE2 HOMPF (design), compact
  inverse-designed bend (design, 0.036 dB / 90 deg, R 1.4 um).
- Not entered: mode (de)MUXes used in the test links (authors' earlier work, ref. 35, no values; D259); cascade mean
  crosstalk -27.0 / -27.8 dB (not tied to TE0-TE1 / TE1-TE0, no "respectively"; D156); simulated backward reflection
  -10.6 / -32.0 dB (p.6, no parameter); TE0-TE2 converter alone (footprint 6 x 1.8 um, 1.4 um multimode port; no
  stand-alone performance -> not a row); initial-structure widths 0.45 / 0.9 um (notes only).
- Fab: "fabricated at Applied Nanotechnology (ANT)" (p.6 Sec. 3.1) -> `org_applied_nanotools`; printed name variant
  "Applied Nanotechnology (ANT)" is not in `org_aliases.csv` (alias request, role fab). No process name printed.
- Judgment calls: HOMPF classed `mode_converter.other` (mode filter, no filter subtype); the fabricated HOMPF taken as
  the bend-structured design (Table 1 footprint 12.5 x 32.6 um2 and the p.10 size remark); simulated 0.18 dB / 22.2 dB
  put on the straight-link design row (the text says the bend version is "nearly unaffected", not shown); converter
  TE0-TE0 residual entered as `crosstalk_db` (the paper uses both words), HOMPF TE0-TE0 values as `extinction_db`;
  measured IL scope `per_component` with method `unspecified` (normalization not described); bend rows carry no
  polarization (not stated).

## billet2022 (GaP-on-insulator by micro-transfer printing)

- Rows: GaP-OI microring (Q best 40 100 at 1534 nm, mean 35 000, std 5000; FSR 922.64 GHz; ER > 8.5 dB; theoretical ng
  3.45 as simulated; widths, thickness, gap), GaP grating coupler (typical 15 dB/coupler; period 900 nm; fill factor
  0.4, definition not stated, D253).
- Not entered: Fig. 4(a) per-resonance Q labels (five values; best / mean / std entered instead); ring radius (not
  stated); propagation loss (no number); Table 1 values of other works; picking yield 90 % and coupon / tether data
  (process, no parameter).
- Fab empty: "we fabricated" with authors at four orgs (Ghent University-imec, ULB, INSA Rennes FOTON, C2N; D80b /
  D154); acknowledgment thanks one person for e-beam processing without naming a place; RENATECH only in funding
  (D80c). No missing org.
- Judgment calls: platform `gap_on_insulator` (GaP on BCB / SiO2 / Si); unqualified Q -> `q_loaded`; band for FSR / mean
  Q inferred from the Fig. 4(a) axis.

## kong2025 (topology-optimized Y-branch, x-cut TFLN)

- Rows: one Y-branch (measured excess loss 0.13 dB per branch at 1498 nm from the cascade slope, mean 0.12 dB and range
  0.11-0.14 dB over 1480-1520 nm, split ratio 53.25 %; simulated 0.123-0.221 / mean 0.141 dB over 1400-1700 nm and 0.12
  / 0.13 / 0.18 dB at 1550 nm for isotropic / anisotropic / anisotropic + 75 deg sidewall; footprint, length 6 um
  (Fig. 2(b) label), film 400 nm, BOX 3.7 um, etch about 400 nm and sidewall 75 deg from SEM).
- Not entered: "+/- 2.10 %" (meaning not defined, kept in notes); bandwidth claims beyond the measured range (300 nm /
  C+L, simulation-based); Fig. 2(a) 100 / 400 nm feature labels (role not tied to a parameter); min feature / curvature
  120 nm (optimization constraint); sidewall roughness < 20 nm (no parameter; RMS-roughness gap already listed, D418);
  grating couplers (no numbers).
- Fab: `org_tsinghua_university` (first-person "we fabricated", own etch recipe; all authors Tsinghua). NanoLN wafer
  in notes. No facility.
- Judgment calls: IL per Y-branch entered as `excess_loss_db` (splitter, D43); cascade-slope fit `measured` (D80a);
  measurement polarization left empty (design TE0, measurement not stated); platform `lnoi_strip` (about 400 nm etch of
  a 400 nm film); Fig. 3 caption letters the IL plot (d) while the text and render say (e).

## ni2024 (three-mode SHMW MMI crossing, 220 nm SOI)

- Rows: TE0/TM0/TM1 crossing (measured 0.72 / 0.27 / 0.90 dB at 1550 nm and < 2 dB over 1505-1580 nm, cross-port
  crosstalk < -38 dB, through-port inter-mode crosstalk < -20 dB; simulated IL / crosstalk at 1550 nm and over
  1500-1600 nm; footprint, MMI width / length, taper length, port strip width, hole period, stack), TE0/TE1/TM0 crossing
  (design, simulated IL and crosstalk at 1550 nm), TM0/TM1 MUX + DEMUX reference pair (`mode_converter.mdm_mux`, mode
  extinction > 24 dB at 1550 nm).
- Not entered: simulated reflections (-13.1 / -35.4 / -31.2 dB at 1550 nm, < -11.9 / -30.2 / -31.2 dB over 1500-1600 nm,
  p.6) - no reflection parameter for crossings; Table 1 bandwidth "about 80 nm (CT < -20 dB)" (no bandwidth parameter
  for crossings); hole width / duty cycle / n1 (no parameter); Fig. 5 tolerance curves; beat lengths.
- Fab empty: passive "are fabricated", authors at NJUST and Hebei University (ni2025a precedent). No facility.
- Judgment calls: `crossing.mmi` (1-D hole array inside an MMI; ni2025a precedent); measured per-crossing values
  `derived` with method `reference_structure` because the text states ten identical crossings were cascaded to obtain
  the average (D80a; ni2025a kept `measured` where the division was not stated); Table 1 "CT < -29 dB" conflicts with
  the text's < -38 dB (noted on the row).

## xu2025a (12-channel LAN-WDM cascaded-MZI multiplexer, 300 nm Si3N4)

- Rows: multiplexer (mean IL 0.87 dB, mean crosstalk 17.03 dB, 1-dB bandwidth 2.3 nm, spacing 4.4 nm measured / 4.5 nm
  design, thermal drift about 11 pm/K estimated, 12 channels, 4 stages, dLbase 95.7 um, 300 nm core), comparison
  multiplexer with only phase shifters optimized (IL up to 5 dB), dual-Bezier multimode bend (simulated < 0.1 dB,
  W 3 um, R 20 um), single-mode and multimode waveguides (2.65 / 0.3 dB/cm, origin not stated -> `author_estimate`).
- Not entered: centre-wavelength shift 22 pm per nm of width bias (p.7, Fig. 7(d); no parameter); Fig. 7(c) Ch. 5 lines
  -16.7 / -26.4 dB (type not named, D156); comparison device "crosstalk lower than -10 dB" (ambiguous for a degraded
  device); Bezier-bend higher-order-mode crosstalk < -20 dB (no crosstalk parameter for waveguide_platform); Table 1
  phase-error values (design analysis); 3-dB BDC and single interleavers (no stand-alone performance).
- Fab: `org_zhejiang_university` (conclusion "We designed and fabricated", all authors ZJU). Raith Voyager EBL is
  equipment. No facility.
- Judgment calls: thermal drift printed as 11 pm/K (abstract, conclusion) and 10 pm/K (p.8): 11 entered with the
  conflict noted; band O inferred from the Fig. 7 axes (the text never names the band); IL scope `de_embedded` with
  method `unspecified` (normalization reference not described); crosstalk type not stated -> `crosstalk_db`.

## li2024b (monolithic 1x9 SOI AWG + Ge PDs for FBG interrogation)

- Rows: AWG (measured centre-channel IL 3.23 dB and crosstalk 20.31 dB on a stand-alone copy; simulated 1.37 / 25.65
  dB; Table 1 counts, order, design spacing; stack, 150 nm etch), Ge PIN PD (dark current 340 nA at -1 V derived from
  0.34 uA, responsivity 0.95 A/W, QE 76 % derived from 0.76, chip-level mean responsivity 0.13 A/W fiber-referred;
  absorber 55 x 8 um, 500 nm Ge), Si taper AWG-to-PD coupler (`waveguide_platform.transition`, 2.4 dB from the Eq. 2
  loss breakdown as `author_estimate`, simulated > 95 %, 50 um), input grating coupler (simulated 2.12 dB).
- Not entered: interrogation-system metrics (accuracy 9.86 / 10.64 / 6.79 pm, resolution, range; system level; p.10
  prints 6.79 "nm" once, typo); Table 1 slab / array effective indices and ng (design inputs); Rowland-circle diameter
  40.38 um (no parameter; FPR length not stated); simulated Ge absorption 86 % / about 90 % (absorption fraction, not a
  QE); taper width 8 um (end not stated).
- Fab empty: the chip "is produced using a 180 nm production line" (p.7, org not named) -> `process_name` "180 nm
  production line", fab empty (D536 / gentry2015). The paper also says "we fabricated" (p.2, p.8), all authors at
  Beijing Information Science & Technology University (`org_beijing_information_science_and_technology_university`
  exists). See question 1.
- Judgment calls: platform generic `soi` (text says "rectangular waveguide" but the process etches 150 of 220 nm);
  AWG measured IL scope `unspecified`; wavelength ranges inferred from Fig. 3 / Fig. 10 axes; Table 2 responsivity
  `ref_plane` unspecified.

## li2021a (ultra-broadband Bragg concave diffraction grating, 220 nm SOI)

- Rows: fabricated AB-CDG (M = m = 2; best IL 0.6 dB de-embedded with a reference straight waveguide, non-uniformity
  about 1.9 dB, adjacent crosstalk < -33.7 dB, spacing 15.4 nm measured / 16 nm design, footprint about 0.8 x 0.7 mm2,
  order 2, 4 um access width, 0.5 um wire, 40 um bends, stack), three simulated designs PB-CDG / AB-CDG 1 / AB-CDG 2
  (Fig. 4 table: peak transmission, non-uniformity, mean / std / worst adjacent crosstalk; Bragg period, order, NB 14,
  10 nm design spacing), grating coupler (3-dB bandwidth about 40 nm around 1.55 um, origin not stated).
- Not entered: Table 1 fill factors 0.34 / 0.76 / 0.76 (`fill_factor` not allowed for wdm); Rowland radii 384 / 344 /
  181 um and blaze / incident angles (no parameters); simulated > 250 nm diffraction bandwidth (no matching parameter);
  number of output channels of the fabricated device (not stated; eight measured); comparison values of earlier CDGs
  (cited, rule 3); Bragg period / fill factor of the fabricated device (not restated; Table 1 values are for the
  Rrc 344 um / 10 nm design).
- Fab empty: "We fabricated" with authors at Xi'an Jiaotong University, XIOPM CAS and Xi'an Sino Huaxin Measurement &
  Control Co. (D80b / D154). No facility.
- Judgment calls: `wdm.eg` (concave grating); Fig. 4 table values entered as `simulated` (printed in the figure table);
  "worst crosstalk" entered with qualifier `ge` (worst channel, suppression at least the value); simulated values
  span the 1.425-1.675 um design band.

## Missing fab / facility orgs

- "Applied Nanotechnology (ANT)" (yang2024a p.6 Sec. 3.1, role fab): mapped to `org_applied_nanotools`; add the
  printed variant as an alias.
- No other missing org; no facility named in any of the seven papers.

## Registry gaps (skipped value + locator + proposed definition)

1. Reflection / return loss for `mode_converter` and `crossing`: yang2024a simulated backward reflection -10.6 dB
   (TE0-TE0) and -32.0 dB (TE0-TE1) (p.6); ni2024 simulated reflection -13.1 / -35.4 / -31.2 dB at 1550 nm (p.6).
   Proposal: widen `back_reflection_db` to mode_converter and crossing ("reflected power into the input port, positive
   dB below the input").
2. `fill_factor` for `wdm` (Bragg-mirror facets): li2021a Table 1 f = 0.34 / 0.76 / 0.76 (p.8), defined as unetched
   strip / period (tooth fraction). Already a D540 candidate.
3. Width sensitivity of a filter: xu2025a centre-wavelength shift 22 pm per nm of waveguide-width bias (p.7,
   Fig. 7(d)). Proposal: `width_sensitivity_pm_per_nm` (wdm, resonator): "centre-wavelength shift per nm of waveguide
   width deviation (sign and how measured in condition)".
4. Mode crosstalk of a multimode bend: xu2025a Bezier bend TE0 -> higher-order crosstalk < -20 dB (simulated, p.6).
   Proposal: widen `crosstalk_db` to waveguide_platform (mode crosstalk, type in condition).
5. Rowland-circle radius for concave gratings / AWGs: li2021a Rrc 384 / 344 / 181 um (p.8 Table 1, p.10); li2024b
   Rowland-circle diameter 40.38 um (p.4 Table 1). Proposal: `rowland_radius_um` (wdm): "radius of the Rowland circle
   on which the access waveguides lie (a printed diameter halved, derived)".

## Coordinator questions

1. li2024b fab: "we fabricated" (p.2, p.8; all authors one university) versus "produced using a 180 nm production line"
   (p.7, unnamed). Recommendation: keep fab empty (the printed line suggests an external fab; D536 / gentry2015);
   alternative: `org_beijing_information_science_and_technology_university` under D72.
2. yang2024a "Applied Nanotechnology (ANT)" -> `org_applied_nanotools` (printed name differs from the registry name):
   confirm and add the alias.
3. li2024b AWG-to-PD Si taper as its own `waveguide_platform.transition` row (Si-to-Ge material transition) rather than
   a value on the PD row: confirm.
4. ni2024 measured per-crossing losses `derived` (explicit ten-crossing averaging) while merged ni2025a rows stay
   `measured`: confirm, or align ni2025a in a sweep.
5. Mode filters (yang2024a HOMPFs) as `mode_converter.other`: a `mode_filter` subtype may be worth adding if more rows
   appear.
