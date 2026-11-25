---
title: Fresh-context audit of the lit author-affiliation batch lit_h70 (24 papers)
date: 2026-11-25
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; checker run only in dry-run or write-run on scratch copies with logs in the scratchpad; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h70/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D352, D366, D368, D380, D410, D416, D426, D442, D565, D659, D742, D756 and earlier lit rulings; D249, D285, D287, D288, D301, D302 from DevLog-008; format from the lit_h69 audit
verdict: GO with F1; 171 slots audited, 167 recorded + 4 no_header (levy2011, D426 G6, correct); 0 wrong rows; 3 imprecise slots (gassenq2012 #3-#5, F1: dash-joined pair split against D426); 10 slots without a row by a known gap, handled as the committed precedents; all 7 named extractor call groups confirmed except the gassenq2012 more_orgs split in call 6
---

# Lit header batch audit: lit_h70 (2026-11-25)

## Scope

Batch lit_h70: 24 papers (Optics Express / Optica printed markers and single blocks, one grouped conference-style
header); 171 slots, 4 papers `slots_from_header` (yu2005, rivoire2009, wang2015, gassenq2012); 216 rows. Restricted
corpus: this record names only authors, orgs, units, cities and countries; no paper text is quoted and no contact,
street, building, site, box or postal text is copied (such spans are named by type only).

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h70 --corpus lit --codes <id> --pdf`
  (all 24, page 1 is the header page in all of them); output kept in the session scratchpad `h70_audit/show/` only.
- Per slot: printed name vs the `show` author list (or the header order for the 4 header-slot papers) and
  `compare.csv`; marker run in both layers; block fields (org, unit chain, more_orgs, campus, city, country); role;
  locator; notes. Committed lit batches grepped for each form question (UCSB, HKUST / CUHK, Grenoble, Lyon, Montpellier,
  dash-joined orgs, DESY / CFEL, KIST School, XIOPM, USTC, Twente, Jr. suffix, Current address precedents).
- All 216 rows of `header_rows.csv` read by paper: roles primary 179, additional 35, present address 2; basis printed
  195, single 16, grouped 5; all grade A; all locators p.1 header. `compare.csv`: 167 `recorded`, 4 `no_header`
  (levy2011); `order_differs` false on all 171.
- Address / contact scan of `headers.yaml` and every derived file (contact sign, URL, 3+-digit numbers, street, road,
  avenue, boulevard, drive, suite, building, room, hall, box, cedex, e-mail / mail, phone, fax, postal, UMR and the
  joint-unit numbers, and every street, building, district, campus and site token printed in this batch's blocks).
  Hits: "DevLog-011" and the extraction date in the file comment; type words in notes ("street address(es)", "postal
  code(s)", "building number", "a campus and a site name", "UMR number", "Cedex"); the D366 district names Clear Water
  Bay / Kowloon in the xue2021 and wan2017 notes (district printed before the city goes to the note, D366; lit_h53
  ahmmed2020 precedent); campus field values (D301). No contact, URL, postal code, street, building, box or site
  text anywhere, notes included.
- Probes on scratch copies (`h70_audit/probes/probe.py` + `mk.py`, scratch `LIT_BASE`, batch name `lit_p70`,
  `cmd_check(..., dry_run=True)`, `RunLog` redirected to the scratchpad: no log written under `logs/`; 41 runs: 39 variants,
  the base write run and the F1 run). Run of the batch as written: 0 errors, 2 warnings (explicit slots porcel2017 #6,
  shtyrkova2019 #7); scratch write-run derived files byte-identical to the stamped `header_rows.csv`, `compare.csv`,
  `unmapped_orgs.csv`, `check_stamp.txt`. md5 of every repo batch file identical before and after the audit;
  `check_stamp.txt` matches `headers.yaml` (sha256 62c93cfa...).

## Counts

| batch | papers audited / total | slots audited | ok | gap (correct handling, no row) | imprecise | wrong |
|---|---|---|---|---|---|---|
| lit_h70 | 24 / 24 | 171 | 158 | 10 | 3 | 0 |

- Papers ok 23, partial 1 (levy2011: authors 1-4 unreadable, D426 G6), unreadable 0; `slots_from_header` 4 (exactly
  the papers.csv rows with `n_authors_meta` 0, each prints the D352 line in `show`); `author_list_differs` 0; explicit
  slots 2 (porcel2017 #6, shtyrkova2019 #7, both required); order warnings 0; present addresses 2 (porcel2017 #5
  LioniX, shtyrkova2019 #1 MIT Lincoln Laboratory); dropped markers 11 (equal contribution: wang2017a #1 #2 marker 4,
  wan2017 #1 #2 #3 marker 7; Current address cue: shtyrkova2019 #4 marker 4, li2018b #2 #3 #9 #10 marker 3, #4 marker
  4); unreadable authors 4 (levy2011); 19 unmapped org strings.
- Gap slots (10): levy2011 #1-#4 (blocks 1-2 not recordable, G6); shtyrkova2019 #4 and li2018b #2 #3 #4 #9 #10
  (Current address blocks not recordable, D442 cue gap). Imprecise (3): gassenq2012 #3 #4 #5 (F1).
- Per paper (slots / rows): porcel2017 7 / 8; wang2017a 7 / 9; levy2011 4 / 0; yu2005 5 / 5; xu2021b 9 / 10;
  osorniomartinez2025a 4 / 4; yan2016 4 / 4; rivoire2009 5 / 5; chang2016 6 / 7; shtyrkova2019 9 / 13; zhang2017b
  5 / 10; chu2023 7 / 10; wan2019a 11 / 15; li2018b 12 / 13; auth2019 5 / 5; duprez2016 4 / 14; wang2015 7 / 11;
  xue2021 8 / 8; wan2017 14 / 18; yu2020 11 / 11; gassenq2012 6 / 15 (12 after F1); wang2013 5 / 5; jiang2018a 9 / 9;
  liu2017a 7 / 7.
- Privacy findings: 0. Notes: 23 correct, 1 to reword with F1 (gassenq2012).

### Per-slot field counts

| field | ok | gap | imprecise | wrong |
|---|---|---|---|---|
| name / slot (171) | 171 | 0 | 0 | 0 |
| markers (printed / single / grouped / dropped, 171) | 171 | 0 | 0 | 0 |
| header position / order | 171 | 0 | 0 | 0 |
| blocks (org / unit / more_orgs / campus / locality / country) (216 rows) | 213 | levy2011 blocks 1-2, 6 Current address blocks not recorded | 3 (gassenq2012 block 3 more_orgs) | 0 |
| roles (primary / additional / present address) | 216 | 0 | 0 | 0 |
| locators | all | 0 | 0 | 0 |
| notes (24) | 23 | 0 | 1 (F1) | 0 |

## Per-paper findings

- porcel2017 (7; printed): calls 2, 4. Block 1 University of Twente with the group, Mesa+ institute and department as
  one unit chain (printed before the org; committed Twente forms), Enschede, NL. Markers 1 / 1 / 1 / 1 / 1,2 / 1 / 1. ok.
- wang2017a (7; printed): Harvard SEAS, Cambridge, US (street not recorded); USTC with the key laboratory and the
  synergetic innovation center as one unit ("Information&" glued as printed; lit committed USTC unit forms), Hefei, CN;
  VCU ECE, Richmond, US. Marker 4 points to the equal-contribution line: dropped on #1 / #2 (correct). ok.
- levy2011 (4; printed, partial): call 1. ok as handled.
- yu2005 (5; grouped, slots from header): two author groups each printed above its block (D368): Solid State and
  Photonics Laboratory / E. L. Ginzton Laboratory, Stanford University, Stanford; both print only the state and postal
  code, no country: country "" (D249). Call 7 (Harris). Probe Y4 (Kuo on G1) 2 errors; probe Y3 (authors 1 / 2
  swapped) 0 errors (O2). ok.
- xu2021b (9; printed): three NTT laboratory blocks (unit lab, org NTT Corporation, locality "Atsugi-shi" as printed,
  D366), Nihon University with department + college chain, "Koriyama-shi" (districts before it not recorded), Yamato
  University "Suita-shi"; all JP. Author line broken across lines ("HIROO / OMI") read correctly; markers 1 / 1 / 2,3 /
  1 / 1 / 4 / 5 / 1 / 1. ok.
- osorniomartinez2025a (4; single): University of Twente, Integrated Optical Systems, MESA+ Institute (form of 7 blocks in
  other lit batches), Enschede, NL; daggers equal contribution. List forms with full given names match the printed initials. ok.
- yan2016 (4; printed single block with marker 1, D285): The Australian National University with the three-level
  unit chain, Canberra (territory not recorded), AU. "KHU VU" vs list "Khu T. Vu" matched by name. ok.
- rivoire2009 (5; printed, slots from header): Ginzton Laboratory, Stanford, "U.S.A." -> US; Humboldt University,
  Department of Physics, Berlin, DE (postal code between org and city not recorded). Header order = YAML. Probe R1
  (block 1 country "") 0 errors (O3, known empty-field gap). ok.
- chang2016 (6; printed): University of California + campus Santa Barbara (printed with a comma), ECE, Santa Barbara,
  US; XIOPM with "Chinese Academy of Sciences" in the printed name and the state key laboratory as unit (form of 3
  blocks in other lit batches), "Xi’an", CN. ok.
- shtyrkova2019 (9; printed): calls 2, 3, 4, 5. ok (#4 gap).
- zhang2017b (5; printed): "Ghent University – imec" joined (D426), group + department chain, Ghent, BE; block 2
  Ghent University, Center for Nano- and Biophotonics, no city printed: locality "" correct (probe Z1 "Ghent": 0
  errors, known gap: a city inside the org name is accepted). ok.
- chu2023 (7; printed): call 6 (KIST School), call 7 (HOSUNG KIM). KIST Center for Opto-Electronic Materials and
  Devices, Seoul; ETRI, Daejeon; all "Republic of Korea" -> KR. Probe C1 (Kim on 1) 3 errors. ok.
- wan2019a (11; printed): call 6 (UCSB). Block 2 Zhejiang University with centre + state key laboratory chain,
  Hangzhou, CN. Markers 1 / 2 / 3 / 4 / 4 / 4 / 4 / 3 / 2 / 1,3,4 / 1,3,4 match both layers; daggers and asterisk not
  blocks. ok.
- li2018b (12; printed): call 3. MIT RLE, Cambridge; Harvard "School of Engineering and Applied Science" (singular, as
  printed), Cambridge; University at Albany, College of Nanoscale Science and Engineering, Albany; all US. ok (#2 #3
  #4 #9 #10 gap).
- auth2019 (5; printed): call 6 (UCSB). "Technische Universitat Darmstadt" as printed in both layers (probe A1 with
  umlaut: 0 errors, neutral; as printed kept), Institute of Applied Physics, Darmstadt, DE (street not recorded). Author
  line broken over five lines ("JOHN / EDWARD BOWERS") read correctly. ok.
- duprez2016 (4; printed): call 6. ok.
- wang2015 (7; printed, slots from header): "Ghent University-imec" joined (D426), Photonics Research Group, Ghent;
  Ghent University NB-Photonics, Ghent; TU München, Walter Schottky Institut, Garching, DE (street not recorded).
  Header order = YAML (probe W1, authors 1 / 2 swapped: 2 errors). ok.
- xue2021 (8; printed): call 6 (HKUST). CUHK Department of Electronic Engineering, Hong Kong, HK (committed form). ok.
- wan2017 (14; printed): call 6 (UCSB, HKUST), call 7 (RUILIN CHAO). National Central University, Department of
  Electrical Engineering, Jungli, "Taiwan" -> TW; Hewlett Packard Enterprise with "Hewlett Packard Labs" as unit (D565
  form; probe H1 lab as org: 0 errors, +2 rows, not better), Palo Alto, US (street not recorded). Marker 7 equal
  contribution dropped on #1-#3. Markers match both layers. ok.
- yu2020 (11; printed): University of Virginia ECE, Charlottesville; NIST Microsystems and Nanotechnology Division,
  Gaithersburg; LIGENTEC SA, Ecublens, CH (street and postal code not recorded). List forms with diacritics / middle
  initial matched by name. ok.
- gassenq2012 (6; printed, slots from header): call 6 (IES). Block 1 "Ghent University-IMEC" joined, unit chain
  "Photonics Research Group, INTEC Department", Ghent; block 2 no city, locality "" correct. Block 3: imprecise (F1).
  "Roelkens,1,2" with a trailing comma read correctly. Header order = YAML.
- wang2013 (5; single): University of British Columbia ECE, Vancouver (province not recorded), CA. ok.
- jiang2018a (9; printed): call 7 (YAN LI). Zhejiang University college, Hangzhou; Longyan University department,
  Longyan; CN. ok.
- liu2017a (7; single): SJTU state key lab + department chain, Shanghai, CN. Only an asterisk on the author line. ok.

## Extractor calls (verified)

1. levy2011 partial. Blocks 1 and 2 each print a building number with a building name between the Cornell school and
   "Cornell University"; the unit-org pair is then not one contiguous segment (probe L1b, building name alone in
   `skip_between`: 2 errors) and the only passing record stores the building number in `skip_between` (probe L1: 0
   errors, the address scan does not catch it, O1), which D244 / the contract forbid (no block / building number in
   any field). Recording the org without the unit fails (L2, 2 errors). So blocks 1-2 are unrecordable (D426 G6;
   lit_h31, h43 chen2022d, h46, h58, h66 precedents) and authors 1-4 are unreadable: Lipson prints 1,3 and cannot be
   readable with marker 3 only (L3, 2 errors). Keeping block 3 with Lipson's marker 3 follows chen2022d; the checker
   would also pass without it (L4, 0 errors, rows unchanged), so it is harmless and keeps the block verified for the
   re-record. The note carries the unit / org / city values for re-recording and no building text. Confirmed.
2. Explicit slots. porcel2017 #6 printed "PETER J.M. VAN DER SLOT" vs list "Petrus J.M. van der Slot": alternate
   given name with agreeing initials (D287), required (probe P1 without: 2 errors). shtyrkova2019 #7 printed
   "KÄRTNER" vs list "Käertner": list misspelling (D287), required (probe S1: 2 errors). Confirmed; both go to the
   D426 review list.
3. Current address blocks. shtyrkova2019 block 4 (Koç University, Istanbul) and li2018b blocks 3 (Analog Photonics
   LLC, Boston) and 4 (Koç University, Istanbul) print the cue "Current address" / "Current Address" after the marker.
   The checker cannot record them with either role (probes S2 / LI1 present_address and S3 / LI2 affiliation: 2 and 5
   errors, the cue sits between the marker and the first field); without the dropped marker the author fails (S4: 2
   errors). Ruling: `status: ok` with the marker in `dropped_markers` is correct. The contract's `partial` means an
   author whose markers cannot be read (`unreadable: true`, no rows); these authors' markers are read and their primary
   rows are right, only the present-address row waits for the D442 cue fix. DevLog-011 D565 (lit_h39 li2018, kept ok,
   imprecise, re-record list) and D659 (lit_h54 zamek2011 ok, li2018 precedent) rule exactly this; 12 committed papers
   use it (beeck2021, ji2017, koyaz2026, kuyken2011, jung2020, purnawirman2017, li2018, liu2020b, yu2025a, zamek2011,
   schall2016, cardenas2009); lit_h67 pernice2012a is partial for a different reason (an unmarked author). A brief
   asking for `partial` here contradicts the contract and D565 / D659. The reason wording matches lit_h17 (the
   13-entry alternative "current address (cue not supported by the checker)" is equivalent; no change). Re-record list:
   shtyrkova2019 #4, li2018b #2 #3 #4 #9 #10 (values in the notes). Confirmed.
4. porcel2017 block 2 ("Currently with", LioniX International BV, Enschede, NL) and shtyrkova2019 block 2 ("Presently
   with", MIT Lincoln Laboratory, Lexington, US) as `present_address`: the checker reads both as present-address cues
   (probes P2 / S5 role affiliation: 2 errors each). Confirmed.
5. shtyrkova2019 block 5: org "Deutsches Electronen Synchrotron (DESY)" exactly as printed (misspelt Electronen, no
   hyphen, acronym in parentheses), unit "Center for Free-Electron Laser Science" (printed before "at" + the org; the
   committed lit_h22 / lit_h47 CFEL blocks use the same org + unit split), University of Hamburg as a structured
   `more_orgs` entry with its own unit "Department of Physics and Center for Ultrafast Imaging" (D367), Hamburg, DE.
   Probes: S7 without "(DESY)" 0 errors (neutral; as printed kept), S8 plain-string Hamburg 0 errors (loses the unit),
   S6 Hamburg dropped 0 errors (known missing-more_orgs gap). Unmapped as printed (org round alias to the DESY id).
   Confirmed.
6. Place / org forms:
   - "University of California Santa Barbara" without a comma -> org University of California + campus Santa Barbara
     (wan2019a 3 blocks, wan2017 3, auth2019 2): the form of 94 UCSB blocks in the other lit batches (one older whole string);
     probe U1 campus removed 0 errors, +1 unmapped (known gap); U2 whole string 0 errors (neutral). Confirmed.
   - HKUST (xue2021 block 1, wan2017 block 5) prints two districts before "Hong Kong, China": locality Hong Kong,
     country HK, districts in the note (D366, D288 "Hong Kong SAR, China" -> HK; lit_h60 geng2014 and the 4 other lit
     HKUST blocks). Probes X1 locality Kowloon / X2 country CN: 0 errors each (the rulings decide, not the checker).
     Confirmed.
   - duprez2016 block 1 "Univ. Grenoble Alpes" + structured `more_orgs` CEA with unit LETI, Grenoble (campus and site
     name not recorded): the majority committed form (lit_h07, h09, h10, h13, h14, h21 ferrotti2016); probe D1 (CEA,
     LETI as plain orgs) 0 errors, +3 rows: not better. Block 2 "Univ. Lyon" + INL, CNRS, Ecole Centrale de Lyon in
     `more_orgs`, Ecully (UMR number not copied): the lit_h27 / lit_h29 Université de Lyon form (first printed org as
     org); probe D2 (CNRS dropped) 0 errors, known gap. Confirmed.
   - gassenq2012 block 3: IES as org (joint unit printed first as an organization, D285 / D466) with the UMR number not
     copied, locality Montpellier ("cedex" designation dropped, D366), FR: confirmed. The split of the printed
     dash-joined pair "Université Montpellier 2 - CNRS" into two `more_orgs` is not: D426 (D416 (5) extended) keeps
     dash-joined joint orgs as printed, with aliases in the org round; the same paper keeps "Ghent University-IMEC"
     joined, and lit_h52 keeps the analogous UMR pair "CNRS-Université de Montpellier" (and "CRHEA-CNRS") as one
     string. Probe G1 (joined) 0 errors, rows 15 -> 12, unmapped count unchanged. -> F1.
   - chu2023 block 2 "Division of Nanoscience and Technology, KIST School" as unit, "University of Science and
     Technology" as org, Seoul, KR: the committed lit form (lit "Korea University of Science and Technology (UST)"
     block with the same unit chain); probe K1 (KIST School out of the unit) 2 errors (not contiguous); K2 (org "KIST
     School at University of Science and Technology") 0 errors, neutral. The bare org string is ambiguous for the
     matcher (unmapped; org round: alias to the Korean UST id, not to any other "University of Science and
     Technology"). Confirmed.
7. Names:
   - yu2005 #3 "J. S. Harris Jr.": the printed comma before the suffix is rejected by the checker (probe Y1: 1 error);
     the committed suffix form is "Name Jr." (Osgood, Holmes, Delfyett, Stephens, do Nascimento); Y2 without the
     suffix also passes (neutral). Confirmed.
   - jiang2018a #4 printed "YAN LI" vs list "Yan Jun Li": matched by name (dropped middle given-name part, D247);
     `slot: 0` is rejected (probe J1: D302). Accepted as the D426 dropped-syllable family (fang2010, feng2011, jin2024,
     xu2025, ren2025); D426 review list. Confirmed.
   - chu2023 #5 "HOSUNG KIM" vs list "Ho-Sung Kim" and wan2017 #3 "RUILIN CHAO" vs list "Rui-Lin Chao": the same given
     name without the hyphen; matched by name, no explicit slot needed (compare.csv recorded, 1 / 2 rows). Confirmed.

## Fixes (exact YAML edits)

F1 (gassenq2012, imprecise: 3 slots #3 Cerutti, #4 Rodriguez, #5 Tournié; D426 dash-joined form). In
`data/_staging/people/lit_headers/lit_h70/headers.yaml`:

Line 332, replace

```
    - {marker: "3", basis: printed, org: "Institut d’Electronique du Sud (IES)", more_orgs: ["Université Montpellier 2", "CNRS"], locality: "Montpellier", country: "FR"}
```

with

```
    - {marker: "3", basis: printed, org: "Institut d’Electronique du Sud (IES)", more_orgs: ["Université Montpellier 2 - CNRS"], locality: "Montpellier", country: "FR"}
```

Line 328 (note), replace

```
block 3 prints IES, then Université Montpellier 2 and CNRS joined by a dash (two organizations; UMR number not copied; Cedex dropped, D366)
```

with

```
block 3 prints IES, then Université Montpellier 2 and CNRS joined by a dash (kept as printed in more_orgs, D426; lit_h52 CNRS-Université de Montpellier form; UMR number not copied; Cedex dropped, D366)
```

Probe of the batch with F1 applied (both edits): 0 errors, 2 warnings (the two explicit slots), rows 216 -> 213
(gassenq2012 15 -> 12), unmapped strings 19 (the split "Université Montpellier 2" is replaced by the joined string).
After applying, re-run `uv run python scripts/ofc_headers.py check lit_h70 --corpus lit` (stamp and derived files
change). Org round: alias "Université Montpellier 2 - CNRS" (as for "CNRS-Université de Montpellier").

No other fix: no slot, marker, block field, role, locator or other note is wrong.

## Observations (no YAML change)

- O1 Privacy-scan gap: a building number followed by a building name ("<3-digit number> <Name> Hall") in
  `skip_between` passes the D244 scan (probe L1, 0 errors; `ADDRESS_RES` has no building-number pattern). The
  extractor did not use it; G6 stays a policy block, and a D410-style placeholder (e.g. `<building number>` verified by
  pattern) would make levy2011 and the other G6 papers recordable. Owner / checker list.
- O2 Grouped / header-slot order gap reconfirmed (h69 O1, D756): yu2005 authors 1 / 2 swapped inside a group pass
  (Y3); printed-basis header-slot papers are order-checked (W1, 2 errors). yu2005 checked by reading.
- O3 Known gaps reconfirmed: empty country accepted when the block prints one (R1), missing `more_orgs` (S6, D2),
  missing `campus` (U1), a district or a city inside the org name accepted as locality (X1, Z1).
- O4 Org round strings of note: "Deutsches Electronen Synchrotron (DESY)" (misprint, alias to DESY), "University of
  Science and Technology" (Korean UST via KIST School unit), "Technische Universitat Darmstadt" (no umlaut), "Univ.
  Lyon" / "Univ. Grenoble Alpes" short forms, "Université Montpellier 2 - CNRS" after F1.

## Lists for the coordinator

- D412 list: none.
- D426 review list: porcel2017 #6 (PETER / Petrus J.M. van der Slot), shtyrkova2019 #7 (KÄRTNER / Käertner), explicit
  slots; jiang2018a #4 (YAN LI / Yan Jun Li), dropped middle part matched by name.
- Re-record list: levy2011 #1-#4 blocks 1-2 (G6, values in the note); shtyrkova2019 #4 block 4 and li2018b #2 #3 #9 #10
  block 3, #4 block 4 (D442 "Current address" cue, values in the notes).
- Org round (19 unmapped strings as written): Deutsches Electronen Synchrotron (DESY); Ecole Centrale de Lyon;
  Humboldt University; Institut des Nanotechnologies de Lyon-INL; Institut d’Electronique du Sud (IES); Longyan
  University; Nihon University; Technische Universitat Darmstadt; Technische Universität München; The Australian
  National University; Univ. Grenoble Alpes; Univ. Lyon; University at Albany; University of Hamburg; University of
  Science and Technology (KR); Université Montpellier 2 (-> "Université Montpellier 2 - CNRS" after F1); Virginia
  Commonwealth University; Xi’an Institute of Optics and Precision Mechanics, Chinese Academy of Sciences; Yamato
  University.

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 2 warnings, 216 rows, 19 unmapped; derived files identical | batch as written |
| L1 / L1b / L2 | levy2011 block 1 with building number + name in skip_between / building name only / org without unit | 0 (+3 rows) / 2 / 2 errors | only a forbidden record passes (O1) / G6 confirmed |
| L3 / L4 | Lipson readable with marker 3 / block 3 removed, Lipson markers [] | 2 / 0 errors | unreadable required / block 3 optional, kept (chen2022d) |
| P1 / P2 | porcel2017 slot 6 removed / block 2 role affiliation | 2 / 2 errors | slot required / Currently with is a cue |
| S1 / S4 / S5 | shtyrkova2019 slot 7 removed / Magden dropped marker removed / block 2 role affiliation | 2 / 2 / 2 errors | verified |
| S2 / S3 | block 4 Koç University as present_address / as affiliation | 2 / 2 errors | Current address cue not recordable (D442) |
| LI1 / LI2 | li2018b block 3 Analog Photonics as present_address / as affiliation | 5 / 5 errors | D442 gap confirmed |
| S6 / S7 / S8 | Hamburg more_org dropped / "(DESY)" removed / Hamburg as plain string | 0 / 0 / 0 errors | known gap / neutral / neutral |
| U1 / U2 | wan2019a campus removed / whole "University of California Santa Barbara" | 0 (+1 unmapped) / 0 errors | known gap / neutral; campus form kept |
| X1 / X2 | xue2021 locality Kowloon / country CN | 0 / 0 errors | rulings decide (D366, D288) |
| G1 / G2 / G3 | gassenq2012 pair joined / "(IES)" removed / UM2 dropped | 0 (-3 rows) / 0 / 0 errors | F1 form passes / neutral / known gap |
| FIX | G1 + note rewording | 0 errors, 2 warnings, 213 rows, 19 unmapped | F1 safe |
| D1 / D2 | duprez2016 CEA, LETI as plain orgs / CNRS dropped | 0 (+3 rows) / 0 errors | committed form kept / known gap |
| K1 / K2 | chu2023 KIST School out of the unit / org "KIST School at ..." | 2 / 0 errors | unit chain required / neutral |
| Y1 / Y2 / Y3 / Y4 | yu2005 "Harris, Jr." / "Harris" / authors 1-2 swapped / Kuo on G1 | 1 / 0 / 0 / 2 errors | comma rejected / neutral / O2 / grouping verified |
| J1 | jiang2018a YAN LI slot 0 | 1 error (D302) | match by name required |
| C1 | chu2023 Kim on marker 1 | 3 errors | verified |
| W1 | wang2015 authors 1-2 swapped | 2 errors | header order verified |
| R1 / Z1 | rivoire2009 block 1 country "" / zhang2017b block 2 locality Ghent | 0 / 0 errors | known gaps (O3) |
| A1 / H1 | auth2019 umlaut added / wan2017 HP Labs as org | 0 / 0 (+2 rows) errors | neutral / D565 form kept |
