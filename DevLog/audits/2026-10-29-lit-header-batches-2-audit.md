---
title: Fresh-context audit of the lit author-affiliation batches lit_h05..lit_h11 (183 papers) before the people rebuild
date: 2026-10-29
auditor: Claude (fresh context; wrote only lit_h11/headers.yaml, the derived files the checker writes, and this record)
scope: data/_staging/people/lit_headers/lit_h05..lit_h11/headers.yaml; both header contracts; DevLog-011 D350-D369, D380, D400, D406
verdict: GO for the people rebuild after the 3 fixes below (applied, check 0 errors); 1 wrong and 13 imprecise slots in 936 audited; 1 privacy item (postal-box code in a skip_between) not removable without a checker change
---

# Lit header batches audit, round 2 (2026-10-29)

## Scope

Batches lit_h05..lit_h11: 183 papers (the queue had 184; lee2022 was removed from lit_h07 before extraction, DevLog-011
progress 2026-10-29 01:27), 1526 author-list slots. Restricted corpus: this record names only authors, orgs, units,
cities and countries; no paper text is quoted and no contact, street, postal or box code is copied.

## Method

- Every paper was read with `uv run python scripts/ofc_headers.py show <batch> --corpus lit --codes <id> [--pdf]`
  (`--pages N` for page-N locators). Two masked spans were checked against `references/<id>/text.md` with contacts
  masked on the terminal (boust2020, notaros2019; finding C1).
- Selection (106 papers, 936 slots, 1144 rows; every one of the 61 `no_header` slots is in it):
  - (a) every explicit `slot:` override, `slot: 0`, `author_list_differs` and `slots_from_header` paper (21 papers);
  - (b) the automatic matches flagged by the extractors: tian2023, uddin2023, vandekerckhove2025, wang2014;
  - (c) all 51 papers with prose blocks, the 3 papers with printed present addresses (dostart2020, rao2019,
    winkler2024), the 3 unreadable papers (cheung2022, morenopozas2025, ryf2002);
  - (d) a random sample of 26 further papers, `random.seed(20261029)` over the 106 papers not in (a)-(c), plus 3
    targeted (mitchell2026 skip_between, lucia2026 order differs, fang2021 grouped). Sample: chen2024a, dirani2019,
    dong2010, gebregiorgis2023, han2015, he2026, huang2018, huang2019, hulyal2025, juvert2018, lischke2020, liu2020,
    mikkelsen2018, morin2021, nauriyal2019, ou2021, rasel2026, seok2016, stanton2017, teng2009, tyler2019, vivien2012,
    wang2016, wang2023c, wang2026b, zali2026.
- Per slot: slot-to-name assignment (D359, D369, D287, D302), markers and `dropped_markers` against the PDF view,
  block mapping, org / unit / more_orgs split, locality (first printed city, as printed), country (printed), role,
  basis. Per prose statement: subject names vs carriers in both directions, clauses, was / is now / pronoun
  statements, coverage.
- Name scan of all 1465 recorded slot matches in the 7 batches (`compare.csv` meta vs header name) for dropped
  full given-name parts, initials and swapped orders.
- Privacy scan of all seven `headers.yaml` (structured: every field value; raw: contact / URL / ORCID patterns) and of
  every derived CSV (`header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`) and `org_requests.csv`.
- Backup before any edit: zip of the seven batch directories and `org_requests.csv` in the session scratchpad.

## Counts

| batch | papers audited | slots | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h05 | 12 | 102 | 100 | 2 | 0 |
| lit_h06 | 17 | 157 | 157 | 0 | 0 |
| lit_h07 | 16 | 117 | 117 | 0 | 0 |
| lit_h08 | 20 | 204 | 203 | 1 | 0 |
| lit_h09 | 12 | 113 | 107 | 6 | 0 |
| lit_h10 | 18 | 163 | 163 | 0 | 0 |
| lit_h11 | 11 | 80 | 75 | 4 | 1 |
| total | 106 | 936 | 922 | 13 | 1 |

- Fixed in this audit: 1 wrong + 4 imprecise slots (F1-F3). Not fixable within the contract / checker: 9 imprecise
  slots (C1-C5).
- The 61 slots without rows are all correct under the rules: 38 nothing printed or no assignment printed
  (morenopozas2025 x8, ryf2002 x30), 5 list authors not printed in the cached header (dietrich2018 #11, lapointe2025
  #3, maiti2020 #6 #8, zhu2024 #9), 3 `slot: 0` by D287 / D369 (gao2026 #5 C L Zhang vs Chicheng; ishii2003 #4 Yukio
  vs Yasuhiro Ando; zhang2025 #3 Xianming vs XIE WU), and 15 run-together statements the checker cannot read
  (cheung2022 x9, psaila2024 #1-#3, liu2025a #4 #9, naraine2024 #17; checker gap G5).

## Rulings on slot overrides (task 1a)

| paper, slot | printed vs list | ruling |
|---|---|---|
| bogaerts2007a #6 | Elroy Pluk vs E.G.C. Pluk | keep `slot: 6` (see below) |
| ma2021 #7 | Jos van der Tol vs J.J.G.M. van der Tol | keep `slot: 7` (same class as Pluk) |
| winkler2024 #10 | Peter J. M. van der Slot vs Petrus J.M. van der Slot | was `slot: 0` (wrong): set `slot: 10` (F1) |
| cai2021 #5 | Tieyin vs Tieying Li | keep: one-letter typo, same position, only Li with a T given name |
| gao2026 #12 | Ziwen Zhou vs Zhou Z | keep: swapped order + initial |
| gao2026 #5 | Chicheng Zhang vs C L Zhang | `slot: 0` correct (D369, common family name) |
| gradkowski2023 #2, #6 | David Stegall vs D. B. Stegall; Peter O'Brien vs Peter A. O'Brien | keep: one missing middle initial |
| he2019 #6 | Marko Loncar vs Lončar Marko | keep: swapped order |
| kopp2023 #4 | DANIEL vs Dan Neugroschl | keep: D287 nickname, distinctive family name |
| korcek2023 #2 | David Medina Quiroz vs David E. Medina-Quiroz | keep: one missing initial + hyphen |
| lahijani2026 #5 | Konstantinos Tsoukalas vs Greek-script form | keep: D287 transliteration |
| liu2025 #7 | SERGEY MIKHRIN vs S. S. Mikhrin | keep: one extra initial, distinctive |
| loi2019 #10, lu2016 #9 | O'Callaghan / O'Brien with typographic apostrophe, one missing initial | keep |
| starnault2024 #3 | Gutiérrez-Castrejn (letter lost in text and PDF layer) vs R. Gutiérrez-Castrejón | keep: the lost glyph cannot be typed back (checker name check), slot needed |
| ishii2003 #4, zhang2025 #3 | different given names | `slot: 0` correct (D287) |

Pluk and van der Tol: the rows are kept. Reasons: D287 (binding for lit through the OFC contract) allows name-part
variants, with the OFC precedent M.R.A. Hassan -> Rosdi Hassan dropping more than one part; D369 restricts matches
through the initials rule, whose stated purpose is common family names (Yu, Deng, Lu); the first initial agrees, the
family name is distinctive and unique in the list, and the printed position equals the list position. The checker
itself accepts several unprinted middle initials whenever the list spells the first name (ma2021 Sander Reniers ~
Sander F. G. Reniers, maiti2020 S.D. Solares ~ Santiago De Jesus Solares, winkler2024 Ronald Dekker ~ Ronald Haentjens
Dekker); reading D369 as "exactly one" initial would make the outcome depend on whether the list spells the first
name, not on the identity evidence. Owner confirmation requested (open question 1); reverting is two one-line edits
(`slot: 0` + `author_list_differs`).

Automatic matches (task 1b):

- tian2023 #4 K. Williams ~ K.A. Williams: ok. Both forms are initials, the printed one has no initial that the list
  contradicts; one Williams in the list, same position. Not the D382 pattern (an extra initial unexplained by a
  spelled given name).
- vandekerckhove2025 #7 Neha Singh ~ Neha Chiruvolu Singh: ok (D247 dropped middle / second family name; one Singh).
- wang2014 #5 Daoxin Dai ~ list "Daoxin Dai A": ok; the trailing "A" is a list artefact (also bauters2013 #3). Merge
  note: the slot name comes from the list (D359), so check that the people parser does not take "A" as the family name.
- uddin2023 #4 Zi Wang ~ Zi Xin Wang: ok under the implemented rules, flagged. The list spells a two-syllable given
  name and the print drops a full syllable, with a common family name. The same pattern: dong2010 #2 Wei Qian ~ Wei
  Ping Qian, li2024a #9 LI DENG ~ Li Fei Deng, oh2023 #2 Jun Yang ~ Jun Mo Yang. D369 handles this only when one form
  is abbreviated (H T Deng vs Hao Deng -> slot 0); for two spelled forms `compatible` drops the syllable as a middle
  name and D302 then rejects `slot: 0` (probe: setting uddin2023 Zi Wang to `slot: 0` gives the D302 error). All 4 are
  at the printed position; no fix possible without a checker rule (open question 2, gap G3).

## Findings and fixes

| # | paper, slots | rating | evidence (locator) | fix |
|---|---|---|---|---|
| F1 | winkler2024 #10 (Peter J. M. van der Slot) | wrong (no row) | p.1 header: marker 1 (University of Twente); list Petrus J.M., initials P. J. M. agree, distinctive family name, same position | `slot: 0` -> `slot: 10`; `author_list_differs: true` removed (all 12 list authors printed); note updated. +1 row (University of Twente) |
| F2 | zhang2023d #8-#10 (Gocalinska, Pelucchi, Corbett), P6 | imprecise | p.1 footnote: statement prints Tyndall National Institute, then the parent University College Cork with a comma before Cork | `more_orgs: ["University College"]` removed (parent not copied, as in loi2019 and gradkowski2023); note updated. -3 unmapped rows with the org string "University College" |
| F3 | zhang2025 #1 (Xiaoyan Zhang), block 1 | imprecise | p.1 header: block 1 prints the city misspelled (Singpore) before the country | `locality: "Singapore"` -> `"Singpore"` (as printed, D366 / D288); note updated; note slip "author 4 printed as XIE WU" -> "author 3" |
| C1 | boust2020 #2 #8 (El Dirani, Kerdiles), P4 | imprecise, not fixable | p.1 footnote: the paper prints Grenoble and France glued to the contact parenthesis; the checker's contact strip removes the place with the contact, so P4 is recorded org-only (CEA-LETI, no city / country) | checker gap G1 |
| C2 | notaros2019 #9 #10 (Baiocco, Fahrenkopf), P9 | imprecise, not fixable | p.1 footnote: state, postcode and country glued to the contact parenthesis, removed by the contact strip; recorded country "" | checker gap G1 |
| C3 | ozdemir2021 #1 #6 (Ozdemir, Van Thourhout), P1; #4 (Kuznetsova) | imprecise, known | P1 country hyphenated across a line break (recorded ""); Kuznetsova's "and is now with" present address (KU Leuven) not recordable | checker gaps G6 (reported by the extractor) |
| C4 | liu2022a #1 (Li Liu) | imprecise, known | the fourth of five affiliations (a state key laboratory at Hunan University, Changsha) lies beyond the 300-character statement window | checker gap G6 |
| C5 | rao2019 #1 (Ashutosh Rao), block 3 | imprecise | present-address block prints NIST and University of Maryland, College Park; `MoreOrg` has no campus field, so College Park is stored as the locality of a plain "University of Maryland" row (the D301 campus rule cannot apply) | checker gap G4 |

Checked and correct (highlights): all 51 prose papers (subjects vs carriers both ways, 28 clause blocks, 13 prose
present addresses incl. pronoun statements in boust2020, davenport2016, fard2021, loi2019, notaros2019, song2024a, testa2018,
zhang2023d; "was / were with" as affiliation; on-leave notes not recorded in matsumoto2018 and taddei2019; the
ma2018 `skip_between` and the mitchell2026 `skip_between` are building names); grouped / per_author layouts
(bogaerts2007a, fang2021, hulyal2025, lapointe2025); page-2 header (liu2020); campus orgs (UCSB, Berkeley, Boulder,
UCSD with locality La Jolla, Maryland College Park, Texas Austin); HK for City University of Hong Kong and CUHK; AE
for UAE; ward-only and prefecture-only blocks with `locality: ""` (matsumoto2018, abe2025, ishii2003); every
`dropped_markers` entry (equal contribution, contact lines) matches the PDF marker run. The unreadable claims hold:
morenopozas2025 prints no affiliation anywhere in the cached text; ryf2002 prints 57 names over two orgs with no
grouping; cheung2022 prints one all-author statement with no word spaces (G5).

## Privacy and as-printed scan (task 2)

- No contact address, URL, ORCID id, phone number, street name or postal code in any field or note of the seven
  `headers.yaml` files, in their derived CSVs, or in `org_requests.csv`. Notes mention address parts only by type
  ("street address ... not recorded"); lapointe2025 names an ORCID link by type only.
- Building / site names: only inside `skip_between` (ma2018 x2, mitchell2026), never in a derived row. Unit
  "University Science Park" (korcek2023 #8) is an organizational unit of the University of Zilina, kept.
- vandekerckhove2025 block 3 (`skip_between` holds a postal-box code): NOT removed. Probes (dry-run, file restored
  byte-identical afterwards, md5 checked): without `skip_between` the checker reports "unit and org are not one
  contiguous printed segment"; recording the block without the unit (org only) fails "marker + first field not
  printed", because the marker precedes the unit. `org` is required, and the unit-org gap allows only letters, so any
  span that passes must contain the box number. A contract-conforming, checker-passing recording without the code does
  not exist with the current checker; recording the unit as an org or moving marker 3 to `dropped_markers` would
  misstate the paper. The code is in staging only and never in a derived row. Needs a checker change (G2) or an owner
  ruling (open question 3).
- zhang2025 locality: fixed to the printed form (F3).

## Commands (2026-10-29, log times)

| Command | Result |
|---|---|
| `check lit_h05 .. lit_h11 --corpus lit --dry-run` (before) 02:37 | 0 errors, 17 warnings; rows 1911, recorded 1464, no_header 62 |
| `check lit_h11 --corpus lit` 02:53:29 (log `lit_headers_check_lit_h11_81436_20261029T025323.log`) | 0 errors, 1 warning (winkler2024 slot 10); lit_h11 rows 201 (was 203), recorded 167, no_header 2, unmapped org strings 10 |
| `aggregate --corpus lit` 02:53:36 (log `lit_headers_aggregate_81529_20261029T025335.log`) | 198 org-request strings (was 199), 0 conflicts, 8 header-only authors (was 9) |
| `check lit_h05 .. lit_h11 --corpus lit --dry-run` (after) 02:53:48 | 0 errors, 18 warnings; slots 1526, recorded 1465, no_header 61, rows 1909 (all grade A) |

Only lit_h11/headers.yaml changed (lit_h05..lit_h10 byte-identical to the backup; their stamps still match).

## Checker gaps observed (scripts not edited)

- G1 Contact strip removes a place glued to the contact parenthesis (no space before it): boust2020 P4, notaros2019
  P9 lose city / country. Fix: stop the strip at the opening parenthesis / cue word, then re-record both blocks.
- G2 `skip_between` is the only way past a postal-box designation between unit and org, and it stores the code
  (vandekerckhove2025). Fix: a verified boolean (e.g. a box / CP / BP / P.O. Box pattern tolerated in the unit-org gap
  without storing it), or let `skip_between` accept the designation word with the digits matched by pattern.
- G3 Full-form given-name syllable dropped with a common family name is auto-matched and `slot: 0` is then rejected by
  D302 (uddin2023, dong2010, li2024a, oh2023): extend D382 / `strict_compatible` to spelled pinyin forms.
- G4 `MoreOrg` has no `campus`; rao2019 stores College Park as locality of a parent-level University of Maryland row.
- G5 Statements printed without word spaces (cheung2022, liu2025a, naraine2024, psaila2024): 15 slots without rows.
- G6 Known from the extraction: "and is now with" clauses (ishii2003, ozdemir2021), plain ", with" clauses and the
  300-character window (liu2022a), hyphenated country across a line break (ozdemir2021).
- G7 No rule rejects a parent fragment in `more_orgs` (zhang2023d "University College"); the OFC parent rule is
  enforced by review only.
- G8 A glyph lost in both layers (starnault2024 Castrejón) can only be handled by typing the name as extracted plus an
  explicit slot; D282 covers detached accents only.

## Open questions

1. D369 wording: confirm that a distinctive family name may take an explicit slot when the list has several initials
   the print omits (Pluk, van der Tol kept), i.e. "missing middle initial(s)".
2. Spelled given names with a dropped syllable and a common family name (4 slots above): keep (current rules) or
   `slot: 0` after a D382 checker extension?
3. vandekerckhove2025 postal-box code in `skip_between`: accept in staging or change the checker (G2)?
4. Re-record boust2020 P4 and notaros2019 P9 with city / country after a G1 fix.
5. Run-together statements (G5, 15 slots, incl. all of cheung2022): checker support or leave without rows?
6. Merge: list name artefact "Daoxin Dai A" (wang2014 #5, bauters2013 #3) as slot name.
