# lit_184 batch report

Papers: lit:li2017a, lit:nejadriahi2021. Distilled 2026-11-18 (verified_on 2026-11-18). Dry run
`merge_component_staging.py data/_staging/components/lit_184 --dry-run`: +14 components, +53 metrics, 0 errors.

Both cached copies are arXiv versions of the listed journal papers (page-1 titles match the source rows); values are
from the cached copies only.

## lit:li2017a (Chalcogenide glass-on-graphene photonics; arXiv 1703.01666 preprint of the Nature Photonics 2017 paper, main text + Supplementary Information in one 50-page file)

`garbled_text_layer` (page 36 only: equations of Supp. Sec. IX); no value is taken from page 36. Table S1 (p.29), Table S2
(p.37) and all figure-read values were checked on the page renders (the text layer dropped the "this report" cells of
Table S2).

Components 9, metric rows 34:

| component | class | rows |
|---|---|---|
| graphene_sandwich_polarizer | polarization.other | IL 0.8 dB (derived, 0.04 cm x 20 dB/cm), ER 23 dB (derived), ER 21 dB (far-field, measured), ER > 20 dB 940-1600 nm (simulated), length 400 um |
| graphene_sandwich_wg | waveguide_platform.straight | graphene-induced TE 590 dB/cm (derived, MZI differential absorption), TM 20 dB/cm excess (derived, ring extraction), modeled TM 0-1.5 / TE 575 dB/cm (simulated) |
| graphene_ring_r40 | resonator.ring (test structure) | radius 40 um, FSR ~4.4 nm (Fig. S8(b) read) |
| gc | fiber_chip_coupler.grating | ~8 dB per coupler (author_estimate, origin not stated, C band inferred) |
| graphene_heater_to_switch | phase_shifter.thermo_optic | 10 nm/mW -> 10000 pm/mW (derived), P_phi 0.11 mW (derived), rise / fall 14 us |
| pc_nanobeam_cavity | resonator.photonic_crystal | Q up to 8000 near 1570 nm, core 560 nm (2 x 280 nm), block width 600 nm (Fig. S16(a) label) |
| bridge_mmi_crossing | crossing.mmi | crossing loss < 0.7 dB 1450-1650 nm TM (simulated; fabricated row, D80e) |
| midir_graphene_pd | photodetector.graphene | 0.25 A/W peak at 2030 nm (author_estimate), 0.108 A/W at 2185 nm / 1.5 V (Fig. 4(c)), 260 ohm, 80 um length, 2.5 um contact spacing, ridge 1.3 um, slab 250 nm, 3 um oxide |
| flexible_graphene_pd | photodetector.graphene | 0.032 A/W at 1550 nm / 1 V (author_estimate), 1650 ohm, 80 um, 1.8 um spacing, ridge 0.8 um, slab 130 nm |

Values not entered and why:
- Mid-IR graphene electro-absorption modulator (modulation depth up to 8 dB/mm over 2.05-2.45 um, time constant 7 us,
  inferred 23 kHz, 0.5 pF / 4.3e5 ohm estimates, 6.4 GHz projection; p.9, p.42-45): modulator metrics are EO-atlas
  scope (skill rule 2, D250); no non-modulator component with its own value in that device.
- Polarizer figure of merit 29 and Table S1 fractional bandwidths 0.45 / 0.91 (no parameter); 980 nm extinction (only a
  polar plot clipped at a -25 dB axis, Fig. 2(h)); undoped-graphene projection 0.94-2.5 um (hypothetical variant).
- Thermo-optic switch FOM 0.65 mW-1 us-1 (no parameter); graphene sheet resistance ~400 ohm/sq and Hall carrier data
  (material values); simulated cavity red-shift 7.2 nm; peak shift ~8 nm at 775 uW (Fig. 3(e)/(f), not stated as a
  tuning range).
- Fig. S16(a) 0.48 um label (period vs block length not stated), connector width modulation ~50-450 nm (Fig. S16(c),
  role / reading); n_periods (N range plotted, count not stated).
- Detector "ridge height" 0.5 / 0.3 um (total rib height vs step not stated); zero-bias responsivity (only a
  photocurrent vs power plot, Fig. 4(b)).
- Mid-IR facet coupling loss (method stated, number not printed).
- Table S1 / Table S2 rows of other works (comparison tables, rule 1 / 3).
- Supp. Sec. I-III (Raman, passivation, As2Se3 nanoimprint grating with 2 um period): no device performance.

Fab / facility: fab `org_mit` (author contributions: H.L., MIT, "carried out device fabrication", p.11); facilities
`org_mit_microsystems_technology_laboratory` + `org_center_for_nanoscale_systems` ("Device fabrication was performed
at" both, p.11 Methods, plus fabrication facility support acknowledged, p.11). No missing orgs. Wafer supplier Silicon
Quest International and UCF glass synthesis are notes.

Judgment calls (for the audit):
1. Harvard University not added as fab although fabrication was "performed at" Harvard CNS (D448 put the owning orgs of
   named processing places on fab for gundavarapu2018); here the named fabricator is MIT and CNS is a shared user
   facility (D82c / D83c reading). Alternative: fab `org_mit;org_harvard_university`.
2. TE 590 dB/cm basis `derived` (ER converted to absorption with the Supp. Sec. V model, then slope vs graphene length)
   and method `cutback` (length series inside MZI arms); `measured` (D80a cascade-slope fit) is the alternative.
3. Polarizer IL 0.8 dB / ER 23 dB `derived` (printed correspondences of the 20 / 590 dB/cm losses over 400 um).
4. Thermo-optic switch split into `phase_shifter.thermo_optic` (graphene heater: tuning efficiency, P_phi, rise / fall)
   and `resonator.photonic_crystal` (Q, geometry) per D396, following the yan2017 graphene-heater precedent instead of
   `switch_fabric.other` (D158 / D407), because tuning_efficiency is not allowed on switch_fabric.
5. P_phi 0.11 mW `derived` (authors' arithmetic with their own FWHM and slope; the FWHM used is not printed).
6. Detector responsivities `author_estimate` (equal-facet halving of a two-lens reference loss, D462 / D514), ref_plane
   on_chip. Fig. 4(d) bias: caption 1.5 V vs Supp. Sec. XV "zero bias" sweep; 1.5 V entered because Fig. 4(d) at 2185 nm
   matches Fig. 4(c) at +1.5 V (D417 note).
7. Contact spacing entered as `absorber_width_um` (D612 schuler2016 precedent).
8. Platform `other` for Ge23Sb7S70 / graphene stacks (merged chalcogenide precedents shen2019, wang2023, du2018).

Registry gaps: none required. Candidate (no row added): polarizer figure of merit (ER / IL) - skipped value 29 (p.6,
Table S1); definition "ratio of extinction ratio to insertion loss of a polarizer, both in dB".

## lit:nejadriahi2021 (Efficient and compact thermo-optic phase shifter in silicon-rich silicon nitride; arXiv 2106.09476 v1 preprint of the Optics Letters 2021 paper)

Components 5, metric rows 19:

| component | class | rows |
|---|---|---|
| ps_serpentine | phase_shifter.thermo_optic | P_pi 8 mW + std 0.25 (1551.5 nm), V_pi 1.5 V + std 0.25, MZI ER > 15 dB, 3-dB bandwidth 15 kHz + std 0.5, length 1200 um, footprint 4225 um2 (65 x 65), heater width 6 um, Ni:Cr 300 nm, top cladding 1 um |
| ps_rectangular | phase_shifter.thermo_optic | P_pi ~11.5 mW, Ni:Cr 300 nm, length 1200 um |
| euler_bend_90 | waveguide_platform.bend | 0.025 dB per 90 deg (3D FDTD, simulated) |
| euler_bend_180 | waveguide_platform.bend | 0.026 dB per bend (simulated), w_max 420 nm |
| y_branch | splitter.y_branch | excess loss 0.159 dB (simulated, printed as insertion loss, D43) |

Values not entered and why:
- Propagation loss ~7 dB/cm and dn/dT 1.65e-4 /K: cited from the authors' ref. [11] (rule 3); spiral loss lower bound
  ~1.2 dB rests on them (not entered).
- Table 1 rows of other works (comparison, rule 1); Table 1 area 0.0016 mm2 for this work conflicts with the text's
  65 x 65 um2 (noted, D417); TPA "negligible" (cited).
- MZI FSR ~0.56 nm (no phase_shifter parameter; property of the test MZI); 97 % temperature uniformity (simulation,
  no parameter); filament separation 8 um and six filaments (no parameter); rectangular heater 100 x 80 um2 (axis
  assignment not stated); 90-degree bend w_max "0.41" (no unit printed); r_effective 4.1 / 4.4 um (Euler bend,
  label only, D619).
- Rectangular-heater bandwidth ("no significant changes", no value).

Fab / facility: fab `org_university_of_california_san_diego` borderline (first-person "we present the design,
fabrication, and characterization", p.1 / p.4; acknowledgment thanks UCSD's Nano3 cleanroom staff for sample
preparation, p.4; D84b, nejadriahi2024 precedent); no facility (staff thanks, D84b). Missing org as printed: "UCSD's
Nano3 cleanroom" (p.4 Acknowledgments; facility role only if the coordinator reads the acknowledgment as a stated place,
D448; possibly an alias question against `org_san_diego_nanotechnology_infrastructure`).

Judgment calls (for the audit):
1. Platform `sin` for SRN with n = 3.1 (merged Si-rich SiN precedents nielson2005 / croce2026 use `sin`); `other` is the
   alternative given the near-Si index.
2. P_pi / V_pi / bandwidth std rows entered with statistic `std` (paper: standard deviation over more than 15 repeated
   measurements); n_samples left empty ("over 15").
3. Rectangular-heater P_pi wavelength 1551.5 nm `wavelength_inferred` ("the corresponding values").
4. Bend / Y-branch simulation wavelength 1550 nm inferred (design wavelength of Eq. 1).

Registry gaps: none.
