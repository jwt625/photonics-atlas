# lit_275 batch report

Papers: lit:buf2015, lit:sapra2019, lit:shi2014, lit:fang2016. Page-1 titles match the source rows (buf2015 is the
JLT vol. 34 no. 2 2016 print of the 2015-09-22 online paper). Total 38 components / 300 metric rows.
`merge_component_staging.py --dry-run`: +38 components, +300 metrics, 0 errors (two pre-existing warnings on other
batches: cmp_lit_guo2024a_exc02, cmp_lit_ni2025b_pimmwc). verified_on 2026-11-24. Helper scripts (generator, PDF
vector readers) are in the session scratchpad `lit_275/`.

## lit:buf2015 (8 components / 49 metrics)

STMicroelectronics / Luxtera PIC25G 300 mm platform review (invited). Platform statistics only; no device-level
design study.

- `cmp_lit_buf2015_smw_rib` (waveguide_platform.straight, soi_rib, 6): Table I SMW 1.8 dB/cm mean / 0.18 std at
  1310 nm (measured); 1.4 dB/cm typical at 1490 nm (author_estimate, no data shown, D544); 310 nm Si, Tslab 166 nm
  target, BOX 0.72 um (derived from 720 nm).
- `cmp_lit_buf2015_mmw` (waveguide_platform.straight, soi, 4): MMW 0.25 mean / 0.07 std dB/cm at 1310 nm.
- `cmp_lit_buf2015_spgc` (fiber_chip_coupler.grating, 11): peak loss 1.8 / 1.45 dB in epoxy (1310 / 1490 nm, typical),
  2.2 dB mean / 0.15 std in air at 1310 nm (Table I), 1.8 dB typical and 0.1 dB std (Fig. 6(d), > 20 k dies) in air at
  1490 nm, peak-wavelength dispersion 5 sigma ~12 nm, fiber angle 8 deg, stack.
- `cmp_lit_buf2015_psgc` (fiber_chip_coupler.grating, 7): 3.2 dB mean / 0.26 std in air at 1310 nm (Table I), 3.1 dB
  typical at 1490 nm (author_estimate), 8 deg, stack.
- `cmp_lit_buf2015_hspd` (photodetector.ge_waveguide, 5): 0.98 A/W mean / 0.05 std at 1310 nm, -1 V; 10 nA mean at
  -1 V; median bandwidth > 20 GHz at -1 V; Ge 250 nm (measured process result).
- `cmp_lit_buf2015_bend_slab163` (waveguide_platform.bend, 8): Fig. 15(a) mean loss per bend at 1310 nm for R 27.5 /
  30 / 32.5 / 35 / 37.5 / 40 um = ~0.21 / 0.135 / 0.055 / 0.025 / 0.008 / 0.005 dB (raster read, +/-0.02 dB;
  bend angle not stated, so insertion_loss_db per_component, not bend_loss_db_per_90).
- `cmp_lit_buf2015_ring_r40_slab163` and `cmp_lit_buf2015_ring_r5_slab50` (resonator.ring, 4 each): FSR 1.72 nm and
  10.9 nm (figure labels, measured), radius, slab 163 / 50 nm, 310 nm core.

Not entered: high-speed phase modulator (HSPM) 17.2 deg/mm mean (std 0.4) and 10.5 deg/mm at 2.5 V, VpiLpi 2.5 V cm,
loss 6 / 4 dB/cm (p.4 Sec. IV, Table I, Fig. 6(a)) - Si PN modulator values with no per-length phase-shifter
parameter (D250) and modulator metrics (EO-atlas scope question); TX MZM total loss 9.2 dB incl. GCs, ER > 4 dB,
275 mW, RX sensitivity -11.9 dBm (system / modulator values, p.6-7); DSOI back-reflector GCs: 0.6 dB average
improvement (no parameter) and "down to 0.85 dB SPGC / 2.2 dB PSGC at 1490 nm" (attributed to the authors' ref. [26],
D259; p.7 Sec. VII.A) - the DSOI GC therefore has no own metric and is not a row (TEM labels 742 nm SiO2 / 86 nm
poly-Si / 291 nm SiO2, Fig. 14); text PSGC 3.25 dB at 1310 nm (conflicts with Table I 3.2 dB; kept in notes);
"responsivity close to 1 A/W" (duplicate of Table I); dark-current std "0.1 decade"; R = 40 um "FSR of only 2 nm"
(rough lambda^2/R estimate); Fig. 15(b) simulated 50 nm-slab bend curve (y axis "Insertion Loss (dB/cm)", values
0.0127-0.0164, normalization unclear); ring notch depths (vary along the raster traces); process statistics (Tslab
within-wafer range 60 A, wafer-to-wafer sigma 23 A over 160 wafers, 193 nm litho minimum feature 80 nm sigma 1.9 nm,
PN overlay +/-20 nm; in component notes); Cu-pillar interconnect parasitics (electrical); the 163 / 50 nm slab
transition taper (no performance).

Fab: empty on all rows. The process is first person ("We pattern the silicon layer", p.3) and the platform is
"developed into a 300 mm manufacturing facility" (p.1), but no org or site is named for fabrication and the authors
sit at STMicroelectronics and Luxtera (D154 / D80b). `process_name` = "PIC25G" (printed platform name; Contract v7
named process, no named foundry). No facility named.

## lit:sapra2019 (25 components / 201 metrics)

- 20 grating-coupler rows `cmp_lit_sapra2019_gc_e{40,60,80,100}_t{40,60,80,100,120}` (etch fraction x target 3-dB
  bandwidth): 3 fabricated (fully etched, targets 40 / 100 / 120 nm) and 17 design rows. Every row: simulated 3-dB
  bandwidth (Fig. 3, relative to the 1550 nm efficiency) and simulated loss at 1550 nm (Fig. 4), both read from the
  PDF vector marker centres (+/-1 nm, +/-0.02 dB; the Fig. 3 and Fig. 4 abscissae agree within 1 nm); grating length
  12 um, fiber angle 5 deg, MFD 10.4 um (specification, SMF-28 model), 220 nm core, 2 um BOX, etch depth derived from
  the etch fraction. Fabricated rows add measured peak loss read from the Fig. 7 vector paths (loopback_half,
  extracted_from_figure: 4.4 dB at ~1514 nm, 5.4 dB at ~1511 nm, 6.3 dB at ~1529 nm), measured 3-dB widths (52 and 94
  nm peak-referenced figure reads; "> 120 nm" printed for the 120 nm-target device), grating width 12 um, taper 215 um,
  500 nm waveguide.
- 4 design rows `cmp_lit_sapra2019_gc_ref23_a{25,20,15,10}` (ref. [23] stack: 3 um BOX, 40 nm feature): Fig. 9 peak
  loss and 3-dB bandwidth per incidence angle; the 25 deg row carries the text values (peak 2.29 dB, 1-dB bandwidth
  64 nm, back reflection ~15 dB).
- `cmp_lit_sapra2019_si_wire_500nm` (waveguide_platform.straight, soi_strip, 4): 34 dB/cm derived (printed 3.4 dB/mm),
  1550 nm inferred.

Not entered: Fig. 2 simulated spectra and back-reflection curves (same designs, back reflection not quantified in
text); Fig. 7 dashed simulated spectra (Fig. 3 / Fig. 4 values used); Fig. 8 overetch study (0 / 4 / 8 / 12 nm
trench enlargement, simulated spectra); "less than 0.5 dB" measured-simulated discrepancy and "7-19 nm" bandwidth
difference (comparisons, not device values); ~40 nm blue shift (note); ref. [23] values (-3.6 dB, 84 nm, cited);
edge-coupler numbers of ref. [3] (cited).

Fab: org_stanford_university ("We fabricated and characterized the fully-etched gratings", p.4; all authors at
Stanford Ginzton Laboratory, one also KU Leuven); facility org_stanford_nanofabrication_facility +
org_stanford_nano_shared_facilities ("All devices were fabricated at the Stanford Nanofabrication Facility and Stanford
Nano Shared Facilities", p.1 footnote; 2019, pre-merger orgs per D80d). Design rows: no fab / facility. Google Cloud
(compute) and gift acknowledgements are not facilities.

## lit:shi2014 (2 components / 22 metrics)

- `cmp_lit_shi2014_gc_nonuniform` (fiber_chip_coupler.grating, soi, 15): 2 dB at 1302 nm (loopback_half, measured,
  D167), 3-dB bandwidth 50 nm, back reflection > 20 dB (derived from the 0.06 dB ripple, O band inferred), simulated
  25 dB back reflection and 1.6 dB optimum loss, 17 deg, 9.2 um target MFD (specification), 220 nm / 2 um BOX / 2.1 um
  cladding, etch 60 nm (front 11 grooves) and 130 nm (rest), periods 490-560 nm (first 20 grooves, Table I), 420 nm
  waveguide, 11 um grating width.
- `cmp_lit_shi2014_gc_uniform` (fiber_chip_coupler.grating, soi, 7): 2.6 dB at 1300 nm, period 500 nm, 60 nm etch,
  fill factor 0.56 (derived from the 220 nm gap), 17 deg, 220 nm / 2 um BOX.

Not entered: simulated mode-mismatch loss 0.5 dB (no parameter); 200 nm minimum feature; per-groove gaps of Table I
(no registry parameter for a gap set on a GC); 34 um focal distance (in notes); 0.9 nm ripple period; values of refs.
[8]-[18] (cited, incl. 0.62 / 0.75 / 1.6 / 1.5 / 3 dB of other GCs).

Fab: org_astar_ime ("The device was fabricated on an 8-inch SOI wafer at Institute of Microelectronics (IME)/A*STAR",
p.3 Sec. III). process_name empty (only "multi-project wafer" and "248 nm DUV" printed; no PDK name). OpSIS appears
only in the funding line (not entered).

## lit:fang2016 (3 components / 28 metrics)

- `cmp_lit_fang2016_cantilever_ssc` (fiber_chip_coupler.edge, soi, 19): best 1.5 dB (TE) / 2.1 dB (TM) per facet with
  index-matching liquid and ~2.6 / 3.0 dB without (per_facet, cutback, 1520-1620 nm), 1-dB bandwidth > 100 nm
  (author_estimate, fills the whole measured span, D435 / D459), 1-dB tolerances +/-2.5 um (X) and +/-2.0 um (Y,
  vertical in condition), fiber MFD 10.5 um (specification), simulated > 80 % at 1550 nm, Table I geometry (SiO2
  waveguide 12 x 8 um, both Si tips 100 nm design plus ~100 nm SEM, 500 nm Si waveguide, 220 nm, 2 um BOX, 3.5 um upper
  cladding).
- `cmp_lit_fang2016_si_wire_500nm` (waveguide_platform.straight, soi_strip, 5): ~2.5 dB/cm TE, ~2.9 dB/cm TM over
  1520-1620 nm (cutback).
- `cmp_lit_fang2016_bend_r10` (waveguide_platform.bend, soi_strip, 4): ~0.01 dB per 180-deg bend, R 10 um, TE and TM
  (insertion_loss_db per_component, cherchi2013 precedent).

Not entered: "coupling dependent loss less than 1 dB" (term undefined: TE-TM difference or spectral variation, D156);
4 % simulated SiO2-taper loss (in notes); SiO2 taper lengths 110 / 85 / 70 um, beam size, section lengths (in
core_material; overlay tapers not entered as taper_length_um, fang2010 precedent); Si taper heights 80 / 140 nm (in
core_material); values of refs. [12]-[16] (cited, incl. the authors' own 2010 / 2011 converters).

Fab: empty. "we optimized and fabricated" (p.1) with authors at Kunming University of Science and Technology, Jilin
University and IME A*STAR, and no fabricating org named (D154). The passive sentence "fabricated on a SOI wafer with
an 8-inch diameter" names no org.

## Missing fab / facility orgs

None needed: org_astar_ime, org_stanford_university, org_stanford_nanofabrication_facility,
org_stanford_nano_shared_facilities exist. (org_stmicroelectronics exists but is not used; see judgment call 1.)

## Judgment calls for the auditor

1. buf2015 fab empty despite first-person process description; an auditor may argue for org_stmicroelectronics
   (11 of 14 authors, "packaging being used within STMicroelectronics", p.4) - left empty per D154 / D80b.
2. buf2015 basis split: Table I / Fig. 6 statistics and the SPGC values the text says were "measured in epoxy / in
   air" are `measured`; the 1490 nm SMW 1.4 dB/cm and PSGC 3.1 dB "typical" values with no data shown are
   `author_estimate` (D544). Text PSGC 3.25 dB at 1310 nm kept only in notes (Table I 3.2 dB entered).
3. buf2015 GC scope per_coupler with method unspecified (D425 precedent); bend values per bend with the angle unstated.
4. sapra2019: 17 design rows from Figs. 3 / 4 (one per etch fraction x target bandwidth). Values are vector reads, so
   basis `simulated` with the reading in notes (D454). Measured 3-dB widths of the 40 / 100 nm devices are
   peak-referenced figure reads, not the paper's centre-referenced definition (not printed).
5. sapra2019 ref23_a25 ties the text comparison design (-2.29 dB, 64 nm 1-dB width) to the Fig. 9 25 deg marker
   (reads -2.30 dB); the incidence angle of the text design is not printed.
6. fang2016 platform `soi` for the cantilevered SiO2 converter follows the merged fang2010 rows of the same group; D82f
   (platform = fiber-facing facet layer) would give `silica`.
7. fang2016 bw_1db_nm "> 100 nm" author_estimate (measured span is exactly 100 nm, D459 analogue); without-liquid
   losses carry the inferred 1520-1620 nm band.
8. shi2014 back reflection "> 20 dB" `derived` (authors infer it from the 0.06 dB ripple), O band inferred.

## Registry gaps

- Per-length phase-shifter efficiency and loss for Si PN modulators: buf2015 HSPM 17.2 deg/mm (std 0.4) and
  10.5 deg/mm at 2.5 V, VpiLpi 2.5 V cm, 6 / 4 dB/cm (p.4 Sec. IV, Table I). Proposed `phase_efficiency_deg_per_mm`
  (phase shift per length at the stated drive) and `loss_db_per_cm` on phase_shifter; or route to the EO atlas if Si
  plasma-dispersion modulators are in its scope (D250 rejected per-length phase-shifter loss earlier).
- `min_feature_nm` (process / design minimum feature): shi2014 200 nm (p.2), sapra2019 100 nm (p.2), buf2015 80 nm
  sigma 1.9 nm (p.3). Proposed definition: smallest drawn / printed feature allowed by the stated process or design rule.
- `tol_1db_vertical_um` (D441 candidate): fang2016 +/-2.0 um vertical, stored in tol_1db_lateral_um with the axis in
  condition.
- GC mode-mismatch loss: shi2014 simulated 0.5 dB (p.3); candidate `mode_mismatch_loss_db` (simulated overlap loss of a
  coupler), low priority.
