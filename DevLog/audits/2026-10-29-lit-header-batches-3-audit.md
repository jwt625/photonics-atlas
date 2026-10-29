---
title: Fresh-context audit of the lit author-affiliation batches lit_h12..lit_h15 (82 papers)
date: 2026-10-29
auditor: Claude (fresh context; wrote only lit_h12..lit_h14/headers.yaml, the derived files the checker writes, org_requests.csv via aggregate, and this record)
scope: data/_staging/people/lit_headers/lit_h12..lit_h15/headers.yaml; both header contracts; DevLog-011 D350-D369, D380, D400, D406; D410 (postal box, read from the checker comment in scripts/ofc_headers.py: DevLog-011 has no D410 entry on 2026-10-29 03:25); previous audit 2026-10-29-lit-header-batches-2-audit.md
verdict: GO for the people rebuild after the fixes below (applied; check 0 errors in all four batches); 1 wrong and 15 imprecise slots in 451 audited (4 fixed); 6 notes named site names (made by-type); 2 notes stated false facts (corrected)
---

# Lit header batches audit, round 3 (2026-10-29)

## Scope

Batches lit_h12 (27 papers), lit_h13 (27), lit_h14 (27), lit_h15 (1): 82 papers, 667 author-list slots. Restricted
corpus: this record names only authors, orgs, units, cities and countries; no paper text is quoted and no contact,
street, postal or box code is copied.

## Method

- Every audited paper read with `uv run python scripts/ofc_headers.py show <batch> --corpus lit --codes <id>`, with
  `--pdf` for every printed-marker, per_author and unreadable paper. Three statements whose tail is masked in `show`
  (contact strip) were read in `references/<id>/text.md` with contacts masked on the terminal: shimizu2023 P1,
  sia2022 P3, theurer2020 P2.
- Selection (55 papers, 451 slots, 581 rows; covers every one of the 25 `no_header` slots):
  - (a) every explicit `slot:` override, `slot: 0`, `author_list_differs`, `slots_from_header` paper: hwang2017,
    li2023, lin2022, sotirova2024, tebeneva2024, ye2021, yulaev2024, cohen2024;
  - (b) all 16 prose papers: andreou2019, ashida2018, cohen2024, dangel2018, ding2017, fan2025, guerber2018,
    karki2019, kumar2024, munk2019, pommarede2017, shimizu2023, sia2022, theurer2020, verdier2017, wilmart2020;
  - (c) partial / unreadable: barwicz2017, cohen2024, keyvaninia2019, lischke2021a, theurer2020; present address
    morichetti2021; per_author de2020, slaby2022; the known items si2026, de2020, cohen2024, sia2022, fang2006;
  - (d) random sample of 16 of the 51 papers not in (a)-(c): `random.seed(20261029); random.sample(sorted(rest), 16)`
    = chen2025, desiatov2019, ding2026, ghosh2012a, hakobyan2025, hassan2020, hinumwagner2025, jiang2020, liu2026,
    lu2016a, maier2022, shang2017, sohn2018, stone2022, xie2016, zhang2017a;
  - (e) 8 targeted: liao2011 (name pattern G3), singaravelu2019 and skandalos2026 (multi-org Grenoble blocks),
    tiecke2015 (blocks without country), wang2026c (locality as printed), zheng2023 (all of lit_h15),
    gallacher2018 (building name), ding2019 (two-org Wuhan block).
- Per slot: slot-to-name assignment (D359, D369, D287, D302), markers and `dropped_markers` against the PDF view,
  block mapping, org / unit / more_orgs split, locality (first printed city as printed), country (printed), role,
  basis. Per prose statement: subject names vs carriers both ways, clauses, coverage.
- Name scan of all 642 recorded slot matches of the 4 batches (`compare.csv` list name vs printed name).
- Claims in notes and known items tested with dry-run probes (`check --dry-run` on a temporarily edited
  `headers.yaml`, file restored byte-identical, md5 asserted; helper in the session scratchpad).
- Privacy scan: every field value and note of the four `headers.yaml` (contact / URL / ORCID, 3+ digit runs and
  postal patterns, street words, site / building / box words); every value of the derived CSVs and
  `org_requests.csv`.
- Backup before any edit: `backup_lit_h12_h15_20261029T031233.zip` (four batch directories + `org_requests.csv`)
  in the session scratchpad `hdr_audit3/`.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h12 | 17 / 27 | 118 | 113 | 4 | 1 |
| lit_h13 | 17 / 27 | 162 | 161 | 1 | 0 |
| lit_h14 | 20 / 27 | 159 | 149 | 10 | 0 |
| lit_h15 | 1 / 1 | 12 | 12 | 0 | 0 |
| total | 55 / 82 | 451 | 435 | 15 | 1 |

- Fixed: 1 wrong (cohen2024 #1) + 3 imprecise (verdier2017 #1 #3 #4). Not fixable within the contract / checker:
  12 imprecise (fang2006 x3, sia2022 x2, stone2022 x4, cohen2024 #4, keyvaninia2019 #3, theurer2020 #13).
- The 25 `no_header` slots after the fixes: 18 in the two unreadable papers (barwicz2017 x5, lischke2021a x13; both
  correct under the rules), 3 list authors not printed in the cached preprint header (lin2022 #7 #8 #12), 1 `slot: 0`
  by D369 (li2023 #1 Zongkai vs Z. Y. Li), 3 checker gaps (cohen2024 #4, keyvaninia2019 #3, theurer2020 #13).
- Header-only authors (`slot: 0`): li2023 Zongkai Li, ye2021 Victor Torres-Company (not in the 5-name list): both correct.

## Rulings on slot overrides and known items

| paper, slot | printed vs list | ruling |
|---|---|---|
| hwang2017 #4 | Peter O'Brien (printed 7th) vs Peter A. O'Brien (list 4th) | keep `slot: 4` (one missing middle initial, distinctive; gradkowski2023 precedent); order differs (D363) |
| sotirova2024 #1, #3 | A. S. Sotirova vs Ana Sotirova; J. D. Leppard vs Jamie Leppard | keep (D369 distinctive family name, one extra initial; same positions) |
| tebeneva2024 #5 | IVAN A. KAPLUNOV vs Cyrillic-script form | keep (D287 transliteration, lahijani2026 precedent) |
| li2023 #1 | ZONGKAI LI vs Z. Y. Li | `slot: 0` correct (D369: Y not explained, common family name) |
| ye2021 | Victor Torres-Company printed, not in list | `slot: 0` correct |
| yulaev2024 | no author list | `slots_from_header` correct; header order = slots |
| si2026 #4 | YAN-QING LU vs Y. H. Lu | known D382: initials disagree but the checker matches it; probe with `slot: 0` gives the D302 error ("matches unmatched metadata slot(s) [4]"). Kept, flagged (open question 1) |
| de2020 #1 | Marc de Cea vs list "Marc de" | correct person (list artefact, family name cut); merge note (open question 4) |
| liao2011 #8 | Wei Qian vs Wei Ping Qian | auto-match, G3 pattern of the previous audit (dropped spelled syllable, common family name); flagged, no fix |

## Findings and fixes

| # | paper, slots | rating | evidence (locator) | fix (field: before -> after) |
|---|---|---|---|---|
| F1 | cohen2024 #1 (Lucas M. Cohen), P1 | wrong (no row) | p.1 footnote: statement 1 names L. M. Cohen; probe with the author readable and `status: ok` gives 0 errors (the note's "text layer does not split the first name" no longer holds with the current checker) | author 1 `unreadable: true` removed; `status: partial` -> `ok`; note rewritten (claim (1) removed; present-address org copied as printed "John Hopkins", was "Johns Hopkins"). +1 row (Purdue University) |
| F2 | verdier2017 #1 #3 #4 (Verdier, Brenot, Debregeas), P1 | imprecise | p.1 footnote: III-V Lab followed by a parenthetical description as a joint lab of Nokia, Thales and CEA-LETI; the same description in pommarede2017 records III-V lab alone, as lit_h05 / lit_h07 / lit_h09 / lit_h11 / lit_h12 brun2014; parent rule of the OFC contract and F2 of the previous audit | P1 `more_orgs: ["Nokia", "Thales", "CEA-LETI"]` -> removed; note updated. -9 rows; org request "Thales, Palaiseau, FR" gone |
| F3 | de2020 (note) | false note | p.1 header: author 6 (Rajeev J. Ram) and his block are printed in the text layer too | note: "author 6 and his block are printed in the PDF layer only" -> "the author list prints author 1 as Marc de (list artefact, matched to Marc de Cea)" |
| F4 | morichetti2021 (note) | false note | p.1 footnote: only blocks 1 and 2 plus the equal-contribution line 3 are printed; no block 4 | note clause "block 4 prints the unit after the organization" removed |
| F5 | brun2014, hassan2020, pommarede2017, singaravelu2019, skandalos2026, wilmart2020 (notes) | privacy rule | site names spelled out in notes (task rule: building / site names only inside skip_prefix / skip_between) | each site name replaced by "a site name" / "two site names"; no field changed |
| C1 | fang2006 #1 #2 #6 (Fang, Park, Bowers), block 1 | imprecise, not fixable | p.1 header: org, campus Santa Barbara, then the Department of Electrical and Computer Engineering; probe adding the unit: "marker + first field (unit or org) not printed" (md and pdf) | none (gap G1) |
| C2 | sia2022 #2 #11 (Xiang Li, Chongyang Liu), P3 | imprecise, not fixable | p.1 footnote: the laboratory name contains an at sign and is removed by the contact strip in both layers; the fragment before it sits in `skip_prefix` (not a building name); the NTU, Singapore row is true | none (gap G2) |
| C3 | stone2022 #1-#4, block 1 | imprecise, known | p.1 header: Joint Quantum Institute, NIST/University of Maryland, College Park; `MoreOrg` has no campus, so College Park is the locality of a plain University of Maryland row (previous audit C5 / G4); JQI with two more_orgs matches lit_h02 | none (G4; open question 2) |
| C4 | cohen2024 #4 (Navin B. Lingaraju) | imprecise, known (no row) | p.1 footnote: SRI International, Arlington, USA, then a present-address sentence (not a with statement); probe recording P3 (SRI): "role affiliation but the block has a present-address cue" (md, pdf), and the md subject check of P1 then fails for Cohen | none: author omitted, `author_list_differs` (gap G3) |
| C5 | keyvaninia2019 #3 (Markus Wössner) | imprecise, known (no row) | p.1 header: only marker 2 (Now with Robert Bosch GmbH, Stuttgart); probe readable: "has no markers and the paper has no unmarked block" + warning "only a present-address block" | none: `unreadable` kept (gap G4) |
| C6 | theurer2020 #13 (Rene G. Heideman), P2 | imprecise, known (no row) | p.1 footnote: name glued to "and" and the verb; probe readable: "not named in the statement subject" (md, pdf) | none (previous G5) |

Checked and correct (highlights): every prose statement of the 16 prose papers (subjects vs carriers both ways;
clause blocks andreou2019 P2, guerber2018 P2, shimizu2023 P3, wilmart2020 P3 / P5; "was with" wilmart2020 P4;
prefecture-only Ibaraki in ashida2018 with `locality: ""`; shimizu2023 P1 Yokosuka glued in the text layer);
per_author layouts (de2020, slaby2022; de2020 blocks print no country: "" correct); every `dropped_markers` entry
read in the PDF view (equal contribution, contact lines); present addresses (keyvaninia2019 block 2, morichetti2021
block 2); campus orgs (UC Berkeley, UC Davis, UCSB, UMD College Park in yulaev2024); HK for City University of Hong
Kong (desiatov2019, Kowloon) and HKUST (yang2014); blocks without a country ("" in de2020, stone2022, tiecke2015 #1
#2); locality as printed (brun2014 GRENOBLE, wang2026c KGS. Lyngby, ding2019 Kgs. Lyngby / Kongens Lyngby). The
unreadable claims hold: barwicz2017 is font-encoded (every glyph shifted) in both layers; lischke2021a prints its
four blocks as a footnote before the title and author line in both layers (D246 order).

Consistency observations (no fix): Wuhan National Laboratory for Optoelectronics with Huazhong University of Science
and Technology is two orgs in ding2019 (printed "WNLO, HUST", as the lit_h02 precedent) and a unit chain in li2026b
(printed "WNLO and School ..., HUST", as most precedents); both as printed (open question 3).

## Privacy and as-printed scan

- No contact address, URL, ORCID id, phone number, street name or postal code in any field or note of the four
  `headers.yaml` files, their derived CSVs (`header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`) or
  `org_requests.csv` (20365 CSV values scanned; only paper codes matched the digit pattern). Notes name address parts
  only by type ("street address ... not recorded", "a ward", "postal designation").
- Site names: 6 notes named them (F5); fixed to by-type. After the fix the only skip span in the four batches is
  sia2022 P3 `skip_prefix` (a laboratory-name fragment, not a building or site name; C2). No postal-box code
  (D410 `<postal box>`) occurs in these batches.
- As printed: cohen2024 note now copies the present-address org as printed (F1); benedikovic2015 "Telecommuncations",
  ghosh2012a "Keyvavinia" and the capitals author lines are as printed.

## Commands (2026-10-29, log times)

| Command | Result |
|---|---|
| `check lit_h12 .. lit_h15 --corpus lit --dry-run` (before) 03:12:51-03:13:16 | 0 errors, 5 warnings; slots 667, recorded 641, no_header 26, rows 852 |
| `check lit_h12 --corpus lit` 03:24:07 (log `lit_headers_check_lit_h12_90442_20261029T032407.log`) | 0 errors, 0 warnings; ok 26, partial 0, unreadable 1; rows 247 (was 246), recorded 182, no_header 6; 18 unmapped org strings |
| `check lit_h13 --corpus lit` 03:24:13 (log `lit_headers_check_lit_h13_90453_20261029T032413.log`) | 0 errors, 2 warnings (hwang2017 slot 4, order differs); rows 271, recorded 228, no_header 18; 26 unmapped |
| `check lit_h14 --corpus lit` 03:24:20 (log `lit_headers_check_lit_h14_90463_20261029T032420.log`) | 0 errors, 3 warnings (sotirova2024 x2, tebeneva2024 slot overrides); rows 312 (was 321), recorded 220, no_header 1; 26 unmapped (was 27) |
| `aggregate --corpus lit` 03:24:35 (log `lit_headers_aggregate_90501_20261029T032435.log`) | 252 org-request strings (was 253: "Thales, Palaiseau, FR" removed), 0 conflicts, 10 header-only authors |
| `check lit_h12 .. lit_h15 --corpus lit --dry-run` (after) 03:24:57 | 0 errors, 5 warnings; slots 667, recorded 642, no_header 25, rows 844 (all grade A), present addresses 2 |

lit_h15/headers.yaml is byte-identical to the backup (md5 checked); its stamp still matches. Probes ran as
`check --dry-run` (log files in `logs/`, derived files untouched; each probed file restored and md5-verified).

## Checker gaps observed (scripts not edited)

- G1 A unit printed after "org, campus" (fang2006 "University of California, Santa Barbara, Department ...") cannot be
  recorded: with a unit set, the first field searched after the marker is the unit.
- G2 Contact strip removes an org / unit name containing an at sign (sia2022: a laboratory name with an at sign); the extractor
  parked the fragment in `skip_prefix`, which is meant for building / complex names. Same family as previous G1.
- G3 A present-address sentence that is not a with statement ("His present address is ...") inside the 300-character
  window of the preceding block makes that block fail the cue check (cohen2024 SRI); with that block recorded, the md
  subject check of the first statement also changes (P1 Cohen fails), so the statement window / subject logic depends
  on later blocks.
- G4 An author whose only printed marker is a present address (keyvaninia2019 Wössner) cannot be recorded; the row
  for the present address is lost.
- G5 Blocks printed before the author line (Nature-style first-page footnote, lischke2021a: 13 slots) fail D246 order.
- G6 Font-encoded text layers (barwicz2017: constant glyph shift in text and PDF) are unreadable by design.
- Known: run-together statements (theurer2020, previous G5); spelled-syllable drop with a common family name
  (liao2011, previous G3); D382 initials (si2026); `MoreOrg` campus (stone2022, previous G4).

## Open questions

1. si2026 #4 Yan-Qing Lu matched to "Y. H. Lu": after D382, re-check and set `slot: 0` + `author_list_differs`?
2. Parents printed with a joint lab / institute: this audit dropped III-V Lab's parents in verdier2017 (parenthetical
   description, as pommarede2017); lit_h02 keyvaninia2013 still records them, and JQI keeps NIST / University of
   Maryland (stone2022, lit_h02). One rule for both?
3. Wuhan National Laboratory for Optoelectronics: two orgs (ding2019) vs HUST unit chain (li2026b and most): normalize?
4. Merge: list artefact "Marc de" (de2020 #1) as slot name; the printed form Marc de Cea should reach person_aliases.
5. sia2022 P3: accept the lab-name fragment in `skip_prefix`, or fix G2 and re-record with the laboratory as unit?
6. Re-record after checker fixes: cohen2024 #4 (G3), keyvaninia2019 #3 (G4), fang2006 unit (G1), lischke2021a (G5),
   theurer2020 #13.
7. DevLog-011 has no D410 row (postal box): only the checker comment documents it.
