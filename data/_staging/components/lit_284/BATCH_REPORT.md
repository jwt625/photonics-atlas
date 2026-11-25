# lit_284 batch report

Distilled 2026-11-25 (verified_on 2026-11-25). Papers: lit:li2018b, lit:auth2019, lit:duprez2016. Page-1 titles match
the source rows; no garbled text layer flagged (li2018b pages 6-12 have column-split text, so values there were read
from the page renders page_06.png-page_12.png). Validation: `merge_component_staging.py data/_staging/components/lit_284
--dry-run` -> +18 components, +116 metrics, 0 errors (two pre-existing warnings on other batches only).

Totals: 18 components, 116 metric rows. No fab or facility org entered on any row (no fabrication statement naming an
org or the authors in any of the three papers).

## lit:li2018b (9 components / 39 metrics)

Monolithic Al2O3:Er3+ Vernier-ring tunable laser on a Si3N4 platform (MIT).

| component | class | metrics |
|---|---|---|
| er_vernier_laser_8p4cm | laser.tunable | 2 (1.6 mW on-chip at 107 mW pump; threshold about 33 mW read off Fig. 3(d)) |
| er_vernier_laser_4p2cm | laser.tunable | 3 (340 kHz linewidth; 2.5 GHz mode spacing and 50 nm Vernier FSR, simulated) |
| ring_r100, ring_r104p6 | resonator.ring (D400) | 7 each (FSR 2.23 / 2.13 nm author_estimate, 8.75 % coupling simulated, geometry) |
| ring_heater | phase_shifter.thermo_optic | 5 (240 ohm, 200 / 230 us time constants, heater geometry) |
| gain_cavity_phase_shifter | phase_shifter.thermo_optic | 8 (170 mW for 2.5 GHz measured, about 200 mW for 2 pi, 25 ohm, 32 / 37 us, geometry) |
| sin_al2o3er_transition | waveguide_platform.transition | 1 (0.3 dB per transition) |
| al2o3er_euler_bend | waveguide_platform.bend | 5 (0.6 dB per 180-degree bend by cutback, geometry) |
| al2o3er_film | waveguide_platform.straight | 1 (background loss < 0.1 dB/cm) |

Not entered and why:
- Tuning 1527-1573 nm (46 nm) with > 40 dB SMSR, < 1.5 dB power variation, lasing at 1525 nm with < 40 dB SMSR, the
  Fig. 3(c) heater-power map and the 0.23 cm2 footprint: the paper fabricated lasers with 4.2 cm and 8.4 cm gain
  waveguides and names a device only for the power data (8.4 cm, p.7-8) and, through the 4.6 cm round-trip cavity, for
  the fine tuning and linewidth (4.2 cm, p.8, p.10). The tuning results come before the two lengths are introduced, so the
  sample is ambiguous (D159): bounds in the notes of both laser rows.
- Slope efficiency 2.2 % with respect to on-chip 980 nm pump power (p.8): optical-to-optical, no parameter (gap 1).
- Fine-tuning efficiency 14 MHz/mW (p.8): no MHz/mW parameter; a pm/mW conversion would need a wavelength the section
  does not state (gap 2).
- Simulated 1.8 dB side-mode selectivity (p.6), simulated confinement factors 90 % / 80 % and material indices (p.6,
  Fig. 1(d)), self-pulsing at 0.125 MHz (p.9), locking to a commercial mode-locked laser comb with < 10 Hz deviation and
  the Allan deviation (p.11, system-level), film spontaneous emission 1524-1574 nm / 50 nm 3-dB width (p.7), designed
  heater sheet resistance 15 ohm/sq (p.5), ring FSR '~250 GHz' (p.8, rounded): no parameter or not component-level.

Missing fab / facility orgs: none to report. Fabrication sentences are passive (p.7); authors at MIT RLE, Harvard and
CNSE University at Albany; acknowledgment thanks two named staff for Er-doped film deposition without naming an org
(neither fab nor facility, D84b / D72).

## lit:auth2019 (1 component / 19 metrics)

Two-section passively mode-locked InAs/InGaAs QD laser grown on on-axis (001) Si, 4.5 mm, 9.4 GHz
(`cmp_lit_auth2019_qd_mll_9p4ghz`, laser.comb, platform iii_v_on_si_epi, temperature 20 C on all rows).

Metrics: repetition rate 9.4 GHz; pulse widths 1.7 / 3.2 / 3.2 ps (stored in fs, derived per D256); timing jitter 9 / 317 /
28 fs (derived from the RF linewidth by the printed formula, kiewiet2025 precedent); -3 dB comb widths 4.5 / 5.5 / 2.63 /
1.1 nm; 103 comb lines (derived); comb centre 1312.5 nm; Table 2 average powers 0.64 / 0.89 / 0.48 mW; fiber-coupled
power about 1.0 mW (Fig. 2(a) read); length 4.5 mm (derived) and ridge 3 um.

Not entered and why: RF (repetition-rate) linewidths 400 Hz / 520 kHz / 4 kHz (gap 3); relative amplitude jitter < 1 %
and 15-70 % (gap 4); RF peak SNR 59 dB, time-bandwidth products, pulse peak powers, bias-map ranges (no parameter);
Table 1 values (other works, including the authors' own refs. [1], [35], rule 3); booster SOA and isolators (setup, rule
13); absorber length (only 18 % printed).

Missing fab / facility orgs: none to report. Growth sentence is passive ('epitaxial growth was completed', p.3);
authors at TU Darmstadt (measurement) and UCSB; no facility named.

## lit:duprez2016 (8 components / 58 metrics)

Heterogeneous III-V/Si sampled-grating DBR lasers in the O band (CEA-LETI / INL).

| component | class | metrics |
|---|---|---|
| sgdbr_laser_1 | laser.tunable | 15 (27 nm tuning, SMSR 35-50 dB and > 40 dB, 7.5 mW in the Si waveguide (derived), 1-8 mW over tuning, threshold about 106 mA (Fig. 6(a)), 22 ohm, heater powers 900 / 1100 mW, mirror FSRs design 6 / 7.5 nm and measured Fig. 7 labels, geometry) |
| sgdbr_laser_2 | laser.tunable | 11 (35 nm tuning, SMSR 35-50 dB, 7.5 mW, 1-8 mW, threshold about 85 mA (Fig. 6(b)), 51 ohm, about 1300 mW heater power, FSRs 6 / 6.5 nm design, geometry) |
| sgdbr1_right / _left, sgdbr2_right / _left mirrors | reflector.bragg | 6 each (80 % design reflectivity simulated, period 196 nm, etch 20 nm, length 635 / 602 / 913 / 915 um, Si 500 nm, width 10 um figure label) |
| iii_v_si_mode_transformer | waveguide_platform.transition | 7 (> 90 % coupling author_estimate, 100 um, 90 nm gap, Si rib stack, III-V 5 um) |
| fiber_grating_coupler | fiber_chip_coupler.grating | 1 (6 dB fiber insertion loss, scope unspecified) |

Not entered and why: sampling periods (39.7 / 31.6 / 36.6 um) and sampling filling factors (0.15 / 0.10) (no parameter,
gap 5); NiFe heater 250 nm thick, 6 um wide (heater parameters not allowed for reflector, gap 5); Fig. 2-4 design-study
mirrors (a_sp 29.8 / 26.5 um, FSR 8 / 9 nm, e = 15 / 25 nm, DCsp 0.10 / 0.15; illustrative designs, not the fabricated
lasers); Fig. 9 0.8 nm-spaced set points (demonstration, noted on laser 1); n-InP thicknesses 125 / 100 nm vs 150 nm
target (fabrication deviation, in notes); +/- 1.34 % relative tuning (arithmetic restatement of 35 nm).

Missing fab / facility orgs: none to report. Fabrication is passive (p.6 Sec. 3); authors at CEA-LETI and INL Lyon;
acknowledgment thanks staff for characterization help; IRT Nanoelec is a funding program (D80c).

## Judgment calls for the auditor

1. li2018b D159: the headline 46 nm tuning and > 40 dB SMSR are not entered on either laser row (sample ambiguous between
   the 4.2 and 8.4 cm devices). Alternative: a coordinator ruling that tuning results belong to the paper's single "laser"
   design and attach them to one row.
2. li2018b two laser rows by gain length (rule 9); linewidth, mode spacing, Vernier FSR and fine tuning placed on the 4.2 cm
   row from the 4.6 cm round-trip statements (p.6, p.8, p.10); power and threshold on the 8.4 cm row.
3. li2018b heater response times entered as `thermal_time_constant_us` (paper: "time constant", exponential fits) rather
   than `rise_time_us` / `fall_time_us` (10-90 % by definition); abstract rounds them to about 200 us and 35 us.
4. li2018b Euler bend 0.6 dB per 180 degrees kept as `insertion_loss_db` per_component (deng2024 precedent) instead of
   halving into `bend_loss_db_per_90` (cheung2019 / chung2017 precedent); cutback "estimated" taken as measured (rule 4).
5. li2018b threshold about 33 mW (+/-3 mW) read off Fig. 3(d) (not printed); 340 kHz linewidth stored as 340000 Hz,
   basis derived (D256); ring FSRs author_estimate (stated with the radii, origin not stated, D82a).
6. auth2019 Table 2 average powers: plane and derivation not stated; Fig. 2(a) fiber-coupled values at the same biases are
   3-4x lower, consistent with the stated ~30 % coupling: entered author_estimate with ref_plane unspecified. The fiber
   power about 1.0 mW at 160 mA / 0 V is a colour-map read.
7. duprez2016 mode-transformer > 90 %: stated with the design, principle referred to [4,11] (ref. [4] is the authors'
   own paper): entered author_estimate; the auditor may judge it a cited value (rule 3 / D259) and remove it.
8. duprez2016 left / right mirror FSR conflict: Table 1 and the Fig. 7 peak annotations agree (right 6 nm, left 7.5 nm for
   laser 1); the Fig. 7 caption and the p.8 text swap sides. Table 1 values entered as simulated, Fig. 7 labels as
   measured.
9. duprez2016 thresholds read off the spiky LI curves (mode hops, power drops to zero near 112-116 mA for laser 1; a spike
   near 85 mA precedes the main rise near 91 mA for laser 2); 7.5 mW in the Si waveguide derived (fiber power plus the
   authors' measured 6 dB, D394); 1-8 mW over the tuning range ref_plane unspecified.
10. duprez2016 grating coupler 6 dB: scope unspecified ("insertion losses into the fibers"; not stated as per coupler),
    O band inferred.
11. duprez2016 mirrors as four reflector.bragg rows whose only performance metric is the simulated 80 % design
    reflectivity (D80e: fabricated parts with simulated values stay fabricated).

## Registry gaps (skipped value + locator + proposed definition)

1. `slope_efficiency_pct` (laser; %): optical-to-optical slope efficiency of an optically pumped laser, pump reference
   plane in condition. li2018b 2.2 % vs on-chip 980 nm pump (p.8 Sec. 3, Fig. 3(d)); also kiani2023 (merged notes).
2. `tuning_efficiency_mhz_per_mw` (laser, phase_shifter; MHz/mW): laser frequency shift per mW of heater power.
   li2018b 14 MHz/mW (p.8 Sec. 4, Fig. 4(b)).
3. `rf_linewidth_hz` (laser; Hz): -3 dB linewidth of the fundamental repetition-rate (inter-mode beat) tone, method in
   condition. auth2019 400 Hz / 520 kHz / 4 kHz (p.8, p.9 Table 2); also kiewiet2025 519 Hz and guzman2019 (merged notes).
4. `amplitude_jitter_pct` (laser; %): relative pulse-amplitude jitter from the integrated RF spectrum up to half the
   repetition rate. auth2019 < 1 % in area D, 15-70 % in area E (p.7-8, Fig. 6(b)).
5. Sampled-grating mirror parameters for reflector: `sampling_period_um` and `sampling_duty_cycle` (reflector), and
   allow `heater_thickness_nm` / `heater_width_um` / `fsr_nm` for reflector. duprez2016 Table 1 (p.7): a_sp 39.7 / 31.6 /
   36.6 um, DCsp 0.15 / 0.10, comb FSR 6 / 7.5 / 6.5 nm; NiFe heater 250 nm (p.6) and 6 um (Fig. 1(c)).
