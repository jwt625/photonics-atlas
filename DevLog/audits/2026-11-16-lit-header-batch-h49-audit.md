---
title: Fresh-context audit of the lit author-affiliation batch lit_h49 (26 papers)
date: 2026-11-16
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; probe checks only on scratch copies under a scratch LIT_BASE; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h49/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D426, D466, D522, D599); format from the 2026-11-16 h47 / h48 audits; read-only comparison with earlier batches (lit_h09 rao2019 article-in-unit present address, City University of Hong Kong / Kowloon blocks, grouped two-block precedent, name-order swap notes)
verdict: GO with 3 fixes; 188 list slots audited (49 from the header); 187 recorded slots with the right person and fields, 1 slot correctly without rows (patel2014 #4), 0 wrong; F1 quack2019 printed IMEC department left out (unit), F2 / F3 isti2025 and xuan2016 explicit slots that the checker does not need (contract: slot only when the script cannot match); rows unchanged except one unit field
---

# Lit header batch audit: lit_h49 (2026-11-16)

## Scope

Batch lit_h49: 26 papers (journal papers in JLT, PTL, JQE, IEEE Photonics Journal, Optics Express, Optica; four
conference papers: fan2016, liu2021b, patel2014, acoleyen2011); 188 list slots (fan2016, patel2014, ciminelli2013,
mao2008, acoleyen2011, nedeljkovic2014 and giuntoni2012 with `slots_from_header`, 49 slots); 229 rows. Restricted
corpus: this record names only authors, orgs, units, cities and countries; no paper text is quoted and no contact,
street, building, postal-box or postal-code text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h49 --corpus lit --codes <id> --pdf`
  (all 26; guo2021 and acoleyen2012 also with `--pages 2`; output only in the session scratchpad `h49_audit/show/`).
- Per slot: printed name vs the `show` author list and `compare.csv`; marker run in the text layer and the PDF layer
  (identical in both layers for every printed-marker paper); prose statement subjects; block fields (org, unit chain,
  more_orgs, campus, city, country); role; locator; grade. Every distinct (paper, org, city, country, org id, match
  basis, role, locator) tuple of `header_rows.csv` read (65 tuples, 229 rows).
- ciminelli2013 marker 3: the first character of each line containing an at-sign on source PDF page 1 read with
  pymupdf (nothing else printed or copied): one line starts with 3, the other with the asterisk. Marker 3 is a contact
  line.
- Probes on scratch copies (`h49_audit/probes/probe.py` and `probe2.py` in the session scratchpad, scratch `LIT_BASE`,
  batch name `lit_p49`; `cmd_check(..., dry_run=True)`, FIX_all with derived files written into the scratch copy only
  and diffed against the repo files). md5 of every repo batch file identical before and after the audit;
  `check_stamp.txt` matches `headers.yaml` (sha256 a8cae026...).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h49 | 26 / 26 | 188 | 187 | 1 | 0 |

- Imprecise: quack2019 #6 Wim Bogaerts, P5 unit printed but not recorded (F1). F2 / F3 change no row.
- Rows 229 (all grade A: printed 117, prose 69, single 31, grouped 12; primary 201, additional 28, present address 0);
  recorded 187, no_header 1 (patel2014 #4 Wei Shi, present-address-only, `unreadable`); papers ok 25, partial 1
  (patel2014), unreadable 0; `slots_from_header` 7; `author_list_differs` 0; explicit slots 2 (isti2025 #2, xuan2016
  #15; both redundant, F2 / F3); `order_differs` 0; multi-affiliation slots 27; 18 unmapped org strings. Check
  baseline (scratch copy, unchanged YAML): 0 errors, 0 warnings.
- Per paper (slots / rows): guo2021 8 / 12; liu2022d 6 / 9; kobayashi2014 8 / 8; fan2016 8 / 9; zhang2025g 3 / 3;
  zhou2022c 5 / 6; zhang2023f 12 / 12; liu2021b 7 / 21; fard2016 3 / 3; yang2024b 3 / 6; chen2016c 11 / 11; isti2025
  8 / 8; patel2014 7 / 6; acoleyen2012 6 / 12; ciminelli2013 5 / 5; mao2008 7 / 10; fang2011 7 / 8; acoleyen2011 5 / 5;
  xuan2016 19 / 20; quack2019 9 / 11; sun2010 2 / 2; nedeljkovic2014 10 / 10; espinola2003 4 / 4; lu2018 14 / 15;
  giuntoni2012 7 / 9; luke2013 4 / 4.

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (188) | 188 | 0 | 0 |
| markers (188 header authors, incl. prose / grouped carriers) | 188 | 0 | 0 |
| header position (188) | 188 | 0 | 0 |
| blocks (org / unit / locality / country) (187 authors with rows) | 186 | 1 (quack2019 #6, F1) | 0 |
| present addresses (patel2014 block 2, no rows: author unreadable) | 1 | 0 | 0 |
| locators (all blocks; guo2021 / acoleyen2012 p.2) | all | 0 | 0 |
| notes (26) | 23 | 3 (quack2019, isti2025, xuan2016; F1-F3) | 0 |

## Per-paper findings

- guo2021 (8; printed, p.2): page 1 IEEE Photonics Journal cover with the names only; page 2 marked author line.
  Shanghai Jiao Tong University + four-part chain (state key laboratory ... Department of Electronic Engineering),
  Shanghai, CN; SJTU-Pinghu Institute of Intelligent Optoelectronics, Pinghu, CN; LIGENTEC SA, Ecublens, CH (site
  and building name between org and city, not recorded). Marker runs exact (Lu, Nisar, Chen, Zhou 1,2; Stroganov 3).
  Probe GU1 (locator p.1): 22 errors, so p.2 is forced. ok.
- liu2022d (6; prose): statement 1 (Liu, Guo, Li) and statement 2 (Lu, Chen, Zhou) both name the same SJTU chain
  (two blocks, contract: one block per statement); statement 2 clause "and also with" SJTU-Pinghu, Pinghu (P3,
  `clause: true`). Unit chain keeps the mid-chain article ("the Shanghai Institute ...") as printed. Probe LD1 (Lu
  without P3): 2 errors. ok.
- kobayashi2014 (8; prose): NEC Yamanashi Ltd. PLC Development Group (Kobayashi, Sato, Watanabe, Yamazaki) / Mod
  Development Group (Namiwaka), Otsuki; NEC Ltd. MONOZUKURI Innovation Division, Kawasaki (as printed); Tohoku
  University, Department of Communication Engineering (Kita) / Department of Electrical and Communication Engineering
  (Yamada), Sendai; all JP; prefectures not recorded. Printed Kenji Sato vs list K. Sato automatic. Probe KO1 bound. ok.
- fan2016 (8; printed symbol markers, slots from header): asterisk-operator, dagger, double dagger and section sign
  are the block markers (legend lines start with them, both layers). University of Twente + "MESA+ institute for
  Nanotechnology, Laser Physics and Nonlinear Optics group"; SatraX B.V.; LioniX B.V.; XiO Photonics B.V.; all
  Enschede, NL. Epping dagger + double dagger (probe FA2: 2 errors). "Klaus.-J Boller" printed so in both layers
  (source typesetting, not an extraction artefact): kept as printed; probe FA1 ("Klaus-J. Boller") also passes, the
  checker folds punctuation (observation O1). FA3 (MESA+ as further org) fails (6 errors): unit chain forced. ok.
- zhang2025g (3; single, capitals): University of Cambridge + Centre for Photonic Devices and Sensors, Cambridge, GB
  (United Kingdom printed); street and postal code not recorded. DAPING CHU vs list Daping P. Chu automatic. ok.
- zhou2022c (5; printed, capitals): UESTC (acronym kept) + School of Electronic Science and Engineering, Chengdu, CN;
  State Key Laboratory of Terahertz and Millimeter Waves with City University of Hong Kong in parentheses, recorded as
  org City University of Hong Kong + unit the laboratory, Kowloon, HK (same form as earlier City University of Hong
  Kong blocks); Hikvision Research Institute, Chengdu, CN. Probe ZH1 (CN): 2 errors; ZH2 (locality Hong Kong) passes,
  Kowloon is the first printed place (D288; D599 org-round question). Hyphen-less printed names (BAOJIE, YUANSONG)
  matched automatically. ok.
- zhang2023f (12; printed): Nexus Photonics, Goleta, US; University of California + campus Santa Barbara + Department
  of Electrical and Computer Engineering, Santa Barbara, US (D301). Morin and Bowers 2, the rest 1. Dagger equal
  contribution, asterisk contact: symbols, no entry needed. ok.
- liu2021b (7; single): Centre de Nanosciences et de Nanotechnologies as org, Université Paris-Saclay and CNRS in
  `more_orgs`, Palaiseau, FR (D466 form). Probe LI1 (Paris-Saclay org, C2N unit) also passes; precedent decides. ok.
- fard2016 (3; printed, capitals): McGill University / Concordia University, both Department of Electrical and Computer
  Engineering, Montreal, CA; province not recorded. GLENN COWAN vs Glenn E. R. Cowan automatic. ok.
- yang2024b (3; printed, capitals): BUPT + state key laboratory (1) / School of Integrated Circuits (2), Beijing, CN.
  All three 1,2. ok.
- chen2016c (11; prose): Ghent University-imec + Photonics Research Group, Department of Information Technology,
  Ghent, BE (Chen, Roelkens); Technical University of Denmark + DTU Fotonik, Kongens Lyngby, DK (Galili, Oxenlowe;
  post-verb article not copied, as other prose statements; probe CH1 neutral); Interuniversity Microelectronics
  Center, Leuven, BE (seven authors). Hongtao Chen vs list Hong Tao Chen automatic. ok.
- isti2025 (8; prose): University of Delaware + Electrical and Computer Engineering Department, Newark, US (six
  authors); Phase Sensitive Innovations Inc., Newark, US (Yao, Hossain). Xiaofeng Zhu slot 2: see F2. ok.
- patel2014 (7; printed, slots from header; partial): McGill University + Dept. of Electrical and Computer
  Engineering, Montreal, CA; block 2 "Currently with" Laval University, unit "the Dept. of ...", Quebec, CA. Wei Shi
  carries only marker 2. Probes: PA1 (unit without article) 4 errors, so the article is forced (lit_h09 rao2019
  precedent); PA2 (Wei Shi readable) 1 error, so `unreadable` is forced (D426 G4 present-address-only gap; h43
  cheung2015 precedent); PA3 (role affiliation) 2 errors. ok.
- acoleyen2012 (6; grouped, p.2): page 1 cover; page 2 author line with membership designations, then two unmarked
  blocks: Ghent University-imec + Photonics Research Group, Department of Information Technology (INTEC), Ghent; Ghent
  University + Center for Nano- and Biophotonics (NB-Photonics), Ghent; BE. Every author carries G1 and G2 (earlier
  batch grouped two-block precedent). Probe AC2 (locator p.1): 4 errors; AC1 (one block only) passes but would drop a
  printed block. Initials vs full list names automatic. ok.
- ciminelli2013 (5; printed, slots from header): Politecnico di Bari + Optoelectronics Laboratory, Bari, IT; Fraunhofer
  Institute for Telecommunications, Heinrich-Hertz-Institut, Berlin, DE (one org; probe CI2 split also passes, the
  institute name is one organization). Soares 2,3: marker 3 is a contact line (pymupdf first character); probe CI1
  (no dropped 3): 2 errors. ok.
- mao2008 (7; printed, slots from header): Institute of Microelectronics, Singapore, SG (A*STAR parent not copied,
  probe MA1 neutral); Nanyang Technological University + School of Electrical and Electronic Engineering, Singapore,
  SG; Xi'an Jiaotong University + School of Electrical and Information Engineering, Xi'an, CN (P.R.China printed;
  curly apostrophe as printed). Mao 1,2,3 (probe MA2 bound), Sun 1,2, Xu 3. ok.
- fang2011 (7; prose): Institute of Microelectronics, Singapore, SG (six authors; parent with expansion not copied);
  Song: statement block IME + clause Jilin University, College of Electronic Science and Engineering, Changchun, CN.
  Hong Cai / Ming Bin Yu vs list Hong Nian Cai / Ming Yu automatic. ok.
- acoleyen2011 (5; single, slots from header): Photonics Research Group, Department of Information Technology (INTEC),
  Ghent University - imec, BE; no city printed (Ghent only inside the org name), locality empty correct; probe AO1
  (Ghent) passes only because the org name contains it. ok.
- xuan2016 (19; printed, capitals): Purdue University + "School of Electrical and Computer Engineering and the Birck
  Nanotechnology Center", West Lafayette, US; Universidad Tecnológica de Pereira + Facultad de Ingenierías, Pereira,
  CO (department code after the city not recorded). Jaramillo-Villegas 1,2. Dagger equal contribution, asterisk
  contact. LI FAN slot 15: see F3. ok.
- quack2019 (9; prose): EPFL, Lausanne, CH (Quack, Sattari, Takabayashi); Zhang: Beihang University, Beijing, CN +
  clause EPFL; Verheyen: Interuniversity Microelectronics Centre (IMEC), Leuven, BE; Bogaerts: IMEC block followed by
  "Department of Information Technology" before the city + clause Center for Nano- and Biophotonics (NB Photonics),
  Ghent, BE (no parent printed, own org); Edinger, Errando-Herranz, Gylfason: KTH + two-part unit chain, Stockholm,
  SE. QU2 (P6 without clause flag) and QU3 (Bogaerts without P6) fail. The department on P5 is left out with the reason
  "unit and org must be contiguous": probe QU1 shows the org + following department passes (contiguous printed
  segment, org-first form as h48 shahin2025a block 3); see F1.
- sun2010 (2; single): Electroscience Laboratory, Department of Electrical and Computer Engineering, The Ohio State
  University (article kept), Columbus, US. ok.
- nedeljkovic2014 (10; prose "The authors are with", slots from header): University of Southampton +
  Optoelectronics Research Centre, Southampton, GB (U.K. printed). Printed order kept. ok.
- espinola2003 (4; prose): Columbia University + Microelectronics Sciences Laboratories (Espinola, Tsai, Osgood) /
  Center for Integrated Science and Engineering (Yardley), New York, US. "R. M. Osgood Jr." vs printed "R. M. Osgood,
  Jr." (punctuation folded). Probe ES1 bound. ok.
- lu2018 (14; printed, capitals): MIT EECS / Mechanical Engineering, Cambridge; RIT Microsystems Engineering,
  Rochester; Air Force Research Laboratory, Rome; Raytheon BBN Technologies, Cambridge; all US. Marker 6 is the
  equal-contribution line: dropped on Lu and Fanto (probes LU1 / LU2: 2 errors each). Fanto 2,3. ok.
- giuntoni2012 (7; printed, slots from header): Technische Universität Berlin + Fachgebiet Hochfrequenztechnik,
  Berlin, DE; IHP, Frankfurt (Oder), DE (as printed). Zimmermann and Tillack 1,2. ok.
- luke2013 (4; printed single block with marker 1, D285): Cornell University + School of Electrical and Computer
  Engineering, Ithaca, US. ok.

## Extractor calls (verified)

1. patel2014 partial: forced by the checker (PA2) and conform to D426 G4 / D599 cheung2015; unit article forced (PA1),
   lit_h09 rao2019 precedent. Correct.
2. Header order (fan2016, patel2014, ciminelli2013, mao2008, acoleyen2011, nedeljkovic2014, giuntoni2012): YAML order
   equals the printed author lines in both layers. Correct.
3. Name-order swaps isti2025 #2 and xuan2016 #15: the people are right (printed Xiaofeng Zhu / LI FAN = list Zhu
   Xiaofeng / Fan Li), but the explicit slots are not needed: probes IS1 / XU1 (no slot) pass with 0 errors and the
   FIX_all scratch `compare.csv` is byte-identical (same slots 2 and 15). Contract: `slot` only when the script cannot
   match; h48 li2025h precedent ("matched by name"). F2 / F3.
4. Prose footnotes (liu2022d, kobayashi2014, chen2016c, isti2025, fang2011, quack2019, nedeljkovic2014,
   espinola2003): every statement that names an author is recorded; clause blocks right after their statement;
   carriers exact (probes LD1, KO1, QU2, QU3, ES1 fail). Correct except the omitted quack2019 department (F1).
5. Cover pages guo2021 / acoleyen2012: p.2 locators forced (GU1 22 errors, AC2 4 errors); acoleyen2012 G1 / G2
   grouped, both blocks on every author, earlier-batch precedent. Correct.
6. ciminelli2013 Soares marker 3 dropped as contact: verified on the PDF (first character only). Correct.
7. quack2019 NB Photonics as own org: printed without a parent university; correct. Department after IMEC not
   recorded: not forced, see F1.
8. fan2016 symbol markers and "Klaus.-J Boller": symbols are the block legend markers; name as printed in both layers.
   Correct (O1).
9. liu2021b C2N as org with Paris-Saclay / CNRS in `more_orgs`: D466 form; probe LI1 neutral. Correct.
10. zhou2022c Kowloon, HK: first printed place, place Hong Kong printed without China; CN fails (ZH1). Correct.

## Fixes (exact YAML edits)

F1 (field accuracy; printed department omitted, note reason wrong). In `lit:quack2019` replace

```yaml
    - {marker: "P5", basis: prose, org: "Interuniversity Microelectronics Centre (IMEC)", locality: "Leuven", country: "BE", locator: "p.1 footnote"}
```

with

```yaml
    - {marker: "P5", basis: prose, org: "Interuniversity Microelectronics Centre (IMEC)", unit: "Department of Information Technology", locality: "Leuven", country: "BE", locator: "p.1 footnote"}
```

and in its note replace

```yaml
statement 5 prints a department after IMEC (not recorded: unit and org must be contiguous)
```

with

```yaml
statement 5 prints a department after IMEC (recorded as its unit, printed after the org)
```

Rows: one field (quack2019 #6 P5 unit) filled; nothing else changes.

F2 (contract: redundant explicit slot; note wording). In `lit:isti2025` replace

```yaml
    - {name: "Xiaofeng Zhu", markers: ["P1"], slot: 2}
```

with

```yaml
    - {name: "Xiaofeng Zhu", markers: ["P1"]}
```

and in its note replace `(name-order swap, slot set, D426 review list)` with
`(name-order swap, matched by name, D426 review list)`. Rows and `compare.csv` unchanged.

F3 (same as F2). In `lit:xuan2016` replace

```yaml
    - {name: "LI FAN", markers: ["1"], slot: 15}
```

with

```yaml
    - {name: "LI FAN", markers: ["1"]}
```

and in its note replace `(name-order swap, slot set, D426 review list)` with
`(name-order swap, matched by name, D426 review list)`. Rows and `compare.csv` unchanged.

Probe FIX_all (F1 + F2 + F3 on a scratch copy, derived files written there): 0 errors, 0 warnings; `compare.csv`
identical to the repo file; `header_rows.csv` differs only in the quack2019 #6 P5 unit.

## Observations (no change recommended)

- O1 fan2016 "Klaus.-J Boller" is a source typesetting error kept as printed (slots from header, no list name); the
  people build will carry that string. Candidate for the D412 / D426 name-review list.
- O2 patel2014 block 2 locality empty also passes (PA4): the known D599 gap (empty `locality` accepted when the block
  prints a city).
- O3 Explicit slots that equal the automatic match raise no warning (F2 / F3 passed the check silently).

## Open questions (with recommendation)

1. D426 review list: isti2025 #2 (Xiaofeng Zhu / Zhu Xiaofeng), xuan2016 #15 (LI FAN / Fan Li), chen2016c #1 (Hongtao
   / Hong Tao), fan2016 #8 (O1). Recommended: add.
2. Re-record list (D426 G4): patel2014 #4 Wei Shi present-address-only (Laval University). Recommended: add.
3. Org round: zhou2022c Kowloon vs Hong Kong locality (D599 question, already open).

## Unmapped org names (org round, no YAML change)

| printed org (unit) | place | proposal |
|---|---|---|
| Air Force Research Laboratory | Rome, US | new org |
| Center for Nano- and Biophotonics (NB Photonics) | Ghent, BE | new org or alias under Ghent University |
| Concordia University | Montreal, CA | new org |
| Hikvision Research Institute | Chengdu, CN | new org |
| IHP | Frankfurt (Oder), DE | alias to an IHP org if present, else new org |
| Interuniversity Microelectronics Centre (IMEC) | Leuven, BE | alias to org_imec (the "Center" spelling in chen2016c already maps there) |
| LioniX B.V. / SatraX B.V. / XiO Photonics B.V. | Enschede, NL | new orgs (LioniX alias if present) |
| NEC Yamanashi Ltd. (2 units) | Otsuki, JP | new org (NEC subsidiary) |
| Politecnico di Bari | Bari, IT | new org |
| Raytheon BBN Technologies | Cambridge, US | new org |
| Rochester Institute of Technology | Rochester, US | new org |
| The Ohio State University | Columbus, US | alias (article form) or new org |
| Universidad Tecnológica de Pereira | Pereira, CO | new org |
| Université Paris-Saclay | Palaiseau, FR | alias or new org |
| Xi'an Jiaotong University | Xi'an, CN | alias (curly apostrophe form) or new org |

(18 strings in `unmapped_orgs.csv`.)

## Privacy and as-printed scan

- Grep over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv` and `papers.csv` for contact / URL
  patterns, street / road / avenue / suite / room / building / box words, the street, park and building names printed
  in the sources, "No." + digit and digit runs of 4 or more: hits only for years inside paper ids and the generic
  words "building" (guo2021 note: a building name exists, not named) and "street" ("street address(es) not recorded").
  No contact, street, building name, postal code or P.O. box anywhere in the batch, notes included; fan2016 note uses
  the accepted "postal boxes" wording (h45 F1).
- As printed (kept, correct): "the Dept. of Electrical and Computer Engineering" (patel2014); NEC Ltd.; Ghent University-imec
  and Ghent University - imec (D426); The Ohio State University; Xi'an with curly apostrophe; MESA+ institute (lower case).

## Commands (2026-11-16, log times)

| Command | Result |
|---|---|
| `show lit_h49 --corpus lit --codes <id> --pdf`, all 26 (+ guo2021, acoleyen2012 `--pages 2`) | headers, statements and author lists read (scratchpad only) |
| pymupdf, ciminelli2013 source PDF page 1, first character of at-sign lines | 3 and asterisk: marker 3 is a contact line |
| `h49_audit/probes/probe.py` 23:50:36-23:53:50 | BASE 0 errors / 0 warnings; probes below |
| `h49_audit/probes/probe2.py` 23:54:41 (AC2) and 23:55:03-23:55:10 (FIX_all, written to scratch) | below; repo batch files md5 unchanged; probe checks wrote their usual logs under `logs/` (prefix `lit_headers_check_lit_p49`) |

| probe | change | result | reading |
|---|---|---|---|
| BASE | unchanged copy | 0 errors, 0 warnings | baseline |
| PA1 / PA2 / PA3 / PA4 | patel unit without article / Wei Shi readable / block 2 as affiliation / locality empty | 4 / 1 / 2 / 0 errors | article, unreadable, role forced; PA4 = O2 |
| GU1 | guo2021 locator p.1 | 22 errors | p.2 forced |
| AC1 / AC2 | acoleyen2012 one block only / locator p.1 | 0 / 4 errors | AC1 would drop a printed block; p.2 forced |
| CI1 / CI2 | ciminelli Soares no dropped 3 / Fraunhofer split | 2 / 0 errors | contact drop bound; split neutral |
| QU1 / QU2 / QU3 | quack P5 unit added / P6 no clause flag / Bogaerts without P6 | 0 / 2 / 3 errors | F1 valid; clause and carrier forced |
| FA1 / FA2 / FA3 | fan Boller normalized / Epping without dagger / MESA+ as org | 0 / 2 / 6 errors | O1; markers bound; unit chain forced |
| IS1 / XU1 | isti / xuan explicit slot removed | 0 / 0 errors | F2 / F3 |
| ZH1 / ZH2 | zhou2022c block 2 CN / locality Hong Kong | 2 / 0 errors | HK forced; Kowloon per D288 |
| LI1 | liu2021b Paris-Saclay org, C2N unit | 0 errors | neutral; D466 form kept |
| LU1 / LU2 | lu2018 Lu / Fanto without dropped 6 | 2 / 2 errors | bound |
| MA1 / MA2 | mao A*STAR as more_orgs / Mao without 3 | 0 / 2 errors | parent rule; bound |
| AO1 | acoleyen2011 locality Ghent | 0 errors | Ghent only inside the org name; empty kept |
| KO1 / CH1 / LD1 / ES1 | kobayashi Yamazaki to P2 / chen DTU with article / liu2022d Lu without P3 / espinola Yardley P1 | 4 / 0 / 2 / 5 errors | carriers bound; CH1 neutral |
| FIX_all | F1 + F2 + F3 | 0 errors, 0 warnings | compare.csv identical; one header_rows field changes |

## Checker gaps observed (scripts not edited)

- Present-address-only author (D426 G4): patel2014 #4.
- Empty `locality` accepted when the block prints a city (D599): PA4.
- Redundant explicit slots pass without a warning (F2 / F3).
- An org-first block with a following department passes with or without the unit (QU1): omission is not caught.

## Verdict

GO with fixes F1-F3. All 188 list slots carry the right person; the 187 recorded slots have the right markers, org,
city and country, and all units except the omitted IMEC department (F1); patel2014 #4 correctly has no rows. Nothing
is invented, no block is missed, no contact, street, building, postal-box or postal-code text is recorded. F2 / F3
remove two explicit slots the checker does not need and correct the notes; no row changes.
