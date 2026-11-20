---
title: Fresh-context audit of the lit author-affiliation batch lit_h57 (25 papers)
date: 2026-11-20
mode: read-only on the batch (wrote only this record and scratchpad show dumps, page renders and probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only as dry runs on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h57/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D287, D366, D368, D369, D380, D410, D426, D442, D572); format from the lit_h56 audit
verdict: GO after F1-F3; 152 slots (69 list + 83 slots_from_header) audited; 146 recorded slots with 1 wrong row (yasuoka2005 #4, OCR given name Tom for the printed Toru, F2) and 11 imprecise (2 unreadable-author name forms fixed by F1 / F2, 6 unit strings fixed by F3, 3 not fixable: city garbled in both text layers); rows 152 -> 151 after the fixes
---

# Lit header batch audit: lit_h57 (2026-11-20)

## Scope

Batch lit_h57: 25 papers (Optics Express / IEEE JQE / PTL / JLT / Photonics Journal, five conference papers, four
1990s-2000s OCR scans); 152 slots, 14 papers `slots_from_header`; 152 rows. Restricted corpus: this record names only
authors, orgs, units, cities and countries; no paper text is quoted and no contact, street, building, postal-box or
postal text is copied (address parts are described, not named).

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h57 --corpus lit --codes <id> --pdf`
  (all 25; shi2010 and olivares2021 also with `--pages 2`); output kept in the session scratchpad `h57_audit/show/`.
- Page renders (`pdftoppm`, page 1, scratchpad `h57_audit/render/`) for the four partial papers (goncher1996, chang2008,
  clark2003, yasuoka2005) and the author lines of the two other OCR scans (lu1996, babic1995): every OCR-garbled name,
  city and statement compared with the printed page.
- Per slot: printed name vs the `show` author list and `compare.csv`; marker run (text and PDF layers); prose statement
  subjects and verbs; block fields (org, unit chain, campus, city, country); role; locator; continuation; notes.
- 49 distinct (paper, role, org, city, country, basis, org id) tuples of `header_rows.csv` read (152 rows; grade A 152;
  primary 146, additional 1, present address 5).
- Address / contact scan of `headers.yaml` and the derived CSVs (postal-code, street, building, box, phone, fax, mail,
  URL patterns and the address parts printed in these papers): clean. Notes name street, postal box, phone, fax and
  postal code only as words ("not recorded"); the one building name sits in `skip_between` (thomson2010), which is
  verified and never stored by design (D380, thomson2007 precedent); it is absent from all three derived CSVs.
- Precedent scans over all committed lit `headers.yaml`: CUDOS / SUPA blocks (lit_h14 singaravelu2019, lit_h28,
  lit_h34, lit_h47 kasture2016 / xiong2011), Heriot-Watt blocks (lit_h18 thomson2007, lit_h22, lit_h47, lit_h51),
  NTT Corporation unit forms (17 unit strings), empty-country blocks (106), University of Illinois forms, unreadable
  author name forms (40 committed: all carry the real name, none an OCR garble).
- Probes on scratch copies (`h57_audit/probes/probe.py`: scratch `LIT_BASE`, batch name `lit_p57`,
  `cmd_check(..., dry_run=True)`; 27 probe runs). Dry-run check of the batch as written: 0 errors, 2 warnings (kang2019
  order, tossoun2018 explicit slot); totals equal the stamped derived files (152 slots, 146 recorded, 6 no_header, 152
  rows). md5 of every repo batch file identical before and after the audit; `check_stamp.txt` matches `headers.yaml`
  (sha256 03f666a2...). Probe checks wrote their usual logs under `logs/` (prefix `lit_headers_check_lit_p57`, 54 files).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h57 | 25 / 25 | 152 | 140 (136 recorded + 4 no_header) | 11 (9 recorded, 2 no_header) | 1 (yasuoka2005 #4) |

- Papers ok 21, partial 4 (goncher1996, chang2008, clark2003, yasuoka2005), unreadable 0; after F2 yasuoka2005 has two
  unreadable authors. `slots_from_header` 14 (lamont2008, thomson2010, umeki2011, lu1996, shi2010, goncher1996,
  chang2008, nishiyama2005, babic1995, imai2010, clark2003, joshi2008, kinsey2001, yasuoka2005; all print the D352
  line in `show` and have `n_authors_meta` 0); `author_list_differs` 0; explicit slots 1 (tossoun2018 #6); order
  warnings 1 (kang2019).
- Per paper (slots / rows): ayan2023 4 / 4; lamont2008 6 / 6; sabapathy2012 5 / 6; agazzi2010 8 / 8; thomson2010 4 / 4;
  umeki2011 4 / 6; lu1996 6 / 9; shi2010 7 / 7; goncher1996 8 / 5; fu2020 7 / 7; chang2008 2 / 1; chaw2025 4 / 4;
  nishiyama2005 9 / 9; wu2025b 5 / 5; babic1995 9 / 9; imai2010 10 / 10; olivares2021 3 / 3; kang2019 12 / 12;
  clark2003 8 / 7; joshi2008 2 / 2; tossoun2018a 6 / 6; nada2020 8 / 8; tossoun2018 7 / 7; kinsey2001 3 / 3;
  yasuoka2005 5 / 4 (3 after F2).

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (152) | 149 | 2 (chang2008 #2, yasuoka2005 #2: unreadable authors recorded with an OCR garble / initial; F1, F2) | 1 (yasuoka2005 #4, F2) |
| markers (printed / prose / single / grouped, 146 recorded) | 146 | 0 | 0 |
| header position / statement subject | 146 | 0 | 0 |
| blocks (org / unit / locality / country) (146 slots with rows) | 137 | 9 (clark2003 #1, #2, #4-#7 unit trailing period, F3; goncher1996 #8 and yasuoka2005 #1, #3 locality empty, city garbled in both text layers, not fixable) | 0 |
| unreadable calls (6 slots) | 6 | 0 | 0 (1 missing: yasuoka2005 #4, F2) |
| present addresses (5: lu1996 3, umeki2011 2) | 5 | 0 | 0 |
| locators | all | 0 | 0 |
| notes (25) | 23 | 0 | 2 (chang2008, yasuoka2005: follow F1 / F2) |

## Per-paper findings

- ayan2023 (4; printed, capitals): EPFL twice, as printed with and without the accent on the E; units PHOSL / LPQM;
  Lausanne, CH. Institute codes and campus station numbers not recorded. List matches (Tobias Jan Kippenberg). ok.
- lamont2008 (6; printed, slots from header): call 2. ok.
- sabapathy2012 (5 / 6 rows; printed): IISc Department of Instrumentation and Applied Physics (1) and Applied Photonics
  Initiative (3), Bangalore, IN; Heriot-Watt School of Engineering and Physical Sciences, Edinburgh, GB. Asokan 1,3.
  List forms Ajoy Kumar Kar, S. Asokan match. ok.
- agazzi2010 (8; printed): University of Twente with the group + MESA+ chain, Enschede, NL; Ghent University
  Photonics Research Group + INTEC department, Gent, BE (as printed). Postal box and street not recorded. ok.
- thomson2010 (4; printed, slots from header): call 1. Marker 2 = equal contribution (dropped) on Psaila and Beecher in
  both layers. ok.
- umeki2011 (4 / 6 rows; printed, slots from header): calls 8. NTT Corporation with units "NTT Photonics Labs" (Atsugi)
  and "NTT Network Innovation Labs." (Yokosuka) as printed (corpus has both unit forms; the place words before the city
  are street-address parts with house numbers, not recorded). ok.
- lu1996 (6 / 9 rows; prose, slots from header): five "was with" / "is with" statements and three "He is now with"
  pronoun statements, each its own block P1-P9 in printed order; UNM CHTM (x3), Sandia (x2), Tektronix, Inc. (Beaverton);
  present addresses SDL, Inc., ArrayComm (San Jose), Hewlett-Packard Laboratories (Palo Alto). Author line checked on
  the render (Bo Lu, John C. Zolper). ok.
- shi2010 (7; printed, slots from header): call 7. NCU EE Taoyuan, NTU EE Taipei (TW), IQE (Europe) Ltd. Cardiff, GB
  ("U.K." printed). Marker 3 of Pinches printed with a space in the text layer, attached in the PDF layer. ok.
- goncher1996 (8 / 5 rows; prose, partial): call 4 and 9 and the partial section below. Readable authors (Luo, Cheng,
  Hersee, Sun: UNM CHTM, Albuquerque; Zolper: Sandia) match the render. ok as recorded; #8 locality imprecise.
- fu2020 (7; printed, conference): markers "1." / "2." before the blocks; UIUC with the Holonyak lab + ECE chain,
  Urbana, US; sdPhotonics, LLC, Orlando, US. List form DENNIS GLENN DEPPE matches. ok.
- chang2008 (2 / 1 row; single, partial): UCSB ECE Department with campus Santa Barbara (D301), US. Partial section.
- chaw2025 (4; prose): "The authors" statement, UIUC Holonyak lab (printed without "Jr." here, hyphenated across the line
  break) + ECE, Urbana, US. ok.
- nishiyama2005 (9; prose, slots from header): "The authors" statement, Corning Inc., Corning, US. ok.
- wu2025b (5; prose): "The authors" statement, The University of Illinois at Urbana-Champaign (leading article as
  printed, D288) with the Holonyak, Jr. lab + ECE chain, Urbana, US. ok.
- babic1995 (9; prose, slots from header): UCSB ECE (campus Santa Barbara), Royal Institute of Technology, Stockholm, SE,
  Hewlett-Packard Laboratories, Palo Alto, US with `continued: "tories"` (statement split by the log-number line).
  Author line checked on the render (Babić, Near M. Margalit as printed). ok.
- imai2010 (10; single, slots from header): Furukawa Electric Co., Ltd. Photonic Device Research Center, Ichihara, JP
  (street, prefecture, postal code not recorded). ok.
- olivares2021 (3; single): call 7. Nanophotonics Technology Center, UPV, Valencia, ES; list Jorge O. Parra matches
  Jorge Parra (dropped middle initial, automatic). ok.
- kang2019 (12; prose): KAIST School of EE (9) and National NanoFab Center (NNFC) (3), Daejeon, KR ("South Korea"). Order
  warning: the list puts Youn, Yu and Park at positions 2-4; slots matched by name. ok.
- clark2003 (8 / 7 rows; prose, partial): Nortel with units Advanced Technology Lab (6 authors) and Nortel
  Optoelectronics (Thomas; Noel unreadable), Nepean, CA. The render prints "Lab," (comma); the trailing period in the
  unit is an OCR artefact: F3. The mailing-address line names no affiliation (not recorded, correct). Partial section.
- joshi2008 (2; prose, slots from header): Discovery Semiconductors, Ewing, US. ok.
- tossoun2018a (6; prose): UVA Charles L. Brown ECE, Charlottesville, US (Tossoun, Zang, Holmes, Beling); UNM ECE,
  Albuquerque, US. List A.L. Holmes matches printed Archie L. Holmes, Jr. automatically. ok.
- nada2020 (8; printed, conference): call 6. ok.
- tossoun2018 (7; prose): call 3. ok.
- kinsey2001 (3; prose, slots from header): UT Austin ECE + Microelectronics Research Center, Austin, US; Lucent
  Technologies Crawford Hill Laboratory, Holmdel, US. ok.
- yasuoka2005 (5 / 4 rows; grouped, partial): calls 4 and 5, partial section; #4 wrong (F2).

## Extractor calls (verified)

1. thomson2010 SUPA at the start of the unit chain, org Heriot-Watt University, building name in `skip_between`. The
   single block prints alliance, school, physics department, building name, university, city, postal code, Scotland.
   Probes: TH1 (unit without SUPA) 2 errors (first field not at the block start); TH2 (no `skip_between`) 2 errors
   (unit and org not contiguous); TH3 (SUPA as org, school / department as unit, Heriot-Watt in `more_orgs`) 2 errors.
   The recorded form is the only one the checker accepts and matches the lit_h47 kasture2016 form (ARC centre CUDOS
   printed before school and university -> unit chain) and the thomson2007 building `skip_between` (lit_h18). lit_h14
   singaravelu2019 records SUPA as org only because that block prints no university. GB for a block printing Scotland
   (thomson2007, bino2018 precedent). Confirmed.
2. lamont2008 CUDOS in the unit chain for both blocks (centre printed before the school / centre and the university,
   kasture2016 form; lit_h28 used `more_orgs` only where CUDOS is printed after the university). Probe L1 (unit without
   CUDOS) 2 errors. Block 1 prints the state and postal code but no city: locality empty (D288; xiong2011 block 2, same
   University of Sydney case). Block 2 Canberra, "The Australian National University" with its article as printed.
   Confirmed.
3. tossoun2018 explicit slot 6 for Archie Holmes Jr. (list A.L. Holmes). Probe T1 (no slot) 2 errors (0 matches, slot 6
   unmatched); T2 (`slot: 0` + `author_list_differs`) 0 errors, so the checker allows either. The printed form drops
   only the middle initial; the same group's tossoun2018a prints Archie L. Holmes, Jr. at UVA (automatic match), the
   statement prints A. Holmes, and slot 6 is the only Holmes: a D287 / D369 name-part variant. Holmes is not a rare
   family name, so the call rests on the corroboration, not on distinctiveness. Keep; D426 review list.
4. Garbled cities left empty: goncher1996 P4 (Sandia; both text layers print a garbled city, the render prints
   Albuquerque) and yasuoka2005 G1 (both layers "Arsugi", render Atsugi). Probes G4 / Y3 (the real city) 2 errors each:
   the checker verifies only the text layers. Empty is the only recordable value; the three slots (goncher1996 #8,
   yasuoka2005 #1, #3) are imprecise, values on the re-record list. Confirmed.
5. yasuoka2005 G2 locality "Showa-cho": the place line prints, in order, an address part (block name with a house
   number), showa-cho, Nakakoma District (as "-gun") and a garbled prefecture, then the postal code and Japan. Showa-cho
   is the town (municipality) of Shōwa in Nakakoma District, Yamanashi: a locality, the first printed city-level place
   (D288), with its "-cho" designation kept like "-shi" (D366). The preceding address part is the street-level element
   and is correctly not recorded. Probes Y4 (address part as locality) and Y6 (district as locality) also pass (0 errors,
   checker gap: no city test), so the call rests on the reading, not on the checker. Printed lower-case "showa-cho"
   (both layers and render); the YAML capitalizes it (case folded by the checker; observation O3, no fix). Confirmed.
6. nada2020 country "" on both blocks: the two blocks print only unit + NTT Corporation (block 1 followed by the contact
   line); no place anywhere in the header. Probe N1 (JP) 2 errors. D249 no inference; 106 committed empty-country blocks.
   Confirmed.
7. shi2010 / olivares2021 blocks from the p.2 header: page 1 of both is the Photonics Journal cover (names without
   markers / without blocks); the marked author line and the blocks are on text.md page 2 (both layers).
   `locator: "p.2 header"` on every block (D366 cover-page rule). Confirmed.
8. umeki2011 "Currently with" blocks 3 / 4 as present addresses: printed as marked blocks 3 and 4 with the cue; markers
   1,3 (Tadanaga) and 2,4 (Takada) in both layers. Probe U2 (block 4 as affiliation) 2 errors. Block 3 prints only a
   prefecture: locality empty (probe U1 with the prefecture: 0 errors, known D572 gap). Block 4 Tokushima. Confirmed.
9. goncher1996 B. Lu "on leave from" not recorded: the statement prints SDL Inc (San Jose) followed by an "on leave from"
   clause naming UNM CHTM; D249 (on leave = not an affiliation), the note says so. Confirmed.

## Partial papers: can any unreadable author be recovered?

| paper | slot | printed (render) | text layers | probe | result |
|---|---|---|---|---|---|
| goncher1996 | #1 G. Goncher | statement 1 after a funding sentence ending with a period | period lost after the contract number; subject window runs into the funding sentence | G1 readable | 2 errors (not named in subject) |
| goncher1996 | #2 Bo Lu | statement 2 inside column interleaving | preceding body line without a period | G2 readable | 2 errors (not named in subject) |
| goncher1996 | #7 R. P. Schneider | Schneider in the statement subject | Schnejder in both layers (lookalike) | G3 readable | 2 errors (not named in subject) |
| chang2008 | #2 | Larry A. Coldren | LaITY A. Coldren in both layers | C1 readable as Larry | 3 errors (name not printed); C2 unreadable with the real name: 0 errors |
| clark2003 | #3 | J.-P. Noel in the statement | statement subject garbled ("J . 2 . Noel") | CL1 readable | 6 errors; CL3 garbled form 7 errors |
| yasuoka2005 | #2 | Haruhiko Kuwatsuka | given name garbled in both layers | Y1 unreadable with the full name | 0 errors |
| yasuoka2005 | #4 | Toru Uchida | Tom Uchida in both layers (lookalike) | Y2 readable as Toru | 2 errors (not printed before the block); Y1 unreadable as Toru: 0 errors |

None of the six unreadable authors can be made readable: the checker reads only the text layers. Two recorded name
forms are not the printed names (chang2008 #2 OCR garble, yasuoka2005 #2 initial only); with `slots_from_header` the
YAML name is the slot's name in `compare.csv`, and every committed unreadable author carries the real printed name
(40 cases; clark2003 #3 in this batch does too). D282: write the intended letters. F1, F2.

yasuoka2005 #4 was recorded readable as "Tom Uchida": the page prints Toru Uchida; "Tom" is the OCR reading of "Toru"
in both layers (the same lookalike class that made the extractor mark chang2008 #2 unreadable). The readable record puts
a wrong given name on a Fujitsu Quantum Devices row: wrong. The correct name cannot pass the name check (Y2), so the
author becomes unreadable with the printed name (F2; rows 152 -> 151, Fujitsu Quantum Devices 2 -> 1). The grouped
block G2 still verifies with Yasaki as the first readable carrier (Y1 0 errors).

## Fixes (exact YAML edits)

F1 (chang2008 #2 name form and note). In `lit:chang2008` replace

```yaml
    - {name: "LaITY A. Coldren", markers: [], unreadable: true}
```

with

```yaml
    - {name: "Larry A. Coldren", markers: [], unreadable: true}
```

and in its `note:` string replace

```yaml
author 2 printed LaITY A. Coldren (OCR lookalike), unreadable (no rows)
```

with

```yaml
author 2 printed Larry A. Coldren on the page render, both text layers read LaITY (OCR lookalike): recorded with the name from the render, unreadable (no rows)
```

F2 (yasuoka2005 #2 name form, #4 wrong readable name, note). In `lit:yasuoka2005` replace

```yaml
    - {name: "H. Kuwatsuka", markers: ["G1"], unreadable: true}
```

with

```yaml
    - {name: "Haruhiko Kuwatsuka", markers: ["G1"], unreadable: true}
```

replace

```yaml
    - {name: "Tom Uchida", markers: ["G2"]}
```

with

```yaml
    - {name: "Toru Uchida", markers: ["G2"], unreadable: true}
```

and in its `note:` string replace

```yaml
author 2 printed with a garbled given name (H d i k o), recorded with its initial only and unreadable (no rows)
```

with

```yaml
author 2 printed Haruhiko Kuwatsuka on the page render, both text layers garble the given name: recorded with the name from the render, unreadable (no rows); author 4 printed Toru Uchida on the page render, both text layers read Tom (OCR lookalike): recorded with the name from the render, unreadable (no rows)
```

(status stays `partial`).

F3 (clark2003 P1 unit, OCR period). In `lit:clark2003` replace

```yaml
unit: "Advanced Technology Lab."
```

with

```yaml
unit: "Advanced Technology Lab"
```

(the render prints a comma after "Lab"; probe CL2 0 errors).

Combined probe FINAL (F1 + F2 + F3): 0 errors, 2 warnings (unchanged); slots 152, recorded 145, no_header 7, rows 151
(grouped 3, printed 56, prose 78, single 14; present address 5).

## Observations (no YAML change)

- O1 Checker reads only the text layers, so a city or name garbled in both layers cannot be recorded even when the
  render is clear (goncher1996 P4 Albuquerque, yasuoka2005 G1 Atsugi, the six unreadable authors). A render-verified
  basis would recover 9 rows; until then these stay on the re-record list.
- O2 Statement subject window: goncher1996 statements 1 and 2 fail because the OCR lost the period ending the previous
  sentence; the subject then starts in the funding text. A subject parse that starts at the last name-list run before
  the verb would make both readable.
- O3 yasuoka2005 G2 locality capitalized ("Showa-cho") while printed lower-case; harmless (case folded, municipality's
  proper form), noted for the "as printed" rule.
- O4 Locality checks accept a prefecture (umeki2011 U1) and an address part or district (yasuoka2005 Y4 / Y6): known
  D572 gap, now with a Japanese address-part case.
- O5 tossoun2018 #6: the checker accepts both the explicit slot and `slot: 0` + `author_list_differs` (T2), because
  "Archie" vs "A. L." is not strict-compatible and D302 does not fire; the explicit slot is the documented D287 / D369
  choice.

## Lists for the coordinator

- D426 review list: tossoun2018 #6 (Archie Holmes Jr. / A.L. Holmes, explicit slot, corroborated by tossoun2018a).
- Re-record list (after O1 / O2): goncher1996 #1 Tektronix, Inc (Beaverton, US), #2 SDL Inc (San Jose, US), #7 Sandia
  National Laboratories, #8 and #7 locality Albuquerque; chang2008 #2 UCSB ECE Department (campus Santa Barbara, US);
  clark2003 #3 Nortel Optoelectronics, Nortel (Nepean, CA); yasuoka2005 #1 and #3 locality Atsugi
  (JP), #2 Fujitsu Laboratories LTD. (Atsugi, JP), #4 Fujitsu Quantum Devices LTD. (Showa-cho, JP).
- Org round (22 unmapped strings before the fixes, 22 after): ArrayComm; Discovery Semiconductors; Fujitsu Laboratories
  LTD.; Fujitsu Quantum Devices LTD.; Heriot-Watt University (two unit strings); Hewlett-Packard Laboratories; Indian
  Institute of Science (two units); KAIST; NTT Electronics Corporation; National NanoFab Center (NNFC); Nortel (two
  units); Royal Institute of Technology (alias of KTH); The Australian National University; The University of New Mexico
  / University of New Mexico (three unit strings); University of Texas at Austin; University of Tokushima; sdPhotonics,
  LLC.

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 2 warnings | batch as written |
| TH1 / TH2 / TH3 | thomson2010 unit without SUPA / no `skip_between` / SUPA as org + Heriot-Watt in `more_orgs` | 2 / 2 / 2 errors | recorded form required (call 1) |
| L1 | lamont2008 block 1 unit without CUDOS | 2 errors | unit chain required (call 2) |
| T1 / T2 | tossoun2018 no slot / `slot: 0` + `author_list_differs` | 2 / 0 errors | explicit slot needed; slot 0 also accepted (O5) |
| G1 / G2 / G3 | goncher1996 #1 / #2 / #7 readable | 2 / 2 / 2 errors | unreadable kept |
| G4 | goncher1996 P4 locality Albuquerque | 2 errors | empty forced (call 4) |
| G5 | goncher1996 P3 without `continued` | 4 errors | continuation required |
| C1 / C2 | chang2008 #2 readable as Larry / unreadable as Larry | 3 / 0 errors | F1 |
| CL1 / CL3 | clark2003 #3 readable / garbled form | 6 / 7 errors | unreadable kept |
| CL2 | clark2003 unit without the period | 0 errors | F3 |
| Y1 | yasuoka2005 #2 Haruhiko, #4 Toru unreadable | 0 errors, rows 151 | F2 |
| Y2 | yasuoka2005 #4 readable as Toru | 2 errors | unreadable required |
| Y3 | yasuoka2005 G1 locality Atsugi | 2 errors | empty forced (call 4) |
| Y4 / Y6 / Y5 | yasuoka2005 G2 locality address part / district / lower-case town | 0 / 0 / 0 errors | checker gap O4; reading decides (call 5) |
| U1 / U2 | umeki2011 block 3 prefecture / block 4 as affiliation | 0 / 2 errors | O4 gap / role verified |
| N1 | nada2020 block 1 country JP | 2 errors | empty country verified |
| FINAL | F1 + F2 + F3 | 0 errors, 2 warnings, rows 151 | fixes pass |
