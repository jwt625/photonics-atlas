---
title: Fresh-context audit of the lit author-affiliation batch lit_h45 (24 papers)
date: 2026-11-15
mode: read-only on the batch (wrote only this record and scratchpad show outputs / probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only with --dry-run, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h45/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D412, D416, D426, D442, D466, D546, D557, D565, D572); format from the 2026-11-15 h43 / h44 audits; read-only comparison with earlier batches (CityU Kowloon, UCSB / UC Davis campus, Grenoble CEA LETI, WNLO, IBM Zurich, Jiaxing / Ningbo Research Institute, lit_h17 barwicz2016 records)
verdict: GO with 2 fixes; 192 list slots + 1 header-only author audited; 190 ok, 1 imprecise (subramanian2012 #1 present address not recordable, checker gap), 1 open org-form question (qiu2018 #3), 0 wrong; F1 note wording (P.O. boxes -> postal boxes, 2 notes), F2 qiu2018 note (wrong precedent claim); optional N1 (snigirev2023 legend); one ruling question (qiu2018 P4 org form, alternative Q1 probed)
---

# Lit header batch audit: lit_h45 (2026-11-15)

## Scope

Batch lit_h45: 24 papers (IEEE journals 9 (JLT x3, PTL x2, JSTQE x2, Photonics Journal x2), Optics Express / Optica
Publishing 5, preprints 7, PhotoniX 1, IEEE Photonics Journal cover-page paper 1, conference digest 1); 192 list
slots (161 from author lists, 31 from headers in the 5 `slots_from_header` papers) plus 1 header-only author (shu2026
Yueyang Zhang, slot 0); 221 rows. Restricted corpus: this record names only authors, orgs, units, cities and
countries; no paper text is quoted and no contact, street, building, postal-box or postal-code text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h45 --corpus lit --codes <id> --pdf`
  (all 24; shang2017a also with `--pages 2`; output in the scratchpad only). Marker runs compared in both layers.
- Symbol legends read on page 1, or in `references/snigirev2023/text.md` (legend on page 8).
- Per slot: printed name vs `compare.csv` and the `show` list (29 name differences read, all automatic matches or
  the 3 explicit slots); marker run; block fields (org, unit chain, more_orgs, campus, city, country); role; locator;
  grade. Every distinct (paper, org, city, country, org id, match basis, role, basis, locator) tuple of
  `header_rows.csv` read (65 tuples, 221 rows).
- Prose papers (ning2022, park2007, pathak2012a, poulton2019, qiu2018, sciancalepore2014, subramanian2012, tran2019,
  tu2024): every statement subject, verb, clause and field read against the footnote (21 prose blocks).
- Corpus precedents read for every judgment call (grep over committed `headers.yaml`, registry lookups).
- Probes on scratch copies (`h45_audit/probes/probe.py` in the session scratchpad, scratch `LIT_BASE`, batch name
  `lit_p45`, `cmd_check(..., dry_run=True)`). md5 of every repo batch file identical before and after the audit;
  `check_stamp.txt` matches `headers.yaml` (sha256 23fc7b73...).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | open | wrong |
|---|---|---|---|---|---|---|
| lit_h45 | 24 / 24 | 192 + 1 header-only | 191 | 1 | 1 | 0 |

- Rows 221 (all grade A: printed 136, prose 73, single 12; primary 198, additional 23, present address 0); recorded
  191, no_header 1 (shu2026 #3, list name Yaci Zhang not printed); papers ok 24, partial 0, unreadable 0;
  `slots_from_header` 5 (oldenbeuving2012, pathak2012a, runge2015, sciancalepore2014, subramanian2012);
  `author_list_differs` 1 (shu2026); explicit slots 3 (rees2020 #6, rudenkov2025 #3, shang2017a #4) plus slot 0
  (shu2026 Yueyang Zhang, no rows; goes to the extra-authors list via `aggregate`); `order_differs` 1 (snigirev2023);
  multi-affiliation slots 20; 19 unmapped org strings.
- Per paper (slots / rows): nejadriahi2024 11 / 11; ning2022 6 / 7; oldenbeuving2012 6 / 12; park2007 6 / 6;
  pathak2012a 5 / 5; poot2014 2 / 2; poulton2019 7 / 7; qiu2018 9 / 10; rees2020 7 / 8; riedhauser2025 7 / 7;
  rudenkov2025 6 / 8; runge2015 5 / 5; sacher2019 12 / 16; sciancalepore2014 11 / 18; shang2017a 4 / 4; shang2023
  8 / 8; shu2026 22 (+1 slot 0) / 25; snigirev2023 16 / 17; stokowski2023 9 / 11; subramanian2012 4 / 4; sun2017
  3 / 3; sun2018 10 / 11; tran2019 6 / 6; tu2024 10 / 10.

### Per-slot field counts

| field | ok | imprecise | open | wrong |
|---|---|---|---|---|
| name / slot (192 + 1) | 193 | 0 | 0 | 0 |
| markers (193) | 193 | 0 | 0 | 0 |
| header position (193) | 193 | 0 | 0 | 0 |
| blocks (org / unit / campus / locality / country) (191 with rows) | 190 | 0 | 1 (qiu2018 #3, question 1) | 0 |
| additional / present-address blocks | all recorded ones | 1 missing (subramanian2012 #1 present address, call 2) | 0 | 0 |
| prose blocks (21 blocks, 9 papers) | 21 | 0 | 0 | 0 |
| locators (all blocks) | all | 0 | 0 | 0 |
| notes (24) | 20 | 4 (F1 x2 wording, F2 qiu2018 precedent claim, N1 snigirev2023 legend) | 0 | 0 |

## Per-paper findings

- nejadriahi2024 (11; printed, capitals): JPL, Pasadena, US (Caltech parent not copied, D416 / lit_h07 ledezma2022
  rule); University of California + campus Santa Barbara + ECE, Santa Barbara, US (`org_ucsb`). Runs 1 / 1 / 2 / 2 /
  2 / 1 / 1 / 2 / 2 / 1 / 2 as printed in both layers; asterisk on Nejadriahi = contact. Eric Kittlaus vs list Eric A.
  Kittlaus automatic. ok.
- ning2022 (6; prose): P1 Zhejiang University + College of Information Science and Electronic Engineering, Hangzhou
  (5 authors); P2 same org for Hui Yu (second statement, own block, as the contract requires) + clause P3 Zhijiang Lab,
  Hangzhou; all CN. Probe C1: clause bound. ok.
- oldenbeuving2012 (6; printed, closing-parenthesis markers, slots from header): blocks 1-7 exact (University of
  Twente + Laser Physics and Nonlinear Optics group; MESA+ Research Institute for Nanotechnology printed alone, as org;
  XiO Photonics; University of Twente + Optical Sciences group; FOM Institute DIFFER, Nieuwegein; Delft University of
  Technology + Delft Center for Systems and Control; Zhejiang University + Institute of Underwater Technology and Ship
  Engineering, Hangzhou, CN); NL otherwise. Runs 1,2 / 3 / 2,4 / 1,2,5 / 6,7 / 1,2; marker a = contact line (probe
  M3: bound). Note wording "P.O. boxes" (F1). ok.
- park2007 (6; prose): P1 "University California Santa Barbara" printed without "of" and without comma; recorded as
  org University California + campus Santa Barbara (probe O1: the "of" form fails, so as printed is forced); ECE unit,
  Santa Barbara, US. P2 Intel Corporation + Photonics Technology Laboratory, Jerusalem, IL. Oded Cohen / Oded M. Cohen
  and John E. / John Edward Bowers automatic. ok.
- pathak2012a (5; prose, "The authors", slots from header): Ghent University-IMEC (dash-joined, D426 kept as printed;
  maps by alias to Ghent University + imec) + Department of Information Technology, Ghent, BE. ok.
- poot2014 (2; printed single block with marker 1): Yale University + Department of Electrical Engineering, New
  Haven, US. Asterisk and dagger = contact lines. ok.
- poulton2019 (7; prose, "The authors"): Analog Photonics, Boston, US (leading article after the verb not copied,
  corpus practice; probe O2 shows the checker accepts either). ok.
- qiu2018 (9; prose): P1 Longyan University + Department of Mechanical and Electrical Engineering, Longyan, CN + clause
  P2 University of British Columbia + ECE, Vancouver, CA (probe C2: bound); P3 Zhejiang University + Department of
  Information Science and Electronics Engineering, Hangzhou, CN (5 authors); P4 Ping Yu, printed Ningbo Institute of
  Technology before Zhejiang University, Ningbo, CN, recorded as ZJU + unit (row maps to `org_zhejiang_university`);
  P5 UBC + ECE, Vancouver, CA. Statement membership exact (probe C3). The note's precedent claim is wrong: the
  earlier ZJU blocks (lit_h11, h20, h42, h44) print "Ningbo Research Institute", a different name (F2); org form is
  question 1. Markers and slots ok.
- rees2020 (7; printed): University of Twente + unit chain (group, Mesa+ institute, department), Enschede, NL;
  LioniX International B.V., Enschede, NL. Runs 1 / 1,2 / 2 / 2 / 2 / 1 / 1; markers 3, 4 contact lines (probes M1,
  M4: both bound). #6 Peter J.M. vs list Petrus J.M. van der Slot: explicit slot required (probe S1), D287 (nickname,
  initials agree). Note wording "P.O. boxes" (F1). ok.
- riedhauser2025 (7; printed single block with marker 1, capitals): both layers print the umlaut of Möhl and of Zürich
  as a yen sign; intended letters written (D282; list prints Charles Möhl; Rüschlikon prints its umlaut correctly).
  IBM Research Zürich (no separator, as printed) maps to `org_ibm_research_zurich`; locality Rüschlikon (city printed
  after the street), CH. Dagger = equal contribution, asterisk = contact. ok.
- rudenkov2025 (6; printed, capitals): NTNU + Department of Physics, Trondheim, NO; Vienna University of Technology +
  Photonics Institute, Vienna, AT; ATLA Lasers AS, Trondheim, NO. Runs 1 / 1 / 1 / 1 / 2,3 / 1,3. #3 Maxim vs list
  Maksim Demesh: explicit slot required (probe S2), D287 transliteration. ok.
- runge2015 (5; single, slots from header): Fraunhofer Heinrich-Hertz-Institute, Berlin, DE. ok.
- sacher2019 (12; printed, capitals): Caltech + Division of Physics, Mathematics, and Astronomy, Pasadena, US;
  University of Toronto + ECE, Toronto, CA; Max Planck Institute of Microstructure Physics, Halle, DE; Advanced Micro
  Foundry Pte Ltd, Singapore, SG (`org_amf`); Institute of Microelectronics, Singapore, SG (A*STAR parent not copied;
  `org_astar_ime` by ROR, as lit_h44 li2013). All 12 runs exact. ok.
- sciancalepore2014 (11; prose, slots from header): P1 Université Grenoble Alpes + `more_orgs` CEA / unit LETI,
  Grenoble, FR (the form of lit_h07, h09, h13, h14; 7 authors); P2 Photon Design Ltd., Oxford, GB; P3 Vistec Electron
  Beam GmbH, Jena, DE. Site names after LETI not recorded (named in the note, as earlier campus-name notes). ok.
- shang2017a (4; single, cover page): page 2 read in both layers; University of California + campus Davis + ECE,
  locality Davis, US, `p.2 header` (8 earlier Davis blocks identical in form). #4 S. J. Ben Yoo vs list Sung Jong Yoo:
  explicit slot required (probe S3), D287 alternate given name, initials agree. ok.
- shang2023 (8; printed): City University of Hong Kong + department & state key laboratory (one unit segment),
  locality Kowloon, HK (CityU precedent, 11+ records; probe L1: Hong Kong also passes; corpus rule still open from
  the h43 audit question 4); Georgia Tech + School of ECE, Atlanta; MIT + Department of Mathematics, Cambridge;
  Virginia Polytechnic Institute and State University + ECE, Arlington; US. Dagger = equal contribution. ok.
- shu2026 (22 + 1; printed, PhotoniX side column): blocks exact. 1 Zhejiang University + four-part chain, Hangzhou
  (Zijingang Campus not recorded, lit_h44 precedent); 2 University of Chinese Academy of Sciences + Hangzhou Institute
  for Advanced Study, Hangzhou (province printed first, not recorded); 3 Westlake University + School of Engineering,
  Hangzhou (district not recorded); 4 China Jiliang University, Hangzhou; 5 Zhejiang University + research center /
  Jiaxing Research Institute chain, Jiaxing (form of the earlier Jiaxing blocks); all CN. All 22 runs exact (Yu 1,5;
  Shi 1,5; Dai 1,4,5). Author 3 printed Yueyang Zhang, list Yaci Zhang: different given name, `slot: 0` +
  `author_list_differs` required (probe SHU1); list slot 3 no_header. #22 Daoxin Dai A list artefact (D412). ok.
- snigirev2023 (16; printed): EPFL long name with (EPFL) + Institute of Physics, Lausanne (`org_epfl` alias); IBM
  Research Europe + campus Zurich, locality Rüschlikon (see call 3); ETH Zürich long name + Integrated Systems
  Laboratory, Zürich; all CH. All 16 runs exact (Popoff 2,3). Asterisk = equal contribution; dagger and double dagger
  = contact lines (legend on page 8; the note calls them corresponding authors: N1). Printed order differs from the
  list: warning, expected. ok.
- stokowski2023 (9; printed): Stanford + Department of Applied Physics and Ginzton Laboratory (one unit segment),
  Stanford; NTT Research, Inc. + Physics & Informatics Laboratories, Sunnyvale (`org_ntt_research`); Stanford +
  Department of Electrical Engineering; US. Runs exact; marker 4 = contact line on the last author (probe M2: not
  bound, known G1 gap). Taewon / Tae-Won Park automatic. ok.
- subramanian2012 (4; prose, slots from header): P1 (was with) University of Southampton + Optoelectronics Research
  Centre, Southampton, GB for author 1; P2 same for authors 2-4. Author 1's present-address statement (pronoun
  subject) not recorded; see call 2. The note carries the re-record values (org / unit / city / country only). #1
  imprecise (missing present-address row).
- sun2017 (3; single, capitals): University of Toronto + Department of Electrical & Computer Engineering, Toronto, CA.
  ok.
- sun2018 (10; printed, capitals): University of Virginia + ECE, Charlottesville; UC + campus Santa Barbara + ECE /
  Materials Department, Santa Barbara (printed without a comma); US. Bowers 2,3. ok.
- tran2019 (6; prose): P1 UC + campus Santa Barbara + ECE (5 authors); P2 Morton Photonics, West Friendship; US. ok.
- tu2024 (10; prose): P1 HUST + WNLO & school (one unit segment, 7 earlier records of this exact form), Wuhan
  (8 authors); P2 Ningbo Ori-Chip Optoelectronics Technology Company Ltd., Ningbo (Dai, Mingzhi Lu); CN. ok.

## Extractor calls (verified)

1. shu2026 `author_list_differs`: Yueyang vs Yaci share no given-name part; D287 forbids an explicit slot. Probe SHU1
   (no slot): 1 error (slot required). Probe SHU2 (`slot: 3`, flag removed): 0 errors, so the checker would accept a
   D287-violating slot here (known D572 gap: explicit slot skips the D369 initials check). The extractor's form is the
   correct one. Keep; Yaci Zhang (#3) and Daoxin Dai A (#22) go to the D412 correction file.
2. subramanian2012 "He is now with" block left out. Probe SUB1 (present-address prose block P2 Ghent University +
   Photonics Research Group, Department of Information Technology, Gent, BE, carried by author 1): 2 errors (author not
   named in the statement subject: the pronoun is not resolved after the period of "U.K."); SUB2 (same without the
   role): 4 errors. Forced. The note's "lit barwicz2016 precedent" is the same gap family (D426 G2, pronoun statement;
   there after a comma, here after an abbreviation period). Keep; add to the re-record list.
3. snigirev2023 IBM Research Europe + campus Zurich + locality Rüschlikon. IBM Research Europe has several labs, and
   the printed "Zurich" names the lab, not the city of the block (Rüschlikon is printed after the street), so D301
   campus is a fair reading; it also keeps the row from mapping a bare "IBM Research Europe" to one lab. Probes SNI1
   (no campus) and SNI2 (locality Zurich, no campus): 0 errors each, so the checker is neutral. Earlier records print
   "IBM Research Europe – Zurich" as one org (lit_h02, lit_h27). Keep; org round alias "IBM Research Europe, Zurich" ->
   `org_ibm_research_zurich`.
4. riedhauser2025 umlaut repairs (Möhl, Zürich): yen sign in both layers is a D282 artefact; the list spells Charles
   Möhl and the block prints Rüschlikon with its umlaut. Correct.
5. Parents left out (D416): nejadriahi2024 JPL without Caltech, sacher2019 IME without A*STAR. Correct, corpus rule.
6. qiu2018 Ningbo Institute of Technology as a unit of Zhejiang University: structurally consistent with the printed
   order and passes; the stated precedent is a different body (F2). See question 1 for the org form.
7. Explicit slots required: rees2020 #6 (S1), rudenkov2025 #3 (S2), shang2017a #4 (S3). All D287-conform.

## Fixes (exact YAML edits)

F1 (note wording; privacy-scan hygiene). Two notes use the token "P.O. boxes" (no box value is recorded anywhere);
the corpus wording is "postal box". In `lit:oldenbeuving2012` replace

```yaml
P.O. boxes, street addresses and postal codes not recorded
```

with

```yaml
postal boxes, street addresses and postal codes not recorded
```

and in `lit:rees2020` replace

```yaml
P.O. boxes and postal codes not recorded
```

with

```yaml
postal boxes and postal codes not recorded
```

Rows unchanged.

F2 (note, factual). In `lit:qiu2018` replace

```yaml
statement 3 prints the Ningbo Institute of Technology before Zhejiang University (recorded as unit, as the Zhejiang University Ningbo Research Institute blocks of earlier batches)
```

with

```yaml
statement 3 prints Ningbo Institute of Technology before Zhejiang University (recorded as unit by the printed order; a different name from the Zhejiang University Ningbo Research Institute blocks of earlier batches; org form open in the lit_h45 audit)
```

Rows unchanged. Superseded by Q1 below if question 1 is decided for the whole-name form.

N1 (optional, note). In `lit:snigirev2023` replace

```yaml
dagger and double dagger the corresponding authors (symbols used by no block)
```

with

```yaml
dagger and double dagger point to contact lines (legend on page 8; symbols used by no block)
```

Probe FIX_all (F1 + F2 + N1 on a scratch copy): 0 errors, 4 warnings (3 explicit slots; snigirev2023 order differs).

## Open questions (with recommendation)

1. qiu2018 P4 org form. Auditor background knowledge, not verifiable offline (no local source names the
   institution apart from this paper): Ningbo Institute of Technology, Zhejiang University was an independent college
   founded by Zhejiang University in Ningbo and later renamed; if so, "Ningbo Institute of Technology, Zhejiang
   University" is the institution's full name (like "Institute of Semiconductors, Chinese Academy of Sciences"), and
   the unit form gives Ping Yu a Zhejiang University row. Alternative Q1 (replaces F2):

   ```yaml
       - {marker: "P4", basis: prose, org: "Ningbo Institute of Technology, Zhejiang University", locality: "Ningbo", country: "CN", locator: "p.1 footnote"}
   ```

   and in the note replace the F2 source clause with
   `statement 3 prints Ningbo Institute of Technology, Zhejiang University (recorded whole as org: the name of a Ningbo institution, not the Zhejiang University Ningbo Research Institute of earlier batches)`.
   Probe FIX_q1 (F1 + Q1 + N1): 0 errors, 4 warnings; the row becomes unmapped (org round, new org). Probe QIU2
   (bare "Ningbo Institute of Technology", parent dropped) also passes but the bare name is less distinctive.
   Recommended: confirm the institution's status in the org round, then apply Q1; until then apply F2.
2. subramanian2012 #1 to the re-record list (pronoun present-address statement after "U.K."; values in the note: Ghent
   University, Photonics Research Group, Department of Information Technology, Gent, BE, role present_address).
   Recommended: yes.
3. D412 correction file: shu2026 #3 (list Yaci Zhang, printed Yueyang Zhang) and #22 (Daoxin Dai A). D426 review list:
   rees2020 #6 (Peter / Petrus), rudenkov2025 #3 (Maxim / Maksim), shang2017a #4 (Ben / Sung Jong). Recommended: add.
4. G1 test list (last author's dropped marker not bound): stokowski2023 #9 Safavi-Naeini (probe M2); rees2020 #6
   (not the last author) is bound (M4). Recommended: add stokowski2023 #9 to the D442 / D546 /
   D557 list.
5. HK locality: shang2023 Kowloon follows the CityU precedent; the corpus rule is still the h43 audit question 4.
   No change here.

## Unmapped org names (org round, no YAML change)

| printed org (unit) | place | proposal |
|---|---|---|
| ATLA Lasers AS | Trondheim, NO | new org |
| China Jiliang University | Hangzhou, CN | new org |
| FOM Institute DIFFER | Nieuwegein, NL | new org |
| IBM Research Europe, Zurich (campus form) | Rüschlikon, CH | alias to `org_ibm_research_zurich` (with the earlier "IBM Research Europe – Zurich" strings) |
| Jet Propulsion Laboratory | Pasadena, US | new org (none in the registry) |
| LioniX International B.V. | Enschede, NL | alias to `org_lionix_international` (registry "LioniX International BV") |
| Longyan University (department) | Longyan, CN | new org |
| MESA+ Research Institute for Nanotechnology | Enschede, NL | alias to `org_mesa_plus_institute_for_nanotechnology` |
| Morton Photonics | West Friendship, US | new org (with lit_h44 "Morton Photonics Inc.") |
| Ningbo Ori-Chip Optoelectronics Technology Company Ltd. | Ningbo, CN | new org |
| Norwegian University of Science and Technology (Department of Physics) | Trondheim, NO | new org |
| Photon Design Ltd. | Oxford, GB | new org |
| Swiss Federal Institute of Technology Zurich (ETH Zürich) (Integrated Systems Laboratory) | Zürich, CH | alias to `org_eth_zurich` |
| University California, Santa Barbara (printed without "of"; ECE) | Santa Barbara, US | alias to `org_ucsb` |
| Vienna University of Technology (Photonics Institute) | Vienna, AT | new org |
| Virginia Polytechnic Institute and State University (ECE) | Arlington, US | alias to `org_virginia_tech` |
| Vistec Electron Beam GmbH | Jena, DE | new org (registry `org_vistec_lithography` is a different company name; check) |
| XiO Photonics | Enschede, NL | new org |
| Zhijiang Lab | Hangzhou, CN | alias to `org_zhejiang_lab` (printed transliteration) |

(19 strings in `unmapped_orgs.csv`.)

## Privacy and as-printed scan

- Scan over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`, `papers.csv` and
  `check_stamp.txt` for contact / URL patterns, street / road / avenue / suite / room / building words, postal-box
  words, "No." + digit and digit runs of 4 or more: no contact address, street name, building name, postal code or
  postal-box value anywhere. Hits are descriptive only: "street address(es) ... not recorded" and "after the street"
  (riedhauser2025, snigirev2023), "a science park name" (sacher2019, name not given), site / campus names in notes
  (sciancalepore2014 MINATEC campus and CEA-Grenoble site; shu2026 Zijingang Campus; both with earlier precedent), and
  the token "P.O. boxes" in two notes (F1). The word e-mail appears nowhere.
- `show` masking gap (outside the batch, known from the h44 audit): fragments of line-broken contact addresses stay
  unmasked in ning2022, park2007, pathak2012a, subramanian2012 and tu2024 (text and PDF layers). Not copied into the
  batch or this record.
- As printed (kept, correct): University California (park2007); Ghent University-IMEC; Mesa+ inside the rees2020
  chain vs MESA+ block in oldenbeuving2012; IBM Research Zürich without separator; Department of Electrical &
  Computer Engineering (sun2017); Morton Photonics without Inc. (tran2019).

## Commands (2026-11-15 / 2026-11-16, log times)

| Command | Result |
|---|---|
| `check lit_h45 --corpus lit --dry-run` 2026-11-15 23:56:56 (pid 93882) | 0 errors, 4 warnings (3 explicit slots; snigirev2023 order differs); slots 192, recorded 191, no_header 1; rows 221 (grade A 221; printed 136, prose 73, single 12; primary 198, additional 23); papers ok 24; slots_from_header 5; multi-affiliation slots 20; 19 unmapped org strings |
| `show lit_h45 --corpus lit --codes <id> --pdf`, all 24 (+ shang2017a `--pages 2`) | headers, statements and author lists read (scratchpad only) |
| `h45_audit/probes/probe.py` on scratch copies, 2026-11-16 00:00:13-00:04:23 | below; repo batch files md5 unchanged; probe checks wrote their usual logs under `logs/` (prefix `lit_headers_check_lit_p45`, 50 files) |

| probe | change | result | reading |
|---|---|---|---|
| BASE | unchanged copy | 0 errors, 4 warnings | baseline |
| SUB1 | subramanian2012 present-address block for author 1 | 2 errors | pronoun not resolved (call 2) |
| SUB2 | same, role affiliation | 4 errors | cue bound to role; pronoun gap |
| SHU1 | shu2026 Yueyang Zhang without slot 0 | 1 error | slot 0 required |
| SHU2 | shu2026 Yueyang Zhang slot 3, no list flag | 0 errors | checker accepts a D287-violating slot (known gap) |
| SNI1 / SNI2 | snigirev2023 no campus / locality Zurich | 0 errors each | checker neutral (call 3) |
| QIU1 / QIU2 | qiu2018 P4 whole name / bare NIT as org | 0 errors each | checker neutral (question 1) |
| S1 / S2 / S3 | explicit slot removed (rees2020 #6, rudenkov2025 #3, shang2017a #4) | 2 errors each | slots required |
| M1 / M4 | rees2020 dropped 3 (van Rees) / dropped 4 (van der Slot) removed | 2 errors each | bound |
| M2 | stokowski2023 Safavi-Naeini dropped 4 removed | 0 errors | G1 (last-author gap) |
| M3 | oldenbeuving2012 dropped a removed | 2 errors | bound |
| C1 / C2 | ning2022 Hui Yu / qiu2018 Qiu without clause block | 3 errors each | clauses bound |
| C3 | qiu2018 Ping Yu on P3 | 5 errors | statement membership bound |
| L1 | shang2023 locality Hong Kong | 0 errors | checker neutral (question 5) |
| O1 | park2007 org University of California | 4 errors | as-printed form forced |
| O2 | poulton2019 org "the Analog Photonics" | 0 errors | leading article neutral |
| Y1 | shu2026 block 2 locality "" | 0 errors | empty locality accepted with a printed city (gap, below) |
| FIX_all | F1 + F2 + N1 | 0 errors, 4 warnings | fixes valid |
| FIX_q1 | F1 + Q1 + N1 | 0 errors, 4 warnings | question 1 alternative valid |

## Checker gaps observed (scripts not edited)

- G1 Last author's further markers not bound: stokowski2023 #9 (M2). Known (D442 / D546 / D557 / D572).
- Pronoun present-address statement after an abbreviation period ("U.K."): subramanian2012 (SUB1). Same family as
  D426 G2; re-record after the fix.
- Explicit slot skips the D369 / D287 name check (SHU2). Known (D572).
- Empty `locality` accepted for a block that prints a city (Y1). Not seen in earlier audit records; YAML exact.

## Verdict

GO with fixes F1 and F2 (note edits only; rows unchanged). All 192 list slots and the header-only author carry the
right person; the 191 slots with rows have the right markers, org, unit, campus, city and country, with one org form
open (qiu2018 P4, question 1) and one present address not recordable until the checker fix (subramanian2012 #1).
Nothing is invented, no block is missed apart from that checker-forced present address, and no contact, street,
building, postal-code or postal-box value is recorded.
