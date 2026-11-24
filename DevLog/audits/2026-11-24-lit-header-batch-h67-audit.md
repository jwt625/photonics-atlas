---
title: Fresh-context audit of the lit author-affiliation batch lit_h67 (19 papers)
date: 2026-11-24
mode: read-only on the batch (wrote only this record and scratchpad show dumps / renders / probes; headers.yaml, derived files, scripts, people and registry data not edited; checker run only in dry-run or write-run on scratch copies with logs redirected to the scratchpad; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h67/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 rulings (D352-D369, D426 G1 / G6, D442, D449, D699 and the lit_h59 cheung2010 campus form; D249, D286d, D288, D301 from DevLog-008); format from the lit_h66 audit
verdict: GO after F1-F3; 149 slots audited (147 recorded + 2 no_header; dumon2004a unreadable, 7 printed authors, no slots), 0 wrong rows, 3 imprecise rows (two "at <campus>" orgs kept whole instead of the committed campus form: F1, F2), 3 notes imprecise (F1-F3); all other extractor calls confirmed
---

# Lit header batch audit: lit_h67 (2026-11-24)

## Scope

Batch lit_h67: 19 papers (Optics Express printed / single blocks, IEEE JSSC / JSTQE / JLT / PTL prose footnotes,
conference papers with grouped or single blocks, one scanned conference paper); 149 slots, 8 papers
`slots_from_header`; 158 rows. Restricted corpus: this record names only authors, orgs, units, cities and countries;
no paper text is quoted and no contact, street, building, box or postal text is copied (such spans are named by type
only).

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h67 --corpus lit --codes <id> --pdf`
  (all 19); output kept in the session scratchpad `h67_audit/show/` only.
- Page 1 rendered to PNG (pdftoppm, scratchpad `h67_audit/img/`) and the header region inspected by eye for
  dumon2004a (markers, author 6 / 7 names, both blocks), frigg2019 (lines behind markers 4 and 5), pernice2012a (Chi
  Xiong without marker), chen2006a (the "of Maryland" spacing, at 300 dpi).
- Per slot: printed name vs the `show` author list (or the header for the 8 header-slot papers) and `compare.csv`;
  marker run in both layers; prose statement subjects; block fields (org, unit chain, campus, city, country); locator;
  notes.
- All 158 rows of `header_rows.csv` read by paper (roles primary 147, additional 8, present address 3; basis printed
  67, prose 63, single 15, grouped 13; all grade A; locators p.1 header 95, p.1 footnote 63; match name 105, ror 2,
  unmapped 51). `compare.csv`: 147 `recorded`, 2 `no_header` (sun2015a #10, pernice2012a #2); `order_differs` true
  only on the 10 qiu2018a slots.
- Checker subject extraction run directly on the sun2015a text layer (`_subject`, read-only call) to see the statement
  1 subject the text layer yields.
- Address / contact scan of `headers.yaml` and every derived file (contact sign, URL, 3+ digit numbers, street,
  strasse, straat, road, rue, avenue, drive, suite, building, Bldg, room, box, P.O. box, cedex, e-mail, phone, ORCID,
  every street token printed in this batch's blocks, US state + postal patterns, UK postcode fragments). Hits only:
  the file-comment contract paths / extraction date, and type words in notes ("street address(es)", "postal
  code(s)", "postal boxes", "contact line(s)", "ORCID glyphs"). No contact, URL, postal code, street, building or box
  text anywhere, notes included; the dumon2004a note lists names, markers, org / unit / city / country only.
- Probes on scratch copies (`h67_audit/probes/probe.py` + `mk.py`, scratch `LIT_BASE`, batch names `p67_*`,
  `RunLog` log_dir in the scratchpad, base wiped per run; 33 dry runs + 4 write runs). Dry-run check of the batch as
  written: 0 errors, 1 warning (qiu2018a order, D363). The scratch write-run of the batch as written produces
  byte-identical `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`; `check_stamp.txt` matches `headers.yaml`
  (sha256 adf84968...). md5 of every repo batch file identical before and after the audit; no file written under
  `logs/`.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h67 | 19 / 19 | 149 | 146 | 3 | 0 |

- Papers ok 16, partial 2 (sun2015a, pernice2012a), unreadable 1 (dumon2004a); `slots_from_header` 8 (orcutt2011,
  dumon2004a, tsuchizawa2003, evans2015, tien2011, chen2006a, pernice2012a, wu2015; exactly the papers.csv rows with
  `n_authors_meta` 0, each prints the D352 line in `show`); `author_list_differs` 0; explicit slots 0; order warnings
  1 (qiu2018a); present addresses 3 (orcutt2011 blocks 4 / 5, chrysostomidis2025 P3); dropped markers 4
  (cardenas2009 #3 marker 2, pernice2012a #1 marker 2, frigg2019 #1 marker 4, #7 marker 5); unreadable authors 2;
  17 unmapped org strings (15 after F1 / F2).
- Per paper (slots / rows): sun2015a 22 / 22; orcutt2011 12 / 17; cardenas2009 6 / 6; dumon2004a 0 / 0 (7 printed);
  bucio2019 10 / 10; chrysostomidis2025 8 / 9; frigg2019 7 / 8; tsuchizawa2003 9 / 9; evans2015 3 / 5; qiu2018a
  10 / 10; tien2011 6 / 6; puckett2019 7 / 7; samusenko2016 7 / 8; zhuang2011 6 / 6; chen2006a 13 / 13; jin2017
  7 / 7; pernice2012a 3 / 2; wu2015 9 / 9; siew2015 4 / 4.
- Privacy findings: 0.

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (149) | 149 | 0 | 0 |
| markers (printed / prose / single / grouped, 147 readable + 2 unreadable) | 149 | 0 | 0 |
| header position / statement subject | 149 | 0 | 0 |
| blocks (org / unit / campus / locality / country) (147 recorded) | 144 | 3 (sun2015a #1 P2 and #22, orcutt2011 #4 block 5: org kept whole instead of org + campus; F1, F2) | 0 |
| dropped markers (4) | 4 | 0 | 0 |
| locators | all | 0 | 0 |
| notes (19) | 16 | 3 (sun2015a, orcutt2011, chen2006a; F1-F3) | 0 |

## Per-paper findings

- sun2015a (22; prose, partial): five statements, subjects verified name by name in the PDF layer: P1 MIT, Department
  of Electrical Engineering and Computer Science, Cambridge, US (11 authors incl. Sun and Timurdogan); P2 University
  of California at Berkeley, same unit name, Berkeley, US (Sun, Stojanović); P3 University of Colorado, campus
  Boulder, Department of Electrical, Computer, and Energy Engineering, Boulder, US (Shainline, Wade, Nammari,
  Popović); P4 Micron Semiconductor Israel, Kiryat Gat, IL; P5 Micron Technology, Inc., Boise, US. Call 1. P2 form:
  F1.
- orcutt2011 (12; printed, slots from header): blocks 1 / 2 MIT (Research Laboratory of Electronics; Microsystems
  Technology Laboratories), Cambridge, US; block 3 Texas Instruments, Dallas, US; blocks 4 / 5 present addresses
  (cue Currently with) of Holzwarth (University of Canterbury, Christchurch, NZ) and Popović (University of Colorado at
  Boulder, Boulder, US). Marker runs match both layers (Orcutt 1, 2 plus asterisk; Ram 1, 2). Call 6 (units with
  "the") confirmed; block 5 org form: F2.
- cardenas2009 (6; printed): block 1 Cornell University, Department of Electrical and Computer Engineering, Ithaca,
  country "" (only the state printed; probe C3 with US: 2 errors). Call 3 confirmed.
- dumon2004a (unreadable, slots from header): call 2 confirmed.
- bucio2019 (10; prose): P1 University of Southampton, Optoelectronics Research Centre, Southampton, GB (Bucio,
  Lacava, Skandalos, Petropoulos, Gardes); P2 Università degli Studi di Pavia, Dipartimento di Fisica, Pavia, IT
  (Clementi, Galli); P3 University of Exeter, EPSRC Centre for Doctoral Training, Exeter, GB (Faneca, Baldycheva);
  P4 Indian Institute of Technology Kharagpur (one printed name, no comma; committed form), Department of Electronics
  and Electrical Communication Engineering, Kharagpur, IN (Debnath). List forms with accents / middle initials match
  by name. ok.
- chrysostomidis2025 (8; prose): call 10. P4 Lumiphase, Zürich, CH; P5 Ligentec SA, Ecublens, CH (the CH-prefixed
  postal code not recorded); P6 Aristotle University of Thessaloniki, Computer Science Department and Center for
  Interdisciplinary Research and Innovation, Thessaloniki, GR. ok.
- frigg2019 (7; printed, capitals): call 8. Block 1 RMIT University, School of Engineering, Integrated Photonics and
  Applications Centre, Melbourne, AU; block 2 Australian National University, Research School of Physics and
  Engineering, Canberra, AU; block 3 Evatec Ltd., Trübbach, CH (street and postal code not recorded). ok.
- tsuchizawa2003 (9; single, slots from header): NTT Microsystem Integration Laboratories, Atsugi-shi (D366 form), JP;
  names printed initial + family name without a space, matched. Probe TS1 (Atsugi): 0 errors (prefix match, neutral;
  D366 keeps the printed form). ok.
- evans2015 (3; printed, slots from header): four Cornell University blocks with their units (Kavli Institute at
  Cornell for Nanoscale Science; Laboratory for Atomic and Solid State Physics; School of Applied and Engineering
  Physics; Materials Science and Engineering Department), Ithaca, US. Marker runs 1, 2 / 3 / 1, 4 in both layers. ok.
- qiu2018a (10; prose): calls 5 and 9. Statement 2 (Hu, Y. Zhang, Xiao): Wuhan Research Institute of Posts
  Telecommunications (as printed; committed lit form, 4 blocks), unit State Key Laboratory of Optical Communication
  Technologies and Networks, Wuhan, CN. Header Xiao Hu vs list Xiao Ying Hu matched by name; Xinliang Zhang (slot 2)
  vs Yuguang Zhang (slot 7) resolved correctly. ok.
- tien2011 (6; single, slots from header): University of California, campus Santa Barbara, Department of Electrical
  and Computer Engineering, Santa Barbara, US. ok.
- puckett2019 (7; printed): block 1 Honeywell International with only the country printed, locality "", US; block 2
  UC campus Santa Barbara, same unit, Santa Barbara, US. List Karl D. Nelson matches. ok.
- samusenko2016 (7; prose): P1 University of Trento, Nanoscience Laboratory, Department of Physics, Trento, IT + clause
  P2 Fondazione Bruno Kessler, Centre for Materials and Microsystems, Trento, IT (Samusenko); P3 the "were with"
  statement (Gandolfi, Chalyan, Guider, Pavesi), same Trento block, affiliation of the work (D354); P4 Fondazione
  Bruno Kessler (Pucker, Ghulinyan; printed with a leading article, recorded without: probe S2 neutral, majority
  prose form). Probe S1 (clause dropped): 2 errors (coverage works here). ok.
- zhuang2011 (6; printed): University of Twente, Telecommunication Engineering group, Enschede, NL; LioniX BV,
  Enschede, NL (postal boxes and codes printed between org and city, not recorded). ok.
- chen2006a (13; grouped, slots from header): call 7; note F3.
- jin2017 (7; printed, initials): block 1 UC campus Santa Barbara (the printed UCSB acronym after the campus not
  recorded, committed UCSB form); block 2 U.S. Army Research Laboratory, Adelphi, US; block 3 Keysight Technologies
  with unit Keysight Laboratories (printed lab-before-company order; HPE / vaerenbergh2021 form), Santa Clara, US;
  block 4 Morton Photonics, West Friendship, US. Asterisk printed before W. Jin's marker 1 (symbol, no entry). ok.
- pernice2012a (3; printed, slots from header, partial): call 4 confirmed.
- wu2015 (9; printed, slots from header): National Sun Yat-sen University, Department of Photonics, Kaohsiung, TW;
  National Taiwan University, Graduate Institute of Photonics and Optoelectronics, Taipei, TW. Yi-Jen Chiu hyphenated
  across the line passes in both layers. ok.
- siew2015 (4; prose): "The authors" statement (one word per line in both layers), National University of Singapore,
  Department of Electrical and Computer Engineering, Singapore, SG. List Soham Saha matches printed Soham S. Saha. ok.

## Extractor calls (verified)

1. sun2015a partial. Author 10 is named "E. Timur-" / "dogan" across a line in statement 1 in both layers (D426 G1).
   Probe T1 (Timurdogan readable): 3 errors (PDF layer: not named in the subject). Probe T2 (unreadable with markers
   []): 0 errors, neutral; carrying P1 is the D366 (8) form. Statement-1 text-layer gap confirmed: the funding
   paragraph ends with a mixed-case word + period + line break, which `PROSE_CUT_RE` does not treat as a boundary
   (only all-caps or lower-case words before ". "), so the text-layer subject starts several sentences earlier and
   contains "of the authors"; the text layer then reads statement 1 as an "all authors" statement (T1 / T3 / T4 text
   errors "statement names all authors"). The PDF layer has a blank line there and verifies all five statements;
   probes T3 (Mehta moved to P3) and T4 (Sun without P2) fail on the PDF layer, so the batch is checked. New checker
   gap (O1). Confirmed.
2. dumon2004a unreadable. Text and PDF layers are the same OCR: markers 1 / 2 read as apostrophe or "l", block 1
   marker lost, author 6 printed "Beck'" and author 7 "Roe1 Baed". The page render shows Pieter Dumon 1, Wim Bogaerts
   1, Joris Van Campenhout 1, Vincent Wiaux 2, Johan Wouters 2, Stephan Beckx 2, Roel Baets 1; block 1 Ghent University
   – IMEC, Dept. of Information Technology, Gent, BELGIUM; block 2 IMEC vzw, Silicon Process Technology Division,
   Leuven, BELGIUM: the note's values match the render exactly and carry no street, postal or contact text.
   Lookalikes are not folded (D286d), so unreadable with values in the note is right (committed unreadable +
   slots_from_header precedents exist). Confirmed.
3. cardenas2009 #3 marker 2 ("Current Address" block, Harvard University, Cambridge, no country printed) in
   `dropped_markers` with the committed reason string (13 earlier uses), paper ok: zamek2011 / li2018 / D442
   precedent. Probe C1 (dropped marker removed): 2 errors; probe C2 (recorded as present address): 2 errors (cue not
   recognized). Confirmed; re-record list.
4. pernice2012a partial. The page render shows Chi Xiong with no marker; no unmarked block exists, so no D286f layout
   reading; unreadable (committed wording reused). Probe P1 (Xiong with marker 1): 3 errors. Author 1 marker 2 ("Current
   address" block: Institute of Nanotechnology, Karlsruhe Institute of Technology, Eggenstein-Leopoldshafen,
   Germany) dropped: probe P2 (not dropped): 2 errors; P3 (recorded as present address): 2 errors. Confirmed;
   re-record list.
5. qiu2018a order warning: Xinliang Zhang is printed last; the list has him second. Authors listed in printed order
   (D363). Probe Q2 (YAML reordered to list order): 0 errors and 0 warnings, i.e. the checker does not verify the YAML
   order of a prose paper against the printed author line (O2); the batch order is the printed one. Confirmed.
6. orcutt2011 present-address units "the Department of Electrical Engineering". Probe O1 (article removed): 6 errors
   (blocks 4 / 5 not found after their markers; block 3 runs into the cue): the unit-first block search needs the
   printed article here. Committed precedent lit_h49 patel2014 "the Dept. of ..." and lit_h09 "the Physical
   Measurement Laboratory". Probe O3 (block 4 role affiliation): 2 errors. Confirmed.
7. chen2006a grouped. Authors 1-11 printed above the Nomadics Inc block, 12-13 above the UMBC block (D368, chosen by
   layout); G1 Nomadics Inc, unit Little Optics Division, Annapolis Junction; G2 University of Maryland Baltimore
   County, unit CSEE Dept, Baltimore; both country "" (only the state printed; probe CH2 with US: 2 errors). Probe CH3
   (Jiao on G1): 2 errors. The org is one printed name without a comma, so no D301 campus split (the only committed
   occurrence is the same form). The 300-dpi render shows a narrow but present space between "of" and "Maryland"; only
   the text and PDF layers join them. Recording it with the space is right (D282: intended letters; probe CH1 joined
   form also 0 errors), but the note says the block prints no space: F3.
8. frigg2019: the render shows lines 4 and 5 under block 3 are two contact lines, no organization or place; markers 4
   (Frigg) and 5 (Mitchell) in `dropped_markers` "contact footnote" are right. Probe FR1 (Frigg marker 4 not dropped):
   2 errors. Probe FR2 (Mitchell marker 5 not dropped): 0 errors (known gap: the last author's extra marker is not
   checked, chang2020 Lipson). Confirmed.
9. qiu2018a P1: Huazhong University of Science and Technology as org, Wuhan National Laboratory for Optoelectronics as
   unit, the committed majority form (8 identical blocks, 40+ HUST blocks with WNLO-led unit chains). Probe Q1 (WNLO as
   org + HUST as more_orgs): 0 errors, neutral. Confirmed.
10. chrysostomidis2025 author 2: "was with" statement (P2, Aristotle University block, role affiliation) followed by the
    pronoun statement "He is now with" OneTouch Technology BV, Gent, BE (P3, `present_address`). Probe CR1 (P3
    removed): 2 errors (D361 coverage). Probe CR2 (P3 role affiliation): 2 errors. P1 and P2 are two blocks for the
    same printed org (two statements, D354). Confirmed.
11. "at <campus>" orgs: the extractor kept "University of California at Berkeley" (sun2015a P2) and "University of
    Colorado at Boulder" (orcutt2011 block 5) whole, citing the OFC pilot "University of California at Davis". The lit
    corpus ruled the other way: lit_h59 cheung2010 (audit 2026-11-20) records "University of California at Davis" as
    org University of California + campus Davis, and the committed lit blocks are 95 / 20 / 15 / 10 / 9 campus forms
    (Santa Barbara / Davis / Boulder / San Diego / Berkeley) against 1 whole "at" form each (OFC pilot only for Davis).
    The same paper (sun2015a P3) already uses campus Boulder. Kept whole, the 3 rows are unmapped; with the campus form
    they map to org_university_of_california_berkeley (2 rows) and org_university_of_colorado_boulder (1 row). Probes
    F1 / F2 / F12: 0 errors, 1 warning. Probe T5 (org University of California without campus): 0 errors (known gap:
    missing campus not detected). Not confirmed: F1, F2.

## Fixes (exact YAML edits)

F1 (precision; 2 rows remapped; sun2015a, lines 6 and 9). Line 9, replace

```
org: "University of California at Berkeley", unit
```

with

```
org: "University of California", campus: "Berkeley", unit
```

In the line 6 `note`, replace

```
statement 2 prints University of California at Berkeley (kept whole, as the OFC pilot University of California at Davis)
```

with

```
statement 2 prints University of California at Berkeley (campus Berkeley, D301; lit_h59 cheung2010 form)
```

F2 (precision; 1 row remapped; orcutt2011, lines 40 and 46). Line 46, replace

```
org: "University of Colorado at Boulder", unit
```

with

```
org: "University of Colorado", campus: "Boulder", unit
```

In the line 40 `note`, replace

```
block 5 prints University of Colorado at Boulder (kept whole) before the city Boulder
```

with

```
block 5 prints University of Colorado at Boulder before the city Boulder (campus Boulder, D301; lit_h59 cheung2010 form)
```

F3 (note only; no row change; chen2006a, line 249). In the `note`, replace

```
block 2 prints University of Maryland Baltimore County with no space after of
```

with

```
block 2: both text layers join of and Maryland in University of Maryland Baltimore County, the page render prints the space (recorded with it)
```

Probe FALL (F1-F3 applied, scratchpad `h67_audit/probes/y/FALL.yaml`): 0 errors, 1 warning (qiu2018a order), 158
rows. Against the stamped derived files exactly three `header_rows.csv` lines change (sun2015a #1 P2, sun2015a #22,
orcutt2011 #4 block 5: org name "University of California, Berkeley" / "University of Colorado, Boulder", match
`name`), two `compare.csv` lines gain the Berkeley org id, and `unmapped_orgs.csv` loses the two "at" strings (17 -> 15).
F1 + F2 alone (probe F12) give byte-identical derived files to FALL. After applying, re-run
`uv run python scripts/ofc_headers.py check lit_h67 --corpus lit` (the stamp hash changes).

No other fix: no slot, marker, other block, field, locator or other note is wrong.

## Observations (no YAML change)

- O1 New checker gap, prose sentence boundary: `PROSE_CUT_RE` does not cut after a mixed-case word + period ("...
  Government." then a line break), so a statement that follows a funding paragraph inherits its sentences; if those
  contain "the authors" the text layer reads an all-authors statement. sun2015a passes only via the PDF layer (blank
  line). Suggest a cut at ". " + line break before an initial-dot-name pattern, with a test.
- O2 Checker gap, author order in prose papers: probe Q2 (qiu2018a YAML reordered to the list order) passes with 0
  errors and 0 warnings; the printed order is not verified against the author line. The batch uses the printed order.
- O3 Known gaps reconfirmed: last author's extra marker not checked (FR2); missing `campus` accepted (T5, J1); org
  word accepted as locality (PU1: puckett2019 block 1 locality "Honeywell", 0 errors); city prefix accepted (TS1);
  hyphenated subject name (G1, sun2015a); "Current address" cue (cardenas2009, pernice2012a, D442).
- O4 samusenko2016 P4 and other prose blocks drop the grammatical "the" before org / unit while orcutt2011 keeps it in
  printed present-address units; both are the committed forms and both are forced or neutral in the checker (O1 probe:
  required in orcutt; S2: neutral in samusenko). No change.

## Lists for the coordinator

- D412 list: none. D426 review list: none.
- Re-record list: sun2015a #10 Erman Timurdogan (P1) once hyphenated subject names are joined (G1); cardenas2009 #3
  present address (Department of Chemistry and Chemical Biology, Harvard University, Cambridge, country "") and
  pernice2012a #1 present address (Institute of Nanotechnology, Karlsruhe Institute of Technology,
  Eggenstein-Leopoldshafen, DE) once the "Current address" cue is supported (D442); dumon2004a if an OCR-tolerant
  marker reading is ever ruled in (values in the note).
- Org round (15 unmapped strings after F1 / F2): Australian National University (AU; committed blocks print both this
  form and "The Australian National University"); Fondazione Bruno Kessler (IT); Honeywell International (US); LioniX BV (NL);
  Micron Semiconductor Israel (IL); Morton Photonics (US); NTT Microsystem Integration Laboratories (JP); Nomadics Inc
  (no country printed); OneTouch Technology BV (BE); RMIT University (AU); U.S. Army Research Laboratory (US);
  University of Canterbury (NZ); University of Exeter (GB); University of Maryland Baltimore County (no country
  printed); Wuhan Research Institute of Posts Telecommunications (CN, misprinted name as printed, alias to the WRI
  org).

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 1 warning, 158 rows; write-run byte-identical | batch as written |
| F1 / F2 / F12 / FALL | fixes | 0 errors, 1 warning; 3 rows remapped | fix form |
| T1 / T2 | sun2015a Timurdogan readable / markers [] | 3 / 0 errors | G1 verified / neutral |
| T3 / T4 | Mehta moved to P3 / Sun without P2 | 4 / 3 errors (PDF layer catches) | statements verified; text-layer gap (O1) |
| T5 / J1 | campus removed (UC Berkeley org / jin2017) | 0 / 0 errors | known gap |
| O1 / O2 / O3 | orcutt units without "the" / block 4 dropped / block 4 role affiliation | 6 / 2 / 2 errors | article required; cue verified |
| C1 / C2 / C3 | cardenas marker kept / present address recorded / country US | 2 / 2 / 2 errors | call 3 verified |
| P1 / P2 / P3 | pernice Xiong marker 1 / marker 2 kept / present address recorded | 3 / 2 / 2 errors | call 4 verified |
| FR1 / FR2 | frigg contact markers not dropped (Frigg / Mitchell) | 2 / 0 errors | verified / known gap |
| CR1 / CR2 | chrysostomidis P3 removed / role affiliation | 2 / 2 errors | call 10 verified |
| Q1 / Q2 | qiu2018a WNLO as org / list order | 0 / 0 errors (0 warnings) | neutral / order gap (O2) |
| S1 / S2 | samusenko clause dropped / org with article | 2 / 0 errors | coverage works / neutral |
| CH1 / CH2 / CH3 | chen2006a joined "ofMaryland" / country US / Jiao on G1 | 0 / 2 / 2 errors | neutral / verified / verified |
| PU1 / TS1 | puckett locality Honeywell / tsuchizawa Atsugi | 0 / 0 errors | known gap / neutral |
