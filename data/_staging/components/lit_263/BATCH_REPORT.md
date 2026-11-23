# lit_263 batch report

Papers: lit:su2018 (Optics Express 2018), lit:mak2018 (Optics Express 2018), lit:roelkens2006 (Optics Express 2006),
lit:antelius2011 (Optics Express 2011), lit:zhou2022d (IEEE Photonics J. 2022). Page-1 titles match the source rows; no
garbled text layers; no correction / erratum. verified_on 2026-11-23. Dry run: +16 components, +139 metrics, 0 errors
(the only warning is the pre-existing ni2025b duplicate, not in this batch). No existing rows for these sources.
Values are only what each paper reports itself; comparison tables and sentences quoting other works (su2018 refs. [3],
[10], [37]; mak2018 Table 3; roelkens2006 ref. [6]; antelius2011 Table 1 rows of other works) are not entered.

## Components / metric rows

| paper | component | class | kind | metrics |
|---|---|---|---|---|
| su2018 | cmp_lit_su2018_conv_gc_10deg | fiber_chip_coupler.grating | design | 7 (IL 1.94 dB, 1-dB 34 nm, 10 deg, 220 nm / 100 nm etch / 2 um BOX / 14 um) |
| su2018 | cmp_lit_su2018_twolayer_gc_normal | fiber_chip_coupler.grating | design | 5 (IL 0.25 dB, 1-dB 22 nm, 0 deg, 220 nm, 12 um) |
| su2018 | cmp_lit_su2018_blazed_gc_normal | fiber_chip_coupler.grating | design | 5 (IL 0.17 dB, 1-dB 26 nm, 0 deg, 220 nm, 14 um) |
| su2018 | cmp_lit_su2018_polinsens_gc_normal | fiber_chip_coupler.grating | design | 8 (IL TE 2.9 / TM 3.6 dB, 1-dB 28 nm both, 0 deg, 220 / 100 nm etch / 2 um BOX / 14 um) |
| su2018 | cmp_lit_su2018_demux_gc_1310_1490 | fiber_chip_coupler.grating | design | 9 (IL 1.5 dB at 1310 / 1.6 dB at 1490 nm, crosstalk > 21 dB, 1-dB 20 / 24 nm, 0 deg, 340 / 180 nm etch, 12 um) |
| su2018 | cmp_lit_su2018_passthrough_demux_gc | fiber_chip_coupler.grating | design | 8 (IL 1.0 dB at 1310 nm, pass-through 0.08 dB at 1490 nm, 1-dB 28 nm, 0 deg, 260 / 140 nm etch / 2 um BOX / 12 um) |
| mak2018 | cmp_lit_mak2018_focusing_bilayer_gc | fiber_chip_coupler.grating | fabricated | 34 (3D-FDTD IL 1.5 dB at 1312 nm and 1-dB 73 nm; Table 2 per-chip IL and 1-dB width for 9 chips; eta 61 % on the 206 nm chip; medians IL 2.1 dB / 1-dB 70.9 nm / center 1331.7 nm; MFD 9.2 um; 840 nm output; SiN 600 / Si 300 / etch 150 nm design and 605 / 300 / 153 nm measured medians; 2 um BOX; 1 um clad) |
| mak2018 | cmp_lit_mak2018_focusing_bilayer_gc_si_minus40 | fiber_chip_coupler.grating | fabricated | 2 (peak 3.1 dB, 1-dB 69 nm) |
| mak2018 | cmp_lit_mak2018_uniform_1d_bilayer_gc | fiber_chip_coupler.grating | design | 5 (eta 73 % / 1.37 dB at 1316 nm, 28 deg, period 1467 nm derived, MFD 9.2 um) |
| roelkens2006 | cmp_lit_roelkens2006_polysi_uniform_gc | fiber_chip_coupler.grating | design | 8 (CE 66 % at 1550 nm, 10 deg, 610 nm period, 0.5 fill, 220 / 150 poly / 220 etch, 2 um BOX) |
| roelkens2006 | cmp_lit_roelkens2006_polysi_apod_gc | fiber_chip_coupler.grating | design | 9 (CE 78 % at 1550 nm, 3-dB 85 nm, 1-dB fiber tolerance +/-1.5 um, 20 periods, 10 deg, stack) |
| antelius2011 | cmp_lit_antelius2011_apod_gc_box2um | fiber_chip_coupler.grating | fabricated | 14 (measured CE 35 % at 1536 nm, 1-dB 47 / 3-dB 83 nm; simulated 33 %, 33 / 58 nm; 20 cells; 10 deg; 220 nm through-etch; 2 um BOX; 14.3 x 12 um; 165 um taper) |
| antelius2011 | cmp_lit_antelius2011_apod_gc_box2p2um | fiber_chip_coupler.grating | design | 8 (CE 72 %, 1-dB 38 / 3-dB 64 nm, back-reflection 30 dB from 0.1 %, 2.2 um BOX) |
| antelius2011 | cmp_lit_antelius2011_periodic_gc_box2p2um | fiber_chip_coupler.grating | design | 7 (CE 51 %, back-reflection 6.78 dB from 21 %, 690 nm / 0.8) |
| antelius2011 | cmp_lit_antelius2011_periodic_gc_box2um | fiber_chip_coupler.grating | design | 7 (CE 22 %, back-reflection 6.99 dB from 0.2, 690 nm / 0.8; Fig. 3 point labels) |
| antelius2011 | cmp_lit_antelius2011_si_wire_500nm | waveguide_platform.straight | fabricated | 3 (82 dB/cm from -8.2 dB/mm cutback, 500 nm, 220 nm) |
| zhou2022d | none | - | - | 0 |

Per paper: su2018 6 / 42, mak2018 3 / 41, roelkens2006 2 / 17, antelius2011 5 / 39, zhou2022d 0 / 0.

## Values not entered and why

su2018
- Fig. 1 statistical study (100 optimization runs per discretization method, 340 nm waveguide, normal incidence,
  50 / 100 nm feature sizes): efficiency distributions only, no single component.
- Fig. 4(a) fully continuous permittivity design (> 99 % coupling efficiency): not a fabricable structure.
- Fiber Gaussian waist not printed (symbol only). Blaze angle 50 deg from the normal kept in notes (no conversion to a
  sidewall angle). Two-layer design (Fig. 3): the 100 nm label marks the upper patterned layer, not entered as an
  etch depth (role ambiguous); no BOX drawn.
- Comparisons: 2.12 dB (ref. [3]), 0.165 dB (ref. [10]), 4.3 / 3.2 dB (ref. [37]) are cited values.

mak2018
- Interlayer SiO2 spacing (target 200 nm; wafer median 229 nm, range 140 nm, std 37.4 nm; per chip 193-333 nm):
  `gap_nm` is not allowed on fiber_chip_coupler; values kept in notes and per-chip conditions (registry gap below).
- Table 2 per-chip eta and EBWP: eta entered only for the 206 nm chip (abstract device); the other chips' eta are the
  linear form of the printed IL; EBWP (figure of merit) has no parameter.
- Table 1 coarse-sampling designs (5 sampled parameter sets, eta 0.21-0.26): design-search intermediates, not entered.
- Simulated sensitivity (within 1 dB for +/-60 nm offset / spacing, center shift up to 50 nm) and measured corner
  deltas (x-offset at most 0.5 dB, SiN teeth -40 nm 0.5 dB lower peak): relative changes, notes only.
- "additional loss of approximately 0.7 dB compared to the simulation": a difference, not entered.
- Fiber array polish angle 29 deg (Table 3 emission angle 29 deg): measurement setup, kept in the condition; design
  angle 28 deg on the 1D design row only (the focusing design's angle is not printed separately).
- Si tooth widths 304 nm and other p(1)* dimensions: no registry parameter for bi-layer tooth widths / offsets (notes).

roelkens2006
- Directionality 85 % (overlay GC) and 55 % (standard 220 nm GC without overlay, no coupling efficiency printed): no
  directionality parameter; the standard GC therefore has no row.
- Table 1 tooth / slit widths: referenced in notes only. Tolerance figures (Figs. 7-8): no single values.
- Fiber assumptions (9 um core, index contrast 0.005, 4.5 um waist) are simulation inputs (condition).

antelius2011
- Measured Fabry-Perot ripple < 0.5 dB: no ripple parameter.
- Fig. 5(b) simulated spectrum of the as-fabricated dimensions and the +/-5 % fill-factor curves: no printed values.
- Table 2 gap / bar widths per cell (minimum 120 nm): notes only.

zhou2022d (no component rows)
- A fiber-optic optoelectronic oscillator built from discrete commercial parts (tunable laser, iXblue DPMZM, 1 km SMF,
  50 GHz PD, electrical amplifier, BPF). The only optical-component values are setup / datasheet specifications of
  purchased equipment (DPMZM 40 GHz and 5.5 V half-wave voltage, PD 0.55 A/W, BPF 45 MHz), which are measurement
  setup (skill rule 13) and modulator metrics (EO atlas, rule 2). System results (phase noise -93 dBc/Hz, pulse widths
  620-2970 ns, repetition rates 185.1 / 370.2 / 555.3 kHz) are not component metrics. Nothing in scope.

## Fab / facility orgs

- mak2018: fab `org_cea_leti` ("fabricated on a 200 mm silicon-on-insulator wafer ... as part of a trial for a SiN-on-Si
  platform that was under development at CEA-LETI", p.7 Sec. 3). `process_name` composed from the printed wording
  (platform under development, 200 mm SOI, 193 nm / 248 nm DUV). No facility.
- antelius2011: fab `org_kth_royal_institute_of_technology` (first-person "We present the design, fabrication, and
  characterization", p.1 abstract and p.7 conclusion; all three authors at KTH Microsystem Technology Laboratory;
  D697 precedent wang1998). Acknowledgment thanks a KTH group member for help with measurements: not a facility.
- su2018, roelkens2006: design only, no fab. zhou2022d: no rows.
- Missing orgs: none.

## Judgment calls for the auditor

1. su2018 and roelkens2006 rows are `row_kind: design`, all performance `simulated` (2D FDFD / 2D eigenmode).
   "Minimum insertion loss" of each su2018 spectrum entered at the 1550 nm design wavelength with
   `wavelength_inferred` (peak wavelength not printed); su2018 Fig. 6 / 7 values carry their stated 1310 / 1490 nm.
2. su2018 pass-through 0.08 dB at 1490 nm entered as `insertion_loss_db` scope `per_coupler` with the condition saying
   it is transmission through the grating to a detector behind the chip, not fiber-to-waveguide coupling.
3. su2018 platform `soi` for the 340 nm (Fig. 6, "infinite BOX" stated) and 260 nm (Fig. 7, drawn Si / 2 um SiO2 / Si
   stack, SOI not named) designs; thicknesses and partial-etch depths read from labelled figure dimensions
   (`extracted_from_figure`); polarization `te` on Fig. 7 rows from the TE field-plot captions, empty for Figs. 2-4, 6.
4. mak2018 per-GC IL scope `loopback_half`, method `loopback`, basis `measured` (GC-pair test structures, per-GC value
   printed, de-embedding not described; D167 / D452 / D622). Table 2 entered per chip (9 x IL + 1-dB width, the chip's
   interlayer spacing in the condition, wavelength_nm = printed center wavelength) plus medians; Table 2 median width
   70.9 nm kept against 70.8 nm in the abstract / text (noted).
5. mak2018 bi-layer stack: `core_thickness_nm` = SiN 600 nm (output-waveguide layer), `layer2_thickness_nm` = Si 300 nm,
   `etch_depth_nm` 150 nm on Si; design targets and ellipsometry medians as separate rows. 3D-FDTD focusing values on the
   fabricated row (D80e); the 2D 1D-uniform design (eta 0.73) on its own design row with period 1467 nm `derived` (t + g).
6. mak2018 Si-teeth -40 nm corner as a sibling fabricated row (peak 3.1 dB, band O inferred, 69 nm).
7. antelius2011 measured 35 % per grating: scope `loopback_half`, method `cutback`, basis `measured` (linear fit of own
   data, halving described but no total printed). Waveguide 8.2 dB/mm -> 82 dB/cm `derived`, C band inferred.
8. antelius2011 periodic starting designs: 2.2 um BOX CE 51 % from the text (Fig. 3(c) point label 0.53, conflict in
   notes); 2 um BOX values only from Fig. 3 point labels (0.22 / 0.2), basis `simulated`. Back-reflection % -> dB kept
   `simulated` (D83f). Fill factor 0.8 kept as printed (definition not stated, D253).
9. antelius2011 fab KTH from "We present the design, fabrication, and characterization" (D697 analogue); drop to
   empty if that wording is judged too weak under D80b.
10. roelkens2006 `tol_1db_lateral_um` 1.5 um for fiber displacement along the waveguide propagation direction
    (in-plane, condition says so).

## Registry gaps

- `gap_nm` (or an `interlayer_spacing_nm`) on fiber_chip_coupler: mak2018 bi-layer SiO2 interlayer spacing 200 nm
  target, wafer median 229 nm, per-chip 193-333 nm (p.3 Fig. 1(a), p.7, p.8 Table 2). Proposed definition: vertical
  spacing between the two guiding layers of a bi-layer / multilayer grating coupler.
- `directionality_pct` on fiber_chip_coupler: roelkens2006 85 % (overlay, 20 periods) and 55 % (standard GC), p.4.
  Proposed definition: fraction of the guided power diffracted towards the fiber side (simulated, grating length in
  condition).
- `ripple_db` on fiber_chip_coupler: antelius2011 measured Fabry-Perot ripple < 0.5 dB (p.6).
