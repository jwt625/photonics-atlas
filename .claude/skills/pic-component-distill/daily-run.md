# Daily cache-and-ingest run (bench / lit queue)

Trigger: the owner says "run today's caching and ingestion" (or "start a new day's caching", "run today's"). This
file is the whole procedure. Do not mine earlier session transcripts for commands or briefs: they are here.
`SK=.claude/skills/pic-component-distill`; `S=<this session's scratchpad>`; all commands from the repo root.

## Standing authorization: no questions (owner, 2026-11-18)

The daily run is pre-approved end to end. Do not ask about any of these; asking was called out as a basic mistake.

| Step | Standing rule |
|---|---|
| Open routes (arXiv, OA publisher) | Launch at once |
| IEEE browser | Launch at once with `--wait-login`; tell the owner in one line that the window is open for sign-in. Do not ask |
| Optica browser | Launch at once with `$SK/scripts/optica_runner.py <day>` (OE / Optica / OME DOIs only; probe 3, 11, 15 min pause, rest). It stops at the first non-ok row and logs the paper, status and page snapshot (`RATE_LIMIT` or `CHECK`); it writes no breaker file |
| Stop on a non-ok row (Optica / IEEE) | Never ask, never leave a breaker (owner 2026-11-20: "remove the stupid breaker; whenever it breaks check manually; continue if the error is a standalone case"). Move any `logs/.lit_browser_blocked_<site>.json` aside to `logs/lit_browser_blocked_<site>_cleared_<stamp>.json`, then open the snapshot (`logs/lit_browser_<site>_<paper_id>_*.html`) and read it. Standalone case (that one article: no PDF, wrong article, paywalled item, one connection reset): relaunch the runner at once; saved papers are skipped. Rate-limit page (Optica: "downloading timeout based on heavy usage, try again in a few minutes"): wait 20 min, relaunch. Skip the route for the day only if the same rate limit or challenge comes back twice after waiting, and report it |
| Per-paper failures inside a run (owner 2026-11-23: "error like this should not trigger a full rerun, which means i have to login again") | The fetcher handles them in-process; an IEEE relaunch costs the owner a second sign-in, so it is the last resort. A dead DOI (doi.org "DOI Not Found", HTTP 404 / 410; day 209 takenobu2008 `10.1109/ofc.2008.4528185.2008`) is status `bad_doi`, no breaker, next paper (no automatic search: the coordinator confirms the DOI and fixes the row, next table row). IEEE: one challenge re-probes the session and, with the session intact, logs `blocked` for that paper only, cools down 3-6 min and continues; only a second challenge in a row sets the breaker and stops. A lost IEEE session waits in the same window for sign-in (`--wait-login`, 30 min) instead of exiting. If IEEE still exits, relaunch only the rows not yet attempted (`--paper-ids`, leave out the failed row) and list the failed row for the owner |
| Obvious data / fetcher error (owner 2026-11-24: "why are you even asking? cache and ingest the papers"; "you do the search and confirm the doi. The script should directly go to the doi papers") | Fix it at once, never ask or park it on the owner list: search the web yourself, confirm the DOI / Xplore document / open repository copy, zip-backup the lists, correct the queue / cache_list / bench_cache_list row (doi, uid, route_url together; day 211 takenobu2008 `...4528185.2008` -> `...4528185`). IET Electronics Letters and Optica conference papers are not on Xplore: route a repository copy as `oa_publisher` (day 211 shinobu2010, yang2013) |
| IEEE sign-ins (owner 2026-11-24: "I have logged in three times for you now in the last 15 min") | Every IEEE window can cost the owner a sign-in: collect all of the day's IEEE targets (fixed rows included) before the one launch; never relaunch for a single paper while another fix is pending. The fetcher saves the session cookies to `cache/browser_profiles/ieee_session_cookies.json` (git-ignored, 600) while access is confirmed and restores them at launch, so a needed relaunch reuses the sign-in |
| No rows for day N (benchmark list days 200-210 exhausted) | Run the backlog within the per-day caps: uncached Optica OA rows of earlier days (runner per day, `&&`-chained with 15 min gaps, about 45 per day) and held IEEE rows; ingest them as day N with the batch planner's exclude list (pre-run `lit` source snapshot) |
| Publisher browser | Not run (day 202 pattern). Leave the rows queued and list them in the final report |
| Fetch dry runs | None. The fetchers run directly (owner question 2026-11-15) |
| Ingestion start | Only after every launched caching route has finished (owner 2026-11-16: "why are you ingesting before the caching is done?") |
| Audit patches | Accept as the auditor recommends, record the ruling as a decision, merge. Items that change rows already merged go to the final report's owner list; never block the run on them |
| Commit and push | When everything is merged and checked, commit to `main` and push without asking (owner 2026-11-16 and 2026-11-17) |

Ask only on a real blocker: IEEE sign-in not done after 30 min, failing checks you cannot fix, or anything that would
delete or overwrite owner data. A fetch stop or breaker is not a blocker: check the snapshot by hand, clear, continue (table above).

## 1. Day number and queue

- Day N = the last `Bench day N` commit + 1 (`git log --oneline -5`). Queue rows: `data/_staging/literature/retrieval_queue.csv`
  with `day == N`; route counts by `route` (arxiv, oa_publisher, ieee_browser, optica_browser, publisher_browser).
- Breakers: `logs/.lit_blocked_<host>.json` and `logs/.lit_browser_blocked_*.json` (`until` epoch; expired ones are
  ignored by the fetchers). An `optica` / `ieee` browser breaker is moved aside before launch and the route run (table above), never asked about.

## 2. Caching (all three launched in the first minutes; separate tmux sessions)

```sh
TS=$(date +%Y%m%dT%H%M%S)
tmux new-session -d -s lit_bench_dN  "cd $PWD && uv run python scripts/lit_fetch_oa.py --day N 2>&1 | tee logs/lit_bench_dN_oa_$TS.log"
tmux new-session -d -s lit_ieee_dN   "cd $PWD && uv run python scripts/lit_fetch_browser.py --site ieee --run --day N --wait-login 2>&1 | tee logs/lit_bench_dN_ieee_$TS.log"
tmux new-session -d -s lit_optica_dN "cd $PWD && uv run python $SK/scripts/optica_runner.py N"
```

- Open routes take about 5 min (MDPI / ACS / AIP / SPIE / ScienceDirect usually 403 and arm breakers; those rows go to
  the manual list at registration). IEEE runs about 110 s per paper (30 rows: about 55 min). Optica finishes about
  the same time as IEEE.
- Per-paper statuses that do not stop a run: `bad_doi`, `no_access`, `no_ieee_copy`, `wrong_pdf`, `no_arnumber`,
  `not_found`, `error`, and a single IEEE `blocked` with the session intact. They go in the final report's caching
  table with the paper id; a `bad_doi` row also goes on the owner list (queue DOI to fix).
- IEEE crash on the first home-page `goto` (`net::ERR_ABORTED; maybe frame was detached`, day 203) is transient:
  relaunch the same command once; it found institutional access 12 s later.
- Progress: `grep -c "\] ok" logs/lit_bench_dN_ieee_*.log`; `cat logs/lit_optica_oa_dN_2*.log`. Wait with a
  background Monitor until both tmux sessions have exited; no polling loops, no ingestion meanwhile. While waiting,
  read the tails of DevLog-007 / -019 and this skill, and find the next decision id (step 3).

## 3. Ingestion (one wave, after caching)

1. Extract and check:
   `uv run python scripts/lit_extract.py --pending > logs/lit_extract_dN_$TS.log 2>&1` (FLAGS lines name
   `garbled_text_layer`, `institutional_stamp`); `uv run python $SK/scripts/title_check.py N` (page-1 title coverage;
   below 0.9 or a correction / erratum: open page 1 and decide; a preprint of the listed work is kept with a note in
   the distill brief; another paper or a correction notice is stopped, D397 / D409).
2. Register: `uv run python scripts/lit_register_sources.py > logs/lit_register_dN_$TS.log 2>&1`,
   `uv run python scripts/validate_db.py` (0 errors), `uv run python scripts/lit_manual_list.py`.
3. Plan: `uv run python $SK/scripts/plan_batches.py N <next lit_NN> $S/batches_dN.json --max=5`
   (`ls data/_staging/components | sort -V | tail -1` for the next NN). Next decision id:
   `grep -ho '^| D6[0-9]*' DevLog/*.md | sort -V | tail -1` (lit-ingest range; D1200+ belongs to DevLog-019).
4. Backup and side batches: `zip -qr $S/components_before_lit<NN>_$TS.zip data/components`;
   `uv run python $SK/scripts/write_header_batches.py $S/batches_dN.json <next hNN>` (next hNN:
   `ls data/_staging/people/lit_headers | sort -V | tail -1`); vendor scan with the printed `VENDOR_ONLY` list:
   `uv run python scripts/scan_vendor_models.py --only "<VENDOR_ONLY>" --batch lit_<next supply NN> --batch-new-only`.
5. DevLog-007 before any dispatch: one decision row (day, PDFs by route, title check, registration counts, batch
   table, header and supply batch names, backup name) and a timestamped progress line. Append with the Edit tool or a
   quoted heredoc (`<<'EOF'`): an unquoted heredoc ate the backticks twice on day 202.
6. Dispatch with the briefs below: one distill per batch, header extractors, one supply reviewer; at most 10 subagents
   at once in all streams; queue the rest. As each distill returns, dispatch its fresh-context audit (distills first
   when slots are short: they are the critical path).
7. Per audited batch: ruling as a decision row in DevLog-007, then `$SK/scripts/merge_batch.sh lit_NN` (patch, re-run
   0 changes, dry run, merge; log under `logs/`). Merges serialized.
8. Header batches: `ofc_headers.py check` 0 errors, fresh audit, apply the audit's F-fixes to `headers.yaml` yourself
   and re-check. Supply: `build_supply_staging.py lit_NN --check-review`, `zip -qr $S/supply_before_lit_NN_$TS.zip
   data/supply`, `--merge`.
9. After the last merge, Coordinator workflow steps 4 (aggregate, people backup, two byte-identical
   `build_people.py` runs, `derive_transitions.py`) and 7 (builds and checks), then:
   - render check: `cd app && npx vite preview --port 4791 --strictPort &` (check the port first), then
     `uv run python $SK/scripts/render_check.py $S <components> <metrics>` (0 console errors on all 8 pages, totals on
     the dashboard; look at `$S/bench.png`), stop the preview;
   - benchmark cells that moved vs HEAD: check the source rows behind any big jump and list them in the report;
   - privacy scan of every added line (`git diff HEAD -U0`): e-mail, local paths, street / P.O. box, postal codes
     (`[0-9]{5,6}, <Country>`), emoji; decision ids in shipped `app/static/data/*.json` not above HEAD's count.
10. DevLogs: DevLog-007 (decisions, progress, session close), DevLog-019 (day line, wrong benchmark-list resolutions),
    DevLog-003 (supply decision), DevLog-011 (people decision).
11. Commit and push: `git add -A DevLog app/static data scripts references` (never `logs/`, PDFs, `text.md`,
    figures: check `git diff --cached --name-only`), one line:
    `Bench day N: <K> lit papers cached and ingested (lit_AA-lit_BB, headers lit_hX-hY, supply lit_P-Q; DAAA-DBBB), components C / metrics M`.
12. Final report: caching table by route, ingestion counts, audit totals, benchmark cells that moved, publisher rows
    still queued, owner decision list.

## Brief templates

Fill `<...>`. Paths are repo-relative; give each agent its own scratch folder `$S/<batch>/`.

Distill:

```text
You are a distill agent for the photonics-atlas repo at <repo root> (all paths below are relative to it).

Read first and follow exactly: .claude/skills/pic-component-distill/SKILL.md (hard rules, Contracts v4-v7, workflow, pitfalls), then data/schema/components.schema.yaml, data/schema/component_parameters.yaml, and the decision tables in DevLog/DevLog-002-p1-component-atlas.md and DevLog/DevLog-007-lit-distill.md (lit rulings D150-<latest>).

Batch lit_NN: papers lit:<id>, lit:<id>, ... (inputs references/<paper_id>/text.md, figures/page_NN.png, source.json; source rows in data/registry/sources.csv). <per-paper notes from the title check: preprint of the listed journal paper, garbled_text_layer, etc.>
Write only into data/_staging/components/lit_NN/: components.csv, component_metrics.csv (same columns as data/components/*.csv) and BATCH_REPORT.md (per paper: components / metric rows, values not entered and why, missing fab / facility orgs as printed + locator, judgment calls, registry gaps). Validate with `uv run --offline python scripts/merge_component_staging.py data/_staging/components/lit_NN --dry-run` until 0 errors. Helper scripts only in <S>/lit_NN/.

These papers were selected because other papers cite them in benchmark tables; distill only what each paper itself reports (rule 1 and 3). No network, no git, no edits outside your staging dir and scratch folder, no emoji, no e-mail addresses or postal addresses. verified_on = <today>. Final message 5-10 lines: per paper components / metrics, anything stopped on.
```

Distill audit:

```text
You are a fresh-context auditor of a component distill batch in the photonics-atlas repo at <repo root>.

Read and follow the "Audit workflow" section of .claude/skills/pic-component-distill/SKILL.md, with all hard rules and Contracts v4-v7 in that file, data/schema/components.schema.yaml, data/schema/component_parameters.yaml and the decision tables of DevLog/DevLog-002-p1-component-atlas.md and DevLog/DevLog-007-lit-distill.md. Format examples: DevLog/audits/<recent date>-lit_<NN>-audit.md.

Batch under audit: data/_staging/components/lit_NN (papers lit:<id>, ...; texts references/<id>/text.md, renders references/<id>/figures/page_NN.png). Read-only on the batch. Do not trust BATCH_REPORT.md: check every metric row at its locator, look for misses, and give recommendations on the judgment calls: <(a) ... (b) ... from the distiller's final message>.

Outputs: DevLog/audits/<today>-lit_NN-audit.md and data/_staging/components/lit_NN/patch.yaml (the only file you write in the batch dir). Validate on a scratchpad copy only (<S>/lit_NN_audit/): `uv run --offline python scripts/patch_component_staging.py <copy> <batch>/patch.yaml`, re-run (0 changes), `uv run --offline python scripts/merge_component_staging.py <copy> --dry-run` (0 errors). Privacy grep of your outputs. No network, no git, no emoji. Final message 5-10 lines: counts ok / imprecise / wrong, misses, coordinator questions with recommendations.
```

Header extractor:

```text
You are a header (author / affiliation) extractor for the photonics-atlas repo at <repo root>.

Read and follow exactly: data/_staging/people/lit_headers/CONTRACT.md and data/_staging/people/ofc_headers/CONTRACT.md (the lit contract extends the OFC one), and the DevLog-011 decisions they cite (DevLog/DevLog-011-lit-author-affiliations.md).

Batch: data/_staging/people/lit_headers/lit_hNN (papers.csv lists <n> lit papers; <zero-author-meta ids> have no metadata author list, so take the authors from the printed header). Tools: `uv run --offline python scripts/ofc_headers.py show lit_hNN --corpus lit --codes <id>[,<id>] [--pdf]`. Write the batch outputs the contract specifies into that batch dir only; run `uv run --offline python scripts/ofc_headers.py check lit_hNN --corpus lit` until 0 errors. Helper scripts only in <S>/lit_hNN/. Known checker gaps (keep the affected papers `partial` with a note, as earlier batches did): present-address-only authors (D426 G4), building numbers inside unit chains (D426 G6), contact in parentheses after a name in a footnote statement, department-only block with the org printed once after the next block (lit_h17 G3), "Current address" cue (D442), empty locality accepted when the block prints a city (D599). Notes must not name buildings, streets or postal codes either.

Org / unit / city / country only: never street, building, postal code, P.O. box or e-mail addresses in any output. No network, no git, no edits outside the batch dir and scratch folder, no emoji. Final message 5-10 lines: papers ok, rows, check result, anything unusual.
```

Header audit:

```text
You are a fresh-context auditor of an author / affiliation header batch in the photonics-atlas repo at <repo root>.

Rules: data/_staging/people/lit_headers/CONTRACT.md and data/_staging/people/ofc_headers/CONTRACT.md, DevLog/DevLog-011-lit-author-affiliations.md decisions. Batch under audit: data/_staging/people/lit_headers/lit_hNN (headers.yaml written by an extractor; derived files from `ofc_headers.py check`). Format examples: DevLog/audits/<recent date>-lit-header-batch-h<NN>-audit.md.

Read-only on the batch. For every paper verify against the source (`uv run --offline python scripts/ofc_headers.py show lit_hNN --corpus lit --codes <id> [--pdf]`): author slots and order, affiliation blocks and markers, org / unit / city / country strings as printed, the extractor's calls (<list from the extractor's final message>), and that no street, building, postal code, P.O. box or e-mail appears anywhere, including notes. Do not trust the extractor's report. Probe alternatives on scratch copies only (<S>/hNN_audit/).

Output: DevLog/audits/<today>-lit-header-batch-hNN-audit.md (front matter title / date / mode; per-paper findings; counts; numbered fixes F1.. each with the exact headers.yaml change; verdict GO / NO-GO). Do not edit headers.yaml yourself. No network, no git, no emoji. Final message 5-10 lines: verdict, fixes.
```

Supply reviewer:

```text
You are a supply-scanner reviewer for the photonics-atlas repo at <repo root>.

Read and follow exactly: data/_staging/supply/products/REVIEW_CONTRACT.md and data/_staging/supply/products/COORD_RULINGS.md (and the DevLog-003 decisions they cite). The previous batches <lit_PP, lit_QQ> (review.csv there) were reviewed and merged; follow their conventions for consistency.

Batch: data/_staging/supply/products/lit_NN (<k> candidates from <n> lit papers). Write ONLY data/_staging/supply/products/lit_NN/review.csv, following the contract's columns and rules. Tools: `uv run --offline python scripts/scan_vendor_models.py --print-batch lit_NN`, `--print-source <source_id>`. Then run `uv run --offline python scripts/build_supply_staging.py lit_NN --check-review` until it passes. Helper scripts only in <S>/sup_lit_NN/.

No network, no git, no edits anywhere else, no emoji, no addresses or e-mails. Final message 5-10 lines: counts by decision, anything for the coordinator.
```

## Unattended open-access night (owner away 2026-11-26 to 2026-11-28)

Owner 2026-11-25: "setup timer to kick you off and run caching and ingestion for open access (arxiv, optica, optics
express etc.) papers tomorrow and Friday and Saturday, at 10 pm. Follow the skill except for paper/journal type ...
Cmt and push once done after each day's portion"; about 50 papers per night at most. Chain (DevLog-020 D1237): a
launchd agent at 22:03 -> a launcher outside the repo -> the running tmux server -> `scripts/night_oa_session.sh run`
-> interactive `claude` in auto permission mode (tmux session `lit_night_run_<stamp>`). The session script holds the
lock `logs/.night_oa_active` while a run is active; the run removes it as its very last step.

- Nobody is there to answer: never ask (no AskUserQuestion), never wait for input. A command the permission check
  denies is not retried in variants: write an owner-list line in DevLog-007 and skip that step. A real blocker
  (failing checks you cannot fix, anything that would delete or overwrite owner data) goes into DevLog-007 as an
  owner-list line, then commit what is clean, push, and stop. Everything else follows the standing authorization
  table above.
- First `git status`: work left uncommitted by an earlier run (a merged batch, DevLog lines) is finished (checked,
  committed, pushed) before this night's caching starts; never reset, revert or delete it.
- Day N = last `Bench day N` commit + 1 (nights 2026-11-26 / -27 / -28 = days 213 / 214 / 215). Queue rows of days
  213-215 come from the reference graph (DevLog-020 stage 3): per day arXiv 15, oa_publisher 5, optica_browser 30,
  publisher_browser 10 (not run), no IEEE rows.
- Snapshot before caching: `$S/pre_lit.json` = `{"pre": [every native_id of corpus lit in data/registry/sources.csv]}`.
- Optica days D = every day with uncached OE / Optica / OME optica_browser rows up to N, oldest first (night 1:
  203,207,213; the runner takes at most 30 papers in that order, so later nights start with the previous day's rest).
  List them with a short script over `retrieval_queue.csv` (route optica_browser, doi `10.1364/(oe|opex|optica|ome).`,
  no `references/<id>/source.pdf`).
- Caching, launched together in tmux:
  `uv run python scripts/lit_fetch_oa.py --day N 2>&1 | tee logs/lit_bench_dN_oa_$TS.log` (arXiv + open-access
  publishers only) and `uv run python $SK/scripts/optica_overnight.py <D comma-separated> --max 30` (one paper per
  browser launch, 4-6 min apart, 30-min back-off on Optica's rate-limit page; about 3 h). No IEEE (no sign-in
  possible), no publisher browser. Wait for both with a background Monitor / until-loop; ingest only after both exit.
- Ingestion = section 3 with these changes: extract with `lit_extract.py --pending`; title check with
  `title_check.py` for N and for each Optica day in D; plan with
  `plan_batches.py <D and N comma-separated, e.g. 203,207,213> <next lit_NN> $S/batches_dN.json --max=5 $S/pre_lit.json`
  (the exclude snapshot keeps already-ingested papers of the backlog days out); header batches and vendor scan from
  that batch file as usual.
- Checks, DevLogs (DevLog-007 session with the caching table, decisions, owner list; DevLog-019 day line), then commit
  and push (section 11, with `.claude/skills` added to the `git add` list). Last step after the push:
  `rm logs/.night_oa_active`.
