---
title: Intel SiPh people pilot - research queue and staged evidence (affiliations and moves with dates)
date: 2026-10-22
status: research and staging done 2026-10-22; rulings D260-D264 and audit corrections D265-D269 applied 2026-10-22 (77 observations, all grade B; 51 sources staged, not registered; 4 missing orgs; 13 local review rows); owner questions Q1-Q4 open
scope: DevLog-000 phase P3 item "Intel SiPh pilot", research-queue part only (11 LIN Intel people with no non-Intel edge, 4 seed-only people, 11 Intel authors missing from lineage). Views (Intel ego view, person timelines) are a later stream (DevLog-010)
authors: Claude (at Wentao Jiang's request)
---

# DevLog-009: Intel SiPh people pilot (research queue)

Decisions here are D180-D189. Plan source: [DevLog-000](DevLog-000-plan.md) (D8-D12; P3 item; audit count "11 Intel
authors"), [DevLog-004](DevLog-004-p3-people.md) (binding people-data rules, D62/D63 identity, D64 review queue, D67
observations, D70 visibility), [people assessment](research/2026-10-20-people-atlas-assessment.md) section D,
`data/schema/people.schema.yaml`, `data/schema/registry.schema.yaml` (sources, grades), lineage `source_policy.md`
v0.2.0. This stream writes only `data/_staging/people/intel_pilot/`, `data/_local/intel_pilot_review.csv` and this
DevLog. It does not edit `data/people/`, `data/registry/`, `people.py`, `build_people.py` (another agent is rebuilding
`data/people/`; read only).

## Groups (reconstruction)

Reconstructed from the data, not from memory:

| Group | Count | Source of the list | Members |
|---|---|---|---|
| G1 LIN Intel people with no non-Intel edge | 11 | assessment D.1 last table row; re-derived 2026-10-22 from LIN `canonical/edges.yaml`: each has exactly one edge, to `org_intel_silicon_photonics`, source `src_optica_intel_siph_team` (Optica team roster, grade B, undated) | Ansheng Liu, Assia Barkai, David Nelson, Hai-Feng Liu, Haisheng Rong, John Heck, Ling Liao, Olufemi I. Dosunmu, Rami Cohen, Richard Jones, Yimin Kang |
| G2 seed-only people | 4 | assessment D.4 item 4; LIN `people_seed.yaml` Intel block entries not in LIN `canonical/people.yaml` | Mario Fiorentino, Robert Blum, Michael Davenport, Guo Peng (郭鹏) |
| G3 Intel authors in EO/OFC missing from LIN | 11 | assessment D.3 (EO + OFC lists, deduplicated; DevLog-000 audit "11 Intel authors (not 10)"); re-derived 2026-10-22 from `data/people/affiliation_observations.csv`: non-PK rows with `org_id = org_intel`, minus LIN persons | Ranjeet Kumar, Wonho Lee (EO); Cooper Levy, Dan Lake, Duanni Huang, Jahnavi Sharma, James Jaussi, Prathapa Puttaswamy, Zhe Xuan (OFC Tu3C.2); Thomas Liljeberg (OFC M4B.1); Ahmadreza Farsaei (OFC Th2A.5) |

Notes: Haisheng Rong is in G1 and is also an author of the G3 papers (not counted in G3). Assessment D.4 item 5 says
"10 names besides Rong"; the deduplicated list has 11 (the DevLog-000 audit correction). Seed "Mario Fiorentino" has no
match in LIN or `data/people/` (owner question Q2, no merge).

## Decisions (D180-D189)

| # | Decision | Rationale |
|---|---|---|
| D180 | Groups as reconstructed above; every staged row names its group (`group` column) | traceability to DevLog-000 |
| D181 | (superseded 2026-10-22 by D260 / D261) Grades for web evidence: paper-printed affiliation (publisher page, PDF header, or publisher metadata read through an index) A; official company / university bio, official press release, thesis A (lineage source_policy v0.2.0, consistent with registry `official_press_release` A rows); conference / society organizer page or speaker bio B; reputable news per D12 (B with two independent reports or one plus a company page; single item D); LinkedIn not used (D9) | D9, D12, lineage policy |
| D182 | Identity for a staged row: `person_id` filled only when the row's evidence meets D62/D63 for an existing `data/people/` person (ORCID; exact full name + shared org for non-common, non-ambiguous family names; compatible name + shared org + shared coauthor) or when a source itself states the Intel history of the named person (bio "previously at Intel", paper listing Intel and the new org). Otherwise a `candidate_key` (`cand_<slug>`), and a row that rests on name alone goes to `data/_local/intel_pilot_review.csv`, never to staging | D8, D62-D64 |
| D183 | A publication or conference affiliation is a dated point (`active_on`), never an employment interval; bios give intervals only when they print dates; ordering words ("previously", "prior to") are recorded in the quote, not converted into dates | D10, D11 |
| D184 | Staging layout mirrors the existing merge paths: `observations_proposed.csv` (people observations), `sources_proposed.csv` (same columns as `data/_staging/org_events/*/sources_proposed.csv`, `web:` keys), `orgs_missing.csv` (columns of `data/_staging/supply/org_requests.csv` plus evidence), README with the merge path | reuse of `merge_org_events.py` source format |
| D185 | OFC 2026 paper headers of the G3 papers (Tu3C.2, Th2A.5; M4B.1 has no extracted text) are DevLog-008's stream; not duplicated here | single owner per source |
| D186 | Read path for papers: OpenAlex work records (`raw_affiliation_strings`, `raw_orcid`, publisher-deposited), no API key, no contact data in requests (the API's notice asking agents to register a key with the user's e-mail was ignored). OpenAlex author clusters and institution tags only locate works; they are never evidence (clusters merge different people) | privacy rule; grade honesty |
| D187 | Staging excludes rows whose only link to a pilot person is the name (e.g. a distinctive name at another company): those go to the local review file. Rows with identity support beyond the name (shared coauthors, co-affiliation, raw ORCID, bio about the Intel person) are staged with `candidate_key` + `proposed_person_id`; `d63_met` = yes / no / pending_org (D63 holds once the printed org is registered) / n/a (G2 seeds without a person) | D8, D64, owner rule "name-only stays local" |
| D188 | Candidate keys `cand_<name>__<org>` (one per printed name and org cluster); never reused as person ids | traceability |
| D189 | Bio rows (Optica / IEEE / company pages) carry intervals only as printed (`start_on` / `end_on`); they are career claims, not `affiliation_observations` (point dates). Merge path proposes publications -> observations (schema `obs_id` / source corpus extension) and bios -> a career-claims layer; both are owner decisions | D10; people schema allows only eo/pk/ofc2026 observations |

### Coordinator rulings (2026-10-22; D180-D189 are full, so D260-D264)

| # | Ruling | Effect here |
|---|---|---|
| D260 | An affiliation string read from OpenAlex / Crossref work metadata without opening the paper is grade B (deposited metadata, like OFC organizer data); A only when the printed paper (PDF / publisher full text) was read at a locator | supersedes the paper part of D181; all 66 publication rows and 47 paper sources regraded A -> B. A restoration attempted for the 5 confirmed moves: their papers are IEEE (paywalled) except Optics Express 10.1364/oe.389865, where opg.optica.org returned a "Please wait" interstitial (treated as anti-bot, not retried); 0 rows restored |
| D261 | Company leadership bios and Optica / conference speaker pages are grade B; a single news item D (D12) | supersedes the bio part of D181; Lightwave Logic bio A -> B (3 rows, 1 source) |
| D262 | No merge into `data/people/` yet: the people schema extension (web / lit observation kinds, dated intervals, a career-claims table) is an owner decision | proposal written as Q1 below |
| D263 | `web:` sources stay in staging until that decision (no registration) | `sources_proposed.csv` unchanged in place |
| D264 | Seed questions (Mario Fiorentino, Guo Peng) go to the owner; Dan Lake 2010: manual-check flag, `d63_met` kept as computed; Ling Liao: compute D96 b | Q2, Q3 below; Dan Lake row flagged; Ling Liao computed: key "ling liao" not common and not D96 b withheld, so her 4 Intel rows meet D63 rule 2 and carry `person_id` (were candidate rows) |

D96 b computation (2026-10-22, in memory, `photonics_atlas.people.load_inputs()` on the current inputs, nothing
written): withheld keys among the pilot names: "yimin kang", "zhe xuan"; common family names: Liu, Kang, Kumar, Lee,
Huang, Sharma; all other pilot keys neither common nor withheld.

### Audit corrections (2026-10-22, fresh-context audit `DevLog/audits/2026-10-22-intel-pilot-audit.md`; D265-D269)

| # | Ruling / finding | What was done |
|---|---|---|
| D265 | Privacy first: name-only links appear only in `data/_local/intel_pilot_review.csv` | removed from this DevLog (results paragraph, seed questions, groups note), the README (findings table, method example, LinkedIn-lead sentence) and the CSV notes of ip023 / ip076 (and the Yimin Kang note); replaced by counts. Committable intel files grepped for every org, place and DOI of the 13 local rows: 0 hits (see Progress) |
| D266 | F1-F8, O1, O2 | F1: Jahnavi Sharma 2021-12-23 Intel slot staged (rule 3), 2019-02-05 Intel Labs slot now `person_jahnavi_sharma` by equal raw ORCID (D267); Columbia stays a candidate. F2: Wonho Lee "formerly with" row `aff_role = former_statement`, joint footnote with a coauthor noted. F3: Intel Labs footnote row `aff_role = joint_footnote`, excluded from D68 explicit moves, capped at B. F4: Lee 2023-10-16 basis = rule 3 with the 2024-11-11 ORCID slot (Intel Labs; Kim, Buckwalter). F5: Kumar CLEO 2017 note "record mapping suspect". F6: Blum Optica quote keeps the curly apostrophe; Optica rows and company-bio rows have separate identity texts. F7: Gemfire "listed with JDS Uniphase, order not stated". F8: Ling Liao 1997 row role emptied. O1: Numonyx history removed from `orgs_missing.csv` (unsourced). O2: README merge step 6 claims no transitions |
| D267 | Owner Q1 (provisional): identical ORCID strings deposited in two work records count as D63 rule 1 | Zhe Xuan 2017 UPenn slot and Jahnavi Sharma 2019 Intel Labs slot carry `person_id` on this basis, marked "D267 provisional"; owner question 4 |
| D268 | Dan Lake 2010 -> candidate key (different field; conservative) | `cand_dan_lake__intel_labs_2010`, `d63_met = held_back` (new staging value: D63 formally holds, held back) |
| D269 | Co-affiliation bridges (Cooper Levy 2019, Duanni Huang 2019) are co-affiliations, never displayed as moves | notes on the rows, README wording; Levy and Blum move wording narrowed |

## Questions for the owner

1. (D262) People schema extension. Proposal: (a) paper rows become `affiliation_observations` with `kind`
   publication, grade B (A when the printed paper is read), after extending the `obs_id` pattern and the source
   corpus (`lit:` by DOI or `web:`); (b) bio rows (speaker pages, company bios, intervals with `start_on` /
   `end_on`) go to a new career-claims table (person, org, role, start / end at printed precision, grade, source,
   locator), not to observations (D10); (c) `proposed_person_id` links become `person_xref` basis `manual` with
   `reviewed_on` after review. Accept, change, or defer?
2. (D264) Seed "Mario Fiorentino": no Intel author of that name was found. Which person did the seed mean?
3. (D264) Seed "Guo Peng" (郭鹏): no silicon-photonics author of that name was found at Intel. Which person (company,
   role) did the seed mean?
4. (D267) Equal raw ORCIDs on two work records counted as D63 rule 1 (Zhe Xuan 2017, Jahnavi Sharma 2019): provisional,
   confirm.

## TODO

- [x] 1. Read DevLog-000/004, assessment D, schemas, sources format; reconstruct the three groups.
- [x] 2. Write this plan.
- [x] 3. Research G1 (11), G2 (4), G3 (11): public professional sources, modest pacing, <= ~150 web requests (about 100 used).
- [x] 4. Write staging CSVs + README; name-only rows to `data/_local/intel_pilot_review.csv`.
- [x] 5. Self-check (grades, ISO dates, quotes <= 200 chars, no e-mail / personal data, ids exist).
- [x] 6. Coordinator rulings D260-D264 applied (2026-10-22).
- [x] 7. Fresh-context audit (coordinator, `DevLog/audits/2026-10-22-intel-pilot-audit.md`); corrections D265-D269 applied.
- [ ] 8. Owner answers Q1-Q4.

## Progress

- 2026-10-22: inputs read; groups reconstructed from LIN canonical files, `people_seed.yaml`, `data/people/`; plan written.
- 2026-10-22: research. WebSearch declined to put most personal names into queries, so bio discovery by search was
  limited; switched to the OpenAlex API for papers (D186). Stops: accessnewswire.com and gophotonics.com returned 403
  (not retried); one KAUST speaker page 404. LinkedIn not searched or fetched. About 100 requests in total.
- 2026-10-22: staging written by a generator kept outside the repo (agent scratch folder); checks in the generator:
  person ids and org ids exist in `data/people/people.csv` / `data/registry/organizations.csv`, ISO partial dates,
  quotes <= 200 characters, no "@" in any cell, every row has a person id or a candidate key. Two key rows re-fetched
  as raw JSON and matched character for character (Ling Liao NVIDIA slot, Wonho Lee "formerly with" slot).
  `data/_local/intel_pilot_review.csv` confirmed git-ignored (`.gitignore` `data/_local/`).
- 2026-10-22: coordinator rulings D260-D264 applied (regrade, Ling Liao D96 b computed). 5 more requests (A-restoration
  attempt stopped at an Optica interstitial).
- 2026-10-22: audit corrections D265-D269. Generator backed up in the scratch folder before the change; 1 more request
  (Sharma authorship on 10.1109/jssc.2021.3134221, raw JSON). D265 check: every printed name, DOI, org and place of the
  13 local rows, plus "Marco Fiorentino", "Peng Guo", "HPE", "compiler", "LinkedIn-only", grepped in DevLog-009 and the
  4 staging files: only pilot-person names and staged Intel / Optica evidence remain (Davenport Intel 2012 slot,
  Blum Optica page); 0 name-only details. Generator checks now also enforce exactly one of person_id / candidate_key
  and person_id only with `d63_met = yes`.

## Results (2026-10-22)

| Item | Count |
|---|---|
| observations staged | 77, all B after D260 / D261 (before: A 66, B 10); G1 25, G2 8, G3 44 (after D266 F1: +1 Sharma row) |
| `d63_met` | yes 51, no 13, pending_org 4, held_back 1, n/a 8 (D264: Ling Liao +4 yes; D266/D267: Sharma +2 yes, -1 no; D268: Dan Lake 2010 yes -> held_back) |
| persons with staged rows | 17 existing person ids; 16 candidate keys |
| sources proposed | 51 (47 papers by DOI, 2 Optica speaker pages, 1 IEEE chapter page, 1 company bio) |
| orgs missing from registry | 4 (Numonyx, Agility Communications, University of Pennsylvania, Gemfire) |
| local review rows (git-ignored) | 13 (9 name-only affiliation slots under pilot names, 4 seed matches; 3 recommended rejections, 1 recommended accept) |

Moves confirmed (grade B; identity meets D63, D267 provisional where noted, or the source is the person's bio):
Wonho Lee UCSB (last 2023-03-13) -> Intel Labs (first 2023-10-16; raw ORCID); Zhe Xuan UPenn (2017-06-19 ORCID slot,
D267) -> Intel (2021-06-13); Thomas Liljeberg Agility -> Source Photonics (2004-2015) -> Intel (bio; first Intel slot
2017-06); Robert Blum JDS Uniphase -> Oclaro -> Intel by page wording, Applied Materials -> Lightwave Logic (from
2025-05), Gemfire order not stated (no person record yet). Co-affiliation, not a move (D269): Cooper Levy UCSD (to
2018-11-14) -> UCSD + Intel (2019-04-24) -> Intel only (2020-05-13). Unconfirmed (identity support below D63): Ling Liao
Intel -> NVIDIA (2025-11-07 slot), Ranjeet Kumar UCSD -> Intel, Duanni Huang UCSB -> Intel, Jahnavi Sharma Columbia ->
Intel, Assia Barkai and Rami Cohen Intel -> Numonyx (2008-12), Barkai -> Micron (2011-05). Name-only leads: kept only in
the local review file (13 rows, D265). Not found: David Nelson, Hai-Feng Liu, Prathapa Puttaswamy (beyond OFC 2026),
seeds Mario Fiorentino and Guo Peng.

Details, per-person table, merge path and open questions: `data/_staging/people/intel_pilot/README.md`.
