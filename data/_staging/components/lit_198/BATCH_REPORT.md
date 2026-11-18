# lit_198 batch report

Distilled 2026-11-18. Papers: dai2012, feng2014, scarcella2017, sakaguchi2015. Totals: 10 components, 71 metric rows.
`merge_component_staging.py data/_staging/components/lit_198 --dry-run`: +10 components, +71 metrics, 0 errors (the one
warning is on the merged row `cmp_lit_ni2025b_pimmwc`, not this batch).

Page-1 identity: all four cached texts are the listed works (IEEE publisher PDFs; download stamps ignored). sakaguchi2015
is the JLT paper printed in vol. 34 no. 1 (January 2016 issue, the registry keeps 2015). No values come from other papers.

## dai2012 (3 components, 26 metrics)

- `mzi_pbs` (polarization.pbs, soi): ER > 10 dB over 1540-1580 nm (both polarizations); highest ER about 25 dB (TE,
  around 1540 nm) and about 16 dB (TM, around 1590 nm) as `per_db`; the two highest-ER wavelengths as
  `center_wavelength_nm`; four figure-read insertion losses from Fig. 3 (spectra normalized by a straight waveguide):
  TE through about 1.7 dB at 1540 nm and about 2.0 dB at 1550 nm, TM cross about 1.4 dB at 1550 nm and about 3.4 dB at
  1590 nm (Fabry-Perot ripple +/-0.4 to +/-0.8 dB, in notes); geometry: 400 nm Si, 250 nm rib height and 150 nm slab
  (derived) at the I/O rib, rib width 1 um, arm widths 1.46 / 1.00 um, arm section 82 um, total about 200 um.
- `mmi_2x2` (splitter.mmi): excess loss < 0.5 dB `author_estimate`; 3.36 x 45.9 um, 2 x 2 ports, 400 nm Si.
- `bilevel_taper` (waveguide_platform.other): < 0.5 dB `author_estimate`, 100 um long.
- Not entered: facet coupling about 30 dB (setup, p.2); "ER expected to be as high as 15 dB" after process improvement
  (expectation); Fig. 2 design curve (simulated design procedure of ref. [17]); 20 um cosine arm tapers (no taper
  parameter on polarization); the 1.36 um gap between MMI access waveguides (no role-specific parameter).
- Orgs: fab `org_ucsb` on all three rows (borderline, see judgment call 1). No facility.

## feng2014 (1 component, 13 metrics)

- `vdc_pbs_3d` (polarization.pbs, sin): ER about 26 dB "for the cross-layer output-port" and about 16 dB for the
  input-layer port at 1550 nm, ER > 16 dB over about 1535-1565 nm (`per_db`); TE excess coupling loss < 0.1 dB and TM about
  1 dB against a single-layer reference waveguide (`insertion_loss_db`, per_component, reference_structure, C band
  inferred); geometry: 200 nm Si3N4 per layer, top / bottom core widths 1.35 / 1.55 um, I/O width 2 um, etch about 220 nm
  (`author_estimate`, D456), 4 um buffer, 3 um cladding, 800 um total length.
- Not entered: vertical gap 920 nm (SEM), coupling length 16 um, S-bend 270 um / 20 um offset / radius about 900 um
  (registry gaps below); calculated index mismatch 0.023 and coupling length about 21 um (no parameter); qualitative
  bend-loss and CMP-roughness observations; other width combinations of the coupler array (no numbers).
- Orgs: fab `org_national_institute_of_advanced_industrial_science_and_technology` (both authors at AIST, first-person
  fabrication statements p.2). No facility.

## scarcella2017 (3 components, 23 metrics)

- `gc_1310_plain_fa` (fiber_chip_coupler.grating, platform empty): fiber-to-fiber 3.4 dB (two GCs, plain fiber array),
  1.7 dB / 68 % `loopback_half` derived, 1-dB lateral tolerance +/-2.5 um (measured), 10 deg acceptance angle, peak about
  1300 nm (figure read).
- `ulens_pair` (micro_optics.other): fiber-to-fiber 3.4 dB, 1.7 dB / 68 % `loopback_half` derived at 1300 nm, 1-dB
  tolerances +/-30 um across and +/-22 um along the GC axis (measured), +/-25 um (Zemax), lens-to-FA assembly +/-2.5 um
  (measured), lens array over GC +/-2.5 um (Zemax); centre wavelength about 1300 nm (across) and 1275-1325 nm (along,
  +/-60 um); lens radius 315 um (derived from 0.315 mm), pitch 250 um, 8 channels, AOI 10 deg.
- `pluggable_connector` (fiber_interface.connector): 30 make / break trials, mean 2.1 dB / 62 %, std 0.2 dB
  (`loopback_half` derived, O band inferred).
- Not entered: the "adds just 0.4 dB" difference (2.1 - 1.7 dB arithmetic); 7.5 nm centre shift per 1 deg AOI on the
  plain FA and the about 7x larger angular sensitivity with lenses (no parameter); derived 7 deg and geometric 9 deg
  internal AOI changes; lens NA 0.16 (no parameter); loopback spectral widths (no printed value, not read).
- Orgs: fab `org_cea_leti` + process_name "MPW run at the CEA-Leti photonic foundry" on the GC row only. Lens arrays are
  the commercial Axetris FCA250FS part (vendor of a purchased part = fab, rule 12): missing org, fab left empty on the
  two lens rows. Assembly (bonding, Lego armature) by unnamed people; authors at Tyndall (6) and CEA-Leti (1), so no
  own-org fab. No facility.

## sakaguchi2015 (3 components, 9 metrics)

- `sdm_mdm_mux_108ch` (mode_converter.mdm_mux, other): IL 6.3-6.9 dB (LP01) and 7.5-9.4 dB (LP11a/b) per core and mode,
  108 inputs.
- `sdm_demux_36ch` (fiber_interface.fan_out, other): IL about 0.5-1 dB (LP01), 1.4-3.8 dB (LP11), 36 channels.
- `mdm_demux_3mode` (mode_converter.mdm_mux, other): IL 3.5 dB (LP01), 8.6 dB (LP11), 3 outputs.
- All IL rows `device_total`, measured, C band inferred (wavelength not printed for the MUX / DEMUX losses).
- Not entered: the 36-core three-mode transmission fiber itself (Table II losses 0.242-0.308 dB/km, cable cutoffs,
  effective areas, DMD, calculated core-to-core crosstalk, Fig. 2 crosstalk vs bending radius), see judgment call 4;
  link-level values that include the 5.5 km fiber and splices (input-to-output loss 8.3-10 dB LP01 / 11-14.6 dB LP11 at
  1550 nm, aggregated crosstalk -16.3 / -17.0 dB worst case, Fig. 8 histograms, OSNR penalties, BER, 403.7 Tb/s; D542);
  Fig. 5 simulated quasi-LP11 intensity (no number); about 2 dB lower LP11 coupling efficiency (restates the IL ranges).
- Orgs: none. The MUX / DEMUX maker is not stated ("we successfully realized"); Optoquest (two authors' affiliation,
  free-space optics subsystems per their bios) is affiliation only. Fujikura is the splicer vendor (setup equipment).

## Judgment calls

1. dai2012 fab `org_ucsb`: first-person "In our fabrication" (p.2) and "We have designed and fabricated" (p.3); every
   author prints UCSB ECE, the first author also Zhejiang University. UCSB is the one org common to all authors (rule
   12 / D72, D452 analogue); the site is not printed, so borderline (hiratani2024 D433 went empty with dual affiliations).
2. dai2012 figure-read insertion losses (4 rows) added although the text prints no IL: spectra are normalized to a straight
   waveguide, so scope `per_component` / `reference_structure`; ripple is large (up to +/-0.8 dB) and in notes. The
   "e.g., <0.5 dB" sentence is entered on both the MMI and bi-level-taper rows as `author_estimate` (origin not stated).
   The bi-level taper is `waveguide_platform.other` (one Si layer, not an inter-layer transition).
3. feng2014 port-label conflict (D417): Fig. 3 at 1550 nm gives about 16 dB at the bottom (cross-layer) port and about
   25-26 dB at the top (input-layer) port, the reverse of the printed assignment; both printed values kept with notes.
   ER of a PBS stored as `per_db` (merged majority: 94 per_db vs 2 extinction_db rows on polarization.pbs).
4. sakaguchi2015: the transmission fiber is not a component row (no class for a link fiber; no merged precedent for
   fiber dB/km rows); the free-space MUX / DEMUX units are in scope as fiber-coupled passive parts with fiber in and out
   (D411; jung2018 collimator pairs, oh2023 metasurface fan-out, shikama2017 FI/FO), unlike fontaine2019 (D642, camera
   output). Platform `other` for free-space optics (jung2018 precedent).
5. scarcella2017: three rows (GC, bench lens pair, pluggable connector) by class (D396); the paper's IL is half the
   shunt loss, so all IL / efficiency values derived from it are `loopback_half` + `derived` (D542), the 3.4 dB
   fiber-to-fiber values `measured`. The +/-30 / +/-22 um tolerances are 1 dB on the halved IL (2 dB on the shunt), noted.
   GC platform left empty (only "Si-PIC" for this chip; SOI only in the general introduction, D423).
6. scarcella2017 Axetris lens arrays treated as purchased parts whose vendor would be fab; left empty pending the org round.

## Missing orgs

- Axetris (Axetris AG), fab (vendor of the purchased micro-lens arrays FCA250FS) for `cmp_lit_scarcella2017_ulens_pair`
  and `cmp_lit_scarcella2017_pluggable_connector`; locator lit:scarcella2017 p.2 Sec. II (ref. [11]).

## Registry gaps

- `gap_nm` on polarization: feng2014 vertical coupling gap 920 nm (SEM, p.2 Fig. 2; also p.3, p.4); definition as for
  splitter (coupling gap, vertical for multilayer couplers). Same gap as D439 / D559.
- `coupling_length_um` on polarization: feng2014 overlapping straight section 16 um (p.2); as for splitter.
- `min_bend_radius_um` on polarization: feng2014 S-bend radius about 900 um (p.2, p.3).
- `taper_length_um` on polarization: dai2012 20 um cosine tapers inside the MZI arms (p.1-2).
- Angular sensitivity of a grating coupler / lens coupling (centre-wavelength shift per degree of angle of incidence,
  nm/deg): scarcella2017 7.5 nm per 1 deg with the plain FA (p.3), about 7x larger with the lens pair (p.3 Fig. 5(c)).
- `numerical_aperture` on micro_optics: scarcella2017 lens NA 0.16 (p.1; D437 candidate).
