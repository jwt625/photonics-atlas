# lit_300 batch report

Distilled 2026-11-27. Papers: lit:riemensberger2020, lit:kim2020, lit:yoon2023, lit:yi2015, lit:liang2021.
Result: 16 components, 92 metric rows. `merge_component_staging.py data/_staging/components/lit_300 --dry-run`:
0 errors (2 warnings, both on merged rows of other batches). Page-1 titles match the source rows; no cached file is
a correction / erratum. Helper script: the batch scratch folder (`build.py`).

## lit:riemensberger2020 (arXiv v1 1912.11374 of the Nature 2020 paper)

Values from the preprint only (journal version not read; noted on every component). Preprint title "... using soliton
microcombs" vs registry "... using a soliton microcomb" (same work, D430 / D433).

Components 2 / metrics 13:
- `cmp_lit_riemensberger2020_ring_99ghz` (resonator.ring, sin, 7 rows): radius 228.39 um (design), width 1500 /
  height 820 nm (derived), D1/2pi 98.9 GHz, kappa_0/2pi 15 MHz, kappa_ex/2pi 80 MHz (p.3) and 100 MHz (p.9).
- `cmp_lit_riemensberger2020_soliton_comb_99ghz` (laser.comb, sin, 6 rows): 99 GHz repetition rate, pulse widths
  58 / 45 fs at detunings 1.2 / 2.9 GHz, 30 LIDAR channels, > 90 channels with < 3 dB power change, FM-transduction
  3-dB cutoff > 40 MHz.

Fab `org_epfl` + facility `org_center_of_micronanotechnology`: p.7 author contributions "J.L fabricated the samples in
the CMi" (D83c; liu2018a precedent). process_name "photonic Damascene process (ref. 41)".

Not entered: D2/2pi 1.13 MHz, D3/2pi 576 Hz (dispersion, D81); Raman self-frequency shift 2 THz; soliton existence
range; excursion slope 22.15 MHz per line; chirp nonlinearity < 1/500; 1.6e17 Hz2 chirp rate; ranging precision and
3 Mpixel/s (system level); simulated repetition-rate mismatch 20.6 MHz per 1.7 GHz (LLE simulation, no parameter);
double-inverse-taper coupler (no value, no row); pump setup (ECDL, SSB, EDFA 1.7 W; rule 13).

Judgment calls:
- kappa_ex printed 80 MHz (p.3) and 100 MHz (p.9) for the same device: both entered with conflict notes (D417).
- Radius: Methods 228.39 um entered; Fig. 1(c) caption labels 228.43 um (note).
- D1/2pi and all kappas `author_estimate`: no extraction / dispersion method is described in this paper (D76, D403).
  liu2018a entered its D1 as measured because that paper states a comb-calibrated fit.
- Pulse widths `author_estimate`: method and width definition not stated (ji2024 precedent), not D84c `derived`.
- FM transduction cutoff stored as `bw3db_ghz` (laser "3-dB electrical / modulation bandwidth"), 0.04 GHz `gt`,
  `derived` (MHz -> GHz). It is a frequency-modulation transfer bandwidth, not intensity modulation; an auditor may
  prefer to drop it.

## lit:kim2020 (Optics Express 2020, polymer OPA thermo-optic phase modulators)

Components 4 / metrics 22:
- `cmp_lit_kim2020_polymer_waveguide` (waveguide_platform.straight, polymer, test_structure, 5 rows): 0.3 dB/cm,
  0.9 dB fiber-to-fiber of the 11 mm waveguide, 4.0 x 3.0 um core, 11 mm length.
- `cmp_lit_kim2020_facet_coupler` (fiber_chip_coupler.edge, polymer, 3 rows): 0.3 dB/facet to UHNA3, design MFD
  4.8 x 4.1 um.
- `cmp_lit_kim2020_topm` (phase_shifter.thermo_optic, polymer, 9 rows): P_pi 2.5 mW measured / 2.1 mW simulated,
  45 ohm, heater 10 um x 2 mm, rise 12.7 ms / fall 13.4 ms, 37.9 Hz bandwidth, 4.2 ms time constant.
- `cmp_lit_kim2020_opa_16ch` (free_space_emitter.other, polymer, 5 rows): 16 channels, 12 um pitch, main-to-side-lobe
  4.8 dB measured / 3.5 dB design, 5.2 dB main-beam loss (12 dBm in, 6.8 dBm out, derived).

Fab empty: "We designed and fabricated" covers authors at three orgs (Pusan National University, Kwangwoon University,
Agency for Defense Development), site not stated (D154 / D395). Facility empty (acknowledgment thanks individuals for
discussions only). ChemOptics Co. polymers: supplier note only (D428).

Not entered: 1x16 splitter and S-bends (no values); side-lobe angle 7.0 deg measured / 7.2 deg design (no parameter);
BPM crosstalk < -25 dB at 12 um pitch (simulated; crosstalk_db not allowed on free_space_emitter); Cr-Au heater
"10-100 nm" (layer split unclear); Table 1 multi-pole transfer functions and the slow viscoelastic drift (no
parameter); beam scanning shown without printed angles.

Judgment calls:
- Index assignment printed both ways on p.2 (core 1.397 / cladding 1.372 in the design paragraph, reversed in the
  fabrication paragraph): core 1.397 recorded, conflict in notes.
- 0.3 dB/cm and 0.3 dB/facet are a split of one 0.9 dB measurement without a stated method: `author_estimate`
  (`loss_breakdown`); the 0.9 dB total stays `measured`, fiber_to_fiber (D83a).
- Bandwidth / time constant from a single-pole asymptote of measured data: `derived` (model + Hz -> kHz, ms -> us).
  Fig. 7 caption puts the primary pole near 116 Hz (Table 1: 729.6 rad/s), inconsistent with 37.9 Hz / 4.2 ms;
  conflict note (D417).
- 45 ohm heater resistance `author_estimate` (stated, not stated as measured; zhou2023b precedent).
- OPA loss includes the packaged cylindrical lens and 45 deg mirror (in `includes`); kept because the lens acts only
  on the vertical axis and no divergence value from the lens path was entered (D558 concerns divergence).

## lit:yoon2023 (Optics Express 2023, 1x64 Si OPA with tunable radiator, ToF LiDAR)

Components 5 / metrics 21:
- `cmp_lit_yoon2023_opa_1x64` (free_space_emitter.other, soi, 10 rows): 64 channels, 2 um pitch, transversal span
  20.4 deg of the imaging phase sets and longitudinal span 9.2 deg (both derived from printed angles), divergence
  0.7 / 0.6 deg measured (mean) and 0.45 / 0.19 deg calculated, SLSR about 10.36 dB (mean), 38.6 dB loss budget.
- `cmp_lit_yoon2023_tunable_radiator` (free_space_emitter.grating_emitter, 4 rows): 11 dB budget term, 4.6 deg
  thermo-optic-only longitudinal steering at 6.5 W, 1 um width, 300 um aperture.
- `cmp_lit_yoon2023_input_gc` (fiber_chip_coupler.grating, 2 rows): 6.8 dB with epoxy-bonded fiber, angle optimized
  for 1525 nm.
- `cmp_lit_yoon2023_mmi_tree_1x64` (splitter.mmi, 3 rows): 3.6 dB excess (six stages), 1 in / 64 out.
- `cmp_lit_yoon2023_pin_phase_shifter` (phase_shifter.other, 2 rows): 4.2 dB budget term, 1.51-18 mW maximum power per
  phase shifter over 64 channels.

Fab empty: "manufactured using a CMOS-compatible process on an 8-inch silicon-on-insulator wafer" (p.4), passive, no
org (D80b / D433); process_name empty (generic wording).

Not entered: 45 deg / 10 deg steering ranges (abstract, p.4) and +/-22.5 deg credited to the authors' refs. [22,26]
(rule 3, D259); radiator tuning speed about 1 us (ref. [25]); footprint printed "5 um x 5 um" (inconsistent with a
64 x 2 um array of 300 um radiators; D159); main-beam share 6.9 % (-11.6 dB) of radiated power; radiator 0.67 deg/W,
about 0.1 W per channel, 3.6 W / 6.5 W totals (registry gaps below); 1 dB waveguide and 12 dB side-lobe /
grating-order terms (in `includes` of the OPA total only, zhou2023b precedent); pulse generator, laser diode, EDFA,
APD (setup, rule 13); 2 cm ranging accuracy and 1.63 m maximum distance (system level).

Judgment calls:
- All loss values are budget terms with no stated origin: `author_estimate`, `loss_breakdown`; band `cl_band`
  inferred from the 1525 / 1570 nm operating wavelengths (zhou2023b precedent).
- The p-i-n phase shifter is a carrier-injection (electro-optic) element with no Vpi / bandwidth: `phase_shifter.other`
  (poulton2019 / D582), not an EO-atlas row.
- Steering spans are the angles actually set in this paper (imaging subset), `derived` from the printed end points;
  the conditions say they are not the full range.

## lit:yi2015 (Optica 2015, silica wedge soliton microcomb)

Components 2 / metrics 11:
- `cmp_lit_yi2015_wedge_disk_3mm` (resonator.disk, silica, 3 rows): radius 1500 um (from 3 mm diameter, derived),
  D1/2pi 21.92 GHz (fit of measured mode frequencies), intrinsic Q near 4e8 (`author_estimate`, D403).
- `cmp_lit_yi2015_soliton_comb_22ghz` (laser.comb, silica, 8 rows): repetition rates 21.92 / 22.01 GHz (two of three
  devices), pulse width 130 fs (sech2 spectral fit, derived), 250 fs (FROG / autocorrelation, preamp-limited),
  123-187 fs over the locked detunings (derived), parametric threshold about 2.5 mW (typical), soliton output
  0.32-0.54 mW and efficiency 0.28-0.67 % (read off Fig. 3(a) / 3(c) on a PDF render).

Fab empty: "were fabricated using float-zone silicon wafers [39]" (passive). Facility empty: Kavli Nanoscience
Institute appears only in the funding list / funding acknowledgment (D83e; yang2018a precedent).

Not entered: phase noise -100 dBc/Hz at 10 kHz offset (referenced to 10 GHz; no parameter, registry gap below);
D2/2pi 17 kHz (dispersion); Aeff about 60 um2; eta 0.29 loading; minimum pump power for soliton existence
(Fig. 3(c), about 190-48 mW; not a parametric threshold, no parameter); power per comb line about 7 uW (no
parameter); Raman time constant 2.4 fs; 24 h locked operation; Fig. 5 design contours (model only).

Judgment calls:
- Fig. 2 devices are three resonators "close in size and shape": one design row, values per device in conditions.
- Figure reads: Fig. 3(a) end points 0.32 / 0.54 mW (+/- 0.01 mW); Fig. 3(c) log axis end points 0.28 / 0.67 %
  (+/- 0.02 percentage points); stored as ranges, `extracted_from_figure`.

## lit:liang2021 (Optica 2021 memorandum, heterogeneous QD DFB laser on Si)

Components 3 / metrics 25:
- `cmp_lit_liang2021_qd_dfb` (laser.heterogeneous, other, 21 rows): threshold 6.7 mA, > 7 mW in the Si waveguide at
  50 mA and 2 mW at 60 C, WPE 9.4 %, SMSR 61 dB best / >= 40 dB (20 C) / >= 35 dB (60 C), lasing near 1297 nm and
  1297.8 nm (22 C, 68 mA), 68 pm/K, 10.1-11.6 pm/mW, Lorentzian linewidth 211-273 kHz, kappa about 150 /cm (design),
  grating period 197 nm, duty 0.5, 10 nm corrugation, 170 nm rib etch, 1.25 um x 300 nm Si rib, 4 um mesa, 800 um
  length.
- `cmp_lit_liang2021_iii_v_si_taper` (waveguide_platform.transition, other, 2 rows): < 0.4 dB, 26 um.
- `cmp_lit_liang2021_output_gc` (fiber_chip_coupler.grating, soi, 2 rows): 7.5 dB, about 15 dB back-reflection.

Fab empty: no fabrication statement naming the authors or an org; all authors Hewlett Packard Labs / HPE (D80b,
cheung2022 precedent).

Not entered: threshold current density 134 A/cm2 and CW lasing to 70 C (registry gaps); 60 % confinement; alpha_H
about 0.9; 12.5 Gb/s direct modulation with 4.3 dB ER (no laser ER / data-rate parameter); transmitter RIN
-125 dBc/Hz referred to OMA (link value with the modulator); MOSCAP wavelength blue shift (no value); taper
reflection about -38 dB (back_reflection_db not allowed for waveguide_platform). EO-atlas candidate (rule 2, not
entered): heterogeneous MOSCAP microring modulator on a separate wafer, R 10 um, 25 Gb/s PRBS15 at 1297.8 nm,
ER 5.8 dB, VDC 3 V / Vpp 4 V, chip reflection from two GCs -20 dB (p.2).

Judgment calls:
- On-chip output power and WPE rest on the 7.5 dB GC loss of unstated origin: `author_estimate`.
- 2 mW at 60 C: reference plane and current not restated, `ref_plane unspecified`.
- 10.1-11.6 pm/mW kept as printed in `tuning_efficiency_pm_per_mw` (D80j self-heating); the power quantity (electrical
  input or dissipated) is not stated (condition says so).
- Mesa width 4 um `design_target` (stated with the SEM image, not stated as measured from it).

## Missing fab / facility orgs

None needed: every fab / facility used is in the registry (`org_epfl`, `org_center_of_micronanotechnology`). No row
waits on a new org.

## Registry gaps (skipped value + locator + proposed definition)

- `steering_efficiency_deg_per_w` (free_space_emitter): yoon2023 0.67 deg/W average radiator tuning efficiency (p.4);
  "emission-angle change per W of tuning power".
- `power_consumption_w` on free_space_emitter (D558 / D703 candidate): yoon2023 about 0.1 W maximum per radiator
  channel, 3.6 W for 2.3 deg and 6.5 W for 4.6 deg (p.4).
- Main-beam fraction of radiated power (free_space_emitter): yoon2023 6.9 % / -11.6 dB (p.4); "share of the total
  radiated power in the main lobe, side lobes and grating orders included in the denominator".
- `threshold_current_density_a_per_cm2` (laser; D431 / D433 candidate): liang2021 134 A/cm2 (p.1, Table 1).
- `max_operating_temperature_k` (laser): liang2021 CW lasing to 70 C (p.1).
- `back_reflection_db` on waveguide_platform: liang2021 III-V/Si taper about -38 dB (p.1).
- Laser / comb phase noise (dBc/Hz at an offset, carrier in condition): yi2015 -100 dBc/Hz at 10 kHz, referenced to
  10 GHz (p.2).
- Minimum pump power for soliton existence (laser.comb): yi2015 Fig. 3(c), about 190-48 mW (p.5).
