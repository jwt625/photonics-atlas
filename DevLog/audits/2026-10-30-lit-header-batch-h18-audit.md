---
title: Fresh-context audit of the lit author-affiliation batch lit_h18 (35 papers)
date: 2026-10-30
auditor: Claude (fresh context; wrote only lit_h18/headers.yaml, the derived files the checker writes, and this record; aggregate not run)
scope: data/_staging/people/lit_headers/lit_h18/headers.yaml; both header contracts; DevLog-011 D350-D369, D380, D400-D416; previous audits 2026-10-29-lit-header-batches-3-audit.md, 2026-10-29-lit-header-batches-4-audit.md
verdict: GO for the people rebuild after the fixes below (applied; check 0 errors, 2 warnings); 0 wrong and 3 imprecise slots in 214 audited (2 fixed, 1 known checker gap); 1 note named site names (made by-type)
---

# Lit header batch audit, lit_h18 (2026-10-30)

## Scope

Batch lit_h18 (35 papers, 214 author-list slots), extracted 2026-10-30 (extractor check: 0 errors, 2 warnings, 34 ok /
1 partial, 213 / 214 slots, 242 rows). Restricted corpus: this record names only authors, orgs, units, cities and
countries; no paper text is quoted and no contact, street, building, postal or box code is copied.

## Method

- Every paper read with `env -u VIRTUAL_ENV uv run python scripts/ofc_headers.py show lit_h18 --corpus lit --codes
  <id> --pdf` (all 35 with the PDF view; `--pages 2` for moser2011, shoji2002, shoji2008, taillaert2006). The
  pernice2012 present-address marker was additionally checked on a rendered crop of the PDF page 1 (author line and
  footnote; crop deleted after viewing).
- Selection: all 35 papers (full coverage):
  - (a) explicit `slot:`: pernice2012 #5, popovic2006 #7; no `slot: 0`, no `author_list_differs`, no
    `slots_from_header`;
  - (b) partial: yang2010; present address: pernice2012, yang2010; prose: matsuo2013, mekis2010; unreadable: none;
  - (c) flagged items: mcnab2003, taillaert2006 (mixed layout), thomson2007 (Scotland, `skip_between`), vivien2009
    (more_orgs, capitals), liu2011 (unit chain), ma2013 / streshinsky2013 / zhang2010 (A*STAR parent), sysak2008 /
    tan2009 (campus), pathak2012 / vermeulen2010 / soganc2013 (dash-joined orgs), shoji2002 / shoji2008 /
    mizukami2011 / matsuo2013 / shoji2010 (Japanese places), moser2011 / zhang2013 / shoji2008 (dropped markers),
    piggott2015 (D412), streshinsky2013 (reordered name), moser2011 / shoji2008 / taillaert2006 (header on p.2),
    shoji2002 (block after the letter text), vlasov2004 / xia2007 / popovic2006 / pfeifle2012 (empty fields);
  - (d) the remaining papers: lira2012, mauthe2020, schuck2013, sun2013, wang2012, yin2007, zaoui2012.
- Per slot: slot-to-name assignment (D359, D369, D287, D302), printed marker run vs `markers` + `dropped_markers`
  (text and PDF layer), block mapping, org / unit / more_orgs split, parent rule, campus (D301), locality (first printed
  city as printed), country (printed), role, basis. Every note claim checked against the page.
- Name scan: all 214 `compare.csv` rows, list name vs printed name (folded); 67 rows differ, every one inspected.
- Claims tested with dry-run probes (`check --dry-run` on a temporarily edited `headers.yaml`, file restored
  byte-identical, md5 asserted after each probe; helper in the session scratchpad).
- Privacy scan: every field and note of `headers.yaml`; every value of `header_rows.csv`, `compare.csv` and
  `unmapped_orgs.csv` (contact / URL / ORCID patterns, 3+ digit runs other than paper codes and decision numbers,
  street / building / box / site words and the address words printed in this batch's blocks).
- Backup before any edit: `backup_lit_h18_20261030T004625.zip` (lit_h18 directory) in the session scratchpad
  `lit_h18_audit/`.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h18 | 35 / 35 | 214 | 211 | 3 | 0 |

- Fixed: 2 imprecise (mcnab2003 #1 #3, F1). Not fixable within the contract / checker: 1 imprecise (yang2010 #4, C1).
- The 1 `no_header` slot: yang2010 #4 (Joris Van Campenhout; only a present-address block, C1).
- Header-only authors (`slot: 0`): none.

## Rulings on slot overrides and known items

| paper, slot | printed vs list | ruling |
|---|---|---|
| pernice2012 #5 | G.N. Goltsman vs Gregory N Gol'tsman | keep `slot: 5` (D287 transliteration variant, initials agree, same position); probe without it: 0 slots matched, 2 errors |
| popovic2006 #7 | Franz X. Kärtner vs Franz X. Käertner | keep `slot: 7` (D287 spelling variant of the umlaut in the list, same position); probe without it: 2 errors |
| piggott2015 #6 | Jelena Vučković vs list artefact "Jelena Vuckovic A" | correct person, auto-matched; a further D412 case (as white2022 / white2024; open question 2) |
| streshinsky2013 #4 | Roger Tern Poh Cher vs Roger Poh Cher Tern | correct (same four name parts, list order permuted; same position) |
| yang2010 #4 | Joris Van Campenhout, printed marker 2 only (present address, IMEC, Leuven) | `unreadable` + `partial` correct under the checker (keyvaninia2019 precedent); probe readable: "has no markers and the paper has no unmarked block" + warning "only a present-address block" (C1) |
| other list-side differences | lira2012 #1 #4, liu2011 #4, ma2013 #8, mauthe2020 #8, mekis2010 #3 #5, mizukami2011 #6, moser2011 #1-#7, pathak2012, pernice2012 #1-#4 #6 #7, pfeifle2012 #2 #3 #5, popovic2006 #3, shoji2002, shoji2008 #5 (Jr.), soganc2013 #1, sun2013 #5, sysak2008 #3, taillaert2006 #3, tan2009, thomson2007, vermeulen2010, vivien2009 #9, wang2012 #4, xia2007 #4, yang2010 #9, zaoui2012 #3, zhang2013 #4 | all initials agree, same positions: correct |

## Findings and fixes

| # | paper, slots | rating | evidence (locator) | fix (field: before -> after) |
|---|---|---|---|---|
| F1 | mcnab2003 #1 #3 (Sharee J. McNab, Yurii A. Vlasov), unmarked block | imprecise | p.1 header: IBM T.J. Watson Research Center, Yorktown Heights, the state, a postal code, then USA (text and PDF layer); the note said the block prints no country; probe with the country: 0 errors | block 1 `country: "" -> "US"`; note: false clause replaced (state and USA printed) and the second place of block 2 (Zurich after Rueschlikon) added per D288. The 2 rows of block 1 now carry US |
| N1 | vivien2009 (note) | privacy rule | note spelled out the two site names printed after CEA-LETI in block 2 (round-3 F5 rule: site names only by type outside `skip_prefix` / `skip_between`) | note: site names replaced by "two site names"; no field changed |
| C1 | yang2010 #4 (Joris Van Campenhout) | imprecise, known (no row) | p.1 header: only marker 2, a present-address block (Currently with IMEC, Leuven, BE) | none: `unreadable` kept (gap G4 of round 3, keyvaninia2019) |

Checked and correct (highlights):
- Present address: pernice2012 block w (Karlsruhe Institute of Technology (KIT), Institute of Nanotechnology,
  Eggenstein-Leopoldshafen, DE) `role: present_address`, carried by Pernice with block 1. The printed mark is a dagger
  on the rendered page; both the text and the PDF layer extract it as the letter w (author line and footnote). Probe
  with the dagger recorded: 6 errors (marker run and block not found in either layer); "w" is the only verifiable form
  (open question 1). The block prints the org before the institute: institute as unit, as pfeifle2012 (KIT institutes
  as units).
- Mixed layouts (grade B): mcnab2003 (unmarked IBM Watson block + asterisk-marked IBM Zurich Research Laboratory
  block carried by Moll; the asterisk is the affiliation mark here, no contact line uses it) and taillaert2006
  (unmarked Ghent University block + block 1 University of St. Andrews carried by Ayre; U.K. -> GB; region not
  recorded). The empty superscript after Taillaert in the PDF view has no footnote on the page (no marker).
- Prose: matsuo2013 P1 / P2 (two NTT laboratory statements, subjects match carriers both ways, prefecture only:
  `locality: ""`); mekis2010 P1 (all authors, Luxtera, Inc., Carlsbad, US).
- Dropped markers: moser2011 a (contact) and b (on-leave footnote, D249, not a block); shoji2008 a (contact);
  zhang2013 3 / 4 / 5 (contact lines). Symbol marks used by no block (asterisks, envelope, zhang2013 daggers) need no
  entry. Every author's printed run matches `markers` + `dropped_markers` in all 35 papers.
- Header on page 2 (publisher cover page 1): moser2011, shoji2008, taillaert2006 with `p.2 header` on every block.
  shoji2002: author line on p.1, single unmarked block printed after the letter text on p.2 (`p.2 affiliations`).
- Parents not copied: ma2013 block 2, streshinsky2013 block 1, zhang2010 (Institute of Microelectronics with A*STAR
  and its expansion after it): contract parent rule, lit_h03 IMRE precedent; 11 earlier "Institute of
  Microelectronics, Singapore" blocks are recorded the same way.
- more_orgs: vivien2009 block 1 IEF with CNRS and Université Paris-Sud XI (three orgs, as pilot virot2014 and the
  C2N / Télécom SudParis precedents of lit_h03 / h06 / h09 / h13); block 2 CEA-LETI; localities ORSAY / GRENOBLE in
  capitals as printed (brun2014 precedent); the Y.Lecunff glued initial written with a space.
- Unit chain: liu2011 block 3 (Wuhan National Laboratory for Optoelectronics, school, then HUST; as lit_h16 ding2013
  and most precedents); block 2 DTU-Fotonik as unit of Technical University of Denmark, Lyngby.
- Campus: sysak2008 University of California, Santa Barbara (comma) and tan2009 University of California San Diego
  (no comma, locality La Jolla): both match the 2 earlier San Diego / La Jolla and 20+ Santa Barbara records.
- Dash-joined orgs kept as printed (D416 (5)): pathak2012 and vermeulen2010 Ghent University - imec, soganc2013 IBM
  Research - Zurich; the lit batches hold 40+ dash- or slash-joined Ghent / imec org strings vs 6 split into org + more_orgs (open
  question 4).
- Japanese places: mizukami2011 Atsugi-shi / Musashino-shi and shoji2002 Atsugi-shi as printed (D366); shoji2008
  blocks 1 / 2 print district names before Tokyo (locality Tokyo, districts only by type in the note, lit_h08 / h09 /
  h12 precedents); shoji2010 Tsukuba (prefecture not recorded).
- Empty fields: vlasov2004, xia2007, popovic2006 print a state and no country (`country: ""`, checked on the page);
  matsuo2013 (prefecture only) and pfeifle2012 (country only) `locality: ""`.
- Country names: thomson2007 Scotland -> GB (the checker's GB name list includes Scotland); its building name sits in
  `skip_between` (D380, verified, absent from every derived file).
- As printed: xia2007 "IBM Thomas J. Watson Research center"; yang2010 IMEC; vermeulen2010 imec; mcnab2003 /
  mauthe2020 Rueschlikon / Rüschlikon; mauthe2020 Empa with its full name as org.

## Privacy and as-printed scan

- No contact address, URL, ORCID id, phone number, street name, building name, postal code or box code in any field
  or note of `headers.yaml`, nor in `header_rows.csv`, `compare.csv` or `unmapped_orgs.csv`: 3+ digit runs occur only
  in paper codes and decision numbers (and the audit date in the mcnab2003 note). Notes name address parts only by type
  (street address, building number, industrial park name, district names, prefecture, postal designations, contact
  numbers, site names after N1). The only verbatim address-like span is thomson2007 `skip_between` (a building name,
  the D380 mechanism; never stored in derived files).
- This record: same scan (no street, building, site, postal, box or contact text).

## Commands (2026-10-30, log times)

| Command | Result |
|---|---|
| `check lit_h18 --corpus lit --dry-run` (before) 00:46:25 (log `lit_headers_check_lit_h18_67494_...`) | 0 errors, 2 warnings (pernice2012 slot 5, popovic2006 slot 7); slots 214, recorded 213, no_header 1, rows 242 (A 234, B 8), present addresses 1, 14 unmapped org strings; stamp matched headers.yaml (sha256 182387a5...) |
| probes (`--dry-run`) 00:52:40, 00:52:48, 00:53:01, 00:53:17, 00:53:24, 00:53:39 | pernice2012 without slot 5: 2 errors; popovic2006 without slot 7: 2 errors; mcnab2003 country US: 0 errors; yang2010 author 4 readable: 2 errors (no regular block) / status ok: 2 errors; pernice2012 dagger as marker: 6 errors. File restored and md5-verified after each |
| `check lit_h18 --corpus lit` 00:54:37 (log `lit_headers_check_lit_h18_80040_20261030T005437.log`) | 0 errors, 2 warnings; ok 34, partial 1, unreadable 0; rows 242 (grade A 234, B 8), recorded 213, no_header 1, present addresses 1; 14 unmapped org strings; stamp matches headers.yaml (sha256 1b506980...) |

`aggregate --corpus lit` not run (the coordinator runs it after the lit_h17 audit). Changes to `headers.yaml` (diff
against the backup): mcnab2003 block 1 `country` and note, vivien2009 note; nothing else. `header_rows.csv` changes
only in the 2 mcnab2003 rows of block 1 (country US); `compare.csv` and `unmapped_orgs.csv` byte-identical.

## Checker gaps observed (scripts not edited)

- Known: an author whose only printed marker is a present address cannot be recorded (yang2010; round-3 G4,
  keyvaninia2019).
- New, no error: a dagger extracted as the letter w in both layers (pernice2012, a Nature Communications page); the
  checker verifies the glyph, so the batch records "w". No other `references/*/text.md` shows the pattern.

## Open questions

1. pernice2012 present-address marker recorded as "w" (rendered dagger, extracted as w in both layers): accept as the
   verifiable printed token? Recommendation: accept (the marker is a link token, not stored as a fact).
2. piggott2015 #6 "Jelena Vuckovic A": add to the D412 author-list correction file (with white2022 / white2024)?
   Recommendation: yes.
3. yang2010 #4 Van Campenhout (present-address-only author): re-record with the IMEC present-address row once the
   checker accepts such authors (round-3 G4)? Recommendation: yes, in the checker follow-up pass with keyvaninia2019.
4. Dash-joined joint orgs (Ghent University - imec, IBM Research - Zurich): extend D416 (5) "kept as printed, alias in
   the org round" from campus forms to joint-org forms? Recommendation: yes (majority precedent; no re-work now).
