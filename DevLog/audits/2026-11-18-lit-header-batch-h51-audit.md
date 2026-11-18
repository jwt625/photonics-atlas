---
title: Fresh-context audit of the lit author-affiliation batch lit_h51 (22 papers)
date: 2026-11-18
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only with --dry-run, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h51/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D412, D416, D426, D521, D546, D550, D572, D599); format from the lit_h49 / lit_h50 audits
verdict: GO with 3 fixes; 225 slots (204 list + 21 slots_from_header) plus 3 header-only authors audited; 219 recorded slots with 0 wrong rows; F1 kim2019a #4 Mengjie Yu present address (dagger, end-of-paper note on p.4) omitted; F2 weng2021 block 3 locality Glasnevin is a district (D521 hatori2014 ruling: empty); F3 bino2018 Xin Xhao should take explicit slot 5 (misprint of the list name Xin Miao Zhao), not slot 0
---

# Lit header batch audit: lit_h51 (2026-11-18)

## Scope

Batch lit_h51: 22 papers (arXiv revtex preprints, Optica / OSA manuscripts, one grouped-layout preprint); 225 slots
(zhou2023a `slots_from_header`, 21 slots) plus 3 header-only authors (bino2018 Xin Xhao, helgason2021 Victor
Torres-Company, li2017a Hongtao Lin, all slot 0); 280 rows. Restricted corpus: this record names only authors, orgs,
units, cities and countries; no paper text is quoted and no contact, street, building or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h51 --corpus lit --codes <id> --pdf`
  (all 22; output kept in the session scratchpad `h51_audit/show/` only).
- Per slot: printed name vs the `show` author list and `compare.csv`; marker run in the text and PDF layers; block
  fields (org, unit chain, campus, city, country); role; locator; notes. Symbol footnotes (asterisk, dagger, double
  dagger, letter a) looked up in `references/<id>/text.md` beyond page 1 for every paper (contact masked in my own
  output): equal contribution confirmed for bino2018, wang2018d, castro2025, liu2019b (end of paper), li2017a,
  chang2020a, liu2024c and dmitriev2022 (end of paper); contact lines for the rest, except kim2019a (F1).
- 91 distinct (paper, marker, role, org, unit, city, country, basis, locator, org id, match basis) tuples of
  `header_rows.csv` read (280 rows).
- Probes on scratch copies (`h51_audit/probes/probe.py`, scratch `LIT_BASE`, batch name `lit_p51`,
  `cmd_check(..., dry_run=True)`). md5 of every repo batch file identical before and after the audit; `check_stamp.txt`
  matches `headers.yaml` (sha256 60272408...). Probe checks wrote their usual logs under `logs/` (prefix
  `lit_headers_check_lit_p51`).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h51 | 22 / 22 | 225 + 3 header-only | 225 | 3 (kim2019a #4 F1; weng2021 #4, #7 F2) | 0 |

bino2018 #5 / Xin Xhao (F3) is counted as imprecise on the slot side only: the extractor's slot 0 leaves the list slot
without rows; no row is wrong.

- Rows 280 (all grade A: printed 236, single 27, grouped 17; primary 221, additional 55, present address 4); recorded
  219, no_header 6 (bino2018 #5; weng2021 #2 unreadable; li2017a #1 duplicate Lan Li, #15 Shiue, #16 Englund not
  printed; chang2020a #9 Chao Xiang not printed); papers ok 21, partial 1 (weng2021), unreadable 0;
  `slots_from_header` 1; `author_list_differs` 4 (bino2018, helgason2021, li2017a, chang2020a); explicit slots 1
  (li2017a Lan Li 7) plus slot 0 three times; 22 unmapped org strings; 3 order warnings (dmitriev2022, rueda2019,
  li2017a). After F1-F3: recorded 220, no_header 5, rows 283 (present address 5), `author_list_differs` 3.
- Per paper (slots / rows): zhou2023a 21 / 22; bino2018 6 / 7; kiewiet2025 14 / 22; weng2021 8 / 9; pfeifle2014 17 / 19;
  wang2018d 15 / 16; xue2017 5 / 9; dmitriev2022 9 / 11; rueda2019 5 / 17; castro2025 13 / 15; liu2019b 8 / 13;
  helgason2021 7 (+1) / 7; xiang2019 8 / 9; liu2024c 9 / 18; kim2019a 9 / 13; nejadriahi2023 6 / 6; li2017a 21 (+1) / 21;
  nejadriahi2021 4 / 4; chang2020a 17 / 18; vogelbacher2019 6 / 7; obrzud2021 10 / 10; ji2022a 7 / 7.

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (225 + 3) | 227 | 1 (bino2018 Xin Xhao, F3) | 0 |
| markers (223 printed authors) | 222 | 1 (kim2019a #4, F1) | 0 |
| header position / grouped order | 223 | 0 | 0 |
| blocks (org / unit / locality / country) (219 authors with rows) | 217 | 2 (weng2021 #4, #7 locality, F2) | 0 |
| unreadable calls (1) | 1 | 0 | 0 |
| present addresses (4 recorded) | 4 + 1 missed (F1) | 0 | 0 |
| locators | all | 0 | 0 |
| notes (22) | 19 | 3 (kim2019a, weng2021, bino2018; F1-F3) | 0 |

## Per-paper findings

- zhou2023a (21; printed, slots from header): Yale Applied Physics, New Haven; JPL, Pasadena (Caltech parent not
  copied, D416 (2) parent rule; probe Z1 with Caltech as more_orgs: 0 errors, neutral); Sandia + unit printed on the line
  before the org, Albuquerque; University of Arizona + Wyant College, Tucson; all US. Eichenfield 3,4. ok.
- bino2018 (6; printed): NPL, Teddington, GB; Heriot-Watt, Edinburgh, GB (Scotland printed, in the checker's GB name
  list); Beihang + school, Beijing, CN. Dagger equal contribution (verified). See call 1 and F3.
- kiewiet2025 (14; printed): "Ghent University - imec" + Photonics Research Group, INTEC, Ghent (dash form kept, D426;
  maps to both org ids by alias); imec, Leuven; BE. Asterisk / dagger contact lines. List forms Sandeep Seema Saseendran
  and Roelof A. Jansen match automatically. ok.
- weng2021 (8; printed, partial): block 1 EPFL + Institute of Physics, country CH, locality empty (only a postal code
  is printed; Lausanne is inside the org name; 2 of 38 EPFL blocks in lit_h01-h49 also carry an empty locality; probe W4 Lausanne
  passes, W5 Geneva fails, so the empty value is the ruling, not a checker result); block 2 (TCD) not recorded, author 2
  unreadable (call 2); block 3 DCU + lab / school chain, IE, see F2; blocks 4 / 5 present addresses NIST Time and
  Frequency Division and University of Colorado Department of Physics, Boulder, US (Lucas 1,4,5). Asterisk, dagger,
  double dagger = contact lines (verified).
- pfeifle2014 (17; printed): KIT + "IPQ and IMT" unit (two institutes joined by and, printed before KIT), Karlsruhe;
  EPFL (detached accents written École / Fédérale, D282), Lausanne; Menlo Systems GmbH, Martinsried; block 4 "now with"
  ETH Zurich, Zurich, `present_address` (Hillerkuss, Leuthold; probe P1 Leuthold without 4: 2 errors). Yimin / Yi-Min
  Yu automatic. ok.
- wang2018d (15; printed, capitals): Sun Yat-sen + state key laboratory, Guangzhou, CN; UCL, Bristol ("Eng." as
  printed), Sheffield departments, GB. Siyuan Yu 1,3. ok.
- xue2017 (5; printed): Tsinghua EE, Beijing, CN; Purdue ECE school and Birck Nanotechnology Center, West Lafayette, US
  (street numbers between org and city not recorded). ok.
- dmitriev2022 (9; printed): Russian Quantum Center, Moscow; MIPT, Dolgoprudny (region not recorded); Samsung R&D
  Institute Russia + SAIT-Russia Laboratory printed after the org, Moscow (probe D1 without unit: 0 errors, neutral;
  as printed); EPFL Institute of Physics, Lausanne, CH; Lomonosov MSU Faculty of Physics, Moscow. Asterisks on authors
  1-5 = equal contribution (end-of-paper note), no block. List swaps Lobanov / Min'kov (order warning, D363). ok.
- rueda2019 (5; grouped): G1-G12 checked against the layout: Rueda (MPL Erlangen; FAU institute; "SAOT, School in
  Advanced Optical Technologies" as printed; IST Austria, Klosterneuburg; Dodd-Walls / Otago), Sedlmeir (MPL, FAU),
  Leuchs printed third (MPL, FAU, "Institute of Applied Physics, Russian Academy of Sciences", Nizhny Novgorod, RU;
  Dodd-Walls / Otago), Kumari and Schwefel (G12). The Dodd-Walls line prints only the country, then "and" the Otago
  department with Dunedin: org + `more_orgs` with own unit / city (D367) is right; locality empty on the Dodd-Walls part
  (probe R3 Dunedin passes: the checker reads the whole block; empty is the ruling). Probe R1 (Kumari on G11): 4 errors
  (position bound). Streets and postal codes not recorded. ok.
- castro2025 (13; printed, capitals): UC + campus Santa Barbara (ECE, Physics, Materials), Santa Barbara; University of
  Cagliari Physics, Monserrato, IT; Nexus Photonics Inc., Goleta. Pintus 1,3; Bowers 1,5. ok.
- liu2019b (8; printed, capitals): UCSB ECE / IEE / Materials; CUHK Electronic Engineering, locality Shatin, HK (see O2).
  Equal-contribution symbol verified on the last page. Gossard and Bowers 1,3,4. ok.
- helgason2021 (7 + 1; single): Chalmers MC2, Gothenburg, SE. Torres-Company printed, not in the list: slot 0 (probe H1
  without slot: 1 error; lit_h30 helgason2023 precedent). ok.
- xiang2019 (8; printed): UCSB ECE / Materials; Morton Photonics, West Friendship, US. ok.
- liu2024c (9; printed): EPFL Institute of Physics and Center for Quantum Science and Engineering, Lausanne, CH; all
  authors 1,2. Asterisk equal contribution, dagger / double dagger contact (note wording "symbol marks" is accurate). ok.
- kim2019a (9; printed): Columbia APAM / EE, New York; Cornell ECE / AEP, Ithaca; US. Dagger on Mengjie Yu points to a
  present address: F1.
- nejadriahi2023 (6) / nejadriahi2021 (4) (single, capitals): one unmarked block with "1" printed on every author
  (dropped, D285; probe N1 one author with "1": 1 error); UC + campus San Diego + ECE, La Jolla, US (street, state,
  postal code not recorded). Paul Yu vs Paul K. L. Yu automatic. ok.
- li2017a (21 + 1; printed): MIT DMSE / EECS, Cambridge, US; Xiamen EE, CN; Chongqing University + unit chain with the
  ministry (contiguous segment forced: probe LI3 without the ministry: 2 errors; same form as the committed Soochow
  "Education Ministry of China" units); UCF College of Optics & Photonics, Orlando; Southampton ORC, GB. See call 3.
- chang2020a (17; printed): UCSB ECE; Peking University + state key laboratory (printed before the org), Beijing; Caltech
  + T. J. Watson Laboratory, Pasadena; RMIT School of Engineering, Melbourne, AU; NIST Gaithersburg / Boulder divisions.
  Dagger equal contribution (verified). List slot 9 Chao Xiang not printed: `author_list_differs` required (probe C1:
  1 error). Qifan / Qi-Fan Yang automatic. ok.
- vogelbacher2019 (6; printed, capitals): AIT + Center for Health & Bioresources, TU Wien + Photonics Institute (unit
  after org; probe V1 without unit: 0 errors, as printed kept), ams AG, Premstätten; AT. ok.
- obrzud2021 (10; single): CSEM (full name with acronym), Neuchâtel, CH; letter a on Brasch = contact footnote (verified).
  Probe O1 (no `dropped_markers` entry): 0 errors, so the entry is not required but correct (D286d). ok.
- ji2022a (7; printed single block with marker 1, D285): EPFL Institute of Physics, Lausanne, CH. ok.

## Extractor calls (verified)

1. bino2018 "Xin Xhao" -> slot 0. Probe B3 (no slot): 0 candidates, so a slot is needed; B1 (slot 5, differs removed)
   and B2 (slot 5, differs kept): 0 errors. The printed name differs from the list name Xin Miao Zhao by a misprinted
   family-name letter and a dropped given-name syllable; same position, same given name, the only candidate, Beihang
   block. D287 allows an explicit slot for plain misspellings (lit_h36 nie2019 NINA TRUK / Nina Turk), D426 accepts
   dropped syllables for review (jin2024, ren2025). The D412 correction list does not apply: the list is not the
   artefact, the header is. Slot 0 leaves list slot 5 without rows and drops the Beihang row (header-only authors get
   no rows). Change: F3.
2. weng2021 block 2 / author 2 unreadable. Probe W1 (TCD as org + CONNECT Research Centre as unit): 2 errors (unit and
   org not contiguous: the building name sits between them), the D426 G6 gap. Probe W2 (CONNECT Research Centre as org,
   TCD as `more_orgs`): 0 errors, but it would make CONNECT an org where ofc_h04 / ofc_h06 / pilot record CONNECT as a
   unit of TCD; D546 practice is to keep the gap and re-record. Keep; re-record list.
3. li2017a: list positions 1 and 7 both Lan Li (probe LI1 without slot: 2 candidates); slot 7 follows the printed
   neighbour Kaiqi Wang, list slot 1 stands where Hongtao Lin is printed (list artefact). Hongtao Lin slot 0: probe LI4
   (slot 1) passes, so the checker is neutral; a different name cannot take a slot (D287). Shiue / Englund not printed.
   Keep; D412 correction list.
4. chang2020a slot 9 not printed, helgason2021 Torres-Company slot 0: required by the checker (C1, H1). Keep.
5. zhou2023a `slots_from_header`: `show` prints no author list. Keep.
6. rueda2019 grouped with Dodd-Walls + Otago `more_orgs`, SAOT as printed: keep (above).
7. weng2021 EPFL empty locality: keep. DCU Glasnevin: F2.
8. dmitriev2022 / vogelbacher2019 unit printed after org: as printed, neutral probes D1 / V1. Keep.
9. nejadriahi2021 / 2023 single unmarked block: keep. obrzud2021 letter a as contact footnote: keep.
10. Order warnings (dmitriev2022 Lobanov / Min'kov swap, rueda2019 Leuchs printed third, li2017a list artefacts):
    expected (D363).

## Fixes (exact YAML edits)

F1 (kim2019a author 4 Mengjie Yu, present address omitted). The dagger after Mengjie Yu (both layers: "1, dagger")
points to a "Currently at" note printed with the end-of-paper notes on text.md page 4: Harvard University, John A.
Paulson School of Engineering and Applied Sciences, Cambridge, US. The extractor called it a symbol mark. Same paper
family and layout as lit_h29 dutt2018 (present address p.6, audit fix D546). The checker verifies the block on p.4:
probes K1 0 errors; K2 (no locator) 2, K3 (Boston) 2, K4 (Harvard College) 4, K5 (shortened unit) 2, K6 (block without
the author marker) 3 errors. Same unit / org form as 5 committed Harvard SEAS blocks.

In `lit:kim2019a` replace

```yaml
  note: "arXiv preprint; asterisk and dagger marks not recorded (symbol marks, no block); states and postal codes not recorded"
```

with

```yaml
  note: "arXiv preprint; asterisk marks the contact line; the dagger on author 4 points to a present address (Currently at) printed with the end-of-paper notes on page 4 (locator p.4 affiliations, lit_h29 dutt2018 precedent); states and postal codes not recorded"
```

after

```yaml
    - {marker: "4", basis: printed, org: "Cornell University", unit: "School of Applied and Engineering Physics", locality: "Ithaca", country: "US"}
```

insert

```yaml
    - {marker: "†", basis: printed, role: present_address, org: "Harvard University", unit: "John A. Paulson School of Engineering and Applied Sciences", locality: "Cambridge", country: "US", locator: "p.4 affiliations"}
```

and replace

```yaml
    - {name: "Mengjie Yu", markers: ["1"]}
```

with

```yaml
    - {name: "Mengjie Yu", markers: ["1", "†"]}
```

F2 (weng2021 block 3 locality). The DCU block prints the district Glasnevin and a postal district, no city. D288 /
D366: locality is the printed city, a district goes to the note; lit_h26 hatori2014 (district Komaba only, locality
empty) is the accepted ruling (D521). Probe W3: 0 errors (the checker cannot tell a district from a city).

In `lit:weng2021` replace

```yaml
locality: "Glasnevin"
```

with

```yaml
locality: ""
```

and in the note replace

```yaml
block 3 prints the Glasnevin district as its only place;
```

with

```yaml
block 3 prints only the district Glasnevin as place (locality empty, lit_h26 hatori2014 ruling, D521);
```

F3 (bino2018 author 5 slot). See call 1. In `lit:bino2018` delete the line

```yaml
  author_list_differs: true
```

replace in the note

```yaml
author 5 printed Xin Xhao, author list Xin Miao Zhao (family-name spelling and middle name differ: slot 0, D412 correction list);
```

with

```yaml
author 5 printed Xin Xhao, author list Xin Miao Zhao: misprinted family name and dropped given-name syllable, same position and only candidate (explicit slot 5, D287 misspelling as lit_h36 nie2019; D426 review list);
```

and replace

```yaml
    - {name: "Xin Xhao", markers: ["1", "3"], slot: 0}
```

with

```yaml
    - {name: "Xin Xhao", markers: ["1", "3"], slot: 5}
```

Probe FIX_ALL (F1 + F2 + F3 on one scratch copy): 0 errors, 4 warnings (the 3 order warnings plus the explicit slot
5 warning); recorded 219 -> 220, no_header 6 -> 5, rows 280 -> 283 (present address 4 -> 5, additional 55 -> 56),
`author_list_differs` 4 -> 3.

## Observations (no change recommended)

- O1 kim2019a shows a checker gap: a symbol marker that points to a present address on a later page passes silently
  when neither block nor marker is recorded (baseline 0 errors); only recording the block binds the marker (K6).
  Extractors should look up every symbol footnote in the end-of-paper notes of revtex preprints.
- O2 liu2019b locality Shatin (district printed before Hong Kong): the corpus is split (Shatin in lit_h04 / lit_h11 for
  the same CUHK department, Hong Kong in lit_h20 / h21 / h50; Kowloon in the CityU blocks). Probe L1 (Hong Kong): 0
  errors. Not changed here; a corpus-wide ruling for Hong Kong districts belongs to the org round.
- O3 Notes calling the asterisk the corresponding-author mark where page 1 prints only a contact line (bino2018,
  wang2018d, vogelbacher2019, helgason2021): same wording as earlier batches (h50 O2); no fix.
- O4 obrzud2021 `dropped_markers` entry for the letter a is not enforced by the checker (probe O1) but correct.

## Open questions (with recommendation)

1. Re-record list (checker gap D426 G6): weng2021 block 2 (values: Trinity College Dublin + unit CONNECT Research
   Centre, no city printed apart from the org name, IE; author 2 marker 2). Recommended: add.
2. D412 author-list corrections: li2017a (list slot 1 duplicate Lan Li where Hongtao Lin is printed; Shiue / Englund
   absent from the preprint header), chang2020a #9 Chao Xiang, helgason2021 (Torres-Company missing, with
   helgason2023). D426 review list: bino2018 #5 (after F3), li2017a #7. Recommended: add.
3. Checker gap O1 (symbol marker to a later-page present address not detected). Recommended: note with the D442 cue
   gaps; no YAML impact beyond F1.

## Unmapped org names (org round, no YAML change)

| printed org (unit) | place | proposal |
|---|---|---|
| Dublin City University (lab, school) | IE | new org |
| Heriot-Watt University | Edinburgh, GB | new org |
| Institute of Applied Physics, Russian Academy of Sciences | Nizhny Novgorod, RU | new org |
| Institute of Science and Technology Austria | Klosterneuburg, AT | new org |
| Jet Propulsion Laboratory | Pasadena, US | new org (Caltech parent) |
| M.V. Lomonosov Moscow State University (Faculty of Physics) | Moscow, RU | new org |
| Morton Photonics | West Friendship, US | new org |
| Moscow Institute of Physics and Technology (MIPT) | Dolgoprudny, RU | new org |
| NIST (Time and Frequency Division) | Boulder, US | alias to the NIST org (acronym form) |
| National Physical Laboratory (NPL) | Teddington, GB | new org |
| RMIT University (School of Engineering) | Melbourne, AU | new org |
| Russian Quantum Center | Moscow, RU | new org |
| SAOT, School in Advanced Optical Technologies | Erlangen, DE | alias under FAU or new org |
| Samsung R&D Institute Russia (SAIT-Russia Laboratory) | Moscow, RU | child of Samsung or new org |
| TU Wien (Photonics Institute) | Vienna, AT | new org or alias |
| The Dodd-Walls Centre for Photonic and Quantum Technologies | NZ | new org |
| University Erlangen-Nuernberg (Institute for Optics, Information and Photonics) | Erlangen, DE | alias to FAU |
| University of Arizona (Wyant College) | Tucson, US | new org or alias |
| University of Colorado (Department of Physics) | Boulder, US | campus question (D301 not applicable: no campus printed) |
| University of Otago (Department of Physics) | Dunedin, NZ | new org |
| University of Sheffield | Sheffield, GB | new org or alias |
| Xiamen University | Xiamen, CN | new org or alias |

(22 strings in `unmapped_orgs.csv`; F1 adds Harvard University, which maps by name to org_harvard_university in 89 committed rows with the same unit.)

## Privacy and as-printed scan

- Grep over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv` and `papers.csv` (paper ids and decision
  ids stripped) for contact / URL patterns, street / road / avenue / drive / gasse / box / building / house words, the
  street, building and postal strings printed in the sources, postal-district forms and digit runs: hits only for notes
  that say a street address, building name or postal code exists without giving it, and the family name Van Gasse. No
  contact, street, building, postal code or P.O. box anywhere in the batch, notes included. The F1-F3 texts name no
  address item.
- As printed (kept, correct): Ghent University - imec; University Erlangen-Nuernberg; SAOT, School in Advanced Optical
  Technologies; Department of Electronic and Electrical Eng. (Bristol); Photonics Systems and Sensing Lab.; Centre Suisse
  d'Electronique et de Microtechnique (CSEM) with the typographic apostrophe; Pascal Del'Haye and Kirill N. Min'kov with
  the typographic apostrophe.

## Commands (2026-11-18)

| Command | Result |
|---|---|
| `show lit_h51 --corpus lit --codes <id> --pdf`, all 22 | headers and author lists read (scratchpad only) |
| `check lit_h51 --corpus lit --dry-run` 09:32:53 (pid 72618) | 0 errors, 3 warnings (order: dmitriev2022, rueda2019, li2017a); slots 225, recorded 219, no_header 6; rows 280 (grade A 280; printed 236, single 27, grouped 17; primary 221, additional 55, present address 4); papers ok 21, partial 1; slots_from_header 1; multi-affiliation slots 46; 22 unmapped org strings |
| `h51_audit/probes/probe.py` on scratch copies | below; repo batch files md5 unchanged |

| probe | change | result | reading |
|---|---|---|---|
| BASE | unchanged copy | 0 errors, 3 warnings | baseline |
| K1 | kim2019a dagger present address p.4 + Yu marker | 0 errors | F1 valid |
| K2 / K3 / K4 / K5 | no locator / Boston / Harvard College / shortened unit | 2 / 2 / 4 / 2 errors | block verified on p.4 |
| K6 | block without the author marker | 3 errors | marker bound once recorded (O1) |
| B1 / B2 | Xin Xhao slot 5, differs removed / kept | 0 / 0 errors | F3 valid |
| B3 / B4 | no slot / name "Xin Zhao" | 1 / 4 errors | slot needed; name as printed forced |
| W1 / W2 | weng2021 block 2 TCD + CONNECT unit / CONNECT org + TCD more_orgs | 2 / 0 errors | G6 gap real; W2 inconsistent with committed form |
| W3 | DCU locality empty | 0 errors | F2 |
| W4 / W5 | EPFL locality Lausanne / Geneva | 0 / 2 errors | empty is the ruling |
| L1 | liu2019b Hong Kong | 0 errors | O2 |
| LI1 / LI2 / LI3 / LI4 | Lan Li no slot / slot 1 / ministry dropped / Lin slot 1 | 1 / 0 / 2 / 0 errors | call 3 |
| O1 | obrzud2021 no dropped a | 0 errors | O4 |
| Z1 | JPL + Caltech more_orgs | 0 errors | parent rule decides |
| H1 | Torres-Company no slot | 1 error | slot 0 required |
| C1 | chang2020a differs removed | 1 error | required |
| R1 / R2 / R3 | Kumari on G11 / SAOT acronym dropped / Dodd-Walls Dunedin | 4 / 0 / 0 errors | position bound; as printed / empty are rulings |
| D1 / V1 | dmitriev2022, vogelbacher2019 unit dropped | 0 / 0 errors | neutral |
| N1 | nejadriahi2021 one author with 1 | 1 error | D285 |
| P1 | pfeifle2014 Leuthold without 4 | 2 errors | bound |
| FIX_ALL | F1 + F2 + F3 | 0 errors, 4 warnings | fixes valid |

## Checker gaps observed (scripts not edited)

- Symbol marker pointing to a present address on a later page is not detected when unrecorded (kim2019a, O1).
- Building name between unit and org in a printed block (weng2021, D426 G6).
- District accepted as locality; empty locality accepted when the org name carries the city (rulings, not checks).
- Letter marker to a contact footnote not required in `dropped_markers` (obrzud2021).
- Explicit slot vs slot 0 not machine-decided (li2017a LI4, bino2018 B1 / B2).

## Verdict

GO with fixes F1-F3. Every printed author carries the right person except bino2018 Xin Xhao (slot 0 instead of the
misprinted list name, F3); the 219 recorded slots have the right markers, org, unit, city and country, apart from the
district recorded as city in weng2021 (F2); kim2019a misses one present address (F1). weng2021 #2 is correctly without
rows (checker gap). Nothing is invented and no contact, street, building or postal text is recorded.
