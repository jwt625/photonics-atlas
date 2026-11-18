---
title: Fresh-context audit of the lit author-affiliation batch lit_h53 (22 papers)
date: 2026-11-18
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only with --dry-run, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h53/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D412, D426, D521, D522, D599, D629, D644); format from the lit_h51 audit
verdict: GO with 0 required fixes; 159 slots (142 list + 17 slots_from_header) audited, 159 recorded with 0 wrong rows; 1 optional note fix (N1 ahmmed2020 district name); Hong Kong locality in ahmmed2020 is the rule-consistent value (the corpus Kowloon / Shatin values are the outliers, org-round normalization)
---

# Lit header batch audit: lit_h53 (2026-11-18)

## Scope

Batch lit_h53: 22 papers (Optics Express / Optica, JLT / PTL / JSTQE footnote statements, one IEEE Access paper, one
conference paper with per-author blocks, one ECTC-style conference paper); 159 slots (zhang2014a 7, libsch2006 7,
wang2020 3 `slots_from_header`); 193 rows. Restricted corpus: this record names only authors, orgs, units, cities and
countries; no paper text is quoted and no contact, street, building, site or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h53 --corpus lit --codes <id> --pdf`
  (all 22; output kept in the session scratchpad `h53_audit/show/` only).
- Per slot: printed name vs the `show` author list and `compare.csv`; marker run in both text layers; every prose
  statement (subject names, verb, clauses) against the footnote; block fields (org, unit chain, campus, city, country);
  role; locator; notes. chang2020 contact lines: only the leading marker character read (4 and 5), the rest not printed.
- 73 distinct (paper, marker, org, unit, city, country, org ids, match basis) tuples of `header_rows.csv` read (193 rows).
- Precedent greps over all `lit_headers` / `ofc_headers` YAMLs: WNLO forms, SIOM forms, LIGENTEC, AIM Photonics / SUNY,
  Ningbo Institute of Technology, UCSB campus, Hong Kong localities, Fraunhofer HHI forms.
- Probes on scratch copies (`h53_audit/probes/probe.py` + `probes_h53.py`, scratch `LIT_BASE`, batch name `lit_p53`,
  `cmd_check(..., dry_run=True)`). md5 of every repo batch file identical before and after the audit; `check_stamp.txt`
  matches `headers.yaml` (sha256 ea1351d6...). Probe checks wrote their usual logs under `logs/` (prefix
  `lit_headers_check_lit_p53`).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h53 | 22 / 22 | 159 | 159 | 0 | 0 |

- Rows 193 (all grade A: prose 108, printed 58, single 18, per_author 9; primary 162, additional 31, present address 0);
  recorded 159, no_header 0; papers ok 22, partial 0, unreadable 0; `slots_from_header` 3; `author_list_differs` 0;
  explicit slots 0; multi-affiliation slots 27; 18 unmapped org strings; 0 warnings.
- Per paper (slots / rows): chang2020 6 / 7; yokota2022 3 / 3; hu2017 7 / 8; zhang2014a 7 / 7; acoleyen2011a 3 / 3;
  zhang2022c 7 / 7; koscica2025 13 / 18; su2023 15 / 22; libsch2006 7 / 7; feng2024 9 / 9; wang2020 3 / 3;
  pruessner2016 5 / 5; li2025f 12 / 15; ikeda2010 4 / 4; ahmmed2020 3 / 4; du2019 12 / 13; song2024b 8 / 15;
  qiu2017 7 / 7; liu2024b 4 / 8; chen2025b 5 / 7; xiang2018 5 / 5; zhu2020 14 / 15.

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (159) | 159 | 0 | 0 |
| markers (159) | 159 | 0 | 0 |
| prose subjects / clauses (108 rows, 13 papers) | all | 0 | 0 |
| blocks (org / unit / campus / locality / country) | 159 | 0 | 0 |
| locators | all | 0 | 0 |
| notes (22) | 21 | 1 (ahmmed2020, N1 optional: district not named) | 0 |

## Per-paper findings

- chang2020 (6; printed, capitals): Columbia EE, New York, US; National Chiao Tung University + Department of Photonics
  and Institute of Electro-Optical Engineering, Hsinchu, TW (Taiwan printed as the place). Marker 3 = equal
  contribution line (Chang, Shin), markers 4 / 5 lead the two masked contact lines (Chang, Lipson). Michal Lipson vs
  list Michal F. Lipson automatic. ok.
- yokota2022 (3; single, capitals): Tohoku University + RIEC, Sendai, JP (prefecture and postal code not recorded). ok.
- hu2017 (7; printed, capitals): HUST + School of Optical and Electronic Information; WRI; Accelink Technologies Co.,
  Ltd.; block 4 prints only the State Key Laboratory of Optical Communication Technologies and Networks, Wuhan (no
  parent printed). Laboratory as org is right (probe H1 with WRI as parent: 4 errors). Yi Hu 1,3; Wei Cao 2;
  Qiu and Yu 4 (probe H2: 2 errors). ok.
- zhang2014a (7; prose, slots from header): "The authors are with" statement; Fraunhofer Institute for
  Telecommunications, Heinrich-Hertz-Institut, Berlin, DE (same string as committed lit blocks, alias to the HHI org;
  leading "the" not copied, prose practice). `show` prints no author list (probe LB2 analogue: required). ok.
- acoleyen2011a (3; prose): Photonics Research Group, Department of Information Technology (INTEC), Ghent
  University-IMEC, Ghent, BE (hyphen form as printed; 17 committed blocks use it). Membership designations ignored. ok.
- zhang2022c (7; single, capitals): HUST with unit "Wuhan National Laboratory for Optoelectronics & School of Optical
  and Electronic Information" (identical string in 6 committed blocks; unit chain is the lit majority form, 23 of 28
  committed WNLO blocks; probe Z1 with WNLO as org + HUST more_orgs: 0 errors, neutral). Street and postal code not recorded. ok.
- koscica2025 (13; prose): statements checked against the footnote, see call 1. UCSB with campus Santa Barbara (P1
  Materials Department and Institute for Energy Efficiency; P2, P3 IEE); P4 clause Aeluma Inc., Goleta; P5 AIM
  Photonics + RF SUNY Polytechnic Institute, Albany; P6 Analog Photonics, Boston; US. List forms Alec M. Skipper,
  Andrew M. Netherton, David L. Harame, John Edward Bowers automatic. ok.
- su2023 (15; prose): five statements, clause blocks P2 (UCAS Center of Materials Science and Optoelectronics
  Engineering, Beijing) and P4 (SIOM key laboratory after ZhangJiang Laboratory); P7 LIGENTEC SA, Ecublens, CH (site
  name between org and city not recorded; probe S1 Lausanne: 2 errors). Statement order and carriers verified
  (probe S3 without the P4 clause: coverage error). See call 5. ok.
- libsch2006 (7; printed, slots from header): IBM T. J. Watson Research Center, Yorktown Heights; Steridian
  Corporation, Vancouver; North Carolina State University + Dept. of Electrical and Computer Engineering, Raleigh. Only
  US states are printed, no country: `country: ""` is required (probe LB1 "US": 2 errors). Streets, suite and postal
  codes not recorded. Sanford 2 (probe LB3: 3 errors). ok.
- feng2024 (9; per_author): blocks under each author verified in reading order (probe F4 Skipper on G5: 3 errors).
  "University of California Santa Barbara" printed without comma: campus form as lit_h52 piggott2020 (probe F3 whole
  name: 0 errors, neutral; D301 decides); IQE, Inc., Greensboro; NAsPIII/V GmbH, Marburg, DE; RF SUNY Polytechnic
  Institute alone, Albany. See calls 1 and 6. ok.
- wang2020 (3; single, capitals, slots from header): Nanchang Hangkong University + School of Information Engineering,
  Nanchang, CN. ok.
- pruessner2016 (5; single): U.S. Naval Research Laboratory, locality Washington (probe P1 "Washington, D.C.": rejected
  as not city only), US. ok.
- li2025f (12; printed): block 1 four-element unit chain before Zhejiang University, campus name after it not recorded
  (D522; probe L1 with the campus: 0 errors, checker neutral, the ruling decides); blocks 2 / 3 Ningbo Research
  Institute, Ningbo, and Intelligent Optics and Photonics Research Center, Jiaxing Research Institute, Jiaxing. Ming
  Zhang 1,2; Dai 1,2,3 (probe L2 without 3: error). List artefact Daoxin Dai A matched (D412). ok.
- ikeda2010 (4; printed single block with marker 1, D285): Tohoku University Department of Nanomechanics, Sendai, JP. ok.
- ahmmed2020 (3; printed, capitals): CityU EE, Hong Kong, HK; University of Chittagong EEE, Chittagong, BD. See call 3
  and N1. ok.
- du2019 (12; printed, capitals, initials): Southampton ORC; NTU Silicon Technologies Centre of Excellence, Singapore,
  SG (postal code then Singapore, recorded as city and country, corpus practice); University of Glasgow, Glasgow, GB
  (no unit printed). All initials agree with the list (S. Stanković, D. T. Tran list forms). ok.
- song2024b (8; prose): four statements, clause blocks P2 (International Research Center for Advanced Photonics,
  Haining), P5 / P8 (Jiaxing key laboratory chain, Jiaxing), P7 (Ningbo Research Institute, Ningbo); Shi and Dai carry
  P6, P7, P8. Unit chains copied whole. ok.
- qiu2017 (7; prose, initials): Longyan University; Zhejiang University Department of Information Science and
  Electronics Engineering, Hangzhou; NTU School of EEE, Singapore; Ningbo Institute of Technology as a unit of Zhejiang
  University, Ningbo. See call 5. ok.
- liu2024b (4; prose): "The authors are with" SIMIT, CAS + State Key Laboratory of Materials for Integrated Circuits,
  Shanghai; clause UCAS + Materials Science and Opto-electronics Technology Research Center, Beijing. ok.
- chen2025b (5; prose): Nanjing University four-element unit chain; Yong Zhao statement with two "also with" clauses
  (Jiangnan University School of Internet of Things Engineering; Wuxi Suntech Power Company Ltd.); Yongjiang
  Laboratory, Ningbo; Yi Ni, Jiangnan University. See call 6. ok.
- xiang2018 (5; prose, initials): UCSB ECE with the place printed once (campus and locality Santa Barbara, all 84
  committed UCSB campus blocks carry locality Santa Barbara); Johns Hopkins ECE, Baltimore; Morton Photonics, West
  Friendship. Paul A. Morton vs Paul Adrian Morton automatic. ok.
- zhu2020 (14; prose): Sun Yat-Sen University state key laboratory + school; Jinan University department / college and
  provincial key laboratory / institute chains, Guangzhou; Zhaohui Li clause Southern Laboratory of Ocean Science and
  Engineering, Zhuhai. See call 6. ok.

## Extractor calls (verified)

1. koscica2025 statement 2 printed without word spaces after the subject: really verified, not passed by default.
   Probes K1 (P2 unit Materials Department): 32 errors; K2 (P2 city Goleta): 2 errors; K7 (Chen Shang on P3 instead of
   P2): 4 errors; K8 (P2 block removed): 35 errors. Statement 4 "AIM Photonics, RF SUNY Polytechnic Institute" as org +
   `more_orgs`: correct as two printed organizations (D285; precedent: the committed "The Research Foundation for State
   University of New York" + SUNY Polytechnic Institute block). Probes K3 (more_orgs dropped), K4 (one joined org), K5
   (RF SUNY org + AIM unit), K6 ("RF" dropped) all 0 errors, so the checker is neutral and the contract decides; K6 / F1
   show it accepts a shortened org string (substring), so "RF" must stay as printed. feng2024 "RF SUNY Polytechnic
   Institute" alone as org: as printed, keep. Keep all.
2. UCSB campus (D301): koscica2025 (comma form), xiang2018 (place printed once), feng2024 (no comma, as lit_h52
   piggott2020). All map to org_ucsb (13 rows). Keep.
3. ahmmed2020 block 1 locality. The block prints a street, then the district Kowloon Tong, then Hong Kong. D366 /
   lit contract: "locality = the city as printed; a district printed before the city goes to the note"; Kowloon Tong is
   a district, Hong Kong the printed city / SAR, so "Hong Kong" is right. "Kowloon" is not printed here as a place of
   its own (only inside the district name), so the earlier Kowloon form would not even be as printed. Probes A1
   (Kowloon Tong), A2 (Kowloon), A3 (empty) all 0 errors: the checker cannot tell a district from a city, the rule
   decides. Corpus: lit HK localities Hong Kong 22, Kowloon 14, Shatin 3; OFC Hong Kong 12, Shatin 1. The Kowloon /
   Shatin values follow the older "first printed place" reading (D288) that D366 narrowed for districts; several lit
   notes already record "the district Shatin / Kowloon / Clear Water Bay before Hong Kong" with locality Hong Kong.
   Ruling recommended for the org round (D599 open item): Hong Kong wherever printed, districts to the note; normalize
   the 14 Kowloon and 3 + 1 Shatin blocks then. Keep ahmmed2020 as recorded (note wording N1 optional).
4. li2025f campus name after Zhejiang University not recorded (D522: a campus within one city is not a distinct
   institution; probe L1 neutral). hu2017 block 4 laboratory as org: correct, nothing else printed (probe H1).
5. qiu2017 Ningbo Institute of Technology as a unit of Zhejiang University: identical to the committed qiu2018 P4
   (same author, same printed form); the org-form question from the lit_h45 audit (question 1, open in the D599 org
   round) covers both; probe Q1 (whole name as org): 0 errors, neutral. su2023 key laboratory as unit of "Shanghai
   Institute of Optics and Fine Mechanics, Chinese Academy of Sciences": no committed block of this laboratory (the 3
   SIOM blocks in this batch are its first), but SIOM as org with its laboratory as unit is the lit form (14 committed
   blocks, 5 with this exact org string); probe S2 with the laboratory as org: 0 errors, neutral); LIGENTEC site name not
   recorded as in 3 committed LIGENTEC blocks. zhang2022c WNLO + school unit chain under HUST: lit majority form (call
   above). Keep all.
6. Name matches without explicit slot, all made automatically by the checker (0 warnings): feng2024 #3 Chen Shang vs
   list Shang Chen (swapped order; the same person is list "Chen Shang" in koscica2025 #10, UCSB Materials); chen2025b
   #4 Yi Ni vs Yi Qing Ni (dropped given-name syllable; probe N1 slot 0: rejected, D302); zhu2020 #3 Zhenshi Chen vs
   Zhen shi Chen (split given name, list artefact). li2025f #12 / song2024b #8 Daoxin Dai A (D412). No YAML change;
   list entries below.
7. chang2020 markers 4 and 5 as contact footnotes (leading characters of the masked lines are 4 and 5), marker 3 equal
   contribution: correct. Probes C1 (Chang without 4) and C2 (Shin without 3): 2 errors each; C3 (Lipson without 5):
   0 errors, the known last-author extra-marker gap (D629 G1). libsch2006 country "" in all three blocks: required (LB1).
   zhang2014a, libsch2006, wang2020 `slots_from_header`: `show` prints no author list for all three (LB2: required).

## Fixes (exact YAML edits)

No required fix.

N1 (optional, note wording). Name the district in the note, as the other Hong Kong notes do ("the district Shatin
before Hong Kong"). In `lit:ahmmed2020` replace

```yaml
block 1 prints a street address and a district before Hong Kong (district not recorded; locality Hong Kong, HK);
```

with

```yaml
block 1 prints a street address and the district Kowloon Tong before Hong Kong (locality Hong Kong, HK, D366);
```

Not probed (note text only; the D244 scan has no pattern for a district name).

## Lists (no YAML change)

1. D426 review list: feng2024 #3 (list Shang Chen, printed Chen Shang; same person as koscica2025 #10), chen2025b #4
   (list Yi Qing Ni, printed Yi Ni).
2. D412 author-list corrections: zhu2020 #3 "Zhen shi Chen" (split given name); li2025f #12 and song2024b #8 "Daoxin
   Dai A" (already listed form).
3. Org round: Hong Kong district ruling (call 3); qiu2017 P4 with the open qiu2018 Ningbo Institute of Technology
   question; hu2017 State Key Laboratory of Optical Communication Technologies and Networks printed without a parent
   (committed blocks print it under WRI or CICT; mapping is an org-round decision, never a YAML inference); RF SUNY
   Polytechnic Institute (4 rows, koscica2025 / feng2024).
4. G1 test cases (last-author extra marker not checked): chang2020 #6 (C3).

## Unmapped org names (org round, no YAML change)

| printed org (unit) | place | proposal |
|---|---|---|
| Aeluma Inc. | Goleta, US | new org |
| Jiangnan University (2 units) | Wuxi, CN | new org |
| Longyan University | Longyan, CN | new org |
| Morton Photonics | West Friendship, US | new org (also lit_h51 xiang2019) |
| NAsPIII/V GmbH | Marburg, DE | new org |
| Nanchang Hangkong University | Nanchang, CN | new org |
| National Chiao Tung University | Hsinchu, TW | new org or alias |
| RF SUNY Polytechnic Institute | Albany, US | alias to the Research Foundation for SUNY / SUNY Poly org (org round) |
| Shanghai Institute of Microsystem and Information Technology, Chinese Academy of Sciences | Shanghai, CN | new org or alias |
| Southern Laboratory of Ocean Science and Engineering | Zhuhai, CN | new org |
| State Key Laboratory of Optical Communication Technologies and Networks | Wuhan, CN | org-round decision (see list 3) |
| Steridian Corporation | Vancouver (no country printed) | new org |
| U.S. Naval Research Laboratory | Washington, US | new org or alias |
| University of Chittagong | Chittagong, BD | new org |
| University of Glasgow | Glasgow, GB | new org or alias |
| Wuxi Suntech Power Company Ltd. | Wuxi, CN | new org |
| Yongjiang Laboratory | Ningbo, CN | new org |

(17 org names; 18 strings in `unmapped_orgs.csv` because Jiangnan University appears with two units.)

## Privacy and as-printed scan

- Grep over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv` and `papers.csv` (paper ids and
  decision ids stripped) for contact / URL patterns, street / road / avenue / drive / box / building / suite / floor /
  room / telephone words, digit runs of 4+, and the street, site, campus and district strings printed in the sources:
  hits only for notes saying that a street address or postal code exists without giving it. No contact, street,
  building, suite, postal code or P.O. box anywhere in the batch, notes included.
- As printed (kept, correct): Ghent University-IMEC; Dept. of Electrical and Computer Eng. (feng2024 G1); NAsPIII/V
  GmbH; ZhangJiang Laboratory; Sun Yat-Sen University; F.R.  Libsch spacing folded by the checker.

## Commands (2026-11-18)

| Command | Result |
|---|---|
| `show lit_h53 --corpus lit --codes <id> --pdf`, all 22 | headers and author lists read (scratchpad only) |
| `check lit_h53 --corpus lit --dry-run` 13:54:43 (pid 65069) | 0 errors, 0 warnings; slots 159, recorded 159; rows 193 (grade A 193; prose 108, printed 58, single 18, per_author 9; primary 162, additional 31); papers ok 22; slots_from_header 3; multi-affiliation slots 27; 18 unmapped org strings |
| `h53_audit/probes/probe.py` on scratch copies | below; repo batch files md5 unchanged |

| probe | change | result | reading |
|---|---|---|---|
| BASE | unchanged copy | 0 errors | baseline |
| K1 / K2 / K7 / K8 | koscica P2 unit wrong / city Goleta / Shang on P3 / P2 removed | 32 / 2 / 4 / 35 errors | space-less statement 2 verified |
| K3 / K4 / K5 / K6 | AIM only / joined org / RF SUNY org + AIM unit / "RF" dropped | 0 each | neutral; contract decides (call 1) |
| F1 | feng2024 "RF" dropped | 0 | substring accepted; keep as printed |
| F2 / F3 | Chen Shang slot 3 / UCSB without campus | 0 / 0 | neutral |
| F4 | Skipper on G5 | 3 errors | per_author position bound |
| A1 / A2 / A3 / A4 | Kowloon Tong / Kowloon / empty / CN | 0 / 0 / 0 / 2 errors | locality is a ruling (call 3) |
| H1 / H2 | hu2017 WRI parent / Yu marker 3 | 4 / 2 errors | block 4 as printed; markers bound |
| L1 / L2 | li2025f campus recorded / Dai without 3 | 0 / 1 error | D522 decides; bound |
| Q1 | qiu2017 NIT whole name as org | 0 | neutral (open org-form question) |
| S1 / S2 / S3 | LIGENTEC Lausanne / key lab as org / P4 clause removed | 2 / 0 / 2 errors | city bound; neutral; coverage |
| Z1 | zhang2022c WNLO org + HUST more_orgs | 0 | neutral; majority form kept |
| N1 | chen2025b Yi Ni slot 0 | 1 error (D302) | automatic match required |
| C1 / C2 / C3 | Chang without 4 / Shin without 3 / Lipson without 5 | 2 / 2 / 0 errors | C3 = last-author gap |
| LB1 / LB2 / LB3 | libsch2006 country US / no slots_from_header / Sanford 1 | 2 / 1 / 3 errors | required as recorded |
| D1 | du2019 Singapore locality empty | 0 | Singapore kept (corpus practice) |
| P1 | pruessner2016 "Washington, D.C." | 1 error | city only |

## Checker gaps observed (scripts not edited)

- Last author's extra marker not checked (chang2020 Lipson, C3; D629 G1).
- District accepted as locality (A1 / A2); a shortened org string accepted (K6 / F1: "RF" dropped passes).
- `show` contact masking: libsch2006 prints a telephone number unmasked and ikeda2010 a domain fragment after the mask
  (terminal output only; nothing reached the batch files; not copied here).

## Verdict

GO, no required fix. All 159 slots carry the right person, markers, org, unit, campus, city and country; every prose
statement and clause is recorded and verified (the space-less koscica2025 statement included); the three
`slots_from_header` papers have no author list. ahmmed2020 locality Hong Kong is the rule-consistent value; the corpus
Kowloon / Shatin blocks are for the org-round ruling. Optional N1 names the district in the ahmmed2020 note. Nothing is
invented and no contact, street, building or postal text is recorded.
