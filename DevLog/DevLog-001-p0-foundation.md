---
title: P0 Foundation - scaffold, registry schema, validator, adapters, org registry, sources table
date: 2026-10-20
status: P0 done (acceptance passed, two fresh-context audits applied)
scope: DevLog-000 phase P0
authors: Claude (at Wentao Jiang's request)
---

# DevLog-001: P0 Foundation

Plan source: [DevLog-000](DevLog-000-plan.md) (U1-U4, D1-D12). This tranche adds data decisions D13-D29 below; they refine, not replace, D1-D12.

## Inputs (read-only)

| Alias | Location (relative to the parent of this repo) | Used for |
|---|---|---|
| EO | `eo-modulator-atlas/data/{organizations,org_sites,author_affiliations,papers,people,paper_authors}.csv` | orgs (284), affiliations, sources (233 papers, 54 of them OFC 2026) |
| PK | `advanced-packaging-atlas/data/{organizations,org_sites,author_affiliations,papers}.csv`, `config/org_aliases.yaml` | orgs (144), affiliations, sources (296 papers) |
| LIN | `PlayGround/20260823_photonics_lineage/canonical/{organizations,events,sources}.yaml` | orgs (172), events (23), sources (282) |
| OFC | `PlayGround/ofc-2026/ofc_full_metadata.json` (`record_kind == presentation`, `authors_json`) | 830 presentations, 6056 author rows, 735 affiliation strings |
| BLOG | `DevLog/research/blog_harvest/local_pdfs.csv` (128 PDFs in the blog repo `assets/doc`) | blog sources |
| ROR | ROR data dump (CC0, Zenodo), cached in git-ignored `cache/ror/` | exact-name lookup for orgs not in EO/PK/LIN |

None of these is edited. Paths live in `config/inputs.yaml` (relative; overridable by `PHOTONICS_ATLAS_INPUTS_ROOT`).

Baseline measured 2026-10-20 before any work: naive normalized-name match of OFC affiliation strings against EO + PK + LIN names/aliases maps 2488 / 6056 author rows (41.1%, 172 strings); 400 most frequent strings cover 91.2% of rows, 185 strings are singletons.

## Data decisions (D13-D25)

| # | Decision | Rationale |
|---|---|---|
| D13 | Registry tables in `data/registry/`: `organizations.csv`, `org_aliases.csv`, `org_events.csv`, `org_event_participants.csv`, `sources.csv`. Schema `data/schema/registry.schema.yaml` is the single source of truth for `scripts/validate_db.py` (EO pattern). Later tables (people, person_xref, sites, products, processes, standards, category trees) are defined in the schema when their phase starts | one schema, validator driven by it |
| D14 | Org ids: LIN `org_*` ids reused verbatim (LIN is absorbed here; its ids are immutable by its schema). New ids `org_<ascii slug of name>` with `_` separators, collision suffix `_2`. Ids never change once written; registry rows are curated data, seed scripts only append | D8, stable keys |
| D15 | `org_type` = institutional kind only, union of EO/PK/LIN: university, academic_lab, company, startup, business_unit, industrial_lab, research_institute, national_lab, government_lab, foundry, facility, consortium, standards_body, venture_fund, other, unknown. Supply-chain roles (D6: wafer_supplier, materials_supplier, equipment_vendor, instrument_vendor, component_vendor, software_vendor, osat; plus foundry_service for contract fabrication offered by an org whose kind is not foundry) go in a separate list column `supply_roles`, filled in P2 with evidence | refines D6: one org holds several roles (a single type cannot); standards_body is an institution kind, kept in org_type |
| D16 | `name` = own preferred English name. `name_basis` records where it came from, priority eo_atlas (researched per EO DevLog-020 #9) > lineage > pk_atlas > ror > printed (most frequent printed form, legal suffix kept as printed). `country` (ISO 3166-1 alpha-2, HK and TW own codes) only from a record that states it (EO/PK/LIN/ROR, or for printed-basis orgs the address in the cited paper header, quoted in notes; amended after the P0 data audit 6.6); otherwise empty | no invented facts; EO convention (e) |
| D17 | Org types for new orgs only from the printed name's own words (University, Institute, Laboratory, legal suffix) or the ROR record; otherwise `unknown` | avoids classification from memory |
| D18 | Name normalization (crosswalk key): NFKD accent strip, lowercase, `&` -> and, punctuation to space, legal suffixes dropped (inc, corp, co, ltd, llc, gmbh, ag, sa, se, bv, nv, plc, limited, kk, ...), whitespace collapsed. Variants that differ only under this key need no alias row. `org_aliases.csv` holds variants the key cannot catch (other language, abbreviation, word order, misspelling, country subsidiary, site- or unit-qualified string, joint affiliation) | aliases stay small and reviewable |
| D19 | Alias rules: `alias_type` in printed_variant, legal_name, native_name, abbreviation, short_name, brand, subsidiary_printed (a national subsidiary or site of a company mapped to the brand org; printed text is always kept in observations), unit_printed (department/lab string mapped to its host org), joint_printed (one string naming two orgs: one alias row per org). An alias string may map to several orgs only as joint_printed. `former_name` is not used: renames are org_events between separate ids (D6) | time-aware entities |
| D20 | Time-aware entities: rename, spin-off, acquisition and merger create separate org ids linked by `org_events` + `org_event_participants` (roles: target, acquirer, predecessor, successor, parent, spun_off, merging, resulting). An acquired org keeps its id (status acquired, `parent_org_id` = acquirer when it survives as a unit) | LIN invariant: acquisition alone never creates a person transition |
| D21 | Dates are ISO partial strings `YYYY`, `YYYY-MM` or `YYYY-MM-DD`; precision is the string length. Events carry `announced_on` and `effective_on` separately; no order is enforced between them (LIN records publication-proxy announcement dates after close), but founded_on <= dissolved_on, valid_from <= valid_to and participant founding before event are checked | LIN date_value without a second column |
| D22 | Event evidence: `grade` (A-D, X), `status` (validated, asserted, inferred, disputed), `source_ids` (`;` list into `sources.csv`), `locator`, `basis` (stated_in_source, imported_lineage). Compatibility: validated needs A/B; C at most asserted; D asserted or disputed; X inferred with a rationale in notes. Imported LIN events cite their LIN sources and locate the claim as `lin:canonical/events.yaml#<event_id>` | lineage v0.2 grade policy; traceability |
| D23 | Sources: one row per source document, `source_id = <corpus>:<native id>` with corpus eo, pk, ofc2026, blog, ds, lin, web. Duplicates point to the canonical row through `same_as`; the 54 OFC 2026 papers already in EO are canonical as `eo:` (exact PDF-page locators, D4), the `ofc2026:` row has `same_as`. Access enum adds `paywalled_conference` and `public_web`; EO/PK values are copied as their atlas records them (EO's 54 OFC rows stay `unknown` there; the `ofc2026:` row says `paywalled_conference`). No PDF or text is copied into this repo | D4, D7 |
| D24 | OFC adapter: one observation per `authors_json` element; date = local date of `session_start`; grade B (D9); emails stripped (regex) from every text field before anything is stored; `presenter_affiliation` ignored (empty on all records) | D9, D11 |
| D25 | Crosswalk files in `data/crosswalk/` are generated (never hand-edited) from the registry + aliases: corpus, printed string, org_ids, match basis (name, alias, ror, unmapped), rows. Manual decisions live only in `organizations.csv` / `org_aliases.csv`. ROR is used offline, exact normalized match on names/labels/aliases only (acronyms only through curation); no fuzzy matching (people report B.2: Calient/Ligent, Korea/Kobe false near-matches) | one source of truth; no similarity guesses |
| D26 | (added during the tranche) Event dates: `announced_on` = first public announcement found (press-release dateline or filing); a separately signed agreement date goes to notes when known (group B rows used the agreement date, which coincides or precedes by a day; noted per row). `effective_on` from the most primary source; a day that only a sub-unit page or a planned date gives is reduced to the month (Osaka, NTT) | earliest public date (D11) without over-precision |
| D27 | (added) Time-aware orgs whose normalized names collide with a current org (Coherent, Inc. vs Coherent Corp.; Broadcom Corporation / Broadcom Limited vs Broadcom Inc.; Xperi Inc. vs PK "Xperi") carry `no_name_match = true`: their names never route crosswalk strings; event participants resolve only through the hand-curated `config/event_participant_map.yaml`. ROR auto-match uses display names and labels only, never ROR alias fields or bare acronyms of <= 4 characters (subsidiary records carry the parent brand: Ajinomoto, CNRS, IDT, TI hits were wrong) | identity safety |
| D29 | (added after the P0 audits) Registry `country` = country of the org's own record (ROR when ror_id is set); a printed site country that differs (EO printed addresses: Ciena CA, Nokia US) stays in the observation layer. Country codes are checked against the ISO codes in the pinned ROR dump (`data/schema/country_codes.txt`) | one country per org; sites carry locations |
| D28 | (added) Aliases may carry a `scope` (corpora where they apply) for strings unambiguous only inside one input (EO "Institute of Microelectronics" = A*STAR IME; OFC "Swiss Federal Institute of Technology" = EPFL per header) | context-dependent strings |

## TODO

- [x] 1. Scaffold: `pyproject.toml` (uv, Python 3.12, ruff, mypy strict, pytest, Pydantic v2), package `src/photonics_atlas/`, `config/inputs.yaml`, README, `.gitignore` additions.
- [x] 2. App: SvelteKit app copied from the EO atlas skeleton (layout, theme toggle, tooltip, paths, css), pnpm; dashboard (registry counts, crosswalk coverage) + org table; `scripts/build_views.py` -> `app/static/data/registry.json`.
- [x] 3. Schema `data/schema/registry.schema.yaml` + `scripts/validate_db.py`: columns/types/enums, id patterns and uniqueness, orphans (parent, alias, participants, sources, crosswalk, same_as), ISO date format and order, grade/status compatibility, evidence locators; tests.
- [x] 4. Adapters (read-only) `src/photonics_atlas/adapters/{eo,pk,lineage,ofc,blog}.py` with typed records; email stripping; tests on real data.
- [x] 5. ROR dump: tiny metadata test, single download to `cache/ror/`, local index.
- [x] 6. Org registry seed (`scripts/seed_org_registry.py`): pilot on diverse rows (Intel/NTT/Harvard from EO, Intel/TSMC from PK, Coherent/II-VI/Finisar from LIN), then full; merge review.
- [x] 7. Crosswalk (`scripts/build_org_crosswalk.py`) + ROR pass for OFC strings; unmapped list.
- [x] 8. Curation of unmapped OFC strings (subagent batches -> `data/_staging/org_curation/`, merged by script after review).
- [x] 9. Org events: LIN 23 imported; vendor lineage researched from primary sources (Agilent/Keysight, Finisar/II-VI/Coherent, Cascade Microtech/FormFactor, New Focus/Newport/MKS, others the crosswalk exposes); PK alias-file events (Xperi/Adeia, Showa Denko Materials/Resonac, Tokyo Tech/Institute of Science Tokyo).
- [x] 10. Sources table (`scripts/build_sources.py`): eo, pk, ofc2026, blog, lin; `same_as` for the 54 OFC papers.
- [x] 11. Acceptance: every EO and PK org maps; >= 90% of OFC author rows map; validator 0 errors; tests pass; app builds; screenshot.
- [x] 12. Fresh-context audit subagents (data; code/privacy); corrections applied and recorded below.

## Script conventions

All writers: `--dry-run` (compute and report, write nothing), timestamped log `logs/<script>_<YYYYMMDDTHHMMSS>.log`, JSONL progress `logs/<script>_<ts>.jsonl` (step, counts, status), skip-existing/append-only for curated tables, `--limit`/`--only` for pilots.

## Progress

- 2026-10-20: inputs read (DevLog-000, research reports, audit, EO/PK atlases, LIN canonical YAML, OFC metadata); baseline coverage measured; this plan written.
- 2026-10-20 12:06: scaffold (uv 0.7.16, Python 3.12, hatchling package `src/photonics_atlas`, ruff/mypy strict/pytest). ROR dump v2.15-2026-10-20 (Zenodo record 23500708, CC0, md5 verified) cached in `cache/ror/` after one metadata query.
- 12:10: schema v1 + validator; adapters reproduce the inventory counts exactly (EO 284/2880/233, PK 144/1996/296, LIN 172/23/282, OFC 830/6056/677 cached texts, blog 128).
  - Note (2026-10-22): PK input changed upstream (advanced-packaging-atlas commit b1daf52, 2026-10-22 00:26, affiliations for 57 more papers): PK now 181 orgs / 2405 affiliation rows / 296 papers (EO, LIN, OFC, blog unchanged). `tests/test_adapters.py` updated. The org crosswalk was not rebuilt: 36 of 174 PK affiliation strings (115 of 2405 rows) have no crosswalk row; none of the 37 new `organizations.csv` names has a PK crosswalk row (9 of them equal an existing registry name or alias, case-insensitive).
- 12:12-12:16: seed pilot on 9 orgs (Intel, NTT, Harvard, TSMC, Coherent, II-VI, Finisar, Intel SiPh group, Nokia Bell Labs) exposed (a) an alias equal to another org's name ("Bell Labs" brand of Nokia Bell Labs vs LIN's historical Bell Labs) -> skipped with a log entry; (b) ROR exact-name hits via ROR alias fields / acronyms were wrong for 5 orgs (Ajinomoto -> Okinawa Ajinomoto, ASM International country mismatch, CNRS -> CNRS-AIST JRL, IDT -> Asiana IDT, TI -> TI Asahi) -> D27 rule. Merge review: EO-PK 21, LIN-EO 30, LIN-PK 11 merges (equal to the people-report overlap counts); manual decisions in `config/org_seed_overrides.yaml` (Penn State merge; EO "Institute of Microelectronics" = A*STAR IME, LIN name used; 7 name-stated parents; Ligent, Tokyo Tech vs Institute of Science Tokyo, Sun Yat-sen vs National Sun Yat-sen kept apart). Seed: 542 orgs, 74 aliases.
- 12:17: crosswalk v1: EO/PK/LIN 100%, OFC 44.5% of author rows. ROR pass (`add_ror_orgs.py`, country-subsidiary records become `subsidiary_printed` aliases of the brand org): +116 orgs, +21 aliases, OFC 60.6%; 417 strings (2387 rows) staged.
- 12:18-12:28: 4 curation subagents (contract `data/_staging/org_curation/INSTRUCTIONS.md`, alphabetical batches, OFC paper headers used for disambiguation, no web): 417 decisions -> 174 new orgs, 274 aliases, 5 strings skipped (12 rows, `skipped.csv` review queue). Coordinator corrections in `config/org_curation_overrides.yaml`: Southeast University -> CN record (inferred from co-affiliations, noted); "Swiss Federal Institute of Technology" scoped to ofc2026; ZTE state key lab given its own ROR record (05cd55294, parent ZTE) instead of mapping to ZTE; Lightera Laboratories parent Lightera; ROR-pass duplicate `org_yangtze_optical_fibre_and_cable_joint_stock` folded into LIN `org_yofc`.
- 12:06-12:24: 3 org-event research subagents (groups A test/tool vendors, B optical components/networking, C materials/academic): 37 events staged with 65 sources (mostly primary: SEC filings, company releases, exchange notices, university pages; also a law-firm release graded C, an industry newsletter graded B and newswire reposts); 32 promoted, 5 excluded (`config/event_participant_map.yaml`: CYCLOTENE product-line rows -> P2, a planned-only Fujitsu transfer, two undated renames). Participants resolved by a hand-curated map (time-aware names collide), 33 orgs created from cited sources.
- 12:29: final build. Registry: 864 orgs (428 with ROR id, 722 with country), 370 aliases (seed 74 + ROR pass 21 + curation 274 + 1 ROR legal-name alias added by the YOFC fold), 55 events (23 LIN imported + 32 researched; grade A 53, B 2), 116 participants, 1834 sources (eo 233, pk 296, ofc2026 830 incl. 54 `same_as` EO, blog 128, lin 282, web 65). Crosswalk: EO 284/284 strings (2880/2880 rows), PK 144/144 (1996/1996), LIN 172/172, OFC 729/734 strings, 6043/6056 author rows = 99.79% (incl. the one empty affiliation). Acceptance PASS.
- Verification run: `validate_db.py` 0 errors, 1 warning (eo:powell2024 year vs published_on, documented EO exception DevLog-020 #1); `pytest` 19 passed; ruff + ruff format + mypy strict clean; `pnpm check` 0 errors, `pnpm test` 2 passed, `pnpm build` ok; screenshots of `/`, `/orgs#org_intel`, `/orgs#org_ii_vi`, `/about` from a local preview (port 47391), no console errors. UI fixes found by the screenshots: org detail ignored hash changes; coverage table and org-type panel clipped.

- 14:05: org curation round 2 (requests from P1 component batches and the P2 supply seed; staged by a subagent as `data/_staging/org_curation/batch_5/decisions.csv`, 33 rows): +25 orgs (NanoLN variants -> one org `org_jinan_jingzheng_electronics`; Stanford SNSF and SNF as separate facility orgs under Stanford, nano@stanford being their later merged successor; AIM Photonics TAP facility; standards bodies ISO, ASTM, ASME by ROR and JEDEC, AEC, IEC, IPC, Telcordia as printed; suppliers JePPIX, CrysTec, Grolltex, NGK Insulators, Novel Si, Soitec, Soluxra, UK national epitaxy facility; facilities ScopeM, KNMF, ARIM, CNCD; SJTU-Pinghu Institute), aliases SIMIT-CAS and IBM Bromont; Shin-Etsu (ambiguous ROR) and DTU Nanolab (training thanks only) skipped. The acronym-named bodies produce no crosswalk hits (checked after the rebuild).
- 14:12: round 3 (coordinator, `batch_6`, printed strings from the OFC texts): +8 orgs (SITRI, Tower Semiconductor, UBC SBQMI Advanced Nanofabrication Facility, UCSB Nanofabrication Facility, Marvell Nanofabrication Laboratory, Center for Nano-Micro Manufacturing, SUSTech Core Research Facilities, Alphion), alias Intel Fab11x -> Intel; `org_aim_photonics` gets ROR 01cb8vz90 (verified offline in the pinned dump). Registry 897 orgs. Crosswalk acceptance PASS unchanged (OFC 6043/6056).

- 2026-10-22 22:08-22:18: org curation round 4 (PK input b1daf52, 2026-10-22; supply org requests). Backup zip of
  data/registry, data/crosswalk, data/supply, data/_staging/{supply,org_curation} and config taken first (private
  scratch). PK data unchanged since b1daf52 (checked in the PK repo log). Every writer dry-run first, rows inspected.
  - Seed (`seed_org_registry.py`): +28 PK orgs, 0 aliases; the other 9 of the 37 new PK names already equal a registry
    name (Beijing Institute of Technology, Eindhoven University of Technology, Instituto de Telecomunicações, MIT, NEC,
    NICT, Thales Alenia Space, Tyndall National Institute, Yonsei University). ROR ids on 18 of the 28: 10 by the
    seed's exact-name lookup (Agency for Defense Development, Beijing Academy of Quantum Information Sciences,
    Bridgewater State, Central South, Georgia Tech Research Institute, Luleå, UCC, Aveiro, Oulu, VUB), 8 by D200
    `ror_ids` overrides (Apic Yamada, MIRISE Technologies, Northrop Grumman, Onto Innovation, Panasonic, Socionext,
    Sumitomo Bakelite, TAZMO). Without ROR id (no exact record): Applied Materials Singapore Technology, Changsha
    Anmuquan Intelligent Technology, Hytek, IMT, LIG Nex1, LPKF Laser & Electronics, OUME Electronics, Panasonic
    Industry, Panasonic System Networks R&D Lab., Somacis. Parents from PK: Applied Materials Singapore Technology ->
    Applied Materials, GTRI -> Georgia Tech, both Panasonic units -> Panasonic. No near-duplicate in the registry
    (keyword grep of every new name against organizations / aliases; no new name key equals an existing alias key).
  - ROR pass (`add_ror_orgs.py --dry-run`): 0 new orgs / aliases (still 5 unmapped OFC strings, 12 rows); not run
    for real (it would only write a new unmapped file).
  - Curation (`merge_org_curation.py`): +1 org `org_shin_etsu` (D203, override row in
    `config/org_curation_overrides.yaml`, which also drops the batch_5 skip from `skipped.csv`: 6 strings / 14 rows
    remain). No new batch directory: after the seed every PK string maps, so the only open decision was the batch_5
    skip, overturned the way Southeast University was (override row).
  - Corrections (`apply_registry_corrections.py`): 12 changes (D201 IMT no_name_match + pk-scoped alias; D202 Tyndall
    parent UCC; D200 origin gains pk on the 9 existing orgs, needed by `tests/test_crosswalk.py`); second run 0.
  - Crosswalk (`build_org_crosswalk.py`): PK 144 strings / 1996 rows (committed file, built from the pre-b1daf52 input;
    against the current input 138 of 174 affiliation strings, 2290 of 2405 rows = 95.2 %) -> 181 / 181 org names,
    2405 / 2405 rows (100 %); 37 PK rows added (36 affiliation strings + University College Cork with 0 rows), n_rows
    updated on 38 existing PK rows, no EO / LIN / OFC row changed (diff against HEAD). Acceptance PASS.
  - Registry: 897 -> 926 orgs (452 with ROR id, 766 with country), 395 -> 396 aliases.
  - Decisions (range D200-D209, shared with DevLog-003):

    | # | Decision |
    |---|---|
    | D200 | PK orgs whose ROR record carries a trailing " (Country)" disambiguator (and a legal suffix) get the ROR id through `config/org_seed_overrides.yaml` `ror_ids` only when the display name minus the disambiguator has the PK name's normalized key, the record is active and its country equals the PK country. Existing orgs that a new PK name maps to by name get `pk` in `origin` (registry correction; the seed is append-only) |
    | D201 | A PK org printed as a bare acronym without full name ("IMT", Rome) is `no_name_match` and mapped through a pk-scoped alias, so other printed "IMT" strings stay unmapped. No ROR id ("IMT Srl (Italy)" is not stated by PK) |
    | D202 | Tyndall National Institute parent = University College Cork (PK parent_org and ROR 007ecwd34 parent relation) |
    | D203 | "Shin-Etsu" (eo:witmer2020 SOI supplier, batch_5 skip): a brand-level org named as printed, type unknown, no country, no ROR id, no parent (ROR has only specific Shin-Etsu companies; which one supplied is not stated). Same pattern as PK's brand-level Panasonic |
    | D204 | (supply, DevLog-003) witmer2020 Shin-Etsu wafer_supply row category A1 by a per-paper `wafer_categories` override: EO devices.csv substrate "float-zone SOI (Shin-Etsu)" |

  - Verification: ruff, mypy clean; pytest 201 passed, 4 failed, validate_db 115 errors: all are
    `data/people/affiliation_observations.csv` rows with empty org_id for exactly the 115 newly mapped PK rows
    ("org_id '' contradicts the crosswalk") and the people rebuild tests; they clear when `build_people.py` is re-run
    (coordinator sequences it; data/people not touched here). 0 errors outside affiliation_observations.

- 2026-10-22 23:08-23:20: org curation round 5 (requests: supply vendor scanner pilot, lit distill batch reports and
  audits lit_01-lit_06, OFC header org requests, Intel SiPh pilot). Backup zip of data/registry, data/crosswalk,
  config, data/_staging/{org_curation, supply/org_requests.csv, components/lit_0*}, data/components taken first
  (private scratch). No network: ROR = the pinned local dump; event sources could not be fetched.
  - Decisions staged as `data/_staging/org_curation/batch_7/decisions.csv` (92 rows: 75 new_org, 11 alias, 6 skip),
    merged by `merge_org_curation.py` (dry-run first; second run 0 / 0). +75 orgs, +20 aliases, +6 skipped strings.
    Routes: 28 orgs named from an exact ROR record (supply 19, component 7, OFC 1, Intel 1); 44 printed (supply 29,
    component 15, incl. ams AG, whose ROR id was dropped by D312); 3 cited_source (Intel pilot web sources).
  - Corrections (`apply_registry_corrections.py`): 2 changes (D275 on `org_national_research_council`); second run 0.
  - Crosswalk (`build_org_crosswalk.py`): 0 rows changed (diff against the previous file empty; the new names and
    aliases match no EO / PK / LIN / OFC metadata string). Acceptance PASS (OFC 6043 / 6055 rows).
  - Requests marked: `data/_staging/supply/org_requests.csv` 56 of 57 open vendor rows resolved by the registry
    matcher (status / resolved_org_id; 79 / 80 rows resolved overall), TFS stays open with the D278 note;
    `data/_staging/people/ofc_headers/org_requests_resolution.csv` (9 resolved, 1 rejected);
    `data/_staging/people/intel_pilot/orgs_resolution.csv` (4 new orgs).
  - Effects for the coordinator: OFC header rows that map now under the `ofc_headers.map_org` rules: 39 of 5370
    (unmapped -> mapped, none re-pointed): pilot 22, ofc_h01 1, ofc_h02 2, ofc_h04 7, ofc_h12 1, ofc_h13 6 (re-check /
    aggregate and `build_people.py` pick them up). `build_supply_staging.py pilot_01 --dry-run`: 113 usage rows staged,
    1 held (TFS), 1 error: product id collision `product_comsol-comsol-multiphysics` printed "COMSOL Multiphysics"
    (eo:didier2026) vs "Comsol Multiphysics" (pk:tcpmt.2025.3533388), now one vendor; needs a review harmonization
    (D206 am.) before the supply merge.
  - Component fab / facility (D277): `coord2.yaml` per lit batch applied with `patch_component_staging.py` (dry-run,
    then apply, second run 0 changes) on top of the current staging CSVs (patch, coord, gapfill, sweep2 already in
    them and merged at 23:02, staging == merged before the run), then `merge_component_staging.py <batch> --replace`
    (dry-run 0 errors each). `data/components`: 26 component rows changed (fab_org_ids 20, facility_org_ids 13,
    notes 26), 0 metric rows changed, row order unchanged.
  - Registry: 926 -> 1001 orgs (481 with ROR id, 803 with country, 48 with supply_roles), 396 -> 416 aliases, events
    unchanged (55). After the audit fixes (D310-D315, below): 480 with ROR id, 49 with supply_roles, 416 aliases.
  - Code: origin enum gains `lit` (schema) and the `printed` name basis accepts it (validator);
    `merge_org_curation.py` reads optional decision columns (origin list, scope, valid_from, name_source,
    supply_roles, no_name_match), keeps origin in enum order, writes a scoped alias even when its key equals the org
    name, and unifies a proposed id that already exists (re-runs of no_name_match orgs were not idempotent); the
    validator no longer flags such an alias of a no_name_match org as redundant (IMT, FEI, ams AG).
  - Decisions (range D270-D279):

    | # | Decision |
    |---|---|
    | D270 | Orgs and aliases first printed in the `lit` corpus get origin `lit` (enum extended); `printed` name basis accepts origin lit. Curation decisions may carry origin (list), scope, valid_from, name_source, supply_roles and no_name_match columns |
    | D271 | Vendor brands with several ROR country records: the brand-level org takes the ROR record that is active, has no parent and is the parent of every other active record with the same key (display name minus the " (Country)" disambiguator equal to the printed key); country and type from it (Thorlabs US, Rohde & Schwarz DE, Oxford Instruments GB, Tektronix, Bruker, Veeco, Nordson, Ansys US, Honeywell US). A single active same-key record is used directly (Schott, Amonics, Active Technologies, OZ Optics, Keyence, Hitachi High-Tech, Senju, Samco, Santec, Panasonic Connect). Two parentless same-key records (Comsol US / GB) -> no ROR id. Extends D200 to sources that print no country |
    | D272 | `supply_roles` on the vendor orgs from the staged supply review (`data/_staging/supply/products/pilot_01/review.csv`, true candidates): H -> instrument_vendor, G and F -> equipment_vendor, J -> software_vendor, E -> materials_supplier, D -> component_vendor, A7 -> wafer_supplier, C -> component_vendor (added by D312); evidence (source ids, pages) in the org notes. Only for orgs created from the vendor requests |
    | D273 | Printed-only vendors: org named as printed (legal suffix kept as printed; type company only with a legal suffix, else unknown; no country unless printed). Product brands whose owner is not printed in any cached text (Loctite, EPO-TEK, Delo, Allied) are brand-level orgs (D203 pattern). An abbreviation printed elsewhere in the corpus with its company gets the company org plus a corpus-scoped abbreviation alias: "PI" -> Physik Instrumente (PI) SE & Co. KG (eo:bankwitz2026 p.19), "SHF" -> SHF Communication Technologies AG (eo:cai2025 p.6; lit:starnault2026 p.10 prints "SHF 806E ... (SHF Communication Technologies)"). "FEI" (pk) is a bare three-letter company name: D201 pattern (no_name_match, pk-scoped alias; ROR FEI records all withdrawn). "Lumerical" (eo:tiberi2025) -> org Lumerical Inc., the company tiberi2025 cites (ref. [114], p.20); not an alias of Ansys (vendor as of the source; the transaction is not sourced). "MenloSystems" -> ROR Menlo Systems (DE) as a curated printed variant (the two ROR words joined). SENJU / MUSASHI: reviewer short forms of printed company names -> pk-scoped short_name aliases (withdrawn by D311) |
    | D274 | Component fab / facility orgs: facility orgs named as printed with the printed host as parent (GWNIC -> GWU, Micro-Nano Fabrication Unit at Technion -> Technion, MIT Microsystems Technology Laboratory -> MIT, SIMIT material-device and characterization platform -> SIMIT, ShanghaiTech Material and Device Lab -> ShanghaiTech); no parent when the host is not printed (Micronova Nanofabrication Centre). C2N: identified by the English label of ROR 00zay3w86 (printed form minus the acronym), named by the ROR display name "Centre de Nanosciences et de Nanotechnologies" (registry convention for ROR-named orgs; wording corrected by D311), type facility -> research_institute, parent org_cnrs (printed, and the only ROR parent in the registry). ams AG: printed name, no_name_match + lit-scoped alias (bare key "ams"); its ROR id 03vz6gs79 was dropped by D312. ams OSRAM International GmbH (Regensburg) is a separate org (time-aware; relation not sourced). Dow Corning Corporation (2013, Midland US) as printed; its withdrawn ROR record not attached. NIST CNST printed misspelled ("Nanosacle") -> ROR 00tbs6p91 by the NIST prefix and acronym CNST under NIST (curated, alias kept as printed) |
    | D275 | `org_national_research_council` is Italy's CNR (ROR 04zaypm56): `no_name_match` (the bare English name also denotes National Research Council Canada, now `org_national_research_council_canada`, and others); maps through its aliases; notes state CNR Italy. No crosswalk row matched it by name |
    | D276 | OFC header requests: spelling / language variants -> unscoped aliases of the existing org (BUPT form, Optical valley laboratory -> Optics Valley Laboratory (Wuhan), Technical University of Berlin, UC at Davis, UCAS singular, WEST Aquila S.r.l.); bare acronyms -> ofc2026-scoped abbreviation aliases with header + metadata evidence (TIM -> Telecom Italia, UPC -> UPC Catalunya); University of Connecticut new by ROR |
    | D277 | coord2.yaml rulings (from the batch reports / audits): ronn2019 7 rows fab C2N + facility Micronova (lit_01 audit Q2); mu2026 LD fab ams OSRAM International; dangel2013 rigid WG fab Dow Corning; heim2025 coil fab Honeywell, borderline (lit_02 audit ruling 5); oz2023 2 rows facility MNFU at Technion; meng2023 3 rows facility GWNIC; yue2026 facility SIMIT platform + SMDL; nevlacsil2020 6 rows fab ams AG (lit_05 audit Q2); ye2023 4 rows fab Qaleido (lit_06 audit Q1). Not assigned (no ruling): bock2010 (NRC Canada / U Ottawa authors), mehta2016 (MIT MTL staff thanks), sheng2012 (passive wording) |
    | D278 | Rejected: TFS (expansion not printed in any cached text; the didier2026 FIB row stays held); the bare "State Key Laboratory of Optical Fiber and Cable Manufacture Technology" header string (host differs by paper, as the batch_4 skip); Colleges of Nanoscale Science and Engineering (kim2019; affiliation only, host relation time-dependent and unsourced); Berkeley Wireless Research Center (support thanks); "Nanostructures Lab" (mehta2016; printed without its host); CMAM (garciablanco2025; RBS beam time, characterization only); LioniX BV (hosseini2015; affiliation only, time-aware vs LioniX International BV) |
    | D279 | Intel pilot orgs: printed names from the staged web sources, name_basis cited_source, origin web, name_source = the staged source key (rows not yet in sources.csv); University of Pennsylvania by ROR. Numonyx country left empty (the printed address is a site) |

  - Org events: none added (no cited source reachable offline). Candidates to research with primary sources before
    any event row: ams AG later names and the ams / OSRAM transactions (ams AG, ams OSRAM International GmbH);
    Lumerical Inc. and Ansys; FEI and Thermo Fisher Scientific; Numonyx formation and its later owner (the pilot
    staged a 2011 "Micron" print for one of the Numonyx authors); Dow Corning and the registry Dow orgs; Université
    Paris-Sud and Université Paris-Saclay (C2N parents); LioniX BV and LioniX International BV; CNSE and its SUNY
    hosts; Grace Semiconductor Manufacturing Corporation later history; Agility Communications later owner.
  - Audit (fresh context, [record](audits/2026-10-22-org-round5-audit.md)): 1 wrong (W1: D275 bypassed by the ROR
    display route of the matcher), 7 imprecise (C2N naming wording, CNST founded_on, Qaleido type, Schott role after
    D296, SENJU / MUSASHI aliases, lit_03 resolution string), open questions 1-6. Fixed 23:40-23:46 after a second
    backup zip (`backup_round5b_*`, private scratch): registry restored to its pre-round-5 rows (= HEAD), batch_7
    regenerated with the fixes, merge (dry-run, then real, second run 0 / 0), corrections (2 changes, second run 0),
    crosswalk rebuild (0 diffs, acceptance PASS). Net registry change against the first round-5 state: org_ams_ag loses
    ROR id / status / founded / QID / website (status unknown), org_qaleido_photonics type unknown, org_schott
    materials_supplier, org_ams_osram_international component_vendor, org_lumerical and org_allied no_name_match with
    eo-scoped printed aliases, CNST founded_on empty; aliases SENJU / MUSASHI removed, Lumerical / Allied added.
    Supply requests "SENJU" / "MUSASHI" reopened with a note (the review lines must carry the printed company
    strings; review.csv is the supply stream's file). OFC header rows: the stored header_rows.csv files (5478 rows,
    re-checked by the OFC stream after round 5) equal the current `map_org` result (0 differences); "National
    Research Council (NRC)" with Ottawa now maps to nothing (was CNR via the ROR route).

    | # | Decision |
    |---|---|
    | D310 | (audit W1) `orgmatch.load_matcher` skips the ROR display / label route for no_name_match orgs (their ROR display is their name). Test `test_no_name_match_org_not_routed_by_ror_display`. Crosswalk unchanged (the 13 `ror` rows point to no no_name_match org) |
    | D311 | (audit I1-I6) C2N wording in D274 (identified by the English label, named by the ROR display, convention kept); CNST founded_on emptied (ROR 1901 = NIST, override in `config/org_curation_overrides.yaml`); Qaleido org_type unknown (D17: type only from the name's words or ROR, the p.12 "start-up" stays in notes); Schott supply_roles materials_supplier (E8 per D296); SENJU / MUSASHI aliases removed (never printed alone; only printed forms are aliases); lit_03 `org_resolution.csv` printed string verbatim ("Nanosacle") |
    | D312 | (audit Q1-Q3, Q5) bock2010 fab_org_ids stay empty (D72: authors split NRC Canada / U Ottawa, the fabricating place not stated). Lumerical Inc. and Allied: no_name_match + eo-scoped printed alias (FEI treatment; a bare print in another corpus / year is not routed). ams AG: ROR id dropped (03vz6gs79 records the current group; the as-of-source 2020 name is kept, renames / successor listed for a sourced event). ams OSRAM International GmbH: supply_roles component_vendor (lit:mu2026 C1 laser_source line, D296); D272 gains C -> component_vendor |
    | D313 | (audit Q6) The ROR adapter takes labels / aliases / acronyms from the JSON dump (`cache/ror/<version>-ror-data.json`, one object per name) when it is cached next to the CSV; the CSV joins variants of one language group with ", " and cannot be split safely, so without the JSON the adapter keeps the "; " split (gap stated in the code). Effect: e.g. "National Research Council of Canada" now matches ROR 04mte1k06. Crosswalk 0 diffs; test `test_ror_labels_split_from_json_dump` |

  - Verification after D310-D313 (23:46): ruff, mypy clean; validate_db 0 errors, 15 warnings; pytest 298 passed,
    0 failed (full suite, incl. the 2 new crosswalk tests).
  - Verification (23:24): ruff, mypy clean; validate_db 0 errors, 15 warnings (was 18: the redundant-alias warning
    no longer fires for no_name_match orgs); pytest (without tests/test_supply_scan.py) 264 passed, 4 failed. All 4
    failures are `tests/test_ofc_headers.py::test_mutation_is_caught` cases (marker checks D246 / D286d); they come
    from the concurrent edit of `scripts/ofc_headers.py` / `tests/test_ofc_headers.py` by the OFC header stream, not
    from registry data. `tests/test_supply_scan.py` fails at collection on `config/supply_scanner.yaml` (being edited
    by the supply stream at 23:24); it passed (11 / 11) at 23:20 against this registry. Per-batch request resolutions:
    `data/_staging/components/lit_0N/org_resolution.csv`.

- 2026-10-23 00:23-00:50: org curation round 6 (requests: OFC header `org_requests.csv` after D300-D305, 127 rows /
  121 printed strings / 588 header rows; supply vendor requests still open after the scanner pilots, 29 rows). Backup
  zip of data/registry, data/crosswalk, config, data/_staging/{org_curation, people, supply/org_requests.csv} and
  data/people first (private scratch, `backup_round6_*`). No network: ROR = the pinned local dump; OFC headers read
  from the cached extracted texts. (Correction, D339: the round-6 evidence did copy address text from
  the headers; scrubbed to org / unit / city / country at 01:30.)
  - Decisions staged as `data/_staging/org_curation/batch_8/decisions.csv` (147 rows: 66 new_org, 77 alias, 3 joint,
    1 skip; generator kept in private scratch). Two older skips overturned by override rows in
    `config/org_curation_overrides.yaml` (same spec as batch_8): "University of Georgia" (batch_4) and the bare
    "State Key Laboratory of Optical Fiber and Cable Manufacture Technology" (batch_4, D278). Merge dry-run, real run,
    second run 0 / 0; no unify event for a batch_8 id; no unresolved parent. The first real run used ids that kept
    legal suffixes (`org_qxp_technology_inc`, ...); the registry, crosswalk and header files were restored from the
    backup and the merge re-run with suffix-free ids (contract rule 8) before anything else read them.
  - Registry: 1001 -> 1067 orgs, 416 -> 511 aliases, events unchanged. New orgs by route: OFC exact ROR record 22
    (+3 campus rows, D334), OFC curated ROR route 3 (UBA, Lab-STICC, ARTEMIS), OFC printed 12 (incl. the SKL, D336);
    supply ROR 5, supply printed 21. Corrections (`apply_registry_corrections.py`): 0 changes.
  - Crosswalk: 2 OFC metadata strings / 8 rows unmapped -> mapped (the bare SKL string 6 rows, University of Georgia
    2 rows); no other row changed (diff against the pre-round file). OFC 6043 -> 6051 of 6055 rows. Acceptance PASS.
  - OFC headers (`ofc_headers.py check all`, `aggregate`): 0 errors, 48 warnings (unchanged). 587 of the 588
    unmapped header rows now map (pilot 1, h01 50, h02 54, h03 25, h04 39, h05 46, h06 45, h07 49, h08 43, h09 18,
    h10 34, h11 32, h12 58, h13 39, h14 33, h15 21); 0 rows re-pointed or lost; 4 rows keep their orgs with match
    basis `alias:unit_org` -> `alias` (Th3F.3 imec-Ghent University). Slot outcomes: agree 3919 -> 4268, unmapped
    381 -> 1, conflict 11 -> 16, extra 422 -> 448. The 5 new conflicts are header orgs the metadata does not name
    (Photonext Center x3 for G. Rizzelli, QXP Technology for B. E. Little, University of Maryland, College Park + Duke
    for N. M. Linke). `org_requests.csv` now holds 1 row (UNIDEF, D337).
  - People: `build_people.py --dry-run` gives 6922 persons, 0 new, but 3 OFC slots would move to another person id
    (compatible name + shared org + coauthor, made possible by the newly mapped YOFC / SKL rows): `person_jie_luo_2` ->
    `person_jie_luo` (M1C.4 #10), `person_peng_li_2` -> `person_peng_li` (Th1A.6 #7), `person_lei_zhang_3` ->
    `person_lei_zhang_2` (Th1A.6 #9); redirected ids 12 -> 15. Per the round brief (person ids must not change from
    this round alone) the real people build and `derive_transitions.py` were not run; data/people is stale against
    the registry until the coordinator rules (validate_db errors below).
  - Requests recorded: `data/_staging/people/ofc_headers/org_requests_resolution.csv` (round 5 rows kept; 127 round 6
    rows appended, columns unit / locality / country added) and `data/_staging/supply/org_requests_resolution.csv`
    (29 rows). The supply request file itself is left to `build_supply_staging.py` (it sets status from the matcher).
  - Tests: `tests/test_ofc_headers.py` `test_campus_row_is_not_the_parent` compared ids by substring (the new
    `org_chinese_university_of_hong_kong_shenzhen` contains the parent id): now splits the id list;
    `test_org_requests_carry_place` relied on the SKL string staying unmapped: now runs on a matcher copy without the
    SKL name, so the place columns and the D305 note path stay under test.
  - Decisions (range D330-D339; D339 kept for the audit):

    | # | Decision |
    |---|---|
    | D330 | OFC header strings that are the same entity at the source date (spelling, abbreviation, language, legal form, article, place word in parentheses) -> unscoped aliases of the existing org: Fraunhofer HHI (5 forms, German forms native_name), EPFL ("Swiss Federal Institute of Technology Lausanne (EPFL)" and the misprint "(EFPL)"), UCL (full form), DTU ("Denmarks Tekniske Universitet", native_name), Padova, Campinas, Peloponnese, UIUC, Palacky, Chalmers, BUPT, TU Chemnitz, TU Berlin, CNIT, Amirkabir (the "(Tehran Polytechnic)" place word blocks the bare variant, D301), Huawei (misspelled / singular forms), CAS IME (misspelled "Institue"), NEC Labs of America, Peng Cheng Lab, ZTE "cooperation", YOFC legal-name forms (Fiber / Fibre, JSLC), imec vzw., CableLabs / FUJIFILM / LuxQuanta / China Mobile legal names, China Unicom (ROR alias), QoreTek, E-lighthouse, Enablence, YanDong, Tratos Cavi; "Universidad de la Republica" ofc2026-scoped (bare name not specific to Uruguay) |
    | D331 | Bare acronyms and brand short forms -> ofc2026-scoped aliases with header + metadata evidence (D276 pattern): AUTH, UCL, KIST (ROR acronym shared by 4 records), INRS, IRISA, FORTH, FOTON-UMR6082 / Institut FOTON, Adtran (Planegg = Adtran Networks SE; the bare brand also names ADTRAN Holdings), EXFO (the batch_2 org was created from this header); "ASN/Nokia" joint (Alcatel Submarine Networks + Nokia) |
    | D332 | Strings naming a printed host plus a site / subsidiary / unit (contract rule 1, batch_1-4 precedent): subsidiary_printed (1Finity Americas, Ciena US, CISCO Systems S.R.L., Cisco Photonics Italy S.r.l., Nokia Bell NV, Nokia Canada Inc, Semtech Canada, Finisar Australia (string names Finisar, not II-VI / Coherent), Huawei Duesseldorf umlaut form, Heraeus Quarzglas Bitterfeld, China Mobile Guangdong, Fujitsu R&D Center (as batch_2), IMEC The Netherlands / IMEC-NL (as "Stichting imec Nederland"), Corning Optical Communications -> org_corning (not the PK German GmbH org)); unit_printed (Cisco Photonics, Cisco Quantum Lab, NI Nokia, Innolight Technology Research Institute, Jinhua Institute of Zhejiang University, Shenzhen HUST Research Institute, the BIT satellite-navigation key lab and the Shenzhen University SKL (host in parentheses), Wuhan National Laboratory for Optoelectronics -> HUST as batch_4); joint (imec-Ghent University, Cisco - Acacia Communications) |
    | D333 | New orgs from exact ROR records (display name; D200 / D271 for company disambiguators; type from ROR, facility -> research_institute). Parent = the record's only ROR parent when it is in the registry (BT Research -> BT Group, IO-CSIC -> CSIC); with several ROR parents, the one printed in the block when exactly one is (Lab-STICC -> CNRS); otherwise empty (OCA, ARTEMIS, Telecom SudParis, CSULA, IST, MPL). Homonym names choose the record by the header country (Al-Azhar University EG of 3; University of Georgia US of 2, from the header place Athens, GA, overriding the batch_4 skip). Curated routes: "Buenos Aires University (UBA)" = word-order variant of the ROR label plus the ROR acronym; "Lab-STICC" and "Artemis" = ROR acronyms printed with the record's parents (ofc2026-scoped aliases) |
    | D334 | Campus rows (D301) get the campus institution's own ROR org, never the parent: Chinese University of Hong Kong, Shenzhen (02d5ks197; two ROR parents, none printed: no parent), Indian Institute of Technology Delhi (049tgcd06), University of Maryland, College Park (047s2c258) |
    | D335 | Printed orgs without a ROR record, named as printed (acronym dropped for NCAIP), country from the header address, type from the name's words (Laboratory / Institute / Research Center -> research_institute; Inc. -> company; else unknown), parent only when the host is printed with the org (none here): Jinyinhu Laboratory, National Engineering Research Center for Next Generation Internet Access System, Chongqing Key Laboratory of Novel Civilian Radar, Hubei Key Laboratory of Advanced Control and Intelligent Automation for Complex Systems, Engineering Research Center of Intelligent Technology for Geo-Exploration (Ministry of Education), Eindhoven Hendrik Casimir Institute (printed "and" the university: relation not stated), Photonext Center, Cluster of Excellence PhoenixD, National Centre for Advanced Integrated Photonics, QXP Technology Inc., Fouad Alghanim & Sons Group of Companies |
    | D336 | (parent withdrawn by D339a) D305 applied: `org_state_key_laboratory_of_optical_fiber_and_cable_manufacture_technology` (printed, research_institute, CN, parent org_yofc). The bare string maps to the lab itself (61 Beijing header rows, 6 metadata rows), so D278's host objection no longer decides the mapping; YOFC-block rows keep mapping to YOFC (org first, unit second). Caveat kept in the notes: the Beijing prints name China Telecom Research Institute beside the lab (Th4C.1 prints CTRI first), so the YOFC parent rests on D305 and the YOFC-block prints |
    | D337 | Rejected: "UNIDEF (CITEDEF-CONICET)" (M1K.5; acronym-only unit, expansion not printed in any cached text, two hosts printed as a pair, relation to each not stated; TFS rule of D278) |
    | D338 | Supply vendor requests: D273 printed orgs (Eravant, Evatec, Graphene Platform JP, Moorfield Nanotechnology, Vanguard Automation GmbH DE, Gel-Pak, KOHERAS and Keithley and Voltcraft brand-level (owner not printed; Keithley is not an alias of Tektronix), Metricon, OFS Fitel, LLC (not mapped to Lightera), Pasternack, AKROMETRIX, AtaiTec, Pactech, Tosetz Inc.); common-word or acronym names no_name_match + corpus-scoped alias (Vigo, FLIR, Parker Corporation, Rogers Corp. (name from the paper's reference [28]), Waltz Corporation). D271 ROR: Micro Resist Technology, Mitaka Kohki, Okuno Chemical Industries Co., Ltd., SUSS MicroTec (root; the PK SUSS MicroTec Lithography org stays separate), Tokyo Electron. D271 not applied to Vigo: the single same-key record "Vigo (Poland)" 00qw0ej89 has an orthopaedics website. "Toptica" -> short_name alias of org_toptica_photonics (the only Toptica org; ROR 00t9ms296 has the same key). D272 extended: A -> materials_supplier; review lines filed under G whose item is a chemical (Okuno plating additives, Parker cleaning solution) -> materials_supplier. "micro resist technology" (eo:powell2024) resolves by key, but powell2024 does not print the vendor (supply stream to decide); TFS stays rejected |

  - Verification (00:50): ruff check clean; ruff format: 1 file would be reformatted (`tests/test_lit_seeds.py`,
    not touched by this round); mypy clean (81 files); pytest 301 passed, 4 failed: `test_people.py`
    (`test_build_is_in_sync_with_inputs`, `test_copy_is_clean`, `test_copy_with_queue_is_clean`) and
    `test_validate.py::test_real_registry_has_no_errors`, all from the stale data/people tables. validate_db 987
    errors, 15 warnings; every error is an `affiliation_observations` row (org_id '' vs the newly mapped header row or
    crosswalk string, D214); 0 errors in any other table. They clear when `build_people.py` runs.
  - Open (this round): coordinator ruling on the 3 person-id moves above, then `build_people.py` (dry-run, real,
    second run identical) and `derive_transitions.py`; registry follow-ups not done here: org_toptica_photonics
    country / name vs the ROR root record (DE), org_suss_microtec_lithography parent; candidate org relations to
    research with primary sources before any event row (none is stated by a local source): OFS Fitel and Lightera,
    Keithley and Tektronix, FLIR and Teledyne FLIR, KOHERAS and its owner.

- 2026-10-23 01:28-01:40: round-6 audit fixes D339 ([audit](audits/2026-10-23-org-round6-audit.md); coordinator
  rulings: W3 scrub incl. the older batches, W2 no SKL parent, W1, I1, I2, I3 separate orgs, I5, I6). Backup zip
  `backup_round6b_*` (private scratch) of registry, crosswalk, config, org_curation, people staging, data/people,
  data/_local/people, app/static/data, this DevLog and the OFC header test. data/supply and data/_staging/supply not
  touched (supply merge running).
  - W3 scrub (address text from restricted headers / papers -> org / unit / city / country): batch_8 regenerated
    (53 rows had address text); batches 1-7: 42 rows (batch_1 4, batch_2 30, batch_3 4, batch_4 1, batch_5 1 (eo),
    batch_7 2 (lit)); registry notes: round-6 rows re-merged from the scrubbed batch_8 (20 org notes, 39 alias notes
    had the text), pre-round-6 rows through `config/registry_corrections.yaml` (25 org notes, 20 alias notes, why
    D339); the 2 round-6 override entries; 1 OFC resolution row (UGA); D333 text above; 5 strings in two audit records
    (round-5 audit: ams AG / ams OSRAM addresses, a Beijing postal code; OFC batch audit: 3 postal codes). Contract
    `data/_staging/org_curation/INSTRUCTIONS.md` (inputs paragraph and rule 7) now states the D172 / D244 rule.
  - Registry rebuilt for round 6 from the pre-round-6 rows (`backup_round6_*`) with the corrected batch_8: merge
    dry-run, real, second run 0 / 0, no unify event, no unresolved parent; corrections 45 changes, second run 0
    (after the 2 late alias notes: 2, then 0). Registry 1001 -> 1069 orgs, 416 -> 510 aliases.
  - Crosswalk: identical to the 00:42 file (acceptance PASS, OFC 6051 / 6055). OFC headers (`check all` 0 errors, 48
    warnings; `aggregate`): against the 01:10 state 13 rows re-pointed by I3 (Cisco Quantum Lab 8: org_cisco ->
    org_cisco_quantum_lab; Innolight Technology Research Institute 5: org_innolight ->
    org_innolight_technology_research_institute), no other row changed; against the pre-round state still 587
    unmapped -> mapped, 0 re-pointed. Slot outcomes: conflict 15 -> 20: the 5 YOFC-side slots whose metadata prints
    the bare SKL string (M1C.4 Jie Luo, Lei Shen; Th1A.6 Peng Li, Lu Dai, Lei Zhang) no longer share a root with their
    YOFC header row (W2).
  - People (D219d unchanged): dry run 0 person-id changes (0 observations moved, 0 committed persons joined, 0
    split; merges 120 / 1762 / 1652 as committed); real run, second run byte-identical (4 tables + review queue),
    `derive_transitions.py` (transitions 47, name-only candidates 106 -> 107, local only). Diff vs 01:10:
    observations 11599 -> 11604 (+5 metadata rows of the 5 new conflict slots, SKL org, review), org_id re-pointed on
    13 header observations (I3), 1 observation and 1 person public -> review; people / aliases / xref unchanged.
    `build_views.py` and `pnpm build` (app) ran.
  - Remaining address-like text after the scrub (grep of the scrubbed strings and of postal / street patterns over
    data/registry, config, data/_staging/org_curation, DevLog, app/static/data): 2 OFC metadata affiliation strings
    that are exact match keys (aliases, crosswalk `printed`, batch inputs, the 2026-10-20 unmapped list,
    registry.json): "Baidu, Systems Department, Kuike Technology Building, No.9 Shangdi Information Road, Haidian
    District" and "Institute of Computing Technology, ..., Beijing 100190, China University of Chinese Academy of
    Sciences". They are the conference metadata strings, not header text; removing them unmaps 9 metadata rows
    (coordinator decision). Other pattern hits are counts, DOIs, hashes and values. Outside the grep scope: two
    `headers.yaml` notes of the OFC header stream ("Haisnes Cedex", "Adastral Park") and a test mutation fixture
    (`tests/test_ofc_headers.py` "Kapeldreef 75").
  - Decisions:

    | # | Decision |
    |---|---|
    | D339 | (audit W3) Evidence, notes, override entries, resolution files and DevLog text quoting an OFC 2026 header (restricted corpus, D172 / D244) or a paper affiliation carry only organization, unit, city and country as printed; never a street, building, site / park name, PO box, room or postal code. Applied to batches 1-8, the registry notes (re-merge for round 6, `registry_corrections.yaml` for older rows), the override entries, the resolution file, this DevLog and two audit records; contract rule 7 updated |
    | D339a | (audit W2, I6; overturns the D305 parent) `org_state_key_laboratory_of_optical_fiber_and_cable_manufacture_technology` has no parent. Evidence: the 61 header rows that map to it are 12 Beijing papers (M1F.5, M1J.4, M2C.3, Th1I.5, Th4C.1, Th4C.4, Tu2C.5, Tu2F.3, Tu3E.5, W1E.2, W1G.2, W4H.6); every block also prints China Telecom Research Institute (first in 9 of 12, after the lab in M1F.5, Th1I.5, Tu2C.5); none prints YOFC; the lab is printed with YOFC only in Wuhan YOFC blocks, which map to org_yofc. Two printed hosts, relation to each not stated by a local source (D335 / D337 rule); the host needs a primary source. The bare string still maps to the lab (D336) |
    | D339b | (audit W1) `org_rogers` = ROR 05m9vrv91 "Rogers" (US, company; D271 brand-level record, parent of 02s5qve69 Rogers (Germany)), set in batch_8 (no correction entry); no_name_match and the pk-scoped aliases "Rogers" and "Rogers Corp." (printed in the paper's reference) kept. The D338 statement "no exact ROR record" was wrong (the exact-key search missed the disambiguated display name) |
    | D339c | (audit I1, I2) "Toptica" -> org_toptica_photonics scoped to lit (the bare brand names the German maker; the org row is the US Inc.; no brand-level org yet); "Corning Optical Communications" -> org_corning scoped to ofc2026 |
    | D339d | (audit I3, contract rule 2) Company research labs printed as their own block are orgs: `org_cisco_quantum_lab` (printed, industrial_lab as Hewlett Packard Labs, US, parent org_cisco) and `org_innolight_technology_research_institute` (printed, research_institute, CN, parent org_innolight). Parents from the company name printed in the lab name (precedent org_lightera_laboratories); neither header prints the company as the lab's host in the same block |
    | D339e | (audit I5) The UGA and SKL orgs carry round-6 provenance ("curated (round 6 override, D333 / D336)", SKL name_source "ofc2026 printed (round 6 override, D336)") through `config/org_curation_overrides.yaml` `orgs:` |

  - Supply follow-up not done here (data/_staging/supply locked): `data/_staging/supply/org_requests_resolution.csv`
    row "Rogers" (resolution new_org_printed -> new_org_ror, notes D339b) and row "Toptica" (scope lit, D339c);
    the round-6 decision rows themselves are correct in batch_8.

## Incidents

- 2026-10-20 14:05: `config/registry_corrections.yaml` had lost its `orgs` / `aliases` sections in the 12:48 edit that split out `orgs_retype_facility` (registry rows were not affected: the corrections had been applied at 12:48:03). The re-run of `merge_org_curation.py` then re-added two alias rows the corrections had re-pointed (China Unicom research institute, Toshiba Europe Ltd). Fix: the sections were restored from `logs/apply_registry_corrections_20261020T124803.jsonl` (the Broadcom Corporation alias stays omitted per the audit 2.2 note), the two re-added rows removed, and both strings pinned in `config/org_curation_overrides.yaml` so the merge cannot re-add them; second runs of both scripts give 0 changes. Lesson: an alias correction that re-points `org_id` also needs a curation override.

- Privacy: org-event subagents A and B each sent one curl request to sec.gov with a User-Agent containing the user's e-mail address (SEC asks for a contact). Both stopped curl after a later 403; no other personal data was sent. Rule added to project memory: fetch subagents must never put personal identifiers in requests and use WebFetch, stopping on 403.
- Rate limit: group C did not enforce the 5 s spacing (about 33 sequential requests over ~7 min); group A about 48, group B about 30 requests. Anti-bot / block signals: investors.adeia.com 403, nokia.com 403, sec.gov 403 to plain curl; each host was then avoided.

## Open items (not blocking P0)

- Skipped OFC strings (12 rows): Hangzhou Institute of Technology, PCL, the bare YOFC/CTRI State Key Laboratory string, Telnet, University of Georgia.
- PK "Xperi" (printed "Xperi Corporation", 2022) has no sourced link to Xperi Holding Corporation / Adeia, so the 9 PK authors who print Xperi (2022) then Adeia (2023) are not yet covered by an org event (people report C.4); needs the Xperi Corporation subsidiary history from a filing.
- Not verified by the event research: Ando/Yokogawa month and mechanism; Raith - EBPG link; CYCLOTENE transfer dates (P2 product data); Viavi, Pavonia and Alcatel rename dates.
- Parent links not set: Harbin Institute of Technology (Shenzhen) (EO row), Bell Labs era orgs (LIN).
- 14 LIN orgs have status `acquired` but LIN records the acquisition only as an edge, not an event (validator warning); import LIN acquisition edges as events in P3.
- Event research caveats (group A report): several locators were quoted through a web summarizer (the P0 data audit re-checked 8 events live, all matched); some 8-K `published_on` values are report/signature dates, not EDGAR filing dates.
- Possible duplicates left for their source atlases: EO ZJU micro/nano fabrication platform (two rows, EO note says they may be the same); PK "University of Applied Science Berlin" (HTW or BHT not stated).
- To report back to eo-modulator-atlas (read-only here): its 1Finity row carries the ROR id / QID / website / founding year of Fujitsu Telecom Networks Limited (corrected here, `config/registry_corrections.yaml`).
- 35 orgs typed `unknown` (no record states the kind).
- (2026-10-22) PK orgs without a ROR id because no record has the exact name: Applied Materials Singapore Technology
  (ROR "Applied Materials (Singapore)" 01c4r0z03 differs in name), IMT (Rome; ROR "IMT Srl (Italy)" not stated by PK),
  Changsha Anmuquan Intelligent Technology, Hytek, LIG Nex1, LPKF Laser & Electronics, OUME Electronics, Panasonic
  Industry, Panasonic System Networks R&D Lab., Somacis. `org_applied_materials` itself has no ROR id (ROR US record
  04h1q4c89 exists; not set this round).
- (2026-10-22) `org_shin_etsu` is brand-level (D203); if a source names the Shin-Etsu company, add it as its own org
  with parent or event, do not rename.

## Audit corrections (2026-10-20)

Two fresh-context audits ran after the build: [data](audits/2026-10-20-p0-data-audit.md) (78 findings: 49 ok, 19 imprecise, 3 wrong, 7 unverifiable; OFC mapping sample 84/85 correct, EO/PK 40/40, no wrong merges, 8/8 live event checks match) and [code / privacy / conventions](audits/2026-10-20-p0-code-privacy-audit.md) (2 validator crash paths, 23 bad-data classes accepted, 3 regenerating writers, 1 public-commit blocker). Applied:

- Privacy (blocker): the people research report named derived career transitions, name-only identity matches, a collision-risk name list and one LinkedIn-sourced lead about living people. Tracked copy redacted to counts (C.3, C.4, B.1, D.2, D.4); the DevLog-044 audit's mention of the LinkedIn lead generalized. Unredacted copies kept in git-ignored `DevLog/research/local/`. Also: Nature `sharing_token` query strings stripped from `blog_harvest/candidates.csv`, the personal about-page context replaced, "his own publication list" reworded, archive path and timing generalized (originals of edited research files kept in `DevLog/research/local/`).
- Validator rewritten (`src/photonics_atlas/validate.py`): no crash on bad enums or malformed dates (rule checks skip rows with cell errors); built tables must exist; required lists need an item; ints by regex; plausible years (0500..next year); country codes vs the ROR code list; event roles per type (required and allowed); event grade not better than its best cited source; event sources must be web/lin/ds documents; imported-lineage anchor equals the event id; locator form 10..300 chars; rights rule for ofc2026/pk; crosswalk acceptance and staleness of name/alias rows; per-item alias scopes; name_basis vs origin; warnings for status without event, redundant aliases, duplicate-source citations, long announce-after-effective gaps. One mutation test per rule (`tests/test_validate.py`).
- Scripts: `add_ror_orgs.py` writes `unmapped_<run>.csv` (the first run's file renamed `unmapped_20261020T121712.csv`); `build_sources.py` keeps rows of corpora it does not build (web, ds); `merge_org_events.py` keeps hand-added events, keeps only cited web sources (8 uncited dropped; sources 1834 -> 1826), checks that sources.csv exists; `build_org_crosswalk.py` exits 1 on acceptance failure; ROR version pinned in `config/inputs.yaml`; YOFC fold reproducible (`ror_ids` override in `config/org_seed_overrides.yaml`); ROR `facility` maps to research_institute.
- New `scripts/apply_registry_corrections.py` + `config/registry_corrections.yaml`: every hand change to registry rows, with its reason, replayable and idempotent (second run: 0 changes). Applied: org_1finity cleared of Fujitsu Telecom Networks' ROR/QID/website, founded_on 2025-07-01 (audit 6.2, wrong); China Unicom research-institute alias re-pointed (2.7, wrong); D29 countries (Ciena US, Nokia FI); statuses from events (Tokyo Tech merged, Showa Denko Materials renamed, Infinera acquired, Telefonica R&D historical); D20 parents (Coherent, Inc. -> Coherent Corp.; Newport -> MKS; Lucent -> Alcatel-Lucent; Avago and Broadcom Corporation -> Broadcom Limited -> Broadcom Inc.); ROR parents (China Mobile Research Institute, FOTON, USTC); scope ofc2026 on header-specific generic aliases (Optoelectronics Research Centre, School of Information Science and Electronic Engineering, IDLab, CICT); Toshiba Europe Ltd -> the Cambridge lab (consistent with the same header form); stale alias notes; 21 ROR-facility orgs retyped research_institute.
- Events (`config/event_participant_map.yaml`): Avago/Broadcom roles per the locator (Broadcom Limited acquirer; Avago, Broadcom Corporation targets); Oclaro dropped as seller in the Newport/New Focus exchange; announced_on emptied for Nokia/Alcatel-Lucent and Xperi Holding -> Adeia (not supported by the quoted locators).
- E-mail stripping extended to grouped (`{a,b}@domain`) and obfuscated (`[at]`, `(at)`) forms, `session_title` stripped too; tests assert no `@` (no longer tautological).
- Docs: README pipeline table with each script's write behaviour and order; decision text fixed (D15 foundry_service, D16 header-address countries, D25 match bases, D29 added); open items revised (Campinas item removed: the row already had its ROR id; group A caveats added).
- Not applied, with reason: blog sources keep access `public_web` (the files are publicly reachable at the blog URL; rights stay `redistribution: unknown`); Adtran Networks status stays unknown (no source on its current status); the possible EO/PK duplicates are left to their atlases; Southeast University CN stays an inference until a paper header is available.
- Re-verification after corrections: validate 0 errors (15 warnings: 14 LIN acquired-without-event, 1 documented EO year exception); pytest 30 passed; ruff, ruff format, mypy strict clean; acceptance PASS (EO/PK/LIN 100%, OFC 6043/6056 = 99.79%); idempotency (corrections second run 0 changes; event merge preserves 0 hand-added events).
