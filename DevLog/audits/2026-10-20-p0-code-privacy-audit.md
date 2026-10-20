---
title: Fresh-context audit of P0 - validator, scripts, adapters, privacy, app, docs
date: 2026-10-20
scope: DevLog-001 (P0) code and documents
mode: read-only subagent; report transcribed by the coordinator (subagents cannot write report files)
---

# P0 code / privacy / conventions audit (2026-10-20)

Baseline reproduced: validate 0 errors / 1 warning; pytest 19 passed; ruff, ruff format, mypy strict clean; pnpm check 0 errors, pnpm test 2 passed; 864 orgs (428 ROR, 722 country), 370 aliases, 55 events (A 53, B 2), 1834 sources, 1334 crosswalk rows. Idempotency: every writer run in README order with writes intercepted reproduces the current files byte-identically except `data/_staging/org_curation/unmapped.csv` (417 -> 5 rows).

## 1. Validator

Implemented: orphans (single and list fk, same_as, crosswalk ids, parent cycles), grade/status (D22), D18/D27 name-key collisions, D28, D23 same_as / DOI / prefix. Partial: ISO date order (crashes on malformed partner dates, no plausibility bound), evidence locators (presence only), roles for 4 of 7 event types, crosswalk freshness and acceptance (pytest only), rights rule (pytest only).

| # | mutation | result | severity |
|---|---|---|---|
| C1 | event grade `E` | crash KeyError (validate.py:240) | high |
| C2 | `founded_on=2020-1` with dissolved set; alias `valid_from=2020-1` | crash KeyError in pdate_lo | high |
| m01/m02 | event tables / crosswalk deleted | warning only | medium |
| m03/m04 | 500-char or `-` locator | accepted | medium |
| m05/m06 | wrong roles for event type | accepted | medium |
| m07 | grade-A event cites an unrelated eo: paper | accepted | low |
| m08 | web sources graded D while events stay A | accepted | medium |
| m09 | required list `;` | accepted | low |
| m10 | n_rows `1_000` / `-5` | accepted | low |
| m11 | founded 0000 / 2099 | accepted | low |
| m12 | country XX | accepted | low |
| m13 | ofc2026 row open_license_ok | accepted (pytest only) | medium |
| m14 | EO crosswalk row unmapped | accepted | medium |
| m15 | name-basis row to a no_name_match org | accepted | medium |
| m16 | same alias, scopes in different order | accepted | low |
| m17 | status acquired without event | accepted | low |
| m18 | imported_lineage anchor to another id, web source | accepted | low |
| m19 | announced 29 years after effective | accepted | low |
| m20 | participant dissolved 1900 | warning | low |
| m21 | event cites a same_as duplicate | accepted | low |
| m22 | name_basis inconsistent with origin | accepted | low |
| m23 | alias equal to own name | accepted | low |

## 2. Scripts

| item | location | severity |
|---|---|---|
| S1 add_ror_orgs overwrites `unmapped.csv` on rerun (417 -> 5 rows) | scripts/add_ror_orgs.py | medium |
| S2 merge_org_events regenerates event tables; a hand-added event would be erased | scripts/merge_org_events.py | medium |
| S3 build_sources keeps only web rows besides its 5 corpora; P2 ds: rows would be deleted | scripts/build_sources.py | medium |
| S4 registry hand-edited outside scripts (org_yofc fold, legal_name alias); a from-scratch rebuild recreates the duplicate; contradicts the DevLog "append-only" note | organizations.csv, org_aliases.csv | medium |
| S5 undocumented run-order dependencies (sources before events; curation before events) | README | low |
| S6 ROR file chosen by lexical sort (v2.15 < v2.9); version not pinned | adapters/ror.py | low |
| S7 sources of excluded events still added | merge_org_events.py | low |
| build_org_crosswalk exits 0 on acceptance failure | | low |

## 3. Adapters

Read-only ok; OFC session date ok; counts ok. E-mail regex misses `{a,b}@domain` and `[at]` forms (5 brace-form addresses exist in OFC headers, relevant to P3); test is tautological (same regex); `session_title` not stripped; `n_rows` description wrong in schema and script docstring.

## 4. Privacy

Tracked-file scan (94 files): no absolute paths, e-mails (except a test fixture `jane.doe@example.org`), secrets, private-startup / employer / diary references. Ignore rules verified.

| item | location | severity |
|---|---|---|
| Named derived career transitions incl. name-only identity matches and a collision-risk name list | DevLog/research/2026-10-20-people-atlas-assessment.md C.3, C.4 | high |
| LinkedIn-derived claim about a named person | people report D.4 item 4; DevLog-044 audit F | high |
| Nature SharedIt `sharing_token` URLs | blog_harvest/candidates.csv (4 rows) | low |
| Owner's personal bio text | candidates.csv (about page row); blog harvest report wording | low |
| NAS archive path fragment and timing | DevLog-044 audit A; DevLog-000 corpus table | low |
| OFC non-OA text in staging / notes | short affiliation lines with locators only | ok |

## 5. App

pnpm check / test pass; registry.json generated and ignored; base-path helpers used; no emoji; only `.spinner` rounded; dark default. Tooltip comment "for the sim UI" is a copy leftover.

## 6. Docs

README does not state per-script write behaviour; DevLog-001 TODO 3 overstated (locators presence-only, crash paths); group A open issues (summarizer-quoted locators, 8-K report vs filing dates) not carried over; append-only note contradicted by the YOFC fold; decision range D13-D25 stale (now D28); phantom match basis `ror_registry` in D25; DevLog-000 status stale; README "every script supports --dry-run" (validator is a reader); D15 role list vs schema `foundry_service`.

## Prioritized corrections (as proposed by the auditor)

1. Redact or git-ignore the people report name-only / collision / C.4 names and the LinkedIn lead (and its mention in the DevLog-044 audit) before any public commit.
2. Fix validator crashes.
3. Validator additions (missing built tables, locator rule, roles per event type, event vs source grade, rights rule, crosswalk acceptance and freshness) with one mutation test per rule.
4. add_ror_orgs must not overwrite unmapped.csv; build_sources keeps unknown corpora; merge_org_events preserves hand-added events.
5. Make the YOFC fold reproducible or document it.
6. Strengthen e-mail stripping before P3.
7. Carry group A open issues into DevLog-001; document per-script write behaviour.
8. Low: sharing tokens, about row, stale docs, ROR pin, Tooltip comment, crosswalk exit code.
