# Batch lit_18 report (distill subagent, 2026-10-29)

Dry-run `batch lit_18: +38 components, +202 metrics; errors 0`. ASCII, no e-mail, no quotes (all nine sources
`restricted_local_only`). Not audited or merged.

## Per paper (components / metrics)

- cheung2022 (10 / 43): HPE QD coupled-cavity comb laser (laser.comb: spacing 63.93 GHz mean, 1.08 GHz std, RIN -144 /
  -135.1 / -138.9 dB/Hz, ~100 pm/K, 1.309 W, 12 of 17 lines within 3 dB, ~-7 dBm/line on-chip as author_estimate); comb-chip
  GC ~10 dB; interleaver-chip GCs ~22 dB (author_estimate, one vs two GCs not stated); Si rib 0.5 / 0.8 um cutback pre-bond
  and after III-V removal; III-V/Si interface transitions 0 / 45 / 72 deg (1.08 / 0.69 / 0.29 dB per facet, cutback; 45 deg
  FDTD 0.36 dB); 1-RAMZI MOSCAP interleaver (wdm.interleaver: XT before / after tuning, Table II ER range, mean ER, 65.78 GHz
  measured spacing, design / fitted kr, ng, Lring, delay length); heater 1-RAMZI (27.59 mW). Not entered: SOA gains and BER
  (refs [24], [14]), Table III link budget (assumptions), simulated sensitivities, reflection < -60 dB (no parameter).
  Fab empty (D80b; all authors HPE, passive "fabricated"; "past in-house fabrication" refers to the budget only).
  Judgment: tuning power 10.0 nW entered (derived nW -> mW) although its p.4 sentence cites ref. [16] (authors' earlier
  interleaver paper); abstract and conclusion state it as this work's result (D80i borderline, flagged). Fig. 5 XT values
  carry no citation and are entered as this paper's.
- huang2019 (10 / 40): UCSB E-DBR lasers kL 0.375 / 0.75 / 1.05 / 3 and RAE-DBR kL 1 / 2 as sibling laser.heterogeneous
  rows (tag dbr; Table 2 power at 400 mA and Lorentzian linewidth; kL 0.375: Ith 50 mA, > 37 mW on-chip, 8.3 mW in fiber,
  SMSR > 55 dB, RIN < -150 dB/Hz; RAE kL 1: Ith 60 mA, 4.8 mW, < 500 Hz); Bragg reflectors kL 0.375 (~40 %, derived from
  measured transmission) and kL 1 (~80 %, "estimated"), kappa = design kL / L (author_estimate); intracavity ring (FSR
  18.5 GHz, FWHM 350 MHz derived, R 600 um, coupling 4 %); 8 deg angled facet to lensed fiber 6.5 dB. Not entered: ULL loss
  0.16 / 0.04 dB/cm and ring Q 4.1 M / 2.1 M (previously demonstrated, ref. [28]), Table 1 comparison, FN floors (no
  parameter), grating 3-dB / FWHM widths 2.9 / 3.3 / 5.0 / ~4 GHz (no GHz parameter for reflector), lasing ~1562.7 nm
  (design not identified). Fab empty (passive fabrication; UCSB + Morton Photonics).
- lee2022 (0 / 0): **cached PDF / text.md is the wrong paper.** source.json and sources.csv describe "Photonic integrated
  circuit with sampled grating lasers ... terahertz generation" (10.1364/oe.454296, 2022), but references/lee2022/text.md
  and the page renders are Ni et al., "Compact and low-crosstalk multimode waveguide crossing utilizing subwavelength holey
  metamaterial waveguides", Opt. Express 32(20) 35743, 2024 (10.1364/OE.533238, printed p.1). Nothing entered; re-fetch.
- ramirez2022 (1 / 22): III-V Lab backside SBG-DFB (laser.heterogeneous): Ith 35 mA, 22 mW single-side waveguide-coupled
  and WPE 17 % (author_estimate: GC-loss calibration not described), 4.5 ohm differential resistance, SMSR > 45 dB, 118 kHz
  (Voigt), T0 52 K and Zth 25 K/W (C -> K relabel, derived), 4 pm/mW self-heating drift, 1543 nm, kappa 37 (stopband,
  derived) / 40 (simulated), intrinsic 14 GHz and fr 9 GHz (derived), geometry (880 um, 240 nm, DC 0.5, 30 nm etch, 2.4 um
  ridge, 825 nm Si rib, 500 nm Si, 2 um BOX). Not entered: 13.4 dBm duplicate, D factor, lifetimes (abstract 8 ps vs text
  ~18 ps), large-signal ER / penalty. Fab empty (passive; III-V Lab / SAMOVAR / CEA-LETI).
- tanaka2012 (7 / 42): Fujitsu flip-chip RSOA + Si ring/DBR mirror laser (laser.ecl: 9.4 mA, 15.0 mW and WPE 7.6 % on-chip at
  20 C, 25 mA / 10.5 mW / 4.5 % at the hot end, ~0.1 W/A, SMSR > 40 dB, RIN < -130 dB/Hz, 78.7 pm/K, mode spacing 15.3 GHz
  / 0.122 nm, ~1555 nm from Fig. 8, 2.0 mm cavity); RSOA (NFP 3.0 x 2.9 um, 600 um); Si-SOA butt interface (1.55 dB
  per_interface author_estimate from the Table 1 loss breakdown with an assumed 0.6 dB waveguide loss; 1-dB tolerances
  +/-1.3 um horizontal / +/-0.9 um vertical; Si-side NFP 3.0 x 3.4 um; tip 50 nm, taper 300 um; gap ~7 um); ring filter
  (FSR 11 nm, 0.6 nm 3 dB, 1.1 dB estimated); DBR (0.6 dB estimated, 5.6 nm stopband, level not stated, 299 nm, 120 um);
  output DC (kappa 0.44); chip facets to lensed fiber (~2 dB, 1.4 dB, author_estimate). Not entered: threshold gain 11.7 dB,
  Si mirror 3.5 dB (simulation input) and ~0.3 nm mirror bandwidth, RR drift 0.076 nm/C (ref. [15]), RSOA SSC length (not
  allowed for amplifier). Fab empty (all Fujitsu Laboratories, passive). The "25 mA / 10.5 mW" temperature is implied
  (high end of 20-60 C), not printed with the values.
- winkler2024 (1 / 9): visible 642 nm GaAs + Si3N4 extended-cavity mode-locked laser (laser.comb): 7.84 GHz repetition rate,
  calculated FSR 7.9 GHz (simulated), 3.4 mW (-2.5 V), ~3.2 mW (-3 V), 3.7 mW (0 V, multimode), Ith 26 mA, 0.141 W/A, 800 um
  gain section. Not entered: Si3N4 loss 0.32 dB/cm (ref. [10]), spectrum FWHM 1.5 nm and RF linewidth 40 kHz (no parameter),
  10 kOhm isolation. Fab empty (no statement for the feedback chip; gain chip purchased from EXALOS AG).
- mitchell2026 (5 / 24): Southampton / Sheffield QCL bar flip-chip on Ge-on-Si: end-fire interface (45 % / 3.5 dB best,
  26 %, 20-27 %, 3.5 % at bar edge, 12.9 % device_total; all author_estimate: calculated Fresnel loss + equal-facet
  assumption; taper 1 mm to 11 um); GOS rib 8.6 dB/cm cutback; 90 deg bend 0.38 dB and 9.8 dB/cm at R 0.2 mm; integrated QCL
  bar (20-30 mW and ~1 mW in-waveguide estimates, 24 lasers, 500 um pitch); 3 mm epi-up FP QCL (> 65 mW CW at 15 C, ~55 deg
  FWHM divergence, ~4.5 um ridge, 6 um trenches). facility_org_ids org_uk_national_epitaxy_facility on both QCL rows (epi grown
  there, p.4; borderline vs wafer-supplier note). Platform `inp` for the QCLs assumed from InGaAs/AlInAs (substrate not
  printed); GOS rows platform `other`. Not entered: threshold current density 0.963 kA/cm2 (no parameter), bonder accuracy.
- mangal2018 (3 / 12): imec downward GC with Ti/Al reflector (~3.3 dB best near 1325 nm, read off Fig. 4(a); 490 nm,
  FF 0.5, 2 um top oxide), standard GC (~2.5 dB near 1300 nm bare, ~9 dB after packaging, Fig. 4(a)), through-substrate
  Ormocer microlens interface (micro_optics.other: 1-dB lateral tolerance ~13 um at z = 0 and ~15.5 um at z = 600-1000 um
  with a 0.2 NA MMF from Fig. 5(a); ROC 150 um measured / 145 um designed; height 8 um). fab_org_ids org_imec on both GCs
  ("fabricated in imec's 200 mm ... pilot line"). Not entered: collimation > 600 um (no parameter), fiber-scan 1/e2 widths
  (convolution with the MMF), FDTD chief-ray angle 4.06 deg.
- morenopozas2025 (1 / 10): Malaga parabolic TIR spot-size converter x570 on Applied Nanotools 220 nm SOI (fab
  org_applied_nanotools): IL 0.23 dB at 1550 nm and < 0.35 dB over 1260-1640 nm (back-to-back pair minus reference, halved:
  per_component, derived), BW1dB > 380 nm, 2.5D FDTD 0.3 dB, MFD "up to 200 um" (author_estimate), geometry. Judgment: class
  micro_optics.other (integrated reflective beam expander); mode_converter.converter is the alternative but disallows
  mfd_chip_um. Not entered: offset-flavor degradations (relative), simulated trade-offs.

## EO-atlas candidates (not entered here, D168 practice)

cheung2022 MOSCAP devices (p.3, p.5): Al2O3 MZI (350 um, ER ~24 dB, 1.69 nm at 2 V, FSR 17.9 nm, VpiL 0.370 V-cm
calculated, f3dB ~1.5 GHz), HfO2/Al2O3 MZI (ER ~30 dB, 2.26 nm at 2 V, FSR 19.0 nm, VpiL 0.294 V-cm), MOSCAP microring
modulator R 10 um (Q 8250, kappa 0.0494, round-trip loss 13 cm-1, 73.6 pm/C, f3dB ~15 GHz, ER ~5.7 dB at 25 Gb/s,
~1.1 V-cm).

## Orgs missing from the registry

- EXALOS AG (winkler2024 p.2 Sec. 2): vendor of the purchased GaAs gain chip; would be fab_org_ids only on a gain-chip row
  (none entered).

## Registry gaps (skipped values)

| gap | skipped value, locator | proposed definition |
|---|---|---|
| bw_3db_ghz / bw_fwhm_ghz for reflector | huang2019 grating 2.9 GHz (p.4), 3.3 / 5.0 GHz (p.4 Fig. 4(b)), ~4 GHz (p.5) | reflection-band full width in frequency at -3 dB / FWHM as stated |
| bw_fwhm_nm for laser | winkler2024 mode-locked spectrum FWHM ~1.5 nm (p.4) | optical spectrum FWHM of a comb / mode-locked laser |
| rf_linewidth_khz (laser) | winkler2024 40 kHz FWHM, Lorentzian 11 kHz (p.4); jafarlou2026 precedent | width of the fundamental repetition-rate RF beat note (level / fit in condition) |
| frequency_noise_hz2_per_hz (laser) | huang2019 < 350 / < 170 Hz2/Hz (p.6) | white frequency-noise level (Lorentzian linewidth = pi x value) |
| threshold_current_density_ka_per_cm2 (laser) | mitchell2026 0.963 kA/cm2 (p.4); ramirez2022 1.65 kA/cm2 (p.5, in condition) | threshold current per pumped area |
| collimation_length_um (micro_optics, free_space_emitter) | mangal2018 > 600 um (p.3) | axial range over which the beam width stays within the stated criterion |
| placement_error_um (chip_chip_coupler) | tanaka2012 mean 0.10 um, sigma 0.37 um, n = 17 (p.6) | post-bond lateral offset of flip-chip / die placement (statistic in statistic) |
| taper_length_um for amplifier | tanaka2012 RSOA SSC 150 um (p.5) | allow the existing parameter for SOA spot-size converters |
| back_reflection_db for waveguide_platform | cheung2022 45 deg III-V/Si interface < -60 dB simulated (p.4); repeats lit_11 | as for couplers |
