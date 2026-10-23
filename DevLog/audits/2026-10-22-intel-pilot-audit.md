---
title: Fresh-context audit - Intel SiPh people pilot staging (DevLog-009)
date: 2026-10-22
scope: DevLog/DevLog-009-intel-siph-pilot.md (groups, D180-D189, D260-D264, results), data/_staging/people/intel_pilot/ (README.md, observations_proposed.csv 76 rows, sources_proposed.csv 51 rows, orgs_missing.csv 4 rows), data/_local/intel_pilot_review.csv (13 rows, read only)
rules: DevLog-004 (D62/D63, D64, D68, D70, D94, D96), DevLog-000 D8-D12
auditor: Claude (fresh context, read only except this file)
---

# Intel SiPh pilot audit (2026-10-22)

## Method

- Groups re-derived independently: LIN `canonical/edges.yaml` + `canonical/people.yaml` + `people_seed.yaml`
  (sibling input `PlayGround/20260823_photonics_lineage`), `data/people/affiliation_observations.csv`,
  `person_xref.csv` (`lin_id` scheme).
- Whole-file mechanical checks on all 76 rows (script in agent scratch, nothing written to the repo): person ids,
  proposed ids, org ids, source keys exist; ISO partial dates; quotes <= 200 chars; no "@"; person_id xor
  candidate_key; d63_met / grade / group counts; source_type values against `registry.schema.yaml`.
- Common-family and D96 b (dense key) flags recomputed in memory with `photonics_atlas.people.load_inputs()` (no
  writes).
- Web: 35 WebFetch requests, no curl, no personal identifier in any request, LinkedIn not touched, no 403 or
  anti-bot page met. 31 OpenAlex work records (`api.openalex.org/works/doi:...?select=publication_date,authorships`,
  the same read path as the pilot) and 4 web pages (2 Optica speaker pages, Lightwave Logic bio, IEEE SCV EPS page;
  3 of them re-read for exact-string checks). 60 of 76 rows checked against their source.

## Counts

| Check | ok | imprecise | wrong |
|---|---|---|---|
| 1. Group reconstruction (3 groups) | 3 | 0 | 0 |
| 2a. Mechanical checks, all 76 rows (ids, dates, quote length, grades, counts) | 76 | 0 | 0 |
| 2b. Rows checked against source (60 rows) | 52 | 7 | 1 |
| 3. The 5 confirmed moves | 3 | 2 | 0 |
| 4. Privacy (6 items) | 3 | 2 | 1 |

## 1. Group reconstruction

| Group | Claimed | Re-derived | Result |
|---|---|---|---|
| G1 | 11 | 11: LIN persons whose every edge targets `org_intel` / `org_intel_silicon_photonics`; each has exactly 1 edge, to `org_intel_silicon_photonics`, source `src_optica_intel_siph_team`. Same 11 names as assessment D.1 | ok |
| G2 | 4 | 4: Intel-block seeds with no canonical record: Mario Fiorentino, Robert Blum, Michael Davenport, Guo Peng. The other 13 Intel-block seeds are canonical (Drew Alduino as `person_andrew_alduino` alias; Li Ruolin / Nie Hui as `person_china_*`; Jie Sun, Marcus Yang by name) | ok |
| G3 | 11 | 11: non-PK observations with `org_id = org_intel` belong to 12 persons; minus LIN person Haisheng Rong = Farsaei, Levy, Lake, Huang, Sharma, Jaussi, Puttaswamy, Kumar (EO + OFC), Liljeberg, Lee (EO), Xuan | ok |

DevLog-009 row counts (G1 25 / G2 8 / G3 43; d63 yes 50 / no 14 / pending_org 4 / n/a 8; 17 person ids, 15
candidate keys; 51 sources, all used, all B) match the files exactly. D96 b computation reproduced: common families
among pilot names = Liu, Kang, Kumar, Lee, Huang, Sharma; dense keys = "yimin kang", "zhe xuan"; "liao", "levy",
"lake", "liljeberg", "cohen", "jones", "jaussi" not common. None of Rong, Jaussi, Mookherjea, Buckwalter,
Krishnaswamy, Aflatouni is a hub (D92), so single-coauthor rule (3) support stands where claimed.

## 2. Row checks

### 2a. Mechanical (76 rows): all ok

All `person_id` / `proposed_person_id` exist in `data/people/people.csv`; all non-empty `org_id` exist in the
registry; 7 rows have empty `org_id` exactly for the 4 missing orgs (Numonyx x2, Gemfire, UPenn x2, Agility x2);
dates match `YYYY[-MM[-DD]]`; max quote length < 200; no "@" anywhere; every row has exactly one of person_id /
candidate_key; every row with `person_id` has `d63_met = yes`; source types are valid enum values.

### 2b. Against the source (60 rows)

Rows checked (verbatim strings, dates and author positions in the OpenAlex record or page): ip001-ip010, ip017,
ip018, ip020, ip023, ip026-ip036, ip038, ip039, ip041-ip045, ip047-ip066, ip068-ip074, ip076. Printed name,
printed org, quote and `active_on` (OpenAlex `-01-01` -> year, `-01` -> month, as D183 / README say) agree for all
60. Findings:

| # | Row(s) | Severity | Evidence | Fix |
|---|---|---|---|---|
| F1 | ip051 (Jahnavi Sharma, Intel Labs 2019-02-05) | wrong | JSSC 10.1109/jssc.2018.2889690 authorship raw_orcid 0000-0003-0304-4706. The same raw ORCID is on Jahnavi Sharma's authorship in JSSC 10.1109/jssc.2021.3134221 (2021-12-23, "Intel Corporation, Hillsboro, OR, USA"), whose author list (Xuan, Kumar, Rong, Jaussi) shares coauthors and Intel with OFC 2026 Tu3C.2, i.e. rule (3) to `person_jahnavi_sharma`. This is exactly the chain used to give ip052 (Zhe Xuan) a person_id; the row says "person has no ORCID" and stays `d63_met = no` | Stage the Sharma slot of jssc.2021.3134221 (rule 3), set ip051 `person_id = person_jahnavi_sharma`, `d63_met = yes`, basis "raw ORCID equal to the 2021-12-23 Intel slot". ip050 (Columbia 2018-02, raw_orcid null, verified) stays a candidate: Columbia -> Intel remains unconfirmed |
| F2 | ip041 (Wonho Lee, "formerly with ... UCSB", `org_ucsb`, aff_role primary, active_on 2023) | imprecise | OpenAlex lssc.2023.3294172: the three strings (UCSB department; "Intel Labs, Hillsboro, OR and Samsung Semiconductor, San Jose, California"; "formerly with ...") are attached identically to both Wonho Lee and coauthor Jeff Shih-Chieh Chien (joint footnote). As coded, the row reads "at UCSB on 2023" | Mark the row as a former-affiliation statement (not `primary`; e.g. aff_role `former`, or keep it only as the move statement for the transition layer); note the string is shared with a coauthor |
| F3 | ip042 (Wonho Lee, Intel Labs, aff_role `present_address`) | imprecise | Same joint footnote names two orgs for two authors. Under D68 a `present_address` row yields `explicit_move_statement`, grade A, from a B row whose author-to-org split is not printed | Do not code as `present_address` (or exclude from D68 explicit-move derivation); transition grade must not exceed B (D260). Intel for Lee is carried by ip043 / ip044 anyway |
| F4 | ip043 (Wonho Lee, Intel Labs 2023-10-16) | imprecise | identity_basis cites org shared with eo:lee2026 and coauthor shared with "the ORCID-bearing slots" (UCSB slots): two different pairs. Rule (3) does hold on one pair: tmtt.2024.3490257 (raw ORCID = person ORCID, "PRL PCR, Intel Labs") shares Intel and both coauthors (Justin J. Kim, James F. Buckwalter) with bcicts.2023.10310903 | Rewrite identity_basis: "rule 3 with the 2024-11-11 ORCID slot (Intel Labs; coauthors J. J. Kim, J. F. Buckwalter)" |
| F5 | ip035 (Ranjeet Kumar, CLEO 2017, Intel) | imprecise | In cleo_at.2017.jth5c.6 the deposited metadata prints "Intel Corporation, United States" also for Shayan Mookherjea, whom the staged UCSD rows (ip036 / ip037) show at UCSD; first two authors print UCSD. Author-to-affiliation mapping in this record is suspect | Add a note "record-level mapping suspect (PI printed Intel)"; the Kumar Intel claim is carried by ip034 (Optica 2016) and the person's ORCID on jssc.2021.3134221 |
| F6 | ip026 (Blum, Optica OIDA 2021) | imprecise | Page has curly apostrophe "Intel’s"; staged quote has ASCII "'" (quote not character-exact). identity_basis on ip026-ip029 says "company bio" but the source is the Optica speaker page | Keep page characters or note normalization; fix identity_basis text for the Optica rows |
| F7 | ip029 (Blum, Gemfire, note "bio order: before JDS Uniphase") | imprecise | Optica page: "Prior to joining Intel ... Oclaro"; "Before joining Oclaro ... JDS Uniphase ... and held various engineering and marketing management roles at Gemfire Corporation". The Gemfire step is joined by "and", no ordering word (D183: ordering words recorded, not inferred) | Note "listed with JDSU, order not stated" |
| F8 | ip004 (Ling Liao, `role = joined Intel`, start_on 1997) | imprecise | IEEE SCV EPS page (meeting 2017-03-08): "She joined Intel in 1997" verified; "joined Intel" is not a role | Leave `role` empty; keep start_on 1997 and the quote |

Not counted as errors but noted:

- ip066 (Dan Lake 2010, Intel Laboratories, virtual-worlds paper): verified as staged (coauthors Mic Bowman, Huaiyu
  Liu, "Intel Laboratories, Intel Corporation, Hillsboro, OR, USA"). D63 rule (2) formally holds ("lake" not common,
  key not dense), but the only link to the 2026 photonics slots is exact name + Intel (a very large org) with no
  shared coauthor and a different field. See open question 2.
- ip012 (John Heck UCSB, book contributor list): "likely list error" is a guess; correctly kept as a candidate
  with `d63_met = no` and a "do not derive a transition" note.
- ip017 / ip020 (Numonyx 2008-12): verified; the JLT record also lists Nomi Elek, Rami Gabay at Numonyx and
  Liu, Kim, Jones, Paniccia at Intel, so the coauthor support is real; `pending_org` is right.
- 2 key rows the pilot re-fetched (s44287-025-00223-0, lssc.2023.3294172) match character for character.
- Grades: all 66 publication rows B per D260 (metadata, printed paper not read) and the 10 bio / society rows B per
  D261: consistent; no A claimed anywhere.

## 3. The 5 confirmed moves

| Move | Verdict | Evidence / caveat |
|---|---|---|
| Wonho Lee UCSB -> Intel Labs (2023) | ok (B; identity ORCID) | Raw ORCID 0000-0001-8159-9067 (= `people.csv` ORCID) on tcsii 2021 (KAIST + UCSB), lssc 2023 and tmtt 2024 (Intel Labs); last UCSB-only slot jmw 2023-03-13, first Intel-only slot 2023-10-16 (rule 3 to the 2024 ORCID slot, F4). Direction supported by "formerly with ... UCSB". Caveat: the "formerly" and "Intel Labs ... and Samsung" strings are joint footnotes shared with a coauthor (F2, F3); the Intel destination rests on the ORCID slot, not on the footnote |
| Zhe Xuan UPenn -> Intel (2017-06-19 -> 2021-06-13) | ok (B; identity ORCID chain) | tmtt.2017.2712144 raw ORCID 0000-0003-4583-4060 = raw ORCID on jssc.2021.3134221 (Intel, Hillsboro); that slot joins the person by rule 3 (Intel + Sharma, Kumar, Rong, Jaussi from OFC Tu3C.2); vlsicircuits 2021-06-13 verified. Caveat: D63 rule (1) is written for EO Crossref slot ORCIDs; extending it to OpenAlex raw_orcid between two staged slots is reasonable but is an owner decision (open question 1). `people.csv` has no ORCID for this person |
| Cooper Levy UCSD -> Intel (co-affiliated 2019-04-24, Intel-only 2020-05-13) | imprecise | Identity ok: 2020-05-13 slot rule 3 (Intel + James E. Jaussi); 2019 slot exact "Cooper S. Levy" + Intel (rule 2, "levy" not common); 2018 UCSD slot exact + UCSD with the 2019 slot. All strings verified; tim.2019 raw ORCID 0000-0002-8995-3670. But the 2019 source lists both UCSD and Intel, so by D68 ("A -> B when hi(last A) < lo(first B) and no source lists both") this is a co-affiliation bridge, not a derived transition. Call it "UCSD (to 2018-11-14) -> UCSD + Intel co-affiliation (2019-04-24) -> Intel only (2020-05-13)"; README merge-path step 6 should not promise a `publication_sequence` arrow here |
| Thomas Liljeberg Agility -> Source Photonics (2004-2015) -> Intel | ok (B; bio states the person) | Optica PECC 2024 page (event 2024-10-22..23) verified verbatim: "From 2004 to 2015, he was at Source Photonics ...", "Prior to Source Photonics, he was with Agility Communications.", UCSB Ph.D.; header "Sr. Director" vs bio "General Manager" noted in the row. Intel start not printed; first Intel slot oic.2017 2017-06 verified; Agility slot SPIE 2003-07-07 verified (coauthor Yuliya A. Akulova, later Intel). Identity: exact name + Intel, "liljeberg" not common |
| Robert Blum Gemfire -> JDSU -> Oclaro -> Intel -> Applied Materials -> Lightwave Logic (from 2025-05) | imprecise | Both bios verified (Lightwave Logic: "joined Lightwave Logic in May 2025", "most recently the Head of Product Line Management ... at Applied Materials", "Head of Silicon Photonics Strategy at Intel Corporation"; Optica OIDA 2021-03-30..31: Intel SiPh director). Ordered by words: Oclaro -> Intel ("Prior to joining Intel"), JDSU -> Oclaro ("Before joining Oclaro"), Applied Materials last before Lightwave Logic ("most recently"). Gemfire -> JDSU is list order only (F7). Identity: two bios joined on name + four shared orgs (strong), no `data/people/` person; the LIN seed link is not evidence (seed has no source). B is correct (D261) |

No move is wrong. Additional move-level finding: Jahnavi Sharma's 2019 Intel Labs slot meets D63 through the ORCID
chain (F1), so her earliest Intel slot moves from 2021-02-13 to 2019-02-05; Columbia -> Intel stays unconfirmed
(no ORCID or shared org on the Columbia slot).

## 4. Privacy

| Item | Result | Evidence / fix |
|---|---|---|
| `data/_local/intel_pilot_review.csv` git-ignored | ok | `git check-ignore -v` -> `.gitignore:26:data/_local/`; `git ls-files data/_local` empty |
| No e-mail / phone / non-professional data in staging | ok | no "@" in any cell; quotes are institutional addresses and roles; raw strings that contain author e-mails (nature02310, ol.36.002101 records) were not copied |
| ORCIDs in locators / identity_basis | ok | professional identifiers already in `data/people/` for Lee / Kumar / Rong; Xuan / Sharma / Levy iDs are publisher-deposited |
| Name-only links kept local only (D64, D69, D182, D187) | wrong | The 13 local rows are local, but their content is restated in files meant to be committed: DevLog-009 lines 117-118 ("Name-only (local): Dosunmu -> Applied Materials (2025-12-02), Farsaei UBC -> Cadence -> LuDALog -> Intel, Davenport Intel (2012) -> Ayar Labs (2020)"); README findings table rows Rong (MIT 2002 / U. Florida 2002-12), Dosunmu (Applied Materials 2025-12-02), Davenport (Ayar Labs 2020), Farsaei (UBC, Cadence, LuDALog); `observations_proposed.csv` notes of ip023 (Applied Materials 2025-12-02) and ip076 (UBC / Cadence / LuDALog). Fix: replace with counts ("n name-only candidates in the local review file") and remove org names and dates of name-only slots from DevLog, README and CSV notes |
| LinkedIn (D9, DevLog-009 "LinkedIn not searched or fetched") | imprecise | README Heck row: "NVIDIA lead is LinkedIn-only, not used". Discloses an unverified move from a C-class source in a committed file and contradicts "not searched" (the lead must have come from a search result). Fix: remove the phrase; if kept, say where it was seen and keep it local |
| Seed name-variant statements | imprecise | DevLog Q2 / README OQ1 name Marco Fiorentino (HPE) as a possible spelling of the seed; DevLog Q3 / README OQ2 describe the Intel "Peng Guo" as a compiler author. Both are rejected name matches stated in committed text. Low risk (no link asserted), but the questions can be asked without naming the other person's employer / field; detail is already in the local file (ipr009, ipr010) |

## Other findings

| # | Item | Severity | Evidence | Fix |
|---|---|---|---|---|
| O1 | `orgs_missing.csv` Numonyx notes: "formation from Intel/STMicroelectronics flash units, later acquisition by Micron" | imprecise | Corporate history stated without a source (the note itself says none researched) | Mark as "unsourced background, to be sourced" or remove until org events are sourced |
| O2 | README merge path step 6 / D68 | imprecise | Promises the confirmed moves appear as `publication_sequence` or `explicit_move_statement`; Cooper Levy gives co-affiliation (source lists both), and Wonho Lee ip042 would give a grade-A explicit move from a B row | Amend step 6; cap transition grade at the evidence grade |
| O3 | ip033 / ip026-ip032 group G2 label | note | The rows carry no person id and no proposed id, so no seed link is asserted; the G2 label only records why they were searched. The Davenport seed link is name + Intel block + topic, and is correctly in the local file (ipr007) | Optional: note "seed link not asserted" on G2 rows |

## Open questions (owner)

1. D63 rule (1) extension: accept OpenAlex `raw_orcid` equality between two staged slots (Zhe Xuan ip052; Jahnavi
   Sharma ip051 after F1) as an ORCID join? Rule (1) is written for EO Crossref slot ORCIDs.
2. Dan Lake 2010 (ip066): keep `person_id` (rule 2 holds) or downgrade to a candidate until a shared coauthor or bio
   ties the 2010 virtual-worlds author to the 2026 photonics author? Exact name + Intel is a weak discriminator for an
   org of Intel's size.
3. Co-affiliation bridges (Cooper Levy, Duanni Huang 2019): show as "moves" in the people views, or only as
   co-affiliation per D68?

## Verdict

Staging is accurate and well sourced: groups exact, 76 / 76 rows mechanically clean, 52 / 60 source checks exact,
grades consistent with D260 / D261. Before commit: fix the privacy leak of name-only details (check 4) and F1
(Sharma ORCID chain); F2-F8 and O1-O2 are wording / coding fixes. The 5 moves hold at B: Lee, Xuan, Liljeberg as
stated; Levy is a co-affiliation bridge rather than a D68 transition; Blum's Gemfire step is list order only.
