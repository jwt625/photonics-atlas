---
title: Fresh-context audit of the lit author-affiliation batch lit_h76 (23 papers)
date: 2026-11-28
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; checker run only on scratch copies with LIT_BASE and RunLog redirected to the session scratchpad; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h76/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D352, D366, D369, D380, D426, D742, D756, D779 and earlier lit rulings; D249, D285, D287, D288, D301, D302 from DevLog-008; format from the lit_h73 / lit_h74 audits
verdict: GO with F1 (note wording only, no row change); 144 slots audited, 140 recorded + 4 no_header (guo2016b #6 and obrzud2018 #5 not printed, obrzud2018 #4 D369 slot 0, miller2015 #1 unreadable by the brief); 0 wrong rows; 0 imprecise rows; 1 imprecise note (miller2015); 1 coordinator question (Q1, miller2015 skip_between)
---

# Lit header batch audit: lit_h76 (2026-11-28)

## Scope

Batch lit_h76: 23 papers (Optics Express / Optica-style numbered or single blocks for 15, arXiv preprints for 5
(xu2019b, ros2019, herr2014a, guo2016b, obrzud2018), Optica / OSA capitals bylines for 3 (belt2017, michaels2018,
miller2015)); 144 slots (compare.csv), 6 papers `slots_from_header` (dong2010a, maesenovo2013, ikeda2008, zortman2010,
cheben2007, miller2015); 160 rows. Restricted corpus: this record names only authors, orgs, units, cities and
countries; no paper text is quoted and no contact, street, building, park, box or postal text is copied (such spans
are named by type only).

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h76 --corpus lit --codes <id> --pdf`
  (all 23); output kept in the session scratchpad `h76_audit/show/` only. `show` wrote nothing under `logs/` (file
  count 15886 before and after the dumps; the only later additions are two `build_supply_staging` logs of another
  stream). Footnote targets checked in `text.md` without printing contact text: guo2016b (equal contribution and
  correspondence footnotes on the last page), belt2017 (dagger footnote on a later page), papes2016 (the first
  contact line starts with marker 8), xu2019b / ros2019 (page-1 footnotes).
- Per slot: printed name vs the `show` author list (or the header order for the 6 header-slot papers) and
  `compare.csv`; markers in both layers; block fields (org, unit chain, more_orgs, campus, city, country); role;
  locator; notes. Committed lit batches grepped for each form question (UC campus forms incl. "at Berkeley" and
  "University of California Santa Barbara" whole, La Jolla, Ostrava-Poruba, Zijingang, Sun Labs / Oracle, Kotura,
  Lomonosov, MESA+ unit chains, IEF forms, INAF / CSEM / Ligentec, University of Muenster, Cedex wording,
  `skip_between` building names, listing_order).
- All 160 rows of `header_rows.csv` read by paper: roles primary 143, additional 17, present address 0; basis printed
  120, single 33, listing_order 7 (sherwooddroz2008); grade A 153, B 7; locators all `p.1 header`. `compare.csv`: 140
  `recorded`, 4 `no_header`; `order_differs` true only on guo2016b (10 rows).
- Address / contact scan of `headers.yaml` and every derived file (contact sign, URL, 3+-digit numbers, street, road,
  avenue, drive, boulevard, mall, lane, suite, building, bldg, bat, room, hall, box, P.O., cedex, mail, phone, fax,
  postal, park, and every street, building-code, park and campus-site token printed in this batch's blocks, searched
  by its printed spelling and not repeated here). Hits: the file comment ("DevLog-011", "2026"); type words in notes
  ("street address(es)", "postal code(s)", "postal boxes", "a building and site code", "a park and building", "a room
  and building name", "a building number", "a building name", "a technology park", "Cedex dropped" (lit_h09 / lit_h70
  wording), "province", "state(s)"); "lane" inside PlanetS; "Park" inside the city Monterey Park. No contact, URL,
  postal code, street, building, park name, box or e-mail text anywhere, notes included.
- Probes on scratch copies (`h76_audit/probes/probe.py` + `variants.py`, scratch `LIT_BASE`, `RunLog` redirected to
  the scratchpad; 46 runs: 43 variants, the base dry run, the base write run and the F1 write run). Run of the batch
  as written: 0 errors, 4 warnings (explicit slots roeloffzen2013 #6, keraly2013 #1, papes2016 #8; order guo2016b);
  scratch write-run derived files byte-identical to the stamped `header_rows.csv`, `compare.csv`,
  `unmapped_orgs.csv`, `check_stamp.txt`. md5 of every repo batch file identical before and after the audit;
  `check_stamp.txt` matches `headers.yaml` (sha256 2600c882...).

## Counts

| batch | papers audited / total | slots audited | ok | gap (correct handling, no row) | imprecise | wrong |
|---|---|---|---|---|---|---|
| lit_h76 | 23 / 23 | 144 | 140 | 4 | 0 | 0 |

- Papers ok 22, partial 1 (miller2015, building name between unit and org, brief), unreadable 0; `slots_from_header`
  6 (exactly the papers.csv rows with `n_authors_meta` 0, each prints the D352 line in `show`); `author_list_differs`
  2 (guo2016b, obrzud2018); explicit slots 4 (roeloffzen2013 #6, keraly2013 #1, papes2016 #8, obrzud2018 M.H.
  Anderson slot 0); order warnings 1 (guo2016b); present addresses 0; dropped markers 1 (papes2016 #2 contact
  footnote); unreadable authors 1 (miller2015); 27 unmapped org strings (61 rows).
- Gap slots (4): guo2016b #6 (Victor Brasch, not printed in the preprint header); obrzud2018 #4 (list Miles Anderson;
  printed M.H. Anderson, D369 slot 0) and #5 (Junqiu Liu, not printed); miller2015 #1 (block not recorded, Q1).
- Per paper (slots / rows): xu2019b 4 / 6; ros2019 8 / 8; densmore2009 9 / 9; dong2010a 9 / 9; roeloffzen2013 10 /
  11; maesenovo2013 9 / 12; herr2014a 7 / 9; guo2016b 10 / 11; keraly2013 4 / 4; ikeda2008 4 / 4; obrzud2018 17 / 18;
  belt2017 4 / 4; dai2012c 3 / 4; dai2010 4 / 4; dai2011 2 / 3; michaels2018 2 / 2; papes2016 13 / 16; dai2011a 2 / 3;
  zortman2010 3 / 4; chen2012a 2 / 2; cheben2007 10 / 10; sherwooddroz2008 7 / 7; miller2015 1 / 0.
- Privacy findings: 0. Notes: 22 correct, 1 imprecise (miller2015, F1).

### Per-slot field counts

| field | ok | gap | imprecise | wrong |
|---|---|---|---|---|
| name / slot (144) | 140 | 4 (guo2016b #6, obrzud2018 #4 #5, miller2015 #1) | 0 | 0 |
| markers (printed / single / listing_order, 140 printed authors with rows) | 140 | 0 | 0 | 0 |
| header position / order | all | 0 | 0 | 0 |
| blocks (org / unit / more_orgs / campus / locality / country) (160 rows) | 160 | 0 | 0 | 0 |
| roles (primary / additional) | 160 | 0 | 0 | 0 |
| locators | all | 0 | 0 | 0 |
| notes (23) | 22 | 0 | 1 (F1) | 0 |

## Per-paper findings

- xu2019b (4; printed symbols, arXiv): double dagger UW ECE, Seattle; section sign Ningbo University with the
  laboratory + institute chain, Ningbo, CN; double bar Intel Corporation with the division unit, Santa Clara;
  perpendicular sign UW Physics, Seattle; US. Dagger (equal contribution) and asterisk (correspondence) used by no
  block, ignored. Jonathan Doylend vs list Jonathan K. Doylend matched by name. XU1 (Xu without section sign) 3
  errors. ok.
- ros2019 (8; printed, arXiv): Oxford Materials, Oxford, GB; "IBM Research - Zurich" kept (D426), "Ruschlikon" as
  printed (RS2 Rüschlikon 0 errors, folded, neutral), CH; "Institue of Physics" misprint copied as printed (RS1 the
  corrected spelling: 2 errors, the block's first field must be printed), University of Muenster (committed twice),
  Muenster, DE; Exeter Engineering, Exeter, GB. Caret = equal contribution (symbol). C David Wright vs list
  Christopher David Wright, Wolfram H.P. vs H. P. matched by name. ok.
- densmore2009 (9; single): NRC Canada with the IMS unit, Ottawa, CA (province and postal code not recorded).
  DE1 (Delâge / Lapointe swapped) 4 errors. List forms Adam S. / Andre Delage / J. Lapointe matched by name. ok.
- dong2010a (9; printed, slots from header): Kotura Inc. (3 committed), Monterey Park; "Sun labs" printed before
  Oracle America as unit (committed Oracle + Sun Labs / Sun labs unit forms; DO3 without the unit: 2 errors, the
  unit is the first printed field), San Diego; US. DO1 (no slots_from_header) 1 error; DO2 (Zheng on 1) 2 errors. ok.
- roeloffzen2013 (10; printed): Twente Telecommunication Engineering group, Enschede; SATRAX BV and LioniX BV,
  Enschede; block 4 CUDOS + University of Sydney with only the country printed: locality "" (RO2 Sydney 0 errors,
  the known city-inside-org gap; singh2015 lit_h74 form), AU; INRS-EMT, Montréal, CA; block 6 University of Twente
  printed before the group + MESA+ chain (unit; committed MESA+ chains), Enschede; NL (postal boxes and postal codes
  not recorded). Paulus vs list Paul W. L. van Dijk: explicit slot 6 (D287 short form, initials agree; RO1 without:
  2 errors, 0 compatible slots). René G. vs René, Klaus -J. vs Klaus J. matched by name. RO3 (Roeloffzen without 2)
  2 errors. ok.
- maesenovo2013 (9; printed, slots from header): Universidad de Málaga with the department + ETSI chain printed
  before it, Málaga; BIONAND-Andalusian Center for Nanomedicine and Biotechnology, Málaga (street and technology park
  not recorded), ES; NRC of Canada, Ottawa, CA. Detached accents folded (D282). MA1 (Halir without 2) 2 errors; MA2
  (authors 1 / 2 swapped) 24 errors: header order verified. ok.
- herr2014a (7; printed, arXiv): EPFL as printed, Lausanne, CH; Faculty of Physics + "M.V.Lomonosov Moscow State
  University" (no space, as printed; committed "M.V. Lomonosov" form x3), Moscow; Russian Quantum Center, Skolkovo;
  RU. HE1 (Gorodetsky without 3) 3 errors. List full given names agree with the initials. ok.
- guo2016b (10; printed, arXiv): EPFL (accented), Lausanne; Lomonosov MSU Faculty of Physics, Moscow; Russian
  Quantum Center, Skolkovo. The header prints 9 names with Karpov first; list slot 6 Victor Brasch is not printed:
  `author_list_differs`, no_header (GU1 without the flag: 1 error). Order warning expected. Footnotes (asterisks
  equal contribution, dagger correspondence) are printed on the last page of text.md (note claim verified). GU2
  (Karpov forced to slot 6) passes with a warning: the checker accepts an explicit slot between different given
  names (D287 enforced by review only, as lit_h74 TR2). ok (#6 gap).
- keraly2013 (4; printed): "University of California at Berkeley, Berkeley" -> org University of California + campus
  Berkeley (D301; lit_h67 D756 F1 sun2015a "at Berkeley" ruling; KE2 whole string 0 errors, neutral), EECS, Berkeley;
  MIT Mathematics, Cambridge; US. Christopher M. Lalau-Keraly vs list Christopher Lalau Keraly: explicit slot 1
  (distinctive family name, missing middle initial, hyphen vs space; D287 / D369; KE1 without: 2 errors). ok.
- ikeda2008 (4; single, slots from header): "University of California, San Diego" -> org + campus San Diego, ECE,
  locality La Jolla (the city printed after the street; 11 committed UCSD / La Jolla blocks; IK2 locality San Diego
  0 errors, neutral but the campus is not the city); the block prints a state and postal code but no country:
  country "" (IK1 US: 2 errors). Street, postal code and the web address line not recorded. ok.
- obrzud2018 (17; printed, arXiv): seven blocks read in both layers. CSEM with the unit printed after it, Neuchâtel;
  Geneva Observatory/PlanetS + Department of Astronomy + University of Geneva (unit chain), Versoix; INAF with the
  Brera observatory after it (unit), Milano; "Fundación Galileo Galilei - INAF" (dash-joined, D426), Breña Baja
  (province after the city not recorded), ES; "Swiss Federal Institute of Technology (EPFL)" with the printed unit
  codes as unit, Lausanne (building and site code not recorded); Ligentec (park and building not recorded),
  Lausanne; "INAF - Osservatorio Astronomico di Cagliari" (dash-joined, D426), Selargius (province code not
  recorded), IT; CH / IT / ES as printed. The header prints 16 names; list slot 5 (Junqiu Liu) not printed. M.H.
  Anderson vs list Miles Anderson: abbreviated form with an initial H that the list form does not explain, common
  family name -> slot 0 (D369; OB1 without slot: 1 error, 0 matching slots; OB2 slot 4 passes with a warning, barred
  by D369; OB3 without the flag: 1 error). OB4 (Molinari without 7) 3 errors. ok (#4 #5 gaps).
- belt2017 (4; single, capitals): unit + "University of California Santa Barbara" (no comma) -> org + campus Santa
  Barbara (D301), the block prints a state but no separate city: locality "Santa Barbara" from the campus name
  (lit_h07 huang2019 form, same printed block; BE1 locality "" 0 errors, known empty-locality gap; BE2 whole string
  0 errors, neutral), US. Michael Belt / John E. Bowers vs list Michael E. / John Edward matched by name. ok.
- dai2012c (3; printed): Zhejiang University with the centre + two laboratories chain, Hangzhou (Zijingang Campus not
  recorded, lit_h74 xu2013 form), CN; UCSB ECE ("University of California, Santa Barbara" -> org + campus), Santa
  Barbara, US. D12 (Tang on 1) 2 errors. "Daoxin Dai A" list artefact (D412 list), matched by name. ok.
- dai2010 (4; single): "University of California Santa Barbara, ECE Department": the org is printed before the unit
  with the campus name between them, so the campus split fails (DA1: 4 errors, org not inside the block window and
  unit / org not contiguous); org kept whole as printed (lit_h05 form, one committed block), ECE Department, Santa
  Barbara, US. ok.
- dai2011 (2; printed): UCSB ECE (org + campus), Santa Barbara, US; Zhejiang University three-unit chain, Hangzhou,
  CN. ok.
- michaels2018 (2; single, capitals): UC Berkeley EECS (org + campus), Berkeley, US (room and building, state and
  postal code not recorded). ok.
- papes2016 (13; printed): Technical University of Ostrava with the faculty after it, locality "Ostrava-Poruba" as
  printed (D366 as-printed rule; PA4 Ostrava 0 errors, neutral), CZ; NRC Canada, Ottawa, CA; block 3 "Institut
  d’Electronique Fondamentale" (curly apostrophe, committed x2) + more_orgs Université Paris Sud, CNRS, Université
  Paris-Saclay (four orgs, D285; UMR number and building number not copied; Cedex dropped; PA3 single org 0 errors
  but loses three printed orgs), Orsay, FR; Lumerical Solutions, Inc., Vancouver, CA; ETSI Telecomunicación +
  Universidad de Málaga, Málaga, ES; Carleton Electronics, Ottawa, CA; University of Zilina with the department
  after it, Zilina, SK. Cheben 2,8: marker 8 starts the first contact line (checked in text.md), `dropped_markers`
  contact footnote (PA2 without: 2 errors). Gonzalo vs list Juan Gonzalo Wangüemert-Pérez: explicit slot 8 (D287
  name-part variant; PA1 without: 2 errors). ok.
- dai2011a (2; printed): UCSB ECE (org + campus), Santa Barbara, US; Zhejiang University with the centre +
  laboratory chain, Hangzhou, CN. D11A (laboratory dropped from the chain) 2 errors. ok.
- zortman2010 (3; printed, slots from header): Sandia Applied Photonic Microsystems, Albuquerque; UNM CHTM,
  Albuquerque; MIT RLE, Cambridge; US. ZO1 (Zortman without 2) 3 errors. ZO2 (block 3 country "") 0 errors: the
  known O2 gap of lit_h73 (a printed country recorded empty passes); the batch value US is correct. ok.
- chen2012a (2; printed): Alcatel-Lucent Bell Laboratories, Holmdel and Murray Hill, US (streets not recorded). CH1
  (localities swapped) 2 errors. ok.
- cheben2007 (10; single, slots from header): NRC of Canada with the IMS unit, Ottawa, CA (street, building code,
  province and postal code not recorded). CB1 (authors 1 / 2 swapped) 20 errors; CB2 (Post removed) 2 errors:
  header order verified. ok.
- sherwooddroz2008 (7; listing_order): the author line prints 1 / 2, both blocks are printed without markers in the
  text and the PDF layer: listing_order (grade B, 7 rows) is the only basis that verifies (SD2 printed: 2 errors;
  SD3 blocks renumbered: 1 error, order rule enforced; SD4 Wang on 1: 2 errors). Cornell ECE, Ithaca; Columbia EE,
  New York; no country printed: country "" (SD1 US: 2 errors). The contract text ties listing_order to "no local
  PDF"; here the PDF exists but prints no block markers either, so the grade-B call is correct (lit_h75 has the same
  form). K. Bergman / Michal F. Lipson list forms matched by name. ok.
- miller2015 (1; partial, slots from header): the single block prints a building name between the Ginzton
  Laboratory and Stanford University (then a street, state, postal code, USA). Without a skip span the unit / org
  contiguity fails (MI2: 2 errors); with the building name in `skip_between` the record passes and gives 1 row,
  Stanford University + Ginzton Laboratory, Stanford, US (MI1: 0 errors). The extractor followed the batch brief (no
  building names written anywhere), so `partial` + `unreadable` is the correct handling under that brief. The note
  cites "du2024 precedent", but du2024 (lit_h47) skips a street address, not a building name, while committed batches
  lit_h03, lit_h08, lit_h18 and lit_h31 record a building name in `skip_between` (D380): F1, and Q1 for the
  coordinator. Values in the note (org, unit, city, country) agree with the page. ok (#1 gap).

## Extractor calls (verified)

1. `slots_from_header` on dong2010a, maesenovo2013, ikeda2008, zortman2010, cheben2007, miller2015: exactly the 6
   papers with `n_authors_meta` 0; YAML in printed order (DO1; MA2 / CB1 / CB2 show the order is checked).
   Confirmed.
2. `author_list_differs`: guo2016b (9 printed, Brasch list slot 6 not printed; GU1) and obrzud2018 (Liu list slot 5
   not printed; M.H. Anderson slot 0 under D369, list slot 4 uncovered; OB1-OB3). Confirmed.
3. Explicit D287 slots roeloffzen2013 #6 (Paulus / Paul), keraly2013 #1 (Lalau-Keraly / Lalau Keraly, missing
   middle initial, distinctive family name), papes2016 #8 (Gonzalo / Juan Gonzalo): each required (RO1 / KE1 / PA1)
   and allowed by D287 / D369. Confirmed.
4. miller2015 `partial` (building name between unit and org; brief forbids `skip_between`): correct under the brief
   (MI2); a D380 record passes (MI1). Note precedent imprecise (F1); Q1.
5. sherwooddroz2008 both blocks `listing_order`, countries empty: confirmed (SD1-SD4).
6. dai2010 org kept whole "University of California Santa Barbara": confirmed (DA1; lit_h05 form).
7. belt2017 locality from the campus name (huang2019 form): confirmed (BE1 / BE2 neutral). roeloffzen2013 CUDOS
   locality empty: confirmed (RO2 passes only through the known gap). ikeda2008 country empty (state only):
   confirmed (IK1). papes2016 contact marker 8 dropped (PA2) and block 3 with four orgs (PA3): confirmed. ros2019
   "Institue" misprint copied as printed: confirmed (RS1).
8. Campus splits (D301): keraly2013 "at Berkeley", ikeda2008 UCSD, belt2017 / dai2012c / dai2011 / dai2011a UCSB,
   michaels2018 Berkeley: confirmed. Zijingang Campus correctly not a campus.
9. Dash-joined orgs kept (D426): ros2019 "IBM Research - Zurich", obrzud2018 "Fundación Galileo Galilei - INAF" and
   "INAF - Osservatorio Astronomico di Cagliari": confirmed.
10. No street, building, postal code, P.O. box or e-mail text anywhere in the batch, notes included: confirmed.

## Fixes (exact YAML edits)

F1 (miller2015 note, imprecise precedent: du2024 skips a street address, while building names have a committed
`skip_between` form). In `data/_staging/people/lit_headers/lit_h76/headers.yaml`, line 347 (note of
`lit:miller2015`), replace

```
so the block is kept out as a building span inside the unit chain (checker gap D426 G6, du2024 precedent): block not recorded,
```

with

```
so the block is not recorded (D426 G6 handling under this batch's brief; committed batches lit_h03, lit_h08, lit_h18 and lit_h31 record a printed building name in skip_between instead):
```

Probe of the batch with F1 applied (write run on a scratch copy): 0 errors, 4 warnings (unchanged); `header_rows.csv`,
`compare.csv`, `unmapped_orgs.csv` byte-identical to the stamped files (160 rows, 27 unmapped strings); only
`check_stamp.txt` changes. After applying, re-run `uv run python scripts/ofc_headers.py check lit_h76 --corpus lit`.

No other fix: no slot, marker, block field, role, locator or other note is wrong.

## Coordinator question

- Q1 miller2015: the batch brief forbids building names in any output, but D380 (and the D742 ruling) accept a
  verified building name in `skip_between` (never stored in derived files; committed in lit_h03, lit_h08, lit_h18,
  lit_h31, lit_h57, lit_h60). If the D380 form is allowed here, replace the miller2015 `status: partial`, empty
  `affiliations` and unreadable author with a single block (`marker: ""`, basis single, org Stanford University, unit
  Ginzton Laboratory, `skip_between` = the printed building name, locality Stanford, country US) and the author with
  `markers: []` (status ok; MI1: 0 errors, rows 160 -> 161) and rewrite the note. Otherwise keep the batch as is
  (with F1) and add miller2015 to the re-record list.

## Observations (no YAML change)

- O1 Known checker gaps reconfirmed: an explicit slot between different given names passes (GU2, OB2; D287 / D369
  enforced by review only); a printed country recorded empty passes (ZO2, lit_h73 O2); a city inside the org name or
  campus passes as locality / an empty locality passes (RO2, BE1).
- O2 obrzud2018 M.H. Anderson vs list Miles Anderson: likely the same person with the list dropping the middle
  initial; candidate for the D412 author-list correction file. The YAML is correct under D369 until the list is
  corrected.
- O3 Contract wording: listing_order is defined for "text lost the block markers, no local PDF"; sherwooddroz2008
  (and lit_h75) show the case of blocks printed without markers in both layers. Worth one line in the lit contract.

## Lists for the coordinator

- D412 list: obrzud2018 #4 (list Miles Anderson; printed M.H. Anderson; O2); "Daoxin Dai A" (dai2012c, dai2010,
  dai2011, dai2011a #1; already on the artefact list).
- D426 review list: roeloffzen2013 #6 (Paulus / Paul), keraly2013 #1 (Lalau-Keraly), papes2016 #8 (Gonzalo / Juan
  Gonzalo) explicit slots; obrzud2018 M.H. Anderson (slot 0).
- Re-record list (unless Q1 resolves it): miller2015 #1 (Stanford University, Ginzton Laboratory, Stanford, US).
- Org round (27 unmapped strings, 61 rows): Alcatel-Lucent Bell Laboratories; BIONAND-Andalusian Center for
  Nanomedicine and Biotechnology; Carleton University; Fundación Galileo Galilei - INAF; INAF - Osservatorio
  Astronomico di Cagliari; Institut d’Electronique Fondamentale; LioniX BV; Lumerical Solutions, Inc.;
  M.V. Lomonosov Moscow State University and the "M.V.Lomonosov" spelling; National Institute of Astrophysics (INAF);
  Ningbo University; Oracle America (Sun labs unit); Russian Quantum Center; SATRAX BV; Swiss Center for Electronics
  and Microtechnology (CSEM); Swiss Federal Institute of Technology (EPFL); Technical University of Ostrava;
  Universidad de Málaga (two unit forms); University of Exeter; University of Geneva; University of Muenster;
  University of New Mexico; University of Zilina; Université Paris Sud; Université Paris-Saclay.

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE / BASE_W | none | 0 errors, 4 warnings, 160 rows, 27 unmapped; derived files identical | batch as written |
| DO1 / DO2 / DO3 | dong2010a no slots_from_header / Zheng on 1 / Sun labs unit removed | 1 / 2 / 2 errors | D352 flag, markers, unit-first verified |
| MA1 / MA2 | maesenovo2013 Halir without 2 / authors 1-2 swapped | 2 / 24 errors | markers and header order verified |
| IK1 / IK2 | ikeda2008 country US / locality San Diego | 2 / 0 errors | country not printed / neutral (campus is not the city) |
| ZO1 / ZO2 | zortman2010 without 2 / block 3 country "" | 3 / 0 errors | verified / known O2 gap |
| CB1 / CB2 | cheben2007 authors 1-2 swapped / Post removed | 20 / 2 errors | header order verified |
| MI1 / MI2 | miller2015 block with building name in skip_between / without | 0 (161 rows) / 2 errors | D380 form passes (Q1) / contiguity fails |
| GU1 / GU2 | guo2016b no flag / Karpov slot 6 | 1 / 0 errors (+1 warning) | flag required / known explicit-slot gap |
| OB1 / OB2 / OB3 / OB4 | obrzud2018 Anderson no slot / slot 4 / no flag / Molinari without 7 | 1 / 0 (161 rows) / 1 / 3 errors | slot 0 required; slot 4 barred by D369; verified |
| RO1 / RO2 / RO3 | roeloffzen2013 no slot 6 / CUDOS locality Sydney / Roeloffzen without 2 | 2 / 0 / 2 errors | slot required / known gap / verified |
| KE1 / KE2 | keraly2013 no slot 1 / whole "at Berkeley" org | 2 / 0 errors | slot required / neutral (D756 campus form kept) |
| PA1 / PA2 / PA3 / PA4 | papes2016 no slot 8 / no dropped marker / single org / Ostrava | 2 / 2 / 0 (157 rows) / 0 errors | required / required / loses printed orgs / neutral |
| SD1 / SD2 / SD3 / SD4 | sherwooddroz2008 country US / basis printed / blocks renumbered / Wang on 1 | 2 / 2 / 1 / 2 errors | listing_order and empty country verified |
| DA1 | dai2010 campus split | 4 errors | whole org required |
| BE1 / BE2 | belt2017 locality "" / whole UCSB org | 0 / 0 errors | known gap / neutral |
| RS1 / RS2 | ros2019 corrected "Institute" / Rüschlikon | 2 / 0 errors | misprint verified / folded, neutral |
| XU1 / HE1 / D12 / D11A / CH1 / DE1 | marker, unit-chain, locality and order variants | 3 / 3 / 2 / 2 / 2 / 4 errors | verified |
| FIX_W | F1 note rewording | 0 errors, 4 warnings, derived CSVs identical | F1 safe |
