# Batch lit_234 report

Distilled 2026-11-20. Papers: lit:doerr2014a, lit:wang2008, lit:akiyama2005, lit:soltanian2023. Page-1 titles match
the source rows; no correction / erratum files; `garbled_text_layer` false for all four (the akiyama2005 text layer drops
`>` / `<` / `~` signs: bounds read from the page renders). Validation: `merge_component_staging.py --dry-run` ->
+9 components, +40 metrics, 0 errors (one WARN belongs to merged ni2025b, not this batch). No fab or facility org set on
any row; no `process_name`.

## lit:doerr2014a (Optics Express 2014, Si modulation-based isolator) - 5 components / 12 metrics

- `two_arm_isolator` (nonreciprocal.isolator, fabricated): isolation 3.0 dB broadband over the C band (ASE input,
  Fig. 8), ~5 dB narrowband (CW, Fig. 7), fiber-to-fiber IL 11.1 dB at 1550 nm, theoretical 4.2 dB for N = 2
  (simulated).
- `gc` (fiber_chip_coupler.grating): 3.5 dB loopback_half, author_estimate, halved from the "7 dB from fiber coupling in
  and out" loss-breakdown term (feng2022 precedent).
- `mmi_1x2` (splitter.mmi): excess loss 1 dB, scope unspecified (breakdown term for "the 1 x 2 MMI couplers", count not
  stated, not divided), n_inputs / n_outputs.
- `pin_phase_modulator` (phase_shifter.other, carrier-injection precedent aflatouni2015 / kang2019): bandwidth 300 MHz
  (bw3db_khz 300000, author_estimate, origin not stated), 1 dB breakdown term for "the two modulators" (scope
  unspecified), length 600 um.
- `four_arm_isolator_design` (row_kind design): 20.7 dB read off the calculated Fig. 5 point at N = 4 (simulated,
  +/- 0.5 dB).
- Not entered: 2 dB waveguide propagation term (no length / per-length value); thermo-optic phase shifter (no value);
  intrinsic-layer width 1.75 um (no role-specific parameter, in notes); modulation depth below 138 deg (no value);
  ~3 dB modulation-off excess (residual AM, no parameter); ref. [8] 11 dB InP and ref. [9] ECOC 2013 3 dB (cited, rule 3).
- Fab: passive "A two-arm version was made in silicon photonics" (p.4), all authors Acacia Communications -> empty (D80b).
- Platform empty on all rows: only "silicon photonics" is printed, no SOI / BOX (D422 / D423).

## lit:wang2008 (OFC 2008, uncooled 1.3 um QD SOA) - 1 component / 10 metrics

- `qd_soa_2p4mm` (amplifier.soa, gaas): on-chip gain up to 25 dB at ~1270 nm (20 C), Psat > 13 dBm at 1294 nm (200 mA,
  20 and 70 C, one row), peak gain > 19 dB at 70 C (band o_band inferred), median 18.5 dB over 1290-1300 nm and 20-70 C,
  NF 6 dB best at 1295 nm / 40 C and 1300 nm / 50 C (two rows from one sentence), NF 6.5 dB at 1300 nm / 70 C, gain
  bandwidth > 80 nm (criterion not stated; laser-limited), length 2400 um (derived), ridge 4 um.
- Not entered (no parameter): +/-3.5 dB gain variation over 20-70 C, 3.4 dB single-wavelength variance, ~1 dB fluctuation
  at 1294 nm, IPDR values (>= 7 / 9 / 13 / > 14 dB; text and conclusion differ: 13 vs 14 dB), ~0.1 dB power penalty,
  6 deg facet angle, 10 QD layers.
- Printed "19dBm" peak gain (p.2) read as 19 dB per abstract / conclusion (noted).
- Fab: passive fabrication sentence, authors at Cambridge University Engineering Department and Innolume -> empty (D154).

## lit:akiyama2005 (IEEE PTL 2005, QD SOA 90 nm / 23 dBm) - 2 components / 12 metrics

- `qd_soa_6p15mm` (amplifier.soa, inp): gain > 25 dB, NF < 5 dB, 3-dB Psat > 19 dBm (2 A) over the 90-nm band
  (wavelength 1410-1500 nm read off the Fig. 2 dark-gray area, `wavelength_inferred` true), gain_bandwidth_nm 90
  (criterion in condition) and 120 (Fig. 2 label + caption criterion, extracted_from_figure), penalty-free output
  23.1 dBm (10 Gb/s, 1550 nm, 2.5 A, statistic best), 25.7 dBm in deep saturation (40 Gb/s, Fig. 4(a)), length 6150 um
  (derived), stripe 2.2 um.
- `qw_soa_1p2mm` (amplifier.soa, platform empty): comparison InGaAsP MQW SOA, Psat 17 dBm (author_estimate), 1200 um,
  1.6 um stripe.
- Not entered: Fig. 2(a) chip-gain curves (about 40 dB peak at 2.5 A; figure only), Fig. 6 points attributed to refs. [18]
  / [9] and other groups' SOAs, ECOC 2003 20 dBm (ref. [9]), "~1 dB" coupling loss cited from ref. [9] (p.1),
  polarization sensitivity "quite large" (no value).
- Fab: "We have successfully realized" only; authors at Fujitsu / Fujitsu Laboratories (OITDA) and the University of
  Tokyo -> empty (D154).

## lit:soltanian2023 (IEEE SiPhotonics 2023, uTP III-V-on-Si SOA) - 1 component / 6 metrics

- `tapered_soa` (amplifier.soa, other): small-signal on-chip gain 9.4 dB at 1573 nm (fit inside data range, measured),
  Psat_out 15.4 dBm and Psat_in 8.9304 dBm (author_estimate, D435: the Eq. (1) fit is extended past the highest measured
  input of about +5 dBm), differential resistance 11 / 9 ohm (left / right segment at 100 mA), mesa width 4 to 7.5 um
  (Fig. 1(a) labels).
- Not entered: material gain saturation power Ps 17.2452 dBm (model parameter, no registry parameter), gain-peak
  wavelength (no amplifier parameter), Fig. 1(a) section lengths and inset thicknesses (no printed total length; inset
  "not to scale"; listed in notes).
- Fab: "we used micro-transfer-printing to integrate pre-fabricated InP SOAs [1]"; authors at Ghent University - imec and
  MIT -> empty (D154; beeck2020 precedent). Platform `other` (transfer-printed III-V on Si; beeck2020 / liu2025).

## Missing fab / facility orgs

None: no paper names a fabricator, foundry or shared facility. (Registry already holds org_acacia_communications,
org_fujitsu, org_innolume, org_university_of_cambridge, org_ghent_university, org_the_university_of_tokyo for the header
batches.)

## Judgment calls for the auditor

1. doerr2014a loss-breakdown terms: GC 7 dB halved to 3.5 dB loopback_half (feng2022), while the MMI (1 dB) and
   modulator (1 dB) terms are kept undivided with scope unspecified because the paper does not say how many parts each
   term covers. Alternative: drop the MMI / modulator rows (breakdown-only components).
2. doerr2014a narrowband ~5 dB: band c_band inferred from the Fig. 7 axis (1555.9-1556.3 nm); the CW laser wavelength of
   that measurement is not printed (the IL sentence before it says 1550 nm).
3. doerr2014a four-arm design row (row_kind design, 20.7 dB read off Fig. 5): kept because Fig. 1(c) proposes the four-arm
   design and Figs. 3-4 simulate it; could be dropped as a theory curve point.
4. akiyama2005 wavelength range 1410-1500 nm is a figure reading (no wavelength printed for the headline values);
   alternative: `band: unspecified` with the reading only in notes.
5. akiyama2005 comparison QW SOA Psat 17 dBm as author_estimate (stated as a device property; the Fig. 4(b) measurement
   may or may not be its origin). Alternative: measured, or drop the row.
6. akiyama2005 D408: kept as a journal extension of OFC 2004 PDP12 (ref. [18]); the Fig. 6 headline point labelled with
   ref. [18] is not used, the Fig. 5 / Sec. V values are. The merged akiyama2007 review row did not enter the same device
   because that review attributes it to the OFC paper.
7. wang2008 nf_db minimum "6 dB at 1295 nm at 40 C and 1300 nm at 50 C" split into two rows (two operating points), not
   one row with both in condition.
8. soltanian2023 mesa width 4-7.5 um: tied to the mesa by label colour matching the inset legend (Mesa blue, MQW green,
   Si grey) and the text's "Si 2 um wider than MQW" check; D156 if the auditor finds the colour tie insufficient.

## Registry gaps (no new parameter proposed unless confirmed by more rows)

- Amplifier gain temperature variation (wang2008 +/-3.5 dB over 1290-1300 nm for 20-70 C, p.2): D250 rejected a gain
  temperature coefficient; this is a gain-flatness-over-temperature span, same rejection likely.
- Amplifier input power dynamic range (wang2008 > 9 dB at < 0.2 dB penalty, p.3): D250 rejected (definition varies).
- Amplifier gain-peak wavelength (soltanian2023 1573 nm, wang2008 ~1270 nm): center_wavelength_nm not allowed on
  amplifier; proposed `center_wavelength_nm` allowance for amplifier = wavelength of maximum small-signal gain.
- Saturation-model parameter Ps (soltanian2023 17.2452 dBm): model parameter, not proposed.
- Isolator drive / modulation frequency (doerr2014a 2.0 GHz drive, 2.4 GHz ideal; condition only), modulator
  intrinsic-region width (doerr2014a 1.75 um): not proposed.
