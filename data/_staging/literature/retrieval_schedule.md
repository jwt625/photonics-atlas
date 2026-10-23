# Retrieval schedule (DevLog-006 S7)

Generated 2026-10-22 by `scripts/lit_build_queue.py` from `cache_list.csv`; queue: `data/_staging/literature/retrieval_queue.csv`. Each route is spread evenly over the days; inside a (day, route) the rows are ordered by class round-robin (curator picks, then score). arXiv copies are preprints: the journal DOI stays the identity; the arXiv copy is the retrieval route.

## Totals

| route | papers |
|---|---:|
| arxiv | 195 |
| oa_publisher | 23 |
| publisher_browser | 87 |
| optica_browser | 418 |
| ieee_browser | 200 |
| ieee_search | 23 |
| manual | 54 |
| total | 1000 |

arXiv copy source: given 181, doi 0, title 6, api 8.

arXiv route gained by matching (rows without arXiv id in cache_list): 24 of 829; paywalled 0 of 182, Optica 7 of 450, IEEE 1 of 199. API queries cached 813 of 813 needed.

IEEE twins (Crossref, prefix 10.1109 / 10.23919, title similarity >= 0.93, shared surname, year within 1) of paywalled non-IEEE rows: 2 found in 104 of 104 lookups (only the 26 conference rows qualify); paywalled Optica rows routed to ieee_browser via a twin: 2 of 67; other publishers: 0. The Optica / journal DOI stays the identity (uid unchanged).

## Per day and route

| day | date | arxiv | oa_publisher | publisher_browser | optica_browser | ieee_browser | ieee_search | manual | total | sessions (optica / ieee / publisher) |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 2026-10-22 | 20 | 2 | 8 | 43 | 20 | 2 | 5 | 100 | 1,2,3 / 1 / 1 |
| 2 | 2026-10-23 | 20 | 2 | 8 | 42 | 21 | 2 | 5 | 100 | 4,5,6 / 2 / 2 |
| 3 | 2026-10-24 | 20 | 2 | 10 | 40 | 21 | 2 | 5 | 100 | 7,8,9 / 3 / 3 |
| 4 | 2026-10-25 | 20 | 2 | 8 | 42 | 20 | 3 | 5 | 100 | 10,11,12 / 4 / 4 |
| 5 | 2026-10-26 | 19 | 3 | 9 | 42 | 19 | 3 | 5 | 100 | 13,14,15 / 5 / 5 |
| 6 | 2026-10-27 | 19 | 3 | 9 | 42 | 19 | 3 | 5 | 100 | 16,17,18 / 6 / 6 |
| 7 | 2026-10-28 | 19 | 3 | 9 | 41 | 20 | 2 | 6 | 100 | 19,20,21 / 7 / 7 |
| 8 | 2026-10-29 | 19 | 2 | 9 | 42 | 20 | 2 | 6 | 100 | 22,23,24 / 8 / 8 |
| 9 | 2026-10-30 | 20 | 2 | 9 | 41 | 20 | 2 | 6 | 100 | 25,26,27 / 9 / 9 |
| 10 | 2026-10-31 | 19 | 2 | 8 | 43 | 20 | 2 | 6 | 100 | 28,29,30 / 10 / 10 |

## Per class and day

| class | d1 | d2 | d3 | d4 | d5 | d6 | d7 | d8 | d9 | d10 | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| amplifier | 5 | 6 | 5 | 4 | 3 | 3 | 4 | 5 | 6 | 4 | 45 |
| chip_chip_coupler | 3 | 2 | 3 | 5 | 7 | 5 | 3 | 3 | 3 | 5 | 39 |
| crossing | 4 | 5 | 4 | 4 | 1 | 3 | 4 | 4 | 2 | 2 | 33 |
| fiber_chip_coupler | 5 | 5 | 6 | 6 | 7 | 6 | 6 | 6 | 7 | 6 | 60 |
| fiber_interface | 3 | 3 | 3 | 3 | 4 | 4 | 3 | 3 | 2 | 3 | 31 |
| free_space_emitter | 6 | 3 | 2 | 2 | 3 | 3 | 5 | 5 | 6 | 5 | 40 |
| frequency_converter | 3 | 4 | 4 | 4 | 3 | 2 | 2 | 2 | 3 | 3 | 30 |
| laser | 9 | 9 | 9 | 9 | 10 | 12 | 12 | 11 | 10 | 11 | 102 |
| micro_optics | 4 | 6 | 4 | 4 | 3 | 3 | 2 | 3 | 4 | 2 | 35 |
| mode_converter | 4 | 2 | 3 | 2 | 3 | 3 | 4 | 4 | 4 | 6 | 35 |
| nonreciprocal | 3 | 4 | 5 | 5 | 4 | 3 | 2 | 2 | 1 | 1 | 30 |
| phase_shifter | 6 | 5 | 6 | 6 | 6 | 7 | 7 | 5 | 6 | 6 | 60 |
| photodetector | 7 | 8 | 6 | 7 | 8 | 8 | 8 | 9 | 8 | 7 | 76 |
| polarization | 3 | 4 | 5 | 5 | 5 | 5 | 4 | 5 | 4 | 5 | 45 |
| reflector | 4 | 2 | 3 | 2 | 2 | 2 | 4 | 4 | 4 | 3 | 30 |
| resonator | 5 | 7 | 7 | 8 | 6 | 6 | 6 | 5 | 5 | 5 | 60 |
| splitter | 6 | 6 | 6 | 6 | 4 | 4 | 3 | 4 | 5 | 6 | 50 |
| switch_fabric | 6 | 6 | 5 | 5 | 6 | 4 | 5 | 5 | 5 | 5 | 52 |
| waveguide_platform | 6 | 6 | 7 | 5 | 8 | 7 | 7 | 7 | 8 | 6 | 67 |
| wdm | 8 | 7 | 7 | 8 | 7 | 10 | 9 | 8 | 7 | 9 | 80 |

## Daily runbook

Fetchers update their own status log, not the queue. Browser sessions: one login per session (IEEE <= 30 papers incl. ieee_search, Optica and publisher <= 20 papers, <= 45 Optica papers per day). ieee_search rows: Xplore title search for an IEEE copy of a paywalled Optica conference paper; without a hit the fetcher falls back to optica_browser at runtime. Manual papers: save the PDF as `references/_inbox/<paper_id>.pdf`.

### Day 1 (2026-10-22): 100 papers

```
uv run python scripts/lit_fetch_oa.py --day 1   # arxiv 20 + oa_publisher 2
uv run python scripts/lit_fetch_browser.py --site optica --day 1 --session 1   # optica_browser 15
uv run python scripts/lit_fetch_browser.py --site optica --day 1 --session 2   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site optica --day 1 --session 3   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site ieee --day 1 --session 1   # ieee_browser 20 + ieee_search 2
uv run python scripts/lit_fetch_browser.py --site publisher --day 1 --session 1   # publisher_browser 8
```

Manual (5):

| paper_id | class | score | link | title |
|---|---|---:|---|---|
| sun2026 | free_space_emitter | 9 | https://doi.org/10.1002/lpor.71737 | Scalable Silicon Nitride OPA‐Based Free‐Space Photonic Interface for Chip‐Scale Atomic Magnetometry |
| morenopozas2026 | micro_optics | 9 | https://doi.org/10.1063/5.0326774 | Cassegrain reflector for hundredfold on-chip spot-size expansion |
| liu2021 | phase_shifter | 9 | https://doi.org/10.1117/12.2587413 | Comparison of thermo-optic phase-shifters implemented on CUMEC silicon photonics platform |
| chung2019 | polarization | 9 | https://doi.org/10.1063/1.5055863 | InP-based polarization rotator-splitter for mid-infrared photonic integration circuits |
| ren2025 | chip_chip_coupler | 8 | https://doi.org/10.1002/lpor.202500826 | Integration of InGaAs/InP Single Photon Avalanche Diode and Thin Film Lithium Niobate Photonic Chip via Photonic Wire Bonding |

### Day 2 (2026-10-23): 100 papers

```
uv run python scripts/lit_fetch_oa.py --day 2   # arxiv 20 + oa_publisher 2
uv run python scripts/lit_fetch_browser.py --site optica --day 2 --session 4   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site optica --day 2 --session 5   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site optica --day 2 --session 6   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site ieee --day 2 --session 2   # ieee_browser 21 + ieee_search 2
uv run python scripts/lit_fetch_browser.py --site publisher --day 2 --session 2   # publisher_browser 8
```

Manual (5):

| paper_id | class | score | link | title |
|---|---|---:|---|---|
| chen2018 | crossing | 9 | https://doi.org/10.1021/acsphotonics.8b00788 | Ultralow Crosstalk and Loss CMOS Compatible Silicon Waveguide Star-Crossings with Arbitrary Included Angles |
| kang2008a | photodetector | 9 | https://doi.org/10.1038/nphoton.2008.247 | Monolithic germanium/silicon avalanche photodiodes with 340 GHz gain–bandwidth product |
| wang2026a | free_space_emitter | 9 | https://doi.org/10.1002/lpor.71490 | Millimeter‐Scale Grating Antenna Harnessing Bosund State in the Continuum for Sub‐mrad‐Resolution Lithium Niobate Optical Phased Array |
| chen2000 | micro_optics | 9 | https://doi.org/10.1117/1.602523 | Vertically tapered polymer waveguide mode size transformer for improved fiber coupling |
| zhang2016 | polarization | 9 | https://doi.org/10.1063/1.4965832 | Ultra-compact and highly efficient silicon polarization splitter and rotator |

### Day 3 (2026-10-24): 100 papers

```
uv run python scripts/lit_fetch_oa.py --day 3   # arxiv 20 + oa_publisher 2
uv run python scripts/lit_fetch_browser.py --site optica --day 3 --session 7   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site optica --day 3 --session 8   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site optica --day 3 --session 9   # optica_browser 12
uv run python scripts/lit_fetch_browser.py --site ieee --day 3 --session 3   # ieee_browser 21 + ieee_search 2
uv run python scripts/lit_fetch_browser.py --site publisher --day 3 --session 3   # publisher_browser 10
```

Manual (5):

| paper_id | class | score | link | title |
|---|---|---:|---|---|
| zhao2022 | crossing | 9 | https://doi.org/10.1002/lpor.202100623 | Silicon Multimode Waveguide Crossing Based on Anisotropic Subwavelength Gratings |
| wang2023a | laser | 9 | https://doi.org/10.1002/lpor.202200979 | High‐Power, Narrow‐Linewidth, and Low‐Noise Quantum Dot Distributed Feedback Lasers |
| a2017 | mode_converter | 8 | https://doi.org/10.1002/lpor.201700109 | 10‐Channel Mode (de)multiplexer with Dual Polarizations |
| colangelo2024 | photodetector | 8 | https://doi.org/10.1021/acsphotonics.3c01628 | Molybdenum Silicide Superconducting Nanowire Single-Photon Detectors on Lithium Niobate Waveguides |
| du2020 | reflector | 9 | https://aip.scitation.org/doi/pdf/10.1063/5.0022963 | Silicon nitride chirped spiral Bragg grating with large group delay |

### Day 4 (2026-10-25): 100 papers

```
uv run python scripts/lit_fetch_oa.py --day 4   # arxiv 20 + oa_publisher 2
uv run python scripts/lit_fetch_browser.py --site optica --day 4 --session 10   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site optica --day 4 --session 11   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site optica --day 4 --session 12   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site ieee --day 4 --session 4   # ieee_browser 20 + ieee_search 3
uv run python scripts/lit_fetch_browser.py --site publisher --day 4 --session 4   # publisher_browser 8
```

Manual (5):

| paper_id | class | score | link | title |
|---|---|---:|---|---|
| coratozanarella2022 | laser | 8 | https://doi.org/10.1038/s41566-022-01120-w | Widely tunable and narrow-linewidth chip-scale lasers from near-ultraviolet to near-infrared wavelengths |
| jung2018 | nonreciprocal | 8 | https://aip.scitation.org/doi/pdf/10.1063/1.5050332 | Fully integrated optical isolators for space division multiplexed (SDM) transmission |
| lee2012 | resonator | 6 | https://doi.org/10.1038/nphoton.2012.109 | Chemically etched ultrahigh-Q wedge-resonator on a silicon chip |
| wang2026i | photodetector | 10 | https://doi.org/10.1021/acsphotonics.5c02939 | Silicon Nitride Waveguide-Integrated Ge Photodetector with >110 GHz Bandwidth under 1 mA Operation in the O-Band |
| chiles2017 | crossing | 8 | https://doi.org/10.1063/1.5000384 | Multi-planar amorphous silicon photonics with compact interplanar couplers, cross talk mitigation, and low crossing loss |

### Day 5 (2026-10-26): 100 papers

```
uv run python scripts/lit_fetch_oa.py --day 5   # arxiv 19 + oa_publisher 3
uv run python scripts/lit_fetch_browser.py --site optica --day 5 --session 13   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site optica --day 5 --session 14   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site optica --day 5 --session 15   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site ieee --day 5 --session 5   # ieee_browser 19 + ieee_search 3
uv run python scripts/lit_fetch_browser.py --site publisher --day 5 --session 5   # publisher_browser 9
```

Manual (5):

| paper_id | class | score | link | title |
|---|---|---:|---|---|
| shoji2002 | fiber_chip_coupler | 9 | https://doi.org/10.1049/el:20021185 | Low loss mode size converter from 0.3 µm square Si wire waveguides to singlemode fibres |
| yamaoka2020 | laser | 8 | https://doi.org/10.1038/s41566-020-00700-y | Directly modulated membrane lasers with 108 GHz bandwidth on a high-thermal-conductivity silicon carbide substrate |
| kittlaus2020 | nonreciprocal | 8 | https://doi.org/10.1038/s41566-020-0640-y | Low-loss nonlinear optical isolators in silicon |
| zhang2023e | switch_fabric | 8 | https://doi.org/10.1002/lpor.202300232 | Ultrabroadband 2D‐Dispersive Wavelength Selective Switch with 1.57 GHz Hyperfine Spectral Resolution and >1600 Channels |
| yan2025a | photodetector | 10 | https://doi.org/10.1021/acsphotonics.5c01684 | Large Bandwidth and High Power Germanium/Silicon Photodetector: A Novel Solution for 100 Gb s –1 Microwave Photonic Links |

### Day 6 (2026-10-27): 100 papers

```
uv run python scripts/lit_fetch_oa.py --day 6   # arxiv 19 + oa_publisher 3
uv run python scripts/lit_fetch_browser.py --site optica --day 6 --session 16   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site optica --day 6 --session 17   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site optica --day 6 --session 18   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site ieee --day 6 --session 6   # ieee_browser 19 + ieee_search 3
uv run python scripts/lit_fetch_browser.py --site publisher --day 6 --session 6   # publisher_browser 9
```

Manual (5):

| paper_id | class | score | link | title |
|---|---|---:|---|---|
| shoji2008 | nonreciprocal | 8 | https://doi.org/10.1063/1.2884855 | Magneto-optical isolator with silicon waveguides fabricated by direct bonding |
| lukin2019 | waveguide_platform | 8 | https://doi.org/10.1038/s41566-019-0556-6 | 4H-silicon-carbide-on-insulator for integrated quantum and nonlinear photonics |
| fowler2019 | fiber_chip_coupler | 7 | https://doi.org/10.1117/12.2511845 | Fiber grating coupler development for Si-photonics process design kits at CEA-LETI |
| chen2016 | laser | 6 | https://doi.org/10.1038/nphoton.2016.21 | Electrically pumped continuous-wave III–V quantum dot lasers on silicon |
| cavalier2011 | photodetector | 9 | https://doi.org/10.1063/1.3656744 | Light interference detection on-chip by integrated SNSPD counters |

### Day 7 (2026-10-28): 100 papers

```
uv run python scripts/lit_fetch_oa.py --day 7   # arxiv 19 + oa_publisher 3
uv run python scripts/lit_fetch_browser.py --site optica --day 7 --session 19   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site optica --day 7 --session 20   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site optica --day 7 --session 21   # optica_browser 13
uv run python scripts/lit_fetch_browser.py --site ieee --day 7 --session 7   # ieee_browser 20 + ieee_search 2
uv run python scripts/lit_fetch_browser.py --site publisher --day 7 --session 7   # publisher_browser 9
```

Manual (6):

| paper_id | class | score | link | title |
|---|---|---:|---|---|
| liu2019 | amplifier | 9 | https://doi.org/10.1021/acsphotonics.9b00903 | High-Performance O-Band Quantum-Dot Semiconductor Optical Amplifiers Directly Grown on a CMOS Compatible Silicon Substrate |
| hausmann2014 | waveguide_platform | 8 | https://doi.org/10.1038/nphoton.2014.72 | Diamond nonlinear photonics |
| lira2012 | nonreciprocal | 6 | https://doi.org/10.1103/physrevlett.109.033901 | Electrically Driven Nonreciprocity Induced by Interband Photonic Transition on a Silicon Chip |
| lacava2016 | fiber_chip_coupler | 10 | https://doi.org/10.1117/12.2212458 | Design and characterization of low-loss 2D grating couplers for silicon photonics integrated circuits |
| simpanen2017 | laser | 10 | https://doi.org/10.1049/el.2017.1165 | 1060 nm single‐mode vertical‐cavity surface‐emitting laser operating at 50 Gbit/s data rate |
| an2025 | photodetector | 9 | https://doi.org/10.1021/acsphotonics.5c00571 | Hyper Self-Doping of GeIn for Cost-Effective Ge PIN Photodiodes with Record-Low Dark Current |

### Day 8 (2026-10-29): 100 papers

```
uv run python scripts/lit_fetch_oa.py --day 8   # arxiv 19 + oa_publisher 2
uv run python scripts/lit_fetch_browser.py --site optica --day 8 --session 22   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site optica --day 8 --session 23   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site optica --day 8 --session 24   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site ieee --day 8 --session 8   # ieee_browser 20 + ieee_search 2
uv run python scripts/lit_fetch_browser.py --site publisher --day 8 --session 8   # publisher_browser 9
```

Manual (6):

| paper_id | class | score | link | title |
|---|---|---:|---|---|
| xu2019 | polarization | 9 | https://doi.org/10.1002/lpor.201800349 | Ultra‐Broadband and Ultra‐Compact On‐Chip Silicon Polarization Beam Splitter by Using Hetero‐Anisotropic Metamaterials |
| foster2006 | amplifier | 8 | https://doi.org/10.1038/nature04932 | Broad-band optical parametric gain on a silicon photonic chip |
| bi2011 | nonreciprocal | 5 | https://doi.org/10.1038/nphoton.2011.270 | On-chip optical isolation in monolithically integrated non-reciprocal optical resonators |
| kim2025 | waveguide_platform | 10 | https://doi.org/10.1117/12.3043377 | Ultra-low loss dispersion-engineered silicon nitride waveguides on 300 mm wafers |
| hermans2021 | laser | 9 | https://aip.scitation.org/doi/pdf/10.1063/5.0058022 | High-pulse-energy III-V-on-silicon-nitride mode-locked laser |
| gehring2019 | fiber_chip_coupler | 8 | https://doi.org/10.1063/1.5064401 | Low-loss fiber-to-chip couplers with ultrawide optical bandwidth |

### Day 9 (2026-10-30): 100 papers

```
uv run python scripts/lit_fetch_oa.py --day 9   # arxiv 20 + oa_publisher 2
uv run python scripts/lit_fetch_browser.py --site optica --day 9 --session 25   # optica_browser 15
uv run python scripts/lit_fetch_browser.py --site optica --day 9 --session 26   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site optica --day 9 --session 27   # optica_browser 12
uv run python scripts/lit_fetch_browser.py --site ieee --day 9 --session 9   # ieee_browser 20 + ieee_search 2
uv run python scripts/lit_fetch_browser.py --site publisher --day 9 --session 9   # publisher_browser 9
```

Manual (6):

| paper_id | class | score | link | title |
|---|---|---:|---|---|
| sun2013 | free_space_emitter | 8 | https://doi.org/10.1038/nature11727 | Large-scale nanophotonic phased array |
| gallacher2020 | polarization | 8 | https://aip.scitation.org/doi/pdf/10.1063/1.5134973 | Ultra-broadband mid-infrared Ge-on-Si waveguide polarization rotator |
| fang2022 | phase_shifter | 6 | https://doi.org/10.1038/s41565-022-01153-w | Ultra-low-energy programmable non-volatile silicon photonics based on phase-change materials with graphene heaters |
| cao2024 | amplifier | 9 | https://pubs.aip.org/aip/app/article-pdf/doi/10.1063/5.0194677/19895096/046110_1_5.0194677.pdf | A novel bidirectionally operated chirped quantum-dot based semiconductor optical amplifier using a dual ground state spectrum |
| wei2026 | laser | 9 | https://doi.org/10.1063/5.0341253 | Integrated frequency-modulated continuous-wave laser self-injection locked to a strongly reflective multimode microring resonator |
| koester2024 | waveguide_platform | 9 | https://doi.org/10.1063/5.0223134 | GaAs-based photonic integrated circuit platform enabling monolithic ring-resonator-coupled lasers |

### Day 10 (2026-10-31): 100 papers

```
uv run python scripts/lit_fetch_oa.py --day 10   # arxiv 19 + oa_publisher 2
uv run python scripts/lit_fetch_browser.py --site optica --day 10 --session 28   # optica_browser 15
uv run python scripts/lit_fetch_browser.py --site optica --day 10 --session 29   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site optica --day 10 --session 30   # optica_browser 14
uv run python scripts/lit_fetch_browser.py --site ieee --day 10 --session 10   # ieee_browser 20 + ieee_search 2
uv run python scripts/lit_fetch_browser.py --site publisher --day 10 --session 10   # publisher_browser 8
```

Manual (6):

| paper_id | class | score | link | title |
|---|---|---:|---|---|
| shen2015 | polarization | 8 | https://doi.org/10.1038/nphoton.2015.80 | An integrated-nanophotonics polarization beamsplitter with 2.4 × 2.4 μm2 footprint |
| qiu2025a | phase_shifter | 10 | https://doi.org/10.1021/acsphotonics.4c02518 | Ultralow Loss Design Methodology for Energy-Efficient Thermo-Optic Phase Shifters |
| liu2022c | wdm | 10 | https://doi.org/10.1063/5.0085332 | High-performance silicon photonic filters based on all-passive tenth-order adiabatic elliptical-microrings |
| jiao2025 | free_space_emitter | 9 | https://doi.org/10.1063/5.0264068 | Two-dimensional multi-beam steering for parallel free-space optical communication based on a silicon nitride optical phase array |
| moser2011 | laser | 9 | https://doi.org/10.14279/depositonce-14934 | 81 fJ/bit energy-to-data ratio of 850 nm vertical-cavity surface-emitting lasers for optical interconnects |
| boucaud2024 | chip_chip_coupler | 8 | https://pubs.aip.org/aip/apl/article-pdf/doi/10.1063/5.0221309/20082420/054101_1_5.0221309.pdf | Glass interposer for heterogeneous integration of flip-chipped photonic and electronic integrated circuits |
