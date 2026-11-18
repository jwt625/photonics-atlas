# lit_190 batch report

Distilled 2026-11-18. Papers: badri2019, xie2024a, tanaka2009, pita2021. Totals: 11 components, 91 metric rows.
`merge_component_staging.py data/_staging/components/lit_190 --dry-run`: +11 components, +91 metrics, 0 errors (the one
warning is on the merged row `cmp_lit_ni2025b_pimmwc`, not this batch).

Page-1 identity: all four cached texts are the listed works. badri2019 is the author manuscript of the SPIE Optical
Engineering paper (p.1 links to the formal version); xie2024a is the arXiv v1 preprint of the APL paper; pita2021 is
the arXiv v3 author version of the Optics Letters paper. tanaka2009 is the publisher PDF. The values come from these
cached copies; the journal versions were not read.

## tanaka2009 (3 components, 14 metrics; design-only, 2-D FDTD)

- `offset_crossing_20deg_te`: TE-optimum offset 0.214 um: 0.021 dB, -55.0 dB crosstalk; core-width tolerance +/-0.03 um:
  < 0.06 dB, < -40 dB; width / thickness 330 nm (derived from 0.33 um).
- `offset_crossing_20deg_tm`: TM-optimum offset 0.251 um: 0.070 dB, -48.6 dB.
- `simple_crossing_20deg`: comparison crossing without offset at 20 deg: 8.0 dB, -1.4 dB (TE).
- Not entered: Fig. 2 angle sweeps (20-70 deg, figure reads of other designs); introduction values for a simple 90 deg
  crossing (about 1.0 dB / -12.4 dB, p.2): origin not stated, outside the Fig. 2 angle range.
- Judgment calls: TE and TM optima are different offsets, so two design rows (rule 9); platform `soi` from the p.2
  statement that Si wire circuits are made on SOI substrates (Fig. 1 shows Si core in SiO2). Fig. 1 attributes the
  structure to the authors' LEOS 2009 conference paper (ref. 7); the journal paper's own simulation values are kept (D408).
- Orgs: none (no fabrication).
- Registry gap: crossing angle (deg) and offset length of an offset crossing; values only in labels.

## badri2019 (2 components, 20 metrics; design-only, 2-D FDTD)

- `mfe_slot_crossing_3x3`: 1.1 dB / -16.0 dB at 1550 nm; average 1.2 dB and crosstalk < -15.1 dB over O-U bands
  (1260-1675 nm from the Fig. 6 axis, `wavelength_inferred`); best 0.76 dB at 1435 nm; C band average 1.16 dB, crosstalk
  < -16.0 dB; O band up to 1.9 dB; footprint 4 um2 (derived from 2 x 2 um2); slot 100 nm (`gap_nm`, precedent
  acoleyen2011 / xu2018), rail 200 nm, height 250 nm, multilayer period 77.5 nm (`subwavelength_period_nm`), 3 x 3 ports.
- `simple_slot_intersection_3x3`: plain intersection without lens: 11.2 dB, -4.7 dB at 1550 nm.
- Not entered: return loss (C band < -12 dB, O band up to -7 dB, p.6): no reflection parameter for `crossing`
  (`back_reflection_db` is limited to coupler classes); minimum inclusion widths 35 / 18 nm (no parameter); comparison
  values of refs. 22-25 (rule 3).
- Orgs: none (no fabrication).
- Registry gap: `back_reflection_db` (or a `return_loss_db`) for `crossing`; skipped values 12 dB (gt, C band, p.6) and
  7 dB (O band, p.6). Proposed definition: reflected power at the input port of the crossing, positive dB below the input.

## pita2021 (4 components, 28 metrics)

- `dual_pol_2d_gc_mcf` (fiber_chip_coupler.grating): -4.3 dB best (core 2) and -4.3 to -5.4 dB range over 7 cores,
  3-dB bandwidth 48 nm (1505-1553 nm), PDL <= 0.54 dB, worst inter-core XT -42.7 dB at 1508 nm (ge) and 34.7 dB relative
  to the coupled power; simulated -3.9 dB / 50 nm; period 623 nm, fill factor 0.7 (definition not printed), 10 x 10 um
  grating, 200 um2 per core, design fiber angle 10 deg and measured best angle about 13 deg, pitch 32 um, 7 channels,
  MCF MFD 8 um (specification), 250 nm Si / 3 um BOX / 1 um cladding.
- `spins_taper` (waveguide_platform.other): simulated 0.5 dB (C band inferred), 50 um2 (derived from 10 x 5 um2),
  450 nm output waveguide.
- `focusing_gc_smf`: -3.65 dB per coupler (regression over 8 calibration waveguides), wavelength not stated.
- `si_waveguide`: 1.4 dB/cm (same regression), wavelength not stated; calibration waveguide width not stated.
- Judgment calls: the 2D-GC efficiency is entered `measured`, scope `per_coupler`, method `reference_structure`, with
  the excluded input GC / feed waveguide in `excludes`: the paper measures the calibration values but prints no
  subtraction or feed length (audit may prefer `author_estimate` + `loss_breakdown`, D428). Best-efficiency rows carry
  the measured 3-dB band as an inferred wavelength span (peak wavelength not printed). The grating etch depth is not
  tied to one of the two etches (250 nm full / 120 nm partial): not entered.
- Fab: `org_applied_nanotools` on all four rows ("fabricated in a dedicated run at Applied Nanotools (ANT)
  facilities", p.3); no process name printed. SOITEC wafer is a note. No shared facility.

## xie2024a (2 components, 29 metrics)

- `inverse_gc`: measured peak -3.8 dB at 1574.93 nm, 1-dB 71.7 nm, 3-dB > 120 nm; simulated -2.94 dB at 1572.4 nm,
  69 / 113 nm; etch-depth tolerance (400-500 nm) -2.85 to -3.9 dB and 66-82 nm; base angle near 80 deg about -3.8 dB;
  15 periods, 12 um grating width, 8 deg fiber angle, 300 um taper, 700 nm film, 450 nm etch, 70 deg base angle
  (`measured`: "estimation from the SEM measurement").
- `apod_chirp_gc` (initial design, same chip): measured -6.33 dB at 1569.3 nm, 45.7 / 85.8 nm; simulated -4.48 dB at
  1571 nm, 34 / 84 nm; first-period fill factor 0.35 (pillar fraction, D253), fiber angle 6 deg, geometry as above.
- Not entered: Table 2 per-period trench / pillar widths (30 values); +/-5 % random-variation deltas (about 0.3 dB,
  8 nm; change values); "-4.5 +/- 0.7 dB" and "-7.1 +/- 0.77 dB" moving-average values (notes); ref. 20 GC values (cited).
- Judgment calls: measured CE rows `scope: unspecified`, `method: unspecified`: the device has two GCs plus tapers
  and a waveguide, and the paper says only that the per-GC efficiency "can be further extracted" (p.6), not that it was
  halved or how the tapers were treated. Measured rows leave polarization empty (polarization controller, TE design).
  Tolerance rows carry the design FOM band 1555-1595 nm as an inferred span (peak wavelengths not printed).
- Fab empty: passive "is fabricated" (p.5), all authors at CU Boulder, no fabrication statement naming the authors (D80b).
- Missing facility org: "Center for Integrated Nanotechnologies, an Office of Science User Facility operated for the
  U.S. Department of Energy (DOE) Office of Science by Los Alamos National Laboratory ... and Sandia National
  Laboratories" (p.7 Acknowledgements; "This work was performed, in part, at"). Role: facility, both xie2024a rows. Not
  in `organizations.csv` / `org_aliases.csv` (Sandia exists as `org_sandia_national_laboratories`, but the operator of
  a facility is not the facility, D82c).

## Stops

None. No correction / erratum, no other-paper copy, no garbled text layer.
