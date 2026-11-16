---
title: Fresh-context audit of the lit author-affiliation batch lit_h43 (24 papers)
date: 2026-11-15
mode: read-only on the batch (wrote only this record and scratchpad renders / probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only with --dry-run, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h43/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D380, D410, D412, D426, D442, D466, D546, D550, D557); format from the 2026-11-14 h42 audit; read-only comparison with earlier batches (HK localities, Colorado / UC campuses, Twente unit chains, lit_h31 liu2024, lit_h32 smith2023, lit_h17 cabezon2012)
verdict: GO; 202 slots audited, 202 ok (190 with rows, 12 correctly without rows), 0 imprecise, 0 wrong; no YAML fix required (one optional note edit N1); partial calls: cheung2015 and errandoherranz2019 forced by the checker, chen2022d not forced but the faithful choice (keep, liu2024 precedent); checker gaps G1-G4
---

# Lit header batch audit: lit_h43 (2026-11-15)

## Scope

Batch lit_h43: 24 papers (Optics Express 9, preprints 8, IEEE journals 6 (JQE, JSTQE x2, PTL, JLT, Proc. IEEE), one
accepted manuscript); 202 slots (2 papers `slots_from_header`: akiyama2007 3, bakonyi2003 7); 215 rows. Restricted
corpus: this record names only authors, orgs, units, cities and countries; no paper text is quoted and no contact,
street, building, postal-box or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h43 --corpus lit --codes <id> --pdf`
  (all 24; output kept in the scratchpad only).
- Rendered pages (pymupdf, 170 dpi, scratchpad `h43/*.png`): deng2019 page-1 footnote (statement 1 is masked in the
  `show` output together with the contact run), header crops of chen2022d, gao2017, cheung2015, and the full page 1 of
  errandoherranz2019.
- Per slot: printed name vs `compare.csv` and the `show` author list; marker run vs text and PDF layer (both layers
  identical for all printed-marker papers); block fields (org, unit chain, more_orgs, campus, city, country); role;
  locator; grade. Every distinct (paper, org, org id, match basis, locality, country) tuple of `header_rows.csv` read.
- Prose papers (akiyama2007, bakonyi2003, bogaerts2010, chen2006, deng2019, errandoherranz2019): every statement
  subject, verb, clause and field read against the footnote.
- Missed blocks: cue scan of the whole `text.md` of all 24 (now with / at, present / current address, currently,
  is / are / was / were (also / now) with, also with, on leave, visiting, formerly, deceased, permanent address,
  affiliat-): every hit is either a recorded statement / block or biography / body text (bakonyi2003, bogaerts2010,
  errandoherranz2019 biographies; chen2024c supplement repeats the same three blocks). No missed block.
- Probes on scratch copies (`h43/probes/probe.py` in the session scratchpad, scratch `LIT_BASE`, batch name
  `lit_p43`). md5 of every repo batch file identical before and after the audit; `check_stamp.txt` matches
  `headers.yaml` (sha256 b51ff315...).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h43 | 24 / 24 | 202 | 202 | 0 | 0 |

- Rows 215 (all grade A: printed 163, prose 44, single 8; primary 199, additional 16); recorded 190, no_header 12
  (chen2022d 5, cheung2015 1, errandoherranz2019 6); papers ok 21, partial 3, unreadable 0; `author_list_differs` 0;
  explicit slots 6 (boller2019 #7, catalalahoz2026 #3, chatterjee2019 #2, deng2019 #1 and #11, fan2020 #3); present
  addresses 0 rows (the only one, cheung2015 block 2, belongs to an unreadable author); prose blocks 14 (6 papers);
  `order_differs` 1 (deng2019); multi-affiliation slots 16; 19 unmapped org strings (37 rows).
- Per paper (slots / rows): akiyama2007 3 / 5; bakonyi2003 7 / 7; baumgartner2020 11 / 12; bogaerts2010 7 / 14;
  boller2019 20 / 23; bonneville2020 4 / 4; bucio2017 4 / 4; catalalahoz2026 13 / 14; chang2018a 15 / 16;
  chatterjee2019 4 / 6; chen2006 2 / 2; chen2022c 6 / 7; chen2022d 14 / 11; chen2023b 5 / 7; chen2024c 14 / 15;
  cheung2015 4 / 3; deng2019 14 / 16; dostart2020a 4 / 4; errandoherranz2019 6 / 0; fan2020 9 / 9; fard2017 4 / 4;
  gao2017 7 / 7; gao2022 15 / 15; han2018 10 / 10. All rated ok.

### Per-slot field counts (202 slots)

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (202) | 202 | 0 | 0 |
| markers (202; 12 unreadable carry the verified subset) | 202 | 0 | 0 |
| blocks (org / unit / campus / locality / country) (190 with rows) | 190 | 0 | 0 |
| prose blocks (14 blocks, 6 papers) | 14 | 0 | 0 |
| present addresses (1 block, no row) | 1 | 0 | 0 |
| locators (all blocks) | all | 0 | 0 |

## Per-paper findings

- akiyama2007 (3; prose, no author list): statement 1 names Akiyama and Sugawara with QD Laser Inc. and Fujitsu
  Laboratories Ltd. (comma-joined, recorded as org + more_orgs), Atsugi, JP; statement 2 Arakawa with University of
  Tokyo, Tokyo, JP. Leading article of the statement not copied (corpus practice: 549 of 558 prose blocks, this batch included, carry no article). ok.
- bakonyi2003 (7; prose, no author list): Bakonyi, Onishchukov, Tünnermann with Friedrich-Schiller University of Jena +
  Institute of Applied Physics, DE, no city printed (locality "" correct); Su, Lester with University of New Mexico +
  Center for High Technology Materials, Albuquerque, US; Gray, Newell with Zia Laser, Inc., Albuquerque, US. Author
  order as printed. ok.
- baumgartner2020 (11; printed): runs 1,2 / 1 / 1 / 3 / 4 x4 / 2 / 1 / 1 as printed. IBM Research – Zürich, Rüschlikon;
  ETH Zürich + IQE and + IEF, Zürich; all CH; IBM T. J. Watson Research Center, Yorktown Heights, US. List #10 Bert Jan
  Offrein vs BERT J. OFFREIN automatic. ok.
- bogaerts2010 (7; prose, "The authors"): Ghent University + Photonics Research Group, Department of Information
  Technology, more_orgs Interuniversity Microelectronics Center (alias to `org_imec`), Ghent, BE; all seven carry P1.
  ok.
- boller2019 (20; printed): Fallnich printed 3,1 and recorded in that order (probe M1: 1,3 fails). Block 1 four-part
  unit chain before University of Twente, Enschede, NL; LioniX International BV, Enschede, NL; University of Münster +
  Institute of Applied Physics, DE, no city (locality "" correct). #7 explicit slot (Peter / Petrus, D287; probe S4
  without slot: 2 errors). List #13 Ronald Haentjens Dekker vs Ronald Dekker automatic. ok.
- bonneville2020 (4; single): McMaster University + Department of Engineering Physics, Hamilton, CA. ok.
- bucio2017 (4; single): University of Southampton + Optoelectronics Research Centre, Southampton, GB (UK printed). ok.
- catalalahoz2026 (13; printed): Universitat Politècnica de València + Photonics Research Labs, iTEAM Research
  Institute, Valencia; iPronics Programmable Photonics S.L., Valencia; both ES; Lumiphase AG, Stäfa, CH; University of
  West Attica, Athens, GR; CEA-Leti, Grenoble, FR. #3 explicit slot (Pérez-López vs list Pérez, dropped second family
  name, D287; probe S5: required). ok.
- chang2018a (15; printed): University of California + campus Santa Barbara + ECE department; RMIT University + School
  of Engineering, Melbourne, AU; NIST Time and Frequency Division and Applied Physics Division, Boulder, US. MJ.
  Kennedy as printed. ok.
- chatterjee2019 (4; printed): Indian Institute of Science + Center For Nano Science and Engineering (capital For as
  printed) and + Molecular Biophysics Unit, Bangalore, no country printed ("" correct). #2 SAUMITRA explicit slot
  (probe S1 without slot: 0 matches, required). ok.
- chen2006 (2; prose, "The authors"): The Hong Kong University of Science and Technology + Photonic Device Laboratory,
  Department of Electronic and Computer Engineering, locality Hong Kong, HK; districts in the note. Same form as the
  earlier HKUST records (lit_h14 yang2014, lit_h21 xue2022). ok (question 4).
- chen2022c (6; printed): University of Washington + ECE and + Department of Physics, Seattle, US; Ningbo University +
  faculty / Zhejiang provincial key laboratory chain, Ningbo, CN. ok.
- chen2022d (14; printed, partial): runs read on text, PDF and the render: 1 / 2,3 / 4,5 / 2 / 2 / 2,3 / 1 / 4 / 4 / 5
  / 6 / 1,7 / 2,3,8 / 1,9; markers 8 and 9 are contact lines (dropped, correct). Recorded blocks: Zhejiang University
  chain, Hangzhou; South China Normal University + National Center for International Research on Green
  Optoelectronics, Guangzhou; Sun Yat-Sen University + state key laboratory / school, Guangzhou; The Hong Kong
  Polytechnic University + Photonics Research Center with two departments, Hong Kong, HK (Hong Kong SAR printed);
  Zhejiang University + Jiaxing chain, Jiaxing; CN otherwise. Block 2 not recorded (see call 1); authors 2, 4, 5, 6, 13
  unreadable. #12 Daoxin Dai A list artefact (D412). ok.
- chen2023b (5; printed): City University of Hong Kong + Department of Electrical Engineering and + state key
  laboratory, locality Kowloon, HK (CityU precedent); City University of Hong Kong Dongguan Research Institute, Dongguan,
  CN and ... Shenzhen Research Institute, Shenzhen, CN (own orgs, li2025d precedent). ok (question 4).
- chen2024c (14; printed): Jilin University + state key laboratory / college, Changchun; Peng Cheng Laboratory,
  Shenzhen; both CN; Advance Micro Foundry Pte. Ltd., Singapore, SG. List #13 Guo-Qiang Lo automatic. ok.
- cheung2015 (4; printed, partial): block 1 University of California + campus Davis + ECE department, Davis, US; block
  2 "Currently with" Furukawa Electric + R&D Laboratory Photonic Research Center, Ichihara, JP (`present_address`,
  correct; prefecture not recorded). Author 2's only block (see call 2). ok.
- deng2019 (14; prose, render read): statement 1 (11 authors) McGill University + Photonics System Group, Department
  of Electrical and Computer Engineering, Montreal, CA; El-Fiky statement P2 (McGill) + clause P3 Alexandria
  University + Electrical Engineering Department, Alexandria, EG; Zhu P4 (McGill) + clause P5 UESTC + key laboratory,
  Chengdu, CN; Koh P6 Lumentum Corporation, Milpitas, US. YAML author order = printed author line (list order
  differs: warning, expected). #11 explicit slot (Jaques printed, list Jacques: misspelling, D287; probe S3: required).
  #1 Deng Mao vs list Mao Deng: explicit slot 1 not required (probe S2 passes without it), harmless; name-order swap
  for the D426 review list (D550). ok.
- dostart2020a (4; printed): University of Colorado + campus Boulder + department, Boulder, US (as the 8 earlier
  records); Boston University + department, Boston, US. ok.
- errandoherranz2019 (6; prose, partial, page render read): the title, author line and footnote statements are printed
  after the abstract in the left column of page 1. Statement 1: Errando-Herranz, Edinger, Gylfason with KTH Royal
  Institute of Technology, Stockholm, SE; statement 2: Takabayashi, Sattari, Quack with École Polytechnique Fédérale de
  Lausanne (EPFL), Lausanne, CH. Marker assignment correct. All six unreadable (see call 3). ok.
- fan2020 (9; printed): University of Twente three-part chain, Enschede, NL; LioniX International BV, Enschede, NL.
  #3 explicit slot (Peter / Petrus, as boller2019). ok.
- fard2017 (4; printed): McGill University + ECE, Concordia University + ECE, both Montreal, CA (Quebec not recorded).
  ok.
- gao2017 (7; printed, render read): Huazhong University of Science and Technology + Wuhan National Laboratory for
  Optoelectronics; Wuhan Research Institute of Post & Telecommunications + state key laboratory; both Wuhan, CN. Xi
  Xiao marker 3 is a contact line (dropped, correct). ok.
- gao2022 (15; printed): Caltech + T. J. Watson Laboratory of Applied Physics, Pasadena; EPFL (as printed, alias) +
  Institute of Physics, Lausanne, CH; University of California + campus Santa Barbara (printed without comma) + ECE
  Department; NIST, Boulder; US otherwise. Asterisk (equal contribution) and dagger (corresponding) used by no block.
  ok.
- han2018 (10; printed): Nanjing University + three-part chain, Nanjing; National University of Defense Technology,
  Changsha (Hunan not recorded); both CN. ok.

## Extractor calls (verified, with ruling recommendation)

1. chen2022d partial (block 2 not recorded, authors 2, 4, 5, 6, 13 unreadable). The page prints a building name and
   number between the unit chain and South China Normal University (render read). Probes: D1 (unit chain + org SCNU,
   no skip) 2 errors (unit and org not contiguous); D4 (org SCNU only) 2 errors (block must start with its first
   printed field); a `skip_between` would store the building number (D244 / D426 G6, not allowed). D2 (provincial key
   laboratory as `org` + SCNU in `more_orgs`) and D3 (same plus the academy in `more_orgs`) pass with 0 errors, so the
   partial is not forced by the checker. Those forms are the lit_h17 cabezon2012 / lit_h32 smith2023 workaround: they
   create an unmapped org row for a laboratory that the print shows as a unit of SCNU (D2 also drops the academy). The
   closest precedent (lit_h31 liu2024: Zhejiang University unit chain + building number) is partial, and D546 put both
   forms on the G6 re-record list. Ruling: keep as recorded; add chen2022d (block 2 values are in its note) to the D546
   building-number re-record list. Authors 2, 6, 13 carry only marker 3 while unreadable (no rows; block 3 stays
   verified), as liu2024.
2. cheung2015 partial (author 2 unreadable). Probe C1 (Kawakita readable): 1 error ("no markers and the paper has no
   unmarked block"; the present-address marker does not count). This is the D426 G4 gap (yang2010, chen2000,
   keyvaninia2019, moscosomartir2017). Forced; keep. Add cheung2015 #2 to the G4 re-record list (values: Furukawa
   Electric, R&D Laboratory Photonic Research Center, Ichihara, JP, present address).
3. errandoherranz2019 partial (all six unreadable). Probe E1 (all six readable): 12 errors, every author "not named in
   the statement subject" in both layers: each subject name is followed by its parenthesized contact and the closing
   parenthesis is a D366 subject boundary, so the subject before the verb is empty. Forced by the checker; no YAML
   form avoids it. Status: the paper is the first lit paper with every author unreadable; `partial` (blocks recorded
   and verified, no rows) is preferable to `unreadable` (which would drop the verified values needed for a re-record).
   Ruling: keep; new checker gap G3 (contact parenthesis inside a statement subject); add to the re-record list.
4. Explicit slots (6). Required (probe errors without them): boller2019 #7, fan2020 #3 (Peter / Petrus), catalalahoz2026
   #3, chatterjee2019 #2, deng2019 #11. Not required but harmless: deng2019 #1. All D287-conform (initials agree).
5. Unit chains printed before the org (boller2019, fan2020, chen2022c, chen2022d block 7, han2018, catalalahoz2026
   block 1): copied as one contiguous segment (D246), as the earlier Twente / Jiaxing records. Accept.

## Fixes (exact YAML edits)

No required fix: no slot, marker, block field, locator, role or grade is wrong or imprecise.

N1 (optional, note only). In `lit:cheung2015` replace

```yaml
no rows; checker gap: present-address-only author);
```

with

```yaml
no rows; checker gap D426 G4: present-address-only author);
```

Rows unchanged (215).

## Open questions (with recommendation)

1. chen2022d (call 1): keep partial; add to the D546 G6 re-record list. Recommended: yes.
2. cheung2015 #2 (call 2): add to the D426 G4 re-record list. Recommended: yes.
3. errandoherranz2019 (call 3): keep `partial` for an all-unreadable paper; new checker gap G3; re-record list.
   Recommended: yes, and state in DevLog-011 that `partial` is allowed when every author is unreadable for a checker gap
   while the blocks verify.
4. HK locality split inside this batch: chen2006 (HKUST) records Hong Kong with the districts in the note (lit_h14,
   lit_h21 precedent and D366 "district printed before the city goes to the note"); chen2023b (CityU) records Kowloon
   (11 earlier CityU records). Both follow their org's precedent; the checker accepts either (probes H1, H2, H3). No
   change here; recommend one corpus rule in the org / locality round (D366 reading: Hong Kong).
5. D412 correction file: chen2022d #12 (Daoxin Dai A). D426 review list: deng2019 #1 (name-order swap). Recommended:
   yes.
6. G1 test list: chen2022d #14 (Liu Liu, dropped contact marker 9 removable, probe M4). Recommended: add to the D442 /
   D546 / D557 last-author list.

## Unmapped org names (org round, no YAML change)

| printed org (unit) | place | proposal |
|---|---|---|
| Advance Micro Foundry Pte. Ltd. | Singapore, SG | new org (check registry for an existing AMF row) |
| Alexandria University (Electrical Engineering Department) | Alexandria, EG | new org |
| Boston University | Boston, US | new org or alias if the registry holds it under another name |
| City University of Hong Kong Dongguan Research Institute | Dongguan, CN | child of `org_city_university_of_hong_kong` |
| City University of Hong Kong Shenzhen Research Institute | Shenzhen, CN | child of `org_city_university_of_hong_kong` |
| Concordia University | Montreal, CA | new org |
| Friedrich-Schiller University of Jena | (no city), DE | new org |
| Fujitsu Laboratories Ltd. | Atsugi, JP | new org (Fujitsu child) |
| Indian Institute of Science (2 units) | Bangalore, no country | new org |
| McMaster University | Hamilton, CA | new org |
| National University of Defense Technology | Changsha, CN | new org |
| Ningbo University | Ningbo, CN | new org |
| QD Laser Inc. | Atsugi, JP | new org |
| RMIT University | Melbourne, AU | new org |
| University of New Mexico | Albuquerque, US | new org |
| Wuhan Research Institute of Post & Telecommunications | Wuhan, CN | new org |
| Zia Laser, Inc. | Albuquerque, US | new org |
| iPronics Programmable Photonics S.L. | Valencia, ES | new org |

(19 strings in `unmapped_orgs.csv`: the Indian Institute of Science appears with two units.)

## Privacy and as-printed scan

- Grep over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv` and `papers.csv` for contact / URL
  patterns, street / road / avenue / building / room / postal-box words, "No." + digit and digit runs of 4 or more:
  0 hits apart from paper-id years. Notes name only the kinds of omitted text (street address, postal codes, building
  number) and districts (allowed by D366). The chen2022d note lists the block 2 org / unit / city / country only.
- As printed (kept, correct): Center For Nano Science and Engineering; MJ. Kennedy; Sun Yat-Sen University; IBM
  Research – Zürich (en dash); Mesa+ Institute for Nanotechnology; Swiss Federal Institute of Technology Lausanne
  (EPFL). No `skip_prefix`, `skip_between`, `continued` or `slot: 0` in this batch; `clause: true` on deng2019 P3, P5.

## Commands (2026-11-15, log times)

| Command | Result |
|---|---|
| `check lit_h43 --corpus lit --dry-run` 22:58:22 (pid 43747) | 0 errors, 6 warnings (5 explicit slots set, deng2019 order differs); slots 202, recorded 190, no_header 12; rows 215 (grade A 215; printed 163, prose 44, single 8; primary 199, additional 16); papers ok 21, partial 3; slots_from_header 2; multi-affiliation slots 16; 19 unmapped org strings |
| `show lit_h43 --corpus lit --codes <id> --pdf`, all 24 | headers, statements and author lists read (scratchpad only) |
| page renders (pymupdf, scratchpad `h43/*.png`) | 5 renders read |
| `h43/probes/probe.py` on scratch copies, 23:02:43-23:05:02 | below; a first run stopped after BASE on a probe-script assertion (fixed); repo batch files md5 unchanged; probe checks wrote their usual logs under `logs/` (prefix `lit_headers_check_lit_p43`) |

| probe | change | result | reading |
|---|---|---|---|
| BASE | unchanged copy | 0 errors, 6 warnings | baseline |
| E1 | errandoherranz2019 all six readable | 12 errors (subject empty, D354) | partial forced (call 3) |
| C1 | cheung2015 Kawakita readable | 1 error | G4 gap, partial forced (call 2) |
| D1 | chen2022d block 2 unit chain + org SCNU | 2 errors (not contiguous) | building span blocks it |
| D2 | block 2 lab as org + more_orgs SCNU, authors readable | 0 errors | workaround passes (call 1) |
| D3 | D2 plus academy in more_orgs | 0 errors | workaround passes (call 1) |
| D4 | block 2 org SCNU only | 2 errors (first field) | not a valid form |
| H1 / H3 | chen2006 locality Kowloon / Clear Water Bay | 0 errors | checker neutral (G2) |
| H2 | chen2023b locality Hong Kong | 0 errors | checker neutral (G2) |
| K1 | cheung2015 locality = the area name printed before the city | 0 errors | G2: non-city place accepted |
| S1 / S3 / S4 / S5 | explicit slot removed (chatterjee2019, deng2019 #11, boller2019, catalalahoz2026) | 2 errors each | slots required |
| S2 | deng2019 #1 slot removed | 0 errors | slot redundant, harmless |
| M1 | boller2019 Fallnich 1,3 | 2 errors | printed order bound |
| M2 | deng2019 El-Fiky without clause P3 | 3 errors | clause bound |
| M3 | akiyama2007 Arakawa P1 | 5 errors | statement membership bound |
| M4 | chen2022d Liu Liu without dropped 9 | 0 errors | G1 (known last-author gap) |

## Checker gaps observed (scripts not edited)

- G1 Last author's further markers not bound: chen2022d Liu Liu passes without dropped marker 9 (M4). Same as
  D442 / D546 / D557 / h42 G1; new test case. YAML exact.
- G2 Locality accepts a district or area printed in the block instead of the city (H1, H3, K1); D366 requires the
  city. Same as h42 G2. YAML exact.
- G3 New: a parenthesized contact after each subject name ends the statement subject (D366 ")" boundary), so every
  author of errandoherranz2019 is reported as not named (E1). Fix direction: treat a parenthesis that held a stripped
  contact as part of the subject. YAML records the verified blocks; re-record after the fix.
- G4 Known: D426 G4 present-address-only author (cheung2015 #2) and D426 G6 building-number span between unit and org
  (chen2022d block 2). YAML exact; both papers go on the re-record lists.

## Verdict

GO. All 202 slots carry the right person; the 190 slots with rows have the right markers, org, unit, campus, city and
country; the 12 slots without rows are correctly unreadable. Nothing is invented, no block is missed, no address or
contact text is recorded. No YAML fix is required; N1 is an optional note completion. The coordinator should add
chen2022d (G6), cheung2015 #2 (G4) and errandoherranz2019 (new G3) to the re-record lists, chen2022d #12 to the D412
file, deng2019 #1 to the D426 review list, and settle the HK locality form (question 4) in the org / locality round.
