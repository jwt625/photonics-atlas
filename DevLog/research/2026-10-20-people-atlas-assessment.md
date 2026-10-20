---
title: People / affiliation / organization atlas - assessment of local data
date: 2026-10-20
status: assessment (read-only; no source file modified); redacted 2026-10-20 for publication (named derived transitions and name-only matches removed; unredacted copy kept local-only)
owner: research subagent (coordinator session 2026-10-20)
---

# People atlas assessment (2026-10-20)

Goal: assess building a photonics people / affiliation / organization atlas (who did what where; moves between
organizations, e.g. the Intel silicon-photonics diaspora) by merging local data only. No web, no LinkedIn, no
downloads. Every person/org/date below is cited to a file + row id. A person appearing with two organizations on
two papers is a publication-affiliation signal (grade A for the affiliation on that date), never proof of an
employment interval.

Source roots (sibling repositories of this one):

| Alias | Path | Content used |
|---|---|---|
| LIN | `PlayGround/20260823_photonics_lineage/` | `schema.yaml` v0.2.0, `edge_types.yaml`, `source_policy.md`, `PROGRESS.md`, `canonical/{people,organizations,edges,events,sources}.yaml`, `research/intel_siph_lineage_initial.md`, `people_seed.yaml` |
| EO | `eo-modulator-atlas/data/` | `people.csv`, `paper_authors.csv`, `author_affiliations.csv`, `organizations.csv`, `org_sites.csv`, `papers.csv`; DevLog-017/018/020 |
| PK | `advanced-packaging-atlas/data/` | `author_affiliations.csv`, `organizations.csv`, `org_sites.csv`, `papers.csv`; `config/org_aliases.yaml`; DevLog-006 |
| OFC | `PlayGround/ofc-2026/ofc_full_metadata.json` | 830 `record_kind == presentation` records |
| OFCT | `PlayGround/20260320_OFC/extracted_text/*.md` | 677 extracted OFC 2026 papers (headers only inspected) |

Analysis scripts ran in the session scratchpad with `uv run --no-project --with pyyaml python`; they are not
persisted. Section C states every rule so the numbers can be re-derived.

---

## A. Schema comparison and shared core model

### A.1 What each dataset models

| Concept | LIN (v0.2.0) | EO | PK | OFC metadata |
|---|---|---|---|---|
| Person entity | `people.yaml` 288; id `person_*`; typed aliases (106 alias names); `name_disambiguator`; `current_organization_id/title`; `timeline_research` defined but populated on 0/288 | `people.csv` 1509; `person_id` = ORCID when known else name slug; `orcid` 374/1509; `variants` (`;`); `merge_basis` (exact_name, compatible_name+shared_org, shared_coauthor, orcid) | none: author string per affiliation row (1497 distinct normalized strings, 201 of them initial-abbreviated, e.g. "M. C. Yew") | `authors_json` `{name, affiliation, raw}`; 6056 author rows, 3803 distinct names |
| Org entity | `organizations.yaml` 172; `org_*`; typed aliases; 11-value `organization_type`; `parent_organization_id` (40); `predecessor_ids/successor_ids` (10 orgs); founded/dissolved; status; website; sources | `organizations.csv` 284; key = `org_name` (own preferred name, DevLog-020 #9); 8 types; `parent_org` (40); `ror_id` 170/284; `name_source` | `organizations.csv` 144; key = `org_name`; `parent_org` (21); printed variants in `notes`; alias map `config/org_aliases.yaml`; no ROR | free-text affiliation string (735 distinct); `presenter_affiliation` and `presenter_country` empty on all 830 |
| Location | `geographies[]` country/region/city | `org_sites.csv` (lat/lon, precision, Wikidata/OSM ref) | `org_sites.csv` + `site_id` | none |
| Person-org relation | `edges.yaml` 556; person-org types used: technical_leadership 126, employment 121, founder 117, research_training 83, executive_role 46, publication_affiliation 23, patent_affiliation 5, collaboration 3, advisor 1; `start_date/end_date` as `date_value{value,precision}` (322/556 edges no start); per-edge evidence grade + sources + locator; status | `author_affiliations.csv` 2880 rows: paper x author_index x aff_order; `kind` primary 2262 / additional 600 / present_address 18; `unit`, `locality`, `country`, `source` (paper / crossref; 34 crossref rows), `locator` | same model, 1996 rows, plus `aff_id`; `kind` incl. present_address (2 rows) | one affiliation per author (no multi-affiliation, no unit) |
| Date | `date_value` with precision | `papers.published_on` (174/233 filled) else `year` | `papers.year` only (no day) | `session_start` 2026-03-16..19 |
| Org events | `events.yaml` 23 (21 acquisition, 1 merger, 1 team_formation); org-org edges acquisition 21, spinout 10 | prose in `notes` only (e.g. Infinera Corporation parent_org Nokia Corporation with acquisition URL) | comments in `config/org_aliases.yaml` L4-5 (Xperi/Adeia spin-off 2022, Showa Denko Materials/Resonac rename 2023, Tokyo Tech/Institute of Science Tokyo merger 2024) | none |
| Evidence grade | A-D + X per edge (491 A, 60 B, 5 C); `sources.yaml` 282 (253 A, 27 B, 2 C) | none on affiliations; `papers.repro_grade` A-C means simulation reproducibility (name clash, different meaning) | none | none |
| Derived | `transition` and `talent_flow` (schema only; builders still v0.1 per `PROGRESS.md` open issues) | lineage panel heuristic: last author = PI proxy (DevLog-017) | none | none |

Key structural differences:
- LIN is claim-based and curated (biographies, filings); atlases are observation-based (every printed affiliation). They are complementary: LIN supplies intervals/roles/events, atlases supply dense dated point observations.
- Org keys differ: LIN uses stable `org_*` ids; EO/PK use the display name as the key (a rename changes the key; EO renamed 43 orgs on 2026-10-05, DevLog-020).
- Person keys: EO `person_id` switches from slug to ORCID when an ORCID appears (unstable); PK has no person table; OFC has names only.

### A.2 Proposed shared core model (all atlases)

```
person            person_id (person_<slug>, immutable, collision suffix _2), display_name, orcid?, disambiguator?,
                  aliases[] {name, lang, alias_type: native_name|transliteration|abbreviated|variant|former_name},
                  research_status, notes
person_xref       person_id, scheme (orcid|eo_person_id|pk_name_key|lin_id|ofc_name), value, basis
                  (orcid|exact_name+shared_org|shared_coauthor|manual), grade, reviewed_on
organization      org_id (org_<slug>, immutable), name (own preferred, DevLog-020 #9), org_type (unified enum below),
                  country, parent_org_id?, ror_id?, wikidata_qid?, website?, status, founded/dissolved (date_value)
org_alias         org_id, alias, alias_type (printed_variant|legal_name|former_name|native_name|abbreviation|brand),
                  valid_from?, valid_to?, source_id
org_event         event_id, event_type (acquisition|merger|spin_off|spinout|rename|dissolution|unit_reorg),
                  participants[{org_id, role}], announced_on, effective_on (date_value), evidence {grade, sources}
source            LIN source entity unchanged (url, type, grade, accessed_date, archive_url, content_hash);
                  papers become source rows (src_paper_<atlas>_<paper_id>, DOI)
affiliation_obs   obs_id, person_id, org_id (most specific org), printed_org, unit, locality, country,
                  kind (publication|conference|patent|employment|founder|executive|technical_leadership|
                        research_training|advisor|board|investment),
                  aff_role (primary|additional|present_address|null),
                  shape (point|interval), observation_type (active_on|started_on|ended_on|announced_on),
                  date | start/end (date_value), source_id, locator, evidence_grade, status, atlas, visibility
derived           person_org_span (first/last active_on per person x org; labelled "observed span", not tenure),
                  transition (LIN schema: direction_status, directness, basis + new basis publication_sequence),
                  talent_flow (aggregate; keeps person_ids and obs_ids)
```

Unified `org_type`: `university, company, startup, research_institute, government_lab, national_lab, foundry,
facility, consortium, business_unit, academic_lab, industrial_lab, venture_fund, other` (union of LIN, EO, PK).

### A.3 Publication affiliation to career-timeline evidence

| Input | Observation | Grade | Rule |
|---|---|---|---|
| EO/PK `author_affiliations` row, `kind=primary/additional`, `source=paper` | `kind=publication`, `observation_type=active_on`, date = `published_on` (day) else `year` (year precision) | A | Point observation only. Never extend to an interval. |
| Same, `source=crossref` (EO 34 rows) | same | A, flagged `source=crossref` | Publisher-deposited metadata. |
| `kind=present_address` (EO 18, PK 2) | two observations: primary org `active_on` (work done) and present-address org `active_on` at publication | A | Explicit move statement: transition basis `explicit_move_statement`, direction confirmed. Example: `eltes2020` authors 1, 11, 12 (Felix Eltes, Jean Fompeyrine, Stefan Abel) primary IBM Research - Zurich, present address Lumiphase. |
| OFC metadata `authors_json` | `kind=conference`, `active_on` = session date | B (conference-organizer record) | One affiliation per author; drops co-affiliations (see C.4). |
| OFC paper header (OFCT md) | `kind=publication`, `active_on` 2026-03 session date | A | Needs extraction + audit (section B.3). |
| LIN edges | interval or point as recorded | as recorded | Unchanged. |

Move signal from many papers: per person, group observations by org (after alias/parent collapse); an ordered
transition A -> B is emitted when the last A observation precedes the first B observation by >= 90 days (day
precision) or by >= 1 calendar year (year precision), and A and B never appear on the same paper. Output
`direction_status=confirmed` with `basis=publication_sequence`, `directness=unknown`. Overlapping spans produce
`direction_status=unknown` (co-affiliation), not an arrow. If an `org_event` (acquisition/rename/spin-off) between
A and B explains the change, emit `basis=acquisition_continuation` and no person transition (LIN schema invariant:
"Acquisition ownership alone never creates a person transition").

---

## B. Overlap measurement

### B.1 People

Keys: NFKD accent strip, lowercase, punctuation removed, suffixes (Jr, III) dropped. "Exact" = full normalized
name; abbreviated names (first token one letter) excluded from EO/PK exact keys. "Shared org" = at least one org of
the person in each dataset matches after normalization (identity support, not proof).

| Dataset | Persons | Distinct full-name keys | ORCID |
|---|---|---|---|
| LIN | 288 (+106 alias names) | 349 | 0 |
| EO | 1509 | 1423 | 374 |
| PK | no table | 1296 (+201 abbreviated strings) | 0 |
| OFC | no table | 3780 (6056 author rows) | 0 |

| Pair | Exact full-name keys | of which shared org | Notes |
|---|---|---|---|
| LIN-EO | 28 | 25 | 14 of 28 carry an ORCID in EO (LIN has none) |
| LIN-PK | 6 | 6 | David Lazovsky, Phil Winterbottom (Celestial AI); Joris Van Campenhout (imec); Lau Boon Long, Ming Chinq Jong, Surya Bhattacharya (A*STAR IME) |
| LIN-OFC | 46 | 35 | first+last token (middle dropped): 48 |
| EO-PK | 16 | 12 | e.g. Joris Van Campenhout, Peter Verheyen, Michael R. Watts, Ken Giewont, Yusheng Bian |
| EO-OFC | 521 | 444 | includes the 54 EO papers that are OFC 2026 papers; excluding those, 246 EO person_ids appear in other OFC presentations |
| PK-OFC | 42 | 27 | token-sorted (family-name-first): 45 |

- LIN people found in any of EO/PK/OFC by exact name: 56 / 288.
- Fuzzy initial+last key (e.g. "j bowers"): LIN-EO 66 keys hitting 113 EO ids (collision-heavy; unusable without discriminators). EO-PK 135 keys.
- Missed by exact match, found by first+last name only: 2 LIN people (name-only matches; identities not asserted here).
- LIN-EO exact matches with no shared org: 3 (org naming differences: lab-level LIN nodes vs university-level EO orgs).
- Common-name exact matches needing discriminators: 6 LIN people match EO slugs by name only.

### B.2 Organizations (normalized name, legal suffixes dropped; exact key only)

| Pair | Shared keys |
|---|---|
| LIN-EO | 30 (e.g. AMF, Broadcom, Caltech, Ciena, Coherent, Enosemi, Huawei, imec, Infinera, Intel, KIT, Lightmatter, Meta, Nexus Photonics, Nokia Bell Labs, NVIDIA, Polariton, Stanford, UCSB) |
| LIN-PK | 11 (A*STAR, A*STAR IME, CEA-Leti, Celestial AI, GlobalFoundries, imec, Intel, Lightmatter, Marvell Technology, Samsung Electronics, TU Berlin) |
| EO-PK | 21 |
| all three | 5: GlobalFoundries, imec, Intel, Lightmatter, Technische Universitat Berlin |
| OFC (657 normalized keys) vs EO / PK / LIN | 109 / 32 / 44 exact |

Alias work visible in the data (needs a curated `org_alias` table, not string similarity):
- OFC imec: "Interuniversitair Micro-Elektronica Centrum" (55 rows), "Interuniversity Microelectronics Center" (34).
- OFC: "Huazhong University of Science and Technology" (93) vs "Huazhong Univ of Science and Technology" (83); "Pengcheng Laboratory" (74) vs "Peng Cheng Laboratory" (61); "Nokia Bell Labs" (140), "Nokia Corporation" (52), "Nokia" (36); "Fraunhofer HHI" (38) vs the German long form (56); NICT also appears as the romanized Japanese legal name ("Kokuritsu Kenkyu Kaihatsu Hojin Joho Tsushin Kenkyu Kiko", record M1C.2).
- LIN-EO near misses: "CREOL, University of Central Florida" vs "University of Central Florida"; A*STAR IME name order variants; LIN `org_ligent` vs EO "Ligent Technologies, Inc." (identity unverified).
- String similarity is unsafe: false near-matches seen include Calient/Ligent, Korea/Kobe University, Anello/Analog Photonics.
- Identifier coverage: ROR only in EO (170/284). Wikidata QIDs are recoverable from `org_sites.source_ref` where `source=wikidata`.

### B.3 OFC 2026 format notes

- `authors_text`: `"Name, Affiliation / Name, Affiliation / ..."`. Affiliations contain commas ("NTT, Inc."), so split on `" / "` and take the first comma only. `authors_json` is already parsed: 830/830 records parse, 0 count mismatches with `authors_text`, 1 empty affiliation.
- One affiliation per author; no unit, no city; `presenter_affiliation` and `presenter_country` empty on all records. Spellings are inconsistent (see B.2).
- OFCT md headers (677 files, all codes present in the metadata): 443 use `<sup>` markers; others use inline digits ("Sludds1"), parentheses "(1)", or a single shared affiliation. Per-author multi-affiliation is parseable, but marker styles vary too much for a regex; use the EO DevLog-018 extraction + audit flow (LLM batches, fresh audit). Headers contain author e-mails: do not store them.

---

## C. Move detection demo (EO + PK + OFC)

### C.1 Method

- Observations: EO 2880 rows, joined to `paper_authors.person_id`; PK 1996 rows, attached to an EO person_id when the full non-abbreviated name matches exactly one EO person, otherwise to a name key; OFC 5523 rows (from 6056, minus rows from the 54 OFC presentations that already appear in EO as `10.1364/ofc.2026.*`, to avoid same-paper double counting).
- Orgs collapsed to root `parent_org` within each atlas, then normalized. Explicit alias groups applied (imec variants, Ghent University/Universiteit Gent/IDLab, EPFL long form, AIST, Fraunhofer-Gesellschaft/IZM, Peng Cheng variants, A*STAR long form). Shared distinctive-token rule for spelling variants.
- Dates: EO `published_on` (day) else `year`; PK `year`; OFC session date.
- Class: `ind` = company, research_institute, national/government lab, foundry, facility, consortium, or an OFC string not classed as a university (keyword heuristic); `uni` otherwise.
- Identity support: `orcid` (EO), `coauth=n` (shared coauthors between the from- and to-papers), `name_only`. `name_only` + common CJK surname = collision risk.

### C.2 Funnel

| Step | Count |
|---|---|
| Person keys | 6167 (EO-linked 1495; source mix: EO only 1235, EO+OFC 242, EO+PK 12, EO+PK+OFC 4, PK only 1452, PK+OFC 29, OFC only 3193) |
| Persons with >= 2 org groups | 457 |
| Strictly ordered, never co-listed transitions | 163 (137 persons) |
| After >= 90 d / later-year gap (removes same-week OFC pairs) | 92 |
| of which org-event continuation (C.4) | 17 |
| candidate moves | 75 (62 persons): uni->ind 31, uni->uni 20, ind->ind 17, ind->uni 7 |
| identity: orcid / shared coauthor / name only | 22 / 13 / 40 (29 name-only with common surname = collision risk) |
| by source pair | EO->EO 30, EO->OFC 26, PK->OFC 7, PK->PK 6, PK->EO 3, EO->PK 2, OFC->EO 1 (EO+PK only: 41) |

### C.3 Candidate transitions (redacted)

Redacted 2026-10-20 (P0 audit, DevLog-001): the named table of the top 30 candidate transitions, the list of four
ORCID-backed uni->uni candidates and the list of 29 collision-risk name-only candidates are kept only in a local,
git-ignored copy. They are derived (grade X) research-queue signals about living people, partly name-only identity
matches, and per D10 / E.4 are not published. Aggregates (from C.2): 75 candidate moves in 62 persons; identity
support ORCID 22, shared coauthor 13, name only 40 (29 of them common-surname collision risks); classes uni->ind 31,
uni->uni 20, ind->ind 17, ind->uni 7. Every signal is a pair of dated publication/conference affiliation observations,
never an employment interval.

### C.4 Org-event continuations and artifacts (not person moves)

| From -> To | People | Explained by |
|---|---|---|
| Xperi (2022) -> Adeia (2023) | 9 (PK ectc51906.2022.00031 -> ectc51909.2023.00023) | spin-off 2022, PK `config/org_aliases.yaml` L4 |
| Showa Denko Materials -> Resonac | 2 | rename 2023, PK `config/org_aliases.yaml` L4 |
| Tokyo Institute of Technology -> Institute of Science Tokyo | 1 | merger 2024, PK `config/org_aliases.yaml` L5 |
| Enosemi (EO johnson2025, 2025-09-29) -> AMD (OFC M1E.2) | 2 | LIN `event_acquisition_enosemi_amd` (announced 2025-05-28) |
| Celestial AI (PK ectc51687.2025.00062) -> Marvell | 3 (PK ectc51846.2026.00346; OFC W3C.5) | LIN `event_acquisition_celestial_ai_marvell` (effective 2026-02-02) |

Artifact classes found and handled:
1. Alias spelling (21 transitions before alias groups, e.g. imec -> "Interuniversity Microelectronics Center" for Joris Van Campenhout, Peter Verheyen, Filippo Ferraro; EPFL long form; AIST).
2. Same-week OFC pairs (61 OFC->OFC pairs, all removed by the 90-day gap).
3. Co-affiliation dropped by OFC metadata: PK ectc51909.2023.00009 prints "CEA-Leti, Univ Grenoble Alpes" (Leopold Virot row note); OFC keeps one affiliation per author, so CEA -> Univ Grenoble Alpes (row 29) is probably the same dual affiliation. Fix: OFCT header extraction.
4. Parent/unit, consortium membership (Fraunhofer-Gesellschaft vs IZM; JOINT2).
5. Additional affiliations (`[add.]`) are concurrent appointments more often than moves.

---

## D. Intel silicon photonics coverage

### D.1 What LIN has

- Org nodes: `org_intel` (Intel Corporation, company) and `org_intel_silicon_photonics` (Intel Silicon Photonics Solutions Group, business_unit, parent `org_intel`, alias "Intel Photonics Technology Lab"; one time-evolving node per its `notes`).
- 27 people with an edge to either node; 27 Intel edges: technical_leadership 16, employment 10, publication_affiliation 1; grades B 19, A 8 (most B edges come from `src_optica_intel_siph_team`, Optica team roster, B per policy).
- Dated Intel edges: 4 of 27 (`edge_hai_ding_intel_employment` 2003-2008; `edge_osa_chou_shung_mok_intel_employment` 1977-1980; `edge_juthika_basak_intel_publication` 2007; `edge_mario_paniccia_intel_siph` end 2016). Chronology for the rest is unknown.

| Person (LIN id) | Non-Intel edges in LIN (edge type, date if any, grade) |
|---|---|
| Andrew Alduino (`person_andrew_alduino`) | Meta Platforms employment (A) |
| Brian Koch (`person_brian_koch`) | Aurrion employment, Juniper employment, Quintessent founder, UCSB Bowers group research_training (all A) |
| Cas Wierzynski | Rockley Photonics technical_leadership (A) |
| Ruolin Li (`person_china_li_ruolin`) | Inxun founder (B) |
| Hui Nie (`person_china_nie_hui`) | NVISION Technology founder (A); Lucent Bell Labs employment (B) |
| Hai Ding | InnoLight technical_leadership from 2008 (A) |
| (1 person) | common-name exact match to EO/OFC authors at a company not in the LIN record | identity unverified; not used |
| Juthika Basak | Nokia, AMD, Finisar technical_leadership (A) |
| Kevin Sullivan | ANELLO Photonics executive_role (A) |
| Marcus Yang | SiPhi Tech founder 2025 (A) |
| Mario Paniccia | ANELLO Photonics founder 2019-11 (A) |
| (1 person) | first+last-name-only match to an OFC author | not used until identity is confirmed |
| Osa Chou-Shung Mok | InnoLight founder 2008; Pine Photonics founder 2000; Uniwave founder 2004-2008 (A) |
| Vikram Sadagopan | Luxtera employment; Xscape Photonics executive_role from 2025-04-18 (A) |
| Vivek Raghunathan | Rockley, Broadcom technical_leadership; Xscape founder (A) |
| Yoel Chetrit | DustPhotonics founder (A) |
| No non-Intel edge (11) | Ansheng Liu, Assia Barkai, David Nelson, Hai-Feng Liu, Haisheng Rong, John Heck, Ling Liao, Olufemi I. Dosunmu, Rami Cohen, Richard Jones, Yimin Kang |

### D.2 LIN Intel people in the atlases / OFC

| Person | Local observation | Use |
|---|---|---|
| Haisheng Rong | EO hsu2024 (Intel Corporation, 2023-08-30); OFC Tu3C.2 (Intel Corporation, 2026-03-17) | dated `active_on` Intel observations; still at Intel at both dates (no move) |
| Andrew Alduino | OFC M4B.6 (Meta Platforms Inc, 2026-03-16) | dated corroboration of `edge_andrew_alduino_meta` |
| (1 person) | first+last-name-only match to an OFC author | not used until identity is confirmed |
| (1 person) | common-name exact match to EO/OFC authors at a company not in the LIN record | identity unverified; not used |
| other 23 | not found by exact or first+last name | |

### D.3 Intel-affiliated authors in local data that LIN lacks

- EO: Ranjeet Kumar (hsu2024), Wonho Lee (lee2026, unit "PHY research lab, Intel lab").
- OFC: Tu3C.2 "Ring Resonator-Based Dynamic Controller for Precise Wavelength Separation of a DWDM Laser Source": Cooper Levy, Dan Lake, Duanni Huang, Jahnavi Sharma, James Jaussi, Prathapa Puttaswamy, Ranjeet Kumar, Zhe Xuan (+ Haisheng Rong); M4B.1 "Integrated Optical I/O Chiplets for Bandwidth Scaling in AI Infrastructure": Thomas Liljeberg; Th2A.5: Ahmadreza Farsaei.
- PK: 266 Intel rows, 241 distinct author strings, 21 papers; units are packaging/logic (Technology Development, Logic Technology Development, Substrate Packaging Technology Development, Components Research, Assembly Test Technology Development); none photonic. 0 in LIN. Relevant to an Intel-wide diaspora view, not SiPh.

### D.4 Gaps visible from local data

1. 11/27 Intel people have no downstream or upstream edge (D.1).
2. 23/27 Intel edges undated: the strict-flow view cannot order them (`PROGRESS.md` audit: 240 of 296 person/display-org pairs lack conclusive order).
3. Upstream (where Intel people came from) is nearly absent: one research_training edge (Koch, UCSB Bowers group). Luxtera (Sadagopan) and Lucent Bell Labs (Nie) edges are undated, so direction is unknown. `source_policy.md` requires both directions around hubs.
4. Seeds still not canonical: Mario Fiorentino, Robert Blum, Michael Davenport, Guo Peng (`people_seed.yaml` L8, L11, L16, L21). Leads not ingested: 2 (one LinkedIn-sourced grade C lead, one OFC-program lead; `research/intel_siph_lineage_initial.md`, gap 5); not restated here.
5. The current Intel SiPh cohort (2023-2026 authors in D.3, 10 names besides Rong) is absent: LIN is diaspora-centric and lacks the present team, so it cannot tell who later leaves.
6. `timeline_research` is populated for 0/288 people. The Intel ego-network acceptance test (`VISUALIZATION_DESIGN.md` "Intel acceptance test") is not implemented (`PROGRESS.md` next actions 3-4).
7. Two Intel org nodes with no dated era split (PTL vs Solutions Group). Intel naming differs across datasets: "Intel Corporation" in EO (ROR `https://ror.org/01ek73717`), "Intel" in PK (no ROR), `org_intel` in LIN (no ROR). These are the first registry crosswalk test case.

---

## E. Recommended plan

### E.1 Data flow and canonical ownership

| Data | Canonical home | Consumers |
|---|---|---|
| Per-paper author x affiliation rows | each atlas (`author_affiliations.csv`), unchanged | people atlas reads them as observations |
| Org registry (`org_id`, aliases, parent, ROR, QID, type), `org_event` | people atlas (new; seeded from LIN orgs + events, EO/PK orgs, PK `org_aliases.yaml`) | atlases map `org_name -> org_id` with a crosswalk file in the people atlas; no atlas edit needed at first |
| Person registry + `person_xref` | people atlas (seeded from LIN people + EO `people.csv`) | atlases keep their own `person_id`; the crosswalk maps them |
| Curated career claims (intervals, roles, founder, events) | LIN canonical YAML (promoted into the people atlas, or the people atlas *is* LIN v0.3) | |
| Conference snapshots (OFC) | people atlas source adapter (metadata now; OFCT header extraction later) | |
| Derived spans, transitions, flows | generated only, never hand-edited | visualizations |

Build: `adapters/{eo,pk,ofc,lin}.py` -> `observations.jsonl` -> `derive.py` (spans, transitions, flows) ->
`validate.py` (orphan ids, endpoint types, date order, grade/status compatibility, aggregate reproducibility, as
in LIN validation gates) -> views. Resumable, dry-run, timestamped logs.

### E.2 Identifiers

- `person_<slug>` and `org_<slug>`, immutable after merge; collisions get `_2`. Do not use ORCID as the primary key (the EO `person_id` changes slug -> ORCID when one is found); store ORCID in `person.orcid` and `person_xref`.
- Merge rules (EO DevLog-020 #2 + LIN `source_policy.md`): ORCID match; or exact name + shared org; or compatible name + shared org + shared coauthor. Never merge on romanized name alone (LIN Chinese-name rule); common CJK names need two discriminators.
- Orgs: ROR first (EO has 170), Wikidata QID from `org_sites`, then the own preferred name. Time-aware entities stay distinct (Bell Labs eras, Finisar / II-VI / Coherent; LIN dedup rules). Renames, spin-offs and acquisitions are `org_event` rows, not aliases.
- Printed org text is always kept (`printed_org`) next to `org_id`.

### E.3 Evidence grading (reuse LIN A-D, X)

- Paper-printed affiliation A; Crossref affiliation A (flagged); conference-organizer metadata (OFC `authors_json`) B; LinkedIn/Crunchbase C; single PR D; derived transitions X unless backed by `present_address` or a dated bio.
- Rename EO `papers.repro_grade` in docs/UI to avoid confusion with evidence grade.
- Default view: A/B only; C in a visibly separate optional layer; D/X never in flow views (LIN `source_policy.md`).

### E.4 Privacy rules

- Public professional sources only. No LinkedIn scraping or capture without Wentao's explicit opt-in. LIN `source_policy.md` v0.2 currently makes LinkedIn a *required* discovery source (grade C): needs a decision (Q2).
- Grade C stays out of the default view; no contact data (OFCT headers contain e-mails: strip them), no non-professional data.
- Name-only identity is never shown as a person transition; collision-risk rows stay in a review queue.
- Living people: show "observed affiliation on date" wording, never "worked at X from-to" unless an A/B interval exists.

### E.5 Visualizations (data only, dark, sharp corners)

1. Org exchange network: orgs as nodes, transitions as edges, styled by `direction_status` (confirmed / unknown / org-event continuation) and grade; ego mode per org (Intel acceptance test from `VISUALIZATION_DESIGN.md`).
2. Person timeline: swimlane per org; dots = dated publication/conference observations, bars = A/B intervals, dashed = C, diamonds = org events; hover lists paper ids and locators.
3. Org-to-org flow over time: transitions binned by year (stacked bars or alluvial per period), filter by class (uni->ind, ind->ind) and technology.
4. Geography: reuse `org_sites` coordinates; arcs between sites for transitions; time slider.
5. Coverage panel: per hub, people with no upstream/downstream, undated edge fraction.

### E.6 Tranche order

| # | Tranche | Output | Acceptance |
|---|---|---|---|
| T0 | Decisions (E.7) | DevLog decision table | answered |
| T1 | Org registry: crosswalk LIN 172 + EO 284 + PK 144 + top OFC strings; `org_alias`; `org_event` from LIN events (23) + PK alias comments (3) | `organizations.csv`, `org_aliases.csv`, `org_events.csv` | every EO/PK org_name and >= 90% of OFC author rows map to an org_id |
| T2 | Person registry: EO 1509 base; PK name dedup (PK has no people table; port EO `scripts/build_people.py`); OFC names; LIN 288 | `people.csv`, `person_xref.csv`, review queue | 0 merges on name alone for common names; audit sample |
| T3 | Observation adapters + derive + validator | `observations.jsonl`, `transitions.csv` | reproduces C.2 numbers with the new registry |
| T4 | OFCT header extraction (677 papers, LLM batches + fresh audit as EO DevLog-018) | per-author multi-affiliation OFC rows | removes single-affiliation artifacts (C.4 item 3) |
| T5 | Intel pilot: Intel ego view + timelines; add current Intel cohort (D.3) as observations; research queue for the 11 Intel people with no non-Intel edge and the 4 seed-only people (A/B sources only) | Intel views | `VISUALIZATION_DESIGN.md` Intel acceptance test passes |
| T6 | Visualizations E.5 | app pages | screenshots, no console errors |
| T7 | Other hubs (Bell Labs, imec/Ghent, Luxtera, UCSB) and more conference years (OFC/ECOC/CLEO metadata) | | |

### E.7 Questions for Wentao

1. Canonical home: promote LIN (`PlayGround/20260823_photonics_lineage`) into a new standalone repo that owns the org/person registry, or keep it in PlayGround?
2. LinkedIn: LIN `source_policy.md` v0.2 treats LinkedIn as a required C-grade discovery source. Keep it (with your opt-in), or remove it so the atlas stays on papers, filings, and official bios?
3. Publication: will the person-level atlas be public? This sets the default view (A/B only) and whether name-only candidates are shown at all.
4. OFC metadata affiliations: accept them as grade B snapshots now, or wait for T4 header extraction?

---

## Limits of this assessment

- Name matching only (no ORCID outside EO); counts are lower bounds for true overlap and include some false exact matches for common names.
- Org normalization in C used heuristic token rules plus a small explicit alias list. T1 replaces both with a curated registry.
- PK has year precision only; EO 59/233 papers lack `published_on`; ordering at year precision needs a full-year gap.
- OFC org class uses a keyword heuristic for unmatched strings.
- No web research was done. Every gap in D.4 is visible from local files only.
