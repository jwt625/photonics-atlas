# Batch lit_66 report (distill subagent, 2026-11-02)

Dry-run `batch lit_66: +50 components, +194 metrics; errors 0` (one WARN about another batch's row,
cmp_lit_ni2025b_pimmwc-m18). Page-1 title check: all 7 texts match their source rows; none is a correction / erratum;
no `garbled_text_layer`. Stopped on: none. ASCII only; no e-mail, street or postal text. Facts and locators only.
Renders checked: fatemi2019 Figs. 1, 6, 13, 14, 20, 24 / Table I; spektor2023 Figs. 2, 3, 4; lee2025 pp.1-2 and Fig. 1;
salehzadeh2020 Figs. 3, 4, 5, 8, 9; chen2024 Figs. 1, 4; sundaram2025 Fig. 2 / Table 1. No render of kumar2026 tables was
needed (text tables clean); chen2024 p.7 has no cached render. Supplements of chen2024, sundaram2025 and spektor2023 are
not in the cached texts, so values given only there are absent.

## Per paper (components / metrics)

- fatemi2019 (8 / 37): 128-element sparse 2-D OPA (16 deg, 0.8 deg, SLSR >= 12 dB measured; 0.64 deg and 16 / 10 dB
  design), 512-element design, antenna (51 %, origin not stated), spiral phase shifter (10.6 mW per pi, 19 kHz), Y-splitter
  (0.4 dB), 1x128 tree (2.8 dB, < 1 dB variation), waveguide 2.5 dB/cm, focusing GC 6 dB. Not entered: CMOS driver metrics
  (electronics), average sidelobe -21 dB and grating-lobe leakage about 7 dB (notes), 0.68 um antenna labels (role not
  tied, D156), Fig. 1(b) 500 nm x 220 nm (generic schematic), -28 dB splitter reflection (registry gap).
- spektor2023 (10 / 30; arXiv version of the Optica paper): four 461 nm emitters (20 / 45 deg, vortex, radial design),
  mode converter design, Ta2O5 waveguide (0.29 / 0.57 / 1.45 dB/cm at 780 / 510 / 450 nm), 1x2 and 1x3 splitters, blue / red
  crossing, 589 / 780 nm WDM. Not entered: 3 dB/m C-band (cited, refs. 70, 71), "over 90 %" group claim, measured emitter
  angles (only modeled values are numeric; the experimental panels show agreement), polarization filter (SI only).
- kumar2026 (4 / 24): concave and convex facet elements (ROC, ensemble mean and range), spiral and axicon (excess IL and
  transmission, mean and range). Not entered: substrate focusing structure (no row, see gaps), shape accuracy, Strehl,
  roughness, cone angle, winding number, all-structure means (notes).
- salehzadeh2020 (4 / 28): optimum SSC (4.0-5.0 dB fiber-to-fiber; 1.3-1.8 dB per facet, 65-75 %, derived; Fig. 8 1.6 dB;
  four 1-dB tolerances; simulated values; geometry), 90 nm sibling (Fig. 8 2.7 dB), 300 um series test structure (0.2 dB per
  SSC, 95 %), primary waveguide (0.9 / 1.1 dB/cm TE / TM). Not entered: Fig. 3 per-shape boxes and Fig. 4 contour (mix
  designs), about 5 dB improvement and about 8 dB calculated no-SSC coupling (notes).
- sundaram2025 (11 / 30): PPKTP-PIC butt interfaces (2.37 dB at 656 nm, 4.46 dB at 1536 nm, derived), PIC edge couplers,
  rotator, MZI, Si pump filter (92.5 dB), visible route, PPKTP WDM, input pigtail, output facet. Not entered: SPDC section
  (photon-pair metrics, D250; geometry-only otherwise: 5.8 um period, 7.5 mm), 110 um mode escalator (no loss value, geometry
  only), 4.67 / 5.31 dB whole-PIC difference (notes), Table 1 channel losses (off-chip filters, setup), g2 / CAR / rates.
- chen2024 (7 / 32): 64-channel half-wavelength OPA (FOV 180 and -70 to +70 deg, six SLSR conditions, 2.1 and 1.68 deg, about
  14 dB budget), PDK edge coupler, 3-dB splitter, waveguide, PBS, TiN phase shifter (about 20 mW per pi), composite variable
  splitter (simulated range). Not entered: target patterns, 35 dB targets, cited 25:75 condition (ref. 41), traditional VS
  simulation, Table S1 and supplement sections.
- lee2025 (6 / 13): Si3N4-ULI transition (0.558 dB), smaller-taper design (< 0.18 dB), Si3N4 and ULI waveguides, two fiber
  facets. Not entered: 0.7-0.8 dB/cm (cited, ref. 4), alignment accuracies and inscription settings (no parameters).

## Missing fab / facility orgs (checked organizations.csv and org_aliases.csv)

- Brookhaven National Laboratory (kumar2026 p.1, p.9; candidate fab org).
- Center for Functional Nanomaterials, "Center for Functional Nanomaterials (CFN)" at BNL (kumar2026 p.9; facility, FIB and
  SEM access acknowledged).
- AdvR Inc (sundaram2025 p.1, p.3; PPKTP waveguides made there; fab org for ppktp_wdm, ppktp_input_pigtail, ppktp_output_facet).
- Rochester Institute of Technology (sundaram2025 p.1; authors only, no fabrication role; for reference).
- Registered and used: org_national_research_council_canada (not org_national_research_council, which is the Italian
  CNR), org_aim_photonics, org_chongqing_united_microelectronics_center, org_university_of_california_davis.

## Registry gaps (skipped value + locator, proposed definition)

- `focal_length_um` (micro_optics): kumar2026 p.5 Fig. 3(c), 222.2 +/- 3.6 um on a substrate element; effective focal
  position of the element. Would also make that element (45 um, ROC 106.13 um, Corning 7980) a row.
- `surface_error_rms_nm` or `shape_accuracy_waves` (micro_optics): kumar2026 p.3-4, lambda/50 and lambda/33 at 633 nm;
  residual to the best-fit surface over a stated area.
- `rms_roughness_nm` (D418 gap, confirmed again): kumar2026 p.11 Table III, Sq 0.56 +/- 0.11 unprocessed, 0.83 +/- 0.03 nm
  FIB-processed; areal RMS over a stated scan.
- `cone_angle_deg` (micro_optics): kumar2026 p.5, p.6 Fig. 4(g), 16.44 deg measured half-angle, design 16.0 deg.
- `back_reflection_db` on splitter: fatemi2019 p.12, -28 dB input reflection of the Y-splitter.
- `extinction_db` on waveguide_platform (D417 gap): sundaram2025 p.6, 92.5 dB pump extinction by Si waveguides (entered as
  wdm.other meanwhile).
- `power_consumption_w` on free_space_emitter: chen2024 p.7, about 4 W worst-case heating; fatemi2019 p.15 stays on the phase
  shifter row.
- `tol_1db_vertical_um`: salehzadeh2020 p.8 vertical tolerances are stored in tol_1db_lateral_um as merged precedents do.
- `pair_generation_rate_mhz_per_mw` (D250 still open): sundaram2025 p.6, 67.06 +/- 7.24 MHz/mW inferred, 80 MHz/mW model.

## Judgment calls for the auditor

1. lee2025: transition and both waveguide losses `author_estimate` (D163: calculated coupling term), although the paper says
   "measured". Same-chip, so waveguide_platform.transition, not chip_chip_coupler; platform `other` (no SiN-to-silica hybrid value).
2. lee2025 sin_waveguide keeps both 1.68 dB/cm and < 0.1 dB/cm (p.1, no reference): they disagree.
3. chen2024 OPA beam_divergence_deg: text prints 21 deg beamwidth at 0 deg; entered 2.1 deg from Fig. 4(b) as a lost decimal point (target 2.06 deg).
4. chen2024 180 deg FOV entered as measured, with a separate derived 140 deg for the demonstrated steering span.
5. chen2024 PBS 30 dB: author_estimate; the foundry attribution sits in the sentence before. Splitter, waveguide and PBS loss
   rows `specification` (foundry data, D161 is about thicknesses).
6. fatemi2019: 6 dB GC, 0.4 dB splitter, 51 % antenna `author_estimate` (origin not stated, D418); < 1 dB variation and 2.5 dB/cm
   `measured` (Sec. VII results). Fab empty; abstract says thick SOI, Sec. VI says 220 nm device layer.
7. spektor2023: emitter angles and divergences `simulated` (figure labels on modeled and experimental panels are the design
   targets); 95 % mode conversion `author_estimate`, row design; azimuth values disagree between text and captions (notes).
   10^-4 crossing crosstalk entered as 40 dB derived, wavelength not stated. Fab empty (D154).
8. kumar2026: spherical elements as micro_optics.facet_lens although monolithic rather than 3D-printed; their only performance
   row is the nominal fiber MFD (`mfd_fiber_um`, specification), since ROC is geometry and shape accuracy has no parameter.
   Spiral and axicon `lens_radius_um` 5 is a halved aperture diameter. Text and Table I swap x / y for the concave element.
9. salehzadeh2020: SSCs as fiber_chip_coupler.edge (chen2000 precedent, D422), not micro_optics.vertical_taper. Fig. 9 tolerances
   do not name the design; placed on the ~120 nm default row (p.4). The ~100 um row aggregates the optimum design family.
10. sundaram2025: one row per class for the edge couplers (D396); chip-chip platform `sin` is the PIC side with AIM as fab for that
    side only; PPKTP WDM, pigtail and facet kept in scope as chip-scale fiber-coupled parts (D411), platform `other`;
    rotator platform empty (layers not named); Si pump filter as wdm.other; pump wavelength inferred for the pigtail.
