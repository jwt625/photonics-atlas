# DevLog-019: Benchmark-citation snowball (next caching round from comparison tables and trend plots)

| | |
|---|---|
| Date | 2026-11-15 |
| Status | B1-B7a done; list `data/_staging/literature/bench_cache_list.csv` (1249 new works, 813 above the cut) queued as days 200-210; days 201-202 cached and ingested (day 201: 95 papers, DevLog-007 D577-D600; day 202: 97 papers, D601-D627); day 203 cached 88 papers and ingested in two halves (half A 44, D631-D645; half B 44, D646-D659); day 204 cached 33 papers (IEEE 30, open routes 3; Optica not run, breaker armed) and ingested (D660-D671); days 205-210 pending |
| Scope | Find cached papers whose authors compiled a comparison table or a trend / benchmark plot of other works, extract the cited works, dedup, resolve and rank them into the next cache list (~1200 new papers, about 2x the `lit` corpus) |
| Related | DevLog-006 (scouting, retrieval, access rules), DevLog-007 (distill), `src/photonics_atlas/litfetch.py` (rate-limited client), `src/photonics_atlas/litpool.py` (norm_doi / norm_title) |
| Decisions | D1200-D1229 reserved for this DevLog |

## Request (2026-11-15, Wentao)

"Inspect currently extracted papers, and i want you to do the following for curating the list for next round of journals:
1. inspect and find currently cached and ingested papers that have a comparison table or trend graph, that contains
metrics extracted by the authors of those papers about similar components in other papers they cited or included in
the benchmark table or evolution plot. 2. extract those papers, and dedup between themselves as well as existing
papers 3. curate a list of papers to be cached next from these papers. [...] Prioritize over open access journals, and
ieee journals/conference papers. Take notes in new devlog as usual [...] Use subagents as needed. Target is to expand
current library by roughly 2x."

## Starting point (inspected 2026-11-15)

- `lit` corpus: 1198 papers cached in `references/<id>/` (source.pdf, text.md with page markers, figures/ with page
  renders and figures.json captions); `sources.csv` corpora: lit 1198, ofc2026 830, pk 299, lin 282, eo 235, blog
  128, web 57.
- Sibling text with local copies: EO atlas `../eo-modulator-atlas/references/` (236 dirs, same layout incl. page
  renders); OFC 2026 `../PlayGround/20260320_OFC/extracted_text/` (677 Marker .md, no page images on disk).
- Rough prevalence (grep, `lit` only): 383 / 1198 texts contain comparison-table or state-of-the-art wording, 890
  contain "this work". PyMuPDF flattens table cells one per line but keeps `[n]` tags next to row labels.
- Dedup material on disk: `sources.csv` (all corpora), `data/_staging/literature/cache_list.csv` (1307 rows incl.
  pending), OpenAlex pool `cache/literature/merged.jsonl` (215,863 records with OA status, venue, abstract),
  EO atlas `data/papers.csv`.

## Owner answers (2026-11-15)

1. Scan scope: `lit` + OFC 2026 + EO atlas (packaging atlas skipped).
2. Target: ~1200 new papers (lit corpus ~1198 -> ~2400); the ranked list runs longer, with a cut line at ~1200.
3. EO modulator papers: separate EO-atlas candidate list, not counted in the lit list, deduped against the EO atlas.
4. Access: tier 1 = arXiv + OA journals (Optics Letters and Photonics Research stay excluded, earlier owner rule);
   tier 2 = IEEE journals and conferences; tier 3 = other paywalled (Nature non-OA, Wiley, ACS, Elsevier, Optica-only
   conference papers, OL), ranked below the cut line, flagged manual, promoted above it only when many benchmarks
   cite it.

## Decisions

| ID | Decision | Source |
|---|---|---|
| D1200 | Benchmark item = a table or figure in the citing paper that puts the paper's result next to values of other works with reference tags (comparison / state-of-the-art table, summary table in a review, trend or evolution plot, scatter of reported devices). Text-only mentions ("[12] reported 0.5 dB") are out | request |
| D1201 | Stages: B1 regex prefilter -> per-paper packets (candidate regions + reference section) -> B2 extraction subagents (text, plus page render for figures) -> B3 resolve cited refs to DOI / arXiv (DOI in string, pool title match, Crossref bibliographic query with verification) -> B4 dedup -> B5 enrich (pool, OpenAlex singleton gets) -> B6 classify and rank -> B7 fresh-context audit -> inspection point | coordinator |
| D1202 | Extraction agents also record the cited values per row (metric, value, unit as printed) in local staging; these are cross-check material for later distills, never atlas rows (distill skill rule 3) | coordinator default |
| D1203 | No year cutoff; pre-2000 cited works are flagged for the history lane | coordinator default |
| D1204 | Storage: packets, raw extraction JSONL and resolver caches in git-ignored `cache/literature/bench/`; committed: scripts, config, the final `data/_staging/literature/bench_cache_list.csv` (ids, title, venue, year, class, citing count, access tier, rationale) and the report | D126 pattern |
| D1206 | Trend plots with unlabelled points but caption / legend reference tags count: one item per listed reference, no values | coordinator, from b07 report (ji2024) |
| D1207 | A table whose caption says it compares reported / previous / literature / state-of-the-art works is a candidate without `[n]` tags (superscript and author-year citations) | coordinator, recall check |
| D1209 | Benchmark list joins the lit pipeline like the history stream: cache_list rows `selection_reason = benchmark_cite`, queue days 201+ (manual day 200), per-day caps per route; caching starts with open routes + IEEE | owner go 2026-11-15 + coordinator |
| D1208 | Any table caption containing compar* / summary / overview / survey is a candidate (no tags needed); agents reject own-design comparisons | coordinator, recall pass 2 |
| D1205 | Network: Crossref and OpenAlex only through `litfetch.py` (per-host lock, min interval, breaker, OpenAlex cost cap, generic UA); pilot 20 refs before the bulk resolve | rate-limit rules |

## TODO

- [x] B0. Inspect corpora, owner questions, this plan.
- [x] B1. Prefilter script `scripts/bench_prefilter.py` -> `cache/literature/bench/candidates.jsonl` + packets; stats.
- [x] B2. Extraction subagents in batches -> `cache/literature/bench/extract/*.jsonl`; pilot batch first, check, then fan out (<= 10 concurrent).
- [x] B3. Resolver `scripts/bench_resolve.py` (pilot, then bulk).
- [x] B4. Dedup against sources.csv, cache_list.csv, EO atlas papers.csv and within the set.
- [x] B5. Enrich access / venue / OA from pool and OpenAlex.
- [x] B6. Classify (component class, modulator -> EO side list) and rank; `bench_cache_list.csv` with a cut line at ~1200.
- [x] B7a. Fresh-context audit of the extraction (sample of 40 items, 25 no_benchmark papers).
- [ ] B7b. Audit of resolution and dedup (sample of resolved DOIs, in_library / new splits).
- [x] Owner: "cmt, and then start a new day's caching" (2026-11-15): commit 232066e; list queued (B8).
- [ ] B8. Days 201-210: open routes + IEEE per day; Optica OA-journal and publisher-browser sessions only on an explicit owner go.

## Progress

- 2026-11-15: B0 done (inspection above, owner answers recorded).
- 2026-11-15 B1: `scripts/bench_prefilter.py` (local reads only). Table candidate = "Table N" caption with a
  comparison keyword (or "this work" in the window) and >= 2 reference tags within -25 / +90 lines; figure candidate =
  caption-style "Fig. N" line whose caption points at other works (state of the art, reported, previous, literature,
  various / recent <devices>, by year, ...) or carries >= 2 tags with compar / versus; caption-less flattened or
  Markdown tables = a short "this work" line with >= 3 tags in -40 / +30 lines. Reference sections: heading variants
  (numbered, singular, Marker `<span>` / bold) plus a headingless fallback (first "1." in the back half followed by
  "2." and "3."); entries parsed as a monotone numbered run. Iterations: first pass 1340 figure regions at ~10 %
  precision (sample of 30) -> caption-style + other-works rule -> 296 figure regions (~20 % in a sample of 25; the
  agents reject the rest). Reference parsing 633 -> 1004 / 1198 lit papers after the heading fixes (the 108 lit
  papers left without a section are mostly pre-1980 history scans). Result: lit 369 / 1198 papers with candidates
  (642 regions), EO 85 / 233 (140), OFC 2026 97 / 677 (117); 551 packets, 5.9 MB; regions: table 518, figure 296,
  caption-less table 85. Spot check of 25 table captions: ~20 true comparison tables.
- 2026-11-15 B2 setup: brief `config/literature/bench_extract_brief.md`; pilot batch of 12 packets (4 lit tables,
  3 lit figure-only, 2 EO, 2 OFC, 1 caption-less) on one agent; the other 539 packets in 24 size-balanced batches
  (`cache/literature/bench/batches/b01..b24.txt`, <= 260 KB / 30 packets each).
- 2026-11-15 B2 pilot (12 packets, one agent, ~128k tokens): 9 ok / 3 no_benchmark, 87 items, 0 empty refs. Agent
  findings and fixes: tables cut by the fixed +90-line window -> window now ends at the next table caption, section
  heading or reference section (max 170 lines); smit2014 review Table 1 (31 rows, plain-number "References" column, no
  comparison keyword) missed -> a table with a "Ref." / "References" column header is accepted without keyword or
  tags; headingless fallback took numbered appendix sections as references (otterstrom2019) -> the fallback needs a
  year near the "1." entry and a parsed list is kept only when >= 50 % of entries carry a year (otterstrom2019 still
  has 3 bad leading entries; agents check entries); brief gained "Pilot rules" (out-of-window tables `region: null`,
  image-only tables read from the PNG, unlabelled trend plots give no items, `out_of_scope.pic` / `.fiber`, not-reported
  cells left out). Rerun: 570 packets (lit 391, EO 92, OFC 87), 6.6 MB; regions table 535, figure 296, caption-less 73.
  Remaining 559 packets in 26 batches (`b01..b26`, <= 28 packets / 260 KB); b01-b10 launched (10 concurrent).
- 2026-11-15 B3 pilot (`bench_resolve.py --limit 20`, then `--limit 40` over pilot + early batch output): 157 unique
  refs, 152 resolved (99 local title match, 52 verified Crossref, 1 printed arXiv), 5 unresolved (conference papers
  without Crossref records). Fix after the first pass: unquoted-title styles (IOP, Nature) verified by the candidate's
  title words (len > 3) appearing in the reference string (>= 85 %), method `crossref_title_in_ref`; JSONL loader skips
  a partial last line (agents append while the resolver runs). Crossref 60 queries, OpenAlex 1 page ($0.0001).
- 2026-11-15 B2 run: b01-b17 done (reports: about half the packets hold a real benchmark; the rest are own-design,
  process or material tables, text-only comparisons, or unlabelled plots). Common agent actions: tables read from the
  page render when the text layer is empty (frequent), benchmark tables outside the packet regions (`region: null`),
  supplement reference lists (sohn2021, tian2021: supplement tags), references taken from text.md when the packet's
  parsed list was wrong (supplement list, table text). Class calls outside the key list: optical phased arrays mostly
  `free_space_emitter.other` (some `out_of_scope.pic`), single-photon sources, beam steering, wavefront shaping, sensors,
  materials -> `out_of_scope.*`. Mid-run yield (pilot + b01-b10, 212 papers): 115 ok, 958 items, 921 distinct refs;
  projection ~2600 items over all packets.
- 2026-11-15 rule change (D1206): trend plots with unlabelled points whose caption / legend lists the plotted works'
  tags give one item per listed reference (`values: []`, note `caption_refs`); before, such plots gave nothing
  (ji2024, spencer2014, suk2025, nagarajan2005 noted `unlabelled_plot`). Brief updated before b19 launched; earlier
  papers noted `unlabelled_plot` get a sweep batch at the end.
- 2026-11-15 recall check: 807 lit papers without a packet; 141 of them have a table caption and "this work". Sample
  of 6: croce2026, lin2022, zhou2025a hold real comparison tables missed because their citations are superscripts
  flattened into plain numbers or author-year labels (no `[n]` tags). Rule D1207: a table whose caption itself says it
  compares reported / previous / literature / state-of-the-art works is accepted without tags. +29 papers (lit 23,
  EO 6), packets written by `--only-new` (existing packets untouched while agents read them), batch b27.
- 2026-11-15 B2 completed b01-b27 + sweep s01 (12 papers extracted before D1206: +53 items; suk2025 group-cited bars
  got refs; yu2023 S1-S21 supplementary refs and lu2025 [34], saghaei2026 [52] are not in the cached text, left
  empty). b27 (D1207 papers) yield 25 / 29 ok, 225 items: the caption rule finds productive papers. OFC packets
  (no page renders) yield low (b24 14 / 28, b25 8 / 28). Not processed: singaravelu2019 Table 1 is black: the embedded
  image (xref 50, 692x324 DeviceRGB, no soft mask) has all-zero pixels in the cached PDF itself, so a re-render does
  not help; another copy of the PDF would be needed. Agents flagged tag / reference-list
  numbering offsets (guo2026, sharma2022, lee2026, sheng2026, eo:chen2022, taghavi2026, yue2025, taballione2019):
  mapped by content where unambiguous, else kept as printed, always noted. EO / OFC twins (58 EO-atlas papers are
  OFC 2026 papers, e.g. eo:tran2026 = ofc2026:W3E.6) are counted once as citing papers (curate maps them by venue and
  `same_as`).
- 2026-11-15 recall pass 2 (D1208): zhou2025a "PERFORMANCE COMPARATION OF ON-CHIP FP FILTERS" (IEEE upper-case
  caption, image-only body) was still missed -> any table caption with compar* / summary / overview / survey is a
  candidate; +41 papers (lit 29, EO 8, OFC 4), batches b28 / b29 (20 / 21 packets); agents reject own-design tables.
- 2026-11-15 b28 / b29 (D1208 papers): 9 / 20 and 10 / 21 ok, 78 + 74 items (lower yield than D1207, as expected).
  B2 totals: 653 paper lines (376 ok, 274 no_benchmark, 3 refs_missing), 3416 items, 3006 distinct reference
  strings; agent cost ~0.15-0.29 M tokens per batch of 16-28 packets.
- 2026-11-15 B7a fresh-context extraction audit (`cache/literature/bench/audit_extract_a.md`, seed 20261115, 40
  items from 20 batches, 25 no_benchmark papers): (a) cross-work comparison and (b) ref_num 38 pass / 0 fail / 2
  unverifiable; (c) reference entry 40 / 40; (d) class 40 / 40; (e) values 34 / 34 (95 % upper bound on item error
  ~9-10 %). no_benchmark 24 / 25 correct (missed: vaskasi2022 Fig. 4 legend "Earlier work [22]"). 10 citing papers
  appear twice (EO-atlas vs OFC 2026 copies; the OFC copy without renders yields fewer items, e.g. huang2026 11 vs
  Th4A.6 1): handled in curate by the twin map (one citing paper, items of both copies kept). 7 ids have
  conflicting status lines between first pass and the s01 sweep (qiu2026, richardson2013): curate reads items only,
  never status lines, so no effect. Remaining caveats: OFC tables without text or render (M1E.2) are incomplete;
  literature-parameter tables are accepted inconsistently (taballione2019 yes, campenhout2010 no); footnote flags
  stay in values (cross-check material only, D1202).
- 2026-11-15 B3 code: `scripts/bench_resolve.py` (printed DOI / arXiv -> pool or sources.csv title match ->
  verified Crossref bibliographic query; OpenAlex `filter=doi:` enrichment, 50 per page; resumable caches).
- 2026-11-15 B3 final: 3006 distinct reference strings -> 2829 resolved, 178 unresolved, 2 errors (Crossref
  ~3 s per query; ~1400 Crossref queries in three passes; OpenAlex `filter=doi:` enrichment). B4-B6
  (`bench_curate.py`): 3416 items -> 2192 works (+206 unresolved refs) -> new 1249, in library 326, already queued
  15, EO atlas 49, out of scope 321, modulators 232 (EO side list `bench_eo_candidates.csv`, 232 rows). New by
  tier: 1 (arXiv / OA) 569, 2 (IEEE) 225, 3 (other paywalled) 455. Above the cut: 813 = all tier 1-2 + 19 tier-3
  works cited by >= 3 benchmarks (no subtype hit the cap of 70). The ~1200 target is not reached from this round:
  tier 1-2 supply is 794; the rest are 436 tier-3 rows below the cut (manual-download pool) and the second hop
  (benchmark tables of the papers cached from this list).
- 2026-11-15 B8 (`scripts/bench_prepare.py`, D1209): above-cut rows appended to `cache_list.csv`
  (`selection_reason = benchmark_cite`, rationale = citing count + topics) and to `retrieval_queue.csv` (backup
  `cache/literature/backup/bench_queue_20261116T053306Z.zip`): 813 rows; routes ieee_browser 295, optica_browser
  225, arxiv 121, oa_publisher 76, publisher_browser 57, manual 36, ieee_search 3; days 201-210 with caps per day
  (arxiv 40, oa_publisher 20, IEEE 30 = one session, Optica 24 in sessions of 12, publisher 10), manual rows day 200.
  paper_id = OpenAlex first-author surname (initial tokens skipped: "Daoxin Dai A" -> dai) + year, else the printed
  reference's first author; unique against references/, cache_list, queue and every registry native id.
- 2026-11-15 21:33 PST day 201 started (owner: "start a new day's caching"): tmux `lit_bench_d201`
  (`lit_fetch_oa.py --day 201`: 40 arxiv + 20 oa_publisher, log `logs/lit_bench_d201_oa_20261115T213316.log`) and
  `lit_ieee_d201` (`lit_fetch_browser.py --site ieee --run --day 201 --wait-login`, 30 rows, log
  `logs/lit_bench_d201_ieee_20261115T213316.log`). Not run (standing rule: explicit owner go per run): Optica
  OA-journal session (24 rows, OE / Optica / OME only) and publisher-browser session (10 rows). First minute: MDPI
  HTTP 403 -> breaker `www.mdpi.com` until 2026-11-16T06:03Z (wilmart2019 blocked).
- 2026-11-15 day 201 result (21:33-22:29 PST). Open routes (`lit_fetch_oa.py --day 201`, done 21:41): 42 ok, 15
  blocked, 3 not_pdf; new breakers (until 2026-11-16T06:03Z) MDPI (HTTP 403) and figshare (WAF challenge); also
  blocked: link.aps.org, cell.com, ssrn, pubs.acs.org (403), ntt-review.jp (TLS verify failed), AIP (standing).
  IEEE (`lit_ieee_d201`): institutional access detected at 21:33:51 without a sign-in, 30 / 30 ok, spacing 86-115 s,
  done 22:28 (owner note: tell him before an IEEE session starts, he logs in first). Optica OA journals (owner go
  "go ahead with optica too"; runner `logs/lit_optica_oa_d201_runner.py`, OE / Optica / OME only, probe 3 + 11,
  15 min pause, + 10): 24 / 24 ok, 21:37-22:29, no challenge, breaker not armed. Publisher-browser rows (10) not
  run. Total 96 PDFs; extracted 96 (`logs/lit_extract_d201_*`; flags: 24 institutional_stamp, 3 garbled text layer:
  boller2019, chen2022c, hu2025a). Page-1 title check (title words in page-1 text): 90 >= 0.9; below: park2007 0.80,
  subramanian2012 0.88 (ligatures / subscripts in IEEE scans, same paper), zheng2020 0.82, chen2022c 0.88,
  stokowski2023 0.89 (arXiv preprint titles, same papers), yu2022 0.62 = wrong paper: the OpenAlex pool's arXiv id
  2212.01945 is Yu et al., "Integrated electro-optic isolator on TFLN", not the Nature 2022 femtosecond pulse
  generator -> folder moved to `cache/literature/quarantine/yu2022_holds_arxiv2212.01945_eo_isolator_20261115`,
  queue / cache_list row re-routed to manual (day 200, arxiv_id cleared). Registered 95 (`lit` 1198 -> 1293,
  sources.csv +95 lines only), validate_db 0 errors / 1386 warnings, manual list 148 rows. Not committed.
- 2026-11-16 day 201 ingested (owner "go", then "cmt and push once everything is done"): 21 distill batches lit_134-lit_154 with one fresh audit each, header batches lit_h43-lit_h46, supply lit_07 / lit_08 (DevLog-007 D577-D600, DevLog-011 D599, DevLog-003 D598): components 4715 -> 5206, metrics 29078 -> 32254, people 11715 -> 12066. A classifier outage stopped two agents mid-run (lit_150 audit, lit_152 distill); both were rerun from scratch, partial outputs kept in the session scratchpad. Next: days 202-210 (about 690 rows; Optica OA journals and publisher-browser sessions need an owner go per run; tell the owner before each IEEE session).
- 2026-11-16 day 202 (owner: "inspect repo recent progress, and run today's caching and ingestion"; IEEE: owner signed in; Optica: owner go "Optica only", publisher-browser rows not run). Open routes (`lit_fetch_oa.py --day 202`, log `logs/lit_bench_d202_oa_20261116T221840.log`, 22:18-22:25 PST): 43 ok, 15 blocked (MDPI x5, SPJ, ACS, Elsevier CDN / ScienceDirect, Science Advances, UTwente repository, AIP x2, Cardiff ORCA, SPIE), 2 not_pdf; new breakers until 2026-11-17T06:49Z. IEEE (`lit_ieee_d202`, log `logs/lit_bench_d202_ieee_20261116T223007.log`): institutional access 22:30:38, 30 / 30 ok, done 23:26. Optica OA journals (runner `logs/lit_optica_oa_d202_runner.py`, OE / Optica only, probe 3 + 11, 15 min pause, + 10): 24 / 24 ok, 22:30-23:25, no challenge. Total 97 PDFs, all extracted, page-1 title check 97 / 97, registered `lit` 1293 -> 1390 in two waves (DevLog-007 D601 / D615); manual list 165 rows. Ingested the same night (D601-D627): components 5206 -> 5590, metrics 32254 -> 34715. Resolution / dedup errors found by the distillers (B7b material): lorenzen2025 (arXiv 2505.15361) is the preprint of merged lit:lorenzen2026 (Nature Communications; every device and value covered, D607); zhou2020a is K. C. Zhou's OE diffraction-tomography paper, a wrong match for wang2022a's "H. Zhou et al., Opt. Express 28, 2020" GeSn photodetector citation (D603); the GeSn paper is not in the cache.
- 2026-11-17 / 2026-11-18 day 203 (owner: "take a look at yesterday's daily cache and ingestion ... incorporate my feedbacks into skills ... then run today's"; the daily procedure now lives in `.claude/skills/pic-component-distill/daily-run.md`, standing authorization, no questions). Open routes (`logs/lit_bench_d203_oa_20261117T232502.log`): 44 ok / 14 blocked / 2 not_pdf. IEEE (`logs/lit_bench_d203_ieee_20261118T081848.log`, first launch died on the home-page goto, relaunched): 30 / 30. Optica OA journals (`.claude/skills/pic-component-distill/scripts/optica_runner.py 203`): probe 3 / 3, chunk 1 11 / 11, chunk 2 stopped on jiang2019 (Playwright navigation-race error, breaker armed, not retried): 14 / 24, 10 rows left on day 203. Publisher-browser rows (10) not run. Ingestion in two halves on owner instruction (DevLog-007 D631): half A = 44 open-route papers (lit_180-lit_191, D631-D643); half B = 44 IEEE + Optica papers on a 13:15 PST timer.
- 2026-11-18 13:15-14:20 PST day 203 half B (DevLog-007 D646-D659): the 44 browser-route papers (IEEE 30, Optica 14) extracted, title check 44 / 44, registered `lit` 1434 -> 1478; distill lit_192-lit_202, audits (0 wrong metric values, 20 misses added), merges; components 5798 -> 5976, metrics 35727 -> 36827; headers lit_h53 / lit_h54 (people 12552 -> 12677); supply lit_12 (+13 products / +46 usage rows). Benchmark: 1 cell moved, AIM Photonics SiN propagation loss < 0.3 -> 0.075 dB/cm (koscica2025, spiral cutback). No wrong benchmark-list resolutions in half B (all 44 page-1 titles matched). Still queued on day 203: 10 Optica rows (breaker armed after the jiang2019 navigation error), 10 publisher-browser rows.
- 2026-11-18 18:11-20:40 PST day 204 (DevLog-007 D660-D671; owner "go on"): open routes 3 ok / 12 blocked / 2 not_pdf; IEEE first launch found no access and timed out unsigned (30 min), relaunched on owner "go on, where to sign in", 30 / 30 ok after sign-in; Optica not run (breaker from the day-203 jiang2019 error still armed; 24 rows queued); publisher browser not run (10 rows). Ingested 33 papers: lit_203-lit_211, headers lit_h55 / lit_h56 (people 12677 -> 12731), supply lit_13; components 5976 -> 6089, metrics 36827 -> 37811. Benchmark: 1 new cell (AIST thermo-optic P_pi 18.1 mW, suzuki2018). No wrong benchmark-list resolutions (all 33 page-1 titles matched; cao2021 is the HAL author manuscript, pfeiffer2018 the arXiv v1 of the listed work).
- 2026-11-19 / 2026-11-20 day 205 (DevLog-007 D672-D686; owner "continue with new days caching and ingestion"; runbook fixed: a leftover Optica / IEEE breaker is cleared and re-probed, never asked about). IEEE 29 / 30 (westbergh2009 no_ieee_copy; institutional access without sign-in); Optica 21 / 24 after clearing the day-203 breaker (probe 3 / 3, chunk 11 / 11, last chunk stopped on xu2019b ECONNRESET, breaker re-armed); no open-route rows on day 205; publisher browser not run (10 rows). Ingested 50 papers: lit_212-lit_223, headers lit_h57 / lit_h58 (people 12731 -> 12814), supply lit_14; components 6089 -> 6307, metrics 37811 -> 39079. Benchmark: Sandia SiPh crossing 0.8 -> 0.06 dB (hoffman2019), new SMIC SiPh grating-coupler IL 9 dB (li2015, packaged pair halved). No wrong benchmark-list resolutions (all 50 page-1 titles matched); registry metadata errors: clark2003 is OFC/IOOC 1999, yasuoka2005 is LEOS 2003.
- 2026-11-20 day 206 (DevLog-007 D687-D697; owner "check again"; then "remove the stupid breaker. Whenever it breaks you should check manually. And continue if the error is a standalone case": Optica runner writes no breaker file, a stop is checked on its page snapshot by hand). IEEE 29 / 30 after the owner's sign-in (yang2013 no_ieee_copy; the first 01:47 attempt timed out unsigned); Optica 6 / 24: Optica's rate-limit page ("downloading timeout based on heavy usage") came back after 1-3 papers per window at 19:40, 20:02 and 20:41 despite 20 and 30 min waits, rest of the day skipped, 18 rows queued; no open-route rows on day 206; publisher browser not run (7 rows). Ingested 35 papers: lit_224-lit_233, headers lit_h59 / lit_h60 (people 12814 -> 12862), supply lit_15; components 6307 -> 6409, metrics 39079 -> 39889. Benchmark: no cell value moved (sources 98); LIGENTEC SiN propagation-loss cell n 8 -> 9 (gao2025b). No wrong benchmark-list resolutions (all 35 page-1 titles matched).
- 2026-11-20 day 207 (DevLog-007 D700-D711). IEEE 29 / 30 (shinobu2010 no_ieee_copy; signed-in session still valid); Optica 7 / 24: rate-limit page at 21:27, 21:52 and 22:18 after 20 min waits (1-3 papers per window), one standalone wrong-PDF stop (barbarin2006 served bernard2021's PDF; title guard refused; relaunched), rest of the day skipped, 17 rows queued; no open-route or publisher rows on day 207. Ingested 36 papers: lit_234-lit_242, headers lit_h61 / lit_h62 (people 12862 -> 12953), supply lit_16; components 6409 -> 6518, metrics 39889 -> 40608. Benchmark: LIGENTEC SiN edge-coupler IL 2.0 dB (lorenzen2026) -> 0.8 dB (wang2023f, measured per SSC facet); new LIGENTEC SiN MMI excess loss 0.2 dB (wang2023f). No wrong benchmark-list resolutions (all 36 page-1 titles matched); registry title lit:barbarin2006 "at 153µm" should read 1.53 um.
- 2026-11-22 day 208 (DevLog-007 D712-D727). IEEE 30 / 30 (institutional access without a sign-in); Optica 24 / 24 (probe 3, chunk 11, 15 min pause, chunk 9; no rate-limit page; yao2012 cached 2026-11-20); no open-route or publisher rows on day 208. Ingested 54 papers: lit_243-lit_254, headers lit_h63 / lit_h64 (people 12953 -> 13057), supply lit_17; components 6518 -> 6759, metrics 40608 -> 42391. Benchmark: AMF / IME MMI excess loss 0.15 -> 0.11 dB (xiao2013); Tower thermo-optic P_pi 8.8 -> 2.56 mW (chung2019a); AMF Ge PD bandwidth 50 -> ~60 GHz (novack2013); CEA-Leti Ge PD responsivity 0.98 -> 1.16 A/W, bandwidth 42 -> > 50 GHz, dark current 18 -> 6 nA (virot2017); AMF Ge PD responsivity 1.09 -> 1.14 A/W (zhang2014b at -4 V; its avalanche-gain values excluded, D726). No wrong benchmark-list resolutions (54 / 54 page-1 titles matched; okai1990 checked on the scanned page image); registry years to fix: lit:chen2002 (1996), lit:sugg2002 (2000), lit:mathur2002 (1998).
- 2026-11-23 day 209 (DevLog-007 D728-D743). IEEE 29 / 30: the first launch stopped after 3 papers on takenobu2008, whose queue DOI `10.1109/ofc.2008.4528185.2008` (trailing ".2008") resolves to doi.org's "DOI Not Found" page (it embeds a Cloudflare Turnstile widget, read as a challenge); relaunched on the other 29 (owner signed in again), 26 more ok; the fetcher now treats a dead DOI as `bad_doi` with an Xplore title-search fallback, tolerates one IEEE challenge with the session intact and waits in-window for re-login (owner: "error like this should not trigger a full rerun"). Optica 24 / 24 (probe 3, chunk 11, 15 min pause, chunk 10; no rate-limit page); no open-route or publisher rows on day 209. Ingested 53 papers: lit_255-lit_266, headers lit_h65 / lit_h66 (people 13057 -> 13219), supply lit_18; components 6759 -> 7007, metrics 42391 -> 44085. Benchmark: new IHP SiN column (lischke2019); AMF SiPh / SiN bend loss new (gao2021a); imec SiPh propagation loss 0.5 -> 0.271 dB/cm (bogaerts2011 rib); Applied Nanotools GC 1-dB bandwidth 20 -> 38 nm (wang2017b); CEA-Leti GC 1-dB bandwidth 27 -> 73.2 nm (mak2018); IHP SiPh dark current 20-100 -> ~30 nA (lischke2019); steckler2024 figure-read responsivities excluded (D743). Wrong benchmark-list resolutions: none (53 / 53 page-1 titles matched); registry metadata error: takenobu2008 DOI.
- 2026-11-24 day 210 (DevLog-007 D744-D757). IEEE 28 / 28 (institutional access at launch, no sign-in; the dead-DOI / single-challenge paths of the fetcher were not exercised); Optica 9 / 9 (probe 3, chunk 6); no open-route or publisher rows on day 210. takenobu2008 (day 209, dead queue DOI) relaunched alone with `--paper-ids`: no institutional access in the new window, no sign-in within 30 min, not fetched. Ingested 37 papers: lit_267-lit_275, headers lit_h67 / lit_h68 (people 13219 -> 13330), supply lit_19; components 7007 -> 7209, metrics 44085 -> 45434. Benchmark: no cell moved vs HEAD; orcutt2011 (post-processed Texas Instruments development wafers) excluded from the view (D757); a would-be imec SiN GC bandwidth cell from subramanian2012a was a 900 nm coupler with a missing band, fixed in the data (D754). Wrong benchmark-list resolutions: none (37 / 37 page-1 titles matched).
- 2026-11-25 day 211, partial wave (DevLog-007 D758-D766; owner: ingest the papers cached so far, commit and push, while the caching session's overnight Optica OA backlog run continues). 22 papers ingested: Optica OA 19 (day-204 backlog), IEEE 2 (colbourne2018; takenobu2008 with the corrected DOI), repository copy 1 (shinobu2010); yang2013's repository copy was a PhD thesis citing the paper, quarantined. lit_276-lit_280, header lit_h69 (people 13330 -> 13393), supply lit_20; components 7209 -> 7285, metrics 45434 -> 45899. Benchmark: no cell value moved vs HEAD (D766).
