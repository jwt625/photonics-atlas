# Literature prefilter statistics (DevLog-006 S2)

Generated 2026-10-22 by `scripts/lit_prefilter.py` from `cache/literature/pool/*.jsonl` (git-ignored). Counts only.
Re-run over the growing pool rewrites this file.

## Pool by lane (raw records)

| lane | pool files | raw records |
|---|---|---|
| arxiv | 212 | 40594 |
| conferences | 89 | 49295 |
| journals | 291 | 131871 |
| seeds | 23 | 11641 |
| total | 615 | 233401 |

## Merge

| step | n |
|---|---|
| raw records | 233401 |
| unreadable lines skipped | 0 |
| dropped type editorial | 3 |
| dropped type erratum | 9 |
| dropped type letter | 31 |
| dropped type paratext | 13 |
| works after merge | 215863 |
| duplicate records merged | 17482 |
| works with more than one record | 15195 |
| of which across lanes | 12574 |
| of which preprint + published version | 9657 |

## Known-id exclusion (work already in a local corpus; a work can be in several)

| corpus | index entries | works matched |
|---|---|---|
| eo_candidates | 461 | 369 |
| eo_papers | 233 | 184 |
| ofc2026 | 830 | 19 |
| pk_cache_list | 300 | 17 |
| pk_papers | 296 | 17 |
| sources:blog | 128 | 6 |
| sources:eo | 233 | 184 |
| sources:lin | 282 | 2 |
| sources:ofc2026 | 830 | 19 |
| sources:pk | 296 | 17 |
| sources:web | 57 | 0 |
| works excluded as known | | 408 |

## Prefilter status (works)

| status | n |
|---|---|
| no_class_hit | 124885 |
| candidate | 49708 |
| excluded:bulk_free_space | 5610 |
| excluded:fiber_laser_amplifier | 5425 |
| excluded:metamaterial_theory | 5026 |
| excluded:biomedical_imaging | 4677 |
| excluded:thz_free_space | 4575 |
| excluded:led_display | 4146 |
| excluded:eo_modulator_only | 2726 |
| excluded:non_optical | 1911 |
| excluded:fiber_sensing | 1826 |
| excluded:solar_cells | 1438 |
| excluded:plasmonic_sensing | 1303 |
| excluded:lidar_system | 1172 |
| known | 408 |
| seed_b_no_title_hit | 380 |
| excluded:astronomy | 358 |
| non_paper | 115 |
| seed_b_pre2005_no_cue | 104 |
| review_seed | 70 |

Candidates (class hit, not known / excluded): 49708.

## Per class (best class; cap = max(cap_min, cap_mult x budget))

cap_min 250, cap_mult 8, min_rule_score 3 (abstract-only hits 5), seed tiers: A +2 (always kept), B +1 (+1 multi-review, within cap). Any-hit = works with this class among their hits. Kept by source: A = tier-A seed; B only = tier-B seed found by no lane; lanes = found by a harvest lane (lanes+B = of which also a tier-B seed).

| group | class | budget | any-hit | best-class candidates | title-hit | below min score | cap | kept | kept A | kept B only | kept lanes | kept lanes+B |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G1 | fiber_chip_coupler | 60 | 1952 | 1214 | 942 | 138 | 480 | 480 | 18 | 103 | 359 | 97 |
| G1 | fiber_interface | 30 | 885 | 562 | 336 | 155 | 250 | 250 | 6 | 10 | 234 | 8 |
| G1 | free_space_emitter | 40 | 1789 | 1429 | 1130 | 229 | 320 | 320 | 12 | 18 | 290 | 33 |
| G1 | micro_optics | 35 | 843 | 630 | 445 | 125 | 280 | 280 | 4 | 13 | 263 | 21 |
| G2 | crossing | 30 | 271 | 134 | 100 | 19 | 250 | 115 | 0 | 20 | 95 | 39 |
| G2 | mode_converter | 35 | 1917 | 1198 | 1028 | 166 | 280 | 280 | 3 | 24 | 253 | 26 |
| G2 | polarization | 45 | 1986 | 1601 | 1350 | 190 | 360 | 360 | 0 | 70 | 290 | 81 |
| G2 | splitter | 50 | 2316 | 1230 | 875 | 211 | 400 | 400 | 4 | 35 | 361 | 38 |
| G3 | reflector | 30 | 1986 | 1156 | 970 | 150 | 250 | 250 | 3 | 34 | 213 | 30 |
| G3 | resonator | 60 | 10632 | 7208 | 5406 | 1321 | 480 | 480 | 28 | 30 | 422 | 28 |
| G3 | wdm | 80 | 3003 | 1693 | 1469 | 154 | 640 | 640 | 3 | 56 | 581 | 64 |
| G4 | nonreciprocal | 30 | 1027 | 790 | 606 | 158 | 250 | 250 | 7 | 40 | 203 | 37 |
| G4 | phase_shifter | 60 | 3576 | 2427 | 2089 | 236 | 480 | 480 | 8 | 58 | 414 | 44 |
| G4 | switch_fabric | 45 | 2450 | 1562 | 1282 | 246 | 360 | 360 | 7 | 64 | 289 | 32 |
| G5 | photodetector | 70 | 6481 | 5497 | 3563 | 1163 | 560 | 560 | 19 | 38 | 503 | 26 |
| G6 | amplifier | 45 | 2200 | 1420 | 1084 | 213 | 360 | 360 | 6 | 70 | 284 | 40 |
| G6 | frequency_converter | 30 | 3728 | 2544 | 2040 | 375 | 250 | 250 | 14 | 30 | 206 | 13 |
| G6 | laser | 90 | 16045 | 13680 | 12418 | 1119 | 720 | 720 | 46 | 35 | 639 | 65 |
| G7 | chip_chip_coupler | 40 | 407 | 166 | 136 | 20 | 320 | 146 | 2 | 16 | 128 | 15 |
| G7 | waveguide_platform | 60 | 5749 | 3567 | 3031 | 346 | 480 | 480 | 22 | 89 | 369 | 83 |
| | total | 965 | | 49708 | 40300 | | | 7461 | 212 | 853 | 6396 | 820 |

## Kept per subtype (kept works whose best class has this subtype hit)

| class.subtype | kept | candidates |
|---|---|---|
| fiber_chip_coupler | 22 | 150 |
| fiber_chip_coupler.edge | 141 | 303 |
| fiber_chip_coupler.grating | 317 | 724 |
| fiber_chip_coupler.photonic_wire_bond | 15 | 67 |
| fiber_interface.connector | 24 | 43 |
| fiber_interface.fan_out | 157 | 384 |
| fiber_interface.fau | 42 | 85 |
| fiber_interface.other | 13 | 25 |
| fiber_interface.v_groove | 37 | 58 |
| free_space_emitter | 1 | 1 |
| free_space_emitter.grating_emitter | 35 | 182 |
| free_space_emitter.metasurface | 80 | 494 |
| free_space_emitter.other | 229 | 809 |
| micro_optics.facet_lens | 53 | 92 |
| micro_optics.integrated_lens | 48 | 101 |
| micro_optics.metalens | 149 | 316 |
| micro_optics.other | 34 | 116 |
| micro_optics.vertical_taper | 25 | 51 |
| crossing.mmi | 43 | 46 |
| crossing.multilevel | 1 | 2 |
| crossing.other | 111 | 129 |
| crossing.swg | 22 | 22 |
| mode_converter.converter | 157 | 489 |
| mode_converter.mdm_mux | 166 | 664 |
| mode_converter.other | 30 | 219 |
| polarization.compensator | 18 | 258 |
| polarization.other | 104 | 488 |
| polarization.pbs | 202 | 535 |
| polarization.psr | 130 | 548 |
| splitter.adiabatic | 35 | 57 |
| splitter.directional_coupler | 133 | 413 |
| splitter.hybrid_90 | 20 | 57 |
| splitter.mmi | 140 | 412 |
| splitter.other | 157 | 385 |
| splitter.y_branch | 43 | 152 |
| reflector.band_stop | 42 | 158 |
| reflector.bragg | 160 | 710 |
| reflector.loop_mirror | 23 | 117 |
| reflector.other | 64 | 261 |
| reflector.phc_mirror | 22 | 110 |
| resonator.bragg | 5 | 75 |
| resonator.coupled_rings | 28 | 517 |
| resonator.disk | 107 | 1594 |
| resonator.other | 351 | 4418 |
| resonator.photonic_crystal | 51 | 1156 |
| resonator.ring | 254 | 2617 |
| wdm.awg | 146 | 286 |
| wdm.bragg_cdc | 66 | 128 |
| wdm.cascaded_mzi | 39 | 90 |
| wdm.eg | 24 | 60 |
| wdm.interleaver | 24 | 57 |
| wdm.mrr | 63 | 136 |
| wdm.other | 469 | 1233 |
| wdm.tff | 1 | 18 |
| nonreciprocal | 71 | 397 |
| nonreciprocal.circulator | 40 | 88 |
| nonreciprocal.isolator | 149 | 323 |
| phase_shifter.ferroelectric_nonvolatile | 73 | 467 |
| phase_shifter.mems | 116 | 484 |
| phase_shifter.other | 111 | 402 |
| phase_shifter.phase_change | 124 | 772 |
| phase_shifter.thermo_optic | 201 | 734 |
| switch_fabric.mems | 44 | 189 |
| switch_fabric.mzi_mesh | 121 | 428 |
| switch_fabric.other | 315 | 1121 |
| switch_fabric.wss | 58 | 299 |
| photodetector.apd | 126 | 780 |
| photodetector.ge_waveguide | 182 | 579 |
| photodetector.graphene | 30 | 339 |
| photodetector.iii_v_on_platform | 112 | 463 |
| photodetector.other | 522 | 4771 |
| photodetector.snspd | 38 | 482 |
| photodetector.spad | 49 | 462 |
| photodetector.vertical | 30 | 181 |
| amplifier.other | 272 | 1016 |
| amplifier.parametric | 66 | 261 |
| amplifier.rare_earth | 136 | 350 |
| amplifier.soa | 129 | 578 |
| frequency_converter.other | 126 | 1301 |
| frequency_converter.sfg_dfg | 116 | 814 |
| frequency_converter.shg | 156 | 1216 |
| laser | 1 | 1 |
| laser.comb | 201 | 4372 |
| laser.dbr | 23 | 159 |
| laser.dfb | 177 | 1586 |
| laser.ecl | 42 | 306 |
| laser.els_module | 9 | 88 |
| laser.heterogeneous | 110 | 653 |
| laser.other | 540 | 8160 |
| laser.pcsel | 6 | 172 |
| laser.sil | 40 | 293 |
| laser.soa_dfb | 12 | 35 |
| laser.tunable | 110 | 950 |
| laser.vcsel | 65 | 1365 |
| chip_chip_coupler | 36 | 41 |
| chip_chip_coupler.butt | 46 | 46 |
| chip_chip_coupler.evanescent | 9 | 11 |
| chip_chip_coupler.other | 57 | 70 |
| waveguide_platform | 1 | 1 |
| waveguide_platform.bend | 51 | 218 |
| waveguide_platform.other | 335 | 2069 |
| waveguide_platform.slow_light | 50 | 558 |
| waveguide_platform.straight | 340 | 1417 |
| waveguide_platform.transition | 19 | 124 |

## Kept per group (scoring batches)

| group | kept |
|---|---|
| G1 | 1330 |
| G2 | 1155 |
| G3 | 1370 |
| G4 | 1090 |
| G5 | 560 |
| G6 | 1330 |
| G7 | 626 |

## Per-lane contribution and abstract coverage (a work counts for every lane that found it)

| lane | works merged | abstract % (merged) | candidates | kept | abstract % (kept) | only this lane (kept) |
|---|---|---|---|---|---|---|
| arxiv | 40573 | 100.0 | 7841 | 877 | 100.0 | 376 |
| conferences | 47553 | 98.6 | 12746 | 1026 | 99.9 | 930 |
| journals | 131775 | 94.6 | 29768 | 5148 | 100.0 | 3956 |
| seeds | 9255 | 87.9 | 4674 | 1885 | 99.8 | 891 |
| all | 215863 | 96.0 | 49708 | 7461 | 99.9 | |

Abstract = at least 100 characters after tag stripping.

## Rule-score distribution (kept)

| score | kept | candidates |
|---|---|---|
| 10 | 5695 | 8148 |
| 9 | 1332 | 7410 |
| 8 | 213 | 7690 |
| 7 | 131 | 7058 |
| 6 | 57 | 5755 |
| 5 | 17 | 4233 |
| 4 | 7 | 4185 |
| 3 | 6 | 2637 |
| 2 | 1 | 1269 |
| 1 | 1 | 701 |
| 0 | 1 | 622 |
