---
title: Fresh-context audit of the lit author-affiliation batch lit_h62 (18 papers)
date: 2026-11-20
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only with --dry-run on the batch, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h62/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D366, D367, D380, D416 (5), D426, D466, D550, D557); format from the lit_h59 / lit_h60 audits
verdict: GO; 113 slots audited, 113 recorded, 0 wrong rows, 0 imprecise rows; all named extractor calls confirmed; F1 (optional, note wording in levy2012 and rombouts2024, no row change)
---

# Lit header batch audit: lit_h62 (2026-11-20)

## Scope

Batch lit_h62: 18 papers (IEEE PTL / JLT / JQE / Photonics Journal prose footnotes, Optics Express printed and single
blocks, one conference paper, two Photonics Journal cover-page papers); 113 slots, 5 papers `slots_from_header`;
144 rows. Restricted corpus: this record names only authors, orgs, units, cities, districts and countries; no paper
text is quoted and no contact, street, building, campus site, postal or box text is copied (such spans are named by
type only).

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h62 --corpus lit --codes <id> --pdf`
  (all 18), plus `--pages 2` for the cover-page papers paredes2021 and chang2018b; output kept in the session
  scratchpad `h62_audit/show/` only.
- Per slot: printed name vs the `show` author list (or the header for the 5 header-slot papers) and `compare.csv`;
  marker run in both layers; prose statement subjects and verbs; block fields (org, unit chain, more_orgs, campus,
  city, country); role; locator; notes.
- All 144 rows of `header_rows.csv` read by paper (roles primary 126, additional 17, present address 1; basis prose
  100, single 31, printed 13; all grade A). `compare.csv`: 113 `recorded`, 0 `order_differs`.
- Address / contact scan of `headers.yaml` and the derived CSVs (contact, URL, 4+ digit, street, avenue, drive,
  suite, road, building, campus, box, postal-code patterns, plus every street, ward, district, campus and box token
  printed in this batch's blocks). Hits: years in `source_id` values and papers.csv, "Telecommunications" (tel), and
  the type words "street address(es)", "contact line", "contacts" in notes. No contact, URL, postal code, street,
  ward, building, campus-site or box text anywhere (the derived CSVs included).
- Probes on scratch copies (`h62_audit/probes/probe.py` + `mk.py`, scratch `LIT_BASE`, batch name `lit_p62`,
  `cmd_check(..., dry_run=True)`; 32 runs). Dry-run check of the real batch: 0 errors, 0 warnings; totals equal the
  stamped derived files (113 slots, 113 recorded, 144 rows, 11 unmapped org strings). md5 of every repo batch file
  identical before and after the audit; `check_stamp.txt` matches `headers.yaml` (sha256 0a95000c...). Probe checks
  wrote their usual logs under `logs/` (prefix `lit_headers_check_lit_p62`, 64 files).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h62 | 18 / 18 | 113 | 113 | 0 | 0 |

- Papers ok 18, partial 0, unreadable 0; `slots_from_header` 5 (pudo2008, lu2008, zhang2013b, sanchis2007, celo2014;
  exactly the papers.csv rows with `n_authors_meta` 0, each prints the D352 line in `show`); `author_list_differs` 0;
  explicit slots 1 (liu2023b #2); order warnings 0; present addresses 1 (rombouts2024 #3); 11 unmapped org strings.
- Per paper (slots / rows): pudo2008 6 / 6; matsuo2012 9 / 9; zhou2023b 6 / 6; he2024 10 / 20; wang2023f 12 / 12;
  kourogi1993 3 / 3; lu2008 6 / 6; levy2012 6 / 8; paredes2021 4 / 4; wang2022c 7 / 7; jiang2021 2 / 2;
  liao2016 9 / 20; chang2018b 7 / 7; liu2023b 3 / 3; zhang2013b 7 / 9; sanchis2007 6 / 6; celo2014 5 / 5;
  rombouts2024 5 / 11.
- Privacy findings: 0. Notes: 2 with block / statement numbering mixed up (F1, wording only).

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (113) | 113 | 0 | 0 |
| markers (printed / prose / single, 113) | 113 | 0 | 0 |
| header position / statement subject | 113 | 0 | 0 |
| blocks (org / unit / more_orgs / locality / country) (113) | 113 | 0 | 0 |
| present addresses (1 recorded: rombouts2024 #3) | 1 | 0 | 0 |
| locators | all | 0 | 0 |
| notes (18) | 16 | 2 (levy2012, rombouts2024 numbering, F1) | 0 |

## Per-paper findings

- pudo2008 (6; single, slots from header): call 1. ok.
- matsuo2012 (9; printed): both blocks print the laboratory, then "NTT Corp.", a street, Atsugi, prefecture, postal
  code, Japan: org "NTT Corp." as printed, unit the laboratory, Atsugi, JP. Markers 1 / 2 in both layers; asterisk =
  contact line. Same structure as the 5 committed "NTT Corporation" + laboratory-unit blocks; the abbreviated org
  string is new to the corpus and already maps to `org_ntt` by name. Probe M1 ("NTT Corporation"): 4 errors. ok.
- zhou2023b (6; prose): two statements; 5 names on ZJU College of Information Science and Electronic Engineering,
  Hangzhou; Hui Yu alone on Zhejiang Laboratory, Hangzhou (committed form). Probe T1 (Hui Yu on P1): 5 errors. ok.
- he2024 (10; prose): call 6. ok.
- wang2023f (12; prose): three statements (Kwangwoon EE, Seoul; Pusan National University EE, Busan; i3system,
  Daejeon with the district printed after the city, D366); each subject names exactly its carriers (W1, Jinung Jin on
  P1: 4 errors); the hyphenated subject name split over a line break resolves. Equal contribution only in the
  funding footnote. List "Jung O. Son", "Min-Cheol Oh" (non-ASCII hyphens) match. Probe W2 (district as locality):
  0 errors, known gap (h60 G4). ok.
- kourogi1993 (3; prose, OCR layer): "The authors" statement; Tokyo Institute of Technology + Interdisciplinary
  Graduate School of Science and Engineering, Yokohama (ward printed before the city, street, prefecture and postal
  code not recorded), JP. List "M. Kourogi", "K. Nakagawa" match. ok.
- lu2008 (6; single, slots from header): call 1. ok.
- levy2012 (6; prose): call 2. Rows right; note numbering F1.
- paredes2021 (4; printed, cover page): call 4. ok.
- wang2022c (7; single, capitals): SJTU with the State Key Lab + Department of Electronic Engineering chain,
  Shanghai, CN; asterisk = contact line. ok.
- jiang2021 (2; prose): "The authors" statement; NJUPT College of Electronic and Optical Engineering, Nanjing, CN. ok.
- liao2016 (9; prose): call 2. ok.
- chang2018b (7; single, cover page): call 4. ok.
- liu2023b (3; prose): call 5. ok.
- zhang2013b (7; prose, slots from header): calls 1, 2, 7. ok.
- sanchis2007 (6; prose, slots from header): calls 1, 7. ok.
- celo2014 (5; single, slots from header): calls 1, 7. ok.
- rombouts2024 (5; prose): calls 2, 3. Rows right; note numbering F1.

## Extractor calls (verified)

1. slots_from_header (pudo2008, lu2008, zhang2013b, sanchis2007, celo2014): `show` prints "[no author list:
   slots_from_header (D352)]" for each, papers.csv `n_authors_meta` 0; authors listed in printed order, all printed
   names present (pudo2008 6, lu2008 6, zhang2013b 7, sanchis2007 6, celo2014 5). Confirmed.
2. Clause blocks (D366):
   - levy2012: statements 4 (Gaeta) and 5 (Lipson) print the school, Cornell, Ithaca, then "and also with" the Kavli
     Institute at Cornell for Nanoscale Science, Cornell, Ithaca: P4 + clause P5, P6 + clause P7, org Cornell
     University with the institute as unit. Probes V1 / V2 (clause dropped): 3 / 3 errors. Statement 2 (Saha,
     Okawachi) printed one word per line in the text layer: resolved. List "Michal F. Lipson" matches.
   - liao2016: statement 1 (3 names) SKL of Transient Optics and Photonics, XIOPM CAS, Xi'an, "also with" the
     China–U.K. Joint Research Center (en dash as printed), XIOPM CAS, Xi'an, "and also with" the University of
     Chinese Academy of Sciences, Beijing: P1 + P2 + P3. Statement 2 (5 names) P4 + P5; statement 3 (Ruan) P6.
     Probes Q1 (Zhao on P6): 6 errors; Q2 (Liao without P3): 2 errors. Org "Xi'an Institute of Optics and Precision
     Mechanics, Chinese Academy of Sciences" (CAS part of the printed name; committed form, one block with "(CAS)").
   - zhang2013b: statement 3 (Hochberg) Delaware ECE, Newark; "and also with" NUS ECE, Singapore; "and also with"
     IME, Singapore: P3 + P4 + P5. Z2 (P5 dropped): 3 errors; Z3 (Lim on P1): 4 errors.
   - rombouts2024: statement 4 (Augustin) SMART Photonics, Eindhoven, "and also with" TU/e EE + EHCI, Eindhoven: P4 +
     clause P5. R4 (P5 dropped): 3 errors.
   Confirmed.
3. rombouts2024 #3 Andreou: "was with" SMART Photonics (Eindhoven, NL) = affiliation of the work (D354; rombouts2025
   lit_h20 identical form), then a pronoun sentence "now with" Keysight Technologies, locality "Gent" as printed, BE:
   `role: present_address`. Street and postal parts of both statements (including the business-park address of
   SMART Photonics) not recorded. Probes R1 (P3 as affiliation): 2 errors (present-address cue); R2 (P2 as
   present_address): 3 errors; R3 (Andreou without P3): 3 errors (D361). Rows: primary `org_smart_photonics`,
   present address `org_keysight_technologies`. lit_h20 records "Ghent" for the same org because that paper prints
   it; both as printed (D366). Confirmed.
4. Cover pages (D366): paredes2021 and chang2018b page 1 is the Photonics Journal cover (names without markers or
   blocks); page 2 prints the marked author line (paredes2021: markers 1, 2, 2, 1 in both layers) and the blocks.
   `locator: "p.2 header"` on every block. Probes P3 (paredes2021 locators removed): 12 errors; C1 (chang2018b
   locator removed): 2 errors.
   paredes2021 block 1 prints the department, New York University, a number (box type, not recorded), "UAE": org
   "New York University", locality "", country "AE" (P4 country US: 2 errors; P1 locality "Abu Dhabi", not printed:
   2 errors). No campus: nothing between the org and the number names a campus (D301 requires a printed place); P5
   (campus "UAE") passes with 0 errors, a checker gap (a country accepted as campus), not a correct form. Block 2
   prints the department, New York University, a hyphen, Tandon School of Engineering, Brooklyn, state, postal code,
   USA: org "New York University", unit "Electrical and Computer Engineering", Brooklyn, US. The school printed after
   the org cannot join the unit (unit + org must be one contiguous segment) and is a school of the same university,
   not a second organization (D416 (5) dash-joined forms are joint organizations: Ghent University - imec, IBM
   Research - Zurich); P2 (org "New York University- Tandon School of Engineering") passes with 0 errors: neutral.
   Leaving it out keeps the org mappable to the university. Equal contribution only in a footnote (no marker).
   chang2018b: one unmarked block (HUST School of Optical and Electronic Information, Wuhan, CN), corresponding
   author footnote. Confirmed.
5. liu2023b #2: printed "Yu Wan", list "Wan Yu": the same two name parts in swapped order. Probe L1 (no explicit
   slot): 0 errors, same slot 2 (matched by name); L2 (`slot: 0` + `author_list_differs`): 1 error (D302). The
   explicit slot is redundant but kept per D550 (h36 F1 not applied; h37 moodie2024 kept); goes on the D426 review
   list as the note says. Confirmed.
6. he2024: one "The authors" statement naming BNRist and the Department of Electronic Engineering of Tsinghua
   University, Beijing, China. Recorded: org BNRist (full name with acronym), structured `more_orgs` Tsinghua
   University + department, Beijing, CN (D367). Rows: 2 per author, `org_beijing_national_research_center_for_
   information_science_and_technology` and `org_tsinghua_university`. The registry holds BNRist as its own org and
   lit_h48 records it as a separate block, so two orgs is the consistent form (ofc_h08 records the "BNRist/Department"
   slash form as Tsinghua unit, a different printed layout). Probes H1 (Tsinghua org, unit = BNRist and department):
   0 errors, 134 rows; H2 (no more_orgs): 0 errors, 134 rows (missing more_orgs not detected, known gap); H3
   (plain-string more_orgs): 0 errors. All neutral; recorded form keeps the department with its own org. Confirmed.
7. Parent / establishment text not copied:
   - sanchis2007 P3: "European Space Agency, ESTEC, Noordwijk, The Netherlands": org ESA, locality Noordwijk, NL;
     ESTEC (the agency's technical centre) not copied, as ofc_h15 Th3E.6 (ESA, Noordwijk). Probes S1 (unit "ESTEC")
     and S2 (org "European Space Agency, ESTEC") 0 errors each: neutral; the recorded form maps to
     `org_european_space_agency`. P2 DAS Photonics, Valencia, ES (D1 country NL: 2 errors).
   - zhang2013b P2 / P5: Institute of Microelectronics with the parent agency printed after it: org "Institute of
     Microelectronics", Singapore, SG (33 committed blocks in this form, 3 more with "(IME)"; maps to
     `org_astar_ime`). Probe Z1 (parent
     in the org): 0 errors, neutral; parent rule kept.
   - matsuo2012: "NTT Corp." as printed (M1 above).
   - celo2014: block prints the company, then a street address with suite, Kanata, province, Canada: org "Huawei
     Technologies Canada", locality "Kanata" (first printed place; 7 committed blocks use Kanata), CA. Probe K1
     ("Ottawa"): 2 errors. Street not recorded; the note names it by type. Confirmed.

## Fixes (exact YAML edits)

F1 (optional, wording; no row change; levy2012 line 113, rombouts2024 line 260). Both notes number the clause blocks
as if they were statements ("statements 4 and 6" in levy2012, where the printed statements are 1-5 and the Kavli
clauses belong to statements 4 and 5; "statements 1 and 5" / "statement 5" in rombouts2024, where the fifth item is
the clause block P5 of statement 4).

- Line 113 (levy2012) `note` ->

```
affiliations printed as footnote statements (prose); statements 4 and 5 (authors 5 and 6; blocks P4 and P6) add the Kavli Institute at Cornell in an and also with clause (clause blocks P5 and P7); author 6 printed Michal Lipson, author list Michal F. Lipson; states, postal codes and contacts not recorded
```

- Line 260 (rombouts2024) `note` ->

```
affiliations printed as footnote statements (prose); blocks P1 and P5 print the Eindhoven Hendrik Casimir Institute with the university (more_orgs); author 3 was with = the affiliation of the work, He is now with = present address; block P5 is the also with clause of statement 4 (author 4); author 4 printed Luc Augustin, author list Luc M. Augustin; membership designation in the author line; street addresses, postal codes and contacts not recorded
```

Probe F1 (both notes replaced): 0 errors, 0 warnings, 144 rows, totals identical. The edited file is in the session
scratchpad `h62_audit/probes/F1.yaml` (diff against the batch = exactly these two lines). After applying, re-run
`check lit_h62 --corpus lit` (the stamp hash changes).

No other fix: no slot, marker, block, field, locator or other note is wrong.

## Observations (no YAML change)

- O1 Campus field accepts a country ("UAE", probe P5): the D301 check verifies the campus is printed in the block but
  not that it is a place other than the country; checker test candidate.
- O2 Known gaps reconfirmed: missing `more_orgs` not detected (H2); district accepted as locality (W2); unit or
  parent text printed after the org accepted inside `org` (P2, S2, Z1).
- O3 paredes2021 block 1 (New York University, AE) is printed without any campus or city. The org round should not map
  it to the New York campus by name alone; whether a (New York University, AE) alias to an Abu Dhabi org is allowed is
  an org-round ruling (the block itself prints no Abu Dhabi).

## Lists for the coordinator

- D426 review list: liu2023b #2 (Yu Wan / Wan Yu, name-order swap, explicit slot kept per D550).
- D412 list: none from this batch.
- Re-record list: none.
- Org round (11 unmapped strings): DAS Photonics (ES); Kwangwoon University (KR); Nanjing University of Posts and
  Telecommunications (CN); National Research Council (CA, unit Institute for Microstructural Sciences); New York
  University (AE, see O3; US, Brooklyn); Xi'an Institute of Optics and Precision Mechanics, Chinese Academy of
  Sciences (two units); Yanshan University (CN); Zhejiang Laboratory (CN); i3system (KR).

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 0 warnings, 144 rows | batch as written |
| F1 | levy2012 / rombouts2024 notes | 0 errors, 144 rows | F1 form |
| R1 / R2 / R3 / R4 | rombouts2024 P3 affiliation / P2 present_address / Andreou without P3 / Augustin without P5 | 2 / 3 / 3 / 3 errors | roles, subjects and clause verified |
| L1 / L2 | liu2023b without slot / slot 0 + differs | 0 / 1 errors | slot matched by name; explicit slot redundant (D550 keep) |
| P1 / P4 | paredes2021 block 1 locality Abu Dhabi / country US | 2 / 2 errors | empty locality and AE verified |
| P2 / P5 | paredes2021 org with Tandon / campus "UAE" | 0 / 0 errors | neutral / checker gap (O1) |
| P3 / C1 | paredes2021 / chang2018b without p.2 locators | 12 / 2 errors | cover-page locators required |
| S1 / S2 / D1 | sanchis2007 unit ESTEC / org with ESTEC / DAS country NL | 0 / 0 / 2 errors | neutral, ESA form kept / country verified |
| Z1 / Z2 / Z3 | zhang2013b parent in org / Hochberg without P5 / Lim on P1 | 0 / 3 / 4 errors | parent rule neutral / clause and subjects verified |
| H1 / H2 / H3 | he2024 Tsinghua org + BNRist unit / no more_orgs / plain more_orgs | 0 / 0 / 0 errors (134 / 134 / 144 rows) | neutral; two-org form kept |
| M1 | matsuo2012 "NTT Corporation" | 4 errors | "NTT Corp." as printed verified |
| K1 | celo2014 locality Ottawa | 2 errors | Kanata verified |
| V1 / V2 | levy2012 Gaeta / Lipson without the Kavli clause | 3 / 3 errors | clauses verified |
| Q1 / Q2 | liao2016 Zhao on P6 / Liao without P3 | 6 / 2 errors | subjects and clauses verified |
| W1 / W2 | wang2023f Jinung Jin on P1 / district as locality | 4 / 0 errors | subjects verified / known gap |
| T1 | zhou2023b Hui Yu on P1 | 5 errors | subjects verified |
