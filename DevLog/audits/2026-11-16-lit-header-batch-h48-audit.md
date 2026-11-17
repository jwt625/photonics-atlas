---
title: Fresh-context audit of the lit author-affiliation batch lit_h48 (23 papers)
date: 2026-11-16
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only with --dry-run, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h48/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D412, D426, D442, D466, D546, D557, D572); format from the 2026-11-15 h45 / h46 audits; read-only comparison with earlier batches (C2N / L2C / Univ. Grenoble Alpes + CEA forms, cover-page notes, lit_h47 chen2021b contact-marker form, "Tieyin / Tieying" misspelling slot)
verdict: GO with 1 fix; 167 list slots + 1 header-only author audited; 163 recorded slots ok, 4 slots correctly without rows, 0 wrong; F1 tabatabavakili2019 note (C2N acronym not printed); all extractor calls verified as forced or precedent-conform
---

# Lit header batch audit: lit_h48 (2026-11-16)

## Scope

Batch lit_h48: 23 papers (journal versions, arXiv preprints including chatterjee2020, jiang2018, shiue2015, doolin2015,
yang2018a and catalalahoz2026a, one Research Square preprint (peng2024) and one OECC/PSC 2025 paper); 167 list slots (shahin2025a, jiang2018, doolin2015 and
catalalahoz2026a with `slots_from_header`, 32 slots) plus 1 header-only author (chatterjee2020 Saumitra Sam, slot 0);
242 rows. Restricted corpus: this record names only authors, orgs, units, cities and countries; no paper text is
quoted and no contact, street, building, postal-box or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h48 --corpus lit --codes <id> --pdf`
  (all 23; peng2024 also with `--pages 2 3`; output kept in the session scratchpad `h48_audit/show/` only).
- Per slot: printed name vs the `show` author list and `compare.csv`; marker run vs text layer and PDF layer
  (identical in both layers for every printed-marker paper); block fields (org, unit chain, more_orgs, city,
  country); role; locator; grade. Every distinct (paper, org, city, country, org id, match basis, role, basis) tuple
  of `header_rows.csv` read (72 tuples, 242 rows).
- Contact lines behind dropped markers whose text is fully masked in `show` (zheng2024 8, zhou2020a 2 / 3, doolin2015
  a / b): the first character of each line containing an at-sign on source PDF page 1 was read with pymupdf (nothing
  else printed or copied): zheng2024 the two lines start with 8 and the asterisk; zhou2020a with 2 and 3; doolin2015
  with a) and b). jiang2018 a / b, shiue2015 b and lake2016 a are legible contact legends in the text layer.
- Symbol legends read on page 1 (wei2023, yang2018a, li2025h, zheng2024, shiue2015, youngblood2014, chatterjee2020,
  catalalahoz2026a).
- Source metadata (`references/<id>/source.json`, read-only) checked for the "arXiv preprint" and "published version"
  statements in notes (chatterjee2020, jiang2018, shiue2015, doolin2015, yang2018a, catalalahoz2026a arXiv URLs;
  yang2018a and peng2024 author lists keyed to the Nature Photonics DOIs).
- Probes on scratch copies (`h48_audit/probes/probe.py` in the session scratchpad, scratch `LIT_BASE`, batch name
  `lit_p48`, `cmd_check(..., dry_run=True)`). md5 of every repo batch file identical before and after the audit;
  `check_stamp.txt` matches `headers.yaml` (sha256 4b83c6b4...).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h48 | 23 / 23 | 167 + 1 header-only | 168 | 0 | 0 |

- Rows 242 (all grade A: printed 220, single 19, per_author 3; primary 194, additional 47, present address 1);
  recorded 163, no_header 4 (peng2024 #6 Chaerin Hong and yang2018a #6 Boqiang Shen, #7 Heming Wang not printed;
  chatterjee2020 #2 Saumitra Yadav, printed name differs); papers ok 23, partial 0, unreadable 0; `slots_from_header` 4;
  `author_list_differs` 3 (peng2024, chatterjee2020, yang2018a); explicit slots 2 (wei2023 #7, tang2021 #2) plus slot 0
  (chatterjee2020 Saumitra Sam); `order_differs` 1 (wei2023); multi-affiliation slots 36; 29 unmapped org strings.
- Per paper (slots / rows): wei2023 11 / 19; tang2021 6 / 12; aflatouni2015 4 / 5; chen2023c 10 / 11; shahin2025a 16 / 20;
  zhou2020a 2 / 2; peng2024 9 / 8; chatterjee2020 4 (+1 slot 0) / 3; feldmann2019 5 / 5; zhang2019e 9 / 9; jiang2018 10 / 15;
  schuler2016 8 / 8; youngblood2014 5 / 5; shiue2015 10 / 10; arianfard2020 4 / 4; yang2018a 8 / 6; lake2016 6 / 8;
  tabatabavakili2019 14 / 47; shiran2021 3 / 3; li2025h 9 / 18; doolin2015 4 / 4; catalalahoz2026a 2 / 2; zheng2024 8 / 18.

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (167 + 1) | 168 | 0 | 0 |
| markers (164 header authors) | 164 | 0 | 0 |
| header position (164) | 164 | 0 | 0 |
| blocks (org / unit / locality / country) (163 authors with rows) | 163 | 0 | 0 |
| present addresses (1 recorded, shahin2025a block 4) | 1 | 0 | 0 |
| locators (all blocks; peng2024 p.3) | all | 0 | 0 |
| notes (23) | 22 | 1 (tabatabavakili2019 acronym, F1) | 0 |

## Per-paper findings

- wei2023 (11; printed): Institute of Physics, Chinese Academy of Sciences, Beijing; Shanghai Jiao Tong University +
  state key laboratory (stray comma inside the laboratory name copied as printed) and Department of Electronic
  Engineering, Shanghai; Songshan Lake Materials Laboratory, Dongguan (province in the note); University of Chinese
  Academy of Sciences + School of Physical Sciences, Beijing; all CN. All 11 marker runs exact in both layers
  (Zi-Hao Wang, Jian-Jun Zhang, Ting Wang 1,3,4; Jing-Zhi Huang 1,4). Printed order differs from the list (Zi-Hao Wang
  printed 7th, list 4th): YAML keeps printed order, checker warning only. See call 1. ok.
- tang2021 (6; printed, capitals): Tsinghua University + Department of Electronic Engineering, Beijing; BNRist, Beijing
  (org with acronym, matched); CN. All six 1,2. See call 2. ok.
- aflatouni2015 (4; printed): Caltech + EE, Pasadena; University of Pennsylvania + ESE, Philadelphia; US. Aflatouni 1,2. ok.
- chen2023c (10; printed): University of Washington ECE / Physics, Seattle; Stanford + Mechanical Engineering,
  Stanford (country printed as United States); The Charles Stark Draper Laboratory (article kept), Cambridge; US.
  Perez and Goodson 3, Geiger 4, Majumdar 1,2. Sarah J. Geiger vs list Sarah Geiger automatic. ok.
- shahin2025a (16; printed, slots from header): imec (lower case, as printed), Leuven, BE; Ghent University +
  Photonics Research Group, Dept. of Information Technology, Ghent, BE; Ghent University + Department of Solid-State
  Sciences (org printed before the unit), Ghent, BE; block 4 present address Nubis Communication, New Providence,
  country empty (only a state code printed). Marker runs exact (Shahin 1,2; Berciano 1,4; Loo 1,3; Van Thourhout 1,2).
  See call 3. ok.
- zhou2020a (2; printed, capitals): Duke University + Department of Biomedical Engineering, Durham, country empty (state
  code only). Markers 2 and 3 are contact lines (verified). ok.
- peng2024 (9 list, 8 printed; single, p.3): page 1 Research Square cover (one org line per author), page 2 version-of-record
  notice, page 3 manuscript author line with one unmarked block: Hewlett Packard Enterprise + Large-Scale Integrated
  Photonics Lab, Milpitas, US. See call 4. ok.
- chatterjee2020 (4; per_author): each author printed above his own block; Indian Institute of Science + Center for
  Nano Science and Engineering (G1, G4) / Molecular Biophysics Unit (G2, G3), Bangalore, country empty (none printed).
  See call 5. ok.
- feldmann2019 (5; printed): University of Muenster + Institute of Physics, Muenster, DE (street between org and city,
  not recorded); University of Oxford + Department of Materials, Oxford, GB; University of Exeter + Department of
  Engineering, Exeter, GB. Initial forms (J. / N. / C.D. / H. / W.H.P.) match automatically. ok.
- zhang2019e (9; printed): SJTU + three-part chain, Shanghai; City, University of London + EEE, London, GB; Peking
  University + state key laboratory and Department of Electronics, Beijing. Jian Xu vs list Jian Xin Xu automatic. ok.
- jiang2018 (10; printed, closing-parenthesis markers, slots from header): USTC + "Hefei National Laboratory for
  Physical Sciences at Microscale and Department of Modern Physics" (unit chain); USTC + CAS Center for Excellence in
  Quantum Information and Quantum Physics; China Electronics Technology Group Corporation No.44 Research Institute,
  Chongqing (the number is part of the org name, not an address); Quantum CTek Co., Ltd., Hefei; all CN. Gao a) and
  Jun Zhang b) are contact legends. Probe J3: the national laboratory as its own org also passes; the unit-chain form
  matches the lit practice for laboratories printed before the host university (zhang2019e, zheng2024). ok.
- schuler2016 (8; printed): Vienna University of Technology + Institute of Photonics / Institute of Solid State
  Electronics, Vienna, AT; AMO GmbH, Aachen, DE. Streets not recorded. ok.
- youngblood2014 (5; printed single block with marker 1, D285): University of Minnesota + ECE, Minneapolis, US. ok.
- shiue2015 (10; printed, closing-parenthesis markers): MIT + EECS; Columbia University + Mechanical Engineering; IBM T.
  J. Watson Research Center (alias match); ICFO - Institut de Ciencies Fotoniques (dash and missing accent as printed);
  no place printed in any block (locality and country empty; probe E3 confirms). a) equal contribution (three authors),
  b) contact. ok.
- arianfard2020 (4; single): Swinburne University of Technology + Optical Sciences Centre, Hawthorn, AU. ok.
- yang2018a (8 list, 6 printed; printed single block with marker 1): Caltech + T. J. Watson Laboratory of Applied
  Physics, Pasadena, US. See call 6. ok.
- lake2016 (6; printed, closing-parenthesis markers): University of Calgary + IQST, Calgary, CA; National Institute for
  Nanotechnology, Edmonton, CA (street between institute and city, not recorded); City College of New York + Physics,
  New York, US; Universidade Estadual de Campinas + Instituto de Física Gleb Wataghin, Campinas, BR (alias match).
  Mitchell 1,2; Barclay 1,2 + a) contact. ok.
- tabatabavakili2019 (14; printed): block 1 Centre de Nanosciences et de Nanotechnologies + CNRS, Univ. Paris-Sud,
  Université Paris-Saclay, Palaiseau; block 2 Univ. Grenoble Alpes + CEA with unit INAC-Pheliqs (dict form), Grenoble;
  block 3 Laboratoire Charles Coulomb (L2C) + Université de Montpellier, CNRS, Montpellier; block 4 Université Côte
  d'Azur + CNRS, CRHEA, Valbonne; all FR. Markers exact. See call 7 and F1. ok.
- shiran2021 (3; single, capitals, one name per line): McGill University + ECE, Montreal, CA. ok.
- li2025h (9; printed): Chinese names in parentheses between each name and its markers (checker reads the run after
  the parenthetical); Southwest University + School of Physical Science and Technology / Chongqing key laboratory,
  Chongqing; NUDT + Center of Material Science, Changsha; Microelectronics Center Co., Ltd., Chongqing; CN. Haitang Li
  and Zihan Shen 1,2,3; Junbo Feng 4; Junbo Yang 2. See call 8. ok.
- doolin2015 (4; single, slots from header): University of Alberta + Department of Physics, Edmonton, CA. C. Doolin a)
  and J.P. Davis b) are contact lines (verified). ok.
- catalalahoz2026a (2; printed, slots from header): Universitat Politècnica de València + Photonics Research Labs,
  iTEAM Research Institute, Valencia (first of the two printed Valencia), ES. See call 9. ok.
- zheng2024 (8; printed): seven blocks (ECNU precision spectroscopy laboratory; ECNU XXL + school; SIOM, CAS with the
  state key laboratory and CAS center chain; Shanxi University, Taiyuan; Shandong Normal University, Jinan; Shanghai
  Research Center for Quantum Sciences; Hefei National Laboratory, Hefei); all CN. Ya Cheng 1-7 exact (probe Z2 bound).
  See call 10. ok.

## Extractor calls (verified)

1. wei2023 "Min Ming" -> slot 7 (list Ming Ming). Probe W1 (no slot): 2 errors. Probe W2 (slot 0 + `author_list_differs`):
   0 errors, so the checker is neutral. Same family name, same initials, one trailing letter missing; precedent: an
   earlier lit batch set the slot for printed Tieyin Li vs list Tieying Li as a plain misspelling. D287-conform; keep,
   with the D426 review-list entry the note announces.
2. tang2021 "HONGXAING JIA" -> slot 2 (list Hongxiang Jia). Probe T1 (no slot): 2 errors. Transposed letters, D287
   plain misspelling. Correct.
3. shahin2025a. `slots_from_header` (no author list, `show` prints the D352 marker). Block 4 cue "now with": probe S1
   (role affiliation) 2 errors, so `present_address` is forced; probe S2 (country US) 2 errors, so country empty is
   forced (only a state code printed). Correct.
4. peng2024. Locator p.3 header forced (probe G2, p.1: 16 errors). The cover's per-author org lines (Di Liang under
   University of California, Santa Barbara; HPE / Hewlett Packard Labs variants for the others) are Research Square
   metadata, not the manuscript header: not recorded, as the earlier cover-page papers (D366). Chaerin Hong (#6) is not
   printed on the cover or the manuscript author line; `author_list_differs` required (probe G1: 1 error). Correct.
5. chatterjee2020 "Saumitra Sam" slot 0. Probe C1 (no slot): 1 error; C3 (no `author_list_differs`): 1 error; C2 (slot 2):
   0 errors, so the checker is neutral. D287 / D369: family names differ and the initials (S. S. vs S. Y.) disagree,
   so slot 0 is the rule-conform call; the likely same person stays for the D412 / D426 lists, as the note says. Country
   empty forced (probe C4 IN: 2 errors). Correct.
6. yang2018a slots 6 / 7 not printed. Printed author line (both layers) has 6 names; the list (Nature Photonics DOI) has
   8. Probe Y1: `author_list_differs` required. No rows, status ok. Correct.
7. tabatabavakili2019 org forms. Probes A1 (C2N as unit of CNRS), A2 (L2C as unit of Université de Montpellier) and A3
   (CEA and INAC-Pheliqs as plain more_orgs) all pass: the checker is neutral. The recorded forms follow D466 (joint
   units recorded as their own org with the partners in `more_orgs`; IEF / C2N / INL / LTM / IMS precedent) and the
   earlier batch block "University Grenoble Alpes" + CEA dict with unit INAC-Pheliqs. Keep.
8. li2025h Zhengmao Wu: list "Wu Zheng-Mao" matched by name to slot 7 (compare.csv); probe I1 (slot 8) fails (slot 8
   matched twice), so Jiagui Wu and Zhengmao Wu are not crossed. Correct; D426 review list as the note says.
9. catalalahoz2026a marker "1*". The block marker prints 1 followed by the asterisk that the template adds to the
   corresponding authors' block; recorded "1" on block and authors. Probe K1 ("1*" everywhere) also passes; "1" is the
   affiliation marker, the asterisk a symbol mark (legend on page 1). Keep.
10. zheng2024 Rongbo Wu marker 8. No block 8 is printed; the source PDF line after the equal-contribution note starts
    with 8 and is a contact line (first character only inspected). Probe Z1 (no dropped 8): 2 errors. `dropped_markers`
    contact footnote correct, lit_h47 chen2021b form.
11. Empty countries (zhou2020a, shahin2025a block 4, chatterjee2020, shiue2015): no country printed in those blocks;
    probes H3, S2, C4, E3 each fail with a code. Correct (D249 / D288).

## Fixes (exact YAML edits)

F1 (note accuracy; the acronym C2N is not printed in this paper, only the full name). In `lit:tabatabavakili2019`
replace

```yaml
block 1 prints the joint unit C2N before CNRS
```

with

```yaml
block 1 prints the joint unit Centre de Nanosciences et de Nanotechnologies (acronym not printed) before CNRS
```

Rows unchanged. Probe FIX_all (F1 on a scratch copy): 0 errors, 3 warnings (the baseline warnings).

## Observations (no change recommended)

- O1 Several notes call the asterisk the corresponding-author mark where page 1 prints only a contact line after it, no
  "corresponding" legend (tang2021, aflatouni2015, chen2023c, shiran2021, peng2024, tabatabavakili2019). Symbol marks
  need no YAML entry and the wording matches earlier batches; no fix.
- O2 Last author's further markers are not bound by the checker (G1, known D442 / D546 / D557): zhou2020a Horstmeyer 3
  (H2), lake2016 Barclay a (L1), shiue2015 Englund b (E1), doolin2015 Davis b (D1) pass without their dropped entries;
  non-last authors are bound (H1, J1, J2, E2, D2, Z1).

## Open questions (with recommendation)

1. D426 review list: wei2023 #7 (printed Min Ming, list Ming Ming, explicit slot), tang2021 #2 (HONGXAING / Hongxiang),
   li2025h #7 (name-order list form Wu Zheng-Mao), zhang2019e #4 (Jian Xu / Jian Xin Xu, automatic). Recommended: add.
2. D412 correction list: chatterjee2020 (list Saumitra Yadav, printed Saumitra Sam; slot 0 under D287), peng2024 #8
   (list artefact "Marco Fiorentino B", same family as "Daoxin Dai A"). Recommended: add both.
3. G1 test list: zhou2020a #2, lake2016 #6, shiue2015 #10, doolin2015 #4 (probes H2, L1, E1, D1). Recommended: add.

## Unmapped org names (org round, no YAML change)

| printed org (unit) | place | proposal |
|---|---|---|
| China Electronics Technology Group Corporation No.44 Research Institute | Chongqing, CN | new org (CETC 44th institute) |
| City College of New York | New York, US | new org or alias under CUNY |
| City, University of London | London, GB | new org |
| CRHEA | Valbonne, FR | new org (CNRS laboratory) |
| Hefei National Laboratory | Hefei, CN | new org (pending since D546) |
| ICFO - Institut de Ciencies Fotoniques | (none printed) | alias to the ICFO org if the registry has one, else new org |
| Indian Institute of Science (2 units) | Bangalore | new org |
| Laboratoire Charles Coulomb (L2C) | Montpellier, FR | new org |
| Microelectronics Center Co., Ltd. | Chongqing, CN | new org |
| National Institute for Nanotechnology | Edmonton, CA | new org |
| National University of Defense Technology | Changsha, CN | new org |
| Nubis Communication | New Providence | new org |
| Quantum CTek Co., Ltd. | Hefei, CN | new org |
| Songshan Lake Materials Laboratory | Dongguan, CN | new org |
| Southwest University (2 units) | Chongqing, CN | new org |
| The Charles Stark Draper Laboratory | Cambridge, US | new org (article form) |
| Univ. Grenoble Alpes | Grenoble, FR | alias (abbreviated form) to the Grenoble Alpes org used by earlier batches, else new org |
| Univ. Paris-Sud / Université Paris-Saclay / Université de Montpellier | Palaiseau / Montpellier, FR | aliases or new orgs |
| University of Alberta, University of Calgary, University of Exeter, University of Minnesota, University of Muenster | | new orgs or aliases (University of Muenster spelling without umlaut) |
| Vienna University of Technology (2 units) | Vienna, AT | alias to TU Wien if present, else new org |

(29 strings in `unmapped_orgs.csv`.)

## Privacy and as-printed scan

- Grep over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv` and `papers.csv` (paper ids and
  decision ids stripped) for contact / URL patterns, street / road / avenue / suite / room / building / box words, the
  street names printed in the sources, "No." + digit and digit runs of 4 or more: hits only for the conference year
  (OECC/PSC 2025), paper ids of precedents and the org name "China Electronics Technology Group Corporation No.44
  Research Institute" (institute number, not an address). Notes say that streets / postal codes exist without giving
  them. No contact, street, building, postal code or P.O. box anywhere in the batch, notes included.
- `show` masking (outside the batch): peng2024 cover prints ORCID URLs (not copied).
- As printed (kept, correct): imec (lower case); ICFO - Institut de Ciencies Fotoniques; State Key Laboratory of Advanced
  Optical, Communication Systems and Networks (stray comma, wei2023); Dept. of Information Technology; Chongqing Key
  Laboratory of Micro&Nano Structure Optoelectronics; City, University of London; The Charles Stark Draper Laboratory.

## Commands (2026-11-16, log times)

| Command | Result |
|---|---|
| `show lit_h48 --corpus lit --codes <id> --pdf`, all 23 (+ peng2024 `--pages 2 3`) | headers, legends and author lists read (scratchpad only) |
| `check lit_h48 --corpus lit --dry-run` 23:07:00 (pid 37300) | 0 errors, 3 warnings (wei2023 slot 7, wei2023 order differs, tang2021 slot 2); slots 167, recorded 163, no_header 4; rows 242 (grade A 242; printed 220, single 19, per_author 3; primary 194, additional 47, present address 1); papers ok 23; slots_from_header 4; multi-affiliation slots 36; 29 unmapped org strings |
| pymupdf, source PDF page 1, first characters of at-sign lines (zheng2024, zhou2020a, doolin2015) | markers 8, 2 / 3, a) / b) confirmed as contact lines |
| `h48_audit/probes/probe.py` on scratch copies, 23:08:11-23:11:51 and FIX run | below; repo batch files md5 unchanged; probe checks wrote their usual logs under `logs/` (prefix `lit_headers_check_lit_p48`) |

| probe | change | result | reading |
|---|---|---|---|
| BASE | unchanged copy | 0 errors, 3 warnings | baseline |
| W1 / W2 | wei2023 Min Ming no slot / slot 0 + differs | 2 / 0 errors | slot needed; 7 vs 0 is a judgment (call 1) |
| T1 | tang2021 HONGXAING no slot | 2 errors | slot required |
| C1 / C2 / C3 / C4 | chatterjee2020 no slot / slot 2 / no differs / country IN | 1 / 0 / 1 / 2 errors | slot 0 rule-conform (call 5) |
| Y1 | yang2018a no differs | 1 error | required |
| G1 / G2 | peng2024 no differs / locator p.1 | 1 / 16 errors | both forced |
| S1 / S2 / S3 | shahin2025a block 4 as affiliation / country US / block 3 without unit | 2 / 2 / 0 errors | present address and empty country forced; S3 would drop a printed unit |
| Z1 / Z2 | zheng2024 Rongbo Wu no dropped 8 / Ya Cheng without 7 | 2 / 1 errors | bound |
| H1 / H2 / H3 | zhou2020a Zhou no dropped 2 / Horstmeyer no dropped 3 / country US | 2 / 0 / 2 errors | H2 = G1 gap |
| J1 / J2 / J3 | jiang2018 Gao no a / Jun Zhang no b / national lab as org | 2 / 2 / 0 errors | J3 neutral, unit chain kept |
| L1 | lake2016 Barclay no dropped a | 0 errors | G1 gap |
| E1 / E2 / E3 | shiue2015 Englund no b / Shiue no a / Cambridge, US on block 1 | 0 / 2 / 4 errors | E1 = G1 gap; empty place forced |
| D1 / D2 | doolin2015 Davis no b / C. Doolin no a | 0 / 3 errors | D1 = G1 gap |
| K1 / K2 | catalalahoz2026a marker 1* / country empty | 0 / 0 errors | neutral; "1" and ES kept as printed |
| A1 / A2 / A3 | tabatabavakili2019 C2N as unit / L2C as unit / CEA plain | 0 errors each | neutral; D466 forms kept |
| I1 | li2025h Zhengmao Wu slot 8 | 2 errors | name match not crossed |
| F1 | feldmann2019 Wright marker 1 | 3 errors | markers bound |
| FIX_all | F1 | 0 errors, 3 warnings | fix valid |

## Checker gaps observed (scripts not edited)

- G1 Last author's further markers not bound: zhou2020a, lake2016, shiue2015, doolin2015 (H2, L1, E1, D1). Known.
- Explicit-slot and slot-0 alternatives are both accepted for wei2023 and chatterjee2020 (W2, C2): the D287 / D369
  judgment is not machine-checked.
- Org-form alternatives for joint units and national laboratories pass both ways (A1-A3, J3); precedent decides.

## Verdict

GO with fix F1. All 167 list slots and the header-only author carry the right person; the 163 recorded slots have the
right markers, org, unit, city and country; the 4 slots without rows are correctly unprinted (peng2024 #6, yang2018a
#6, #7) or a differing printed name (chatterjee2020 #2, printed author kept as slot 0). Nothing is invented, no block is
missed, no contact, street, building or postal text is recorded. F1 only corrects the C2N wording in the
tabatabavakili2019 note.
