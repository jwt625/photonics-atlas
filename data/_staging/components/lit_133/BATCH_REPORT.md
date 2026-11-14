# lit_133 batch report (distiller, 2026-11-14)

Family: crossing / fiber_chip_coupler. Six papers, all `restricted_local_only` in `sources.csv` (facts and locators
only). Page-1 titles checked against the source rows: all six cached texts are the paper of their row; none is a
correction / erratum. zhao2022 `garbled_text_layer` covers only page 9 (reference list); every zhao2022 value was read
from clean text and cross-checked on the page renders (p.5-p.8). Validator: `merge_component_staging.py
data/_staging/components/lit_133 --dry-run` -> +16 components, +188 metrics, 0 errors (the only warning is the
pre-existing one on merged cmp_lit_ni2025b_pimmwc-m18).

| paper | components | metric rows |
|---|---|---|
| deng2025 | 1 | 22 |
| gao2025 | 1 | 20 |
| xu2025 | 1 | 25 |
| zhao2022 | 4 | 29 |
| jin2024 | 7 | 70 |
| yi2024 | 2 | 22 |
| total | 16 | 188 |

## deng2025 (polarization-independent MMI crossing, 300 nm LNOI, Chin. Opt. Lett. 2025)

- Row: `crossing.mmi`, `lnoi_strip` (full etch of the 300 nm LN layer). Measured (normalized to a straight LNOI strip
  waveguide): IL < 0.80 dB TE0 / < 0.97 dB TM0, best 0.50 / 0.65 dB, CT > 39 / > 37 dB, best 47 / 45 dB, PDL < 0.2 dB,
  all 1480-1640 nm. Simulated (1460-1660 nm): IL < 0.27 / < 0.55 dB, best 0.12 / 0.37 dB, CT > 39.5 / > 36.3 dB.
  Geometry: MMI arm length 4.5 um, taper central widths 1.50-1.93 um (range row), 1.2 um input, 300 nm LN, 1 um
  cladding, 70 deg sidewall (Fig. 3(b) label), footprint 81 um2.
- Not entered: simulated tolerance (Fig. 4, no parameter); Table 2 values of other works; etch depth (full etch, no
  number printed); LN crystal cut (not stated).
- Fab empty (passive "is fabricated", authors at four orgs, D80b). No facility.
- Judgment calls: (1) measured IL conflicts inside the paper: abstract "< -0.96 dB" (both), Sec. 3 best -0.50 / 0.65 dB,
  conclusion and Table 2 -0.80 / -0.97 dB; Fig. 7 traces support the conclusion / Table 2 bounds, which were entered
  with the abstract value in notes (D417). (2) Scope `per_component` / method `reference_structure`, basis `measured`:
  the paper shows a single crossing and a 10-crossing cascade (Fig. 5) but never says which one gave the printed IL or
  that a division was made (D167 / D452). (3) `mmi_width_um` stored as the 1.50-1.93 um range of the 13 taper central
  widths (Table 1 mislabels the row "Length"); drop to notes if a range is not acceptable for the template.

## gao2025 (2D-Gaussian-beam-synthesis polarization-insensitive crossing, 220 nm SOI, SITRI MPW)

- Row: `crossing.other` (Gaussian-beam synthesis, same subtype as merged dumais2017 / han2022), `soi`. Measured cutback
  (20 / 40 / 60 / 80 crossings): ~0.05 / ~0.12 dB per crossing at 1550 nm (fit slopes, `measured`, D80a), 0.018-0.099 /
  0.090-0.162 dB over 1520-1580 nm, PDL < 0.104 dB, CT > 44.1 / > 38.8 dB. Simulated nominal (0.020-0.077 / 0.074-0.120
  dB, CT > 51.8 / > 43.2 dB) and with +/-20 nm width / 85 deg sidewall (< 0.19 / < 0.17 dB, CT > 45.3 / > 42.3 dB).
  Geometry: W0 500 nm, Lt1 1.529 / Lt2 1.653 um tapers, 220 nm, footprint 256 um2.
- Not entered: Ws1 / Ws2 / Ls1 / Ls2 (no role-specific crossing parameter; notes); Gaussian waist 496 / 562 nm
  (simulated, no parameter); "below 0.15 dB over a 40 nm bandwidth" (p.2; span not located).
- Fab `org_sitri` ("fabrication ... was carried out by" SITRI, p.3-4); `process_name` "SITRI standard MPW process (8-inch
  220 nm SOI, 193 nm DUV lithography)".
- Judgment calls: TM tolerance bound printed < 0.17 dB, but the Fig. 3(c) 85 deg curve reads about 0.18 dB at 1580 nm
  (noted, D417); tolerance rows use the 1520-1580 nm Fig. 3 axis as an inferred span.

## xu2025 (B-spline three-mode multimode crossing, X-cut 600 nm LNOI rib)

- Row: `crossing.other`, `lnoi_rib` (300 nm etch, 300 nm slab). Y- and Z-propagation are conditions of the one crossing.
  Measured cutback at 1550 nm: Y 0.11 / 0.22 / 0.32 dB, Z 0.19 / 0.40 / 0.53 dB (TE0 / TE1 / TE2); single-crossing CT
  structure: max IL 1.26 dB (Y, 1550 nm) / 1.42 dB (Z), worst CT -16.08 / -16.26 dB over 1500-1600 nm. Simulated: max
  IL ~0.16 dB (Y) / 0.41 dB (Z), through-port CT ~-32 / <= -22 dB, cross-port ~-53 / < -53 dB, tolerance CT < -18 dB
  (TE2). Geometry: 3.5 um top width, 600 nm film, 300 nm slab and etch, 70 deg, 4.7 um BOX, ~1 um cladding, footprint
  1120 um2.
- Not entered: Table 1 100 nm bandwidth (no crossing bandwidth parameter); MUX / DEMUX (no geometry or own values);
  control-point coordinates (not printed).
- Fab `org_huazhong_university_of_science_and_technology` as D84b borderline: passive fabrication sentence plus thanks
  to named engineers of the Center of Optoelectronic Micro & Nano Fabrication and Characterizing Facility, WNLO of
  HUST, "for the support with device fabrication" (p.5). Facility left empty (staff thanks never set a facility).
  Wafer supplier NANOLN in notes.
- Judgment calls: (1) the 1.26 / 1.42 dB "maximum IL of a single crossing" from the MUX / DEMUX crosstalk structure
  conflicts with the cutback values; entered as printed (`le`, method `unspecified`) with a conflict note; delete if
  the auditor reads them as link values. (2) The Z 1.42 dB row takes 1550 nm from the parallel Y sentence
  (`wavelength_inferred`). (3) Alternative fab reading: the facility org
  `org_center_of_optoelectronic_micro_and_nano_fabrication_and_characterizing_facility` instead of the parent.

## zhao2022 (anisotropic 1D / 2D-SWG multimode crossing, 220 nm SOI, Laser Photonics Rev. 2022)

- Rows: three-mode SWG crossing `crossing.swg` (cutback ~0.06 / ~0.16 / ~0.26 dB per crossing, mean over 1525-1605 nm;
  intermode CT < -20 dB; crossing-port CT < -45 dB; simulated < 0.08 / < 0.10 / < 0.15 dB and CT < -42 / < -60 dB over
  1400-1700 nm; W 3.6 um, L1 5 um, periods 200 / 400 nm, 220 nm, 2 um BOX / cladding, 219.04 um2); ten-mode SWG crossing
  design (< 0.37 dB, < -19 dB, 1450-1700 nm; W 12 um; 576 um2); plain 3.6 um strip crossing design (simulated 0.15 /
  0.58 / 1.54 dB, CT ~-25 dB); mode MUX + DEMUX pair reference (~1.0 dB device_total, CT < -20 dB).
- Not entered: duty cycles fD 0.45 / fC 0.75-0.5, N = 9, 50 nm minimum gap / tip (no crossing parameters; notes);
  simulated C-D coupling efficiency and N / W sweeps (design study); PIC-level ~1.0 dB with one MWC (includes the MUX
  pair); Table 2 bandwidths (no crossing bandwidth parameter) and other works.
- Fab empty (passive "was then fabricated with the fabrication process with E-beam lithography"; all authors at
  Zhejiang University, D80b). No facility.
- Judgment calls: (1) per-crossing cutback slopes `measured` (fit, D80a) although the text says "estimated"; the TE1
  value is 0.16 dB in the text but 0.15 dB/MWC on the Fig. 11 label (text value entered, D417). (2) Simulated TE1
  printed < 0.10 dB while Fig. 6(b) labels -0.13 dB (noted). (3) Ten-mode "less than ~0.37 dB" (p.6, Table 2) vs
  "less than 0.36 dB" (conclusion): 0.37 entered. (4) Strip-crossing values entered as `le` with the 1400-1700 nm Fig. 7
  axis (dotted reference lines touch the curves near 1700 nm). (5) MUX pair design comes from the authors' ref. [9];
  the ~1.0 dB / < -20 dB are this paper's own measurements (not D259); drop the row if the auditor disagrees. (6) Crossing-
  port CT < -45 dB has no printed wavelength: measurement span (Fig. 9 axes) used, `wavelength_inferred`.

## jin2024 (fabrication-constrained inverse-designed grating couplers, 220 nm SOI, Chin. Opt. Lett. 2024)

- Rows (`fiber_chip_coupler.grating`, `soi`): five EBL GCs by minimum feature size 60 / 100 / 130 / 160 / 180 nm
  (simulated CE 1.55 / 1.63 / 1.69 / 2.02 / 2.29 dB, measured 2.70 / 2.89 / 2.83 / 3.31 / 3.72 dB at ~1550 nm), the
  180 nm design made in the IMECAS 180 nm MPW with 248 nm DUV (best 2.77 dB, mean 3.2 dB, mean 3-dB bandwidth 72 nm,
  25 chips), and the EBL uniform GC reference (measured 4.43 dB, simulated 2.6 dB). Shared geometry on the designed
  GCs: 100 nm etch, 220 nm Si, 740 nm TOX (EBL rows), 14.5 deg, SMF-28 10.4 um MFD (specification), 25 periods, 350 um
  taper, 450 nm waveguide, 12 x 15 um grating area as footprint; AFM etch depth ~104 nm on the 100 nm MFS GC.
- Not entered: per-device measured / simulated 3-dB bandwidths (printed only as "changes from 70 to 67 nm" and "ranges
  from 68 to 60 nm" across the five GCs; D159); groove-width variants (+/-20 nm, CE within 0.5 dB, Fig. 8); initial
  apodized GC (MFS 30 nm, simulated -2.15 dB, p.3): its numbers equal the Table 1 entry of ref. [20] (MFS 30 nm,
  -2.15 dB), so it is treated as a cited starting design (rule 3); minimum feature size (registry gap, see below);
  0.95 dB DUV-vs-EBL difference (arithmetic on printed values); Table 1 other works.
- Fab: EBL rows `org_shanghai_jiao_tong_university` + facility `org_center_for_advanced_electronic_materials_and_devices`
  (first-person "we utilized the EBL system ... available at the Center for Advanced Electronic Materials and Devices
  (AEMD) of Shanghai Jiao Tong University to fabricate", p.4; all authors at SJTU). DUV row
  `org_institute_of_microelectronics_chinese_academy_of_sciences`, `process_name` "IMECAS 180 nm CMOS process platform,
  MPW (248 nm DUV lithography)" ("we employed the MPW service offered by the IMECAS 180 nm CMOS process platform").
- Judgment calls: (1) measured CEs come from an input + output GC structure and are printed per GC with no arithmetic:
  scope `loopback_half`, method `loopback`, basis `measured` (D452 lorenzen2026 precedent); waveguide / taper loss
  removal not stated. (2) Measured wavelength 1550 nm taken as stated ("operating at approximately 1550 nm", "central
  wavelength close to 1550 nm"); DUV and UGC rows `wavelength_inferred` from the Fig. 7 / Fig. 3 peaks. (3) UGC
  simulated -2.6 dB equals the Table 1 simulated value of ref. [23] (an apodized GC, 180 nm MFS); kept because the
  paper plots its own "UGC Sim" curve (Fig. 3) and calls the -2.6 dB the UGC CE; flag for the auditor. (4) The
  12 x 15 um grating stored as `footprint_um2` 180 (which number is width vs length is not stated).

## yi2024 (asymmetric bi-level dual-core O-band edge coupler, 220 nm SOI, Nanophotonics 2024)

- Rows: edge coupler `fiber_chip_coupler.edge` (measured 0.82-1.35 dB TE / 0.94-1.49 dB TM per EC over 1260-1360 nm,
  three structures, loop-back, FA excess loss subtracted; PDL ~0.31 dB; simulated 0.44-0.56 / 0.48-0.61 dB per facet,
  PDL < 0.097 dB, 1-dB bandwidth > 340 / > 230 nm, lateral 1-dB tolerance ~+/-1.0 um; HNA MFD ~4 um specification;
  130 nm tip, 220 / 150 nm cores, 0.38 um input, 270 um length, 3 um BOX / cladding); mode transition region
  `waveguide_platform.transition` (simulated < 0.045 dB TE, < 0.057 dB TM O-band, <= 0.25 dB at dw +20 nm; 220 / 150
  nm cores; D396 cross-note).
- Not entered: simulated sub-loss terms (mode mismatch 0.22 / 0.20 dB, expanding region 0.26 / 0.27 dB, substrate
  leakage 0.08-0.24 dB, 0.5 um gap penalty 0.40 / 0.36 dB, the 1.46 dB tolerance case); vertical 1-dB tolerance
  +/-0.9 um (registry gap, D568 candidate); conventional bi-level taper comparison (Supp. S3, not cached); reflection
  < -57.1 dB (no reflection parameter on waveguide_platform); Table 1 "Exp." bandwidth 100 nm (= SLD span); gaps wg1 /
  wg2, wb1, L1, L9 (notes; `gap_nm` is not allowed on fiber_chip_coupler and is defined as vertical for transitions).
- Fab empty (passive, all authors at Zhejiang University, D80b). No facility.
- Judgment calls: (1) per-EC measured values from the loop-back with no shown halving: `loopback_half`, `measured`
  (D452). (2) The transition row is extra (simulated only, a part of the EC); drop if the auditor prefers the EC row
  alone. (3) Simulated PDL < 0.097 dB (text) vs < 0.096 dB (Table 1). (4) Page 1 prints a CC BY 4.0 licence while
  `sources.csv` says `restricted_local_only` (registry check for the coordinator, as li2018 in D569).

## Missing orgs

None. Orgs used: `org_sitri`, `org_huazhong_university_of_science_and_technology`, `org_shanghai_jiao_tong_university`,
`org_center_for_advanced_electronic_materials_and_devices`, `org_institute_of_microelectronics_chinese_academy_of_sciences`.
Alias candidate: "Shanghai Industrial u-Technology Research Institute (SITRI)" (gao2025 p.3-4, fab) is the expansion of
`org_sitri` (registry note says the expansion was not printed in its first source).

## Registry gaps (skipped value + locator + proposed definition)

- Crossing bandwidth: deng2025 Table 2 (160 nm measured / 200 nm simulated), xu2025 Table 1 (100 nm), zhao2022 Table 2
  (> 80 / 300 / 250 nm) -> `bw_criterion_nm` on crossing: full width over which the stated IL / CT criterion holds
  (criterion in condition).
- Minimum feature size: jin2024 MFS 60-180 nm (p.3, Table 1), yi2024 130 nm (Table 1) -> `min_feature_size_nm`
  (all classes, geometry): smallest drawn feature of the design as stated (also D566 candidate).
- SWG / grating duty cycle on crossing: zhao2022 fD 0.45, fC 0.75-0.5 (Table 1) -> allow `fill_factor` on crossing.
- Lateral (in-plane) gap between the two cores of a bi-level transition / edge coupler: yi2024 wg2 0.18 um (p.3) ->
  widen `gap_nm` to fiber_chip_coupler and define lateral vs vertical in condition.
- Vertical 1-dB misalignment tolerance: yi2024 +/-0.9 um (p.4) -> `tol_1db_vertical_um` (D568 candidate).
