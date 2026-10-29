# Batch lit_25 report (distill subagent, 2026-10-29)

Dry-run `batch lit_25: +44 components, +306 metrics; errors 0`. ASCII, no e-mail, no quotes (all eight sources
`restricted_local_only`). Page-1 title / author check passed for all eight texts. Not yet audited or merged.

## Per paper (components / metrics)

- dirani2019 (4 / 30): LPCVD Si3N4 200-GHz rings, 1.63 x 0.8 um, fully subtractive process on 200 mm wafers. Gap 600 nm wafer T3
  (kappa_0 23 / 36 MHz, Q0 8.5e6 / 5.3e6 at 1560 / 1520 nm, splitting 60 MHz as 0.06 GHz derived, 3.5 dB/m -> 0.035 dB/cm
  derived le, abstract ~3 dB/m band average author_estimate, ng 1.79 author_estimate, 40 dBm CW handling); gap 550 nm (20-die
  mean / std of kappa_0 and extinction); T1 / T2 anneal variants (Fig. 3(b) Q0 means, extracted_from_figure). Not entered:
  thermal susceptibility 185 MHz/mW of dropped power (gap), Fig. 4(a)/(b)/(d) figure-only curves, sidewall roughness,
  TXRF contamination, earlier-work deposition values. Fab empty (authors CEA-LETI + CNRS-LTM + INL; no fab statement).
  Judgment: Fig. 3(b) gap not stated, T3 mean put on the 600 nm row with a note; power handling (stated for all
  microresonators) entered on both T3 rows; nominal 200 GHz FSR as author_estimate.
- dumon2004 (12 / 51): SOI photonic wires 400 / 440 / 450 / 500 nm (Table I, FP-cavity cutback), 3 um -> wire tapers (upper
  bounds 0.19-0.27 dB, author_estimate: rest on calculated 39.30% facet reflectance), racetrack R 5 um as wdm.mrr (FSR 14 nm,
  0.5 nm 3-dB, Q > 3000 derived, ng ~4.6, crosstalk 20 / 25 dB, drop loss ~3 dB, geometry) plus resonator.ring row of the same
  device (finesse 28 derived, round-trip 5 dB/mm -> 50 dB/cm derived; D396), ring Q 8000 (wdm.mrr; power coupling 1-4%
  derived from amplitude 0.1-0.2), 415 nm wire 2.2 dB/mm (author_estimate, origin not stated). Not entered: racetrack
  coupling factor 0.3 (amplitude vs power not stated), substrate-leakage share 1-1.5 dB/cm (simulated contribution),
  15 nm resonance shift per 5 nm width. Fab empty (passive; staff thanks for exposures / mask design).
  Judgment: Fig. 5 caption widths (500 / 450 nm) vs text (450 / 415 nm) for the same racetrack: text values used, both noted.
  Racetrack wavelengths c_band inferred (Fig. 6 spans 1500-1640 nm).
- li2024a (1 / 9): suspended Ta2O5 microdisk, D ~120 um, PLACE: QL 1.92e6 (fundamental, ~1560 nm), Qi 2.05e6 derived, three
  higher-order QL 1.34-1.44e6, FSR ~3.02 nm, radius 60 derived, film / BOX. Not entered: roughness, minimum transmission 77%
  as dB, Table 1 values of other works. Fab empty (SIOM, UCAS, ShanghaiTech, ECNU, ...). Film provided by Ningbo University
  (note only; text also describes own sputtering).
- lucia2026 (4 / 34): InGaAs-on-InP mid-IR spiral waveguides (1.3 TM / 1.04 TE dB/cm at 8.5 um measured; 4.6 um TM 0.3-1.0
  author_estimate, TE 0.42-0.72 extracted_from_figure, abstract 0.28 author_estimate with origin note), racetrack Lc 100 um
  (FWHM 101 MHz, QL 6.4e5 TM / 2.1e5 TE, Qi author_estimate because the coupling regime is assumed, 0.24 dB/cm), two 8.5 um
  racetracks with Lc not stated (separate rows, D159). Not entered: facet reflectivities 0.26 / 0.33, simulated Lc curves,
  Drude prediction. Fab empty (all authors C2N; work "performed within the C2N micro nanotechnologies platforms").
- cabanillas2021 (1 / 11): rapid adiabatic 3-dB coupler, 75 um, GlobalFoundries 45CLO (fab org_globalfoundries, process
  45CLO): SR 50 +/- 1.08% best (100 nm), +/- 3.27% / +/- 2.46% over 7 reticles (ranges derived), per-coupler IL < 0.2 dB at
  1290 nm and < 0.3 dB (derived upper bounds), FDTD SR / IL. Not entered: ref. [9] own earlier RAC results, Fig. 3(c)
  literature comparison. Polarization not stated.
- huang2018 (3 / 8): 10-mode triple-clad all-fiber photonic lantern (mode_converter.mdm_mux, ofc2026 M1C.4 precedent): IL
  0.6-2.0 dB per input (c_band inferred), length ~5 cm, ports; BPM design rows triple-clad (IL 0.01 dB) and double-clad
  reference (0.23 dB). Not entered: MDL (pairwise < 4.5 dB, ~2 dB each; simulated 0.03 / 0.7 dB) -> registry gap; preform
  hole / circle diameters (no parameter); ref. [3] lantern values. Fab empty (Bell Labs, CREOL, Southampton, Tianjin).
- zhou2021 (4 / 19): oxyhydrogen-flame HLPFG OAM converters in SMF, S1-S4 (pitch, length; -3 / -10 dB widths, S1 dip
  32.7 dB, twist-tuning ranges for S1 / S2). Abstract pairs S4's 303.9 nm (-3 dB) with S2's 182.2 nm (-10 dB); entered per
  device. Not entered: S5 (no stated width), -15.2 dB width 158.8 nm (no parameter), simulated DTP pitches. Fab empty.
- baghban2017 (15 / 144): LNOI sidewall Bragg gratings (reflector.bragg), 12 rows: rectangular LB 252.5 um dw 50-125 nm
  (ER 25 / ~27 dB, FWHM 10.8 / 23 nm), sinusoidal LB 252.5 and 505 um dw 50-125 nm (text 24.2 dB, 25.7 dB / 4.77 nm, ~3 nm;
  others from Fig. 6, pixel-calibrated against the three text points); 760 nm / 2.35 um waveguides (76.2 / 15.1 dB/cm);
  grating coupler (19.9 dB pair, 9.95 dB loopback_half, 16.74 dB simulated, > 80 nm 3-dB, geometry). Not entered: kappa*LB
  1.5-6.9 (computed, not per device), TMM curves, slab loss 3 dB/cm (origin not stated, not a component). Fab empty (all KTH,
  passive); LNOI wafer from Partow Technologies (note).
  Judgment: "around 27 dB" (rectangular dw 75-125) entered approx on each row (nevlacsil2020 precedent); rectangular widths
  as bw_fwhm_nm (paper says FWHM only), sinusoidal as bw_3db_nm (paper calls them 3dB bandwidths); stopband wavelengths
  only noted (S band for rectangular), not entered.

## Organizations missing from the registry

- "C2N micro nanotechnologies platforms" (lucia2026 p.9 Acknowledgements; facility where the work was performed). C2N is in
  the registry as a research institute (owner); facility_org_ids left empty pending a coordinator ruling.
- "RENATECH network" (lucia2026 p.9 Acknowledgements; "partly supported by"; facility network).
- Partow Technologies LLC (baghban2017 p.3; LNOI wafer supplier, note only).
- Ningbo University (li2024a p.6 Acknowledgments; Ta2O5 film provider, note only).

## Registry gaps

- `mdl_db` for mode_converter: huang2018 photonic lantern pairwise MDL < 4.5 dB over 191.45-195.85 THz (p.6 Fig. 7),
  ~2 dB per lantern; simulated 0.03 dB (triple-clad) / 0.7 dB (double-clad) (p.4). Proposed: extend `mdl_db` classes to
  mode_converter ("mode-dependent loss of a mode multiplexer, per device or back-to-back pair as stated in condition").
- `thermal_susceptibility_mhz_per_mw` (resonator): dirani2019 185 MHz/mW at 1560 nm (p.13 Fig. 5(b)). Proposed: "resonance
  shift per mW of optical power dropped into the resonator (self-heating), as reported".
- `corrugation_amplitude_nm` (reflector): baghban2017 dw 50 / 75 / 100 / 125 nm (p.4, p.6). Proposed: "sidewall modulation
  amplitude of a corrugated grating (w = w0 + dw f(x); definition as stated)". Currently only in labels / notes.
- `reflectivity_pct` or `facet_reflectivity` for waveguide_platform: lucia2026 fitted facet reflectivity 0.26 (TM) / 0.33
  (TE) at 8.5 um (p.4 Fig. 2). Proposed: allow `reflectivity_pct` for waveguide_platform (cleaved-facet power reflectivity).
- `bw_15db_nm` or a generic width-at-level parameter (mode_converter): zhou2021 S2 158.8 nm at -15.2 dB (p.5 Fig. 5(a)).
  Low priority (single value).
