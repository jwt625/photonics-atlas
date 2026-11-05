---
title: Fresh-context audit of the lit author-affiliation batch lit_h23 (9 papers)
date: 2026-11-04
auditor: Claude (fresh context; wrote only this record; headers.yaml, derived files, scripts, tests, people and registry data not edited; aggregate not run)
scope: data/_staging/people/lit_headers/lit_h23/headers.yaml and derived files; both header contracts; DevLog-011 D350-D369, D380, D400-D442; previous audit 2026-11-02-lit-header-batch-h21-audit.md
verdict: GO for the people rebuild; 0 wrong and 3 imprecise slots in 72 audited (the 3 are one known checker gap, no row, never a wrong row); 2 note corrections proposed, no field changes; nothing applied
---

# Lit header batch audit: lit_h23 (2026-11-04)

## Scope

Batch lit_h23 (9 papers, 72 author-list slots). Restricted corpus: this record names only authors, orgs, units, cities
and countries; no paper text is quoted and no contact, street, building or postal text is copied.

## Method

- Every paper read with `uv run python scripts/ofc_headers.py show lit_h23 --corpus lit --codes <id> --pdf` (all 9);
  `--pages 2` added for wang2016a. Extractor notes treated as claims to test.
- Header pages of all 9 papers looked at as rendered images (`figures/` has no page 1 render for 8 of the 9, so page 1,
  and page 2 of wang2016a, were rendered to the session scratchpad and deleted after reading).
- Per-slot expectation typed from those renders in `expected.py`, then diffed against `header_rows.csv` on org, unit,
  locality, country and row order: 72 slots, 114 rows expected, 114 rows found, 0 differences. `headers.yaml` had been
  read before this, so it is a mechanical cross-check of the reading against the rows, not a blind extraction.
- Markers: printed run vs `markers` + `dropped_markers`, text layer, PDF layer and render, for all 9.
- Missed blocks: cue scan over the whole `text.md` of all 9 (present / current address, present affiliation, now with /
  at, is / are now, currently, permanent, on leave, visiting, deceased, retired, also with, formerly, corresponding
  author, equal contribution), every hit read. Only hits on an affiliation: the zhuang2025 clause (recorded) and the
  yulaev2022 supplement title page on p.25, which repeats the same two blocks. Other hits are body text or contact
  lines. No present address in the batch.
- Org mapping: all 24 (org, id, match basis) triples of `header_rows.csv` read; none wrong.
- Claims tested with dry-run probes on a scratch copy of the batch (`probe.py`, via the module's `LIT_BASE`); the repo's
  `headers.yaml` was never touched, md5 asserted after the probe run; each probe left only a dry-run log in the
  git-ignored `logs/`. Helpers: `audit_lit_h23/` in the session
  scratchpad.
- Stamp: `check_stamp.txt` matches `headers.yaml` (sha256 df145c2b...). Derived files untouched by this audit (mtimes
  18:32).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h23 | 9 / 9 | 72 | 69 | 3 | 0 |

- Rows 114 (all grade A); recorded 68; no_header 4; ok 8, partial 1, unreadable 0; 9 unmapped org strings.
- The 4 `no_header` slots: wessling2022 #5 (correct, not printed in the header); zhuang2025 #9 #12 #13 (C1).
- Per paper (slots / rows): wang2016a 7 / 7; wang2023d 11 / 11; wessling2022 9 / 8; wu2018 4 / 4; yang2026 13 / 49;
  yasui2026 7 / 9; yulaev2022 3 / 4; zhang2026c 5 / 10; zhuang2025 13 / 12. In yang2026: 22 rows for the three
  non-USTC orgs, 27 USTC rows; 49 in all.

## Rulings on the points flagged for attention

| paper | what the page shows | ruling |
|---|---|---|
| zhuang2025 | p.1 footnote: four statements. Statement 1 Dongwei Zhuang with Peng Cheng Laboratory (Shenzhen, CN), then two clauses: State Key Laboratory of Luminescence and Application, Changchun Institute of Optics, Fine Mechanics and Physics, Chinese Academy of Sciences (Changchun, CN) and Center of Materials Science and Opto-electronics Engineering, University of Chinese Academy of Sciences (Beijing, CN). Statement 2 nine authors with Peng Cheng Laboratory (Shenzhen, CN). Statement 3 Baisong Chen, Junfeng Song with State Key Laboratory of Integrated Optoelectronics, College of Electronic Science and Engineering, Jilin University (Changchun, CN). Statement 4 Li Qin with the same Changchun institute and laboratory as clause P2 | P1-P6 correct, in printed order, `clause` flags correct, subjects vs carriers correct both ways. Article on P1 as printed (D288) and it maps to the same id as P4. Unreadable claim: see C1 and N2 |
| wessling2022 | p.1 header: two side-by-side groups. Left: Wessling, Guilhabert, Toon, Dawson, Strain above Institute of Photonics, Department of Physics, University of Strathclyde (Glasgow, GB). Right: Ghosh, Kappers, Oliver above Cambridge Center for Gallium Nitride, University of Cambridge (Cambridge, GB) | `grouped` correct (D368); YAML in printed order, slots by name, warning correct (D363). All 8 slot assignments checked in `compare.csv`. A. Hinz (#5) is not in the header; in the text only as a co-author in the reference list (3 hits). `author_list_differs: true` and no row correct. Probe H1: adding the name fails D368 |
| yang2026 | p.1 header: four blocks, as recorded | All 13 marker runs correct, including the printed order 3, 2 on Jiu-Peng Chen. Blocks 2 and 4 org + `more_orgs` {USTC, CAS Center unit, own place}; block 3 org + USTC string; block 1 unit chain. Exact form of lit_h10 wang2026b blocks 1-3 and lit_h04 ye2023 block 7; the unit chain in block 1 matches h21 sun2025 (D442). Rows per org: Jinan 9, Hefei National Laboratory 8, Shanghai 5, each with a USTC row carrying the right unit and place |
| zhang2026c | p.1 header: both blocks print a postal designation and the country, no separate city | `locality: ""`, country `CH` correct: Lausanne stands only inside the org name in block 1 and is absent from block 2 (the contract's Hong Kong inside an org rule applies the same way). Note names the type only. Probes L1, L2: see G3. Block 2 org `EPFL` + unit follows lit_h09; maps to `org_epfl` |
| wang2016a | p.1 cover: title, volume, names without any block. p.2: author line, single unmarked block | `locator: "p.2 header"`, `basis: single`, `markers: []` correct (D366). Unit, org, Vancouver, CA correct; region and postal code not recorded. Probe C1: without the locator the checker fails, so the locator is load-bearing |
| wang2023d | p.1 header: markers in parentheses; Hengyu Wang and Yang Xu carry 1 and 4; 4 is an equal-contribution line, printed like a block | `dropped_markers` correct on exactly those two; not recorded as a block. Asterisks (1, 2, 3 stars) sit on Yuan Dong, Lianxi Jia and Zhanshi Yao and point to contact lines: ignored correctly (D286d). Probe A1: removing the drop fails, so it is binding |
| wu2018 | p.1 header: single block printed with 1; Moss carries 1 and a; a points to a correspondence footnote | `printed`, marker 1 (D285), `dropped_markers` a with reason contact footnote correct. Hawthorn first printed place, state not recorded, AU. Probe A2: drop not binding on a last author (G2); the value is right regardless |

Other papers:
- yasui2026: all 7 marker runs correct; the given and family name of author 1 printed without a space (note correct, render
  confirms); S. Adachi (#5) is Satoru Adachi, initial agrees; NTT labs recorded as printed, this print has no NTT
  Corporation (lit_h03, lit_h09 have it and record it, so no conflict); Atsugi and Sapporo, region not recorded.
- yulaev2022: University of Maryland + `campus: "College Park"` + `locality` correct (D301), maps to the College Park id;
  NIST unit as in lit_h14. The contact block printed below the header names a NIST division and a street for Aksyuk: not
  an affiliation block, not recorded (correct), so his row keeps the laboratory printed for marker 1. Asterisk note
  correct. Daron A. Westly and Vladimir A. Aksyuk vs list without the middle initial: correct, same positions.
- Parents: wang2023d, zhuang2025 Chinese Academy of Sciences institutes keep the academy in the printed name (contract
  example); no parent copied elsewhere.
- Country: UK -> GB, USA -> US, P. R. China -> CN, all printed in the block; nothing inferred.
- Name scan: every list name vs printed name in `compare.csv` read; only middle-initial or initial-form differences
  (Menno J. Kappers, Michael John Strain, S. Adachi, Daron Westly, Vladimir Aksyuk); no common-name match by position.

## Findings and proposed fixes (not applied)

| # | paper, slots | rating | evidence (locator) | proposed fix (field: before -> after) |
|---|---|---|---|---|
| C1 | zhuang2025 #9 #12 #13 (Qibing Wang, Zhixue He, Lei Wang), P4 | imprecise, not fixable in the batch (no row) | p.1 footnote, statement 2: the three names, the verb and the org lose their word spaces in both text layers. The rendered page shows them with tight spacing and is clear: all three are with Peng Cheng Laboratory, Shenzhen, CN, which is what P4 records. Probe Z1 (readable, `status: ok`): 6 errors, not named in the statement subject (md, pdf). Handling matches psaila2024, liu2025a, naraine2024; never a wrong row | None in the YAML now. After a checker fix (question 1): remove the 3 `unreadable: true`, `status: ok`, drop the note sentence; rows 114 -> 117, recorded 68 -> 71, no_header 4 -> 1 (probe Z2: 0 errors) |
| N1 | yasui2026 (note only) | note unsupported | Note says the asterisk on Xuejun Xu marks the corresponding author. No legend for it on the p.1 render, and no correspondence line anywhere in `text.md` (the word stem has 2 hits, both body text; the other asterisks in the text are garbled equation glyphs). Marker handling itself is correct (unused symbol, D286d) | `note`: state that the asterisk on author 6 has no legend in the paper; keep the sentence on author 1. No field or row changes |
| N2 | zhuang2025 (note only) | note imprecise | Note says the end of statement 2 is printed without word spaces and the subject names cannot be verified. The render shows the spaces: only the text layers lose them, and it is the checker that cannot verify the names | `note`: say the text and PDF layers lose the word spaces, the page itself is readable, the checker cannot parse the three names. No field or row changes |

A note edit changes the YAML hash, so `check lit_h23 --corpus lit` must be re-run afterwards to refresh the stamp.

Unmapped org strings (9): not errors, for the org round. `aggregate` has not run on this batch, so 5 of them are new to
the org requests file: University of Strathclyde (not in the registry), Shanghai Research Center for Quantum Science
(the registry has the plural form, `org_shanghai_research_center_for_quantum_sciences`) and the 3 NTT lab strings (this
print form has no parent corporation; the registry has `org_ntt`). The other 4 are already requested: Hefei National
Laboratory, Jinan Institute of Quantum Technology, the Changchun institute, and the Shanghai institute (the registry
has it without the academy, `org_shanghai_institute_of_microsystem_and_information_technology`).

## Privacy and as-printed scan

- `privscan.py` (same scratchpad folder) over every line of `headers.yaml`, `header_rows.csv`, `compare.csv`,
  `unmapped_orgs.csv`, `papers.csv` and this record: contact / URL patterns, digit runs, street and building words, and
  the postal and street strings printed in this batch's blocks and contact lines. Result in all 6 files: 0 contact or
  URL hits, 0 printed postal or street strings. Street-word hits: 1 in the YAML (its header comment stating the rule) and
  the rest in this record (the words naming the type of text left out). Digit runs of 4 or more: years in paper ids, dates,
  and in this record also the probe times and ids; none is a postal code.
- No `skip_prefix` or `skip_between` in this batch, so no altered span (h21 G3) can occur here.

## Commands (2026-11-04, log times)

| Command | Result |
|---|---|
| `check lit_h23 --corpus lit --dry-run` 18:33:03 (pid 5305) | 0 errors, 1 warning (wessling2022 printed order, correct); slots 72, recorded 68, no_header 4, rows 114 (grade A 114; primary 76, additional 38; grouped 8, printed 87, prose 12, single 7); ok 8, partial 1; multi-affiliation slots 18; present addresses 0; 9 unmapped org strings |
| probes on the scratch copy (`cmd_check` with `dry_run=True`), run twice, 18:37:47-18:38:28 and 18:39:55-18:40:36 | Z1 6 errors; Z2 0 errors (rows 117, recorded 71, no_header 1); L1 0 errors; L2 2 errors; H1 2 errors; A1 2 errors; A2 0 errors; C1 2 errors. Repo `headers.yaml` md5 unchanged |
| `privscan.py` over this record and the batch | 0 contact, 0 printed postal or street strings; word hits as described above |

| probe | change | result | reading |
|---|---|---|---|
| Z1 | zhuang2025 #9 #12 #13 readable, `status: ok` | 6 errors, not named in subject (md, pdf) | extractor's claim confirmed: not recordable under the current checker |
| Z2 | Z1 + monkeypatch of `_subject` candidates: strip a leading glued "and", split at lower-to-upper case | 0 errors, rows 117 | a small parser change is enough for this paper; not tested on other batches |
| L1 | zhang2026c block 1 `locality: "Lausanne"` | 0 errors | G3 |
| L2 | zhang2026c block 2 `locality: "Lausanne"` | 2 errors, locality not inside the block | Lausanne is not printed in block 2 |
| H1 | wessling2022 A. Hinz added to group 1 | 2 errors, not printed before the block | not in the header, confirmed |
| A1 | wang2023d Hengyu Wang without the dropped marker 4 | 2 errors, printed markers differ | drop binding |
| A2 | wu2018 Moss without the dropped letter a | 0 errors | G2 |
| C1 | wang2016a block without its locator | 2 errors, first field not printed | locator binding |

## Checker gaps observed (scripts not edited)

- G1 Statement subjects with lost word spaces: `_subject` splits candidates at commas and the word "and", so glued names
  are never split (zhuang2025; family of G5 in the 2026-10-29 round 2 audit: cheung2022, psaila2024, liu2025a,
  naraine2024). Rows lost, none wrong.
- G2 Last-author marker run: with `exact=False` only the recorded markers must start the run, so a further printed
  marker on the last author is not enforced and a `dropped_markers` entry there is neither required nor verified (wu2018
  Moss, probe A2). Same area as the last-author marker window gap in D442 (chen2024b #6). The value here is right by
  reading.
- G3 A locality counts as inside the block when it appears only in the org name (zhang2026c block 1, probe L1). This
  batch is correct with an empty locality, but the checker would not catch the wrong form.

## Coordinator questions

1. G1: add run-together handling to the subject parser (probe Z2 form, with a test), then re-record zhuang2025 #9 #12
   #13? This is question 5 of the 2026-10-29 round 2 audit, open as far as DevLog-011 shows, with 3 more slots. Recommended: yes, in the checker
   follow-up pass, not blocking; re-run `check all` for both corpora first and re-read the older papers, since the other
   four papers were not probed.
2. N1, N2: apply the two note corrections and re-run `check`? Recommended: yes, before `aggregate`; no row changes.
3. Older form, seen by grep only: lit_h03 qi2024 P8 records Hefei National Laboratory as a unit of USTC, while lit_h04
   ye2023, lit_h10 wang2026b and this batch record two orgs. qi2024 was not re-read, so whether its print differs is
   open. Recommended: check in the org round; lit_h23 follows the majority form for this exact print.

## Verdict

GO. No slot carries a wrong person, org, unit, city, country or marker, nothing is invented, no block is missed and no
address or contact text is recorded. The 3 slots without rows are correct under the current checker and the known
never-guess handling.
