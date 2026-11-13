# lit_129 batch report (distill, 2026-11-12)

Papers: wu2025, vaerenbergh2021, gordillo2019, zhang2025d, tian2019. All five cached texts are the source-row papers
(page-1 titles match the `lit:` rows); none is a correction / erratum; no garbled text layer; no supplement cached.
Figure values were checked on the page renders. Validation: `merge_component_staging.py data/_staging/components/lit_129
--dry-run` -> +16 components, +118 metrics, 0 errors (the one warning printed concerns merged row
`cmp_lit_ni2025b_pimmwc`, not this batch).

## Per paper

| paper | components | metric rows | notes |
|---|---|---|---|
| wu2025 | 1 | 17 | inverse-designed perfectly vertical PSGC (measured + simulated values on the fabricated row, D80e) |
| vaerenbergh2021 | 5 | 31 | design of record (67-die WLT), inverse-designed DOE and two adjoint-inspired DOEs as population rows (D165), foundry PDK 8 deg GC |
| gordillo2019 | 2 | 5 | 3D-printed funnel connector (`fiber_interface.connector`), bare imec MPW TE GC |
| zhang2025d | 3 | 29 | MC-BG + adiabatic ADC PBS (fabricated), TM2-stripper variant (`design`), ADC TE2-TE0 block (`mode_converter.converter`, simulated only) |
| tian2019 | 5 | 36 | slot / taper-etched ADC PBS, TE-filter variant (`design`), 150-220 nm height step (`design`), TE and TM GCs |
| total | 16 | 118 | |

## Values deliberately not entered

- wu2025: simulated Hbox tolerance (peak IL within 0.27 dB for Hbox 450-580 nm, 0.33 dB at 1550 nm; p.6 Fig. 4, caption
  says 450-600 nm) and etch-bias tolerance (Fig. 5, no number): no tolerance parameter; FOM design objective (p.3);
  Table 1 comparison rows (cited, p.2); Al thickness 40 nm and 40 nm pixel size (no parameter).
- vaerenbergh2021: Fig. 4 per-design box plots (129 / 149 / 159 nm, robust designs) and Fig. 5 / Fig. 6 per-device
  values (plotted only); beam widths Fig. 7(c)-(d) (estimates resting on an assumed 9.2 um fiber MFD, p.12); wafer maps
  Fig. 8 and Fig. 9; estimates without the Hilbert envelope (1.91 dB, 18.9 / 26.9 nm, p.11); loss-budget terms (0.26 dB
  phase-front curvature, 0.1 dB Si height, p.11); 0.1 dB DI-water improvement (p.7); gauge R&R 0.3 / 0.1 / 0.2 dB
  (setup property); horn angle 24 deg, eccentricity, 65 / 63 nm minimal features (no parameter); cited values (1.0 dB
  ref. 3, 1.35 dB ref. 24, 1.5 dB ref. 5).
- gordillo2019: lateral tolerance "beyond +/-10 um" (window set by the 20 um funnel aperture, no 1-dB criterion,
  soganc2013 precedent); loss variation within 0.6 dB over 20-100 C (p.5 Fig. 3(c), no parameter); device spread of
  Fig. 3(b) (histogram only); possible 30 um pitch (no array made); funnel / waveguide widths (no role parameter, in
  notes).
- zhang2025d: grating period 390 / 120 nm, N1 / N2, gap 100 nm, L1-L4 sections (period_nm, n_periods, gap_nm,
  coupling_length_um not allowed for `polarization`; L1 entered on the ADC row); MC-BG design sweeps (Fig. 3: > 75 %
  conversion at N1 = 5, > 90 % to about 1300 nm at N2 = 25, not the final design); simulated tolerances (Fig. 6, shift
  ratio about 2.0); Table 2 "~2" dB experimental IL over the 315 nm ER > 10 dB band (approximate, kept in notes);
  Table 2 other works and the authors' earlier 336 nm result (ref. 27, cited).
- tian2019: rotated-polarization powers (TM-to-TE cross port about -20 dB measured, -18 dB simulated, others < -20 dB)
  and simulated unwanted-port transmission < -25 dB: leakage relative to input, no polarization crosstalk parameter
  (D424); slot 180 nm and gap 250 nm (gap_nm not allowed for `polarization`); simulated fabrication tolerances (p.3);
  height-step reflection "around -30 dBm" (unit as printed, no parameter on waveguide_platform); effective indices;
  Table 2 other works.

## Missing fab / facility orgs

None missing. Used: `org_cea_leti` (vaerenbergh2021 fab, p.2 / p.3), `org_imec` (gordillo2019 GC fab, p.2 "MPW run
from imec"), `org_columbia_university` (gordillo2019 connector fab, first-person sentence p.2, all authors Columbia),
`org_advanced_science_research_center_nanofabrication_facility` (gordillo2019 facility, p.6 "performed in part at").
Fab left empty (no named fabricating org): wu2025 (first-person sentence names authors at two unrelated orgs, BUPT and
Second Institute for Wuhan Ship Development & Design, p.1; p.3 refers to an unnamed "EBL foundry"), zhang2025d
(passive, p.9), tian2019 ("commercially available MPW service", p.7, no org, no node / flow for `process_name`).

## Judgment calls (for the audit)

1. wu2025 measured IL (1.05 / 1.09 dB) scope `per_coupler`, method `unspecified`, basis `measured` (D167): the Fig. 6(d)
   test path shows the PSGC with two conventional GCs and the paper never says how their loss was removed. The
   fabrication section mentions only commercial SOI, EBL and a Bosch etch; whether the fabricated chip carries the Al
   reflector / 530 nm oxide of the design (Table 2) is not stated (component notes). `mfd_fiber_um` 2.5 um entered as
   `specification` ("lensed fibers with a 2.5-um diameter", the design target).
2. wu2025 "1-dB bandwidth of PDL" 68 nm entered as `pdl_db` < 1 dB over 1490-1558 nm (no PDL-bandwidth parameter);
   simulated "100 nm" likewise as `pdl_db` < 1 dB over 1500-1600 nm.
3. vaerenbergh2021 DOR 1-dB bandwidth: Sec. 5.1 prints 20.5 nm (67-die median), abstract and conclusion 21.3 nm; 20.5 nm
   entered, 21.3 in notes (D417). In-waveguide reflection R1 -16.5 dB entered as `back_reflection_db` 16.5 `derived`
   (fringe-amplitude estimate the authors flag as approximate).
4. vaerenbergh2021 per-GC losses from loopback structures: `loopback_half`, `measured` (no halving shown, D452). The
   best-IL device of the inverse-designed DOE (1.77 dB median of 5 dies) is not stated to be the DOR, so it stays on
   the DOE population row; the DOE rows carry best / median band peaks (D165).
5. vaerenbergh2021 PDK 8 deg GC: fab `org_cea_leti` because the paper's foundry is the CEA-Leti pilot line; whether
   the GC sat on the same wafer is not stated; scope `unspecified`.
6. gordillo2019 class `fiber_interface.connector` (the paper's "connector", mechanical + optical passive alignment;
   alternative `fiber_chip_coupler.other`, 3D-printed coupler). Excess loss 0.05 dB `de_embedded`, `derived`
   (normalized to the printed 4.7 dB bare-GC peak loss; reference at 1582 nm, connector at 1544 nm). GC platform empty
   (SOI never stated, D423).
7. zhang2025d experimental IL: Table 2 prints Exp. IL "<2" dB over the 220 nm ER > 30 dB band, the conclusion says below
   0.9 dB (= the simulated abstract bound); the Table 2 value is entered with the conflict noted (D417). Table 1 vs
   text conflicts (N1 / N2 swapped; taper widths W4 / W5) kept in notes, no rows on the conflicting widths.
8. zhang2025d adiabatic ADC entered as its own `mode_converter.converter` row (fabricated on the PBS chip, simulated
   values only, D80e); TM2-stripper and tian2019 TE-filter variants as `design` rows. tian2019 150-220 nm height step
   as `waveguide_platform.other` `design` (one Si layer, xiao2022 precedent; fabrication of the step not stated).
9. tian2019 reference-normalized ILs (Eq. (1)) kept `measured` with `reference_structure` (merged majority practice);
   GC losses 5 / 7 dB per facet `loopback_half` measured (D452). PBS widths 450 / 540 nm entered as two `width_nm` rows
   with the role in `condition` (no role-specific width parameter for `polarization`).

## Registry gaps (skipped value + locator + proposed definition)

- `gap_nm`, `period_nm`, `n_periods`, `coupling_length_um` on `polarization` (zhang2025d gap 100 nm, period 390 nm,
  N1 / N2, L1 60 um, p.6-7 Table 1; tian2019 gap 250 nm, slot 180 nm, p.4 Table 1); D439 already lists these
  candidates. Proposed: widen the existing definitions to `polarization`.
- `gap_nm` on `mode_converter` (zhang2025d ADC gap 100 nm, p.6; D533 lists it).
- Polarization crosstalk / rotated-polarization leakage relative to input (tian2019 TM-to-TE -20 dB measured, p.9
  Fig. 9; D424 candidate `crosstalk_db` on `polarization`).
- `pdl_bw_nm` (fiber_chip_coupler): full width over which PDL stays below a stated level (wu2025 68 nm measured / 100 nm
  simulated at the 1 dB level, p.1 / p.2); entered meanwhile as bounded `pdl_db` rows over the range.
- Coupler fabrication-tolerance parameter, e.g. `il_tolerance_db` (peak IL change over a stated layer-thickness or
  etch-bias sweep; wu2025 0.27 / 0.33 dB, p.6): definition varies between papers, low priority.
- Temperature dependence of coupling loss (gordillo2019 within 0.6 dB over 20-100 C, p.5): rejected before (D71), not
  re-proposed.
