# Batch lit_46 report (distill subagent, 2026-10-29)

Dry-run `batch lit_46: +27 components, +191 metrics; errors 0`. The only warning comes from another batch's merged row
(ni2025b). The files are ASCII only, with no e-mail addresses. Quotes of a few words appear only for open_license_ok
sources (nader2025, lim2026, yang2024). For every paper, the page-1 title and authors match the source row, and no
cached file is a different paper or a correction. Supplements are inline in text.md: jin2021 p.11-19, nader2025 p.13-17
and yang2024 p.13-17. Not audited or merged.

## Per paper (components / metrics)

- jin2021 (8 / 49). This source is restricted: facts and locators only.
  - Rows: three resonators (resonator.ring), one each for the 30 GHz ring, the 10 GHz racetrack and the 5 GHz racetrack.
  - 30 GHz ring:
    - Q values: Qi 220 M / QL 150 M at 1560 nm (doublet fit, ring-down check). Qi mean 260 M and std 13.5 M over 34
      modes at 1630-1650 nm. Qi 250 M for the ring used in the laser (wavelength inferred, 1556 nm).
    - Fig. S2: Q0 and QL at 8 wavelengths.
    - FSR 30 GHz (author_estimate, nominal) and finesse 42,600 (derived by the authors).
    - Geometry: radius 1 mm, width 8 um, pulley gap 5 um, 100 nm core, 14.5 um BOX, 2 um cladding.
  - 10 GHz and 5 GHz racetracks: Qi 56 M and 100 M at 1560 nm, FSR 10.8 and 5.4 GHz, width 2.8 um (5 GHz only).
  - Platform: waveguide_platform.straight, 0.001 dB/cm (printed 0.1 dB/m, inferred from Q; author_estimate).
  - Two laser.sil rows (commercial DFB self-injection-locked to the 10 GHz and 5 GHz racetracks):
    - 5 GHz: 3 Hz linewidth (derived by the authors from 0.5 Hz2/Hz) and 5.4 GHz comb rate.
    - 10 GHz: comb rates 10.873 GHz (Fig. 3(b)) and 43.2 GHz, ten comb lines > -10 dBm on-chip, pump at 1555.438 nm.
      Fundamental linewidths from Fig. 4(c): pump ~9 Hz; comb lines 3-35 Hz (extracted, +/-1 Hz).
  - Commercial DFB (laser.dfb): up to 30 mW into the bus at 1556 nm.
  - DFB-to-bus butt coupling (chip_chip_coupler.butt): typical T = -6 dB, entered as 6 dB per_interface,
    author_estimate (a model parameter of unstated origin).
  - Not entered:
    - 30 GHz SIL configuration: its only result is a 1 Hz2/Hz white noise floor. There is no parameter for that and the
      paper gives no linewidth, so this configuration has no row. The 0.8 Hz2/Hz value for the 10 GHz configuration is
      in notes.
    - Comb phase noise (-100 / -129 and -114 / -140 dBc/Hz), D2/2pi (-20.3 / -80.2 kHz), 50 dB noise suppression,
      5 ms turnkey time: no parameters.
    - 0.045 dB/m (cited from ref. 31); Table I values of other works; simulated bend-loss curves (Fig. S1).
  - Fab empty: an unnamed "high-volume CMOS foundry". Anello (org_anello) only co-designed and is acknowledged.
- nader2025 (9 / 63). Open licence.
  - Three heterogeneous InGaAs-QW / Ta2O5 DFB rows (laser.heterogeneous, platform other), one per grating period
    (148 / 150 / 152 nm):
    - 148 nm: SMSR 43 dB at 76 mA; linewidths 1.2 MHz fundamental, 2.0 MHz (1/pi) and 9.4 MHz (beta-line), all
      derived because MHz -> Hz.
    - 150 nm: SMSR > 30 dB over 70-100 mA / 6-28 C.
    - 152 nm: threshold 45 mA, 2 mW at 100 mA (20 C).
    - 150 and 152 nm: best SMSR ~38.5 dB read from Fig. 2(e).
    - All three: measured wavelength, kappa 10 cm-1 (simulated), 8 nm etch target, 1.2 mm length, 1 um Ta2O5 width,
      570 nm / 0.8 um / 1.4 um stack, and 60 GHz mode spacing (family statement; author_estimate).
  - FP laser: 40 mA threshold, > 2 mW waveguide-coupled output, 1.5 mm.
  - SOA: 24.5 dB peak on-chip gain at 987.4 nm, 8.5 nm 3-dB bandwidth, 122.5 dB/cm (from 28.2 cm-1, derived), 2 mm.
  - III-V -> Ta2O5 multistage taper (waveguide_platform.transition): 86 % simulated, with tip and taper geometry.
  - 1064 nm Ta2O5 ring: Qi 2.53e6, QL 2.35e6, Qc 3.2e7 (Fig. 4(c) labels), 2.0 um width.
  - Two edge-coupler rows, both author_estimate (origin not stated):
    - Laser-chip angled facet to the lensed fiber: 3 dB (+/- 1 dB), per_facet.
    - OPO chip: 6 dB, scope unspecified.
  - Not entered:
    - Current tuning rates in pm/mA: no parameter.
    - Tuning range > 250 GHz (Supp. prints 300 GHz): stated for the family, and no GHz tuning-range parameter.
    - kappa*L 1.2 and mirror reflectance 29 % (design).
    - "SOAs with > 21 dB gain" (conclusion, no device).
    - OPO microrings (radius 45 um, widths 930-970 nm): signal 778 / 750 / 752 nm and 183 THz span have no
      frequency_converter parameter, so no row.
    - Loop-mirror reflection vs DC length (Fig. S5(c)): a sweep, and the FP laser's own DC length is not stated.
    - > 95 % bonding yield, < 10 nm alignment.
  - Fab org_national_institute_of_standards_and_technology on the bonded-chip rows ("We fabricate", p.4; all authors at
    NIST divisions, D154). Not on the 1064 nm ring or the separate OPO chip, whose fabrication site is not stated.
- zhang2026a (1 / 37). This source is restricted.
  - One laser.soa_dfb row: monolithic InP 4-channel REC-DFB array with Y-combiner and SOA, butterfly packaged.
  - Power: > 100 mW per channel; 62 -> 100 mW with ISOA 0 -> 200 mA. Threshold 60-81 mA.
  - SMSR: > 40 / > 35 / > 40 / > 39 dB, one row per operating sweep.
  - Spectrum: 4 channel wavelengths; spacing 2.421 nm (fit); wavelength deviations < 0.072 nm (vs fit) and < 0.038 /
    0.039 / 0.039 nm (fitted vs designed); PDM < 2 dB (3 sweeps).
  - Drift 120 pm/K (derived from 0.12 nm/C). Linewidths 488-526 kHz per channel (derived kHz -> Hz). RIN < -145 dB/Hz.
  - Divergence 11.6 x 32.6 deg measured and 11.0 x 32.9 deg simulated.
  - Geometry: 4 channels, 15 um pitch, 5 um ridge, 2000 / 3500 um lengths, footprint, 256.25 nm seed period.
  - Not entered:
    - Current tuning 0.0062 / 0.0016 nm/mA (no parameter).
    - Nominal 300 GHz / 2.4 nm spacing.
    - The intro's divergence (12.3 x 31.5 deg) and p.3 simulated 9.5 x 21.8 deg, which conflict with p.11 / p.4.
    - 4.5 dB dynamic ER (external LN modulator).
    - Integrated SOA and Y-combiner as separate rows: no standalone values.
  - Fab empty (passive voice).
- lim2026 (2 / 5). Open licence.
  - SiN metalens on the backside of a surface ion trap (micro_optics.metalens, platform sin):
    - Measured point-source detection efficiency 0.58 % (scope device_total, author_estimate because isotropic emission
      is assumed).
    - Simulated collection 0.91 %.
    - BSG + metalens transmission 67 %, entered as 1.74 dB (author_estimate, origin not stated).
    - Pillar height 700 nm.
  - Design row for the 40 x 600 um aperture: 3.17 % simulated.
  - Fab org_university_washington ("We design, fabricate, and test", p.1; all authors UW).
  - Not entered: PSF FWHM 0.95 / 1.31 um vs 0.92 um simulated (no focal-spot parameter); pillar period 250 nm (gap
    already reported in lit_34); trap frequencies; source divergence and acceptance angle (setup).
- yang2024 (1 / 11). Open licence, cc-by-nc-nd.
  - Free-space SOS metasurface PBS (polarization.pbs, platform other).
  - PER: measured 26.6 dB (x) and 12 dB (y), confirmed against a 250 dpi render of p.5 because the text-layer
    subscripts are garbled. Simulated 16.7 / 22.6 dB.
  - IL 4.81 dB per port (from 33 %) and 2.29 dB total (from 59 %), both derived.
  - Geometry: Si 500 nm design and 494.0 nm measured at center (ellipsometry); ~10 nm under-etch pedestal; sidewall
    83 deg (from a 7 deg taper, derived); 1 mm2 array.
  - Not entered: Table S1 balanced-point port fractions and the Table S2 non-ideal-geometry simulations (in notes or
    omitted); magnetometer sensitivity (system).
  - Fab empty. Facility CNM is missing from the registry (below).
- zhang2025b (6 / 26). This source is restricted.
  - Four-directional circular 64-element Si3N4 OPA at 632.5 nm (free_space_emitter.other):
    - SLSR 4.85 dB measured, 5.72 dB simulated.
    - Steering 9 deg elevation / 360 deg azimuth at SLSR >= 3 dB.
    - Main lobe 0.15 x 0.15 deg.
  - Arrowhead grating antenna (free_space_emitter.grating_emitter, simulated only): 8 deg emission angle, 21 deg FWHM,
    420 nm period, fill 0.5, footprint.
  - Grating coupler: 11 dB, scope unspecified.
  - 1x2 MMI: 0.1 dB excess, per_component.
  - Straight waveguide: 6 dB/cm, 1 um width, 300 nm core, 3 um BOX.
  - Folded thermo-optic phase shifter: P_pi 23 mW measured on an MZI test structure (24 mW simulated); response time
    18.74 us entered as rise_time_us with "definition not stated"; heater ~514 ohm.
  - Not entered: residual energy 10.8 % -> 3.8 % (simulated, no parameter); the 128-element simulation; the
    conventional-heater 70 mW simulation (in notes).
  - Fab empty.

## Missing orgs

- Washington Nanofabrication Facility, University of Washington, Seattle, US (lim2026 p.4-5 acknowledgments: "a portion
  of this work was carried out at").
- Molecular Analysis Facility, University of Washington, Seattle, US (lim2026 p.5, same sentence).
- Center for Nanoscale Materials, Argonne National Laboratory, Lemont, US (yang2024 p.9 acknowledgments: PBS
  nanofabrication performed there). Argonne National Laboratory itself is also absent (yang2024 p.1 affiliation 2).
- University of Wisconsin-Madison (yang2024 p.1 affiliation 1): no component role.
- Yongjiang Laboratory, Ningbo, CN (zhang2026a p.1 affiliation 1): no component role.

## Judgment calls for the audit

1. jin2021 q_intrinsic from the doublet-lineshape fit is `measured` (standard fit of own data; the ring is designed
   under-coupled). The fit is not a Q_L + extinction computation with an assumed regime, so D403 is not applied.
   Please confirm.
2. jin2021 laser structure:
   - Each resonator configuration is one laser.sil row. Its Kerr-comb operating states are conditions on that row
     (rule 9 within class laser) rather than separate laser.comb rows.
   - The 43.2 GHz comb ("resonator with 10.8 GHz FSR") is assumed to be the 10 GHz racetrack design.
   - The commercial DFB and the DFB-to-bus butt interface get their own rows.
3. jin2021 platform loss: 0.1 dB/m is put on a platform waveguide row (author_estimate). The paper does not name the
   resonator it was inferred from (D159 analogue: kept off the ring row).
4. nader2025 family-level statements:
   - The 60 GHz mode spacing and the design values (kappa, etch depth, length, stack) are entered on all three DFB rows.
   - The > 250 GHz tuning range and the pm/mA tuning rates are not entered. The main text prints 26.5 / 16.6 /
     24.0 pm/mA; the supplement text prints 26.6 / 16.6 / 24.6. The Fig. S4(b) bar for 998 nm reads ~24.0.
5. nader2025 edge-coupler losses are `author_estimate`: the paper states them as setup facts without saying how they
   were obtained. D167 would instead give `measured` for a directly stated per-facet loss.
6. lim2026 detection efficiency is `author_estimate`: isotropic emission is an assumed input to the conversion. An audit
   could argue for `measured`.
7. yang2024 classed polarization.pbs (free-space metasurface), not micro_optics.metalens, because the function is
   polarization splitting and per_db is allowed there. In scope as a chip-scale nanophotonic element (D411)?
8. zhang2026a: one laser.soa_dfb row for the whole array, with per-channel values as conditions. Power values are
   ref_plane unspecified because the paper does not say whether they were measured at the chip or the packaged module.
9. zhang2025b arrowhead antenna is kept as a fabricated row with only simulated performance (70 merged precedents).
   The 18.74 us "response time" is in rise_time_us with the definition flagged.

## Registry gaps

- `frequency_noise_hz2_per_hz` (laser): white (fundamental) frequency-noise floor, single-sideband, as reported.
  - jin2021: 1 / 0.8 / 0.5 Hz2/Hz (Fig. 2(b) caption, p.3).
  - nader2025: 4e5 Hz2/Hz (p.6).
  - With it, the 30 GHz SIL configuration could get a row.
- `current_tuning_pm_per_ma` (laser): lasing-wavelength shift per mA of injection current.
  - nader2025: 26.5 / 16.6 / 24.0 pm/mA (p.5, Supp. p.15).
  - zhang2026a: 6.2 and 1.6 pm/mA (p.7, p.8).
  - fm_efficiency_ghz_per_ma would need a wavelength-dependent conversion.
- `tuning_range_ghz` (laser): mode-hop-free tuning range in frequency. nader2025 > 250 GHz (p.5) / 300 GHz (Supp. p.15).
- `phase_noise_dbc_per_hz` (laser, comb repetition-rate beat note at a stated offset, offset in condition). jin2021
  -100 / -129 dBc/Hz (10.8 GHz) and -114 / -140 dBc/Hz (5.4 GHz) at 10 / 100 kHz (p.5).
- `gvd_d2_khz` (resonator): integrated-dispersion D2/2pi. jin2021 -20.3 / -80.2 kHz (p.4). D81 rejected beta2; this is
  the resonator-normalized form.
- Frequency-converter OPO outputs (`signal_wavelength_nm`, `span_thz`): nader2025 778 / 750 nm signals and 183 THz span
  (p.7-9).
- `focal_spot_fwhm_um` (micro_optics): measured PSF FWHM at the focal plane. lim2026 0.95 / 1.31 um (p.3).
- `subwavelength_period_nm` for micro_optics and polarization (metasurface lattice): lim2026 250 nm, yang2024 400 nm.
  This repeats the lit_34 gap.
