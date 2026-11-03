---
title: Fresh-context audit of the lit author-affiliation batch lit_h20 (35 papers)
date: 2026-11-02
auditor: Claude (fresh context; wrote only lit_h20/headers.yaml, the derived files the checker writes, and this record; aggregate not run)
scope: data/_staging/people/lit_headers/lit_h20/headers.yaml; both header contracts; DevLog-011 D350-D369, D380, D400-D426; previous audit 2026-10-30-lit-header-batch-h17-audit.md
verdict: GO for the people rebuild after the fixes below (applied; check 0 errors, 4 warnings); 0 wrong and 15 imprecise slots in 261 audited (2 fixed, 13 checker gaps)
---

# Lit header batch audit: lit_h20 (2026-11-02)

## Scope

Batch lit_h20 (35 papers, 261 author-list slots), extracted 2026-11-02 (extractor check: 0 errors, 4 warnings; 34 ok /
1 partial; 260 / 261 slots recorded; 344 rows). lit_h19 and lit_h21 were not touched. Restricted corpus: this record
names only authors, orgs, units, cities and countries; no paper text is quoted and no contact, street, building, postal
or box code is copied.

## Method

- Every paper read with `env -u VIRTUAL_ENV uv run python scripts/ofc_headers.py show lit_h20 --corpus lit --codes <id>
  --pdf` (all 35), through a display filter (`view.py`, session scratchpad `lit_h20_audit/`) that keeps the whole header
  and every later line carrying an org, cue, country or marker word; the dropped-line count was printed per paper.
  `--pages 2` for the two cover-page papers (kharas2020, pathak2014a), `--pages 8` for oser2019 (triangle mark). Full
  statement context read separately for lindenmann2014, palmer2026, primiani2019.
- Findings formed from the page first; extractor notes then tested claim by claim.
- Selection: all 35 papers (full coverage):
  - (a) explicit `slot:` / order differs: palmer2026 #2, qiu2026 #9 (and order), spektor2023 #4;
  - (b) partial: lee2024; prose: lim2021, lindenmann2014, marin2023, palmer2026, primiani2019, rombouts2025, saghaei2026;
    present addresses: lihachev2022, primiani2019, rombouts2025 (recorded), oser2019, stanton2020 (not recorded by the
    extractor); single: kharas2020, pita2023, salehzadeh2020;
  - (c) flagged items: empty countries (lindenmann2014, palmer2026 by hyphenation; liang2017, roy2026 not printed),
    two-org blocks (oser2019, primiani2019 P4, rombouts2025 P1 / P5, palmer2026 P4), parents (lim2021, sacher2014a,
    primiani2019), campus (khope2019, lee2025, pathak2014a, ropp2021, roy2026, spektor2023, stanton2020), unused block
    (spektor2023 block 5), contact markers (su2026), locators (kharas2020, pathak2014a `p.2 header`; lihachev2022,
    luo2014 and prose `p.1 footnote`);
  - (d) the remaining papers: kazama2021, khope2019, kumar2026, liang2017, limongi2026, mason2025, moralesalvarado2026,
    peng2021, romerogarcia2013, sacher2014, song2025, stern2018.
- Per slot: slot-to-name assignment (D359, D369, D287, D302), printed marker run vs `markers` + `dropped_markers`, block
  mapping, org / unit / more_orgs split, parent rule, campus (D301), locality (first printed city as printed), country
  (printed), role, basis, locator. Every note claim checked against the page.
- Name scan: all 261 `compare.csv` rows, list name vs printed name (folded); 59 rows differ, every one inspected.
- Org mapping: every distinct (printed org, org ids, match basis) of `header_rows.csv` read; all correct.
- Missed present addresses: all pages of the 35 `text.md` files scanned for cue patterns (paper, page and cue only
  printed): lihachev2022, primiani2019, rombouts2025, oser2019 as above; luo2014 p.5 is body text and marin2023 p.7 is an
  author biography at the same org: no further block. Every symbol mark on an author line resolved to its footnote.
- Claims tested with dry-run probes (`check --dry-run` on a temporarily edited `headers.yaml`, file restored
  byte-identical, md5 asserted after each probe; helper `probe.py`, same folder).
- Consistency: the same org in earlier lit batches read for Tyndall National Institute (lit_h05, lit_h08, lit_h11,
  lit_h13, lit_h16), Lincoln Laboratory (lit_h02, lit_h09, lit_h14), CEA-LETI with Université Grenoble Alpes.
- Privacy scan (`privscan.py`, same folder): see below.
- Backup before any edit: `backup_lit_h20_20261102T223429.zip` (lit_h20 directory + `org_requests.csv`), same folder.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h20 | 35 / 35 | 261 | 246 | 15 | 0 |

- Fixed: 2 imprecise (oser2019 #4, F1; palmer2026 #3, F2). Not fixable within the contract / checker: 13 imprecise
  (lindenmann2014 #1-#6 #8 #9, palmer2026 #1 #6 #8 #9, stanton2020 #4; C1, C2).
- The 1 `no_header` slot: lee2024 #10 (Michelle Zhang): printed without any marker in both layers next to two marked
  blocks, no unmarked block exists; `unreadable` is correct under the never-guess rule (probe marker 1: "printed markers
  differ"; precedent kang2008 #10 #11).
- Header-only authors (`slot: 0`): none.

## Rulings on slot overrides and known items

| paper, slot | printed vs list | ruling |
|---|---|---|
| palmer2026 #2 | Henk Bulthuis vs H.F. Bulthuis | keep `slot: 2` (D369 distinctive family name, missing middle initial; probe without slot: 0 matches) |
| qiu2026 #9 | Grigorii Likhachev vs Grigory Lihachev | keep `slot: 9` (D287 transliteration variant; probe without slot: 0 matches) |
| spektor2023 #4 | J.L. Skarda vs Jinhie Skarda | keep `slot: 4` (D369, distinctive family name, first initial agrees; probes without slot and `slot: 0` both error) |
| qiu2026 | printed order differs from the list (Hu, Yang, Xurong Li) | warning correct; all 12 slots resolve by name (D363) |
| song2025 #1 | Hao Song vs list Hao Ran Song | auto-match with a dropped syllable, common family name; first author, same position: accepted and listed for review as fang2010 / feng2011 (D426; open question 3) |
| spektor2023 #10 | J. Vučković vs list artefact "Jelena Vuckovic A" | correct person; D412 form (open question 2) |
| primiani2019 #10 | Frédéric van Dijk vs list Frederic V. Dijk | correct person; list abbreviates the particle (open question 2) |
| su2026 #5 | Xiangyue Li vs list xiangyue Li | correct person; list case artefact (open question 2) |
| other list-side differences | e.g. Temitope Paul Onanuga / Temitope Onanuga, Maria Laura Goedecke / Gödecke, Julian L. Pita Ruiz / Julián L. Pita, Leonardo Vieira do Prado Cunha / L. Cunha, AbuBakar / Abu Bakar Bhatti, John E. / John Edward Bowers, Amit Kumar / A. Agrawal, Georgios / G. Charalampous | all initials agree, same positions: correct |

## Findings and fixes

| # | paper, slots | rating | evidence (locator) | fix (field: before -> after) |
|---|---|---|---|---|
| F1 | oser2019 #4 (Diego Pérez-Galacho), present address | imprecise, extractor claim false | p.1 header: triangle mark on the name; p.8: a statement with a recognized cue names him at iTEAM, Universitat Politecnica de Valencia, ES. The note said the form is not recordable; probe block with marker triangle, `present_address`, `p.8 affiliations`: 0 errors in md and pdf | new block `{marker: "△", role: present_address, org: "Universitat Politecnica de Valencia", unit: "Photonics Reseach Labs, iTEAM Research Institute", locality: "", country: "ES", locator: "p.8 affiliations"}` (unit spelled as printed; no city outside the university name); author markers `["1"]` -> `["1", "△"]`; note rewritten. +1 row, mapped `org_upv` |
| F2 | palmer2026 #3 (Cleitus Antony), P4 | imprecise | p.1 footnote: Tyndall National Institute, then School of Physics, then University College Cork, Cork, IE. Five earlier batches treat University College Cork after the institute as a parent, not copied (lit_h05, lit_h08, lit_h11, lit_h13, lit_h16 notes). The note also called the postal and unit-number text of statements 4 / 5 "street text" | `more_orgs: ["University College Cork"]` -> removed; note rewritten (parent and school named as not copied; "address text"). -1 row; `compare.csv` org ids of slot 3 `org_tyndall_national_institute;org_university_college_cork` -> `org_tyndall_national_institute` (open question 1) |
| C1 | lindenmann2014 #1-#6 #8 #9 (P1), palmer2026 #1 #6 #8 #9 (P1) | imprecise, not fixable | p.1 footnote: both statements print the country hyphenated across a line break (DE); probes country DE: "country is not printed in this block" (md, pdf) | none (known gap: ozdemir2021); `country: ""`, noted; open question 4 |
| C2 | stanton2020 #4 (Galan Moody), present address | imprecise, not fixable | p.1 header: dagger on the name; footnote with the cue Current affiliation (University of California, Santa Barbara, ECE, US); probe dagger block `present_address`: "marker + first field not printed" (md, pdf): the cue is not in `CUES` | none (family of the known "Current address:" gap: kuyken2011, ji2017, koyaz2026, beeck2021); noted; open question 4 |

Checked and correct (highlights):
- Prose: lim2021 P1-P5 (clause P4 for Peng Zhao; subjects vs carriers both ways); lindenmann2014 P1 / P2; marin2023 and
  saghaei2026 ("The authors" = all); palmer2026 P1-P5 (subjects vs carriers both ways); primiani2019 P1 "was with" + P2
  pronoun present address (Cordon Italy), P3 and P4; rombouts2025 P1, P2 "was with" + P3 pronoun present address
  (Keysight Technologies, Ghent), P4 + clause P5.
- Parents not copied: A*STAR in lim2021, sacher2014a; III-V Lab parents in primiani2019 (D426); University College Cork
  in palmer2026 after F2.
- Two orgs kept: primiani2019 P4 CEA-LETI + Université Grenoble Alpes (same form as earlier batches); rombouts2025 P1 /
  P5 Eindhoven University of Technology + Eindhoven Hendrik Casimir Institute (printed joined by "and"); oser2019 blocks
  1 / 2 with CNRS and the universities (UMR rule).
- Campus: khope2019, stanton2020 Santa Barbara; lee2025, pathak2014a Davis (pathak2014a prints no comma); roy2026
  Berkeley; ropp2021 College Park; spektor2023 Boulder (D416 nader2025 form). Mapped to the campus orgs.
- Empty fields: liang2017 blocks 1 / 2, roy2026 print no country. Hong Kong printed as the place: khope2019 block 3 `HK`.
- Locators: kharas2020, pathak2014a `p.2 header` (page 1 is a cover); lihachev2022, luo2014 `p.1 footnote`.
- Markers: every readable author's printed run matches `markers` + `dropped_markers`. Equal contribution lihachev2022 4;
  contact su2026 3, 4 (three masked contact lines for marks 3, 4 and asterisk; their content is masked, so that reading
  rests on the count and position); symbol marks never used by a block except F1.
- Unused block: spektor2023 block 5 (Vector Atomic): no author carries 5 in either layer; not recorded, as the contract
  says. Block numbering kept (block 6 stays 6).
- As printed: luo2014 Keren Bergmen; moralesalvarado2026 Institute for Advanced Studies, IEAv; palmer2026 Huawei
  Heisenberg Research Center (Munich); kumar2026 unit Quantum Information Science and Technology; oser2019 Reseach.
- Consistency: kharas2020 MIT + unit Lincoln Laboratory as in lit_h02, lit_h09, lit_h14 (same org id).

## Privacy and as-printed scan

- See the result line under Commands. Notes name address parts only by type (campus name, street text, address text);
  peng2021's campus name and every street, building, postal and unit-number string printed in this batch are stored
  nowhere. No `skip_prefix` / `skip_between` span in the batch.

## Commands (2026-11-02, log times)

| Command | Result |
|---|---|
| `check lit_h20 --corpus lit --dry-run` (before) 22:34:30 (log `lit_headers_check_lit_h20_66229_20261102T223430.log`) | 0 errors, 4 warnings (palmer2026 slot 2, qiu2026 slot 9 and order, spektor2023 slot 4); slots 261, recorded 260, no_header 1, rows 344, present addresses 3, 25 unmapped org strings |
| probes (`--dry-run`) 22:38:44 (67772), 22:38:51 (67850), 22:38:58 (67925), 22:39:05 (68020), 22:39:11 (68069), 22:39:19 (68133), 22:39:26 (68205), 22:39:33 (68254), 22:39:40 (68315), 22:39:47 (68381) | lindenmann2014 country DE: 2 errors; palmer2026 country DE: 2 errors; stanton2020 dagger block: 2 errors; oser2019 triangle block: 0 errors; spektor2023 no slot: 2 errors; spektor2023 `slot: 0`: 1 error; palmer2026 no slot: 2 errors; qiu2026 no slot: 2 errors; palmer2026 P4 as University College Cork + unit: 0 errors (not adopted, F2); lee2024 Zhang marker 1: 3 errors. File restored and md5-verified after each |
| `check lit_h20 --corpus lit` 22:41:23 (log `lit_headers_check_lit_h20_68810_20261102T224123.log`) | 0 errors, 4 warnings; ok 34, partial 1, unreadable 0; rows 344 (grade A 344), recorded 260, no_header 1, present addresses 4; 25 unmapped org strings; stamp matches headers.yaml (sha256 2dcc5909...) |
| privacy scan, 2026-11-02 | `privscan.py` over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`, `papers.csv`, `check_stamp.txt` and this record: contact / URL / ORCID patterns, source-stamp wording, the street, building, postal and unit-number strings printed in this batch: 0 hits; 3+ digit runs only in the two YAML comment lines (DevLog number, extraction date) |

Changes to `headers.yaml` (diff against the backup): oser2019 note, new block, author markers; palmer2026 note, P4
`more_orgs`; nothing else. `header_rows.csv` gains the oser2019 present-address row and loses the palmer2026 University
College Cork row; `compare.csv` changes only for oser2019 #4 and palmer2026 #3; `unmapped_orgs.csv`, `papers.csv` and
`org_requests.csv` unchanged. `aggregate` not run (coordinator).

Process note: one read-only `git status` on the staging paths was run while confirming that nothing outside the batch
had changed, against the no-git instruction of this audit. It changed nothing; the audit's conclusions do not rest on it.

## Checker gaps observed (scripts not edited)

- Hyphenated country across a line break (known: ozdemir2021): lindenmann2014, palmer2026, 12 slots with `country: ""`.
- "Current affiliation:" cue (family of "Current address:"): stanton2020 #4.
- Observation: a non-asterisk symbol mark carries a present-address block without any checker change (oser2019 triangle;
  stanton2020's dagger fails only on the cue, not on the mark). D426 G4 lists present-address-only markers; the case read
  for this audit (chen2000, 2026-10-30 record) is an asterisk; yang2010 and keyvaninia2019 were not read.

## Open questions

1. palmer2026 P4: University College Cork dropped as a parent of Tyndall National Institute although a School of Physics
   is printed between them (F2): confirm? Recommended: yes, consistent with five batches; the alternative (University
   College Cork + unit, probe 0 errors) would be a one-off form.
2. D412 author-list correction file: add spektor2023 #10 "Jelena Vuckovic A", primiani2019 #10 "Frederic V. Dijk", su2026
   #5 "xiangyue Li"? Recommended: yes.
3. song2025 #1 (Hao Song / Hao Ran Song) dropped-syllable auto-match: accept and add to the D426 review list?
   Recommended: yes.
4. Re-record after checker fixes: lindenmann2014 P1 and palmer2026 P1 country DE (hyphenated country), stanton2020 #4
   ("Current affiliation:" cue). Recommended: add to the D426 list.
5. Earlier dropped symbol-mark present addresses: F1 shows a triangle mark verifies today. Sweep committed lit batches for
   non-asterisk symbol marks noted as "not recordable" in the follow-up pass? Recommended: yes; not done here (scope).
