# Batch lit_323 report

Papers: lit:michaels2018 (Optics Express 26, 4766, 2018), lit:papes2016 (Optics Express 24, 5026, 2016), lit:dai2011a
(Optics Express 19, 18614, 2011). Distilled 2026-11-28. Validation: `merge_component_staging.py
data/_staging/components/lit_323 --dry-run` -> +6 components, +63 metrics, 0 errors (the 2 warnings are in other
batches: guo2024a, ni2025b).

Page-1 title check: all three texts match their source rows. None is a correction or erratum. Text layers are clean
(`garbled_text_layer` false). All three are simulation / design papers, so every row is `row_kind: design` and has no
fab, facility or process. None of the papers states a fabrication or a facility, and the acknowledgments name only
funding programs (ONR; Czech ministry grant, NRC Canada and SRDA support; DARPA MTO CIPhER), none of which is entered.

## lit:michaels2018 (2 components / 18 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_michaels2018_pvgc_ideal | fiber_chip_coupler.grating | soi | CE 99.2 % / IL 0.035 dB per_coupler at 1550 nm (p.7-8); back reflection 43 dB (chip-to-fiber, p.11) and 44 dB (fiber-to-chip, p.12); 1-dB BW ~24 nm (p.11); target MFD 10.4 um, fiber angle 0 deg, 26 periods, 220 nm film |
| cmp_lit_michaels2018_pvgc_65nm | fiber_chip_coupler.grating | soi | CE 96.9 % / IL 0.137 dB (p.10); back reflection 41 dB (chip-to-fiber) and 37 dB (fiber-to-chip); 1-dB BW ~24 nm; same geometry rows |

All values come from 2D FDFD simulation and are `simulated`, TE input, 1550 nm (stated). The target fiber MFD is
`author_estimate` because the paper takes a Gaussian beam as the approximate SMF mode (cheben2015 precedent). The
Fig. 5 caption prints 10 um and the text prints 10.4 um; 10.4 um is entered and the difference is noted.

Values not entered and why:
- Fig. 8: efficiency vs minimum feature size (0-180 nm). Each point is a separate constrained design. Only the 65 nm
  point is labelled, and the others would need both x and y read off the plot. "Better than -0.5 dB out to a minimum
  feature size of over 130 nm" (p.10) does not tie the bound to one design (D159 / D156).
- "-20 dB bandwidth of only 8 nm" for the back reflection (p.12): the sentence does not say which design it refers to
  (D159), and there is no reflection-bandwidth parameter.
- Mode match "over 99 %" (p.8): the same quantity as the 99.2 % efficiency.
- Starting structure (uniform grating, period 586 nm, duty factor 80 %, layer shift 160 nm, 48 % efficiency, p.6): this
  is the optimizer's starting point, not a proposed design. It is in the component notes.
- Chirped period / duty factor per period (Fig. 7): curves only, not entered.
- Minimum feature size 65 nm as a geometry value: no parameter.

Judgment calls: platform `soi` (single 220 nm Si film etched from top and bottom, SiO2 clad on both sides). The
110 nm layer thickness is kept in core_material and the condition, with no etch_depth row (the paper does not call it
an etch depth). Both back-reflection directions are entered as separate rows, with the excitation in condition.

## lit:papes2016 (3 components / 38 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_papes2016_ec_hna_design1 | fiber_chip_coupler.edge | silica | overall CE 90.7 % / 0.42 dB per_coupler (3D-FDTD, 1550 nm, p.9); facet overlap 94.5 % per_facet (p.6); eta2 96 % (FDTD) and > 95 % (EME, 255 um) on_chip_excess; WDL < 0.2 dB 1450-1600 nm; 1-dB tolerance 1.3 um; MFD 6.6 x 4.77 um; fiber MFD 6 um; geometry (tip 150 nm, end 270 nm, taper 260 um, rib 8.75 um, tclad 5 um, d 3 um, Si3N4 20 nm, SWG pitch 500 nm, BOX 3 um, Si 220 nm) |
| cmp_lit_papes2016_ec_smf28_design2 | fiber_chip_coupler.edge | silica | overall CE 84 % / 0.75 dB per_coupler (3D-EME, p.12); overlap 92.6 % per_facet; eta2 90.5 %; WDL < 0.2 dB; 1-dB tolerance 2.2 um; MFD 10.8 x 8.4 um; fiber MFD 10.4 um; geometry (tip 150 nm, length 1500 um, rib 14.15 um, tclad 11 um, d 6.5 um, Si3N4 30 nm, BOX 3 um) |
| cmp_lit_papes2016_ec_hna_homog_sin | fiber_chip_coupler.edge | silica | eta2 91 % with unpatterned Si3N4 layers (p.11) |

Values not entered and why:
- 2 um BOX: 0.4 dB lower efficiency for design 1 (p.13). Only the penalty is printed and no parameter holds a delta, so
  it is noted on design 1 and no 2 um BOX row was made.
- Homogeneous-Si3N4 variant: 0.23 dB penalty on the overall efficiency (p.11). Only the penalty is printed, so no
  absolute overall loss is computed. It is noted on the variant row.
- Fiber offsets x0 / y0, SiO2 spacer thicknesses (Table 1), Si3N4 strip lengths (50 / 200 um; 1320 / 660 / 165 um):
  no matching parameters, kept in component notes / core_material.
- The intro's comparisons with refs [14]-[19] are cited work.

Judgment calls:
- Platform `silica`: D82f puts the edge coupler on the layer at the fiber-facing facet, which is a SiO2 rib whose
  index is raised by thin Si3N4 layers. su2026 is the precedent; the full stack is in core_material. If the
  coordinator prefers `soi` (Si inverse taper, fang2010 / cheben2015 precedent), only the platform field changes.
- Facet overlap is stored as coupling_efficiency_pct `per_facet` (cheben2015 precedent). The taper transformation
  efficiency eta2 is stored as coupling_efficiency_pct `on_chip_excess`, with includes / excludes saying it leaves out
  the facet overlap (cheben2015 m6 used on_chip_excess for the taper term).
- The FDTD design gives a 260 um coupling length (p.7) and the EME nominal structure 255 um (50 + 205 um, p.10). Both
  are treated as one design: values sit on the same row and the difference is noted.
- Wavelength: the FDTD values are tied to 1550 nm (Fig. 7 caption). Overlap and EME values print no wavelength, so they
  get 1550 nm with `wavelength_inferred: true` (indices given near 1550 nm; design centred at 1.55 um).
- 1-dB alignment tolerance is stored as tol_1db_lateral_um. The paper does not say which transverse axis, or whether
  the value is a half or full width (noted).
- Fiber MFDs 6 um (HNA) and 10.4 um (SMF-28) are `specification` (the design-target fibers are named purchased fiber
  types, rule 4).
- Rib etch depths 3 / 6.5 um are stored as etch_depth_nm 3000 / 6500 `derived` (unit conversion, D157).

## lit:dai2011a (1 component / 7 metric rows)

| component | class | platform | metrics |
|---|---|---|---|
| cmp_lit_dai2011a_bent_dc_pbs | polarization.pbs | soi | PER > 10 dB over ~200 nm (1450-1650 nm, inferred from the Fig. 6 axis); IL ~0.07 dB TM cross / ~0.15 dB TE through at 1550 nm read off Fig. 6 (simulated, D454); length 9.5 um; widths 460 / 534 nm; Si 220 nm |

Group check (D259 / D408): this paper does not reproduce values from the authors' earlier work. Refs [14], [26] and
[28] (Dai / Bowers) are cited only in the introduction, and ref. [31] (linewidth uniformity) is an input to the
tolerance assumption. Only this paper's own simulated design is entered.

Values not entered and why:
- Coupling-region length 4.5 um and gap 203 nm: coupling_length_um and gap_nm are not allowed for class polarization
  (registry gap below). Both are in the component notes.
- Bend radii R1 19.3 / R2 20 / R3 18 um and through-port R0: radius_um and min_bend_radius_um are not allowed for
  polarization. R0 is printed as 4 um (p.4) and 3 um (p.5); the conflict is noted and not resolved.
- Waveguide-width tolerance +/-60 nm (Fig. 7): no parameter, noted.
- ER as one number per port at 1550 nm: the linear plot cannot resolve a near-zero unwanted-port power, so no reading.

Judgment calls: per_db range endpoints come from the Fig. 6 axis (1.45-1.65 um = 200 nm), with `wavelength_inferred`.
By eye the TM0 ratio at 1.45 um is about 9.5 dB, so the edges are approximate (noted; the printed value is "about
200 nm"). Upper cladding is not stated, so cladding is left empty.

## Missing fab / facility orgs

None. No paper states a fabrication or a facility.

## Registry gaps

1. `coupling_length_um` and `gap_nm` for class `polarization` (DC-based PBS / PSR). Skipped: dai2011a 4.5 um and
   203 nm (p.5, Fig. 5 caption). Proposal: allow both for polarization, with the definitions they have for splitter.
2. `min_bend_radius_um` / `radius_um` for class `polarization`. Skipped: dai2011a R2 20 um / R1 19.3 um (p.5). Proposal:
   allow `radius_um` for polarization, with which arm in condition.
3. Extinction-ratio bandwidth (full width over which the PER stays above a stated level). Skipped: dai2011a ~200 nm
   for ER > 10 dB (p.6). Here it is entered as per_db > 10 dB with a wavelength range instead. Proposal: `per_bw_nm`,
   level in condition. Defer unless more rows need it.
4. Back-reflection bandwidth (full width over which reflection stays below a level). Skipped: michaels2018 "-20 dB
   bandwidth of only 8 nm" (p.12; design identity ambiguous anyway). Defer.
5. Minimum feature size of a design (lithography constraint). Skipped: michaels2018 65 nm (p.10). Defer.
