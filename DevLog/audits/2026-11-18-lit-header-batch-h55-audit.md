---
title: Fresh-context audit of the lit author-affiliation batch lit_h55 (17 papers)
date: 2026-11-18
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only with --dry-run, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h55/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D412, D426, D466, D521, D522, D599, D629, D644, D659); format from the lit_h53 audit
verdict: GO after F1 (cao2021 block 6, IEMN as the org with Université Polytechnique Hauts-de-France in more_orgs, D285 / D466); 129 slots (88 list + 41 slots_from_header) audited, 127 ok, 2 imprecise (fixed by F1), 0 wrong; 1 optional note fix (N1 liu2022f)
---

# Lit header batch audit: lit_h55 (2026-11-18)

## Scope

Batch lit_h55: 17 papers (JLT / JSTQE / PTL footnote statements, two IEEE conference papers with per-author blocks,
one VLSI conference paper, one arXiv preprint, one Springer review, one IEEE Photonics Journal paper with a cover
page, one HAL manuscript of a Wiley paper with grouped blocks); 129 slots (ghosh1996 7, nykolak1993 5, cao2021 17,
rouvie2008 6, cezar2024 6 `slots_from_header`); 135 rows. Restricted corpus: this record names only authors, orgs,
units, cities and countries; no paper text is quoted and no contact, street, building or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h55 --corpus lit --codes <id> --pdf`
  (all 17; cao2021 and kim2017 also with `--pages 2`; output kept in the session scratchpad `h55_audit/show/` only).
- Per slot: printed name vs the `show` author list and `compare.csv`; marker run / group / statement subject in both
  layers; block fields (org, unit chain, city, country); locator; notes.
- cao2023 grid read from the PDF word positions (PyMuPDF, scratch only): row 1 Cao / Xiang / Sun, row 2 Xie / Guo / Dai;
  both text layers read it column by column. liu2022f author-line spans read the same way (see N1).
- All 135 rows of `header_rows.csv` read (distinct tuples per paper / marker); `compare.csv` 129 rows all `recorded`.
- Precedent greps over all `lit_headers` / `ofc_headers` YAMLs and `data/registry/`: Bell Labs forms, HP Labs forms,
  French joint research units (UMR), A*STAR institutes, Center for Interdisciplinary Research and Innovation, Ulsan.
- Probes on scratch copies (`h55_audit/probes/probe.py`, scratch `LIT_BASE`, batch name `lit_p55`,
  `cmd_check(..., dry_run=True)`): table below. md5 of every repo batch file identical before and after the audit;
  `check_stamp.txt` matches `headers.yaml` (sha256 9be588c9...). Probe checks wrote their usual logs under `logs/`
  (prefix `lit_headers_check_lit_p55`).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h55 | 17 / 17 | 129 | 127 | 2 (cao2021 #10, #15: F1) | 0 |

- Rows 135 (all grade A: prose 68, single 26, grouped 21, per_author 12, printed 8; primary 129, additional 6, present
  address 0); recorded 129, no_header 0; papers ok 17, partial 0, unreadable 0; `slots_from_header` 5;
  `author_list_differs` 0; explicit slots 0; multi-affiliation slots 6; 11 unmapped org strings; 1 warning (cao2023
  printed order). After F1: rows 137 (grouped 23), 12 unmapped strings, 0 errors (probe C1).
- Per paper (slots / rows): shimizu2024 9 / 11; chrysostomidis2021 10 / 10; ghosh1996 7 / 7; nykolak1993 5 / 5;
  liu2022f 8 / 8; zhu2017 3 / 3; zhang2022e 16 / 16; pfeiffer2018 6 / 6; gundlapalli2022 8 / 8; cao2021 17 / 21;
  rouvie2008 6 / 6; yanikgonul2022 3 / 3; okimoto2023 8 / 8; yuan2021 7 / 7; cao2023 6 / 6; cezar2024 6 / 6; kim2017 4 / 4.

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (129) | 129 | 0 | 0 |
| markers / groups / statement carriers (129) | 129 | 0 | 0 |
| prose subjects / clauses (68 rows, 10 papers) | all | 0 | 0 |
| blocks (org / unit / locality / country) | 127 | 2 (cao2021 G6 form, F1) | 0 |
| locators | all | 0 | 0 |
| notes (17) | 16 | 1 (liu2022f, N1 optional) | 0 |

## Per-paper findings

- shimizu2024 (9; prose): NTT Corporation with NTT Network Innovation Laboratories, Yokosuka (P1) and NTT Device
  Technology Laboratories, Atsugi (P2, P4); statement 2 (Kazama, Umeki) has the "and also with" clause P3 (Network
  Innovation Laboratories, Yokosuka). Carriers verified (probe S1: 2 errors without P3). ok.
- chrysostomidis2021 (10; prose): Aristotle University of Thessaloniki with "Department of Physics and Center for
  Interdisciplinary Research and Innovation" (P1: Chrysostomidis, Roumpos, Vyrsokinos) and the Informatics form (P2:
  Fotiadis, Manolis, Vagionas, Alexoudi); University of Twente, IOS Group, MESA+ chain, Enschede, NL (P3: Mu,
  Dijkstra, Garcia Blanco). See call 8. ok.
- ghosh1996 (7; prose, slots from header): "The authors are with" Lucent Technologies, Bell Laboratories, Murray Hill,
  US; the statement's second line is separated from the first by other footnote lines in both layers, the checker
  still finds city and country. See call 4. ok.
- nykolak1993 (5; prose, slots from header): page 1 opens with the reference list of the preceding paper, header
  follows; AT&T Bell Laboratories, Murray Hill, state only, `country: ""` (probe N1 "US": 2 errors). "Member, ZEEE"
  (OCR of IEEE) after the last name is not part of the name. ok.
- liu2022f (8; printed single footnote block with marker 1, D285): Chongqing United Microelectronics Center, Chongqing,
  CN. Li Jin vs list Jin Li (call 5). Note wording N1. ok.
- zhu2017 (3; prose): Fujikura Ltd., Advanced Technology Laboratory, Sakura, JP (prefecture not recorded). ok.
- zhang2022e (16; single, VLSI Symposium 2022): NUS (NUS) with the ECE department; postal code then Singapore printed
  once (locality and country, corpus practice, lit_h53 du2019). Asterisk on Xiao Gong leads the contact line. ok.
- pfeiffer2018 (6; single, arXiv): EPFL (EPFL) printed before the laboratory LPQM, Lausanne, CH. Arslan S. Raja and
  Tobias J. Kippenberg vs list full middle names: automatic, initials agree. ok.
- gundlapalli2022 (8; prose): IMRE (P1: Gundlapalli, Leong, Krivitsky), IHPC (P2: Ong, Ang, Png), Advanced Micro
  Foundry (P3: Yanikgonul, Siew), all Singapore, SG. Same strings as lit_h24. See calls 7 and 8. ok.
- cao2021 (17; grouped, slots from header, p.2 header): six groups verified against the p.2 layout: G1 ECE (10 names),
  G2 Physics (Cao, Wee, Venkatesan), G3 MSE (Li, Yang, Pennycook), G4 NGS (Tang), G5 SSLS (Tang, Yang), G6 IEMN DOAE /
  UPHF (K. and E. Dogheche). Every group-form initial agrees with the full-name author line (Eric Jun Hao, Shawn
  Yohanes, Chi Sin, Andrew Thye Shen). Probes C6 (Yang on G4) and C9 (Wee on G1): 4 errors each. Block 6 form: F1.
  See call 1. ok after F1.
- rouvie2008 (6; prose, slots from header): Alcatel-Thales III–V Laboratory, Marcoussis, FR. See call 9. ok.
- yanikgonul2022 (3; prose): Advanced Micro Foundry with unit Research and Development, Singapore, SG. ok.
- okimoto2023 (8; prose): Sumitomo Electric Industries, Ltd., Transmission Devices Laboratory, Yokohama (Okimoto,
  Yagi); Sumitomo Electric Device Innovations, Inc., Yokohama (6 authors). Probe O1 (Yagi on P2): 4 errors. ok.
- yuan2021 (7; prose): HPE with Hewlett Packard Labs as unit, Milpitas, US. See call 6. ok.
- cao2023 (6; per_author, ACP/POEM 2023): six identical blocks (College of Optical Science and Engineering, Zhejiang
  University, Hangzhou, CN). See call 2. ok.
- cezar2024 (6; per_author, slots from header, ICTON 2024): blocks under each author verified (probe Z1 with author 2's
  unit swapped to author 6's: 10 errors). See call 9. ok.
- kim2017 (4; single, p.2 header): page 1 is the open-access cover with the names only; UNIST School of Electrical and
  Computer Engineering, Ulsan, KR on p.2 (probe K1 without the p.2 locator: 2 errors). ok.

## Extractor calls (verified)

1. cao2021 block 5 and block 6.
   - Block 5: Singapore Synchrotron Light Source (SSLS) as a unit of National University of Singapore is right. SSLS is
     a facility of NUS, not a joint unit of several organizations; the block prints it on the line above NUS exactly
     like the department lines of blocks 1-4. Probe C4 (SSLS as org + NUS more_orgs): 0 errors, so the checker is
     neutral and the form decides. Keep.
   - Block 6: imprecise. The Institute of Electronics, Microelectronics, and Nanotechnology (IEMN) is a French joint
     research unit (UMR) of which Université Polytechnique Hauts-de-France is one partner; DOAE is its Valenciennes
     department. D285 records a UMR as `unit` only when printed as a sub-unit; the committed lit practice for a UMR
     line printed above or before the university is the UMR as org with the university in `more_orgs`: D466 (lit_h25
     caillaud2021, IMS Laboratory printed before University of Bordeaux, changed by audit fix F1 to org + more_orgs),
     IEF, C2N, INL, LTM, Institut FOTON; no committed lit block records a UMR as a unit under a university
     when the UMR is printed first. The org name stops before ", IEMN DOAE"; "IEMN DOAE" (acronym + department) is the
     unit, printed right after the name in the same segment. Probes C1 (this form), C2 (whole line as org), C3 (DOAE
     dropped) all 0 errors: checker neutral, D466 decides. Fix F1 (C1 form: rows 135 -> 137, IEMN and UPHF rows for
     each Dogheche slot).
   - Group-form names: the six groups print abbreviated names; the full-name line is printed above. Probe C7 (Yu Cao
     instead of Y. Cao): 2 errors (D368 position check needs the group form), so the group form is required, as in
     lit_h28 / h31 / h42. This is the first `grouped` paper with `slots_from_header`, so its slot names are initials
     (Y. Cao, ...): the full names of the p.2 author line go to the D412 author-list correction file (list 2), not the
     YAML. Authors listed in the full-name line order (the header order that defines the slots): right.
   - Probe C5 (C. S. Tang without G5): 0 errors. The D368 check misses a dropped carrier printed first in a group
     (gap list); G5 carried by Tang and Yang verified by eye.
2. cao2023: confirmed from the PDF word positions (grid of 3 columns x 2 rows; the author list follows the rows, both
   text layers read the columns). Authors in text-layer order are required (probe D1 list order: 8 errors); slots match
   by name; the warning is the expected D363 warning. All six blocks identical, so no row depends on the order. Keep.
3. nykolak1993: `country: ""` required (N1: 2 errors); "Member, ZEEE" not part of the name, accepted by the checker.
   `slots_from_header` required for all five papers that have it (C8, N2, G3, R3, Z2: 1 error each). Keep.
4. ghosh1996: the statement prints Lucent Technologies first, then Bell Laboratories; Bell Laboratories as unit follows
   the lit Nokia / Bell Labs and Alcatel-Lucent / Bell Laboratories practice (lit_h06, lit_h29, lit_h50). Probe G1
   (Bell Laboratories as org, Lucent in more_orgs): 4 errors (first printed field must be org or unit). Probe G2
   (Holmdel): 2 errors, so the interleaved continuation is really checked. Rows map to `org_lucent_technologies`; the
   registry also has the lineage org `org_lucent_bell_labs` (org round, list 3). nykolak1993 "AT&T Bell Laboratories"
   unmapped, as the identical lit_h50 string; registry has `org_bell_labs` and `org_at_and_t` (org round). Keep.
5. liu2022f: printed "Li Jin" (PDF spans confirm), list "Jin Li" at slot 5; matched automatically by swapped order;
   probe L1 (slot 0): 2 errors (D302). Same family / given parts, so the D426 review list decides which order is the
   person's name (list 1). Keep.
6. yuan2021: HPE org + Hewlett Packard Labs unit is the lit form (lit_h04, h16, h39; ofc_h13); probe Y1 (HP Labs org +
   HPE more_orgs): 0 errors, neutral, precedent decides. "Marco Fiorentino B" is a list artefact like "Daoxin Dai A"
   (D412, list 2); matched automatically. Keep.
7. gundlapalli2022: A*STAR not copied (contract parent rule; lit_h24 recorded the same two institutes the same way).
   Probe A1 (A*STAR in more_orgs): 0 errors, neutral, the rule decides. Keep.
8. Singapore: "Singapore" + postal code printed once per block, locality Singapore, country SG (corpus practice; probe
   A2 empty locality: 0 errors, neutral). chrysostomidis2021 "Department of X and Center for Interdisciplinary Research
   and Innovation" as one unit segment: required (probe H1 department only: 2 errors, contiguity) and identical to the
   committed lit_h46 strings. Keep.
9. rouvie2008: "Daniéle" with an acute accent is printed in both layers; kept as printed (the checker folds accents,
   probe R2 0 errors, so this is a rule call: D282 corrects extraction artefacts only, and both layers agree). "III–V"
   with an en dash as printed (probe R1 hyphen: 0 errors); the registry org `org_iii_v_lab` is the org-round target.
   cezar2024 "Fed. Univ. of Technology - Paraná" with the detached accent restored (D282) and the five unit variants
   (PPGEM / DAMEC twice, CPGEI, PPGFA / DAFIS, PPGQ / DAQBI, CPGEI / DAELN) verified per author. Keep.

## Fixes (exact YAML edits)

F1 (required, form; cao2021 slots 10 and 15). In `lit:cao2021` replace

```yaml
    - {marker: "G6", basis: grouped, org: "Université Polytechnique Hauts-de-France", unit: "Institute of Electronics, Microelectronics, and Nanotechnology, IEMN DOAE", locality: "Valenciennes", country: "FR", locator: "p.2 header"}
```

with

```yaml
    - {marker: "G6", basis: grouped, org: "Institute of Electronics, Microelectronics, and Nanotechnology", unit: "IEMN DOAE", more_orgs: ["Université Polytechnique Hauts-de-France"], locality: "Valenciennes", country: "FR", locator: "p.2 header"}
```

and in its note replace

```yaml
block 6 prints the IEMN institute line before Université Polytechnique Hauts-de-France (recorded as unit);
```

with

```yaml
block 6 prints the IEMN institute line (joint research unit, department DOAE) before Université Polytechnique Hauts-de-France (institute as org, university in more_orgs, D285 / D466);
```

Probe C1: 0 errors, rows 137.

N1 (optional, note wording; liu2022f). The author line prints no mark after Junbo Feng in either layer; the contact
footnote that names him starts with a pictogram glyph that extracts as an asterisk. In `lit:liu2022f` replace

```yaml
the asterisk on author 2 points to a contact line;
```

with

```yaml
a contact footnote names author 2 (no mark after the name in the author line);
```

Not probed (note text only).

## Lists (no YAML change)

1. D426 review list: liu2022f #5 (printed Li Jin, list Jin Li, swapped order).
2. D412 author-list corrections: yuan2021 #6 "Marco Fiorentino B"; cao2021 slot names from the group form (initials):
   full names printed in the p.2 author line (17 names), first `grouped` + `slots_from_header` paper.
3. Org round: Alcatel-Thales III–V Laboratory -> `org_iii_v_lab` (historical name); AT&T Bell Laboratories ->
   `org_bell_labs` lineage (as lit_h50); ghosh1996 Lucent Technologies + Bell Laboratories unit vs the lineage org
   `org_lucent_bell_labs`; IMRE -> `org_a_star_institute_of_materials_research_and_engineering`; IHPC new or alias.
4. Checker gaps: a carrier printed first in a group may drop the block (C5); locality emptiness not checked for grouped
   blocks (C10, 0 errors); `show` contact masking leaves a domain fragment (gundlapalli2022) and ORCID links
   (cezar2024) in the terminal output (nothing reached the batch files; not copied here).

## Unmapped org names (org round, no YAML change)

| printed org (unit) | place | proposal |
|---|---|---|
| AT&T Bell Laboratories | Murray Hill (no country printed) | alias to the Bell Labs lineage org (list 3) |
| Alcatel-Thales III–V Laboratory | Marcoussis, FR | alias to `org_iii_v_lab` |
| Fed. Univ. of Technology - Paraná (5 units) | Curitiba, BR | new org |
| Institute of High Performance Computing | Singapore, SG | new org or alias |
| Institute of Materials Research and Engineering | Singapore, SG | alias to the A*STAR IMRE org |
| Ulsan National Institute of Science and Technology | Ulsan, KR | new org or alias (also lit_h03) |
| Université Polytechnique Hauts-de-France | Valenciennes, FR | new org (after F1 in more_orgs) |
| Institute of Electronics, Microelectronics, and Nanotechnology (after F1) | Valenciennes, FR | new org (UMR) |

(11 strings in `unmapped_orgs.csv` now because the Paraná university appears with five units; 12 after F1.)

## Privacy and as-printed scan

- Grep over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv` and `papers.csv` (paper ids and
  decision ids stripped) for contact / URL patterns, street / road / avenue / drive / box / building / suite / floor /
  room / hall / wing / telephone words, digit runs of 4+, and the street, building, state and prefecture strings printed
  in the sources: hits only for notes saying that street addresses, building names or postal codes exist without
  giving them. No contact, street, building, postal code or P.O. box anywhere in the batch, notes included.
- As printed (kept, correct): Alcatel-Thales III–V Laboratory (en dash); Daniéle; Fed. Univ. of Technology - Paraná;
  National University of Singapore (NUS); École Polytechnique Fédérale de Lausanne (EPFL).

## Commands (2026-11-18)

| Command | Result |
|---|---|
| `show lit_h55 --corpus lit --codes <id> --pdf`, all 17 (+ `--pages 2` for cao2021, kim2017) | headers and author lists read (scratchpad only) |
| `check lit_h55 --corpus lit --dry-run` 20:16:11 (pid 2459) | 0 errors, 1 warning (cao2023 order); slots 129, recorded 129; rows 135 (grade A 135); papers ok 17; slots_from_header 5; multi-affiliation slots 6; 11 unmapped org strings |
| `h55_audit/probes/probe.py ALL` on scratch copies | below; repo batch files md5 unchanged |

| probe | change | result | reading |
|---|---|---|---|
| BASE | unchanged copy | 0 errors, 1 warning | baseline |
| C1 / C2 / C3 | cao2021 G6 IEMN org + unit IEMN DOAE + UPHF more_orgs / whole line as org / DOAE dropped | 0 / 0 / 0 (C1 rows 137) | neutral; D466 decides (F1 = C1) |
| C4 | SSLS as org + NUS more_orgs | 0 | neutral; unit kept |
| C5 / C6 / C9 | Tang without G5 / Yang on G4 / Wee on G1 | 0 / 4 / 4 errors | C5 = checker gap; groups bound |
| C7 | Yu Cao instead of Y. Cao | 2 errors | group form required |
| C10 | G6 locality empty | 0 | not checked (gap list) |
| C8 / N2 / G3 / R3 / Z2 | `slots_from_header` removed (cao2021, nykolak1993, ghosh1996, rouvie2008, cezar2024) | 1 error each | required |
| D1 | cao2023 authors in list order | 8 errors | text-layer order required |
| N1 | nykolak1993 country US | 2 errors | "" required |
| G1 / G2 | ghosh1996 Bell Laboratories org / Holmdel | 4 / 2 errors | as recorded |
| L1 / L2 | liu2022f Li Jin slot 0 / Feng dropped asterisk | 2 errors / 0 | automatic match required; neutral |
| Y1 | yuan2021 HP Labs org + HPE more_orgs | 0 | neutral; precedent kept |
| A1 / A2 / A3 | A*STAR in more_orgs / IMRE locality empty / Png on P1 | 0 / 0 / 4 errors | rule decides; carriers bound |
| H1 / H2 | chrysostomidis2021 department only / Mu on P2 | 2 / 4 errors | unit chain required; carriers bound |
| R1 / R2 | rouvie2008 hyphen / Danièle | 0 / 0 | folded; as printed kept |
| Z1 | cezar2024 author 2 unit = author 6 unit | 10 errors | per_author position bound |
| S1 / O1 / K1 | shimizu Kazama without P3 / Yagi on P2 / kim2017 without p.2 locator | 2 / 4 / 2 errors | bound |

## Verdict

GO after F1. All 129 slots carry the right person and markers; every prose statement and clause, every group and every
per-author block is recorded and verified; the five `slots_from_header` papers have no author list. F1 records the
cao2021 IEMN block in the committed UMR form (institute as org, Université Polytechnique Hauts-de-France in
`more_orgs`, D466), 2 slots. N1 is optional note wording. Nothing is invented and no contact, street, building or
postal text is recorded.
