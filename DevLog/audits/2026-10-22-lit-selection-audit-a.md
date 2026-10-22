---
title: DevLog-006 S6 audit A (correctness) of the component-literature cache list
date: 2026-10-22
mode: fresh-context subagent (did not build the list); report transcribed by the coordinator (the subagent could not write files outside its own outputs)
target: data/_staging/literature/cache_list.csv (1000 rows, selection of 2026-10-22 01:25 UTC)
outputs: data/_staging/literature/audit_a_corrections.yaml (8 drops, 5 reclass)
---

# Lit selection audit A: correctness

## Method

- Inputs: DevLog-006 (D120-D139), scoring_prompt.md, selection.yaml, component_parameters.yaml, curation YAMLs
  (format only). Full records (abstracts) joined by uid from prefiltered.jsonl and curator_adds.jsonl: 1000 / 1000.
- Known-work check against sources.csv (1831 rows: ofc2026, pk, lin, eo, blog, web) and EO papers.csv (233), by
  normalized DOI, arXiv id, exact normalized title (> 25 chars) and fuzzy title (difflib >= 0.85), incl. alt_dois /
  alt_uids / alt_titles.
- Stratified sample: 160 rows (8 per class; per class 2 curator + 2 rank picks where available, rest random; seed
  20261022): curator 67, rank 74, other 19. Every abstract read; scope, likely measured metrics, class, subtype,
  platform judged.
- Identifier check: 25 random rows (seed 20261023), one free OpenAlex singleton get each via `litfetch.get_json`.

## Headline

- Sample: ok 140 (87.5 %), imprecise 18 (11.2 %), wrong 2 (1.2 %); both wrong rows are curator adds. Imprecise by
  origin: curator 9 / 67, rank 7 / 74, subtype floor / reserve 2 / 19.
- Duplicates: 0 on uid / DOI / arXiv id / paper_id; one conference + journal version pair selected
  (10.1109/siphotonics60897.2024.10543882 precursor of 10.1109/jlt.2024.3407339).
- Known: 0 against sources.csv and EO papers.csv by any match. Two rows `known_in: eo_candidates`
  (s41566-022-01003-0, s41566-026-02008-9): eligible under D139.
- Identifiers: 25 / 25 HTTP 200, title similarity 1.0, years equal.
- Access consistency: 0 oa rows without oa_url, 0 paywalled rows with an arXiv id / preprint URL / is_oa.

## Whole-list findings

- 1 row without DOI or arXiv id: openalex:W2915271777 (2018 ETS dissertation); keep only if theses are acceptable.
- Version-family review (8 near-identical-title pairs, 37 same-author pairs with Jaccard >= 0.3 and years within 3):
  only El-Saeed SiPhotonics 2024 / JLT 2024 is a strict version pair (drop the conference paper). Mangal OFC 2018
  tu2a.1 / JSTQE 2019 related, not a version (candidate drop); Fargas Cabanillas OFC 2021 / IPR 2021 same device
  family, different data; Theurer PTL 2019 / JLT 2020, Ashida OE 2017 / JLT 2018 and four other pairs distinct.
- Paywalled share above the 20 % target (D124, curator picks may exceed it): laser 23 / 101, waveguide_platform
  15 / 65, crossing 9 / 33, fiber_interface 8 / 31.
- Retrieval risks for S7: 409 oa_url values are doi.org landing links; 53 are IEEE ielx7 PDF links (8 bronze), WAF
  risk for headless fetches; 36 rows bronze (free to read, no licence): treat as restricted_local_only; 5 rows
  OpenAlex "closed" but with a correct arXiv OA URL.
- Record types: article 890, conference-paper 59, preprint 49, journal-article 1, dissertation 1. Review words in
  titles: 1 false positive. Commentary: s41377-020-0292-1 (single author, on 10.1038/s41377-020-0272-5, already
  selected): drop. Possible overview: tcpmt.2025.3531206 (score 3): check at S7.
- Simulation-only: 16 rows without experimental cue read; 2 simulation-only, both curator adds (ol.30.000138,
  oe.19.010940): drop. The other 14 report measured numbers or are industry platform papers.
- Out-of-scope title words: THz 5 (all optical bandwidth / tuning: ok), microwave 2 (MWP Ge PDs: ok), fiber-only
  pump combiner 1 (in scope by rule), AR holography 1 (oe.582322: drop), bio / sensing 4 (jphot.2009.2031596
  biosensor: drop), OPA / lidar 31 (in class; arxiv:2610.21027 free-space GMR metasurface, D138: drop), plasmonic 10
  (ok), quantum 42 (ok), system / link 42 (component numbers or industry module: ok), modulator 17 (none
  EO-modulator-main), simulation / design in title 7 (all measured; nanoph-2023-0637 candidate reclass to
  phase_shifter.phase_change), bulk / free-space 3 (ok).
- Scope edges kept but flagged: acsphotonics.4c00744 (free-space metasurface beamsplitter), fiber-tip metalenses,
  oe.435951 (helical LPG OAM converter), oe.28.001518 (hollow-core fiber micro-optics), oe.417827 (MCF connector):
  fiber-only parts not intended for chips need one rule.
- Metadata: primary class missing from `classes` in 4 rows (jlt.2022.3172781, oe.26.010400, jlt.2020.3002716,
  ofc.2001.927572; the last two with empty `classes`); empty venue 4 (group4.2012.6324140, 12.2511845,
  ofc.2001.927572, 12.3043377); ofc.2001.927572 year 2002 vs DOI 2001. Platform "unstated" 127 rows (91 curator);
  band "unstated" 479. Empty abstracts 20 (all Nature-family curator adds, title-only judgement). Pre-2016 rows 149
  (144 seed lane, 5 curator; consistent with D121). Senior-author cap: 0 violations. 10 arXiv-only rows 2018-2024 may
  have journal versions (not checked).

## Error rates per class (sample, 8 each)

| class | ok | imprecise | wrong |
|---|---|---|---|
| amplifier | 8 | 0 | 0 |
| chip_chip_coupler | 6 | 2 | 0 |
| crossing | 7 | 1 | 0 |
| fiber_chip_coupler | 8 | 0 | 0 |
| fiber_interface | 7 | 1 | 0 |
| free_space_emitter | 7 | 1 | 0 |
| frequency_converter | 4 | 4 | 0 |
| laser | 8 | 0 | 0 |
| micro_optics | 5 | 3 | 0 |
| mode_converter | 8 | 0 | 0 |
| nonreciprocal | 8 | 0 | 0 |
| phase_shifter | 7 | 1 | 0 |
| photodetector | 8 | 0 | 0 |
| polarization | 7 | 0 | 1 |
| reflector | 8 | 0 | 0 |
| resonator | 7 | 1 | 0 |
| splitter | 7 | 1 | 0 |
| switch_fabric | 6 | 2 | 0 |
| waveguide_platform | 8 | 0 | 0 |
| wdm | 6 | 1 | 1 |
| total | 140 (87.5 %) | 18 (11.2 %) | 2 (1.2 %) |

Imprecise by type: platform 6, subtype 5, class 3, scope edge 3, metadata 1.

## Recommendations (auditor)

1. Apply `audit_a_corrections.yaml` and refill the freed slots.
2. Fill the 127 "unstated" platforms from title / abstract before reporting platform floors (sample fixes:
   lpt.2016.2616021 hybrid, col202523.111304 soi, s41566-020-00708-4 sin, s41467-022-31134-5 tfln, optica.3.001126
   aln, lpor.201600213 soi).
3. Fix metadata: the 4 rows with the primary class missing from `classes`, 4 empty venues, ofc.2001.927572 year.
4. Re-verify curator adds with no abstract or score < 6 (10 rows < 6).
5. Decide one rule for fiber-only parts not intended for chips.
6. Lower-confidence candidates: drop ofc.2018.tu2a.1; keep one of the Fargas Cabanillas pair; reclass
   nanoph-2023-0637 to phase_shifter.phase_change; reclass col202422.081401 to laser.dfb; s41377-024-01542-x to
   free_space_emitter.other; check tcpmt.2025.3531206.
7. S7: resolve doi.org links, plan for the IEEE WAF and bronze licensing, prefer journal versions of the 10 older
   arXiv-only rows, decide on the dissertation row.

## Sample table (160 rows)

| uid | class | subtype | reason_kind | verdict | reason |
|---|---|---|---|---|---|
| 10.1109/jstqe.2016.2593103 | amplifier | soa | curator | ok | heterogeneous III-V/Si SOA: 25 dB gain, 14 dBm Psat, transition loss |
| 10.1364/optica.442332 | amplifier | parametric | curator | ok | PPLN nanophotonic OPA, measured dB/cm gain near 2 um |
| arxiv:2401.07198 | amplifier | parametric | rank | ok | SiN + GO film OPA, 24 dB parametric gain measured |
| arxiv:2605.13828 | amplifier | rare_earth | rank | ok | Yb:Al2O3 amplifier, 0.5 W, NF 3.3 dB |
| arxiv:2608.18295 | amplifier | parametric | subtype | ok | TFLN CW-pumped OPA, 56 THz 3-dB gain bandwidth, gains |
| 10.1364/prj.545946 | amplifier | soa | rank | ok | transfer-printed QD SOA on SiPh, 7.5 dB on-chip gain |
| 10.1038/s41586-025-08666-z | amplifier | parametric | rank | ok | GaP-on-SiO2 OPA, 35 dB gain |
| 10.1038/s41586-025-08824-3 | amplifier | parametric | rank | ok | SiN FWM parametric amplification; measured gain/bandwidth expected |
| 10.3788/col202422.081401 | chip_chip_coupler | photonic_wire_bond | curator | imprecise | abstract gives only laser metrics (SMSR, bandwidth); PWB coupling loss not stated; laser.dfb fits the measured data better |
| 10.1364/oe.600656 | chip_chip_coupler | butt | curator | ok | flip-chip QCL end-fire to Ge-on-Si, 3.03 dB coupling loss |
| 10.1364/oe.474256 | chip_chip_coupler | butt | rank | ok | flip-chip LD butt-coupled to SSC, >10 dBm coupled, 2.3 um 1-dB tolerance (transmitter paper) |
| 10.1364/oe.504032 | chip_chip_coupler | evanescent | rank | ok | wafer-scale interposer, 0.54 dB inter-chip evanescent coupling |
| 10.1109/lpt.2019.2892851 | chip_chip_coupler | butt | rank | ok | InP-to-SiN flip-chip interface, >40 mW coupled; distinct from JLT 2020 sibling |
| 10.1109/jlt.2022.3172781 | chip_chip_coupler | other | curator | ok | angled flip-chip VCSEL over SiN grating, measured IL; primary class missing from classes column |
| 10.1109/lpt.2016.2616021 | chip_chip_coupler | evanescent | curator | imprecise | platform unstated but abstract is Si3N4 + polymer (hybrid); class ok |
| 10.1364/optica.559260 | chip_chip_coupler | evanescent | rank | ok | SiN-to-polymer adiabatic coupling ~1 dB TE/TM |
| 10.1364/oe.21.012002 | crossing | multilevel | curator | ok | SiN-over-SOI multilevel crossing, crosstalk measured |
| 10.1364/acpc.2021.t4a.130 | crossing | other | curator | ok | 6 mdB single-layer Si crossing |
| 10.1364/oe.533238 | crossing | swg | rank | ok | SWG holey-metamaterial multimode crossing, IL/crosstalk |
| 10.1364/ol.32.002801 | crossing | other | rank | ok | double-etch SOI crossing, -1.7 dB, -40 dB crosstalk |
| 10.3788/col202523.111303 | crossing | other | rank | ok | LNOI multimode crossing, IL per mode |
| 10.1364/ol.402446 | crossing | other | reserve | ok | GF 45CLO crossing, 0.2 dB, 8-chip statistics |
| 10.1364/oe.381304 | crossing | mmi | subtype | ok | MMI crossing 43 mdB, backscatter |
| 10.3788/col202523.111304 | crossing | other | curator | imprecise | platform unstated but abstract says 220 nm SOI MPW |
| 10.1364/ol.28.001302 | fiber_chip_coupler | edge | curator | ok | landmark Si nanotaper edge coupler |
| 10.1002/lpor.202000542 | fiber_chip_coupler | grating | curator | ok | zero-order radiation surface coupler, >80 % CE, 90 nm 1-dB BW |
| 10.1117/12.2212458 | fiber_chip_coupler | grating | rank | ok | CEA-Leti 2D grating coupler, loss and 3-dB BW |
| 10.1364/osac.1.000013 | fiber_chip_coupler | grating | rank | ok | foundry SiNx bilayer GC, -2.56 dB |
| 10.1109/jlt.2025.3567712 | fiber_chip_coupler | edge | rank | ok | AlOx UV edge coupler 0.31 dB at 375 nm (band uv, not multi) |
| 10.1364/oe.23.022628 | fiber_chip_coupler | grating | curator | ok | SWG GC with metal reflector, -0.69 dB |
| 10.1364/oe.26.010400 | fiber_chip_coupler | other | subtype | ok | vertically curved Si surface coupler (fiber_chip_coupler.other per D138); primary class missing from classes column |
| 10.1364/oe.18.018278 | fiber_chip_coupler | grating | rank | ok | poly-Si overlay GC, -1.6 dB, 200 mm pilot line |
| 10.1109/ipc48725.2021.9592855 | fiber_interface | v_groove | curator | ok | imec U-groove 30-fiber passive assembly, <1 dB excess |
| 10.1364/ofc.2020.th3i.4 | fiber_interface | v_groove | curator | ok | GF monolithic fiber attach, yield/reliability (numbers not in abstract) |
| 10.1364/oe.457374 | fiber_interface | fan_out | rank | ok | FM-MCF fan-in/fan-out, per-mode IL (fiber-only, in scope by rule) |
| 10.1364/oe.497184 | fiber_interface | connector | rank | ok | OPCB polymer waveguides + MT connectors, 0.77 dB per interface |
| 10.1109/jphot.2020.3039900 | fiber_interface | v_groove | subtype | ok | fs-written glass interposer with V-grooves, coupling and propagation loss |
| 10.1109/jlt.2023.3239138 | fiber_interface | connector | rank | ok | expanded-beam PIC connector, ~2 dB, 80 mating cycles |
| 10.1364/oe.480418 | fiber_interface | connector | subtype | ok | detachable expanded-beam CPO interface, <1 dB |
| 10.1364/oe.417827 | fiber_interface | connector | subtype | imprecise | MCF-to-MCF LC connector: fiber-only part not for chips; scope edge |
| 10.1038/s41586-020-2811-x | free_space_emitter | grating_emitter | curator | ok | ion-trap chip with integrated UV-NIR grating emitters (AMO); numbers likely in text |
| 10.1021/acsphotonics.2c00422 | free_space_emitter | grating_emitter | curator | ok | inverse-designed surface-normal grating, measured 90 um Gaussian at 780 nm |
| 10.1364/optica.389006 | free_space_emitter | grating_emitter | rank | ok | serpentine OPA, wavelength-steered grating array |
| 10.1364/oe.23.006509 | free_space_emitter | other | rank | ok | 8x8 CMOS OPA transceiver |
| 10.1002/lpor.71737 | free_space_emitter | other | rank | ok | SiN OPA beam for magnetometry, 26.5 % radiation efficiency, 168-device statistics |
| 10.1364/ol.467779 | free_space_emitter | other | rank | ok | 32-ch OPA with on-chip phase calibration, SLSR, divergence |
| 10.1364/ol.34.001477 | free_space_emitter | grating_emitter | rank | ok | first SOI 1D OPA of grating couplers |
| 10.1038/s41377-024-01542-x | free_space_emitter | grating_emitter | curator | imprecise | ion-addressing chip with closely spaced output channels at the chip output (not stated as grating emitters); subtype likely free_space_emitter.other |
| 10.1038/s41566-020-00708-4 | frequency_converter | shg | curator | imprecise | platform unstated but abstract is silicon nitride microresonator |
| arxiv:2512.07968 | frequency_converter | shg | curator | ok | PP thin-film LiTaO3 watt-level SHG |
| 10.1109/jlt.2020.3046371 | frequency_converter | shg | rank | ok | polymer PIC with inserted bulk PPLN, fiber-to-fiber SHG efficiency |
| arxiv:2505.10338 | frequency_converter | sfg_dfg | rank | imprecise | Bragg-scattering FWM (chi3) conversion: frequency_converter.other, not sfg_dfg |
| 10.1063/5.0117691 | frequency_converter | other | subtype | ok | SiN microring OPO 590-1150 nm, 15 % efficiency |
| 10.1038/s41467-022-31134-5 | frequency_converter | shg | curator | imprecise | platform unstated but abstract is thin-film lithium niobate |
| 10.1364/optica.3.001126 | frequency_converter | shg | curator | imprecise | platform unstated but abstract is AlN microring |
| 10.1109/jlt.2025.3563899 | frequency_converter | sfg_dfg | subtype | ok | PPLN wavelength converter modules for U-band, gain flatness, NF |
| 10.1002/lpor.202200979 | laser | dfb | curator | ok | 1.3 um QD DFB, 100 mW, 1.62 kHz, RIN |
| 10.1364/oe.523353 | laser | dfb | curator | ok | 16-ch RW-DFB array, >85 mW, RIN, linewidth |
| 10.1109/jlt.2023.3265973 | laser | heterogeneous | rank | ok | transfer-printed membrane DR laser on Si, Ith, SMSR, 25 GHz |
| 10.1364/oe.24.013555 | laser | dfb | rank | ok | DML array TOSA, bandwidth and crosstalk (module level) |
| 10.1364/ol.573857 | laser | tunable | reserve | ok | InP MCI tunable laser, 120 mW, 40 kHz, 56 nm |
| 10.1364/oe.26.032500 | laser | other | rank | ok | GeSn microdisk laser to 230 K (optically pumped) |
| 10.1109/jlt.2019.2940589 | laser | tunable | reserve | ok | SiPh tunable laser with SOA, 21.5 dBm, 60 kHz |
| 10.1109/jlt.2022.3196914 | laser | comb | rank | ok | QD comb laser FSR/RIN plus MOSCAP interleaver crosstalk; transmitter paper |
| 10.1038/ncomms11763 | micro_optics | facet_lens | curator | ok | 3D-printed free-form optics on SMF facets (benchmark; shape accuracy, beam patterns) |
| 10.1002/lpor.202200025 | micro_optics | other | curator | ok | 3D-printed free-form reflector, 0.5 dB, 300 nm 1-dB BW |
| arxiv:2604.18426 | micro_optics | other | rank | imprecise | FIB-machined fiber-facet optics for photon collection; shape metrology only, no fiber-chip coupling metric; scope edge |
| 10.1364/oe.533232 | micro_optics | other | rank | imprecise | 45-degree micro-mirror vertical coupling: micro_optics.vertical_taper, not other |
| 10.1109/jlt.2020.2966446 | micro_optics | other | subtype | ok | ball lens in package via, backside GC coupling tolerance |
| 10.1002/nap2.70217 | micro_optics | facet_lens | subtype | imprecise | GO microlens array on fiber facet for imaging/sensing; NA and focal length only; scope edge |
| 10.1002/lpor.201900172 | micro_optics | integrated_lens | subtype | ok | SWG GRIN-lens spot-size converter, <1 dB over 130 nm |
| 10.1364/ol.486595 | micro_optics | integrated_lens | rank | ok | micro-dispensed lenses on grating couplers |
| 10.1002/lpor.201700109 | mode_converter | mdm_mux | curator | ok | 10-channel dual-polarization mode MUX |
| 10.1038/ncomms4069 | mode_converter | mdm_mux | curator | ok | landmark ring-based WDM-compatible MDM (no abstract in record; title only) |
| 10.1364/prj.562457 | mode_converter | mdm_mux | rank | ok | inverse-designed 3-mode MUX, measured |
| 10.1364/oe.579163 | mode_converter | mdm_mux | rank | ok | dual-polarization mode splitter, IL/CT per mode |
| 10.1109/lpt.2019.2917388 | mode_converter | other | subtype | ok | polymer LPG mode filter, 10 dB rejection over 190 nm |
| 10.1021/acsphotonics.5c02651 | mode_converter | other | subtype | ok | graphene-SiN mode filter, measured |
| 10.1364/oe.22.022172 | mode_converter | mdm_mux | curator | ok | SiN 3-mode MDM with ADCs, crosstalk |
| 10.1364/ol.42.001221 | mode_converter | converter | curator | ok | ADC mode converter/MUX, 90 % measured |
| 10.1038/s41566-024-01601-0 | nonreciprocal | isolator | curator | ok | passive Faraday isolator for hybrid integration (no abstract in record) |
| 10.1038/s41566-020-0640-y | nonreciprocal | isolator | curator | ok | nonlinear Si isolators (no abstract in record) |
| 10.1364/optica.408458 | nonreciprocal | isolator | rank | ok | MO isolators/circulators on SiN, 1 dB IL, 28 dB isolation |
| 10.1038/s41566-018-0254-9 | nonreciprocal | isolator | rank | ok | interband Brillouin nonreciprocity 38 dB, 125 GHz |
| 10.1109/lpt.2012.2212426 | nonreciprocal | isolator | rank | ok | Ce:YIG/SOI MZI isolator, 11 dB |
| 10.1038/s41566-020-00711-9 | nonreciprocal | isolator | curator | ok | SAW acousto-optic nonreciprocity in SOI (curator ruling) |
| 10.1364/optica.483017 | nonreciprocal | isolator | curator | ok | polarization-independent MO isolator, IL and isolation |
| 10.1038/s41467-026-75451-5 | nonreciprocal | isolator | rank | ok | TFLN EO isolator, strong-coupling regime |
| 10.1364/oe.448614 | phase_shifter | thermo_optic | curator | ok | visible SiN TOPS, P_pi 0.78-1.2 mW |
| 10.1038/s41566-021-00903-x | phase_shifter | mems | curator | ok | AlN piezo-optomechanical phase shifters in 200 mm SiN MZM |
| 10.1021/acsphotonics.3c00053 | phase_shifter | thermo_optic | rank | ok | MoS2 transparent heater, P_pi 7.5 mW |
| 10.1364/ol.35.001013 | phase_shifter | thermo_optic | rank | ok | NiSi waveguide heater, P_pi 20 mW |
| 10.1364/ol.469358 | phase_shifter | thermo_optic | curator | ok | LNOI thermo-optic phase shifter, bandwidth, VL |
| 10.1364/optica.6.000001 | phase_shifter | phase_change | rank | imprecise | GST multilevel amplitude memory cell; metrics are transmission levels and pulse energies, not phase shift |
| 10.1364/prj.441215 | phase_shifter | mems | rank | ok | wafer-level hermetic sealing of SiPh MEMS (iSiPP50G) |
| 10.1364/oe.413202 | phase_shifter | mems | curator | ok | NOEMS phase shifter, Vpi 2 V, IL <0.5 dB |
| 10.1038/ncomms9233 | photodetector | snspd | curator | ok | NbTiN waveguide SNSPD in nanobeam cavity, near-unity OCDE |
| 10.1021/acsphotonics.3c01628 | photodetector | snspd | curator | ok | MoSi SNSPD on TFLN, 50 % OCDE |
| 10.1364/oe.580467 | photodetector | apd | rank | ok | visible waveguide PDs, EQE, 18 GHz, APD GBP 374 GHz |
| 10.1364/oe.23.027213 | photodetector | ge_waveguide | rank | ok | IHP Ge PIN, >70 GHz, 1 A/W |
| 10.1021/acsphotonics.5c02939 | photodetector | ge_waveguide | rank | ok | SiN-fed Ge PD >110 GHz at 1 mA |
| 10.1021/acsphotonics.6c00574 | photodetector | graphene | subtype | ok | graphene-plasmonic PD, 155 GHz, 0.2 A/W |
| arxiv:2606.22863 | photodetector | spad | curator | ok | waveguide SPAD on SiN, PDE 1.95 % |
| 10.1109/iedm50854.2024.10873440 | photodetector | iii_v_on_platform | subtype | ok | III-V PD on SOI, 5-300 K responsivity |
| 10.1364/ol.481314 | polarization | pbs | curator | ok | 4H-SiC PBS, PER and IL |
| 10.1364/oe.16.004872 | polarization | psr | curator | ok | NTT Si polarization-diversity circuit, splitter + rotator |
| 10.1364/oe.20.025345 | polarization | pbs | rank | ok | hybrid-plasmonic PBS, ER and IL measured |
| 10.1364/oe.27.000999 | polarization | pbs | rank | ok | slot-DC PBS, PER 30/40 dB over 175 nm |
| 10.1364/oe.19.010940 | polarization | psr | curator | wrong | simulation-only concept paper (abstract: 'a design example is given'); curator reason 'with measurement' not supported |
| 10.1364/ol.39.000965 | polarization | pbs | rank | ok | four-port mode-evolution PBS, 300 mm CMOS |
| 10.1364/cleo_si.2024.sf1m.2 | polarization | psr | rank | ok | foundry visible SiN PSR, PER >18 dB, IL <1 dB |
| 10.1364/oe.23.029413 | polarization | pbs | curator | ok | cascaded broadband-coupler PBS, >20 dB over 125 nm |
| 10.1364/ol.34.001357 | reflector | bragg | curator | ok | cladding-modulated Bragg gratings, kappa and BW |
| 10.1002/lpor.201800226 | reflector | band_stop | curator | ok | coherency-broken Bragg rejection filters (band_stop) |
| 10.1364/oe.26.034366 | reflector | bragg | rank | ok | Ge-rich SiGe LWIR Bragg gratings and FP resonators |
| 10.1364/ol.36.004416 | reflector | bragg | rank | ok | fs-written chirped Bragg grating in silica, 10 nm BW |
| 10.1109/lpt.2019.2915262 | reflector | bragg | curator | ok | LioniX SiN Bragg, 0.2 nm stop band, thermal tuning |
| 10.1364/oe.542890 | reflector | bragg | rank | ok | Si-LNOI Bragg filters, ER 29 dB, Q 3.4e4 |
| 10.1002/nap2.70072 | reflector | bragg | rank | ok | chirped multimode SiN waveguide gratings, dispersion and ripple |
| 10.1364/ol.394455 | reflector | bragg | curator | ok | SWG modal Bragg filter, 60 dB rejection |
| 10.1364/oe.381224 | resonator | ring | curator | ok | SiN ring QL 1.4e6 at 780 nm |
| 10.1038/nphoton.2012.109 | resonator | disk | curator | ok | silica wedge resonator on Si (no abstract in record) |
| 10.1364/prj.387816 | resonator | ring | rank | ok | multimode Si racetrack, ultrahigh Q, MPW |
| arxiv:2601.15753 | resonator | ring | rank | ok | Ta2O5 microrings Qi >4e6 |
| 10.1364/oe.19.015864 | resonator | ring | rank | imprecise | MEMS cantilever tuning of a ring (122 pm at 9 V): primary phase_shifter.mems |
| 10.1063/5.0296704 | resonator | ring | curator | ok | InGaAs/InP mid-IR racetracks, loss and QL >6e5 |
| 10.1364/ol.40.003153 | resonator | bragg | curator | ok | tunable sidewall Bragg FP filter, Q 33,500 |
| 10.1364/prj.470644 | resonator | photonic_crystal | curator | ok | million-Q integrated FP cavity, reflector loss 0.05 dB |
| 10.1364/oe.25.010474 | splitter | y_branch | curator | ok | SiN tri-layer vertical Y-junction, 0.23 dB excess |
| 10.1364/oe.23.003795 | splitter | directional_coupler | curator | ok | broadband asymmetric DC, ratios and bandwidth |
| 10.29026/oea.2026.260026 | splitter | directional_coupler | rank | ok | AGF dense array and arbitrary-ratio DC, crosstalk |
| 10.1002/nap2.70320 | splitter | hybrid_90 | rank | ok | 4x4 MMI 90-degree hybrid, phase trimming |
| 10.1364/ol.603244 | splitter | directional_coupler | rank | ok | fs-written glass DC (platform other) |
| 10.1109/jphot.2018.2832188 | splitter | mmi | rank | ok | cascaded MMI 1x3 variable ratio, measured |
| 10.1002/lpor.201600213 | splitter | mmi | curator | imprecise | platform unstated but abstract is silicon photonics SWG MMI (soi) |
| 10.1364/ol.383757 | splitter | other | rank | ok | SiN slot splitter, <0.62 dB over 420 nm |
| 10.1364/oe.24.009295 | switch_fabric | mzi_mesh | curator | ok | 16x16 Si EO MZI switch fabric, IL and switching time |
| 10.1109/jphot.2022.3233663 | switch_fabric | wss | curator | ok | LCoS 3x3 folded WSS module, IL and resolution |
| 10.1109/jlt.2020.2989379 | switch_fabric | wss | rank | ok | Si WSS with contra-DCs, ER and BW |
| 10.1364/oe.27.005203 | switch_fabric | mzi_mesh | rank | imprecise | ring-resonator crossbar switch: switch_fabric.other, not mzi_mesh |
| 10.1364/ofc.2018.th4a.1 | switch_fabric | wss | curator | ok | twin 8x24 WSS, 3.3-6.8 dB IL |
| 10.1364/ol.44.004614 | switch_fabric | mzi_mesh | rank | ok | shift-and-dump MZ switch, ER >33 dB |
| 10.1002/lpor.202300232 | switch_fabric | wss | curator | ok | VIPA 2D WSS, 1.57 GHz resolution |
| 10.1109/ofc.2001.927572 | switch_fabric | mems | curator | imprecise | content ok (1296-port MEMS OXC, IL, crosstalk); metadata: empty classes and venue, year 2002 vs OFC 2001 DOI |
| 10.1364/ome.448376 | waveguide_platform | straight | curator | ok | chalcogenide LWIR pedestal waveguides 0.9 dB/cm |
| 10.1364/oe.515173 | waveguide_platform | bend | curator | ok | TFLN free-form bends <0.05 dB |
| 10.1109/jlt.2026.3651821 | waveguide_platform | straight | rank | ok | PECVD SiN loss study, measured vs model (title 'Modeling' but experimental) |
| 10.1038/s41566-019-0537-9 | waveguide_platform | straight | rank | ok | GaP-on-insulator, 1.2 dB/cm, Q >1e5 |
| 10.1364/ofc.2023.w2b.1 | waveguide_platform | straight | reserve | ok | TFLN on 8-inch Si, 0.47 dB/cm |
| 10.1364/optica.3.000999 | waveguide_platform | transition | rank | ok | Si-wire to plasmonic slot converter 1.7 dB (transition) |
| 10.1364/oe.21.014036 | waveguide_platform | straight | rank | ok | visible SiN platform, loss, bends, GC, MMI |
| 10.1063/5.0223134 | waveguide_platform | straight | rank | ok | GaAs active/passive PIC platform, loss, Qi, ring laser |
| 10.1021/acsphotonics.7b00987 | wdm | other | curator | ok | inverse-designed 3-channel demux, IL and crosstalk |
| arxiv:2509.07233 | wdm | other | curator | ok | co-optimized inverse-design WDM, <-40 dB crosstalk |
| 10.1109/jlt.2017.2715118 | wdm | other | rank | imprecise | MZI + Bragg-grating add-drop multiplexer: wdm.bragg_cdc, not other |
| 10.1063/5.0085332 | wdm | mrr | rank | ok | 10th-order elliptical microring filters, ER >60 dB |
| 10.1109/lpt.2014.2303793 | wdm | awg | rank | ok | Si AWG mask-grid study, crosstalk |
| 10.1109/jlt.2023.3325655 | wdm | eg | curator | ok | 1x40 cascaded echelle on 3-um SOI |
| 10.1364/ol.457566 | wdm | tff | curator | wrong | TFF focal-shift optics study; no MUX insertion loss, crosstalk or passband in abstract |
| 10.1117/1.apn.3.3.036012 | wdm | awg | rank | ok | 32x32 Si AWG 0.4 nm spacing, 0.65 dB excess |
