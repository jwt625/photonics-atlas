# DevLog-019: Benchmark-citation snowball (next caching round from comparison tables and trend plots)

| | |
|---|---|
| Date | 2026-11-15 |
| Status | B1-B7a done; list `data/_staging/literature/bench_cache_list.csv` (1249 new works, 813 above the cut) queued as days 200-210; day 201 cached (96 PDFs, 95 registered) and ingested (DevLog-007 D577-D600); days 202-210 pending |
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
