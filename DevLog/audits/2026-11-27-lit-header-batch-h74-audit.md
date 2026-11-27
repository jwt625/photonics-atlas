---
title: Fresh-context audit of the lit author-affiliation batch lit_h74 (23 papers)
date: 2026-11-27
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; checker run only in dry-run or write-run on scratch copies with logs in the scratchpad; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h74/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D352, D366, D368, D369, D412, D416, D426, D442 and earlier lit rulings; D249, D285, D287, D288, D301, D302 from DevLog-008; format from the lit_h72 audit
verdict: GO with F1 (note wording only, no row change); 178 slots audited, 169 recorded + 9 no_header (shastri2021 #1-#7 unreadable, trocha2018 #3 D287 slot 0, wang2019a #3 not printed; all correct); 0 wrong rows; 0 imprecise rows; 1 imprecise note (bogaerts2020); every named extractor call confirmed
---

# Lit header batch audit: lit_h74 (2026-11-27)

## Scope

Batch lit_h74: 23 papers (Optica / Optics Express / Optics Letters-style numbered blocks for 13, arXiv or preprint
headers for 7, one IEEE-conference-style per-author header (moss2013), one Nature submitted manuscript with page-1
footnote blocks (bogaerts2020), one unreadable preprint (shastri2021)); 178 slots, 5 papers `slots_from_header`
(xiao2008, xu2013, seidler2013, nozaki2013, singh2015); 196 rows. Restricted corpus: this record names only authors,
orgs, units, cities and countries; no paper text is quoted and no contact, street, building, box or postal text is
copied (such spans are named by type only).

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h74 --corpus lit --codes <id> --pdf`
  (all 23); output kept in the session scratchpad `h74_audit/show/` only. `show` wrote no log under `logs/` (file
  count 15489 before and after). For wang2019a and trocha2018 the equal-contribution footnotes were checked in
  `text.md` (wang2019a prints them on its last page; trocha2018 on page 1).
- Per slot: printed name vs the `show` author list (or the header order for the 5 header-slot papers) and
  `compare.csv`; markers in both layers; block fields (org, unit chain, more_orgs, campus, city, country); role;
  locator; notes. Committed lit batches grepped for each form question (Current address cue, glued letter markers /
  gatkine2022, University of Colorado / Massachusetts campus forms, WNLO unit forms, Zijingang, Kowloon / HK,
  Université de Lyon + INL, postal box wording, NTT / IBM Zurich / Ghent-IMEC / LioniX / INRS-EMT / Carl Zeiss forms).
- All 196 rows of `header_rows.csv` read by paper: roles primary 172, additional 23, present address 1 (trocha2018
  #9 Carl Zeiss AG); basis printed 162, single 30, per_author 4; all grade A; locators p.1 header 184, p.1 footnote 12
  (bogaerts2020). `compare.csv`: 169 `recorded`, 9 `no_header`; `order_differs` true only on trocha2018 (13) and
  moss2013 (4).
- Address / contact scan of `headers.yaml` and every derived file (contact sign, URL, 3+-digit numbers, street, road,
  avenue, drive, boulevard, mall, lane, suite, building, room, hall, box, P.O., cedex, mail, phone, fax, postal, and
  every street, district and postal-code token printed in this batch's blocks, searched by its printed spelling and
  not repeated here). Hits: the file comment
  ("DevLog-011", "2026"); paper-id years; decision ids in notes; type words in notes ("street address(es)",
  "postal code(s)", "a postal box" (corpus wording, lit_h45 F1), "district", "prefecture", "province", "state(s)",
  "a web address line", "a campus site name"); org names (University of Colorado, University of California,
  University of Massachusetts); locality Varennes (city). No contact, URL, postal code, street, building, box or
  district text anywhere, notes included.
- Probes on scratch copies (`h74_audit/probes/probe.py` + `variants.py`, scratch `LIT_BASE`, `RunLog` redirected to
  the scratchpad; 38 runs: 35 variants, the base dry run, the base write run and the F1 write run). Run of the batch as
  written: 0 errors, 3 warnings (order trocha2018, moss2013; explicit slot bauters2011a #6); scratch write-run derived
  files byte-identical to the stamped `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`, `check_stamp.txt`. md5 of
  every repo batch file identical before and after the audit; `check_stamp.txt` matches `headers.yaml` (sha256
  0908fd75...).

## Counts

| batch | papers audited / total | slots audited | ok | gap (correct handling, no row) | imprecise | wrong |
|---|---|---|---|---|---|---|
| lit_h74 | 23 / 23 | 178 | 169 | 9 | 0 | 0 |

- Papers ok 22, partial 0, unreadable 1 (shastri2021, glued letter markers, D416 G1); `slots_from_header` 5 (exactly
  the papers.csv rows with `n_authors_meta` 0, each prints the D352 line in `show`); `author_list_differs` 2
  (trocha2018, wang2019a); explicit slots 2 (trocha2018 Denis Ganin slot 0, bauters2011a #6); order warnings 2
  (trocha2018, moss2013); present addresses 1 (trocha2018 #9); dropped markers 3 (zhang2019f #1 / #9 contact lines,
  feldmann2021 #2 Current Address, D442); unreadable authors 0; 19 unmapped org strings (44 rows).
- Gap slots (9): shastri2021 #1-#7 (paper unreadable; values in the note for the re-record list); trocha2018 #3 (list
  Dmitry V. Ganin; printed Denis Ganin is a different given name, slot 0, D287 / D369; the header author gets no row);
  wang2019a #3 (list Mengjie Yu, not printed in the preprint header). Besides, feldmann2021 #2 (N. Youngblood) has its
  printed Current Address block (University of Pittsburgh) unrecorded by rule (D442); the slot itself is recorded.
- Per paper (slots / rows): newman2019 22 / 26; tan2022 13 / 14; zhang2019f 9 / 9; xiao2008 4 / 4; trocha2018 13 / 16;
  suh2018 2 / 2; shekhar2024 7 / 7; feldmann2021 16 / 17; bogaerts2020 8 / 12; shastri2021 7 / 0; wang2019 4 / 4;
  moss2013 4 / 4; he2018 4 / 4; xu2013 5 / 5; seidler2013 5 / 5; nozaki2013 6 / 12; chang2018c 8 / 9; singh2015 9 / 12;
  molesky2018 6 / 6; jiang2019 4 / 4; bauters2011a 10 / 10; wang2019a 6 / 8; fukuda2008 6 / 6.
- Privacy findings: 0. Notes: 22 correct, 1 incomplete (bogaerts2020, F1).

### Per-slot field counts

| field | ok | gap | imprecise | wrong |
|---|---|---|---|---|
| name / slot (178) | 169 | 9 (shastri2021 x7, trocha2018 #3, wang2019a #3) | 0 | 0 |
| markers (printed / single / per_author, 171 printed authors) | 171 | 0 | 0 | 0 |
| header position / order | all | 0 | 0 | 0 |
| blocks (org / unit / more_orgs / campus / locality / country) (196 rows) | 196 | 0 | 0 | 0 |
| roles (primary / additional / present address) | 196 | 0 | 0 | 0 |
| locators | all | 0 | 0 | 0 |
| notes (23) | 22 | 0 | 1 (F1) | 0 |

## Per-paper findings

- newman2019 (22; printed, capitals): six blocks read in both layers. NIST, Boulder, US; "University of Colorado
  Boulder" -> org University of Colorado + campus Boulder (D301; 17 committed blocks of this form; probe NE1 whole
  string 0 errors, neutral), Department of Physics; NIST with the center printed before it (unit), Gaithersburg;
  Caltech, Pasadena; Charles Stark Draper Laboratories, Cambridge (as printed, committed once); Stanford University,
  Stanford; US (states and postal codes not recorded). Markers 1,2 on Stone / Fredrick / Diddams / Papp. List forms
  Vincent N. / Tara E. / B. Ilic / Leo W. / Kartik A. / John E. matched by name. Probe NE2 (Li on 1) 2 errors. ok.
- tan2022 (13; printed, capitals): block 1 "Wuhan National Laboratory for Optoelectronics & School of Optical and
  Electronic Information" as the HUST unit chain (9 committed blocks with this exact "&" form, 11 with "and"); Ori-Chip
  Optoelectronics Technology Co. Ltd., Ningbo; Zhejiang University with the college printed before it, Hangzhou;
  Changchun University of Science and Technology with the key laboratory as unit, Changchun; CN (streets and postal
  codes not recorded). CAN LIU split across lines verifies (TA1 without 3: 3 errors). ok.
- zhang2019f (9; printed, capitals): "University of California, Davis" -> org + campus Davis (D301), ECE unit; the two
  Lockheed Martin companies, Louisville / Eagan; US. Markers 4 (Yu Zhang) and 5 (Ben Yoo) point to the two contact
  lines: `dropped_markers` "contact footnote" (ZH1 without: 2 errors). ok.
- xiao2008 (4; single, slots from header): NIST, Boulder; the block prints a state and postal code but no country:
  country "" (XI1 US: 2 errors). ok.
- trocha2018 (13; printed, arXiv): KIT with IPQ unit, Karlsruhe, DE; EPFL as printed (detached accents folded, D282),
  Lausanne, CH; block 3 "Now with:" -> present address Carl Zeiss AG with the unit printed before it, Oberkochen, DE
  (TR3 role removed: 2 errors; committed form exists once); block 4 KIT with IMT unit, Eggenstein-Leopoldshafen, no
  country printed (TR4 DE: 2 errors). Weimann 1,3 (TR5 without 3: 3 errors); Randel / Freude / Koos 1,4. Asterisks are
  the equal-contribution footnote, dagger / double dagger the two contact lines (symbols used by no block). Denis
  Ganin vs list Dmitry V. Ganin: slot 0 required (TR1 without: 1 error, 0 compatible slots); slot 3 passes the checker
  (TR2, 0 errors) but D287 bars a match between different given names. Order warning expected (list order Trocha,
  Karpov, Ganin, ...). ok (#3 gap).
- suh2018 (2; single, arXiv): Caltech with the T. J. Watson Laboratory of Applied Physics printed before it, Pasadena,
  US. Kerry Vahala vs list Kerry J. Vahala matched by name. ok.
- shekhar2024 (7; printed, arXiv): block 1 marker printed "1*" (verifies); UBC ECE, Vancouver, CA; "Ghent University
  - IMEC" kept (D426), Department of Information Technology printed before it, Ghent, BE; UCSB and "University of
  Massachusetts Boston" printed without a comma -> org + campus (D301; committed UMass Boston / Lowell campus forms);
  Luminous Computing, Santa Clara; Queen’s University (curly apostrophe as printed), Kingston, CA. Streets, postal
  codes, states and provinces not recorded. SK1 (Soref on 4) 4 errors. ok.
- feldmann2021 (16; printed, arXiv): University of Muenster Institute of Physics, Muenster; Oxford Department of
  Materials, Oxford, GB; block 3 Current Address (University of Pittsburgh) not recorded, marker 3 under
  `dropped_markers` on Youngblood: the D442 form of lit_h65 / h67 / h70 and 11 earlier batches (FE1 recorded as a
  present address: 2 errors, marker + cue + first field fails; FE2 without the dropped marker: 2 errors); "Swiss
  Federal Institute of Technology Lausanne (EPFL)" as printed with the laboratory unit, Lausanne, CH; "IBM Research -
  Zurich" kept (D426), Rüschlikon, CH; Exeter Department of Engineering, Exeter, GB; "University of Münster" Center
  for Soft Nanoscience, Münster, DE (spelling differs from block 1 as printed). Asterisks equal contribution, hash
  the correspondence line. ok (Current Address to the D442 cue list).
- bogaerts2020 (8; printed, p.1 footnote): the nine blocks are printed at the foot of the first column of page 1
  (locator p.1 footnote; BO1 p.1 header also passes, neutral). Ghent University – IMEC (D426) + IT department, Gent;
  block 2 Ghent University with the center printed before it, no city printed: locality "" (BO2 Ghent: 0 errors, the
  known city-inside-org gap); Universitat Politècnica València (as printed) + ITEAM, Valencia, ES; iPronics, Valencia,
  ES (the "Programmable Photonics" words after it not recorded: part of the company style, neutral); Stanford Ginzton
  Laboratory; Max Planck Institute of Microstructure Physics, Halle, DE; University of Toronto + Rogers ECE (semicolon
  separator), Toronto, CA; MIT RLE, Cambridge, US; Politecnico di Milano + DEIB (dash separator), Milano, IT. Poon 6,7
  (BO3 without 7: 3 errors). List forms J. Capmany / David A. B. / Joyce K. S. / Andrea Ivano matched by name. Note
  incomplete (F1): blocks 5 and 7 also print the organization before the unit. ok.
- shastri2021 (7; unreadable): call confirmed. The author markers are glued to the names in the text layer
  (superscripts only in the PDF layer) and all six block markers are glued to the block's first word in both layers.
  Probe SH2 (the full record, printed basis, g = equal contribution and h = contact line dropped): 19 errors (7 md
  author errors; 6 md + 6 pdf block errors: the marker cannot precede a word start); SH1 (basis pdf): 25 errors (lit
  has no pdf-basis source). No block verifies in either layer, so not even `partial` is possible; nothing recorded,
  values in the note (gatkine2022 lit_h29 form). The note's block values (orgs, units, cities, countries, author
  carriers) agree with the page. Re-record list (G1). ok.
- wang2019 (4; printed, markers with a period): Peking University with the state key laboratory + collaborative
  innovation center + school chain, Beijing, CN (committed form once); "Dipartimento di Fisica - Sapienza Università
  di Roma": unit + org (WG1 org only: 2 errors, the unit is the first printed field), Roma, IT; Bristol QET Labs + H. H.
  Wills + EEE chain (3 committed blocks), Bristol, "United Kingdom" -> GB. ok.
- moss2013 (4; per_author, D368): one block under each name: INRS-EMT (street before Varennes not recorded), Varennes,
  CA; RMIT University with SECE unit, Melbourne, AU; Cornell AEP and Cornell ECE, Ithaca, US. Printed order Morandotti,
  Moss, Gaeta, Lipson vs list Moss, Morandotti: YAML in printed order, order warning expected (D363). MO1 (G1 / G2
  carriers swapped) 4 errors; MO2 (G3 / G4 units swapped) 4 errors: positions verified. List forms David Moss / Michal
  F. Lipson matched by name. ok.
- he2018 (4; single, capitals): Shanghai Jiao Tong University with the state key lab + department chain, Shanghai, CN.
  HE1 (name altered) 4 errors. ok.
- xu2013 (5; single, slots from header): Zhejiang University with the three-unit chain, Hangzhou, CN; Zijingang
  Campus not recorded (lit_h01 / h10 / h33 form). Probe XU1 (authors 1 / 2 swapped): 2 errors, so the header order is
  now verified for single-block header-slot papers (h72 O1 gap not reproduced here). ok.
- seidler2013 (5; single, slots from header): "IBM Research – Zurich" (en dash, kept, D426; committed once), Rüschlikon,
  CH (street and postal code not recorded; SE1 hyphen form 0 errors, folded). ok.
- nozaki2013 (6; printed, slots from header): three blocks with the NTT center / laboratory before "NTT Corp." (unit,
  org as printed; committed lit uses "NTT Corporation" where printed so), Atsugi, JP; the district printed before
  Atsugi, the prefecture and postal codes not recorded. NO1 (Matsuo 1,2) 2 errors. ok.
- chang2018c (8; printed, capitals): HUST with the school (block 1) and with WNLO as unit (block 2; 9 committed blocks
  of this form), Wuhan, CN. CH1 (Zhang without 2) 1 error. ok.
- singh2015 (9; printed, slots from header): block 1 University of Sydney with the CUDOS + IPOS + School of Physics
  chain, only the state and postal code printed: locality "" (SG1 Sydney 0 errors, known city-inside-org gap); block 2
  Australian National University with the CUDOS + Laser Physics Center + school chain, Canberra, AU; block 3 Université
  de Lyon + `more_orgs` Institut des Nanotechnologies de Lyon, CNRS, Ecole Centrale de Lyon, Ecully, FR (four orgs,
  D285; lit_h27 / h29 Université de Lyon forms; the INL acronym glued to the UMR number not copied: SG2 with INL 0
  errors, neutral; SG3 single org 0 errors but loses 3 printed orgs). Eric C. Mägi as printed. ok.
- molesky2018 (6; printed, closing parenthesis markers): Princeton EE, Princeton; Harvard SEAS (no comma before the
  university), Cambridge; Stanford Ginzton Laboratory, Stanford; no country printed in any block: country "" (MOL1 US:
  2 errors). Jelena Vučković vs list "Jelena Vuckovic A" (D412 artefact) matched by name. ok.
- jiang2019 (4; single, capitals): Nanjing University of Posts and Telecommunications with the college printed before
  it, Nanjing, CN. List full given names match the printed initials. ok.
- bauters2011a (10; printed): UCSB ECE ("University of California, Santa Barbara" -> org + campus), US; LioniX BV,
  Enschede, NL (postal box and postal code not recorded; 7 committed LioniX BV blocks). Jonathon S. Barton vs list Jon S.
  Barton: explicit slot 6 (D287 short form, initials agree; BA1 without: 2 errors). "Daoxin Dai A" list artefact (D412),
  matched by name. ok.
- wang2019a (6; printed, arXiv): Harvard SEAS, Cambridge, US; City University of Hong Kong EE, Kowloon, HK (14 committed
  Kowloon / HK blocks vs 1 Kowloon / CN; WA1 Hong Kong locality 0 errors, neutral); Zhejiang University with the
  academy + college chain, and with the College of Optical Science and Engineering, Hangzhou, CN. The preprint prints 5
  names; list slot 3 (Mengjie Yu) not printed: `author_list_differs`, no_header. Equal-contribution / dagger footnotes
  printed on the last page of text.md (note claim verified). WA2 (Hu without 4) 3 errors. ok (#3 gap).
- fukuda2008 (6; single): NTT Microsystem Integration Laboratories printed alone (org as printed, 4 committed blocks),
  locality "Atsugi-Shi" as printed (D366 "Atsugi-shi" precedent; FU1 Atsugi 0 errors, neutral), JP; street, district
  and prefecture not recorded; the web address line not recorded and not copied. ok.

## Extractor calls (verified)

1. shastri2021 `unreadable` (glued letter markers, D416 G1, gatkine2022 precedent): confirmed (SH1 / SH2; no block
   verifies in either layer, so `partial` is not available).
2. `slots_from_header` on xiao2008, xu2013, seidler2013, nozaki2013, singh2015: exactly the 5 papers with
   `n_authors_meta` 0; YAML in printed order (read, and XU1 shows the order is checked for xu2013). Confirmed.
3. trocha2018 Denis Ganin slot 0 + `author_list_differs`, list slot 3 no_header: confirmed (TR1 / TR2, D287 / D369).
   O1 for the list name.
4. wang2019a preprint header omits list slot 3 (Mengjie Yu): `author_list_differs`, no rows: confirmed.
5. moss2013 per_author G1-G4, order warning: confirmed (MO1 / MO2).
6. bauters2011a slot 6 Jonathon / Jon (D287): confirmed (BA1).
7. trocha2018 Carl Zeiss "Now with" present address: confirmed (TR3, TR5).
8. feldmann2021 University of Pittsburgh "Current Address" not recorded, marker under `dropped_markers`, paper `ok`
   (D442; lit_h65 / h67 / h70 and older precedents): confirmed (FE1 / FE2).
9. Campus splits (D301): newman2019 Colorado Boulder, zhang2019f UC Davis, shekhar2024 UCSB and UMass Boston,
   bauters2011a UCSB: confirmed (committed forms; NE1 whole string neutral). Zijingang Campus (xu2013) correctly not a
   campus.
10. Dash-joined orgs kept (D426): shekhar2024 "Ghent University - IMEC", bogaerts2020 "Ghent University – IMEC",
    feldmann2021 "IBM Research - Zurich", seidler2013 "IBM Research – Zurich": confirmed. wang2019 and bogaerts2020
    block 9 dashes separate a unit from the org (not joined orgs): unit + org, confirmed (WG1).
11. WNLO as a HUST unit chain (tan2022 block 1, chang2018c block 2): majority committed form, confirmed.
12. singh2015 block 3 as four orgs (D285): confirmed (SG2 / SG3).
13. bogaerts2020 page-1 footnote blocks (locator p.1 footnote): confirmed; note incomplete (F1).
14. Empty country (xiao2008, trocha2018 block 4, molesky2018 blocks 1-3) and empty locality (bogaerts2020 block 2,
    singh2015 block 1): confirmed (XI1, TR4, MOL1; BO2 / SG1 pass only through the known city-inside-org gap).

## Fixes (exact YAML edits)

F1 (bogaerts2020 note, incomplete: blocks 5 (Stanford University, Ginzton Laboratory) and 7 (University of Toronto;
Rogers ECE) also print the organization before the unit). In
`data/_staging/people/lit_headers/lit_h74/headers.yaml`, line 173 (note of `lit:bogaerts2020`), replace

```
blocks 1, 3 and 9 print the organization before the unit;
```

with

```
blocks 1, 3, 5, 7 and 9 print the organization before the unit (block 7 separates them with a semicolon);
```

Probe of the batch with F1 applied (write run on a scratch copy): 0 errors, 3 warnings (unchanged); `header_rows.csv`,
`compare.csv`, `unmapped_orgs.csv` byte-identical to the stamped files (196 rows, 19 unmapped strings); only
`check_stamp.txt` changes. After applying, re-run `uv run python scripts/ofc_headers.py check lit_h74 --corpus lit`.

No other fix: no slot, marker, block field, role, locator or other note is wrong.

## Observations (no YAML change)

- O1 trocha2018 list name: the list gives "Dmitry V. Ganin" in slot 3; the paper prints "Denis Ganin" (KIT IPQ, and
  "D.G." in the equal-contribution footnote). Candidate for the D412 author-list correction file; the YAML is correct
  under D287 until the list is corrected.
- O2 Known gaps reconfirmed: a city inside the org name is accepted as locality (BO2 Ghent, SG1 Sydney); an empty
  locality is accepted where a city is printed (BA2 LioniX locality "" passes, D599 gap); TR2 shows the checker accepts
  an explicit slot between different given names (D287 is enforced by review only).
- O3 Header-slot order: XU1 errors when two authors of a single-block header-slot paper are swapped (name position
  check "not printed after the previous author"), so the h70 / h72 O1 gap seen on prose and swapped-name probes does
  not apply to this batch's plain bylines.
- O4 shastri2021 values in the note are ready for the re-record once glued letter markers are supported (G1 test
  case: six blocks, all glued to their first word in both layers).

## Lists for the coordinator

- D412 list: trocha2018 #3 (list Dmitry V. Ganin; printed Denis Ganin; O1); molesky2018 #5 "Jelena Vuckovic A" and
  bauters2011a #4 "Daoxin Dai A" (already on the artefact list).
- D426 review list: bauters2011a #6 (Jonathon / Jon S. Barton, explicit slot); trocha2018 Denis Ganin (slot 0).
- D442 cue list: feldmann2021 #2 (Current Address, University of Pittsburgh, Pittsburgh, US).
- Re-record list: shastri2021 (all 7 authors, glued letter markers, D416 G1).
- Org round (19 unmapped strings, 44 rows): Australian National University (unit chain; committed "The Australian
  National University"); Charles Stark Draper Laboratories; Ecole Centrale de Lyon; INRS-EMT; Institut des
  Nanotechnologies de Lyon; LioniX BV; Lockheed Martin Advanced Technology Laboratory; Lockheed Martin Coherent
  Technologies; NTT Microsystem Integration Laboratories; Nanjing University of Posts and Telecommunications; Ori-Chip
  Optoelectronics Technology Co. Ltd.; Princeton University (country empty); RMIT University; Sapienza Università di
  Roma; Universitat Politècnica València; University of Exeter; "University of Massachusetts, Boston" (campus);
  University of Muenster (spelling variant of the mapped University of Münster); Université de Lyon.

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 3 warnings, 196 rows, 19 unmapped; derived files identical | batch as written |
| TR1 / TR2 | trocha2018 Ganin slot 0 removed / slot 3 | 1 / 0 errors (197 rows) | slot 0 required; slot 3 barred by D287 |
| TR3 / TR4 / TR5 | Zeiss role removed / block 4 country DE / Weimann without 3 | 2 / 2 / 3 errors | present address, empty country, markers verified |
| FE1 / FE2 | feldmann2021 Current Address as present address / dropped marker removed | 2 / 2 errors | D442 form required |
| BA1 / BA2 | bauters2011a slot 6 removed / LioniX locality empty | 2 / 0 errors | slot required / known empty-locality gap |
| SH1 / SH2 | shastri2021 full record, basis pdf / printed | 25 / 19 errors | unreadable confirmed |
| MO1 / MO2 | moss2013 carriers G1/G2 swapped / units G3/G4 swapped | 4 / 4 errors | per_author positions verified |
| XI1 / MOL1 | country US on xiao2008 / molesky2018 block 1 | 2 / 2 errors | country not printed |
| XU1 | xu2013 authors 1 / 2 swapped | 2 errors | header order verified (O3) |
| SG1 / SG2 / SG3 | singh2015 locality Sydney / INL acronym / single org | 0 / 0 / 0 (193 rows) errors | gap / neutral / loses printed orgs |
| BO1 / BO2 / BO3 | bogaerts2020 locator header / block 2 locality Ghent / Poon without 7 | 0 / 0 / 3 errors | neutral / gap / markers verified |
| NE1 / NE2 | newman2019 whole Colorado string / Li on 1 | 0 / 2 errors | neutral / markers verified |
| ZH1 | zhang2019f dropped contact marker removed | 2 errors | dropped marker required |
| WA1 / WA2 | wang2019a locality Hong Kong / Hu without 4 | 0 / 3 errors | neutral (Kowloon is the committed form) / verified |
| WG1 | wang2019 Sapienza without the unit | 2 errors | unit is the first printed field |
| NO1 / TA1 / CH1 / SK1 / HE1 | marker or name variants | 2 / 3 / 1 / 4 / 4 errors | verified |
| SE1 / FU1 | seidler2013 hyphen for en dash / fukuda2008 Atsugi | 0 / 0 errors | neutral (folded / as-printed kept) |
| FIX | F1 note rewording | 0 errors, 3 warnings, derived CSVs identical | F1 safe |
