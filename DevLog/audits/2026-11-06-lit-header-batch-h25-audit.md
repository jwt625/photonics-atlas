---
title: Fresh-context audit of the lit author-affiliation batch lit_h25 (17 papers)
date: 2026-11-06
auditor: Claude (fresh context; wrote only this record; headers.yaml, derived files, scripts, tests, people and registry data not edited; aggregate and the people build not run; no git, no network)
scope: data/_staging/people/lit_headers/lit_h25/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369, D380, D400-D461; format and precedent from the 2026-11-06 h24 audit
verdict: GO for the people rebuild after F1 (or GO as is, since no row is wrong); 154 slots audited, 147 ok, 7 imprecise, 0 wrong; 1 fixable finding (F1, 2 slots, field changes only), 5 slots imprecise from known checker gaps (no fix in the YAML now), 2 note corrections; nothing applied
---

# Lit header batch audit: lit_h25 (2026-11-06)

## Scope

Batch lit_h25 (17 IEEE / IEEE-hosted papers, 154 author-list slots, 182 rows). Restricted corpus: this record names only
authors, orgs, units, cities and countries; no paper text is quoted and no contact, street, building, site or postal text
is copied.

## Method

- Every paper read with `uv run --offline python scripts/ofc_headers.py show lit_h25 --corpus lit --codes <id> --pdf`
  (all 17; `--pages 2` for kurczveil2013, mangal2019, yamaguchi2016, whose author lines are on page 2 after a cover).
- Rendered pages looked at where markers, layout or spacing were in question: golshani2021 (author grid,
  `figures/page_01.png`), poulton2017 (block 4, `figures/page_01.png`), yamaguchi2016 (`figures/page_02.png`), and
  scratch renders of the header crops of her2022 (text layers without word spaces), caillaud2021 (block 1), kurczveil2013
  and mangal2019 (page 2). Scratch renders deleted after reading.
- Per slot: printed name vs `compare.csv` slot, printed marker run vs `markers` + `dropped_markers`, block fields vs the
  print (org, unit, campus, city, country), present address, parents, as-printed forms. All 50 distinct (org, unit,
  place, role, id) row tuples of `header_rows.csv` read; no wrong mapping.
- Missed blocks: cue scan of the whole `text.md` of all 17 (now with / at, present / current address, currently,
  presently, also with, was / were with, on leave, visiting, current / present affiliation, formerly, deceased, permanent
  address). Header hits: bayoumi2025, maeda2024, tsakyridis2020 (clauses, recorded), bolk2018 and chung2017 (was with /
  now with, recorded), moscosomartir2017 block 2 (recorded). Other hits are biographies on later pages. poulton2017
  block 4 has no scan hit because the text layer prints its cue with a ligature; read on the page render (C1). No
  missed block.
- Claims tested with dry-run probes on a scratch copy of the batch (`probe.py`, via the module's `LIT_BASE`; md5 of the
  repo `headers.yaml` asserted unchanged). `probe2.py` ran `cmd_check` without dry-run on a scratch copy only, to read the
  rows F1 would derive; its derived files were deleted with the scratch directory and every repo batch file's md5 was
  asserted unchanged. Each probe left a log in the git-ignored `logs/`.
- Stamp: `check_stamp.txt` matches `headers.yaml` (sha256 02ec1471...). `headers.yaml` mtime 01:58:36 is 41 s after the
  stamp (01:57:55) but the content hash is the stamped one. Repo batch files untouched by this audit.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h25 | 17 / 17 | 154 | 147 | 7 | 0 |

- Rows 182 (all grade A: prose 104, printed 61, per_author 11, single 6); recorded 153, no_header 1 (moscosomartir2017
  #7); ok 16, partial 1 (moscosomartir2017), unreadable 0; present addresses 2 (bolk2018 #6, chung2017 #2); 7 unmapped
  org strings; `order_differs` false on all 154 slots.
- Imprecise by cause: fixable now 2 (F1 caillaud2021 #4 #8); checker gaps 5 (C1 poulton2017 #1 #4 #6 #8; C2
  moscosomartir2017 #7).
- Per paper (slots / rows): bayoumi2025 19 / 27; bolk2018 10 / 11; caillaud2021 8 / 11; chung2017 3 / 4; feyisa2022 5 /
  5; golshani2021 11 / 11; her2022 10 / 10; itoh2024 16 / 16; kurczveil2013 5 / 7; maeda2024 13 / 15; mangal2019 5 / 9;
  moscosomartir2017 15 / 14; poulton2017 9 / 10; sun2023 4 / 4; tsakyridis2020 7 / 14; yamaguchi2016 6 / 6; yuan2023 8 /
  8.

## Findings and proposed fixes (not applied)

| # | paper, slots | rating | evidence (locator) | proposed fix (field: before -> after) |
|---|---|---|---|---|
| F1 | caillaud2021 #4 (R. Gnanamani), #8 (C. Maneux), block 2 | imprecise, fixable (form; one org missing as an org) | p.1 header: the block prints IMS Laboratory, then University of Bordeaux, then CNRS with the joint-unit (UMR) number, then the city. D285 treats a UMR like a state key laboratory: `more_orgs` when printed as a separate organization. Every committed lit UMR print records the joint unit as its own org with the partners in `more_orgs`: lit_h10 IEF + Univ. Paris-Sud + CNRS (same order: lab, university, CNRS), lit_h03 / h06 / h13 C2N, lit_h06 Institut des nanotechnologies de Lyon + CNRS + Ecole Centrale Lyon, lit_h14 LTM; none records a UMR lab as a `unit` with CNRS in `more_orgs`. Probe C1: 0 errors; `probe2` rows 182 -> 184 (each slot: IMS Laboratory, University of Bordeaux, CNRS; CNRS -> `org_cnrs`, the other two unmapped as now) | block 2 `org`: "University of Bordeaux" -> "IMS Laboratory"; remove `unit: "IMS Laboratory"`; `more_orgs`: ["CNRS"] -> ["University of Bordeaux", "CNRS"]. `note`: "block 2 prints the IMS Laboratory, University of Bordeaux and CNRS with a joint-unit number (CNRS recorded as a further organization, D285)" -> "block 2 prints the joint research unit IMS Laboratory with University of Bordeaux and CNRS and its UMR number (three organizations, D285, as lit_h10 IEF; the number is not copied)" |
| C1 | poulton2017 #1 #4 #6 #8, block 4 | imprecise, not fixable now (present-address rows missing, none wrong) | p.1 header and page render: block 4 is printed with the cue Current Affiliation, followed by Analog Photonics, Boston, USA. Probe P1 (block 4 recorded `role: present_address`, marker 4 moved from `dropped_markers` to `markers`): 2 errors, marker + first field not adjacent (md, pdf); `CUE_WORDS` has no current / present affiliation form. Same gap as D442 (stanton2020 #4, zhang2025c #2) and the Current address cue (lit_h05, h16, h17); recorded the same way (marker under `dropped_markers`, note says so) | after the checker fix: add block 4 `{marker: "4", basis: printed, role: present_address, org: "Analog Photonics", locality: "Boston", country: "US"}`; authors 1, 4, 6, 8 `markers: ["1", "4"]` without `dropped_markers`; rows 182 -> 186 (186 -> 188 with F1); drop the gap sentence from the note |
| C2 | moscosomartir2017 #7 (F. Lelarge) | imprecise, not fixable now (no rows) | p.1 header and PDF layer: author 7 carries only marker 2, the block printed with the cue Now with (Almae Technologies SAS, Marcoussis, France); no affiliation of the work is printed for him. Probe M1 (`unreadable` and `partial` removed): 1 error (no markers and no unmarked block) + 1 warning (only a present-address block). D426 G4 gap, recorded as keyvaninia2019 (lit_h13) and yang2010 (lit_h18) | after the G4 checker fix: drop `unreadable: true`, paper `status: ok`; 1 present-address row (Almae Technologies SAS, Marcoussis, FR); slot #7 `recorded` |
| N1 | kurczveil2013 (note) | note imprecise | page 2 render: the marker pairs of authors 1 and 2 are printed with a comma; only the text and PDF layers carry a semicolon glyph there | `note`: "markers printed with semicolons" -> "the text layers carry a semicolon between the paired markers of authors 1 and 2 (the page prints a comma)"; no field or row change |
| N2 | golshani2021 (note) | note imprecise (minor) | page 1 render: the grid row 2 prints De Coster, Milenin, Thiam, Mingardi; the text layers give De Coster after row 1, then row 3, then Milenin, Mingardi, Thiam (Thiam and Mingardi swapped as well as moved) | `note`: "(row 2 columns 2-4 last)" -> "(row 2 columns 2-4 last, columns 3 and 4 swapped)"; no field or row change |

Any change to the YAML changes its hash: re-run `check lit_h25 --corpus lit` afterwards to refresh the stamp.

## Extractor questions: recommendations

1. bayoumi2025 P2 (clause): printed group chain (Photonics Research Group, Department of Information Technology), then
   imec, then Ghent University, then Ghent, Belgium; recorded org Ghent University + the chain as `unit` + imec in
   `more_orgs`. Probes: B1 (org imec + chain + `more_orgs` Ghent University) 0 errors, so this is a contract call, not a
   checker limit. The recorded form passes only because the 4-character "imec" fits in the 10-character unit-org gap
   that `_window_checks` tolerates (probe B2, unit cut to the group alone: "not one contiguous printed segment"), so it
   is not contiguous in the strict sense of the contract. Weighing: (a) the print names the pair as the joint parent of
   the chain, the same structure as the dash-joined "Ghent University - imec" that D416 (5) / D426 keep as one org with
   the chain as unit; a comma pair cannot be kept as one org string (it would be an unmappable one-off); (b) every
   committed split of this group records Ghent University as the org carrying the chain and imec in `more_orgs`
   (lit_h01 deng2026 / deng2026a, lit_h05 brouckaert2007, lit_h09 sattari2020, lit_h01 elsaeed2024 P3), so the
   recorded form gives the same rows (`org_ghent_university` with the chain, `org_imec`) for the same group and the same
   authors; (c) B1 would attach a group recorded in about 30 committed blocks under Ghent University to imec instead.
   No text is invented either way: both orgs and the chain are printed in the block. Recommended: accept as recorded
   (4 slots ok) and record a coordinator ruling extending D416 (5): a comma-joined org pair printed after a unit chain
   ("unit, A, B") is split into `org` + `more_orgs` with the chain on the org that the committed records of that unit
   use; the 10-character gap is then the only verification, so state the ruling rather than rely on the checker.
2. tsakyridis2020 P2: the clause prints the centre, then a site name, then the postal code and the city. The site name
   is in the address position (after the org, before the postal code), the place where lit_h10 and lit_h13 leave out site
   names and this batch leaves out the campus site of moscosomartir2017 block 3; recording it as an org or unit would
   create an org that the block does not name as an affiliation. The checker would accept it as `more_orgs` or `unit`
   (probes T1, T2: 0 errors), so this is a contract call. Recommended: accept as recorded (left out, named in the note
   as now). The centre itself stays an org of its own (printed in its own clause without the university, D366 clause
   rule); unmapped, for the org round.
3. caillaud2021: (a) block 1 prints only III-V lab, its description as a joint lab of three organizations and a contact
   line; no city or country. `locality: ""`, `country: ""` are required by D288 / D249 (no inference): probes C2
   (country FR) and C3 (locality Palaiseau) fail, "not printed in this block". Parents not copied (contract parent rule,
   D426 keyvaninia2012; lit_h05, h09, h13, h14, h17 III-V lab blocks); the checker would accept a parent in
   `more_orgs` (probe C4: 0 errors), so the omission is the ruling, not a checker limit. Accept; the row maps to
   `org_iii_v_lab` with an empty place. (b) CNRS in `more_orgs` is right (D285), but the IMS Laboratory should be the org
   with University of Bordeaux and CNRS as `more_orgs`, not a unit of the university: see F1.
4. bolk2018 #6: list name "E Elton Bitincka", printed "E. Bitincka". Not a D412 case on the evidence available: D412
   covers list artefacts that would publish a truncated or garbled name (a stray trailing letter, a cut family name or
   given name); this form is complete, carries the printed initial (D369 match on E), and the same form appears in all
   three `merged.jsonl` records that name him (bolk2018 and two other cached works), so it is the upstream name, not an
   extraction artefact of this list. Whether "E" is a separate given name or a doubled initial of Elton cannot be decided
   offline and is not printed. Recommended: keep the slot and its rows; do not add it to the D412 correction file; add it
   to the D426 review list ("initial + given name" form, check against an authoritative record in the people review).

## Reported gaps and flagged points

| paper | what the page shows | ruling |
|---|---|---|
| moscosomartir2017 #7 | author 7 prints only the present-address marker | G4 gap confirmed (C2, probe M1); recorded like keyvaninia2019 / yang2010 (D426); `partial` correct |
| poulton2017 block 4 | present address printed with the cue Current Affiliation | D442 gap confirmed (C1, probe P1); `dropped_markers` with the reason, as lit_h05 / h16 / h17 / h21 |
| golshani2021 | IEEE conference grid of 11 authors (3 rows), one block under each; text and PDF layers list the grid in another order and after the figure 2 caption | Correct as recorded. The block list must follow the text-layer order (probe G4, blocks moved to the printed order: 6 errors, D368); the carriers are bound (probes G1 Thiam / Mingardi swapped and G2 Milenin / Verheyen swapped: 4 errors each); the G numbers are synthetic and free (probe G3, numbers in printed-grid order with the list order kept: 0 errors). Authors are listed in printed reading order (row by row), as the contract requires, and that order equals the author list (`order_differs` false). Every author's unit matches the render; no change (note detail N2) |
| her2022 | text and PDF layers lose the word spaces of the title, author line and blocks; page readable | Names, markers and both blocks read from the render; all 10 correct; asterisks on authors 9 and 10 point to contact lines (ignored, D286d) |
| kurczveil2013, mangal2019, yamaguchi2016 | cover page; author line and blocks on page 2 | `p.2 header` on every block correct (D366). kurczveil2013 block 1 org University of California + `campus` Santa Barbara (D301, as h24 F1 / F2); mangal2019 block 1 Ghent University as a structured `more_orgs` entry with its own place (D367); yamaguchi2016 prints only the prefecture: `locality: ""` (D288) |

Other papers (all correct; recorded values match the print):

- Markers: every printed run matches `markers` + `dropped_markers` in all 6 papers with printed markers. Symbol marks without a block
  ignored (caillaud2021 none; her2022 asterisks; moscosomartir2017 #15 asterisk).
- Prose papers (9): bayoumi2025, bolk2018, chung2017, feyisa2022, itoh2024, maeda2024, sun2023, tsakyridis2020,
  yuan2023 (and the clause blocks of bayoumi2025, maeda2024, tsakyridis2020). Every statement naming an author is
  recorded; subjects match the carriers. "Was with" recorded as the affiliation of the work and "He is now with" as a
  present address in bolk2018 (#6, ASML, Veldhoven) and chung2017 (#2, Rockley Photonics, Pasadena). bolk2018 P3 and P6
  name the same org in two statements: two blocks (contract prose rule).
- Places: maeda2024 Keio clause prints a ward and a prefecture only: `locality: ""` (D288, as lit_h02 / h17 Keio blocks
  with no city); sun2023 Hefei with the province not copied; "Atsugi-Shi" kept as printed (D366); "University of Tokyo"
  printed without an article.
- As printed: feyisa2022 "Eindhoven university of Technology" (lower-case u, maps to `org_eindhoven_university_of_technology`);
  yuan2023 unit chain joined with "and" (same form as lit_h13); her2022 KAIST with its parenthesized acronym (maps by
  `name:no_parenthetical`); moscosomartir2017 III-V Lab without parents and the site / street spans of blocks 3 and 4 not
  recorded.
- Name matches: only initials, dropped middle names or hyphen / case variants (Philippe P. Absil, Ken-ichi / Kenichi
  Machinaga, Menaka DE ZOYSA, J. D. / Jonathan D. Peters, John Edward / John E. Bowers, Alexey P. Milenin, A. / Andrea
  Mingardi, Nikolaos-Panteleimon Pandelis Diamantopoulos, and similar); no match by position, no explicit `slot:`.

Unmapped org strings (7): not errors, for the org round. Center for Interdisciplinary Research and Innovation, Daegu
Gyeongbuk Institute of Science and Technology, HP Labs, InPACT SA, RWTH Aachen University, University at Albany,
University of Bordeaux (with F1 also IMS Laboratory).

## Privacy and as-printed scan

- `privscan.py` (session scratchpad) over every line of `headers.yaml`, `header_rows.csv`, `compare.csv`,
  `unmapped_orgs.csv`, `papers.csv` and this record: contact / URL patterns, street and building words, digit runs of 4
  or more, and the postal and street strings printed in this batch's blocks (35 postal codes taken from the header
  pages of all 17 papers, plus the street, site and ward words of the blocks). Result in all 6 files: 0 contact or URL
  hits, 0 printed postal strings. Street / site hits: 1, in the YAML (the tsakyridis2020 note names the site word it
  leaves out, as lit_h10 / lit_h13 notes do); 0 in this record. Digit runs of 4 or more: years in paper ids, dates
  and notes, and in this record also the three check / probe pids and the stamp-hash prefix; none is a postal code.
- No `skip_prefix` or `skip_between` in this batch.

## Commands (2026-11-06, log times)

| Command | Result |
|---|---|
| `check lit_h25 --corpus lit --dry-run` 01:59:56 (pid 29192) | 0 errors, 0 warnings; slots 154, recorded 153, no_header 1; rows 182 (grade A 182; primary 157, additional 23; per_author 11, printed 61, prose 104, single 6); ok 16, partial 1; multi-affiliation slots 18; present addresses 2; 7 unmapped org strings |
| `probe.py` on the scratch copy, dry-run, 02:05-02:07 (pid 31049) | results in the probe table; repo `headers.yaml` md5 unchanged |
| `probe2.py` on the scratch copy, 02:08:25 (pid 31608) | F1: 0 errors, rows 184; scratch derived files deleted; repo batch files md5 unchanged |
| `privscan.py` over the 5 batch files and this record | 0 contact, 0 printed postal strings; 1 site word in a YAML note, 0 in this record |

| probe | change | result | reading |
|---|---|---|---|
| B1 | bayoumi2025 P2 org imec + chain + `more_orgs` Ghent University | 0 errors | question 1 is a contract call |
| B2 | bayoumi2025 P2 unit cut to the group alone | 2 errors, unit and org not contiguous | recorded form passes on the 10-character gap only |
| C1 | caillaud2021 block 2 org IMS Laboratory + `more_orgs` University of Bordeaux, CNRS | 0 errors (rows 184 in `probe2`) | F1 |
| C2 / C3 | caillaud2021 block 1 country FR / locality Palaiseau | 2 errors each, not printed in this block | question 3 (a): empty place required |
| C4 | caillaud2021 block 1 a parent in `more_orgs` | 0 errors | parent omission is the ruling |
| T1 / T2 | tsakyridis2020 P2 site name as `more_orgs` / `unit` | 0 errors each | question 2 is a contract call |
| P1 | poulton2017 block 4 as present address | 2 errors, marker + first field | C1 confirmed |
| M1 | moscosomartir2017 #7 readable | 1 error + 1 warning | C2 (G4) confirmed |
| G1 / G2 | golshani2021 carriers swapped | 4 / 4 errors (D368) | grouping binding |
| G3 | golshani2021 G numbers in grid order, list order kept | 0 errors | numbering free |
| G4 | golshani2021 blocks listed in printed order | 6 errors (D368) | text-layer list order required |

## Checker gaps observed (scripts not edited)

- G1 Current / Present Affiliation cue (D442): not a present-address cue; a cue between marker and first field also
  breaks the marker adjacency check (poulton2017, probe P1).
- G2 Present-address-only marker (D426 G4): moscosomartir2017 #7 (probe M1).
- G3 (minor) The 10-character unit-org gap in `_window_checks` lets a short second org printed between the unit and the
  org pass as "contiguous" (bayoumi2025, probe B2). Harmless here (question 1), but a ruling should say when it is
  intended.

## Coordinator questions

1. Apply F1, N1 and N2 now, then re-run `check lit_h25 --corpus lit`? Recommended: yes, before `aggregate`; rows
   182 -> 184.
2. Accept the recommendations on questions 1-4, with a ruling for comma-joined org pairs after a unit chain (question
   1)?
3. Add bolk2018 #6 to the D426 review list (not D412), and poulton2017 block 4 / moscosomartir2017 #7 to the
   re-record list after the G1 / G2 checker fixes?

## Verdict

GO. No slot carries a wrong person, org, unit, city, country or marker, nothing is invented, no block is missed, and no
address or contact text is recorded. 2 slots should take the joint-unit form (F1, field changes only); 5 slots wait on
known checker gaps and are correct as far as recorded.
