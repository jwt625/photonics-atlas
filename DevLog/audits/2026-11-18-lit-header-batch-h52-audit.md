---
title: Fresh-context audit of the lit author-affiliation batch lit_h52 (22 papers)
date: 2026-11-18
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only with --dry-run, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h52/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D412, D426, D466, D546, D629); format from the lit_h49 / lit_h50 audits
verdict: GO, 0 required fixes; 153 slots (115 list + 38 slots_from_header) plus 1 header-only author audited; 146 recorded slots ok, 7 slots without rows (fontaine2019 6, piggott2020 #2), all correctly; 0 wrong rows; 1 optional note edit (N1)
---

# Lit header batch audit: lit_h52 (2026-11-18)

## Scope

Batch lit_h52: 22 papers (OSA / Optica, APS-style arXiv preprints, AIP preprints with a HAL cover page, one MEMS
conference paper, one SPIE preprint, one IEICE letter, two Chinese Optics Letters papers, one Nature-style preprint);
153 slots (dong2019, deotare2009, yu2014, deotare2009a, badri2019, tanaka2009, xing2015 with `slots_from_header`,
38 slots) plus 1 header-only author (piggott2020 Eric Y. Ma, slot 0); 190 rows. Restricted corpus: this record names
only authors, orgs, units, cities and countries; no paper text is quoted and no contact, street, building, postal-box
or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h52 --corpus lit --codes <id> --pdf`
  (all 22; tabatabavakili2017 also with `--pages 2 2`; output kept in the session scratchpad `h52_audit/show/` only).
- Per slot: printed name vs the `show` author list and `compare.csv`; marker run vs text layer and PDF layer (identical
  in both layers for every paper); block fields (org, unit chain, campus, city, country); role; locator; grade. Every
  distinct (paper, marker, role, org, unit, city, country, basis, locator, org id, match basis) tuple of
  `header_rows.csv` read (55 tuples, 190 rows).
- lu2019a symbol footnotes: page 1 prints no footnote text for the asterisk and dagger; `references/lu2019a/text.md`
  carries both as contact lines on a later page (read with at-sign tokens masked in my own output).
- Probes on scratch copies (`h52_audit/probes/probe.py` in the session scratchpad, scratch `LIT_BASE`, batch name
  `lit_p52`, `cmd_check(..., dry_run=True)`; results in `h52_audit/probes/results.txt`). md5 of every repo batch file
  identical before and after the audit; `check_stamp.txt` matches `headers.yaml` (sha256 1ec4daf1...). Probe checks
  wrote their usual logs under `logs/` (prefix `lit_headers_check_lit_p52`).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h52 | 22 / 22 | 153 + 1 header-only | 154 | 0 | 0 |

- Rows 190 (all grade A: printed 153, single 37; primary 172, additional 18, present address 0); recorded 146,
  no_header 7 (fontaine2019 all 6, unreadable paper; piggott2020 #2 Yue Ma, header name Eric Y. Ma is slot 0); papers
  ok 21, partial 0, unreadable 1 (fontaine2019); `slots_from_header` 7; `author_list_differs` 1 (piggott2020);
  explicit slots: 1 (slot 0, piggott2020 Eric Y. Ma); multi-affiliation slots 16; order differs 0; 20 unmapped org
  strings. Org match basis: name 120, alias 10, ror (no parenthetical) 2, unmapped 58 rows.
- Per paper (slots / rows): xu2021d 6 / 6; gu2021 7 / 7; dong2019 5 / 5; deotare2009 5 / 5; piggott2020 10 (+1 slot 0)
  / 9; li2017 8 / 10; cai2019 3 / 3; tabatabavakili2017 13 / 41; yu2014 9 / 9; lu2019a 7 / 11; fontaine2019 6 / 0;
  deotare2009a 5 / 5; heide2022 13 / 14; guarino2007 5 / 5; logan2018 10 / 12; liao2024 8 / 8; gu2020 8 / 8;
  badri2019 4 / 4; xie2024a 3 / 3; tanaka2009 3 / 3; pita2021 8 / 15; xing2015 7 / 7.

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (153 + 1) | 154 | 0 | 0 |
| markers (148 header authors) | 148 | 0 | 0 |
| header position (148) | 148 | 0 | 0 |
| blocks (org / unit / locality / country) (146 authors with rows) | 146 | 0 | 0 |
| unreadable calls (1 paper, 6 slots) | 6 | 0 | 0 |
| locators (all blocks; tabatabavakili2017 p.2) | all | 0 | 0 |
| notes (22) | 21 | 1 (tabatabavakili2017, N1 optional) | 0 |

## Per-paper findings

- xu2021d (6; printed, capitals): Yale University + Department of Electrical Engineering, New Haven, US; single block
  with marker 1 (D285). Joshua Surya ~ list Joshua B. Surya (dropped middle initial, automatic). ok.
- gu2021 (7; printed): NWPU + unit chain (MIIT key laboratory, Shaanxi key laboratory, School of Science; lower-case
  "light-field manipulation" as printed), Xi'an, CN, same form as lit_h22; China Academy of Space Technology + Qian
  Xuesen laboratory unit, Beijing, CN. Printed order Gan before J. Zhao equals the list. ok.
- dong2019 (5; printed, slots from header): Purdue + OxideMEMS Lab, West Lafayette, US; EPFL with its acronym,
  Lausanne, CH (postal code before the city not recorded; mapped org_epfl). ok.
- deotare2009 / deotare2009a (5 + 5; single, slots from header): Harvard + SEAS, Cambridge, country empty (no country
  printed; probe P12 US: 2 errors). Detached caron written Lončar (D282). ok.
- piggott2020 (10 + 1; printed, symbol markers): Stanford + Ginzton Laboratory, Stanford, US; SLAC + Stanford
  Institute for Materials and Energy Sciences unit, Menlo Park, US; University of California + campus Santa Barbara,
  Santa Barbara, US (printed without a comma; org_ucsb, D461 form). Section mark = equal contribution in
  `dropped_markers` for Piggott, Ma, Su (verified). Eric Y. Ma: see call 1. Vučković (detached accents, D282) ~ list
  "Jelena Vuckovic A" (known D412 artefact form). ok.
- li2017 (8; printed): Tsinghua + Department of Electronic Engineering, Beijing, CN; Arizona State + School of
  Electrical, Computer, and Energy Engineering, Tempe, US. "Jianxing, Zhang" printed with a comma, recorded Jianxing
  Zhang (checker folds punctuation). C. Z. Ning ~ Cun-Zheng Ning (hyphenated syllables, D369). Fan Fan and Ning 1,2.
  ok.
- cai2019 (3; single, capitals): Carnegie Mellon + ECE, Pittsburgh, US. See O1 (asterisk wording). ok.
- tabatabavakili2017 (13; printed, p.2 header): HAL cover page on page 1, marked author line and blocks on page 2
  (probe P6 without the locator: 20 errors). Block 1 Centre de Nanosciences et de Nanotechnologies + CNRS, Univ.
  Paris-Sud, Université Paris-Saclay, Orsay (lit_h48 / D466 form); block 2 CEA + "INAC-PHELIQS, Nanophysique et
  semiconducteurs group", Grenoble (CEA org + unit chain, D546 ferrotti2016 form); block 3 Laboratoire Charles Coulomb
  (L2C) + "CNRS-Université de Montpellier", Montpellier (UMR number between them not copied); block 4 Université Côte
  d'Azur + "CRHEA-CNRS", Valbonne; block 5 Univ. Grenoble Alpes, Grenoble; all FR. Boucaud 1 + a = contact line
  (dropped). Semond printed without accent (list F. Sèmond; folded). See call 3 and N1. ok.
- yu2014 (9; single, slots from header): DTU + unit chain DTU Fotonik, Department of Photonics Engineering, Kongens
  Lyngby, DK (postal prefix not recorded). Dagger on Yu = contact line. ok.
- lu2019a (7; printed): NIST + Center for Nanoscale Science and Technology, Gaithersburg, US; University of Maryland +
  campus College Park + Maryland NanoCenter, College Park, US (org_university_of_maryland_college_park; probe P10
  without campus: 0 errors, D301 decides); Photon Spot, Inc., Monrovia, country empty (block prints state and postal
  code only; probe P9 US: 2 errors). Gregory Moille ~ Gregory T. Moille automatic. ok.
- fontaine2019 (6; unreadable): see call 2. ok.
- heide2022 (13; printed, parenthesized markers): Eindhoven University of Technology + High-Capacity Optical
  Transmission Laboratory, Eindhoven, country empty (probe P7 NL: 2 errors); Nokia Bell Labs, New Providence, US
  (street not recorded); UCF + CREOL unit chain, Orlando, US; UNAM + Instituto de Ciencias Aplicadas y Tecnología,
  Mexico City, country empty (see call 4). Velazquez-Benitez (1),(4) (probe P21 without 4: 3 errors). ok.
- guarino2007 (5; single): ETH Zurich + Nonlinear Optics Laboratory, Institute of Quantum Electronics, Zurich, CH.
  Peter Gunter printed without umlaut in both layers (list Peter Günter; probe P17 with umlaut: 0 errors, as printed
  wins). ok.
- logan2018 (10; printed, capitals): University of Washington + Department of Electrical and Computing Engineering /
  Department of Physics, Seattle, country empty (probe P11 US: 2 errors); Humboldt-Universitat zu Berlin + Department
  of Physics, Berlin, DE (no umlaut in both layers; probe P16 with umlaut: 0 errors; lit_h26 / lit_h29 record the
  umlaut form where it is printed, so the org round needs an alias); Harvard + John A. Paulson SEAS, Cambridge,
  country empty; Princeton + Department of Electrical Engineering, Princeton, US. Majumdar and Fu 1,2. Emma R.
  Schmidgall ~ Emma Schmidgall automatic. ok.
- liao2024 (8; printed): Ningbo University + EECS department, Ningbo, CN; Zhejiang University + Centre for Optical and
  Electromagnetic Research, College of Optical Science and Engineering, Hangzhou, CN. Chen Tang ~ list "Chen Ying Tang"
  automatic (dropped middle); see open question 2. ok.
- gu2020 (8; printed): NWPU + MOE key laboratory / Shaanxi key laboratory / School of Science chain, Xi'an; Sun Yat-Sen
  University + state key laboratory, School of Physics, Guangzhou; CAST + Qian Xuesen laboratory, Beijing; all CN.
  Printed order equals the list. ok.
- badri2019 (4; printed letter markers, slots from header): Islamic Azad University + "Department of Electrical
  Engineering, Sarab Branch", Sarab / "... Tabriz Branch", Tabriz; University of Tabriz + "School of Engineering-
  Emerging Technologies" (hyphen-space as printed), Tabriz; all IR (postal code not recorded). ok.
- xie2024a (3; printed, capitals): University of Colorado + campus Boulder + ECE department, Boulder, US
  (org_university_of_colorado_boulder; lit_h06 / h43 / h47 form; probe P24 whole-string org: 0 errors, D301 decides).
  Marker 2 on Xie = contact line (probe P13 without it: 2 errors). Campus mail code not recorded. ok.
- tanaka2009 (3; single, slots from header): Keio University + School of Integrated DESIGN Engineering, Graduate School
  of Science and Technology, locality Yokohama-shi (D366; lit_h02 form), JP; ward Kohoku-ku named in the note only
  (lit_h35 / h36 / h38 precedent: ward printed before the city goes to the note); the street-number span, the
  neighbourhood name and the postal code are not in any field or note. Probes P14 (Yokohama) and P15 (Kohoku-ku) both
  0 errors: checker neutral, D366 / D288 decide. Marker a = contact line (probe P20 without it: 2 errors). ok.
- pita2021 (8; printed, capitals): University of Campinas + Photonics Research Center / School of Electrical and
  Computer Engineering / "Gleb Wataghin" Physics Institute (curly quotes as printed), Campinas, BR (alias to
  org_state_university_of_campinas); Corning Research & Development Corporation, Corning, US (street not recorded);
  State University of São Paulo + Campus of São João da Boa Vista, São João da Boa Vista, BR. Kocabaş written with
  cedillas (D282). Name variants: JULIAN L. PITA RUIZ ~ Julián L. Pita (second family name dropped), JUN YANG ~ Jun Mo
  Yang, PAULO DAINESE ~ Paulo Clovis Dainese Junior, all automatic. Dainese 1,3,4 (probe P22 without 4: 2 errors). ok.
- xing2015 (7; single, slots from header): Institute of Semiconductors, Chinese Academy of Sciences (one name) + State
  Key Laboratory on Integrated Optoelectronics, Beijing, CN. ok.

## Extractor calls (verified)

1. piggott2020 "Eric Y. Ma" vs list "Yue Ma" as slot 0 + `author_list_differs`. Probe P2 (no slot): 1 error (matches 0
   slots); probe P1 (slot 2, differs false): 0 errors, 1 warning, so the checker is neutral between slot 0 and slot 2.
   The printed first given name (E.) is not explained by the list form; D287 lists "J. I. / Iwan" and "R. M. / Mark"
   (first initial differs, second agrees) as slot 0, the same pattern. Keep; the middle initial Y. agrees with "Yue",
   so add to the D426 review list (cost: list slot 2 without rows, Stanford and SLAC blocks without rows).
2. fontaine2019 unreadable. Both marked blocks, the equal-contribution line and the contact line are printed above the
   title and author line in both layers. Probe P3 (blocks recorded, p.1 header) and P26 (blocks with `p.1 footnote`
   locator): 6 errors each (block not found after the author line, both layers). Same checker gap as liu2010a (lit_h47),
   hu2022, lukin2019. The note's "printed, not recorded" summary names orgs, unit, cities and countries only. Keep;
   re-record list.
3. tabatabavakili2017 dash-joined "CNRS-Université de Montpellier" and "CRHEA-CNRS" kept whole. Probes P4 / P5 (split
   into two orgs each): 0 errors, checker neutral. lit_h48 tabatabavakili2019 splits because that paper prints the
   orgs comma-separated; this paper prints them dash-joined, and D426 keeps dash-joined pairs as printed (aliases in
   the org round, older split forms left). Probe P23 (UMR number included): 0 errors; precedent (lit_h01, h27, h29,
   h30) is "UMR number not copied". Keep.
4. Empty countries: heide2022 block 1 (no country printed) and block 4 (México only inside the org name, Mexico City
   as the city; probe P8 MX: 0 errors because the checker finds the name inside the block), lu2019a block 3, logan2018
   blocks 1 / 2 / 4, deotare2009 / deotare2009a. D249: no inference, a name inside the org is not the place; empty is
   right for all. lit_h10 UNAM records MX where the country is printed separately. Keep.
5. Names without umlauts (logan2018 Humboldt-Universitat, guarino2007 Gunter): no diacritic in either layer (not a
   detached-accent artefact, so D282 does not apply); as printed. Keep.
6. Campus localities: piggott2020 Santa Barbara, lu2019a College Park, xie2024a Boulder all `org` + `campus` (D301),
   each mapped to its campus org id. Keep.
7. slots_from_header (dong2019, deotare2009, deotare2009a, yu2014, badri2019, tanaka2009, xing2015): `show` prints
   "[no author list: slots_from_header (D352)]" for all seven; header order recorded. Keep.

## Fixes (exact YAML edits)

No required fix.

N1 (optional, note only; tabatabavakili2017): the note does not say that block 3 prints a UMR number between L2C and
the dash-joined pair (precedent notes lit_h27 / h29 / h30 say "UMR number not copied"). In `lit:tabatabavakili2017`
replace

```yaml
block 3 prints the joint unit L2C before the dash-joined CNRS-Université de Montpellier (kept as printed, D426);
```

with

```yaml
block 3 prints the joint unit L2C before the dash-joined CNRS-Université de Montpellier (kept as printed, D426; UMR number not copied);
```

No field change; `check` must be re-run to refresh the stamp (rows unchanged at 190).

## Observations (no change recommended)

- O1 cai2019, logan2018, guarino2007: the notes call the asterisk the corresponding-author mark, but page 1 shows only
  a masked contact line or no footnote at all (cai2019); same wording as earlier batches (h48 O1, h50 O2). Symbol
  marks need no entry. No fix.
- O2 tabatabavakili2017 Boucaud: probe P19 (without the `dropped_markers` entry for a): 0 errors, the known last-author
  gap (D629 G1 list). The recorded entry is correct.
- O3 piggott2020: with Eric Y. Ma at slot 0, the SLAC block has no row in this batch.

## Open questions (with recommendation)

1. D426 review list: piggott2020 #2 (printed Eric Y. Ma, list Yue Ma; middle initial agrees). Recommended: add; if the
   coordinator rules this a name-part variant (D287 Seyed Morteza / Morteza form), set `slot: 2` and
   `author_list_differs: false` (probe P1: 0 errors, 1 warning).
2. D412 author-list corrections: liao2024 #5 list "Chen Ying Tang" (the printed Chinese name has a one-syllable given
   name, so "Ying" is not supported by the source); piggott2020 #10 "Jelena Vuckovic A" (known form). Recommended: add.
3. Re-record list (checker gap, blocks above the title): fontaine2019 (values in its note). Recommended: add with
   liu2010a / hu2022 / lukin2019.

## Unmapped org names (org round, no YAML change)

| printed org (unit) | place | proposal |
|---|---|---|
| Arizona State University | Tempe, US | new org or alias |
| CNRS-Université de Montpellier | Montpellier, FR | alias to CNRS + Université de Montpellier (D426 dash form) |
| CRHEA-CNRS | Valbonne, FR | alias to CNRS (+ CRHEA if curated) |
| Carnegie Mellon University | Pittsburgh, US | new org or alias |
| China Academy of Space Technology | Beijing, CN | new org |
| Humboldt-Universitat zu Berlin | Berlin, DE | alias to the Humboldt-Universität zu Berlin org (printed without umlaut) |
| Islamic Azad University (Sarab / Tabriz branches) | Sarab / Tabriz, IR | new org (branches as units) |
| Laboratoire Charles Coulomb (L2C) | Montpellier, FR | new org (joint unit) |
| Ningbo University | Ningbo, CN | new org |
| Northwestern Polytechnical University (two unit chains) | Xi'an, CN | new org (also lit_h22) |
| Photon Spot, Inc. | Monrovia | new org |
| Princeton University | Princeton, US | new org or alias |
| State University of São Paulo | São João da Boa Vista, BR | new org (campus as unit) |
| Univ. Grenoble Alpes | Grenoble, FR | alias |
| Univ. Paris-Sud | Orsay, FR | alias |
| Universidad Nacional Autónoma de México | Mexico City | alias (lit_h10 prints it with UNAM) |
| University of Tabriz | Tabriz, IR | new org |
| Université Paris-Saclay | Orsay, FR | alias |

(20 rows in `unmapped_orgs.csv`; the two NWPU unit chains and the two Islamic Azad branches are one line each above.)

## Privacy and as-printed scan

- Grep over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv` and `papers.csv` (paper ids and
  decision ids stripped) for contact / URL patterns, street / road / avenue / drive / via / suite / room / building /
  box / complex words, the street, campus-address, mail-code, neighbourhood and postal strings printed in these
  sources, state abbreviations and digit runs: hits only for marker / slot digits, "DevLog-011" and notes that say a
  street address, campus address, campus mail code or postal code exists without giving it. The word e-mail does not
  appear. No contact, street, building, postal code or P.O. box anywhere in the batch, notes included. The ward
  Kohoku-ku in the tanaka2009 note is a district name (D366 note rule), not an address item.
- As printed (kept, correct): "Key Laboratory of light-field manipulation ..." (lower case), "Qian Xuesen laboratory
  of Space Technology", "Department of Electrical and Computing Engineering", "School of Engineering- Emerging
  Technologies", "School of Integrated DESIGN Engineering", "Humboldt-Universitat zu Berlin", "Peter Gunter",
  "Yokohama-shi", "Photon Spot, Inc.".

## Commands (2026-11-18, log times)

| Command | Result |
|---|---|
| `show lit_h52 --corpus lit --codes <id> --pdf`, all 22 (+ tabatabavakili2017 `--pages 2 2`) | headers, author lists read (scratchpad only) |
| `check lit_h52 --corpus lit --dry-run` 09:34:12 (pid 74081) | 0 errors, 0 warnings; slots 153, recorded 146, no_header 7; rows 190 (grade A 190; printed 153, single 37; primary 172, additional 18); papers ok 21, unreadable 1; slots_from_header 7; multi-affiliation slots 16; 20 unmapped org strings |
| `h52_audit/probes/probe.py` on scratch copies, 09:36-09:39 | below; repo batch files md5 unchanged |

| probe | change | result | reading |
|---|---|---|---|
| BASE | unchanged copy | 0 errors, 0 warnings | baseline |
| P1 / P2 | piggott2020 Ma slot 2 (differs false) / no slot | 0 + 1 warning / 1 error | call 1: checker neutral, rule decides |
| P3 / P26 | fontaine2019 blocks recorded (header / footnote locator) | 6 / 6 errors | call 2: unreadable forced |
| P4 / P5 | tabatabavakili2017 L2C pair / CRHEA pair split | 0 / 0 errors | call 3: D426 decides |
| P6 | tabatabavakili2017 without p.2 locators | 20 errors | locator required |
| P23 | tabatabavakili2017 UMR number in more_orgs | 0 errors | precedent decides (not copied) |
| P7 / P8 | heide2022 block 1 NL / block 4 MX | 2 / 0 errors | call 4 |
| P9 | lu2019a block 3 US | 2 errors | empty forced |
| P10 / P24 / P18 | campus dropped: lu2019a / xie2024a / piggott2020 | 0 / 0 / 0 errors | D301 decides |
| P11 / P12 | logan2018 block 1 US / deotare2009 US | 2 / 2 errors | empty forced |
| P13 / P20 | xie2024a without dropped 2 / tanaka2009 without dropped a | 2 / 2 errors | entries required |
| P14 / P15 | tanaka2009 locality Yokohama / Kohoku-ku | 0 / 0 errors | D366 / D288 decide |
| P16 / P17 | Humboldt with umlaut / Günter with umlaut | 0 / 0 errors | as printed decides |
| P19 | tabatabavakili2017 Boucaud without dropped a | 0 errors | O2 last-author gap |
| P21 / P22 | heide2022 Velazquez-Benitez without 4 / pita2021 Dainese without 4 | 3 / 2 errors | bound |
| P25 | dong2019 EPFL without acronym | 0 errors | neutral; as printed kept |

## Checker gaps observed (scripts not edited)

- Blocks printed above the title / author line not searched (fontaine2019; known, liu2010a / hu2022 / lukin2019).
- A country name inside an org name satisfies the country check (heide2022 P8 MX).
- Last author's extra markers not bound (tabatabavakili2017 P19; known D629 G1).
- Slot 0 vs explicit slot for a first-initial difference not machine-decided (piggott2020 P1).

## Verdict

GO, no required fix. All 153 list / header slots and the 1 header-only author carry the right person; the 146
recorded slots have the right markers, org, unit, city and country; fontaine2019 (blocks above the title) and
piggott2020 #2 (printed Eric Y. Ma, slot 0 under D287) are correctly without rows. Nothing is invented, no block is
missed, no contact, street, building or postal text is recorded. N1 is an optional note wording edit.
