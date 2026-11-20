---
title: Fresh-context audit of the lit author-affiliation batch lit_h58 (25 papers)
date: 2026-11-20
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only with --dry-run, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h58/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D366, D380, D410, D426 G6, D442, D557, D565, D572, D599, D659, D670); format from the lit_h56 audit
verdict: GO, no required fix; 178 slots audited; 173 recorded with 0 wrong rows; 1 imprecise (ye2014 #9 present address not recordable); 5 correct no_header (ye2015 #3, yang2018b #1 #2 #3 #6, checker gaps); all 7 extractor calls confirmed
---

# Lit header batch audit: lit_h58 (2026-11-20)

## Scope

Batch lit_h58: 25 papers (IEEE PTL / JLT / JQE prose footnotes, Optica / Optics Express printed and single blocks, two
conference papers); 178 slots, 10 papers `slots_from_header`; 185 rows. Restricted corpus: this record names only
authors, orgs, units, cities and countries; no paper text is quoted and no contact, street, building or postal text is
copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h58 --corpus lit --codes <id> --pdf`
  (all 25); output kept in the session scratchpad `h58_audit/show/` only.
- Per slot: printed name vs the `show` author list and `compare.csv`; marker run (text and PDF layers); prose statement
  subjects and verbs; block fields (org, unit chain, campus, city, country); role; locator; notes.
- 52 distinct (paper, role, org, unit, city, country, basis, org id) tuples of `header_rows.csv` read (185 rows).
- Address / contact scan of `headers.yaml` and the derived CSVs (postal-code, street, building, box, phone, contact,
  URL patterns; the street / building / district words of the printed blocks): clean. Notes name street, building,
  P.O. box and postal code only as words ("not recorded"); district names (Clear Water Bay, Hung Hom) and the second
  place Ipswich appear in notes as D366 / D288 require; no number of any address appears.
- Precedent scans over all committed lit / OFC `headers.yaml`: AFB localities, Air Force Research Laboratory forms, Hong
  Kong localities (22 Hong Kong / HK, 14 Kowloon / HK, 3 Shatin / HK, 1 Kowloon / CN), Martlesham / Ipswich, SIMIT org
  strings (13 committed blocks, all with Chinese Academy of Sciences in `org`), Zijingang notes (lit_h01, h10, h33),
  Universitat Politècnica (de) València forms, "Current address" handling (li2018, zamek2011), loi2019 parent rule,
  chen2022d building-number partial.
- Probes on scratch copies (`h58_audit/probes/probe.py` + `probes.py`, scratch `LIT_BASE`, batch name `lit_p58`,
  `cmd_check(..., dry_run=True)`; 30 runs). Dry-run check of the real batch: 0 errors, 0 warnings; totals equal the
  stamped derived files (178 slots, 173 recorded, 5 no_header, 185 rows: prose 77, printed 76, single 32; primary 173,
  additional 10, present address 2; 16 unmapped org strings). md5 of every repo batch file identical before and after
  the audit; `check_stamp.txt` matches `headers.yaml` (sha256 889a1edd...). Probe checks wrote their usual logs under
  `logs/` (prefix `lit_headers_check_lit_p58`, 60 files). The one probe file holding a building designation (YB2) was
  deleted from the scratchpad after the run.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h58 | 25 / 25 | 178 | 177 (172 recorded + 5 correct no_header) | 1 (ye2014 #9) | 0 |

- Papers ok 23, partial 2 (ye2015, yang2018b), unreadable 0; `slots_from_header` 10 (ye2015, franco2005, duan2012,
  ye2014, li2015, hayashi1998, nakata2002, xu2008, albert1999, kashyap1993; exactly the papers.csv rows with
  `n_authors_meta` 0, each prints the D352 line in `show`); `author_list_differs` 0; explicit slots 0; order warnings 0;
  16 unmapped org strings.
- Per paper (slots / rows): huang2016b 9 / 10; campbell1988 4 / 4; ye2015 15 / 15; lenox1999 7 / 7; franco2005 8 / 9;
  duan2012 5 / 5; ye2014 18 / 18; li2015 6 / 6; hayashi1998 7 / 7; nakata2002 6 / 6; hoffman2019 7 / 7; xu2008 2 / 2;
  xiong2014 6 / 7; wang2014b 8 / 9; nelan2022b 7 / 10; ma2019 7 / 7; tan2016 5 / 7; ding2012 4 / 4; zanzi2019 14 / 14;
  kumar2022b 4 / 6; albert1999 8 / 8; chen2015a 4 / 4; suzuki2017 8 / 8; yang2018b 6 / 2; kashyap1993 3 / 3.

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (178) | 178 | 0 | 0 |
| markers (printed / prose / single, 173 recorded) | 173 | 0 | 0 |
| header position / statement subject | 173 | 0 | 0 |
| blocks (org / unit / locality / country) (173 authors with rows) | 172 | 1 (ye2014 #9, present address missing) | 0 |
| unreadable calls (2 papers, 5 slots) | 5 | 0 | 0 |
| present addresses (2 recorded: franco2005 #3, kumar2022b #1) | 2 | 0 | 0 |
| locators | all | 0 | 0 |
| notes (25) | 25 | 0 | 0 |

## Per-paper findings

- huang2016b (9; printed, capitals): Hewlett Packard Laboratories, Palo Alto, US; Texas A&M University ECE, College
  Station, US. Markers in both layers (Yu 1,2; Palermo 2; the others 1); asterisk = contact line. List "Marco
  Fiorentino B" matched automatically (probe HF1 `slot: 0`: 1 error, D302). ok; D412 list.
- campbell1988 (4; prose): call 4. ok.
- ye2015 (15; prose, slots from header, partial): call 7. ok.
- lenox1999 (7; prose): "The authors" statement; The University of Texas at Austin with the MRC + ECE chain, Austin, US
  (leading article as printed, D288). List forms Chet / Hui Fan / Geoffrey S. / A.L. Homles / Ben G. / Joe Charles match
  the printed initials; the printed family name Homles (sic) agrees with the list. ok.
- franco2005 (8; prose, slots from header): call 2. ok.
- duan2012 (5; single, slots from header): Institute of Microelectronics, Singapore, SG; A*STAR parent not copied
  (probe D1 with the parent: 0 errors, neutral; parent rule). ok.
- ye2014 (18; prose, slots from header): call 1. P1 subject lists exactly the 14 authors carrying P1; P3 Eblana Photonics,
  Dublin, IE (Phelan, Kelly, O'Carroll). #9 imprecise (present address not recordable).
- li2015 (6; prose, slots from header): "The authors" statement; Institute of Semiconductors, Chinese Academy of Sciences
  (contract example form) + SKL on Integrated Optoelectronics, Beijing, CN. ok.
- hayashi1998 (7; prose, slots from header): NEC Corporation with Optoelectronics and High Frequency Device Research
  Laboratories, Tsukuba (authors 1-5, 7) and Guidance and Electro-Optics Division, Futyu as printed (Yamakata); JP.
  Subjects verified. ok.
- nakata2002 (6; single, slots from header): NEC Corporation + Photonic and Wireless Research Laboratories, Tsukuba, JP
  (ECOC 2001 per the printed proceedings line). ok.
- hoffman2019 (7; single, capitals): Sandia National Laboratories, Albuquerque, US; the block's box number is covered
  by "address" in the note. List middle names (Christina M., Andrew T. S., Douglas C., Christopher Todd) are dropped
  middle forms. ok.
- xu2008 (2; single, slots from header): HKUST Photonic Device Laboratory + ECE department; locality Hong Kong, HK
  ("Hong Kong SAR, China" printed as the place, D249); district in the note (D366). ok. See call 6.
- xiong2014 (6; printed): NRC Canada + Information and Communication Technologies, Ottawa, CA; Carleton University
  Department of Electronics, Ottawa, CA. Markers in both layers. ok.
- wang2014b (8; printed): call 5. ok.
- nelan2022b (7; printed, capitals): University of Delaware ECE, Newark, US; Phase Sensitive Innovations, Newark, US.
  Markers (Nelan, Shi, Prather 1,2) in both layers. ok.
- ma2019 (7; printed, capitals): The University of British Columbia ECE, Vancouver, CA; McGill University ECE,
  Montreal, CA (province not recorded). ok.
- tan2016 (5; printed): IME (A*STAR not copied), Singapore, SG; NUS ECE, Singapore, SG; The Hong Kong Polytechnic
  University EIE, Hong Kong, HK. Markers (Tan 1,2; Yu 2,3). ok. See call 6.
- ding2012 (4; printed): Technical University of Denmark + DTU-Fotonik, locality "Kgs. Lyngby" as printed (D366); the
  street and building printed after the org lie outside the unit-org segment and are not recorded; South China Normal
  University + South China Academy of Advanced Opto-electronics (as printed), Guangzhou, CN. ok.
- zanzi2019 (14; printed, capitals): call 6. Blocks 2-5 (DAS photonics, València; Aristotle University of Thessaloniki,
  Thessaloniki, GR; ams AG, Premstaetten, AT; Fraunhofer IZM, Berlin, DE) as printed. #14 list "A. Brimont" matches
  ANTOINE BRIMONT. ok.
- kumar2022b (4; printed, capitals): call 6. Block 2 present address (probe KU3 as affiliation: 2 errors); block 3
  KACST, Riyadh, SA (additional for Alshamrani); marker 4 = equal contribution on both co-first authors. ok.
- albert1999 (8; prose, slots from header): Communications Research Centre, Ottawa, CA; NTT Optical Network Systems
  Laboratories, Yokosuka, JP; NTT Opto-electronics Laboratories, Tokai, JP; subjects verified (NTT lab names as org,
  NTT Photonics Laboratories precedent). ok.
- chen2015a (4; single): Zhejiang University with the COER / SKL / provincial key laboratory chain, Hangzhou, CN; campus
  name not recorded (lit_h10 / lit_h33 precedent); list "Daoxin Dai A" matched automatically. ok; D412 list.
- suzuki2017 (8; single, capitals): National Institute of Advanced Industrial Science and Technology (AIST), Tsukuba,
  JP. ok.
- yang2018b (6; printed, capitals, partial): call 7. ok.
- kashyap1993 (3; prose, slots from header): call 3. ok.

## Extractor calls (verified)

1. ye2014 #9 N. Mac Suibhne: the statement "was with" Tyndall (Cork, IE; affiliation of the work, D354) continues in
   the same sentence with "and now is with" the Aston institute (Birmingham, U.K.). `VERB_RE` needs "is now with", not
   "now is with"; `CLAUSE_RE` needs "and (is / are) (also) with". Probe E1 (P3 clause, present_address): 2 errors
   (clause anchor not found); E2 (P3 as its own statement): 4 errors (no cue, subject not found); E3 (P2 as
   present_address): 3 errors. So only the "was with" block is recordable; the present address stays in the note
   (Aston Institute of Photonic Technologies, School of Engineering and Applied Science, Birmingham, GB: no postal
   code). Same treatment as li2018 / zamek2011 (D442 cue gap, address kept for re-recording). Confirmed; imprecise
   (missing present-address row), re-record list.
2. franco2005: P2 org "AFRL/SNHC" as printed (one slash-joined token, no comma), locality "Hanscom AFB" as printed
   (lit_h36 "Wright-Patterson AFB" precedent). Probes F1 (org AFRL + unit SNHC), F2 (locality empty), F2b (Hanscom):
   0 errors each, neutral; the whole-token form follows the company-plus-acronym rule (Siemens HL, CEA LETI; h56 call
   3). P3 Solid State Scientific Corporation, Hollis, US ("was with", affiliation; F5 as present_address: 3 errors);
   P4 OptoGration, Haverhill, US, present address ("He is currently with"; F4 as affiliation: 2 errors); P5 University
   of Massachusetts + campus Lowell (D301) + Photonics Center, Department of Physics, Lowell, US (F3 without campus:
   0 errors, neutral; D301 form kept). Confirmed; org round (AFRL/SNHC as a child or alias of Air Force Research
   Laboratory).
3. kashyap1993: page 1 opens with the end of the preceding paper; the kashyap1993 title, author line and footnote
   follow. "The authors" statement: BT Laboratories, Martlesham Heath before Ipswich, then an interleaved log-number line,
   then postal code and UK. Locality Martlesham Heath = first printed place (D288); probe K1 (Ipswich) 0 errors,
   neutral. Country GB: UK printed in the statement (K3 IE: 2 errors; K2 empty: 0 errors, checker accepts an empty
   country when one is printed). The UK after the interleaved line belongs to the same statement (no other statement on
   the page), unlike adar1994. No committed Martlesham block exists; OFC BT blocks print Ipswich only. Confirmed.
4. campbell1988: the OCR reads the statement's first word as "fhe" in both layers; "The authors" statement accepted by
   the checker; AT&T Bell Laboratories, Holmdel; the statement prints a state code and postal code, no country:
   country "" (D249; probe C1 US: 2 errors). List "Joe Charles Campbell" / "Bart C. Johnson" agree on initials.
   Confirmed.
5. wang2014b: Gan printed with markers 1,3 in both layers; marker 3 heads the first of the two contact lines (asterisk the
   second, Qi): `dropped_markers` 3 "contact footnote" is right. Probe W1 (dropped marker removed) passes with 0
   errors: the last author's later markers are not checked (known gap, D442 / D565 / D629). Purdue block 2: the
   school and the Birck Nanotechnology Center are both printed before Purdue University, joined by "and the"; probe W2
   (unit without the Birck centre): 2 errors, so the full chain is required. Block 1 SIMIT with Chinese Academy of
   Sciences in `org` (13 committed blocks in that form; W3 without CAS 0 errors, neutral). Confirmed.
6. Places:
   - kumar2022b block 1: University of California + campus San Diego + ECE, locality La Jolla (the city printed after
     the street), US: same form as zamek2011 (lit_h54). KU1 (no campus) and KU2 (San Diego as locality) 0 errors,
     neutral; the recorded form follows D301 and the printed city. Confirmed.
   - zanzi2019 block 1: printed without "de", and no place outside the org name (postal code, Spain). Locality ""
     (D288 / D249); probe Z1 (València) passes only through the known gap (city found inside the org name, D557
     johnson2020). Confirmed. The h05 / h50 UPV blocks that record València print the city separately.
   - tan2016 block 3 and xu2008: district printed before Hong Kong, then China / SAR China: locality Hong Kong, country
     HK (D249), district in the note. The contract (D366, lit CONTRACT locality rule) sends a district printed before
     the city to the note, and the lit_h53 N1 ruling (ahmmed2020, Kowloon Tong) applied the same; districts are place
     names, not street addresses (the D244 scan does not cover them and should not). Keep. Probes T1 / X1 (district as
     locality) 0 errors and T2 (country CN) 0 errors: checker gaps (district accepted as locality; HK / CN both
     accepted, D659); the recorded forms follow D366 / D249.
7. Parent rule and list artefacts:
   - ye2014 / ye2015: University College Cork printed after Tyndall National Institute is not copied (loi2019 lit_h08,
     palmer2026 D442 F2). duan2012 / tan2016: A*STAR after IME not copied (D1 neutral). Confirmed.
   - huang2016b "Marco Fiorentino B" and chen2015a "Daoxin Dai A": automatic matches; D412 correction list (zeng2019,
     vaerenbergh2021, yuan2021 / xu2025a, zhao2022 and others).
   - yang2018b (partial): block 1 prints a building designation between the unit chain and South China Normal
     University. Probe YB1 (block recorded without a skip): 2 errors (unit and org not contiguous). Probe YB2 (the
     building designation in `skip_between`): 0 errors, but it stores a building number in the YAML, which the contract
     forbids (D244; D380 covers building or site names, not numbers; the D244 scan misses this "No." form, D546 gap).
     The extractor's partial is the only faithful form: block 1 not recorded, authors 1, 2, 3 and 6 unreadable (YB3
     LIU LIU with marker 1 and no block: 1 error). Block 2 Sun Yat-sen University + SKL / School of Microelectronics,
     Guangzhou, CN (Zhu, Cai). The note's re-record values (unit chain, university, Guangzhou, CN) contain no building
     designation. chen2022d precedent (D599, D426 G6). Confirmed.
   - ye2015 (partial): the statement subject prints authors 2 and 3 without a comma; probe Y1 (M. Gleeson readable):
     3 errors (not named in the subject, partial without an unreadable author). Author 3 unreadable is the only passing
     faithful form; re-record values in the note (Tyndall National Institute, Cork, IE). P2 Peters "is also with"
     University College Cork + Department of Physics, Cork, IE (the subject's first initial is hidden by the masked
     contact run in `show` only; the checker verifies the raw text). New checker gap (missing comma between subject
     names). Confirmed.

## Fixes (exact YAML edits)

None required. No slot, marker, block, field or note is wrong.

## Observations (no YAML change)

- O1 "and now is with" (cue before the verb) is a new statement-continuation form beyond the D426 / G6 and h56 O3 lists
  (ye2014 #9); a clause anchor for it with `role: present_address` would make the Aston present address recordable.
- O2 Missing comma between two names in a statement subject (ye2015 "H. Yang M. Gleeson") joins them into one subject
  name; checker test candidate.
- O3 `skip_between` accepts a building number (probe YB2, 0 errors): the D244 scan does not catch this form in
  `skip_between`; the field should reject digits other than the D410 postal-box token.
- O4 Known gaps reconfirmed: last author's later markers unchecked (W1), empty country accepted when one is printed
  (K2), district / second place accepted as locality (T1, X1, K1), HK / CN both accepted (T2), a city inside the org
  name accepted (Z1).

## Lists for the coordinator

- D412 correction file: huang2016b #6 ("Marco Fiorentino B"), chen2015a #4 ("Daoxin Dai A").
- Re-record list: ye2014 #9 present address (Aston Institute of Photonic Technologies, School of Engineering and
  Applied Science, Birmingham, GB) after O1; ye2015 #3 (Tyndall National Institute, Cork, IE) after O2; yang2018b block
  1 (South China Normal University with the Centre for Optical and Electromagnetic Research, Guangdong Provincial Key
  Laboratory of Optical Information Materials and Technology, South China Academy of Advanced Optoelectronics chain,
  Guangzhou, CN; authors 1, 2, 3, 6) after the G6 building-number skip.
- Org round (16 unmapped strings): AFRL/SNHC (Air Force Research Laboratory unit), AT&T Bell Laboratories, BT
  Laboratories, Carleton University, Communications Research Centre, DAS photonics, Eblana Photonics, Hewlett Packard
  Laboratories (alias of `org_hewlett_packard_labs`), KACST, NTT Optical Network Systems Laboratories, NTT
  Opto-electronics Laboratories, OptoGration, SIMIT with CAS, Solid State Scientific Corporation, Universitat
  Politècnica València (alias of the UPV org), University of Massachusetts, Lowell (campus, D301).

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 0 warnings | batch as written |
| Y1 | ye2015 Gleeson readable | 3 errors | unreadable required |
| E1 / E2 / E3 | ye2014 Aston as clause / as statement / P2 present_address | 2 / 4 / 3 errors | present address not recordable; P2 affiliation required |
| F1 / F2 / F2b | franco2005 AFRL + unit SNHC / locality empty / Hanscom | 0 / 0 / 0 errors | neutral; printed forms kept |
| F3 / F4 / F5 | franco2005 no campus / P4 affiliation / P3 present_address | 0 / 2 / 3 errors | D301 form kept; roles verified |
| K1 / K2 / K3 | kashyap1993 Ipswich / country empty / IE | 0 / 0 / 2 errors | D288 first place kept; GB verified |
| C1 | campbell1988 country US | 2 errors | empty country required |
| W1 / W2 / W3 | wang2014b no dropped marker / Purdue unit without Birck / SIMIT without CAS | 0 / 2 / 0 errors | last-author gap; chain required; neutral |
| KU1 / KU2 / KU3 | kumar2022b no campus / San Diego locality / block 2 affiliation | 0 / 0 / 2 errors | neutral; neutral; cue verified |
| Z1 | zanzi2019 block 1 València | 0 errors | gap (city inside org name); empty kept |
| T1 / T2 / X1 | tan2016 Hung Hom / tan2016 CN / xu2008 Clear Water Bay | 0 / 0 / 0 errors | gaps; D366 / D249 forms kept |
| D1 | duan2012 org with A*STAR | 0 errors | neutral; parent rule kept |
| YB1 / YB2 / YB3 | yang2018b block 1 without skip / with building in skip_between / Liu Liu marker 1 | 2 / 0 / 1 errors | partial required; YB2 forbidden by D244 (O3) |
| HF1 | huang2016b Fiorentino slot 0 | 1 error (D302) | automatic match forced |
