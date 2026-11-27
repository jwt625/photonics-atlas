---
title: Fresh-context audit of the lit author-affiliation batch lit_h73 (23 papers)
date: 2026-11-27
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; checker run only in dry-run or write-run on scratch copies with logs in the scratchpad; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h73/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D352, D366, D369, D426, D449, D461, D756 and earlier lit rulings; D249, D282, D285, D286d, D287, D288, D301 from DevLog-008; format from the lit_h72 audit
verdict: GO, no required fix; 166 slots audited, 166 recorded, 0 wrong, 0 imprecise; all named extractor calls confirmed
---

# Lit header batch audit: lit_h73 (2026-11-27)

## Scope

Batch lit_h73: 23 papers (17 Optica Publishing Group journal headers, numbered markers or a single block, 1 Optics Express 2005 single
block, 5 arXiv preprints); 166 slots, 2 papers `slots_from_header` (kim2005,
herr2012); 199 rows. Restricted corpus: this record names only authors, orgs, units, cities and countries; no paper
text is quoted and no contact, street, building, park, box or postal text is copied (such spans are named by type
only).

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h73 --corpus lit --codes <id> --pdf`
  (all 23); output kept in the session scratchpad `h73_audit/show/` only. `show` wrote no log of its own (the new
  files under `logs/` in that window are component-merge logs of other streams).
- Per slot: printed name and marker run in both layers vs the `show` author list (or the header order for the 2
  header-slot papers) and `compare.csv`; block fields (org, unit chain, campus, city, country); locators; notes.
  Contact lines are masked in `show`; for fan2017, dong2025, xiang2022a and zhu2021 only the leading marker character
  of each contact line in `text.md` was inspected (nothing copied): fan2017 3 / 4, dong2025 6 / 7 / asterisk,
  xiang2022a 6 / 7 / asterisk, which confirms the dropped contact markers.
- Committed lit batches grepped for each form question (UCSB campus with a department after the campus, Wuhan
  National Laboratory for Optoelectronics, Ministry of Education centres and key laboratories, Hewlett Packard Labs /
  Enterprise, ETH Zürich localities, RF SUNY Polytechnic Institute, CRANN / CONNECT, Tianjin University key-laboratory
  chains, Pusan / Busan, district notes); registry `organizations.csv` for the Ministry of Education centre, the Hubei
  key laboratory, Hewlett Packard Enterprise and the Agency for Defense Development.
- All 199 rows of `header_rows.csv` read by paper: roles primary 166, additional 33; basis printed 148, single 51;
  all grade A. `compare.csv`: 166 `recorded`, `order_differs` false everywhere. Campus rows (park2007a, dong2025,
  skipper2025; 15) map to org_ucsb; Caltech 11 rows org_caltech; HUST 10 org_huazhong_university_of_science_and_technology;
  the Ministry of Education centre (8) and the Hubei key laboratory (8) map to their own registry ids; HPE 7
  org_hewlett_packard_enterprise; ETH Zürich 6 org_eth_zurich; Intel 3 org_intel.
- Address / contact scan of `headers.yaml` and every derived file (contact sign, URL, 3+-digit numbers, street, road,
  avenue, boulevard, drive, suite, building, room, hall, box, cedex, e-mail / mail, phone, fax, postal, and every
  street, park, building-code and region token printed in this batch's blocks). Hits: years in paper ids, DevLog and decision ids
  (011, D352), the stamp hash, type words in notes ("street address(es)", "postal code(s)", "an industrial park
  name"), the ward Hodogayaku (ito2019) and the district Yuseong-gu (yoon2023) named in notes (D366: a district
  printed before the city goes to the note; committed precedents Fuyang, Shatin, Kowloon, Komaba). No contact, URL,
  postal code, street, building, park, box or neighbourhood text anywhere, notes included.
- Probes on scratch copies (`h73_audit/probes/probe.py` + `mk.py`, scratch `LIT_BASE`, batch name `lit_p73`,
  `cmd_check(..., dry_run=True)`, `RunLog` redirected to the scratchpad; 37 variants plus the base write run). Run of
  the batch as written: 0 errors, 1 warning (xue2015 explicit slot 7); scratch write-run derived files byte-identical
  to the stamped `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`, `check_stamp.txt`. md5 of every repo batch
  file identical before and after the audit; `check_stamp.txt` matches `headers.yaml` (sha256 b844d551...).

## Counts

| batch | papers audited / total | slots audited | ok | gap (correct handling, no row) | imprecise | wrong |
|---|---|---|---|---|---|---|
| lit_h73 | 23 / 23 | 166 | 166 | 0 | 0 | 0 |

- Papers ok 23, partial 0, unreadable 0; `slots_from_header` 2 (exactly the papers.csv rows with `n_authors_meta` 0,
  each prints the D352 line in `show`); `author_list_differs` 0; explicit slots 1 (xue2015 #7); order warnings 0;
  present addresses 0; prose blocks 0; dropped markers 7 (fan2017 #3 #7, dong2025 #5 #6, xiang2022a #1 #2 equal
  contribution, #6 #10 contact); unreadable authors 0; 8 unmapped org strings.
- Per paper (slots / rows): zhu2021 15 / 16; woods2020 9 / 9; park2007a 7 / 7; fan2017 7 / 7; hamrouni2024 9 / 11;
  kim2005 3 / 3; xue2015 9 / 13; dong2025 6 / 9; suh2016 5 / 5; riemensberger2020 7 / 7; kim2020 6 / 6; yoon2023 8 / 8;
  yi2015 5 / 5; liang2021 7 / 7; herr2012 8 / 9; ye2023a 11 / 28; xiang2022a 10 / 11; ashtiani2019 2 / 2; ito2019 8 / 8;
  li2019a 5 / 5; mehta2020 6 / 6; skipper2025 7 / 9; wang2021c 6 / 8.
- Privacy findings: 0. Notes: 23 correct.

### Per-slot field counts

| field | ok | gap | imprecise | wrong |
|---|---|---|---|---|
| name / slot (166) | 166 | 0 | 0 | 0 |
| markers (printed / single, incl. 7 dropped) (166) | 166 | 0 | 0 | 0 |
| header position / order | 166 | 0 | 0 | 0 |
| blocks (org / unit / campus / locality / country) (199 rows) | 199 | 0 | 0 | 0 |
| roles (primary / additional) | 199 | 0 | 0 | 0 |
| locators (all p.1 header) | all | 0 | 0 | 0 |
| notes (23) | 23 | 0 | 0 | 0 |

## Per-paper findings

- zhu2021 (15; printed, capitals): markers 1 x11, 1,2 (Sinclair), 3, 3, 1 read in both layers (probe ZH1 Sinclair
  without 2: 3 errors). Harvard University with the SEAS unit, Cambridge, US; Caltech with the division + alliance
  unit joined by "and" (one printed segment), Pasadena, US; HyperLight Corporation, Cambridge, US. List forms Soumya
  Shankar Ghosh / Neil E. Sinclair matched by name. ok.
- woods2020 (9; printed, capitals, names split over lines): University of Southampton with School of Physics and
  Astronomy (1) and Optoelectronics Research Centre (2), Southampton, "UK" -> GB (county, street and postal code not
  recorded). Probe WO1 (Tropper on 2) 2 errors. List form Péter Horák matched. ok.
- park2007a (7; printed): call verified. Block 1 org University of California + campus Santa Barbara, locality Santa
  Barbara, US; the department after the campus is not recorded: probe PK1 (unit added to the campus form) 2 errors,
  the unit is not contiguous with the org across the campus; PK2 (whole "University of California, Santa Barbara" as
  org + department) 0 errors but violates D301; the committed lit form drops the department in the same layout (two
  committed notes, "unit not recordable as one segment with the org across the campus"). Blocks 2 / 3 Intel
  Corporation, Santa Clara, US and Jerusalem, IL (a building code and an industrial park name not recorded). List
  forms Ying-Hao / Oded M. / John Edward matched. ok.
- fan2017 (7; printed, capitals): call verified. Tianjin University with the laboratory + Ministry of Education key
  laboratory + school chain (committed Tianjin chain carrying a Ministry of Education key laboratory inside the unit
  exists), Tianjin (postal code before the city not recorded), CN; East China Normal University State Key Laboratory
  of Precision Spectroscopy, Shanghai, CN. #3 Gu 2,3 and #7 Hu 1,4: 3 and 4 lead the two contact lines (dropped,
  contact footnote). Probe FN1 (Gu without dropped 3) 2 errors; FN2 (Hu without dropped 4) 0 errors: last-author gap
  (O1), Hu 1,4 read in both layers. ok.
- hamrouni2024 (9; printed, capitals): Université de Neuchâtel Laboratoire Temps-Fréquence, Neuchâtel, CH (street
  after the org not recorded); Stanford University E. L. Ginzton Laboratory, Stanford, US; NTT Research, Inc. with
  Physics & Informatics Laboratories printed after it, Sunnyvale, US. Probe HA1 (Jankowski without 3) 3 errors. List
  form M. M. Fejer matched. ok.
- kim2005 (3; single, slots from header): call verified. Header order = YAML (probe KM1 authors swapped: 2 errors,
  unlike the prose-basis gap of h72 O1). Unit chain group, college and two centres joined by slashes, glued
  "Excellence(FPCE)" as printed, University of Central Florida, Orlando, US (street, state and postal code not
  recorded). Probe KM2 (unit cut after the college) 2 errors: the whole chain is required. ok.
- xue2015 (9; printed, preprint): call verified. Purdue ECE (1) and Birck Nanotechnology Center (2), West Lafayette, US.
  #7 printed Dan E. Leaird vs list Daniel E. Leaird: probe X1 without the slot 2 errors (slot 7 unmatched); a short
  form with agreeing initials and the same distinctive family name is a D287 nickname / name-part case, so the
  explicit slot is right and `author_list_differs` stays false. Probe XU1 (Xuan without 2) 2 errors. ok.
- dong2025 (6; printed): call verified. Markers 1,2,3 / 4 / 2 / 5 / 2,6 / 1,4,7 read in the PDF layer (daggers equal
  contribution, asterisk corresponding); 6 and 7 lead contact lines (dropped). Blocks 1 / 4 University of California +
  campus Santa Barbara with IEE / ECE units, Santa Barbara, US; KAUST Integrated Photonics Laboratory, Thuwal (province
  after the city in the note), SA; Université Laval ECE, Québec City, CA; Sandia National Laboratories, Albuquerque,
  US. Probes DG1 (Wan without 6) 2 errors, DG3 (Dong without 3) 3 errors; DG2 (Bowers without dropped 7) 0 errors:
  last-author gap (O1), 1,4,7 read in both layers. List form John Edward Bowers matched. ok.
- suh2016 (5; printed single block with marker 1, D285): Caltech T. J. Watson Laboratory of Applied Physics, Pasadena,
  US. Daggers equal contribution, asterisk corresponding (legend on page 1). ok.
- riemensberger2020 (7; single, preprint): EPFL with the acronym, then the LPQM laboratory (org printed first),
  Lausanne (country-prefixed postal code not recorded), CH. Probe RI1 (acronyms removed) 0 errors, neutral; acronyms
  kept as printed (contract). The asterisk legend is a contact line late in the paper. List form Tobias Jan Kippenberg
  matched. ok.
- kim2020 (6; printed, capitals): Pusan National University ECE, locality "Pusan" (Busan in parentheses after it;
  D288 first printed form; probe KI1 Busan 0 errors, neutral), KR; Kwangwoon University ECE, Seoul, KR; Agency for
  Defense Development, Daejeon, KR. "South Korea" -> KR. ok.
- yoon2023 (8; single, capitals): call verified. KAIST School of Electrical Engineering, Daejeon, "Republic of Korea"
  -> KR; street not recorded; district Yuseong-gu in the note (D366; probe YO1 locality Yuseong-gu 0 errors, the
  checker cannot tell, the city is right). ok.
- yi2015 (5; single, capitals): Caltech T. J. Watson Laboratory, Pasadena, US; KERRY VAHALA vs list Kerry J. Vahala
  (dropped middle initial, matched by name). ok.
- liang2021 (7; single): Hewlett Packard Labs printed before Hewlett Packard Enterprise -> org HPE + unit Hewlett
  Packard Labs, Milpitas, US: the exact committed form (2 committed blocks). Probe LI1 (HP Labs org + HPE more_orgs)
  0 errors, +7 rows: not the precedent. List forms Géza Kurczveil / Raymond G. Beausoleil matched. ok.
- herr2012 (8; printed, slots from header): call verified. Header order = YAML (probe HR2 swapped: 2 errors). Markers
  1 / 1 / 2 / 3 / 1 / 3 / 4 / 1,2 in both layers (HR3 Wang on 3: 2 errors; HR1 Kippenberg without 2: 0 errors, last-
  author gap O1). EPFL, Lausanne, CH; Max-Planck-Institut für Quantenoptik (intended umlaut, D282), Garching, DE; Menlo
  Systems GmbH, Martinsried, DE; Moscow State University Faculty of Physics (printed before the org), Moscow, RU;
  postal codes not recorded. The asterisk legend is a contact line; "corresponding author" in the note is the usual
  reading. ok.
- ye2023a (11; printed, capitals): calls verified. China University of Geosciences School of Automation, Wuhan, CN;
  Hubei key laboratory as its own org (no parent printed; registry id exists); the Engineering Research Center keeps
  ", Ministry of Education" in the org name: the registry id is the ministry form (probe YE2 without it: 0 errors,
  +1 unmapped string), committed lit_h27 / two Tianjin clause blocks keep the ministry; lit_h08 liu2022a recorded the
  same centre without it (O3). Block 4 HUST with the "Wuhan National Laboratory for Optoelectronics and School of
  Optical and Electronic Information" unit chain: the exact committed string (10 committed blocks; 34 committed HUST
  unit-chain blocks vs 4 WNLO-as-org blocks); probe YE1 (WNLO org + HUST more_orgs) 0 errors, +4 rows, the minority
  form. Weilun Zhang 1,2,3,4 (YE3 without 4: 2 errors). ok.
- xiang2022a (10; printed, capitals): calls verified. Markers: Xiang 1,5,*; Zhang 1,5; Lu 1,6; Guo 1,7: 5 is the
  equal-contribution line, 6 and 7 lead contact lines (dropped with those reasons). Probes XG1 / XG2 (dropped 5 / 6
  removed) 2 errors each; XG3 (Guo without 7) 0 errors, last-author gap (O1), 1,7 read in both layers. HUST with the
  "&" WNLO + school chain (8 committed blocks of this exact string), Wuhan, CN; Ori-chip optoelectronics technology LTD
  as printed, Ningbo, CN; Zhejiang University college, Hangzhou, CN; Trinity College with the group, school, CRANN and
  CONNECT chain printed before it, Dublin, "Ireland" -> IE (XG4 chain cut after the school: 2 errors, the whole chain
  is required). Can Liu 2,3 (XG5: 3 errors). List form John Francis Donegan matched. Streets and postal codes not
  recorded. ok.
- ashtiani2019 (2; single, capitals): University of Pennsylvania ESE, Philadelphia, US. ok.
- ito2019 (8; single): call verified. Yokohama National University ECE, Yokohama, JP; the neighbourhood with block
  number before the ward is not recorded and not named; the ward Hodogayaku is named in the note as printed (D366;
  IT1 locality Hodogayaku 0 errors, neutral). ok.
- li2019a (5; single, capitals): Shanghai Jiao Tong University with the state key laboratory + department chain,
  Shanghai, CN. ok.
- mehta2020 (6; single, preprint): call verified. The block prints "ETH Zürich, Switzerland" (text layer "Z¨urich",
  intended letters "Zürich", D282; probe ME2 "ETH Zurich" 0 errors, neutral) after the department + institute unit
  joined by "&"; no city outside the org name, so locality "" (committed rule "no city apart from the organization
  name -> locality empty", h72 S15 / BK1; probe ME1 Zürich 0 errors, known gap O4), country CH. List forms Thanh Long
  Nguyen / M. Stadler / Jonathan Home matched by name. ok.
- skipper2025 (7; printed, capitals): call verified. Blocks 1-3 "University of California Santa Barbara" without a
  comma -> org + campus (D301, D461 committed form; SK1 whole string 0 errors, neutral) with IEE / ECE / Materials
  units, Santa Barbara, US; RF SUNY Polytechnic Institute as printed (2 committed blocks of this string), Albany, US.
  Probe SK2 (Koscica on 2) 2 errors. List forms David L. Harame / John Edward Bowers matched. ok.
- wang2021c (6; printed, capitals): SIMIT with "Chinese Academy of Sciences" in the institute name (13 committed
  blocks of this string) and the state key laboratory unit, Shanghai, CN; University of Chinese Academy of Sciences,
  Beijing, CN. Probe WA1 (Jia on 1,2) 2 errors. ok.

## Extractor calls (verified)

1. kim2005 and herr2012 slots from the printed header: both have `n_authors_meta` 0 and print the D352 line; YAML in
   printed order (KM1 / HR2 swaps fail). Confirmed.
2. xue2015 explicit slot 7 for Dan E. Leaird vs list Daniel E. Leaird: required (X1) and allowed (D287 short given
   name, initials agree). Confirmed.
3. park2007a campus between University of California and the department, unit left out: PK1 fails, PK2 passes only by
   breaking D301; committed precedent drops the department. Confirmed.
4. Contact / equal-contribution markers dropped (fan2017 3-4, dong2025 6-7, xiang2022a 5-7): the leading characters
   of the masked contact lines and the printed equal-contribution line agree. Confirmed (last-author drops verified by
   reading, O1).
5. mehta2020 "ETH Zürich, Switzerland" with empty locality: confirmed (the brief's "Zurich" spelling is the folded
   form; the record keeps the printed umlaut).
6. Wuhan National Laboratory for Optoelectronics as a unit chain of HUST (ye2023a block 4, xiang2022a block 1): the
   dominant committed form, exact strings committed. Confirmed.
7. ye2023a Ministry of Education centre keeps the ministry in the org name: matches the registry id. Confirmed (O3).
8. ito2019 ward and yoon2023 district named in notes: D366; no street or neighbourhood named. Confirmed.

## Fixes (exact YAML edits)

None required. No slot, marker, block field, role, locator or note is wrong or imprecise.

## Observations (no YAML change)

- O1 Checker gap: the last author's marker run is checked only as a prefix (`_author_marks`, `exact=False`), so a
  missing `dropped_markers` entry or a missing trailing marker on the last author passes (FN2, DG2, XG3, HR1). The
  four last-author runs of this batch (Hu 1,4; Bowers 1,4,7; Guo 1,7; Kippenberg 1,2) were verified by reading both
  layers.
- O2 Checker gap: a country printed in the block but recorded as "" passes (ME3); the recorded countries were checked
  by reading.
- O3 Org round: the Engineering Research Center of Intelligent Technology for Geo-Exploration is recorded with the
  ministry here (registry id form) and without it in lit_h08 liu2022a (unmapped there); an alias for the short form
  would unify both.
- O4 Known gaps reconfirmed: city inside the org name accepted as locality (ME1); district / ward accepted as locality
  (YO1, IT1); second printed city form accepted (KI1); campus removal accepted (SK1, PK2); acronym removal accepted
  (RI1).

## Lists for the coordinator

- D412 list: none.
- D426 review list: xue2015 #7 (Dan E. Leaird / Daniel E. Leaird, explicit slot).
- Re-record list: none.
- Org round (8 unmapped strings): Kwangwoon University; Max-Planck-Institut für Quantenoptik; Moscow State University;
  Ori-chip optoelectronics technology LTD; RF SUNY Polytechnic Institute; Shanghai Institute of Microsystem and
  Information Technology, Chinese Academy of Sciences; Trinity College (unit chain names CRANN and CONNECT); Université
  de Neuchâtel.

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 1 warning, 199 rows, 8 unmapped; derived files identical | batch as written |
| X1 / XU1 | xue2015 slot 7 removed / Xuan without 2 | 2 / 2 errors | slot required / markers verified |
| PK1 / PK2 | park2007a dept on the campus form / whole campus string + dept | 2 / 0 errors | not contiguous / D301 forbids |
| FN1 / FN2 | fan2017 Gu without dropped 3 / Hu without dropped 4 | 2 / 0 errors | verified / last-author gap O1 |
| DG1 / DG2 / DG3 | dong2025 Wan without 6 / Bowers without 7 / Dong without 3 | 2 / 0 / 3 errors | verified / O1 / verified |
| XG1 / XG2 / XG3 | xiang2022a dropped 5 / 6 / 7 removed | 2 / 2 / 0 errors | verified / verified / O1 |
| XG4 / XG5 | Trinity chain cut after the school / Can Liu without 3 | 2 / 3 errors | whole chain required / verified |
| ME1 / ME2 / ME3 | mehta2020 locality Zürich / org ETH Zurich / country "" | 0 / 0 / 0 errors | O4 / neutral / O2 |
| KM1 / KM2 | kim2005 authors swapped / chain cut after the college | 2 / 2 errors | order and chain verified |
| HR1 / HR2 / HR3 | herr2012 Kippenberg without 2 / authors swapped / Wang on 3 | 0 / 2 / 2 errors | O1 / verified / verified |
| YE1 / YE2 / YE3 | ye2023a WNLO as org / centre without ministry / Zhang without 4 | 0 (+4 rows) / 0 (+1 unmapped) / 2 errors | minority form / registry form kept / verified |
| KI1 / YO1 / IT1 | Busan / Yuseong-gu / Hodogayaku as locality | 0 / 0 / 0 errors | O4 |
| SK1 / SK2 | skipper2025 whole UCSB string / Koscica on 2 | 0 / 2 errors | neutral / verified |
| LI1 / RI1 | liang2021 HP Labs org + HPE more_orgs / EPFL acronyms removed | 0 (+7 rows) / 0 errors | not precedent / neutral |
| HA1 / ZH1 / WA1 / WO1 | marker variants | 3 / 3 / 2 / 2 errors | verified |
