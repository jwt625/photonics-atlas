---
title: Fresh-context audit of the lit author-affiliation batch lit_h75 (23 papers)
date: 2026-11-28
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; checker run only as dry runs or write runs on scratch copies with logs in the scratchpad; aggregate and the people build not run; no network; one read-only `git status` call, nothing else in git)
scope: data/_staging/people/lit_headers/lit_h75/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D352, D353, D366, D369, D380, D412, D416, D426, D442, D466, D629, D742 and earlier lit rulings; D173, D240, D244, D249, D285, D286, D287, D288, D301, D302 from DevLog-008; format from the lit_h73 / lit_h74 audits
verdict: GO with F1 and F2 (note wording only, no row change); 157 slots audited, 154 recorded + 3 no_header (ludlow2015 #1-#3 unreadable, correct); 0 wrong rows; 0 imprecise rows; 2 imprecise notes (xiong2012, zhuang2015); every named extractor call confirmed
---

# Lit header batch audit: lit_h75 (2026-11-28)

## Scope

Batch lit_h75: 23 papers (Optica / Optics Express numbered or single blocks for 14, arXiv or preprint headers for 8,
one SPIE-style enhanced abstract (boes2023)); 157 slots, 5 papers `slots_from_header` (kim2015, xiong2012, hulme2013,
ferdous2011, green2007); 171 rows. Restricted corpus: this record names only authors, orgs, units, cities and
countries; no paper text is quoted and no contact, street, building, box or postal text is copied (such spans are
named by type only).

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h75 --corpus lit --codes <id> --pdf`
  (all 23); output kept in the session scratchpad `h75_audit/show/` only. `show` wrote no log under `logs/` (the new
  log files during the audit belong to other streams). rogers2021 page 1 was also rendered to an image (scratchpad,
  deleted after viewing) to confirm that block 3 carries no printed marker on the page. huang2019d / li2012 / lu2021
  asterisk and dagger legends checked in `text.md` (contact lines, later pages for huang2019d and li2012).
- Per slot: printed name vs the `show` author list (or the header order for the 5 header-slot papers) and
  `compare.csv`; markers in both layers; block fields (org, unit chain, more_orgs, campus, city, country); role;
  locator; notes. Committed lit batches grepped for each form question (Fejer name forms, JPL with / without Caltech,
  JILA / Joint Quantum Institute / Renewable and Sustainable Energy Institute joint-institute forms, NIST Time and
  Frequency Division units, `skip_between` entries, University of Illinois / UCLA / University of Maryland campus
  forms, Monash / LioniX / SATRAX forms, `listing_order` use).
- All 171 rows of `header_rows.csv` read by paper: roles primary 154, additional 17, present address 0; basis printed
  134, single 36, listing_order 1 (rogers2021 block 3, grade B); grade A 170, B 1; locators all `p.1 header`;
  match basis name 134, alias 8, ror 6, unmapped 23. `compare.csv`: 154 `recorded`, 3 `no_header`; `order_differs`
  false everywhere. Country empty on 6 rows (boes2023 blocks 1 and 8, carmon2004), each with no printed country.
- Address / contact scan of `headers.yaml` and every derived file (contact sign, URL, mail, phone, fax, box, P.O.,
  street, road, avenue, drive, boulevard, building, room, suite, cedex, county, district, the US state names and
  abbreviations, every 3+-digit number, and every street, box and postal-code token printed in this batch's blocks,
  searched by its printed spelling and not repeated here). Hits: years and decision ids; org names (University of
  California, University of Illinois, University of Oregon, University of Colorado in the ludlow2015 note); the
  author surname MA (guan2018 YANGJIN MA); the author name "P.O. Schmidt" (ludlow2015, a printed initial pair, not a
  box); type words in notes ("street address(es)", "postal code(s)", "postal boxes", "county", "states"); the NIST
  division number in papp2014 `skip_between` only (absent from every derived file). No contact, URL, postal code,
  street, building, box or e-mail text anywhere, notes included.
- Probes on scratch copies (`h75_audit/probes/probe.py` + `variants.py`, scratch `LIT_BASE`, `RunLog` redirected to
  the scratchpad; 44 runs: the base write run, 42 variants, the fix write run). Run of the batch as written: 0
  errors, 1 warning (boes2023 explicit slot 8); scratch write-run derived files byte-identical to the stamped
  `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`, `check_stamp.txt`. md5 of every repo batch file identical
  before and after the audit; `check_stamp.txt` matches `headers.yaml` (sha256 aeac8d18...).

## Counts

| batch | papers audited / total | slots audited | ok | gap (correct handling, no row) | imprecise | wrong |
|---|---|---|---|---|---|---|
| lit_h75 | 23 / 23 | 157 | 154 | 3 | 0 | 0 |

- Papers ok 22, partial 1 (ludlow2015, blocks between two author groups, checker gap), unreadable 0;
  `slots_from_header` 5 (exactly the papers.csv rows with `n_authors_meta` 0, each prints the D352 line in `show`);
  `author_list_differs` 0; explicit slots 1 (boes2023 #8 Martin Fejer); order warnings 0; present addresses 0;
  dropped markers 4 (he2019a #9 / #10 contact lines, guan2018 #1 / #2 equal contribution); unreadable authors 3
  (ludlow2015 #1-#3); 14 unmapped org strings (23 rows).
- Gap slots (3): ludlow2015 #1 Ludlow, #2 Boyd, #3 Ye (blocks 1-3 printed between the two author groups cannot be
  located by the checker; values in the note for the re-record list). Besides, xiong2012 #2 (Pernice) has its
  printed Current address block (KIT Institute of Nanotechnology) unrecorded by rule (D442); the slot itself is
  recorded.
- Per paper (slots / rows): winzer2018 3 / 3; boes2023 10 / 13; luo2017 6 / 8; carmon2004 3 / 3; kim2015 5 / 5;
  xiong2012 3 / 3; lu2021 6 / 6; ludlow2015 5 / 3; tian2020 7 / 7; rogers2021 12 / 12; doylend2011 6 / 6; he2019a
  10 / 11; papp2014 7 / 7; hulme2013 3 / 3; hulme2015 8 / 8; guan2018 14 / 16; suh2018a 15 / 16; huang2019d 8 / 10;
  ferdous2011 8 / 12; cheng2018 5 / 5; green2007 4 / 4; zhuang2015 5 / 6; li2012 4 / 4.
- Privacy findings: 0. Notes: 21 correct, 2 imprecise (xiong2012 F1, zhuang2015 F2: each lists a street address as
  not recorded where none is printed).

### Per-slot field counts

| field | ok | gap | imprecise | wrong |
|---|---|---|---|---|
| name / slot (157) | 154 | 3 (ludlow2015 #1-#3) | 0 | 0 |
| markers (printed / single / listing_order, 154 readable authors) | 154 | 0 | 0 | 0 |
| header position / order | all | 0 | 0 | 0 |
| blocks (org / unit / more_orgs / campus / locality / country) (171 rows) | 171 | 0 | 0 | 0 |
| roles (primary / additional) | 171 | 0 | 0 | 0 |
| locators | all | 0 | 0 | 0 |
| notes (23) | 21 | 0 | 2 (F1, F2) | 0 |

## Per-paper findings

- winzer2018 (3; single, capitals): Nokia Bell Labs, Holmdel, US (street, state, postal code not recorded). List
  forms matched by name. WI1 (name altered) 6 errors. ok.
- boes2023 (10; printed, enhanced abstract): ten blocks read in both layers. RMIT University with the InPAC + School
  of Engineering chain, a state and postal code then Melbourne, no country: country "" (BB1 AU: 2 errors); Peking
  University Department of Electronics, Beijing, CN; University of Adelaide IPAS and EEE school, only a state and
  postal code before Australia: locality "" (BB3 Adelaide passes only through the known city-inside-org gap);
  Stanford Ginzton Laboratory; Harvard SEAS, Cambridge; USC Ming Hsieh ECE, Los Angeles; HyperLight with a street
  address, Cambridge, no country: country "" (BB8 US: 2 errors); Rochester ECE; "University of California, Santa
  Barbara" -> org + campus (D301). Boes 1,3,4 (BM1 without 4: 3 errors); daggers are the equal-contribution legend.
  Martin Fejer vs list "M. M. Fejer": explicit slot 8 (see calls). John Bowers vs John Edward Bowers by name. ok.
- luo2017 (6; printed, capitals): Rochester Institute of Optics / Physics and Astronomy / ECE, SJTU Physics and
  Astronomy, Shanghai, CN. Jiang 1,2 (LO1 without 2: 3 errors). ok.
- carmon2004 (3; single): Caltech Applied Physics, Pasadena; the block prints a state and postal code, no country:
  country "" (CA1 US: 2 errors). ok.
- kim2015 (5; printed, slots from header): "University of Illinois at Urbana-Champaign" kept whole with unit
  Mechanical Science and Engineering, Urbana, US (9 committed blocks of this whole form, mapped; KI2 campus split
  0 errors, neutral); University of Oregon Physics, Eugene, US. Header order verified (KI1 swap: 4 errors). ok.
- xiong2012 (3; printed marker 1 on a single block, D285, slots from header): Yale EE, New Haven, US. Pernice's
  dagger points to a Current address block (KIT Institute of Nanotechnology, Eggenstein-Leopoldshafen, DE), not
  recordable (D442; XI1 as present address and XI2 as regular block: 2 errors each, marker + cue + first field
  fails); the dagger is a symbol no block uses, so no `dropped_markers` entry. Header order verified (XI3: 2 errors).
  Note lists a street address as not recorded; none is printed (F1). ok.
- lu2021 (6; printed, arXiv): Yale EE, New Haven, US; USTC Department of Optics, Hefei, "P. R. China" -> CN. Zou on 2
  (LU21 on 1: 3 errors). ok.
- ludlow2015 (5; partial, arXiv): two author groups, each followed by its own marked blocks (Ludlow / Boyd / Ye with
  blocks 1-3; Peik / Schmidt with blocks 4-5). Blocks 4 PTB, Braunschweig, DE and 5 Leibniz Universität Hannover with
  the Institut für Quantenoptik printed before it (unit), Hannover, DE (LU3 without unit: 2 errors). Schmidt 4,5
  (LU2 without 5: 1 error). Authors 1-3 unreadable: see calls. Note block values agree with the page. partial
  confirmed.
- tian2020 (7; printed, arXiv): Purdue OxideMEMS Lab, West Lafayette, US (postal code printed before the city);
  "Swiss Federal Institute of Technology Lausanne (EPFL)" with Institute of Physics, Lausanne, CH. Daggers point to
  the contact line. J Connor Skehan vs J. Connor Skehan by name. TI1 (Dong on 2) 2 errors. ok.
- rogers2021 (12; printed + listing_order, arXiv): Pointcloud Inc, San Francisco, US; Southampton ORC with a street
  before the city, Southampton, GB ("UK"); block 3 Opris Consulting, San Jose, US printed without a marker on the
  page (render checked) and in both layers: see calls. Asterisks equal contribution, dagger the contact line. ok.
- doylend2011 (6; single): "University of California, Santa Barbara" -> org + campus, unit "Dept. of Electrical and
  Computer Engineering" as printed, US. List forms matched by name. ok.
- he2019a (10; printed, capitals): Rochester ECE, Caltech T.J. Watson Laboratory (unit as printed without the space),
  Rochester Institute of Optics. Vahala 2,4 and Lin 1,3,5: markers 4 / 5 are the two contact lines, dropped (HE1
  without the drop: 2 errors; HE2 on the last author 0 errors, the known last-author prefix gap, lit_h73 O1). ok.
- papp2014 (7; printed, capitals): block 1 NIST with unit Time and Frequency Division, the division number in
  `skip_between` (see calls), Boulder, US; Caltech T. J. Watson Laboratory, Pasadena, US. ok.
- hulme2013 (3; single, slots from header): "University of California Santa Barbara" without a comma -> org + campus,
  unit "Electrical & Computer Engineering Department", US. Header order verified (HU1 swap: 2 errors). ok.
- hulme2015 (8; single): same block, printed without a comma between department and university (unit then org,
  contiguous). List forms (Jared C., Martijn J. R., Michael L., Jock T.) matched by name. ok.
- guan2018 (14; printed, capitals): Columbia EE, New York, US; Elenion Technologies, New York, US (committed form
  twice). Guan / Novack 1,2,3 with 3 = equal-contribution line, dropped (GU1 without: 2 errors). FATHOLOLOUMI split
  across lines verifies. ok.
- suh2018a (15; printed, arXiv): Caltech T. J. Watson Laboratory; JPL without the Caltech parent; NIST with a street
  address, Boulder; "University of California Los Angeles" -> org + campus (2 committed blocks; SU4 whole string 0
  errors, neutral); W.M. Keck Observatory, Kamuela; Caltech Astronomy; NASA Exoplanet Science Institute as a Caltech
  unit. Mawet printed 6,2 with a space before the run: recorded in printed order (SU3 2,6: 2 errors). D. Mawet vs
  Dimitri P. Mawet by name. ok.
- huang2019d (8; printed, arXiv): "École Polytechnique Fédérale de Lausanne" with detached accents folded (D282),
  IPHYS unit, Lausanne, CH; M.V. Lomonosov Moscow State University Faculty of Physics, Moscow, RU; Russian Quantum
  Centre, Skolkovo, RU (postal code printed before the place). Asterisk / dagger point to contact lines on the last
  page. HG1 (Lihachev without 3) 2 errors. ok.
- ferdous2011 (8; printed, slots from header): Purdue ECE Department and Birck Nanotechnology Center (street
  addresses not recorded), West Lafayette; NIST CNST (street not recorded), Gaithersburg; "University of Maryland,
  College Park" -> org + campus with unit Maryland Nanocenter (21 committed campus blocks; FE3 without campus 0
  errors, neutral but against D301); US. Header order verified (FE1 swap: 4 errors); Miao 2,3 (FE2 without 3: 3
  errors). ok.
- cheng2018 (5; single, capitals): Columbia Lightwave Research Laboratory + EE chain, New York, US. Madeleine Glick vs
  Madeleine Strom Glick, KEREN BERGMAN vs K. Bergman by name. ok.
- green2007 (4; single, slots from header): IBM Thomas J. Watson Research Center, Yorktown Heights, US; the web
  address line not recorded and not copied. Header order verified (GR1 swap: 4 errors; GR2 extra name: 2 errors). ok.
- zhuang2015 (5; printed, capitals): Monash Electro-Photonics Laboratory + ECSE chain (3 committed blocks of this
  exact form), Clayton, AU; SATRAX B.V. and LioniX BV (postal boxes and postal codes not recorded), Enschede, NL;
  Twente Laser Physics and Nonlinear Optics group, Enschede, NL; Monash CUDOS, Clayton, AU. Lowery 1,5 (ZH1 without
  5: 1 error). Note lists street addresses as not recorded; none is printed (F2). ok.
- li2012 (4; single, arXiv): Caltech T. J. Watson Laboratory, Pasadena, US. ok.

## Extractor calls (verified)

1. boes2023 "Martin Fejer" explicit slot 8 (list "M. M. Fejer"): confirmed. Distinctive family name, the only
   difference is the missing middle initial (D369 last sentence / D287); same person printed "Martin Fejer" in
   lit_h03 qi2025 and "Martin M. Fejer" in 7 committed batches. BF1 (no slot): 2 errors (0 compatible slots). BF2
   (slot 0 + `author_list_differs`) passes the checker with 0 errors (D302 does not fire because D369 makes the forms
   incompatible), so the choice is enforced by review only; slot 8 is the D369 rule.
2. ludlow2015 `partial` with Ludlow / Boyd / Ye `unreadable` and the block values in the note: confirmed. LU1 (full
   record, blocks 1-3 with JILA + more_orgs, NIST (NIST), AOSense; Ludlow 1,2, Boyd 1,3, Ye 1; status ok): 8 errors
   (blocks 1-3 not found after the author line in both layers; Ye's marker run swallows the blocks before Peik). The
   checker locates blocks only after the last printed author (`analyse`), so this two-group layout is a new checker
   gap (O1). No other basis applies (markers are printed, so `grouped` is barred). Note values and marker sets agree
   with the page.
3. rogers2021 block 3 Opris Consulting `listing_order` grade B: confirmed, with a coordinator question (Q1). The page
   render and both text layers print the block without a marker; it is the only unmarked block, third in order, and
   marker 3 (Opris only) is the only author marker without a printed block, so D173's "blocks 1..N, N = largest author
   marker" precondition holds and the grade B note ("affiliation marker inferred from block order") describes exactly
   this inference. RO2 (`printed`): 2 errors; RO3 (`layout`, unmarked author): 2 errors (Opris prints marker 3).
   Alternative `unreadable` (RO1: Opris unreadable, block 3 dropped, partial) passes with 0 errors but discards a row
   the page supports. The contract text ties `listing_order` to "no local PDF"; here the PDF exists and confirms the
   marker is not printed (not lost), which the checker does not flag for lit (no pdf map in lit runs).
4. papp2014 NIST division number in `skip_between`: confirmed (D742 secretariat-code ruling, D380 entries; verified,
   not stored: the number appears in no derived file). PA1 (no `skip_between`): 2 errors (unit and org not
   contiguous); PA3 (wrong number): 4 errors, so the span is verified token-exactly. PA2 (number kept inside the unit)
   passes with 0 errors (O2): rejected because it would store the number and split the unit from the 9 committed NIST
   "Time and Frequency Division" units.
5. suh2018a JPL without the Caltech parent (D416 (2); lit_h16 / h29 / h45 / h51 form; only lit_h07 ledezma2022 keeps
   Caltech, pre-ruling) and NASA Exoplanet Science Institute as a Caltech unit: confirmed. SU1 (Caltech more_orgs) and
   SU2 (NExScI as org, Caltech dropped) both pass (neutral); NExScI is a Caltech-operated center printed before
   Caltech, the same unit-before-org pattern as the T. J. Watson Laboratory blocks, unlike JPL (separately named
   laboratory with its own registry identity). First committed NExScI block; no precedent conflict.
6. xiong2012 Pernice Current address block not recorded (D442): confirmed (XI1 / XI2). The dagger is a symbol used by
   no block, ignored without a `dropped_markers` entry (contract, D286d); the feldmann2021 numeric-marker form does
   not apply. Values in the note agree with the page and carry no postal code. Goes to the D442 cue list.
7. ludlow2015 JILA as org with National Institute of Standards and Technology / University of Colorado as further
   orgs (note values only): confirmed as the joint-institute form (Joint Quantum Institute with NIST / University of
   Maryland, 3 committed blocks; D629 Renewable and Sustainable Energy Institute with NREL / University of Colorado;
   D466 IMS Laboratory). LU1 shows the fields themselves raise no field-level error; only the position fails.
8. Header-derived slots for kim2015, xiong2012, hulme2013, ferdous2011, green2007: confirmed. Exactly the 5 papers
   with `n_authors_meta` 0; YAML in printed order; a swap of two authors errors on every one (KI1, XI3, HU1, FE1, GR1)
   and an extra name errors (GR2).
9. Campus splits (D301): boes2023 / doylend2011 / hulme2013 / hulme2015 UCSB, suh2018a UCLA, ferdous2011 University
   of Maryland College Park: confirmed; kim2015 University of Illinois at Urbana-Champaign kept whole (committed form,
   mapped).
10. Empty country (boes2023 blocks 1 and 8, carmon2004) and empty locality (boes2023 blocks 3 / 4): confirmed (BB1,
    BB8, CA1; BB3 passes only through the known city-inside-org gap).
11. No street, building, postal code, P.O. box or e-mail anywhere: confirmed (scan above; "P.O. Schmidt" is a name).

## Fixes (exact YAML edits)

F1 (xiong2012 note: no street address is printed in the Yale block or in the unrecorded Current address block). In
`data/_staging/people/lit_headers/lit_h75/headers.yaml`, line 83 (note of `lit:xiong2012`), replace

```
not recorded, the symbol mark is ignored; street address, state and postal codes not recorded
```

with

```
not recorded, the symbol mark is ignored; state and postal codes not recorded
```

F2 (zhuang2015 note: the five blocks print postal boxes, a state and postal codes, but no street address). In
`data/_staging/people/lit_headers/lit_h75/headers.yaml`, line 339 (note of `lit:zhuang2015`), replace

```
blocks 2-4 print The Netherlands; street addresses, states, postal boxes and postal codes not recorded
```

with

```
blocks 2-4 print The Netherlands; states, postal boxes and postal codes not recorded
```

Probe of the batch with F1 and F2 applied (write run on a scratch copy): 0 errors, 1 warning (unchanged);
`header_rows.csv`, `compare.csv`, `unmapped_orgs.csv` byte-identical to the stamped files (171 rows, 14 unmapped
strings); only `check_stamp.txt` changes. After applying, re-run
`uv run python scripts/ofc_headers.py check lit_h75 --corpus lit`.

No other fix: no slot, marker, block field, role, locator or other note is wrong.

## Coordinator question

- Q1 rogers2021 (and lit_h76, which uses the same form for two blocks): accept `listing_order` (grade B) for blocks
  printed without markers on the page itself when a local PDF exists and confirms the absence, provided D173's 1..N
  precondition holds? Recommended yes (amend the contract's "no local PDF" wording to "markers not visible in the
  text, the PDF or the page"); the alternative is `unreadable` authors and no rows (RO1 passes either way).

## Observations (no YAML change)

- O1 New checker gap: marked blocks printed between two author groups (ludlow2015) cannot be located, since blocks are
  searched only after the last printed author. Re-record list: ludlow2015 #1-#3 (values in the note).
- O2 The D244 address scan accepts a bare 3-digit number inside a unit ("Time and Frequency Division" plus the
  division number, PA2: 0 errors); the `skip_between` form is held by review only.
- O3 Known gaps reconfirmed: last author's markers checked as a prefix only (HE2, ZH1, LU2: the run "1,3" without the
  dropped 5 passes); city inside an org name accepted as locality (BB3); empty locality accepted where a city is
  printed (RO5 Southampton ""); slot 0 accepted for a D369-incompatible pair that D287 would match (BF2); campus
  split / whole-string forms both pass (KI2, SU4, FE3).
- O4 "P.O. Schmidt" (ludlow2015 #5) is a printed name; any downstream scan for "P.O." box text should not flag it.

## Lists for the coordinator

- D442 cue list: xiong2012 #2 (Current address, KIT Institute of Nanotechnology, Eggenstein-Leopoldshafen, DE).
- Re-record list: ludlow2015 #1-#3 (two-group header, O1).
- D426 review list: boes2023 #8 (Martin Fejer / M. M. Fejer, explicit slot).
- Org round (14 unmapped strings, 23 rows): Jet Propulsion Laboratory (4 rows); LioniX BV; M.V. Lomonosov Moscow State
  University (Faculty of Physics); Monash University (CUDOS; Electro-Photonics Laboratory chain); Opris Consulting;
  Physikalisch-Technische Bundesanstalt; RMIT University (country empty); Russian Quantum Centre; SATRAX B.V.;
  University of Adelaide (IPAS; EEE school); University of Oregon; W.M. Keck Observatory.

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 1 warning, 171 rows, 14 unmapped; derived files identical | batch as written |
| BF1 / BF2 | boes2023 Fejer slot removed / slot 0 + author_list_differs | 2 / 0 errors | slot required; slot 0 passes, barred by D369 |
| BB1 / BB8 / BB3 / BM1 | block 1 AU / block 8 US / block 3 Adelaide / Boes without 4 | 2 / 2 / 0 / 3 errors | countries not printed; known gap; markers verified |
| LU1 | ludlow2015 full record (blocks 1-3, markers, ok) | 8 errors | blocks between groups not locatable (O1) |
| LU2 / LU3 | Schmidt without 5 / block 5 without unit | 1 / 2 errors | verified |
| RO1 | Opris unreadable, block 3 dropped, partial | 0 errors | valid alternative, loses a supported row |
| RO2 / RO3 | block 3 printed / layout with unmarked Opris | 2 / 2 errors | marker not printed / Opris prints 3 |
| RO4 / RO5 | Opris unreadable with block kept / Southampton locality "" | 0 / 0 errors | neutral / known gap |
| PA1 / PA2 / PA3 | no skip_between / number in unit / wrong number | 2 / 0 / 4 errors | skip span verified; O2 |
| SU1 / SU2 / SU4 | JPL + Caltech / NExScI as org / UCLA whole string | 0 / 0 / 0 errors | neutral |
| SU3 | Mawet 2,6 | 2 errors | printed order verified |
| XI1 / XI2 | Current address block as present address / regular | 2 / 2 errors | D442 handling required |
| XI3 / KI1 / HU1 / FE1 / GR1 | header-slot authors swapped | 2 / 4 / 2 / 4 / 4 errors | header order verified |
| GR2 | green2007 extra author | 2 errors | verified |
| KI2 / FE3 | Illinois campus split / College Park campus removed | 0 / 0 errors | neutral (committed forms kept) |
| FE2 / LO1 / GU1 / HE1 / HG1 / LU21 / TI1 / ZH1 | marker variants | 3 / 3 / 2 / 2 / 2 / 3 / 2 / 1 errors | verified |
| HE2 | Lin without the dropped 5 | 0 errors | last-author prefix gap (O3) |
| CA1 / WI1 | carmon2004 US / Neilson misspelled | 2 / 6 errors | verified |
| FIX | F1 + F2 note rewording | 0 errors, 1 warning, derived CSVs identical | F1 / F2 safe |
