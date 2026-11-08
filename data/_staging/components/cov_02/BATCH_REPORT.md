# Batch cov_02 report (distill subagent, 2026-11-07)

Six laser papers (high-power DFB, DFB arrays, external laser sources for CPO). Dry run:
`batch cov_02: +14 components, +119 metrics; errors 0` (one WARN about another batch's row, cmp_lit_ni2025b_pimmwc-m18).
No existing rows for these six sources in `data/components/`. `lit:levy2026` (JLT, wavelength-spacing controller) is a
different paper from `eo:levy2026` (VLSI 2026 transceiver, staged in cpo_01). Page-1 titles match the source rows; none
is a correction or erratum; no garbled text layer. All restricted: facts and locators only. Page renders checked: hatai
p.3, zhou p.1-2, mao p.1-2, levy p.5, mehta p.4, xie p.4 and p.7.

## Per paper (components / metrics)

- hatai2024, Lumentum OFC 2024 (2 / 11): 400-GHz 8-ch SOA-DFB array (laser.soa_dfb, inp): 100 mW at 350 mA and 50 C,
  threshold about 25 mA, 0.56 dB power spread, SMSR > 40 dB, 400 GHz spacing, 300-500 GHz over 20-75 C (pulse),
  wavelength range from Fig. 2(b). Sibling 200-GHz array: 170-230 GHz, wavelength range from Fig. 2(f).
- zhou2022b, Lumentum / Facebook CLEO 2022 (3 / 21): 4 mm 1310 nm DFB COS (laser.dfb, inp): 880 mW max at 25 C,
  99 mA, 0.45 W/A, PCE peak about 31 % (figure), SMSR > 50 dB, far field 6.0 / 20.1 deg. 14-pin butterfly module
  (laser.els_module): 720 / 640 / 580 mW ex-fiber at LD 25 / 40 / 50 C, 150 mA and 0.35 W/A at 50 C, 1.8 V at 2.0 A,
  PCE >= 10 % at 400 mW, peak about 20.5 % (figure), SMSR > 45 dB, RIN < -156, PER > 16 dB. Lensed PM fiber coupling
  86 % (fiber_chip_coupler.other, per_facet).
- mao2024, Huawei OFC 2024 (4 / 20): S-band 2.5 mm SCOW DFB: > 700 mW kink-free, figure reads (560 mW at 60 C,
  thresholds), about 1490 nm, SMSR about 50 dB, typical divergence 9.0 / 15.4 deg. L-band 2.5 mm: RIN < -160 dB/Hz,
  intrinsic linewidth 21.5 / 23.5 kHz (derived per the zhuang2025 precedent), Fig. 1(a) power reads. L-band 2 mm:
  Fig. 1(a) reads. L-band mounting-comparison laser: thermal resistance 16 / 12 K/W (p-side up / down).
- levy2026, Intel JLT 2026 (2 / 10): 8-lambda DFB array under the delta-lambda controller (laser.dfb): 200 GHz
  nominal, spacing 187.5-212.5 GHz open loop, 196.5-203.5 GHz locked (L1 ref), 193-207 GHz under 20 / 30 C steps,
  power variation < 3 dB typical before and < 1.5 dB after VOA equalization. Reference ring (resonator.ring): FSR
  200 GHz (author_estimate), radius 60 um, 65 mW heater share of the controller estimate (author_estimate).
- mehta2026, NVIDIA / Lumentum ECTC 2026 (2 / 10): ELSFP module (laser.els_module): 8 ch, 200 GHz, spacing 184-216 GHz,
  power variation < 1.6 dB (derived from +/-0.8 dB), per-lambda 7.5-9.2 dBm after the 8x8 mux (figure), RIN < -130,
  module efficiency 7.2 % plus per-channel range 6.5-7.65 % over three modules (figure), SMSR > 40 dB at 350 mA.
  DFB-SOA array die (laser.soa_dfb, inp): ex-facet variation < 0.8 dB (derived from +/-0.4 dB).
- xie2026a, Nanjing Univ. et al. Opt. Express 2026 (1 / 47): 8-ch REC asymmetric pi-phase-shift DFB array (laser.dfb,
  inp): 315.53 mW mean at 800 mA, threshold 41.5 mA, 0.49 W/A, 2.2 ohm, WPE 27 % mean max; LD2 at 15 / 65 C
  (threshold, SE, 800 mA power, max WPE); SMSR > 50 dB; spacing 1.1336 nm and deviation 0.075 mean / 0.0417 std
  (individual), 1.1169 nm and 0.0692 / 0.0738 (simultaneous 300 mA); Table 1 range 113.2-119.7 mW and 0.24 dB
  (derived); 3.9 W array power; 112 pm/K; tuning ranges 5.61 nm (temperature) and 2.67 nm (current); 0.66 GHz/mA
  (derived from 3.8 pm/mA); 13 K/W; far field measured and simulated; Lorentzian linewidth 300 kHz best, < 450 kHz;
  RIN peak -154 / -126 dB/Hz; relaxation oscillation 1 / 5.8 GHz; 2 mm cavity, 250 um pitch, 4 um ridge.

## Not entered, and why

- hatai2024: 2000-h aging at 80 C and the +/-0.2 nm (+/-50 GHz) post-aging wavelength shift (no aging parameter);
  calculated gain spectra (Fig. 1(b)); thermal wavelength drift (only computable from Fig. 2(c) slopes, not stated).
- zhou2022b: 22-25 dBm per-laser need and 10 % PCE target (requirements); structure statements cited to [2] / [3].
- mao2024: earlier results cited to [1] / [5] (700 mW C / L band, 200 mW O band at 85 C, 2000-h aging, rule 3 / D259);
  aging of 20 samples over 5000 h at 90 C, 1.5 A, one failure at 4170 h; FIT 86.7 / 45.1 (author_estimate with assumed
  Ea and n); -20 dB widths 470 / 430 kHz (kept as the source of the derived intrinsic values); Fig. 1(b) powers.
- levy2026: 120 mW integrated-controller estimate (other than the 65 mW heater share), 800-1300 Hz loop-bandwidth
  estimate, 13 kHz ring-heater thermal bandwidth (no parameter); marker tones; VOAs, p-i-n modulators, MMI combiners,
  output coupler (no quantitative result); CW-WDM / OCI MSA tolerances and the comparison values from [30], [32], [35]
  (cited); emission wavelengths (Fig. 8(e) tick labels too coarse for a clean read).
- mehta2026: 8 dBm per lambda and 100 mW SOA output (design statements tied to [9-11]); Fig. 5(b) channel frequencies;
  Fig. 8(a) junction temperature versus ex-facet power; all link-efficiency modeling (Figs. 6-7, 1.6 dB, about
  +/-10 GHz, about 10 % thresholds); NVLink table and GPU platform figures (out of scope).
- xie2026a: FP-laser internal loss 2.9 /cm (Hakki-Paoli) and calculated cavity loss 3.0 /cm (no laser parameter);
  simulated thermal maps and random-phase wavelength variation (generic cavities); Fig. 2(b) design wavelengths and
  sampled-grating periods 4.4-5.3 um (sampling period, not the Bragg period_nm); Table 2 simultaneous-operation
  wavelength shifts (up to 1.47 nm) and estimated junction-temperature rises; about 3 W thermal load (estimate);
  values attributed to other groups in the introduction.

## Organizations

- Fab orgs entered: org_huawei on mao2024 S-band row only ("we have fabricated", p.2; all authors Huawei; D399).
- Fab left empty (D80b, passive verbs or no fabrication sentence): hatai2024, zhou2022b, mao2024 L-band rows,
  levy2026 (Intel platform statement applies to the earlier array [33]), mehta2026, xie2026a.
- Missing from the registry: "O-NET" (mehta2026 p.5 Acknowledgment, collaborators supporting ELS packaging and
  evaluation-board development). Not entered as fab or facility (company, packaging support, not a shared facility).
- No facility acknowledgements in any of the six papers.

## Registry gaps (skipped value + locator, proposed definition)

1. `channel_spacing_error_ghz` (laser, wdm; GHz): maximum deviation of adjacent-channel spacing from the target grid,
   +/- as stated. Skipped as such: levy2026 +/-12.5 / +/-3.5 / < 7 GHz (p.5-6, Figs. 8-9), mehta2026 +/-16 GHz
   (p.3, Fig. 5(b)), hatai2024 +/-100 / +/-30 GHz (p.2). Entered meanwhile as `channel_spacing_ghz` ranges (derived).
2. `aging_wavelength_shift_nm` or a reliability group (laser): wavelength shift and power change after an aging test
   (duration, temperature, current in condition); `fit_rate` (count per 1e9 device-hours, author_estimate). Values:
   hatai2024 +/-0.2 nm after 2000 h at 80 C (p.2); mao2024 FIT 86.7 / 45.1 (p.3, Fig. 5).
3. `internal_loss_per_cm` (laser, amplifier; 1/cm): modal internal loss of the active waveguide (method in condition).
   Values: xie2026a 2.9 /cm, Hakki-Paoli on a 1000 um FP companion laser (p.5, Fig. 5); 3.0 /cm calculated (p.3).
4. `current_tuning_pm_per_ma` (laser; pm/mA) to keep the printed unit: xie2026a 3.8 pm/mA (p.7) is entered as
   0.66 GHz/mA (derived) in `fm_efficiency_ghz_per_ma`.
5. `thermal_bandwidth_khz` (phase_shifter, resonator): heater thermal bandwidth; levy2026 13 kHz (p.5).

## Questions for the coordinator

1. zhou2022b butterfly module as `laser.els_module` (the paper calls it the ELS laser prototype, single laser) rather
   than `laser.dfb` with ref_plane fiber. Keep?
2. mao2024 Fig. 1 (cavity-length and mounting comparisons): the paper says it first reviews earlier work "and compares"
   cavity lengths and mounting, without saying whether Fig. 1 is new. Figure reads and the 16 / 12 K/W were kept. If
   the coordinator reads Fig. 1 as reproduced (D259 / D408), delete the 2 mm row, the mounting row and the four
   Fig. 1(a) power rows.
3. mao2024 platform left empty (SCOW named, material not stated; D422), while zhou / hatai / mehta / xie state InP-based
   epitaxy. Confirm.
4. Spacing errors written as `channel_spacing_ghz` ranges around the nominal (derived) until a spacing-error parameter
   exists (gap 1). Acceptable, or leave them out?
5. levy2026 fab and platform empty: Intel's hybrid III-V/Si platform is stated for the earlier array [33]; for this die
   the paper only says "fabricated at a nominal spacing" (passive) and has no acknowledgement. Confirm empty.
6. mehta2026 O-NET packaging support: no fab / facility entry. Should a packaging-assembly support acknowledgement count
   as fab org for an assembled module (analogous to D398)?
7. mehta2026 7.2 % module efficiency: statistic (mean over channels / modules) not stated; entered without statistic,
   plus the Fig. 5(e) per-channel range. The y-axis says LD efficiency while the text says module efficiency including
   driver-side losses; kept as module efficiency with the text definition.
8. mao2024 intrinsic linewidths entered as `derived` (zhuang2025 precedent for -20 dB-based values) although the paper
   prints them. Confirm.
