---
title: P2 Supply-chain atlas - category tree, schema, rules, first local data tranche
date: 2026-10-20
status: foundation tranche done 2026-10-20 (local data only); two fresh-context audits done 2026-10-20, corrections applied (see Audit corrections, rounds 1 and 2)
scope: DevLog-000 phase P2 (foundation; datasheet harvest and the vendor/model scanner are later tranches)
authors: Claude (at Wentao Jiang's request)
---

# DevLog-003: P2 Supply-chain atlas (foundation)

Plan source: [DevLog-000](DevLog-000-plan.md) P2 (D6, D7, U4), research input
[supply-chain taxonomy report](research/2026-10-20-supply-chain-taxonomy.md) (section 1 tree, section 2 specs,
section 3 seeds, section 4 schema sketch), registry conventions [DevLog-001](DevLog-001-p0-foundation.md) (D13-D29).

This tranche: local structured inputs only, no network of any kind. The datasheet harvest (U4) and the productized
vendor/model scanner over paper texts are later, separately approved steps.

## Inputs (read-only)

| Alias | Location (relative to the parent of this repo) | Used for |
|---|---|---|
| EO | `eo-modulator-atlas/data/papers.csv` (`foundry_or_fab`, `wafer_supplier`, `process_name`, `verified_on`), `data/devices.csv` (`waveguide_platform`) | fabrication / facility / wafer-supplier usage, foundry process observations |
| PK | `advanced-packaging-atlas/data/metrics.csv` (rows with non-empty `test_standard`) | standards, reliability tests |
| Registry | `data/registry/{organizations,org_aliases,sources}.csv` (this repo, not edited) | org ids via `orgmatch` (corpus `eo` / `pk`), source ids |

## Data decisions (D51-D60)

| # | Decision | Rationale |
|---|---|---|
| D51 | Tables in `data/supply/`: `products`, `product_usage`, `product_specs` (long), `foundry_processes`, `standards`, `reliability_tests`; schema `data/schema/supply.schema.yaml` (loaded by the shared validator after the registry and component schemas); new enum and pattern names carry a `supply_` prefix; the shared `qualifier` enum (components schema) is reused. Category tree in `data/schema/supply_categories.yaml`. Table rules in `src/photonics_atlas/rules_supply.py` (validator tranche hook). A table is `built: true` once its CSV exists (header-only CSVs count: `products`, `product_specs` are empty this tranche) | D13 single schema; no collisions with registry/components/people schema files |
| D52 | Category ids from report section 1: top level `A`..`K`, children `A1`..`H17`, grandchildren `A2.1`; each node has label and parent; the parent of a child is its id prefix. A fact row may carry a top-level id (`B`) only when the source does not state the subcategory (validator warning, note required) | report section 1; no forced subcategory (rule (a)) |
| D53 | `product_usage` = one row per (source, org, role, product): the source states that the org (and, when named, the product) was used in that role for the reported work. Facts and locators only: no verbatim text column at all (refines D7: the 200-char quote is dropped because most supply sources are non-OA; `stated_spec` holds a short factual paraphrase, <= 120 chars, no quotation marks for restricted sources). `usage_id = use_<source slug>_<org slug>_<role>[_<product slug>]`, deterministic, so re-runs skip existing rows | traceability rule; non-OA rights (D4, D23) |
| D54 | Usage roles (`supply_usage_role`): fabrication (foundry / company / lab stated to have fabricated the device), facility_use (shared cleanroom where work was performed, registry org_type `facility`), mpw_access (MPW broker / aggregator), post_processing (BEOL material deposition or film growth service on someone else's wafer), wafer_supply, material_supply, fab_tool, test_instrument, packaging_material, assembly_tool, fiber_component, laser_source, software, standard_reference. Each role allows only certain top-level categories (fabrication / mpw_access / post_processing / facility_use -> B; wafer_supply -> A, B; material_supply -> A, E; fab_tool -> G; test_instrument -> H; packaging_material -> E; assembly_tool -> F; fiber_component -> D; laser_source -> C, H; software -> J; standard_reference -> I, K); facility_use -> B7 and an org typed `facility` | consistent lens category -> vendor; one role per fact |
| D55 | `basis` (`supply_basis`): stated (the source states the fact), inferred_from_model (vendor inferred from a stated model number), datasheet_spec / datasheet_typical (product_specs from `ds:` sources only). `extraction` (`supply_extraction`): atlas_import (copied from a sibling atlas field), manual, auto_regex, auto_sentence. Locators: page form `p.N` / `p.~N` / `pNA` plus figure/table/section text, or an atlas anchor `eo-atlas:<file>.csv#<id>/<column>` / `pk-atlas:<file>.csv#<id>` for paper-level atlas fields that carry no page. Consistency: atlas_import needs basis stated and the anchor of the source's own corpus; manual / auto_* need a page locator; inferred_from_model and auto_regex need a product_id | EO paper-level fields have no page locator; no invented pages |
| D56 | EO `foundry_or_fab` import: each name is matched with `orgmatch` (corpus `eo`); registry org_type `facility` -> facility_use / B7; CMC Microsystems -> mpw_access / B6; otherwise fabrication (post_processing for NLM Photonics, whose EO process text states SOH post-processing). The B subcategory of each fabrication row is set by hand per (paper, org) in `data/supply/curation.yaml` only from what the paper's own EO `process_name` states (SOI / silicon photonics -> B1, SiN -> B2, TFLN -> B3, InP -> B4, BTO / OEO / plasmonic-organic hybrid -> B5); nothing stated -> top-level `B` with a note | rule (a); org kind comes from the registry record, platform from the paper |
| D57 | EO `wafer_supplier` import: the cell is split on `;` outside parentheses; a trailing parenthetical is the stated qualifier (`stated_spec`); name candidates are the text before the parenthesis and its first comma segment; phrases "not named" / "not stated" / "fabricated by the authors" yield no row (logged). Category: per-(paper, org) override in curation > qualifier keywords (LNOI/TFLN A2.1, LTOI/TFLT/lithium tantalate A2.2, LN-on-sapphire A2.3, BTO A2.4, GaAs/InP A3, chromophore/EO material/FN-LC A4, graphene/hBN A5, GdScO3 A6, SiN wafers B2, SOI A1) > org default in curation > the paper's EO device `waveguide_platform` (lnoi_* A2.1, ltoi_* A2.2, lnos_* A2.3, bto_* A2.4, algaas/gaas A3; noted as derived) > top-level `A`. Role from category (A1-A3, A6, A7, B2 wafer_supply; A4, A5 material_supply; B5 post_processing). Unmapped names go to `data/_staging/supply/org_requests.csv` (corpus, printed string, kind, source ids), never into the registry | free-text cells; no guessed suppliers; registry is curated elsewhere |
| D58 | `foundry_processes` = per-source process observations (`proc_<org slug>_<source slug>`), not canonical processes: identity between observations is not asserted unless a source states it (views group by org and `pdk_name`). Fields only when stated in the EO `process_name` text: platform (`supply_platform`), wafer_mm (8-inch -> 200, 12-inch -> 300 nominal, noted), pdk_name (a named PDK / platform only), access_route (`supply_access_route`), broker_org_id, pdk_open. A process is attributed to an org when the text names it or the org is the paper's only non-facility fabrication org | no merge without evidence |
| D59 | `standards`: one row per standard document designation without revision letter (`std_jesd22_a104`); the cited revision / method / condition stays in the citing row (`reliability_tests.standard_printed`). `body_org_id` only when the body is a registry org (none are this tranche: requests staged); title and scope empty unless a local source states them; access `unknown` until checked. Designations are parsed from the PK `test_standard` string by an explicit pattern list; typos and ambiguous strings ("MIL Standard 833", "ESD22-B111", "IPD/JEDEC-9704A", "MIL-STD-883-2") are not corrected, they stay unparsed with the printed string kept | no invented titles; printed strings preserved |
| D60 | `reliability_tests`: one row per PK `metrics.csv` row with a non-empty `test_standard` (`rt_pk_<metric id slug>`), source `pk:<paper_id>` (via PK `test_vehicles.csv`), PK locator verbatim, `atlas_ref = pk-atlas:metrics.csv#<metric_id>`, PK basis / value / value_text / unit / statistic / n_samples / condition / pass_criterion / result copied. `test_type` by the keyword table `TEST_TYPES` in the script on the PK parameter, then on the printed standard string when the parameter matches nothing; preconditioning is dropped when another stress also matches, uhast wins over hast, two or more remaining types -> `other` (sequence rows such as "IL shift after TC, DH, HTS, LTS" claim no single type). Designations are never mapped to test types (that would need the standard's title, which no local source states). Condition fields are parsed only for the types where they are the stress (t_min_c / t_max_c: temperature_cycling, thermal_shock; temp_c + rh_pct: humidity tests and preconditioning; single temp_c: storage and humidity tests) and only when the pattern occurs exactly once in the condition text; otherwise empty (a preconditioning soak inside an HTS or TC row is not taken as that row's stress) | mirrors PK; parse only unambiguous text |

### Amendments 2026-10-20 (fresh-context audit; original rows above kept as written)

| # | Amendment | Rationale |
|---|---|---|
| D53 (am.) | `stated_spec` holds only the stated fact; locator words at the end of an EO cell qualifier ("acknowledgements", "as written in Methods", "per acknowledgements") go to notes as `EO cell locator words: ...`; legal-name or printed-form parentheticals (NanoLN "Jinan Jingzheng Electronics Co., Ltd.", "written NONOLN in the paper") are curated `wafer_parts` notes, never stated_spec. Restricted-source rows reject curly single quotes too (`QUOTES` = straight and curly double and single) | audit #7, #35, #30 |
| D54 (am.) | Validator: an org typed `facility` in the registry may carry B-category rows only as facility_use / B7 (A-category wafer or material supply from a facility, e.g. an epitaxy facility, stays allowed); wafer_supply allows A* or B2 only; atlas_import anchors must name the source's own record (`#<native_id>`) and an allowed column (`product_usage`: foundry_or_fab, wafer_supplier; `foundry_processes`: process_name) | audit #25, #26, #28, #29 |
| D56 (am.) | `fab_categories` entries may carry a `note`; valdez2023 / valdez2023a Sandia stay top-level `B` with a note: the papers credit Sandia staff with "fabrication assistance" (acknowledgements) and do not name the waveguide foundry, so the D58 only-fab-org attribution used for e.g. chaudhury2024 (paper: "fabricated by Applied Nanotools") is not applied | audit #5; attribution only where the paper states fabrication |
| D57 (am.) | (1) Qualifier keywords growth / integration / deposition -> B5 post_processing (checked after the SOI-substrate rule, so "SOI substrates for BTO growth" stays A1; never applied to org names, so "Novel Si Integration Technology" is not B5). (2) Same fact in two EO cells: when an org of the paper's foundry_or_fab (fabrication / post_processing / mpw_access row) also appears in its wafer_supplier with a B category, one row is kept (the foundry_or_fab one, its locator), stated_spec taken from the wafer_supplier qualifier and the merge noted. kohli2025: LIGENTEC = one fabrication / B2 row ("SiN wafers"; paper: SiN wafers fabricated by Ligentec, SiN waveguides produced in a photonic foundry), Lumiphase = one post_processing / B5 row ("BTO growth and integration"; paper: growth and integration of the BTO completed by Lumiphase). (3) Org-default category notes read `category: curation org default` (the reason, which cites other papers, stays in curation.yaml only). (4) Printed names curated in `alias_requests` (SIMIT-CAS -> org_shanghai_institute_of_microsystem_and_information_technology) are staged as kind `alias` with `alias_of_org_id`, never as new orgs; `request_notes` mark printed variants; staging columns `status` (open / resolved) and `resolved_org_id` are set from the registry matcher on every run | audit #2, #3, #4, #6, #22, #33, #34 |
| D58 (am.) | Process names keep the printed wording of the EO record (yin2026: "multi-wafer project (MPW)", not "multi-project wafer") | audit #8 |
| D59 (am.) | Designation parsing normalizes separators and drops the revision letter (`JESD22A-104F`, `JESD22-A104F` -> `JESD22-A104`); that is the only normalization: typos and ambiguous strings stay unparsed. Validator: each `standard_ids` designation must occur in `standard_printed` (case- and separator-insensitive), and designations ending in a revision letter after the number are rejected. `body_org_id` is filled from the registry when the designation prefix names a body (22 of 24 after org curation round 2). J-STD-020 and MIL-STD-883 name no single body by designation; J-STD-020's note records the printed prefix `IPC/JEDEC` (pk:eptc67330.2025.11392108) and it keeps no body_org_id (joint document) | audit #16, #27, #29 |
| D60 (am.) | (1) `test_type` = the stress; new column `measurand` (`supply_test_measurand`: optical_loss, electrical_resistance, die_shear, adhesion, thermal_resistance, warpage, leak) from the PK parameter. IL after HTS = high_temp_storage / optical_loss with the HTS temperature parsed. Rows with no stress keep the measurement type as test_type (IL per facet = optical_loss / optical_loss). Leak is a measurement, not a stress. (2) Stress search order: parameter, condition, printed standard (condition before standard, audit #1); in each text the preconditioning clause is split off first: from an MSL / precon keyword to the end of its `;` segment, over the following ` + ` / `then` steps that name no stress other than reflow (bake, soak, THS, reflow are precon steps; a following TC / uHAST / HTS step is the main stress again). "MSL3 preconditioning + reflow" = msl_preconditioning (reflow does not override precon). Reflow is dropped when another stress is named (a reflow before a stress is assembly or precon). In condition text, cycling / shock keywords need a temperature range or the word cycle (TCB = thermocompression bonding, Tc = case temperature). (3) Parsed fields per type: t_min_c / t_max_c only temperature_cycling, thermal_shock; rh_pct only humidity types and msl_preconditioning; temp_c for storage and humidity types, and for msl_preconditioning only as the temperature of a T / RH soak pair (never a reflow peak; `SINGLE_T_TYPES` no longer includes msl). Main-stress fields are parsed from the condition without its precon clause; msl rows from the precon clause (or the whole condition when it has no precon keyword). Enforced by the validator (shared sets in rules_supply). (4) New columns `variant`, `scope` (PK, as recorded), `qualifier` (shared enum, from the PK `qualifiers` token `value:<q>`). Values keep the sign as printed: negative IL rows (ectc51687.2025.00012) keep `-2.46` etc., PK scope says "sign as printed (negative)", and the row note says component tables store loss positive (D33) and the value is not flipped. (5) Validator: `test_id == test_id('pk', <metric id of atlas_ref>)`; the atlas_ref metric must be of the row's `tv_ref` and the tv of the row's source (`<native_id>-<tv>` / `<tv>-m<N>`). (6) Corrections land through `--replace-ids` (explicit list or `@file`): listed ids are replaced by the rebuilt row, or removed when the rebuild no longer produces them; everything else stays append-only (differences logged as `differs`, ids no longer produced as `stale`) | audit #1, #10, #11, #14, #15, #25, #27, #32 |

Round 2 (2026-10-20, second fresh-context audit):

| # | Amendment | Rationale |
|---|---|---|
| D54 (am. 2) | Validator: imported usage roles are bound to their EO column (fabrication / facility_use / mpw_access <- foundry_or_fab; wafer_supply / material_supply <- wafer_supplier; post_processing either); subcategories per role: wafer_supply A (top level, D52), A1-A3, A6, A7, B2; material_supply A (top level), A4, A5, E*; a wafer_supply / B2 row for an org that also has a fabrication row for the same source is an error (one fact, D57); `verified_on` may not be in the future (products, product_usage, product_specs, foundry_processes) | round 2 #4 |
| D57 (am. 2) | The per-(paper, org) category override named in D57 is implemented as curation key `wafer_categories` (checked before the qualifier keywords; its `basis` goes to the row note). chen2024 NanoLN -> A2.1 (paper p.5: commercially available 4-inch x-cut TFLN wafer, printed NONOLN; EO process_name: x-cut TFLN; the paper has no EO device rows, so the platform fallback had nothing). Soluxra gets org default A4 (witmer2020 EO process_name: SEO100C (Soluxra) spin-coated and poled; paper p.5: SEO100C from Soluxra is the EO polymer): material_supply, same pattern as Polaris / NLM | round 2 #2, #5 |
| D59 (am. 2) | Revision-letter rule also covers a dotted suffix (`JESD22-A118B.01`) | round 2 #4 |
| D60 (am. 2) | (1) Stress search order: parameter, condition, PK `variant`, printed standard. A variant starting with "before" is a baseline and is not searched (ectc51909.2023.00274-a-m1, iedm45741.2023.10413759-a-m6 stay die_shear). The parameter still decides first (ectc51687.2025.00027 variant "LTS" = low-temperature solder, the parameter's TCT wins). (2) For measurand warpage, "reflow" names the temperature profile or a flatness requirement along which warpage is measured (shadow moire), not a stress: such rows are warpage / warpage. (3) In humidity-type rows "T C / N %" without "RH" is a temperature / RH pair. (4) Measurand keywords: continuity, conductivity (not thermal) -> electrical_resistance; pressure test -> leak. (5) Validator: parsed t_min_c / t_max_c / temp_c / rh_pct must occur as numbers in the condition text; a measurement test_type has measurand equal to it or empty; qualifier needs a value; damp_heat needs a humidity keyword in parameter / variant / condition; restricted-source rows reject quotation marks in parameter, variant, condition, standard_printed, value_text, pass_criterion, scope, notes | round 2 #1, #3, #4, #6, #7 |
| D56 (am. 2) | Sandia top-level B notes for weigel2018 (author affiliation only; the paper states foundry processing of the Si photonic features, text p.4, but names no foundry) and boynton2020 (a CMOS line is stated, EO process_name Sandia MESA CMOS line; no B subcategory matches a CMOS line) | round 2 #7 |

## TODO

- [x] 1. `data/schema/supply_categories.yaml` (report section 1; 86 nodes).
- [x] 2. `data/schema/supply.schema.yaml` (six tables, `supply_` enums and patterns; shared `qualifier` enum reused).
- [x] 3. `src/photonics_atlas/rules_supply.py` (categories, role/category, product org/category, deterministic ids, locator form, basis/extraction, test ranges, rights) + id helpers shared with the script.
- [x] 4. `data/supply/curation.yaml` (EO fabrication categories, process fields, org defaults, wafer cell splits) from EO `process_name` / `wafer_supplier` text.
- [x] 5. `scripts/build_supply_seed.py` (`--dry-run`, `--limit`, `--only`, `--steps`, RunLog, append-only / skip-existing, org requests merge); new read-only adapter `adapters/pk_metrics.py`.
- [x] 6. Pilot on diverse rows (AMF + NLM johnson2025, AMF + CMC geravand2025, facility + wafer berman2026, LIGENTEC + Lumiphase + BRNC kohli2025, NSIT/SIMIT cai2025 and wafer cell split wang2024b, chelladurai2025; PK JEDEC TC/uHAST/HTS ectc32696.2021.00125 and GR-468 ectc51906.2022.00072); inspected; then full.
- [x] 7. `tests/test_supply.py` (23 tests: real data, rebuild reproduces the tables, parser units, 13 mutation tests).
- [x] 8. ruff format / ruff check / mypy / pytest / validate_db (supply files clean; see Progress).
- [x] 9. Counts, open issues and shared-file requests below.
- [x] 10. Fresh-context audit of the rows against the EO / PK records (coordinator, 2026-10-20); corrections applied below.
- [x] 10a. Second fresh-context audit of the corrected rows (coordinator, 2026-10-20); round 2 corrections applied below.
- [ ] 10b. Optional third audit pass on the round 2 rows (coordinator decides).
- [ ] 11. Later tranches: ~~registry orgs for the staged requests, then re-run (append-only adds their usage rows)~~ (done 2026-10-22: all 23 requests resolved, Shin-Etsu by D203, +1 usage row; see Progress); productized vendor/model scanner (products, product_usage with page locators) (scanner + 10-paper pilot staged 2026-10-22, D205-D209, section Vendor/model scanner tranche; audit, merge and full corpus open); datasheet harvest (U4); views.

## Progress

- 2026-10-20: inputs read (DevLog-000/001/002, supply report, registry schema, validator, schema loader, orgmatch, EO/PK adapters and atlas columns). Inventory: EO 233 papers; `foundry_or_fab` 97 papers / 52 names / 124 name occurrences (all map to registry orgs, 27 typed `facility`); `wafer_supplier` 74 papers / 36 distinct strings (NanoLN and most suppliers are not registry orgs: requests); `process_name` 151 papers. PK `metrics.csv`: 401 rows with `test_standard` (111 distinct strings, 72 papers). This plan written before implementation.
- 2026-10-20 13:35: schema, category tree, rules and header-only CSVs in place (header-only CSVs written first so the shared validator never sees a `built` table missing while parallel streams run).
- 13:38: pilot (7 EO papers, 2 PK papers): 17 usage rows, 3 process rows, 3 standards, 14 test rows. Found by inspection: single stress temperatures (HTS 150 C, LTS -40 C) not parsed -> rule added. Pilot rows (own output) reset before the full run.
- 13:38-13:40: full run: found by inspection: "unbiased HAST" matched both uhast and hast (-> other), and the 30 C/60 %RH soak of a Level-3 precon was attached to HTS / TC rows -> D60 rule restricted per test type; reliability_tests rebuilt. Second full run: 0 new, 0 differ on all tables (idempotent); rebuild-from-inputs test reproduces every table exactly.
- Results: `product_usage` 137 rows (100 EO papers, 57 orgs): facility_use / B7 75, fabrication 47 (B1 25, B 10 subcategory not stated, B5 4, B3 3, B2 3, B4 2), mpw_access / B6 1, post_processing / B5 1, wafer_supply 5 (A2.4 3, A2.2 1, B2 1), material_supply 8 (A4 7, A5 1). `foundry_processes` 39 observations, 21 orgs (siph 20, si_sin 4, tfln 3, sin 2, inp 2, sige_bicmos 2, plasmonic_organic 2, oeo_hybrid 1, bto 1, cmos 1, platform not stated 1). `standards` 24 designations (body_org_id empty: no standards body is a registry org yet). `reliability_tests` 401 rows from 72 PK papers (214 with a parsed designation; temperature range parsed 137, temp_c 79, rh_pct 49; test types: temperature_cycling 133, optical_loss 36, uhast 33, msl_preconditioning 33, high_temp_storage 31, other 31, adhesion 21, ...). `products`, `product_specs`: header only. `data/_staging/supply/org_requests.csv`: 23 requests (14 wafer suppliers, incl. NanoLN in 47 papers plus 3 printed variants; 8 standards bodies; 1 broker JePPIX).
- Verification: `validate_db.py` 0 errors, 15 warnings (all pre-existing; none from supply rules); `pytest -q` 65 passed, 1 failed (`tests/test_people.py`, P3 stream mid-build); `ruff check .` and `mypy` report errors only in P1/P3 files (`scripts/build_people.py`, `scripts/derive_transitions.py`, `scripts/scan_component_candidates.py`, `tests/test_people.py`); supply files clean under ruff format, ruff check, mypy strict.

- 2026-10-20 14:05: audit corrections started. Zip backup of data/supply/, data/_staging/supply/ and the owned code / DevLog taken before any rewrite (private scratch folder, `supply_backup_2026-10-20_pre_audit_fix.zip`). Each finding re-checked against the paper text first (001c.147203 p.4 Sec. IV.A: TS -55/125 C 1000 cycles after MSL Lv.3A precon; ectc51687.2025.00048 p.4: MSL4 30 C/60 %, 96 h, reflow peak 260 C is not a soak; kohli2025 author contributions: SiN wafers fabricated by Ligentec, growth and integration of the BTO by Lumiphase; valdez2023 / valdez2023a acknowledgements: Sandia staff for fabrication assistance; yin2026 p.1: multi-wafer project (MPW); cai2025 / wang2024b acknowledgements: LTOI wafers fabricated in NSIT and the SIMIT-CAS).
- 14:10: schema (4 new reliability_tests columns, `supply_test_measurand`), rules (anchors, deterministic test ids, designation-in-printed, revision letter, field-per-type, facility / wafer_supply, curly quotes), script (stress / measurand split, precon clause split, condition order, locator words, same-fact merge, alias / resolved requests, `--replace-ids`), curation (kohli2025 Lumiphase post_processing, valdez notes, yin2026 wording, wafer_parts notes for cai2025 / wang2024b / chen2024 / rahman2025 / weigel2018, alias_requests, request_notes).
- 14:12: coordinator: org curation round 2 merged (NanoLN -> org_jinan_jingzheng_electronics, Novel Si, Soitec, JePPIX, CrysTec, Grolltex, NGK, Soluxra, UK epitaxy facility, 8 standards bodies; SIMIT-CAS alias). Dry runs with the in-memory diff (all new / differ / stale rows printed and inspected). Found by inspection and fixed before writing: "Integration" in the org name "Shanghai Novel Si Integration Technology" triggered the new B5 keyword (keyword now applied to qualifiers only); precon clause swallowed a following "+ TC ..." step (step-aware split); "TCB 250 C, 100 MPa" (thermocompression bonding) and "Tc lid center" read as TC from condition text (range / cycle guard); "He leak after reflow" typed leak (leak is a measurand).
- 14:15: real run with `--replace-ids @<344 ids>` (every differing or no-longer-built id): product_usage 137 -> 197 (63 new, 11 replaced, 3 removed), foundry_processes 39 (2 replaced: yin2026 wording, gupta2023 broker org_jeppix now a registry org), standards 24 (23 replaced: 22 body_org_id filled, J-STD-020 note), reliability_tests 401 (305 replaced: new columns, 40 test_type changes, parsed fields). Second plain run: 0 new, 0 differ, 0 stale on all tables (idempotent). org_requests: 23 rows, 22 resolved, 1 open (Shin-Etsu).
- 14:19: verification: `validate_db.py --quiet` 0 errors, 15 warnings (none from supply rules); `pytest -q tests/test_supply.py` 30 passed; full `pytest -q` 69 passed, 4 failed in files not owned by this stream (`tests/test_people.py` x3, `tests/test_validate.py::test_name_basis_vs_origin`); ruff format / ruff check / mypy clean on the owned code files.
- 14:30: round 2 audit received. Backup zip `supply_backup_2026-10-20_pre_audit2_fix.zip` and copies of the CSVs taken (private scratch folder) before any rewrite. Sources re-checked: tcpmt.2026.3672227 rows m39 / m46 / m59 vs their SAT / warpage siblings (stress only in the PK variant); ectc51846.2026.00110-c (variant "after HTS 500 h"); witmer2020 text p.5 (SEO100C from Soluxra) and EO process_name; chen2024 text p.5 (4-inch x-cut TFLN wafer, NONOLN); weigel2018 text p.4 (foundry processing, no foundry named; the audit said p.3, the text.md page marker puts it on p.4); eptc67330.2025.11392108-a-m6 and ectc51906.2022.00309-a-m1 conditions (shadow moire 25-260 C; JEDEC reflow profile RT to 260 C); ectc51687.2025.00007-b-m2 / m3 conditions (110 C / 85 %, 130 C / 85 %).
- 14:37: dry run with `--replace-ids @<63 ids>` inspected (the 25 variant rows exactly as listed by the audit; 2 warpage rows; 2 RH pairs; 33 measurand-only changes from the new continuity / conductivity / pressure test keywords), then the real run: product_usage 197 (1 new witmer2020 Soluxra material_supply / A4, 1 removed old wafer_supply id, 3 replaced: chen2024 A2.1, weigel2018 and boynton2020 notes), reliability_tests 401 (59 replaced). Plain re-run: 0 new / differ / stale on all tables.
- 14:40: verification: `validate_db.py --quiet` 0 errors, 21 warnings (organizations / people / sources only; none from supply tables); `pytest -q tests/test_supply.py` 32 passed (2 new round 2 mutation tests, new parser and on-disk assertions); ruff format / ruff check / mypy clean on the owned code files.

- 2026-10-22 22:14-22:15: re-run for the staged org requests (TODO 11, org-requests part; registry side in DevLog-001
  round 4, decisions D200-D204). `data/_staging/supply/org_requests.csv` had 1 open request of 23 (Shin-Etsu,
  eo:witmer2020); D203 made it the brand-level registry org `org_shin_etsu`. Curation (`data/supply/curation.yaml`):
  request note updated; D204 per-paper `wafer_categories` entry (witmer2020, org_shin_etsu, A1; EO devices.csv
  substrate "float-zone SOI (Shin-Etsu)"), without which the row would be top-level A. Dry run inspected (row
  previewed), then the real run (append-only, no --replace-ids): product_usage 197 -> 198 (+1
  `use_eo_witmer2020_shin_etsu_wafer_supply`, wafer_supply / A1), foundry_processes 39, standards 24,
  reliability_tests 401 unchanged (PK metrics: 72 papers / 401 rows, unchanged by PK b1daf52); org_requests 23/23
  resolved, 0 open. Second dry run: 0 new / differ / stale on all tables. The 28 new PK orgs add no supply rows (supply
  reads EO papers and PK test standards only).

## Vendor/model scanner tranche (2026-10-22, TODO 11 scanner part)

Plan source: DevLog-000 P2 ("Productize the vendor/model scanner (dry-run, JSONL, skip-existing); pilot 10 papers,
audit; then EO 231 + packaging 296 + OFC 677"). Input: the 2026-10-20 scratch scanner (`vendors.py` ~330 vendor
regexes, `modelreg.py` ~120 model regexes, git-ignored `DevLog/research/scripts_2026-10-20/supply/`) and the seed list
of the [supply report](research/2026-10-20-supply-chain-taxonomy.md) section 3. This tranche: scanner + review /
staging path + 10-paper pilot only; no full-corpus run (after audit), no merge into `data/supply/` (coordinator, after
audit), no registry edits (vendor gaps go to `data/_staging/supply/org_requests.csv`). No network.

### Decisions (D205-D209)

| # | Decision | Rationale |
|---|---|---|
| D205 | Scanner `scripts/scan_vendor_models.py` (logic in `src/photonics_atlas/supply_scan.py`, hand decisions in `config/supply_scanner.yaml`) only proposes candidates. Corpora: `eo` (EO `references/<id>/text.md`), `pk` (packaging atlas `references/<id>/text.md`), `lit` (this repo `references/<id>/text.md`), `ofc2026` (`ofc_text_dir/<code>-*.md`; codes whose source has `same_as` are skipped, the EO copy is scanned). Only sources registered in `sources.csv`. Dictionary: (a) the config gazetteer (vendor name, regex, registry `org_id` explicit or resolved by `orgmatch` on the name, top-level category hint; vendors without a registry org stay in the gazetteer so gaps are visible), (b) every registry org of a vendor-like `org_type` (company, startup, foundry, business_unit, industrial_lab) by its name and aliases, literal, case-sensitive, word-bounded, >= 3 chars, minus the config stoplist; (c) model regexes with their gazetteer vendor and a subcategory hint. Text: page markers `<!-- page N -->` -> `p.N` (eo, pk, lit); OFC `_page_k_` figure markers -> `p.~(k+1)`, `pNA` before the first marker (D4). The reference list (last References / Bibliography heading after 40 % of the text) is not scanned; zones `front` (page 1 before the Abstract / Introduction), `ack` (Acknowledg* / Funding heading to the next heading) and `body` are flagged, not dropped. Candidate = one sentence x one vendor entity (a vendor match and a model match of the same gazetteer vendor in one sentence merge); flags: usage cue (verb list), zone, match kind (vendor / model / vendor+model). Output: JSONL with the sentence context (<= 300 chars) in the git-ignored `data/_local/supply/scan/candidates.jsonl` (restricted texts never leave the machine), skip-existing per source (`--force` rescans); `--batch <name>` also writes `data/_staging/supply/products/<name>/candidates.csv` without any text (ids, locator, zone, printed vendor, printed model, org id, hints, flags) for review verdicts. `--dry-run`, `--limit`, `--only`, `--corpus`; timestamped RunLog logs | scanner proposes, reviewer decides; rights (s1) |
| D206 | Review -> staging: the reviewer (LLM for the pilot) reads each candidate's page and records (1) a verdict per candidate in `candidates.csv` (`verdict` true / false, `reason`), (2) one line per fact in `review.csv` (source, printed vendor, org id, model as printed, category, role, basis, locator, stated_spec, notes, candidate ids). `scripts/build_supply_staging.py <batch>` turns `review.csv` into schema rows `products.csv` / `product_usage.csv` in the batch dir: `product_id = product_<org slug>-<model slug>` (helper `rules_supply.product_id`, checked by the validator), one product per (org, model as printed), status `unknown`, `usage_id` per D53, `extraction = scan_review` (new `supply_extraction` value: scanner candidate confirmed by a reviewer reading the page), basis `stated` (vendor printed with the item in the source) or `inferred_from_model` (only the model printed; vendor from the config model pattern, noted). Before writing, it checks against the cached text that the model string and (basis stated) a dictionary surface form of the vendor occur on the cited page; it validates the merged temp copy (`data/supply` + staged rows) with the full validator and fails on errors the batch introduces. Rows of vendors not in the registry are held (listed, request staged, D208); a later build appends them once the registry resolves the printed name. `--merge` appends to `data/supply/` (append-only, skip existing ids) and is for the coordinator after audit | never invent a model or vendor; replayable |
| D207 | Usage scope (a candidate is true only when the source states that the vendor's item / service was used, bought or supplied for the reported work): setup instruments, fab tools and consumables, wafers / materials, fibers / FAUs / connectors, packaging materials and tools, lasers and modules used as sources, software. False: affiliations, citations of others' work, commercial products named only for comparison, funding, trademarks or company names in introductions, the source's own device under test. Roles by category (D54): G -> fab_tool (also metrology in a packaging flow: SEM, X-ray CT), H -> test_instrument (lasers used as light sources of a measurement are H1 test instruments; laser_source / C only for a commercial laser die or module built into the reported system), F -> assembly_tool, E -> packaging_material (material_supply for A / E bulk materials), D -> fiber_component, C -> laser_source, J -> software, A -> wafer_supply / material_supply, B -> fabrication / mpw_access / post_processing. Vendor-only rows (no model) are kept when the item category is stated. Vendor as of the source (Agilent stays Agilent; renames are org_events, D6). One row per (source, org, role, product) | D6, D53, D54 |
| D208 | Vendor gaps (true candidates whose vendor has no registry org) are appended to `data/_staging/supply/org_requests.csv` as kind `vendor`, column `text`, printed = the vendor as printed, source ids unioned, note naming the batch and category; nothing in `data/registry/` is edited. `build_supply_seed.py merge_requests` keeps these rows (keyed by corpus, kind, printed, column) | registry curated elsewhere |
| D209 | Validator (rules_supply): `scan_review` rows need a page locator (`p.N` for eo / pk / lit, `p.~N` / `pNA` for ofc2026); products: `product_id == product_id(org_id, model)`; usage rows with a product bind org and category (existing). Pilot precision = true / all raw candidates, reported per zone, cue and match kind | traceability |

Amendments 2026-10-22 (during the pilot; rows above kept as written):

| # | Amendment | Rationale |
|---|---|---|
| D205 (am.) | Literal spaces in gazetteer / model regexes and registry names match any whitespace run (pymupdf wraps lines inside names: lit:mu2026 p.3 "Advanced / Micro Foundry" was missed by run 1). Page-1 sentences with a postal address or country are zone `affil`. Candidate model and vendor strings are whitespace-normalized (candidate ids hash the normalized model). Known gap kept: line-break hyphens inside a vendor name ("Amo- nics") are not matched by the scanner (the build check normalizes them) | pilot run 1 misses |
| D206 (am.) | Verdict reasons in `candidates.csv`: true = row (staged), org_gap (vendor not in the registry, held), covered (fact already in `data/supply` from the EO atlas import), no_vendor (item used but vendor neither printed nor inferable: SU-8, Sylgard 184, AFG-2125), dup (same fact as another candidate of the paper); false = affiliation, acknowledgement, own_org (the authors' own company as designer / test site), collaboration. One review line per fact; it lists every candidate id that points at it. Model slug: `+` -> `plus` (EBPG 5200+ and EBPG 5200 are different Raith products). A model whose tokens are printed but not contiguous (tiberi2025 p.9 EBPG Raith 5200; tcpmt.2025.3533388 p.2 brand and number split by a footnote marker) passes the page check with a warning and a row note. Products keep the printed spelling; a reviewer harmonizes variants within one paper (tiberi2025 XPD3120R / XPD 3120R -> one product, note) | pilot review |
| D207 (am.) | Commercial items evaluated in the reported work and rejected are in scope (lit:mu2026 p.19: Delo OB6268, Dymax 9622 tested as underfill and rejected; the row says so). A test service (VLC Photonics, johnson2025) is not a product row (no role); its instrument is | pilot review |
| D208 (am.) | Request notes name the gazetteer vendor when the printed form matches one (Loctite -> Henkel; EPO-TEK -> Epoxy Technology); printed variants stay separate requests (ThorLabs / Thorlabs, Ansys / ANSYS, Comsol / COMSOL), as in D57 | curation needs the canonical vendor |

### TODO

- [x] S1. Plan (this section) before code.
- [x] S2. `config/supply_scanner.yaml` (gazetteer + models + stoplist, ported from the scratch lists; registry ids checked).
- [x] S3. `src/photonics_atlas/supply_scan.py` + `scripts/scan_vendor_models.py` (dry-run, JSONL, skip-existing, --limit / --only / --corpus / --batch, RunLog).
- [x] S4. `scripts/build_supply_staging.py` (review.csv -> products / product_usage, page checks, org requests, temp-copy validation, --merge for the coordinator).
- [x] S5. Schema / rules (`scan_review`, product id helper and check, page locator per corpus) + tests (`tests/test_supply_scan.py`, 12 tests).
- [x] S6. Pilot: 10 papers (EO instrument-heavy, foundry, PK assembly with adhesives / FAU, one lit), raw scan, review every candidate, staged rows, validate.
- [x] S7. Precision report, vendor gaps, checks (ruff, mypy, pytest, validate_db).
- [x] S8a. Fresh-context audit of pilot_01 (coordinator, 2026-10-22); fixes D290-D299; second pilot pilot_02 on unseen papers (section Pilot audit fixes).
- [x] S8b. Second audit (2026-10-23), fixes D316-D325, pilot_01 + pilot_02 merged into data/supply (D324).
- [ ] S8. Full corpus in batches (coordinator dispatch; first batch gate D325); was: coordinator review of pilot_02, then merge (`build_supply_staging.py pilot_01 --merge`), registry curation of the vendor requests, then EO 231 + PK 296 + OFC 677 in batches.

### Progress

- 2026-10-22: inputs read (DevLog-003 D51-D60, schema, rules_supply, build_supply_seed, DevLog-000 D4/D6/D7, supply
  report section 3, scratch scanner scripts). Registry coverage of the scratch vendor list: 112 of 337 entries resolve
  to a registry org by name (most instrument, fab-tool and material vendors are gaps). Plan written before code.
- 22:30-22:37: config (308 gazetteer vendors, 166 model patterns at run 1; 319 / 180 after tuning, 101 vendors with a
  registry org id; stoplist of large
  companies / common words for the automatic registry forms), library, scanner. Region detection first used free-form
  heading lines; pymupdf wraps lines, so short text lines were taken as headings (didier2026 acknowledgements ended
  after one line): replaced by a list of known section headings; Nature-style Methods after the reference list are
  scanned; papers without a References heading (tiberi2025) cut at a `[1] ... [2]` run.
- 22:37 run 1 (raw, the precision of record): pilot papers eo:mao2024 (CC-BY, instrument-heavy), eo:valdez2023a
  (instrument-heavy, restricted), eo:didier2026 (CC-BY, fab tools + instruments), eo:johnson2025 (foundry paper: AMF
  dedicated run + NLM SOH post-processing, restricted), eo:tiberi2025 (CC-BY, graphene modulator, fab + RF test),
  pk:ectc51687.2025.00027 (2.5D assembly line: bonders, dispenser, molding, grinding, reflow), pk:ectc51846.2026.00176
  (FAU active alignment; adhesives unnamed), pk:eptc59621.2023.10457729 (Dymax optical epoxy, glass interposer),
  pk:tcpmt.2025.3533388 (glass interposer, EPO-TEK underfill, RF probes), lit:mu2026 (open; AMF visible-light
  platform, flip-chip LD integration, adhesives). 134 candidates; every one reviewed against its page (local text,
  nothing copied into the repo). Saved as `pilot_01/candidates_run1.csv`.
- 22:40-22:47 tuning (D205 am.): whitespace-flexible patterns, page-1 address flag, model normalization, 11 vendors and
  14 model patterns added for items seen while reading the pilot pages (Fairview Microwave, AT Microwaves, FiberLabs,
  Menlo Systems, Koheron, Arroyo, Maple Leaf Photonics, Kitagawa Seiki, MSC Software, Cotronics, TFS / PI / Delo /
  MUSASHI / Allied forms, Keysight M80xx / P50xx / DSOX / PathWave). Run 2 on the same papers: 165 candidates (118 keep
  their run-1 id and verdict; of 47 new ids, those matching a run-1 candidate by source / page / vendor / kind / model
  carry its verdict, the rest were reviewed on the page).
- 22:48-22:49 review -> `pilot_01/review.csv` (115 facts), `build_supply_staging.py pilot_01` dry run, then real run
  (org_requests.csv backed up first to the private scratch folder; the build only appends request rows; a
  `build_supply_seed.py --dry-run` afterwards keeps all 80 request rows). Found by the build checks and fixed: the
  model slug merged EBPG 5200+ (didier2026) and EBPG 5200 (tiberi2025) into one product id (`+` -> `plus`); two models
  printed non-contiguously (warning + note rule).
- 22:53 verification: `validate_db.py` 0 errors, 16 warnings (none from supply tables); `pytest -q` 255 passed
  (`tests/test_supply_scan.py` 12 new; `test_supply.py` atlas-import test now also accepts merged scan_review rows);
  `ruff check .`, `ruff format --check` (owned files), `mypy` (81 files, strict) clean. Not run: the full corpus (after
  audit), `--merge`.

- 23:18-23:39 audit fixes (D290-D299): config backed up to the private scratch folder first; scanner, config, build
  and rules changed; pilot_01 re-scanned (candidates_run2.csv = previous file), re-linked and rebuilt; registry checked
  stable (mtime 23:12, DevLog-001 round 5 entry) before the config org refresh; org_requests.csv backed up before each
  build (only appends and status refreshes; the D278 TFS note is kept). pilot_02 scanned once, all 51 candidates
  reviewed, 3 papers read in full, built. Verification: `validate_db.py` 0 errors, 15 warnings (none from supply);
  `pytest -q` 288 passed (`tests/test_supply_scan.py` 20 tests); `ruff check .`, `ruff format --check` (owned files),
  `mypy` (81 files, strict) clean. Not run: `--merge`, the full corpus.

### Pilot results (2026-10-22)

Raw scanner precision (run 1, before tuning; true = the candidate points at a usage fact stated in the paper):

| cut | true / candidates |
|---|---|
| all | 111 / 134 (0.83) |
| zone body | 111 / 117 (0.95); front 0 / 5, ack 0 / 12 |
| usage cue in sentence | 97 / 108; no cue 14 / 26 |
| kind | vendor+model 61 / 61, model only 7 / 7, vendor only 43 / 66 |
| per paper | didier2026 16/16, mao2024 14/14, tiberi2025 13/13, valdez2023a 16/18, johnson2025 7/17, mu2026 19/20, ectc51687.2025.00027 12/21, ectc51846.2026.00176 2/3, eptc59621.2023.10457729 3/3, tcpmt.2025.3533388 9/9 |

False candidates (23): acknowledgements 12 (thanks to vendors and staff), affiliations 6, own-company roles 4
(johnson2025: NLM / Enosemi as designer and test site), collaboration 1. All false ones are vendor-only matches; every
false one sits in front / ack / affiliation text or names the authors' own company. Run 2 (tuned on the same papers,
optimistic): 142 / 165 (0.86), body 142 / 147.

Recall (not measured exhaustively; facts found by reading the candidate pages plus a sweep of parenthetical
vendor / model mentions): 22 of the 115 facts had no run-1 candidate of their own (vendors missing from the gazetteer
12, models in a proposed sentence but not in the model list 5 (Keysight M8050 / M8042A / M8009 / M8059A / N1000),
line-wrapped name 1 (AMF in mu2026), printed forms the regex did not cover 4 (Allied Multiprep, PI RS-40, Delo, ARB
Rider without its vendor)); run 2 proposes all 115 (tuned on these papers). Not proposed and not rowable: GW Instek
AFG-2125, SU-8, Sylgard 184 (vendor not printed).

Staged (`data/_staging/supply/products/pilot_01/`, not merged): 115 review facts -> 44 usage rows + 41 products for
registry vendors; 71 facts held for 52 printed vendor names without a registry org (57 requests in
`data/_staging/supply/org_requests.csv`, kind vendor, all open); 4 true candidates already covered by the EO atlas
import (NanoLN valdez2023a, NGK didier2026, AMF / NLM johnson2025).

| staged usage by category | rows |
|---|---|
| H test instruments (H1 1, H2 2, H3 3, H4 4, H5 5, H6 6, H7 6, H9 6, H12 1, H17 2) | 36 |
| G fab tools (G1 2, G5 3) | 5 |
| F7 molding (APIC Yamada VCM-330MS) | 1 |
| J software (Keysight PathWave EM Design) | 1 |
| B1 fabrication (AMF, lit:mu2026) | 1 |

Staged vendors: Keysight 17 usage rows, FormFactor 5 (incl. 1 vendor-only), Newport 4, DISCO 3, Raith 2, Anritsu 2,
Finisar 2, Agilent 2, Micram, Hewlett-Packard, Ando Electric, Yokogawa, Cascade Microtech (vendor-only), APIC Yamada,
AMF (vendor-only fabrication) 1 each. Basis: 112 stated, 3 inferred_from_model (Heidelberg DWL 66+, Active
Technologies ARB Rider AWG-7204, Cotronics Duralco 132; all three held as org gaps).

Held facts by role: test_instrument 27, fab_tool 15, software 9, assembly_tool 9, packaging_material 8,
fiber_component 2, wafer_supply 1. Vendor gaps (printed names): AIMECHATEC, ANSYS / Ansys, AT Microwaves, Active
Technologies, Allied, Amonics, Arroyo Instruments, Bruker, COMSOL / Comsol, Centellax, Cotronics, Delo, Dymax, EPO-TEK,
Elionix, FEI, TFS, Fairview Microwave, FiberLabs, Ficontec, Finetech, GGB Industries, Heidelberg Instruments, Hitachi
High-Tech, KITAGAWA SEIKI, Keyence, Koheron, Loctite, Lumerical, MSC Software, MUSASHI, Maple Leaf Photonics,
MenloSystems, Nordson, Nufern, Oxford Instruments, Oz Optics, PI, Panasonic Connect, Rohde & Schwarz, SAMCO, SENJU,
SHF, Sakura Seiki, Santec, Schott, Tektronix, ThorLabs / Thorlabs, Veeco. Packaging papers: adhesives and FAUs stay
mostly unnamed (ectc51846.2026.00176), the named ones (Dymax OP-29, EPO-TEK 301-2, Loctite, Delo, Cotronics) are all
gaps; the assembly-equipment vendors of ectc51687.2025.00027 are gaps except APIC Yamada and DISCO.

### Audit checklist (pilot_01)

1. Each staged usage row against its page (`review.csv` locator; local texts): vendor printed, model string as printed,
   role / category (D207), stated_spec a paraphrase of what the page states (restricted sources: valdez2023a,
   johnson2025, the four pk papers: no verbatim text).
2. Verdicts in `candidates.csv` (and `candidates_run1.csv` for the raw precision): especially false own_org /
   collaboration (johnson2025) and the covered / dup / no_vendor reasons.
3. Vendor-as-of-source choices: Agilent 8164B / 81110A (not Keysight), Ando AQ6317B (not Yokogawa), Finisar XPDV /
   XPD (not Coherent), Cascade Microtech (tcpmt: printed Cascade, currently FormFactor), Hewlett Packard 83651B.
4. Product identity: printed-spelling products (EBPG 5200+ vs EBPG 5200; N4372 vs N4372E; DCA-X vs N1000; Model
   number forms 1471, Model 110), categories of borderline items (101-190D / CSR-4 calibration substrates as H9;
   EPO-TEK 301-2 as E3 underfill; Duralco as E7; Borofloat 33 as A7 wafer_supply; VH-2347 top-level F).
5. Inferred vendors (3 held rows) and the `infer: false` model list in `config/supply_scanner.yaml`.
6. Recall: read the methods / setup sections of 2-3 pilot papers for vendors the review missed.
7. Org requests (57 rows): which printed names are brands of one vendor (Loctite / Henkel, EPO-TEK / Epoxy Technology,
   TFS / FEI / Thermo Fisher, Lumerical / Ansys, PI / Physik Instrumente) and which registry entities to create.
8. Scanner config: stoplist (giants like Intel, TSMC, Samsung are not matched from the registry automatically; they
   enter only through gazetteer regexes) and the gazetteer entries left without an org because the registry entity is
   a subsidiary (Toptica: only TOPTICA Photonics Inc.; SUSS MicroTec: only SUSS MicroTec Lithography; EXFO: only EXFO
   Solutions) or ambiguous (Coherent Corp. vs Coherent, Inc.).

### Pilot audit fixes (2026-10-22, decisions D290-D299)

Input: fresh-context audit [2026-10-22-supply-scanner-pilot-audit](audits/2026-10-22-supply-scanner-pilot-audit.md)
(pilot_01 rows sound, recall weak, full corpus no-go until findings 1-5, 8, 9, 11 are fixed). D205-D209 are full;
D270-D279 belong to org round 5.

| # | Decision | Rationale |
|---|---|---|
| D290 | Product identity: key = vendor org + canonical model (`rules_supply.canonical_model`: NFKC, uppercase, every separator dropped, `+` and `.` kept; id slug lowercase, `+` -> `plus`); the build strips a leading vendor / brand token of the product's own vendor from the printed model (COMSOL Multiphysics -> Multiphysics, EPO-TEK 301-2 -> 301-2); `products.model` holds that display form, the usage row note keeps `printed model: ...` when it differs. Families go to `products.product_line` (new `review.csv` column): DCA-X family vs N1000 / N1000A models; when only a family is printed the product is family-level (model = product_line = DCA-X, UXR, Infinity, ACP, \|Z\| probe). Distinct suffixes stay distinct models (N4372 vs N4372E; EBPG 5200 vs EBPG 5200+). Replaces the D206 printed-spelling key before any merge (product ids are immutable, D8); fixes the COMSOL / Comsol build failure (audit finding 8) | audit 8 |
| D291 | (amends D207) Acknowledgement candidates are not false by default: an acknowledgement that states supply (equipment lent, materials or samples provided, devices fabricated at a facility) is a usage fact with basis stated and a note naming the acknowledgement; thanks for help, discussion or support stay false. Pilot verdicts unchanged (all 14 pilot_01 ack candidates are thanks); pilot_02 ofc2026:Th3C.1 acknowledgements state fabrication at two facilities -> facility_use rows | audit 7 |
| D292 | Scanner text fixes: (1) `" ?"` / `" *"` in patterns -> `\s*`, `" "` -> `\s+` (NewFocus, MenloSystems, LakeShore matched again); (2) model tails: no `\w*` / `\s?\w*` after a word stem (optional token must start with a capital or digit: Titanium, "Lumerical and" no longer match), `\S*` tails -> `[\w.+/-]*[\w+]`; candidate models cleaned (`clean_model`: whitespace, line-break hyphens joined, trailing punctuation and trailing lowercase words dropped); product names removed from vendor regexes (Lumerical, HFSS, RSoft, FIMMWAVE, Tidy3D, CSAR, OrmoComp, Picoprobe, Fineplacer, Duralco, Megtron, ...: model patterns now); (3) registry forms of <= 4 capitals are dropped (SLM, IDT, MEC, ...; `registry_short_forms_keep` empty), AGC only as AGC Inc / with a glass model, MPI TITAN dropped, Hewlett-Packard not before Enterprise / Labs, DOW not before CORNING, Corning lookbehind `(?<!Dow\s)`; (4) reference lists: headings with span anchors, bold, section numbers and the block glyph, References and links, singular Reference only when a `[1]` / `1.` entry follows within 400 characters (mu2026 comparison table), bulleted `- [1]` lists; (5) inline Acknowledgement / Funding / Disclosure labels zone their paragraph (ack), competing-interest and disclosure blocks are zone `coi` (not scanned for unlisted names); (6) OFC `<span id="page-k-m">` anchors are page marks (p.~(k+1)); (7) sentences do not split inside parentheses or after Inc. / Co. / Ltd. / Fig. / initials; (8) usage cue words from / by / with / via dropped (cue is now discriminative: pilot_01 cue true 119 / 122 true, cue false 46 / 71) | audit 1-6, 13, 14 |
| D293 | Gazetteer org = explicit `org`, else the registry match of the vendor name (orgmatch, no ROR), unless `resolve: false` (Coherent); after org round 5 had settled (registry mtime 23:12, DevLog-001 round 5 entry) the resolved ids were written into the config (46 refreshed; 147 of 337 gazetteer vendors now carry an org). Registry twins of a gazetteer org are skipped, forms equal to a gazetteer name are skipped, and candidates group by org (one candidate per sentence and org). Vendor names of >= 5 letters match case-insensitively unless `case: true` (33 common-phrase names such as CORNERSTONE, Cadence, Single Quantum, New Focus). Candidate ids hash only what the paper prints (source, offset, printed vendor, printed model), so registry or gazetteer changes do not change them. The build resolves an empty `org_id` by the registry match of the printed vendor, then by the gazetteer vendor of the printed form | audit 9, 10 |
| D294 | Gazetteer-independent candidates, kind `unlisted` (body and ack zones only): a parenthetical "(Name Model)" or "(Model, Name ...)" with a model token (letters and digits, no unit) and a capitalized 1-4 word name, or a company name with a case-sensitive legal suffix (Inc, Ltd, GmbH, AG, Corporation, Co., Ltd, LLC, ...). Unlisted candidates are reported separately in the precision tables. Gazetteer additions from the audit recall list: Evatec, VIGO, Akrometrix, Shinko, FLIR, AtaiTec, Aixtron, Moorfield, Graphene Platform, Eravant, LPKF, Pasternack, Gel-Pak, Voltcraft, ams OSRAM, JDSU, Yenista, Lumerical (with Inc / Solutions only), Cree, Rogers models | audit 10 |
| D295 | Lineage: `infer: false` on models whose vendor changed over time (Lumerical, HFSS, CST, RSoft / OptoDesigner, Savannah / Fiji, Dektak / Dimension, EXFO T100S / XTA-50 / CTP10, Agilent-era Keysight models N52xx, N437x, PNA-X, E5071C / E5080, N90x0, B29xx, DSOX). Config `lineage:` (Keysight: Agilent, Hewlett-Packard; Yokogawa: Ando; Finisar: II-VI, Coherent; Ansys: Lumerical; Bruker and Cambridge NanoTech: Veeco; FormFactor: Cascade Microtech; Newport / New Focus; EXFO: Yenista): a model printed next to a lineage vendor merges into one candidate carrying the printed vendor (tiberi2025 Agilent 8164B, valdez2023a Agilent 81110A, Ando AQ6317B now one candidate each) | audit 11 |
| D296 | Category / role rulings: RF power sensors (R&S NRP) are top-level H with a note (H3 = optical power meters; config hint fixed); glass cores of packaging test vehicles are E8 packaging_material (tcpmt Borofloat 33), glass panels hosting waveguides are A7 wafer_supply (ectc51846.2026.00302 D 263 T eco); a flux cleaner, a vacuum press, a device tray are top-level F with a note; thermometers and IR cameras top-level H with a note; metal foil growth substrates and polymer waveguide materials top-level A (material_supply) with a note. A co-author company that supplied an item for the work is a usage fact (lit:mu2026 AMF fabrication and ams OSRAM laser diodes, the latter org = the ams OSRAM entity of the paper's affiliations); own_org false stays for the authors' company as designer or test site (johnson2025) | audit rows 5-7, recall list |
| D297 | Rights: restricted rows paraphrase anything longer than an instrument-type name (at most about 5 consecutive words of the source); one pilot_01 row reworded (ectc51846.2026.00176 alignment phrase). The NC-ND redistribution mismatch (lit CC-BY-NC-ND sources open_license_ok, eo ones restricted) is a registry question, not changed here | audit 15 |
| D298 | Vendor requests: notes list the union of category / role pairs of the held facts and the gazetteer vendor found by searching printed vendor + model (TFS Helios -> FEI, PI RS-40 -> Physik Instrumente); notes amended by curation (TFS, D278) are kept; every vendor request's status / resolved_org_id is refreshed from the current registry on each build (matcher, then gazetteer org) | audit 16 |
| D299 | Merge rule for several batches: `build_supply_staging.py <batch> --merge` per batch in sequence (each run rebuilds against the current `data/supply/`, so shared products such as Keysight M8199B are appended once); a combined validation of data/supply + pilot_01 + pilot_02 has 0 new errors. Full corpus stays no-go until the coordinator reviews pilot_02 (precision below) | sequencing |

Coordinator rulings on the open items (2026-10-22):

| # | Decision | Rationale |
|---|---|---|
| D299a | Registry orgs of type facility (and their aliases; config `registry_facility_types: [facility]`, 49 orgs) are proposed as candidates (origin `facility`, hint B7) in methods / body and acknowledgement text only, never in front matter or affiliations; a facility_use row needs an explicit fabrication / processing statement (D291) | pilot_02 Th3C.1 recall misses |
| D299b | Virginia Diodes only by its full name or an extender / multiplier model (VNAX, WRx.x AMC / SAX / MixAMC); never bare VDI | pilot_02 VDI Technology Center funding false positive |
| D299c | `unlisted` candidates only in body text (never front matter, acknowledgements, funding or competing-interest text) | pilot_02 unlisted 0 / 6, all acknowledgement partners / funding |

#### pilot_01 after the fixes

- Re-scan (same 10 papers; tuned on them, optimistic): 193 candidates, 165 true (0.85); body 165 / 170, front 0 / 6,
  ack 0 / 14, affiliation 0 / 3; vendor+model 101 / 101, model 18 / 18, vendor-only 46 / 74; unlisted 0 on these papers.
  Run-1 / run-2 verdicts carried by (source, page, printed vendor, model); every candidate re-checked against the
  review lines (`candidates_run2.csv` keeps the previous file).
- Review: audit rows 1-7 corrected (N1030A spec + a mao2024 DCA-X family row; tiberi2025 Infinity family; tcpmt ACP
  and |Z| probe family products; NRP110T.02 -> H; Borofloat 33 -> E8 packaging_material; YWV-4635S -> F); 20 facts
  from the audit recall list added (all page-checked by the build; Shinko as package-substrate supplier E4, ams OSRAM
  laser diodes C1, Eravant x2, Evatec vendor-only, ...); N1000 / DCA-X product_line.
- Build: 135 facts -> 120 staged usage rows + 108 products (org round 5 added most gap vendors), 15 held (Allied,
  TFS, Evatec, VIGO, Akrometrix, FLIR, Pactech, Rogers, AtaiTec, Moorfield, Graphene Platform, Eravant x2, Gel-Pak,
  Voltcraft, ... see org_requests), 0 new validation errors. Staged by top-level category: H 65, G 20, F 11, J 10,
  E 10, D 2, B 1, C 1 (subcategories in the build log).

#### pilot_02 (unseen papers, run once with the fixed scanner; precision of record)

Papers (seeded random draw 20261022 from sources with text, excluding pilot_01; OFC from the component scanner's
device list, score >= 4): ofc2026:W4E.5, ofc2026:Th3C.1, ofc2026:W2A.15, pk:ectc51846.2026.00302,
pk:ectc51687.2025.00097, pk:ectc32696.2021.00125, eo:yin2026, eo:hulyal2026, lit:hu2023, lit:huang2019a.

| cut | true / candidates |
|---|---|
| all | 31 / 51 (0.61) |
| zone body | 31 / 33 (0.94); front 0 / 10, ack 0 / 8 |
| kind | vendor+model 11 / 11, model 3 / 3, vendor-only 17 / 31, unlisted 0 / 6 |
| usage cue | 21 / 23 with cue, 10 / 28 without |

False (20): affiliations 10 (7 author blocks of one Micron paper), collaboration 5 (ack project partners, all
`unlisted`), citation 2 (lit:hu2023 IHP and a prior-art comparison), funding 2 (VDI Technology Center matched
Virginia Diodes' VDI; an ack funding agency as unlisted), acknowledgement 1. Body-zone precision holds (0.94); the
low overall number is driven by author blocks and ack paragraphs, which the review discards quickly by zone.

Recall: 21 review facts, 18 with a candidate of their own (0.86). Papers read in full: ofc2026:Th3C.1 2 / 4 (the two
fabrication facilities named in the acknowledgements are not vendor-typed orgs and are not in the dictionary),
pk:ectc51846.2026.00302 1 / 1, eo:hulyal2026 3 / 3: 6 / 8 (0.75). Other papers swept (parentheticals, company
suffixes, usage keywords): 1 miss (KOHERAS SuperK Compact, brand not in the gazetteer). Staged: 15 usage rows + 9
products (incl. 2 facility_use rows from an acknowledgement, D291), 6 facts held (SHF, Keithley, OFS Fitel, KOHERAS,
Micro Resist Technology x2), 1 covered (yin2026 AMF).

Rescan after D299a-c (once, same 10 papers; the first-scan numbers above stay the numbers of record; the first scan
is kept as `pilot_02/candidates_scan1.csv`): 47 candidates, 34 true (0.72); body 31 / 33, ack 3 / 4 (the three
facilities, all true: Th3C.1 x2 and ofc2026:W2A.15 UCSB Nanofabrication Facility, a new facility_use fact), front
0 / 10; unlisted 0 candidates (the 6 acknowledgement / funding ones and the VDI funding match are gone). Review facts
22, 21 with a candidate (0.95); full-read recall 8 / 8 (Th3C.1 now 4 / 4). Rebuild: 16 staged usage rows + 9
products, 6 held, 0 new validation errors. pilot_01 was not re-scanned after D299a-c (its candidates predate them).

Superseded by D299a-c: open items (1)-(3) below. Open: (1) facility orgs in acknowledgements (facility_use) are not candidates: add registry orgs of type facility to
the dictionary in ack zones; (2) `VDI` alone over-matches (funding agency): restrict Virginia Diodes to the full name
or a VNA extender model; (3) unlisted kind had 0 / 6 on pilot_02 (all ack partners / funding) and found the audit
misses only after they were added to the gazetteer: restrict unlisted to body zone or keep for review; (4) full
corpus still no-go until the coordinator accepts these numbers.

### Second audit fixes and pilot merge (2026-10-23, decisions D316-D325)

Input: [2026-10-23-supply-scanner-pilot2-audit](audits/2026-10-23-supply-scanner-pilot2-audit.md) (0 wrong facts; merge
conditional go after M1-M6; full corpus no-go until M1-M3, F1-F4). D310-D315 belong to the org stream.

| # | Decision | Rationale |
|---|---|---|
| D316 | (coordinator ruling) "a portion of this work was performed in / at <facility>" is a facility_use row (DevLog-002 D42: a shared facility where work was performed), never fabrication: ofc2026:W2A.15 UCSB Nanofabrication Facility kept; eo:valdez2023a SDNI already exists as an EO atlas import (covered); eo:didier2026 ShanghaiTech Material and Device Lab ("fabricated by", registry type facility) -> facility_use / B7 | audit P2-3, M5, M6 |
| D317 | Product identity residuals: (1) a printed model that differs from the catalogue form only by a missing suffix letter is not taken as that model: the row uses the family-level product when the family is printed (johnson2025 "Keysight N1000 DCA-X" -> product DCA-X; hu2023 "N1000A" stays N1000A with product_line DCA-X); (2) vendor-strip keeps the printed name when only a generic word would remain (Ansys Optics, not Optics); (3) a leading Model / Type / Series word and a trailing System / Series word are dropped from the product model (Model 110 -> 110 with product_line Picoprobe; Multiprep System -> Multiprep), the printed form stays in the usage note; (4) software releases: model = product name, release in the note (MARC2023.4 -> MARC, release 2023.4); (5) product_line UXR for UXR0702AP (prefix of the family product); Infinity for I67-A-GSG by coordinator ruling, noted as vendor part numbering not printed in the paper; the build also sets product_line when a family-level product of the same vendor prefixes the model (logged warning) | audit D-1 to D-8, F2 |
| D318 | Gazetteer org gaps: explicit `org:` for LioniX, SMIC, Innolight, Eoptolink, Accelink, Epoxy Technology (org_epo_tek: EPO-TEK 301-2 -> 301-2), Taiyo Ink, Senju Metal, Musashi Engineering, FEI, SHF (SHF now resolves in lit / pk / OFC; the registry alias is eo-scoped), Physik Instrumente, Luceda, ams OSRAM; `resolve: false` with a note for the intentional six (Coherent, Henkel / Loctite, SUSS MicroTec, Vistec, EXFO, Toptica). `load_dictionary` reports a warning for any other gazetteer vendor without org whose pattern matches a registry org name (none now; logged by the scanner, asserted by a test) | audit M3 |
| D319 | Rows: MUSASHI / SENJU vendor_printed = the printed company strings (the 23:43 registry edit removed the short aliases); ams OSRAM laser diodes top-level C with a note (no node for blue FP edge emitters); mao2024 N1030A / DCA-X stated_spec only printed words; lit:hu2023 cdb278f3f4cf9 true / dup (the p.2 Finisar PD is this work's reference PD); stale Th3C.1 notes replaced; second-audit recall facts added: tcpmt Rogers 4450 F prepreg (pilot_01), huang2019a Metricon 2010 prism coupler (pilot_02; no candidate in the pilot_02 scan of record) | audit M1, M4, recall |
| D320 | `canonical_model` folds accents (NFKD, combining marks dropped; micro sign -> U): TherMoire / TherMoire with accent are one product | audit D-9, F1 |
| D321 | `unlisted` noise filters: NAME_STOP += step(s), phase, case, stage, publisher names; numeric-range model tokens rejected; company names in footer / copyright lines (publisher, publishing, (c) / copyright sign, all rights reserved, Wiley-VCH) skipped; no unlisted candidates in funding sentences (supported / funded / sponsored / grant / program); an all-digit model in "(Name Model)" only when the name is a registry org name or alias. Metricon added (gazetteer + model 2010) | audit F3, recall |
| D322 | Case gaps: 'SMART photonics' added to the case-sensitive SMART Photonics entry (eo:hillier2025). The other 32 `case: true` vendors were checked for a lowercase second word in printed forms: none known; the first full-corpus batch is the check | audit F4 |
| D323 | A top-level category id warns only when that node has children (J has none, so software rows no longer warn); products in a top-level category carry the category note (build copies the usage-row `category:` note; three merged products updated: Kitagawa VH-2347, R&S NRP110T.02, Sakura YWV-4635S) | validator noise after merge |
| D324 | Merge executed (D299): zip backup of data/supply and data/_staging/supply first (private scratch, `supply_backup_2026-10-23_pre_pilot_merge.zip`); `build_supply_staging.py pilot_01 --merge` (+108 products, +122 usage rows), then `pilot_02 --merge` (+7 products: M8199B and XPDV3320R already present, +17 usage rows); combined validation 0 new errors. `data/supply/products.csv` 115 rows, `product_usage.csv` 337 (198 atlas imports + 139 scan_review). `build_supply_seed.py --dry-run` keeps the 139 scan rows (reported as stale, kept); its rebuild test now compares only atlas_import rows | merge |
| D325 | Full corpus: not started (coordinator dispatches in batches). Gate: the first batch of about 30 papers (at least 8 OFC, 8 PK) is measured against the second audit (body precision about 0.9, overall 0.6-0.7, recall vs a full read of 3 papers) before continuing. Known residuals for the first batches: OE-format reference lists inside the first 30 % of the text (6 sources), model list additions (Keysight ADS, N5290A / N5291A, Thorlabs APD410), the bare CST alternation of Dassault CST, ofc2026:Th3C.1 "AIM die" (implied supplier, left out) | audit (b) |

Progress 2026-10-23 00:00-00:08: config / scanner / build / rules changed (D317-D323); pilot_01 re-scanned once
(`candidates_run3.csv` = previous file; 193 candidates, 3 new facility candidates reviewed: didier2026 SMDL x2 true,
valdez2023a SDNI true / covered; 3 earlier ids no longer produced: MUSASHI registry twin and ams OSRAM GmbH affiliation
merged into their gazetteer vendors, SENJU p.3 duplicate); pilot_02 not re-scanned (its numbers stay as recorded).
Final batches: pilot_01 137 facts -> 122 usage rows, 108 products, 15 held; pilot_02 23 facts -> 17 usage rows, 9
products (7 new at merge), 6 held. pilot_02 precision of record with the D319 verdict correction: first scan 32 / 51
(0.63), rescan after D299a-c 35 / 47 (0.74). Org requests: backup taken; builds only append / refresh status (1 new:
Metricon). Verification: `validate_db.py` 0 errors, 15 warnings (none from supply); `pytest -q` 301 passed;
`ruff check .` clean; `mypy` (81 files, strict) clean.

### D326 and the first full-corpus batch full_01 (2026-10-23)

| # | Decision | Rationale |
|---|---|---|
| D326 | (coordinator ruling) `product_line` only when the family is printed on a cited page of the row's source, or an earlier merged row of the same product carries it (its source printed it). Enforced by the build (error otherwise). The merged I67-A-GSG product (Infinity from vendor part numbering, D317) was corrected through the build path: pilot_01 review line emptied, then `build_supply_staging.py pilot_01 --merge --replace-ids product_formfactor-i67agsg,use_eo_mao2024_formfactor_test_instrument_formfactor_i67agsg` (new option: listed ids already in data/supply are replaced by their rebuilt rows, mutable fields only; ids immutable) after a zip backup (`supply_backup_2026-10-23_pre_d326.zip`); diff = exactly those two rows. Batch files now always hold every row the batch builds (also rows already merged), so they stay the batch record | coordinator |
| D326a | Residual scanner fixes before full_01: OE-format reference lists (References and links / REFERENCES right after the abstract, followed by an Introduction heading) are refs even in the first 30 % (lit:hosseini2015, bock2010, billah2018, tanizawa2015, vazquezcordova2014); Introduction ends a reference list; models Keysight ADS (Advanced Design System / Keysight ADS / PathWave ADS, infer false), N5290A / N5291A (infer false), Thorlabs APD410 series; Dassault CST no longer matches a bare CST. After the full_01 scan (not re-scanned; numbers below are of record): the conflict-of-interest heading also matches the fl ligature (kohli2025), Namics `case: true` (matched dy-namics) | second audit residuals; full_01 review |
| D326b | full_01 gate results (below); full_01 staged, not merged | D325 gate |

full_01: 30 papers drawn with seed 20261024 from registered sources with text, excluding pilot_01, pilot_02 and the
second audit's 20 unseen papers: ofc2026 W4H.3, M4F.5, M2J.2, Th3D.4, M1D.6, Th1A.2, W3B.3, M2D.5, W3K.5; pk
ectc51529.2024.00125, ectc51906.2022.00323, tcpmt.2023.3312037, iwlpc52010.2020.9375887, ectc51909.2023.00009,
ectc51909.2023.00307, ectc51687.2025.00071, ectc51687.2025.00148, icep61562.2024.10535612; eo nenezic2026, powell2024,
singer2025, zhang2026b, kohli2025, kieninger2020, liu2026a; lit maeda2023, li2025, dangel2013, zhang2021, bogaerts2006.
Scanned once (92 candidates; 4 OFC and 1 EO paper had none), every candidate reviewed in context.

| cut | full_01 | second audit (20 unseen, sample of 60) |
|---|---|---|
| all | 56 / 92 (0.61) | 35 / 60 (0.58) |
| body | 50 / 60 (0.83) | 33 / 45 |
| body without unlisted | 47 / 57 (0.82) | 33 / 37 (0.89) |
| ack | 6 / 9 | 2 / 5 |
| front / affiliation / coi | 0 / 17, 0 / 4, 0 / 2 | 0 / 8, 0 / 2 |
| vendor+model / model / vendor-only / unlisted | 9 / 9, 14 / 16, 30 / 64, 3 / 3 | 11 / 11, 9 / 13, 15 / 28, 0 / 8 |
| by corpus | eo 21 / 28, lit 17 / 25, pk 16 / 31, ofc2026 2 / 8 | eo 16 / 20, lit 13 / 20, pk 5 / 9, ofc2026 1 / 11 |

False (36): affiliations / author blocks 21, generic mentions 3 (ABF described in an Ajinomoto paper's introduction,
an SMF28 design target), competing-interest 3, collaboration 2, citations 2, acknowledgement thanks 2, funding 1, a
word fragment 1 (dy-namics -> Namics, fixed), a future demonstrator 1. Body false 10 of 60. True includes 11
no_vendor (li2025 UHNA7, vendor not printed), 7 covered by EO atlas imports, 6 duplicates.

Recall: 37 review facts, 35 with a candidate of their own (0.95; misses: HP 83440D in lit:maeda2023, printed as bare
HP; Okuno Chemical Industries plating additives in pk:ectc51909.2023.00307). Full reads: ofc2026:Th1A.2 2 / 2,
eo:powell2024 3 / 3 rowable (SPR700-1.0 resist without vendor not counted), pk:ectc51909.2023.00307 7 / 8: 12 / 13
(0.92); second audit full reads 12 / 12. Two acknowledgement supply facts (D291) became rows: imec provided the
waveguide circuits (eo:nenezic2026), IMEC P-line processing (lit:bogaerts2006).

Staged (`data/_staging/supply/products/full_01/`, not merged): 37 facts -> 26 usage rows, 18 new products (20 in the
batch file, 2 already merged: Keysight N1000A, M8199B), 11 held. Held vendors (10 new open requests): micro resist
technology (ma-N2405, inferred), Vanguard Automation (Sonata 1000, VanCore B), Toptica (resolve: false), Waltz (STAC
test die, an `unlisted` candidate), SUSS MicroTec (resolve: false), Tokyo Electron, Parker Corporation, Tosetz,
Okuno Chemical Industries, Mitaka Kohki. Staged by category: H 14, E4 4, B1 3, A 2, A2.1 1, G4 1, J 1.

Verification 2026-10-23 00:26: `validate_db.py` 0 errors, 15 warnings (none from supply); `pytest -q` 302 passed, 1
failed (`tests/test_views.py::test_no_review_ids_in_committed_views`, views stream editing build_views.py at the
time, not touched here); `ruff check .`, `mypy` (81 files, strict) clean.

### Full-corpus scan and parallel review set-up (2026-10-23, decisions D327-D329)

| # | Decision | Rationale |
|---|---|---|
| D327 | (coordinator) D325 gate passed on full_01; full_01 merged with `build_supply_staging.py full_01 --merge` after a zip backup (`supply_backup_2026-10-23_pre_full01_merge.zip`): +18 products, +26 usage rows, 0 new validation errors. `data/supply/products.csv` 133 rows, `product_usage.csv` 363 (198 atlas imports + 165 scan_review) | gate |
| D328 | Full-corpus scan run once as a single process: `scan_vendor_models.py --split-prefix full --split-start 2 --split-size 100 --force` = every registered source with text not yet in a batch dir (1169 of 1214; the 45 pilot / full_01 sources are not rescanned), one shared local JSONL, split in a deterministic corpus-mixed order (sha1 of the source id) into full_02 .. full_13; each batch gets a text-free `candidates.csv` (verdict / reason empty) and `sources.csv` (source_id, corpus, n_candidates; papers without candidates included for recall reading). New read-only reviewer helpers `--print-batch <batch>` (candidates with context from the local JSONL) and `--print-source <source_id>`. Review format v2 (`review.csv` columns + `line_kind`, `reason`): candidate verdicts come from review.csv alone (fact lines make their candidates true; verdict lines carry true reasons covered / no_vendor / dup or false reasons); the build writes the verdicts and the row / org_gap / dup reasons into the batch's `candidates.csv`. `build_supply_staging.py <batch> --check-review`: review-only validation (verdict coverage and conflicts, unknown candidate ids, page checks of vendor / model / product_line, category / role / basis / locator form / stated_spec / quotation lint also for held lines, facility_use org type, temp-copy validation); no log files, no batch files, no org requests | parallel review |
| D329 | `data/_staging/supply/products/REVIEW_CONTRACT.md`: brief for reviewer subagents (write only `<batch>/review.csv`; format; verdict rules D207 / D291 / D299a-c / D316 / D296; product identity D290 / D317 / D326; category / role table; vendor as of the source; rights D297; page check; recall reading of methods / setup / acknowledgements of every paper in `sources.csv`; self-check and hand-off). The supply owner builds and merges the batches sequentially after review | parallel review |

Batches (scan 2026-10-23 00:32-00:35, 1169 sources, 3963 candidates):

| batch | papers (eo / lit / ofc2026 / pk) | candidates |
|---|---|---|
| full_02 | 98 (19 / 6 / 50 / 23) | 301 |
| full_03 | 98 (7 / 5 / 57 / 29) | 324 |
| full_04 | 98 (9 / 3 / 63 / 23) | 310 |
| full_05 | 98 (21 / 8 / 54 / 15) | 334 |
| full_06 | 98 (12 / 5 / 55 / 26) | 303 |
| full_07 | 97 (19 / 2 / 49 / 27) | 358 |
| full_08 | 97 (17 / 3 / 54 / 23) | 331 |
| full_09 | 97 (19 / 5 / 38 / 35) | 370 |
| full_10 | 97 (20 / 3 / 52 / 22) | 286 |
| full_11 | 97 (32 / 4 / 49 / 12) | 346 |
| full_12 | 97 (20 / 8 / 46 / 23) | 277 |
| full_13 | 97 (23 / 4 / 48 / 22) | 423 |

### Cross-batch rulings, harmonization and merge of full_02 .. full_13 (2026-10-23, decisions D340-D349)

Rulings: `data/_staging/supply/products/COORD_RULINGS.md` (R1-R25, the R4 amendment and the R4 follow-up lists). The
original reviewer files are kept in the private scratch folder; every harmonized batch passed `--check-review`.

| # | Decision | Applied |
|---|---|---|
| D340 | R1-R3, R13, R15, R16 (orgs and fabrication): printed "Samsung Foundry" -> `org_samsung_electronics` with the printed form in notes; specific printed Stanford facilities (SNSF / SNF) are facility_use lines next to the umbrella EO import (not covered); the authors' own company / institute is a fabricator only with an explicit fabrication / processing statement; a named product of a co-author company used in the work is a fact | full_05 Th3F.6 Samsung org; full_07 witmer2020 SNSF + SNF verdict covered -> two facility_use lines; full_04 re-checked for R15 (its own_org verdicts are platforms or the paper's own developments, no named product skipped: no change) |
| D341 | R4 + amendment, R5, R6, R10, R23-R25 (equipment classes): pluggables / transceivers / transponders / CDM / ICR modules -> top-level C, role laser_source, note "category: commercial module in setup"; line systems / ROADMs / routers / OCS -> top-level H, note "category: network / transport equipment in setup"; compute / IT gear and datasets not entered; commercial modulators C7 with note "test-setup modulator"; FPGA / RFSoC boards H6 or top-level H; reliability equipment top-level H; discrete electronic dies and measurement services not entered; standards used in the method -> K / standard_reference | modules -> C: full_02 (CISCO CIM-8, NeoPhotonics CDM + ICR merged into one vendor-only line per R8), full_03 (Fujitsu ICR, Adtran QuadFlex / Teraflex), full_04, full_05, full_06 (Arista, Nokia), full_07 (Voyager, ADVA, Ciena), full_09 (Cisco SFP+), full_10 (Adtran, Fujitsu CFP2-DCO, ADVA), full_13 (Ciena WaveLogic); network notes standardized (Lumentum / Polatis / Ciena line systems); full_04 Edgecore host switch removed (compute / IT); full_11 park2026 ZCU111 -> H; C7 notes in every batch; follow-up lines added from the cited pages: full_08 Tu2K.2 (Ciena 6500, Waveserver 5, WaveLogic 5 Extreme), M1B.5 (Nokia 800G ZR OSFP modules, IXR-6e; acknowledgement states Nokia provided them), M1A.3 (Lumentum ROADMs; Edgecore stays other); full_09 M3Z.15 (Nokia 1830, SR 7750), Tu2C.2 (Nokia 1830 PSS), M4B.6 (Broadcom Bailly CPO switch system); full_13 Th2A.34 (ADTRAN Quadflex -> C; ADTRAN Controller MNC -> J software), W3K.6 (ThinkQuantum QUKY -> H), M4A.2 (TIP Phoenix transponder -> C; NEC network operating system -> J), Tu2A.3 OIF 400ZR -> K / standard_reference (R24) |
| D342 | R7, R8, R11, R12, R14, R18, R19, R20 (printing and identity rules): models without a vendor in recall not entered; colliding vendor-only lines merged; explicit org_id for unambiguous printed variants (bare "Oxford" for an instrument -> Oxford Instruments); models kept as printed; renamed facilities held under the printed name; OFC recall locators from page markers; a product of the authors' company needs the vendor printed with it, in a trademark notice or in a cited reference | full_02 pk:ectc51846.2026.00130 Reflexion LK Prime removed (vendor not printed with it; its candidate joins the Endura fact as dup); EVG120 kept with vendor_printed EVG (brand printed within the model name); pk 00096 Applied Materials DLT kept (vendor printed with the item) |
| D343 | R9 scanner fix: supplementary material after the reference list ("Supplementary Information for: ...") resumes scanning; "Supplementary References" is a reference heading; the [1] ... [2] fallback is used only when no main References heading exists (a body line starting [1] before a real References heading is not a list); test `test_r9_supplementary_after_references`. Regions changed for 10 sources (eo cai2025, fukui2025, kari2025, khalil2026, kim2025, larocque2024, thureja2025; lit heim2025, qi2025, wilson2019); targeted rescan with `--batch full_14 --batch-new-only` (new option: only candidate ids in no other batch, plus sources.csv): full_14 = 10 sources, 13 new candidates, not reviewed | R9 |
| D344 | R21, R22: the gazetteer no longer maps Thermo Fisher / Thermo Scientific / TFS to FEI (FEI is printed FEI only; new gazetteer vendor Thermo Fisher Scientific without org, lineage FEI -> Thermo Fisher Scientific); those lines are held. Bare or possessive "Lumerical" without the company printed -> verdict no_vendor | R22 lines converted: full_02 oz2023, full_05 nelan2022 (MODE), tiberi2026, full_06 zhang2024, full_07 yang2022, kawahara2025 x2, Th2A.4, full_12 chelladurai2025 x2, papadovasilakis2023a, pilot_01 tiberi2025 (held, candidate -> no_vendor); "Lumerical Inc." lines (nevlacsil2020, lee2020a, xu2022) and "Ansys Lumerical" lines kept |
| D345 | Merge: zip backups before each run (`supply_backup_2026-10-23_pre_full02_11_merge.zip`, `..._pre_full12_13_merge.zip`, `..._pre_resolved_merge.zip`); `build_supply_staging.py <batch> --merge` in sequence full_02 .. full_13, `validate_db.py` 0 errors after each. full_09 - full_11 first stopped on cross-batch product conflicts (D348) and were merged after the fix | see table below |
| D346 | Held rows of earlier batches that the registry now resolves are appended by a plain re-run (D206 design): pilot_01 +15 usage / +9 products (1 still held), pilot_02 +6 / +2, full_01 +11 / +7 | registry rounds 5-6 added the gap vendors |
| D347 | R17: one org request per vendor over all batches, rebuilt by every build from the held fact lines of every batch review.csv (vendor = gazetteer vendor of the printed form, else the printed-name key); the row lists corpora, sources, category / role pairs, batches and "printed variants: A + B"; curated text of earlier rows is kept after "; curated: " (TFS keeps the D278 ruling); resolved vendor rows of earlier rounds stay as records; other request kinds untouched; the rebuild is idempotent | org_requests.csv |
| D348 | Build changes found during the merge: (1) the D317 family-prefix auto rule is dropped (it set product_line PNA on PNA-X); product_line comes only from the review line (D326); product lines set by it on products merged in full_02 - full_08 (UXR on UXR models, ABF on ABF GX-92 / GL-102, ACP on ACP-110-GSG-200, PNA on PNA5225B) are kept: the family token is printed within the model; (2) product_line conflicts compare canonically (PicoProbe = Picoprobe); (3) one category per product across batches: later lines take the merged product's category with a note (Keysight N4391B H7, Zeiss Ultra Plus G7, ASMPT Amicra NANO F2, EXFO CTP10 H); (4) lint: locator words (acknowledgement, "per the", page numbers) are not allowed in stated_spec; seven merged rows fixed through `--replace-ids` (wolf2018a SHF MUX; full_13 Hitachi Chemical, AGC, Ajinomoto, anderson2025 SNSF / SNF, li2024 N1032A) | merge |
| D349 | Open: full_14 review (13 candidates; the 10 sources' supplementary sections also need recall reading); 355 open vendor requests (org round); org-round notes from the rulings: Oxford scoped alias (R11), EXFO alias is corpus-scoped (eo / pk EXFO lines stay held), Georgia Tech IEN -> Institute for Matter and Systems as an org_event (R14), a Thermo Fisher Scientific org (R21); owner questions: a node for network / transport equipment and commercial modules (R4), discrete electronic dies (R23) | next steps |

Per-batch merge results (rows added to data/supply; held = facts whose vendor has no registry org at merge time):

| batch | usage rows | products | held |
|---|---|---|---|
| full_02 | 122 | 78 | 52 |
| full_03 | 129 | 66 | 40 |
| full_04 | 104 | 66 | 49 |
| full_05 | 157 | 74 | 41 |
| full_06 | 90 | 48 | 37 |
| full_07 | 164 | 75 | 64 |
| full_08 | 138 | 63 | 35 |
| full_09 | 138 | 48 | 68 |
| full_10 | 131 | 51 | 40 |
| full_11 | 151 | 54 | 40 |
| full_12 | 97 | 27 | 32 |
| full_13 | 180 | 51 | 67 |
| pilot_01 / pilot_02 / full_01 re-run (D346) | 15 / 6 / 11 | 9 / 2 / 7 | 1 / 0 / 0 |

Totals after the merge: `data/supply/products.csv` 852 rows, `product_usage.csv` 1996 (198 atlas imports + 1798
scan_review). Org requests: 355 open vendor requests (569 held lines over all batches; most frequent by sources:
JEOL 13, EXFO 9, Zeon 7, Dassault CST 6, Keopsys 6, NKT Photonics 6, Rigol 6, Swabian Instruments 6, Thermo Fisher
Scientific 6, Allresist 5, Besi 5, Cambridge NanoTech 5, ID Photonics 5, Namics 5, Optec 5, SPTS 5, Synopsys 5, Tokyo
Ohka Kogyo 5). Verification 2026-10-23 01:41: `validate_db.py` 0 errors, 15 warnings (none from supply); `pytest -q`
307 passed; `ruff check .`, `mypy` (81 files, strict) clean. The registry was being edited by the org stream during
the merges; no registry file was touched here and every merge validated with 0 errors.

## Audit corrections (2026-10-20)

| Finding | Re-check against source | Done |
|---|---|---|
| #1 001c.147203-b-m1..m4 typed msl_preconditioning, 60 C / 60 %RH | p.4 Sec. IV.A: TS -55/125 C after MSL Lv.3A precon (HTS 125 C 24 h + THS 60 C/60 %RH 40 h + reflow 260 C x3) | thermal_shock, t_min -55, t_max 125, temp / RH empty; classify on condition before standard (D60 am. 2) |
| #11 ectc51687.2025.00048-a-m14 temp_c 260 | p.4: MSL4 = 30 C/60 %, 96 h; 260 C is the reflow peak | temp_c empty; msl no longer in SINGLE_T_TYPES (only a T/RH soak pair) (D60 am. 3) |
| #2 / #3 / #22 kohli2025 Lumiphase wafer_supply A2.4 + fabrication B5 | author contributions: growth and integration of the BTO by Lumiphase | one post_processing / B5 row; growth / integration / deposition keyword -> B5 (D57 am. 1, 2); old ids removed via --replace-ids |
| #4 kohli2025 LIGENTEC fabrication B2 + wafer_supply B2 | SiN wafers fabricated by Ligentec; SiN waveguides produced in a photonic foundry | one fact: fabrication / B2 kept (foundry_or_fab), stated_spec "SiN wafers", note records the merge; wafer_supply row removed. Rationale: Ligentec patterned the SiN waveguide wafers (foundry fabrication); the wafer_supplier cell restates the same delivery |
| #10 PK variant / scope not imported; negative-IL sign | PK scope of ectc51687.2025.00012 IL rows: "sign as printed (negative)" | new columns variant, scope, qualifier; note on negative optical_loss rows (D33 stores loss positive, not flipped) (D60 am. 4) |
| #25-#30 validator gaps | n/a | all rules added (D54 am., D59 am., D60 am. 5) + 6 new mutation tests (anchors, test ids / tv / source, designation-in-printed + revision letter, field-per-type, facility / wafer_supply / curly quotes) |
| #32 no replace path | n/a | `--replace-ids` (comma list or `@file`; replace or remove), stale ids reported; backup zip taken before the first rewrite; unit test `test_merge_table_replace` |
| #34 SIMIT-CAS staged as new org | cai2025 acknowledgements: LTOI wafers fabricated in NSIT and the SIMIT-CAS | alias request (kind alias, alias_of_org_id); registry alias applied by the coordinator, so the cai2025 SIMIT wafer_supply / A2.2 row now exists. The registry alias note asks to check the role: kept as wafer_supply because the paper states the LTOI wafers were fabricated there (wafer manufacture = wafer supply, D54) |
| #33 request count | n/a | request_notes: 22 new-org rows = 18 distinct orgs (NanoLN x4 printed forms, Novel Si x2) + SIMIT-CAS alias; status / resolved_org_id columns: 22 resolved, Shin-Etsu open |
| #35 NanoLN parentheticals in stated_spec | EO cells of rahman2025, weigel2018, chen2024 | wafer_parts overrides: printed NanoLN, empty qualifier, legal name / NONOLN remark in notes |
| #14 / #15 test_type mixes stress and measurand | n/a | `measurand` column; precon clause split; "MSL3 preconditioning + reflow" = msl_preconditioning (D60 am. 1, 2) |
| #5 valdez2023 / valdez2023a Sandia top-level B | acknowledgements: fabrication assistance; foundry not named | kept B, note added (D56 am.) |
| #6 org-default notes cite other papers | n/a | `category: curation org default` (5 rows) |
| #7 locator words in stated_spec | n/a | moved to notes (chelladurai2025, horst2025, wang2024b, cai2025; new rows didier2026, li2025b) |
| #8 yin2026 wording | p.1: multi-wafer project (MPW) | process_name and curation why use the printed wording |
| #16 D59 wording | n/a | D59 am. (normalization, J-STD-020 IPC/JEDEC prefix note) |
| #17 ectc51529.2024.00093-c-m1 lacks test_standard | PK row: TC -55 to 120 C, no test_standard | not edited (PK is read-only); upstream follow-up below |

### Round 2 (2026-10-20)

| Finding | Re-check against source | Done |
|---|---|---|
| 1. 25 rows whose stress is only in PK `variant` (tcpmt.2026.3672227-a-m40..m45, m47..m58, m61..m64; ectc51846.2026.00110-c-m2, m4, m5) | variants "TC/B ... cycles", "HTSL ... h", "uHAST ... h", "after HTS 500 h"; siblings m39 / m46 / m59 typed TC / HTS / uHAST | variant searched after condition, before the printed standard; "before ..." variants skipped; 25 rows now TC / HTS / uHAST with parsed fields; replaced |
| 2. witmer2020 Soluxra wafer_supply / A | paper p.5: SEO100C from Soluxra as the EO polymer; EO process_name SEO100C (Soluxra) | org default A4 -> material_supply / A4; old id removed via --replace-ids |
| 3. warpage rows typed reflow | eptc p.3 / 00309 p.4: warpage by shadow moire along a reflow profile | warpage / warpage (reflow not a stress for measurand warpage) |
| 4. validator gaps | n/a | 10 rules added (revision suffix .NN, restricted quotes in reliability_tests text, role vs anchor column, fab + B2 wafer_supply, parsed numbers in condition, measurement type vs measurand, qualifier needs value, role vs subcategory, damp_heat humidity keyword, verified_on not in the future); mutation tests `test_mutation_round2_usage`, `test_mutation_round2_tests_and_standards` |
| 5. chen2024 NanoLN top-level A; D57 names an override not implemented | paper p.5: 4-inch x-cut TFLN wafer (NONOLN) | `wafer_categories` implemented; chen2024 -> A2.1 |
| 6. ectc51687.2025.00007-b-m2 / m3 RH empty | conditions 110 C / 85 %, 130 C / 85 % | T C / N % accepted as a pair in humidity rows; rh_pct 85 |
| 7. Sandia notes; measurand keywords | weigel2018 text p.4; boynton2020 EO process_name | notes added; continuity / conductivity / pressure test keywords added. The optional tcpmt note ("standard as paired in the paper's Table II") was not added: the PK printed standard is already kept verbatim in `standard_printed` |

## Open items

- Upstream (advanced-packaging-atlas, audit #17): `metrics.csv` ectc51529.2024.00093-c-m1 (TC cycles without resistance change, -55 to 120 C) has an empty `test_standard`, so it is not imported; if the paper cites a standard, PK should record it and a re-run appends the row.
- (Resolved 2026-10-22, D203.) Shin-Etsu (witmer2020 wafer_supplier) was still an open request after org curation round 2; it is now the brand-level registry org `org_shin_etsu` (which Shin-Etsu company supplied the SOI is not stated). witmer2020 Soluxra is material_supply / A4 since round 2.

- (Superseded 2026-10-20: org curation round 2 resolved 22 of 23 requests; kept for history.) Org requests (`data/_staging/supply/org_requests.csv`) need registry curation (P0 workflow, not this tranche): NanoLN / Jinan Jingzheng Electronics (47 EO papers; variants "NanoLN, China", "NanoLN, Jinan", "NanoLN, Jinan Jingzheng Electronics Co., Ltd."), Shanghai Novel Si Integration Technology / "Novel Si Integration Technology", "SIMIT-CAS" (an alias candidate of the registry SIMIT org; not decided here), NGK Insulators, Grolltex, CrysTec, Shin-Etsu, Soitec, Soluxra, UK national epitaxy facility (Sheffield), JePPIX; standards bodies JEDEC, AEC, ASME, ASTM, IEC, IPC, ISO, Telcordia (the standards-body requests list PK papers whose cited designations imply the body; the body string itself is not always printed). After curation, a re-run appends their rows (existing rows untouched).
- 187 of 401 test rows have no parsed designation (generic "JEDEC ...", typos kept as printed: "MIL Standard 833", "JEDEC ESD22-B111", "IPD/JEDEC-9704A", "MIL-STD-883-2"); 25 rows typed `other` after the 2026-10-20 amendment (was 31; sequence rows naming two or more stresses, parameters with no stress and no measurand keyword).
- Usage rows carry atlas anchors, not page locators (EO paper-level fields have none); a later pass over the EO text can add `p.N` locators (extraction manual) without changing ids.
- Standard titles, scopes and access are empty / unknown until a source that states them is cited (datasheet / standards tranche).
- `data/supply/curation.yaml` holds hand decisions; if the project prefers all hand decisions under `config/`, it can move to `config/supply_curation.yaml` (path constant `CURATION` in the script).
- Registry `organizations.supply_roles` is not filled by this tranche (registry is curated elsewhere); a later step can derive it from `product_usage` roles with these rows as evidence.
