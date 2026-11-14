---
title: Fresh-context audit of the lit author-affiliation batch lit_h41 (12 papers)
date: 2026-11-14
auditor: Claude (fresh context; wrote only this record; headers.yaml, derived files, scripts, tests, people and registry data not edited; check run only with --dry-run on the repo batch, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h41/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D400-D565); format from the 2026-11-12 h39 / h40 audits; read-only comparison with earlier batches (WNLO, IEU, Nanjing University chain, UCSB campus, Universidad de Malaga, De Gruyter grouped and list-duplicate precedents) and the org registry
verdict: GO for the people rebuild; 130 author-list slots audited, 130 ok (128 recorded, 2 correctly without rows: kim2023 list duplicates #2 / #10), 0 imprecise, 0 wrong; header-only author chowdhury2022 John Pellerin (slot 0) ok; all 11 extractor judgment calls confirmed; two note-only fixes (N1 gao2025, N2 xu2025: wrong precedent batch named); D412 / D426 candidates jin2024 #1, xu2025 #7, kim2023, chowdhury2022; checker gaps G1 (last author's second marker not bound, 2 new cases), G2 (province accepted as locality)
---

# Lit header batch audit: lit_h41 (2026-11-14)

## Scope

Batch lit_h41 (12 papers: 7 Chinese Optics Letters with bilingual author lines, 2 Nanophotonics / De Gruyter, 1 OFC
2022 paper (Optica format), 1 APL Photonics (AIP cover page), 1 Optics & Laser Technology (Elsevier); 130 author-list
slots, 1 header-only author; 148 rows).
Restricted corpus: this record names only authors, orgs, units, cities and countries; no paper text is quoted and no
contact, street, building, postal-box or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h41 --corpus lit --codes <id> --pdf`
  (all 12; morenopozas2026 also with `--pages 2`; output kept in the session scratchpad only). Text and PDF layers
  agree on every author line, marker run and block. No `references/<id>/figures/page_01.png` render exists for these
  papers (page_02 only, or none for kim2023 / morenopozas2026); the PDF layer was used as the page view.
- Per slot: printed name vs `compare.csv` slot and the author list printed by `show`; printed marker run vs `markers` +
  `dropped_markers`; block fields vs the print (org, unit chain, more_orgs, campus, city, country); role; locator; grade.
  All 31 distinct (paper, org, unit, place, org id, match basis) tuples of `header_rows.csv` read.
- Contact markers: the leading character of each masked contact line on page 1 of `text.md` (contents not printed): the
  7 Chinese Optics Letters papers start their lines with one or two asterisks (corresponding author), chowdhury2022 with
  asterisks, perezarmenta2023 with an unmarked line, kim2023 / li2025b inside the grouped footnote; morenopozas2026 page
  2 marks its correspondence line with letter a (verified). Only morenopozas2026 needs a `dropped_markers` entry; it is
  there. Daggers in xu2025 and zhang2025e point to a printed equal-contribution line (symbol marks, no entry needed).
- Missed blocks: cue scan of the whole `text.md` of all 12 (now with / at, present / current address or affiliation,
  currently, presently, is / are / was / were (also / now) with, also with, on leave, visiting, formerly, deceased,
  permanent address, affiliat-). 5 hits: gao2025 (2) and kim2023 (2) body-text "within", morenopozas2026 the AIP
  affiliations heading on page 2. No present address, prose statement or later-page affiliation list. No missed block.
- Claims tested with probes on scratch copies of the batch (`probes/probe.py` in the session scratchpad; module
  `LIT_BASE` pointed at a scratch base; derived files written only there). md5 of every repo batch file identical
  before and after the audit.
- Stamp: `check_stamp.txt` matches `headers.yaml` (sha256 5a22f1ce...).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h41 | 12 / 12 | 130 | 130 | 0 | 0 |

- Rows 148 (all grade A: printed 78, single 47, grouped 23; primary 128, additional 20; locators p.1 header 118, p.1
  footnote 23, p.2 header 7); recorded 128, no_header 2 (kim2023 #2, #10: duplicate list entries); papers ok 12,
  partial 0, unreadable 0; `author_list_differs` 2 (chowdhury2022, kim2023); explicit slots 3 (kim2023 #1, #9; chowdhury2022
  Pellerin `slot: 0`), all required (probes C1, K1); present addresses 0; prose blocks 0; `order_differs` false on
  every slot; multi-affiliation slots 20; 9 unmapped org strings.
- Per paper (slots / rows / rating): chowdhury2022 30 (+1 header-only) / 30 ok; deng2025 9 / 10 ok; gao2025 6 / 9 ok;
  jin2024 10 / 15 ok; ma2024 9 / 9 ok; xu2025 9 / 16 ok; zhang2025e 10 / 10 ok; zhao2025b 11 / 11 ok; kim2023 10 / 11
  ok (8 recorded, 2 list duplicates without rows); li2025b 11 / 12 ok; morenopozas2026 7 / 7 ok; perezarmenta2023 8 / 8 ok.

### Per-slot field counts (130 slots)

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (130) | 130 | 0 | 0 |
| markers + dropped_markers (128 recorded) | 128 | 0 | 0 |
| blocks (org / unit / campus / locality / country) (128 recorded) | 128 | 0 | 0 |
| prose blocks | n/a (none printed) | | |
| present addresses | n/a (none printed) | | |
| locators (128 recorded) | 128 | 0 | 0 |
| unreadable authors | n/a (none) | | |

## Per-paper findings

- chowdhury2022 (30 + 1): single unmarked block (`single`, authors `[]`) GlobalFoundries, Malta, US (state, street and
  postal code not recorded). Header p.1 prints 31 names; the author list stops at 30 (Ted Letavic). John Pellerin (31st
  printed, last) matches no list name: `slot: 0` + `author_list_differs` required (probe C1 without it: 1 error). List
  forms with extra given names / initials (Asif Jahangir Chowdhury, Judson Robert Holt, Ryan William Sporer, Michał
  Rakowski, ...) matched automatically. Asterisks on authors 1 and 8 = contact lines (symbol marks). ok.
- deng2025 (9): runs 1 / 1 / 2 / 3 / 3,4 / 5 / 1 / 2,* / 1,** (Chinese names in parentheses between name and markers,
  read through by the checker). Block 1 Henan Normal University + unit with the printed misspelling Hennan, Xinxiang;
  block 2 Southeast University + Advanced Photonics Center, School of Electronic Science and Engineering, Nanjing
  (`org_southeast_university`); block 3 Shanxi key laboratory alone, Jincheng; block 4 Jincheng Research Institute of
  Opto-mechatronics Industry, Jincheng; block 5 Henan Normal University + Henan key laboratory and college, Xinxiang;
  all CN. Probe D2 (Yu Zhang 3 only): 3 errors (bound). ok.
- gao2025 (6): runs 1 / 1,2,* / 3,** / 3 / 1,2 / 1,2. Block 1 Shanghai Jiao Tong University + State Key Laboratory
  of Photonics and Communications, Department of Electronic Engineering, Shanghai; block 2 SJTU-Pinghu Institute of
  Intelligent Optoelectronics, printed with the province Zhejiang only (no city): `locality: ""` right (D288); block 3
  IEU + Henan Key Laboratory of Quantum Information and Cryptography, Zhengzhou; all CN. List #4 Wan-Su Bao vs printed
  Wansu Bao: automatic. ok (note names the wrong precedent batch: N1).
- jin2024 (10): runs 1,2 x3 / 2,3 / 2,4 / 2 x4 / 2,*. Four Shanghai Jiao Tong University blocks with their own units
  (Department of Electronic Engineering; Center for Advanced Electronic Materials and Devices; State Key Laboratory of
  Metal Matrix Composites, School of Materials Science and Engineering; Department of Micro/Nano Electronics), Shanghai,
  CN. Probe J1 (Rujun Liao 2 only): 3 errors. List #1 Xin Min Jin vs printed Xin Jin (two-character Chinese name
  printed): automatic match, question 6. ok.
- ma2024 (9): runs 1 x4 / 1,* / 1,** / 2 / 2 / 1. Block 1 Nanjing University with the ampersand-joined chain (ministry
  key laboratory, national laboratory, college, institute, Nanjing University-Tongding joint lab) as one unit, Nanjing
  (same chain without the joint lab in lit_h03, h14, h16, h28, h33); block 2 54th Research Institute of China
  Electronics Technology Group Corporation + Optical Communication Research and Development Center, Shijiazhuang; both
  CN. ok.
- xu2025 (9): runs 1,2,dagger / 1,dagger / 1,2 x4 / 1,2,* / 1,** / 1,2. Block 1 Huazhong University of Science and
  Technology + unit Wuhan National Laboratory for Optoelectronics and School of Optical and Electronic Information,
  Wuhan; block 2 Optics Valley Laboratory, Wuhan; both CN. List #7 Jing Hong Du vs printed Jing Du (two-character
  Chinese name printed): automatic, question 6. ok (note names the wrong precedent batch: N2).
- zhang2025e (10): single unmarked block (`single`, authors `[]`; daggers equal contribution, asterisk corresponding
  author): Nanjing University + the national laboratory / school / college / school / innovation center chain, Nanjing,
  CN (College of Engineering and Applied Science singular, as printed). Xinjie Lü with the diaeresis as printed; list
  #10 Shining N. Zhu vs Shining Zhu automatic. ok.
- zhao2025b (11): runs 1 / 1,* / 1,** / 2 / 2 / 1 x3 / 3 / 1 / 1. Block 1 identical to ma2024 block 1; block 2 China
  United Network Communications Corporation Limited + unit Nanjing Branch (branch printed first), Nanjing (maps by alias
  to `org_china_united_network_communications_group`); block 3 Jiangsu University of Science and Technology + Ocean
  College, Zhenjiang; all CN. ok.
- kim2023 (10 slots, 8 authors): De Gruyter, no markers on the author line; the p.1 footnote prints the corresponding
  author (Myung-Ki Kim) with two blocks (Korea University + KU-KIST Graduate School of Converging Science and
  Technology; Korea Institute of Science and Technology (KIST) + Center for Quantum Information), then the groups
  Moohyuk Kim / Nu-Ri Park / Aran Yu (KU-KIST), Jin Tae Kim (Electronics and Telecommunications Research Institute
  (ETRI) + Quantum Technology Research Department, Daejeon), Minseok Jeon (KU-KIST; KIST), Seung-Woo Jeon (KIST),
  Sang-Wook Han (KIST; Korea University of Science and Technology (UST) + Division of Nanoscience and Technology, KIST
  School); Seoul for all but ETRI; all KR (Republic of Korea printed). G1-G9 map exactly; `p.1 footnote` right. The
  author list has Moohyuk Kim at 1 and 2 and Myung-Ki Kim at 9 and 10: explicit slots required (probe K1: 2 errors);
  probe K2 (slots 2 / 10) also passes, so the first-occurrence choice is the liu2019 (lit_h31) convention, not a check
  result. Probe K3 (corresponding author moved to G3): 4 errors, grouping verified. ok.
- li2025b (11): De Gruyter, same footnote layout: Bowers (G1, corresponding), Li / Xiang / Guo / Peters / Dumont (G2)
  with University of California Santa Barbara (printed without a comma) + Department of Electrical and Computer
  Engineering, Santa Barbara; Xue / Gao (G3: University of Rochester + Department of Electrical and Computer
  Engineering), Staffa / Hu (G4: University of Rochester + Institute of Optics), Lin (G5, G6: both Rochester units);
  Rochester; all US (state codes not recorded). Org University of California + `campus` Santa Barbara maps to
  `org_ucsb`. List #11 John Edward Bowers vs John E. Bowers automatic. ok.
- morenopozas2026 (7): p.1 is the AIP cover (names, no affiliation); the author line with marker a on author 1 and one
  unmarked block are on p.2: Universidad de Málaga + Photonics and RF Research Lab., Telecommunication Research
  Institute (TELMA), Málaga, ES (street and postal code not recorded). `locator: "p.2 header"` required (probe M2: 4
  errors without it); a = correspondence line, `dropped_markers` required (probe M1: 2 errors). List forms Miguel Barona
  Ruiz, Manuel Montilla-Gallardo, Íñigo Molina-Fernández matched automatically. ok.
- perezarmenta2023 (8): Elsevier letter markers, runs a,* / a x3 / b / b / a / a. Block a Universidad de Málaga + unit
  Telecommunication Research Institute (TELMA), Málaga, ES; the block then prints the CEI Andalucía TECH campus of
  excellence and the E.T.S.I. Telecomunicación school after the university (not copied); block b National Research
  Council Canada, Ottawa, CA (`org_national_research_council_canada`; province Ontario not recorded). Detached accents
  in the text layer written with the intended letters (D282). List #8 Juan Gonzalo vs printed J. Gonzalo
  Wangüemert-Pérez automatic. ok.

## Extractor calls (verified against the page, with ruling recommendation)

1. chowdhury2022 John Pellerin `slot: 0`. Verified: 31 printed names, 30 list names, the list ends at Ted Letavic and
   contains no Pellerin. Probe C1: the slot is required. Recommendation: accept; Pellerin becomes a header-only author
   in `lit_headers_extra_authors.csv` at aggregate; add chowdhury2022 to the D412 correction file (list truncated after
   30 names, missing the last author), as alexander2024 (D546).
2. kim2023 duplicate list names. Verified (list 10 entries for 8 printed authors). Explicit `slot: 1` / `slot: 9`
   required (probe K1); slots 2 and 10 stay without rows. Recommendation: accept (liu2019 convention, D546); kim2023 to
   the D412 correction file (drop list entries 2 and 10).
3. kim2023 / li2025b De Gruyter grouped layout. Verified against the footnote order (corresponding author first, then
   the groups); identical to the lit_h24 yang2018 / lit_h26 cabo2024 form ruled in D461 and D546 (grouped chosen by
   layout). Probe K3 shows the checker binds carriers to their group. Recommendation: accept.
4. li2025b UCSB campus. Printed University of California Santa Barbara without a comma; `campus: "Santa Barbara"` is
   the D301 / D449 / D461 corpus form (lit_h24, h32, h34 notes record the same no-comma case). Probe L1 (one-string org)
   also maps to `org_ucsb`, so the people links are the same either way. Recommendation: accept.
5. morenopozas2026 cover page. Verified: p.1 is the AIP cover, the author line and block are on text.md p.2;
   `p.2 header` (D366) and the dropped contact marker a are both required (probes M1, M2). Recommendation: accept.
6. xu2025 WNLO as a unit chain under HUST. The printed sequence (laboratory and school, then the university) is recorded
   as a HUST unit chain in lit_h06, h11, h13, h16, h17, h18, h21 (one block), h25, h31, h33, h35, h38 and 11 OFC
   batches (ofc_h01-h03, h05, h06, h09-h11, h13-h15; some with the school first), and as
   two orgs (WNLO + `more_orgs` HUST) in lit_h02, h12, h21 (one block), h26, h28. Probe X1 (two-org form): 0 errors, and
   the WNLO row maps by alias to `org_huazhong_university_of_science_and_technology`, so both forms give the same org id.
   The note's "as lit_h40" is wrong (lit_h40 has no WNLO block): N2. Recommendation: accept the unit chain (majority
   form); no retro-edit of the two-org records (org round already aliases WNLO to HUST).
7. deng2025 Shanxi key laboratory as org; Hennan kept. Verified: block 3 prints the key laboratory with only the city,
   no parent org; the misspelling Hennan is printed in block 1 (block 5 prints Henan). Recommendation: accept both (D550
   li2025c Beijing key laboratory as its own org; D550 "Southeast Univcersity" as printed).
8. gao2025 IEU org with the Henan key laboratory unit; block 2 with province only. Verified: block 3 prints the key
   laboratory, then IEU, then Zhengzhou; identical to lit_h06 gao2025a block 3 (already in `org_requests.csv`). Block 2
   prints only Zhejiang (province) and China: `locality: ""` (D288; lit_h06 gao2025a block 2 printed Pinghu and records
   it). The note's "as lit_h39" is wrong: N1. Recommendation: accept the fields; org round resolves the acronym from a
   source (no expansion is printed in either paper).
9. ma2024 54th Research Institute of China Electronics Technology Group Corporation as one org name. Verified as one
   contiguous printed name after the unit. Probe E1 (institute + `more_orgs` CETC): 0 errors, both strings unmapped.
   The group name is joined by "of" inside the institute's printed name (the "Institute of Semiconductors, Chinese
   Academy of Sciences" class of the contract), not a separate parent after a comma. Recommendation: accept; org round:
   new org with parent China Electronics Technology Group Corporation.
10. zhao2025b China Unicom Nanjing Branch as unit. Verified: Nanjing Branch is printed before the company. Recorded org =
    company, unit = branch maps by alias to `org_china_united_network_communications_group`; probe Z1 (one string)
    leaves the row unmapped. Same direction as the D565 company-as-org rule and the ofc_h15 China Mobile Guangdong /
    Zhuhai Branch block. Recommendation: accept.
11. perezarmenta2023 campus-of-excellence text dropped. Verified: CEI Andalucía TECH and E.T.S.I. Telecomunicación are
    printed after the university, so neither can join the contiguous unit. Probe P1 (CEI Andalucía TECH as `more_orgs`):
    0 errors but adds an unmapped row for a consortium label, not an employer. Same handling as lit_h26 cabo2024 (D521).
    Recommendation: accept.

## Fixes (exact YAML edits)

No slot, marker, block field or locator needs a change. Two note corrections (precedent references only; rows
unchanged, but the check stamp changes, so rerun `check lit_h41 --corpus lit` after applying):

N1 `lit:gao2025` note: replace `(recorded as unit, as lit_h39)` with `(recorded as unit, as lit_h06 gao2025a)`.

N2 `lit:xu2025` note: replace `(recorded as a unit chain of the university, as lit_h40 and earlier precedents of this
printed form)` with `(recorded as a unit chain of the university, as lit_h13, lit_h21, lit_h35 and lit_h38; lit_h02,
lit_h26 and lit_h28 record two orgs, same org id)`.

## Open questions (with recommendation)

1. Calls 1-11 above: accept as recorded. Recommended: yes.
2. N1 / N2: apply (notes only). Recommended: yes, before the stamp is used by aggregate.
3. D412 correction file: chowdhury2022 (append John Pellerin, list stops at 30 of 31), kim2023 (list entries 2 and 10
   are duplicates). Recommended: yes.
4. jin2024 #1 (list Xin Min Jin, printed Xin Jin with a two-character Chinese name) and xu2025 #7 (list Jing Hong Du,
   printed Jing Du with a two-character Chinese name): automatic matches with a list-only given-name syllable, same
   class as ni2024 #5 (D565) and hu2020 #4 / lin2023 #6 (D550). The printed Chinese names have one given-name character,
   so the extra list syllable is not on the page. Recommended: D426 review list for both; D412 entries (list name to
   the printed form) as for hu2020 / lin2023.
5. G1 / G2 below: add gao2025 #6 and xu2025 #9 to the D442 / D546 / D557 / D565 last-author test list; add gao2025
   block 2 (province as locality) next to the h40 G2 state-code case. Recommended: yes; YAML already exact.

## Unmapped org names (org round, no YAML change)

| printed org (unit) | place | proposal |
|---|---|---|
| 54th Research Institute of China Electronics Technology Group Corporation (Optical Communication Research and Development Center) | Shijiazhuang, CN | new org, parent CETC (call 9) |
| Henan Normal University (two key laboratory / school or college units) | Xinxiang, CN | new org |
| IEU (Henan Key Laboratory of Quantum Information and Cryptography) | Zhengzhou, CN | already requested (lit_h06 gao2025a); resolve acronym from a source |
| Jiangsu University of Science and Technology (Ocean College) | Zhenjiang, CN | already requested (other units) |
| Jincheng Research Institute of Opto-mechatronics Industry | Jincheng, CN | new org |
| Shanxi Key Laboratory of Advanced Semiconductor Optoelectronic Devices and Integrated Systems | Jincheng, CN | new org (host not printed) |
| Universidad de Málaga (TELMA; Photonics and RF Research Lab., TELMA) | Málaga, ES | already requested (lit_h12, h26, h29, h31) |

## Privacy and as-printed scan

- Grep over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv` and `papers.csv` (paper ids removed)
  for contact / URL / ORCID patterns, street, road, avenue, building, room, postal-box and Cedex words, the printed
  street words of chowdhury2022 and morenopozas2026, and digit runs of 4 or more: 0 hits. Notes name only the kinds of
  omitted text (street address, postal codes, provinces, states), never their values.
- As printed (kept, correct): Hennan (deng2025 block 1); Opto-mechatronics with its hyphen; Xinjie Lü with the
  diaeresis; Photonics and RF Research Lab. with its period; parenthesized acronyms (KIST, ETRI, UST, TELMA). No
  `skip_prefix`, `skip_between`, `continued` or `more_orgs` field in this batch; one `campus` (li2025b).

## Commands (2026-11-14, log times)

| Command | Result |
|---|---|
| `check lit_h41 --corpus lit --dry-run` 10:07:38 (pid 51815) | 0 errors, 0 warnings; slots 130, recorded 128, no_header 2; rows 148 (grade A 148; printed 78, single 47, grouped 23; primary 128, additional 20); papers ok 12; multi-affiliation slots 20; present addresses 0; 9 unmapped org strings |
| `show lit_h41 --corpus lit --codes <id> --pdf`, all 12 (+ `--pages 2` for morenopozas2026) | headers and author lists read (scratchpad only) |
| `probes/probe.py` on scratch copies, 10:09:18-10:12:35 | below; repo batch files md5 unchanged; each probe writes its usual log files under `logs/` (name contains `lit_p41`) |

| probe | change | result | reading |
|---|---|---|---|
| BASE | unchanged copy | 0 errors, 0 warnings | baseline |
| C1 | Pellerin without `slot: 0` | 1 error (0 candidates) | slot 0 required |
| K1 | kim2023 without explicit slots | 2 errors (2 candidates each) | explicit slots required |
| K2 | kim2023 slots 2 / 10 | 0 errors | first occurrence is a convention |
| K3 | Myung-Ki Kim moved to G3 | 4 errors | grouping verified |
| G1 | gao2025 block 2 locality Zhejiang | 0 errors | G2: province accepted as locality |
| M1 | morenopozas2026 without dropped a | 2 errors | contact marker bound |
| M2 | morenopozas2026 block without `p.2 header` | 4 errors | locator required |
| D1 | Kun Yu (last) marker 2 | 2 errors | last author's single marker bound |
| D2 | Yu Zhang marker 3 only | 3 errors | markers bound |
| J1 | Rujun Liao marker 2 only | 3 errors | markers bound |
| LZ1 | Linjie Zhou (last) marker 1 only | 0 errors | G1 |
| JW1 | Jian Wang (last) marker 1 only | 0 errors | G1 |
| X1 | xu2025 WNLO org + `more_orgs` HUST | 0 errors; both rows map to HUST | same id either way |
| P1 | perezarmenta2023 `more_orgs` CEI Andalucía TECH | 0 errors; extra unmapped row | not needed |
| Z1 | zhao2025b branch and company as one org string | 0 errors; unmapped | recorded form better |
| L1 | li2025b org University of California Santa Barbara, no campus | 0 errors; `org_ucsb` | same id either way |
| E1 | ma2024 institute + `more_orgs` CETC | 0 errors; both unmapped | recorded form accepted |

## Checker gaps observed (scripts not edited)

- G1 Last author's markers after the first are not bound: gao2025 #6 (Linjie Zhou 1,2) and xu2025 #9 (Jian Wang 1,2)
  pass with the second marker removed (probes LZ1, JW1); a wrong single marker on the last author is caught (D1).
  Extends the D442 / D546 / D557 / D565 last-author gap. YAML exact in both.
- G2 Locality check accepts a printed province (probe G1, gao2025 block 2 "Zhejiang" passes); D288 requires an empty
  locality when only a province is printed. Same class as the h40 G2 state-code case. YAML exact.

## Verdict

GO. No slot carries a wrong person, org, city, country or marker, nothing is invented, no block is missed, and no
address or contact text is recorded. All 11 extractor judgment calls are confirmed with the recommendation to accept.
Two note-only corrections (N1, N2) fix wrong precedent references; rows are unchanged by them. D412 gains chowdhury2022
and kim2023; jin2024 #1 and xu2025 #7 go to the D426 review list (and D412 as for hu2020 / lin2023).
