# lit_252 batch report

Papers: lit:dasmahapatra2014, lit:zhang2019g, lit:tanaka2009a, lit:chen2015b, lit:guerber2017. Page-1 titles match
the source rows; no garbled text layer. verified_on 2026-11-22. Dry run: +21 components, +133 metrics, 0 errors,
no warnings on batch rows.

## Components / metric rows

| paper | component | class | metrics |
|---|---|---|---|
| dasmahapatra2014 | crosspoint_8x4 | switch_fabric.other | 6 (8 in / 4 out, 14.0 dB fiber-to-fiber fit intercept, 14.5-22 dB path losses from Fig. 7, extinction 19.5-23.4 dB over 28 paths, 3-dB 75 GHz worst path) |
| dasmahapatra2014 | switch_element | switch_fabric.other | 9 (off-state 0.9 dB, on-state 2.0 dB, Vpi 6.9 V, Ppi 120 mW, rise 17 / fall 4 us, heater 330 x 3 um, footprint) |
| dasmahapatra2014 | fifth_order_ring | resonator.coupled_rings | 17 (tuning 11.8 / 7.4 / 13.3 pm/mW, FSR 350 GHz design / 2.84 nm model, kappa 90 / 60 / 35 %, geometry) |
| dasmahapatra2014 | soi_wire | waveguide_platform.straight | 1 (2.6 dB/cm, origin not stated) |
| zhang2019g | awgr_8x8 | wdm.awg | 8 (IL 1.8 / ~2.8 dB central / side input, crosstalk 13 dB, 200 GHz and 1.6 THz design, footprint, ports) |
| zhang2019g | awgr_16x16 | wdm.awg | 5 (IL 5 dB, crosstalk 10 dB, footprint, ports) |
| zhang2019g | awgr_32x32 | wdm.awg | 5 (IL 2 dB, crosstalk 10 dB, footprint, ports) |
| zhang2019g | microdisk_thermal | resonator.disk | 5 (380 pm/mW, 65 mW per FSR, FSR 24.8 nm, +/-1 nm spread over 9 disks, radius < 5 um) |
| tanaka2009a | soa_gate_switch | switch_fabric.other | 10 (ON-OFF > 70 dB, > 51.4 dB, crosstalk > 44.4 dB derived, gain deviation 1.2 / 2.7 / 3.0 dB, PDG 0.2-2.5 dB, 8:1, footprint) |
| tanaka2009a | switch_amplifier | amplifier.soa | 2 (fiber-to-fiber gain > 14.3 dB, total NF 8.6-9.4 dB) |
| tanaka2009a | soa_gate_800um | amplifier.soa | 9 (gain > 10 dB and NF < 6.4 dB over 1490-1570 nm, >= 80 nm span, Psat +15.6 dBm, chip NF ~4.5 dB and G 16 dB estimates, length, mesa, MQW thickness) |
| tanaka2009a | ffc_8to1 | splitter.other | 7 (imbalance 1.0 dB, L_c 14-16 dB estimate, 250 um, W1 1.6 um, 8:1, 200 nm core) |
| tanaka2009a | ssc_fiber_coupling | fiber_chip_coupler.edge | 1 (1.6 dB per facet incl. lens-module isolator) |
| chen2015b | demux_18ch | wdm.awg | 7 (excess ~8 dB, crosstalk 15-18 dB, non-uniformity ~2 dB, 1.6 nm offset, 18 ch, footprint, MZI-AWG misalignment < 0.5 nm) |
| chen2015b | bidir_awg_10x10 | wdm.awg | 12 (excess ~6 dB measured, ~1.5 dB edge-input estimate, design geometry) |
| chen2015b | mzi_interleaver | wdm.interleaver | 5 (FSR ~3.2 nm, excess ~1.0 dB standalone / ~2 dB in demux, cross-port ER > 30 dB, dL 189.5 um) |
| chen2015b | mmi_2x2 | splitter.mmi | 3 (simulated ~0.7 dB for two MMIs in a symmetric MZI, 2.4 x 6.3 um) |
| chen2015b | regular_awg_14ch | wdm.awg | 5 (Table I: excess ~6 dB, crosstalk ~10 dB, 200 GHz, 14 ch, footprint) |
| chen2015b | soi_nanowire | waveguide_platform.straight | 4 (1.9-5 dB/cm spiral cutback, 15 um min bend, 460 x 220 nm) |
| guerber2017 | awg_standard | wdm.awg | 8 (channel IL 1.91-2.29 dB, non-uniformity 0.38 dB, crosstalk > 36 dB, 4 ch, 20 nm design, 52 arms, order 5, < 1 mm2) |
| guerber2017 | awg_flattened | wdm.awg | 4 (1-dB bandwidth 9.2 nm TE / 9.0 nm TM, 4 ch, 20 nm design) |

## Values not entered and why

- dasmahapatra2014: grating-coupler loss 2 x 6.0 dB / 12 dB (foundry specification, refs. 27-28: cited); MMI crossing
  ~0.1 dB (ref. 9: cited), so no crossing or GC rows (geometry only: crossing 32 x 3 um2); 20 K temperature rise for pi
  (ref. 9); 122 / 69 K model temperatures (Table III model, no parameter); power penalty < 1.0 dB (Table V, no
  parameter); abstract "100-GHz passbands" (operating window, not a printed 3-dB width); on / off bias statistics
  (Fig. 5, no parameter); 400 Ohm heater resistance and bus pitches 300 / 250 um (not allowed on switch_fabric, see gaps);
  fiber-chip-fiber "of order -17 dB" in Fig. 4 (rounded, superseded by Fig. 7 values).
- zhang2019g: SiN-to-SiN chip-to-interposer evanescent coupler, minimum 0.41 dB and 3-dB tolerance ~+/-3 um (p.5): the
  value sentence cites ref. 31, the authors' own earlier conference paper (D259 / D408), so not entered; the coupler then
  has only geometry (500 um overlap, 250 nm taper) and no row. Microdisk modulator ER > 20 dB / IL < 3 dB (EO modulator,
  rule 2). Earlier design -18 dB crosstalk (ref. 25). 3.2 pJ/bit system estimate (system level). Error-free BER results
  (no parameter).
- tanaka2009a: rise / fall 2.5 / 1.0 ns (sentence cites the driver paper ref. 14, no data shown; D80i); power penalty
  < 0.4 dB and 20.5 dB input power dynamic range (no parameter); drive-voltage deviation < 90 mV and insulation
  resistance > 200 kOhm (no parameter); gate capacitance < 6 pF, far-field FWHM 16.6 x 18.7 deg, PDG < 0.3 dB of the
  discrete gate, butt-joint reflectivity < 1e-5 (parameters not allowed for these classes, see gaps); Fig. 7
  test-waveguide losses (scope not identifiable: the structure includes the SOA butt-joint, fiber coupling not described);
  +10.1 dBm penalty-free 40 Gb/s output (rests on an assumed 5.5 dB margin from ref. 12); FFC 50 um fabrication
  tolerance (note only).
- chen2015b: nine-channel 400 GHz AWG on the same chip ("similar" crosstalk, no value: no row); Fig. 4 grating-coupler
  spectra (no value stated); simulated MMI split-ratio curve Fig. 3(b) (not read).
- guerber2017: abstract crosstalk "as high as 37dB" over multiple devices (not assignable to either AWG, D159; noted on
  the standard-design row); flattened-design loss level (no number; edge-coupled, facets included); FSR > 80 nm design
  criterion (design rule); flattened-design array order / arm count (printed for the standard design only).

## Missing fab / facility orgs

- ePIXfab (fab, MPW foundry service): lit:dasmahapatra2014 p.3 Sec. III-A ("fabricated on a standard silicon-on-insulator
  (SOI) platform by the ePIXfab foundry") and p.9 Acknowledgment. Not in organizations.csv / org_aliases.csv; fab left
  empty on all four rows, `process_name` "ePIXfab foundry, standard SOI platform". (Already named for the org round in
  D422.)
- zhang2019g p.8 Acknowledgment names the Marvell Nanolab Facility and the Center for Nano-Micro Manufacturing for the
  interposer test chip only; that coupler has no row, so no facility ids were needed.

## Judgment calls

a. zhang2019g evanescent coupler 0.41 dB not entered: the result sentence ends with ref. 31 (authors' 2018 conference
   paper on the interposer coupler) although Fig. 9(b) shows the data in this paper (D408 read strictly).
b. dasmahapatra2014: matrix and switch element as `switch_fabric.other` (D407, khope2019 precedent) plus a
   `resonator.coupled_rings` row for the fifth-order ring's spectral / tuning values (D396 cross-notes).
c. dasmahapatra2014: 11.8 pm/mW and 120 mW P_pi `author_estimate` because the power axis assumes a constant 400 Ohm
   heater resistance (p.5); 6.9 V V_pi `measured`. Off-state 0.9 dB (fit slope) and the 14.0 dB intercept `measured`
   (D80a), on-state 2.0 dB `author_estimate` (intercept minus the cited 12 dB coupler loss).
d. dasmahapatra2014: fsr_nm 2.84 (Table II model parameter, origin not stated) `author_estimate`; Table II coupling
   coefficients 0.90 / 0.60 / 0.35 entered as 90 / 60 / 35 % `derived` (curve fit). Waveguide 2.6 dB/cm
   `author_estimate`, wavelength 1550 nm inferred from Table II.
e. tanaka2009a fab empty (passive "was fabricated", "we developed"; D80b) although all authors are at Fujitsu
   Laboratories.
f. tanaka2009a: the 8:1 switch carries switch_fabric values and a second `amplifier.soa` row for its fiber-to-fiber gain
   and total NF (D396); gain deviation entered as `il_nonuniformity_db`, PDG as `pdl_db` on the switch row. Total NF
   8.6-9.4 dB `derived` (TE / TM equalized with a stated assumption, D80a); conclusion's 1.2 dB "total gain deviation"
   vs 3.0 dB kept as a conflict note (D417).
g. tanaka2009a: FFC "channel imbalance of 1.0 dB" entered as `il_nonuniformity_db` (8 ports) `author_estimate`
   (measured vs simulated not stated); L_c 14-16 dB (NF-relation parameter) on the FFC row as `author_estimate`
   insertion loss including the fan-out waveguides.
h. chen2015b fab org_zhejiang_university on all rows from "we also fabricated a simple regular 14-channel AWG" (p.6),
   reading "also" as covering the main chip; the main fabrication paragraph is passive.
i. chen2015b: MZI interleaver keeps both the standalone ~1.0 dB (Fig. 7) and the in-demux ~2 dB contribution; MMI
   simulated 0.7 dB scoped `device_total` (two MMIs in a symmetric MZI).
j. zhang2019g: 16x16 / 32x32 losses scope `unspecified` (normalization stated only for the 8x8); fab AIM from "in the
   same MPW run" (p.6). Microdisk thermal tuner entered as `resonator.disk` (non-EO values of a PDK modulator).
k. guerber2017: channel IL 1.91-2.29 dB scope `unspecified` (grating-coupler measurement, normalization not stated);
   fab org_stmicroelectronics from "fabricated on 300mm wafers in ST Crolles", `process_name` empty (no process named).
l. Design channel spacings / FSRs (zhang 200 GHz and 1.6 THz, guerber 20 nm, chen 3.2 nm and 200 GHz, dasmahapatra
   350 GHz) `author_estimate` per D82a.

## Registry gaps (skipped value + locator + proposed definition)

- `heater_resistance_ohm` on switch_fabric: dasmahapatra2014 400 Ohm parallel heater pair (p.4 Sec. III-B); same
  definition as phase_shifter (already a D440 candidate).
- `pitch_um` on switch_fabric: dasmahapatra2014 input / output bus pitch 300 / 250 um (p.4 Sec. III-A) (D440 candidate).
- `capacitance_ff` on amplifier: tanaka2009a SOA gate parasitic capacitance < 6 pF (p.5 Sec. III-A); "device
  capacitance of an SOA gate".
- `beam_divergence_deg` on amplifier (or fiber_chip_coupler): tanaka2009a far-field FWHM 16.6 x 18.7 deg vertical x
  horizontal at the SOA facet with SSC (p.3 Sec. II-B).
- `pdl_db` on amplifier: tanaka2009a PDG < 0.3 dB over 1490-1570 nm (p.3 Sec. II-B); "polarization-dependent gain".
- `back_reflection_db` on waveguide_platform (transition): tanaka2009a active-passive butt-joint reflectivity < 1e-5
  (about 50 dB) for all channels and polarizations (p.3-4, Fig. 6); "reflection at an on-chip material junction,
  positive dB below the input".
- System-level, probably rejected: `power_penalty_db` (tanaka2009a < 0.4 dB p.6; dasmahapatra2014 < 1.0 dB Table V),
  input power dynamic range (tanaka2009a 20.5 dB at 0.5 dB penalty, p.6).
