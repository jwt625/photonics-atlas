# Intel SiPh pilot: staged evidence (DevLog-009)

Staging only. Nothing here is merged into `data/people/` or `data/registry/` (D262, D263). Research date 2026-10-22.
Decisions D180-D189 and D260-D269 in [DevLog-009](../../../../DevLog/DevLog-009-intel-siph-pilot.md); audit in
`DevLog/audits/2026-10-22-intel-pilot-audit.md`.

## Files

| File | Rows | Content |
|---|---|---|
| `observations_proposed.csv` | 77 | dated affiliation evidence per person, all grade B (D260 / D261) |
| `sources_proposed.csv` | 51 | proposed `web:` source rows (47 papers via DOI, 4 web pages), all grade B; staging only, not registered (D263); columns of `data/_staging/org_events/*/sources_proposed.csv` plus `doi` |
| `orgs_missing.csv` | 4 | printed orgs with no registry row (columns of `data/_staging/supply/org_requests.csv`) |
| `data/_local/intel_pilot_review.csv` (git-ignored) | 13 | name-only identity leads and seed matches; never committed, never shown; details are only there (D265) |

## Groups (D180)

- G1 (11): LIN Intel people whose only LIN edge is the undated Optica team-roster edge: Ansheng Liu, Assia Barkai,
  David Nelson, Hai-Feng Liu, Haisheng Rong, John Heck, Ling Liao, Olufemi I. Dosunmu, Rami Cohen, Richard Jones,
  Yimin Kang.
- G2 (4): Intel-block seeds in LIN `people_seed.yaml` with no canonical record: Mario Fiorentino, Robert Blum,
  Michael Davenport, Guo Peng.
- G3 (11): non-PK Intel authors in `data/people/affiliation_observations.csv` missing from LIN: Ranjeet Kumar,
  Wonho Lee, Cooper Levy, Dan Lake, Duanni Huang, Jahnavi Sharma, James Jaussi, Prathapa Puttaswamy, Zhe Xuan,
  Thomas Liljeberg, Ahmadreza Farsaei.

## Method

1. Read path: OpenAlex API work records (`api.openalex.org`, no key, no contact header), fields `raw_author_name`,
   `raw_affiliation_strings` and `raw_orcid` per authorship. These are deposited metadata, printed paper not read,
   so publication rows are grade B (D260; A only when the printed paper is read at a locator). OpenAlex author
   clusters and institution tags were used only to find works, never as evidence (several clusters merge different
   people).
2. Web pages: Optica speaker pages, an IEEE chapter talk page, one company leadership bio, all grade B (D261).
   LinkedIn was not used (D9). Press: one issuer release returned HTTP 403 and was not retried.
3. Quotes: exact affiliation strings or page phrases, <= 200 characters, page characters kept (e.g. curly apostrophe).
   Key rows re-fetched as raw JSON and matched character for character (10.1038/s44287-025-00223-0,
   10.1109/lssc.2023.3294172, 10.1109/jssc.2021.3134221).
4. Dates: `active_on` = publication date of the work; OpenAlex values ending in `-01-01` are reduced to the year and
   values ending in `-01` to the month (D183). Bio intervals only where the page prints years; ordering words are
   quoted in notes, list order is not read as sequence.
5. Requests: about 110 (OpenAlex API, Optica, IEEE, one company page, web searches). The web-search tool declined
   to include most personal names in queries, so bio discovery by search was limited. Grade A restoration (D260) was
   attempted for the confirmed moves: their papers are IEEE (paywalled) except Optics Express 10.1364/oe.389865, where
   opg.optica.org returned a "Please wait" interstitial (treated as anti-bot, not retried); 0 rows restored.

## Columns of `observations_proposed.csv`

`person_id` is set only when the row meets D62/D63 against the current `data/people/` person (ORCID, incl. equal raw
ORCIDs on two work records, D267 provisional; exact name + shared org for non-common, non-withheld names; compatible
name + shared org + shared coauthor), or when the source itself is the person's bio at Intel (`d63_met = yes`).
Otherwise `candidate_key` (`cand_<name>__<org>`) plus `proposed_person_id` with the identity support in
`identity_basis`; `d63_met` = `no` (support below D63), `pending_org` (D63 would hold once the printed org is
registered), `held_back` (D63 formally holds but held back, D268), `n/a` (G2: no `data/people/` person; seed link not
asserted). Rows whose only link to a pilot person is the name are not here (local review file, D182, D265).

`kind`: publication, conference_bio, society_page, company_bio. `aff_role` (publications): primary, additional, and
two staging-only values: `former_statement` (a printed "formerly with" string, not an affiliation on that date) and
`joint_footnote` (one footnote naming several orgs for several authors). Neither is a `present_address` row; both are
excluded from D68 explicit-move derivation, and any transition from them is capped at B.

## Findings by person

| Group | Person | Staged evidence (grade B, date) | Status |
|---|---|---|---|
| G1 | Richard Jones | Intel 2004-02 (Nature), 2024-03-12 | no move found |
| G1 | Haisheng Rong | Intel 2025-11-07 | no move found |
| G1 | John Heck | Intel 2023 (OFC 2023, book chapter); book contributor list prints UCSB (conflict, candidate row, no transition) | no move found |
| G1 | Assia Barkai | Intel 2005-10-18 .. 2011-05; Numonyx 2008-12 (pending org); Micron 2011-05-27 (candidate) | unconfirmed (Intel SiPh coauthors; no shared org) |
| G1 | Rami Cohen | Intel 2008-05-12; Numonyx 2008-12 (pending org) | unconfirmed |
| G1 | Olufemi I. Dosunmu | Intel 2006-10-20 .. 2024-03-12 | no move staged |
| G1 | Ling Liao | Intel: start 1997 (IEEE page), 2017-03-08, 2023, 2024-03-12 (D63 rule 2, D264); NVIDIA 2025-11-07 (candidate) | Intel -> NVIDIA unconfirmed (coauthors Rong, Jaussi; no shared org) |
| G1 | Ansheng Liu | Intel 2024-03-12 (candidate, common family name) | no move found |
| G1 | Yimin Kang | Intel 2011-04-18, 2014-03-08 (candidate; common family name, key D96 b withheld) | no move found |
| G1 | David Nelson, Hai-Feng Liu | none found | not found |
| G2 | Robert Blum | Optica page (2021-03-30): Intel SiPh director; Oclaro before Intel ("Prior to joining Intel"); JDS Uniphase before Oclaro ("Before joining Oclaro"); Gemfire listed with JDS Uniphase, order not stated. Company bio: Intel, Applied Materials (most recent before Lightwave Logic), Lightwave Logic from 2025-05 | ordered by page wording: JDS Uniphase -> Oclaro -> Intel; Applied Materials -> Lightwave Logic (2025-05); Intel -> Applied Materials order from "most recently" only; no person record |
| G2 | Michael Davenport | Intel PTL 2012-10-04 (candidate slot; seed link not asserted) | none staged |
| G2 | Mario Fiorentino, Guo Peng | none | not found (owner questions) |
| G3 | Wonho Lee | KAIST + UCSB 2021-07-02, UCSB 2023-03-13, "formerly with ... UCSB" statement 2023 (joint footnote), Intel Labs 2023-10-16, 2024-11-11 (raw ORCID) | confirmed: UCSB (last 2023-03-13) -> Intel Labs (first 2023-10-16) |
| G3 | Zhe Xuan | UPenn 2017-06-19 (raw ORCID), 2020-04-29 (pending org); Intel 2021-06-13, 2021-12-23 (raw ORCID) | confirmed: UPenn (2017-06-19 ORCID slot, D267 provisional) -> Intel (2021-06-13) |
| G3 | Cooper Levy | UCSD 2018-11-14; UCSD + Intel co-affiliation 2019-04-24 (raw ORCID); Intel only 2020-05-13, 2026-06-14 | UCSD (to 2018-11-14) -> UCSD + Intel co-affiliation (2019-04-24) -> Intel only (2020-05-13); a co-affiliation bridge, not a D68 move (D269) |
| G3 | Thomas Liljeberg | Agility 2003-07-07 (pending org); UCSB 2001 (candidate); Source Photonics 2004-2015 (bio); Intel 2017-06, 2024-10-22 (bio) | confirmed (bio): Agility -> Source Photonics (2004-2015) -> Intel (start not printed; first Intel slot 2017-06) |
| G3 | Ranjeet Kumar | UCSD 2013-06-10 .. 2015-03-10 (candidate); Intel 2016-08-04, 2017 (record mapping suspect) | UCSD -> Intel unconfirmed (coauthor Mookherjea, index ORCID) |
| G3 | Duanni Huang | UCSB 2018-08-30, UCSB + Intel Labs co-affiliation 2019-11-01 (candidate); Intel 2020, 2026-06-14 | unconfirmed; the 2019 row is a co-affiliation, not a move (D269) |
| G3 | Jahnavi Sharma | Columbia 2018-02 (candidate); Intel Labs 2019-02-05 (raw ORCID = 2021-12-23 Intel slot, D267 provisional); Intel 2021-02-13, 2021-12-23, 2026-06-14 | Columbia -> Intel unconfirmed (Columbia slot has no ORCID or shared org) |
| G3 | James Jaussi | Intel 2003-09 .. 2026-06-14 | no move found |
| G3 | Dan Lake | Intel 2026-06-14; Intel Labs 2010-11 (candidate, held back, D268) | no move found |
| G3 | Ahmadreza Farsaei | Intel 2025 (OFC 2025) | no move staged |
| G3 | Prathapa Puttaswamy | none beyond the existing OFC 2026 row | not found |

Name-only leads (no identity support beyond the name): 13 rows, kept only in the local review file: 9 affiliation
slots printed under pilot names (8 for review, 1 recommended reject) and 4 seed matches (1 recommended accept, 2
recommended reject, 1 for review).

## Proposed merge path (after the owner decides, D262)

1. Owner review of `observations_proposed.csv`, rows with `d63_met = yes` first, then the identity proposals.
2. Orgs: add the 4 rows of `orgs_missing.csv` through the org-curation path; Numonyx needs sourced org events before
   its rows count as an org shared with Intel. Then re-check `pending_org` rows.
3. Sources: `merge_org_events.py` regenerates all `web:` rows of `sources.csv` from `data/_staging/org_events/*` and
   drops uncited ones, so these rows would be lost there. Either a people-evidence merge step that appends `web:` rows
   from this folder, or registration of papers under the `lit:` corpus by DOI (`doi` column given).
4. Observations: the people schema allows `kind` publication / conference and `obs_id` for `eo|pk|ofc2026` sources
   only, with point dates. Proposal (DevLog-009 Q1): publication rows become `affiliation_observations` (kind
   publication, grade B, A once the printed paper is read) after extending the `obs_id` pattern and source corpus;
   bio rows (`conference_bio`, `society_page`, `company_bio`, intervals) go to a career-claims table (D10).
5. Identity: `proposed_person_id` rows become `person_xref` rows with basis `manual` and `reviewed_on` only after
   review; the local file is reviewed the same way and is never committed.
6. Transitions: after a merge, `derive_transitions.py` decides; no transition is claimed here. Co-affiliation bridges
   (Levy 2019, Huang 2019) are co-affiliations under D68, not moves (D269); `former_statement` / `joint_footnote` rows
   do not yield `explicit_move_statement`; transition grade never exceeds the B evidence grade.

## Open questions (owner; also in DevLog-009)

1. Seed "Mario Fiorentino": no Intel author of that name was found. Which person did the seed mean?
2. Seed "Guo Peng" (郭鹏): no silicon-photonics author of that name was found at Intel. Which person (company, role)
   did the seed mean?
3. D267 (equal raw ORCIDs on two work records count as D63 rule 1) is provisional: confirm.
