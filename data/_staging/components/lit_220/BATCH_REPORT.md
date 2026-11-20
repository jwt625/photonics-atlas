# lit_220 batch report

Distilled 2026-11-20 (verified_on 2026-11-20). Papers: lit:hoffman2019, lit:xu2008, lit:xiong2014, lit:wang2014b.
Page-1 titles match the source rows; no garbled text layer. Totals: 27 components, 168 metric rows. Dry-run
`merge_component_staging.py data/_staging/components/lit_220 --dry-run`: +27 / +168, 0 errors (the one warning is on an
existing ni2025b row, not this batch).

## lit:hoffman2019 (adjoint shape-optimized SOI crossing, Sandia) - 7 components / 25 metrics

- `lm_crossing_fab` (crossing.other, fabricated): measured best through power 0.06 dB per crossing (crossing-array
  series, method cutback), figure read <= 0.18 dB over 1500-1635 nm, measured cross power extinction ratio 50 dB peak at
  1600 nm and >= ~31 dB over the measured span (figure read), simulated 0 nm-bias peak ~71 dB at ~1.54 um (Fig. 9(b)
  read), core 250 nm design / ~230 nm after oxidation smoothing (author_estimate), 400 nm feed width, 10 um total width.
  Fab org_sandia_national_laboratories, process_name "Sandia CMOS-compatible silicon photonics process, 248 nm DUV
  photolithography" (p.11 sentence names the org and process).
- Design rows (row_kind design, simulated): LM FOM (1, -1) headline design (< 0.08 dB, > 60 dB over 1500-1600 nm), LM and
  GD FOM (1, -1.5) convergence designs (through-power asymptote 0.08 / 0.13 dB), Table 1 BFW 100 / 200 / 300 nm designs
  (worst-case 0.02 / 0.06 / 0.07 dB, 55 / 55 / 54 dB).
- Not entered: radiated and reflected power (Table 1, Fig. 5-6; no crossing parameter for reflection or radiation),
  relative GD-vs-LM statements (3 dB, 5 dB, 2 dB), Table 1 Ref. [8]/[39]/[41]/[42] columns (cited works), simulated
  through-power curves of the bias family, crossing-array crossing counts (not printed).
- Judgment calls: (1) platform `soi` (etch depth not stated; coplanar SiO2-buried). (2) The "cross power extinction
  ratio" (Pthrough / Pcross) is stored as `crosstalk_db`. (3) "total width of 10 um" stored as `length_um` (arm end to
  arm end of the 8-fold symmetric crossing). (4) Measured rows keep polarization empty (optimization is quasi-TE; the
  measurement polarization is not stated). (5) Sec. 4.3 design thickness 230 nm taken from "setup the same as 4.2".
- Missing orgs: none (Sandia in registry). No facility statement.

## lit:xu2008 (MMI-crossing microring cross-connect filters, HKUST) - 14 components / 83 metrics

- Crossings: 4 Table 1 designs (Wm 1.0 / 1.2 / 1.3 and the optimized 1.1 x 4.4 um; 2-D FDTD loss and crosstalk), a
  no-taper design (~0.3 dB, Lm ~4.7 um), three fabricated MMI crossings Lm 4.3 / 4.5 / 4.7 um (only simulated values:
  Fig. 2(d) points read off the plot), the fabricated plain control crossing (simulated 0.80 dB, ~23 dB crosstalk read
  off Fig. 2(c)).
- `rib_waveguide` (waveguide_platform.straight): ~20 dB/cm, author_estimate (origin not stated), C band inferred.
- Filters (wdm.mrr): MMI and plain single cross-connect filters (Q ~1e4 measured, FSR ~2.7 / ~2.6 nm and notch depth
  7-9 / 10-12 dB read off Fig. 3, corner radius ~25 um, Lc ~15 um, gap ~0.35 um, bus ~0.4 um), 4-channel 1x4 filter
  (Q ~1e4, 4 channels, radii 20-20.6 um, Lc 15 um), 2-channel 2x2 cross-grid filter (0.09 nm second-order D1 and 0.19
  nm first-order D3 bandwidths, radii 20 / 20.3 um, Lc 18 um).
- Fab org_the_hong_kong_university_of_science_and_technology on fabricated rows ("We design and fabricate", both
  authors HKUST). process_name empty: only "standard silicon CMOS microelectronics fabrication processes" + i-line
  lithography / RIE printed (generic wording; in notes).
- Not entered: 0.4 dB measured MMI crossing loss and 1.1 / 4.3 um dimensions of the earlier MMI crossing (ref. [16],
  cited), ~1 dB / -20 dB typical plain crossing (cited), Table 1 back-reflection (no crossing parameter), Fig. 1 filter
  simulation parameters (R 6.5 um, g 0.2 um, Wb 0.3 um; field plots only, no values), slab-mode baseline ~ -52 dB (not a
  component value), 4-channel resonance positions / spacing (order 2, 1, 3, 4; no printed spacing), drop-port levels
  (normalized to the lensed-fiber output, include facet coupling).
- Judgment calls: (1) 2x2 cross-grid values kept although the Fig. 5 caption cites the authors' own conference paper
  [26] after panel (a) (SEM) and the fabrication sentence cites [26-28]: the bandwidth sentence carries no citation
  (D408); auditor to confirm. (2) The unqualified "filtering bandwidth" stored as `bw_3db_nm` with "level not stated"
  (davis2020 precedent). (3) Single cross-connect filters classed `wdm.mrr` (channel drop in a cross-connect path,
  D400). (4) Fabricated crossings Lm 4.3 / 4.5 / 4.7 entered as rows with only the simulated Fig. 2(d) point (D80e);
  the Wm 1.1 / Lm 4.4 design is a separate design row (not fabricated at that Lm). (5) As-fabricated "~0.4 um" and
  "~0.35 um" stored in nm as `derived` (D157 unit rescale). (6) Q wavelength spans and the 2x2 bandwidth span inferred
  from the figure axes (`wavelength_inferred`).
- Missing orgs: none. No facility named (acknowledgment lists grants only).

## lit:xiong2014 (taper-etched DC PSR design, NRC / Carleton) - 3 components / 36 metrics

- Three design rows (polarization.psr, row_kind design, all simulated): He 70 / 110 / 150 nm with Wt 410 / 350 / 310 nm
  and chosen LDC 400 / 200 / 150 um. Per row: Table 1 conversion loss at saturation (0.38 / 0.26 / 0.32 dB), Table 3 TE
  IL (< 0.15 / 0.07 / 0.05 dB), PCL < 0.5 dB, XT_TE and XT_TM as `per_db` (1460-1625 nm); He 110 also the 3D-FDTD
  ~0.09 dB C-band conversion loss, the Fig. 5 TE IL < 0.07 dB over 1450-1650 nm and PCL < 0.3 dB over the C band.
  Geometry W 450 nm, Wt, H 220 nm, He, etch depth, LDC.
- Not entered: Table 2 fabrication tolerances and the tip-width statement (Dt ~80 nm, 0.2 dB penalty; no tolerance
  parameter, tip_width_nm not allowed for polarization), gap 200 nm and S-bend radius 50 um (parameters not allowed for
  polarization), Table 4 other-work columns (cited).
- Judgment calls: (1) He 70 nm XT_TM: text "below -20 dB" vs Table 3 "< -15 dB"; Table value entered with a conflict
  note (D417). (2) Platform `soi` (wire plus partially etched waveguide). (3) Table 1 conversion loss placed on the row
  with the later-chosen LDC, condition states the saturation LDC.
- Missing orgs: none (no fabrication).

## lit:wang2014b (rib-DC PSR design, SIMIT / Purdue) - 3 components / 24 metrics

- `rib_dc_psr_design` (polarization.psr, design): ~97 % conversion efficiency stored as 0.13 dB (simulated, D83f),
  cross / through ER 20 / 26.7 dB at 1550 nm, cross ER > 19 dB over 1500-1600 nm, through ER 6.3 dB at 1600 nm,
  tolerance ER > 12 dB (cross) and > 10 dB (through, gap), widths 262 / 500 nm, H 250 nm, slab 50 nm, ~24 um length.
- `cascaded_psr_design` (polarization.psr, design): through ER 15.7 dB at 1600 nm, widths 262 / 500 / 250 nm, Ltotal
  48 um (Fig. 5(b) inset label).
- `strip_rib_bilevel_taper_design` (waveguide_platform.other, design): T > 0.95 over 1500-1600 nm stored as < 0.22 dB,
  Ltp 10 um, Wside 300 nm (derived from 0.3 um), H 250 nm, slab 50 nm.
- Not entered: gap 150 nm, Gout 1 um, Lc / S-bend lengths as separate rows (gap_nm / coupling_length_um not allowed for
  polarization; Lc in notes), etch-depth and upper-cladding-index tolerance statements (no value / sign ambiguous).
- Judgment calls: (1) ER rows stored as `per_db` with polarization empty (the paper does not define which powers the
  cross / through ER compares). (2) Percent conversion / transmission converted to dB on simulated values (basis
  simulated, D83f). (3) Strip-rib taper as `waveguide_platform.other` (one Si layer; dai2012 precedent).
- Missing orgs: none (no fabrication).

## Registry gaps

- `gap_nm` for `polarization` (DC-based PSR coupling gap): xiong2014 Dgap 200 nm (p.3, Table 1), wang2014b G 150 nm
  (p.3, Fig. 3 caption). Proposed: widen `gap_nm` to polarization ("coupling gap of a DC-based PBS / PSR").
- `coupling_length_um` for `polarization`: wang2014b Lc 9 um (Fig. 3), cascaded Lc1 11 / Lc2 7 um (Fig. 5).
- `min_bend_radius_um` for `polarization`: xiong2014 S-bend radius 50 um (p.3).
- Back-reflection for crossings: xu2008 Table 1 (~ -18 / -45 / -30 / -30 dB) and hoffman2019 Table 1 Max(Preflected)
  (-44 / -35 / -42 dB), simulated. Proposed: widen `back_reflection_db` to `crossing`.
- Radiated power fraction of a crossing: hoffman2019 Table 1 Max(Pradiated) -24 / -19 / -18 dB (simulated). No
  proposal (single paper).
