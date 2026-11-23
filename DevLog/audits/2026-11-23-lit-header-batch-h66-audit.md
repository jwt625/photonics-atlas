---
title: Fresh-context audit of the lit author-affiliation batch lit_h66 (26 papers)
date: 2026-11-23
mode: read-only on the batch (wrote only this record and scratchpad show dumps / renders / probes; headers.yaml, derived files, scripts, people and registry data not edited; checker run only in dry-run or write-run on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h66/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D366, D369, D380, D410, D412, D416, D426, D442, D466, D599 chen2022d, D686 yang2018b; D287, D288, D301 from DevLog-008); format from the lit_h64 audit
verdict: GO; 179 slots audited, 163 recorded + 16 no_header, 0 wrong rows, 0 imprecise rows; all named extractor calls confirmed; F1 removes a redundant explicit slot (maire2008 #11) and rewords its note (no row change)
---

# Lit header batch audit: lit_h66 (2026-11-23)

## Scope

Batch lit_h66: 26 papers (Optics Express printed and single blocks, IEEE JLT / JSTQE / PTL / Photonics Journal prose
footnotes, one conference paper); 179 slots, 5 papers `slots_from_header`; 201 rows. Restricted corpus: this record
names only authors, orgs, units, cities and countries; no paper text is quoted and no contact, street, building,
site, box or postal text is copied (such spans are named by type only).

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h66 --corpus lit --codes <id> --pdf`
  (all 26); output kept in the session scratchpad `h66_audit/show/` only.
- benedikovic2016, chen2020b, watanabe2020, wang2017c, rawat2023, yu2023b: page 1 of the local PDF rendered to PNG
  (scratchpad `h66_audit/img/`); the header regions of benedikovic2016, chen2020b and watanabe2020 inspected by eye to
  see what the masked lines after the blocks carry (call 6).
- Per slot: printed name vs the `show` author list (or the header for the 5 header-slot papers) and `compare.csv`;
  marker run in both layers; prose statement subjects; block fields (org, unit chain, more_orgs, campus, city,
  country); locator; notes.
- All 201 rows of `header_rows.csv` read by paper (roles primary 184, additional 17, present address 0; basis
  printed 135, prose 29, single 37; all grade A; locators p.1 header 172, p.1 footnote 29). `compare.csv`: 163
  `recorded`, 16 `no_header` (yu2023b 5, chen2020b 5, wang2017c 6); `order_differs` false on all 179.
- IEEE download stamp: 5 papers carry the institutional download stamp line on page 1 (ma2017, zhang2020b, yang2011,
  yu2023b, zheng2013). No block in the batch is taken from it; the only Stanford University block is su2018 block 1,
  printed in the Optics Express header (no stamp on that paper).
- Address / contact scan of `headers.yaml` and every derived file (contact sign, URL, 3+ digit numbers, street, road,
  rue, avenue, drive, suite, building, Bldg, Bat., room, box, campus, cedex, UMR, every street, site and building token
  printed in this batch's blocks). Hits: years in the file comment, "DevLog-011", and type words in notes ("street
  address(es)", "postal code(s)", "building number", "campus box number", "campus name", "UMR number"), the campus
  field values San Diego / Davis (D301), and the campus name in the yang2011 note (same form as the committed notes of
  lit_h01 / h10 / h33 / h42 / h44 / h45 / h46). No contact, URL, postal code, street, building, box or site-number
  text anywhere.
- Probes on scratch copies (`h66_audit/probes/probe.py` + `mk.py`, scratch `LIT_BASE`, batch name `lit_p66`,
  `cmd_check(..., dry_run=True)`, logs redirected to the scratchpad after the first run; 33 runs). Dry-run check of
  the batch as written: 0 errors, 0 warnings; totals equal the stamped derived files (179 slots, 163 recorded, 201
  rows, 16 unmapped org strings). md5 of every repo batch file identical before and after the audit;
  `check_stamp.txt` matches `headers.yaml` (sha256 d236a8e5...). The first probe run wrote its usual 2 log files under
  `logs/` (prefix `lit_headers_check_lit_p66`).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h66 | 26 / 26 | 179 | 179 | 0 | 0 |

- Papers ok 23, partial 3 (yu2023b, chen2020b, wang2017c), unreadable 0; `slots_from_header` 5 (wang2014c,
  antelius2011, cheung2014, yang2011, zheng2013; exactly the papers.csv rows with `n_authors_meta` 0, each prints the
  D352 line in `show`); `author_list_differs` 0; explicit slots 1 (maire2008 #11, redundant: F1); order warnings 0;
  present addresses 0; dropped markers 5 (benedikovic2016 #2 / #3, chen2020b #6, watanabe2020 #1 / #2); unreadable
  authors 16; 16 unmapped org strings.
- Per paper (slots / rows): ma2017 7 / 7; zhao2016a 9 / 9; yu2023b 6 / 3; zhang2020b 4 / 4; xu2021c 9 / 11;
  wang2014c 8 / 8; zhu2017a 8 / 15; ding2015 6 / 8; maire2008 12 / 22; su2018 6 / 7; mak2018 5 / 5;
  roelkens2006 3 / 3; antelius2011 3 / 3; zhou2022d 4 / 4; benedikovic2016 12 / 21; chen2020b 7 / 2;
  wang2017b 10 / 10; zou2015 6 / 6; rawat2023 5 / 5; watanabe2020 6 / 6; ruiz2021 8 / 13; xue2019 5 / 5;
  wang2017c 8 / 2; cheung2014 4 / 4; yang2011 7 / 7; zheng2013 11 / 11.
- Privacy findings: 0. Notes: 1 with an outdated detail (maire2008, F1).

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (179) | 178 | 1 (maire2008 #11 redundant explicit slot; F1, same slot) | 0 |
| markers (printed / prose / single, 163 readable + 16 unreadable) | 179 | 0 | 0 |
| header position / statement subject | 179 | 0 | 0 |
| blocks (org / unit / more_orgs / campus / locality / country) (163 recorded) | 163 | 0 | 0 |
| dropped markers (5) | 5 | 0 | 0 |
| locators | all | 0 | 0 |
| notes (26) | 25 | 1 (maire2008; F1) | 0 |

## Per-paper findings

- ma2017 (7; prose): P1 The University of British Columbia (leading article as printed; probe T1 without it: 0
  errors, neutral), Department of Electrical and Computer Engineering, Vancouver, CA; P2 Lumerical Solution Inc. (as
  printed), Vancouver, CA. Statement subjects name exactly the carriers. ok.
- zhao2016a (9; printed, capitals): block 1 Lanzhou University with the institute + MOE key laboratory + school
  chain, Lanzhou, CN (province not recorded); block 2 Northwest University with the international cooperation
  center + institute chain, Xi'an, CN (province printed as Shanxi, note). Markers in both layers. ok.
- yu2023b (6; prose, partial): call 2. ok.
- zhang2020b (4; prose): call 7. List "Bill P.-P. Kuo" matches printed Bill Ping-Piu Kuo. ok.
- xu2021c (9; printed, capitals): two Shanghai Jiao Tong University blocks (Department of Electronic Engineering;
  Center for Advanced Electronic Materials and Devices), Shanghai, CN; Xu and Li on 1, 2. ok.
- wang2014c (8; printed, slots from header): calls 3 and 5. Block 1 University of British Columbia (no article
  printed here), Vancouver, CA; block 3 University of Washington, Department of Electrical Engineering, Seattle, US
  (box number, state and postal code not recorded). ok.
- zhu2017a (8; printed, capitals): call 4. Block 1 Ghent University, Photonics Research Group, Department of
  Information Technology (INTEC); block 3 Physics and Chemistry of Nanostructures (street and postal codes not
  recorded); block 4 Eindhoven University of Technology, Institute for Photonic Integration (IPI), Eindhoven, NL
  (country split across a line, both layers pass). ok.
- ding2015 (6; printed): call 7. Block 1 Technical University of Denmark, unit DTU Fotonik + department, locality
  Kgs. Lyngby as printed (committed blocks use both Lyngby and Kgs. Lyngby; probe D2: 0 errors, neutral); block 3 NTT
  Corporation, NTT Network Innovation Laboratories, Yokosuka, JP (prefecture in the note). ok.
- maire2008 (12; printed, dash markers): calls 4 and 7. Block 2 Multitel a.s.b.l., Applied Photonics Departement (as
  printed), Mons, BE; block 3 Universidad Politécnica de Valencia, Nanophotonics Technology Center, Valencia, ES;
  block 4 KTH – Royal Institute of Technology (en dash as printed), Microsystem Technology Laboratory + School of
  Electrical Engineering, Stockholm, SE. Street, building, postal text not recorded. Rows right; F1.
- su2018 (6; printed, capitals): Stanford University, Ginzton Laboratory, Stanford, US; KU Leuven, Department of
  Physics, Leuven, BE (street and postal code not recorded); Vercruysse on 1, 2; list form "Jelena Vuckovic A"
  (D412) matched by name. ok.
- mak2018 (5; printed, capitals): University of Toronto, Department of Electrical and Computer Engineering, Toronto,
  CA; CEA-Leti, Grenoble, FR (printed hyphenated form; committed blocks also use org "CEA-Leti"). List "S. Olivier"
  matches. ok.
- roelkens2006 (3; single): Ghent University – IMEC kept as printed (D416 (5) / D426), Photonics Research Group,
  Ghent, BE. ok.
- antelius2011 (3; single, slots from header): call 3. KTH - Royal Institute of Technology (hyphen as printed),
  same unit chain as maire2008 block 4, Stockholm, SE. ok.
- zhou2022d (4; prose): "The authors" statement, Jilin University, College of Electronic Science and Engineering,
  Changchun, CN. ok.
- benedikovic2016 (12; printed): calls 6 and 7. Block 2 National Research Council Canada, unit Information and
  Communication Technologies, Ottawa, CA (street, province, postal code not recorded); block 3 Universidad de Málaga,
  unit "Dpto. de Ingeniería Comunicaciones, ETSI Telecomunicación", Málaga, ES; block 4 University of Žilina,
  faculty + department chain printed after the org, Žilina, SK. List "J. Lapointe" matches Jean Lapointe. ok.
- chen2020b (7; printed, capitals, initials; partial): calls 1 and 6. ok.
- wang2017b (10; single, capitals): McGill University, Department of Electrical and Computer Engineering, Montreal,
  CA. List "Md. Ghulam Saber" and "Eslam A. El-Fiky" match. ok.
- zou2015 (6; printed): block 1 Huazhong University of Science and Technology with the Wuhan National Laboratory
  for Optoelectronics + school chain (lit_h21 sun2025 / D442 form), Wuhan, CN; block 2 Huawei Technologies Co. Ltd.,
  Transmission Technology Research Department, Shenzhen, CN. ok.
- rawat2023 (5; single, capitals): call 7. ok.
- watanabe2020 (6; printed, capitals): call 6. ETH Zurich, unit "Institute of Electromagnetics Fields (IEF)" as
  printed, Zurich, CH (street and postal code not recorded). List "T. Watanabe" and "Yuriy Myronovych Fedoryshyn"
  match. ok.
- ruiz2021 (8; printed, capitals): three University of Campinas blocks (Photonics Research Center; School of
  Electrical and Computer Engineering; the Physics Institute with its quoted name as printed), Campinas, BR; block 4
  Corning Research & Development Corporation, Corning, US (street, state and postal code not recorded); block 5 State
  University of São Paulo, Center for Advanced and Sustainable Technologies, São João da Boa Vista, BR. Kocabaş
  printed with detached cedillas in both layers (D282). ok.
- xue2019 (5; single, capitals): Huazhong University of Science and Technology with the same unit chain as zou2015,
  Wuhan, CN. ok.
- wang2017c (8; printed, capitals; partial): calls 1 and 6. ok.
- cheung2014 (4; prose, slots from header): calls 3, 5 and 7. ok.
- yang2011 (7; prose, slots from header): call 3. "The authors" statement, Zhejiang University with the centre +
  state key laboratory chain, Hangzhou, CN; the campus name printed between the university and the postal code is
  not recorded (committed form). ok.
- zheng2013 (11; single, slots from header): call 3. Oracle Labs, San Diego, US (state and postal code not
  recorded; committed lit form). ok.

## Extractor calls (verified)

1. chen2020b / wang2017c partial (G6). Both print the same two problem blocks: block 1 (South China Normal
   University) prints a building number between the unit chain and the university (and a site name after it); block
   3 (Zhejiang University) prints a building number and a campus name between the unit chain and the university.
   Block 2 (Sun Yat-sen University) is clean. Probe C1 (chen2020b block 1 recorded with org + full unit chain, no
   skip): 2 errors (unit and org not contiguous). Probe C2 (same, with the printed building span as `skip_between`):
   0 errors, i.e. the checker would accept it, but that stores a building number in `headers.yaml` (contract D244:
   no building number in any field; D410's placeholder exists only for postal boxes), so it is not an allowed form
   (see O2). Leaving the blocks unrecorded is the committed handling (lit_h43 chen2022d, lit_h58 yang2018b, D426 G6).
   Unreadable sets verified from the printed marker runs: chen2020b 1, 2, 3, 6, 7 (each carries 1 or 3);
   wang2017c 1, 2, 3, 4, 7, 8. wang2017c #3 Yuntao Zhu (printed 1, 2) keeps marker 2 while unreadable (chen2022d
   form); probe W2 (markers []): 0 errors, neutral; probe W1 (readable with ["2"]): 2 errors (marker run). Probe C4
   (chen2020b L. Liu readable with 1, 3): 3 errors. Confirmed.
2. yu2023b partial. Statements 1 and 2 print their subject names without word spaces in both the text and the PDF
   layer (statement 1: authors 1, 3, 4, 5; statement 2: author 2); statement 3 (Daoxin Dai) is spaced. Probes Y1 /
   Y2 (Laiwen Yu / Jingshu Guo readable): 2 / 4 errors (not named in the subject, D354). The unreadable authors carry
   their prose markers (D366 (8)); Jingshu Guo P2 + clause P3. Daoxin Dai: P4 (Hangzhou unit chain), clause P5
   (Jiaxing key laboratory + research center + Jiaxing Research Institute, Zhejiang University, Jiaxing) and clause
   P6 (Ningbo Research Institute, Zhejiang University, Ningbo; committed form). Two statements naming the same
   Hangzhou block are two blocks (P1, P2; D354). Membership designation printed after Dai. Confirmed.
3. slots_from_header: wang2014c, antelius2011, cheung2014, yang2011, zheng2013 are exactly the papers.csv rows
   with `n_authors_meta` 0, and `show` prints the D352 line for each. Header order taken as printed; cheung2014
   statement subjects in initials (S. J. B. Yoo) resolve to the printed author line. Probe S1 (flag removed from
   wang2014c): 1 error. Confirmed.
4. maire2008 #11 / zhu2017a block 2:
   - Printed Hans Sohlström, list Hans B. Sohlstrom. The checker already matches this pair by name (dropped middle
     initial, accent folded): probe M1 (explicit slot removed) gives 0 errors, 0 warnings, and the fix-applied
     write-run produces byte-identical `header_rows.csv`, `compare.csv` and `unmapped_orgs.csv` (slot 11 = Hans B.
     Sohlstrom). The explicit slot is redundant (h49 F2 / F3 precedent: redundant explicit slots removed); the
     match itself is right. Probe M3 (YAML name with the middle initial): 4 errors (not printed). F1.
   - zhu2017a block 2 prints the university name with a transposed-letter misprint; kept as printed (D699 misprints
     kept as printed). Probe Z1 (corrected spelling): 4 errors. The 7 rows go unmapped until an alias exists (org
     round). Confirmed.
5. Empty locality:
   - wang2014c block 2: Université Laval with only the province abbreviation and the country printed; locality ""
     (D288). Probe L1 (locality Quebec): 2 errors (not printed). Confirmed.
   - cheung2014 P2: the Aidi Corporation (leading article as printed, matcher normalizes; probe K2 without it: 0
     errors, neutral), followed by a postal code and Ibaraki, Japan. Ibaraki here is the prefecture (the same author's lab block in
     lit_h64 zhang2019g prints Tsukuba as the city), so locality "" (D288). Probe K1
     (locality Ibaraki): 0 errors (checker cannot tell a prefecture from a city; known gap class K1). Confirmed.
6. Contact-footnote markers. The renders show each dropped marker printed directly in front of a contact line with no
   organization or place: benedikovic2016 markers 5 and 6 (first and second contact lines; the asterisk on the
   third), chen2020b marker 4 (first contact line; asterisk on the second), watanabe2020 markers 2 and 3 (second and
   third lines under the single block). `dropped_markers` with reason "contact footnote" is right. Probes B1 / B2 /
   W3 / W4 (dropped marker removed): 2 errors each. chen2020b #6 P. Chen carries the dropped 4 while unreadable;
   neutral. Confirmed.
7. Multi-org, campus and single-block forms:
   - maire2008 block 1 and benedikovic2016 block 1: Institut d'Electronique Fondamentale as org with the printed
     partners as `more_orgs` (maire2008: CNRS, Université Paris-Sud 11; benedikovic2016: Université Paris Sud, CNRS,
     Université Paris-Saclay, in printed order); UMR numbers and the building number not recorded; locality ORSAY /
     Orsay as printed, Cedex dropped (D366 (9)). Same form as the committed IEF blocks (virot2014, D466). Probes M2 /
     B3 (one more_org dropped): 0 errors (known gap: missing more_orgs not detected). Confirmed.
   - ding2015 block 2: FOTON Laboratory as org, CNRS and University of Rennes 1 as `more_orgs`, the school between
     them dropped (D288 rule for a department between a joint unit and a second org; D285); the identical block is
     already committed in this form. Probe D1 (school added as more_org): 0 errors, +1 unmapped, neutral; the rule
     drops it. Confirmed.
   - zhang2020b: both statements print University of California, San Diego, then La Jolla: `campus: "San Diego"`,
     locality La Jolla (committed blocks in lit_h01 / h10 / h18 / h54 / h58 in this form). cheung2014 P1: University of California, Davis ->
     `campus: "Davis"`, locality Davis. Probes U1 / U2 (campus removed): 0 errors, +2 / +1 unmapped (known gap; the
     campus is required for the mapping). Probe U3 (zhang2020b locality San Diego): 0 errors (the campus word satisfies
     the check), La Jolla is the printed city. Confirmed.
   - rawat2023: the page-1 header is clean in both layers; one unmarked block, Indian Institute of Science, Center
     for Nano Science and Engineering, Bangalore, IN; daggers = equal contribution (symbol marks, no entry needed);
     the group web link under the block not recorded. Probe R1 (locality Bengaluru): 2 errors. Confirmed.

## Fixes (exact YAML edits)

F1 (precision; no row change; maire2008, lines 136 and 153). Remove the redundant explicit slot and update the note.
Line 153, replace

```
    - {name: "Hans Sohlström", markers: ["4"], slot: 11}
```

with

```
    - {name: "Hans Sohlström", markers: ["4"]}
```

In the line 136 `note`, replace

```
author 11 printed as Hans Sohlström, author list Hans B. Sohlstrom (distinctive family name, missing middle initial: slot set, D369 / D287)
```

with

```
author 11 printed as Hans Sohlström, author list Hans B. Sohlstrom (missing middle initial: matched by name, no explicit slot)
```

Probe F (F1 applied): 0 errors, 0 warnings, 201 rows, 16 unmapped; scratch write-run derived files byte-identical to
the stamped ones (scratchpad `h66_audit/probes/F.yaml`). After applying, re-run
`uv run python scripts/ofc_headers.py check lit_h66 --corpus lit` (the stamp hash changes).

No other fix: no slot, marker, block, field, locator or other note is wrong.

## Observations (no YAML change)

- O1 Checker gap, prose clauses: dropping Daoxin Dai's last "and also with" clause (P6, probe Y3) or Jingshu Guo's
  clause (P3, probe Y4) gives 0 errors, although D366 (2) makes an unrecorded clause of an author-naming statement a
  coverage error. The batch records every clause.
- O2 Checker gap, privacy scan: the room / building pattern requires a digit right after the building word, so a
  "building word + No. + number" span is not caught; probe C2 stored such a span in `skip_between` and passed with 0
  errors. Suggest widening the pattern (optional "No." between the word and the number) with a test; until then the
  G6 handling (block not recorded) is the only allowed form.
- O3 Checker gap, IEEE download stamp: the stamp line sits inside the page-1 search window. Probe A2 (zheng2013
  single block replaced by "Stanford University" with no place) passes with 0 errors; probe A1 (with US) fails only
  on the country. Suggest stripping the stamp line in `show` / `check` the way contacts are masked. No block in this
  batch comes from it.
- O4 Known gaps reconfirmed: missing `campus` (U1, U2), missing `more_orgs` (M2, B3), prefecture accepted as
  locality (K1), campus word accepted as locality (U3).
- O5 The yu2023b note's "lit_h21 form" is inherited from the committed lit_h43 chen2022d note; it refers to the
  D442 unit-chain form (lit_h21 sun2025), not to the lit_h21 Jiaxing block, which is recorded as a two-word org.
  Wording left as is (same as the committed note).

## Lists for the coordinator

- D412 list: yu2023b "Daoxin Dai A", su2018 "Jelena Vuckovic A" (known forms, matched by name).
- D426 review list: none.
- Re-record list: chen2020b blocks 1 and 3 (authors 1, 2, 3, 6, 7) and wang2017c blocks 1 and 3 (authors 1, 2, 3, 4,
  7, 8) once a verified building-number skip exists (G6, O2); yu2023b authors 1-5 once glued statement subjects are
  handled (zhuang2025 / psaila2024 type, D449).
- Org round (16 unmapped strings): FOTON Laboratory (FR); Ghent University misprint, block 2 of zhu2017a (BE, alias
  to Ghent University); Indian Institute of Science (IN); Institut d'Electronique Fondamentale (FR, curly apostrophe
  form); Lumerical Solution Inc. (CA); Multitel a.s.b.l. (BE); Northwest University (CN); Oracle Labs (US); State
  University of São Paulo (BR); Universidad de Málaga (ES); University of Rennes 1 (FR); University of Žilina (SK);
  Université Paris Sud (FR); Université Paris-Saclay (FR); Université Paris-Sud 11 (FR); the Aidi Corporation (JP).
  Mapped but campus-qualified: University of California, San Diego; University of California, Davis.

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 0 warnings, 201 rows | batch as written |
| F | F1 | 0 errors, 201 rows, derived files identical | fix form |
| Y1 / Y2 | yu2023b Yu / Guo readable | 2 / 4 errors | glued subjects verified |
| Y3 / Y4 | yu2023b P6 / P3 clause dropped | 0 / 0 errors | checker gap (O1) |
| C1 / C2 | chen2020b block 1 recorded without / with building skip | 2 / 0 errors | G6 verified; C2 forbidden form (O2) |
| C4 | chen2020b L. Liu readable | 3 errors | unreadable verified |
| W1 / W2 | wang2017c Zhu readable / markers [] | 2 / 0 errors | marker run verified / neutral |
| M1 / M3 | maire2008 slot removed / name with middle initial | 0 / 4 errors | slot redundant (F1) / as printed verified |
| M2 / B3 | IEF block one more_org dropped (maire2008 / benedikovic2016) | 0 / 0 errors | known gap |
| Z1 | zhu2017a corrected spelling | 4 errors | misprint as printed verified |
| L1 | wang2014c locality Quebec | 2 errors | empty locality verified |
| K1 / K2 | cheung2014 locality Ibaraki / org without article | 0 / 0 errors | known gap / neutral |
| U1 / U2 / U3 | campus removed (zhang2020b / cheung2014) / locality San Diego | 0 / 0 / 0 errors | known gaps; D301 forms kept |
| B1 / B2 / W3 / W4 | contact markers removed | 2 errors each | contact markers verified |
| D1 / D2 | ding2015 school as more_org / locality Lyngby | 0 / 0 errors | neutral |
| S1 | wang2014c slots_from_header removed | 1 error | flag required |
| R1 | rawat2023 locality Bengaluru | 2 errors | as printed verified |
| A1 / A2 | zheng2013 block from the download stamp, with / without US | 2 / 0 errors | stamp inside the window (O3) |
| T1 | ma2017 org without leading article | 0 errors | neutral |
