# lit_309 batch report

Distilled 2026-11-27. Papers: lit:molesky2018, lit:jiang2019, lit:bauters2011a, lit:wang2019a. Result: 8 component
rows, 80 metric rows; `merge_component_staging.py --dry-run`: +8 components, +80 metrics, 0 errors (the 2 warnings
name merged rows of other batches). Page-1 titles checked: jiang2019 and bauters2011a are the Optics Express versions
of their source rows; molesky2018 and wang2019a are arXiv v1 preprints of the listed journal works (titles differ, see
below). No cached file is another paper or a correction / erratum. Values from the cached text and page renders only.

## lit:molesky2018 (review, arXiv 1801.06715 v1)

Components: 0. Metric rows: 0.

The preprint is titled "Outlook for inverse design in nanophotonics" (journal title "Inverse design in
nanophotonics"); same author list and scope, accepted as the same work (D430 / D433 precedent). Values from the
preprint only.

Values not entered and why:
- Every device number in the review is credited to cited work (rule 3, D259 / D408): Spuhler et al. SiO2/SiON coupler
  2 dB gain (p.2, ref. 21), Cox-Dobson bandgap +34 % (p.2, ref. 22), photonic-crystal bend < 1 % loss (p.3, ref. 25),
  slow-light group index ~300 (p.5, ref. 77), Purcell tripling (p.5, ref. 80), nonlinear FOM gains (Fig. 2, refs.
  73-75), metagrating 75 % efficiency (Fig. 5, ref. 115), splitter 69.5 % (p.9, ref. 40), sub-5 dB WDM splitters
  (p.10, refs. 35 / 36) and the three-port splitter >= 23 % per port over 1400-1700 nm (p.10, ref. 37).
- Fig. 6 measured spectra of the two- and three-channel wavelength splitters are reproduced from the co-authors' own
  earlier papers (Piggott et al., refs. 36 / 37): D259 / D408, not entered.
- Fig. 3 topology-optimized exceptional-point lattice (ref. 85) and Fig. 4 applications: cited work, no own device.

Missing fab / facility orgs: none (no rows).

## lit:jiang2019 (Optics Express, simulation-only design)

Components: 2 (both `row_kind: design`, `mode_converter.other`, platform `soi`). Metric rows: 25.
- `cmp_lit_jiang2019_tm1_pass_filter_4stage` (15): TM1 IL 0.63 dB, mode ER 26.4 dB, ER > 15 dB over 1433-1588 nm,
  3-dB BW 493 nm, 1-dB BW > 100 nm, TE0 / TE1 IL 41.6 / 51.5 dB, ER > 24.0 dB (width error +/-50 nm), ER > 23.1 dB
  (bridge offset +/-20 nm), length < 260 um, plus geometry (220 nm, W 2 um, Wb 100 nm, pitch 250 nm, taper 25 um).
- `cmp_lit_jiang2019_tm1_pass_filter_1stage` (10): TM1 IL 0.19 dB, TM0 IL 3.4 dB, 1-dB BW 512 nm, 3-dB BW > 600 nm,
  ER < 3.4 dB over the simulated band, same geometry.

Values not entered and why:
- Table 1 and the introduction values of other HOM-pass filters (p.2-3, p.10): cited work, rule 3.
- Fig. 2 / Fig. 4 effective-index curves (TM1 n_eff > 1.5 at W = 2 um, p.5): mode-solver data, no registry parameter.
- TM1 power transfer efficiency > 95.5 % for N >= 100 taper pitches (p.7 Fig. 5): same quantity as the 0.19 dB TM1 IL
  at N = 100; noted on the 1-stage row.
- Al bridge section length Lb = 12.5 um: no role-specific parameter (noted in component notes; `length_um` holds the
  stated total device length instead).
- TM1 IL deterioration < 0.5 dB / < 0.11 dB under the tolerance sweeps: change values, kept in the conditions of the
  ER tolerance rows.
- Single-stage TM0 IL 3.4 dB is entered as the rejected-mode loss; the single-stage ER at 1550 nm is not printed.

Judgment calls:
- Mode filter class `mode_converter.other` and mode ER as `extinction_db` (zhang2022a / dagostino2015 precedent).
- Wavelength 1550 nm `wavelength_inferred: true` on the propagation rows: Sec. 3 fixes the design wavelength at
  1550 nm, the propagation sections do not restate it.
- "Over 100 nm from 1518 to 1618 nm" entered as 100 `gt` (rule 7), range in the condition; abstract "over 493 nm" vs
  p.8 "calculated to be 493 nm": entered without qualifier, both quoted.
- W = 2 um entered as width_nm 2000 `derived` (unit rescale, D157); Wb and pitch printed in nm stay `design_target`.
- Cladding SiO2 entered from the proposed fabrication sequence (p.4); no fabrication was done, fab / facility empty.

Missing fab / facility orgs: none (design only).

## lit:bauters2011a (Optics Express, UCSB / LioniX)

Components: 3 (`waveguide_platform.straight`, platform `sin`, one per core thickness 80 / 90 / 100 nm, test
structures). Metric rows: 35.
- Per row: OFDR propagation loss (2.91 / 4.22 / 5.33 dB/m -> 0.0291 / 0.0422 / 0.0533 dB/cm, `derived`), OFDR group
  index 1.54 / 1.57 / 1.59 (`measured`), FIMMWAVE group index 1.53 / 1.55 / 1.57 (`simulated`), ring-resonator loss
  at R = 1, 1.5, 2, 4 mm read off Fig. 5(a) (`extracted_from_figure`, +/-0.3 dB/m), core thickness, width 2.8 um,
  lower / upper cladding 8 / 7.5 um (Fig. 1(a) labels).
- 100 nm row also: 8-9 dB/m at 0.5 mm bend radius (text, `derived`). 80 nm row also: 3 dB/m at 2 mm bend radius (text,
  method unspecified, `derived`).

Values not entered and why:
- Conclusion "8-9, 5, 3.5, and 3 dB/m at 0.5, 1, 1.5, and 2 mm" (p.12): the 1 mm (5 dB/m) and 1.5 mm (3.5 dB/m) values
  name no core thickness and do not match one series in Fig. 5(a) unambiguously (D159); the bounds are in the
  component notes. The 0.5 mm and 2 mm values are entered from the p.10-11 sentences that name the thickness.
- 90 nm point at 0.5 mm (at the 25 dB/m plot edge) and the off-scale 80 nm 0.5 mm point: not entered.
- Model projections: green curve ~17 dB/m at 0.2 mm to ~1 dB/m at 10 mm (p.11) and 0.1 dB/m at 7 mm with the
  sidewall roughness 3.16 nm taken from ref. [15] (p.1, p.11): a model envelope of lowest-loss geometries, not one
  design; the 0.1 dB/m projection rests on a cited input (rule 3).
- Fitted roughness parameters (sigma, Lc), substrate leakage ~0.001 dB/m and the 33.41 dB/cm model check against ref.
  [18] (p.4, p.6, p.9): model values, not component results (the last is cited work).
- Fig. 5(b) typical spectrum of a 100 nm, 4 mm ring: no printed Q / linewidth / extinction, not read off.
- Ring coupling design (gap ~2 um, kappa ~0.01, three coupling lengths): design of the test structures, in notes.
- Fig. 7 literature points (other works): rule 3.

Judgment calls:
- One row per core thickness, class `waveguide_platform.straight`, with each ring's bend radius in the condition
  (D32 / D81: bend values use prop_loss_db_per_cm with the radius in the condition). An auditor may prefer splitting
  the bend-limited points (0.5-1 mm) into `waveguide_platform.bend` rows.
- 80 nm "3 dB/m at 2 mm" entered as a separate text row next to the Fig. 5(a) ring reading (~3.5 dB/m) and the OFDR
  2.91 dB/m: the sentence does not say which measurement it reports (noted).
- Figure-read ring values keep `extracted_from_figure` after the dB/m -> dB/cm conversion (merged precedent: 25 rows).
- Width 2.8 um from the Fig. 1(a) label w_core = 2.8 um for all three thicknesses, consistent with the p.8 mask width;
  `derived` (um -> nm). Cladding 8 / 7.5 um are figure labels on a to-scale design cross-section:
  `extracted_from_figure` (gassenq2012 precedent).
- OFDR and FIMMWAVE group-index and OFDR loss rows carry wavelength 1550 nm `wavelength_inferred: true` (design
  wavelength, p.3); Fig. 5 ring rows use the caption's "lambda ~1550 nm" as a stated wavelength (D393).
- process_name "TriPleX LPCVD Si3N4 technology" as printed; fab empty (no org named in the fabrication sentence; the
  LioniX co-authors are affiliation only, Contract v7; hosseini2015 / roeloffzen2018 / bauters2011 precedents).

Missing fab / facility orgs: none needed. Note for the org round: the printed "LioniX BV" (2011 entity, p.1
affiliation) has no registry org (org_lionix_international is the later entity; a2011 precedent); not used here.

## lit:wang2019a (arXiv 1809.08637 v1, Harvard)

Components: 3. Metric rows: 20.
- `cmp_lit_wang2019a_comb_ring_r80` (`resonator.ring`, 10): TE Q_L 6.6e5 (`measured`), Q_i 1.1e6 and Q_C 1.7e6
  (`author_estimate`, assumed under-coupling, D403), TM Q_L 6.0e5 / Q_i 9.2e5, linewidth 2.4 pm (Fig. 1(b) label),
  extinction 13.4 dB (`derived` from T = 4.6 %), R 80 um, top width 1.3 um, LN 600 nm.
- `cmp_lit_wang2019a_kerr_comb` (`laser.comb`, 3): line spacing ~250 GHz / ~2 nm, OPO threshold ~80 mW
  (`author_estimate`, Eq. S1).
- `cmp_lit_wang2019a_eo_filter_ring` (`wdm.mrr`, 7): EO tuning 2.4 pm/V, pump rejection 47 dB (`crosstalk_db`),
  adjacent-line suppression 20 dB (`crosstalk_adjacent_db`), calculated 25 / 52 dB (`simulated`), passband 3 pm
  (`author_estimate`), FSR 2.19 nm (`simulated`).

Preprint note: the arXiv v1 is titled "Monolithic photonic circuits for Kerr frequency comb generation, filtering and
modulation"; registry title "Monolithic lithium niobate photonic circuits for Kerr frequency comb generation and
modulation". Same authors and experiment; accepted as the same work (D430 / D433). Values from the preprint only.

Values not entered and why:
- Filter / modulator EO bandwidth ~400 MHz (photon-lifetime limited, 0.4 ns), 250 / 500 Mbit/s eye diagrams, 1.5 V
  peak-to-peak drive (p.3): modulator metrics, rule 2 (EO-atlas candidate: the paper is not in
  `eo-modulator-atlas/data/devices.csv`).
- Comb spans (TE 1400-2100 nm, ~700 nm; TM ~300 nm; p.2, Fig. 2): no registry parameter (comb span rejected, D81).
- ~50 W circulating power without optical damage after hours of pumping, photorefractive quenching above 100 mW
  (p.2): circulating power is not an input-power handling value.
- 13 V step to the adjacent comb line and 27 pm comb-filter FSR difference (p.3), FSR mismatch ~1 % (p.2) vs 1.2 %
  (p.7): no registry parameter; noted.
- Simulated GVD curves (Fig. 2(a-b)), neff 1.91 / mode area 0.875 um2 / V = 440 um3 (Supp. IV): model inputs.
- Material constants (r33, chi(3), n2) and literature values in the introduction (Q up to 1e7 ref. [25], bulk
  WGM 1e8 ref. [23]): rule 3 / material data.
- Filter tuning efficiency "lower than our previous results [S24]" (p.6): the earlier value is not printed.

Judgment calls:
- The comb ring is one physical device in two classes (`resonator.ring` + `laser.comb`, D396 cross-notes); the filter
  is `wdm.mrr` (channel filter in the comb-line selection path, D400).
- Pump rejection (47 dB, a specific non-adjacent line ~30 comb lines away) as `crosstalk_db` with the wording in the
  condition; the printed "20 dB extinction for the comb lines adjacent to the target line" as
  `crosstalk_adjacent_db` (it is the drop-port suppression of the neighbouring channels).
- Q measurement wavelength not stated: `band c_band`, `wavelength_inferred: true` (pump ~1556 nm, telecom laser).
  Filter passband 3 pm: wavelength 1616 nm inferred (target line of the experiment).
- TM Q_i 9.2e5 `author_estimate`: no extraction described for TM; TE extraction assumes under-coupling (D403).
- Platform left empty on all three rows: EBL + Ar+ RIE of the 600 nm LN film, etch depth / slab never stated
  (D422 / D423; coordinator may set `family_override`).
- Fab `org_harvard_university` + facility `org_center_for_nanoscale_systems`: acknowledgment "Device fabrication is
  performed at the Harvard University Center for Nanoscale Systems" (p.4) plus "similar process as described in our
  previous work" (p.6) (D84a / D448; wang2018 precedent D462). NANOLN is the wafer supplier (note only).

Missing fab / facility orgs: none (both ids exist in the registry).

## Registry gaps

- Kerr comb span (wang2019a TE 1400-2100 nm, p.2): no parameter; D81 rejected comb span, not re-proposed.
- Circulating-power handling of a resonator (wang2019a ~50 W, p.2): `power_handling_dbm` is defined on input power;
  a `circulating_power_w` parameter would be needed. Single value, not proposed.
