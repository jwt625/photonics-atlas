---
title: Fresh-context audit of the lit author-affiliation batch lit_h56 (16 papers)
date: 2026-11-18
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only with --dry-run, probes on scratch copies; aggregate and the people build not run; no network; one read-only git status on the batch directory was run by mistake, nothing else from git)
scope: data/_staging/people/lit_headers/lit_h56/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D382 open item, D412, D426, D442, D572); format from the lit_h54 audit
verdict: GO with 1 note fix; 75 slots (35 list + 40 slots_from_header) audited; 67 recorded slots with 0 wrong rows; 4 imprecise (chen2010a #2 second-initial match, checker gap D382; noe2016 #1-#3 block 1 place printed on a shared line, layout gap); jeong2020 unreadable confirmed (no faithful partial recording passes); F1 jeong2020 note wording
---

# Lit header batch audit: lit_h56 (2026-11-18)

## Scope

Batch lit_h56: 16 papers (IEEE JLT / JSTQE / JQE / PTL prose footnotes, four conference papers with printed or single
blocks); 75 slots, 8 papers `slots_from_header`; 75 rows. Restricted corpus: this record names only authors, orgs,
units, cities and countries; no paper text is quoted and no contact, street, building or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h56 --corpus lit --codes <id> --pdf`
  (all 16); output kept in the session scratchpad `h56_audit/show/` only.
- Per slot: printed name vs the `show` author list and `compare.csv`; marker run (text and PDF layers); prose statement
  subjects and verbs; block fields (org, unit chain, campus, city, country); role; locator; continuation; notes.
- 28 distinct (paper, role, org, city, country, basis, org id) tuples of `header_rows.csv` read (75 rows).
- Address / contact scan of `headers.yaml` and the derived CSVs (postal-code, street, building, box, phone, contact and
  URL patterns; state / prefecture codes): clean. Notes name street and postal code only as words ("not recorded").
- Precedent scans over all committed lit / OFC `headers.yaml`: side-by-side or shared-place blocks, Siemens and
  company-plus-acronym org strings, AIST, NTT Photonics Laboratories, MIT Lincoln Laboratory, KTH forms, Zhejiang
  University COER chains, "currently with" / "and is now with" statements (cohen2024, ozdemir2021, yang2010 and others).
- Probes on scratch copies (`h56_audit/probes/probe.py`, scratch `LIT_BASE`, batch name `lit_p56`,
  `cmd_check(..., dry_run=True)`; 30 probe runs). Dry-run check of the real batch: 0 errors, 0 warnings; totals equal
  the stamped derived files (75 slots, 67 recorded, 8 no_header, 75 rows: prose 55, printed 19, single 1; primary 67,
  additional 4, present address 4; 8 unmapped org strings). md5 of every repo batch file identical before and after the
  audit; `check_stamp.txt` matches `headers.yaml` (sha256 5aa60f10...). Probe checks wrote their usual logs under
  `logs/` (prefix `lit_headers_check_lit_p56`, 60 files).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h56 | 16 / 16 | 75 | 71 (63 recorded + 8 correct no_header) | 4 (chen2010a #2; noe2016 #1-#3) | 0 |

- Papers ok 15, partial 0, unreadable 1 (jeong2020); `slots_from_header` 8 (noe2016, chen2012, wenger1997, goh1999,
  shi2009, guan2014b, lu1994, koyama2013; all print "[no author list: slots_from_header (D352)]" in `show`);
  `author_list_differs` 0; explicit slots 0; order warnings 0; 8 unmapped org strings.
- Per paper (slots / rows): noe2016 3 / 5; chen2010a 2 / 2; celo2017 7 / 7; chen2012 1 / 1; wenger1997 7 / 7;
  goh1999 5 / 5; shi2009 3 / 5; xu2017 2 / 2; guan2014b 9 / 13; jeong2020 8 / 0; lu1994 2 / 2; koyama2013 7 / 7;
  shokraneh2020 3 / 3; guo2017a 5 / 5; suzuki2018 8 / 8; liu2017 3 / 3.

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (75) | 74 | 1 (chen2010a #2, D382) | 0 |
| markers (printed / prose / single, 67 recorded) | 67 | 0 | 0 |
| header position / statement subject | 67 | 0 | 0 |
| blocks (org / unit / locality / country) (67 authors with rows) | 64 | 3 (noe2016 #1-#3, block 1 place) | 0 |
| unreadable calls (1 paper, 8 slots) | 8 | 0 | 0 |
| present addresses (4 recorded, guan2014b) | 4 | 0 | 0 |
| locators | all | 0 | 0 |
| notes (16) | 15 | 0 | 1 (jeong2020 overstatement, F1) |

## Per-paper findings

- noe2016 (3; printed, slots from header): blocks 1 Paderborn University and 2 Novoptel GmbH printed side by side on one
  line, one place line under both (unit acronym, street, postal code, Paderborn, Germany); the text and PDF layers put
  the place line after block 2. Block 1 org only (locality / country empty), block 2 Paderborn, DE. Probes N1 / N1b
  (block 1 Paderborn / DE or DE alone): 2 errors each (country not inside block 1); N2 (unit acronym on block 1): 2
  errors. The recording is the only one the checker accepts and records only what each block window prints (D249 no
  inference). Markers Noé 1,2; Koch 1,2; Mirvoda 1 in both layers. Call 2 confirmed; slots #1-#3 imprecise (place of
  block 1 printed on the shared line, not recordable). Details under call 2.
- chen2010a (2; prose): "The authors" statement: National Chiao Tung University, Department of Photonics and Institute of
  Electro-Optical Engineering, Hsinchu, TW. #2 printed Chia-Hsiang Chiu (initials C, H), list C. L. Chiu (C, L): matched
  automatically (no `slot:` in the YAML; the brief's "explicit slot 2" is the automatic match). Call 1 confirmed,
  imprecise (D382 gap).
- celo2017 (7; printed): Huawei Technologies Canada Co., Ltd., Ottawa, CA; Huawei Technologies Co. Ltd., Shenzhen, CN.
  Markers (Liu 2, the others 1) in both layers; asterisk = contact line. List forms Patrick Dumais, Dominic J.
  Goodwill, Jia Jiang, É. Bernier match automatically. ok.
- chen2012 (1; single, slots from header): figure text precedes the title in the extraction; one author, one unmarked
  block (same NCTU department, Hsinchu; "Taiwan, R.O.C" printed -> TW; probe CH1 CN: 2 errors). ok.
- wenger1997 (7; prose, slots from header): three statements, Siemens HL Regensburg (Wenger, Acklin, G. Müller), Siemens
  ZT Munich (Schienle, J. Müller, Eichinger), Siemens ÖN Munich (Bellermann); DE. Probe W2 (swap the two Müllers): 8
  errors, so the J. / G. initials are verified. Call 3 confirmed (see below). ok.
- goh1999 (5; prose, slots from header): NTT Photonics Laboratories (authors 1-4) and NTT Network Innovation
  Laboratories (Hattori); each statement prints only a prefecture and the country: locality empty, JP (D288; 2 committed
  blocks of the same org with empty locality). Probe G1 (Ibaraki-ken): 0 errors, known checker gap (prefecture accepted,
  D572). ok.
- shi2009 (3; prose, slots from header): call 4, see below. ok.
- xu2017 (2; prose): Zhejiang University with the SKL / COER / provincial key laboratory chain as printed, Hangzhou, CN.
  ok.
- guan2014b (9; prose, slots from header): call 5, see below. ok.
- jeong2020 (8; unreadable): see "jeong2020" below. Unreadable confirmed; F1 note wording.
- lu1994 (2; prose, slots from header): call 6. ok.
- koyama2013 (7; printed, capitals, slots from header): Waseda University Faculty of Science and Engineering; Hitachi
  Ltd. Central Research Laboratory; Waseda University Green Computing System Research Organization; all Tokyo, JP.
  Markers 1,1,1,2,2,3,1 in both layers (probe K1 Matsushima marker 1: 3 errors). ok.
- shokraneh2020 (3; prose): McGill University ECE, Montréal, CA (province, postal code not recorded). ok.
- guo2017a (5; prose): Shanghai Jiao Tong University with the SKL + Department of Electronic Engineering chain,
  Shanghai, CN. ok.
- suzuki2018 (8; prose): call 7. Hasegawa: Furukawa Electric Co., Ltd. + Telecommunications and Energy Laboratory,
  Ichihara, JP. Author line split by ORCID marks and membership designations; all 8 names match the list. ok.
- liu2017 (3; prose): Peking University with the SKL + School of EECS chain, Beijing, CN; #3 printed Zhiping Zhou, list
  Zhiping James Zhou (dropped middle name, automatic). ok.

## jeong2020: is a partial or ok recording possible?

Printed (p.1 footnote): statement 1 (author 1) is with the Photonics Electronics Technology Research Association
(PETRA), Tsukuba, Japan, and, in the same sentence without a verb, "currently with" a University of Suwon department
(Hwaseong-si, Korea); statement 2 (authors 2-6 and 8) PETRA, Tsukuba, Japan; statement 3 (author 7) the National
Institute of Advanced Industrial Science and Technology, Tsukuba, Japan. Author 8's family name is hyphenated across a
line in the statement 2 subject. Both layers identical.

Checker reading: `VERB_RE` needs is / are / was / were before "currently with" and `CLAUSE_RE` needs "and (is / are /
also) with", so neither stops the statement 1 window; the cue lands inside it. In the committed ozdemir2021 case ("and
is now with") `VERB_RE` stops the window, which is why that work affiliation was recordable and this one is not.

| probe | recording | result |
|---|---|---|
| J1 | P1 PETRA (affiliation) + clause P2 Suwon (present_address), P3, P4; Nakamura unreadable | 4 errors (P1 cue; clause anchor not found) |
| J2 / J3 | P1 PETRA affiliation only; Jeong readable / unreadable | 2 / 2 errors (P1 cue) |
| J4 | no P1, Jeong unreadable; P3 statement 2, P4 statement 3 | 16 errors (P3 lands on statement 1, its first field; subject and D361 coverage) |
| J9 | cohen2024 form (Jeong omitted, `author_list_differs`) | 14 errors (same as J4) |
| J6 / J5b | Nakamura readable | +2 errors (hyphenated subject name, gap G1 of D426) |
| J7 | Jeong printed as S.-H. Jeong | 16 errors |
| J5 | P1 PETRA with `role: present_address`, Jeong unreadable, Nakamura unreadable | 0 errors |

J5 is the only recording that passes, and it states that PETRA is a present address, which the print contradicts (it
is the affiliation of the work). No row derives from P1 (its only carrier is unreadable), and J5 would yield 6 correct
slots (5 PETRA, 1 AIST), but a false role in the YAML is invented data: not recommended. Every faithful recording fails,
so `unreadable` is the right call (extractor confirmed). The note's "fails any recording of it" is too strong (J5):
F1.

## Extractor calls (verified)

1. chen2010a #2: automatic match to list slot 2 (C. L. Chiu). Probe C1 (`slot: 0` + `author_list_differs`): 1 error
   (D302), because `strict_compatible` accepts equal initial counts without comparing them (D382, open). Same handling
   as yeh2024 #14 / #24 (lit_h34) and hsu2025 #4 (lit_h35). Same NCTU row either way. Imprecise, not fixable now; D426
   review list and D412 correction file (position 2 list form vs printed Chia-Hsiang Chiu).
2. noe2016 side-by-side blocks with one shared place line: no committed side-by-side marked-block precedent with a
   shared place line exists (scan of every lit / OFC batch for a printed block with empty place followed by a placed
   block: 5 hits, sun2026a, caillaud2021, ofc Th2A.3 / Th2A.19 / Th2A.44, all blocks that print no place of their own).
   The nearest precedents are the shared trailing org (lit_h17 foster2006, lit_h22, lit_h44): the checker cannot attach
   text printed once after the last block to earlier blocks, and the corpus records only what lies inside each block.
   noe2016 follows that rule (block 1 has its own org, so it stays recordable with an empty place). Consistent. The unit
   acronym is not tied by the print to one block; probe N3 (acronym as Novoptel unit) passes (0 errors) but would put a
   university department code on the company row: not recording it is right. Keep; re-record list item.
3. wenger1997 "Siemens HL" / "Siemens ZT" / "Siemens ÖN" kept whole: printed as one name without a comma; probe W1
   (org Siemens + unit HL / ZT / ÖN) 0 errors, neutral. Committed company-plus-acronym strings are kept whole ("CEA
   LETI" x2, "Telefonica CTO"); the split form is used only where a comma separates them ("CEA", "LETI", 11 blocks).
   Keep; org round (no Siemens org in the registry; three division strings, one parent).
4. shi2009 P1 unit chain ending in the Joint Research Center of Photonics of the Royal Institute of Technology (Sweden),
   org Zhejiang University, Hangzhou, CN: the joint centre's printed name ends with "and Zhejiang University", so the
   org is the tail of that name and the place (Hangzhou, China) is Zhejiang University's; no KTH row is created for a
   Hangzhou block. Probe S1 (unit without the joint centre): 2 errors (unit and org not contiguous), so the chain must
   include it. P2 clause and P3 KTH copied as printed "Royal institute of Technology (KTH)" (lower-case i in both
   layers; matching folds case), Department of Microelectronics and Applied Physics, Kista, SE (lit_h04 KTH Kista
   precedent). Keep.
5. guan2014b: P1 "are with" UC Davis ECE (authors 1, 2, 6, 8, 9); P2 / P4 / P6 / P8 "was with" UC + campus Davis
   (affiliation of the work, role affiliation, D354); P3 Alcatel-Lucent Bell Laboratories, Holmdel, US; P5 Shanghai
   Jiao Tong University + Department of Electronic Engineering, Shanghai, CN (district Minhang in the note, D366); P7
   NTT Photonics Laboratories, Atsugi-shi, JP (D366 "-shi" kept; prefecture not recorded); P9 MIT + Lincoln Laboratory,
   Lexington, US (5 committed blocks in this split form; probe GU4 whole-name form 0 errors, neutral); all four
   `present_address` (probe GU1 P3 as affiliation: 2 errors). GU2 (Minhang) and GU3 (no campus) 0 errors, neutral;
   recorded forms follow D366 / D301. Keep.
6. lu1994 statement split after "University of", continuation "Pittsburgh" at a line start later on p.1 in both layers:
   `continued: "Pittsburgh"` required (probe L1 without it: 4 errors) and verifying (L2 wrong city: 2 errors).
   goh1999 prefecture-only statements: locality empty (G1 neutral, known gap). Keep.
7. suzuki2018 org "AIST" as printed (the statement prints only the acronym; leading article not copied, corpus practice
   for prose; 2 committed AIST blocks, lit_h07 / lit_h27; row maps to org_national_institute_of_advanced_industrial_science_and_technology
   by alias). Probe SU1 (full institute name): 4 errors (not printed). Keep.
8. The 8 `slots_from_header` papers are exactly the papers.csv rows with `n_authors_meta` 0 and print the D352 line in
   `show`. Confirmed.

## Fixes (exact YAML edits)

F1 (jeong2020 note, factual wording). Probe J5 shows one recording of statement 1 that passes (false present-address
role); the note should say that no recording with the true role passes. Probe F1: 0 errors, rows unchanged.

In `lit:jeong2020` replace

```yaml
so the cue falls inside the statement 1 window and fails any recording of it,
```

with

```yaml
so the cue falls inside the statement 1 window and fails any recording of it under its true role (affiliation of the work),
```

(inside the `note:` string; nothing else in the paper changes).

No other fix: no slot, marker, block or field is wrong.

## Observations (no YAML change)

- O1 shi2009 clause coverage gap: probe S2 (KTH clause block removed from Shi and He) passes with 0 errors. The
  coverage loop treats the ")" of "(Sweden)" inside statement 1 as a sentence boundary (`PROSE_CUT_RE`) and skips the
  "and also with" clause as body text. The extractor recorded the clause, so this batch is unaffected; checker test
  candidate (a closing parenthesis inside a statement is not a boundary).
- O2 noe2016: side-by-side marked blocks with one shared place line are a new layout gap (place printed once for both
  blocks); with a layout form for it, block 1 would get Paderborn, DE.
- O3 "and currently with" (no verb) is a new clause form beyond the D426 / G6 list ("and is now with"); jeong2020 is the
  first case. A clause anchor for it (with `role: present_address` on the clause) would make jeong2020 recordable
  except author 8 (hyphenated subject name, G1).
- O4 checker accepts a prefecture as locality (goh1999 Ibaraki-ken, probe G1), as in the h54 Y1 case (D572 gap).

## Lists for the coordinator

- D426 review list / D412 correction file: chen2010a #2 (list C. L. Chiu, printed Chia-Hsiang Chiu; D382 gap; another
  equal-count case like yeh2024 #14 #24, hsu2025 #4, lai2025 and the DevLog-011 D382 list).
- Re-record list: jeong2020 (after an "and currently with" clause anchor and the G1 hyphenated-subject fix): P1 PETRA,
  Tsukuba, JP + clause Suwon Department of Electronic Material Engineering, Hwaseong-si, KR (`present_address`) for
  author 1; PETRA, Tsukuba, JP for authors 2-6 and 8; AIST full name, Tsukuba, JP for author 7. noe2016 block 1 place
  (O2).
- Org round (8 unmapped strings): Alcatel-Lucent Bell Laboratories; NTT Photonics Laboratories (5 rows; child of NTT
  like the mapped NTT Network Innovation Laboratories); National Chiao Tung University (3 rows); Novoptel GmbH; Royal
  institute of Technology (KTH) (alias of KTH); Siemens HL / Siemens ZT / Siemens ÖN (Siemens divisions).

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 0 warnings | batch as written |
| N1 / N1b | noe2016 block 1 Paderborn + DE / DE only | 2 / 2 errors | empty place forced |
| N2 / N3 | noe2016 unit acronym on block 1 / block 2 | 2 / 0 errors | block 1 impossible; block 2 neutral, not recorded (call 2) |
| C1 | chen2010a #2 `slot: 0` + `author_list_differs` | 1 error (D302) | automatic match forced (D382) |
| W1 / W2 | wenger1997 Siemens + unit / Müller markers swapped | 0 / 8 errors | neutral, whole kept / initials verified |
| G1 | goh1999 locality Ibaraki-ken | 0 errors | checker gap; empty kept |
| S1 / S2 | shi2009 unit without joint centre / clause removed | 2 / 0 errors | chain required / coverage gap O1 |
| GU1 | guan2014b P3 as affiliation | 2 errors | present-address role required |
| GU2 / GU3 / GU4 | guan2014b Minhang / no campus / MIT whole name | 0 / 0 / 0 errors | neutral; D366 / D301 / precedent forms kept |
| L1 / L2 | lu1994 no `continued` / wrong city | 4 / 2 errors | continuation required and verified |
| SU1 | suzuki2018 full AIST name | 4 errors | acronym as printed required |
| CH1 | chen2012 country CN | 2 errors | TW verified |
| K1 | koyama2013 Matsushima marker 1 | 3 errors | markers verified |
| J1-J9 | jeong2020 recordings (table above) | 2-18 errors; J5 0 | unreadable kept; J5 rejected (false role) |
| F1 | jeong2020 note wording | 0 errors | fix |
