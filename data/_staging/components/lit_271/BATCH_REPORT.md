# lit_271 batch report

Batch lit_271 (DevLog-007 D744): lit:pernice2012a, lit:wu2015, lit:siew2015, lit:sun2013b. Distilled 2026-11-24 under
the pic-component-distill skill (Contracts v4-v7). The cached text of each paper matches its source row (page-1 title).
No text layer is garbled. No paper is a correction, an erratum or another paper.

Validation: `uv run --offline python scripts/merge_component_staging.py data/_staging/components/lit_271 --dry-run`
gives +20 components, +159 metrics and 0 errors. The batch rows raise no warnings.

| paper | components | metric rows |
|---|---|---|
| pernice2012a | 12 | 89 |
| wu2015 | 4 | 37 |
| siew2015 | 2 | 20 |
| sun2013b | 2 | 13 |
| total | 20 | 159 |

## pernice2012a: AlN-on-insulator rings and grating couplers, NIR and 770 nm (Optics Express 2012)

Rows:

- `nir_ring_g1000`: the 440k loaded-Q device (1000 nm gap). It has Q, the 3.5 pm linewidth, the 0.8 dB/cm loss and a
  figure-read dip depth.
- `nir_ring_w900_g650`: the critically coupled Fig. 4(b) device, with Q ~1e5, ER 30 dB, FSR 1.9 nm and ng 2.01.
- Width series (Fig. 5): `nir_ring_w650`, `w700`, `w800`, `w1000`, `w1100`, `w1200`. Each row has a Fig. 5(a) Q read
  and the Fig. 5(b) maximum ER with its gap. The w1200 row has Q only.
- Visible rings: `vis_ring_g250` and `vis_ring_g300` (R 40 um, pulley bus).
- GC families: `gc_1550` and `gc_770`.
- Platform `other` (AlN on oxide, D515 precedent). Fab `org_yale_university`: "we fabricate" (p.7) and "To fabricate
  ... we first develop" (p.3), all authors at Yale. No facility: only staff are thanked.

Not entered:

- GC coupling bandwidths "roughly 60 nm" and "about 30 nm": the level is not stated. They are in the component notes.
- Cutback "comparable loss" (p.7): no number printed.
- AFM roughness of 1.2 nm rms top and 3.5 nm sidewall: no parameter.
- Simulated single-mode cutoff width of 630 nm: no parameter.
- Pulley FDTD curves (Fig. 2): plots only.
- Visible 100 nm gap device: no resonances observed.
- Fig. 5(b) points other than the per-width maximum: these are separate gap devices with no Q.
- Per-design GC peak losses in Fig. 1: only the stated typical values are entered, on family rows.

Judgment calls:

1. The Fig. 4(b) device (30 dB, Q ~1e5, 650 nm gap) is tied to the 900 nm width. p.8 assigns the 650 nm critical gap
   to the 900 nm series, and only that curve peaks at 650 nm in Fig. 5(b).
2. FSR 1.9 nm and ng 2.01 are entered on the w900_g650 row. The sentence states them for the 200 um diameter series,
   just before the Fig. 4(b) device, and the Fig. 4(b) dip spacing agrees. An auditor may prefer notes-only under D254.
3. The 0.8 dB/cm loss is `author_estimate`. The paper's formula reproduces 0.80 dB/cm only when the loaded Q of 440,000
   is used as Q_int (D403 / D76). The visible 20 dB/cm is also `author_estimate`: the formula with Q 30,000 and ng 2.2
   gives ~26 dB/cm, so the Q_int input is not stated.
4. Visible q_intrinsic "> 30,000" (abstract) is entered as `author_estimate` with qualifier gt.
5. Fig. 5 values are reads of the PDF render, with axis ticks located by pixel: Q about +/-5 % on the log axis, ER
   +/-0.3 dB. The width-series widths and the gaps at maximum ER are axis / legend labels (`extracted_from_figure`).
6. The g1000 device's ring width is not stated. It is kept as its own row: the gap makes it a separate design, so D159
   does not apply.
7. GC typical losses (8.5 +/- 1 and 7.7 +/- 1 dB) are `loopback_half` + measured. The pair is measured, the couplers are
   assumed identical, and the Fig. 1 curves are per coupler.

## wu2015: Ta2O5 channel waveguide, inverse taper and 200 um ring (Optics Express 2015)

Rows: `channel_wg` (cutback 1.5 dB/cm), `inverse_taper` (edge coupler), `untapered_facet` (reference facet) and
`ring_d200` (TE0 and TM0 fits). Platform `other` (Ta2O5 precedent rows). Fab is empty: patterning is stated passively,
the only first-person step is the target pre-sputter, and the authors span NSYSU and NTU (D80b). No facility.

Not entered:

- Projected "< 1 dB/cm" with better stitching and the expected Q > 1e5: projections.
- Bus-ring field transmission coefficients t 0.9923 / 0.9930: BPM-simulated inputs to the fit, no parameter. They are
  in the notes.
- Film data: n ~2.1, crack density, AFM roughness 0.13 nm and XRD. These are material data, not component metrics.
- Notch depths: not printed. The Fig. 4(d) dips are model curves.
- Rabiei Q comparison (ref. [15]): cited work.

Judgment calls:

1. The 3.2 dB cutback intercept is `fiber_to_fiber` with propagation excluded, following the two-facet total precedent
   (chen2021b / feyisa2022). The 1.6 dB per facet is `loopback_half` derived.
2. The untapered facet's 3.5 dB per facet is derived as (3.2 + (7.8 - 4.0)) / 2. Both 4.8 mm devices have the same
   length.
3. Ring loss (8.1 / 9.0 dB/cm) and Q_i 4.48e4 are `author_estimate`: the coupling coefficient comes from BPM simulation,
   not from the data (D403). Q_L (39131 / 34019) is measured. The abstract says "coupled Q up to 38,000" against
   3.91e4 in the text and figure, noted under D417.
4. The sidewall angle (~84 deg) and the SEM facet widths (350 / 440 nm and 730 / 800 nm) are `measured`. How the angle
   was obtained is not stated.

## siew2015: LNOI rib microring and rib waveguide (IEEE PTL 2016)

Rows: `rib_ring_r50` (Q 2800, FWHM 0.57 nm, FSR 3.2 nm, finesse 5.6, ER 18.7 dB, EO tuning 2.15 pm/V, geometry) and
`rib_wg` (5.3 dB/cm from imaging, 8.3 dB/cm from Fabry-Perot). Platform `lnoi_rib`. Fab
`org_national_university_of_singapore`: first-person processing, all authors at NUS. The NANOLN wafer is a note
(D428). No facility.

Not entered:

- Table I literature rows: other works.
- Simulated effective indices 1.902 / 1.928 and the Fig. 2(a) normalized bend flux: no matching parameter.
- Conclusion range 5.3-8.48 dB/cm: noted (8.48 vs 8.3 under D417).

Judgment calls:

1. The printed "modulation depth 18.7 dB" is the depth of the 1606.9 nm resonance before the electrodes, with no voltage
   applied. It is entered as `extinction_db` with the wording in the notes.
2. The EO tuning of 2.15 pm/V sits on the ring row because no EO-atlas row exists (D589 precedent); this paper is an
   EO-atlas candidate. Table I prints 0.244 pm/V for this work, against the text and Fig. 7 (107.5 pm per 50 V);
   noted under D417.
3. The Fabry-Perot 8.3 dB/cm is `measured` (D394, Fresnel R 0.13 as the model input). Its 1600 nm wavelength is
   inferred from the LiNbO3 index used for R. The imaging 5.3 dB/cm is `band: unspecified`: the source and wavelength
   of that measurement are not stated.

## sun2013b: ARM filter and integrated heater in deep-trench bulk CMOS (OIC 2013)

Rows:

- `arm_filter_d6` (`resonator.ring`, D400: no WDM path on the chip): FSR 3.7 THz, 350 GHz range converted to ~1.94 nm,
  10-15 uW/GHz converted to ~370-555 pm/mW, Table 1 37 mW per 2 pi as `author_estimate` (D435), two figure-read
  extinctions, and geometry.
- `arm_heater` (`phase_shifter.thermo_optic`, D396 cross-note): ~1.7 kOhm (`author_estimate`, origin not stated) and
  3.5 mW at the max setting.
- Platform `other` (poly-Si bulk CMOS precedent). `process_name` is the printed "commercial 0.25 um-equivalent bulk
  CMOS process with deep-trench isolation (equivalent to a DRAM periphery process)".

Not entered:

- Driver circuit areas, the 8-bit step of ~1.37 GHz and total power vs clock (Fig. 2 right): electronics or system
  values, in the notes.
- Fig. 3 tuning cost at other clocks.
- Table 1 rows for refs. [3]-[8].
- Drop-port levels: the normalization of "relative transmission" is not stated.

Judgment calls:

1. Fab is `org_micron_technology`, borderline under D84b: the acknowledgment credits "fabrication support of Micron
   Technology Inc." and names Micron staff, and the text names no foundry.
2. The GHz-to-nm and uW/GHz-to-pm/mW conversions use lambda^2 / c at the printed ~1290 nm design wavelength (churaev2023 /
   andreou2019 precedent). The tuning cost includes driver power at a 20 MHz clock (stated in the condition).
3. Deep-trench depth of 1.2 um (Fig. 1 schematic label) is entered as `box_thickness_um` (lower cladding),
   `extracted_from_figure`.
4. Fig. 2 off-state resonances near 1291 and 1313 nm look ~22 nm apart by eye, against the printed 3.7 THz (~20.5 nm).
   This is noted only.

## Missing fab / facility orgs

None. Yale, NUS and Micron Technology already have registry ids (`org_yale_university`,
`org_national_university_of_singapore`, `org_micron_technology`). wu2015 has no fab or facility statement.

## Registry gaps (value skipped + locator + proposed definition)

- `rms_roughness_nm` (already listed in D418): pernice2012a 1.2 nm top and 3.5 nm sidewall (p.6); wu2015 film 0.13 nm
  (p.4). Proposed definition: "RMS surface or sidewall roughness, measurement method (AFM, SEM) in condition".
- Coupling bandwidth with an unstated level: pernice2012a GC ~60 nm / ~30 nm (p.4, Fig. 1). Either `bw_unspecified_nm`
  ("full coupling bandwidth as printed, level not stated") or keep in notes, which is the current practice.
- `self_coupling_field` (resonator): wu2015 t = 0.9923 TE0 / 0.9930 TM0 (p.7, Fig. 4(d)). Proposed definition: "field
  self-coupling (bus transmission) coefficient of the ring coupler as reported".
- `tuning_step_ghz` (resonator / phase_shifter): sun2013b ~1.37 GHz per 8-bit code (p.2). Proposed definition:
  "smallest resonance-tuning step of a digitally driven heater".
