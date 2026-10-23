# People atlas: OFC 2026 header merge audit (2026-10-23)

Fresh-context audit of the OFC 2026 paper-header merge into the people tables (DevLog-004 D214-D219, Progress
2026-10-23 00:00; DevLog-008 merge path, D240-D245, D281-D289, D300-D305). Read-only: no repo file changed except this
report. Scripts and outputs in the session scratchpad (`people_merge_audit/`), not committed.

Baselines: current `data/people/*.csv` (written 00:02); the 22:52 build from the zip backup
`people_backup_2026-10-22_r5.zip` (people tables + local queue); staged rows of all 16 batches
(`pilot`, `ofc_h01..ofc_h15`, all 16 check stamps recomputed and current, 5478 rows, A 4955 / B 523); registry,
crosswalk and `sources.csv` as on disk at 00:07.

## Verdict

**Go.** 0 wrong in checks 1, 2, 4, 5, 6, 7, 8. Check 3: samples clean, full population shows 1 minor finding (F1: 3
observations lose their registry org link through a parenthetical-dropping fold). No identity change, no exposure.

## Counts per check

| # | Check | ok | wrong | Notes |
|---|---|---|---|---|
| 1 | 80 random header observations traced field by field (obs id -> staged row: org id incl. `.m`, printed org, unit, country, role, locator, printed name, grade (= staged grade = basis rule), kind, source, `active_on` = session date; person = the slot's person in the 22:52 build) | 80 | 0 | Full population: header printed name shares a name token with the slot's metadata name in 5449 / 5449; validator 0 errors on every header row |
| 2 | Conflict slots: every observation review | 10 | 0 | 20 rows (10 metadata + 10 header), all review; 8 metadata rows public -> review, 2 already review (queue). Local list 11 = these 10 + `Th1D.1#a20` (EO calibration paper, slot not in the build) |
| 3a | 40 sampled confirmed slots: dropped metadata row matches a header root org (or printed string) | 40 | 0 | Full population: independent re-classification agrees on 4315 / 4318 confirmed slots; 3 differ (F1) |
| 3b | 30 sampled unmapped / conflict slots: metadata row kept unchanged | 30 | 0 | Full population: 385 / 385 kept (375 unmapped + 10 conflict; 390 rows, public 323 / review 67) |
| 4 | 3 persons public -> review | 3 | 0 | `person_aristotelis_kretsis` (M3Z.6#a1), `person_edward_echeverry` (W4H.1#a2), `person_lukas_rapp` (M3K.4#a1): each had one observation, on a conflict slot; now 2 review rows each. 0 persons review -> public; 0 public persons without a public observation or LIN record |
| 5 | No person-id change, no new join | all | 0 | 0 of 10120 slots change person, 0 slots lost, 0 obs change person; `people.csv` 0 added / 0 removed, only `visibility` differs (3 rows); `person_xref.csv` identical (7664); merges 120 / 1762 / 1652 (dry-run log); local review queue byte-identical to the 22:52 queue (470 pairs) |
| 6 | +900 aliases marked not-for-identity, name text only | 900 | 0 | All origin `ofc2026`, note "OFC paper header form; not used for identity (D218)"; abbreviated 564 / printed_variant 336; every alias is a header printed name of the same person; 0 aliases lost. Non-letter characters: `.` 797, `-` 38, `(` `)` 4 each. No consumer reads `person_aliases` for identity (only `rules_people.py` printed-name check) |
| 7 | Privacy: `app/static/data/people.json` (00:06) | all | 0 | 6248 persons = the 6248 public persons; 10688 obs = the 10688 public obs; 0 review persons / obs; 0 field differences vs the CSV; the 3 D216 persons absent; no alias field. No line of the local conflict / extra-author lists, review queue, name-only candidates or transitions, and no queue pair, in any non-ignored file (819 files); `data/_local/` git-ignored |
| 8 | EO-duplicate papers skipped | 2 papers | 0 | Th1D.1 (37 rows, same_as `eo:tobing2026`) and Th4A.1 (12 rows, `eo:aihara2026`): 49 staged rows, 0 observations cite them, no alias from them; EO canonical rows (37 + 12) present |

Additional: all header rows come from papers with status `ok` (5357) / `partial` (121); 0 rows for the 37 unreadable
authors; every obs id matches schema v3 `people_obs_id`. DevLog-004 Progress 00:00 numbers reproduced exactly
(5449 header obs, A 4922 / B 527, primary 4836 / additional 605 / present_address 8, public 4816 / review 633, 588
without org id; 4326 metadata rows removed, all from the 4318 confirmed slots; 8 visibility changes).

## Runs

- `uv run python scripts/build_people.py --dry-run`: exit 0; 0 new persons, 0 refreshed fields; stats equal to the
  committed tables (6922 persons, 11955 obs, 1235 aliases, 470 pairs). Header merge: confirmed 4318 / unmapped 375 /
  conflict 10; 49 rows without a kept slot; no stale batch.
- Real build redirected to a scratch copy of `data/people/` (module `OUT` / `LOCAL` patched): all 4 tables and the
  review queue byte-identical to the repo files. SHA-1 of `data/people/*.csv`, queue and `people.json` unchanged
  before / after all runs.
- `uv run python scripts/validate_db.py`: 0 errors, 15 warnings (none people).
- `uv run pytest tests/test_people.py tests/test_views.py`: 46 passed (includes
  `test_no_review_ids_in_committed_views`, failing at 00:00, now passing after the 00:06 view rebuild).

## Findings

F1 (minor, wrong outcome, D215 letter followed). `header_status` uses the person-name `fold()`, which deletes
parenthesized text. `ofc2026:M4C.4#a1`, `#a3`, `#a4`: metadata "Amirkabir University of Technology"
(`org_amirkabir_university_of_technology`) vs header "Amirkabir University of Technology (Tehran Polytechnic)"
(staged `org_ids` empty, `match_basis` unmapped). Folded strings are equal, so the slots are confirmed and the metadata
rows dropped; the 3 remaining header observations have `org_id` empty. Net: 3 public observations lose a registry link
that the 22:52 build had (printed org kept). These are the only 3 of 4318 confirmed slots where no header row carries
the metadata org or its root. Evidence: 22:52 rows `ofc2026:M4C.4#a{1,3,4}.1`; current `#a{1,3,4}.h1.1`;
`ofc_h04/header_rows.csv`; `org_requests.csv` already proposes `org_amirkabir_university_of_technology`.
Fix (either): (a) apply the org request and re-run `ofc_headers.py check ofc_h04` + `aggregate` so the staged rows
carry the id, then rebuild; (b) in `header_status`, accept the folded-string match only when the metadata is unmapped or
some header row reproduces a metadata root, else `unmapped` (keep the metadata row). (b) is the general guard; (a)
alone fixes the 3 rows.

F2 (info, by rule). 31 confirmed slots drop a metadata org id whose root is in the header: 27 replace a root by a more
specific child (Nokia -> Nokia Bell Labs, A*STAR -> IME / NSTIC, Huawei -> Huawei Technologies Canada, Corning -> Corning
R&D, Marvell -> Celestial AI); 4 coarsen: `M1F.1#a5/#a6/#a8` FOTON -> CNRS + Universite de Rennes (header
"Institut FOTON" unmapped, `org_requests.csv` row without proposed id) and `W4E.5#a8` Institute of Integrated Research
-> Institute of Science Tokyo (the unit is kept in `unit`). Fix: register "Institut FOTON" as an alias of the FOTON
org through the org-curation stream; re-check `ofc_h01`.

F3 (info). 19 header aliases equal another person's display name (e.g. `person_adytia_kakkar` alias "Aditya Kakkar" =
`person_aditya_kakkar`; `person_joyce_poon` alias "Joyce K. S. Poon" = `person_joyce_k_s_poon`). Expected under D217
(header names are not identity evidence); they are candidates for the separate, reviewed header-identity change. Any
future consumer that resolves persons by alias must honour the D218 note.

F4 (info). Alias form: 2 joined-initial forms without spaces (`G.Talli`, `Y.W.Liu`, typed abbreviated) and 4 printed
parenthetical given names (`Li (Grace) Zhang`, `Linke (Link) Li`, `Ming (Richard) Xiao`, `Tianshu (Gavin) Wu`). Name
text as printed; no fix needed.

F5 (info). D216 says review "until the local conflict entry is resolved"; the build does not read
`data/_local/ofc_headers_conflicts.csv` and recomputes conflict from the crosswalk / staged ids. A conflict is cleared
only by a registry / crosswalk change or a staged-row correction, not by marking the local entry. Fine for now; record
the resolution path in DevLog-004 when the first entry is resolved.
