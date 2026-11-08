---
title: Fresh-context audit of the lit author-affiliation batch lit_h31 (21 papers)
date: 2026-11-08
auditor: Claude (fresh context; wrote only this record; headers.yaml, derived files, scripts, tests, people and registry data not edited; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h31/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369, D380, D400-D522; format and precedent from the 2026-11-06 h27 audit
verdict: GO for the people rebuild (no slot wrong); 199 author-list slots audited, 184 ok, 15 imprecise, 0 wrong; F1 (13 slots, locator only) and N1 (note) fixable now; C1 (2 slots, parked block) waits on the D426 G6 checker gap; nothing applied
---

# Lit header batch audit: lit_h31 (2026-11-08)

## Scope

Batch lit_h31 (21 papers: 7 Optica-family journal papers, 5 arXiv preprints, 2 IEEE PTL footnote-prose papers, 2
Wiley papers, 3 conference papers, 1 ACS Just Accepted manuscript, 1 Optics Express single-block paper; 199
author-list slots, 180 recorded, 19 no_header; 205 rows). Restricted corpus: this record names only authors, orgs,
units, cities and countries; no paper text is quoted and no contact, street, building, site or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h31 --corpus lit --codes <id> --pdf`
  (all 21; liu2019 also with `--pages 2 2`); output kept in the session scratchpad only. Both text layers carry every
  numeric marker legibly; the detached accents of masanovic2003 and ortegamonux2013 are fold-equivalent (D282).
  ortegamonux2013 page 1 rendered once (scratch, deleted) to settle the block position.
- Per slot: printed name vs `compare.csv` slot, printed marker run vs `markers` + `dropped_markers`, prose subject vs
  carriers, grouped / per-author position, block fields vs the print (org, unit, campus, city, country), parents,
  locator. Every distinct (org, unit, place) tuple of `header_rows.csv` read; no wrong mapping. All 30 name-form
  differences between `meta_name` and `header_name` read (initials, dropped middle names, group forms, Jon /
  Jonathon); none is a different person.
- Missed blocks: cue scan of the whole `text.md` of all 21 (now with / at, present / current address, present /
  current affiliation, currently, presently, also with, is / are / was / were with, on leave, visiting, formerly,
  deceased, permanent address). Header hits only the two recorded "The authors are with" statements (ma2000,
  masanovic2003); every other hit is body text. No missed block, no present address in the batch.
- Symbol legends: the asterisk / dagger legends that notes cite for liu2018a and liu2020a are printed on a later page
  (equal contribution); legends of li2022 and ling2024 on page 1. Symbol marks used by no block need no entry (D286d).
- Claims tested with dry-run probes on a scratch copy of the batch (`probe.py`, module `LIT_BASE` pointed at the
  scratchpad; md5 of every repo batch file asserted unchanged after each run).
- Stamp: `check_stamp.txt` matches `headers.yaml` (sha256 e26f4ded...). `headers.yaml` mtime 12:06:50, stamp and
  derived files 12:06:57. Repo batch files untouched by this audit.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h31 | 21 / 21 | 199 | 184 | 15 | 0 |

- Recorded slots 180: ok 167, imprecise 13 (F1). no_header slots 19: ok 17 (liu2019 #2 and #9-#23 list duplicates,
  liu2018a #6 not printed in this version), imprecise 2 (C1, liu2024 #2 #7 parked).
- Rows 205, all grade A (printed 144, single 25, grouped 21, prose 10, per_author 5; primary 180, additional 25,
  present address 0); papers ok 20, partial 1 (liu2024), unreadable 0; `author_list_differs` 2 (liu2018a, liu2019);
  explicit slots: liu2019 (7, D412 list artefact) and masanovic2003 #3 (D287); `order_differs` li2022, liu2019,
  luquegonzalez2019 (name-matched, correct); 13 unmapped org strings.
- Per paper (slots / recorded / rows; rating): li2022 17 / 17 / 18 ok; li2023a 6 / 6 / 12 ok; li2024 10 / 10 / 11 ok;
  li2025d 7 / 7 / 9 ok; ling2024 10 / 10 / 11 ok; lischke2015 10 / 10 / 10 ok; liu2018a 10 / 9 / 9 ok; liu2019
  23 / 7 / 13 ok (note N1); liu2020a 12 / 12 / 12 ok; liu2024 7 / 5 / 10 (5 ok, 2 imprecise C1); lo2017 6 / 6 / 8 ok;
  lu2015a 7 / 7 / 7 ok; lu2025a 18 / 18 / 18 ok; luquegonzalez2019 8 / 8 / 8 ok; ma2000 4 / 4 / 4 ok; ma2015
  10 / 10 / 11 ok; mao2024 5 / 5 / 5 ok; masanovic2003 6 / 6 / 6 ok; mehta2026 5 / 5 / 5 ok; ni2025 5 / 5 / 5 ok;
  ortegamonux2013 13 / 13 / 13 (13 imprecise, F1).

## Per-paper findings

- li2022: 5 blocks; US state codes only, `country: ""` correct (D249). Block 2 prints the UC name and the campus without
  a comma; `org` University of California + `campus` Santa Barbara (D449) maps to org_ucsb. Printed form "Lopez-rios"
  kept. Order swaps vs list (#7 / #8, #11 / #12) name-matched. ok.
- li2023a: block 1 recorded as HUST with the national laboratory + school as one unit chain; the corpus carries both
  this form (lit_h16, lit_h18) and the two-org form (lit_h02, lit_h12, lit_h21, lit_h26), already open for the org
  round (D522). Markers 3 / 4 dropped as contact. ok.
- li2024: 3 blocks, markers 4 / 5 dropped as contact; truncated printed unit "School of Opto-Electronical" kept as
  printed; curly apostrophe in Xi'an as printed (lit_h33 same). ok.
- li2025d: Kowloon / HK on blocks 1 and 5 (lit precedent for the same lab); Dongguan entity with the parenthesized
  place inside `org` (D301); Shenzhen research institute as its own org (same form in other committed batches). ok.
- ling2024, liu2018a, liu2020a: revtex preprints, blocks under the author line (header). liu2018a list author 6
  (Botao Du) is not printed in this arXiv version: no row, `author_list_differs` correct. liu2020a block 2 Purdue
  OxideMEMS Lab, West Lafayette, US. ok.
- lischke2015: IHP, Frankfurt (Oder) as printed; block 2 prints the institute after the university, contiguous. ok.
- liu2019: cover page 1, header on page 2 (`p.2 header` correct). Four groups, each above its block: G1 (S. Liu,
  A. Torres, A. Gossard, J. Bowers), G2 (S. Liu, D. Jung, A. Gossard, J. Bowers), G3 (J. Norman, M. Dumont,
  A. Gossard, J. Bowers), G4 (D. Jung, Korea Institute of Science and Technology, Seoul, KR). All markers correct;
  probe J1 confirms the grouped position check binds. Explicit slots point to the first full-name occurrences
  (1, 3-8); probe S2 shows `slot` is required (S. Liu otherwise matches the abbreviated list slots 9, 10, 14, 15).
  The note is imprecise: the list has Songtao Liu twice (slots 1 and 2), so slot 2 also gets no row (N1).
- liu2024: blocks 1, 2, 4, 5, 6 correct. Block 3 (Zhejiang University with a three-part unit chain, Hangzhou, CN)
  prints a building designation with a number and a campus name between the unit chain and the university. The
  extractor parked it (authors 2 Ziliang Ruan and 7 Liu Liu `unreadable`, no rows), as lit_h22 kim2026 (G3) and the
  G6 cases. Probe Z2 (only the campus name as `skip_between`): 2 errors, unit and org not contiguous (the gap allows
  letters only). Probe Z1 (the full span including the number as `skip_between`): 0 errors, so the checker would
  accept it and the D244 scan does not flag it (gap G1 below); the extractor correctly applied the contract rule (no
  building number in any field) instead. Parking correct; rated imprecise until G6 (C1).
- lo2017: COBRA Research Institute as unit of TU/e; SMART Photonics; street and postal text not recorded. ok.
- lu2015a, lu2025a: single blocks (UBC Vancouver CA; TSMC Hsinchu TW). ok.
- luquegonzalez2019: Wiley first-page footnote, two groups (G1 Malaga 6 authors, G2 NRC Canada 2 authors), group
  forms with titles stripped, `p.1 footnote` correct. ok.
- ma2000: "The authors are with" statement (all 4); the Technological Institute between department and Northwestern
  University is the building name, `skip_between` (D380) correct; Evanston, US; `p.1 footnote` correct. ok.
- ma2015: 3 blocks, Coriant Advanced Technology Group New York US, asterisk equal contribution. ok.
- mao2024: three Huawei blocks, provinces not recorded. ok.
- masanovic2003: "The authors are with" statement (all 6); UC + campus Santa Barbara, unit "Electrical and Computer
  Engineering and Materials Departments"; Jonathon S. Barton -> list Jon S. Barton, explicit slot 3 (D287 alternate
  name, initials agree; probe M1: without `slot` 0 slots match). ok.
- mehta2026: per_author blocks (D368); block 3 prints only a state code and the country, block 5 only a prefecture and
  the country: `locality: ""` correct (D288). ok.
- ni2025: 2 blocks, markers 3 / 4 dropped as contact. ok.
- ortegamonux2013: fields, markers and slots correct. Pavel Cheben is printed with marker 1 (Malaga) in both layers
  (probe O1: marker 2 fails, 2 errors); recorded as printed (his NRC block in luquegonzalez2019 is in the same batch).
  The two blocks are printed at the foot of page 1, below the body text (render checked; both text layers place them
  after the Introduction paragraphs), but carry the default `p.1 header` locator (F1).

## Findings and proposed fixes (not applied)

| # | paper, slots | rating | evidence | proposed fix (exact YAML edit) |
|---|---|---|---|---|
| F1 | ortegamonux2013 #1-#13 | imprecise, fixable now (locator only; fields correct) | p.1: both blocks are a first-page footnote (Laser Photonics Rev. letter layout; same as luquegonzalez2019 in this batch and h27 F1 / D522). Probe L1: 0 errors, rows unchanged | block 1: after `country: "ES"` add `, locator: "p.1 footnote"`; block 2: after `country: "CA"` add `, locator: "p.1 footnote"`. Result lines: `{marker: "1", basis: printed, org: "Universidad de Málaga", unit: "Dpto. de Ingeniería de Comunicaciones, ETSI Telecomunicación", locality: "Málaga", country: "ES", locator: "p.1 footnote"}` and `{marker: "2", basis: printed, org: "National Research Council Canada", locality: "Ottawa", country: "CA", locator: "p.1 footnote"}`; optionally append to the note "; blocks printed as a first-page footnote" |
| N1 | liu2019 (note only) | imprecise note | author list slots 1 and 2 are both Songtao Liu; slots 9-23 repeat the four groups. The note says the list repeats the 7 authors "23 times" and names only slots 9-23 as without row | note: replace "the author list repeats the 7 header authors 23 times (list artefact for the D412 correction file): explicit slots to the first occurrence, list slots 9-23 get no row" with "the author list has 23 entries for the 7 header authors (Songtao Liu twice in slots 1 and 2, the four groups again in slots 9-23; list artefact for the D412 correction file): explicit slots to the first occurrence, list slots 2 and 9-23 get no row" |
| C1 | liu2024 #2 (Ziliang Ruan), #7 (Liu Liu) | imprecise, not fixable now (parked block, no rows; nothing wrong recorded) | p.1 header block 3: a building designation with a number sits between the unit chain and Zhejiang University; D244 forbids storing it, and the unit-org gap admits letters only (Z2). Same class as D426 G6 | after a verified, never-stored building placeholder exists (as D410 `<postal box>`): insert before block 4 `{marker: "3", basis: printed, org: "Zhejiang University", unit: "State Key Laboratory of Extreme Photonics and Instrumentation, College of Optical Science and Engineering, International Research Center for Advanced Photonics", skip_between: "<placeholder>", locality: "Hangzhou", country: "CN"}` (unit chain as lit_h21 yi2024a); authors 2 and 7 `markers: ["3"]` without `unreadable`; `status: ok`; drop the gap sentence from the note. Rows 205 -> 207 |

Any change to the YAML changes its hash: re-run `check lit_h31 --corpus lit` afterwards to refresh the stamp.

## Points checked and correct

- liu2018a #6 Botao Du: in the author list, not printed in the cached arXiv version: correctly no row; not a D412
  case (no evidence of a list defect; the list may follow another version).
- liu2019 list: 23 entries for 7 people, a list artefact (slot 2 and 9-23): D412 correction file.
- masanovic2003 #3 Jon / Jonathon: alternate name form, initials J. S. agree, same group and co-authors; accepted.
- ortegamonux2013 Pavel Cheben marker 1: printed in both layers; kept (never invent).
- No present address, no prose clause, no `continued`, no `more_orgs` in the batch; one `skip_between` (ma2000,
  building name, no number).
- Country: li2022 (5 blocks) no country printed, `""` correct; HK for Kowloon blocks; KR from the printed South Korea.

## Privacy and as-printed scan

- Digit runs of 3 or more in `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`: paper-id years
  and decision numbers only. No contact, URL, street, building or postal string in any batch file (pattern scan plus
  the street, building and postal strings of the header pages of all 21 papers). Notes say what was not recorded
  without copying it; the liu2024 note names the parked block's fields only (no building or campus text).
- As printed (kept, correct): li2022 Lopez-rios; li2024 truncated unit and curly apostrophe; lischke2015 IHP and
  Frankfurt (Oder); luquegonzalez2019 / ortegamonux2013 two printed spellings of the Malaga department (both unmapped,
  org round).

## Commands (2026-11-08, log times)

| Command | Result |
|---|---|
| `show lit_h31 --corpus lit --codes <id> --pdf`, all 21 papers (liu2019 also `--pages 2 2`), 12:07-12:10 | headers and author lists read (scratchpad only) |
| `check lit_h31 --corpus lit --dry-run` 12:07:39 (pid 16406) | 0 errors, 4 warnings (3 order_differs, masanovic2003 explicit slot); slots 199, recorded 180, no_header 19; rows 205 (grade A 205; printed 144, single 25, grouped 21, prose 10, per_author 5); papers ok 20, partial 1; 13 unmapped org strings |
| `probe.py` on a scratch copy, dry-run, 12:13:01-12:13:40 (pid 23930) and 12:14:46-12:14:53 (pid 25535); a first attempt failed at import (module not registered), nothing run | results below; repo batch md5 unchanged after each run |

Dry-run and probe runs wrote their usual log files under `logs/` (`lit_headers_check_lit_h31_*`); nothing else.

| probe | change | result | reading |
|---|---|---|---|
| B0 | none | 0 errors | baseline |
| Z1 | liu2024 block 3 with the full building + campus span as `skip_between` | 0 errors | checker would accept; D244 scan misses the span (G1); withheld by contract |
| Z2 | liu2024 block 3 with only the campus name as `skip_between` | 2 errors, unit and org not contiguous | C1 waits on G6 |
| O1 | ortegamonux2013 Pavel Cheben marker 2 | 2 errors, printed markers differ | marker 1 is printed |
| J1 | liu2019 D. Jung without G2 | 2 errors, author printed between group and block | grouped check binds |
| M1 | masanovic2003 no explicit slot for Jonathon S. Barton | 2 errors, 0 slots match | slot 3 required |
| S2 | liu2019 no explicit slot for S. Liu | 1 error, 4 abbreviated slots match | slot 1 required |
| L1 | ortegamonux2013 blocks `p.1 footnote` | 0 errors | F1 |

## Checker gaps observed (scripts not edited)

- G1 D244 address scan: the room / building pattern requires the number right after the keyword, so a building
  designation with "No." before the number passes the YAML scan (probe Z1). Proposed: allow an optional `No.` between
  keyword and number, with a test; then a building span can never reach a committed file by accident.
- G2 (D426 G6, open) No verified, never-stored placeholder for a building / site span with a number between unit and
  org (D410 has one for postal boxes only). Blocks liu2024 block 3 (C1).
- G3 (as h27 G3) Locator vs layout: a first-page footnote block passes with the default `p.1 header` (F1).

## Coordinator questions

1. Apply F1 (ortegamonux2013 locators) and N1 (liu2019 note) now, then re-run `check lit_h31 --corpus lit`?
   Recommended: yes, before `aggregate`; rows unchanged (205).
2. C1: implement a building placeholder for `skip_between` (G2, D410 pattern) together with the G1 scan fix, then
   re-record liu2024 block 3? Recommended: yes, in the next checker pass; keep liu2024 `partial` until then.
3. Lists: liu2019 (slots 2, 9-23) to the D412 correction file; masanovic2003 #3 (Jon / Jonathon) and ortegamonux2013
   Pavel Cheben (printed under the Malaga block) to the D426 review list; liu2024 #2 #7 to the re-record list.

## Verdict

GO. No slot carries a wrong person, org, city, country or marker, nothing is invented, no block is missed, and no
address or contact text is recorded. 13 slots should take the footnote locator (F1, field additions only), one note
undercounts the rowless list duplicates (N1), and 2 slots wait on the known building-span checker gap (C1).
