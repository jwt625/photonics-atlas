---
title: Fresh-context audit of the lit author-affiliation batch lit_h22 (35 papers)
date: 2026-11-04
auditor: Claude (fresh context; wrote only this record and scratchpad helpers; headers.yaml, scripts, tests, people and registry data not edited; aggregate not run)
scope: data/_staging/people/lit_headers/lit_h22/headers.yaml; both header contracts; DevLog-011 D350-D369, D380, D400-D442; example audit 2026-11-02-lit-header-batch-h19-audit.md
verdict: GO for the people rebuild (check 0 errors, 2 warnings); 0 wrong and 10 imprecise slots in 275 audited (7 fixable, proposed below and not applied; 3 are a known checker gap); 1 note to make by-type
---

# Lit header batch audit: lit_h22 (2026-11-04)

## Scope

Batch lit_h22 (35 papers, 275 author-list slots), extracted 2026-11-04 (dry-run check: 0 errors, 2 warnings; 34 ok, 1
partial; 263 / 275 slots recorded; 305 rows, all grade A; 28 unmapped org strings). Restricted corpus: this record names
only authors, orgs, units, cities and countries; no paper text is quoted and no contact, street, building, postal or box
code is copied. Site words at issue are named by type, with a `headers.yaml` line number.

## Method

- Every paper read with `uv run --offline python scripts/ofc_headers.py show lit_h22 --corpus lit --codes <id> --pdf`,
  through a terminal-only viewer that keeps the header, the footnote statements, every affiliation-like line and the
  superscript lines of the PDF layer (`view.py`, `view2.py` in the session scratchpad `audit_lit_h22/`). `--pages 1 2` for
  hoffman2016 (cover page). The extractor's notes were checked against the page, not used as evidence.
- Selection: all 35 papers (full coverage):
  - (a) `slot: 0` / `author_list_differs` / order differs / explicit slot: gundavarapu2018, shi2026, stanfield2019;
  - (b) prose: bai2023, barwicz2018, boerma2026, heermeier2025, hossain2026, huang2019b, konoike2022, lu2025, poulton2022,
    reniers2019, rizzo2020, shahin2025, shi2026, srinivasan2020; present addresses: barwicz2018, rizzo2020, shahin2025;
  - (c) flagged items: kim2026, huang2019b #5, hossain2026 #5, hoffman2016 block 4, melati2022 block 2, lu2025 parent;
  - (d) the remaining papers: akritidis2026, blundell2025, chang2026, gagino2024, georgieva2022, gissibl2016, lorenzen2026,
    lu2019, mnaymneh2018, peng2020a, probst2023, shui2026, song2021b, su2024, sundaram2024, vines2019.
- Per slot: slot-to-name assignment (D359, D369, D287, D302), printed marker run vs `markers` (text and PDF layer), block
  mapping, org / unit / more_orgs split, parent rule, campus (D301), locality, country, role, basis, locator.
- Page crops rendered from the local PDF and read for kim2026 (author line), hoffman2016 p.2 (author line and all five
  blocks) and lorenzen2026 (author line): markers agree with both text layers. Crops removed afterwards.
- Name scan: all 275 `compare.csv` rows, list name vs printed name (folded): 43 rows differ or have no header; all read.
- Org mapping: all 70 (printed org, id, place) combinations of `header_rows.csv` read against the block; registry and
  people files read only.
- Missed blocks and present addresses: all pages of all 35 papers searched for statement and present-address cues through
  `show --pages` (`cues.py`).
- Claims tested with probes on a scratch copy of the batch, `check_batch` called directly (`probe.py`, `probe2.py`); the
  repo `headers.yaml` hash was asserted unchanged after each run.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h22 | 35 / 35 | 275 | 265 | 10 | 0 |

- Imprecise: gundavarapu2018 #1 #2 #4 #5 #15 (F1, fixable), hoffman2016 #2 #5 (F2, fixable), kim2026 #1 #2 #3 (C1, checker
  gap, no rows).
- `no_header` slots: 12. Three are C1. Nine are correct: gundavarapu2018 #3 #7 #8 #9 #10 #11 #13 #14 (not printed in the
  cached preprint), shi2026 #2 (`slot: 0`, D369).
- Header-only authors (`slot: 0`): 1 (shi2026 Fei Wang), no rows, correct.

## Rulings on the points flagged for attention

| paper, slot / block | evidence | ruling |
|---|---|---|
| kim2026 #1-#5 | p.1 header, both layers and page crop: Kim and Örsel carry marker 1, Workman marker 2, Yim and Bahl marker 3. Blocks 1 and 2 print a department only; the org and place follow block 3 once. Probe with block 1 recorded (unit + org): 4 errors | `partial` correct; Yim and Bahl rows correct; the note's facts correct; 3 authors carried as unreadable because of the gap (C1) |
| gundavarapu2018 | p.1 header prints 7 names; registry row carries a preprint id; 15 in the list; all 7 match by exact name at list positions 1, 6, 2, 5, 4, 12, 15; the 8 names in the note are the 8 unprinted ones | `author_list_differs` and the order warning correct; markers and blocks 2, 3 correct; block 1 org: F1 |
| shi2026 #2 | p.1 header and p.1 footnote print Fei Wang; list F S Wang at the same position. Probe without `slot:`: matches 0 slots (D369: initial S unexplained; common family name) | `slot: 0` + `author_list_differs` correct; no rows; open question 1 |
| stanfield2019 #1 | P. R. Stanfield printed; list Paul Stanfield; first initial agrees, middle initial missing from the list, distinctive family name, same position. Probe without `slot:`: 2 errors | explicit `slot: 1` correct under D369 / D287; warning expected |
| huang2019b #5 | Xiang Meng in the author line, X. Meng in the statement; list Xiang Zheng Meng, same position. Probe `slot: 0`: D302 error | auto-match accepted, dropped-syllable pattern; open question 2 |
| hossain2026 #5 | Gerald J. Leake printed; list token Jr. after the given name, same position. Probe `slot: 0`: D302 error. `people.py` drops the suffix from the name key (`SUFFIXES`), so the slot keys as gerald leake, an existing person | auto-match correct |
| hoffman2016 block 4 | p.2 header and page crop: department, then the center, then the city and Belgium; no parent printed. Probe with no org: error (block has no org) | center as org, department as unit correct; nothing invented; no id forced (open question 4). Both carriers also carry block 3 |
| melati2022 block 2 | p.1 header: center, CNRS, Université Paris-Saclay, Palaiseau, France, each printed as a separate name (D285 joint unit) | org + 2 `more_orgs` correct; 3 rows on Melati; Université Paris-Saclay unmapped |
| lu2025 P1 | p.1 footnote: parenthetical parent after Vanguard Automation GmbH | not copied, correct under the parent rule; maps to `org_vanguard_automation` |
| shahin2025 P2, P3 | p.1 footnote: Berciano's past-tense statement (IMEC, Leuven, BE), then a pronoun present-address statement (Nubis Communications, Mountain View, US) | both blocks and `role: present_address` correct. The state printed with the city does not match the usual state of Mountain View: city kept as printed, not corrected, correct |

## Findings and proposed fixes (none applied)

| # | paper, slots | rating | evidence (locator) | proposed fix (field: before -> after) |
|---|---|---|---|---|
| F1 | gundavarapu2018 #1 #2 #4 #5 #15, block 1 (`headers.yaml` line 164) | imprecise, fixable | p.1 header: University of California at Santa Barbara. D301 asks for org without the place and the place in `campus`; chang2026 block 1 in this batch and a2011 / kang2008 / kang2008a do so. Recorded in `org` without `campus`, so 5 rows are unmapped | `org`: University of California at Santa Barbara -> University of California; add `campus: "Santa Barbara"`. Probe: 0 errors; 5 rows map to `org_ucsb`; unit and place unchanged |
| F2 | hoffman2016 #2 #5, block 3 (line 197) | imprecise, fixable | p.2 header and page crop: the `org` field starts with a site word joined by a dash to Universiteit Gent. Auditor's background knowledge, no local source to confirm it and no network used: the site word names a university building, not an organization. D380 keeps building names out of the rows. Rows are unmapped although the registry has Universiteit Gent as an alias | `org` -> Universiteit Gent; add `skip_between` = the site word plus the dash as printed. Probe: 0 errors; 2 rows map to `org_ghent_university` by alias. Alternative if the coordinator does not accept the background knowledge: keep the string (D416 (5)) and add an org-round alias (open question 3) |
| N1 | song2021b (note, line 487) | privacy rule | the note names the campus printed before Hangzhou (h17 audit N1 practice: address parts by type only) | note: the campus name -> "a campus name"; no field changed, rows unchanged |
| C1 | kim2026 #1 #2 #3 | imprecise, not fixable (no rows) | see the ruling above; precedent foster2006 #1 #3 #6 (h17 C3) | none now (gap G1). After the gap is fixed, record Kim and Örsel: Department of Electrical & Computer Engineering; Workman: Department of Physics; all University of Illinois at Urbana-Champaign, Urbana, US |

F1 and F2 probed together: 0 errors. After any fix, re-run `check` (the stamp hash changes), then
`aggregate`.

Checked and correct (highlights):
- Prose (14 papers, every subject name vs carrier both ways): bai2023 P1 / P2 clause, P3, P4; barwicz2018 P1-P7 (Peng,
  Leidy and Khater statements in the past tense, Peng present address Global Foundries, Hopewell Junction; Leidy at Essex
  Junction); boerma2026 P1, P2 + P3 clause; heermeier2025 P1, P2; hossain2026 P1 + P2 clause, P3; huang2019b P1, P2, P3
  (Novack: Columbia department and Elenion, one place; the Elenion row has no unit, correct); konoike2022 and
  poulton2022, reniers2019, srinivasan2020 ("the authors": all carry P1); lu2025 P1-P3; rizzo2020 P1-P3 (Cheng past tense
  at Columbia, present address University of Cambridge, GB); shahin2025 P1-P6 (Loo: IMEC + clause Ghent University, own
  unit and place); shi2026 P1, P2.
- Marked papers: every printed marker run matches `markers` in both layers. peng2020a all 26 runs; blundell2025 symbol
  markers and the three blocks; chang2026 #2 #12 and `campus` Berkeley; song2021b block 1 chain, Ningbo block 2; shui2026
  block 3 (province only, `locality` empty); su2024 block 2 (province by type in the note).
- Single blocks: mnaymneh2018, stanfield2019 (a box code is printed before the city in stanfield2019, not recorded).
- Cover page: hoffman2016 `p.2 header`. Foot-of-page blocks: gagino2024, gissibl2016, lorenzen2026, vines2019 `p.1
  footnote`.
- Later pages: only biographies (boerma2026 p.7, huang2019b p.8, konoike2022 p.6, poulton2022 p.8) and competing-interest
  lines; not header statements, not recorded. No present-address cue outside the three papers above.
- Org mapping: all mapped strings read and correct, including Interuniversity Microelectronics Center to `org_imec`,
  dash-joined Ghent University forms to both ids, Technical University of Berlin to `org_tu_berlin`, IBM T. J. Watson
  Research Center to `org_ibm_watson`. 28 unmapped org / unit strings, none wrongly forced.
- `compare.csv`: 263 recorded, 12 `no_header`; every list-side difference is an initial, a middle name or a list form of
  the same name at the same position (for example K. Bergman, J.J.G.M. van der Tol, Andrew Jay Leenheer).

## Privacy and as-printed scan

- `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`, `papers.csv`: scanned for contact and URL patterns,
  3+ digit runs and street / road / avenue / drive / building / box / campus words and the street names printed in this
  batch's blocks. Hits: song2021b note (N1), the F2 site word (found by reading, then confirmed by the scan), the file-header comment, and two false positives (the word Intelligent; `campus` as a field name). No
  `skip_prefix` / `skip_between` span in the batch.
- This record: same scan (`privscan.py`). Hits: generic words, dates, counts, decision and line numbers only. Site words
  named by type only.

## Commands (2026-11-04, log times)

| Command | Result |
|---|---|
| `uv run --offline python scripts/ofc_headers.py check lit_h22 --corpus lit --dry-run` 18:37:38 (log `lit_headers_check_lit_h22_7073_20261104T183731.log`), repeated 18:45:44 (pid 10379) | 0 errors, 2 warnings (gundavarapu2018 order, stanfield2019 explicit slot); papers ok 34, partial 1; slots 275, recorded 263, no_header 12; rows 305 (grade A 305, printed 188, prose 104, single 13); present addresses 3; 28 unmapped org strings |
| Stamp | `check_stamp.txt` matches `headers.yaml` (sha256 9b16cb21febe...) |
| Probes on the scratch copy | baseline 0 errors; F1, F2 each 0 errors, unmapped strings 28 -> 27; shi2026 no slot 1 error; kim2026 block 1 recorded 4 errors; huang2019b #5 `slot: 0` 2 errors; stanfield2019 no slot 2 errors; hossain2026 #5 `slot: 0` 2 errors; lu2025 parent copied 0 errors (G3); hoffman2016 block 4 no org 1 error |

Boundary note: one read-only `git status` was issued by mistake inside a shell command, against the no-git boundary of
this audit; its output was discarded and it changed nothing. No other git command, no network request.

## Checker gaps observed (scripts not edited)

- G1 Org and place printed once after unit-only blocks cannot be recorded (D426 G3; kim2026, as foster2006).
- G2 A campus printed inside `org` with "at" passes without `campus` and without a warning (gundavarapu2018): a warning for
  the University of California pattern would catch it.
- G3 The parent rule is not enforced: a parenthetical parent copied into `org` passes (probe on lu2025).
- G4 Org matching does not fold an en dash to a hyphen: University of Illinois at Urbana-Champaign has an alias, the
  printed en-dash form in kim2026 stays unmapped.
- G5 The D244 scan does not see campus names in notes (song2021b), nor a site word inside an org string (hoffman2016).

## Open questions

1. shi2026 #2: add F S Wang (same position as the printed Fei Wang) to the D412 author-list correction file, so the slot
   gets rows? Recommended: yes; no rows until then.
2. huang2019b #5 (Xiang Meng / Xiang Zheng Meng): accept and add to the D426 review list with jia2025 #3 and the D442
   names? Recommended: accept.
3. F2 rests on background knowledge of the site word: apply the `skip_between` fix, or keep the string with an org-round
   alias? Recommended: the fix; both give `org_ghent_university`.
4. Org round, aliases to existing ids (printed strings kept): Global Foundries to `org_globalfoundries`; Technical
   University of Eindhoven to `org_eindhoven_university_of_technology`; Fraunhofer Institute for Telecommunication,
   Heinrich-Hertz-Institute to `org_fraunhofer_heinrich_hertz_institute`; the en-dash Illinois form to
   `org_university_of_illinois_urbana_champaign`; the Xi'an Institute string to
   `org_xian_institute_of_optics_and_precision_mechanics`. New ids or a decision needed for the rest of
   `unmapped_orgs.csv`; the registry's AIM Photonics id is the test and packaging facility, so not an automatic alias for
   the AIM Photonics string; Center for Nano and Biophotonics prints no parent, so no id should be inferred from the paper.
5. gundavarapu2018: the 8 list authors absent from the preprint header stay without rows (merge item 8). Reading the
   published header would need that version in the cache. Recommended: leave.
