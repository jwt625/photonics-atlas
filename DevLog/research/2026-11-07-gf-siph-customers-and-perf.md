# GlobalFoundries silicon photonics: platform, customers, measured performance

| | |
|---|---|
| Date | 2026-11-07 |
| Purpose | Evidence base for the GF column of the foundry PDK benchmark (DevLog-014) |
| Values | `2026-11-07-gf-siph-values.csv` (150 rows, 32 papers; 111 rows read in full text, 24 rows from the PsiQuantum Nature main text without the SI, 15 abstract-only rows) |
| Method | Web (WebSearch / WebFetch) plus read-only local `references/<id>/text.md`; three parallel research streams (platform + customers, 45 nm papers, 90 nm papers) and the PsiQuantum paper read by the coordinator. No repo file other than these two was written |
| Limits | The shared web-search budget (200 calls) ran out during the run: the 45 nm stream did not search UPenn, MIT or Columbia GF papers, and no further PsiQuantum or Xanadu papers were searched. Several primary hosts returned 403 or anti-bot pages (investors.gf.com, businesswire, opg.optica.org, pmc.ncbi.nlm.nih.gov, nature.com); the stream stopped on them. The PsiQuantum Nature SI PDF exceeds the 10 MB fetch limit and was not read |

## 1. Platform summary

| Platform / item | Facts (source type) | Date | URL |
|---|---|---|---|
| 90 nm SiPh (90WG; paper name CMS90WG) | 90 nm RF-SOI SiPh qualified on 300 mm at Fab 10 East Fishkill, previously 200 mm; Cadence design kit (secondary, eeNews) | 2018-03-19 | https://www.eenewseurope.com/en/glofo-extends-silicon-photonics-roadmap-2/ |
| 90 nm paper of record | Giewont et al., "300-mm Monolithic Silicon Photonics Foundry Technology", JSTQE 25(5), 10.1109/JSTQE.2019.2908790 | 2019 | https://research.ibm.com/publications/300-mm-monolithic-silicon-photonics-foundry-technology |
| 45CLO | Rakowski et al., OFC 2020 T3H.3: monolithic 45 nm CMOS-SiPh, 300 mm | 2020-03 | https://www.isi.edu/results/publications/15212/45nm-cmos-silicon-photonics-monolithic-technology-45clo-for-next-generation-low-power-and-high-speed-optical-interconnects/ |
| GF Fotonix launch | Monolithic 300 mm photonics + RF-CMOS; made at Malta NY; PDK 1.0 April 2022; "on-die lasers" listed; EDA partners Ansys, Cadence, Synopsys (GF release read via verbatim reprint; GF host 403) | 2022-03-07 | https://silicon-saxony.de/en/globalfoundries-next-generation-in-silicon-photonics-solutions-and-collaborates-to-advance-a-new-era-of-more-in-the-data-center/ |
| 45SPCLO = Fotonix (MPW naming) | CMC lists "GF Fotonix (45SPCLO)", 45 nm SOI, PSR / modulators / PDs / edge + grating couplers, far-BEOL V-groove; Europractice: "Nitride wave guide in MOL", Ge epi PD, Fab 8 Malta, 12-inch (secondary, MPW distributors) | accessed 2026-11-07 | https://www.cmc.ca/globalfoundries-fotonix-45spclo/ ; https://europractice-ic.com/technologies/photonics/globalfoundries/ |
| PsiQuantum custom flow | PsiQuantum + GF installed proprietary tools in GF 300 mm fabs (photonic chips in New York, control chips Dresden) (GF release, not fetched; AnandTech secondary) | 2021-05-05 | https://at-web1.www.anandtech.com/show/16660/globalfoundries-upgrades-for-silicon-photonics-in-quantum-computers |
| PsiQuantum Omega | "manufactured at GlobalFoundries in New York"; superconducting detector material and BTO introduced into the fab (customer) | 2025-02-26 | https://www.psiquantum.com/news-import/omega |
| PsiQuantum Fab 8 | "GlobalFoundries' Fab 8 in New York" (customer) | 2025-04-15 | https://www.psiquantum.com/news-import/psiquantum-afrl-omega |
| AMF acquisition | Announced 2025-11-17; completed 2025-11-18, USD 453M cash (SEC 6-K); AMF 200 mm Singapore, plan to 300 mm. InfiniLink (optical chiplet design) closed 2025-11-14, USD 48M | 2025-11-18 | https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000112/gfs-20260331.htm |
| AMF process names | NLM Photonics PICs on "GF AMF GP Process", gen 2 on "AMF HP Process" (customer) | 2026-03-16 | https://www.nlmphotonics.com/?p=5266 |
| Tech page | Gen 1 up to 100G/lambda, Gen 2 2x, Gen 3 path to 400G/lambda; 300 mm and 200 mm at Malta and Singapore; passive V-groove and non-undercut attach; BTO integration; "on-die lasers (in development)" (primary) | accessed 2026-11-07 | https://gf.com/technology-platforms/silicon-photonics/ |
| SCALE CPO module | OCI MSA; CWDM + DWDM bidirectional, 8/16 lambda; 50 and 100 Gb/s micro-ring modulators; TSVs (GF release via reprint) | 2026-05-07 | https://www.design-reuse.com/news/202530466-globalfoundries-accelerates-adoption-of-co-packaged-optics-for-advanced-ai-data-centers-with-scale-optical-module-solution/ |
| Quantum Technology Solutions unit | New GF quantum business, PsiQuantum quote (primary) | 2026-05-21 | https://gf.com/news-and-events/news/globalfoundries-launches-quantum-technology-solutions-to-scale-us-quantum-manufacturing/ |
| Commerce SiPh LOI | USD 300M CHIPS R&D LOI; SiPh materials, packaging, 3D hybrid bonding for NPO / CPO; Malta and Burlington (primary) | 2026-07-29 | https://gf.com/news-and-events/news/globalfoundries-signs-letter-of-intent-with-the-us-department-of-commerce-for-a-300-million-award-to-accelerate-us-silicon-photonics-leadership/ |
| Hybrid InP lasers | SMART Photonics InP lasers / SOAs flip-chipped into GF silicon, GA 2H 2027 (partner) | 2026-09-21 | https://smartphotonics.nl/knowledge-hub/smart-photonics-partners-with-globalfoundries |
| SiN + SNSPD (Xanadu) | GF to manufacture Xanadu SiN photonics and SNSPDs on the Malta 300 mm line (release reprint) | 2026-10-06 | https://www.bnnbloomberg.ca/press-releases/2026/10/06/xanadu-and-globalfoundries-announce-strategic-partnership-to-accelerate-utility-scale-quantum-manufacturing/ |
| SiPh revenue | Over USD 200M in 2025 per Q4 2025 call (transcript snippet, not fetched: unverified) | 2026-02-11 | https://www.fool.com/earnings/call-transcripts/2026/02/11/globalfoundries-gfs-q4-2025-earnings-transcript |

Conflicts and gaps (platform):
- 90WG fab site: eeNews 2018 says Fab 10 East Fishkill (since sold to onsemi); current 90WG site not found in a GF primary source.
- Names 45CLO / 45SPCLO / "CLO PDK" (Keysight 2026) / Fotonix appear to be one family; no GF primary page maps them.
- Lasers: 2022 release "on-die lasers" vs 2026 tech page "on-die lasers (in development)".
- N/A: GF primary statement of bonded heterogeneous III-V lasers; SiN layer specs; SiPh wafer capacity; any GF SiPh production in China.
- Full stream file with 35 fact rows: scratchpad `platform_customers.md` (not committed).

## 2. Customers and partners

Fab: `stated` = the source says the product or chip is made / manufactured / fabricated on GF; `partner_only` = quote, collaboration, PDK or ecosystem role; `(future)` = stated plan.

| Company | What on GF | Date | Source | Fab |
|---|---|---|---|---|
| PsiQuantum | Q1 photonic chips (New York) + control chips (Dresden) | 2021-05-05 | GF release (not fetched) via https://at-web1.www.anandtech.com/show/16660/globalfoundries-upgrades-for-silicon-photonics-in-quantum-computers | stated |
| PsiQuantum | Omega chipset (sources, SNSPDs, BTO switch), Fab 8 | 2025-02-26; 2025-04-15 | https://www.psiquantum.com/news-import/omega ; https://www.psiquantum.com/news-import/psiquantum-afrl-omega | stated |
| Lightmatter | Passage; "partnering with GlobalFoundries to mass produce Passage"; M1000 "utilizes the GF Fotonix" platform | 2024-11-18; 2025-03-31 | https://lightmatter.co/blog/lightmatter-and-globalfoundries-partner-to-mass-produce-passage-platform/ ; https://lightmatter.co/press-release/lightmatter-unveils-passage-m1000-photonic-superchip-worlds-fastest-ai-interconnect/ | stated (future, mass production) |
| NLM Photonics | Silicon-organic-hybrid PICs on AMF GP / HP | 2026-03-16 | https://www.nlmphotonics.com/?p=5266 | stated |
| Xanadu | Photonic chips (2022 plan); SiN + SNSPD production on Malta 300 mm (2026) | 2022-03-14; 2026-10-06 | https://picmagazine.net/article/114406/Xanadu_Announces_Collaboration_With_GlobalFoundries (trade reprint); bnnbloomberg reprint above | stated (future) |
| Siluxtek | 200G/lane SiPh receiver chips | 2026-03 | GF 6-K https://www.sec.gov/Archives/edgar/data/0001709048/000170904826000111/globalfoundries1q2026earni.htm | stated (future) |
| NVIDIA | 2022 quote: interconnect solutions "manufactured with" Fotonix; no product named | 2022-03-07 | silicon-saxony reprint (Sec. 1) | stated (future, quote only) |
| Ayar Labs | TeraPHY optical I/O chiplet: "demonstrated on" GF 45 nm (2020), "first working silicon on the platform" (2022), UCIe TeraPHY "enabled by" Fotonix (2025) | 2020-12-02; 2022-03-07; 2025-03-31 | https://www.hpcwire.com/off-the-wire/ayar-labs-demonstrates-optical-interconnect-on-globalfoundries-photonics-manufacturing-process/ ; https://www.eejournal.com/industry_news/ayar-labs-unveils-worlds-first-ucie-optical-chiplet-for-ai-scale-up-architectures/ | partner_only in primary wording; "built using 45SPCLO" only in secondary https://gazettabyte.com/?p=146250 |
| Ranovus | Odin optical I/O and 800G CPO "based on GF Fotonix" | 2022-03-07 | https://ranovus.com/ranovus-and-gf-fotonix-mar7-2022/ | partner_only (strict reading) |
| Cisco | Custom SiPh solution with own PDK (GF release); 2026 supporting quote | 2022-03-07; 2026-07-29 | Sec. 1 reprint; LOI URL | partner_only |
| Marvell | SiGe capacity at Burlington for optics (SiGe stated, SiPh not) | 2026-09-17 | https://gf.com/news-and-events/news/globalfoundries-and-marvell-expand-collaboration-fornext-generation-optical-connectivity/ | partner_only for SiPh |
| Broadcom, MACOM | Supporting quotes | 2022-03-07; 2026-07-29 | Sec. 1 reprint; LOI URL | partner_only |
| SMART Photonics | InP laser / SOA flip-chip service | 2026-09-21 | Sec. 1 | partner_only |
| Teramount, SENKO, Corning (+EXFO) | Fiber attach / detachable interfaces / CPO showcase | 2024-03-26; 2026-03 | GF 6-K above; https://lightwaveonline.com/home/article/55002231/teramount-and-globalfoundries-partner-on-driving-new-silicon-photonic-solutions (secondary) | partner_only |
| Lightwave Logic | Polymer modulator in GDSFactory PDK for GF SiPh (snippet, not fetched) | 2026-03-16 | https://www.accessnewswire.com/newsroom/en/industrial-and-manufacturing/lightwave-logic-high-speed-modulator-platform-now-available-in-gds-fac-1147929 | partner_only |
| Cadence, Ansys, Synopsys | Fotonix design flow / simulation | 2022-03-07 | https://eejournal.com/industry_news/cadence-collaborates-with-globalfoundries-to-advance-silicon-photonics-ic-design | partner_only |
| Keysight, Flexcompute, Luceda, StarIC | CLO PDK in ADS; PhotonForge PDK; 45SPCLO Luceda PDK; MRM driver / TIA IP | 2026-03..06 | https://www.keysight.com/us/en/about/newsroom/news-releases/2026/0603_pr26-075-keysight-expands-photonics-design-ecosystem-with-globalfoundries-pdk.html ; https://www.photonicsonline.com/doc/luceda-photonics-and-globalfoundries-announce-strategic-collaboration-to-deliver-luceda-pdk-accelerating-0001 | partner_only |
| AMD, Lumentum, Meta, Microsoft, Qualcomm | Supporting quotes on the 2026 LOI | 2026-07-29 | LOI URL | partner_only |
| Celestial AI, Rockley Photonics | No GF link found | N/A | N/A | not_found |

## 3. Papers (GF fabrication stated or platform named in the paper)

`in_repo` checked against `data/registry/sources.csv` (DOI, arXiv id, title) and `data/components/components.csv`.

| # | Paper | Venue, year | DOI / arXiv | GF process (as stated) | Flow | Full text | in_repo | Rows |
|---|---|---|---|---|---|---|---|---|
| 1 | A manufacturable platform for photonic quantum computing (PsiQuantum) | Nature 641, 876-883, 2025 | 10.1038/s41586-025-08820-7 / 2404.17570 | Baseline: co-developed with GF, fabricated in GF 300 mm foundry; next-gen devices: fab not named | customer_flow / unstated | main text yes, SI no | absent (EO atlas candidate psiquantum2025 only) | 24 |
| 2 | 300-mm Monolithic Silicon Photonics Foundry Technology | JSTQE 2019 | 10.1109/JSTQE.2019.2908790 | CMS90WG | public_pdk / development | yes (local) | present_with_components | 20 |
| 3 | Integrated Metamaterial Interfaces for Self-Aligned Fiber-to-Chip Coupling in Volume Manufacturing | JSTQE 2019 | 10.1109/JSTQE.2018.2879018 | GF 300 / 200 mm (ack) | unstated | yes (local) | present_with_components | 6 |
| 4 | A CMOS Compatible Monolithic Fiber Attach Solution ... | OFC 2020 Th3I.4 | 10.1364/OFC.2020.Th3I.4 | GF 300 mm, IOSMF PDK coupler | public_pdk | yes (local) | present_with_components | 4 |
| 5 | Monolithically Fabricated Subwavelength Grating Filters for O-band MUX/DEMUX | CLEO 2020 | 10.1364/CLEO_SI.2020.SM4J.2 | 90WG | public_pdk | yes (local) | present_with_components | 4 |
| 6 | Compact MMI-Based AWGs in a Scalable Monolithic Silicon Photonics Platform | IEEE PJ 2021 | 10.1109/JPHOT.2021.3099436 | GF monolithic (cites Giewont 2019) | public_pdk | yes (local) | present_with_components | 3 |
| 7 | Fabrication-Tolerant O-Band WDM Filter With Phase-Balanced Tapered Arms ... | JLT 2024 | 10.1109/JLT.2023.3300875 | GF monolithic, 160 nm Si | public_pdk | yes (local) | present_with_components | 5 |
| 8 | Straight and curved distributed Bragg reflector design for compact WDM filters | OE 2023 | 10.1364/OE.485609 | GF monolithic | public_pdk | yes (local) | present_with_components | 4 |
| 9 | Ultra-fast high-power Ge PIN photodetectors ... 300-mm monolithic CMOS SiPh foundry | CLEO 2025 PD | 10.1364/CLEO_AT.2025.PD104_7 | GF 300 mm, node not stated | unstated | yes (local) | present_with_components (fab_org_ids empty, D80b) | 4 |
| 10 | Low-loss and broadband adiabatic PSR on a CMOS-integrated SiPh platform | OFC 2024 M1J.5 | 10.1364/OFC.2024.M1J.5 | Fotonix design rules | unstated | yes (local) | present_with_components (fab_org_ids empty) | 4 |
| 11 | A universal 3D imaging sensor on a silicon photonics platform | Nature 2021 | 10.1038/s41586-021-03259-y / 2008.02411 | CMS90WG MPW | public_pdk | yes (arXiv) | absent | 4 |
| 12 | A reconfigurable non-linear active metasurface for coherent wave down-conversion | arXiv 2024 | 2411.09965 | GF 90 nm | unstated | yes (arXiv) | absent | 4 |
| 13 | Monolithically integrated silicon nitride platform | OFC 2021 Th1A.46 | DOI not confirmed | GF monolithic | unstated | no (abstract) | absent | 2 |
| 14 | 3D Integrated Laser Attach Technology on a 300-mm Monolithic CMOS SiPh Platform | JSTQE 2023 | 10.1109/JSTQE.2023.3238290 | GF 300 mm | unstated | no (abstract) | absent | 1 |
| 15 | Microring Modulators in a New Silicon Photonics-Optimized 45 nm ... Platform | CLEO 2021 SW3C.1 | 10.1364/CLEO_SI.2021.SW3C.1 | 45CLO (test vehicle) | unstated | yes | absent | 9 |
| 16 | Photonic crystal modulator in a CMOS foundry platform | CLEO 2021 | DOI not resolved | 45CLO | unstated | yes (NSF PAR) | absent | 4 |
| 17 | High Q, Compact Photonic Crystal Nanobeam Cavity ... CMOS Silicon Photonics Process | GFP 2021 | 10.1109/GFP51802.2021.9673876 | 45CLO | unstated | yes | absent | 1 |
| 18 | Reflectionless dual standing-wave microcavity resonator units for PICs | OE 2020 | 10.1364/OE.403486 | 45SPCLO (named in text) | unstated | yes | absent | 2 |
| 19 | Reflectionless standing-wave operation in microring resonators | OFC 2022 | DOI not resolved | 45CLO | unstated | yes (NSF PAR) | absent | 2 |
| 20 | Miniature, highly sensitive MOSCAP ring modulators in co-optimized electronic-photonic CMOS | Photonics Res. 2022 | 10.1364/PRJ.438047 | 45CLO, modified implants | customer_flow | yes | absent | 6 |
| 21 | Fast-Tuning Adiabatic Microrings for CROW Filters and Athermal WDM Receivers in a 45 nm SOI CMOS Process | CLEO 2022 | 10.1364/CLEO_SI.2022.SF4M.2 | GF next-gen 45 nm | unstated | yes | absent | 3 |
| 22 | RF-optical signal conversion via Dual Active-Cavity modulator ... | FiO 2024 | 10.1364/FIO.2024.FTh1D.4 | 45CLO | unstated | yes | absent | 1 |
| 23 | 0.08 fF, 0.72 nA dark current, 91% QE, 38 Gb/s Nano-photodetector on a 45 nm CMOS Silicon-Photonic Platform | arXiv 2024 | 2401.03527 | 45SPCLO | unstated | yes | absent | 5 |
| 24 | Monolithically Integrated Microring Transmitter and Receiver for High-Density 3D CPO (Lightmatter) | OFC 2025 Tu3J.6 | 10.1364/OFC.2025.Tu3J.6 | 45SPCLO | unstated | yes (company-hosted PDF) | absent | 6 |
| 25 | C2PO: Coherent Co-packaged Optics using offset-QAM-16 ... | OE 2025 | 10.1364/oe.571527 / 2506.12160 | 45SPCLO | unstated | yes (arXiv v1) | absent | 4 |
| 26 | Monolithic Silicon-Photonics Sign-Sign Dot-Product Circuits ... | Nanophotonics 2026 | 10.1002/nap2.70063 | 45SPCLO | unstated | yes | absent | 1 |
| 27 | A large-scale coherent 4D imaging sensor | Nature 2026 | 10.1038/s41586-026-10183-6 | 45SPCLO | unstated | yes | absent | 2 |
| 28 | Scalable Feedback Stabilization of Quantum Light Sources on a CMOS Chip | arXiv 2024 (Nat. Electron. 2025 version not read) | 2411.05921 | 45SPCLO preliminary data; main device 45RFSOI zero-change | unstated / zero_change | yes | absent | 3 |
| 29 | Monolithically integrated 112 Gbps PAM4 optical transmitter and receiver in a 45 nm CMOS-SiPh process | OE 2023 | 10.1364/oe.495246 | Fotonix (45SPCLO) | unstated | no (abstract; Optica anti-bot) | absent | 2 |
| 30 | Beam shaping for ultra-compact waveguide crossings on monolithic silicon photonics platform | OL 2020 | 10.1364/OL.402446 | 45CLO | unstated | no (abstract) | absent | 2 |
| 31 | Multi-layer inverse design of vertical grating couplers for high-density, commercial foundry interconnects | OE 2022 | 10.1364/oe.466015 | 45CLO | unstated | no (abstract; Optica anti-bot) | absent | 7 |
| 32 | Cubic-wavelength mode volume photonic crystal nanobeam cavities in a monolithic CMOS platform | OL 2023 | 10.1364/ol.481483 | 45CLO (index record) | unstated | no (abstract) | absent | 1 |

Repo note: `lit:bian2025` and `lit:lee2024` are GF-authored (all authors GF; lee2024 states Fotonix design rules) but carry empty `fab_org_ids` under D80b (no explicit fabrication sentence), so their values (0.96 A/W median over >400 PDs; PSR 0.35 dB) do not reach the GF column. That is the D80b ruling working as written, not an extraction error; a coordinator ruling would be needed to change it.

## 4. PsiQuantum paper in depth (Nature 2025, main text read; SI not read)

Fabrication statements (main text):
- Baseline stack "developed in partnership with GlobalFoundries" and fabricated in GF's 300 mm high-volume foundry; >20 lithography levels; modules: SOI waveguides, NbN SNSPD layer, metal-filled deep trenches, resistive heaters with undercut, grating couplers, Cu BEOL, Al redistribution.
- Next-generation section (SiN waveguides / crossings / splitters, edge couplers, BTO, PNRD, cascaded SiN source): "derived from several process flows"; fab not named. BTO grown by MBE on full 300 mm wafers with a process "compatible with foundry processes". So the record-low SiN and coupler values are **not stated as GF-fabricated** in the paper. PsiQuantum's 2025-02-26 Omega release says detectors and BTO were introduced into the GF fab, but a release is not the paper; the SI (22 figures) may say more.

| Device | Value (Nature) | arXiv v1 value | Conditions / statistic | Locator | GF stated |
|---|---|---|---|---|---|
| SiN single-mode waveguide | 1.8 +/- 0.2 dB/m (0.018 dB/cm) | 1.58 +/- 0.50 dB/m | cutback; "example wafers"; temperature N/A | Sec. Low-loss SiN; Fig. 5a | no |
| SiN multimode waveguide | 0.5 +/- 0.3 dB/m (0.005 dB/cm) | 0.39 +/- 0.12 dB/m | cutback | Fig. 5a | no |
| SiN crossing | 1.2 +/- 0.4 mdB | 1.6 +/- 0.1 mdB | per component; ~2x above target | Fig. 5b | no |
| SiN splitter (type not stated) | 0.5 +/- 0.2 mdB | same | per component | Fig. 5b | no |
| Edge coupler, SMF-28 | 127 +/- 18 mdB | 120 +/- 17 mdB | best designs; per-coupler isolation not described in main text | Sec. Fibre-to-chip; Fig. 5c | no |
| Edge coupler, UHNA4 | 52 +/- 12 mdB | 53 +/- 12 mdB | same | Fig. 5c | no |
| BTO-on-SiN phase shifter | 53 +/- 3 dB/m; ~100 mdB for 2 mm | same | cutback, 95 % CI | Fig. 5f | no |
| BTO MZI | VpiL 0.62 V cm DC (single arm); alpha VpiL 0.33 +/- 0.02 dB V | same | no EO bandwidth measured | Fig. 5g | no |
| BTO film | r_eff > 1000 pm/V; thickness 3 sigma < 3 % over 300 mm | same | free-space | Fig. 5d | no |
| SNSPD (NbN, hairpin) | median 93.4 %, mean 88.9 +/- 3.5 % on-chip efficiency | same | ~2 K; N not stated; DCR only plotted; jitter not reported | Sec. Photon detection; Fig. 2e | yes |
| PNRD (SiN-coupled) | median 98.9 % (best design); mean 96.2 +/- 4.3 % over 6 devices | same | up to 4-photon resolution | Fig. 4e,f | no |
| MZI (thermal) | ER > 50 dB with heralded single photons | same | ~2 K; heater P_pi not given | Fig. 2d | yes |
| Pump filter network | 99.1 +/- 1.2 dB rejection; ~1 dB signal / herald loss (origin not stated) | same | ~115 dB pump-to-SNSPD incl. shielding | Sec. HSPS; Fig. 2c | yes |
| Grating coupler | "about 3 dB" fibre-to-chip | same | system context, scope unspecified | Sec. Chip-to-chip | yes |
| HSPS / benchmarks | purity 99.5 +/- 0.1 %; HOM 99.50 +/- 0.25 %; SPAM 99.98 +/- 0.01 %; fusion 99.22 +/- 0.12 %; chip-to-chip 99.72 +/- 0.04 % | same | not accounting for loss | Figs. 2b, 3; Table 1 | yes |

Not reported in the main text: Si (SOI) waveguide loss, thermal P_pi, ring Q, wavelengths in nm (only "C band" in general), SNSPD dark-count rate as a number, timing jitter, die / wafer yield numbers. Data repository: http://github.com/PsiQ/2404_17570.

## 5. Best values per benchmark row

Public PDK / MPW / GF-authored platform papers vs customer-specific flows. Basis measured unless noted. "fab not named" = PsiQuantum next-generation device (Sec. 4).

| Benchmark row | Best public-PDK / platform value | Paper | Customer-specific flow value | Paper |
|---|---|---|---|---|
| Si waveguide loss | < 1.5 dB/cm single-mode (text); ~0.5 dB/cm multimode (histogram mode, figure-read) | Giewont 2019, CMS90WG | N/A | - |
| SiN waveguide loss | < 0.3 dB/cm (roadmap, "development"); < 0.35 dB/cm (abstract only) | Giewont 2019; Bian OFC 2021 | 0.005 dB/cm MM, 0.018 dB/cm SM (fab not named) | PsiQuantum 2025 |
| Bend loss | 0.024 dB/90 deg (w 300 nm, R 10 um, 1310 nm); median ~0.028 over 5 sites | Papadovasilakis JLT 2024 | N/A | - |
| Edge coupler IL per facet | 0.7 dB TE / 1.4 dB TM, V-groove self-aligned SMF, O-band; 0.9 dB TE over 100 samples | Barwicz 2019 = Giewont 2019 (same device); Peng OFC 2020 | 0.052 dB UHNA4, 0.127 dB SMF-28 (scope unspecified; fab not named) | PsiQuantum 2025 |
| Grating coupler IL | 4.7 dB single-pol (abstract only); ~4 dB (setup statement) | Multi-layer inverse design of vertical GCs, OE 2022, 45CLO; C2PO 2025, 45SPCLO | ~3 dB (author estimate, scope unspecified) | PsiQuantum 2025 |
| Grating coupler 1 dB BW | N/A (only 3 dB BW: 75 nm single-pol, 89 nm dual-pol, abstract) | OE 2022, 45CLO | N/A | - |
| MMI excess loss | N/A | - | 0.0005 dB splitter, type not stated (fab not named) | PsiQuantum 2025 |
| Crossing loss | 0.197 +/- 0.017 dB mean over 8 chips, 35 dB XT (abstract only) | Chandran OL 2020, 45CLO | 0.0012 dB SiN (fab not named) | PsiQuantum 2025 |
| AWG IL | N/A (not reported) | - | N/A | - |
| AWG crosstalk | 9.6-12.6 dB (4-ch MMI-AWG) | Taha IEEE PJ 2021 | N/A | - |
| Thermo-optic P_pi | 2.81 mW undercut heater; wafer range 2.73-2.91 mW | Giewont 2019 | N/A (not reported) | PsiQuantum 2025 |
| Ge PD responsivity | 0.96 A/W median, > 400 devices, 1310 nm, -1 V (repo fab empty, D80b); 0.96 A/W resonant AFP PD at -2 V, 45SPCLO | Bian CLEO 2025; arXiv 2401.03527 | - | - |
| Ge PD 3 dB BW | 56 GHz at -1 V (45SPCLO); > 135 GHz at -2 V is extrapolated past the 110 GHz LCA (author_estimate, D435) | Lightmatter OFC 2025; Bian CLEO 2025 | - | - |
| Ge PD dark current | 0.72 nA at -1 V (resonant AFP PD, 45SPCLO); < 20 nA mean over > 400 lateral PDs | arXiv 2401.03527; Bian CLEO 2025 | - | - |
| MZM VpiL | N/A in accessible GF Si papers | - | 0.62 V cm BTO-on-SiN, single arm (BTO: excluded from native cells by D903; fab not named) | PsiQuantum 2025 |
| MZM EO BW | > 35 GHz (50G TW-MZM under qualification, equipment-limited) | Giewont 2019 | N/A | - |
| Ring modulator BW | 30.9 +/- 2 GHz at -1 V, O-band (45SPCLO); > 30 GHz spoked ring (45CLO) | Lightmatter OFC 2025; CLEO 2021 SW3C.1 | - | - |
| EAM BW | N/A | - | - | - |
| Laser | up to 20 mW flip-chip III-V butt-coupled (abstract only) | Bian JSTQE 2023 | - | - |
| Ring intrinsic Q (extra) | 0.75-0.85 x 10^6 full-rib ring, preliminary 45SPCLO | arXiv 2411.05921 Supp. 1.5 | - | - |
| SNSPD efficiency (extra) | - | - | 93.4 % median (GF stated); PNRD 98.9 % median (fab not named) | PsiQuantum 2025 |

## 6. Gaps

- No accessible GF value for: AWG IL, MMI excess loss (Si), 1 dB grating-coupler bandwidth, Si MZM VpiL, EAM, ring-modulator efficiency with a stated method at C-band, laser metrics beyond one abstract.
- 45CLO / 45SPCLO platform paper (Rakowski OFC 2020) is paywalled; its edge-coupler (0.7-1.4 dB) and PD numbers appear in other papers only as citations and were not entered.
- PsiQuantum SI (22 figures) not read: needed to settle coupler scope (per coupler vs two-facet), crossing / splitter cascade method, SNSPD N, dark counts, jitter and where next-generation devices were made.
- Not searched (budget): UPenn / Aflatouni 45CLO papers, MIT, Columbia GF 45 nm papers, Ayar Labs ISSCC / VLSI / JSSC papers, Xanadu GF papers, PsiQuantum follow-up papers (SNSPD, BTO), GF OFC 2023-2026 device papers (Bian / Hirokawa group).
- Platform-name ambiguity: several university papers name only "GF monolithic platform" and cite Giewont 2019; the 45 nm vs 90 nm attribution of Bian 2025 and Lee 2024 is not stated.

## 7. Prioritized ingest list

| Rank | Paper | Why | Open access |
|---|---|---|---|
| 1 | A manufacturable platform for photonic quantum computing, Nature 2025, 10.1038/s41586-025-08820-7 (+ SI) | Best-in-class SiN loss, edge coupler, crossing, SNSPD; absent from repo; SI resolves scope / fab | yes (CC BY 4.0; SI > 10 MB) |
| 2 | Rakowski et al., 45CLO platform, OFC 2020 T3H.3, 10.1364/OFC.2020.T3H.3 | Platform paper of record for 45CLO (edge coupler, PD, modulators) | no |
| 3 | Monolithically Integrated Microring Tx and Rx for 3D CPO (Lightmatter), OFC 2025 Tu3J.6 | Ring-mod BW 30.9 GHz, PD 56 GHz, 45SPCLO | yes (company-hosted PDF) |
| 4 | Multi-layer inverse design of vertical grating couplers, OE 2022, 10.1364/oe.466015 | Only GF grating-coupler IL / BW across 3 wafers | yes (Optica OA; anti-bot blocked fetch) |
| 5 | Beam shaping for ultra-compact waveguide crossings, OL 2020, 10.1364/OL.402446 | Crossing loss over 8 chips | no |
| 6 | 0.08 fF, 0.72 nA ... Nano-photodetector on 45 nm, arXiv 2401.03527 | PD dark current / responsivity, 45SPCLO | yes |
| 7 | Scalable Feedback Stabilization of Quantum Light Sources on a CMOS Chip, arXiv 2411.05921 (Nat. Electron. 2025) | 45SPCLO ring Qi 0.75-0.85 M | yes (arXiv) |
| 8 | A universal 3D imaging sensor on a silicon photonics platform, Nature 2021, 10.1038/s41586-021-03259-y | CMS90WG MPW thermo-optic switch power / timing | yes (arXiv 2008.02411) |
| 9 | Monolithically integrated 112 Gbps PAM4 Tx and Rx in a 45 nm CMOS-SiPh process, OE 2023, 10.1364/oe.495246 | Fotonix MZM + PD link; likely MZM BW / VpiL in full text | yes (Optica OA; anti-bot blocked fetch) |
| 10 | Miniature, highly sensitive MOSCAP ring modulators, Photonics Res. 2022, 10.1364/PRJ.438047 | 45CLO MOSCAP ring, ~175 pm/V | yes |
| 11 | A large-scale coherent 4D imaging sensor, Nature 2026, 10.1038/s41586-026-10183-6 | 45SPCLO V-groove and switch loss budget | yes |
| 12 | Bian et al., Monolithically integrated silicon nitride platform, OFC 2021 Th1A.46 | GF SiN < 0.35 dB/cm, Si-SiN 0.026 dB transition | no |
| 13 | Bian et al., 3D Integrated Laser Attach Technology, JSTQE 2023, 10.1109/JSTQE.2023.3238290 | Only GF laser-attach metrics | no |
| 14 | Microring Modulators in a New Silicon Photonics-Optimized 45 nm Platform, CLEO 2021, 10.1364/CLEO_SI.2021.SW3C.1 | 45CLO ring BW > 30 GHz | yes |
| 15 | Sub-wavelength grating Si to SiN interlayer couplers in commercial foundry SiPh, OE 2026, 10.1364/oe.583483 | 45SPCLO Si-SiN transition (abstract had no numbers) | yes (Optica OA) |

All values: `2026-11-07-gf-siph-values.csv`. Coordinator edits to stream rows: Bian CLEO 2025 > 135 GHz set to `author_estimate` (D435); Peng OFC 2020 damp-heat row renamed `il_drift_db` (it is a drift, not an IL). Parameters marked "(not in schema)" are registry gaps.
