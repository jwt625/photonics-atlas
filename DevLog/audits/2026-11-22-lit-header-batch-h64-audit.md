---
title: Fresh-context audit of the lit author-affiliation batch lit_h64 (27 papers)
date: 2026-11-22
mode: read-only on the batch (wrote only this record and scratchpad show dumps / renders / probes; headers.yaml, derived files, scripts, people and registry data not edited; checker run only in dry-run on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h64/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D366, D369, D426, D466, D287, D301 from DevLog-008); format from the lit_h62 audit
verdict: GO; 154 slots audited, 154 recorded, 0 wrong rows, 0 imprecise rows; all named extractor calls confirmed; F1-F3 note wording only (no row change)
---

# Lit header batch audit: lit_h64 (2026-11-22)

## Scope

Batch lit_h64: 27 papers (Optics Express printed and single blocks, IEEE JLT / JSTQE / JQE / PTL prose footnotes, two
Photonics Journal cover-page papers, two conference papers); 154 slots, 8 papers `slots_from_header`; 196 rows.
Restricted corpus: this record names only authors, orgs, units, cities and countries; no paper text is quoted and no
contact, street, building, site, room or postal text is copied (such spans are named by type only).

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h64 --corpus lit --codes <id> --pdf`
  (all 27), plus `--pages 2` for the cover-page papers liu2019c and zhu2018; output kept in the session scratchpad
  `h64_audit/show/` only.
- guo2023a and chen2015c: page-1 header region of the local PDF rendered to PNG (scratchpad `h64_audit/png/`) and
  inspected by eye, to see what the masked lines after the blocks carry (call 2).
- Per slot: printed name vs the `show` author list (or the header for the 8 header-slot papers) and `compare.csv`;
  marker run in both layers; prose statement subjects; block fields (org, unit chain, more_orgs, campus, city,
  country); locator; notes.
- All 196 rows of `header_rows.csv` read by paper (roles primary 179, additional 17, present address 0; basis
  printed 88, prose 80, single 28; all grade A). `compare.csv`: 154 `recorded`; `order_differs` true only on the 10
  guerber2017 slots.
- Address / contact scan of `headers.yaml` and every derived file (contact, URL, 4+ digit, street, road, drive, rue,
  avenue, suite, building, room, box, plaza, campus, cedex, UMR / UMI numbers, plus every street, site, district,
  building and room token printed in this batch's blocks). Hits: years in `source_id` values and the file comment,
  the family name Dong, the stamp hash, the campus field values College Park / Davis (D301) and the type words
  "street address(es)", "postal code(s)", "building name", "room number", "site name", "UMR / UMI number" in notes.
  No contact, URL, postal code, street, site, district, building, room or box text anywhere.
- Probes on scratch copies (`h64_audit/probes/probe.py` + `mk.py`, scratch `LIT_BASE`, batch name `lit_p64`,
  `cmd_check(..., dry_run=True)`; 31 runs). Dry-run check of the batch as written: 0 errors, 3 warnings (guerber2017
  order; pitris2018 explicit slots 4 and 7); totals equal the stamped derived files (154 slots, 154 recorded, 196
  rows, 20 unmapped org strings). md5 of every repo batch file identical before and after the audit;
  `check_stamp.txt` matches `headers.yaml` (sha256 ddb4ec15...). Probe checks wrote their usual logs under `logs/`
  (prefix `lit_headers_check_lit_p64`, 62 files).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h64 | 27 / 27 | 154 | 154 | 0 | 0 |

- Papers ok 27, partial 0, unreadable 0; `slots_from_header` 8 (zou2014, yao2012, chen2015c, chen2015b,
  valicourt2015, alboresmejia2010, park2011, fan2021a; exactly the papers.csv rows with `n_authors_meta` 0, each
  prints the D352 line in `show`); `author_list_differs` 0; explicit slots 2 (pitris2018 #4, #7); order warnings 1
  (guerber2017); present addresses 0; dropped markers 2 (guo2023a #2, chen2015c #5); 20 unmapped org strings.
- Per paper (slots / rows): xiao2019 8 / 9; zou2014 4 / 5; cheng2019 7 / 7; yao2012 2 / 2; ai2024 5 / 5;
  guo2023a 3 / 4; chen2015c 6 / 8; xiao2013 8 / 10; gehl2017 6 / 6; dong2016 1 / 1; stabile2013 3 / 3;
  han2020 3 / 3; dasmahapatra2014 4 / 4; zhang2019g 10 / 10; tanaka2009a 7 / 7; chen2015b 6 / 6;
  guerber2017 10 / 29; liu2019c 3 / 3; pitris2018 9 / 14; valicourt2015 18 / 28; joo2018 3 / 3; akca2018 2 / 2;
  zhu2018 5 / 5; alboresmejia2010 11 / 11; park2011 4 / 4; stabile2016 3 / 3; fan2021a 3 / 4.
- Privacy findings: 0. Notes: 3 with a wrong factual detail (F1-F3, wording only).

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (154) | 154 | 0 | 0 |
| markers (printed / prose / single, 154) | 154 | 0 | 0 |
| header position / statement subject | 154 | 0 | 0 |
| blocks (org / unit / more_orgs / campus / locality / country) (154) | 154 | 0 | 0 |
| dropped markers (2) | 2 | 0 | 0 |
| locators | all | 0 | 0 |
| notes (27) | 24 | 0 | 3 (guo2023a, chen2015c, valicourt2015; F1-F3) |

## Per-paper findings

- xiao2019 (8; printed, capitals): block 1 unit chain copied in full (three Nanjing University units joined by
  ampersands, then the Microwave-Photonics Technology Laboratory), Nanjing, CN; block 2 University of Miami,
  Department of Physics, College of Arts and Sciences, Coral Gables, US. Markers in both layers. Probe XC (unit cut
  to the last laboratory): 2 errors. ok.
- zou2014 (4; printed, slots from header): call 4. ok.
- cheng2019 (7; single, capitals): BUPT Key Laboratory of Information Photonics and Optical Communications, Beijing,
  CN; asterisk = contact line. ok.
- yao2012 (2; single, slots from header): call 5. Unit chain (centre, state key laboratory, provincial key
  laboratory) in full. ok.
- ai2024 (5; printed, capitals): call 5. List "xiheng ai" and "M. Dagenais" match by name. ok.
- guo2023a (3; printed, capitals): call 2. Unit chains in full (Hebei University: centre, provincial centre, college;
  Southeast University: national research center, school), Baoding / Nanjing, CN. Rows right; note F1.
- chen2015c (6; printed, slots from header): call 2. Block 2 org printed without "and" between Posts and
  Telecommunications (PNG confirms); probe C2 (with "and"): 4 errors. Rows right; note F2.
- xiao2013 (8; printed): call 3. Lim on block 5 only (probe X2, Lim on 1: 3 errors). ok.
- gehl2017 (6; single, capitals, initials): Sandia National Laboratories, unit Applied Photonic Microsystems,
  Albuquerque, US; street, state and postal code not recorded; initials-only names match the full list names. ok.
- dong2016 (1; single, footnote): call 1. ok.
- stabile2013 (3; prose): call 6; P2 PhotonIC Corp., Culver City, US (leading article as printed, matcher
  normalizes). Probe S1 (Williams on P2): 4 errors. List "Abhinav Rohit" matches printed "A. Rohit". ok.
- han2020 (3; prose): call 6; P2 Université du Québec à Montréal, Microtechnology and Microsystems Laboratory,
  Montréal, CA. ok.
- dasmahapatra2014 (4; prose): call 6. ok.
- zhang2019g (10; prose): call 5; P2 Okamoto Lab, Tsukuba, JP as printed (probe O1 "Okamoto Laboratory": 4
  errors). Subject names in initials (S. J. B. Yoo) resolve to the printed author line. ok.
- tanaka2009a (7; prose): "The authors" statement, Fujitsu Laboratories Ltd., Atsugi, JP (committed form, 2 earlier
  blocks); statement words one per line in the text layer, both layers pass. ok.
- chen2015b (6; prose, slots from header): "The authors" statement; same Zhejiang University unit chain as yao2012,
  Hangzhou, CN (no campus printed here). ok.
- guerber2017 (10; printed, letters): call 3 and warning 1. ok.
- liu2019c (3; single, cover page): call / warning on cover pages. ok.
- pitris2018 (9; printed, capitals): warning 2. Blocks 1 / 2 Aristotle University of Thessaloniki with Department of
  Informatics / Center for Interdisciplinary Research and Innovation, Thessaloniki, GR; block 3 imec, Leuven, BE;
  block 4 Bright Photonics B.V., Eindhoven, NL (street address and postal code before the city not recorded); block 5
  University of Bristol, High Performance Networks Group, Bristol, GB. ok.
- valicourt2015 (18; prose, slots from header): call 3. Six statements; every subject names exactly its carriers
  (probe V3, Mestre on P1: 4 errors). Rows right; note F3.
- joo2018 (3; prose): "The authors" statement, ETRI, Daejeon, KR. ok.
- akca2018 (2; prose): P1 VU University Amsterdam, LaserLaB, Department of Physics and Astronomy, Amsterdam, NL;
  P2 Acacia Communications, Hazlet, US. List "Christopher Richard Doerr" matches. ok.
- zhu2018 (5; single, cover page): call 6 and cover pages. ok.
- alboresmejia2010 (11; prose, slots from header): "The authors" statement, Technische Universiteit Eindhoven,
  Faculteit Electrical Engineering, Eindhoven, NL; all 11 printed names in order. ok.
- park2011 (4; single, slots from header): ETRI, Daejeon, KR ("Korea" printed); street and district before the city
  not recorded. Probe K1 (district as locality): 0 errors, known gap (h60 G4, h62 W2). ok.
- stabile2016 (3; prose): call 6. ok.
- fan2021a (3; printed, slots from header): block 1 Zhejiang University unit chain (state key laboratory, centre,
  college), Hangzhou, CN; block 2 Lightip Technologies (Hangzhou), Co. Ltd., Hangzhou, CN (street and room number not
  recorded); asterisk after marker 1 on Fan = corresponding author. ok.

## Extractor calls (verified)

1. dong2016: single author; the only block is a first-page footnote statement with the singular subject "The author",
   placing him at Bell Labs, Nokia, Holmdel, US. Recorded `basis: single`, `locator: "p.1 footnote"`, org Nokia,
   unit Bell Labs: same form as lit_h46 xu2025b (single-author footnote) and lit_h06 / lit_h29 (Bell Labs printed
   before Nokia -> org Nokia, unit Bell Labs). Probe D1 (prose P1): 2 errors (singular subject not read as naming
   the author); D3 (org "Nokia Bell Labs"): 2 errors (not printed in that order); D2 (locator removed): 0 errors,
   neutral (the checker searches page 1 either way), the footnote locator is the correct description. Confirmed.
2. Contact markers: the rendered PDF of guo2023a shows marker 3 directly in front of the first contact line (an
   address line, no organization or place) and the asterisk in front of the second; chen2015c shows marker 4 in front
   of the first contact line and the asterisk in front of the second. Neither marker carries an affiliation, so
   `dropped_markers` with reason "contact footnote" is right. Probes G1 / C1 (dropped marker removed): 2 / 2 errors.
   Both notes say "second contact line": wrong order (F1, F2). Confirmed with note fixes.
3. Multi-org blocks:
   - xiao2013: blocks 2 and 4 print the parent A*STAR after Institute of Microelectronics / National Metrology Centre:
     not copied (parent rule; committed IME form). Probe X1 (parent in org): 0 errors, neutral. Block 3 joint
     unit "CINTRA CNRS/NTU/THALES" as org with the UMI number, the building name and the street not recorded; probe X3
     (CINTRA + CNRS / NTU / THALES as more_orgs): 0 errors, 199 rows, neutral; the slash form is printed as one
     name, one org is the plainer reading. Block 1 NTU, unit OPTIMUS + school (chain in full); block 5 NTU school.
   - guerber2017 block a: printed unit, dash, STMicroelectronics SAS, dash, street, postal code, city in capitals,
     country in capitals: unit TR&D, org STMicroelectronics SAS, locality "CROLLES" as printed (D366), FR. Probe B2
     (locality Grenoble): 12 errors. Block b: Centre for Nanoscience and Nanotechnology, CNRS, Univ. Paris-Sud,
     Université Paris-Saclay, then the acronym C2N, Orsay twice, Cedex, France: org = the joint unit, the three
     others in `more_orgs` (D466: IEF, C2N, INL, LTM precedent; rows map to the C2N and CNRS org ids), locality
     Orsay (second print and Cedex not recorded). Probe B1 (one more_org dropped): 0 errors, known gap (missing
     more_orgs not detected). Probe B3 (Baudot on b): 11 errors.
   - valicourt2015: P1 "Bell Labs, Alcatel-Lucent", Holmdel, US -> org Alcatel-Lucent, unit Bell Labs (same pattern
     as call 1). P2 "Alcatel-Lucent Bell Labs France", Nozay, FR kept whole (printed as one name; the same string
     is a committed lit_h02 III-V Lab more_orgs entry); probe V4 (org Alcatel-Lucent + unit "Bell Labs France"): 0 errors, 19 unmapped,
     neutral; the whole name is one printed organization name. P3 "CEA LETI", then a site name, Grenoble (Cedex and
     numbers dropped): org CEA, unit LETI (committed blocks in this form); probe V2 (org "CEA LETI"): 0 errors,
     neutral. P4 Université Européenne de Bretagne, CNRS, UMR number, Foton Laboratory, Lannion: org UEB,
     `more_orgs` CNRS + Foton Laboratory (number not copied; D285; Université de Rennes / CNRS / Institut FOTON
     precedents); probe V5 (Foton dropped): 0 errors, known gap. P5 Institut d'Electronique Fondamentale, CNRS with a
     UMR number, Université Paris-Sud, Orsay: org IEF, `more_orgs` CNRS + Université Paris-Sud (D466 IEF precedent).
     P6 III-V Lab, Palaiseau, FR, joint-laboratory parents not copied (D426; committed III-V Lab blocks in this
     form); probe V1 (parents as more_orgs): 0 errors, 205 rows, neutral.
   Confirmed.
4. zou2014 block 2: the joint institute is printed as one name ("University of Michigan and Shanghai Jiao Tong
   University Joint Institute"), Shanghai, CN; recorded whole as one org (unmapped). Probe Z1 (University of Michigan
   + "Shanghai Jiao Tong University Joint Institute" as more_orgs): 0 errors, 197 rows, neutral; splitting would
   attach Shanghai rows to the University of Michigan, so the whole-name form is the correct one. Block 1 SJTU state
   key laboratory + department chain in full. Confirmed.
5. Campus (D301): ai2024 both blocks University of Maryland, College Park -> `campus: "College Park"` (committed
   blocks in this form); zhang2019g P1 University of California, Davis -> `campus: "Davis"` (D301 example). Probes
   A1 / U1 (campus removed): 0 errors each (missing campus not detected, known gap), unmapped +2 / +1: the campus is
   required for the right mapping. yao2012 prints Zijingang Campus (a site of the same university) between the org
   and Hangzhou: not recorded, as lit_h01 / h10 / h33 / h44 / h46; probe Y1 (campus "Zijingang Campus"): 0 errors,
   +1 unmapped, would wrongly split Zhejiang University. Confirmed.
6. Unit chains copied in full: xiao2019 (four units, see above); zhu2018 page 2 (National Laboratory of Solid State
   Microstructures, College of Engineering and Applied Sciences, Key Laboratory of Intelligent Optical Sensing and
   Integration of Ministry of Education, and Collaborative Innovation Center of Advanced Microstructures, Nanjing
   University); han2020 P1 (COPL with acronym, then the département, Université Laval, Québec City, CA); stabile2013
   P1 (Department of Electrical Engineering, COBRA Research Institute, Eindhoven University of Technology);
   dasmahapatra2014 P1 (COBRA Research Centre, ECO Group, Department of Electrical Engineering, Eindhoven University
   of Technology); stabile2016 P1 (Electrical Engineering Department, COBRA Research Institute, Technische
   Universiteit Eindhoven). Each unit string equals the full printed segment between the verb / marker and the
   university (line-break hyphens joined). Confirmed.

Warnings (verified):

- guerber2017: printed order puts Baudot last (position 10); the list has him at slot 2. YAML lists printed order;
  slots matched by name (compare.csv slot 2 = Charles Baudot, block a). The text layer glues the letter markers to the
  names; the PDF layer passes. D363 warning only.
- pitris2018 #4 printed Theoni Alexoudi, list Theonitsa Alexoudi: short form of the given name, same initial,
  distinctive family name (D287); probe P1 (no slot): 2 errors (0 matches). #7 printed Ronald Broeke, list
  R.G. Broeke: distinctive family name, list adds a middle initial (D369 / D287); probe P2 (no slot): 2 errors. Both
  explicit slots required and allowed.
- Cover pages (D366): liu2019c and zhu2018 page 1 is the Photonics Journal cover (names only, no blocks); page 2
  prints the author line and the one unmarked block. `locator: "p.2 header"` on each; probes L1 / L2 (locator
  removed): 2 / 2 errors.

## Fixes (exact YAML edits)

F1 (wording; no row change; guo2023a, line 72). In the `note`, replace

```
marker 3 (author 2) has no affiliation block and points to the second contact line
```

with

```
marker 3 (author 2) has no affiliation block and points to the first contact line
```

F2 (wording; no row change; chen2015c, line 84). In the `note`, replace

```
marker 4 (author 5) has no affiliation block and points to the second contact line
```

with

```
marker 4 (author 5) has no affiliation block and points to the first contact line
```

F3 (wording; no row change; valicourt2015, line 268). The detached accents are in the university names of statements
4 and 5 (both layers), not in person names. In the `note`, replace

```
names in the statements printed with detached accents
```

with

```
university names in statements 4 and 5 printed with detached accents
```

Probe F (F1-F3 applied): 0 errors, 3 warnings, 196 rows, 20 unmapped, totals identical; the diff against the batch is
exactly these three lines (scratchpad `h64_audit/probes/F.yaml`). After applying, re-run
`uv run python scripts/ofc_headers.py check lit_h64 --corpus lit` (the stamp hash changes).

No other fix: no slot, marker, block, field, locator or other note is wrong.

## Observations (no YAML change)

- O1 Known checker gaps reconfirmed: missing `campus` not detected (A1, U1); missing `more_orgs` not detected (B1,
  V5); district accepted as locality (K1); parent text after the org accepted inside `org` (X1); a site name
  accepted as campus (Y1); single-block locator not enforced on page 1 (D2).
- O2 valicourt2015 P2 "Alcatel-Lucent Bell Labs France" and P1 Alcatel-Lucent + unit Bell Labs map to different org
  strings for the same corporate lab family; alias decisions belong to the org round.

## Lists for the coordinator

- D426 review list: none from this batch (pitris2018 slots are D287 / D369 cases, not name-order swaps).
- D412 list: none.
- Re-record list: none.
- Org round (20 unmapped strings): Alcatel-Lucent Bell Labs France (FR); Bright Photonics B.V. (NL); CINTRA
  CNRS/NTU/THALES (SG); Foton Laboratory (FR); Fujitsu Laboratories Ltd. (JP); Hebei University (CN); Institut
  d'Electronique Fondamentale (FR); Lightip Technologies (Hangzhou), Co. Ltd. (CN); National Metrology Centre (SG);
  Okamoto Lab (JP); PhotonIC Corp. (US); Univ. Paris-Sud (FR); University of Miami (US); University of Michigan and
  Shanghai Jiao Tong University Joint Institute (CN); Université Européenne de Bretagne (FR); Université
  Paris-Saclay (FR); Université Paris-Sud (FR); Université du Québec à Montréal (CA); VU University Amsterdam (NL);
  Wuhan Research Institute of Posts Telecommunications (CN). Mapped but campus-qualified: University of Maryland,
  College Park; University of California, Davis.

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 3 warnings, 196 rows | batch as written |
| F | F1-F3 notes | 0 errors, 196 rows | fix form |
| G1 / C1 | guo2023a / chen2015c dropped marker removed | 2 / 2 errors | contact markers verified |
| C2 | chen2015c org with "and" | 4 errors | as printed verified |
| D1 / D2 / D3 | dong2016 prose P1 / no locator / org "Nokia Bell Labs" | 2 / 0 / 2 errors | single form required / neutral / unit form verified |
| X1 / X2 / X3 | xiao2013 parent in org / Lim on 1 / CINTRA split | 0 / 3 / 0 errors | neutral / markers verified / neutral |
| XC | xiao2019 unit cut to last laboratory | 2 errors | full chain verified |
| B1 / B2 / B3 | guerber2017 one more_org dropped / locality Grenoble / Baudot on b | 0 / 12 / 11 errors | known gap / CROLLES verified / markers verified |
| V1 / V2 / V3 / V4 / V5 | valicourt2015 III-V parents / org "CEA LETI" / Mestre on P1 / Alcatel-Lucent + unit / Foton dropped | 0 / 0 / 4 / 0 / 0 errors | neutral / neutral / subjects verified / neutral / known gap |
| Z1 | zou2014 joint institute split | 0 errors, 197 rows | neutral; whole name kept |
| A1 / U1 / Y1 | ai2024 / zhang2019g campus removed / yao2012 campus Zijingang | 0 / 0 / 0 errors | checker gaps; D301 forms kept |
| P1 / P2 | pitris2018 slot 4 / slot 7 removed | 2 / 2 errors | explicit slots required |
| L1 / L2 | liu2019c / zhu2018 p.2 locator removed | 2 / 2 errors | cover-page locators required |
| K1 | park2011 district as locality | 0 errors | known gap |
| O1 | zhang2019g "Okamoto Laboratory" | 4 errors | as printed verified |
| S1 | stabile2013 Williams on P2 | 4 errors | subjects verified |
