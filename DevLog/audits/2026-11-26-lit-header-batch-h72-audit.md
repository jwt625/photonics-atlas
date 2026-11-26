---
title: Fresh-context audit of the lit author-affiliation batch lit_h72 (29 papers)
date: 2026-11-26
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; checker run only in dry-run or write-run on scratch copies with logs in the scratchpad; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h72/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D352, D354, D361, D366, D369, D416, D426, D442, D461, D466 and earlier lit rulings; D249, D285, D287, D288, D301, D302 from DevLog-008; format from the lit_h70 audit
verdict: GO with F1; 232 slots audited, 231 recorded + 1 no_header (siew2021 #7, D369, correct); 0 wrong rows; 4 imprecise slots (kopp2010 #1-#4, F1: printed LETI dropped); all 9 named extractor call groups confirmed except the LETI drop in call 2
---

# Lit header batch audit: lit_h72 (2026-11-26)

## Scope

Batch lit_h72: 29 papers (IEEE journal footnote statements for 26, one IEEE Photonics Journal cover-page paper, one
conference paper with symbol markers, one Communications Magazine byline, one Electronics Letters end-of-letter
block); 232 slots, 3 papers `slots_from_header` (smit1996, selvaraja2009, selvaraja2009a); 271 rows. Restricted corpus:
this record names only authors, orgs, units, cities and countries; no paper text is quoted and no contact, street,
building, site, box or postal text is copied (such spans are named by type only).

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h72 --corpus lit --codes <id> --pdf`
  (all 29; plus `--pages 2` for subramanian2013 and yariv2000); output kept in the session scratchpad
  `h72_audit/show/` only. `show` wrote no log under `logs/`.
- Per slot: printed name vs the `show` author list (or the header order for the 3 header-slot papers) and
  `compare.csv`; statement subjects (every name, "are / is / was / were with", "now with", "and also with"); block
  fields (org, unit chain, more_orgs, campus, city, country); role; locator; notes. Committed lit batches grepped for
  each form question (UCSB / UCLA / UC Davis campus, CEA / Leti / LETI / MINATEC, IME / A*STAR, Tyndall / UCC,
  Ghent University-IMEC dash forms, Center for Nano- and Biophotonics, Peter O’Brien explicit slots, glued words,
  Hanscom AFB); registry `organizations.csv` / `org_aliases.csv` for org_cea / org_cea_leti.
- All 271 rows of `header_rows.csv` read by paper: roles primary 250, additional 11, present address 10; basis prose
  239, printed 29, single 3; all grade A. `compare.csv`: 231 `recorded`, 1 `no_header` (siew2021 #7); `order_differs`
  true only on martin2018 (14 slots).
- Address / contact scan of `headers.yaml` and every derived file (contact sign, URL, 3+-digit numbers, street, road,
  avenue, drive, suite, building, room, hall, box, cedex, e-mail / mail, phone, fax, postal, UMR numbers, and the
  site / county tokens printed in this batch's blocks). Hits: the file comment; decision ids in notes (D352, D369);
  "Hallemeier" (name); type words in notes ("postal code(s)", "postal designation", "UMR number", "a campus name",
  "a county", "state(s)", "province(s)"); the second place Paris in the duan2014 note (D288 second place to the note);
  campus field values (D301); locality "Hanscom AFB" (printed place, committed lit AFRL/SNHC form). No contact, URL,
  postal code, street, building, box or site text anywhere, notes included.
- Probes on scratch copies (`h72_audit/probes/probe.py` + `mk.py`, scratch `LIT_BASE`, batch name `lit_p72`,
  `cmd_check(..., dry_run=True)`, `RunLog` redirected to the scratchpad; 37 runs: 35 variants, the base write run and
  the F1 write run). Run of the batch as written: 0 errors, 4 warnings (explicit slots martin2018 #11 #12, snyder2013
  #2; martin2018 order); scratch write-run derived files byte-identical to the stamped `header_rows.csv`,
  `compare.csv`, `unmapped_orgs.csv`, `check_stamp.txt`. md5 of every repo batch file identical before and after the
  audit; `check_stamp.txt` matches `headers.yaml` (sha256 effd9c58...).

## Counts

| batch | papers audited / total | slots audited | ok | gap (correct handling, no row) | imprecise | wrong |
|---|---|---|---|---|---|---|
| lit_h72 | 29 / 29 | 232 | 227 | 1 | 4 | 0 |

- Papers ok 29, partial 0, unreadable 0; `slots_from_header` 3 (exactly the papers.csv rows with `n_authors_meta` 0,
  each prints the D352 line in `show`); `author_list_differs` 1 (siew2021); explicit slots 4 (martin2018 #11 #12,
  snyder2013 #2, siew2021 slot 0); order warnings 1 (martin2018); present addresses 10 (komljenovic2018 #5, sacher2018
  #1 #6 #12, pfeiffer2018a #2 #4 #5 #6, heck2012 #6 #8); clause blocks 2 (rahim2018 P2, lim2014 P3); dropped markers 0;
  unreadable authors 0; 24 unmapped org strings (25 after F1).
- Gap slot (1): siew2021 #7 (Shangran Xie): printed S. W. Xie carries an initial the list name does not explain (D369),
  slot 0 + `author_list_differs`; the header author gets no row, the list slot is `no_header`. Imprecise (4): kopp2010
  #1-#4 (F1).
- Per paper (slots / rows): komljenovic2015a 10 / 10; duan2014 23 / 23; komljenovic2018 6 / 7; martin2018 14 / 14;
  blumenthal2018 5 / 5; sacher2018 13 / 16; pfeiffer2018a 7 / 11; masood2013 8 / 8; rahim2018 4 / 8; jalali2006 2 / 2;
  rahim2016 20 / 37; subramanian2013 15 / 21; heck2012 9 / 11; siew2021 13 / 12; lim2014 9 / 10; vlasov2012 1 / 1;
  wooten2000 11 / 11; yariv2000 1 / 1; kopp2010 9 / 10 (14 after F1); tsuchizawa2005 10 / 10; laere2007a 9 / 9;
  taillaert2003 6 / 6; soref2006 1 / 1; sacher2015 4 / 4; snyder2013 2 / 2; bakir2010 7 / 8; smit1996 2 / 2;
  selvaraja2009 5 / 5; selvaraja2009a 6 / 6.
- Privacy findings: 0. Notes: 28 correct, 1 to reword with F1 (kopp2010).

### Per-slot field counts

| field | ok | gap | imprecise | wrong |
|---|---|---|---|---|
| name / slot (232) | 231 | 1 (siew2021 #7, D369) | 0 | 0 |
| markers (prose / printed / single, 232) | 232 | 0 | 0 | 0 |
| header position / order | 232 | 0 | 0 | 0 |
| blocks (org / unit / more_orgs / campus / locality / country) (271 rows) | 267 | 0 | 4 (kopp2010 P1, LETI not recorded) | 0 |
| roles (primary / additional / present address) | 271 | 0 | 0 | 0 |
| locators | all | 0 | 0 | 0 |
| notes (29) | 28 | 0 | 1 (F1) | 0 |

## Per-paper findings

- komljenovic2015a (10; prose, "The authors are with"): call 7. UCSB printed without a comma -> org University of
  California + campus Santa Barbara, Santa Barbara, US (state and postal code not recorded). List forms
  Komljenović / Michael L. / Jared C. / John Edward matched by name. ok.
- duan2014 (23; prose, 5 statements): calls 5, 9. III-V Lab, Palaiseau (first place; postal designation dropped,
  Paris in the note), FR; CEA/Leti, Grenoble, FR (the repeated LETI and the campus name after it not recorded; probe D1
  unit LETI 0 errors, rows unchanged, neutral); Bell Laboratories with the department printed after the org, Nozay,
  FR; Ghent University-IMEC with unit "Photonic Research Group, INTEC" (singular as printed), Ghent, BE; University of
  Southampton ORC, Southampton, "U.K." -> GB. Statement 1 abbreviates author 3 as A. L. Liepvre (subject check passes).
  "Graham. T. Reed" recorded without the stray period (D282). ok.
- komljenovic2018 (6; prose, capitals): UCSB "at Santa Barbara" -> campus form; #5 "was with" UCSB (P2) + "He is now
  with" Ayar Labs, Inc., Emeryville, US (present address P3). Probe K18 (Davenport on P1) 5 errors. ok.
- martin2018 (14; prose): calls 3, 6, 9. Thales Research and Technology, Palaiseau, FR; Tyndall National Institute,
  Cork, IE (UCC parent not copied, D442 palmer2026); Ghent University-IMEC, Ghent; IMEC-Leuven as printed, Leuven; BE.
  Explicit slots #11 (printed Peter O’Brien, curly apostrophe vs list Peter A. O'Brien; probe M1 without: 2 errors;
  committed form in lit_h06 / h13 / h44 / h54) and #12 (Spuessens vs list Spuesens, list misspelling, D287; probe M2:
  2 errors). The author list order is scrambled (Verheyen, De Heyn, Absil, Feneyrou, Bourderionnet in slots 2-6);
  slots by name, YAML in printed order, order warning expected (D363). ok.
- blumenthal2018 (5; prose, capitals): call 7 (UCSB printed with an en dash), ECE unit printed before the org, US;
  LioniX International BV, Enschede, NL (postal code not recorded). ok.
- sacher2018 (13; prose, capitals): call 3. #1 "was with" Toronto ECE (P1) + "He is now with" Caltech Division of
  Physics, Mathematics, and Astronomy, Pasadena (P2); Toronto ECE again for 4 authors (P3, own statement); "A*STAR
  Institute of Microelectronics" printed as the name (no ", A*STAR" parent after it), Singapore, SG for #3 #7 (P4) and
  #6 #12 "were with" (P5) + "They are now with" Advanced Micro Foundry, Singapore (P6); Huawei Technologies Canada Co.
  Ltd., Kanata, CA (P7). Two statements naming the same org are two blocks (contract). Probe SA1 (Luo on P4) 12
  errors. ok.
- pfeiffer2018a (7; prose): "Swiss Federal Institute of Technology", Lausanne, CH (P1); #2 was with / now with TRUMPF
  Scientific Lasers, Unterföhring, DE (P2 / P3); #4-#6 were with / now with Ligentec SA, Lausanne, CH (P4 / P5).
  Probe PF1 (Morais without P5) 2 errors. ok.
- masood2013 (8; printed symbol markers, both layers agree): block ∗ "Ghent University - imec" (dash-joined, D426)
  with unit Photonics Research Group printed before it; the department and the Center of Nano- and Biophotonics
  printed after the org are not recorded: the lit_h19 iseghem2022 form for the same printed chain (department after
  the org not contiguous, D442 gap). Probes MA1 (center as a plain `more_orgs`) 0 errors, +3 rows, +1 unmapped and
  MA2 (unit = department) 0 errors: both pass, neither is required; the org ids (Ghent University + imec via alias)
  are already on the rows (O2). Block † IMEC vzw, Leuven, BE. Probe MS1 (Masood on †) 2 errors. ok.
- rahim2018 (4; prose, capitals): call 3. "Ghent University/imec" kept as printed, unit chain group + department,
  Ghent; "and also with" clause P2 Ghent University + Center for Nano- and Biophotonics, Ghent (D366). ok.
- jalali2006 (2; prose): call 7. "University of California, Los Angeles" -> org University of California + campus Los
  Angeles, locality Los Angeles (the place printed once serves both, as the committed UC Davis blocks), EE unit, US.
  Probe J1 (whole string) 0 errors, neutral. ok.
- rahim2016 (20; prose): call 1. ok (see calls). Statement 2 (Helin, Severi, Rottenberg) is one word per line in both
  layers and verifies: IMEC, Leuven, BE.
- subramanian2013 (15; printed, cover page): page 1 is the cover (unmarked names); the marked author line and the three
  blocks are on text.md page 2 (locator p.2 header, D366). Markers printed with semicolons; 1,2 / 3 / 1,2 / 3 / 3 / 3 /
  1,2 / 1,2,3 / 3 x5 / 1,2 / 3 read in both layers. Ghent University-IMEC Photonics Research Group, Ghent; Ghent
  University "Centre for Nano- and Biophotonics" (British spelling as printed), Ghent; IMEC, Leuven; BE. Probe SU1
  (Selvaraja without 3) 2 errors. ok.
- heck2012 (9; prose): call 7. P1 UCSB, US; #6 and #8 "was with" UCSB printed with the state only, no country: country
  "" (D249; probe H1 country US: 2 errors) and "He is now with" HP Labs, Palo Alto, US / OneChip Photonics, Inc.,
  Ottawa, CA. ok.
- siew2021 (13; prose): call 9. Advanced Micro Foundry Pte Ltd, Singapore, SG. #7 S. W. Xie: slot 0 required (probe
  SW1 without: 1 error, 0 compatible slots); explicit slot 7 would pass the checker (SW2, 0 errors) but D369 forbids a
  match with a disagreeing initial. List forms Shawn Yohanes / Feng / Han Yue / Bin / Xianshu / G. Q. Lo matched by
  name. ok (#7 gap).
- lim2014 (9; prose): calls 4, 6. Institute of Microelectronics, Singapore, SG (", A*STAR" parent not copied; probe L2
  with A*STAR as more_orgs passes, +8 rows: not the rule); #2 own statement P2 + "and also with" clause P3 Jilin
  University with the key laboratory + college chain, Changchun, CN. "StateKey" written "State Key" (D282 intended
  letters; probe L1 glued form 0 errors, neutral). Probe LI1 (Song without P3) 3 errors. ok.
- vlasov2012 (1; single): byline "name, IBM T. J. Watson Research Center" at the end of the page 1 extraction; no city
  or country printed: locality / country "" (D288 / D249). ok.
- wooten2000 (11; prose): JDS Uniphase Corp., Bloomfield, US (state and postal code not recorded). List forms
  D. Lafaw / P. Hallemeier / David R. Maack matched by name. ok.
- yariv2000 (1; single): call 8. Author line on page 1, block in parentheses after the name at the end of the letter on
  text.md page 2 (locator p.2 affiliations): California Institute of Technology, Pasadena (state not recorded), US.
  Probe Y1 (name Avigail Yariv) 2 errors: the printed "A. Yariv" is the only valid record. ok (O3 for the list name).
- kopp2010 (9; prose): call 2 imprecise (F1). P2 Institut des Nanotechnologies de Lyon (UMR number not copied) +
  Institut National des Sciences Appliquées de Lyon in `more_orgs` (D285 joint-unit form), Villeurbanne, FR;
  Austriamicrosystems AG, Unterpremstaetten, AT; Photline Technologies, Besançon, FR; TU Berlin with the
  Fachgebiet printed before it (P5) and without unit (P6), Berlin, DE (spelling Technische Universitaet as printed).
- tsuchizawa2005 (10; prose): NTT Microsystem Integration Laboratories, Atsugi (as printed; postal code not recorded),
  JP. List forms T. Watanabe / Junichi / M. Takahashi matched by name. ok.
- laere2007a (9; prose): Ghent University-IMEC with "Department of Information Technology (INTEC)", Ghent, BE;
  University of St. Andrews School of Physics and Astronomy, St. Andrews, "U.K." -> GB (county and postal code not
  recorded). Probe LA1 (O’Faolain on P1) 5 errors. ok.
- taillaert2003 (6; prose): "Ghent University—IMEC" (em dash, kept, D426), INTEC unit, Gent, BE; Glasgow University
  EE, Glasgow, GB (postal code before the city not recorded); Technical University of Denmark, Research Center COM
  printed before it, Kgs. Lyngby, DK. ok.
- soref2006 (1; single, p.1 footnote): call 9. "The author is with" is not read as naming the author (probe SO1 as
  prose: 2 errors), so `single` with the footnote locator is right (lit_h46 / lit_h64). Air Force Research Laboratory
  with the directorate printed after the org, Hanscom AFB (as printed), US. ok.
- sacher2015 (4; prose): call 6. Toronto ECE, no city printed (province only): locality "" (probe S15 Toronto 0
  errors: known city-inside-org gap); Institute of Microelectronics, Singapore, SG (the written-out A*STAR parent not
  copied). ok.
- snyder2013 (2; prose): call 6. Tyndall National Institute, Cork, IE (UCC parent not copied). #2 explicit slot required
  for the curly apostrophe (probe SN1 without: 2 errors; SN2 straight apostrophe without slot: 0 errors, equivalent;
  committed curly + slot form kept). ok.
- bakir2010 (7; prose): calls 4, 5, 9. P1 "CEA-Léti" with the campus name glued after it (not recorded) and the
  Technological Research Department after that, Grenoble, FR; statement 1 abbreviates #2 as A. V. de Gyves. P2
  "Institut des Nanotechnolgies de Lyon" misspelt in both layers, kept (probe BK2 corrected spelling: 4 errors), +
  INSA-Lyon in `more_orgs`, no city printed (locality ""; probe BK1 Lyon 0 errors, known gap), FR. ok.
- smit1996 (2; prose, slots from header): Delft University of Technology, Delft, NL (postal code not recorded).
  Printed order = YAML (probe SH1, authors swapped: 0 errors, O1). ok.
- selvaraja2009 (5; prose, slots from header): call 3 family; "Ghent University–Interuniversity Microelectronics Centre
  (IMEC)" (en dash, acronym as printed, D426), Department of Information Technology printed before it, Ghent, BE.
  Printed order = YAML. ok.
- selvaraja2009a (6; prose, slots from header): call 3. "Gent University-IMEC" with INTEC unit, Gent; #2 "IMEC-
  Interuniversitair Micro Electronica Centrum" as printed, Leuven; BE. Printed order = YAML. ok.

## Extractor calls (verified)

1. rahim2016 P1. The statement prints the group + department, then IMEC, then the center, then Ghent University. The
   only contiguous unit-org segment is the group + department chain + IMEC: the committed bayoumi2025 form (org Ghent
   University + unit chain + `more_orgs` imec, D466) fails here (probe R1: 2 errors, the center between unit and Ghent
   University exceeds the D246 gap), as does R4 (Ghent University + IMEC + structured center: 2 errors). R2 (Ghent
   University as a plain string) 0 errors but loses the center unit; R3 (no `more_orgs`) loses Ghent University (rows
   37 -> 20); R5 (structured `more_orgs` without place) 0 errors, rows unchanged, neutral. The extractor's form keeps
   every printed org and unit and is the only full record that passes. Confirmed; the unit chain is attached to IMEC
   by print order (O2).
2. kopp2010 P1. Org "Commissariat à l'Energie Atomique" with unit DOPT/STM (printed before the org, contiguous):
   confirmed; the unit cannot be LETI instead (probe K2: 4 errors, the first field after the verb must be recorded).
   The MINATEC institute name after LETI is a site name and stays out (lit_h05 aamer2012 note, h70 duprez2016).
   Dropping LETI is not confirmed: LETI is printed directly after the org in the same statement; the committed lit
   forms always record it when printed (aamer2012: CEA + unit LETI written out; 25 committed blocks carry LETI / Leti as
   the CEA unit, mostly in structured `more_orgs` as in h70 duprez2016; 20 CEA-Leti / CEA-LETI / CEA LETI org
   strings), the registry holds it as its own org (org_cea_leti, parent
   org_cea), and the same authors (Fedeli, Ben Bakir) map to org_cea_leti in duan2014 / bakir2010 of this batch. With
   the unit field taken by DOPT/STM, the recordable form is a plain `more_orgs` string (probe K1: 0 errors, +4 rows,
   +1 unmapped; K3 with the site name too: 0 errors, not wanted). -> F1.
3. Names kept as printed: martin2018 "IMEC-Leuven", selvaraja2009a "Gent University-IMEC" and "IMEC-Interuniversitair
   Micro Electronica Centrum", rahim2018 "Ghent University/imec", sacher2018 "A*STAR Institute of Microelectronics"
   (2 committed blocks of this exact string), plus masood2013 "Ghent University - imec", taillaert2003 "Ghent
   University—IMEC", selvaraja2009 "Ghent University–Interuniversity Microelectronics Centre (IMEC)": D426 / D416 (5)
   dash-joined and as-printed forms; aliases in the org round. Confirmed.
4. bakir2010 "Nanotechnolgies" kept (both layers; correction fails, BK2) and lim2014 "StateKey" written "State Key"
   (D282; both forms pass). Confirmed.
5. Campus / site names after CEA/Leti not recorded (duan2014 P2, bakir2010 P1): committed practice for campus and site
   names (aamer2012, lit_h21 and others); D1 neutral. Confirmed.
6. Parents dropped: A*STAR after IME (lim2014 P1 / P2, sacher2015 P2 written out) and University College Cork after
   Tyndall (martin2018 P2, snyder2013 P1): contract parent rule, 44 committed IME blocks and 25 Tyndall blocks, D442
   palmer2026. Confirmed.
7. UCSB / UCLA as org University of California + campus (komljenovic2015a, komljenovic2018 P1 P2, blumenthal2018,
   heck2012 P1 P2 P4, jalali2006): D301 and the committed UCSB form (h70 call 6, D461); KO1 / J1 whole strings 0
   errors (neutral). Confirmed.
8. yariv2000 printed "A. Yariv" vs list given name Avigail: matched by initial, printed form required (Y1). Confirmed;
   list name to O3.
9. Units printed after the org (soref2006, duan2014 P3, bakir2010 P1) are contiguous with the org and recordable (D461,
   not the iseghem2022 gap): confirmed. siew2021 `author_list_differs` with S. W. Xie slot 0 (D369, SW1 / SW2):
   confirmed. martin2018 order warning (D363): confirmed. `slots_from_header` on smit1996 / selvaraja2009 /
   selvaraja2009a: exactly the 3 papers with no author list (`n_authors_meta` 0): confirmed. siew2021 #7 `no_header`:
   confirmed.

## Fixes (exact YAML edits)

F1 (kopp2010, imprecise: 4 slots #1 Kopp, #2 Bernabé, #3 Ben Bakir, #4 Fedeli; printed LETI not recorded). In
`data/_staging/people/lit_headers/lit_h72/headers.yaml`:

Line 337, replace

```
    - {marker: "P1", basis: prose, org: "Commissariat à l'Energie Atomique", unit: "DOPT/STM", locality: "Grenoble", country: "FR", locator: "p.1 footnote"}
```

with

```
    - {marker: "P1", basis: prose, org: "Commissariat à l'Energie Atomique", unit: "DOPT/STM", more_orgs: ["Laboratoire d'Electronique et de Technologies de l'Information"], locality: "Grenoble", country: "FR", locator: "p.1 footnote"}
```

Line 335 (note), replace

```
then the Laboratoire d'Electronique et de Technologies de l'Information and an institute name after it (not recorded);
```

with

```
then the Laboratoire d'Electronique et de Technologies de l'Information (a second organization, more_orgs: the unit field holds DOPT/STM, lit_h05 aamer2012 records LETI) and an institute name after it (site name, not recorded);
```

Probe of the batch with F1 applied (both edits): 0 errors, 4 warnings (unchanged), rows 271 -> 275 (kopp2010 10 -> 14),
unmapped strings 24 -> 25 (the LETI string, 4 rows). After applying, re-run `uv run python scripts/ofc_headers.py check
lit_h72 --corpus lit` (stamp and derived files change). Org round: alias "Laboratoire d'Electronique et de
Technologies de l'Information" -> org_cea_leti (the registry alias reads "des technologies", not exact); "Commissariat
à l'Energie Atomique" -> org_cea (as for the lit_h05 aamer2012 request).

No other fix: no slot, marker, block field, role, locator or other note is wrong.

## Observations (no YAML change)

- O1 Header-slot order gap reconfirmed (h70 O2, D756): smit1996 authors swapped pass (SH1, prose basis); the 3
  header-slot papers were checked by reading.
- O2 Form notes for the people / org round: rahim2016 P1 puts the Photonics Research Group / Department of
  Information Technology chain on IMEC by print order, while committed Ghent blocks put this chain on Ghent University;
  the row set (IMEC + Ghent University) is right, only the unit owner differs. masood2013 block ∗ drops the department
  and the Center of Nano- and Biophotonics printed after the org (iseghem2022 form; MA1 shows the center could be added
  as a plain `more_orgs`, the org ids are unaffected). Both stay as written.
- O3 yariv2000 list name: the author list gives "Avigail Yariv"; the paper prints only "A. Yariv" (California Institute
  of Technology, Pasadena). The local corpus (santis2014, a Caltech paper) prints "Amnon Yariv"; the list given name is
  probably a metadata error. Candidate for the D412 author-list correction file; the YAML is correct.
- O4 Known gaps reconfirmed: city inside the org name accepted as locality (S15 Toronto, BK1 Lyon); campus removal
  accepted (KO1); plain vs structured `more_orgs` without place equivalent (R5); a straight apostrophe makes the
  O’Brien explicit slots unnecessary (SN2), the committed curly + slot form is kept.

## Lists for the coordinator

- D412 list: yariv2000 #1 (list Avigail Yariv; printed A. Yariv; O3).
- D426 review list: martin2018 #11 and snyder2013 #2 (Peter O’Brien / Peter A. O'Brien, explicit slots), martin2018
  #12 (Spuessens / Spuesens, explicit slot); siew2021 #7 (S. W. Xie / Shangran Xie, slot 0, D369).
- Re-record list: none.
- Org round (24 unmapped strings as written, 25 after F1): Air Force Research Laboratory; Austriamicrosystems AG; Bell
  Laboratories; Commissariat à l'Energie Atomique; Gent University-IMEC; Ghent University–Interuniversity
  Microelectronics Centre (IMEC); Ghent University—IMEC; Glasgow University; HP Labs; IMEC-Interuniversitair Micro
  Electronica Centrum; IMEC-Leuven; INSA-Lyon; Institut National des Sciences Appliquées de Lyon; Institut des
  Nanotechnolgies de Lyon (misprint); Institut des Nanotechnologies de Lyon; NTT Microsystem Integration Laboratories;
  OneChip Photonics, Inc.; Photline Technologies; Swiss Federal Institute of Technology; TRUMPF Scientific Lasers;
  Technische Universitaet Berlin (2 unit forms); Thales Research and Technology; University of St. Andrews; after F1
  Laboratoire d'Electronique et de Technologies de l'Information.

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 4 warnings, 271 rows, 24 unmapped; derived files identical | batch as written |
| R1 / R4 | rahim2016 P1 org Ghent University + unit chain + IMEC (+ structured center) | 2 / 2 errors | not contiguous; extractor form needed |
| R2 / R3 / R5 | Ghent University plain / no more_orgs / structured without place | 0 / 0 (37 -> 20 rows) / 0 errors | lose center / lose Ghent / neutral |
| K1 / K3 | kopp2010 P1 + LETI more_orgs / + LETI and site name | 0 (+4 rows, +1 unmapped) / 0 (+8) errors | F1 form / site name not wanted |
| K2 | kopp2010 unit LETI instead of DOPT/STM | 4 errors | DOPT/STM must be the unit |
| FIX | K1 + note rewording | 0 errors, 4 warnings, 275 rows, 25 unmapped | F1 safe |
| M1 / M2 / SN1 / SN2 | explicit slots removed / snyder2013 straight apostrophe | 2 / 2 / 2 / 0 errors | slots required for the curly form |
| SW1 / SW2 | siew2021 slot 0 removed / slot 7 | 1 / 0 errors | slot 0 required; slot 7 barred by D369 |
| H1 | heck2012 P2 country US | 2 errors | country not printed |
| MA1 / MA2 / MS1 | masood2013 center more_orgs / unit department / Masood on † | 0 (+3 rows) / 0 / 2 errors | optional (O2) / neutral / markers verified |
| L1 / L2 / LI1 | lim2014 StateKey / A*STAR more_orgs / Song without P3 | 0 / 0 (+8 rows) / 3 errors | neutral / parent rule / clause verified |
| S15 / BK1 | sacher2015 locality Toronto / bakir2010 locality Lyon | 0 / 0 errors | known gap (O4) |
| BK2 | bakir2010 corrected spelling | 4 errors | misprint kept |
| SO1 | soref2006 as prose P1 | 2 errors | single required |
| KO1 / J1 / D1 | whole UCSB string / whole UCLA string / duan2014 unit LETI | 0 / 0 / 0 errors | neutral |
| SH1 | smit1996 authors swapped | 0 errors | O1 |
| Y1 | yariv2000 name Avigail Yariv | 2 errors | printed form required |
| SU1 / K18 / SA1 / PF1 / LA1 | marker / statement variants | 2 / 5 / 12 / 2 / 5 errors | verified |
