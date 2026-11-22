# lit_251 batch report

Papers: lit:gehl2017 (Opt. Express 2017, Si AWGs with active phase correction, Sandia), lit:dong2016 (IEEE JSTQE
2016, invited review of Si WDM PICs), lit:stabile2013 (JLT 2014, InP 8 x 8 space and wavelength selective
cross-connect), lit:han2020 (IEEE PTL 2020, superlattice SiN AWG). Page-1 titles match the source rows. verified_on
2026-11-22. Dry run: +14 components, +103 metrics, 0 errors.

## Components / metric rows

| paper | component | class | metrics |
|---|---|---|---|
| gehl2017 | cmp_lit_gehl2017_awg_50ghz | wdm.awg | 4 (SLSR 19 dB, 50 GHz nominal, 11 channels, footprint) |
| gehl2017 | cmp_lit_gehl2017_awg_10ghz | wdm.awg | 8 (SLSR > 20 dB, adjacent XT > 25 dB, IL 7-8 dB fiber to fiber, AWG < 3 dB estimate, 10 GHz nominal, 11 ch, 35 arms, footprint) |
| gehl2017 | cmp_lit_gehl2017_awg_1ghz | wdm.awg | 12 (SLSR 15-20 dB, adjacent XT 15-25 dB, spacing 0.961 GHz measured / 1 GHz nominal, IL 17-22 dB fiber to fiber, 12-18 dB AWG estimate, 11 x 11 ports, 35 arms, 6 um bends, 1.1 cm2) |
| gehl2017 | cmp_lit_gehl2017_doped_si_heater | phase_shifter.thermo_optic | 2 (phase shift < 2 pi at about 85 mW, doped-region offset 1.8 um) |
| gehl2017 | cmp_lit_gehl2017_wg_1um | waveguide_platform.straight | 4 (< 1 dB/cm at 1550 nm, cutback; width, 250 nm Si, 3 um BOX) |
| gehl2017 | cmp_lit_gehl2017_wg_400nm | waveguide_platform.straight | 4 (about 3 dB/cm; width, 6 um bend radius, 250 nm Si) |
| gehl2017 | cmp_lit_gehl2017_inverse_taper | fiber_chip_coupler.edge | 2 (4 dB per facet estimate; 4-5 dB coupling share, scope unspecified) |
| dong2016 | cmp_lit_dong2016_si_sin_transition | waveguide_platform.transition (test structure) | 5 (0.15 dB per transition derived; 100 um taper, 220 nm Si, 400 nm SiN, about 100 nm spacer) |
| stabile2013 | cmp_lit_stabile2013_xconnect_8x8 | switch_fabric.other | 9 (on-chip loss 7.6-14.7 dB estimate, fiber-to-fiber 21.1-28.2 dB derived, leakage >= 35.1 dB, rise 3.8 ns / fall 2.8 ns, 8 x 8 x 8 wavelengths, footprint) |
| stabile2013 | cmp_lit_stabile2013_cyclic_router_8x8 | wdm.awg | 8 (3-dB passband 173 GHz measured / 180 GHz design, spacing 400 GHz measured / 3.2 nm design, 8 x 8, 8 channels, 1.5 um arms) |
| stabile2013 | cmp_lit_stabile2013_lensed_fiber_facet | fiber_chip_coupler.edge | 2 (13.5 dB total coupling, assumed term; 250 um input pitch) |
| han2020 | cmp_lit_han2020_sl_awg_1x8 | wdm.awg | 22 (IL 3.4 dB best, XT 18 dB mean, FSR 6.4 nm label, 100 GHz / 1550 nm design, ports, 40 arms, 800 / 900 nm arms, 1.5 um gap, two arm increments, tapers, bend, footprint, stack, sidewall 85 deg) |
| han2020 | cmp_lit_han2020_conv_awg_1x8 | wdm.awg | 19 (IL 3.6 dB best, XT 14 dB mean, FSR 6.4 nm label, same design / stack rows, 800 nm arms) |
| han2020 | cmp_lit_han2020_sin_wg | waveguide_platform.straight | 2 (about 1.5 dB/cm, 440 nm core) |

Per paper: gehl2017 7 / 36, dong2016 1 / 5, stabile2013 3 / 19, han2020 3 / 43.

Fab / facility / process:
- gehl2017: fab `org_sandia_national_laboratories` on all rows (p.4 Sec. 2: the device was fabricated using the
  silicon photonics platform at the Sandia MESA silicon micro-fabrication facilities; passive sentence naming the
  org, Contract v7). process_name "Sandia MESA silicon photonics platform" (printed words: "the silicon photonics
  platform at the Sandia ... (MESA) ... facilities"). Facility empty: MESA not in the registry.
- dong2016: fab `org_astar_ime` borderline (p.8 Acknowledgment thanks two named Institute of Microelectronics,
  Singapore staff for PIC fabrication; D84b), not tied to a specific chip in a review.
- stabile2013: fab empty (passive "is fabricated on a re-grown active-passive epitaxial 2-inch wafer", process
  modules cited; acknowledgment thanks for discussion during fabrication and for wafer growth, no org named; D80b).
- han2020: fab empty pending the org round (p.4 Acknowledgment thanks AEPONYX Inc. for fabricating the devices;
  AEPONYX missing from `organizations.csv` / `org_aliases.csv`).

## Values not entered and why

gehl2017
- Spectral shift with optical power about -70.4 MHz/mW up to 34 mW on chip, power handling above 30 mW, and
  temperature shift about 11.2 GHz/C (p.11 Sec. 7, p.14 Sec. 8, p.15 Fig. 11): the paper says "the AWG" / "this
  device" after demonstrating both the 10 GHz and the 1 GHz AWG; Fig. 11(b) peak frequencies (194.87-195.03 THz)
  match neither the Fig. 7 (about 1540 nm) nor the Fig. 8 (194.16-194.17 THz) channels. D159: notes on the AWG rows.
- Star coupler design: about 80 % of the centre-input light collected, about -1 dB in the ideal structure (p.3):
  design value of an AWG sub-part; in the 1 GHz AWG notes.
- Bend plus mode-filter loss below 0.03 dB per 180-degree bend, below 1 dB for 32 bends (p.4): simulation-based
  estimate per 180 degrees; `bend_loss_db_per_90` is per 90 degrees.
- 8.8 dB transmission increase (p.7), > 15 dB crosstalk improvement vs the intensity method (p.11): differences.
- Residual phase error std < 0.1 rad (p.12 Fig. 8(b)), thermal crosstalk matrices (Fig. 6): no parameter.
- Fig. 6 diagonal phase slopes and Fig. 3(b) peak levels: figure-only, 3D bar plot / reference not stated.
- RF channelizer background < -40 dB and about -20 dB crosstalk (p.13-p.15): system demonstration.
- Fiber-to-chip coupling below 1 dB with index-matching fluid (p.11): projection.
- Longest path 17.4 cm (p.5): geometry without parameter (label of the 1 GHz row).

dong2016
- Every device result in Sec. III-IV is credited to cited work: VOA-MUX AWG (ref. [58]: 9.1-9.7 dB IL, 1-dB
  35 GHz, > 22 dB isolation, 1 mm x 2 mm), DWDM transmitter (ref. [11]: 17.5 dB fiber to fiber, +/- 0.6 dB),
  receivers (refs. [24], [25], [27], [28]: responsivities, 5.3 nm shift, PDL, crosstalk), ring filters and ring
  modulators (refs. [10], [12]-[15], [17]: circumference, radii, 60 GHz 3-dB width, < -25 dB crosstalk, FSR
  6.4 nm), 2-D grating > 4 dB / 40 nm (ref. [57]): rule 3 (fontaine2022 / wang2020 review precedent).
- Typical LPCVD SiN loss below 0.5 dB/cm in the C band (p.3): technology-level statement, no device or measurement
  named (fontaine2022 Table 1 precedent).
- Generic sensitivity calculations (index sensitivity 3.7e-3 / 3.0e-4 per nm, 0.8 nm/nm, 0.07 nm/C), typical
  tuning powers and times (p.3, p.5): no device.

stabile2013
- SOA gain 8.2 dB at 40 mA (2 kA/cm2) and passive path loss 33.6-37.8 dB / 33.6 dB (p.3, p.5): computed from
  component losses of earlier circuits (refs. [16], [25], [29]); 4.2 dB path variation from 0.2 dB per crossing
  (ref. [25]). Rule 3. The SOA gate (1 mm x 2 um), MMIs (6.5 x 46.5 um), mode filters (6 x 100 um), 30 um tapers,
  waveguides (1.5 um deep, 2 um shallow, 100 um bends) have no own performance value: geometry in the switch notes,
  no rows (rule 9).
- OSNR > 30 dB/0.1 nm and Table I OSNR: no parameter. Power penalties, BER: system metrics.
- In-fiber ASE PSD distributions (-51.5 to -45.5 dBm/0.1 nm input side, 74 % above -60 dBm/0.1 nm), their 2.2 /
  0.8 dB std, 8.5 dB output-input difference, 6.5 / 8.5 dB mean excess loss of defective paths (p.3-p.4):
  path-level diagnostics with mixed causes (defects, crossings, MMIs).
- Connectivity 84 %, 126 / 136 working SOAs (p.3): no parameter.
- Cyclic router FSR (eight channel spacings, design; 25.6 nm not printed): not computed.

han2020
- Inter-channel imbalance about 3 dB (p.3): stated once after the IL of both AWGs without naming the device; D159 /
  D254, notes of both AWG rows.
- 2.24 dB adjacent-order coupling loss and about -21 dB phase-error / receiver crosstalk (p.3-p.4): estimated
  budget terms, not device totals.
- MZI test structures with the supercell / identical-width couplers (Fig. 5): no printed values; the supercell MZI
  cross port sits near -40 dB in the plot (figure only, at the noise floor). Simulated intra- / inter-coupling
  below -40 dB (Fig. 2): simulation of the same supercell, no component row.
- Previous AWG of the authors (ref. [15], 4.7 mm x 1.4 mm, 10 um gaps): cited.

## Missing fab / facility orgs

- AEPONYX Inc. (fab, lit:han2020 p.4 Acknowledgment "for fabricating the devices"). Also named in merged
  lit:barazani2023 notes ("AEPONYX custom process").
- Sandia Microsystems and Engineering Sciences Applications (MESA) silicon micro-fabrication facilities (facility
  candidate under `org_sandia_national_laboratories`, lit:gehl2017 p.4 Sec. 2). Fab already set to Sandia.

## Judgment calls for the auditor

(a) gehl2017 Fig. 11 power / temperature shifts not entered on any AWG row (D159): device not identified, and the
    Fig. 11(b) frequencies match neither measured AWG. Alternative: enter on the 1 GHz row (Sec. 7 context).
(b) gehl2017 inverse taper: two `author_estimate` rows, 4 dB `per_facet` (p.14, input taper) and 4-5 dB
    `unspecified` (p.11 / p.12, "fiber to chip coupling" of the whole path; one vs two facets not stated). The two
    statements are inconsistent if the 4-5 dB covers both facets.
(c) gehl2017 process_name "Sandia MESA silicon photonics platform" composed from the printed sentence (Contract v7
    prefers printed wording; derose2011 precedent "Sandia CMOS compatible silicon photonics process"). Alternative:
    leave empty as a generic "silicon photonics platform".
(d) gehl2017 1 um waveguide loss measured on "a similar sample": kept on this platform's row with fab Sandia and
    `measured`, method cutback.
(e) gehl2017 heater: `phase_shift_pi` < 2 `measured` (phase from the interferometer calibration); the 85 mW drive
    in the condition is an author estimate. `heater_offset_um` 1.8 = printed distance of the doped regions from the
    waveguide centre (edge vs centre of the doped region not stated).
(f) gehl2017 IL de-embedded rows (< 3 dB, 12-18 dB) `author_estimate` with method `loss_breakdown` (coupling term of
    unstated origin); the fiber-to-fiber ranges `measured`, `statistic: range`.
(g) dong2016: the Fig. 3(c) Si/SiN transition result is entered although the paper is a review, because it carries
    no citation; possibly from the author's earlier Bell Labs work (not stated). `derived` (2 dB / 14). Fab
    `org_astar_ime` borderline from the staff-thanks acknowledgment (D84b).
(h) stabile2013 fall time: Sec. V prints 2.8 ns, the abstract 3.2 ns; Sec. V value entered (D417), conflict noted.
    Rise / fall times placed on the switch_fabric row (the SOA has no rise-time parameter; Fig. 11(b) caption calls
    them SOA times).
(i) stabile2013 fiber-to-fiber IL 21.1-28.2 dB `derived` as Table I on-chip loss + the 13.5 dB the paper subtracted
    (restores the measured quantity). On-chip loss `de_embedded` `author_estimate` (assumed coupling). Both include
    SOA gain (net path loss).
(j) stabile2013 coupling 13.5 dB entered as its own `fiber_chip_coupler.edge` row (`author_estimate`, scope
    `unspecified`, total for both facets per the Table I footnote; loss-budget term of unstated origin, rule 4).
(k) stabile2013 cyclic router `bw_3db_ghz` 173 = mode of the distribution (no `statistic` value for a mode; left
    empty, condition says so); channel spacing 400 GHz `measured` = distribution centre.
(l) han2020 IL rows scope `unspecified` (Fig. 6 normalization not stated), `statistic: best` for "minimum insertion
    loss"; crosstalk `crosstalk_db` (type not stated), `mean` from the conclusion's "average across 8 channels".
(m) han2020 FSR 6.4 nm `measured` from the printed figure label on each measured spectrum (akiyama2005 precedent).
(n) han2020 sidewall angle 85 deg `measured` approx (printed, SEM cross-sections in Fig. 4; method not stated).
(o) han2020 design geometry and stack repeated on both AWG rows (two physical designs on one chip).

## Registry gaps

- No new parameter proposed (stabile2013 input pitch 250 um entered on the facet row, `pitch_um` allowed there); all skipped performance values are system metrics, budget terms or cited values.
