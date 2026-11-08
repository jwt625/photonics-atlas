---
title: Fresh-context audit of the lit author-affiliation batch lit_h28 (21 papers)
date: 2026-11-08
auditor: Claude (fresh context; wrote only this record; headers.yaml, derived files, scripts, tests, people and registry data not edited; aggregate and the people build not run; check run only with --dry-run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h28/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D406-D522); format from the 2026-11-06 h27 audit
verdict: GO for the people rebuild (no slot wrong); 186 slots audited, 181 ok, 5 imprecise, 0 wrong; F1 (note only) fixable now; F2 (4 slots, Hefei National Laboratory as a USTC unit) and F3 (1 slot, second block of the last author) wait on known checker gaps; nothing applied
---

# Lit header batch audit: lit_h28 (2026-11-08)

## Scope

Batch lit_h28 (21 papers: 1 Wiley grouped footnote, 1 IEEE prose footnote, 1 Nature consortium paper with the author
list at the end, 2 cover-page papers (ACS just-accepted, AIP), 16 Optica / Nature-family / preprint papers with printed
markers or a single block; 186 author-list slots plus 72 header-only authors; 245 rows). Restricted corpus: this record
names only authors, orgs, units, cities and countries; no paper text is quoted and no contact, street, building, campus
site or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h28 --corpus lit --codes <id> --pdf`
  (all 21; `--pages 8 8` for alexander2024, `--pages 2 2` for chen2018 and chung2019, whose blocks are on later pages).
  Output kept in the session scratchpad only.
- Per slot: printed name vs `compare.csv` slot, printed marker run vs `markers` + `dropped_markers`, prose subject vs
  carriers (babichev2025), group position (a2017), block fields vs the print (org, more_orgs, unit, campus, city,
  country), locator. alexander2024: all 101 printed names and marker runs compared programmatically with the YAML
  (only non-breaking-space differences).
- Dropped numeric markers checked against the first character of the masked contact lines in `text.md` (chen2025a 7 / 8,
  coratozanarella2026 4 / 5; chung2019 a) printed before the contact line). No contact text copied.
- Missed blocks: cue scan of the whole `text.md` of all 21 (now with / at, present / current address, current / present
  affiliation, currently, presently, also with, is / are / was / were with, on leave, visiting, formerly, deceased,
  permanent address). Only header hits: babichev2025 statements and clause (recorded). Other hits are a biography on a
  later page (babichev2025) and body text. No missed block.
- Author lists read from `cache/literature/merged.jsonl` for chen2019 #3 (name-form count across Baile Chen co-author
  records).
- Claims and the coordinator question tested with dry-run probes on a scratch copy of the batch (`probe.py`, module
  `LIT_BASE` pointed at the copy); md5 of every repo batch file asserted unchanged before and after.
- Stamp: `check_stamp.txt` matches `headers.yaml` (sha256 f4f1b548...). Repo batch files untouched by this audit.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h28 | 21 / 21 | 186 | 181 | 5 | 0 |

- Rows 245 (all grade A: printed 192, single 27, prose 16, grouped 10; primary 210, additional 35, present address 0);
  recorded 185, no_header 1 (alexander2024 #1, the collective name); papers ok 21, partial 0, unreadable 0;
  `author_list_differs` 1 (alexander2024, 72 header-only authors with `slot: 0`); `order_differs` false on all 186;
  22 unmapped org strings; 3 warnings (explicit slots: babichev2025 #2 #10, coratozanarella2026 #9).
- Per slot field: name 186 ok; markers 185 ok / 1 imprecise (chen2018 #6, second marker not recorded); blocks (org /
  unit / place) 182 ok / 4 imprecise (chen2026c #1 #3 #7 #12); locators 186 ok; prose 13 ok; present addresses: none
  printed in a header.
- Per paper (slots / rows): a2017 10 / 10; abediasl2015 2 / 2; alexander2024 30 / 31; babichev2025 13 / 16; beals2026
  7 / 9; bonneville2024 4 / 4; chen2016 12 / 12; chen2016a 11 / 12; chen2018 6 / 16; chen2019 5 / 7; chen2020 8 / 16;
  chen2025a 19 / 23; chen2026c 12 / 33; chung2019 7 / 8; coratozanarella2026 9 / 9; dagostino2015 7 / 7; dagostino2018
  4 / 4; dean2025 9 / 10; ding2013a 3 / 3; ding2014 4 / 6; douglass2018 4 / 7.

## Findings and proposed fixes (not applied)

| # | paper, slots | rating | evidence (locator) | proposed fix (exact YAML edit) |
|---|---|---|---|---|
| F1 | dean2025 (note only) | note imprecise, fields correct | p.1 header: the dagger after authors 1 and 2 has no printed legend in either text layer (the line after block 2 holds only a joining word, the star and the contact line). The note states an equal-contribution meaning that is not printed (h23 N1 yasui2026 precedent). Symbol marks need no entry (D286d) | `note`: "preprint; dagger marks equal contribution, the star the corresponding author; state and postal codes not recorded" -> "preprint; the dagger after authors 1 and 2 has no printed legend in either text layer (symbol, not an affiliation); the star points to the contact line; state and postal codes not recorded" |
| F2 | chen2026c #1 (Ruiyang Chen), #3 (Sanli Huang), #7 (Zhen Chen), #12 (Junqiu Liu), block 2 | imprecise (a separate org recorded inside a unit; nothing invented, the USTC row is right) | p.1 header: block 2 prints the School of Physical Sciences and Hefei National Laboratory joined by and, then University of Science and Technology of China, Hefei, China. Contract: two printed organizations in one block go to `org` + `more_orgs`, not `unit`; the corpus records Hefei National Laboratory as its own org in lit_h02, h04, h07, h10, h11, h21, h23, h24 (only lit_h03 qi2024 P8 has it as a USTC unit, already listed for the org round). Probe H1 (unit School only, HNL in `more_orgs`): 2 errors, unit and org not contiguous (the h27 G2 gap). Probe H2 (H1 + `skip_between: "and Hefei National Laboratory"`): 0 errors | after the G2 checker change (D522 re-record list, as spiga2016): block 2 `unit`: "School of Physical Sciences and Hefei National Laboratory" -> "School of Physical Sciences"; add `more_orgs: ["Hefei National Laboratory"]`. `note`: "block 2 prints the School of Physical Sciences and Hefei National Laboratory before the university (recorded as the unit chain as printed, as lit_h03 qi2024; org round)" -> "block 2 prints the School of Physical Sciences and Hefei National Laboratory before the university (school as unit, the laboratory as a further organization, as lit_h04 / h10 / h23)". Rows 33 -> 37. Option (a) of h27 question 1 (the `skip_between` of H2) gives the same rows now if the coordinator rules it |
| F3 | chen2018 #6 (Shaohua Yu) | imprecise (second block missing; first block correct) | p.2 header (cover page 1): both text layers print the dagger and the double dagger after the last author. Probe C1 (author 6 `markers: ["†", "‡"]`): 2 errors, printed markers differ (last-author marker window, D442 chen2024b, D461 dutta2025 #8). Note already states the gap | after the last-author window fix: author 6 `markers: ["†"]` -> `["†", "‡"]`; drop from `note` the sentence "author 6 prints both block markers but only the first is recorded: the checker window after the last author cuts the second symbol (checker gap, as chen2024b; re-record block 2 for author 6 after a fix);". Rows 16 -> 17 |

Any change to the YAML changes its hash: re-run `check lit_h28 --corpus lit` afterwards to refresh the stamp.

Points checked and correct:

- a2017 (Wiley): no markers in the author line; the first-page footnote prints three groups of titled abbreviated names,
  each above its block (7 authors / Zhejiang University research centre chain, 2 authors / Zhejiang University college,
  1 author / the Chinese University of Hong Kong). Grouped recording, names in group form without titles, all 10 slots
  matched. Probe A1 (S. Gao moved to G2): 4 errors (D368 position check), so the grouping is verified. Block 3 country
  HK correct (D249: Hong Kong printed as the place with S. A. R., China; probe K1 shows CN would also pass, so this is
  a contract call already made). Campus site in block 1 left out (probe A3 shows a `campus` would pass; h27 question 5
  ruling: same-city site, no campus). Slot 1 "Daoxin Dai A" is the known D412 artefact.
- alexander2024: page 1 prints only the collective name; page 8 prints 101 names with markers 1 / 1,2 and both blocks.
  Author list = collective name + the first 29 printed names, so slots 2-30 = printed 1-29 (Chia-Jung Chung = C. J.
  Chung; Josep M. Fargas Cabanillas = Josep Fargas, dropped second family name), slot 1 no_header (no person),
  printed 30-101 `slot: 0` (no unmatched slot left, D302). Country GB from the printed UK (accepted form). Locator
  `p.8 header`: probe L1 shows `p.8 affiliations` also passes; `header` is the stricter choice (the author line is
  searched from page 8, where it is printed). No person is created for slot 1 (no header rows, dropped at build).
- babichev2025: four statements plus one also-with clause; carriers match every subject (Mikhail Maximov in P2 and
  P3); P4 CIOMP with its CAS name as one org (contract example form), Bimberg centre as unit; P5 TU Berlin clause.
  Explicit slots: probe N2 shows Pikhtin (slot 8) auto-matches, so `slot: 8` is redundant but harmless; probe N1 shows
  Novikov needs `slot: 10` (I. I. vs Innokenty), see question 3.
- chen2025a dropped markers 7 / 8 and coratozanarella2026 4 / 5: the masked contact lines begin with exactly these
  markers; chung2019 a) is printed on the contact line. Correct as `contact footnote`.
- chen2018 block 2 (innovation center + Wuhan Research Institute as two orgs) and chen2026c block 1 (International
  Quantum Academy + the Futian SUSTech institute): two printed organizations, correct. The research institute name is
  printed without "and" and kept as printed.
- chen2020 WNLO + HUST with the school dropped (lit_h26 form, contract rule for a department between two orgs); probe
  W1 shows the HUST unit-chain form also passes (contract call; both forms exist in the corpus, h27 question 4).
- chung2019 `campus: "Austin"` for The University of Texas (D301, multi-campus system); ding2014 FOTON as org with CNRS
  and University of Rennes 1 in `more_orgs`, school dropped, UMR number not copied (D285, caillaud2021 form);
  douglass2018 block 1 state only (locality empty), CUDOS as a further org, block 2 centre as Fraunhofer unit.
- Footnote locators: a2017, babichev2025, chen2016 carry `p.1 footnote` on every block (the h27 F1 lesson is applied);
  cover pages chen2018 and chung2019 `p.2 header`.

## Lists (for the coordinator's existing files)

- D412 author-list correction file: a2017 #1 ("Daoxin Dai A", as wang2014 / bauters2013 / a2011 / a2013); alexander2024
  (collective entry as slot 1 and the list cut at 29 of 101 printed persons; 72 authors have no slot and no rows).
- D426 review list: chen2019 #3 (printed Jian Huang, list Jian Hua Huang; the upstream records with Baile Chen as
  co-author carry Jian Hua Huang 27 times and Jian Huang 3 times; dropped-syllable match, only candidate); babichev2025
  #10 (question 3).
- Org round: 22 unmapped strings (none wrong). Observation: Wuhan National Laboratory for Optoelectronics maps by
  alias to `org_huazhong_university_of_science_and_technology`, so chen2020 gives each of its 8 slots two rows with the
  same org id (WNLO + HUST more_orgs); the people build should not count them as two affiliations.

## Coordinator questions

1. a2017 `grouped` (D368) for a Wiley first-page footnote: is it right, and should it be the rule? Recommended: yes, it
   is the right layout, and yes as a layout rule, not a publisher rule. The page has no markers on the author line and
   prints each group of titled abbreviated names directly above its own block, which is the D368 definition; probe A1
   proves the checker binds each group to its block. Rule text (as D461 did for De Gruyter): "Wiley first-page footnote
   with no markers in the author line and author groups (academic titles not copied) above their blocks: `grouped`
   (D368), names in the group form, `locator: "p.1 footnote"`; an author printed in two groups carries both markers; a
   group continued on the next page takes that page's locator." Limits: older Wiley pages with printed numeric markers
   in the author line and numbered footnote blocks stay `printed` (lit_h29 halir2016 and lit_h31 ortegamonux2013, Laser
   Photonics Rev. 2016 / 2013, have that form; the grouped form appears from the 2017 a2017 page and lit_h31
   luquegonzalez2019, which is already recorded grouped). Probe A2 shows the checker also accepts the full author-line
   name in a group; keep the group form for consistency with lit_h31.
2. F2 chen2026c: wait for the G2 checker change (D522, as spiga2016), or rule h27 option (a) and apply with
   `skip_between` now (probe H2: 0 errors)? Recommended: wait (keeps `skip_between` to building / site / postal-box
   spans, D380 / D410); the USTC row is already right.
3. babichev2025 #10: printed Innokenty Novikov, list I. I. Novikov. Novikov is a common Russian family name, so D369
   read literally gives `slot: 0`; but the unexplained second initial is the patronymic, which East Slavic full-name forms
   never print, and the given name is rare and agrees. Recommended: keep `slot: 10`, put it on the D426 review list, and
   add to D369 that a patronymic initial in an East Slavic list form is not an unexplained initial (also covers #2
   Pirogov and #8 Pikhtin, recorded the same way).
4. Apply F1 now and put F2 / F3 on the re-record list?

## Privacy and as-printed scan

- `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv` and this record scanned for contact / URL
  patterns, digit runs of 4 or more, and street / building / road / campus words and the street, building and site
  names printed on the header pages. Result: no contact or URL text; digit runs are paper-id years and the stamp hash
  only; street / building words occur only in notes saying such text was not recorded; the a2017 note names the
  district before Hong Kong (D366 places a district in the note) and does not name the campus site.
- As printed (kept, correct): chung2019 "Electronical" in the unit; chen2016a Ghent University with the dash joined
  imec (D426); a2017 "the Chinese University of Hong Kong" with the lower-case article; chen2018 research-institute name
  without "and"; ding2013a "Kgs. Lyngby" and ding2014 "Kongens Lyngby" each as printed.
- No `skip_prefix` or `skip_between` in this batch.

## Commands (2026-11-08, log times)

| Command | Result |
|---|---|
| `check lit_h28 --corpus lit --dry-run` 12:07:44 (pid 16478) | 0 errors, 3 warnings (explicit slots); slots 186, recorded 185, no_header 1; rows 245 (grade A 245; printed 192, single 27, prose 16, grouped 10); papers ok 21; 22 unmapped org strings |
| `show lit_h28 --corpus lit --codes <id> --pdf [--pages]`, all 21 papers | headers and author lists read (scratchpad only) |
| `probe.py` on a scratch copy, dry-run | results below; repo batch files md5 unchanged |

| probe | change | result | reading |
|---|---|---|---|
| B0 | none | 0 errors, 3 warnings | baseline equals the repo check |
| A1 | a2017 S. Gao moved from G1 to G2 | 4 errors (D368 position) | grouping verified |
| A2 | a2017 D. Dai written as the author-line full name | 0 errors | either name form passes |
| A3 | a2017 block 1 with a campus field | 0 errors | contract call (h27 question 5) |
| K1 | a2017 block 3 country CN | 0 errors | contract call; HK per D249 |
| C1 | chen2018 author 6 with both markers | 2 errors, printed markers differ | F3 waits on the window fix |
| H1 | chen2026c block 2 school as unit, HNL in `more_orgs` | 2 errors, unit and org not contiguous | F2 blocked by G2 |
| H2 | H1 + `skip_between` naming the laboratory | 0 errors | question 2 option |
| L1 | alexander2024 locators `p.8 affiliations` | 0 errors | `p.8 header` kept (stricter) |
| N1 | babichev2025 Novikov without `slot` | 2 errors, matches 0 slots | explicit slot required (question 3) |
| N2 | babichev2025 Pikhtin without `slot` | 0 errors | `slot: 8` redundant |
| W1 | chen2020 HUST org with WNLO + school as unit | 0 errors | contract call, lit_h26 form kept |

## Verdict

GO. No slot carries a wrong person, org, city, country or marker, nothing is invented, no block is missed, and no
address or contact text is recorded. One note overstates an unprinted legend (F1, fixable now); 4 slots carry Hefei
National Laboratory inside the USTC unit (F2) and 1 slot lacks its second block (F3), both waiting on known checker
gaps and correct as far as recorded.
