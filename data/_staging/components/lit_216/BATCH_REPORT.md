# lit_216 batch report

Distilled 2026-11-20. Papers: lit:olivares2021, lit:kang2019, lit:clark2003, lit:joshi2008. Page-1 titles match the source
rows; none is a correction / erratum; no garbled text layer. Totals: 14 components, 58 metric rows.
`merge_component_staging.py data/_staging/components/lit_216 --dry-run`: +14 components, +58 metrics, 0 errors (one
warning on an already merged row of another batch, cmp_lit_ni2025b_pimmwc).

## lit:clark2003 (InGaAs/InP APDs for 10 Gb/s receivers; OFC paper TuI1, Nortel) - 3 components / 11 metrics

- `cmp_lit_clark2003_apd_20um` (photodetector.apd, inp): GBP 140 GHz at M = 40 (measured, statistic typical), 3-dB
  bandwidth at M = 5 / 10 / 20 / 40 read off Fig. 4 (about 8 / 9 / 6.5 / 3.5 GHz), capacitance ~220 fF at 90 % of
  breakdown (derived, pF -> fF), series contact resistance < 15 ohm, absorber 1000 nm (derived from 1 um).
- `cmp_lit_clark2003_pin_50um_ref` (photodetector.vertical, inp): reference p-i-n, 0.70 A/W at 1300 nm (fiber ref
  plane, measured), QE 67 % (derived by the authors from the responsivity). Kept as uncited own calibration device
  (D588 martinez2016 precedent).
- `cmp_lit_clark2003_apd_back_mirror_rx` (photodetector.apd, inp): back-mirror version in the receiver module,
  unity-gain responsivity 0.85 A/W (author_estimate: "was estimated", method not stated).

Not entered and why:
- Gain "more than 30" before the dark current exceeds 20 nA, and dark current "< 5 nA" at M = 10 (p.2): no bias
  printed; avalanche_gain / dark_current_na require bias_v. Reading a bias off Fig. 2 would be a guess.
- k_eff = 0.31 at M = 10 (p.2, McIntyre analysis of Fig. 3): registry gap `ionization_ratio_k` (D436 candidate).
- Fig. 3 excess-noise points: both "APD" arrows point at triangle markers while the dashed line runs through square
  markers; which series is the measured APD is not unambiguous (D156), so no `excess_noise_factor` rows.
- Receiver sensitivity -27.8 dBm at 1e-9 BER, 10 Gb/s, NRZ 2^23-1 (p.2, Fig. 6): registry gap `rx_sensitivity_dbm`
  (D436 / D443 candidate).
- Reliability (< 1 failure per 1000 h on 40 APDs at 200 C, 100 uA / 2 mA; Fig. 5): no parameter.
- Active diameter 20 um, guard ring 5 um, PIN 50 um: no diameter parameter (component notes).
- Comparison k values for InP / InAlAs (refs. 4-6): cited.

Fab / facility: fab empty. The fabrication section is passive and the conclusion says "have been fabricated"; all
authors at Nortel (Advanced Technology Lab, Nortel Optoelectronics; p.1). No org needed unless the auditor rules fab
(Nortel is not in organizations.csv / org_aliases.csv).

Registry note: the `lit:clark2003` source row has year 2003 and venue OFC while the DOI is 10.1109/ofc.1999.767804
and the page header is "TuI1" (OFC 1999 numbering). The cached PDF matches the title; the year field may be wrong
(registry follow-up, not changed here).

## lit:joshi2008 (2 um InGaAs p-i-n photoreceiver, Discovery Semiconductors) - 2 components / 11 metrics

- `cmp_lit_joshi2008_ddr_pin_30um` (photodetector.vertical, inp): dark current 400 nA at 5 V (measured) plus Fig. 3
  reads at 10 / 15 / 20 V (~1.1 / 2.5 / 4.4 uA); responsivity 1.34 A/W at 2050 nm, 5 V, `ref_plane module` (measured
  on the SMF-pigtailed package, D155); QE 90 % (author_estimate: rests on a 10 % fiber + AR loss of unstated origin);
  saturation photocurrent 1 mA (highest linear point, 0.75 mW); series resistance 10 ohm from the p-contact
  (author_estimate, method not stated); absorber 2000 nm (derived from 2 um). All at 300 K as printed.
- `cmp_lit_joshi2008_photoreceiver` (photodetector.vertical, inp): receiver-level 3-dB bandwidth 6 GHz (RC-limited,
  -3 dBm input, 5 V) and total capacitance ~400 fF (PD + pads + TIA input + package; derived from ~0.4 pF).

Not entered and why: conversion gain 670 V/W, NEP 9.9 pW/rtHz (calculated), PD-only NEP 13.6 pW/rtHz (calculated),
> 1 V pp RF output, shot-noise-limited above 200 mV pp: no registry parameters (nep_pw_per_rthz, transimpedance /
conversion gain are open candidates D434 / D455 / D534). TIA (500 ohm, 10 GHz, 12 pA/rtHz) is electronics. Prior-work
50 GHz statement (ref. [11]) cited.

Fab / facility: fab empty ("was fabricated", passive; both authors at Discovery Semiconductors). Coherent
Technologies thanked for characterization help (not fab / facility). Discovery Semiconductors is not in the registry
(only relevant if the auditor rules fab).

## lit:kang2019 (1 x 16 Si OPA with p-i-n phase shifters, KAIST / NNFC) - 7 components / 26 metrics

- `cmp_lit_kang2019_pin_ps_wi2p5` (phase_shifter.other, soi_rib, test_structure): P_pi 1.7 mW/pi at 1550 nm TE
  (measured, MZI test device); simulated ~1.55 mW/pi (Fig. 2(a) read); rise / fall 29 / 22 ns (derived, ns -> us);
  simulated additional loss for 2 pi 2.9-3.2 dB (insertion_loss_db per_component, `includes` says injection-induced
  part only); design geometry 500 nm x 220 nm rib, 70 nm slab, 1 mm (derived), BOX 2 um.
- `cmp_lit_kang2019_pin_ps_wi1/_wi2/_wi3/_wi4/_wi5` (phase_shifter.other): Fig. 5(a) width series, P_pi ~0.95 /
  1.57 / 1.98 / 2.21 / 2.46 mW/pi (extracted_from_figure, +/-0.03), one sibling row per i-region width (rule 9).
- `cmp_lit_kang2019_opa_1x16` (free_space_emitter.other, soi): steering range 45.4 deg (measured) and > 45 deg design
  (author_estimate), divergence 3.4 / 5.9 deg and SLSR 8.2 dB measured, 3.3 / 6.2 deg and 12.6 dB simulated, radiator
  pitch 2 um, 16 channels, footprint 1.76e6 um2 (derived from 1.1 mm x 1.6 mm).

Not entered and why:
- Average beam-forming power 39.6 mW of the 16 phase shifters (per beam 40.3 / 37.2 / 38.7 / 42.1 mW) and average
  transition time 24 ns (24 / 26 / 22 ns): no free_space_emitter power / switching-time parameter (D558 candidates);
  in OPA notes.
- 2 pi at 1.1 V: v_pi_v holds pi voltages, no pi voltage printed; "20 Mbps / 20 MHz modulation speed": not a 3-dB
  bandwidth; i-region width (no phase-shifter intrinsic-width parameter); 50 um phase-shifter pitch.
- Element losses (GC, MMI, radiators): the paper points to its ref. [11] (cited). Ref. [10] comparison values cited.
- Fig. 3(b) 3.1 / 3.2 dB simulated order-intensity drops: no parameter.

Fab / facility: fab empty ("The OPA was fabricated on an 8-inch SOI wafer ... using CMOS compatible processes",
passive, no org; authors at KAIST and the National NanoFab Center). If the auditor reads NNFC as the fabricator: NNFC
is not in the registry (name as printed "National NanoFab Center (NNFC)", p.1).

## lit:olivares2021 (SAHAS non-volatile photonic memory, UPV) - 2 components / 10 metrics, all row_kind design

- `cmp_lit_olivares2021_sahas_ps` (phase_shifter.other, design, platform empty): retention > 10 years
  (315,360,000 s, simulated; written-state delta n_eff stays above 1.1e-3), poly-Si gate width 450 nm, Si slab 100 nm
  (design_target); stack thicknesses (6 / 4 / 6 nm) and gate thickness 70 nm in core_material.
- `cmp_lit_olivares2021_sahas_ring_memory` (resonator.ring, design): ER > 12 dB over 10 years and ~15 dB in cycling,
  IL < 1 dB written state (per_component), SAHAS-waveguide loss 112.8 / 82.4 dB/cm written / erased (simulated,
  printed 11.28 / 8.24 dB/mm), power coupling 15 % (author_estimate design input, printed |k| = 0.15), R = 20 um.

Not entered and why: write / erase times (100 us) and voltages (+21.5 / -30 V), energies 1.25 / 5.7 pJ, stored
charge, delta n_eff values: no registry parameters (`write_time_us`, `write_energy_pj`, `delta_neff` would be needed;
`rise_time_us` is a 10-90 % optical response, not a charge-programming time). Output-power drift ~2 dB over retention:
no parameter. Table 1 comparison: other works.

Fab / facility: none (simulation only; "experimental validation ... remains as a future work", p.8).

## Judgment calls for the auditor

1. olivares2021 waveguide losses (dB/mm) placed on the ring row as `prop_loss_db_per_cm` because phase_shifter has no
   dB/cm parameter and Fig. 6(a) draws the whole ring as the SAHAS waveguide; alternative: a third
   `waveguide_platform.straight` design row (D396).
2. olivares2021 platform left empty (no BOX / wafer stated, D422) although the paper frames it as Si photonics.
3. olivares2021 ring wavelength: `band c_band` + `wavelength_inferred` (readout wavelength not printed; model at
   1.55 um); the loss rows use 1550 nm as stated for the material model.
4. olivares2021 |k| = 0.15 entered as power_coupling_pct 15 with basis author_estimate (design input) rather than
   derived (ratio -> %).
5. kang2019 simulated "additional loss for 2 pi" (2.9-3.2 dB) entered as insertion_loss_db per_component with an
   `includes` note; alternative: notes only.
6. kang2019 rise / fall times assigned to the 2.5 um design (printed for "a MZI test device" at 1.1 V pp, the 2 pi
   voltage of that design; conclusion ties them together). If read as D159-ambiguous, move to notes.
7. kang2019 p-i-n carrier-injection phase shifter as phase_shifter.other (poulton2019 / D582), not EO atlas.
8. joshi2008 split into photodiode row and photoreceiver row (bandwidth / capacitance include TIA and package).
9. clark2003 GBP 140 GHz statistic `typical` ("typical device" of Fig. 4) although the conclusion says "as high as".
10. joshi2008 saturation photocurrent 1 mA without qualifier (highest linear point measured; beckerwerth2021 precedent).

## Registry gaps (value skipped + locator + proposed definition)

- `ionization_ratio_k` (photodetector, unit 1): effective ionization rate ratio k_eff from excess-noise analysis;
  clark2003 0.31 at M = 10 (p.2).
- `rx_sensitivity_dbm` (photodetector, dBm): receiver sensitivity at the stated BER / bit rate; clark2003 -27.8 dBm at
  1e-9, 10 Gb/s (p.2, Fig. 6).
- `nep_pw_per_rthz` (photodetector, pW/rtHz): noise-equivalent power; joshi2008 9.9 (receiver) / 13.6 (PD only,
  50 ohm) (p.1, p.3).
- `conversion_gain_v_per_w` (photodetector, V/W): photoreceiver responsivity x transimpedance; joshi2008 670 V/W (p.2).
- `power_consumption_w` widened to free_space_emitter, plus a beam `transition_time_ns`; kang2019 39.6 mW average,
  24 ns (p.4, Fig. 6(b)).
- `write_time_us`, `write_voltage_v`, `write_energy_pj` (phase_shifter, non-volatile programming); olivares2021
  100 us, +21.5 / -30 V, 1.25 / 5.7 pJ (p.6-7).
- `delta_neff` (phase_shifter, unit 1): effective index change of a phase-shifter waveguide; olivares2021 1.5e-3
  written, > 1.1e-3 after 10 years (p.6-7).
- `intrinsic_width_um` (phase_shifter geometry): i-region width of a p-i-n phase shifter; kang2019 1-5 um series
  (p.2-3).

## Missing orgs

None required for the entered rows (all fab / facility fields empty by D80b). For reference only, not in the registry:
"Nortel" (Advanced Technology Lab / Nortel Optoelectronics, clark2003 p.1), "Discovery Semiconductors" (joshi2008
p.1), "National NanoFab Center (NNFC)" (kang2019 p.1).
