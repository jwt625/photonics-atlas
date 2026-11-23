# Batch lit_262 report

Papers: lit:xu2021c, lit:wang2014c, lit:zhu2017a, lit:ding2015, lit:maire2008 (papers cited in other papers' benchmark
tables; only values each paper reports itself are entered). verified_on 2026-11-23.
Total 19 components / 145 metric rows; `merge_component_staging.py --dry-run`: 0 errors, no warnings on these rows.
Page-1 titles match the source rows; no correction / erratum; no garbled text layer. Generator script kept in the
session scratchpad (`lit_262/gen.py`).

## lit:maire2008 (High efficiency Si3N4 surface grating couplers, OE 2008) - 5 components / 42 metrics

- `gc_full_etch_clad`, `gc_full_etch_noclad`, `gc_partial_etch_clad`, `gc_partial_etch_noclad` (fiber_chip_coupler.grating,
  sin; 300 nm LPCVD Si3N4 on 3.26 um SiO2, 40 um wide): measured CE at 1310 nm 67 / 23 / 62 / 40 % (p.4, Fig. 2), resonance
  angles 10.5 / 14 deg (clad), 3-dB bandwidth about 50 nm "for each structure" (one row per structure), partial-etch clad
  wavelength scan > 40 % over 1250-1400 nm and > 20 % at 1450 nm (p.4, Fig. 3); simulated about 60 % (fully etched,
  60 nm top cladding, p.3); geometry (period 1 um derived, duty 0.5, etch 300 / 250 nm, 50 nm slab, 530 nm top clad derived).
- `gc_partial_clad_w30_dr050` (30 um wide duty-ratio set, best at 0.5): CE about 50 %, angle about 13.3 deg (p.5).
- CE definition: (P_inc - P_t - P_r) / P_inc from measured powers (p.4 Eq. (3)), free-space beam (1/e2 diameter about
  30 um): `measured`, `per_coupler`, method `direct`.
- Not entered: 3-dB angular tolerance about 4 deg (no parameter); coupling length Lc about 11.2 um (no parameter); other
  duty ratios (Fig. 4 only); period of the partially etched gratings (not printed separately).
- Fab / facility: fab empty (passive fabrication sentences; authors at IEF / Paris-Sud, Multitel, UPV NTC, KTH; D80b /
  D154). No facility. No missing orgs.

## lit:xu2021c (Binary blazed GC for perfectly perpendicular coupling, OE 2021) - 2 components / 20 metrics

- `bbgc_t588` (fiber_chip_coupler.grating, soi): measured -3.69 dB at 1550.53 nm and 3-dB bandwidth about 70 nm (p.9,
  Fig. 8(b), Table 2), scope `unspecified`; simulated 1.78 dB / 66.4 %, 1-dB about 60 nm, 3-dB about 100 nm (2D FDTD,
  p.5); Table 1 design (T 588, sub-period 294, W1 57, W2 225, H3 77 nm), AFM etch depth about 77 nm (p.8), 220 nm Si,
  2 um BOX, 0 deg.
- `bbgc_w1_series` (population row, D165): IL < 4.64 dB at 1550 nm for all five W1 variants 47-67 nm (p.9, p.11; n = 5
  from the Fig. 9(a) legend).
- Not entered: simulated fabrication tolerances (26 nm period, 50 nm widths, 20 nm etch) and center-wavelength
  sensitivities (5 nm per 5 nm W1, 20 nm per 10 nm T), H1 85 nm, aspect ratio 1.35 (no parameters); Table 2 rows of other
  works (rule 3); T-series spectra (Fig. 9(b)).
- Fab / facility: fab `org_shanghai_jiao_tong_university` (first-person "we have designed and fabricated", p.11; all
  authors SJTU, parent org D154); facility `org_center_for_advanced_electronic_materials_and_devices` from "SJTU-AEMD for
  support" (p.11), borderline D80c. No missing orgs.

## lit:wang2014c (Focusing sub-wavelength GCs with low back reflections, OE 2014) - 4 components / 33 metrics

- `swg_gc_te` (soi, 220 nm on 3 um BOX, fully etched, -25 deg): measured IL 4.1 dB at the measured central wavelength
  1580 nm, 1-dB 30.6 nm, 3-dB 52.3 nm (p.9, p.11), scope `unspecified` (GC pair test structure, uncalibrated fiber /
  connector losses); back reflection 16.2 dB `author_estimate` (abstract only, origin not stated, 1550 nm inferred);
  simulated 2.2 dB / 32.5 / 58 nm (p.6); design 593 / 237 / 74 nm.
- `swg_gc_tm` (10 deg): measured IL 3.7-3.8 dB and 1-dB 45.8-47.5 nm over 11 devices (range rows, p.11, Fig. 8(b)(c)),
  3-dB 81.5 nm best; back reflection 20.8 dB `author_estimate`; simulated 2.7 dB / 57 / 92 nm; design 960 / 575 / 140 nm.
- `swg_gc_te_apodized_design`, `swg_gc_tm_apodized_design` (row_kind design): simulated minimum IL 1.6 / 1.9 dB (p.6).
- Not entered: Table 1 center-wavelength sensitivities (nm per nm), measured ripple < 0.25 dB and simulated ripple
  extinction 0.3 / 0.15 dB, simulated upward diffraction about 69 % (no parameters); Fresnel reflections 0.6 % / 17 % of
  generic shallow / regular gratings (not components); 127 um GC pitch (test-pair spacing); variant series spectra.
- Fab / facility: fab `org_university_washington` ("fabricated using electron beam lithography at the University of
  Washington", p.7; acknowledgment p.11). CMC Microsystems "provision of services" not a fab org (D425); NNIN program.
  Missing org: **Washington Nanofabrication Facility (WNF)** - facility role, lit:wang2014c p.11 Acknowledgments
  ("fabricated at the University of Washington, Washington Nanofabrication Facility (WNF)"); facility left empty.

## lit:zhu2017a (Ultra-compact SiN GC for microscopy systems, OE 2017) - 4 components / 25 metrics

- `gc_out_p620` (fiber_chip_coupler.grating, sin, suspended 220 nm SiN over a 950 nm air gap and Al mirror, 3 periods,
  632.8 nm): CE 53 % / 2.76 dB to an NA 0.65 objective (p.8, abstract), `author_estimate` (rests on the simulated 15.9 %
  input GC and a waveguide loss taken negligible from the authors' ref. [18]); geometry.
- `gc_out_p600` (optimized design, inside the fabricated period sweep, D80e): simulated 59 % with 1-dB 116 nm (NA 0.65),
  about 75 % / 1.25 dB at NA 0.95 (p.5, abstract); footprint about 4 x 2 um2 (derived 8 um2).
- `gc_in_p560`: simulated 15.9 % input coupling from a 1.5 um-waist Gaussian beam (p.7-8).
- `gc_standard_reference_design` (row_kind design): simulated 38 % and 1-dB 71 nm for a standard grating whose geometry is
  cited from ref. [5] (geometry not entered, rule 3).
- Not entered: Fig. 7 measured points of other periods (figure only; author_estimate quantity); Al reflectance 80.5 %
  (no GC parameter); Fig. 2 / 3(a)-(b) sweeps.
- Fab / facility: fab empty ("We fabricated", p.6, authors at Ghent University and TU Eindhoven; D154 / D395). No
  facility. No missing orgs.

## lit:ding2015 (GC array MCF fan-in/fan-out on SOI, OE 2015) - 4 components / 25 metrics

- `mcf_fifo_7ch` (fiber_interface.fan_out, soi): best coupling loss 3.8 dB SSMF -> MCF core (`fiber_to_fiber`,
  `author_estimate`: the free-space demux loss 1.5 dB subtracted is cited, ref. [14]; wavelength about 1540 nm from the
  Fig. 7 marker, inferred), channel variation < 1.5 dB, crosstalk > 32 dB over 60 nm, 7 channels (p.6).
- `gc_ssmf`, `gc_mcf_core` (fiber_chip_coupler.grating, apodized PhC-slot GCs with 100 nm Al mirror): simulated peak
  0.44 dB (2D EME, Fig. 3 peak near 1560 nm, inferred), 15 deg, beam diameters 10.4 / 11.8 um (`author_estimate`), widths
  12 / 13 um, slot 345 nm, 500 um taper, 49 um pitch, stack 1.6 um below (derived) / 1 um above.
- `slant_45deg` (waveguide_platform.bend, shahwar2025 precedent): 0.05 dB per slant by cut-back, 1520-1620 nm (p.5, Fig. 5).
- Not entered: measured 3-dB link bandwidth 48 nm and 1.5-dB bandwidth covering the C band (registry gap below);
  simulated 1.5-dB bandwidths 54 / 49 nm (no parameter); back reflection < 1.4 % (cited ref. [11]); demux crosstalk
  -37 dB (setup).
- Fab / facility: fab empty (passive "the device was fabricated on a commercial SOI sample", p.4; authors DTU, Rennes,
  NTT). No facility. No missing orgs.

## Judgment calls for the auditor

1. maire2008: the same chip measured before and after the top-SiO2 deposition entered as separate component rows
   (`*_clad` / `*_noclad`), not as conditions of one row (different cladding = different structure).
2. maire2008 and zhu2017a: free-space / objective-coupled gratings classed `fiber_chip_coupler.grating`; free-space beam
   resonance angles in `fiber_angle_deg` (romerogarcia2013, radulaski2018, logan2018 precedents).
3. xu2021c and wang2014c measured IL rows scope `unspecified`: both measure input-GC / waveguide / output-GC test
   structures and never say whether the printed value is halved (xu2021c Table 2 calls it the coupling efficiency;
   wang2014c Fig. 8(b) plots it against the single-GC simulation). Alternative: `loopback_half` or `per_coupler`.
4. xu2021c: AEMD facility from a generic "for support" acknowledgment (D80c borderline); etch depth entered twice
   (Table 1 `design_target` and AFM `measured` about 77 nm); BBG sub-period 294 nm as `subwavelength_period_nm`; W1 / W2
   as two `width_nm` rows with the role in `condition`.
5. wang2014c back reflections 16.2 / 20.8 dB (abstract only) `author_estimate`, 1550 nm inferred; could also be read as
   `simulated` (they match the Fig. 4 simulated reflection curves).
6. zhu2017a 53 % / 2.76 dB `author_estimate` (method `reference_structure`, input GC and waveguide in `excludes`);
   `gc_out_p600` kept `fabricated` because the Fig. 7 sweep axis covers 600 nm; `gc_standard_reference_design` row is a
   simulation of a cited geometry.
7. ding2015: 3.8 dB `author_estimate` (cited 1.5 dB subtraction) while `il_nonuniformity_db` < 1.5 dB stays `measured`
   (the same constant is subtracted from every channel); link classed `fiber_interface.fan_out` (bandwidths then
   unenterable); `box_thickness_um` 1.6 derived from the printed 800 nm SiO2 + 800 nm BPSG.

## Registry gaps (skipped value + locator, proposed definition)

- `bw_3db_nm` / `bw_1db_nm` for `fiber_interface`: ding2015 measured 3-dB coupling bandwidth 48 nm of the SSMF -> MCF
  link (p.6, Fig. 7). Proposal: allow both for fiber_interface (full width of the link transmission within 3 / 1 dB of
  its peak).
- Angular 3-dB tolerance: maire2008 about 4 deg at -3 dB (p.4, p.6); romerogarcia2013 had +/- 0.4 deg unentered.
  Proposal `angle_tol_3db_deg` (fiber_chip_coupler, free_space_emitter): incidence-angle width within 3 dB of the peak,
  full width vs +/- as printed in condition.
- Grating coupling / decay length: maire2008 Lc about 11.2 um (p.5); romerogarcia2013 decay length 17.4 um unentered.
  Proposal `decay_length_um` (fiber_chip_coupler, free_space_emitter): 1/e length of the radiated power along the
  grating, definition in condition.
- Center-wavelength sensitivity to a dimension: wang2014c Table 1 (TE 1.0 / 0.67 / 2.06, TM 0.43 / 0.35 / 0.24 nm per nm
  measured, p.9) and xu2021c (about 5 nm per 5 nm W1, about 20 nm per 10 nm T, p.9-10). Proposal
  `center_wavelength_sensitivity_nm_per_nm` (fiber_chip_coupler, wdm, resonator): center-wavelength shift per nm of the
  dimension named in condition.
- Directionality: wang2014c simulated upward diffraction about 69 % (p.6). Proposal `directionality_pct`
  (fiber_chip_coupler, free_space_emitter): fraction of guided power diffracted toward the fiber side (single value
  here; defer unless other batches confirm).
