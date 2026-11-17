# lit_166 batch report

Distilled 2026-11-16 under the pic-component-distill skill (Contracts v4-v7). 4 papers, 14 components, 72 metric rows.
`merge_component_staging.py data/_staging/components/lit_166 --dry-run`: +14 components, +72 metrics, 0 errors, no
warnings on this batch. Page-1 titles match the source rows for all four cached texts; no correction / erratum, no
garbled text layer.

| paper | components | metric rows |
|---|---|---|
| tabatabavakili2019 | 6 (4 resonator.disk, 2 laser.other) | 21 |
| shiran2021 | 2 (splitter.mmi, mode_converter.mdm_mux) | 22 |
| li2025h | 2 (splitter.y_branch, row_kind design) | 13 |
| doolin2015 | 4 (resonator.disk) | 16 |

## lit:tabatabavakili2019 (Sci. Rep. 2019, arXiv v3 text with supplement p.11-16)

III-nitride (InGaN/GaN QW) 5 um microdisks on Si with bent, suspended bus waveguides; optically pumped, blue.

- Rows: resonator.disk for the A = 90 deg gap series 30 / 45 / 55 / 120 nm (q_loaded, gap, radius, bus width; fsr_nm
  3.6-4.0 nm on the 45 nm device; q_intrinsic on the 120 nm device), laser.other for the 45 nm device (lasing at 416 /
  420 nm, text) and the 120 nm device (lasing peak about 420.7 nm, Fig. S7(a) read). Resonator and laser rows of one
  device carry cross-notes (D396).
- Judgment calls:
  - Q_int = 4700 is the Lorentzian-fit loaded Q of the 120 nm gap device: entered as `q_loaded` measured and
    `q_intrinsic` author_estimate (negligible coupling assumed; the paper's Q_C > 1e5 at 120 nm is computed from this
    Q_int; D403, ilchenko1999 precedent).
  - Q_loaded of the 30 / 45 / 55 nm devices read from the labelled Fig. 4(d) points (about 1270 / 2230 / 3150, +/- 50),
    cross-checked against Fig. 2(d) ratios; the printed "factor 2 reduction at 45 nm" in notes.
  - Mode spacing 3.6-4.0 nm entered `measured`: the sentence covers the experimental and simulated spectra, whose mode
    positions coincide in Fig. S2.
  - Measured gaps and width (SEM) `measured`; per-device nominal gaps are stated only for the 45 nm device (nominal 50).
  - Platform `other` (no III-nitride platform value), stack in core_material.
- Not entered: lasing thresholds in mJ/cm2 per pulse (1.7 at 45 nm, 1.2 = 300 kW/cm2 at 120 nm, Fig. 4(c) per gap and
  angle) - no areal pump-threshold parameter; text 1.7 vs Fig. 4(c)/(d) about 1.8 mJ/cm2 for the 45 nm device noted
  (D417); A = 0 deg devices (thresholds only); 30 / 55 nm lasing (Fig. S6, thresholds only); out-coupled signal in a.u.
  (Fig. 5); proximity-effect blue shift 0.8 nm per 10 nm gap (no parameter); estimated ng_eff 3.2 and Q_abs,QW 5000
  (model estimates); linewidth narrowing near threshold (spectrometer resolution not stated, D250); fit constants B, F, C.
- Fab / facility: "We fabricated" with authors at four organizations (C2N / Univ. Paris-Sud, Univ. Grenoble Alpes /
  CEA, L2C Montpellier, CRHEA) -> fab empty (D80b, D154). RENATECH only as support in the acknowledgments (program,
  D80c; billet2022 precedent). No missing orgs.

## lit:shiran2021 (Opt. Express 29(15), 2021)

- Rows: SWG dual-mode 2x2 MMI (`splitter.mmi`: measured excess loss TE0 0.28 / TE1 0.65 dB, crosstalk > 17 dB;
  simulated excess loss < 0.4 dB, crosstalk > 32 dB, phase error 0.9 / 2.8 deg; Table 1 geometry) and the ADC two-mode
  multiplexer test structure (`mode_converter.mdm_mux`: worst IL 0.34 / 1.04 dB, crosstalk >= 19.66 dB).
- Judgment calls:
  - TE0 excess loss: abstract prints < 0.1 dB, body 0.28 dB, conclusion < 1 dB; body values entered with the conflict
    in notes (D417).
  - MMI loss `measured`, method reference_structure, excludes GCs (GC-GC straight-waveguide normalization) and the mode
    (de)multiplexers (stated, not shown; D167).
  - MMI crosstalk is measured through the whole MDM link incl. the (de)multiplexers (condition / notes).
  - Multiplexer "worst IL of the mode multiplexer" from a mux-demux cascade: scope per_component, basis measured
    (D167), the isolation step not shown (notes).
  - Fab `org_applied_nanotools` ("fabrication through Applied Nanotools Inc", p.8); process_name empty (no named
    process).
  - width_nm 1000 derived from the printed 1 um input width (D157).
- Not entered: SWG period counts NMMI 148 / NT 37, separation S 1.05 um, SWG duty cycle 0.5 (fill_factor not allowed on
  splitter); simulated taper IL < 0.1 dB and TE1 slab-to-SWG 0.1 dB per conversion (sub-parts); cladding voids
  < 500 nm2; Table 2 rows of other works (rule 3); GC (no values).
- Missing orgs: none.

## lit:li2025h (Chin. Opt. Lett. 23(2), 2025)

- Simulation-only paper (FDTD, direct binary search); no fabrication or measurement. Two `splitter.y_branch` rows,
  `row_kind: design`, fab empty: the 100 nm radius index-perturbation hole design (excess loss <= 0.7 dB over
  1300-1650 nm) and the 150 nm radius Sb2S3 six-level design (excess loss <= 0.34 dB at 1550 nm; imbalance 0.57-2.70 dB
  from the printed ratios 1.14-1.86, simulated per D83f).
- Judgment calls: the paper's IL = -10 lg((T_up + T_down)/T_in) is loss beyond the ideal split -> `excess_loss_db`
  (D43). "Measured at 0.34 dB" sits in the simulation section (Fig. 6 captioned simulation) -> simulated; abstract
  0.35 dB and introduction 0.4 dB in notes. Conclusion names a 100 nm radius; the Sb2S3 design uses 150 nm (noted).
- Not entered: radius sweep (max 0.35 dB at r = 0.3 um, 1450 nm; a sweep over designs), approximate ratio span 2.2-0.8
  for the index sweep, cascaded 16-splitter array (no metric), PCM hole radius (no radius parameter on splitter), Sb2S3
  indices (cited model inputs).

## lit:doolin2015 (Appl. Phys. Lett. 2015, arXiv text)

- Rows: four undercut Si3N4 microdisks (15 / 20 / 25 / 30 um, 150 nm film), each with q_loaded (fiber attached, in
  water), q_intrinsic (paper's "unloaded" Q, fiber hovered), radius (derived) and film thickness (design_target, D402).
- Judgment calls:
  - 20 um loaded Q 1.5e4 from the abstract (`measured`); other loaded Qs read from Fig. 4(c) (log axis, +/- 15 %,
    PyMuPDF zoom render of the vector figure).
  - "Unloaded" Q (fiber hovered away) entered as `q_intrinsic` author_estimate (D403, ilchenko1999 precedent), values
    read from Fig. 4(c); the printed "> 1e5 for the 25 and 30 um disks" in notes.
  - Wavelength 780 nm as stated for the light (modes within the 765-781 nm laser range, notes); polarization TE from
    the paper's simulation-based mode identification.
- Not entered: refractive-index sensitivity (200 +/- 30 nm/RIU abstract, 230 +/- 20 nm/RIU body, 221-238 nm/RIU per
  event, Fig. 4(b) per diameter), detection limit (1.3 +/- 0.1) x 1e-6 RIU, 0.1 pm wavelength std - no sensing
  parameter; mode splitting "a few pm" (no number); dimpled tapered fiber > 50 % transmission (setup equipment, rule
  13); estimated thinning to about 120 nm (estimate) and 3 um oxide (removed in the undercut; not drawn).
- Fab / facility: passive "Devices were fabricated", all authors University of Alberta -> fab empty (D80b); no
  facility named. Wafer supplier Rogue Valley Microdevices in notes. No missing orgs.

## Registry gaps (proposals)

1. `pump_threshold_density_mj_per_cm2` (laser; pulsed optical-pump threshold energy density per pulse, mJ/cm2;
   tabatabavakili2019 1.7 mJ/cm2 at g = 45 nm, p.4 / p.5 Fig. 3; 1.2 mJ/cm2 at g = 120 nm, p.13 Supp. Fig. S7) and / or
   `pump_threshold_intensity_kw_per_cm2` (300 kW/cm2, p.13 Supp.). `pump_threshold_mw` does not fit areal values.
2. `ri_sensitivity_nm_per_riu` (resonator; bulk refractive-index sensitivity of a resonance, nm/RIU; doolin2015
   230 +/- 20 nm/RIU, p.3) and `ri_detection_limit_riu` (doolin2015 (1.3 +/- 0.1) x 1e-6 RIU, p.3).
3. `fill_factor` and `n_periods` on splitter for SWG MMIs (shiran2021 duty cycle 0.5, NMMI 148, NT 37; p.4, p.6
   Table 1); `radius_um` (or a `hole_radius_nm`) on splitter for perturbation holes (li2025h 150 nm, p.4).
4. `coupling_angle_deg` on resonator (bus wrap angle around a disk / ring; tabatabavakili2019 A = 0-90 deg, p.3).
