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
