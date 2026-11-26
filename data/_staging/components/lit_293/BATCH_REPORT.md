# Batch lit_293 report

Distilled 2026-11-26. Four papers. `uv run --offline python scripts/merge_component_staging.py data/_staging/components/lit_293 --dry-run`: +22 components, +120 metrics, 0 errors. The two WARN lines belong to the merged guo2024a / ni2025b rows.

Page-1 titles match the source rows for all four papers. None is a correction or erratum, and no text layer is garbled. Page 1 of laere2007a, kopp2010 and tsuchizawa2005 has no `figures/page_01.png`. Those pages and some figure zooms were rendered from `source.pdf` into the session scratchpad only.

## lit:taillaert2003 (IEEE PTL 15(9) 1249, 2003; 2-D grating coupler used as a polarization splitter)

| component | class | metrics |
|---|---|---|
| cmp_lit_taillaert2003_gc_2d_pol_splitter | fiber_chip_coupler.grating | 11 |

- Fiber-to-fiber transmission 4 % (TE, measured) on the Fig. 1(C) structure, which is a single waveguide with the 2-D grating at both ends.
- Per-coupler efficiency about 20 % (derived: the square root, as the paper does it) and 6.99 dB (derived, not printed).
- Polarization extinction between the two outputs over 1530-1560 nm: > 18 dB as `crosstalk_db` (measured), with a Fig. 3 peak of about 24.5 dB at 1540 nm (extracted_from_figure).
- Geometry: 580 nm lattice, 90 nm etch, 220 nm Si, 1 um BOX, 10 um waveguides, 0 deg fiber design.

### Values not entered and why
- Hole diameter 300 nm, bend radius 530 um, Waveguide 1 length 850 um, effective indices 2.83 / 1.89, beam size 10.6 um and fiber height about 10 um: no registry parameter, or setup values. They are in the notes or conditions.
- 50 % maximum efficiency for a symmetric grating at normal incidence: a concept statement, not a result.
- 0.5 nm fringe spacing and 25 dB input-polarization extinction: setup values (rule 13).
- Fig. 4 output powers: absolute detected powers at the cleaved facet, not a component metric.

### Missing fab / facility orgs
None. The fabrication sentence (p.2 Sec. III-A, EBL + RIE) is passive. The authors are spread over Ghent University - IMEC, Glasgow University and Research Center COM (DTU), so fab is empty (D80b, D154).

## lit:laere2007a (IEEE PTL 19(23) 1919, 2007; compact focusing grating couplers, SOI and gold on SOI)

| component | class | metrics |
|---|---|---|
| cmp_lit_laere2007a_focusing_gc_short_taper | fiber_chip_coupler.grating | 11 |
| cmp_lit_laere2007a_focusing_gc_aperture_0p8 | fiber_chip_coupler.grating | 9 |
| cmp_lit_laere2007a_gold_focusing_gc_f125 | fiber_chip_coupler.grating | 8 |
| cmp_lit_laere2007a_gold_focusing_gc_f250 | fiber_chip_coupler.grating | 7 |
| cmp_lit_laere2007a_gold_linear_grating_design | fiber_chip_coupler.grating (design) | 5 |

- SOI focusing GC with short taper:
  - Fiber-to-fiber 10.5 dB (measured). The pair is the focusing input grating plus a standard linear output grating.
  - About 30 % per coupler (derived, as printed).
  - Geometry: 18.5 um width, 28-68 um total length, 518 um2 footprint (derived), 70 nm etch, 220 nm Si, 500 nm wire, 630 nm period / 0.5 duty cycle of the underlying design, 10 deg fiber.
- 0.8 um shallow-aperture variant:
  - 11.1 dB fiber-to-fiber, derived as 10.5 + 0.6 dB.
  - Geometry: aperture width, 30 um length, 17.5 um grating length (derived), 30 um transition.
- Gold focusing GC, 125 um focal distance:
  - Fiber-to-focus efficiency >= 20 % at 1575 nm (derived lower bound, square root of fiber-to-fiber).
  - 1-dB bandwidth 41 nm.
  - Geometry: 20 Au lines 119 nm wide, 595 nm mid period, 220 nm Si, 2 um BOX, 10 deg fiber.
- Gold focusing GC, 250 um focal distance: best Fig. 4 bar about 18.3 % at +1 um displacement (extracted_from_figure). All bar reads are in the notes.
- Gold linear grating FDTD design: 32 % simulated at 1550 nm, plus the design geometry.

### Values not entered and why
- 33 % / 40 nm / +/-2 um (ref. [2]), 69 % (ref. [3]), 34 % / 35 nm (ref. [4]) and the 37 % theoretical efficiency of the ref. [2] design: cited values (rule 3).
- 2.0 um aperture: "wider apertures show no performance penalty", but no number is printed. The Fig. 2 curve cannot be told apart from the 28 um taper trace (both dotted). The row would be geometry only, so it is not a row (rule 9).
- Reference structure (two linear gratings and a 700 um adiabatic taper): the reference has "known efficiency" from ref. [2] and no own printed number, so it has no row.
- Au line height 20 nm, the designed 125 um / 250 um focal distances and n_eff 2.7787: no registry parameter. They are in the notes.
- About 50 nm alignment accuracy between grating and waveguide: a process statement, in core_material.

### Missing fab / facility orgs
- "ePIXnet Nanostructuring Platform for Photonic Integration" (p.3 Sec. IV-A, with footnote www.nanophotonics.eu). Role: fab of the gold focusing couplers ("The devices were fabricated through ..."). It is not in organizations.csv or org_aliases.csv. Fab is empty on the two fabricated gold rows until an org exists, and the platform name is in process_name.
- The SOI couplers have a passive fabrication sentence (p.2 Sec. III-A, 248 nm DUV + ICP-RIE, ref. [8]), so fab is empty (D80b; D622 laere2007 precedent).

## lit:kopp2010 (IEEE JSTQE 17(3) 498, 2011 issue; invited review of on-CMOS integration, fiber coupling and packaging)

| component | class | metrics |
|---|---|---|
| cmp_lit_kopp2010_flipped_gc_si_mirror | fiber_chip_coupler.grating | 9 |
| cmp_lit_kopp2010_gc_initial_design | fiber_chip_coupler.grating (design) | 5 |
| cmp_lit_kopp2010_gc_bragg_mirror_3layer | fiber_chip_coupler.grating (design) | 2 |
| cmp_lit_kopp2010_gc_bragg_mirror_2layer | fiber_chip_coupler.grating (design) | 2 |
| cmp_lit_kopp2010_gc_bragg_mirror_1layer | fiber_chip_coupler.grating (design) | 2 |
| cmp_lit_kopp2010_gc_swg_mirror | fiber_chip_coupler.grating (design) | 1 |
| cmp_lit_kopp2010_si_wire | waveguide_platform.straight | 1 |

- Flipped GC with a 100 nm Si single-layer mirror, integrated above CMOS:
  - < 2.5 dB fiber-to-waveguide at 1550 nm TE (derived from the fiber-to-fiber pair).
  - Fig. 15 minimum about 2.4 dB at about 1545 nm and 1-dB width about 32 nm (both extracted_from_figure).
  - 64 % / about 2 dB theoretical (simulated).
  - Geometry: 632 nm, 70 nm, 220 nm, 0.8 um silica gap to the mirror.
- Design rows, all simulated:
  - FDTD base grating: 40 % and 14 deg optimal angle.
  - Bragg mirrors with 3 / 2 / 1 Si layers and a 1.3 um gap: 75 / 70 / 64 %.
  - SWG-mirror design: > 75 %.
- Si wire: 2.2 dB/cm measured (wavelength not printed, C band inferred).

### Values not entered and why
- Entire edge-coupler section (p.4-5 Sec. III-A, Figs. 5-10): the SiOx-overlay spot-size converter is introduced with ref. [13]. Ref. [13] is the authors' own PTL 2010 paper and is cached in this corpus as lit:bakir2010, batch lit_294. A grep of that cached text shows the same values and sentences (1-dB bandwidth about 100 nm, > 300 nm at 3 dB, three additional samples, 0.6 dB at 1400 nm / 1 dB at 1300 nm, BPM < 1 dB over 1550-1600 nm, 80 nm tip, 200-300 um taper, 3.5 um SiOx, n about 1.6, MFD 3 um lensed fiber). Not entered under D259a: reproduced from the authors' earlier paper, and entering it would duplicate lit:bakir2010. This includes the < 0.25 dB at 1550 nm and < 1 dB over 1520-1600 nm. bakir2010 was opened only to check the attribution; no value was taken from it.
- Table I (coupling loss -7 / -1.5 / -4.5 / -1 dB, +/-0.3 / +/-2 um, 60 nm): cited (refs. [12], [13], [15], [20]).
- 40-50 % state of the art (ref. [15]), 69 % Selvaraja (ref. [20]), BOX 2 um +/-50 nm giving < 2 % and < 1 deg (ref. [18]), 1-dB band 1500-1550 nm (ref. [15]): cited.
- Fig. 12 BOX-thickness illustration and the "80 % within 100 nm" rule of thumb: generic illustration, no device.
- Gaussian-mode alignment calculations (Figs. 18-19: -5 dB and +/-1.75 um for a 3 um MFD to SMF, +/-0.75 um lensed, +/-2.5 um for 10 um MFD): generic theory, not a component of the paper.
- Fig. 20 measured tolerance map "through a surface grating coupler": the grating is not identified, and the +/-1 um sentence cites refs. [34], [35] (D159, D80i).
- Packaging (Figs. 16-17, 21-22; +/-2 um dry film ref. [40], mushroom structures ref. [39], 2 um ref. [38], QFN receiver ref. [26]): cited or not components.
- Quarter-wave mirror layers 111 / 269 nm and the SWG mirror 950 nm / 130 nm: no registry parameter for mirror-layer geometry. They are in component notes.
- Si wire geometry: printed as "500 x 220 um2" (unit as printed), so it is not entered.

### Missing fab / facility orgs
None entered. No fabrication sentence names a fabricator. The Fig. 14 SEM banner reads "CEA-LETI-MINATEC" (p.7, Fig. 14 image). That banner is not a fabrication statement under D80b, so fab is empty; the auditor may weigh it. org_cea_leti exists in the registry.

## lit:tsuchizawa2005 (IEEE JSTQE 11(1) 232, 2005; invited review of NTT Si wire progress)

| component | class | metrics |
|---|---|---|
| cmp_lit_tsuchizawa2005_sion_ssc | fiber_chip_coupler.edge | 8 |
| cmp_lit_tsuchizawa2005_wire_400x200 | waveguide_platform.straight | 4 |
| cmp_lit_tsuchizawa2005_wire_300x300 | waveguide_platform.straight | 4 |
| cmp_lit_tsuchizawa2005_bend_400x200 | waveguide_platform.bend | 4 |
| cmp_lit_tsuchizawa2005_bend_300x300 | waveguide_platform.bend | 4 |
| cmp_lit_tsuchizawa2005_ring_r5 | resonator.ring | 9 |
| cmp_lit_tsuchizawa2005_ring_r10 | resonator.ring | 3 |
| cmp_lit_tsuchizawa2005_lattice_x3_series | wdm.cascaded_mzi | 5 |
| cmp_lit_tsuchizawa2005_lattice_x5_parallel | wdm.cascaded_mzi | 6 |

- SiON spot-size converter:
  - 0.5 dB per connection with 4.3 um MFD fibers and about 2.5 dB with 9 um MFD fibers (derived by subtracting the propagation loss).
  - No deterioration at 20 dBm (`power_handling_dbm` 20 gt).
  - Geometry: tip 80 nm (SEM), SiON 3 x 3 um (SEM), 7 um SiO2 overcladding, 3 um BOX.
- Si wires (TE cutback at 1550 nm): 2.8 dB/cm for 400 x 200 nm ("as low as", statistic best) and about 7.8 dB/cm for 300 x 300 nm.
- 90 deg bends at 2 um radius: 0.15 dB (400 x 200) and 0.6 dB (300 x 300) per bend (derived from 24-bend structures).
- Ring R = 5 um: FSR 17.9 nm, drop loss < 3 dB, 3-dB width < 0.12 nm at 1550 nm, Q about 13 000 (derived). Ring R = 10 um: Q about 20 000.
- Lattice filters, three in series: about 30 dB extinction relative to the sidelobe peak (`slsr_db`).
- Lattice filters, five in parallel: about 14 nm average channel shift per 50 nm delay step, 5 channels.

### Values not entered and why
- Polymer converter 0.8 dB per connection: "In previous papers, we reported" (refs. [4], [12]); rule 3.
- 60 dB/cm and 13 dB/cm for the 300 nm square wire, from earlier processes (p.3, Fig. 5). These reproduce the authors' LEOS 2002 paper (ref. [16], lit:tsuchizawa2003, already merged with the same values). The Fig. 5 SEM images and their dB/cm labels are the tsuchizawa2003 Fig. 3 / 4 images. D259a.
- 1-D photonic-crystal filter (Sec. III-A: 10 nm drop band, < 3 nm peak variation, 8 nm band gap at 1535 nm, 10 Gb/s eye, 60 nm gaps, 400 nm period, 200 cuts). The device is introduced with the authors' ref. [4] (IEICE Trans. 2004, not in the corpus). It is treated as reproduced from that paper (D259a, same pattern as kopp2010 / bakir2010). Auditor question 1.
- Single lattice filter (Fig. 16: 10 nm bandwidth, 84 nm FSR, drop loss < 2 dB, extinction > 10 dB, 75 x 6 um): introduced with the authors' ref. [23] (Opt. Lett. 2003, not in the corpus). Treated as D259a. The lattice geometry (175 nm gap, 2.5 um semicircles, 8 couplers) is kept as design geometry on the series / parallel rows. Auditor question 1.
- Ring Q below 10 000 of other groups (refs. [6], [7]): cited.
- FWM wavelength conversion in plain Si wires (Figs. 19-20: conversion efficiency "reaches 30 dB" for 5.8 cm, 3-dB bandwidth > 50 nm for 0.35 cm, input 7 dBm): registry gap, see below.
- Cross-absorption (TPA) modulator (Figs. 21-22: about 75 % modulation of the probe at 658 mW pump, about 4 ns response limited by carrier lifetime, 4.5 mm wire): no fitting class / parameter, see below.
- Sidewall roughness rms 1-2 nm (FIB-TEM), the "taper > 200 um, tip < 100 nm" design guideline, SiON / SiO2 indices, and the > 350 nm applicable bandwidth (no dB level): no parameter, or a guideline. They are in the notes.
- Fig. 6 intercepts and Fig. 9 spectra: not read (no defined quantity per converter type).

### Missing fab / facility orgs
None. Fab is org_ntt on all nine rows. The process is described in the first person ("We start off with a 100-mm SOI wafer", p.2; "our fabrication process", p.1; "we fabricated functional devices", p.4), and all authors are at NTT Microsystem Integration Laboratories (D72, D84a).

## Judgment calls (auditor please check)
1. Device sections introduced with the authors' own earlier paper but values printed without a citation. kopp2010 edge coupler (ref. [13]) is verified as reproduced from lit:bakir2010 and left out. tsuchizawa2005 1-D PhC filter (ref. [4]) and single lattice filter (ref. [23]) are left out by the same pattern but are not verifiable (the cited papers are not cached). The kopp2010 flipped mirror grating (design approach cited to ref. [19], SPIE 2010, not cached) is entered: its measured / simulated values carry no citation (D408), and the paper presents them as its own ("Experimentally, we have reached"). The alternative is to drop all ref. [19]-linked rows (7 components, 22 metrics) for consistency.
2. taillaert2003: one PSGC row with the extinction as crosstalk_db (lit_58 streshinsky2013 ruling) rather than a D396 polarization.pbs row. The efficiency comes from the Fig. 1(C) single-waveguide structure with the same 2-D grating, so both measurements are on one row (test_structure true).
3. laere2007a short-taper row: one family row covers the 28 um and 68 um total-length variants (length_um 28-68). The 10.5 dB / 30 % is printed once for the configuration and the curves overlap (D165, D254). The alternative is two rows with the value on neither.
4. laere2007a 0.8 um aperture: 11.1 dB = 10.5 + 0.6 dB (derived). The 0.6 dB increase is taken relative to the 10.5 dB short-taper value; the text does not name the baseline explicitly.
5. laere2007a f250 row: the Fig. 4 efficiency is assumed to use the same square-root definition as Fig. 3 (axis "coupling efficiency at 1575 nm"; the text does not restate it).
6. laere2007a period_nm 630 / fill_factor 0.5: the linear-grating design of ref. [2] applied to the curved lines. These are design dimensions of this paper's device, so they are entered as design_target with a note. The ref. [2] 37 % efficiency is not entered.
7. kopp2010 m1 < 2.5 dB is `derived` (the authors' extraction from fiber-to-fiber, D80a). Whether the wire loss was subtracted is not printed.
8. kopp2010 Si wire: 2.2 dB/cm with C band inferred, and the "500 x 220 um2" cross-section not entered.
9. tsuchizawa2005 R = 5 um ring typed resonator.ring although the paper calls it a channel-dropping filter. It is a Q / loss demonstration with an R = 10 um sibling, not a filter in a WDM path (D400).
10. tsuchizawa2005 series lattice: "extinction ratio with respect to the sidelobe peak" is stored as `slsr_db` (main peak over sidelobe). The alternative is `extinction_db` with that condition.
11. tsuchizawa2005 parallel lattice: "average wavelength shift per delay increment about 14 nm" is stored as `channel_spacing_nm` (mean, approx).
12. tsuchizawa2005 SSC 0.5 / 2.5 dB: `derived`, method cutback (the paper describes subtracting the propagation loss). The wavelength is 1550 nm inferred from the Fig. 6 propagation data. The Si core (200 or 300 nm) of the SSC sample is not stated. `power_handling_dbm` uses qualifier gt per the registry definition, although the text ("even at 20 dBm") reads as ge.
13. tsuchizawa2005 bends: the per-bend values are `derived` (24-bend totals), with 1550 nm inferred. The 300 x 300 nm Fig. 8 data differ from the tsuchizawa2003 Fig. 6 bend curve (about 31 dB vs about 26 dB at 2 um), so they are treated as new data.

## Registry gaps
- `conversion_efficiency_db` (frequency_converter): FWM / parametric conversion efficiency as a dB ratio of idler to signal (or to the paper's reference) as defined by the paper, sign as printed. Skipped: tsuchizawa2005 "reaches 30 dB" for a 5.8 cm Si wire (p.6-7 Sec. III-D, Fig. 20). Allowing `bw_3db_nm` on frequency_converter (conversion 3-dB bandwidth vs detuning) would cover the skipped > 50 nm for 0.35 cm (p.7).
- All-optical (cross-absorption) modulation: no class or parameter for modulation depth in % or a carrier-lifetime-limited response time. Skipped: tsuchizawa2005 about 75 % at 658 mW and about 4 ns (p.7 Sec. III-E, Fig. 22). Proposed: `modulation_depth_pct` and `response_time_ns` on switch_fabric.other (D468 all-optical gate precedent). Low priority: single values.
- Mirror-layer geometry for bottom-reflector grating couplers (`mirror_layer_thickness_nm`, `mirror_gap_um`): kopp2010 Si 111 nm / SiO2 269 nm, 100 nm and 130 nm mirror layers, SWG mirror period 950 nm (p.6-7). The gap is currently stored in box_thickness_um ("lower cladding thickness") with a condition.
- `hole_diameter_nm` (fiber_chip_coupler, 2-D / photonic-crystal gratings): taillaert2003 300 nm (p.2 Sec. III-A).
- `metal_thickness_nm` for metal-line gratings: laere2007a Au lines 20 nm (p.2 Sec. II, p.3 Sec. IV-A).
