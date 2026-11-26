# lit_290 batch report

Batch lit_290 (DevLog-007 D780, reference-graph day 212): lit:rahim2018, lit:jalali2006, lit:rahim2016,
lit:subramanian2013. Distilled 2026-11-26 (verified_on). Dry run `merge_component_staging.py --dry-run`: +10
components, +33 metrics, 0 errors.

Page-1 title check: all four cached texts are their source rows' papers (rahim2016 prints JLT vol. 35 no. 4,
February 2017; online publication 2016-10-12, as the source row). No erratum-only file, no garbled text layer.

| paper | components | metric rows | note |
|---|---|---|---|
| rahim2018 | 0 | 0 | overview of open-access platforms; no own results |
| jalali2006 | 0 | 0 | invited review; every device value credited to cited work |
| rahim2016 | 0 | 0 | invited platform comparison; the one measured device (SiN PCG) is the authors' earlier work |
| subramanian2013 | 10 | 33 | own PECVD SiN wire-waveguide and GC measurements |

## lit:rahim2018 (Proc. IEEE 2018, open-access silicon photonics overview): 0 rows

- The paper states that its discussion "is based solely on publicly accessible information", i.e. peer-reviewed
  papers and providers' publicity (p.3). No measurement of its own.
- Table 1 (p.11, page render): foundry / platform / lithography / access / waveguide-layer thickness / wafer size per
  provider. Geometry only (layer thicknesses), no performance value: not component rows (rule 9). The table cites no
  per-row source, and the thicknesses are provider statements, not this paper's platform figures.
- Fig. 6 (p.8): qualitative 1-5 scores for submicrometer SOI, thick SOI and SiN; not physical values.
- Fig. 3 (p.3-4): chip cost per mm2 from ePIXfab member inputs; not a component metric.
- Values in the text are all cited: thick SOI ~0.1 dB/cm and Euler bends < 0.1 dB/bend (refs. [29], [74], [77],
  p.5), 20 dB/cm O-band loss of the bulk-CMOS polysilicon platform (refs. [41], [91], [97], p.6), 220 nm SOI 5 um
  bend radius (p.4, generic), 500 nm SOI "few dB per meter" (ref. [60], p.5). Not entered (rules 1 and 3).
- Orgs: none (no fabrication). The acknowledgment thanks named individuals for inputs to the text; not facilities.

## lit:jalali2006 (JLT 2006, invited review "Silicon Photonics"): 0 rows

- Every device value carries a reference: inverse-taper 0.2 dB (ref. [24]), GC 1 dB (ref. [28]), MIT SiN add/drop
  50 dB extinction and 2 dB drop loss (ref. [31], Fig. 7), Intel MOS modulator 3.3 V cm / 19 dB total loss (ref.
  [40]), Luxtera modulator and GC pair 3 dB (ref. [14]), Cornell ring modulator (refs. [44], [45]), Raman laser
  ~4 dB gain / ~8 mW (ref. [87]), microdisk 0.1 dB/cm from Q (ref. [126]), mid-IR nonlinear absorption (Fig. 20,
  ref. [124]; the authors' group, cited), Table I Raman materials (ref. [12]). Not entered (rules 1 and 3; D259 for
  the UCLA-group items).
- Own arithmetic only on hypothetical numbers (Raman gain ~1 dB/mm at 100 MW/cm2 with a 20 cm/GW coefficient, p.9;
  FCA coefficient 1.45e-17 N, p.6): not components.
- Fig. 1 silicon absorption spectrum (p.2): material property, not a component.
- Orgs: none.

## lit:rahim2016 (JLT 2017, invited SiN vs SOI comparison): 0 rows

- Measured device: the 10-channel LPCVD SiN PCG of Fig. 5 (p.8; 0.3 um SiN on 3.3 um BOX, 1 um top oxide;
  nearest-neighbour crosstalk -34 dB, central-channel IL 1.5 dB). The Fig. 5 caption credits it to ref. [43]
  (Ryckeboer et al., SPIE 2016, a co-author's earlier paper), and the text compares PCGs "demonstrated" in refs.
  [128] and [43]. Not entered (D259 / D259a / D408: the value is attributed to the earlier paper).
- Fig. 2 (p.4): "indicative" FFT of spurious reflections in oxide-clad SOI and LPCVD SiN strip waveguides
  "fabricated using the same fabrication technology at imec", no citation. Only a normalized FFT trace (Si ~-30 dB,
  SiN ~-50 dB levels by eye); no length-normalized backscatter value is stated and the registry has no
  distributed-backscatter parameter (see registry gaps). Not entered.
- Table I (p.6): typical platform values (SOI loss 1-1.5 dB/cm, SiN 0.001-0.5 dB/cm refs. [71], [39], PECVD 4.0 dB/cm
  ref. [72], backscatter -25 / -30 to -40 dB/mm ref. [67], thermo-optic and Kerr coefficients). Review values: SOI
  values carry no row citation in the table but the text gives ~1.5 dB/cm from ref. [27] (p.4). Not entered.
- Simulations of Fig. 3 / Fig. 4 (effective-index sensitivity of 0.45 x 0.22 um Si and 1.2 x 0.3 um SiN strips) and
  the Eq. (3) AWG crosstalk estimates (~-18 dB Si, ~-30 dB SiN for a 16 x 200 GHz AWG, p.7) describe generic
  waveguides / a hypothetical AWG resting on an assumed variation ratio from ref. [124]; no designed component, not
  entered.
- The paper says it details aspects already published in ref. [24] (OFC 2016 Th3J.1); D408 would keep values of a
  journal extension, but no own value remains after the D259 exclusion above.
- Orgs: none for component rows. Fig. 2 waveguides fabricated "at imec" (p.4), but no row.

## lit:subramanian2013 (IEEE Photonics J. 2013, PECVD SiN wires 532-900 nm): 10 components, 33 metrics

Components (all platform `sin`, fully etched PECVD Si3N4 strips, TE, cutback on 1-8 cm spirals with GCs at both
ends, basis measured unless noted):

| component | values |
|---|---|
| wg180_unclad_wide | 0.65 dB/cm best at 532 nm (widths > 800 nm); film 178.9 nm mean of 9 points; BOX 2 um |
| wg180_unclad_sm | 2.3 dB/cm at 532 nm (conclusion, unclad single-mode wire) |
| wg180_clad_w400 | < 1 dB/cm at 532 nm; width 400 nm; top oxide 2 um |
| wg180_clad_wide | < 0.1 dB/cm at 532 nm (beyond set-up accuracy; widths 800-1000 nm per Fig. 6(a)) |
| wg180_clad_w300 | < 2 dB/cm at 532 nm; width 300 nm |
| wg220_unclad_w700 | 1.33 dB/cm best at 780 nm; width 700 nm |
| wg220_unclad_w800 | 0.62 dB/cm best at 900 nm; wafer map: centre dies < 0.8, edge dies ~1 dB/cm, Fig. 7(b) range 0.60-1.16 dB/cm (extracted_from_figure, n 11); width 800 nm; film 220 target / 230 nm SEM; BOX 2.4 um |
| wg220_clad_w800 | 0.3 dB/cm best at 900 nm; width 800 nm |
| gc_unclad | ~7 dB/coupler typical (family, band unspecified); periods 365 / 530 / 630 nm design, 620 nm SEM; etch 70-140 nm design, 135 nm SEM; fill factor 0.45-0.6; 8 um grating waveguide; 125 um taper (532 nm) |
| gc_clad | ~6 dB/coupler (clad samples) |

Not entered and why:
- Figure-only points of Fig. 5 (unclad, all widths at 532 / 780 / 900 nm) and Fig. 6 (clad, 532 / 900 nm) other than
  the text-stated values: ~25 points with error bars; the text states the best / bound values that were entered.
  Readings quoted in component notes where they support identity (500 nm unclad 532 nm ~2.4, 300 / 400 nm unclad
  ~7.3 / ~3.2, clad 900 nm 500 nm ~0.74 dB/cm). An auditor may want them as extracted_from_figure rows.
- Family statements (unclad > 700 nm < 1 dB/cm at 532 and 900 nm; unclad 500-700 nm 1-2 dB/cm at all wavelengths;
  clad < 1 dB/cm over 500-800 nm at 900 nm, p.7): not entered on one representative row (D254), kept in notes.
- Simulated single-mode cut-off widths (532 nm: ~380 clad / ~530 unclad; 780 nm: ~630 / 900; 900 nm: ~770 / ~1100
  nm; unclad cut-off at <= 500 nm for 900 nm, p.3-4): no parameter (not a component dimension).
- Film refractive index (1.93 at 532 nm, 1.89 at 780 / 900 nm by ellipsometry) and AFM RMS roughness (0.13 nm HDP
  SiO2, 0.28 nm on 100 nm PECVD Si3N4 test films, p.5 Fig. 3): no registry parameter (see gaps).
- SEM width 485 +/- 25 nm of the nominal 500 nm wire (p.6): the 500 nm 220 nm-stack wire has no text-stated loss;
  in notes of wg220_unclad_w800 only.
- "< 3 dB/coupler" GC improvement via DBR / metal reflectors: cited work (refs. [13]-[16]); earlier PECVD results
  of refs. [9], [10] (0.5 / 0.7 dB/cm, 0.05 dB/90 deg) in the introduction: cited.

Missing fab / facility orgs: none to request. Fab is empty on all 10 rows: the paper says only "fabricated in a CMOS
pilot line" (p.2 abstract, p.9 conclusion) and passive process steps (p.4 Sec. 3) without naming the org; authors at
Ghent University-IMEC and IMEC (D80b, Contract v7; `org_imec` exists in the registry if the coordinator reads the
pilot line as imec's). process_name empty ("CMOS pilot line" names no node or flow). No acknowledgment of a facility.

## Judgment calls for the auditor

1. subramanian2013 wg180_unclad_sm: the conclusion's 2.3 dB/cm (unclad single-mode, 532 nm) is entered on a row
   without a width; the notes tie it to the 500 nm wire by the simulated ~530 nm cut-off and the Fig. 5 point
   (~2.4 dB/cm). If D159 is read strictly (width not printed with the value), the row could be moved to notes.
2. Population rows (D165): wg180_unclad_wide ("wider than 800 nm" -> 900 / 1000 nm) and wg180_clad_wide ("wider
   waveguides" -> 800-1000 nm from Fig. 6(a)). The width sets come from the figure, not the text.
3. GC family rows: one typical value (~7 dB, ~6 dB clad) stated for all GC designs at three wavelengths; entered as
   family rows with band unspecified and basis `measured` (D167: a stated per-coupler loss without arithmetic),
   method `unspecified` (extraction not described). D544 (origin not stated -> author_estimate) is the alternative.
4. Fig. 7(b) printed conflict (D417): text bound < 0.8 dB/cm for centre dies 4-7, but dies 5 / 6 read ~0.87 /
   ~0.88 dB/cm; both kept with notes.
5. Wafer-level film values (178.9 nm 9-point mean on the 180 nm lot; 230 nm SEM and 2.4 um BOX on the 220 nm
   stack) entered once each on one representative waveguide row with a cross-note, not on every row of the stack.
6. rahim2016 Fig. 2 (imec SOI vs SiN spurious-reflection FFT, uncited, "indicative") treated as no row (no
   parameter, no stated value).
7. rahim2016 PCG (Fig. 5) excluded under D259 because the caption credits ref. [43] (co-author earlier paper), even
   though the text then says the crosstalk and IL "was measured".

## Registry gaps (skipped value + locator + proposed definition)

- `refractive_index` (waveguide_platform, film index at a stated wavelength, method in notes): subramanian2013
  PECVD Si3N4 1.89 at 780 nm, 1.93 at 532 nm (p.3, p.5 Fig. 2).
- `rms_roughness_nm` (already a candidate, D418 / D432): subramanian2013 AFM 0.28 nm on PECVD Si3N4, 0.13 nm on HDP
  SiO2 over 2 x 2 um (p.5 Fig. 3).
- `distributed_backscatter_db_per_mm` (waveguide_platform, roughness-induced distributed reflection per length):
  rahim2016 Fig. 2 (p.4) has only an indicative trace; Table I values are cited (ref. [67]). Low priority.
