---
title: Fresh-context audit of the lit author-affiliation batch lit_h35 (15 papers)
date: 2026-11-09
auditor: Claude (fresh context; wrote only this record; headers.yaml, derived files, scripts, tests, people and registry data not edited; aggregate and the people build not run; check run only with --dry-run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h35/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D406-D546); format from the 2026-11-08 h34 audit
verdict: GO for the people rebuild (no slot wrong); 117 slots audited, 114 ok, 3 imprecise, 0 wrong; no YAML edit needed now; F1 (hsu2025 #4, second-initial mismatch) waits on the D382 checker change; F2 (hu2020 #4, lin2023 #6, dropped-syllable list form) goes to the D426 review list and the D412 correction file; N1 note wording optional; nothing applied
---

# Lit header batch audit: lit_h35 (2026-11-09)

## Scope

Batch lit_h35 (15 papers, all Optics Express research articles 2020-2026 in the same layout: author line in capitals,
numbered blocks printed directly under it, contact lines masked, abstract after the blocks; 117 author-list slots, no
header-only author; 154 rows). Restricted corpus: this record names only authors, orgs, units, cities and countries;
no paper text is quoted and no contact, street, site, building or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h35 --corpus lit --codes <id> --pdf`
  (all 15; output kept in the session scratchpad only). All blocks are on page 1; no `--pages` needed. The PDF layer
  carries every superscript run legibly; no page render needed.
- Per slot: printed name vs `compare.csv` slot and the author list printed by `show`; printed marker run vs `markers` +
  `dropped_markers`; block fields vs the print (org, unit chain, campus, city, country); locator; parents; present
  addresses. All 37 distinct (paper, org, unit, place, org id) tuples of `header_rows.csv` read; no wrong mapping.
- Contact markers: the masked contact lines of chen2022a (4), fatema2026 (3, 4), hu2021 (2, 3), itoh2024a (3) and
  lin2023 (4) were checked in `text.md` by their leading character only (contents not printed): each dropped marker
  leads a contact line, so `dropped_markers` with reason contact footnote is right. goyvaerts2020 marker 4 is the
  printed equal-contribution line (dropped, right). The other 10 papers have one contact line led by the asterisk.
- Missed blocks: cue scan of the whole `text.md` of all 15 (now with / at, present / current address, present / current
  affiliation, currently, presently, is / are / was / were (also / now) with, also with, on leave, visiting, formerly,
  deceased, permanent address, equal contribution). 2 hits: goyvaerts2020 p.1 (the equal-contribution footnote,
  recorded as dropped marker 4) and cui2023a p.3 (body text). No present address, prose statement or later-page
  affiliation list in any paper. No missed block.
- Author lists for hsu2025, hu2020 and lin2023 read from `cache/literature/merged.jsonl` (OpenAlex-derived list); name
  form counts over the whole file: "Jian Xin Xu" 20, "C.-J. Wang" 5, "Chia-Hsuan Wang" 7.
- Claims and contract calls tested with dry-run probes on scratch copies of the batch (`probes/probe.py` in the session
  scratchpad, via the module's `LIT_BASE`); md5 of every repo batch file identical before and after the audit.
- Stamp: `check_stamp.txt` matches `headers.yaml` (sha256 f04e4b38...). Repo batch files untouched by this audit.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h35 | 15 / 15 | 117 | 114 | 3 | 0 |

- Rows 154 (all grade A: printed 144, single 10; primary 117, additional 37; locator p.1 header on all); recorded 117,
  no_header 0; papers ok 15, partial 0, unreadable 0; `author_list_differs` 0; `slots_from_header` 0; present
  addresses 0; prose blocks 0; `order_differs` false on all 117; explicit `slot:` 0; 8 unmapped org strings.
- Imprecise by cause: checker gap 1 (F1, hsu2025 #4); list-side name form 2 (F2, hu2020 #4, lin2023 #6). Fixable now
  in the YAML: 0.
- Per paper (slots / rows / rating): arsanjani2024 6 / 7 ok; chen2022a 5 / 7 ok; cui2023a 6 / 12 ok; deng2020 6 / 6 ok;
  fatema2026 10 / 10 ok; goyvaerts2020 9 / 15 ok; hsu2025 8 / 8 (7 ok, 1 imprecise); hu2020 7 / 7 (6 ok, 1
  imprecise); hu2021 8 / 8 ok; ito2022 4 / 4 ok; itoh2024a 15 / 21 ok; karunakaran2024 10 / 11 ok; li2025c 7 / 21 ok;
  lin2023 8 / 9 (7 ok, 1 imprecise); liu2024a 8 / 8 ok.

### Per-slot field counts (117 slots)

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot | 114 | 3 (hsu2025 #4, hu2020 #4, lin2023 #6) | 0 |
| markers + dropped_markers | 117 | 0 | 0 |
| blocks (org / unit / campus / locality / country) | 117 | 0 | 0 |
| prose blocks | n/a (none printed) | | |
| present addresses | n/a (none printed) | | |
| locators | 117 | 0 | 0 |
| parked / unreadable | n/a (none) | | |

## Per-paper findings

- arsanjani2024 (6): markers 1,2 / 1 / 1 / 1 / 2 / 1 as printed (asterisk on the last author ignored). Block 1 Silicon
  Austria Labs GmbH, Villach, AT (unmapped); block 2 Technical University of Berlin, Berlin, DE (alias to
  `org_tu_berlin`). Postal codes not recorded. ok.
- chen2022a (5): Shengbao Wu 3,4 with 4 = contact (verified). Block 1 Southeast University with the research-center +
  school chain printed before it (contiguous), Nanjing, CN; block 2 Purple Mountain Laboratories, Nanjing (province not
  recorded, D288); block 3 Hebei University with the two-center + college chain, Baoding, CN (unmapped, also h34). ok.
- cui2023a (6): every author 1,2. Block 1 Huazhong University of Science and Technology + unit "Wuhan National
  Laboratory for Optoelectronics & School of Optical and Electronic Information", identical to 3 committed blocks (lit_h17, lit_h31, ofc_h03)
  (corpus split noted in D522 / h33: 4 committed blocks record WNLO as org + HUST more_orgs; rows map to the HUST id
  either way). Block 2 Optics Valley Laboratory, Wuhan, CN. ok.
- deng2020 (6): one unmarked block (`single`, authors `[]`); Shanghai University with the key-lab / joint-lab /
  institute unit chain, Shanghai, CN; street and postal code not recorded. ok.
- fatema2026 (10): Tasneem Fatema 1,3 and Andreas Beling 1,4 with 3 and 4 = contact (verified; probe F1, marker 4 as
  affiliation: 1 error). Block 2 University of Maryland + campus College Park (D301, maps to
  `org_university_of_maryland_college_park`, as yulaev2019 in h34). US state codes not recorded; country printed as USA
  -> US. List forms M. Dagenais and Andréas Beling match automatically. ok.
- goyvaerts2020 (9): Goyvaerts and Kumari 1,2,4 with 4 = equal contribution (printed footnote). Block 1 Ghent
  University-imec as printed (D426 dash-joined form; alias maps to both ids), unit Photonics Research Group, locality
  Gent as printed; block 2 Ghent University, Center for Nano- and Biophotonics, no city printed: `locality: ""` right
  (probe G1, Gent: 2 errors); block 3 Tyndall National Institute, Cork, IE, parent University College Cork not copied
  and the site name not recorded (parent rule, loi2019 precedent). List forms Agnieszka M. Gocalinska and E. Pelucchi
  match automatically. ok.
- hsu2025 (8): block 1 National Central University, Department of Electrical Engineering, Taoyuan, TW; block 2 Corning
  Incorporated, Corning, US (state code not recorded). #4 printed Chia-Hsuan Wang vs list C.-J. Wang: the second
  initial (H vs J) is not explained and Wang is a common family name, so D369 asks for `slot: 0` +
  `author_list_differs`; probe H1 (`slot: 0`) fails with the D302 error because `strict_compatible` does not compare
  initials at equal count (the h34 G1 gap). The automatic match to slot 4 (no explicit `slot:` in the YAML) is kept as
  in yeh2024 #14 / #24: imprecise, F1. Same Corning row either way. Note accurate.
- hu2020 (7): block 1 Shanghai Jiao Tong University with the state key lab + institute + department chain; block 2 SJTU,
  Center of Advanced Electronic Materials and Devices; block 3 City, University of London (official name, comma as
  printed), Department of Electrical and Electronic Engineering, London, GB (country printed as United Kingdom; postal
  code not recorded; unmapped). #4 printed Jian Xu vs list Jian Xin Xu: automatic dropped-syllable match (the checker
  treats Xin as a middle name; probe J1 `slot: 0`: D302 error). Imprecise, F2. ok otherwise.
- hu2021 (8): one marked block (1) for all; Cheng Zeng 1,2 and Jinsong Xia 1,3 with 2 and 3 = contact (verified). HUST +
  unit Wuhan National Laboratory for Optoelectronics, Wuhan, CN. ok.
- ito2022 (4): one unmarked block (`single`): The University of Tokyo (leading article as printed), School of
  Engineering, Tokyo, JP; the ward printed before the city is in the note (D366); street and postal code not recorded.
  ok.
- itoh2024a (15): markers checked one by one against the PDF layer (authors 1-6 1,2; 7-10 1; 11-15 2; Susumu Noda 2,3
  with 3 = contact, verified). Block 1 Sumitomo Electric Industries, Ltd., Transmission Devices Laboratory, Yokohama,
  JP (same org + unit as 5 committed blocks); block 2 Kyoto University, Department of Electronic Science and Engineering,
  Kyoto, JP. ok.
- karunakaran2024 (10): block 1 NKT Photonics, Birkerod (as printed, without the Danish letter), DK, street not
  recorded (unmapped); block 2 Technical University of Denmark + unit DTU Electro, Kgs. Lyngby (as committed); block 3
  Ecole Polytechnique Fédérale de Lausanne + unit Photonic Systems Laboratory (PHOSL) printed after the org (identical
  to the lit_h16 block); block 4 LIGENTEC SA, Ecublens, CH, site name not recorded (probe K1, Lausanne: 2 errors).
  #9 list Patrick Bowen Montague vs printed Patrick Montague: dropped middle name of a distinctive family name,
  automatic. Note wording N1 (minor). ok.
- li2025c (7): every author 1,2,3. Block 1 Institute of Semiconductors, Chinese Academy of Sciences (parent part of
  the printed name) + state key lab unit; block 2 University of Chinese Academy of Sciences + Center of Materials
  Science and Optoelectronics Engineering (identical to 11 committed blocks); block 3 Beijing Key Laboratory of Low
  Dimensional Semiconductor Materials and Devices printed alone with its own marker and place: recorded as an org
  (probe L1, recorded as an IoS CAS unit: 4 errors, so the org form is the only checkable form). Unmapped, org round.
  ok.
- lin2023 (8): Jian Xu 2,4 with 4 = contact (verified); Xinlun Cai 1,3. Block 1 Sun Yat-sen University + state key lab
  / school chain, Guangzhou, CN; block 2 South China University of Technology + Department of Tourism Management,
  Guangzhou, CN (printed so; recorded as printed); block 3 Hefei National Laboratory, Hefei, CN (unmapped, recurring).
  #6 printed Jian Xu vs list Jian Xin Xu (probe J2 `slot: 0`: D302 error). Imprecise, F2.
- liu2024a (8): block 1 SJTU + state key lab unit; block 2 Shanghai Optoweave Technology Co., Ltd., Shanghai, CN; block
  3 TTM Technologies + unit Technology Center, Guangzhou, CN; block 4 Peng Cheng Laboratory, Shenzhen, CN. List form
  Marika P. Immonen vs printed Marika Immonen: automatic. ok.

## Fixes (exact YAML edits; none applicable now)

| # | paper, slots | rating | evidence | edit |
|---|---|---|---|---|
| F1 | hsu2025 #4 (Chia-Hsuan Wang) | imprecise, not fixable now (checker gap; same Corning row either way) | p.1 header: printed given name Chia-Hsuan (initials C, H); list form C.-J. Wang (C, J). D369 requires every initial to be explained. Probe H1: `slot: 0` + `author_list_differs: true` -> 1 error (D302) | after the D382 checker change: add `author_list_differs: true` to the paper; `{name: "CHIA-HSUAN WANG", markers: ["2"]}` -> `{name: "CHIA-HSUAN WANG", markers: ["2"], slot: 0}`; in `note` replace "header Chia-Hsuan Wang and the list form at position 4 (C.-J. Wang) differ in the second initial: the checker counts them compatible (equal initial count) and rejects slot 0 (D302), so it takes slot 4, as yeh2024; listed for review" with "header Chia-Hsuan Wang does not agree on the second initial with the list form at position 4 (C.-J. Wang; D369): slot 0". Rows 154 -> 153, no_header 0 -> 1. Not needed if the D412 entry (question 1) lands first |
| F2 | hu2020 #4, lin2023 #6 (Jian Xu) | imprecise (slot name form only; position, markers and org right) | p.1 header of both: printed Jian Xu; both lists carry Jian Xin Xu, an unprinted second given-name syllable on a common family name. The same list form occurs 20 times in `merged.jsonl` and here on two unrelated affiliations (SJTU materials center 2020, SCUT tourism department 2023): an upstream profile display name, not the printed author. Probes J1 / J2: `slot: 0` -> D302 error; precedent jia2025 #3, song2025 #1, chen2019 #3 (D426 / D442 / D546): dropped-syllable matches accepted and listed | none in the YAML. D426 review list: hu2020 #4, lin2023 #6. D412 correction file: hu2020 #4 and lin2023 #6 list name Jian Xin Xu -> Jian Xu. The two slots do not join in the people build (D63 needs a shared org; SJTU vs SCUT) |
| N1 | karunakaran2024 note | wording (no row affected) | block 3 prints EPFL then the laboratory; no school is printed | in `note` replace "block 3 prints the laboratory after the school (unit, as an earlier batch)" with "block 3 prints the laboratory after the organization (unit, as lit_h16)" |

Any change to the YAML changes its hash: re-run `check lit_h35 --corpus lit` afterwards to refresh the stamp.

## Open questions (with recommendation)

1. hsu2025 #4 author list: add a D412 correction entry (position 4 C.-J. Wang -> printed Chia-Hsuan Wang)? Then the
   automatic match is exact and F1 is moot. Recommended: yes; until then keep the automatic match (yeh2024 #14 / #24
   precedent) and put hsu2025 #4 on the D426 review list next to them.
2. F2: accept the two Jian Xu dropped-syllable matches, list them for review (D426) and add both to the D412 correction
   file? Recommended: yes. The 20 "Jian Xin Xu" list entries in `merged.jsonl` suggest a corpus-wide sweep of that
   form in the D412 pass.
3. D382 checker change: hsu2025 is the fourth case (with lai2025 and yeh2024 #14 / #24) of equal-count initials not
   compared. Recommended: implement, then re-check lit_h14 / lit_h30 / lit_h34 / lit_h35.
4. N1 note wording: apply with the next batch edit. Recommended: yes (cosmetic).
5. li2025c block 3: keep Beijing Key Laboratory of Low Dimensional Semiconductor Materials and Devices as its own org
   (printed alone with its own marker and place; probe L1 shows the unit form is not checkable) and decide host /
   alias in the org round. Recommended: yes.

## Unmapped org strings (org round; no YAML change)

| org | unit | country | rows | paper |
|---|---|---|---|---|
| Beijing Key Laboratory of Low Dimensional Semiconductor Materials and Devices | | CN | 7 | li2025c |
| City, University of London | Department of Electrical and Electronic Engineering | GB | 1 | hu2020 |
| Hebei University | Photonics Information Innovation Center and Hebei Provincial Center for Optical Sensing Innovations, College of Physics Science and Technology | CN | 1 | chen2022a |
| Hefei National Laboratory | | CN | 1 | lin2023 |
| NKT Photonics | | DK | 3 | karunakaran2024 |
| Shanghai Optoweave Technology Co., Ltd. | | CN | 1 | liu2024a |
| Silicon Austria Labs GmbH | | AT | 5 | arsanjani2024 |
| TTM Technologies | Technology Center | CN | 1 | liu2024a |

None of the 8 names is in `data/registry/organizations.csv`; Hebei University and Hefei National Laboratory recur from
earlier batches (h34, D546).

## Privacy and as-printed scan

- Grep over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`, `papers.csv`, `check_stamp.txt` and
  this record for contact / URL patterns, street, site and building words, and digit runs of 4 or more: 0 contact or URL
  hits; street words only in notes that say such text was not recorded; digit runs only paper-id years and the stamp
  hash. No postal code, street, site or building text in any field.
- As printed (kept, correct): Gent (goyvaerts2020 block 1), Birkerod, Kgs. Lyngby, Ecole Polytechnique Fédérale de
  Lausanne without the accent on the first letter, City, University of London with its comma, The University of Tokyo
  with the article, the ampersand in the cui2023a unit. No `skip_prefix` or `skip_between` in this batch.

## Commands (2026-11-09, log times)

| Command | Result |
|---|---|
| `check lit_h35 --corpus lit --dry-run` 19:15:21 (pid 80142) | 0 errors, 0 warnings; slots 117, recorded 117; rows 154 (grade A 154; primary 117, additional 37; printed 144, single 10); papers ok 15; multi-affiliation slots 30; present addresses 0; 8 unmapped org strings |
| `show lit_h35 --corpus lit --codes <id> --pdf`, all 15 | headers and author lists read (scratchpad only) |
| `probes/probe.py` on scratch copies, dry-run, 19:19:30 (pid 89361) | below; repo batch files md5 unchanged; the dry-run check writes its usual log files under `logs/` |

| probe | change | result | reading |
|---|---|---|---|
| H1 | hsu2025 Chia-Hsuan Wang `slot: 0` + `author_list_differs` | 1 error (D302, matches slot 4) | F1 blocked by the checker |
| J1 | hu2020 Jian Xu `slot: 0` + `author_list_differs` | 1 error (D302, matches slot 4) | dropped syllable compatible by rule |
| J2 | lin2023 Jian Xu `slot: 0` + `author_list_differs` | 1 error (D302, matches slot 6) | same |
| G1 | goyvaerts2020 block 2 locality Gent | 2 errors (not in block) | empty locality required |
| K1 | karunakaran2024 block 4 locality Lausanne | 2 errors (not in block) | Ecublens is the printed city |
| F1 | fatema2026 Beling marker 4 as affiliation | 1 error (no block) | contact marker must be dropped |
| L1 | li2025c block 3 as IoS CAS org + key-lab unit | 4 errors (org not in block, not contiguous) | own-org form is the checkable one |

## Checker gaps observed (scripts not edited)

- G1 (= h34 G1) `strict_compatible` (D369 / D382): equal initial counts skip the initial comparison, so C.-J. ~
  Chia-Hsuan passes and `slot: 0` is rejected by D302.

## Verdict

GO. No slot carries a wrong person, org, city, country or marker, nothing is invented, no block is missed, and no
address or contact text is recorded. 3 slots keep list name forms that differ from the print (hsu2025 #4 second
initial; hu2020 #4 and lin2023 #6 unprinted syllable); their rows carry the right org, and they wait on the D412 list
correction or the D382 checker change.
