---
title: Fresh-context audit of the lit author-affiliation batch lit_h37 (12 papers)
date: 2026-11-11
auditor: Claude (fresh context; wrote only this record; headers.yaml, derived files, scripts, tests, people and registry data not edited; aggregate and the people build not run; check run only with --dry-run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h37/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D406-D550); format from the 2026-11-09 h35 audit
verdict: GO for the people rebuild (no slot wrong); 87 slots audited, 78 ok, 9 imprecise, 0 wrong; F1 (cao2025 block 4, parent CICT copied as more_orgs, 2 slots, -2 rows) and F2 (lin2021 block 1 locality Halle vs printed Halle (Saale), 7 slots, rows unchanged) recommended before the rebuild; moodie2024 #6 explicit slot kept (D550) and listed for D426 review; nothing applied
---

# Lit header batch audit: lit_h37 (2026-11-11)

## Scope

Batch lit_h37 (12 papers, all Optics Express research articles 2020-2025 in the same layout: author line in capitals,
numbered or single unmarked blocks printed directly under it, contact lines masked, abstract after the blocks; 87
author-list slots, no header-only author; 102 rows). Restricted corpus: this record names only authors, orgs, units,
cities and countries; no paper text is quoted and no contact, street, site, building or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h37 --corpus lit --codes <id> --pdf`
  (all 12; output kept in the session scratchpad only). All blocks are on page 1; no `--pages` needed. The PDF layer
  carries every superscript run legibly; no page render needed.
- Per slot: printed name vs `compare.csv` slot and the author list printed by `show`; printed marker run vs `markers` +
  `dropped_markers`; block fields vs the print (org, unit chain, campus, city, country); locator; parents; present
  addresses. All 35 distinct (paper, marker, org, place, org id) tuples of `header_rows.csv` read.
- Contact markers: the masked contact lines were checked in `text.md` by their leading character only (contents not
  printed). katsura2023: two contact lines led by 5 and the asterisk; papadovasilakis2022: three led by 3, 4 and the
  asterisk; papadovasilakis2023: three led by 3, 4 and 5 (no asterisk printed in that paper). Every dropped marker
  leads a contact line and no printed affiliation block carries markers 5 (katsura2023), 3-4 (papadovasilakis2022) or
  3-5 (papadovasilakis2023): `dropped_markers` with reason contact footnote is right. The other 9 papers have one
  contact line led by the asterisk. cao2025 dagger = printed equal-contribution line (symbol mark, ignored, right).
- Missed blocks: cue scan of the whole `text.md` of all 12 (now with / at, present / current address, present / current
  affiliation, currently, presently, is / are / was / were (also / now) with, also with, on leave, visiting, formerly,
  deceased, permanent address, equal contribution / contributed equally). 7 hits: cao2025 p.1 (the equal-contribution
  line) and 6 body-text matches (hammond2022, han2022, lin2021, mao2021 x2, moodie2024). No present address, prose
  statement or later-page affiliation list in any paper. No missed block.
- Precedents read in committed batches: NOIC blocks (lit_h01 hu2023, lit_h06 hu2023a, lit_h13 hu2021a, lit_h28
  chen2018, ofc_h08), Max Planck Institute of Microstructure Physics blocks (lit_h02 mu2026, lit_h11 yong2021, lit_h21
  thiessen2020, lit_h24 govdeli2025: each prints Halle alone), parenthesized localities (Frankfurt (Oder) 6, Frankfurt
  (O.) 2), Tsinghua-Berkeley Shenzhen Institute (ofc_h07), Ghent University-imec spellings (em-dash form in 2 committed
  blocks), Khalifa University (lit_h03, lit_h06, lit_h10).
- Claims and contract calls tested with dry-run probes on scratch copies of the batch (`probes/probe.py` in the session
  scratchpad, via the module's `LIT_BASE`); md5 of every repo batch file identical before and after the probes.
- Stamp: `check_stamp.txt` matches `headers.yaml` (sha256 11c504c9...). Repo batch files untouched by this audit.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h37 | 12 / 12 | 87 | 78 | 9 | 0 |

- Rows 102 (all grade A: printed 74, single 28; primary 89, additional 13; locator p.1 header on all); recorded 87,
  no_header 0; papers ok 12, partial 0, unreadable 0; `author_list_differs` 0; `slots_from_header` 0; present
  addresses 0; prose blocks 0; `order_differs` false on all 87; explicit `slot:` 1 (moodie2024 #6); 7 unmapped org
  strings.
- Imprecise by cause: parent org copied as `more_orgs` 2 (F1, cao2025 #5 #8); locality shortened from the printed city
  name 7 (F2, lin2021 #1 #3 #4 #5 #6 #9 #10). Fixable now in the YAML: 9.
- Per paper (slots / rows / rating): cao2025 9 / 14 (7 ok, 2 imprecise); chen2021a 6 / 6 ok; hammond2022 4 / 4 ok;
  han2022 4 / 7 ok; johnson2020 3 / 4 ok; katsura2023 10 / 11 ok; lin2021 10 / 12 (3 ok, 7 imprecise); mangal2021 5 /
  6 ok; mao2021 4 / 4 ok; moodie2024 14 / 14 ok; papadovasilakis2022 9 / 10 ok; papadovasilakis2023 9 / 10 ok.

### Per-slot field counts (87 slots)

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot | 87 | 0 | 0 |
| markers + dropped_markers | 87 | 0 | 0 |
| blocks (org / unit / campus / locality / country) | 78 | 9 (cao2025 #5 #8 more_orgs; lin2021 7 slots locality) | 0 |
| prose blocks | n/a (none printed) | | |
| present addresses | n/a (none printed) | | |
| locators | 87 | 0 | 0 |
| parked / unreadable | n/a (none) | | |

## Per-paper findings

- cao2025 (9; p.1 header): marker runs 1,2 / 1 / 1 / 3 / 4 / 2 / 2 / 4 / 2,3,5 as printed (dagger on authors 1-2 and
  asterisk on author 9 ignored). Block 1 Shenzhen Technology University + College of Integrated Circuits and
  Optoelectronic Chips, Shenzhen, CN (unmapped); block 2 Institute of Semiconductors, Chinese Academy of Sciences
  (parent part of the printed name) + Laboratory of Solid State Optoelectronics Information Technology, Beijing; block
  3 University College London + Department of Electronic and Electrical Engineering, London, GB (United Kingdom
  printed); block 5 University of Chinese Academy of Science as printed (alias to
  `org_university_of_chinese_academy_of_sciences`) + college unit, Beijing. Block 4: National Information
  Optoelectronics Innovation Center with China Information and Communication Technologies Group Corporation (CICT)
  printed after it, Wuhan. The YAML puts CICT in `more_orgs`, so Zhihang Liu (#5) and Xi Xiao (#8) get a second primary
  row each (`org_china_information_and_communication_technologies_group`). The identical printed block in lit_h13
  hu2021a and the ofc_h08 NOEIC block record the center alone with the parent group not copied (parent rule, OFC
  contract). Imprecise, F1. ok otherwise.
- chen2021a (6): one unmarked block (`single`, authors `[]`): National University of Singapore + Department of
  Electrical and Computer Engineering; Singapore printed only as the place after the postal code: locality Singapore,
  SG (city-state; lit_h11 / lit_h24 AMF precedent). List form Aaron James Danner vs printed AARON J. DANNER: initial
  explained, automatic. ok.
- hammond2022 (4): one unmarked block: Georgia Institute of Technology + School of Electrical and Computer
  Engineering, Atlanta, US (state code and postal code not recorded). ok.
- han2022 (4): runs 1 / 2 / 2,3 / 1,2,3. Block 1 Zhejiang University + Polytechnic Institute, Hangzhou; block 2
  Zhejiang Laboratory + Research Institute of Intelligent Networks, Hangzhou (unmapped; registry has
  `org_zhejiang_lab` "Zhejiang Lab"); block 3 Zhejiang University + College of Information Science and Electronic
  Engineering, Hangzhou. ok.
- johnson2020 (3): runs 1,2 / 1 / 1. Both blocks University of Bristol with the lab + H. H. Wills Physics Laboratory
  unit chain; neither block prints a city (street, postal code, UK only): `locality: ""` right, country GB from UK.
  Probe J1 (locality Bristol) passes with 0 errors only because the word is inside the org name: checker gap G1, not
  a reason to fill the city. Printed DÖNDÜ SAHIN vs list Dondu Sahin: accent fold, automatic. ok.
- katsura2023 (10): runs 1 / 1 / 2 / 3 / 3 / 3 / 2 / 2,4 / 3,5 / 1 as printed in the PDF layer. Makoto Okano marker 5
  = contact line (verified; no block 5 printed; probe K1 marker 5 as affiliation: 1 error). Block 1 Osaka Metropolitan
  University + Department of Physics and Electronics, Sakai, JP (unmapped); block 2 Kyoto University + Department of
  Electronic Science and Engineering, Kyoto; block 3 National Institute of Advanced Industrial Science and Technology,
  Tsukuba (prefecture not recorded); block 4 Kyoto University + Photonics and Electronics Science and Engineering
  Center, Kyoto. ok.
- lin2021 (10): runs 1 / 2 / 1 / 1,2 / 1 / 1 / 3 / 3 / 1 / 1,2 (asterisk on author 1 ignored). Block 1 Max Planck
  Institute of Microstructure Physics, place printed as Halle (Saale), recorded as Halle; the note says earlier
  batches record this institute so, but the four committed MPI blocks (mu2026, yong2021, thiessen2020, govdeli2025)
  each print Halle alone, while the corpus keeps the parenthesized official city names Frankfurt (Oder) / Frankfurt
  (O.) as printed (8 blocks). D366 locality = the city as printed (only postal designations dropped); (Saale) is part
  of the official city name, not a postal designation or a region. Probe H1 (Halle (Saale)): 0 errors, rows and
  mapping unchanged. Imprecise on the 7 slots carrying marker 1, F2. Block 2 University of Toronto + Department of
  Electrical and Computer Engineering, Toronto, CA (province not recorded); block 3 Advanced Micro Foundry Pte Ltd as
  printed, Singapore, SG (`org_amf`; the science-park site name and postal code not recorded). ok otherwise.
- mangal2021 (5): runs 1,2 / 2 / 2 / 1 / 1. Block 1 Ghent University—imec as printed (em dash; D416 (5) / D426
  dash-joined form kept; 2 committed blocks use the same em-dash form) + Centre for Microsystems Technology, Ghent, BE
  (unmapped: the registry aliases carry the hyphen and slash forms only); block 2 imec, Heverlee, BE (`org_imec`;
  street and postal code not recorded). List form Bradley W. Snyder: automatic. ok.
- mao2021 (4): one unmarked block: Tsinghua University + unit "Tsinghua-Berkeley Shenzhen Institute & Tsinghua
  Shenzhen International Graduate School" (the joint chain printed before the org, contiguous), Shenzhen, CN. Ruling:
  right. Tsinghua-Berkeley Shenzhen Institute is recorded as a Tsinghua University unit in ofc_h07; the place after the
  org is the city followed by the postal code, not a campus name (D301 not triggered; probe T1 with `campus:
  "Shenzhen"` passes but unmaps 4 rows, so no campus). No University of California org is printed, none recorded.
  List form Li-Rong Lilly Cheng vs printed LIRONG CHENG: same given name plus an unprinted English name, automatic. ok.
- moodie2024 (14): one unmarked block: Huawei Technologies Research and Development + Ipswich Research Centre, Ipswich,
  GB (UK printed; unmapped). #6 printed LU QI vs list Qi Lu at position 6: same two name parts in swapped order; the
  explicit `slot: 6` is redundant (probe M1 without it: 0 errors, 0 warnings, same slot) and is kept per D550 (h36 F1
  ruling: it documents the swap and survives a stricter D382 matcher). Rating ok (slot right); D426 review list as a
  name-order swap (song2024 #6, tao2025 #7, zhang2022b precedent). #8 printed EVA REPISO MENENDEZ vs list Eva Repiso:
  dropped second family name, automatic; #1 #5 #14 list middle initials not printed, automatic. ok.
- papadovasilakis2022 (9): runs 1,3 / 1,2 / 1 / 2,4 / 2 / 2 / 2 / 2 / 1 (asterisk on author 1 ignored). Markers 3
  and 4 = contact lines (verified; probe P1 marker 4 as affiliation: 1 error). Block 1 Khalifa University of Science
  and Technology (full name as printed) + Electrical Engineering and Computer Science Department, Abu Dhabi, AE
  (unmapped); block 2 GlobalFoundries, Malta, US (state, street and postal code not recorded). List forms Michał
  Rakowski, Abdelsalam A. Aboketaf: automatic. ok.
- papadovasilakis2023 (9): runs 1,3,4 / 1,2 / 1 / 1 / 1 / 2,5 / 2 / 2 / 1; no asterisk printed. Markers 3, 4, 5 =
  contact lines (verified). Block 1 Khalifa University (short form as printed; same as lit_h03 / h06 / h10) + department,
  Abu Dhabi, AE (unmapped); block 2 GlobalFoundries, Malta, US. ok.

## Fixes (exact YAML edits)

| # | paper, slots | rating | evidence | edit |
|---|---|---|---|---|
| F1 | cao2025 #5 (Zhihang Liu), #8 (Xi Xiao) | imprecise (extra parent row; center row right) | p.1 header block 4 prints the center, then the parent group CICT, then Wuhan; lit_h13 hu2021a prints the same block and records the center alone ("parent CICT ... not copied"), ofc_h08 likewise. Probe C1: 0 errors, rows 102 -> 100 (primary 89 -> 87), unmapped strings unchanged | block 4 `{marker: "4", basis: printed, org: "National Information Optoelectronics Innovation Center", more_orgs: ["China Information and Communication Technologies Group Corporation (CICT)"], locality: "Wuhan", country: "CN"}` -> `{marker: "4", basis: printed, org: "National Information Optoelectronics Innovation Center", locality: "Wuhan", country: "CN"}`; in `note` replace "block 4 prints National Information Optoelectronics Innovation Center and China Information and Communication Technologies Group Corporation (CICT) (two organizations)" with "block 4 prints the parent CICT after the center (not copied, as lit_h13 hu2021a)" |
| F2 | lin2021 #1 #3 #4 #5 #6 #9 #10 (block 1) | imprecise (locality string only; org and mapping right) | p.1 header block 1 prints Halle (Saale) (official city name); D366 keeps the city as printed; committed Frankfurt (Oder) / (O.) localities keep their parenthesis; committed MPI blocks print Halle alone, so the note's rationale is wrong. Probe H1: 0 errors, rows unchanged | block 1 `locality: "Halle"` -> `locality: "Halle (Saale)"`; in `note` replace "block 1 place printed as Halle (Saale), recorded as Halle (as earlier batches record this institute)" with "block 1 locality Halle (Saale) as printed (official city name, as Frankfurt (Oder) in earlier batches; earlier MPI blocks print Halle alone)" |

Any change to the YAML changes its hash: re-run `check lit_h37 --corpus lit` afterwards to refresh the stamp and the
derived files (expected: 0 errors, 0 warnings, rows 100 with F1).

## Open questions (with recommendation)

1. F1: drop the CICT `more_orgs` entry on cao2025 block 4 (parent rule; identical committed block lit_h13 hu2021a)?
   Recommended: yes. The alternative (keep CICT as a second org) would need the same change on hu2021a and ofc_h08
   for consistency; no reason found for that.
2. F2: record lin2021 locality as printed, Halle (Saale)? Recommended: yes (D366, Frankfurt (Oder) precedent). If the
   coordinator prefers the short form for grouping, keep Halle and apply only the note correction (the stated
   rationale is wrong either way).
3. moodie2024 #6 LU QI / Qi Lu: keep the redundant explicit `slot: 6` (D550) and add moodie2024 #6 to the D426 review
   list as a name-order swap. Recommended: yes. Which part is the family name is not decidable from this paper.
4. mao2021: keep Tsinghua University as org with the joint Tsinghua-Berkeley Shenzhen Institute / Tsinghua Shenzhen
   International Graduate School chain as unit, no campus (ofc_h07 precedent; D301 not triggered). Recommended: yes.
5. Checker gap G1 (below): should a locality found only inside the org / unit span count as printed? Recommended: no;
   add a check in the D382 / D412 follow-up pass. Not blocking (no committed lit_h37 row relies on it).

## Unmapped org strings (org round; no YAML change)

| org | unit | country | rows | paper | note |
|---|---|---|---|---|---|
| Ghent University—imec | Centre for Microsystems Technology | BE | 3 | mangal2021 | em-dash variant of the `joint_printed` alias pair (org_ghent_university + org_imec); unit exists as `org_centre_for_microsystems_technology` |
| Huawei Technologies Research and Development | Ipswich Research Centre | GB | 14 | moodie2024 | UK R&D entity; alias to `org_huawei` or a GB child: org-round decision |
| Khalifa University | Electrical Engineering and Computer Science Department | AE | 6 | papadovasilakis2023 | recurring (already in `org_requests.csv`, 10 rows) |
| Khalifa University of Science and Technology | Electrical Engineering and Computer Science Department | AE | 4 | papadovasilakis2022 | full-name form of the same request |
| Osaka Metropolitan University | Department of Physics and Electronics | JP | 3 | katsura2023 | not in the registry; Osaka Prefecture University is a separate open request (pilot); relation to be checked in the org round |
| Shenzhen Technology University | College of Integrated Circuits and Optoelectronic Chips | CN | 3 | cao2025 | recurring (already in `org_requests.csv`) |
| Zhejiang Laboratory | Research Institute of Intelligent Networks | CN | 3 | han2022 | alias to existing `org_zhejiang_lab` ("Zhejiang Lab") |

None of the 7 printed names is in `data/registry/organizations.csv` or `org_aliases.csv` as printed.

## Privacy and as-printed scan

- Grep over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`, `papers.csv`, `check_stamp.txt` and
  this record for contact / URL patterns, street, site and building words, and digit runs of 4 or more: 0 contact or URL
  hits; street words only in notes that say such text was not recorded; digit runs only paper-id years and the stamp
  hash. No postal code, street, site or building text in any field.
- As printed (kept, correct): University of Chinese Academy of Science (singular), Ghent University—imec (em dash),
  Khalifa University in both printed forms, Advanced Micro Foundry Pte Ltd without periods, DÖNDÜ SAHIN. No
  `skip_prefix` or `skip_between` in this batch.

## Commands (2026-11-11, log times)

| Command | Result |
|---|---|
| `check lit_h37 --corpus lit --dry-run` 00:18:08 (pid 56680) | 0 errors, 0 warnings; slots 87, recorded 87; rows 102 (grade A 102; primary 89, additional 13; printed 74, single 28); papers ok 12; multi-affiliation slots 11; present addresses 0; 7 unmapped org strings |
| `show lit_h37 --corpus lit --codes <id> --pdf`, all 12 | headers and author lists read (scratchpad only) |
| `probes/probe.py` on scratch copies, dry-run, 00:18:43-00:19:19 (pid 56827) | below; repo batch files md5 unchanged; the dry-run check writes its usual log files under `logs/` |

| probe | change | result | reading |
|---|---|---|---|
| C1 | cao2025 block 4 without the CICT `more_orgs` | 0 errors; rows 100 | F1 applies cleanly |
| H1 | lin2021 block 1 locality Halle (Saale) | 0 errors; rows 102 | F2 applies cleanly |
| M1 | moodie2024 LU QI without `slot: 6` | 0 errors, 0 warnings | explicit slot redundant; kept per D550 |
| K1 | katsura2023 Okano marker 5 as affiliation | 1 error (no block) | contact marker must be dropped |
| P1 | papadovasilakis2022 Bian marker 4 as affiliation | 1 error (no block) | contact marker must be dropped |
| J1 | johnson2020 block 1 locality Bristol | 0 errors | checker gap G1: matched inside the org name; empty locality stays |
| T1 | mao2021 `campus: "Shenzhen"` | 0 errors; unmapped 7 -> 8 | campus not printed as such; would unmap Tsinghua |

## Checker gaps observed (scripts not edited)

- G1 Locality check accepts a city that occurs only inside the org or unit name of the block (johnson2020 "Bristol" in
  University of Bristol; mao2021 "Shenzhen" in the unit chain for `campus`). The check should require the place
  outside the org / unit span.
- (= h35 G1, unchanged) `strict_compatible` equal-count initials (D382); no lit_h37 slot affected.

## Verdict

GO. No slot carries a wrong person, org, city, country or marker, nothing is invented, no block is missed, and no
address or contact text is recorded. 9 slots are imprecise and fixable now: cao2025 #5 #8 carry an extra parent-org
row (F1) and lin2021's 7 MPI slots carry Halle for the printed Halle (Saale) (F2). Applying F1 and F2 before the
rebuild is recommended; the rebuild is safe either way.
