# Batch lit_305 report

Papers: lit:feldmann2021, lit:bogaerts2020. Distilled 2026-11-27. Validation: `merge_component_staging.py
data/_staging/components/lit_305 --dry-run` -> +6 components, +19 metrics, 0 errors (the 2 warnings are in other
batches: guo2024a, ni2025b).

Page-1 title check: feldmann2021 text p.1 "Parallel convolution processing using an integrated photonic tensor core"
(arXiv 2002.00281 v2; the source row title says "convolutional"; same work, preprint wording). bogaerts2020 text p.1
"Programmable photonic circuits", "Review paper - formatted final submitted manuscript" (Ghent University repository
copy of the Nature review). Neither file is a correction / erratum or another paper.

## lit:feldmann2021 (6 components / 19 metric rows)

Preprint only: values are from the arXiv text; journal version unread; the Supplementary Information (sections 4, 6,
11-14, Figs. S1-S7) is not in the cached copy. Noted on every component row.

| component | class | metrics |
|---|---|---|
| cmp_lit_feldmann2021_matrix_dc | splitter.directional_coupler | excess_loss_db 0.1 per_component measured (p.13, Fig. 5(d) caption); width 1200 / core 325 / etch 325 / BOX 3.3 um |
| cmp_lit_feldmann2021_matrix_crossing | crossing.other | crossing_loss_db 0.12 measured (p.13, Fig. 5(d) caption); same stack (4 rows) |
| cmp_lit_feldmann2021_sin_waveguide | waveguide_platform.straight | prop_loss_db_per_cm 0.2 author_estimate (p.13, origin not stated); same stack (4 rows) |
| cmp_lit_feldmann2021_comb_ring | resonator.ring | q_loaded > 5e6 measured (p.26); fsr_ghz 100 author_estimate (p.26) |
| cmp_lit_feldmann2021_soliton_microcomb | laser.comb | channel_spacing_ghz 100 measured (p.9, p.27, Fig. 2(e) label) |
| cmp_lit_feldmann2021_comb_chip_edge_coupler | fiber_chip_coupler.edge | insertion_loss_db 4 per_facet mean measured (p.26, "average loss 4 dB/interface") |

Values not entered and why:
- PCM (GST) cell as `phase_shifter.phase_change`: no cell-level performance value in the main text; "more than 8-bit"
  closed-loop programming precision is only shown in Supp. Fig. S6 (not cached); 5-bit resolution (std 0.008,
  Fig. 5(c)) is a system-level MAC result. Cell geometry (10 nm GST + 10 nm ITO, 3 x 3 um2) is in the crossing
  row's core_material (geometry-only items are not rows, rule 9).
- Measured matrix losses for fabricated matrices up to 32 x 32 (Fig. 5(d) stars): no printed values, read only
  against heatmap contours; the PCM crossbar matrix as a whole has no class (compute core).
- Directional-coupler wavelength range "approximately 100 nm" (p.14): criterion not stated; split ratios only in
  the Supplementary Information.
- Comb span "more than 25 THz" (p.9, Fig. 2(e)) and lines "from 1500 nm to 1650 nm" (p.15): no comb-span parameter
  (D81 rejected). "> 8 hours of continuous operation" (p.27): no parameter.
- "High Q factors reaching 10^7" (p.26): capability of the cited Photonic Damascene process (ref. 56), rule 3.
- Microring cross-section "0.82 x 1.50 um" (design, p.26): not split into core_thickness_nm / width_nm because the
  text does not say which number is the height (kept in core_material).
- Anomalous GVD "about 1-2 MHz" (p.26): dispersion not a registry parameter (D81).
- 1 mW / 10 mW per heater, 11,000 um2 per interferometer (p.3-4): cited from refs. 27 / 30, rule 3. Crossing
  improvement (ref. 58), foundry-scale matrices (ref. 65): cited.
- System figures (2 TMAC/s, 1.2 TOPS/mm2, 0.4 / 7.0 TOPS/W, 17 fJ/MAC, 95.3 % / 96.1 % accuracy, 285 x 354 um MAC
  cell, < 30 x 30 um2 SOI projection): system level or projections, no component class.
- Setup equipment (rule 13): MEMS VOAs, fibre multiplexers, EOMs ("40 GHz bandwidth" p.13 vs "20 GHz" p.25,
  inconsistent in the preprint), New Focus 2011 detectors, 12 GHz photodiode, EDFAs, notch filter.
- 3D-printed TIR couplers (refs. 53, 54, own earlier work) and the Bragg grating couplers for PCM programming: no
  values in the main text (Supp. section 12 not cached).

Fab / facility orgs: none entered. Matrix chips: passive fabrication text with no org (p.24, D80b); wafer supplier
Rogue Valley Microdevices (p.24) as a note. Comb chips: "fabricated using Photonic Damascene process" (p.26), passive,
process cited to ref. 56: fab empty, `process_name` "Photonic Damascene process (ref. 56)" (che2024 form). No
acknowledgment section in the cached copy, so no facility statement. Missing registry orgs: none.

Judgment calls:
- The 0.1 dB per directional coupler is entered as `excess_loss_db` (loss beyond the ideal 1/(m x n) split that the
  paper accounts separately, D43); printed wording "insertion loss" in notes.
- Coupler / crossing / Q / packaging losses stated as "measured" or as fabricated-device values without shown
  method: `measured`, method `unspecified` (D167 analogue). Waveguide 0.2 dB/cm given in parentheses with no method or
  citation: `author_estimate` (origin not stated).
- Microring FSR 100 GHz `author_estimate` (design or measured not stated, D82a); the measured 100 GHz line spacing is
  on the comb row (`channel_spacing_ghz`, D83b: no pulse characterization). Ring and comb are one device, two classes
  (D396), plus the packaging edge coupler of the same chip.
- Edge-coupler "4 dB/interface" entered as `per_facet` with statistic `mean`; how the per-interface value was
  isolated is not stated (method `unspecified`).
- Wavelength: no value carries a stated wavelength; C band inferred on all wavelength-conditioned rows with the
  reason in notes (C-band EDFA on the comb lines and pump, 1550 nm programming, dispersion designed around 1550 nm).
- Matrix-stack geometry (1.2 um width, 325 nm SiN fully etched, 3.3 um oxide) repeated on the three matrix rows
  (feldmann2019 precedent).

Registry gaps (candidates, not added):
- `comb_span_thz` (laser.comb): full spectral span of a comb as stated; skipped value "more than 25 THz" (p.9,
  Fig. 2(e)). D81 rejected comb span; listed again for the coordinator.

## lit:bogaerts2020 (0 components / 0 metric rows)

Review (Nature, "Review paper"). No row entered:
- Generic technology statements are not device results: waveguide losses "0.1-1 dB/cm" (p.5), thermal tuners
  "several mW", "10-100 us" (p.5), "~0.05-0.2 dB per gate" (p.5), modulators "exceeding 50 GHz" (p.7, refs. 57 / 85),
  "~1 million components per cm2" (p.10).
- Design examples: "~1 mm" segment -> "~50 GHz" FSR (p.5, p.7) is a calculation example, not a device.
- Fig. 2(c) (26 inputs, 88 MZI, 240 control lines) credited to refs. 6 / 15; Fig. 2(b) to ref. 31: cited (rule 3).
- Fig. 3(f) double-ring add/drop filter transmission in a hexagonal mesh (p.4): the hexagonal mesh is credited to
  ref. [44] (authors' own earlier work); the review states no device, platform, process or value for it and gives no
  provenance for the measurement, so any number would be a figure reading of reproduced work (D80i, D259 / D408;
  errandoherranz2019 / fontaine2022 review precedent).

Fab / facility orgs: none. Acknowledgements (p.11) list grants and "Polifab, Politecnico di Milano ... for supporting
the review of technology aspects": support of the review text, not fabrication or work performed (D80c); not
entered, no missing org.

Registry gaps: none.
