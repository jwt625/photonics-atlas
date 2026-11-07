---
title: Fresh-context audit of the lit author-affiliation batch lit_h26 (23 papers)
date: 2026-11-06
auditor: Claude (fresh context; wrote only this record; headers.yaml, derived files, scripts, tests, people and registry data not edited; aggregate and the people build not run; no git, no network)
scope: data/_staging/people/lit_headers/lit_h26/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369, D400-D466; format and precedent from the 2026-11-06 h25 audit
verdict: GO for the people rebuild after F1 (marinins2022 can be recorded now; the checker already verifies it) and F2; 194 slots audited, 162 ok, 32 imprecise, 0 wrong; nothing applied
---

# Lit header batch audit: lit_h26 (2026-11-06)

## Scope

Batch lit_h26 (23 papers, 194 author-list slots, 233 rows). Restricted corpus: this record names only authors, orgs,
units, cities and countries; no paper text is quoted and no contact, street, building, site, district or postal text
is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h26 --corpus lit --codes <id> --pdf`
  (all 23; `--pages 2` for li2021 and manganelli2017, whose author lines and blocks are on page 2 after a cover).
- Rendered page crops (pdftoppm, session scratchpad, deleted after reading) where the text layers were in doubt:
  iadanza2024 author line and blocks (both text-layer copies unreliable), marinins2022 footnote of author 12, cabo2024
  footnote (accents).
- Per slot: printed name vs `compare.csv` slot (author-list position), printed marker run vs `markers` +
  `dropped_markers`, block fields vs the print (org, unit, campus, city, country), present address, parents,
  as-printed forms. All distinct (org, unit, place, role, org_ids) tuples of `header_rows.csv` read; no wrong mapping.
- Missed blocks: cue scan of the whole `text.md` of all 23 (now with / at, present / current address, current /
  present affiliation, currently, presently, also with, was / were with, on leave, visiting, formerly, deceased,
  permanent address). Header hits only in denicola2013 and hatori2014 (clauses, recorded) and marinins2022 (8
  statement hits, see F1); the other hits are biographies on page 11 of marinins2022. No missed block elsewhere.
- Claims tested with dry-run probes on a scratch copy (`probe.py`: copies the batch, patches the module's
  `LIT_BASE`, runs `cmd_check(dry_run=True)`; md5 of every repo batch file asserted unchanged after each run).
- Stamp: `check_stamp.txt` (22:40:17) matches `headers.yaml` (sha256 35ed8f59...; file 22:40:10). Derived files agree
  with the dry-run (rows 233, 17 unmapped strings).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h26 | 23 / 23 | 194 | 162 | 32 | 0 |

- Rows 233 (all grade A: printed 163, prose 42, grouped 15, single 13; primary 182, additional 51); recorded 168,
  no_header 26 (marinins2022 21, iadanza2024 4, jung2025 1); ok 20, partial 2, unreadable 1; present addresses 0;
  17 unmapped org strings; `order_differs` false on all 194 slots.
- Imprecise by cause: fixable now 25 (F1 marinins2022 21 slots; F2 cabo2024 4 slots); contract lookalike rule 5
  (C1 iadanza2024 #1 #2 #3 #4 #6); checker gap 2 (C2 jung2025 #2 #7).
- Per paper (slots / rows): akhlaghi2015 3 / 3; anthony2019 7 / 7; brunetta2026 7 / 7; cabo2024 7 / 15; cai2024 6 /
  18; denicola2013 14 / 17; dumais2016 11 / 11; hatori2014 9 / 18; iadanza2024 7 / 5; ji2026 11 / 20; jung2025 7 / 6;
  kandil2024 9 / 10; katsumi2018 5 / 7; kiewiet2026 11 / 18; kittlaus2018 5 / 5; krumrein2026 8 / 11; kumar2022a 7 /
  7; li2021 6 / 6; manganelli2017 8 / 12; marchetti2017 9 / 9; marinins2022 21 / 0; niffenegger2020 13 / 16;
  nikolai2025 3 / 5.

## Findings and proposed fixes (not applied)

| # | paper, slots | rating | evidence (locator) | proposed fix (field: before -> after) |
|---|---|---|---|---|
| F1 | marinins2022, all 21 slots | imprecise, fixable now (no rows; nothing wrong) | p.1 footnote, page render: the present-address statement of author 12 (Ozan Yilmaz) is printed in full and names Aeva Technologies, Mountain View, USA. Both text layers carry that line with its word spaces lost (one token run up to the contact address). `show` masks the whole non-space run around an at-sign, which takes the whole space-less line, so the extractor saw an empty statement. The checker does not: `_prep` removes only the address characters (D366), and the glued org, city and country are found by the normalized comparison. Probe M0 (pending record as is): 2 errors, D361 coverage at md and pdf. Probe M1 (pending record + this block): 0 errors, rows 233 -> 258, recorded 168 -> 189, present addresses 0 -> 4, unmapped strings 17 -> 21. Probe M2 (block without the author's marker): 3 errors (D354), so the block is bound to its subject. The 11 other statements of the pending record were checked against the page: correct | `status`: unreadable -> ok. `note` -> "affiliations printed as first-page footnote statements (prose); was with = affiliation of the work, He / She is now with = present address (authors 11, 12, 19, 20); the present-address line of author 12 is printed without word spaces in both text layers (read on the page; the checker verifies it)". Uncomment the pending record and renumber P6-P11 to P7-P12; insert after P5: `{marker: "P6", basis: prose, role: present_address, org: "Aeva Technologies", locality: "Mountain View", country: "US", locator: "p.1 footnote"}`; Ozan Yilmaz `markers: ["P5"]` -> `["P5", "P6"]`; Morthier `["P6"]` -> `["P7"]`, Smyth and McKee `["P7"]` -> `["P8"]`, Pantouvaki `["P8", "P9"]` -> `["P9", "P10"]`, La Tulipe `["P10", "P11"]` -> `["P11", "P12"]` |
| F2 | cabo2024 #3 #4 #5 #7 (Yang, Melati, Alonso-Ramos, González-Andrade), blocks G3 G4 G5 G7 | imprecise (form) | p.1 footnote render: the university is printed with its accent (Université Paris-Saclay); the text layers drop the letter's accent (D282: write the intended letters). Probe C2: 0 errors, rows unchanged (233); the string is unmapped in either form (all 65 committed lit rows of this university are unmapped) | G3, G4, G5, G7 `more_orgs`: ["CNRS", "Universite Paris-Saclay"] -> ["CNRS", "Université Paris-Saclay"] |
| C1 | iadanza2024 #1 #2 #3 #4 #6 | imprecise, not fixable under the contract (IBM rows missing; nothing wrong) | page render: author markers 1,2,3 / 1 / 1 / 1,2,3 / 4 / 1 / 2,3; block 1 IBM Research, Rüschlikon, Switzerland. The first text-layer copy is in a shifted font encoding with empty superscripts (`^{}` in the PDF view); the second (OCR) copy prints marker 1 of block 1 and of authors 3, 4, 6 as an apostrophe, and the second initial of author 3 as a zero. Lookalikes are not folded (contract): block 1 not recorded; author 2 carries only marker 1 (printed as a digit, but its block is not recorded) and is unreadable with 3, 4 and 6. Probe I1: Scherrer recorded with markers 2, 3 passes (0 errors: the checker ignores the apostrophe), so the rule is enforced only by the extractor; I2 (2, 3 + dropped 1) fails, as the OCR copy prints no 1 there | none now. Note correction N1. After an OCR re-extraction of page 1 (or a coordinator ruling allowing render reads for marker glyphs): block 1 `{marker: "1", basis: printed, org: "IBM Research", locality: "Rüschlikon", country: "CH"}`, authors 2, 3, 6 `["1"]`, authors 1 and 4 `["1", "2", "3"]` |
| C2 | jung2025 #2 (Gehring), #7 (Pernice, block b) | imprecise, checker gap (no row / one row missing) | p.1 header: block b (Institute of Physics and Center for Nanotechnology, University of Münster, Münster, Germany) begins with its unit glued to the letter marker in both layers. Probes JU2 / JU3: block b fails the block-start check at md and pdf (`_find_word` needs a word start before the unit; blocks a and c pass because their glued first word is the org, which is only searched backward from the unit). glued-letter-marker gap (lit_h16 audit G1, D416 (1)), recorded like lit_h16 chang2026a | after the glued-letter fix: add block b with that org, unit, `locality: "Münster"`, `country: "DE"`; Gehring `["b"]`; Pernice `["a", "b"]` without `dropped_markers`; status ok |
| N1 | iadanza2024 (note) | note imprecise (minor) | render: the zero replaces author 3's second initial (list form C. Oliver Martinez); author 2's own marker is printed as a digit | `note`: "author 3's given-name initial as a zero" -> "author 3's second initial as a zero"; after "authors 2, 3, 4 and 6 unreadable" add "(author 2 carries only marker 1)" |

Any change to the YAML changes its hash: re-run `check lit_h26 --corpus lit` afterwards to refresh the stamp.

## Extractor questions: recommendations

1. marinins2022 (coverage vs raw text): neither. The statement is not fully masked: it is printed on the page and the
   checker's own text keeps it (only `show` hides it, F1), and the checker passes the full record with it (probe M1).
   A coverage skip would let an author-naming statement drop without trace, which D361 exists to prevent (pilot audit
   mutations M12 / M13). Extractors should keep to `show` (contract: no other reads of the sources); the fix belongs
   in `show`: use the same address-only pattern as `_prep` (D366) in `mask()`, so `show` and the checker see the same
   text, then record as F1. Same family as the open gap "contact masking eating a glued place" (DevLog-011
   2026-10-29) and the run-together statements of cheung2022 / psaila2024 / liu2025a / naraine2024 / zhuang2025; unlike
   those, the subject and verb here are spaced and the checker already resolves it. If a statement is ever truly
   unrecoverable in every layer, decide then (a narrow, verified exemption naming the statement); none exists here.
2. ji2026 block 3 (Varian Semiconductor, Applied Materials): accept as recorded (org Applied Materials, unit Varian
   Semiconductor). The block prints the business unit first and the company after it, the structure of lit_h06
   (Bell Labs before Nokia: org Nokia, unit Bell Labs, audited) and ofc_h05 (Corning subsidiary recorded as unit of
   Corning Inc.). Probes J1 (two orgs) and J2 (Varian Semiconductor alone, parent dropped) also pass (0 errors), so this
   is a contract call; the recorded form maps 2 rows to `org_applied_materials` (registry name match), the alternatives
   would leave unmapped one-off strings.
3. (a) cabo2024 G1 / G6 (CSIC + unit Instituto de Óptica): accept as recorded; same institute, same co-authors and
   same form as lit_h06 gonzalezandrade2019 (org CSIC, unit Instituto de Óptica Daza de Valdés); maps to
   `org_consejo_superior_de_investigaciones_cientificas`. (b) denicola2013 P5 (National Research Council + unit
   Institute for Microelectronics and Microsystems): accept; lit_h19 alasio2024 (CNR + IEIIT) and lit_h24 (CNR +
   Istituto di Nanoscienze) record CNR institutes the same way. The row is unmapped by design: the bare English name is
   `no_name_match` (D275, `config/registry_corrections.yaml`), so it needs a lit-scoped alias in the org round, not a
   YAML change. Probes C1 / D1 (institute as org, council dropped) pass too (0 errors), so both are contract calls;
   the corpus is split (lit_h14 shoaa2025 and ofc_h11 record CSIC institutes as orgs; the registry has
   `org_instituto_de_optica_daza_de_valdes` with parent CSIC), see coordinator question 2. (c) nikolai2025 block 2
   (EPFL from the parenthesis): accept. The parenthesis is the only print of the parent and names EPFL; the same
   centre in ji2026 block 2 is printed with the full EPFL name and recorded as EPFL + unit, and iadanza2024 block 3 prints
   EPFL as a plain org; the recorded form gives the same `org_epfl` row. Probes N1 (one string with the parenthesis)
   and N2 (centre alone) pass but would create unmapped centre-as-org strings.
4. hatori2014 P5 (district only): `locality: ""` as recorded. D288 / D366: locality is the printed city; a district
   goes to the note; a block without a city gets an empty locality (lit_h25 maeda2024 Keio ward-only clause, lit_h02 /
   h17 Keio blocks, lit_h18 and lit_h14 district notes). Probe H1 (district as locality) passes (0 errors): the checker
   cannot tell a district from a city, so this is the ruling, not a checker result. The row still maps to
   `org_the_university_of_tokyo` with country JP.

## Reported gaps and flagged points

| paper | what the page shows | ruling |
|---|---|---|
| iadanza2024 | IEDM page with a font-garbled first copy and an OCR copy | C1; recorded rows (PSI and EPFL for authors 1 and 7, Glasgow for author 5) match the render; block 2 prints no city (`locality: ""`, D288) |
| jung2025 | glued letter markers | C2 (G1); umlaut transliterations in the list (ue / ae) take explicit slots 3, 4 (D287 transliteration variant), correct |
| 6 explicit-slot warnings | iadanza2024 #4 (M. A. vs Markus Scherrer), jung2025 #3 #4, niffenegger2020 #1 #6 #8 (middle initials R. J., C. D., R. T. not in the list) | all D287 / D369 cases on distinctive family names; probe S1 (Niffenegger slot removed): 2 errors, so the slots are needed; no change |
| li2021, manganelli2017 | IEEE Photonics Journal cover page 1 | `p.2 header` on every block (D366), correct |
| cai2024 | WNLO and a HUST school, then HUST | recorded as two orgs with the school dropped (D288), as lit_h02 and lit_h21 (footnote form); lit_h13 / h17 / h25 record HUST + unit chain; both map to the HUST id (existing alias), no row difference |

Other papers (all correct; recorded values match the print):

- Markers: every printed run matches `markers` + `dropped_markers` in the 15 papers with printed markers; symbol marks
  without a block ignored (brunetta2026, ji2026, kiewiet2026, krumrein2026, niffenegger2020, nikolai2025 asterisks /
  daggers; kandil2024's asterisk and dagger are block markers and recorded as such).
- Prose (anthony2019, denicola2013, hatori2014): every statement naming an author is recorded; clause blocks of
  denicola2013 (P4, P6) and hatori2014 (P2, P4, P6) correct; subjects match carriers; membership designations ignored.
- Grouped (cabo2024): De Gruyter footnote, one block per author in printed order, as yang2018 (D461).
- Places: kumar2022a no country printed (`country: ""`, D249); katsumi2018 ward not recorded, Tokyo kept; anthony2019, marchetti2017,
  marinins2022 (F1) and iadanza2024 print U.K. / United Kingdom (GB).
- As printed: krumrein2026 Max Planck Insitute (typo in the source) and the Ferdinand-Braun-Institut full name with
  its Leibniz subtitle as one org (as the dash-joined IHP name in earlier batches); kandil2024 Imec, kiewiet2026
  Ghent University - imec and kandil2024 Ghent University-Imec kept (D416 (5), D426); manganelli2017 site name after
  CEA LETI and the city after the school name not copied; denicola2013 office names joined to Oclaro North America
  Inc. and CGS S.p.A. by a hyphen recorded as units (probe S2: dropping them also passes; kept, as the print names
  the office as part of the employer designation), MIST E-R in full with its acronym (P1) and as the acronym (P4,
  P6).
- Name matches: initials, dropped middle names, joined syllables (Jie Yun / Jieyun, Kai Xin / Kaixin), detached
  accents (brunetta2026), De Nicola / DeNicola; no match by position.

Unmapped org strings (17): not errors, for the org round. CGS S.p.A., Ferdinand-Braun-Institut gGmbH (full name),
Humboldt-Universität zu Berlin, Institute for Photonics-Electronics Convergence System Technology (PECST), MIST E-R
(two forms), Leibniz-Institute of Surface Engineering (IOM), Linköping University, Max Planck Insitute for Solid State
Research, McMaster University, National Research Council (CNR, D275), Oclaro North America Inc., Paul Scherrer
Institut, Universidad de Málaga, Universite Paris-Saclay (F2), University of Glasgow, University of Manchester. With F1:
4 more (21).

## Privacy and as-printed scan

- `privscan.py` (session scratchpad) over every line of `headers.yaml`, `header_rows.csv`, `compare.csv`,
  `unmapped_orgs.csv`, `papers.csv` and this record: at-sign, URL, mail-word, phone-like and street-word patterns,
  digit runs of 4 or more, and 49 postal, street and district strings taken from the header pages of all 23 papers.
  Result: 0 contact, URL or phone hits; 0 printed postal or street strings. Street-word hits: 8, all the word in
  notes that say a street address is not recorded. Digit runs: years in paper ids and notes only (in this record also
  the stamp prefix, log pids and dates). One district name appears in the hatori2014 note (as lit_h10's note names a
  district); not in this record.
- No `skip_prefix` or `skip_between` in this batch.

## Commands (2026-11-06, log times)

| Command | Result |
|---|---|
| `show lit_h26 --corpus lit --codes <id> --pdf` for all 23 (+ `--pages 2` for li2021, manganelli2017) | read |
| `check lit_h26 --corpus lit --dry-run` 22:42:43 (pid 17680) | 0 errors, 6 warnings (explicit slots); slots 194, recorded 168, no_header 26; rows 233; ok 20, partial 2, unreadable 1; 17 unmapped |
| `probe.py variants.json` 22:51-22:53 (pid 25390) | results below; repo batch md5 unchanged |
| `probe.py variants2.json` 22:53 (pid 26792) | results below; repo batch md5 unchanged |
| `privscan.py` over the 5 batch files and this record | 0 contact, 0 postal / street strings |

| probe | change | result | reading |
|---|---|---|---|
| M0 | marinins2022 pending record as is | 2 errors (D361 coverage, md + pdf) | the extractor's failure reproduced |
| M1 | M0 + P6 Aeva Technologies present address | 0 errors; rows 258 | F1 |
| M2 | M1 without P6 on Yilmaz | 3 errors (D354) | block bound to its subject |
| J1 / J2 | ji2026 Varian Semiconductor as org (+ / - Applied Materials) | 0 / 0 errors | question 2 is a contract call |
| H1 | hatori2014 P5 locality = district | 0 errors | question 4 is a ruling |
| C1 / D1 | cabo2024 / denicola2013 institute as org, council dropped | 0 / 0 errors | question 3 (a), (b) are contract calls |
| C2 | cabo2024 Université Paris-Saclay | 0 errors, rows 233 | F2 |
| N1 / N2 | nikolai2025 centre with / without the parenthesis as org | 0 / 0 errors | question 3 (c) is a contract call |
| JU2 / JU3 | jung2025 block b (unit first / org only) | 5 errors each (block b start at md + pdf; md author line) | C2 confirmed |
| I1 / I2 | iadanza2024 Scherrer 2, 3 (without / with dropped 1) | 0 / 2 errors | C1: lookalike not caught by the checker |
| S1 | niffenegger2020 slot 1 removed | 2 errors (D247) | explicit slot needed |
| S2 | denicola2013 Oclaro office unit dropped | 0 errors | kept as recorded |

## Checker gaps observed (scripts not edited)

- G1 `show` masking (`mask()`, whole non-space run around an at-sign) is wider than the checker's (`_prep`, D366): a line whose words run
  together into the contact address disappears from `show` but not from the checker (marinins2022, F1).
- G2 Glued letter marker before a unit-first block (lit_h16 audit G1, D416 (1)): jung2025 block b (probes JU2 / JU3).
- G3 Lookalike marker glyphs are not detected: an apostrophe in a marker run is skipped, so a recorded subset passes
  (iadanza2024, probe I1); the contract rule rests on the extractor.
- G4 (minor) D369 joined-letter rule accepts a Western given name for two initials by an inner letter (niffenegger2020
  J. M. Sage ~ Jeremy Sage, matched without an explicit slot). The match is the same person here (distinctive family
  name); the rule is looser than the D287 explicit-slot path.
- G5 (minor) The md author-line errors in JU2 (authors after Gehring) appear only when the pdf layer also fails, i.e.
  latent md errors are suppressed whenever the other layer passes; expected (`check_provenance` takes either layer),
  noted so a later re-record of jung2025 is not confused by them.

## Coordinator questions

1. Apply F1 (marinins2022 recorded, rows 233 -> 258), F2 and N1 now, then re-run `check lit_h26 --corpus lit`?
   Recommended: yes, before `aggregate`. Optionally first change `show`'s `mask()` to the `_prep` pattern (G1) so the
   record can be reproduced from `show`.
2. National research council institutes (CSIC, CNR): keep the lit form "council as org + institute as unit" (lit_h06,
   h19, h24, h26) as the rule, with lit_h14 shoaa2025 (institute as org, CSIC dropped) as the outlier for the D412 /
   org-round normalization? Recommended: yes; it maps without new aliases except the D275 CNR alias.
3. Re-record list after checker fixes: jung2025 block b (glued-letter gap, D416 (1)) and iadanza2024 block 1 (needs a readable
   marker source; an OCR re-run of page 1 or a ruling on render reads).

## Verdict

GO. No slot carries a wrong person, org, unit, city, country or marker, nothing is invented, and no address or contact
text is recorded. marinins2022 is recordable now (F1, 21 slots, 25 rows, verified by the checker), and 4 slots should
take the printed accent (F2); 7 slots wait on the lookalike rule (C1) or a known checker gap (C2) and are correct as
far as recorded.
