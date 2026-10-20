---
title: Fresh-context audits of component batches bf_07-bf_12, bt_01-bt_05, pk_oi, ofc_pilot, ofc_01-ofc_09
date: 2026-10-20
mode: 8 read-only subagents (shared contract; patches validated on private copies of data/); condensed by the coordinator. Patches applied as data/_staging/components/<batch>/patch.yaml, batches re-merged with --replace (0 component errors each)
---

# Component audits, second wave (2026-10-20)

| audit | metrics ok / wrong / imprecise | components ok / wrong / imprecise | misses added |
|---|---|---|---|
| bf_07-09 (193 metrics, 60 components) | 137 / 21 / 35 | 48 / 0 / 12 | 25 |
| bf_10-12 (99, 48) | 81 / 0 / 18 | 35 / 1 / 12 | 15 (+4 components) |
| bt_01-05 (96, 49) | 85 / 0 / 11 | 41 / 1 / 7 | 8 |
| pk_oi (103, 32) | 89 / 5 / 9 | 22 / 0 / 10 | 0 |
| ofc_pilot + ofc_01 (203, 61) | 192 / 0 / 11 | 42 / 0 / 19 | 16 |
| ofc_02-04 (205, 47) | 193 / 0 / 12 | 40 / 0 / 7 | 2 |
| ofc_05-07 (206, 52) | 197 / 0 / 9 | 50 / 0 / 2 | 1 |
| ofc_08-09 (103, 31) | 93 / 0 / 10 | 25 / 0 / 6 | 5 |

Wrong values: bf_07 21 rows stored the intrinsic loss rate kappa_0 as linewidth_mhz (repointed to kappa_intrinsic_mhz, D73); pk_oi 4 locators in the wrong section (00230) and one design-target loss row (00052-m8). Wrong components: bf_10 zhu2022 fab (all fabricators HyperLight, p.6); bt_01 okuda2026 fab org without a fabrication statement. No other wrong numbers in any OFC batch.

Main imprecision classes, now patched: basis of per-coupler / per-facet values and platform claims of unstated origin (author_estimate, D44 / D76); loss from Q with ng not stated (author_estimate); transition scope (per_component); D72 own-org fab where the paper states who fabricated (Furukawa, UC Berkeley, Harvard, EPFL, KIT, imec, Corning, AIST, Columbia, HyperLight); time-correct Stanford facilities (celik2022, witmer2020 -> SNSF + SNF); new-org fab / facility ids (SITRI, Tower, UBC SBQMI, UCSB Nanofab, Marvell Nanolab, Davis CNM, SUSTech, Alphion, AIM TAP); Tu2D.4 PD subtype (not stated -> other); W3E.3 NTT fab removed (D80b); Tu2J.4 -> wdm.other (D81).

Coordinator rulings on the optional blocks and open questions: DevLog-002 D80 (basis of authors' arithmetic, D72 strictness, grant / program acknowledgements, time-aware facilities, row_kind, fiber-only scope, on-chip mirror couplers, ge_waveguide subtype, citation sentences, self-heating), D81 (registry extension) and D82 (design-stated performance, supplement locators, facility owners, conversions, platform inheritance, SSC platform, repetition rate vs spacing). Not applied: the bf_07 21 GHz map repoint (inference), the steckler2025 bias-sweep figure readings, the ofc_09 M1D.5 fiber-ring comb (not integrated), the ARIM facility proposals (D80c, reverted on M4D.3), the ofc_01 "developed" own-org fab block, ofc_04 W3F.5 deletion (kept as author_estimate with a note), Th1K.2 / W4E.4 optional misses, the eltes2020 300 K point (pending the EO-atlas fix).

Cross-batch items handed to the convention sweep (scratchpad brief): remaining transition scopes, Q-derived loss bases, design_target on performance values, row_kind, platforms (luan2026 soi_slot, SiON SSCs, xu2022), comb repetition rates, didier2026 IBM facility, D72 strictness on earlier rows, Corning fan-out cross-notes.

EO-atlas follow-ups (report only): eltes2020-a / -c carry the 300 K loss with temperature_k 4 (4 K value 5.4 +/- 0.3 dB/cm, Supp. Fig. S1(b)); holzgrafe2020 and the gaier2025 comb racetrack have no EO rows. PK-atlas follow-ups: 00048-b-o1 coupling loss (text "approaching 1.5 dB"), 00072-a-o1/o2 mfd_chip_um 0.35 is the in-PIC mode, 00229-b-o1/o2 wavelength 1310 for O-band averages, 00014-a-o1 qualifier vs "typical", 00012 Table V 2.39 vs text 2.40, ectc51529.2024.00093-c-m1 missing test_standard (P2 audit #17).

Incidents: the bf_10-12 auditor wrote two stray patch files into the repo root through a broken shell chain and deleted them at once; the P3 audit wrote two temp pickles into the repo root and moved them out (both verified absent).

## Third wave (2026-10-20 15:00)

- pk_02 audit (25 components / 59 metrics): metrics 58 ok / 0 wrong / 1 imprecise, components 21 ok / 4 imprecise. Applied: 00324 AIST fab ("we can easily fabricate", p.3, borderline D80b), 00106 notes (stale org note, OFC Th1D.3 cross-notes, the "4 dB/cm" vs Fig. 6 inconsistency), pk_oi addendum (00023 Corning fab emptied: passive fabrication; stale cross-notes); coordinator: pk_oi 00227 imec fab emptied ("co-designed and fabricated", passive). Not applied: optional Fig. 5 / Fig. 20 readings, TSMC CI row_kind block.
- Audit 3 of the convention sweep and the D81 gap-fill: sweep 84 row ops (128 field changes) 79 ok / 0 wrong / 5 imprecise; gap-fill 66 rows + 1 component 65 ok / 1 imprecise (Th3F.4 m15 bias -2.5 V added); missed by the sweep: liu2023 mode-demux loss excess_loss_db -> insertion_loss_db (D76); 43 notes fixed (29 stale "no parameter" / contradicting fab notes after D81 and the sweep). Rulings D84.
