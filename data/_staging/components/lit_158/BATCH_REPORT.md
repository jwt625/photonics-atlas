# lit_158 batch report

Distilled 2026-11-16 (contract v7, skill `pic-component-distill`). Papers: timurdogan2017, lorenzen2025, yang2010a,
kasture2016, xiong2011. Page-1 titles match the source rows (timurdogan2017 is arXiv 1603.04515 of the Nature
Photonics paper, kasture2016 arXiv 1606.08127v2, xiong2011 the arXiv copy of the APL paper; locators are pages of
the cached texts). No correction / erratum, no garbled text layer.

Totals: 9 components, 58 metric rows. `merge_component_staging.py --dry-run`: 0 errors (one WARN on an unrelated
merged row, cmp_lit_ni2025b_pimmwc).

| paper | components | metrics |
|---|---|---|
| timurdogan2017 | 1 | 9 |
| lorenzen2025 | 0 (stopped, see below) | 0 |
| yang2010a | 5 | 32 |
| kasture2016 | 2 | 8 |
| xiong2011 | 1 | 9 |

## timurdogan2017 (field-induced chi(2) in Si ridge waveguides, MIT)

- Row: `frequency_converter.shg` QPM EFISHG waveguide (800 nm ridge, periodic lateral p-i-n junctions, 1 mm),
  `soi_rib`.
- Measured: P2w/Pw^2 = 12 %/W at lambda_w ~2.29 um, -21 V, on-chip 25 mW pump (coupling calibrated with
  waveguides of varying length). Simulated: 0.9-12 %/W design range (Eq. (2) with the chi(3) spread).
- Geometry: width 800 nm, 220 nm Si, 100 nm slab, 110 nm partial etch (before oxidation), 2 um BOX, L 1 mm
  (`derived`), QPM period 1.44 um in `poling_period_um` with the condition that it is the junction period (no
  ferroelectric poling). Judgment call: the registry has no QPM-period parameter distinct from poling.
- Not entered: DC Kerr MZI phase shifters (3 / 4 mm, VpiL 2.4 V cm at ~1580 nm, p.1 / p.6 / p.10): an EO
  (quadratic electro-optic) modulator, EO-atlas candidate, as D168; the only other performance data are Fig. 1(d)
  traces (cross-port minima near 9.5 V for 3 mm and 7.2 V for 4 mm by eye, which give about 2.9 V cm, not the
  printed 2.4 V cm). Effective chi(2) 41 pm/V (measured overlay) and 26 +/- 15 pm/V (simulated); 6.5 nm simulated
  SHG main-lobe width; SHG observed for pump 2.16-2.42 um in sibling waveguides (no width / period printed); simulated
  loss coefficients 3.6 / 0.2 cm-1 (model inputs); leakage < 0.1 uA at -21 V; inverse tapers, 3 dB couplers and
  heater (no values).
- Fab empty: "fabricated in a 300mm CMOS foundry" (p.13), no foundry or process named (D80b, Contract v7);
  `process_name` empty (no node or flow printed).

## lorenzen2025 (Tm:Al2O3 LMA amplifier, DESY / Twente) - stopped, 0 rows

- The cached arXiv 2505.15361v1 is the preprint of the work already merged as `lit:lorenzen2026` (Nature
  Communications 2026, "Zero-PDG silicon photonic amplifier with high saturation power and low noise figure",
  lit_77, D452): same devices and numbers (10.7 cm serpentine, Tm 4.0e20 cm-3, 29.8 dB at 1.28 W, 815 mW,
  Psat,out > 115 mW, 43 %, coupling losses 2.6 / 3.9-4.2 / 2.0 / 2.2 / 4.7 / 7.1 / 3.9 / 4.9 dB, tunable-PDG
  device, 2.2 cm reference waveguide). Distilling it would duplicate 6 merged components under a second source id;
  skill rule 1 also excludes another version of a paper. Not a wrong-paper case (D397): the file matches its source
  row.
- Differences in the preprint, for the coordinator: NF "as low as 3.7 dB" (p.5, p.9 conclusion) vs "around 3.6 dB at
  30 dB gain" (p.2) in the same text (merged row holds 3.6 dB); PDG gain layer printed "t = 1100 um" (p.10, typo for
  nm); no 6.7 cm stability device.
- Recommendation: `same_as = lit:lorenzen2026` on the `lit:lorenzen2025` source row (or keep it rowless, as the
  D548 rowless sources), and map benchmark citations of the arXiv version to the journal source.

## yang2010a (Al2O3:Nd3+ channel waveguide amplifiers, University of Twente)

- Rows: five `amplifier.rare_earth` designs (one per Nd concentration and length the paper ties a value to):
  1.13e20 / 4.1 cm (14.4 dB at 1064 nm, 5.1 dB at 1330 nm), 1.13e20 / 3.0 cm and 0.65e20 / 4.1 cm (3.0 dB at
  880 nm each), 1.68e20 / 1.4 cm (6.3 dB/cm at 1064 nm, 1.93 dB/cm at 1330 nm), 1.40e20 / 1.0 cm (1.57 dB/cm at
  880 nm). Platform `al2o3`, air top cladding, 8 um thermal oxide.
- Basis `derived` on all gain rows (D166): internal net gain = pumped / unpumped signal ratio minus the background
  propagation and absorption loss (Eq. (1)); pump 45 mW at 802 nm in the condition.
- Geometry on every row: 600 nm layer, 2.0 um width (`derived`), ~70 nm etch, 8 um BOX, length (`derived`).
- Conflicts (D417, in notes): Table 2 swaps thickness / width (2.0 / 0.6 um) against the text; the abstract names
  0.65e20 for the 880 nm 1.57 dB/cm result while Sec. 3.2 names 1.40e20 (body kept); abstract length 1.4 cm vs
  Sec. 3.2 range 1.30-1.65 cm for the 1.68e20 sample (1.4 cm entered); Fig. 4(b) concentration 1.03e20 in text vs
  1.13e20 in the caption.
- Not entered: net-gain bandwidth 865-930 nm (stated across Figs. 4(b) and 4(c), several samples, D159); "additional
  channel propagation losses" 0.6 / 0.3 / 0.15 dB/cm (p.3: unclear whether full channel loss or an excess over the
  slab loss, sample not named; judgment call, values in notes); lifetime 325 us, Judd-Ofelt values, cross sections,
  ETU parameters; Fig. 3(b) pump-power curves.
- Fab empty: passive fabrication sentences, all authors University of Twente (D80b); no facility named.

## kasture2016 (RPE PPLN UV-telecom converter, Griffith / RMIT)

- Rows: `frequency_converter.sfg_dfg` (3 cm, 10 um, z-cut, third-order QPM 7.11 um) and
  `waveguide_platform.straight` for the same waveguide (D396). Platform `other` (proton-exchanged bulk LiNbO3).
- Normalized efficiencies 22.4 %/W/cm2 (SFG) and 1.2 %/W/cm2 (DFG, 135 C) as `author_estimate`: normalized by the
  4.9 mm interaction length inferred from the 0.21 nm SFG FWHM, and internal powers rest on Fresnel reflectances of
  unstated origin; internal vs external and the SFG temperature not stated.
- Propagation losses 0.1 / 0.7 / 1.6 dB/cm measured; wavelengths 1580.3 / 482.3 / 369.525 nm `wavelength_inferred`
  (sentence names telecom / pump / UV).
- Not entered: single-photon conversion efficiencies (Fig. 4, about 0.02 %, photon-number ratio, registry gap);
  projected 4.6-9.2 % for a 3 cm interaction length; Raman noise slopes; ~86 % fiber coupling stated for RPE
  waveguides in general; Fresnel 17 / 15 %; 0.21 nm acceptance width (no frequency_converter bandwidth parameter).
- Fab empty (first-person annealing step, authors at two unrelated orgs, D154 / D433).
- Missing facility org: "Queensland node - Griffith - of the Australian National Fabrication Facility" (p.5,
  "performed in part at"), facility role, would go on both kasture2016 rows.

## xiong2011 (As2S3 waveguide photon-pair source, CUDOS / Bristol)

- Row: `waveguide_platform.straight` As2S3 rib (1 um, 850 nm film, 350 nm rib step from the Fig. 1 inset), 7.1 cm,
  platform `other`, IPG upper cladding.
- Measured fiber-to-fiber IL 14.24 dB (TE) / 18.6 dB (TM) at 1550 nm with 2.5 um MFD lensed fibers;
  propagation loss 0.7 / 1.3 dB/cm `author_estimate` ("estimated", method not stated), 1550 nm inferred.
- No `frequency_converter.other` row: the photon-pair metrics (80 /s net coincidence rate at 57 mW, CAR) have no
  registry parameter (rule 9). Simulated dispersion, gamma 14 /W/m, Aeff 0.86 um2 not entered. AWG / filters /
  SSPDs are setup equipment (rule 13).
- Fab empty: no fabrication statement.

## Registry gaps (skipped value + locator; proposed definition)

- `photon_conversion_efficiency_pct` (frequency_converter): photon-number conversion efficiency
  eta = Pout / Pin x lambda_out / lambda_in (kasture2016 Fig. 4, about 0.02 % SFG / DFG, p.4).
- Frequency-converter bandwidth (`bw_fwhm_nm` / `bw_3db_nm` widened to frequency_converter, as D419):
  kasture2016 SFG acceptance FWHM 0.21 nm (p.4 Fig. 3), timurdogan2017 simulated main lobe 6.5 nm (p.9).
- `chi2_eff_pm_per_v` (frequency_converter): effective (field-induced) second-order susceptibility
  (timurdogan2017 41 pm/V, p.10).
- Photon-pair source metrics (already candidates): `pair_coincidence_rate_hz` (xiong2011 80 /s at 57 mW, p.1-2),
  `car` (xiong2011, not printed as a number).
- `upper_state_lifetime_us` (amplifier; candidate since D429 / D448): yang2010a 325 us (p.3).
- `vpi_l_v_cm` (phase_shifter; candidate since D438 / D455): timurdogan2017 2.4 V cm, if the DC Kerr MZI stays
  out of the EO atlas.
- `nonlinear_coefficient_per_w_per_m` (waveguide_platform): xiong2011 gamma 14 /W/m (estimated, p.1).

## Judgment calls

1. lorenzen2025 stopped as a preprint duplicate of lit:lorenzen2026 (see above).
2. timurdogan2017 DC Kerr phase shifter treated as an EO-atlas candidate, no row (D168 analogue).
3. timurdogan2017 junction period in `poling_period_um` with an explicit condition.
4. yang2010a one row per (concentration, length) the text ties a value to; "additional" channel losses not entered.
5. kasture2016 normalized efficiencies `author_estimate` (inferred interaction length plus Fresnel terms of unstated
   origin) rather than `derived`.
