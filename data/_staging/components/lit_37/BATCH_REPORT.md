# Batch lit_37 report (distill subagent, 2026-10-29)

Dry-run `batch lit_37: +29 components, +154 metrics; errors 0` (one WARN printed for lit_* ni2025b, not this batch). ASCII, no
e-mail, no addresses, no quotes beyond a few words. Builder script: scratchpad `distill_lit_37/build.py`.

## Per paper (components / metrics)

- gelerkremer2022 (0 / 0): the cached text and PDF are the 1-page Author Correction (doi 10.1038/s41566-022-01041-8, p.1), not
  the paper. Nothing entered; the source needs a re-fetch.
- zhang2019 (2 / 7): GSS4T1 strip on a 400 nm LPCVD SiN racetrack, laser-switched non-volatile resonant switch, as
  resonator.ring (fang2021 ring-switch precedent; no on-chip actuator, so no phase_shifter row): CR 42 dB, IL < 0.5 dB (scope
  unspecified), amorphous-state ER 33-44 dB over 4 cycles (Fig. 5(d), extracted), geometry. GST-225 reference ring: amorphous
  about 44 dB, crystalline about 9.5 dB (Fig. 5(e), extracted). Wavelengths from the figure axes (inferred). Fab org_mit +
  org_mit_lincoln_laboratory (contributions p.12-13: MIT and Lincoln Laboratory co-authors fabricated, D80b); facilities MTL +
  Harvard CNS (p.12). Not entered: free-space electrothermal GSS4T1 reflective pixel (24 -> 34 % reflection at 1550 nm, 1 us /
  24 V / 5.5 uJ amorphization, 42.5 mJ crystallization, > 1000 cycles; no class), material FOM / n / k, CR 12 dB / IL 2.5 dB of
  prior switches (cited).
- ding2019 (5 / 17): graphene-plasmonic slot PDs L = 2.7 / 3.5 / 9 / 19 um (photodetector.graphene, plasmonic_mim, one row per
  length, rule 9): responsivity (on_chip, w.r.t. slot power; 26 and 360 mA/W derived from mA/W, 50 / 245 mA/W read from Fig.
  3(A)), EQE 2 / 29 % (derived), zero-bias 1.3 mA/W, bw3db > 110 GHz (2.7 um text; 3.5 / 9 um figure; 19 um from Table 1 /
  summary), absorber length. Graphene-loaded plasmonic slot waveguide: 0.8 dB/um cut-back (8000 dB/cm derived) and ~1 dB/um
  (author_estimate, Supplementary not cached). Wavelength not stated anywhere: C band inferred. Not entered: system-limited
  impulse-response bandwidths (85 / 75 GHz), 1.5-dB bandwidth 110 GHz (19 um; registry gap), eye diagrams, transit-time estimate
  520 GHz, Table 1 values of other works. Fab / facility empty (passive fabrication, DTU / SDU / HUST authors).
- huang2014 (8 / 44): IME Si3N4-on-SOI BEOL multilayer. 600 nm PECVD SiN waveguide (3.5 / 0.8 / 0.24 dB/cm at 1550 / 1580 /
  1270 nm, < 0.45 dB/cm 1270-1330 nm); 400 nm PECVD and LPCVD SiN and 220 nm Si waveguides (Table 1, all three wavelengths);
  SiN inverse-taper edge coupler 1.4 TE / 1.5 TM dB per facet (band unspecified); Si-SiN transition coupler Lo = 50 um (< 0.2
  dB at 1550, 1530-1600 and 1270-1330 nm, tips 200 / 300 nm, tapers 50 um, spacer 100 nm design / 115 nm ellipsometry) and Lo =
  0 um (about 2 dB, Fig. 4(d)); TiN-heated Si ring R 20 um (Q > 30000, mean IL < 1 dB, 0.11 nm/mW -> 110 pm/mW derived). Fab
  org_astar_ime (borderline, see calls). Not entered: Lo = 10 / 30 um points (Fig. 4(c) only), simulated < 0.25 dB for Lo > 20
  um (family), Table 2 values of other works.
- li2026b (6 / 18): LTOI (x-cut congruent LiTaO3 400 nm). Loss ring: Qi 6.50-7.72 x 10^6 (n = 5, Fig. 1(g)), 0.05-0.06 dB/cm
  (author_estimate, ng not stated). Ferroelectric non-volatile phase shifters (phase_shifter.ferroelectric_nonvolatile): 1 mm
  single-arm MZI shifter (1.1 pi at 127.5 V, 8 levels, one-week retention, 10^6 cycles, width 2 um, etch 240 nm), 2 mm
  four-section weighted electrode (137 positions across pi as n_levels, phase range 1 pi), MZM bias electrodes and MZM
  balancing interferometer (80 h retention each, derived). Ring with 1 mm tuning region: 0.138 nm non-volatile shift (Fig. 2(j)).
  Page 9 Table 1 read from the render (garbled layer). Not entered: thermo-optic P_pi 55 mW of the authors' earlier LTOI devices
  (D259); 0.0026 pi shortest-segment increment (ambiguous device, D159); delta n model estimates; programming voltage / energy /
  100-ms tuning time (gaps); MZM metrics (EO 3-dB about 110 GHz at Q, 103 GHz on chip before packaging, VpiL 3.1 V cm, ER 35.9 ->
  59.3 dB at 1553 nm, 200 / 240 Gbit/s OOK, 400 Gbit/s PAM-4: EO-atlas candidates); edge-detection system metrics (3.48 TOPS/W).
  Fab / facility empty (see orgs).
- sia2022 (5 / 50): CompoundTek 200 mm C-band platform (fab org_compoundtek, p.2-3). Si rib W 450 / strip W 450 / strip W 500
  waveguides (Table I median / mean / std, single-die 0.41 and 0.59 dB/cm, width, 90 nm rib slab from the Fig. 1(b) label, BOX,
  bend radius 15 um); focusing GC (IL mean 4.31 / median 4.29 / std 0.13 dB per coupler, period 630 nm, duty 0.5, 70 nm etch);
  Ge waveguide PD 4 x 10 um x 500 nm (bw3db median / mean / std at 1, 2, 3 V from Table IV and text, single die 43 GHz,
  responsivity 0.835 / 0.837 / 0.05 A/W at 3 V, ref_plane unspecified). Wavelength C band inferred throughout. Not entered:
  dark current 2.58 / 2.79 / 0.86 nA (bias not stated with the value; bias required); MZM and microring modulator metrics
  (median 38.5 / 43 GHz, VpiL 1.6 / 1.85 V cm, MZM IL 2.94 / 3.18 / 0.33 dB, FSR 5.69 / 9.69 nm: EO-atlas candidates); die
  counts (wafer maps only).
- singaravelu2019 (3 / 18): two-tier Si taper Si-to-SiN vertical SSC (waveguide_platform.transition): 180 nm interlayer row
  0.058 dB at 1525 nm (cut-back), mean 0.298 / std 0.092 dB over 1520-1620 nm, full geometry; 246 / 303 nm interlayer siblings
  about 0.26 / 0.38 dB (Fig. 3(c), band unspecified). Not entered: Si rib 1.9 dB/cm, SiN 0.8 dB/cm and facet 7 dB from the same
  run reported in ref. [16] (D259); taper-length / tip-width spectra (no per-coupler values); simulated curves; Table 1 blank in
  the render. Fab / facility empty (Cork IT / Tyndall / St Andrews / CEA-Leti, passive fabrication).

## Orgs missing from the registry

- MIT Materials Research Laboratory (zhang2019 p.12, characterization facility support).
- Advanced Micro-Nano Fabrication Center of Huazhong University of Science and Technology (li2026b p.20, facility support).

## Judgment calls

- zhang2019 fab = MIT + MIT Lincoln Laboratory (D80b; Lincoln is an MIT child org); same fab / facility on the GST reference.
- ding2019 L = 19 um bw3db_ghz > 110 entered from Table 1 / summary although the text gives a 1.5-dB bandwidth of 110 GHz;
  zero-bias responsivity entered with bias_v 0 per text / caption (inset label prints VB = 0.1 V); slot absorption as a
  waveguide_platform.straight prop_loss row.
- huang2014 fab org_astar_ime: all authors IME, conclusion states the paper presents the fabrication, 'our scanner' (D84a
  borderline). 400 nm SiN rows from the authors' earlier runs entered as own data (no reference cited). SiN width 1 um is
  stated with the simulation (derived, noted). Heated ring as resonator.ring (platform test device, not a WDM path).
- li2026b endurance (10^6) put on the 1 mm single-arm MZI row (Sec. 2.2, cycling device not separately identified); 137 phase
  positions entered as n_levels with the authors' "not digitally addressable" caveat in condition; MZM-embedded non-volatile
  electrodes entered as phase_shifter rows holding retention only.
- sia2022 GC IL scoped per_coupler as stated (isolation method not stated).

## Registry gaps

- gap_nm (or slot_width_nm) for photodetector: plasmonic slot / MSM electrode gap, ding2019 120 nm (p.2). Proposed: "electrode or
  plasmonic slot gap of a PD".
- bw_1p5db_ghz (or a generic bandwidth-at-stated-level parameter) for photodetector: ding2019 L = 19 um 1.5-dB optical bandwidth
  110 GHz (p.3). Proposed: "electrical / optical response bandwidth at the drop level given in condition".
- programming_energy_uj and programming_voltage_v for phase_shifter: li2026b set 2.6 uJ / reset 3.06 uJ (p.9 Table 1),
  switching from 100 V, full reversal 127.5 V (p.6). Proposed: "write / erase energy per programming event" and "write voltage
  as stated". (Switching energy was deferred in D81; these are new skipped values.)
- electrode_gap_um for phase_shifter (non-thermal actuators): li2026b 6 um (p.6). Proposed: "gap between the actuating electrodes".
- phase_step_pi for phase_shifter: li2026b average step about 0.007 pi (p.8). Proposed: "smallest / average programmable phase
  increment".
- Class for free-space reflective modulators / pixels (e.g. free_space_emitter.other or a new class): zhang2019 GSS4T1 pixel
  reflection 24 -> 34 % at 1550 nm, 1000+ cycles, switching energies (p.9-12).
