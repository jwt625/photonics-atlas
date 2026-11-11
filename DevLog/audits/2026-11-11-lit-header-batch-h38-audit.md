---
title: Fresh-context audit of the lit author-affiliation batch lit_h38 (11 papers)
date: 2026-11-11
auditor: Claude (fresh context; wrote only this record; headers.yaml, derived files, scripts, tests, people and registry data not edited; check run only with --dry-run, probes on a scratch copy; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h38/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D400-D550); format from the 2026-11-09 h36 audit
verdict: GO for the people rebuild (no slot wrong); 76 slots audited, 76 ok, 0 imprecise, 0 wrong; zeng2023 #4 #5 unreadable confirmed (block 2 prints no organization anywhere); zhang2026b slot 6 (X. STEVE YAO / Steve Yao) confirmed; yang2021 and zhang2024 ampersand unit chains confirmed; no YAML fix needed; one checker gap (G1, zhang2024 last author's second marker not bound)
---

# Lit header batch audit: lit_h38 (2026-11-11)

## Scope

Batch lit_h38 (11 papers, all Optics Express research articles with capitals author lines; 76 author-list slots, no
header-only author; 81 rows). Restricted corpus: this record names only authors, orgs, units, cities and countries; no
paper text is quoted and no contact, street, building, postal-box or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h38 --corpus lit --codes <id> --pdf`
  (all 11; output kept in the session scratchpad only). Every header and block is on page 1; no `--pages` needed (no
  cover page, no later-page affiliation list). Markers legible and identical in both layers in all 11.
- Per slot: printed name vs `compare.csv` slot and the author list printed by `show`; printed marker run vs `markers` +
  `dropped_markers`; block fields vs the print (org, unit chain, campus, city, country); locator; parents; present
  addresses. All 25 distinct (paper, marker, org, unit, place, org id, role) tuples of `header_rows.csv` read; no wrong
  mapping.
- Contact markers: yang2021 markers 2 and 3, zhang2024 markers 3 and 4 checked by the leading character of the masked
  contact lines in `text.md` (contents not printed): the lines start with 2 / 3 and 3 / 4, so `dropped_markers` with
  reason contact footnote is right. The other 9 papers mark their contact line with an asterisk only. The daggers in
  zhang2024 and zhang2026b point to a printed equal-contribution line and are symbol marks (no entry needed).
- Missed blocks: cue scan of the whole `text.md` of all 11 (now with / at, present / current address, present / current
  affiliation, currently, presently, is / are / was / were (also / now) with, also with, on leave, visiting, formerly,
  deceased, permanent address, affiliat-). 4 hits, all body text (poulsen2025 p.2, shi2023 p.1, sun2022a p.1, wang2026g
  p.1, each after the abstract). No present address, prose statement or later-page affiliation list. No missed block.
- zeng2023: whole `text.md` (11 pages) searched for the names of authors 4 and 5, company / institute words and the
  funding, acknowledgment and disclosure sections: no organization is printed for them anywhere (details below).
- Claims tested with dry-run probes on scratch copies of the batch (`probes/probe.py`, `probes/probe2.py` in the session
  scratchpad, via the module's `LIT_BASE`); md5 of every repo batch file identical before and after the audit.
- Stamp: `check_stamp.txt` matches `headers.yaml` (sha256 7005d4f1...). Repo batch files untouched by this audit.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h38 | 11 / 11 | 76 | 76 | 0 | 0 |

- Rows 81 (all grade A: printed 70, single 11; primary 74, additional 7; all locators p.1 header); recorded 74,
  no_header 2 (zeng2023 #4 #5); papers ok 10, partial 1 (zeng2023), unreadable 0; `author_list_differs` 0; explicit
  slots 1 (zhang2026b #6, needed: probe Y1); present addresses 0; prose blocks 0; `order_differs` false on every slot;
  9 unmapped org strings; multi-affiliation slots 7.
- ok includes zeng2023 #4 #5 (no organization printed: unreadable is the contract outcome, lit_h17 kang2008 #13 /
  kang2008a #8 precedent) and zhang2024 #8 (record exact; its second marker is not bound by the checker, G1).
- Per paper (slots / rows / rating): poulsen2025 2 / 2 ok; shi2023 6 / 6 ok; sun2022a 2 / 2 ok; tahara2024 10 / 10 ok;
  wang2026g 8 / 11 ok; yang2021 4 / 4 ok; zeng2023 7 / 5 ok (2 unreadable by contract); zhang2021a 15 / 17 ok; zhang2024
  8 / 8 ok; zhang2026 7 / 7 ok; zhang2026b 7 / 9 ok.

### Per-slot field counts (76 slots)

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (76, incl. 2 unreadable) | 76 | 0 | 0 |
| markers + dropped_markers (74 recorded) | 74 | 0 | 0 |
| blocks (org / unit / campus / locality / country) (74 recorded) | 74 | 0 | 0 |
| prose blocks | n/a (none printed) | | |
| present addresses | n/a (none printed) | | |
| locators (74 recorded) | 74 | 0 | 0 |
| unreadable authors (2 slots) | 2 (zeng2023 #4 #5) | 0 | 0 |

## Per-paper findings

- poulsen2025 (2): single unmarked block (`single`, authors `[]`; asterisk = corresponding author), org The University
  of Western Ontario with its leading article as printed (D288), unit Department of Electrical and Computer
  Engineering, London, CA (province printed after the city, not recorded). Unmapped (org round). ok.
- shi2023 (6): marker runs 1 / 1 / 1,* / 2 / 3 / 1. Block 1 Shanghai Jiao Tong University + State Key Laboratory of
  Advanced Optical Communication Systems and Networks, Shanghai, CN; block 2 TTM Technologies with the unit Technology
  Center printed after the org, Guangzhou, CN; block 3 TTM Technologies, Shanghai, CN (two places, two blocks; street
  text not recorded). List #4 Marika P. Immonen vs printed MARIKA IMMONEN: automatic. ok.
- sun2022a (2): single unmarked block, Zhejiang University + College of Information Science and Electronic
  Engineering, Hangzhou, CN (`org_zhejiang_university`). ok.
- tahara2024 (10): marker runs 1 x5, 2 x4, 1,* (Baba; probe T1 with an added 2: 2 errors, bound). Block 1 Yokohama
  National University + Department of Electrical and Computer Engineering, locality Yokohama (ward printed before the
  city in the note, D366), JP; block 2 National Institute of Advanced Industrial Science and Technology (AIST), Tsukuba,
  JP (alias to the AIST id). List #9 Kôji Yamada vs KOJI YAMADA: automatic. ok.
- wang2026g (8): marker runs 1,2 / 1,3 / 1 / 1 / 1 / 1,2 / 1 / 1,* (probe W1 bound). Block 1 Imec (capital I as
  printed; `org_imec`), Leuven, BE; block 2 KU Leuven + Department of Physics and Astronomy, Leuven, BE; block 3 Brno
  University of Technology + Faculty of Mechanical Engineering (FME), Brno, CZ (unit printed before the org). List #2 is
  in capitals (TEREZA BACOVA; question 3). ok.
- yang2021 (4): one block printed with marker 1 (`printed`, D285). Marker runs 1,2 / 1 / 1,3 / 1, with 2 and 3 =
  contact lines (verified; probe B3 without the dropped 2: 2 errors). Unit chain: the state key laboratory and two joint
  labs (Alferov Russian-Chinese Joint Lab ..., BUPT-Hengtong Joint Lab ...) joined by ampersands, then Beijing University
  of Posts and Telecommunications, Beijing, CN. The whole chain as one unit is required (probe B1, unit cut to the state
  key laboratory: 2 errors, not contiguous; probe B2, last joint lab only: 2 errors) and right: the joint labs are
  printed as sub-units before BUPT, no partner organization is printed as its own org, same form as lit_h34 (state key
  laboratory & school, BUPT org) and the OFC BUPT blocks. ok.
- zeng2023 (7): marker runs 1 / 1 / 1 / 2 / 2 / 1 / 1,*. Block 1 Jilin University + State Key Laboratory of Integrated
  Optoelectronics, College of Electronic Science and Engineering, Changchun, CN. Block 2 prints only an address and the
  place Changchun, China in both layers; no organization name. Searched further: the author line and the two blocks are
  the only affiliation text; the funding line names a national programme only, the disclosure line names no org, there
  is no acknowledgment section and no footnote or prose statement; the names Junfeng Yang / Jun Yan occur only in the
  author line (one J. Yang in a reference-list author string, a different paper). Authors 4 and 5 `unreadable: true`
  with `markers: []`, status partial: correct under never-guess (lit_h17 kang2008 #13, kang2008a #8). Probe Z1 (both with
  marker 2 and no block 2): 4 errors, so the block cannot be dropped silently. An org must not be inferred from the
  address. ok.
- zhang2021a (15): marker runs 1 / 1 / 1 / 2 / 1 / 1 / 3 / 1 / 1 / 1 / 1,3 / 1 / 4 / 4 / 1,3,*. Blocks Jilin University
  (same unit chain as zeng2023), Changchun Institute of Optics, Fine Mechanics and Physics, Chinese Academy of Sciences +
  State Key Laboratory of Luminescence and Application (same org string as the earlier lit request), Changchun; Peng
  Cheng Laboratory, Shenzhen; all CN; block 4 Advance Micro Foundry Pte Ltd, Singapore, SG (printed without the d in both
  layers; probe A1 with the registry spelling: 2 errors, so as printed is required; the science-park text is address,
  locality Singapore). List #6 Bo-Song Chen vs BOSONG CHEN and #14 with a non-ASCII hyphen: automatic. ok.
- zhang2024 (8): marker runs 1,dagger / 1,dagger / 2 / 1 / 1 / 1 / 1,3 / 1,4; 3 and 4 = contact lines (verified). Block 1
  Huazhong University of Science and Technology + Wuhan National Laboratory for Optoelectronics & School of Optical and
  Electronic Information, Wuhan, CN: the identical org + unit string is committed in lit_h17, lit_h31 and ofc_h03, and the
  WNLO-as-org form (lit_h02, lit_h18, lit_h21, lit_h26, lit_h28) is used only where WNLO is printed as its own org; whole
  chain required (probe H1, WNLO only: 2 errors). Block 2 Ningbo Ori-Chip Optoelectronics Technology Ltd., Ningbo, CN.
  Weihua Guo (name split across two lines) carries `dropped_markers` 4 as printed, but the checker does not bind his
  second marker (G1: probe H2 without it and H4 with 5 instead of 4 both pass, 0 errors; Qiaoyin Lu's 3 is bound, probe
  H3: 2 errors). Record exact. ok.
- zhang2026 (7): single unmarked block, Jilin University + State Key Laboratory of Integrated Optoelectronics, College of
  Electronic Science and Engineering, College of Integrated Circuits, Changchun, CN. ok.
- zhang2026b (7): marker runs 1,2,dagger / 1,dagger / 3 / 1 / 2,4 / 1 / 1,* (probe L1 bound). Blocks Hebei University
  (centre / provincial centre / college chain, comma-separated as printed here; lit_h13 lin2022 prints the first two
  joined by "and"), Baoding; Southeast University (national research center + school), Nanjing (`org_southeast_university`);
  Fuzhou University (institute + school), Fuzhou; Purple Mountain Laboratories, Nanjing (province printed after the city,
  not recorded; `org_purple_mountain_laboratories`); all CN. Author 6 printed X. STEVE YAO, list #6 Steve Yao: the
  strict lit matcher finds 0 candidates without the explicit slot (probe Y1: 2 errors) and `slot: 0` fails because the
  list name stays unmatched (probe Y2: 1 error, D302). `slot: 6` is right: D287 name-part variant (a leading given-name
  part dropped, as Seyed Morteza / Morteza; OFC precedent ofc_h02 M. Sezer Erkilinç -> slot 8 Sezer Erkilinc); every
  part of the list form is printed, the list holds one Yao, printed and list positions agree (6 of 7), and the D369
  objection (an initial contradicting a full given name, Siyuan / S. F.) does not arise. lit_h13 lin2022 #11 has the
  list form X. Steve Yao (question 1). ok.

## Fixes (exact YAML edits)

None. No slot, marker, block field, locator or note needs a change; the explicit slot is required (probe Y1).

## Open questions (with recommendation)

1. zhang2026b #6: keep `slot: 6`. The list form Steve Yao lacks the leading initial that lit_h13 lin2022 #11 (list X.
   Steve Yao) carries, so the people build may not join the two slots. Recommended: add zhang2026b #6 to the D426 review
   list now (leading-initial name-part variant, explicit slot) and to the D412 correction-file candidates as a
   low-priority entry (Steve Yao -> X. Steve Yao), as hu2020 #4 / lin2023 #6 in D550.
2. G1 (zhang2024 #8): the checker does not bind the second marker of the last author when his name is split over two
   lines and the run is followed by the block list. Recommended: add zhang2024 #8 as a test case to the D442 / D546
   last-author marker-window gap (chen2024b #6, chen2018); no re-record needed (YAML already exact).
3. wang2026g #2: author-list name in capitals (TEREZA BACOVA would become the slot name). Recommended: D412 correction
   file, low-priority display fix (piyush2026 #1 precedent, D550).
4. zeng2023 #4 #5: keep `unreadable` (no organization printed anywhere in the paper). Recommended: yes; never resolve
   from the address.

## Unmapped org names (org round, no YAML change)

| printed org (unit) | place | proposal |
|---|---|---|
| Advance Micro Foundry Pte Ltd | Singapore, SG | lit-scoped printed-variant alias to `org_amf` (registry name Advanced Micro Foundry; printed typo) |
| Brno University of Technology (Faculty of Mechanical Engineering (FME)) | Brno, CZ | new org (no registry entry, no earlier request) |
| Changchun Institute of Optics, Fine Mechanics and Physics, Chinese Academy of Sciences (State Key Laboratory of Luminescence and Application) | Changchun, CN | new org (same string already requested in `lit_headers/org_requests.csv`) |
| Fuzhou University (institute + school) | Fuzhou, CN | new org (requested from yu2025, zhu2025) |
| Hebei University (centre / college chain) | Baoding, CN | new org (requested from lin2022 and others) |
| Ningbo Ori-Chip Optoelectronics Technology Ltd. | Ningbo, CN | new org; same company as the requested "... LTD" form (lu2024): one org, both printed forms as aliases |
| TTM Technologies (Technology Center) | Guangzhou, CN | new org (requested from liu2024a) |
| TTM Technologies | Shanghai, CN | same org as the row above |
| The University of Western Ontario (Department of Electrical and Computer Engineering) | London, CA | new org (no registry entry, no earlier request) |

## Privacy and as-printed scan

- Grep over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`, `papers.csv`, `check_stamp.txt` and
  this record for contact / URL patterns, the street and building words of the printed blocks, and digit runs of 4 or
  more: 0 contact or URL hits; the words street / address only in notes that say such text was not recorded (zeng2023
  names only the kinds of address parts, not their text); digit runs only paper-id years, the stamp hash and the log pid. No postal
  code, street or building text in any field. tahara2024 note names the ward printed before the city (allowed, D366).
- As printed (kept, correct): zhang2021a Advance Micro Foundry Pte Ltd; wang2026g Imec; poulsen2025 The University of
  Western Ontario (leading article); zhang2024 Ltd. with period; ampersand unit chains in yang2021 and zhang2024. No
  `skip_prefix` or `skip_between` in this batch.

## Commands (2026-11-11, log times)

| Command | Result |
|---|---|
| `check lit_h38 --corpus lit --dry-run` 00:16:04 (pid 55207) | 0 errors, 1 warning (zhang2026b explicit slot 6); slots 76, recorded 74, no_header 2; rows 81 (grade A 81; primary 74, additional 7; printed 70, single 11); papers ok 10, partial 1; multi-affiliation slots 7; present addresses 0; 9 unmapped org strings |
| `show lit_h38 --corpus lit --codes <id> --pdf`, all 11 | headers and author lists read (scratchpad only) |
| `probes/probe.py`, `probes/probe2.py` on scratch copies, dry-run, 00:18:14-00:19:52 | below; repo batch files md5 unchanged; the dry-run check writes its usual log files under `logs/` |

| probe | change | result | reading |
|---|---|---|---|
| Y1 | zhang2026b X. STEVE YAO without `slot: 6` | 2 errors (0 candidates, slot 6 unmatched) | explicit slot required |
| Y2 | same with `slot: 0` | 1 error (slot 6 unmatched) | slot 0 not allowed (D302) |
| B1 | yang2021 unit cut to the state key laboratory | 2 errors (not contiguous) | whole ampersand chain required |
| B2 | yang2021 unit = last joint lab only | 2 errors (first field not found) | same |
| B3 | yang2021 Yang without dropped marker 2 | 2 errors | contact marker bound |
| H1 | zhang2024 unit cut to WNLO | 2 errors (not contiguous) | whole ampersand chain required |
| H2 | zhang2024 Guo without dropped marker 4 | 0 errors | G1: last author's second marker not bound |
| H3 | zhang2024 Qiaoyin Lu without dropped marker 3 | 2 errors | contact marker bound |
| H4 | zhang2024 Guo dropped marker 5 instead of 4 | 0 errors | G1 confirmed |
| A1 | zhang2021a org Advanced Micro Foundry Pte Ltd | 2 errors | printed spelling required |
| Z1 | zeng2023 #4 #5 with marker 2, no block 2, status ok | 4 errors | unreadable required |
| L1 | zhang2026b Lei Zhang without marker 2 | 2 errors | markers bound |
| T1 | tahara2024 Baba with markers 1, 2 | 2 errors | markers bound |
| W1 | wang2026g Neutens with markers 1, 2 | 2 errors | markers bound |

## Checker gaps observed (scripts not edited)

- G1 Second marker of the last author not bound when the name is split over two lines before the block list
  (zhang2024 #8, printed 1,4): a missing or wrong dropped marker passes. Related to the D442 / D546 last-author marker
  gap (chen2024b, chen2018). The YAML is exact; nothing waits on it.

## Verdict

GO. No slot carries a wrong person, org, city, country or marker, nothing is invented, no block is missed, and no
address or contact text is recorded. zeng2023 #4 #5 stay unreadable (no organization printed anywhere); zhang2026b
slot 6 is a valid D287 name-part variant; the ampersand unit chains of yang2021 and zhang2024 are copied whole as
required. No YAML fix; questions 1-3 are list entries for D426 / D412 and the checker gap list.
