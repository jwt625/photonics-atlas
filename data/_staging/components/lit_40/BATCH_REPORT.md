# Batch lit_40 report (distill subagent, 2026-10-29)

Dry-run `batch lit_40: +27 components, +103 metrics; errors 0` (the only WARN printed concerns merged row
cmp_lit_ni2025b_pimmwc, not this batch). ASCII, no e-mail, no quotes. All seven cached texts match their source rows
(page-1 title / authors); no garbled text layer. Not audited or merged.

## Per paper (components / metrics)

- dangel2018 (5 / 29): Si taper to directly processed SM polymer waveguide (waveguide_platform.transition, Lc 0.2-2.8 mm
  family: < 1.1 dB TE / < 0.5 dB TM over 1270-1370 nm for Lc 1.6-2.4 mm, geometry); flip-chip Si taper to PWG on glass
  (chip_chip_coupler.evanescent, mu2016 precedent: < 1.4 / < 0.6 dB at 1310 nm, < 1.5 dB O + C band, 1-dB lateral
  tolerance ~2 um, back-reflection > 45 dB); fiber-PWG-SiWG interface (fiber_chip_coupler.other: IL/facet < 3.5 / < 3.0 dB,
  mean 3.4 / 2.5 dB over 50 I/Os, 94 coupler I/Os, 50 um pitch); SMF-PWG butt coupling (~0.3 dB typical; 0.5 dB budget
  term author_estimate); test-polymer PWG ~1.5 dB/cm. Fab org_ibm_research_zurich ("we structured" the SOI wafers;
  own PWG technology, D84a). Not entered: former-formulation PWG loss <= 0.4 dB/cm (Fig. 21, own earlier work, D259);
  abstract "< 3.5 dB across the O-band" (Fig. 20 reaches ~4.7 dB at 1370 nm); simulated adiabaticity / overlap values.
- tiecke2015 (5 / 13): conical tapered fiber tip on Si3N4 nanophotonic waveguides (fiber_chip_coupler.other, D138):
  tapered-waveguide family (97(1) % best, 93-97 % Fig. 3(e)), rectangular-width family (89-96.5 %), cavity detached onto
  the fiber (96(1) %), low-Q double-sided cavity test device (87 %, back-reflection >= 27.0 dB TE / >= 24.0 dB TM, derived
  from upper-limit reflectivities), non-adiabatic fiber D (~50-60 %). Efficiencies author_estimate (Bragg mirror
  reflectivity assumed 1, typical FC-FC 0.89). Fab empty (fiber tips "we fabricate", authors split Harvard / MIT / UEC;
  Si3N4 fabrication by reference); facility org_center_for_nanoscale_systems ("performed in part at CNS").
- hwang2017 (2 / 6): apodized GC array on the 128 x 128 MEMS switch (2.5 dB/facet at 1310 nm, 10 deg, 63.5 um pitch;
  origin not stated, D167); 136-channel ion-exchanged glass pitch-reducing array (fiber_interface.fan_out, IL 0.6-1.2 dB,
  scope unspecified, O-band inferred). Fab empty (authors Tyndall / UC Berkeley / GIST). Coupler count 272 vs 276
  inconsistent, not entered; no switch performance in the paper.
- margaria2025 (3 / 8): QD micropillar direct fiber pigtail (fiber_chip_coupler.other: 75(5) % author_estimate from the
  loss budget with assumed unchanged first-lens brightness; simulated 71 % at the device gap and 96 / 93.8 / 89.9 % at
  0.23 / 1 / 2 um gaps); UHNA3-780HP splice (fiber_interface.other, 90(2) %); micropillar cavity family
  (resonator.photonic_crystal, Q ~13,000 typical, 20 / 40 DBR pairs). Fab: micropillars C2N (+ Quandela, missing);
  pigtail empty (Quandela missing). RENATECH named only in funding (D80c). Not entered: 3.5 um gap, < 200 nm alignment
  precision, Purcell factor, projections (96 % contact, 95 % splice), free-space lens coupling 0.82 (other component).
- miller2011 (4 / 5): self-aligning ferrule / sleeve / circular-Si-substrate fiber-to-TES package (fiber_interface.other:
  coupling > 99 % author_estimate, band unspecified; back-reflection > 20 dB over 1525-1630 nm derived from < 1 %);
  TES detectors per design wavelength (photodetector.other: system detection efficiency 96-98 % at 805 nm, 83-87 % at
  850 nm, 88-95 % at 1550 nm, extracted from Fig. 8, ref_plane fiber). Fab empty (passive; Albion College / NIST). Not
  entered: alignment offset 3.1 +/- 1.3 um over 35 devices (no parameter), calculated < 0.1 % penalty, earlier manual
  alignment (cited), device count 7 vs 8 (n_samples left empty).
- guerber2018 (2 / 12): phase-controlled DC PBS on 600 nm PECVD SiN (polarization.pbs: IL < 0.6 dB, PER > 10 dB over
  1260-1355 nm both polarizations, normalized to a straight waveguide; footprint 136 x 8.7 um; stack); cascaded three-PBS
  (IL < 1.3 dB / PER > 20 dB over 1260-1355 nm; IL < 1.1 dB / PER > 24 dB over 1270-1355 nm, Table I). Fab
  org_stmicroelectronics ("fabricated on ... DAPHNE in ST Crolles"). ER (TE / TM power difference per output) entered
  as per_db (merged polarization precedent).
- lin2022 (6 / 30): bilayer edge coupler (lnoi_strip at the facet, D82f: 1.7 / 1.55 dB per facet TE / TM, PDL 0.15 dB
  derived, 3-dB bandwidth >= 70 nm = measured span, full taper geometry); mode-evolution PSR (on-chip IL < 0.12 dB,
  crosstalk ~23 dB as per_db); 2 um rib waveguide (~0.11 dB/cm, sidewall 64 deg SEM); single-stage SOP generator
  (PER 22.8 dB), multi-stage SOP generator (PER 41.9 dB), endless polarization controller (on-chip IL 0.92 dB, footprint
  ~1.5 x 0.3 cm) as polarization.compensator. Fab org_sun_yat_sen_university (fabrication performed at the SYSU State
  Key Lab; fabricating author at SYSU). Not entered: Table 1 0.52 dB (footnote device identity ambiguous, D159);
  scrambling rate, DOP, SOP accuracy, tracking rate (no parameters); simulated electrode trade-off.

## EO-atlas candidate (not entered, skill rule 2 / D168)

lin2022 2x2 EO MZI building block (X-cut TFLN, 1.2 cm arms, single-drive push-pull): Vpi 2.4 V, switching < 5 ns,
IL < 0.4 dB, ER ~22.6 dB (p.3 Fig. 1(e)-(f)).

## Orgs missing

Quandela SAS (margaria2025 p.1 affiliation; p.9 author contributions: pigtailing and source fabrication).

## Judgment calls

- dangel2018: one row per fabrication approach with taper length Lc in the metric condition (family rows, D165) rather
  than one row per Lc; coupler loss from a two-coupler S-shaped test unit entered per_component as the paper uses it as
  the single-coupler loss (halving not stated, noted). Direct-processed PWG on the Si chip = transition; PWG on a separate
  glass die flip-chip bonded = chip_chip_coupler.
- tiecke2015 / dangel2018: wavelengths inferred (780 nm design; O-band) where not stated with the value.
- margaria2025: micropillar cavity entered as resonator.photonic_crystal (Fabry-Perot DBR cavity) family row.
- miller2011: fiber-to-detector package as fiber_interface.other (no on-chip waveguide); TES as photodetector.other.
- lin2022 polarization controllers as polarization.compensator; their EO MZI metrics left to the EO atlas.

## Registry gaps

| parameter / class | skipped value | locator | proposed definition |
|---|---|---|---|
| gap_nm, coupling_length_um, min_bend_radius_um for polarization | guerber2018 gap 600 nm, Lc 30 um, Lpc 18 um, S-bend 40 um; lin2022 ADC 34 um | guerber2018 p.2 Sec. II; lin2022 p.13 Supp. II | allow the splitter geometry parameters for DC-based polarization devices |
| mmi_width_um / mmi_length_um for polarization | lin2022 MMI mode filter 6 x 53.5 um | lin2022 p.13 Supp. II | width / length of an MMI mode filter in a PSR |
| fiber_chip_coupler working gap (e.g. fiber_gap_um) | margaria2025 3.5 um (3 um design) | margaria2025 p.4 | fiber-facet-to-device distance of a direct (butt / normal-incidence) fiber coupling |
| alignment offset (e.g. alignment_offset_um) for fiber_interface / fiber_chip_coupler | miller2011 mean 3.1 um, sigma 1.3 um (35 devices); margaria2025 < 200 nm | miller2011 p.4-5 Fig. 2; margaria2025 p.4 | measured lateral offset / alignment precision of an assembled fiber coupling (statistic in condition) |
| polarization tracking / scrambling rate (rad/s) | lin2022 10 krad/s tracking, 65 Mrad/s scrambling | lin2022 p.5, p.7 | rate of SOP change tracked (residual in condition) or generated |
