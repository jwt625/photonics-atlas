# lit_226 batch report

Papers: lit:komljenovic2015, lit:cao2014, lit:cheung2010, lit:menezo1999. Page-1 titles match the source rows; no
correction / erratum; no garbled text layer (values checked on the page renders where the text layer dropped symbols:
cheung2010 temperatures and approximation signs, menezo1999 kappa / tuning units). verified_on 2026-11-20. Dry run of
`merge_component_staging.py`: +15 components, +92 metrics, 0 errors; the one warning names the merged row
cmp_lit_ni2025b_pimmwc, not in this batch. No component rows existed for these papers.

| paper | components | metric rows |
|---|---|---|
| komljenovic2015 | 7 | 25 |
| cao2014 | 2 | 22 |
| cheung2010 | 3 | 18 |
| menezo1999 | 3 | 27 |

## komljenovic2015 (heterogeneous III-V/Si widely tunable laser with a ~4 cm integrated external cavity, JSTQE 2015)

Rows:
- `laser.tunable` external-cavity laser (platform `other`, heterogeneous III-V/Si): tuning > 54 nm (1237.7-1292.4 nm),
  SMSR > 45 dB, > 10 mW (reference plane not stated), threshold ~30 mA; linewidth < 100 kHz over the tuning range,
  best 50 kHz, ~300 kHz with the external cavity off (SOA2 -3 V, 45 mA) (all kHz -> Hz derived, 20 C stage);
  relaxation oscillation ~2 GHz at 70 mA (author_estimate: the paper says the unperturbed laser could not be measured);
  Vernier repeat spacing 70 nm (design, author_estimate); compound-cavity mode spacings ~0.97 GHz (mode splitting) and
  ~2 GHz (stable modes when the external cavity lases); RIN < -150 dBc/Hz outside the Fig. 7 window (noise floor) and
  Fig. 7(b) peak ~-146 dBc/Hz (extracted_from_figure); main cavity 2 mm, external cavity ~4 cm (derived).
- `laser.tunable` comparison laser without external cavity (test_structure): 345 / 355 / 370 kHz at 96 / 74 / 65 mA,
  one row per device.
- `resonator.ring` Vernier ring pair (intracavity, D400): Q ~12 000 (unqualified -> q_loaded), ring FSR ~300 GHz.
- `reflector.loop_mirror` front 10 % and back 60 % power reflection (author_estimate, origin not stated).
- `waveguide_platform.straight` 3 cm Si spiral: 0.67 dB/cm (author_estimate, origin not stated), length 3 cm.
- `phase_shifter.thermo_optic` external-cavity phase heater: ~20 mW per pi ("estimated", author_estimate).

Not entered:
- Fig. 4(d) linewidth vs main-cavity phase-tuner power (~4 MHz -> 375 kHz, p.3): the measured device is not identified
  (external-cavity laser or the no-external-cavity design), D159.
- Sub-20 kHz linewidths at higher SOA2 current (p.7): laser multimode, no single-mode value.
- External-cavity round-trip loss ~5 dB (p.2), taper reflection ~-40 dB and feedback ~-50 dB (p.6): estimates with no
  registry parameter (roundtrip loss; back-reflection is not allowed on transitions).
- SOA2 transparency current ~12-15 mA and assumed ~20 dB single-pass absorption at -3 V (p.6): no amplifier parameter;
  no SOA row.
- Modulation response (Fig. 6, 70 mA): no 3-dB bandwidth printed; 8 GHz photon-photon resonance peak only.
- Theory: linewidth-reduction factors F 3 -> 9.6 and ~32 (Fig. 4(c), Fig. 5(c)), simulated, no parameter.
- Fig. 11 linewidth-vs-year comparison: other works (rule 3).
- Heater sweep range 0-20 mA / up to 200 mW (p.6): sweep setting, in notes.

Fab / facility: fab empty. "designed at UCSB and fabricated using a heterogeneous photonic integration PDK and foundries
developed under the DARPA EPHI program [27]" (p.2 Sec. II-B): no foundry or fabricating org named (D80b; not the
tran2019 case, where the UCSB process was named with "fabricated in"). `process_name` "heterogeneous photonic
integration PDK (DARPA EPHI program)" as printed. Platform `other` on the two lasers (tran2019 precedent for
heterogeneous Si/InP); Si passive parts platform empty (SOI, BOX or Si thickness never stated; D422 / D423).

## cao2014 (2.2 um InAs/InGaAs triangular vs rectangular QW ridge lasers on InP, PTL 2014)

Rows (`laser.other`, platform `inp`, one row per sample design; babichev2025 precedent for FP lasers):
- Laser A (rectangular QW) and laser B (triangular QW), 0.8 mm, 6 um strip, each: threshold 124 / 68 mA (CW, 300 K);
  3.6 / 10.4 mW per facet at 400 mA (ref_plane chip); differential resistance ~1.87 ohm (D254, stated for both);
  T0 CW 65.2 / 82.1 K (200-280 K), 32.1 / 40.5 K (high-temperature range), pulsed 25.5 / 35.9 K; lasing peak ~2160 nm
  at 310 K / ~2250 nm at 330 K (um -> nm derived); dlambda/dT ~0.8 / ~1 nm/K (as 800 / 1000 pm/K, derived); length
  800 um (derived), ridge width 6 um (design_target), etch depth ~1890 nm (SEM label 1.89 um, derived).

Not entered (no registry parameter): threshold current densities (CW 2.58 / 1.42, pulsed 2.44 / 1.34 kA/cm2, cavity-length
series Fig. 5(a)); maximum operating temperatures (CW 310 / 330 K, pulsed 345 / 360 K); external differential quantum
efficiency vs temperature (A 14.2 % at 270 K -> 5.1 % at 310 K; B 26.3 % -> 11.6 % at 330 K) and T1 92 / 118 K;
internal quantum efficiency ~40 / 45 % and internal loss 16.7 / 14.4 cm-1 (multi-length fit, Fig. 5(b), p.4); turn-on
voltage ~1.25 V (no current stated, forward_voltage_v needs one). The 1.2 / 1.5 / 2.0 mm lasers of Fig. 5 have no
per-length value in a registry parameter: no rows.

Fab / facility: fab empty: "were grown" / "were fabricated" (passive, p.1-2 Sec. II), all authors at SIMIT (one org is
not enough, D80b). Growth machine named only as equipment.

## cheung2010 (1 GHz monolithic hybrid mode-locked InP laser, PTL 2010)

Rows:
- `laser.comb` 1 GHz HML laser (guo2023 / guzman2017 precedents), platform `inp`: repetition rate 1.0558 GHz (Fig. 2
  operating point) and 1.0425 GHz (optimization sweeps); pulse width 70 ps (3 C), ~51 ps (7 C), 36 ps (4 C, best);
  timing jitter <= 4.16 ps (20 kHz-80 MHz, upper limit); CW threshold 230 mA at 3 C and 320 mA at 12 C; peak
  fiber-coupled power 0.59 mW (peak, not average; condition says so); optical mode FWHM ~81 MHz (7 C) and ~70 MHz (4 C)
  as `linewidth_hz`; ~1578 nm (heterodyne 0 GHz reference, at the spectral peak); cavity length 41195.13 um (Fig. 1(a)
  design label, extracted_from_figure); gain / SA ridge width 2.5 um. ps / MHz values derived (D256).
- `waveguide_platform.straight` 2.5 um and 5 um passive waveguides: ~2 and ~0.7 dB/cm (author_estimate, origin not
  stated), widths (derived).

Not entered: RF CNR ~50 dB (10 MHz RBW), RF peak 55 dB above the noise floor, RF peak width ~1 MHz at -20 dB,
time-bandwidth products 5.1 / 3.6 (no parameters; guzman2017 precedent); overall cavity loss < 3 dB (no roundtrip-loss
parameter); optical spectrum widths (Fig. 2(c) "~5nm", Fig. 4(d) / 5(c) "100 GHz" markers: level not stated); tapers
2.5 -> 5 um (170 um) and 5 -> 1.5 um (185 um): geometry only, in notes; SA 150 um / SOA 4000 um / 10 um gap (359 nm
deep): section geometry in core_material (no section-length parameter on laser).

Conflict kept (D417): ~51 ps at 7 C: text prints 376 mA / 6.19 V; Fig. 4(a) label prints 386 mA / -6.18 V and Fig. 3
shows the 386 mA curve reaching ~50 ps (376 mA stays ~58 ps). Condition follows the text, conflict in notes.

Fab / facility: fab `org_university_of_california_davis` (borderline, see judgment call 1). No facility named.

## menezo1999 (10-wavelength 200 GHz DBR laser array + PHASAR emitter on InP, PTL 1999)

Rows:
- `laser.dbr` 10-channel DBR array (one row: same design except grating pitch): 10 channels; threshold 12-18 mA
  (8 lasers, 5 and 6 excluded); SMSR > 40 dB on the array, > 32 dB all channels / all biases, > 35 dB design
  (author_estimate); tuning 5.2 nm typical at 60 mA Bragg current, 9 nm estimate (rests on cited index data,
  author_estimate); cavity-mode spacing 0.3 nm (measured), 40 GHz design (author_estimate); kappa 20 /cm (design);
  emitter channel spacing 200 GHz (accuracy better than 25 GHz in condition); power homogeneity < 5 dB (except
  channels 5 and 6); active-facet power ~10-15.5 mW at 120 mA (Fig. 3(a) read); section lengths 900 / 500 um (design).
- `wdm.awg` flat-top PHASAR 10x1 combiner: 3-dB width 150 GHz (isolated PHASAR), 1.2 nm (Fig. 2(a) label, isolated)
  and 1.2 nm (Fig. 2(b) label, on the PIC), 162.5 GHz design; "rejection" 7 dB measured / 10 dB design as
  `crosstalk_db` (type not stated); design spacing 200 GHz; 10 channels, 47 arms, order 112, 500 um arm bend radius.
- `waveguide_platform.straight` passive straight waveguide: 15 dB/cm (Fabry-Perot resonance method, measured, D394;
  C band inferred).

Not entered: additional loss of the flattening modification "estimated at 2.5 dB" (p.2): a partial term relative to an
unflattened PHASAR, not the device excess loss (judgment call 5); channel-spacing accuracy +/- 25 GHz (no GHz spread
parameter; in condition); Fig. 1 layout labels 1.5 / 4.4 / 3.3 mm (PHASAR extent not separable); Fig. 4 peak coupled
powers (uniformity row covers them); Bragg-side power stated as half of the active-side power (note).

Fab / facility: fab empty: "The photonic integrated circuit (PIC) is realized in three epitaxial growth steps" and other
passive sentences (p.2 Sec. II); authors at OPTO+ (France Telecom/BD/CNET; Alcatel CRC), no statement that they
fabricated it (D80b). No facility named.

## Judgment calls for the auditor

1. cheung2010 fab `org_university_of_california_davis`: "Our integration process, similarly described in [3] and [4]"
   (p.2) treated as an own-process statement (D84a "our process fab"); 7 of 8 authors at UC Davis, the eighth at the
   Agilent Measurement Research Laboratory (measurement role not stated). Alternative: fab empty (D154 / D433 strictness).
2. Propagation losses with no measurement shown (komljenovic2015 0.67 dB/cm; cheung2010 ~2 / ~0.7 dB/cm) entered as
   `author_estimate` with method unspecified (rule 4 / D76 "origin not stated"; guzman2017 precedent). tran2019 (same
   UCSB platform family) kept a no-method 1.2 dB/cm as `measured`; the auditor may prefer that.
3. komljenovic2015 ring pair as one `resonator.ring` row: Q ~12 000 and ring FSR ~300 GHz are stated for "the rings"
   and the radii are not printed, so the two rings cannot be separated (rule 9 vs D254). Alternative: values to notes.
4. komljenovic2015 RIN peak ~-146 dBc/Hz read off Fig. 7(b) (extracted_from_figure, +/- 1 dB); relaxation oscillation
   ~2 GHz `author_estimate` (the paper says the unperturbed laser could not be measured).
5. menezo1999 2.5 dB "additional losses due to this modification" left out of `excess_loss_db` (partial loss term).
6. menezo1999 PHASAR "rejection" 7 dB (measured) / 10 dB (design) as `crosstalk_db` with the printed word in condition;
   Fig. 2(a) shows it as flat top to the highest out-of-band lobe, so `slsr_db` is a possible alternative.
7. menezo1999 SMSR: three rows (> 40 dB on the array, > 32 dB for all channels and biases from abstract / conclusion,
   > 35 dB design). The 32 dB figure is called "rejection" in the abstract and SMSR in the conclusion.
8. menezo1999 isolated PHASAR and on-PIC PHASAR on one row (same design; rule 9), test_structure left empty because the
   rows mix the isolated test PHASAR and the integrated one.
9. cheung2010 comb-mode FWHM (81 / 70 MHz, heterodyne) entered as `linewidth_hz` with the definition in condition;
   peak (not average) fiber power 0.59 mW in `output_power_mw` with "peak" in condition.
10. cao2014 ridge width 6 um `design_target` (stated strip width) although the Fig. 3 caption gives a 10 um mask (wet
    etch); the printed Jth = Ith / (6 um x 0.8 mm) confirms 6 um is the width the authors use.
11. cao2014 high-temperature T0 range: text "beyond 290 K", Fig. 4(a) labels 280-310 K (A) / 280-330 K (B); both in condition.

## Registry gaps (skipped value + locator + proposed definition)

- `threshold_current_density_a_per_cm2` (laser; D431 / D433 candidate): cao2014 2580 / 1420 A/cm2 CW 300 K, 2440 / 1340
  pulsed, cavity-length series (p.3-4, Fig. 4(a), Fig. 5(a)). Definition: threshold current per pumped area at the
  stated temperature and drive mode.
- `max_operating_temperature_k` (laser; D431 candidate): cao2014 CW 310 / 330 K, pulsed 345 / 360 K (p.2-3).
- `internal_loss_per_cm` and `internal_efficiency_pct` (laser; D431 candidates): cao2014 16.7 / 14.4 cm-1 and ~40 / 45 %
  (p.4 Fig. 5(b)).
- `external_differential_efficiency_pct` (laser): cao2014 eta_ext 26.3 % at 270 K -> 11.6 % at 330 K (B), 14.2 % ->
  5.1 % (A) (p.3 Fig. 4(b)); with `characteristic_temperature_t1_k` (92 / 118 K). Definition: external differential
  quantum efficiency (both facets or per facet as stated).
- `roundtrip_loss_db` (laser / waveguide_platform; D420 candidate): komljenovic2015 external-cavity round trip ~5 dB
  (p.2); cheung2010 cavity loss < 3 dB for 41 mm (p.2).
- `rf_linewidth_hz` / RF carrier-to-noise ratio (laser.comb; D431 candidate): cheung2010 ~1 MHz at -20 dB, CNR ~50 dB at
  10 MHz RBW, 55 dB above noise floor (p.3).
- `time_bandwidth_product` (laser.comb): cheung2010 5.1 / 3.6 (p.3).
- `transparency_current_ma` (amplifier): komljenovic2015 SOA2 ~12-15 mA (p.6).

## Missing orgs

None needed for a fab / facility role. Printed orgs without a role here: OPTO+ (France Telecom/BD/CNET; Alcatel CRC,
Groupement d'Interet Economique) (menezo1999 p.1 affiliations); Aurrion (in the registry, affiliation only).
