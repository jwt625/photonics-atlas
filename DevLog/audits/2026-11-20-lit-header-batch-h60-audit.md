---
title: Fresh-context audit of the lit author-affiliation batch lit_h60 (17 papers)
date: 2026-11-20
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only with --dry-run on the batch, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h60/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D366, D380, D410, D426 G6, D442, D546, D557, D565, D599, D686); round-3 F5 / h17 N1 / h18 N1 / h22 F2 site-name rule; format from the lit_h58 audit
verdict: NO-GO as written, GO after F1 (privacy: a campus site name stored verbatim in three unit fields of zheng2023a; no derived row changes); 113 slots audited, 110 recorded with 0 wrong rows, 3 correct no_header (zheng2023a #1-#3, checker gap); all extractor calls confirmed
---

# Lit header batch audit: lit_h60 (2026-11-20)

## Scope

Batch lit_h60: 17 papers (IEEE PTL / JLT / JSTQE / Proc. IEEE prose footnotes, Optica / Optics Express printed blocks,
two conference papers); 113 slots, 6 papers `slots_from_header`; 119 rows. Restricted corpus: this record names only
authors, orgs, units, cities, districts and countries; no paper text is quoted and no contact, street, building, site
or postal text is copied. The site word at issue (F1) is named by type with its `headers.yaml` line numbers.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h60 --corpus lit --codes <id> --pdf`
  (all 17); output kept in the session scratchpad `h60_audit/show/` only.
- Per slot: printed name vs the `show` author list (or the header for the 6 header-slot papers) and `compare.csv`;
  marker run in both layers; prose statement subjects and verbs; block fields (org, unit chain, campus, city,
  country); role; locator; notes. Contact-line markers checked by the first character of each contact line in
  `text.md` (the contact itself not printed).
- All 34 distinct (paper, org, unit, city, country) tuples of `header_rows.csv` read (119 rows; roles primary 110,
  additional 8, present address 1; basis printed 69, prose 50; all grade A).
- Address / contact scan of `headers.yaml` and the derived CSVs (contact, URL, postal-code / 4+ digit, street,
  road, building, box patterns, plus every street, ward, site, district and state word printed in this batch's
  blocks). Hits: the word "street" in four notes ("street address ... not recorded"), districts Kowloon (gao2011
  note), Clear Water Bay (geng2014 note), Naka-Gun (takiguchi1996 note), suburb Camperdown (fontaine2022 locality and
  note; D366 / D288 allow these), years in papers.csv / unmapped_orgs.csv, and the campus site word in three
  `unit` fields of zheng2023a (lines 225, 227, 228; F1). No contact, URL, postal code, street, ward, building or box
  text anywhere. The derived CSVs do not contain the site word (authors 1-3 of zheng2023a derive no rows).
- Probes on scratch copies (`h60_audit/probes/probe.py` + `mk.py`, scratch `LIT_BASE`, batch name `lit_p60`,
  `cmd_check(..., dry_run=True)`; Z1w / Z2w with derived files written into the scratch base only; 27 runs). Dry-run
  check of the real batch: 0 errors, 0 warnings; totals equal the stamped derived files (113 slots, 110 recorded,
  3 no_header, 119 rows, 5 unmapped org strings). md5 of every repo batch file identical before and after the audit;
  `check_stamp.txt` matches `headers.yaml` (sha256 f525b875...). Probe checks wrote their usual logs under `logs/`
  (prefix `lit_headers_check_lit_p60`, 54 files).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h60 | 17 / 17 | 113 | 113 (110 recorded + 3 correct no_header) | 0 | 0 |

- Papers ok 16, partial 1 (zheng2023a), unreadable 0; `slots_from_header` 6 (hoessbacher2014, gao2011, geng2014,
  fontaine2022, takiguchi1996, doerr2005; exactly the papers.csv rows with `n_authors_meta` 0, each prints the D352
  line in `show`); `author_list_differs` 0; explicit slots 0; order warnings 0; 5 unmapped org strings.
- Per paper (slots / rows): xu2019c 8 / 8; hoessbacher2014 8 / 8; gao2011 7 / 7; dong2017 11 / 11; geng2014 4 / 5;
  gao2025b 9 / 10; bernard2021 10 / 11; ozdemir2020 8 / 10; fontaine2022 7 / 7; yi2024b 10 / 10; yen2020 2 / 2;
  akiyama2021a 7 / 11; xu2017a 2 / 2; takiguchi1996 4 / 4; zheng2023a 4 / 1; ong2020 6 / 6; doerr2005 6 / 6.
- Privacy findings: 1 (F1, three `unit` fields of one paper); notes: 1 inaccurate wording (folded into F1).

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (113) | 113 | 0 | 0 |
| markers (printed / prose, 110 recorded) | 110 | 0 | 0 |
| header position / statement subject | 110 | 0 | 0 |
| blocks (org / unit / locality / country) (110 authors with rows) | 110 | 0 | 0 |
| unreadable calls (1 paper, 3 slots) | 3 | 0 | 0 |
| present addresses (1 recorded: geng2014 #2) | 1 | 0 | 0 |
| locators | all | 0 | 0 |
| notes (17) | 16 | 1 (zheng2023a wording, F1) | 0 |

## Per-paper findings

- xu2019c (8; printed, capitals): NUS ECE, Singapore, SG; Applied Materials Inc., Sunnyvale, US (state and "United
  States" printed; state not recorded); NTU EEE, Singapore, SG. Markers in both layers (Gong 1,4; Yeo 1,5). The two
  contact lines start with 4 and 5: `dropped_markers` right (probe X1 without Gong's 4: 2 errors; X2 without Yeo's 5:
  0 errors, the known last-author gap). ok.
- hoessbacher2014 (8; printed, capitals, slots from header): ETH Zurich + Institute of Electromagnetic Fields, Zurich,
  CH; Karlsruhe Institute of Technology (KIT) + "Institutes IMT" as printed, Karlsruhe, DE. Contact lines start with
  3 and 4 (H1 without Hoessbacher's 3: 2 errors; H2 without Leuthold's 4: 0 errors, last-author gap). ok.
- gao2011 (7; prose, slots from header): "The authors" statement; HKUST (no leading article printed) + ECE department;
  district Kowloon before Hong Kong: locality Hong Kong, HK, district in the note (D366; h58 tan2016 / xu2008). Probe
  K1 (country CN): 2 errors. ok.
- dong2017 (11; printed, capitals): NUS (NUS) ECE and NTU (NTU) EEE, both Singapore, SG, acronyms kept as printed;
  asterisk = corresponding author with a contact line. List "Shuh-Ying Lee" etc. match. ok.
- geng2014 (4; prose, slots from header): call 1. ok.
- gao2025b (9; printed): University of Virginia ECE and Department of Physics, Charlottesville, US (state not
  recorded). Xu Yi 1,2,3: the contact line starts with 3 (GB1 without the dropped 3: 2 errors; GB2 with 3 as an
  affiliation marker: 1 error). List "Andréas Beling" matches the printed name. ok.
- bernard2021 (10; printed): Fondazione Bruno Kessler + "Sensors and Devices" as printed (the other committed FBK block
  prints "Center for Sensors and Devices"), Trento, IT; University of Trento + Department of Industrial Engineering,
  Trento, IT; street parts of both blocks not recorded. Gemma 1,2. List "G. Paternoster" / "Alberto Giacomo Gola"
  match. ok.
- ozdemir2020 (8; printed): imec, Leuven, BE (no unit printed); Ghent University + "Photonics Research Group, INTEC",
  Ghent, BE; street and site parts not recorded. Ozdemir and Van Thourhout 1,2; asterisk = contact. List "Özdemir"
  matches. ok.
- fontaine2022 (7; prose, slots from header): call 2. ok.
- yi2024b (10; prose): two statements; HUST with the WNLO + school chain as unit (majority form, D572 N2), Wuhan, CN
  (province not recorded); Fudan University with the MoE key laboratory + department chain, Shanghai, CN. Subjects:
  5 + 5 names, each carrying exactly its block. Equal-contribution and corresponding-author parentheses carry no
  markers. ok.
- yen2020 (2; prose): "The authors" statement; National Sun Yat-sen University + Department of Photonics, Kaohsiung,
  TW. ok.
- akiyama2021a (7; printed, conference): call 4. ok.
- xu2017a (2; prose): "The authors" statement; Zhejiang University with the SKL for Modern Optical Instrumentation +
  COER chain, Hangzhou, CN. ok.
- takiguchi1996 (4; prose, slots from header): call 3. ok.
- zheng2023a (4; prose, partial): call 5. Liu Liu P5: Zhejiang University with the SKL / college / research-center
  chain, Hangzhou, CN (the lit_h43 chen2022d block 1 form). Rows correct; F1 (privacy, YAML only).
- ong2020 (6; prose): call 6. ok.
- doerr2005 (6; prose, slots from header): "The authors" statement; Lucent Technologies (org) + Bell Laboratories
  (unit), Holmdel, US: the form of the committed Lucent blocks (3 Holmdel / Murray Hill blocks). State and postal code
  not recorded. ok.

## Extractor calls (verified)

1. geng2014: P1 Geng, Poon, Lau "are with" HKUST ECE; P2 Feng "was with" HKUST ECE = affiliation of the work (D354;
   ye2014 / franco2005 precedent), its own block although the org repeats (two statements, two blocks); P3 "He is now
   with" = present address, University of California + `campus` Davis + ECE, locality Davis, US (D301 form, as
   zamek2011 / kumar2022b / franco2005). Probes: G1 (P2 as present_address) 3 errors; G2 (P3 as affiliation) 2 errors;
   G5 (Feng on P1) 5 errors; G3 (no campus) 0 errors, neutral, D301 form kept. Rows: Feng primary HKUST + present
   address `org_university_of_california_davis`. Locality Hong Kong, HK with the district Clear Water Bay in the note
   (D366); G4 (Clear Water Bay as locality) 0 errors, known gap. Confirmed.
2. fontaine2022: author line in capitals after "By" with membership designations; six statements, each subject
   naming exactly the carriers (P5 Jung and Richardson). P4 The University of Sydney + IPoS, locality Camperdown: the
   only place printed in the statement (a suburb, then state code, postal code, country). D288 takes the first printed
   city; Camperdown is a printed locality, not a state, so recording it as printed is right (La Jolla precedent,
   kumar2022b / zamek2011); the six committed Sydney blocks that print no place record "" (lit_h13, h29, h47, h57).
   Probes F1 (locality "") and F2 ("Sydney") 0 errors each: neutral, known gaps (empty locality accepted; city inside
   the org name accepted, D557). Southampton, GB (U.K. printed); UQ "The University of Queensland" and "School of IT
   and Electrical Engineering (ITEE)" as printed, Brisbane; Macquarie, Sydney; UCF College of Optics and Photonics,
   Orlando; Nokia Bell Labs, Murray Hill. Confirmed.
3. takiguchi1996: "The authors" statement; NTT Opto-Electronics Laboratories, locality "Tokai-Mura" as printed, then
   the district Naka-Gun and the prefecture (note / not recorded). lit_h58 albert1999 records "Tokai" because that
   paper prints "Tokai" (checked in its text). Both follow D366 (Atsugi-shi, Yokohama-shi, Showa-cho kept as printed);
   the difference is in the sources, not in the rule. Probe T1 ("Tokai") 0 errors: neutral (prefix match). The org
   strings differ in case (Opto-Electronics / Opto-electronics, both as printed): one alias for the org round.
   Confirmed.
4. akiyama2021a: markers printed in parentheses after the names and before the blocks, both layers; the checker
   reads them (probe A1, Akiyama without 3: 2 errors). PETRA full name with acronym (10 committed blocks in this form);
   block 2 "PETRA" as printed, Tsukuba; Fujitsu Limited, Kawasaki (`org_fujitsu`). Street, ward and prefecture not
   recorded; the note names them by type only. Confirmed.
5. zheng2023a (partial): the three South China Normal University statements (authors 1, 2, 3) print a campus site name
   between the Guangdong provincial key laboratory and the South China Academy of Advanced Optoelectronics, before the
   university. Recording the whole chain needs a skip for a span inside the unit chain, which the checker lacks
   (D426 G6; chen2022d lit_h43 and yang2018b lit_h58 had a building number in the same chain). Probes:
   - Z3 (blocks P1 / P3 / P4 dropped, the printed-block precedent form): 8 errors (D361 statement coverage; clause P2
     without its statement). So, unlike chen2022d / yang2018b, prose statements must stay recorded.
   - Z5 (author 1 readable with P2 only): 3 errors (named in the P1 subject without P1). Author 1 losing the P2 row
     is forced while P1 is unreadable. Confirmed.
   - Z6 (org empty): 2 errors (block has no org). Z4 (`skip_between` = site name only): 4 errors (the academy still
     separates unit and org).
   - Z1 (unit = key laboratory, `skip_between` = the printed span from the site name to the university, authors still
     unreadable): 0 errors, 119 rows unchanged, the site word absent from every derived file.
   - Z2 (Z1 with authors 1-3 readable): 0 errors, 123 rows, but the unit chains lose the academy (and P4 the National
     Center): a workaround of G6 with incomplete units; not recommended (D546: gaps recorded, not worked around).
   The partial status, the unreadable authors and author 1's lost P2 row are right. The stored form is not: the site
   name sits verbatim in the `unit` of P1, P3 and P4 (lines 225, 227, 228). Site names may appear only inside
   `skip_prefix` / `skip_between` (round-3 F5, h17 N1, h18 N1, h22 F2, D380); the extractor's own note names it only
   by type. The note also says the checker "cannot skip without storing it", while D380 stores site names in
   `skip_between`; the real gap is the academy printed after the site, and the note mentions P1 / P3 but not P4. F1.
6. ong2020: statement 1 prints the parent agency with its acronym after the Institute of High Performance Computing;
   not copied (parent rule; duan2012 / tan2016 A*STAR precedent; 3 committed IHPC blocks in this form). Probe O1 (org
   with the parent) 0 errors, neutral. Statement 2 NTU + "Silicon Technologies–Centre of Excellence" with the en dash as
   printed (one committed block prints it without the dash). Singapore printed once after the org: locality
   Singapore, SG. List "Tina Xin Guo" matches printed Tina X. Guo. Confirmed.
7. Contact `dropped_markers`: xu2019c 4 / 5, hoessbacher2014 3 / 4, gao2025b 3: each contact line starts with that
   marker (text.md, first character only); no block uses them. Confirmed (last-author cases unchecked by the checker,
   X2 / H2).

## Fixes (exact YAML edits)

F1 (required, privacy; zheng2023a, `headers.yaml` lines 223, 225, 227, 228; rows unchanged, still partial):

- Lines 225 (P1) and 227 (P3): `unit` -> "Guangdong Provincial Key Laboratory of Optical Information Materials and
  Technology"; add `skip_between:` = the rest of the current `unit` value after "Technology, " verbatim (the site
  name, ", ", "South China Academy of Advanced Optoelectronics"), placed after `unit`.
- Line 228 (P4): same `unit`; `skip_between:` = the rest of the current `unit` value after "Technology, " verbatim
  (site name through "and the National Center for International Research on Green Optoelectronics").
- Line 223 `note` ->

```
affiliations printed as footnote statements (prose); statement 1 (author 1) has an and also with clause (Sun Yat-sen University, clause block P2); the South China Normal University statements (authors 1, 2, 3; blocks P1, P3, P4) print a campus site name inside the unit chain, between the key laboratory and the academy (checker gap D426 G6: no skip for a span inside the chain; chen2022d / yang2018b precedent for the same laboratory chain): the three blocks carry the key laboratory as unit and the printed span from the site name to the university in skip_between (never stored), only so the statements stay verified; authors 1, 2 and 3 unreadable, no rows (author 1 also loses the clause block P2); re-record after a checker fix: South China Normal University with the unit chain Guangdong Provincial Key Laboratory of Optical Information Materials and Technology, South China Academy of Advanced Optoelectronics (statement 3 adds the National Center for International Research on Green Optoelectronics), Guangzhou, CN; author 1 also Sun Yat-sen University with the State Key Laboratory of Optoelectronic Materials and Technologies and the School of Electronics and Information Technology, Guangzhou, CN; postal codes and contacts not recorded
```

Probe Z1n (F1 applied in full): 0 errors, 0 warnings, 119 rows, totals identical; the site word then appears only in
the three `skip_between` values. The edited file is in the session scratchpad `h60_audit/probes/Z1n.yaml` (diff
against the batch = exactly these four lines). After applying, re-run `check lit_h60 --corpus lit` (the stamp hash
changes).

No other fix: no slot, marker, block, field or other note is wrong.

## Observations (no YAML change)

- O1 The D244 / site scan does not see a hyphenated site name inside a `unit` field (zheng2023a, as h22 G5 for an org
  field); checker test candidate.
- O2 G6 gains a prose case: a site span inside a unit chain of a prose statement cannot be dropped (D361 coverage),
  unlike the printed-block cases chen2022d / yang2018b. A `skip_between` that may sit anywhere inside the unit-org
  segment (verified, never stored) would make zheng2023a #1-#3 recordable with the full chain.
- O3 Known gaps reconfirmed: last author's later markers unchecked (X2, H2), empty locality and a city inside the org
  name accepted (F1, F2), district accepted as locality (G4), locality prefix accepted (T1), parent after the
  institute neutral (O1 probe).

## Lists for the coordinator

- Re-record list: zheng2023a #1-#3 (values in the F1 note) after the G6 inside-chain skip.
- D412 / D426 lists: none from this batch.
- Org round (5 unmapped strings): Fondazione Bruno Kessler (unit "Sensors and Devices"), Institute of High Performance
  Computing, Macquarie University, NTT Opto-Electronics Laboratories (case alias of lit_h58 "NTT Opto-electronics
  Laboratories"), The University of Queensland.

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 0 warnings | batch as written |
| Z1 / Z1n | zheng2023a site span in `skip_between`, authors unreadable (+ note) | 0 / 0 errors, 119 rows | F1 form |
| Z2 | Z1 with authors 1-3 readable | 0 errors, 123 rows | G6 workaround, units incomplete; not recommended |
| Z3 | SCNU blocks dropped (printed-block precedent form) | 8 errors | prose statements must stay recorded (D361) |
| Z4 / Z5 / Z6 | site-only skip / author 1 with P2 only / org empty | 4 / 3 / 2 errors | partial with author 1 unreadable required |
| G1 / G2 / G5 | geng2014 P2 present_address / P3 affiliation / Feng on P1 | 3 / 2 / 5 errors | roles and subjects verified |
| G3 / G4 | geng2014 no campus / Clear Water Bay locality | 0 / 0 errors | neutral; D301 / D366 forms kept |
| K1 | gao2011 country CN | 2 errors | HK verified |
| F1 / F2 | fontaine2022 P4 locality "" / "Sydney" | 0 / 0 errors | gaps; printed Camperdown kept |
| T1 | takiguchi1996 "Tokai" | 0 errors | neutral; printed form kept |
| O1 | ong2020 org with the parent agency | 0 errors | neutral; parent rule kept |
| A1 | akiyama2021a Akiyama without 3 | 2 errors | parenthesized markers checked |
| X1 / X2 | xu2019c Gong / Yeo without the dropped contact marker | 2 / 0 errors | verified / last-author gap |
| H1 / H2 | hoessbacher2014 Hoessbacher / Leuthold without the dropped marker | 2 / 0 errors | verified / last-author gap |
| GB1 / GB2 | gao2025b Xu Yi without dropped 3 / 3 as affiliation | 2 / 1 errors | contact marker verified |
