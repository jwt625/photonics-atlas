# Batch lit_12 report (distill subagent, 2026-10-29)

Dry-run `batch lit_12: +26 components, +130 metrics; errors 0`. ASCII, no e-mail; quotes only a few words (tian2021 is
open_license_ok, no longer quotes). Every component has at least one performance metric. Not audited or merged.

## Per paper (components / metrics)

- ledezma2022 (1 / 12): dispersion-engineered PPLN degenerate OPA, 6 mm (amplifier.parametric, lnoi_rib): small-signal
  gain ~30 dB / ~50 dB/cm (1.2 pJ pump, 15 C), OPG-extracted gain >66 dB / 110 dB/cm (fit of own OPG data -> measured,
  "estimated" quoted in notes), gain bandwidth >600 nm (10 dB below peak), input coupling ~25 dB per facet
  (author_estimate, supplement not cached), geometry. Not entered: non-degenerate "~100 dB/cm, similar magnitude"
  (no separate value), Fig. 1(c) simulated comparison geometries, poling period (supplement only). Fab org_caltech (all
  authors Caltech, "To fabricate the device, we use ...").
- liu2025 (5 / 31): micro-transfer-printed InAs/GaAs QD SOA 1.66 mm (gain 7.51 dB @1299 nm 20 C, 4.03 dB @1314 nm 50 C,
  derived per D166; differential resistance 3.89 / 3.73 ohm), adiabatic III-V/Si taper (99.1 % simulated at 1 um
  misalignment), imec Si GC (single-GC loss ~8.5 dB from Fig. 5(b) inset, extracted_from_figure), QD DFB (threshold 70 mA,
  19.7 / 14.1 mW WG-coupled, SMSR 33.3 dB, linewidth 2.05 MHz -> 803.6 kHz, RIN, grating 390 nm / 1.4 mm), QD Vernier
  tunable laser (80 mA, <3 ohm, 3.6 mW, >35 nm, SMSR ~40 dB, design FSRs, ring radii). Not entered: SOA saturation
  (only "stable below -5 dBm"), taper feedback <-40 dB (no parameter), feedback-tolerance RIN / BER (D250), BER.
- cheng2024 (2 / 10): cryogenic PPLN waveguide (frequency_converter.shg, 4.3 um period, 1 cm poled; on-chip loss <1 dB
  author_estimate; geometry) and lensed-fiber end-fire coupling in the cryostat (7 / 8 dB per facet, author_estimate,
  7 K). Not entered: QPM wavelengths 774.33 / 763.13 nm (gap), theoretical >4000 %/W/cm2 (ref. [18]) and +3.8 %
  (calculation), photon-pair brightness / bandwidth / CAR (D250). No measured normalized efficiency in the paper.
- minami2023 (1 / 4): polarization-diverse cascaded SHG/DFG PPLN wavelength converter, C <-> L (frequency_converter.sfg_dfg,
  platform empty). Signal-to-idler CE mean / min-max per direction stored as power_conversion_efficiency_pct, dB -> %
  derived (9.9 dB = 977 %). Not entered: NF 5.0/5.4/4.7 and 4.8/5.0/4.6 dB (gap), CE roll-off above 0 dBm, system SNR.
  No fab statement (all NTT authors; D80b).
- rao2019 (4 / 18): nano-PPLN SHG 0.6 mm (2800 +/- 250 %/W/cm2 @1540 nm, 10.08 %/W derived, pulsed >10 % at 20 pJ,
  period 2.67 um) and 0.3 mm (4600 +/- 410 %/W/cm2, wavelength inferred from Fig. 2(f)); TFLN ridge waveguide
  (3 / 7 dB/cm by Fabry-Perot fringes); polished facet + lensed fiber (6 / 7 dB per facet measured). Fab
  org_university_of_central_florida (parent, D154). Not entered: poling duty 45-50 % (gap), SFG 1460-1620 nm range,
  simulated 5500 %/W/cm2.
- ghosh2012 (5 / 23): Ce:YIG/SOI MZI isolators with unequal arm widths, one row per arm length 1.49 / 0.99 / 0.49 /
  0.19 mm (isolation 11 / 10 / 6.8 / 2 dB from Fig. 5 annotations, TM; geometry on the 1.49 mm row incl. BCB ~80 nm as
  cladding_thickness_um derived); unequal-output 1x2 MMI (simulated 41 / 29 % split, 1.55 dB excess simulated, imbalance
  1.49 dB derived from the fitted (C2/C1)^2 = 0.71, MMI 3.9 x 12.5 um). Not entered: FSRs, ER (Fig. 6(b)), NRPS
  1.633 rad/mm, fitted differential loss 1.4 dB/mm, insertion loss (normalization not stated), MMI output offset 1.35 um
  (pitch vs gap ambiguous). Fab empty (procedures in refs. [6], [13]).
- ma2021 (5 / 21): polarization-independent four-port circulator on IMOS (nonreciprocal.circulator, inp_membrane):
  8 port-pair isolations TE / TM (27.0 / 24.1 / 19.9 / 18.6 dB; 34.0 / 30.9 / 16.8 / 16.4 dB), fiber-to-fiber
  transmittance ranges (Tables 1-2), Ce:YIG excess 3.0 dB (with vs without Ce:YIG, derived); IMOS waveguide 22 dB/cm
  (author_estimate); PC ~1.0 dB and 2x2 MMI ~1.0 dB (author_estimate, scope unspecified: per instance vs per path not
  stated); TE GC 6.9 dB loopback_half (13.8 dB pair halved). Not entered: cited PC >99 % / <10 um, 1.3 dB/cm [30],
  simulated 72 nm BCB. Fab empty (TU/e + Tokyo Tech).
- tian2021 (3 / 11): magnetic-free Si3N4 microring AOM isolator, main device (isolation 9.3 dB @1542.6 nm, max 10 dB at
  20 dBm per actuator, 9.5 dB @1545.55 nm, ~9 dB over 30 dB optical power, >8 dB for >20 ns pulses, IL 0.8 dB), second
  device with 950 nm gap (IL 0.1 dB), Si3N4 microring R 118 um (TE00 680 MHz, TM00 1160 MHz linewidths, extinction
  10.1 dB). Not entered: 700 MHz isolation bandwidth, RF drive powers, sideband conversion 8 %, HBAR / actuator data
  (2.958 GHz, k2 0.2 %, Qm 270, S21 -45 dB, crosstalk <-60 dB), kappa_ex ratios, 810 x 820 nm side assignment.
  Fab org_epfl + org_purdue_university (author contribution + "Samples were fabricated in the EPFL CMi, and Birck ...",
  p.11), facility org_center_of_micronanotechnology.

## Fab / facility organizations missing from the registry

- Kavli Nanoscience Institute (KNI) at Caltech: ledezma2022 p.5 Acknowledgments ("device nanofabrication was performed
  at"), facility.
- USTC Center for Micro and Nanoscale Research and Fabrication: cheng2024 p.7 Acknowledgments ("partially carried out
  at"), facility.
- NanoLab@TU/e: ma2021 p.7 Acknowledgment (use of cleanroom facilities), facility.
- Birck Nanotechnology Center at Purdue University: tian2021 p.11 Acknowledgments (samples fabricated in), facility.
- Plasma-Therm (printed "Plasma-Therm", "Plasma Therm LLC"): tian2021 p.10 Methods ("through foundry services"), p.11
  (AlN deposition performed at); fab role for the Mo / AlN films.

## Judgment calls for the coordinator

1. minami2023 signal-to-idler CE (dB, includes parametric gain) entered as power_conversion_efficiency_pct (977-1259 %);
   alternative: a dB conversion-efficiency parameter (gap below) and drop these 4 rows.
2. liu2025 fab org_imec on the hybrid SOA / DFB / tunable laser (Si circuit fabricated at imec; QD coupons pre-fabricated
   and printed by authors spread over Ghent University - imec, Innolume, EV Group, IMEC).
3. tian2021 fab = both fabrication sites named (EPFL, Purdue) per D83c; ledezma2022 org_caltech with a JPL dual affiliation.
4. ma2021 four-port circulator kept as nonreciprocal.circulator (a genuine 1 -> 2 -> 3 -> 4 -> 1 circulator, unlike the
   song2025a routers in nonreciprocal.other).
5. ledezma2022 OPG-extracted gain (66 dB / 110 dB/cm) as measured (standard fit of own data); author_estimate if the model
   assumptions (sinh^2 approximation, g proportional to sqrt(E_pump)) are judged assumed inputs.
6. ghosh2012 isolation values are Fig. 5 annotations (measured), wavelength = panel span (inferred).

## Registry gaps (value actually skipped, locator, proposed definition)

- center_wavelength_nm for frequency_converter: cheng2024 SH peak 774.33 nm (293 K) / 763.13 nm (7 K), p.5 Fig. 2(b).
  "Phase-matching (peak conversion) wavelength; fundamental or generated wave and temperature in condition".
- nf_db for frequency_converter: minami2023 conversion NF 5.0 / 5.4 / 4.7 dB (C-to-L), 4.8 / 5.0 / 4.6 dB (L-to-C), p.3
  Sec. III-B. "Noise figure of the converted (idler) output vs the input signal".
- conversion_efficiency_db for frequency_converter (only if call 1 is reversed): minami2023 CE 9.9 / 10.7 / 8.4 dB and
  10.4 / 11.0 / 9.5 dB, p.3. "Signal-to-idler power conversion efficiency in dB, as defined by the paper".
- fsr_nm and extinction_db for nonreciprocal: ghosh2012 measured FSR 2.3 / 3.4 / 6.8 / 18.4 nm (p.3 Sec. III);
  tian2021 backward extinction 6 dB of the 950 nm-gap device (p.20 Supp. Note 5). Definitions as for resonator / wdm
  (interferometer or resonance FSR; notch depth).
- isolation_bw_ghz for nonreciprocal: tian2021 700 MHz (p.3). "Isolation bandwidth in frequency (criterion in condition)".
- gap_nm for nonreciprocal: tian2021 bus-microring gap 950 nm (p.20). "Bus-resonator coupling gap of a resonant isolator".
- power_consumption_w (or a drive-power parameter) for nonreciprocal: tian2021 RF drive 14 dBm per actuator for C = 1,
  20 dBm per actuator (100 mW) for 10 dB isolation (p.3, p.7 Fig. 4). "Electrical / RF drive power, per actuator or
  total in condition".
- nrps_rad_per_mm for nonreciprocal: ghosh2012 differential NRPS 1.633 rad/mm (p.3, fit over four lengths).
  "Non-reciprocal phase shift per unit length (differential vs single-arm in condition)".
- poling duty cycle for frequency_converter: rao2019 45-50 % by AFM (p.5). "Inverted-domain fraction of the poling
  period (method in notes)"; not fill_factor (grating tooth fraction).
- Not confirmed (no definition settled): an operating-wavelength-range parameter for frequency_converter (rao2019 SFG
  pumps 1460-1620 nm, p.6).
