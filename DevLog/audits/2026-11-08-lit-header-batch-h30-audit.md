---
title: Fresh-context audit of the lit author-affiliation batch lit_h30 (21 papers)
date: 2026-11-08
auditor: Claude (fresh context; wrote only this record; headers.yaml, derived files, scripts, tests, people and registry data not edited; check run only with --dry-run, probes on a scratch copy; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h30/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369, D400-D522; format from the 2026-11-06 h27 audit
verdict: GO for the people rebuild (no slot wrong); 162 slots audited, 141 ok, 21 imprecise, 0 wrong; F1-F3 (notes only) fixable now; B1-B6 (21 slots) wait on checker changes or a ruling; nothing applied
---

# Lit header batch audit: lit_h30 (2026-11-08)

## Scope

Batch lit_h30 (21 papers: 2 IEEE footnote-prose papers, 2 Nature-family papers with footnote blocks, 1 Nature
Photonics cover-page reprint, 1 trade-journal article, 15 Optica / AIP / SPIE / preprint headers; 162 author-list
slots plus 1 header-only author; 157 rows). Restricted corpus: this record names only authors, orgs, units, cities and
countries; no paper text is quoted and no contact, street, building, site or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h30 --corpus lit --codes <id> --pdf`
  (all 21; scratchpad only); helgason2023 and jung2018 also with `--pages 2 2` (page 1 is a cover in both).
- Per slot: printed name vs `compare.csv` slot, printed marker run vs `markers` + `dropped_markers`, prose subject vs
  carriers, block fields vs the print (org, unit, campus, city, country), present addresses, parents, locator. All 46
  distinct (paper, marker, role, org, unit, place, basis, locator, org id) tuples of `header_rows.csv` read; no wrong
  mapping.
- Name pairs: every `compare.csv` pair whose folded tokens differ (31) read against D287 / D369; `strict_compatible`
  tested directly on the lai2025 pairs.
- Missed blocks: cue scan of the whole `text.md` of all 21 (now with / at, present / current address, current / present
  affiliation, currently, presently, also with, was / were with, on leave, visiting, formerly, deceased, permanent
  address). Header hits: jung2020 (Current address line, author 2) and kanazawa2016 (parenthetical currently in block 3).
  All other hits are body text or biographies (kashiwazaki2021 page 7). No missed block. Legend scan: huang2016
  dagger legend found on page 7 (equal contribution).
- Claims tested with dry-run probes on a scratch copy of the batch (`probe.py` in the session scratchpad, module
  `LIT_BASE` pointed at the copy; md5 of every repo batch file asserted unchanged after all probes).
- Stamp: `check_stamp.txt` matches `headers.yaml` (sha256 f5d758e8...). `headers.yaml`, stamp and derived files all
  12:07. Repo batch files untouched by this audit.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h30 | 21 / 21 | 162 | 141 | 21 | 0 |

- Rows 157 (all grade A: printed 110, single 30, prose 17; primary 149, additional 8, present address 0); recorded 139,
  no_header 23; papers ok 17, partial 2 (kramnik2024, lacava2016), unreadable 2 (hu2022, kashiwazaki2021);
  `author_list_differs` 2 (helgason2023 header-only author, lai2025 #2); explicit slots 4 (warnings: hazan2022 #1,
  jia2014 #7, lacava2016 #2, levy2026 #8); 11 unmapped org strings; multi-affiliation slots 7.
- Imprecise by cause (all wait on a checker change or a ruling; none fixable by a YAML edit today): hu2022 #1-#11
  (blocks printed before the author line, B5); lacava2016 #1 #4 #5 #6 (glued letter marker, B3); kramnik2024 #4 #5
  (Eth letter dropped by the fold, B2); lai2025 #1 #4 (D369 initials not compared, B1); jung2020 #2 (Current address
  cue, B4); kanazawa2016 #4 (parenthetical present address, B6). The 21 slots are distinct.
- ok includes kashiwazaki2021 #1-#6 (no affiliation in a recordable form; unreadable is the contract outcome) and
  lai2025 #2 (slot 0, list defect).
- Per paper (slots / rows): hazan2022 6 / 6; helgason2023 5 / 5; horst2013 6 / 6; hu2021b 10 / 13; hu2022 11 / 0;
  huang2016 7 / 8; ji2020 7 / 7; jia2014 9 / 10; jiang2016 11 / 11; jung2018 6 / 6; jung2020 11 / 11; kanazawa2016 8 / 8;
  kashiwazaki2021 6 / 0; kashiwazaki2021a 6 / 7; kervazo2025 5 / 15; kiani2023 4 / 4; kramnik2024 11 / 9; lacava2016
  10 / 8; lai2025 7 / 6; levy2026 11 / 11; li2019 5 / 6.

## Per-paper findings

| paper | slots | rating | evidence (locator) |
|---|---|---|---|
| hazan2022 | 6 | ok | p.1 footnote, two prose statements: Photonic Integration Group, Electrical Engineering, Eindhoven University of Technology, Eindhoven, NL (authors 1, 3, 5, 6); SMART Photonics, Eindhoven, NL (authors 2, 4). #1 printed Joel Hazan, list J.P. Hazan: missing second initial on a distinctive family name, explicit slot (D287 / D369) correct. #4 list carries extra initials (auto match, fine) |
| helgason2023 | 5 (+1) | ok | page 1 repository cover; page 2 author line (no markers) and one unmarked block (Department of Microtechnology and Nanoscience, Chalmers University of Technology, Gothenburg, SE) printed at the foot of the first article page. `single`, `p.2 header` per the contract cover-page rule (D366; lit_h07 precedent). Victor Torres-Company printed 6th, absent from the 5-name list: `slot: 0` + `author_list_differs` correct (as zhao2025, D522). Locator question: Q1 |
| horst2013 | 6 | ok | p.1 header, markers 1-3 as printed; IBM Research - Zürich, Rüschlikon, CH; IBM Research – T.J.Watson Research Center, Yorktown Heights, US (dash form kept, D426); IBM Systems &Technology Group (as printed), unit Microelectronics Division, Essex Junction, US (country on the next line). Asterisk is the contact line |
| hu2021b | 10 | ok | p.1 footnote (Nature list at the foot of page 1, `p.1 footnote` set): 1 Harvard SEAS, 2 Harvard Physics (Cambridge, US), 3 Caltech Division of Physics, Mathematics and Astronomy, 4 Alliance for Quantum Technologies (AQT) (Pasadena, US), 5 HyperLight Corporation (Cambridge, US). Marker runs 1,2 / 1,3,4 / 5 match; envelope symbol ignored |
| hu2022 | 11 | imprecise (B5) | p.1: both layers print the six marked blocks (Harvard SEAS; Harvard Physics; USC Ming Hsieh Department of Electrical and Computer Engineering, Los Angeles; Stanford Edward L. Ginzton Laboratory, Department of Electrical Engineering, Stanford; Caltech division and AQT, Pasadena; HyperLight Corporation, Cambridge; all US) and the equal-contribution line before the title and author line. Probe U1 (all six blocks recorded): 16 errors, every block fails the after-author-line position check. `unreadable` with the printed values in the note is the lit_h13 precedent; the note values match the print. No row is wrong; 11 slots lack rows |
| huang2016 | 7 | ok | p.1 header, capitals author line, markers 1-4; University of California + campus Santa Barbara + locality Santa Barbara (no separate city printed; lit_h07 huang2019 and 42 committed UCSB blocks carry the same form); Scuola Superiore Sant’Anna, Pisa, IT; Morton Photonics, West Friendship, US; Tokyo Institute of Technology, Department of Electrical and Electronic Engineering/FIRST, Tokyo, JP. Note imprecise: the dagger legend (equal contribution) is printed on page 7 (F1) |
| ji2020 | 7 | ok | p.1 header; two Columbia University departments, New York, US; marker runs match |
| jia2014 | 9 | ok | p.1 header; Institute of Microelectronics, Singapore, SG (A*STAR parent not copied, site name left out); Jilin University with the state key laboratory + college unit chain, Changchun, CN. #7 printed Sing-Chee Koh, list Koh Sing Chee: name-order swap, explicit slot; D426 review list (as zhang2022b, D522) |
| jiang2016 | 11 | ok | p.1 header; Shanghai Jiao Tong University with the state key lab + department chain, Shanghai, CN (same form as 6 committed SJTU blocks); École de technologie supérieure, Laboratoire de Technologies de Réseaux, Montreal, CA |
| jung2018 | 6 | ok | page 1 citation cover; page 2: University of Southampton, Optoelectronics Research Centre, Southampton, GB; Fujikura Ltd., Sakura, JP (district before the city left out, D366). `p.2 header` correct |
| jung2020 | 11 | 10 ok, #2 imprecise (B4) | p.1 header, capitals; block 1 Southampton ORC. Author 2 carries 1,2,4: block 2 is a Current address line (Hongik University, Electrical and Electronic Convergence Department, Sejong, KR). Probe J1 (block recorded as present address): 2 errors, cue not accepted (D442 gap). Marker 2 under `dropped_markers` is the lit_h17 precedent; 3 and 4 are contact lines |
| kanazawa2016 | 8 | 7 ok, #4 imprecise (B6) | p.1 header; NTT Corporation with NTT Device Innovation Center / NTT Device Technology Laboratories, Atsugi City, JP; block 3 NTT Photonics Laboratories, Atsugi City, JP (no parent printed; recorded as printed, as two committed prose blocks). Block 3 also prints Hokkaido University in parentheses with a currently cue and no own marker: author 4's present address is not expressible (one marker, two roles) |
| kashiwazaki2021 | 6 | ok | trade-journal article: page 1 author line with no affiliation; orgs only in the end biographies (page 7). Contract has no biography format: `unreadable` correct (Q3) |
| kashiwazaki2021a | 6 | ok | p.1 header, parenthesis markers; NTT Corporation, NTT Device Technology Labs, Atsugi, JP; The University of Tokyo, Department of Applied Physics, School of Engineering, Tokyo, JP (ward before the city left out); RIKEN Center for Quantum Computing, Optical Quantum Computing Research Team, Wako, JP. a) and b) are contact lines (`dropped_markers` correct) |
| kervazo2025 | 5 | ok | p.1 header, one unmarked block: Univ Rennes, CNRS, Institut FOTON (UMR number dropped), Lannion, FR; org + `more_orgs` in printed order (D285; committed Rennes / FOTON blocks use the same structure) |
| kiani2023 | 4 | ok | p.1 header; one block printed with a 1 that no author carries: `single`, `markers: []` (D285); McMaster University, Department of Engineering Physics, Hamilton, CA |
| kramnik2024 | 11 | 9 ok, #4 #5 imprecise (B2) | p.1 header; UC campus Berkeley (D301), Boston University (department + Photonics Center), Northwestern University (center + department), Evanston. Author 5 starts with U+00D0 (Eth) in both layers; `fold_text` drops it (tested: Gluhović folds to orde gluhovic), so the name is not found and author 4's run then fails. Probes K1 (both readable): 5 errors; K2 (author 4 only): 2 errors; K3 (U+0110 spelling): 7 errors incl. slot loss. `partial` with both unreadable is the only passing form; both are printed with marker 2 (Boston University) |
| lacava2016 | 10 | 6 ok, #1 #4 #5 #6 imprecise (B3) | p.1 header (SPIE); block a (University of Pavia, Dept. of Electrical, Computer and Biomedical Engineering, Pavia, IT) has its marker glued to the unit in both layers. Probe L1 (block a recorded, authors 4-6 marker a, author 1 a,b): 15 errors, block a fails the word-start test in both layers (D416 G1 gap). Block e passes only because its unit LETI is located first and CEA + e sit directly before it. Blocks b Southampton ORC, c Pavia Dept. of Physics, d Tyndall National Insitute (misspelling as printed; building not recorded), Cork, IE, e CEA / LETI, Grenoble, FR correct. #2 Lee Carrol / L. Carroll spelling variant, explicit slot (D287) |
| lai2025 | 7 | 4 ok + #2 ok, #1 #4 imprecise (B1) | p.1 header, one block: National Yang Ming Chiao Tung University, Department of Photonics, Hsinchu, TW. #2 printed Li-Sheng Hu, list Ling Hu: different given name, `slot: 0` correct (D369). #1 printed Yong-Wei Lai vs list Y. Y. Lai and #4 Tien-Chiu Chen vs T.R. Chen: the second initials (W vs Y, C vs R) are not explained, which D369 makes `slot: 0` for common family names. The checker matched both because `strict_compatible` returns early when the abbreviated form has no more initials than the full form and never compares them (G1). Probe N1 (`slot: 0` on both): 2 errors (D302), so the D369 outcome is not recordable now. The note sends them to the D426 review list; they are D369 / D412 cases (F2) |
| levy2026 | 11 | ok | p.1 footnote, one prose statement for all authors: Intel Corporation, Santa Clara, US. Asterisks = equal contribution. #8 list name in Chinese script, printed Junyi Gao (consistent transliteration), explicit slot; under D413 such a list name builds no lit slot, so it needs a D412 correction entry. A stray K after the last author name has no legend (F3) |
| li2019 | 5 | ok | p.1 header; University of Rochester, Department of Electrical and Computer Engineering / Institute of Optics, Rochester; only a US state code printed, `country: ""` correct (D249) |

## Fixes (exact YAML edits; F1-F3 now, B1-B6 after the named change)

Fixable now (notes only; rows unchanged at 157; re-run `check lit_h30 --corpus lit` afterwards to refresh the stamp):

- F1 huang2016 `note`: "the dagger on authors 1 and 2 has no printed legend on page 1 (ignored)" -> "the dagger on
  authors 1 and 2 marks equal contribution (legend printed on page 7; symbol, no entry needed)".
- F2 lai2025 `note`: "authors 1 and 4 matched by the checker to the list forms Y. Y. Lai and T.R. Chen although the
  second initials differ from the printed given names (for the D426 review list)" -> "authors 1 and 4 matched by the
  checker to the list forms Y. Y. Lai and T.R. Chen although the second initials are not explained by the printed given
  names (D369 slot 0 case; the checker compares only the number of initials: re-record after the fix, D412 list)".
- F3 levy2026 `note`: after "asterisks mark equal contribution;" insert " a K printed after the last author name has no
  legend (ignored);".

Blocked (apply only after the named checker change or ruling; each turns imprecise slots into ok):

- B1 (after G1: `strict_compatible` compares the initials position by position when the abbreviated form has as many
  initials as the full form) lai2025: `{name: "YONG-WEI LAI", markers: []}` -> `{name: "YONG-WEI LAI", markers: [], slot: 0}`;
  `{name: "TIEN-CHIU CHEN", markers: []}` -> `{name: "TIEN-CHIU CHEN", markers: [], slot: 0}`; note as F2 with the
  last sentence replaced by "slot 0 (D369), D412 list". Rows 6 -> 4 (no row for an unmatched list name).
- B2 (after G2: `FOLD_FIX` maps U+00D0 / U+00F0 to D / d, and U+0110 / U+0111 stay D / d) kramnik2024: authors 4 and 5
  `markers: [], unreadable: true` -> `markers: ["2"]`; `status: partial` -> `ok`; note: drop the Eth sentence. Rows 9 -> 11.
- B3 (after the glued-letter-marker gap D416 G1) lacava2016: insert before block b
  `{marker: "a", basis: printed, org: "University of Pavia", unit: "Dept. of Electrical, Computer and Biomedical Engineering", locality: "Pavia", country: "IT"}`;
  author 1 `markers: ["a", "b"]` (drop `dropped_markers`); authors 4, 5, 6 `markers: ["a"]` (drop `unreadable`);
  `status: ok`; note: drop the block a sentence. Rows 8 -> 12.
- B4 (after the Current address cue fix D442) jung2020: add
  `{marker: "2", basis: printed, role: present_address, org: "Hongik University", unit: "Electrical and Electronic Convergence Department", locality: "Sejong", country: "KR"}`;
  author 2 `markers: ["1", "2"]`, `dropped_markers: [{marker: "4", reason: "contact footnote"}]`; note: drop the gap
  sentence. Rows 11 -> 12.
- B5 (after a checker mode for blocks printed before the author line, or a ruling to verify them without the position
  check) hu2022: record the six blocks listed in its note (`p.1 footnote`), authors in printed order with markers
  Yaowen Hu 1,2; Mengjie Yu 1,3; Brandon Buscaino 4; Neil Sinclair 1,5; Di Zhu 1; Rebecca Cheng 1; Amirhassan
  Shams-Ansari 1; Linbo Shao 1; Mian Zhang 6; Joseph M. Kahn 4; Marko Lončar 1; marker 7 on authors 1 and 2 to
  `dropped_markers` (equal contribution). Block 5 prints the Caltech division and AQT before California Institute of
  Technology: org Caltech with the division as unit and AQT in `more_orgs` needs the same unit-org gap change as h27 G2;
  until then AQT stays inside the unit as in probe U1.
- B6 (ruling needed) kanazawa2016 #4: a present address printed in parentheses inside a marked block has no marker of
  its own. Proposed: a `present_address` sub-field on the block (org, locality, country) checked inside the block
  window with the currently cue; then Hokkaido University (no city printed, country JP from the block) for author 4.

## Open questions (with recommendation)

1. helgason2023 locator: the block is a first-article-page footnote (h27 F1 / D522 would give `p.2 footnote`), but the
   contract cover-page rule says `p.N header` so the checker skips the cover (lit_h07 precedent, same layout). Probe
   H1 (`p.2 footnote`): 0 errors, but only because the cover prints abbreviated names that do not match; the search
   then starts on page 1. Recommended: keep `p.2 header` (contract wording); if the footnote position should be kept,
   extend `lit_search_pages` so any `p.N` locator of a paper whose page 1 is a cover sets the base, then switch.
2. G1 (D369 implementation): `strict_compatible` skips the comparison when the abbreviated form has no extra
   initials, so a hyphenated given name (two syllables) accepts any second initial (Yong-Wei ~ Y. Y., Tien-Chiu ~
   T. R.), while the joined form (Yongwei ~ Y. Y.) is rejected. Recommended: compare initials position by position, with
   a test on these two pairs; then apply B1 and sweep committed lit batches for automatic matches of this shape.
3. kashiwazaki2021: the end biographies name each author's group and lab (NTT Device Technology Laboratories). They
   are not header, footnote or prose-statement blocks. Recommended: keep `unreadable` (no new format for one trade
   journal article).
4. Lists: helgason2023 Victor Torres-Company (missing from the list, same defect as zhao2025) and lai2025 #2 Ling Hu /
   Li-Sheng Hu, #1 Y. Y. Lai, #4 T.R. Chen to the D412 correction file; levy2026 #8 (Chinese-script list name, D413:
   no slot built) to the D412 file as Junyi Gao; jia2014 #7 (order swap) to the D426 review list. Re-record list:
   B2-B5 after their checker fixes; B6 after a ruling.
5. Unmapped org strings for the org round (11): Alliance for Quantum Technologies (AQT); Boston University (with its
   unit); IBM Research – T.J.Watson Research Center; IBM Systems &Technology Group; Institut FOTON; McMaster University
   (with its unit); Morton Photonics; NTT Photonics Laboratories; RIKEN Center for Quantum Computing; Tyndall National
   Insitute (printed misspelling); Univ Rennes. Boston University and McMaster University are plain names and
   probably need only an alias.

## Privacy and as-printed scan

- Scan of `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`, `papers.csv`: contact / URL patterns,
  digit runs of 4 or more, street and building words, and the street, site, building and postal strings printed on the
  header pages of all 21 papers. Result: 0 hits except paper-id years in the CSVs. Notes mention left-out site,
  district, ward and building names only generically.
- As printed (kept, correct): Tyndall National Insitute; IBM Systems &Technology Group (no space); IBM Research dash
  forms; Atsugi City and Atsugi as printed in their papers; Scuola Superiore Sant’Anna with its typographic apostrophe.
- No `skip_prefix`, `skip_between`, `continued` or `clause` in this batch.

## Commands (2026-11-08, log times)

| Command | Result |
|---|---|
| `show lit_h30 --corpus lit --codes <id> --pdf`, all 21, plus `--pages 2 2` for helgason2023 and jung2018, 12:08-12:10 | headers and author lists read (scratchpad only) |
| `check lit_h30 --corpus lit --dry-run` 12:08:16 (pid 17050) | 0 errors, 4 warnings (explicit slots hazan2022 #1, jia2014 #7, lacava2016 #2, levy2026 #8); slots 162, recorded 139, no_header 23; rows 157; papers ok 17 / partial 2 / unreadable 2; 11 unmapped org strings |
| `probe.py` on a scratch copy, dry-run, 12:09-12:15 | results below; repo batch files md5 unchanged |

| probe | change | result | reading |
|---|---|---|---|
| base0 | unchanged copy | 0 errors | harness reproduces the repo check |
| K1 / K2 / K3 | kramnik2024 authors 4-5 readable / author 4 only / U+0110 spelling | 5 / 2 / 7 errors | B2: fold gap, partial required |
| L1 | lacava2016 block a recorded, authors 1, 4-6 carry a | 15 errors (block a word start, both layers) | B3: glued marker gap |
| N1 | lai2025 #1 #4 `slot: 0` | 2 errors (D302) | B1 needs G1 first |
| H1 | helgason2023 `p.2 footnote` | 0 errors | Q1 is a contract call |
| J1 | jung2020 block 2 as present address | 2 errors (cue) | B4: D442 gap |
| U1 | hu2022 six blocks recorded | 16 errors (block position) | B5: unreadable required |

## Checker gaps observed (scripts not edited)

- G1 `strict_compatible` (D369) compares initials only when the abbreviated form has more of them (lai2025 #1 #4).
- G2 `FOLD_FIX` drops U+00D0 (Eth, used for the Serbo-Croatian D with stroke), so names starting with it cannot be
  located (kramnik2024 #5, and through it #4).
- Known, reconfirmed: glued letter marker at a block start (D416 G1, lacava2016); Current address cue (D442,
  jung2020); blocks printed before the author line (lit_h13, hu2022); a single locator conflating the search base with
  the block position on cover-page papers (helgason2023).

## Verdict

GO. No slot carries a wrong person, org, city, country or marker, nothing is invented, no block is missed, and no
address or contact text is recorded. Three notes need a wording fix (F1-F3). 21 slots lack rows or carry a
match D369 would reject, each waiting on a named checker change (G1, G2, D416 G1, D442, block position) or a
ruling (B6).
