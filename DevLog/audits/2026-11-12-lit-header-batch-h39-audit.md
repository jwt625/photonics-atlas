---
title: Fresh-context audit of the lit author-affiliation batch lit_h39 (12 papers)
date: 2026-11-12
auditor: Claude (fresh context; wrote only this record; headers.yaml, derived files, scripts, tests, people and registry data not edited; check run only with --dry-run, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h39/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D400-D557); format from the 2026-11-11 h38 audit; read-only comparison with lit_h40 vaerenbergh2021, earlier batches and the org registry for the Hewlett Packard question
verdict: GO for the people rebuild (no slot wrong); 89 slots audited, 88 ok, 1 imprecise (li2018 #3, present address not recordable until the D442 cue fix), 0 wrong; all six extractor calls confirmed; no YAML fix in lit_h39; one consistency fix recommended in lit_h40 (vaerenbergh2021 blocks 1-2, Hewlett Packard Enterprise as org); checker gaps G1 (last author's second marker, now also on a one-line name) and G2 (locality inside the org name)
---

# Lit header batch audit: lit_h39 (2026-11-12)

## Scope

Batch lit_h39 (12 papers: 9 Optics Express / OSA-style with capitals author lines, 3 Optica with mixed-case or
capitals lines; 89 author-list slots, no header-only author; 115 rows). Restricted corpus: this record names only
authors, orgs, units, cities and countries; no paper text is quoted and no contact, street, building, postal-box or
postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h39 --corpus lit --codes <id> --pdf`
  (all 12; output kept in the session scratchpad only). Every author line and block is on page 1; no cover page, no
  later-page affiliation list, no prose statement. Markers legible and identical in both layers in all 12.
- Per slot: printed name vs `compare.csv` slot and the author list printed by `show`; printed marker run vs `markers` +
  `dropped_markers`; block fields vs the print (org, unit chain, more_orgs, city, country); role; locator; parents.
  All 30 distinct (paper, org, unit, place) tuples of `header_rows.csv` read; mappings in `compare.csv` read.
- Contact markers: sheng2026 marker 3 and zhou2020 marker 5 checked by the leading character of the masked contact lines
  in `text.md` (contents not printed): the lines start with 3 and 5, so `dropped_markers` with reason contact footnote
  is right. The other 10 papers mark their contact line with an asterisk only. Daggers in sheng2026 and miller2019 point
  to a printed equal-contribution line (symbol marks, no entry needed); gasse2019 marker 3 points to a printed
  equal-contribution line (`dropped_markers`, equal contribution: right).
- Missed blocks: cue scan of the whole `text.md` of all 12 (now with / at, present / current address, present / current
  affiliation, currently, presently, is / are / was / were (also / now) with, also with, on leave, visiting, formerly,
  deceased, permanent address, affiliat-). 3 hits: li2018 p.1 (the Current address block, below) and two body-text
  matches (jacques2019 p.7, sheng2026 p.11, both inside ordinary sentences). No missed block.
- Claims tested with dry-run probes on scratch copies of the batch (and of lit_h40 for the Hewlett Packard question)
  via the module's `LIT_BASE` (`probes/probe.py` in the session scratchpad); md5 of every lit_h39 and lit_h40 file
  identical before and after the audit.
- Stamp: `check_stamp.txt` matches `headers.yaml` (sha256 1ba43bc3...). Repo batch files untouched by this audit.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h39 | 12 / 12 | 89 | 88 | 1 | 0 |

- Rows 115 (all grade A: printed 107, single 8; primary 101, additional 14; all locators p.1 header); recorded 89,
  no_header 0; papers ok 12, partial 0, unreadable 0; `author_list_differs` 0; explicit slots 1 (lee2022 #7, needed:
  probe L1); present addresses recorded 0 (1 printed, not recordable: li2018 #3); prose blocks 0; `order_differs`
  false on every slot; 6 unmapped org strings; multi-affiliation slots 14.
- Imprecise by cause: checker gap D442 "Current address" cue (li2018 #3, Carlos Ríos: block 2 not recorded, the
  precedent form; values for the re-record list in question 1).
- Per paper (slots / rows / rating): beeck2020 8 / 13 ok; gasse2019 3 / 6 ok; kumar2025 2 / 2 ok; souleiman2024
  11 / 14 ok; lee2022 8 / 10 ok; thai2018 10 / 20 ok; sheng2026 5 / 5 ok; li2018 7 / 7 (6 ok, 1 imprecise); miller2019
  12 / 13 ok; jacques2019 6 / 7 ok; zhou2020 11 / 12 ok; zeng2019 6 / 6 ok.

### Per-slot field counts (89 slots)

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (89) | 89 | 0 | 0 |
| markers + dropped_markers (89) | 89 | 0 | 0 |
| blocks (org / unit / more_orgs / locality / country) (89) | 89 | 0 | 0 |
| present addresses (1 printed) | 0 | 1 (li2018 #3, D442 gap) | 0 |
| prose blocks | n/a (none printed) | | |
| locators (89) | 89 | 0 | 0 |
| unreadable authors | n/a (none) | | |

## Per-paper findings

- beeck2020 (8): marker runs 1,2 x5 / 3 x3 (asterisk on author 1 = corresponding author). Block 1 Ghent University -
  imec (dash-joined, kept as printed, D426) + Photonics Research Group, Department of Information Technology, country
  BE; block 2 Ghent University + Center for Nano- and Biophotonics, BE; block 3 Tyndall National Institute, Cork, IE.
  Blocks 1 and 2 print only the country: `locality: ""` is right (D288). The checker does not enforce it (probes B1 /
  B2: Ghent added to either block passes, G2). Rows map to Ghent University + imec and Tyndall. ok.
- gasse2019 (3): marker runs 1,2,3 / 1,2,3 / 1,2; 3 = equal contribution (`dropped_markers`, probe G1 without it: 2
  errors). Block 1 same org + unit as beeck2020, Ghent, BE (a site name and the street printed after the org are not
  recorded; no skip span needed because they follow the org); block 2 Ghent University + Center for Nano- and
  Biophotonics (NB-Photonics) with its acronym as printed, Ghent, BE. List #3 Günther vs printed GUNTHER: automatic. ok.
- kumar2025 (2): single unmarked block (`single`, authors `[]`), University of Rochester + The Institute of Optics
  (leading article as printed), Rochester, US (state not recorded). List #2 Cárdenas vs CARDENAS: automatic. ok.
- souleiman2024 (11): marker runs 1,2 / 1 x3 / 3 x2 / 1 x2 / 2 x2 / 1 (asterisk on author 11). Block 1 III-V Lab,
  Palaiseau, FR: the printed description naming its three parent organizations is not copied (parent rule, D426
  keyvaninia2012; III-V Lab alone in lit_h05, h09, h11, h12, h14, h17, h20, h25, h32); the postal designation after the
  city dropped (D366). Block 2 Télécom SudParis + unit SAMOVAR, Palaiseau, FR, parent Institut Polytechnique de Paris
  not copied: identical to lit_h09 ramirez2022 and ofc_h04 M4A.1 (probe U1: adding the parent as more_orgs also
  passes, so the form is a ruling, not a checker constraint). Block 3 CEA-Leti + more_orgs Université Grenoble Alpes,
  Grenoble, FR: the printed order org-then-university, same form as lit_h01 brisson2023 / fowler2025, lit_h07
  ibrahimi2021, lit_h20 primiani2019, ofc_h03 M3B.6. Initials-only names match their full list names automatically. ok.
- lee2022 (8): marker runs 1 x2 / 2 / 1 x3 / 1,3 / 1,3 (asterisk on author 1). Block 1 Fraunhofer Heinrich Hertz
  Institute, Berlin, DE (street not recorded); block 2 Soares Photonics, Lisbon, PT; block 3 Technische Universität
  Berlin + unit Institut für Festkörperphysik (printed before the university), Berlin, DE. Author 7 printed BJOERN
  GLOBISCH, list Björn Globisch: the strict matcher finds 0 candidates without the explicit slot (probe L1: 2 errors)
  and `slot: 0` fails (probe L2: 1 error, D302); `slot: 7` is a D287 transliteration variant (umlaut written oe; same
  family name, same position, one Globisch in the list). Martin Schell's second marker 3 is not bound (probe E1, G1).
  ok.
- thai2018 (10): marker runs 1 / 1 / 2 / 2 / 1 / 2 x4 / 1 (asterisk on author 1). Blocks print University Grenoble
  Alpes, then CEA, then the CEA unit: recorded as org University Grenoble Alpes + structured more_orgs CEA with unit
  INAC-Pheliqs (block 1) / Leti (block 2), Grenoble, FR; the same form as lit_h10 tyler2019, lit_h14 singaravelu2019,
  lit_h21 szelag2017 (and Univ. / Université variants in lit_h07, h09, h13, h29, h40). Unit spellings Leti and
  INAC-Pheliqs as printed. University Grenoble Alpes is unmapped (10 rows) but already requested in
  `lit_headers/org_requests.csv` (28 rows); the CEA rows map. Abbreviated list names (N. Pauc, J. Aubin, V. Delaye, A.
  Chelnokov, V. Calvo) automatic. ok.
- sheng2026 (5): marker runs 1,dagger,* / 1,3,dagger / 2 / 1 / 1. Marker 3 has no printed block and points to a contact
  line (verified; probe S1 without it: 2 errors). Block 1 Eindhoven University of Technology + Eindhoven Hendrik Casimir
  Institute (EHCI), Eindhoven, NL; block 2 Tokyo Institute of Technology + Department of Electrical and Electronic
  Engineering (period between unit and org as printed), Tokyo, JP. ok.
- li2018 (7): marker runs 1 / 1 / 1,2 / 1 / 3 / 4 / 1,*. Blocks Department of Materials, University of Oxford, Oxford,
  GB; Department of Engineering, University of Exeter, Exeter, GB; Department of Physics, University of Münster,
  Münster, DE. Block 2 is a present address of Carlos Ríos printed with the cue Current address: the checker rejects it
  both as `present_address` (probe R2: 2 errors, marker + first field) and as an affiliation (probe R3: same 2
  errors), and the marker is bound (probe R1 without the dropped 2: 2 errors). Keeping 2 under `dropped_markers` is the
  only passing form and follows jung2020 (lit_h30), purnawirman2017 (lit_h32) and the lit_h05 / h16 / h17 / h27 cases:
  imprecise (D442), question 1. C. DAVID WRIGHT vs list Christopher David Wright and WOLFRAM HP PERNICE vs Wolfram H. P.
  Pernice: automatic. ok otherwise.
- miller2019 (12): mixed-case author line; marker runs 1,dagger / 1,2,dagger / 1 x9 / 1,*. Block 1 Columbia University
  + Department of Electrical Engineering, New York, US (state not recorded); block 2 National Chiao Tung University +
  Department of Photonics and Institute of Electro-Optical Engineering, Hsinchu, TW (probe M1: dropping Chang's 2 gives 3
  errors). ok.
- jacques2019 (6): marker runs 1,* / 1 / 1,2 / 1 / 1 / 1. Block 1 McGill University + Department of Electrical and
  Computer Engineering, Montreal, CA; block 2 Alexandria University + Electrical Engineering Department, Alexandria, EG
  (probe J1 bound). ok.
- zhou2020 (11): marker runs 1 / 2 / 1,3 / 4 / 1 x4 / 3 / 1 / 2 / 1,5. Block 1 Nanyang Technological University +
  School of Electrical and Electronic Engineering, Singapore, SG; block 2 National University of Singapore + Department
  of Electrical and Computer Engineering, Singapore, SG; block 3 Singapore MIT Alliance for Research and Technology
  (SMART) + unit Low Energy Electronic Systems (LEES) (printed before the alliance), Singapore, SG; block 4 Applied
  Materials Inc., Sunnyvale, US (`org_applied_materials`). Marker 5 of the last author points to a contact line
  (verified), but the checker does not bind it (probes Z1 without it and Z2 with 6 instead: 0 errors, G1). Names split
  over lines (YI-CHIAU HUANG, KWANG HONG LEE, CHUAN SENG TAN) read whole. ok.
- zeng2019 (6): single unmarked block (`single`, authors `[]`; asterisk on author 3 = corresponding author): printed
  Hewlett Packard Labs, then Hewlett Packard Enterprise, then Palo Alto, US. Recorded org Hewlett Packard Enterprise +
  unit Hewlett Packard Labs (rows map to `org_hewlett_packard_enterprise`). List #5 Marco Fiorentino B is an author-list
  artefact (D412), name printed correctly in the YAML; slot 5 automatic. ok (question 6 on the org form).

## Fixes (exact YAML edits)

None in lit_h39. No slot, marker, block field, locator or note needs a change; the explicit slot is required (probe
L1).

Recommended in lit_h40 (sibling batch, its own audit decides), for the consistency of question 6, verified on a
scratch copy (probe V1: 0 errors, 1 expected warning):

```yaml
    - {marker: "1", basis: printed, org: "HPE Belgium", unit: "LSIP Lab, Hewlett Packard Labs", locality: "Diegem", country: "BE"}
    - {marker: "2", basis: printed, org: "Hewlett Packard Enterprise", unit: "LSIP Lab, Hewlett Packard Labs", locality: "", country: "US"}
```

with the vaerenbergh2021 note sentence on blocks 1 and 2 changed to say the printed company (HPE Belgium / Hewlett
Packard Enterprise) is the org and LSIP Lab, Hewlett Packard Labs the unit chain, as tossoun2019 / tossoun2024 /
zeng2019 / ofc Th2A.29.

## Open questions (with recommendation)

1. li2018 #3 Carlos Ríos, block 2 Current address (extractor call 1). Confirmed: the checker rejects the cue (probes R2,
   R3), marker 2 is bound (R1), the YAML matches the jung2020 / purnawirman2017 precedent. Recommended: accept as is
   and add to the D442 re-record list with: `{marker: "2", basis: printed, role: present_address, org: "Massachusetts
   Institute of Technology", unit: "Department of Materials Science & Engineering", locality: "Cambridge", country:
   "US"}` inserted between blocks 1 and 3, author 3 `markers: ["1", "2"]` without `dropped_markers`, and the note
   sentence on block 2 removed.
2. zeng2019 #5 Marco Fiorentino B (call 2). Confirmed: the list name carries a trailing letter, the printed name is
   right. The same artefact is in lit_h40 vaerenbergh2021 slot 8. Recommended: both slots go into the D412
   author-list correction file (Marco Fiorentino B -> Marco Fiorentino); no YAML change.
3. sheng2026 #2 marker 3 and zhou2020 #11 marker 5 as contact footnotes (call 3). Confirmed by the leading characters
   of the masked contact lines; neither has a printed block. Recommended: accept. zhou2020 #11 (and lee2022 #8) are new
   test cases for G1.
4. lee2022 slot 7 BJOERN GLOBISCH / Björn Globisch (call 4). Confirmed required (L1) and the only passing value (L2);
   oe for an umlaut is a plain transliteration variant under D287 (Naoto / Nato class), distinctive family name, same
   position. Recommended: accept; no D426 review entry needed (not a dropped syllable or order swap). Optional checker
   improvement: fold umlaut vowels to their oe / ue / ae spellings in the lit matcher (low priority).
5. souleiman2024, thai2018, beeck2020 (call 5). Confirmed: III-V Lab parents not copied (D426), SAMOVAR as unit of
   Télécom SudParis with the Institut Polytechnique de Paris parent not copied (lit_h09 ramirez2022, ofc_h04 M4A.1),
   CEA-Leti + Université Grenoble Alpes in more_orgs (lit_h01, h07, h20, ofc_h03), thai2018 University Grenoble Alpes +
   structured CEA more_orgs with the CEA unit (lit_h10, h14, h21), beeck2020 blocks 1-2 print no city (locality empty
   is required by D288 even though the checker would accept Ghent, G2). Recommended: accept all.
6. Hewlett Packard Labs vs Hewlett Packard Enterprise (call 6). What each prints: zeng2019 prints the lab, then the
   company Hewlett Packard Enterprise, then the city. lit_h40 vaerenbergh2021 prints LSIP Lab, then Hewlett Packard
   Labs, then the company (HPE Belgium in block 1, Hewlett Packard Enterprise in block 2). Earlier batches: the identical
   lab-then-company string is recorded as org Hewlett Packard Enterprise + unit Hewlett Packard Labs in lit_h04
   tossoun2019, lit_h16 tossoun2024 and ofc_h13 Th2A.29 (all map to `org_hewlett_packard_enterprise`); lit_h01
   cheung2023 (company printed first, then the lab) org Hewlett Packard Enterprise + unit Large-Scale Integrated
   Photonics Lab; only ofc_h01 M1G.3, which prints no company, has org Hewlett Packard Labs. The same corporate-lab form
   is used for Nokia + Bell Labs (lit_h29), Applied Materials + Varian Semiconductor (lit_h26, D521) and IBM Research +
   T. J. Watson Research Center (lit_h17). Registry: `org_hewlett_packard_enterprise` (ROR-backed) and
   `org_hewlett_packard_labs` (created from M1G.3) both exist; the lab has no `parent_org_id` (its note flags HPE as a
   review candidate); `org_aliases.csv` has no Hewlett Packard entry; HP Labs, Hewlett Packard Enterprise Labs and
   Hewlett Packard Laboratories are open lit org requests. As recorded now, Zhihong Huang, Marco Fiorentino and Raymond
   G. Beausoleil get rows under HPE in zeng2019 and under the unlinked HP Labs id in vaerenbergh2021. Recommended one
   form: when a company is printed after the lab, org = the printed company, unit = the lab chain ending in Hewlett
   Packard Labs; org Hewlett Packard Labs only when no company is printed (M1G.3) or the lab name is printed alone.
   zeng2019 stays as is; lit_h40 vaerenbergh2021 blocks 1-2 change as in Fixes (HPE Belgium to the org round as a
   lit-scoped alias or child of `org_hewlett_packard_enterprise`). In the org round also set `org_hewlett_packard_labs`
   `parent_org_id` = `org_hewlett_packard_enterprise` and map HP Labs / Hewlett Packard Laboratories / Hewlett Packard
   Enterprise Labs to the lab id. The alternative (org Hewlett Packard Labs, parent rule) would require re-recording the
   four committed or staged lab-then-company blocks instead of two.

## Unmapped org names (org round, no YAML change)

| printed org (unit) | place | proposal |
|---|---|---|
| Alexandria University (Electrical Engineering Department) | Alexandria, EG | new org (no registry entry, no earlier request) |
| National Chiao Tung University (Department of Photonics and Institute of Electro-Optical Engineering) | Hsinchu, TW | new org; already requested from lit:fan2021 |
| Singapore MIT Alliance for Research and Technology (SMART) (Low Energy Electronic Systems (LEES)) | Singapore, SG | new org (no registry entry) |
| Soares Photonics | Lisbon, PT | new org (no registry entry) |
| University Grenoble Alpes | Grenoble, FR | printed-variant alias to `org_universite_grenoble_alpes` (already requested, 28 rows) |
| University of Exeter (Department of Engineering) | Exeter, GB | new org (no registry entry) |

## Privacy and as-printed scan

- Grep over the batch files and this record for contact / URL patterns, street and building words of the printed
  blocks, and digit runs of 4 or more: no contact or URL text; street / postal / site words only in notes that say such
  text was not recorded; digit runs only paper-id years, the stamp hash and log pids. No postal code, street, building
  or site text in any field.
- As printed (kept, correct): Ghent University - imec (dash-joined), The Institute of Optics (leading article), Leti
  and INAC-Pheliqs spellings, Applied Materials Inc., Télécom SudParis and Université Grenoble Alpes accents, University
  Grenoble Alpes (thai2018 form). No `skip_prefix` or `skip_between` in this batch.

## Commands (2026-11-12, log times)

| Command | Result |
|---|---|
| `check lit_h39 --corpus lit --dry-run` 23:22:13 (pid 31383) | 0 errors, 1 warning (lee2022 explicit slot 7); slots 89, recorded 89; rows 115 (grade A 115; primary 101, additional 14; printed 107, single 8); papers ok 12; multi-affiliation slots 14; present addresses 0; 6 unmapped org strings |
| `show lit_h39 --corpus lit --codes <id> --pdf`, all 12 | headers and author lists read (scratchpad only) |
| `show` (no `--pdf`) for lit_h04 tossoun2019, lit_h16 tossoun2024, lit_h01 cheung2023, lit_h40 vaerenbergh2021, ofc_h13 Th2A.29 | Hewlett Packard block forms read (scratchpad only) |
| `probes/probe.py` on scratch copies, dry-run | below; repo lit_h39 and lit_h40 md5 unchanged; the dry-run checks write their usual log files under `logs/` |

| probe | change | result | reading |
|---|---|---|---|
| L1 | lee2022 BJOERN GLOBISCH without `slot: 7` | 2 errors (0 candidates, slot 7 unmatched) | explicit slot required |
| L2 | same with `slot: 0` | 1 error (slot 7 unmatched) | slot 0 not allowed (D302) |
| E1 | lee2022 Martin Schell without marker 3 | 0 errors | G1: last author's second marker not bound (one-line name) |
| S1 | sheng2026 Yi Wang without dropped marker 3 | 2 errors | contact marker bound |
| Z1 | zhou2020 Chuan Seng Tan without dropped marker 5 | 0 errors | G1 (name split over two lines) |
| Z2 | zhou2020 Tan dropped marker 6 instead of 5 | 0 errors | G1 confirmed |
| R1 | li2018 Carlos Ríos without dropped marker 2 | 2 errors | marker bound |
| R2 | li2018 block 2 recorded as `present_address` (MIT), Ríos markers 1, 2 | 2 errors (marker + first field) | D442 cue gap; dropped_markers is the only passing form |
| R3 | same block with role affiliation | 2 errors (same) | cue blocks any recording |
| G1 | gasse2019 Van Gasse without dropped marker 3 | 2 errors | equal-contribution marker bound |
| B1 | beeck2020 block 1 locality Ghent | 0 errors | G2: city accepted from inside the org name |
| B2 | beeck2020 block 2 locality Ghent | 0 errors | G2 |
| M1 | miller2019 You-Chia Chang without marker 2 | 3 errors | markers bound |
| J1 | jacques2019 El-Fiky without marker 2 | 3 errors | markers bound |
| U1 | souleiman2024 block 2 + more_orgs Institut Polytechnique de Paris | 0 errors | parent omission is a ruling (D426), not checker-enforced |
| Y1 | zeng2019 org Hewlett Packard Labs, no unit | 0 errors | both org forms pass; consistency is a ruling |
| V0 | lit_h40 unchanged copy | 0 errors, 1 warning | baseline |
| V1 | lit_h40 vaerenbergh2021 blocks 1-2 as in Fixes | 0 errors, 1 warning | recommended form passes |

## Checker gaps observed (scripts not edited)

- G1 Last author's second marker not bound: zhou2020 #11 (name split over two lines, as h38 zhang2024 #8) and now also
  lee2022 #8 (name on one line, followed by the block list). A missing or wrong second marker passes. Add both as test
  cases to the D442 / D546 last-author marker-window gap (chen2024b, chen2018, zhang2024). YAML exact; nothing waits.
- G2 Locality check accepts a city found only inside the org name (beeck2020 blocks 1-2 with Ghent pass; D557
  johnson2020 gap). YAML exact (empty).
- D442 "Current address" cue still unsupported (li2018 #3; re-record values in question 1).

## Verdict

GO. No slot carries a wrong person, org, city, country or marker, nothing is invented, no block is missed, and no
address or contact text is recorded. The one imprecise slot (li2018 #3) is the known D442 cue gap in its precedent
form. No YAML fix in lit_h39; for corpus consistency the lit_h40 vaerenbergh2021 blocks 1-2 should take the
company-as-org form (question 6) before or with the next rebuild, plus the HP Labs parent link in the org round.
