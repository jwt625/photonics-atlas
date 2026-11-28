# lit_324 batch report

Distilled 2026-11-28. Papers: lit:zortman2010, lit:chen2012a, lit:cheben2007, lit:sherwooddroz2008, lit:miller2015.
Result: 14 component rows, 91 metric rows; `merge_component_staging.py --dry-run`: +14 components, +91 metrics,
0 errors (the 2 warnings name merged rows of other batches). Page-1 titles match the source rows; all five are Optica
publisher copies (Optics Express x4, Optica x1); none is another paper or an erratum. `garbled_text_layer` false for
all; figure values checked on the page renders. No modulator metrics in this batch (rule 2: zortman2010 W1 disks are
microdisk modulators, but no modulator metric is reported). No existing rows for these sources in `data/components/`.

## lit:zortman2010 (Optics Express 2010, Silicon photonics manufacturing)

Components: 1 (`resonator.disk`, platform `soi`, fab `org_sandia_national_laboratories`, `process_name`
"radiation hardened six inch SOI 0.35 um process, 248 nm lithography"). Metric rows: 17.
- `cmp_lit_zortman2010_microdisk_d6um`: 12 resonance-spread rows (`wavelength_spread_nm`, all `derived`): Table 1
  within-wafer std TE / TM for W1, W1 filtered, W2 (6); within-wafer range TE about 1 THz and TM nearly 2.5 THz
  (Fig. 1(b), 2); wafer-to-wafer |W1 - W2| TE 1.117 THz and TM 0.666 THz (2); within-die range 105 GHz
  (diameter-corrected) and about 70 GHz (diameter + thickness corrected) (Fig. 5(a), 2). Geometry 5: radius 3 um
  (from 6 um diameter, derived), gap 320 nm, Si 240 nm, BOX 3 um, oxide cladding 5000 A -> 0.5 um (derived).

Judgment calls:
- The paper prints every spread in GHz / THz. The registry has only `wavelength_spread_nm`, so each value is
  converted with d_lambda = c d_f / f^2 at the stated mean frequency (per-wafer Table 1 mean for per-wafer rows; the
  mean of the W1 / W2 means, 191.6 THz TE and 194.45 THz TM, for combined rows); printed value and frequency in each
  row's notes. Coordinator may prefer a frequency parameter (registry gap 1) and re-point these rows.
- One component row for W1 (metalized, doped, contacted) and W2 (silicon only) disks: same design, wafer as a metric
  condition. W0 (from ref. [13], the authors' earlier paper) is not entered (D259 / D408); Fig. 1(b) also plots W0,
  noted on the 1 THz / 2.5 THz range rows.
- Table 1 caption filters the first chip of W1; p.4 text says the outlier chip from the top of W2 was filtered.
  Table 1 followed, inconsistency noted; n_samples left empty on filtered rows.
- 105 GHz / 70 GHz within-die ranges are reconstituted from Eq. (1) dimensional extraction after residual analysis:
  `derived` (model-based on own data).
- Fab: "Sandia National Labs' radiation hardened six inch SOI 0.35um process" names the org with the process
  (Contract v7). No facility.

Values not entered and why:
- Table 2 mode-solver sensitivities (TE 140 / 52 GHz/nm, TM 330 / 36 GHz/nm for thickness / diameter): simulated, no
  parameter (registry gap 2).
- Extracted dimensional variations: within-die thickness +/-0.1 nm, diameter about +/-0.35 nm and +/-4 A after
  residual analysis; diameter variation over 10 nm across a wafer (p.6-7, p.10): no parameter (registry gap 3).
- Chip matching: two chips matched within 7 GHz, 42 % within 25 GHz (p.8): a matching statistic, not a spread of one
  population; left in notes.
- Trimming power 231 uW, 1.1 mW tuning, 1.371 mW total, 110 fJ/bit (p.9-10): computed from the cited heater
  efficiency 4.4 uW/GHz (ref. [10]) and an assumed 10 GHz/C (rule 3).
- Lensed-fiber on/off-chip loss about 20 dB (p.4): setup loss, coupler not described; measurement repeatability
  3 sigma +/-250 MHz: setup resolution.
- Medians and mean frequencies of Table 1: centre values, not entered.

## lit:chen2012a (Optics Express 2012, 8x8 broadband Si switch)

Components: 8. Metric rows: 31. Fab `org_astar_ime` on all fabricated rows: acknowledgment thanks two IME staff "for
fabrication" (p.9; D84b borderline, noted). `process_name` empty: "200-mm-diameter wafers with 220-nm-thick silicon
using CMOS compatible processes" names no node or flow (Contract v7).
- `cmp_lit_chen2012a_switch_8x8` (`switch_fabric.mzi_mesh`, soi, 13): fiber-to-fiber IL I1-O1 11.8 dB at 1500 nm and
  10.5 dB at 1580 nm (measured); on-chip loss about 4 dB (`de_embedded`, author_estimate: rests on the estimated
  3.5 dB/facet coupling; `statistic best` per the abstract "minimum on-chip loss"); IL non-uniformity over I1-O1..O8
  about 0.8 dB or less at 1515 / 1580 nm and up to 2.8 dB at 1500 / 1565 nm (4 rows); port-to-port isolation > 30 dB
  over 1500-1580 nm and > 45 dB over the central 30 nm (`crosstalk_db`; 1525-1555 nm inferred as the centre of the
  span, flagged); total power < 70 mW upper bound (author_estimate, 0.07 W); footprint 8 x 8 mm (derived); 8 inputs /
  8 outputs.
- `cmp_lit_chen2012a_switch_cell_1x2` (`switch_fabric.mzi_mesh`, soi_rib, 7): ER > 16 dB over 1500-1580 nm, max
  > 30 dB (best, wavelength not stated), about 20 dB at 1540 nm (Fig. 6(a)); P_pi < 1.5 mW at 1540 nm; rise and fall
  about 250 us (20-80 %, noted); loss-breakdown unit loss 0.33 dB (author_estimate, origin not stated).
- `cmp_lit_chen2012a_to_phase_shifter` (`phase_shifter.thermo_optic`, soi_rib, 1): TiN heater resistance about
  1 kOhm (author_estimate: measured or design not stated). Cross-row to the cell (D396).
- `cmp_lit_chen2012a_crossing_ridge_w6um` (`crossing.other`, soi_rib, 3): 3D FDTD crossing loss about 0.015 dB at
  1550 nm and crosstalk below -40 dB (simulated), W = 6 um (derived). Fabricated row (D80e).
- `cmp_lit_chen2012a_crossing_wire_500x220_design` (`crossing.other`, `design`, soi_strip, 2): comparison crossing
  of 500 x 220 nm fully etched guides, 1.2 dB (author_estimate: calculated or measured not stated; 1550 nm inferred
  from the preceding FDTD sentence), width 500 nm.
- `cmp_lit_chen2012a_ridge_rib_transition` (`waveguide_platform.other`, soi, 1): 0.25 dB per transition
  (author_estimate, loss-breakdown table).
- `cmp_lit_chen2012a_waveguides` (`waveguide_platform.straight`, soi, 1): 0.6 dB/cm (author_estimate, scope
  unspecified, loss-breakdown table).
- `cmp_lit_chen2012a_cantilever_edge_coupler` (`fiber_chip_coupler.edge`, silica per D82f, 3): about 3.5 dB/facet
  (author_estimate, "We estimate ... roughly"), SiO2 cantilever 6 x 6 um.

Judgment calls:
- 1x2 cell as `switch_fabric.mzi_mesh` (D158: a cell characterized inside a mesh; ding2017 / ribeiro2016 precedent);
  P_pi and switching times on the cell row, heater resistance on a separate phase-shifter row (D396).
- Port-to-port isolation entered as `crosstalk_db` (switch_fabric has no isolation parameter).
- "about 0.8 dB or less" -> `le` 0.8; "up to 2.8 dB" -> `le` 2.8; one row per stated wavelength.
- Loss-breakdown unit losses (Fig. 4(b) "Estimated loss breakdown") are author_estimate, origin not stated.
- Wavelength not stated for the on-chip loss, coupling loss and breakdown terms: `band unspecified` (measured span
  1500-1580 nm crosses S / C / L, no single band to infer).

Values not entered and why:
- 1.3 dB variation of the I1-O1 fiber-to-fiber loss over 80 nm (p.6): `wdl_db` not allowed for switch_fabric
  (registry gap 5).
- Loss-breakdown total 11.0 dB (Fig. 4(b)): wavelength not stated; the measured 11.8 / 10.5 dB endpoints are entered.
- Thermal crosstalk: neighbouring heater changes transmission up to 0.35 dB at 8 mW, 0.1 dB (0.1 pi) at 1.5 mW
  (p.8, Fig. 7): no parameter (registry gap 4); in the phase-shifter notes.
- "maximum switching speed close to 2 kHz": inferred from rise / fall time, not a measured bandwidth.
- Table 1 architecture losses (0.25 dB per MZI assumed), 1.5 dB/facet projection, 500 x 220 nm comparison only as
  above; measured 0.8 dB spread "consistent with" 0.015 dB/crossing: no per-crossing value derived.

## lit:cheben2007 (Optics Express 2007, SOI AWG microspectrometer)

Components: 1 (`wdm.awg`, soi_rib, fab empty). Metric rows: 22.
- `cmp_lit_cheben2007_awg_50ch_0p2nm`: measured (TM) channel spacing 0.2 nm, 3-dB channel bandwidth 0.15 nm,
  crosstalk 10 dB or better (`crosstalk_db` ge, type not stated), IL 17 dB at 1545 nm (`device_total`, includes the
  fiber input coupling, objective output), channel roll-off 5 dB over one FSR, FSR about 10 nm (derived from 20 nm /
  2 FSRs; design statement p.4). Geometry 16: 50 channels, 125 arms, order 160, FPR 166 um, slit width 600 nm, ridge
  width 1500 nm, wa 1200 nm, receiver pitch 1 um, array pitch 1.6 um, taper 100 um, Si 1500 nm, BOX 1 um, cladding
  1 um, etch 870 nm (profilometry, measured) and 900 nm nominal, footprint 8 x 8 mm2.

Judgment calls:
- IL wavelength: abstract prints 1.545 um, p.7 text prints 1.45 um; 1545 nm entered with the discrepancy in notes.
- Measured spectral values without a printed wavelength: `c_band` inferred from the Fig. 4 axis (about 1537-1553 nm).
- Fab empty: passive "Devices were fabricated on SOI wafers from Soitec" with no fabricating org named (all authors
  at NRC IMS; D80b, Contract v7). Soitec as wafer supplier in notes only.

Values not entered and why:
- Ridge-to-slit two-level mode transformer loss better than -0.4 dB: reported in refs. [25, 31] (authors' own
  earlier and forthcoming work, p.5) and restated on p.7; not entered (rule 3, D259 / D408); no separate component
  row since it has no other value.
- Theoretical resolving power 20,000 / 0.08 nm Rayleigh limit, ~0.1 nm resolvable separation (estimate), design
  crosstalk 25 dB and loss penalty 1.5 dB (design choices), Rowland radius 83 um (FPR length entered instead).
- Sibling spectrometer without the deep etch (Fig. 3 B / C): only "resolution better by more than a factor of three"
  for the deep-etched device; no number for the sibling, no row. TE loss / crosstalk "significantly worse": no value.

## lit:sherwooddroz2008 (Optics Express 2008, 4x4 hitless Si router)

Components: 4 (fab empty). Metric rows: 21.
- `cmp_lit_sherwooddroz2008_router_4x4` (`switch_fabric.other`, soi, 4): max routing extinction 20.79 dB at
  1553.67 nm (best over tested paths), footprint 0.07 mm2 (derived), 4 x 4 ports.
- `cmp_lit_sherwooddroz2008_ring_switch_element` (`switch_fabric.other`, soi, 2): switching extinction 17 dB at
  < 2 mW and > 21 dB at 6.5 mW (C band inferred from the Fig. 6 axis).
- `cmp_lit_sherwooddroz2008_ring_r10um` (`resonator.ring`, soi, 13): FSR 8.8 nm, FWHM 0.31 nm, linewidth about
  38.5 GHz (`linewidth_mhz` 38500, derived), tuning about 0.25 nm/mW (250 pm/mW, derived), tuning range 10 nm;
  geometry radius 10 um, gap 200 nm, width 450 nm, Si 250 nm, BOX 3 um, cladding 1 um, heater 1 um wide, NiCr 300 nm.
- `cmp_lit_sherwooddroz2008_crossing` (`crossing.other`, soi, 2): simulated IL 0.18 dB and crosstalk better than
  -20 dB (fabricated row, D80e).

Judgment calls:
- Ring switch element `switch_fabric.other` (D407) plus the ring itself as `resonator.ring` (D396; dasmahapatra2014
  precedent); the 17 / 21 dB on/off extinction on the element row, the spectral / tuning values on the ring row.
- Platform `soi`: etch depth of the 450 x 250 nm waveguides not stated (D422).
- Fab empty: first-person fabrication ("We start with commercial SOI wafers ... we pattern", p.6) by authors at two
  universities (Cornell, Columbia): fabricating org ambiguous (D80b / D154). No acknowledgment section.

Values not entered and why:
- "We have made and tested similar crossings with -0.51 dB insertion loss" (p.7): design identity of the tested
  crossings not given (D159), in crossing notes.
- Simulated heater design values (metal absorption about 2.17e-4 /cm, > 56 % of heater temperature reaching the
  waveguide, ~5 um lateral spread): no parameter / unit sign ambiguous; heater-to-waveguide distance 1 um:
  `heater_gap_um` allowed only for phase_shifter (registry gap 6).
- TO ~20 nm and EO ~2 nm shift magnitudes (p.4): cited (refs. [16, 17]).
- Router insertion loss and route crosstalk: not reported (deferred to packaged work, p.8).

## lit:miller2015 (Optica 2015, Perfect optics with imperfect components)

Components: 0. Metric rows: 0. Theory letter: a self-configuring algorithm and a double-MZI (DMZI) block that
tolerates fabricated beam-splitter ratios from 85:15 to 15:85 (analytic bound |delta R| <= 1/sqrt(8), p.3-4). No
fabricated or simulated device, no platform, no wavelength and no component performance value; the tolerance range is
a property of the proposed architecture, not a split ratio of a component (`split_ratio_pct` would misstate it). Not
entered (rule 9: no performance metric). Supplement 1 is not in the cached file.

## Missing fab / facility orgs

None. Sandia National Laboratories (`org_sandia_national_laboratories`) and A*STAR IME (`org_astar_ime`) are in the
registry. No facility acknowledgments in any of the five papers.

## Registry gaps (skipped value + locator + proposed definition)

1. `frequency_spread_ghz` (resonator, wdm, laser; GHz): spread of resonance / channel frequency across devices, dies or
   wafers (+/- value, std or range as stated, kind in condition). zortman2010 Table 1 TE std 556 / 357 / 430 GHz,
   TM std 1194 / 749 / 957 GHz (p.5), TE range ~1 THz, TM ~2.5 THz (p.4), within-die 105 GHz / ~70 GHz (p.8). Entered
   for now as converted `wavelength_spread_nm` (derived).
2. `resonance_sensitivity_ghz_per_nm` (resonator; GHz/nm): resonance frequency shift per nm of a stated dimension
   (dimension in condition). zortman2010 Table 2 (p.5): TE 140 (thickness) / 52 (diameter), TM 330 / 36 GHz/nm,
   simulated.
3. `dimension_variation_nm` (resonator, waveguide_platform; nm): extracted variation of a stated dimension (thickness,
   diameter, width) across a die / wafer (+/- value, scope in condition). zortman2010 within-die thickness +/-0.1 nm,
   diameter about +/-0.35 nm, +/-0.4 nm after residual analysis (p.6-7, Fig. 4).
4. `thermal_crosstalk_pi_per_mw` or a transmission-change form (phase_shifter, switch_fabric): phase (or dB) change
   induced in a neighbouring element per heater power. chen2012a: 0.1 pi (0.1 dB) at 1.5 mW, up to 0.35 dB at 8 mW
   (p.8, Fig. 7).
5. `wdl_db` for switch_fabric: chen2012a I1-O1 fiber-to-fiber loss varies 1.3 dB over 1500-1580 nm (p.6, Fig. 4(a)).
6. `heater_gap_um` for resonator (heater above a ring): sherwooddroz2008 heater 1 um above the waveguide (p.5).
