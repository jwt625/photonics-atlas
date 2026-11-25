# DevLog-020: Reference graph from cached reference sections (triage for the next caching rounds)

| | |
|---|---|
| Date | 2026-11-24 |
| Status | Stage 1 (reference graph) and stage 2 (metadata, 2640 new works cited by 3+ corpus papers) done; queueing next |
| Scope | Parse the reference section of every cached `lit` paper, match each reference to a work already in the corpus, identify and deduplicate the references that are not, and rank the missing works by how many corpus papers cite them |
| Related | DevLog-019 (benchmark-citation snowball: table / plot citations only, 2026-11-15 corpus), DevLog-006 (pool, retrieval, access rules), `src/photonics_atlas/litpool.py` (norm_doi / norm_title) |
| Decisions | D1230-D1249 reserved for this DevLog |

## Request (2026-11-24, Wentao)

"can we triage by parsing reference section of cached papers, and find the matching paper thats already in the
corpus, and dedup the ones thats not in the corpus. Should be straight forward to setup a similarity score, and after
simple formating cleanup it should be really high for id-ing the papers." Context: "Should help with sourcing the
next batch."

## Starting point (inspected 2026-11-24)

- 1776 `lit` texts (`references/<id>/text.md`, PyMuPDF text with `<!-- page N -->` markers). Reference headings:
  1284 with a References / Bibliography line, 9 inline, 483 without one (Nature-style lists with no heading, old Optics
  Express "References and links" at the top of the paper, conference papers). Entry styles among headed texts: `[n]`
  578, `n.` 576, `n ` 31, `(n)` 11, other 97.
- PyMuPDF artifacts in reference lists: line-break hyphenation ("Mi-\ncrophotonics"), ligatures, curly quotes, figure
  axis labels interleaved into Nature-style lists, page markers.
- Existing citation data: DevLog-019 `cache/literature/bench/works.jsonl` (3079 table / plot edges from 375 citing
  papers); OpenAlex `referenced_works` for 71 review seeds only (`refs_of_all` in the pool). The OpenAlex pool
  `cache/literature/merged.jsonl` (215,863 records) has titles / DOIs / years / authors / OA status but no reference
  lists.
- No network is needed: everything is matched against local files.

## Plan

1. Reference entries (location-agnostic): scan the text for numbered entry starts (`[n]`, `n.`, `(n)`, `n `); keep
   the longest run that counts up from 1 with most entries carrying a year; an entry runs to the next start. Page
   markers and headings are dropped.
2. Identifiers in the entry: DOI (regex, normalized with `norm_doi`), arXiv id, years.
3. Matching, in order: (a) DOI / arXiv id exact against the corpus; (b) title containment against the corpus: corpus
   title and reference string both squashed to `[a-z0-9]` (NFKD, no spaces / punctuation; absorbs hyphenation, line
   breaks, ligatures and quotes); exact substring = 1.0, otherwise the matched-block fraction of the title; candidates
   from an index of title word bigrams; year within +/- 1 when the entry has a year; first-author surname recorded as
   a confidence signal; (c) the same against the OpenAlex pool for references not in the corpus (gives a DOI / OA
   status / venue for the missing work); (d) the rest clustered by extracted title (quoted title for IEEE / Optica
   style) or surname + year + volume + page.
4. Corpus = every registry corpus in `data/registry/sources.csv` (lit, eo, pk, ofc2026, lin, blog, web) plus
   `cache_list.csv` rows (cached or queued). Queued-but-uncached works are reported as "queued", not missing.
5. Outputs (git-ignored `cache/literature/refgraph/`): `refs.jsonl` (one row per reference: citing paper, number,
   trimmed raw string, ids, match kind / id / score / method), `missing.csv` (deduplicated works not in the corpus:
   id, title, year, venue, OA status, number of citing corpus papers, citing ids, one example string),
   `summary.json`. Script `scripts/lit_refgraph.py` (`--paper-ids`, `--limit`, `--out`), tests in
   `tests/test_lit_refgraph.py`.
6. Pilot on ~20 diverse papers (IEEE `[n]`, Optica `n.`, Nature without heading, APS without titles, old OE top
   references, conference); look at the score distribution and every borderline match by hand; set thresholds; then
   the full corpus.
7. Fresh-context audit of a random sample of matches (precision) and of unmatched entries (recall).

## TODO

- [x] Script + tests (`scripts/lit_refgraph.py`, `tests/test_lit_refgraph.py` 8 / 8)
- [x] Pilot, thresholds (D1230-D1233)
- [x] Full run, summary, top missing works by class (`cache/literature/refgraph/run_20261124/`)
- [x] Audit (fresh context, [audit](audits/2026-11-24-refgraph-audit.md)); fixes D1234, re-run `run_20261124T235543`
- [ ] Owner: how the missing list feeds the next queue (cut, routes)

## Decisions

| ID | Decision | Source |
|---|---|---|
| D1230 | Corpus for matching = registry corpora lit / eo / pk / ofc2026 (text cached = `corpus`, else `registry_uncached`) + blog paper rows ("Author Year, " prefix stripped) + cache_list rows (`queued` when not cached). lin / web rows are bios, filings and pages, not papers. `registry_uncached` matches are listed as missing | pilot |
| D1231 | Acceptance: squashed-title containment >= 0.90 (year within +/- 1 when the entry has a year); titles under 30 squashed characters need an exact substring plus the first-author surname in the first 40 words (or the exact year when no surname is known); 0.75-0.90 accepted only with surname and exact year (`title_author`). Pilot: 119 exact 1.00 matches, every accepted non-exact match read by hand correct (abbreviated "SOI", typo "Lss-than"); generic short titles ("Silicon photonics") no longer match other works | pilot (20 papers, 499 entries) |
| D1232 | Entry runs keep one numbering style (`[n]` / `n.` / `(n)` / bare). (Corrected by the audit: a `1.` section heading still chained into `n.` lists, about 1,400 body-text rows in 369 papers; fixed in D1234.) Optica page footers (`#NNNNNN Received ... OPTICS EXPRESS NNNN`) and the citing paper's own DOI are removed from entries before matching (a footer had merged Kippenberg 2011 with the citing paper's DOI) | full-run inspection |
| D1233 | Missing-work dedup = union-find over DOI, first quoted title and surname + year + first page (>= 3 digits); an entry with two or more quoted titles (several works) keys on its first title only; DOIs with a suffix under 6 characters (cut at a line break) are ignored. Dissimilar-title clusters 19 -> 4 of about 25.8k. Candidate order sorted, so runs are byte-identical across hash seeds | full-run inspection |
| D1234 | ([audit](audits/2026-11-24-refgraph-audit.md)) Audit of run_20261124: precision about 97.3 % over 23,352 matched rows (doi 20 / 20, arxiv 10 / 10, title 1.0 54 / 55, title 0.90-0.99 15 / 20, title_short 43 / 45, title_author 20 / 40); recall about 87-88 % (12 of 92 real unmatched references were present: 3 corpus, 9 pool; 10 of them title-less APS / AIP / Optica entries); 9 / 12 papers split correctly; dedup 40 / 40 clusters clean, 5 pool / unresolved duplicate pairs in the top 300; no self-citation. Accepted recs 1, 2, 3, 4, 5, 6, 7, 8, 10, 12: latest `1` among runs within 85 % of the longest and section-like first entries rejected; glued `1M.`, `1 .` and lone-number styles; DOIs built from venue + volume + page (Optica legacy journals, APS) and a surname + year match with the page inside the candidate DOI for title-less entries; exact squashed quoted-title lookup and one shared bigram for short titles; "[Invited]" stripped; title_author >= 0.85 with the entry's first author; partial containment needs one block >= 60 % of the title; venue-named pool records dropped and authorless pool records not accepted on the year alone; earlier versions of the citing paper labelled `self_version`; IEEE running headers / "Authorized licensed use" / Nature page labels removed. Deferred: rec 9 (venue-type version preference), rec 11 beyond the latest-run rule (supplementary lists). Re-run (18 s; intermediate run since superseded by run_20261125T004100, D1235): papers with a list 1573 -> 1617, entries 48,086 -> 49,074, corpus matches 7466 -> 8206, pool 14,894 -> 16,718, unmatched 24,734 -> 23,014, self_version 35; missing works 25,848 -> 24,336, cited by 3+ 2623 -> 2824 (pool 1662, unresolved 1158, registry 4), 10+ 204 -> 261; spot check of the new rules 28 / 28 correct (built DOI 12, author + page 10, exact title 6). Dissimilar-title clusters 10 (was 4; rare, not chased). The 22-entry hand sample claim of "no missed corpus paper" was wrong (audit: 3 corpus misses in 92) | audit + coordinator |
| D1235 | Stage 2 (`scripts/refgraph_prepare.py`, `data/_staging/literature/refgraph_cache_list.csv`). Crossref on the 675 unresolved clusters cited by 3+: 642 resolved (verify rule of bench_resolve: surname, year +/- 1, title / title words / page), 14 / 14 sampled correct; OpenAlex enrich 539 DOIs. Fixes found on the output: rows resolving to one DOI / arXiv id are merged (46 DOIs, a pool row plus a title-less cluster of the same paper; citing papers unioned); built-DOI parser fixes (volume must end at a non-digit, colon / comma-before-issue separators, spaced IEEE page numbers "17 106", Optics Express volumes 1-13 use `opex`, APS 6-digit article numbers since 2001 padded, a "volume" >= 1000 is a year), and DOIs that neither the pool nor OpenAlex knows go through Crossref on the cluster's entries. Final stage-1 run run_20261125T004100 (49,074 entries; corpus 8225, queued 1025, pool 16,725, unmatched 23,007; missing works 24,482, cited by 3+ 2799). Stage-2 list: 2750 works after the merge: new 2640 (routes: manual 890, IEEE browser 569, Optica OA 513, arXiv 285, publisher browser 175, OA publisher 175, IEEE search 33; tier 1 1312, tier 2 440, tier 3 888; types article 2423, conference paper 185, preprint 20), already in the library 47 (missed by the title matcher, caught by DOI), queued 1, not a paper (books) 12, DOI unverified 10, unresolved 40. Not queued yet | coordinator |

## Results (run_20261124, 2026-11-24 23:35 PST, 35 s)

- 1776 texts, 1573 with a reference list (203 none: conference papers without one, footnote-style 1960s papers, a
  missing first entry), 48,086 entries.
- Matched: corpus 7466 (15.5 %), queued 963 (2.0 %), registry without text 29, OpenAlex pool 14,894 (31.0 %);
  unmatched 24,734 (51.4 %; superseded by D1234: recall about 87-88 %, the re-run recovers part of the gap).
- Missing works after dedup: 25,848; cited by 10+ corpus papers 204, 5-9 801, 3-4 1618, 2 2866, 1 20,359. Cited by
  3+: 2623 (pool-resolved 1489 with DOI / OA status: closed 657, gold 471, green 209, hybrid 67, bronze 46; types:
  article 1361, conference paper 100, book 7; unresolved 1131).
- Top of the list: Taillaert 2004 GC (45 citing papers), Chrostowski / Hochberg book (40), Bogaerts 2011 rings (36),
  Reed 2010 modulators (34), Bauters 2011 SiN (33), Barwicz 2006 (31), Zhu 2021 TFLN review (31, unresolved).
  `missing.csv` carries the citing papers' class mix (`citing_classes`).

## Stage 2 plan: metadata for the works cited by 3+ corpus papers (owner 2026-11-24)

Owner: "let's do these 2623 papers next. Start preparing their metadata."

1. Input: `missing.csv` rows with `n_citing >= 3` of the latest run (2623 on run_20261124; 2824 on
   run_20261124T235543 after D1234: pool-resolved 1662, unresolved 1158, registry-only 4).
2. Pool-resolved: DOI, arXiv id, title, authors, year, venue, type, OA status / URL from the pool record.
3. Unresolved: the cluster's member entries (union-find rebuilt from `refs.jsonl`, same order as the run); a printed
   DOI / arXiv id first; else Crossref `query.bibliographic` on the best entry (quoted title, longest), accepted only
   with `bench_resolve.verify` (first-author surname, year within 1, title similarity >= 0.8 or title words in the
   string or first page); a second entry when the first fails. Resolved DOIs not in the pool: OpenAlex
   `filter=doi:` batches of 50 for OA status / venue / type. Rate-limited client `photonics_atlas.litfetch` (generic
   User-Agent, per-host spacing, breaker); results cached in `cache/literature/refgraph/resolve_cache.jsonl`
   (resumable, keyed by cluster root).
4. Dedup after resolution against sources.csv, cache_list.csv, the retrieval queue and the EO atlas tables; books,
   theses and book chapters flagged (not cacheable as papers); class hint = most frequent primary class of the citing
   papers, with the full mix kept.
5. Route by the `bench_prepare.py` rules (arXiv, Optica OA journals, IEEE, publisher browser, OA publisher, manual).
6. Output `data/_staging/literature/refgraph_cache_list.csv` (not queued); queueing (days, caps) is the next step after
   the audit of stage 1.

## Progress

- 2026-11-24 23:25 PST plan written (day 211 Optica caching still running in parallel; this stream is offline).
- 2026-11-24 23:35 PST pilot (2 rounds), fixes D1230-D1233, full run; fresh-context audit dispatched.
- 2026-11-24 23:56 PST audit back; fixes D1234; re-run; stage 2 (metadata for 2824 works) next.
- 2026-11-25 00:41 PST stage 2 done (D1235): `refgraph_cache_list.csv`, 2750 works, 2640 new; intermediate runs removed (kept: run_20261124 = audited baseline, run_20261125T004100 = final).
