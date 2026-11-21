---
title: Fresh-context audit of the lit author-affiliation batch lit_h59 (18 papers)
date: 2026-11-20
mode: read-only on the batch (wrote only this record and scratchpad show dumps, page renders and probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only as dry runs on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h59/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D287, D288, D301, D366, D380, D410, D426, D442, D572); format from the lit_h57 audit
verdict: GO after F1; 113 slots (35 list + 78 slots_from_header) audited; 0 wrong rows; 1 imprecise slot (alloush2021 #7 Luc Augustin marked unreadable although the PDF layer verifies the statement: F1 makes it readable, rows 121 -> 122; its country stays empty, checker gap); N1 / N2 optional note wording
---

# Lit header batch audit: lit_h59 (2026-11-20)

## Scope

Batch lit_h59: 18 papers (IEEE JSTQE / PTL / JQE, Optics Express, two conference papers, two 1996 OCR scans); 113
slots, 13 papers `slots_from_header`; 121 rows (prose 93, printed 28; all grade A). Restricted corpus: this record
names only authors, orgs, units, cities and countries; no paper text is quoted and no contact, street, postal-box or
postal text is copied (address parts are described, not named).

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h59 --corpus lit --codes <id> --pdf`
  (all 18); output kept in the session scratchpad `h59_audit/show/`.
- Page renders (`pdftoppm` 200 dpi, page 1 footnote crops, scratchpad `h59_audit/render/`) for mason2000 (unit
  misprint), staring1996 (city misprint), zirngibl1996 (OCR line order), alloush2021 (statement 4 and its country) and
  cao2014 (singular "Science", which the checker cannot distinguish, see O5).
- Per slot: printed name vs the `show` author list (or the header for the 13 header-slot papers) and `compare.csv`;
  marker run (text and PDF layers); prose statement subjects and verbs; block fields (org, unit chain, campus, city,
  country); role; locator; continuation; notes.
- 40 distinct (paper, marker, role, org, unit, city, country, org id, match) tuples of `header_rows.csv` read (121 rows;
  primary 112, additional 9, present address 0).
- Address / contact scan of `headers.yaml` and the four derived CSVs (postal-code, street, road, route, building, box,
  phone, fax, mail, URL, domain and digit patterns, plus the address parts printed in these papers): clean. Notes name
  street addresses, states, postal codes and a postal box only as words ("not recorded"); the vandekerckhove2023 block 2
  box code sits in `skip_between: "<postal box>"` (D410 token, never stored); the only digits in the files are years in
  paper ids and notes. A ward name (fujita1999) is in a note, allowed by D366.
- Precedent scans over all committed lit / OFC `headers.yaml`: SIMIT State Key Laboratory of Functional Materials for
  Informatics (5 committed blocks, same org + unit form), "Chinese Academy of Science" singular (University of Chinese
  Academy of Science blocks, printed form kept), UC Davis (14 blocks as `University of California` + campus Davis, one
  older whole-string form), UC Santa Barbara campus form (123 blocks, none with a leading article in `org`), University
  of Illinois at Urbana-Champaign (7 bare, 1 "The", 1 "the"), Lucent Technologies + Bell Laboratories / Crawford Hill
  units (3), NTT Photonics Laboratories unit chains (4), III-V lab (22 bare, 1 lit_h02 block with partners in
  `more_orgs`, D426 normalizes to bare), OPTO+ (first occurrence), hyphenated-country empty-country cases
  (lit_h20 lindenmann2014, palmer2026).
- Probes on scratch copies (`h59_audit/probes/probe.py`: scratch `LIT_BASE`, batch name `lit_p59`,
  `cmd_check(..., dry_run=True)`; 17 probe runs plus 2 instrumented runs of the D354 subject parser,
  `h59_audit/probes/dbg.py`). Dry-run check of the batch as written: 0 errors, 0 warnings; totals equal the stamped
  derived files (113 slots, 112 recorded, 1 no_header, 121 rows, 9 unmapped strings). md5 of every repo batch file
  identical before and after the audit; `check_stamp.txt` matches `headers.yaml` (sha256 7350c9f9...). Probe checks
  wrote their usual logs under `logs/` (prefix `lit_headers_check_lit_p59`, 42 files).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h59 | 18 / 18 | 113 | 112 (112 recorded) | 1 (alloush2021 #7, no_header; F1) | 0 |

- Papers ok 17, partial 1 (alloush2021), unreadable 0; after F1 all 18 ok. `slots_from_header` 13 (serries2001,
  papatryfonos2014, cao2014, cheung2010, menezo1999, fujita1999, wang1998, byun2009, zirngibl1996, sato2008, mason2000,
  gopinath2007, staring1996; all print the D352 line in `show` and have `n_authors_meta` 0); `author_list_differs` 0;
  explicit slots 0; order warnings 0.
- Per paper (slots / rows): huang2016c 6 / 7; vandekerckhove2023 8 / 12; cheng2023b 4 / 8; serries2001 5 / 5;
  papatryfonos2014 8 / 8; komljenovic2015 6 / 6; cao2014 6 / 6; cheung2010 8 / 8; menezo1999 6 / 6; fujita1999 3 / 3;
  wang1998 3 / 3; byun2009 7 / 7; zirngibl1996 5 / 5; sato2008 5 / 5; alloush2021 11 / 10 (11 after F1);
  mason2000 5 / 5; gopinath2007 9 / 9; staring1996 8 / 8.

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (113) | 113 | 0 | 0 |
| markers (printed / prose, 112 recorded) | 112 | 0 | 0 |
| header position / statement subject | 112 | 0 | 0 |
| blocks (org / unit / campus / locality / country) (112 slots with rows) | 112 | 0 | 0 |
| unreadable calls (1 slot) | 0 | 0 | 1 (alloush2021 #7 readable on the PDF layer, F1) |
| present addresses (0) | - | - | - |
| locators | all | 0 | 0 |
| notes (18) | 15 | 2 (fujita1999 ward spelling, zirngibl1996 split described as printed; N1 / N2 optional) | 1 (alloush2021: wrong checker-gap claim, F1) |

After F1, alloush2021 #7 gets a row with `country: ""` although the page prints the Netherlands (hyphenated across a
line break, D442 checker gap, lindenmann2014 / palmer2026 precedent): imprecise, not fixable now.

## Per-paper findings

- huang2016c (6; prose, list): statement 1 Huang / Zhang / Bowers UCSB ECE (org University of California + campus
  Santa Barbara, D301); statement 2 Pintus UCSB ECE with an "and also with" clause to the TeCIP Institute, Scuola
  Superiore Sant'Anna, Pisa, IT (P3 `clause: true`, D366; probe H1 without `clause` gives 4 errors: required);
  statements 3 / 4 Shoji (Quantum Nanoelectronics Research Center) and Mizumoto (Department of Electrical and
  Electronic Engineering), Tokyo Institute of Technology, Tokyo, JP. The equal-contribution sentence names no
  affiliation. "John E. Bowers" matches the list "John Edward Bowers". ok.
- vandekerckhove2023 (8; printed, conference): markers printed "1." / "2." / "3." on the blocks; author runs read in
  both layers (Vandekerckhove 1,2; Vanackere 1,2; Clemmen 1,2,3; others 1); asterisk = contact line (symbol, no block).
  Block 1 "Ghent University - imec" with unit "Photonics Research Group, INTEC" (D426 dash-joined joint org; maps to
  Ghent University + imec by alias); block 2 OPERA-Photonique, Universite Libre de Bruxelles, a postal-box code printed
  between unit and org recorded as `skip_between: "<postal box>"` (D410, the lit_h10 vandekerckhove2025 form; probe V1
  without it: 2 errors); block 3 Laboratoire d'Information Quantique, same university; Ghent / Brussels, BE. ok.
- cheng2023b (4; printed, capitals): blocks 1, 2, 4, 5 National Taiwan University units, Taipei, TW; block 3 unit chain
  "Nick Holonyak, Jr. Micro and Nanotechnology Laboratory, Department of Electrical and Computer Engineering" with org
  "the University of Illinois at Urbana-Champaign" (leading article as printed, D288; maps `alias:no_article`), Urbana,
  US; street parts not recorded. "CHAO-HSIN WU" matches the list "Chao-Hsin Wayne Wu" (dropped middle name). Probe C1:
  the bare org also passes; the printed form is the rule. ok.
- serries2001 (5; prose, slots from header): one "The authors" statement: Fraunhofer-Institut fur Angewandte
  Festkorperphysik (line-break hyphen joined into the compound word), Freiburg, DE; postal prefix not recorded. ok.
- papatryfonos2014 (8; printed "1:" / "2:", conference, slots from header): block 1 "CNRS Laboratory for Photonics and
  Nanostructures" as one printed name (CNRS printed inside the name, not a trailing parent), Marcoussis, FR; block 2
  "III-V lab" (lower-case l as printed) with its joint-lab description of three parents dropped (D426 keyvaninia2012
  ruling), Marcoussis, FR; street parts not recorded. Joshi 2, all others 1. ok.
- komljenovic2015 (6; prose, list): statement 1 prints the university with a leading article and the campus without a
  comma: org University of California + campus Santa Barbara (no unit printed; 123 committed campus blocks carry no
  article in `org`); statement 2 Aurrion Inc., Goleta, US (Norberg, Fish). Name forms match the list (Komljenovic accent,
  dropped middle initials). ok.
- cao2014 (6; prose, slots from header): one "The authors" statement; unit State Key Laboratory of Functional Materials
  for Informatics, org "Shanghai Institute of Microsystem and Information Technology, Chinese Academy of Science"
  (singular confirmed on the page render; the 5 committed SIMIT blocks use the same org + unit split with the plural as
  printed there), Shanghai, CN. ok.
- cheung2010 (8; prose, slots from header): statement 1 (seven authors, Yoo as "S. J. B. Yoo") University of California
  at Davis: org University of California + campus Davis, unit Department of Electrical and Computer Engineering, Davis,
  US (majority committed form); statement 2 Baney, Measurement Research Laboratory, Agilent Technologies, Santa Clara,
  US. Author 8 recorded as printed in the author line ("S. J. Ben Yoo"). ok.
- menezo1999 (6; prose, slots from header): statement 1 (five authors) and statement 2 (Gaborit) both print OPTO+
  followed by a partner (France Telecom/BD/CNET resp. Alcatel CRC) and the GIE legal form, Marcoussis, France: org
  OPTO+ only, Marcoussis, FR, two blocks (two statements, D354). Dropping the partners follows the III-V lab ruling
  (D426); the partners are the parent employers of the joint lab, not separate affiliations. ok.
- fujita1999 (3; prose, slots from header): "The authors" statement: Division of Electrical and Computer Engineering,
  Yokohama National University, Yokohama, JP; the ward printed before the city goes to the note (D366). The note writes
  the ward hyphenated while both text layers print it without a hyphen (N1, optional). ok.
- wang1998 (3; prose, slots from header): Department of Electrical Engineering, National Taiwan University, Taipei; the
  place prints Taiwan with R.O.C.: TW. ok.
- byun2009 (7; prose, slots from header): statement 1 Byun / Pudo / Ippen / Kartner, Department of Electrical
  Engineering and Computer Science, Massachusetts Institute of Technology, Cambridge, US; statement 2 Frolov / Hanjani /
  Shmulovich, CyOptics, Inc., South Plainfield (line-break hyphen joined), US. ok.
- zirngibl1996 (5; prose, OCR scan, slots from header): "The authors" statement, Lucent Technologies with Bell Labs
  Innovations as unit (Lucent + Bell Laboratories unit precedent, 3 committed blocks), Holmdel, US. The page render
  prints the statement contiguous (city, state and country on consecutive lines); both text layers read the publisher
  item line between the city line and the state line, so `continued: "NJ"` binds the country check to the right line.
  Probe Z1 without `continued`: 0 errors (the 300-character window reaches the country anyway); keeping it is the
  tighter verification. The note describes the split as printed; it is a text-layer artefact (N2, optional). ok.
- sato2008 (5; prose, slots from header): three statements with NTT unit chains ending in NTT Photonics Laboratories,
  org "Nippon Telegraph and Telephone (NTT) Corporation" (3 committed blocks use this form); each prints only a
  prefecture, so `locality: ""` (D288; probe SA1 with the prefecture also passes: O4 gap, the empty value is the rule);
  JP. The `show` terminal output leaves a contact-domain fragment unmasked (known D659 item); no batch file carries it. ok.
- alloush2021 (11; prose, list): statements 1 / 2 Ruhr University Bochum, Institute of Photonics and Terahertz
  Technology resp. Institute of Electronic Circuits, Bochum, DE; statement 3 Lo, Research Group of Information and
  Communication Engineering, University College London, London, GB (U.K. printed); statement 4 Augustin, SMART
  Photonics, Eindhoven, the Netherlands hyphenated across a line break; statement 5 Guzman / Carpintero, Department of
  Electronic Technology, University Carlos III de Madrid, Leganes, ES. "M. Ali Alloush" matches "Mohammad Ali Alloush".
  Extractor call on #7 tested: the claimed subject gap holds only for the text layer. The checker accepts a block when
  one layer passes; in the PDF layer the statements are separated by a blank line and the subject of statement 4 is
  exactly "Luc Augustin" (instrumented run). Probe A4 (#7 readable, status ok, country empty): 0 errors; A5 (Augustin on
  P5) and A6 / A7 (Lo added to or moved to P4) fail as they should, so the subject check is live. The country cannot be
  recorded (A2 / A3 with NL: country not found, D442 hyphenation gap). F1.
- mason2000 (5; prose, slots from header): statement 1 Agility Communications, Inc., Santa Barbara, US (Mason, Fish);
  statement 2 Electrical and Computrer Engineering Department (misprint confirmed on the page render), University of
  California Santa Barbara without a comma: org University of California + campus Santa Barbara, US. Probe M1 with the
  corrected spelling: 4 errors (as-printed form required). ok.
- gopinath2007 (9; prose, slots from header): "The authors" statement, MIT Lincoln Laboratory, Lexington, US; Life
  Fellow / Senior Member designations ignored. ok.
- staring1996 (8; prose, OCR scan, slots from header): statement 1 (six authors) Philips Optoelectronics Centre,
  locality "Eindoven" (misprint confirmed on the page render; probe ST1 with Eindhoven: 2 errors); statement 2
  Spiekman / Smit, Delft University of Technology, Delft, NL; postal code not recorded. ok.

## Fixes

F1 (alloush2021 #7 readable; status and note). In `lit:alloush2021` replace

```yaml
  status: partial
```

with

```yaml
  status: ok
```

replace

```yaml
    - {name: "Luc Augustin", markers: ["P4"], unreadable: true}
```

with

```yaml
    - {name: "Luc Augustin", markers: ["P4"]}
```

and replace the paper note with

```yaml
  note: "affiliations printed as footnote statements (prose); statement 4 (Luc Augustin, SMART Photonics, Eindhoven) prints its country hyphenated across a line break (The Nether-lands), which the checker cannot verify: country left empty (printed NL; lindenmann2014 / palmer2026 precedent); the text layer runs statement 4 on from statement 3 (no accepted boundary after U.K.), the PDF layer separates them and verifies the subject; author 1 printed M. Ali Alloush, the author list prints Mohammad Ali Alloush; statement 3 prints U.K. as the country; membership designations in the author line; postal codes not recorded"
```

(block P4 unchanged: `org: "SMART Photonics", locality: "Eindhoven", country: ""`; the new row maps to the existing
`org_smart_photonics`; unmapped strings stay 9).

N1 (optional, fujita1999 note). Replace `the statement names the ward Hodogaya-ku before the city` with
`the statement names the ward Hodogayaku (as printed) before the city`.

N2 (optional, zirngibl1996 note). Replace `the statement is split after the city by the publisher item line, the state
and country follow on the next footnote line (continued)` with `in both text layers the publisher item line is read
between the city and the state and country line (the page prints the statement contiguous; continued)`.

Combined probe FINAL (F1 + N1 + N2): 0 errors, 0 warnings; slots 113, recorded 113, no_header 0, rows 122 (prose 94,
printed 28; primary 113, additional 9); papers ok 18; unmapped strings 9.

## Observations (no YAML change)

- O1 The partial call on alloush2021 rested on the text-layer failure only; the checker passes a prose block when the
  PDF layer verifies it. Extractors should probe the readable form before marking an author unreadable.
- O2 Subject cut (`PROSE_CUT_RE`): a dotted country abbreviation ("U.K.", "U.S.A.") is not a sentence boundary
  (`[A-Z]{2,}\.` needs two adjacent capitals and the country-word list skips words of 3 or fewer letters), so in the
  text layer the subject of statement 4 includes the tail of statement 3. Adding dotted abbreviations as boundaries
  would make the text layer pass too.
- O3 Hyphenated country across a line break (D442 gap) still blocks NL for alloush2021 P4: re-record after the fix.
- O4 Locality check accepts a prefecture (sato2008 SA1), known D572 gap; the recorded empty value is right.
- O5 Probe CA1: the checker accepts "Chinese Academy of Sciences" for the printed singular because the next printed
  word starts with s (normalized substring); only the render settles it (singular, recorded correctly).
- O6 zirngibl1996: `continued` is not required by the checker (Z1) but is the more precise verification; no change.
- O7 cheng2023b: org with and without the leading article both pass (C1); the printed form stays (D288).

## Lists for the coordinator

- Re-record list (after O3 / the D442 hyphenated-country fix): alloush2021 P4 country NL.
- D426 review list: none new (menezo1999 OPTO+ partners and papatryfonos2014 III-V lab parents dropped under the
  existing D426 ruling).
- Org round (9 unmapped strings, unchanged by F1): CNRS Laboratory for Photonics and Nanostructures; CyOptics, Inc.;
  Fraunhofer-Institut fur Angewandte Festkorperphysik (printed with umlauts); OPTO+; Philips Optoelectronics Centre;
  Ruhr University Bochum (two unit strings); SIMIT with "Chinese Academy of Science" singular (alias of the plural form);
  University Carlos III de Madrid.

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 0 warnings | batch as written; totals equal the stamped files |
| A1 | alloush2021 #7 readable, status partial | 1 error (partial needs an unreadable author) | status must follow |
| A2 | #7 readable, status partial, P4 country NL | 4 errors | NL not verifiable (O3) |
| A3 | #7 unreadable, P4 country NL | 2 errors | NL not verifiable |
| A4 | #7 readable, status ok, country empty | 0 errors, rows 122 | F1 |
| A5 | #7 readable on P5 | 4 errors | subject check live |
| A6 / A7 | Lo also on / moved to P4 | 3 / 6 errors | subject check live |
| Z1 | zirngibl1996 without `continued` | 0 errors | O6 |
| V1 | vandekerckhove2023 block 2 without `skip_between` | 2 errors | skip token required |
| H1 | huang2016c P3 without `clause` | 4 errors | clause required |
| M1 | mason2000 unit "Computer" | 4 errors | misprint as printed required |
| ST1 | staring1996 locality Eindhoven | 2 errors | misprint as printed required |
| SA1 | sato2008 P2 locality = prefecture | 0 errors | O4 gap; empty is the rule |
| C1 | cheng2023b org without the article | 0 errors | O7; printed form kept |
| CA1 | cao2014 "Sciences" | 0 errors | O5; render confirms singular |
| FINAL | F1 + N1 + N2 | 0 errors, 0 warnings, rows 122 | fixes pass |
