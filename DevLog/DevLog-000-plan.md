---
title: Photonics atlas - plan, decisions, TODO (components, supply chain, people)
date: 2026-10-20
status: active (P0 done; P1 back-fill, P2 and P3 foundations in progress as parallel streams, DevLog-002/003/004)
scope: PIC component atlases, supply-chain/vendor atlas, people/affiliation/org atlas, shared registry
authors: Claude (at Wentao Jiang's request)
---

# DevLog-000: Photonics atlas

Origin: drafted in eo-modulator-atlas as DevLog-044 on 2026-10-20, moved here with the research reports after the user decisions below; audit corrections applied (see end).

## Request (2026-10-20)

Expand the EO modulator atlas line of effort to optical interconnects and PICs in general:

1. Component atlases by category (MMI, couplers: grating / edge / PWB / free-space for AMO, ...), with specs per component.
2. Supply-chain and vendor atlas (PIC foundries, SOI/InP/TFLN wafer suppliers, DFB/DBR laser suppliers, epoxies, characterization equipment: PD, UV lamps, microscopes, stages and controllers, reliability testing, ...).
3. People/affiliation/org atlas (e.g. Intel SiPh core contributors and where they went; moves between companies). Extends `PlayGround/20260823_photonics_lineage`.

Data should be shared and presented differently. Initial sourcing: cached papers in eo-modulator-atlas, advanced-packaging-atlas, the blog repo, and the OFC 2026 corpus; open access first.

## User decisions (2026-10-20)

| # | Decision |
|---|---|
| U1 | WDM is its own top-level component category, subcategories AWG, echelle grating (EG), cascaded MZI, MRR (plus Bragg/CDC, interleaver, TFF). |
| U2 | New standalone public repo `photonics-atlas`. |
| U3 | People layer is public for most players. For prominent people, widely reported moves are in scope even when personal-career in nature, because they are public news (user example: Ashkan's move from NVIDIA to ams OSRAM; to be sourced like any other claim). Every claim still needs a public source and an evidence grade. |
| U4 | Public vendor datasheet fetching approved (P2), rate-limited, tiny test first. |

## Exploration inputs (2026-10-20)

Research reports (read-only exploration by four subagents, `research/`):

| Report | Content |
|---|---|
| [component taxonomy](research/2026-10-20-component-atlas-taxonomy.md) | 19 classes including the WDM category, per-class spec fields, 9 binding reporting pitfalls, 68 located example values, schema recommendation, corpus yield, 32 seed refs |
| [supply-chain taxonomy](research/2026-10-20-supply-chain-taxonomy.md) | category tree A-K, per-category specs, 173 vendor/product seed rows with locators, schema sketch, datasheet gaps |
| [people assessment](research/2026-10-20-people-atlas-assessment.md) | shared person/org model, overlap counts, move-detection demo (75 candidates in 62 people), Intel SiPh coverage, tranche plan |
| [blog harvest](research/blog_harvest/2026-10-20-blog-harvest.md) | 1990 identifiers from 144 blog files, 718 OA, 534 OA photonics not in either atlas, top-40 seeds |
| [audit](audits/2026-10-20-devlog-044-audit.md) | fresh-context audit of this plan (71 claims) |

Scripts and small outputs behind those reports: `research/scripts_2026-10-20/` (git-ignored; they hardcode local paths). The reports themselves were scrubbed of local paths.

Corpus inventory (counts 2026-10-20):

| Corpus | Size | Access | Use |
|---|---|---|---|
| eo-modulator-atlas `references/` | 231 text extracts, 293 PDFs; 233 audited papers (54 of them OFC 2026), 519 devices | 119 arXiv + 41 OA + rest | redistribution per licence; largest OA source of component side-data |
| advanced-packaging-atlas `references/` | 296 text extracts; 296 papers, 938 test vehicles | mostly IEEE, local-only | facts + locators; reliability, adhesives, optical interfaces (55 rows) |
| OFC 2026 (`PlayGround/20260320_OFC`, `PlayGround/ofc-2026`) | 677 text extracts; 830 presentation metadata records; 126 local PDFs; all 677 PDFs in a local archive | not OA | facts + approximate locators only; industry-heavy (lasers, WDM, CPO, foundries); affiliation snapshot 2026-03 |
| Blog repo | 128 photonics PDFs in `assets/doc`; 1990 linked identifiers | mixed | seed list; OIF ELSFP / CPO specs, Intel / Ranovus / NVIDIA CPO decks |
| Lineage (`PlayGround/20260823_photonics_lineage`) | 288 people, 172 orgs, 556 edges (491 grade A), 23 events, 282 sources | public web sources | canonical career claims |

Key findings:

- Both existing atlases use the same stack (SvelteKit 3 / Svelte 5, adapter-static, Plotly, GH Pages) and the same data pattern (CSV + `evidence/` + locators + `basis` + distill skill + `build_views.py`). New atlases reuse it.
- Org names do not line up: EO (284) and packaging (144) orgs share 16 names exactly (21 after legal-suffix normalization); OFC has 735 raw affiliation strings (657 normalized by the exploration heuristic; 663 under the DevLog-001 D18 key), 109 exact-match EO. A curated org registry with aliases and org events is the first dependency for everything.
- EO `papers.csv` already holds `foundry_or_fab` (97 papers), `wafer_supplier` (74; NanoLN dominant), `process_name` (151): supply-chain seed data exists.
- EO papers report component side-data (grating/edge coupler loss, MMI, waveguide loss, rings) with `host_device_id` linkage possible; this is the largest audited OA component source.
- Dedicated component papers (lasers, SOA, AWG/WDM, PD) are mostly OFC (non-OA): admit as facts with `p.~N` locators.
- Industry papers anonymize adhesives, fiber arrays and CPO laser die; those categories need public datasheets.
- People: 457 persons with >= 2 orgs across EO + packaging + OFC; 75 candidate moves after org-event and gap filtering, 22 ORCID-backed; Intel SiPh in lineage: 27 people, 4 of 27 Intel edges dated; 11 Intel authors in EO/OFC missing from lineage.

## Architecture

One shared registry, several fact layers, several lenses. Each fact is extracted once, with its evidence, and shown in every atlas that needs it.

```
sources (papers, conference papers, datasheets, filings, bios)  -- source_id, corpus, access, licence
   |
registry (shared)       organizations (+aliases, ROR/QID, org_type, parent)   org_events (acquisition, spin-off, rename, merger)
                        people (+ORCID, variants, person_xref)                sites (lat/lon)
                        products (vendor x model)                             processes / platforms (foundry PDKs)
                        standards (GR-468, JEDEC, IEC, OIF IAs)               category trees (component, supply)
   |
fact tables             devices (EO atlas)            components + component_metrics (long)      test_vehicles... (packaging atlas)
(evidence-backed)       product_usage (paper x product x role)   product_specs (datasheet, long)   reliability_tests
                        affiliation_observations (person x org x date x source x grade)   career_claims (lineage edges)
   |
lenses (one app)        EO modulators | Components (per class, WDM, couplers, ...) | Supply chain (category -> vendor -> product -> used-in)
                        People (org exchange network, person timelines, flows by year, geography) | Org page = hub joining all lenses
                        Packaging atlas linked, not duplicated
```

Shared-data examples: one paper's methods section yields device rows (EO), coupler/WDM rows (components), instrument and wafer usage (supply chain) and dated affiliations (people). An org page shows its papers, devices, components, products, processes and people inflow/outflow.

### Repo layout

- This repo owns: registry, component atlas, supply-chain atlas, people atlas (lineage promoted as its career-claims layer), unified app.
- eo-modulator-atlas and advanced-packaging-atlas stay canonical for their own tables, unchanged. Adapters here read their CSVs (read-only) and map `org_name -> org_id`, `person_id -> person_id` through crosswalk files. Later, optionally, the two atlases consume the registry.
- `PlayGround/20260823_photonics_lineage` stays untouched; its canonical YAML is imported, then this repo is where it grows.

### Data decisions (decided per project conventions; recorded, not asked)

| # | Decision | Rationale |
|---|---|---|
| D1 | Components: one `components.csv` (class, subtype, shared fields) + long `component_metrics.csv` validated by a per-class parameter registry YAML; per-class wide views generated for the app | long format proven by packaging `metrics.csv` (7511 rows); metric sets differ per class |
| D2 | WDM top-level category: `wdm.awg`, `wdm.eg`, `wdm.cascaded_mzi`, `wdm.mrr`, `wdm.bragg_cdc`, `wdm.interleaver`, `wdm.tff`; single resonators stay in `resonator` (Q / loss extraction) | U1 |
| D3 | Loss `scope` enum per component report 2.3 (`per_coupler`, `per_facet`, `per_interface`, `loopback_half`, `fiber_to_fiber`, `on_chip_excess`, `device_total`, `de_embedded`, `unspecified`) with `includes`/`excludes`; measured / simulated / derived / design_target `basis` per value | pitfalls found in corpus (component report 2.2-2.3) |
| D4 | OFC 2026 rows: facts only, local-only text, consistent with EO DevLog-020 #11. New here: `access=paywalled_conference` and approximate `p.~N` locators for the extracted-text corpus (EO used exact PDF pages and `access=unknown` for its 54 OFC papers; reuse those exact locators where the paper is already in EO) | text extracts have no page markers |
| D5 | First component data = back-fill from the 233 audited EO papers (231 with cached text) via `host_device_id`, then OA blog seeds, then OFC | largest audited OA source; no new retrieval needed |
| D6 | Supply chain: extend org registry with `org_type` values (wafer_supplier, materials_supplier, equipment_vendor, instrument_vendor, component_vendor, software_vendor, osat, standards_body); vendor renames/acquisitions (Agilent/Keysight, Finisar/II-VI/Coherent, Cascade Microtech/FormFactor, New Focus/Newport/MKS) are `org_events`, not aliases (supply report 4 proposed `aliases`/`lineage` columns; this follows people report E.2 and lineage `source_policy.md` time-aware entities instead) | time-aware entities |
| D7 | `product_usage` rows quote <= 200 chars of the stated text with locator; `product_specs` from datasheets carry `basis` datasheet_spec / datasheet_typical | traceability rule |
| D8 | IDs: immutable `person_<slug>`, `org_<slug>`, `product_<vendor>-<model>`; ORCID / ROR / QID stored as fields, not keys. Deliberately differs from EO DevLog-020 #2 (ORCID as `person_id` when known); the crosswalk maps EO ids. Never merge people on romanized name alone | slug ids stay stable when an ORCID is found later |
| D9 | Evidence grades reuse lineage A-D, X: paper-printed affiliation A, OFC organizer metadata B (admitted now), LinkedIn C (lineage v0.2 makes it a required discovery source shown only in a separate optional layer; new rule here: manual capture only, no automated scraping), single press item D, derived transition X unless backed by present-address or a dated bio | consistency with lineage v0.2 (2026-08) |
| D10 | Publication affiliation = dated `active_on` observation, never an employment interval; name-only transitions stay in a review queue and are not shown | avoids invented careers |
| D11 | Dates ISO; earliest public date; emails stripped from OFC header extraction | standing rules |
| D12 | Publication (U3): default public view = A/B claims. Moves of prominent people reported by reputable news count as B when the outlet states the move directly (two independent reports, or one plus a company page, preferred); single unconfirmed press items stay D. Non-professional personal data never collected | U3 |

## Plan

Phases run as tranches with a DevLog each, pilot-then-batch, fresh-context audits after each phase. Up to 10 subagents concurrent.

### P0 - Foundation

- [x] Scaffold (uv, ruff, mypy, pytest, Pydantic; SvelteKit app from the existing atlas skeleton); README.
- [x] Registry schema + validator (orphans, enums, date order, grade/status, evidence locators).
- [x] Adapters (read-only): eo-modulator-atlas, advanced-packaging-atlas, lineage canonical YAML, OFC metadata.
- [x] Org registry tranche: crosswalk EO 284 + packaging 144 + lineage 172 + OFC top strings; `org_aliases.csv` hand-curated; `org_events.csv` from lineage events + vendor lineage. Acceptance: every EO/packaging org maps; >= 90% of OFC author rows map.
- [x] Sources table unifying corpora (`eo:`, `pk:`, `ofc2026:`, `blog:`, `ds:` datasheet) with access/licence; dedupe the 54 OFC papers already in EO.

### P1 - Component atlas

- [x] Component parameter registry (YAML) for the 19 classes incl. WDM subtypes; `pic-component-distill` skill + batch contract (mirrors the EO distill skill). (DevLog-002)
- [x] Pilot: 10 diverse EO papers (TFLN, SiPh, SiN, BTO, AMO/visible), audit, fix the contract. (DevLog-002)
- [x] Back-fill from the EO papers (grating/edge couplers, MMI/DC/Y, waveguide loss, rings, WDM), `host_device_id` linked; split ring-filter papers into `wdm.mrr`. (DevLog-002: bf_01-12, bt_01-05, each audited; packaging pk_oi, pk_02)
- [ ] OA seed retrieval (rate-limited, arXiv first) from blog top-40 + component report seeds; ingest.
- [x] OFC 2026 facts-only pass on dedicated component papers (lasers, SOA, WDM, PD, GC, micro-optics). (DevLog-002: ofc_pilot + ofc_01-09, audited; convention sweep + D81 gap-fill)
- [ ] Views: per-class tables; loss vs band per platform; GC CE vs 1-dB BW; edge coupler loss vs MFD; WDM IL / crosstalk vs channel spacing; PD BW vs responsivity.

### P2 - Supply-chain atlas

- [x] Category tree YAML (A-K); `products`, `product_usage`, `product_specs`, `foundry_processes`, `standards`, `reliability_tests` tables. (DevLog-003)
- [ ] Productize the vendor/model scanner (dry-run, JSONL, skip-existing); pilot 10 papers, audit; then EO 231 + packaging 296 + OFC 677.
- [x] Foundry/process and wafer-supplier rows from EO `papers.csv`; reliability tests from packaging `metrics.csv` `test_standard`. (DevLog-003; wafer suppliers missing from the registry staged)
- [ ] Datasheet harvest (U4) for the top ~30 products by usage and the anonymized categories (adhesives, FAU/connectors, ELS lasers, wafers): public PDFs only, rate-limited, tiny test first, stop on anti-bot signals.
- [ ] Views: category -> vendor -> product -> used-in-papers; vendor share by category and year; instrument ceiling vs reported bandwidth (link to EO `bw_measured_to_ghz`).

### P3 - People atlas

- [x] Person registry: EO 1509 base + packaging names + OFC 830-record authors + lineage 288; `person_xref`; review queue for common names. (DevLog-004)
- [x] Observation build + transition derivation + validator; reproduce the 2026-10-20 funnel numbers. (DevLog-004: strict rules give 13 candidate moves vs 75; differences explained)
- [ ] OFC header extraction (677 papers, LLM batches, audit; emails stripped) to get multi-affiliation rows.
- [ ] Intel SiPh pilot: Intel ego view and person timelines; research queue for 11 Intel people with no non-Intel edge, 4 seed-only people, 11 Intel authors missing from lineage (A/B public sources; prominent-people news per D12).
- [ ] Views: org exchange network, person timelines, org-to-org flow by year, geography arcs, coverage panel.
- [ ] Other hubs (Bell Labs, imec/Ghent, Luxtera, UCSB, Infinera, Acacia) and more conference years.

### P4 - Integration

- [ ] Org hub page joining all lenses; cross-links to the EO and packaging atlas sites.
- [ ] Build, smoke tests, screenshots; fresh-context audits (two) of data and UI; README; GH Pages deploy (repo to be created on GitHub by Wentao).

## Audit corrections (2026-10-20, [audit](audits/2026-10-20-devlog-044-audit.md))

71 claims: 51 ok, 14 imprecise, 5 wrong, 1 unsupported. Applied:

- Packaging counts 239 papers / 770 test vehicles / 54 optical interfaces / 5999 metrics -> 296 / 938 / 55 / 7511 (the packaging atlas ingested 57 papers on 2026-10-20 during this work; earlier figures were stale line counts).
- Org overlap EO-packaging: 16 exact, 21 normalized (both stated). OFC affiliation strings 735 raw / 657 normalized.
- D9 "manual capture only" relabelled as a new rule here, not lineage policy; LinkedIn's required-discovery status in lineage v0.2 stated.
- D4, D6, D8 sources and departures from EO conventions stated explicitly; D3 enum aligned with the component report; D1 "disjoint metrics" reworded.
- Counts: 11 Intel authors (not 10), 173 supply seed rows, 68 component examples, 19 classes including WDM, 233 audited EO papers (231 with text).
- Report-level: component report OFC overlap 3 -> 54; supply report foundry fields 233 -> 97/151; people report C.3 marked as a research queue (name-only rows not for display); local paths scrubbed from reports and audit.

## Progress

- 2026-10-20: exploration done (four reports + audit); WDM feedback applied; user decisions U1-U4; repo created locally (`git init`, `main`), research and audit moved here from eo-modulator-atlas. No commit, no remote yet.
- 2026-10-20: P0 done ([DevLog-001](DevLog-001-p0-foundation.md)): registry 864 orgs / 370 aliases / 55 events / 1826 sources; crosswalk EO/PK/LIN 100%, OFC 99.79% of author rows; two fresh-context audits applied.
- 2026-10-20 15:00: P1 back-fill and OFC pass done and audited (554 components, 1791 metrics); P2 supply and P3 people corrections each audited twice and fixed. Details in DevLog-001..004.
