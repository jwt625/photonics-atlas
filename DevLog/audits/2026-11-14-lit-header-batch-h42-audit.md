---
title: Fresh-context audit of the lit author-affiliation batch lit_h42 (11 papers)
date: 2026-11-14
auditor: Claude (fresh context; wrote only this record and scratchpad renders / probes; headers.yaml, derived files, scripts, tests, people and registry data not edited; check run only with --dry-run, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h42/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D412, D426, D461, D466, D546, D550, D557, D565); format from the 2026-11-12 h39 / h40 audits; read-only comparison with earlier batches (grouped, per_author, later-page locators, Zijingang, Ningbo / Jiaxing institutes, Hefei / Zhejiang Lab, CUHK / HKUST (Guangzhou)) and the org registry
verdict: GO for the people rebuild; 88 slots audited, 88 ok, 0 imprecise, 0 wrong; no YAML fix required (one optional note edit N1); all 9 extractor judgment calls confirmed; 3 more D412 "Daoxin Dai A" cases; checker gaps G1 (last-author further marker, known), G2 (ward accepted as locality), G3 (explicit slot bypasses the D369 initials check), G4 (YAML author order of per_author / grouped papers not verified)
---

# Lit header batch audit: lit_h42 (2026-11-14)

## Scope

Batch lit_h42: 11 papers (Laser & Photonics Reviews 7, Nanophotonics 2 (one Wiley bar layout, one De Gruyter
footnote layout), ACS Photonics 1, one conference paper); 88 author-list slots, no header-only author; 149 rows.
Restricted corpus: this record names only authors, orgs, units, cities and countries; no paper text is quoted and no
contact, street, building, postal-box or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h42 --corpus lit --codes <id> --pdf`
  (all 11), wang2026h also with `--pages 7`; output kept in the scratchpad only.
- Rendered pages (pymupdf, 200 dpi, scratchpad `lit_h42_audit/`): page-1 footnote crops of ren2025, wang2023,
  wang2023a, xia2024, zhao2022; page-1 header crops of zhang2026d and wang2026j. Every grouped block of the five Wiley
  footnote papers was read on the render, not on the text layer.
- Text-layer state: word spaces are dropped in the later groups of ren2025, wang2023, wang2023a and xia2024 (names and
  some unit words run together); zhao2022's footnote text is clean (the page render agrees with it). Markers of the
  three printed-marker papers (sun2026, wang2026j, zhang2026d) are identical in the text and PDF layers.
- Per slot: printed name vs `compare.csv` and the author list printed by `show`; marker / group membership vs the
  print; block fields (org, unit chain, campus, city, country); role; locator; grade. All distinct (paper, org,
  org id, match basis) tuples of `header_rows.csv` read.
- Missed blocks: cue scan of the whole `text.md` of all 11 (now with / at, present / current address or affiliation,
  currently, is / are / was / were (also / now) with, also with, on leave, visiting, formerly, deceased, permanent
  address, affiliat-): 7 hits (wang2023a p.4 x2, p.5; wang2026h p.4; yi2024 p.2; yokokawa2022 p.2; zhang2026d p.9), all
  body text (physics wording). No present address, prose statement or missed block. wang2026h page 1 prints no
  affiliation (checked).
- Probes on scratch copies (`lit_h42_audit/probes/probe.py` in the session scratchpad; one scratch `LIT_BASE` per
  probe). md5 of every repo batch file identical before and after the audit. Stamp: `check_stamp.txt` matches
  `headers.yaml` (sha256 1354f6a3...).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h42 | 11 / 11 | 88 | 88 | 0 | 0 |

- Rows 149 (all grade A: grouped 82, printed 54, single 8, per_author 5; primary 88, additional 61); recorded 88,
  no_header 0; papers ok 11, partial 0, unreadable 0; `author_list_differs` 0; explicit slots 1 (wang2023a S. Wang,
  required: probe A1); present addresses 0; prose blocks 0; `order_differs` on 5 papers (ren2025, wang2023,
  wang2023a, wang2026h, yi2024: group / section order, expected); multi-affiliation slots 42; 8 unmapped org strings.
- Per paper (slots / rows / rating): ren2025 9 / 11 ok; sun2026 7 / 28 ok; wang2023 9 / 12 ok; wang2023a 10 / 20 ok;
  wang2026h 5 / 5 ok; wang2026j 10 / 12 ok; xia2024 10 / 21 ok; yi2024 7 / 10 ok; yokokawa2022 8 / 8 ok; zhang2026d
  7 / 14 ok; zhao2022 6 / 8 ok.

### Per-slot field counts (88 slots)

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (88) | 88 | 0 | 0 |
| markers / group membership (88) | 88 | 0 | 0 |
| blocks (org / unit / campus / locality / country) (88) | 88 | 0 | 0 |
| prose blocks | n/a (none printed) | | |
| present addresses | n/a (none printed) | | |
| locators (88) | 88 | 0 | 0 |

## Per-paper findings

- ren2025 (9; p.1 footnote, grouped, render read): group 1 X. Ren, Y. Huang, W. Zhang above Tsinghua University with
  the three-level chain (frontier science center, state key laboratory of low-dimensional quantum physics, Department
  of Electronic Engineering), Beijing; group 2 Y. Zhao, L. Lin, H.-B. Sun above Tsinghua University with the precision
  measurement state key laboratory and Department of Precision Instrument, Beijing; group 3 Z. Yan, Z. Yuan, Y. Huang,
  W. Zhang above Beijing Academy of Quantum Information Sciences, Beijing; group 4 Y. Shi above Yunnan University +
  School of Physics and Astronomy, Kunming; all CN. Membership exact (Huang and Zhang G1+G3; probe R1 shows G3
  membership is bound). List #2 Yao Ming Zhao vs printed Yao Zhao / Y. Zhao: automatic (dropped second given name; D426
  review list, question 9). ok.
- sun2026 (7; printed): marker runs 1-5 / 1-6 / 7 / 7 / 1-5 x3, identical in text and PDF. Blocks 1, 2, 6 Beihang
  University with units School of Instrumentation and Optoelectronic Engineering; Institute of Large-scale Scientific
  Facility and Centre for Zero Magnetic Field Science (one and-joined segment); Quantum Science and Technology College;
  all Beijing. Blocks 3 Hangzhou Extremely Weak Magnetic Field Major Science and Technology Infrastructure Research
  Institute and 4 Beihang Hangzhou Innovation Institute, Hangzhou, printed without a parent; 5 Hefei National
  Laboratory, Hefei; 7 Zhejiang Laboratory, Hangzhou; all CN. Correspondence line carries no marker. ok (question 3).
- wang2023 (9; p.1 footnote, grouped, render read): five groups exactly as recorded (C. Wang G1+G2, Z. Li G1+G5,
  Q. Chen G4+G5). Block 1 Sun Yat-sen University with the school and the Guangdong provincial key laboratory joined by
  and (one segment), Guangzhou; Peng Cheng Laboratory, Shenzhen; South China Normal University + the Guangdong
  engineering technology research center, Guangzhou; Sun Yat-sen University + School of Microelectronics Science and
  Technology, Zhuhai (locality, no campus: no place printed after the org other than the city); Southern Marine
  Science and Engineering Guangdong Laboratory (Zhuhai), Zhuhai; all CN. ok (question 6).
- wang2023a (10; p.1 footnote, grouped, render read): the nine-author group printed twice (above blocks 1 and 2), C. Ji
  printed twice (blocks 3 and 4). Block 1 Institute of Semiconductors, Chinese Academy of Sciences + Key Laboratory of
  Semiconductor Materials Science, Beijing; block 2 University of Chinese Academy of Sciences + Center of Materials
  Science and Optoelectronics Engineering, Beijing; block 3 Zhejiang University + College of Information Science and
  Electronic Engineering, Hangzhou; block 4 Zhejiang Labs (as printed), Hangzhou; all CN. S. Wang slot 1 and S.-L.
  Wang automatic slot 4 (question 2). List #6 Lei S. Meng vs L. Meng: automatic. ok.
- wang2026h (5; p.7 author-information section, per_author): no affiliation on page 1. The section prints the
  corresponding author (Hon Ki Tsang) and then Zelu Wang, Kaihang Lu, Hongnan Xu, Yeyu Tong, each followed by its own
  block: CUHK Department of Electronic Engineering, Hong Kong + China (HK, D249; earlier CUHK records: 4 Hong Kong / HK,
  2 Shatin / HK) for Tsang, Wang, Xu; The Hong Kong University of Science and Technology (Guangzhou) + Microelectronic Thrust,
  Guangzhou, CN for Lu and Tong (maps by name). Authors listed in the section order. ok (question 1).
- wang2026j (10; printed, Wiley bar layout, render read): runs 1 x9 / 1,2,3. Block 1 Zhejiang University + the
  four-part chain (state key laboratory, centre, college, international research center), Hangzhou; block 2 China
  Jiliang University, Hangzhou; block 3 Zhejiang University + Intelligent Optics & Photonics Research Center, Jiaxing
  Research Institute, Jiaxing (same form as earlier Jiaxing records); all CN. List #10 Daoxin Dai A (question 8). ok.
- xia2024 (10; p.1 footnote, grouped, render read): the ten-author group printed twice (blocks 1 and 2), Z. Li above
  block 3. Block 1 Sun Yat-sen University + Guangdong provincial key laboratory, School of Electrical and Information
  Technology (comma chain as printed), Guangzhou; block 2 Sun Yat-sen University + Key Laboratory of Optoelectronic
  Materials and Technologies (printed without State), Guangzhou; block 3 Southern Marine Science and Engineering
  Guangdong Laboratory (Zhuhai), Zhuhai; all CN. The note omits that the text layer drops word spaces in groups 2-3
  (optional N1). ok.
- yi2024 (7; De Gruyter p.1 footnote, grouped, D461 yang2018 rule): corresponding author Daoxin Dai with three blocks
  (Hangzhou chain; Ningbo Research Institute, Ningbo; Jiaxing key laboratory chain, Jiaxing), then the five-author group
  with the Hangzhou chain, then Yaocheng Shi with the Hangzhou chain and Ningbo Research Institute; all Zhejiang
  University, CN. Zijingang Campus printed before Hangzhou in every Hangzhou block, not recorded (question 5). Probe Y1
  (Shi without G6) fails: membership bound. List #7 Daoxin Dai A (question 8). ok.
- yokokawa2022 (8): single unmarked block Lumentum Japan, Inc., Sagamihara, JP (alias to `org_lumentum`, as ofc
  Tu3J.7); ward Chuo-ku printed before the city noted only (question 7); street, prefecture and postal code not
  recorded. ok.
- zhang2026d (7; printed, bars, render read): every author 1,2. Block 1 Photonic Research Group (printed without the
  s), Department of Information Technology, Ghent University - IMEC, Ghent; block 2 Ghent University + Center for Nano-
  and Biophotonics (NB Photonics), Ghent; both BE. ok (question 4).
- zhao2022 (6; p.1 footnote, grouped, render read): group 1 all six authors above Zhejiang University + State Key
  Laboratory for Modern Optical Instrumentation, College of Optical Science and Engineering, International Research
  Center for Advanced Photonics, Hangzhou (Zijingang Campus not recorded); group 2 W. Zhao, D. Dai above Zhejiang
  University + Ningbo Research Institute, Ningbo (4 earlier records use this form); both CN. List #6 Daoxin Dai A
  (question 8). ok.

## Extractor calls (verified against the page, with ruling recommendation)

1. wang2026h ACS author-information layout, `per_author` + `locator: "p.7 affiliations"`. Each name is followed by its
   own block, no markers: this is the D368 per_author structure (one block per author, verified by position), only on
   a later page. Locator form `p.N affiliations` is the contract form for blocks printed on a later page (D353; cai2021
   lit_h05 is the same ACS section with one shared block, recorded `single` + p.7 affiliations). Probes: W1 (Zelu Wang /
   Kaihang Lu blocks swapped) 4 errors, so the per-author binding is verified; W3 (locator p.1 header) 5 errors; W4
   (basis layout) 5 errors. Grade A is right (positionally verified, not inferred). Ruling recommendation: accept; record
   as the rule for ACS papers whose affiliations appear only in the author-information section: per_author +
   `p.N affiliations` when blocks differ per author, `single` + `p.N affiliations` when one block is shared (cai2021).
2. wang2023a S. Wang explicit slot 1. The footnote prints S. Wang and S.-L. Wang (hyphenated given name Sheng-Lin);
   the author line prints Shuai Wang first and Sheng-Lin Wang fourth. S. Wang = Shuai (slot 1), S.-L. Wang = Shenglin
   (slot 4, automatic). Probe A1 (no slot): 2 errors (matches slots 1 and 4), so the explicit slot is required (D247).
   Probe A2 (the two swapped, S.-L. Wang forced to slot 1 Shuai Wang) passes with only a warning: checker gap G3, so the
   recorded reading is the only safeguard and it is right. Ruling: accept; the same form as lit_h28 a2017 (group-form
   names).
3. sun2026 Beihang naming and blocks 3-4. Units copied as the contiguous printed segments before Beihang University
   (block 2 and-joined, block 6 college). Blocks 3 and 4 print no parent organization; Beihang Hangzhou Innovation
   Institute is one printed name, and probe S2 (org Beihang University + unit Hangzhou Innovation Institute) fails
   (2 errors: not printed that way). Ruling: accept as standalone orgs; in the org round create Beihang Hangzhou
   Innovation Institute as a child of `org_beihang_university` and the Hangzhou magnetic-field infrastructure institute
   as its own org; never an alias of the university.
4. zhang2026d "Ghent University - IMEC" kept dash-joined (D426). Maps by alias to `org_ghent_university;org_imec`;
   probe G1 (split Ghent University + more_orgs IMEC) passes and gives the same two ids. Ruling: accept as recorded (D426
   keeps dash-joined pairs; 3 earlier records (lit_h08, lit_h17, lit_h19) use the same string).
5. Zijingang Campus not recorded (yi2024 4 blocks, zhao2022 block 1). Same as lit_h01, lit_h10 and two lit_h33 records
   (address part, a campus of the same university in the same city, not a distinct institution under D301). Probe Y2
   (`campus: "Zijingang Campus"`) also passes, so the checker does not force either reading. Ruling: accept; no campus.
6. "(Zhuhai)" kept in the org (wang2023 block 5, xia2024 block 3). Contract D301: a parenthesized place stays inside
   `org` and is never dropped by the matcher. Probe X1 (without "(Zhuhai)") passes and is also unmapped. Ruling: accept;
   in the org round create the org with the parenthesized place in its name (one string for both papers, 3 rows).
7. yokokawa2022 ward Chuo-ku noted only. D366: a district printed before the city goes to the note; locality is the
   city as printed (Sagamihara, as ofc Tu3J.7). Probe K1 (locality Chuo-ku) passes: checker gap G2. Ruling: accept.
8. "Daoxin Dai A" author-list artefact (wang2026j #10, yi2024 #7, zhao2022 #6). All three printed names are right and
   matched automatically; same artefact as wang2014, bauters2013, zhang2025b, piggott2015, xu2025a. Ruling: add the
   three to the D412 correction file; rows stay (committed precedent). No YAML workaround exists (h40 probe V6 class).
9. Hefei National Laboratory and Zhejiang Laboratory / Zhejiang Labs unmapped. Correct for this batch: no registry
   alias exists for these strings. Hefei National Laboratory is already unmapped in 13 earlier lit papers (26 rows in
   `org_requests.csv`; lit_h03 qi2024 records it as a USTC unit, D449 notes), and Zhejiang Laboratory in lit han2022.
   The registry holds `org_hefei_laboratory` (name Hefei Laboratory, national_lab, CN) and `org_zhejiang_lab` (Zhejiang
   Lab, ROR 02m2h7991). Ruling: no YAML change; org round: aliases Zhejiang Laboratory and Zhejiang Labs to
   `org_zhejiang_lab`; Hefei National Laboratory as a candidate alias to `org_hefei_laboratory` after confirming the
   registry row is the same institution (its name lacks National).

Further, not flagged by the extractor: ren2025 #2 list Yao Ming Zhao vs printed Yao Zhao (automatic, dropped second
given name): D426 review list with ni2024 #5, hu2020 #4, lin2023 #6 (low priority).

## Fixes (exact YAML edits)

No required fix: no slot, marker, block field, locator or grade is wrong or imprecise.

N1 (optional, note only). In `lit:xia2024` replace the note text

```yaml
asterisks mark the corresponding authors; postal codes not recorded"
```

(the end of the xia2024 note) with

```yaml
asterisks mark the corresponding authors; text layer drops word spaces in groups 2-3 (blocks verified on the rendered page); postal codes not recorded"
```

The replaced string occurs only once inside the xia2024 note; apply it there only (wang2023 and wang2023a notes end
the same way). Rows unchanged (149).

## Open questions (with recommendation)

1. ACS author-information rule (call 1): per_author + `p.N affiliations` (blocks differ) / single + `p.N affiliations`
   (one block). Recommended: yes, record in DevLog-011.
2. wang2023a slot 1 (call 2): keep. Recommended: yes.
3. sun2026 standalone orgs (call 3): keep; Beihang Hangzhou Innovation Institute child of Beihang in the org round.
   Recommended: yes.
4. zhang2026d dash form (call 4), Zijingang (call 5), "(Zhuhai)" (call 6), ward (call 7): keep. Recommended: yes.
5. D412 (call 8): wang2026j #10, yi2024 #7, zhao2022 #6. Recommended: yes.
6. Org round (call 9): Zhejiang Laboratory / Zhejiang Labs -> `org_zhejiang_lab`; Hefei National Laboratory ->
   `org_hefei_laboratory` after identity check. Recommended: yes.
7. G1 test list: sun2026 #7 (Xinran Su, marker 5 droppable). Recommended: add to the D442 / D546 / D557 list.

## Unmapped org names (org round, no YAML change)

| printed org (unit) | place | proposal |
|---|---|---|
| Beihang Hangzhou Innovation Institute | Hangzhou, CN | new org, child of `org_beihang_university` |
| China Jiliang University | Hangzhou, CN | new org |
| Hangzhou Extremely Weak Magnetic Field Major Science and Technology Infrastructure Research Institute | Hangzhou, CN | new org |
| Hefei National Laboratory | Hefei, CN | already requested (26 rows); candidate alias to `org_hefei_laboratory` |
| Southern Marine Science and Engineering Guangdong Laboratory (Zhuhai) | Zhuhai, CN | new org (name with the parenthesized place) |
| Yunnan University (School of Physics and Astronomy) | Kunming, CN | new org |
| Zhejiang Laboratory | Hangzhou, CN | already requested (han2022); alias to `org_zhejiang_lab` |
| Zhejiang Labs | Hangzhou, CN | alias to `org_zhejiang_lab` |

## Privacy and as-printed scan

- Grep over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv` and `papers.csv` for contact / URL
  patterns, street / road / avenue / building / room / postal-box words and digit runs of 4 or more: 0 hits apart from
  paper-id years. Notes name only the kinds of omitted text (postal codes, street address, prefecture, ORCID links)
  and the ward (allowed by D366).
- As printed (kept, correct): Photonic Research Group (zhang2026d, without s); Zhejiang Labs; Key Laboratory of
  Optoelectronic Materials and Technologies without State (xia2024); The Chinese University of Hong Kong with the
  article; Institute of Semiconductors, Chinese Academy of Sciences (academy part of the printed name, contract
  example). No `skip_prefix`, `skip_between`, `continued`, `more_orgs` or `campus` field in this batch.

## Commands (2026-11-14, log times)

| Command | Result |
|---|---|
| `check lit_h42 --corpus lit --dry-run` 10:06:14 (pid 51104) | 0 errors, 5 warnings (order differs: ren2025, wang2023, wang2023a, wang2026h, yi2024); slots 88, recorded 88; rows 149 (grade A 149; primary 88, additional 61; grouped 82, printed 54, single 8, per_author 5); papers ok 11; multi-affiliation slots 42; present addresses 0; 8 unmapped org strings |
| `show lit_h42 --corpus lit --codes <id> --pdf`, all 11; wang2026h with `--pages 7` | headers, sections and author lists read (scratchpad only) |
| page renders (pymupdf, scratchpad `lit_h42_audit/*.png`) | 7 crops read |
| `lit_h42_audit/probes/probe.py` on scratch copies, 10:09:39-10:11:23 | below; repo batch files md5 unchanged; each probe check writes its usual log files under `logs/` (prefix `lit_headers_check_lit_p42`) |

| probe | change | result | reading |
|---|---|---|---|
| BASE | unchanged copy | 0 errors, 5 warnings | baseline |
| W1 | wang2026h Zelu Wang G3, Kaihang Lu G2 | 4 errors (D368 position) | per_author binding verified |
| W2 | wang2026h authors in page-1 order (Tsang last) | 0 errors | G4: YAML author order not verified |
| W3 | wang2026h locators p.1 header | 5 errors | p.7 locator required |
| W4 | wang2026h basis layout | 5 errors | per_author is the only passing basis |
| A1 | wang2023a S. Wang without slot | 2 errors (slots 1 and 4) | explicit slot required |
| A2 | S. Wang slot 4, S.-L. Wang slot 1 | 0 errors, 1 warning | G3: explicit slot skips the D369 initials check |
| A3 | C. Ji G3 only | 1 error (G4 unused) | membership bound |
| R1 | ren2025 Y. Huang G1 only | 2 errors (D368) | membership bound |
| R2 | ren2025 Xiaosong Ren for X. Ren | 0 errors | full name also passes (author line before the blocks); group form follows a2017 |
| S1 | sun2026 Xinran Su (last) markers 1-4 | 0 errors | G1 (known last-author gap) |
| S2 | sun2026 block 4 Beihang University + unit | 2 errors | standalone org is the printed form |
| Y1 | yi2024 Yaocheng Shi G5 only | 1 error (G6 unused) | membership bound |
| Y2 | yi2024 G4 campus Zijingang Campus | 0 errors | checker neutral; precedent decides (no campus) |
| G1 | zhang2026d Ghent University + more_orgs IMEC | 0 errors; ids `org_ghent_university`, `org_imec` | same ids as the dash form |
| X1 | xia2024 block 3 without (Zhuhai) | 0 errors; unmapped | keep as printed |
| J1 | wang2026j Daoxin Dai markers 1,2 | 1 error (block 3 unused) | bound |
| K1 | yokokawa2022 locality Chuo-ku | 0 errors | G2: ward accepted as locality |

## Checker gaps observed (scripts not edited)

- G1 Last author's further markers not bound: sun2026 Xinran Su passes without marker 5 (S1). Same gap as D442 / D546 /
  D557 / h40 G1; new test case. YAML exact.
- G2 Locality accepts a ward printed in the block (K1, Chuo-ku); D366 requires the city. Related to h40 G2 (state code)
  and the D557 johnson2020 locality gap. YAML exact.
- G3 An explicit `slot:` bypasses the D369 every-initial agreement: S.-L. Wang forced onto Shuai Wang passes with a
  warning (A2). Related to the D546 initials-comparison gap, but on the explicit-slot path. YAML exact.
- G4 For per_author / grouped papers the YAML author order is not checked against the printed order (W2 passes with
  the page-1 order); the D368 block positions are still bound (W1). Only `header_pos` and the order warning change.
  YAML exact.

## Verdict

GO. All 88 slots carry the right person, markers / group membership, org, unit, city and country; nothing is invented,
no block is missed, no address or contact text is recorded. No YAML fix is required; N1 is an optional note
completion. All nine extractor calls are confirmed as recorded; the coordinator should adopt the ACS
author-information rule (call 1) in DevLog-011, add wang2026j #10 / yi2024 #7 / zhao2022 #6 to the D412 file, add
ren2025 #2 to the D426 review list, and carry the Zhejiang Laboratory / Zhejiang Labs / Hefei National Laboratory alias
proposals to the org round.
