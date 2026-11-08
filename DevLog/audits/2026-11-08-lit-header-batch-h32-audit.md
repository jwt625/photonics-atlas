---
title: Fresh-context audit of the lit author-affiliation batch lit_h32 (21 papers)
date: 2026-11-08
auditor: Claude (fresh context; wrote only this record; headers.yaml, derived files, scripts, tests, people and registry data not edited; check run only with --dry-run; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h32/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369, D380, D406-D413, D416, D426, D442, D449, D461, D466, D521, D522; format from the 2026-11-06 h27 audit
verdict: GO for the people rebuild (no slot wrong); 217 slots audited, 214 ok, 3 imprecise, 0 wrong; nothing fixable now except one optional note edit (N1); C1 (1 slot, present address) waits on the D442 cue gap, C2 (2 slots, street / building span between unit and org) waits on the D426 G6 gap; nothing applied
---

# Lit header batch audit: lit_h32 (2026-11-08)

## Scope

Batch lit_h32 (21 papers: 1 IEEE footnote-prose paper, 2 Nature-family papers with first-page footnote blocks, 1 ACS
accepted manuscript with a cover page, 1 Electronics Letters paper with end-of-letter grouped blocks, 1 OFC paper,
15 Optica / OSA journal papers and preprints; 217 author-list slots plus 1 header-only author; 245 rows). Restricted
corpus: this record names only authors, orgs, units, cities and countries; no paper text is quoted and no contact,
street, building, site or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h32 --corpus lit --codes <id> --pdf`
  (all 21; output in the session scratchpad only); salamin2018 and simpanen2017 also with `--pages 2 2` (cover page;
  end-of-letter blocks). Both text layers carry every marker legibly; no page render needed.
- Per slot: printed name vs the `show` author list and `compare.csv`, printed marker run vs `markers` +
  `dropped_markers`, prose subject vs carriers (roeloffzen2018), grouped position (radosavljevic2017, simpanen2017),
  block fields vs the print (org, unit, campus, city, country, role), locator, notes.
- Contact footnotes: the masked lines of shim2026 (markers 3, 4) and sacher2017 (markers 5, 6) checked in the PDF
  span layer (first character only, address masked in the probe output): each starts with the dropped marker.
- Missed blocks: cue scan of the whole `text.md` of all 21 (now with / at, present / current address, current /
  present affiliation, currently, presently, also with, was / were with, is / are with, on leave, visiting, formerly,
  deceased, permanent address). Header hits: purnawirman2017 (Current address line, see C1), rizzo2023 (two Present
  address blocks, recorded), roeloffzen2018 (five statements and one clause, recorded). All other hits are body text
  or a biography on a later page. No missed block.
- Probes: `probe.py` (session scratchpad) on a scratch copy of the batch through the module's `LIT_BASE`, dry-run;
  md5 of every repo batch file asserted unchanged before and after.
- Stamp: `check_stamp.txt` matches `headers.yaml` (sha256 7dd8de97...). `headers.yaml` mtime 12:07:19, stamp and
  derived files 12:07:26. Repo batch files md5-identical before and after this audit.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h32 | 21 / 21 | 217 | 214 | 3 | 0 |

- Rows 245 (all grade A: printed 169, prose 30, single 32, grouped 14; primary 218, additional 25, present address
  2); locators p.1 header 178, p.1 footnote 50, p.2 header 9, p.2 affiliations 8. Recorded 216, no_header 1
  (shim2026 #2); papers ok 21, partial 0, unreadable 0; `author_list_differs` 1 (shim2026); explicit slots 7
  (purnawirman2017 #1, roeloffzen2018 #6 #19, shen2016 #5, shen2020 #12, simpanen2017 #3 #4) plus 1 `slot: 0`;
  14 unmapped org strings; `order_differs` false on all 217.
- Imprecise by cause: checker gap D442 (C1: purnawirman2017 #13); checker gap D426 G6 (C2: smith2023 #1, #4). No
  slot is imprecise for a reason fixable now.
- Per paper (slots / rows): poulton2016 9 / 10; purnawirman2017 14 / 15; qubaisi2020 2 / 2; radosavljevic2017 3 / 6;
  raja2019 14 / 20; rizzo2023 11 / 16; roeloffzen2018 28 / 30; saber2017 11 / 11; sacher2017 12 / 12; salamin2018
  9 / 9; selvaraja2014 12 / 12; shen2015 4 / 4; shen2016 8 / 9; shen2020 17 / 18; shi2013 9 / 9; shi2013a 10 / 10;
  shim2026 8 / 8 (7 with rows); simpanen2017 8 / 8; smith2023 4 / 6; soltanian2022 16 / 21; song2013 8 / 9.

## Per-paper findings

| paper | slots ok / imp / wrong | finding |
|---|---|---|
| poulton2016 | 9 / 0 / 0 | 3 printed blocks (MIT RLE, Harvard SEAS as printed with singular Science, University at Albany CNSE), all Cambridge / Albany, US; author 5 carries 1, 2 |
| purnawirman2017 | 13 / 1 / 0 | blocks 1-3 as poulton2016; author 1 single-name, explicit slot 1 matches the single list name; author 13 marker 4 points to a Current address block (McMaster University, Department of Engineering Physics, Hamilton, Canada), kept as `dropped_markers` per the lit_h05 / h16 / h17 / h21 / h25 precedent: C1 |
| qubaisi2020 | 2 / 0 / 0 | single unmarked block, Boston University ECE, Boston, US; detached accent in Popović folded |
| radosavljevic2017 | 3 / 0 / 0 | no markers; author group above two unmarked blocks, `grouped` G1 / G2 on every author (D368); G1 Ghent University - imec dash form kept (D426); G2 prints the centre with no university (probe R1: Ghent University not in the block, 4 errors), so the centre as org is as printed |
| raja2019 | 14 / 0 / 0 | 4 printed blocks; EPFL Lausanne CH, Russian Quantum Center Moscow RU, MIPT Dolgoprudny RU, Moscow State University with Faculty of Physics as unit; asterisk / dagger / double dagger used by no block |
| rizzo2023 | 11 / 0 / 0 | first-page footnote blocks with `p.1 footnote`; AFRL with Information Directorate unit, Rome, US; markers 4 / 5 Present address (Shanghai Jiao Tong University John Hopcroft Center, Shanghai CN; University of Cambridge Engineering Department, Cambridge GB) as present addresses of authors 5 / 8; marker 6 equal contribution dropped on authors 1-3 |
| roeloffzen2018 | 28 / 0 / 0 | five prose statements + one clause, all subjects match carriers: P1 (20 authors) and P2 LioniX International BV, Enschede NL; P3 clause and P4 University of Twente with the group + MESA+ institute chain, Enschede NL; P5 University of Sydney with the centre, no city printed (locality empty, D288); P6 Monash University with the laboratory chain, Clayton AU; explicit slots #6 (Denys vs D. V. Marchenko, distinctive family name, D369 / D287) and #19 (Paulus vs Paul, D287) accepted; Ronald Dekker vs Ronald Haentjens Dekker automatic (dropped family-name part) |
| saber2017 | 11 / 0 / 0 | single unmarked block, McGill University ECE, Montreal, CA |
| sacher2017 | 12 / 0 / 0 | 3 printed blocks; Huawei Technologies Canada Co. Ltd., Kanata CA; Institute of Microelectronics, Singapore SG (A*STAR parent not copied, contract); markers 4 equal contribution and 5 / 6 contact lines dropped (verified) |
| salamin2018 | 9 / 0 / 0 | cover page; author line and single block on page 2 (`p.2 header`, D366); ETH Zurich + IEF unit, Zurich CH; header form Yuriy Fedoryshyn (page 2) vs list with middle name, automatic. Note detail: N1 |
| selvaraja2014 | 12 / 0 / 0 | OFC one-line blocks: imec Leuven BE, Ghent University-imec Ghent BE, Soitec Bernin FR |
| shen2015 | 4 / 0 / 0 | Nature Photonics foot-of-page blocks with `p.1 footnote`; University of Utah ECE and Utah Nanofabrication Facility, Salt Lake City, US |
| shen2016 | 8 / 0 / 0 | 3 printed blocks (TU/e two groups, Ghent University-IMEC Photonics Research Group); #5 J. P. vs Jorn van Engelen explicit slot (distinctive family name, D369 / garciablanco2025 precedent) |
| shen2020 | 17 / 0 / 0 | 4 printed blocks; block 2 University of California + campus Santa Barbara (printed without a comma, D301 / D449; maps to `org_ucsb`); EPFL long form with Institute of Physics; #12 Dave vs David explicit slot (D287) |
| shi2013 | 9 / 0 / 0 | UBC ECE Vancouver CA, University of Delaware ECE Newark US |
| shi2013a | 10 / 0 / 0 | single unmarked block, UBC ECE Vancouver CA |
| shim2026 | 7 / 0 / 0 (+1 without rows, ok) | Harvard SEAS (plural Sciences as printed) and KAIST School of Electrical Engineering, Daejeon KR; printed second author Seonghun Kim vs list S. J. Kim: the J is not explained, common family name, so `slot: 0` + `author_list_differs` is the D369 outcome (probe K1: removing it fails; K2: forcing slot 2 passes, so the rule, not the checker, decides); markers 3 / 4 contact lines (verified); detached caron in Lončar folded |
| simpanen2017 | 8 / 0 / 0 | author line on page 1, author groups reprinted with parenthesized blocks at the end of the letter on page 2 (`grouped`, `p.2 affiliations`): Chalmers University of Technology with the Photonics Laboratory / department chain, Göteborg SE; Hewlett Packard Enterprise, Palo Alto US. The author list carries Emanuel P. Haglund in slots 3 and 4; printed E. Haglund and E.P. Haglund both fit that form (probe H2: 2 slots each, 3 errors), so explicit slots are required; position order (3, 4) chosen (probe H1: the swap also passes, with an order warning). The print gives no given name for author 3: list defect, D412 (question 2) |
| smith2023 | 2 / 2 / 0 | block 1 prints Institute of Photonics, a department, a street and building span, then University of Strathclyde, Glasgow, UK; recorded as org Institute of Photonics + `more_orgs` University of Strathclyde, department dropped, as lit_h17 cabezon2012 (D426 G6). Target form University of Strathclyde + unit chain fails contiguity (probe S1, 2 errors) and the span cannot go into `skip_between` (street text, D244): C2. Block 2 LIGENTEC, Ecublens CH correct (site and street not recorded) |
| soltanian2022 | 16 / 0 / 0 | 6 printed blocks: Ghent University-IMEC PRG; Ghent University with the Center for Nano- and Biophotonics as unit (university printed here, unlike radosavljevic2017); IMEC Heverlee; Brolis Sensor Technology BV Zwijnaarde; EV Group E.Thallner GmbH, St. Florian am Inn AT; III-V Lab Palaiseau FR |
| song2013 | 8 / 0 / 0 | IME Singapore (A*STAR parent not copied); Jilin University with the state key laboratory + college chain, Changchun CN (same form as the committed Jilin rows) |

## Fixes (exact YAML edits; none applied)

No slot carries a field that can be corrected now. One optional note edit:

| # | paper | edit (before -> after) | rows |
|---|---|---|---|
| N1 | salamin2018 `note` | "asterisks and hash signs on authors 1, 2 and 9 are used by no block" -> "asterisks on authors 1, 2 and 9 and hash signs on authors 1 and 2 are used by no block" (page 2 prints the hash sign only on authors 1 and 2) | unchanged (9) |

Re-record items, to apply only after the named checker change (values verified against the print):

| # | paper, slots | after | edit |
|---|---|---|---|
| C1 | purnawirman2017 #13 (Jonathan D. B. Bradley) | D442 cue fix ("Current address" accepted as a present-address cue; probe Q1 today: 2 errors, marker + first field) | add after block 3: `- {marker: "4", basis: printed, role: present_address, org: "McMaster University", unit: "Department of Engineering Physics", locality: "Hamilton", country: "CA"}`; author 13: `{name: "JONATHAN D. B. BRADLEY", markers: ["1", "4"]}` (drop `dropped_markers`); note: remove the sentence on block 4 and the cue. Rows 15 -> 16 |
| C2 | smith2023 #1 (Jack A. Smith), #4 (Michael J. Strain) | D426 G6 (verified, never-stored skip for a street / building span between unit and org) | block 1: `{marker: "1", basis: printed, org: "University of Strathclyde", unit: "Institute of Photonics, Dept. of Physics", locality: "Glasgow", country: "GB"}` plus the G6 skip field; note: replace the parenthetical on block 1 with "(the unit chain is printed before a street and building span and the university, D426 G6)". Rows 6 -> 4; consistent with the lit_h23 grouped Strathclyde block (University of Strathclyde + Institute of Photonics, Department of Physics) |

Any change to the YAML changes its hash: re-run `check lit_h32 --corpus lit` afterwards to refresh the stamp.

## Open questions (with recommendation)

1. N1: apply now? Recommended: yes (note only, rows unchanged).
2. simpanen2017 #3: the author list repeats Emanuel P. Haglund for the printed E. Haglund (given name not printed).
   Slot 3 will carry the list name Emanuel P. Haglund (D359), giving that person two slots on one paper in the
   people build. Recommended: keep the header record (correct as printed) and add slot 3 to the D412 author-list
   correction file, as chang2026a (Ting Xu twice, D416 (3)); do not invent the given name.
3. shim2026 #2: list S. J. Kim vs printed Seonghun Kim (D369 non-match). Recommended: header-only author list as
   liang2025 / song2008 / wang2026 (D369), and add to the D412 correction file only if a source for the list form
   is found; no slot forced (probe K2 shows the checker would accept it, so the rule must hold).
4. radosavljevic2017 G2 (Center for Nano- and Biophotonics as its own org, no university printed) vs soltanian2022
   block 2 and 8 blocks in lit_h02, h04, h07, h11, h12, h19 (Ghent University + the centre as unit): accept as printed (D249, never invent);
   the org round may alias the bare centre to Ghent University (one unmapped string).
5. C1 / C2 to the re-record lists after the D442 and G6 checker changes.

## Privacy and as-printed scan

- `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`, `papers.csv` scanned for contact / URL
  patterns, digit runs of 4 or more, and the street, building and site words printed in the 21 headers: 0 contact or
  URL hits, 0 street / building / postal strings; digit runs are paper-id years only. Notes name only the kind of
  text left out (street address, building name, site name, district, postal code).
- No `skip_prefix` or `skip_between` in this batch.
- As printed (kept, correct): Harvard SEAS singular Science (poulton2016, purnawirman2017) vs plural (shim2026);
  Ghent University - imec / Ghent University-imec / Ghent University-IMEC dash forms (D426); MESA+Research without a
  space (roeloffzen2018); State Key Laboratory on Integrated opto-electronics lower case (song2013, as committed);
  ECE Department (shen2020); EV Group E.Thallner GmbH.

## Commands (2026-11-08, log times)

| Command | Result |
|---|---|
| `show lit_h32 --corpus lit --codes <id> --pdf`, all 21, plus `--pages 2 2` for salamin2018 and simpanen2017, 12:11-12:13 | headers and author lists read (scratchpad only) |
| `check lit_h32 --corpus lit --dry-run` 12:11:04 (pid 22022) | 0 errors, 5 warnings (explicit slots); slots 217, recorded 216, no_header 1; rows 245 (grade A 245; printed 169, prose 30, single 32, grouped 14; primary 218, additional 25, present address 2); papers ok 21; multi-affiliation slots 25; 14 unmapped org strings |
| `probe.py` on a scratch copy, dry-run, 12:15:56-12:16:40 (pid 26930; run logs in `logs/`, gitignored) | results below; repo batch files md5 unchanged |

| probe | change | result | reading |
|---|---|---|---|
| S1 | smith2023 block 1 University of Strathclyde + unit chain | 2 errors, unit and org not contiguous | C2 blocked by G6 |
| Q1 | purnawirman2017 marker 4 present-address block | 2 errors, marker + first field | C1 blocked by D442 |
| H1 | simpanen2017 Haglund slots swapped | 0 errors, order warning | slot choice is a convention; position order kept |
| H2 | simpanen2017 explicit slots removed | 3 errors, 2 slots each | explicit slots required |
| K1 | shim2026 `slot: 0` removed | 1 error, 0 slots | slot 0 required |
| K2 | shim2026 forced to slot 2 | 0 errors | D369 decides, not the checker |
| R1 | radosavljevic2017 G2 with Ghent University as org | 4 errors, org not in the block | centre as org is as printed |

## Verdict

GO. No slot carries a wrong person, org, unit, city, country, marker or role; nothing is invented; no block is
missed; no contact, street or postal text is recorded. Three slots wait on known checker gaps (C1 present-address
cue, C2 street span between unit and org) and are correct as far as recorded; one optional note edit (N1).
