# lit_98 batch report (2026-11-06)

All five cached texts match their source rows (page-1 title); none is a correction, erratum or another paper. No garbled text layer flagged. katsumi2018 (arXiv v1) and niffenegger2020 (arXiv v2) are preprint texts with the journal titles and content of their source rows: accepted as the same works, journal versions unread (D430 / D433). Dry-run: +44 components, +189 metrics, 0 errors (the one warning, ni2025b m18 / m4, is an existing merged row, not this batch).

| paper | components | metrics |
|---|---|---|
| hatori2014 | 10 (fiber_chip_coupler.edge 1; chip_chip_coupler.butt 6; laser.heterogeneous 3) | 45 |
| katsumi2018 | 9 (resonator.photonic_crystal 4; chip_chip_coupler.evanescent 5, of which 2 design) | 27 |
| marinins2022 | 7 (chip_chip_coupler.butt 3; laser.dfb 3; fiber_chip_coupler.grating 1) | 39 |
| niffenegger2020 | 12 (free_space_emitter.grating_emitter 4; fiber_chip_coupler.edge 4; waveguide_platform.straight 4) | 48 |
| raptakis2024 | 6 (free_space_emitter.other 4; phase_shifter.thermo_optic 1; waveguide_platform.straight 1) | 30 |

## Not entered, and why

hatori2014
- Simulated mode-mismatch excess losses < 0.01 dB / < 0.005 dB at the two trident discontinuities (p.2, Fig. 3): partial terms of one discontinuity each; in notes.
- Calculated SOI-thickness sensitivity (+/-10 nm -> < +/-0.15 dB, p.3); "maximum coupling loss below 1 dB" and "below 4-5 dB" with the alignment accuracy (p.3, p.5): estimates, no parameter.
- Reference LD on a diamond heat sink (0.3 mW/mA, Fig. 7): the curve is the heat-sink LD with 2.5 dB coupling loss applied for comparison, not a device value.
- 104-channel source (two LD arrays, 20 / 30 um pitch, 3.2 x 1.5 mm, Fig. 9): no performance value, so no row.
- QD source power degradation vs temperature (about 1.5 dB to 85 C, 2.5 dB to 100 C at 60 mA, Fig. 13(c)) and slope efficiency vs temperature (Fig. 13(b), plot only): no parameter / plot only.
- Trident widths W1 300 nm, W2 100 nm, Wc 100 nm and the 1 um side-waveguide spacing: no registry parameter (in notes).
- LD-SSC gap about 1 um: gap_nm is defined as a coupling gap; left in notes.
- Optical link with the Si interposer (refs. [2], [21]): other papers of the authors, not entered (rule 3).

katsumi2018
- Single-photon-source metrics (eta beta 63 / 74 / 52 %, beta 87 / 80 / 57 %, g2(0) 0.23 / 0.24 / 0.25, decay rate 3.83 ns-1, Purcell, 1.5 nm phonon-assisted width): no registry slot (mnaymneh2018 precedent); in notes.
- Placement accuracy (< 100 nm, < 1 deg) and simulated misalignment robustness (eta 99.5 % at 200 nm offset, > 99 % at 10 deg): no parameter; in notes.
- Simulated Q of the Si / SiN design variants (2310, 7900): resonator values of design-only variants; in notes.
- Hole radius 53 vs 59.8 nm printed inconsistently (p.19 vs p.21) and no registry parameter.
- Achievable eta beta estimates of Supp. S10 and the > 50,000 Q of ref. [10] (cited own work, rule 3).

marinins2022
- Placement accuracy (x / y 3 sigma 254 / 284 nm, means 26 / 13 nm, n = 51), tilt (< 0.003 / 0.03 deg), cycle time 25 s: no parameter; in notes.
- Simulated misalignment tolerances (Fig. 3(b), (c)): the X / Y / Z axes are not defined in the text against lateral / longitudinal (D156); placement specs and the 0.05 / 0.09 deg pitch / roll limits are design specs.
- Simulated Fig. 3(a) loss for the 400 / 450 nm tips: not read (simulated curves; text values entered for 350 nm).
- Normalized thermal resistance 26.6 K mm/W, feedback coefficient C 0.56, upper linewidth "tens of MHz", shear strength (87.8 / 36.5 gf, 828.6 gf/mm2), MSL1 result, thermal-expansion displacement: no parameter / qualitative.
- SiN GC insertion loss: measured on a reference structure but not printed.

niffenegger2020
- SiN propagation loss < 0.5 dB/cm above 633 nm, about 10 dB/cm at 405 nm (p.22): the sentence points to the authors' platform paper (ref. [20]); D80i.
- In-vacuum feedthrough (3 dB) and cool-down (about 7 dB) losses and the 26.4-35 dB totals (Table I): system / packaging terms, 1092 nm values inferred by the authors; in edge-coupler notes.
- "Grating efficiencies approximately 10 %" (p.4) and the design beam sizes (about 11 um / 4-7 um, p.15): stated once for all gratings (D254); per-grating losses and ion-measured diameters entered instead.
- Beam crossing height 65 um (vs 55 um ion height): no parameter (focus / crossing height); emission angles not printed.
- Ion-physics results (detection fidelity, Ramsey decay, heating rate, pi-pulse time): not component metrics.
- Fig. 5 labels (150 um taper, 20 x 20 um grating) belong to "one of the grating couplers" (unnamed); in notes only.

raptakis2024
- Main-lobe power ratio (Fig. 3(c)) and per-angle SLS / FWHM curves: plot only.
- Thermal crosstalk < 5 % beyond 60 um (expectation with ref. [15]); tuning time about 2 ms (definition not stated).
- Uniform 6 um pitch reference array: theoretical curves and the authors' earlier work [18] (rule 3).
- Table I comparison rows: other works.

## Organizations

- Missing from the registry (facility): TIA-SCR (Tsukuba super clean room), operated by AIST, Tsukuba, Japan (hatori2014 p.7 acknowledgment: technical support and device fabrication); also wanted for konoike2022 (D453, "AIST SCR"). Would go on the 7 Si-side hatori2014 rows.
- Missing (vendor / maker): QD Laser Inc., Japan (hatori2014 p.5: QD LD fabricated there). Sivers Photonics, Glasgow, UK (marinins2022 p.3 Sec. II-B: DFB lasers manufactured on its InP100 platform; fab org for the 3 laser.dfb rows once registered).
- hatori2014 fab org AIST on the Si-side rows is borderline (D84b analogue: fabrication thanks to an AIST unit; the "we fabricated" sentences span PETRA / AIST / University of Tokyo). Laser rows left empty.
- katsumi2018 fab org_the_university_of_tokyo (first-person fabrication, all authors in UTokyo units; D154).
- raptakis2024 fab org_fraunhofer_heinrich_hertz_institute ("fabricated using the polymer-based platform of HHI"; D455 analogue, borderline).
- marinins2022 and niffenegger2020: fab empty (no fabrication sentence naming an org; D80b).

## Judgment calls

1. hatori2014 trident SSC: one fiber_chip_coupler.edge row (lensed-fiber chain test, geometry) and separate chip_chip_coupler.butt rows for the LD test coupling (polished facet), the flip-chip mounted interface (dry-etched facet, unfilled gap), and the 1.3 um design (D396; facet process and design differ). Tip-width series of Fig. 6 / Fig. 12 entered as population rows (D165) with figure-read ranges.
2. hatori2014 0.92 / 0.94 dB lensed-fiber losses scoped per_facet, measured (D167): the Fig. 4 intercept (about -1.85 dB) covers two facets; the halving is not shown. The 0.55 / 0.24 dB per-SSC slopes are per_component, cutback.
3. hatori2014 flip-chip FP LD sources classed laser.heterogeneous (mu2026 precedent for flip-chip FP LDs on a PIC); waveguide-referred slope efficiency and > 2 mW output author_estimate (referencing not stated, D460 / D431). QD source platform empty (QD material not stated, D422). The 52-port light source is a separate row from the Fig. 7 I-L row (the text does not tie Fig. 7 to the 52-port chip). Paper cites "Fig. 12" for Fig. 13(a) (noted, D417).
4. katsumi2018: cavity and waveguide made separately and joined by transfer printing -> chip_chip_coupler.evanescent (not transition, unlike mnaymneh2018 where the waveguide was defined under the placed nanowire). Each printed cavity has a resonator.photonic_crystal row (Q) and a coupler row (eta) (D396). eta_exp 72 / 92 / 93 % derived (Eq. (3) model extraction with a stated assumption, D80a), although the uncoupled Q is the average of other cavities on glass; an audit may prefer author_estimate. Cavity L / R wavelengths read off Fig. 5 (inferred flag set).
5. marinins2022: one coupler row per SiN tip width (350 / 400 / 450 nm, sibling designs); the text's 1.5 +/- 0.5 dB is entered on both the 350 and 400 nm rows because the sentence names both; Fig. 6(a) after / before underfill min-max ranges entered per tip (extracted_from_figure). Coupling loss derived (LD power before vs fiber power after, GC loss calibrated out). Output powers derived (waveguide-referred via the GC reference, D394). Thermal resistance derived (ratio of fitted slopes, maeda2023 precedent). Bare-die and earlier-run assemblies as separate laser.dfb rows (theurer2019 precedent).
6. marinins2022 SiN GC back-reflection 14 dB measured (Fabry-Perot ripple of a reference waveguide, D394), band c_band inferred.
7. niffenegger2020: per-path rows for the four pathways (grating, edge taper, routing waveguide). Grating and OCC losses derived (subtraction / halving stated in Methods G); OCC scoped loopback_half (two facets of a straight test waveguide, propagation removed); routing-waveguide path losses derived (per-length loss times length). Only the 674 nm FTO 21.4 dB is printed as a total (device_total, measured). Ion-measured 1/e2 beam diameters entered in beam_diameter_um with direction and height in the condition (D451).
8. raptakis2024 OPAs as free_space_emitter.other (chen2024 / chung2017 precedent); "SLS" entered as slsr_db; beam FWHM averages in beam_divergence_deg; the +/- 10 deg characterized span as steering_range_deg 20 measured. Single-emitter theta_3dB 6.3 deg author_estimate (origin not stated). Platform propagation loss about 0.7 dB/cm author_estimate (no measurement shown).

## Registry gaps (proposed)

- `placement_accuracy_3sigma_um` on chip_chip_coupler (marinins2022 254 / 284 nm x / y, n = 51; tanaka2012 merged notes): post-bond placement spread, axis in condition.
- Single-photon-source metrics on a source class (katsumi2018 eta beta 63 / 74 / 52 %, g2(0) 0.23-0.25; mnaymneh2018): e.g. `single_photon_coupling_efficiency_pct`, `g2_zero`.
- `thermal_resistance_length_k_mm_per_w` on laser (marinins2022 26.6 K mm/W): length-normalized thermal resistance.
- `focus_height_um` on free_space_emitter (niffenegger2020 65 um crossing height): height of the beam focus / crossing above the chip surface.
- `facet_gap_um` on chip_chip_coupler (hatori2014 about 1 um, marinins2022 500 nm model gap): LD-to-PIC facet distance of butt coupling (gap_nm is defined as a coupling gap).
