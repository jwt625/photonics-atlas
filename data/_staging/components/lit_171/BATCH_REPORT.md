# lit_171 batch report

Distilled 2026-11-16 under the pic-component-distill skill (Contracts v4-v7). Papers: lit:acoleyen2012,
lit:ciminelli2013, lit:mao2008, lit:fang2011, lit:acoleyen2011. Totals: 13 components, 82 metric rows.
`merge_component_staging.py --dry-run`: +13 components, +82 metrics, 0 errors (the one warning printed belongs to the
merged row cmp_lit_ni2025b_pimmwc, not this batch).

Page-1 title check: all five cached texts are their source rows' papers (titles match `sources.csv`). None is a
correction / erratum; no garbled text layer flagged.

## lit:acoleyen2012 - 1 component, 10 metric rows

| component | class | metrics |
|---|---|---|
| cmp_lit_acoleyen2012_nems_slot_ps_3x5p8um | phase_shifter.mems | phase shift about 0.222 pi (printed about 40 deg) at 13 V, derived; mechanical resonance 60 / 26 MHz (fixed / hinged, simulated, in kHz); capacitance about 350 fF (author_estimate); 5.8 um free-standing length per region; slot 100 nm, beams 230 nm, Si 220 nm, BOX 2 um, 220 nm etch |

Values not entered and why:
- Pull-in voltage about 34 V (fixed) / 15 V (hinged) for L = 5.8 um (p.5, simulated): no registry parameter.
- Gas-damping mechanical Q about 7, damping time 37 ns (p.10, calculated): no parameter (mechanical Q is a D438
  registry candidate).
- Distributed resistance about 20 MOhm and RC constant about 7 us (p.10): no parameter for a MEMS phase shifter
  (`series_resistance_ohm` is not allowed on phase_shifter); in component notes.
- Dynamic response (Fig. 13, 10 V square wave, 100 us period): no number measured; "expected" MHz speed is a projection.
- Simulated phase-vs-voltage curves for other lengths (Fig. 6) and n_eff vs slot width (Fig. 2): curves only.

## lit:acoleyen2011 - 1 component, 8 metric rows

| component | class | metrics |
|---|---|---|
| cmp_lit_acoleyen2011_nems_slot_ps_9um | phase_shifter.mems | phase shift 0.333 pi (printed 60 deg) at 15 V, derived; insertion loss about 5 dB at the Fabry-Perot resonance near 1525 nm (scope unspecified); 9 um free-standing length; slot 100 nm, beams 230 nm, Si 220 nm, BOX 2 um, 220 nm etch |

Values not entered and why:
- V_pi L_pi figure of merit 96 / 68 / 52.5 V um for designed lengths 15 / 20 / 25 um (p.3, simulated): no registry
  parameter (D438 candidate `vpi_l_v_cm`); a v_pi_v derived from the product would rest on an unstated definition of
  L_pi, so no design rows were created.
- Stable (pre-pull-in) solution up to 18 V for the 9 um device (p.2, simulated): no parameter.

Same-group handling (D259 / D408): the two papers describe different devices (single 9 um slot vs cascade of three
5.8 um slots). acoleyen2012 cites acoleyen2011 as ref. [10] ("first proof-of-principle") but restates none of its
values; each paper's geometry (100 nm slot, 230 nm beams, 220 nm Si, 2 um BOX) is stated by that paper itself and is
kept on its own row. The shared simulated curves (n_eff vs slot width) are not entered in either. Cross-notes on both
rows.

## lit:ciminelli2013 - 6 components, 35 metric rows

| component | class | metrics |
|---|---|---|
| cmp_lit_ciminelli2013_ring_r13mm_g3 | resonator.ring | Table 1 (mean of 24 resonances): Q_L 0.97e6, FWHM 1.6 pm, FSR 8.4 pm (0.0084 nm derived), resonance depth 7.0 dB, finesse 5.3; fit alpha 0.44 dB/cm and coupler efficiency 27.7 % (measured, ring_extraction); Q_i 1.24e6 author_estimate (D403, extraction not stated); design depth 8 dB and design coupling 49.9 % simulated; R 13 mm, gap 1.524 um, width 2.0 um, etch 0.3 um, core 1 um |
| cmp_lit_ciminelli2013_ring_r13mm_g1 | resonator.ring | coupler efficiency close to 9 %, depth about 2 dB (measured); design 34.1 % (simulated); R, gap |
| cmp_lit_ciminelli2013_ring_r13mm_g2 | resonator.ring | design coupling 42.3 % (simulated); R, gap |
| cmp_lit_ciminelli2013_ring_r13mm_g4 | resonator.ring | design coupling 56.9 % (simulated); R, gap |
| cmp_lit_ciminelli2013_inp_rib_wg | waveguide_platform.straight | Fabry-Perot fringe loss 0.50 / 0.44 / 0.40 dB/cm (21.0 / 11.7 / 6.7 mm) and mean 0.45 dB/cm (measured, D394, R = 31 % input); simulated quasi-TE 0.45-1.0 dB/cm; width / etch / core |
| cmp_lit_ciminelli2013_bus_taper | fiber_chip_coupler.edge | simulated 22 % overlap with SMF (per_coupler, 1550 nm inferred) |

Values not entered and why:
- g4 ring Q = 740,000: "has been reported in [24]" (the authors' IPRM 2012 paper): rule 3 / D259.
- "Other fabricated resonators have a quality factor of the order of 1e4-1e5" (p.7): not tied to one ring (D159 /
  D254; it also conflicts with the cited 740,000 for g4); in notes.
- Family statement "coupling efficiency 20-25 % lower than designed" (p.5): notes only.
- Standard deviation of the three test-waveguide losses (9 % of the mean): notes only (a derived 0.04 dB/cm `std`
  row was not added).
- Fabry-Perot FSR 17.8 pm measured / 16.9 pm calculated for the 21 mm test waveguide, n_eff 3.205, TM loss > 1 dB/cm,
  confinement > 80 %: no waveguide_platform parameter or simulated-only side values; in notes.
- Taper internal loss below 1 % (simulated): notes. Chip footprint about 700 mm2: chip-level, not a component value.
- Projected Q 1.13e6 at 0.36 dB/cm and all gyro resolutions (p.8-9): model predictions of a system.
- Judgment: the Table 1 "Waveguide propagation loss 0.45 dB/cm" is the Fabry-Perot test-waveguide mean, entered on
  the waveguide row only; the ring row carries the 0.44 dB/cm fit value. The fit is entered as `measured` (standard fit
  of own data, D80a); the all-pass fit's loss / coupling ambiguity is resolved by the independent 0.45 dB/cm, noted.
- Unit rescales (13 mm, 1.524 um, 2.0 um, 1 um -> um / nm) are `derived` with the printed value in notes (D157 /
  D256); 300 nm etch stays `design_target` (the Fig. 3(b) caption prints 300 nm).

## lit:mao2008 - 2 components, 10 metric rows

| component | class | metrics |
|---|---|---|
| cmp_lit_mao2008_pecvd_sin_wg_s5 | waveguide_platform.straight | 2.1 +/- 0.2 dB/cm at 1550 nm (cutback, measured); 700 x 400 nm, BOX 5 um, top cladding 2 um |
| cmp_lit_mao2008_pecvd_sin_wg_s4 | waveguide_platform.straight | 2.3 +/- 0.2 dB/cm at 1550 nm (cutback, measured); same geometry |

Values not entered and why: coupling loss (Fig. 6 intercept, never printed); AFM roughness 2.13 / 0.18 nm (no
parameter); film indices, deposition rates and H concentrations (material data); Table II values of other works
(rule 3). Upper-cladding conflict 2 um (p.3) vs 3 um (Table II): 2 um entered, conflict noted (D417). Polarization not
stated (PM lensed fibers only): left empty. Etch depth not entered ("etched down till the buried SiO2" gives no number).

## lit:fang2011 - 3 components, 19 metric rows

| component | class | metrics |
|---|---|---|
| cmp_lit_fang2011_to_switch_suspended | switch_fabric.other | P_pi 0.49 mW, crosstalk > 23 dB, normalized IL < 0.3 dB (per_component, reference_structure), rise 144 us / fall 122 us at 1550 nm TE; heater 1000 x 6 um, TiN 200 nm, DC gap 250 nm, 500 x 220 nm, BOX 2 um |
| cmp_lit_fang2011_tin_heater_suspended | phase_shifter.thermo_optic | heater resistance about 1500 ohm; 2 um heater gap; heater geometry (D396 cross-row) |
| cmp_lit_fang2011_to_switch_no_trench | switch_fabric.other | 31 mW switching power, 8 dB crosstalk (same-chip reference without trenches) |

Values not entered and why: total response time 266 us (sum of the two entered values); temperature change 4.2 C design
/ 4.5 C actual (Fig. 4, estimated from Eq. (1)-(2); no parameter); "more than 98 %" power reduction (ratio of entered
values); suspended-SiO2 converter paragraph (p.3) describes no measured device. Judgment: the 23 dB is called extinction
ratio in the abstract and crosstalk in the body; entered once as `crosstalk_db`.

## Fab / facility orgs

- acoleyen2011: fab org_imec ("fabricated on SOI at imec", p.1). ePIXfab only cited as ref. [7]: not a fab org.
- acoleyen2012: fab org_imec ("at imec through ePIXfab", p.7 Sec. 4); `process_name` as printed.
- fang2011: fab org_astar_ime ("we designed and fabricated", all authors at IME A*STAR, one also Jilin University).
- ciminelli2013, mao2008: fab empty (no fabrication sentence names an org; passive wording, D80b).
- No facility statements in any of the five papers. Post-processing staff thanked by name without an org (acoleyen2011,
  acoleyen2012): no fab / facility (D84b / D543).

Missing orgs (registry):
- "ePIXfab" - fab role (MPW access provider named for fabrication, D398) - lit:acoleyen2012 p.7 Sec. 4 ("at imec
  through ePIXfab"); same gap as cabezon2012 / lindenmann2012 / romerogarcia2014.

## Registry gaps

- `pull_in_voltage_v` (phase_shifter, switch_fabric): voltage at which an electrostatic actuator collapses.
  Skipped: acoleyen2012 about 34 V fixed / 15 V hinged (p.5, simulated); acoleyen2011 stable up to 18 V (p.2,
  simulated). Also D440 candidate.
- `vpi_l_v_cm` on phase_shifter (D438 candidate): acoleyen2011 96 / 68 / 52.5 V um (p.3, simulated designs).
- `mech_q` (phase_shifter): acoleyen2012 gas-damping Q about 7 (p.10, calculated).
