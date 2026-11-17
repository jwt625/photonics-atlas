# lit_170 batch report

Distilled 2026-11-16 under the pic-component-distill skill (Contracts v4-v7). Papers: lit:fard2016, lit:yang2024b,
lit:chen2016c, lit:isti2025, lit:patel2014 (bench-citation selection: only what each paper itself reports).
Totals: 20 components, 152 metric rows. `merge_component_staging.py --dry-run`: +20 components, +152 metrics,
0 errors (the one warning printed belongs to merged row cmp_lit_ni2025b_pimmwc, not this batch).

Page-1 title check: all five cached texts are their source rows' papers (fard2016 Optics Express 24(24) 27738;
yang2024b Optics Express 32(26) 47184; chen2016c JLT 35(4) 722, published 2017 issue, online 2016; isti2025 PTL 37(19)
1101; patel2014 OIC 2014 paper TuD5). No correction / erratum, no garbled text layer. Values read from text and
checked against page renders where tables / figures were used (fard2016 Table 3 p.13, Fig. 8 p.8; yang2024b Figs. 2-4
and 6; chen2016c Fig. 7; isti2025 Figs. 1-4, Table I; patel2014 Fig. 1).

## lit:fard2016 - 10 components, 88 metric rows

| component | class | metrics |
|---|---|---|
| cmp_lit_fard2016_pd01_8x8_1c (PD-A, reference) | photodetector.ge_waveguide | 11 |
| cmp_lit_fard2016_pd02_8x8_2c1p6 (PD-B) | photodetector.ge_waveguide | 10 |
| cmp_lit_fard2016_pd03_8x8_2c2 | photodetector.ge_waveguide | 8 |
| cmp_lit_fard2016_pd04_8p5x8_2c2p7 | photodetector.ge_waveguide | 8 |
| cmp_lit_fard2016_pd05_8x10_2c2 | photodetector.ge_waveguide | 8 |
| cmp_lit_fard2016_pd06_8x15_1c | photodetector.ge_waveguide | 8 |
| cmp_lit_fard2016_pd07_8x15_2c1p6 | photodetector.ge_waveguide | 7 |
| cmp_lit_fard2016_pd08_8x20_1c (PD-C) | photodetector.ge_waveguide | 10 |
| cmp_lit_fard2016_pd09_8x20_2c1p6 (PD-D, optimized) | photodetector.ge_waveguide | 11 |
| cmp_lit_fard2016_pd10_8x25_1c | photodetector.ge_waveguide | 7 |

- Per device (Table 3, PD-A..D also Table 2): dark current at -2 V (uA -> nA, derived), responsivity at 1550 nm
  (`on_chip`, GC loss measured on adjacent connected GCs, `reference_structure`), 3-dB bandwidth at -2 V without and
  with the integrated peaking inductor, W_Ge / L_Ge (`absorber_width_um` / `absorber_length_um`), Ge 500 nm, Si
  220 nm (Fig. 8(b) label). Table 2 adds -4 V dark current and bandwidth for PD-A..D.
- PD-A: simulated small-signal bandwidth 45 GHz (Fig. 9(a)); R_PD 215 ohm and PD-D R_PD 87 ohm (Table 1) as
  `author_estimate` (estimated from foundry sheet / contact resistances).
- Fab `org_astar_ime` ("fabricated at the Institute of Microelectronics IME-A*Star", p.8). CMC thanked for
  "contribution and technical support" only: not a fab org (fard2017 precedent). process_name empty (only "a foundry
  PDK" is named). Platform `soi` (Fig. 8(b) shows BOX and 220 nm Si).

Not entered: junction capacitances 12.2 / 35.2 fF (Table 1; computed from a capacitance per area reported in ref. [9],
rule 3 / D611); transit-time bandwidth ~60 GHz (computed from a cited saturation velocity); simulated responsivity /
dark-current / bandwidth curves of Figs. 3, 4, 6(b), 13 and the 30.1 / 45.2 GHz design numbers (design studies of
non-fabricated variants, 360 pH optimum not fabricated); simulated 1.01 A/W (not tied to one design, D156); 19 % / 1 %
metal-loss responsivity penalties (simulation, no parameter); BER sensitivity improvements (3.2 / 1.9 / 0.6 / 0.7 /
2.8 dB, no parameter; in notes); inductor 540 pH, 87 x 85 um (electrical part, notes); n-doped Ge and contact
dimensions (no parameter, notes).

Judgment calls:
- One row per Ge / contact design (10 rows); the with-inductor version is a condition on the bandwidth rows, not a
  separate row (Table 3 prints one dark current and one responsivity per number). The unlabelled first bandwidth
  column of Table 3 is read as "without inductor" (p.14: largest bandwidth without inductor 35 GHz, no. 1).
- Responsivity rows carry no bias: Tables 2 / 3 print none, and the text pairs PD-A 0.66 A/W with both 2 V (p.3)
  and 4 V (p.12).
- Bandwidth rows: LCA wavelength not stated; 1550 nm with `wavelength_inferred` (responsivity and BER at 1550 nm).

## lit:yang2024b - 5 components, 30 metric rows

| component | class | metrics |
|---|---|---|
| cmp_lit_yang2024b_mzi_switch | switch_fabric.other | 9 |
| cmp_lit_yang2024b_spiral_tops | phase_shifter.thermo_optic | 11 |
| cmp_lit_yang2024b_mmi_2x2 | splitter.mmi | 3 |
| cmp_lit_yang2024b_euler_bend_w400 | waveguide_platform.bend | 3 |
| cmp_lit_yang2024b_euler_bend_w550 | waveguide_platform.bend | 4 |

- Switch: P_pi ~1.4 mW (1550 nm), ER > 28 dB over the C band, maxima 39 / 41 dB (bar / cross), crosstalk > 40 dB
  (printed < -40 dB), IL < 1.4 dB, rise / fall ~24 / ~25 us, footprint 240 x 360 um2 (derived).
- TOPS: simulated P_pi ~1.3 mW (N = 5), heater ~1.3 kOhm (calculated), 1.16 dB loss-budget share, heater 3 um x
  1300 um x 200 nm TiW, cladding 2.2 um, widths 400 / 550 nm, spiral length 9.16 mm, footprint ~0.11 x 0.11 mm2.
- MMI: excess loss 0.12 dB per MMI (half of ~0.24 dB for two, loss budget).
- Bends: simulated hybrid Euler 90-degree bend loss at R_eff 6 um, rho 0.4 (0.0025 / 0.0021 dB at 1550 nm, 550 nm
  < 0.005 dB over 1520-1580 nm), radius and width.
- Fab `org_beijing_university_of_posts_and_telecommunications` ("We fabricate the device", all authors at BUPT).

Not entered: Table 1 "This work" BW 40 nm (BW not defined by the table; Fig. 6(b) shows ER > 28 dB over
1525-1565 nm); Table 1 rows of other works (rule 3); bend losses at R_eff 3 / 9 um (design studies not on the chip);
arc-bend comparison curves; Fig. 2(b) P_pi for N other than 5; SOI thickness / etch depth / MMI dimensions (in the
uncached Supplement 1); waveguide pitch 1 um, heater centre distance 6 um and centre taper 10 um (no phase_shifter
parameter; notes).

Judgment calls:
- Switch IL < 1.4 dB `author_estimate`, scope `de_embedded`, method `unspecified`: the GC normalization is described
  only in the uncached Supplement 1 (D428 / D583). MMI and phase-shifter shares `author_estimate` + `loss_breakdown`
  (origin not stated); the TOPS share scope `unspecified` (the paper says "the phase shifters", not per arm).
- Measured P_pi / ER / crosstalk / times stay on the switch row (merged switch precedents); the TOPS row holds the
  simulated P_pi and the heater design.

## lit:chen2016c - 2 components, 9 metric rows

| component | class | metrics |
|---|---|---|
| cmp_lit_chen2016c_si_lpin_gepd_20um | photodetector.ge_waveguide | 8 |
| cmp_lit_chen2016c_gc_cband | fiber_chip_coupler.grating | 1 |

- 20 um Si-LPIN GePD: 0.92 A/W at 1550 nm, -1 V (measured); Fig. 7 end points ~1.02 A/W at 1530 nm and ~0.72 A/W at
  1570 nm (figure reads, +/- 0.02 A/W); Ge 160 nm x 0.5 um x 20 um, Si 220 nm, 450 nm input wire.
- C-band GC: 2.5 dB per coupler, `author_estimate` (printed in parentheses, no measurement shown).
- Fab `org_imec` ("fabricated in imec's fully integrated Si Photonics Platform", D455), process_name as printed (same
  string as merged lit:chen2016a). Staff thanks to imec's mask team / process line: no facility.

Not entered (D259 / D259a, rule 3): every value of the 14 um device. 0.74 A/W, 4 nA, 67 GHz at -1 V and 6.8 fF are
restated from the authors' ref. [16] = lit:chen2016a (p.1, p.5); Fig. 3 (bandwidth vs power, incl. ~59 GHz at
0.62 mW and "60 GHz and above") is "reproduced with permission from [16]"; "beyond 67 GHz at -2 V" (p.4) is the
same statement already merged as cmp_lit_chen2016a_si_lpin_gepd_ge160-m2. The 14 um device therefore has no new
performance metric here and no row (its 80 / 100 Gbps eye diagrams have no parameter). Also not entered: eye-diagram
jitter / height readouts and transmitted-data extinction ratios (setup / link quantities), poly-Si taper geometry
(no photodetector parameter; in core_material).

Judgment calls: responsivity `ref_plane: unspecified` (the paper does not say how the coupler loss was removed;
the data experiments quote waveguide-coupled power). GC fab `org_imec` from the same sentence ("along with ...
various passive devices"), noted on the row.

## lit:isti2025 - 1 component, 7 metric rows

| component | class | metrics |
|---|---|---|
| cmp_lit_isti2025_bto_ridge_wg | waveguide_platform.straight | 7 |

- Propagation loss 0.7 dB/cm (OBR / OFDR, `statistic: best` for "as low as", average of the high-quality waveguide;
  no wavelength stated: `band: unspecified`), BTO 147.3 nm (TEM label), etch 150 nm, sidewall 37 deg (SEM / AFM),
  BOX 3 um, width 2.28 um (SEM label, derived), length ~3.5 cm (derived).

Not entered: RMS sidewall roughness within 2.5 nm (no parameter: `rms_roughness_nm` candidate, D432), simulated
single-mode cut-off ~1.9 um, the zero-loss 1-cm window of Fig. 4(b), medium-quality waveguide (no printed value),
ellipsometry n / k, etch rates, Table I values of other works (rule 3).

Judgment calls (flag for the auditor):
- Platform `bto_on_oxide_substrate`: the text says BTO "on a Silicon-on-insulator (SOI) platform", but Fig. 1(a)
  TEM and Fig. 2(a) show BTO / 3.9 nm STO directly on 3 um SiO2 on Si, no Si device layer (kim2025 / mohl2025
  precedents). Alternative: `bto_on_si` if the coordinator reads the text literally.
- Width 2.28 um from the Fig. 3(a) SEM label: top vs base not stated (a 210 nm label marks the sloped edge).
- Etch depth 150 nm `design_target` (the SEM / AFM sentence confirms the sidewall angle; no height value printed).
- Fab empty: first-person etch work ("We varied the RF bias") by authors at the University of Delaware and Phase
  Sensitive Innovations, site not stated (D154). Facility empty: UDNF named in the funding / support line ("in part
  by the Staff at Phase Sensitive Innovation (PSI) and the University of Delaware Nanofabrication Facility (UDNF)"),
  borderline D80c, org missing from the registry.

## lit:patel2014 - 2 components, 18 metric rows

| component | class | metrics |
|---|---|---|
| cmp_lit_patel2014_mzi_2x2_switch | switch_fabric.other | 10 |
| cmp_lit_patel2014_doped_si_heater_ps | phase_shifter.thermo_optic | 8 |

- Switch building block: ER 18 dB (state 1) / 42 dB (state 2) at 1550 nm, 1.8 dB output imbalance as
  `il_nonuniformity_db`, rise / fall 4.4 / 5.0 us, power 16 / 41 mW for state 1 / 2 (`power_consumption_w`,
  derived), length 220 um, 2 x 2 ports.
- Phase shifter: equivalent resistance ~298 ohm (eight segments in parallel, Fig. 5 I-V), 2.4 kOhm per segment
  (`author_estimate`, "estimated"), resistor 25 um x 1 um, 0.8 um from the rib, rib 0.5 um (Fig. 1 label, derived),
  220 nm core, 90 nm slab.
- Fab `org_astar_ime` + `org_cmc_microsystems` ("fabricated by ... IME A*STAR ... with the multi-project wafer
  service organized by ... CMC", D83d / D398); process_name from the printed MPW wording.

Not entered: the 4x4 crossbar (not yet characterized, p.1); drive 0.64 Vpp on 2.7 V bias (not a V_pi: the paper
gives it as the switching drive; in condition / notes); grating couplers and rib directional couplers (no values);
the Si thermo-optic coefficient (cited material constant).

Judgment calls: the tested element is the standalone 2x2 building block (Fig. 2 labels a separate "2x2 switch"
next to the crossbar; Fig. 5 "a 2x2 switch block"): `switch_fabric.other` (D158), not `mzi_mesh`. The 1.8 dB
"imbalance" between the switch outputs goes to `il_nonuniformity_db` (imbalance_db is splitter-only); the paper
attributes part of it to fibre-array alignment (condition / notes). Platform `soi_rib` (deep-etched rib with 90 nm
slab stated).

## Missing fab / facility orgs (check done in organizations.csv / org_aliases.csv)

- "University of Delaware Nanofabrication Facility (UDNF)" - facility (borderline, D80c), lit:isti2025 p.1 (funding /
  support line); also missing for merged lit:xiao2022 (D417). Parent `org_university_of_delaware` exists.

All other orgs used exist: org_astar_ime, org_cmc_microsystems, org_imec,
org_beijing_university_of_posts_and_telecommunications. Supplier noted only: La Luce Cristallina, Inc.
(lit:isti2025 p.1; `org_la_luce_cristallina` exists, not a fab org per D428).

## Registry gaps

- `rms_roughness_nm` (waveguide_platform): isti2025 sidewall RMS roughness within 2.5 nm (AFM), p.2 Sec. IV;
  already a candidate (D432 / D434). Proposed definition: RMS sidewall (or surface, stated) roughness from AFM / SEM.
- `xt_bandwidth_nm` or a switch operating-bandwidth parameter with a definition column: yang2024b Table 1 "BW 40 nm"
  (p.7), not entered because the table does not define BW.
- `heater_resistance_ohm` on switch_fabric (D440 candidate): not needed here (separate phase-shifter rows).
- `data_rate_gbps` (D534 candidate): fard2016 30 Gb/s BER, chen2016c 80 / 100 Gbps RZ reception.
