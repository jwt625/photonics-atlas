---
title: Distillation of the cached literature corpus (`lit`) into the component atlas
date: 2026-10-22
status: in progress
scope: DevLog-006 S8 (distill batches + audits) for the papers cached by S7
authors: Claude (at Wentao Jiang's request)
---

# DevLog-007: `lit` corpus distillation (S8)

Decisions here are D150-D169 and D250-D259 (incl. D256a, D259a). Session-wide stream plan and decision ranges: [DevLog-000](DevLog-000-plan.md)
Progress, 2026-10-22 22:00.

## Request (2026-10-22, Wentao)

"go ahead with your TODOs. Delegate to subagents accordingly." This DevLog covers the S8 item of DevLog-006.

## Decisions

| # | Decision | Rationale |
|---|---|---|
| D150 | Batches of 8-12 cached `lit` papers grouped by class family (one subagent each, contract `BATCH_INSTRUCTIONS.md` + its `lit` addendum), then one fresh-context audit per batch with a replayable `patch.yaml` (D50), then merge with `merge_component_staging.py` | DevLog-002 workflow; pilot discipline already done on 600+ components |
| D151 | Validator: `lit:` metric locators must start with `p.N` (page of `references/<id>/text.md`) | same as `eo:`; the lit text has page markers |
| D152 | Registry: `fiber_chip_coupler.other` added now (D138); InP-native waveguide PDs stay `photodetector.other` until batches show enough rows for a subtype | D138 |
| D154 | (lit_03 audit) Fabrication stated by authors who all sit in sub-units of one parent (CEA-Leti + CEA-IRIG): fab_org_ids = the parent (`org_cea`), not a sub-unit chosen from outside knowledge; authors spread over unrelated orgs stay empty (qi2024) | D72 "unambiguous own org" |
| D155 | (lit_03 audit) Discrete fiber-coupled detector chips measured at the module input are in scope (`ref_plane module`), e.g. qi2024 InGaAs SPAD; amplitude-only phase-change memories stay `phase_shifter.phase_change` with a note until a variable-attenuator class is justified by more rows | audit questions 2-3 |
| D156 | Figure labels that cannot be tied to a curve unambiguously are not entered even when one of them is plausible (song2021 Fig. 3(e)) | never invent |
| D157 | (lit_02 audit) A pure unit rescaling of a printed dimension is `derived` with the printed value in notes (D82d / D111 stand); merged rows that kept `design_target` / `measured` after a rescale (e.g. boynton2020 vertical coupler m3) are fixed by a convention sweep over `data/components/` (follow-up) | consistency with D82d |
| D158 | A single 1x2 / 2x2 MZI switch element is `switch_fabric.other`; `mzi_mesh` only for NxN meshes or a cell characterized as part of one | mu2026; earlier rows split both ways |
| D159 | A value whose sample identity is ambiguous between two components (dangel2013 VIS-NIR bound: flex or rigid) is not entered on either; the bound goes into component notes | never invent |
| D160 | `patch_component_staging.py` gains `delete_components` (drops the component and its metric rows, logged); used for setup equipment entered as a component (djogo2026 MCF fanout probe, skill rule 13) | audit lit_04 |
| D161 | Foundry-stack / own-wafer layer thicknesses are `design_target` (skill rule 4), not `specification`; `specification` stays for vendor datasheet values | 113 merged precedent rows |
| D162 | `fill_factor` is kept as printed with the paper's definition in notes (mehta2016 gap fraction) until the convention sweep fixes one definition (tooth fraction) for all rows | registry def "duty cycle" is ambiguous |
| D163 | Loopback-pair bandwidths measured through a packaged path stay on the GC row with the path in condition (djogo2026 m3 / m4); fs-laser-written waveguide loss with a calculated coupling term stays author_estimate; zhang2021 platforms stay per guiding stack (D47) | audit lit_04 questions 5-7 |
| D164 | Per-crossing loss is `crossing_loss_db` (all crossing rows); the `mmi` layout template's primary metric for `crossing.mmi` changes to `crossing_loss_db` in the registry extension | audit lit_05 Q1 |
| D165 | Array-level rows (values regressed over a family of devices, e.g. xu2022 cavity series) stay as one component row with the population in notes / n_samples; a physical device used for its coupling ratio stays `splitter.directional_coupler` even when it converts modes (xu2022 asymmetric TE0-TE1 coupler) | audit lit_05 Q3-Q4 |
| D166 | Internal / on-chip amplifier gain and NF computed from the source's own measured fiber-to-fiber value and its own measured losses are `derived` (D80a, class-wide) | audit lit_01 Q1 |
| D167 | A per-facet coupling loss stated directly without shown arithmetic is `measured` (shi2024) | audit lit_01 Q8 |
| D168 | Kept until the registry extension: mckenna2022 SHG racetrack as resonator.ring and OPO as laser.other (reclass to frequency_converter once it allows Q / FSR / threshold / efficiency); song2025a routers as circulators (nonreciprocal.other to be added); starnault2026 platform empty (etch not stated, never defaulted from the foundry). starnault2026 MZM metrics (Vpi 2.25 / 2.5 V, EO bandwidth 102 vs 104 GHz) are an EO-atlas candidate, listed here for that atlas | audit lit_01 Q4-Q7 |
| D169 | (registry extension after lit_01-lit_06; DevLog-002 D81 rule: only gaps with a confirmed skipped value and an unambiguous definition) New parameters: photodetector dark_count_rate_hz, afterpulse_probability_pct, timing_jitter_ps, max_count_rate_mhz, recovery_time_ns, critical_current_ua, excess_noise_factor, dark_current_density_ma_per_cm2 (bias required); series_resistance_ohm (photodetector, laser); phase_shifter endurance_cycles, n_levels; amplifier gain_db_per_cm, gain_bandwidth_nm (criterion in condition); power_conversion_efficiency_pct (amplifier, frequency_converter); frequency_converter conversion_efficiency_pct_per_w_cm2; laser thermal_resistance_k_per_w, characteristic_temperature_k; nonreciprocal isolation_bw_nm; free_space_emitter steering_range_deg, steering_efficiency_deg_per_nm; fiber_interface mdl_db; waveguide_platform dgd_ps; splitter coupling_angle_deg (geometry); resonator q_external; wdm bw_fwhm_ghz, drop_efficiency_pct; switch_fabric bw_0p5db_ghz, xt_bandwidth_nm. Widened: pdl_db (+waveguide_platform, crossing), wdl_db (+crossing), per_db (+waveguide_platform), gap_nm (+crossing, switch_fabric), crosstalk_db (+nonreciprocal), q_loaded / q_intrinsic / fsr_ghz / pump_threshold_mw / thermal_drift_pm_per_k (+frequency_converter), fsr_nm (+laser: mode spacing or intracavity-filter FSR, which in condition), extinction_db (+phase_shifter, mode_converter), capacitance_ff (+phase_shifter), period_nm / n_periods / bw_10db_nm / coupling_length_um (+mode_converter), pitch_um / n_channels / slsr_db (+free_space_emitter), taper_length_um (+wdm), bw_3db_ghz (+switch_fabric). Subtype nonreciprocal.other. Platform values gap_on_insulator, iii_v_on_si_epi. Registry 161 -> 189 parameters (28 new) | audit "registry gaps confirmed" sections lit_01-lit_06 |
| D250 | (registry extension, rejected / deferred) Detector gate width (setting of the gating circuit, qi2024); per-length phase-shifter loss / extinction in dB/um (two different quantities, oz2023 / meng2023); laser emission FWHM limited by OSA resolution (mu2026, not a device property); laser q_loaded / q_intrinsic (the only value, mckenna2022 OPO, moved to frequency_converter); poling_period for resonator / laser (same); amplifier input dynamic range and gain temperature coefficient (single values, definition varies); dispersion beta2 (D81 stands); photon-pair metrics and modulator metrics (not confirmed / EO atlas); 3-dB / 0.5-dB tolerances, feedback tolerance (D77 / D81 stand); facet angle, pitch for waveguide_platform, min_bend_radius for chip_chip_coupler / amplifier, tol_1db for transitions (single or simulated values, audit lit_02 did not re-propose); wdl_db for waveguide_platform (zhang2021 +/- bound ambiguous vs max-min); bw_* for crossings (simulated only); Raman efficiency (not confirmed); resonator bw_fwhm_ghz / drop_efficiency_pct and wdm q_external, mdl_db for mode_converter (no skipped value; resonator widths stay linewidth_mhz) | never add a parameter without a value |
| D251 | D164 implemented as `primary_by_class: {crossing.mmi: {parameter: crossing_loss_db, scope: per_component, better: lower}}` on the `mmi` template (splitter.mmi keeps excess_loss_db); test checks the override parameter and class. The app reads only `template.primary` (`app/src/lib/layout/resolve.ts` primaryMetric, `routes/layout/+page.svelte` lines with `t.primary` / `r.template.primary`): the app owner must read the override; new platform values also need a family in `app/src/lib/explore/colors.ts` (not edited here, app/ owned by another agent) | D164 |
| D252 | Reclasses in the gap-fill (D168 closed): mckenna2022 SHG racetrack -> frequency_converter.shg, OPO -> frequency_converter.other; song2025a four-port and 5x5 routers -> nonreciprocal.other (three-port circulator stays); platforms kuznetsov2025 (4) and wilson2019 (5) -> gap_on_insulator, song2021 (9, InP-on-Si template grown on V-grooved Si) -> iii_v_on_si_epi | D47, D168 |
| D253 | fill_factor = tooth (unetched) width / period (registry definition fixed). A paper that defines the gap fraction is converted (1 - x, derived, printed value and definition in notes: mehta2016); a percentage stored as a fraction is a unit conversion (derived, D157); papers that do not define their duty cycle keep the printed value with a note (guo2026, li2022b, qiao2017, jahed2022); 0.5 values need no note | D162 |
| D254 | (gap-fill rulings) A "typical" value stated once for a family of sibling components is not entered on one representative row (hosseini2015 MZI ER 25 dB stays a note; D159 extended); a gap-fill may add a sibling component row when the text ties a newly allowed value to a design without a row (meng2023 double-heater cell: endurance; single heater-pair cell: 6 levels; D81 precedent); virot2014 F = 5.24 kept with the gain as printed ("at both M = 1 and M = 10", flagged); brisson2023 200 MHz maximum count rate is the incident photon flux the paper calls maximum count rate (condition says so); an I-V-slope differential resistance enters series_resistance_ohm with the method in notes (zhang2023, lu2024); subagent extras accepted where the text states them (yue2026 theta_y range, prost2022 / kim2019 calculated ranges and SLSR as simulated, kim2019 125-element SLSR from Table I, lu2024 design mode spacing, huang2019a 66 C width, song2025a simulated crosstalk, starnault2026 O-band isolation window 65 nm derived) | gap-fill reports |
| D255 | Convention sweep 2 (`sweep2.yaml` per batch, replay order patch, sweep, gapfill, addendum, geometry, geoaudit, coord, sweep2): D157 candidates found mechanically over all 37 batches (dimension parameters plus mfd / beam sizes, non-derived, non-simulated basis; value absent in the stored unit anywhere in the source text, present in another length unit), each verified at its locator from text snippets; excluded where a figure label prints the stored unit (guo2026 x4) or the printed unit is unknown (wang2026 Table II image). 104 rows without alt-unit evidence (tables, figure labels, "10 x 10 um" forms) are unchanged. Simulated rows stay simulated (D83f) | D157, D162 |
| D256 | (ext audit Q1, Q3) D82d applies to every unit or prefix conversion (kHz -> Hz, mW <-> W, THz -> GHz), not only dimensions; a row keeps its basis only when the source prints the stored-unit form for the same quantity somewhere (text, table, figure label; cite that locator), otherwise `derived` with the printed value in notes. Sweep 3 verifies the 26 open candidates under this rule | [audit](audits/2026-10-22-registry-ext-gapfill-sweep-audit.md) |
| D257 | (Q2) guo2026 GC fill factor: the Fig. 2(b) sketch puts rho over the etched groove, so rho is the gap fraction: store 0.3 (tooth fraction, D253) `derived` | audit Q2 |
| D258 | (Q4) `series_resistance_ohm` also allowed for amplifier (zhang2023 SOA 10 ohm); `fsr_nm` / `fsr_ghz` definitions state which quantity goes in condition; `gap_nm` definition updated for crossing / switch_fabric; dc template gains `coupling_angle_deg` | audit part 1 |
| D259 | (Q5) Values the authors restate from their own earlier paper are cited values (skill rule 3 / D80i) and are removed (zhang2023 WTL1) | audit Q5 |
| D256a | Rows already `author_estimate` keep that basis after a unit / prefix conversion, with the printed value and the conversion in notes (20 rows in sweep 3); no sweep | coordinator ruling on the ext-audit application |
| D259a | D259 applied strictly to zhang2023: every value from figures / statements the paper reproduces from the authors' own earlier work is removed (ref. [29] ECTC 2022: Fig. 5 SOA I-V incl. the 10 ohm row and gain / gain spectra, Fig. 6 switch; ref. [32] OFC 2022 transmitter: WTL1, printing-site taper coupling); a component left without a performance metric is deleted (D49). `lit_01/extaudit2.yaml`: SOA, MZI switch and taper components deleted (9 metric rows); lit:zhang2023 now has no component rows | coordinator ruling |
| D153 | Distill batches also enter the stated layout geometry (D102 role-specific parameters) so new rows can feed the layout viewer and showcase selection | dedicated component papers state geometry; avoids a second geometry pass |

## Batches (64 papers cached on day 1)

| batch | classes | papers |
|---|---|---|
| lit_01 | amplifier, frequency_converter, nonreciprocal | garciablanco2025 zhang2023 ronn2019 kuznetsov2025 li2025 vazquezcordova2014 zhang2023a mckenna2022 shi2024 cheng2025 song2025a starnault2026 |
| lit_02 | laser, chip_chip_coupler, micro_optics, polymer waveguides | heim2025 lu2024 mu2026 liang2025 maeda2023 billah2018 jahed2022 mangal2020 suda2025 dangel2013 |
| lit_03 | photodetector, phase_shifter, LWIR platform | brisson2023 hu2023 qi2024 virot2014 song2021 wang2022a hosseini2015 meng2023 oz2023 mourgelas2021 |
| lit_04 | fiber_chip_coupler, fiber_interface, free_space_emitter, GaP platform | sulway2023 zhang2021 jia2017 djogo2026 shikama2017 yue2026 mehta2016 prost2022 kim2019 wilson2019 |
| lit_05 | crossing, splitter, mode_converter, reflector, resonator | nan2025 bock2010 nevlacsil2020 wang2026 elsaeed2024 sheng2012 xu2023a huang2019a qi2025 jayatilleka2021 xu2022 song2021a |
| lit_06 | wdm, switch_fabric, SiN foundry platform | deng2026 fu2023 bogaerts2006 fujisawa2020 papadovasilakis2023a qiao2017 tanizawa2015 iwama2015 nakamura2020 ye2023 |
| lit_07 | amplifier, frequency_converter, nonreciprocal, reflector | liu2022 riemensberger2022 tao2024 akin2024 lu2020 suntsov2021 white2024 yan2024 zhang2017 liu2018 |
| lit_08 | laser, chip_chip_coupler, micro_optics, free_space_emitter | jafarlou2026 keyvaninia2013 koninck2025 nie2024 tran2022 vaskasi2022 sun2011 yu2023 zhang2024a fowler2025 |
| lit_09 | phase_shifter, photodetector, waveguide_platform | baghdadi2021 cheung2023 dong2021 murray2015 seo2025 alexander2026 flory2020 nozaki2016 tossoun2019 ding2022 |
| lit_10 | resonator, splitter, mode_converter | ashida2017 gao2021 jeong2013 radulaski2018 suk2025 wang2021 camus2020 nikbakht2022 zhang2013a yu2025 |
| lit_11 | crossing, fiber_chip_coupler, fiber_interface, switch_fabric, waveguide_platform, wdm | ni2025a shen2019 zaoui2014 ma2026 nauriyal2023 seok2019 song2008 suzuki2025 huang2026 shamsansari2022 davis2020 deng2026a |

Later retrieval days (DevLog-006 S7) add batches lit_07+ as papers are cached. Day 2 (2026-10-23): lit_07-lit_11 (52 papers).

## TODO

- [x] Plan, validator rule (D151), registry subtype (D152), contract addendum.
- [x] lit_01-lit_06 distill (subagents), dry-run 0 errors each.
- [x] Fresh-context audit per batch -> `patch.yaml`; apply; merge; validate_db; views rebuild.
- [x] Registry extension (gaps from all six batch reports + audits), gap-fill per batch (`gapfill.yaml`), convention sweep over `data/components/` (D157 unit rescale, D162 fill_factor), template primary for crossings (D164).
- [x] Org round 5: missing fab / facility orgs from the batch reports, then `coord2.yaml` fab assignments per batch (DevLog-001 round 5 entry, D277; applied and merged 23:15-23:17).
- [x] Ext audit corrections (D256-D259) as `extaudit.yaml` and convention sweep 3 (D256) as `extaudit.yaml` / `sweep3.yaml`; replay order patch, sweep, gapfill, addendum, geometry, geoaudit, coord, sweep2, coord2, extaudit, sweep3, extaudit2 (lit_01, D259a).
- [ ] Batches for papers cached on later retrieval days.

## Progress

- 2026-10-22 22:00 PDT: plan written; lit_01-lit_06 dispatched.
- 22:15 PDT: distill done for all 6 batches (dry-run 0 errors each): lit_01 47 / 237, lit_02 33 / 221, lit_03 30 / 165,
  lit_04 42 / 199, lit_05 47 / 297, lit_06 57 / 312 (components / metrics); reports transcribed to each
  `BATCH_REPORT.md`; audits dispatched per batch.
- 22:17: lit_03 audit ([record](audits/2026-10-22-lit_03-audit.md)): 165 metrics 162 ok / 3 imprecise / 0 wrong,
  2 misses added; 30 components ok. `patch.yaml` + `coord.yaml` (D154) applied, merged: 585 components / 2144
  metric rows in `data/components/`. Registry gaps from all batches collected for one registry extension after the
  audits.
- 22:24: audits lit_02 (221 metrics: 186 ok / 34 imprecise / 1 wrong, 10 misses; [record](audits/2026-10-22-lit_02-audit.md)),
  lit_04 (199: 160 / 37 / 2, 10 misses, 1 setup component deleted; [record](audits/2026-10-22-lit_04-audit.md)),
  lit_06 (312: 304 / 8 / 0, 10 misses; [record](audits/2026-10-22-lit_06-audit.md)) applied with `patch.yaml` + `coord.yaml`
  (D157-D163) and merged: 715 components / 2902 metric rows. Open: Qaleido Photonics (ye2023 fab) and the other missing
  fab / facility orgs go to the next org round, then a coord patch per batch with `--replace`.
- 22:27: audit lit_05 (297 metrics: 279 ok / 18 imprecise / 0 wrong, 6 misses; 4 component fixes;
  [record](audits/2026-10-22-lit_05-audit.md)) applied and merged (D164-D165).
- 22:34: audit lit_01 (237 metrics: 175 ok / 62 imprecise / 0 wrong, 15 misses; 4 components wrong fab (ronn2019 Aalto
  emptied); [record](audits/2026-10-22-lit_01-audit.md)) applied with D166-D168 and merged. All six batches merged:
  809 components / 3457 metric rows.
- 22:39-23:05: registry extension D169 (28 new parameters, 22 parameters widened by 25 class allowances, nonreciprocal.other, platforms
  gap_on_insulator / iii_v_on_si_epi; rejected / deferred D250); D164 as `primary_by_class` on the `mmi` template (D251,
  app wiring left to the app owner). Gap-fill (6 subagents, every value re-read at its locator) as `gapfill.yaml` per lit
  batch: lit_01 +35 metrics (mckenna2022 -> frequency_converter, song2025a routers -> nonreciprocal.other, kuznetsov2025
  GaP-on-insulator), lit_02 +17, lit_03 +24 and 2 sibling components (meng2023; song2021 iii_v_on_si_epi; coordinator
  dropped hosseini2015 ER row, D254), lit_04 +24 (wilson2019 GaP-on-insulator), lit_05 +18, lit_06 +14: 132 metric rows,
  2 components. Convention sweep 2 (D255) as `sweep2.yaml` in 28 batches: 110 D157 unit-rescale basis fixes + 6 fill_factor
  ops (mehta2016 gap fraction converted, D253). Dry-run 0 errors for all 29 affected batches, merged with `--replace`:
  811 components / 3589 metric rows; staging and merged tables in sync; validate_db 0 errors, ruff / mypy / pytest
  (261 passed) clean. Views not rebuilt (another agent owns build_views.py / app/static/data). Backup before the pass:
  session scratchpad `backup-2026-10-22-pre-registry-ext.zip`. Open: fresh-context audit of the gap-fill + sweep2 rows.
- 23:25: fresh audit of the registry extension / gap-fill / sweep2 ([record](audits/2026-10-22-registry-ext-gapfill-sweep-audit.md)):
  parameters 28/28 ok; gap-fill 132 rows 117 ok / 15 imprecise / 0 wrong; sweep2 116 ops 101 ok / 1 imprecise / 14
  wrong (song2021 x12, guo2026 x2 reverted); 3 sweep misses; proposed `extaudit.yaml` (55 ops, 14 batches). Rulings
  D256-D259; application + sweep 3 queued after org round 5 finishes re-merging the lit batches.
- 23:30-23:50: ext audit applied (D256-D259). Staging == merged for all 37 batches before the run (coord2 dry-run 0
  changes in lit_01-06). Registry (D258): `series_resistance_ohm` +amplifier; `fsr_nm` / `fsr_ghz` defs say which
  cavity / filter / resonator / mode family goes in condition; `gap_nm` def names multilevel crossings and switch DC gaps;
  `dc` layout template optional list +`coupling_angle_deg` (the app reads template lists generically, but the dc scene
  in `app/src/lib/layout/scene.ts` still draws a straight coupling section: app owner to draw the angle). Files:
  `extaudit.yaml` in the 14 audit batches (audit blocks resolved per rulings, "pending" wording dropped, plus lit_01:
  zhang2023 SOA series_resistance_ohm m5 = 10 ohm and notes, D259 delete of the WTL1 component with its 8 rows,
  mckenna2022 SHG fsr_ghz condition per D258) and `sweep3.yaml` in 10 batches without an extaudit (bf_03, bf_04, bf_07,
  bt_01, bt_02, ofc_01, ofc_04, ofc_07, ofc_09, ofc_pilot); sweep 3 ops of batches with an extaudit sit in that file.
  88 ops (59 audit / ruling ops + 29 sweep 3 ops), 187 field changes, every patch re-run 0 changes, merge dry-run 0
  errors for all 24 batches, merged with `--replace`. `merge --replace` does not drop a component deleted from staging,
  so the WTL1 component and its 8 metric rows were removed from `data/components` by id first (scratch script, same
  CSV writer). Result: 810 components / 3584 metric rows (-1 / -8 WTL1, +1 zhang2023 m5, +2 lit_05 gap-fill misses
  huang2019a bw_10db_nm m17, bock2010 wdl_db m3); staging == merged; validate_db 0 errors; ruff / mypy clean; pytest
  298 passed. Backup: session scratchpad `backup-2026-10-22-pre-extaudit.zip` (data/components + 24 staging dirs).
  Sweep 3 (D256): mechanical scan of all non-geometry, non-derived, non-simulated rows (value absent in the stored unit,
  present in another unit of the same family: frequency, power, dB/length, time, current, capacitance, wavelength,
  pm/mW, pm/K, resistance; plus dBm <-> mW and % <-> fraction, no hits) gave 50 candidates (the audit's 32 plus range /
  table forms) and 1 row with the stored unit on another page; each read at the locator (text, OFC pdftotext; renders
  for powell2024 Fig. 3 and okuda2026 Fig. 2). 30 measured / specification rows -> derived (6 in the audit blocks, 24
  new: holzgrafe2020, billah2018 m5 / m6, lu2024 m13 / m20, okuda2026, powell2024 ring, shamsansari2021, OFC M1G.3,
  M4D.5, Th1F.6, Th1H.1 x4, Th2A.7, Tu3C.1, W2A.11 x2, W3E.3 x3, W4E.2, W4E.5); heim2025 ECTL ILW kept measured (Fig.
  2(e) caption prints 1750 Hz; locator cites it); 20 author_estimate rows keep their basis with the printed value and
  conversion in notes (ext audit Q1 proposal; precedent cai2025 / powell2024a / wang2024b / hu2023 / wolf2018a), 4 of
  them needed the printed value added (mohl2025 m3 / m5, Th1K.2, saxena2023). Open for the coordinator: (1) D256 read
  literally would also make those 20 author_estimate rows derived (one-line sweep if so ruled); (2) D259 consistency:
  zhang2023 Fig. 5 (SOA I-V incl. the new 10 ohm, gain spectra) and Fig. 6 (switch) are also reproduced from the
  authors' ECTC 2022 paper (ref. [29]), and the iii_v_si_taper m1 (> 90 % coupling, p.10) describes the [32]
  transmitter; applied as instructed (10 ohm added, only WTL1 removed).
- 23:50: D256a / D259a. `lit_01/extaudit2.yaml` (3 delete_components, 12 changes, re-run 0) deletes the zhang2023 SOA
  (gain m1, bw m2 / m3, series_resistance m5 from Fig. 5 of ref. [29]; length m4 geometry), MZI switch (crosstalk m1,
  Fig. 6 of ref. [29]) and III-V/Si taper (coupling m1 from the ref. [32] transmitter; taper length m2 / gap m3 geometry)
  components; removed from `data/components` by id first (as WTL1), lit_01 merged with `--replace` (dry-run 0 errors).
  Result: 807 components / 3575 metric rows; open question (1) of the 23:30 entry closed by D256a (no sweep), (2) by
  D259a. Backup: session scratchpad `backup-2026-10-22-pre-extaudit2.zip`.
- 2026-10-23 01:50 PDT: day-2 batches distilled (dry-run 0 errors each, reports condensed into each `BATCH_REPORT.md`):
  lit_07 44 / 205, lit_08 36 / 246, lit_09 77 / 423, lit_10 32 / 216, lit_11 52 / 386 (components / metrics). Not
  audited or merged: paused by the owner after this step. Next: one fresh-context audit per batch, coordinator rulings,
  merge, then a registry extension for the gaps listed in the five reports.
