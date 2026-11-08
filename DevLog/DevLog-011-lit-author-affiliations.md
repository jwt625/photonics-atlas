---
title: Literature cache (`lit`) per-author affiliations from the printed paper, for the people atlas
date: 2026-10-23
status: all 116 lit papers extracted (pilot + lit_h01..lit_h04, check all 0 errors); batch fixes D366-D369 applied 2026-10-23: 115 ok, 0 partial, 1 unreadable (no affiliation printed); merge proposal below, not executed
scope: owner request 2026-10-23 (the people atlas has no authors from the literature cache); every cached `lit` paper
authors: Claude (at Wentao Jiang's request)
---

# DevLog-011: `lit` author affiliations

Decisions here are D350-D369. Builds on [DevLog-008](DevLog-008-ofc-header-extraction.md) (OFC header extraction:
YAML format, checker D246-D248, D282-D288, D300-D305) and [DevLog-004](DevLog-004-p3-people.md) (people build; OFC
merge D214-D219e). This stream edits `scripts/ofc_headers.py` (generalized), its tests, and
`data/_staging/people/lit_headers/`; it does not edit people code / data, the registry, `app/` or
`scripts/build_views.py`.

## Inputs (read-only)

| Input | Content |
|---|---|
| `data/registry/sources.csv`, corpus `lit` | 116 sources on 2026-10-23 (`restricted_local_only` 91, `open_license_ok` 25); more each retrieval day |
| `references/<paper_id>/text.md` | pymupdf text with `<!-- page N -->` markers; title, author line, affiliation blocks or footnotes on page 1 (some on later pages) |
| `references/<paper_id>/source.pdf` | local PDF for all 116 (superscript markers recoverable with pymupdf span flags) |
| `references/<paper_id>/source.json` | `garbled_text_layer` (2 papers), pages |
| `data/_staging/literature/cache_list.csv` + `cache/literature/merged.jsonl`, `cache/literature/curator_adds.jsonl` | `paper_id` -> `uid` -> ordered `authors` (merged.jsonl 115 of 116; virot2014 from curator_adds.jsonl, D362); `institutions` is paper-level only, so there is no per-author metadata org |

Survey (2026-10-23): page 1 carries the abstract in 81 papers; 21 papers state affiliations in prose footnotes
("K. A and L. B are with X", IEEE / JLT style; one accepted manuscript writes "was with" and its text extraction puts
the footnote statements before the title and author line, with one statement continued in the other column;
corrected 2026-10-23 after the pilot audit: the earlier "no author line on page 1" was wrong); author lines carry
IEEE / OSA membership designations ("Member, IEEE", also without comma, "Fellow OSA").

## Decisions (D350-D369)

| # | Decision | Rationale |
|---|---|---|
| D350 | One tool: `scripts/ofc_headers.py` gains a corpus spec (`--corpus ofc2026` default, `--corpus lit`). Same YAML format, contract, checks (D244, D246-D248, D249, D282-D288, D300-D303), `show`, `queue`, `check`, `aggregate`. OFC behaviour and `tests/test_ofc_headers.py` unchanged (regression) | owner: reuse, one set of never-invent rules |
| D351 | Staging: `data/_staging/people/lit_headers/<batch>/` (`papers.csv`, `headers.yaml`, derived `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`, `check_stamp.txt`); pilot `pilot/`, batches `lit_hNN` of ~25 papers; `org_requests.csv` in `lit_headers/`; local lists `data/_local/lit_headers_*.csv` | parallel to DevLog-008 D179 / D248 |
| D352 | Slots: one slot per author position of the ordered `authors` list (merged.jsonl via cache_list uid; D62); slot names = those names. A paper without an author list (virot2014) takes its slots from the header order: the YAML sets `slots_from_header: true`, every row carries it in `compare.csv`, and the merge treats such slots as flagged (proposal below) | owner: handle the missing one from the header alone, flagged |
| D353 | Search text: page 1 of `text.md` plus every page named in a block locator, in page order; PDF view: the same pages of `source.pdf` with superscripts marked. No cut at the abstract (footnote affiliations follow it). Locators `p.N header` / `p.N footnote` / `p.N affiliations` (exact page of `text.md`) | lit text has page markers; affiliations can be first-page footnotes or an end-of-paper list |
| D354 | Prose affiliations (`basis: prose`, grade A): a footnote statement "<names> is / are (also / now) with <block>" is a block with a synthetic marker (`P1`, `P2`, ...; never printed). Checks: the block starts at the verb phrase + its first field; fields inside the statement (up to the next statement, 300 normalized characters); every author carrying the marker is name-compatible with a name printed in that statement's subject ("The authors" = all authors, who must then all carry it); "is now with" = `present_address` (cue); "was with" = the affiliation of the work (role affiliation); prose markers are not part of the printed marker run (D286d) and an author whose blocks are all prose may be absent from the author line | 21 of 116 papers |
| D355 | Membership designations in author lines ("Member, IEEE", "Senior Member, IEEE", "Fellow, OSA", ...) are removed before name / marker matching (both corpora; no OFC header has them) | IEEE author lines |
| D356 | Comparison: no per-author metadata org, so `compare.csv` outcome is `recorded` (header rows exist) or `no_header`; header org mapping and `org_requests.csv` as in DevLog-008 (org matching with corpus `lit` scoped aliases, then the global rules) | `institutions` is paper-level |
| D357 | Rights: facts only (names and org / unit / city / country) for all `lit` papers, `restricted_local_only` and `open_license_ok` alike; no quotes; `show` prints to the terminal only | owner |
| D358 | Grades: printed / single / pdf / prose = A; listing_order / layout = B (D240, D246) | owner |

### Pilot audit fixes (2026-10-23, [audit](audits/2026-10-23-lit-header-pilot-audit.md), coordinator: D359-D365)

| # | Decision | Implementation |
|---|---|---|
| D359 | (coordinator, owner-level ruling) D62 extended: `lit` author slots = one slot per position of the paper's author list (`lit:<paper_id>#a<i>`), slot number = author-list position; printed header names go to `person_aliases` only (D218), never slot names | merge path items 1, 3, 3a |
| D360 | (F1) A prose statement continued in another column or block: block field `continued` = first printed word(s) of the continuation; the checker takes the first part up to the end of the verb's printed line, finds the continuation at a line start later on the searched pages, and checks the fields in the joined text (a field may straddle the split: "Intel" + "Corporation") | `_prose_checks`, `_at_line_start`; jayatilleka2021 P3 re-recorded as Intel Corporation, Santa Clara, US (`continued: "Corporation"`); note corrected; tests `continuation dropped`, `continuation not printed` |
| D361 | (F2) Coverage: in a `lit` paper every statement "<subject> is / are / was / were (also / now / currently / presently) with" on the searched pages whose subject names a slot author ("the authors", or a pronoun after such a statement) must be a recorded prose block, else an error | `_prose_checks(coverage=True)` for corpus lit; tests for the audit mutations M12 (omitted "He is now with") and M13 (omitted "They are now with"); OFC unaffected (coverage off) |
| D362 | (F3) Author list fallback: `cache/literature/curator_adds.jsonl` (same `authors` field) for a cache-list paper missing from `merged.jsonl`; D352 (`slots_from_header`) remains only for a paper with no list in either file. Name folding for slot matching also maps the oe ligature ("F. Boeuf" printed with it in the curator list) | `lit_papers`, `FOLD_FIX`; virot2014 now 8 author-list slots, `slots_from_header` dropped; tests updated (`test_lit_author_lists`, `test_slots_from_header_without_any_list`) |
| D363 | (F4) Printed author order different from the author list: warning and `compare.csv` column `order_differs` (lit only; OFC compare files unchanged); slots stay author-list positions, `header_pos` keeps the printed order | pilot: kim2019 |
| D364 | (F5) `MEMBERSHIP_RE` accepts the comma-less forms ("Fellow OSA", "Member IEEE") | test `test_membership_designations_are_removed` |
| D365 | (F6) Merge proposal amended: D218 analogue (header printed forms to `printed_name` and `person_aliases`, origin lit, never `Slot.names`), build-time duplicate-paper check (DOI and normalized title across all corpora), D359 slot rule, preprint attribution | merge path items 3a, 6, 8 |


### Batch fixes (2026-10-23, coordinator: D366-D369)

| # | Decision | Implementation |
|---|---|---|
| D366 | Prose / text rules from the 4 batches: (1) a statement subject starts after a real sentence boundary only (")", ";", a blank line, a number / upper-case or lower-case word / country name / closing quote before ". ", or the previous statement's verb); a period after a capitalized name ("F. Ferraro. Y. Ban") is not one, and subject names are also split there; (2) "<names> is with A, and (also) with B[, and with C]" (also ", also with", "and are also with"): each further clause is its own block (`clause: true`) of the same statement (same subject, own unit / place), and an unrecorded clause of an author-naming statement is a coverage error; (3) `skip_prefix`: a verified printed span (building / complex) between the verb and the first field, never recorded; (4) a letter marker glued to its cue ("aPresent address") is split for the cue check; (6) the author line is searched from the first page a locator names as header (cover pages skipped); (8) unreadable authors may carry prose markers; (9) locality = the city as printed (postal designations dropped); (10) `show` prints text.md page separators. Contact stripping in the checker now ends an address at a non-address character (`[\w.+-]*@[\w.-]*` first, then the shared pattern), so an address no longer swallows the next line's given name or a closing parenthesis; within prose the first field may be glued to its verb / clause anchor ("andalsowiththeKeyLab") | `PROSE_CUT_RE`, `_subject`, `CLAUSE_RE`, `_prose_checks`, `lit_search_pages`, `_words`, `_prep`; tests `test_d366` (cut, clauses, skip_prefix, glued cue, cover page) |
| D367 | `more_orgs` entries may be structured (`{org, unit, locality, country}`) so a unit or place printed after a second org is recordable; plain strings keep the block's place | `MoreOrg`, `AffIn.mo`, row building; elsaeed2024 P1 / P3 |
| D368 | New bases `per_author` (block(s) printed under each author, IEEE conference style) and `grouped` (an author group printed above its own block(s)), synthetic markers `G<n>`, grade A, verified by position: the block's first field follows the previous grouped block, every carrier is printed between the previous block and this one, no other author after the group's first name (a group's further block may follow directly); a single unmarked block next to marked blocks stays `layout` (grade B) | `_grouped_checks`; liang2025 (per_author), shamsansari2022 and mu2026 (grouped); tests in `test_d366` |
| D369 | Lit slot matching: when one name form is abbreviated, every initial must be explained by the other form (its given-name syllables, or the letters of a joined given name in order: "S. H." ~ "Shaohua", "D. L." ~ "DimLee"; "S. F." !~ "Siyuan", "M. B." !~ "Ming"). Unexplained (common family name) -> `slot: 0` + `author_list_differs`: liang2025 Siyuan Yu (S. F. Yu), song2008 M. B. Yu (Ming Yu), wang2026 Hao Deng (H T Deng) and Junpeng Lu (J. Y. Lu). A distinctive family name differing only by a missing middle initial takes an explicit name-part `slot:` (D287): garciablanco2025 S. M. Garcia-Blanco -> slot 1. OFC matching unchanged | `strict_compatible`, `match_slots(strict=lit)`; `test_strict_initials` |

## Merge path (proposal for the people-stream owner; NOT executed)

As the OFC merge (DevLog-004 D214-D219e), with these differences:

1. Slots (D359 extends D62): `lit:<paper_id>#a<i>`, i = position in the ordered author list (D352, D362), never
   the printed position (`header_pos`, which differs in some papers, D363); a new slot source in `people.py` (`_lit_slots`),
   kind `publication`, grade from the header row (A, or B for listing_order / layout), `active_on` = the source's
   `published_on`, else its year. There is no metadata observation to keep or drop: header rows are the only
   observations of a `lit` slot.
2. Observation ids: `lit:<paper_id>#a<i>.h<aff_order>.<org_k>.m<n>` (D219e form), stable under org-mapping changes.
3. Identity (D217): slot names come from the author list, never from the header printed names; header orgs are not
   identity keys; the D63 rules and the D219d join rule (new common-family rule-3 joins need a resolved or non-common
   shared coauthor) apply unchanged, so `lit` slots join existing persons only through the existing rules.
3a. Printed names (D218 analogue): the header printed form of each slot goes to the observation's `printed_name` and
   to `person_aliases` (`printed_variant`, origin lit, notes "lit header form, not used for identity"), never to
   `Slot.names`, coauthor keys or display names.
4. `slots_from_header` papers (none on 2026-10-23 after D362): slots built from the header order; observations
   `visibility = review` until an author list is available, or excluded (owner choice).
5. Header-only authors (`slot: 0`) are not merged (D243 analogue); local list `data/_local/lit_headers_extra_authors.csv`.
6. Duplicates: a `lit` source with `same_as` is skipped (none on 2026-10-23), and the build checks DOI and
   normalized title against every other corpus (eo, pk, ofc2026, lin, blog, web) before adding `lit` slots: a
   duplicate paper would give an author two slots whose coauthors are the same paper and inflate D63 rule-3 evidence.
   The pilot audit found 0 DOI and 0 title overlaps on 2026-10-23.
7. Validator: corpus `lit` kind publication, header id pattern, grade A / B as above; schema text p4.
8. Preprint text: when the cached text is a preprint (arXiv) of the registered source, its printed affiliations are
   attributed to the registered `lit:` source and its `published_on` (the printed order may differ, D363).

## TODO

- [x] 1. Read inputs, people rules D217 / D219d / D219e; survey; plan (this file).
- [x] 2. Generalize `scripts/ofc_headers.py` (corpus spec, lit loaders, prose basis, membership strip, page-aware search text, lit `show` / `queue` / `aggregate`); OFC regression (tests unchanged, `check all` OFC byte-identical derived files).
- [x] 3. Contract `data/_staging/people/lit_headers/CONTRACT.md` (lit addendum to the OFC contract).
- [x] 4. Pilot 10 papers; check to 0 errors; results.
- [x] 5. Queue the rest: 4 batches `lit_h01`..`lit_h04` (27, 27, 27, 25 papers).
- [x] 6. Tests for the lit additions (`tests/test_lit_headers.py`); ruff, mypy, pytest, validate_db.
- [ ] 7. Fresh-context audit (coordinator), batches (coordinator), merge (people owner).

## Progress

- 2026-10-23: stream assigned; inputs read; survey; plan written.
- 2026-10-23 10:12-10:22 (log times): `scripts/ofc_headers.py` generalized (D350): `Spec` (corpus, staging dir,
  locator pattern), `--corpus` on every subcommand, lit loaders (`lit_papers` from cache_list uid -> merged.jsonl
  `authors`; `lit_text` / `lit_pdf_text` page-aware), `basis: prose` (D354), `slots_from_header` (D352), membership
  strip (D355), `recorded` outcome (D356), map_org with the corpus alias scope. OFC regression before any lit work:
  hash snapshot of the 65 OFC derived files, then OFC `check all` + `aggregate` with the new code: 65 / 65
  byte-identical; `tests/test_ofc_headers.py` unchanged, 72 passed.
- Pilot (10 papers chosen for diversity: Optica / arXiv superscripts, two IEEE / JLT prose footnotes, an accepted
  manuscript with no author line, an 18-author Nature paper with a campus block, the paper without an author list,
  a paper flagged with a garbled text layer, capitals author lines with contact-footnote markers, a VLSI paper):
  (correction 2026-10-23: the accepted manuscript does print a title and author line on page 1; its text extraction
  puts them after the footnote statements)
  first dry run 8 / 10 clean; 38 errors in kim2019 and jayatilleka2021, all tool defects: (a) a prose block searched
  from the previous statement's verb found that statement's own first field (now the next search starts after the
  located field), (b) detached accents in statement subjects were not folded, (c) prose-only authors found inside the
  statements were put through the author-line marker check. After the fixes 0 errors, 0 warnings. Rows written,
  `aggregate --corpus lit`: 6 org requests, 0 conflicts, 0 header-only authors.
- Queue (`queue --corpus lit --size 27`): 106 papers in `lit_h01` (27 papers, 231 authors), `lit_h02` (27, 220),
  `lit_h03` (27, 207), `lit_h04` (25, 227); nothing skipped.

## Pilot results (2026-10-23)

| paper | slots | slots with rows | rows | basis | multi-aff slots | present address | unmapped rows |
|---|---|---|---|---|---|---|---|
| billah2018 | 13 | 13 | 21 | printed | 6 | 0 | 2 |
| shikama2017 | 4 | 4 | 4 | prose | 0 | 0 | 0 |
| jayatilleka2021 | 8 | 8 | 8 | prose | 0 | 0 | 0 |
| kim2019 | 13 | 13 | 16 | prose | 0 | 3 | 6 |
| tran2022 | 18 | 18 | 18 | printed | 0 | 0 | 0 |
| virot2014 | 8 | 8 | 20 | printed | 1 | 0 | 10 |
| jeong2013 | 10 | 10 | 11 | printed | 1 | 0 | 0 |
| ashida2017 | 10 | 10 | 11 | printed | 1 | 0 | 2 |
| gao2021 | 9 | 9 | 19 | printed | 6 | 0 | 0 |
| wang2022a | 7 | 7 | 7 | printed | 0 | 0 | 0 |
| total | 100 | 100 | 135 | | 15 | 3 | 20 |

- 10 / 10 papers `ok`; 100 / 100 slots with rows; 135 rows, all grade A (printed 107, prose 28; no listing_order or
  layout needed: every lost marker was readable in the local PDF or printed in the text).
- Slots: all 92 author-list slots matched by name without a `slot:` override, including kim2019 whose header order
  differs from the author list; virot2014 (8 slots) first from the header (`slots_from_header`), since D362 from
  the curator author list.
- Prose: 3 papers, 12 statements (kim2019 7 incl. 2 pronoun statements "They / He ... now with" = present
  addresses; shikama2017 2; jayatilleka2021 3; the third was first recorded as cut after "Intel", which was wrong: it continues
  in the other column of page 1 and is recorded since D360 as Intel Corporation, Santa Clara, US).
- Campus rule: "University of California, Berkeley" (kim2019) and "..., Santa Barbara" (tran2022) map to the campus
  orgs (`org_university_of_california_berkeley`, `org_ucsb`), not to a parent.
- `dropped_markers`: equal contribution (tran2022 x3), contact footnotes (ashida2017, gao2021 x2).
- Unmapped org strings (6, `org_requests.csv`): Colleges of Nanoscale Science and Engineering, Institut
  d'Electronique Fondamentale (IEF), Osaka Prefecture University, Rafael Advanced Defense Systems, Universite
  Paris-Sud, Vanguard Photonics GmbH. Every mapped string was checked by reading (e.g. KIT, HHI, AIST, PETRA, SIOM,
  CEA, CNRS, Intel).

## Batch list

| batch | papers | authors | first..last paper_id |
|---|---|---|---|
| lit_h01 | 27 | 231 | akin2024..huang2026 |
| lit_h02 | 27 | 220 | iwama2015..ni2025a |
| lit_h03 | 27 | 207 | nie2024..sun2011 |
| lit_h04 | 25 | 227 | suntsov2021..zhang2024a |

New `lit` sources from later retrieval days: `queue --corpus lit --size 27` adds them as `lit_h05`... (existing
batches are never rewritten).

## Verification (2026-10-23 10:22 log time)

- `uv run python scripts/ofc_headers.py check pilot --corpus lit`: 0 errors, 0 warnings; `check all --corpus lit
  --dry-run`: 0 errors, 4 warnings (batches not extracted); `aggregate --corpus lit`: exit 0.
- OFC regression: `check all` (OFC) 0 errors, 48 warnings (unchanged); 65 / 65 OFC derived files byte-identical to
  the snapshot taken before the refactor.
- `uv run pytest -q`: 325 passed (`tests/test_ofc_headers.py` unchanged 72, `tests/test_lit_headers.py` 14).
- `uv run ruff check`, `ruff format`, `mypy` on `scripts/ofc_headers.py` and both test files: clean.
- `uv run python scripts/validate_db.py --quiet`: 0 errors, 15 warnings (pre-existing).

- 2026-10-23 (after the pilot audit): D359-D365 implemented (`continued`, coverage check, curator_adds fallback,
  oe-ligature fold, `order_differs`, comma-less membership, merge proposal). Pilot re-checked: 0 errors, 1 warning
  (kim2019 order); 135 rows, 100 / 100 slots recorded (jayatilleka2021 P3 now Intel Corporation, Santa Clara, US), all grade A;
  `aggregate --corpus lit`: 6 org requests. OFC regression: `check all` 0 errors / 48 warnings, 65 / 65 derived files
  byte-identical. `check all --corpus lit --dry-run`: 0 errors, 5 warnings (4 batches not extracted, kim2019 order).

## Verification (2026-10-23 10:43 log time, after D359-D365)

- `check pilot --corpus lit`: 0 errors, 1 warning (kim2019 order, D363); `aggregate --corpus lit`: exit 0 (6 org
  requests); `check all --corpus lit --dry-run`: 0 errors, 5 warnings.
- OFC regression: `check all` 0 errors / 48 warnings; 65 / 65 OFC derived files byte-identical to the pre-refactor
  snapshot; `tests/test_ofc_headers.py` unchanged in git, passing.
- `uv run pytest -q`: 330 passed (`tests/test_lit_headers.py` 19). ruff check / format and mypy on
  `scripts/ofc_headers.py` and both test files: clean. `validate_db.py --quiet`: 0 errors, 15 warnings.

- 2026-10-23 (batch fixes, coordinator D366-D369): checker extended (see D366-D369); 11 papers re-extracted by this
  stream (elsaeed2024, qi2024, sheng2012, shamsansari2022, mu2026, jahed2022, liang2025, koninck2025, maeda2023 with
  its printed localities Atsugi-shi / Yokohama-shi, mangal2020, wang2026), song2008 and garciablanco2025 slots per
  D369; ma2026 stays unreadable (no affiliation printed). Two regressions seen and fixed before writing: (a) the new
  contact strip ate the closing parenthesis of "(email: ...)" (a statement boundary), (b) it ate "USA" glued to an
  address by a backslash in one OFC header (OFC W3D.2): the strip now keeps to address characters. OFC `check all` 0
  errors / 48 warnings, 65 / 65 derived files byte-identical.

## Totals (D366-D369 applied; pilot + lit_h01..lit_h04, `check all --corpus lit` 0 errors)

| Item | Count |
|---|---|
| papers | 116: ok 115, partial 0, unreadable 1 (ma2026: no affiliation printed in text or PDF) |
| slots (author-list positions) | 985: recorded 973, without rows 12 |
| rows | 1312, all grade A (printed 1001, prose 201, single 76, grouped 29, per_author 5); present addresses 10 |
| multi-affiliation slots | 175 |
| papers with printed order differing from the list (D363) | 5 |
| header-only authors (`slot: 0`, local list) | 5 (liang2025 Siyuan Yu, meng2023 Gelu Comanescu, song2008 M. B. Yu, wang2026 Hao Deng and Junpeng Lu) |
| org requests (`aggregate --corpus lit`) | 75 strings |

Slots without rows (12): ma2026 x3 (unreadable paper), list authors not printed in the header (garciablanco2025
#7, koninck2025 #7, liu2022 #4, wilson2019 #5 #6), and the D369 non-matches (liang2025 #6, song2008 #5, wang2026 #6
#9).

## Verification (2026-10-23 11:11 log time, after D366-D369)

- `check all --corpus lit`: 0 errors, 8 warnings (5 printed-order notices, 3 explicit `slot:` overrides);
  `aggregate --corpus lit`: exit 0 (75 org requests, 5 local header-only authors).
- OFC regression: `check all` 0 errors / 48 warnings; 65 / 65 OFC derived files byte-identical to the snapshot taken
  before this round; `tests/test_ofc_headers.py` unchanged in git, passing.
- `uv run pytest -q`: 350 passed (`tests/test_lit_headers.py` 39). ruff check / format and mypy on
  `scripts/ofc_headers.py` and both test files: clean. `validate_db.py --quiet`: 0 errors, 15 warnings.

## Handoff (2026-10-23 16:00 PDT, owner: wrap up)

- D380 (coordinator, done): new verified field `skip_between` (building / site name printed between unit and org; checked
  inside the block window, never stored); sulway2023 block 1 fixed (building name no longer in derived rows); tests
  `skip_between (clean | missing | not printed)`. The scan of other lit / OFC blocks for building names is NOT done.
- Open (not started; two agent attempts ended on an API content-filter error): D381 nakamura2020 #4 Tamagawa as a
  structured more_orgs entry; D382 strict_compatible initials must match a syllable start (exact pinyin or
  capitalized-part segmentation; tests "M. G. Li" !~ "Ming Li", "S. A. Yu" !~ "Siyuan Yu", "J. N. Smith" !~ "Johann
  Smith", "S. H." ~ "Shaohua"); D383 DevLog slot-id wording (`lit:<paper_id>#<i>`).
- State: 116 papers, 115 ok, 973 / 985 slots, 1312 rows (grade A); fresh batch audit GO (0 wrong in 342 slots).
- Next: D381-D383, then the people merge build (DevLog-004 D370-D379; switch `LIT_MERGE` in
  src/photonics_atlas/people.py), build_views, push.

## TODO (postponed by the owner 2026-10-23: lit authors made visible first)

- [ ] D381 nakamura2020 #4: Tamagawa as a structured more_orgs entry with its own place (AIST place only as printed).
- [ ] D382 strict_compatible: an extra initial must match a syllable start (exact pinyin or capitalized-part
      segmentation); tests "M. G. Li" !~ "Ming Li", "S. A. Yu" !~ "Siyuan Yu", "J. N. Smith" !~ "Johann Smith",
      "S. H." ~ "Shaohua"; re-check lit slots and rebuild people if any slot changes. (No current slot is affected,
      per the batch audit.)
- [ ] D383 wording: lit slot id `lit:<paper_id>#<i>` everywhere in this DevLog.
- [ ] D380 follow-up: scan all lit / OFC blocks for building / site names in unit / org fields (sulway2023 fixed).
- [ ] Org round for the 75 lit org requests (data/_staging/people/lit_headers/org_requests.csv), then
      `check all --corpus lit` + aggregate + people rebuild.
- [x] Lit authors in the people atlas (DevLog-004 2026-10-23 16:20): built and served.

## Session 2026-10-29 (Wentao: "check cached papers that have not been ingested, and start parsing and ingesting them")

| # | Decision | Rationale |
|---|---|---|
| D406 | (lit_h11 zhang2023d) D361 coverage: an "and (also) with" clause belongs to the preceding statement only when no sentence boundary (`PROSE_CUT_RE`, D366) lies between the statement verb and the clause; body text such as "... high-volume and with a high yield" after the footnote statement is not a clause. `_prose_checks` change + test (`test_d366` case on lit_h11 zhang2023d); lit `check all` 0 errors, OFC `check all` 0 errors / 48 warnings, every finished batch's derived files byte-identical to the pre-change snapshot; 115 header tests pass | false positive on real text |
| D410 | (lit_h10 vandekerckhove2025) A postal-box code printed between unit and org ("CP ...", "BP ...", "P.O. Box ...") is recorded as `skip_between: "<postal box>"`: the checker verifies a box-code pattern in the unit-org gap and the code is never stored (YAML, derived files). Tests: clean case and missing-token case; lit `check all` 0 errors, OFC unchanged | no postal data in committed files |
| D412 | Author-list artefacts become slot names (D359): "Daoxin Dai A" (wang2014, bauters2013; committed 2026-10-23), "Jelena Vuckovic A" (white2022 / white2024; committed), "Marc de" (de2020), "Zhou Z" (gao2026). Follow-up: a curated, replayable author-list correction file applied in `lit_author_lists` and `ofc_headers.lit_papers`, with same_as redirects for the committed ids; not done this session | never publish a truncated name as a person |
| D413 | An author-list name without Latin letters (Greek / Cyrillic: lahijani2026 #5, tebeneva2024 #5) gets no lit slot: it folded to no name key and produced `person_unnamed` ids without xref rows. `people.lit_list_name_ok`; the build counts them as dropped; their header rows stay staged; `test_real_people_tables` expects rows only for created slots (also excludes the two slots_from_header papers, which have no author list) | identity key required |
| D400 | The 184 `lit` papers cached on retrieval days 2-4 (not in lit_h01-lit_h04) queued with `queue --corpus lit --size 27`: lit_h05-lit_h10 (27 papers each) and lit_h11 (22); one extraction subagent per batch under `CONTRACT.md`, check to 0 errors, then `aggregate --corpus lit`, a fresh-context audit, and the people rebuild (`LIT_MERGE` already on, DevLog-004) | DevLog-011 scope: every cached `lit` paper |

- [x] lit_h05-lit_h11 extraction (subagents), `check --corpus lit` 0 errors each (2026-10-29 02:35; D406 checker fix for lit_h11).
- [x] `aggregate --corpus lit`; fresh-context audits ([batches 2](audits/2026-10-29-lit-header-batches-2-audit.md): lit_h05-lit_h11, 936 slots checked, 922 ok, 5 fixed; [batches 3](audits/2026-10-29-lit-header-batches-3-audit.md): lit_h12-lit_h15, 451 slots checked, 435 ok, 4 fixed; GO).
- [x] People rebuild with the new lit slots, validate_db, views rebuild (03:36, below).

### Progress 2026-10-29

- 01:27 queue: lit_h05-lit_h11 (184 papers); lee2022 removed from lit_h07 (its cached file was another paper, DevLog-007 D397): 183 papers.
- 01:58-02:35 extraction (one subagent per batch), all `check --corpus lit` 0 errors:

| batch | papers ok / partial / unreadable | slots recorded / total | rows | notes |
|---|---|---|---|---|
| lit_h05 | 26 / 0 / 1 | 220 / 229 | 272 | cheung2022 unreadable (statement words run together in text and PDF layer); explicit slots bogaerts2007a Pluk, cai2021 Li (list typo) |
| lit_h06 | 27 / 0 / 0 | 229 / 231 | 304 | author_list_differs dietrich2018 (preprint header), gao2026 C. Zhang |
| lit_h07 | 26 / 0 / 0 | 194 / 196 | 261 | slots_from_header isichenko2023 (no author list); author_list_differs ishii2003, lapointe2025 (preprint cover) |
| lit_h08 | 24 / 2 / 1 | 236 / 249 | 296 | partial liu2025a, naraine2024 (glued statements); morenopozas2025 prints no affiliation |
| lit_h09 | 25 / 1 / 1 | 179 / 212 | 237 | ryf2002 unreadable (57 names, two orgs, no markers); psaila2024 partial |
| lit_h10 | 27 / 0 / 0 | 240 / 240 | 338 | |
| lit_h11 | 22 / 0 / 0 | 166 / 169 | 203 | D406; author_list_differs winkler2024, zhang2025, zhu2024 |

- `aggregate --corpus lit`: 199 org-request strings, 0 conflicts, 9 header-only authors (local list).
- Checker gaps seen (not fixed): "was with A and is now with B" (present address not recordable: ishii2003, ozdemir2021); "Current address:" cue (beeck2021); plain ", with A" clauses (recorded as more_orgs); statements with run-together words (cheung2022, psaila2024, liu2025a, naraine2024); 300-character statement window (liu2022a); hyphenated country across a line break (ozdemir2021).
- Before commit: fresh-context audit of lit_h05-lit_h11 incl. a privacy scan (a postal-box code was put in a `skip_between` span: vandekerckhove2025).
- 03:01 day-5 papers queued: lit_h12-lit_h14 (27 each), lit_h15 (1); extracted 03:05-03:12 (all `check` 0 errors), audited (GO).
- `check all --corpus lit`: 381 papers (369 ok, 6 partial, 6 unreadable), 0 errors; `aggregate`: 252 org-request strings, 0 conflicts, 10 header-only authors.
- 03:27-03:37 people rebuild: backup `cache/backup/people_before_lit_h05-h15_build_20261029T102710Z.zip`; first build exposed D413 (two unnamed persons); `data/people/` restored from HEAD, rebuilt with D413, second run byte-identical, derive_transitions, build_views, app build + 58 app tests. people 7583 -> 8991, observations 12941 -> 15759; no committed person or observation id removed; 54 committed persons changed (mostly public -> review: new lit name collisions under the D219 rules; one same_as redirect). Slots: lit 3068 (dropped: 2 papers without author list, 2 non-Latin names, 98 authors without header rows).
- Checks 03:40: ruff clean (one pre-existing format diff in tests/test_lit_seeds.py, untouched), mypy clean, pytest 361 passed, validate_db 0 errors / 712 warnings (the new lit printed orgs not yet in the registry: org round).
- Open (next): D412 author-list corrections; org round for the lit org requests; checker gaps (present address inside a statement, "Current address:", plain ", with A" clauses, run-together words, blocks printed above the title, 300-character window, contact masking eating a glued place); D382 forced matches (si2026, uddin2023, dong2010, li2024a, oh2023); a pre-existing EO-atlas observation (eo:niels2025) carries a postal-box code in its unit field (upstream data).

### Progress 2026-10-29 late (DevLog-007 D415)

- 23:31 queue: lit_h16 (29 day-6 papers, `queue --corpus lit --size 29`).
- lit_h16 extraction (one subagent), `check --corpus lit` 0 errors / 1 warning (bauters2011 explicit slot):

| batch | papers ok / partial / unreadable | slots recorded / total | rows | notes |
|---|---|---|---|---|
| lit_h16 | 27 / 2 / 0 | 231 / 238 | 259 | partial chang2026a (letter markers glued to the block's first word: new checker gap; 3 blocks unrecorded, 1 author unreadable), sun2022 (two blocks print the same marker); author_list_differs chang2026a, he2023, jin2021, ye2019; "Current address:" cue (ji2017, koyaz2026); 19 unmapped org strings |

- Fresh-context audit dispatched (`DevLog/audits/2026-10-29-lit-header-batches-4-audit.md`), then `aggregate --corpus lit` and the people rebuild.
- 23:48 audit ([record](audits/2026-10-29-lit-header-batches-4-audit.md)): all 29 papers / 238 slots read, 0 wrong,
  11 imprecise (6 fixed: nader2025 University of Colorado campus Boulder on 6 slots, as lit_h06 / lit_h09; 5 are
  checker gaps), verdict GO. `check lit_h16` 0 errors / 1 warning; `aggregate --corpus lit`: 265 org-request strings
  (was 252), 0 conflicts, 13 header-only authors. Privacy scan clean.

| # | Ruling (coordinator, 2026-10-29) | Rationale |
|---|---|---|
| D416 | lit_h16 audit questions: (1) chang2026a block b stays unrecorded until the glued-letter-marker checker gap (G1) is fixed, then recorded with the institute as org like lit_h03 / h04 / h10 / h13 (no one-off org = academy form); (2) ledezma2022 (lit_h07) Caltech `more_orgs` on the printed JPL block: normalize to the parent rule (no parent copied) in the D412 / checker follow-up pass, not now; (3) chang2026a author list (Ting Xu twice, Yulin Wu missing) and (4) zhang2025b "Daoxin Dai A" go into the D412 author-list correction file; Ting Xu slot 4 confirmed; (5) yang2024 "University of Wisconsin - Madison" kept as printed in `org`, mapped by alias in the org round | consistency with committed batches; no re-work of committed rows in this pass |

- 23:52 people rebuild: backup `cache/backup/people_before_lit_h16_build_20261030T065136Z.zip`; dry-run then build:
  lit slots 3068 -> 3299 (+231), dropped without header rows 98 -> 105; people 8991 -> 9134 (+143), observations
  15759 -> 16022; vs HEAD no person or observation id removed, 14 persons / 16 observations changed;
  derive_transitions (local only), build_views.

### Progress 2026-10-30 (DevLog-007 D421)

- 00:21 queue: lit_h17 / lit_h18 (35 papers each, `queue --corpus lit --size 35`); extraction (one subagent each), audits ([h17](audits/2026-10-30-lit-header-batch-h17-audit.md), [h18](audits/2026-10-30-lit-header-batch-h18-audit.md)), both GO:

| batch | papers ok / partial / unreadable | slots recorded / total | rows | audit |
|---|---|---|---|---|
| lit_h17 | 30 / 5 / 0 | 236 / 247 | 255 (A) | 0 wrong, 20 imprecise (3 fixed: keyvaninia2012 III-V Lab parents dropped from more_orgs, -9 rows; 17 are checker gaps G1-G6) |
| lit_h18 | 34 / 1 / 0 | 213 / 214 | 242 (A 234, B 8 layout) | 0 wrong, 3 imprecise (2 fixed: mcnab2003 IBM Watson block country US) |

| # | Ruling (coordinator, 2026-10-30) | Rationale |
|---|---|---|
| D426 | lit_h17 / lit_h18 audit questions accepted as recommended: pernice2012 dagger recorded as marker "w" (the only form both text layers carry); keyvaninia2012 III-V Lab parents dropped (parent rule; lit_h02 keyvaninia2013 normalized in the D412 follow-up); cabezon2012 research group as org + Universidad de Zaragoza more_orgs kept until a verified skip span for building / street text exists (G6); D412 correction list adds piggott2015 / a2011 / a2013 "Daoxin Dai A" / "Jelena Vuckovic A" forms and kang2008 #1 (list Yunlu vs printed Y. / Yimin Kang); D416 (5) extended: dash-joined joint orgs (Ghent University - imec, IBM Research - Zurich) kept as printed, aliases in the org round, older split forms left; barwicz2016 Asahi Glass + AGC Electronics as two orgs; dropped-syllable name matches (fang2010, feng2011) accepted and listed for review; re-record after checker fixes: G1 hyphenated subject name, G2 pronoun statement after a comma, G3 org printed once after unit-only blocks, G4 present-address-only marker (yang2010, chen2000, keyvaninia2019), G5 org name inside an earlier block, G6 building / street span between unit and org; test `test_real_people_tables` now allows lit grade-B layout rows (D286f) | audit records 2026-10-30 h17 / h18 |

- 01:00 `aggregate --corpus lit`: 300 org-request strings, 0 conflicts, 14 header-only authors; `check all --corpus lit`: 482 papers (461 ok, 13 partial, 6 unreadable), 0 errors / 36 warnings. People rebuild (backup `cache/backup/people_before_lit_h17-h18_build_20261030T080025Z.zip`): lit slots 3299 -> 3748, dropped without header rows 105 -> 117; people 9134 -> 9409, observations 16022 -> 16543; vs HEAD (8991 / 15759) no person or observation id removed, 31 persons / 50 observations changed; derive_transitions, build_views, app build + 58 app tests.

### Progress 2026-11-02 (DevLog-007 D427)

- 22:00 queue: lit_h19 / lit_h20 (35 papers each) and lit_h21 (25), `queue --corpus lit --size 35`; one extraction subagent and one fresh audit each, all GO: [h19](audits/2026-11-02-lit-header-batch-h19-audit.md) 0 wrong / 7 imprecise (checker gaps), [h20](audits/2026-11-02-lit-header-batch-h20-audit.md) 0 wrong / 15 imprecise (2 fixed), [h21](audits/2026-11-02-lit-header-batch-h21-audit.md) 0 wrong / 4 imprecise.

| # | Ruling (coordinator, 2026-11-02) | Rationale |
|---|---|---|
| D442 | wang2025 block 4: the extractor's altered `skip_between` ("2012Labs", no space, passes the D244 scan) is rejected. "2012 Labs" is a Huawei lab name in the unit chain: narrow scan exemption `\b\d{4}\s+(?!Labs?\b)[A-Z][a-z]+` with a test (`test_address_scan_lab_name_exemption`), block recorded as printed in `unit`. h20 F1 (oser2019 present address) and F2 (palmer2026 UCC parent dropped) accepted. h21 sun2025 unit chain accepted, older two-org rows unchanged. Dropped-syllable matches accepted for the D426 review list: jia2025 #3, song2025 #1, wang2025b #5, wang2026f #2, xue2026 #2. Open follow-up, not done here: D412 author-list correction file (bian2025 7 names, spektor2023 #10, primiani2019 #10, su2026 #5, wang2025 #5, wang2025b #2 #12, xue2026 #4, yoo2022 #9, yi2024a #11: no rows until it exists); checker gaps: last-author marker window (chen2024b #6), department after org (iseghem2022), country hyphenated across a line (lindenmann2014, palmer2026), "Current affiliation" / "Present affiliation" cues (stanton2020 #4, zhang2025c #2), token-exact `skip_between` verification; sweep of committed lit batches for symbol marks noted as not recordable | privacy check not bypassed; never publish a truncated name |

### Progress 2026-11-04 (DevLog-007 D447)

- 18:30 queue: lit_h22 (35 papers), lit_h23 (9), `queue --corpus lit --size 35`; one extraction subagent and one fresh audit each, both GO: [h22](audits/2026-11-04-lit-header-batch-h22-audit.md) 275 slots, 265 ok / 10 imprecise / 0 wrong; [h23](audits/2026-11-04-lit-header-batch-h23-audit.md) 72 slots, 69 ok / 3 imprecise / 0 wrong.

| # | Ruling (coordinator, 2026-11-04) | Rationale |
|---|---|---|
| D449 | Audit fixes applied, `check --corpus lit` 0 errors on both batches: h22 F1 gundavarapu2018 block 1 `org` University of California + `campus` Santa Barbara (5 rows map to org_ucsb); h22 F2 hoffman2016 block 3 `org` Universiteit Gent + `skip_between` for the site word (rows map to org_ghent_university); h22 N1 song2021b note no longer names a campus; h23 N1 yasui2026 note (no printed legend for the asterisk); h23 N2 zhuang2025 note (text layers lose the word spaces, the page is readable). kim2026 #1-#3 and zhuang2025 #9, #12, #13 stay without rows until the checker gaps are fixed (kim2026: org printed once after unit-only blocks, as foster2006; zhuang2025: glued statement subjects, as psaila2024, liu2025a, naraine2024). The values are in the audits | audited, no printed text altered |

- Open from these audits: shi2026 #2 for the D412 correction file; huang2019b #5 for the D426 review list; 5 org-round aliases to existing ids (h22); lit_h03 qi2024 P8 records Hefei National Laboratory as a USTC unit while h04, h10 and h23 record two orgs (org round).

### Progress 2026-11-06 (DevLog-007 D457)

- 01:20 queue: lit_h24 (28 papers, day 9 wave 1), `queue --corpus lit --size 35`; one extraction subagent and one fresh audit, GO: [h24](audits/2026-11-06-lit-header-batch-h24-audit.md) 204 slots, 178 ok / 26 imprecise / 0 wrong.

| # | Ruling (coordinator, 2026-11-06) | Rationale |
|---|---|---|
| D461 | Audit fixes applied, `check lit_h24 --corpus lit` 0 errors / 1 warning (hazan2021 explicit slot), rows 286: F1 heim2026 and F2 puckett2021 `org` University of California + `campus` Santa Barbara (D301, 31 merged UCSB blocks); F3 jung2026 units Kirchhoff Institute for Physics / Center for Nanotechnology (unit follows the org directly, not the iseghem2022 gap); N2 zhou2025a note. Extractor questions: yang2018 De Gruyter footnote recorded `grouped` (D368; the checker fails when an author is moved, so the grouping is verified) is the rule for later De Gruyter papers; franken2025 block 2 country stays empty until the checker accepts "nl" as a printed form of NL (as "us", "uk"; no general alpha-2 rule, US state codes would pass); fan2021 campus without the acronym (D301, khope2019); perezgalacho2017 4 orgs (D285, lit_h20). Waiting on checker gaps, no rows: dutta2025 #8 second marker (as chen2024b), zhou2025a #1-#3 (glued verb; re-record with Beijing Institute of Technology as org and its institute / key lab / innovation center as units, the Chongqing key laboratory as its own org). li2025a #9 and su2017 #5 go to the D412 correction file | audited, no printed text altered |

- 01:51 queue: lit_h25 (17 papers, rest of the day 9 IEEE session); one extraction subagent and one fresh audit, GO: [h25](audits/2026-11-06-lit-header-batch-h25-audit.md) 154 slots, 147 ok / 7 imprecise / 0 wrong.

| # | Ruling (coordinator, 2026-11-06) | Rationale |
|---|---|---|
| D466 | Audit fixes applied, `check lit_h25 --corpus lit` 0 errors / 0 warnings, rows 182 -> 184: F1 caillaud2021 block 2 joint unit IMS Laboratory recorded as its own org with University of Bordeaux and CNRS in `more_orgs` (D285; IEF, C2N, INL, LTM precedent); N1 kurczveil2013 and N2 golshani2021 notes. Extractor questions: bayoumi2025 P2 (group chain, imec, Ghent University) recorded as Ghent University + unit chain + imec in `more_orgs`: D416 (5) extended to comma-joined org pairs (deng2026, deng2026a, brouckaert2007, sattari2020, elsaeed2024); tsakyridis2020 site name in the address position left out (lit_h10, lit_h13); caillaud2021 block 1 place stays empty (not printed, D288 / D249); bolk2018 #6 not a D412 case, goes to the D426 review list. Waiting on checker gaps, no rows: poulton2017 #1 #4 #6 #8 "Current Affiliation" cue (D442), moscosomartir2017 #7 present-address-only marker (D426 G4). 7 unmapped org strings for the org round | audited, no printed text altered |

- 02:11 `aggregate --corpus lit`: 384 org-request strings, 0 local conflicts, 27 extra authors; `check all --corpus lit --dry-run` 0 errors / 51 warnings (640 papers ok, 17 partial, 7 unreadable). People rebuild (backup `cache/backup/people_before_lit_h24-h25_build_20261106T101145Z.zip`): dry-run then build, second run byte-identical; persons 10133 -> 10296 (public 8685 / review 1611), observations 18077 -> 18547 vs HEAD, no person or observation id removed; lit slots 5264; derive_transitions (113 transitions, local only).

## Session 2026-11-06 evening (day 10 ingest, DevLog-007 D512)

- 22:28 queue: lit_h26 (23), lit_h27 (22), `queue --corpus lit --size 23`; one extraction subagent and one fresh audit per batch. h26 audit GO: [h26](audits/2026-11-06-lit-header-batch-h26-audit.md) 194 slots, 162 ok / 32 imprecise / 0 wrong.

| # | Decision | Rationale |
|---|---|---|
| D521 | lit_h26 audit fixes applied, `check lit_h26 --corpus lit` 0 errors / 6 warnings (explicit slots, D287 / D369), rows 233 -> 258: F1 marinins2022 unparked (author 12's present-address line is printed in full without word spaces; `show` masked the whole run, the checker verifies it): pending record uncommented, P6 Aeva Technologies (Mountain View, US) present address inserted, P6-P11 -> P7-P12; F2 cabo2024 `Université Paris-Saclay` with its accent (D282); N1 iadanza2024 note. Extractor questions: ji2026 org Applied Materials + unit Varian Semiconductor (lit_h06 Nokia / Bell Labs precedent); cabo2024 CSIC + institute unit, denicola2013 National Research Council + institute unit (needs a lit alias, D275), nikolai2025 EPFL from the parenthesis: accepted for this batch; the corpus split on CSIC institutes (lit_h14, ofc_h11 record them as orgs) goes to the org round, no retro-edit; hatori2014 locality empty (Komaba not recorded, D288 / D366). Re-record list: iadanza2024 block 1 (IBM Research, OCR apostrophe markers) and jung2025 block b (glued letter marker, D416 (1)). Open: `ofc_headers.py show` masking should use the address-only pattern of `_prep` (D366) so a space-less line is not hidden; script not changed in this session | audit h26 |
- h27 audit GO: [h27](audits/2026-11-06-lit-header-batch-h27-audit.md) 180 slots, 147 ok / 33 imprecise / 0 wrong.

| # | Decision | Rationale |
|---|---|---|
| D522 | lit_h27 audit F1 applied (perez2017, yan2025, zhao2025: `locator: "p.1 footnote"` on 9 blocks, 27 slots), `check lit_h27 --corpus lit` 0 errors / 0 warnings, rows 233. F2 spiga2016 (department on the imec centre row, not Ghent University as in D466 / lit_h01 / lit_h05) left as recorded until the checker accepts one `more_orgs` org between unit and org; then re-record. Extractor answers accepted: yu2023a one org name (lit_h19 guo2024), raptakis2024 ICCS org + lab unit + NTUA more_orgs (ofc_h04 / ofc_h11), sun2021 WNLO org + school unit (lit_h19), no campus for Southeast University Sipailou (D301). zhao2025 Torres-Company `slot: 0` -> D412 correction list; zhang2022b name-order swap and spiga2016 "Xin Liang Yin" -> D426 review list; qu2024 #6 #8 and raghunathan2025 #5 present addresses -> re-record list after the "Current address" / "Present affiliation" cue fix (D442). The auditor ran one read-only `git status` (no change) | audit h27 |

- 23:02 `aggregate --corpus lit`: 421 org-request strings, 0 local conflicts, 28 extra authors; `check all --corpus lit --dry-run` 0 errors / 57 warnings (683 papers ok, 19 partial, 7 unreadable). People rebuild (backup `cache/backup/people_before_lit_h26-h27_build_20261107T070243Z.zip`): dry-run then build, second run byte-identical; persons 10296 -> 10516 (public 8845), observations 18547 -> 19047 vs HEAD, no person or observation id removed; derive_transitions (116 transitions, local only).

## Session 2026-11-08 (DevLog-007 D530; owner: "start ingesting the newly cached papers as usual")

- 11:35 queue: lit_h28-lit_h34 (`queue --corpus lit --size 21`, 141 papers: the 85 papers of D530 + 56 DevLog-015 owner-collection / coverage papers that never had a header batch). One extractor and one fresh audit per batch.
- Extraction (check 0 errors each): h28 185 / 186 slots, 245 rows; h29 159 / 165, 218 rows (gatkine2022 unreadable, hausmann2014 partial); h30 139 / 162, 157 rows (hu2022, kashiwazaki2021 unreadable; kramnik2024, lacava2016 partial); h31 180 / 199, 205 rows (liu2024 partial; liu2019 list duplicates); h32 216 / 217, 245 rows; h33 188 / 190, 230 rows; h34 150 / 152, 173 rows.

| # | Decision | Rationale |
|---|---|---|
| D546 | Header audits h28-h34 ([h28](audits/2026-11-08-lit-header-batch-h28-audit.md), [h29](audits/2026-11-08-lit-header-batch-h29-audit.md), [h30](audits/2026-11-08-lit-header-batch-h30-audit.md), [h31](audits/2026-11-08-lit-header-batch-h31-audit.md), [h32](audits/2026-11-08-lit-header-batch-h32-audit.md), [h33](audits/2026-11-08-lit-header-batch-h33-audit.md), [h34](audits/2026-11-08-lit-header-batch-h34-audit.md)): all GO, 0 wrong slots. Applied now: h28 F1 (note), h29 F1 (ferrotti2016 CEA org + LETI unit, as the 11 committed blocks) + F2 (dutt2018 present address p.6), h30 F1-F3 (notes), h31 F1 (ortegamonux2013 `p.1 footnote`) + N1, h32 N1, h33 F1 (tian2025 cover blocks -> manuscript prose block P1, D366). Waiting on checker changes (re-record lists): glued letter markers (gatkine2022, lacava2016), one dagger for two present addresses (hausmann2014), "Current address" cue (jung2020, purnawirman2017; D442), second marker after the last author (chen2018), building-number span (liu2024, smith2023; D426 G6, plus the "No." regex gap), Ð fold (kramnik2024), blocks before the author line (hu2022), D382 / D369 initials comparison when both forms have the same count (lai2025, yeh2024 #14 / #24), one more_orgs org between unit and org (chen2026c Hefei National Laboratory). Rulings: a2017 `grouped` is right; grouped is chosen by layout (no markers on the author line, groups printed above their blocks), not by publisher. babichev2025 Novikov keeps slot 10 (a patronymic initial is not an unexplained initial; D369 addendum). kashiwazaki2021 stays unreadable (biographies only). D412 correction-file candidates: a2017 #1, alexander2024 (collective name + 29 of 101), liu2019 duplicates, simpanen2017 #3, lai2025 #1 #2 #4, levy2026 #8, helgason2023 (Torres-Company), xie2026 #9, wang2025a #2, yeh2024 (30 of 42). D426 review list: chen2019 #3, jia2014 #7, tian2025 #1, yeh2024 #14 / #24 until the D412 entry | audit verdicts; checker gaps recorded, not worked around |
- 12:22-12:23 fixes of D546 applied by a subagent; `check lit_hNN --corpus lit` 0 errors on h28-h33 (h29 rows 218 -> 214, present addresses 3 -> 4); h34 unchanged.
- 12:23 `aggregate --corpus lit`: 484 org-request strings (421 before), 0 local conflicts, 119 extra authors (alexander2024 adds 72); `check all --corpus lit --dry-run` 0 errors / 77 warnings (817 papers ok, 23 partial, 10 unreadable; 8744 rows). People rebuild (backup `cache/backup/people_before_lit_h28-h34_build_20261108T202417Z.zip`): dry-run then build, second run byte-identical; persons 10516 -> 11219, observations 19047 -> 20529, xref 11861 -> 12651, aliases 1997 -> 2201; `derive_transitions.py` 123 transitions, 483 name-only candidates (local only).
