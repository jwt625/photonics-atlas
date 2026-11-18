# lit_192 batch report

Distilled 2026-11-18 under SKILL.md Contracts v4-v7 and the DevLog-007 rulings (D150-D646). Validation:
`merge_component_staging.py data/_staging/components/lit_192 --dry-run` -> +24 components, +102 metrics, 0 errors
(the only warning is the pre-existing `cmp_lit_ni2025b_pimmwc-m18` duplicate, not in this batch).

| paper | components | metric rows |
|---|---|---|
| lit:chang2020 | 5 | 30 |
| lit:yokota2022 | 0 | 0 |
| lit:hu2017 | 5 | 25 |
| lit:zhang2014a | 7 | 20 |
| lit:acoleyen2011a | 7 | 27 |
| total | 24 | 102 |

All five texts match their source rows (page-1 titles). chang2020 is printed in Optics Express 29(2), 2021 (the id year
comes from the online date). No garbled text layer; the IEEE stamp lines were ignored.

## lit:chang2020 (metalens on Si photonics 2D beam steerer)

Rows: beam steerer system (`free_space_emitter.other`), metalens (`free_space_emitter.metasurface`, he2026 precedent),
ring emitter (`free_space_emitter.other`) and the same rings as `resonator.ring` (D396), switch network
(`switch_fabric.other`, D158).

- Fab `org_columbia_university`: the Appendix uses first person for the switch network and the metalens ("We fabricate",
  "We deposit", p.7). All authors are at Columbia (one also lists NCTU), so this follows the miller2019 precedent from
  the same group. Facility `org_advanced_science_research_center_nanofabrication_facility` ("performed in part at the
  CUNY Advanced Science Research Center NanoFabrication Facility", p.9).
- No wavelength is printed. Every performance row is `c_band` + `wavelength_inferred`, based on the ring spectra in
  Fig. 2(b) / 5(a) (about 1557-1562 nm).
- Not entered:
  - Power: 83 / 56 mW max / mean steering power is on the switch-network row (`power_consumption_w`) because the
    parameter is not allowed for free_space_emitter. The 252 mW for a 1024 x 128 array is a projection and was left
    out.
  - Losses: the 4.1 dB loss estimate rests on cited MMI losses [44,45] plus an assumed 2 dB/cm (rule 3). The ~100 mW
    power-handling sentence cites [46,47].
  - Metalens: the 90 um focal length has no parameter, and the 82 % efficiency is cited from ref. [30].
  - The typical 0.25 nm/mW heater tuning cites [43].
  - The drive voltage of < 4.8 V is not a Vpi.
  - The Fig. 2(b) doublet has no printed Q.

## lit:yokota2022 (directly modulated optical negative feedback laser) - 0 rows

Stopped on scope (judgment call). The device under test is a bench or module assembly: an InGaAsP MQW DFB laser, a lens
and a discrete bulk Fabry-Perot etalon (FSR 25 GHz, finesse 156) in free space, then an isolator and a collimator into
fiber (Fig. 3(a), p.5-6). Both the narrow-linewidth result and the frequency-sweep behaviour come from the
bulk-etalon feedback. I treated this as D411 (discrete bulk resonator, out of scope), in line with the D641 / D642
exclusions of bulk parts and bench assemblies. The paper prints no value for the solitary DFB chip on its own: Fig. 3(c)
is a curve with no number, and the threshold is ambiguous ("10 times the threshold current (~70 mA)"; Table 1 uses
193 mA for the simulated laser from ref. [51]).

Values available if the coordinator rules the ONF laser in scope (`laser.other`, platform empty per D422, fab empty):

- 1538 nm operating point at 24 C and ~70 mA, with 10-kHz triangular current modulation.
- Intrinsic linewidth ~2.0 kHz (p.7). This would be `author_estimate`: the white FM-noise level of 1.3e3 Hz2/Hz is a
  drawn estimate that "indicated reasonable agreement" with the ranging simulation, then halved for the
  self-delayed homodyne.
- Frequency excursion 162.6 MHz peak-to-peak, with deviation from the ideal triangle < 0.66 MHz (0.4 %) outside the
  first 0-10 us (p.5, Fig. 3(b)). Registry gaps: sweep excursion and sweep nonlinearity (candidate
  `chirp_nonlinearity_pct`, D431).
- Etalon peak transmittance 65 %. This belongs to the bulk etalon and would stay out either way.

The ranging SNR of 30-56 dB and the -1.7 dB relative peak power at 300 m are system results, with no parameter.

## lit:hu2017 (SOA + Si double-ring ECL)

Rows: laser (`laser.tunable`), double-ring Vernier filter (`resonator.ring`, D400; one row for the pair as in
kobayashi2014), 1x2 MMI 5:95 (`splitter.mmi`), SOA-chip double-lens coupling (`chip_chip_coupler.other`), SOA gain
chip (`amplifier.soa`).

- Fab is empty: there is no fabrication or assembly statement (D80b).
- Platform is empty on all rows: SOI, the layer stack and the SOA material are never stated (D422 / D423).
- Output-power plane is `unspecified`: Fig. 1 shows a collimator into a fiber, but the text does not name the plane.
- Linewidth: "< 130 kHz" is the printed 20-dB width of the self-heterodyne spectrum, which the paper calls the
  linewidth. It is entered as printed (`lt`, kHz -> Hz derived) with that definition in the condition. It is not
  converted.
- Tuning range: the measured Vernier span is 57 nm (Fig. 4(b) labels 1526.372 / 1583.74 nm). It is on the laser
  (tuning_range_nm) and on the filter (fsr_nm, measured) with a cross-note. The calculated 53 nm FSR3 is
  `author_estimate` because its inputs FSR1 / FSR2 are of unstated origin.
- The printed FSRs (Ring-1 2.296 nm at R 46 um, Ring-2 2.400 nm at R 47 um) pair the larger FSR with the larger
  radius, and the text says "we pick out larger FSR1". They are entered as printed and flagged in the notes. Racetrack
  straight lengths are not stated.
- Q 19324 is `derived`: lambda / FWHM from the labelled half-power points. The text prints the 3-dB width as 0.084 nm,
  while the labels span 0.080 nm (noted).
- TEC power is entered as three `author_estimate` rows (1.21 / 1.15 / 1.27 W at "kept at" 30 / -5 / 70 C). Whether that
  is the board or the ambient temperature is not stated.
- Not entered:
  - Ring coupling: "kappa ... 1.54*10^7 (m^-1)" (quantity unclear). Desired Q >= 8611 is a design criterion.
  - Filter contrast: the 3.4 dB main-to-sub-peak contrast has no resonator parameter (gap below).
  - Beam divergence: SSC far field 14.1 x 19.9 deg (Fig. 3(a), apparently simulated) and SOA divergence 16 / 30 deg
    have no allowed parameter (gap below).
  - Isolator: 45 dB isolation is for a bulk part in the module.
  - The introduction's comparison values belong to refs. [1], [3] and [4] (rule 3).

## lit:zhang2014a (multicore polymer waveguides, multistep 45 deg mirrors)

Rows: multicore waveguide (`waveguide_platform.straight`), lensed-fiber facet (`fiber_chip_coupler.edge`), and five
mirror rows (`micro_optics.vertical_taper`, one per mirror depth, rule 9; zhang2024a precedent).

- Fab is empty: the fabrication is described only in passive voice, with all authors at Fraunhofer HHI (D80b).
  ChemOptics ZPU-12 is a material supplier and appears in notes only.
- Propagation loss: one row per layer with the printed fit slopes from the Fig. 4 labels (0.6125-0.9995 dB/cm,
  `measured`, cutback; figure-label precedent D574). The text's 0.61 and 0.88-1 dB/cm values agree.
- Facet loss: half of the printed two-facet cut-back intercepts per layer (`loopback_half`, `derived`; du2024 / D608
  precedent). These are tiny and scattered (0.02-0.24 dB per facet), and the notes say so.
- Mirror loss: Layer 1 = 1.5 dB and Layer 5 = 1.9 dB come from the text range at 1550 nm, with the order taken from
  Fig. 7 and the text ("deeper mirrors gradually more loss-prone"). Layers 2-4 (1.66 / 1.73 / 1.81 dB) were read off
  Fig. 7 at 1550 nm, +/-0.03 dB.
- Not entered:
  - Crosstalk: Table I (worst neighbour -40.7 dB at 3.8 cm) is in the waveguide notes, because crosstalk_db is not
    allowed for waveguide_platform (gap below).
  - Material: 0.5 dB/cm bulk material loss from a slab film.
  - Geometry with no parameter: 20 um lattice pitch, 17.32 um layer distance.
  - Fig. 2 simulated MFD scan over other widths. The SMF-28e MFD of 10.4 um is only a comparison.

## lit:acoleyen2011a (2D dispersive off-chip beam scanner, SOI)

Rows: shared out-coupling grating (`free_space_emitter.other`, acoleyen2009 precedent), five scanners
(`free_space_emitter.other`, one per AWG order q = -50 ... -250, rule 9), and the 1x16 star coupler (`splitter.other`).

- Fab `org_imec` with process_name "(ePIXfab silicon photonics platform cited, ref. 7)", copied from the acoleyen2011
  ruling (D616).
- Ref. [4] is the authors' own Group IV Photonics 2010 paper. No value sentence cites it, so the values are kept (D408).
- Per-scanner values: Table I measured dphi/dlambda, with the sign as printed (negative). The theory values and the
  Table I AWG FSR are in notes: fsr_nm is not allowed for free_space_emitter, and the table does not say whether the
  FSR is computed.
- Theta-direction values (0.148 deg/nm, theta0 2.9 deg at 1550 nm, ~15 deg range) are on the shared grating row. They
  were measured on the order-150 device, but the theta steering is a property of the grating, which is identical in
  all five scanners.
- The beam FWHM of 3.5-4.0 deg and the ~50 deg phi range are on the order-150 row (the device of Figs. 2-4).
- Not entered:
  - Efficiency: the 10-13 % input-waveguide-to-free-space efficiency names no scanner (D254); it is in the notes of all
    five rows.
  - Waveguide loss: "approximately 1 dB" with no length.
  - Simulated dispersion factors and n_eff.
  - Grating-array pitch: "16 waveguides spaced at a distance of 2 um" is ambiguous between the star-coupler output
    and the grating array.

## Missing fab / facility orgs

None. Every org this batch names is in the registry: `org_columbia_university`,
`org_advanced_science_research_center_nanofabrication_facility`, `org_imec`. ePIXfab (still missing, D596) appears in
acoleyen2011a only as a cited platform (ref. 7, p.3), not as a fabrication service.

## Judgment calls

- (a) chang2020 metalens is classed `free_space_emitter.metasurface`, following the he2026 precedent of a metasurface
  steering by emitter selection; `micro_optics.metalens` is the alternative. Its focusing efficiency is stored as
  coupling_efficiency_pct per_component (vocht2024 precedent).
- (b) yokota2022 has 0 rows: a bulk FP etalon in free-space feedback, D411 analogue. The values are listed above for a
  coordinator ruling.
- (c) hu2017 "linewidth < 130 kHz" is the 20-dB self-heterodyne width. It is kept as printed with that definition and
  not converted.
- (d) zhang2014a facet losses are halved cut-back intercepts (`loopback_half`, derived). The values are very small
  and fit-limited.
- (e) zhang2014a mirror losses are `author_estimate`: they are extracted with a nominal PD responsivity of "around
  1.1 A/W", and the paper attributes the wavelength dependence to that responsivity. `measured` with
  `reference_structure` is the alternative (pita2021 D639).
- (f) acoleyen2011a theta-direction values (grating) are placed on a shared grating row, and the family efficiency is
  kept in notes (D254).
- (g) chang2020 power consumption is placed on the switch-network row, since the paper says the MZ switches plus the
  ring heaters consume it.

## Registry gaps (skipped value, locator, proposed definition)

- `crosstalk_db` on waveguide_platform: zhang2014a Table I (p.3), worst -40.7 dB between neighbouring cores of a
  multicore waveguide at 3.8 cm. Proposed definition: inter-waveguide crosstalk suppression of coupled / multicore
  waveguides over the stated length. Also D594.
- `beam_divergence_deg` on chip_chip_coupler and amplifier: hu2017 p.4 Sec. 2.2, SSC 14.1 x 19.9 deg and SOA 16 /
  30 deg. Proposed definition: far-field divergence of a coupler or gain-chip facet, with level and axis in the
  condition.
- `focal_length_um` on free_space_emitter / micro_optics: chang2020 p.4, metalens f = 90 um. Also D441.
- `power_consumption_w` on free_space_emitter: chang2020 p.5, 83 / 56 mW steering power (entered on the switch-network
  row instead). Also miller2019.
- Vernier main-to-sub-peak contrast on resonator: hu2017 p.5 Sec. 2.4, 3.4 dB. Proposed definition: suppression of the
  nearest unmatched peak of a Vernier filter, in dB.
- `fsr_nm` on free_space_emitter (AWG-fed scanners): acoleyen2011a Table I, 22.7-4.7 nm.
- Laser frequency-sweep excursion / sweep nonlinearity: yokota2022 p.5, 162.6 MHz, 0.66 MHz (0.4 %). Only relevant if
  the ONF laser is ruled in scope.
