# Photonics supply-chain and vendor atlas: taxonomy, tracked specs, seed list

- Date: 2026-10-20. Status: exploration only, nothing ingested into any atlas table.
- Scope: optical interconnects and PICs in general (wafers, foundries, lasers, fiber/connectors, packaging materials and tools, fab tools, test, reliability).
- Corpora scanned (read-only):

| tag | corpus | n docs | access |
|---|---|---|---|
| `eo:` | `eo-modulator-atlas/references/<paper_id>/text.md` | 231 | per `data/papers.csv` access/license (arXiv, OA, some publisher-copyright) |
| `pk:` | `advanced-packaging-atlas/references/<id>/text.md` + `data/{components,process_steps,metrics}.csv` | 296 | mostly IEEE (ECTC/TCPMT/EPTC/ESTC), i.e. paywalled; `001c.*` = IMAPS (access to verify) |
| `ofc2026:` | `PlayGround/20260320_OFC/extracted_text/<code>-*.md` (the 126 `ofc_browser` texts are same-named duplicates) | 677 | `paywalled_conference`: facts/locators only |
| `blog:` | `jwt625.github.io/assets/doc/2025/*.pdf`, text extracted to scratch | 15 PDFs (Soitec URD grepped separately) | OIF IAs, vendor/institute PDFs, papers |

## 0. Method and caveats

- Pass 1: regex dictionary of ~330 vendor names (`vendors.py`, scratch) over all corpora, reference sections cut. Pass 2: usage filter = sentence contains the vendor plus a usage verb (used, measured, generated, fabricated, bonded, cured, purchased, by, with, ...) and no citation/affiliation markers. Pass 3: model-number registry (~120 regexes, e.g. `M8199[AB]`, `TSL-5[57]0`, `XPDV\d{4}R`) with vendor attribution checked against snippets. Pass 4: deep read of methods/packaging/test sections of: berman2026, sun2026a, multani2025, didier2026, chen2024, tiberi2025, valdez2023a, mao2024, bankwitz2026, aihara2026, saxena2023/johnson2025 (foundry), pk:ectc51687.2025.00012 (EMIB CPO FAU), pk:ectc51906.2022.00072 (GR-468 V-groove), pk:ectc51846.2026.00176 (ficonTEC/3D photonic pkg), pk:eptc59621.2023.10457729, pk:tcpmt.2025.3533388, ofc2026:{W1B.3, W3E.1, Tu2D.3, Th1D.3, Th3C.2, Tu2D.2, W2A.10}, blog: OIF ELSFP IA, OIF CPO FD, FBH adhesive qualification, FBH ECDL-MOPA module, Intel detachable glass connector, HHI InP foundry flyer, Corning SMF-28 Ultra, Intel/NVIDIA/Ranovus decks, MediaTek CPO review.
- Locators: `eo:<id>:pN` / `pk:<id>:pN` = `<!-- page N -->` PDF page in text.md. `ofc2026:<code>:pN` = page of nearest preceding figure marker (`_page_k_` + 1) in the marker-pdf text, approximate lower bound; `pNA` = before the first figure marker (usually p1). `blog:<stem>:pN` = PDF page.
- Counts in Section 3 = distinct documents with a usage-context sentence (eo/pk/ofc/blog). They are heuristic: a few author affiliations survive the filter (TSMC, Intel, imec, NVIDIA in pk/ofc), and some EO papers are also in the OFC corpus (e.g. eo:aihara2026 = ofc2026:Th4A.1), so cross-corpus totals can double count. Raw regex counts were larger and noisy (e.g. "MPI" = multipath interference, "SRS" = stimulated Raman scattering, "Okamoto" = author name); those were removed.
- Industry papers anonymize materials: "multiple adhesives ... mechanical adhesive(s) ... optical adhesive(s)", FAUs "from different suppliers" (pk:ectc51687.2025.00012:p2); "a set of three complimentary adhesives" unnamed (pk:ectc51906.2022.00072:p5); "Adhesive 1-4" (blog:Micro-integrated_optical_systems...:p4). This is the main structural gap (Section 5).

## 1. Category tree (revised from evidence)

Codes are proposed `category_id`s.

- **A. Platform materials and substrates**
  - A1 SOI wafers (220 nm / 2 um BOX, float-zone, Photonics-SOI): Soitec, Shin-Etsu
  - A2 Thin-film ferroelectric on insulator: A2.1 LNOI (x/z-cut, MgO-doped), A2.2 LTOI, A2.3 LN-on-sapphire, A2.4 BTO-on-insulator / BTO-on-SOI / BTO on SiN
  - A3 III-V substrates and epi (InP, GaAs; MBE/MOCVD epi services)
  - A4 EO organics and LC: OEO chromophores (JRD1, Selerion-HTX, Perkinamine, SEO100C), ferroelectric nematic LC
  - A5 2D materials (CVD graphene, hBN)
  - A6 single-crystal oxide substrates (GdScO3, LSAT, SrTiO3)
  - A7 glass substrates / glass cores / glass waveguide wafers (alkali-free, ion-exchange glass)
- **B. PIC foundries and MPW access**
  - B1 SiPh 200/300 mm (passive + active, Ge PD, MRM/MZM)
  - B2 SiN (LPCVD / Damascene)
  - B3 TFLN / TFLT foundry and PDK
  - B4 InP generic integration
  - B5 BTO / OEO / hybrid post-processing service (foundry wafer + BEOL material)
  - B6 MPW brokers and aggregators
  - B7 shared cleanrooms (`foundry_or_fab` facilities; already tracked in EO atlas)
  - B8 OSAT / advanced-packaging foundries (CoWoS, EMIB, fan-out)
- **C. Lasers and active III-V components**
  - C1 DFB/DBR/EML/EA-DFB die and arrays (incl. membrane, heterogeneous)
  - C2 SOA-integrated DFB, high-power CW sources for ELS
  - C3 ELS / ELSFP modules and TOSAs
  - C4 comb sources (QD comb lasers, Kerr microcombs)
  - C5 hybrid/heterogeneous laser integration routes (flip-chip, micro-transfer printing, monolithic nano-ridge)
  - C6 narrow-linewidth and micro-integrated laser modules (ECDL-MOPA, VHBG)
  - C7 commercial discrete EO modulators used as references (bulk LN)
- **D. Fiber, fiber arrays, connectors, optical I/O**
  - D1 fiber: SMF, PMF, UHNA, HNLF, multicore, hollow-core
  - D2 lensed fiber, fiber arrays, FAU, V-groove attach
  - D3 MT ferrules, MPO/MTP, blindmate and detachable connectors
  - D4 glass waveguide fan-out, glass optical bridges, micro-optics/metalenses
  - D5 fusion splicers and fiber processing
- **E. Packaging materials**
  - E1 optical adhesives (UV, hybrid UV+thermal, index-matching), E2 structural/lid adhesives, E3 underfill (CUF, NCF, MUF), E4 build-up dielectric and laminates (ABF, BCB/Cyclotene, Megtron-class), E5 solder, flux, sinter, E6 EMC/mold, E7 TIM, E8 glass cores and interposers
- **F. Packaging and assembly equipment**
  - F1 photonic active alignment / assembly cells, hexapods
  - F2 die and flip-chip bonders (TCB, Au-Au thermocompression)
  - F3 wire bonders
  - F4 photonic wire bonding / 2PP writers
  - F5 micro-transfer printing
  - F6 dispensing and UV curing
  - F7 molding, F8 wafer bonding / debonding, F9 reflow and plating
- **G. Fab tools and consumables**
  - G1 EBL, G2 optical lithography (DUV stepper, maskless, contact), G3 dry etch / ion milling, G4 deposition (PECVD/HDP, ALD, evaporation, sputter), G5 dicing / grinding / CMP / polishing, G6 resists, G7 metrology (ellipsometry, AFM, SEM/FIB/TEM, XRD, confocal, X-ray CT, SAT)
- **H. Characterization and test instruments**
  - H1 tunable lasers / CW sources, H2 OSA, H3 optical power meters, H4 photodetectors / O-E modules / photoreceivers, H5 LCA and VNA (incl. mmWave extenders), H6 AWG / DAC / BERT, H7 oscilloscopes (real-time, sampling DCA), H8 RF amplifiers, drivers, bias tees, MUX, H9 RF probes and probe stations, H10 optical amplifiers (EDFA, PDFA, SOA), H11 filters, polarization control and analysis, H12 SMU / DC supplies / parameter analyzers, H13 positioners and stages, H14 cryogenics, H15 single-photon detection and time tagging, H16 OFDR / reflectometry, H17 laser and TEC controllers, lock-ins, signal generators
- **I. Reliability and qualification**
  - I1 standards (Telcordia, MIL-STD, ESCC, JEDEC, IPC, AEC, IEC, TIA, ASTM, ISO), I2 test types and conditions (TC, DH, HTS/LTS, uHAST, MSL precon, shock/vibration, die shear, radiation), I3 test equipment (shear testers, chambers, gamma sources, X-ray/SAT)
- **J. Design and simulation software** (EDA/PDK flows, FDTD/FEM/RF solvers)
- **K. Standards bodies / MSAs and interface specs** (OIF ELSFP IA, OIF CPO FD, CMIS, IEEE 802.3, UCIe)

Revisions vs the initial brief: split ferroelectric films (A2) from SOI; added A4 organics/LC, A5 2D, A7 glass; added B5 post-processing service and B8 OSAT; added C4 combs and C5 integration routes; added D4 glass optics; added F5 micro-transfer and F9 reflow/plating; added J software and K interface specs (OIF IAs carry many tracked specs).

## 2. Tracked specs per category

Format: field (unit) | why | how papers report | example + locator. Basis vocabulary matches the EO atlas (`measured`, `design_target`, `derived`, `extracted_from_figure`, `simulated`, `author_estimate`) plus proposed `datasheet_spec` / `datasheet_typical` / `stated_in_paper` for vendor values.

### A. Platform materials and substrates

| field | unit | why | reported as | example + locator |
|---|---|---|---|---|
| film_material, cut, dopant | - | Pockels tensor, PRE, DC drift | text in methods | 5 mol% MgO x-cut LN, NanoLN (eo:valdez2023a:p3) |
| film_thickness_nm | nm | mode confinement, Vpi | text | 200 nm LN on 2 um BOX (eo:valdez2023a:p3); LN-on-sapphire 0.9/1.5 um, NGK (eo:didier2026:p6 via papers.csv) |
| box_thickness_um / substrate | um | leakage, RF loss | text | ~500 um Si handle (eo:valdez2023a:p3); BTO 330 nm on insulator, La Luce Cristallina (eo:berman2026:p2) |
| wafer_diameter_mm | mm | fab compatibility, cost | text | 100 mm LNOI (eo:valdez2023a:p3) |
| handle_resistivity | ohm cm | RF loss of electrodes | text | >4000 ohm cm Si interposer (ofc2026:Th4A.6:pNA) |
| soi_grade | - | carrier lifetime, RF | text | float-zone SOI from Shin-Etsu (eo:witmer2020:p14) |
| supplier_process | - | provenance | acknowledgements | LTOI from NSIT and SIMIT-CAS (eo:wang2024b:p9) |
| glass CTE, Dk/Df, thickness | ppm/K, -, um | warpage, RF | text/table | Corning glass panel CTE 7.8 ppm (pk:ectc51909.2023.00298:p2); AGC EN-A1 100 um core (pk:ectc51906.2022.00360:p1); Schott D 263, 50 x 50 x 0.4 mm (pk:ectc51529.2024.00133:p2) |
| EO coefficient of organic (r33) | pm/V | drive voltage | measured in device | N/A in vendor terms; device-level values already in EO atlas |
| datasheet-only | - | - | not in papers | thickness uniformity, TTV, bow, film stoichiometry, defect density, price, lead time: N/A in corpus |

Product-line evidence for substrates: Soitec URD names Photonics-SOI, POI and LNOI product lines (blog:soitec-universal-registration-document-2024-2025---en:p5, p27).

### B. Foundries / MPW

| field | unit | why | reported as | example + locator |
|---|---|---|---|---|
| platform, wafer size, node/litho | - | capability | text | AIM 300 mm SOI, 220 nm Si, 193 nm immersion (eo:saxena2023:p1); AMF O-band GP v4.5 platform, 200 mm (eo:johnson2025:p1); IHP 200 mm SiGe BiCMOS, 248 nm DUV (eo:steckler2025 via papers.csv) |
| wg_loss_db_per_cm by waveguide type | dB/cm | link budget | text/table | Samsung Foundry: Si strip 1.2, SiN strip 0.4, Si rib 0.7 dB/cm (ofc2026:Tu2D.3:p1-2, Sec. 3) |
| coupler loss and 1 dB BW (GC/EC) | dB, nm | I/O budget | text | Samsung: 1D Si GC 1.9 dB, 27 nm; SiN GC 2.1 dB, 57 nm (ofc2026:Tu2D.3, Sec. 3) |
| modulator BBs (eff., BW) | pm/V, V cm, GHz | PDK value | text | Samsung MRM 52.0 pm/V, MZM ~1.4 V cm, 50 GHz (ofc2026:Tu2D.3, Sec. 3); HHI InP: 25 GHz EAM/MZM, 40 GHz PD, DBR 50 nm tuning, SOA >15 dB (blog:20210910_Foundry-services...:p2) |
| PDK features | - | design flow | table | Samsung PDK >40 devices, DRC/LVS/PEX, 25-85 C models (ofc2026:Tu2D.3, Table 2) |
| MPW cadence / access route | - | schedule | flyer | HHI "tape out every 3 months", MPW + customer runs (blog:20210910_Foundry-services...:p1); JePPIX MPW (eo:gupta2023:p1); CMC Microsystems MPW of AMF (eo:geravand2025:p12) |
| open PDK | - | access | text | Luxtelligence lnoi400 open-source PDK (eo:kari2025:p4) |
| post-process option | - | hybrid EO | text | SOH post-processing by NLM on AMF wafers (eo:johnson2025:p1); FN-LC coated post-foundry on AMF (eo:taghavi2026:p4) |
| datasheet-only | - | - | - | price per mm2/run, design rules, yield, reliability qual of BBs: N/A in corpus |

### C. Lasers and active III-V

| field | unit | why | reported as | example + locator |
|---|---|---|---|---|
| fiber_coupled_power_dbm per channel | dBm | ELS power class | figure/text | >+25 dBm x 8 ch at 25 C case, >=+23 dBm at 55 C (ofc2026:W1B.3:p2-3) |
| channel count, wavelength grid | -, nm | CWDM/DR mapping | text | 16-ch ELSFP from two 8-ch TOSAs (ofc2026:W3E.1:p2) |
| wall-plug / power conversion eff. | % | thermal budget | text | PCE 23.5 % / 21.6 % at +20 dBm, 25 / 55 C (ofc2026:W3E.1:p2) |
| case temperature range | C | cooled vs uncooled | text | 25 C cooled, 55 C uncooled (ofc2026:W1B.3:p2) |
| cavity length / chip size / package size | mm | thermal resistance | text | SOA-DFB 1.0 and 1.8 mm; TOSA 22.5 x 13.0 x 3.3 mm (ofc2026:W1B.3:p1) |
| RIN | dB/Hz | link SNR | slide | < -155 dB/Hz (blog:robert-blum-intel-high-volume-silicon-photonics:p6) |
| SMSR | dB | single-mode | slide | > 40 dB (same, p6) |
| reliability FIT | FIT | system FIT | slide/table | ~2 FIT laser (blog:robert-blum...:p3); OIF CPO target 50 FIT per 3.2T laser source, 10 FIT engine, 6 yr life (blog:OIF-Co-Packaging-FD-01.0:p13 Table 1) |
| linewidth, tuning range | kHz, GHz | coherent / sensing | text | ECDL-MOPA mode-hop-free tuning 22 GHz, >100 GHz cascaded (blog:ao-64-30-9049-...:p1) |
| integration route | - | supply chain | text | Au-Au TC flip-chip DFB on LN with Fineplacer Femto 2 (eo:shamsansari2021:p2); micro-transfer printing (eo:zheng2026:p3); GaAs nano-ridge on 300 mm Si (ofc2026:W2A.10) |
| datasheet-only | - | - | - | aging slope, Ith vs T, kink-free power, ESD, price: N/A |

### D. Fiber, arrays, connectors

| field | unit | why | reported as | example + locator |
|---|---|---|---|---|
| MFD at lambda | um | coupling | datasheet / text | SMF-28 Ultra 9.2 +/- 0.4 um @1310, 10.4 +/- 0.5 um @1550 (blog:corning-smf-28-ultra-specifications:p1); UHNA4 3.3 um @1310, 4.0 um @1550 (eo:li2026aa:p2) |
| attenuation, cutoff, standard compliance | dB/km, nm | link | datasheet | <=0.32 dB/km @1310, <=0.18 @1550, lambda_cc <=1260 nm, G.652.D / G.657.A1 (blog:corning-smf-28...:p1) |
| fiber-to-PIC IL per facet, spread, n | dB | yield | table | EMIB CPO mean -2.46 dB/facet, sigma 0.38 dB, 386 chiplets / 193 packages, IEC 61300-3-4 (pk:ectc51687.2025.00012:p2) |
| connector IL / mating | dB | detachability | text | Intel glass bridge: 0.33 dB avg connector loss, 1.41 dB fiber-to-PIC (blog:Detachable_Optical_Chiplet_Connector...:p1); 3-sigma tolerance 1.58 um, 6.5 um MFD at PIC (p3) |
| pitch, channel count | um | density | text | 250 um FA pitch, <30 um possible (blog:Detachable...:p2); 2D FAU 12 x 3, 500/250 um pitch (ofc2026:Th2A.8) |
| MT ferrule type and standard | - | interop | spec | MT-12/24/36 per TIA-604-5, IEC 61754-7-1/-2, IEC 61755-3-31 (blog:OIF-ELSFP-02.0-1:p33) |
| PER | dB | PM delivery | spec | defined at MT ferrule, value per application (blog:OIF-ELSFP-02.0-1:p36) |
| glass waveguide loss / bend loss | dB/cm | fan-out | abstract | 0.01 dB/cm bend loss R>6 mm @1310, <0.3 dB coupling, 150 mm wafers (ofc2026:Th1D.3:pNA) |
| lensed fiber spec | - | test setups | part number | OZ Optics TSMJ-X-1550-9/125-0.25-7-2.5-14-2 (eo:gaier2025:p13) |

### E. Packaging materials

| field | unit | why | reported as | example + locator |
|---|---|---|---|---|
| refractive index (cured) | - | index matching | text | Dymax OP-29 n = 1.5 (pk:eptc59621.2023.10457729:p3) |
| viscosity | cP | dispense, wicking | text | OP-29 2500 cP (same) |
| cure schedule (UV dose, T, t) | mJ/cm2, C, s | throughput, stress | text | OP-29 ~2 min; hybrid adhesives UV then 120 C 30 min, 10 C/min (blog:Micro-integrated_optical_systems...:p4); UF batch cure 160 C 2 h (pk:ectc51846.2026.00176:p2) |
| linear shrinkage | % | alignment drift | text | stated as "linear shrinkage" for index-matching epoxy, value in source (blog:Detachable...:p3) |
| Dk / Df at f | -, - | RF of CPO substrate | text | EPO-TEK 301-2 Dk 3.8, Df 0.012 (pk:tcpmt.2025.3533388:p9) |
| shear strength vs aging | N | qualification | figure | MIL-STD-883L TM 2019.9 requirement 24.5 N (1.0x) / 49 N (2.0x) for 8 mm2 die (blog:Micro-integrated_optical_systems...:p5) |
| Tg, CTE, modulus, outgassing (ASTM E595), moisture uptake | C, ppm/K, GPa, % | reliability | rarely in papers | mold Tg 150 C (pk:ectc51846.2026.00176:p2); adhesive Tg/CTE/outgassing: N/A in corpus |
| build-up film product | - | substrate stack | text/table | ABF GX92 / GX92P (pk:ectc51909.2023.00298:p2); ABF GL-102 (pk:ectc51529.2024.00392:p1) |

### F. Packaging / assembly equipment

| field | unit | why | reported as | example + locator |
|---|---|---|---|---|
| placement accuracy | um (3 sigma) | coupling yield | rarely in papers | "sub-micron bonder" Finetech FEMTO2 (pk:tcpmt.2024.3507552:p7); numbers N/A |
| alignment DOF / method | - | active vs passive | text | ficonTEC AL1200 six-axis active FAU alignment (pk:ectc51846.2026.00176:p3); PI H-206 hexapod (eo:bankwitz2026:p19) |
| bond force, temperature, time | N, C, s | process window | text | lid attach 150 C, 15 kg, 300 s (pk:ectc51846.2026.00176:p2) |
| UV source | - | cure | text | Dymax ECE 5000 flood lamp (pk:001c.147108:p2); intensity-calibrated Hg source (blog:Micro-integrated_optical_systems...:p4) |
| dispense volume resolution | nL | adhesive control | text | 240 nL applied, down to 20 nL (blog:Micro-integrated_optical_systems...:p4) |
| throughput (UPH), price | - | cost model | N/A in corpus | - |

### G. Fab tools and consumables

| field | unit | why | reported as | example + locator |
|---|---|---|---|---|
| EBL acceleration voltage | kV | resolution | text | Raith EBPG 5200+ 100 kV (eo:didier2026:p7); JEOL JBX-6300FS 100 keV (eo:multani2025:p17); Raith Voyager 50 kV (eo:berman2026:p8) |
| litho wavelength / tool | nm | CD | text | ASML PAS 5500/350C DUV (eo:li2026ba:p3, eo:cai2025:p13); Heidelberg MLA 150 at 375 nm (eo:multani2025:p17) |
| etch chemistry, depth, sidewall | -, nm, deg | loss | text | Oxford PlasmaPro 100 Ar+ RIE, 1 um (eo:didier2026:p7); Ar/CHF3 ICP ~75 deg (eo:berman2026 via papers.csv) |
| deposition tool, T | C | film quality | text | Veeco Fiji PE-ALD Al2O3 at 150 C (eo:tiberi2025:p9); PlasmaTherm Versaline HDP-CVD (eo:multani2025:p17) |
| dicing / polishing | - | facet quality | text | Disco DAD 3221 + Allied MultiPrep polish (eo:didier2026:p7) |
| resist (tone, thickness) | nm | pattern | text | ma-N 2405 at 500 nm (eo:berman2026:p8); ZEP520A 600 nm, Elionix Boden-150 (eo:sun2026a:p25) |

### H. Characterization instruments (tracked both as product specs and as "as-used" specs per paper)

| field | unit | why | example + locator |
|---|---|---|---|
| analog BW / frequency range | GHz | sets bw_measured_to_ghz ceiling in EO atlas | Anritsu ME7838AX 70 kHz-125 GHz with MPI T110A 110 GHz probes (eo:li2026:p2); Picoprobe Model 110 to 110 GHz (eo:valdez2023a:p4); Finisar XPDV3120R 70 GHz (eo:ummethala2021:p5); Keysight UXR0702AP 70 GHz (eo:mao2024:p7) |
| sample rate / DAC resolution | GSa/s, bit | max baud | Keysight M8199B 256 GSa/s (eo:aihara2026:p2), 80 GHz analog BW (eo:mao2024:p7); Micram DAC4 100 GS/s (eo:tiberi2025:p15) |
| tuning range, linewidth, sweep speed | nm, kHz, nm/s | resonator metrology | Santec TSL-550 / TSL-570 / TSL-710 (Section 3); specs datasheet-only |
| OSA resolution | GHz/pm | sideband method | Thorlabs OSA 305 at 1.9 GHz resolution (eo:didier2026:p8) |
| gain / NF / Psat of amplifier | dB, dBm | link | PriTel LNFA-33, 33 dB small-signal gain (eo:bankwitz2026:p19) |
| RF amp gain, BW, Psat; bias tee range | dB, GHz | drive | Mini-Circuits ZX85-12G-S+ 0.2 MHz-12 GHz (eo:sun2026a:p16) |
| probe pitch, config | um, GSG/GSSG | pad design | PicoProbe 40A, 150 um pitch (eo:berman2026:p9) |
| timing resolution | ps | photon statistics | Swabian Time Tagger Ultra 8 ps (eo:bankwitz2026:p21) |
| base temperature | K | cryo EO | Montana Instruments S200 ~5 K (eo:anderson2025:p8); Bluefors LD400 (eo:mohl2025:p21) |
| calibration method | - | traceability | SOLT on calibration substrate (eo:li2026:p2); NIST-calibrated Thorlabs FDS1010-CAL (ofc2026:Th1A.4:p1) |

### I. Reliability

| field | unit | example + locator |
|---|---|---|
| standard id + method/condition letter | - | MIL-STD-883L TM 1010.8 A: -55/85 C, 100 cycles; TM 1010.8 B adapted -55/150 C, 100 cycles, 20 min dwell, 10 s transfer (blog:Micro-integrated_optical_systems...:p4); ESCC 23201 (same, p4) |
| T range, cycles, dwell | C, n, min | Telcordia GR-468 (non-powered, adapted): TC -40/+85 C 500 cycles; HTS 85 C 1250 h; LTS -40 C 72 h; DH 85 C/85 %RH 500 h, extended to 2000 h (pk:ectc51906.2022.00072:p6 Table 1) |
| pass criterion | dB, N | IL shift < 0.5 dB after GR-468 (pk:ectc51906.2022.00072:p2) |
| mechanical | g, ms, g_rms | shock 1500 G, 0.5 ms; vibration 20 G RMS, 15 min/axis, MIL-STD-883 2002 B / 2026F (pk:ectc51687.2025.00012:p5) |
| radiation | Sv, source | Co-60 gamma 10 000 mSv (blog:Micro-integrated_optical_systems...:p4-5) |
| moisture / package | - | J-STD-020E MSL4 30 C/60 %RH/96 h + reflow (pk:ectc32696.2021.00315 via metrics.csv p5 Table I); JESD22-A118 uHAST 130 C/85 %RH/96 h (pk:ectc51529.2024.00011 via metrics.csv p6 Table 2) |
| failure-mode taxonomy | - | DIN EN ISO 10365 AF/CF/ACF/JF (blog:Micro-integrated_optical_systems...:p5) |
| sample size | n | 45 samples, 1250 h (pk:ectc51906.2022.00072:p5) |
| test equipment | - | Nordson Dage 4000 Plus, <=1 % force accuracy (blog:Micro-integrated_optical_systems...:p5) |

### K. Interface specs (OIF)

| field | unit | value + locator |
|---|---|---|
| ELSFP optical power class (per lambda per core, +/-1.5 dB) | dBm | LP 11, MP 14, HP 17, VHP 20, UHP 23, SHP 26 (blog:OIF-ELSFP-02.0-1:p38 Table 6) |
| ELSFP electrical power class | W | LP / Class 1 1.5 W, Class 2 5 W, Class 3 10 W, Class 4 15 W ... (blog:OIF-ELSFP-02.0-1:p43 Table 8) |
| supply | V, A | six 3.3 V pin pairs, up to 1.5 A each (same, p43) |
| case temperature ranges | C | 0-70, -5-85, -40-85 (same, p47) |
| laser safety | - | IEC 60825-2 Hazard Level 1 (same, p10); IEC 60825-1/-2 (blog:OIF-Co-Packaging-FD-01.0:p20) |
| CPO energy / reliability targets | pJ/b, FIT, yr | <=15 pJ/b (DC switching), 5-10 pJ/b (HPC/AI); engine 10 FIT and laser 50 FIT per 3.2T; 6 yr (blog:OIF-Co-Packaging-FD-01.0:p13 Table 1) |
| optical IL budget | dB | 4 dB single-mode DR/FR, 1.8 dB short reach MM, 8-10 dB CXL (blog:OIF-Co-Packaging-FD-01.0:p12,p14) |

## 3. Observed items (seed list)

Columns: vendor (as the paper names it; lineage in notes) | product/model (only if stated; "-" otherwise) | cat | locators (up to ~5) | n = distinct docs with usage sentence (eo/pk/ofc/blog). Model-level counts in brackets are distinct docs matching that model regex.

### 3.1 Wafers, substrates, materials (A)

| vendor | product/model | cat | locators | n |
|---|---|---|---|---|
| NanoLN (Jinan Jingzheng Electronics) | x-cut / z-cut LNOI, MgO:LN, x-cut LTOI/TFLT, 4-inch | A2.1/A2.2 | eo:valdez2023a:p3; eo:li2020:p3; eo:lin2025:p5; eo:sayem2026c:p2; eo:lin2026a:p13 | 46 (44/0/2/0) |
| Novel Si Integration Technology (NSIT) + SIMIT-CAS | LTOI wafers | A2.2 | eo:wang2024b:p9; eo:cai2025:p8 | 2 |
| NGK Insulators | x-cut LN-on-sapphire 0.9 / 1.5 um | A2.3 | eo:didier2026:p6 | 1 |
| La Luce Cristallina | BTO-on-insulator 330/400 nm | A2.4 | eo:berman2026:p2; eo:chelladurai2025 (ack, papers.csv) | 1-2 |
| Lumiphase | BTO growth/integration, 200 mm BTO process | A2.4/B5 | eo:qiu2026a:p1; eo:kohli2025:p10; ofc2026:Th3J.4:pNA | 3 |
| Soitec | SOI substrates; Photonics-SOI, POI, LNOI lines | A1 | eo:sun2026a:p13; blog:soitec-urd:p5,p27 | 1 + URD |
| Shin-Etsu | float-zone SOI | A1 | eo:witmer2020:p14 | 1 |
| Okmetic | Si wafers (ack) | A1 | pk:tcpmt.2021.3111345:p7 | 1 |
| Sumitomo Electric | InP / fiber / HNLF (role varies) | A3/D1 | pk:estc60143.2024.10712002:p1; ofc2026:M4C.1:p1; ofc2026:M1K.5:p1 | 4 |
| IQE | epi (mention) | A3 | ofc2026 (1 raw mention, no usage sentence) | 0 |
| UK national epitaxy facility (Sheffield) | GaAs wafers | A3 | papers.csv wafer_supplier (paper per papers.csv) | 1 |
| NLM Photonics | JRD1, Selerion-HTX OEO; SOH post-processing | A4/B5 | eo:johnson2025:p1; eo:karakida2026:p3; eo:soma2025:p4; ofc2026:W2A.5:p2 | 4 |
| Lightwave Logic | Perkinamine chromophore series 3 | A4 | eo:hess2026:p3; eo:horst2025:p4; ofc2026:M2B.5:p3 | 3 |
| Soluxra | SEO100C EO polymer | A4 | eo:witmer2020:p5; eo:taghavi2022a:p9 | 2 |
| Polaris Electro-Optics | FN-LC PM-158 / pm-158 | A4 | eo:taghavi2024:p13; eo:taghavi2026:p4; eo:zhang2026a:p1; ofc2026:M2B.4:pNA | 4 |
| Graphenea | 6-inch CVD graphene | A5 | eo:wu2023:p3 | 1 |
| Grolltex | CVD graphene | A5 | eo:lee2020:p12; eo:lee2020a:p3 | 2 |
| CrysTec | GdScO3 (110)o substrate | A6 | eo:suceava2025:p8 | 1 |
| MTI Corp | single-crystal substrate | A6 | eo:suceava2025:p21 | 1 |
| Corning | glass panels/cores; IOX glass waveguides | A7/D4 | pk:ectc51909.2023.00298:p2; pk:001c.74748:p1; pk:ectc51529.2024.00396:p2; ofc2026:Th1D.3; ofc2026:Th3C.2 | 14 (0/9/5/0) |
| AGC | EN-A1 alkali-free glass | A7/E8 | pk:ectc51906.2022.00360:p1; pk:ectc51846.2026.00103:p2 [EN-A1: 2] | 5 |
| Schott | D 263 (T eco) glass, BF33 | A7/E8 | pk:ectc51529.2024.00133:p2; pk:ectc51846.2026.00302:p1; pk:tcpmt.2025.3533388:p2 | 4 |
| Heraeus (Comvance) | multicore fiber / fused silica | A7/D1 | ofc2026:Th4C.2:p1; ofc2026:Th2A.18:pNA | 3 |

### 3.2 Foundries, MPW, OSAT (B)

| org | process / product | cat | locators | n |
|---|---|---|---|---|
| Advanced Micro Foundry (AMF) | SOI process, O-band GP v4.5, DUV with 5 um oxide opening | B1 | eo:johnson2025:p1; eo:taghavi2026:p4; eo:singer2025:p5; eo:zhong2026:p4; eo:shen2021:p2 | 21 (11/0/10/0) |
| imec | ISIPP50G PDK; 200 mm pilot line; GaAs nano-ridge on 300 mm | B1 | eo:li2026b:p1; eo:wu2023:p11; eo:heidari2022:p1; ofc2026:W2A.10 | 26 (includes affiliations) |
| AIM Photonics | 300 mm Active PIC, AP SUNY PDK | B1 | eo:saxena2023:p1; eo:shawon2024:p7; eo:larocque2024:p22; pk:ectc51909.2023.00048:p1 | 7 |
| GlobalFoundries | SiPh platform (named); V-groove FA with IBM Bromont | B1 | eo:chaudhury2024:p1; pk:ectc51906.2022.00072:p2; pk:ectc51909.2023.00252:p1; ofc2026:M2D.6:p1 | 8 |
| Samsung Foundry | 300 mm SiPh platform + PDK | B1 | ofc2026:Tu2D.3; ofc2026:Th3F.6:p1 | 3 |
| Intel | 300 mm SiPh, hybrid III-V lasers, wafer-level burn-in | B1/C1 | eo:hsu2024:p6; blog:robert-blum-intel...:p2; pk:ectc51687.2025.00012:p1 | 27 (mostly own-author) |
| TSMC | 3D-stacked SiPh engine process (for NVIDIA); CoWoS | B1/B8 | blog:umesh-shainer-nvidia...:p13; pk:ectc51687.2025.00047:p1 | 27 (mostly own-author) |
| IHP | 200 mm SiGe BiCMOS / SG13G2 | B1 | eo:steckler2025:p7; eo:kawahara2025:p4 | 2 |
| CUMEC | 8-inch 130 nm Si/SiN PDK | B1 | eo:wu2025:p11; ofc2026:Th2A.9:p2 | 2 |
| CompoundTek | 90 nm 200 mm SOI | B1 | eo:han2023:p7; eo:sia2022:p1 | 2 |
| SMIC | CMOS SiPh process | B1 | eo:yue2023:p8 | 1 |
| A*STAR IME | 200 mm SOI | B1 | eo:kieninger2020:p2; eo:wolf2018a:p4 | 7 (some affiliations) |
| Tower Semiconductor | SiPh (named) | B1 | pk:ectc51909.2023.00023:p2; ofc2026:M1E.4:p2; ofc2026:W4B.1:pNA | 3 |
| STMicroelectronics | SiPh (named) | B1 | ofc2026:Tu2D.4:pNA | 1 |
| CORNERSTONE | 220 nm SOI, selective planarization | B1 | eo:tiberi2026:p1; ofc2026:Th2A.12:pNA | 2 |
| Applied Nanotools | 220 nm SOI passive | B1 | eo:chaudhury2024:p4; ofc2026:Th2A.4:p2; ofc2026:Tu2J.5:p1 | 4 |
| Sandia National Laboratories | MESA CMOS line | B1 | eo:boynton2020:p3; eo:derose2012:p2 | 3 |
| LIGENTEC | SiN wafers | B2 | eo:kohli2025:p10; eo:rahman2025:p3; eo:valdez2026:p1; ofc2026:W1A.6:pNA | 5 |
| Luxtelligence | TFLN foundry, lnoi400 PDK | B3 | eo:kari2025:p4; eo:liu2026d:p4 | 2 (+4 affiliations) |
| CSEM | TFLN MPW run | B3 | eo:larocque2024:p6 | 1 |
| HyperLight | TFLN devices (own-author paper; foundry role not stated) | B3 | eo:kharel2021:p1 | 1 |
| Fraunhofer HHI | generic InP MPW; TFLN; polymer PolyBoard | B4 | eo:gupta2023:p1; eo:ummethala2021:p4; blog:20210910_Foundry-services...:p1-2; blog:4.2-Frraunhofer-HHI-Martin-Schell:p2 | 12 |
| SMART Photonics | JePPIX generic InP | B4 | eo:hillier2025 (papers.csv) | 1 |
| JePPIX | InP MPW broker | B6 | eo:gupta2023:p1; eo:hillier2025:p5 | 2 |
| CMC Microsystems | MPW broker (AMF) | B6 | eo:geravand2025:p12; eo:taghavi2022a:p15; ofc2026:M1G.6:p3 | 3 |
| Enosemi | SOH PIC design with NLM | B5 | eo:johnson2025:p1 | 1 |
| Amkor | OSAT | B8 | pk:ectc51529.2024.00392:p2; pk:tcpmt.2025.3610036:p1 | 5 |
| ASE | OSAT | B8 | pk:ectc51846.2026.00008:p1; pk:ectc51687.2025.00095:p1 | 3 |
| SPIL | OSAT | B8 | pk:ectc51687.2025.00187:p6; pk:ectc51906.2022.00181:p1 | 3 |
| JCET | OSAT | B8 | pk:ectc32696.2021.00174:p6 | 1 |
| Fraunhofer IZM-ASSID | TSV wafers | B8 | pk data/components.csv supplier | 3 rows |

### 3.3 Lasers, sources, active components (C)

| vendor | product/model | cat | locators | n |
|---|---|---|---|---|
| Furukawa Electric | SOA-integrated DFB-LD, 8-ch CWDM TOSA, 16-ch ELSFP | C2/C3 | ofc2026:W1B.3; ofc2026:W3E.1 | 2 |
| Intel | hybrid III-V/Si DFB, 8-ch on-chip DFB array, CWDM4 transmitter | C1/C5 | blog:robert-blum-intel...:p3,p6,p13 | 1 deck |
| NVIDIA | 1.6T SiPh CPO, "high-power, high-efficiency lasers", detachable connectors | C3/K | blog:umesh-shainer-nvidia...:p13,p16 | 1 deck |
| Ranovus (with MediaTek) | Odin CPO 3.0, integrated laser, 4 pJ/bit incl. laser | C1/B | blog:ranovus-mediatek-cpo-3-ofc-2024:p1 | 1 |
| Lumentum | Graybox ROADM (testbed, ofc2026:M3Z.3); other roles per paper | C | ofc2026:M3Z.3:pNA; ofc2026:M1A.3:p2; eo:kawahara2026:p3 | 6 |
| NeoPhotonics | Class 60 coherent driver modulator (CDM) | C | ofc2026:M3J.2:p2; ofc2026:W2A.39:p2 | 3 |
| NTT Electronics | NLK1556STG (laser) | C | ofc2026:W4D.6:pNA | 1 |
| ID Photonics | CoBriteDX4 ECL | H1 | ofc2026:M3B.3:p2; ofc2026:M3M.2:p1; ofc2026:W3B.4:p2 | 5 |
| X-Celeprint | micro-transfer printing | C5/F5 | eo:zheng2026:p3; blog:Combined-ECTC-2015...:p3 | 1-2 |
| Thorlabs | LN27S-FC, LN65S-FC bulk LN modulators (reference) | C7 | eo:larocque2024:p22; eo:zhu2022:p2 | 2 |
| Eospace | LN modulator (as used) | C7 | eo:zhang2024:p13 | 1 |
| FBH (Ferdinand-Braun-Institut) | micro-integrated ECDL-MOPA module (custom Peltier with NTC, VHBG, 60 dB micro-isolator) | C6 | blog:ao-64-30-9049-...:p2-3 | 1 |
| OIF member roster (role not stated) | ~120 companies, e.g. Coherent, Lumentum, Broadcom, Marvell, AOI, Innolight, Eoptolink, Source Photonics, Scintil, Quintessent, Sicoya, SiFotonics, DustPhotonics, Teramount, US Conec, Senko, Molex, Fujikura, Hirose, TE, Samtec, Amphenol | K | blog:OIF-ELSFP-02.0-1:p61; blog:OIF-Co-Packaging-FD-01.0:p52-53 | roster, not usage |

### 3.4 Fiber, arrays, connectors (D)

| vendor | product/model | cat | locators | n |
|---|---|---|---|---|
| Corning | SMF-28 / SMF-28 Ultra [SMF-28: 22 docs] | D1 | blog:corning-smf-28-ultra-specifications:p1; eo:geravand2025:p13; eo:larocque2024:p23; eo:mohl2025:p21 | 22 (model) |
| Nufern (written "Coherent-Nufern") | PLMA-YDF-10/125-M Yb fiber; UHNA fibers usually stated without vendor | D1 | eo:park2026:p16; eo:liu2026d:p4; eo:guo2026:p13; UHNA4 vendor not stated (eo:li2026aa:p2) | 3 |
| OFS | HNLF (OFS Denmark), fibers | D1 | ofc2026:M4C.1:p1; ofc2026:Tu3D.4:p2; ofc2026:W4B.5:p2 | 5 |
| YOFC | fibers (OFC usage) | D1 | ofc2026:Th1A.6:p2; ofc2026:Tu3D.4:p2; ofc2026:Tu3E.5:p2 | 4 |
| Sumitomo Electric | HNLF | D1 | ofc2026:M4C.1:p1 | see A |
| Fujikura | FSM-100P fusion splicer | D5 | ofc2026:M1J.4:p2; ofc2026:Th2A.18:pNA | 2 |
| OZ Optics | lensed fiber TSMJ-X-1550-9/125-..., 8 deg angled FA | D2 | eo:gaier2025:p13; eo:taghavi2026:p6; eo:renaud2023:p5; eo:nelan2022:p5; eo:larocque2024:p22 | 8 |
| Chiral Photonics | fan-in/out | D2 | ofc2026:W1F.7:p3 | 1 |
| Pixel Photonics / Linq Photonics | (named in eo:bankwitz2026) | D/? | eo:bankwitz2026:p12; eo:bankwitz2026:p23 | 1 |
| Intel | glass optical bridge + pluggable FAU (laser-written waveguides) | D3/D4 | blog:Detachable_Optical_Chiplet_Connector...:p1-p8 | 1 |
| AuthenX | meta-lens + 2D FAU detachable coupling | D4 | ofc2026:Th2A.8 | 1 |
| IBM Bromont + GlobalFoundries | self-aligned V-groove SMF attach | D2/F | pk:ectc51906.2022.00072:p2 | 1 |
| unnamed FAU suppliers | 24-ch FAU, 2x12 MTP to 1x24 PM FA | D2/D3 | pk:ectc51687.2025.00012:p2 | 1 |

### 3.5 Packaging materials (E)

| vendor | product/model | cat | locators | n |
|---|---|---|---|---|
| Dymax | OP-29 optical epoxy; ECE 5000 UV flood lamp | E1/F6 | pk:eptc59621.2023.10457729:p3; pk:001c.147108:p2 | 2 |
| Epoxy Technology | EPO-TEK 301-2 (underfill role) | E1/E3 | pk:tcpmt.2025.3533388:p4,p9 | 1 |
| Henkel / Loctite | (named) | E | pk:tcpmt.2021.3111345:p3 | 1 |
| Namics | U8410-406, U8443-14, U8419-73CF3 underfill; H9890-7 sinter glue | E3/E5 | pk:ectc51529.2024.00311:p3; pk:tcpmt.2025.3614186:p3; pk:estc55720.2022.9939446:p3; pk:ectc51846.2026.00096:p5 | 4 |
| Ajinomoto | ABF GL-102, GX92, GX92P | E4 | pk:ectc51909.2023.00298:p2; pk:ectc51529.2024.00392:p1; pk:ectc51846.2026.00074:p4 [13 docs] | 34 (brand mention) |
| DuPont | CYCLOTENE DF-PID, XP80 (BCB) | E4 | pk:3dic63395.2024.10830178:p1; pk:ectc51687.2025.00233:p1 | 3 |
| Dow / Dow Corning | FOX-16 / HSQ (as stated) | E/G6 | eo:he2019:p8; eo:shamsansari2021:p2; pk:ectc51906.2022.00053:p3 | 6 |
| Resonac | build-up/underfill/mold (role per paper) | E3/E4/E6 | pk:ectc51909.2023.00298:p2; pk:ectc51846.2026.00153:p2; pk:ectc51846.2026.00074:p4 | 5 (+11 components.csv rows) |
| Panasonic | R-1566S FR4, R-G740M RCC | E4 | pk:estc60143.2024.10712019:p1; pk:001c.147203:p2 | 3 |
| Nitto Denko | tapes/films (role per paper) | E | pk:ectc51846.2026.00356:p2; pk:ectc51846.2026.00153:p3 | 3 |
| JSR, Toray, Taiyo Ink, HD MicroSystems, Unimicron | dielectrics / PI / solder resist / substrate | E4 | pk:tcpmt.2025.3610036:p1; pk:ectc51846.2026.00424:p2; pk:ectc51846.2026.00119:p1; pk:ectc51529.2024.00321:p4; pk:ectc51687.2025.00233:p5 | 1-2 each |
| Senju Metal | SNR-1065GT reflow oven (equipment) / solder | E5/F9 | pk:ectc51909.2023.00155:p4; pk:ectc51687.2025.00027:p3 | 3 |
| Indium Corp | solder | E5 | pk:tcpmt.2021.3111345:p2 | 1 |
| Fujifilm | MS6020 Cu cleaning | E/G | pk:ectc51529.2024.00311:p2 | 1 |
| Nagase | (named) | E | eo:khalil2026:p14 | 1 |
| unnamed | index-matching silicone, silica-filled low-shrink epoxy, silicone lid adhesive | E1/E2 | pk:ectc51846.2026.00176:p2-4 | 1 |

### 3.6 Packaging / assembly equipment (F)

| vendor | product/model | cat | locators | n |
|---|---|---|---|---|
| ficonTEC | AL1200 automated active alignment | F1 | pk:ectc51846.2026.00176:p3; ofc2026:Th1D.5:pNA; ofc2026:Th3C.1:p2 | 3 |
| Physik Instrumente (PI) | H-206 hexapod; H-811 hexapod + P-611.3 piezo; RS-40 rotation stage | F1/H13 | eo:bankwitz2026:p19; ofc2026:Tu2D.5:pNA; eo:didier2026:p7; eo:shawon2024:p3 | 3-4 |
| Finetech | Fineplacer Femto 2 / FEMTO2 | F2 | eo:shamsansari2021:p2; pk:001c.74770:p3; pk:tcpmt.2024.3507552:p7 | 3 |
| Besi | TC-advanced, TCnext | F2 | pk:ectc51906.2022.00179:p2; pk:tcpmt.2025.3628798:p5 | 5 |
| Kulicke & Soffa | APAMA C2W, APTURA | F2 | pk:ectc51846.2026.00062:p2; pk:ectc51529.2024.00392:p5 | 4 |
| Panasonic Connect | MD-P300 flip-chip bonder, NPM-WX mounter | F2 | pk:ectc51529.2024.00155:p3; pk:ectc51687.2025.00027:p2 | 4 |
| SET | (bonder, named) | F2 | pk:ectc51846.2026.00204:p2 | 1 |
| ASMPT | (named) | F2 | eo:zheng2026:p6; pk:ectc51909.2023.00048:p3 | 2 |
| Shinkawa | (bonder, named) | F2/F3 | eo:li2020:p8 | 1 |
| West Bond / Hesse / TPT | wire bonders | F3 | eo:kawahara2025:p8; eo:powell2024:p4; pk:tcpmt.2024.3507552:p6 | 1-2 each |
| Vanguard Automation | photonic wire bonding | F4 | eo:singer2025:p16; eo:taghavi2026:p7; ofc2026:W4B.1:p2 | 3 |
| Nanoscribe | 2PP | F4 | ofc2026:W2A.7:p1 | 1 |
| Musashi Engineering | FAD2500 jet dispenser | F6 | pk:ectc51529.2024.00155:p2; pk:ectc51687.2025.00027:p2 [4 docs] | 4 |
| APIC Yamada / Towa | VCM-300 compression molding / wafer molding | F7 | pk:ectc51529.2024.00155:p2; pk:ectc51909.2023.00155:p3 | 3 each |
| EV Group | EVG 810/501/301 plasma activation + bonding, EVG 620, EVG520IS, Gemini FB XT | F8 | eo:li2026ba:p3; eo:wu2025:p12; pk:tcpmt.2021.3111345:p2; pk data/process_steps.csv | 12 |
| SUSS MicroTec | XBS300 D2W bonder, XBC300 laser debonder, ACS300 track, MA6 | F8/G2 | pk:ectc51529.2024.00106:p2; pk:eptc62800.2024.10909935:p1; eo:lee2020:p12 | 5 |
| AIMECHATEC | laser debonder / wafer bonder | F8 | pk:ectc51687.2025.00027:p2; pk:ectc51529.2024.00155:p2 | 2 |
| Sakura Seiki | YWV-4635S flux cleaner | F9 | pk:ectc51687.2025.00027:p3 | 2 |
| Tosetz | 4C204 face-up electroplating | F9 | pk:ectc51909.2023.00307:p4; pk:001c.147098:p3 | 2 |

### 3.7 Fab tools and consumables (G)

| vendor | product/model | cat | locators | n |
|---|---|---|---|---|
| Raith (Vistec) | EBPG 5200(+), Voyager | G1 | eo:didier2026:p7; eo:tiberi2025:p9; eo:berman2026:p8; eo:shen2025:p4 (as "Vistec EBPG 5200+") | 6 (+2 Vistec) |
| JEOL | JBX-6300FS, JBX-8100FS, JBX-9300FS; JIB-4700F FIB | G1/G7 | eo:multani2025:p17; eo:taghavi2024:p12; eo:park2026:p16; eo:berman2026:p8 | 12 |
| Elionix | ELS-G100, ELS-F125, ELS-G150, Boden-150 | G1 | eo:mao2024:p6; eo:renaud2023:p5; eo:kim2025:p2; eo:sun2026a:p25 | 8 |
| ASML | PAS 5500/350C DUV stepper | G2 | eo:li2026ba:p3; eo:cai2025:p13; eo:lin2025:p12 | 8 |
| Heidelberg Instruments | MLA 150, MLA 300, DWL 66 | G2 | eo:multani2025:p17; eo:valdez2023a:p3; eo:didier2026:p7; pk:ectc51846.2026.00199:p4 | 12 |
| Oxford Instruments | PlasmaPro 100, ICP380 | G3 | eo:didier2026:p7; eo:tiberi2025:p9 | 5 |
| PlasmaTherm | Versaline HDP-CVD, ICP RIE | G3/G4 | eo:multani2025:p17 | 1 |
| SAMCO | NR10 etcher | G3 | eo:mao2024:p6; eo:lu2020:p7 | 3 |
| SPTS | Omega fxP ICP (pk) | G3 | eo:li2026ba:p3; eo:soma2025:p11; pk:ectc51906.2022.00244:p7 | 5 |
| Intlvac | ion beam mill | G3 | eo:multani2025:p17 | 1 |
| Veeco / Cambridge NanoTech | Fiji PE-ALD, Savannah ALD | G4 | eo:tiberi2025:p9; eo:sun2026a:p25 | 3-5 |
| Denton, AJA, Kurt J. Lesker, ULVAC, Moorfield | evaporators / sputter | G4 | eo:gaier2025:p13; eo:berman2026:p8; eo:multani2025:p17; eo:tiberi2025:p9 | 1-4 each |
| DISCO | DAD 3221 / DAD3220 / DAD3360 / DAD3361 dicing; DAG810 grinder; DFD6860; DGP8761 | G5 | eo:didier2026:p7; pk:ectc51529.2024.00155:p2; pk:ectc51687.2025.00027:p2 | 11 |
| Applied Materials | Reflexion LK Prime CMP, Producer, Endura | G4/G5 | pk data/process_steps.csv; pk:ectc51909.2023.00190:p1 | 9 (pk) |
| Ebara, Okamoto (GNX200BH), Logitech, Allied (MultiPrep) | CMP / grind / lap / polish | G5 | pk:ectc51529.2024.00155:p7; pk:001c.147098:p3; pk:ectc51846.2026.00202:p3; eo:didier2026:p7 | 1-6 |
| Resists: Dow/Corning HSQ (FOX-16, XR-1561), Zeon ZEP520A, micro resist ma-N 2403/2405, Allresist CSAR / AR-P 6200, PMMA 495K, AZ (4620, 5214, 2070), SPR3612 / SPR220 / S1813 | (vendor often not stated) | G6 | eo:he2019:p8; eo:sun2026a:p25; eo:berman2026:p8; eo:witmer2020:p5; eo:lee2020:p12; eo:feng2022:p9; eo:multani2025:p17 | HSQ 17, ZEP 7, AZ 8 |
| J.A. Woollam | M-2000(XI) ellipsometer | G7 | eo:suceava2025:p22; pk:ectc51846.2026.00416:p2 | 3 |
| Bruker, Asylum, Park | AFM / profilometry | G7 | pk:ectc51529.2024.00396:p2; eo:tian2026:p5 | 1-2 |
| FEI / Thermo Fisher, Tescan, Zeiss, Hitachi High-Tech | SEM / FIB / TEM | G7 | eo:suceava2025:p9; eo:sun2026a:p14; pk:ectc51909.2023.00155:p4 | 1-9 |
| Keyence | VX3600 laser confocal | G7 | pk:ectc51909.2023.00298:p3 | 13 (pk) |
| Nordson (Dage) | 4000 Plus bond tester; XD7600 X-ray CT | G7/I3 | blog:Micro-integrated_optical_systems...:p5; pk:ectc51529.2024.00155:p3 | 8 |
| Rigaku, Malvern Panalytical, Horiba, IONTOF | XRD / Raman / ToF-SIMS | G7 | eo:tian2026:p5-6; eo:suceava2025:p8; eo:falcone2026:p8 | 1-2 |

### 3.8 Characterization instruments (H)

| vendor | product/model [model docs] | cat | locators | n |
|---|---|---|---|---|
| Keysight (incl. Agilent, HP lineage) | M8199A/B AWG [66]; M8194A [21]; M8195A [8]; M8196A [5]; UXR (0594A/AP, 0702AP, 0704A, 1004A, 1104A) [32]; PNA/PNA-X N5225B/N5227A/B/N5245B/N5247A/B [36]; N1000A DCA [16]; N1030A [10]; N1032A [11]; N1046A [3]; DCA-X 86100D [10]; N4372B/E, N4373E LCA [14]; N7776C/N7778C/81600B/81608A/81940A TLS [12]; N7744A/C, N7745C, 8163A, 81634B power meters [7]; N7786B/C, N7788C pol. [3]; E8257D, E8267D, N5183B sig gen [5]; B2900-series SMU [7]; N9030A, N9020 [3]; N9917A FieldFox [3]; E36313A [1]; E5080B, P5004A VNA; 81110A pulse gen | H1-H12 | eo:aihara2026:p2; eo:mao2024:p7; eo:valdez2023a:p10; eo:tiberi2025:p14; eo:berman2026:p9 | 200 (109/13/78/0) |
| HP (legacy) | 4142B, 81689A, 8562A | H12/H1 | ofc2026:Th1A.3:p1; eo:suceava2025:p9; eo:hsu2024:p13 | 8 |
| Anritsu | MS4647B / MS4640B VectorStar [8]; ME7838AX [5]; MN4765B(-0072) O/E module [8]; MG3697C / MG369C [3]; MP1800A, MP1900A, MP1763B [4]; MS9740B OSA [1] | H5/H6/H2 | eo:mao2024:p7; eo:li2026:p2; eo:chen2024:p10; eo:larocque2024:p23; eo:gaier2025:p13 | 24 |
| Rohde & Schwarz | SMA100B, SGS100A, SMU200A, SMW200A; ZNA26/50/67, ZNB20; FSW26/43/85; NRP110T; RTA4004 | H5/H17/H7 | eo:valdez2023a:p11; eo:multani2025:p47; eo:didier2026:p8; eo:chen2024:p10 | 19 |
| Tektronix (incl. Keithley) | DPO73304, DPO75902SX, DPO77002SX, DSA8300, MDO4104C, MSO64B; AWG7102; AFG31252; Keithley 2400/2450 SMU | H7/H6/H12 | eo:didier2026:p8; eo:han2023:p8; eo:bankwitz2026:p19; eo:sun2026a:p16 | 13 + Keithley 10 |
| Teledyne LeCroy | real-time scope | H7 | eo:wu2025:p12; eo:chen2022:p8 | 4 |
| Active Technologies | ARB Rider AWG-7204 | H6 | eo:didier2026:p8 | 1 |
| Micram | DAC4 / DAC10004 / DAC1002 | H6 | eo:tiberi2025:p14; eo:chen2022:p8; eo:guo2026:p13 | 7 |
| SHF | S807 / S807C, S804B amplifiers [21]; SHF 827 / M827B [4]; BT110R/B, BT65R bias tees [6]; T850C linear driver; 12104A BERT [4]; C603B 2:1 MUX [3] | H8/H6 | eo:mao2024:p7; eo:chen2024:p6; eo:han2023:p8; eo:cai2025:p6 | 44 |
| MultiLane | ML4039E BERT | H6 | eo:singer2025:p7 | 3 |
| Thorlabs | RXM38AF/40AF/42AF photoreceivers; DET01CFC/08CFC; PDFA100 PDFA; EDFA100S; BOA785S SOA; S120VC/S121C/S142C/S154C sensors; PM100U; FPC560/561; MAX313D NanoMax; MX40A microwave amp; HVA200; OSA305; FDS1010-CAL | H4/H10/H3/H11/H13/H8/H2 | eo:bankwitz2026:p20; eo:hsu2024:p13; eo:liu2026d:p4; eo:valdez2023a:p4; eo:didier2026:p7-8; eo:sun2026a:p16 | 39 |
| Santec | TSL-510 / 550 / 570 / 710 / 770 [46]; MPM-200/210/210H/215/220 [5]; OTF-350 [1] | H1/H3/H11 | eo:sun2026a:p14; eo:berman2026:p9; eo:multani2025:p16; eo:mao2024:p6 | 44 |
| EXFO | T100S / T200S / T500S [6]; CTP10 [4]; XTA-50, XTM-50 [3]; IQS-2800, FTB-2250 | H1/H11 | eo:zhang2023:p9; eo:zheng2026:p7; eo:steckler2025:p8 | 12 |
| Yokogawa / Ando | AQ6370 (B/D/E), AQ6373E, AQ6374, AQ6375E, AQ6331, AQ6317B [13] | H2 | eo:multani2025:p43; eo:chen2024:p6; eo:valdez2023a:p4 | 11 |
| Finisar / II-VI / Coherent | XPDV2120R, XPDV3120R, XPDV4120R, XPDV4121R, XPD3120R [27]; BPDV3320R / 4120R [3]; WaveShaper 15000S [2] | H4/H11 | eo:ummethala2021:p5; eo:tiberi2025:p14; eo:hulyal2026:p3 | 26 + WaveShaper 11 |
| Newport / New Focus (MKS) | 1014, 1024, 1471, 1544(A), 1623 detectors; TBF-1550 filter | H4/H11 | eo:li2020:p4; eo:celik2022:p6; eo:chen2024:p10; eo:valdez2023a:p4; eo:berman2026:p9 | 21 + 7 |
| Optilab | PD-40-M, APR-10 | H4 | eo:multani2025:p44; eo:li2025b:p4 | 2 |
| Hamamatsu | C5658 APD module (1 GHz); C12741-03 InGaAs camera | H4 | ofc2026:Th1G.3:p2; ofc2026:W1F.3:pNA | 2 |
| GGB Industries | Picoprobe 40A, 67A, Model 110 | H9 | eo:valdez2023a:p4; eo:berman2026:p9; eo:sun2026a:p16 | 16 |
| FormFactor (Cascade Microtech) | Infinity I67-A-GSG, I110, GS Infinity; ACP40, ACP-65; CM300xi-SiPh station | H9 | eo:mao2024:p7; eo:ummethala2021:p13; eo:lu2020:p8; eo:sabatti2024:p2; ofc2026:Tu2D.5:pNA | 15 |
| MPI | T110A-GSG0100 probes; TS2000 station | H9 | eo:li2026:p2; eo:li2026ba:p4; eo:zheng2026:p7 | 4 |
| Virginia Diodes | VNAX WR6.5/WR3.4 extenders; WR9.0+WR2.8 source | H5 | eo:chelladurai2025:p9; eo:gaier2025:p13 | 4 |
| OML | RF extender | H5 | eo:multani2025:p47 | 1 |
| Centellax, Mini-Circuits (ZX85-12G-S+, ZHL-42W), Fairview (FMAM513) | RF amps / bias tee | H8 | eo:ummethala2021:p5; eo:sun2026a:p16; ofc2026:Th1G.3:p2; eo:didier2026:p8 | 1-4 |
| Amonics | AEDFA-40, AEDFA-L-30-B-FA EDFA | H10 | eo:mao2024:p7; eo:zhang2024:p12; eo:chen2024:p8 | 5 |
| Keopsys | EDFA | H10 | eo:chen2023a:p9; eo:tan2024:p7 | 4 |
| PriTel | LNFA-33 | H10 | eo:bankwitz2026:p19 | 1 |
| Toptica, NKT Photonics (Koheras E15/X15), Spectra-Physics, M Squared | CW / pulsed lasers | H1 | eo:berman2026:p8; ofc2026:M3J.2:p2; eo:suceava2025:p9 | 2-5 |
| Luna | OBR 6415, OVA 5000 | H16 | eo:nelan2022:p5; ofc2026:Th3D.3:p2 | 2 |
| Swabian Instruments | Time Tagger Ultra | H15 | eo:bankwitz2026:p21; ofc2026:Tu2K.3:p2 | 4 |
| Single Quantum | SNSPD | H15 | eo:zhu2022:p6; ofc2026:Tu2K.3:p2 | 2 |
| Stanford Research Systems | SR830 / SR865A lock-in; LDC501/502, PTC10 | H17 | eo:suceava2025:p9; eo:li2025b:p4; blog:ao-64-30-9049-...:p3,p5 | 2-3 |
| Montana Instruments | S200 Cryostation | H14 | eo:anderson2025:p8; eo:multani2025:p43 | 3 |
| Bluefors | LD400 | H14 | eo:mohl2025:p21; pk:ectc51909.2023.00316:p5 | 2 |
| attocube, Lake Shore | cryo positioners / controllers | H13/H14 | eo:khalil2026:p9; eo:hsu2024:p19 | 1-3 |
| Novoptel / EPS (as written "EPS PM1000") | polarimeter | H11 | ofc2026:M4J.4:pNA | 1 |

### 3.9 Software (J)

| vendor | product | locators | n |
|---|---|---|---|
| Ansys | Lumerical, HFSS (regex group) | eo:cai2025:p14; eo:sun2026:p2; eo:lotkov2024:p5 | 86 |
| COMSOL | Multiphysics | eo:celik2022:p3; eo:cai2025:p13 | 41 |
| Dassault | CST | eo:ummethala2021:p5; eo:mao2022:p4 | 7 |
| Keysight | ADS, PathWave EM Design | eo:saxena2023:p4; eo:valdez2023a:p1 | 7 |
| Cadence | - | eo:saxena2023:p1; eo:kawahara2025:p7 | 9 |
| Synopsys | RSoft / OptoDesigner (regex group) | eo:thiele2022:p5; eo:gong2026:p2 | 6 |
| Flexcompute | Tidy3D | eo:sun2026a:p12 | 1 |
| Photon Design | FIMMWAVE | eo:heidari2022:p3 | 1 |
| Sonnet, KLayout, VPIphotonics | - | eo:witmer2020:p26; eo:kawahara2025:p7; ofc2026:W4F.5:p2 | 1 each |

### 3.10 Reliability standards (I) observed

| standard | cited for | locators |
|---|---|---|
| Telcordia GR-468 (non-powered, adapted) | TC, DH, HTS, LTS of fiber attach | pk:ectc51906.2022.00072:p2,p6 |
| Telcordia GR-63-CORE | thermal/airflow reference for ELSFP case temp | blog:OIF-ELSFP-02.0-1:p47 |
| MIL-STD-883 (L, G) TM 1010.8, 2002 B, 2019.9, 2026F | TC, shock, die shear, vibration | blog:Micro-integrated_optical_systems...:p4-5; pk:ectc51687.2025.00012:p5; pk:ectc51687.2025.00142 (metrics.csv) |
| ESCC 23201 | adhesive qualification for space | blog:Micro-integrated_optical_systems...:p4 |
| IEC 61300-3-4 | IL measurement | pk:ectc51687.2025.00012:p2 |
| IEC 60825-1 / -2 | laser safety (ELS) | blog:OIF-Co-Packaging-FD-01.0:p20; blog:OIF-ELSFP-02.0-1:p10 |
| IEC 61754-7-1/-2, IEC 61755-3-31, TIA-604-5 | MT ferrules | blog:OIF-ELSFP-02.0-1:p33 |
| IEC 60794-3 | PMD link design value | blog:corning-smf-28-ultra-specifications:p1 |
| ITU-T G.652.D, G.657.A1 | fiber class | blog:corning-smf-28-ultra-specifications:p1 |
| JEDEC JESD22-A104F, A103(E), A118(B), A113D, B110A, JESD47K, J-STD-020(E) | package TC/HTS/uHAST/MSL | pk data/metrics.csv test_standard (e.g. pk:ectc51687.2025.00027 p6 Table VI; pk:tcpmt.2026.3672227 p7 Table II) |
| AEC-Q100 / Q104, IPC-9701A, ASTM D5470, ISO 2409 / ASTM D3359 | automotive qual, board TC, TIM Rth, adhesion | pk data/metrics.csv (pk:ectc51846.2026.00073 p6; pk:ectc51846.2026.00274 p3; pk:ectc51687.2025.00055 p2) |
| DIN EN ISO 10365 | adhesive failure modes | blog:Micro-integrated_optical_systems...:p5 |

## 4. Proposed tables (schema sketch)

Conventions reused from the EO atlas: `org_name` = organization's own preferred English name with `ror_id`/`name_source` (devices.schema.yaml rule (e)); `paper_id` from papers.csv (other corpora prefixed `pk:` / `ofc2026:` / `blog:`); locators "p.N" PDF page index + "Fig."/"Table"; evidence entries with `basis`; `qualifiers` field:gt|lt|approx; ISO dates; `verified_on`.

**organizations.csv (extend, do not fork)**: add org_type values `wafer_supplier`, `materials_supplier`, `equipment_vendor`, `instrument_vendor`, `component_vendor`, `software_vendor`, `osat`, `standards_body`; add columns `aliases` (pipe list, e.g. `Agilent|Keysight`), `lineage` (e.g. `Finisar -> II-VI -> Coherent`; `Cascade Microtech -> FormFactor`; `New Focus -> Newport -> MKS`; lineage entries need a source), `website`.

**vendors_roles.csv**: `org_name, category_id, role (supplier|foundry|broker|osat|tool_vendor), first_seen_paper, n_papers, basis, notes, verified_on`.

**products.csv**: `product_id` (slug `keysight-m8199b`), `org_name`, `product_line`, `model`, `model_regex` (for extraction), `category_id`, `product_type`, `status` (active|discontinued|N/A), `datasheet_ref` (local cache path), `datasheet_access` (public|registration|paywalled|N/A), `notes`, `verified_on`.

**product_specs.csv (long format)**: `product_id, field, value, value_max, unit, condition (lambda, T, f), qualifier, basis (datasheet_spec|datasheet_typical|stated_in_paper|measured|derived), source (datasheet_ref or paper_id), locator, verified_on, notes`.

**product_usage.csv (paper link)**: `usage_id, paper_id, corpus (eo|pk|ofc2026|blog), device_id (optional, devices.csv), org_name, product_id (empty if model not stated), role (fab_tool|substrate|test_instrument|packaging_material|assembly_tool|foundry_process|fiber_component|software), stated_text (<=200 chars verbatim), stated_spec (e.g. "110 GHz"), locator, extraction (auto_regex|auto_sentence|manual), basis (stated|inferred_from_model), verified_on`.

**foundry_processes.csv**: `process_id, org_name, platform (SiPh|SiN|TFLN|InP|BTO|...), wafer_mm, litho, pdk_name, access_route (MPW|dedicated|broker), broker_org, building_blocks (list), pdk_open (bool), source, locator`. Link from papers.csv `foundry_or_fab` / `process_name` (populated for 97 EO papers in `foundry_or_fab` and 151 in `process_name`; corrected 2026-10-20 per audit).

**standards.csv + reliability_tests.csv**: `standard_id (e.g. Telcordia GR-468-CORE), body, edition, scope, access`; tests: `paper_id, tv_or_device_id, standard_id, method/condition, t_min_c, t_max_c, cycles, dwell_min, duration_h, rh_pct, dose, pass_criterion, result, n_samples, locator, basis` (mirrors packaging-atlas metrics.csv `test_standard`).

**category_tree.yaml**: ids and labels of Section 1.

Auto-extraction vs datasheet:

| data | auto from methods (precision) | needs datasheet / vendor |
|---|---|---|
| vendor + model of instruments | high (parenthetical "(model, vendor)" and model regex) | - |
| as-used instrument specs (BW, GSa/s, probe GHz) | medium (stated next to model) | full spec sheet |
| wafer supplier + stack | high for TFLN (NanoLN in 46 docs) | uniformity, TTV, price |
| foundry + PDK name | high (papers.csv already) | BB library, rules, cost, cadence |
| fab tools | high in arXiv methods | throughput, resolution specs |
| adhesives / underfill / FAU | low (often anonymized) | index, Tg, CTE, shrinkage, outgassing, cure |
| laser die for CPO / ELS | low (in-house or unnamed) | power vs T, RIN, aging, FIT |
| reliability conditions | high in pk (metrics.csv) | standard text itself |

Vendor-name normalization needed: Agilent/Keysight/HP, Finisar/II-VI/Coherent, Cascade Microtech/FormFactor, New Focus/Newport, Raith/Vistec (EBPG 5200 attributed to both: eo:tiberi2025:p9 vs eo:shen2025:p4), "Rhode & Schwartz" misspelling (eo:multani2025:p47), "NONOLN" (papers.csv), Ando/Yokogawa (AQ6317B, eo:valdez2023a:p4), Dow/DuPont (CYCLOTENE stated as DuPont, pk:3dic63395.2024.10830178:p1).

## 5. Gaps

| gap | evidence of gap | where to get it | access |
|---|---|---|---|
| optical / structural adhesives (index, Tg, CTE, modulus, shrinkage, outgassing, cure) | anonymized in CPO and space-qual papers (pk:ectc51687.2025.00012:p2; pk:ectc51906.2022.00072:p5; blog:Micro-integrated_optical_systems...:p4) | Dymax, Norland, EPO-TEK, DELO, Panacol, NTT-AT datasheets; NASA outgassing DB | vendor datasheets usually public (to verify per vendor) |
| FAU, V-groove arrays, MT/MPO, blindmate connectors | FAU "from different suppliers" unnamed (pk:ectc51687.2025.00012:p2); connector firms only in OIF member list (blog:OIF-ELSFP-02.0-1:p61) | US Conec, Senko, Fujikura, Molex, Sumitomo product pages; TIA-604-5, IEC 61754 | product pages public; IEC/TIA paywalled |
| laser die / ELS module specs (P vs T, RIN, SMSR, aging, FIT) | only Furukawa OFC papers (paywalled) and Intel deck; OIF leaves per-application specs open (blog:OIF-ELSFP-02.0-1:p35) | vendor product briefs; ELSFP CMIS IA | mixed |
| PDK building-block values, MPW cost, cadence, design rules | only flyers/OFC summaries (blog:20210910_Foundry-services...; ofc2026:Tu2D.3) | Europractice, JePPIX, AIM, AMF, LIGENTEC, Luxtelligence (lnoi400 PDK, eo:kari2025:p4) | some public, many NDA |
| wafer specs (LNOI thickness uniformity, TTV, bow, defect density; SOI grades) | papers state only stack | NanoLN, Partow, Soitec, Shin-Etsu datasheets | public product pages (to verify) |
| packaging and test equipment specs (placement accuracy, UPH, alignment speed) | only names (ficonTEC AL1200, Finetech FEMTO2) | vendor datasheets | public brochures usually |
| TEC / thermistor / micro-optics / isolators / VHBG | custom or unnamed (blog:ao-64-30-9049-...:p2-3) | vendor catalogs | public |
| instrument full specs (TLS linewidth, sweep, OSA dynamic range, VNA DR) | papers state only model, sometimes BW | Keysight, Santec, Anritsu, R&S, Yokogawa datasheets | public |
| reliability standard texts (GR-468, JEDEC, MIL-STD-883, ESCC, IEC) | only cited | Telcordia (paywalled); JEDEC (free download with registration for many docs, to verify); MIL-STD-883 (DLA ASSIST, to verify); ESCC (ESA ESCIES, to verify); IEC (paywalled) | mixed |
| pricing, lead time, capacity, market share | none in corpus | Soitec URD gives product lines (blog:soitec-urd:p5,p27); vendor financial filings | public filings |

## 6. Next steps (not executed)

- [ ] Decide org_type extensions and whether `products`/`product_usage` live in eo-modulator-atlas or a new repo.
- [ ] Turn scratch `vendors.py` + model registry into a repo script (dry-run, JSONL output, skip-existing), pilot on 10 diverse EO papers, audit.
- [ ] Backfill product_usage for the 231 EO papers from methods sentences; link to devices.csv (instrument BW ceilings vs bw_measured_to_ghz).
- [ ] Datasheet harvest plan (rate-limited, public PDFs only) for top 30 products by usage.
- [ ] Fresh-context audit of Section 3 locators.

Scratch artifacts (not committed; copies of the scripts are in the git-ignored `DevLog/research/scripts_2026-10-20/supply/`) (`vendors.py`, `modelreg.py`, `hits.json`, `usage_sent.json`, `models.json`, `usage_table.tsv`, `blog/*.md`).
