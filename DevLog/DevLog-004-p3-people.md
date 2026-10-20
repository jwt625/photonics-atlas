---
title: P3 People foundation - person registry, xref, affiliation observations, review queue, transitions
date: 2026-10-20
status: foundation built 2026-10-20; audit corrections round 1 (D90-D94) and round 2 (D95-D97) applied 2026-10-20; third audit pending
scope: DevLog-000 phase P3, first two items (person registry; observation build + transition derivation + validator)
authors: Claude (at Wentao Jiang's request)
---

# DevLog-004: P3 People foundation

Plan source: [DevLog-000](DevLog-000-plan.md) P3 (U3, D8-D12), [DevLog-001](DevLog-001-p0-foundation.md) (registry,
crosswalk, D13-D29), [people assessment](research/2026-10-20-people-atlas-assessment.md) (A.2 core model, A.3
observation rules, C.1 method, C.2 funnel, E.2-E.4 identifiers / grading / privacy), lineage `schema.yaml` v0.2.0 and
`source_policy.md`. This tranche adds decisions D61-D70.

Binding people-data rules (owner, 2026-10-20): public professional sources only; default public view = grade A/B; a
publication affiliation is a dated `active_on` observation, never an employment interval; name-only identity matches
stay in a local review queue (`data/_local/people/`, git-ignored), never displayed or committed; never merge two people
on romanized name alone, common family names need two discriminators; no LinkedIn in this tranche; OFC author rows grade B,
paper-printed affiliations grade A; e-mail addresses stripped from stored text; no network.

## Inputs (read-only)

| Input | Rows | Used for |
|---|---|---|
| LIN `canonical/people.yaml`, `edges.yaml` | 288 people, 523 person-org edges | person rows (ids verbatim), aliases, orgs known per person (identity support only; edges are not imported as observations here) |
| EO `people.csv`, `paper_authors.csv`, `author_affiliations.csv`, `papers.csv`, `references/*/crossref.json` | 1509 people, 2298 author slots, 2880 affiliation rows | slots, slot-level ORCID (EO rule), observations |
| PK `author_affiliations.csv`, `papers.csv` | 1932 author slots, 1996 affiliation rows | slots, observations |
| OFC `ofc_full_metadata.json` `authors_json` (adapter, e-mails stripped) | 830 presentations, 6056 author rows | slots, observations (minus the 54 presentations already in EO) |
| registry `organizations.csv`, `org_events.csv`, participants, `sources.csv`; `data/crosswalk/org_crosswalk.csv` | | org ids, parent roots, continuations, source ids and `same_as` |

## Data decisions (D61-D70)

| # | Decision | Rationale |
|---|---|---|
| D61 | Committed tables in `data/people/`: `people.csv`, `person_aliases.csv`, `person_xref.csv`, `affiliation_observations.csv`; schema `data/schema/people.schema.yaml` (column types as the registry schema; new pattern/enum names prefixed `people_`). Local-only (`data/_local/people/`): `review_queue.csv`, `transitions.csv`, `name_only_candidates.csv`, `funnel.json`. Observations carry one column beyond the A.2 list, `printed_name` (author name as printed), because identity review needs it | traceability; D10 |
| D62 | Identity unit = one author slot (EO `paper_authors` row, PK paper x author_index, OFC `authors_json` element) or one LIN person. EO person groups are re-checked slot by slot under D63 (EO joins on exact name alone are not inherited); EO and LIN splits are respected: slots of two different EO persons, two LIN persons, two different ORCIDs, or two slots of one paper are never joined | owner rule: never merge on name alone; EO DevLog-020 #2 joins exact names of non-common family names without other evidence |
| D63 | Merge rules, applied in this order: (1) same ORCID on EO slots (slot ORCID = the EO person's ORCID when the paper's Crossref author record at that position carries one, EO rule); (2) exact full name (same folded given tokens and family token; first given token not an initial; LIN names and romanized LIN aliases count) + shared org, only for non-common family names; (3) compatible name (exact, or initials vs full given names) + shared org + shared coauthor; rule (3) is the only rule for common family names and for initial-abbreviated names. Shared org = the two slots' identity org keys intersect: registry root org (parent chain collapsed), plus one key per org event the root takes part in, so a predecessor and its successor (rename, merger, acquisition, spin-off) count as shared; direct event links only, no transitive chains (a closure joined 9 optical-component companies through New Focus / Bookham / Oclaro / JDSU deals). LIN: roots of the person's edge targets and current org. Shared coauthor = a coauthor key on both papers other than the two slots themselves (key = first initial + family name; full folded name when the family name is common). Common family names = the EO list (`build_people.py` COMMON, 68 names) plus every family name with >= 8 distinct full-name keys across all inputs (92 in total on 2026-10-20). Names are folded (accents, case), parenthesized nicknames dropped, hyphenated family names joined. Rule (3) rows carry basis `compatible_name_shared_org_coauthor` also when the names are exact | E.2; LIN Chinese-name rule; two discriminators for common names |
| D64 | Review queue (local only): pairs of final persons that share an exact full-name key, or compatible names plus a shared org, without meeting D63, plus joins blocked by D62; reason and discriminator flags per pair. Every observation of a person in the queue has `visibility = review`; the validator checks this whenever the local queue exists | owner rule: name-only matches never displayed or committed |
| D65 | `person_id`: LIN ids verbatim; otherwise `person_<slug of display name>`, collisions `_2`, `_3` in deterministic order; never reassigned. Rebuilds reuse existing ids through `obs_id -> person_id` and `eo_person_id` / `lin_id` xrefs; existing `people.csv` rows are kept verbatim (curated), new persons are appended. `display_name` = LIN name, else the most complete printed form (most non-initial tokens, then a cased form over an all-lowercase one, then frequency, then length; EO rule); an all-lowercase printed name is kept as printed when no other form exists (106 persons). ORCID is a field and an xref, never the key | D8, E.2 |
| D66 | `person_xref.basis` = the four listed bases plus `origin` (the record the person was seeded from: identity by construction, no match involved). Grades: `origin` A for eo/pk records, B for OFC names, LIN = best grade of the person's LIN sources (4 LIN people rest only on grade-C startup-database sources and get C; no LIN person source is LinkedIn); `orcid` A; rule-based merges X (inference, LIN grade policy; the observations keep their own A/B grades); `manual` needs `reviewed_on` and is preserved across rebuilds. Values: `eo_person_id` = EO person_id, `lin_id`, `orcid`, `pk_name_key` = folded name key, `ofc_name` = printed OFC name | a seeded record needs a basis; grade honesty |
| D67 | Observations: one per EO/PK affiliation row and per OFC `authors_json` element; `obs_id = <source_id>#a<author_index>.<aff_order>` (`.k` suffix per org for joint_printed strings mapping to several orgs). `printed_org` = the input's org string (EO/PK `org_name`, OFC affiliation text); `org_id` from the crosswalk (empty when unmapped); `unit`, `country` copied from EO/PK. OFC rows of presentations whose `ofc2026:` source has `same_as` an `eo:` row are dropped (counted once, EO row canonical). `active_on`: EO `published_on`, else the OFC session date when the EO paper is an OFC 2026 paper, else the year; PK year; OFC session date. Grades: publication A (EO Crossref-sourced rows stay A, their locator names Crossref), conference B. Locators: EO/PK locator as recorded; OFC `program metadata authors_json #<index>` | A.3, D23, D24 |
| D68 | Transitions (`derive_transitions.py`, local only) per C.1 on registry persons: org group = registry root org; A -> B when hi(last A) < lo(first B) and no source lists both; gap >= 90 days when both dates have day precision, else a later calendar year; overlapping groups = co-affiliation (counted, no arrow). An org event whose participants' roots are A and B, dated on or before the first B observation (or undated), makes the pair `acquisition_continuation` (no person transition). `present_address` rows give `explicit_move_statement` (grade A, direction confirmed); the rest `publication_sequence`, `direction_status = confirmed`, `directness = unknown`, grade X. Classes: uni = registry org_type university / academic_lab, unk = unknown, ind = every other type | C.1; LIN invariant "acquisition ownership alone never creates a person transition" |
| D69 | Name-only candidates (local only, for the funnel comparison): persons joined through review-queue exact-name pairs are grouped, and transitions that need such a link are written to `name_only_candidates.csv` with identity `name_only`; never committed, never shown | C.2 counted name-only identities; D10 |
| D70 | Visibility: `public` only for grade A/B observations of persons not in the review queue; everything else `review`. LIN career edges stay LIN claims in this tranche (not observations); LinkedIn not used; no network | D12, E.3, E.4 |

### Decision amendments (2026-10-20, fresh-context audit)

- D63 (2026-10-20): name comparison replaced by D90; common family names extended by D91; shared coauthor discounted by D92. The EO list is 68 names (the code comment said 58; corrected).
- D64 (2026-10-20): the queue also holds every pair of registry persons that one EO person was split into (reason `eo_person_split`, any evidence), pairs of different EO persons with compatible full given names (`eo_split_compatible_name`), and rule merges blocked by D90 (`blocked_name_ambiguous`, `blocked_name_conflict`).
- D65 (2026-10-20): id reuse weights an old id's ORCID above observation counts (a split keeps the id on the ORCID-backed part), and an id spelled like the cluster's display name wins ties. Kept `people.csv` rows refresh only derived fields: `visibility`, `orcid` (from the person's records), `display_name` when no record of the person prints it any more (split), and a disambiguator copied from LIN (D93). Old ids whose records all moved into another person (new merges) stay as rows without records (validator warning).
- D66 (2026-10-20): on `scheme = orcid` rows, basis `orcid` means "ORCID field as recorded" (EO Crossref author record), not a join; on other schemes it is the join basis (I6). `lin_id` rows carry `notes = lin sources: <source_id>;...`, the grade is checked against those sources. Slot ORCID (rule 1) is set only when the Crossref iD at that author position equals the EO person's iD after EO's duplicate map (I3; 0 slots differ on 2026-10-20).
- D69 (2026-10-20): name-joined components use every queue pair with the `exact_name` flag (any reason), so the new queue reasons do not change the D69 set.
- D70 (2026-10-20): person-level visibility added (D94).

Round 2 amendments (2026-10-20, fresh-context audit 2; coordinator rulings marked):

- D64 (ruling): a queue pair whose partner has 0 observations (a LIN-only record) stays queued but does not demote the other side's observations; a person's observations are review when it is in a pair whose partner has >= 1 observation (`people.demoted_by_queue`). With the queue present, the validator requires every pair of registry persons split from one EO person to be queued.
- D65 (2026-10-20): immutability of person ids starts at the first commit of `data/people/`. Before it, ids that no longer hold any record are retired (`build_people.py --retire-orphans`, pre-commit only; 4 retired in the final round-2 build against the 13:42 base). After the first commit an id is never deleted; a merged id will get a redirect (planned column `people.same_as`, not implemented). Id reuse order: the id's ORCID, then the id spelled like the cluster's display name, then observation counts (D96).
- D70 (ruling): `printed_org` / `unit` are verbatim paper text; a present-address row may print "present address" or move wording there. The move / status wording rule applies to curated notes-type cells only (D97).
- D91 (b), D92: replaced by D96.
- D94 (ruling): a queued LIN person with A/B sources keeps `visibility = public` (the LIN record is displayable); none of its queued observations is public (D64 ruling).

| # | Decision | Rationale |
|---|---|---|
| D95 | Name compatibility (D90) adds: a full given name printed after an initial ("J. Y. Ezra", fictitious) must be one of the other side's full given names when that side has any; for common family names a one-syllable full given name is not compatible with two or more initials ("Qoz" !~ "Q. T."). Common-family flags are passed into the cluster-level and ambiguity checks | audit 2 (2c, 2d): one-syllable / tail-name joins |
| D96 | (a) Slot-frequency common rule needs >= 10 slots AND >= 3 distinct full-name keys (`COMMON_SLOT_MIN_KEYS`): a prolific person's own family name is not "common" (common names 130 -> 112). (b) D91(b) re-derived: rule (2) is withheld only for full-name keys that are ambiguous in the data, i.e. the family name is region-dense (>= 50 % of its slots with a known country in CN, TW, HK, MO, JP, KR or SG, using the printed EO / PK site country and the registry org country only as fallback) AND the family name and the given names are each carried by >= 2 distinct full-name keys (`DENSE_FAM_KEYS`, `DENSE_GIVEN_KEYS`; 1111 keys). Distinctive full names keep rule (2). (c) Hub discount (D92) is not applied when one of the two slots is itself a hub; for common family names shared-coauthor support needs >= 1 non-hub coauthor (two hubs alone do not count). Variants measured (persons joined, pairs blocked only by (b)): no (b) 6646 / 0; dense + family keys >= 2 (given any) 6681 / 47 person pairs; chosen dense + family >= 2 + given >= 2 6658 / 14; given >= 3 6654 / 9; region-free family >= 2 + given >= 2 6673 / 31 but it blocks distinctive names in other regions | audit 2 (2e, 2f, 2g): round-1 D91(b) hid 117 persons / 158 observations on region alone; slot rule made one person's name common; hub discount split the hubs |
| D97 | Validator (round 2): spelled "at" with a real dot and the full-width at sign count as e-mail; phone numbers (tel / fax prefix, or + country code) rejected; status wording (currently, presently, transferred, hired, departed, present address) rejected in notes-type cells (`people.disambiguator`, `people.notes`, `person_aliases.notes`, `person_xref.notes`); one ORCID held by two persons is an error; with the queue present every split-EO pair must be queued; file paths derived from the validate root (`validate.py` passes `root` to the people rules) | audit 2 (4b, 4c) |

| # | Decision | Rationale |
|---|---|---|
| D90 | Names are parsed (`people.parse`): hyphenated given syllables kept for initials (fictitious examples: `Qai-Tun` -> q, t; key form stays joined), capital runs of 2-3 letters in a mixed-case name are initials (`QT` -> q, t), all-caps names are not re-read. Two names are compatible when the family names agree, the full initials sequences agree position by position (one may be a prefix: a missing middle initial), and the leading full given names agree as letters or end on a syllable boundary (`Hiro` !~ `Hirotaka`, `Qeng-Qi` !~ `Qeng-Qieh`). Rule (2)/(3) unions also need cluster-level compatibility: every record of one cluster name-compatible with every record of the other (else `blocked_name_conflict`); a record whose rule partners include two mutually incompatible records is not merged by name at all (`blocked_name_ambiguous`). Rule (3) pairs are applied strongest first (most shared non-hub coauthors). ORCID merges are exempt | I1/P6: name chaining through initials and joined syllables built 6 clusters with incompatible given names |
| D91 | Rule (2) (exact name + shared org) is not applied to (a) common family names: EO list + >= 8 distinct full-name keys (unchanged) + >= 10 EO/PK/OFC author slots (`COMMON_MIN_SLOTS`, new: 130 common names, was 92), and (b) region-dense family names: >= 50 % of the family's org-mapped slots at registry orgs in CN, TW, HK, MO, JP, KR or SG (`DENSE_SHARE`, 722 further names). Both are data-driven (no name list). Slot frequency alone cannot reach the audit-flagged persons: their family names have 1-9 slots, and a slot threshold <= 2 would abolish rule (2) (every merge needs 2 slots); (b) covers them. Coauthor keys use only (a) | I2: 172 exact name + org merges on family names outside the common set, 19 persons resting on name + org only |
| D92 | Shared-coauthor support (rule 3, review flags) = one shared non-hub coauthor, or >= 2 shared coauthors of any kind. Hub = coauthor key printed on >= 10 sources (`HUB_MIN_SOURCES`; 21 keys on 2026-10-20) | P6: one prolific senior coauthor links most authors of one org |
| D93 | `people.disambiguator` carries only curated non-career discriminators (field, native-script name). The LIN `name_disambiguator` (employer, role, founder, "former ..." wording, no source or grade in this table) is not copied; the 46 copied values were cleared. This repo has no LIN claims layer yet, so the wording is dropped here and stays in LIN with its sources | P4 |
| D94 | `people.visibility` (new column): `public` iff the person has >= 1 public observation or a LIN source of grade A/B, and is not a LIN person whose sources are all below B; such C-only LIN persons (4) are `review` and so are their observations (2) | P5 |

## TODO

- [x] 1. Read inputs and conventions; write this plan (before code).
- [x] 2. `data/schema/people.schema.yaml` (4 tables, `people_` enums/patterns).
- [x] 3. `src/photonics_atlas/people.py`: name folding/keys, slot loading (EO/PK/OFC/LIN), constrained union-find with logged bases, review-queue pairs, observations, id assignment.
- [x] 4. `scripts/build_people.py` (`--dry-run`, `--limit N` family blocks, `--only NAME`, RunLog log + JSONL, deterministic, curated rows kept).
- [x] 5. `src/photonics_atlas/rules_people.py`: fk/source/kind/grade/date/id/visibility/xref rules.
- [x] 6. Pilot (ORCID-backed person, LIN person, common family name, OFC-only author); fix; full run.
- [x] 7. `scripts/derive_transitions.py` -> `data/_local/people/`; funnel vs C.2 with explanations.
- [x] 8. `tests/test_people.py` (real data + mutation tests); ruff format, ruff check, mypy, pytest, validate_db.
- [x] 9. Progress, counts, open issues recorded here.
- [x] 10. Fresh-context audit 1 (coordinator) - corrections applied 2026-10-20, see Audit corrections.
- [ ] 11. Second fresh-context audit of the corrected build - coordinator.

## Progress

- 2026-10-20: inputs read (DevLog-000/001, assessment, LIN schema/policy, adapters, crosswalk, validator); plan written.
- 13:20: schema, `people.py`, `build_people.py`. The schema file was kept out of `data/schema/` until the first build so that parallel validator runs never saw missing built tables.
- 13:25 pilot (`--only`, report-only, log in `logs/`), four people, described without names (D64):
  - ORCID-backed EO person (4 EO slots, 1 with a Crossref ORCID): 3 slots joined (exact name + shared org; the ORCID slot among them); the 4th slot has no affiliation row in EO, so it is a separate person, queued as exact name + shared coauthor. EO had joined all 4 on exact name.
  - LIN Intel person: LIN record + 1 EO slot + 1 OFC slot joined (exact name + shared root org Intel); xref eo_person_id / ofc_name basis exact_name_shared_org, grade X.
  - Common family name (in the EO list), 21 slots in EO + OFC: 3 persons (EO university slots joined by org + coauthor; 18 OFC slots of one company joined by org + coauthor; 1 OFC slot without a mapped org alone); 3 queue pairs, none merged on name + org alone. A second common name with a LIN record stayed apart from 3 same-name persons (queue).
  - OFC-only author (Intel, one presentation): 1 person, seed only, public.
  - Fixes from the pilot: none to the rules; display name casing priority added later (106 all-lowercase printed names).
- 13:36 first full build; validator found 6 false e-mail hits (`nano@stanford`, `@NEST` are org/unit names): rule narrowed to the shared `EMAIL_RE`.
- 13:38 xref basis changed from "strongest join touching the slot" to the weakest join on the slot's chain from the person's anchor record (accepted joins form a spanning forest); org-event identity keys added (D63), first as a transitive closure, then direct links only. Own first-build outputs deleted and rebuilt from scratch (nothing had been published).
- 13:42 final build + derive. Rebuild over existing outputs is byte-identical (all 8 files), 0 new ids.
- 14:11 audit corrections started. Zip backup of `data/people/`, `data/_local/people/` and the owned code in the agent's private scratch folder. Dry run on the 14:08 crosswalk (registry merge) before any change: identical counts to 13:42 (crosswalk rebuild had no effect on people).
- 14:15-14:21 D90 parser, cluster-level and ambiguity checks; measured the six audit clusters (all split). Hub threshold chosen from the key distribution (keys on >= 10 sources: 26 before common-set change, 21 after). I2: the slot-frequency rule was measured first; the flagged persons' family names have 1-9 slots, so the region-dense share (D91 b) was added; variants compared (persons 6606-6717, review persons 604-798).
- 14:21 first corrected build; validator: 1 error (a kept row's ORCID field after a split) -> D65 amendment (ORCID refreshed; ORCID-weighted id reuse). D92 relaxed to "one non-hub or two shared coauthors" after a split of an ORCID-backed person through a single hub coauthor was seen. EO person splits always queued.
- 14:24 restored the 13:42 tables from the backup before the final build so that ids of intermediate builds (never published) are not kept as immutable ids; final build + derive.
- 14:28 rebuild over the corrected outputs byte-identical (8 files), 0 new ids; validator 0 errors.
- 14:50 audit 2 corrections started; zip backup of the 14:28 state (`data/people/`, `data/_local/people/`, owned code) in the private scratch folder.
- 14:52-14:56 D95 (tail / one-syllable rules), D96 (slot rule keys, hub exemption, common-name coauthor rule, ambiguous-key rule (b)); variants of (b) measured against the raw slots (table in D96).
- 14:56 restored the 13:42 tables (round-1 backup) as the id base; `build_people.py --retire-orphans` (4 retired); derive.
- 14:57 validator 0 errors, no people warnings; cited persons checked one by one against the rebuilt tables (ids only).
- 15:01 rebuild byte-identical (8 files), 0 new ids; pytest 94 passed.

## Results (2026-10-20 13:42, before the audit corrections; current numbers in Results after audit corrections)

| Table | Rows | Breakdown |
|---|---|---|
| `people.csv` | 6604 | LIN 288 (ids verbatim; validated 284, in_research 4); not_started 6316; ORCID 374 (= EO's 374 iDs). Corpus mix: OFC only 3347, PK only 1412, EO only 1322, LIN only 245, EO+OFC 198, OFC+PK 24, LIN+OFC 17, EO+LIN 11, EO+PK 10, EO+LIN+OFC 9, EO+OFC+PK 3, LIN+PK 3, LIN+OFC+PK 2, EO+LIN+OFC+PK 1 |
| `person_xref.csv` | 7357 | origin 6604 (ofc_name 3347, eo_person_id 1533, pk_name_key 1436, lin_id 288); orcid 374; exact_name_shared_org 195 (ofc 157, eo 21, pk 17); compatible_name_shared_org_coauthor 184 (ofc 113, pk 71). Grades A 3598, B 3376, X 379, C 4 |
| `person_aliases.csv` | 326 | abbreviated 143, printed_variant 77, LIN alternate_spelling 46, native_name 31, common_name 29 |
| `affiliation_observations.csv` | 10423 | publication/A 4876 (EO 2880 + PK 1996 input rows), conference/B 5547 (5524 OFC rows + 23 extra rows for joint_printed strings); public 9296, review 1127; primary 9741, additional 662, present_address 20; org unmapped 13 (12 skipped OFC strings + 1 empty affiliation) |
| local `review_queue.csv` | 390 pairs, 612 persons | name_only 168, exact name + shared org but common family name 94, exact name + shared coauthor without shared org 85, compatible name + shared org without coauthor 40, blocked same source 2, blocked EO split 1 |
| local `transitions.csv` | 36 | publication_sequence 13 (9 persons), acquisition_continuation 3, explicit_move_statement 20 (EO 18, PK 2 present-address rows) |
| local `name_only_candidates.csv` | 100 | name only 69, name + shared coauthor 31; 68 of them on common family names |

Merges (slot pairs joined): orcid 120, exact_name_shared_org 1900, compatible_name_shared_org_coauthor 1418. EO's 1509 persons map to 1554 registry persons: 44 EO persons are split into 89 registry persons (45 additional), because their EO joins are not supported by D63; every EO person_id is kept as an xref value. 532 OFC author rows of the 54 presentations already in EO were dropped (counted once).

## Funnel vs assessment C.2

| Step | C.2 (heuristic orgs, name-key identity) | P3 strict (registry persons) | P3 name-joined (review-queue exact-name links, local) |
|---|---|---|---|
| Person keys with observations | 6167 | 6323 persons | 247 components of 2+ persons |
| >= 2 org groups | 457 | 287 | 163 |
| Strictly ordered, never co-listed | 163 (137 persons) | 17 (12) | 148 (112) |
| After 90 d / later-year gap | 92 | 16 (11) | 100 (79) |
| of which org-event continuation | 17 | 3 | 0 |
| Candidate moves | 75 (62 persons) | 13 (9) | 100 (94 components) |
| Class | uni->ind 31, uni->uni 20, ind->ind 17, ind->uni 7 | uni->uni 6, uni->ind 6, ind->ind 1 | ind->ind 34, uni->ind 33, uni->uni 25, ind->uni 8 |
| Identity | orcid 22, coauthor 13, name only 40 | orcid 10, shared coauthor 1, name + org merge chain 2 (rests on grade-X exact name + shared org merges) | name + coauthor 31, name only 69 |
| Source pair | EO->EO 30, EO->OFC 26, PK->OFC 7, PK->PK 6, PK->EO 3, EO->PK 2, OFC->EO 1 | EO->EO 12, PK->PK 1 | EO->EO 38, EO->OFC 32, PK->PK 14, PK->OFC 7, OFC->EO 4, PK->EO 3, EO->PK 2 |

Units of the first row: C.2 counts 6167 person keys with observations (EO person ids + PK / OFC name keys, assessment C.2); P3 counts 6323 registry persons with >= 1 observation (13:42; 6424 after the audit corrections). OFC rows: C.2 states 5523 OFC rows; P3 keeps 5524 OFC author rows (6056 - 532), one of them with an empty affiliation (org_id empty); the difference of 1 is consistent with that row but was not checked against the C.2 script.

Strict + name-joined = 113 candidates vs 75. Not tuned; the differences come from:

1. Identity. C.2 kept EO's person groups (EO joins exact names of non-common family names on name alone) and attached PK / OFC rows to an EO person by a unique exact name, so a move between two orgs needed no discriminator. Here every join needs ORCID or a shared org (D63); two non-overlapping orgs can only be linked by ORCID, a shared coauthor plus org, or a bridging co-affiliation. So strict moves are few and mostly ORCID-backed, and the bulk sits in the local name-joined set, which is the C.2 identity notion plus common-name pairs.
2. ORCID 22 -> 10. C.2 counted a move as ORCID-backed when the EO person had an ORCID, even if one end was a name-attached PK/OFC row or an EO slot without the iD; here both slots must carry the Crossref iD.
3. Org grouping. Registry roots replace token heuristics and the small alias list: OFC spelling variants map through curated aliases (no alias-spelling artifacts), and units collapse into parents (D20: Celestial AI -> Marvell and Enosemi -> AMD are parents now, so those 5 people show one org group and no pair; C.2 counted them as continuations).
4. Continuations 17 -> 3. Resonac rename (2) and the Science Tokyo merger (1) are continuations. Xperi (PK "Xperi", 2022) -> Adeia (2023) has no sourced event link (DevLog-001 open item), so its 9 people appear as name-joined ind->ind candidates; they are an org event, not moves.
5. More name-joined candidates than C.2 name-only (69 + 31 vs 40): common family names are not excluded from the name-joined set (68 of 100 are common-name pairs = collision risk). A possible further contributor, not measured: the registry maps 99.79% of OFC author rows to orgs, while C.2's heuristic mapping rate was not recorded.
6. The gap rule is identical: same-week OFC pairs order by session day and are removed by the 90-day gap (C.2: 61 OFC->OFC pairs; here 1 strict, 48 name-joined pairs removed in total by the gap, all sources).

## Audit corrections (2026-10-20, fresh-context audit 1)

| Finding | What was done |
|---|---|
| I1 / P6 (high): name chaining, joined hyphenated syllables, capital runs read as given names, initials compared only up to the shorter tuple, no cluster-level check; 6 clusters with incompatible given names (2 public) | D90 parser and compatibility; cluster-level check before every rule union (`blocked_name_conflict`), ambiguous initials records not merged (`blocked_name_ambiguous`, 5 queue pairs); D92 hub discount; rule (3) strongest evidence first. All 6 clusters split (into 3, 2, 2, 2, 3 and 4 persons); the original ids stay on the part holding most of their observations (ties: the id spelled like the display name). Regression tests with fictitious names (`test_given_name_compatibility`, `test_no_name_chaining_and_ambiguous_initials`, `test_hub_coauthor_is_not_enough`) |
| I2: exact name + shared org merges on family names outside the common set; 19 persons on name + org only | D91 (data-driven, no name list): slot-frequency threshold 10 plus region-dense share 0.5. Rule (2) edges 1900 -> 1136; persons whose rule (2) joins have no coauthor support: 98 -> 68 (all on non-common, non-dense family names; 0 on dense ones). One person the audit listed remains among the 68: no data-driven criterion separates it; left for manual review. Superseded by round 2 (D96) |
| P4: committed disambiguator carried LIN career claims without source or grade | D93: not copied, 46 values cleared; validator rejects role / move wording in `people.disambiguator` and `notes` |
| C2 / P7: validator gaps | `rules_people.py`: LinkedIn and move wording over all cells of the 4 tables; spelled-out e-mail pattern (`x at y dot edu`, also stripped at build); unknown files in `data/people/` rejected; absent local queue warns; scheme orcid must be grade A; lin_id grade = best grade of the LIN sources listed in its notes (C-only graded A fails); org_id must agree with the crosswalk for (corpus, printed string); active_on must equal EO published_on (else the OFC session date for OFC 2026 papers, else the year), the OFC session date, or the PK year; printed_name must be the person's display name or alias; `validated` only for LIN people. Mutation tests for each |
| P5: person-level visibility | D94 `people.visibility`; the 4 C-only LIN persons and their 2 observations are review; validator + `test_person_visibility_and_c_only_lin` |
| Low: EO-split pairs not always queued | every split EO person queued (`eo_person_split`, 56 pairs; the cited ORCID-backed pair is now in the queue) |
| Low: I6 basis semantics | documented (D66 amendment, schema desc) |
| Low: people.py comment 58 vs 68 | fixed (68) |
| Low: real researcher names in tests and the build_people docstring | replaced with fictitious names |
| Low: I3 Crossref ORCID not compared with the EO iD | compared after EO's duplicate map (copied constant, test checks it against the EO script); 0 slots differ |
| Low: DevLog wording (I5, F2, OFC rows, org chain) | fixed above (44 EO persons split; 6323 vs 6167 units; 5524 vs 5523; "name + org merge chain") |
| C3: rules_people import failure and empty people.csv returned silently | `validate.py` hook: an import failure of `rules_people` is an error (other tranche modules unchanged); empty or missing people tables are an error; tests for both |

## Results after audit corrections (2026-10-20 14:28)

| Item | Before (13:42) | After (14:28) |
|---|---|---|
| `people.csv` rows | 6604 | 6716 (112 new ids from splits; 6 old ids kept without records after new merges, D65) |
| persons with observations | 6323 | 6424 |
| person visibility (new) | - | public 5927, review 789 |
| merges orcid / exact_name_shared_org / compatible_name_shared_org_coauthor | 120 / 1900 / 1418 | 120 / 1136 / 2076 |
| common family names | 92 | 130 (+ 722 region-dense for rule 2) |
| `person_xref.csv` | 7357 (A 3598, B 3376, X 379, C 4) | 7442 (A 3633, B 3447, X 358, C 4) |
| `person_aliases.csv` | 326 | 321 |
| observations public / review | 9296 / 1127 | 8983 / 1440 (10423 rows, unchanged) |
| local review queue pairs / persons | 390 / 612 | 526 / 791 (exact name + shared org but common or region-dense family 198, name_only 174, eo_person_split 56, exact name + shared coauthor without shared org 51, compatible name + shared org without coauthor 40, blocked_name_ambiguous 5, blocked_eo_split 1, eo_split_compatible_name 1) |
| EO persons split | 44 (into 89) | 52 (into 106) |
| disambiguators | 46 (LIN copies) | 0 |
| local transitions | 36 (publication_sequence 13, continuation 3, explicit 20) | 32 (publication_sequence 12, continuation 0, explicit 20) |
| local name-only candidates | 100 (name only 69, + coauthor 31) | 100 (name only 72, + coauthor 28; 70 on common family names) |

Funnel after the corrections (columns as above): strict - persons with observations 6424, >= 2 org groups 286, strictly ordered 13 (9 persons), after gap 12 (8), continuation 0, candidate moves 12 (8 persons; uni->uni 6, uni->ind 6; orcid 10, shared coauthor 1, name + org merge chain 1; EO->EO 12). Name-joined - 323 components, >= 2 org groups 171, strictly ordered 151 (114), after gap 103 (81), continuation 3, candidate moves 100 (94 components; ind->ind 34, uni->ind 33, uni->uni 25, ind->uni 8; name + coauthor 28, name only 72; EO->EO 38, EO->OFC 32, PK->PK 14, PK->OFC 7, OFC->EO 4, PK->EO 3, EO->PK 2). The 3 continuations (Resonac rename, Science Tokyo merger) moved from strict to name-joined: their persons' rule (2) joins fall on region-dense family names now.

## Audit corrections round 2 (2026-10-20, fresh-context audit 2)

| Finding | What was done |
|---|---|
| 2e: D91(b) over-blocked (72 exact name + shared org queue pairs blocked only by it; 117 persons / 158 observations hidden), share used the registry root country | D96(b): printed site country first, registry country as fallback; rule (2) withheld only for ambiguous full-name keys (family and given names each carried by >= 2 full names in the data). Pairs blocked only by (b): 72 -> 11; persons hidden only by (b): 117 -> 19; their observations 158 -> 29. The four persons cited by the audit are public with all observations |
| 2f: slot threshold made one prolific person's family name common | D96(a): >= 10 slots AND >= 3 distinct full-name keys; the cited OFC person is one person with 10 public observations |
| 2g: hub discount split the hubs; 7 merges rested on 2 hubs only | D96(c): no discount when a slot is a hub; common families need >= 1 non-hub coauthor. Of the 7 cited hub persons, 3 are now one person each; 4 stay split by rule: the extra slots have no mapped org or a different org (3 persons) or share only one hub coauthor under a common family name (1 person). Two shared hubs no longer support a common-family merge unless one of the two slots is itself a hub (D96 c); the 3 cited 2-hub merges were not re-checked one by one |
| 2c, 2d: tail given name and one-syllable vs two-initial joins | D95; the cited persons are now separate |
| 3a, 3b: ids and orphans | D65 amendment: ORCID > spelling > observations; `--retire-orphans` before the first commit (4 retired); `people.same_as` redirect planned for after the first commit. The cited initials / full-name id pairs now hold the matching spellings |
| 2h, 1f: coordinator rulings | D64 / D70 / D94 amendments; `people.demoted_by_queue`; tests `test_local_review_queue_hides_its_people`, `test_queue_rulings_and_eo_split` |
| 4b, 4c: validator | D97 rules; mutation tests `test_phone_spelled_email_and_status_words`, `test_orcid_held_by_two_persons`, `test_queue_rulings_and_eo_split`, `test_copy_with_queue_is_clean`; `validate.py` passes the root to the people rules |
| Low: real name in a test, cluster given names in code comments, DevLog wording | fictitious forms; DevLog wording without region or origin labels for names |

Weak rule (2) merges after round 2 (exact name + shared org without coauthor support): 870 persons have rule (2) joins; 91 have all of them unsupported, 187 at least one (round 1: 68 and 136). The increase is the price of releasing the over-blocked distinctive names (2e) and of the stricter common-name coauthor rule moving merges out of rule (3) (2g); left for the third audit and manual review.

## Results after audit corrections round 2 (2026-10-20 15:01)

| Item | Round 1 (14:28) | Round 2 (15:01) |
|---|---|---|
| `people.csv` rows | 6716 (6 kept without records) | 6658 (0 kept without records; 4 retired pre-commit) |
| persons with observations | 6424 | 6377 |
| person visibility | public 5927, review 789 | public 6013, review 645 |
| merges orcid / exact_name_shared_org / compatible_name_shared_org_coauthor | 120 / 1136 / 2076 | 120 / 1680 / 1584 |
| common family names / rule-2-withheld keys / hub keys | 130 / 722 dense families / 21 | 112 / 1111 ambiguous full-name keys / 26 |
| `person_xref.csv` | 7442 | 7400 (A 3625, B 3403, X 368, C 4) |
| `person_aliases.csv` | 321 | 316 |
| observations public / review | 8983 / 1440 | 9343 / 1080 |
| local review queue pairs / persons | 526 / 791 | 459 / 684, of which 648 demoted (name_only 167, exact name + shared org with common family or ambiguous name 130, eo_person_split 58, exact name + shared coauthor without shared org 51, compatible name + shared org without coauthor 38, blocked_name_ambiguous 11, blocked_name_conflict 3, blocked_eo_split 1) |
| EO persons split | 52 (into 106) | 49 (into 102) |
| local transitions | 32 | 36 (publication_sequence 13 for 9 persons, acquisition_continuation 3, explicit 20) |
| local name-only candidates | 100 | 99 (name only 71, + coauthor 28; 70 on common family names) |

Funnel (strict) after round 2: persons with observations 6377, >= 2 org groups 288, strictly ordered 17 (12 persons), after gap 16 (11), continuation 3 (Resonac rename 2, Science Tokyo merger 1), candidate moves 13 (9 persons; uni->uni 6, uni->ind 6, ind->ind 1; orcid 10, shared coauthor 1, name + org merge chain 2; EO->EO 12, PK->PK 1). Name-joined: 271 components, >= 2 org groups 165, strictly ordered 147 (111), after gap 99 (78), candidate moves 99 (93 components; ind->ind 33, uni->ind 33, uni->uni 25, ind->uni 8; name only 71, name + coauthor 28).

## Verification (2026-10-20 13:45)

- `uv run python scripts/validate_db.py --quiet`: 0 errors, 15 warnings (all pre-existing P0 warnings; none from the people tables).
- `uv run pytest -q`: 66 passed (13 in `tests/test_people.py`: synthetic merge rules, name folding, real-table invariants, review-queue visibility, in-memory rebuild = committed ids, 8 mutation tests).
- `uv run ruff format --check .`, `uv run ruff check .`: clean. `uv run mypy`: clean for this tranche's files; 2 errors in `scripts/scan_component_candidates.py` (another tranche's file, in progress).

## Verification (2026-10-20 14:30, after audit corrections)

- `uv run python scripts/build_people.py --dry-run`, then the real run; `uv run python scripts/derive_transitions.py`; rebuild byte-identical.
- `uv run python scripts/validate_db.py --quiet`: 0 errors, 21 warnings (15 registry / sources warnings of other tranches; 6 people warnings: old ids kept without records after new merges, D65).
- `uv run pytest -q`: 84 passed, 1 failed (`tests/test_validate.py::test_name_basis_vs_origin`, registry test, not a people file; reported to the coordinator). `tests/test_people.py`: 25 passed.
- `uv run ruff check`, `uv run ruff format --check`, `uv run mypy` on the owned files and `validate.py`: clean.

## Verification (2026-10-20 15:01, after round 2)

- `uv run python scripts/build_people.py --dry-run`; real run with `--retire-orphans` on the 13:42 base; `uv run python scripts/derive_transitions.py`; second rebuild byte-identical.
- `uv run python scripts/validate_db.py --quiet`: 0 errors, 15 warnings (none from the people tables).
- `uv run pytest -q`: 94 passed (`tests/test_people.py` 32).
- `uv run ruff check`, `uv run ruff format --check`, `uv run mypy` on the owned files and `validate.py`: clean.

## Incidents

- 13:42 `uv run ruff format .` (whole repo) reformatted two files of the component tranche, `scripts/scan_component_candidates.py` and `scripts/merge_component_staging.py` (layout only, no code change). Afterwards only this tranche's files were formatted.

## Open issues

- Strict identity cannot link a clean move between two orgs without ORCID or coauthor + org; the useful move signal (100 name-joined candidates) stays local until reviewed. Next: manual review of the queue (basis `manual`, `reviewed_on`), starting with the 31 name + shared-coauthor candidates, and OFC header extraction (T4) for co-affiliations.
- Registry gaps seen through people data (not edited here): PK `org_xperi` has no event link to Xperi Holding / Adeia (9 people); `org_ntt_innovative_devices` has no parent link to `org_ntt` (3 name-joined candidates), and no source in this repo states one.
- EO slots without affiliation rows (36) cannot share an org and stay separate persons unless ORCID links them.
- Manual xref rows are preserved but not yet used as forced joins or splits; implement when the first review decisions exist.
- (2026-10-20, audit 1) 6 old ids (initial-only and capital-run forms) are kept without records after D90 merged their records into other persons; they are review rows. Decide at review whether merged ids get a `same_as`-style redirect.
- (2026-10-20, audit 1) D90 prefix rule: a fully spelled one-syllable given name is compatible with two initials ("Qoz" ~ "Q. T.", fictitious), as a missing middle initial is; rule (3) evidence is still required. Resolved in round 2 (D95: incompatible for common family names).
- (2026-10-20, audit 1) 68 persons still rest on exact name + shared org without coauthor support (non-common, non-region-dense family names); review sample in the second audit. Round 2: see D96 counts.
- (2026-10-20, audit 1) `blocked_name_conflict` produced 0 queue pairs on this data: the ambiguity rule removes the chaining records first; the check stays as a guard (tested).
- Persons kept without records after an input change are retained (immutable ids) with a validator warning; none on 2026-10-20.
- LIN career edges (556) are not imported as observations; they remain LIN claims for the career-claims layer.
