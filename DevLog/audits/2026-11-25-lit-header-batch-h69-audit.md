---
title: Fresh-context audit of the lit author-affiliation batch lit_h69 (22 papers)
date: 2026-11-25
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; checker run only in dry-run or write-run on scratch copies with logs in the scratchpad; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h69/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D352, D366, D368, D380, D410, D426, D699, D756 and earlier lit rulings; D285, D287, D288, D301 from DevLog-008; format from the lit_h68 audit
verdict: GO; 121 slots audited, 121 recorded, 0 wrong rows, 0 imprecise rows; all 9 named extractor calls confirmed; no required fix; N1 optional note wording (zheng2018, no row change)
---

# Lit header batch audit: lit_h69 (2026-11-25)

## Scope

Batch lit_h69: 22 papers (Optics Express / Optica printed markers and single blocks, one OFC single block, one
conference paper with "1:" markers, one Electronics Letters end-of-letter affiliation section); 121 slots, 4 papers
`slots_from_header` (foster2007, takenobu2008, lee2014a, shinobu2010); 137 rows. Restricted corpus: this record names
only authors, orgs, units, cities and countries; no paper text is quoted and no contact, street, building, site, box
or postal text is copied (such spans are named by type only).

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h69 --corpus lit --codes <id> --pdf`
  (all 22; shinobu2010 also with `--pages 1 2`); output kept in the session scratchpad `h69_audit/show/` only.
- Per slot: printed name vs the `show` author list (or the header order for the 4 header-slot papers) and
  `compare.csv`; marker run in both layers; block fields (org, unit chain, more_orgs, campus, skip_between, city,
  country); role; locator; notes.
- All 137 rows of `header_rows.csv` read by paper: roles primary 123, additional 11, present address 3; basis printed
  108, single 23, grouped 6; all grade A; locators p.1 header 131, p.2 affiliations 6. `compare.csv`: 121 `recorded`,
  0 `no_header`; `order_differs` false on all 121.
- Address / contact scan of `headers.yaml` and every derived file (contact sign, URL, 3+-digit numbers, street, road,
  rue, avenue, boulevard, drive, suite, building, room, box, cedex, campus, e-mail / mail, phone, fax, postal, s/n,
  UMR and the joint-unit number, and every street, district, town and site token printed in this batch's blocks).
  Hits: "DevLog-011" in the file comment, type words in notes ("street address", "postal code(s)", "postal box",
  "campus site name", "joint-unit number"), the D410 placeholder value `<postal box>` and the `campus` field key /
  D301 values. No contact, URL, postal code, street, building, box, district or site text anywhere, notes included.
- Probes on scratch copies (`h69_audit/probes/probe.py` + `mk.py`, scratch `LIT_BASE`, batch name `lit_p69`,
  `cmd_check(..., dry_run=True)`, `RunLog` redirected to the scratchpad: no log written under `logs/`; 41 runs incl. the base dry and write runs). Dry
  run of the batch as written: 0 errors, 2 warnings (explicit slots clemmen2009 #4, zheng2018 #10); scratch write-run
  derived files byte-identical to the stamped `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`,
  `check_stamp.txt`. md5 of every repo batch file identical before and after the audit; `check_stamp.txt` matches
  `headers.yaml` (sha256 8111d0fd...).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h69 | 22 / 22 | 121 | 121 | 0 | 0 |

- Papers ok 22, partial 0, unreadable 0; `slots_from_header` 4 (exactly the papers.csv rows with `n_authors_meta` 0,
  each prints the D352 line in `show`); `author_list_differs` 0; explicit slots 2 (clemmen2009 #4, zheng2018 #10, both
  required); order warnings 0; present addresses 3 (zafar2018 #5, #6; herrerobermello2020 #1); dropped markers 2
  (zhang2021c #4 marker 5, #5 marker 6, contact footnotes); unreadable authors 0; 24 unmapped org strings.
- Per paper (slots / rows): clemmen2009 6 / 8; foster2007 5 / 5; linnenbank2016 3 / 3; turnerfoster2010 5 / 5;
  zheng2018 12 / 14; colbourne2018 5 / 5; takenobu2008 12 / 12; debevc2022 3 / 3; ma2020 6 / 6; lee2014a 5 / 7;
  an2019 2 / 2; shinobu2010 3 / 6; wu2021 4 / 4; wu2022a 5 / 5; zafar2018 6 / 8; zhang2021d 7 / 8; zhang2016a 10 / 10;
  zhang2021c 5 / 5; kudalippalliyalil2020 3 / 4; lin2022b 3 / 5; zhan2021 4 / 4; herrerobermello2020 7 / 8.
- Privacy findings: 0. Notes: 22 correct; 1 optional wording edit (N1).

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (121) | 121 | 0 | 0 |
| markers (printed / single / grouped, 121) | 121 | 0 | 0 |
| header position / order | 121 | 0 | 0 |
| blocks (org / unit / more_orgs / campus / skip_between / locality / country) (137 rows) | 137 | 0 | 0 |
| roles (primary / additional / present address) | 137 | 0 | 0 |
| locators | all | 0 | 0 |
| notes (22) | 22 | 0 (N1 optional) | 0 |

## Per-paper findings

- clemmen2009 (6; printed): calls 3. Name matches by name: S. Clemmen / Stéphane, K. Phan Huy / Kien, W. Bogaerts /
  Wim, S. Massar / Serge; Ph. Emplit equal. ok.
- foster2007 (5; printed, slots from header): Cornell University, School of Applied and Engineering Physics (1) /
  School of Electrical and Computer Engineering (2), Ithaca; both blocks print the state and postal code, no country.
  Header order Foster, Turner, Salem, Lipson, Gaeta = YAML. Probes F1 (country US) 2 errors, F2 (authors 2 / 3
  swapped) 4 errors. Call 8. ok.
- linnenbank2016 (3; single): University of Stuttgart, unit 4th Physics Institute and Research Center SCOPE (printed
  before the org), Stuttgart, DE. Steinle / Giessen list forms with middle initials match by name. ok.
- turnerfoster2010 (5; printed): Cornell blocks in the reverse order of foster2007 (1 ECE, 2 AEP), Ithaca, "U.S.A."
  -> US. Lipson printed without the list's middle initial F, matched by name. ok.
- zheng2018 (12; printed, 9 blocks): call 5. Markers 1 / 2 / 1,3 / 1 / 4 / 5 / 5 / 4 / 6 / 7 / 8 / 1,9 match both
  layers. Block 3 Ningbo University with the Zhejiang provincial key laboratory as unit, Ningbo (province in the
  block, not recorded), CN; block 5 "US Naval Research Lab" as printed, Washington, US; block 7 Intel Corporation,
  Silicon Photonic Products Division, Santa Clara, US. ok (N1 optional).
- colbourne2018 (5; single, OFC): Lumentum, Ottawa, CA (street, province, postal code not recorded). "Sheldon
  McLaughlin" vs list "Mclaughlin" (case) matched by name. ok.
- takenobu2008 (12; printed, slots from header): call 9. Header order (12 names, three lines) = YAML order; probes
  T1 (Kuwana on 1) 3 errors, T2 (Ono / Sato swapped) 4 errors. Fraunhofer Institute for Telecommunications,
  Heinrich-Hertz-Institut as one org (committed majority form, maps to org_fraunhofer_heinrich_hertz_institute);
  probe T4 (split into two orgs) 0 errors, +5 rows, +2 unmapped: committed form kept. ok.
- debevc2022 (3; single): University of Ljubljana (printed before the faculty), Faculty of Electrical Engineering,
  Ljubljana, SI. Capital names with detached carons written with the intended letters (D282). ok.
- ma2020 (6; single): The University of British Columbia (leading article as printed, maps by alias), ECE department,
  Vancouver, CA. ok.
- lee2014a (5; printed, slots from header): call 2. Header order Lee, Giese, Ajayi, Magnusson, Johnson = YAML.
  Block 2 Stanford University, EE department, Stanford (city printed), US; block 3 Sikorsky Aircraft, Stratford, US
  (street not recorded). ok.
- an2019 (2; single): Electronics and Telecommunications Research Institute (ETRI) with the laboratory as unit,
  Daejeon (a district glued before the city, not recorded), KR. ok.
- shinobu2010 (3; grouped, slots from header): call 1. ok.
- wu2021 (4; single): Hebei University, two centres + college as unit chain (printed before the org), Baoding, CN. ok.
- wu2022a (5; printed): block 1 the wu2021 block; block 2 Southeast University, national research center + school
  chain, Nanjing, CN. Markers 1 / 2 / 1 / 2 / 1. ok.
- zafar2018 (6; printed): call 6. ok.
- zhang2021d (7; printed): McGill University, Photonics Systems Group + ECE department, Montreal; CMC
  Microsystems, Kingston; Ericsson Canada, Montreal; all CA (provinces not recorded). "STEPHANE LESSARD" vs list
  "Stéphane" matched by name; "YANNICK D’MELLO" as printed. ok.
- zhang2016a (10; printed): SJTU state key lab + department chain, Shanghai; Zhejiang University, department,
  Hangzhou; École de technologie supérieure, Laboratoire de Technologies de Réseaux (printed before the org),
  Montreal, CA. Tremblay list middle initial L, matched by name. ok.
- zhang2021c (5; printed): call 4. ok.
- kudalippalliyalil2020 (3; printed): University of Maryland + campus College Park (D301), unit Institute for
  Research in Electronics & Applied Physics, locality College Park; Laboratory for Physical Sciences, College Park;
  both US. Markers 1,2 / 1 / 2. ok.
- lin2022b (3; printed): block 1 Zhejiang University with centre + college + state key laboratory chain, Hangzhou;
  block 2 Eindhoven University of Technology, Institute for Photonic Integration (IPI), Eindhoven, NL (postal box and
  postal code after the org not recorded; "The Netherlands"); block 3 "Shanghai Institute for Advanced Study of
  Zhejiang University" as one printed name, Shanghai, CN. Probe N1 (org Zhejiang University + institute as unit):
  0 errors, -1 unmapped; the printed one-name form is kept (D565 "Northeastern University at Qinhuangdao" / D659
  "Yiwu Research Institute of Fudan University" precedent; org round). ok.
- zhan2021 (4; printed): University of Maryland + campus College Park, ECE (1) / Astronomy (2), College Park, US.
  "MARIO DAGENAIS" vs list "M. Dagenais" matched by name. ok.
- herrerobermello2020 (7; printed): call 7. Block 3 Universidad de Málaga with "Depto. De Ingeniería de
  Comunicaciones, ETSI de Telecomunicación" as unit (printed after the org), Málaga, ES (campus site name not
  recorded; committed lit form); block 4 National Research Council of Canada, Ottawa, CA. List forms with the
  Unicode hyphen and "Aitor Villafranca Velasco" (printed "AITOR V. VELASCO") matched by name. ok.

## Extractor calls (verified)

1. shinobu2010 grouped G1 + G2. Page 1 prints the three full names with no markers and no block; the page-2
   authors' affiliations section prints the three authors by initials, then one parenthesis with the department,
   Yokohama National University, a street / district / prefecture / postal span, Japan, and a second sentence
   stating that they also belong to CREST, Japan Science and Technology Agency, Japan (no city). One author group
   carrying two printed orgs = two grouped blocks (D368; lit_h18 simpanen2017 Electronics Letters precedent with
   `p.2 affiliations`). G1 rows primary, G2 rows additional (header_rows.csv). CREST (a JST programme printed before
   the agency) as `unit` of org JST follows the unit-then-org reading; probe H1 (CREST as org, JST in more_orgs)
   0 errors, +3 rows, +1 unmapped: not better. G2 locality "" is correct (probe H5 Yokohama: 2 errors). Names from
   the page-1 author line (full names) are the better record for header slots; probe H3 (initials) 0 errors,
   neutral. Probe H2 (Baba without G2) 4 errors. Header order Shinobu, Arita, Baba on both pages = YAML. Confirmed.
   Checker gaps: H4 (G2 removed from the block list and from all authors) 0 errors; H6 (authors 1 / 2 swapped)
   0 errors (O1).
2. lee2014a "University of Texas at Arlington" -> org University of Texas + campus Arlington. This is the D756 form
   (lit_h67 sun2015a "University of California at Berkeley", orcutt2011 "University of Colorado at Boulder" -> org +
   campus) and the D301 multi-campus rule; lit_h08 and lit_h28 record UT Austin the same way. The five committed
   "(The) University of Texas at Austin" whole strings predate D756 and map to the registry name
   `org_the_university_of_texas_at_austin`; there is no Arlington id, so the rows are unmapped either way (probes L1
   whole string / L3 campus removed: 0 errors, unmapped count unchanged; matcher lookup of the whole string:
   unmapped). Campus form confirmed; the org round needs a UT Arlington id with the "University of Texas, Arlington"
   form as alias (O2 lists the system-wide mix). The postal box after the university is not recorded and not in
   `skip_between` (it is printed after the org, outside the unit-org gap): correct. Block 4 Clemson University with
   "Department of Electrical & Computer Engineering" (ampersand as printed), the state and postal code only: locality
   "" correct (probe L2 locality "South Carolina": 0 errors, known gap: state accepted as locality). Confirmed.
3. clemmen2009. Block 1 Laboratoire d’Information Quantique, postal box, Université Libre de Bruxelles (U.L.B.),
   street, Bruxelles, Belgium; block 4 Service OPERA-Photonique, postal box, ULB (U.L.B.), street, Brussels, Belgium:
   `skip_between: "<postal box>"` on both (D410; probe C5 without it: 2 errors, unit and org not contiguous); the
   parenthesized "(U.L.B.)" kept as printed (contract; maps by `name:no_parenthetical`; probe C6 without it: 0 errors,
   neutral); localities Bruxelles / Brussels each as printed. Block 2 Département d’Optique P.M. Duffieux, Institut
   FEMTO-ST, CNRS with its UMR number, Université de Franche-Comté, Besançon, France: FEMTO-ST as org (the joint
   research unit printed as an organization), CNRS and the university in `more_orgs` (D285; D466 / D727 guerber2017
   pattern), the UMR number not copied; probe C3 (more_orgs dropped) 0 errors, -2 rows (known gap: a missing more_org
   is not detected). Block 3 "Ghent University - IMEC" joined as printed (D426 dash-joined form; maps to
   org_ghent_university + org_imec), unit "Department of Information Technology (INTEC)", Gent; probe C4 (split) 0
   errors, +2 rows: committed form kept. Explicit slot 4 for printed "R. G. Baets" vs list "Roel Baets": required
   (probe C1 without it: 2 errors, 0 slots match); first initial agrees, the list lacks the middle initial,
   distinctive family name (D287 / D369); probe C2 (list form as YAML name) 4 errors. Confirmed.
4. zhang2021c. Block 4 prints the institute, then "AMS Beijing", then the city Beijing and postal code: org "AMS
   Beijing" as printed (probe K4 expanded name: 4 errors). "Mirco" printed in both layers (D699 misprints as printed;
   probe K3 corrected: 2 errors). Block 1 Jiang Su University prints only the province and postal code: locality ""
   correct (probe K2 "Jiangsu": 0 errors, known gap). Markers 5 and 6 (Guo, Yang) have no block; two contact lines
   follow block 4 (masked in `show`): `dropped_markers` "contact footnote" (probe K1 without: 2 errors). Block 2 DTU
   Fotonik as unit of Technical University of Denmark, Lyngby (prefixed postal code not recorded). Confirmed.
5. zheng2018. Block 6 "Air Force Research Laboratory, Sensors Directorate, Wright-Patterson Air Force Base, OH ...":
   org AFRL, unit Sensors Directorate (printed after the org; committed lit form, e.g. AFRL Information Directorate
   at Rome), locality "Wright-Patterson Air Force Base" as printed (probe Z6 "Wright-Patterson AFB": 2 errors; probe
   Z5 unit dropped: 0 errors, neutral). Block 4 "Department of Electrical Engineering, Stanford University, CA ...":
   no city printed, locality "" correct (probe Z2 "Stanford": 0 errors, known gap: a city found only inside the org
   name is accepted). Block 8 University of California + campus San Diego, locality La Jolla (D301; all 11 committed
   UCSD campus blocks use La Jolla; probe Z3 campus removed: 0 errors, +1 unmapped, known gap; probe Z4 locality San
   Diego: 0 errors, known gap). Explicit slot 10 for printed "JONATHAN DOYLEND" vs list "J. K. Doylend": required
   (probe Z1 without: 2 errors); first initial agrees, the printed form lacks the middle initial K, distinctive family
   name (D287 / D369). Confirmed (N1 optional note wording).
6. zafar2018. Block 1 prints the department, Masdar Institute, Khalifa University of Science and Technology, Abu
   Dhabi, UAE: org Khalifa University with "Electrical and Computer Engineering Department, Masdar Institute" as
   the unit chain (one contiguous segment; Masdar Institute was merged into Khalifa University); probe A4 (Masdar
   dropped from the unit) 2 errors; probe A2 (Masdar as org, Khalifa in more_orgs) 0 errors, +6 rows, +1 unmapped:
   not better. "UAE" accepted as the printed AE. Blocks 2 / 3 "Currently with the ..." present addresses keeping the
   article: the checker requires it (probe A1, articles removed: 6 errors, first field not after the marker), and
   the committed printed-marker present addresses keep it (lit_h67 orcutt2011, lit_h49 patel2014, lit_h09 rao2019;
   prose statements drop the article after "with", a different construction). Block 2 imec, Leuven, BE (street and
   postal code not recorded); block 3 Boston University, "the Department of Electrical and Computer Engineering",
   Boston, US. Probe A3 (block 2 role affiliation) 2 errors. Confirmed.
7. herrerobermello2020. Block 5 "Currently with Alcyon Photonics S.L. Madrid, Spain" (no comma after S.L.): role
   present_address, org Alcyon Photonics S.L., Madrid, ES (probe E2 role affiliation: 2 errors; E3 marker 5 removed
   from author 1: 3 errors). Block 1 Instituto de Óptica, Consejo Superior de Investigaciones Científicas, Madrid:
   the acronym "(CSIC)" is not printed in this paper, so the org is the full name only (probe E1 with "(CSIC)": 4
   errors); same org / unit form as the committed lit CSIC blocks; maps. Confirmed.
8. foster2007 country "" on both blocks: only "Ithaca, NY" and a postal code printed, no country (D249 / D288;
   probe F1: 2 errors). Confirmed.
9. takenobu2008 markers "1:" to "4:" (colon after the digit; "3:" glued to the org): recorded "1"-"4"; the second
   "1:" and "4:" lines are contact lines after blocks 1 and 4 (masked or partly masked in `show`; nothing from them
   recorded; the note names them by type). Block 1 locality Yokohama (street-address town before it and the
   prefecture after it not recorded), block 2 Tokyo (ward before it not recorded), block 3 "Ichihara-shi" as printed
   (D366; probe T3 "Ichihara" 0 errors, known prefix gap), block 4 Berlin; "JAPAN" / "GERMANY" -> JP / DE. Confirmed.

## Fixes (exact YAML edits)

No required fix: no slot, marker, block, field, role, locator or note is wrong.

N1 (optional, wording only; no row change; zheng2018, line 59). In the `note`, replace

```
author 10 printed Jonathan Doylend, author list J. K. Doylend (distinctive family name, explicit slot, D287 / D369)
```

with

```
author 10 printed Jonathan Doylend, author list J. K. Doylend (first initial agrees, the printed form lacks the middle initial; distinctive family name, explicit slot, D287 / D369)
```

(parallels the clemmen2009 note). If applied, re-run `uv run python scripts/ofc_headers.py check lit_h69 --corpus lit`
(the stamp hash changes; derived files unchanged).

## Observations (no YAML change)

- O1 Checker gaps for `grouped` papers: removing a group's second block from the block list and from every author
  (H4) passes with 0 errors, and the YAML author order of a grouped / slots_from_header paper is not compared with
  the printed author line (H6; same family as h68 O1 / D756). shinobu2010 was checked by reading.
- O2 University of Texas forms across committed lit batches: 5 whole "(The) University of Texas at Austin" strings
  (lit_h18, h24, h46, h57, h58; map to `org_the_university_of_texas_at_austin`) vs campus form for Austin (lit_h08,
  lit_h28) and now Arlington (lit_h69). D756 makes the campus form the rule; the older whole strings map and need no
  change for the rows, but the org round should add a UT Arlington id with the campus-form alias.
- O3 Known gaps reconfirmed: missing `more_orgs` (C3), missing `campus` (Z3), state / province or a city inside the
  org name accepted as locality (L2, K2, Z2), campus place accepted as locality (Z4), locality prefix accepted (T3).
- O4 The imec present-address string "the Interuniversity Microelectronics Center (imec)" is unmapped although the
  registry has the alias "Interuniversity Microelectronics Center" (direct matcher lookups of the string with and
  without the article or the parenthesis: unmapped). Org round alias; the YAML form is fixed by the checker (call 6).

## Lists for the coordinator

- D412 list: none.
- D426 review list: clemmen2009 #4 (R. G. Baets / Roel Baets) and zheng2018 #10 (JONATHAN DOYLEND / J. K. Doylend),
  explicit slots (D287 / D369 middle-initial cases).
- Re-record list: none.
- Org round (24 unmapped strings): AMS Beijing; Air Force Research Laboratory (unit Sensors Directorate); Alcyon
  Photonics S.L.; Asahi Glass Co., Ltd. (7 rows); Boston University; Centre National de la Recherche Scientifique;
  Clemson University; Ericsson Canada; Hebei University (7 rows); Institut FEMTO-ST; Japan Science and Technology
  Agency (unit CREST); Jiang Su University; Khalifa University of Science and Technology (6 rows); Laboratory for
  Physical Sciences; National University of Defense Technology; Ningbo University; Shanghai Institute for Advanced
  Study of Zhejiang University; Sikorsky Aircraft; US Naval Research Lab; Universidad de Málaga; University of
  Ljubljana; University of Texas, Arlington (4 rows); Université de Franche-Comté; the Interuniversity
  Microelectronics Center (imec) (O4).

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 2 warnings, 137 rows, 24 unmapped; derived files identical | batch as written |
| C1 / C2 | clemmen2009 slot removed / YAML name Roel Baets | 2 / 4 errors | slot required / printed form verified |
| C3 / C4 | FEMTO-ST more_orgs dropped / Ghent - IMEC split | 0 (-2 rows) / 0 (+2 rows) errors | known gap / D426 joined form kept |
| C5 / C6 | ULB block 1 skip_between removed / "(U.L.B.)" removed | 2 / 0 errors | D410 skip verified / neutral, as printed kept |
| Z1 | zheng2018 slot removed | 2 errors | slot required |
| Z2 / Z3 / Z4 | Stanford locality / UCSD campus removed / locality San Diego | 0 / 0 (+1 unmapped) / 0 errors | known gaps; extractor form correct |
| Z5 / Z6 | AFRL unit dropped / locality Wright-Patterson AFB | 0 / 2 errors | neutral / as printed verified |
| L1 / L3 / L2 | UTA whole string / campus removed / Clemson locality South Carolina | 0 / 0 / 0 errors | D756 ruling decides / neutral / known gap |
| H1 / H2 / H3 | CREST as org / Baba without G2 / initials as names | 0 (+3 rows, +1 unmapped) / 4 / 0 errors | unit form kept / grouping verified / neutral |
| H4 / H5 / H6 | G2 removed everywhere / G2 locality Yokohama / authors 1-2 swapped | 0 / 2 / 0 errors | O1 / verified / O1 |
| K1 / K2 / K3 / K4 | Guo dropped marker removed / locality Jiangsu / "Micro" / AMS expanded | 2 / 0 / 2 / 4 errors | verified / known gap / misprint verified / as printed verified |
| A1 / A2 / A3 / A4 | articles removed / Masdar as org / imec role affiliation / Masdar out of unit | 6 / 0 (+6 rows) / 2 / 2 errors | article required / chain kept / verified / verified |
| E1 / E2 / E3 | "(CSIC)" added / block 5 role affiliation / marker 5 removed | 4 / 2 / 3 errors | verified |
| F1 / F2 | foster2007 country US / authors 2-3 swapped | 2 / 4 errors | verified |
| T1 / T2 / T3 / T4 | Kuwana on 1 / Ono-Sato swapped / Ichihara / HHI split | 3 / 4 / 0 / 0 (+5 rows) errors | verified / verified / known gap / committed form kept |
| N1 | lin2022b institute as ZJU unit | 0 errors, -1 unmapped | printed one-name form kept (org round) |
