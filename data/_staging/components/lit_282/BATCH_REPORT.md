# lit_282 batch report

Distilled 2026-11-25. Papers: lit:xu2021b, lit:osorniomartinez2025a, lit:yan2016, lit:rivoire2009, lit:chang2016
(amplifier / frequency_converter family; selected because other papers cite them in benchmark tables). Page-1 titles
match the source rows; no correction / erratum; no garbled text layer. No existing `cmp_lit_<id>_` rows for any of the
five. Total 13 components / 67 metric rows. `merge_component_staging.py --dry-run`: 0 errors (2 warnings belong to
other batches: guo2024a, ni2025b).

Fab / facility: `fab_org_ids` empty on every row (passive fabrication wording, or first person with authors at
unrelated orgs). One facility set: rivoire2009 `org_stanford_nanofabrication_facility`. Missing org: ANFF (yan2016).

## lit:xu2021b (2 components / 5 metrics)

- `cmp_lit_xu2021b_sin_reo_soi_wg_w1p08` (waveguide_platform.straight, platform `other`): cutback loss 4.70 dB/cm at
  1445.8 nm TM (printed +/- 2.05), width 1080 nm, BOX 2 um.
- `cmp_lit_xu2021b_focusing_apodized_gc_tm` (fiber_chip_coupler.grating): measured CE ~14.4 % at the 1462 nm pump
  (per_coupler, method unspecified), simulated peak CE > 30 % (wavelength not printed, band unspecified).
- Not entered: signal enhancement ~16 dB/cm at 1536 nm, 1510-1560 nm span (pump on / off ratio, no net gain; D674,
  in component notes); Er3+ absorption > 35 dB/cm from the dip depth (ion-absorption part only, not a total loss;
  notes); deduced pump absorption ~2.84 dB/cm, ETU parameter, PL lifetime ~2.35 ms, confinement factor 18 / 56 %
  (no parameters); 1.14 / 1.20 um loss spectra (plot only); simulated leakage curves (Fig. 1); GC simulated PER ~30 dB
  (registry gap below).
- No amplifier row: the only amplifier quantity is signal enhancement (D674), so it would have no performance metric.
- Fab: "we grew" the REO film (p.4) but authors at NTT units, Nihon University and Yamato University; SiN patterning
  passive with citation (ref. 49): empty (D80b / D154).
- Judgment calls: platform `other` (SiN strip-loaded REO on SOI; no enum value); abstract stack order "SiN / REO / Si
  72 / 90 / 300 nm" contradicts the Fig. 1 caption and the 300 nm SiN deposition: caption order used in
  core_material, conflict noted; layer thicknesses kept in core_material only (multi-layer core).

## lit:osorniomartinez2025a (5 components / 35 metrics)

- `cmp_lit_osorniomartinez2025a_edwa_30cm` (amplifier.rare_earth, al2o3): fiber-to-fiber gain ~15 dB (small signal),
  14.7 dB (-28.4 dBm incident), ~10 dB at 3 dBm incident (Fig. 6(b), extracted); NF 6.5 dB at 1550 nm and 5.6 dB
  minimum at 1566 nm (fiber-to-fiber); off-chip output 17.5 dBm (fiber); on-chip ~101 mW (20.0 dBm) and 22 % optical
  efficiency (author_estimate: rest on the conservative 2.5 / 3 dB per-facet coupling); gain bandwidth ~60 nm
  (criterion within 10 dB of peak); length, footprint (derived), width 1750 design / 1756 measured, film 770 design /
  804 measured, cladding ~7 um (derived sum).
- `cmp_lit_osorniomartinez2025a_al2o3er_waveguide` (waveguide_platform.straight): IR-camera total loss 0.75 dB/cm
  (1550 nm, -26 dBm), 0.09 dB/cm (7 dBm incident), < 0.1 dB/cm at 1640 nm; Fig. 4(d) points 1530 / 1560 / 1600 /
  1620 nm extracted.
- `cmp_lit_osorniomartinez2025a_al2o3er_film_slab` (waveguide_platform.other): background ~0.015 dB/cm at 1550 nm,
  author_estimate (fit extrapolated from 451-785 nm, D435).
- `cmp_lit_osorniomartinez2025a_edge_coupler` (fiber_chip_coupler.edge, test_structure): 2.36 dB/facet mean of 4
  loops at 1550 nm (loopback_half, derived halving, includes half the 2.9 mm Er-doped loop), ~2.9 dB at 1480 nm
  (Fig. 5, extracted), simulated ~0.8 dB at the 200 nm tip for 1480 / 1550 nm (Fig. 1(a) curves, D454); tip 200
  design / 242 measured, taper 1 mm, simulated MFD 5.5 um, fiber MFD 10.1 um (specification, PM1550-XP).
- `cmp_lit_osorniomartinez2025a_bend_r450` (waveguide_platform.bend): simulated bend loss < 0.01 dB/cm at R 450 um
  (simulation wavelength not printed: band unspecified); min bend radius 450 um.
- Not entered: conservative 2.5 dB/facet coupling (an analysis choice, noted), Fig. 9 gain / output / NF spectra beyond
  the stated values, slab losses at 451-978 nm (plot only), ASE spectrum, simulated mode overlap ~79 %.
- Conflicts noted: NF minimum printed at 1566 nm (abstract, p.9) vs 1556 nm (p.2), and the Fig. 9(d) lowest points sit
  near 1590-1600 nm; printed 1566 nm kept.
- Fab: passive verbs, all authors at University of Twente MESA+: empty (D80b). CMAM beam time for RBS only and the FIB
  milling thanks a person: no facility (garciablanco2025 precedent). MESA+ NanoLab is not named in this paper.
- Judgment calls: gain_db rows carry `ref_plane fiber` (bao2024 precedent); NF and 14.7 dB basis `measured`
  (standard IEC extraction of own spectra, D80a); the 0.09 dB/cm value is below the method limit the paper states
  (noted, kept as printed).

## lit:yan2016 (2 components / 7 metrics)

- `cmp_lit_yan2016_er_gegase_as2s3_rib_w2` (waveguide_platform.straight, platform `other`): cutback 1.7 dB/cm at
  1610 nm TE (62 / 40 / 22 mm); width 2000 nm (derived rescale), Er:GeGaSe 650 nm and As2S3 450 nm (reflectometer,
  measured), etch 400 nm, BOX 2 um.
- `cmp_lit_yan2016_lensed_fiber_facet` (fiber_chip_coupler.edge): ~4 dB per facet (combined lens, overlap and
  reflection losses; origin not stated -> author_estimate; 1505 nm pump wavelength inferred).
- Not entered: signal enhancement ~9 dB, 50 % / ~55 % inversion (no gain achieved; D674, notes); PL lifetimes;
  photoinduced loss increases of undoped test waveguides (loss change, no parameter); Fig. 3(b) loss spectrum.
- No amplifier row (no gain; only enhancement / inversion).
- Missing facility: "Australian National Fabrication Facility (ANFF) at the Australian National University" (p.10
  Acknowledgments, "facilities and support") - facility role for both rows; not in organizations.csv / org_aliases.csv.
- Fab: passive, all authors at ANU: empty.

## lit:rivoire2009 (1 component / 7 metrics)

- `cmp_lit_rivoire2009_gap_l3_phc_shg` (frequency_converter.shg, platform `other`): 430 %/W normalized efficiency and
  5e-5 (0.005 %) coupled-power efficiency at 11 uW (author_estimate: rest on the ~5 % coupling estimate); 2e-6
  (0.0002 %) relative to 220 uW through the objective (derived, unit conversion); Q 5600 (reflectivity, typical) and
  6000 (SH Lorentzian-squared fit) near 1485.5 nm (axis read), FDTD Q limit 15000 (simulated, 1500 nm inferred);
  membrane 160 nm.
- Facility `org_stanford_nanofabrication_facility` ("performed in part at the Stanford Nanofabrication Facility of
  NNIN", pre-merger SNF, D80d). Fab empty (passive; authors at Stanford and Humboldt University).
- Not entered: ~5 % input coupling (coupling_efficiency_pct not allowed for frequency_converter), lattice constant
  500-560 nm (period_nm not allowed), cos^4 polarization dependence, refs. 14 / 15 efficiencies (cited).
- Judgment calls: one row for the design family (paper reports "typical" cavities; which cavity gave Fig. 4 is not
  stated, noted per D159 spirit but the values are kept since all come from the one design); Q as q_loaded
  (unqualified, free-space-coupled cavity); platform `other` (suspended GaP has no enum value; gap_on_insulator would
  be wrong).

## lit:chang2016 (3 components / 13 metrics)

- `cmp_lit_chang2016_sin_tfln_ppln_shg` (frequency_converter.shg, lnoi_loaded_sin): ~160 %/W/cm2 at 1530 nm TE
  (measured), simulated 1600 %/W/cm2; poling period 6.6 um, poled length 4.8 mm, SiN ridge 2 um, etch ~350 nm, LN
  700 nm, BOX 2 um, cladding 1 um.
- `cmp_lit_chang2016_sin_tfln_waveguide` (waveguide_platform.straight): ~0.3 dB/cm around 1550 nm, ~1 dB/cm around
  1530 nm (method not stated).
- `cmp_lit_chang2016_lensed_fiber_facet` (fiber_chip_coupler.edge): ~6 dB per facet (telecom, c_band inferred), ~14 dB
  for the SH light incl. lensed-fiber propagation loss (765 nm inferred).
- Not entered: 3-dB width ~3 nm of the efficiency spectrum (registry gap), domain duty cycle 40 +/- 10 % (fill_factor
  not allowed for frequency_converter), 80 nW SH at 0.5 mW pump (pump reference plane not stated), 2.4 um shortest
  period (other sample), poling field 48 kV/mm / threshold > 30 kV/mm (no parameter), cited bulk PPLN 30-40 %/W/cm2.
- Fab: passive; thanks for help with processing is a person: empty. LNOI supplier NANOLN in notes. No facility named.

## Registry gaps (skipped value + locator + proposed definition)

1. `bw_3db_nm` (or a new `qpm_bandwidth_nm`) for `frequency_converter`: chang2016 ~3 nm 3-dB width of the normalized
   SHG efficiency vs pump wavelength (p.4 Sec. 3, Fig. 4(a)). Proposed: "full width at -3 dB of the conversion
   efficiency vs pump wavelength (phase-matching / acceptance bandwidth; which wave in condition)". Related to the D429
   candidates bw_fwhm_nm / bw_fwhm_ghz on frequency_converter.
2. `coupling_efficiency_pct` for `frequency_converter`: rivoire2009 ~5 % free-space input coupling into the cavity
   (p.5 Sec. 3). Proposed: "pump power fraction coupled into the converter (free-space or fiber), as reported".
3. `period_nm` for `frequency_converter`: rivoire2009 photonic-crystal lattice constant a = 500-560 nm (p.3).
4. `per_db` for `fiber_chip_coupler`: xu2021b simulated TM / TE polarization extinction of the GC ~30 dB (p.4).
   Proposed: "ratio of the coupling efficiency of the design polarization to the orthogonal one, positive dB".
5. Long-standing (lit_13 / D674): `signal_enhancement_db` / `_db_per_cm` for amplifier: xu2021b ~16 dB/cm at 1536 nm
   (p.6-7), yan2016 ~9 dB at 1538 nm (p.7).

## Missing orgs

- Australian National Fabrication Facility (ANFF) at the Australian National University - facility -
  lit:yan2016 p.10 Acknowledgments (both yan2016 rows).
