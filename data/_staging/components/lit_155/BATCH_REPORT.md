# lit_155 batch report

Distilled 2026-11-16 (contract v7, skill `pic-component-distill`). Papers: liu2010a, bao2024, luo2021, bruch2018.
All four cached texts are arXiv versions of the journal papers in the source rows; page-1 titles match (luo2021 arXiv
v1 omits the "[Invited]" tag of the Chinese Optics Letters record; bruch2018 is arXiv v3 of the APL paper; liu2010a is
arXiv 1001.1533 of the Nature Photonics paper; bao2024 arXiv v1 of the LPR paper). Journal versions unread; values are
what the cached copies report. No correction / erratum, no garbled text layer.

Totals: 14 components, 78 metric rows. `merge_component_staging.py --dry-run`: 0 errors (one WARN on an unrelated
merged row, cmp_lit_ni2025b_pimmwc).

| paper | components | metrics |
|---|---|---|
| liu2010a | 4 | 20 |
| bao2024 | 4 | 23 |
| luo2021 | 3 | 21 |
| bruch2018 | 3 | 14 |

## liu2010a (mid-IR Si nanophotonic OPA, Columbia / IBM)

- Rows: `amplifier.parametric` (4 mm OPA), `frequency_converter.other` (idler conversion + cascaded FWM, same guide,
  D396), `waveguide_platform.straight` (cutback set), `fiber_chip_coupler.edge` (lensed fibre to cleaved facet).
  Pattern follows kuyken2011 / foster2006.
- On-chip gains (24 dB best at 2238 nm, 23.4 dB Fig. 2(a) fit, 220 nm / 187 nm gain spans, 7.5 W transparency) are
  `derived` (D166: output over the input inferred from the pump-off output corrected by the measured propagation loss).
  Net off-chip gains 10 dB (signal) / 13 dB (idler, as 1995 %) `derived`, ref_plane fiber.
- Idler conversion 25.4 / 24.7 dB stored as power_conversion_efficiency_pct 34674 / 29512 % (derived). Idler-peak
  wavelength about 2105 nm read off Fig. 1(d) (+/-5 nm).
- Cascaded FWM: peak 5 ~-12 dB (6.3 %) and peaks 6-9 -4 to -9 dB (12.6-39.8 %) `author_estimate` (rest on the authors'
  choice of the dominant mixing term, p.6 / Table 1).
- Coupling 6.5 +/- 1 dB/facet: `derived` (fiber-to-fiber minus cutback loss, halved); 4 / 10 dB/cm at 2030 / 2500 nm
  cutback `measured`. Polarization `unpolarized` (ASE source, p.9).
- Geometry 700 x 425 nm `design_target` (SEM image shown, dimensions stated as the design); BOX 3 um, upper SiO2 3 um.
- Not entered: simulated D = 1000 ps/nm/km and gamma = 110 /W/m (no parameter); > 30 dB linear dynamic range; saturation
  onset Pp ~19 W with gain > 20 dB; fitted TPA / 3PA coefficients (model fit).
- Fab `org_ibm`: "fabricated at the IBM Microelectronics Research Laboratory" (p.8, p.15).
- Missing org / alias (fab role): "IBM Microelectronics Research Laboratory" (p.8 Methods, p.15 Acknowledgements). The
  paper does not place it; barwicz2017 / barwicz2018 / campenhout2009 rows map the same lab to `org_ibm_watson` because
  their papers say Watson. Coordinator: alias to `org_ibm_watson` would move these rows from `org_ibm`.

## bao2024 (Er:TFLN LMA EDWA > 100 mW, East China Normal University)

- Rows: folded 7 cm LMA amplifier chip, 6 cm straight 9 um and 1 um width-series waveguides (only these two widths
  have measured values), lensed-fiber facet coupler.
- All on-chip values (20.5 dB small-signal, 16 dB at max pump, 110 / 113 / 18 mW outputs, PCE 52 %) rest on an
  assumed equal 6.5 dB per facet for signal and pump: `author_estimate` (D462 / D514). Off-chip 7.5 dB gain and the
  14.049 dBm fiber output (Fig. 3(c) label) `measured`. Coupling loss 6.5 dB at 1550 nm `measured` (D167, method not
  stated).
- NF 7.1 dB at 1552 nm `measured`, ref_plane `unspecified` (the paper does not say whether G is on- or off-chip).
- Fig. 4(b) highest on-chip gain about 35.5 dB at 1531.5 nm (input about -46 dBm) entered `author_estimate`, read
  +/-1 dB; it lies in the parasitic-lasing regime (the paper's thresholds 28 dB at 1531.5 nm / 21 dB at 1550 nm in
  notes). Fig. 4(c) 1550 nm points not entered (parasitic-lasing-disturbed, no printed value).
- Abstract pairs 113 mW (straight 9 um guide, p.5) with the folded chip's 16 dB; entered on the rows the body text
  ties them to.
- Platform `lnoi_rib` from the Fig. 1(a) simulated mode insets (ridge on a slab); etch depth, slab and Er
  concentration not printed. `process_name` "PLACE (photolithography assisted chemo-mechanical etching)" as printed.
- Fab `org_east_china_normal_university`: first-person "We fabricate ... using our home-developed PLACE technique"
  (p.3; D84a), all authors list ECNU. Note: merged li2025 (same group, passive "designed and fabricated by PLACE") has
  fab empty; this paper's sentence is first-person.
- Not entered: 1 mm adiabatic taper (simulated field only, geometry-only, no row); ASE band 1510-1590 nm and peak
  1531.5 nm (no amplifier parameter); simulated Fig. 2(c) width series.
- Registry gap: `taper_length_um` (1 mm, p.3) and `center_wavelength_nm` / an ASE-band parameter are not allowed for
  `amplifier`. Proposed: allow `taper_length_um` for amplifier (LMA tapers inside the gain section).

## luo2021 (Er:LNOI waveguide amplifier, Nankai University) - arXiv preprint of the COL paper

- Distilled from the cached arXiv v1 preprint (2103.15786) of the listed Chinese Optics Letters paper; journal
  version not read, values are those of the preprint.
- Rows: ~5 mm amplifier, R = 100 um loss-extraction ring (same chip), lensed-fiber facet.
- Ring: QL 9.78e4 (1531.5 nm) / 2.42e5 (974.5 nm) `measured` (Lorentz fit); Qi 5.0e5 / 2.6e5 and losses 0.83 / 2.5 dB/cm
  `author_estimate` (coupling regime "inferred by gap", D403). Facet 6.76 / 6.35 dB `author_estimate` (identical facets
  assumed, loss input author_estimate).
- Amplifier internal net gains subtract alpha L = 0.42 dB from the author_estimate loss: all gain rows
  `author_estimate` (strict D403 chain; zhou2021a precedent kept `derived` for a ring-derived loss, flagged here).
- Inconsistency kept as printed: ~15 dB (~30 dB/cm) at ~-65 dBm signal and ~23 mW pump (Fig. 4(c)) vs ~5.5 dB
  (11 dB/cm) at ~5 nW and ~64 mW (Fig. 4(a)); the text prints "~65 dBm" / "~34 dBm" without the minus sign (Fig. 4(c)
  axis negative). Transparency at ~1 mW pump entered as pump_threshold_mw.
- Geometry: top width 1.4 um, etch 280 nm, 60 deg wedge, film 600 nm, BOX 2 um (design_target / derived), slab 320 nm
  derived (600 - 280).
- Not entered: ~0.13 dB gain at about -34 dBm (saturation tail); ASE spectrum; Er 0.1 mol% (no parameter, in
  core_material).
- Fab `org_nankai_university`: "we present the fabrication ..." (p.2), "we fabricated" (p.6), all authors Nankai.
  No facility.

## bruch2018 (17,000 %/W SHG in single-crystalline AlN rings, Yale / ISCAS)

- Rows: `frequency_converter.shg` for the Fig. 2(c) ring (1.24 um width, 0.65 um visible gap, 1556 nm mode),
  `frequency_converter.shg` for the 1590 nm mode (geometry not printed), `resonator.ring` for the representative
  Fig. 1(c) resonances. Platform `other` (AlN on sapphire, D515).
- Judgment call: the 1590 nm (17,000 %/W) device is taken as a separate ring from the 1556 nm one (a ring cannot
  phase-match both over the +/-10 C tuning of Fig. 3(b)); the paper does not say. The Fig. 1(c) ring is not tied to
  either (its 1555.52 nm resonance suggests the 1556 nm ring; not stated), so its Q values sit on their own row with
  statistic `typical`.
- 14,500 +/- 200 %/W `measured` (linear fit, D80a); 15,000 and 17,000 %/W `derived` (fiber powers corrected by the
  measured 22 % / 10 % transmissions, +/-3000 %/W); absolute efficiency 11 % `measured`. Q0 8.0e5 / 4.0e5
  `author_estimate` (coupling regime asserted, D403); kappa0/2pi 240 / 970 MHz equal these Q0 and are not entered twice.
- Fab empty: first-person fabrication by authors at two orgs (Yale University, Institute of Semiconductors CAS), no
  sentence naming the processing org (D154 / D80b). Merged guo2016 (same group, all authors Yale) has fab
  org_yale_university. No facility acknowledged.
- Not entered: chi(2) 6.2 +/- 0.4 pm/V and g/2pi 0.12 MHz (model extraction, no parameter); pump-depletion onset
  3.5 mW; 20 nW SHG from 190 uW (Fig. 2(b) heat map); simulated 20,000 %/W optimum (Fig. 3(a)); 1.2 dB/cm simulated
  radiation loss of a partially etched example; phase-matching tuning 1480-1640 nm over widths 1.2-1.3 um.
- Registry gap: `gap_nm` (visible gap 0.65 um, p.3; critically coupled 0.60-0.65 um vs overcoupled 0.50-0.55 um) and
  `radius_um` are not allowed for `frequency_converter` (same gap as guo2016). Proposed: allow `gap_nm`, `radius_um`
  and `bus_width_nm` for frequency_converter (ring-based converters).

## Missing fab / facility orgs

- "IBM Microelectronics Research Laboratory" (liu2010a p.8 Methods, p.15 Acknowledgements; fab role): entered as
  `org_ibm`; alias decision for the coordinator (see liu2010a).
- None else: Yale University, Institute of Semiconductors CAS, East China Normal University and Nankai University are
  in the registry. Wafer / film suppliers: SOITEC (liu2010a, note only).
