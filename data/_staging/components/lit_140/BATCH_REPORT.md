# lit_140 batch report (distiller, 2026-11-15)

Family: laser / free_space_emitter (benchmark-citation papers, D577). Five papers, all cached texts checked against
their source rows (page-1 titles match; fan2020 and lihachev2024 are the arXiv versions of the journal papers,
oldenbeuving2012 the arXiv version; same works, D430 / D433). No `garbled_text_layer`. Merge dry-run: +32 components,
+165 metrics, 0 errors (one unrelated existing warning on ni2025b). Helper: session scratchpad
`lit_140/build_lit140.py`.

| paper | components | metric rows |
|---|---|---|
| fan2020 | 6 | 33 |
| tran2019 | 12 | 64 |
| poulton2019 | 3 | 11 |
| lihachev2024 | 5 | 28 |
| oldenbeuving2012 | 6 | 29 |
| total | 32 | 165 |

## fan2020 (hybrid InP-Si3N4 laser, 40 Hz intrinsic linewidth)

Rows: hybrid laser (`laser.tunable`, platform `other`, zhao2016 precedent), feedback arm (`reflector.other`,
simulated Rf 51 %, 3.6 pm FWHM, 12.5 dB side-resonance suppression), Vernier ring pair R 99 / 102 um and R3 1485 um ring
(`resonator.ring`, D400), double-stripe waveguide (`waveguide_platform.straight`, < 0.1 dB/cm on 5 / 10 / 15 cm test
structures), COVEGA SAF 1126 gain chip (`amplifier.soa`, MFD from the far-field specification, `author_estimate`).

Not entered and why:
- White frequency-noise level 6.5 +/- 1.3 Hz2/Hz (p.12): no frequency-noise parameter (registry gap); the derived 40 Hz is entered.
- 290 Hz earlier result (p.12, ref. [26]) and 0.045 dB/m Si3N4 loss (p.13, ref. [48]): cited (rule 3).
- Gain-to-Si3N4 coupling Tc 90-93 % and 98 % fiber coupling (p.7): sentence carries ref. [43] (D80i); Ri about 3 %
  and the 10 % interface loss are assumed loss-budget inputs.
- Specified gain-chip output 60 mW, HR 90 % / AR 1e-4 facet values, 6 deg tilt: datasheet values without a fitting
  parameter on `amplifier` (reflectivity) or kept in notes.
- Calculated photon lifetime (Fig. 3), roundtrip optical length 0.49 m, intracavity power 4 W / 0.15 GW/cm2: no parameter.
- Mode size 1.6 x 1.7 um2, index contrast 0.53: not a facet MFD; notes.
- Fig. 12 linewidth-vs-threshold-factor points: figure only, no per-point values needed beyond the PSD value.

Fab / facility: none stated (platform only cited as ref. [42]; authors at University of Twente and LioniX
International). Missing org: COVEGA (vendor of the SAF 1126 gain chip, fab role, p.6), not in `organizations.csv` /
`org_aliases.csv`.

Judgment calls:
- Ring Q, finesse, FSR and kappa^2 are printed in the laser-design section without a stated origin: `author_estimate`
  (D82a). The two Vernier rings share one population row (values printed once for both, D165 / D254).
- 40 Hz `derived` (2 pi x PSD level, arithmetic printed; ji2026 / jin2021 precedent); statistic `best` ("as low as").
- The feedback arm (three rings + Sagnac mirror) is a `reflector.other` row carrying only simulated values (fabricated
  part, D80e).
- Waveguide loss method `unspecified` (IR-camera scattered-light imaging on three lengths; no enum value); band C
  inferred (no measurement wavelength printed).

## tran2019 (heterogeneous Si/InP ring-resonator tunable lasers, Gen. 1 and Gen. 2)

Rows: Gen. 1 dual-ring laser (threshold, figure-read output 11.3 mW at 150 mA, 40 nm tuning, SMSR > 50 dB and 45-55 dB
map range, linewidths 2.1 kHz / 1.7-2.1 kHz across the band / 4 kHz at zero detuning, model 2 kHz, 66 pm mode spacing,
0.25 nm continuous tuning, footprint), its two rings (R 60 / 62.5 um; measured 1.7 nm FSR on the 60 um ring), front
loop mirror (designed 40-50 %), 15 % MMI tap, two rib waveguides (1.2 / 1.0 dB/cm at 1550 nm for 650 / 800 nm widths);
Gen. 2 triple-ring laser (threshold about 100 mA, about 3 mW, 110 nm tuning 1490-1600 nm, SMSR 40-55 dB, < 220 Hz,
model < 100 Hz, 114 nm superstructure period), triple-ring mirror (simulated SMSR > 8 dB) and its three rings
(R 599.97 / 600.86 / 707.57 um, kappa^2 0.09, 1.8 um / 56 nm etch geometry).

Not entered and why:
- Ultra-low-loss waveguide loss about 0.16 dB/cm and minimum bend radius about 600 um (p.9, p.12): stated "based on the
  results in [22]" (authors' earlier paper; rule 3, D259). No Gen. 2 waveguide row for that reason.
- Si/III-V taper loss 0.5 dB and < -33 dB reflection (p.2): cited [26], [27]; Table I lists 0.5 dB as a model input.
- Table I model inputs (ng 3.689 / 3.608, internal loss 6 /cm, nsp, alpha_H): model parameters, not measurements.
- Fig. 13(b) output power (about 10.8 mW at 120 mA, zero detuning): separate measurement, conflicts with the Fig. 9 L-I
  level at 120 mA (about 8.5 mW); left in notes.
- Effective cavity length > 50 mm (Fig. 19) and the Fig. 15 coupling map: no parameter / simulated design maps.
- Heater powers of the 2D tuning maps (0-70 mW axes, Figs. 10 and 23): no per-range tuning power printed.

Printed conflicts (D417 notes): white-noise level 65 Hz2/Hz in the p.7 text vs 650 Hz2/Hz in Fig. 12(a)-(b) (pi x 650
= 2.04 kHz matches the printed 2.1 kHz); the text cites "Figure 26" for the Fig. 24 noise spectrum; Fig. 8(a) labels
the ring-mirror coupler "1x2 MMI" while the text says 3-dB MMI.

Fab / facility: empty. Gen. 1 "built upon the standard process-design-kit for the heterogeneous Si/InP developed at
UCSB" and "fabricated in a standard Si/InP heterogeneous process [35], [36]" (p.4-5); Gen. 2 "fabricated in a modified
version of the Si/III-V heterogeneous process" (p.10). Coordinator question 1: does "PDK developed at UCSB" name the
fabricating org (Contract v7 "org named with the process"), which would set `org_ucsb` on the 9 Gen. 1 rows (and the
Gen. 2 rows by "the" process)? Distiller kept fab empty (D80b, passive sentences; "developed at" names the PDK author).
`process_name` keeps the printed wording. Staff thanks (Morton Photonics, UCSB individuals) do not set fab / facility.

Judgment calls:
- Gen. 1 output plane: broad-area photodetector, plane not stated -> `ref_plane unspecified`.
- Gen. 1 / Gen. 2 rib waveguide geometry (231 nm etch of 500 nm, 1 um BOX / cladding) is restated on each Gen. 1 ring
  and waveguide row; the 1.8 um / 56 nm geometry on each Gen. 2 ring (no waveguide row, loss cited).
- Front mirror and MMI tap rows carry only design values (`author_estimate`, D82a); kept because the parts are on the
  fabricated chip (D80e). Their waveguide etch is not stated for Gen. 1: platform `soi`.
- tran2019 is an invited review of the authors' own lasers; no laser value sentence or figure caption cites an earlier
  paper of theirs (D408), so the laser measurements are entered; only the waveguide / taper values attributed to [22],
  [26], [27] are left out.

## poulton2019 (512-element OPA LiDAR / FSO)

Rows: 512-element OPA (`free_space_emitter.other`: n 512, 1.65 um pitch, FWHM < 0.04 deg, SLSR 12 dB, steering 56 deg
phase x 15 deg wavelength), electro-optic phase shifter (`phase_shifter.other`, 2.4 dB mean loss per element over C+L,
2 pi, <= 2 uW), 1x512 distribution network (`splitter.other`, 0.6 dB estimated, `author_estimate`).

Not entered and why:
- Total OPA power < 1 mW: no power parameter on `free_space_emitter` (registry gap, as D432).
- Antenna upwards directionality > 90 % (approximate, from about 1 dB element-factor fringes, 1450-1640 nm) and
  simulated > 93 %: no directionality parameter (registry gap); no antenna row without a performance metric.
- "< 30 us phase shifter time constant" (abstract): the body ties about 30 us point-to-point steering to the FPGA-DAC
  interface; an EO phase shifter has no thermal time constant; settling about 6 us (FSO test) also not entered.
- Grating-lobe loss about 1 dB, noise floor about -25 dB (camera-limited), aperture about 10 mm2, yield > 95 %
  (expected): no fitting parameter or estimate only; notes.
- LiDAR ranges (25 m, 185 m, 3D at about 7-12 m) and FSO links (10 Gbps at 50 m, 1 Gbps point-to-multipoint):
  system results.
- Passive large-scale OPAs used for LiDAR / FSO: no component-level value printed; no rows.

Fab / facility: empty ("fabricated on 300 mm SOI wafers in a silicon photonics process", passive; all authors at
Analog Photonics; poulton2022 precedent). `process_name` empty (generic wording).

Judgment calls: phase shifter class `phase_shifter.other` (electro-optic, gagino2024 / D451 precedent) and an EO-atlas
candidate; loss band `cl_band` ("similar throughout the C+L band"); splitter band inferred from C+L operation.

## lihachev2024 (frequency-agile RSOA / Si3N4 Vernier laser with PZT actuators)

Rows: Vernier ECL (`laser.tunable`: 400 Hz, 6 mW in fiber at 1567 nm, SMSR 50 dB, Vernier FSR 8.7 THz, PZT excursions
1833 / 1516 MHz as nm, <= 3 GHz single-mode range), Vernier filter (`reflector.other`, reflection peaks up to 25 %),
rings R1 / R2 (`resonator.ring`: FSR 96.724 / 97.919 GHz, kappa_0 43.5 / 64.4 MHz, kappa_ex 97.7 / 96.0 MHz, 350 nm
gap, 2200 x 900 nm, 2.5 um cladding; R1 total linewidth 110-140 MHz from Fig. 2(d)), PZT actuator (`phase_shifter.other`:
166 MHz/V laser tuning and 150 MHz/V static ring shift as pm/V, 7 / 6 ns rise / fall, 75 nW).

Not entered and why:
- Chirp nonlinearity 1.5 % / 1 % before and 0.05 % / 0.25 % after linearization (p.5): registry gap
  (`chirp_nonlinearity_pct`, candidate since D431).
- Flat electro-optical response up to 960 kHz (p.4): not a 3-dB bandwidth (registry gap, as lihachev2022).
- Ring radii: diameters 472 / 465 um printed without assignment to R1 / R2 (D159); in notes.
- Wavelength switching up to 4 FSRs (400 GHz): stated from the PZT saturation voltage, not demonstrated.
- RSOA (Thorlabs SAF1126C, 90 % back facet): no performance value; no row (vendor note on the laser row).
- LiDAR 1.8 GHz / 8.5 cm resolution: system result.

Printed conflicts (D417 notes): Vernier FSR 8.7 THz vs 7.9 THz from the printed ring FSRs; "after multiplying by 2 pi"
vs 400 Hz = pi x 127 Hz2/Hz; Fig. 2(c) caption "intrinsic linewidth of 96 MHz" vs panel labels (64.4 intrinsic, 96.0
external); the text gives kappa_ex 96.0 MHz for both rings, the Fig. 2(b) label for R1 is 97.7 MHz (entered).

Fab / facility: Si3N4 rows (filter, rings) fab `org_epfl` (R.N.W. fabricated the device, contributions p.7; EPFL
affiliation) with facility `org_center_of_micronanotechnology` (CMi named for chip fabrication); actuator fab
`org_purdue_university` (H.T., A.A. designed and fabricated actuators and microheaters) with facility
`org_birck_nanotechnology_center`; laser row fab empty (packaging by authors with dual EPFL / Deeplight affiliations,
D83c), both facilities listed. Missing org: Radiant Technologies Inc. (PZT layer fabricated there, p.7; fab role on
the actuator row; already queued in D431).

Judgment calls: kappa_0 / kappa_ex `author_estimate` (symmetric coupling assumed, regime not determined from the data,
D403; lihachev2022 precedent); rise / fall times `derived` (ns -> us) from tanh fits; MHz-per-volt and MHz excursions
converted to pm/V and nm at 1559 nm (`derived`).

## oldenbeuving2012 (25 kHz waveguide-based external-cavity laser)

Rows: WECSL (`laser.tunable`: threshold 5.6 mA, 1.0 mW, SMSR 50 dB best / 40-50 dB typical, 25 kHz, 5 Hz theoretical,
>= 44 nm tuning, Vernier FSR 42.6 nm measured / 44 nm design), MRR mirror (`reflector.other`: about 20 % reflectivity,
PHR 0.55 as 2.6 dB, design 2.0 dB), ring pair (`resonator.ring`: R 50 / 55 um, design FSRs 4.4 / 4.0 nm, 4.0 nm switch
step, fitted kappa^2 0.39 and ng 1.7293), R1 heater (`phase_shifter.thermo_optic`: 200 us 10-90 % switching), HHI gain
chip free-running (`laser.other`: threshold 17.8 mA measured / 17.0 mA specified, 7.4 mW, SMSR 24 / 20 dB, 2.5 GHz
FWHM, 19 deg divergence, 6 um FWHM MFD), 5 % tap coupler (`splitter.directional_coupler`, design).

Not entered and why:
- TriPleX scattering loss <= 0.06 dB/cm and bend loss about 1 dB/cm at R 50 um (p.3): cited refs. 15, 16 (rule 3).
- Mode-field diameter about 1.5 um of the box-shaped waveguide (p.3): no waveguide row (only geometry-like value).
- Calculated single-ring FWHM 0.51-0.52 nm for kappa^2 0.44 (design kappa, not the fitted mirror), cavity photon
  lifetime 13.5 ps, finesse F0 0.89 / F1 440: model values; notes.
- Gain slope 0.48 dB/nm: no parameter. Other mirrors' 20-30 % reflectivity: population of other devices (note).

Fab / facility: mirror chip "We have fabricated such frequency selective waveguide circuits ... (TriPleX)" (p.3) with
authors at University of Twente, XiO Photonics, FOM DIFFER, Delft / Zhejiang: fab empty (D154 / D395). Gain chip fab
`org_fraunhofer_heinrich_hertz_institute` (custom chip supplied by HHI, vendor rule 12; zhao2016 precedent).

Judgment calls:
- Free-running gain chip classed `laser.other` (it lases on its residual facet feedback; threshold / SMSR / linewidth
  are laser parameters; D396), platform empty (material not stated, D422).
- Mirror reflectivity 20 % `derived` (ratio of two port powers); PHR converted to dB (`derived`); kappa^2 and ng from a
  model fit with equal-kappa assumption `derived` (D80a), on one ring-pair row.
- The 25 kHz linewidth is a self-heterodyne Lorentzian FWHM (half of the 50 kHz beat width), not a frequency-noise
  intrinsic linewidth; condition says so.
- Heater rise / fall both 200 us (the paper prints one value for both switching directions).

## Missing orgs (name as printed + locator + role)

- COVEGA (fan2020 p.6, "The InP semiconductor amplifier (COVEGA, SAF 1126)"): fab (vendor) of
  `cmp_lit_fan2020_covega_gain_chip`.
- Radiant Technologies Inc. (lihachev2024 p.7, "PZT layer was fabricated at Radiant Technologies Inc."): fab of
  `cmp_lit_lihachev2024_pzt_actuator` (queued since D431).

## Registry gaps (skipped value + locator + proposed definition)

- `frequency_noise_hz2_per_hz` (white frequency-noise level, one- or two-sided in condition): fan2020 6.5 Hz2/Hz
  (p.12), tran2019 650 / 70 Hz2/Hz (p.7-8, p.11-12), lihachev2024 127 Hz2/Hz (p.3). Candidate since D431 / D448.
- `chirp_nonlinearity_pct` (RMS deviation of a frequency chirp from a fitted ramp, relative to the excursion; rate in
  condition): lihachev2024 1.5 / 1 / 0.05 / 0.25 % (p.5). Candidate since D431.
- Flat-band actuation bandwidth (phase_shifter, kHz, criterion in condition): lihachev2024 960 kHz (p.4), as lihachev2022.
- `power_consumption_w` on free_space_emitter: poulton2019 < 1 mW total (p.2). Candidate since D432.
- `directionality_pct` on free_space_emitter (fraction of radiated power emitted upwards): poulton2019 > 90 %
  (approximate measurement) / > 93 % simulated (p.3).
- Facet reflectivity on amplifier / laser (`reflectivity_pct` widened): fan2020 Rb 90 % (p.6), oldenbeuving2012 85 % /
  0.1 % specified (p.5), lihachev2024 RSOA 90 % (p.2).

## Coordinator questions

1. tran2019 fab: is "standard process-design-kit for the heterogeneous Si/InP developed at UCSB" enough for
   `org_ucsb` (Contract v7 "org named with the process"), or does D80b keep it empty? Recommendation: keep empty
   (the sentence names who developed the PDK; the fabrication sentence is passive and names no org).
2. lihachev2024 laser row: keep fab empty for the packaged assembly (dual EPFL / Deeplight affiliations of the
   packagers), or set `org_epfl` as for the chip rows? Recommendation: keep empty (D83c, hiratani2024 precedent).
