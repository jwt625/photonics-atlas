# Increment selection delta (DevLog-006, D230-D232)

Generated 2026-10-22 by `scripts/lit_select.py --delta` (applied: cache_list.csv rewritten). Rules: budget 1000; frozen = cached papers, queue days 1-2, curator picks; a work outside the previous list enters only by displacing a not-yet-retrieved incumbent of its primary class on days 3-10 that the unconstrained `selection.yaml` run drops; senior-author cap and paywalled share re-checked per swap.

- previous rows 1000; new rows 1000; entering candidates (unconstrained run) 16; entered 10; blocked 6
- previous rows the unconstrained run drops 16: displaced 10, kept as frozen 4, kept without a same-class entrant 2
- previous rows now headed by another version (identity kept) 0; previous rows no longer eligible (kept verbatim unless displaced) 0; paper_id changes of kept uids 0

| class | budget | previous | candidates | entered | displaced | blocked | dropped by rules, kept frozen | new |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| amplifier | 45 | 45 | 1 | 0 | 0 | 1 | 1 (of 1 dropped) | 45 |
| chip_chip_coupler | 40 | 39 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 39 |
| crossing | 30 | 33 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 33 |
| fiber_chip_coupler | 60 | 60 | 3 | 2 | 2 | 1 | 1 (of 3 dropped) | 60 |
| fiber_interface | 30 | 31 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 31 |
| free_space_emitter | 40 | 40 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 40 |
| frequency_converter | 30 | 30 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 30 |
| laser | 90 | 102 | 3 | 2 | 2 | 1 | 1 (of 3 dropped) | 102 |
| micro_optics | 35 | 35 | 2 | 2 | 2 | 0 | 0 (of 2 dropped) | 35 |
| mode_converter | 35 | 35 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 35 |
| nonreciprocal | 30 | 30 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 30 |
| phase_shifter | 60 | 60 | 2 | 1 | 1 | 1 | 1 (of 2 dropped) | 60 |
| photodetector | 70 | 76 | 2 | 1 | 1 | 1 | 0 (of 1 dropped) | 76 |
| polarization | 45 | 45 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 45 |
| reflector | 30 | 30 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 30 |
| resonator | 60 | 60 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 60 |
| splitter | 50 | 50 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 50 |
| switch_fabric | 45 | 52 | 0 | 0 | 0 | 0 | 0 (of 2 dropped) | 52 |
| waveguide_platform | 60 | 67 | 2 | 1 | 1 | 1 | 0 (of 1 dropped) | 67 |
| wdm | 80 | 80 | 1 | 1 | 1 | 0 | 0 (of 1 dropped) | 80 |
| total | 965 | 1000 | 16 | 10 | 10 | 6 | 4 (of 16) | 1000 |

## Entering

| paper_id | class | subtype | score | access | venue | year | rule | displaces | title |
|---|---|---|---:|---|---|---|---|---|---|
| korcek2023 | fiber_chip_coupler | fiber_chip_coupler.grating | 9 | oa | Scientific Reports | 2023 | rank | p2025 | Library of single-etch silicon nitride grating couplers for low-loss and fabrication-robust fiber-chip interconnection |
| croce2026 | fiber_chip_coupler | fiber_chip_coupler.grating | 9 | oa | Scientific Reports | 2026 | rank | zhou2025 | High-efficiency grating couplers for vertical coupling in thin-film silicon nitride technology |
| holl2025 | laser | laser.vcsel | 9 | oa | Applied Physics Letters | 2025 | subtype floor laser.vcsel | wang2025a | 2.5 W GaSb-based VECSEL at 2062.4 nm with an absolute wavelength stability below 1 MHz |
| hamaguchi2018 | laser | laser.vcsel | 9 | oa | Scientific Reports | 2018 | subtype floor laser.vcsel | moser2011 | Lateral optical confinement of GaN-based VCSEL using an atomically smooth monolithic curved mirror |
| hassan2020 | micro_optics | micro_optics.other | 9 | oa | Scientific Reports | 2020 | subtype floor micro_optics.other | melkonyan2017 | Integrated photonic guided metalens based on a pseudo-graded index distribution |
| kasztelanic2018 | micro_optics | micro_optics.facet_lens | 8 | oa | Scientific Reports | 2018 | rank | scarcella2017 | Integrating Free-Form Nanostructured GRIN Microlenses with Single-Mode Fibers for Optofluidic Systems |
| song2016 | phase_shifter | phase_shifter.other | 9 | oa | Scientific Reports | 2016 | subtype floor phase_shifter.other | ai2024 | Integrated photonics with programmable non-volatile memory |
| yanikgonul2021 | photodetector | photodetector.apd | 10 | oa | Nature Communications | 2021 | subtype floor photodetector.apd | shi2025 | Integrated avalanche photodetectors for visible light |
| fan2021 | waveguide_platform | waveguide_platform.other | 9 | oa | Scientific Reports | 2021 | subtype floor waveguide_platform.other | wang2026l | Higher order mode supercontinuum generation in tantalum pentoxide (Ta2O5) channel waveguide |
| hsu2023 | wdm | wdm.mrr | 9 | oa | Scientific Reports | 2023 | rank | errandoherranz2015 | On-chip wavelength division multiplexing filters using extremely efficient gate-driven silicon microring resonator array |

## Displaced

| paper_id | class | score | access | day | route | previous reason | by | title |
|---|---|---:|---|---:|---|---|---|---|
| p2025 | fiber_chip_coupler | 9 | oa | 3 | optica_browser | rank | korcek2023 | High-efficiency grating fiber-chip couplers in wide bandgap III-nitride material platforms |
| zhou2025 | fiber_chip_coupler | 9 | oa | 4 | publisher_browser | rank | croce2026 | Waveguide grating couplers with bandwidth beyond 200 nm |
| moser2011 | laser | 9 | oa | 10 | manual | subtype floor laser.vcsel | hamaguchi2018 | 81 fJ/bit energy-to-data ratio of 850 nm vertical-cavity surface-emitting lasers for optical interconnects |
| wang2025a | laser | 9 | oa | 7 | optica_browser | subtype floor laser.vcsel | holl2025 | Heterogeneous integration, single-mode MEMS-VCSEL with super-span resonance filtering, small divergence angle, and Gaussian distribution |
| melkonyan2017 | micro_optics | 8 | oa | 6 | ieee_browser | rank | hassan2020 | Efficient Fiber-to-Waveguide Edge Coupling Using an Optical Fiber Axicon Lens Fabricated by Focused Ion Beam |
| scarcella2017 | micro_optics | 8 | oa | 5 | ieee_browser | rank | kasztelanic2018 | Pluggable Single-Mode Fiber-Array-to-PIC Coupling Using Micro-Lenses |
| ai2024 | phase_shifter | 8 | oa | 3 | optica_browser | rank | song2016 | On-chip broadband Mach-Zehnder interferometer based on a broadband taper-section phase shifter |
| shi2025 | photodetector | 9 | oa | 9 | publisher_browser | reserve: best remaining | yanikgonul2021 | Ultrafast avalanche photodiode exceeding 100 GHz bandwidth |
| wang2026l | waveguide_platform | 8 | oa | 9 | optica_browser | subtype floor waveguide_platform.other | fan2021 | Octave-spanning supercontinuum generation in a wafer-scale, low loss deuterated silicon nitride waveguide |
| errandoherranz2015 | wdm | 9 | oa | 9 | optica_browser | rank | hsu2023 | Low-power microelectromechanically tunable silicon photonic ring resonator add-drop filter |

## Blocked entering candidates

| uid | class | score | access | why | title |
|---|---|---:|---|---|---|
| 10.1364/ofc.2022.w3j.6 | amplifier | 9 | oa | no displaceable incumbent of the class on days 3-10 | 3D printed and spiral lithographically patterned erbium-doped polymer micro-waveguide amplifiers |
| 10.1063/5.0324732 | fiber_chip_coupler | 9 | oa | no displaceable incumbent of the class on days 3-10 | High-efficiency scalable hybrid silicon grating couplers for thin-film lithium niobate photonics |
| 10.1038/s41598-026-50776-9 | laser | 9 | oa | no displaceable incumbent of the class on days 3-10 | Narrow-linewidth photonic wirebonded silicon nitride external cavity tunable laser |
| 10.1038/s41598-022-21590-w | phase_shifter | 9 | oa | no displaceable incumbent of the class on days 3-10 | Thermo-optic tuning of silicon nitride microring resonators with low loss non-volatile $$\hbox {Sb}_{2}\hbox {S}_{3}$$ phase change material |
| 10.1063/1.4941995 | photodetector | 9 | oa | no displaceable incumbent of the class on days 3-10 | Resonance-enhanced waveguide-coupled silicon-germanium detector |
| 10.1063/5.0221409 | waveguide_platform | 10 | paywalled | no displaceable incumbent of the class on days 3-10 | 300-nm-thick, ultralow-loss silicon nitride photonic integrated circuits by 8-in. foundry production |

## Dropped by the unconstrained run, kept (frozen or curator)

| paper_id | class | score | why kept | previous reason | title |
|---|---|---:|---|---|---|
| ronn2019 | amplifier | 9 | cached | rank | Ultra-high on-chip optical gain in erbium-based hybrid slot waveguides |
| wu2025 | fiber_chip_coupler | 9 | queue day 2 | rank | Ultra-low-loss polarization-splitting grating coupler based on inverse-design |
| heim2025 | laser | 9 | cached | reserve: best remaining | Hybrid integrated ultra-low linewidth coil stabilized isolator-free widely tunable external cavity laser |
| meng2023 | phase_shifter | 8 | cached | rank | Electrical programmable multilevel nonvolatile photonic random-access memory |

# D233 follow-up delta (coordinator drop of holl2025, config/literature/curation/increment.yaml)

Superseded rows above: holl2025 dropped; moser2011 back in its previous slot (day 10, manual, queue row identical to the pre-increment row).


Generated 2026-10-22 by `scripts/lit_select.py --delta` (applied: cache_list.csv rewritten). Rules: budget 1000; frozen = cached papers, queue days 1-2, curator picks; a work outside the previous list enters only by displacing a not-yet-retrieved incumbent of its primary class on days 3-10 that the unconstrained `selection.yaml` run drops; senior-author cap and paywalled share re-checked per swap.

- previous rows 1000; new rows 1000; entering candidates (unconstrained run) 7; entered 1; blocked 6
- previous rows the unconstrained run drops 7: displaced 1, kept as frozen 4, kept without a same-class entrant 2
- previous rows now headed by another version (identity kept) 0; previous rows no longer eligible (kept verbatim unless displaced) 1; paper_id changes of kept uids 0

| class | budget | previous | candidates | entered | displaced | blocked | dropped by rules, kept frozen | new |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| amplifier | 45 | 45 | 1 | 0 | 0 | 1 | 1 (of 1 dropped) | 45 |
| chip_chip_coupler | 40 | 39 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 39 |
| crossing | 30 | 33 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 33 |
| fiber_chip_coupler | 60 | 60 | 1 | 0 | 0 | 1 | 1 (of 1 dropped) | 60 |
| fiber_interface | 30 | 31 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 31 |
| free_space_emitter | 40 | 40 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 40 |
| frequency_converter | 30 | 30 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 30 |
| laser | 90 | 102 | 2 | 1 | 1 | 1 | 1 (of 2 dropped) | 102 |
| micro_optics | 35 | 35 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 35 |
| mode_converter | 35 | 35 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 35 |
| nonreciprocal | 30 | 30 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 30 |
| phase_shifter | 60 | 60 | 1 | 0 | 0 | 1 | 1 (of 1 dropped) | 60 |
| photodetector | 70 | 76 | 1 | 0 | 0 | 1 | 0 (of 0 dropped) | 76 |
| polarization | 45 | 45 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 45 |
| reflector | 30 | 30 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 30 |
| resonator | 60 | 60 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 60 |
| splitter | 50 | 50 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 50 |
| switch_fabric | 45 | 52 | 0 | 0 | 0 | 0 | 0 (of 2 dropped) | 52 |
| waveguide_platform | 60 | 67 | 1 | 0 | 0 | 1 | 0 (of 0 dropped) | 67 |
| wdm | 80 | 80 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 80 |
| total | 965 | 1000 | 7 | 1 | 1 | 6 | 4 (of 7) | 1000 |

### Entering

| paper_id | class | subtype | score | access | venue | year | rule | displaces | title |
|---|---|---|---:|---|---|---|---|---|---|
| moser2011 | laser | laser.vcsel | 9 | oa | Applied Physics Letters | 2011 | subtype floor laser.vcsel | holl2025 | 81 fJ/bit energy-to-data ratio of 850 nm vertical-cavity surface-emitting lasers for optical interconnects |

### Displaced

| paper_id | class | score | access | day | route | previous reason | by | title |
|---|---|---:|---|---:|---|---|---|---|
| holl2025 | laser | 9 | oa | 10 | manual | subtype floor laser.vcsel | moser2011 | 2.5 W GaSb-based VECSEL at 2062.4 nm with an absolute wavelength stability below 1 MHz |

### Blocked entering candidates

| uid | class | score | access | why | title |
|---|---|---:|---|---|---|
| 10.1364/ofc.2022.w3j.6 | amplifier | 9 | oa | no displaceable incumbent of the class on days 3-10 | 3D printed and spiral lithographically patterned erbium-doped polymer micro-waveguide amplifiers |
| 10.1063/5.0324732 | fiber_chip_coupler | 9 | oa | no displaceable incumbent of the class on days 3-10 | High-efficiency scalable hybrid silicon grating couplers for thin-film lithium niobate photonics |
| 10.1038/s41598-026-50776-9 | laser | 9 | oa | no displaceable incumbent of the class on days 3-10 | Narrow-linewidth photonic wirebonded silicon nitride external cavity tunable laser |
| 10.1038/s41598-022-21590-w | phase_shifter | 9 | oa | no displaceable incumbent of the class on days 3-10 | Thermo-optic tuning of silicon nitride microring resonators with low loss non-volatile $$\hbox {Sb}_{2}\hbox {S}_{3}$$ phase change material |
| 10.1063/1.4941995 | photodetector | 9 | oa | no displaceable incumbent of the class on days 3-10 | Resonance-enhanced waveguide-coupled silicon-germanium detector |
| 10.1063/5.0221409 | waveguide_platform | 10 | paywalled | no displaceable incumbent of the class on days 3-10 | 300-nm-thick, ultralow-loss silicon nitride photonic integrated circuits by 8-in. foundry production |

### Dropped by the unconstrained run, kept (frozen or curator)

| paper_id | class | score | why kept | previous reason | title |
|---|---|---:|---|---|---|
| ronn2019 | amplifier | 9 | cached | rank | Ultra-high on-chip optical gain in erbium-based hybrid slot waveguides |
| wu2025 | fiber_chip_coupler | 9 | queue day 2 | rank | Ultra-low-loss polarization-splitting grating coupler based on inverse-design |
| heim2025 | laser | 9 | cached | reserve: best remaining | Hybrid integrated ultra-low linewidth coil stabilized isolator-free widely tunable external cavity laser |
| meng2023 | phase_shifter | 8 | cached | rank | Electrical programmable multilevel nonvolatile photonic random-access memory |

### Identity notes

- holl2025 (10.1063/5.0293416): no longer eligible in the current pool / scores (curation drop or exclusion); displaced

## D511 delta (2026-11-06): owner add 10.1364/oe.563146

Generated 2026-11-06 by `scripts/lit_select.py --delta` (applied: cache_list.csv rewritten). Rules: budget 1000; frozen = cached papers, queue days 1-2, curator picks; a work outside the previous list enters only by displacing a not-yet-retrieved incumbent of its primary class on days 3-10 that the unconstrained `selection.yaml` run drops; senior-author cap and paywalled share re-checked per swap; a curator pick without such a slot enters beyond the class budget (D511).

- previous rows 1000; new rows 1001; entering candidates (unconstrained run) 7; entered 1 (0 by swap, 1 curator beyond budget); blocked 6
- previous rows the unconstrained run drops 7: displaced 0, kept as frozen 7, kept without a same-class entrant 0
- previous rows now headed by another version (identity kept) 0; previous rows no longer eligible (kept verbatim unless displaced) 0; paper_id changes of kept uids 0

| class | budget | previous | candidates | entered | displaced | blocked | dropped by rules, kept frozen | new |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| amplifier | 45 | 45 | 1 | 0 | 0 | 1 | 1 (of 1 dropped) | 45 |
| chip_chip_coupler | 40 | 39 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 39 |
| crossing | 30 | 33 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 33 |
| fiber_chip_coupler | 60 | 60 | 1 | 0 | 0 | 1 | 1 (of 1 dropped) | 60 |
| fiber_interface | 30 | 31 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 31 |
| free_space_emitter | 40 | 40 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 40 |
| frequency_converter | 30 | 30 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 30 |
| laser | 90 | 102 | 1 | 0 | 0 | 1 | 1 (of 1 dropped) | 102 |
| micro_optics | 35 | 35 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 35 |
| mode_converter | 35 | 35 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 35 |
| nonreciprocal | 30 | 30 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 30 |
| phase_shifter | 60 | 60 | 1 | 0 | 0 | 1 | 1 (of 1 dropped) | 60 |
| photodetector | 70 | 76 | 1 | 0 | 0 | 1 | 0 (of 0 dropped) | 76 |
| polarization | 45 | 45 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 45 |
| reflector | 30 | 30 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 30 |
| resonator | 60 | 60 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 60 |
| splitter | 50 | 50 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 50 |
| switch_fabric | 45 | 52 | 0 | 0 | 0 | 0 | 2 (of 2 dropped) | 52 |
| waveguide_platform | 60 | 67 | 1 | 0 | 0 | 1 | 0 (of 0 dropped) | 67 |
| wdm | 80 | 80 | 1 | 1 | 0 | 0 | 1 (of 1 dropped) | 81 |
| total | 965 | 1000 | 7 | 1 | 0 | 6 | 7 (of 7) | 1001 |

### Entering

| paper_id | class | subtype | score | access | venue | year | rule | displaces | title |
|---|---|---|---:|---|---|---|---|---|---|
| xu2025a | wdm | wdm.other | 8 | oa | Optics Express | 2025 | curator: owner add 2026-11-06: 12-channel LAN-WDM MZI multiplexer on SiN, low random phase errors | (beyond budget) | 12-channel LAN wavelength-division multiplexer with low random phase errors |

### Displaced

| paper_id | class | score | access | day | route | previous reason | by | title |
|---|---|---:|---|---:|---|---|---|---|

### Blocked entering candidates

| uid | class | score | access | why | title |
|---|---|---:|---|---|---|
| 10.1364/ofc.2022.w3j.6 | amplifier | 9 | oa | no displaceable incumbent of the class on days 3-10 | 3D printed and spiral lithographically patterned erbium-doped polymer micro-waveguide amplifiers |
| 10.1063/5.0324732 | fiber_chip_coupler | 9 | oa | no displaceable incumbent of the class on days 3-10 | High-efficiency scalable hybrid silicon grating couplers for thin-film lithium niobate photonics |
| 10.1038/s41598-026-50776-9 | laser | 9 | oa | no displaceable incumbent of the class on days 3-10 | Narrow-linewidth photonic wirebonded silicon nitride external cavity tunable laser |
| 10.1038/s41598-022-21590-w | phase_shifter | 9 | oa | no displaceable incumbent of the class on days 3-10 | Thermo-optic tuning of silicon nitride microring resonators with low loss non-volatile $$\hbox {Sb}_{2}\hbox {S}_{3}$$ phase change material |
| 10.1063/1.4941995 | photodetector | 9 | oa | no displaceable incumbent of the class on days 3-10 | Resonance-enhanced waveguide-coupled silicon-germanium detector |
| 10.1063/5.0221409 | waveguide_platform | 10 | paywalled | no displaceable incumbent of the class on days 3-10 | 300-nm-thick, ultralow-loss silicon nitride photonic integrated circuits by 8-in. foundry production |

### Dropped by the unconstrained run, kept (frozen or curator)

| paper_id | class | score | why kept | previous reason | title |
|---|---|---:|---|---|---|
| ronn2019 | amplifier | 9 | cached | rank | Ultra-high on-chip optical gain in erbium-based hybrid slot waveguides |
| wu2025 | fiber_chip_coupler | 9 | queue day 2 | rank | Ultra-low-loss polarization-splitting grating coupler based on inverse-design |
| heim2025 | laser | 9 | cached | reserve: best remaining | Hybrid integrated ultra-low linewidth coil stabilized isolator-free widely tunable external cavity laser |
| meng2023 | phase_shifter | 8 | cached | rank | Electrical programmable multilevel nonvolatile photonic random-access memory |
| xia2026 | switch_fabric | 9 | cached | reserve: best remaining | Assessment of low polarization sensitive InP photonic integrated multicast and select switch with commercial 400G-ZR transceivers |
| zali2026 | switch_fabric | 9 | cached | reserve: best remaining | Densely integrated low polarization dependent 8 × 8 optical switch for optical network applications |
| amorim2017 | wdm | 9 | cached | rank | Monolithic Add–Drop Multiplexers in Fused Silica Fabricated by Femtosecond Laser Direct Writing |

## Coordinator add delta (2026-11-07): arXiv 2404.17570 (DevLog-014 benchmark, D511 rule)

Generated 2026-11-07 by `scripts/lit_select.py --delta` (applied: cache_list.csv rewritten). Rules: budget 1000; frozen = cached papers, queue days 1-2, curator picks; a work outside the previous list enters only by displacing a not-yet-retrieved incumbent of its primary class on days 3-10 that the unconstrained `selection.yaml` run drops; senior-author cap and paywalled share re-checked per swap; a curator pick without such a slot enters beyond the class budget (D511).

- previous rows 1001; new rows 1002; entering candidates (unconstrained run) 7; entered 1 (0 by swap, 1 curator beyond budget); blocked 6
- previous rows the unconstrained run drops 8: displaced 0, kept as frozen 8, kept without a same-class entrant 0
- previous rows now headed by another version (identity kept) 0; previous rows no longer eligible (kept verbatim unless displaced) 0; paper_id changes of kept uids 0

| class | budget | previous | candidates | entered | displaced | blocked | dropped by rules, kept frozen | new |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| amplifier | 45 | 45 | 1 | 0 | 0 | 1 | 1 (of 1 dropped) | 45 |
| chip_chip_coupler | 40 | 39 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 39 |
| crossing | 30 | 33 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 33 |
| fiber_chip_coupler | 60 | 60 | 1 | 0 | 0 | 1 | 1 (of 1 dropped) | 60 |
| fiber_interface | 30 | 31 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 31 |
| free_space_emitter | 40 | 40 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 40 |
| frequency_converter | 30 | 30 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 30 |
| laser | 90 | 102 | 1 | 0 | 0 | 1 | 1 (of 1 dropped) | 102 |
| micro_optics | 35 | 35 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 35 |
| mode_converter | 35 | 35 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 35 |
| nonreciprocal | 30 | 30 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 30 |
| phase_shifter | 60 | 60 | 1 | 0 | 0 | 1 | 1 (of 1 dropped) | 60 |
| photodetector | 70 | 76 | 1 | 0 | 0 | 1 | 0 (of 0 dropped) | 76 |
| polarization | 45 | 45 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 45 |
| reflector | 30 | 30 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 30 |
| resonator | 60 | 60 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 60 |
| splitter | 50 | 50 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 50 |
| switch_fabric | 45 | 52 | 0 | 0 | 0 | 0 | 2 (of 2 dropped) | 52 |
| waveguide_platform | 60 | 67 | 2 | 1 | 0 | 1 | 1 (of 1 dropped) | 68 |
| wdm | 80 | 81 | 0 | 0 | 0 | 0 | 1 (of 1 dropped) | 81 |
| total | 965 | 1001 | 7 | 1 | 0 | 6 | 8 (of 8) | 1002 |

### Entering

| paper_id | class | subtype | score | access | venue | year | rule | displaces | title |
|---|---|---|---:|---|---|---|---|---|---|
| alexander2024 | waveguide_platform | waveguide_platform.straight | 8 | oa | arXiv | 2024 | curator: add: coordinator add 2026-11-07 (DevLog-014 PDK benchmark): PsiQuantum / GlobalFoundries 300 mm SiN platform building blocks, arXiv copy of Nature 641, 876 (2025), CC BY | (beyond budget) | A manufacturable platform for photonic quantum computing |

### Displaced

| paper_id | class | score | access | day | route | previous reason | by | title |
|---|---|---:|---|---:|---|---|---|---|

### Blocked entering candidates

| uid | class | score | access | why | title |
|---|---|---:|---|---|---|
| 10.1364/ofc.2022.w3j.6 | amplifier | 9 | oa | no displaceable incumbent of the class on days 3-10 | 3D printed and spiral lithographically patterned erbium-doped polymer micro-waveguide amplifiers |
| 10.1063/5.0324732 | fiber_chip_coupler | 9 | oa | no displaceable incumbent of the class on days 3-10 | High-efficiency scalable hybrid silicon grating couplers for thin-film lithium niobate photonics |
| 10.1038/s41598-026-50776-9 | laser | 9 | oa | no displaceable incumbent of the class on days 3-10 | Narrow-linewidth photonic wirebonded silicon nitride external cavity tunable laser |
| 10.1038/s41598-022-21590-w | phase_shifter | 9 | oa | no displaceable incumbent of the class on days 3-10 | Thermo-optic tuning of silicon nitride microring resonators with low loss non-volatile $$\hbox {Sb}_{2}\hbox {S}_{3}$$ phase change material |
| 10.1063/1.4941995 | photodetector | 9 | oa | no displaceable incumbent of the class on days 3-10 | Resonance-enhanced waveguide-coupled silicon-germanium detector |
| 10.1063/5.0221409 | waveguide_platform | 10 | paywalled | no displaceable incumbent of the class on days 3-10 | 300-nm-thick, ultralow-loss silicon nitride photonic integrated circuits by 8-in. foundry production |

### Dropped by the unconstrained run, kept (frozen or curator)

| paper_id | class | score | why kept | previous reason | title |
|---|---|---:|---|---|---|
| ronn2019 | amplifier | 9 | cached | rank | Ultra-high on-chip optical gain in erbium-based hybrid slot waveguides |
| wu2025 | fiber_chip_coupler | 9 | queue day 2 | rank | Ultra-low-loss polarization-splitting grating coupler based on inverse-design |
| heim2025 | laser | 9 | cached | reserve: best remaining | Hybrid integrated ultra-low linewidth coil stabilized isolator-free widely tunable external cavity laser |
| meng2023 | phase_shifter | 8 | cached | rank | Electrical programmable multilevel nonvolatile photonic random-access memory |
| xia2026 | switch_fabric | 9 | cached | reserve: best remaining | Assessment of low polarization sensitive InP photonic integrated multicast and select switch with commercial 400G-ZR transceivers |
| zali2026 | switch_fabric | 9 | cached | reserve: best remaining | Densely integrated low polarization dependent 8 × 8 optical switch for optical network applications |
| li2026a | waveguide_platform | 9 | cached | reserve: best remaining | Mid-infrared-to-ultraviolet supercontinuum generation in low-loss tantalum pentoxide nanophotonic waveguides |
| amorim2017 | wdm | 9 | cached | rank | Monolithic Add–Drop Multiplexers in Fused Silica Fabricated by Femtosecond Laser Direct Writing |

## DevLog-015 owner adds delta (2026-11-07): 54 beyond_budget curator adds (D921, D926)

Generated 2026-11-07 by `scripts/lit_select.py --delta` (applied: cache_list.csv rewritten). Rules: budget 1000; frozen = cached papers, queue days 1-2, curator picks; a work outside the previous list enters only by displacing a not-yet-retrieved incumbent of its primary class on days 3-10 that the unconstrained `selection.yaml` run drops; senior-author cap and paywalled share re-checked per swap; a curator pick without such a slot enters beyond the class budget (D511); curation adds flagged beyond_budget enter beyond the class budget without a swap or cap check and stay out of the unconstrained run (D926).

- previous rows 1002; new rows 1056; entering candidates (unconstrained run) 6; entered 54 (0 by swap, 54 curator beyond budget); blocked 6
- previous rows the unconstrained run drops 8: displaced 0, kept as frozen 8, kept without a same-class entrant 0
- previous rows now headed by another version (identity kept) 0; previous rows no longer eligible (kept verbatim unless displaced) 0; paper_id changes of kept uids 0

| class | budget | previous | candidates | entered | displaced | blocked | dropped by rules, kept frozen | new |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| amplifier | 45 | 45 | 1 | 4 | 0 | 1 | 1 (of 1 dropped) | 49 |
| chip_chip_coupler | 40 | 39 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 39 |
| crossing | 30 | 33 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 33 |
| fiber_chip_coupler | 60 | 60 | 1 | 0 | 0 | 1 | 1 (of 1 dropped) | 60 |
| fiber_interface | 30 | 31 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 31 |
| free_space_emitter | 40 | 40 | 0 | 1 | 0 | 0 | 0 (of 0 dropped) | 41 |
| frequency_converter | 30 | 30 | 0 | 4 | 0 | 0 | 0 (of 0 dropped) | 34 |
| laser | 90 | 102 | 1 | 25 | 0 | 1 | 1 (of 1 dropped) | 127 |
| micro_optics | 35 | 35 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 35 |
| mode_converter | 35 | 35 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 35 |
| nonreciprocal | 30 | 30 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 30 |
| phase_shifter | 60 | 60 | 1 | 0 | 0 | 1 | 1 (of 1 dropped) | 60 |
| photodetector | 70 | 76 | 1 | 0 | 0 | 1 | 0 (of 0 dropped) | 76 |
| polarization | 45 | 45 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 45 |
| reflector | 30 | 30 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 30 |
| resonator | 60 | 60 | 0 | 9 | 0 | 0 | 0 (of 0 dropped) | 69 |
| splitter | 50 | 50 | 0 | 3 | 0 | 0 | 0 (of 0 dropped) | 53 |
| switch_fabric | 45 | 52 | 0 | 1 | 0 | 0 | 2 (of 2 dropped) | 53 |
| waveguide_platform | 60 | 68 | 1 | 6 | 0 | 1 | 1 (of 1 dropped) | 74 |
| wdm | 80 | 81 | 0 | 1 | 0 | 0 | 1 (of 1 dropped) | 82 |
| total | 965 | 1002 | 6 | 54 | 0 | 6 | 8 (of 8) | 1056 |

### Entering

| paper_id | class | subtype | score | access | venue | year | rule | displaces | title |
|---|---|---|---:|---|---|---|---|---|---|
| chen2025a | amplifier | amplifier.parametric | 8 | oa | Optica | 2025 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): CW-pumped OPA (domain-engineered waveguide) | (beyond budget) | High-gain optical parametric amplification with a continuous-wave pump using a domain-engineered thin-film lithium niobate waveguide |
| dean2025 | amplifier | amplifier.parametric | 8 | oa | arXiv | 2025 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): TFLN OPA via SH resonance | (beyond budget) | Low-power integrated optical parametric amplification via second-harmonic resonance |
| hazan2022 | amplifier | amplifier.soa | 8 | oa | IEEE photonics journal | 2022 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): 1300 nm SOA in InP generic platform (SMART) | (beyond budget) | 1300 nm Semiconductor Optical Amplifier Compatible With an InP Monolithic Active/Passive Integration Technology |
| kashiwazaki2021 | amplifier | amplifier.parametric | 8 | oa | NTT technical review | 2021 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): PPLN waveguide OPA module | (beyond budget) | High-gain Optical Parametric Amplifier Module by Using a PPLN Waveguide and Its Application to Quadrature Squeezing |
| poulton2016 | free_space_emitter | free_space_emitter.grating_emitter | 8 | paywalled | Optics Letters | 2016 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): SiN optical phased arrays (MMI tree, emitters) | (beyond budget) | Large-scale silicon nitride nanophotonic phased arrays at infrared and visible wavelengths |
| li2025d | frequency_converter | frequency_converter.sfg_dfg | 8 | oa | APL Photonics | 2025 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): two-stage TFLN wavelength conversion | (beyond budget) | Two-stage lithium niobate nonlinear photonic circuits for low-crosstalk and broadband all optical wavelength conversion |
| stokowski2024 | frequency_converter | frequency_converter.other | 8 | oa | Nature | 2024 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): TFLN FM OPO | (beyond budget) | Integrated frequency-modulated optical parametric oscillator |
| xin2024 | frequency_converter | frequency_converter.shg | 8 | oa | arXiv | 2024 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): wafer-scale TFLN SHG mixers | (beyond budget) | Wavelength-accurate and wafer-scale process for nonlinear frequency mixers in thin-film lithium niobate |
| kashiwazaki2021a | frequency_converter | frequency_converter.shg | 8 | oa | Applied Physics Letters | 2021 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): low-loss PPLN waveguide | (beyond budget) | Fabrication of low-loss quasi-single-mode PPLN waveguide and its application to a modularized broadband high-level squeezer |
| chen2020 | laser | laser.tunable | 9 | paywalled | Photonics Research | 2020 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): thermally tuned MCI tunable laser | (beyond budget) | Narrow-linewidth thermally tuned multi-channel interference widely tunable semiconductor laser with thermal tuning power below 50 mW |
| xie2026a | laser | laser.dfb | 8 | oa | Optics Express | 2026 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_02): >300 mW O-band 8-ch DFB array | (beyond budget) | Over 300 mW O-band 8-channel DFB laser array for optical I/O technology |
| mehta2026 | laser | laser.soa_dfb | 8 | oa | IEEE Electronic Components and Technology Conference (ECTC) | 2026 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_02): DWDM CW DFB-SOA array in ELSFP (NVIDIA / Lumentum) | (beyond budget) | Design and Packaging of a DWDM CW-DFB Laser Array for Co-Integrated Optical Interconnects |
| wang2025a | laser | laser.comb | 8 | oa | Optics Express | 2025 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_08): flat-top TFLN EO comb | (beyond budget) | Highly tunable flat-top thin-film lithium niobate electro-optic frequency comb generator with 148 comb lines |
| zhou2025 | laser | laser.tunable | 8 | oa | Laser & Photonics Review | 2025 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): TFLN EO-tunable MCI laser | (beyond budget) | An Integrated Electro‐Optically Tunable Multi‐Channel Interference Cavity Laser |
| babichev2025 | laser | laser.other | 8 | oa | IEEE Journal of Quantum Electronics | 2025 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): 1300 nm superlattice lasers | (beyond budget) | Gain and Threshold Improvements of 1300 nm Lasers Based on InGaAs/InAlGaAs Superlattice Active Regions |
| fan2025a | laser | laser.ecl | 8 | oa | Chinese Optics Letters | 2025 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): hybrid ECL with cascaded loop mirrors | (beyond budget) | Wavelength and reflectivity tunable hybrid integrated external cavity laser using cascaded micro-rings with wide-bandwidth adjustable Sagnac-loop reflectors |
| zhang2024c | laser | laser.comb | 8 | oa | Nature Communications | 2024 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_08): parallel high-coherence sources (comb, DFB, SOA) | (beyond budget) | High-coherence parallelization in integrated photonics |
| ling2024 | laser | laser.comb | 8 | oa | Nature Communications | 2024 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_08): electrically empowered microcomb laser | (beyond budget) | Electrically empowered microcomb laser |
| helgason2023 | laser | laser.comb | 8 | oa | Nature Photonics | 2023 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_08): coupled-ring microcomb efficiency | (beyond budget) | Surpassing the nonlinear conversion efficiency of soliton microcombs |
| guo2023 | laser | laser.other | 8 | oa | arXiv | 2023 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): mode-locked laser in TFLN | (beyond budget) | Mode-locked laser in nanophotonic lithium niobate |
| hu2022 | laser | laser.comb | 8 | oa | Nature Photonics | 2022 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_08): TFLN EO comb generators | (beyond budget) | High-efficiency and broadband on-chip electro-optic frequency comb generators |
| li2022 | laser | laser.tunable | 8 | oa | Nature Communications | 2022 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): integrated Pockels laser | (beyond budget) | Integrated Pockels laser |
| xiang2021 | laser | laser.comb | 8 | oa | Science | 2021 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): laser soliton microcombs on Si | (beyond budget) | Laser soliton microcombs heterogeneously integrated on silicon |
| xiang2021a | laser | laser.heterogeneous | 8 | oa | Nature Communications | 2021 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): lasers for SiN photonics (own data; overview, rule 3 per value) | (beyond budget) | High-performance lasers for fully integrated silicon nitride photonics |
| shen2020 | laser | laser.comb | 8 | oa | Nature | 2020 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): turnkey soliton microcomb (SIL) | (beyond budget) | Integrated turnkey soliton microcombs |
| liu2020a | laser | laser.comb | 8 | oa | Nature | 2020 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): piezo-controlled SiN microcomb (AlN actuator) | (beyond budget) | Monolithic piezoelectric control of soliton microcombs |
| zhang2019b | laser | laser.comb | 8 | oa | Nature | 2019 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_08): TFLN microring EO comb | (beyond budget) | Broadband electro-optic frequency comb generation in a lithium niobate microring resonator |
| raja2019 | laser | laser.comb | 8 | oa | Nature Communications | 2019 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): electrically pumped integrated microcomb | (beyond budget) | Electrically pumped photonic integrated soliton microcomb |
| dutt2018 | laser | laser.comb | 8 | oa | Science Advances | 2018 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): on-chip dual comb (SiN rings, heaters) | (beyond budget) | On-chip dual-comb source for spectroscopy |
| liu2018a | laser | laser.comb | 8 | oa | Optica | 2018 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): low-power soliton microcombs, Q, edge coupling | (beyond budget) | Ultralow-power chip-based soliton microcombs for photonic integration |
| levy2026 | laser | laser.dfb | 8 | paywalled | Journal of Lightwave Technology | 2026 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_02): DFB array wavelength-spacing control (Intel) | (beyond budget) | Precision Wavelength-Spacing Controller for Continuous Control of a DFB laser array |
| hatai2024 | laser | laser.soa_dfb | 8 | paywalled | Optical Fiber Communication Conference (OFC) 2024 | 2024 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_02): CW-WDM MSA 8-ch CW-DFB laser array, 100 mW (D923: Optica DOI verified, title match) | (beyond budget) | CW-WDM MSA compatible 100-mW (up to 50°C), 400-GHz spacing highly-reliable CW-DFB 8-channel laser array |
| mao2024 | laser | laser.dfb | 8 | paywalled | Optical Fiber Communication Conference (OFC) 2024 | 2024 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_02): high-power reliable DFB | (beyond budget) | Development of High-Power DFB Lasers with High Reliability |
| zhou2022b | laser | laser.dfb | 8 | paywalled | Conference on Lasers and Electro-Optics | 2022 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_02): high-power CW laser for CPO | (beyond budget) | High Power CW Laser for Co-Packaged Optics |
| ji2020 | resonator | resonator.ring | 9 | oa | Laser & Photonics Review | 2020 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): ultralow-loss multimode waveguide rings (Q, loss) | (beyond budget) | Exploiting Ultralow Loss Multimode Waveguides for Broadband Frequency Combs |
| shim2026 | resonator | resonator.ring | 8 | oa | ACS Photonics | 2026 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_04): TFLN anisotropic thermo-optic response (rings) | (beyond budget) | Generalized Model of Anisotropic Thermo-Optic Response on Thin-Film Lithium Niobate Platform |
| beals2026 | resonator | resonator.other | 8 | oa | arXiv | 2026 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): ultra-compact Kerr soliton resonators | (beyond budget) | Kerr Soliton Generation in Ultra-Compact Photonic Devices |
| sun2024 | resonator | resonator.other | 8 | oa | Nature | 2024 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): integrated optical frequency division (resonator, PD) | (beyond budget) | Integrated optical frequency division for microwave and mmWave generation |
| kramnik2024 | resonator | resonator.ring | 8 | oa | arXiv | 2024 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): GF 45RFSOI CMOS photon-pair rings + feedback (GF fab) | (beyond budget) | Scalable Feedback Stabilization of Quantum Light Sources on a CMOS Chip |
| rizzo2023 | resonator | resonator.disk | 8 | oa | Nature Photonics | 2023 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): Kerr-comb SiP link with measured microdisk / interleaver (AIM fab) | (beyond budget) | Massively scalable Kerr comb-driven silicon photonic link |
| li2019 | resonator | resonator.photonic_crystal | 8 | oa | Laser & Photonics Review | 2019 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_04): LN photonic-crystal nanoresonators, Q | (beyond budget) | High‐Q 2D Lithium Niobate Photonic Crystal Slab Nanoresonators |
| yu2016 | resonator | resonator.other | 8 | oa | Optica | 2016 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): Si mid-IR microresonator comb (Q, comb) | (beyond budget) | Mode-locked mid-infrared frequency combs in a silicon microresonator |
| hu2021b | resonator | resonator.coupled_rings | 6 | oa | Nature | 2021 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_04): TFLN EO frequency shifters / beam splitters (EO devices; check EO atlas scope) | (beyond budget) | On-chip electro-optic frequency shifters and beam splitters |
| tian2025 | splitter | splitter.other | 8 | oa | Optical and Quantum Electronics | 2025 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): SOI star-coupler splitter | (beyond budget) | Silicon-based star coupler power splitter with enhanced non-uniformity |
| masanovic2003 | splitter | splitter.mmi | 8 | paywalled | IEEE Photonics Technology Letters | 2003 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): InP two-stage 1x2 MMI splitter | (beyond budget) | Multimode interference-based two-stage 1 /spl times/ 2 light splitter for compact photonic integrated circuits |
| ma2000 | splitter | splitter.mmi | 8 | paywalled | IEEE Photonics Technology Letters | 2000 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): deep-etched MMI 3-dB coupler, measured | (beyond budget) | Ultracompact multimode interference 3-dB coupler with strong lateral confinement by deep dry etching |
| wu2023a | switch_fabric | switch_fabric.mzi_mesh | 8 | oa |  | 2023 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_04): TFLN programmable 4x4 mesh (EO; check EO atlas) | (beyond budget) | Electro-optically programmable photonic circuits enabled by wafer-scale integration on thin-film lithium niobate |
| chen2026c | waveguide_platform | waveguide_platform.straight | 8 | oa | arXiv | 2026 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): ultralow-loss SiN quantum platform (MMI, ring, crossing, heater) | (beyond budget) | An ultralow-loss integrated photonic platform for discrete-variable quantum information processing |
| dagostino2015 | waveguide_platform | waveguide_platform.straight | 8 | oa | Optics Express | 2015 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): Zn-diffused low-loss InP passive waveguides, ring, MMI | (beyond budget) | Low-loss passive waveguides in a generic InP foundry process via local diffusion of zinc |
| yeh2024 | waveguide_platform | waveguide_platform.straight | 8 | paywalled | Technical digest - International Electron Devices Meeting/Technical digest | 2024 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): TSMC SiPh platform (GC, waveguide, PD, MOD) (TSMC fab) | (beyond budget) | Silicon Photonics Platform for Next Generation Data Communication Technologies |
| fahrenkopf2019 | waveguide_platform | waveguide_platform.straight | 2 | oa | IEEE Journal of Selected Topics in Quantum Electronics | 2019 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): AIM Photonics MPW platform data (AIM fab) | (beyond budget) | The AIM Photonics MPW: A Highly Accessible Cutting Edge Technology for Rapid Prototyping of Photonic Integrated Circuits |
| worhoff2015 | waveguide_platform | waveguide_platform.straight | 2 | oa | Advanced Optical Technologies | 2015 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): TriPleX platform overview (LioniX); own platform data, check rule 3 per value | (beyond budget) | TriPleX: a versatile dielectric photonic platform |
| roeloffzen2018 | waveguide_platform | waveguide_platform.straight | 0 | oa | IEEE Journal of Selected Topics in Quantum Electronics | 2018 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): TriPleX waveguide overview (LioniX); own data, check rule 3 per value | (beyond budget) | Low-Loss Si3N4 TriPleX Optical Waveguides: Technology and Applications Overview |
| gatkine2022 | wdm | wdm.awg | 8 | oa | arXiv | 2022 | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_04): astrophotonic AWG spectrograph (LIGENTEC SiN) | (beyond budget) | An on-chip astrophotonic spectrograph with a resolving power of 12,000 |

### Displaced

| paper_id | class | score | access | day | route | previous reason | by | title |
|---|---|---:|---|---:|---|---|---|---|

### Blocked entering candidates

| uid | class | score | access | why | title |
|---|---|---:|---|---|---|
| 10.1364/ofc.2022.w3j.6 | amplifier | 9 | oa | no displaceable incumbent of the class on days 3-10 | 3D printed and spiral lithographically patterned erbium-doped polymer micro-waveguide amplifiers |
| 10.1063/5.0324732 | fiber_chip_coupler | 9 | oa | no displaceable incumbent of the class on days 3-10 | High-efficiency scalable hybrid silicon grating couplers for thin-film lithium niobate photonics |
| 10.1038/s41598-026-50776-9 | laser | 9 | oa | no displaceable incumbent of the class on days 3-10 | Narrow-linewidth photonic wirebonded silicon nitride external cavity tunable laser |
| 10.1038/s41598-022-21590-w | phase_shifter | 9 | oa | no displaceable incumbent of the class on days 3-10 | Thermo-optic tuning of silicon nitride microring resonators with low loss non-volatile $$\hbox {Sb}_{2}\hbox {S}_{3}$$ phase change material |
| 10.1063/1.4941995 | photodetector | 9 | oa | no displaceable incumbent of the class on days 3-10 | Resonance-enhanced waveguide-coupled silicon-germanium detector |
| 10.1063/5.0221409 | waveguide_platform | 10 | paywalled | no displaceable incumbent of the class on days 3-10 | 300-nm-thick, ultralow-loss silicon nitride photonic integrated circuits by 8-in. foundry production |

### Dropped by the unconstrained run, kept (frozen or curator)

| paper_id | class | score | why kept | previous reason | title |
|---|---|---:|---|---|---|
| ronn2019 | amplifier | 9 | cached | rank | Ultra-high on-chip optical gain in erbium-based hybrid slot waveguides |
| wu2025 | fiber_chip_coupler | 9 | queue day 2 | rank | Ultra-low-loss polarization-splitting grating coupler based on inverse-design |
| heim2025 | laser | 9 | cached | reserve: best remaining | Hybrid integrated ultra-low linewidth coil stabilized isolator-free widely tunable external cavity laser |
| meng2023 | phase_shifter | 8 | cached | rank | Electrical programmable multilevel nonvolatile photonic random-access memory |
| xia2026 | switch_fabric | 9 | cached | reserve: best remaining | Assessment of low polarization sensitive InP photonic integrated multicast and select switch with commercial 400G-ZR transceivers |
| zali2026 | switch_fabric | 9 | cached | reserve: best remaining | Densely integrated low polarization dependent 8 × 8 optical switch for optical network applications |
| li2026a | waveguide_platform | 9 | cached | reserve: best remaining | Mid-infrared-to-ultraviolet supercontinuum generation in low-loss tantalum pentoxide nanophotonic waveguides |
| amorim2017 | wdm | 9 | cached | rank | Monolithic Add–Drop Multiplexers in Fused Silica Fabricated by Femtosecond Laser Direct Writing |

## DevLog-015 owner add delta (2026-11-07): 1 beyond_budget curator add, OFC 2025 Th1G.2 (cov_tsmc2, D921, D926)

Post-run correction: the run also rewrote 4 previous rows from their scored record (liu2018a primary_class laser -> resonator, guo2023 and zhou2025 subtype, alexander2024 arxiv_id cleared); these rows were restored verbatim from the pre-run list and only the new row was inserted (ranks renumbered).

Generated 2026-11-07 by `scripts/lit_select.py --delta` (applied: cache_list.csv rewritten). Rules: budget 1000; frozen = cached papers, queue days 1-2, curator picks; a work outside the previous list enters only by displacing a not-yet-retrieved incumbent of its primary class on days 3-10 that the unconstrained `selection.yaml` run drops; senior-author cap and paywalled share re-checked per swap; a curator pick without such a slot enters beyond the class budget (D511); curation adds flagged beyond_budget enter beyond the class budget without a swap or cap check and stay out of the unconstrained run (D926).

- previous rows 1056; new rows 1057; entering candidates (unconstrained run) 6; entered 1 (0 by swap, 1 curator beyond budget); blocked 60
- previous rows the unconstrained run drops 62: displaced 0, kept as frozen 62, kept without a same-class entrant 0
- previous rows now headed by another version (identity kept) 0; previous rows no longer eligible (kept verbatim unless displaced) 42; paper_id changes of kept uids 0

| class | budget | previous | candidates | entered | displaced | blocked | dropped by rules, kept frozen | new |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| amplifier | 45 | 49 | 1 | 0 | 0 | 5 | 5 (of 5 dropped) | 49 |
| chip_chip_coupler | 40 | 39 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 39 |
| crossing | 30 | 33 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 33 |
| fiber_chip_coupler | 60 | 60 | 1 | 0 | 0 | 1 | 1 (of 1 dropped) | 60 |
| fiber_interface | 30 | 31 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 31 |
| free_space_emitter | 40 | 41 | 0 | 0 | 0 | 1 | 1 (of 1 dropped) | 41 |
| frequency_converter | 30 | 34 | 0 | 0 | 0 | 4 | 4 (of 4 dropped) | 34 |
| laser | 90 | 127 | 1 | 0 | 0 | 26 | 26 (of 26 dropped) | 126 |
| micro_optics | 35 | 35 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 35 |
| mode_converter | 35 | 35 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 35 |
| nonreciprocal | 30 | 30 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 30 |
| phase_shifter | 60 | 60 | 1 | 0 | 0 | 1 | 1 (of 1 dropped) | 60 |
| photodetector | 70 | 76 | 1 | 0 | 0 | 1 | 0 (of 0 dropped) | 76 |
| polarization | 45 | 45 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 45 |
| reflector | 30 | 30 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 30 |
| resonator | 60 | 69 | 0 | 0 | 0 | 9 | 9 (of 9 dropped) | 70 |
| splitter | 50 | 53 | 0 | 0 | 0 | 3 | 3 (of 3 dropped) | 53 |
| switch_fabric | 45 | 53 | 0 | 0 | 0 | 1 | 3 (of 3 dropped) | 53 |
| waveguide_platform | 60 | 74 | 1 | 1 | 0 | 7 | 7 (of 7 dropped) | 75 |
| wdm | 80 | 82 | 0 | 0 | 0 | 1 | 2 (of 2 dropped) | 82 |
| total | 965 | 1056 | 6 | 1 | 0 | 60 | 62 (of 62) | 1057 |

### Entering

| paper_id | class | subtype | score | access | venue | year | rule | displaces | title |
|---|---|---|---:|---|---|---|---|---|---|
| lu2025a | waveguide_platform | waveguide_platform.straight | 8 | paywalled | Optical Fiber Communication Conference (OFC) 2025 | 2025 | curator: add: owner add 2026-11-07 (DevLog-015, cov_tsmc2): TSMC SiPh-integrated PECVD SiN building blocks (waveguide, bend, taper, crossing, MMI, SiN-Si transition, edge coupler) | (beyond budget) | Low-loss High-uniformity Silicon Nitride Optical Building Blocks Integrated on Silicon Photonics Platform |

### Displaced

| paper_id | class | score | access | day | route | previous reason | by | title |
|---|---|---:|---|---:|---|---|---|---|

### Blocked entering candidates

| uid | class | score | access | why | title |
|---|---|---:|---|---|---|
| 10.1364/ofc.2022.w3j.6 | amplifier | 9 | oa | no displaceable incumbent of the class on days 3-10 | 3D printed and spiral lithographically patterned erbium-doped polymer micro-waveguide amplifiers |
| 10.1364/optica.565112 | amplifier | 8 | oa | beyond_budget add already in the list | High-gain optical parametric amplification with a continuous-wave pump using a domain-engineered thin-film lithium niobate waveguide |
| arxiv:2509.26425 | amplifier | 8 | oa | beyond_budget add already in the list | Low-power integrated optical parametric amplification via second-harmonic resonance |
| 10.1109/jphot.2022.3175373 | amplifier | 8 | oa | beyond_budget add already in the list | 1300 nm Semiconductor Optical Amplifier Compatible With an InP Monolithic Active/Passive Integration Technology |
| 10.53829/ntr202111ra1 | amplifier | 8 | oa | beyond_budget add already in the list | High-gain Optical Parametric Amplifier Module by Using a PPLN Waveguide and Its Application to Quadrature Squeezing |
| 10.1063/5.0324732 | fiber_chip_coupler | 9 | oa | no displaceable incumbent of the class on days 3-10 | High-efficiency scalable hybrid silicon grating couplers for thin-film lithium niobate photonics |
| 10.1364/ol.42.000021 | free_space_emitter | 8 | paywalled | beyond_budget add already in the list | Large-scale silicon nitride nanophotonic phased arrays at infrared and visible wavelengths |
| 10.1063/5.0268177 | frequency_converter | 8 | oa | beyond_budget add already in the list | Two-stage lithium niobate nonlinear photonic circuits for low-crosstalk and broadband all optical wavelength conversion |
| 10.1038/s41586-024-07071-2 | frequency_converter | 8 | oa | beyond_budget add already in the list | Integrated frequency-modulated optical parametric oscillator |
| arxiv:2404.12381 | frequency_converter | 8 | oa | beyond_budget add already in the list | Wavelength-accurate and wafer-scale process for nonlinear frequency mixers in thin-film lithium niobate |
| 10.1063/5.0063118 | frequency_converter | 8 | oa | beyond_budget add already in the list | Fabrication of low-loss quasi-single-mode PPLN waveguide and its application to a modularized broadband high-level squeezer |
| 10.1038/s41598-026-50776-9 | laser | 9 | oa | no displaceable incumbent of the class on days 3-10 | Narrow-linewidth photonic wirebonded silicon nitride external cavity tunable laser |
| 10.1364/prj.380002 | laser | 9 | paywalled | beyond_budget add already in the list | Narrow-linewidth thermally tuned multi-channel interference widely tunable semiconductor laser with thermal tuning power below 50 mW |
| 10.1364/oe.581698 | laser | 8 | oa | beyond_budget add already in the list | Over 300 mW O-band 8-channel DFB laser array for optical I/O technology |
| 10.1109/ectc51846.2026.00021 | laser | 8 | oa | beyond_budget add already in the list | Design and Packaging of a DWDM CW-DFB Laser Array for Co-Integrated Optical Interconnects |
| 10.1364/oe.561993 | laser | 8 | oa | beyond_budget add already in the list | Highly tunable flat-top thin-film lithium niobate electro-optic frequency comb generator with 148 comb lines |
| 10.1002/lpor.202401664 | laser | 8 | oa | beyond_budget add already in the list | An Integrated Electro‐Optically Tunable Multi‐Channel Interference Cavity Laser |
| 10.1109/jqe.2025.3553022 | laser | 8 | oa | beyond_budget add already in the list | Gain and Threshold Improvements of 1300 nm Lasers Based on InGaAs/InAlGaAs Superlattice Active Regions |
| 10.3788/col202523.081301 | laser | 8 | oa | beyond_budget add already in the list | Wavelength and reflectivity tunable hybrid integrated external cavity laser using cascaded micro-rings with wide-bandwidth adjustable Sagnac-loop reflectors |
| 10.1038/s41467-024-52269-7 | laser | 8 | oa | beyond_budget add already in the list | High-coherence parallelization in integrated photonics |
| 10.1038/s41467-024-48544-2 | laser | 8 | oa | beyond_budget add already in the list | Electrically empowered microcomb laser |
| 10.1038/s41566-023-01280-3 | laser | 8 | oa | beyond_budget add already in the list | Surpassing the nonlinear conversion efficiency of soliton microcombs |
| arxiv:2306.05314 | laser | 8 | oa | beyond_budget add already in the list | Mode-locked laser in nanophotonic lithium niobate |
| 10.1038/s41566-022-01059-y | laser | 8 | oa | beyond_budget add already in the list | High-efficiency and broadband on-chip electro-optic frequency comb generators |
| 10.1038/s41467-022-33101-6 | laser | 8 | oa | beyond_budget add already in the list | Integrated Pockels laser |
| 10.1126/science.abh2076 | laser | 8 | oa | beyond_budget add already in the list | Laser soliton microcombs heterogeneously integrated on silicon |
| 10.1038/s41467-021-26804-9 | laser | 8 | oa | beyond_budget add already in the list | High-performance lasers for fully integrated silicon nitride photonics |
| 10.1038/s41586-020-2358-x | laser | 8 | oa | beyond_budget add already in the list | Integrated turnkey soliton microcombs |
| 10.1038/s41586-020-2465-8 | laser | 8 | oa | beyond_budget add already in the list | Monolithic piezoelectric control of soliton microcombs |
| 10.1038/s41586-019-1008-7 | laser | 8 | oa | beyond_budget add already in the list | Broadband electro-optic frequency comb generation in a lithium niobate microring resonator |
| 10.1038/s41467-019-08498-2 | laser | 8 | oa | beyond_budget add already in the list | Electrically pumped photonic integrated soliton microcomb |
| 10.1126/sciadv.1701858 | laser | 8 | oa | beyond_budget add already in the list | On-chip dual-comb source for spectroscopy |
| 10.1364/optica.5.001347 | laser | 8 | oa | beyond_budget add already in the list | Ultralow-power chip-based soliton microcombs for photonic integration |
| 10.1109/jlt.2026.3739658 | laser | 8 | paywalled | beyond_budget add already in the list | Precision Wavelength-Spacing Controller for Continuous Control of a DFB laser array |
| 10.1364/ofc.2024.m1d.1 | laser | 8 | paywalled | beyond_budget add already in the list | CW-WDM MSA compatible 100-mW (up to 50°C), 400-GHz spacing highly-reliable CW-DFB 8-channel laser array |
| 10.1364/ofc.2024.m1d.3 | laser | 8 | paywalled | beyond_budget add already in the list | Development of High-Power DFB Lasers with High Reliability |
| 10.1364/cleo_si.2022.ss2d.3 | laser | 8 | paywalled | beyond_budget add already in the list | High Power CW Laser for Co-Packaged Optics |
| 10.1038/s41598-022-21590-w | phase_shifter | 9 | oa | no displaceable incumbent of the class on days 3-10 | Thermo-optic tuning of silicon nitride microring resonators with low loss non-volatile $$\hbox {Sb}_{2}\hbox {S}_{3}$$ phase change material |
| 10.1063/1.4941995 | photodetector | 9 | oa | no displaceable incumbent of the class on days 3-10 | Resonance-enhanced waveguide-coupled silicon-germanium detector |
| 10.1002/lpor.202000353 | resonator | 9 | oa | beyond_budget add already in the list | Exploiting Ultralow Loss Multimode Waveguides for Broadband Frequency Combs |
| 10.1021/acsphotonics.6c00117 | resonator | 8 | oa | beyond_budget add already in the list | Generalized Model of Anisotropic Thermo-Optic Response on Thin-Film Lithium Niobate Platform |
| arxiv:2606.18067 | resonator | 8 | oa | beyond_budget add already in the list | Kerr Soliton Generation in Ultra-Compact Photonic Devices |
| 10.1038/s41586-024-07057-0 | resonator | 8 | oa | beyond_budget add already in the list | Integrated optical frequency division for microwave and mmWave generation |
| arxiv:2411.05921 | resonator | 8 | oa | beyond_budget add already in the list | Scalable Feedback Stabilization of Quantum Light Sources on a CMOS Chip |
| 10.1038/s41566-023-01244-7 | resonator | 8 | oa | beyond_budget add already in the list | Massively scalable Kerr comb-driven silicon photonic link |
| 10.1002/lpor.201800228 | resonator | 8 | oa | beyond_budget add already in the list | High‐Q 2D Lithium Niobate Photonic Crystal Slab Nanoresonators |
| 10.1364/optica.3.000854 | resonator | 8 | oa | beyond_budget add already in the list | Mode-locked mid-infrared frequency combs in a silicon microresonator |
| 10.1038/s41586-021-03999-x | resonator | 6 | oa | beyond_budget add already in the list | On-chip electro-optic frequency shifters and beam splitters |
| 10.1007/s11082-024-07958-4 | splitter | 8 | oa | beyond_budget add already in the list | Silicon-based star coupler power splitter with enhanced non-uniformity |
| 10.1109/lpt.2003.809972 | splitter | 8 | paywalled | beyond_budget add already in the list | Multimode interference-based two-stage 1 /spl times/ 2 light splitter for compact photonic integrated circuits |
| 10.1109/68.841263 | splitter | 8 | paywalled | beyond_budget add already in the list | Ultracompact multimode interference 3-dB coupler with strong lateral confinement by deep dry etching |
| 10.1364/opticaopen.22573447 | switch_fabric | 8 | oa | beyond_budget add already in the list | Electro-optically programmable photonic circuits enabled by wafer-scale integration on thin-film lithium niobate |
| 10.1063/5.0221409 | waveguide_platform | 10 | paywalled | no displaceable incumbent of the class on days 3-10 | 300-nm-thick, ultralow-loss silicon nitride photonic integrated circuits by 8-in. foundry production |
| arxiv:2606.26910 | waveguide_platform | 8 | oa | beyond_budget add already in the list | An ultralow-loss integrated photonic platform for discrete-variable quantum information processing |
| 10.1364/oe.23.025143 | waveguide_platform | 8 | oa | beyond_budget add already in the list | Low-loss passive waveguides in a generic InP foundry process via local diffusion of zinc |
| 10.1109/iedm50854.2024.10873369 | waveguide_platform | 8 | paywalled | beyond_budget add already in the list | Silicon Photonics Platform for Next Generation Data Communication Technologies |
| 10.1109/jstqe.2019.2935698 | waveguide_platform | 2 | oa | beyond_budget add already in the list | The AIM Photonics MPW: A Highly Accessible Cutting Edge Technology for Rapid Prototyping of Photonic Integrated Circuits |
| 10.1515/aot-2015-0016 | waveguide_platform | 2 | oa | beyond_budget add already in the list | TriPleX: a versatile dielectric photonic platform |
| 10.1109/jstqe.2018.2793945 | waveguide_platform | 0 | oa | beyond_budget add already in the list | Low-Loss Si3N4 TriPleX Optical Waveguides: Technology and Applications Overview |
| arxiv:2203.07867 | wdm | 8 | oa | beyond_budget add already in the list | An on-chip astrophotonic spectrograph with a resolving power of 12,000 |

### Dropped by the unconstrained run, kept (frozen or curator)

| paper_id | class | score | why kept | previous reason | title |
|---|---|---:|---|---|---|
| chen2025a | amplifier | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): CW-pumped OPA (domain-engineered waveguide) | High-gain optical parametric amplification with a continuous-wave pump using a domain-engineered thin-film lithium niobate waveguide |
| dean2025 | amplifier | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): TFLN OPA via SH resonance | Low-power integrated optical parametric amplification via second-harmonic resonance |
| hazan2022 | amplifier | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): 1300 nm SOA in InP generic platform (SMART) | 1300 nm Semiconductor Optical Amplifier Compatible With an InP Monolithic Active/Passive Integration Technology |
| kashiwazaki2021 | amplifier | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): PPLN waveguide OPA module | High-gain Optical Parametric Amplifier Module by Using a PPLN Waveguide and Its Application to Quadrature Squeezing |
| ronn2019 | amplifier | 9 | cached | rank | Ultra-high on-chip optical gain in erbium-based hybrid slot waveguides |
| wu2025 | fiber_chip_coupler | 9 | queue day 2 | rank | Ultra-low-loss polarization-splitting grating coupler based on inverse-design |
| poulton2016 | free_space_emitter | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): SiN optical phased arrays (MMI tree, emitters) | Large-scale silicon nitride nanophotonic phased arrays at infrared and visible wavelengths |
| kashiwazaki2021a | frequency_converter | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): low-loss PPLN waveguide | Fabrication of low-loss quasi-single-mode PPLN waveguide and its application to a modularized broadband high-level squeezer |
| li2025d | frequency_converter | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): two-stage TFLN wavelength conversion | Two-stage lithium niobate nonlinear photonic circuits for low-crosstalk and broadband all optical wavelength conversion |
| stokowski2024 | frequency_converter | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): TFLN FM OPO | Integrated frequency-modulated optical parametric oscillator |
| xin2024 | frequency_converter | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): wafer-scale TFLN SHG mixers | Wavelength-accurate and wafer-scale process for nonlinear frequency mixers in thin-film lithium niobate |
| babichev2025 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): 1300 nm superlattice lasers | Gain and Threshold Improvements of 1300 nm Lasers Based on InGaAs/InAlGaAs Superlattice Active Regions |
| chen2020 | laser | 9 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): thermally tuned MCI tunable laser | Narrow-linewidth thermally tuned multi-channel interference widely tunable semiconductor laser with thermal tuning power below 50 mW |
| dutt2018 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): on-chip dual comb (SiN rings, heaters) | On-chip dual-comb source for spectroscopy |
| fan2025a | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): hybrid ECL with cascaded loop mirrors | Wavelength and reflectivity tunable hybrid integrated external cavity laser using cascaded micro-rings with wide-bandwidth adjustable Sagnac-loop reflectors |
| guo2023 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): mode-locked laser in TFLN | Mode-locked laser in nanophotonic lithium niobate |
| hatai2024 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_02): CW-WDM MSA 8-ch CW-DFB laser array, 100 mW (D923: Optica DOI verified, title match) | CW-WDM MSA compatible 100-mW (up to 50°C), 400-GHz spacing highly-reliable CW-DFB 8-channel laser array |
| heim2025 | laser | 9 | cached | reserve: best remaining | Hybrid integrated ultra-low linewidth coil stabilized isolator-free widely tunable external cavity laser |
| helgason2023 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_08): coupled-ring microcomb efficiency | Surpassing the nonlinear conversion efficiency of soliton microcombs |
| hu2022 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_08): TFLN EO comb generators | High-efficiency and broadband on-chip electro-optic frequency comb generators |
| levy2026 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_02): DFB array wavelength-spacing control (Intel) | Precision Wavelength-Spacing Controller for Continuous Control of a DFB laser array |
| li2022 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): integrated Pockels laser | Integrated Pockels laser |
| ling2024 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_08): electrically empowered microcomb laser | Electrically empowered microcomb laser |
| liu2018a | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): low-power soliton microcombs, Q, edge coupling | Ultralow-power chip-based soliton microcombs for photonic integration |
| liu2020a | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): piezo-controlled SiN microcomb (AlN actuator) | Monolithic piezoelectric control of soliton microcombs |
| mao2024 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_02): high-power reliable DFB | Development of High-Power DFB Lasers with High Reliability |
| mehta2026 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_02): DWDM CW DFB-SOA array in ELSFP (NVIDIA / Lumentum) | Design and Packaging of a DWDM CW-DFB Laser Array for Co-Integrated Optical Interconnects |
| raja2019 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): electrically pumped integrated microcomb | Electrically pumped photonic integrated soliton microcomb |
| shen2020 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): turnkey soliton microcomb (SIL) | Integrated turnkey soliton microcombs |
| wang2025a | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_08): flat-top TFLN EO comb | Highly tunable flat-top thin-film lithium niobate electro-optic frequency comb generator with 148 comb lines |
| xiang2021 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): laser soliton microcombs on Si | Laser soliton microcombs heterogeneously integrated on silicon |
| xiang2021a | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): lasers for SiN photonics (own data; overview, rule 3 per value) | High-performance lasers for fully integrated silicon nitride photonics |
| xie2026a | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_02): >300 mW O-band 8-ch DFB array | Over 300 mW O-band 8-channel DFB laser array for optical I/O technology |
| zhang2019b | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_08): TFLN microring EO comb | Broadband electro-optic frequency comb generation in a lithium niobate microring resonator |
| zhang2024c | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_08): parallel high-coherence sources (comb, DFB, SOA) | High-coherence parallelization in integrated photonics |
| zhou2022b | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_02): high-power CW laser for CPO | High Power CW Laser for Co-Packaged Optics |
| zhou2025 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): TFLN EO-tunable MCI laser | An Integrated Electro‐Optically Tunable Multi‐Channel Interference Cavity Laser |
| meng2023 | phase_shifter | 8 | cached | rank | Electrical programmable multilevel nonvolatile photonic random-access memory |
| beals2026 | resonator | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): ultra-compact Kerr soliton resonators | Kerr Soliton Generation in Ultra-Compact Photonic Devices |
| hu2021b | resonator | 6 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_04): TFLN EO frequency shifters / beam splitters (EO devices; check EO atlas scope) | On-chip electro-optic frequency shifters and beam splitters |
| ji2020 | resonator | 9 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): ultralow-loss multimode waveguide rings (Q, loss) | Exploiting Ultralow Loss Multimode Waveguides for Broadband Frequency Combs |
| kramnik2024 | resonator | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): GF 45RFSOI CMOS photon-pair rings + feedback (GF fab) | Scalable Feedback Stabilization of Quantum Light Sources on a CMOS Chip |
| li2019 | resonator | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_04): LN photonic-crystal nanoresonators, Q | High‐Q 2D Lithium Niobate Photonic Crystal Slab Nanoresonators |
| rizzo2023 | resonator | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): Kerr-comb SiP link with measured microdisk / interleaver (AIM fab) | Massively scalable Kerr comb-driven silicon photonic link |
| shim2026 | resonator | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_04): TFLN anisotropic thermo-optic response (rings) | Generalized Model of Anisotropic Thermo-Optic Response on Thin-Film Lithium Niobate Platform |
| sun2024 | resonator | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): integrated optical frequency division (resonator, PD) | Integrated optical frequency division for microwave and mmWave generation |
| yu2016 | resonator | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): Si mid-IR microresonator comb (Q, comb) | Mode-locked mid-infrared frequency combs in a silicon microresonator |
| ma2000 | splitter | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): deep-etched MMI 3-dB coupler, measured | Ultracompact multimode interference 3-dB coupler with strong lateral confinement by deep dry etching |
| masanovic2003 | splitter | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): InP two-stage 1x2 MMI splitter | Multimode interference-based two-stage 1 /spl times/ 2 light splitter for compact photonic integrated circuits |
| tian2025 | splitter | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): SOI star-coupler splitter | Silicon-based star coupler power splitter with enhanced non-uniformity |
| wu2023a | switch_fabric | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_04): TFLN programmable 4x4 mesh (EO; check EO atlas) | Electro-optically programmable photonic circuits enabled by wafer-scale integration on thin-film lithium niobate |
| xia2026 | switch_fabric | 9 | cached | reserve: best remaining | Assessment of low polarization sensitive InP photonic integrated multicast and select switch with commercial 400G-ZR transceivers |
| zali2026 | switch_fabric | 9 | cached | reserve: best remaining | Densely integrated low polarization dependent 8 × 8 optical switch for optical network applications |
| chen2026c | waveguide_platform | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): ultralow-loss SiN quantum platform (MMI, ring, crossing, heater) | An ultralow-loss integrated photonic platform for discrete-variable quantum information processing |
| dagostino2015 | waveguide_platform | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): Zn-diffused low-loss InP passive waveguides, ring, MMI | Low-loss passive waveguides in a generic InP foundry process via local diffusion of zinc |
| fahrenkopf2019 | waveguide_platform | 2 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): AIM Photonics MPW platform data (AIM fab) | The AIM Photonics MPW: A Highly Accessible Cutting Edge Technology for Rapid Prototyping of Photonic Integrated Circuits |
| li2026a | waveguide_platform | 9 | cached | reserve: best remaining | Mid-infrared-to-ultraviolet supercontinuum generation in low-loss tantalum pentoxide nanophotonic waveguides |
| roeloffzen2018 | waveguide_platform | 0 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): TriPleX waveguide overview (LioniX); own data, check rule 3 per value | Low-Loss Si3N4 TriPleX Optical Waveguides: Technology and Applications Overview |
| worhoff2015 | waveguide_platform | 2 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): TriPleX platform overview (LioniX); own platform data, check rule 3 per value | TriPleX: a versatile dielectric photonic platform |
| yeh2024 | waveguide_platform | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): TSMC SiPh platform (GC, waveguide, PD, MOD) (TSMC fab) | Silicon Photonics Platform for Next Generation Data Communication Technologies |
| amorim2017 | wdm | 9 | cached | rank | Monolithic Add–Drop Multiplexers in Fused Silica Fabricated by Femtosecond Laser Direct Writing |
| gatkine2022 | wdm | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_04): astrophotonic AWG spectrograph (LIGENTEC SiN) | An on-chip astrophotonic spectrograph with a resolving power of 12,000 |

### Identity notes

- chen2025a (10.1364/optica.565112): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- kashiwazaki2021 (10.53829/ntr202111ra1): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- poulton2016 (10.1364/ol.42.000021): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- xin2024 (arxiv:2404.12381): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- kashiwazaki2021a (10.1063/5.0063118): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- xie2026a (10.1364/oe.581698): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- mehta2026 (10.1109/ectc51846.2026.00021): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- wang2025a (10.1364/oe.561993): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- babichev2025 (10.1109/jqe.2025.3553022): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- fan2025a (10.3788/col202523.081301): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- zhang2024c (10.1038/s41467-024-52269-7): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- ling2024 (10.1038/s41467-024-48544-2): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- helgason2023 (10.1038/s41566-023-01280-3): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- hu2022 (10.1038/s41566-022-01059-y): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- li2022 (10.1038/s41467-022-33101-6): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- xiang2021 (10.1126/science.abh2076): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- xiang2021a (10.1038/s41467-021-26804-9): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- liu2020a (10.1038/s41586-020-2465-8): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- raja2019 (10.1038/s41467-019-08498-2): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- dutt2018 (10.1126/sciadv.1701858): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- levy2026 (10.1109/jlt.2026.3739658): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- hatai2024 (10.1364/ofc.2024.m1d.1): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- mao2024 (10.1364/ofc.2024.m1d.3): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- zhou2022b (10.1364/cleo_si.2022.ss2d.3): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- shim2026 (10.1021/acsphotonics.6c00117): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- beals2026 (arxiv:2606.18067): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- sun2024 (10.1038/s41586-024-07057-0): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- kramnik2024 (arxiv:2411.05921): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- rizzo2023 (10.1038/s41566-023-01244-7): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- li2019 (10.1002/lpor.201800228): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- yu2016 (10.1364/optica.3.000854): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- hu2021b (10.1038/s41586-021-03999-x): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- tian2025 (10.1007/s11082-024-07958-4): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- masanovic2003 (10.1109/lpt.2003.809972): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- ma2000 (10.1109/68.841263): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- wu2023a (10.1364/opticaopen.22573447): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- chen2026c (arxiv:2606.26910): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- dagostino2015 (10.1364/oe.23.025143): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- yeh2024 (10.1109/iedm50854.2024.10873369): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- worhoff2015 (10.1515/aot-2015-0016): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- roeloffzen2018 (10.1109/jstqe.2018.2793945): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- gatkine2022 (arxiv:2203.07867): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim

## Delta verbatim-row fix (2026-11-07): no new rows, script-consistent ranks (D926 follow-up)

`lit_select.delta_select` now keeps every previous row that is not displaced verbatim except its rank (the post-run correction of liu2018a, guo2023, zhou2025 and alexander2024 above is now what the script produces). Backup `cache/literature/backup/s5_before_delta_verbatim_fix_20261108T044856Z.zip`. Result against the pre-run list: 0 rows added or removed, 0 content changes, 34 rank renumberings.

Generated 2026-11-07 by `scripts/lit_select.py --delta` (applied: cache_list.csv rewritten). Rules: budget 1000; frozen = cached papers, queue days 1-2, curator picks; a work outside the previous list enters only by displacing a not-yet-retrieved incumbent of its primary class on days 3-10 that the unconstrained `selection.yaml` run drops; senior-author cap and paywalled share re-checked per swap; a curator pick without such a slot enters beyond the class budget (D511); curation adds flagged beyond_budget enter beyond the class budget without a swap or cap check and stay out of the unconstrained run (D926).

- previous rows 1057; new rows 1057; entering candidates (unconstrained run) 6; entered 0 (0 by swap, 0 curator beyond budget); blocked 61
- previous rows the unconstrained run drops 63: displaced 0, kept as frozen 63, kept without a same-class entrant 0
- previous rows now headed by another version (identity kept) 0; previous rows no longer eligible (kept verbatim unless displaced) 43; paper_id changes of kept uids 0

| class | budget | previous | candidates | entered | displaced | blocked | dropped by rules, kept frozen | new |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| amplifier | 45 | 49 | 1 | 0 | 0 | 5 | 5 (of 5 dropped) | 49 |
| chip_chip_coupler | 40 | 39 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 39 |
| crossing | 30 | 33 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 33 |
| fiber_chip_coupler | 60 | 60 | 1 | 0 | 0 | 1 | 1 (of 1 dropped) | 60 |
| fiber_interface | 30 | 31 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 31 |
| free_space_emitter | 40 | 41 | 0 | 0 | 0 | 1 | 1 (of 1 dropped) | 41 |
| frequency_converter | 30 | 34 | 0 | 0 | 0 | 4 | 4 (of 4 dropped) | 34 |
| laser | 90 | 127 | 1 | 0 | 0 | 26 | 26 (of 26 dropped) | 127 |
| micro_optics | 35 | 35 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 35 |
| mode_converter | 35 | 35 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 35 |
| nonreciprocal | 30 | 30 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 30 |
| phase_shifter | 60 | 60 | 1 | 0 | 0 | 1 | 1 (of 1 dropped) | 60 |
| photodetector | 70 | 76 | 1 | 0 | 0 | 1 | 0 (of 0 dropped) | 76 |
| polarization | 45 | 45 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 45 |
| reflector | 30 | 30 | 0 | 0 | 0 | 0 | 0 (of 0 dropped) | 30 |
| resonator | 60 | 69 | 0 | 0 | 0 | 9 | 9 (of 9 dropped) | 69 |
| splitter | 50 | 53 | 0 | 0 | 0 | 3 | 3 (of 3 dropped) | 53 |
| switch_fabric | 45 | 53 | 0 | 0 | 0 | 1 | 3 (of 3 dropped) | 53 |
| waveguide_platform | 60 | 75 | 1 | 0 | 0 | 8 | 8 (of 8 dropped) | 75 |
| wdm | 80 | 82 | 0 | 0 | 0 | 1 | 2 (of 2 dropped) | 82 |
| total | 965 | 1057 | 6 | 0 | 0 | 61 | 63 (of 63) | 1057 |

### Entering

| paper_id | class | subtype | score | access | venue | year | rule | displaces | title |
|---|---|---|---:|---|---|---|---|---|---|

### Displaced

| paper_id | class | score | access | day | route | previous reason | by | title |
|---|---|---:|---|---:|---|---|---|---|

### Blocked entering candidates

| uid | class | score | access | why | title |
|---|---|---:|---|---|---|
| 10.1364/ofc.2022.w3j.6 | amplifier | 9 | oa | no displaceable incumbent of the class on days 3-10 | 3D printed and spiral lithographically patterned erbium-doped polymer micro-waveguide amplifiers |
| 10.1364/optica.565112 | amplifier | 8 | oa | beyond_budget add already in the list | High-gain optical parametric amplification with a continuous-wave pump using a domain-engineered thin-film lithium niobate waveguide |
| arxiv:2509.26425 | amplifier | 8 | oa | beyond_budget add already in the list | Low-power integrated optical parametric amplification via second-harmonic resonance |
| 10.1109/jphot.2022.3175373 | amplifier | 8 | oa | beyond_budget add already in the list | 1300 nm Semiconductor Optical Amplifier Compatible With an InP Monolithic Active/Passive Integration Technology |
| 10.53829/ntr202111ra1 | amplifier | 8 | oa | beyond_budget add already in the list | High-gain Optical Parametric Amplifier Module by Using a PPLN Waveguide and Its Application to Quadrature Squeezing |
| 10.1063/5.0324732 | fiber_chip_coupler | 9 | oa | no displaceable incumbent of the class on days 3-10 | High-efficiency scalable hybrid silicon grating couplers for thin-film lithium niobate photonics |
| 10.1364/ol.42.000021 | free_space_emitter | 8 | paywalled | beyond_budget add already in the list | Large-scale silicon nitride nanophotonic phased arrays at infrared and visible wavelengths |
| 10.1063/5.0268177 | frequency_converter | 8 | oa | beyond_budget add already in the list | Two-stage lithium niobate nonlinear photonic circuits for low-crosstalk and broadband all optical wavelength conversion |
| 10.1038/s41586-024-07071-2 | frequency_converter | 8 | oa | beyond_budget add already in the list | Integrated frequency-modulated optical parametric oscillator |
| arxiv:2404.12381 | frequency_converter | 8 | oa | beyond_budget add already in the list | Wavelength-accurate and wafer-scale process for nonlinear frequency mixers in thin-film lithium niobate |
| 10.1063/5.0063118 | frequency_converter | 8 | oa | beyond_budget add already in the list | Fabrication of low-loss quasi-single-mode PPLN waveguide and its application to a modularized broadband high-level squeezer |
| 10.1038/s41598-026-50776-9 | laser | 9 | oa | no displaceable incumbent of the class on days 3-10 | Narrow-linewidth photonic wirebonded silicon nitride external cavity tunable laser |
| 10.1364/prj.380002 | laser | 9 | paywalled | beyond_budget add already in the list | Narrow-linewidth thermally tuned multi-channel interference widely tunable semiconductor laser with thermal tuning power below 50 mW |
| 10.1364/oe.581698 | laser | 8 | oa | beyond_budget add already in the list | Over 300 mW O-band 8-channel DFB laser array for optical I/O technology |
| 10.1109/ectc51846.2026.00021 | laser | 8 | oa | beyond_budget add already in the list | Design and Packaging of a DWDM CW-DFB Laser Array for Co-Integrated Optical Interconnects |
| 10.1364/oe.561993 | laser | 8 | oa | beyond_budget add already in the list | Highly tunable flat-top thin-film lithium niobate electro-optic frequency comb generator with 148 comb lines |
| 10.1002/lpor.202401664 | laser | 8 | oa | beyond_budget add already in the list | An Integrated Electro‐Optically Tunable Multi‐Channel Interference Cavity Laser |
| 10.1109/jqe.2025.3553022 | laser | 8 | oa | beyond_budget add already in the list | Gain and Threshold Improvements of 1300 nm Lasers Based on InGaAs/InAlGaAs Superlattice Active Regions |
| 10.3788/col202523.081301 | laser | 8 | oa | beyond_budget add already in the list | Wavelength and reflectivity tunable hybrid integrated external cavity laser using cascaded micro-rings with wide-bandwidth adjustable Sagnac-loop reflectors |
| 10.1038/s41467-024-52269-7 | laser | 8 | oa | beyond_budget add already in the list | High-coherence parallelization in integrated photonics |
| 10.1038/s41467-024-48544-2 | laser | 8 | oa | beyond_budget add already in the list | Electrically empowered microcomb laser |
| 10.1038/s41566-023-01280-3 | laser | 8 | oa | beyond_budget add already in the list | Surpassing the nonlinear conversion efficiency of soliton microcombs |
| arxiv:2306.05314 | laser | 8 | oa | beyond_budget add already in the list | Mode-locked laser in nanophotonic lithium niobate |
| 10.1038/s41566-022-01059-y | laser | 8 | oa | beyond_budget add already in the list | High-efficiency and broadband on-chip electro-optic frequency comb generators |
| 10.1038/s41467-022-33101-6 | laser | 8 | oa | beyond_budget add already in the list | Integrated Pockels laser |
| 10.1126/science.abh2076 | laser | 8 | oa | beyond_budget add already in the list | Laser soliton microcombs heterogeneously integrated on silicon |
| 10.1038/s41467-021-26804-9 | laser | 8 | oa | beyond_budget add already in the list | High-performance lasers for fully integrated silicon nitride photonics |
| 10.1038/s41586-020-2358-x | laser | 8 | oa | beyond_budget add already in the list | Integrated turnkey soliton microcombs |
| 10.1038/s41586-020-2465-8 | laser | 8 | oa | beyond_budget add already in the list | Monolithic piezoelectric control of soliton microcombs |
| 10.1038/s41586-019-1008-7 | laser | 8 | oa | beyond_budget add already in the list | Broadband electro-optic frequency comb generation in a lithium niobate microring resonator |
| 10.1038/s41467-019-08498-2 | laser | 8 | oa | beyond_budget add already in the list | Electrically pumped photonic integrated soliton microcomb |
| 10.1126/sciadv.1701858 | laser | 8 | oa | beyond_budget add already in the list | On-chip dual-comb source for spectroscopy |
| 10.1364/optica.5.001347 | laser | 8 | oa | beyond_budget add already in the list | Ultralow-power chip-based soliton microcombs for photonic integration |
| 10.1109/jlt.2026.3739658 | laser | 8 | paywalled | beyond_budget add already in the list | Precision Wavelength-Spacing Controller for Continuous Control of a DFB laser array |
| 10.1364/ofc.2024.m1d.1 | laser | 8 | paywalled | beyond_budget add already in the list | CW-WDM MSA compatible 100-mW (up to 50°C), 400-GHz spacing highly-reliable CW-DFB 8-channel laser array |
| 10.1364/ofc.2024.m1d.3 | laser | 8 | paywalled | beyond_budget add already in the list | Development of High-Power DFB Lasers with High Reliability |
| 10.1364/cleo_si.2022.ss2d.3 | laser | 8 | paywalled | beyond_budget add already in the list | High Power CW Laser for Co-Packaged Optics |
| 10.1038/s41598-022-21590-w | phase_shifter | 9 | oa | no displaceable incumbent of the class on days 3-10 | Thermo-optic tuning of silicon nitride microring resonators with low loss non-volatile $$\hbox {Sb}_{2}\hbox {S}_{3}$$ phase change material |
| 10.1063/1.4941995 | photodetector | 9 | oa | no displaceable incumbent of the class on days 3-10 | Resonance-enhanced waveguide-coupled silicon-germanium detector |
| 10.1002/lpor.202000353 | resonator | 9 | oa | beyond_budget add already in the list | Exploiting Ultralow Loss Multimode Waveguides for Broadband Frequency Combs |
| 10.1021/acsphotonics.6c00117 | resonator | 8 | oa | beyond_budget add already in the list | Generalized Model of Anisotropic Thermo-Optic Response on Thin-Film Lithium Niobate Platform |
| arxiv:2606.18067 | resonator | 8 | oa | beyond_budget add already in the list | Kerr Soliton Generation in Ultra-Compact Photonic Devices |
| 10.1038/s41586-024-07057-0 | resonator | 8 | oa | beyond_budget add already in the list | Integrated optical frequency division for microwave and mmWave generation |
| arxiv:2411.05921 | resonator | 8 | oa | beyond_budget add already in the list | Scalable Feedback Stabilization of Quantum Light Sources on a CMOS Chip |
| 10.1038/s41566-023-01244-7 | resonator | 8 | oa | beyond_budget add already in the list | Massively scalable Kerr comb-driven silicon photonic link |
| 10.1002/lpor.201800228 | resonator | 8 | oa | beyond_budget add already in the list | High‐Q 2D Lithium Niobate Photonic Crystal Slab Nanoresonators |
| 10.1364/optica.3.000854 | resonator | 8 | oa | beyond_budget add already in the list | Mode-locked mid-infrared frequency combs in a silicon microresonator |
| 10.1038/s41586-021-03999-x | resonator | 6 | oa | beyond_budget add already in the list | On-chip electro-optic frequency shifters and beam splitters |
| 10.1007/s11082-024-07958-4 | splitter | 8 | oa | beyond_budget add already in the list | Silicon-based star coupler power splitter with enhanced non-uniformity |
| 10.1109/lpt.2003.809972 | splitter | 8 | paywalled | beyond_budget add already in the list | Multimode interference-based two-stage 1 /spl times/ 2 light splitter for compact photonic integrated circuits |
| 10.1109/68.841263 | splitter | 8 | paywalled | beyond_budget add already in the list | Ultracompact multimode interference 3-dB coupler with strong lateral confinement by deep dry etching |
| 10.1364/opticaopen.22573447 | switch_fabric | 8 | oa | beyond_budget add already in the list | Electro-optically programmable photonic circuits enabled by wafer-scale integration on thin-film lithium niobate |
| 10.1063/5.0221409 | waveguide_platform | 10 | paywalled | no displaceable incumbent of the class on days 3-10 | 300-nm-thick, ultralow-loss silicon nitride photonic integrated circuits by 8-in. foundry production |
| arxiv:2606.26910 | waveguide_platform | 8 | oa | beyond_budget add already in the list | An ultralow-loss integrated photonic platform for discrete-variable quantum information processing |
| 10.1364/oe.23.025143 | waveguide_platform | 8 | oa | beyond_budget add already in the list | Low-loss passive waveguides in a generic InP foundry process via local diffusion of zinc |
| 10.1364/ofc.2025.th1g.2 | waveguide_platform | 8 | paywalled | beyond_budget add already in the list | Low-loss High-uniformity Silicon Nitride Optical Building Blocks Integrated on Silicon Photonics Platform |
| 10.1109/iedm50854.2024.10873369 | waveguide_platform | 8 | paywalled | beyond_budget add already in the list | Silicon Photonics Platform for Next Generation Data Communication Technologies |
| 10.1109/jstqe.2019.2935698 | waveguide_platform | 2 | oa | beyond_budget add already in the list | The AIM Photonics MPW: A Highly Accessible Cutting Edge Technology for Rapid Prototyping of Photonic Integrated Circuits |
| 10.1515/aot-2015-0016 | waveguide_platform | 2 | oa | beyond_budget add already in the list | TriPleX: a versatile dielectric photonic platform |
| 10.1109/jstqe.2018.2793945 | waveguide_platform | 0 | oa | beyond_budget add already in the list | Low-Loss Si3N4 TriPleX Optical Waveguides: Technology and Applications Overview |
| arxiv:2203.07867 | wdm | 8 | oa | beyond_budget add already in the list | An on-chip astrophotonic spectrograph with a resolving power of 12,000 |

### Dropped by the unconstrained run, kept (frozen or curator)

| paper_id | class | score | why kept | previous reason | title |
|---|---|---:|---|---|---|
| chen2025a | amplifier | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): CW-pumped OPA (domain-engineered waveguide) | High-gain optical parametric amplification with a continuous-wave pump using a domain-engineered thin-film lithium niobate waveguide |
| dean2025 | amplifier | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): TFLN OPA via SH resonance | Low-power integrated optical parametric amplification via second-harmonic resonance |
| hazan2022 | amplifier | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): 1300 nm SOA in InP generic platform (SMART) | 1300 nm Semiconductor Optical Amplifier Compatible With an InP Monolithic Active/Passive Integration Technology |
| kashiwazaki2021 | amplifier | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): PPLN waveguide OPA module | High-gain Optical Parametric Amplifier Module by Using a PPLN Waveguide and Its Application to Quadrature Squeezing |
| ronn2019 | amplifier | 9 | cached | rank | Ultra-high on-chip optical gain in erbium-based hybrid slot waveguides |
| wu2025 | fiber_chip_coupler | 9 | queue day 2 | rank | Ultra-low-loss polarization-splitting grating coupler based on inverse-design |
| poulton2016 | free_space_emitter | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): SiN optical phased arrays (MMI tree, emitters) | Large-scale silicon nitride nanophotonic phased arrays at infrared and visible wavelengths |
| kashiwazaki2021a | frequency_converter | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): low-loss PPLN waveguide | Fabrication of low-loss quasi-single-mode PPLN waveguide and its application to a modularized broadband high-level squeezer |
| li2025d | frequency_converter | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): two-stage TFLN wavelength conversion | Two-stage lithium niobate nonlinear photonic circuits for low-crosstalk and broadband all optical wavelength conversion |
| stokowski2024 | frequency_converter | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): TFLN FM OPO | Integrated frequency-modulated optical parametric oscillator |
| xin2024 | frequency_converter | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_05): wafer-scale TFLN SHG mixers | Wavelength-accurate and wafer-scale process for nonlinear frequency mixers in thin-film lithium niobate |
| babichev2025 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): 1300 nm superlattice lasers | Gain and Threshold Improvements of 1300 nm Lasers Based on InGaAs/InAlGaAs Superlattice Active Regions |
| chen2020 | laser | 9 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): thermally tuned MCI tunable laser | Narrow-linewidth thermally tuned multi-channel interference widely tunable semiconductor laser with thermal tuning power below 50 mW |
| dutt2018 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): on-chip dual comb (SiN rings, heaters) | On-chip dual-comb source for spectroscopy |
| fan2025a | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): hybrid ECL with cascaded loop mirrors | Wavelength and reflectivity tunable hybrid integrated external cavity laser using cascaded micro-rings with wide-bandwidth adjustable Sagnac-loop reflectors |
| guo2023 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): mode-locked laser in TFLN | Mode-locked laser in nanophotonic lithium niobate |
| hatai2024 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_02): CW-WDM MSA 8-ch CW-DFB laser array, 100 mW (D923: Optica DOI verified, title match) | CW-WDM MSA compatible 100-mW (up to 50°C), 400-GHz spacing highly-reliable CW-DFB 8-channel laser array |
| heim2025 | laser | 9 | cached | reserve: best remaining | Hybrid integrated ultra-low linewidth coil stabilized isolator-free widely tunable external cavity laser |
| helgason2023 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_08): coupled-ring microcomb efficiency | Surpassing the nonlinear conversion efficiency of soliton microcombs |
| hu2022 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_08): TFLN EO comb generators | High-efficiency and broadband on-chip electro-optic frequency comb generators |
| levy2026 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_02): DFB array wavelength-spacing control (Intel) | Precision Wavelength-Spacing Controller for Continuous Control of a DFB laser array |
| li2022 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): integrated Pockels laser | Integrated Pockels laser |
| ling2024 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_08): electrically empowered microcomb laser | Electrically empowered microcomb laser |
| liu2018a | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): low-power soliton microcombs, Q, edge coupling | Ultralow-power chip-based soliton microcombs for photonic integration |
| liu2020a | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): piezo-controlled SiN microcomb (AlN actuator) | Monolithic piezoelectric control of soliton microcombs |
| mao2024 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_02): high-power reliable DFB | Development of High-Power DFB Lasers with High Reliability |
| mehta2026 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_02): DWDM CW DFB-SOA array in ELSFP (NVIDIA / Lumentum) | Design and Packaging of a DWDM CW-DFB Laser Array for Co-Integrated Optical Interconnects |
| raja2019 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): electrically pumped integrated microcomb | Electrically pumped photonic integrated soliton microcomb |
| shen2020 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): turnkey soliton microcomb (SIL) | Integrated turnkey soliton microcombs |
| wang2025a | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_08): flat-top TFLN EO comb | Highly tunable flat-top thin-film lithium niobate electro-optic frequency comb generator with 148 comb lines |
| xiang2021 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_07): laser soliton microcombs on Si | Laser soliton microcombs heterogeneously integrated on silicon |
| xiang2021a | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): lasers for SiN photonics (own data; overview, rule 3 per value) | High-performance lasers for fully integrated silicon nitride photonics |
| xie2026a | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_02): >300 mW O-band 8-ch DFB array | Over 300 mW O-band 8-channel DFB laser array for optical I/O technology |
| zhang2019b | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_08): TFLN microring EO comb | Broadband electro-optic frequency comb generation in a lithium niobate microring resonator |
| zhang2024c | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_08): parallel high-coherence sources (comb, DFB, SOA) | High-coherence parallelization in integrated photonics |
| zhou2022b | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_02): high-power CW laser for CPO | High Power CW Laser for Co-Packaged Optics |
| zhou2025 | laser | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_06): TFLN EO-tunable MCI laser | An Integrated Electro‐Optically Tunable Multi‐Channel Interference Cavity Laser |
| meng2023 | phase_shifter | 8 | cached | rank | Electrical programmable multilevel nonvolatile photonic random-access memory |
| beals2026 | resonator | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): ultra-compact Kerr soliton resonators | Kerr Soliton Generation in Ultra-Compact Photonic Devices |
| hu2021b | resonator | 6 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_04): TFLN EO frequency shifters / beam splitters (EO devices; check EO atlas scope) | On-chip electro-optic frequency shifters and beam splitters |
| ji2020 | resonator | 9 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): ultralow-loss multimode waveguide rings (Q, loss) | Exploiting Ultralow Loss Multimode Waveguides for Broadband Frequency Combs |
| kramnik2024 | resonator | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): GF 45RFSOI CMOS photon-pair rings + feedback (GF fab) | Scalable Feedback Stabilization of Quantum Light Sources on a CMOS Chip |
| li2019 | resonator | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_04): LN photonic-crystal nanoresonators, Q | High‐Q 2D Lithium Niobate Photonic Crystal Slab Nanoresonators |
| rizzo2023 | resonator | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): Kerr-comb SiP link with measured microdisk / interleaver (AIM fab) | Massively scalable Kerr comb-driven silicon photonic link |
| shim2026 | resonator | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_04): TFLN anisotropic thermo-optic response (rings) | Generalized Model of Anisotropic Thermo-Optic Response on Thin-Film Lithium Niobate Platform |
| sun2024 | resonator | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): integrated optical frequency division (resonator, PD) | Integrated optical frequency division for microwave and mmWave generation |
| yu2016 | resonator | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): Si mid-IR microresonator comb (Q, comb) | Mode-locked mid-infrared frequency combs in a silicon microresonator |
| ma2000 | splitter | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): deep-etched MMI 3-dB coupler, measured | Ultracompact multimode interference 3-dB coupler with strong lateral confinement by deep dry etching |
| masanovic2003 | splitter | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): InP two-stage 1x2 MMI splitter | Multimode interference-based two-stage 1 /spl times/ 2 light splitter for compact photonic integrated circuits |
| tian2025 | splitter | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_03): SOI star-coupler splitter | Silicon-based star coupler power splitter with enhanced non-uniformity |
| wu2023a | switch_fabric | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_04): TFLN programmable 4x4 mesh (EO; check EO atlas) | Electro-optically programmable photonic circuits enabled by wafer-scale integration on thin-film lithium niobate |
| xia2026 | switch_fabric | 9 | cached | reserve: best remaining | Assessment of low polarization sensitive InP photonic integrated multicast and select switch with commercial 400G-ZR transceivers |
| zali2026 | switch_fabric | 9 | cached | reserve: best remaining | Densely integrated low polarization dependent 8 × 8 optical switch for optical network applications |
| chen2026c | waveguide_platform | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): ultralow-loss SiN quantum platform (MMI, ring, crossing, heater) | An ultralow-loss integrated photonic platform for discrete-variable quantum information processing |
| dagostino2015 | waveguide_platform | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): Zn-diffused low-loss InP passive waveguides, ring, MMI | Low-loss passive waveguides in a generic InP foundry process via local diffusion of zinc |
| fahrenkopf2019 | waveguide_platform | 2 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): AIM Photonics MPW platform data (AIM fab) | The AIM Photonics MPW: A Highly Accessible Cutting Edge Technology for Rapid Prototyping of Photonic Integrated Circuits |
| li2026a | waveguide_platform | 9 | cached | reserve: best remaining | Mid-infrared-to-ultraviolet supercontinuum generation in low-loss tantalum pentoxide nanophotonic waveguides |
| lu2025a | waveguide_platform | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015, cov_tsmc2): TSMC SiPh-integrated PECVD SiN building blocks (waveguide, bend, taper, crossing, MMI, SiN-Si transition, edge coupler) | Low-loss High-uniformity Silicon Nitride Optical Building Blocks Integrated on Silicon Photonics Platform |
| roeloffzen2018 | waveguide_platform | 0 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): TriPleX waveguide overview (LioniX); own data, check rule 3 per value | Low-Loss Si3N4 TriPleX Optical Waveguides: Technology and Applications Overview |
| worhoff2015 | waveguide_platform | 2 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): TriPleX platform overview (LioniX); own platform data, check rule 3 per value | TriPleX: a versatile dielectric photonic platform |
| yeh2024 | waveguide_platform | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_01): TSMC SiPh platform (GC, waveguide, PD, MOD) (TSMC fab) | Silicon Photonics Platform for Next Generation Data Communication Technologies |
| amorim2017 | wdm | 9 | cached | rank | Monolithic Add–Drop Multiplexers in Fused Silica Fabricated by Femtosecond Laser Direct Writing |
| gatkine2022 | wdm | 8 | cached | curator: add: owner add 2026-11-07 (DevLog-015 S4, cov_04): astrophotonic AWG spectrograph (LIGENTEC SiN) | An on-chip astrophotonic spectrograph with a resolving power of 12,000 |

### Identity notes

- chen2025a (10.1364/optica.565112): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- kashiwazaki2021 (10.53829/ntr202111ra1): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- poulton2016 (10.1364/ol.42.000021): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- xin2024 (arxiv:2404.12381): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- kashiwazaki2021a (10.1063/5.0063118): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- xie2026a (10.1364/oe.581698): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- mehta2026 (10.1109/ectc51846.2026.00021): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- wang2025a (10.1364/oe.561993): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- babichev2025 (10.1109/jqe.2025.3553022): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- fan2025a (10.3788/col202523.081301): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- zhang2024c (10.1038/s41467-024-52269-7): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- ling2024 (10.1038/s41467-024-48544-2): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- helgason2023 (10.1038/s41566-023-01280-3): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- hu2022 (10.1038/s41566-022-01059-y): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- li2022 (10.1038/s41467-022-33101-6): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- xiang2021 (10.1126/science.abh2076): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- xiang2021a (10.1038/s41467-021-26804-9): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- liu2020a (10.1038/s41586-020-2465-8): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- raja2019 (10.1038/s41467-019-08498-2): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- dutt2018 (10.1126/sciadv.1701858): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- levy2026 (10.1109/jlt.2026.3739658): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- hatai2024 (10.1364/ofc.2024.m1d.1): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- mao2024 (10.1364/ofc.2024.m1d.3): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- zhou2022b (10.1364/cleo_si.2022.ss2d.3): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- shim2026 (10.1021/acsphotonics.6c00117): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- beals2026 (arxiv:2606.18067): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- sun2024 (10.1038/s41586-024-07057-0): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- kramnik2024 (arxiv:2411.05921): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- rizzo2023 (10.1038/s41566-023-01244-7): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- li2019 (10.1002/lpor.201800228): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- yu2016 (10.1364/optica.3.000854): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- hu2021b (10.1038/s41586-021-03999-x): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- tian2025 (10.1007/s11082-024-07958-4): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- masanovic2003 (10.1109/lpt.2003.809972): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- ma2000 (10.1109/68.841263): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- wu2023a (10.1364/opticaopen.22573447): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- chen2026c (arxiv:2606.26910): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- dagostino2015 (10.1364/oe.23.025143): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- lu2025a (10.1364/ofc.2025.th1g.2): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- yeh2024 (10.1109/iedm50854.2024.10873369): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- worhoff2015 (10.1515/aot-2015-0016): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- roeloffzen2018 (10.1109/jstqe.2018.2793945): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
- gatkine2022 (arxiv:2203.07867): no longer eligible in the current pool / scores (curation drop or exclusion); row kept verbatim
