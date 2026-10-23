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
