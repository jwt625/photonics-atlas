---
title: Fresh-context audit of the lit author-affiliation batch lit_h71 (1 paper)
date: 2026-11-25
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; checker run only in dry-run or write-run on scratch copies with logs in the scratchpad; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h71/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 lit rulings; D244, D246, D286d, D287 checker rules; format from the lit_h69 audit
verdict: GO; 5 slots audited, 5 recorded, 0 wrong rows, 0 imprecise rows; all 6 named extractor calls confirmed; no required fix
---

# Lit header batch audit: lit_h71 (2026-11-25)

## Scope

Batch lit_h71: 1 paper (jongebloed2026, Optics Express 2026, printed numeric markers, two blocks); 5 slots, 0
`slots_from_header`, 0 explicit slots; 7 rows. Restricted corpus: this record names only authors, orgs, units, cities
and countries; no contact, street, building, box or postal text is copied (such spans are named by type only).

## Method

- `uv run --offline python scripts/ofc_headers.py show lit_h71 --corpus lit --codes jongebloed2026` with and without
  `--pdf`; output kept in the session scratchpad `h71_audit/` only. text.md and the local PDF agree on the header.
- Per slot: printed name vs the `show` author list and `compare.csv`; marker run in both layers (PDF superscripts);
  block fields (org, unit chain, locality, country); role; locator; note. Codepoints of the two hyphenated names
  checked against the PDF layer (ASCII hyphen, precomposed accented capital in both the PDF text and the YAML).
- All 7 rows of `header_rows.csv` read: roles primary 5, additional 2; basis printed 7; grade A 7; locator p.1 header
  7; org ids org_university_of_twente (4 rows), org_aluvia_photonics (3 rows: 1 primary, 2 additional), match basis
  name 7.
  `compare.csv`: 5 `recorded`, `order_differs` false on all 5; `unmapped_orgs.csv` header only (0 strings).
- Consistency with committed lit blocks of the same group: the identical block 1 form (org University of Twente,
  unit "Integrated Optical Systems, MESA+ Institute for Nanotechnology", Enschede, NL) is committed in lit_h01
  garciablanco2025, lit_h22, lit_h28, lit_h36 osorniomartinez2025, lit_h47 and lit_h70 osorniomartinez2025a; the
  identical block 2 form (org ALUVIA Photonics, no unit, Enschede, NL) in lit_h01 and lit_h36. Registry: both org ids
  exist (ALUVIA Photonics curated from garciablanco2025; University of Twente ROR exact).
- Address / contact scan of `headers.yaml` and every derived file (contact sign, URL, www, 3+-digit numbers, the
  printed postal code and its letter suffix, street, road, box, building, room, campus, mail, phone, fax, and Twente
  campus / street tokens). Hits: "DevLog-011" in the file comment, the digits of the source code, the stamp hash,
  and the type words "postal code" in the note. No contact, URL, postal code, street, building or box text anywhere,
  note included.
- Probes on scratch copies (`h71_audit/probe.py` + `mk.py`, scratch `LIT_BASE`, batch name `lit_p71`,
  `cmd_check(..., dry_run=True)`, `RunLog` redirected to the scratchpad: no log written under `logs/`; 13 runs incl.
  the base dry and write runs). Dry run of the batch as written: 0 errors, 0 warnings; scratch write-run derived
  files byte-identical to the stamped `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`, `check_stamp.txt`
  (stamp sha256 f2f6f256... matches `headers.yaml`). md5 of every repo batch file identical before and after the
  audit.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h71 | 1 / 1 | 5 | 5 | 0 | 0 |

- Papers ok 1, partial 0, unreadable 0; `slots_from_header` 0; `author_list_differs` 0; explicit slots 0; order
  warnings 0; present addresses 0; dropped markers 0; unreadable authors 0; unmapped org strings 0.
- Per paper (slots / rows): jongebloed2026 5 / 7.
- Privacy findings: 0. Notes: 1 correct.

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (5) | 5 | 0 | 0 |
| markers (printed, 5) | 5 | 0 | 0 |
| header position / order | 5 | 0 | 0 |
| blocks (org / unit / locality / country) (7 rows) | 7 | 0 | 0 |
| roles (primary / additional) | 7 | 0 | 0 |
| locators | 7 | 0 | 0 |
| notes (1) | 1 | 0 | 0 |

## Per-paper findings

- jongebloed2026 (5; printed). Author line in capitals with initials, four lines: B. JONGEBLOED 1,2;
  C. E. OSORNIO-MARTINEZ 2; K. WANG 1; M. DIJKSTRA 1 and S. M. GARCÍA-BLANCO 1,2,*. YAML names, order and marker
  lists equal the print; header_pos 1-5 = list slots 1-5. Author list Bjorn Jongebloed, Carlos E.
  Osornio-Martinez, Kai Wang, Meindert Dijkstra, Sonia M. García-Blanco (Unicode hyphen): every printed initial run
  agrees with the list given names and middle initials, so name matching needs no explicit slot. Block 1 prints the
  group, the MESA+ institute, the university, a postal code glued before the city, then the country; block 2 prints
  ALUVIA Photonics, the city and the country. One contact line after block 2 (masked in `show`; nothing recorded).
  ok.

## Extractor calls (verified)

1. Capitalised printed names recorded as printed and auto-matched to the author list, no explicit slots. Probe P9
   (list form "Bjorn Jongebloed" as YAML name) 2 errors (not printed); probe P5 (authors 3 / 4 swapped) 4 errors and
   1 order warning. The capitals form is the committed lit practice for this group (lit_h01, lit_h36, lit_h70).
   Confirmed.
2. Asterisk (corresponding author) ignored. Probe P6 (asterisk added as a marker) 1 error (marker has no block); the
   asterisk points to the masked contact line only, so no `dropped_markers` entry is needed (base run passes the
   marker comparison with the asterisk excluded). Same note wording as lit_h36 / lit_h70. Confirmed.
3. Block 1 org University of Twente with unit chain "Integrated Optical Systems, MESA+ Institute for
   Nanotechnology" (printed before the org). Probe P1 (MESA+ dropped from the unit) 2 errors (unit-org not
   contiguous, D246). Probe P2 (MESA+ institute as org, University of Twente in `more_orgs`, group as unit) 0 errors,
   +4 rows, 0 unmapped: not better; the committed lit form (six batches listed above) keeps the university as org
   with the group + institute chain. Confirmed.
4. Block 2 ALUVIA Photonics with no unit. Probe P8 (company suffix added) 2 errors, +1 unmapped: the printed name
   carries no legal suffix. Confirmed.
5. Both blocks Enschede, NL ("The Netherlands" -> NL). Probe P3 (locality with the printed postal code) 7 errors
   (D244); probe P10 (block 2 country "") 0 errors (known gap: an empty country is accepted when the country is
   printed). Confirmed.
6. Org ids org_university_of_twente and org_aluvia_photonics, match basis name on all 7 rows; 0 unmapped.
   Confirmed.

Marker probes: P4 (OSORNIO-MARTINEZ given marker 1) 2 errors; P7 (JONGEBLOED without marker 2) 2 errors.

## Fixes (exact YAML edits)

No required fix: no slot, marker, block, field, role, locator or note is wrong. No optional edit.

## Observations (no YAML change)

- O1 Known gaps reconfirmed: an empty `country` is accepted for a block whose country is printed (P10); an accented
  capital written without the accent passes (P11, "GARCIA-BLANCO": 0 errors), so the accent was checked by reading
  (precomposed accented capital in both the PDF layer and the YAML).

## Lists for the coordinator

- D412 list: none.
- D426 review list: none (no explicit slots).
- Re-record list: none.
- Org round: none (0 unmapped strings).

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 0 warnings, 7 rows, 0 unmapped; derived files identical | batch as written |
| P1 / P2 | MESA+ out of the unit / MESA+ as org, Twente in more_orgs | 2 / 0 (+4 rows) errors | chain verified / committed form kept |
| P3 | block 1 locality with the postal code | 7 errors | D244 verified |
| P4 / P7 | OSORNIO-MARTINEZ + marker 1 / JONGEBLOED without marker 2 | 2 / 2 errors | markers verified |
| P5 | authors 3 / 4 swapped | 4 errors, 1 warning | order verified |
| P6 | asterisk as a marker | 1 error | asterisk correctly ignored |
| P8 | "ALUVIA Photonics B.V." | 2 errors, +1 unmapped | as printed verified |
| P9 | list form as YAML name | 2 errors | printed form verified |
| P10 | block 2 country "" | 0 errors | known gap (O1) |
| P11 | accent stripped from GARCÍA | 0 errors | known gap (O1) |
