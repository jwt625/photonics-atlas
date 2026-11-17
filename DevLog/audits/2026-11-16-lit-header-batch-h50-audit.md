---
title: Fresh-context audit of the lit author-affiliation batch lit_h50 (25 papers)
date: 2026-11-16
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only with --dry-run, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h50/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D412, D426, D461, D466, D521, D546, D550, D572, D599); format from the lit_h47 / lit_h48 audits
verdict: GO with 1 fix; 178 slots (150 list + 28 slots_from_header) plus 2 header-only authors audited; 175 recorded slots ok, 3 slots without rows (1 of them wrongly, F1), 0 wrong rows; F1 bundalo2022 #7 Lee Carrol present address is printed in full (space-less line masked only in the show view), record it and drop `unreadable`
---

# Lit header batch audit: lit_h50 (2026-11-16)

## Scope

Batch lit_h50: 25 papers (IEEE journal / letter footnote papers, OSA / Optica header papers, three conference papers, one
1994 scanned paper); 178 slots (burla2015, guillentorres2014, adar1994, cherchi2014 and wang2014a with
`slots_from_header`, 28 slots) plus 2 header-only authors (bundalo2022 Martin Zoldak and Peter O'Brien, slot 0); 199 rows.
Restricted corpus: this record names only authors, orgs, units, cities and countries; no paper text is quoted and no
contact, street, building, postal-box or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h50 --corpus lit --codes <id> --pdf`
  (all 25; bundalo2022 also with `--pages 9`; output kept in the session scratchpad `h50_audit/show/` only).
- Per slot: printed name vs the `show` author list and `compare.csv`; marker run vs text layer and PDF layer (identical
  in both layers for every printed-marker paper); prose statement subjects and verbs; block fields (org, unit chain,
  campus, city, country); role; locator; grade. Every distinct (paper, marker, role, org, unit, city, country, basis,
  locator, org id, match basis) tuple of `header_rows.csv` read (67 tuples, 199 rows).
- bundalo2022 author 7 present-address line: `show` masks the whole continuation line. The source text layer
  (`references/bundalo2022/text.md`) and the PDF layer (pymupdf, page 9) were read with at-sign tokens and digits
  masked in my own output: both print the line in full without word spaces (organization, an address span, city,
  country), the D521 marinins2022 situation.
- Probes on scratch copies (`h50_audit/probes/probe.py` in the session scratchpad, scratch `LIT_BASE`, batch name
  `lit_p50`, `cmd_check(..., dry_run=True)`). md5 of every repo batch file identical before and after the audit;
  `check_stamp.txt` matches `headers.yaml` (sha256 e9873fa9...). Probe checks wrote their usual logs under `logs/`
  (prefix `lit_headers_check_lit_p50`).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h50 | 25 / 25 | 178 + 2 header-only | 179 | 1 (bundalo2022 #7, F1) | 0 |

- Rows 199 (all grade A: prose 118, printed 50, single 31; primary 175, additional 17, present address 7); recorded
  175, no_header 3 (adar1994 #2 Serbin, bundalo2022 #7 Carrol, #29 Wuytens; all `unreadable`); papers ok 23, partial 2
  (adar1994, bundalo2022), unreadable 0; `slots_from_header` 5; `author_list_differs` 1 (bundalo2022); explicit slots
  2 (chauhan2022 #7, bundalo2022 #19) plus slot 0 twice (bundalo2022 Zoldak, O'Brien); multi-affiliation slots 7;
  18 unmapped org strings. After F1: recorded 176, no_header 2, rows 201, present address 8.
- Per paper (slots / rows): burla2015 4 / 4; guillentorres2014 5 / 5; chen2015 10 / 10; chauhan2022 8 / 8; liu2020d 6 / 6;
  adar1994 3 / 2; li2013b 6 / 6; cherchi2014 6 / 6; gondarenko2009 3 / 3; zhou2024a 5 / 20; bozzola2015 5 / 5;
  liu2022e 5 / 5; laere2007 8 / 8; chen2010 5 / 5; bundalo2022 30 (+2 slot 0) / 36; zhong2014 10 / 11; gui2021 6 / 6;
  larrea2018 5 / 5; doerr2010 4 / 4; sacher2014b 7 / 7; chang2023 8 / 8; li2013a 4 / 4; wan2019 6 / 6; wang2014a 10 / 12;
  nielson2005 9 / 9.

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (178 + 2) | 180 | 0 | 0 |
| markers (180 header authors) | 180 | 0 | 0 |
| header / statement position | 180 | 0 | 0 |
| blocks (org / unit / locality / country) (175 authors with rows) | 175 | 0 | 0 |
| unreadable calls (3) | 2 | 1 (bundalo2022 #7, F1) | 0 |
| present addresses (7 recorded + bundalo2022 P8, P11 without rows) | 8 | 1 (P11 truncated, F1) | 0 |
| locators (all blocks; bundalo2022 p.9) | all | 0 | 0 |
| notes (25) | 24 | 1 (bundalo2022, F1) | 0 |

## Per-paper findings

- burla2015 (4; printed, slots from header): INRS + unit "Énergie, Matériaux et Télécommunications (INRS-EMT)", Varennes,
  CA (dash between institute and centre; earlier batches record INRS with the same centre unit); UBC + ECE, Vancouver, CA.
  Burla 1 + hash mark = contact line (verified in both layers). Probe U1: the hash entry in `dropped_markers` is not
  required (symbol mark) but harmless. ok.
- guillentorres2014 (5; single, slots from header): UBC + ECE, Vancouver, CA; the unit is followed by a period in print.
  Detached accent written Guillén-Torres (D282). ok.
- chen2015 (10; single): UBC + ECE, Vancouver, CA. ok.
- chauhan2022 (8; printed, capitals): University of California + campus Santa Barbara + ECE, Santa Barbara, US (org id
  org_ucsb); Honeywell Aerospace, Plymouth, US. Blumenthal 1 + asterisk. See call 1. ok.
- liu2020d (6; prose, all authors): HUST + unit chain (national engineering laboratory, school), Wuhan, CN. ok.
- adar1994 (3; prose, slots from header, OCR): statement 1 (Adar, Mizrahi) AT&T Bell Laboratories, Murray Hill, country
  empty; statement 2 (Serbin) "ATkT Bell Laboratories", Breinigsville, country empty, Serbin unreadable. See call 2. ok.
- li2013b (6; single): Georgia Tech + ECE, Atlanta, US. A. / H. initials vs list full names automatic. ok.
- cherchi2014 (6; single, slots from header): VTT Technical Research Centre of Finland, Espoo, FI. ok.
- gondarenko2009 (3; printed, markers with period): Cornell University + School of Applied and Engineering Physics /
  ECE school, Ithaca; no country printed (probe G1 US: 2 errors). ok.
- zhou2024a (5; prose, statement + 3 clauses): BIT + Radar Technology Research Institute chain, Beijing; BIT + key
  laboratory (BIT printed in parentheses after it; ministry not copied), Beijing; BIT + Chongqing Innovation Center,
  Chongqing; Chongqing Key Laboratory of Novel Civilian Radar as its own org, Chongqing; all CN. Exactly the D461
  re-record form. Probe Z1 (no P4): 15 errors (clause coverage bound); Z2 (ministry as more_orgs): 0 errors (neutral;
  parent rule keeps it out). ok.
- bozzola2015 (5; printed): Pavia Physics Department / DECBE, Pavia, IT; Tyndall, Cork, IE (building name between org and
  city not recorded). Markers 4, 5, 6 contact lines. Probe O2 (Carroll without 6): 2 errors; O1 (Andreani without 5):
  0 errors = known last-author gap. ok.
- liu2022e (5; prose): HUST + WNLO unit, Wuhan, CN (majority form, D572). ok.
- laere2007 (8; prose): "Ghent University-Interuniversity Microelectronics Center (IMEC)" + INTEC, Ghent, BE (dash-joined,
  kept whole, D426); University of St. Andrews + School of Physics and Astronomy, St. Andrews, GB (Ayre, Krauss). ok.
- chen2010 (5; prose): The Chinese University of Hong Kong + Department of Electronic Engineering; district printed
  before Hong Kong (in the note), locality Hong Kong, HK. Probes H1 (district as locality) and H2 (CN) pass: the
  checker is neutral; D366 (district to the note) and D288 ("Hong Kong ..., China" -> HK) decide. ok.
- bundalo2022 (30 + 2; prose, p.9 "Authors' Affiliations"): 24 statement / pronoun blocks P1-P24 checked one by one
  against both layers: subjects, was with / are with (affiliation) vs He is now with (present address), orgs as
  printed (CSEM S.E., STMicroelectronics s.r.l., imec/Ghent University, imec / Ghent University, III-V labs, KIT,
  Argotech a.s., VTT, Eblana Photonics, Karlsruhe Institute of Technology (KIT) + IPQ, Metallux SA, VLAIO,
  Evoelectronics s.r.l), cities (Cork, Alpnach, Agrate Brianza, Ghent, Ecublens, Palaiseau, Karlsruhe, Náchod, Oulu,
  Dublin, Mendrisio, Brussel, Pomezia) and countries all correct; streets, buildings, campus names and postal codes
  not recorded. Slots: Zoldak and O'Brien not in the 30-name list (slot 0 + `author_list_differs`; probes B6 / B7 1
  error each); Tienforti Marcello slot 19 (name-order swap; probe B5 shows the checker matches it without the slot too,
  harmless); Junsu Su Lee, Sean / Seán Collins, Leos / Leoš Halmo, Christian / Christian G. Koos automatic. #29 Wuytens
  unreadable: see call 3. #7 Carrol: see F1.
- zhong2014 (10; printed): McGill ECE, Montreal; UBC ECE, Vancouver; block 3 Currently with Université Laval + ECE,
  Québec, `present_address` (probe Q1: 2 errors); University of Washington + Washington Nanofabrication Facility,
  Seattle, US. Wei Shi 1,3. ok.
- gui2021 (6; prose): Huawei Technologies + Transmission & Access Research Department, Shenzhen; HUST + WNLO / national
  engineering laboratory / school chain, Wuhan (last line space-less in print); CN. ok.
- larrea2018 (5; prose): "Universitat Politècnica València" as printed (probe L1 with "de": 4 errors) + Nanophotonics
  Technology Center, València, ES. ok.
- doerr2010 (4; prose): Alcatel-Lucent + unit Bell Laboratories, Holmdel (Doerr, L. Chen, Buhl) / Murray Hill
  (Y.-K. Chen), US. See call 4. ok.
- sacher2014b (7; printed): University of Toronto + ECE, Toronto, CA; Institute of Microelectronics (A*STAR parent not
  copied), Singapore, SG (23 committed blocks use the same form). ok.
- chang2023 (8; prose): Texas A&M University + Analog and Mixed-Signal Center, College Station; University of
  California + campus Davis + ECE, Davis; US. Co-first-author sentence is not a marker. ok.
- li2013a (4; single): Institute of Microelectronics, Singapore, SG. ok.
- wan2019 (6; prose): Georgia Tech + ECE, Atlanta, US. ok.
- wang2014a (10; printed, slots from header): SIMIT, CAS (one name, as committed blocks) + state key laboratory, Shanghai;
  Grace Semiconductor Manufacturing Corporation, Shanghai; CN; Purdue + "School of Electrical and Computer Engineering,
  and Birck Nano-technology Center", West Lafayette, US. Jing Wang 1,3; Shichang Zou 1,2 (probe W1: 2 errors). ok.
- nielson2005 (9; prose): Sandia National Laboratories, Albuquerque; MIT, Cambridge (6 authors); Pirelli Laboratories,
  Milan, IT; Haus statement "deceased, was with MIT" recorded as P4 (the affiliation of the work), deceased remark not a
  block. Probe N1 (Haus on P2): 5 errors. ok.

## Extractor calls (verified)

1. chauhan2022 "C. W. HOYT" -> slot 7 (list Chad Hoyt). Probe C1 (no slot): 2 errors; C2 (slot 0 + differs): 0 errors, so
   the checker is neutral. Distinctive family name, the only difference is the missing middle initial: the D369 /
   D287 explicit-slot case (garciablanco2025 precedent). Keep.
2. adar1994. Both statements are interleaved with the next column: the country line of statement 1 is printed after
   statement 2. Probe A3 (P1 country US): 2 errors, so empty is forced. Probe A4 (P2 country US): 0 errors, because the
   checker finds statement 1's country inside statement 2's span; the extractor's empty country is the correct reading
   (Serbin's own line ends in the OCR-garbled country). Probe A2 (P2 org AT&T): 4 errors, so the printed OCR form is the
   only one the checker accepts; probe A1 (Serbin readable, status partial kept): only the status error, i.e. the
   checker would let "ATkT Bell Laboratories" become a row. Serbin unreadable avoids publishing a garbled org; keep, and
   list for an OCR-fold re-record.
3. bundalo2022 #29 Wuytens unreadable. Probe B3 (readable): P8 "not named in the statement subject" in both layers, so
   the checker gap (period after "University" not a sentence end, pronoun subject unresolved) is real. Probe B4 (P8
   removed, Wuytens readable on P7 only): 0 errors, i.e. the checker would also accept dropping a printed present
   address; rejected (D361). P7 has no place printed (probe B8 Ghent / BE: country error). Keeping both blocks with no
   rows is the D546 "gap recorded, not worked around" practice. Keep; re-record list.
4. doerr2010 Bell Laboratories as unit of Alcatel-Lucent (org id org_alcatel_lucent). Probe D1 (Bell Laboratories as org,
   Alcatel-Lucent more_orgs): 0 errors (neutral). lit_h06 / lit_h29 record Nokia + unit Bell Labs for the comma form;
   lit_h13 keeps the slash form "Bell Laboratories/Alcatel-Lucent" whole as printed. Keep.
5. imec/Ghent dash / slash forms kept whole (laere2007, bundalo2022 P6 / P7 / P21): D426 and the ofc_h03 "Ghent
   University/imec" precedent; P6 / P21 map to both org_ghent_university and org_imec by alias. Keep.
6. zhou2024a D461 form, nielson2005 Haus, chen2010 Hong Kong: verified above.

## Fixes (exact YAML edits)

F1 (bundalo2022 author 7 Lee Carrol, present address printed in full). The "He is now with" line continues on the next
line without word spaces; `show` masks that line, but both source layers print the organization, an address span, the
city and the country (verified with masked output). D521 (lit_h26 marinins2022) records such a line from the checker's
view. Probe B1 / FIX_F1: 0 errors; probes B9 (Agency for Authority), B10 (Cork) and B11 (GB) each fail, so the checker
verifies org, city and country on that line. The current truncated org "Sustainable En" with empty place would be a
wrong row the moment `unreadable` is lifted (probe B2 passes with it: the checker only checks a prefix there).

In `lit:bundalo2022` replace

```yaml
    - {marker: "P11", basis: prose, role: present_address, org: "Sustainable En", locality: "", country: "", locator: "p.9 affiliations"}
```

with

```yaml
    - {marker: "P11", basis: prose, role: present_address, org: "Sustainable Energy Authority Ireland", locality: "Dublin", country: "IE", locator: "p.9 affiliations"}
```

replace

```yaml
    - {name: "Lee Carrol", markers: ["P10", "P11"], unreadable: true}
```

with

```yaml
    - {name: "Lee Carrol", markers: ["P10", "P11"]}
```

and in the note replace

```yaml
author 7 (Lee Carrol) present address is truncated by the masked contact run after its first words in the show view of both layers: block kept so the statement stays consistent, author 7 unreadable (no rows, also not for the Tyndall statement)
```

with

```yaml
author 7 (Lee Carrol) present address continues on the next line printed without word spaces (show masks that line; both source layers print it in full, lit_h26 marinins2022 precedent, D521): organization and city recorded, the address span between them not recorded
```

`status: partial` stays (Wuytens). Probe FIX_F1 (all three edits on a scratch copy): 0 errors, 1 warning (baseline
chauhan2022 slot warning); recorded 175 -> 176, no_header 3 -> 2, rows 199 -> 201 (Tyndall primary + present address),
present address 7 -> 8.

## Observations (no change recommended)

- O1 bundalo2022: whenever any bundalo2022 block fails in both layers (probes B3, B8-B13, and the unrelated B12 with a
  wrong P15 country), the checker also prints text-layer errors for P1 ("statement names all authors") and P2 (Bundalo
  not in the subject): the text layer reads the "Authors' Affiliations" heading into the first statement; the PDF layer
  passes, so the baseline is clean. A later editor of this paper should expect these two companion errors.
- O2 Notes calling the asterisk the corresponding-author mark where page 1 prints only a contact line (chen2015,
  li2013b, cherchi2014, sacher2014b, li2013a, zhong2014): same wording as earlier batches (h48 O1); no fix.
- O3 burla2015 `dropped_markers` entry for the hash mark is not required (probe U1) but correct in content.

## Open questions (with recommendation)

1. Re-record list (checker gaps): bundalo2022 #29 Wuytens (pronoun statement after "University.", values: P7 imec /
   Ghent University with no place; P8 Ligentec SA, Ecublens, CH, present address); adar1994 #2 Serbin (OCR "ATkT" /
   "IJSA"; record AT&T Bell Laboratories, Breinigsville, US only if an OCR fold is added). Recommended: add.
2. D412 author-list corrections: bundalo2022 (list stops at 30 of 32 printed names; Zoldak, O'Brien). D426 review list:
   bundalo2022 #19 (Tienforti Marcello / Marcello Tienforti), chauhan2022 #7 (C. W. Hoyt / Chad Hoyt). Recommended: add.
3. G1 last-author test case: bozzola2015 #5 Andreani marker 5 (probe O1). Recommended: add.
4. Checker gap: a country printed after an interleaved line is accepted for the wrong statement (adar1994 probe A4).
   Recommended: note with the interleaving gaps, no YAML impact.

## Unmapped org names (org round, no YAML change)

| printed org (unit) | place | proposal |
|---|---|---|
| AT&T Bell Laboratories | Murray Hill | new org or alias under a Bell Labs org |
| CSEM S.E. | Alpnach, CH | alias to CSEM if present (form as printed) |
| Cordon Electronics Italy | Agrate Brianza, IT | new org |
| Eblana Photonics | Dublin, IE | new org |
| Evoelectronics s.r.l | Pomezia, IT | new org |
| Ghent University-Interuniversity Microelectronics Center (IMEC) (INTEC) | Ghent, BE | alias to Ghent University + imec (D426 dash form) |
| Honeywell Aerospace | Plymouth, US | alias vs child (D550) |
| III-V labs | Palaiseau, FR | alias to the III-V Lab org |
| Metallux SA | Mendrisio, CH | new org |
| Pirelli Laboratories | Milan, IT | new org |
| STMicroelectronics s.r.l. | Agrate Brianza, IT | alias to STMicroelectronics |
| Shanghai Institute of Microsystem and Information Technology, Chinese Academy of Sciences | Shanghai, CN | alias to the SIMIT org (the same org string is used in earlier lit batches) |
| Universitat Politècnica València | València, ES | alias to UPV |
| University of St. Andrews | St. Andrews, GB | new org or alias |
| VLAIO | Brussel, BE | new org |
| VTT; VTT Technical Research Centre of Finland | Oulu / Espoo, FI | one org, two aliases |
| Vanguard Photonics GmbH | Karlsruhe, DE | new org |
| Sustainable Energy Authority Ireland (after F1) | Dublin, IE | new org |

(18 strings in `unmapped_orgs.csv`; 19 after F1.)

## Privacy and as-printed scan

- Grep over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv` and `papers.csv` (paper ids and decision
  ids stripped) for contact / URL patterns, street / road / avenue / boulevard / drive / via / suite / room / building /
  box / campus / complex words, the street, building, campus and Eircode strings printed in the sources, "No." + digit
  and digit runs: hits only for prose markers P10-P24, slot numbers, the year 1994 in a note, and notes that say a
  street / building / postal code exists without giving it. No contact, street, building, postal code or P.O. box
  anywhere in the batch, notes included. The F1 note text names no address item.
- As printed (kept, correct): imec/Ghent University and imec / Ghent University; III-V labs; CSEM S.E.; Evoelectronics
  s.r.l (no final period); Universitat Politècnica València; Photonics Packaging and Integration group (lower case, P3);
  Birck Nano-technology Center.

## Commands (2026-11-16 / 17, log times)

| Command | Result |
|---|---|
| `show lit_h50 --corpus lit --codes <id> --pdf`, all 25 (+ bundalo2022 `--pages 9`) | headers, statements, author lists read (scratchpad only) |
| `check lit_h50 --corpus lit --dry-run` 23:54:18 (pid 56121) | 0 errors, 1 warning (chauhan2022 slot 7); slots 178, recorded 175, no_header 3; rows 199 (grade A 199; prose 118, printed 50, single 31; primary 175, additional 17, present address 7); papers ok 23, partial 2; slots_from_header 5; multi-affiliation slots 7; 18 unmapped org strings |
| pymupdf page 9 of bundalo2022, at-signs and digits masked | author 7 present-address line printed in full in the PDF layer |
| `h50_audit/probes/probe.py` on scratch copies, 23:55-00:00 | below; repo batch files md5 unchanged |

| probe | change | result | reading |
|---|---|---|---|
| BASE | unchanged copy | 0 errors, 1 warning | baseline |
| B1 / B2 | Carrol P11 full org + Dublin / IE, readable / truncated org, readable | 0 / 0 errors | F1 valid; truncated prefix not caught |
| B9 / B10 / B11 | P11 org "Agency" / Cork / GB | 6 / 4 / 4 errors | org, city, country verified on the space-less line |
| B13 | Carrol without P11 | 4 errors | statement coverage bound |
| B3 / B4 | Wuytens readable / readable without P8 | 4 / 0 errors | gap real; B4 would drop a printed block |
| B5 / B6 / B7 | Tienforti no slot / no differs / O'Brien no slot | 0 / 1 / 1 errors | slot 19 harmless; differs and slot 0 required |
| B8 | P7 Ghent / BE | 4 errors | no place printed |
| B12 | unrelated P15 country SE | 4 errors | O1 companion errors on P1 / P2 |
| A1 / A2 / A3 / A4 | Serbin readable / AT&T / P1 US / P2 US | 1 / 4 / 2 / 0 errors | call 2 |
| C1 / C2 | Hoyt no slot / slot 0 + differs | 2 / 0 errors | call 1 |
| Z1 / Z2 | zhou2024a no P4 / ministry more_orgs | 15 / 0 errors | clause bound; parent not copied |
| D1 | doerr2010 Bell Laboratories as org | 0 errors | neutral |
| H1 / H2 | chen2010 district as locality / CN | 0 / 0 errors | neutral; D366 / D288 decide |
| U1 | burla2015 without hash entry | 0 errors | O3 |
| N1 | nielson2005 Haus on P2 | 5 errors | P4 required |
| Q1 | zhong2014 block 3 as affiliation | 2 errors | present address forced |
| G1 | gondarenko2009 US | 2 errors | empty forced |
| O1 / O2 | bozzola2015 Andreani no 5 / Carroll no 6 | 0 / 2 errors | O1 = last-author gap |
| W1 | wang2014a Zou marker 1 only | 2 errors | bound |
| L1 | larrea2018 "de" inserted | 4 errors | as printed forced |
| FIX_F1 | F1 (3 edits) | 0 errors, 1 warning | fix valid |

## Checker gaps observed (scripts not edited)

- Pronoun statement after a period that follows a capitalized word ("University.") not resolved (bundalo2022 #29); the
  same gap lets a printed present address be dropped without error (B4).
- Truncated org on a space-less continuation line passes as a prefix (B2).
- Country of an interleaved statement accepted for the next statement (adar1994 A4).
- No OCR fold for "AT&T" / "ATkT" (adar1994 A2).
- Last author's later markers not bound (bozzola2015 O1). Known (D442 / D546 / D557).
- Explicit slot vs slot 0 not machine-decided (C2).

## Verdict

GO with fix F1. All 178 list / header slots and the 2 header-only authors carry the right person; the 175 recorded slots
have the right markers, org, unit, city and country; adar1994 #2 and bundalo2022 #29 are correctly without rows (OCR
garble, checker gap). F1 turns bundalo2022 #7 Lee Carrol into two rows (Tyndall National Institute, Cork, IE;
present address Sustainable Energy Authority Ireland, Dublin, IE) instead of a truncated, unrecorded block. Nothing is
invented, no block is missed, no contact, street, building or postal text is recorded.
