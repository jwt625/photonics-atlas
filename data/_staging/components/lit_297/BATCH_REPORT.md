# Batch lit_297 report

Papers: lit:woods2020, lit:park2007a. Both cached texts match their source rows (page-1 titles checked); no
garbled text layer. Validation: `merge_component_staging.py data/_staging/components/lit_297 --dry-run` ->
+8 components, +56 metrics, 0 errors (the two warnings name merged rows of other batches).

## lit:woods2020 (Ta2O5 supercontinuum waveguides, Optics Express 2020)

Components 3 / metric rows 19.

- `cmp_lit_woods2020_clad_wg_w3p2` (waveguide_platform.straight, SiO2-clad 3.2 x 0.7 um, about 18 mm): insertion
  loss 19.6 dB TM / 20.0 dB TE (device_total, mean over the 900-1500 nm pump sweep, `derived`: the paper converts
  the mean collected powers against the 110 mW incident power); GNLSE-matched propagation loss 3-4 dB/cm
  (`author_estimate`); geometry (width, core, 2 um cladding, 2.5 um thermal oxide, length).
- `cmp_lit_woods2020_unclad_wg_w2p2` (unclad 2.2 x 0.7 um): insertion loss 25.6 dB TM / 23.4 dB TE (`derived`);
  NLSE-matched propagation loss 5-6.5 dB/cm (`author_estimate`, wavelength inferred from the pump sweep); geometry.
- `cmp_lit_woods2020_clad_wg_w2p0_fp` (2 x 0.7 um clad waveguide, `test_structure`): Fabry-Perot propagation loss
  ~1.4 dB/cm near 1550 nm (`measured`, the paper calls it a lower limit for higher-order modes); geometry.

Not entered: supercontinuum / broadening widths (no parameter); simulated dispersion and ZDWs of Fig. 6 (dispersion
not in the registry, D81 / D250); the ~12 dB coupling loss, 7.5 mW launched power and 2 dB/cm loss of Fig. 7 (model
assumptions); per-subfigure fit values of Figs. 8-9 (summarized by the 3-4 dB/cm range row); 2.6 x 0.7 um clad
waveguide of Fig. 3 (octave-spanning spectrum at 175 mW, no performance parameter, geometry only); collected powers
in mW (converted by the paper to the IL rows).

Fab / facility: fab `org_university_of_southampton` (first-person fabrication, p.2 Sec. 2 and p.3 Fig. 1 caption;
all authors in two units of the university, D154). No facility acknowledged. No missing orgs.

Judgment calls:
1. IL rows `derived` (paper's own arithmetic on its measured powers, D80a), scope `device_total` (free-space input
   referred to the facet power, output collected by a lens); the output light is spectrally broadened and of
   undetermined mode content (noted).
2. Model-matched loss ranges entered as `author_estimate` (they rest on the cited n2 of ref. [16] and a free coupled
   power). An auditor may prefer to leave them out as fit parameters; flagged here.
3. Platform `other` (Ta2O5 core; fan2021 precedent). The 1.4 dB/cm waveguide is described only as "comparable" to the
   experiment guides: own row, fab kept from the same first-person process statement.

Registry gaps: none new (supercontinuum bandwidth and dispersion already deferred).

## lit:park2007a (hybrid AlGaInAs-Si evanescent preamplifier and photodetector, Optics Express 2007)

Components 5 / metric rows 37.

- `cmp_lit_park2007a_input_facet` (fiber_chip_coupler.edge, 10 deg angled AR-coated Si facet to lensed fiber): 5 dB
  per facet from a passive reference waveguide (`author_estimate`: reference IL and split not printed; D437 / D583,
  park2007 precedent).
- `cmp_lit_park2007a_hybrid_soa` (amplifier.soa, 1240 um, 14 um mesa): chip gain 9.5 dB at 1550 and 1575 nm, 300 mA
  (`author_estimate`, rests on the 5 dB term); 3-dB gain bandwidth ~60 nm (`measured`); geometry.
- `cmp_lit_park2007a_iii_v_taper` (waveguide_platform.transition): ~0.6 dB over 1530-1580 nm for this device and
  typical 0.6-1.2 dB (both `author_estimate`); simulated < 0.1 dB at 70 um (Fig. 6(b) inset); taper length, widths,
  Si stack.
- `cmp_lit_park2007a_hybrid_pd` (photodetector.iii_v_on_platform, 2 x 100 um): internal QE 50-55 % at 1550 / 1575 nm
  and 55 % best (on_chip, `author_estimate`); dark current 50 nA at -1 V and 400 nA at -4 V; series resistance
  80 ohm; capacitance 300 fF at 0 V and 170 fF at -4 V; 3 GHz bandwidth from the impulse response; absorber and Si
  geometry.
- `cmp_lit_park2007a_preamp_receiver` (photodetector.other, receiver = SOA + PD; santini2017 precedent): responsivity
  5.7 A/W (on_chip, `author_estimate`); saturation photocurrent 25 mA at 0.5 dB compression (`measured`); ASE dark
  current 25 uA at 300 mA.

Not entered: 13 dB chip gain of ref. [8] and 0.5 dB power penalty of ref. [13] (cited, rule 3); RC-limited
bandwidth 7.5 GHz (a calculated limit from C and R with 50 ohm, not the device response; capacitance bias not
stated); 18 ps rise time; tapered-junction reflectivity < 6e-4 and non-tapered ~5e-3; receiver sensitivity -17.5 dBm
and -8.5 dB power penalty; eye Q factors; reverse-biased amplifier responsivity 1.06-1.15 A/W (used in the taper-loss
condition, not a component of its own); calculated confinement 63 % / 4 % (in core_material); Ta2O5 AR coating
"~5 % reflectivity" (meaning not stated); TM gain / responsivity (qualitative only); tip width "0 um" (paper reports a
blunt tip).

Fab / facility: fab empty on all rows (passive fabrication sentences, authors at UCSB and Intel, acknowledgment thanks
a named person for dicing with no org; D80b). No facility. No missing orgs.

Judgment calls:
1. QE, chip gain and receiver responsivity all rest on the 5 dB coupling estimate: `author_estimate` with ref_plane
   `on_chip` (D583). Spectral width and compression point kept `measured` (independent of the absolute input scale).
2. Dark-current endpoints paired with the bias endpoints (50 nA at -1 V, 400 nA at -4 V) as the monotonic Fig. 4(a)
   curve shows; 170 fF placed at -4 V from the end of the Fig. 4(b) axis.
3. QE range printed as 50-55 % at -2 to -4 V while Fig. 3(a) reads about 50-52.5 % there (55.5 % at -1 V); printed
   range entered with the readings in notes.
4. Receiver kept as its own photodetector.other row rather than putting 5.7 A/W on the bare detector row.
5. Taper method `loss_breakdown` (loss attributed from the photocurrent deficit under a full-absorption assumption).

Registry gaps (skipped value + locator + proposed definition):
- Reflectivity of an on-chip transition / amplifier junction: < 6e-4 (tapered) and ~5e-3 (non-tapered 7 deg tilted
  junction), p.5 Sec. 3. Proposed: `back_reflection_db` widened to waveguide_platform and amplifier (power reflection
  as positive dB below the input; 6e-4 -> 32.2 dB, derived), or a linear `reflectivity_pct` allowance.
- Photodetector impulse-response rise time: 18 ps (10-90 %), p.7 Sec. 3. Proposed: `rise_time_ps` for photodetector
  (10-90 % unless noted).
- Receiver sensitivity: -17.5 dBm at BER 1e-9, 2.5 Gb/s NRZ PRBS 2^31-1, p.8 Sec. 3 / Fig. 9(b). Proposed:
  `receiver_sensitivity_dbm` for photodetector (BER, rate, format in condition).
