---
title: Literature lane L3 (arXiv preprints) harvest report
date: 2026-10-21
scope: DevLog-006 stage S1, lane L3
---

# Lane L3: arXiv preprints 2018-01-01 to 2026-10-21

## What ran (2026-10-21, 15:39-16:01 local)

- Script: `scripts/lit_harvest_arxiv.py` (stdlib `xml.etree` Atom parser; every request via `photonics_atlas.litfetch.get`).
- Probes (tiny requests, max_results 1-3) for query syntax, then pilot `--start 2026-09 --end 2026-09`, then
  `uv run python scripts/lit_harvest_arxiv.py --max-minutes 8` three times (newest to oldest, resumable, skip-existing).
- Tests: `tests/test_lit_harvest_arxiv.py` (3 pure-function tests, no network). ruff, ruff format, mypy strict pass.
- Logs: `logs/lit_harvest_arxiv_20261021T*.log|jsonl`, requests in `logs/litfetch_2026-10-21.jsonl`.

## Queries (sortBy submittedDate ascending, max_results 500, one window per calendar month)

| set | file | search_query |
|---|---|---|
| optics | `arxiv_optics_YYYY-MM.jsonl` | `cat:physics.optics AND submittedDate:[YYYYMMDD0000 TO YYYYMMDD2359]` (primary or cross-list) |
| appq | `arxiv_appq_YYYY-MM.jsonl` | `(cat:physics.app-ph OR cat:quant-ph) AND (KW) AND submittedDate:[...] ANDNOT cat:physics.optics` |

KW = `abs:waveguide OR abs:waveguides OR abs:"integrated photonic" OR abs:"integrated photonics" OR abs:"integrated optics"
OR abs:"integrated optical" OR abs:"photonic integrated" OR abs:"photonic chip" OR abs:"silicon photonics"
OR abs:"silicon photonic" OR abs:"on-chip" OR abs:microring OR abs:"ring resonator" OR abs:"lithium niobate"
OR abs:"silicon nitride"`.

- `ANDNOT` must be the last clause: `A ANDNOT B AND (C)` is mis-parsed by the API (probe: 189,430 hits).
- appq also includes entries whose primary is another archive but cross-listed to app-ph / quant-ph (e.g.
  cond-mat.mes-hall 238). Safety filter drops any appq entry carrying physics.optics (0 dropped).
- Pilot check (2026-09 appq, 53 hits): 41 contain a KW literal in the abstract; 12 do not (arXiv tokenization of
  phrases such as "on-chip"), so appq has some off-topic hits; no relevance screening done here.

## Outputs (`cache/literature/pool/`, git-ignored, 84 MB)

212 files (106 months x 2 sets), 40,594 records, 40,594 unique uids, 0 duplicates across files, 0 records outside
their window. All windows < 2000 (max 532), so no day splits were needed; every window reached opensearch:totalResults.

| year | optics | appq |
|---|---|---|
| 2018 | 2,878 | 291 |
| 2019 | 3,454 | 312 |
| 2020 | 3,844 | 369 |
| 2021 | 4,037 | 316 |
| 2022 | 3,976 | 336 |
| 2023 | 4,202 | 407 |
| 2024 | 4,633 | 491 |
| 2025 | 5,160 | 601 |
| 2026 (to 10-21) | 4,743 | 544 |
| total | 36,927 | 3,667 |

Monthly range: optics 198 (2018-04) to 532 (2026-05); appq 17 (2018-02) to 76 (2026-03). Per-month counts are in the
run logs (`month` events).

optics primary archive: physics.optics 23,221; quant-ph 4,319; cond-mat.mes-hall 1,617; physics.app-ph 1,502;
cond-mat.mtrl-sci 824; physics.ins-det 529; physics.atom-ph 502; eess.IV 425. appq primary: quant-ph 2,240;
physics.app-ph 798; cond-mat.mes-hall 238; cond-mat.mtrl-sci 72.

## Completeness check

physics.optics volume is 2.9-5.2k per year, below the 7-12k planned. Verified for 2023-09: the arXiv listing page
`/list/physics.optics/2023-09` shows 327 entries (127 cross-lists); all 327 ids are in the pool (324 in the 2023-09
file, 3 held submissions with v1 dated 2023-05 / 2023-07 in those month files). The API `submittedDate` is the v1 date,
so ids can sit in an earlier month file than their id prefix.

## Record fields

litpool layout: uid `arxiv:<id without version>`, arxiv_id, title, authors (first 30), n_authors, last_author,
abstract, year and publication_date = v1 date, type `preprint`, venue `arXiv`, venue_type `repository`, is_oa true,
oa_url `https://arxiv.org/pdf/<id>`, lane `arxiv`, discovered_via = query, harvested_on 2026-10-21. Extra:
`arxiv_primary`, `arxiv_categories`, `arxiv_updated`, `arxiv_journal_ref`, `arxiv_comment`, `arxiv_dois`.

- `doi`: journal DOI from `arxiv:doi` (first token if several, all in `arxiv_dois`) for 20,209 records; uid stays
  `arxiv:`. The S2 merger must dedupe on doi against journal / conference lane records (and arxiv_id against OpenAlex
  records with 10.48550 DOIs). journal_ref present for 12,968.
- `license`: not exposed by the API, empty for all. `oa_status` empty. `cited_by_count` null (unknown, not 0).
- `institutions`: only from `arxiv:affiliation` (first / last author), present for 886 records.
- `openalex_id` empty.

## Requests and problems

- export.arxiv.org: 233 requests, all HTTP 200 (includes 2 listing pages and 1 id_list check); no 429/503, breaker not
  armed. Spacing by litfetch (>= 3.5 s + jitter).
- 2026-10 files are partial (to 2026-10-21). They exist, so reruns skip them; to refresh, move both 2026-10 files
  aside and run `uv run python scripts/lit_harvest_arxiv.py --start 2026-10 --end 2026-10`.
