---
title: Fresh-context audit of P0 - data correctness
date: 2026-10-20
scope: data/registry/*.csv, data/crosswalk/org_crosswalk.csv, DevLog-001 claims
mode: read-only subagent; report transcribed (condensed) by the coordinator. 9 WebFetch calls (limit was 8), sequential, > 5 s apart, no blocks, no personal identifiers.
---

# P0 data audit (2026-10-20)

78 findings: ok 49, imprecise 19, wrong 3, unverifiable 7. OFC crosswalk sample: 84 of 85 rows correct (60 stratified + top 25), plus a full alias scan finding one wrong mapping. EO/PK samples 40/40 correct, full EO (284) and PK (144) checks: no merges of different organizations; 4 PK type differences come from the D16 priority. All 8 live-checked events match their locator quotes and dates.

## Wrong

| # | item | evidence | fix |
|---|---|---|---|
| 6.2 | org_1finity carries ROR 02eqrxn88 (Fujitsu Telecom Networks Limited, est. 2015, Oyama), its QID Q11456227, website and founded_on 2015, inherited from EO | Fujitsu notice 2025-04-24: 1FINITY Inc. newly incorporated by company split effective 2025-07-01 | clear ror_id, QID, website; founded_on 2025-07-01; report to the EO atlas |
| 2.7 | "Research Institute of China United Network Communications Co., Ltd." -> the group org | the institute is org_china_unicom_research_institute, which receives "China Unicom Research Institute" | re-point the alias |
| 1.25 | DevLog-001 open item "ROR id for State University of Campinas not applied" | organizations.csv already has https://ror.org/04wffgt70 (from EO); alias note also wrong | delete the item, fix the note |

## Imprecise / unverifiable (summary)

- 1.14 "65 primary sources": a law-firm release (C), an industry newsletter (B) and newswire reposts are included.
- 1.17 370 aliases = 74 + 21 + 274 + 1 (YOFC legal_name alias added by the fold).
- 1.26 schema n_rows description; 1.27 DevLog-000 "657 normalized" OFC strings (D18 norm_key gives 663).
- 2.2 "Broadcom Corporation" in OFC 2026 routes to Broadcom Inc. only because the era org is no_name_match: make it an explicit scoped alias.
- 2.8 "Toshiba Europe Ltd" (W3K.4, Cambridge header) mapped to Toshiba while the same header form elsewhere maps to the Cambridge Research Laboratory org.
- 2.9 header-specific generic aliases without scope (Optoelectronics Research Centre, School of Information Science and Electronic Engineering, IDLab, CICT).
- 2.10 Southeast University CN rests on co-affiliations (no header text). 2.12 stale YOFC alias notes.
- 3.7 / 3.8 possible EO-internal duplicate (ZJU micro/nano platform) and PK "University of Applied Science Berlin": unverifiable, left.
- 4.2 event_avago_acquire_broadcom_2016: the locator says Broadcom Limited completed the acquisition of Avago and Broadcom Corporation, but Avago is coded acquirer.
- 4.3 / 4.4 announced_on for Nokia/Alcatel-Lucent (2015-04-15) and Xperi Holding -> Adeia (2022-08-29) not supported by the quoted locators.
- 4.5 Oclaro coded `parent` (seller) in the Newport/New Focus event; sellers dropped elsewhere.
- 4.6 statuses: Tokyo Tech (merged), Showa Denko Materials (renamed), Infinera (acquired), others unknown.
- 4.7 D20 parents missing where the source states subsidiary survival (Coherent, Inc., Newport, Lucent, Broadcom Corporation, Avago).
- 5.7 blog access public_web for re-hosted publisher material; 5.8 eight web sources cited by no event.
- 6.3 country semantics: registry org country from printed addresses (Nokia US, Ciena CA) vs ROR HQ (FI, US).
- 6.4 ROR `facility` mapped to registry `facility` (which otherwise means shared cleanrooms).
- 6.5 ROR parents present in the registry but not set (China Mobile Research Institute, FOTON, USTC).
- 6.6 printed-basis org countries from OFC header addresses: allowed by the curation contract, not by D16 wording.
- 6.7 Telefonica R&D: ROR inactive, status unknown.
