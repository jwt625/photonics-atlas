---
title: Fresh-context audit of the lit author-affiliation batch lit_h19 (35 papers)
date: 2026-11-02
auditor: Claude (fresh context; wrote only lit_h19/headers.yaml, the derived files the checker writes, and this record; aggregate not run)
scope: data/_staging/people/lit_headers/lit_h19/headers.yaml; both header contracts; DevLog-011 D350-D369, D380, D400-D426; previous audit 2026-10-30-lit-header-batch-h17-audit.md
verdict: GO for the people rebuild (check 0 errors, 2 warnings); 0 wrong and 7 imprecise slots in 298 audited (0 fixable, all 7 checker gaps G1 / G2); 1 note made by-type
---

# Lit header batch audit: lit_h19 (2026-11-02)

## Scope

Batch lit_h19 (35 papers, 298 author-list slots), extracted 2026-11-02 (extractor check: 0 errors, 2 warnings; 35 ok;
298 / 298 slots recorded; 366 rows, all grade A; 21 unmapped org strings). Restricted corpus: this record names only
authors, orgs, units, cities and countries; no paper text is quoted and no contact, street, building, postal or box
code is copied.

## Method

- Every paper read with `env -u VIRTUAL_ENV uv run python scripts/ofc_headers.py show lit_h19 --corpus lit --codes <id>
  --pdf`, through a viewer that keeps the header, the footnote statements and every affiliation-like line (helper
  `view.py` in the session scratchpad `lit_h19_audit/`; terminal only, nothing stored). `--pages 1 11` for blaicher2020,
  `--pages 1 2` for hiraki2017.
- Selection: all 35 papers (full coverage):
  - (a) explicit `slot: 0` / `author_list_differs` / order differs: bian2025, giewont2019, he2021;
  - (b) prose: ahmadi2022, alasio2024, anelli2024, barazani2023, beckerwerth2021, chen2022b, cheung2019, fatemi2019,
    giewont2019, guo2024, guzman2019, hiratani2024, izumisawa2026, jia2025; per_author: he2021; present addresses:
    asch2025, barazani2023;
  - (c) flagged items: chen2024b (recorded marker cut by the checker window), iseghem2022 (department after the
    university), blaicher2020 (blocks on page 11), hiraki2017 (cover page), guo2024 (key laboratory without a host),
    giewont2019 (org typo), he2025 (parent), empty localities (hiraki2017, iseghem2022, izumisawa2026) and empty
    countries (asch2025 block 3, chen2024b);
  - (d) the remaining papers: afzal2020, asano2017, brusberg2025, cheben2015, chen2022, chen2024, cheng2022,
    cherchi2013, du2022, grottke2020, hamaguchi2018, huh2016, kasztelanic2018.
- Per slot: slot-to-name assignment (D359, D369, D287, D302), printed marker run vs `markers` + `dropped_markers` (text
  and PDF view), block mapping, org / unit / more_orgs split, parent rule, campus (D301), locality (first printed city
  as printed), country (printed), role, basis, locator. Every note claim checked against the page.
- Name scan: all 298 `compare.csv` rows, list name vs printed name (folded); 24 rows differ, every one inspected.
- Org mapping: every printed org string vs its `org_ids` in `header_rows.csv` (68 strings), read; the CNR mapping checked
  against the registry record (read only).
- Missed blocks and present addresses: all pages of every paper searched through `show --pages` for author-detail and
  present-address cues.
- Claims tested with dry-run probes (`check --dry-run` on a temporarily edited `headers.yaml`, file restored
  byte-identical, md5 asserted after each probe; helper `probe.py`, same folder).
- Privacy scan (`privscan.py`, same folder): see below.
- Backup before any edit: `backup_lit_h19_20261102T223443.zip`, same folder.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h19 | 35 / 35 | 298 | 291 | 7 | 0 |

- Fixed: 0 slots. Not fixable within the contract / checker: 7 imprecise (chen2024b #6; iseghem2022 #1 #2 #5 #9 #10
  #11; C1, C2).
- `no_header` slots: 0.
- Header-only authors (`slot: 0`): 7, all bian2025 (Bob Mulfinger, Ryan Sporer, Vikas Gupta, Ken Giewont, Rick Carter,
  Kevin Soukup, Ted Letavic): printed in the header, the author list stops at 30 names; correct, no rows (open
  question 1).

## Rulings on slot overrides and known items

| paper, slot | printed vs list | ruling |
|---|---|---|
| bian2025 printed 31-37 | 7 names vs nothing | `slot: 0` + `author_list_differs` correct; none is compatible with a list name |
| jia2025 #3 | Xiao Xu vs list Xiao Xue Xu | auto-match with a dropped syllable, common family name; same position, same statement; probe `slot: 0` gives the D302 error; accepted, flagged (open question 3) |
| giewont2019, he2021 | printed order differs from the list | warnings correct; slots resolve by name, no overrides |
| guzman2019 #1 #6 | Robinson C. Guzmán Martínez, Guillermo Carpintero del Barrio vs list Robinson Guzmán, Guillermo Carpintero | the list drops family-name parts; initials agree, same positions: correct |
| huh2016 #5 | SUNME KIM vs list Sun-Me Kim | same name: correct |
| other list-side differences | alasio2024 #7; beckerwerth2021 #5; blaicher2020 #3 #4 #7 #11 #12 #15 #18 #19; cheben2015 #7 #9; chen2022b #4; chen2024b #6; cherchi2013 #3 #5; giewont2019 #5 #8 #16; kasztelanic2018 #10 | initials or middle names only, all agree, same positions: correct |

## Findings and fixes

| # | paper, slots | rating | evidence (locator) | fix (field: before -> after) |
|---|---|---|---|---|
| N1 | hiratani2024 (note) | privacy rule | the note named two wards and a prefecture printed around the city (h17 audit N1 practice: address parts by type only) | names -> "a ward", "a prefecture"; no field changed; rows unchanged |
| C1 | chen2024b #6 (Z. Rena Huang), block ‡ | imprecise, not fixable | p.1 header: the last author carries a star and both symbol markers; only † recorded; probe markers † + ‡: "printed markers differ" (md, pdf). Extractor's cause confirmed in the code: the last author's run is read from a 12-character window, and the two normalized symbol tokens need at least 13 | none (gap G1); same org, the second department only is missing; the note says so |
| C2 | iseghem2022 #1 #2 #5 #9 #10 #11, blocks 1, 3, 4 | imprecise, not fixable (second sub-unit lost) | p.1 header: group, then university, then a department, then the country; group recorded as `unit`, department not; probe unit = group + department: "marker + first field not printed" (md, pdf) | none (gap G2; family of the "unit printed after org campus" gap); the note says so; the more specific unit is the one kept |

Checked and correct (highlights):
- Prose: alasio2024 P1-P4 (clause P3 for the CNR institute; the printed host of the institute is not a third org; Turin in
  P2 and Torino in P3, both as printed); barazani2023 P1-P4 ("was with"
  P1, pronoun present address P2 AEPONYX Inc); guo2024 P1-P9 (three statements with clauses; P7 Georgia
  Tech-Shenzhen Institute as unit of Tianjin University with locality Shenzhen; `campus` not set: the unit carries the
  site and the row maps to `org_tianjin_university`);
  guzman2019 P1 / P2; hiratani2024 P1-P7 (three statements; carriers both ways; Dept. and Department forms as printed);
  giewont2019 P1-P4 (subjects vs carriers both ways); anelli2024, ahmadi2022, beckerwerth2021, chen2022b, cheung2019,
  fatemi2019, izumisawa2026, jia2025 ("the authors" or plain subjects).
- Per author: he2021 G1-G7 (imec, Leuven under each name; reading order kept in the YAML).
- Present addresses: asch2025 block 3 (cue printed, Huawei Technologies, no place: `locality` and `country` empty, on
  He only); barazani2023 P2. No other cue on any page of the batch except biographies at the end of ahmadi2022 and
  hiratani2024 (not header statements). blaicher2020 p.11 prints a competing-interests statement naming employers: not
  an affiliation block, not recorded.
- Later page: blaicher2020 blocks 3-6 `p.11 affiliations`, blocks 1 / 2 `p.1 footnote`, both consistent; markers 3-6 on
  the author line read in both layers. Cover page: hiraki2017 `p.2 header`.
- Empty fields: hiraki2017 and izumisawa2026 print a prefecture only (`locality: ""`); iseghem2022 blocks 1-5 print no
  city (Lausanne only inside the EPFL name: not the place); chen2024b prints a city and a state, no country
  (`country: ""`).
- Parents not copied: he2025 ISCE2 (A*STAR after it, Singapore place kept).
- Two-org blocks: asch2025 block 1 imec + Ghent University (`more_orgs`, unit CMST); iseghem2022 block 1 dash-joined form
  kept as printed (D416 (5)), maps to `org_ghent_university;org_imec`.
- Key laboratory: guo2024 P2 / P6 print no host university, recorded as org with its ministry as printed; the two
  printed casings are two strings (open question 2); no host inferred.
- Markers: every readable author's printed run matches `markers` + `dropped_markers` in both layers; contact footnotes
  chen2024 5 and 6 (both masked lines follow block 4); symbol marks: equal contribution bian2025 and chen2022 (no block
  uses them), corresponding author elsewhere.
- As printed: giewont2019 P4 GLOBALFOUINDRIES (typo in the source; P1 / P2 spelled correctly; open question 2); he2025
  School of Future Tech; asch2025 Gent and Imec; alasio2024 Turin and Torino; du2022 unit chain joined by ampersands;
  blaicher2020 KIT in full and as abbreviation.
- Org mapping: all 47 mapped strings read and correct, including Consiglio Nazionale delle Ricerche to the Italian
  `org_national_research_council` (registry country IT), National Research Council Canada to its own id, Innolight
  Technology Research Institute (ITRI) to the Innolight id (not the Taiwan ITRI), Wuhan National Laboratory for
  Optoelectronics to Huazhong University of Science and Technology (existing alias). 21 unmapped (`unmapped_orgs.csv`), none wrongly
  forced.

## Privacy and as-printed scan

- No contact address, URL, ORCID id, phone number, street name, building name, postal code or box code in any field or
  note of `headers.yaml` after N1, nor in `header_rows.csv` (366 rows), `compare.csv` (298), `unmapped_orgs.csv` (21) or
  `papers.csv`: scanned for contact / URL / ORCID patterns, 3+ digit runs, street / building / box / park words and the
  address words printed in this batch's blocks. Hits: only this batch's dates and counts, the DevLog / decision numbers,
  and the generic file-header comment. Notes name address parts only by type (district, ward, prefecture, state). No
  `skip_prefix` / `skip_between` span in the batch.
- This record: same scan, same result.

## Commands (2026-11-02, log times)

| Command | Result |
|---|---|
| `check lit_h19 --corpus lit` (before) 22:34:32 (pid 66238) | 0 errors, 2 warnings (giewont2019, he2021 order); slots 298, recorded 298, rows 366 (grade A 366), present addresses 2, 21 unmapped org strings |
| probes (`--dry-run`) 22:39:45 (68358), 22:40:38 (68607), 22:40:45 (68661) | chen2024b Huang both markers: 2 errors; iseghem2022 block 1 unit + department: 2 errors; jia2025 `slot: 0`: 2 errors (D302). File restored and md5-verified after each |
| `check lit_h19 --corpus lit` 22:41:25 (log `lit_headers_check_lit_h19_68820_20261102T224125.log`) | 0 errors, 2 warnings; ok 35, partial 0, unreadable 0; rows 366 (grade A 366), recorded 298, no_header 0, present addresses 2; 21 unmapped org strings; stamp matches headers.yaml (sha256 375ebddb...) |

Changes to `headers.yaml` (diff against the backup): hiratani2024 note; nothing else. Derived rows unchanged in content.
`aggregate` not run (coordinator).

## Checker gaps observed (scripts not edited)

- G1 The last author's marker run is read from a fixed 12-character normalized window: two symbol markers ("dagger" +
  "ddagger") do not fit, so the second cannot be recorded (chen2024b #6).
- G2 A department printed after the org, when a group is printed before it (group, org, department), has no field: only
  one contiguous unit + org segment is checked (iseghem2022 blocks 1, 3, 4).

## Open questions

1. bian2025: the author list stops at 30 of 37 printed names: add the 7 names to the D412 author-list correction file so
   they get slots? Recommended: yes; no rows until then.
2. Org round aliases: giewont2019 GLOBALFOUINDRIES to `org_globalfoundries`; guo2024 key laboratory, two casings, one
   id. Recommended: yes; keep the printed strings.
3. jia2025 #3 (Xiao Xu / Xiao Xue Xu) auto-match with a dropped syllable: accept and add to the D426 review list with
   fang2010 and feng2011? Recommended: accept.
4. Re-record after checker fixes: chen2024b #6 (G1), iseghem2022 blocks 1, 3, 4 (G2)? Recommended: yes; neither blocks
   the rebuild (same org ids in both).
5. A lit_h08 note still names one of these wards (seen by file search, not edited): make them by-type in the
   follow-up pass, with the lit_h01 / lit_h10 campus names of the h17 audit? Recommended: yes.
