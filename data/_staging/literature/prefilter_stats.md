# Literature prefilter statistics (DevLog-006 S2)

Generated 2026-10-21 by `scripts/lit_prefilter.py` from `cache/literature/pool/*.jsonl` (git-ignored). Counts only.
Re-run over the growing pool rewrites this file.

## Pool by lane (raw records)

| lane | pool files | raw records |
|---|---|---|
| arxiv | 212 | 40594 |
| conferences | 89 | 49295 |
| journals | 252 | 116973 |
| seeds | 23 | 11641 |
| total | 576 | 218503 |

## Merge

| step | n |
|---|---|
| raw records | 218503 |
| unreadable lines skipped | 0 |
| dropped type editorial | 3 |
| dropped type erratum | 9 |
| dropped type letter | 28 |
| dropped type paratext | 13 |
| works after merge | 202302 |
| duplicate records merged | 16148 |
| works with more than one record | 14011 |
| of which across lanes | 11349 |
| of which preprint + published version | 8683 |

## Known-id exclusion (work already in a local corpus; a work can be in several)

| corpus | index entries | works matched |
|---|---|---|
| eo_candidates | 461 | 366 |
| eo_papers | 233 | 183 |
| ofc2026 | 830 | 19 |
| pk_cache_list | 300 | 17 |
| pk_papers | 296 | 17 |
| sources:blog | 128 | 6 |
| sources:eo | 233 | 183 |
| sources:lin | 282 | 2 |
| sources:ofc2026 | 830 | 19 |
| sources:pk | 296 | 17 |
| sources:web | 57 | 0 |
| works excluded as known | | 405 |

## Prefilter status (works)

| status | n |
|---|---|
| no_class_hit | 116900 |
| candidate | 46958 |
| excluded:bulk_free_space | 5480 |
| excluded:fiber_laser_amplifier | 5250 |
| excluded:metamaterial_theory | 4593 |
| excluded:biomedical_imaging | 4531 |
| excluded:thz_free_space | 4143 |
| excluded:led_display | 3739 |
| excluded:eo_modulator_only | 2648 |
| excluded:fiber_sensing | 1794 |
| excluded:non_optical | 1311 |
| excluded:solar_cells | 1285 |
| excluded:lidar_system | 1165 |
| excluded:plasmonic_sensing | 1085 |
| seed_b_no_title_hit | 411 |
| known | 405 |
| excluded:astronomy | 353 |
| seed_b_pre2005_no_cue | 104 |
| non_paper | 77 |
| review_seed | 70 |

Candidates (class hit, not known / excluded): 46958.

## Per class (best class; cap = max(cap_min, cap_mult x budget))

cap_min 250, cap_mult 8, min_rule_score 3 (abstract-only hits 5), seed tiers: A +2 (always kept), B +1 (+1 multi-review, within cap). Any-hit = works with this class among their hits. Kept by source: A = tier-A seed; B only = tier-B seed found by no lane; lanes = found by a harvest lane (lanes+B = of which also a tier-B seed).

| group | class | budget | any-hit | best-class candidates | title-hit | below min score | cap | kept | kept A | kept B only | kept lanes | kept lanes+B |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G1 | fiber_chip_coupler | 60 | 1893 | 1174 | 914 | 134 | 480 | 480 | 18 | 114 | 348 | 98 |
| G1 | fiber_interface | 30 | 866 | 547 | 332 | 152 | 250 | 250 | 6 | 12 | 232 | 6 |
| G1 | free_space_emitter | 40 | 1700 | 1355 | 1080 | 214 | 320 | 320 | 12 | 20 | 288 | 32 |
| G1 | micro_optics | 35 | 797 | 593 | 420 | 120 | 280 | 280 | 4 | 13 | 263 | 21 |
| G2 | crossing | 30 | 265 | 131 | 99 | 18 | 250 | 113 | 0 | 20 | 93 | 39 |
| G2 | mode_converter | 35 | 1867 | 1169 | 1008 | 158 | 280 | 280 | 3 | 24 | 253 | 26 |
| G2 | polarization | 45 | 1845 | 1470 | 1248 | 165 | 360 | 360 | 0 | 75 | 285 | 80 |
| G2 | splitter | 50 | 2233 | 1170 | 843 | 197 | 400 | 400 | 4 | 38 | 358 | 35 |
| G3 | reflector | 30 | 1875 | 1094 | 927 | 134 | 250 | 250 | 3 | 37 | 210 | 27 |
| G3 | resonator | 60 | 9983 | 6688 | 5060 | 1208 | 480 | 480 | 28 | 33 | 419 | 27 |
| G3 | wdm | 80 | 2951 | 1663 | 1447 | 152 | 640 | 640 | 3 | 58 | 579 | 63 |
| G4 | nonreciprocal | 30 | 938 | 712 | 553 | 137 | 250 | 250 | 7 | 45 | 198 | 32 |
| G4 | phase_shifter | 60 | 3355 | 2253 | 1934 | 221 | 480 | 480 | 8 | 59 | 413 | 44 |
| G4 | switch_fabric | 45 | 2351 | 1497 | 1245 | 225 | 360 | 360 | 7 | 66 | 287 | 30 |
| G5 | photodetector | 70 | 6046 | 5137 | 3365 | 1074 | 560 | 560 | 19 | 41 | 500 | 29 |
| G6 | amplifier | 45 | 2107 | 1363 | 1043 | 201 | 360 | 360 | 6 | 72 | 282 | 39 |
| G6 | frequency_converter | 30 | 3568 | 2426 | 1964 | 348 | 250 | 250 | 14 | 31 | 205 | 15 |
| G6 | laser | 90 | 15192 | 12962 | 11780 | 1055 | 720 | 720 | 46 | 44 | 630 | 70 |
| G7 | chip_chip_coupler | 40 | 397 | 164 | 135 | 20 | 320 | 144 | 2 | 17 | 125 | 14 |
| G7 | waveguide_platform | 60 | 5494 | 3390 | 2897 | 319 | 480 | 480 | 22 | 93 | 365 | 80 |
| | total | 965 | | 46958 | 38294 | | | 7457 | 212 | 912 | 6333 | 807 |

## Kept per subtype (kept works whose best class has this subtype hit)

| class.subtype | kept | candidates |
|---|---|---|
| fiber_chip_coupler | 23 | 147 |
| fiber_chip_coupler.edge | 143 | 295 |
| fiber_chip_coupler.grating | 315 | 697 |
| fiber_chip_coupler.photonic_wire_bond | 14 | 65 |
| fiber_interface.connector | 25 | 43 |
| fiber_interface.fan_out | 158 | 379 |
| fiber_interface.fau | 41 | 83 |
| fiber_interface.other | 13 | 24 |
| fiber_interface.v_groove | 36 | 51 |
| free_space_emitter | 1 | 1 |
| free_space_emitter.grating_emitter | 36 | 177 |
| free_space_emitter.metasurface | 75 | 462 |
| free_space_emitter.other | 234 | 768 |
| micro_optics.facet_lens | 53 | 87 |
| micro_optics.integrated_lens | 49 | 98 |
| micro_optics.metalens | 149 | 294 |
| micro_optics.other | 34 | 110 |
| micro_optics.vertical_taper | 25 | 49 |
| crossing.mmi | 43 | 46 |
| crossing.multilevel | 1 | 1 |
| crossing.other | 109 | 127 |
| crossing.swg | 22 | 22 |
| mode_converter.converter | 154 | 472 |
| mode_converter.mdm_mux | 168 | 659 |
| mode_converter.other | 31 | 211 |
| polarization.compensator | 18 | 248 |
| polarization.other | 105 | 455 |
| polarization.pbs | 201 | 502 |
| polarization.psr | 132 | 483 |
| splitter.adiabatic | 33 | 55 |
| splitter.directional_coupler | 137 | 389 |
| splitter.hybrid_90 | 23 | 56 |
| splitter.mmi | 139 | 401 |
| splitter.other | 154 | 372 |
| splitter.y_branch | 42 | 137 |
| reflector.band_stop | 41 | 147 |
| reflector.bragg | 160 | 673 |
| reflector.loop_mirror | 23 | 115 |
| reflector.other | 64 | 243 |
| reflector.phc_mirror | 22 | 100 |
| resonator.bragg | 5 | 72 |
| resonator.coupled_rings | 28 | 493 |
| resonator.disk | 108 | 1472 |
| resonator.other | 350 | 4095 |
| resonator.photonic_crystal | 51 | 1078 |
| resonator.ring | 250 | 2472 |
| wdm.awg | 148 | 285 |
| wdm.bragg_cdc | 66 | 127 |
| wdm.cascaded_mzi | 40 | 90 |
| wdm.eg | 24 | 60 |
| wdm.interleaver | 24 | 57 |
| wdm.mrr | 65 | 136 |
| wdm.other | 468 | 1204 |
| wdm.tff | 1 | 18 |
| nonreciprocal | 67 | 348 |
| nonreciprocal.circulator | 41 | 78 |
| nonreciprocal.isolator | 152 | 304 |
| phase_shifter.ferroelectric_nonvolatile | 75 | 446 |
| phase_shifter.mems | 115 | 420 |
| phase_shifter.other | 112 | 388 |
| phase_shifter.phase_change | 117 | 719 |
| phase_shifter.thermo_optic | 206 | 696 |
| switch_fabric.mems | 45 | 185 |
| switch_fabric.mzi_mesh | 124 | 424 |
| switch_fabric.other | 313 | 1062 |
| switch_fabric.wss | 58 | 297 |
| photodetector.apd | 127 | 740 |
| photodetector.ge_waveguide | 187 | 547 |
| photodetector.graphene | 29 | 315 |
| photodetector.iii_v_on_platform | 115 | 444 |
| photodetector.other | 520 | 4440 |
| photodetector.snspd | 40 | 471 |
| photodetector.spad | 51 | 454 |
| photodetector.vertical | 30 | 157 |
| amplifier.other | 274 | 975 |
| amplifier.parametric | 66 | 248 |
| amplifier.rare_earth | 132 | 337 |
| amplifier.soa | 131 | 565 |
| frequency_converter.other | 127 | 1249 |
| frequency_converter.sfg_dfg | 115 | 778 |
| frequency_converter.shg | 155 | 1159 |
| laser | 1 | 1 |
| laser.comb | 202 | 4231 |
| laser.dbr | 21 | 155 |
| laser.dfb | 174 | 1520 |
| laser.ecl | 43 | 300 |
| laser.els_module | 9 | 86 |
| laser.heterogeneous | 120 | 631 |
| laser.other | 529 | 7615 |
| laser.pcsel | 5 | 161 |
| laser.sil | 39 | 291 |
| laser.soa_dfb | 12 | 35 |
| laser.tunable | 109 | 911 |
| laser.vcsel | 67 | 1296 |
| chip_chip_coupler | 36 | 41 |
| chip_chip_coupler.butt | 45 | 45 |
| chip_chip_coupler.evanescent | 9 | 11 |
| chip_chip_coupler.other | 56 | 69 |
| waveguide_platform | 1 | 1 |
| waveguide_platform.bend | 52 | 211 |
| waveguide_platform.other | 332 | 1967 |
| waveguide_platform.slow_light | 53 | 522 |
| waveguide_platform.straight | 337 | 1360 |
| waveguide_platform.transition | 19 | 112 |

## Kept per group (scoring batches)

| group | kept |
|---|---|
| G1 | 1330 |
| G2 | 1153 |
| G3 | 1370 |
| G4 | 1090 |
| G5 | 560 |
| G6 | 1330 |
| G7 | 624 |

## Per-lane contribution and abstract coverage (a work counts for every lane that found it)

| lane | works merged | abstract % (merged) | candidates | kept | abstract % (kept) | only this lane (kept) |
|---|---|---|---|---|---|---|
| arxiv | 40574 | 100.0 | 7830 | 906 | 100.0 | 414 |
| conferences | 47553 | 98.6 | 12745 | 1101 | 99.9 | 998 |
| journals | 116882 | 94.0 | 26577 | 4953 | 100.0 | 3816 |
| seeds | 9255 | 87.9 | 4643 | 1931 | 99.8 | 953 |
| all | 202302 | 95.7 | 46958 | 7457 | 99.9 | |

Abstract = at least 100 characters after tag stripping.

## Rule-score distribution (kept)

| score | kept | candidates |
|---|---|---|
| 10 | 5628 | 7805 |
| 9 | 1374 | 7009 |
| 8 | 219 | 7246 |
| 7 | 149 | 6624 |
| 6 | 54 | 5421 |
| 5 | 17 | 4004 |
| 4 | 7 | 3919 |
| 3 | 6 | 2462 |
| 2 | 1 | 1220 |
| 1 | 1 | 656 |
| 0 | 1 | 592 |
