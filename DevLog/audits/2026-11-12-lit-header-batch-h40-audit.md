---
title: Fresh-context audit of the lit author-affiliation batch lit_h40 (12 papers)
date: 2026-11-12
auditor: Claude (fresh context; wrote only this record; headers.yaml, derived files, scripts, tests, people and registry data not edited; check run only with --dry-run, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h40/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D400-D557); format from the 2026-11-11 h38 audit; read-only comparison with earlier batches, the sibling lit_h39 and the org registry for the Hewlett Packard and Ghent / imec questions
verdict: GO for the people rebuild (no slot wrong); 84 slots audited, 76 ok, 8 imprecise (vaerenbergh2021 Hewlett Packard slots, org / unit split differs from the corpus form of the identical printed sequence), 0 wrong; one YAML fix recommended before the rebuild (F1, vaerenbergh2021 blocks 1-2, company as org); extractor calls 1, 3, 4, 5 confirmed, call 2 confirmed for the empty locality and the dropped parent wording but the org choice should follow the corpus form; checker gaps G1 (last author's further markers not bound, 4 new cases), G2 (state code accepted as locality), G3 (dropped more_orgs not detected)
---

# Lit header batch audit: lit_h40 (2026-11-12)

## Scope

Batch lit_h40 (12 papers, Optics Express and Optical Materials Express articles, all with capitals author lines; 84
author-list slots, no header-only author; 120 rows).
Restricted corpus: this record names only authors, orgs, units, cities and countries; no paper text is quoted and no
contact, street, building, postal-box or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h40 --corpus lit --codes <id> --pdf`
  (all 12; output kept in the session scratchpad only). Every author line and block is on page 1; no cover page, no
  later-page affiliation list, no prose statement. Markers legible and identical in the text and PDF layers in all 12.
- Per slot: printed name vs `compare.csv` slot and the author list printed by `show`; printed marker run vs `markers` +
  `dropped_markers`; block fields vs the print (org, unit chain, more_orgs, campus, city, country); role; locator; grade.
  All distinct (paper, marker, org, unit, org id, match basis) tuples of `header_rows.csv` read.
- Contact markers: the leading character of each masked contact line on page 1 of `text.md` (contents not printed):
  yang2024a 5 / 6, kong2025 2 / 3 / 4, ni2024 3 / 4, zhang2025d 5 then asterisk; the other 8 papers mark their contact
  line with an asterisk only. Every numeric `dropped_markers` entry with reason contact footnote is right. The daggers in
  zhang2025d (Lei Zhang, Zhiyuan Gao) point to a printed equal-contribution line and are symbol marks (no entry needed).
- Missed blocks: cue scan of the whole `text.md` of all 12 (now with / at, present / current address or affiliation,
  currently, presently, is / are / was / were (also / now) with, also with, on leave, visiting, formerly, deceased,
  permanent address, affiliat-). 4 hits (kong2025 p.2, ni2024 p.5, vaerenbergh2021 p.6, gordillo2019 p.4), all body
  text. No present address, prose statement or later-page affiliation list. No missed block.
- Claims tested with probes on scratch copies of the batch (`probes/probe.py` in the session scratchpad; one scratch
  `LIT_BASE` per probe; derived files written only there). md5 of every repo batch file identical before and after the
  audit.
- Stamp: `check_stamp.txt` matches `headers.yaml` (sha256 195f00a3...).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h40 | 12 / 12 | 84 | 76 | 8 | 0 |

- Rows 120 (all grade A: printed 107, single 13; primary 103, additional 17; all locators p.1 header); recorded 84,
  no_header 0; papers ok 12, partial 0, unreadable 0; `author_list_differs` 0; explicit slots 1 (vaerenbergh2021 #9,
  needed: probe V3); present addresses 0; prose blocks 0; `order_differs` false on every slot; multi-affiliation slots
  15; 14 unmapped org strings.
- Imprecise: vaerenbergh2021 #1-#4 and #6-#9 (8 slots on blocks 1-2): org Hewlett Packard Labs with unit LSIP Lab,
  while the identical lab-then-company sequence is recorded everywhere else with the company as org (question 2, F1).
  Person, place, country and markers are right on all 8.
- Per paper (slots / rows / rating): yang2024a 4 / 5 ok; billet2022 11 / 35 ok; kong2025 6 / 6 ok; ni2024 8 / 8 ok;
  xu2025a 7 / 7 ok; li2024b 7 / 14 ok; li2021a 5 / 7 ok; wu2025 7 / 7 ok; vaerenbergh2021 9 / 10 (8 imprecise, 1 ok);
  gordillo2019 6 / 7 ok; zhang2025d 8 / 8 ok; tian2019 6 / 6 ok.

### Per-slot field counts (84 slots)

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (84) | 84 | 0 | 0 |
| markers + dropped_markers (84) | 84 | 0 | 0 |
| blocks (org / unit / campus / locality / country) (84) | 76 | 8 (vaerenbergh2021 org / unit split) | 0 |
| prose blocks | n/a (none printed) | | |
| present addresses | n/a (none printed) | | |
| locators (84) | 84 | 0 | 0 |

## Per-paper findings

- yang2024a (4): marker runs 1 / 2 / 1,5 / 3,4,6 (last name split across two lines). Blocks Xidian University + School
  of Optoelectronic Engineering, Xi'an; Lanzhou University + School of Physical Science and Technology, Lanzhou; Beijing
  University of Posts and Telecommunications with two separate blocks (School of Integrated Circuits; State Key
  Laboratory of Information Photonics and Optical Communications), Beijing; all CN (provinces after the city not
  recorded, D288). 5 and 6 = contact lines (verified). ok.
- billet2022 (11): marker runs 1,2,3,* / 1,2,3 / 4 / 4 / 5 x4 / 1,2 / 3 / 1,2. Block 1 Ghent University + more_orgs IMEC
  + unit Photonics Research Group, Department of Information Technology, Ghent, BE; the block then repeats the group with
  the dash-joined Ghent University-IMEC and Ghent, Belgium, without a marker of its own: not recorded (question 1). Block
  2 Ghent University + Center for Nano- and Biophotonics (NB-Photonics), Ghent; block 3 Université libre de Bruxelles +
  OPERA-Photonique, Brussels; all BE. Block 4 Université Rennes + more_orgs INSA Rennes, CNRS, Institut FOTON, Rennes,
  FR (UMR number not copied; same form as ofc_h01, Institut FOTON printed last as a further org, D285). Block 5 Centre de
  Nanosciences et de Nanotechnologies (C2N) + CNRS + Université Paris Saclay, Palaiseau, FR. List #8 G. Beaudoin, #9
  Günther Roelkens, #10 François Léo vs the capitals: automatic. ok.
- kong2025 (6): one block printed with marker 1 (`printed`, D285): Tsinghua University + Department of Electronic
  Engineering, Beijing, CN (postal code printed before the city, not recorded). Runs 1 x3, 1,2 / 1,3 / 1,4 with 2-4 =
  contact lines (verified). ok.
- ni2024 (8): runs 1,3 / 1 x5 / 2,4 / 1; 3 and 4 contact lines. Blocks Nanjing University of Science and Technology +
  School of Electronic and Optical Engineering, Nanjing; Hebei University + the centre / provincial centre / college
  chain (identical to zhang2025d block 1 and the earlier Hebei requests), Baoding; both CN. #5 printed YING QIAN, list
  Ying Ping Qian: automatic match (dropped second given name), same class as hu2020 #4 / lin2023 #6 (question 5). ok.
- xu2025a (7): single unmarked block (`single`, authors `[]`; asterisk = corresponding author): Zhejiang University +
  State Key Laboratory of Extreme Photonics and Instrumentation, College of Optical Science and Engineering, Hangzhou,
  CN. List #6 Daoxin Dai A matched automatically to DAOXIN DAI (question 4). ok.
- li2024b (7): every author 1,2 (Pei Yuan 1,2,*). Two Beijing Information Science & Technology University blocks with
  their own units (ministry key laboratory; Beijing laboratory of optical fiber sensing), Beijing, CN. ok.
- li2021a (5): runs 1 / 1,* / 2,3 / 1 / 1,2. Block 1 Xi'an Jiaotong University with the ministry key laboratory and the
  Shaanxi key lab joined by and before the school, copied as one contiguous unit; block 2 Xi'an Institute of Optics and
  Precision Mechanics, Chinese Academy of Sciences (CAS in the printed name, contract example); block 3 Xi'an Sino
  Huaxin Measurement & Control Co., Ltd.; all Xi'an, CN. ok.
- wu2025 (7): runs 1 / 1,* / 1 x3 / 2 / 1. Beijing University of Posts and Telecommunications + School of Electronic
  Engineering, Beijing; Second Institute for Wuhan Ship Development & Design, Wuhan; both CN. ok.
- vaerenbergh2021 (9): runs 1,* / 2 / 2 / 2 / 3 / 2 / 2 / 2 / 2. Block 1 prints LSIP Lab, Hewlett Packard Labs, HPE
  Belgium, Diegem, Belgium; block 2 LSIP Lab, Hewlett Packard Labs, Hewlett Packard Enterprise, then only the state and
  USA (no city: `locality: ""` right, D288; country US right). Recorded org Hewlett Packard Labs + unit LSIP Lab on both
  (rows map to `org_hewlett_packard_labs`): imprecise, question 2 / F1. Block 3 Univ. Grenoble Alpes + structured
  more_orgs CEA with unit LETI, Grenoble, FR: same form as the committed lit_h01 / h07 / h10 / h14 / h20 / h21 blocks.
  #8 MARCO FIORENTINO matched automatically to list Marco Fiorentino B (question 4); #9 RAY BEAUSOLEIL `slot: 9`
  (question 3). Markers, names, places right on all 9.
- gordillo2019 (6): runs 1 x2 / 1,2 / 1 / 1 / 1,*. Columbia University + Department of Electrical Engineering, New York,
  US (state not recorded); National Chiao Tung University + Department of Photonics and Institute of Electro-Optical
  Engineering, Hsinchu, TW (Taiwan printed as the place, D249). #6 MICHAL LIPSON vs list Michal F. Lipson: automatic
  (missing middle initial, distinctive family name). ok.
- zhang2025d (8): runs 1,dagger / 1,dagger / 1 / 2 / 1 / 3 / 4,5 / 1,*; 5 = contact line (verified). Blocks Hebei
  University (chain as ni2024), Baoding; Fuzhou University + School of Physics and Information Engineering, Fuzhou;
  Northeastern University at Qinhuangdao + Hebei Key Laboratory of Micro-Nano Precision Optical Sensing and Measurement
  Technology, Qinhuangdao (question 3 below as call 3); Southeast University + national research center + school,
  Nanjing (`org_southeast_university`); all CN. ok.
- tian2019 (6): single unmarked block (asterisk = corresponding author): Beijing University of Posts and
  Telecommunications + Key Laboratory of Information Photonics and Optical Communications, Beijing, CN. ok.

## Extractor calls (verified against the page)

1. billet2022 block 1. The block prints the group and department, then Ghent University and IMEC joined by a space, then
   Ghent and Belgium, then a repeat of the group with the dash-joined form and Ghent, Belgium, all under marker 1 with no
   second marker. Recorded Ghent University + more_orgs IMEC (rows `org_ghent_university` and `org_imec` by exact name).
   Probe B1 (one string Ghent University IMEC, no more_orgs): 0 errors and the row maps by alias to the same two ids,
   so both readings give the same people links. Space-joined is neither the D426 dash form nor the D466 comma form; the
   split reading equals lit_h01 / h25 committed Ghent University + imec blocks. Leaving the repeat out is right: it has
   no marker, adds no org, unit or place, and a second marker-1 block would duplicate rows. Recommendation: accept as
   recorded; no change.
2. vaerenbergh2021 blocks 1-2. Verified: the printed order is lab, Hewlett Packard Labs, company (HPE Belgium in block
   1, Hewlett Packard Enterprise in block 2); block 2 prints no city (state code and postal text only), so `locality:
   ""` is required (D288); country US printed. Org choice: the identical lab-then-company sequence is recorded with the
   company as org and Hewlett Packard Labs in the unit in lit_h04 tossoun2019, lit_h16 tossoun2024, ofc_h13 Th2A.29 and
   the sibling lit_h39 zeng2019 (all `org_hewlett_packard_enterprise`); the corporate-lab form is the corpus convention
   (Nokia + Bell Labs, Applied Materials + Varian Semiconductor D521, IBM Research + Watson). The only org Hewlett
   Packard Labs record (ofc_h01 M1G.3) prints no company, so the note's "as in OFC" holds only for that form.
   `org_hewlett_packard_labs` has no parent link in the registry, so the same people (Zhihong Huang, Marco Fiorentino,
   Raymond G. Beausoleil, under HPE in tossoun2019 / zeng2019 / tossoun2024 / cheung2023 / Th2A.29) would sit under
   two unlinked HP ids. The sibling h39 audit reached the same
   recommendation independently. Recommendation: F1 (company as org, lab chain as unit); probe V1 0 errors.
3. zhang2025d Northeastern University at Qinhuangdao. Verified as printed, one contiguous name before the city. The
   registry `org_northeastern_university` is the Boston university (US); probe Z1 (org Northeastern University): 0
   errors but the row maps to that homonym, a wrong org. Probe Z2 (org Northeastern University + campus Qinhuangdao):
   0 errors, unmapped. D301 targets an org followed by a printed place ("org, place"); here "at Qinhuangdao" is inside
   the printed name, and keeping it whole keeps the row unmapped (correct until the registry has the campus).
   Recommendation: accept as recorded; in the org round create the Qinhuangdao campus as its own org (CN), never an
   alias of `org_northeastern_university`.
4. D412 candidates. xu2025a #6 list Daoxin Dai A (same artefact as wang2014, bauters2013, zhang2025b, piggott2015) and
   vaerenbergh2021 #8 list Marco Fiorentino B (same artefact as lit_h39 zeng2019 #5). Both printed names are right and
   matched automatically; probe V6 (`slot: 0` for Fiorentino) fails (D302), so no YAML workaround exists.
   Recommendation: add both to the D412 author-list correction file (Daoxin Dai A -> Daoxin Dai, Marco Fiorentino B ->
   Marco Fiorentino); rows stay as recorded (committed precedent).
5. vaerenbergh2021 slot 9 RAY BEAUSOLEIL / Raymond G. Beausoleil. Probe V3 (no `slot`): 2 errors (0 candidates, slot 9
   unmatched), so the explicit slot is required. D287 allows nicknames whose initials agree (Drew / Andrew class); the
   family name is distinctive, the list holds one Beausoleil, printed and list positions agree (9 of 9), and the same
   person is printed as Raymond G. Beausoleil in ofc Th2A.29 under the same company. Recommendation: accept; the list form
   is the fuller name, so no D412 entry; optional D426 review-list entry (nickname slot).

## Fixes (exact YAML edits)

F1 (recommended before the rebuild; imprecise, not wrong). In `lit:vaerenbergh2021` replace blocks 1 and 2 with:

```yaml
    - {marker: "1", basis: printed, org: "HPE Belgium", unit: "LSIP Lab, Hewlett Packard Labs", locality: "Diegem", country: "BE"}
    - {marker: "2", basis: printed, org: "Hewlett Packard Enterprise", unit: "LSIP Lab, Hewlett Packard Labs", locality: "", country: "US"}
```

and in its note replace the sentence on blocks 1 and 2 with: blocks 1 and 2 print LSIP Lab and Hewlett Packard Labs
before the company (HPE Belgium in block 1, Hewlett Packard Enterprise in block 2): company as org, lab chain as unit,
as tossoun2019, tossoun2024, zeng2019 and ofc Th2A.29; block 2 prints only the state and USA, no city (locality empty).
Probe V1: 0 errors, 1 warning (the expected explicit slot); block 2 rows map to `org_hewlett_packard_enterprise`, block
1 (#1 only) becomes unmapped until the org round adds HPE Belgium (lit-scoped subsidiary alias or child of
`org_hewlett_packard_enterprise`). Rows stay 120.

No other slot, marker, block field, locator or note needs a change.

## Open questions (with recommendation)

1. billet2022 block 1 (call 1): accept Ghent University + more_orgs IMEC; same ids as the one-string form (probe B1);
   repeated dash-joined line correctly left out. Recommended: yes, no change.
2. vaerenbergh2021 org form (call 2): apply F1 now; in the org round set `org_hewlett_packard_labs` parent to
   `org_hewlett_packard_enterprise` and add HPE Belgium. Rule for later batches: when a company is printed after the
   lab, org = the printed company, unit = the lab chain; org Hewlett Packard Labs only when no company is printed.
   Recommended: yes (2 blocks to change, against 4 lab-then-company records the other way).
3. zhang2025d (call 3): keep Northeastern University at Qinhuangdao whole, no campus field; never alias to the Boston id
   (probe Z1 shows the homonym trap). Recommended: yes.
4. D412 (call 4): xu2025a #6 and vaerenbergh2021 #8 to the correction file. Recommended: yes, no YAML change.
5. ni2024 #5 YING QIAN / Ying Ping Qian (automatic, dropped second given name): D426 review list with hu2020 #4 and
   lin2023 #6 (D550). Recommended: yes, low priority.
6. vaerenbergh2021 #9 (call 5): keep `slot: 9`. Recommended: yes.
7. G1 (below): billet2022 #11, kong2025 #6, yang2024a #4 and li2021a #5 are new test cases for the D442 / D546 / D557
   last-author marker gap. Recommended: add to that test list; YAML already exact.

## Unmapped org names (org round, no YAML change)

| printed org (unit) | place | proposal |
|---|---|---|
| Fuzhou University (School of Physics and Information Engineering) | Fuzhou, CN | new org (already requested) |
| Hebei University (centre / provincial centre / college chain) | Baoding, CN | new org (already requested) |
| INSA Rennes | Rennes, FR | new org (no earlier request) |
| Institut FOTON | Rennes, FR | already requested; candidate alias to `org_fonctions_optiques_pour_les_technologies_de_linformation` |
| Nanjing University of Science and Technology (School of Electronic and Optical Engineering) | Nanjing, CN | new org (already requested) |
| National Chiao Tung University (department and institute) | Hsinchu, TW | already requested; predecessor of `org_national_yang_ming_chiao_tung_university` (org-round decision) |
| Northeastern University at Qinhuangdao (Hebei key laboratory) | Qinhuangdao, CN | new campus org; never `org_northeastern_university` (question 3) |
| Second Institute for Wuhan Ship Development & Design | Wuhan, CN | new org (no earlier request) |
| Univ. Grenoble Alpes | Grenoble, FR | already requested; alias to `org_universite_grenoble_alpes` |
| Université Paris Saclay | Palaiseau, FR | already requested |
| Université Rennes | Rennes, FR | already requested; alias to `org_universite_de_rennes` |
| Xi'an Institute of Optics and Precision Mechanics, Chinese Academy of Sciences | Xi'an, CN | alias to `org_xian_institute_of_optics_and_precision_mechanics` |
| Xi'an Jiaotong University (key laboratory chain, school) | Xi'an, CN | new org (no earlier request) |
| Xi'an Sino Huaxin Measurement & Control Co., Ltd. | Xi'an, CN | new org (no earlier request) |

After F1: HPE Belgium (LSIP Lab, Hewlett Packard Labs), Diegem, BE joins the list (subsidiary of
`org_hewlett_packard_enterprise`).

## Privacy and as-printed scan

- Grep over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`, `papers.csv` and `check_stamp.txt`
  (paper ids removed) for contact / URL patterns, street, road, avenue, building, room, postal-box and Cedex words and
  digit runs of 4 or more: 0 hits apart from the YAML header comment that says no street or postal text is recorded.
  Notes name only the kinds of omitted text (postal codes, provinces, states), never their values.
- As printed (kept, correct): Université libre de Bruxelles (lower-case l / de); Université Rennes and Université Paris
  Saclay without the de / hyphen of the registry names; Univ. Grenoble Alpes abbreviation; Beijing Information Science &
  Technology University with the ampersand; Xi'an with a straight apostrophe (the print uses a curly one; the checker
  folds punctuation). No `skip_prefix`, `skip_between`, `continued` or campus field in this batch.

## Commands (2026-11-12, log times)

| Command | Result |
|---|---|
| `check lit_h40 --corpus lit --dry-run` 23:22:06 (pid 31331) | 0 errors, 1 warning (vaerenbergh2021 explicit slot 9); slots 84, recorded 84; rows 120 (grade A 120; primary 103, additional 17; printed 107, single 13); papers ok 12; multi-affiliation slots 15; present addresses 0; 14 unmapped org strings |
| `show lit_h40 --corpus lit --codes <id> --pdf`, all 12 | headers and author lists read (scratchpad only) |
| `show` for lit_h04 tossoun2019, lit_h16 tossoun2024, lit_h39 zeng2019 (lit) and `show ofc_h13 --codes Th2A.29`, `ofc_h01 --codes M1G.3` | Hewlett Packard printed forms compared (scratchpad only) |
| `probes/probe.py` on scratch copies, 23:23:02-23:27:38 | below; repo batch files md5 unchanged; each probe check writes its usual log files under `logs/` (prefix `lit_headers_check_lit_p`) |

| probe | change | result | reading |
|---|---|---|---|
| BASE | unchanged copy | 0 errors, 1 warning | baseline |
| V1 | vaerenbergh2021 blocks 1-2 as F1 | 0 errors; block 2 -> `org_hewlett_packard_enterprise`, block 1 unmapped | F1 valid |
| V2 | block 2 only as F1 | 0 errors | same |
| V3 | RAY BEAUSOLEIL without `slot: 9` | 2 errors (0 candidates, slot 9 unmatched) | explicit slot required |
| V4 | Beausoleil marker 3 instead of 2 | 2 errors | last author's single marker bound |
| V5 | block 2 locality CA | 0 errors | G2: state code accepted as locality |
| V6 | MARCO FIORENTINO `slot: 0` | 2 errors (D302) | no YAML workaround for the D412 artefact |
| B1 | billet2022 org Ghent University IMEC, no more_orgs | 0 errors; alias to `org_ghent_university;org_imec` | same ids as recorded |
| B2 | billet2022 block 1 without more_orgs IMEC | 0 errors | G3: dropped more_orgs not detected |
| B3 | Bart Kuyken (last) markers 1 only | 0 errors | G1 |
| B4 | Maximilien Billet markers 1,2 only | 2 errors | markers bound (first author) |
| Z1 | zhang2025d org Northeastern University | 0 errors; maps to the Boston id | homonym trap; keep full name |
| Z2 | org Northeastern University + campus Qinhuangdao | 0 errors; unmapped | alternative, not needed |
| Z3 | Jinbiao Xiao without dropped 5 | 2 errors | contact marker bound |
| K1 | Yidong Huang (last) without dropped 4 | 0 errors | G1 |
| K2 | Yidong Huang dropped 5 instead of 4 | 0 errors | G1 |
| Y1 | Lei Zhang (last, name split) without dropped 6 | 0 errors | G1 |
| Y2 | Hanlin Qin without dropped 5 | 2 errors | contact marker bound |
| N1 | Shengbao Wu (ni2024) without dropped 4 | 2 errors | contact marker bound |
| L1 | Qihang Duan markers 2 only | 3 errors | markers bound |
| L2 | Xun Hou (last) markers 1 only | 0 errors | G1 |
| G1 | You-Chia Chang markers 1 only | 3 errors | markers bound |

## Checker gaps observed (scripts not edited)

- G1 Last author's markers after the first are not bound: a missing affiliation marker (billet2022 #11, li2021a #5) or a
  missing or wrong contact marker (kong2025 #6, yang2024a #4) passes with 0 errors, whether or not the name is split over
  two lines. The same authors' first marker is bound (V4). Extends the D442 / D546 / D557 last-author gap (chen2024b,
  chen2018, zhang2024 #8). YAML exact in all four.
- G2 Locality check accepts a printed state code (V5, vaerenbergh2021 block 2 locality CA passes); D288 requires an empty
  locality when only a state is printed. Related to the D557 johnson2020 locality gap. YAML exact.
- G3 A printed further org omitted from `more_orgs` is not detected (B2). YAML exact here.

## Verdict

GO. No slot carries a wrong person, city, country or marker, nothing is invented, no block is missed, and no address or
contact text is recorded. One consistency fix is recommended before the rebuild (F1: vaerenbergh2021 blocks 1-2 with
the printed company as org and LSIP Lab, Hewlett Packard Labs as unit, as the four other records of this printed
sequence); without it the rebuild is still safe (HP Labs is the printed lab, not a wrong org) but splits the same people
over two unlinked HP ids. Calls 1, 3, 4 and 5 accepted as recorded; D412 gains xu2025a #6 and vaerenbergh2021 #8.
