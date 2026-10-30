# Batch lit_56 report (distill subagent, 2026-10-30)

Dry-run `batch lit_56: +28 components, +219 metrics; errors 0` (only the pre-existing WARN on cmp_lit_ni2025b_pimmwc-m18).
ASCII, no e-mail, no street / postal text. Rights: all eight `restricted_local_only` (facts and locators, at most a few
words quoted). Page-1 title / authors match the source rows for all eight; none is a correction / erratum (3-12 pages each).
wang2012 `garbled_text_layer` (pages 10-12): Table 1, Fig. 10-12 and the acknowledgments were read on the page renders;
pages 1-9 read cleanly. No supplement cached (lee2012 refers to Supplementary Sections I-II). Generator: scratchpad
`lit_56/gen.py`.

## Per paper (components / metrics)

- wang2012 (7 / 67): sidewall Bragg gratings in a compact SOI ridge (500 nm ridge, 1 um slab, 70 nm etch, 220 nm, 2 um BOX,
  period 290 nm, L 580 um, 2000 periods) and comparison strip gratings (500 x 220 nm, period 320 nm), reflector.bragg, fab
  org_imec ("fabricated at IMEC", p.4). Die -2, 25 C, TE: 3-dB bandwidths ridge-corrugated 40 / 60 nm 0.47 / 0.65 nm,
  slab-corrugated 40 / 60 nm 0.43 / 0.60 nm (Fig. 6 labels; panel assignment checked on the render: the text-layer order
  puts the labels in the wrong panels), peak R > 90 % for 60 nm (both); strip 10 / 40 nm 1.56 / 5.21 nm. Table 1 wafer
  statistics (centre-row dies): bandwidth mean / std for RGR (0.68 / 0.04), RGS 80 nm slab (0.72 / 0.08), SG (5.36 / 0.61),
  wavelength condition = mean Bragg wavelength. Not entered: Bragg wavelength mean / std / range per device (no reflector
  parameter, in notes), Fig. 9 bandwidth-vs-corrugation points (plot), simulated sensitivities S (Fig. 11), extracted
  thickness / width variations (Fig. 12), the authors' earlier 0.8 nm strip result (ref. [8], D259), GC / Y-branch / 30 um
  strip-to-ridge taper (no performance values). Strip Bragg wavelength read off Fig. 8 (~1513 nm, inferred).
- giuntoni2009 (3 / 29): top-corrugated SOI rib Bragg reflectors (t 1.5 um, rib etch 0.7 um, L 800 um, D 0.3 trench fraction ->
  fill_factor 0.7 derived, D253), w 1.6 um: shallow (d 80 nm, 226 nm) R 80 % at 1549 nm, 0.8 nm bandwidth, 15 dB transmission
  extinction, ~0.5 dB out-of-band IL; deep (d 150 nm, 225 nm) R 88 %, 2.1 nm, up to 19 dB, < 1 dB, plus the 2D BEP design
  (R > 99 %, 2.1 nm, < 0.15 dB, simulated). Reference rib waveguide row: 0.2 dB/cm, lensed-fiber coupling 47 % per facet
  (virtual cut-back; % derived). Reflectivities are `author_estimate` (Eq. (1) uses the nominal K = 0.5 3-dB coupler).
  Deep-grating Bragg wavelength ~1540 nm read off Fig. 5(c) (inferred). Not entered: 77 pm/K thermal tuning (2.2 um rib,
  Fig. 8; no reflector thermal parameter, so no row for that device), TM shift 3 nm / birefringence 7e-3, Fig. 7 Bragg
  wavelength vs width (plot).
- zhang2010 (4 / 39): two-layer Si TE mode converter (200 x 400 nm vertical <-> 400 x 200 nm horizontal waveguide, 400 nm SOI,
  200 nm partial etch, ~100 nm taper tip), one row per transition length 5 / 10 / 30 um (mode_converter.converter): transition IL
  1.1 / 1.2 / 1.2 dB (vertical launch) and 1.9 / 1.9 / 2.1 dB (horizontal launch), `author_estimate` (subtracts an "estimated"
  5.5 dB reference term and a nominal 5 dB polarizer loss); output PER 16.9-17.3 dB (extinction_db, type in condition); ASE
  1530-1570 nm. Reference 3 mm waveguide row: ~5.5 dB coupling + propagation (scope unspecified: facet count not stated),
  180 nm facet tips. Not entered: 3D FDTD IL vs transition length (Fig. 3, curve), "flat" wavelength response (no number),
  0.5 dB/coupling outlook (ref. [13]).
- lee2012 (6 / 22): chemically etched silica wedge disks on Si (resonator.disk, platform silica, 10 um thermal oxide, 27 deg
  wedge, TE, "1,500 nm band"): Q_int per diameter from the Fig. 2 caption (each value one device): D ~7.5 mm 799-875 M
  (record 875 M, FWHM ~0.3 MHz), ~3 mm 326-367 M, ~1 mm 169-174 M, ~0.5 mm 88-91 M; SBL set (4 devices, mask D 6,020-6,080 um)
  FSR 10.793-10.898 GHz (Fig. 4(a) legend); SBL laser row (laser.other, D396): pump threshold < 0.2 mW (all 4 devices), SMSR
  > 60 dB at 1 mW output. Not entered: material Q 2.5 billion (model fit), AFM roughness (registry gap already recorded, D418),
  FSR-control r.m.s. deviations 2.4 / 0.45 MHz (no parameter), 10 deg / thinner-oxide data (plot only), earlier wedge Q 50 M
  (own earlier work, ref. [15]), sub-Hz ST linewidth (Supplementary, not cached).
- tan2009 (2 / 18): cladding-modulated Bragg gratings (Si cylinders W 200 nm beside a 500 x 250 nm SOI strip, 3 um BOX, 2 um
  PECVD cladding), device A (d 200 nm, 300 nm, L 100 um) and B (d 50 nm, 295 nm, L 70 um): measured stopband (zeros of the
  central lobe) 8 / 16 nm, 2D FDTD 7 / 13 nm, CMT kappa 43 / 921 /cm (simulated; the abstract pairs them with the measured
  bandwidths). Not entered: extinction (Fig. 5 in arbitrary units), Fig. 2 experimental kappa squares (axis assignment of the
  legend vs caption ambiguous, D156), the 2.3 mm / 0.9 nm outlook (calculated example).
- biberman2012 (1 / 20): Si ridge ring R 2.45 mm, 2.25 um gap, 2.05 um x 220 nm ridge on 1 um slab, 300 nm thermal oxide,
  1 um BOX (resonator.ring, soi_rib): TE 1600 nm FWHM 9.9 MHz, FSR 5.35 GHz, Q0 2.2e7 and 2.7 dB/m (stored 0.027 dB/cm) as
  `author_estimate` (fit, regime not stated, D403); TM 1554 nm FWHM 1668.2 MHz, FSR 5.07 GHz, Q0 1.4e5, alpha 0.5 /cm -> 4.34 dB/cm
  (author_estimate, computed, formula in notes); figure-read dip depths ~7.1 / ~19.5 dB; mode-solver Q0 2.2298e7 / 1.3246e5
  (simulated). Not entered: ~30 dB fiber-to-fiber chip IL (couplers not described), comparison values of other works (p.1).
- a2013 (1 / 14): 4-channel TM0-TM3 mode (de)MUX link of cascaded asymmetric DCs on 220 nm SOI (mode_converter.mdm_mux, array /
  link row as ding2013): excess loss < 0.5 dB `de_embedded` vs straight waveguides (abstract says < 1 dB, noted), crosstalk
  > 23 dB over 20 nm, fiber-to-fiber 12-13 dB; FDTD per-stage excess < 0.1 dB and CT >= 25 dB (simulated); access width 0.4 um,
  Lc 4.5 / 7.0 / 9.7 um, 1 um PECVD cladding, 4 / 4 ports. Not entered: bus widths 1.02 / 1.68 / 2.35 um (no role parameter),
  gap 0.3 um (gap_nm not allowed for mode_converter), 1.8 deg taper angle, +/- 10 nm tolerance, per-input Fig. 6 CT labels
  25 / 24 / 28.3 / 23 dB (wavelength not stated; in notes). Measured wavelength not stated: band unspecified + note.
- dolgaleva2011 (4 / 10): fs-laser-written chirped Bragg grating waveguides in fused silica (reflector.bragg, silica): TFT
  device ~10 nm band at 1550.5 nm; series end members uniform 0.2 nm / 90 % and max chirp 18 nm / 10 % (band inferred); grating
  waveguide row (waveguide_platform.straight, amorim2017 precedent): 0.7 dB/cm, 0.05 dB/facet, 3.6 dB total (derived sum),
  mode diameter 11 um, 5 cm. Not entered: dispersion 34.8 ps/nm measured (FTSI) and ~48 ps/nm simulated (no parameter),
  measured reflectivity peak (skewed, rippled Fig. 1(a)), grating length (not stated), transfer-matrix model inputs.

## Fab / facility organizations

- Entered: wang2012 fab org_imec (7 rows).
- Missing from the registry (not entered): "SFU Nanoimaging facility" (wang2012 p.12 Acknowledgments, Simon Fraser
  University, Canada; acknowledged for assistance with FIB cross-section images): shared facility use, add in the org round,
  then facility_org_ids on the 7 wang2012 rows if the coordinator counts imaging assistance as facility use.
- Not entered by rule: CMC Microsystems (wang2012, thanked "for making this project possible"; not a fabrication statement,
  simard2013 / lit_49 precedent; the devices were on a multi-project wafer, see Q2). All other papers state fabrication in
  the passive voice or as "we" across several orgs (dolgaleva2011: Toronto / INRS / INESC-Porto) -> empty (D80b, D154).

## Judgment calls

1. lee2012 Q_int kept `measured` (not D403 author_estimate): the paper sets the coupling regime experimentally (taper gap
   moved between under- and over-coupling; spectra taken under-coupled; ring-down cross-checks agree) and labels the record
   value Q_int. The Fig. 2 caption values (one per device) are entered as q_intrinsic with that reasoning in notes.
2. biberman2012 Q0 `author_estimate` (regime not stated); the printed Q0 values are not reproduced by the standard all-pass
   formula from the printed FWHM and the figure-read dip depths (~2.6e7 TE / ~2.1e5 TM under-coupled); printed values kept,
   cross-check in component notes. TM loss 4.34 dB/cm is computed from the printed alpha_TM 0.5 /cm (field convention
   fixed by the TE pair 3.1e-3 /cm <-> 2.7 dB/m).
3. zhang2010 classed mode_converter.converter (TE0 shape conversion between two cross-sections of one Si layer); alternative
   waveguide_platform.transition (but not inter-material). Two width_nm rows per converter with the role in condition.
4. giuntoni2009 reflectivities `author_estimate` (Eq. (1) rests on the nominal 3-dB coupler ratio K = 0.5); bandwidths and
   transmission extinction `measured`. Grating trench depth stored as etch_depth_nm (role in condition); the rib etch is
   expressed via slab_thickness_nm to avoid two etch-depth rows.
5. dolgaleva2011 losses ("our LCBGW") placed on a separate waveguide_platform.straight row because reflector has no
   prop_loss parameter; 3.6 dB total `derived` (sum of the two stated terms). Grating "reflectivity bandwidth" entered as
   stopband_width_nm with the level "not stated" in condition (also giuntoni2009 0.8 / 2.1 nm).
6. Simulated values attached to the fabricated rows when the simulated design equals the fabricated one (giuntoni2009 deep
   grating 2D BEP, tan2009 FDTD / CMT, a2013 FDTD per stage, biberman2012 mode solver) instead of separate design rows.
7. lee2012 wavelength: "the 1,500 nm band" entered as wavelength_nm 1500 without inferred flag (D393 reading); alternative
   band c_band inferred.

## Registry gaps (proposed definition; skipped value + locator)

- reflector `center_wavelength_nm` (Bragg / peak reflection wavelength): wang2012 die -2 ~1515 nm (p.7) and Table 1 means
  1501.69 / 1508.82 / 1508.42 nm (p.10); giuntoni2009 1549 nm (p.6); dolgaleva2011 1550.5 nm (p.2).
- reflector `wavelength_spread_nm` (die-to-die / wafer spread of the Bragg wavelength, statistic in `statistic`): wang2012
  std 17.28 / 5.65 / 5.69 nm, range 50.70 / 19.90 / 20.1 nm (p.10 Table 1).
- reflector `thermal_drift_pm_per_k`: giuntoni2009 77 pm/K, both polarizations, 2.2 um rib, d 150 nm (p.7, Fig. 8).
- reflector group-delay dispersion `dispersion_ps_per_nm` (chirped gratings, sign / definition in condition): dolgaleva2011
  34.8 ps/nm measured by FTSI (p.3, Fig. 3(d)), ~48 ps/nm simulated (p.2).
- reflector lateral coupling gap / perturbation offset (`gap_nm` widened to reflector, definition "distance of a lateral
  grating perturbation from the waveguide edge"): tan2009 d 200 / 50 nm (p.2); scatterer diameter W 200 nm (p.1-2) and
  corrugation width per side (wang2012 10-80 nm, p.5-6) need a `corrugation_width_nm` (design, per side).
- mode_converter `gap_nm`: a2013 0.3 um (p.2), third paper after yang2014 / ding2013 (D418 already lists it); bus-section
  widths 1.02 / 1.68 / 2.35 um need the role parameter proposed in the lit_49 audit.
- resonator FSR-reproducibility (r.m.s. FSR deviation across devices): lee2012 2.4 MHz / 0.45 MHz (p.3, Fig. 3); recommend
  defer (single paper).

## Open questions for the coordinator

1. lee2012 D403 reading (judgment call 1): keep `measured` for experimentally set / identified under-coupling, or apply
   D403 strictly (author_estimate) to the 6 q_intrinsic rows?
2. wang2012 CMC Microsystems: devices on a 6 inch multi-project wafer at imec, CMC thanked "for making this project
   possible". Not a fab org here (simard2013 precedent); if the coordinator reads it as MPW access (D83d / D398), add
   org_cmc_microsystems (in the registry) to fab_org_ids on the 7 rows.
3. SFU Nanoimaging facility (FIB imaging only): facility_org_ids or not, once registered.
