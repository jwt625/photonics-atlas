# lit_281 batch report

Distilled 2026-11-25. Papers: lit:porcel2017, lit:wang2017a, lit:levy2011, lit:yu2005 (all Optics Express,
frequency-converter family: chi(2) SHG in Si3N4, TFLN and AlGaAs). Page-1 titles match the source rows; no correction /
erratum; no garbled text-layer flag (wang2017a p.5-6 two-column text is column-chopped in text.md: values on those
pages were read from the page render). Total 28 components / 113 metric rows. `merge_component_staging.py --dry-run`:
0 errors (the 2 warnings belong to other batches: guo2024a, ni2025b).

No org is missing from the registry: org_lionix_international, org_harvard_university,
org_center_for_nanoscale_systems, org_stanford_university, org_cornell_nanoscale_facility all exist.

## lit:levy2011 (1 component / 2 metrics)

- `cmp_lit_levy2011_sin_ring_shg` (frequency_converter.shg, sin): max conversion -35 dB (100 uW SH for 315 mW pump
  dropped into the ring, p.4; Fig. 5 top point ~25 dBm / -10 dBm) as 0.0316 % and the normalized 0.101 %/W computed
  from the printed powers; both author_estimate (OSA powers corrected with waveguide-fiber / fiber-OSA coupling
  efficiencies whose values and origin are not printed; D256a). Pump 1554.2 nm (Fig. 2(b) caption).
- Not entered: effective chi(2) up to 4e-14 m/V, range 3e-15 to 4e-14 m/V (p.6, minus signs verified on the page
  render; no parameter); C_p ~156 (p.6); slope 1.9745 +/- 0.0225; SH seen from 3 mW pump; THG "on the order of
  picowatts" at 120 mW dropped (no definite number, no THG row); ring radius 116 um and gap 350 nm (radius_um /
  gap_nm not allowed on frequency_converter); cross-section "725x1500 nm" kept in core_material only (the paper does
  not say which number is the height, so width_nm / core_thickness_nm not entered).
- Fab empty: "We design ... with the same fabrication process previously described [5, 14]" (p.3) names no org and
  has no first-person fabrication (D80b; compare turnerfoster2010 which says "designed and fabricated"). Facility
  org_cornell_nanoscale_facility ("performed in part at the Cornell NanoScale Facility", p.7).

## lit:porcel2017 (9 components / 40 metrics)

- `..._w0p9_l36` (best device): 0.4 % (53 uW at 13 mW coupled, p.1 / p.4 / p.10 / p.16-17) author_estimate (the
  waveguide-internal pump rests on the input-coupling estimate that assumes the cited 0.5 dB/cm [13], p.6); vertical
  polarization 0.349 % from Fig. 7; width / height / length.
- Width series at 36 mm (`w0p6`, `w0p7`, `w1p1`, `w1p2`) and length series at w 0.9 um (`l22`, `l60`, `l74`):
  SH power read off Fig. 7 (vector markers extracted from the PDF, +/- 0.5 uW) at the fixed 10 mW internal pump,
  stored as power_conversion_efficiency_pct = SH / 10 mW, extracted_from_figure (ayan2023 precedent); horizontal
  (te) and vertical (tm) where plotted.
- `..._population`: threshold pump P0 = 1.22 mW (linear fit of the Fig. 3(e) growth rates of four waveguides,
  author_estimate: P0 at / just below the lowest point and the internal pump rests on the assumed loss); input
  coupling ~75 % loss -> 6.02 dB per facet (author_estimate, assumed 0.5 dB/cm), output 43 % -> 2.44 dB (derived).
- Not entered (no parameter): chi(2)_eq 3.7 +/- 0.2 pm/V and kappa (Fig. 10); SH output powers in uW; growth rates
  1e-4 to 1e-2 s^-1; no degradation after a week in darkness / UV erasure (retention_time_s only for phase_shifter /
  switch_fabric); "15% of the incoming power was coupled through the waveguide" (p.1, not reconcilable with the 75 %
  input loss without a definition); Fig. 3(a)-(d) initialization traces; simulated Fig. 1 / Fig. 9 phase-matching
  widths and QPM periods; the comparison values for other works (p.17, incl. "< 0.04 pm/V" for levy2011, rule 3).
- Conflict noted: the text lists six widths (0.6-1.2 incl. 0.8 um) for "five different" widths; Fig. 7(a) has no
  0.8 um point, so no 0.8 um row.
- Fab org_lionix_international (borderline, D84b): acknowledgment thanks LioniX International staff for the mask
  design and "cleanroom processing and fabrication of the samples" (p.17); process_name "TripleX" as printed
  ("proprietary TripleX process from LioniX International", p.6; merged rows mostly spell it "TriPleX"). Cladding
  SiO2 from the p.4 platform description (not restated for these samples).

## lit:wang2017a (12 components / 51 metrics)

- `..._mpm_w630` (best modal-phase-matched device, 1 mm): 41 %/W/cm2 and 0.412 %/W (computed from 1.38 pW at 18.3 uW),
  both author_estimate: in-coupled pump rests on the 4.8 dB/facet estimate, which uses the 3.0 dB/cm loss extracted
  with an FDTD-calculated facet reflectance R = 0.147 (D608). Wavelength 1574 nm = 2 x the ~787 nm SH peak of the
  Fig. 4(c) inset (wavelength_inferred).
- `..._pgln_w670` (periodically grooved, 0.5 mm): 6.8 %/W/cm2 and 0.017 %/W (author_estimate); simulated 12.1 %/W/cm2
  (lossless), 4.6 %/W/cm2 and 0.012 %/W with the simulated losses for the same design (D80e).
- Width-series siblings from Fig. 4(c)/(d) peak reads (extracted_from_figure): mpm w580 0.21 %/W, w680 0.09 %/W;
  pgln w700 0.005 %/W, w720 0.006 %/W.
- `..._pgln_w670_wg` (waveguide_platform.other, D396 cross-row): simulated total loss 13.5 dB/cm pump, 63.5 dB/cm SH.
- Design rows (row_kind design, simulated): `..._mpm_design_w600` (60 %/W/cm2; 31 %/W at 20 mm, page render),
  `..._pgln_design_22nm_11mm` (0.16 %/W), `..._pgln_design_8nm_11cm` (2.3 %/W with an assumed 0.25 dB/cm).
- `..._tfln_wg_typical` (waveguide_platform.straight): 3.0 +/- 0.2 dB/cm (author_estimate, FDTD R; 1567-1574 nm from
  the Fig. 4(b) inset), ~10.2 dB fiber-to-fiber (measured, 1480-1580 nm axis). `..._lensed_fiber_facet`
  (fiber_chip_coupler.edge): 4.8 dB / 33 % per facet, mean over many waveguides, author_estimate.
- Not entered: Aeff 0.52 um2; input-output slopes 1.99 +/- 0.01; SH output pW values; groove period of the measured
  PGLN devices (only a "typical" 2.77 um in Fig. 3(c)) and the 80 nm groove depth (no parameter; notes); "< 0.5 dB
  with tapered fibers [39]" and "< 20 um bending radii" (cited / prospective); d33 = 27 pm/V (cited material value).
- Fab org_harvard_university + facility org_center_for_nanoscale_systems: "Device fabrication was performed at the
  Center for Nanoscale Systems (CNS) at Harvard University" (p.11, stated place, D448).

## lit:yu2005 (6 components / 20 metrics)

- `cmp_lit_yu2005_qpm_shg_5mm` (frequency_converter.shg, algaas; 5 mm, 5.8 um, QPM period 4.7 um): internal
  23 %/W (derived: 0.85 uW / (1.91 mW)^2 with the measured 45 % input coupling and a 72 % SH out-coupling), external
  ~3.4 %/W (measured, 0.61 uW at 4.25 mW in front of the facet), simulated 125 %/W lossless and 27 %/W with losses;
  input coupling ~45 % -> 3.47 dB per facet (derived); geometry incl. Fig. 1(b) cladding labels 2 / 5 um
  (extracted_from_figure, generic structure).
- `..._qpm_shg_5mm_wg` (D396 cross-row): 6.7 dB/cm at 1.56 um (measured, FP), 13-15 dB/cm at 780 nm (derived, tuning
  curve fit, D80a), ~4.4 um 1/e^2 mode width (author_estimate, origin not stated).
- Loss rows by growth: 665 C patterned 6-7 dB/cm, 665 C unpatterned 3-4 dB/cm, 725 C patterned 15-20 dB/cm,
  725 C unpatterned 2-3 dB/cm (all at 1.55 um TE, FP, measured; unpatterned rows test_structure true).
- Not entered: SHG tuning FWHM ~0.37 nm (simulated lossless ~0.19 nm) - registry gap below; SH output powers; slope
  "close to 2"; template corrugation 30-45 nm and 200-300 nm grooves; < 2 dB/cm loss variation over 6-14 um widths
  (no parameter; note on the 725 C row); earlier-work values in the introduction (rule 3).
- Conflicts (D417): abstract pump 1.568 um vs body / Fig. 3(b) tuning peak 1559.1 nm (1559.1 used); core / cladding
  composition Al0.63Ga0.37As / Al0.66Ga0.34As (p.6) vs Fig. 1(b) Al0.67Ga0.33As / Al0.7Ga0.3As.
- Fab org_stanford_university: "We have fabricated" (p.1), "we fabricated ... templates ... and grew waveguides"
  (p.3), all five authors at Stanford University. No facility.

## Judgment calls for the auditor

1. levy2011 fab left empty (process "previously described [5, 14]" without first-person fabrication); facility only.
   If the coordinator reads it as D84a ("our previous process"), fab would be org_cornell_university.
2. porcel2017 fab org_lionix_international from staff thanks for fabrication (D84b borderline); process_name
   "TripleX" as printed vs the merged spelling "TriPleX".
3. Distiller-computed %/W values not printed by the paper: levy2011 0.101 %/W, wang2017a 0.412 / 0.017 %/W
   (arithmetic on printed powers, basis inherited author_estimate). Delete if the coordinator prefers printed-only.
4. porcel2017 Fig. 7 SH powers stored as power_conversion_efficiency_pct (SH / 10 mW) for 7 sibling rows; ref_plane
   left empty (pump plane waveguide-internal, SH plane not stated).
5. wang2017a widths basis `measured` from the Fig. 4 caption "(measured at the waveguide top)"; method not stated
   (could be design_target). sidewall_angle_deg not entered: theta = 40 deg is measured from the film normal per the
   printed wt / wb / t, while the registry defines the angle to the film plane.
6. wang2017a in-coupled efficiencies author_estimate (FDTD-calculated R, D608); yu2005 internal 23 %/W derived (72 %
   SH out-coupling factor of unstated origin; author_estimate would be the stricter reading); yu2005 external 3.4 %/W
   measured (printed, no correction).
7. yu2005 free-space input coupling (aspheric lens) and porcel2017 lens coupling stored as insertion_loss_db
   per_facet on the converter rows (no fiber involved, no separate coupler row).

## Registry gaps (skipped value + locator + proposed definition)

- `chi2_eff_pm_per_v` (frequency_converter): effective / equivalent second-order susceptibility extracted from the
  device's conversion efficiency (model in notes). porcel2017 3.7 +/- 0.2 pm/V (p.1, p.16 Fig. 10); levy2011
  4e-14 m/V = 0.04 pm/V, range 0.003-0.04 pm/V (p.6).
- `bw_fwhm_nm` (or a conversion-bandwidth parameter) on frequency_converter: SHG phase-matching tuning FWHM in pump
  wavelength. yu2005 ~0.37 nm measured, ~0.19 nm simulated lossless (p.6). (Same gap as the lit_276 report.)
- `output_power_mw` on frequency_converter: generated harmonic power at a stated pump. porcel2017 53 uW at 13 mW
  (p.4); levy2011 100 uW at 315 mW (p.4); yu2005 0.85 uW internal at 1.91 mW (p.7); wang2017a 1.38 pW at 18.3 uW
  (p.10). (Same candidate as D462 / D514.)
- `radius_um`, `gap_nm` on frequency_converter (ring-based converters): levy2011 116 um / 350 nm (p.3).
- `retention_time_s` on frequency_converter (photo-induced chi(2) gratings): porcel2017 "at least a week" in darkness
  without degradation (p.11) - lower bound only.
- `qpm_period_um` (or widen poling_period_um to non-poled QPM gratings): wang2017a periodic-groove period 2.77 um
  ("typical" device, p.7 Fig. 3(c)); yu2005's orientation-pattern period is stored in poling_period_um with a note.
