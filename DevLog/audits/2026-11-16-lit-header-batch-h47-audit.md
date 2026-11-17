---
title: Fresh-context audit of the lit author-affiliation batch lit_h47 (23 papers)
date: 2026-11-16
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only with --dry-run, probes on scratch copies; aggregate and the people build not run; no network; one read-only `git status` of the staging folder was run by mistake, nothing else touched git)
scope: data/_staging/people/lit_headers/lit_h47/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D412, D416, D426, D442, D466, D522, D546, D565, D572, D599); format from the 2026-11-15 h45 / h46 audits; read-only comparison with earlier batches (lit_h02 / h14 / h27 Joint Quantum Institute blocks, lit_h01 / h03 / h27 Centre for Quantum Technologies, lit_h28 / h34 CUDOS, lit_h31 liu2024 and lit_h43 chen2022d G6 partials, C2N blocks, Kowloon, UC San Diego campus, H. H. Wills unit chains, Ghent University-IMEC)
verdict: GO with 1 fix; 186 slots audited (160 author-list slots + 26 header slots of kasture2016 / xiong2011); 176 recorded slots, 185 ok, 1 imprecise (hickstein2019 #8 block 6, F1), 0 wrong; 10 slots correctly without rows; extractor calls verified (liu2010a unreadable, du2024 partial, slots_from_header x2, author_list_differs x2, gaafar2024 #15 slot, chen2021b marker 3, kasture2016 CUDOS unit, poulvellarie2021 block 7, xiong2011 block 4, luo2021 #6, chen2021b #2) all forced or precedent-conform
---

# Lit header batch audit: lit_h47 (2026-11-16)

## Scope

Batch lit_h47: 23 papers; 186 slots (160 author-list slots plus 26 header slots for kasture2016 (7) and xiong2011 (19) with `slots_from_header`); 225 rows.
Restricted corpus: this record names only authors, orgs, units, cities and countries; no paper text is quoted and no
contact, street, building, postal-box or postal-code text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h47 --corpus lit --codes <id> --pdf`
  (all 23; output kept in the session scratchpad `h47_audit/show/` only).
- Per slot: printed name vs the `show` author list and `compare.csv`; marker run vs text layer and PDF layer
  (identical in both layers for every paper); block fields (org, unit chain, more_orgs, campus, city, country); role;
  locator; grade. All 76 distinct (paper, org, unit, city, country, org id, match basis, locator) tuples of
  `header_rows.csv` read (225 rows).
- Symbol legends: page 1 of every paper read for asterisk / dagger / hash / arrow / letter legends; the first
  character of masked contact lines checked in `references/<id>/text.md` where a marker depended on it (chen2021b
  marker 3, bruch2018, du2024, javid2021, chen2023d, herrmann2022; only the leading symbol inspected, nothing copied).
- Probes on scratch copies (`h47_audit/probes/probe.py` in the session scratchpad: scratch `LIT_BASE`, batch name
  `lit_p47`, `cmd_check(..., dry_run=True)`). md5 of every repo batch file identical before and after the audit;
  `check_stamp.txt` matches `headers.yaml` (sha256 ab4e6ad2...).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h47 | 23 / 23 | 186 | 185 | 1 | 0 |

- Rows 225 (all grade A: printed 215, single 10; primary 179, additional 46, present address 0); recorded 176,
  no_header 10 (liu2010a #1-#4 unreadable paper; du2024 #1, #6 unreadable; timurdogan2017 #3, siddharth2024 #3, #7,
  #10 not printed in the cached version); papers ok 21, partial 1 (du2024), unreadable 1 (liu2010a);
  `slots_from_header` 2 (kasture2016, xiong2011); `author_list_differs` 2 (timurdogan2017, siddharth2024); explicit
  slots 1 (gaafar2024 #15); `order_differs` 0; multi-affiliation slots 36; 25 unmapped org strings (26 after F1).
- Per paper (slots / rows): liu2010a 4 / 0; bao2024 9 / 16; luo2021 9 / 11; bruch2018 9 / 9; hwang2023 10 / 10;
  gaafar2024 17 / 21; zhao2020 4 / 5; luo2018 5 / 6; hickstein2019 10 / 15; du2024 6 / 5; chen2023d 6 / 7;
  chen2021b 7 / 7; yan2021 5 / 5; timurdogan2017 4 / 3; lorenzen2025 5 / 6; yang2010a 5 / 5; kasture2016 7 / 9;
  xiong2011 19 / 26; herrmann2022 6 / 6; che2024 10 / 11; javid2021 6 / 7; poulvellarie2021 10 / 18;
  siddharth2024 13 / 17.

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (186) | 186 | 0 | 0 |
| markers (178 header authors; du2024 #1 / #6 unreadable) | 178 | 0 | 0 |
| header position (178) | 178 | 0 | 0 |
| blocks (org / unit / campus / locality / country) (176 authors with rows) | 175 | 1 (hickstein2019 #8 block 6, F1) | 0 |
| recorded blocks (73) | 72 | 1 (hickstein2019 block 6) | 0 |
| unrecorded printed blocks (3: liu2010a 1, 2; du2024 1) | 3 forced | 0 | 0 |
| present addresses (0 printed) | n/a | 0 | 0 |
| locators (all blocks; yang2010a `p.1 footnote`) | all | 0 | 0 |
| notes (23) | 22 | 1 (hickstein2019, changes with F1) | 0 |

## Per-paper findings

- liu2010a (4; unreadable): both marked blocks (Columbia University + Department of Electrical Engineering, New York;
  IBM Thomas J. Watson Research Center, Yorktown Heights; US) are printed above the title, before the author line, in
  both layers. Probe L1: 6 errors (blocks not after the author line; author 2 also carries the printed suffix Jr.).
  Forced; same gap as hu2022 / lukin2019 (D550). Note values match the page; no building or street value in the
  note. ok.
- bao2024 (9; printed): 7 blocks read in both layers: ECNU + XXL / school chain; ECNU + State Key Laboratory of
  Precision Spectroscopy; SIOM, CAS (org form identical to lit_h46 wang2024c) + state key laboratory / CAS center
  unit; Shanxi University, Taiyuan; Shandong Normal University, Jinan (block prints People's Republic of China);
  Hefei National Laboratory, Hefei; ECNU + joint research center (lit_h46 zhou2024 form). All CN. Ya Cheng 1-7,
  Rui Bao 1,2 exact; probe B1 (Cheng without 7) fails. ok.
- luo2021 (9; printed): Nankai University + MOE key laboratory / TEDA institute / school chain, Tianjin; Shanxi
  University, Taiyuan (province after the city, not recorded); Shandong Normal University, Jinan; CN. #6 printed
  Fang Bo vs list Bo Fang: matched automatically (no warning; probe LU1 with explicit slot 6 is neutral). Same person
  (given / family order swapped in the list). ok.
- bruch2018 (9; printed): Yale University + Department of Electrical Engineering, New Haven, US; Institute of
  Semiconductors, Chinese Academy of Sciences + R&D center, Beijing, CN. Asterisk on Tang leads to a contact line.
  ok.
- hwang2023 (10; printed): Stanford University + E.L. Ginzton Laboratory, Stanford, US; NTT Research, Inc. + Physics
  & Informatics Laboratories, Sunnyvale, country empty (block prints a state and postal code only; probe HW1 with US
  fails). #3 Taewon / Tae-Won Park and #9 Martin M. / M. M. Fejer automatic. ok.
- gaafar2024 (17; printed): DESY, Hamburg; University of Twente + Integrated Optical Systems, MESA+ chain, Enschede
  (4 blocks in lit_h01 / h22 / h28 / h36 use this unit form); LIGENTEC SA, Ecublens, CH (site name and street not recorded; the country
  printed before the city is not a place); Max-Planck Institute for the Science of Light, Erlangen; FAU
  Erlangen-Nürnberg + Department of Physics, Erlangen; Universität Hamburg + Department of Physics, Hamburg. Single
  asterisk = equal-contribution legend; double asterisk (Herr) has no affiliation use. #15 see call 4. ok.
- zhao2020 (4; printed): University of California + campus San Diego + ECE, La Jolla, US (lit_h01 / h10 / h18 blocks use
  campus San Diego with La Jolla; probe Z1 shows the campus is precedent, not forced); TU Dresden + Institut für
  Angewandte Physik, Dresden, DE. Rüsing 1,2 exact. ok.
- luo2018 (5; printed): University of Rochester + Institute of Optics / ECE, Rochester, country empty (no country
  printed; state code only). ok.
- hickstein2019 (10; printed, closing-parenthesis markers): NIST (full name) + Time and Frequency Division, Boulder;
  University of Colorado + campus Boulder + department (blocks 2, 5, 7); Johns Hopkins + ECE, Baltimore; NIST
  (acronym) + CNST, Gaithersburg; all US (printed U.S.A.). Marker a = contact line (legend on page 1; probe H2 bound).
  Smalyukh 2,5,6, Diddams / Papp 1,7 exact. Block 6: fields correct, structure imprecise (F1).
- du2024 (6; partial, capitals): blocks 2-5 exact (SUTD + group, Singapore; Institute of Microelectronics with the
  parent A*STAR not copied, Singapore, maps to org_astar_ime; Technology Innovation Institute + Quantum Research
  Centre, Abu Dhabi, AE; NUS + Department of Physics, Singapore). Block 1 see call 2. ok.
- chen2023d (6; printed): University of Arizona + J. C. Wyant College of Optical Sciences / Department of Physics,
  Tucson, US. Pao-Kang Chen 1,2. Asterisk legend is a contact line at the end of the paper. ok.
- chen2021b (7; printed): City University of Hong Kong + department & state key laboratory unit, Kowloon, HK (12
  earlier CityU blocks use locality Kowloon; probe C3 neutral); Tianjin University + three-part chain, Tianjin, CN.
  Dagger = equal contribution (legend printed). #5 marker 3 and #2 see calls 7 and 10. ok.
- yan2021 (5; single): one unmarked block (Shanghai Jiao Tong University + state key laboratory / school chain,
  Shanghai, CN); the 1 on every author dropped (D285; probe Y1 with a marked block fails). a) / b) are contact lines
  (legends on page 1); asterisk legend (equal contribution) printed on page 4. ok.
- timurdogan2017 (4; printed, single block with marker 1): MIT + Research Laboratory of Electronics, Cambridge, US.
  See call 6. ok.
- lorenzen2025 (5; printed, capitals): DESY + CFEL unit, locality empty (block prints only the country; probe LO1
  with Hamburg fails); University of Twente chain, Enschede, NL; Universität Hamburg + Department of Physics,
  Hamburg, DE. Hash and asterisk lead to contact lines. FRANZ X. KÄRTNER matches the list form here. ok.
- yang2010a (5; single, `p.1 footnote`): University of Twente + Integrated Optical Micro Systems Group, MESA+ chain,
  Enschede, NL; footnote below the abstract (Springer style). All initials agree with the list (Jun Yang, Kerstin
  Wörhoff, Feridun Ay, Markus Pollnau). ok.
- kasture2016 (7; printed, slots from header): Griffith University + Centre for Quantum Dynamics, Nathan; RMIT
  University + CUDOS / school chain, Melbourne; Griffith University + Institute for Glycomics, Southport; Griffith
  University + Queensland Micro and Nanotechnology Centre, Nathan; all AU. See calls 5 and 8. ok.
- xiong2011 (19; printed, slots from header): CUDOS (org, country only), University of Sydney + IPOS / School of
  Physics (state, no city), Macquarie University + MQ Photonics / department (state, no city), University of Bristol
  chain, Bristol, GB (printed UK), ANU + Laser Physics Centre, Canberra, Heriot-Watt + school, Edinburgh, GB, Delft
  University of Technology + Kavli Institute, Delft, NL. All 19 marker runs exact (line breaks inside two names
  checked). See calls 5 and 9. ok.
- herrmann2022 (6; printed, period markers): Stanford University + Ginzton Laboratory and Department of Applied
  Physics / of Electrical Engineering, Stanford, US. Asterisk on Herrmann leads to a contact line on a later page.
  ok.
- che2024 (10; printed): Nokia Bell Labs, Murray Hill, US; Swiss Federal Institute of Technology Lausanne (EPFL) +
  Institute of Physics, Lausanne, CH; University of Central Florida + CREOL, The College of Optics and Photonics,
  Orlando, US. Dagger / asterisk legends printed. Blanco-Redondo 1,3 exact. ok.
- javid2021 (6; printed): University of Rochester + Institute Of Optics (capital O as printed) / ECE, Rochester, US.
  Up arrow = equal contribution (legend printed). ok.
- poulvellarie2021 (10; printed): ULB + OPERA-Photonique, Brussels, BE; Ghent University-IMEC (dash-joined, D416 /
  D426; maps to Ghent University + imec) + Photonics Research Group / NB-Photonics, Ghent, BE; Université d'Angers +
  Laboratoire de Photonique d'Angers EA 4464 (laboratory code, not a postal code), Angers; Thalès Research and
  Technology (accent as printed, D282), Palaiseau; C2N + CNRS, Université Paris Sud, Université Paris Saclay,
  Palaiseau (committed C2N form); block 7 see call 11; FR. Asterisk on author 1 leads to a contact line. ok.
- siddharth2024 (13 list, 10 printed; printed): EPFL full name + Laboratory of Photonics and Quantum Measurements,
  Lausanne, CH; EPFL acronym + Center of Quantum Science and Engineering, Lausanne, CH; Purdue University + OxideMEMS
  Lab, West Lafayette, US. Asterisk / dagger on authors 9 and 10 have no legend on page 1. See call 6. ok.

## Extractor calls (verified)

1. liu2010a unreadable: forced (probe L1, 6 errors). Add to the blocks-above-the-author-line checker gap list with
   hu2022 and lukin2019.
2. du2024 partial. Block 1 prints a street address between Centre for Quantum Technologies and National University
   of Singapore (both layers). Probe D1 (NUS + unit CQT, authors 1 and 6 readable): 2 errors (unit and org not
   contiguous). Probe D2 (Ling readable with only 5): 2 errors (marker run). Probe D3 (CQT as its own org + NUS in
   `more_orgs`) passes, but lit_h01, h03 and h27 record CQT as an NUS unit (3 blocks), so D3 would be a one-off
   structure. Partial is the precedent form (lit_h31 liu2024, lit_h43 chen2022d: an author whose other block is
   recordable keeps that marker and is unreadable). Keep; see question 1.
3. slots_from_header (kasture2016, xiong2011): `show` prints no author list for either; probes K2 / X1 fail without
   the flag. Correct.
4. gaafar2024 #15: printed Franz X. Kärtner, list Franz X. Käertner (the list form inserts an e after the umlaut;
   the same person is printed with the list's own form Kärtner in lorenzen2025). Probe G1 without the slot: 2
   errors. D287 misspelling, explicit slot correct; the checker's single warning is this slot.
5. kasture2016 block 2 CUDOS in RMIT's unit chain. Probe K1 (ARC Centre for Excellence CUDOS as org + structured
   RMIT University / School of Engineering) also passes. The centre is printed first in the chain before the school
   and the university, which the corpus records as unit (state key laboratories before a university; Aalto QTF
   Centre of Excellence, 2 blocks); lit_h28 douglass2018 records CUDOS as a further org only because it is printed
   after the university. Keep the unit form; see question 2.
6. author_list_differs: timurdogan2017 prints 3 authors (slot 3 Matthew J. Byrd appears nowhere in the cached text);
   siddharth2024 prints 10 (slots 3, 7, 10 absent from page 1). Probes T1 / S1 fail without the flag. Correct; no
   rows for the unprinted slots.
7. chen2021b marker 3 (De-Long Zhang 2,3): no block 3 is printed; the first masked contact line below the
   equal-contribution legend begins with 3 (leading character checked in text.md). `dropped_markers` contact
   footnote is correct; probe C1 (without it) 2 errors.
8. CUDOS blocks: xiong2011 block 1 prints CUDOS alone with only the country, so it must be the org (lit_h34 form);
   kasture2016 differs only because of its printed position (call 5).
9. xiong2011 block 4: the unit is printed across a line break with no separator between H. H. Wills Physics
   Laboratory and Dept. of Electrical and Electronic Engineering; recorded without the comma, as printed; the
   lit_h03 / h37 University of Bristol blocks also keep H. H. Wills Physics Laboratory inside the unit chain. Probe X3 (unit cut after the laboratory) fails (not contiguous with the org); X2 (comma added)
   is neutral. Blocks 2 and 3 locality empty is right: only a state and postal code are printed (probe X4 with
   Sydney passes only because Sydney is inside the org name, not a printed city).
10. chen2021b #2: printed Qing Xu, list Qing Quan Xu; automatic match (dropped second given-name syllable). Probe C2
    (slot 0) fails (D302). Correct; common family name, so listed for the D426 review list (question 3).
11. poulvellarie2021 block 7 prints Université de Paris first, then C2N: org + `more_orgs` follows the printed order;
    probe P1 (C2N first) fails (block start). Correct.
12. hickstein2019 block 6: see F1.

## Fixes (exact YAML edits)

F1 (block structure; precedent). hickstein2019 block 6 prints Renewable and Sustainable Energy Institute, NREL and
University of Colorado, Boulder: a joint institute of two organizations. The corpus records this pattern as three
organizations with the joint institute as org and no campus on the joint block (Joint Quantum Institute with NIST
and University of Maryland: lit_h02, lit_h14, lit_h27; joint units D466). The extractor made the institute a unit of
NREL only. In `lit:hickstein2019` replace

```yaml
    - {marker: "6", basis: printed, org: "NREL", more_orgs: ["University of Colorado"], unit: "Renewable and Sustainable Energy Institute", locality: "Boulder", country: "US"}
```

with

```yaml
    - {marker: "6", basis: printed, org: "Renewable and Sustainable Energy Institute", more_orgs: ["NREL", "University of Colorado"], locality: "Boulder", country: "US"}
```

and in the same paper's note replace

```yaml
block 6 prints the Renewable and Sustainable Energy Institute before NREL and University of Colorado (unit + two organizations; the campus is not attached to the further organization)
```

with

```yaml
block 6 prints the Renewable and Sustainable Energy Institute with NREL and the University of Colorado (recorded as three organizations, no campus on the joint block, as the Joint Quantum Institute blocks)
```

Rows 225 -> 226 (Smalyukh block 6: Renewable and Sustainable Energy Institute, NREL, University of Colorado; the
NREL row loses the unit); unmapped strings 25 -> 26. Probe FIX_all (F1 on a scratch copy): 0 errors, 1 warning
(gaafar2024 explicit slot). Probe H3 (University of Colorado + campus Boulder as org, NREL in more_orgs, institute
as unit) also passes but makes the joint institute a CU unit: not recommended.

## Open questions (with recommendation)

1. du2024 block 1: add to the D426 G6 re-record list (values in the paper note: Centre for Quantum Technologies,
   National University of Singapore, Singapore, SG; authors 1 and 6). Recommended: yes; do not switch to the D3
   one-off org form.
2. kasture2016 CUDOS: keep as RMIT unit (call 5); the org round may alias ARC Centre for Excellence CUDOS forms to
   the CUDOS org string of xiong2011 / lit_h28 / lit_h34 if a CUDOS org is created. Recommended: keep YAML.
3. D412 correction file: gaafar2024 #15 (Käertner list form). D426 review list: chen2021b #2 (Qing Quan Xu / Qing
   Xu), luo2021 #6 (Bo Fang / Fang Bo order swap); both automatic matches. Recommended: add.
4. G1 test list (last author's further markers not bound): gaafar2024 #17 Herr without 6 (probe G2), javid2021 #6
   Lin without 2 (J1), siddharth2024 #10 Kippenberg without 2 (SI1) all pass; a non-last author is bound (SI2
   Riemensberger, 2 errors). Records are correct; checker gap only. Recommended: add the three cases.
5. liu2010a to the blocks-above-the-author-line gap list (with hu2022, lukin2019). Recommended: yes.

## Unmapped org names (org round, no YAML change)

| printed org (unit) | place | proposal |
|---|---|---|
| Australian National University (Laser Physics Centre) | Canberra, AU | new org (lit_h46 also has The Australian National University) |
| Centre for Ultrahigh-bandwidth Devices for Optical Systems (CUDOS) | AU | new org (also lit_h28 / h34) |
| Deutsches Elektronen-Synchrotron DESY (2 unit forms) | Hamburg / -, DE | new org |
| FAU Erlangen-Nürnberg (Department of Physics) | Erlangen, DE | alias to org_friedrich_alexander_universitat_erlangen_nurnberg |
| Griffith University (3 units) | Nathan / Southport, AU | new org |
| Hefei National Laboratory | Hefei, CN | pending from D546 / h46; compare with org_hefei_laboratory before aliasing |
| Heriot-Watt University | Edinburgh, GB | new org |
| Macquarie University (MQ Photonics, Dept. of Physics & Astronomy) | AU | new org |
| NIST (Center for Nanoscale Science and Technology) | Gaithersburg, US | alias to org_national_institute_of_standards_and_technology |
| NREL (unit drops with F1) | Boulder, US | new org |
| Renewable and Sustainable Energy Institute (after F1) | Boulder, US | new org (joint institute) |
| RMIT University (CUDOS / School of Engineering) | Melbourne, AU | new org |
| Singapore University of Technology and Design | Singapore, SG | new org |
| TU Dresden | Dresden, DE | alias to org_technische_universitat_dresden |
| Thalès Research and Technology | Palaiseau, FR | new org (printed accent) |
| University of Arizona (2 units) | Tucson, US | new org |
| University of Colorado (more_orgs, Boulder) | Boulder, US | same handling as University of Maryland in the JQI blocks (unmapped there too) |
| Universität Hamburg | Hamburg, DE | new org |
| Université Paris Saclay, Université Paris Sud, Université de Paris | Palaiseau, FR | aliases / new orgs with the earlier C2N blocks |
| Université d'Angers (Laboratoire de Photonique d'Angers EA 4464) | Angers, FR | new org |

## Privacy and as-printed scan

- Grep over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv` and `papers.csv` (paper ids and
  decision ids stripped) for contact / URL patterns, fax / phone, street / road / drive / boulevard / chaussee /
  chemin / weg / suite / room / building / block / box words, the street and building names printed in this batch's
  blocks, "No." + digit and digit runs of 4 or more: the only hits are generic note words ("street address(es)",
  "building names", "postal box", "site name") with no value, and the laboratory code EA 4464 in the Angers unit
  (printed as part of the laboratory name; not a postal code). No contact, street, building, postal code or P.O. box
  anywhere in the batch, notes included.
- `show` masking gap (outside the batch): yang2010a prints a fax number and a postal-box value unmasked in the `show`
  output; not copied into the batch or this record.
- As printed (kept, correct): Institute Of Optics (javid2021); Thalès (poulvellarie2021); Ghent University-IMEC
  (dash-joined); E.L. Ginzton Laboratory (no space); Physics & Informatics Laboratories (ampersand); Max-Planck
  Institute for the Science of Light (hyphen).

## Commands (2026-11-16, log times)

| Command | Result |
|---|---|
| `check lit_h47 --corpus lit --dry-run` 22:58:46 (pid 33432) | 0 errors, 1 warning (gaafar2024 explicit slot); slots 186, recorded 176, no_header 10; rows 225 (grade A 225; printed 215, single 10; primary 179, additional 46); papers ok 21, partial 1, unreadable 1; slots_from_header 2; multi-affiliation slots 36; 25 unmapped org strings |
| `show lit_h47 --corpus lit --codes <id> --pdf`, all 23 | headers, legends and author lists read (scratchpad only) |
| text.md leading symbol of masked contact lines (chen2021b, bruch2018, du2024, javid2021, chen2023d, herrmann2022) | marker 3 (chen2021b) and asterisks confirmed as contact lines |
| `h47_audit/probes/probe.py` on scratch copies, 23:01-23:07 | below; repo batch files md5 unchanged; probe checks wrote their usual logs under `logs/` (prefix `lit_headers_check_lit_p47`) |

| probe | change | result | reading |
|---|---|---|---|
| BASE | unchanged copy | 0 errors, 1 warning | baseline |
| L1 | liu2010a blocks and authors recorded | 6 errors | unreadable forced |
| D1 | du2024 block 1 NUS + unit CQT, authors readable | 2 errors | partial forced |
| D2 | du2024 Ling readable with 5 only | 2 errors | unreadable required |
| D3 | du2024 block 1 CQT org + NUS more_orgs | 0 errors | passes; against the 3-block CQT precedent |
| K1 | kasture2016 CUDOS as org + structured RMIT | 0 errors | neutral; unit form kept |
| K2 / X1 | kasture2016 / xiong2011 without slots_from_header | 1 error each | required |
| X2 | xiong2011 block 4 unit with comma | 0 errors | neutral |
| X3 | xiong2011 block 4 unit cut after the laboratory | 2 errors | full chain required |
| X4 | xiong2011 block 2 locality Sydney | 0 errors | false pass (Sydney inside the org name); empty is right |
| T1 / S1 | timurdogan2017 / siddharth2024 without author_list_differs | 1 error each | required |
| G1 | gaafar2024 Kärtner without slot | 2 errors | slot required |
| G2 / J1 / SI1 | last author without a further marker (Herr 6, Lin 2, Kippenberg 2) | 0 errors | G1 gap |
| SI2 | siddharth2024 Riemensberger without 2 | 2 errors | bound |
| B1 | bao2024 Ya Cheng without 7 | 1 error | block use bound |
| C1 | chen2021b Zhang without dropped 3 | 2 errors | bound |
| C2 | chen2021b Qing Xu slot 0 | 1 error | D302 |
| C3 | chen2021b locality Hong Kong | 0 errors | neutral; Kowloon is the corpus form |
| LU1 | luo2021 Fang Bo explicit slot 6 | 0 errors | neutral (automatic) |
| H1 | hickstein2019 block 6 institute as org + NREL, University of Colorado | 0 errors | F1 valid |
| H2 | hickstein2019 Hickstein without dropped a | 2 errors | bound |
| H3 | hickstein2019 block 6 University of Colorado + campus, NREL more_orgs, institute unit | 0 errors | passes; not recommended |
| P1 | poulvellarie2021 block 7 C2N first | 2 errors | printed order forced |
| HW1 | hwang2023 block 2 country US | 2 errors | not printed |
| LO1 | lorenzen2025 block 1 locality Hamburg | 4 errors | not printed in block 1 |
| Z1 | zhao2020 without campus | 0 errors | campus by precedent |
| Y1 | yan2021 block marked 1, authors 1 | 2 errors | block unmarked; single correct |
| FIX_all | F1 (block and note) | 0 errors, 1 warning; rows 226, unmapped 26 | fix valid |

## Checker gaps observed (scripts not edited)

- G1 last author's further markers not bound: gaafar2024 Herr, javid2021 Lin, siddharth2024 Kippenberg (records
  correct). Known (D442 / D546 / D557).
- D426 G6 street span between unit and org: du2024 block 1. Known; re-record after the fix.
- Blocks printed above the author line: liu2010a (as hu2022, lukin2019).
- Locality check passes a city that appears only inside the org name (probe X4).
- `show` masking: fax number and postal-box value unmasked in yang2010a output.

## Verdict

GO with fix F1. All 186 slots carry the right person; the 176 recorded slots have the right markers, org, unit,
campus, city and country, with one structural imprecision in hickstein2019 block 6 (F1, precedent form for a joint
institute). The 10 slots without rows are correctly unreadable (liu2010a, du2024 #1 / #6) or not printed in the
cached version (timurdogan2017 #3, siddharth2024 #3 / #7 / #10). Nothing is invented, no printed block is missed
except the three forced ones (documented in the notes), and no contact, street, building or postal text is
recorded.
