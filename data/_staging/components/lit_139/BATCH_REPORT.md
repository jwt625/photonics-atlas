# lit_139 batch report (distiller, 2026-11-15)

Family: laser / free_space_emitter (benchmark-citation papers, DevLog-019 / D577). Five papers. Page-1 titles checked
against the source rows: all five cached texts are the paper of their row (chen2024c, snigirev2023, vissers2021,
nejadriahi2024 are arXiv versions of the journal papers; xu2022a is the JLT version); none is a correction / erratum;
no `garbled_text_layer`. Redistribution: nejadriahi2024 `open_license_ok`, the other four `restricted_local_only`
(facts and locators only). Validator: `merge_component_staging.py data/_staging/components/lit_139 --dry-run` -> +23
components, +126 metrics, 0 errors (only warning: the pre-existing merged cmp_lit_ni2025b_pimmwc-m18). 112 of the 126
metric rows were checked mechanically against a quoted snippet on the stated page of `text.md` (0 misses); the other
14 are figure reads or figure labels checked on the page renders.

| paper | components | metric rows |
|---|---|---|
| chen2024c | 4 | 20 |
| snigirev2023 | 2 | 16 |
| xu2022a | 6 | 41 |
| vissers2021 | 4 | 23 |
| nejadriahi2024 | 7 | 26 |
| total | 23 | 126 |

## chen2024c (SiN-on-SOI Vernier OPA LiDAR, 160 deg FoV, LPR 2024)

- Rows: Tx OPA (`free_space_emitter.other`, 128 ch, 3.8 um pitch): beam power within 3 dB over 158 deg (Fig. 2(b)
  caption; text "~160 deg" in notes), calculated beam-power 3-dB width ~170 deg (simulated), beam width 0.161 x 0.044
  deg at 0 deg and ~0.7 deg at the FoV edges (Supp. S2 / S4), vertical FoV ~3 deg over 42 nm, channels, pitch.
  Vernier transceiver (`free_space_emitter.other`, 256 ch): side-lobe suppression > 10 dB over -78 to 80 deg
  (`derived`: far field synthesized from separately measured Tx / Rx far fields), simulated 34 / 30 / > 16 dB at 0 /
  40 / 80 deg, ~160 deg ranging FoV, Rx pitch 4.2 um. Chained grating antenna (`grating_emitter`): simulated far-field
  3-dB width ~115 deg at wp 200 nm, SiN 1 um x 0.34 um. TO phase shifter: ~6 mW/pi (measured).
- Not entered: unidirectionality 82-91 % (Supp. S1, no parameter); 25 dBm in -> ~11 dBm main beam (p.6, no
  parameter); > 37 dBm SiN-on-SOI power handling (p.6, cited ref. 11); SNPR, ranging accuracy 5.5 mm, velocity (system
  level); wp 1 um 77 deg (unfabricated design); Table 1 / Table S1 values of other works.
- Fab: `org_amf` from the author contributions "G.L. support the wafer fabrication process" (p.8) with G.L. at
  "Advance Micro Foundry Pte. Ltd." (printed spelling). Borderline (D395 / D398 reading: the fabrication sentence names
  an AMF author). No facility. `process_name` empty ("multilayered SiN-on-SOI platform" names no PDK / process).
- Judgment calls: (1) Tx OPA and the Vernier transceiver as two rows (the Rx OPA alone has only design values); (2)
  phase-shifter platform empty (layer not stated; it follows the SiN-Si transition); (3) p_pi band `unspecified`
  (no wavelength stated anywhere for this value; the laser / EDFA band is not printed).

## snigirev2023 (LNOD self-injection-locked frequency-agile laser, Nature 2023; arXiv v3)

- Rows: `laser.sil` (InP DFB + LNOD ring, `lnoi_loaded_sin`): lasing 1555.4 nm, SMSR ~50 dB, intrinsic linewidth
  3.14 kHz, integrated FWHM 56 kHz / 262 kHz / 1.1 MHz (0.1 / 1 / 100 ms), Pockels tuning efficiency 0.237 / 0.220 /
  0.203 pm/V at 10 kHz / 100 kHz / 1 MHz (Supp. Fig. 8 inset reads 29.4 / 27.3 / 25.1 MHz/V converted with lambda^2/c),
  linear tuning band 600 MHz and ~500 MHz excursion as `tuning_range_nm` (lihachev2022 precedent). `resonator.ring`
  (102 GHz FSR): FSR, median linewidth ~100 MHz (593 resonances), Q_L ~1.9e6 (derived), 8.5 dB/m (author_estimate:
  near-critical-coupling reading, n_g not stated; D76 / D403), 4 um thermal oxide.
- Not entered: 3.9 dB per facet (p.2 cites ref. [38]; rule 3); Damascene < 1 dB/m (cited); power reflection 3 %
  (no resonator parameter); locking span ~1 GHz, >= 20 dB frequency-noise suppression, 12 PHz/s tuning rate, 1 %
  chirp nonlinearity, flat EO response to 100 MHz, 15 cm LiDAR resolution (no parameters).
- Fab: ring row `org_epfl;org_ibm_research_zurich` (author contributions p.8 name fabricators at both orgs; D80b,
  churaev2023); facility `org_center_of_micronanotechnology;org_binnig_and_rohrer_nanotechnology_center` ("samples were
  fabricated in" CMi and BRNC, p.8). SIL row: fab empty (DFB maker and assembly not stated; lihachev2022 SIL rows),
  same facilities.
- Judgment calls / conflicts (D417): (1) Fig. 2(c) caption calls the spectrum free-running DFB, the p.3 text assigns
  it (1555.4 nm, SMSR 50 dB) to the self-injection-locked laser; entered on the SIL row per the text. (2) The 100 MHz
  value is called the (loaded) resonance linewidth in the text (p.2, p.3, p.7) but the Fig. 2(b) histogram axis is
  kappa_0/2pi and its legend says 532 resonances (caption 593); entered as `linewidth_mhz` per the text. (3) Ring rows
  carry the inferred span 1500-1630 nm (Supp. Fig. 6 full span; histogram span not printed).

## xu2022a (fully integrated LiDAR transmitter, tri-layer Si3N4-on-Si, JLT 2023)

- Rows: Si3N4 Vernier ECL (`laser.tunable`, platform `other`): on-chip 18.5 mW at 420 mA (author_estimate: tap /
  FA de-embedding not described), 2.8 kHz intrinsic linewidth, worst-case SMSR 42.6 dB, 99.3 nm tuning
  (1471.92-1571.18 nm), simulated 93 nm / 63.3 dB. Reference Si ECL (saturates at 2.4 mW). Vernier MRR pair
  (`resonator.ring`, D400): simulated 95 nm Vernier FSR, design coupling 10 %, n_g ~1.95, circumferences 577 / 564 um,
  1 x 0.4 um. OPA (`free_space_emitter.other`, `si_sin_multilayer`): 0.051 x 0.016 deg (off-chip laser) and 0.049 x
  0.016 deg (on-chip ECL), 141 deg (psi) and 16.8 deg (theta) steering, 0.168 deg/nm, SLSR 11 / > 6 / 7.8 dB, simulated
  0.05 x 0.014 deg, 154 deg, > 15 dB, 256 elements, pitch 6.14 (average) / 3.6 um (minimum), on-chip IL ~2.7 dB
  (loss breakdown, author_estimate). Grating antenna (`grating_emitter`): simulated 0.16 deg/nm, SLSR > 29 dB, < 0.014
  deg, 0.7 um period, 14700 periods, 10.3 mm, 0.4 um Si. Si3N4 bus waveguide: power handling > 30 dBm (Fig. 10(c), 1 W).
- Not entered: beamforming loss 17 dB (p.8), 5 W average TO power (p.6), 0.01 deg steering error (p.6) (no
  parameters); simulated passive SMSR 5.87 dB of the cavity round trip; SSC geometry (270 nm tip, 17.9 deg, 60 um /
  15 um sections; geometry only, no coupling value); per-period 0.3 % emission (cited ref. [40], authors' own work,
  D259); MMI / interlayer-transition / phase-shifter unit losses (Supp. Table S2 not in the cached text); Sagnac (TSL)
  20 % reflectivity (simulation setting, not a result); threshold (Fig. 7(a) too coarse).
- Fab: `org_amf` ("Fabricated by Advanced Micro Foundry (AMF Singapore)", p.5) on PIC rows; ECL row also
  `org_sjtu_pinghu_institute_of_intelligent_optoelectronics` ("the chip is packaged by SJTU-Pinghu Institute", p.5;
  borderline D399: assembled FA + RSOA + PIC). Reference Si ECL fab empty (where it was made is not stated) and
  platform empty. `process_name` empty (no PDK named).
- Judgment call: on-chip IL 2.7 dB kept `author_estimate` + `loss_breakdown` (inputs in an uncached supplement); the
  wavelength span is the ECL tuning range, `wavelength_inferred` true.

## vissers2021 (hybrid InP / Si3N4 extended-cavity mode-locked lasers, OE 2021; arXiv v2)

- Rows: laser A (`laser.comb`, 1.2 mm cavity): 15.5 GHz, -3 dB 1.5 nm, 3.1 ps (sech2), threshold ~51 mA and centre
  ~1567 nm (figure reads), ~0.4 mW saturation in the lensed fiber. Laser B (3 cm): 2.18 GHz, -3 dB 4 nm, 465 lines in
  the -10 dB band, 6.31 ps, threshold ~59 mA and centre ~1564.5 nm (figure reads), ~0.4 mW. SU8 / Si3N4 butt coupler
  (`chip_chip_coupler.butt`, `polymer`): simulated 90 % mode overlap, 3.8 um x 875 nm (measured) SU8, 300 nm Si3N4,
  3.3 um oxide. Sagnac reflector (`reflector.loop_mirror`): 70 % (author_estimate, origin not stated).
- Not entered: RF linewidths 940 kHz (-10 dB Voigt, p.5) and 31 Hz (Lorentzian, p.7) (no parameter); -10 dB comb
  width 8.3 nm (`bw_10db_nm` not allowed on laser); 85-90 % overlap sweep and alignment window (design sweep / not a
  1-dB tolerance); intro "< 5 dB" coupling excess loss (general); output SU8 converter to the lensed fiber (3 um wide;
  geometry only, no value -> no row); loop bend radius 150 um (no reflector parameter).
- Fab: empty on all rows. SMART Photonics is named for the InP RSOA chip (p.2, acknowledgment p.8), which has no row
  (no RSOA-only metric); the Si3N4 chip fabrication is passive with no org; LioniX International supplied the SiN wafer
  material (note only). Coordinator option: the merged ibrahimi2021 MLL row lists both part fabricators on the laser
  row; under that reading the two laser rows would get `org_smart_photonics` (I did not apply it: rule 12 / D399 keep
  part orgs on part rows).
- Judgment calls / conflicts: p.2 says 15.8 GHz, everywhere else 15.5 GHz (D417); "saturation power of the lasers is
  around 0.4 mW" entered on both rows (sentence describes both; D465 reading); Fig. 6 caption panel letters (a)-(e) do
  not match the three-panel figure; Fig. 2 caption prints 875 "um" for the 875 nm SU8 layer.

## nejadriahi2024 (852 nm Si3N4 ECL, sub-100 Hz intrinsic linewidth, OL 2024; arXiv v2)

- Rows: ECL (`laser.tunable`, `other`, heim2025 precedent): ~24 mW maximum (ref plane chip), threshold ~60 mA, SMSR
  > 50 dB, ~65 Hz intrinsic linewidth, ~15 nm tuning. Vernier ring pair (`resonator.ring`, D400): single-ring FSRs
  31.19-31.26 pm as one range, Vernier overlap 15.6 nm (author_estimate), radii 2104.3 / 2100 um, 3 um width, 300 nm
  gap, stack from Fig. 1 labels (40 nm Si3N4, 8 um thermal oxide, 5 um top oxide). Sagnac loop mirror 60-80 %
  (author_estimate) and its DC (20-30 %, 1.25 x 100 um, 400 nm gap; D396 cross-notes). RSOA-to-taper butt coupling
  typical ~50 % across chips (measured). 40 nm Si3N4 waveguide ~0.1 dB/cm (printed ~10 dB/m). RSOA
  (`amplifier.soa`, purchased Photodigm 850SAF100): 15 nm 3-dB optical bandwidth (specification).
- Not entered: 6.5 cm round-trip optical length; 0-500 mW heater range (no per-actuator efficiency); taper "extends up
  to 11.1 um" (role of the dimension not stated) and 10.5 deg angle; RSOA 1 mm optical length, R ~90 % / 0.1 % facets,
  845-855 nm centre, 14 x 3 um beam (no amplifier parameters); Schawlow-Townes estimate.
- Conflicts (D417): output power 24 mW (abstract, p.1, p.4) vs ~25 mW at 215 mA (p.3); reference plane free-space at
  the chip output (p.2, Fig. 2(a) caption, conclusion) vs "fiber-coupled output" (p.3), entered as chip; tuning
  "~15 nm" vs the Fig. 3 peaks spanning about 846.0-854.6 nm; the printed FSR pairing assigns the larger FSR to the
  larger radius (inverted vs FSR ~ 1/R), so no per-ring FSR is entered (D159).
- Fab: empty on all rows. Borderline JPL fab (acknowledgment thanks JPL cleanroom staff for assistance in the
  preparation of samples; research carried out at JPL; D84b / D448), but JPL is not in the registry.

## Missing fab / facility orgs (name as printed + locator)

- "Jet Propulsion Laboratory, California Institute of Technology" (nejadriahi2024 p.1 affiliation, p.4
  acknowledgment): borderline fab (D84b / D448) for the 7 nejadriahi2024 rows; parent org_caltech. Also pending from
  D419 (kittlaus2020a) and the header org_requests.
- "Photodigm, Inc." (nejadriahi2024 p.2): vendor of the purchased RSOA (fab on cmp_lit_nejadriahi2024_rsoa_850saf100
  under rule 12 vendor clause, D554 precedent).
- Alias: "Advance Micro Foundry Pte. Ltd." (chen2024c p.1 / p.8 / p.10 affiliation, printed spelling) -> org_amf.

## Registry gaps (skipped value + locator + proposed definition)

- `rf_linewidth_hz` (laser): vissers2021 940 kHz (-10 dB, Voigt fit, p.5) and 31 Hz (Lorentzian fit of SSB phase
  noise, p.7). "RF beat-note (repetition-rate) linewidth of a mode-locked laser; level / fit in condition" (D431
  candidate).
- `bw_10db_nm` widened to laser: vissers2021 8.3 nm -10 dB comb width (p.7).
- Reflection on resonator: snigirev2023 power reflection up to 3 % (p.3, Fig. 2(a)). "peak power reflection of the
  resonator (backscatter) at resonance, %" (D540 candidate).
- Laser locking / chirp parameters: snigirev2023 self-injection locking span ~1 GHz (p.3), tuning rate 12 PHz/s (p.5),
  minimum chirp nonlinearity 1 % at 100 kHz (p.4). Proposed `locking_range_ghz`, `chirp_rate_hz_per_s`,
  `chirp_nonlinearity_pct` (D431 candidate).
- Beamforming / main-lobe loss on free_space_emitter: xu2022a 17 dB (p.8, Fig. 10(d)); chen2024c 25 dBm in -> ~11 dBm
  main beam (p.6). "loss from the power entering the array to the power in the main lobe, dB".
- `power_consumption_w` widened to free_space_emitter: xu2022a average TO power 5 W after phase alignment (p.6) (D432
  candidate).
- Emission directionality on free_space_emitter: chen2024c unidirectionality 91 % at 1560 nm, minimum 82 % over
  1510-1630 nm (p.11, Supp. Fig. S1). "fraction of radiated power emitted upward, P_up / (P_up + P_down), %".
- Steering accuracy: xu2022a maximum error 0.01 deg over 350 incidences (p.6). "maximum pointing error over repeated
  steering, deg".
- `min_bend_radius_um` on reflector: vissers2021 Sagnac loop bend radius 150 um (p.4) (D430 candidate).
