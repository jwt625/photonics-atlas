---
title: Fresh-context audit of the lit author-affiliation batch lit_h36 (15 papers)
date: 2026-11-09
auditor: Claude (fresh context; wrote only this record; headers.yaml, derived files, scripts, tests, people and registry data not edited; check run only with --dry-run, probes on a scratch copy; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h36/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D400-D546); format from the 2026-11-08 h34 audit
verdict: GO for the people rebuild (no slot wrong); 109 slots audited, 98 ok, 11 imprecise, 0 wrong; both unreadable calls confirmed (lukin2019 checker gap, 11 slots imprecise, re-record list; zhao2016 font-encoded, unreadable by design); F1 (2 redundant explicit slots) and N1 (zhao2016 note) optional, no row change; nothing applied
---

# Lit header batch audit: lit_h36 (2026-11-09)

## Scope

Batch lit_h36 (15 papers: 13 Optica-publishing journal papers (Optics Express 12, Optics Letters 1), 1 Nature
Photonics article, 1 conference paper with a font-encoded text layer; 109 author-list slots, no header-only author; 102
rows). Restricted corpus: this record names only authors, orgs, units, cities and countries; no paper text is quoted
and no contact, street, building, postal-box or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h36 --corpus lit --codes <id> --pdf`
  (all 15; output kept in the session scratchpad only). Every header and block is on page 1; no `--pages` needed (no
  cover page, no later-page affiliation list). Markers legible in both layers in the 13 recorded papers.
- Per slot: printed name vs `compare.csv` slot and the author list printed by `show`; printed marker run vs `markers` +
  `dropped_markers`; block fields vs the print (org, unit chain, campus, city, country); locator; parents; present
  addresses. All 31 distinct (paper, org, unit, place, org id) tuples of `header_rows.csv` read; no wrong mapping.
- Contact markers: tao2025 markers 4 and 5 checked by the leading character of the two masked contact lines in
  `text.md` and in the PDF spans (contents not printed): lines start with 4 and 5, so `dropped_markers` with reason
  contact footnote is right. Every other paper marks its contact line with an asterisk only.
- Missed blocks: cue scan of the whole `text.md` of all 15 (now with / at, present / current address, present / current
  affiliation, currently, presently, is / are / was / were (also / now) with, also with, on leave, visiting, formerly,
  deceased, permanent address, affiliation). 4 hits, all body text (osorniomartinez2025 p.9, parra2020 p.8, piyush2026
  p.8, vocht2024 p.4). No present address, prose statement or later-page affiliation list. No missed block.
- Unreadable papers: lukin2019 tested by recording its blocks on a scratch copy (probes L1, L2); zhao2016 by reading the
  code points of its superscript spans (pymupdf rawdict, read-only).
- Claims and contract calls tested with dry-run probes on scratch copies of the batch (`probes/probe.py` in the session
  scratchpad, via the module's `LIT_BASE`); md5 of every repo batch file identical before and after the audit.
- Stamp: `check_stamp.txt` matches `headers.yaml` (sha256 6240c11f...). Repo batch files untouched by this audit.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h36 | 15 / 15 | 109 | 98 | 11 | 0 |

- Rows 102 (all grade A: printed 80, single 22; primary 87, additional 15; all locators p.1 header); recorded 87,
  no_header 22 (lukin2019 11, zhao2016 11); papers ok 13, partial 0, unreadable 2; `author_list_differs` 0; explicit
  slots 3 (nie2019 #2 needed; song2024 #6 and tao2025 #7 redundant, F1); present addresses 0; prose blocks 0;
  `order_differs` true only on nie2019 (5 slots, warning); 10 unmapped org strings; multi-affiliation slots 15.
- Imprecise by cause: checker gap 11 (lukin2019 #1-#11, blocks and the equal-contribution line printed before the
  author line; as hu2022 B5 in the h30 audit). Fixable now: 0.
- ok includes zhao2016 #1-#11 (font-encoded layers; unreadable is the contract outcome, barwicz2017 precedent, batches-3
  audit G6).
- Per paper (slots / rows / rating): lukin2019 11 / 0 imprecise (checker gap); melus2025 3 / 4 ok; morishima2021 6 / 6
  ok; nie2019 5 / 10 ok; osorniomartinez2025 5 / 8 ok; parra2020 4 / 4 ok; piyush2026 6 / 6 ok; song2024 10 / 12 ok;
  tabatabaei2026 11 / 11 ok; tao2025 9 / 13 ok; vocht2024 5 / 5 ok; xu2023b 9 / 9 ok; zhang2023b 6 / 6 ok; zhao2016
  11 / 0 ok (unreadable by design); zhu2025 8 / 8 ok.

### Per-slot field counts (109 slots)

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (87 recorded) | 87 | 0 | 0 |
| markers + dropped_markers (87 recorded) | 87 | 0 | 0 |
| blocks (org / unit / campus / locality / country) (87 recorded) | 87 | 0 | 0 |
| prose blocks | n/a (none printed) | | |
| present addresses | n/a (none printed) | | |
| locators (87 recorded) | 87 | 0 | 0 |
| unreadable papers (22 slots) | 11 (zhao2016) | 11 (lukin2019) | 0 |

## Per-paper findings

- lukin2019 (11): Nature Photonics. p.1 footnote prints the two marked blocks (1 E. L. Ginzton Laboratory, Stanford
  University, Stanford, US; 2 Department of Electrical and Computer Engineering, University of California, Davis, US)
  and the equal-contribution line (marker 3, naming authors 1-3) before the title and the author line in both the text
  and the PDF layer. Author markers legible: 1,3 / 1,3 / 1,3 / 1 / 1 / 1 / 1,2 (Marina Radulaski) / 1 / 1 / 1 / 1
  (asterisk on Jelena Vučković = corresponding author). Unreadable confirmed: probes L1 / L2 (both blocks recorded,
  `p.1 footnote` or `p.1 header`) give 10 errors each: both blocks fail the D246 position check, and the names of
  authors 1-3 are first found in the equal-contribution line, so their marker runs fail too. The legible header is
  lost only to the checker order rule: imprecise, re-record list (question 1). List #11 is "Jelena Vuckovic A" (D412
  artefact). Note accurate (it lists the blocks with org first; printed order is unit first).
- melus2025 (3): capitals; Melus 1,2 / Suelzer 1 / Reano 2 (probe M1, Melus without 2: 2 errors). Block 1 Air Force
  Research Laboratory, place printed as Wright-Patterson AFB (kept as printed; the only place printed), US; block 2 The
  Ohio State University + ElectroScience Laboratory, Columbus, US. State names and street text not recorded. ok.
- morishima2021 (6): single unmarked block Sumitomo Electric Industries, Ltd., Yokohama, JP (`org_sumitomo_electric_industries`);
  ward printed before the city in the note (D366), prefecture not recorded. ok.
- nie2019 (5): Optics Letters; every author 1,2. Block 1 Photonics Research Group, INTEC + Ghent University-IMEC (dash
  form kept as printed, D416 (5) / D426; maps by alias to Ghent University + imec); block 2 Center for Nano- and
  Biophotonics + Ghent University. Printed NINA TRUK vs list Nina Turk: letter transposition, `slot: 2` required (probe
  N1, slot removed: 0 candidates) and allowed (D287 plain misspelling); printed order differs from the list (warning,
  D363). ok.
- osorniomartinez2025 (5): blocks 1 University of Twente (unit chain Integrated Optical Systems, MESA+ Institute for
  Nanotechnology), 2 ALUVIA Photonics (`org_aluvia_photonics`), 3 PHIX B.V., all Enschede, NL; dagger = equal
  contribution (authors 1, 2). A. R. DO NASCIMENTO JR. keeps the suffix in the name (probe O1, suffix removed: the
  marker run fails); list form A. R. do Nascimento matches. S. M. GARCÍA-BLANCO vs list with a non-ASCII hyphen:
  automatic. ok.
- parra2020 (4): single block, Universitat Politècnica de València + Nanophotonics Technology Center, Valencia, ES
  (`org_upv`). ok.
- piyush2026 (6): single block; unit printed as centre + department without separator, one contiguous segment; org
  printed as IIT Madras (probe P1, org Indian Institute of Technology Madras: 4 errors, so as printed is required);
  Chennai, IN; unmapped until an alias exists (org round). List #1 is in capitals (KUMAR PIYUSH; question 3). ok.
- song2024 (10): five blocks; marker runs 1 / 2 / 3 / 1 / 1 / 4 / 1,5 / 3 / 1,3 / 1,3, dagger = equal contribution.
  Block 3 org printed Southeast Univcersity in both layers (probe S1, corrected spelling: 4 errors); kept as printed,
  as giewont2019 and krumrein2026 typos; unmapped, alias in the org round. LIU LI vs list Li Liu: name-order swap;
  matched by name also without the explicit slot (probe S2: 0 errors; F1). JUNPENG LU vs list Junpeng Lü: automatic.
  ok.
- tabatabaei2026 (11): blocks University of Virginia (Charlottesville), University of California + campus Santa
  Barbara (D301; place printed twice, locality Santa Barbara; `org_ucsb`), Honeywell Aerospace Technologies (Plymouth),
  all US. Marker runs match (dagger = equal contribution, authors 1, 2). List forms without middle initials
  (Vithoulkas, Keyes, Nelson) automatic; list #11 carries an accent the print does not (Andréas; question 3). ok.
- tao2025 (9): blocks Nankai University + MOE key laboratory / school / TEDA institute chain, Tianjin; Shanghai
  Institute of Microsystem and Information Technology, Chinese Academy of Sciences + national key laboratory unit,
  Shanghai (same org form as the 9 committed SIMIT blocks); University of Chinese Academy of Sciences + centre unit,
  Beijing; all CN. Xin Ou 2,3,4 and Guoquan Zhang 1,5 with 4 and 5 = contact lines (verified). FANG BO vs list Bo
  Fang: swap, matched by name without the explicit slot (probe T1: 0 errors; F1). YUCHEN ZHANG vs Yu-Chen Zhang:
  automatic. ok.
- vocht2024 (5): blocks Eindhoven University of Technology + Eindhoven Hendrik Casimir Institute, SMART Photonics BV
  (`org_smart_photonics`), Eindhoven, NL. ERWIN BENTE vs list Erwin A. J. M. Bente, ALONSO MILLAN-MEJIA vs Alonso
  Millan Mejia: automatic. ok.
- xu2023b (9): four blocks (Jilin University, Changchun; Westlake University, Hangzhou; Zhejiang University with the
  two-laboratory + college chain, Hangzhou; Institute of Microelectronics of the Chinese Academy of Sciences, Beijing;
  all CN). Unit chains contiguous as printed. ok.
- zhang2023b (6): single block, University of California + campus Davis, locality Davis (place printed once; same
  form as the 5 committed UC Davis blocks; probe Z1 shows the campus-less form also passes, so the campus is the D301
  call), US; maps to `org_university_of_california_davis`. ok.
- zhao2016 (11): text and PDF layer of page 1 use one constant code-point shift for every glyph (letters and digits);
  the superscript spans after the names carry shifted control codes (the PDF view prints them as `^{}`), and the 4
  blocks (decoded org names: Huawei Technologies, LioniX BV, XiO Photonics BV, University of Twente) print postal-box
  codes. `source.json` flags the garbled layer. The checker cannot verify any field: unreadable correct (barwicz2017,
  iadanza2024 first copy). Note slightly imprecise on the markers (N1). ok.
- zhu2025 (8): blocks Hebei University (centre / provincial centre / college chain, Baoding), Fuzhou University
  (institute + school, Fuzhou), Southeast University (national research center + school, Nanjing), all CN; dagger =
  equal contribution. ok.

## Fixes (exact YAML edits; optional, none needed for the rebuild)

| # | paper, slots | rating | evidence | edit |
|---|---|---|---|---|
| F1 | song2024 #6 (LIU LI), tao2025 #7 (FANG BO) | ok (slot right), contract wording: `slot:` only when the script cannot match | probes S2 / T1: both match by name without the explicit slot (0 errors, no warning); rows unchanged | song2024: `{name: "LIU LI", markers: ["4"], slot: 6}` -> `{name: "LIU LI", markers: ["4"]}`, note `(same name parts in swapped order, slot set)` -> `(same name parts in swapped order, matched by name)`; tao2025: `{name: "FANG BO", markers: ["1"], slot: 7}` -> `{name: "FANG BO", markers: ["1"]}`, same note change. Recommended: keep as is (question 2) |
| N1 | zhao2016 (note only) | note imprecise | rawdict: superscript spans carry shifted control codes, not lost glyphs | note -> `"text and PDF layer of page 1 are font-encoded (one constant code-point shift on every glyph, digits included; the superscript markers are shifted control codes that the PDF view prints empty), so the author line and the blocks cannot be verified; no rows (barwicz2017 precedent)"` |

Any change to the YAML changes its hash: re-run `check lit_h36 --corpus lit` afterwards to refresh the stamp.

## Open questions (with recommendation)

1. lukin2019: add to the D546 re-record list "blocks before the author line" (hu2022, lischke2021a). Values for the
   re-record (all `locator: "p.1 footnote"`): block 1 `{marker: "1", basis: printed, org: "Stanford University", unit:
   "E. L. Ginzton Laboratory", locality: "Stanford", country: "US"}`; block 2 `{marker: "2", basis: printed, org:
   "University of California", campus: "Davis", unit: "Department of Electrical and Computer Engineering", locality:
   "Davis", country: "US"}`; authors 1-3 `markers: ["1"]` + `dropped_markers: [{marker: "3", reason: "equal
   contribution"}]`, Marina Radulaski `["1", "2"]`, the other 7 `["1"]`. The checker change must also skip author
   names printed in a footnote before the author line (probe L1). Recommended: yes; keep `unreadable` until then.
2. F1: keep the two redundant explicit slots (they document the swap and survive a stricter D382 matcher) and add
   song2024 #6 and tao2025 #7 to the D426 review list as name-order swaps (zhang2022b precedent, D522); nie2019 #2
   (Truk / Turk) is a plain misspelling, no review needed. Recommended: yes.
3. D412 correction-file candidates: lukin2019 #11 "Jelena Vuckovic A" (same artefact as white2022 / white2024);
   piyush2026 #1 list form in capitals (KUMAR PIYUSH would become the slot name); tabatabaei2026 #11 list accent
   (Andréas; printed ANDREAS). Recommended: add #11 lukin2019 now; the other two as low-priority display fixes.
4. zhao2016: keep `unreadable`. A decode route for constant-shift layers would make it checkable (third such paper
   after barwicz2017 and iadanza2024), but the checker verifies printed text only. Recommended: no checker work now;
   list the three papers if a decode feature is ever scoped.

## Unmapped org names (org round, no YAML change)

| printed org (unit) | place | proposal |
|---|---|---|
| Air Force Research Laboratory | Wright-Patterson AFB, US | new org (already requested from rizzo2023 / sundaram2024 / sundaram2025) |
| The Ohio State University (ElectroScience Laboratory) | Columbus, US | new org (requested from sun2011) |
| PHIX B.V. | Enschede, NL | alias to `org_phix_photonics_assembly` (requested from winkler2024) |
| IIT Madras (centre + department) | Chennai, IN | alias to `org_indian_institute_of_technology_madras` |
| Southeast Univcersity (School of Physics) | Nanjing, CN | lit-scoped printed-variant alias to `org_southeast_university` (printed typo) |
| Honeywell Aerospace Technologies | Plymouth, US | alias or child of `org_honeywell` (same string requested from sun2024; Honeywell Aerospace from heim2026) |
| Shanghai Institute of Microsystem and Information Technology, Chinese Academy of Sciences (national key laboratory) | Shanghai, CN | alias to `org_shanghai_institute_of_microsystem_and_information_technology` |
| Institute of Microelectronics of the Chinese Academy of Sciences | Beijing, CN | alias to `org_institute_of_microelectronics_chinese_academy_of_sciences` (requested from han2024) |
| Hebei University (centre / college chain) | Baoding, CN | new org (requested from earlier batches) |
| Fuzhou University (institute + school) | Fuzhou, CN | new org (requested from yu2025) |

## Privacy and as-printed scan

- Grep over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`, `papers.csv`, `check_stamp.txt` and
  this record for contact / URL patterns, street and building words, postal-box codes and digit runs of 4 or more: 0
  contact or URL hits; the word street only in notes that say such text was not recorded; digit runs only paper-id
  years, the stamp hash and log times. No postal code, street or building text in any field.
- As printed (kept, correct): song2024 Southeast Univcersity (typo in the source); nie2019 Ghent University-IMEC
  (dash form); piyush2026 IIT Madras and the separator-less unit; parra2020 Universitat Politècnica de València with
  accents; melus2025 Wright-Patterson AFB; osorniomartinez2025 name suffix JR. No `skip_prefix` or `skip_between` in
  this batch.

## Commands (2026-11-09, log times)

| Command | Result |
|---|---|
| `check lit_h36 --corpus lit --dry-run` 19:16:40 (pid 83635) | 0 errors, 2 warnings (nie2019 explicit slot, nie2019 order); slots 109, recorded 87, no_header 22; rows 102 (grade A 102; primary 87, additional 15; printed 80, single 22); papers ok 13, unreadable 2; multi-affiliation slots 15; present addresses 0; 10 unmapped org strings |
| `show lit_h36 --corpus lit --codes <id> --pdf`, all 15 | headers and author lists read (scratchpad only) |
| `probes/probe.py` on scratch copies, dry-run, 19:18:39-19:19:45 (pid 88746) | below; repo batch files md5 unchanged; the dry-run check writes its usual log files under `logs/` |

| probe | change | result | reading |
|---|---|---|---|
| L1 | lukin2019 both blocks + markers recorded, `p.1 footnote` | 10 errors (block position x4, marker runs of authors 1-3 x6) | unreadable required now |
| L2 | same, `p.1 header` | 10 errors | same |
| S1 | song2024 block 3 org spelled Southeast University | 4 errors | typo as printed required |
| S2 | song2024 LIU LI without `slot: 6` | 0 errors | explicit slot redundant (F1) |
| T1 | tao2025 FANG BO without `slot: 7` | 0 errors | explicit slot redundant (F1) |
| N1 | nie2019 NINA TRUK without `slot: 2` | 2 errors (0 candidates) | explicit slot required |
| P1 | piyush2026 org Indian Institute of Technology Madras | 4 errors | IIT Madras as printed required |
| M1 | melus2025 Melus without marker 2 | 2 errors | markers bound |
| Z1 | zhang2023b org University of California, Davis without campus | 0 errors | campus is the D301 call |
| O1 | osorniomartinez2025 name without JR. | 2 errors | suffix part of the printed name run |

## Checker gaps observed (scripts not edited)

- G1 Blocks and an equal-contribution line printed before the author line (lukin2019; hu2022, lischke2021a): the block
  position check (D246) and the first-occurrence name search both fail. Already on the D546 re-record list.
- G2 Constant-shift font encoding (zhao2016; barwicz2017, iadanza2024): unreadable by design (batches-3 audit G6).

## Verdict

GO. No slot carries a wrong person, org, city, country or marker, nothing is invented, no block is missed, and no
address or contact text is recorded. lukin2019 (11 slots) is legible but blocked by the checker order rule and waits on
the re-record list; zhao2016 stays unreadable by design. F1 and N1 are optional and change no row.
