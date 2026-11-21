---
title: Fresh-context audit of the lit author-affiliation batch lit_h61 (18 papers)
date: 2026-11-20
mode: read-only on the batch (wrote only this record and scratchpad show dumps, one page render and probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only with --dry-run on the batch, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h61/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D366, D380, D426, D442 iseghem2022 gap, D461, D557, D686, D699); format from the lit_h59 / lit_h60 audits
verdict: GO (105 slots audited, 105 recorded with 0 wrong rows; 133 rows correct; no privacy finding); apply F1 (kim2004 note: incomplete garble description, render values missing; no row change) before commit; N1 optional (raptakis2021 note); all other extractor calls confirmed
---

# Lit header batch audit: lit_h61 (2026-11-20)

## Scope

Batch lit_h61: 18 papers (IEEE PTL / JLT prose footnotes, Optics Express / CLEO / ICTON / IEEE conference printed,
grouped, per-author and single blocks, one IEEE Photonics Journal cover page, one OCR scan); 105 slots, 7 papers
`slots_from_header`; 133 rows. Restricted corpus: this record names only authors, orgs, units, cities, districts and
countries; no paper text is quoted and no contact, street, building, site or postal text is copied. The park2007b site
name is referred to by type only.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h61 --corpus lit --codes <id> --pdf`
  (all 18; hirano2020 also with `--pages 2`); output kept in the session scratchpad `h61_audit/show/` only.
- kim2004 page 1 rendered from `references/kim2004/source.pdf` (pdftoppm, 300 dpi, header crop) and read.
- Per slot: printed name vs the `show` author list (or the header for the 7 header-slot papers) and `compare.csv`;
  marker run in both layers; prose statement subjects and verbs; block fields (org, unit chain, campus, city,
  country); role; locator; notes.
- All 33 distinct (paper, org, unit, city, country, role) tuples of `header_rows.csv` read (133 rows; roles primary
  123, additional 9, present address 1; basis prose 63, single 26, printed 26, grouped 12, per_author 6; all grade A).
- Address / contact scan of `headers.yaml` and the derived CSVs (contact, URL, postal-code / 3+ digit, street, road,
  boulevard, drive, suite, box, building, park, campus, phone, fax patterns, plus every street, site and box word
  printed in this batch's blocks). Hits: only the YAML key `campus` (park2007b, xie2018), the surname Park, the words
  "street address", "postal details", "web address" and "site name" in notes (types only), and digits in source ids.
  No street, building, campus site, postal code, P.O. box, mail stop, URL or contact text anywhere, notes included.
- Probes on scratch copies (`h61_audit/probes/probe.py` + `mk.py`, scratch `LIT_BASE`, batch name `lit_p61`,
  `cmd_check(..., dry_run=True)`; 28 runs). Dry-run check of the real batch: 0 errors, 0 warnings; totals equal the
  stamped derived files (105 slots, 105 recorded, 133 rows, 6 unmapped org strings). md5 of every repo batch file
  identical before and after the audit; `check_stamp.txt` matches `headers.yaml` (sha256 7416f692...). Probe checks
  wrote their usual logs under `logs/` (prefix `lit_headers_check_lit_p61`, 56 files).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h61 | 18 / 18 | 105 | 105 | 0 | 0 |

- Papers ok 17, partial 0, unreadable 1 (kim2004, 3 printed authors, 0 slots); `slots_from_header` 7 (wang2008,
  bimberg2009, park2007b, resan2005, kim2004, luo2015, barbarin2006; exactly the papers.csv rows with
  `n_authors_meta` 0, each prints the D352 line in `show`); `author_list_differs` 0; explicit slots 0; order warnings
  0; 6 unmapped org strings.
- Per paper (slots / rows): doerr2014a 3 / 3; wang2008 7 / 7; akiyama2005 8 / 18; soltanian2023 6 / 6; bimberg2009
  6 / 7; juodawlkis2009 6 / 6; park2007b 5 / 5; resan2005 3 / 4; kim2004 0 / 0; raptakis2021 11 / 21; luo2015 7 / 7;
  komatsu2021 4 / 4; fowler2023 6 / 11; poulton2018 6 / 6; barbarin2006 6 / 6; hirano2020 8 / 8; zhang2022f 9 / 10;
  xie2018 4 / 4.
- Privacy findings: 0. Notes: 1 incomplete (kim2004, F1), 1 optional precision (raptakis2021, N1).

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (105) | 105 | 0 | 0 |
| markers (printed / prose / grouped / per_author / single) | 105 | 0 | 0 |
| header position / statement subject | 105 | 0 | 0 |
| blocks (org / unit / campus / locality / country) | 105 | 0 | 0 |
| unreadable calls (1 paper) | 1 | 0 | 0 |
| present addresses (1: resan2005 #1) | 1 | 0 | 0 |
| locators | all | 0 | 0 |
| notes (18) | 16 | 2 (kim2004 F1; raptakis2021 N1) | 0 |

## Per-paper findings

- doerr2014a (3; single): Acacia Communications, Hazlet, US (street, state, postal code not recorded). Asterisk after
  Doerr = corresponding author, contact line follows. List "Christopher Richard Doerr" / "Diedrik Vermeulen" match
  the printed initials. ok.
- wang2008 (7; grouped, slots from header): call 4. ok.
- akiyama2005 (8; prose): call 2. ok.
- soltanian2023 (6; per_author): six blocks, one under each author, in both layers: Ghent University - imec + Photonics
  Research Group, Ghent, BE (5); Massachusetts Institute of Technology (MIT) + Research Laboratory of Electronics,
  Cambridge, US (Hermans). List "Günther" matches printed "Gunther". ok.
- bimberg2009 (6; printed, slots from header): 1 Technische Universitaet Berlin + Institut fuer Festkoerperphysik,
  Berlin, DE (street and postal code not recorded); 2 Technion + "Electrical Engineering Dept." as printed (unit
  before org), Haifa, IL. Markers in the PDF layer: all 1, Eisenstein 1,2 (probe BI1 without 2: 1 error); asterisk on
  Bimberg = phone / fax / contact line. ok.
- juodawlkis2009 (6; prose): "The authors are with the Lincoln Laboratory, MIT" (hyphenated across a line) =
  Massachusetts Institute of Technology + Lincoln Laboratory, Lexington, US: the committed form (4 blocks). Name list
  initials agree; typographic apostrophe in O'Donnell as printed and in the list. ok.
- park2007b (5; grouped, slots from header): call 5. ok.
- resan2005 (3; prose, slots from header): call 3. ok.
- kim2004 (unreadable): call 1; F1 (note only).
- raptakis2021 (11; prose): call 6; N1 optional.
- luo2015 (7; single, slots from header): Institute of Semiconductors, Chinese Academy of Sciences (parent part of the
  printed name) + Key Laboratory of Semiconductor Materials Science, Beijing, CN; the P.O. box and postal code not
  recorded, note says "postal details" only. Asterisk on T. Yang = contact. ok.
- komatsu2021 (4; prose): "The authors" statement; The University of Tokyo (leading article printed) + School of
  Engineering, Tokyo, JP. ok.
- fowler2023 (6; printed): call 7. ok.
- poulton2018 (6; single): Analog Photonics LLC, Boston, US ("United States" printed; street, suite, state, postal code
  not recorded). ok.
- barbarin2006 (6; single, slots from header): call 8. ok.
- hirano2020 (8; printed, cover page): call 9. ok.
- zhang2022f (9; prose): call 6. ok.
- xie2018 (4; single): call 5 (UCSB campus, USA printed: country US). Asterisk on Xie = contact. List "Komljenović"
  / "John Edward Bowers" match. ok.

## Extractor calls (verified)

1. kim2004 unreadable. Both text layers garble the header (OCR): author 2 given name (render: Shinwook), author 3
   family name run into the suffix, the conjunction, and in the only block the word "of" twice (unit and org) and the
   separator before FPCE. The page render is clean: Kyungbum Kim, Shinwook Lee, Peter J. Delfyett Jr.; one unmarked
   block: University of Central Florida, unit College of Optics and Photonics/CREOL/FPCE, Orlando, no country
   printed (state and postal code only); a phone / fax / contact line follows. Probes: K1 (status partial, single
   block with the render values, Kim readable, Lee and Delfyett unreadable): 2 errors (block first field not printed,
   md and pdf); K2 (org only, no unit): 2 errors (same). The checker verifies against the text layers only, so no
   block can be recorded and no author can get rows: unreadable is right. What a fix records today: nothing more
   than the note (F1). The extractor's note names only author 3 and the org; author 2, the unit and the conjunction
   are also garbled, the D352 slot wording is missing, and the render values are not recorded for re-recording
   (precedent: lit_h13 lischke2021a, lit_h30 hu2022, lit_h47 liu2010a "Printed (not recorded)"). F1.
   First unreadable paper without a metadata author list: `slots_from_header: true` with `authors: []` gives 0 slots,
   so its three authors appear in no compare row (O1).
2. akiyama2005: statement 1 subject = the five Fujitsu authors (1, 2, 4, 5, 6), Fujitsu Ltd. + more_orgs Fujitsu
   Laboratories Ltd. (lit_h43 QD Laser / Fujitsu Laboratories form), Atsugi, JP. "They are also with OITDA, Tokyo,
   Japan" follows a sentence end after Japan: pronoun statement for the same five authors, role additional (5 rows),
   own block P2. Statement 3: IIS, RCAST, and NCRC (unit as printed) + University of Tokyo (no article printed),
   Tokyo, JP for Sugawara, Ebe, Arakawa. Probes: A1 (Akiyama without P2) 2 errors; A2 (P2 statement not recorded at
   all) 5 errors (D361 coverage resolves the pronoun subject); A3 (P2 as present_address) 2 errors. Confirmed.
3. resan2005: statement 1 "B. Resan was with" UCF = affiliation of the work (D354), "He is now with" the Advanced
   Systems Business Unit (unit printed before the org), Coherent Inc., Santa Clara, US = present address (P2);
   statement 2 "L. Archundia and P. J. Delfyett, Jr. is with" the same UCF chain = its own block P3 (two statements,
   two blocks). Unit chain "College of Optics and Photonics/Center for Research and Education in Optics and Lasers
   (CREOL) and Florida Photonics Center of Excellence (FPCE)" contiguous with the org in both statements. Probes: R1
   (P1 present_address) 3 errors; R2 (P2 affiliation) 2 errors; R3 (Resan without P1) 4 errors; R5 (Archundia on P1)
   4 errors. Name "Peter J. Delfyett Jr." without the printed comma: R4 (comma kept) 1 error, the checker rejects
   punctuation in names; the comma-less form is also the committed form of all 7 "Jr." names in other batches (lit_h57 / h58 Osgood,
   Holmes, Stephens, do Nascimento). Confirmed.
4. wang2008: two author groups, each above its own block (grouped). Block 1 prints the centre, then "Cambridge
   University", then "Engineering Department"; recorded org Cambridge University + unit Centre for Photonic Systems,
   department not recorded. Probe W1 (unit = centre + department): 2 errors. This is the iseghem2022 gap (D442; h19
   audit C2: department printed after the org cannot be added); the note uses the iseghem2022 wording. Rows map
   `org_university_of_cambridge` by alias. Block 2 Innolume GmbH, Dortmund, DE (committed form, lit_h08 / h10). W2
   (Kovsh on G1): 3 errors. UK -> GB. Confirmed.
5. park2007b: three groups (Park / Fang / Bowers; Jones; Cohen) each above its block, in both layers. Block 1 prints
   "University of California Santa Barbara" without a comma: org University of California + `campus` Santa Barbara
   (D301; 90 committed `campus: "Santa Barbara"` blocks in other batches, 16 notes on comma-less UCSB prints, e.g. lit_h18; D449 / D461). PK4 (org with the campus
   inside, no `campus`): 0 errors, neutral; D301 form kept. Blocks 1 and 2 print only a state code and postal code,
   no country: `country: ""` right (PK1 / PK2 with US: 2 errors each). Block 3 Intel Corporation prints a site name
   between the org and Jerusalem; not stored, and the note names it by type only (round-3 F5 / D380: allowed). Block
   2 street and mail stop not recorded. PK3 (Jones on G3): 7 errors. Confirmed.
   xie2018: same comma-less UCSB print, `campus` Santa Barbara, country US (USA printed). Confirmed.
6. Clause blocks. raptakis2021 statement 3 (Groumas, Kouloumentas): ICCS block, then "and also with" Optagon
   Photonics printed without word spaces in both layers; clause block P4 after P3 (D366). zhang2022f statement 2
   (Tingge Dai): ZJU Interdisciplinary Center chain, then "and also with" Ningbo Research Institute, Zhejiang
   University, Ningbo, CN (committed form, 5 blocks). Probes: RP1 (Groumas without P4) 2 errors; RP2 (P4 without
   `clause`) 4 errors; Z1 (Dai without P3) 3 errors; Z2 (P3 without `clause`) 4 errors. raptakis2021 statements 1 and
   3 = raptakis2024 (lit_h27) form exactly: ICCS org, laboratory unit, NTUA in `more_orgs`, locality Zografou (first
   printed place, Athens second, D288). RP3 (Athens): 0 errors, neutral; precedent kept. Fraunhofer Institute for
   Telecommunications, HHI, Berlin, DE (committed form). The Optagon clause also prints two places (Agia Paraskevi,
   then Athens); the note mentions the second place only for statements 1 and 3 (N1, optional).
7. fowler2023: markers "1." / "2." before the blocks, superscripts in the PDF layer; block 1 Univ. Grenoble Alpes +
   more_orgs {CEA, unit Leti, Grenoble, FR}: the committed dict form (Université Grenoble Alpes / CEA / LETI, 2
   blocks; D367), rows CEA -> `org_cea`, UGA unmapped. Block 2 III-V Lab, Palaiseau, FR. Asterisk on Guerber =
   contact. FO1 (Krakowski on 1): 3 errors. Confirmed.
8. barbarin2006: single block COBRA Research Institute (unit) + Technische Universiteit Eindhoven, then street,
   postal code and The Netherlands: no city printed, `locality: ""` right (D288; lit_h11 TU/e empty-locality
   precedent). B1 ("Eindhoven"): 0 errors, known gap (city inside the org name accepted, D557). The web address under
   the block is named by type only in the note. Row maps `org_eindhoven_university_of_technology` (ror). Confirmed.
9. hirano2020: page 1 is a cover page (title, names without markers, DOI); the marked author line and both blocks are on
   page 2: `locator: "p.2 header"` on both blocks (D366). H1 (block 1 without the locator): 16 errors. Block 2 NICT +
   Advanced ICT Research Institute prints only the prefecture Hyogo: `locality: ""` (D288; hiraki2017 / izumisawa2026
   / sato2008). H2 ("Hyogo"): 0 errors, known gap; D288 form kept. Confirmed.

## Fixes (exact YAML edits)

F1 (apply before commit; kim2004 note, `headers.yaml` line 124; rows unchanged, status stays unreadable) -> replace
the `note` value with:

```
no author list in the literature cache (slots from the header, D352); conference paper scan, OCR text in both layers: the author line garbles author 2 (Shiuwook for the Shinwook of the page render), author 3 (family name misread and run into the suffix) and the conjunction, and the only block garbles the word of in the unit and the org and the separator before FPCE, so neither the names nor the block can be verified; nothing recorded. Printed on the page render (not recorded): Kyungbum Kim, Shinwook Lee, Peter J. Delfyett Jr.; one unmarked block for all three: University of Central Florida, College of Optics and Photonics/CREOL/FPCE, Orlando, no country printed; street address, state, postal code, phone, fax and contact line not recorded
```

N1 (optional; raptakis2021 note, line 130): replace the fragment
`statement 3 adds Optagon Photonics in an and also with clause printed without word spaces (clause block);` with

```
statement 3 adds Optagon Photonics in an and also with clause printed without word spaces (clause block), which also prints two places (Agia Paraskevi recorded, Athens in this note);
```

Probes: F1 alone (`h61_audit/probes/F1.yaml`): 0 errors, 0 warnings, 133 rows; F1 + N1
(`h61_audit/probes/F1N1.yaml`, diff against the batch = exactly lines 124 and 130): 0 errors, 0 warnings, 133 rows,
totals identical. Both files are in the session scratchpad
the session scratchpad `h61_audit/probes/`.
After applying, re-run `check lit_h61 --corpus lit` (the stamp hash changes).

No other fix: no slot, marker, block, field or privacy item is wrong.

## Observations (no YAML change)

- O1 kim2004 is the first unreadable paper with no metadata author list: with `authors: []` it contributes 0 slots,
  so its three authors exist in no compare row or extra-author list. The render names are in the F1 note; whether
  header-slot unreadable papers should list their authors as `unreadable: true` (status partial with no blocks is not
  defined by the contract) is a coordinator call.
- O2 `show` does not mask phone / fax lines (bimberg2009, kim2004; the kim2004 contact line is OCR-garbled and escapes
  the masking) or a bare web address (barbarin2006). Batch files are clean; the masking gap concerns `show` output only.
- O3 Known gaps reconfirmed: city inside the org name accepted as locality (B1), prefecture accepted as locality (H2),
  second place accepted as locality (RP3), campus inside the org accepted (PK4), department after the org not
  recordable (W1, iseghem2022 gap).

## Lists for the coordinator

- Re-record list: kim2004 (render values in the F1 note) only if the checker gains a render-verified or OCR-tolerant
  path; none otherwise.
- D412 / D426 lists: none from this batch.
- Org round (6 unmapped strings): Fujitsu Laboratories Ltd. (JP; committed lit_h08 / h10 / h43 form, still unmapped),
  NHK Science and Technology Research Laboratories, OITDA, Optagon Photonics, Technische Universitaet Berlin (unit
  Institut fuer Festkoerperphysik), Univ. Grenoble Alpes.

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 0 warnings, 133 rows | batch as written |
| F1 / F1N1 | kim2004 note / + raptakis2021 note | 0 / 0 errors, 133 rows | fix forms |
| K1 / K2 | kim2004 partial with the render block (unit + org / org only) | 2 / 2 errors | unreadable required |
| A1 / A2 / A3 | akiyama2005 Akiyama without P2 / P2 statement dropped / P2 present_address | 2 / 5 / 2 errors | pronoun statement verified |
| R1 / R2 / R3 / R5 | resan2005 P1 present_address / P2 affiliation / Resan without P1 / Archundia on P1 | 3 / 2 / 4 / 4 errors | roles and subjects verified |
| R4 | resan2005 name with the printed comma before Jr. | 1 error | comma-less form forced |
| RP1 / RP2 / RP3 | raptakis2021 Groumas without P4 / P4 not clause / locality Athens | 2 / 4 / 0 errors | clause verified; Athens neutral |
| Z1 / Z2 | zhang2022f Dai without P3 / P3 not clause | 3 / 4 errors | clause verified |
| W1 / W2 | wang2008 unit + department / Kovsh on G1 | 2 / 3 errors | iseghem2022 gap; grouping verified |
| PK1 / PK2 / PK3 / PK4 | park2007b block 1 US / block 2 US / Jones on G3 / no campus | 2 / 2 / 7 / 0 errors | empty country verified; campus neutral |
| B1 | barbarin2006 locality Eindhoven | 0 errors | gap; empty kept |
| H1 / H2 | hirano2020 block 1 without p.2 locator / locality Hyogo | 16 / 0 errors | locator verified; gap |
| BI1 | bimberg2009 Eisenstein without 2 | 1 error | marker verified |
| FO1 | fowler2023 Krakowski on 1 | 3 errors | marker verified |
