---
title: Fresh-context audit of the OFC 2026 header-extraction batches ofc_h01..ofc_h15 + pilot (DevLog-008, before the people merge)
date: 2026-10-23
scope: DevLog-008 (D170-D179, D240-D249, D281-D289, D289 totals), data/_staging/people/ofc_headers/ (CONTRACT.md, pilot/, ofc_h01..ofc_h15/headers.yaml + header_rows.csv + compare.csv + unmapped_orgs.csv, org_requests.csv), scripts/ofc_headers.py (`show`, `check`), tests/test_ofc_headers.py
auditor: Claude (fresh context, read-only for repo data; scratch work outside the repo)
---

# Audit: OFC 2026 header-extraction batches

Verdict: the extraction is accurate. Of 491 audited author slots, 488 are ok, 1 is imprecise and 2 are wrong (0.4 %).
Both wrong slots have simple fixes. One of them comes from a gap in the checker: it never compares an explicit
`slot: 0` against an exact name match, and a scan of all 83 `slot: 0` authors finds only this one case. The other
comes from a branch-campus organization (The Chinese University of Hong Kong, Shenzhen) that was mapped to the Hong
Kong university. Totals, stamps and tests reproduce. **Go for the merge into people** once findings W1 and W2 are
fixed and the checker guard for S1 is added (one small YAML edit, one registry/alias decision, one checker rule).
S2 (org requests without locality) should be fixed before the org-curation stream resolves generic strings.

## What was run (2026-10-22 23:29-23:40 PDT; no network, no git writes)

| Step | Result |
|---|---|
| `uv run python scripts/ofc_headers.py check all` | exit 0; `errors 0, warnings 48` (46 explicit `slot:` overrides that are not name-compatible, 2 "listing_order although a local PDF exists" for Tu2D.2) |
| sha1 of every file under `data/_staging/people/ofc_headers/` before / after `check all` and pytest | identical: the checker rewrote nothing, so every `check_stamp.txt` matches its `headers.yaml` and the derived CSVs are the current output |
| `uv run pytest -q tests/test_ofc_headers.py` | 65 passed (7 third-party deprecation warnings) |
| Totals of the check run vs DevLog-008 D289 table | identical: 620 papers (ok 604 / partial 12 / unreadable 4), 4821 slots, 5477 rows (A 4954 / B 523; listing_order 514, layout 9), primary 4853 / additional 616 / present_address 8, outcomes agree 3920 / extra 422 / unmapped 379 / no_header 88 / conflict 11 / present_address 1, multi-affiliation slots 541 |
| `org_requests.csv` vs the union of the 16 `unmapped_orgs.csv` | same 120 strings, same counts; `proposed_org_id` empty for all 120 |
| Sample views | `show`-equivalent views (same `header_text`, `pdf_header`, `mask` functions; terminal only) of the 78 audited papers plus 6 for the systematic checks, with the local PDF page 1 for the 14 audited papers that have one |
| Independent scans of all 16 YAMLs | field hygiene, locality / country pairs, `slot: 0` vs metadata names, notes |

The checker run wrote its usual log to `logs/` (git-ignored). No repo file other than this audit was written.

## Method

Sample (fixed seed, script in the scratch folder): per batch ofc_h01..ofc_h15, 4 papers stratified as (1) a paper
with >= 2 `printed` blocks, (2) a paper with a `listing_order` block (grade B), (3) a paper with `dropped_markers` or
an explicit `slot:`, (4) a random non-unreadable paper. Plus every `conflict` slot (11), every `present_address` row
(8 rows), and 10 random `extra` slots (all batches + pilot). For each slot: printed name, slot assignment, recorded
markers and dropped markers (with reason), marker -> block mapping, org / more_orgs / unit / locality / country of
each block against the printed header (text extraction, and local PDF where present), basis and grade, and that no
field carries an e-mail, street, postal code or other text. Header-only authors (`slot: 0`) of the sampled papers
were checked against the metadata list.

Rating: ok = matches the print and the contract; imprecise = defensible data with a defect that does not put a wrong
org on a person (e.g. a stale note); wrong = a row or slot outcome that misstates the print or the institution.

## Counts

Stratified sample (60 papers):

| Batch | Papers (sampled codes) | Slots | Rows | ok | imprecise | wrong |
|---|---|---|---|---|---|---|
| ofc_h01 | M1E.4, M1F.1, M1D.2, M1I.4 | 40 | 56 | 40 | 0 | 0 |
| ofc_h02 | M2D.2, M2E.5, M2E.6, M1J.3 | 21 | 23 | 21 | 0 | 0 |
| ofc_h03 | M3C.5, M3A.6, M3D.6, M3C.2 | 31 | 35 | 31 | 0 | 0 |
| ofc_h04 | M3Z.8, M3Z.16, M4B.6, M3Z.10 | 43 | 45 | 42 | 1 | 0 |
| ofc_h05 | Tu2B.2, Tu2D.1, Tu2C.1, Tu2C.7 | 15 | 15 | 15 | 0 | 0 |
| ofc_h06 | Tu3B.2, Tu2D.2, Tu2E.4, Tu3C.4 | 28 | 27 | 28 | 0 | 0 |
| ofc_h07 | W1D.4, W1D.6, W1B.5, Tu3K.5 | 22 | 25 | 21 | 0 | 1 |
| ofc_h08 | W1G.3, W1G.6, W1G.7, W2A.22 | 44 | 44 | 44 | 0 | 0 |
| ofc_h09 | W2A.41, W2A.51, W2A.39, W2A.49 | 29 | 29 | 28 | 0 | 1 |
| ofc_h10 | W3A.6, W3K.6, W3E.4, W3D.5 | 26 | 28 | 26 | 0 | 0 |
| ofc_h11 | W4D.5, W4H.2, W4B.2, W4K.1 | 36 | 38 | 36 | 0 | 0 |
| ofc_h12 | Th1I.5, Th1D.5, Th1C.2, Th1J.3 | 33 | 43 | 33 | 0 | 0 |
| ofc_h13 | Th2A.18, Th2A.6, Th2A.38, Th2A.22 | 29 | 30 | 29 | 0 | 0 |
| ofc_h14 | Th2A.39, Th3A.6, Th2A.55, Th2A.58 | 24 | 27 | 24 | 0 | 0 |
| ofc_h15 | Th3F.2, Th3D.4, Th3E.3, Th3D.5 | 44 | 49 | 44 | 0 | 0 |
| **sample total** | 60 | **465** | 514 | **462** | **1** | **2** |

Slots = metadata slots of the paper (including the 12 `no_header` slots of these papers). The 60 papers also print 21
header-only authors (`slot: 0`): 20 correctly not in the metadata, 1 wrong (W2A.39, same finding as W2 below).
Stratum coverage: 15 multi-block printed, 15 listing_order (h12 has only one listing_order paper), 15 with dropped
markers or explicit slots, 15 random (2 of them `partial`: M1I.4, Th2A.22). Basis covered: printed, single, pdf
(W1B.5; among the targeted slots also M2C.3, Th4B.5, M3F.4), listing_order (incl. mixed printed / listing_order papers), `marker` "1" single blocks,
parenthesized markers, present addresses with numeric and dagger markers, joint blocks (`more_orgs`), shared orgs.

Targeted slots (outside the 60 papers, 18 more papers; 26 slots):

| Set | Slots | ok | imprecise | wrong |
|---|---|---|---|---|
| conflict (11; W1G.7 #10 already in the sample) | M2C.3 #13, M3K.4 #1, M3Z.6 #1 #2 #14, W1G.7 #10, W4H.1 #1 #2, Th2A.60 #10, Th4B.5 #17, Th1D.1 #20 | 11 | 0 | 0 |
| present_address rows (8; M1E.4 #6 in the sample) | M1E.4 #6, Th1F.5 #4 #5, M3F.4 #3 #4, M4E.6 #3, W3E.7 #6 #7 | 8 | 0 | 0 |
| random extra (10; M1F.1 #1 in the sample) | Th3F.1 #16 #6, Tu2J.5 #6, Th2A.9 #3 #1, Th3F.3 #2, M2K.7 #3, Th2A.47 #1, M1F.1 #1, Th3F.5 #4 | 10 | 0 | 0 |
| **targeted unique (overlaps removed)** | 26 | 26 | 0 | 0 |

**Overall: 491 slots audited; ok 488, imprecise 1, wrong 2.**

All 11 conflicts are real disagreements between the printed header and the organizer metadata. The header is read
correctly in each (e.g. W1G.7 #10 printed marker 1 = SJTU vs metadata PKU; Th4B.5 #17 PDF `^{4}` = Lightera vs
metadata Nokia; M3K.4 #1 single Nokia Bell Labs block vs metadata MIT). Three of them are registry-level near-identities
rather than person-level conflicts: M3Z.6 #1 #2 #14 (ICCS vs NTUA) and W4H.1 #1 #2 (Telefonica I+D vs Telefonica
Innovacion Digital). The D241 / D281 review handling covers them.

## Non-ok slots

| # | Batch / paper / slot | Rating | Evidence | Fix |
|---|---|---|---|---|
| W1 | ofc_h09 W2A.39 #6 (Weisheng Hu) | wrong | The header prints 6 authors ending in "Weisheng Hu" (single SJTU block). The metadata has 6 slots with slot 6 = "Weisheng Hu" (`papers.csv` n_authors_meta 6). The YAML sets `slot: 0`, `author_list_differs: true` and the note "metadata 5". Result: slot 6 is `no_header`, no header row, and Weisheng Hu is in the local header-only list (the D289 count of 83 includes him) | Remove `slot: 0`, set `author_list_differs: false` and delete the note clause; re-run `check ofc_h09` + `aggregate`. Slot 6 becomes `agree` (1 row, single, grade A); header-only authors 82 |
| W2 | ofc_h07 W1B.5 #9 (Connie J. Chang-Hasnain), block 3 | wrong | Printed (text and PDF): "School of Science and Engineering, the Chinese University of Hong Kong, Shenzhen, China". Recorded as org "the Chinese University of Hong Kong", locality "Shenzhen", CN, mapped to `org_chinese_university_of_hong_kong` (registry: CUHK, HK). The institution is The Chinese University of Hong Kong, Shenzhen, a separate university, so the merge would give her a CUHK (Hong Kong) observation and a wrong `extra` root. Only occurrence in all 5477 rows (scan of orgs at branch-campus cities) | Keep the printed fields but do not map them to CUHK: either record the org as printed including ", Shenzhen" (if the checker accepts the locality inside the org segment) with an alias to a new registry org for CUHK-Shenzhen, or add a scoped alias keyed on (printed org, locality Shenzhen). Until then the row should be unmapped, not CUHK |
| I1 | ofc_h04 M4B.6 #8 (metadata Wing Wang; header Qing Wang) | imprecise (note) | The outcome follows D287 (`slot: 0`, slot 8 `no_header`), but the paper note still says "header Qing Wang to slot 8 Wing Wang (same position ...; treated as metadata spelling)" before the appended D287 clause "not matched ... slot 0". The note contradicts itself | Delete the superseded clause (see S3; same pattern in 5 more notes) |

Slots rated ok with a coverage caveat (contract-conformant `unreadable`; no wrong data, but readable information is
dropped): M1I.4 #10 (markers 1 and 4; block 4 printed with an asterisk), Th2A.22 #1 #2 (markers 1, 2; block 2 has a
stray digit inside the unit chain, so the contiguity rule cannot pass), Th2A.38 #1 (markers printed "13", no block 3).

## Systematic issues

| # | Issue | Evidence | Recommendation |
|---|---|---|---|
| S1 | The checker never checks `slot: 0` against the metadata names. `match_slots` skips name matching for any author with `slot:` set, and slot coverage only requires `author_list_differs` | W1. Scan of all 83 `slot: 0` authors: 1 has an exact match to an unused metadata slot (W2A.39). The other 8 with a family-name hit are the D287 rulings (Qing / Wing Wang, Ziawei / Jiawei Luo, Huanyu Le / Le Yu, R. M. / Mark Stevenson x2, J. I. / Iwan Davies, Sheng-Fu / Vincent Lin) or a different person (M1J.2 Peng Li vs hongmin Li) | Checker error when a `slot: 0` author has an exact match (or a unique compatible match) to a metadata slot that no other header author takes. Add a pytest mutation |
| S2 | Branch campuses printed as "University, Campus" are split into org + locality. Org requests carry only `printed_org` | W2 (wrong mapping). Same pattern, unmapped: M4F.1 "University of California, Department of Electrical and Computer Engineering Davis" -> org "University of California", locality Davis; W3C.2 "Indian Institute of Technology, Delhi" -> org "Indian Institute of Technology", locality Delhi. `org_requests.csv` has `printed_org, count, locators, proposed_org_id`, while the per-batch `unmapped_orgs.csv` also holds unit and country. Generic strings ("University of California", "Indian Institute of Technology") cannot be resolved without locality | Add `locality` / `country` (and unit) to `org_requests.csv`, and let curation aliases for generic names be keyed on (printed_org, locality). Contract line: a campus that is a separate institution (CUHK-Shenzhen, HKUST (Guangzhou) precedent) is part of the org, not the locality |
| S3 | Stale notes after the D287 slot-0 changes: the original "matched to slot N" clause was kept and the D287 clause was appended | M4B.6 (h04), Tu3D.1 (h06), W1J.2 (h08), W1D.3 (h07), W4K.5 (h11), Th2A.8 (h13). The slot data are right; the notes contradict themselves | Delete the superseded clause in these 6 notes (notes go to the local extra-authors list, not to the people rows) |
| S4 | Meaning of `extra`: `_outcome` returns `extra` when the roots match but an unmapped header string is present, and registry parent chains fold real second orgs into `agree` | Th1I.5 #1 #2 #5 #6 #9-#11 and M2C.3 CTRI slots are `extra` only because the unmapped "State Key Laboratory of Optical Fiber and Cable Manufacture Technology" string is present. Th3F.2 #1 is `extra` only because of "imec-Ghent University". M2E.5 #8 #9 and M3D.6 #5 #7 #8 are `agree` although they print Optics Valley Laboratory or SJTU-Pinghu Institute (registry children of HUST and SJTU) | Not an extraction error. The merge must use the header rows, not the `extra` label, to decide what is new. Report "extra (mapped)" separately from "extra (unmapped string only)" in the totals |
| S5 | One printed lab, two encodings: the SKL of Optical Fiber and Cable Manufacture Technology is a `unit` of YOFC in YOFC blocks and a separate org (`org` / `more_orgs`) when printed beside China Telecom Research Institute | W2A.22, Th1J.3, M2C.3 block 2 (unit) vs M2C.3 block 1, Th1I.5 block 1 (org). Both follow the contract (sub-unit vs separately printed org). It is the largest org request (61 rows) | Curation: register it as a child of YOFC, so CTRI-printed rows resolve to YOFC + CTRI and not to an orphan string |
| S6 | `listing_order` (grade B) cannot be checked against PDFs (no local PDF for those papers; Tu2D.2's PDF text is garbled) | Indirect check: 444 slots in 64 papers have a listing_order row; outcomes agree 326, extra 52, unmapped 66, conflict 0. The 15 sampled listing_order papers read correctly against the printed block order | Keep grade B (D240). No action |
| S7 | DevLog-008 timestamps | Progress entries "23:30" and "23:45 (D289)" are later than the last coordinator `check all` / `aggregate` logs (23:27:33-23:28:08 PDT) and later than this audit's run (23:29, clock 23:36). The numbers reproduce exactly | Correct the times to the log times |

Clean results (no finding):

- Field hygiene, all 16 YAMLs: no e-mail, URL, phone, street, postal code or building number in any field or note.
  A broader independent heuristic flagged 23 fields, all false positives: Tokyo / Osaka are the first printed city
  after a ward ("Bunkyo-ku, Tokyo"; Koganei is used correctly where printed first, e.g. Tu2J.4, M3C.2), Menlo Park /
  College Park / Park Ridge, "3D", and "FOTON-UMR6082" (a unit number, not an address). Names carry no markers.
- Locality / country: 333 distinct pairs reviewed. Every block with a locality and an empty country prints no
  country (e.g. Hubei Optical Fundamental Research Center "Wuhan" in W1I.5, W4J.2, Th2A.56; Yonsei "Seoul,"; US blocks with a state only). HK used only where Hong Kong is the printed place.
- Markers: every dropped marker in the sample points to a printed equal-contribution or "no longer affiliated"
  footnote (M3D.6, W1B.5, W1G.7, W3E.4, Th2A.47, Th3F.3). Every printed marker run equals markers + dropped markers.
  Multi-marker order is kept as printed (W3A.6 "2,1" -> primary block 2).
- Explicit `slot:` overrides in the sample follow D287 (M1D.2 Philippe / Phillippe, M3C.2 Mindaugaus / Mindaugas,
  M4B.6 Drew / Andrew and Shamsshooli, Tu2C.1 Ll. / Lluis, Th1C.2 Ming (Richard), Th2A.55 Hilmi Othman, Th2A.58
  D.Pavitra Varsha, Th3E.3 Mercinelli, Th3F.2 Shahin).
- Present addresses: all 8 rows carry a printed "Now with" / "now at" cue and the right role. M4E.6 #3 is the only
  `present_address` outcome (metadata Microsoft = printed present address).
- `org_requests.csv`: consistent with the batches. Typos and variants are copied as printed ("Franhofer HHI",
  "(EFPL)", "ZTE cooperation", "Yangtze Optica Fibre"), which is correct for alias requests.

## Go / no-go

**Go** for the merge into people (DevLog-008 merge path items 1-8, people-stream owner), on three conditions:

1. W1: fix W2A.39 in `ofc_h09/headers.yaml`, re-run `check ofc_h09` and `aggregate`.
2. W2: W1B.5 block 3 must not map to `org_chinese_university_of_hong_kong` (CUHK-Shenzhen org or alias decision).
3. S1: checker rule plus test for `slot: 0` against exact / unique name matches. Re-run `check all` (expected: no new
   error except any further case the rule finds).

Before org curation: S2 (locality in `org_requests.csv`; campus rule in the contract). Housekeeping: S3 notes, S7
DevLog times. Not blocking: S4 (merge must read rows, not the `extra` label), S5 (curation), S6.
