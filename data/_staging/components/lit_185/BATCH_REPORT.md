# lit_185 batch report

Papers: lit:chang2020a, lit:vogelbacher2019, lit:obrzud2021. verified_on 2026-11-18. All three cached texts are the
arXiv versions of the listed journal papers (page-1 titles match the source rows; none is a correction / erratum):
chang2020a = arXiv 1909.09778v1 of Nature Communications 2020 (34-page preprint layout, figures and Table 1 at the
end); vogelbacher2019 = arXiv 1910.07257v1 of Optics Express 2019 (journal layout with the OSA open-access line);
obrzud2021 = arXiv 2110.12868v1 of APL Photonics 2021. Values are distilled from these cached copies; the journal
versions were not read. Dry-run: +23 components, +85 metrics, 0 errors (the one WARN is on cmp_lit_ni2025b, another
batch).

## lit:chang2020a (AlGaAs-on-insulator microresonator Kerr combs)

Components 5 / metric rows 18:

| component | metrics | content |
|---|---|---|
| cmp_lit_chang2020a_ring_1thz | 8 | Q_L 1e6 (Fig. 3(b) label, measured), Q_0 ~1.53e6 and ~0.4 dB/cm (author_estimate), R 12 um, 700 x 400 nm, 3 um BOX, sidewall ~90 deg (SEM) |
| cmp_lit_chang2020a_comb_1thz | 2 | threshold ~0.036 mW (Table 1 prints mW), line spacing 1 THz (nominal, author_estimate) |
| cmp_lit_chang2020a_comb_450ghz | 4 | > 50 comb lines at 250 uW, line spacing 450 GHz (nominal), 700 x 400 nm |
| cmp_lit_chang2020a_ring_r100_gvd | 3 | FSR 118 GHz near 1550 nm (measured), R 100 um, 400 nm |
| cmp_lit_chang2020a_inverse_taper_facet | 1 | ~5 dB per facet to lensed fiber (measured, D167; C band inferred) |

Fab `org_ucsb` on all rows: the author contributions (p.33) name W.X., L.C. and J.P. as doing the fabrication, all
three at UCSB (D395). No facility is named. Platform `algaas` (first lit rows with this value).

Not entered:
- Comb span > 250 nm at 300 uW (1 THz) and > 200 nm at 250 uW (450 GHz): no comb-span parameter (D81 rejected).
- D2/2pi = 10.8 MHz (R 100 um ring, p.10): dispersion not a parameter (D81). In component notes.
- Fig. 3(c) split resonance near 1577.17 nm: the ring is not named (D159 / D156); no mode_splitting row.
- Soliton step at 2.5 dBm in the bus waveguide, 5 nm/s scan (p.16, Fig. 5): an operating condition, not a threshold
  of a defined quantity; in notes of the 450 GHz comb row.
- Simulated mode area ~0.28 um2, mode-volume factor ~4, ~270x threshold comparison, projected SHG ~10^8 %/W level
  (p.13, p.17): model / projection values without a device (rule 4 / no parameter).
- Table 1 rows of other platforms (refs. 14, 19, 21, 34, 46-50): cited values (rule 3). The "this work" row repeats
  the text values (Q 1.5e6, 0.036 mW), used only as the mW locator for the threshold.
- Material constants (n2, thermo-optic coefficient, bandgaps): not component metrics.

Judgment calls:
- Q_0 1.53e6 `author_estimate` (D403): one Lorentzian fit; the under-coupled branch (Q_0 / Q_L = 1.53) is not shown
  to be the right one. The dip depth (near zero on the plot) is consistent with it but does not fix the regime. The
  0.4 dB/cm follows from Q_0 with an unprinted group index (D76), also `author_estimate`.
- Resonance wavelength 1519 nm as in the text (p.11); caption says "around 1518 nm" and the plot axis is
  1518.90-1518.92 nm. Recorded in notes, no D417 conflict (rounding).
- The 1 THz ring is one physical device with resonator and comb functions: two rows with cross-notes (D396).
- Comb line spacings 1 THz / 450 GHz entered as `channel_spacing_ghz` (D83b, ji2020 precedent) but `author_estimate`
  rather than measured: they are round nominal FSR labels, no measured spacing is printed. The audit may prefer
  label-only (no row).
- Threshold `ref_plane` left empty: the paper does not say whether 36 uW is on-chip or fiber power.
- Sidewall angle ~90 deg (SEM Fig. 2(c), device not named) entered once, on the 1 THz ring row, as the process
  cross-section.
- Facet loss "around ~5 dB" per facet `measured` (D167 / D462; no arithmetic, isolation method not stated). D418
  (nader2025) kept a similar unstated-origin value as author_estimate; flagged for the audit.

Registry gaps: comb span (nm) for laser.comb (D81 rejected; skipped values 250 / 200 nm, p.12); dispersion D2/2pi
(rejected D81; 10.8 MHz, p.10). No new proposal.

## lit:vogelbacher2019 (SiN partial Euler bends at 850 nm)

`garbled_text_layer` on page 11: the TE values (0.028 / 0.007 dB) and the TM 0.5 dB sentence were confirmed on the
page render; Fig. 9 markers were read from the PDF vector data (marker centres) with axis ticks located on a 10x
render of the page (pymupdf in the repo environment, scratch scripts only).

Components 17 / metric rows 60:

| component | metrics | content |
|---|---|---|
| cmp_lit_vogelbacher2019_euler90_reff50_{p0, p0p05, p0p1, p0p15, p0p2, p0p3, p0p5, p0p7, p1} (9 fabricated) | 4 each | TE and TM bend loss per 90 deg at 850 nm (TE p = 0: 0.028 dB and p = 0.2: 0.007 dB from the text, measured; all other TE and all TM points from Fig. 9 vector reads, extracted_from_figure), width 680 nm (SEM), SiN 160 nm nominal |
| cmp_lit_vogelbacher2019_b45_reff40_{p0, p0p3, p1} (3 design) | 3 each | simulated 45-deg bend loss 0.09 / 0.07 / 0.14 dB as `insertion_loss_db` per_component (per 45 deg), 700 x 160 nm |
| cmp_lit_vogelbacher2019_b90_reff40_{p0, p0p2, p1} (3 design) | 3 each | simulated 0.10 / 0.05 / 0.19 dB per 90 deg |
| cmp_lit_vogelbacher2019_b90_reff70_{p0, p0p2} (2 design) | 3 each | simulated 0.026 / 0.001 dB per 90 deg |

Fig. 9 reads (dB): TE p = 0.05 0.0149, 0.1 0.0078, 0.15 0.0078, 0.3 0.0078, 0.5 0.0087, 0.7 0.0091, 1.0 0.0118 (TE
p = 0 marker 0.0276, p = 0.2 0.0071 agree with the printed 0.028 / 0.007); TM p = 0 0.660, 0.05 0.510, 0.1 0.684,
0.15 0.734, 0.2 0.784, 0.3 0.836, 0.5 1.036, 0.7 1.236, 1.0 1.309. Uncertainty about +/- 0.0003 dB (TE) and
+/- 0.01 dB (TM). The printed TM minimum "0.5 dB" (p.11) matches the p = 0.05 point and is in that row's notes.

Fab empty on all rows: "fabricated on a SiN photonic platform [39]" (p.10) is passive and names no org; ref. 39 is
an ams AG paper and two authors are at ams AG (`org_ams_ag` exists; merged nevlacsil2020 has an explicit "fabricated
by ams AG" sentence), but no fabrication statement in this paper (D433, D80b). process_name empty (no process phrase
printed). No facility.

Not entered:
- 180-deg bends (p.9): "decreases from 0.083 dB to 0.047 dB for Reff = 40 um" cannot be tied to Fig. 7 points (the
  Reff = 40 um curve reads about 0.11 dB at p = 0, about 0.047 dB at p = 0.05 and about 0.028 dB near p = 0.2;
  0.083 dB matches no marker). Printed values not tied to a design: not entered (D156 / D159).
- Effective radii for a 0.1 dB target (36 / 39 / 45 um) and for the 0.026 dB target (43 / 57 um), density factors
  1.17 / 2.7 / 1.8 (p.7-8): Reff is not min_bend_radius_um (D619) and no parameter fits; text only.
- EME / FDTD benchmark "agree within 0.01 dB, or 7 %" (Fig. 3, Reff 40 um): method check, not a device value.
- EME curves for the fabricated bends (Fig. 9, h = 158 / 160 nm, n 1.92) and the remaining Fig. 4 / 5 / 7 curve
  points: only text-stated simulated values were entered; the measured Fig. 9 points carry the fabricated rows.
- "+0.2 dB for a pure Euler bend when the simulated height goes from 160 to 158 nm" (p.11): simulated sensitivity,
  no parameter.
- Propagation losses 0.7 dB (TE) / 0.4 dB (TM) "included in the numerical simulations" (p.10) carry ref. [8] and
  no length or unit basis (dB vs dB/cm unclear): cited input (rule 3).
- Refractive indices (ellipsometry 1.92 / 1.46): in core_material / cladding text only.

Judgment calls:
- One row per bend parameter p (sibling designs, rule 9); TE and TM as two metric rows per design.
- Text-stated TE values kept `measured` with method `reference_structure`: the per-bend value comes from a difference
  to a reference waveguide divided by 240 (TE) or 4 (TM), but no totals are printed (D452 / D567 reading of D80a). If
  the audit applies D80a strictly, these two rows become `derived`; the figure reads stay extracted_from_figure.
- Simulated rows are `row_kind: design` (700 x 160 nm, n 2.02 literature index; not the fabricated 680 nm / n 1.92
  waveguide). The 45-deg values use `insertion_loss_db` per_component with "per 45-deg bend" in the condition
  (deng2024 precedent for non-90-deg bends).
- Reff 70 um for the 0.001 dB (p = 0.2) design: the p.6 sentence says "larger than approximately 70 um"; Fig. 5(a)
  at Reff = 70 um confirms about 0.001 dB; noted on the row.
- Polarization `te` / `tm` for the paper's TE-like / TM-like modes (condition text says "-like").

Registry gaps: none new. Effective radius of Euler bends has no parameter (D619 keeps it in labels / notes; skipped
values 50 / 40 / 70 um and the target radii above).

## lit:obrzud2021 (LNOI waveguide for on-chip f-2f self-referencing)

Components 1 / metric rows 7:

| component | metrics | content |
|---|---|---|
| cmp_lit_obrzud2021_lensed_fiber_facet | 7 | ~6.2 dB per facet lensed SMF to air-clad LNOI waveguide (measured, D167; 1555 nm inferred); width 1300 nm nominal, 600 nm x-cut film, 400 nm etch, 200 nm slab (derived), sidewall 55 deg to the film plane (derived from the printed 35 deg to the normal), 4.7 um BOX |

Fab `org_csem`: "fabricated at CSEM's micro-fabrication facility" (p.2), all authors at CSEM. The company's own
cleanroom is not entered as a facility (D404). NanoLN (LNOI wafer supplier) in notes only.

Not entered:
- The 1300 nm nonlinear waveguide (supercontinuum + SH generation for f-2f) as its own row: no registry performance
  parameter applies (rule 9; geometry-only). Its geometry is on the facet row. Values: about 140 pJ pulses at
  1555 nm give a more than octave-spanning spectrum, SH from about 600 to 900 nm (p.2, Fig. 2(b)); pulse energy has
  no parameter (`pulse_energy_pj` candidate, D433).
- fceo beat SNR 56 dB (in-loop) / 45 dB (out-of-loop) at 30 kHz RBW, fceo standard deviation 0.1 / 6.8 mHz, Allan
  deviation, integrated phase noise 233 / 255 mrad (234 mrad in the conclusion), frep phase noise: system / lock
  metrics, not component values.
- Supercontinuum power stability (Table I, +/- 3 sigma limits at 700-1900 nm, < 25 % deviation over 72 h): no
  parameter.
- 0.5 dB per facet with mode converters (refs. 34, 35): cited (rule 3).
- Si PIN photodiode at the waveguide output: purchased setup detector (rule 13).
- Input-facet damage seen in SEM (p.6): no value.

Judgment calls:
- Facet loss ~6.2 dB `measured` per_facet (D167; "measured coupling losses ... per facet", isolation method not
  stated). Wavelength 1555 nm `wavelength_inferred` (source centre; no wavelength with the value).
- Width 1300 nm put on the facet row: the loss sentence speaks of "the waveguides with an air top cladding" of the
  current system; the experiment's waveguide is the 1300 nm one (noted).
- Sidewall angle converted to the registry convention (90 - 35 = 55 deg, derived); the printed value is a process
  result shown in the Fig. 2(a) SEM.

Registry gaps: pulse energy for supercontinuum / frequency-converter waveguides (skipped 140 pJ, p.2; existing
candidate D433), fceo beat SNR (skipped 56 dB, p.5; system-level, not proposed).

## Missing orgs

None. UCSB (`org_ucsb`) and CSEM (`org_csem`) are in the registry. vogelbacher2019 names no fabricating org.
