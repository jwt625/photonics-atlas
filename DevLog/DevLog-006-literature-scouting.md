---
title: Literature scouting, screening and downselection for the component atlas (~1000 papers)
date: 2026-10-21
status: S0-S6 done; inspection point (D129) before S7 retrieval
scope: P1 component atlas, new literature beyond the EO / packaging / OFC 2026 corpora
authors: Claude (at Wentao Jiang's request)
---

# DevLog-006: Literature scouting for the component atlas

Decisions here are D120-D139.

## Request (2026-10-21, Wentao)

"Propose and scout more relevant literatures to cache for ingestion. Take a look at how literatures are sourced for
the other two atlas projects, come up with a plan and delegate to subagents for exploring various sources, cache list
of papers from various journals or conferences, and screen them with author/title/abstract and downselect papers to
cache and ingest. Budget for ~30 papers per component etc, and total of ~1000 papers."

## Starting point (2026-10-21)

- 554 components / 1977 metric rows from 246 sources: eo 305 components, ofc2026 192, pk 57. Every source so far is
  side data of modulator papers, OFC 2026 (non-OA, facts only) or packaging papers. No dedicated new literature yet.
- Classes with no or almost no rows: free_space_emitter 0, crossing 0, nonreciprocal 1, frequency_converter 1,
  polarization 3, reflector 5, amplifier 6, switch_fabric 10 (taxonomy report section 5 lists the same gaps).
- Seeds already on disk: taxonomy report section 5 (32 review / benchmark references), blog harvest
  (`DevLog/research/blog_harvest/candidates.csv`, 534 OA photonics identifiers in neither atlas), EO atlas
  `data/candidates.csv` (462 rows, modulator-focused).

## How the sibling atlases sourced literature (read 2026-10-21)

| step | eo-modulator-atlas | advanced-packaging-atlas |
|---|---|---|
| discovery | topic / author / group searches by 3 subagents (Crossref, OpenAlex, arXiv last) + seed lists | full table-of-contents enumeration per venue-year (Xplore, Crossref by prefix), abstracts from OpenAlex; pool 10,342 |
| screening | subagent priority 1/2/3 from title + abstract, no rubric | regex prefilter (`prefilter.py`, `buckets.yaml`) -> 4,388; LLM scoring 0-10 with a point rubric (`scoring_prompt.md`, batches of 100) -> ~3,900 scored; curation subagent per bucket; `select_cache.py` + `selection.yaml` (threshold, per-bucket floors on n / orgs / years, cap 300) |
| retrieval | arXiv + CC-licensed publisher PDFs, serialized fetcher (lock, 5 s + jitter, per-host breaker); paywalled -> `references/_inbox/` manual list | Xplore via headed browser with SSO (60-120 s spacing, 60 / 2 h); manual list |
| cache | `references/<firstauthorYEAR>/` source.pdf, source.json, text.md (PyMuPDF, `<!-- page N -->`), figures/ | same, paper_id = DOI suffix, OCR fallback |
| lessons | arXiv 429 with two agents in parallel; one download owner only | Xplore WAF for headless; 2.8 % placeholder abstracts |

This plan copies the packaging pipeline (enumerate, prefilter, LLM-score, curate, select by rules) because it is
reproducible and auditable, and the EO cache layout and fetcher rules for retrieval.

## Constraints found while planning

- OpenAlex (probed 2026-10-21): without an API key all callers on this IP share $0.10/day. A request with a search term
  costs $0.001 (100/day); a filter-only list page (up to 200 records with abstracts) costs $0.0001 (~200k
  records/day); singleton gets cost 0. Consequence: harvest by venue-year filter lists, never by keyword search, and
  screen locally. A free personal key ($1/day) needs the user's email at openalex.org (question Q1).
- Crossref: free, no key; abstracts only for publishers that deposit them (good for Optica / Springer Nature, absent
  for IEEE). Used for venues OpenAlex lacks and for gap-filling.
- arXiv: one owner at a time, >= 3.5 s spacing (EO 429 history).
- Shared client `src/photonics_atlas/litfetch.py`: per-host file lock + minimum interval, breaker on 403/429/503,
  OpenAlex daily cost cap (`OPENALEX_DAILY_CAP_USD`, default 0.08), generic User-Agent, no personal identifiers,
  request log `logs/litfetch_<date>.jsonl`. Every scouting script uses it, so parallel subagents cannot exceed limits.

## Decisions (D120-D129)

| # | Decision | Rationale |
|---|---|---|
| D120 | Target ~1000 papers selected for caching and ingestion, allocated per class (budget table below, ~30 minimum per class, more for broad classes; 35 reserve for curator benchmark / record picks). A paper counts once, toward its primary class | request |
| D121 | Window: journals and conferences 2016-2026 by enumeration; older landmark / record papers only via the seed + snowball lane | recency and volume; benchmarks still reachable |
| D122 | Pipeline = packaging-atlas pattern: S1 enumerate venue-years + seeds -> S2 regex prefilter with per-class caps -> S3 LLM scoring of title / authors / venue / abstract (rubric in `config/literature/scoring_prompt.md`) -> S4 curation subagent per class group -> S5 rule-based selection (`config/literature/selection.yaml`) -> S6 fresh-context audit -> S7 retrieval -> S8 distill batches | reproducible, auditable |
| D123 | Exclude papers already in the eo / pk / ofc2026 corpora or `sources.csv` (DOI, arXiv id, normalized title). EO-modulator papers stay in the EO atlas; reviews are snowball seeds, not ingestion targets (their numbers are cited work, skill rule 3) | no duplicates; skill rules |
| D124 | OA first: target >= 80 % of the selection open (arXiv or OA journal). Paywalled picks need score >= 8 or a curator reason, and go to a ranked manual-download list (`references/_inbox/`, `<id>.pdf`) | retrieval cost; rights |
| D125 | Diversity rules per class: subtype floor (min(5, available)), >= 3 platforms where available, <= 4 papers per senior (last) author, >= 3 years, industry / foundry papers kept when scored | avoid one-group dominance; supply-chain value |
| D126 | Storage: raw API pages and abstracts stay in git-ignored `cache/literature/`; committed: configs, prefilter / scoring statistics, `data/_staging/literature/cache_list.csv` (ids, title, venue, year, classes, score, rationale <= 20 words, access) and the triage report | abstracts are publisher text; OpenAlex metadata CC0 |
| D127 | New registry corpus `lit` for these papers (`lit:<firstauthorYEAR[a-z]>`), cache `references/<id>/` in this repo with the EO layout (source.pdf, source.json, text.md with page markers, figures/); added to the schema at retrieval time (S7), not before | one id scheme per corpus |
| D128 | Parallel streams: one subagent per source lane in S1, one per class group in S3-S4, at most 10 at once; arXiv and PDF downloads have a single owner | parallel-streams feedback; rate limits |
| D129 | Inspection point after S6 (selection + audit + retrieval plan) before bulk PDF downloads | rule: ask before bulk runs on rate-limited sites |

## Budget (D120)

| group | class | rows now | budget |
|---|---|---|---|
| G1 fiber / free-space coupling | fiber_chip_coupler (grating, edge, PWB) | 122 | 60 |
| | micro_optics | 21 | 35 |
| | fiber_interface | 17 | 30 |
| | free_space_emitter | 0 | 40 |
| G2 on-chip passives | splitter | 37 | 50 |
| | crossing | 0 | 30 |
| | mode_converter | 15 | 35 |
| | polarization | 3 | 45 |
| G3 resonators, filters, WDM | resonator | 57 | 60 |
| | wdm | 21 | 80 |
| | reflector | 5 | 30 |
| G4 tuning, switching, nonreciprocal | phase_shifter | 25 | 60 |
| | switch_fabric | 10 | 45 |
| | nonreciprocal | 1 | 30 |
| G5 detectors | photodetector | 38 | 70 |
| G6 sources and gain | laser | 61 | 90 |
| | amplifier | 6 | 45 |
| | frequency_converter | 1 | 30 |
| G7 platform and chip-chip | waveguide_platform | 100 | 60 |
| | chip_chip_coupler | 14 | 40 |
| reserve | curator benchmark / record picks | | 35 |
| total | | 554 | 1000 |

## Source lanes (S1)

| lane | content | API |
|---|---|---|
| L1 journals | Optica, Optics Express, Optics Letters, Photonics Research, APL Photonics, Optical Materials Express, Advanced Photonics (+ Nexus), Chinese Optics Letters, JLT, PTL, JSTQE, IEEE Photonics Journal, IEEE JQE, Nature Photonics, Nature, Science, Nature Communications / Science Advances / APL / Scientific Reports (optics subfield filter), Light: Sci. Appl., ACS Photonics, Laser Photonics Rev., Nanophotonics, Opto-Electron. Adv., eLight, PhotoniX, npj Nanophotonics; 2016-2026 | OpenAlex filter lists (Crossref fallback) |
| L2 conferences | OFC 2016-2025, ECOC, CLEO, IEEE GFP, IEEE IPC, ECIO, ACP, CLEO-PR, IEDM / VLSI photonics papers | OpenAlex sources + Crossref by DOI prefix |
| L3 preprints | arXiv physics.optics (+ app-ph) 2018-2026 via OpenAlex arXiv source with subfield filter | OpenAlex |
| L4 seeds and snowball | taxonomy section 5 seeds, blog harvest OA rows, EO candidates with component content; per class 2-4 recent reviews -> reference lists (OpenAlex singleton gets, free) and benchmark / record papers | OpenAlex gets, Crossref |

## TODO

- [x] S0. Read sibling pipelines; probe APIs; shared client `litfetch.py`; this plan.
- [x] S1. Lanes L1-L4 (subagents) -> `cache/literature/pool/*.jsonl` (one normalized record per work) + lane reports.
- [x] S2. Merge + dedupe + known-id exclusion + regex prefilter (`config/literature/buckets.yaml`), per-class caps ~200.
- [x] S3. LLM scoring by class group (subagents, batches of ~150).
- [x] S4. Curation per class group: benchmark / record coverage, subtype and platform gaps, overrides with reasons.
- [x] S5. Selection script -> `data/_staging/literature/cache_list.csv` + triage report.
- [x] S6. Fresh-context audit of the selection; corrections recorded.
- [ ] Inspection point (D129): retrieval plan, manual-download list (written; waiting for review).
- [x] Increment harvest: Nature Communications 2016-2021, Science Advances, Applied Physics Letters, Scientific Reports 2016-2026 (2026-10-23 UTC, 14,898 records, $0.0103), S2 rerun, delta batches G1_b010 .. G7_b006 (281 records).
- [x] Increment scoring: score the 7 delta batches, then the S5 select delta (D230-D232; `data/_staging/literature/increment_delta.md`).
- [ ] S7. Retrieval (OA, single owner, pilot then escalate), extraction, registry corpus `lit`.
- [ ] S8. Distill batches with the pic-component-distill skill + audits.

## Questions for Wentao

- Q1. OpenAlex free key: the packaging atlas has one in its `.env`; this session was not permitted to read it. To use
  it here, export `OPENALEX_API_KEY` in the shell that runs the harvest or copy it into this repo's git-ignored `.env`.
  Without it the harvest stays under the shared free budget (filter-only lists), which is enough but slower.

## Progress

- 2026-10-21 22:30 UTC: S0 done. Probes: OpenAlex search $0.001, filter-only list $0.0001 (200 records with abstracts),
  singleton get $0; arXiv and Crossref reachable without identifiers.
- 2026-10-21 22:40 UTC: S1 lanes L1-L4 and the S2 builder dispatched (5 subagents, own files each; shared rules in
  the session scratchpad `common.md`).
- L3 arXiv done: 40,594 records (physics.optics 36,927 incl. cross-lists, 2,878 (2018) to 5,160 (2025) per year;
  app-ph / quant-ph keyword-restricted 3,667), 233 requests, all HTTP 200, no breaker, OpenAlex $0. Every month
  window matched opensearch:totalResults; one month cross-checked against the arXiv listing page (327 / 327 ids).
  20,209 records carry the journal DOI (dedupe in S2). Report: `research/2026-10-21-lit-lane-arxiv.md`.
- S2 builder done (no network): `config/literature/buckets.yaml` (20 classes, title-strong / abstract-weak regexes,
  14 global exclusions, 17 platform regexes), `scripts/lit_prefilter.py` (merge / prefilter / sample),
  `scripts/lit_make_score_batches.py`, 11 tests; full suite 125 pass, mypy strict clean. Trial on the partial pool
  (95,161 records -> 91,731 works, 3,426 duplicates merged, 222 known works excluded, 19,952 class candidates, 6,867
  kept for scoring); thin candidate classes: chip_chip_coupler 49, crossing 37 (seed lane expected to help). Stats:
  `data/_staging/literature/prefilter_stats.md`. Batches are written only after the lanes finish.

- L1 journals partial (22:38-23:07 UTC): 29 venues resolved, dry-run 131,861 works / 825 pages / ~$0.083; harvested
  2022-2026 of Optica, OE, OL, PRJ, APL Photonics and JLT 2024-2026 (33,191 records, every unit = meta.count,
  abstracts 97.2 %), then stopped at the shared cap ($0.0729 that day). Broad journals filtered by 20 OpenAlex
  photonics topics (487,340 -> 18,082; recall 134 / 134 EO-atlas journal papers). Issues: cursor paging returns 401
  without a key (page=N used, fine up to 10k per unit); newest-year IEEE early-access items lack abstracts (JLT 2026:
  459 / 930); Nanophotonics 2019 has 30 works in OpenAlex (Crossref fallback); Science drops after 2022 under the
  topic filter (not investigated). Resume queued by the coordinator to start 00:01 UTC 2026-10-22 (core journals
  2022-2026, then 2016-2021, then the rest). Report: `research/2026-10-21-lit-lane-journals.md`.
- 2026-10-22 00:01-00:03 UTC: the queued journal resume crashed three times on HTTP 200 responses with truncated JSON
  bodies (OpenAlex, right after the day rollover). Fix: `litfetch.get_json` retries a truncated body up to 4 times
  with 15 / 30 / 45 s pauses (each retry is a normal rate-limited request); resume restarted 00:06 UTC.
- L2 conferences done: 49,295 records (OFC, CLEO, ECOC, GFP / SiPhotonics, IPC, Advanced Photonics Congress (IPR),
  ACP, CLEO-PR, IEDM, VLSI; 2016-2025; OFC 2026 excluded), abstracts 98.8 %, first / last-author affiliations
  58.9 %, OA 5.2 %. Routes: Optica 2020-2025 via Crossref (100 % abstracts), Optica 2016-2019 and IEEE via OpenAlex
  source lists, IET / missing-source years via Crossref + OpenAlex DOI enrichment. Not indexed anywhere reachable:
  ECOC 2022 and 2024, ACP 2019, GFP 2020 and 2022, VLSI 2025, ECIO (dropped). Lane OpenAlex cost ~$0.040. Optica
  Crossref records (18,419) carry no affiliations: enrich only the prefiltered set later (DOI batches).
  Report: `research/2026-10-21-lit-lane-conferences.md`.
- L4 seeds done: 11,641 rows / 9,391 unique works: 554 local seeds (494 blog, 32 taxonomy, 45 EO non-modulator
  candidates; 6 unresolved listed), 71 reviews (2-7 per class, `config/literature/seed_reviews.yaml`), 10,774 works
  referenced by them (1836-2025), 242 forward citations for reflector (only class with all reviews < 2021). Reviews
  found mainly as review-titled, most-cited 2018-2026 citers of 49 landmark papers (filter-only); 14 OpenAlex
  searches. Weak review coverage: Ge PD, AWG / echelle, Er amplifiers, WSS; reflector and crossing 2 reviews each.
  Lane OpenAlex cost ~$0.033. Report: `research/2026-10-21-lit-lane-seeds.md`.
- 2026-10-22 00:06-00:40 UTC: journal resume finished all core and most secondary journals, then stopped at the cap
  ($0.075). Not yet harvested: Nature Communications 2016-2021, Science Advances, Applied Physics Letters,
  Scientific Reports (broad journals, topic-filtered): increment after the next UTC rollover (scoring batches are
  append-only). One HTTP 504 crashed a pass; the next pass resumed it.
- 00:44 UTC: S2 full run: 218,503 records / 576 files -> 202,302 works (16,148 duplicates merged), 405 known,
  46,958 class candidates, 7,457 kept for scoring -> 53 batches (G1 9, G2 8, G3 10, G4 8, G5 4, G6 9, G7 5).
  `scripts/lit_check_scores.py` validates outputs (uid coverage, enums, score = clamp of the rubric sum).
- S3 pilot: G1_b001 and G6_b001 (Sonnet scorers, task template in the session scratchpad), checked before fan-out.
  Pilot fix: never lower a score for a suspected duplicate (version families are merged in S5).
- S3 done (01:00-02:10 UTC, 26 Sonnet scorers, <= 10 at once): 53 / 53 batches pass `lit_check_scores.py`;
  7,457 records: score 8-10 4,616, 6-7 587, 4-5 286, 0-3 1,968; out_of_scope 1,117, reviews 56,
  EO-modulator-main 136 (listed for the EO atlas). Rubric clarifications added mid-run (scoring_prompt.md): scope of
  photodetectors (material-science surface detectors out), fiber sensors / AR combiners out, THz / mm-wave out,
  fiber-only passive parts in. Earlier batches scored before a clarification are reconciled by the curators
  (notes in the session scratchpad `curation_notes.md`: THz, fiber mode-selective parts, WSS modules, EMLs, PPLN
  waveguides). Score saturation: dedicated measured papers mostly land at 8-9, so ties inside a class are broken by
  OA, industry, record claim, recency, citations / year, and the curators.
- `scripts/lit_select.py` (S5): eligibility, version families (title token Jaccard >= 0.6 + difflib >= 0.85 + shared
  first / last author surname; journal > conference > preprint, then OA), per-class fill (curator picks, subtype
  floors, platform floors, rank) under the senior-author cap (4) and the paywalled share (20 % of the class budget,
  score >= 8), reserve = 35 + unfilled class budget, filled by curator overflow picks and then the best remaining
  works (at most +50 % of a class budget). Writes per-class curation inputs (`cache/literature/curation_inputs/`).
- S4 curation: one Opus curator per group G1-G7 writes `config/literature/curation/<group>.yaml` (picks, drops,
  reclass, verified adds).

| # | Decision | Rationale |
|---|---|---|
| D135 | Rescue pass: per class the most-cited title-hit prefilter candidates that the caps cut (ceil(0.6 x budget), 579 works) are scored as group G9 with the same rubric | curators G1 / G2 / G3 / G5 found landmark papers (Q, GC, PSR, SNSPD benchmarks) beyond the caps |
| D136 | Curator picks override a scorer's out_of_scope / review flag; a curator-picked version heads its version family; adds are resolved by `scripts/lit_curator_adds.py` (merged pool first, else a free OpenAlex singleton get; title match >= 0.9 required) and become picks | curator reports G2, G5 |
| D137 | Version families tightened: token Jaccard >= 0.7, difflib >= 0.9, |year difference| <= 2, shared first / last author surname; the senior-author cap (4 per class) also binds reserve fills | false merge MoSi-SNSPD-on-SiN vs NbN-on-Ta2O5 (G5); Dai 6 wdm rows via reserve (G3) |
| D138 | Surface-normal grating mirrors (HCG, guided-mode resonance, epitaxial DBR stacks) are free-space parts, out of scope atlas-wide; InP-native waveguide PDs use photodetector.other until a subtype is added; fiber_chip_coupler.other (3D-printed out-of-plane couplers, tapered-fiber interfaces) to be added to the registry at ingestion | curator reports G3, G5, G1 |
| D139 | `known` = already ingested somewhere (this registry, EO papers, packaging cache, OFC 2026); EO-atlas candidates the EO atlas never ingested stay eligible. Picks also override `eo_modulator_main`. Senior-author cap keys on the full normalized name, not the surname | curator report G4 (two Nature Photonics isolators listed only as EO candidates; SAW isolator flagged as a modulator; surname collisions such as Wu) |
| D140 | Conflicts between curator picks and audit drops are ruled by the coordinator: MEMS crossconnect and LCoS WSS modules stay in scope (registry subtypes switch_fabric.mems / .wss); Kittlaus 2021 and Lira 2012 isolators kept; discrete InGaAs SPAD, the Ayar Labs link paper and a supercontinuum paper with a side loss number dropped. Rulings recorded in the applied copy `config/literature/curation/audit_b.yaml` (auditor original kept in staging) | audit B vs G4 / G5 / G6 / G7 |
| D134 | Seed tiers (amends D131): tier A = local seeds (D131 treatment); tier B = review references / forward citations: +1 (+1 more when cited by >= 2 reviews or classes), title class hit required, counts toward the cap, pre-2005 needs an experimental / quantitative cue; reviews themselves are not scored | 10.8k reference seeds would overflow the caps under D131 |
| D130 | Per-class scoring cap `max(250, 8 x budget)` (not 6x): 6x tops out at 5,890, below the 6-9k scoring target | S2 trial |
| D131 | Seeds get +2, rank first and are kept beyond the cap; a seed's `seed_class` stands in when no regex fires | seeds are curated evidence |
| D132 | Rule-score floors: title hit >= 3, abstract-only hit >= 5; arXiv app-ph / quant-ph-only records need a title hit | precision on arXiv noise |
| D133 | Best class: title hit over abstract hit, specific subtype over `other`; S5 re-checks `known_in` and prefilter status at selection time (batches are append-only) | stable batches over a growing pool |
- S4 curation done (02:15-02:40 UTC): G1-G7 YAMLs, 101 verified adds (all resolved, title match >= 0.9),
  ~150 drops, picks 330 incl. rescues of wrongly out_of_scope rows. Fixes made from curator reports: D136, D137,
  D139. Rescue pass D135: 579 works (G9_b001-b004) scored, 57 / 57 batches valid.
- S6 audits (fresh context, 2): A (correctness, `audits/2026-10-22-lit-selection-audit-a.md`): sample of 160
  rows ok 87.5 %, imprecise 11.2 %, wrong 1.2 % (both curator adds, simulation-only); 0 known, 0 identifier
  mismatches in 25 checks, 1 version pair; 8 drops / 5 reclass applied. B (coverage,
  `audits/2026-10-22-lit-selection-audit-b.md`): passive classes solid; laser / resonator weakest (scored 5.6 % /
  7.2 % of their candidates); 18 picks / 31 drops / 13 adds proposed (1 add rejected by the title check: wrong DOI),
  4 drops overruled (D140). Applied copies: `config/literature/curation/audit_a.yaml`, `audit_b.yaml`.
- Final selection (`data/_staging/literature/cache_list.csv`, triage report alongside): 1000 papers, OA 818,
  paywalled 182; every class at or above budget except chip_chip_coupler 39 / 40; reasons rank 410, curator 330,
  subtype floor 224, reserve 36. Years 2000-2026 (pre-2016: ~150, landmark seeds). EO-modulator-main works for the
  EO atlas: `data/_staging/literature/eo_atlas_candidates.csv` (137).
- Retrieval routes: arXiv 170; OA publisher 648 (Optica ~387 without an arXiv copy, IEEE ~126, Nature ~46, Wiley /
  AIP / De Gruyter / ACS ~66); paywalled 182 (`data/_staging/literature/manual_downloads.md`, save as
  `references/_inbox/<paper_id>.pdf`).
- Checks 02:47 UTC: ruff, mypy (62 files) clean; validate_db 0 errors; pytest 131 pass, 2 fail in
  test_adapters / test_people (inventory counts and people sync against the sibling EO atlas, which changed after
  those tests were written; no tracked file was modified in this session).
- 2026-10-23 04:58-05:09 UTC, broad-journal increment (L1 method: OpenAlex filter-only venue-year lists, 20-topic
  filter, page=N, no search, shared `litfetch` client, no key). OpenAlex spend that UTC day before the run: $0;
  after: $0.0103 (103 requests, all HTTP 200: 8 group_by incl. a 4-request dry-run, 95 list pages); nothing remains
  for these venues. Every unit = meta.count = group_by count. Logs: `logs/lit_harvest_openalex_journals_20261022T215841.*`
  (dry-run), `..._20261022T215852.*` (harvest), `logs/litfetch_2026-10-23.jsonl`.

| venue | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 | total | abstract | OA |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Nature Communications | 200 | 235 | 235 | 235 | 253 | 268 | (done) | (done) | (done) | (done) | (done) | 1,426 | 1,424 | 100 % |
| Science Advances | 36 | 45 | 61 | 57 | 75 | 81 | 96 | 76 | 107 | 173 | 111 | 918 | 917 | 100 % |
| Applied Physics Letters | 806 | 713 | 596 | 491 | 489 | 582 | 465 | 582 | 613 | 568 | 517 | 6,422 | 6,329 | 38.7 % |
| Scientific Reports | 988 | 976 | 558 | 547 | 453 | 420 | 428 | 357 | 416 | 586 | 403 | 6,132 | 6,132 | 100 % |
| total | | | | | | | | | | | | 14,898 | 14,802 | |

  Nature Communications 2022-2026 now counts 1,940 in OpenAlex vs 1,937 harvested 2026-10-22 (files not refreshed).
- S2 rerun 05:04 UTC (backup of the previous outputs first: `cache/literature/backup/s2_before_increment_20261023T050406Z.zip`):
  pool 218,503 -> 233,401 records (615 files); works 202,302 -> 215,863 (13,563 new works, 1,335 records merged into
  existing works, 24 of them already-scored arXiv / conference records now headed by the journal DOI); known 405 ->
  408; class candidates 46,958 -> 49,708 (2,753 new: APL 1,357, Sci Rep 1,070, Nat Commun 202, Sci Adv 124; laser
  719, resonator 521, photodetector 361); kept for scoring 7,457 -> 7,461. The per-class caps (D130) bind for 18 / 20
  classes, so new works enter only by outranking incumbents: 277 new works kept (APL 151, Sci Rep 116, Nat Commun 8,
  Sci Adv 2) and 277 earlier-kept, already-scored works fell below the caps (they stay scored and eligible in S5);
  4 existing works became candidates through the journal version's abstract. Few Nat Commun works pass the cap:
  the cap rank uses rule score, title hit, numbers in title + abstract and recency, which their qualitative
  2016-2021 abstracts lose (observation, not changed).
- Delta batches 05:08 UTC (`scripts/lit_make_score_batches.py --flush`): G1_b010 49, G2_b009 39, G3_b011 45,
  G4_b009 45, G5_b005 32, G6_b010 60, G7_b006 11 = 281 records (APL 152, Sci Rep 118, Nat Commun 9, Sci Adv 2).
  SHA-256 of all 115 existing files in `cache/literature/scoring/` identical before / after except `manifest.json`,
  whose 53 earlier entries are unchanged; appended: G9_b001 .. b004 (recovered from the rescue files, which had no
  manifest entry) and the 7 new batches (64 entries, 0 duplicate uids). Not scored.
- Fixes for the rerun (ruff, mypy, 12 prefilter tests pass):

| # | Decision | Rationale |
|---|---|---|
| D148 | `lit_prefilter.build_known` skips sources.csv corpus `lit` | the 64 S7-registered papers would otherwise be `known` and drop out of a later S5 run |
| D149 | `lit_select` keeps a scored work under its scored uid when a later harvest merges in a version that heads the record (alias in `alt_uids`) | without it a S5 rerun drops 2 selected papers (isichenko2023 -> Sci Rep 2024, yulaev2024 -> APL 2024) |

- Expected S5 changes once the delta is scored (checked with a scratch copy of `lit_select.py` writing outside the
  repo; real outputs untouched): with only D148 / D149 and no new scores, 999 / 1000 uids unchanged, 996 rows
  identical except rank; ronn2019 (amplifier, rank) displaced by 10.1364/ofc.2022.w3j.6, now merged with its Sci
  Rep 2021 version; isichenko2023 and yulaev2024 now carry journal venue metadata; paper_id shifts
  isichenko2023 -> isichenko2024 (journal year) and gao2021 -> gao2021a (COL LN microring, collision with the new
  gao2021). Both shifted ids are in the retrieval queue (days 2026-10-25, 2026-10-23): pin paper_ids of queued /
  cached rows before re-running S5.

## S7 retrieval plan (proposed, waits for review)

1. Registry: corpus `lit` (D127), `references/<paper_id>/` with the EO layout; source PDFs local-only
   (`references/*/source.pdf` git-ignored), `source.json` committed; bronze OA = restricted_local_only.
2. arXiv first (170 + journal-matched preprints): single owner, >= 5 s + jitter, breaker (EO `fetch_source.py`
   pattern); pilot 10, then 20 / 40 / rest.
3. Optica OA (~387): Optica flagged this user's traffic before. Options: (a) very slow headless fetch of the
   published PDF (>= 60-120 s spacing, <= 30 per 2 h, stop on any challenge); (b) the user's logged-in browser via a
   queue file; (c) look for arXiv versions first (title match in the 40.6k arXiv pool) and fetch only the rest.
4. IEEE OA (~126): Xplore WAF blocks headless; headed browser with the packaging-atlas `ieee_fetch.py` pattern
   (60-120 s spacing, <= 60 per 2 h) or manual.
5. Nature / Wiley / ACS / AIP / De Gruyter OA (~112): publisher PDF links, >= 10 s spacing per host.
6. Extraction: PyMuPDF `text.md` with `<!-- page N -->`, figures/ (EO `extract_source.py`), then distill batches of
   10 with the pic-component-distill skill, an audit per batch, merge.

## User answers (2026-10-22)

| # | Answer / decision | Applied as |
|---|---|---|
| D141 | Start retrieval; pace ~100 papers per day over 10 days | `data/_staging/literature/retrieval_queue.csv` + `retrieval_schedule.md` (days 2026-10-22 .. 2026-10-31, class-balanced per day) |
| D142 | Optica papers: arXiv copy when one exists, otherwise the user's local Playwright Chromium / Firefox sessions | queue route `arxiv` first (local pool + arXiv title search); `optica_browser` via `scripts/lit_fetch_browser.py --site optica` (headed persistent profile, 60-120 s spacing, <= 20 per session) |
| D143 | IEEE: reuse the packaging-atlas fetcher; the user logs in once per session of 30 papers | `scripts/lit_fetch_browser.py --site ieee --login / --run --session S` (adapted from advanced-packaging-atlas `ieee_fetch.py`) |
| D144 | OpenAlex key: the user obtained one before; look it up in local agent logs | the lookup was refused by the permission classifier (credential exploration); `litfetch` now reads `OPENALEX_API_KEY` from the repo's git-ignored `.env` (cap 0.9 USD / day with a key); waiting for the user to place it there |
| D146 | Non-OA Optica papers: prefer the IEEE Xplore copy (co-published OFC / CLEO / ACP / IPR proceedings, e.g. 10.1364/ACPC.2021.T4A.130 = Xplore 9738431) over the Optica site; IEEE institutional access is easier and the IEEE fetcher works | R1: Crossref title lookup with prefix 10.1109 (similarity >= 0.93, shared author, year +-1), columns ieee_doi / ieee_match_score, route ieee_browser; identity stays the Optica DOI. Preference: arXiv, then IEEE twin (paywalled Optica), then optica_browser |
| D145 | Commit like the previous atlas projects | commit a112b7e (one-line message, main, not pushed) |

- 2026-10-22: fetch extra `fetch` = playwright 1.64.0 + pymupdf (as in the packaging atlas); `.gitignore` keeps
  `references/*/*.pdf`, `references/*/arxiv/`, `references/*/supplement/` local. Streams dispatched: R1 queue +
  arXiv matching + schedule, R2 OA fetcher + extraction + `lit` corpus registration + inbox, R3 browser fetcher.

## S7 retrieval progress

- 2026-10-22 00:00-01:05 local: streams R1-R3 built `scripts/lit_build_queue.py` (queue + 10-day schedule;
  arXiv copies: local pool + 814 arXiv title queries -> 24 extra arXiv routes, most selected Optica / IEEE device
  papers have no arXiv copy (spot-checked with looser queries); IEEE twins via Crossref: 2), `lit_fetch_oa.py`
  (arXiv + repositories), `lit_fetch_browser.py` (headed Playwright persistent profiles: optica, ieee incl. Xplore
  title search `ieee_search` (D146), publisher), `lit_extract.py` (PyMuPDF text.md + figures + source.json),
  `lit_ingest_inbox.py`, `lit_register_sources.py` (`lit` corpus rows in sources.csv; schema enum + source_id
  pattern), `lit_daily.sh` (daily runbook). Routes: arxiv 194, optica_browser 423, ieee_browser 202,
  publisher_browser 81, ieee_search 23, oa_publisher 23, manual 54; 100 per day, days 2026-10-22 .. 2026-10-31.
- Publisher behaviour observed (no retries, breakers armed): plain fetch blocked by Nature (JS challenge), Wiley,
  AIP (403), De Gruyter (AWS WAF), PubMed Central (captcha), Elsevier linkinghub (TLS verify failure). Headed browser:
  Nature ok; Wiley and AIP 403 on the landing page; Optica OA ok (no challenge in 30+ requests), subscription and
  some mislabeled-OA Optica papers `no_access` without an institutional login. Decision D147: Wiley, AIP, De
  Gruyter rows go to the manual list unless a logged-in browser session clears them; HTTP 403 stays a stop signal.
- Day 1 (2026-10-22): arXiv 24 ok (incl. pilot); repositories 1 ok, 7 blocked / not PDF; Optica session 1: 11 ok,
  4 no_access (+ 2 smoke ok, 2 no_access); publisher session: 5 ok, 3 blocked; IEEE session not run: the login
  window timed out (30 min) without a sign-in. Cached and extracted: 43 papers; `lit:` rows in sources.csv 43;
  validate_db 0 errors.
- Next per day: `zsh scripts/lit_daily.sh <day>` in tmux, then the IEEE session with the user's login. Pending: the
  user's IEEE sign-in (day 1 session), an optional Optica institutional sign-in (`--site optica --login`) to recover
  `no_access` rows, OPENALEX_API_KEY in `.env` for the broad-journal increment, manual downloads
  (`data/_staging/literature/manual_downloads.md` to be regenerated from the queue's manual + blocked rows).
- 2026-10-22 09:10-09:51 local, IEEE day-1 session (user signed in): first attempt stopped on a false-positive
  challenge (the word `captcha` in an Xplore CSS class; the Angular article page has no citation_* meta): detection
  fixed (Xplore document markers count as article pages, captcha only as a widget signature), test added, breaker
  archived as `logs/lit_browser_blocked_ieee_20261022T091125_false_positive.json`. Second attempt: institutional
  session cookies do not survive a separate --login window, so `--run --wait-login` signs in in the same window
  (runbook updated). Result: 21 / 22 ok (incl. xu2023a via Xplore title search, similarity 1.0), 1 no_ieee_copy
  (yokokawa2022, OFC 2022 -> optica_browser fallback). Day 1 total: 64 papers cached and registered.
- 2026-10-22 22:10 PDT: `scripts/lit_manual_list.py` (new) regenerated `data/_staging/literature/manual_downloads.md`
  from the queue and the fetch status log (cached papers left out): 97 rows = 54 route manual, 34 D147 hosts (Wiley
  21, De Gruyter 13), 9 failed day-1 attempts (optica no_access 5, oa_publisher blocked 2, ieee_search no_access 1,
  no_ieee_copy 1). Re-run it after each retrieval day. S8 distillation moved to DevLog-007.

## Increment S5 delta (2026-10-22 local, coordinator rules)

The 7 delta batches (G1_b010 .. G7_b006, 281 records) are scored (`lit_check_scores.py`: 7 ok, 0 errors). Selection
delta under the coordinator's rules, recorded as decisions:

| # | Decision | Rationale |
|---|---|---|
| D230 | Identity pinning: `lit_select.py` reads the previous `cache_list.csv` as a pin table; a selected work whose uid (or a version-family member's uid) is in it keeps that row's paper_id, and every previous paper_id is reserved, so a new work never takes a retired or existing id | fixes isichenko2023 -> isichenko2024 and gao2021 -> gao2021a; queue, status log and `references/<paper_id>/` key on paper_id |
| D231 | Budget stays 1000. Frozen (never displaced): cached papers (`references/<paper_id>/source.pdf`), every day-1 and day-2 queue row, curator picks. A work outside the previous list enters only by displacing a not-yet-retrieved, non-curator incumbent of the same primary class on days 3-10, and only when the unconstrained `selection.yaml` rules (rank, subtype / platform floors, senior-author cap, paywalled share) select it and drop that incumbent; the final list is re-checked for the senior-author cap and the paywalled share | retrieval in progress; no churn of fetched or scheduled-today work |
| D232 | Procedure: zip backup of cache_list, queue, schedule, manual list, triage report into `cache/literature/backup/`; `lit_select.py --delta` dry-run writes `increment_delta.md` (entering / displaced, class, score, reason); apply; `lit_build_queue.py --delta` keeps every retained queue row verbatim and gives incoming rows the displaced rows' day slots (route by the normal matching logic; arXiv API <= ~50 queries via `litfetch`, stop on 403/429); verify day 1-2 rows unchanged, total 1000, per-class counts; regenerate the manual list | auditable, reversible |

Plan: (1) pin table + `--delta` mode in `lit_select.py`, test; (2) `--delta` mode in `lit_build_queue.py`, test;
(3) backup, dry-run, delta report; (4) apply, queue rebuild, verification, manual list; (5) checks.

Progress (2026-10-22 22:20-22:28 PDT):

- Code: `lit_select.py` pin table + `assign_paper_ids` (D230), `--delta` / `delta_select` / `increment_delta.md`
  writer (D231); `lit_build_queue.py --delta` / `delta_slots` (D232). Tests: `tests/test_lit_select.py` (2, new),
  `test_delta_slots_keeps_rows_and_hands_over_day_slots` in `tests/test_lit_build_queue.py`.
- Backup: `cache/literature/backup/s5_before_increment_delta_20261023T052420Z.zip` (cache_list, queue, schedule,
  manual list, triage report, eo_atlas_candidates).
- Dry-run (`logs/lit_select_20261022T222239.*`) and apply (`..._20261022T222426.*`) gave the same delta: unconstrained
  run on 8,317 scored records picks 16 works outside the previous list; 10 entered, 6 blocked (no displaceable
  same-class incumbent: the class's dropped incumbents are cached, on day 2, or absent); 16 previous rows dropped by
  the unconstrained run: 10 displaced, 4 kept as frozen (ronn2019, heim2025, meng2023 cached; wu2025 day 2), 2
  switch_fabric rows kept (no switch_fabric entrant). Entering: all OA, 8 Scientific Reports, 1 Nature
  Communications, 1 APL (holl2025); list in `increment_delta.md`. 990 / 990 kept uids keep their paper_id
  (isichenko2023, gao2021 unchanged); kept rows changed only rank, selection_reason (5, rule relabels) and journal
  metadata of isichenko2023 / yulaev2024 (D149). Per-class counts identical to the previous list; OA 818.
- Queue (`logs/lit_build_queue_20261022T222445.*`): 9 arXiv title queries via `litfetch` (all HTTP 200, 0 hits);
  yanikgonul2021 has a given arXiv id. 990 rows byte-identical (day 1-2 diff empty; full diff = the 10 replaced
  lines); 100 per day kept. Routes: arxiv 195, oa_publisher 23, publisher_browser 87, optica_browser 418,
  ieee_browser 200, ieee_search 23, manual 54. Manual list regenerated: 96 rows (zhou2025 out, moser2011 ->
  holl2025).
- Checks: ruff clean, mypy 76 files clean, pytest 213 pass, validate_db 0 errors / 18 registry warnings
  (`logs/s5_delta_checks_20261022T222555.log`).

| # | Decision | Rationale |
|---|---|---|
| D233 | Coordinator override: holl2025 (10.1063/5.0293416, optically pumped 2 um GaSb VECSEL) dropped as not an integrated-photonics component, via a curation drop in `config/literature/curation/increment.yaml` (replayable); hamaguchi2018 kept | coordinator review of the increment delta |

- 2026-10-22 22:29 PDT, D233 applied with the same procedure: backup
  `cache/literature/backup/s5_before_d233_20261023T052856Z.zip`; dry-run and apply identical (1 swap: moser2011
  re-enters on the laser.vcsel floor, displacing holl2025; paper_id moser2011 regenerated unchanged); queue rebuild
  without network (moser2011 arXiv lookup cached): 999 rows byte-identical, day 1-2 diff empty, the moser2011 row is
  byte-identical to its pre-increment row. Net increment vs HEAD: 9 swaps (18 diff lines). Routes: arxiv 195,
  oa_publisher 23, publisher_browser 87, optica_browser 418, ieee_browser 200, ieee_search 23, manual 54. Manual
  list 96 rows. `increment_delta.md` holds the first delta plus a D233 section. `write_delta` now marks an ineligible
  previous row as displaced when it was.
- 2026-10-23 00:07-01:27 PDT, day 2 automated part (tmux `lit_day2`, log `logs/lit_daily_day2_20261023T000710.log`):
  arXiv / repositories 18 ok (1 blocked: researching.cn TLS verify failure, breaker armed; 1 not_pdf), Optica browser
  sessions + publisher session: 34 ok in total across routes, 11 no_access; new breaker: pubs.acs.org (challenge 403 on
  PDF re-request, manual reset only); Wiley / De Gruyter skipped by their D147 breakers. Extraction + registration: `lit`
  corpus 116 sources (+52), validate_db 0 errors. Manual list regenerated: 110 rows. IEEE day-2 session (21 papers)
  waits for the user's sign-in (`--site ieee --run --day 2 --wait-login`). Distill batches lit_07-lit_11 (DevLog-007).
