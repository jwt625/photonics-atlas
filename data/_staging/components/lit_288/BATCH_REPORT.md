# lit_288 batch report

Papers: lit:komljenovic2015a, lit:duan2014, lit:komljenovic2018, lit:martin2018. Contract: SKILL.md v4-v7, DevLog-007
rulings through D780. verified_on 2026-11-26. Validation: `merge_component_staging.py data/_staging/components/lit_288
--dry-run` -> +20 components, +114 metrics, 0 errors (the 2 warnings are on merged rows of other papers).

Page-1 title check: all four cached texts match their source rows (komljenovic2015a JLT 34(1) tutorial review;
duan2014 JSTQE 20(4) invited paper; komljenovic2018 Proc. IEEE 106(12); martin2018 JLT 36(19) invited paper).

| paper | components | metrics |
|---|---|---|
| komljenovic2015a | 0 | 0 |
| duan2014 | 15 | 94 |
| komljenovic2018 | 0 | 0 |
| martin2018 | 5 | 20 |

## komljenovic2015a (tutorial review, 0 rows)

Review with no own results in this paper. Every device value carries a reference number in its sentence, paragraph or
caption, including the authors' own UCSB devices (rule 3, D259 / D408): e.g. Si / Si3N4 loss and 0.4-0.8 dB transitions
[34]-[38]; PSR [45]; ring tuning 20 nm [48]; athermal rings [51], [53]; QD lasers [6], [8]; broadband LED [55];
mode-locked laser [56]; short-cavity DFB [57]; microring lasers [14], [58]; EAM array [59]; LEAP laser [12]; 2 um
lasers [64]; MUTC photodiodes [61]; beam-steering PIC [65]; high-Q laser and 1.1 M Si resonator [91]-[93];
CRR / Vernier lasers [31], [78], [79]; monolithic external-cavity laser incl. 0.67 dB/cm at 1310 nm, 10 % / 60 % loop
mirrors, 54 nm tuning (Sec. VI-C paragraph and Fig. 23 cite [36]); hybrid butt-coupled laser [35]. Equations and
measurement-technique tutorial carry no device values.

## komljenovic2018 (Proc. IEEE overview, 0 rows)

Overview with no own results in this paper. All values are credited to references: DFB / tunable / mode-locked lasers,
SOAs, modulators, photodetectors [21]-[62]; microwave generator [64]; gyroscope driver [66]; beam scanner [69];
network-on-chip [73]; isolators [93]-[99] (incl. 32 dB, 20 dB over 18 nm); circulators [102], [103] (14.4 dB,
400 ps, 28 dB). Not entered: "We have demonstrated up to 105 C lasing" (p.2, the authors' earlier work restated
without a device in this paper; rule 3) and the generic "insertion loss typically 7-10 dB" of integrated isolators
(p.9, no device).

## duan2014 (invited summary of the authors' recent work, 15 components / 94 metrics)

Components: hybrid III-V/Si DBR laser + back / front Si Bragg mirrors; widely tunable double-ring laser + rings R1 /
R2 (test samples) + Bragg reflectors + vertical grating coupler; 5-channel AWG laser + intracavity AWG + R1 / R2
reflectors + vertical grating coupler; ITLMZ ring-filtered laser + NiCr ring heater.

Not entered and why:
- Introduction sentences that attribute values to the authors' earlier papers (rule 3, D259): ref. [11] tuning over
  45 nm and SMSR over 40 dB (p.2); refs. [15], [16] 5-channel 392 GHz and 4-channel 200 GHz AWG lasers, thresholds
  38-42 mA, fiber power -8.4 to -2.2 dBm (p.2); ref. [18] ITLMZ 9 nm tunability, ER 6-10 dB, 13 GHz (p.2); ref. [22]
  10 Gb/s direct modulation and 100 Gb/s coherent LO use (p.6); BER sentence cites [18] (p.9).
- Silicon MZM of the ITLMZ (3 mm, VpiLpi about 3 V cm, ER over 10 dB / 6.5 dB, about 13 dB intrinsic loss, over
  13 GHz bandwidth, FSR about 4.5 nm, p.9): modulator metrics, EO-atlas territory (rule 2). EO-atlas candidate.
- Double adiabatic taper (Sec. II-B, Fig. 4): simulated curves only, no printed number besides tip widths 0.4 / 0.8 /
  1 um and taper length about 30 um (geometry-only, not a row); calculated MQW confinement 5-12 %.
- Fig. 9 marker 7.22 GHz (not tied to one bias curve, D156; text "around 7 GHz" entered).
- Conclusion family statements kept in DBR-laser notes only (D254): slope efficiency 0.1-0.15 mW/mA for the 400 um
  hybrid lasers, thermal impedance about 120 K/W for 400 um devices, about 20 K rise at 100 mA (p.10).
- Differential quantum efficiencies 13.3 % (DBR), about 8 % (tunable), about 5 % (AWG): no registry parameter.
- 6 dB output-power variation across the tuning range (p.6): power_uniformity_db is defined across channels / ports.
- Laser-model result (4 dB intracavity AWG loss -> 20-30 % lower external efficiency, p.6): calculation, no device.

Fab / facility: none. Fabrication is passive ("The fabrication starts with 200 mm SOI wafers", p.2) and the authors
span III-V Lab, CEA-Leti, Ghent University-IMEC, University of Southampton and Bell Labs (D80b, D154). No
acknowledgment section. No missing org.

Judgment calls (auditor):
1. D408 body vs introduction: the paper "summarizes our recent advances". Body sentences, figures and Table I cite
   nothing and are entered (boller2019 precedent: uncited measurement sentences kept, citation only on the
   introductory / record sentence). Three body values equal values the introduction attributes to refs. [11] / [15]:
   tunable-laser tuning_range_nm > 45 and smsr_db > 40 (m6, m7), AWG-laser channel_spacing_ghz 392 (m22) and the
   Table I thresholds 38-42 mA (m1-m5). If the auditor reads the introduction attribution as covering the whole
   section (ahmadi2022 / subramanian2012 direction), delete those rows; the ITLMZ body values differ from [18]
   (8 nm vs 9 nm) and look new.
2. Ring R1 / R2 FSRs 650 / 590 GHz stated in the design section -> author_estimate (D82a); Fig. 11 shows the measured
   combs but no printed measured FSR.
3. Directly stated coupler / AWG properties without a method (AWG-laser GC peak about 1560 nm, 45 nm 3 dB passband;
   AWG 190 GHz 3 dB bandwidth; AWG loss 2.5-6 dB "in our samples") -> measured (D167 analogue). The 18 GHz FP mode
   spacing -> author_estimate (could be computed from cavity length).
4. ITLMZ on-chip powers (2.5 / 6.5 / > 1 mW) -> author_estimate (referencing to the Si waveguide not explained);
   6.5 and > 1 mW plane `unspecified`.
5. DBR-laser front-mirror powers -> derived (fiber power + insertion loss measured on a same-wafer reference
   structure, D80a).
6. Ring heater as phase_shifter.thermo_optic (heater_resistance_ohm is not allowed on resonator); the ring itself has
   no other value, so no resonator row for the ITLMZ ring.
7. Mirror reflectivity wavelength: DBR mirrors take the 1546.97 nm lasing wavelength, tunable-laser reflectors C band,
   AWG-laser reflectors 1513-1525 nm, all `wavelength_inferred`.
8. Subtypes: DBR, AWG and ITLMZ lasers `laser.heterogeneous` (ferrotti2016 precedent), double-ring laser
   `laser.tunable`; platform `other` for the lasers (fang2006 / ferrotti2016), `soi` for the passive Si parts (rib vs
   strip of each part not stated).

## martin2018 (own system demonstration, 5 components / 20 metrics)

Components: shallow-etched shunt waveguide (power handling), grating coupler, balanced photodiode pair, folded
doped-Si thermo-optic phase shifter, 1x8 MZI switch tree.

Not entered and why:
- System-level LiDAR results (60 m range, 5 mW emitted, 20 mW out for 200 mW in, 28 cm resolution, SNR): no
  component parameter.
- "20 mW for their deep etched counterparts" (p.4): comparison device, context of ref. [15], not this chip.
- 8 cm spiral delay line (1 ns), 75/25 and 10/90 directional couplers, 170 um DLI phase shifter: design values only, no
  measured performance (not rows).
- Commercial DFB laser (Gooch and Housego series) and fiber circulators: setup / off-chip parts (rule 13).
- No wavelength is printed anywhere; every wavelength-conditioned row is `band: unspecified` with a note (rule 8).
- Heater length: the 120 um three-waveguide section is not stated as the heater length (not entered).

Fab / facility: fab org_imec on all 5 rows ("fabricated within IMEC's (Belgium) silicon photonics full platform
(ISIPP25G) on 200 mm SOI wafers", p.2), process_name "imec silicon photonics full platform (ISIPP25G), 200 mm SOI".
Fiber attach by Tyndall Institute (org_tyndall_national_institute exists) is an assembly step, note only. No facility.
No missing org.

Judgment calls (auditor):
9. Grating-coupler row rests on one implied value: insertion_loss_db 3 per_coupler `author_estimate`, the difference of
   the printed 22 dBm fiber input and "19 dBm at waveguide input" (also 25 vs 22 dBm). Delete the row if implied
   loss-budget terms are not to be entered.
10. Shunt waveguide power handling: 22 dBm fiber-side 1-dB compression `measured` (chung2017 precedent), 19 dBm at the
    waveguide input `author_estimate` (unstated coupling term), 25 dBm 3-dB compression `author_estimate`
    (extrapolated, D435).
11. Photodiode subtype `photodetector.other` (absorber not named), platform `soi`, responsivity `ref_plane: on_chip`
    (Fig. 2 axis "optical power on photodiode"; referencing method not stated). Fig. 2 annotation 8.4 mA entered as
    saturation_photocurrent_ma `measured` (figure annotation, churaev2023 practice).
12. One switch row for SN1 and SN2 (both 1x8 cascaded 2x2 MZI trees; identical design not stated); crosstalk > 30 dB
    measured on SN2, the 2.3 dB loss sentence is plural. Subtype switch_fabric.other (D158).
13. p_pi_mw 20 derived by halving the printed 40 mW per 2 pi (abediasl2015 precedent); 40 mW kept as tuning_power_mw.

## Registry gaps

- `differential_quantum_efficiency_pct` (laser): duan2014 DBR 13.3 % at 20 C (p.4 Sec. III-B), tunable about 8 %
  (p.5 Sec. IV-C), AWG about 5 % (p.7 Sec. V-B). Proposed definition: external differential quantum efficiency,
  derivative of the L-I curve times e / h nu, reference plane in ref_plane.
- `power_uniformity_db` widened to a tunable laser's output-power variation across its tuning range (duan2014 6 dB,
  p.6 Sec. IV-C), or a separate parameter; skipped for now.
