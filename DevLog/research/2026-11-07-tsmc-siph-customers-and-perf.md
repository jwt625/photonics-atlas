# TSMC silicon photonics: customers, fab statements, measured performance

| | |
|---|---|
| Date | 2026-11-07 |
| Purpose | Evidence base for the TSMC SiPh column of the foundry PDK benchmark (DevLog-014; stream S1 of DevLog-015) |
| Values | `2026-11-07-tsmc-siph-values.csv` (50 rows: 43 values, 7 N/A rows; 4 rows already in the repo, marked) |
| Method | Local first: repo registry and component tables, OFC 2026 extracted texts, EO atlas and packaging atlas texts, owner local copies of public papers (text extracts reused; figures re-rendered for reading). Then about 65 WebSearch / WebFetch calls. No repo file other than these two was written |
| Limits | Hosts that returned 403 / anti-bot and were not retried: investors.broadcom.com, businesswire.com, globenewswire.com, research.tsmc.com, semiwiki.com, eprints.soton.ac.uk, dblp (Anubis). api.crossref.org returned 429 after three queries. Optica full texts are paywalled (abstract pages only). The TSMC OFC 2025 SiN paper, the ECTC 2021 COUPE paper and the OFC 2025 TSMC invited paper were not read (no local copy) |

## 1. TSMC platform statements (TSMC primary)

| Item | What TSMC states | Date | Source |
|---|---|---|---|
| PIC / EIC nodes | Photonic engine on 300 mm; PIC "N65 and beyond", EIC "N7 and beyond"; PIC-EIC via COUPE or CoWoS; 65 nm CMOS-based 300 mm SOI line, Ge selective epi, 6 metal BEOL, CD 3 sigma within 2 nm | 2024-12-07 | IEDM 2024 paper (Sec. 3 row 1), p.1 Sec. I, II.B |
| COUPE roadmap | "TSMC plans to qualify COUPE for small form factor pluggables in 2025", then CoWoS CPO in 2026; SoIC-X EIC-on-PIC stacking | 2024-04-24 | https://pr.tsmc.com/english/news/3136 (read via verbatim reprint https://www.silicon.co.uk/press-release/tsmc-celebrates-30th-north-america-technology-symposium-with-innovations-powering-ai-with-silicon-leadership) |
| COUPE in 3DFabric list | "silicon photonics integration with TSMC's Compact Universal Photonic Engine (COUPE)"; no customers named | 2025-04-24 | https://pr.tsmc.com/english/news/3228 |
| COUPE on substrate | "co-packaged optics solution using COUPE on substrate beginning production in 2026"; "featured in a 200Gbps micro-ring modulator"; 2X power efficiency, 10X latency vs pluggable (vendor claim); no customers named | 2026-04-23 | https://pr.tsmc.com/english/news/3302 |
| Volume production | "TSMC's 65nm silicon photonics technology is in volume production"; "achieved 200 gigabits per second (Gbs) optical signal modulation and greater than 99% 3D stacking yield on engineering samples" (undated web page) | accessed 2026-11-07 | https://www.tsmc.com/english/dedicatedFoundry/technology/platform_HPC_tech_connectivity |
| SEMICON Taiwan 2025 | TSMC director quoted: PIC contains "an advanced 200G micro-ring modulator"; Ge PD ">110 GHz" (trade reports, secondary) | 2025-09-08 | https://www.trendforce.com/news/2025/09/09/news-silicon-photonics-in-the-spotlight-tsmc-lifts-the-curtain-on-coupe-at-semicon-taiwan/ ; https://www.simpletechtrend.com/en/post/semicon2025_silicon-photonics-summit_tsmc-en |

## 2. Customers: claim vs evidence

Evidence classes: `paper` = a peer-reviewed / conference paper by the customer names TSMC for its photonics; `primary PR` = customer or TSMC release names TSMC / COUPE for the product; `PR, partner only` = TSMC named as partner without saying what it makes; `secondary` = trade press or analyst only.

| Company | Claim checked | What the best source says (verbatim fragments) | Date | Source | Evidence class |
|---|---|---|---|---|---|
| NVIDIA | CPO (Quantum-X / Spectrum-X Photonics) on TSMC COUPE | Release: ecosystem "includes TSMC"; TSMC CEO quote: "chip manufacturing and TSMC-SoIC 3D chip stacking"; COUPE and MRM not named | 2025-03-18 | https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-Announces-Spectrum-X-Photonics-Co-Packaged-Optics-Networking-Switches-to-Scale-AI-Factories-to-Millions-of-GPUs/ | PR, partner only |
| NVIDIA | same | Developer blog: optical engines "leveraging TSMC's COUPE technology"; "three COUPE-based optical engines, each supporting 1.6Tbps"; "Deep collaboration with TSMC has helped NVIDIA solve ... manufacturing problems ... associated with Micro Ring Modulators" | 2025-08-26 | https://developer.nvidia.com/blog/how-industry-collaboration-fosters-nvidia-co-packaged-optics/ | primary PR (stated) |
| NVIDIA | same | IEDM 2025 (B. G. Lee): Fig. 2 "NVIDIA's CPO technology [6] based on TSMC's COUPE process [13]" | 2025-12-06 | 10.1109/IEDM50572.2025.11353715 | paper (position paper, no device data) |
| NVIDIA | same | OFC 2026 M2A.7 (D. Patel): GTC 2025 1.6 Tbps CPO switch "featuring MRMs fabricated using ... TSMC Compact Universal Photonic Engine (COUPE) process" | 2026-03 | 10.1364/ofc.2026.m2a.7 | paper (review, no own data) |
| NVIDIA | 7 nm EIC / 65 nm PIC DWDM link on TSMC | ISSCC 2026 23.1 and OFC 2026 M4B.2 do not name the fab ("65nm SiPh process", "Cu-Cu hybrid bonding"); M4B.2 cites the TSMC IEDM 2024 platform paper as ref [2] for the "3D-integrated SiPh platform" | 2026-02-17; 2026-03 | 10.1109/ISSCC49663.2026.11409081; OFC 2026 M4B.2 | paper, fab by citation only |
| Broadcom | Tomahawk 6 Davisson CPO on COUPE | Broadcom release: "heterogeneously integrating TSMC Compact Universal Photonic Engine (TSMC COUPE) technology-based optical engines"; TSMC NA president: "By leveraging our COUPE process ... support Broadcom in bringing the Tomahawk 6 - Davisson platform to fruition" (read via reprint; Broadcom IR host 403) | 2025-10-08 | https://www.itiger.com/news/2573692637 (reprint of the GlobeNewswire release) | primary PR (stated) |
| Broadcom | earlier gens (Humboldt, Bailly) | PIC fab not found | - | - | N/A |
| Ayar Labs | TeraPHY on TSMC COUPE | Alchip + Ayar release at TSMC NA OIP forum: TeraPHY "co-packaged with Alchip's advanced solutions on a common substrate"; COUPE, foundry, fab not mentioned | 2025-09-26 | https://markets.financialcontent.com/franklincredit/article/gnwcq-2025-9-26-alchip-and-ayar-labs-unveil-co-packaged-optics-for-ai-datacenter-scale-up | PR, partner only |
| Ayar Labs | same | Trade press: Alchip + Ayar engine "built on TSMC's Compact Universal Photonic Engine (COUPE) platform" at TSMC OIP Europe; Tom's Hardware calls the reference design a mockup; no company quote | 2025-12-03 | https://picmagazine.net/article/123062/Alchip_and_Ayar_Labs_debut_first_TSMC_COUPE-based_optical_connectivity_engine_for_AI_chips ; Tom's Hardware (same story) | secondary |
| Ayar Labs | earlier GF flow | TeraPHY "demonstrated on" GF 45 nm (2020), UCIe TeraPHY "enabled by" GF Fotonix (2025); "built using 45SPCLO" only in secondary press | 2020-12-02; 2025-03-31 | see `2026-11-07-gf-siph-customers-and-perf.md` Sec. 2 | GF: partner wording |
| Lightmatter | Passage CPO on TSMC COUPE | Lightmatter + GUC release: Passage 3D CPO with GUC; TSMC is GUC's largest shareholder and "sole foundry supplier"; COUPE and PIC fab not stated | 2026-01-26 | https://lightmatter.co/press-release/lightmatter-and-guc-partner-to-produce-co-packaged-optics-cpo-solutions-for-ai-hyperscalers/ (search snippet; businesswire 403) | PR, partner only |
| Lightmatter | same | Trade press: "deepening collaboration with TSMC on a Compact Universal Photonic Engine (COUPE) platform"; CEO: "several co-developed products with TSMC are expected to enter production around 2027"; also works with GF and Tower | 2026-05-26 | https://www.smbom.com/news/47761 (also Business Today Taiwan 2026-01-27, not fetched) | secondary (CEO quoted) |
| Lightmatter | earlier GF flow | "partnering with GlobalFoundries to mass produce Passage"; M1000 "utilizes the GF Fotonix" | 2024-11-18; 2025-03-31 | GF note Sec. 2 | GF: stated |
| AMD | CPO on COUPE | Enosemi acquisition (2025-05-28) release names no foundry; AMD-COUPE link is Tom's Hardware analysis ("Assuming that AMD adopts TSMC's COUPE") | 2025-05-28 | https://www.tomshardware.com/tech-industry/semiconductors/amd-reportedly-establishes-usd280-million-silicon-photonics-hub-in-taiwan-new-r-and-d-center-could-accelerate-companys-co-packaged-optics-roadmap | secondary (speculation) |
| Marvell | CPO on TSMC | Not found. Marvell acquired Celestial AI (announced 2025-12) | - | - | N/A |
| Celestial AI | Photonic Fabric on TSMC | Hot Chips 2025 slides: "TSMC 5/4nm EIC - completed 4 tapeouts"; "Photonics integrated directly into a 2.5D interposer using CoWoS"; EAM modulators; PIC foundry not stated | 2025-08 | https://www.hc2025.hotchips.org/assets/program/conference/day2/76-Hotchips_25_Celestial_AI_v4.pdf | primary slides: EIC on TSMC; PIC fab N/A |
| Cisco (via Luxtera) | SiPh on TSMC | Luxtera release: devices "built utilizing TSMC's ... process technology using a 300mm Silicon-On-Insulator (SOI) wafer optimized for O-band"; companion CMOS in TSMC 7 nm; Cisco acquired Luxtera 2019-02. Current Cisco PIC fab not found; SemiAnalysis (about 2022): "Cisco use TSMC for some of their photonics needs" | 2018-03-13 | https://semiconductor-today.com/news_items/2018/mar/luxtera-tsmc_140318.shtml (reprint; GlobeNewswire 403) | primary PR (2018, Luxtera); current: secondary |
| Cisco | GF | Custom SiPh with GF (2022) | 2022-03-07 | GF note Sec. 2 | GF: partner only |
| Ranovus | TSMC | Odin "based on GF Fotonix"; no TSMC link found | 2022-03-07 | https://ranovus.com/ranovus-and-gf-fotonix-mar7-2022/ | TSMC: N/A |

Summary: stated by the customer for the photonics: NVIDIA (blog, IEDM 2025, OFC 2026 review: MRMs on COUPE) and Broadcom (Davisson COUPE-based optical engines, TSMC quote). Partner-level only: Ayar Labs (primary), Lightmatter (primary via GUC). Trade press only: Ayar COUPE engine (mockup), Lightmatter COUPE collaboration, AMD. Not found: Marvell, Ranovus, Celestial AI PIC, Broadcom earlier generations. The owner's list (NVIDIA, Lightmatter, Ayar) is incomplete (Broadcom is the second stated customer) and over-states Lightmatter and Ayar (both still GF in primary wording).

## 3. Papers

| Title | Venue | Year | DOI | Fab statement (locator) | Open access | In repo | Owner local copy |
|---|---|---|---|---|---|---|---|
| Silicon Photonics Platform for Next Generation Data Communication Technologies (Yeh et al.) | IEDM 2024 | 2024 | 10.1109/IEDM50854.2024.10873369 | TSMC authors; "TSMC's SiPh platform ... 300mm silicon-on-insulator" (p.1 Sec. II.B) | no | no | yes |
| Optical and Electrical Characterization of a Compact Universal Photonic Engine (Chen et al.) | ECTC 2025, pp. 54-58 | 2025 | 10.1109/ECTC51687.2025.00015 | TSMC authors; "TSMC Compact Universal Photonic Engine" (Abstract) | no | registry `pk:ectc51687.2025.00015`, 0 components | yes |
| Adjoint-Optimized Dual-Layer Grating Couplers ... (Shi et al.) | OFC 2026 Tu2J.2 | 2026 | not in registry | TSMC authors; "TSMC's Silicon Photonics platform ... 65nm" (Sec. 2) | no | yes, distilled (current 2 TSMC cells) | OFC corpus |
| A 256 Gb/s DWDM Optical I/O in a 3D-Stacked EIC/PIC SiPh Platform (Mehta et al., NVIDIA) | OFC 2026 M4B.2 | 2026 | not in registry | not named; ref [2] = TSMC IEDM 2024 (Sec. 1) | no | yes, 2 components, fab org empty | OFC corpus |
| A 32Gb/s/lambda 256Gb/s/Fiber ... 3D-Stacked 7nm EIC/65nm PIC (Song et al., NVIDIA) | ISSCC 2026 23.1 | 2026 | 10.1109/ISSCC49663.2026.11409081 | not named ("65nm SiPh process", p.1) | no | registry `eo:song2026` (EO ring row), no components | yes |
| Photonic Interconnect for Next-Generation AI Systems (B. G. Lee, NVIDIA) | IEDM 2025 | 2025 | 10.1109/IEDM50572.2025.11353715 | "NVIDIA's CPO technology [6] based on TSMC's COUPE process" (Fig. 2 caption) | no | no | yes |
| Si Microring Resonator Modulators at >200Gb/s (D. Patel, NVIDIA) | OFC 2026 M2A.7 | 2026 | 10.1364/ofc.2026.m2a.7 | "MRMs fabricated using ... TSMC ... COUPE process" (Sec. 1) | no | registry only | OFC corpus |
| Integrated Optical Interconnect Systems (iOIS) ... (Hsia et al.) | ECTC 2023, pp. 612-616 | 2023 | 10.1109/ECTC51909.2023.00108 | TSMC authors (COUPE2.0, CoWoS CI) | no | registry `pk:` only | packaging atlas text |
| High Bandwidth and Energy Efficient E-O System Integration Using COUPE (Lu et al.) | ECTC 2024, pp. 893-897 | 2024 | 10.1109/ECTC51529.2024.00144 | TSMC authors; simulation only (PD BW, TIA noise) | no | registry `pk:` only | packaging atlas text |
| Broadband Optical Engine System Integration by Wafer Level Process in HPC/AI Era | ECTC 2025, pp. 1672-1675 | 2025 | 10.1109/ECTC51687.2025.00284 | TSMC (repo fab org_tsmc) | no | yes, 6 components (micro-optics, FAU, SiN transitions; no benchmark-row classes) | packaging atlas text |
| Low-loss High-uniformity Silicon Nitride Optical Building Blocks Integrated on Silicon Photonics Platform (Lu et al.) | OFC 2025 Th1G.2 | 2025 | 10.1364/OFC.2025.Th1G.2 | TSMC authors; abstract: SiN straight WGs, bends, tapers, 1x2 MMIs, SiN-Si transitions, edge couplers on TSMC SiPh platform | no (Optica "Not Accessible") | no | no |
| Heterogeneous Integration of a Compact Universal Photonic Engine for Silicon Photonics Applications in HPC (Hsia et al.) | ECTC 2021, pp. 263-268 | 2021 | 10.1109/ECTC32696.2021.00052 | TSMC authors (COUPE concept) | no | no | no |
| TSMC in the Silicon Photonics Era - an electrical perspective (Sahrling, Li, Lee, Rusu) | OFC 2025 Tu3G.1 | 2025 | 10.1364/ofc.2025.tu3g.1 | TSMC authors; electrical (SoIC / TDV) scope per abstract | no | no | no |
| Advanced silicon photonics technology platform leveraging a semiconductor supply chain (De Dobbelaere et al., Luxtera) | IEDM 2017, 34.1 | 2017 | 10.1109/IEDM.2017.8268493 | not verified (Luxtera-TSMC 300 mm platform per 2017-2018 releases; abstract not read) | no | no | no |

## 4. Values per benchmark row (TSMC SiPh column)

Basis per the pic-component-distill rules (D76: a performance value of unstated measured / design origin is `author_estimate`). "Cell" = would pass the benchmark filters (basis measured / extracted_from_figure / derived, scope allowed).

| Row | Best value | Basis | Source | Cell? | Notes |
|---|---|---|---|---|---|
| wg_loss | 0.67 dB/cm (SM Si rib); 0.20 dB/cm (MM rib) | author_estimate | IEDM 2024 p.2 | no | Method not shown; owner ruling needed (OWAT monitors WG loss, so likely measured). SiN 0.21 / 0.14 dB/cm excluded from SiPh wg_loss |
| bend_loss | N/A | - | - | - | Only 0.009 dB/90 deg for the CoWoS interposer routing layer (iOIS, origin not stated, not SiPh) |
| edge_il | 1.2 dB, SiN EC, 1270-1330 nm, PDL 0.18 dB | measured ("demonstrated"), scope unspecified | IEDM 2024 p.2 Sec. III.B | no (scope) | Per facet vs total not stated; OFC 2025 Th1G.2 likely has the full data |
| gc_il | <= 1.2 dB half-loopback, COUPE-GC (through micro-lens + reflector) | measured | ECTC 2025 p.3, Fig. 6 | yes | Current cell 0.98 dB (Tu2J.2 Si SPGC, repo scope per_coupler, isolation not stated). IEDM 2024: SPGC < 1.3 dB, PSGC ~2 dB (scope unspecified). NVIDIA ISSCC envelope: two-coupler peak 3.6-3.9 dB, per coupler <= 1.8-2.0 dB (author_estimate) |
| gc_bw | 62 nm (dual-layer SiN/Si SPGC, in repo) | measured | OFC 2026 Tu2J.2 | yes (current) | Si SPGC: ~20 nm (IEDM 2024, ECTC 2025 derived), COUPE-GC ~25 nm, PSGC ~25 nm |
| mmi_el | N/A measured | - | - | - | Simulated tapered 2x2 MMI ~0.03 dB (IEDM 2024 Fig. 6a) |
| crossing, awg_il, awg_xt | N/A | - | - | - | In the PDK list (IEDM 2024 Fig. 5) without numbers; no TSMC AWG found |
| to_ppi | N/A | - | - | - | ISSCC 2026 gives heater energy (0.76 pJ/b bench; 0.49 pJ/b estimate) but no P_pi or tuning efficiency |
| pd_resp | ~1.0 A/W (WG-referred, up to 5 mW) | measured | IEDM 2024 p.2, Fig. 8a | yes | Fig. 8a reads 1.00-1.04 A/W; bias / wavelength not stated |
| pd_bw | ~110 GHz (-1.75 V, 200 uA); > 50 GHz at 1 mA | measured | IEDM 2024 p.2, Fig. 8c | yes | -3 dB point at the edge of the 110 GHz sweep |
| pd_dark | 4.5 nA median at -1.5 V (wafer) | measured | IEDM 2024 p.2, Fig. 8b | yes | all < 20 nA from -1 to -2.5 V |
| mzm_vpil, mzm_bw | N/A | - | - | - | No TSMC MZM data found (PDK lists phase shifter, VOA) |
| ring_mod_bw | 76 GHz at 4 dB IL (63 GHz at 6 dB IL) | measured | IEDM 2024 p.2, Fig. 7b | yes (EO-atlas row source: needs an EO atlas entry) | low laser power |
| eam_bw | N/A | - | - | - | none |

Ring-modulator extras (not benchmark rows): VpiL 0.35 V.cm printed on the measured spectra (5 um radius efficiency design, IEDM 2024 Fig. 7a); 42-46 pm/V read from the same figure (0 to -3.5 V); loaded Q about 3350-3730 read from the 0 V dip width; ISSCC 2026 TX MRM Q ~4.5K and RX filter Q 4K ("validated by device test chip measurements"); dip ER 18.5-21.5 dB (Fig. 7a). Uniformity: SPGC peak 3 sigma 1.32 nm, MRR dip 3 sigma 1.44 nm within wafer (IEDM 2024 Table 1); COUPE GC center within +/-1.7 nm across the wafer; DMRR 1 sigma 0.7 nm.

Second-order derivation (NVIDIA ISSCC 2026, Fig. 23.1.5 top left, TX bus frequency sweep): off-resonance envelope peaks at about -3.6 dB (reading +/-0.3 dB at 600 dpi, 13.2 px/dB) near 1305-1315 nm. If the sweep is un-normalized fiber-in to fiber-out through two identical GC interfaces (GC + lens carrier + FAU, Fig. 23.1.7), one interface is at most 1.8-2.0 dB, the remainder being bus waveguide and nine off-resonance rings. Normalization and path are not stated, so the per-coupler value is `author_estimate`; the envelope reading itself is `extracted_from_figure`. The 1 dB width was not read (ring dips cut the envelope). The result is consistent with the 1.3 dB per GC printed in OFC 2026 M4B.2.

Conflicts:
- COUPE coupler loss: 0.3 dB "FAU coupling loss" (iOIS ECTC 2023 and IEDM 2024 p.1, no data) vs <= 1.2 dB half-loopback measured (ECTC 2025). Probably different quantities (lens-path excess vs total GC), not stated.
- MRR filter Q: 4200 (OFC 2026 M4B.2) vs 4K (ISSCC 2026), same link.
- Tu2J.2 (in repo) quotes the IEDM 2024 SPGC as "better than -1.2 dB at 1311 nm, 3-sigma ... less than 0.1 dB and 1.5 nm [2]": cited, not entered (rule 3). IEDM 2024 Table 1 gives an SPGC peak-wavelength 3 sigma of 1.32 nm (consistent with < 1.5 nm); a 0.1 dB loss 3 sigma is not in the IEDM 2024 text.

## 5. Ingest list (priority order)

| # | Source | Why | Action |
|---|---|---|---|
| 1 | IEDM 2024 Yeh et al., 10.1109/IEDM50854.2024.10873369 | Fills pd_resp, pd_bw, pd_dark, ring_mod_bw, gc_bw; WG / EC values pending basis ruling | register (owner local copy, text extract exists), distill |
| 2 | ECTC 2025 Chen et al., 10.1109/ECTC51687.2025.00015 | Only TSMC gc_il with an allowed scope (loopback_half); uniformity, reliability | already registered (`pk:`), distill |
| 3 | ISSCC 2026 Song et al., 10.1109/ISSCC49663.2026.11409081 | Envelope-derived GC bound, MRM / MRR Q; fab only by citation | already registered (`eo:song2026`), distill components; set fab via D-ruling on citation-based attribution |
| 4 | OFC 2025 Th1G.2 Lu et al., 10.1364/OFC.2025.Th1G.2 | TSMC SiN bends, MMI, edge couplers, Si-SiN transitions (edge_il, mmi_el, bend_loss candidates) | obtain PDF (paywalled; owner download), register, distill |
| 5 | NVIDIA IEDM 2025 Lee, 10.1109/IEDM50572.2025.11353715 | Fab statement for NVIDIA CPO = TSMC COUPE (supply / customer evidence; no device data) | register (owner local copy) |
| 6 | OFC 2026 M4B.2 (in repo) | fab_org_ids empty; attribution to TSMC only via ref [2] | coordinator ruling: set org_tsmc with note or leave empty |
| 7 | ECTC 2021 Hsia, 10.1109/ECTC32696.2021.00052; OFC 2025 Tu3G.1, 10.1364/ofc.2025.tu3g.1; IEDM 2017 Luxtera, 10.1109/IEDM.2017.8268493 | possible COUPE coupler data / Luxtera-TSMC device library | obtain and screen; low expected yield |

Owner decisions needed: (a) basis of IEDM 2024 text-only values (WG loss 0.67 / 0.20 dB/cm, SiN EC 1.2 dB): author_estimate per D76 or measured; (b) whether an NVIDIA paper that cites the TSMC platform paper counts as TSMC fab; (c) whether press-release device claims (Luxtera 2018: GC < 1 dB, Ge PD > 1 A/W and > 45 GHz) may enter as a marked overlay like D910.
