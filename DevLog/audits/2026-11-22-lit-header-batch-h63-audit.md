---
title: Fresh-context audit of the lit author-affiliation batch lit_h63 (27 papers)
date: 2026-11-22
mode: read-only on the batch (wrote only this record and scratchpad show dumps / crops / probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only with --dry-run on the batch, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h63/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D282, D286f, D287, D301, D366, D369, D412, D426, D522 / D572, D686, D699, D711); format from the lit_h62 audit
verdict: GO with F1 (menna2001 note: wrong reason for the unrecorded asterisk block) and F2 (menna2001 unmarked block basis single -> layout, D286f; 4 rows grade A -> B); 162 slots audited, 156 recorded, 6 without rows (all confirmed), 0 wrong rows, 4 imprecise rows (F2); all named extractor calls confirmed; optional N1 (deng2016 note wording)
---

# Lit header batch audit: lit_h63 (2026-11-22)

## Scope

Batch lit_h63: 27 papers (IEEE PTL / JSTQE prose footnotes, Optics Express printed / single / grouped blocks, five
conference-paper scans with OCR text, one 1990 scan without a text layer); 162 slots, 14 papers `slots_from_header`;
201 rows. Restricted corpus: this record names only authors, orgs, units, cities, districts and countries; no paper
text is quoted and no contact, street, building, campus site, park, postal or box text is copied (such spans are
named by type only).

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h63 --corpus lit --codes <id> --pdf`
  (all 27); output kept in the session scratchpad `h63_audit/show/` only.
- Page renders viewed for the scans: menna2002, menna2001, sugg2002 (header crops of `img_p01_1.png`), mathur2002,
  chen2002, okai1990 (whole `img_p01_1.png`, downscaled); crops in the scratchpad `h63_audit/img/` only.
- Per slot: printed name vs the `show` author list (or the header for the 14 header-slot papers) and `compare.csv`;
  marker run in both layers; prose statement subjects; block fields (org, unit chain, more_orgs, campus, city,
  country); basis; locator; notes.
- All 201 rows of `header_rows.csv` read by paper (roles primary 187, additional 14; basis printed 97, prose 51,
  single 39, grouped 8, layout 6; grade A 195, B 6). `compare.csv`: 156 `recorded`, 6 `no_header`.
- Address / contact scan of `headers.yaml` and the derived CSVs (contact, URL, 4+ digit, 5-digit, street, avenue,
  road, route, drive, suite, building, campus, box, cedex, ward, park patterns, plus every street, campus, park,
  ward and site token printed in this batch's blocks). Hits: years in `source_id` values, "Lightwave", and the type
  words "street address", "campus site name", "technology park site name", "science park site name", "ward", "web
  address", "contact line", "phone, fax" in notes. No contact, URL, postal code, street, ward, building, campus-site,
  park or box text anywhere (derived CSVs included); the word e-mail appears in no note.
- Probes on scratch copies (`h63_audit/probes/probe.py`, scratch `LIT_BASE`, batch name `lit_p63`,
  `cmd_check(..., dry_run=True)`; 29 runs). Dry-run check of the real batch: 0 errors, 1 warning (ahn2007 explicit
  slot 9); totals equal the stamped derived files (162 slots, 156 recorded, 201 rows, 22 unmapped org strings).
  md5 of every repo batch file identical before and after the audit; `check_stamp.txt` matches `headers.yaml`
  (sha256 44970c38...). Probe checks wrote their usual logs under `logs/` (prefix `lit_headers_check_lit_p63`).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h63 | 27 / 27 | 162 | 158 | 4 (menna2001 #1, #2, #6, #7: basis, F2) | 0 |

- Papers ok 22, partial 2 (menna2002, menna2001), unreadable 3 (sugg2002, mathur2002, okai1990); all five calls
  confirmed. `slots_from_header` 14 (exactly the papers.csv rows with `n_authors_meta` 0; each prints the D352 line);
  the three unreadable papers have 0 slots (16 printed authors appear in no compare row, lit_h61 kim2004 precedent).
- Slots without rows 6: menna2002 #4, #5; menna2001 #3, #4, #5 (unreadable); ahn2007 list slot 1 (printed author is
  slot 0). `author_list_differs` 1 (ahn2007); explicit slots 2 (ahn2007 #1 slot 0, #9 slot 9); order warnings 0;
  present addresses 0; 22 unmapped org strings.
- Per paper (slots / rows): nishi2017 4 / 4; tadokoro2009 6 / 6; oishi1997 3 / 3; menna2002 8 / 6; sato2007 6 / 6;
  faugeron2011 9 / 10; sato2008a 7 / 7; chen2002 6 / 6; menna2001 7 / 4; faugeron2012 9 / 10; sugg2002 0 / 0;
  mitsuhara1999 5 / 5; mathur2002 0 / 0; okai1990 0 / 0; chung2019a 3 / 3; fujisawa2017 4 / 4; deng2016 6 / 6;
  novack2013 11 / 15; hadijelhouati2019 7 / 9; virot2017 15 / 47; chen2016d 4 / 4; zhang2014b 11 / 16;
  rosa2016 5 / 5; ahn2007 9 / 8; priyadarshini2024 4 / 4; yao2018 3 / 3; xu2007 10 / 10.
- Privacy findings: 0. Notes: 1 with a wrong reason (menna2001, F1), 1 loosely worded (deng2016, N1).

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (162) | 162 | 0 | 0 |
| markers (printed / prose / single / grouped / layout; 156 readable + 6 unreadable) | 162 | 0 | 0 |
| header position / statement subject | 162 | 0 | 0 |
| blocks (org / unit / more_orgs / campus / locality / country) | 162 | 0 | 0 |
| basis / grade | 158 | 4 (menna2001, F2) | 0 |
| locators | all | 0 | 0 |
| notes (27) | 25 | 1 (deng2016, N1) | 1 (menna2001 reason, F1) |

## Per-paper findings

- nishi2017 (4; prose): statement 1 (three names) QD Laser, Inc., Atsugi, JP; statement 2 (Arakawa) University of
  Tokyo, Tokyo, JP. Probes H1 (Sugawara on P2): 4 errors; N1x (P1 locality Tokyo): 2 errors. ok.
- tadokoro2009 (6; prose, slots from header): "The authors" statement, NTT Photonics Laboratories, Atsugi, JP (same org-only
  form as the committed NTT Photonics Laboratories blocks, which print other Atsugi spellings). ok.
- oishi1997 (3) / mitsuhara1999 (5) (prose, slots from header): "The authors" statement, NTT Opto-electronics
  Laboratories, "Atsugi-shi" as printed (D366), prefecture and postal code not recorded; lit_h58 has the identical block.
  ok.
- menna2002 (8; partial, slots from header): call 1. ok.
- sato2007 (6; prose, slots from header): call 6. ok.
- faugeron2011 / faugeron2012 (9 / 9; prose, slots from header): call 7. ok.
- sato2008a (7; prose, slots from header): "The authors" statement printing the laboratory before Nippon Telegraph and
  Telephone Corporation, Atsugi (prefecture after the city): org the company, unit the laboratory (committed form for
  NTT laboratories printed with the company name). ok.
- chen2002 (6; single, OCR, slots from header): render and both layers print the six names (the text layer splits
  "S . Oh"; recorded "S. Oh"), one unmarked block Ortel Corporation, then phone / fax lines, a street, Alhambra and a
  state with postal code, no country: locality Alhambra, country "" (call 10). ok.
- menna2001 (7; partial, slots from header): call 2; F1, F2.
- sugg2002, mathur2002, okai1990 (unreadable): call 3.
- chung2019a (3; single, capitals): University of Southern California, Los Angeles, US; asterisk = contact line;
  list "SungWon Chung" matches. ok.
- fujisawa2017 (4; single, capitals): unit "Graduate school of information science and technology" with the printed
  lower case, Hokkaido University, Sapporo, JP; street and ward before the city not recorded. ok.
- deng2016 (6; printed): blocks 1 / 2 and markers verified in the PDF layer (Zhou 1 plus the asterisk). List "Jürgen
  Michel" and "Zhiping James Zhou" match by name. Rows right; note wording N1.
- novack2013 (11; printed): five blocks; markers 1,2 / 3 / 4 / 4 / 1,2 / 4 / 5 / 1 / 1 / 3 / 1,2,3 in the PDF layer;
  block 1 Institute of Microelectronics (A*STAR parent and the science park site not copied, call 9); NUS ECE;
  University of Washington EE, Seattle; University of Delaware ECE, Newark; Università degli Studi Roma Tre,
  Dipartimento di Scienze, Rome, IT. ok.
- hadijelhouati2019 (7; printed, capitals): block 1 Universidad de Málaga with the department + ETSI chain, Málaga
  (campus site and postal code not recorded); block 2 Bionand, Málaga (technology park site not recorded); block 3
  National Research Council Canada, Ottawa, CA. Markers verified; "J. Gonzalo Wangüemert-Pérez" matches the list
  "Juan Gonzalo ...". ok.
- virot2017 (15; printed, capitals): call 8. ok.
- chen2016d (4; printed): call 7. ok.
- zhang2014b (11; printed): calls 7, 9. ok.
- rosa2016 (5; single): Nanophotonics Technology Center, Universitat Politècnica de València, Valencia, ES; street
  and postal code not recorded; "Ana Gutiérrez" matches "Ana Maria Gutierrez". ok.
- ahn2007 (9; grouped): call 4. ok.
- priyadarshini2024 (4; single, capitals): call 5. ok.
- yao2018 (3; single, capitals): unit chain school "and" Shandong key laboratory before Liaocheng University,
  Liaocheng, CN. ok.
- xu2007 (10; single, slots from header): NRC Canada with the Institute for Microstructural Sciences as unit, Ottawa,
  CA (lit_h62 form); street, contact and web address not recorded. ok.

## Extractor calls (verified)

1. menna2002 partial. The render prints marker (1) after Khalfin and Tsekoun; both text layers read "(l)". Lookalikes
   are not folded (OFC contract, markers): authors 4 and 5 `unreadable: true`, carrying ["1"]. Block 1 is verified
   even though only unreadable authors carry it (probe M2, locality Trenton: 2 errors; M3, block removed: 2 errors,
   markers without a block). The unmarked block (Princeton Lightwave Inc., Cranbury, US) is `layout` (D286f; M4
   `single`: 2 errors). Block 1 "Princeton Lightwave Inc. contractor from Sarnoff Corporation, Princeton, ..., USA":
   two organizations, Princeton, US, as recorded. M1 (Khalfin readable): 2 errors. Confirmed; partial is right.
2. menna2001 partial, outcome confirmed, stated reason wrong (F1), basis imprecise (F2).
   - Render (verified): Maiorov without marker, "V. Khalfin*", "L. DiMarco*"; unmarked block Princeton Lightwave,
     Inc., Cranbury, state, postal code, no country; asterisk block "Princeton Lightwave, Inc. contractors from
     Sarnoff Corporation, Princeton, NJ", no country.
   - Both text layers keep the asterisks (after both names and before the block). They read "Khalfm" and "Samoff".
     The note's reason ("the text extraction drops the bare asterisk") is wrong. Probe N2 (OCR forms "V. Khalfm" and
     "Samoff Corporation" recorded readable with block "*") fails only on the partial status: the asterisk itself
     verifies. The OCR forms are not the printed text (D282, D686 F2: an OCR-wrong readable name is not recorded),
     so N2 is not an acceptable record.
   - Probes with the printed forms: N3 (Khalfin unreadable, block with Sarnoff): 5 errors (Sarnoff not in the block;
     DiMarco's and the block's md run break after the unreadable garbled name; Maiorov). N8 (Maiorov and Khalfin
     unreadable, DiMarco readable, block without Sarnoff): 0 errors, but drops the printed employer and puts
     Sarnoff's city on Princeton Lightwave (misleading; not acceptable). N6 / N7 (block basis pdf): "basis pdf
     without a local PDF" (the lit check takes no pdf basis; the extractor is right on that point).
   - N1 (Maiorov readable): 2 errors (both layers); his run cannot be delimited before the garbled next name.
     Checker gap as the note says; unreadable is the only passing form.
   - Conclusion: DiMarco cannot be recorded with the printed block; three unreadable authors and the asterisk block
     kept in the note is right. The unmarked block, however, sits next to a printed marked block: D286f prescribes
     `layout` (grade B), as in menna2002; `single` claims a one-block paper (F2; N10: 0 errors, 4 rows grade A -> B).
3. Unreadable papers. The checker verifies against `text.md` and the PDF text layer only; a render is never a basis
   (lit_h61 kim2004, D711). Re-checked whether any could be recorded:
   - sugg2002: render prints Sugg 1, Abeles 2, Braun 2, Maiorov 1, Menna 2, DiMarco 2, Martinelli 2, Connolly 2 and
     blocks 1 Sensors Unlimited, Inc., Princeton, USA / 2 Sarnoff Corporation, Princeton, USA (matches the note).
     Both layers read the superscripts as lookalike symbols and the block markers likewise, so no author and no
     block marker verifies; a partial record would have every author unreadable and no rows. Unreadable is right.
   - mathur2002: render prints Atul Mathur, Mehrdad Ziari, Vivek Agrawal and one unmarked block SDL Inc., street, San
     Jose, state, postal code, no country (matches the note). Both layers lost the left part of the header (author 1
     and the organization), so the block cannot be verified and authors 2-3 have no recordable block. Right.
   - okai1990: text and PDF layers hold only the download stamp; the page image prints M. Okai, T. Tsuchiya, K.
     Uomi, N. Chinone, T. Harada (capitals) and one "The authors" footnote statement: Central Research Laboratory,
     Hitachi, Ltd., Tokyo, Japan (with a postal number, not in the note). Matches the note. Right.
4. ahn2007 grouped (D368). Two author groups, each printed above its own MIT block (Department of Materials Science
   and Engineering; Department of Electrical Engineering and Computer Science), Cambridge, US; streets not recorded.
   A4 (Jian Chen on G1): 2 errors. #1 printed "Donghwan Ahn", list "Dae-Hwan Ahn": A3 (no slot) 1 error (no match);
   A2 (`slot: 1`) passes with a warning, but Dong / Dae are different given-name syllables (a different name, not a
   transliteration; D287 / D369, lit_h17 kang2008 Yunlu / Yimin precedent): `slot: 0` + `author_list_differs` and
   the D412 list are right. #9 "Kärtner" / list "Käertner": A1 (no slot) 1 error; explicit slot 9 is a
   transliteration variant (D287). Confirmed.
5. priyadarshini2024: the block prints the center and department, "Indian Institute of Technology", Chennai, postal
   code, India: org without the place, campus "Chennai", locality Chennai, IN (D301; ofc_h10 precedent "Indian Institute
   of Technology" campus "Delhi"). PR1 (campus dropped): 0 errors (known gap, missing campus not detected); the row
   org string "Indian Institute of Technology, Chennai" stays unmapped until the registry has the campus (the
   committed "Indian Institute of Technology Madras" blocks print that name). Confirmed.
6. sato2007: statement 1 NTT Photonics Laboratories, NTT Corporation, then a prefecture (Kanagawa), postal code,
   Japan; statement 2 Department of Advanced Physics, Hirosaki University, then "Aomori", postal code, Japan. The
   postal code belongs to Hirosaki city, so "Aomori" names the prefecture: locality "" in both (D288; lit_h60 sato2008
   prefecture-only precedent). S1 ("Aomori") and S2 ("Hirosaki") both pass with 0 errors: neutral / checker gap
   (S2 matches the city inside the org name, O1). T1 (Watanabe on P1): 4+ errors. Confirmed.
7. Organization forms as printed:
   - faugeron2011 "III–V Laboratory", faugeron2012 "III–V Lab" (en dash as printed; lit_h44 has "III–V Laboratory",
     17 committed blocks "III-V Lab"), Palaiseau, FR; the three named parents not copied (D426; lit_h17 keyvaninia2012 and
     several committed notes). F1 probe (parents as more_orgs): 0 errors, neutral. Statement 3 prints the LMOPS full
     name, then "SUPELEC/LMOPS", Metz: org LMOPS full name, more_orgs SUPELEC (D285 joint-unit treatment). Statement
     1 Thales Air Systems, Limours, FR. Statement 2 of faugeron2012 is extracted one word per line in the text layer;
     verifies. Confirmed.
   - chen2016d block 2 "Wuhan Research Institute of Posts Telecommunications" (the "and" is missing in both layers):
     C1 (with "and"): 4 errors. Block 1 WNLO "&" school chain as unit of Huazhong University of Science and
     Technology: majority committed form (D572; committed blocks print the WNLO "&" chain with
     another school name). Confirmed.
   - zhang2014b block 6 "University of Singapore" as printed: Z1 ("National University of Singapore"): 4 errors.
     Confirmed; the org round must not map it to NUS by name alone (O3).
8. virot2017: block 1 Centre de Nanosciences et de Nanotechnologies + CNRS, Univ. Paris-Sud, Université Paris-Saclay
   (identical in lit_h24, lit_h44, lit_h48, lit_h52), Orsay, FR; the acronym-and-place span and postal designation not copied. Block 2
   University Grenoble Alpes + structured CEA / LETI, Grenoble (committed form with "Univ." / "Université"; this
   paper prints "University"); the site name not recorded. V1 (plain "CEA" + unit LETI): 0 errors, neutral. Block 3
   STMicroelectronics, Silicon Technology Development, Crolles, FR. Markers verified in the capitals PDF layer;
   "FRÉDÉRIC BOEUF" matches the list "F. Bœuf". Confirmed.
9. A*STAR parent not copied (novack2013 block 1, zhang2014b block 5): org "Institute of Microelectronics", Singapore,
   SG (committed majority form, maps to `org_astar_ime`). Confirmed.
10. No printed country -> "" (chen2002, menna2001 unmarked block): both renders print a state and postal code without
   a country. Confirmed.

## Fixes (exact YAML edits)

F1 (required, note; no row change). menna2001, line 124 `note` ->

```
  note: "no author list in the literature cache (slots from the header, D352); conference paper scan, OCR text in both layers; authors 4 and 5 carry an asterisk pointing to a second block (Princeton Lightwave, Inc. contractors from Sarnoff Corporation, Princeton, no country printed); the unmarked block holds the other authors (layout, D286f); both text layers keep the asterisks but read Sarnoff as Samoff and author 4 as Khalfm (the page render prints V. Khalfin and Sarnoff), so the asterisk block cannot be recorded as printed and authors 4 and 5 are unreadable (no rows; values here for re-recording); author 3 is readable on the page but marked unreadable: the OCR-garbled next name breaks the checker marker run (checker gap); the unmarked block prints no country; street address, state, postal code, phone, fax and contact line not recorded"
```

F2 (required, basis; 4 rows grade A -> B). menna2001, line 126 ->

```
    - {marker: "", basis: layout, org: "Princeton Lightwave, Inc.", locality: "Cranbury", country: ""}
```

Probe FIX (F1 + F2 together): 0 errors, 1 warning (ahn2007 slot 9); 162 slots, 156 recorded, 201 rows, basis layout
10 / single 35, grade A 191 / B 10. The edited file is in the session scratchpad `h63_audit/probes/FIX.yaml` (diff
against the batch = exactly these two lines). After applying, re-run `check lit_h63 --corpus lit` (the stamp hash
changes).

N1 (optional, wording; no row change). deng2016, line 212 `note` ->

```
  note: "asterisk marks the corresponding author; author 5 printed Jurgen Michel (author list Jürgen Michel), author 6 printed Zhiping Zhou (author list adds a middle name); states and postal codes not recorded"
```

No other fix: no slot, marker, block, field, locator or other note is wrong.

## Observations (no YAML change)

- O1 Locality accepted when it is printed only inside the org name (sato2007 S2 "Hirosaki" from "Hirosaki
  University": 0 errors); checker test candidate.
- O2 D286f is enforced only when the marked block is recorded (menna2002 M4 errors; menna2001 `single` passes with
  the asterisk block unrecorded); checker test candidate: a printed marked block that the YAML omits should still
  force `layout`.
- O3 Org round: "University of Singapore" (zhang2014b) and "Indian Institute of Technology, Chennai"
  (priyadarshini2024) need explicit rulings; "Wuhan Research Institute of Posts Telecommunications" is a printed
  misprint of the WRI name (alias request, not a new org).
- O4 Known gaps reconfirmed: missing campus not detected (PR1); parent / joint-lab parents accepted as more_orgs
  (faugeron F1 probe); an unreadable OCR-garbled name breaks the neighbouring marker run (menna2001 N1, N5).
- O5 `show` output (not batch files) leaves phone / fax digits of menna2002, menna2001 and chen2002 unmasked, as
  noted for bimberg2009 / kim2004 in D711.

## Lists for the coordinator

- D412 list: ahn2007 list slot 1 "Dae-Hwan Ahn" (printed Donghwan Ahn; slot 0).
- D426 review list: none new (ahn2007 #9 Kärtner / Käertner is a transliteration slot).
- Re-record list: menna2002 #4 Khalfin, #5 Tsekoun (block 1 already recorded); menna2001 #3 Maiorov (checker gap),
  #4 Khalfin, #5 DiMarco with the asterisk block (needs an OCR-correction or render basis); sugg2002, mathur2002,
  okai1990 whole headers (values in the notes).
- Org round (22 unmapped strings): Bionand Center for Nanomedicine and Biotechnology (ES); Hirosaki University (JP);
  III–V Lab and III–V Laboratory (FR); Indian Institute of Technology, Chennai (IN, O3); Laboratoire Matériaux
  Optiques Photonique et Systèmes (FR); NTT Opto-electronics Laboratories (JP); NTT Photonics Laboratories (JP);
  Ortel Corporation (no country); Princeton Lightwave Inc. (US) and Princeton Lightwave, Inc. (no country); QD
  Laser, Inc. (JP); SUPELEC (FR); Silicon Lightwave Services, LLC (US); Thales Air Systems (FR); Univ. Paris-Sud,
  Université Paris-Saclay, University Grenoble Alpes (FR); Universidad de Málaga (ES); University of Singapore (SG,
  O3); Università degli Studi Roma Tre (IT); Wuhan Research Institute of Posts Telecommunications (CN, O3).

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 1 warning, 201 rows | batch as written |
| FIX | F1 + F2 (menna2001) | 0 errors, 201 rows, grade B 10 | fix form |
| N1 | menna2001 Maiorov readable | 2 errors | checker gap confirmed |
| N2 | menna2001 OCR forms Khalfm / Samoff readable, block "*" | 1 error (status only) | asterisk verifies; OCR forms not acceptable |
| N3 / N4 / N5 | Khalfin unreadable, block "*" with Sarnoff / no second org / Samoff; Maiorov readable | 5 / 4 / 4 errors | printed block not verifiable |
| N6 / N7 | block "*" basis pdf | basis pdf without a local PDF | no pdf basis in lit |
| N8 / N9 | Maiorov + Khalfin unreadable, DiMarco readable, block without Sarnoff / with Samoff | 0 / 0 errors | pass but misleading / OCR text: rejected |
| N10 | menna2001 unmarked block layout | 0 errors | F2 form |
| M1 / M2 / M3 / M4 | menna2002 Khalfin readable / block 1 Trenton / block 1 removed / unmarked block single | 2 / 2 / 2 / 2 errors | lookalike, block verification, D286f |
| A1 / A2 / A3 / A4 | ahn2007 no slot 9 / slot 1 / no slot 0 / Chen on G1 | 1 / 0 (2 warnings) / 1 / 2 errors | slots and groups verified; A2 rejected on D287 |
| S1 / S2 / T1 | sato2007 Aomori / Hirosaki / Watanabe on P1 | 0 / 0 / 4+ errors | neutral / gap O1 / subjects verified |
| C1 / Z1 | chen2016d with "and" / zhang2014b NUS | 4 / 4 errors | as printed verified |
| PR1 / F1 / V1 | no campus / III-V parents as more_orgs / plain CEA + LETI unit | 0 / 0 / 0 errors | neutral, recorded forms kept |
| H1 / N1x | nishi2017 Sugawara on P2 / P1 Tokyo | 4 / 2 errors | subjects and place verified |
