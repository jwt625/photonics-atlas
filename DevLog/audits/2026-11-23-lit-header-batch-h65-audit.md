---
title: Fresh-context audit of the lit author-affiliation batch lit_h65 (27 papers)
date: 2026-11-23
mode: read-only on the batch (wrote only this record and scratchpad show dumps / one render crop / probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only with --dry-run on the batch, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h65/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D282, D286f, D287, D301, D302, D361, D366, D369, D380, D410, D412, D416, D426, D442, D449, D522, D565, D727); format from the lit_h63 audit; precedents lit_h30 lai2025, lit_h39 li2018, lit_h45 F1, lit_h60 zheng2023a
verdict: GO with F1 (koos2007 author 3 readable: the skip_between record passes and is complete, status partial -> ok, +1 row) and F2-F4 (privacy wording in three notes: two campus site names, one abbreviated postal-box wording); 172 slots audited, 171 recorded, 1 without rows (koos2007 #3, F1), 0 wrong rows, 3 imprecise slots (koos2007 #3 F1; su2022 #5 and schall2016 #3 checker gaps, no YAML fix); all other extractor calls confirmed; optional N1 (schall2016 note values)
---

# Lit header batch audit: lit_h65 (2026-11-23)

## Scope

Batch lit_h65: 27 papers (IEEE JLT / PTL prose footnotes, four IEEE Photonics Journal papers with a cover page 1,
Optics Express printed / single blocks, one IEEE conference paper, two other conference-style headers); 172 slots, 8
papers `slots_from_header`; 187 rows. Restricted corpus: this record names only authors, orgs, units, cities and
countries; no paper text is quoted and no contact, street, building, campus site, postal or box text is copied (such
spans are named by type only; the koos2007 secretariat code is referred to as such).

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h65 --corpus lit --codes <id> --pdf`
  (all 27), plus `--pages 2 2` for bogaerts2011, prost2019, chen2021c, hao2019 (cover page 1); output kept in the
  session scratchpad `h65_audit/show/` only.
- Page render viewed for bogaerts2011 p.2 (header crop, scratchpad `h65_audit/img/`): the joint org prints an em dash
  between the university and IMEC.
- Per slot: printed name vs the `show` author list (or the header for the 8 header-slot papers) and `compare.csv`;
  marker run in both layers; prose statement subjects; block fields (org, unit chain, more_orgs, campus, city,
  country); basis; locator; notes.
- All 187 rows of `header_rows.csv` read by paper (primary 173, additional 14; basis prose 90, printed 66, single 31;
  grade A 187). `compare.csv`: 171 `recorded`, 1 `no_header`.
- Address / contact scan of `headers.yaml` and the three derived CSVs (contact, URL, 4+ digit, street, avenue, road,
  drive, suite, building, campus, box, P.O., cedex, plus every street, campus-site and secretariat token printed in
  this batch's blocks). Derived CSVs: no hit (the secretariat code is absent from every derived file). headers.yaml:
  line 127 `skip_between` holding the secretariat code (call 1); notes naming a campus site (line 81 yu2016a, line 159 blascosolvas2024;
  F2, F3); the abbreviated postal-box wording in a note (line 230 malik2014; F4); type words "street" / "campus" (prost2019 campus Davis is
  a D301 campus, not a site) otherwise. No e-mail word in any note. The IEEE institutional download stamp printed
  at the foot of the IEEE pages appears in no field, note or derived row.
- Probes on scratch copies (`h65_audit/probes/probe.py`, scratch `LIT_BASE`, batch name `lit_p65`,
  `cmd_check(..., dry_run=True)`; 29 runs). Dry-run check of the real batch: 0 errors, 1 warning (blascosolvas2024
  explicit slot 7); totals equal the stamped derived files (172 slots, 171 recorded, 187 rows, 17 unmapped org
  strings). md5 of every repo batch file identical before and after the audit; `check_stamp.txt` matches
  `headers.yaml` (sha256 7e0f9ee2...). Probe checks wrote their usual logs under `logs/` (prefix
  `lit_headers_check_lit_p65`).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h65 | 27 / 27 | 172 | 169 | 3 (koos2007 #3 F1; su2022 #5 D369 gap; schall2016 #3 current-address gap) | 0 |

- Papers ok 26, partial 1 (koos2007; ok after F1), unreadable 0. `slots_from_header` 8 (exactly the papers.csv rows
  with `n_authors_meta` 0; each note carries the D352 line).
- Slots without rows 1: koos2007 #3 Zimmermann (unreadable, F1). `author_list_differs` 0; explicit slots 1
  (blascosolvas2024 #7); order warnings 0; present addresses 0; 17 unmapped org strings.
- Per paper (slots / rows): bogaerts2011 2 / 4; schall2016 9 / 9; luyssaert2005 5 / 5; gao2021a 7 / 7; acoleyen2011b
  2 / 2; atabaki2010 5 / 5; yu2016a 5 / 6; lin2022c 9 / 9; song2016a 5 / 5; koos2007 6 / 5; su2022 11 / 11;
  blascosolvas2024 8 / 8; pruessner2007 4 / 4; lin2024 6 / 6; ahmad2002 6 / 6; prost2019 8 / 8; malik2014 11 / 19;
  steckler2024 6 / 7; lischke2019 19 / 20; yan2018 9 / 9; hao2019 8 / 8; gupta2017 3 / 3; morino2014 3 / 3;
  abuelmaaty2018 5 / 6; guo2024a 4 / 4; chen2021c 4 / 6; zhang2015a 2 / 2.
- Privacy findings: 3 note wordings (F2-F4), 0 in fields or derived files. Notes: 1 with a wrong reason (koos2007,
  F1), 1 with incomplete re-record values (schall2016, N1).

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (172) | 171 | 1 (su2022 #5, D369 checker gap) | 0 |
| markers (printed / prose / single; 171 readable + 1 unreadable) | 170 | 2 (koos2007 #3 F1; schall2016 #3 dropped current-address marker, known gap) | 0 |
| header position / statement subject | 172 | 0 | 0 |
| blocks (org / unit / more_orgs / campus / locality / country) | 172 | 0 | 0 |
| basis / grade | 172 | 0 | 0 |
| locators | all | 0 | 0 |
| notes (27) | 22 | 1 (schall2016, N1) | 4 (koos2007 reason F1; yu2016a F3, blascosolvas2024 F2, malik2014 F4 privacy wording) |

## Per-paper findings

- bogaerts2011 (2; single, slots from header, p.2): call 2. ok.
- schall2016 (9; printed): block 1 unit AMICA before AMO GmbH, Aachen, DE (street, postal code not recorded); markers
  1,* / 1 / 1,2 / 1 ... verified in the PDF layer; list "Abhay Abhimanyu Sagade" and "H. Kurz" match. Call 5; N1.
- luyssaert2005 (5; prose, slots from header): "The authors" statement, Photonics Research Group, Department of
  Information Technology (INTEC), Ghent University-IMEC (hyphen as printed, D416 / D426), Gent, BE. ok.
- gao2021a (7; prose): "The authors" statement, Advanced Micro Foundry Pte. Ltd., Singapore, SG (maps to `org_amf`);
  list full names match the initials. ok.
- acoleyen2011b (2; single, slots from header): conference header, unit lines then "Ghent University - imec, Belgium",
  no city: locality "" (call 6). Probe A1 (locality Ghent): 0 errors only because Ghent is inside the org name (gap
  O1). ok.
- atabaki2010 (5; single): Georgia Institute of Technology, School of ECE, Atlanta, US; all five list names are
  full forms of the printed initials. ok.
- yu2016a (5; printed, capitals): call 6; F3.
- lin2022c (9; prose): "The authors" statement, Advanced Photonics Center, Southeast University, Nanjing, CN. ok.
- song2016a (5; prose): "The authors" statement, imec, Leuven, BE. ok.
- koos2007 (6; prose, partial, slots from header): call 1; F1.
- su2022 (11; prose): four statements; P1 unit "Graduate Institute of Photonics and Optoelectronics and the
  Department of Electrical Engineering" (hyphenated line break joined), National Taiwan University, Taipei, TW; P2
  Graduate Institute of Electronics Engineering, NTU; P3 RCAST, University of Tokyo, Tokyo, JP; P4 Department of
  Electronic Engineering, National Kaohsiung University of Applied Sciences, Kaohsiung, TW. Subjects verified
  (probe SU1, Chih-Hsien Cheng on P1: 5 errors). Call 3.
- blascosolvas2024 (8; prose): call 4; F2.
- pruessner2007 (4; single): Naval Research Laboratory (NRL), Washington, "D.C." and postal code, no country: locality
  Washington, country "" (probes PR1 country US: 2 errors; PR2 locality "Washington, D.C.": 1 error, city only).
  Asterisk = contact line. ok.
- lin2024 (6; prose, one word per line in the text layer): Jiangsu Key Laboratory on Opto-Electronic Technology,
  School of Computer and Electronic Information, Nanjing Normal University, Nanjing, CN. ok.
- ahmad2002 (6; prose, slots from header): "The authors" statement, Microelectronics Sciences Laboratories, Columbia
  University, New York, US (state, postal code not recorded); "R. M. Osgood, Jr." recorded "R. M. Osgood Jr." (suffix
  dropped from the person key, lit_h22 hossain2026). ok.
- prost2019 (8; single, p.2): call 6. ok.
- malik2014 (11; printed, slots from header): five blocks and markers verified in the PDF layer (1,2,* / 1,2 / 1,2 /
  1,2,3 / 4,5 / 4 x5 / 1,2,3); block 1 Ghent University-imec (D416), Photonics Research Group, Ghent; block 2 Center
  for Nano- and Biophotonics, Ghent University, Belgium only (locality "", call 6; probe M1: 0 errors, gap O1);
  block 3 COBRA Research Institute, Eindhoven University of Technology, Eindhoven, NL (a postal box and postal code
  between org and city not recorded); block 4 imec, Leuven; block 5 Instituut voor Kern- en Stralingsfysica, KU
  Leuven, Leuven. Fields ok; F4.
- steckler2024 (6; prose): statement 1 IHP-Leibniz Institut für Innovative Mikroelektronik, Frankfurt (Oder), DE;
  statement 2 FG Silizium-Photonik, Technische Universität Berlin, Berlin, DE; statement 3 Zimmermann IHP plus the
  "and also with" clause (P4, D366). Probe ST1 (clause omitted): 0 errors (gap O2), so the clause is verified only
  positively; it is printed. ok.
- lischke2019 (19; printed): call 6. ok.
- yan2018 (9; prose): WNLO unit of HUST, Wuhan; SKL unit of Sun Yat-sen University, Guangzhou; Department of
  Photonics Engineering, DTU, Kongens Lyngby, DK. Subjects verified. ok.
- hao2019 (8; single, p.2): four-unit chain (MOE key laboratory, NLSSM, college and institute) of Nanjing University,
  Nanjing, CN, province not recorded. ok.
- gupta2017 (3; prose): Department of Electrical Engineering, Indian Institute of Technology Madras, Chennai, IN
  (hyphenated "In- stitute" joined). ok.
- morino2014 (3; prose, slots from header): Graduate School of Natural Science and Technology, Kanazawa University,
  Kanazawa, JP. ok.
- abuelmaaty2018 (5; printed, slots from header): call 6. Blocks: E-JUST (acronym in parentheses kept), Alexandria,
  EG; Alexandria University EE Department, Alexandria, EG; Kyushu University with the abbreviated unit as printed,
  Fukuoka, JP. ok.
- guo2024a (4; prose): Fuzhou University unit chain, Fuzhou; Hebei University chain, Baoding, CN. ok.
- chen2021c (4; printed, p.2): markers 1,2 / 1,2 / 3 / 3 in the PDF layer; Nanjing University x2 (NLSSM + college;
  Collaborative Innovation Center), ShanghaiTech University, Shanghai, CN. ok.
- zhang2015a (2; prose): Microwave Photonics Research Laboratory, School of EECS, University of Ottawa, Ottawa, CA. ok.

## Extractor calls (verified)

1. koos2007 partial: outcome NOT confirmed; record form confirmed (F1).
   - Text and PDF layers print Zimmermann's statement one word per line: unit "Fachgebiet
     Hochfrequenztechnik/Photonik", then the TU Berlin secretariat code, then Technical University Berlin, postal
     code, Berlin, Germany. The other two statements verified (Karlsruhe IHQ, DE; Erlangen MPRG, postal code then
     Erlangen, no country: Poulton block country "" is right, probe KP1 country DE: 2 errors).
   - Probes: K2 (no skip_between): 2 errors (unit and org not contiguous); K3 (org only): 4 errors (D354 first field,
     D361 coverage); K4 (sentinel `<postal box>`): 2 errors (the code is not a postal-box pattern); K5 (block
     removed): 2 errors (D361); K6 (unit only): validation error. The `skip_between` form is the only passing record.
   - K1 (same YAML, `unreadable` removed, status ok): 0 errors, 188 rows; Zimmermann's row is Technical University
     Berlin, unit as printed, Berlin, DE, maps to `org_tu_berlin`. Every recorded field is complete and as printed;
     the code itself is in no derived file.
   - The zheng2023a precedent does not apply: there the skip span swallowed a printed unit (South China Academy of
     Advanced Optoelectronics), so the recorded chain was incomplete and the authors were withheld. Here the span
     holds only the secretariat code. Building / site names between unit and org sit in `skip_between` with
     readable authors in six committed batches (lit_h03, lit_h08, lit_h18, lit_h31, lit_h57; lit_h22 hoffman2016
     D449); a secretariat code is a building abbreviation plus a secretariat number, with no street, postal code or
     box, and passes the D244 scan. The note's "checker gap D426 G6" is wrong (G6 is the span with no skip; this one
     is skipped and verified).
   - Since the YAML already carries the token, withholding the row buys no privacy. If the coordinator instead rules
     the code a D410-class routing code (sentinel only, never verbatim), the checker needs a pattern for it; the
     author is readable under that reading too. Either way `unreadable` goes (F1); the ruling on the verbatim token is
     question Q1.
2. bogaerts2011 split form: confirmed. The render prints "Ghent University—IMEC" (em dash); both text layers carry a
   "V" in its place. B1 (em-dash joined form) and B2 (hyphen joined form): 4 errors each (org not inside the block);
   B3 (IMEC as org, Ghent University in more_orgs): 2 errors (order). The joined D416 form is not verifiable; the
   recorded split (org Ghent University, more_orgs IMEC) passes and maps to the same two orgs as the joined forms
   (rows `org_ghent_university`, `org_imec`; 3 committed blocks use this split). Unit order "Department of Information
   Technology, Photonics Research Group" and locality "Gent" as printed; page-2 locator right (cover page 1, D366).
3. su2022 #5: confirmed as the only recordable form; slot imprecise (checker gap). Printed "Cheng-Ting Tsai", list "C.S.
   Tsai": the second initial S is not explained by Ting, so D369 asks for `slot: 0` + `author_list_differs` (common
   family name). Probe T1 (that form): 1 error (D302, compatible with unmatched slot 5); T2 (explicit `slot: 5`): 0
   errors, redundant. Same situation as lit_h30 lai2025 #1 / #4 (strict_compatible never compares the extra initials;
   B1 there). Keep as written; D426 / D412 review list.
4. blascosolvas2024 #7: confirmed. BL1 (no slot): 2 errors (no match; the list name carries a dotless i with a
   combining accent and lacks the second family name). BL2 (`slot: 0` + `author_list_differs`): 0 errors, not
   preferred: the printed form only adds the second family name to the list form, a D287 name-part variant (same
   statement, IMB-CNM). Explicit slot 7 right; D426 review list.
5. schall2016 current address: confirmed. Block 2 prints the cue "Current address" before the Cambridge centre. SC1
   (recorded as `present_address` with marker 2): 2 errors (marker + first field not printed, the cue sits between);
   SC2 (dropped marker removed): 2 errors (D286d). Not recordable until the D442 cue fix; marker in
   `dropped_markers` as lit_h05, lit_h16, lit_h39 li2018. The note's re-record values omit the centre (N1).
6. Other named calls, confirmed:
   - yu2016a: JORCEP printed between the centre and the state key laboratory; Y1 (chain without it): 2 errors. The
     committed lit forms carry the joint centre inside the ZJU unit chain (one block spells it out). Marker 3 = contact
     line (dropped_markers); probe YU1 (entry removed): 0 errors, the third marker of the last author is not checked
     (gap O3), but the printed run is 1,2,3 in both layers. Daoxin Dai: 1 plus asterisk. A campus site name printed
     before Hangzhou is not a D301 campus (single-institution site); not recorded, but the note names it (F3).
   - abuelmaaty2018 block 4: org "Indraprastha Institute of Information Technology", locality Delhi, IN; the acronym
     is printed after Delhi so it cannot join the org; Delhi is the city, not a campus of a multi-campus org (AB1
     campus Delhi: 0 errors, neutral; not preferred).
   - prost2019: University of California + campus Davis + locality Davis (D301 listed case); D1 (campus dropped): 0
     errors (known gap, missing campus not detected); rows map to `org_university_of_california_davis`.
   - pruessner2007: see per-paper (country "", locality city only).
   - acoleyen2011b / malik2014 block 2: no city printed, locality "" (A1 / M1 pass only through gap O1).
   - lischke2019 "IHP – Leibniz-Institut für innovative Mikroelektronik" (en dash) and steckler2024
     "IHP-Leibniz Institut für Innovative Mikroelektronik": both as printed; L1 (steckler form on lischke2019): 0
     errors (punctuation and case folded), so neither form is enforced; both strings are unmapped (org round, as the
     committed IHP variants).
   - Download stamp: the IEEE institutional download line at the page foot appears in no YAML field, note or row.

## Fixes (exact YAML edits)

F1 (required, status / readability; koos2007; rows 187 -> 188, no_header 1 -> 0, papers ok 27). Three lines:

line 121
```yaml
  status: ok
```

line 123
```yaml
  note: "no author list in the literature cache (slots from the header, D352); affiliations printed as first-page footnote statements (prose); statement 2 prints no country; statement 3 (author 3) prints a secretariat code between the unit and Technical University Berlin (verified skip_between, not stored, D380); membership designations in the author line; postal codes not recorded"
```

line 131
```yaml
    - {name: "Lars Zimmermann", markers: ["P3"]}
```

F2 (required, privacy wording; blascosolvas2024 line 159 note). Replace the clause from `the parent CSIC and the site` up to and including `after the institute` with

```yaml
the parent CSIC and a campus site name after the institute
```

F3 (required, privacy wording; yu2016a line 81 note). Replace the clause that follows `JORCEP inside the unit chain ` and ends with `(part of the address, not
recorded)` with

```yaml
and a campus site name before Hangzhou (not recorded)
```

(lit_h01, lit_h10 and lit_h33 notes name the same site; they are committed and outside this batch.)

F4 (required, note wording, lit_h45 F1; malik2014 line 230 note). Replace the abbreviated postal-box word in `street addresses, ... and postal codes not recorded` (the only such token
in the note) so that the clause reads

```yaml
street addresses, postal box and postal codes not recorded
```

Probe FIX (F1-F4 together, plus N1): 0 errors, 1 warning (blascosolvas2024 explicit slot 7); 172 slots, 172 recorded,
188 rows, all grade A, papers ok 27. The edited file is in the session scratchpad `h65_audit/probes/FIX.yaml` (diff
against the batch = exactly the 7 lines of F1-F4 and N1). After applying, re-run `check lit_h65 --corpus lit` (the
stamp hash changes).

N1 (optional, note values; schall2016 line 16). Replace `(University of Cambridge, Department of Engineering,
Cambridge, UK)` with

```yaml
(Centre for Advanced Photonics and Electronics, Department of Engineering, University of Cambridge, Cambridge, UK)
```

No other fix: no slot, marker, block, field, basis or locator is wrong.

## Questions for the coordinator

- Q1 koos2007: is a secretariat code (building abbreviation plus number) a D380 span that may stay verbatim in
  `skip_between` (recommended: yes, as the committed building names; no street, postal code or box), or a D410-class
  routing code (then a checker pattern / sentinel is needed before commit)? F1 applies under both.

## Observations (no YAML change)

- O1 Locality accepted when it is printed only inside the org name (acoleyen2011b A1, malik2014 M1 "Ghent" from
  "Ghent University"); same as lit_h63 O1.
- O2 D361 coverage does not detect an omitted "and also with" clause (steckler2024 ST1: 0 errors).
- O3 The last author's third marker is not checked (yu2016a YU1; lit_h40 last-author marker gap).
- O4 Missing campus not detected (prost2019 D1); D369 extra initials not compared (su2022 T1, lit_h30 G1).
- O5 `show` output (not batch files) leaves contact domain fragments of several IEEE papers unmasked (song2016a,
  steckler2024, yan2018, lin2022c, morino2014); the batch files carry none.

## Lists for the coordinator

- D412 list: yu2016a list slot 4 "Daoxin Dai A".
- D426 review list: su2022 #5 Cheng-Ting Tsai / C.S. Tsai (auto-matched, D369 non-match); blascosolvas2024 #7 Carlos
  Domínguez-Horna / Carlos Domínguez (explicit slot, name-part variant).
- Re-record list: schall2016 #3 Sagade present address (values in N1) after the "Current address" cue fix (D442).
- Org round (17 unmapped strings): Alexandria University (EG); Egypt-Japan University of Science and Technology
  (E-JUST) (EG); Fuzhou University (CN); Hebei University (CN); IHP Solutions GmbH (DE); IHP – Leibniz-Institut für
  innovative Mikroelektronik and IHP-Leibniz Institut für Innovative Mikroelektronik (DE; registry
  `org_ihp_leibniz_institute_for_high_performance_microelectronics`, alias request); Indraprastha Institute of
  Information Technology (IN); Instituto de Microelectrónica de Barcelona (ES); Kanazawa University (JP); Nanjing
  Normal University (CN); National Kaohsiung University of Applied Sciences (TW); Naval Research Laboratory (NRL) (no
  country); Royal Institute of Technology (SE); University of Erlangen-Nürnberg (no country); University of Karlsruhe
  (DE); plus Technical University Berlin rows of koos2007 after F1 map to `org_tu_berlin`.

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 1 warning, 187 rows | batch as written |
| FIX | F1-F4 + N1 | 0 errors, 1 warning, 188 rows | fix form |
| K1 | koos2007 Zimmermann readable, status ok | 0 errors, 188 rows | F1 form |
| K2 / K3 / K4 / K5 / K6 | no skip / org only / postal-box sentinel / block removed / unit only | 2 / 4 / 2 / 2 errors / validation error | skip_between form is the only passing record |
| KP1 | koos2007 P2 country DE | 2 errors | no country printed |
| B1 / B2 / B3 | bogaerts2011 em-dash joined / hyphen joined / IMEC first | 4 / 4 / 2 errors | split form verified |
| T1 / T2 | su2022 #5 slot 0 + differs / explicit slot 5 | 1 error (D302) / 0 errors | auto-match forced |
| BL1 / BL2 | blascosolvas2024 #7 no slot / slot 0 + differs | 2 / 0 errors | explicit slot kept (D287) |
| SC1 / SC2 | schall2016 current address recorded / dropped marker removed | 2 / 2 errors | not recordable; marker run verified |
| SU1 | su2022 Chih-Hsien Cheng on P1 | 5 errors | subjects verified |
| Y1 / YU1 | yu2016a chain without JORCEP / contact marker entry removed | 2 / 0 errors | chain verified / gap O3 |
| PR1 / PR2 | pruessner2007 country US / locality with D.C. | 2 / 1 errors | as recorded verified |
| A1 / M1 | acoleyen2011b / malik2014 block 2 locality Ghent | 0 / 0 errors | gap O1 |
| D1 / AB1 | prost2019 no campus / abuelmaaty2018 campus Delhi | 0 / 0 errors | neutral, recorded forms kept |
| L1 / ST1 | lischke2019 steckler IHP form / steckler2024 clause omitted | 0 / 0 errors | neutral / gap O2 |
