# Batch lit_28 report (distill subagent, 2026-10-29)

Dry-run `batch lit_28: +29 components, +237 metrics; errors 0` (1 WARN: ni2025b m4 / m18 share value 0.65 dB, they differ
by mode TE0 / TE1). ASCII, no e-mail, no quotes (all ten sources `restricted_local_only`). Page-1 title / authors checked
for all ten texts: all match their source rows (nauriyal2019 is the arXiv v1 preprint, see below). Not audited or merged.

## Per paper (components / metrics)

- dumais2017 (2 / 14): three-mode Gaussian-synthesis SOI crossing (crossing.other; 0.007 dB best, derived from 260-crossing
  chain minus reference; Fig. 3 band bound <= 0.025 dB extracted; 4 +/- 4 mdB geometry loss author_estimate; simulated
  Fig. 3 peak and Table I C-band maxima; crosstalk > 40 dB measured / > 60 dB simulated; geometry); Si wire 1.5-3 dB/cm
  (author_estimate, origin not stated). Not entered: foundry-yield prediction <= 20 mdB (hypothetical 300 mm process,
  cited tolerances); optimum-wavelength shift vs width / thickness (no parameter). Fab empty (Huawei Canada, passive
  "were fabricated").
- ni2025b (1 / 32): six-port polarization-insensitive multimode crossing (crossing.other), per mode TE0 / TM0 / TE1 / TM1:
  measured IL / CT bounds 1520-1600 nm (derived, (de)mux pair subtracted), cutback slopes at 1550 nm (measured), nominal
  and +/-20 nm tolerance simulations; footprint, 220 nm, A0 width, n_inputs 3. Two-mode (de)multiplexer pair characterized
  without values (no row). Fab empty (Ningbo / Wenzhou / Zhejiang, passive).
- lin2025 (2 / 26): SiOx/AlOx UV edge coupler (platform silica, D82f): 0.31 / 0.18 dB TE / TM at 375 nm (loopback_half,
  derived: printed formula omits the /2, the printed value implies it), 0.29 / 0.62 dB at 405 nm (author_estimate: the
  405 nm propagation loss used is not stated); simulated per-facet values, band bounds, tip tolerance, 1-dB lateral
  tolerance; geometry incl. SEM tip 61.6 nm, 83 deg sidewall. AlOx waveguide 12.02 / 12.01 dB/cm at 375 nm (scattered-light
  fit). Fab empty (Ghent University, process described without "we fabricated"). Table I (other works) not entered.
- nauriyal2019 (1 / 12): CO2-fused SMF-28 to SiO2 mode converter + SiN nanotaper (fiber_chip_coupler.edge, silica): 1.0 dB
  fused + adhesive, 1.3 dB fused, 2.1 dB unfused (all derived loss breakdowns), WDL 0.6 dB over 1480-1640 nm, simulated
  0.3 dB / 2.5 um tolerance, geometry. Fab org_university_of_rochester ("We fabricate", all authors Rochester), facility
  org_cornell_nanoscale_facility. Not entered: SiN waveguide 0.4 dB (length not stated), vertical 1-dB tolerance 2.4 um
  (gap below).
- ong2018a (3 / 40): AIM MPW displaced-bilayer SiNx GCs: apodized elliptical 2.32 um BOX (-2.56 dB, 46.9 nm; sim -2.28 dB,
  57.7 nm), uniform elliptical 2.32 um BOX (-2.61 dB, 50.7 nm; sim 55.1%), apodized elliptical 6.0 um BOX (-2.73 dB,
  54.1 nm; sim -2.35 dB, 52.1 nm); loopback_half derived; periods, n_periods, stack, interlayer taper. Fab
  org_aim_photonics (MPW runs). Not entered: Table 1 "This work" (-2.73 dB, 47.9 nm, matches neither text design),
  circular / rectangular layouts (figure curves only), duty cycles la/lb (ratio vs fraction ambiguous), interlayer TEOS
  100 nm (gap_nm not allowed), directionality 72.4% (no parameter).
- rasel2026 (5 / 15): four unclad fiber-PWB-fiber bonds by offset ((0,0) 1.41, (20,0) 1.69, (0,10) 2.52, (20,10) 2.92 dB
  mean of 8, fiber_to_fiber) with simulated baselines (0.93 / 1.29 printed, 0.97 / 1.09 read off Fig. 5); clad PWB power
  handling 29 dBm (fails at 30) and 20 dBm for 18 days (C-band inferred from the EDFA). IL wavelength not stated
  (band unspecified). Fab empty (Vanguard tool = equipment; mixed affiliations). Misalignment curves not entered.
- gradkowski2023 (3 / 26): expanded-beam MTP link (fiber_interface.connector): Table I per-coupler 1.68-2.54 dB, 0.86 dB
  non-uniformity, P1 2.3 dB, process stages 0.7 / 1.9 dB, mating statistics (P1 ~2.4, P2 2.3-2.4 dB), simulated 1.02 dB,
  1-dB tolerances (14-15 um measured; 23 / 19.45 / 13.7 um simulated; axial 1.7 mm), 50 um beam (spec); PIC micro-lens
  (micro_optics.facet_lens: 2.35 um measured / 3.5 um simulated tolerance, ROC 192 um, 600 um thick); LioniX reference-PIC
  SiN edge coupler (air 3-4 dB, index-matched 1-1.5 dB, WDL 0.5 dB, tolerance 2.1-2.7 um, MFD 6.8 x 6.2 um measured vs
  10 um design; fab org_lionix_international "fabricated by Lionix"). Not entered: loopback-product tolerances 9.1 / 11.4 /
  20 um, angular tolerance curve.
- zhang2022 (1 / 20): 7-core 6-mode fused-taper Fi/Fo (fiber_interface.fan_out): per-mode mean over 7 cores (abstract
  values; Sec. 4 text swaps LP11a / LP11b, Table 5 means confirm the abstract), per-mode range over cores with center-core
  value in notes, simulated Table 4 totals, 42 channels, bundle pitch 41.8 um. Fab empty (HUST + YOFC, not unambiguous).
  Not entered: misalignment excess loss (Fig. 8), 7-core 6-mode fiber itself.
- bauters2013 (10 / 40): Si3N4 TE-pass polarizers (polarization.other, per_db): 40 nm cores straight 12 dB, 8 s-bends 4 um
  42.6 dB / TE <= 8 dB, 5 um 36.8 dB / TE < 1 dB, 28 mm s-bend 3.5 um 58-75 dB / TE < 0.3 dB, 1 m spiral >= 75 dB; 100 nm
  cores s-bend 38-62 dB / TE 0.4 dB, thin-clad straight up to 40 dB, thin-clad s-bend TE 6 dB; 100 nm x 6 um waveguide 1.2 /
  0.6 dB/m TE / TM (derived to dB/cm); simulated 40 nm x 5 um fiber coupling 0.87 / 0.91 dB (design row). Not entered:
  TE < 0.1 dB/m for 40 nm cores (restated from ref. [14], D259), group birefringence (no parameter), 180 nm simulated
  bandwidth (no parameter). Fab: 100 nm rows org_aurrion (acknowledged for fabrication, borderline D84b); 40 nm rows empty
  (see orgs).
- chen2021 (1 / 14): adiabatic LNOI PSR (polarization.psr, lnoi_rib): port crosstalk ~8 / ~10 dB as per_db (measured),
  simulated 16.2 / 23.9 dB, conversion loss ~2 / ~3 dB (author_estimate: rests on cited 6 dB/facet coupling), geometry.
  Fab org_city_university_of_hong_kong ("We fabricate", all CityU). Not entered: simulated 99.6 / 97.6% efficiency, taper
  lengths 4000 / 3000 um (gaps below), ~2 dB/cm platform loss (resonator data not in this paper), bandwidth claims.

## Orgs missing (fab / facility)

- LioniX BV (bauters2013 p.8 Acknowledgment, 40 nm waveguide fabrication): registry has only `org_lionix_international`
  (later entity); coordinator to decide time-correct mapping (D80d analogue) or a new org.
- SUSS Micro-Optics (gradkowski2023 p.4 Sec. III, vendor of the purchased micro-lens; registry has SUSS MicroTec only).
- Molex (gradkowski2023 p.4 Sec. III, VersaBeam MTP connector vendor; part of the link row, fab left empty).

## Judgment calls

- Polarization crosstalk / polarizer extinction entered as `per_db` (bauters2013, chen2021); the merged wang2014 polarizer
  rows use `extinction_db`: coordinator to fix one convention.
- rasel2026 fiber-to-fiber PWBs classed fiber_chip_coupler.photonic_wire_bond (fiber-array PWB study, no chip); one row
  per offset design (sibling geometries). power_handling_dbm 29 entered without qualifier (failed at 30 dBm).
- gradkowski2023: link values on the connector row, lens tolerances on a separate micro_optics row (D396 spirit);
  per-coupler loopback values with connector losses corrected scoped loopback_half, derived.
- dumais2017 / ni2025b crossings `crossing.other` (dumais: authors say not an MMI; ni2025b: hole-pattern inverse design).
- ong2018a fab: AIM Photonics only; SUNY Poly named as compatible foundry, not as fabricator.
- nauriyal2019: cached text is the arXiv v1 preprint (page-1 title "Fiber to Chip Fusion Splicing for Robust, Low Loss
  Photonic Packaging", same authors) of the Optica paper of the source row; values taken from the preprint.

## Registry gaps

- `taper_length_um` for polarization: chen2021 Step I taper 4000 um (p.2 Fig. 1(a)) and Step II slow taper 3000 um (p.2
  Sec. 2) skipped. Proposed: allow taper_length_um (and gap_nm, for adiabatic-coupler PSR / PBS sections) for polarization.
- `crosstalk_db` for polarization: chen2021 port polarization crosstalk (p.4) entered as per_db; proposed: allow crosstalk_db
  for polarization (PSR / PBS port crosstalk) or confirm per_db as the convention.
- `conversion_efficiency_pct` (or coupling_efficiency_pct) for polarization: chen2021 simulated 99.6% / 97.6% (p.3)
  skipped. Proposed: polarization conversion / transmission efficiency in %, linear as reported.
- `tol_1db_vertical_um` (fiber_chip_coupler, micro_optics, fiber_interface): nauriyal2019 vertical 1-dB tolerance 2.4 um
  (p.4-5 Fig. 5) skipped; lin2025 axial (vertical) +/-0.5 um only noted. Proposed: vertical (out-of-plane) misalignment
  for 1 dB excess loss, half-width.
- `center_wavelength_nm` (or a wavelength-sensitivity parameter) for crossing: dumais2017 optimum wavelength 1547.5 nm and
  +15 nm per +10 nm width bias (p.2 Fig. 4, Table I) skipped. Proposed: center_wavelength_nm allowed for crossing
  (wavelength of minimum loss).
- `gap_nm` for fiber_chip_coupler: ong2018a 100 nm TEOS between the two SiNx grating layers (p.3) skipped. Proposed: allow
  gap_nm (interlayer spacing of bilayer / dual-layer gratings).
