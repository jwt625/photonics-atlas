# lit_147 batch report

Distilled 2026-11-15 under the pic-component-distill skill (Contracts v4-v7, DevLog-002 D30-D84, DevLog-007
D150-D581). Totals: 20 components, 165 metric rows. `merge_component_staging.py data/_staging/components/lit_147
--dry-run`: +20 components, +165 metrics, 0 errors (the one warning printed concerns a merged ni2025b row, not this
batch). Figures read on the page renders (and the embedded Fig. 9 image of liu2023a).

Page-1 check: every cached text is its source row's work. liu2020b is the arXiv v3 preprint titled "Nanophotonic
soliton-based microwave synthesizers"; the source row carries the Nature Photonics title. Same arXiv id (1901.10372),
same authors and experiments, so it is the same work (D430 / D433); the journal version was not read.
krasnokutska2019 and li2022a are arXiv texts whose titles match their source rows. liu2023a is the Optica OA version.

## Per paper

| paper | components | metrics | classes |
|---|---|---|---|
| liu2020b | 5 | 34 | resonator.ring x2, laser.comb x2, fiber_chip_coupler.edge |
| liu2023a | 3 | 42 | splitter.adiabatic x3 |
| li2022a | 2 | 18 | resonator.ring, waveguide_platform.straight |
| krasnokutska2019 | 10 | 71 | resonator.ring x7, waveguide_platform.straight, fiber_chip_coupler.edge x2 |

### liu2020b (Si3N4 soliton microcombs at X- and K-band repetition rates, Nat. Photon. 2020; arXiv text)
- Rows: 20 GHz ring design (2.30 mm diameter, 1700 x 950 nm; samples A / B), 10 GHz ring design (4.60 mm,
  2100 x 950 nm; samples C / D), the two soliton combs on those rings (D396 class split), double-inverse nanotaper
  edge coupler.
- 20 GHz ring: kappa_0/2pi 8.5 MHz histogram mode over 7079 resonances from nine samples (`typical`, n 7079) and
  Q0 > 22e6, both `author_estimate` (D403: the population fit does not show how the regime was fixed; D465
  population precedent); FSR (D1/2pi) ~19.6 GHz; loaded linewidths ~18 MHz (A, eta ~1/3) and ~27 MHz (B, eta ~2/3);
  alpha ~1 dB/m entered as 0.01 dB/cm `author_estimate` (sentence cites the process papers 46-47, no measurement
  shown; D80i borderline, D578 precedent); radius derived from the diameter, cross-section `design_target`.
- 10 GHz ring: loaded linewidths ~17 MHz (C, critical) and ~22 MHz (D, eta ~2/3), geometry.
- Combs: repetition rates 19.6 / 9.78 GHz; 3-dB bandwidths 11.0 / 26.9 / 17.4 / 25.8 nm (sech2 fit = `measured`);
  comb lines within 3 dB 69 / 170 / 139 / 327; pulse durations 232 / 94.6 / 146 / 98.6 fs `derived` (computed from
  the fitted bandwidth, D84c); sample A soliton threshold 38 mW and parametric oscillation 7 mW in the bus waveguide,
  `derived` on-chip (fiber power minus ~3 dB per facet, D394).
- Edge coupler: ~3 dB per facet (`measured`, D167) and ~25 % fiber-to-fiber (`derived`, the paper's conversion).
- Not entered (no parameter): SSB phase noise of the 19.6 GHz carrier (~-80 / -110 / -130 dBc/Hz at 1 / 10 /
  100 kHz, p.5 Fig. 3(d); abstract < -105 dBc/Hz at 10 kHz, -140 dBc/Hz at 1 MHz), injection-locking range 40 kHz
  (p.5), PM-to-PM transduction -55 dB and AM-to-PM 79 Hz/mW (p.10 Supp.), Raman self-frequency shift ~4.9 / ~4.4 nm
  (p.6), D2/2pi 63.3 kHz and D3/2pi -15 Hz (dispersion rejected, D81), quiet-point detuning ~439 MHz.
- Fab `org_epfl` (author contribution: J.L. designed and fabricated the samples) + facility
  `org_center_of_micronanotechnology` (acknowledgment, fabricated in the EPFL CMi); `process_name` "photonic
  Damascene reflow" (lihachev2022 precedent wording).

### liu2023a (rib-waveguide adiabatic arbitrary-ratio splitters on SOI, OE 2024)
- Rows: 50:50 (L 78 um), 70:30 (L 70 um), 90:10 (L 79 um) adiabatic directional couplers, each with measured mean
  split ratio (51.2 / 28.1 / 10.9 %, `derived` fraction -> %, D256), printed +/- deviation as `coupling_variation`
  (0.051 / 0.032 / 0.040, measured, 1450-1600 nm), IL < 0.22 dB as `excess_loss_db` per_component, cutback (cascade
  regression, GC response removed), Fig. 9 regression-curve ranges (0.03-0.15 / 0.015-0.155 / 0.08-0.225 dB,
  `extracted_from_figure` +/-0.01 dB), simulated split ratio and deviation (49.9 / 29.6 / 9.8 %, 0.026 / 0.033 /
  0.018), and geometry (L, G2 100 nm, W 350 nm, 220 nm Si, 160 nm rib etch, 60 nm slab derived, 2 um BOX / cladding).
- Judgment calls: the < 0.22 dB bound is printed once but names all three ratios, so it is entered on each row (not
  a family average, D254 does not apply); the 90:10 regression peak (~0.225 dB) sits at the bound (note). The 50:50
  average 0.512 is not tied to a port (Fig. 7(c) bar and cross both near 0.5); 70:30 / 90:10 averages are the cross
  (lower-ratio) port by Fig. 8(b) / 8(e). Table 1 widths W1-W4 and G1 kept in notes (no role-specific parameter, the
  layout rule forbids guessing which width is which); only W (350 nm port width) entered as `width_nm`.
- Not entered: "over 150 nm" measured and 200 nm simulated bandwidths (criterion not defined; 1450-1600 nm is the
  laser range); Fig. 5 tolerance curves (no printed values); Fig. 10 dB ratios; TE grating couplers (no values).
- Fab `org_shanghai_institute_of_microsystem_and_information_technology`: first-person EBL / ICP fabrication and
  "we fabricated and tested", all authors at SIMIT (first author also UCAS; D72 / D80b). No process name (in-house EBL).

### li2022a (transfer-printed LN microrings on SiN, OME 2022; arXiv text)
- Rows: transfer-printed x-cut LN membrane ring on a SiN bus chip (R 40 um, 2.5 um ridge, 350 nm etch; platform
  `other`), monolithic LNOI rib loss structure (~3 dB/cm, Fabry-Perot, `measured` per D394).
- Ring: q_loaded 32k / 26k / 3.4k at 1577.15 / 1578.48 / 1576.4 nm (TE00 / TE01 / lossy TE02 by the p.6 text),
  q_intrinsic 39k / 27k / 3.6k `author_estimate` (D403: single all-pass fit, regime not stated); FSR ~4 nm; geometry.
  The 3.4k / 3.6k values come only from the Fig. 5(b) label.
- Judgment calls: platform `other` (LN rib ring resting on an SiN film chip; no LN-on-SiN membrane value). Fab
  empty on both rows: no sentence names who made the LN devices ("we developed a fabrication process" only, D80b;
  authors at Fraunhofer CAP and Strathclyde). The SiN receiver chip came from a CORNERSTONE MPW run
  (`org_cornerstone` exists), but it is the host bus waveguide, not the measured LN component, so it is kept in
  notes, not on the ring row (fab per component, D515 / D463). Coordinator may prefer org_cornerstone on the ring row.
- Not entered: fitted coupling coefficients kappa 0.008 / 0.003 / 0.04 (Fig. 5 labels; field vs power not defined);
  simulated bend loss curves and LN field fractions (78 % Fig. 1, 86 / 89 / 83 % Fig. 6); the SiN waveguide
  (geometry only, no performance; 300 x 1200 nm on 3 um SiO2).

### krasnokutska2019 (tunable large-FSR Z-cut LNOI microrings, Sci. Rep. 2019; arXiv text)
- Rows: rib waveguide loss structure (< 0.5 dB/cm TE and TM, Fabry-Perot, `measured`; simulated group indices 2.38
  TE / 2.33 TM; geometry incl. FIB-SEM etch depth 350 nm and 75 deg sidewall `measured`), inverse taper edge coupler
  (8 dB fiber-to-fiber for the 6 mm chip incl. propagation; 200 um / 200 nm design), untapered facet reference
  (15 dB fiber-to-fiber), seven rings R = 30-90 um (300 nm gap, heavily overcoupled).
- Rings: Fig. 2(b) Q points (TE and TM, `extracted_from_figure` +/-200) and Fig. 3(a) / 3(d) FSR points (+/-0.05 nm)
  per radius; R30 keeps the printed TM Q ~9000, TE Q ~1200 and TM FSR 5.7 nm (figure reads ~8600 / ~1550 / ~5.55 nm
  noted, D417), model bend losses 1.5 (TM) / 12 (TE) dB/cm `author_estimate`, simulated Q ~10000 and FWHM ~155 pm;
  R70 adds Table I (Q 7500, FSR 2.5 nm, polarization unstated) and the 3 pm/V EO resonance tuning (0 to -55 V).
- Q values are the paper's unqualified Q of overcoupled rings -> `q_loaded`. Resonance wavelengths not stated: Q rows
  carry the 1530-1610 nm sweep with `wavelength_inferred`.
- Not entered: effective indices TE 1.85 / TM 1.72 and index contrasts (no parameter); EO electrode-to-waveguide
  separation 3 um (design; no electrode-gap parameter for resonator); Table I rows of other works (rule 3).
- EO tuning of a ring filter is entered here (`tuning_efficiency_pm_per_v`); no EO-atlas row exists for this paper.

## Missing fab / facility orgs (name as printed + locator)

- RMIT University: fab, krasnokutska2019 all 10 rows (p.2 Sec. II, components made with the authors' own process of
  ref. 24; all authors at RMIT; D84a). Fab left empty until the org exists.
- Melbourne Centre for Nanofabrication in the Victorian Node of the Australian National Fabrication Facility (ANFF):
  facility, krasnokutska2019 all rows (p.6 Acknowledgments, work performed in part there).
- Nanolab at Swinburne University of Technology: facility, krasnokutska2019 all rows (p.6; parent
  `org_swinburne_university_of_technology` exists, the lab itself does not; the owner is not entered, D82c).
- Australian Microscopy & Microanalysis Research Facility at RMIT University: facility, krasnokutska2019 all rows
  (p.6, use of the facilities acknowledged).

## Registry gaps (skipped value + locator + proposed definition)

- `phase_noise_dbc_per_hz` (laser): single-sideband phase noise of the photodetected repetition-rate carrier at a
  stated offset (offset frequency and carrier in condition); liu2020b ~-110 dBc/Hz at 10 kHz (p.5 Fig. 3(d)).
- `injection_locking_range_khz` (laser): half-width of the RF injection-locking range; liu2020b 40 kHz (p.5).
- `coupling_ratio_eta` (resonator): kappa_ex / kappa as reported; liu2020b samples A-D ~1/3, ~2/3, ~1/2, ~2/3 (p.6).
- `effective_index` (waveguide_platform): krasnokutska2019 TE 1.85 / TM 1.72 at 1550 nm (p.3).
- `confinement_factor_pct` (resonator, waveguide_platform): li2022a LN field fraction 78 % (Fig. 1) / 86 % (Fig. 6).
- Splitter operating bandwidth with a stated criterion (`criterion_bw_nm`, D539 candidate): liu2023a > 150 nm
  measured, 200 nm simulated (criterion not printed, p.1 / p.4).
