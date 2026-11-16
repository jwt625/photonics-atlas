# lit_137 batch report (distiller, 2026-11-15)

Five papers selected because benchmark tables of other papers cite them (amplifier / resonator family). Only what each
paper reports itself was entered (rules 1, 3). Page-1 titles checked against the source rows: all five cached texts
are the paper of their row; none is a correction / erratum. rudenkov2025 and jung2021 are arXiv texts of the journal
works (same titles; journal versions unread). subramanian2012 and bakonyi2003 are not flagged `garbled_text_layer`,
but their text layers drop numbers set in math font (e.g. "0.65 [+/- 0.05] dB/cm", "~9 dBm"): every such value was
read from the page renders (subramanian2012 p.2-p.5, bakonyi2003 p.2-p.4; no render exists for subramanian2012 p.1 /
p.6, whose abstract / conclusion values were matched to the p.5 render). Validator: `merge_component_staging.py
data/_staging/components/lit_137 --dry-run` -> +34 components, +153 metrics, 0 errors (only warning: the
pre-existing one on merged cmp_lit_ni2025b_pimmwc-m18).

| paper | components | metric rows |
|---|---|---|
| rudenkov2025 | 8 | 38 |
| cheung2015 | 7 | 47 |
| jung2021 | 12 | 44 |
| subramanian2012 | 5 | 18 |
| bakonyi2003 | 2 | 6 |
| total | 34 | 153 |

## rudenkov2025 (Cr:ZnS laser-written depressed-cladding waveguide amplifier, 2.35 um CPA, Opt. Express 2025)

- Rows: 8 `amplifier.other` rows, one per design (diameter 50 / 40 / 30 / 20 um x defect step 3 / 4 um; rule 9),
  platform `other` (polycrystalline Cr2+:ZnS bulk sample, 34 mm). Text values: WG#1 (50 um, 3 um step) gain factor
  75 -> 18.75 dB, 5.5 dB/cm (printed, derived by the authors), 2.35 W -> 33.71 dBm, power-added efficiency 16.2 % at
  14.3 W incident pump; WG#28 (50 um, 4 um step) factor 57, 2.11 W, 16.1 % at 12.9 W; WG#11 (40 um, 4 um step)
  factor 68, 2.04 W, 14.0 % at 14.3 W. Figure labels (gain factor k, Opt.eff.): WG#24 59 / 15.5 %, WG#8 56 / 13.6 %,
  WG#12 6.5 / 1.8 %, WG#26 4.9 / 1.4 %, WG#31 5.01 / 1.26 %, WG#27 4.13 / 1.20 %. Geometry: diameter (`width_nm`,
  derived) and 34 mm length on every row.
- Gain rows: the paper's gain factor is pump-on / pump-off seed output at the same plane (facets and coupling
  cancel): `ref_plane on_chip`, dB conversion `derived`. Output powers are measured after a collimating lens and
  dichroic separators: `ref_plane unspecified`. Efficiencies `derived` (ratios computed by the authors).
- Not entered: text statement for the 30 and 20 um groups together (0.23-0.3 W, factors 5-6.5, 1.2-1.8 %; D254,
  in notes); M2 = 1.13 x 1.25 of WG#28 (no parameter); sub-ps (WG#24_fs / WG#28_fs) curves, burst-mode trace and
  harmonic generation (no values); all modelling results (Figs. 10-12, gain curves for assumed index profiles).
- Fab empty: "We fabricated 31 circular waveguides" (p.3) is first person, but the authors are at three orgs
  (D154). Orgs as printed: Department of Physics, Norwegian University of Science and Technology (p.1); Photonics
  Institute, Vienna University of Technology (p.1); ATLA Lasers AS (p.1; also maker of the writing laser, p.3). None
  of the three is in the registry (only relevant if the coordinator assigns fab).
- Judgment calls: (1) Scope: a waveguide laser-written inside a bulk crystal, free-space coupled. Kept as in scope
  (fs-written waveguide precedent amorim2017; not a discrete bulk resonator, D411); coordinator question below.
  (2) Label efficiencies of WG#24, WG#26, WG#31 and WG#27 reproduce only with 14.3 W incident pump, although their
  plotted curves end near 12.9 W (batch check, in notes); pump level left open on those rows. (3) Signal wavelength
  entered as 2350 nm (stretched seed spectrum ~100 nm wide centred at 2.35 um, p.2; seed laser centre 2336 nm).
- Registry gaps: beam quality M2 (p.3, Fig. 4(a): 1.13 x 1.25) - proposed `m2_beam_quality` (amplifier, laser).

## cheung2015 (hybrid III-V/Si SOAs, high WPE, Opt. Express 2015)

- Rows: straight SOA (400 um, Si width 500 nm) and flared SOA (400 um, Si width 4 -> 8 um), `amplifier.soa`, platform
  `other` (davenport2016 / keyvaninia2012 precedent); four passive Si rib waveguides (`soi_rib`, 500 nm SOI, 250 nm
  etch; widths 500 / 600 / 700 / 3000 nm) with FP losses 1.128 / 0.977 / 0.898 / 0.401 dB/cm (`measured`, D394,
  simulated 42.2 % facet reflectivity in notes); one `fiber_chip_coupler.edge` row (3 um polished facet, 7 deg angled
  output, AR-coated PM lensed fibers): 13.74 dB per facet (derived: (27.65 - 0.158) / 2), 27.65 dB fiber-to-fiber
  passive insertion loss (measured), 13.73 dB per facet from the photodetector method (author_estimate, assumed QE
  0.95), FDTD back reflection < 0.3 % -> > 25.23 dB (simulated).
- SOA rows: on-chip output powers as printed (10.1 dBm at 95 mA and 7.0 dBm at 35 mA, Pin 2 mW; -2.43 dBm at Pin
  0.1 mW; flared 11.24 dBm at Pin 2 mW and -2.5 dBm at Pin 0.1 mW), `derived` (output coupling loss removed, D394).
  Gain is not printed by the paper; on-chip gain rows = Pout - Pin computed by the batch (7.09 / 3.99 / 7.57 dB
  straight, 8.23 / 7.5 dB flared; D166, formula in notes): drop them if batch-computed gain is unwanted. Series
  resistance 3.46 ohm (I-V) and 6.876 ohm (4-point probe); stack geometry (Si 500 nm, BOX 3 um, etch 250 nm, mesa
  75 um, 1 um SiO2).
- Not entered: WPE (headline 12.1 % flared, 9.2 % / 7.2 % / ~0.38 % straight, ~0.4 % flared at 0.1 mW; abstract
  7.3 % conflicts with the body's 9.2 %) - `wpe_pct` is laser-only (registry gap, already raised at D535; values in
  component notes); sibling designs with curves only (Si width 600 / 700 nm, lengths 500-700 um, flared 6-10 /
  8-12 / 10-14 um); gain ripple < 1 dB; leakage current 0.9 uA; n-contact resistance; III-V taper FDTD reflection
  1.7e-5 % (geometry-only otherwise, not a row); design / thermal simulations (Fig. 3, Fig. 12); Table 1 (other
  works and product sheets).
- Conflicts noted (D417): flared output 11.24 dBm (text) vs 11.42 dBm (Fig. 9 caption); series resistance 3.46 ohm
  (text) vs 3.679 ohm (Fig. 6 caption); Fig. 6 caption "width = 4um" for the straight 500 nm SOA.
- Fab empty, coordinator question below. Orgs as printed: Department of Electrical and Computer Engineering,
  University of California, Davis (p.1; `org_university_of_california_davis` exists); Furukawa Electric, R&D
  Laboratory Photonic Research Center (p.1, "Currently with"; `org_furukawa_electric` exists). No acknowledgment, no
  facility.
- Registry gaps: `wpe_pct` on amplifier (values above, p.1 / p.10-12); `back_reflection_db` on
  waveguide_platform.transition (III-V/Si taper 1.7e-5 % simulated, p.5-6).

## jung2021 (tantala Kerr-nonlinear integrated photonics, Optica 2021)

- Rows (fab `org_national_institute_of_standards_and_technology` on all fabricated rows: "we fabricate" / "our
  fabrication process", all six authors at NIST; facility empty, see missing org):
  - High-Q test ring, RW 5 um (Fig. 1(e)): Q_L 1.9e6, FWHM 100 MHz (measured), Q_int ~3.8e6 `derived` (2 Q_L, regime
    from the transmitted power, D403 / D463 / D514), 8 dB/m -> 0.08 dB/cm `author_estimate` (group index not
    printed, D76). Film thickness and diameter not stated for this ring (in notes).
  - RW 3 um ring, 46 um diameter, 570 nm, air-clad (Fig. 2(e)-(g)): seven Fig. 2(f) Q_L labels (TE00 2.4 / 2.5 / 2.3 /
    2.2 M, TE01 1.3 / 1.4 / 1.0 M; resonance wavelengths read +/- 0.1 nm), TE00 FSR ~3.56 nm (figure read), FWHM 190 MHz
    at 1065.48 nm and 220 MHz at 2034.35 nm (labels), Q_int 1.6e6 / 1e6 (captions, `author_estimate`, regime not
    stated), Fig. 2(b) Q_int ~2.3e6 (figure read), radius 23 um (from the 46 um diameter), gap 600 nm.
  - Fig. 2(b) ring-width series RW 1 / 1.5 / 2 / 4 / 5 um: one row each with the figure-read Q_int (0.17 / 1.02 / 1.45
    / 1.90 / 1.77 M, +/- 0.1 M; D400 test-series rings).
  - Edge couplers to a 2.5 um MFD lensed fiber: ~500 nm inverse taper ~3 dB per facet (20 um long) and > 2 um wide
    edges ~4 dB per facet (one group row, D165); band C inferred.
  - Kerr-soliton combs (`laser.comb`), RW 1.6 / 1.65 um: pulse durations 32 / 25 fs `derived` from the sech2 spectral
    FWHM 9.8 / 12.6 THz (D84c).
  - Unpatterned 820 nm film (`waveguide_platform.other`, slab): loss < 0.3 dB/cm at 633 nm (prism coupler,
    measurement-limited), thickness 817(1) nm mean of 9 points; fab empty (IBS film from FiveNine Optics, supplier note).
- Not entered: n2 = 6.2(23)e-19 m2/W and dn/dT 8.8e-6 /K (material properties); Fig. 1(f) threshold series (15 rings,
  no device identity) and Fig. 1(g) thermo-optic shift (~-0.9 GHz/K read; ring not identified, D159); Turing onset 20
  mW (Fig. 3(f), device not identified); Fig. 2(a) anneal series and Fig. 2(c) Q_L vs gap (figure curves only);
  supercontinuum results (500-2500 nm span, 60 pJ dispersive-wave threshold: no registry class / parameter); the
  "~50 % at each facet" coupling stated once for two edge designs (D254); stress 38(7) MPa.
- Conflicts noted: "46-um radius" (p.6) vs 46 um diameter (p.3, p.5, Fig. 1(c)): radius not entered on the comb rows;
  Fig. 2(d) minimum reads ~3.5 dB near 0.4 um against the printed ~3 dB per facet (printed value entered); Fig. 2(g)
  220 MHz label implies Q_L ~0.67e6, so 2 Q_L ~1.3e6 vs the caption's Q_int 1e6.
- Missing org: Boulder Microfabrication Facility (facility, p.8 Acknowledgements "Jeff Chiles and the Boulder
  Microfabrication Facility"; thanked without a stated role, borderline D80c) for the 11 fabricated rows; already
  reported missing by an earlier batch (merged NIST rows carry the same note).
- Registry gaps: thermo-optic resonance shift in GHz/K (`thermal_drift_ghz_per_k`, candidate already in D443);
  supercontinuum span / pulse-energy threshold (no class).

## subramanian2012 (Er:Ta2O5 rib waveguide amplifiers, JLT 2012)

- Rows: amplifier `amplifier.rare_earth` (2.3 cm, nominal 2.6 um wide, 2 um film, 400 nm etch, Er 2.7e20 cm-3):
  net gain 4.83 +/- 0.11 dB at 1531.5 nm, 20 mW launched 977 nm pump (measured), 2.1 dB/cm (derived), net-gain
  threshold ~4.5 mW (measured); theory without upconversion 3.1 dB/cm net and 0.5 mW threshold (simulated). Passive
  silica-clad rib waveguide row: 0.65 +/- 0.05 dB/cm at 1600 nm (FP, best, measured, D394) and 1.0 +/- 0.1 dB/cm at
  977 nm (cutback). Initial unclad, unannealed waveguides: 2.5-4.0 dB/cm (range). Two `row_kind: design` model optima
  (Fig. 8, 200 mW pump): 21.9 dB at 5.8 cm / 5.4e20 cm-3 (Cup 5e-18 cm3/s) and 12.2 dB at 5.1 cm / 4.0e20 cm-3 (Cup
  1e-17 cm3/s), band C inferred from the 1527 nm cross sections.
- Not entered: slab loss 0.4 dB/cm at 633 nm (sentence cites the authors' ref. [10], rule 3); cross sections,
  absorption spectra and lifetimes (material); Table I model inputs; effective index 2.04 (no parameter); modal spot
  size 3.5 x 2 um (for a W = 1 um guide, no amplifier row; origin of the profile not stated); 23 dB / 10 cm model point
  and Figs. 6-7 curves; fitted Cup 1e-17 cm3/s; ideal gross gain 3.75 dB/cm.
- Fab empty (passive sentences; all authors ORC Southampton; staff thanked by name only).
- Judgment call / coordinator question: Sec. V says the 2.3 cm waveguides "were used for gain measurements as
  discussed in [11]" (the same authors' Opt. Commun. 285, 124 (2011), a gain paper). The value sentence ("The
  experimentally measured maximum gain was 4.83 +/- 0.11 dB"), Fig. 9 and its caption cite nothing, and the abstract /
  conclusion present the gain as this paper's result, so the gain rows are kept under the D408 test (attribution in
  the value sentence or figure). If the coordinator reads "as discussed in [11]" as attributing the measurement to
  [11] (D259a), delete m1-m3 of the amplifier row (the theory rows m4-m5 and the passive rows stay).

## bakonyi2003 (1300 nm InAs-InGaAs DWELL QD-SOA, JQE 2003)

- Rows: `amplifier.soa`, platform `gaas`: 18 dB small-signal chip gain at 1300 nm and 100 mA (heat sink 24 C;
  fiber coupling de-embedded; gain referenced to the transparency current), output saturation power ~9 dBm (3-dB, chip
  output), NF ~8 dB (from ASE density, derived), length 2.4 mm, ridge 4 um. Facet coupling row
  (`fiber_chip_coupler.edge`): ~12 dB per facet with unoptimized spherical lensed fibers (ASE-based estimate, band O
  inferred).
- Not entered: optical bandwidth 50 nm = ASE FWHM (registry: `bw_fwhm_nm` not allowed on amplifier and the paper does
  not call it 3 dB); polarization dependence of gain > 20 dB; linewidth enhancement factor ~0.1; gain recovery time
  constants ~10 ps / ~140 ps; transparency current ~30 mA; lasing onset 135 mA at 1304.5 nm; ripple < 2 dB; waveguide
  loss < 2 cm-1 (origin not stated); ~18 dB (17 cm-1) near 135 mA (same headline); EL peak 1305 nm / FWHM 65 nm and
  dot density (material); MQW-SOA comparison device (setup / commercial reference).
- Fab empty (passive "was fabricated"; authors at Friedrich-Schiller University Jena, UNM Center for High Technology
  Materials, Zia Laser, Inc.).
- Registry gaps: `bw_fwhm_nm` (or an ASE-bandwidth parameter) on amplifier (50 nm, p.1 / p.2); polarization-dependent
  gain (`pdg_db`, amplifier; > 20 dB, p.3 / p.4); linewidth enhancement factor (`alpha_h`, amplifier / laser; ~0.1,
  p.3, Fig. 6); gain recovery time (`gain_recovery_ps`, amplifier; ~10 / ~140 ps, p.4).

## Coordinator questions

1. rudenkov2025 scope: keep the laser-written Cr:ZnS waveguide amplifier rows (waveguide in a 34 mm bulk crystal,
   free-space coupled, amorim2017 precedent) or delete them under D411? Recommendation: keep.
2. cheung2015 fab: first-person fabrication ("we employ photoresist reflow", p.7; "We fabricated several flared SOA
   devices", p.11) with three authors at UC Davis and one printed only as "Currently with Furukawa Electric". Left
   empty (D154 / D433); recommendation: `org_university_of_california_davis` as borderline (the "currently with" note
   implies the author was at UC Davis during the work), on all 7 rows.
3. cheung2015 batch-computed on-chip gain rows (Pout - Pin, 5 rows): keep (D166 arithmetic on the paper's own on-chip
   powers) or drop? Recommendation: keep.
4. subramanian2012 gain values vs "as discussed in [11]" (see the paper section). Recommendation: keep (D408 test).
