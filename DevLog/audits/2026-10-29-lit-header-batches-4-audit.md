---
title: Fresh-context audit of the lit author-affiliation batch lit_h16 (29 papers)
date: 2026-10-29
auditor: Claude (fresh context; wrote only lit_h16/headers.yaml, the derived files the checker writes, org_requests.csv and the data/_local lists via aggregate, and this record)
scope: data/_staging/people/lit_headers/lit_h16/headers.yaml; both header contracts; DevLog-011 D350-D369, D380, D400-D413; previous audits 2026-10-23-lit-header-batches-audit.md, 2026-10-29-lit-header-batches-2-audit.md, 2026-10-29-lit-header-batches-3-audit.md
verdict: GO for the people rebuild after the fix below (applied; check 0 errors, 1 warning); 0 wrong and 11 imprecise slots in 238 audited (6 fixed, 5 checker gaps); 1 note completed
---

# Lit header batches audit, round 4 (2026-10-29)

## Scope

Batch lit_h16 (29 papers, 238 author-list slots), extracted 2026-10-29 (extractor check: 0 errors, 1 warning).
Restricted corpus: this record names only authors, orgs, units, cities and countries; no paper text is quoted and no
contact, street, building, postal or box code is copied.

## Method

- Every paper read with `env -u VIRTUAL_ENV uv run python scripts/ofc_headers.py show lit_h16 --corpus lit --codes
  <id>`; `--pdf` for chang2026a, sun2022, bauters2011, he2023, ye2019, jin2021, ji2017, koyaz2026, nader2025,
  kittlaus2020a, muthuganesan2023 (overrides, partial papers, present addresses, flagged items). Footnote meanings
  stated in notes but not on page 1 (xiao2022 equal-contribution dagger) read in `references/<id>/text.md` with
  contacts masked on the terminal.
- Selection: all 29 papers (full coverage; supersedes the random sample):
  - (a) explicit `slot:` / `slot: 0` / `author_list_differs`: bauters2011, chang2026a, he2023, jin2021, ye2019;
  - (b) partial: chang2026a, sun2022; present address: nader2025; prose: none in the batch; unreadable: none;
  - (c) flagged items: ding2013, sun2022, deng2024 (list-only extra given names), zhang2025b (D412 artefact), ji2017
    and koyaz2026 ("Current address:"), kittlaus2020a and muthuganesan2023 (parents), muthuganesan2023, ye2019,
    jankowski2020, jin2021, valdez2025 (empty locality / country), tamura2026, bauters2011, jin2021 (campus);
  - (d) the 12 remaining papers: adya2024, lim2026, lu2015, pospischil2013, ribeiro2016, simard2013,
    taballione2019, tossoun2024, xiao2022, xu2026, yang2024, zhang2026a.
- Per slot: slot-to-name assignment (D359, D369, D287, D302), printed marker run vs `markers` + `dropped_markers`,
  block mapping, org / unit / more_orgs split, parent rule, campus (D301), locality (first printed city as printed),
  country (printed), role, basis. Every note claim checked against the page.
- Name scan: all 238 `compare.csv` rows, list name vs printed name (folded); 29 rows differ, every one inspected.
- Claims tested with dry-run probes (`check --dry-run` on a temporarily edited `headers.yaml`, file restored
  byte-identical, md5 asserted after each probe; helper in the session scratchpad).
- Privacy scan: every field and note of `headers.yaml`; every value of `header_rows.csv`, `compare.csv`,
  `unmapped_orgs.csv` and `org_requests.csv` (contact / URL / ORCID patterns, 3+ digit runs other than paper codes,
  street / building / box words and the address words printed in this batch's blocks).
- Backup before any edit: `backup_lit_h16_20261029T234137.zip` (lit_h16 directory + `org_requests.csv`) in the
  session scratchpad `lit_h16_audit/`.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h16 | 29 / 29 | 238 | 227 | 11 | 0 |

- Fixed: 6 imprecise (nader2025 #2 #3 #4 #5 #6 #7, F1). Not fixable within the contract / checker: 5 imprecise
  (chang2026a #1 #3, C1; ji2017 #2 #5, koyaz2026 #2, C2).
- The 7 `no_header` slots: chang2026a #3 (Xiaochuan Xu, only block d, glued marker: C1) and #5 (second "Ting Xu",
  list duplicate), he2023 #1 (C.F. He, D369), jin2021 #8 (Maodong Gao, not printed in the cached arXiv v1 header),
  sun2022 #3 #5 #6 (Song Liang, Yongguang Huang, Ruikang Zhang: two blocks print the same marker 2; correct under
  the never-guess rule).
- Header-only authors (`slot: 0`): chang2026a Yulin Wu (not in the list), he2023 Chengxing He (D369), ye2019 Victor
  Torres-Company (not in the 3-name list): all correct; aggregate extra authors 10 -> 13.

## Rulings on slot overrides and known items

| paper, slot | printed vs list | ruling |
|---|---|---|
| bauters2011 #4 | Jonathon S. Barton vs Jon S. Barton | keep `slot: 4` (D287 short form, initials agree, same position, distinctive family name) |
| chang2026a #4 | Ting Xu printed 5th; list prints Ting Xu at #4 and #5 (Yulin Wu absent, list positions shifted) | `slot: 4` accepted (either duplicate is defensible; order stays monotone); #5 stays `no_header` (open question 3) |
| chang2026a Yulin Wu | printed 3rd, not in the list | `slot: 0` correct; no compatible unmatched slot (D302) |
| he2023 #1 | CHENGXING HE vs C.F. He | `slot: 0` correct (D369: F not explained by the given name, common family name) |
| ye2019 | VICTOR TORRES-COMPANY printed 4th, list has 3 names | `slot: 0` correct |
| jin2021 #8 | Maodong Gao in the list, not printed in the cached arXiv v1 header (11 names) | `author_list_differs` correct; no row |
| ding2013 #2, sun2022 #1, deng2024 #13 | Jing Xu / Jing Ming Xu, XIAO SUN / Xiao Hong Sun, Neha Singh / Neha Chiruvolu Singh | checker matches (list-only extra given name); same list and printed position in each paper: accepted, no fix |
| zhang2025b #6 | DAOXIN DAI vs list artefact "Daoxin Dai A" | correct person; a new D412 case (open question 4) |
| zhang2025b #1 | QIANHAN ZHANG vs Q. Zhang | correct (initial explained) |
| other list-side differences | taballione2019 A. Eckstein, muthuganesan2023 E. Pelucchi / Enrica E. Mura / Paul D. Townsend / Callum G. Littlejohns, ji2017 F. A. S. Barbosa / Alex W. Bryant / Michal F. Lipson / Samantha Pamela Roberts, tossoun2024, valdez2025, yang2024, lim2026, bauters2011 #5 #7 #9, jin2021 #12, deng2024 #21 | all initials agree, same positions: correct |

## Findings and fixes

| # | paper, slots | rating | evidence (locator) | fix (field: before -> after) |
|---|---|---|---|---|
| F1 | nader2025 #2-#7 (Stanton, Brodnik, Jahan, Weight, Williams, Eshaghian Dorche), block 3 | imprecise | p.1 header: Department of Physics, University of Colorado, then a street address (not recorded), then Boulder; the only place printed after the org is Boulder; lit_h06 dostart2020 / gentry2015 and lit_h09 reddy2020 record the same org with `campus: "Boulder"`; probe with the campus: 0 errors | block 3 `campus: "Boulder"` added; note extended. The 6 rows now map to `org_university_of_colorado_boulder` (were unmapped "University of Colorado"); unmapped org strings 19 -> 18 |
| N1 | chang2026a (note) | incomplete note | probe: block b recorded as org Chinese Academy of Sciences + unit Shanghai Institute of Microsystem and Information Technology (printed order) gives 0 errors (+1 row for Chang Chang; Yulin Wu is slot 0); the note said b cannot be verified | note: clause added that b verifies only in that academy-as-org form, unlike the institute-as-org form of lit_h03 / lit_h04 / lit_h10 / lit_h13; block not recorded (open question 1) |
| C1 | chang2026a #1 (Chang Chang; blocks b, c), #3 (Xiaochuan Xu; block d) | imprecise, not fixable | p.1 header: letter markers glued to the first word of every block (text and PDF); probe recording c (University of Chinese Academy of Sciences, Beijing) and d (Harbin Institute of Technology, Shenzhen, first key laboratory as unit): "marker + first field (unit or org) not printed" (md, pdf) | none (gap G1); blocks a and e verify because their unit is found first and the org is matched directly before it |
| C2 | ji2017 #2 #5 (Barbosa, Cardenas), koyaz2026 #2 (Yakar) | imprecise, known | p.1 header: present-address blocks printed with the cue Current address (Universidade Estadual de Campinas, Campinas, BR; University of Rochester, Rochester, US; DESY, Hamburg, DE); probe ji2017 block 3 as `present_address`: "marker + first field not printed" (md, pdf) | none (gap of round 2, beeck2021 precedent); markers kept in `dropped_markers`, primary rows intact |

Checked and correct (highlights):
- Partial papers: sun2022 prints marker 2 on two blocks (Jilin University, College of Physics, Changchun;
  Institute of Semiconductors, Chinese Academy of Sciences, Beijing) in both layers; authors 3 / 5 / 6 unreadable,
  neither block recorded: correct (never guess). chang2026a `partial` with author 4 unreadable: correct.
- Present addresses: nader2025 blocks 4 / 5 (Currently with: EMode Photonix, Boulder; Nexus Photonics, Goleta)
  `role: present_address`, carried by Stanton and Eshaghian Dorche.
- Parents not copied: kittlaus2020a Jet Propulsion Laboratory (California Institute of Technology printed after it);
  muthuganesan2023 Tyndall National Institute (University College Cork after it): both follow the contract parent
  rule and the Tyndall precedents (zhang2023d F2 of round 2, loi2019).
- Empty fields: muthuganesan2023 block 2 and ye2019 print a postal code and no city (`locality: ""`); jankowski2020
  block 5, jin2021 block 3, valdez2025 blocks 1 / 2 print no country (`country: ""`).
- Campus: bauters2011 and tamura2026 (comma, then the place), jin2021 (University of California Santa Barbara,
  no comma): `campus` correct. yang2024 University of Wisconsin – Madison (dash-joined name) kept in `org` as
  printed (open question 5).
- As printed: ding2013 Kgs. Lyngby; sun2022 Xian; xu2026 Atsugi-shi / Narashino-shi / Koriyama-shi (district names
  before the city in block 4 only in the note, by type); jankowski2020 Kowloon with HK; simard2013 Québec;
  taballione2019 Lionix International BV vs bauters2011 LioniX BV (both as printed); deng2024 imec.
- Markers: every author's printed run matches `markers` + `dropped_markers` (all 29 papers); symbol marks
  (asterisk, dagger) never used by a block; xiao2022 dagger = equal contribution (printed on a later page).
- Unit chains: chang2026a block e, ding2013 block 2 (national laboratory and school before HUST, as most
  precedents), zhang2026a block 2 (four units joined by ampersands), zhang2025b, simard2013, tamura2026 block 1.

Consistency observation (no fix, other batch): lit_h07 ledezma2022 prints the same Jet Propulsion Laboratory,
California Institute of Technology, Pasadena block and records Caltech as `more_orgs`; kittlaus2020a (this batch)
drops the parent per the contract (open question 2). The aggregate now holds one JPL request with both papers.

## Privacy and as-printed scan

- No contact address, URL, ORCID id, phone number, street name, building name, postal code or box code in any field
  or note of `headers.yaml`, nor in `header_rows.csv` (4680 values), `compare.csv` (2390), `unmapped_orgs.csv` (95)
  or `org_requests.csv` (2128): 3+ digit runs occur only in paper codes and decision numbers. Notes name address
  parts only by type (street address, postal box, postal code, building name, district names, province /
  prefecture). No `skip_prefix` / `skip_between` span in the batch.
- This record: same scan (see Commands).

## Commands (2026-10-29, log times)

| Command | Result |
|---|---|
| `check lit_h16 --corpus lit --dry-run` (before) 23:41:40 (log `lit_headers_check_lit_h16_27588_20261029T234140.log`) | 0 errors, 1 warning (bauters2011 slot 4); slots 238, recorded 231, no_header 7, rows 259, present addresses 2, 19 unmapped org strings |
| probes (`--dry-run`) 23:42:57 (28308), 23:46:51 (31320), 23:46:58 (31381), 23:47:13 (31463) | chang2026a block b as academy + institute unit: 0 errors; chang2026a blocks c / d: 4 errors; ji2017 Current address as present_address: 2 errors; nader2025 campus Boulder: 0 errors, unmapped 18. File restored and md5-verified after each |
| `check lit_h16 --corpus lit` 23:48:25 (log `lit_headers_check_lit_h16_32173_20261029T234825.log`) | 0 errors, 1 warning; ok 27, partial 2, unreadable 0; rows 259 (grade A 259), recorded 231, no_header 7, present addresses 2; 18 unmapped org strings; stamp matches headers.yaml (sha256 23a0a179...) |
| `aggregate --corpus lit` 23:48:38 (log `lit_headers_aggregate_32314_20261029T234838.log`) | 265 org-request strings (was 252: +13 new strings from lit_h16, 5 existing strings gain lit_h16 locators), 0 conflicts, 13 header-only authors (was 10) |

Changes to `headers.yaml` (diff against the backup): nader2025 block 3 `campus` and note, chang2026a note; nothing
else. `header_rows.csv` changes only in the 6 nader2025 rows of block 3.

## Checker gaps observed (scripts not edited)

- G1 A letter marker glued to the first word of a block ("aOrg", SPIE style) fails the word-start test of the first
  field; a block verifies only when its unit is printed after the org (the org is then matched as a prefix). D366
  (4) splits a glued letter only before a present-address cue. chang2026a loses blocks b, c, d (2 slots affected).
- Known: "Current address:" cue (ji2017, koyaz2026; beeck2021 of round 2).

## Open questions

1. chang2026a block b: record as org Chinese Academy of Sciences + unit Shanghai Institute of Microsystem and
   Information Technology (verifies now, maps to the academy), or wait for G1 and record the institute as org?
2. Jet Propulsion Laboratory with Caltech printed after it: lit_h07 ledezma2022 keeps Caltech in `more_orgs`,
   kittlaus2020a drops it (contract parent rule); normalize ledezma2022?
3. chang2026a author list: "Ting Xu" twice (#4, #5), Yulin Wu missing; add to the D412 author-list correction file
   (drop the duplicate, insert Yulin Wu) and confirm slot 4 for Ting Xu.
4. zhang2025b #6 "Daoxin Dai A": add to the D412 list (with wang2014, bauters2013).
5. yang2024 University of Wisconsin – Madison: keep the dash-joined name in `org` (as printed) or split into org +
   `campus: "Madison"` like the comma forms?
