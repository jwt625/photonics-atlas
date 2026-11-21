# lit_241 batch report

Papers: lit:chang2018b, lit:liu2023b, lit:zhang2013b, lit:sanchis2007, lit:celo2014 (all waveguide crossings).
Page-1 titles match the source rows; no garbled text layer; none is a correction. verified_on 2026-11-20. Dry run of
`merge_component_staging.py`: +13 components, +108 metrics, 0 errors; the one warning names the merged row
cmp_lit_ni2025b_pimmwc, not in this batch. Figure values were read on page renders at 4-6x zoom.

| paper | components | metric rows |
|---|---|---|
| chang2018b | 2 | 21 |
| liu2023b | 2 | 19 |
| zhang2013b | 1 | 14 |
| sanchis2007 | 5 | 40 |
| celo2014 | 3 | 14 |

## chang2018b (three-mode crossing with subwavelength asymmetric Y-junctions, IEEE Photonics J. 2018)

Rows:
- `crossing.other` three-mode crossing (four SW Y-junctions + 3 x 3 MMI crossing array): cutback per-crossing loss
  TE0 / TE1 / TE2 = 1 / 1.42 / 1.92 dB at 1560 nm (fit slope over 1 / 3 / 5 / 7 crossings, measured); single-device
  normalized IL < 2 dB over 1530-1590 nm (scope unspecified: normalization reference not named); crosstalk bar port
  > 20 dB and cross port > 35 dB; simulated IL < 1.5 dB and CT > 22 dB (1520-1580 nm); footprint 1156 um2 (derived),
  220 nm core / hole etch, 1.2 um SiO2, access taper 1.35 um long, 1.4 um wide end, 0.45 um narrow end.
- `mode_converter.mdm_mux` SW asymmetric Y-junction MUX / DEMUX: reference MDM system (MUX + multimode waveguide +
  DEMUX) IL < 1.6 dB (mean, scope unspecified) and CT > 22 dB over 1530-1590 nm; footprint 17.28 um2 (3.6 x 4.8),
  220 nm etch / core, 1.2 um cladding.

Not entered:
- Abstract IL < 0.9 dB and CT < -24 dB over 1.52-1.60 um (p.2): conflict with the body (IL < 2 dB, cutback 1-1.92 dB
  per crossing, CT < -20 dB; p.3, p.7, p.8) and the conclusion; noted on the component (liu2019 D535 precedent).
- Fabry-Perot fringe spacing ~9 nm (8.86 nm calculated) in the cascades (p.7): not a crossing property.
- Simulated hole-radius tolerance (ILs up ~1 dB, CT < -18 dB at 40 nm radius; Fig. 6, p.7-8): perturbed design, no
  wavelength printed.
- Array geometry with no role-specific parameter: taper-to-intersection 2.525 um, intersection spacing 3.25 um, 5 um
  single-mode links (p.4); Y-branch gap 1.575 um (gap_nm not allowed on mode_converter); pixel 120 nm and hole radius
  45 nm (no parameter; in core_material).

Orgs: fab `org_huazhong_university_of_science_and_technology` on both rows: "we also designed, fabricated and
experimentally characterized three, five and seven cascaded crossings" (p.7), all authors at HUST School of Optical and
Electronic Information (p.2); EBL / ICP flow on p.5. No facility named. No missing org.

## liu2023b (polarization-insensitive metasurface crossing, PTL 2024)

Rows:
- `crossing.other` TE0 / TM0 metasurface crossing (inverse design, 40 x 40 pixels of 120 nm, 0.8 um waveguides):
  measured IL < 0.4 dB TE0 and < 0.7 dB TM0, CT > 20 dB, 1500-1600 nm (normalized by the reference back-to-back PDM
  system, per_component); simulated IL < 0.45 / < 0.39 dB (TE0 / TM0, 1200-1700 nm), 0.08 / 0.31 dB at 1550 nm, CT > 28
  dB (cross port), > 110 dB (through-port polarization conversion); pixel +/-30 nm tolerance IL < 0.73 / < 0.40 dB and
  CT > 26 dB (at 1250 and 1550 nm, one row, rule 7); footprint 23.04 um2; 220 nm core / etch, 2 um BOX.
- `polarization.psr` PSR pair (reference back-to-back PDM system): IL < 0.4 dB (input I1) and < 2 dB (input I2),
  1500-1600 nm, scope unspecified.

Not entered:
- Abstract / p.1 simulated IL < 0.4 dB for both polarizations over 1200-1700 nm: conflicts with p.2 TE0 < 0.45 dB; p.2
  values entered, conflict noted.
- PSR footprint 7.92 x 2.4 um2: cited from the authors' ref. [3] (rule 3).
- Reference-system CT < -12 dB (p.4): `crosstalk_db` not allowed on polarization; not a wanted / unwanted output-port
  ratio for `per_db` (D424). Registry gap: crosstalk_db on polarization (already a D439 candidate).
- Circuit footprint 30 x 30 um2 (crossing + four PSRs): system, not a component. Table I rows: other works.
- IL increase "up to 0.1 dB" under pixel variation: a delta, no parameter.

Orgs: fab empty ("The designed device is fabricated", passive; all authors Yanshan University; D80b). No facility. No
missing org.

## zhang2013b (CMOS-compatible low-loss crossing, PTL 2013)

Rows:
- `crossing.other` PSO-optimized spline-taper crossing: cross-wafer IL mean 0.18 dB, std 0.03 dB, range 0.13-0.27 dB
  (26 dies, cutback slope over 5 / 10 / 15 / 20 crossings), single-die < 0.2 dB; crosstalk mean 41 dB, std 2 dB, range
  36-45 dB, typical > 40 dB (orthogonal port vs GC loop, near noise floor); simulated IL 0.11-0.27 dB and CT 38.3-42.7
  dB over 1500-1580 nm (Fig. 2 reads), simulated ~0.4 dB at 200 nm top Si; 220 nm core, 2 um BOX, 2.3 um cladding.
  process_name "248 nm CMOS compatible process, one patterning step (8-inch SOI)".

Not entered:
- Taper widths w1-w10: not printed (geometry kept from ref. [15]).
- Simulated back-reflection (Fig. 2(b), about -27 to -37 dB): `back_reflection_db` not allowed on crossing (registry
  gap; value Fig. 2(b), p.2; proposed: allow back_reflection_db on crossing). Measured reflection not obtained (p.3).
- FOM 0.965 at 1550 nm (normalized transmission minus crosstalk): not a registry quantity.

Orgs: fab empty. "We taped out the crossing design" with DRC routines "provided by the foundry" and a passive
fabrication sentence (p.2) name no foundry (D433); authors at University of Delaware, IME A*STAR and NUS. OPSIS appears
only as a supported project in the funding note and acknowledgment (D80c). No facility. No missing org.

## sanchis2007 (optimized-angle SOI crossings, PTL 2007)

Rows: five `crossing.other` rows, one per fabricated crossing angle (40 / 60 / 90 / 120 / 140 deg; sibling designs,
rule 9). Each: IN-to-OUT1 crossing loss at 1550 nm (normalized to a straight waveguide), crosstalk to OUT2 and OUT3,
205 nm core, 3 um silica, 500 nm width.
- 60 / 120 deg: printed IL 1.6 dB (measured, "for these optimum crossing angles", p.3); crosstalk figure reads OUT2 /
  OUT3 ~20.2 / ~18.3 dB (60 deg) and ~17.8 / ~19.4 dB (120 deg); 60 deg also ~20 dB over 1535-1570 nm (Fig. 5, text).
- 40 / 90 / 140 deg: experimental IL ~6.4 / ~1.5 / ~6.6 dB and crosstalk OUT2 ~16.0 / ~10.4 / ~4.4 dB, OUT3 ~5.5 /
  ~10.8 / ~11.6 dB (extracted_from_figure, reading +/-0.1 dB IL, +/-0.3 dB crosstalk); 3D-FDTD squares at the same
  angles as simulated rows (IL ~6.45 / ~1.55 / ~6.1 dB; OUT2 ~18.3 / ~12.2 / ~6.4 dB; OUT3 ~6.0 / ~12.1 / ~16.2 dB).

Not entered:
- 3D-FDTD points at 50 / 70 / 110 / 130 deg and the 2D-FDTD curves (n_eff 2.8 effective-index model): simulation-only
  angles with no fabricated device; could be added as `row_kind: design` rows if the auditor wants them.
- Printed "crosstalk losses up to 20 dB" / "around 20 dB" at 60 / 120 deg at 1550 nm (p.3): the per-port figure reads
  are entered instead (the printed value is approximate and pooled over two angles and two ports); kept only for the
  60 deg wavelength sweep, which is the only place the paper ties it to a span.
- "more than 10 dB" crosstalk improvement vs 90 deg (abstract): a difference.
- Width robustness study (optimum angle ~60 / 120 deg for 450-550 nm widths, simulated): no value per design.
- Bend radius 5 um: `min_bend_radius_um` not allowed on crossing.
- Registry gap: crossing angle (proposed `crossing_angle_deg`, geometry, crossing: angle between the input waveguide and
  the crossing waveguide as printed); values 40 / 60 / 90 / 120 / 140 deg, p.2-3 Figs. 2-4. Currently in labels only.

Orgs: fab empty. EBL / ICP with Cr lift-off described passively (p.2); the acknowledgment thanks three named people for
contributions to the fabrication process without naming their org (D543). Authors at the Valencia Nanophotonics
Technology Center (Universidad Politecnica de Valencia), DAS Photonics and ESA (p.1). No facility. No missing org (no
fab / facility role to fill; NTC as a UPV unit is the open D533 org-round item, not needed here).

## celo2014 (low-loss single-etch crossings on SOI, GFP 2014)

Rows:
- `crossing.mmi` GA-optimized DRC-smoothed MMI crossing: C-band mean 0.11 dB per crossing (normalized loss / N, derived,
  3 structures), 0.10 dB at 1540 nm (linear fit over 40 / 80 / 120 crossings, measured, +/-0.02 dB), crosstalk > 45 dB
  over the C band; simulated 0.07 dB (1530 nm), 0.09 dB (1570 nm), 0.045 dB best (1540 nm); footprint 42.25 um2
  (6.5 x 6.5), length 6 um and arm width 1.3 um from the Fig. 1 labels, 220 nm core, 2 um BOX, 2.3 um cladding.
- `fiber_chip_coupler.grating` GC reference loop: fiber-to-fiber peak 9.9 dB (loopback, C band inferred).
- `waveguide_platform.straight` test waveguide: 2 dB/cm (C band inferred, method unspecified).

Not entered:
- Measured losses "30-40 % higher" than simulation: a comparison.
- Fig. 3 crossing transmission spectra (whole cascades): the per-crossing values are entered instead.
- Fig. 1 "1.3 um" entered as `width_nm` (role in the MMI not stated), not `mmi_width_um`.

Orgs: fab `org_cmc_microsystems` on all three rows ("through a CMC (Canadian Microelectronics Corporation)
Microsystems multi-project-wafer run", p.2; MPW access provider, D83d / D398); the research foundry is not named (p.1).
Authors at Huawei Technologies Canada. No facility. No missing org.

## Judgment calls for the auditor

1. chang2018b: fab HUST on the mode-converter row rests on the shared p.5 flow plus the p.7 first-person sentence for
   the crossing cascades (D656 single-flow precedent).
2. chang2018b: p.4 Y-junction geometry placed on the reference MUX / DEMUX row; the paper names both the same structure
   but does not state the layouts are identical (noted on the row).
3. chang2018b / liu2023b: back-to-back reference systems (MUX + DEMUX; PSR pair) entered as component rows with scope
   unspecified (normalization not stated), rather than `de_embedded` (a2017 precedent used de_embedded with a stated
   reference).
4. chang2018b: abstract 0.9 dB / -24 dB left out as conflicting with the body; the alternative is entering them with a
   D417 conflict note.
5. chang2018b: single-device "< 2 dB" row scope unspecified / method unspecified although a reference MDM system was
   fabricated "to evaluate the performance" (p.5); per_component + reference_structure is the other reading.
6. sanchis2007: printed 1.6 dB entered on both the 60 and 120 deg rows (the sentence names both angles); crosstalk per
   port from figure reads instead of the printed "around 20 dB".
7. zhang2013b: wavelength C band inferred for the measured rows (peak of GC-limited spectra, Fig. 3 near 1535-1540 nm).
8. celo2014: 0.11 dB mean `derived` (authors divide normalized cascade loss by N, D80a) and 0.10 dB fit `measured`.

## Registry gaps

- `crossing_angle_deg` (geometry, crossing): sanchis2007 40 / 60 / 90 / 120 / 140 deg (p.2-3, Figs. 2-4).
- `back_reflection_db` on crossing: zhang2013b simulated about -27 to -37 dB over 1500-1580 nm (p.2 Fig. 2(b)).
- `crosstalk_db` on polarization (existing D439 candidate): liu2023b PSR pair CT < -12 dB (p.4).
- `gap_nm` on mode_converter (existing D533 candidate): chang2018b Y-branch gap 1.575 um (p.4).
