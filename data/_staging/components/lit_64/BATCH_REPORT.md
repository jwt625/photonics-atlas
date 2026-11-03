# Batch lit_64 report (distill subagent, 2026-11-02)

Dry-run `batch lit_64: +40 components, +246 metrics; errors 0` (one WARN about another batch's row,
cmp_lit_ni2025b_pimmwc-m18). All seven sources are `restricted_local_only`: facts and locators only. ASCII only; no e-mail,
street or postal text in the rows. Page-1 title check: all 7 texts match their source rows; none is a correction / erratum;
no `garbled_text_layer`. Rows built by a scratchpad script (one spec file). Figure renders checked: thiessen2020 pp.3, 4, 7;
kharas2020 pp.3, 9; wang2025 pp.7, 8; zhang2025c pp.3, 7; guzman2019 pp.2, 6; lihachev2022 pp.4, 5.

## Per paper (components / metrics)

- thiessen2020 (11 / 73): 6 III-V-on-Si O-band lasers (laser.heterogeneous, platform other: FP L / H, DM L25 / L50 / H25 / H50):
  Table 1 threshold, max on-chip power (derived, 6.8 dB GC loss removed, D394), Lorentzian minimum, resistance range 6-6.8 ohm,
  SMSR, 660 um cavity, 4 um width, 300 nm c-Si. Rear DBR and two front DBRs (reflector.bragg, soi): simulated reflectivity,
  simulated 36 nm / observed 26 nm bandwidth, period, periods. Interlayer transition (simulated 0.14 dB). Output GC (6.8 dB
  test structures, back reflection design). Not entered: Gaussian linewidth 200-300 kHz (family statement, notes), group index
  3.81 (no laser parameter), delta n, slot index step, all comparison values.
- kharas2020 (4 / 37): single-element SCOWECL (laser.ecl, other): 312 / ~280 mW, 360 mA, ~10 % WPE, 55 dB, 1538.6 nm, RIN,
  192 kHz / 8 kHz, FSR, mode 5.1 x 4.0 um. 4-element array: ~80 mW / channel, 34 dB, ~1 nm, 50 um. SiN DBR (reflector.bragg, sin):
  ~20 %, 0.23 nm, 18 mm, 508 nm. SCOWA-to-SiN coupler (chip_chip_coupler.butt): 1.6 dB (n = 8), 2 dB (B, C), 0.8 um gap, mode,
  taper. Not entered: 0.2 dB/cm SiN loss (cited ref. [1]); FDTD sensitivities (no 1-dB value, notes); placement errors (notes);
  SiN edge coupler (no loss stated).
- wang2026f (5 / 21): InAs/InP QD FP lasers (laser.other, inp): 15 um x 3 mm with ~265 mA, 8.5 mW / facet, 2018.4 nm, 90 pm/K,
  T0 27 K, 882 mA at 50 C (derived), FSR; 15 um x 1 / 1.5 / 2 mm threshold derived from printed Jth; 8 um x 3 mm ~200 mA. Not
  entered: Jth, Jtr, internal loss, internal efficiency, differential gain, maximum temperature (registry gaps); QD density / PL
  data (material, not a component); lasing FWHM 7.4 nm (D250).
- lihachev2022 (12 / 32): SIL lasers at FSR 190.7 / 9.87 / 2.45 GHz and PZT 100 GHz (laser.sil, sin): integrated linewidths at
  1 / 10 / 100 ms, 1556 nm, tuning ranges converted to nm. DFB chip (laser.dfb). Feedback rings (resonator.ring, D396, D400): FSR,
  Q0 bounds, kappa_0 < 10 MHz (author_estimate, D403). AlN single, AlN dual apodized, PZT actuators (phase_shifter.other): tuning
  efficiency in pm/V (derived), mechanical resonances. Not entered: 25 Hz intrinsic linewidth and SMSR 60 dB (see judgment 1);
  frequency-noise floors, chirp nonlinearity, flat actuation bandwidth (gaps); 1 dB/m (not tied to a ring); HBAR 17 MHz (citation in
  the sentence); commercial laser comparison.
- wang2025 (3 / 27): triple-lattice QD PCSELs (laser.pcsel, gaas): a = 386 nm full set at 10 / 25 C; a = 376 nm, 60 um aperture
  and a = 381 nm, 40 um aperture with threshold, figure-read power, wavelength. Not entered: Jth, simulated mode loss, confinement
  factors, PC filling factor (not the fill_factor definition), FWHM 0.1 nm, PL data.
- zhang2025c (3 / 36): tunable ring laser (laser.tunable, inp); 2 mm grating antenna (free_space_emitter.grating_emitter, inp):
  divergence, SLSR, steering, angles, geometry; 800 um taper (waveguide_platform.other, simulated < 0.01 dB). Not entered: grating
  kappa and back reflection in /mm and dB/mm (no parameter); etch depth (30 nm layer, depth not explicit); values of ref. [14] etc.
- guzman2019 (2 / 20): 100 GHz MCPMLL (laser.comb, inp): repetition rates 100 / 25 GHz, line spacing, comb lines, SMSR, threshold
  ranges, fiber-coupled power, 1.66 mm, footprint. MIR (reflector.other): 60 / 40 % (author_estimate, origin not stated). Not
  entered: RF linewidths and locking data (gap below); boost SOA (LI with the other sections off, no gain: no row); 2x2 MMI (no
  value).

## Papers stopped on

None.

## Missing orgs (not in `organizations.csv` / `org_aliases.csv`)

- Birck Nanotechnology Center, Purdue University (lihachev2022 p.10 acknowledgements): facility for chip fabrication; wanted on
  the AlN actuator rows and SIL rows.
- Radiant Technologies Inc. (lihachev2022 p.10): "PZT actuators were fabricated at"; wanted as fab on `pzt_actuator`.
- OEM Group Inc. (lihachev2022 p.10): AlN deposition performed there; note only unless ruled a fab org.

Fab left empty on purpose: thiessen2020 (unnamed foundry; SCINTIL and CEA-Leti not tied to fabrication), wang2025 (passive voice,
four orgs), zhang2025c (judgment 3), lihachev2022 SIL assemblies and DFB (supplier people named, no org printed).

## Judgment calls for the auditor

1. lihachev2022 25 Hz intrinsic linewidth and SMSR > 60 dB: no resonator named, so D159: not entered, in notes on all SIL rows.
   pi x 8 Hz2/Hz (2.45 GHz floor, p.3) = 25 Hz would point to `sil_2p45ghz`, but the relation and the assignment are not printed.
   Recommendation: keep out unless the coordinator accepts that arithmetic as identifying the device (then `linewidth_hz` 25,
   author_estimate).
2. kharas2020 coupling loss 1.6 / 2 dB: `derived` (ratio of own responsivities with two stated assumptions, D80a); rule 4 could read
   `author_estimate`. 0.23 nm DBR bandwidth in `stopband_width_nm` with "level not stated" (dolgaleva2011 / giuntoni2009 precedent).
3. zhang2025c fab empty: the paper names the SMART Photonics generic platform but no fabrication sentence (D80b); `process_name`
   kept. Recommendation: confirm against D84a.
4. zhang2025c Fig. 6: text order (1568, 1497 nm) reverses the caption order; 0.044 deg / 5.5 dB attached to 1568 nm, 0.048 deg / 12
   dB to 1497 nm. Panel (b), 1568 nm by its angle axis, has the larger sidelobes, which supports this.
5. wang2026f sibling rows: threshold_ma from printed Jth x ridge area (derived; assumes 15 um area, checked by 589 A/cm2 <-> 265 mA
   at 3 mm). If threshold from density is not accepted, the three shorter lengths lose their only performance metric and should be
   deleted, with the Jth values in the 3 mm row notes.
6. wang2025 threshold about 80 mA: printed without tying it to one device; `measured` on the 60 um device, `extracted_from_figure` on
   the 40 um device (Fig. 7(a) kinks near 80-82 mA). a = 386 nm tied to the Fig. 5 device through the Fig. 7(b) legend (1245 nm) and the
   SEM lattice constant.
7. thiessen2020 DM L25 threshold 48 mA (Table 1) vs 49 mA (p.5): table stored. Resistance range 6-6.8 ohm entered on all 6 rows as a
   true bound (D254 forbids one representative row, not this). DM H25 / H50 SMSR 64 / 66 dB `approx`, paper hedges.
8. guzman2019 5.8794 nm is also printed as 1.1372 THz (about 0.72 THz at that wavelength): nm stored, mismatch in notes (D417). Text
   says SMSR > 25 dB for all cases while Fig. 6(a) labels > 20 dB. Line spacing in `channel_spacing_nm`; repetition rate wording is
   the paper's (D83b).
9. lihachev2022: FSRs `author_estimate` (origin not stated, D76); GHz and MHz/V converted to nm and pm/V with lambda^2 / c at 1556 nm
   (precedent andreou2019, churaev2023). Mechanical modes of the chip entered on the actuator rows, since they limit the actuator.
   Actuators follow the `phase_shifter.other` precedent (dong2021, hosseini2015).
10. wang2026f `temperature_k` empty for RT values: no number printed for RT in the main text.

## Registry gaps (skipped value, locator, proposed definition)

- `rf_linewidth_hz` (laser): guzman2019 100 GHz tone ~400 kHz at -3 dB (p.6 Fig. 7(b)), 150 kHz (p.1, p.7), 350 kHz at 25 GHz (p.1), hybrid
  < 1 Hz (p.7). Definition: electrical beat-tone linewidth of a mode-locked laser (level in condition). No merged `linewidth_hz` row
  holds an RF linewidth, so these stay out.
- `threshold_current_density_a_per_cm2` (laser): wang2026f 589, 993, 760, 664 (p.6), 1960 at 50 C; wang2025 1770 (p.6); kharas2020 900
  (p.7). Per-layer values in condition.
- `max_operating_temperature_k` (laser): wang2026f 50 C (p.6).
- `internal_loss_per_cm`, `internal_efficiency_pct` (laser): wang2026f ~6.7 /cm, 60 % (p.6). `group_index` for laser: thiessen2020 3.81 (p.6).
- Frequency-noise floor (`frequency_noise_hz2_per_hz`, laser; confirmed gap of D418): lihachev2022 8 / 10 / 300 Hz2/Hz at 3 MHz (p.3).
- `chirp_nonlinearity_pct` (laser): lihachev2022 < 1 % up to 800 kHz (p.4), 0.95 % (p.6). Flat actuation bandwidth 1-dB (`bw1db_khz`,
  phase_shifter): lihachev2022 nearly 20 MHz (p.6).
- Grating strength per length for free_space_emitter: zhang2025c 0.04 /mm (p.3), simulated; `kappa_per_cm` is not allowed for this class.
