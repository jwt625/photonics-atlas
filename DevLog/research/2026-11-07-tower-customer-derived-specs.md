# Tower SiPh building blocks inferred from customer product specs (2026-11-07)

Purpose: fill the thin Tower column of the foundry PDK benchmark (DevLog-014) from public specs of products that a
primary source says are made on Tower silicon photonics. Builds on `2026-11-07-tower-siph-customers-and-perf.md`
(26 customers / partners). Companion data: `2026-11-07-tower-customer-derived-values.csv` (30 rows, `tcd01`-`tcd30`).

Method and limits:
- WebSearch / WebFetch only, about 115 web calls (two parallel streams plus checks).
- Hosts that returned 403 and were dropped: umc.com, businesswire.com, docsend.com, globenewswire.com,
  ir.towerjazz.com.
- The owner's local OFC 2026 full-text corpus was grepped for papers by the customers below. The only hit with Tower
  relevance was Th4A.4, which is already in the repo.
- Kinds used in the CSV:
  - `direct_spec`: the source states the number for the component.
  - `bound`: an inequality, or a quantity limited by the measurement.
  - `inference`: needs an assumption or arithmetic.
- "Figure read" means read by eye from a slide plot. These values must be digitized before ingest.
- No row uses a data rate to stand in for a bandwidth. Data-rate-only cases are kept as N/A rows so the gap is
  visible.

## 1. What "SiLith" is

- **Identity.** SILITH Technology Pte. Ltd. (printed "Silith Technology" in OFC 2026 M1E.3), 8 Cleantech Loop,
  Singapore. It is a silicon photonics PIC design company:
  - founded 2021;
  - "cumulative shipments of more than 8 million 100G/lane and 200G/lane PICs";
  - has a 1.6T platform and is developing a 400G/lane all-Si MZM platform.
  - Sources: SILITH / UMC press release, 2026-07-13/14, via Design & Reuse
    (https://www.design-reuse.com/news/202530817-silith-and-umc-achieve-mass-production-milestone-for-silicon-photonics/),
    and Mark LaPedus, 2026-07-16 (https://marklapedus.substack.com/p/tower-umc-expand-efforts-in-silicon).
- **Public foundry is UMC, not Tower.** UMC's Singapore 12-inch fab delivered SILITH's first mass-production
  silicon photonics wafers (2026-07). No public source found ties SILITH to Tower.
  - The press release does not say where the earlier 8 million PICs were made.
  - Saying they came from Tower would be a guess, so the SILITH OFC 2026 M1E.3 values (heater P_pi 12 mW, edge
    coupling ~1.5 dB per facet, PD RF bandwidth > 40 GHz, C band) are NOT used for Tower.
  - PitchBook lists a SiLith Technology in Suzhou. Whether this is the same group is unresolved.
- **Close-name matches checked:**
  - SiLC Technologies (FMCW LiDAR chip): no Tower link found; UMC Capital is an investor.
  - LightIC Technologies (FMCW LiDAR): Tower-confirmed (Tower PR 2026-01-05), but no numeric specs are public.
  - If the owner meant a different company, its name or a link is needed.

## 2. Customers with a verified Tower link and usable public specs

| Customer | Product | Tower link (primary or close to primary) | Platform |
|---|---|---|---|
| OpenLight | 3.2T / 1.6T DR8 PICs; PDK test PASICs | PR 2026-03-10: "Fabricated on Tower Semiconductor's PH18DA process"; eeNews 2024-11-07: "The only foundry that OpenLight's process is installed at is Tower." | PH18DA |
| NewPhotonics | NPG102 / NPG10204 / NPG10240 | Photonics Online 2026-03-05 (first OpenLight customer in volume on PH18DA); Tower PR 2026-09-17. NewPhotonics' own pages do not name Tower | PH18DA |
| Coherent | 400G/lane Si MZM prototype | Tower PR 2026-03-23 (Si modulator in a "production-ready SiPho process", 420 Gb/s PAM4, "presented last week at OFC"). No platform named | PH18 or PH45 (not stated) |
| Scintil Photonics | LEAF Light DWDM laser source | Gazettabyte 2025-11-13: "Production leverages Tower Semiconductor's PH18 silicon-photonics platform"; Convergedigest 2026-02-17: "Fabricated on Tower's PH18M" | PH18M Si wafer plus Scintil's own III-V (SHIP), not PH18DA / DB |
| Anello Photonics | ULL SiN process | Tower PR 2021-11-01 | SiN (process name not given) |
| Alcyon Photonics | PH18M building-block IP library | Tower PR 2025-03-25; Alcyon news 2026-09-10 ("Tower Semiconductor-qualified photonic IP library") | PH18M |

Customers verified as Tower, but with no component-level public number (data rate, system power or qualitative only):

| Customer | What is public |
|---|---|
| Alpine Optoelectronics | nCP4: 4 x 56 GBd, 400G DR4. Qualitative: "efficient edge coupler", "high OE bandwidth" |
| Inphi / Marvell | COLORZ 100G DWDM (PH18); "five million coherent PICs" |
| InnoLight | 400G / 800G on PH18M; NPO on PH18M and 300 mm |
| Teramount | PH18 "Bump-ready" wafers, no dB values. Its 0.5 dB / +/-30 um tolerance figure is tied to GlobalFoundries |
| Xscape | ChromX on PH18: "CWDM and DWDM grids" only |
| Quintessent | PH18DB: no laser numbers in any Tower-linked source |
| Salience Labs | OC-32M "insertion loss below 2 dB" (secondary source, Unite.ai 2026-10-14), not tied to Tower in that source; excluded |
| Oriole, LightIC, Xanadu | No numbers |
| NLM Photonics | SOH modulators on a PH18M MPW (NLM release 2026-03-16), no measured numbers. A ">110 GHz" claim appears only in secondary coverage and is not tied to PH18M |

DustPhotonics (and Credo, which agreed to acquire it) is excluded: Tower appears as its foundry only in secondary
sources.

## 3. Derived component values (strongest first)

### Facts: direct statements in a source that names Tower

| Benchmark row | Value | Chain | Source (date) | Confidence |
|---|---|---|---|---|
| eam_bw | approaching 100 GHz, differential 3 dB | OpenLight PR: 448G InP EAM "differential 3 dB bandwidth approaching 100GHz". The same PR says it is fabricated on PH18DA | OpenLight PR (2026-03-10) | high for attribution; medium for value. Die vs packaged and de-embedding not stated |
| (eam_er) | > 3.5 dB at 2.0 Vppd | same PR | 2026-03-10 | as above |
| (III-V to Si coupling) | ~90 % | same PR; eeNews: loss "of the order of 10 percent" | 2026-03-10; 2024-11-07 | medium |
| wg_loss (SiN) | approaches 0.005 dB/cm, 1550 nm, bend radius < 1 mm | Tower / Anello process claim | Tower PR (2021-11-01) | process claim, not a measured distribution |
| ring_qi (SiN) | > 100 M | same PR | 2021-11-01 | intrinsic vs loaded not stated |
| (laser power, Scintil) | up to 20 mW per carrier; better than +/-10 GHz grid accuracy; 8 x 200 GHz or 16 x 100 GHz | Scintil interview. The laser is Scintil's III-V on a Tower PH18 wafer | Gazettabyte (2025-11-13) | medium. Reference plane not stated; not a Tower laser process |
| (CWDM robustness, Alcyon) | channel drift < 3 nm with up to 30 nm fabrication variation | Tower PR. Component not named | 2025-03-25 | low (component unknown) |

### Facts with an attribution assumption: measured, but the source does not name Tower

| Benchmark row | Value | Chain | Assumption | Source |
|---|---|---|---|---|
| mzm_bw | > 70 GHz EO 3 dB (Si TW MZM, lateral PN, 220 nm Si, 2.8 um Al, 75 ohm differential) | Tower PR says Coherent's Si modulator was fabricated in Tower SiPh and presented at OFC. The OFC 2026 Th4A.4 paper by Coherent authors (Si MZM, 420 Gb/s PAM4) measures > 70 GHz | Th4A.4 is the paper the PR refers to (no paper number in the PR). Platform PH18 vs PH45 unknown | OFC 2026 Th4A.4; Tower PR 2026-03-23 |
| laser_power (PH18DA DFB) | 35 mW max at 200 mA (on-chip, tap monitor PD) | SWTest slide 6 table | OpenLight wafers are Tower PH18DA (eeNews: Tower is the only foundry). The deck says only "8" wafers via commercial CMOS foundry" | OpenLight SWTest deck (2026-06-08) |
| laser_power (PH18DA tunable ring laser) | 30 mW max at 200 mA, tunable over 35 nm | slide 6 | same | same |

### Estimates: figure reads from the SWTest 2026 deck (same attribution assumption)

| Row | Value | Chain |
|---|---|---|
| laser threshold (1.6T PASIC DFB) | ~78-80 mA | slide 9 LIV, 4 lanes |
| laser power at 200 mA | ~19-20 mW (slope ~0.16 mW/mA) | slide 9. Conflicts with the 35 mW table value: a different DFB design or reference plane; unresolved |
| laser SMSR | >= ~45-50 dB (bound) | slide 13: peak ~-17 dBm vs highest side feature ~-66 dBm. The floor may be ASE or the OSA |
| eam IL (static) | ~0.7-0.8 dB at 0 V | slide 10 |
| SOA gain | ~9-10 dB at ~98 mA | slide 11 |
| CWDM mux IL | ~4.2-6.2 dB per channel; 3 dB passband ~15-17 nm | slide 16. Mux type not stated, so not mapped to awg_il |
| to_ppi | ~35-40 mW (inference) | slide 17: 2 pi heater period ~74 mW on an AMZI, so P_pi = period / 2. Same slide: AMZI IL ~1-1.5 dB, ER ~21-28 dB |

### Not derivable (N/A)

| Row | Why |
|---|---|
| mzm_vpil | Th4A.4 gives effective Vpi ~7 V (VpiL / length); the length is not printed |
| pd_resp, pd_bw, pd_dark | No Tower customer states on-chip Ge PD numbers. Th4A.4 used external PDs. OpenLight PDK says only "High-speed PDs 100G, 200G" |
| edge_il, gc_il | No Tower-tied dB value. The SWTest grating reading is at a ~400 um fiber standoff, so it is not an IL |
| mmi_el, crossing, awg_il / awg_xt, bend_loss, wg_loss (Si) | No numbers. The Alcyon PH18M library has no public performance figures; its Tower white papers are on DocSend (403) |
| ring_mod_bw | No product found |
| eam_bw / mzm_bw from data rates | NewPhotonics 224G PAM4 and Alpine 56 GBd lanes: a data rate does not fix a 3 dB bandwidth, so no bound is given |
| laser linewidth, RIN | Not stated in any customer product source. The only Tower-tied value is literature: OpenLight 8 kHz (JLT 2025 abstract) |

## 4. What would turn each into a literature value

- **EAM ~100 GHz (PH18DA).** Needs a paper or datasheet with the S21 plot, the bias and the measurement plane.
  - Candidates: OpenLight OFC 2026 / ECOC 2026 EAM papers; Ostrovskis JLT 2025.
  - Check that the paper text names Tower or PH18DA.
- **Si MZM > 70 GHz.** Needs Th4A.4 or a follow-up paper to name the foundry, or a Coherent statement linking Th4A.4
  to Tower by paper number. VpiL needs the phase-shifter length.
- **PH18DA DFB, TRL, SOA, mux, AMZI.** Digitize the SWTest slides only if the owner accepts the eeNews-based foundry
  attribution. Better: a written OpenLight paper with the same data that names PH18DA.
  - Shi et al., ISLC 2024: the abstract names "PH18DA at Tower".
  - Norberg et al., JLT 2025.
- **Scintil LEAF Light power.** Needs a datasheet or paper giving the reference plane, temperature, SMSR and RIN.
- **Alcyon PH18M blocks.** Needs the Alcyon "Tower" white papers (DocSend, needs a browser) or the Luceda IPKISS
  library documentation. These would be the only public MMI / CWDM / PSR numbers on PH18M.
- **Ge PD.** Nothing on the customer side. The GFP 2018 TowerJazz paper (10.1109/group4.2018.8478742) remains the
  only lead.

## 5. Papers or documents by these customers naming Tower (or PH18x) with component data, for ingestion

| Item | ID | Names Tower in text? | Data | Access |
|---|---|---|---|---|
| Shi et al., DFB lasers in an open-market SiPh platform (ISLC 2024) | 10.1109/ISLC57752.2024.10717410 | yes (abstract: PH18DA at Tower) | DFB threshold / power / SMSR expected | closed IEEE |
| Norberg et al., heterogeneous laser sources in an open-access PDK (JLT 2025) | 10.1109/JLT.2025.3554392 | to check | DFB > 40 mW, tunable 8 kHz | closed IEEE |
| Ostrovskis et al., heterogeneous InP EAM beyond 300 Gb/s (JLT 2025) | 10.1109/JLT.2025.3526822 | to check | EAM bandwidth, IL | closed IEEE |
| Dong et al. (Coherent), 400G/lane Si MZM (OFC 2026 Th4A.4) | ofc2026:Th4A.4 (in repo) | no (Tower only via PR 2026-03-23) | MZM > 70 GHz | owner corpus |
| Xiang et al. (UCSB / Anello / Caltech), Nature 620 (2023) | 10.1038/s41586-023-06251-w | yes (Methods) | SiN loss / Q / transition | OA |
| Barnard et al. (OpenLight), SWTest 2026 slides | https://www.swtest.org/library/2026proc/pdf/M01_02_BARNARD_SWTest-2026.pdf | no (Tower via eeNews) | DFB / TRL / FP power, LIV, SMSR, EAM, SOA, mux, AMZI plots | open PDF; not peer-reviewed, no DOI |

No new customer paper naming Tower as fab was found beyond those already listed in the earlier Tower doc. Searches
returned nothing for Scintil, Quintessent, NewPhotonics, Xscape, InnoLight, Alcyon or Teramount.

## 6. Sources (date accessed 2026-11-07)

| Source | URL |
|---|---|
| OpenLight PR, 2026-03-10 | https://openlightphotonics.com/newsroom/openlight-introduces-3-2t-dr8-silicon-photonics-pics-as-well-as-1-6t-dr8-lro-and-lpo-variants |
| eeNews, 2024-11-07 | https://www.eenewseurope.com/en/openlight-proliferates-pdks-to-address-photonic-ic-markets/ |
| OpenLight SWTest deck, 2026-06-08..10 | https://www.swtest.org/library/2026proc/pdf/M01_02_BARNARD_SWTest-2026.pdf |
| Tower / Coherent PR, 2026-03-23 | https://towersemi.com/2026/03/23/03232026/ |
| Gazettabyte, Scintil, 2025-11-13 | https://gazettabyte.com/?p=146180 |
| Convergedigest, Tower / Scintil, 2026-02-17 | https://convergedigest.com/tower-and-scintil-roll-out-first-heterogeneous-dwdm-lasers/?amp=1 |
| Photonics Online, OpenLight / NewPhotonics, 2026-03-05 | https://www.photonicsonline.com/doc/openlight-receives-first-volume-production-orders-for-newphotonics-g-and-t-laser-integrated-pics-with-tower-semiconductor-0001 |
| NewPhotonics NPG10204 page (undated) | https://newphotonics.com/npg10204-pic-chip-for-dsp-modules/ |
| Tower / Anello PR, 2021-11-01 | https://towersemi.com/2021/11/01/11012021/ |
| Tower / Alcyon PR, 2025-03-25 | https://towersemi.com/2025/03/25/03252025/ |
| Alcyon catalog (undated) | https://alcyonphotonics.com/solution/ |
| Tower / Alpine PR, 2020-12-29 | https://towersemi.com/2020/12/29/12292021/ |
| NLM Photonics release, 2026-03-16 | https://www.nlmphotonics.com/?p=5258 |
