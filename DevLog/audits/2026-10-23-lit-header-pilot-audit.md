---
title: Fresh-context audit of the lit author-affiliation pilot and tooling (DevLog-011)
date: 2026-10-23
scope: DevLog-011 D350-D358 + merge proposal; scripts/ofc_headers.py (--corpus lit); tests/test_lit_headers.py; data/_staging/people/lit_headers/ (CONTRACT.md, pilot/, org_requests.csv, skipped.csv, lit_h01..lit_h04/papers.csv)
auditor: Claude (fresh context, read-only; scratch runs only)
verdict: GO for batch extraction with two contract additions (findings 1, 2); merge NO-GO until findings 1-3 are fixed
---

# lit header pilot audit (2026-10-23)

Method: every pilot slot compared with the printed header / footnote statements in `references/<id>/text.md` and the
local `source.pdf` (pymupdf spans, column positions); author lists from `cache/literature/merged.jsonl` via
`cache_list.csv`; 23 mutations of my own on scratch copies; OFC and lit checks re-run into scratch copies with the
derived files diffed against the committed ones. Restricted text: only names and org / unit / city / country are named
below; nothing is quoted.

## Counts

| Item | Result |
|---|---|
| Pilot papers / slots / rows | 10 / 100 / 135 (printed 107, prose 28; all grade A) |
| Slot rating | ok 94, imprecise 6 (jayatilleka2021 P3 carriers), wrong 0 |
| Blocks checked | 39 blocks: 27 printed, 12 prose statements (kim2019 7, shikama2017 2, jayatilleka2021 3) |
| Own mutations | 23 run; 21 caught, 2 not caught (omitted statements, finding 2) |
| Lit check (scratch copy, write) | 0 errors, 4 warnings (batches not extracted); 11 / 11 derived files byte-identical |
| OFC `check all` (scratch copy, write) | 0 errors, 48 warnings; 83 / 83 files byte-identical to the committed ones |
| pytest | `tests/test_ofc_headers.py` + `tests/test_lit_headers.py` 86 passed; full suite 325 passed; `test_ofc_headers.py` unchanged in git |
| ruff / format / mypy | clean (ofc_headers.py, both test files) |
| validate_db --quiet | 0 errors, 15 warnings |
| Queue | 116 lit sources = pilot 10 + lit_h01 27 + lit_h02 27 + lit_h03 27 + lit_h04 25; each exactly once; none missing / extra; skipped.csv empty |
| Author-list sample (10 queued papers + 10 pilot) | 19 lists from merged.jsonl (virot2014 none, finding 3): complete 19 / 19; printed order equal 16 / 19 |

### Per-paper slot ratings

| paper | slots | ok | imprecise | wrong | notes |
|---|---|---|---|---|---|
| billah2018 | 13 | 13 | 0 | 0 | 5 blocks, markers incl. Vanguard (3) on Dietrich / Koos match the printed run |
| shikama2017 | 4 | 4 | 0 | 0 | 2 statements, NTT Atsugi / Tsukuba, subjects match |
| jayatilleka2021 | 8 | 2 | 6 | 0 | P1 (was with, Santa Clara) and P2 (Rio Rancho) ok; P3 under-recorded, finding 1 |
| kim2019 | 13 | 13 | 0 | 0 | 7 statements; pronoun statements P3 (They: Poulton, Timurdogan) and P6 (He: Yaacobi) correctly present addresses; campus Berkeley |
| tran2022 | 18 | 18 | 0 | 0 | equal-contribution 4 dropped x3; campus Santa Barbara |
| virot2014 | 8 | 8 | 0 | 0 | rows ok; slot source flagged, finding 3 |
| jeong2013 | 10 | 10 | 0 | 0 | building text of block 1 correctly left out |
| ashida2017 | 10 | 10 | 0 | 0 | contact marker 5 dropped |
| gao2021 | 9 | 9 | 0 | 0 | Ya Cheng 6 blocks + contact 11 dropped; block 8 unused, not recorded |
| wang2022a | 7 | 7 | 0 | 0 | Singapore locality + SG consistent with 86 OFC rows |

## Findings

1. **jayatilleka2021 P3 is not cut; pilot note and DevLog claims are false (medium).** In the local PDF the third
   statement continues at the bottom of the right column of page 1 (same footnote band, y 697 at x 314) with the rest
   of the org name and Santa Clara, US, followed by the contact list of exactly the six P3 authors; `text.md` has the
   same continuation further down page 1, after the body text. Page 1 also prints the title and the full author line
   (top of the page; in `text.md` after the footnotes), so "page 1 prints no title or author line" in the YAML note,
   the DevLog survey ("one accepted manuscript has no author line on page 1") and the progress entry are wrong. P3
   should be org Intel Corporation, locality Santa Clara, country US; the checker cannot accept it today (mutation M8:
   the 300-character statement window never reaches the other column). The 6 rows map to `org_intel` either way, so
   only locality / country / org string are affected. Fix: a prose `continued` mechanism (second anchor = first word
   of the continuation, located in the footnote band of the same page, fields checked in statement window +
   continuation window), then re-record P3 and correct the note, the DevLog survey sentence and the CONTRACT example.
   Contract line for the batches now: footnote statements can continue in the next column; record what is printed in
   both parts and note the split (the coordinator fixes them after the tool change).
2. **Omitted prose statements pass the checker (medium).** Removing kim2019 P6 (He is now with, Yaacobi) or P3 (They
   are now with, Poulton / Timurdogan) together with the markers gives 0 errors (M12, M13). Printed blocks are
   protected by the D286d marker-run check; prose statements have no equivalent, so a missed present address or
   additional affiliation ("is also with") is silent. Queued papers with such statements include alexander2026 and
   qi2024 (2), and about 18 queued papers carry statement-style footnotes on page 1. Fix: in `_prose_checks`, every
   verb-phrase match (is / are / was / were, optionally also / now / currently, with) in the searched pages whose
   subject names a slot author must be covered by a recorded prose block, else an error (statements in biographies
   on later pages are out of the searched text unless a locator names that page). Contract line now: record every
   such statement naming an author, including present addresses and additional affiliations.
3. **virot2014 has an author list (medium; D217).** `cache/literature/curator_adds.jsonl` holds uid
   10.1038/ncomms5957 with 8 authors in the printed order; `lit_papers()` reads only `merged.jsonl` (the other 11
   curator adds of the cache list are in merged.jsonl, this one is not). With `slots_from_header` the slot names are
   the header printed names, which is the identity-from-header-names case D217 excludes; merge item 4 (review or
   exclude) contains it, but the simpler fix removes it: fall back to `curator_adds.jsonl` (same `authors` field),
   drop `slots_from_header` from the pilot YAML, re-check, update `test_lit_author_lists`, and keep D352 only for a
   paper with no list in either file.
4. **Author-list order differs from the printed order in 3 of 19 papers (low).** kim2019 (metadata order scrambled),
   shamsansari2022 and riemensberger2022 (cached text is a version whose author order differs from the published
   record; lists are complete). Name matching handled kim2019 with no `slot:` override and `header_rows.csv` keeps
   `header_pos`. Fix: flag order differences in `compare.csv` (e.g. `order_differs`), and state in the merge proposal
   that the slot index is the author-list position (D62), not the printed position. Where the cached text is a
   preprint, its affiliations are attributed to the published source and its `published_on`; say so in the merge
   proposal.
5. **Membership regex misses comma-less forms (low, fail-safe).** `MEMBERSHIP_RE` leaves "Fellow OSA" (printed so in
   jayatilleka2021) and "Member IEEE"; only jayatilleka2021 has the form in the 116 papers. The residue only causes
   false marker errors for printed-marker authors, never a false pass. Fix: make the comma optional.
6. **Merge proposal gaps (low).** (a) No D218 analogue: header printed forms go to `printed_name` and
   `person_aliases` (origin lit), never to `Slot.names`; add it. (b) Item 6 relies on `same_as` only: verified 0 DOI
   and 0 title overlaps between the 116 lit sources and eo / pk / ofc2026 / lin / blog / web sources on 2026-10-23, but
   a DOI / title overlap check at build time is needed before later retrieval days (a duplicate paper would give an
   author two slots whose shared coauthors are the same paper, inflating D63 rule-3 evidence). (c) D62 lists the slot
   sources; adding `lit` slots is an owner amendment of D62, not only a code change. Otherwise the proposal respects
   D62 (one slot per author-list position, two slots of one paper never joined), D217 (names from the author list,
   header orgs not identity keys), D219d (unchanged join rule) and D219e (id form with `.m<n>`); privacy: no contacts,
   addresses, paths or personal data in any audited file (grep and the checker's own scan).
7. **Pronoun resolution uses the previous recorded statement (info).** "He / She / They" take the subject of the
   previous recorded prose block, not of the previous printed statement; correct in the pilot, and an omitted
   statement is caught here only when its authors are left without a regular block. Finding 2's coverage check closes
   this.
8. **Tests depend on the local cache (info).** 13 of 14 lit tests skip without `references/` and `merged.jsonl` (CI
   runs only the membership test); expected for restricted local text.

## Mutation results (scratch copies of pilot/headers.yaml)

| # | Mutation | Caught | Error |
|---|---|---|---|
| M1 | jayatilleka2021 Frish given P1 (wrong statement) | yes | not named in subject; named in P2 but carries no P2 |
| M2 | jayatilleka2021 Rong markers removed (missing from P3) | yes | named in statement, carries no P3 |
| M2b | shikama2017 Aratake moved P1 -> P2 | yes | both directions |
| M3 | shikama2017 P1 locality Tsukuba (from P2) | yes | not inside block |
| M3b | jayatilleka2021 P2 locality Santa Clara (from P1) | yes | not inside block |
| M3c | kim2019 P2 unit from P1 | yes | statement not located; cascade |
| M3d | kim2019 P6 country US (from P7) | yes | country not printed in block |
| M4 | kim2019 P6 (He is now with) as affiliation | yes | present-address cue |
| M4b | kim2019 P5 (was with) as present address | yes | lacks cue |
| M4c | kim2019 They-statement P3 moved to Yaacobi | yes | subject mismatch both ways |
| M4d | kim2019 He-statement P6 also on Poulton | yes | not named in subject |
| M5 | kim2019 P7 invented org | yes | statement not located |
| M5b | shikama2017 P1 invented more_orgs | yes | not inside block |
| M5c | kim2019 invented statement P8 | yes | not printed |
| M6 | jayatilleka2021 P1 street in unit | yes | street + postal (D244) |
| M6b | kim2019 P1 postal code in locality | yes | postal code; city only |
| M6c | shikama2017 address in paper note | yes | postal code in headers.yaml |
| M7 | shikama2017 statement order swapped | yes | statement not located |
| M8 | jayatilleka2021 P3 completed from the other column | rejected | finding 1 (tool limit, not a false pass) |
| M9 | shikama2017 invented prose-only author | yes | not named; header-only slot |
| M10 | kim2019 Timurdogan only the present-address block | yes | no regular block |
| M11 | billah2018 prose marker on a printed-marker paper | yes | no block; markers differ |
| M12 | kim2019 omit P6 statement + markers | **no** | 0 errors (finding 2) |
| M13 | kim2019 omit P3 statement + markers | **no** | 0 errors (finding 2) |

## Go / no-go

- Batches lit_h01..lit_h04: **GO**, with two contract lines added first: record every statement that names an author
  (incl. "also with" and present addresses), and record both parts of a statement split across columns with a note.
- Coordinator after the tool fixes (findings 1-3, 5): re-check pilot and batches; correct the DevLog survey /
  progress sentences on jayatilleka2021.
- Merge: **NO-GO** until findings 1-3 are fixed and the merge proposal carries finding 4 and 6 items.

Scratch (not in the repo): mutation and regression scripts and copies under the session scratchpad
`lit_header_audit/`.
