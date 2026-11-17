# lit_173 batch report

Distilled 2026-11-16 under the pic-component-distill skill (Contracts v4-v7). Papers: lit:lu2018, lit:giuntoni2012,
lit:luke2013, lit:burla2015, lit:guillentorres2014. Totals: 13 components, 85 metric rows.
`merge_component_staging.py --dry-run`: +13 components, +85 metrics, 0 errors (the one warning printed belongs to
merged row cmp_lit_ni2025b_pimmwc, not this batch).

Page-1 title check: all five cached texts are their source rows' papers; none is a correction / erratum; no garbled
text layer flagged. The papers were selected as benchmark-table citations; only values each paper reports as its own
result are entered (rules 1 and 3).

## lit:lu2018 - 7 components, 40 metric rows

AlN on sapphire (platform `other`, D515), purchased Kyma Technologies wafers (200 +/- 10 nm c-plane AlN on 430 um
sapphire; supplier in notes, thicknesses `design_target`, D402).

| component | class | metrics |
|---|---|---|
| cmp_lit_lu2018_ring_r40_sion | resonator.ring | 10 (Q 24,118 at 369.492 nm; 75 dB/cm author_estimate; ng 2.45; FSR 0.22-0.4 nm; best OSA Q about 7.2e4 near 474 nm read off Fig. 4(c); geometry) |
| cmp_lit_lu2018_ring_r50_pmma | resonator.ring | 10 (Q_L 140,947 at 637.996 nm; Q_i > 170,000 and 5.3 dB/cm author_estimate (D403); ng 2.15; notch about 3.9 dB read off Fig. 4(d); geometry) |
| cmp_lit_lu2018_gc_green | fiber_chip_coupler.grating | 4 (measured peak 532.9 nm; simulated peak about 19.5 % near 506 nm read off Fig. 3(b); periods 285-346 nm; 200 nm etch) |
| cmp_lit_lu2018_gc_red | fiber_chip_coupler.grating | 4 (measured peak 625.3 nm; simulated peak about 24.5 % near 610 nm; periods 285-414 nm; 200 nm etch) |
| cmp_lit_lu2018_edge_coupler_uv | fiber_chip_coupler.edge | 2 (facet-to-facet transmission >= 40 %, device_total; SiON 3 um) |
| cmp_lit_lu2018_dbr_532 | reflector.bragg | 6 (extinction > 13 dB measured, 45 dB simulated at 532 nm; 140 nm period; fill 0.5; ~735 nm wide sections) |
| cmp_lit_lu2018_dc_637 | splitter.directional_coupler | 4 (50/50 at 14 um coupling length, 637 nm; gap 200 nm; 0-25 um series) |

Values not entered and why:
- Measured grating-coupler transmissions 0.1544 / 0.1565 a.u.: arbitrary units (objective not mode-matched, p.7);
  only the peak wavelengths are entered.
- Ring gap 300 nm (Fig. 4(a) caption): the caption does not say which ring (radius, cladding) the SEM shows (D159);
  in component notes.
- Ti:Sapphire Q points at 369.5 nm in Fig. 4(c) (about 1.4e4-2.3e4): only the Fig. 4(b) fit is entered.
- Material data (AFM roughness 0.9 nm RMS, XRD FWHM 0.12 / 0.20 deg, refractive index, autofluorescence counts): no
  component parameter.
- Simulated directional-coupler lengths (23 um coupled-mode, 14 um full simulation): in notes (the row is the
  coupling-length series, D165).
- Table 1 values of AlN on SiO2 / SiN on SiO2 and the chi(2), r33, d33, n2, dn/dT figures: cited (rule 3).

Judgment calls:
- Unqualified Q on the UV ring stored as `q_loaded` (pitfall); the paper treats it as the loss-limited Q of an
  undercoupled ring. The 75 dB/cm derived from it is `author_estimate` (rests on that treatment and on the stated
  scattering / absorption assumption).
- 638 nm ring: Q_i > 170,000 `author_estimate` (D403: regime stated, T0 not printed; the gap-series evidence is
  described for the UV rings). The Fig. 4(d) read (T0 about 0.40) reproduces Q_i about 1.73e5 and the printed
  5.3 dB/cm, noted on the rows.
- Edge coupler: the only number is the facet-to-facet transmission ">= 40 %", entered as `coupling_efficiency_pct`
  scope `device_total` with the stitching-loss caveat; wavelength 360-480 nm inferred from the UV range in which all
  edge-coupled measurements were made.
- Ring widths 250 / 450 nm from the Fig. 2(c) caption, tied to the rings by p.9 ("wrapping these waveguides into
  rings").
- Directional coupler kept as one series row (D165): Fig. 5(d) has no device at exactly 14 um (points at 12.5 and
  15 um); the 50/50 statement is the paper's interpolation.
- Sidewall angle "close to 90 degrees" entered as `measured` approx (stated fabrication outcome, SEM shown).
- Fab empty on all rows: fabrication section mostly passive, authors at MIT, RIT, AFRL and Raytheon BBN (D80b,
  D154); no facility acknowledged.

Missing fab / facility orgs: none.

## lit:giuntoni2012 - 1 component, 9 metric rows

| component | class | metrics |
|---|---|---|
| cmp_lit_giuntoni2012_tapered_bragg_drop_filter | reflector.bragg | 9 (1.2 nm band at 1535.4 nm (level not stated, `stopband_width_nm`, dolgaleva2011 / li2023a precedent); drop-path loss 1.7-6 dB `de_embedded` over the band and for the 1535.8 nm signal over 32-41 C; period 224 nm, grating etch 50 nm, 1 cm, rib 1.5 um, Si 1.4 um, BOX 1 um) |

Values not entered and why:
- Delay quantities (group delay 500 ps over the band, 250 ps per grating pair; tuning almost 0-440 ps, abstract
  450 ps; -51 ps/C; dispersion 500 ps/nm; Table 1 loss figure 9.6 dB/ns): no registry parameter (gap below).
- Bragg shift 80 pm/C observed on p.4: `thermal_drift_pm_per_k` is not allowed for `reflector` (gap below); the
  same number in Sec. 2 cites refs. [14,15].
- "linear loss around 0.2 dB/cm" (p.3): design aim of the rib geometry, not a measurement.
- Sec. 4 BER / data-rate results: VPI emulations of a system (with a fictitious compensating filter).
- Rib height 0.5 um: not entered as an etch depth (etch_depth_nm holds the 50 nm grating etch; avoids two meanings
  on one row); in notes.

Judgment calls:
- Class `reflector.bragg` for a chirped Bragg-grating drop-filter delay line (li2023a, sun2021 precedents).
- Fab empty: "was manufactured using a double lithographic process based on Deep-UV 248 nm lithography" is passive
  and names no org (authors at TU Berlin and IHP; D80b); no process name printed (lithography wording only).

Missing fab / facility orgs: none.

## lit:luke2013 - 1 component, 11 metric rows

| component | class | metrics |
|---|---|---|
| cmp_lit_luke2013_sin_ring_r115 | resonator.ring | 11 (TE linewidth 36 MHz at 1554.8 nm; extinction 5.85 dB derived from 26 % transmission; Q_i 7e6 and 4.2 dB/m author_estimate (D403); TM Q 4e6 as q_loaded; FSR 2.0 nm; R 115 um, gap 680 nm, 1800 x 910 nm, cladding 2.25 um derived) |

Values not entered and why:
- Absorption loss 3.0 dB/m and its 71 % share: computed for the devices of ref. [18] (rule 3).
- Loaded Q: not printed (not derived from the linewidth).
- Simulated modal confinement 71 % / 93 % (Fig. 1): no parameter.

Judgment calls:
- Q_i 7e6 `author_estimate` (D403: the paper does not state how the coupling regime was fixed); 4.2 dB/m stored as
  0.042 dB/cm keeps `author_estimate` (D256a).
- TM "Q of 4 million" stored as `q_loaded` (unqualified Q, pitfall) with a note that the sentence compares it with the
  TE intrinsic Q; wavelength C band inferred.
- Fab `org_cornell_university`: first-person fabrication steps, all authors at Cornell (D72). The Cornell Center for
  Materials Research line is funding, not a facility (D80c).

Missing fab / facility orgs: none.

## lit:burla2015 - 1 component, 12 metric rows

| component | class | metrics |
|---|---|---|
| cmp_lit_burla2015_mmwg_racetrack_r450 | resonator.ring | 12 (Q about 1.32e6 near 1550.975 nm; 0.3 dB/cm fit author_estimate; notch about 7.4 dB and FSR about 0.16 nm read off Fig. 4; 146 MHz author_estimate; simulated ng 3.7081; R 450 um, Lc 585 um, gap 140 nm, 3000 nm MMWG, 220 nm) |

Values not entered and why:
- RF notch-filter results (notch about 150 MHz, tuning 0.97-8.34 GHz, cancellation up to 60 dB): system-level
  microwave-photonic filter with an external DP-MZM, laser and EDFAs.
- Table I design coupling coefficients: symbols garbled in the text layer and the definition (field vs power
  coefficient; the printed values approximately match sqrt(1 - t^2)) is ambiguous.
- Crossover length 7.802 mm, supermode indices 2.82976 / 2.82966, effective index 2.8328: simulated, no parameter
  (effective index in notes).
- Sibling designs (Lc 260-825 um in 20 um steps, radii 300 / 180 um): no values.
- 2.12 GHz FSR, 113 MHz and 1.5e6 of ref. [5]: cited (rule 3).

Judgment calls:
- Platform `soi`: the paper states a standard SOI process but not whether the 3000 nm MMWG is rib or strip.
- 0.3 dB/cm `author_estimate`: model fit whose coupling regime / inputs are not stated (D403 analogue).
- 146 MHz "resonator" width `author_estimate`: origin not stated; it equals c / (lambda Q) for Q 1.32e6 near 1551 nm;
  band c_band inferred (the filter used the 1557.1 nm resonance).
- Gap 140 nm is the design-procedure gap for the 584.23 um / 0.3 dB/cm design; the measured device (Lc 585 um)
  matches that design but its gap is not restated (noted).
- Fab `org_university_washington` from "realized via electron beam lithography at Microfabrication Facility of the
  University of Washington" (simard2015 / eid2016 precedent).

Missing fab / facility orgs:
- "Microfabrication Facility of the University of Washington" (p.3 Sec. II-D; p.4 acknowledgments "Microfabrication
  Facility at the University of Washington"): facility role (and fab place); not in the registry. Earlier batches
  reported the same site as "University of Washington Nanofabrication Facility" / "Washington Nanofabrication
  Facility" (D420, wang2016a) and "University of Washington Microfabrication/Nanotechnology User Facility"
  (shi2013a); one org with these aliases would cover all.

## lit:guillentorres2014 - 3 components, 13 metric rows

| component | class | metrics |
|---|---|---|
| cmp_lit_guillentorres2014_mmwg_rib | waveguide_platform.straight | 4 (0.085 dB/cm cutback, 1500-1570 nm inferred; 3 um rib, 220 nm, 90 nm slab) |
| cmp_lit_guillentorres2014_bends_tapers | waveguide_platform.other | 4 (0.07 dB for 40 adiabatic bends + tapers, derived, on_chip_excess; taper 100 um; 500 nm SMWG; 220 nm) |
| cmp_lit_guillentorres2014_ring_37p7mm | resonator.ring | 5 (Q_L 1.7e6 and FWHM 0.91 pm at 1550.803 nm; FSR 17.1 pm derived; 20 dB insertion loss scope unspecified; 37.7 mm) |

Values not entered and why:
- Excess loss per pass 0.8 dB (p.2): no round-trip loss parameter (gap below); it is an author estimate from Q_L and a
  Q_i that is not printed.
- Qcc about 4e6: hypothetical critically coupled ring built only of MMWG.
- Angular-velocity resolutions 0.018 / 0.5 deg/s: gyroscope system estimates (the 0.018 deg/s case assumes a 1 dB insertion loss and a hypothetical ring).
- Slab width 5.1 um: no parameter (in notes).
- Cited Qs (35e6, 22e6, 9e6, 7.6e5 / 5.11e5, 5.1e5 / 2.8e5): rule 3.

Judgment calls:
- 0.07 dB bends + tapers: a separate `waveguide_platform.other` row (the set of 40 bends and tapers; per-element split
  not printed), `derived` (difference of the extrapolated zero-length loss and a reference loopback, "we estimate").
- Wavelength of the loss values: the averaging span is not stated; 1500-1570 nm from the Fig. 1(b) axis, inferred.
- 20 dB ring insertion loss kept with scope `unspecified` (what it includes is not stated).
- Fab `org_astar_ime` on all three rows ("fabricated ... at IME, Singapore"; acknowledgment "IME Singapore for
  fabrication"); process wording "standard CMOS-compatible SOI process" names no node or flow, so `process_name` is
  empty. CMC Microsystems (equipment and financial support) not entered (no fabrication wording; wang2012 / D425).

Missing fab / facility orgs: none.

## Registry gaps (skipped value + locator + proposed definition)

- `group_delay_ps` / `delay_tuning_range_ps` (reflector, wdm): giuntoni2012 500 ps over the band and 0-440 ps
  tuning at 1535.8 nm (p.3-4, Fig. 3). Proposed: "group delay (or its tunable range) added by a dispersive or
  delay-line component at the stated wavelength and tuning condition".
- `delay_tuning_coefficient_ps_per_k` (reflector): giuntoni2012 -51 ps/C (p.4). Proposed: "delay change per kelvin
  of a thermally tuned delay line (sign as printed)".
- `dispersion_ps_per_nm` (reflector, wdm): giuntoni2012 500 ps/nm (p.4). Proposed: "group-delay dispersion of a
  chirped grating / filter, ps/nm, sign as printed".
- `thermal_drift_pm_per_k` on reflector: giuntoni2012 80 pm/C Bragg shift (p.4) (also D430 candidate).
- `roundtrip_loss_db` (resonator): guillentorres2014 excess loss per pass 0.8 dB (p.2). Proposed: "loss per round
  trip of a resonator, or the stated part of it, positive dB".
