# lit_222 batch report

Distilled 2026-11-20. Papers: lit:zanzi2019, lit:kumar2022b, lit:albert1999 (page-1 titles match the source rows).
Totals: 18 components, 120 metric rows. `merge_component_staging.py data/_staging/components/lit_222 --dry-run`:
0 errors (the only warning is the pre-existing cmp_lit_ni2025b_pimmwc-m18 duplicate, not in this batch).

## lit:zanzi2019 (14 components, 82 metrics)

Vertical-pn carrier-depletion 2x2 MZI switches in two generations: generation 1 prototyped at NTC-UPV, generation 2
transferred to the ams AG 350 nm CMOS line.

| component | class | metrics |
|---|---|---|
| g1_asym_mzi_switch_pn6um | switch_fabric.other | 8 (30 dB fiber-to-fiber, ports, length, stack) |
| g1_switch_pn2um | switch_fabric.other | 13 (41.5 dB, static ER 7 dB, eye ER 4.7 / 4.1 dB, 60 ps rise / fall, stack) |
| g1_ps_pn6um | phase_shifter.other | 6 (11 dB loss-budget term, length, stack) |
| g1_ps_pn2um | phase_shifter.other | 8 (22.5 dB budget term, simulated 120 ps rise / fall, length, stack) |
| g1_mmi, g1_gc, g1_gc_taper, g1_rib_wg | splitter.mmi, fiber_chip_coupler.grating, waveguide_platform.other / .straight | 5 + 5 + 6 + 5 (budget terms + stack) |
| g2_switch | switch_fabric.other | 18 (about 20.5 dB, on-off > 10 dB, 4 eye-ER ranges, packet ER > 20 / > 15 dB, 0.54 GHz, rise / fall, power estimates, ports, length) |
| g2_ps | phase_shifter.other | 2 (8.25 dB at -2 V, derived from cut-back 6.6 dB/mm; length) |
| g2_mmi, g2_gc, g2_gc_taper, g2_rib_wg | as generation 1 | 1 + 1 + 2 + 2 |

Not entered and why:
- VpiL (0.23-0.5 V cm generation 1; 0.26 / 0.33 / 0.39 V cm generation 2) and Vpi: kept in notes (lu2016a /
  campenhout2009 precedent); Vpi not computed because VpiL varies with the voltage swing.
- Bend losses 2.4 dB (generation 1, "see [38]", the authors' own bend paper) and 1.2 / 0.8 dB (generation 2, sentence
  cites [28]): cited values (rule 3, D80i, D259).
- Capacitances 4.94 / 4.81 / 4.8 / 4.7 pF (p.14): capacitance_ff not allowed for switch_fabric; ambiguous whether per
  arm or per device, so not moved to the phase-shifter rows. Notes on g2_switch.
- Switching energy 3.5 / 0.856 pJ and 117 / 18 fJ per switched bit (p.15-16): no parameter (switching energy
  rejected in D81). Power penalties 0.1-0.4 dB at 40 Gb/s (p.13): system level.
- Per-length phase-shifter loss 8.8 / 18 / 6.6 dB/mm: no parameter (D250); entered as the 1.25 mm totals.
- Generation-2 asymmetric MZI (Fig. 9-10): only VpiL and breakdown (-7 V), no switch parameter -> no row, values in
  the g2 notes. Simulated 11.5 dB excess loss / 1-1.2 um junction estimate (p.7), 15 ps travelling-wave projection
  (p.13): model / projection, not entered. Doping profiles, SIMS: not component metrics.

Missing org (fab): "NTC-UPV" / "Valencia Nanophotonics Technology Center, Universitat Politecnica Valencia" (as
printed: "fabricated in NTC-UPV 6-inch clean room facilities", p.3 Sec. 3; affiliation p.1). Generation-1 rows use
org_upv until an NTC org (child of UPV) exists (D533, larrea2018 precedent). ams AG = org_ams_ag (registry).

## lit:kumar2022b (3 components, 25 metrics)

| component | class | metrics |
|---|---|---|
| cascaded_cdc | wdm.bragg_cdc | 12 (SLSR 12.93 dB measured, 11.17 dB simulated, center about 1527.5 nm figure read, simulated center about 1541.5 nm, CDC2 geometry, 0.4 mm) |
| cdc1 | wdm.bragg_cdc | 10 (SLSR about 5.57 dB measured before tuning, 4.46 dB simulated, heater 72.54 mW derived, WG1 geometry, about 0.19 mm) |
| similar_cdc_cascade_design | wdm.bragg_cdc (design) | 3 (simulated 8.43 / 3.97 dB, 600 periods) |

Not entered: duty cycles 50 % (WG1) / 49.2 % (WG3): fill_factor not allowed for wdm (notes); +/-25 nm corrugation (no
parameter); drop-port insertion loss and bandwidth (Fig. 4 normalization not stated, not printed); 7.36 / 2.74 dB
improvements (differences of entered values); inverse-taper edge coupler 180 nm tip (no performance metric). Fab
org_applied_nanotools (MPW run stated). SDNI appears only in the funding list (D83e): no facility.

## lit:albert1999 (1 component, 13 metrics)

PLC Mach-Zehnder OADM with UV-written Bragg gratings, ge_silica, wdm.bragg_cdc (amorim2017 precedent). Rows: bare MZI
before inscription 0.14 dB / crosstalk 26 TE / 24.9 TM dB at 1550 nm; drop 1 dB TE / 0.7 dB TM at 1527.7 nm; drop
out-of-band about 30 dB; 3-dB width 1.1 nm; Bragg wavelength 1527.7 nm; through IL 1 dB; through notch 36 dB; PDL
0.07 dB; Port 2 worst-case 10 dB; length 25 mm.

Not entered: about 3 dB loss peak 1.2 nm short of the Bragg wavelength (p.2; ambiguous whether additional to the 1 dB);
Port 1 return spectrum "as low as 10 dB" (back_reflection_db not allowed for wdm); 3.8 mm grating length and 250 um arm
spacing (no wdm parameter); BER no-penalty result (system level).

Missing org (fab candidate): "Photonic Integration Research Inc." (footnote, p.1: the commercial Ge-doped silica PLCs
used are "available from" it). Fab left empty: the grating-writing sentences are passive (D80b), and the vendor is not
in the registry.

## Judgment calls for the auditor

1. zanzi2019 two generations as separate rows per part (NTC-UPV vs ams AG fab); stack geometry (220 nm / 2 um BOX /
   70 nm etch / 150 nm slab) only on generation-1 rows, since the ams run does not restate it; generation-2 platform
   soi_rib kept from the transferred shallow-rib design.
2. Loss-budget terms (MMI, GC, taper, passive waveguide, phase shifter) entered as author_estimate rows. GC 9 dB
   "from the I/O grating couplers" halved to 4.5 dB `loopback_half`; MMI 1.6 / 0.6 dB and taper 0.5 / 0.2 dB kept
   unhalved with scope `unspecified` (plural, count not stated).
3. 0.54 GHz E/O bandwidth stored as bw3db_khz 540000 (definition names thermo-optic / MEMS / PCM actuators; feng2011
   p-i-n VOA precedent).
4. zanzi2019 lower-drive eye ERs (10.7-14.5, 6.6-8.9 dB): text says "+/-1.2 Vpp", Fig. 14 caption says 0.6 Vpp;
   assigned to 0.6 Vpp per the caption (noted).
5. zanzi2019 rise / fall "700-750 ps" and "1055 ps" are single printed numbers for both edges: entered as both
   rise_time_us and fall_time_us.
6. zanzi2019 wavelengths: generation-1 values inferred (Fig. 4 axis 1541.5-1543.5 nm on the 6 um switch; c_band
   inferred elsewhere); generation-2 DC values c_band inferred; packet-test ER 1540 nm inferred from the Sec. 5.2 lead
   sentence.
7. kumar2022b CDC1 split into its own row (own geometry and heater); CDC2 has no standalone performance value, so its
   geometry sits on the cascade row with condition labels. The similar-CDC design keeps both stage values on one row.
8. albert1999 PDL 0.07 dB: port not stated (follows the through-port sentence), entered with that condition.
   Port 2 "as low as 10 dB" entered as a worst-case crosstalk without `statistic: best`.

## Registry gaps (skipped value, locator, proposed definition)

- capacitance_ff for switch_fabric: zanzi2019 4.94 / 4.81 pF bar, 4.8 / 4.7 pF cross (p.14); "device capacitance of a
  switch element (state and drive in condition)".
- fill_factor for wdm: kumar2022b 50 % / 49.2 % (p.5-6); same definition as for reflectors.
- grating_length_um for wdm: albert1999 3.8 mm Bragg gratings (p.1).
- back_reflection_db for wdm: albert1999 Port 1 return "as low as 10 dB" (p.2, Fig. 2(d)).
- VpiL for non-EO-atlas switches (vpi_l_v_cm candidate, D438): zanzi2019 0.23-0.5 / 0.26-0.39 V cm (p.5-6, p.8).
