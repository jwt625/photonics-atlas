---
title: Literature lane L1 (journals) harvest report
date: 2026-10-21
scope: DevLog-006 stage S1, lane L1
---

# Lane L1: photonics journals 2016-2026 (OpenAlex venue-year filter lists)

## What ran (2026-10-21, 22:38-23:07 UTC)

- Source resolution: 28 x `/sources/issn:<issn>` (free singleton gets); npj Nanophotonics via one `/sources?search=`
  (ISSN 2948-216X, S5407036647). All 29 requested venues resolve; none dropped.
- Filter measurement for broad journals (group_by, see below), type check (group_by type).
- Script `scripts/lit_harvest_openalex.py`, config `config/literature/venues_journals.yaml`,
  tests `tests/test_lit_harvest_openalex.py` (6 pure-function tests). ruff, ruff format, mypy strict pass.
- Commands:
  - `uv run python scripts/lit_harvest_openalex.py --config config/literature/venues_journals.yaml --dry-run`
  - pilot `... --only optica --years 2026`
  - P1 pass A `... --only <13 core keys> --years 2022-2026 --stop-at-usd 0.072` (stopped at the shared cost line)
  - P1 pass B `... --only <13 core keys> --years 2016-2021 --stop-at-usd 0.072` (stopped before any unit)
- Logs: `logs/lit_harvest_openalex_journals_20261021T*.log|jsonl` (dry-run counts: `..._20261021T154419.jsonl`),
  requests in `logs/litfetch_2026-10-21.jsonl`.

## Filters

- Unit filter: `primary_location.source.id:<id>,type:article|review|letter[,extra_filter],publication_year:<y>`,
  per_page 200, `select=OPENALEX_SELECT`.
- Types: the 28 sources 2016-2026 hold article 598,384, erratum 15,491, other 5,108, paratext 3,444, editorial 3,441,
  review 2,183, book-review 1,542, retraction 716, letter 415, smaller types < 130. `other` in the photonics
  journals is 56 works (LSA 39, OEA 12, Nat Photon 3): news-and-views / highlight pieces, excluded.
- Broad journals (Nature, Science, Nat Commun, Sci Adv, APL, Sci Rep): `topics.id:` any of 20 OpenAlex photonics
  topics (list in the config header). Measured on 2016-2026 article|review|letter:

| filter | works (6 broad journals) | recall on 134 EO-atlas journal papers |
|---|---|---|
| none | 487,340 | - |
| topics.id core 18 topics | 11,937 | 134/134 |
| topics.id core + metamaterials + plasmonics (used) | 18,082 | 134/134 |
| primary_topic.id core + meta | 7,722 | 126/134 |
| primary_topic.subfield.id:3107 | 16,931 | 123/134 for 3107 or 2208 |

  The recall set is modulator-heavy (EO atlas); metasurface / plasmonic topics were kept for free-space emitters and
  micro-optics.

## Venues (expected = dry-run group_by count; harvested as of 23:07 UTC)

| key | venue | source id | priority | years with works | expected | harvested | years done | abstract % | OA % |
|---|---|---|---|---|---|---|---|---|---|
| optica | Optica | S4210197940 | 1 | 2016-2026 | 2607 | 1116 | 5/11 | 98.2 | 100.0 |
| optics_express | Optics Express | S178776955 | 1 | 2016-2026 | 36973 | 17683 | 5/11 | 98.9 | 100.0 |
| optics_letters | Optics Letters | S134390580 | 1 | 2016-2026 | 17794 | 8455 | 5/11 | 99.1 | 17.9 |
| photonics_research | Photonics Research | S2764698263 | 1 | 2016-2026 | 2994 | 1703 | 5/11 | 95.0 | 15.7 |
| apl_photonics | APL Photonics | S4210226744 | 1 | 2016-2026 | 1806 | 1116 | 5/11 | 99.1 | 100.0 |
| jlt | Journal of Lightwave Technology | S2307745 | 1 | 2016-2026 | 10263 | 3118 | 3/11 | 82.9 | 18.2 |
| ptl | IEEE Photonics Technology Letters | S27723657 | 1 | 2016-2026 | 5403 | 0 | 0/11 |  |  |
| jstqe | IEEE Journal of Selected Topics in Quantum Electronics | S192705446 | 1 | 2016-2026 | 2430 | 0 | 0/11 |  |  |
| nature_photonics | Nature Photonics | S120392215 | 1 | 2016-2026 | 2364 | 0 | 0/11 |  |  |
| lsa | Light Science & Applications | S2498964232 | 1 | 2016-2026 | 2579 | 0 | 0/11 |  |  |
| acs_photonics | ACS Photonics | S135184319 | 1 | 2016-2026 | 5535 | 0 | 0/11 |  |  |
| lpr | Laser & Photonics Review | S95928045 | 1 | 2016-2026 | 5077 | 0 | 0/11 |  |  |
| nanophotonics | Nanophotonics | S2737520951 | 1 | 2016-2026 | 3101 | 0 | 0/11 |  |  |
| optical_materials_express | Optical Materials Express | S2496121912 | 2 | 2016-2026 | 3868 | 0 | 0/11 |  |  |
| advanced_photonics | Advanced Photonics | S4210199334 | 2 | 2019-2026 | 565 | 0 | 0/8 |  |  |
| advanced_photonics_nexus | Advanced Photonics Nexus | S4387281427 | 2 | 2022-2026 | 433 | 0 | 0/5 |  |  |
| chinese_optics_letters | Chinese Optics Letters | S112097523 | 2 | 2016-2026 | 2683 | 0 | 0/11 |  |  |
| ieee_photonics_journal | IEEE Photonics Journal | S72499069 | 2 | 2016-2026 | 5248 | 0 | 0/11 |  |  |
| ieee_jqe | IEEE Journal of Quantum Electronics | S80223966 | 2 | 2016-2026 | 1072 | 0 | 0/11 |  |  |
| oea | Opto-Electronic Advances | S2883262519 | 2 | 2018-2026 | 436 | 0 | 0/9 |  |  |
| elight | eLight | S4210205584 | 2 | 2021-2026 | 131 | 0 | 0/6 |  |  |
| photonix | PhotoniX | S3035551292 | 2 | 2020-2026 | 280 | 0 | 0/7 |  |  |
| npj_nanophotonics | npj Nanophotonics | S5407036647 | 2 | 2024-2026 | 137 | 0 | 0/3 |  |  |
| nature | Nature | S137773608 | 3 | 2016-2026 | 655 | 0 | 0/11 |  |  |
| science | Science | S3880285 | 3 | 2016-2026 | 602 | 0 | 0/11 |  |  |
| nat_commun | Nature Communications | S64187185 | 3 | 2016-2026 | 3363 | 0 | 0/11 |  |  |
| sci_adv | Science Advances | S2737427234 | 3 | 2016-2026 | 916 | 0 | 0/11 |  |  |
| apl | Applied Physics Letters | S105243760 | 3 | 2016-2026 | 6416 | 0 | 0/11 |  |  |
| sci_rep | Scientific Reports | S196734849 | 3 | 2016-2026 | 6130 | 0 | 0/11 |  |  |
| total | | | | | 131861 | 33191 | | 97.2 | 67.1 |

- Every harvested unit matched meta.count and the group_by count exactly (0 count mismatches, 0 duplicate uids,
  33,191 records in 28 files `cache/literature/pool/journals_<key>_<year>.jsonl`).
- Dry-run total: 131,861 works, 825 pages, est. $0.0825 (plus 1 group_by request per venue per run).

## Abstract coverage and data anomalies

- Missing abstracts concentrate in the newest year: JLT 2026 459 of 930 (early-access items), OE 2026 177,
  PRJ 2026 84, OL 2026 70, JLT 2025 40, JLT 2024 33; elsewhere < 1 %. IEEE does not deposit abstracts with Crossref,
  so JLT / PTL / JSTQE gaps need another source (or a refresh of OpenAlex later).
- Nanophotonics 2019: OpenAlex has 30 works vs 414 (2018) and 273 (2020) for source S2737520951; the ISSN 2192-8614
  resolves to the same source. Likely mis-assigned works; Crossref by ISSN is the fallback for that year.
- Science broad-filter counts drop from 2022 (21-34 per year vs 62-104 before); not investigated.
- OA % is the OpenAlex `is_oa` value (e.g. Photonics Research 15.7 %, Optics Letters 17.9 %).
- Cursor paging returned HTTP 401 on page 2 without an API key (2026-10-21); the script uses page=N paging (valid to
  10,000 results; the largest unit, OE 2025, is 3,968).

## Cost

- Shared OpenAlex spend 2026-10-21 (all agents) 0.0729 USD at stop; this lane's requests ~0.037 USD (253 requests:
  resolution 0, probes ~0.003, dry-run 0.0029, harvest ~0.031).
- Remaining: 98,670 works, 643 pages (386 of them priority 1) + 29 group_by = ~0.067 USD, i.e. most of one UTC day of
  the shared cap.

## Remaining and resume (after 2026-10-22T00:00Z)

Done: Optica, OE, OL, PRJ, APL Photonics 2022-2026; JLT 2024-2026. Not started: JLT 2016-2023, PTL, JSTQE, Nature
Photonics, LSA, ACS Photonics, LPR, Nanophotonics (priority 1); all priority 2 and 3 venues; 2016-2021 for all.
Resume (skips finished files; priority order; venue-major within each pass):

```
uv run python scripts/lit_harvest_openalex.py --config config/literature/venues_journals.yaml --years 2022-2026 --stop-at-usd 0.075
uv run python scripts/lit_harvest_openalex.py --config config/literature/venues_journals.yaml --years 2016-2021 --stop-at-usd 0.075
```

Restrict to core first with `--only optica,optics_express,optics_letters,photonics_research,apl_photonics,jlt,ptl,jstqe,nature_photonics,lsa,acs_photonics,lpr,nanophotonics`.
