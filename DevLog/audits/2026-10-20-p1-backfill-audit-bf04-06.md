---
title: Fresh-context audit of component back-fill batches bf_04-bf_06
date: 2026-10-20
mode: read-only subagent; condensed by the coordinator; the auditor's patch blocks (incl. optional Block B D72 own-org fab per D76, Block C gupta2023 kappa) are applied as data/_staging/components/bf_0{4,5,6}/patch.yaml
---

# Back-fill audit bf_04-bf_06 (2026-10-20)

Scope: 49 component rows, 93 metric rows (staging = merged before patching); every metric at its locator; figure values checked on the images (xu2020 Fig. 2(a) P_pi, aihara2026 Fig. 2(a) SMSR / wavelength); host ids, physical-device siblings, org ids, parameters, units and EO-column duplicates machine-checked (0 errors); 7 papers read end to end, the 6 no-row papers scanned.

| | ok | wrong | imprecise |
|---|---|---|---|
| metrics (93) | 82 | 2 | 9 |
| components (49) | 43 | 0 | 6 |

Wrong: lin2026a MMI 3.25 / 3.11 dB entered as insertion_loss_db including the 3 dB split (D43) -> excess_loss_db 0.24 (derived) / 0.10 (simulated).
Imprecise: powell2024 split ratio basis (author_estimate, assumed identical couplers) and radius from diameter (derived); bf_05 per-coupler / per-facet values of unstated origin (schwarzenberger2026a, xu2020, wang2024a, wang2022, witmer2020) -> author_estimate, aligned with bf_04 / bf_06; niels2026 MMI value covers both MMIs (C1 + C2 = 3.8 dB PDK part), fab org_imec (pilot line); witmer2020 SNSF / SNF facility -> org_nano_stanford (celik2022 precedent); shen2026 subtypes (laser.tunable, laser.heterogeneous); wang2025 reference GC polarization te.
Misses (now entered): shawon2024 TO-switch heater thermal time constant ~15 us (new component); hu2026a il_nonuniformity_db 1.36 dB; witmer2020 bw_fwhm_nm ~40 nm; saxena2023 251 pm/mW and 15 us; aihara2026 laser electrical power 93 mW; gupta2023 HHI grating kappa 550 / 100 1/cm (process-level, author_estimate).
D72 own-org fab (D76): powell2024 x3 and renaud2023 (Harvard), niels2026 transition (imec + Ghent), wang2024a (EPFL), lin2026a x3 (Ghent).

Cross-batch conventions raised for the D76 sweep / a later ruling: platform of SiON SSCs (lnoi_rib in li2026aa vs sion in hu2026a / wu2022); whether `derived` means arithmetic by the batch or also a difference / cascade result stated by the authors (measured in schwarzenberger2026a, niels2026, kohli2025, valdez2022; derived in hu2026a, li2026aa, li2022b, vanackere2023); two possibly overlapping HUST WNLO facility orgs; CNCD (wang2022a p.4) missing from the registry.

After patching, bf_04-06 re-merged with --replace: bf_04 14 / 30, bf_05 21 / 46, bf_06 17 / 25 (components / metrics), 0 errors.
