---
title: OFC 2026 header extraction - paper-printed author affiliations (grade A) for the people atlas
date: 2026-10-22
status: extraction done 2026-10-22 (pilot + 15 batches, 620 papers, check all 0 errors); batch audit 2026-10-23 GO for the people merge, its conditions D300-D305 applied; merge designed, not executed
scope: DevLog-000 phase P3 item "OFC header extraction (677 papers, LLM batches, audit; emails stripped) to get multi-affiliation rows"
authors: Claude (at Wentao Jiang's request)
---

# DevLog-008: OFC 2026 header extraction

Decisions here are D170-D179, the coordinator rulings D240-D245, the audit fixes D246-D249 the batch fixes D281-D289 and the batch-audit fixes D300-D305 (D170-D179 are full; D250-D255 belong to DevLog-007, D290-D299 to the supply stream). Plan source: [DevLog-000](DevLog-000-plan.md) (D4 facts only + `p.~N` locators, D8-D12
grades and visibility, D11 e-mails stripped), [DevLog-004](DevLog-004-p3-people.md) (slot model D62, observations D67,
visibility D70, validator D97, binding people-data rules). This stream does not edit `data/people/*`,
`scripts/build_people.py`, `src/photonics_atlas/people.py`, `tests/test_people.py`, `data/registry/` or
`data/schema/`; changes needed there are proposals (section Merge path).

## What exists and what the headers add

| Input | Content | Grade in the people build |
|---|---|---|
| OFC metadata `ofc_full_metadata.json` `authors_json` (adapter `adapters/ofc.py`) | 830 presentations, one affiliation string per author (organizer submission data), order = program author order | B, kind `conference`, `aff_role` primary only, locator `program metadata authors_json #<i>` (D67) |
| OFC extracted text `PlayGround/20260320_OFC/extracted_text/*.md` | 677 papers (Marker extraction of the PDFs, no page markers); title, author line with markers, affiliation blocks, contact line, abstract | not used yet |
| Local PDFs `PlayGround/ofc-2026/ofc_browser/pdfs/` | 126 PDFs (125 with a header-bearing text) | not used yet |

Survey of the 677 texts (2026-10-22): 672 have a header before "Abstract"; 5 (M2F.4, M4C.1, Th1C.1, W1I.3, W4I.1)
are slide-type extractions without an "Abstract" (1 metadata author each, W4I.1 2; corrected 2026-10-22, audit finding 17). 661 of 672 headers print a contact e-mail. 54 OFC presentations
are EO papers (`same_as eo:`); the people build drops their OFC rows (EO paper-printed rows are canonical, p6).

The paper header adds: per-author affiliation as printed (unit + org + locality), several affiliations per author
(markers `1,2`), present-address footnotes ("Now with ..."), and corrections where the organizer metadata holds a
different or stale affiliation. These become grade A `publication`-type facts with an approximate locator.

Extraction quirk found in the survey: in many texts the superscript markers survive on the author line (`<sup>1</sup>`
or `Mori2,1`) but are lost on the affiliation line (blocks listed in order without their numbers). Marker basis is
recorded per affiliation (D173) instead of silently assuming order.

## Decisions (D170-D179)

| # | Decision | Rationale |
|---|---|---|
| D170 | Authored artifact = one `headers.yaml` per batch, written by the extractor (LLM): per paper, the affiliation blocks keyed by printed marker and the authors in header order with their marker lists. Derived by `scripts/ofc_headers.py check <batch>`: `header_rows.csv` (one row per author slot x affiliation), `compare.csv` (header vs metadata per slot), `unmapped_orgs.csv`. The YAML is the source of truth; derived files are regenerable and never hand-edited | compact, LLM-friendly input; mechanical expansion avoids hand-typed slot indices and row repetition |
| D171 | `header_rows.csv` columns: `source_id, author_index, header_pos, printed_name, aff_order, aff_marker, aff_role, org_k, org_name, unit, locality, country, aff_text, marker_basis, locator, org_ids, match_basis` (amended by D240 / D244: `aff_text` removed, `evidence_grade` and `grade_note` added). `author_index` = 1-based OFC metadata slot (D62 identity unit; D67 obs_id `ofc2026:<code>#a<author_index>.<aff_order>`), `header_pos` = position in the printed author line; `aff_order` = position in the author's marker list (first = `primary`, others `additional`, a present-address block = `present_address`, EO convention); `org_k` = 1 for the block's org, 2.. for further orgs of a joint-printed block ("University of L'Aquila and CNIT"; obs id `.k` suffix as D67 joint_printed); `aff_text` = the printed affiliation block verbatim minus e-mail / phone / URL; `org_name`, `unit`, `locality` = printed segments of it; `country` ISO 3166-1 alpha-2 of the printed country (empty when not printed); `locator` `p.~1 header` (author line + blocks) or `p.~1 footnote` (D4: approximate page; the header is on the first page) | mirrors EO `author_affiliations.csv` (org_name / unit / locality / country / locator) so the merge path is the same as for EO rows |
| D172 | Restricted corpus (D4): only names and affiliation fields are stored (D244: org, unit, city, country; no verbatim block, street or postal code); no title, abstract, body text, contact line, footnote wording other than an affiliation, equal-contribution or corresponding-author marks. E-mail addresses are never typed, not even masked; phone numbers and URLs neither | OFC 2026 is `paywalled_conference` / `restricted_local_only`; D11 |
| D173 | `marker_basis` per affiliation block: `printed` (block marker visible in the text and the author markers visible), `single` (one block, no markers, every author belongs to it), `listing_order` (author markers visible, block markers lost in the extraction: the k-th listed block is marker k; allowed only when the blocks are consecutive 1..N and N = the largest numeric author marker), `pdf` (marker read in the local PDF because the text lost it), `layout` (no markers; grouping by printed layout, e.g. authors listed under their block). All are grade A paper-printed facts; `listing_order` rows are flagged so the audit can sample them against the local PDFs (pilot check below) | never assume silently; keep the inference visible |
| D174 | Slot matching: the script matches each header author to a metadata slot: the slot at the same position when the names are compatible, else the unique compatible slot (compatible = same folded family name or swapped order, same first initial; a shared full token for compound family names). The YAML may set `slot: N` to override, or `slot: 0` for a header author missing from the metadata (no row is derived for slot 0; recorded in `compare.csv`). Every metadata slot must be matched exactly once, else the paper needs `author_list_differs: true` and a note | within one paper name + position is a safe join; cross-paper identity stays with the people build (D62/D63) |
| D175 | Paper `status`: `ok`; `partial` (some authors' markers unreadable: those authors carry `unreadable: true` and get no rows); `unreadable` (author line or blocks garbled or missing in the extraction: no rows; never guessed). Papers not queued: no text (153 of 830), no header (5), EO duplicates (54) | never invent |
| D176 | Checker (`check`; (b) amended by D244, address scan added): (a) no `@`, full-width at sign, `textnorm.EMAIL_RE`, `people.SPELLED_EMAIL_RE`, phone pattern (as `rules_people.PHONE_RE`), `http`/`www.` or the word e-mail in any file of the batch directory (raw text scan); (b) every printed name and every `aff_text` is a substring of the paper's header text after normalization (markup and accents removed, whitespace collapsed, case folded), and `org_name` / `unit` / `locality` are substrings of their `aff_text`; (c) markers: every author marker is a defined block, every block is used, `listing_order` / `single` preconditions (D173); (d) slot coverage (D174); (e) every row has a locator `^p\.~[0-9]+`; (f) papers belong to the batch, no EO duplicate, no paper twice across batches | (b) is the mechanical "never invent" guard: an affiliation that is not in the text cannot pass |
| D177 | Org mapping reuses `orgmatch.Matcher` (corpus `ofc2026`: scoped aliases, registry name, alias, ROR) on deterministic variants of the printed `org_name`, first hit wins: as printed; parenthesized part removed ("... (NICT)" -> "..."); the parenthesized acronym alone; `unit, org_name`. `match_basis` records the variant (`name:no_parenthetical`, `alias:unit_org`, ...). No fuzzy matching. Unmapped header org strings go to `unmapped_orgs.csv` (input for the org-curation stream; this stream does not edit `data/registry/` or the crosswalk). Comparison with the metadata is made on registry root orgs (parent chain collapsed, `people.org_root`) | D18/D19/D25 matching rules; units such as NTT labs collapse into the parent as in the people build |
| D178 | Per-slot comparison classes: `agree` (header root set = metadata root set), `extra` (header roots include the metadata root plus more: multi-affiliation found), `present_address` (the metadata org is the printed present address, not a regular block), `conflict` (metadata root not among the header roots), `unmapped` (a header or metadata org string has no registry org, compared as strings only), `no_header` (slot unreadable or not in the header). Counted per batch and in total | the pilot measure asked for: agreements, extra affiliations, conflicts |
| D179 | Batches: `data/_staging/people/ofc_headers/<batch>/` with `papers.csv` (queue, written by `ofc_headers.py queue`), `headers.yaml` (extractor), derived files (checker). ~40 papers per batch, sorted by presentation code; pilot papers excluded from the batches. Contract: `data/_staging/people/ofc_headers/CONTRACT.md`. The merge into the people build is designed (below) and not executed | parallel subagent work with one directory per batch |

### Coordinator rulings (2026-10-22, D240-D245)

| # | Decision | Implementation |
|---|---|---|
| D240 | (Q1) `listing_order` rows without PDF confirmation: grade B (as the metadata), note "affiliation marker inferred from block order"; `printed` / `single` / `pdf` / `layout`: grade A | `header_rows.csv` columns `evidence_grade`, `grade_note`; pilot: 10 rows B (M1A.1), 417 A; test `test_listing_order_rows_are_grade_b` |
| D241 | (Q2) conflict slots: keep the metadata observation (B) and add the header observation (A); both dated observations (D10), never drop data; conflicts listed in a local review file | Merge path item 4; `check` writes `data/_local/ofc_headers_conflicts.csv` (git-ignored; pilot: 1 slot) |
| D242 | (Q3) unmapped header org strings go to the org-curation stream as alias requests (one registry owner); this stream does not edit `data/registry/` or `config/` | `check` regenerates `data/_staging/people/ofc_headers/org_requests.csv` across all batches: `printed_org, count, locators, proposed_org_id` (exact registry name after accent / case folding, also with the parenthetical removed; empty for all 9 pilot strings) |
| D243 | (Q4) header-only authors (not in the metadata): not added to the people build; listed locally | `check` writes `data/_local/ofc_headers_extra_authors.csv` (pilot: 1, W1E.3) |
| D244 | (Q6) restricted corpus: no street addresses or postal codes in any committed file; blocks keep `org_name`, `unit`, `locality` (city), `country` only | `text` removed from `headers.yaml` (pydantic `extra=forbid` now rejects it) and `aff_text` from `header_rows.csv`; `locality` = city only (checker rejects digits or commas in it); provenance check (D176 b) now runs on each field (`org`, `unit`, `locality`, `more_orgs`) against the header text / local PDF; address scan on every YAML / CSV of a batch: postal codes (JP `NNN-NNNN`, 5- and 6-digit, SE `NNN NN`, UK, PT `NNNN-NNN`, 4 digits + capitalized word), block numbers (`N-N-N`, `N-N, Word`, `#NN-NN`), street words after a house number, Via / Rue / Calle; ISO dates exempt. `compare.csv` no longer carries the metadata affiliation string (ids only; the local conflict list has it). Applied to the pre-D244 pilot YAML (88 blocks), the final scan flags every block that contains a digit; the blocks without a digit carry no street or postal part. That copy was deleted afterwards |
| D245 | (Q5) batches run after a fresh-context audit of the pilot and tooling, dispatched by the coordinator | TODO 7 / 8 |

### Audit fixes (2026-10-22, [audit](audits/2026-10-22-ofc-header-pilot-audit.md), coordinator: D246-D249)

| # | Decision | Implementation |
|---|---|---|
| D246 | (findings 1, 2, 4, 3) The marker basis, the block a field comes from, the author -> marker mapping, the role and the country are verified against the printed text, per source (md extraction or local PDF page 1). Per source: contacts and markup removed, escaped `\*` = star, unescaped markdown `*` dropped, dagger / pilcrow / section symbols as words; each author must be printed as name directly followed by exactly its markers (symbol tokens may sit between); blocks are located after the author line in printed order (so the title is never searched), by marker + optional cue + first field (unit or org) for `printed` blocks and, on the PDF, for `pdf` blocks, by the first field otherwise (a preceding cue word belongs to the block); a block's window runs to the next block (last block: 600 normalized characters); org / unit / city / more_orgs must lie in the window; unit and org must be one contiguous printed segment (<= 10 letters between, no digits); a present-address cue must be in the window iff `role: present_address`; a recorded country must be printed in the window (word match against a 90-code table of names and forms; HK / MO / TW own codes). Paper passes when the PDF analysis is clean, or the md analysis is clean and no block claims `pdf`. `layout` needs a paper note and gives grade B ("affiliation grouping read from the printed layout") | `analyse`, `check_provenance`, `GRADE_OF_BASIS`, `COUNTRIES`; mutations a1-a8, a13, a14, a16 |
| D247 | (finding 5) Author -> slot by name only: exact name (token-equal, order-free or joined) first, then compatible; both names need >= 2 tokens; two full given names must be equal (joined), or share the first given name plus a family token (dropped middle / second family name); initials must agree with the first given name; family-name-first only against an initial. No positional assignment. A name with 0 or several candidates is an error until `slot:` is set; a `slot:` that is not name-compatible is a warning | `compatible`, `_exact`, `match_slots`; mutation a12; `test_name_compatibility` (Yi / Yu, Jun / Jian, swapped Chinese-order names, bare family name) |
| D248 | (findings 10, 12) `check` writes only inside its batch, atomically (temp file + rename), and only at 0 errors for that batch, together with `check_stamp.txt` (sha256 of `headers.yaml`); derived files are scanned in memory before writing. New `aggregate` subcommand (coordinator, after the batch checks) writes `org_requests.csv` and the two local lists from batches whose stamp matches their YAML (stale batches are reported, exit 1). Log names carry the batch label and the pid | `write_atomic`, `stamp_ok`, `cmd_aggregate`; tests `test_mutation_is_caught` (no derived files on error), `test_aggregate_skips_stale_batches` |
| D249 | (findings 3, 11, 13, 14, 16, 17, 18; W1G.2) Contract: quoted ISO code of the place printed in the block, HK / MO / TW own codes, no inference; non-affiliation footnotes are not blocks (checker rejects "no longer / deceased / visiting / on leave / retired" in fields); `partial` = >= 1 unreadable author, `ok` = none; two printed orgs in one block -> `org` + `more_orgs`. YAML loaded with booleans limited to true / false (NO stays Norway). Address scan extended (house number after the street name, NL / CA / DK-style codes, room / building / floor numbers) and applied to every field as well as every YAML / CSV line. `map_org`: acronym-alone variant last and only through `ofc2026`-scoped aliases. Pilot: W1G.2 block 6 recorded as joint-printed (`more_orgs`: the state key laboratory; unit empty), countries quoted, Th1D.1 note corrected; doc errors corrected (finding 17) | pilot now 428 rows (418 A, 10 B), 10 unmapped strings; mutations a10, a11, a15, a17, a18, a19 |

### Batch ofc_h01 fixes (2026-10-22, coordinator: D282-D285, renumbered on 2026-10-22 from the D25x range (D252 -> D282 ... D255 -> D285, D251 -> D281) because DevLog-007 also used D250-D255; D281 recorded by the coordinator)

| # | Decision | Implementation |
|---|---|---|
| D282 | Text fold maps extraction artefacts: dotless / dotted i (U+0131, U+0130), dotless j, and detached spacing accents (acute U+00B4, tilde, circumflex, diaeresis, cedilla, breve, caron, dot, ring, double acute, ogonek, backtick) are removed or mapped before `ascii_fold`, so a name extracted as "Lu" + acute + dotless i + "s" matches "Luis" with an accented i | `FOLD_FIX`, `fold_text` used by `alnum`, `_norm_map`, `_words`; `test_fold_artefacts`. M1C.3 re-extracted (status ok; blocks 1, 2, 4 listing_order grade B, block 3 printed) |
| D283 | Shared organization prefix: a block may take its org from a prefix printed once before a run of marked blocks (`org_from_prefix: true`); the block is located by marker + its unit or city; the org must be printed directly before the first block of the run; unit / city / country are checked in the block window as usual | `AffIn.org_from_prefix`, `analyse`; `test_org_from_prefix` (3 mutations). M1I.5 re-extracted (status ok; 7 USGS authors with blocks 1-4, no country printed) |
| D284 | An author with `unreadable: true` is not checked against the printed text (name or markers) but still needs a metadata slot (name match or explicit `slot:`) | `analyse` skips unreadable authors; `test_unreadable_author_needs_slot_not_name` |
| D285 | Contract: a single block printed with a marker is `printed` (authors carry the marker); an unmarked single block is `single`. French joint research units (UMR: IRISA, Institut FOTON, ...) like state key laboratories: `more_orgs` when printed as a separate org, `unit` only when printed as a sub-unit. Two places in one block: the first place as `locality`, the second in the note | CONTRACT.md |

### Batch cleanup (2026-10-22, coordinator: D286-D289)

| # | Decision | Implementation |
|---|---|---|
| D286 | Checker fixes from the 15 batches. (a) Country table = all 249 ISO 3166-1 alpha-2 codes with printed names / forms (Uruguay was missing). (b) `_prep` drops link targets and keeps link text (ORCID "[,](https://orcid...)" between name and marker), images and bare URLs. (c) Block placement: whole-word matches only (UBITECH no longer inside QUBITECH, FORTH inside a longer name), unit first (an org printed directly before the unit starts the block), and each block searched after the previous block's last located field (shared orgs: M2K.5, Tu2J.5, W1G.1, W2A.56, W3K.6, W4B.6). (d) Exact markers: authors are located in order; the printed marker run between a name and the next name must equal the recorded markers plus the new per-author `dropped_markers` (marker + reason); symbol marks that no block uses are ignored; a "1" printed on the authors of a single unmarked block is allowed (contract); the last author keeps the prefix rule. (e) `marker_trailing: true` for blocks printed "Org, City, Country (1)": grade A, the marker must follow the block's last field. (f) Mixed layout: at most one unmarked regular block; next to marked blocks it must be `layout` (note, grade B) and holds every author without a marker. (g) No folding of lookalikes ("l" or a stray digit is not marker 1) | `TOK_RE`, `_find_word`, `_locate_block`, `_author_marks`, `DroppedIn`, `AffIn.marker_trailing`; 18 parametrized cases `test_d286`, `test_no_fold_for_lookalikes`; four older mutation tests now report the D286 message (still caught); auditor harness rerun: 19 / 19 caught. The stricter marker rule raised 77 errors in 15 already-passing papers: 7 single-block papers with a printed "1" on the authors (now allowed, contract) and 8 papers whose authors print an equal-contribution or "no longer affiliated" footnote number that the batch notes already documented: recorded as `dropped_markers` (M3D.6, W1B.5, W1G.5, W1G.7, W3E.4, Th2A.47, Th3A.2, Th3F.3) |
| D287 | Explicit `slot:` only for misspellings / transliterations, name-part variants, nicknames or alternate names with agreeing initials (listed cases), or a printed parenthetical name; a different name or a differing first initial is `slot: 0` + `author_list_differs` + note | All 56 non-zero overrides reviewed; 7 set to `slot: 0` (49 kept): M4B.6 Qing Wang (metadata Wing Wang), W1D.3 Huanyu Le (Le Yu), W1J.2 and W4K.5 R. M. Stevenson (Mark Stevenson), W4K.5 J. I. Davies (Iwan Davies), Th2A.8 Sheng-Fu Lin (Vincent Lin), and Tu3D.1 Ziawei Luo (Jiawei Luo: first initial differs; flagged to the coordinator). Kept: M1J.1 M.R.A. Hassan -> Rosdi Hassan (name-part variant, same as the listed Th4B.8 case), Tu2J.2 Alex. F -> Alex Fann (initials agree; author unreadable) and the misspelling / nickname cases |
| D288 | Contract: leading articles copied as printed (org matching tries the name without "the"); "Hong Kong" inside an org name is not the place (HKUST (Guangzhou) -> CN); province / prefecture only -> locality empty; two places -> strictly the first printed (M2J.5 block 3 now Theale); a department printed between a joint institute and a second org is dropped with a note | CONTRACT.md; `map_org` variant `no_article`; M2J.5 corrected. HKUST (Guangzhou) blocks were already CN (h09, h11, h15) |
| D289 | Totals across the pilot and the 15 batches (below, Progress 23:45) | `check all` + `aggregate` |

### Batch audit fixes (2026-10-23, [audit](audits/2026-10-23-ofc-header-batches-audit.md), coordinator: D300-D305)

| # | Decision | Implementation |
|---|---|---|
| D300 | (W1) h09 W2A.39: Weisheng Hu is metadata slot 6 | `slot: 0` and `author_list_differs` removed, note corrected; the slot now has a header row; header-only authors 83 -> 82 |
| D301 | (W2, S2) Campus rule: when the place printed right after a multi-campus or homonym org names a distinct campus or institution, the org match uses org + place, never the parent or homonym | New block field `campus` (verified inside the block window, place only); row `org_name` = "org, campus"; `map_org` variants all keep the campus; a parenthesized place ("(Guangzhou)") is never dropped by the parenthetical variant (acronyms still are). Applied to every occurrence found: h07 W1B.5 block 3 ("the Chinese University of Hong Kong, Shenzhen": unmapped, no longer `org_chinese_university_of_hong_kong`), h05 M4F.1 ("University of California, Davis": now `org_university_of_california_davis`), h10 W3C.2 ("Indian Institute of Technology, Delhi": unmapped), h02 M2K.3 ("University of Maryland, College Park": unmapped). CUHK blocks printed at Shatin / Hong Kong (Tu2E.6, M1F.7) are the main university and unchanged. Contract + tests `test_campus_row_is_not_the_parent`, `test_parenthesized_place_is_kept`, `test_d30x` |
| D302 | (S1) An explicit `slot: 0` author whose name is compatible with a metadata author left unmatched is an error | `match_slots`; `test_d30x` (W2A.39 mutation); all 82 `slot: 0` authors pass (the D287 rulings are not name-compatible) |
| D303 | (S2) `org_requests.csv` = one row per (printed org, city, country) with the printed units, count, locators, proposed id, curation note | `REQUEST_COLS`; `test_org_requests_carry_place`. 127 rows, 121 distinct printed strings, 588 row references |
| D304 | (S3, S7) Six notes still carried the superseded "matched to slot N" clause after D287 (M4B.6, Tu3D.1, W1J.2, W1D.3, W4K.5, Th2A.8); Progress / Verification times did not match the run logs | Superseded clauses deleted; Progress and Verification times set to the `logs/ofc_headers_*` timestamps (the logs carry the date 2026-10-22) |
| D305 | (S5) The State Key Laboratory of Optical Fiber and Cable Manufacture Technology is requested as a child org of YOFC (no registry edit here) | `CURATION_NOTES` -> `org_requests.csv` `curation_note` on its row (61 references) |

## Merge path (designed, NOT executed; proposal for the people-stream owner)

Proposed changes, to be applied by the owner of `people.py` / `build_people.py` / `rules_people.py` /
`people.schema.yaml` after the batches are audited:

1. Loader: `people.load_ofc_headers()` reads `header_rows.csv` of every batch whose `check_stamp.txt` matches its
   `headers.yaml` (`ofc_headers.stamp_ok`) and whose paper `status` is `ok` or `partial`, keyed by
   `(source_id, author_index)`. Sources with `same_as` (the 2 EO calibration papers in `pilot/`) are skipped: EO rows
   stay canonical (p6).
2. `_ofc_slots`: the slot's identity names stay the metadata names (D62; audit finding 8): header printed forms
   (initials, "F. Masahisa") are not added to `Slot.names`, so D63 parsing, coauthor keys and display names are
   unchanged. The header form goes to the observation's `printed_name` and to `person_aliases` (`printed_variant`,
   notes "OFC header form, not used for identity"), which the validator's printed-name check accepts. `affs` = the
   header rows with `org_ids` taken from `header_rows.org_ids` (finding 9b), `printed_org` = `org_name` (for
   `match_basis` `*:unit_org`: "unit, org_name"), `unit`, `country`, `role` = `aff_role`, locator = row locator;
   `kind = publication`. Identity keys (`roots`) include every header org (present addresses and joint-printed orgs
   too, D63 shared org).
3. Observation ids (finding 7): header rows get their own namespace `ofc2026:<code>#a<i>.h<aff_order>.<org_k>`, so
   two orgs of one block get distinct ids (finding 9a); schema pattern `people_obs_id` extended to
   `#a[0-9]+\.(h[0-9]+\.[0-9]+|[0-9]+(\.[0-9]+)?)`. The metadata observation keeps `#a<i>.1` and its meaning. Person
   id reuse (D65) looks up old ids by slot prefix (`<source_id>#a<i>`), not only by full obs id, so dropping a
   metadata row never orphans a person id.
4. Metadata observation of a slot with header rows (D241, finding 6): dropped only when the header confirms it,
   recomputed at build time with the current crosswalk: `agree`, `extra`, `present_address`, or folded printed strings
   equal. `conflict` and `unmapped` keep it (kind `conference`, grade B, `#a<i>.1`); both are dated observations
   (D10). Review list: `data/_local/ofc_headers_conflicts.csv` (`aggregate`). Proposal (finding 20, needs a ruling):
   both observations of a conflict slot `visibility = review` until the entry is resolved.
4a. Grades (D240, D246): the observation copies `evidence_grade`; validator: an `ofc2026` `publication` row may be
   grade B only when its header row has `marker_basis` `listing_order` or `layout`.
4b. Header-only authors (`slot: 0`, D243): not added; local list `data/_local/ofc_headers_extra_authors.csv`.
4c. Unmapped header org strings (D242): `org_requests.csv` (`aggregate`) for the org-curation stream; merge after
   those aliases exist.
5. Crosswalk (finding 9b): `build_org_crosswalk.py` registers each header printed string with the result of
   `ofc_headers.map_org` (same variants, same order), key `(ofc2026, printed_org)` as defined in item 2, and the
   variant tag in `match_basis`, so the validator's crosswalk check reproduces the staged `org_ids`.
6. Validator (`rules_people.py`): `KIND_OF_CORPUS["ofc2026"]` becomes `{conference, publication}`; `publication`
   rows need grade A (B per 4a), a locator `^p\.~[0-9]+`, an `h` obs id and an existing header row; `conference`
   keeps grade B, `primary` and the `program metadata` locator. `active_on` stays the session date for both.
7. Schema `people.schema.yaml` v3: p4 text amended, obs-id pattern (item 3); no new columns.
8. Run (finding 19): DevLog-004 row-diff procedure before committing (new joins, splits, D65 id reuse, visibility
   changes); review every new join that rests on a header org. Tests: fixture batch with a multi-affiliation slot, a
   joint-printed block, a present-address slot, a conflict slot and an unreadable paper.

Pre-merge TODOs (people-stream owner): items 1-8 above (audit findings 6, 7, 8, 9, 19, 20). Not planned: blocks the
extraction puts after the abstract (finding 15, about 1 % of queued papers by a keyword heuristic) stay `unreadable`.

## Pilot plan

~20 papers chosen for diversity: single org, many authors (50, 48, 29), many orgs (11, 9), industry + university,
Japanese / Chinese / Korean names, present-address footnotes, lost affiliation markers, two EO duplicates as
calibration against EO's paper-printed rows (calibration only; EO duplicates are not queued), local PDF available for
some to verify `listing_order`. Extracted by the coordinator-assigned agent itself (the LLM), checked with the script,
compared with the metadata.

## TODO

- [x] 1. Read DevLog-000 / 004, people schema, OFC adapter, inputs, people build path, orgmatch.
- [x] 2. Survey the 677 texts (header presence, e-mail presence, marker forms, local PDFs).
- [x] 3. Plan + decisions D170-D179 + merge-path proposal (this file).
- [x] 4. `scripts/ofc_headers.py` (`pilot`, `queue`, `show`, `check`), contract `data/_staging/people/ofc_headers/CONTRACT.md`, `tests/test_ofc_headers.py`.
- [x] 5. Pilot (22 papers): `headers.yaml`, check 0 errors, comparison with the metadata and with EO for the 2 calibration papers.
- [x] 6. Queue: 598 papers in 15 batches `ofc_h01`..`ofc_h15` (40 papers, last 38); `skipped.csv`.
- [x] 7. Fresh-context audit of the pilot and the tooling (coordinator, 2026-10-22: 20 findings, pilot 332 / 333 ok, checker no-go) -> D246-D249 applied.
- [ ] 8. Batches by subagents (coordinator; one batch per subagent, contract as the brief), audits.
- [ ] 9. Org curation of `unmapped_orgs.csv` strings (org-curation stream; aliases, not here).
- [ ] 10. Merge into the people build (people-stream owner, after the audits; Merge path above).

## Progress

- 2026-10-22 22:00 PDT: stream assigned (coordinator). Inputs read; survey done; plan written.
- 22:05: `scripts/ofc_headers.py` written. While extracting the pilot two format needs appeared and were added before
  any data was written: joint-printed blocks (`more_orgs`, `org_k`) and the `present_address` comparison class; the
  single-block rule was relaxed so that an author line `1` with an unmarked block counts as `single`, and a
  present-address marker can accompany it.
- 22:08: pilot list (22 papers, `ofc_headers.py pilot`); headers read with `show --pdf` (local PDF page 1 with
  superscripts for 9 of the 22); `pilot/headers.yaml` written by hand.
- 22:10: `check pilot`: 0 errors, 0 warnings at the first run. To make sure the checker is not vacuous, 17 mutations
  of the pilot (invented block text, org outside its block, invented author, undefined / unused marker, e-mail /
  spelled e-mail / phone in a note, missing slot, broken listing order, bad locator, marker inside a name,
  unreadable-with-rows, pdf basis without a PDF, paper outside the batch, duplicate paper) were run in a scratch copy:
  each one is an error. 15 of them are now pytest cases.
- 22:12: `queue`: 15 batches; `check all`: 0 errors, 15 warnings (batches not extracted yet).
- 22:15: calibration against EO (below); results table. Reported to the coordinator.
- 22:17-22:27 (log times): coordinator rulings D240-D245 received and applied: grades (D240), conflict and extra-author local lists
  (D241, D243), `org_requests.csv` (D242), no street / postal data (D244: `text` / `aff_text` removed, locality = city,
  field-level provenance check, address scan). Pilot YAML regenerated mechanically (blocks' `text` dropped, locality
  cut to the city; Hong Kong SAR -> Hong Kong); the scan first flagged its own stale `header_rows.csv` and two notes
  ("authors 1-2"), so the scan now runs after the derived files are rewritten and two-part numbers count only when
  followed by ", Word" (JP block numbers). `check pilot`: 0 errors, 0 warnings, identical outcome counts.
  CONTRACT.md and tests updated (22 tests).
- 22:44-22:49 (log times): audit received (no-go: checker missed 16 of 19 new mutations). Backup of the script in the private scratch
  folder; checker reworked (D246-D249). First pilot run: 4 errors, all M3F.4 present-address cues: (a) "3Now with"
  in the PDF glued the marker to the cue word, (b) unmarked blocks started at the org after the cue; both fixed in the
  tool (digit / letter split in the word view; a cue directly before the first field belongs to the block). Then
  `check pilot` 0 errors. Auditor's harness (`ofc_audit/harness/mutate.py`, unchanged) on the new checker: 19 / 19
  caught. Pilot regenerated (W1G.2 correction: 428 rows, 10 unmapped strings; outcome counts unchanged).
  `aggregate` run: org_requests 10 strings, local conflicts 1, extra authors 1.
- Open risk: the stricter provenance rules were tuned on 22 papers; their false-error rate on the queued 598 is
  unknown. Proposal: run one batch first and look at the errors before fanning out.
- 22:54-22:58 (log times): batch ofc_h01 result from the coordinator (36 ok / 3 partial / 1 unreadable) and four checker issues ->
  D282-D285. Fold fix, `org_from_prefix`, unreadable-author rule, contract text; M1C.3 and M1I.5 re-extracted by this
  stream in `ofc_h01/headers.yaml` (only those two papers touched). `check ofc_h01`: 0 errors, 3 warnings (the batch
  agent's explicit `slot:` overrides for metadata misspellings: M1D.2, M1I.1, M1J.1); papers 38 ok / 2 partial / 0
  unreadable; 430 rows (A 375, B 55); outcomes agree 300, extra 40, unmapped 35, no_header 6. `check pilot`: 0
  errors, unchanged. `aggregate` not run (coordinator step).
- 23:18-23:28 (log times; corrected 2026-10-23, D304): coordinator: all 15 batches at 0 errors; consolidated cleanup D281-D289. Decision ids renumbered (D251-D255
  -> D281-D285; DevLog-007 used D250-D255) in this DevLog, CONTRACT.md, the script, the tests and two batch notes
  (h01, h12). Checker fixes D286 a-g; 12 withheld papers re-extracted in their batch YAMLs (h02 M2K.5; h03 M3A.2,
  M3D.3; h04 M3Z.13, M4A.3; h06 Tu2J.5; h08 W1G.1; h09 W2A.56, W3A.3; h10 W3K.6; h11 W4B.6; h14 Th2A.40), all `ok`;
  W3A.3 block 2 recorded as Nokia + Alcatel Submarine Networks (two printed orgs). Slot overrides per D287 (7 set to
  0). Contract D288; M2J.5 locality Theale.
- 23:26:31 write `check all`, 23:28:08 last `aggregate` (D289; log times, corrected D304) totals, pilot + 15 batches (`check all` 0 errors, 48 warnings = 46 explicit `slot:` overrides and 2 "listing_order although a local PDF exists" for Tu2D.2, whose PDF text is garbled; `aggregate` exit 0):

  | Item | Count |
  |---|---|
  | papers | 620 (pilot 22 incl. 2 EO calibration papers, batches 598): ok 604, partial 12, unreadable 4 |
  | metadata slots | 4821 |
  | header rows | 5477: grade A 4954, grade B 523 (listing_order 514, layout 9); primary 4853, additional 616, present_address 8 |
  | marker basis (rows) | printed 3819, single 977, listing_order 514, pdf 158, layout 9 |
  | slot outcomes | agree 3920, extra 422, unmapped 379, no_header 88, conflict 11, present_address 1 |
  | multi-affiliation slots | 541 |
  | header-only authors (local list, not merged) | 83 |
  | conflicts (local list) | 11 |
  | unmapped header org strings | 120 distinct (`org_requests.csv`; 166 summed per batch) |

  Unreadable papers (4): M2D.5 and Tu3A.6 (affiliation blocks missing from the text extraction), W1C.4 (two unmarked
  blocks, no author-to-block grouping printed), W1E.1 (six block markers lost, block order in doubt). Partial papers
  (12; 38 unreadable authors): M1F.3, W2A.3, W4K.3, Th3A.3 (blocks missing from the extraction), M1I.4, W2A.43,
  W3K.2 (misprinted block markers), Tu2F.3 ("l" for a marker), Th2A.22 (stray digit in a block), Th2A.38 (author
  markers printed "13" with no block 3), Th4B.8 (author markers lost), Tu2J.2 (one author printed without a marker).
  No local PDF exists for any of these 16.
- 23:42 (log time; the batch audit is dated 2026-10-23): D300-D305. W2A.39 fixed, campus rule (4 blocks), slot-0
  check, org_requests columns, 6 notes, log-based times, YOFC child request. `check all` 23:42:31: 0 errors, 48
  warnings; `aggregate` 23:42:46: exit 0. Totals now: papers 620 (ok 604, partial 12, unreadable 4); slots 4821;
  rows 5478 (A 4955, B 523); outcomes agree 3919, extra 422, unmapped 381, no_header 87, conflict 11,
  present_address 1; header-only authors 82; conflicts 11; org_requests 127 rows (121 distinct printed strings).

## Pilot results (2026-10-22 22:12; crosswalk as of that run, being rebuilt by another stream)

Pilot: 22 papers, 333 metadata slots, 427 header rows (primary 337, additional 85, present_address 5), marker basis:
printed 279 rows, single 109, pdf 29, listing_order 10 (one paper, no local PDF). All 22 papers `ok`; no unreadable
header among them.

| paper | slots | agree | extra | conflict | present_address | unmapped | multi-aff slots | additional rows | PA rows | basis |
|---|---|---|---|---|---|---|---|---|---|---|
| M1A.1 | 9 | 8 | 1 | 0 | 0 | 0 | 1 | 1 | 0 | listing_order |
| M1A.3 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | printed |
| M1B.2 | 9 | 1 | 8 | 0 | 0 | 0 | 8 | 8 | 0 | pdf |
| M1F.7 | 8 | 5 | 1 | 0 | 0 | 2 | 1 | 1 | 0 | pdf/printed |
| M2K.2 | 13 | 11 | 2 | 0 | 0 | 0 | 2 | 2 | 0 | printed |
| M3F.4 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | pdf |
| M4B.3 | 50 | 50 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | single |
| M4E.6 | 8 | 3 | 4 | 0 | 1 | 0 | 0 | 0 | 1 | printed |
| Tu2C.6 | 7 | 0 | 0 | 0 | 0 | 7 | 0 | 0 | 0 | single |
| Tu2D.3 | 48 | 48 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | single |
| W1D.2 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | single |
| W1E.3 | 13 | 13 | 0 | 0 | 0 | 0 | 12 | 12 | 0 | printed |
| W1G.2 | 14 | 10 | 3 | 0 | 0 | 1 | 3 | 3 | 0 | printed |
| W2A.71 | 10 | 10 | 0 | 0 | 0 | 0 | 10 | 10 | 0 | printed |
| W3E.7 | 8 | 8 | 0 | 0 | 0 | 0 | 4 | 4 | 2 | printed |
| W4H.4 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | printed |
| Th1A.2 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | printed |
| Th1D.1 (EO dup) | 24 | 22 | 1 | 1 | 0 | 0 | 13 | 13 | 0 | printed |
| Th3E.4 | 16 | 8 | 3 | 0 | 0 | 5 | 3 | 3 | 0 | printed |
| Th3F.1 | 21 | 14 | 7 | 0 | 0 | 0 | 19 | 20 | 0 | printed |
| Th4A.1 (EO dup) | 7 | 7 | 0 | 0 | 0 | 0 | 5 | 5 | 0 | printed |
| Th4C.2 | 29 | 26 | 3 | 0 | 0 | 0 | 3 | 3 | 0 | printed |
| total | 333 | 283 | 33 | 1 | 1 | 15 | 84 | 85 | 5 | |

Reading the table:

- agree 283 / 333 (85 %) at registry-root level. 84 slots (25 %) carry >= 2 regular affiliation blocks: 55 of them
  are `agree` because every block maps to the metadata's root org (NTT Device Innovation Center + Device Technology
  Labs; ZTE + the state key lab the registry places under ZTE; A*STAR IME + NSTIC, both under one root), 29 are
  `extra`. Plus 4 `extra` slots from one joint-printed block (M4E.6 "University of L'Aquila and CNIT"). Of the 33
  `extra` slots, 26 add a mapped second root org (e.g. UCAS, CNIT, NSTIC, Riga TU, RISE, Nagoya U., HS Photonics) and
  7 add only an org string that is not mapped yet (M2K.2 x2, Th3E.4 x2, M1B.2, M1F.7, Th4C.2). These are the
  multi-affiliation rows the metadata does not have; same-root second blocks still add org-level rows (unit orgs).
- conflict 1: Th1D.1 slot 20 (metadata NUS, header prints marker 1 = NSTIC only). EO's paper-printed row agrees with
  the header, so the metadata is the outlier.
- present_address 1: M4E.6 slot 3 (metadata gives the printed present address, Microsoft; the header prints NICT plus
  "Now with Microsoft Azure"). 5 present-address rows in total (M3F.4 x2, M4E.6, W3E.7 x2).
- unmapped 15 slots / 9 header org strings: 7 are spelling variants of registry orgs (checked against
  `organizations.csv`: "University of California at Davis", "Beijing Univ. of Posts and Telecommunications (BUPT)",
  "UPC" = Universitat Politecnica de Catalunya, "TIM" = Telecom Italia, "WEST Aquila S.r.l.", "University of Chinese
  Academy of Science", "Technical University of Berlin" = `org_tu_berlin`); 2 have no registry org ("Optical valley
  laboratory", "University of Connecticut", the latter a present address only); one metadata string
  (W1G.2 slot 11, a state key lab) has no crosswalk mapping. These need aliases in the org-curation stream; they are
  not counted as agreements here.
- Author lists: W1E.3 prints 14 authors, the metadata has 13 (header author 13 missing from the metadata):
  `author_list_differs`, `slot: 0`, no row derived. 1 of 22 papers.
- Name forms: header and metadata differ in form for many slots (initials vs full names, `F. Masahisa` printed as
  family-name initial + given name vs metadata `Masahisa Fujino`, compound family names, lower-case metadata names); all 333 slots
  matched automatically (D174), no `slot:` override needed.
- Text extraction quality: block markers lost in 4 of 22 texts (M1A.1, M1B.2, M1F.7 partly, M3F.4); 3 recovered from
  the local PDF, 1 (M1A.1) by listing order. Survey estimate for the corpus is not made; batch reports will count it.

Calibration against EO (the 2 EO-duplicate papers, `tobing2026`, `aihara2026`): 31 / 31 slots have identical ordered
(org, unit, role) lists after removing parenthesized acronyms (EO prints "Institute of Microelectronics", the header
row keeps "(IME)").

Effort: about 2 minutes of reading per typical paper; 50-author single-block papers are fast; multi-block papers with
lost markers need the PDF view.

## Verification (2026-10-22 23:42 log time, after D300-D305)

- `check all`: 0 errors, 48 warnings (46 explicit `slot:` overrides, 2 Tu2D.2 listing_order notices); `aggregate`:
  exit 0 (127 org requests, 11 local conflicts, 82 local header-only authors).
- `uv run pytest -q tests/test_ofc_headers.py`: 72 passed. ruff check / format and mypy on the script and the test:
  clean.

## Verification (2026-10-22 23:28 log time, after D286-D289)

- `uv run python scripts/ofc_headers.py check all`: 0 errors, 48 warnings; `aggregate`: exit 0 (120 org requests, 11
  local conflicts, 83 local extra authors).
- `uv run pytest -q tests/test_ofc_headers.py`: 65 passed. Auditor's harness (unchanged): 19 / 19 caught.
- ruff check / format and mypy on `scripts/ofc_headers.py` and `tests/test_ofc_headers.py`: clean.

## Verification (2026-10-22 22:58 log time, after D282-D285)

- `check pilot`: 0 errors, 0 warnings (unchanged: 428 rows, A 418 / B 10). `check ofc_h01`: 0 errors, 3 warnings.
- `uv run pytest -q tests/test_ofc_headers.py`: 47 passed (new: fold artefacts, h01 clean, 3 prefix mutations,
  unreadable author with and without a slot). ruff check / format and mypy on the script and the test: clean.

## Verification (2026-10-22 22:49 log time, after D246-D249)

- `uv run python scripts/ofc_headers.py check pilot`: 0 errors, 0 warnings; agree 283, extra 33, conflict 1,
  present_address 1, unmapped 15; 428 rows (A 418, B 10); `check_stamp.txt` written. `aggregate`: exit 0.
  `check all --dry-run`: 0 errors, 15 warnings (batches not extracted).
- Audit mutations (auditor's harness, rerun unchanged against the new checker): 19 / 19 caught (table in the reply to
  the coordinator; each is also a pytest case, a1-a19).
- `uv run pytest -q tests/test_ofc_headers.py`: 41 passed. ruff check / format and mypy on `scripts/ofc_headers.py`
  and `tests/test_ofc_headers.py`: clean.

## Verification (2026-10-22 22:27 log time, after D240-D245)

- `uv run python scripts/ofc_headers.py check pilot`: 0 errors, 0 warnings; outcomes unchanged (agree 283, extra 33,
  conflict 1, present_address 1, unmapped 15; 427 rows: grade A 417, B 10); org_requests 9 strings, local conflicts 1,
  local extra authors 1 (both files git-ignored, checked with `git check-ignore`).
- `uv run pytest -q tests/test_ofc_headers.py`: 22 passed (new: invented org / locality, locality beyond the city,
  postal code, street number, verbatim `text` field rejected, listing-order grade B).
- `uv run ruff check`, `ruff format`, `mypy` on `scripts/ofc_headers.py` and `tests/test_ofc_headers.py`: clean.

## Verification (2026-10-22 22:16)

- `uv run python scripts/ofc_headers.py check pilot`: 0 errors, 0 warnings (log `logs/ofc_headers_check_<ts>.log`).
- `uv run python scripts/ofc_headers.py check all --dry-run`: 0 errors, 15 warnings (batches not extracted).
- `uv run pytest -q tests/test_ofc_headers.py`: 17 passed. Full suite: 201 passed, 4 failed (`test_crosswalk`,
  `test_people` x3, `test_validate::test_real_registry_has_no_errors`): crosswalk / people / registry files are being
  rebuilt by other streams in the working tree (validator errors are people observations vs the new crosswalk); none
  touches this stream's files.
- `uv run ruff check`, `ruff format`, `mypy` on `scripts/ofc_headers.py` and `tests/test_ofc_headers.py`: clean.
- Contact scan: `check` scans every file of every batch directory for `@`, e-mail patterns, spelled-out addresses,
  phone numbers, URLs and the word e-mail; 0 hits in `pilot/`. Nothing in this stream stores header text other than
  names and affiliation blocks.

## Open questions (for the coordinator) - answered 2026-10-22 by D240-D245

1. Q1 grade of `listing_order` rows (affiliation markers lost in the extraction, no local PDF; 10 rows in the pilot):
   grade A like the rest (proposal), or kept out of the merge until a PDF check? The full PDF archive is not local
   (126 of 677 PDFs are).
2. Q2 `conflict` slots: proposal drops the metadata row and lists the slot locally for review; alternative is to keep
   the metadata row as a grade B `conference` observation beside the header rows.
3. Q3 the 9 unmapped header strings (and more from the batches): send to the org-curation stream as alias requests
   (`unmapped_orgs.csv` per batch), or let this stream add `ofc2026`-scoped aliases through the curation overrides?
4. Q4 header-only authors (W1E.3): not in the metadata, so there is no OFC slot for them; propose a new slot type in
   the people build (`ofc2026:<code>#h<pos>`, grade A) or leave them out.
5. Q5 batches by subagents: 15 batches of ~40 papers; one subagent per batch with `CONTRACT.md` as the brief; audit a
   sample (e.g. 5 papers per batch against the PDF where local) before the merge.
6. Q6 `aff_text` keeps the printed block verbatim (as specified), which includes institutional street addresses and
   postal codes (no personal data). If the restricted-corpus rule should be tighter, drop `aff_text` from the derived
   rows and keep only `org_name` / `unit` / `locality` / `country` (the provenance check would still run on the YAML).
- 2026-10-22 22:55 PDT (coordinator): D281 (finding 20): both observations of a conflict slot (metadata grade B and
  header grade A) carry `visibility = review` until the conflict is resolved. Batch ofc_h01 runs alone first; the other
  14 start after its checker errors are reviewed (false-error rate of the D246-D249 rules unknown beyond the pilot).
