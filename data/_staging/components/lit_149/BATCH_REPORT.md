---
batch: lit_149
date: 2026-11-15
papers: lit:shang2023, lit:lin2021a, lit:chen2022d, lit:kim2014, lit:wu2020b, lit:li2013
totals: 17 components, 125 metric rows
validation: merge_component_staging.py --dry-run, 0 errors (1 unrelated warning on cmp_lit_ni2025b)
---

# lit_149 batch report

Page-1 check: all six cached texts are their source rows' papers (titles match). shang2023 is the arXiv preprint
(2212.09302) of the ACS Photonics paper, same title and authors (D430 / D433). No `garbled_text_layer`. No paper had
component rows before this batch. Only each paper's own results are entered; the comparison tables of other works
(kim2014 Table 1, li2013 Table I, wu2020b Table 1 other rows) are not (rule 3).

## lit:shang2023 (4 components, 33 metric rows)

| component | class | metrics |
|---|---|---|
| te0_te1_mode_mux | mode_converter.mdm_mux | 11 (single-device IL ~1.5 dB derived from the pair, pair crosstalk bound > 15.8 dB, 18.8 dB equal-crosstalk estimate, simulated IL < 0.9 dB / crosstalk > 17 dB, footprint 144 um2, input width, LN stack) |
| crossing | crossing.other | 10 (0.48 dB per crossing cutback, crosstalk 36 / 39 dB ports 3 / 4, simulated 0.22 dB / > 40 dB, footprint, LN stack) |
| compact_bend | waveguide_platform.bend | 10 (0.41 dB measured, 0.29 dB simulated, R 6 um, width, footprint, LN stack, as-fabricated etch ~230 nm) |
| circular_bend_r6 | waveguide_platform.bend (design) | 2 (simulated 3.7 dB, R 6 um) |

Not entered and why:
- Pair values (average IL < 3 dB 1520-1600 nm, two-pair totals 6.18 / 6.21 dB, simulated pair IL < 2 dB / crosstalk
  < -16.5 dB): totals of two or four devices; component notes. The single-device 1.5 dB is the authors' halving (derived).
- 2 um gap between the MUX output arms: `gap_nm` not allowed for mode_converter (notes). Minimum feature sizes
  0.2 / 0.5 / 0.4 um: no parameter (notes).
- "0.29 dB equals a 30 um circular bend" (p.7): implicit simulated value of another bend; note only.

Judgment calls:
- Crossing crosstalk 36 / 39 dB entered as printed without statistic: the p.3 wording is "< -36 dB", but the Fig. 3(d)
  S31 trace reaches about -30 dB, so the values read as averages; conflict in notes (D417).
- MUX single-device crosstalk: the measured pair value (> 15.8 dB, `measured`) is the paper's stated upper bound for
  one device; the 18.8 dB value assumes |c1| = |c2| (`author_estimate`).
- Stack rows (400 nm film, 250 nm etch, 150 nm slab, 45 deg sidewall) entered on each fabricated row (D153); the bend
  row also carries the ~230 nm under-etched rib as `author_estimate` (origin not stated).
- The 3.7 dB circular bend has no wavelength with the value: `band unspecified` + note.

Fab / facility: fab empty (passive fabrication from commercial NANOLN film, no org named, D80b); NANOLN as supplier in
notes. No facility acknowledged. No missing orgs.

## lit:lin2021a (2 components, 10 metric rows)

| component | class | metrics |
|---|---|---|
| pbs_cascaded_mzi | polarization.pbs (design) | 5 (ER > 20 dB 1390-1750 nm, IL < 0.5 dB 1390-1700 nm, IL < 1 dB 1390-1740 nm, both polarizations; 220 nm core, 550 nm width) |
| pbs_no_filter | polarization.pbs (design) | 5 (intermediate design without filters: TE IL < 0.25 dB, TE ER > 20 dB, TM IL < 0.5 dB; wavelength edges read off Fig. 4; core, width) |

Simulation-only paper (Lumerical FDTD / MODE + transfer matrix); both rows `row_kind design`, basis `simulated`.

Not entered and why:
- SWG period 210 nm, SWG gap 80 nm, N1 = 2, filter SWG periods 400 / 400 nm, N2 = 5: `subwavelength_period_nm`,
  `gap_nm`, `n_periods` not allowed for polarization (registry gap below); in component notes with all Table 1 / 2 values.
- Euler-bend filter TE1 crosstalk < -30 dB (Fig. 5(c)): sub-element of the PBS; `crosstalk_db` not allowed for
  polarization or waveguide_platform; note.
- Tolerance study (bandwidth over 250 / 210 nm for +/-5 / +/-10 nm width error, Fig. 7-8): no parameter; note.
- Point-symmetric design TM ER: below 20 dB in some bands (Fig. 4(b)), no stated value.

Judgment calls: pbs_no_filter edges for TE ER (1350-1630 nm) and TM IL (1370-1720 nm) are figure reads of a simulated
curve (`simulated`, D454) matching the printed 280 / 350 nm bandwidths.

Fab / facility: none (design only).

## lit:chen2022d (2 components, 14 metric rows)

| component | class | metrics |
|---|---|---|
| tfln_crossing | crossing.other | 5 (0.09 dB per crossing from 8 cascaded, derived; crosstalk > 31 dB measured; 36 dB simulated; w1 720 nm; 400 nm film) |
| tfln_waveguide | waveguide_platform.straight | 9 (simulated 0.04 dB/cm and group index 2.20; width 1.5 um, film 400 nm, ridge 200 nm, slab 200 nm derived, BOX 3 um, cladding 0.9 um, bend radius 150 um) |

Not entered and why:
- Modulator metrics (Vpi 0.67 / 0.70 V, VpiL, EO bandwidth 42 / 45 GHz, on-chip IL 5.8 dB, static ER > 25 dB, RF loss,
  energy per bit): EO-atlas data (rule 2). The paper (OE 30(14) 25308, folded CLTW TFLN MZM on Si) is not in
  ../eo-modulator-atlas (its `chen2022` is a different paper, APL Photonics 7, 026103): EO-atlas candidate.
- Measured TFLN waveguide loss 0.15 dB/cm (ring): credited to ref. [15] (rule 3).
- GC loss: not stated. 14 dB total minus 5.8 dB on-chip would imply about 8.2 dB for two GCs, not entered (the
  paper does not say how the on-chip value was separated). MMI splitters: no values.
- Crossing w2 3.58 um, l1 10 um, l2 29.2 um: roles in the Fig. 1(d) drawing are not unambiguous; notes.

Judgment calls: crossing loss `derived` (0.72 / 8 printed by the authors), method unspecified (reference not stated);
simulated values wavelength not stated, C band inferred from the 1540-1580 nm spectra and the EDFA link.

Fab / facility: fab empty (passive "fabricated on a commercial ... wafer (NanoLN)", process in ref. [15]; D80b).
No facility. No missing orgs.

## lit:kim2014 (5 components, 28 metric rows)

| component | class | metrics |
|---|---|---|
| te_te_mmi_crossing | crossing.mmi | 14 (0.29 dB per crossing cutback, crosstalk >= 38 dB C band, simulated 44 dB at 1550 nm / > 40 dB / best 50 dB / 0.24 dB at 1560 nm, MMI 1.3 x 6.2 um, port 1.0 um, taper 3 um, access 450 nm, stack) |
| tm_tm_mmi_crossing | crossing.mmi | 6 (crosstalk >= 48 dB C band, MMI 1.5 x 6.3 um, port 1.5 um, taper 3 um, core) |
| te_tm_mmi_crossing | crossing.mmi | 5 (0.31 dB TE / 0.26 dB TM per crossing, crosstalk >= 42 dB both, MMI length 6.0 um, core) |
| pol_diversity_crossing | crossing.other | 1 (crosstalk >= 30 dB both polarizations, C band) |
| ssc | fiber_chip_coupler.edge | 2 (coupling loss per I/O port 4.5 dB TE / 3.4 dB TM) |

Not entered and why:
- Crossing angles 110 / 105 deg: no parameter (notes). TM-TM loss: not stated. PBSs of the diversity circuit: no
  values. Simulated Fig. 2 / Fig. 3(a)-(b) / Fig. 3(d) / Fig. 4 curves: only the stated optima entered.
- Table 1 (other works): rule 3.

Judgment calls:
- Fab `org_national_institute_of_advanced_industrial_science_and_technology` (borderline): all authors at AIST,
  first-person "we used a simple reactive ion etching" / "We laid on a waveguide chip patterns" (p.5) plus staff thanks
  for device-fabrication assistance (p.8). Coordinator may empty it if the first-person etch sentence is judged
  insufficient (D80b / D84a).
- Text -44 dB at 110 deg (p.5) vs the Fig. 3(a) minimum near -48 dB: printed value kept, conflict noted (D417).
- Measured crosstalk "lower than -X dB, which occurs at ..." stored as `ge` (the worst case equals X).
- TE-TM per-crossing losses "estimated" with no method shown: `measured`, method unspecified (rule 4). SSC per-port
  coupling loss stated directly: `measured`, `per_facet` (D167), with lens input / lensed-fiber output in condition.
- Cutback and coupling-loss wavelengths not stated: C band inferred (`wavelength_inferred`).

Fab / facility: AIST (registry id exists). No facility. No missing orgs.

## lit:wu2020b (2 components, 25 metric rows)

| component | class | metrics |
|---|---|---|
| dual_mode_crossing | crossing.mmi | 22 (0.1 / 0.12 dB TE0 / TE1 at 1550 nm, < 0.81 / < 0.69 dB over 1525-1600 nm, cross-port crosstalk 49 / 47 dB at 1550 nm and > 30 dB over 1525-1600 nm, simulated 0.043 / 0.084 dB, < 0.87 / < 0.54 dB, > 56 dB, geometry of regions I-IV, 70 nm shallow etch, footprint 1135.69 um2 derived) |
| mode_mux_demux | mode_converter.mdm_mux | 3 (average excess loss 0.05 dB TE0 / 0.43 dB TE1, crosstalk > 24 dB at 1550 nm) |

Not entered and why:
- Bar-port crosstalk -25 / -32 dB (TE0 / TE1 links): attributed by the paper to the mode MUX / DEMUX, measured through
  the whole chain; note on the crossing row.
- GC losses: subtracted but not stated.

Judgment calls:
- "< 0.81 / 0.69 dB over the whole span" read as per crossing (Fig. 6: about -8 / -7 dB for ten crossings near
  1600 nm); `derived` (/10 after subtracting GC and MUX / DEMUX losses), method reference_structure.
- Two multimode sections: `mmi_width_um` / `mmi_length_um` entered twice with the region in `condition` (W2 / L2
  shallow-etched intersection, W1 / L1 fully etched); taper lengths Lt1 / Lt2 likewise.
- MUX / DEMUX excess losses: whether per device or MUX + DEMUX pair is not stated: scope `unspecified`.
- The fabrication sentence prints "284 nm deep ultraviolet lithography" (likely 248 nm); kept as printed in notes;
  `process_name` empty (no named process).

Fab / facility: fab empty (passive sentence, no org; D80b). No facility. No missing orgs.

## lit:li2013 (2 components, 15 metric rows)

| component | class | metrics |
|---|---|---|
| nonuniform_gc | fiber_chip_coupler.grating | 14 (mean IL 3.1 dB over 31 dies, best 2.7 dB, 1-dB bandwidth 41 nm, back-reflection > 17 dB derived / 25 dB simulated, mode angle ~17 deg, period 640 nm, fill factor 0.469, fiber MFD ~10.5 um, taper-start width ~400 nm, 60 nm etch, 220 nm core, 2 um BOX, 2.3 um cladding) |
| uniform_gc | fiber_chip_coupler.grating | 1 (mean IL ~3.47 dB derived: 3.1 + 0.37 dB) |

Not entered and why:
- 0.2 dB standard variation of IL: kept in notes (not a separate `std` row).
- Simulated maximum directionality ~0.65 (1.87 dB) and optimal cladding / BOX 2.38 / 1.96 um (Fig. 2): no
  directionality parameter; uniform-GC parameter sweep; notes.
- Table II trench sizes of the first 13 gratings, minimum feature 180 nm, peak shift ~5 nm per degree: notes.
- Cross-wafer peak wavelength (Fig. 3(b)): set by the chosen tilt; not entered.

Judgment calls:
- Per-GC values from GC loops printed directly with no total or halving shown: `loopback_half`, `measured` (D452).
- Fill factor defined as trench / period (etched fraction): fend 0.531 stored as tooth fraction 0.469 `derived` (D253).
- Back-reflection bound > 17 dB `derived` (the authors' worst-case bound from their measured 0.2 dB ripple; formula not
  printed); auditor may prefer `author_estimate`.
- Uniform GC row: fabricated comparison design, value from the printed 0.37 dB difference (approx, 3.1 is rounded).

Fab / facility: fab `org_astar_ime` ("fabricated on an 8' SOI wafer at the Institute of Microelectronics
(IME)/A*STAR", p.3). OpSIS named only as the funding project (p.1 footnote, p.4 acknowledgment): not a fab org.
`process_name` empty (no named PDK; "248 nm photolithography" is a lithography step). No missing orgs.

## Registry gaps (proposals)

- `subwavelength_period_nm`, `gap_nm`, `n_periods` for `polarization` (lin2021a SWG period 210 nm, SWG gap 80 nm,
  N1 = 2 / N2 = 5, p.4 Table 1, p.8 Table 2): allow the existing definitions on polarization.
- `gap_nm` for `mode_converter` (shang2023 2 um gap between the MUX output arms, p.4): allow (output-arm separation).
- `crossing_angle_deg` for `crossing` (kim2014 110 / 105 deg, p.5): angle between the two intersecting MMIs /
  waveguides.
- `directionality_pct` for `fiber_chip_coupler` (li2013 simulated maximum ~0.65, p.2): upward-diffracted fraction of
  the grating power.
- `min_feature_nm` (all classes, design rule; shang2023 0.2 / 0.5 / 0.4 um, li2013 180 nm).
