---
title: Fresh-context audit of the lit author-affiliation batch lit_h21 (25 papers)
date: 2026-11-02
auditor: Claude (fresh context; wrote only lit_h21/headers.yaml, the derived files the checker writes, and this record; aggregate not run)
scope: data/_staging/people/lit_headers/lit_h21/headers.yaml; both header contracts; DevLog-011 D350-D369, D380, D400-D426; previous audits 2026-10-30-lit-header-batch-h17-audit.md, 2026-10-29-lit-header-batches-3-audit.md (Wuhan National Laboratory forms)
verdict: GO for the people rebuild after the fixes below (applied; check 0 errors, 5 warnings); 0 wrong and 4 imprecise slots in 279 audited (2 fixed, 1 held without a row pending a one-line checker change, 1 checker gap); altered skip_between removed; 6 notes made by-type
---

# Lit header batch audit: lit_h21 (2026-11-02)

## Scope

Batch lit_h21 (25 papers, 279 author-list slots), extracted 2026-11-02 (extractor check: 0 errors, 5 warnings; 25 ok;
274 / 279 slots recorded; 366 rows). Restricted corpus: this record names only authors, orgs, units, cities and
countries; no paper text is quoted and no contact, street, building or postal text is copied. The one printed name
that looks like a postal pattern, the Huawei lab name "2012 Labs", is a unit name, not an address.

## Method

- Every paper read with `env -u VIRTUAL_ENV uv run python scripts/ofc_headers.py show lit_h21 --corpus lit --codes
  <id> --pdf` (all 25); `--pages 10` added for the three end-of-paper lists (wang2026f, yi2024a, zhang2024b). Each field
  compared with the page; the extractor's notes treated as claims to test.
- Per slot: slot-to-name assignment (D359, D369, D287, D302), printed marker run vs `markers` + `dropped_markers`
  (text and PDF view), block mapping, org / unit / more_orgs split, parent rule, campus (D301), locality, country,
  role, basis, locator. Every note claim checked against the page (contact lines are masked in `show`, so "contact
  footnote" claims were checked by the masked line's marker and position).
- Missed blocks and present addresses: cue scan over the pages shown (page 1, and page 10 for the three papers above; present address, current address,
  present affiliation, now with / at, is / are now, currently, permanent, on leave, visiting, deceased, retired, also
  with, formerly): one hit, zhang2025c block 2.
- Name scan: all 279 `compare.csv` rows, list name vs printed name (folded); 50 rows differ, every one inspected.
- Org mapping: every mapped (org, id, match basis) triple in `header_rows.csv` read; none wrong.
- Claims tested with dry-run probes (`check --dry-run` on a temporarily edited `headers.yaml`, file restored
  byte-identical, md5 asserted after each probe; helper `probe.py` in the session scratchpad `lit_h21_audit/`).
- Backup before any edit: `backup_lit_h21_*.zip` (lit_h21 directory) in the same scratchpad folder.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h21 | 25 / 25 | 279 | 275 | 4 | 0 |

- Fixed: 2 imprecise (sun2025 #2 #14, F1). Held without a row pending coordinator question 1: 1 (wang2025 #4, F2). Not
  fixable within the contract / checker: 1 (zhang2025c #2, C1).
- Before -> after: rows 366 -> 363; recorded 274 -> 273; no_header 5 -> 6; ok 25 -> 24, partial 0 -> 1; unmapped org
  strings 27 -> 27.
- The 6 `no_header` slots: wang2025 #4 (F2, restorable); wang2025 #5, wang2025b #2 #12, xue2026 #4, yoo2022 #9
  (`slot: 0` rulings below, correct under the never-guess rules).

## Ruling on the altered `skip_between` (wang2025 block 4)

Printed block: Central Research Institute Planning, then the lab name 2012 Labs, then Huawei Technologies Company Ltd.,
Shenzhen, China. The extractor stored `skip_between: "2012Labs"` with the space removed. It passed only because the
D244 scan pattern (four digits, whitespace, capitalized word) needs the whitespace, while the verification compares
letters and digits only, so the altered string still verifies.

Not acceptable under the contract, for three reasons:

1. As printed: fields are copied as printed, verified spans are recorded "as printed" (D366 `skip_prefix`; D380 same
   mechanism). The value is not what is printed; it was changed so that a guard would not fire.
2. The D244 scan is a rights control. There is no privacy harm in this instance (a lab name, a false positive), but the
   same edit would let any real postal code + city string through by deleting its space, so a false positive is a
   checker question, not something a batch resolves by editing the string. The D410 postal-box case set the precedent:
   the checker was changed (pattern-verified placeholder), the value was not reformatted.
3. Wrong field: D380 / D410 cover building, site and postal-box spans that must not be recorded. 2012 Labs is a named
   Huawei lab, the most specific part of the unit chain; the contract says to copy the whole sub-unit chain. Skipping
   it dropped it from the row without a trace. The note's "not stored" was also inaccurate: the span sits in the YAML.

Right handling: `unit: "Central Research Institute Planning, 2012 Labs"` with no skip span, after a narrow exemption in
the scan (question 1). Probe W2 shows that form fails only on the 3 D244 hits, with no D246 error, so the exemption is
all it needs.

Interim handling applied (no checker change allowed here): block 4 not recorded, Xia Liu `unreadable: true` with the
reason in the note, paper `partial`, as other blocks that cannot be recorded (keyvaninia2012 G5, foster2006 G3). This
loses one correct row until question 1 is answered.

Alternatives probed and rejected:

| probe | form | result | ruling |
|---|---|---|---|
| W1 | `skip_between: "2012 Labs"` as printed | 1 error, D244 scan | correct text, blocked by the scan |
| W2 | unit chain as printed | 3 errors, all D244 scan (YAML, unit field, derived row) | target form, needs question 1 |
| W3 | no span | 2 errors, unit and org not contiguous (md, pdf) | not recordable |
| W4 | `skip_between: "2012"` | 0 errors, because the checker's gap slack of up to 10 letters absorbs "Labs" | rejected: truncated span, same workaround in another form, lab name still lost |
| W5 | org only, no unit | 2 errors, marker + first field not printed | not recordable |
| W6 | block omitted, author unreadable, paper partial | 0 errors, rows 365, no_header 6 | applied |

Org + `more_orgs` (cabezon2012 precedent, D426) was also considered and not used: it would publish Central Research
Institute Planning as an organization, and the D426 precedent covers a street span that can never be recorded, whereas
here the printed text is recordable once the scan is exempted.

`skip_between` / `skip_prefix` in this batch: this was the only span (0 `skip_prefix`). Across all lit and OFC batches,
the 6 remaining `skip_between` values show no digits glued to letters (grep only; other batches were not re-read against
their pages, so other forms of alteration are not ruled out).

## Rulings on `author_list_differs`, `slot: 0` and slot overrides

| paper, slot | printed vs list | ruling |
|---|---|---|
| wang2025 #5 | Huanyu Lu vs Hui Lu | `slot: 0` correct (different given name, common family name, D287). Printed at the same position (question 3) |
| wang2025b #2 | Xiao Hu vs Xiaohua Hu | `slot: 0` correct (D247 different full given names; D302 passes, so not compatible). Same position (question 3) |
| wang2025b #12 | Haibin Zhao vs Hai Sheng Zhao | `slot: 0` correct (second syllable differs). Same position (question 3) |
| xue2026 #4 | Qian Liu vs Q. B. Liu | `slot: 0` correct (D369, initial B unexplained). Same position (question 3) |
| yoo2022 #9 | Jong Jin Lee vs Joongku Lee | `slot: 0` correct (different given name). Same position (question 3); Joon Ki Lee correctly takes #10 |
| sundaram2025 #8 | Phil Battle vs Philip R. Battle | keep `slot: 8` (D287 nickname, initials agree, distinctive family name) |
| sundaram2025 #12 | Nick Vamivakas vs A. Nick Vamivakas | keep `slot: 12` (D287 name part, distinctive family name) |
| szelag2017 #5 | Ph. Rodriguez vs Philippe Rodriguez | keep `slot: 5` (abbreviated given name, initial agrees) |
| theurer2019 #13 | R. G. Heideman vs René Heideman | keep `slot: 13` (D369 distinctive family name, missing middle initial only) |
| sutherland2019 | A. F. Evans printed last, list #2 | warning correct (D363); slot by name |
| wang2025b #5, wang2026f #2, xue2026 #2 | Li Xu vs Li Qiang Xu; Hui Jia vs Hui Min Jia; Chao Cheng vs Chao Zeng Cheng | auto-matches with a dropped syllable, common family names, same position: accepted per D426, listed for review (question 4) |
| yi2024a #11 | Daoxin Dai vs list artefact "Daoxin Dai A" | correct person; new D412 case (question 5) |
| other list-side differences | initials, middle names, hyphenation (e.g. Vijay S. S. Sundaram, Erwine Pargon / E. Pargon, Jin-Yu Liu / Jinyu Liu, Sanghwa Yoo / Sang-Hwa Yoo) | all initials agree, same positions: correct |

## Findings and fixes

| # | paper, slots | rating | evidence (locator) | fix (field: before -> after) |
|---|---|---|---|---|
| F1 | sun2025 #2 #14 (Qiyuan Li, Li Shen), block 2 | imprecise | p.1 header: Wuhan National Laboratory for Optoelectronics and a school, then Huazhong University of Science and Technology. This "lab and school, university" form is a HUST unit chain in the precedents (round 3 li2026b and most; lit_h13, lit_h17 exact form; lit_h18 liu2011), while the two-org form belongs to the "lab, university" print (ding2019, yan2017 below). The extraction dropped the school from the row. Probe S1: 0 errors | org WNLO + `more_orgs` HUST -> org `Huazhong University of Science and Technology`, unit `Wuhan National Laboratory for Optoelectronics and School of Optical and Electronic Information`; note rewritten. -2 rows; org id unchanged (`org_huazhong_university_of_science_and_technology`) |
| F2 | wang2025 #4 (Xia Liu), block 4 | imprecise (unit truncated, verification span altered) | p.1 header; ruling above | block removed, `unreadable: true`, `status: partial`, note rewritten. -1 row, restorable by question 1 |
| C1 | zhang2025c #2 (Rastko Pajković), present address | imprecise, not fixable | p.1 header: block 2 printed with the cue Present affiliation (ASML, Veldhoven, NL). Probes Z1 (`present_address`), Z2 (`affiliation`): "marker + first field not printed" (md, pdf) and a D361 coverage error | none (gap G1, family of "Current address:", kuyken2011); marker kept in `dropped_markers`, extractor's claim confirmed |
| N1 | szelag2017, thiessen2020, xue2022, yi2024a, xue2026, sundaram2025 (notes) | privacy rule | notes named a postal designation (2), districts (2), a province and a state rather than the type (h17 N1, h19) | named parts -> by type; no field changed |

Checked and correct (highlights):
- Prose: sutherland2019 P1 (9 authors) / P2 (De Jong); theurer2019 P1 / P2 (Heideman printed inside the LioniX
  statement); veiga2026 P1 / P2; wang2023e P1 / P2; xie2023 P1 / P2. Subjects vs carriers checked both ways; no further
  statements on the pages.
- Two-org blocks: yan2017 block 1 prints lab, then university, directly (two orgs, ding2019 precedent, both map to the
  HUST id); szelag2017 block 1 and veiga2026 P2 University / Université Grenoble Alpes + structured CEA with unit LETI
  (lit batch precedents); veiga2026 P1 five orgs as printed, CEA/LETI-Minatec as one printed string (contains a site name
  as printed in the org string; alias request).
- Campus: thiel2026 blocks 1 / 5 / 6 University of California + `campus: "Santa Barbara"` (`org_ucsb`); zeng2026 block
  3 (comma form) and block 7 (no comma) University of Colorado + `campus: "Boulder"` (`org_university_of_colorado_boulder`).
- Empty fields: zeng2026 blocks 1 / 2 print no place, blocks 3 / 7 no country; sundaram2025 block 5 the state only.
- Country: xue2022 blocks 1 / 3 and yi2024a block 4 Hong Kong prints -> HK (D288); wang2026f UK -> GB; xue2022 block
  2 mainland place -> CN.
- Locators: wang2026f, yi2024a, zhang2024b `p.10 affiliations` (full lists on page 10, read); xue2026, yan2017 `p.1
  footnote`; all prose statements `p.1 footnote`.
- Markers: every readable author's printed run matches `markers` + `dropped_markers` in both layers; contact footnotes
  sun2025 4 5, wang2025b 3 4; equal contribution xue2026 3; symbol marks (asterisk, dagger, section, envelope) never
  used by a block.
- Parents: wang2025, wang2026f, xue2026, zhao2026 Chinese Academy of Sciences institutes keep the academy in the printed
  institute name (contract example); no parent copied elsewhere. yi2024a block 5 Jiaxing Research Institute Zhejiang
  University kept as printed.
- As printed: wang2025 Sun Yat-Sen vs xue2022 Sun Yat-sen; zhang2025c Technical University Eindhoven; szelag2017
  University Grenoble Alpes.

## Privacy and as-printed scan

- `privscan.py` (scratchpad `lit_h21_audit/`) over every line of `headers.yaml`, `header_rows.csv`, `compare.csv`,
  `unmapped_orgs.csv`, `papers.csv` and this record: contact / URL patterns, digit runs, street / building words, and
  the address words printed in this batch's blocks. Result: 0 contact, street, building or address-word hits in any
  file; digit hits only in dates (YAML, 2 lines) and, in this record, counts, process ids, dates and the lab name 2012
  Labs. That lab name is in no YAML or derived file after F2 (grep: 0).
- CEA/LETI-Minatec stays: it is the printed org string of veiga2026 P1, not a separate address.

## Commands (2026-11-02, log times)

| Command | Result |
|---|---|
| `check lit_h21 --corpus lit --dry-run` (before) 22:41:22 (pid 68801) | 0 errors, 5 warnings; slots 279, recorded 274, no_header 5, rows 366, 27 unmapped org strings |
| probes (`--dry-run`) 22:43:47-22:44:40 (pids 69548-69628) | W1 1 error; W2 3 errors; W3 2 errors; W4 0 errors; W5 2 errors; W6 0 errors, rows 365; Z1 3 errors; Z2 3 errors; S1 0 errors, rows 364. File restored and md5-verified after each |
| `check lit_h21 --corpus lit` 22:45:29 (log `lit_headers_check_lit_h21_69865_20261102T224529`) | 0 errors, 5 warnings; ok 24, partial 1, unreadable 0; rows 363 (grade A 363), recorded 273, no_header 6, present addresses 0; 27 unmapped org strings; stamp matches headers.yaml (sha256 b8717c8e...) |

Changes to `headers.yaml` (diff against the backup): sun2025 block 2 and note; wang2025 status, note, block 4, Xia Liu;
notes of sundaram2025, szelag2017, thiessen2020, xue2022, xue2026, yi2024a; nothing else. `header_rows.csv` loses 3 rows
net; `compare.csv` changes only in wang2025 #4; `unmapped_orgs.csv` unchanged. `aggregate` not run (coordinator).

## Checker gaps observed (scripts not edited)

- G1 "Present affiliation" is not a present-address cue and the cue is not skipped between marker and first field
  (zhang2025c); family of "Current address:" (kuyken2011, ji2017, koyaz2026, beeck2021).
- G2 The `postal code + city` scan pattern hits a lab name made of a number and a capitalized word (wang2025).
- G3 `skip_between` is compared in letters-and-digits form with a 10-letter gap slack, so a reformatted or truncated span
  passes both verification and the scan (W4, and the original value).

## Coordinator questions

1. wang2025 block 4: approve a narrow scan exemption, then re-record? Recommended: yes, before the rebuild. In
   `ADDRESS_RES`, `\b\d{4}\s+(?!Labs?\b)[A-Z][a-z]+` plus a test; then in wang2025 add block `{marker: "4", basis: printed,
   org: "Huawei Technologies Company Ltd.", unit: "Central Research Institute Planning, 2012 Labs", locality: "Shenzhen",
   country: "CN"}`, set Xia Liu `markers: ["4"]`, `status: ok`, drop the note sentence. Without it, the rebuild runs with
   slot #4 unrecorded.
2. G3: make `skip_between` / `skip_prefix` verification token-exact (whitespace-collapsed printed form, no letter slack
   around the span) so a reformatted span fails? Recommended: yes; re-run `check all` for both corpora first, since it may
   flag older spans.
3. wang2025 #5, wang2025b #2 #12, xue2026 #4, yoo2022 #9: five printed authors differ from the list at the same position
   and get no rows; add them to the D412 author-list correction file? Recommended: yes; until then they stay header-only.
4. wang2025b #5 (Li Xu / Li Qiang Xu), wang2026f #2 (Hui Jia / Hui Min Jia), xue2026 #2 (Chao Cheng / Chao Zeng Cheng):
   accept per D426 and add to the dropped-syllable review list? Recommended: yes.
5. yi2024a #11 "Daoxin Dai A": add to the D412 list? Recommended: yes.
6. zhang2025c #2: add "Present affiliation" to the cue set with "Current address:" and re-record (ASML, Veldhoven, NL,
   `present_address`)? Recommended: yes, in the checker follow-up pass, not blocking.
7. sun2025 follows the "lab and school, university" unit-chain precedent (F1), which round 3 question 3 left open. The
   D288 sentence on a department between a joint institute and a second org reads the other way: confirm the unit chain
   for this print and leave the older two-org rows? Recommended: yes.
