---
title: DevLog-006 S6 audit B - coverage and balance of the 1000-paper literature selection
date: 2026-10-22
auditor: fresh-context subagent (Claude), integrated-photonics reviewer role
inputs: data/_staging/literature/cache_list.csv (1000 rows), triage_report.md, cache/literature/curation_inputs/*.csv, cache/literature/prefiltered.jsonl, cache/literature/merged.jsonl (202,302 works), config/literature/scoring_prompt.md, selection.yaml, data/schema/component_parameters.yaml
outputs: data/_staging/literature/audit_b_corrections.yaml (18 picks, 31 drops, 13 adds; budget-neutral per class)
---

# Audit B: coverage and balance

## Method

- Benchmarks: for every class a list of landmark / record / foundry-statistics / industry papers a reviewer would expect,
  checked by title regex against `merged.jsonl` and classified as selected / scored but not selected / in pool but
  never scored / not in pool. Papers not in the pool were verified by OpenAlex singleton gets (5 gets, 4 resolved,
  1 HTTP 404 for a guessed DOI that was then not used; no searches, generic User-Agent via `litfetch.get_json`).
- Unselected candidates: per class, the `not_selected` rows with score >= 7 ranked by citations per year.
- Prefilter recall: per class, prefiltered works with a title class hit, cited_by >= 100, never scored.
- Balance: subtype, platform, band, year, industrial flag, senior (last) author, venue, access from `cache_list.csv`.
- Every proposed change is paired with a weaker drop in the same class (class budgets unchanged).

## Overall judgement

Coverage is adequate for a first ingestion batch in the passive classes (crossing, splitter, mode converter, micro
optics, fiber interface, reflector, chip-chip coupler) and for the classes the curators worked hardest (fiber-chip
coupler, free-space emitter, nonreciprocal). It is weakest where the pool is largest relative to the budget: laser,
resonator, photodetector, waveguide_platform, frequency_converter, phase_shifter. In those classes several canonical
benchmarks were never scored because the per-class scoring cap cut them (prefilter keep rate: laser 720 / 12,962 =
5.6 %, resonator 480 / 6,688 = 7.2 %, frequency_converter 250 / 2,426 = 10 %, photodetector 560 / 5,137 = 11 %,
waveguide_platform 480 / 3,390 = 14 %; versus chip_chip_coupler 144 / 164 and crossing 113 / 131), or because a title
regex missed them (`no_class_hit`), or because the senior-author cap (4) is binding on the dominant groups.
With the corrections the list is fit for S7, but the laser class needs a second pass (see recommendations R1-R3).

## Systemic findings

1. Scoring cap, not the scorer, is the main coverage loss. Unscored prefiltered works with a title hit and >= 100
   citations: laser 309, resonator 141, photodetector 115, waveguide_platform 86, frequency_converter 61,
   phase_shifter 43, polarization 13, free_space_emitter 5, all other classes 0-2. Many are noise (reviews, 2D-material
   photodetectors, VO2 films), but they include: Xiang 2021 Science (laser soliton microcombs heterogeneously integrated,
   10.1126/science.abh2076), Snigirev 2023 Nature (TFLN ultrafast tunable laser, rule score 10, cap_rank 1217), Raja
   2019 Nat Commun, Yoshida 2023 Nature PCSEL (cap_rank 6431), Ye 2023 PRJ foundry ultralow-loss SiN (rule score 9,
   cap_rank 665), Luke 2020 OE wafer-scale TFLN (rule score 10), Bose 2024 LSA anneal-free SiN, Ji 2023 LPR deposited
   SiN, Gondarenko 2009 high-Q SiN ring, Li 2016 Nat Photon single-photon frequency conversion, Taballione 2019 8x8 SiN
   mesh, Ribeiro 2016 4x4 universal circuit.
2. Title-regex misses (`prefilter_rejects.jsonl`, status `no_class_hit`): Hirose 2014 Nat Photon watt-class
   photonic-crystal lasers ("photonic-crystal lasers" does not hit `laser.pcsel`), Shen 2015 Nat Photon
   "polarization beamsplitter" (one word), Pospischil 2013 Nat Photon graphene photodetector, Barwicz 2006 Nat Photon
   polarization-transparent devices, Foster 2006 Nature parametric gain on Si. The G1 / G5 curators found the same
   pattern (D135). Regexes need one-word / hyphen variants ("beamsplitter", "photonic-crystal laser", "parametric gain").
3. Senior-author cap binds on landmarks. At cap 4 in laser: Bowers, Kippenberg, Blumenthal, Roelkens, Kuyken. Blocked
   landmarks: Xiang 2023 Nature 3D-integrated isolator-free laser (10.1038/s41586-023-06251-w, scored 8), Xiang 2021
   Science, Shen 2020 Nature turnkey microcombs (scored 8), Snigirev 2023, Raja 2019. Also at cap: Kawashima and Ikeda
   (switch_fabric), Lei Bi (nonreciprocal: Zhang 2019 Optica broadband monolithic isolators blocked), Majumdar
   (phase_shifter: Zheng 2020 Adv Mater PIN-heater PCM switch blocked), Van Campenhout (photodetector), Vahala
   (resonator), Dai (wdm), Tsang (fiber_chip_coupler), Koos (chip_chip_coupler), Roelkens (amplifier). Global
   concentration is acceptable: top seniors Bowers 18, Dai 14, Van Campenhout 12, Tsang 12, Roelkens 11, Kuyken 10.
   Name variants do not currently break the cap ("G. Q. Lo" + "Guo-Qiang Lo" = 4 in fiber_chip_coupler; "Tobias
   Kippenberg" + "Tobias Jan Kippenberg" = 4 in amplifier), but 19 rows carry a truncated last author ("Daoxin Dai A" 14,
   "Jelena Vuckovic A" 5), which the cap and any author statistics must normalize.
4. Scope inconsistency, WSS: scoring_prompt.md puts bulk free-space optics out of scope, but switch_fabric.wss holds
   6 LCoS / free-space WSS module papers (two scored 0 and kept by curator override). Only the two score-0 rows are
   dropped here; the rule for LCoS WSS modules should be written down (keep as module datasheet-style rows, or exclude).
5. Version handling: 180 of 819 OA rows are arXiv copies. Two arXiv picks have the journal version in the pool as a
   separate, unmerged record (arxiv:2501.04248 vs 10.1364/prj.547240; arxiv:2110.12850 vs 10.1364/prj.447478). The
   distiller must record which version the numbers come from; several rationales say "possible duplicate of" a
   conference version (13 rows) that the family merge did not catch.
6. Low-yield landmark rows kept on purpose: Mehta 2016 Nat Nano and Niffenegger 2020 Nature (score 2, ion-qubit system
   papers with emitter numbers inside), Liu 2016 Nat Photon QD lasers on Si (title only), Lee 2012 Nat Photon wedge
   resonator (title only), Bi 2011 Nat Photon isolator (title only), Skacel 2025 TCPMT PWB (score 3). Expect few rows.

## Balance (cache_list.csv before corrections)

| dimension | finding |
|---|---|
| platform | soi 326, hybrid 167, unstated 127, sin 113, other 61, inp 58, tfln 48, ge_sige 27, polymer 20, al2o3 9, silica_plc 9, gaas_algaas 9, chalcogenide 7, lt 6, sic 5, aln 4, ta2o5 4. SOI share 33 % is reasonable; AlN / SiC / Ta2O5 / diamond thin (resonator had no SiC ring) |
| band | unstated 479 (scorer could not tell from abstracts), C 194, multi 142, O 65, nir_other 55, visible 33, mid_ir 22, L 7. O-band (datacom / CPO) is thin: wdm 11, photodetector 11, laser 9 |
| year | pre-2016 only via seeds; laser 50 / 101 and free_space_emitter 19 / 40 from 2024-2026 (recency heavy); polarization 15 / 45 and fiber_chip_coupler 17 / 60 pre-2016 (landmark heavy). No class below 11 distinct years |
| industry flag | 411 / 1000 (rubric counts research institutes). Low: mode_converter 2 / 35, nonreciprocal 2 / 30, chip_chip_coupler 5 / 39, reflector 5 / 30, frequency_converter 6 / 30, crossing 7 / 33. High: fiber_chip_coupler 40 / 60, switch_fabric 37 / 52, waveguide_platform 40 / 65, laser 63 / 101 |
| venue | Optics Express 311 (31 %), JLT 84, OL 81, Optica 52, arXiv 47; conference papers 55 (OFC 15 incl. both name forms, ECOC 5): industry conference results are underweighted by the OA rule (45 of 55 conference picks are paywalled) |
| subtype | thin subtypes: laser.els_module 1 (score 2), laser.soa_dfb 2, wdm.tff 2, reflector.phc_mirror 2, fiber_chip_coupler.photonic_wire_bond 3 (one was a commentary), free_space_emitter.metasurface 5, laser.pcsel 5 (one misfiled). Heavy: free_space_emitter OPAs about 24 / 40, waveguide_platform.straight 42 / 65, wdm.awg 29 / 80 |

## Per-class findings

Notation: S = selected, U = scored but not selected (score), P = in pool never scored, N = not in pool (OpenAlex
verified), K = known (already in another corpus).

### fiber_chip_coupler (60; grating 33, edge 19, PWB 3; SOI 31; paywalled 9)
- Benchmarks S: Almeida 2003 nanotaper, Taillaert 2006 JJAP, Ding 2014 -0.58 dB, Benedikovic 2015 SWG sub-dB, Cheben 2015 SWG edge coupler,
  Sfar Zaoui 2014, Vermeulen 2010 (CMOS pilot line), GF 2020 production metamaterial couplers, Tsang-group 2022 photolithography sub-dB.
  U: Marchetti 2017 Sci Rep -0.9 dB (9, OA), Hu 2021 OE TFLN edge 0.54 dB / facet (8, OA), Notaros 2016 OFC
  ultra-efficient CMOS GC (9, paywalled), Lindenmann 2014 JLT PWB to MCF (8, OA), dual-level reflector-less GC -0.8 dB (PRJ 2023)
  (9, OA). P: Cardenas 2014 PTL etched-facet tapers.
- Weak: 10.1038/s41377-020-0292-1 is a News-and-Views commentary (score 0) on Blaicher 2020, which is selected in
  chip_chip_coupler. Name variants of Lo reach the cap of 4.
- Corrections: picks Marchetti, Hu, Lindenmann; drops commentary, Lo 2014 laser-welded packaging, Kim 2013 SiON taper.

### micro_optics (35; balanced 5 subtypes; paywalled 6)
- S: Dietrich 2018 Nat Photon in-situ printed elements, Gissibl 2016 Nat Commun, Missinne backside lenses, Ortega-Monux
  reflectors / GRIN. U candidates are fiber-tip metalenses (mostly paywalled). No change.

### fiber_interface (31; paywalled 8 = 26 %, above 20 %)
- S: Barwicz 2016 JSTQE IBM V-groove, IBM 2018 self-aligned metamaterial interface, Brusberg 2019 Corning ferrule, Giewont 2020 GF
  attach, imec U-groove, ITRI detachable CPO interface. U: Barwicz 2015 ECTC automated 12-fiber assembly (9, paywalled),
  12-channel glass-waveguide fiber-array coupler (JLT 2010) (9, paywalled); both blocked by the paywall share. No change.

### free_space_emitter (40; other 21, grating_emitter 14, metasurface 5)
- S: Sun 2013 Nature 4096-element OPA, Watts 8192-element OPA, Mehta 2016, Niffenegger 2020, Mehta 2017 focusing
  gratings, Aksyuk meta-gratings. U: Poulton 2019 JSTQE long-range OPA LiDAR (8, paywalled), 180-degree-FOV Si OPA (Optica 2022)
  (8), 160x160 MEMS OPA (Optica 2019) (8). About 24 / 40 are OPAs: the AMO grating-emitter core is still thin
  (focused-spot size, efficiency, polarization metrics). No change; recommend R5.

### splitter (50; 6 subtypes; SOI 27)
- S: Zhang 2013 Y-junction, Halir 2016 SWG MMI, Lu 2015 / Wang 2016 broadband DCs, rapid adiabatic couplers in 45 nm
  CMOS (two Wade conference papers on the same device family, both paywalled). P: Piggott 2017 Sci Rep
  fabrication-constrained inverse design. U: Halir 2012 colorless DC (scored 3). No change.

### crossing (33; other 17, swg 6, mmi 5, multilevel 5; paywalled 9 = 27 %)
- S: Bogaerts 2007, Ma 2013, Zhang 2013 Bloch-mode crossing array, 43 mdB MMI crossing (OE 2020), 0.007 dB three-mode-synthesis crossing (2017), Sacher 2017 tri-layer, Chiles
  2017. Coverage good; paywalled share is high but each pick has a curator reason. No change.

### mode_converter (35; mdm_mux 19, converter 11; industry 2)
- S: Luo 2014 Nat Commun (title only), Dai 2013, Ding 2013, Frellsen 2016. U: 8-channel hybrid mode / polarization demux (LPR 2014)
  (8, paywalled), 11-mode SWG demux (JLT 2018) (9, paywalled), Dana 2024 LSA 3D-printed photonic lantern (8, OA).
- Weak: two fiber OAM long-period-grating converters (10.1364/oe.421967, 10.1364/oe.435951); one PCM inverse-design
  paper mostly simulated (10.1515/nanoph-2023-0637).
- Corrections: pick Dana 2024; drop the second OAM grating converter.

### polarization (45; psr 20, pbs 15; pre-2016 15)
- S: Dai 2011, Fukuda 2006, Sacher 2014, Ding 2013, Watts four-port PBS. U: Liu 2011 OE SOI PSR (8, OA).
  P (no_class_hit): Shen 2015 Nat Photon 2.4 x 2.4 um PBS, Barwicz 2006 Nat Photon.
- Weak: Watts / Haus 2005 OL (score 0, FDTD only, paywalled); Itabashi 2008 system-level diversity circuit.
- Corrections: pick Liu 2011, add Shen 2015; drop both weak rows.

### resonator (62; ring 31, PhC 11; SOI 21, SiN 14)
- S: Spencer 2014 81 M, Ji 2017, Puckett 2021 422 M, Zhang 2017 TFLN, Asano 2017 PhC 11 M, Wu 2020 > 1e9, Lee 2012,
  Biberman 2012, Lončar-group 2024 TFLN 29 M. U: Wang 2021 LSA 4H-SiCOI Q 6.75e6 (9, OA), Gao 2021 COL TFLN Q > 1e8 (9, OA),
  Xie 2020 OE AlGaAs-on-insulator (9). P: Gondarenko 2009, Liu 2018 Optica AlN UV microrings, Ji 2021 APL Photonics.
- Weak: Bienstman 2009 slot-ring biosensor (sensor metrics), Tsang 2023 spectrometer (system), a 2 um soliton comb row.
- Corrections: picks Wang 2021, Gao 2021; drops biosensor, spectrometer.

### wdm (80; awg 29, cascaded_mzi 11, eg 5, tff 2; paywalled 7)
- S: Pathak 2014 AWG vs echelle, Horst 2013 IBM lattice, Xia 2007 IBM ring filter, Shi 2013 contra-DC, Piggott 2015
  (title only), mask-grid AWG study (PTL 2014). U: Brouckaert 2007 JLT SOI echelle (9, OA), Bogaerts 2006 JSTQE wavelength-
  selective functions (8, OA). N: Popovic 2006 OL multistage high-order microring filters (10.1364/ol.31.002571).
- Weak: dissertation (openalex:W2915271777), two system-level InP routers / MIMO demux, an AWG-PD FBG interrogator.
- Corrections: picks Brouckaert, Bogaerts 2006; add Popovic 2006; drops dissertation, InP router, MIMO demux.

### reflector (30; bragg 19; paywalled 6 = cap)
- S: Wang 2012 narrow-band Bragg (CMOS), Tan 2009 cladding-modulated, Oser 2019 > 80 dB coherency-broken, low-kappa SiN 2015. U: Wang 2011 PTL
  uniform / sampled sidewall gratings (8, paywalled; paywall share at cap). No change.

### phase_shifter (60; thermo_optic 27, phase_change 13, mems 8)
- S: Harris 2014, IBM 2010 NiSi heaters, Zhang 2019 GSST, Rios 2022, Edinger 2021 MEMS, Dong 2021 AlN piezo mesh.
  U: Rios 2015 Nat Photon PCM memory (5, paywalled), Zheng 2020 Adv Mater PIN heater (6; Majumdar at cap). Switch-class
  input: Fang 2011 PTL suspended-arm TO switch (9, paywalled). N: Dong 2010 OE ultralow tuning power racetracks.
- Weak: ULI passive achromatic phase element (not tunable).
- Corrections: add Dong 2010; drop the ULI row.

### switch_fabric (52; mzi_mesh 19, wss 12, mems 7)
- S: Seok 2016 / 2019 MEMS, Qiao 2017 32x32, Lu 2016 16x16, Perez 2017 hex mesh, NTT 2001 16x16 PLC, PILOSS 8x8.
  U: Han 2015 Optica 50x50 MEMS (9, OA), Tanizawa 2015 OE 32x32 PILOSS (9, OA), 32x32 Si switch with silica PLC
  connector (JLT 2018; 9, paywalled). P: Taballione 2019 SiN 8x8 mesh, Ribeiro 2016 4x4 universal circuit.
- Weak: two score-0 bulk free-space rows (LCoS module, 1296-port MEMS OXC), a single graphene all-optical switch device.
- Corrections: picks Han, Tanizawa; adds Taballione, Ribeiro; drops the two score-0 rows, the graphene device, and the
  2-channel CDC WSS (Kawashima cap swap).

### nonreciprocal (30; isolator 25, circulator 5; Lei Bi 4)
- S: Bi 2011 (title only), Shoji 2008, Huang / Pintus Bowers rings, Yan 2020 Optica SiN MO, Tian 2021, Sohn 2021,
  White 2022 passive nonlinear. U: Ghosh 2012 OE bonded Ce:YIG (8, OA), Huang 2016 JSTQE (9, paywalled; Bowers 3),
  Zhang 2019 Optica (7; Bi cap). N: Yu 2023 Nat Photon TFLN EO isolator (10.1038/s41566-023-01227-8).
- Weak: Lipson 2012 PRL (6, no numbers, paywalled), Kittlaus 2021 acousto-optic modulator (6).
- Corrections: pick Ghosh 2012, add Yu 2023; drop both weak rows.

### photodetector (77; ge_waveguide 23, apd 15; paywalled 16 = 21 %)
- S: Lischke 2021 265 GHz, Vivien 2012 zero-bias, Kang 2008 340 GHz GBP APD, Pernice 2012 SNSPD, Salamin 2018,
  Ding 2019 graphene > 110 GHz, Reddy 2020 98 % SNSPD. U: Vivien 2009 OE 42 GHz Ge PIN (8, OA), Korzh 2020 Nat Photon
  sub-3 ps SNSPD (9, OA), Assefa 2010 Nature Ge APD (7, paywalled), Gan 2013 Nat Photon graphene (5, paywalled).
  P (no_class_hit): Pospischil 2013 Nat Photon graphene PD; Schall 2014 ACS Photonics 50 Gb/s wafer-scale graphene.
- Weak: discrete free-space InGaAs SPAD (outside the PD scope note), a normal-incidence metasurface Ge PD preprint.
- Corrections: pick Vivien 2009, add Pospischil 2013; drop both weak rows.

### laser (101 incl. reserve; heterogeneous 20, dfb 16, comb 12; els_module 1; 5 seniors at cap)
- S: Fang 2006, Chen 2016 QD on Si, Jin 2021 Hertz-linewidth, Stern 2018 battery comb, Corato-Zanarella 2022, Yamaoka
  2020 108 GHz DML, Noda-group InP PCSELs (2). U: Gundavarapu 2019 Nat Photon sub-Hz Brillouin (9, OA), Tran 2022
  Nature submicrometre III-V on SiN (9, OA), Xiang 2023 Nature (8, Bowers cap), Shen 2020 Nature (8, Bowers cap),
  Fan 2020 OE 40 Hz hybrid InP-SiN (8). P: Xiang 2021 Science, Snigirev 2023 Nature, Raja 2019, Yoshida 2023 Nature
  PCSEL, Yoshida 2019 Nat Mater double-lattice PCSEL, Tran 2019 JSTQE ring-tuned lasers, Li 2022 Nat Commun Pockels
  laser, Wan 2018 PRJ QD lasers on Si; no_class_hit: Hirose 2014 Nat Photon (paywalled). ELS: Sawamura 2023 OFC CWDM
  TOSA for CPO external laser sources (in pool, cut by cap).
- Weak: els_module's only paper is a score-2 link-level result; an edge-emitting PhC laser with DFG filed as pcsel;
  a discrete WGM-stabilized module.
- Corrections: picks Gundavarapu (swap for the paywalled Blumenthal photonic-molecule paper), Tran 2022; adds Yoshida
  2023, Sawamura 2023 ELS; drops the four rows above.

### amplifier (45; rare_earth 16, soa 13, parametric 11)
- S: Liu 2022 Science Er:SiN, Riemensberger 2022 Nature TWPA, Kippenberg-group 2025 GaP OPA, Andrekson-group 2025 Nature, Vazquez-Cordova
  2014 Er:Al2O3 spirals, Van Gasse 2019 27 dB SOA, Davenport 2016, Matsumoto 2018 Fujitsu. U: Juodawlkis 2005 PTL SCOWA (9,
  paywalled), Mu 2020 PRJ Er:Al2O3 on Si3N4 18.1 dB (8, OA), several Er:TFLN. N: Kuyken 2011 OL 50 dB parametric gain.
  P (no_class_hit): Foster 2006 Nature.
- Weak: QD gain-material paper (modal gain only), PSA phase-regeneration system paper.
- Corrections: adds Foster 2006, Kuyken 2011; drops both weak rows.

### frequency_converter (30; shg 17)
- S: Wang 2018 Optica PPLN 2600 %/W cm2, Lu 2019 PPLN ring 250,000 %/W, McKenna 2022, Jankowski 2020, Lu 2020 SiN
  photoinduced, AlN microring 2500 %/W (Optica 2016), NTT PPZnLN, Covesion 2.5 W. U: Rao 2019 OE 4600 %/W cm2 (8, OA), Chen 2019 Optica
  QPM LN microring (8, OA), Chang 2016 Optica first TFLN converters (8, OA). P: Li 2016 Nat Photon single-photon
  frequency conversion, PRL 2019 QPM harmonic generation in an LN microdisk.
- Weak: bulk PPLN crystal in a polymer PIC (0.03 %/W).
- Corrections: pick Rao 2019; drop the bulk-PPLN row.

### waveguide_platform (65; straight 42; paywalled 15 = 23 %)
- S: Liu 2021 Nat Commun SiN, Blumenthal-group 0.034 dB/m, Shams-Ansari 2022 TFLN, Hausmann 2014 diamond, Lukin 2019
  SiC, Wilson 2019 GaP, Vlasov 2004 strip waveguides and bends, imec 300 mm. U: Bauters 2011 OE 0.045 dB/m (9, OA), Pfeiffer 2016 Optica
  Damascene (8, OA), Bogaerts 2005 JLT CMOS SOI wires (9, paywalled), Giewont 2019 JSTQE GF 300 mm (7, paywalled),
  Horikawa 2018 JSTQE PETRA 300 mm (9), Cardenas 2009 etchless (8), Dong 2010 shallow ridge (8), Fahrenkopf 2019 AIM
  MPW (scored 2). P: Ye 2023 PRJ foundry SiN, Luke 2020 OE wafer-scale TFLN, Bose 2024 LSA, Ji 2023 LPR, Pfeiffer 2018
  Optica Damascene reflow, Mashanovich 2011 mid-IR Si. K: Wang 2024 Nature lithium tantalate PICs, Rakowski 2020 45CLO.
- Weak: GVD-only paper, supercontinuum paper, PPLN OPA module (misfiled), suspended slot sensing waveguide.
- Corrections: picks Bauters, Giewont; adds Ye 2023, Luke 2020; drops the four weak rows.

### chip_chip_coupler (39; 4 subtypes; Koos 4)
- S: Lindenmann 2012, Billah 2018, Blaicher 2020, Theurer 2020 HHI flip-chip, imec 2022 flip-chip DFB, IBM 2013
  polymer flip-chip, IBM metamaterial chip-to-chip. All score >= 7 candidates in the input are already selected.
- Weak (score 6, kept for subtype coverage): 10.1364/oe.510036 (PWB laser used as a swept source), 10.1364/oe.474256
  (transmitter), 10.1109/jqe.2019.2958365, 10.1109/jlt.2014.2304305. No change; replacements need new harvesting.

## Paywalled share (181 / 1000 = 18.1 %)

- Within D124 (<= 20 %). By reason: curator 84, rank 44, subtype 39, reserve 14. Conference papers are 45 of the 181.
- Classes above 20 %: crossing 27 %, fiber_interface 26 %, laser 23 %, waveguide_platform 23 %, photodetector 21 %,
  chip_chip_coupler 21 % (curator overrides). 12 paywalled rows have score < 8; all carry curator reasons, but two are
  score 0 (Haus 2005 FDTD-only, Lucent 1296-port MEMS) and one is score 2 (link-level ELS chiplet): all three dropped.
  Remaining justified paywalled picks are mostly canonical (Nature Photonics / Nature landmarks, OFC / ECOC industry).
- After corrections: 179 paywalled (-2).

## Recommendations

- R1. Laser second pass: re-score the top 100 cut-by-cap laser candidates by citations per year (cost: one batch) and
  allow a curator landmark exemption to the senior cap (e.g. 5 for laser, or landmarks outside the cap with a reason),
  to admit Xiang 2021 / 2023, Shen 2020, Snigirev 2023, Raja 2019.
- R2. Fix the regex recall gaps listed in systemic finding 2 and re-run the prefilter delta (no new harvest needed).
- R3. Raise the scoring cap for laser / resonator / photodetector / waveguide_platform, or rank cut candidates by
  citations per year before the cap so that cap_rank is not dominated by lane order.
- R4. Write the WSS rule (LCoS module papers in or out) into scoring_prompt.md.
- R5. free_space_emitter: cap OPAs at about half of the class and refill with AMO grating emitters and metasurface
  couplers when S7 shows yield.
- R6. els_module and soa_dfb are thin (1 and 2 rows; 2 and 2 after corrections): a targeted OFC / ECOC / JLT pass for CPO
  external laser sources and high-power SOA-DFBs; these are mostly paywalled conference papers, so the manual list.
- R7. At distillation, record the version (arXiv vs journal) for the 180 arXiv-copy OA rows.

## Corrections file

`data/_staging/literature/audit_b_corrections.yaml`: 18 picks, 31 drops, 13 adds (9 from the pool, 4 verified by
OpenAlex singleton get on 2026-10-22: 10.1364/oe.18.020298, 10.1038/s41566-023-01227-8, 10.1364/ol.31.002571,
10.1364/ol.36.004401). Per-class in / out counts balance exactly; paywalled -2.
Cross-check with `audit_a_corrections.yaml` (present on 2026-10-22): no conflicts; 3 of my drops are also audit-A drops
(10.1038/s41377-020-0292-1, 10.1109/jphot.2009.2031596, 10.1364/ol.30.000138). Audit A has drops only (8, no picks or
adds), so an overlapping drop counts once and my pick for it keeps the class budget-neutral.
