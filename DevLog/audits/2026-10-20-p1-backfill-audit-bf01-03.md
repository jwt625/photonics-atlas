---
title: Fresh-context audit of component back-fill batches bf_01-bf_03
date: 2026-10-20
mode: read-only subagent; condensed by the coordinator; the auditor's patch blocks are applied as data/_staging/components/bf_0{1,2,3}/patch.yaml
---

# Back-fill audit bf_01-bf_03 (2026-10-20)

Scope: 52 component rows, 127 metric rows (staging = merged, byte-identical); every metric at its locator; figure values checked on the images; host ids, physical devices and org ids machine-checked; 7 papers read end to end, all others at key sections, 0-row papers grepped.

| | ok | wrong | imprecise |
|---|---|---|---|
| metrics (127) | 116 | 4 | 7 |
| components (52) | 36 | 3 | 13 (11 = v3 fab rule) |

Wrong: kohli2023 three components with BRNC facility from operations-team thanks (D72); boynton2020 simulated 5.96 dB rests on a cited 1.28 dB propagation term (author_estimate); guo2026 sidewall 60 deg x2 and li2025a w0 600 nm duplicate linked EO geometry columns.
Imprecise: boynton2020 scope note; kohli2023 converter method (loss breakdown, not cutback); lu2020 polarization TM x2; taghavi2026 GC basis (origin not stated); taghavi2026 PWB class (v3 subtype); porto2026 NF temperature; li2025a stale class note; v3 fab rule for university self-fabrication (kim2025, liu2023, luan2026a).
Misses: none under v2; v3 back-fill possible: kawahara2025 TiN heater (new component), liu2023 SLSR and reflectivity, montifiore2026 linewidths, porto2026 RIN, shamsansari2021 gap.

Cross-batch conventions raised (coordinator rulings in DevLog-002 D76): transition scope (per_interface vs per_component), basis of Q-derived loss, converter loss parameter, D72 for universities, supplement locator form, model-fit basis, FSR of unstated origin.
