# lit_187 batch report

Papers: lit:piggott2020, lit:li2017, lit:cai2019, lit:tabatabavakili2017. verified_on 2026-11-18. All four cached
texts match their source rows (page-1 titles checked); none is a correction. Cached copies: piggott2020 and cai2019
are arXiv versions, li2017 is the arXiv preprint (title wording differs slightly: "with a Silicon Nanobeam Cavity";
Supplementary Materials not cached), tabatabavakili2017 is the HAL author manuscript (text.md p.1 = HAL cover page,
paper p.1 = text.md p.2). Values are from the cached copies; journal versions unread. Dry-run: +25 components,
+140 metrics, 0 errors (the one warning printed concerns cmp_lit_ni2025b, not this batch).

## lit:piggott2020 (ACS Photonics 2020, inverse-designed devices on an AIM Photonics MPW)

Components 4 / metric rows 32:

| component | metrics | content |
|---|---|---|
| cmp_lit_piggott2020_mode_mux (`mode_converter.mdm_mux`) | 8 | IL < 1.0 dB and crosstalk > 15.6 dB over 1500-1600 nm (single device from the back-to-back structure), footprint, 750 / 400 nm widths, 220 nm core, ports |
| cmp_lit_piggott2020_wdm_3ch (`wdm.other`) | 14 | IL 3.0 / 3.1 / 1.2 dB and crosstalk 8.3 / 12.6 / 12.3 dB at 1500 / 1540 / 1580 nm, design wavelengths (simulated), ports, footprint, core |
| cmp_lit_piggott2020_dc_2x2 (`splitter.directional_coupler`) | 5 | average excess loss 0.5 dB over a 45 nm band, footprint, ports, core |
| cmp_lit_piggott2020_splitter_1x3 (`splitter.other`) | 5 | excess loss 0.4 dB over 1450-1600 nm, footprint, ports, core |

Not entered:
- Power imbalance "< 10%" (directional coupler, p.9) and "4.4%" (1x3 splitter, p.9): percentages with no stated
  definition; no % imbalance parameter (registry gap below). In component notes.
- Directional coupler design center 1545 nm vs measured operation around 1505 nm (p.9): no center-wavelength
  parameter for splitters; in notes. "Reasonably matched output powers over a 100 nm bandwidth": no criterion.
- Design constraints (minimum radius of curvature 40-100 nm, minimum gap 90 nm; p.5, p.7-9): design-rule inputs, no
  parameter (gap_nm is not a feature-size rule); in notes.
- Measurement uncertainty +/-0.6 dB and reference-waveguide variation (p.11, p.13): in notes.
- EBL versions of the demux and splitter are the authors' earlier papers (refs. 18, 19): not used (rule 3).

Judgment calls:
- Fab `org_aim_photonics` on all four rows ("fabricated as part of the AIM Photonics 300 mm wafer MPW", p.3, p.12).
  The Fig. 1 caption (p.4) states the wafers are fabricated "at the Albany NanoTech fabrication facility": a stated
  place (D448), not in the registry (missing org below). process_name "AIM Photonics 300 mm wafer MPW run, 193 nm
  water-immersion DUV lithography" (p.4, p.12-13).
- Platform `soi_strip` (single fully etched 220 nm Si, oxide on all sides, p.3; D434 / D459).
- Mode-mux IL and crosstalk `derived`: the paper extracts single-device values from the back-to-back structure
  (halving, Methods p.13; D80a). Scope `per_component`, method `reference_structure` (spectra normalized to straight
  reference waveguides).
- Splitter "insertion loss" values (0.5 dB DC, 0.4 dB 1x3) stored as `excess_loss_db` (they are below the ideal split
  for 50/50 and 1/3 splitters; rule 6). Demux IL `de_embedded` (wdm precedent, su2017 / lit_179).
- DC wavelength: the 45 nm averaging span is not located; 1505 nm (stated operating point of the measured devices)
  with `wavelength_inferred: true`.
- Footprints are products of the printed dimensions (`derived`); the 1x3 splitter prints "3.8 x 2.5 um".
- Polarization `te` only on the mode mux (TE00 / TE10 stated); not stated for the other three.

## lit:li2017 (Nature Nanotechnology 2017, monolayer MoTe2 on a Si nanobeam cavity, room-temperature CW lasing)

Components 2 / metric rows 23:

| component | metrics | content |
|---|---|---|
| cmp_lit_li2017_nanobeam_cavity (`resonator.photonic_crystal`) | 21 | calculated Q 5.2e6 / 6.5e5 / 1.4e3 and wavelengths 1054 / 1132 / 1167 nm; measured mode wavelengths 1052 / 1132 / 1166 nm (Fig. 2E labels); Q 5605 from the 0.202 nm lasing linewidth (derived); cold-cavity Q 2830 (author_estimate); linewidths 400 / 300 / 202 / 220 / 280 pm vs pump; length 7.2 um, width 365 nm, 220 nm core, mirror period 268 nm, 10 periods |
| cmp_lit_li2017_mote2_nanolaser (`laser.other`) | 2 | lasing wavelength 1132.25 nm, pump threshold 0.097 mW (633 nm CW, max-slope criterion) |

Not entered:
- Threshold power density 6.6 W/cm2 (p.1, p.6; derived in the uncached supplement): no optical-pump density
  parameter (registry gap below).
- Spontaneous emission factor beta = 0.1 (rate-equation fit, p.6), Purcell factor 76 and mode volume 0.48 (lambda/n)^3
  (simulated, p.6-7): no parameters (registry gaps below).
- Calculated re-broadened linewidth 0.251 nm and the ~8 /cm carrier-absorption estimate (p.7): model values.
- Si absorption 1.5 / 16.3 /cm (cited, refs. 28-29), earlier TMD-laser Q values (cited): rule 3.
- Hole diameter 94 nm and the 0.057 taper steps (p.3): no hole-size parameter; in notes.
- Light-out values are arbitrary units (Fig. 3B, 4C).

Judgment calls:
- D396: one row per class for the same device. Cavity-mode linewidths (Lorentzian FWHM vs pump) and the Q values
  computed from them sit on the resonator row with the pump in condition (the paper calls them the cavity-mode FWHM,
  p.6); D250 keeps Q off laser rows. The lasing-linewidth Q 5605 is `derived` (lambda / FWHM, abstract prints 5603).
- Linewidths stored in pm (`derived`, nm printed, D256). Fig. 4B wavelength axis (1127.5-1129.5 nm) disagrees with the
  ~1132.2 nm resonance of Fig. 4D; only its FWHM labels are used, noted.
- Fab `org_tsinghua_university`: author contributions name Y.L., J.Z., D.H. as fabricators, all at Tsinghua (p.8; D439
  / D395). The thanks to a named professor for use of fabrication equipment is not a facility statement.
- Platform `soi` (suspended Si nanobeam from the SOI top layer; air-bridged Si PhC precedent asano2017 / ashida2017).
- Width 365 nm (text) vs 0.36 um (Fig. 1E caption): 365 entered, conflict noted.
- Pump threshold `measured` (maximum slope of the own L-L data); incident vs absorbed pump power not stated.

## lit:cai2019 (Optics Express 2019, Y-cut TFLN waveguide loss vs BOX thickness)

Components 15 / metric rows 72:

| component | metrics | content |
|---|---|---|
| cmp_lit_cai2019_wg_w{1,2}_box{1,1p5,2}_t0, _box2_t45, _box2_t90 (`waveguide_platform.straight`, 10 rows) | 5 each | Table 1 propagation loss (3 / 0.94 / 0.77 / 0.83 / 1.09 dB/cm for W = 1 um; 1.85 / 0.59 / 0.37 / 0.23 / 0.34 dB/cm for W = 2 um), width, BOX, etch ~300 nm, 500 nm film |
| cmp_lit_cai2019_bend_r100_w{2,1}_box2 (`waveguide_platform.bend`) | 4 each | bend loss 1.1 / 1.55 dB/cm (R = 100 um), radius, width, BOX |
| cmp_lit_cai2019_rt_l4000_w{2,1}_box2 (`resonator.ring`) | 6 each | Q_L 843,000 / 549,000 (measured), Q_U 1,061,000 / 628,000 (author_estimate), notch depth ~4.1 / ~2.6 dB (figure read), radius, width, BOX |
| cmp_lit_cai2019_gc (`fiber_chip_coupler.grating`) | 2 | 7 dB per GC at 1550 nm, etch ~300 nm |

Not entered:
- p.2 "low-loss waveguides (0.33 dB/cm)": matches no Table 1 entry (0.37 for W = 2 um at 2 um BOX, theta 0); conflict
  note on that row (D417).
- Simulated leakage losses (Fig. 2(c)-(d) contours) and kt2 of SAW devices (Fig. 1, acoustic, out of scope).
- Q of the L = 300 / 700 / 2000 um racetracks (Fig. 4(c)-(d) plotted only, no labels): not read; no rows for those
  racetracks.
- 200 nm coupling gap (Fig. 3(c) caption): the pictured W = 2 um racetrack's length is not stated (D159); in notes.
- Grating-coupler design (period, fill, angle): not stated.

Judgment calls:
- Ten straight rows: each (width, BOX sample, propagation angle) is a separate physical design (rule 9). Values are
  the fit slopes the paper calls average losses (`statistic: mean`), +/- one standard deviation in notes.
- Propagation and bend losses `author_estimate` with method `ring_extraction`: they rest on per-racetrack intrinsic
  losses from Lorentzian fits whose coupling regime is not stated (D403; kim2025 precedent). The audit may prefer
  `measured` (D80a slope fit) since no group index is needed for alpha in dB; flagged.
- Q_U `author_estimate` (D403); Q_L `measured` (printed fit labels). wavelength_nm 1550 ("around 1550 nm", D393).
- Film thickness 500 nm `design_target`: the text gives it for the simulated stack (p.3) and Fig. 2(a) labels the rib
  waveguide schematic; the purchased film thickness is not printed separately. Noted on every row.
- Etch depth "about 300 nm" `design_target` (no SEM / AFM measurement stated). Widths printed in um stored in nm
  (`derived`, D157).
- Bend rows carry theta = 0 deg from context (p.5-6 discuss the 2 um BOX, theta 0 devices of Fig. 4).
- GC 7 dB `measured`, scope `per_coupler`, method `unspecified`; BOX sample not stated ("each GC").
- Fab empty: first-person fabrication by authors all at Carnegie Mellon University, which is not in the registry
  (missing org below). NGK Insulators (registry `org_ngk_insulators`) supplied the LNOI wafers: supplier note only.
- Theta definition: Fig. 3 caption says angle to the crystal z axis, p.7 text says rotation relative to the X axis;
  noted.

## lit:tabatabavakili2017 (APL 2017, III-nitride-on-Si L3 photonic-crystal cavities in the UV)

Components 4 / metric rows 13:

| component | metrics | content |
|---|---|---|
| cmp_lit_tabatabavakili2017_l3_ra028 | 4 | Q 1085 at 337 nm (Lorentzian fit), FWHM 310 pm (derived from 0.31 nm), 337 nm, period 130 nm |
| cmp_lit_tabatabavakili2017_l3_ra029 / _ra030 / _ra031 | 3 each | Q ~735 / ~515 / ~450 and wavelengths ~335.3 / ~332.3 / ~330.0 nm read off Fig. 2(b) (+/- 15, +/- 0.3 nm), period 130 nm |

Not entered:
- "Resonances down to 315 nm" (abstract): the cavity is not identified.
- Fig. 3 Q values: points for various a, r/a, d/a are unlabelled (D156).
- FDTD Q 1600-5000 for the L3 family and > 10000 for d/a = 0.25, r/a = 0.22 (p.3): family-level / hypothetical design
  (D254).
- Q limit ~2000 at 300 nm and ~1000 at 340 nm (abstract, conclusions): model / summary, no device.
- AlN absorption coefficients (Fig. 4 inset): material property, no component.
- Nominal r/a (hole radius) and hole displacement d/a: no parameters; in labels / notes.

Judgment calls:
- Platform `other` (III-nitride membrane on Si; tabatabavakili2019 precedent). Unqualified Q -> `q_loaded` with a note
  (no bus waveguide).
- Fig. 1 caption (typical L3, displacement 0.10a) vs Fig. 2 caption (d/a = 0.15 for the r/a series): label uses 0.15,
  conflict noted on the r/a 0.28 row.
- Fab empty ("standard cleanroom processing", no org; D80b). RENATECH = program acknowledgement (D80c,
  gonzalezandrade2019 precedent). Sample growth by ammonia MBE is not attributed to an org in the text.

## Missing fab / facility orgs (name as printed + locator)

- "Albany NanoTech fabrication facility" (lit:piggott2020 p.4 Fig. 1 caption: AIM Photonics wafers fabricated there):
  fab place / facility for the four piggott2020 rows (D448). The registry has `org_suny_polytechnic_institute` and
  `org_college_of_nanoscale_science_and_engineering` but no Albany NanoTech entry or alias; owner mapping not inferred.
- "Carnegie Mellon University" (lit:cai2019 p.1 affiliation; p.4 Sec. 3.1 first-person fabrication): fab org for the
  15 cai2019 rows.

## Registry gaps (skipped value + locator + proposed definition)

- `imbalance_pct` (splitter): "output power imbalance as a percentage, as defined by the paper (definition in
  condition)". Skipped: piggott2020 < 10% (DC, p.9) and 4.4% (1x3 splitter, p.9). Definition not printed in this
  paper, so even with the parameter the condition would say "definition not stated".
- `pump_threshold_density_w_per_cm2` (laser): "optical pump power density at threshold". Skipped: li2017 6.6 W/cm2
  (p.1, p.6).
- `spontaneous_emission_factor` (laser, unit 1): "beta factor from a rate-equation fit". Skipped: li2017 0.1 (p.6).
- `purcell_factor` (resonator, unit 1) and `mode_volume_lambda_n3` (resonator, unit (lambda/n)^3): skipped li2017 76
  and 0.48 (simulated, p.6-7). Low priority.
