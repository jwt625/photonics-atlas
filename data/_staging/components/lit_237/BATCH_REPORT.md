# lit_237 batch report

Distilled 2026-11-20. Papers: lit:barbarin2006, lit:hirano2020, lit:zhang2022f, lit:xie2018. Page-1 titles match the
source rows; no garbled text layers. Totals: 14 components, 106 metric rows. Dry-run merge
(`merge_component_staging.py data/_staging/components/lit_237 --dry-run`): +14 / +106, 0 errors (the one warning,
cmp_lit_ni2025b_pimmwc-m18, is a merged row outside this batch).

No paper names a fabricating org or a shared facility: fab_org_ids and facility_org_ids are empty on all 14 rows
(D80b), so no missing orgs are reported.

## lit:barbarin2006 (2 components, 23 metrics)

- `cmp_lit_barbarin2006_ring_mll_sa40` (laser.comb, inp; 19): repetition rate 14.7 GHz (Table 1) and 14.698-14.760 GHz
  range (Fig. 9 read); timing jitter 1.46 / 7.06 / 3.18 / 3.32 ps over the four Table 1 integration ranges (as fs,
  derived); thresholds 338 mA (-0.8 V), 347 mA (-2.5 V), 340 mA (-2.0 V); relaxation oscillation ~1 GHz; mode
  linewidth ~600 MHz typical; center wavelength ~1530 nm; output power ~0.047 mW per arm (Fig. 5(d) read, chip
  plane); geometry: ring length 5291 um, SA 40 um, ridge 2 um, minimum bend radius 500 um, 120 nm Q1.55 active layer,
  1.5 um p-InP.
- `cmp_lit_barbarin2006_output_dc` (splitter.directional_coupler, inp; 4): design output coupling ~35 %
  (author_estimate), 200 um length, 0.9 um gap, 2 um ridge.
- Not entered: optical spectrum FWHM 4 nm typical, <= 3.5 nm at -2.3 V, up to 4.0 nm (40 um SA) and 4.5 nm (50 um
  SA) (laser spectral width: registry gap, D695); RF linewidth 2.8 MHz at -20 dB / < 400 kHz at -3 dB, -20 dB widths
  2.5-5.5 MHz (MLL RF linewidth: registry candidate, D695); repetition-rate tuning range 60 MHz as its own number
  (no parameter; the Fig. 9 range row carries it); modelocking window 355-410 mA / 3.3-4.9 kA/cm2 at 0.9-2.2 V (no
  parameter; threshold current density candidate, D695); RF peak 50 dB over noise floor / 33 dB over low-frequency
  content; confinement factor 0.28; 200 kOhm contact isolation; transform-limit estimate 700 fs (calculation);
  facet angle 7 deg (D250 rejected).
- Pulse widths not entered (D159): "5-8 ps" autocorrelation, 7.5 ps after a 1 nm filter, just over 4 ps after 8 m
  SMF (p.9) are not tied to a device; the only trace (Fig. 8) is the 50 um SA device. Kept in the component notes.
- The 50 um SA device has no row: its only device-specific number (4.5 nm FWHM) has no laser parameter.

## lit:hirano2020 (2 components, 10 metrics)

- `cmp_lit_hirano2020_eo_polymer_opa_8ch` (free_space_emitter.other, polymer; 4): 8 channels, 4.5 um emission pitch,
  main-lobe divergence 3.9 deg measured and 3.8 deg theoretical.
- `cmp_lit_hirano2020_eo_polymer_phase_shifter` (phase_shifter.other, polymer; 6): Vpi 12.05-13.4 V across the eight
  channels at 3 kHz (Fig. 2 read, extracted_from_figure); total power of the eight phase shifters 0.38 mW during
  500 kHz scanning (author_estimate, origin not stated); core 1.5 x 1.5 um, upper / lower cladding 1.0 / 2.5 um.
- No wavelength is stated anywhere in the paper: band `unspecified` with a note on every spectral row.
- Not entered: 2 MHz / 500 kHz beam-scanning rates (no scan-rate parameter for free_space_emitter: registry gap,
  proposed `scan_rate_khz`, "beam-scanning repetition frequency demonstrated", p.7 Fig. 4); main-lobe to
  grating-lobe angle 19.1 deg (no parameter); 1x8 MMI (160 um x 3.3 mm) geometry only (rule 9); Vpi values below
  2 kHz (transient regime; notes).
- EO-atlas candidate: EO-polymer phase shifter (10.1109/JPHOT.2020.2981743).

## lit:zhang2022f (7 components, 45 metrics)

- `cmp_lit_zhang2022f_opa_1x256` (free_space_emitter.other, si_sin_multilayer; 14): 256 ch, 2 um pitch; steering
  45.6 deg (theta, 1550 nm) and 16.12 deg (phi, 1510-1630 nm); 0.1343 deg/nm; SLSR > 10.8 dB; FWHM 0.154 x 0.0435
  deg measured, 0.154 x 0.027 deg simulated; device_total loss ~16 dB (main lobe -16 dBm for 0 dBm launched,
  derived); aperture 500 x 3000 um; footprint 4 x 16 mm.
- `cmp_lit_zhang2022f_sin_assisted_grating` (free_space_emitter.grating_emitter, si_sin_multilayer; 8): simulated
  upward emission efficiency ~47 %; period 610 nm, duty cycle 0.418, Si 1 um x 220 nm, 30 nm Si3N4 etch, 3 um BOX,
  3 mm length.
- `cmp_lit_zhang2022f_sin_edge_coupler` (fiber_chip_coupler.edge, sin; 1): 1.4 dB per_coupler.
- `cmp_lit_zhang2022f_sin_mmi_tree_1x256` (splitter.other, sin; 2): 1.4 dB excess, device_total; 256 outputs.
- `cmp_lit_zhang2022f_routing_waveguides` (waveguide_platform.other, platform empty; 1): 2.2 dB device_total.
- `cmp_lit_zhang2022f_sin_si_vertical_transition` (waveguide_platform.transition, si_sin_multilayer; 9): 0.2 dB;
  130 um taper, Si3N4 1 um -> 250 nm, Si 130 -> 500 nm, 250 nm gap, 220 / 400 nm layers.
- `cmp_lit_zhang2022f_folded_to_phase_shifter` (phase_shifter.thermo_optic, soi; 10): P_pi ~4.5 mW, MZI ER > 16.6
  dB, rise / fall 19.8 / 20.8 us, 17.7 kHz (derived, 0.35 / rise), TiN heater 120 nm x 8 um x 250 um, 2 um above Si.
- Not entered: grating emission rate 13.9 dB/cm at 1550 nm, ~15.1 dB/cm average, Fig. 4 slopes 13.49-16.76 dB/cm
  (1500-1620 nm), simulated ~15 dB/cm (no emission-rate parameter for free_space_emitter: registry gap, proposed
  `emission_rate_db_per_cm`, "decay of guided power along a grating antenna by emission", p.3-4 Fig. 4, cutback);
  main lobe ~40 % of emitted power (no parameter); Fig. 6(b) theta-cut side-lobe 11.5 dB label (the text's > 10.8 dB
  entered); > 8.5 mm needed for 95 % radiation (simulation of an unbuilt length); Fig. 5(e) emission angles (only
  the span is printed; not read).

## lit:xie2018 (3 components, 28 metrics)

- `cmp_lit_xie2018_iii_v_si_phase_shifter` (phase_shifter.other, other; 9): 2 pi at 0.9 V reverse bias (phase_shift_pi
  with the voltage in bias_v / condition, D451), MZI ER > 23 dB, bias-induced loss 0.15 dB per 2 pi, power < 3 nW
  (author_estimate), bandwidth > 1 GHz (author_estimate); ~5 mm length, 2 um mesa, 500 nm SOI, 231 nm etch.
- `cmp_lit_xie2018_opa_32ch` (free_space_emitter.other, other; 16): 32 ch, 4 um pitch, SLSR 16 dB after focusing,
  steering ~22 deg (psi), 8 deg (1520-1580 nm) and 28 deg (1450-1650 nm) theta, 0.138 deg/nm, FWHM 0.02 x 0.78 deg;
  grating 560 nm period, duty 0.5, 14 nm etch, 800 nm wide, 10 mm; SOI 500 nm / 231 nm rib etch.
- `cmp_lit_xie2018_opa_240ch` (free_space_emitter.other, other; 3): 240 ch, 4 um pitch, 0.1 deg psi beam width as
  author_estimate.
- Not entered: dark current < 3 nA at -2 V (no phase-shifter dark-current parameter); operation over 1450-1650 nm (no
  parameter); "about -1 V for C-band" operating voltage (abstract wording of the 0.9 V result; notes); 1xN star
  coupler and the test-MZI 2x2 MMIs (no values).
- EO-atlas candidate: III-V/Si QW phase shifter (10.1109/ACP.2018.8596249).

## Judgment calls for the auditor

1. barbarin2006: Fig. 5 values (thresholds 338 / 347 mA, output power) attached to the 40 um SA device via the p.7
   sentence linking Fig. 5 to the Labs = 40 um animation; the Fig. 5 caption itself names no SA length. Design text
   says SA lengths 30 or 60 um while all captions say 40 / 50 um (captions used, conflict noted).
2. barbarin2006: pulse widths (5-8 ps, 7.5 ps filtered, ~4 ps compressed) left out under D159 rather than put on the
   40 um row.
3. barbarin2006: Fig. 5(d) bias conflict (text -1.8 V, plot title and caption -2.0 V); -2.0 V used on the power row.
4. hirano2020: array total 0.38 mW stored as `tuning_power_mw` on the phase-shifter row (condition: total of eight)
   because free_space_emitter has no power parameter (D558 gap); alternative is to drop it to notes.
5. hirano2020 / xie2018: electro-optic phase-shifter values (Vpi, 2 pi voltage, bandwidth) kept here (not EO-atlas
   sources; D582 / D589 / D600); both listed as EO-atlas candidates.
6. xie2018: 0.15 dB bias-induced loss as `insertion_loss_db` per_component, basis derived (authors' difference of two
   transmission peaks, D80a), with the passive loss in `excludes`; > 1 GHz bandwidth and < 3 nW as author_estimate
   (no measurement shown).
7. xie2018: OPA rows platform `other` (heterogeneous III-V/Si phase shifters in the optical path), grating geometry on
   the 32-channel OPA row instead of a geometry-only grating row.
8. zhang2022f: the four p.3 loss terms kept `measured` (the paper says "measured to be") with method unspecified and
   C band inferred; the 2.2 dB routing row has an empty platform (layer not stated); the 1.4 dB splitter value as
   excess_loss_db device_total.
9. zhang2022f: 17.7 kHz "operation speed" as bw3db_khz derived (reproduces 0.35 / 19.8 us; espinola2003 precedent).

## Registry gaps

- free_space_emitter `emission_rate_db_per_cm` (zhang2022f 13.9 dB/cm at 1550 nm, p.4 Sec. IV / p.3 Fig. 4).
- free_space_emitter scan rate (hirano2020 2 MHz, p.7 Fig. 4) and power consumption (hirano2020 0.38 mW; D558).
- free_space_emitter main-lobe power fraction (zhang2022f ~40 %, p.4).
- laser spectral FWHM (barbarin2006 4.0 / 4.5 nm, p.8 / p.12), MLL RF linewidth (barbarin2006 < 400 kHz at -3 dB,
  p.5), repetition-rate tuning range (60 MHz, p.9), current density (3.3-4.9 kA/cm2 over the modelocking window,
  p.5; the threshold-current-density candidate of D695 would not cover a window): recurring (D695).
- phase_shifter dark / leakage current (xie2018 < 3 nA at -2 V, p.2).
