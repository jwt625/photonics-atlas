# Lane L4: seeds and snowball (DevLog-006 S1, 2026-10-21/22)

Candidates only, with no relevance screening. Every record comes from an OpenAlex response, and its reason fields come from local files or the review it was cited in. Pool files are in `cache/literature/pool/` (git-ignored) and raw API caches are in `cache/literature/seeds/`.

## Commands (all resumable, skip cached)

```
uv run python scripts/lit_seeds.py local            # local seeds -> seeds_local.jsonl
uv run python scripts/lit_seeds.py find-reviews [--openalex-search] --show [--review-only]
uv run python scripts/lit_seeds.py anchor-reviews --show   # review-like works citing landmark anchors
uv run python scripts/lit_seeds.py reviews          # seeds_reviews.jsonl + seeds_refs_<class>.jsonl
uv run python scripts/lit_seeds.py cites            # seeds_cites_<class>.jsonl
```

Config: `config/literature/seed_reviews.yaml` (queries, anchors, openalex_queries, reviews, cites). Tests: `tests/test_lit_seeds.py`.

## Outputs (2026-10-22 00:26 UTC)

| file | records | years | OA | with abstract |
|---|---|---|---|---|
| seeds_local.jsonl | 554 | 2002-2026 | 522 | 531 |
| seeds_reviews.jsonl (`is_review_seed: true`) | 71 | 2017-2026 | 47 | 61 |
| seeds_refs_<class>.jsonl (20 files) | 10,774 (sum) | 1836-2025 | | |
| seeds_cites_reflector.jsonl | 242 | 2012-2026 | 116 | 226 |
| all seeds_* | 11,641 rows, 9,391 unique uid | | | |

- Local: blog harvest gives 494 inputs (OA, photonics topic, in neither atlas, with an id; 40 url-only rows skipped); taxonomy section 5 gives 32; EO candidates give 45 (a title regex for non-modulator components). Unresolved: 4 ids (3 truncated blog DOIs `10.1364/oe.581`, `oe.26`, `oe.399` and arXiv 2609.17480, which is not yet in OpenAlex) and 2 taxonomy titles below the match threshold. The PCM title "A new family of ultralow loss reversible phase-change materials..." matched in Crossref at ratio 0.856. The "High efficiency apodized grating coupler for SOI waveguides" title has no matching Crossref hit. 14 taxonomy titles matched at ratio 1.0, which is recorded in `title_match`. Newer Optica URIs were resolved through Crossref with an exact journal, volume, issue and first-page match. Extra fields: `seed_source`, `seed_reason`, `seed_input_id`, `seed_class` (taxonomy only), `seed_arxiv_id`.
- Refs records carry `discovered_via: refs_of:<first review doi>`, `seed_class`, and `refs_of_all`. A work cited by reviews in two classes appears in both class files.

## Reviews per class (referenced works pulled = distinct ids; records = found in OpenAlex)

| class | n | reviews (doi, year, subtype) | refs | records | years |
|---|---|---|---|---|---|
| amplifier | 4 | 10.3390/s23177326 (2023, soa); 10.3390/photonics10020161 (2023, soa); 10.1109/jlt.2022.3153447 (2022); 10.3390/app122211712 (2022, rare_earth) | 355 | 352 | 1974-2022 |
| chip_chip_coupler | 3 | 10.1038/s41377-025-02048-w (2026, PWB); 10.37188/lam.2021.005 (2021); 10.3724/cjos.2025.026 (2026, transfer printing) | 607 | 604 | 1948-2025 |
| crossing | 2 | 10.3390/mi11030326 (2020); 10.3390/photonics13060539 (2026) | 162 | 162 | 1956-2025 |
| fiber_chip_coupler | 4 | 10.1364/prj.7.000201 (2019); 10.1515/nanoph-2018-0075 (2017); 10.3390/mi11070666 (2020, grating); 10.3390/app10041538 (2020, edge) | 465 | 460 | 1956-2024 |
| fiber_interface | 4 | 10.1021/acsphotonics.2c00891 (2022); 10.1109/jstqe.2020.2964383 (2020); 10.1109/tcpmt.2025.3582041 (2025); 10.1117/1.ap.3.2.024002 (2021, fan_out) | 494 | 488 | 1968-2024 |
| free_space_emitter | 4 | 10.1038/s42254-020-0182-8 (2020); 10.1109/jstqe.2020.3022948 (2020, OPA); 10.3390/mi13070990 (2022); 10.1364/aop.495828 (2023, metasurface) | 708 | 698 | 1908-2023 |
| frequency_converter | 4 | 10.1038/s41578-024-00668-z (2024); 10.1117/1.ap.4.3.034003 (2022); 10.1364/aop.495768 (2024); 10.1016/j.infrared.2022.104243 (2022, PPLN) | 1088 | 1072 | 1949-2024 |
| laser | 7 | 10.1364/aop.455976 (2022, heterogeneous); 10.1186/s43593-022-00027-x (2023); 10.1007/s11467-022-1245-3 (2023, SIL); 10.1063/1.5124254 (2019, tunable); 10.1117/1.ap.2.3.034001 (2020, comb); 10.1364/aop.502863 (2023, PCSEL); 10.3390/photonics10040410 (2023, VCSEL) | 994 | 983 | 1958-2024 |
| micro_optics | 4 | 10.1364/prj.453338 (2022); 10.1016/j.addma.2022.102682 (2022); 10.1038/s41377-022-00885-7 (2022, metalens); 10.1038/s41578-020-0203-3 (2020) | 657 | 646 | 1931-2023 |
| mode_converter | 3 | 10.29026/oea.2022.210127 (2022); 10.1063/5.0046071 (2021); 10.1109/jlt.2024.3412391 (2024) | 349 | 345 | 1970-2024 |
| nonreciprocal | 3 | 10.1364/ome.447398 (2022); 10.1364/ome.8.003307 (2018); 10.1039/d5tc01540e (2025) | 291 | 291 | 1877-2025 |
| phase_shifter | 5 | 10.1007/s12200-022-00012-9 (2022, TO); 10.3390/mi13091509 (2022); 10.1364/ome.8.002415 (2018, PCM); 10.1021/acsphotonics.2c00976 (2022, PCM); 10.1515/nanoph-2021-0082 (2021, MEMS/NOEMS) | 512 | 507 | 1959-2024 |
| photodetector | 4 | 10.1364/ome.435902 (2021, Ge); 10.1088/1361-6528/ac5442 (2022, APD); 10.1063/5.0045990 (2021, SNSPD); 10.1038/s41578-018-0040-9 (2018, graphene) | 796 | 794 | 1905-2021 |
| polarization | 3 | 10.1002/lpor.202301025 (2024); 10.1002/lpor.202500643 (2025); 10.1049/iet-opt.2019.0079 (2019, PBS) | 382 | 382 | 1836-2025 |
| reflector | 2 | 10.1109/jlt.2020.3035372 (2020); 10.1007/s12200-018-0813-1 (2018) + cites of 10.1364/oe.20.015547 | 102 | 99 | 1973-2023 |
| resonator | 3 | 10.1007/s11433-018-9349-2 (2019); 10.3390/photonics10111199 (2023, PhC); 10.1038/s41578-024-00668-z (2024) | 593 | 592 | 1961-2023 |
| splitter | 3 | 10.1038/s41586-018-0421-7 (2018); 10.1515/nanoph-2021-0110 (2021); 10.3390/photonics12090928 (2025) | 390 | 389 | 1956-2025 |
| switch_fabric | 4 | 10.3390/mi10010051 (2019); 10.1002/lpor.202200571 (2023); 10.1109/jlt.2020.3022375 (2020, WSS); 10.1109/comst.2019.2895817 (2019, MEMS OXC) | 386 | 380 | 1959-2022 |
| waveguide_platform | 4 | 10.1109/jlt.2021.3066203 (2021); 10.1364/aop.411024 (2021); 10.1364/prj.452936 (2022); 10.1038/s41467-024-44750-0 (2024) | 918 | 904 | 1963-2024 |
| wdm | 3 | 10.1016/j.scib.2018.05.038 (2018); 10.1038/s41377-022-00853-1 (2022, echelle/AWG spectrometers); 10.29026/oea.2022.210127 (2022) | 630 | 626 | 1961-2021 |

## How reviews were found

- Crossref `query.bibliographic` (74 queries) ranks "review" poorly. It matches journal names such as "Physical Review". About 15 picks came from it, after a review-word title filter.
- The best source was anchor citing lists: the 200 most-cited 2018-2026 works citing each of 49 landmark papers (`filter=cites:W`, filter-only), filtered for review-like titles. Anchor DOIs were checked against the OpenAlex title. One wrong DOI was replaced through a Crossref title match: the AWG anchor is now 10.1109/2944.577370. The OpenAlex `type:review` filter alone is too narrow (mostly Nature Reviews and Chem. Rev.) and was dropped after one pass.
- 14 OpenAlex `title.search` requests. Two picks came from them: the SOA review and 3-D packaging.
- Two reviews were dropped because OpenAlex has 0 referenced_works for them: 10.3788/lop55.120009 (AWG, 2018) and 10.1117/1.ap.7.6.064001 (Er, 2025).

## OpenAlex cost

L4 total about $0.033: 2026-10-21 $0.027 (14 searches $0.014, 78 anchor list pages $0.008, 50 refs pages $0.005); 2026-10-22 $0.0055. Singleton gets: free, about 900.

## Problems, gaps, suggestions

- On 2026-10-21 the shared daily cap blocked the run mid-way. It resumed after 00:00 UTC.
- Some large OpenAlex pages arrived truncated (JSONDecodeError). The script now retries up to 3 times.
- Cursor page 2 for `cites:` returned HTTP 401. The script now uses `page=`. This is worth noting in litfetch for L1-L3.
- Weak gaps: no dedicated Ge-PD, AWG/echelle, Er-amplifier (refs not indexed) or WSS (22 refs) review with good reference lists. Reflector and crossing have only 2 reviews each. Refs years stop at about 2021-2025, so recent work comes from L1-L3.
- Volume is higher than the "few thousand" expected (9,391 unique uids). Many are pre-2016, off-topic (sensing, chemistry, computing) or theory and textbooks. The S2 prefilter must handle that. Tag-based merging should use `seed_class` and `refs_of_all`.
