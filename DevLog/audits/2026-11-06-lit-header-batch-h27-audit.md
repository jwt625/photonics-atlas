---
title: Fresh-context audit of the lit author-affiliation batch lit_h27 (22 papers)
date: 2026-11-06
auditor: Claude (fresh context; wrote only this record; headers.yaml, derived files, scripts, tests, people and registry data not edited; aggregate and the people build not run; no network; no git except one read-only `git status --short` of the batch directory, run in error at the end)
scope: data/_staging/people/lit_headers/lit_h27/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369, D400-D466; format and precedent from the 2026-11-06 h25 audit
verdict: GO for the people rebuild (no slot wrong); 180 slots audited, 147 ok, 33 imprecise, 0 wrong; F1 (27 slots, locator only) fixable now; F2 (3 slots, unit on the wrong org of a joint pair) waits on a ruling or a checker change; C1 (3 slots, present addresses) waits on the D442 cue gap; nothing applied
---

# Lit header batch audit: lit_h27 (2026-11-06)

## Scope

Batch lit_h27 (22 papers: 11 IEEE footnote-prose papers, 3 Nature-family papers, 8 preprints / other journals; 180
author-list slots plus 1 header-only author; 233 rows). Restricted corpus: this record names only authors, orgs, units,
cities and countries; no paper text is quoted and no contact, street, building, site or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h27 --corpus lit --codes <id> --pdf`
  (all 22, output kept in the session scratchpad only). No paper has a cover page or a later-page block; `--pages` was
  not needed. Both text layers carry every marker legibly (qu2024 bracketed symbols, yan2025 / perez2017 markers on the
  next line, wang2024 letter markers); no page render needed.
- Per slot: printed name vs `compare.csv` slot, printed marker run vs `markers` + `dropped_markers`, prose subject vs
  carriers, block fields vs the print (org, unit, campus, city, country), present address, parents, locator. All 73
  distinct (org, unit, place, role, id) tuples of `header_rows.csv` read; no wrong mapping.
- Author lists read from `cache/literature/merged.jsonl` for zhao2025, zhang2022b and spiga2016 (DOI lookup), and the
  name forms of the four automatic matches counted across all merged records with their co-authors.
- Missed blocks: cue scan of the whole `text.md` of all 22 (now with / at, present / current address, current / present
  affiliation, currently, presently, also with, was / were with, on leave, visiting, formerly, deceased, permanent
  address). Header hits: qu2024 (two current-address lines), raghunathan2025 (present affiliation), raptakis2024,
  yu2023a, zhong2025 (clauses, recorded), spiga2016 (was with / now with, recorded). All other hits are biographies on
  later pages or body text. No missed block.
- Claims and the five extractor questions tested with dry-run probes on a scratch copy of the batch (`probe.py`, via the
  module's `LIT_BASE`; md5 of every repo batch file asserted unchanged after the run).
- Lit locator precedent: every committed lit paper whose note says the blocks are a first-page footnote (21 papers in
  lit_h03-lit_h24) was tabulated with its locators.
- Stamp: `check_stamp.txt` matches `headers.yaml` (sha256 4c6f6b95...). `headers.yaml` mtime 22:47:20, stamp and
  derived files 22:47:27. Repo batch files untouched by this audit.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h27 | 22 / 22 | 180 | 147 | 33 | 0 |

- Rows 233 (all grade A: printed 122, prose 103, single 8; primary 210, additional 22, present address 1); recorded 180,
  no_header 0; papers ok 22, partial 0, unreadable 0; `author_list_differs` 1 (zhao2025, header-only author with
  `slot: 0`, no row); present addresses 1 (spiga2016 #4); 28 unmapped org strings; `order_differs` false on all 180.
- Imprecise by cause: fixable now 27 (F1 locator only: perez2017 9, yan2025 13, zhao2025 5); ruling or checker change 3
  (F2 spiga2016 #2 #5 #6); checker gap 3 (C1 qu2024 #6 #8, raghunathan2025 #5). The 33 slots are distinct.
- Per paper (slots / rows): perez2017 9 / 10; qu2024 13 / 35; raghunathan2025 7 / 9; raptakis2024 11 / 21; shindo2023
  10 / 10; song2020 6 / 6; spiga2016 8 / 12; stone2026 6 / 10; sun2021 12 / 12; sun2025a 6 / 6; suzuki2020 7 / 7;
  wang2024 14 / 16; wen2022 11 / 11; wu2025a 8 / 8; xie2022 3 / 3; yamaoka2024 11 / 11; yan2025 13 / 16; yu2023a 3 / 6;
  zhang2022b 9 / 9; zhao2025 5 / 6; zhong2025 6 / 7; zhou2022 2 / 2.

## Findings and proposed fixes (not applied)

| # | paper, slots | rating | evidence (locator) | proposed fix (field: before -> after) |
|---|---|---|---|---|
| F1 | perez2017 #1-#9, yan2025 #1-#13, zhao2025 #1-#5 (and the header-only author) | imprecise, fixable now (locator only; fields correct) | p.1: in all three Nature-family papers the affiliation list is printed at the foot of page 1, after the abstract / body start; the paper notes say so. Contract: `p.1 footnote` for a block printed as a first-page footnote; all 21 committed lit papers with that note carry `p.1 footnote` on every block (e.g. lit_h20 lihachev2022, luo2014; lit_h21 xue2026, yan2017; lit_h24 fan2021, li2025a). Here the blocks carry the default, so 32 rows say `p.1 header`. Probe L1: 0 errors, rows unchanged | every block of perez2017 (markers 1-3), yan2025 (markers 1-4) and zhao2025 (markers 1-2): add `locator: "p.1 footnote"`; no other change |
| F2 | spiga2016 #2 (Wouter Soenen), #5 (Xin Yin), #6 (Johan Bauwelinck), block P2 | imprecise (unit attached to the wrong org of the pair; both orgs present, nothing invented) | p.1 footnote: the statement prints the department, then the Interuniversity Microelectronics Centre, then Ghent University, then Ghent, Belgium. D466 (bayoumi2025) rules this comma-joined pair after a unit: Ghent University carries the unit, the centre goes to `more_orgs`; committed rows of the same department give it to Ghent University (lit_h01 P1, lit_h05 P1). The recorded form puts the department on the centre's row. Probe S1 (D466 form): 2 errors, unit and org not contiguous (the 38-letter centre name exceeds the 10-character unit-org gap; bayoumi2025 passes only because the short form imec fits). Probe S2 (D466 form + `skip_between` naming the centre): 0 errors. Probes S3 / S4 (no unit): 4 errors each (first field) | after a ruling or the G2 checker change (see question 1): P2 `org`: "Interuniversity Microelectronics Centre" -> "Ghent University"; `more_orgs`: ["Ghent University"] -> ["Interuniversity Microelectronics Centre"]; `unit` unchanged; with option (a) also `skip_between: "Interuniversity Microelectronics Centre"`. `note`: "(the centre name is too long for the unit-org gap, so the centre is recorded as org with the department as unit and Ghent University as a further organization, unlike D466 bayoumi2025)" -> "(recorded as Ghent University with the department as unit and the centre as a further organization, D466 bayoumi2025)". Rows stay 12; the unit moves to the `org_ghent_university` row |
| C1 | qu2024 #6 (Houssein El Dirani), #8 (Corrado Sciancalepore); raghunathan2025 #5 (Chaitali Joshi) | imprecise, not fixable now (present-address rows missing; none wrong) | p.1 header, both layers: qu2024 prints two bracketed-symbol lines with the cue Current address (LIGENTEC SA, Corbeil-Essonnes, France; Soitec SA, Bernin, France), carried by authors 6 and 8; raghunathan2025 prints a dagger line with the cue Present affiliation (Google Quantum AI, Santa Barbara, US), carried by author 5. Probe Q1 (qu2024 block "+" as present address): 2 errors, block lacks a present-address cue; probe G1 (raghunathan2025 dagger block): 2 errors, marker + first field not adjacent (the cue sits between them). Same gap as D442 / D466 (poulton2017, stanton2020, zhang2025c) and the Current address lines of lit_h05 / h16 / h17. The marks are symbols, so no `dropped_markers` entry is needed (D286d) | after the cue fix: qu2024 add `{marker: "+", basis: printed, role: present_address, org: "LIGENTEC SA", locality: "Corbeil-Essonnes", country: "FR"}` and `{marker: "++", basis: printed, role: present_address, org: "Soitec SA", locality: "Bernin", country: "FR"}` after block 2; authors 6 / 8 `markers: ["2", "+"]` / `["2", "++"]`. raghunathan2025 add `{marker: "†", basis: printed, role: present_address, org: "Google Quantum AI", locality: "Santa Barbara", country: "US"}`; author 5 `markers: ["1", "†"]`. Rows 233 -> 236; drop the gap sentences from both notes |

Any change to the YAML changes its hash: re-run `check lit_h27 --corpus lit` afterwards to refresh the stamp.

Points checked and correct (asked for in the brief):

- zhao2025: the header prints 6 authors; the `merged.jsonl` list has 5 (Ping Zhao, Vijay Shekhawat, Marcello Girardi,
  Zonglong He, Peter A. Andrekson). Victor Torres-Company, printed 5th with marker 1 (Chalmers), is in no slot:
  `slot: 0` + `author_list_differs` correct (probe N1, slot removed: "matches 0 metadata slots"). A missing author is a
  list defect: D412 correction file (as chang2026a Yulin Wu, D416 (3)).
- zhang2022b #3: printed (author line and statement subject) Deng Mao; list Mao Deng. Same two name parts in swapped
  order, the only candidate of 9 slots. Merged records with David V. Plant as co-author carry both orders (Mao Deng in
  the 2022 records, Deng Mao in the 2021 and 2023 ones), so the person build may split him. Match accepted; add to the
  D426 review list (order swap).
- yan2025 #13: printed Qi Jie Wang, list Qijie Wang: joined given name, same syllables; ok.
- spiga2016 #4: printed Dean Maximilian Schoke (statement D. M. Schoke), list Dean Schoke: dropped middle name of a
  distinctive family name; ok. #5: printed Xin Yin (statement X. Yin), list Xin Liang Yin; the list form is the upstream
  name (over 100 merged-record occurrences, Johan Bauwelinck co-author in most), not an extraction artefact; dropped given-name
  syllable or middle name of a common family name. Match accepted (only candidate, same group, same co-authors); add to
  the D426 review list (as fang2010, feng2011, bolk2018 #6).
- qu2024 #6 #8, raghunathan2025 #5: present addresses unrecorded, gap confirmed (C1).
- stone2026 (4 blocks) and xie2022 (2 blocks): US state codes and postal codes only, no country printed: `country: ""`
  required (D249; probe N2, US on stone2026 block 1: "not printed in this block"). xie2022 campus College Park (D301)
  correct; stone2026 block 4 joint form (Joint Quantum Institute + NIST + University of Maryland, no campus) matches
  lit_h02 and lit_h14.

## Extractor questions: recommendations

1. spiga2016 P2 (centre as org, department as unit, Ghent University in `more_orgs`): not the D466 form, so rated
   imprecise (F2). D466 is explicit for this structure (unit, imec, Ghent University), and the committed records of
   the same department carry it under Ghent University (lit_h01 P1, lit_h05 P1; lit_h05 G1 dash-joined). The only
   obstacle is the checker's 10-character gap (S1). Options: (a) now, with `skip_between` naming the centre (S2: 0
   errors); D380 defines `skip_between` for building / site spans that are never recorded, so this needs a ruling that a
   printed org also listed in `more_orgs` may fill it; (b) a checker change (G2): the unit-org gap may be exactly a
   `more_orgs` org of the same block, as whole words, which also turns the bayoumi2025 pass from incidental into
   verified. Recommended: (b), then re-record with the D466 form; keep the YAML as is until then (no wrong org, both
   orgs present). If the coordinator prefers no checker work, (a) gives the same rows now.
2. yu2023a P1 (Engineering Research Center of Photonic Design Software, Ministry of Education as one org): accept. The
   statement prints no host university; the ministry is the designating body, part of the centre's official name, not
   a parent printed after it. Recording the ministry as org (probe Y1: 0 errors, so a contract call) would attribute
   three authors to a ministry. Precedent: lit_h19 guo2024 P2 / P6 (Key Laboratory of Opto-electronic Information
   Technology, Ministry of Education, no university, one org) and ofc_h11 (Engineering Research Center of Intelligent
   Technology for Geo-Exploration, Ministry of Education, one org). The org round maps it as a new org.
3. raptakis2024 P1 / P4 (Institute of Communication and Computer Systems as org, Photonic Communications Research
   Laboratory as unit, National Technical University of Athens in `more_orgs`): accept. The institute is a separate
   organization, so the contract's two-organizations rule puts it in `org` / `more_orgs`, not in the unit chain
   (probe R1, NTUA as org with lab + institute as unit: 0 errors, but makes an org a unit). With NTUA as org and the
   institute in `more_orgs`, unit and org are not contiguous (R2: 4 errors) unless the `skip_between` device of
   question 1 is used (R3: 0 errors). No committed record of this laboratory exists, so the D466 "org of the committed
   records" rule does not pull it to NTUA; the printed parent directly after the unit takes it. Committed OFC rows
   record the institute as its own org (ofc_h04, ofc_h11). Both orgs map (`org_institute_of_communication_and_computer_systems`,
   `org_national_technical_university_of_athens`).
4. sun2021 P5 (Wuhan National Lab for Optoelectronics as org, the school as unit): accept. Neither Huazhong University
   of Science and Technology nor any other university is printed; inferring it is not allowed (D249, never invent).
   Dropping the school fails (probe W1: first field not printed, 4 errors), and the chain rule copies the printed
   sub-unit chain on the only printed org. Precedent: WNLO as its own org when no university is printed (lit_h19 guo2024
   P3, ofc_h03, ofc_h14); with the university printed, the school + WNLO chain is a HUST unit chain (lit_h16, lit_h18)
   or WNLO + HUST two orgs (lit_h02, lit_h12, lit_h21, lit_h26). The printed short form "Lab" maps by alias in the org
   round (lit_h12 printed a similar short form).
5. sun2021 P1 / P3 / P7 (Southeast University with a campus name after a dash, no `campus` field): accept. D301 is for a
   place that names a distinct institution or campus of a multi-campus or homonym org (CUHK Shenzhen, UC Davis, IIT
   Delhi, UMD College Park), where the registry needs a separate org; here the printed name is a site of the same
   university in the same city, and a campus would block the `org_southeast_university` mapping for 7 slots (D301: no
   parent fallback) for no identity gain. The checker accepts either (probe C1: 0 errors), so this is a contract call.
   Precedent for site names left out: lit_h10, lit_h13, h25 moscosomartir2017 block 3 and tsakyridis2020. The dash is
   not a D416 (5) / D426 joint-org dash (one org plus a site, not two orgs).

## Privacy and as-printed scan

- `privscan.py` (session scratchpad) over every line of `headers.yaml`, `header_rows.csv`, `compare.csv`,
  `unmapped_orgs.csv`, `papers.csv`, `check_stamp.txt` and this record: contact / URL patterns, street and building
  words, digit runs of 4 or more, and 150 postal and street strings taken from the header pages of all 22 papers.
  Result: 0 contact or URL hits and 0 printed postal / street strings in all files. Street-word hits only in YAML notes
  that say street addresses / building numbers were not recorded. Digit runs: paper-id years only (YAML, CSV), the
  stamp hash, and in this record also dates, the check pid and the hash prefix; none is a postal code.
- As printed (kept, correct): stone2026 National Institute for Standards and Technology (printed form; unmapped, org
  round); sun2021 Institute of Semiconductor (singular); yamaoka2024 NTT corporation (lower-case c, maps to `org_ntt`);
  qu2024 block 5 training-centre name with its printed comma; wen2022 IBM Research Europe dash form (D426); zhong2025
  SITRI with its micro sign. Parents not copied: wang2024 A*STAR after IMRE / IME (contract example). The sun2021 note
  names the campus site word it leaves out (same practice as the lit_h10 / lit_h13 / h25 notes); no field carries it.
- No `skip_prefix` or `skip_between` in this batch.

## Commands (2026-11-06, log times)

| Command | Result |
|---|---|
| `show lit_h27 --corpus lit --codes <id> --pdf`, all 22 papers, 22:48 | headers and author lists read (scratchpad only) |
| `check lit_h27 --corpus lit --dry-run` 22:49:15 (pid 23741) | 0 errors, 0 warnings; slots 180, recorded 180; rows 233 (grade A 233; primary 210, additional 22; printed 122, prose 103, single 8); papers ok 22; multi-affiliation slots 17; present addresses 1; 28 unmapped org strings |
| `probe.py` on a scratch copy, dry-run, 22:56:01-22:57:42 (pid 28342) | results below; repo batch files md5 unchanged |
| `privscan.py` over the 6 batch files and this record | 0 contact, 0 printed postal / street strings |

| probe | change | result | reading |
|---|---|---|---|
| S1 | spiga2016 P2 D466 form (org Ghent University, centre in `more_orgs`) | 2 errors, unit and org not contiguous | F2 blocked by the 10-character gap |
| S2 | S1 + `skip_between` naming the centre | 0 errors | question 1 option (a) |
| S3 / S4 | spiga2016 P2 without unit (either org first) | 4 / 4 errors, first field | the unit must stay |
| Y1 / Y2 | yu2023a P1 ministry as org + centre as unit / centre without ministry | 0 / 0 errors | question 2 is a contract call |
| R1 | raptakis2024 P1 P4 NTUA as org, lab + institute as unit chain | 0 errors | contract call (two-organizations rule decides) |
| R2 / R3 | raptakis2024 NTUA as org, institute in `more_orgs` without / with `skip_between` | 4 errors / 0 errors | same gap as S1 |
| W1 | sun2021 P5 without the school | 4 errors, first field | question 4 |
| C1 | sun2021 P1 with a campus field | 0 errors | question 5 is a contract call |
| L1 | perez2017, yan2025, zhao2025 blocks `p.1 footnote` | 0 errors | F1 |
| Q1 | qu2024 author 6 current-address block | 2 errors, no present-address cue | C1 confirmed |
| G1 | raghunathan2025 author 5 present-affiliation block | 2 errors, marker + first field | C1 confirmed |
| N1 | zhao2025 `slot: 0` removed | 1 error, matches 0 slots | slot 0 required |
| N2 | stone2026 block 1 country US | 2 errors, not printed | empty country required |
| N3 | spiga2016 Xin Yin moved from P2 to P1 | 4 errors (D354) | prose carriers bound |

## Checker gaps observed (scripts not edited)

- G1 Present-address cues Current address and Present affiliation (D442): not in the cue list; a cue between a symbol
  marker and the first field also breaks marker adjacency (qu2024, raghunathan2025; probes Q1, G1).
- G2 Unit-org gap: a joint org printed between the unit and the org that D466 says carries the unit is accepted only
  when it is at most 10 letters (bayoumi2025 imec passes, spiga2016 full centre name fails; probes S1, R2). Proposed: the
  gap may be exactly one `more_orgs` org of the same block, matched as whole words.
- G3 (minor) Locator vs layout: a first-page footnote block passes with the default `p.1 header` locator (F1); the
  checker cannot tell header from footnote, so the contract rule is unverified.

## Coordinator questions

1. Apply F1 (locators on perez2017, yan2025, zhao2025) now, then re-run `check lit_h27 --corpus lit`? Recommended: yes,
   before `aggregate`; rows unchanged (233), locators of 32 rows corrected.
2. F2 / question 1: (a) allow `skip_between` to carry a printed org that is also in `more_orgs` and re-record
   spiga2016 P2 now, or (b) implement G2 and re-record after it? Recommended: (b).
3. Accept the recommendations on questions 2-5 as recorded?
4. Lists: zhao2025 Victor Torres-Company (missing from the author list) to the D412 correction file; zhang2022b #3
   (order swap) and spiga2016 #5 (dropped syllable) to the D426 review list; qu2024 #6 #8 and raghunathan2025 #5 to the
   re-record list after the G1 cue fix.

## Verdict

GO. No slot carries a wrong person, org, city, country or marker, nothing is invented, no block is missed, and no
address or contact text is recorded. 27 slots should take the footnote locator (F1, field additions only); 3 slots
carry their department on the joint centre instead of Ghent University (F2, waiting on question 2); 3 slots wait on
the known present-address cue gap and are correct as far as recorded.
