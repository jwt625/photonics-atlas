# Batch report lit_59 (crossing, fiber_chip_coupler, polarization), 2026-10-30

Papers: mekis2010, ma2013, chiles2017, fang2010, liu2011, guan2014a, bogaerts2007. All seven are
`restricted_local_only` (facts and locators only). Page-1 titles and authors match the source rows. None is a
correction or erratum, and none is flagged `garbled_text_layer`. No existing component rows for these papers.
Page renders read: bogaerts2007 pp.1-3, ma2013 p.6, chiles2017 p.5, guan2014a pp.3-4, mekis2010 Fig. 6 (p.6), p.8,
Fig. 14 (p.9).

Dry run: `batch lit_59: +27 components, +156 metrics; errors 0`. The only WARN is the pre-existing
cmp_lit_ni2025b_pimmwc-m18.

## Per paper

| paper | components | metrics | rows |
|---|---|---|---|
| bogaerts2007 | 1 | 8 | double-etch parabolic crossing (crossing.other) |
| ma2013 | 4 | 37 | 1550 and 1310 nm PSO crossings (crossing.other); OPC test crossing without / with OPC (2 rows) |
| chiles2017 | 8 | 39 | interplane coupler, best measured design + simulated design (waveguide_platform.transition, skill rule 10); P1/P2 and P1/P3 crossings (crossing.multilevel); three R = 30 um rings, one per plane (resonator.ring); a-Si slab film (waveguide_platform.other) |
| fang2010 | 4 | 24 | suspended SiO2 + bilevel Si nano-taper converter (edge); 30 nm-tip simulated design row; SiO2-clad nano-taper reference (edge); Si wire loss (waveguide_platform.straight) |
| liu2011 | 1 | 6 | air-clad two-wire PSR (polarization.psr) |
| guan2014a | 6 | 34 | 1310 nm PSR; sub-elements DC PBS (polarization.pbs), bi-level TM0-TE1 taper and asymmetric-MZ TE1-TE0 converter (mode_converter.converter, simulated only, row_kind fabricated per D80e / lu2015); TE and TM SPGCs (grating) |
| mekis2010 | 3 | 8 | focusing apodized SPGC (C band); diamond-scatterer PSGC (S band); library directional coupler from wafer-scale cascades (Fig. 14, figure-read) |

## Values deliberately not entered

- **bogaerts2007**
  - The abstract's "97.5 % (-1.7 dB)" is a typo. The body and Fig. 4(b) give -0.16 dB, which matches 97.5 %.
  - 2-D EME transmissions of the comparison crossings (Fig. 1(a)-(c): 67.6 / 61.6 / 31.9 %): these are reference designs following ref. [4], not this paper's components.
  - Ref. [4] values.
  - The 440-550 nm width sweep: "similar" performance, no numbers.
  - Shallow etch depth: not stated.
- **ma2013**
  - 3D-FDTD FOM values (p.5). The FOM is TE0 transmission minus crosstalk and reflection, so it is not a crossing loss.
  - FOMs for 250 / 300 nm Si.
  - Simulated maximum reflection -28 dB: no crossing parameter.
  - The authors' earlier crossing, -0.18 dB (ref. [6], D259).
  - 1310 nm headline "< -37 dB" crosstalk: contradicted by the five-die range of -34.1 to -43.6 dB. The five-die values are entered instead.
  - Table 1 taper widths w2-w12: no role parameter, listed in notes.
- **chiles2017**
  - Interplane gap: the paper gives pitch (900 nm design, ~700 nm measured) but does not define pitch vs gap (D159 spirit).
  - IPC wmin / wmid and L1 / L2: Fig. 4(b) does not assign them to a tip / lower-tip / taper role (D102). They are in notes.
  - Co-propagation crosstalk between planes: -4.8 +/- 0.7 dB (P1/P2, equal widths, 16 um), -12.5 +/- 0.7 dB (P1/P2, dw = 80 nm, 58 um), -35 +/- 0.7 dB (P1/P3, 25 um) (p.7). No class / parameter fits (registry gap below).
  - Simulated crosstalk values (< -33 dB with offset; 34.5 / 2.8 / 6.7 dB).
  - The 2 um-pitch "< 19 dB" design statement.
  - Crossing stub pitch 3 um: a test-structure spacing (pitfall).
- **fang2010**
  - Si nano-taper length: not stated.
  - SiO2 lateral taper (6 -> 2 um over 60 um) and terminated taper (300 nm tip, 1 um x 50 um): overlay tapers with no role parameter, in notes.
  - Simulation input MFD 6 um: setup input, in condition.
  - Tip-width sweep points in Fig. 2(b), apart from the 30 nm and 110 nm values printed in the text.
- **liu2011**
  - w1 600 / w2 333 nm widths and the 100 nm gap. width_nm would be ambiguous, and gap_nm is not allowed for polarization. Both are in core_material and notes.
  - 15 nm/nm width sensitivity: simulated, and the Fig. 5 caption (w2) contradicts the text (w1).
  - Fig. 8 repeatability: no values.
- **guan2014a**
  - DC gap 220 nm and Lc 10 um (gap_nm / coupling_length_um not allowed for polarization). The source also reuses the symbol W2 for 620 nm.
  - Bi-level taper section widths (in notes).
  - The +/-0.2 dB five-die spreads (in notes; the statistic type is not stated).
- **mekis2010**
  - 8 deg fiber polish angle: the tilt from the normal is not stated.
  - Back-end loss 0.1 dB typical: no parameter.
  - Analytic apodization overlap loss 0.5 dB: a model, not the device.
  - First trench width 158 nm: no role parameter.
  - PSGC "minimal PDL over > 30 nm": no number.
  - Circular-hole PSGC: no values.
  - Tester gage capability (0.1 dB / 4 nm): equipment.
  - Transceiver die: EO / system metrics, none printed.
  - Individual DC wafer points.

## Fab / facility orgs missing from the registry

- **OpSIS** (MPW access service), ma2013 p.5 Sec. 2.3: "through an OpSIS multi-project-wafer run" next to IME A*STAR. This is a fab role under D398. Also raised in lit_49 (simard2013) and D418. guan2014a cites OpSIS only as a grant program (p.1), so it is not entered there.
- **Boulder Microfabrication Facility** (NIST, Boulder, CO, US), chiles2017 p.4 Sec. II: the platform was prototyped there. Facility role, parent org_national_institute_of_standards_and_technology.
- **Freescale Semiconductor, Inc.**, mekis2010 p.2 Sec. III A: the Luxtera process is based on Freescale's 0.13 um CMOS process, and wafers are processed in "the fab". This is the candidate fab org for all three mekis2010 rows; fab_org_ids is left empty until it is registered.

## Judgment calls

1. **bogaerts2007 fab = org_ghent_university + org_imec.**
   - Basis: "We fabricated" (p.2), and all authors are at "Ghent University - IMEC" (vandekerckhove2025 precedent).
   - Alternative: org_imec only, following bogaerts2007a / pathak2014 for 248 nm DUV on 200 mm wafers. That precedent also leaned on a P-line acknowledgment, which this paper does not have.
2. **liu2011 fab = org_technical_university_of_denmark.**
   - "We fabricated" (p.5), and every author lists DTU Fotonik (two also list SCNU / HUST). DTU is the unambiguous common org (D154 analogue).
3. **chiles2017 fab = NIST.**
   - The platform was prototyped at NIST's Boulder Microfabrication Facility, and all authors are at NIST. D83c analogue: facility owner = fab org. The facility row itself is missing (see above).
4. **guan2014a fab empty.**
   - The fabrication is described passively, and the authors are at NUS, University of Delaware and IME (D80b).
5. **ma2013 crossings as crossing.other.**
   - These are PSO-shaped multimode tapers with no MMI section (zhang2025 precedent), not crossing.mmi as with lu2016a.
6. **ma2013 OPC crossing as two rows (mask without / with OPC).**
   - These are separate physical devices (rule 9). Geometry and wavelength are not stated (band unspecified).
7. **ma2013 crossing-loss wavelength.**
   - The slope is taken at each cascade's fitted spectral peak, and that peak is not printed. Entered as band c_band / o_band with wavelength_inferred.
8. **ma2013 wdl_db values are `derived`.**
   - The authors' arithmetic is explicit: 55-crossing spectrum minus the GC loop, divided by 55 (D80a / valdez2025 ruling).
9. **ma2013 "+/-" terms entered as statistic std.**
   - The source does not name the statistic.
10. **ma2013 crosstalk.**
    - The five-die mean is entered with `gt`, because every value is at the noise floor.
    - The range rows carry no qualifier and have a note instead.
11. **guan2014a crosstalk "better than 20 dB" entered as per_db.**
    - The definition (wrong input mode at an output port) is in condition, following the lu2015 / cheng2023 precedent.
    - The gao2026 audit instead listed PSR crosstalk as a gap (crosstalk_db for polarization). If that ruling prevails, delete guan2014a psr_1310-m6.
12. **guan2014a sub-elements.**
    - Entered as rows with simulated values only, as row_kind fabricated (lu2015 / D80e).
    - The asymmetric-MZ "efficiency larger than 1.13 dB" is read as a worst-case loss. This is consistent with the printed total 1.57 = 0.08 + 0.36 + 1.13.
13. **guan2014a SPGC 7.6 / 8.9 dB as loopback_half, measured (D167).**
    - These are per-coupler values from averaged loops; Fig. 6 loop peaks are about -15 / -18 dB.
    - The PSR losses normalized with these loops are `derived` (cheng2023 ruling).
14. **chiles2017 ring propagation loss 7.4 dB/cm is author_estimate.**
    - It is computed from a loaded Q with an unstated coupling regime and group index (D403 analogue).
    - The FSR of ~425 GHz is stated once for the three identical rings and entered on each ring row with a note. If D254 is read strictly, move it to notes.
15. **chiles2017 ring Q wavelengths.**
    - Entered as the Fig. 3(b) axis span (1535-1536.2 nm) for all six Q rows.
    - The crossing loss uses the setup's nominal 1540 nm (p.4).
16. **mekis2010 SPGC std 0.1 dB.**
    - It refers to "the coupler used in transceiver modules", inside the paragraph on this SPGC.
    - Kept on that row with a note (identity borderline, D159).
17. **mekis2010 figure readings.**
    - bw_1db_nm SPGC ~30 nm and PSGC ~27 nm (+/-2 nm).
    - DC excess loss ~0.02 dB, from the Fig. 14 lot-mean lines (+/-0.001 dB).
18. **fang2010 post-trim dimensions as design_target.**
    - Tip 110 nm and waveguide 450 nm are process values with no stated measurement.
19. **fang2010 SiO2-clad nano-taper reference row.**
    - It is measured in this paper with the same fibers ("similar to" ref. [17]).
    - Its values are stated once for TE and TM, so polarization is `both`.

## Registry gaps (proposed definition; skipped value + locator)

- **`crosstalk_db` for waveguide_platform** (or a new `interplane_crosstalk_db`): "maximum fraction of power transferred between co-propagating waveguides on different layers over the stated length, positive dB (length in condition)". Skipped: chiles2017 4.8 / 12.5 / 35 dB at 16 / 58 / 25 um (p.7 Sec. III D, Fig. 6(b)).
- **`gap_nm`, `coupling_length_um` for polarization** (already confirmed in the lit_27 audit). Skipped:
  - liu2011 gap 100 nm and w1 / w2 600 / 333 nm (p.3);
  - guan2014a DC gap 220 nm and Lc 10 um (p.2).
- **Role widths for two-waveguide PSRs** (e.g. `width2_nm`, "width of the second (narrow / coupled) waveguide"). Skipped: liu2011 333 nm (p.3).
- **`back_reflection_db` for crossing**. Skipped: ma2013 simulated maximum total reflection -28 dB (p.5, Fig. 2(b)); simulated only, low priority.
- **`fiber_polish_angle_deg` for fiber_chip_coupler**. Skipped: mekis2010 8 deg (p.5). It is distinct from the tilt in fiber_angle_deg; one value, low priority.

## Open questions

1. Register OpSIS (fab role, D398), the Boulder Microfabrication Facility (facility) and Freescale Semiconductor (fab, mekis2010)?
2. bogaerts2007 fab: both Ghent University and imec, or imec only?
3. PSR crosstalk: per_db with a definition (guan2014a, as entered) or a registry gap (gao2026)? The answer sets one rule for both.
