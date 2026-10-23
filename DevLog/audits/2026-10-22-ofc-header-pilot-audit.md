---
title: Fresh-context audit of the OFC 2026 header-extraction pilot and tooling (DevLog-008, D245)
date: 2026-10-22
scope: DevLog-008 (D170-D179, D240-D245, merge path), scripts/ofc_headers.py, tests/test_ofc_headers.py, data/_staging/people/ofc_headers/ (CONTRACT.md, pilot/, ofc_h01..ofc_h15/papers.csv, skipped.csv, org_requests.csv)
auditor: Claude (fresh context, read-only; scratch work outside the repo)
---

# Audit: OFC 2026 header-extraction pilot and tooling

Verdict: pilot data are correct (332 of 333 slots ok, 1 imprecise, 0 wrong). The checker misses 16 of 19 new
mutations: it cannot tell grade-A from grade-B marker bases, it does not tie a block's fields to one printed block,
and it never verifies country, role or the author-to-marker mapping. Slot matching accepts different given names
that share an initial. Per-batch `check` runs are not safe to run in parallel. **No-go for the 15 batches until
findings 1, 2, 4, 5, 10 and the contract items in 3 / 14 / 16 are fixed** (estimate: one short tooling pass; the
fixes are listed below and the two key ones were prototyped against the pilot). The merge-path findings (6-9, 19)
have to be fixed before the merge, not before the batches.

## What was run (2026-10-22, all read-only for repo data)

| Step | Result |
|---|---|
| `show pilot --pdf` (terminal / scratch only) | 22 headers + 9 local PDF page-1 views read; every slot compared by hand |
| `check pilot --dry-run` | 0 errors, 0 warnings; agree 283, extra 33, conflict 1, present_address 1, unmapped 15; 427 rows |
| `check all --dry-run` | 0 errors, 15 warnings (batches not extracted) |
| `check pilot` (write mode) on a scratch copy of the batch tree (BASE / LOCAL redirected) | `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`, `org_requests.csv` byte-identical to the committed files; local lists: 1 conflict (Th1D.1 #20), 1 extra author (W1E.3) |
| `pytest -q tests/test_ofc_headers.py` | 22 passed |
| `ruff check`, `ruff format --check`, `mypy` on script + test | clean |
| 19 new mutations of the pilot (scratch copies) | 3 caught, 16 missed (finding table below) |
| Queue coverage script (830 presentations) | every code exactly once; skip reasons re-derived 210 / 210 |
| Contact / address scan of all 23 files under `ofc_headers/` (checker regexes + extra patterns) and git history | 0 hits (the word e-mail occurs only in CONTRACT.md instructions); the pre-D244 YAML was never committed (one commit, 9f7557b, identical to the working tree) |

Logs of the dry runs went to `logs/` (git-ignored). No file other than this audit was written in the repo.

## 1. Pilot correctness (22 papers, 333 metadata slots, 88 blocks, 334 header authors)

| Rating | Slots |
|---|---|
| ok | 332 |
| imprecise | 1 |
| wrong | 0 |

Header-only author: 1 (W1E.3 pos 13, `slot: 0`), correctly excluded. Checked per slot: author order, printed name,
marker list (against the text and, for the 9 papers with a local PDF, the PDF superscripts), marker -> block,
org / unit / locality / country split, present-address handling (M3F.4 x2, M4E.6, W3E.7 x2: all correct),
`marker_basis` (M1A.1 listing_order is the only possible basis there: no PDF, blocks 1..6, author markers up to 6; the
metadata agrees with all 9 primary blocks; M1B.2 / M3F.4 pdf, M1F.7 block 2 pdf, others printed / single: all
correct) and grade (10 B rows = M1A.1, rest A: correct). EO calibration re-checked against
`eo-modulator-atlas/data/author_affiliations.csv` (`tobing2026`, `aihara2026`): 31 / 31 slots identical in
org / unit / role order.

Non-ok slot:

- W1G.2 slot 11 (Dezhi Zhang), imprecise. Block 6 prints a research institute followed by a state key laboratory
  ("China Telecom Research Institute, State Key Laboratory of Optical Fiber and Cable Manufacture Technology"). The
  YAML records the laboratory as `unit` of China Telecom Research Institute. The same laboratory is printed under YOFC
  in M2K.2 block 2, and the metadata gives the laboratory alone, so it is not a department of the institute. Fix:
  record it as a joint-printed block (`more_orgs: [State Key Laboratory ...]`, unit empty), or keep the split and say
  why in a note.

Notes (not errors): M1F.7 block 1 country `HK` for a block printed "Hong Kong SAR, China" matches the registry
convention (`org_chinese_university_of_hong_kong` country HK; Taiwan orgs TW), but the contract does not say so (see
3). Th1D.1 note says "printed family-name-last as F. Masahisa"; DevLog-008 says "family-name-first"; the printed form
is family-name initial + given name (finding 17).

## 2. Findings

| # | Severity | Finding | Evidence | Fix |
|---|---|---|---|---|
| 1 | High | `marker_basis` is not verified, so a grade-B row can be entered as grade A (D240). `listing_order` relabelled `printed` passes with 0 errors (10 rows B -> A). `layout` has no precondition: no note is required, the marker labels are free text, and it gives grade A | mutations 5, 14 | For `printed` blocks, require `alnum(marker) + alnum(first field)` (org or unit; for present-address blocks also after a cue word: now with / now at / present address / currently) in the header text. Prototype on the pilot: 66 / 67 printed blocks pass, and the 1 miss is the "3 Now with" cue case. For `pdf` blocks, run the same test on the PDF text. Relabelled M1A.1 fails 5 / 6 blocks. `layout`: require a note and set grade B, or forbid it until the coordinator rules on it |
| 2 | High | Field provenance (D176 b) checks each field anywhere in the pre-abstract text, including the title and the contact line. D244 dropped `aff_text`, and with it the original guarantee that org / unit / locality come from one printed block. Fields can now be mixed across blocks or taken from the title | mutations 3 (locality of block 2 put on block 1), 6 (org copied from the paper title), 7 (`more_orgs` taken from another block): all pass | Compute a block window at check time (raw header text between consecutive block-marker tokens, or a <= 300-character span), require every field of a block inside one window, and leave the title line(s) and the contact line out of the search text. Nothing new is stored |
| 3 | Medium | `country` is never checked against the text, so an invented or wrong country passes. The contract's "ISO of the printed country" is ambiguous for Hong Kong / Macau / Taiwan (30 queued headers name one of them) | mutations 1 (country added to a block that prints none), 2 (IT -> FR) | Map printed country names and aliases (USA, U.S.A., UK, P.R. China, Republic of Korea, ...) to ISO codes and require one inside the block window (finding 2); empty otherwise. Contract: "country = ISO code of the printed place; HK, MO, TW as in the registry" |
| 4 | Medium | The author -> marker mapping and the block `role` are not checked mechanically. Reassigning an author to another existing block, or turning a present-address block into a regular one, passes | mutations 4 (Th1D.1 K. W. Ang 1 -> 3), 8 (M3F.4 "Now with" block as `affiliation`), 13 (markers of 2 authors swapped) | (a) Require `alnum(name) + concatenated alnum markers` in the header text or the PDF text. Prototype on the pilot: 225 / 225 authors with alphanumeric markers pass, and this catches mutations 4 / 13. Symbol markers (dagger etc.) stay with the audit. (b) Require `role: present_address` exactly when the block window has a cue word. Queued headers with such cues: 2 (M1E.4, Th1F.5) |
| 5 | Medium | Slot matching (D174, `compatible`) accepts different given names that share an initial ("Yi Wang" / "Yu Wang", "Jun Li" / "Jian Li"), swapped-order false positives ("Zhang Wei" / "Wei Zhao") and bare family names ("Anand" / "Rishi Anand"). Matching is positional first, so a header printed in a different order from the metadata attaches the affiliations to the wrong slot with no error, which amounts to a name-only join inside the paper | queued papers: 23 same-paper metadata pairs in 17 papers that `compatible` cannot separate (e.g. W2A.22 Li / Liyan / Lei Zhang; Th3F.6 three "S... Kim"; M3A.3 "Liuyan Han" / "Han Li"); mutation 12 (truncated name) passes | When both forms have full given names, require equal folded given names (ignoring hyphens and spaces). Use exact matches across the whole paper before compatible ones. Require >= 2 name tokens. Warn when a paper has an ambiguous pair and require explicit `slot:` there |
| 6 | Medium | Merge path item 4 drops the metadata observation when the outcome is `unmapped`, but `unmapped` means the header did not confirm the metadata org (one side has no registry id). This contradicts D241 (never drop data) | `_outcome` returns `unmapped` whenever the metadata or header id set is empty; pilot: 15 slots | Keep the metadata observation for `unmapped` (as for `conflict`) unless the folded strings are equal. Recompute the outcome in the build against the crosswalk current at build time, not from `compare.csv` |
| 7 | Medium | Merge path item 3 reuses committed obs ids: `#a<i>.1` (today the metadata row: kind conference, grade B, metadata org) would hold the header primary row (publication, A, possibly another org), and conflict slots move the metadata row to `.n+1`. The meaning of committed observation ids changes, while D10 treats an observation as a dated fact | DevLog-008 merge path items 3-4; D67 id pattern | Give header rows their own id namespace (e.g. `#a<i>.h<j>[.<k>]`, which still starts with `#a`, as the validator requires). The metadata `.1` keeps its meaning and is dropped only when confirmed. Or get an explicit coordinator ruling that obs ids are not stable across sources |
| 8 | Medium | The merge path does not say where `printed_name` comes from. The validator needs `printed_name` among the person's names (display_name / aliases). Header forms (initials, "F. Masahisa" = family-name initial first) either fail that check or, if added to `Slot.names`, corrupt D63 name parsing, coauthor keys and the display_name choice | `rules_people.py` printed_name check; `people.py` `s.variants` / `coauthor_key` from `s.names` | Identity names stay the metadata names (D62 already fixes the slot). The header printed name goes to `printed_name` and to `person_aliases` only, marked as not used for identity parsing |
| 9 | Medium | Merge-path org ids: (a) the header rows put the orgs of a joint-printed block as separate rows with the same `aff_order` (`org_k`). `people.obs_ids()` adds `.k` only inside one Aff, so one Aff per row gives duplicate obs ids. (b) The merge path takes org ids "from the crosswalk for the printed org_name", but `map_org` matched 15 of 427 pilot rows through variants (no_parenthetical 9, unit_org 6). The crosswalk keyed on the printed string alone will not reproduce them, and the validator then reports a contradiction or "not in the crosswalk" | pilot `header_rows.csv` match_basis counts; M4E.6 org_k=2 rows x4 | The loader builds the obs id explicitly from `aff_order` and `org_k`, and uses `header_rows.org_ids`. `build_org_crosswalk.py` registers the same variant result for `(ofc2026, org_name)` (for unit_org, the unit+org string) |
| 10 | Medium | `check <batch>` from 15 parallel subagents is unsafe. Every run rewrites `org_requests.csv` and both `data/_local` lists with a non-atomic `open("w")`, and reads the other batches' `header_rows.csv` / `compare.csv` while they may be half-written (wrong aggregates or a csv parse error in an unrelated batch). `RunLog` file names have 1-second resolution, so two runs started in the same second overwrite each other's log | `write_aggregates`, `csvio.write_csv`, `RunLog.__init__` | Add `--no-aggregate` (the subagent default) and let the coordinator run `check all` after the batches. Write through tmp + rename. Put the pid or a counter in the log name |
| 11 | Low | Address-scan gaps (D244): house number after the street name (the usual Dutch / German / Belgian form, e.g. `Examplestraat 12`; 27 queued headers carry such a pattern), Dutch postal codes `1234 AB`, Canadian `A1B 2C3`, `DK-NNNN`, "Room / Building N", `NNN 22nd Street`, and street names without a number. org / unit / more_orgs have no digit or address guard (only locality has one). One false positive: an org name of a year plus a capitalized word (`2012 Labs`) is rejected as "postal code + city" (0 such names in the queued headers) | regex probe with synthetic strings; mutation 9 (a street name without a number as `unit`) passes | Add patterns for street-word suffixes followed by a number, NL / CA / DK codes, Room / Building / Floor N. Reject the address patterns also inside org / unit / more_orgs. Allow-list known org names with digits |
| 12 | Low | `check` writes the derived files even when it reports errors, and nothing ties `header_rows.csv` to the current `headers.yaml` | `check_batch` writes whenever `write` is true | Write derived files only at 0 errors (or stamp them with the YAML hash). The merge loader re-derives from the YAML or verifies the stamp |
| 13 | Low | `status: partial` with no `unreadable` author passes | mutation 15 | Error: partial needs >= 1 unreadable author; ok must have none |
| 14 | Low | Non-affiliation footnotes ("no longer affiliated" in Th3F.2, Th3F.3; also deceased / visiting) are not covered by the contract. Entered as a block they pass provenance and become org rows and org requests | mutation 16 (a non-org string as a present-address block) passes; queued-header survey | Contract: such a footnote is not a block; drop the marker and record it in the note. Optional checker rule: reject org values matching `no longer|deceased|visiting|on leave` |
| 15 | Low | Affiliation blocks that the Marker text puts after the abstract cannot pass provenance, because the search text ends at "Abstract", even though the contract offers `p.~1 footnote`. Those papers will be `unreadable` (safe, small loss) | M2D.5 confirmed (blocks start about 2 kB after the header). Keyword heuristic candidates: M1K.3, M2D.5, M4B.6 (local PDF), Tu3E.1, W2A.24, W4H.1, Th1C.2 (about 1 % of 598; heuristic, not a count) | Optional: for blocks with `locator: p.~1 footnote`, accept a second search text that runs from the abstract to the first section heading |
| 16 | Low | YAML 1.1 reads `country: NO` (Norway) as boolean false, and pydantic reports "Input should be a valid string". The contract example has the country unquoted | mutation 19 (caught, but the message is confusing) | Quote `country` in the contract example and the pilot style; or load the YAML with a loader that keeps NO / ON / YES as strings |
| 17 | Low (doc) | DevLog-008 says the 5 `no_header` skips have 0 metadata authors. They have 1 (M2F.4, M4C.1, Th1C.1, W1I.3) and 2 (W4I.1); `skipped.csv` gives the right reason (`no_header`, since `no_metadata_authors` is tested first). The Th1D.1 YAML note and the DevLog contradict each other on "F. Masahisa" (it is family-name initial + given name) | adapter counts | Correct the two texts |
| 18 | Low | `map_org` tries the parenthesized acronym alone before `unit, org`; the docstring says the acronym is the last resort. Matching on an acronym alone can resolve to another org when the registry carries the same acronym unscoped (exact, not fuzzy; not used in the pilot) | `map_org` variant order | Move the acronym variant last, and accept it only through `ofc2026`-scoped aliases |
| 19 | Low | Merge path item 2 makes every header org an identity key, including present addresses and joint-printed consortium orgs (CNIT for every L'Aquila author). This is right under D63 (shared org), but it will add rule (2) / (3) joins, and no before / after diff is planned | DevLog-008 merge path item 2 | Run the merge with the DevLog-004 row-diff procedure (new joins, splits, D65 id reuse, visibility changes) and review the new joins before committing |
| 20 | Info | Conflict slots (D241) get two public observations of the same slot and date with different orgs | merge path item 4 | Consider `visibility = review` for both until the local conflict list is resolved |

Mutation detail (scratch copies; real files untouched):

| # | Mutation | Result |
|---|---|---|
| 1 | country added to a block that prints none (W3E.7 block 2) | missed |
| 2 | wrong country (M1F.7 block 4 IT -> FR) | missed |
| 3 | locality of block 2 put on block 1 (M1A.3) | missed |
| 4 | author marker reassigned to an existing block (Th1D.1 K. W. Ang) | missed |
| 5 | `listing_order` -> `printed` (M1A.1; grade B -> A) | missed |
| 6 | org copied from the paper title (M1B.2 block 4) | missed |
| 7 | `more_orgs` taken from another block (M4E.6 block 1) | missed |
| 8 | present-address block relabelled `affiliation` (M3F.4) | missed |
| 9 | street name without a number as `unit` (Th4A.1) | missed |
| 10 | Dutch-style postal code in a note | missed |
| 11 | Canadian-style postal code in a note | missed |
| 12 | author name truncated to the family name (M4B.3) | missed |
| 13 | markers of two authors swapped (W1E.3) | missed |
| 14 | all blocks `layout`, no note (Th1A.2) | missed |
| 15 | `partial` with no unreadable author (M1A.3) | missed |
| 16 | non-org string as a present-address block (Th1A.2) | missed |
| 17 | street + house number in `unit` (string absent from that header) | caught (provenance, not the address scan) |
| 18 | building / unit number in `unit` | caught (street number) |
| 19 | unquoted `country: NO` | caught (pydantic type error) |

## 3. Rules

- Personal data: 0 e-mail / phone / URL / street / postal hits in the 23 files under `ofc_headers/` and in git history.
  The only stored personal data are author names as printed, which the people atlas is built on. Local review lists
  are in `data/_local/` (git-ignored, `git check-ignore` confirmed).
- Facts only: the pilot values are all printed text (section 1). Guard gaps: findings 1-4.
- Org mapping: `orgmatch.Matcher` is exact (registry name key, alias key, ROR label with a unique registry org), and
  `map_org` adds only deterministic string variants. No fuzzy matching (acronym caveat: finding 18).

## 4. Batch queue

- 830 metadata presentations = 22 pilot + 598 queued (14 x 40 + 38, `ofc_h01`..`ofc_h15`) + 210 skipped (no_text
  153, eo_duplicate 52 (+2 EO duplicates in the pilot = 54), no_header 5). 0 codes twice, 0 missing, 0 unknown;
  `n_authors_meta` and `local_pdf` in every `papers.csv` match the inputs. Queued: 4488 slots, max 42 authors per
  paper (2 papers > 30), 81 with a local PDF.
- Skip reasons re-derived for all 210 with the queue rule: 210 match. Sample of 10 checked individually (M3E.1,
  Tu3I.6, W4I.3, W4C.2, M2I.6, W4C.1, Tu1A.3: no text file and no local PDF; M2A.7, Th1C.3, Tu2J.3: registry
  `same_as eo:`). The 5 `no_header` texts are slide-type extractions with no "Abstract" (M2F.4, W4I.1 inspected).
- Edge-case counts in the 598 queued headers (inputs for the contract): symbol markers (dagger-like) 34,
  equal-contribution lines 6, present-address cues 2, "no longer affiliated" 2, letter superscripts 2, Hong Kong 15 /
  Taiwan 11 / Macau 4, house-number-after-street patterns 27, headers under 250 characters 29 (mostly single-author or
  single-block, but M2D.5 has no blocks).

## 5. Merge path vs D62 / D10 / visibility / name-only joins

- D62: rows are keyed by `(source_id, author_index)` (the OFC slot), so the slot stays the identity unit and two
  slots of one paper are never joined. The weak point is the within-paper name -> slot assignment (finding 5).
- D10: header and metadata rows are dated observations with the session date. Problems: committed obs ids get
  re-pointed (finding 7), and the metadata row is dropped for `unmapped` (finding 6).
- Visibility: unchanged rule (D70: A/B public unless the person is queued); grade B for listing_order is kept by
  item 4a. Validator `GRADE_OF_KIND` needs the planned exception. Conflict pairs: finding 20.
- Name-only joins: none across papers (header-only authors excluded, D243). Within a paper, finding 5. The name-set
  side effects of header printed names: finding 8.

## 6. Required before the 15 batches (go / no-go)

No-go now. Go once these are done and the pilot re-checked (0 errors), with the new checks added as pytest cases:

1. Finding 1: marker-basis verification for printed / pdf blocks; layout needs a note and gets grade B (or is not
   allowed).
2. Finding 2: block-window co-location; title and contact line left out of the search text.
3. Finding 4a: name + marker string check (225 / 225 on the pilot); 4b present-address cue check.
4. Finding 5: stricter `compatible`, exact matches first, ambiguity warning.
5. Finding 10: per-batch `check --no-aggregate` for subagents, atomic writes, unique log names.
6. Contract edits: country rule and HK / MO / TW (3), non-affiliation footnotes (14), quoted country (16),
   `partial` semantics (13).

Recommended in the same pass: finding 3 country check, finding 11 address patterns, finding 12 derived-file
staleness. Before the merge (people-stream owner): findings 6, 7, 8, 9, 19, 20, plus the W1G.2 #11 correction.
