# Tower Semiconductor silicon photonics: platform, customers, literature performance (2026-11-07)

Purpose: evidence base for a Tower column in the foundry PDK benchmark (DevLog-014). Companion data:
`DevLog/research/2026-11-07-tower-siph-values.csv` (50 rows, 40 with values; one row per value, schema as requested).

Method and limits:
- Platform and customer facts come from Tower press releases on towersemi.com, Tower's FY2025 20-F, and partner or trade
  articles. Each fact has a URL.
- Papers: three parallel literature streams (passive, active, heterogeneous) plus the owner's local OFC 2026 full-text
  corpus (`PlayGround/20260320_OFC/extracted_text`, 1354 files, grepped for Tower / TowerJazz / PH18 / PH45).
- Constraints hit:
  - The turn's WebSearch budget (200 calls) ran out.
  - opg.optica.org returned a bot challenge; ieeexplore returned 418; MDPI, science.org and CORE returned 403;
    Semantic Scholar and Crossref returned 429. Each was stopped at the first signal.
  - Most IEEE and Optica papers were therefore read at abstract level only (`read_full_text=false`, no locator).
- Strict rule: a paper counts as Tower-fabricated only when its own text says so. Attribution by press release or
  author affiliation is marked as such in `tower_process`.

## 1. Platform summary

| Item | Fact | Date | Source |
|---|---|---|---|
| PH18 family | 200 mm, 0.18 um generation SiPh. The FY2025 20-F lists PH18 (200 mm) and PH45 (300 mm) in high-volume production, the leading SiPho platforms for 400G-1.6T. | 20-F filed 2026-04-30 | https://www.sec.gov/Archives/edgar/data/928876/000117891326002318/zk2635149.htm (Item 4.B) |
| SiPh fabs | Item 4.A / 4.D: Fab 2 (Migdal HaEmek, 0.18 / 0.13 um), Fab 3 (Newport Beach, "specializes in silicon photonics"), Fab 9 (San Antonio). $920M capex plan "primarily to expand our SiPho and SiGe capacity at Fabs 2, 3, 7 and 9" (Item 5; Fab 7 = Uozu, 300 mm) | 2026-04-30 | same 20-F |
| PH18M | Base platform: low-loss waveguides, photodetectors, modulators on one chip | 2023-03-02 | https://towersemi.com/2023/03/02/03022023/ |
| PH18MA | Si-only platform, "in high-volume production" | 2023-03-02 | same |
| PH18DA | Heterogeneous III-V platform. Lasers, SOA, EAM and PD co-integrated (Juniper, 2021); InP-on-Si (2026). PDK expected end 2021, first MPW early 2022, 400G / 800G reference-design samples Q2 2022. "Prototyping" 2023-03; first volume orders (NewPhotonics) 2026-03-20; high-volume shipments 2026-09-17 | 2021-12-21; 2026-08-11 | https://towersemi.com/2021/12/21/12212021/ ; https://towersemi.com/2026/08/11/08112026/ ; https://www.semiconductor-today.com/news_items/2026/mar/openlight-tower-200326.shtml |
| PH18DB | GaAs quantum-dot lasers + SOA on PH18M, 220 nm SOI (Quintessent; DARPA LUMOS). Initial PDKs; MPWs planned 2023-2024 | 2021-09-02; 2023-03-02 | https://towersemi.com/2021/09/02/09022021/ ; https://towersemi.com/2023/03/02/03022023/ |
| ULL SiN process (with Anello) | Loss "approaches 0.005dB/cm" at 1550 nm, bend radius < 1 mm, Q "surpassing 100 million", delay lines > 10 m. Foundry version offered from Q1 2022 (claims; not paper values) | 2021-11-01 | https://towersemi.com/2021/11/01/11012021/ |
| 300 mm SiPh | Standard foundry offering; "complements" 200 mm PH18. Si and "low-loss silicon nitride waveguides"; trade press adds Ge PIN and APD, heaters, 180 nm Al BEOL. Name PH45 per 20-F | 2024-11-26 | https://towersemi.com/2024/11/26/11262024/ ; https://www.eenewseurope.com/en/tower-ports-silicon-photonics-to-300mm-wafers (secondary) |
| TPS45PH | Named in the Salience release as the platform with "low loss nitride waveguides". Relation to PH45: N/A (not stated) | 2026-02-25 | https://towersemi.com/2026/02/25/02252026/ |
| 300 mm expansion | Fab 7 Uozu plus adjacent land: target 4x current Uozu 300 mm capacity, citing "optical and photonics platforms". No dates or amounts | 2026-03-25 | https://towersemi.com/2026/03/25/03252026_300mm/ |
| Technology page | 200 / 300 mm. O and C band. Si and SiN waveguides; Ge PIN and APD; PIN phase shifters and MZMs; heaters; Al or Cu BEOL; UBM for laser attach; on-chip or integrated laser options; 3D-IC hybrid wafer bonding; in-line wafer-level optical test; MPW and short-loop runs. PDK partners: Ansys, Cadence, GDSFactory, LDS, Luceda, Siemens, Synopsys. No numeric specs | accessed 2026-11-07 | https://towersemi.com/technology/rf-and-hpa/silicon-photonics-rf/ |
| 1.6T platform | "Latest SiPho platform" in volume production: 200 Gb/s per lane, 8 lanes; "high bandwidth optical modulators and low-loss edge coupling" | 2024-11-19 | https://towersemi.com/2024/11/19/11192024/ |
| 400G/lane | PH18DA heterogeneous modulator: PAM4, ER > 3.5 dB, 0.6 Vpp (2025-03-12). Native Si MZM with Coherent: 420 Gb/s PAM4 (2026-03-23) | 2025-03-12; 2026-03-23 | https://towersemi.com/2025/03/12/03122025/ ; https://towersemi.com/2026/03/23/03232026/ |
| CPO | 300 mm wafer bonding (from stacked BSI sensors) for PIC on EIC (SiGe) stacking; Cadence reference flow | 2025-11-12 | https://towersemi.com/2025/11/12/11122025/ |
| Business | $1.3B SiPho contracts for 2027 revenue; $290M capacity prepayments. Roadmap: TFLN, InP, organic, MRM, Si EAM and uLED modulators in development; "400GHz/lane" (sic) modulator and detector performance claimed | 2026-05-13 | https://towersemi.com/2026/05/13/05132026_1/ |
| PDK / EDA | Synopsys end-to-end flow incl. 800G-DR8 case study with integrated laser (2022-06-08); OpenLight PH18DA PDK in Cadence (2026-08-11) | 2022-06-08 | https://towersemi.com/2022/06/08/06082022/ |

No Tower source gives a numeric PDK device spec: loss, PD bandwidth or responsivity, VpiL, coupler IL. The only
platform number is the Anello SiN loss claim.

## 2. Customers and partners

"Stated" means the source states that Tower manufactures the product, or that the product uses a Tower platform.

| # | Company / group | What they build on Tower | Date | Tower fab | Source |
|---|---|---|---|---|---|
| 1 | Inphi (now Marvell) | SiPh PICs for 100G PAM4 DWDM QSFP28 DCI; qualified Tower PH18 "for production" | 2019-12-03 (dateline) | stated | https://towersemi.com/2019/12/04/04122019/ |
| 2 | Alpine Optoelectronics | 400G PAM4 nCP4 optical engine (400G DR4), PH18 | 2020-12-29 | stated | https://towersemi.com/2020/12/29/12292021/ |
| 3 | USC (SungWon Chung) | 1550 nm FMCW OPA LiDAR IC, PH18 (ISSCC 2021) | 2021-09-13 | stated | https://towersemi.com/2021/09/13/09132021/ |
| 4 | Quintessent | QD lasers / SOAs: PH18DB platform co-development | 2021-09-02; 2023-03-02 | stated (platform partner) | https://towersemi.com/2021/09/02/09022021/ |
| 5 | Anello Photonics | ULL SiN process for the SiPhOG optical gyroscope | 2021-11-01 | process stated; product manufacture at Tower implied, not explicit | https://towersemi.com/2021/11/01/11012021/ |
| 6 | Juniper Networks | Heterogeneous III-V platform co-development and qualification (became OpenLight / PH18DA) | 2021-12-21 | stated (development partner) | https://towersemi.com/2021/12/21/12212021/ |
| 7 | OpenLight | PH18DA PDK / IP owner; 400G/lane modulator demo; Cadence PDK | 2022-06-08; 2025-03-12; 2026-08-11 | stated | https://towersemi.com/2025/03/12/03122025/ |
| 8 | Teramount | PhotonicPlug fiber attach on PH18 "Bump-ready" wafers | 2023-03-06 | stated (packaging partner) | https://towersemi.com/2023/03/06/03062023/ |
| 9 | InnoLight | 400G (mass production 2023) and 800G (volume Q4 2023) on PH18M. First NPO device in early production on PH18M at the Tower CA fab; multiple NPO tape-outs on Tower 300 mm | 2023-09-07; 2025-03-10; 2026-11-03 | stated | https://towersemi.com/2023/09/07/09072323/ ; https://towersemi.com/2026/11/03/11032026/ |
| 10 | Coherent | SiPh transceivers on PH18 (supplier award, 2024-03-18). Quoted in the 1.6T production release. 400G/lane Si MZM (OFC 2026 Th4A.4 per PR) | 2024-03-18; 2024-11-19; 2026-03-23 | stated | https://towersemi.com/2024/03/18/03182024/ ; https://towersemi.com/2026/03/23/03232026/ |
| 11 | Alcyon Photonics | Silicon-validated building blocks for Tower SiPho (O-band CWDM, C+L coherent) | 2025-03-25 | stated (design IP partner) | https://towersemi.com/2025/03/25/03252025/ |
| 12 | Xscape Photonics | ChromX optically pumped multi-wavelength laser on PH18; prototyping / validation kits | 2025-08-25 | stated | https://towersemi.com/2025/08/25/08252025/ |
| 13 | LightIC Technologies | FMCW LiDAR PICs (Lark, FR60); "LightIC designs, Tower manufactures" | 2026-01-05 | stated | https://towersemi.com/2026/01/05/01052026/ |
| 14 | NVIDIA | 1.6T modules "designed for NVIDIA networking protocols" using Tower SiPho. NVIDIA's role is ecosystem collaboration, not stated as a wafer customer | 2026-02-05 | stated for platform; NVIDIA role ambiguous | https://towersemi.com/2026/02/05/02052026/ |
| 15 | Scintil Photonics | SHIP heterogeneous DWDM lasers (LEAF Light) "validated on Tower's silicon photonics platform" | 2026-02-17 | stated | https://towersemi.com/2026/02/17/02172026/ |
| 16 | Xanadu | Photonic quantum hardware; co-engineered stack; ULL SiN and integrated PDs | 2026-02-19 | stated | https://towersemi.com/2026/02/19/02192026/ |
| 17 | Salience Labs | Optical circuit switches on PH18DA and TPS45PH; pre-production | 2026-02-25 | stated | https://towersemi.com/2026/02/25/02252026/ |
| 18 | Oriole Networks | Nanosecond optical circuit switching (PRISM) on Tower SiPho | 2026-03-16 | stated | https://towersemi.com/2026/03/16/03162026/ |
| 19 | Marvell | Over 5 million coherent PICs shipped; product line not named | 2026-06-18 | stated | https://towersemi.com/2026/06/18/06182026/ |
| 20 | NewPhotonics | Laser-integrated optical-engine PICs on PH18DA (NPG102, 800G / 1.6T, 200G/lane) in high-volume shipment; NPC505 6.4T planned 1H27 | 2026-03-20; 2026-09-17 | stated | https://towersemi.com/2026/09/17/09172026/ ; semiconductor-today URL in Sec. 1 |
| 21 | IQE (supplier) | Multi-year InP epiwafer supply for Tower SiPh platforms | 2026-06-15 | supplier, not a customer | https://towersemi.com/2026/06/15/06152026/ |
| 22 | Columbia University (Bergman, Lipson, Gaeta) | 4-tap MZI Fourier synthesizer, "fabricated through TowerJazz foundry", commercial 300 mm platform | 2026-03 (OFC 2026 M1E.4) | stated (paper) | local OFC corpus; repo source ofc2026:M1E.4 |
| 23 | UCSB (Bowers) with Anello / Caltech | 3D-integrated SIL lasers on Tower 200 mm ULL SiN | 2023 (Nature 620) | stated (paper) | doi:10.1038/s41586-023-06251-w |
| 24 | Hebrew University (Levy group) | TowerJazz 220 nm SOI rings (flash trimming, NDR optical SRAM) | 2017; 2023 | stated (paper) | arXiv 1705.08290; doi:10.1126/sciadv.adf5589 |
| 25 | UC3M Madrid (Carpintero group) | PBS on PH18MA | 2023 | stated (abstract) | doi:10.1117/12.2649958 |
| 26 | Authors of Munk et al. 2019 | 8-ch 17 GHz ARMA DWDM, Tower-Jazz SOI | 2019 | stated (paper) | doi:10.1109/jstqe.2019.2904437 (in repo) |

Not verified: NLM Photonics SOH modulators on a PH18M MPW (the active stream saw a 2026-03-16 release; no URL fetched).
The Semtech 2024-12-10 and 2026-10-13 releases concern SiGe, not SiPh.

## 3. Papers (26 retained, by strength of Tower evidence)

`in_repo`: checked by DOI / arXiv / venue paper number against `data/registry/sources.csv` and
`data/components/components.csv` on 2026-11-07.

| Paper | Venue / ID | Tower evidence | Access | Full text | Values | in_repo |
|---|---|---|---|---|---|---|
| Xiang et al., 3D integration enables ultralow-noise isolator-free lasers | Nature 620, 2023, 10.1038/s41586-023-06251-w | Methods: SiN "performed at Tower Semiconductor", 200 mm, 100 nm LPCVD | OA (PMC10396957) | yes | 7 | absent |
| Wang et al., Programmable MZI Fourier synthesizer | OFC 2026 M1E.4 | Sec. 1 commercial 300 mm platform; Sec. 3 "fabricated through TowerJazz foundry" | owner corpus | yes | 1 | source only (ofc2026:M1E.4), no components |
| Munk et al., 8-ch 17 GHz DWDM | JSTQE 2019, 10.1109/jstqe.2019.2904437 | p.4 Sec. III-A Tower-Jazz | in repo | yes | 3 (copied from repo) | present, fab_org_ids empty |
| Adaptive facet-attached microlenses | OFC 2026 W4B.1 | Sec. 2 "fabricated by Tower Semiconductor" | in repo | yes | 1 (from repo) | present (org_tower_semiconductor) |
| Gherabli et al., electro-optical SRAM cavity (NDR) | Sci. Adv. 9, 2023, 10.1126/sciadv.adf5589 | Methods "fabricated by TowerJazz", 220 nm SOI | OA (PMC10096569) | yes (main text) | 4 (non-registry params) | absent |
| Grajower et al., flash-memory post-trimming of microresonators | arXiv 1705.08290 (2017) | p.4 "Towerjazz semiconductor Ltd." | OA | yes | 1 (non-registry) | absent |
| Spanidou et al., cascaded-DC PBS | SPIE 2023, 10.1117/12.2649958 | abstract: PH18MA | UC3M repository 403 | no | 0 | absent |
| Shi et al., DFB lasers in open-market SiPh platform | ISLC 2024, 10.1109/ISLC57752.2024.10717410 | abstract: "PH18DA at Tower Semiconductor" | closed | no | 0 | absent |
| Ge PIN photodiode for high-volume SiPh | GFP 2018, 10.1109/group4.2018.8478742 | all authors TowerJazz (affiliation) | closed | no | 3 (abstract) | absent (in lit candidate pool) |
| Considerations for SiPh process technologies in a commercial foundry | OFC 2022 Th3C.5, 10.1364/ofc.2022.th3c.5 | all authors Tower | closed | no | 0 | absent |
| Poly-Si waveguides on deep-trench isolation, 180 nm SiGe BiCMOS | OFC 2018 Th2A.2, 10.1364/ofc.2018.th2a.2 | TowerJazz co-author; commercial BiCMOS (not PH18) | closed | no | 2 (abstract) | absent |
| Zero-process-change SiGe HJ APD | IEEE EDL 2021, 10.1109/led.2021.3102001 | Tower co-author; commercial SiGe BiCMOS | closed | no | 4 (abstract) | absent |
| 16-ch WDM transceiver with interleavers | CLEO 2022 STh4K.3 | Tower co-author only | closed | no | 1 (56 Gb/s) | absent |
| SDM SiPh interconnects with MCF | CLEO 2022 STh4N.3 | Tower co-author only | closed | no | 0 | absent |
| Coherent: 400G/lane PAM4 with Si MZMs | OFC 2026 Th4A.4 | paper names no foundry; Tower PR 2026-03-23 | owner corpus | yes | 3 | present (ofc2026:Th4A.4; EO atlas dong2026-a) |
| Chung, Nakai, Hashemi, low-power TO Si modulator | Opt. Express 27, 13430 (2019) | "commercial foundry"; USC lab page says Tower Jazz | OA journal, Optica bot-blocked | no | 2 (abstract) | absent |
| Optical phased-array FMCW LiDAR with on-chip calibration | ISSCC 2021, 10.1109/ISSCC42613.2021.9366004 | Tower PR 2021-09-13 | closed | no | 0 | absent |
| Norberg et al., heterogeneous Si-III-V laser sources in open-access PDK | JLT 43(13) 2025, 10.1109/JLT.2025.3554392 | "open access Si-Ge BiCMOS foundry"; PH18DA per press | closed | no | 3 (abstract) | absent |
| Norberg et al., open-access heterogeneous laser sources | ECOC 2024 | same as JLT (precursor) | closed | no | 2 (duplicate) | absent |
| Piels et al., 800G transmitter PIC with integrated lasers | OFC 2023 W3D.3 | "open market platform" | closed | no | 0 | absent |
| SiPh platform with heterogeneous lasers and EAMs for 1.6/3.2T | OFC 2025 M3K.3 | per press | closed | no | 1 (abstract) | absent |
| Ostrovskis et al., heterogeneous InP EAM beyond 300 Gb/s | JLT 2025, 10.1109/JLT.2025.3526822 | OpenLight co-authors; per press | closed | no | 1 (abstract) | absent |
| Ostrovskis et al., heterogeneous InP EAM beyond 200 Gb/s per lambda | OFC 2024 Th4C.8 | per press | closed | no | 1 (abstract) | absent |
| Heterogeneous SiPh in open-access PDK | ACP 2025, 10.1109/ACP66871.2025.11350694 | per press | closed | no | 0 | absent |
| 53 Gb/s link with heterogeneous transmitter | IEEE SiPhotonics 2024, 10.1109/SiPhotonics60897.2024.10543620 | per press | closed | no | 0 | absent |
| Multi-wavelength QD comb lasers (Quintessent) | OFC 2025 W1G.3 | PH18DB per PR; video only, no written paper | none | no | 0 | absent |

Repo collisions checked: the repo rows ofc2026:Th3C.5, W3D.3, M3K.3, Th4C.8 and W1G.3 are different OFC 2026 papers with
the same paper numbers.

Likely-Tower papers rejected because their text does not name the foundry:
- Jin et al., Nat. Photonics 2021 (`lit:jin2021`, in repo): 0.001 dB/cm, Q_i > 260 M, "high-volume CMOS foundry". It
  is the ULL SiN that Xiang 2023 attributes to Tower, but the attribution cannot be made under the rule.
- Guo et al., arXiv 2406.09533.
- Xiang et al., Nat. Commun. 2021.
- Li et al., Nature 2025.
- arXiv 2507.17287: 8-inch deuterated SiN with AMF / SUTD authors, no Tower.

Full reject lists are in the stream notes. Those notes are in the scratchpad and will not be kept.

## 4. Best value per benchmark row (Tower)

Filter column: "D901 pass" means the value would pass the DevLog-014 cell filter, given basis, scope and Tower fab
attribution in the paper text.

| Benchmark row | Best Tower value found | Paper | Basis / access | D901 pass |
|---|---|---|---|---|
| wg_loss, Si | 1.8 dB/cm (220 nm rib, TE, C band, scope unspecified) | Munk 2019 | measured, full text, in repo | would pass if `fab_org_ids` set; currently empty, so no Tower cell |
| wg_loss, SiN | ~0.005 dB/cm (0.5 dB/m, from fitted Q) | Xiang 2023 | author_estimate (Q-derived) | no (author_estimate excluded) |
| ring_qi, SiN | ~50 M | Xiang 2023 | author_estimate (D403) | no |
| bend_loss | N/A | none | none | none |
| edge_il | N/A. Nearest: 0.82 dB loopback-half for lens pair + Tower SiN edge coupler (W4B.1, micro_optics class); 3 dB "fibre-chip coupling" (Xiang 2023, coupler type and method not stated) | none | none | no |
| gc_il | 10 dB per coupler (TE, C band) | Munk 2019 | measured, in repo | would pass with fab org; weak value |
| gc_bw (1 dB) | N/A | none | none | none |
| mmi_el | N/A for PH18. 0.38 dB poly-Si MMI in 180 nm SiGe BiCMOS | OFC 2018 Th2A.2 | abstract only | no |
| crossing | N/A | none | none | none |
| awg_il / awg_xt | N/A. Munk 2019 ARMA filter: 22 dB worst-case crosstalk, not an AWG | none | none | none |
| to_ppi | 8.8 mW (folded waveguide, trenches, reference MZI, C band) | OFC 2026 M1E.4 | measured, full text | yes, once distilled |
| to_ppi (unconfirmed) | 2.56 mW per 180 deg | Opt. Express 2019 (USC) | abstract; Tower not in text | no |
| pd_resp | 0.9 A/W | GFP 2018 (Tower authors) | abstract; no wavelength or bias | no |
| pd_bw | 67 GHz ("optical bandwidth"; 3 dB not stated) | GFP 2018 | abstract | no |
| pd_dark | 90 mA/cm2 at -1 V (density; no area, so no nA value) | GFP 2018 | abstract | no |
| mzm_vpil | N/A. Th4A.4 gives only "effective Vpi ~7 V" (VpiL / length; neither printed) | none | none | none |
| mzm_bw | > 70 GHz (Si TW MZM, Al electrodes) | OFC 2026 Th4A.4 (Coherent) | measured, full text; Tower only per PR | no (fab not in paper) |
| ring_mod_bw | N/A (56 Gb/s data rate only) | CLEO 2022 STh4K.3 | abstract | no |
| eam_bw | N/A (340 Gb/s PAM4 / 256 GBd OOK on heterogeneous InP EAM) | JLT 2025 / OFC 2024 (OpenLight) | abstract; per press | no |
| hetero laser threshold / power | N/A for PH18DA / DB. > 40 mW "total" DFB (plane not stated) | JLT 2025 Norberg | abstract | no |

Other values recorded:
- Xiang 2023 on the Tower SiN wafer:
  - Inter-layer SiN transition < 0.03 dB per transition (derived; measured on a separate test wafer).
  - Ring heater ~0.5 W per 30 GHz FSR.
  - Heterogeneous DFB threshold ~74 mA and SIL fundamental linewidth ~5 Hz. These are UCSB III-V processing on a Tower
    SiN wafer, not a Tower heterogeneous process.
- SiGe HJ APD: gain > 16,000; 4.2 A/W at 1066 nm (abstract).
- OpenLight tunable laser: 8 kHz fundamental linewidth (abstract).

## 5. Gaps

- No open full text found with Tower-stated PH18 values for: Si strip loss, bend loss, edge coupler (the platform
  headline feature), grating 1 dB BW, MMI, crossing, AWG, Ge PD (in nA / GHz with bias), MZM VpiL, ring modulator BW,
  or PH18DA / PH18DB laser threshold and WPE.
- Tower publishes no numeric PDK specs on its public pages. `data/supply/product_specs.csv` would need Tower PDK
  documents, which are not public.
- Most Tower-relevant papers are OpenLight / Tower IEEE or Optica proceedings. Full text needs the owner's licensed
  access. The agent hit bot walls and did not attempt to bypass them.
- Repo data fix to consider (not a new ingest): `lit:munk2019` components say "Fabricated by the commercial silicon
  foundry Tower-Jazz" (p.4 Sec. III-A) but `fab_org_ids` is empty. `org_tower_semiconductor` now exists
  (ofc2026 batch_6). Setting it would give the benchmark a Tower SiPh column seed (Si loss 1.8 dB/cm, GC 10 dB).
- Ambiguous attributions to leave out of a Tower cell unless the paper text is found: Jin 2021 ULL SiN; OE 2019 TO
  P_pi; Th4A.4 MZM.

## 6. Prioritized ingest list

| Rank | Paper | Why | Access |
|---|---|---|---|
| 1 | OFC 2026 M1E.4 (Columbia, TowerJazz 300 mm) | only full-text Tower-stated to_ppi (8.8 mW) | owner corpus; source row exists, distill only |
| 2 | Xiang et al., Nature 2023 | Tower SiN loss / Q / transition; values are author_estimate or derived, so they serve as showcase rows rather than benchmark cells | OA, PMC10396957 |
| 3 | GFP 2018 Ge PIN PD (all TowerJazz authors) | only Tower Ge PD data (0.9 A/W, 67 GHz) | closed IEEE |
| 4 | OFC 2022 Th3C.5 (all Tower authors) | likely PH18 process / device numbers | closed Optica |
| 5 | ISLC 2024 Shi et al. (PH18DA DFB, names Tower) | PH18DA laser threshold / power / SMSR | closed IEEE |
| 6 | JLT 2025 Norberg et al., 10.1109/JLT.2025.3554392 | PH18DA DFB > 40 mW, tunable 8 kHz; check whether the body names Tower | closed IEEE |
| 7 | JLT 2025 Ostrovskis et al., 10.1109/JLT.2025.3526822 | heterogeneous EAM EO bandwidth, IL | closed IEEE; RTU ORTUS record (OA copy not confirmed) |
| 8 | Opt. Express 2019 Chung et al., 10.1364/OE.27.013430 | 2.56 mW TO P_pi; confirm Tower in text | gold OA (Optics Express); blocked for the agent only |
| 9 | ISSCC 2021 19.1 USC OPA LiDAR, 10.1109/ISSCC42613.2021.9366004 | PH18 per Tower PR; modulator / PS / SiN data | closed IEEE |
| 10 | SPIE 2023 Spanidou et al., PH18MA PBS | names PH18MA; PBS IL / extinction | UC3M accepted manuscript (hdl 10016/37005), 403 for the agent |
| 11 | OFC 2023 W3D.3 Piels et al., 800G DR8 with integrated lasers | PH18DA laser / EAM in a product-like PIC | closed |
| 12 | CLEO 2022 STh4K.3 | ring modulator on (probably) Tower | closed |
| 13 | IEEE EDL 2021 SiGe HJ APD | APD gain / GBP | closed |
| 14 | Opt. Express 2015 Abediasl and Hashemi, 10.1364/OE.23.006509 | possible early USC Tower OPA (foundry unconfirmed) | gold OA |
| 15 | Sci. Adv. 2023 Gherabli et al. | full text read; Tower-stated but only non-registry ring values | OA |

Lower priority: Grajower arXiv 2017 (OA; trimming only); OFC 2024 Th4C.8, OFC 2025 M3K.3, ACP 2025, SiPhotonics 2024
(OpenLight; closed); ECOC 2024 (duplicate of JLT 2025).
