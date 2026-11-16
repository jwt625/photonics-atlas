---
title: Fresh-context audit of the lit author-affiliation batch lit_h44 (24 papers)
date: 2026-11-15
mode: read-only on the batch (wrote only this record and scratchpad renders / probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only with --dry-run, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h44/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D412, D426, D442, D466, D546, D557, D572); format from the 2026-11-15 h43 audit; read-only comparison with earlier batches (lit_h05 / h16 / h17 Current address, lit_h17 foster2006, lit_h25 per_author grid, Zijingang / Colorado / EPFL centre / C2N / PolyU records)
verdict: GO with 2 fixes; 177 list slots + 1 header-only author audited; 174 recorded slots ok (2 with an imprecise header position, morgan2021), 3 correctly without rows, 0 wrong; F1 privacy note edit (li2022a building name), F2 morgan2021 author order + note; optional N1-N2; extractor calls (kim2021a partial, liu2020b Current address, li2022a slot 0) verified and forced by the checker; one ruling question (li2013 #2)
---

# Lit header batch audit: lit_h44 (2026-11-15)

## Scope

Batch lit_h44: 24 papers (preprints 10, IEEE journals 7 (PTL x3, JLT x2, Photonics Journal x2), Optics Express /
OSA 6, one IEEE conference paper); 177 list slots plus 1 header-only author (li2022a Strain, slot 0); 216 rows.
Restricted corpus: this record names only authors, orgs, units, cities and countries; no paper text is quoted and no
contact, street, building, postal-box or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h44 --corpus lit --codes <id> --pdf`
  (all 24; lin2021a also with `--pages 2`; output kept in the scratchpad only).
- Page renders (pymupdf, 110 dpi, scratchpad `h44/*.png`): morgan2021 header grid, kim2021a header, li2013 and
  kaspar2015 page 1.
- Per slot: printed name vs `compare.csv` and the `show` author list; marker run vs text and PDF layer (identical in
  both layers for every printed-marker paper); block fields (org, unit chain, more_orgs, campus, city, country); role;
  locator; grade. Every distinct (paper, org, city, country, org id, match basis, role, basis, locator) tuple of
  `header_rows.csv` read (64 tuples, 216 rows).
- Prose papers (kaspar2015, kita2021, li2013, liu2020c, lu2024a, morton2021): every statement subject, verb, clause
  and field read against the footnote.
- Symbol legends: checked on page 1 (lihachev2024, krasnokutska2019, lin2022a, jung2021, hu2025a, harris2017) or in
  `text.md` (liu2020b equal-contribution legend on a later page).
- Probes on scratch copies (`h44/probes/probe.py` in the session scratchpad, scratch `LIT_BASE`, batch name
  `lit_p44`, `cmd_check(..., dry_run=True)`). md5 of every repo batch file identical before and after the audit;
  `check_stamp.txt` matches `headers.yaml` (sha256 35b6a707...).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h44 | 24 / 24 | 177 + 1 header-only | 176 | 2 | 0 |

- Rows 216 (all grade A: printed 145, prose 50, single 15, per_author 6; primary 177, additional 38, present address
  1); recorded 174, no_header 3 (kim2021a #1 #2 #4); papers ok 23, partial 1, unreadable 0; `author_list_differs` 1
  (li2022a); explicit slots 4 (kaspar2015 #13, li2013 #1 and #2, morgan2021 #3) plus slot 0 (li2022a Strain);
  `order_differs` 2 (harris2017, morgan2021); multi-affiliation slots 32; 18 unmapped org strings.
- Per paper (slots / rows): harris2017 12 / 12; hu2025a 7 / 14; jung2021 6 / 11; kaspar2015 18 / 18; kim2014 5 / 5;
  kim2021a 4 / 1; kita2021 2 / 2; krasnokutska2019 3 / 3; li2013 7 / 8; li2018a 10 / 13; li2022a 6 (+1 slot 0) / 7;
  lihachev2024 13 / 25; lin2021a 4 / 8; lin2022a 11 / 13; liu2018b 9 / 9; liu2020b 10 / 11; liu2020c 4 / 8;
  liu2023a 4 / 5; lu2024a 5 / 5; ma2023 12 / 13; martinez2016 8 / 8; morgan2021 6 / 6; morton2021 9 / 9;
  naghdi2016 2 / 2.

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (177 + 1) | 178 | 0 | 0 |
| markers (178; 3 unreadable carry []) | 178 | 0 | 0 |
| header position (178) | 176 | 2 (morgan2021 Knecht, Kharas: F2) | 0 |
| blocks (org / unit / campus / locality / country) (174 with rows + Strain) | 175 | 0 | 0 |
| prose blocks (19 blocks, 6 papers) | 19 | 0 | 0 |
| present addresses (1 block) | 1 | 0 | 0 |
| locators (all blocks) | all | 0 | 0 |
| notes (24) | 22 | 1 privacy (li2022a, F1), 1 order claim (morgan2021, F2) | 0 |

## Per-paper findings

- harris2017 (12; printed, closing-parenthesis markers): runs 1 / 1 / 1 / 2 / 1 / 3 / 1 / 1 / 4 / 4 / 5 / 1,6 as
  printed (star symbol on Harris ignored). MIT EECS, Physics, Mechanical Engineering, Cambridge, US; Harvard
  University + school unit (printed before the org), Cambridge, US; Elenion Technologies, New York, US. Marker 6 is the
  corresponding-author line (dropped, correct). Printed order differs from the list (Mower / Prabhu): warning,
  expected. ok.
- hu2025a (7; printed): Zhejiang University with the four-part chain, Hangzhou; Jiaxing chain, Jiaxing; Ningbo
  Research Institute, Ningbo; all CN. Campus name after the org not recorded (lit_h01 / h10 / h33 precedent). #7
  Daoxin Dai A list artefact (D412). ok.
- jung2021 (6; printed): NIST + Time and Frequency Division, Boulder; University of Colorado + campus Boulder +
  Department of Physics, Boulder (as the 10 earlier records; campus mail code between org and city not recorded);
  block 3 present address (cue printed) KIST + Center for Quantum Information, Seoul, KR (South Korea printed). Jung
  1,2,3. ok.
- kaspar2015 (18; prose): P1 III–V Laboratory, Palaiseau, FR (6 authors); P2 Bell Laboratories + WDM Dynamic
  Networks Department, Nozay, FR, with the site name between verb and department in `skip_prefix` (probe P1: required,
  D366); P3 Tyndall National Institute, Cork, IE (parent not copied, corpus form); P4 CEA–Leti, Grenoble, FR.
  Statement membership exact (probe M4). #13 Peter O'Brien vs list Peter A. O'Brien: explicit slot required (probe S3)
  and D369-conform (distinctive family name, missing middle initial). Dalila Make / D. Maké automatic. ok.
- kim2014 (5; single): org printed as National Institute of Advanced Science and Technology (as printed) + Network
  Photonics Research Center, Tsukuba, JP; prefecture not recorded. ok.
- kim2021a (4; printed, partial): render read. Block 1 prints only the department; the org and place are printed once
  after block 2. Block 2 University of Illinois at Urbana–Champaign + ECE, Urbana, US (Peterson). Authors 1, 2, 4
  unreadable (see call 1). ok.
- kita2021 (2; prose): Waseda University + Department of Applied Physics, locality Koganei (first printed city in
  both layers; probe L1 shows the checker would also take Tokyo, G2); NICT (parenthesized acronym kept), Koganei; both
  JP. ok.
- krasnokutska2019 (3; printed single block with marker 1): RMIT University + laboratory / centre / school chain,
  Melbourne, AU (state not recorded). Asterisk = equal contribution, dagger = contact (legend on page 1). ok.
- li2013 (7; prose): P1 University of Minnesota + ECE, Minneapolis; P2 University of Delaware + ECE, Newark (Liu,
  Galland, Baehr-Jones); P3 Institute of Microelectronics, Singapore, SG (A*STAR parent not copied; maps to
  `org_astar_ime` by ROR); Hochberg P4 Delaware + clause P5 NUS + ECE, Singapore, SG (probe M3: clause bound). #1 Li He
  vs list He Li: automatic (probe S2), explicit slot harmless. #2 Yang Liu vs list Liu Shuan Yang: explicit slot
  required (probe S1); see call 4. ok.
- li2018a (10; printed, capitals): HUST + WNLO & school chain, Wuhan; Xiamen University + institute and department,
  Xiamen; C2N as its own org with CNRS, Univ. Paris-Sud, Université Paris-Saclay in `more_orgs`, Orsay, FR (D466,
  same form as the earlier C2N records); South-Central University for Nationalities + Hubei key laboratory / college,
  Wuhan; CN otherwise. Markers 5, 6 contact lines (dropped; probe M2: bound). ok.
- li2022a (6 + 1; printed, capitals): Fraunhofer Centre for Applied Photonics, Glasgow, GB; University of Strathclyde
  + Institute of Photonics, Dept. of Physics, Glasgow, GB (UK printed). The list has 6 names and omits Michael J.
  Strain: `slot: 0` + `author_list_differs` (probe S5: required). Markers 3, 4 contact lines. Mark Scullion vs list
  Mark G. Scullion automatic. Note names a building (F1). ok.
- lihachev2024 (13; printed): EPFL long name + Institute of Physics; EPFL + Center of Quantum Science and Engineering
  (same form as 2 earlier records); Deeplight SA; all Lausanne, CH; Purdue University + OxideMEMS Lab, West Lafayette,
  US. Runs exact (Bancora and Voloshin 1,2,3). Symbol legends on page 1 (equal contribution, contact). ok.
- lin2021a (4; printed, cover page): page 2 header read in both layers. Zhejiang University + two-part chain,
  Hangzhou; Ningbo Research Institute, Ningbo; South China Normal University + centre / academy chain, Guangzhou; all
  CN; `p.2 header` on every block. ok.
- lin2022a (11; printed): Max Planck Institute of Microstructure Physics, Halle, DE; University of Toronto + ECE,
  Toronto, CA; Advanced Micro Foundry Pte Ltd, Singapore, SG (`org_amf`). Patrick Guo Qiang Lo vs list Patrick Lo
  automatic. ok.
- liu2018b (9; printed): Yale University + Department of Electrical Engineering, New Haven, US; Institute of
  Semiconductors, Chinese Academy of Sciences + R & D Center for Semiconductor Lighting, Beijing, CN. ok.
- liu2020b (10; printed): EPFL long name + Institute of Physics, Lausanne, CH; The Hong Kong Polytechnic University
  + Department of Electrical Engineering, Hong Kong, HK (4 earlier PolyU records identical). Block 3 (Guo) printed with
  the Current address cue: not recorded, marker under `dropped_markers` (see call 2). ok.
- liu2020c (4; prose, "The authors"): P1 Zhejiang University + four-part chain (leading article inside the chain kept
  as printed), Hangzhou; clause P2 Ningbo Research Institute, Ningbo; both CN. #4 Daoxin Dai A (D412). ok.
- liu2023a (4; printed, capitals): SIMIT, Chinese Academy of Sciences + state key laboratory, Shanghai; University
  of Chinese Academy of Sciences, Beijing; both CN. ok.
- lu2024a (5; prose): P1 Tsinghua University + Department of Electronic Engineering (printed without a comma),
  Beijing; P2 China Mobile Research Institute, Beijing; both CN. ok.
- ma2023 (12; printed, capitals): NUDT + institute & state key laboratory / college chain, and NUDT + Center of
  Material Science, both Changsha, CN (province not recorded). Markers 3, 4, 5 contact lines. #7 YANG YU vs list Yang
  Woo Yu automatic (dropped middle name; possible list artefact, see question 3). ok.
- martinez2016 (8; single, capitals): Sandia National Laboratories, Albuquerque, US. ok.
- morgan2021 (6; per_author): blocks exact (MIT + Department of Aeronautics and Astronautics, Cambridge, country ""
  (only the state printed, correct); MIT Lincoln Laboratory, Lexington, US). #3 Jeffrey Knecht vs list J.M. Knecht:
  explicit slot required (probe S4), D369-conform. Render read: the six blocks form a two-column grid; read row by
  row the order is Morgan, Kharas, Knecht, Juodawlkis, Cahoy, Sorace-Agaskar, which equals the author list. The YAML
  follows the text-layer order (Knecht before Kharas) and the note says the printed order differs from the list
  (F2). Slots and rows are unaffected; header position imprecise for 2 authors.
- morton2021 (9; prose): P1 Morton Photonics Inc., West Friendship; P2 University of California + campus Santa
  Barbara, Santa Barbara (`org_ucsb`); P3 Johns Hopkins University, Baltimore (leading article not copied, corpus
  practice); P4 Nexus Photonics, Santa Barbara; all US. ok.
- naghdi2016 (2; single, capitals): McGill University + ECE, Montreal, CA. ok.

## Extractor calls (verified)

1. kim2021a partial (block 1 unrecorded, authors 1, 2, 4 unreadable). Probe K1 (block 1 with org University of
   Illinois at Urbana–Champaign + department unit): 4 errors (unit and org not contiguous; block 2 then not found),
   in both layers. Probe K2 (department as `org`, no place) passes, but records a department as an organization with
   no country: not a valid form. Forced; same gap as lit_h17 foster2006 (h17 audit G3, shared org suffix). Keep;
   add kim2021a block 1 to the G3 re-record list (values: Department of Mechanical Science and Engineering, University
   of Illinois at Urbana–Champaign, Urbana, US).
2. liu2020b Current address (block 3 dropped). Probe G1 (block 3 as `present_address`, Guo 1,3): 2 errors (marker +
   first field not found, the cue is not accepted). Forced; same form as lit_h05, h16 (two papers), h17, h27. Keep;
   re-record list for the Current address cue gap (values in the paper note, no postal code).
3. li2022a Strain `slot: 0`. The `show` list has 6 names; Strain is printed 7th with markers 2,4. Probe S5: required.
   Correct; Strain goes to the local extra-authors list via `aggregate`.
4. Explicit slots. Required: kaspar2015 #13 (S3), li2013 #2 (S1), morgan2021 #3 (S4). Redundant, harmless: li2013 #1
   (S2). li2013 #2 is a judgment call: the list form Liu Shuan Yang contains both printed name parts in swapped order
   plus an extra part; no reading makes the first initials agree (Y. Liu vs L. S. Yang / S. Y. Liu), but D369 governs
   abbreviated forms and D287 allows swapped order (Koh Sing Chee, Lončar Marko) and extra name parts (Rosdi Hassan).
   Same position, same Delaware statement. Probe S6 shows `slot: 0` + `author_list_differs` also passes. Recommend:
   keep slot 2 and put the list form on the D412 correction file (question 1).

## Fixes (exact YAML edits)

F1 (privacy, note only). In `lit:li2022a` the note names the building printed in blocks 1 and 2. Replace the clause
from `blocks 1 and 2 print the building` up to and including `(not recorded)` with

```yaml
blocks 1 and 2 print a building name (not recorded)
```

so the note reads `...markers 3 and 4 point to contact lines; blocks 1 and 2 print a building name (not recorded);
street addresses and postal codes not recorded`. Rows unchanged.

F2 (header position + note). In `lit:morgan2021` swap the two author lines so that the authors follow the printed
reading order of the grid:

```yaml
    - {name: "Dave Kharas", markers: ["G3"]}
    - {name: "Jeffrey Knecht", markers: ["G2"], slot: 3}
```

(replacing the pair `Jeffrey Knecht ... slot: 3}` / `Dave Kharas ...}`; blocks G1-G6 stay in text-layer order, lit_h25
precedent), and in the note replace

```yaml
explicit slot 3; printed order differs from the author list"
```

with

```yaml
explicit slot 3; the blocks form a two-column grid read row by row (authors listed in that printed reading order, which equals the author list); the text layer reads Knecht before Kharas (blocks numbered in text-layer order, lit_h25 precedent)"
```

Rows unchanged in content (216); header_pos of slots 2 and 3 swap; the `order_differs` warning for morgan2021 goes.

N1 (optional, note). In `lit:kim2021a` replace `(shared org suffix, checker gap G3, as foster2006)` with
`(shared org suffix, lit_h17 audit gap G3, as lit_h17 foster2006)` (the bare label G3 collides with the h43 audit G3).

N2 (optional, note). In `lit:li2013` replace `the author list prints Liu Shuan Yang;` with
`the author list prints Liu Shuan Yang (swapped order plus an extra name part, both printed name parts present; slot set, D287; list form for the D412 correction file);`

Probe FIX_all (F1 + F2 + N1 + N2 on a scratch copy): 0 errors, 4 warnings (3 explicit slots; harris2017 order
differs).

## Open questions (with recommendation)

1. li2013 #2 (call 4): keep `slot: 2`, add the list form Liu Shuan Yang to the D412 correction file. Alternative
   `slot: 0` + `author_list_differs` passes (probe S6) but would leave list slot 2 without a header. Recommended:
   keep.
2. kim2021a block 1 to the h17 G3 (shared org suffix) re-record list; liu2020b block 3 to the Current address
   re-record list. Recommended: yes.
3. D412 / D426 lists: hu2025a #7 and liu2020c #4 (Daoxin Dai A), li2013 #1 (name-order swap, D426 review), ma2023 #7
   (list Yang Woo Yu, printed YANG YU; matched automatically by dropped middle name; the extra Woo looks like a list
   artefact). Recommended: add.
4. G1 test list (last author's dropped marker not bound): harris2017 #12 Englund passes without dropped marker 6
   (probe M1); li2018a Gao (not last) is bound (M2). Recommended: add harris2017 #12 to the D442 / D546 / D557 list.

## Unmapped org names (org round, no YAML change)

| printed org (unit) | place | proposal |
|---|---|---|
| Bell Laboratories (WDM Dynamic Networks Department) | Nozay, FR | alias to `org_nokia_bell_labs` (France site; registry has Nokia Bell Labs France as a printed alias) |
| CEA–Leti | Grenoble, FR | alias (en dash form) to `org_cea_leti` |
| Deeplight SA | Lausanne, CH | new org |
| Fraunhofer Centre for Applied Photonics | Glasgow, GB | new org |
| III–V Laboratory | Palaiseau, FR | alias to `org_iii_v_lab` |
| Morton Photonics Inc. | West Friendship, US | new org |
| National Institute of Advanced Science and Technology (printed without Industrial) | Tsukuba, JP | alias to `org_national_institute_of_advanced_industrial_science_and_technology`, flagged as a printed misnomer |
| National University of Defense Technology (2 units) | Changsha, CN | new org (also unmapped in lit_h43) |
| RMIT University | Melbourne, AU | new org (also unmapped in lit_h43) |
| Shanghai Institute of Microsystem and Information Technology, Chinese Academy of Sciences | Shanghai, CN | new org or alias |
| South-Central University for Nationalities | Wuhan, CN | new org |
| Univ. Paris-Sud; Université Paris-Saclay | Orsay, FR | aliases or new orgs (check the registry; earlier C2N blocks carry the same strings) |
| University of Illinois at Urbana–Champaign | Urbana, US | alias (en dash form) to `org_university_of_illinois_urbana_champaign` (hyphen form already an alias) |
| University of Minnesota | Minneapolis, US | new org |
| University of Strathclyde | Glasgow, GB | new org |
| Xiamen University | Xiamen, CN | new org |

(18 strings in `unmapped_orgs.csv`: NUDT appears with two units.)

## Privacy and as-printed scan

- Grep over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv` and `papers.csv` for contact / URL
  patterns, street / road / avenue / suite / room / building words, postal-box words, "No." + digit and digit runs of
  4 or more: 0 hits apart from paper-id years and decision ids; no contact address, street, postal code or P.O. box anywhere.
  One building name appears in a note (li2022a, F1). The kaspar2015 site name is stored in `skip_prefix` (D366
  mechanism, required by the checker) and repeated in that paper's note; accepted as the D366 form. Campus names in the
  hu2025a / lin2021a notes follow the lit_h01 / h10 / h33 notes.
- `show` masking gap (outside the batch): the morton2021 footnote keeps an unmasked fragment of a contact address
  where the address breaks across a line (text and PDF layers). Not copied into the batch or this record. Recommend a
  masking fix for line-broken addresses.
- As printed (kept, correct): National Institute of Advanced Science and Technology; III–V Laboratory and CEA–Leti (en
  dashes); University of Illinois at Urbana–Champaign (en dash); R & D Center; Center of Quantum Science and
  Engineering; Chirstophe Jany (as in the list); Tsinghua University Department (no comma).

## Commands (2026-11-15, log times)

| Command | Result |
|---|---|
| `check lit_h44 --corpus lit --dry-run` 23:22:03 (pid 66122) | 0 errors, 5 warnings (3 explicit slots; harris2017, morgan2021 order differs); slots 177, recorded 174, no_header 3; rows 216 (grade A 216; printed 145, prose 50, single 15, per_author 6; primary 177, additional 38, present address 1); papers ok 23, partial 1; multi-affiliation slots 32; 18 unmapped org strings |
| `show lit_h44 --corpus lit --codes <id> --pdf`, all 24 (+ lin2021a `--pages 2`) | headers, statements and author lists read (scratchpad only) |
| page renders (pymupdf, scratchpad `h44/*.png`) | 4 renders, 2 read (morgan2021, kim2021a) |
| `h44/probes/probe.py` on scratch copies, 23:23:00-23:26:32 | below; repo batch files md5 unchanged; probe checks wrote their usual logs under `logs/` (prefix `lit_headers_check_lit_p44`) |

| probe | change | result | reading |
|---|---|---|---|
| BASE | unchanged copy | 0 errors, 5 warnings | baseline |
| K1 | kim2021a block 1 with org UIUC, authors readable | 4 errors | partial forced (call 1) |
| K2 | kim2021a block 1 department as org | 0 errors | not a valid form |
| G1 | liu2020b block 3 as present address | 2 errors | Current address gap (call 2) |
| S1 / S3 / S4 | explicit slot removed (li2013 #2, kaspar2015 #13, morgan2021 #3) | 2 errors each | slots required |
| S2 | li2013 #1 slot removed | 0 errors | redundant, harmless |
| S5 | li2022a Strain without slot 0 | 1 error | slot 0 required |
| S6 | li2013 #2 as slot 0 + author_list_differs | 0 errors | checker neutral (question 1) |
| O1 | morgan2021 Kharas before Knecht | 0 errors, order warning gone | F2 valid |
| M1 | harris2017 Englund without dropped 6 | 0 errors | G1 (last-author gap) |
| M2 | li2018a Gao without dropped 5 | 2 errors | bound |
| M3 | li2013 Hochberg without clause P5 | 3 errors | clause bound |
| M4 | kaspar2015 Pavarelli P4 | 4 errors | statement membership bound |
| C1 | jung2021 without campus | 0 errors | campus by precedent, not forced |
| P1 | kaspar2015 without skip_prefix | 4 errors | skip_prefix required |
| L1 | kita2021 locality Tokyo | 0 errors | G2 (any printed place accepted) |
| FIX_all | F1 + F2 + N1 + N2 | 0 errors, 4 warnings | fixes valid |

## Checker gaps observed (scripts not edited)

- G1 Last author's further markers not bound: harris2017 Englund (M1). Known (D442 / D546 / D557 / h43 G1).
- G2 Locality accepts any printed place in the block (L1). Known (h42 / h43 G2). YAML exact.
- h17 G3 Shared org suffix (kim2021a). Known; re-record after the fix.
- Current address cue not accepted (liu2020b). Known (D286 list); re-record after the fix.
- `show` / text masking: line-broken contact fragment left unmasked (morton2021). New; outside the batch.

## Verdict

GO with fixes F1 and F2. All 177 list slots and the header-only author carry the right person; the 174 slots with rows
have the right markers, org, unit, campus, city and country; the 3 slots without rows are correctly unreadable.
Nothing is invented, no block is missed, no contact, street or postal text is recorded. F1 removes a building name
from a note; F2 aligns the morgan2021 author order with the printed grid (header position only). N1 / N2 are optional
note completions.
