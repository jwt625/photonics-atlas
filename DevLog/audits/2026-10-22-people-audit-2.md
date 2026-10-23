---
title: Fresh-context audit of the corrected people build (DevLog-004 TODO 11)
date: 2026-10-22
scope: data/people/*.csv (build of 2026-10-22 22:26, D210), data/_local/people/ (local only), people.py, rules_people.py, build_people.py, derive_transitions.py
mode: read-only subagent; no network, no git writes; audit scripts kept in the auditor's private scratch folder (not committed)
---

# People audit 2 (2026-10-22)

Verdict: go. No wrong merge, no D62 violation, no privacy leak, all 10832 observations match their input rows, build deterministic, validator 0 errors, tests pass. One medium finding (F1): the D95 one-syllable rule rejects unhyphenated spellings of hyphenated two-syllable given names, which blocks 10 rule-supported joins (6 identities split into 16 persons, all hidden as `review`). This is the conservative direction (missed merges, no exposure); fix in the next round.

Diff base: `HEAD` at audit start was 9d2cb02. During the audit the coordinator committed the people tables as 9f7557b (22:31); its `data/people/*.csv` are byte-identical to the audited working tree. "Touched today" below is the diff 9d2cb02 -> 9f7557b.

Privacy note for this file (D64): queue pairs are cited by input slot id (`<source_id>#<author_index>`) only, without names or person ids.

## Method

- Independent re-derivation: author slots, coauthor lists, slot ORCID (Crossref author at the same index, EO duplicate map), printed strings, crosswalk org ids, registry root and event keys, common family names, hub keys and ambiguous full-name keys were rebuilt from the raw inputs (EO `paper_authors` / `author_affiliations` / `people` / `papers` / `crossref.json`, PK `author_affiliations` / `papers`, OFC `ofc_full_metadata.json`, LIN `people.yaml` / `edges.yaml`, registry, crosswalk) with the auditor's own parser, not with `photonics_atlas.people`. Data-driven sets reproduce the DevLog numbers: 116 common family names, 28 hub keys, 1175 rule-2-withheld full-name keys; 10444 slots (EO 2298, PK 2334, OFC 5524, LIN 288), 532 OFC duplicate rows dropped.
- Committed persons were mapped back to slots through `obs_id` (and `lin_id` / unique `eo_person_id` xrefs for slots without observations).
- Identity: every multi-slot person was tested for D62 and for connectivity under an own D63 implementation (ORCID; exact full name + shared org on a non-common, non-ambiguous key; compatible name + shared org + D92/D96 coauthor support). Missed merges: every cross-person slot pair in a family block that the own D63 would join was checked against the local queue reason and D62. Divergences between the own (looser) name compatibility and D90/D95 were resolved by reading the rule text and, where needed, by an in-memory patched rebuild.
- Code-level D90 invariant: every record pair inside every person checked with `names_compatible`.
- Observations: all rows checked field by field against the raw row; a 90-row random sample read by eye.
- Determinism: `--dry-run`; real build into a scratch copy (current tables as base, and 9d2cb02 tables as base), byte comparison with the committed tables and the local queue.

## Sample sizes and counts

| Check | Sample | ok | wrong-merge | missed-merge | notes |
|---|---|---|---|---|---|
| 1a identity, population | 6900 persons with records, 1777 multi-slot | 1777 | 0 | see 1d | D62 violations 0 (two slots of one source 0, two EO persons 0, two ORCIDs 0, two LIN ids 0); 1 person not connected under the own rules was an artefact of the auditor's folding (sharp s), connected under D63 |
| 1b identity, stratified by xref basis | 66 persons (orcid 22, exact_name_shared_org 22, compatible_name_shared_org_coauthor 22) | 66 | 0 | 0 | every joined slot read against its input rows |
| 1c identity, stratified by merge edge | 75 accepted edges (25 per basis, distinct persons) | 75 | 0 | 0 | own D63 confirms each edge's basis |
| 1d common family names | 20 multi-slot persons | 20 | 0 | 0 | all joins rule (3) with >= 1 non-hub shared coauthor, or ORCID |
| 1e touched today | 378 persons (264 new ids, 114 changed) | 378 | 0 | 0 in the touched set beyond F1 | 9 observations changed person: each traced (below) |
| 1f D90 invariant (code) | all persons | all | 0 | - | 0 name-incompatible record pairs inside a person; 0 persons without a shared family name |
| 1g missed merges, population | 35 cross-person slot pairs / 32 person pairs joinable by the own rules | - | - | 6 identities (F1) + 1 low (F2) | 23 queued or D62-blocked: 15 are the F1 blocks, 8 hold (5 D90 ambiguity, 1 EO split, 1 same source, 1 compatible name without coauthor); 9 not queued: 8 hold under D90 syllable-boundary / D95 tail and initials rules (own parser looser), 1 is F2 |
| 2 observations | all 10832 rows (12 fields each) + 90-row read | 10832 | - | - | 0 mismatches: printed_name, printed_org, unit, country, aff_role, locator, kind, grade, active_on, source (canonical), org_id vs crosswalk, visibility per D64/D94; person visibility 0 mismatches over 6922 rows |
| 3 privacy | 4 tables, git index and history, app view | pass | - | - | see below |
| 4 determinism | 2 rebuilds | pass | - | - | byte-identical |
| 5 validator / tests | - | pass | - | - | 0 errors, 18 warnings; 32 passed |

Weak rule (2) joins (inside the rules, for manual review): 911 persons have rule-2 joins; 87 have no shared coauthor on any of them, 181 on at least one (round 2: 91 / 187). 15 of the 87 read by eye: same org, distinctive full names, plausible.

### Touched today: the 9 observations whose person changed (9d2cb02 -> 9f7557b)

| obs_id | cause | rule check |
|---|---|---|
| eo:chen2022#a8.1, ofc2026:Tu3E.3#a7.1 | family name became common (>= 10 slots, >= 3 full-name keys) with the new PK slots; rule (2) withheld; no shared coauthor | correct per D91/D96; see open question Q1 |
| ofc2026:M3Z.5#a2.1 | full-name key became ambiguous (D96 b); no shared coauthor with the other records | correct |
| pk:ectc51909.2023.00298#a3.1 | common family; only shared coauthor is a hub | correct (D96 c) |
| pk:vlsitechnologyandcir65830.2026.11577576#a2.1 | family name became common; no shared coauthor | correct |
| pk:ectc51906.2022.00180#a4.1, #a4.2 | non-common family; one shared coauthor, a hub (D92 needs one non-hub or two shared) | correct |
| pk:ectc51846.2026.00074#a8.1 | merged into the person holding the same name with a middle initial (shared org + non-hub coauthor, rule 3) | correct; old committed id kept without records (D65) |
| pk:ectc51846.2026.00016#a1.1 | merged into a LIN person through a new PK slot (rule 2 + rule 3 chain) | correct; old committed id kept without records (D65) |

Other diffs vs 9d2cb02: +409 PK observations (388 public, 21 review, 0 unmapped), 29 observation visibility changes, 14 person visibility changes; 0 observations removed; 0 committed ids missing or renamed; 264 new ids.

## Privacy (check 3)

- `git check-ignore -v`: `data/_local/` ignored (.gitignore:26) for `review_queue.csv`, `transitions.csv`, `name_only_candidates.csv`, `funnel.json`. `git ls-files data/_local`: empty; `git log --all -- data/_local`: no commit ever touched it.
- No name-only identity in committed tables: every multi-slot person is connected by ORCID or name + org (+ coauthor) edges (1a); xref bases are only origin / orcid / the two rule bases; no queue pair or transition is written to `data/people/` (the committed tables carry only the `visibility = review` effect of the queue, by design).
- E-mail / phone: validator patterns clean; the 6 `@` hits are org or unit names (`nano@stanford`, `Center for Nanotechnology Innovation @NEST`), not addresses. Columns hold names, printed affiliation strings, country, dates, ORCID iDs (public professional identifier) and source locators only.
- Institutional postal addresses: 10 OFC `printed_org` strings print an institution's street address or post code (presentations Th3B.2, 8 rows; Th2A.35, 2 rows). Institutional, not personal; verbatim per the D70 ruling. Informational.
- Outside `data/people/` (not in scope, checked because it reads these tables): `app/static/data/people.json` (untracked, written by `scripts/build_views.py`, D192) holds 6245 persons and 9710 observations, exactly the public rows; 0 review persons.

## Determinism (check 4)

- `uv run python scripts/build_people.py --dry-run`: people 6922, people_new 0, people_refreshed {}, kept without records 2, observations 10832 (public 9710 / review 1122), queue 485 pairs / 714 persons, merges orcid 120 / exact_name_shared_org 1762 / compatible_name_shared_org_coauthor 1642; all equal to the DevLog-004 22:26 entry. The dry run prints counts, not a diff, so the next item is the actual no-change proof.
- Real build into a scratch copy with the current tables as id base: `people.csv`, `person_aliases.csv`, `person_xref.csv`, `affiliation_observations.csv` and the local `review_queue.csv` byte-identical to the committed / local files.
- Real build into a scratch copy with the 9d2cb02 tables as id base (D210 procedure): the four tables byte-identical to the committed ones.

## Validator and tests (check 5)

- `uv run python scripts/validate_db.py`: errors 0, warnings 18 (14 registry `acquired without an org event`, 1 `IMT` redundant alias key, 1 source year vs published_on, 2 persons kept without records: the two committed ids of the 9 reassigned observations above).
- `uv run pytest -q tests/test_people.py`: 32 passed.

## Findings (non-ok)

| # | Severity | Finding | Evidence | Proposed fix |
|---|---|---|---|---|
| F1 | medium (missed merges, recall; no exposure) | D95 one-syllable rule misfires on unhyphenated or camel-case spellings of two-syllable given names. `Name.mono` is "one given token", not one syllable, so for common family names `compatible()` rejects a joined spelling against its own hyphenated spelling (fictitious: "Qaitun Ozz" !~ "Qai-Tun Ozz"), although the two have the same exact key and the D90 docstring itself states "Qaitun" ~ "Qai-Tun". `evaluate()` still treats the pair as exact (rule pair), then `ambiguous_slots` / `name_conflict` block every rule merge of the records that touch the joined spelling. 10 exact-key variant pairs in the data are rejected this way; 6 identities with rule-3 support (shared org, 1-3 shared non-hub coauthors) are split into 16 persons, all `review` with their 16 observations hidden. Includes 3 identically spelled slots with 3 shared non-hub coauthors at one org split into 3 persons only because a fourth record prints the name without the hyphen. 13 of the 16 persons existed at 9d2cb02 (pre-existing since round 2); 3 are new today | slot pairs (shared roots / non-hub shared coauthors): pk:ectc51687.2025.00085#1 ~ pk:ectc51687.2025.00131#5 (1 org / 3), ~ pk:ectc51846.2026.00092#7 (1 / 3), ~ pk:ectc51846.2026.00274#5 (1 / 3); pk:ectc51687.2025.00007#1 ~ pk:ectc51909.2023.00179#11 (1 / 1); pk:ectc51687.2025.00090#1 ~ pk:eptc62800.2024.10909872#2 (1 / 3); pk:ectc51687.2025.00090#4 ~ pk:eptc62800.2024.10909872#3 (1 / 3); pk:ectc32696.2021.00174#2 ~ pk:ectc51529.2024.00011#4 (1 / 2), ~ pk:iwlpc52010.2020.9375887#2 (1 / 1); pk:001c.129764#9 ~ pk:ectc51529.2024.00094#5 (1 / 4); pk:001c.129733#9 ~ pk:ectc51529.2024.00094#5 (1 / 2). Queue reasons on the person pairs among the 16: blocked_name_ambiguous 12, blocked_name_conflict 3 (the other 5 blocked_name_ambiguous pairs in the queue are correct D90 blocks) | In `compatible()`, return True before the D95 checks when both names are non-abbreviated with the same family and the same joined given key (`a.given == b.given`); equivalently apply the mono rule only when the other side's initials are not backed by the same letters. Regression test with fictitious names under a common family ("Qaitun Ozz" ~ "Qai-Tun Ozz"; "Qing Ozz" !~ "Q. T. Ozz" must still hold). Measured with an in-memory patch: clusters 6920 -> 6910, rule-3 merges 1642 -> 1652, blocked slot pairs name_ambiguous 18 -> 6 and name_conflict 3 -> 0, no other cluster changes. The 16 ids are committed (9f7557b), so up to 10 become rows without records (D65); implement the planned `people.same_as` redirect with the fix |
| F2 | low (spec question) | D95 also rejects a one-syllable full given name against the same full given name plus middle initials under a common family name (fictitious "Qoz Ozz" !~ "Qoz Q. T. Ozz"), though the leading full names agree and D90 allows a missing middle initial; D95's example ("Qoz" !~ "Q. T.") concerns initials only. 1 identity in the data (2 persons; shared org, 1 non-hub shared coauthor); not queued, because `evaluate()` sees no compatible name | pk:ectc51529.2024.00144#10 ~ pk:ectc51906.2022.00176#2 | Coordinator ruling: if D95 is meant for initials-only partners, skip the mono rule when both sides have the same leading full given name (measured: +1 rule-3 merge, no other change) |

## Open questions

- Q1 (recall vs rule): rule (2) is withheld for every common family name, also for long distinctive full names. Today one person with a four-token full name was split into 3 persons (5 observations, all now `review`) because the family name crossed the common threshold with new PK slots (slot ids eo:chen2022#8, ofc2026:Tu3E.3#7 vs the person's other OFC slots; no shared coauthor). Correct per D91/D96. Option: allow rule (2) on a common family name when the full-name key has >= 3 given tokens and is not ambiguous (D96 b); owner decision, not proposed as a fix.
- Q2: 20 EO slots without affiliation rows belong to EO persons that are split into several registry persons; the committed tables do not record which registry person holds them (no observation; the `eo_person_id` xref sits on every split part). No display effect. Record the slot in an xref or a local note if the split review needs it.
- Q3: committed ids without records are now 2 (and up to 12 after F1); the `people.same_as` redirect (D65 round-2 amendment) is still planned only.
- Q4: 87 persons rest on rule (2) joins without any shared coauthor (inside the rules); keep in the manual review queue as planned.
