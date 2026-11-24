# lit_274 batch report

Papers: lit:watanabe2019, lit:ura2017, lit:wang2025d, lit:xu2017c, lit:nambiar2017. Page-1 titles match the source
rows; no garbled text layer. Total 8 components / 76 metric rows. `merge_component_staging.py --dry-run`:
+8 components, +76 metrics, 0 errors (two warnings from other batches: cmp_lit_guo2024a_exc02, cmp_lit_ni2025b_pimmwc).
verified_on 2026-11-24. Values only from each paper's own text, tables and figures; comparison-table rows of other
works (watanabe2019 Table 1, wang2025d Table II) not entered.

## lit:watanabe2019 (2 components / 24 metrics)

- `cmp_lit_watanabe2019_2dgc_vertical` (fiber_chip_coupler.grating, soi, 21 metrics): measured per-coupler loss
  2.6 dB at 1544 nm (x-port) and 3.4 dB at 1536 nm (y-port), `reference_structure`, basis measured (waveguide,
  back-to-back and 1-D GC terms "characterized separately", only 0.43 dB/mm printed; D167 / D452); 3-dB widths 36 /
  27 nm; worst-case polarization crosstalk 16.2 / 20.8 dB (`ge`, Fig. 6 span 1480-1600 nm inferred); PDL ~3 dB at
  1540 nm (fiber-to-fiber, both ports summed); back-reflection 9.6 / 20 / 8.2 dB at 1520 / 1540 / 1560 nm from the
  printed ~11 / 1 / 15 % Fabry-Perot reflectivities (derived); simulated 2.4 dB (58 %), 19 dB crosstalk, 30 nm 3-dB
  width; geometry: 0 deg fiber, 20 periods, 220 nm Si, 3 um BOX, 70 nm shallow etch, 1.5 um cladding, 300 um tapers,
  450 nm output waveguides.
- `cmp_lit_watanabe2019_si_waveguide` (waveguide_platform.straight, soi_strip, 3 metrics): 4.3 dB/cm (printed
  0.43 dB/mm, derived), C band inferred; width 450 nm, 220 nm Si.

Not entered: Fig. 4 simulated fabrication tolerances (CE > 50 % for +/-5 nm etch-depth error, width / misalignment /
tilt sweeps; no parameter); per-period apodization parameters t1, t2, w1, w2, w3 (Fig. 2(a) curves); Fig. 3
periodic comparison design (simulation only, no performance value); fabricated -45 / 28 nm etch-layer misalignment
(notes); 1-D output GC loss (authors' earlier design, ref. [4], value not printed).
Fab: org_eth_zurich, first-person "We fabricated" (p.7) with all authors at IEF, ETH Zurich (printed "Institute of
Electromagnetics Fields, Zurich"; watanabe2020 precedent uses the parent org). No facility named ("our fabrication
facility", p.4).

## lit:ura2017 (3 components / 12 metrics)

- `cmp_lit_ura2017_crigic_center` (free_space_emitter.other, sin, 7 metrics): simulated maximum output coupling
  efficiency 32 % into air at 1553 nm (CMT model, = eta_Air); design period 878.0 nm, 11 periods (9.66 um), CRIGIC
  width 70 um, 50 nm groove, 550 nm deposited Si-N (design tF 500 + tG 50 nm).
- `cmp_lit_ura2017_crigic_quarter_shift` (free_space_emitter.other, sin, 1 metric): simulated output coupling 0 %
  ("vanishes at delta = +/-1/4").
- `cmp_lit_ura2017_crigic_rear_dbr` (reflector.bragg, sin, 4 metrics): calculated reflectance 1.000 (100 %), kappa_DBR
  30.3 /mm -> 303 /cm (simulated, D83f), length 252 um, 50 nm groove.

Not entered: measured result is only a normalized near-field profile (Fig. 11) plus "too small to be seen" for the
quarter-shift device, no number; GC radiation decay / coupling factors alpha = kappa_GC = 1.68 /mm (no parameter);
front DBR 57.1 um and phase gaps 329 nm (notes); Fig. 10 FWHM vs delta (no printed values); input GC 0.5 x 0.5 mm
(no performance value).
Fab: empty (passive "designed and fabricated", authors at two orgs: Kyoto Institute of Technology and AIST).

## lit:wang2025d (1 component / 19 metrics)

- `cmp_lit_wang2025d_trident_grating_ec` (fiber_chip_coupler.edge, ge_silica, 19 metrics): coupling loss 0.95 dB/facet
  at 1310 nm, 0.93 dB/facet at 1550 nm, range 0.41-1.36 dB/facet over 1264-1620 nm (author_estimate, see judgment
  call 1); 1-dB tolerance +/-3 um (x) and +/-3.5 um (y, vertical axis in the condition, D460) measured at 1550 nm;
  simulated 0.86 dB/facet at 1550 nm and 0.40-1.36 dB/facet; Table I geometry (32 periods, 2.6 um period, f 0.5,
  W1 / W2 tip widths 1.8 / 2.4 um, W3 1.1 um, Wout 4 um), 83.2 um tapered length, footprint 715.52 um2 (8.6 x 83.2),
  4 um core, 10 um lower / 20 um upper cladding.

Not entered: 0.12 dB/cm straight-waveguide loss (sentence cites ref. [19], D80i); "bandwidth 356 nm" for
CL < 1.36 dB/facet (no parameter for a custom-level bandwidth; the range row holds the information); Gap 1.3 um
(gap_nm not allowed on fiber_chip_coupler); lg 1.3 um (implied by f and period); 124.8 um simulated transition
length; 8 deg polished facet angle (no parameter); 10 Gb/s eye diagrams.
Fab: Shijia Ltd. (CN) is named with the platform ("prepared on the SiO2 PLC platform (Shijia Ltd., CN)", p.2
Sec. III) but is not in the registry: fab left empty, process_name "SiO2 PLC platform (Shijia Ltd., CN)".

## lit:xu2017c (1 component / 11 metrics)

- `cmp_lit_xu2017c_sin_gc_au_mirror` (fiber_chip_coupler.grating, sin, 11 metrics): 22 % per grating at 1550 nm
  (`loopback_half`, eta = sqrt(T), derived), 3-dB width 58 nm (measured, as printed), 1-dB lateral tolerance
  >= 4 um (both axes, one row); simulated 60 %, centre 1550 nm, 1-dB width 60 nm; period 1000 nm (printed 1 um,
  derived), 50 periods, 130 nm groove depth (HSQ-defined, no etch), 400 nm Si3N4, 7 deg fiber.

Not entered: Fig. 3 sibling periods 0.98 / 0.96 um (no printed values); Au mirror 100 nm and lower SiO2 (no
parameter / thickness not stated; in core_material).
Fab: org_university_of_central_florida (see judgment call 4).

## lit:nambiar2017 (1 component / 10 metrics)

- `cmp_lit_nambiar2017_dual_band_gc` (fiber_chip_coupler.grating, sin, 10 metrics): per-coupler loss 9.2 dB (O band)
  and 6.35 dB (C band), measured, method unspecified; 3-dB widths 55 / 58 nm; 950 nm period, fill factor 0.4
  (printed 40 %, definition not stated), 8 deg fiber, 700 nm SiN, 1.7 um bottom oxide, etch depth 400 nm from the
  Fig. 1(a) label (judgment call 5).

Not entered: simulated maps and etch-depth sweeps (Fig. 1(b)-(e)); values for the 930 / 940 nm periods (curves only).
Fab: empty (passive "were fabricated"; authors at CeNSE, Indian Institute of Science).

## Judgment calls for the auditor

1. wang2025d coupling losses `author_estimate`, not `derived`: CL = (IL - PL)/2 uses 0.12 dB/cm printed in a sentence
   that cites ref. [19] ("characterized ... obtained from the cut-back method [19]"); D80i makes the input borderline
   cited (rule 4). The 1-dB tolerances are relative measurements and stay `measured`.
2. watanabe2019 per-coupler losses `measured` + `reference_structure`: the subtracted b2b and 1-D GC terms are own
   separate characterizations whose values are not printed (D167 / D452); 3-dB widths measured on the de-embedded
   spectra. Crosstalk "at the maximum" stored as `ge` suppression over the Fig. 6 span (inferred 1480-1600 nm).
3. watanabe2019 back-reflection rows: printed % reflectivities from Fabry-Perot ripples converted to dB, `derived`,
   `approx` (sacher2014b / li2013 precedent).
4. xu2017c fab org_university_of_central_florida from "we present the design and fabrication" (p.2 Conclusion;
   luo2021 precedent) with all authors at CREOL, UCF; parent org as in rao2019 (org_ucf_creol also exists in the
   registry).
5. nambiar2017 etch depth 400 nm `extracted_from_figure` from the Fig. 1(a) schematic label on a vertical bracket
   (same symbol as the 700 nm t_SiN bracket); D156 says drop it if the auditor finds the label ambiguous.
   nambiar2017 losses scope `per_coupler` as printed ("per coupler"), method unspecified.
6. ura2017: CRIGIC classed `free_space_emitter.other` (guided wave to vertical free-space radiation, no fiber;
   mehta2016 input-GC precedent), scope `per_coupler`, all performance values simulated (D80e keeps the rows
   `fabricated`). The rear DBR is a separate `reflector.bragg` row (D396); the quarter-shift sibling is a row with a
   simulated 0 % efficiency (its only printed performance value).
7. wang2025d tip_width_nm used for the two fiber-end branch widths (W1, W2) and width_nm for W3 / Wout, roles in the
   condition (hatori2014 trident precedent); taper_length_um 83.2 um = whole tapered grating section.
8. watanabe2019 waveguide row platform `soi_strip` (waveguides defined in the full-etch step, p.7) and width 450 nm
   tied to the loss value by reading of the setup (noted).

## Missing orgs

- Shijia Ltd. (CN): fab, lit:wang2025d p.2 Sec. III ("SiO2 PLC platform (Shijia Ltd., CN)"); would go on
  cmp_lit_wang2025d_trident_grating_ec.

## Registry gaps

- gap_nm on fiber_chip_coupler: wang2025d trident branch Gap 1.3 um (p.2 Table I); also noted for watanabe2020.
  Proposed: allow gap_nm on fiber_chip_coupler (gap between parallel grating / taper branches).
- Bandwidth at a custom loss level: wang2025d 356 nm for CL < 1.36 dB/facet (p.3 Sec. III). Proposed:
  `bw_at_level_nm` with the level in condition (deferred precedent D81 / D250 style; the range row already holds it).
- Grating radiation decay factor: ura2017 alpha = 1.68 /mm (p.4 Sec. III-B). Proposed: `radiation_decay_per_mm`
  (free_space_emitter, fiber_chip_coupler), calculated or measured as stated.
- Fabrication tolerance of coupling efficiency vs etch depth: watanabe2019 CE > 50 % for +/-5 nm (p.6, Fig. 4(a),
  simulated). Proposed: `etch_depth_tolerance_nm` with the criterion in condition.
- Facet angle: wang2025d 8 deg polished facet (p.2 Sec. III); rejected earlier (D250), listed only as a repeat.
