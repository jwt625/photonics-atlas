---
title: Fresh-context audit of the lit author-affiliation batch lit_h33 (21 papers)
date: 2026-11-08
auditor: Claude (fresh context; wrote only this record; headers.yaml, derived files, scripts, tests, people and registry data not edited; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h33/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369, D400-D522; format and precedent from the 2026-11-06 h27 audit
verdict: GO for the people rebuild (no slot wrong); 190 author-list slots audited, 186 ok, 4 imprecise, 0 wrong; F1 (tian2025, 4 slots: the manuscript footnote statement on page 2 is fully verifiable and carries unit and country the cover blocks lack) fixable now, choice in question 1; nothing applied
---

# Lit header batch audit: lit_h33 (2026-11-08)

## Scope

Batch lit_h33 (21 papers: 13 Optica Publishing Group headers (2 with a single unmarked block), 3 Nature-family
first-page footnotes, 2 arXiv-style preprint headers, 1 Research Square preprint with a cover page, 1 De Gruyter
footnote, 1 Wiley footnote; 190 author-list slots; 230 rows). Restricted corpus: this record names only authors, orgs, units, cities and countries; no paper text is
quoted and no contact, street, building, site or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h33 --corpus lit --codes <id> --pdf`
  (all 21; output kept in the session scratchpad only); xiang2021 also with `--pages 7` (symbol legend) and tian2025
  with `--pages 2 3` (manuscript first page after the cover). Both text layers carry every numeric marker legibly; the
  Nature Communications layout of xiang2021a prints several markers on the next line (both layers agree).
- Per slot: printed name vs `compare.csv` slot, printed marker run vs `markers` + `dropped_markers`, block fields vs the
  print (org, unit, campus, city, country), parents, locator. All distinct (org, place, ids, locator, role) tuples of
  `header_rows.csv` read; no wrong mapping.
- Dropped contact markers: the first character of each masked contact line in `text.md` read (address not copied):
  wang2025a marker 4, wu2023a marker 7, xie2026a markers 6 and 7 each start their contact line; xiang2021 dagger and
  double dagger are contact lines in the page 7 legend, the asterisk is equal contribution there.
- Missed blocks: cue scan of the whole `text.md` of all 21 papers (now with / at, present / current address, present /
  current affiliation, currently, presently, also with, is / are / was / were with, on leave, visiting, formerly,
  deceased, permanent address). Header hit only in tian2025 (page 2 footnote statement, see F1). Other hits are body
  text (trappen2020, wu2023a, xiang2021, xie2017, xu2016, xu2019) or a biography on the last pages (worhoff2015). No
  present address and no missed block in any other paper.
- Claims tested with dry-run probes on a scratch copy of the batch (`probe.py`, via the module's `LIT_BASE`; md5 of every
  repo batch file asserted unchanged after the run).
- Stamp: `check_stamp.txt` matches `headers.yaml` (sha256 5b5ca479...). `headers.yaml`, stamp and derived files all
  12:12 local time; repo batch files untouched by this audit (md5 before / after identical).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h33 | 21 / 21 | 190 | 186 | 4 | 0 |

Per field over the 190 slots:

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot | 190 | 0 | 0 |
| markers (incl. `dropped_markers`) | 190 | 0 | 0 |
| org | 190 | 0 | 0 |
| unit | 186 | 4 (tian2025, F1) | 0 |
| locality | 190 | 0 | 0 |
| country | 186 | 4 (tian2025, F1) | 0 |
| locator | 190 | 0 | 0 |
| present address | 190 (none printed) | 0 | 0 |

- Rows 230 (all grade A: printed 210, single 12, per_author 4, grouped 4; primary 188, additional 42, present address
  0); recorded 188, no_header 2 (wang2025a #2, xie2026 #9: printed name not compatible with the list form, `slot: 0`,
  correct); papers ok 21, partial 0, unreadable 0; parked papers none; `author_list_differs` 2; `order_differs` 1 paper
  (wu2023a, all 13 slots); 19 unmapped org strings.
- Per paper (slots / rows): spencer2014 4 / 4; stokowski2024 11 / 15; su2014 7 / 7; sun2013a 8 / 8; sun2024 17 / 19;
  suzuki2014 14 / 14; suzuki2015 7 / 7; tian2025 4 / 4; trappen2020 15 / 25; velha2016 8 / 8; wang2025a 7 / 7;
  worhoff2015 4 / 4; wu2023a 13 / 24; xiang2021 13 / 14; xiang2021a 15 / 16; xie2017 4 / 5; xie2026 10 / 11;
  xie2026a 10 / 14; xin2024 14 / 19; xu2016 2 / 2; xu2019 3 / 3.

## Per-paper findings

| paper | ok / imprecise / wrong | notes |
|---|---|---|
| spencer2014 | 4 / 0 / 0 | UCSB `campus` Santa Barbara (D449 / D461); Aurrion, Goleta; block 3 Aarhus University, Department of Engineering, Denmark, no separate city (locality empty correct; probe N3 shows Aarhus passes only because it is inside the org name, as Hong Kong in D249) |
| stokowski2024 | 11 / 0 / 0 | Nature footnote, `p.1 footnote` on all 3 blocks (h27 F1 rule); Stanford (Applied Physics + Ginzton; Electrical Engineering), NTT Research PHI Labs, Sunnyvale; list Tae-Won Park / M. M. Fejer automatic |
| su2014 | 7 / 0 / 0 | MIT RLE Cambridge; University at Albany CNSE (matches 6 committed rows); misspelt state not recorded |
| sun2013a | 8 / 0 / 0 | mononym Purnawirman explicit slot 2 (list carries the same single name); Thomas N. Adam block 2 |
| sun2024 | 17 / 0 / 0 | Nature footnote, `p.1 footnote`; marker 6 equal contribution (legend printed) in `dropped_markers`; UCSB printed without the comma, campus field correct; Morton Photonics Palm Bay, Honeywell Aerospace Technologies Plymouth |
| suzuki2014 | 14 / 0 / 0 | AIST Network Photonics Research Center / Nanoelectronics Research Institute, Tsukuba; prefecture not recorded; list T. Chiba automatic |
| suzuki2015 | 7 / 0 / 0 | single unmarked block, AIST NPRC Tsukuba |
| tian2025 | 0 / 4 / 0 | F1: cover blocks correct as far as they go, but the manuscript statement on page 2 carries unit and country and the note's reason for not using it is inaccurate. #1 printed Yu Tian, list Yu Peng Tian: automatic (dropped given-name syllable or middle name, common family name), D426 review list. #4 explicit slot 4 (distinctive family name, missing middle initial and hyphen, D369) correct |
| trappen2020 | 15 / 0 / 0 | KIT IPQ Karlsruhe / IMT Eggenstein-Leopoldshafen; Vanguard Photonics; Ficontec Achim; Ghent University - imec dash form kept (D426) with Photonics Research Group, Gent BE; Fraunhofer HHI full name as one org (6 committed rows in the same form family); LioniX International B.V. Enschede NL |
| velha2016 | 8 / 0 / 0 | SSSA + TeCIP Institute unit and CNIT + Laboratory of Photonic Networks unit from the dash-joined forms: identical to committed rows (4 earlier blocks); Ericsson Research Pisa |
| wang2025a | 7 / 0 / 0 | #2 printed Qi Wang vs list Q.P. Wang: initial P unexplained, common family name, `slot: 0` + `author_list_differs` (D369; probe N1: 0 slots); dagger equal contribution, marker 4 contact (verified); SYSU unit chain joined by and; Liobate Technology Nanjing; Hefei National Laboratory |
| worhoff2015 | 4 / 0 / 0 | De Gruyter footnote recorded `grouped` (D461 yang2018 rule): G1 corresponding author, G2 the other three; LioniX BV Enschede NL; `p.1 footnote` |
| wu2023a | 13 / 0 / 0 | printed order differs from the list (warning, slots by name); marker 7 contact (verified); SIOM + CAS as one org (contract example form); Shanxi University, Shandong Normal University, Shanghai Research Center for Quantum Sciences |
| xiang2021 | 13 / 0 / 0 | arXiv; symbol legend on page 7 (asterisk equal contribution, dagger / double dagger contact) matches the `dropped_markers`; UCSB ECE / Materials with campus; EPFL Institute of Physics Lausanne CH |
| xiang2021a | 15 / 0 / 0 | Nature Communications footnote, `p.1 footnote`; Caltech T. J. Watson Laboratory; Pro Precision Process and Reliability LLC Carpinteria; Anello Photonics Santa Clara; Morton Photonics West Friendship |
| xie2017 | 4 / 0 / 0 | HUST with WNLO + school as unit chain (one of the two committed forms, h27 question 4; corpus split stays with the org round); WRI State Key Laboratory unit |
| xie2026 | 10 / 0 / 0 | #9 printed Shuiying Xiang vs list shui xiang: different full given names, `slot: 0` + `author_list_differs` (probe N2: 0 slots); D412 correction-file candidate (truncated list name) |
| xie2026a | 10 / 0 / 0 | NJU four-unit ampersand chain identical to 5 committed rows; Yongjiang Laboratory Ningbo; Quanzhou University of Information Engineering; Ningbo University faculty + provincial key laboratory chain; University of Glasgow, UK printed -> GB (accepted printed form); markers 6 / 7 contact (verified); Yuechun Shi printed run 2, 1 kept in printed order |
| xin2024 | 14 / 0 / 0 | dagger equal contribution, asterisk corresponding (symbols); DRS Daylight Solutions San Diego (street not recorded); Bar-Ilan University Ramat-Gan IL; Stevens, Northwestern; David Barton III vs list David Barton automatic |
| xu2016 | 2 / 0 / 0 | single unmarked block, ZJU three-unit chain; campus name before Hangzhou not recorded (lit_h01, lit_h10 precedent) |
| xu2019 | 3 / 0 / 0 | Wiley footnote under the abbreviated names, `single` + `p.1 footnote`; slot 2 is the D412 artefact Daoxin Dai A (already on the list) |

## Findings and proposed fixes (not applied)

| # | paper, slots | rating | evidence (locator) | proposed fix |
|---|---|---|---|---|
| F1 | tian2025 #1-#4 (Yu Tian, Varam Voskerchyan, Francisco Soares, Francisco Diaz Otero) | imprecise (org correct; unit and country printed but not recorded; note reason inaccurate) | p.1 is a Research Square cover printing only the university under each name. p.2 (manuscript first page) prints the unmarked author line and a footnote statement naming all four authors: QOPHI lab, Atlantic research center of telecommunication, University de Vigo, Spain. In both text layers the words after the university are glued to the contact run without spaces, so `show` masks the whole line (same as D521 marinins2022); the checker's own preparation keeps them. Probe T1 (statement as P1, cover blocks removed): 0 errors, rows 230. No city is printed apart from the university name (probe T2 with locality Vigo also passes, only because Vigo is inside the org name; same reading as spencer2014 Aarhus): locality stays empty. D366 cover rule: when page 1 is a cover, the blocks of page N are the record | see the YAML below (option a of question 1) |

F1 YAML (replace the whole tian2025 record):

```yaml
- source_id: lit:tian2025
  status: ok
  note: "Research Square preprint: page 1 is a cover printing only the university under each name; the manuscript first page (text page 2) prints the author line without markers and a footnote statement naming all four authors (prose P1, locator p.2 footnote, D366 cover rule); the place words of the statement are glued to the contact text in both layers (masked by show, read by the checker, as D521 marinins2022); no city printed apart from the university name (locality empty); author 4 printed without the middle initial and hyphen of the list form Francisco J. Diaz-Otero (distinctive family name, explicit slot 4, D287 / D369)"
  affiliations:
    - {marker: "P1", basis: prose, org: "University de Vigo", unit: "QOPHI lab, Atlantic research center of telecommunication", locality: "", country: "ES", locator: "p.2 footnote"}
  authors:
    - {name: "Yu Tian", markers: ["P1"]}
    - {name: "Varam Voskerchyan", markers: ["P1"]}
    - {name: "Francisco Soares", markers: ["P1"]}
    - {name: "Francisco Diaz Otero", markers: ["P1"], slot: 4}
```

Effect (probe T1): rows 230 unchanged; tian2025 rows become `prose` grade A with unit and country ES; `rows_basis_per_author`
4 -> 0, `rows_basis_prose` 0 -> 4; the unmapped string Universidade de Vigo (no place) becomes University de Vigo (ES)
for the org round. Any change to the YAML changes its hash: re-run `check lit_h33 --corpus lit` afterwards to refresh the
stamp and derived files.

If the coordinator keeps the cover blocks (question 1, option c), only the note is wrong; N1 replaces the clause
"the manuscript footnote statement on page 2 is cut by contact masking after its first words and is not used" with
"the manuscript footnote statement on page 2 (unit and country printed; masked by show, readable by the checker) is not
recorded: cover blocks kept".

## Points checked and correct

- wang2025a #2 and xie2026 #9: `slot: 0` required (probes N1 / N2: removing it gives "matches 0 metadata slots"). Both
  list slots get no row (no_header). Recommended lists: xie2026 shui xiang -> D412 correction file (truncated given
  name); wang2025a Q.P. Wang -> D412 correction file or D426 review (list initials do not match the printed given name).
- tian2025 #1 Yu Tian vs Yu Peng Tian and xin2024 #12 David Barton III vs David Barton: automatic matches, the only
  candidates; tian2025 #1 goes to the D426 review list (dropped syllable, common family name, as spiga2016 #5).
- Locators: the five first-page-footnote papers (stokowski2024, sun2024, xiang2021a, worhoff2015, xu2019) carry
  `p.1 footnote` on every block; all header-layout papers keep the default. Probe N4 (xu2019 back to the default) still
  passes, so locators remain unverified by the checker (h27 G3); they were checked by reading.
- Symbols: asterisks, envelope marks and the xin2024 / wang2025a daggers are symbols; recorded as equal-contribution
  `dropped_markers` where the legend says so (wang2025a, xiang2021, xin2024), otherwise ignored (D286d); both are allowed.
- Country: every block prints its country (US from USA, GB from UK, NL from The Netherlands, CH, IL, IT, DE, BE, JP, CN,
  DK) except tian2025 cover blocks (none printed, `""` correct as recorded).
- Campus: UCSB `campus` on spencer2014, sun2024, xiang2021, xiang2021a (D449 / D461); ZJU campus name in xu2016 / xu2019
  left out (a campus of the same university in the same city, h27 question 5 reading); no other campus case.

## Privacy and as-printed scan

- Scan of `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`, `papers.csv`, `check_stamp.txt`:
  contact / URL / at-sign patterns, street words, digit runs of 4 or more, and 20 street, postal-box, building and region
  strings taken from the header pages. Result: 0 contact or URL hits, 0 printed street / postal / region strings; street
  words only in notes saying street addresses were not recorded; digit runs only paper-id years and the stamp hash.
- As printed (kept, correct): Scuola Superiore Sant'Anna with the typographic apostrophe; Xi'an with the typographic
  apostrophe; Sun Yat-Sen University; Ghent University - imec with the en dash; The Key Laboratory / The School with the
  leading article (D288); Fraunhofer HHI full form with (HHI); Karlsruhe Institute of Technology (KIT) with the acronym.
- No `skip_prefix` or `skip_between` in this batch. The F1 unit carries no address text.

## Commands (2026-11-08, log times)

| Command | Result |
|---|---|
| `check lit_h33 --corpus lit --dry-run` 12:13:13 (pid 24158) | 0 errors, 3 warnings (sun2013a / tian2025 explicit slots, wu2023a order); slots 190, recorded 188, no_header 2; rows 230 (grade A 230; printed 210, single 12, per_author 4, grouped 4; primary 188, additional 42); papers ok 21; multi-affiliation slots 34; present addresses 0; 19 unmapped org strings |
| `show lit_h33 --corpus lit --codes <id> --pdf`, all 21 papers (plus `--pages 7` xiang2021, `--pages 2 3` tian2025) | headers and author lists read (scratchpad only) |
| `probe.py` on a scratch copy, dry-run, 12:18:06-12:19:03 | results below; repo batch files md5 unchanged |

| probe | change | result | reading |
|---|---|---|---|
| T1 | tian2025 cover blocks replaced by P1 (University de Vigo, unit, ES, `p.2 footnote`) | 0 errors, rows 230 | F1 verifiable |
| T2 | T1 with locality Vigo | 0 errors | passes only through the org name; keep empty |
| T3 | cover blocks kept + P1 added | 0 errors, rows 234 | option b of question 1 (duplicate org rows) |
| T4 | T1 with org Universidade de Vigo | 4 errors, org not in the block | the statement prints the hybrid form |
| T5 | T1 without unit | 4 errors, first field + D361 coverage | unit required |
| T6 | cover blocks with one `p.2 footnote` locator | 2 errors, D361 coverage | page 2 is unsearched today, so the statement escapes coverage |
| N1 | wang2025a QI WANG without `slot: 0` | 1 error, 0 slots | slot 0 required |
| N2 | xie2026 SHUIYING XIANG without `slot: 0` | 1 error, 0 slots | slot 0 required |
| N3 | spencer2014 block 3 locality Aarhus | 0 errors | incidental (name inside the org); keep empty |
| N4 | xu2019 locator back to the default | 0 errors | locator unverified (h27 G3) |

## Checker gaps observed (scripts not edited)

- G1 Cover-page coverage: a footnote statement on the manuscript page after a cover is outside the searched pages when
  every block uses the default locator, so D361 coverage cannot see it (T6 shows it is enforced once page 2 is
  searched). Same family as the D521 `show` masking open item (a space-less contact run hides printed place words).
- G3 (h27) Locator vs layout still unverified (N4).

## Coordinator questions

1. tian2025: (a) record the page 2 statement only (F1 YAML; recommended: D366 cover rule, the statement is the authors'
   own affiliation with unit and country, verified by T1); (b) keep the cover blocks and add P1 (T3, 4 extra rows that
   duplicate the org per author); (c) keep the cover blocks and fix only the note (N1). lit_h07 lapointe2025 is not a
   precedent against (a): its Research Square file has no manuscript affiliation statement.
2. Lists: xie2026 #9 (shui xiang) and wang2025a #2 (Q.P. Wang) to the D412 correction file; tian2025 #1 (Yu Peng Tian)
   to the D426 review list. Recommended: yes.
3. Org round: University de Vigo / Universidade de Vigo, University at Albany CNSE, LioniX BV / LioniX International
   B.V., Morton Photonics (two places), Yongjiang Laboratory are the recurring unmapped strings of this batch.

## Verdict

GO. No slot carries a wrong person, org, city, country or marker, nothing is invented, no block is missed, and no
address or contact text is recorded. tian2025 (4 slots) should take its manuscript footnote statement, which adds the
printed unit and country (F1, question 1); everything else is correct as recorded.
