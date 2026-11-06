---
title: Fresh-context audit of the lit author-affiliation batch lit_h24 (28 papers)
date: 2026-11-06
auditor: Claude (fresh context; wrote only this record; headers.yaml, derived files, scripts, tests, people and registry data not edited; aggregate and the people build not run; no git, no network)
scope: data/_staging/people/lit_headers/lit_h24/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369, D380, D400-D449; format and precedent from audits 2026-11-04 h22 / h23
verdict: GO for the people rebuild after F1-F3 (or GO as is, since no row is wrong); 204 slots audited, 178 ok, 26 imprecise, 0 wrong; 3 fixable findings (F1-F3, 20 slots, field changes only), 6 slots imprecise from checker gaps (no fix in the YAML now), 2 note corrections; nothing applied
---

# Lit header batch audit: lit_h24 (2026-11-06)

## Scope

Batch lit_h24 (28 papers, 204 author-list slots, 286 rows). Restricted corpus: this record names only authors, orgs,
units, cities and countries; no paper text is quoted and no contact, street, building or postal text is copied.

## Method

- Every paper read with `uv run --offline python scripts/ofc_headers.py show lit_h24 --corpus lit --codes <id> --pdf`
  (all 28). Extractor notes and the five questions treated as claims to test.
- Rendered page 1 of all 28 PDFs (only 7 have a `figures/page_01.png`) to the session scratchpad and looked at the
  header / footnote crops where markers, layout or spacing were in question: dutta2025 (author 8 run), franken2025
  (block 2 place), yanikgonul2021 (6 printed names), li2025a, govdeli2025, perezgalacho2017, zhao2025a (marker runs),
  zhou2025a (footnote spacing). Renders deleted after reading.
- Per slot: printed name vs `compare.csv` slot, printed marker run vs `markers` + `dropped_markers`, block fields vs the
  print (org, unit, campus, city, country), present address, parents, as-printed forms. All 70 (org, id, match basis,
  country) triples of `header_rows.csv` read; no wrong mapping.
- Missed blocks: cue scan of the whole `text.md` of all 28 (present / current address, currently at / with, present
  affiliation, now at / with, also with, permanent address, on leave, visiting, deceased, formerly). Hits: miller2017
  block 5 (recorded as present address) and the zhou2025a clauses (see question 5); one body-text hit in ji2024. No
  missed block.
- Claims tested with dry-run probes on a scratch copy of the batch (`probe.py`, `probe2.py` via the module's
  `LIT_BASE`; md5 of the repo `headers.yaml` asserted unchanged after each script). `probe2.py` ran `cmd_check` without
  dry-run on the scratch copy only, to read the rows the F1 / F3 changes would derive; its derived files were written to
  and deleted with the scratch directory. Each probe left a log in the git-ignored `logs/`.
- Stamp: `check_stamp.txt` matches `headers.yaml` (sha256 4f48dff7...). Repo batch files untouched by this audit
  (mtimes 01:30 / 01:31, before the audit's first command).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h24 | 28 / 28 | 204 | 178 | 26 | 0 |

- Rows 286 (all grade A: printed 254, prose 11, single 12, grouped 9); recorded 200, no_header 4; ok 27, partial 0,
  unreadable 1 (zhou2025a); present addresses 1 (miller2017 #5); 17 unmapped org strings.
- Imprecise by cause: fixable now 20 (F1 heim2026 #1 #2 #3 #5; F2 puckett2021 #2 #3 #4 #11; F3 jung2026 #1-#12);
  checker gaps 6 (C1 dutta2025 #8; C2 franken2025 #1 #11; C3 zhou2025a #1-#3).
- The 4 `no_header` slots: yanikgonul2021 #5 (correct, not printed in the header) and zhou2025a #1-#3 (C3).
- Per paper (slots / rows): dutta2025 8 / 9; fan2021 15 / 20; franken2025 12 / 15; govdeli2025 7 / 8; harris2014 7 / 7;
  hazan2021 6 / 6; heim2026 5 / 5; hsu2023 5 / 6; ji2024 6 / 12; jung2026 12 / 15; kao2026 5 / 5; li2025a 9 / 17;
  mehta2017 2 / 2; miller2017 7 / 11; nevlacsil2019 7 / 7; perezgalacho2017 11 / 41; puckett2021 11 / 11;
  romerogarcia2014 5 / 5; sawamura2023 7 / 7; sohn2021 3 / 3; su2017 5 / 5; tzu2019 6 / 6; wang2018 8 / 11;
  watanabe2025 5 / 5; yang2018 7 / 9; yanikgonul2021 7 / 7; zhao2025a 13 / 31; zhou2025a 3 / 0.

## Findings and proposed fixes (not applied)

| # | paper, slots | rating | evidence (locator) | proposed fix (field: before -> after) |
|---|---|---|---|---|
| F1 | heim2026 #1 #2 #3 #5, block 1 | imprecise, fixable (form only; mapping unchanged) | p.1 header: department, then University of California Santa Barbara without a comma, then the city. D301 records the org without the place and the place in `campus`; lit_h16 jin2021 has the same comma-less print and records `campus` (accepted in the 2026-10-29 round-4 audit); 31 other UCSB blocks in the lit batches do the same; only one lit_h05 block has the older in-org form. Probe U1: 0 errors; rows become "University of California, Santa Barbara", still `org_ucsb` | block 1 `org`: "University of California Santa Barbara" -> "University of California"; add `campus: "Santa Barbara"`. `note`: "block 1 prints University of California Santa Barbara without a comma (kept as printed in org)" -> "block 1 prints the campus Santa Barbara after the university without a comma (campus, D301)" |
| F2 | puckett2021 #2 #3 #4 #11, block 2 | imprecise, fixable (form only) | p.1 header: same print as F1 | block 2 `org`: "University of California Santa Barbara" -> "University of California"; add `campus: "Santa Barbara"`; same note change as F1 for block 2. Probe U1 (with F1): 0 errors, 4 rows `org_ucsb` |
| F3 | jung2026 #1-#12, blocks 1 and 2 | imprecise, fixable (unit omitted) | p.1 header: each block prints the university first, then its institute (Kirchhoff Institute for Physics; Center for Nanotechnology), then a street and the city. The note says the unit is not recordable because unit and org must be contiguous: they are contiguous (org, unit). This is not the iseghem2022 gap (D442), where a group is printed before and a department after the university. Probes J1 (block 1) and J2 (both blocks): 0 errors; 15 rows keep org, place and ids, unit filled. lit precedent: lit_h10 Sandia National Laboratories block 2, unit printed after the org and recorded | block 1 add `unit: "Kirchhoff Institute for Physics"`; block 2 add `unit: "Center for Nanotechnology"`. `note`: "both blocks print an institute after the university, not recorded (unit and org must be contiguous)" -> "both blocks print the unit after the university" |
| C1 | dutta2025 #8 (Arka Majumdar), block 3 | imprecise, not fixable now (row missing, none wrong) | p.1 header and render: run asterisk, dagger, pilcrow; recorded dagger only. Probes D1 (dagger + pilcrow) and D2 (pilcrow only): "printed markers differ" (md, pdf). Extractor's claim confirmed; same gap as D442 chen2024b and h23 G2 | after the checker fix: `markers: ["†", "¶"]`, rows 286 -> 287 (University of Washington, Department of Physics); drop the gap sentence from the note |
| C2 | franken2025 #1 #11, block 2 | imprecise, not fixable now | p.1 header and render: block 2 ends with the city, then "NL". Probe N1: country "NL" rejected, "not printed in this block" (md, pdf). `COUNTRIES["NL"]` has no "nl" form, while US and GB carry "us" / "uk". Probe N2 (monkeypatch adding "nl"): 0 errors | after the checker fix (question 2): block 2 `country`: "" -> "NL"; note sentence on the code removed |
| C3 | zhou2025a #1-#3 | imprecise, not fixable now (no rows) | p.1 footnote: one statement for all authors with four blocks. The render is readable with tight spacing; both text layers lose the word spaces on its first line, verb included. Probe Z1 (re-record as in question 5): 24 errors, not named in the statement subject. Probe Z2 (the h23 run-together split of subject candidates): same 24 errors, because the verb itself is glued | after a checker fix: re-record as in question 5; rows 286 -> 298 (3 authors x 4 blocks), status ok |
| N1 | jung2026 (note) | note wrong | see F3 | covered by F3 |
| N2 | zhou2025a (note) | note imprecise | note says the line runs together "in both the text and the PDF view"; true of the text layers, but the page is readable (as h23 N2, zhuang2025) | `note`: say that the text and PDF layers lose the word spaces on the first line of the statement, the page itself is readable, and the checker cannot parse the subject; no field or row change |

Any change to the YAML changes its hash: re-run `check lit_h24 --corpus lit` afterwards to refresh the stamp. F1-F3
together were probed on the scratch copy: 0 errors, 1 warning (the hazan2021 explicit slot), rows 286.

## Extractor questions: recommendations

1. yang2018 `grouped` for the De Gruyter footnote (no lit precedent). The first-page footnote prints, for the
   corresponding author and then for three author groups, the names followed by their block(s) (Lee: Baylor, then Texas
   A&M; Yang, Ghimire, Gurung, Arndt: Baylor; Wu: Academia Sinica, then Caltech; Tsai: Academia Sinica). That is the D368
   `grouped` structure (an author group printed with its own blocks, one block per printed org, marker `G<n>`, grade A).
   `prose` (D354) needs a verb statement; `layout` (D286f, grade B) is for one unmarked block next to marked blocks; there
   are no markers for `printed` / `pdf`. The checker verifies position: probes Y1 (Tsai moved to G4), Y2 (Lee moved to G3)
   and Y3 (Gurung moved to G6) each fail with D368 errors, so the groups are binding. The Baylor block printed twice is two
   blocks (G1, G3), as two statements naming the same org are two blocks (contract, prose rule). All six blocks and the
   seven carriers are correct. Recommended: accept; record a coordinator ruling (name-colon footnote groups = `grouped`,
   D368) so later De Gruyter papers follow it. Only other De Gruyter paper in the lit batches: lit_h13 pfister2025
   (preprint layout, `printed`), so no conflict.
2. franken2025 block 2 "NL". The print is the country code itself, at the place of the country; it is not an inference.
   But D246 requires the country to be verifiable in the block, and the checker's form list for NL has no "nl" (probe N1),
   so "" is the only value that passes now and the note says why. Recommended: keep "" in this round; in the checker
   follow-up add "nl" to the printed forms of NL only (as "us" and "uk" already are for US and GB), with a test, then set
   `country: "NL"` (probe N2: 0 errors). Do not accept bare alpha-2 codes generally: US state abbreviations printed in the
   same position (CA, DE, IN, MA, PA, ...) would then pass as countries.
3. fan2021 campus "Santa Barbara" without "(UCSB)". D301 makes `campus` the printed place only, and the matcher names the
   row "org, campus"; the acronym follows the place and is not part of an organization name, so the "keep parenthesized
   acronyms" rule (which keeps them inside `org`, e.g. "Institute of Microelectronics (IME)") does not apply. Precedent:
   lit_h20 khope2019 prints the same "University of California, Santa Barbara (UCSB)" and records org University of
   California + campus Santa Barbara without the acronym (audited GO). The checker would accept "Santa Barbara (UCSB)"
   (probe U2: 0 errors), so this is a contract call, not a checker limit. Recommended: accept as recorded; the 3 rows map
   to `org_ucsb`.
4. perezgalacho2017 block 1 as four organizations. Same print and same form as lit_h20 (block 1 "Centre for Nanoscience
   and Nanotechnology" + CNRS, Université Paris-Sud, Université Paris-Saclay), and lit_h03 / lit_h06 record the C2N print
   with CNRS, Paris-Sud and Paris-Saclay as four orgs; D285 puts joint-unit partners in `more_orgs`. The acronym C2N is
   printed after Paris-Saclay, before the city, not attached to the centre's name, so not copying it matches lit_h06.
   "Univ. Paris-Sud" is the printed abbreviation (lit_h10 has the same form); alias in the org round. Block 2 (Université
   Côte d'Azur, CNRS, Institut de Physique de Nice) as three orgs follows the same rule. Recommended: accept.
5. zhou2025a: agree that the paper stays `unreadable` (every author depends on the one statement) until the checker reads
   run-together statements, as zhuang2025 / psaila2024 / liu2025a / naraine2024 (D449). The fix needed is larger than the
   h23 Z2 subject split: here the verb phrase is glued too (probe Z2, 24 errors). Re-record plan, probed for consistency
   only (Z1; fails only on the subject check): P1 org Beijing Institute of Technology, unit "Radar Technology Research
   Institute, School of Information and Electronics", Beijing, CN; P2 (`clause: true`) org Beijing Institute of
   Technology, unit "Key Laboratory of Electronic and Information Technology in Satellite Navigation", Beijing, CN (the
   university is printed in parentheses after the laboratory name; the ministry printed after it is a parent, not
   copied); P3 (`clause: true`) org Beijing Institute of Technology, unit "Chongqing Innovation Center", Chongqing, CN; P4
   (`clause: true`) org "Chongqing Key Laboratory of Novel Civilian Radar", Chongqing, CN, with no university (none is
   printed in that clause; do not attach it to BIT). All three authors carry P1-P4. The co-first-author and
   corresponding-author parentheticals are not statements. Recommended: yes for P1-P3 as "BIT as org, lab as unit"; P4 as
   its own org.

## Reported gaps and flagged points

| paper | what the page shows | ruling |
|---|---|---|
| dutta2025 | author 8 prints asterisk, dagger, pilcrow; asterisk on authors 1 and 8 has no block; block 2 starts with a stray comma before its marker; block 2 is CNR dash-joined with its institute; block 4 is the institute, then CNR | Gap confirmed (C1). Block 2 dash-joined org kept as printed (D426); block 4 unit + org correct. Provinces after Rende not recorded (correct, D288). Ferraro and Pane (§), Lio (||), Caputo (‡, §) correct |
| jung2026 | org first, then institute, in both blocks | Not a checker gap: recordable now (F3) |
| yanikgonul2021 | render and both text layers: 6 names; list slot 5 (Shawn Yohanes Siew) not printed | `author_list_differs: true` and no row correct; probe S1 (flag removed): D174 error, so it is required. A*STAR parent after IMRE / IHPC / IME not copied (contract parent rule). Blocks print a postal code and Singapore: locality Singapore, SG (63 earlier blocks use this form). Dagger (author 2) and asterisk (author 3) point to contact lines: ignored correctly |
| hazan2021 | printed "Joel Hazan"; list "J.P. Hazan" | Explicit `slot: 1` correct: distinctive family name, the only difference is the middle initial absent from the print (D369 last sentence, D287; same form as garciablanco2025). Probe H1 (no slot): 0 matching slots, D247 error; H2 (`slot: 0`): D174 error. Warning in the check is the expected one |

Other papers (all correct; recorded values match the print):

- Markers: every printed run matches `markers` + `dropped_markers` in all 27 readable papers. Dropped numeric / letter
  markers verified: franken2025 #12 (6, contact), govdeli2025 #1 #7 (4, 5, contact), li2025a #1 #2 (4, equal
  contribution), mehta2017 #1 (a, contact; probe M1: required), zhao2025a #2 #3 #13 (12, 11, 13, contact). Symbol marks
  without a block ignored (D286d). The zhao2025a #13 drop is not enforced by the checker (probe Z0: 0 errors without it;
  same last-author gap as C1); the value is right by reading.
- Footnote blocks with `p.1 footnote`: fan2021, hsu2023, li2025a, romerogarcia2014 (prose), tzu2019 (prose), yang2018
  (grouped). Prose statements in romerogarcia2014 and tzu2019 are "The authors are with", carried by every author.
- Present address: miller2017 block 5 ("Currently at", Rochester, no country printed) carried by Cardenas with block 2.
- Empty fields correct: mehta2017 and miller2017 block 5 print no country; watanabe2025 prints neither city nor country
  (contact follows the org); franken2025 block 2 see C2.
- Country: Kowloon with HK for City University of Hong Kong (wang2018, as jankowski2020); Taiwan -> TW; The Netherlands
  -> NL (hazan2021); nothing inferred.
- As printed: "Karl. D. Nelson" (heim2026); "Furukawa Electric., Ltd." (watanabe2025) vs "Furukawa Electric Co., Ltd."
  (sawamura2023), both map to `org_furukawa_electric`; "University of Illinois at Urbana–Champaign" (unmapped, org round);
  fan2021 block 6 unit chain copied whole.
- Name matches: only initial or name-part differences (Martin M. / M. M. Fejer, Klaus-J. / Klaus J. Boller, John F.
  Conley Jr / John F. Conley, Michal / Michal F. Lipson, and similar); no match by position.
- D412 list artefacts: li2025a #9 "Daoxin Dai A" and su2017 #5 "Jelena Vuckovic A" in the author list; both matched and
  recorded (as earlier batches). Add both to the D412 correction file.

Unmapped org strings (17): not errors, for the org round. Academia Sinica (RCAS), CNR-Nanotec dash form, Hefei National
Laboratory, Honeywell Aerospace, Honeywell International, Howard University, IHPC, IMRE, National Chiao Tung University,
Northern Arizona University, RMIT University, RWTH Aachen University, Univ. Paris-Sud, University of Calabria, University
of Illinois at Urbana–Champaign, Université Paris-Saclay, Williams College.

## Privacy and as-printed scan

- `privscan.py` (session scratchpad) over every line of `headers.yaml`, `header_rows.csv`, `compare.csv`,
  `unmapped_orgs.csv`, `papers.csv` and this record: contact / URL patterns, street and building words, and the postal and
  street strings printed in this batch's blocks (postal codes and street names of all 28 headers). Result in all 6
  files: 0 contact or URL hits, 0 printed postal or street strings. Street-word hits: 4 in the YAML (its header comment
  and three notes naming the type of text left out) and 6 lines of this record (the same kind of type words, including this paragraph). Digit runs of 4
  or more: years in paper ids and dates, and in this record also the three check / probe pids; none is a postal code.
- No `skip_prefix` or `skip_between` in this batch.

## Commands (2026-11-06, log times)

| Command | Result |
|---|---|
| `check lit_h24 --corpus lit --dry-run` 01:32:28 (pid 19630) | 0 errors, 1 warning (hazan2021 explicit slot); slots 204, recorded 200, no_header 4; rows 286 (grade A 286; primary 230, additional 55; grouped 9, printed 254, prose 11, single 12); ok 27, unreadable 1; multi-affiliation slots 43; present addresses 1; 17 unmapped org strings |
| `probe.py` on the scratch copy, dry-run, 01:37:54-01:39:36 (pid 23069) | results in the probe table; repo `headers.yaml` md5 unchanged |
| `probe2.py` on the scratch copy, 01:40:04 (pid 23942) | F1 + F2 + F3 together: 0 errors, 1 warning; rows read from the scratch derived files, then deleted |
| `privscan.py` over the 5 batch files and this record | 0 contact, 0 printed postal or street strings; word hits as described above |

| probe | change | result | reading |
|---|---|---|---|
| N1 | franken2025 block 2 country NL | 2 errors, not printed in this block | C2 confirmed |
| N2 | N1 + "nl" as a printed form of NL | 0 errors | question 2 fix |
| U1 | heim2026 / puckett2021 org + campus | 0 errors; rows `org_ucsb` | F1, F2 |
| U2 | fan2021 campus "Santa Barbara (UCSB)" | 0 errors | question 3 is a contract call |
| J1 / J2 | jung2026 unit after org (block 1 / both) | 0 errors; 15 rows with unit | F3; extractor's gap claim not confirmed |
| D1 / D2 | dutta2025 #8 markers dagger + pilcrow / pilcrow only | 2 errors each, printed markers differ | C1 confirmed |
| Y1 / Y2 / Y3 | yang2018 author moved to another group | 5 / 4 / 4 errors (D368) | grouping binding |
| H1 / H2 | hazan2021 no slot / `slot: 0` | 2 / 1 errors | explicit slot required |
| S1 | yanikgonul2021 without `author_list_differs` | 1 error (D174) | flag required |
| M1 | mehta2017 letter a not dropped | 2 errors | drop binding |
| Z0 | zhao2025a #13 without dropped 13 | 0 errors | last-author gap (G1) |
| Z1 / Z2 | zhou2025a re-recorded / + subject split | 24 / 24 errors, not named in subject | C3; Z2 patch insufficient |

## Checker gaps observed (scripts not edited)

- G1 Last-author marker run (D442 chen2024b, h23 G2): a further printed marker on the last author is neither accepted
  (dutta2025, probe D1) nor enforced (zhao2025a, probe Z0).
- G2 Run-together prose statement with a glued verb ("authors are with" without spaces): the subject split from h23 Z2
  is not enough (zhou2025a, probe Z2). Same family as zhuang2025 / psaila2024 / liu2025a / naraine2024.
- G3 Country printed as an ISO code: "NL" is not a printed form of NL (franken2025, probe N1).
- G4 (minor) `campus` accepts a parenthesized acronym (probe U2); the D301 format check rejects only digits and commas.

## Coordinator questions

1. Apply F1-F3 and N2 now, then re-run `check lit_h24 --corpus lit`? Recommended: yes, before `aggregate`; no row count
   change, 20 rows gain the campus form or a unit.
2. Accept the recommendations on questions 1-5 above, with a ruling for the De Gruyter `grouped` form (question 1) and
   the narrow "nl" form (question 2)?
3. Add li2025a #9 and su2017 #5 to the D412 correction file, and C1 / C2 / C3 to the checker follow-up list (re-record
   dutta2025 #8, franken2025 block 2, zhou2025a after the fixes)?

## Verdict

GO. No slot carries a wrong person, org, unit, city, country or marker, nothing is invented, no block is missed, and no
address or contact text is recorded. 20 slots should take the campus form or the omitted unit (F1-F3, field changes
only); 6 slots wait on known checker gaps and are correct as far as recorded.
