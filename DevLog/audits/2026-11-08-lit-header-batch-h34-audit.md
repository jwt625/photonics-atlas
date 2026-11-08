---
title: Fresh-context audit of the lit author-affiliation batch lit_h34 (15 papers)
date: 2026-11-08
auditor: Claude (fresh context; wrote only this record; headers.yaml, derived files, scripts, tests, people and registry data not edited; aggregate and the people build not run; check run only with --dry-run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h34/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D406-D522); format from the 2026-11-06 h27 audit
verdict: GO for the people rebuild (no slot wrong); 152 slots audited, 150 ok, 2 imprecise, 0 wrong; no YAML edit needed now; F1 (2 slots, yeh2024 second-initial mismatch) waits on the D382 checker change; yeh2024 author list goes to the D412 correction file; nothing applied
---

# Lit header batch audit: lit_h34 (2026-11-08)

## Scope

Batch lit_h34 (15 papers: 7 Optica-publishing journal papers (Optics Express 6, Optics Letters 1), 2 Nature-family
papers, 1 IEDM paper, 1 CLEO paper, 1 ACS Just Accepted manuscript, 1 APL Photonics paper with a cover page, 2
manuscript layouts (yu2016 arXiv form of an Optica paper, zhou2025 manuscript of a Laser Photonics Rev. paper); 152
author-list slots plus 12 header-only authors; 173 rows). Restricted corpus: this record names only
authors, orgs, units, cities and countries; no paper text is quoted and no contact, street, building, postal-box or
postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h34 --corpus lit --codes <id> --pdf`
  (all 15; output kept in the session scratchpad only); yulaev2019 and zhang2016 also with `--pages 2` (cover pages,
  marked author line and blocks on page 2). Both text layers carry every marker legibly (zhang2024c markers on the next
  line in the text layer, read in the PDF layer; zhou2025 letter markers; zhou2022b parenthesized leading block markers).
  No page render needed.
- Per slot: printed name vs `compare.csv` slot and the author list printed by `show`; printed marker run vs `markers` +
  `dropped_markers`; block fields vs the print (org, unit chain, campus, city, country); locator; parents; present
  addresses. All 49 distinct (paper, org, unit, place, org id) tuples of `header_rows.csv` read; no wrong mapping.
- Contact markers: the masked contact lines of yang2026a (markers 4, 5), zhang2022a (marker 3), zhong2026 (marker 7) and
  zhang2016 (marker a) were checked in `text.md` by their leading character only (contents not printed): each is a
  contact line, so `dropped_markers` with reason contact footnote is right.
- Missed blocks: cue scan of the whole `text.md` of all 15 (now with / at, present / current address, present / current
  affiliation, currently, presently, is / are / was / were with, also with, on leave, visiting, formerly, deceased,
  permanent address). 5 hits, all body text on later pages (yu2016 p.5, yulaev2019 p.2 abstract and p.12, zhuang2016
  p.8 and p.11). No present address, prose statement or later-page affiliation list in any paper. No missed block.
- Claims and contract calls tested with dry-run probes on scratch copies of the batch (`probes/probe.py` in the session
  scratchpad, via the module's `LIT_BASE`); md5 of every repo batch file identical before and after the audit.
- Stamp: `check_stamp.txt` matches `headers.yaml` (sha256 d108e350...). Repo batch files untouched by this audit.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h34 | 15 / 15 | 152 | 150 | 2 | 0 |

- Rows 173 (all grade A: printed 139, single 34; primary 150, additional 23; locators p.1 header 117, p.1 footnote 38,
  p.2 header 18); recorded 150, no_header 2 (yeh2024 #28, #30); papers ok 15, partial 0, unreadable 0;
  `author_list_differs` 1 (yeh2024: 12 header-only authors and 2 initial mismatches with `slot: 0`); present addresses 0;
  prose blocks 0; `order_differs` false on all 152; 13 unmapped org strings.
- Imprecise by cause: checker gap 2 (F1, yeh2024 #14 #24). Fixable now: 0.
- Per paper (slots / rows / rating): yang2026a 3 / 4 ok; yeh2024 30 / 28 (28 ok incl. the two correct no_header slots,
  2 imprecise); yu2016 5 / 6 ok; yulaev2019 7 / 11 ok; zhang2014 9 / 10 ok; zhang2015 4 / 4 ok; zhang2016 7 / 7 ok;
  zhang2019b 8 / 13 ok; zhang2022a 7 / 7 ok; zhang2024c 22 / 25 ok; zhao2026a 2 / 2 ok; zhong2026 14 / 15 ok; zhou2022b
  15 / 15 ok; zhou2025 11 / 16 ok; zhuang2016 8 / 10 ok.

### Per-slot field counts (152 slots)

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot | 150 | 2 (yeh2024 #14, #24) | 0 |
| markers + dropped_markers | 152 | 0 | 0 |
| blocks (org / unit / campus / locality / country) | 152 | 0 | 0 |
| prose blocks | n/a (none printed) | | |
| present addresses | n/a (none printed) | | |
| locators | 152 | 0 | 0 |
| parked / unreadable | n/a (none) | | |

## Per-paper findings

- yang2026a (3): author line in capitals; markers 1,2 / 2,4 / 3,5; 4 and 5 are contact lines (dropped, verified).
  Block 2 records the printed centre / key-laboratory chain before Lanzhou University as one unit chain (contiguous; the
  Gansu and MoE laboratories are printed as sub-units of the university, no second org printed). City Xi'an with the
  printed apostrophe. ok.
- yeh2024 (30 slots, 42 printed): one unmarked block (Taiwan Semiconductor Manufacturing Company, Hsinchu, Taiwan ->
  TW), `single`, all authors `[]`. Printed order equals the list order for positions 1-30; the list stops at 30
  (printed 31-42, J.Y. Lin to S.F. Huang, `slot: 0`, correct). #28 printed Y.M. Wang vs list Yike Wang and #30 printed
  S.M. Wu vs list Saijun Wu: the second initial is not explained, common family names: `slot: 0` (D369) correct; probe
  Y3 (slot removed) fails with 0 candidates, probe Y4 (forced `slot: 30`) passes with a warning only, so slot 0 is the
  rule call, not a checker requirement. #14 printed K.Q. Wen vs list Kai-Shin Wen and #24 printed C.Y. Tsai vs list
  Chia-Heng Tsai: second initial disagrees (Q vs S, Y vs H); under D369 these would also be `slot: 0`, but
  `strict_compatible` skips the initial comparison when both forms have the same number of initials, and probes Y1 / Y2
  (`slot: 0`) fail with D302. Kept matched, as lit_h14 (Yan-Qing Lu vs Y. H. Lu) and lit_h30 (Y. Y. Lai, T.R. Chen):
  imprecise, F1. The other full-name list forms (Chih-Ming Hung, Jinghai Yang, Chun Hui Huang, Tsung-Han Wu, Fuchun
  Huang) agree on every initial. Note accurate.
- yu2016 (5): arXiv layout; Mengjie Yu 1,2 (asterisk = corresponding author); blocks print US state codes and no
  country: `country: ""` correct (probe Z4, US on block 1: 2 errors). Michal Lipson vs list Michal F. Lipson: dropped
  middle initial, automatic. ok.
- yulaev2019 (7): page 1 is the ACS cover; author line and blocks on page 2, every block `p.2 header` (D366). Block 2
  University of Maryland + campus College Park (D301 contract example), maps to `org_university_of_maryland_college_park`.
  Amit Agrawal vs list Amit Kumar Agrawal, Daron A. Westly vs Daron Westly: automatic. ok.
- zhang2014 (9): block 1 Institute of Microelectronics, Singapore, SG; A*STAR parent not copied (contract example);
  maps to `org_astar_ime`. Block 2 Jilin University with the state key laboratory + college chain, Changchun, CN. Junfeng
  Song 1,2 (probe Z3, marker 2 removed: 3 errors). ok.
- zhang2015 (4): single unmarked block, University of Ottawa, laboratory + school chain, Ottawa, CA. ok.
- zhang2016 (7): AIP cover on page 1; author line and blocks on page 2 (`p.2 header`). Block 2 The University of
  Massachusetts + campus Boston (D301), locality Boston; unmapped (campus not in the registry, correct per D301). Yikai Su
  marker a = contact (dropped, verified). ok.
- zhang2019b (8): Nature letter; blocks at the foot of page 1, `p.1 footnote` on all 6 (h27 F1 practice). Marker 7 =
  equal contribution (Mian Zhang, Brandon Buscaino, Cheng Wang; dropped). Block 4 City University of Hong Kong, place
  printed as Hong Kong, China -> HK (contract; probe Z1 shows CN would also pass, so HK is the contract call, consistent
  with every committed City University / CUHK block). Block 5 Howard University, Washington, US (unmapped). ok.
- zhang2022a (7): capitals; markers 1 / 2 alternate as printed; Jinbiao Xiao marker 3 = contact (verified). Hebei
  University unit chain unmapped (org round). ok.
- zhang2024c (22): Nature Communications; `p.1 footnote` on all 5 blocks; marker 6 = equal contribution (authors 1-3).
  Markers read from the PDF layer where the text layer wraps them (Lin Chang 1,5; Xingjun Wang 1,3,5; John E. Bowers 2).
  Block 2 University of California + campus Santa Barbara (printed without comma, D449), maps to `org_ucsb`. Block 3
  Peking University Yangtze Delta Institute of Optoelectronics as one org (printed name; maps to its own id). ok.
- zhao2026a (2): single unmarked block, University of Stuttgart, institute + research center unit, Stuttgart, DE. Harald
  Giessen vs list Harald W. Giessen: automatic. ok.
- zhong2026 (14): capitals; dagger / asterisk symbols ignored; Bo Liu 4,5,7 with 7 = contact (verified). Block 5 unit
  The Institute of Optics and Electronics printed before the university (contiguous chain). Two companies (ZTE Photonics,
  Jiangsu Hengtong) unmapped. ok.
- zhou2022b (15): CLEO layout, parenthesized leading markers; Lumentum Inc., San Jose and Facebook Inc, Menlo Park with US
  state codes and no country: `country: ""` correct (D249). ok.
- zhou2025 (11): letter markers a-g; block d (University of Chinese Academy of Sciences) carried by no author (Ya Cheng
  prints a, b, c, e, f, g): not recorded, noted, correct. Block c SIOM org form with both parenthesized acronyms and the
  laboratory + CAS centre unit identical to the committed lit_h-batch SIOM blocks. #8 printed Jian Liu, list J. Liu
  (abbreviated list form, automatic; slot name will be the list form, not a D412 truncation). ok.
- zhuang2016 (8): block 2 CUDOS prints only Australia: locality empty (probe Z2, Clayton: 2 errors). Blocks 4 and 5
  (SATRAX BV, LioniX BV, Enschede, NL) print a postal box, not recorded; no `skip_between` needed (org first). Monash and
  RMIT blocks with state codes, not recorded. Arthur J. Lowery vs list Arthur James Lowery: automatic. ok.

## Fixes (exact YAML edits; none applicable now)

| # | paper, slots | rating | evidence | edit |
|---|---|---|---|---|
| F1 | yeh2024 #14 (K.Q. Wen), #24 (C.Y. Tsai) | imprecise, not fixable now (checker gap; same TSMC block either way, so no row carries a wrong org) | p.1 header: printed second initials Q and Y; list forms Kai-Shin Wen and Chia-Heng Tsai explain S and H. D369 requires every initial to be explained. Probes Y1 / Y2: `slot: 0` -> 1 error each (D302), because `strict_compatible` returns true without comparing initials when both forms have the same initial count | after the D382 checker change (compare initials also at equal count): `{name: "K.Q. Wen", markers: []}` -> `{name: "K.Q. Wen", markers: [], slot: 0}`; `{name: "C.Y. Tsai", markers: []}` -> `{name: "C.Y. Tsai", markers: [], slot: 0}`; in `note` replace "header K.Q. Wen and C.Y. Tsai match list positions 14 and 24 (Kai-Shin Wen, Chia-Heng Tsai) although the second initial differs: the checker counts them compatible (equal initial count) and rejects slot 0 (D302), so they take those slots; listed for review" with "header K.Q. Wen and C.Y. Tsai do not agree on the second initial with the list forms at positions 14 and 24 (Kai-Shin Wen, Chia-Heng Tsai; D369): slot 0". Rows 173 -> 171, no_header 2 -> 4. Not needed if the D412 correction (question 1) lands first |

Any change to the YAML changes its hash: re-run `check lit_h34 --corpus lit` afterwards to refresh the stamp.

## Open questions (with recommendation)

1. yeh2024 author list: the cached list stops at 30 of 42 printed authors, and positions 14, 24, 28, 30 carry full names
   whose initials disagree with the print (positions otherwise align one to one with the printed order). Recommended:
   D412 correction file entry for yeh2024 (append printed 31-42; replace the four list forms by the printed forms),
   which makes all 42 match and removes F1 and the two no_header slots. Until then keep the YAML as is.
2. F1 itself: until the D412 entry exists, keep the automatic matches #14 #24 (lit_h14 / lit_h30 precedent) and add
   them to the D426 review list. Recommended: yes.
3. D382 checker change: extend `strict_compatible` to compare initials position by position also when both forms have
   the same initial count (yeh2024 shows the gap with two cases in one paper; lit_h14 and lit_h30 kept three such
   matches). Recommended: yes, then re-check lit_h14 / lit_h30 / lit_h34.
4. Org round (no YAML change): 13 unmapped strings, among them Monash University, RMIT University, Howard University,
   Hebei University, Hefei National Laboratory, SiFotonics, ZTE Photonics, Jiangsu Hengtong, Facebook Inc (Meta),
   SATRAX BV, LioniX BV (alias to `org_lionix_international`, as D540), CUDOS, and The University of Massachusetts,
   Boston (needs a campus org, D301).

## Privacy and as-printed scan

- Grep over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`, `papers.csv`, `check_stamp.txt` and
  this record for contact / URL patterns, street and building words, postal-box codes and digit runs of 4 or more: 0
  contact or URL hits; street / postal-box words only in notes that say such text was not recorded; digit runs only
  paper-id years, dates, the stamp hash and log times. No postal code, street or building text in any field.
- As printed (kept, correct): yang2026a Xi'an with a typographic apostrophe; zhang2014 laboratory name in lower-case
  opto-electronics; zhang2016 leading article The; zhou2022b Facebook Inc without a period; zhuang2016 Montréal with
  the accent. No `skip_prefix` or `skip_between` in this batch.

## Commands (2026-11-08, log times)

| Command | Result |
|---|---|
| `check lit_h34 --corpus lit --dry-run` 12:13:42 (pid 24577) | 0 errors, 0 warnings; slots 152, recorded 150, no_header 2; rows 173 (grade A 173; primary 150, additional 23; printed 139, single 34); papers ok 15; multi-affiliation slots 18; present addresses 0; 13 unmapped org strings |
| `show lit_h34 --corpus lit --codes <id> --pdf`, all 15; yulaev2019 and zhang2016 also `--pages 2` | headers and author lists read (scratchpad only) |
| `probes/probe.py` on scratch copies, dry-run, 12:16:45-12:17:28 (pid 28040) | below; repo batch files md5 unchanged; the dry-run check writes its usual log files under `logs/` |

| probe | change | result | reading |
|---|---|---|---|
| Y1 | yeh2024 K.Q. Wen `slot: 0` | 1 error (D302, matches slot 14) | F1 blocked by the checker |
| Y2 | yeh2024 C.Y. Tsai `slot: 0` | 1 error (D302, matches slot 24) | F1 blocked by the checker |
| Y3 | yeh2024 Y.M. Wang without `slot: 0` | 1 error (0 candidates) | slot setting required |
| Y4 | yeh2024 S.M. Wu `slot: 30` | 0 errors, 1 warning | slot 0 is the D369 call |
| Z1 | zhang2019b block 4 country CN | 0 errors | HK is the contract call |
| Z2 | zhuang2016 block 2 locality Clayton | 2 errors (not in block) | empty locality required |
| Z3 | zhang2014 Junfeng Song without marker 2 | 3 errors | markers bound |
| Z4 | yu2016 block 1 country US | 2 errors (not printed) | empty country required |

## Checker gaps observed (scripts not edited)

- G1 `strict_compatible` (D369 / D382): when the abbreviated and the full form have the same number of initials, the
  initials are not compared, so K.Q. ~ Kai-Shin and C.Y. ~ Chia-Heng pass and `slot: 0` is rejected by D302.

## Verdict

GO. No slot carries a wrong person, org, city, country or marker, nothing is invented, no block is missed, and no
address or contact text is recorded. 2 yeh2024 slots are matched to list names whose second initial disagrees with
the print (same TSMC row either way); they wait on the D412 list correction or the D382 checker change.
