# lit_321 batch report

Distilled 2026-11-28. Papers: lit:guo2016b, lit:keraly2013, lit:ikeda2008, lit:obrzud2018, lit:belt2017. Page-1
titles checked against the source rows: no other paper, no correction or erratum; `garbled_text_layer` false on all
five. Dry run `merge_component_staging.py data/_staging/components/lit_321 --dry-run`: +15 components, +63 metrics,
0 errors (the only warnings belong to merged rows of other sources: guo2024a, ni2025b).

| paper | components | metric rows |
|---|---|---|
| guo2016b | 2 | 3 |
| keraly2013 | 1 | 4 |
| ikeda2008 | 7 | 29 |
| obrzud2018 | 2 | 4 |
| belt2017 | 3 | 23 |
| total | 15 | 63 |

Preprint note: guo2016b and obrzud2018 are arXiv preprints of the listed journal papers (guo2016b = arXiv
1601.05036v1, dated 2016-01-20, titled "Universal dynamics and controlled switching of dissipative Kerr solitons in
optical microresonators"; the Nature Physics title says "deterministic switching"; obrzud2018 = arXiv 1712.09526v1,
dated 2017-12-29, same title as the Nature Photonics paper). Values come from the preprints only; the journal versions
were not read; locators are preprint pages. Every component row of both papers says so in its notes. keraly2013,
ikeda2008 and belt2017 are the publisher copies (Optica open access).

## lit:guo2016b (Kerr soliton switching; Si3N4 microring and MgF2 resonator)

Rows: `sin_ring_100ghz` (resonator.ring: FSR 100 GHz `author_estimate`, nominal; Q ~1e6 `q_loaded` `approx`
`author_estimate`, order of magnitude only, 1553.4 nm inferred) and `lensed_fiber_facet` (fiber_chip_coupler.edge:
2.5-3 dB per facet, lensed fibers, `measured` per D167 / D462).

Not entered:
- MgF2 crystalline resonator (diamond-turned and hand-polished, 5 mm diameter, FSR 14 GHz, linewidth 100 kHz,
  Q ~1e9, D2/2pi 1.9 kHz; p.7, p.10): polished bulk part, out of scope (D411; herr2012 precedent).
- Si3N4 dispersion D2/2pi = 1-2 MHz, D3/2pi = O(1 kHz) (p.9): no dispersion parameter (D81).
- Soliton existence range delta_s ~0.78 GHz, delta_max ~2.0 GHz (p.8-9), tuning speeds, pump powers: operating
  quantities, no registry parameter; pump power and pumped resonance in notes.
- No laser.comb row: the soliton spectra (Fig. 1(h)-(j)) carry no printed line spacing or other comb value besides
  the nominal 100 GHz FSR (a comb row would have no metric of its own, rule 9).
- Ring cross-section, radius, filtering-section geometry: not stated (only a 100 um scale bar in Fig. 1(b)).

Orgs: fab `org_epfl` + facility `org_center_of_micronanotechnology` from "All samples were fabricated and grown in the
Center of MicroNanoTechnology (CMi) at EPFL" (p.11, D448) and the author contributions (A.K. fabricated the Si3N4
samples, p.11). `process_name` "Photonic Damascene process (ref. 38)" (feldmann2021 / trocha2018 form). No missing
orgs.

Judgment calls: the ~1e6 Q is entered as an order-of-magnitude `approx` `author_estimate` (no measurement described);
FSR nominal as in herr2012 / pfeiffer2018a.

## lit:keraly2013 (adjoint shape optimization; simulated Si Y-junction)

Row: `adjoint_y_splitter` (splitter.y_branch, `row_kind` design, platform soi): excess loss 0.07 dB at 1550 nm
(3D FDTD, `simulated`; printed "insertion loss -0.07dB", which is the total transmission to both outputs, so
`excess_loss_db` per D43), 0.07-0.12 dB over 1500-1600 nm read off Fig. 6 (`simulated`, D454, +/- 0.003 dB), Si
thickness 220 nm, design-region side 2 um.

Not entered: ref. [3] particle-swarm design -0.13 dB (cited, rule 3); 200 nm minimum radius of curvature (shape
constraint, not a bend radius); 2D effective index 2.8 and iteration counts (simulation settings, in notes).

Orgs: none (design only, no fabrication). Polarization not stated (left empty).

## lit:ikeda2008 (PECVD SiN/SiO2 waveguides and rings; thermal and Kerr nonlinearity)

Rows (fab `org_university_of_california_san_diego` on all: first-person fabrication, all authors at UCSD; no
facility named):
- `pecvd_sin_wg` (waveguide_platform.straight, test structure): 4 dB/cm TE-like by cutback (`measured`), 500 nm core,
  1 um width (`derived`), 3 um under / 2 um upper cladding.
- `butt_facet` (fiber_chip_coupler.edge): 5 dB per facet, printed with "see Fig. 1(c)"; the fit intercept 10.241 dB is
  the two-facet total, so `derived` (halving, D80a), method cutback.
- `inverse_taper` (fiber_chip_coupler.edge): 2.5 dB "from fiber tip to the SiN waveguide", no measurement described:
  `author_estimate` (D418 / D651).
- `adddrop_r10_g700`, `adddrop_r15_g700`, `adddrop_r20_g700` (resonator.ring): Q 460 / 8500 / 12900 `measured`
  (unqualified Q -> `q_loaded`), radius, gap, core thickness. r20 also: resonance 1548 nm (stated), linewidth 120 pm
  (`derived` from the 0.12 nm label), n_g 1.91 (`measured`, fit), alpha 1.2 dB/mm -> 12 dB/cm `author_estimate`.
- `allpass_r20_g600` (resonator.ring): Q 35,600 `measured` (resonance wavelength about 1567 nm read off Fig. 5(a),
  inferred), linewidth 44 pm `derived`, n_g 1.91 `measured`, alpha 1.6 dB/mm -> 16 dB/cm `author_estimate`, radius,
  gap, core thickness.

Not entered:
- Fitted coupling coefficients kappa = 0.006 (p.5) and 0.009 (p.7): power vs field coupling not defined; Eq. (5)
  (render checked) uses sqrt(kappa) as the bus self-coupling term, which does not reproduce M = 11.4 if kappa = 0.009
  is a power coupling, so the quantity is ambiguous (D156 spirit).
- g = 300 / 500 nm rings: no values ("smaller gaps resulted in smaller Q factors"), geometry only (rule 9).
- Thermal study (p.4-6): resonance shift vs power (Fig. 3(a), no printed slope), bistability at 23 dBm, 5.4 dB probe
  modulation, index change 1.5e-4, 0.9 W intracavity power (model), thermal response > 5 us vs < 1 us calculated:
  no registry parameter fits (an optically induced shift is not `tuning_efficiency_pm_per_mw` per D80j; the > 5 us
  response is a rise of the probe signal, not a stated time constant).
- Kerr study (p.6-7): 1 GHz probe modulation 1.4 %, 0.001 nm shift, index change 1.2e-6, M = 11.4, 2.6 W
  intracavity power: model quantities.
- SiN film n2 = 2.4e-15 cm2/W (p.7, abstract) and film indices 1.99 / 1.46 (p.3): material constants, no parameter
  (registry gaps below).
- Fig. 2(b) FSR (about 9.7-9.8 nm by eye): never printed or cited in the text; not read off.

Judgment calls: ring alpha values `author_estimate` (spectral fits whose loss / coupling regime is not shown to be
determined by the data, D403 / D454; the paper also says they include bending loss); n_g kept `measured` (fit, D80a,
wu2018). The waveguide-loss wavelength is not printed: `c_band` inferred from the 1530-1570 nm spectra and the
1548 / 1558 nm pump / probe (rule 8); same for the coupling losses and the r10 / r15 Q values.

## lit:obrzud2018 (microphotonic astrocomb; Si3N4 microring soliton comb)

Rows: `sin_ring_23p7ghz` (resonator.ring: FSR 23.7 GHz `author_estimate`, method of obtaining it not stated;
resonance width 300 MHz `linewidth_mhz` `measured` as a stated device characteristic, 1560 nm inferred) and
`soliton_comb` (laser.comb: line spacing 23.7 GHz `measured`, lines resolved on the spectrometer in Fig. 2(c);
soliton pulse approx. 50 fs `author_estimate`, no time-domain measurement).

Not entered: 20 dB envelope about 170 nm (comb span not a registry parameter, D81); calibration results (25 cm/s
precision, 3.24 +/- 0.23 MHz drift, < 100 MHz line-fit uncertainty, 10 cm/s level): system-level; driving laser
power (about 1 W on chip) and modulation frequency (11.85 GHz) in conditions / notes.

Orgs: fab empty: the ring is only "fabricated on a silicon-nitride chip" with ref. 37 (a platform review); no
fabrication statement names an org (D80b, D433), although one author is at Ligentec. No facility. No missing orgs.

Judgment calls: 23.7 GHz entered as `channel_spacing_ghz` because it is printed as line / mode spacing and no pulse
is measured (D83b); the text also says the soliton "adopts twice the modulation frequency as its repetition rate",
so a coordinator could move it to `repetition_rate_ghz`.

## lit:belt2017 (Ta2O5-core / SiO2-clad planar waveguides; OFDR loss)

Rows (platform `other`, Ta2O5 core in `core_material`, as merged fan2021 / jung2021; fab
`org_ucsb` on all: "we designed and fabricated" the spirals, etch in "our shared fabrication space", all authors at
UCSB; facility empty because the shared space is not named):
- `ta2o5_spiral_10m` (waveguide_platform.straight, test structure): 3 +/- 1 dB/m across the C band after the
  300 C / 3 h anneal -> 0.03 dB/cm `derived` `mean`, n = 3 dies, TE, OFDR; Fig. 6 readings (`extracted_from_figure`):
  annealed mean 2.75-3.7 dB/m and un-annealed mean 5.45-6.1 dB/m over 1535-1600 nm; min bend radius 2 mm, length
  10 m, core 90 nm, width 2.8 um, lower / upper cladding 15 / 1.1 um, etch depth 150 nm and sidewall angle 80 deg
  (AFM, `measured`).
- `ta2o5_spiral_0p7m` (waveguide_platform.straight, test structure): group index 1.55 `measured` by OFDR, min bend
  760 um, length 0.7 m, design stack.
- `diced_facet` (fiber_chip_coupler.edge): 3 dB per facet with cleaved SMF-28 (`measured`, D167), calculated TE mode
  1/e2 intensity diameters 2.7 um (horizontal) and 1.1 um (vertical) as `mfd_chip_um` `simulated`.

Not entered: refractive indices and n2 of Ta2O5 / Si3N4 / SiO2 (Table 1, cited refs. 15-16), Si3N4 / Ta2O5 film
stress, bandgap, transparency window (cited or material data); ref. [25] 6 dB/m and ref. [27] Si3N4 markers in Fig. 6
(cited, rule 3); Fig. 5 backscatter slope (no printed value); simulated confinement factor 0.15 and effective index
1.474 (no parameter); AFM roughness (registry gap below); the outlook design (1.0 um core, 90 nm shallow etch, p.5:
proposal, not fabricated, no performance value); loop mirror (no reflectivity value, not a row).

Judgment calls: anneal state carried as a metric condition on one 10 m spiral row (the same dies were measured
before and after annealing); the Fig. 1(b) wavelength conflict (text 1590 nm, caption 1.55 um) noted on the MFD rows,
caption kept (D417).

## Missing fab / facility orgs

None. All needed ids exist (`org_epfl`, `org_center_of_micronanotechnology`, `org_university_of_california_san_diego`,
`org_ucsb`). belt2017's "our shared fabrication space" (p.3) is unnamed, so no facility is proposed.

## Registry gaps (skipped value + locator, proposed definition)

- `refractive_index` (waveguide_platform; already a D785 candidate): ikeda2008 PECVD SiN about 1.99 and PECVD SiO2
  about 1.46 (p.3 Sec. 2). Definition: refractive index of a named film at the stated wavelength (film in condition).
- `n2_cm2_per_w` (waveguide_platform): ikeda2008 PECVD SiN film n2 = 2.4e-15 cm2/W (p.7 Sec. 4; rests on the assumed
  2.5 dB coupling loss, so it would be `author_estimate`). Definition: nonlinear (Kerr) refractive index of the core
  film as reported, method in notes.
- `rms_roughness_nm` (waveguide_platform; already a D785 / D418 candidate): belt2017 sidewall Rq 3.0 nm (Ra 2.4 nm)
  and top-surface Rq 0.21 nm (Ra 0.31 nm), AFM (p.3 Sec. 3A). Definition: RMS roughness of the stated surface
  (sidewall / top) and method.
- Soliton existence range (resonator): guo2016b delta_s ~0.78 GHz, delta_max ~2.0 GHz (p.8-9). Not proposed (one
  paper, operating-condition dependent).
