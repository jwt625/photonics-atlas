---
title: Fresh-context audit of the lit author-affiliation batch lit_h29 (21 papers)
date: 2026-11-08
auditor: Claude (fresh context; wrote only this record; headers.yaml, derived files, scripts, tests, people and registry data not edited; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h29/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369, D400-D522; format and precedent from the 2026-11-06 h27 audit
verdict: GO for the people rebuild (no slot wrong); 165 slots audited, 153 ok, 12 imprecise, 0 wrong; F1 (5 slots, LETI recorded as its own org) and F2 (1 slot, missed present address on page 6) fixable now (probe 0 errors); C1 (gatkine2022, 5 slots) and C2 (hausmann2014 #4) wait on checker gaps; nothing applied
---

# Lit header batch audit: lit_h29 (2026-11-08)

## Scope

Batch lit_h29 (21 papers: 1 IEEE footnote-prose paper, 2 cover-page papers (ACS accepted manuscript, AIP), 2 first-page
footnote papers (Laser Photonics Rev., Nature Photonics), 1 SPIE paper, 15 Optica / arXiv / other header papers; 165
author-list slots; 218 rows). Restricted corpus: this record names only authors, orgs, units, cities and countries; no
paper text is quoted and no contact, street, building, site or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h29 --corpus lit --codes <id> --pdf`
  (du2018 and gehring2019 also `--pages 2`, their cover-page layout); output kept in the session scratchpad only. Both
  text layers carry every author marker legibly except gatkine2022 (letter markers glued in the text layer).
- Per slot: printed name vs `compare.csv` slot, printed marker run vs `markers` + `dropped_markers`, prose subject vs
  carriers (fahrenkopf2019), block fields vs the print (org, unit, city, country, role), locator. All 83 distinct
  (paper, org, unit, place, role, org id, locator) tuples of `header_rows.csv` read; no wrong mapping.
- Marker targets checked against the footnote lines (contact / equal contribution / corresponding / present address);
  han2024 marker 3 confirmed as a contact line by a pattern count on `text.md` (no contact printed).
- Missed blocks: cue scan of the whole `text.md` of all 21 (now with / at, present / current address or affiliation,
  currently with / at, also with / at, is / are / was / were with, affiliated with, on leave, visiting, formerly,
  deceased, permanent address, and every line starting with a symbol mark). Header hits: frandsen2014, gehring2019,
  hausmann2014 (recorded or parked), fahrenkopf2019 (statements recorded; the was-with hit on a later page is a
  biography). One missed block: dutt2018 (F2).
- Claims and parked papers tested with dry-run probes on a scratch copy of the batch (`probe.py` in the session
  scratchpad: copies `papers.csv` + `headers.yaml`, applies exact text replacements, sets the module's `LIT_BASE` to the
  copy, runs `cmd_check(["lit_h29"], dry_run=True, corpus="lit")`). md5 of every repo batch file identical before and
  after the audit.
- Precedent: committed lit blocks for Université Grenoble Alpes + CEA + LETI, IME Singapore, Hokkaido / RIKEN, INL,
  "Key Laboratory ..., Chinese Academy of Sciences", leading articles in prose blocks.
- Stamp: `check_stamp.txt` matches `headers.yaml` (sha256 45efc711...). `headers.yaml` mtime 12:05:21, stamp and
  derived files 12:05:26.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h29 | 21 / 21 | 165 | 153 | 12 | 0 |

- Rows 218 (all grade A: printed 189, prose 6, single 23; primary 172, additional 43, present address 3); recorded 159,
  no_header 6 (gatkine2022 5, hausmann2014 #4); papers ok 19, partial 1 (hausmann2014), unreadable 1 (gatkine2022);
  `author_list_differs` 0; `slots_from_header` 0; explicit slots 1 (halir2016 #6, warning); 22 unmapped org strings;
  `order_differs` false on all 165.
- Imprecise by cause: fixable now 6 (F1 ferrotti2016 #1 #2 #3 #4 #8; F2 dutt2018 #4); checker gap 6 (C1 gatkine2022
  #1-#5; C2 hausmann2014 #4). The 12 slots are distinct.
- Per paper (slots / rows): du2018 13 / 14; dutt2018 8 / 11; eznaveh2018 11 / 12; fahrenkopf2019 6 / 6; fan2025a 6 / 9;
  ferrotti2016 8 / 30; frandsen2014 7 / 8; fu2026 8 / 8; garciarodriguez2017 4 / 4; gatkine2022 5 / 0; gehring2019
  7 / 10; gu2015 8 / 12; guan2014 9 / 14; guan2017 13 / 14; guo2023 11 / 14; guo2025 7 / 14; guzman2017 4 / 4; halir2016
  10 / 13; han2024 8 / 9; hatai2024 7 / 7; hausmann2014 5 / 5.

## Per-paper findings

| paper | slots ok / imprecise / wrong | finding |
|---|---|---|
| du2018 | 13 / 0 / 0 | cover page; author line and 4 blocks on page 2, `p.2 header` correct; block 1 prints MA but no country (`country: ""`, D249); dagger equal contribution, asterisk corresponding (symbols, ignored) |
| dutt2018 | 7 / 1 / 0 | F2: the asterisk on author 4 (Jaime Cardenas) is not a contact mark; it points to a present address (The Institute of Optics, University of Rochester, Rochester, US) printed with the end-of-paper notes on page 6. Note says both symbols mark contact lines; only the dagger does |
| eznaveh2018 | 11 / 0 / 0 | block 3 NEC Laboratories America, Inc., Princeton; block 4 no city (Southampton only inside the org name), `locality: ""`; blocks 6 / 7 state code only, `locality: ""`; block 5 Nokia org + Bell Labs unit (lit_h06, D521 precedent) |
| fahrenkopf2019 | 6 / 0 / 0 | two prose statements, carriers match the subjects (4 + 2 authors); the grammatical article before Analog Photonics not copied: consistent with all 542 committed prose blocks (none starts a unit or org with an article that the statement grammar supplies) |
| fan2025a | 6 / 0 / 0 | three blocks as printed; block 2 unit chain (two labs + college) contiguous |
| ferrotti2016 | 3 / 5 / 0 | F1: block 1 prints Université Grenoble Alpes, CEA, LETI; recorded with CEA and LETI as two plain `more_orgs`, giving 5 rows with an org named LETI (unmapped). All 11 committed lit blocks of this printed pattern record CEA with unit LETI as a structured `more_orgs` entry (lit_h07, h09, h10, h13, h14, h21). Block 3 (Université de Lyon + Ecole Centrale de Lyon + CNRS + INL) matches lit_h27 perez2017 |
| frandsen2014 | 7 / 0 / 0 | block 3 Now-at present address (Topsoe Fuel Cell, Lyngby) on author 2, correct |
| fu2026 | 8 / 0 / 0 | single unmarked block; JLU Region kept in the unit chain as printed |
| garciarodriguez2017 | 4 / 0 / 0 | single block, Valencia, ES |
| gatkine2022 | 0 / 5 / 0 | C1: unreadable is required. Probe G1 (blocks a / b `printed`, authors carrying a / b): 9 errors (author names glued to markers in the text layer; block marker glued to the first word in both layers). Probe G2 (`pdf` basis): 11 errors. Same gap as D416 (1) / D521 (jung2025). The note lists the two blocks (Caltech division, JPL; both Pasadena, US) and carriers correctly |
| gehring2019 | 7 / 0 / 0 | cover page, `p.2 header`; marker a equal contribution and c contact correctly in `dropped_markers`; b Now-at present address (Nanoscribe GmbH, Eggenstein-Leopoldshafen) on author 2; block 3 Humboldt-Universität zu Berlin printed before its institute / working group, recorded as org + unit |
| gu2015 | 8 / 0 / 0 | Saitama and Hokkaido printed with prefecture-level postal codes only, `locality: ""` (D288) |
| guan2014 | 9 / 0 / 0 | IME without the A*STAR parent, Singapore / SG (19 committed IME blocks identical) |
| guan2017 | 13 / 0 / 0 | marker 3 equal contribution dropped on authors 1-2 |
| guo2023 | 11 / 0 / 0 | block 2 prints NY only, `locality: ""`; dagger is the contact line |
| guo2025 | 7 / 0 / 0 | block 1 prints the key laboratory with the Chinese Academy of Sciences and no institute; org CAS + unit accepted (question 1) |
| guzman2017 | 4 / 0 / 0 | printed order of markers 1, 3, 2, 1 against blocks 1-3 recorded correctly; block 3 period-separated chain contiguous |
| halir2016 | 10 / 0 / 0 | first-page footnote, `p.1 footnote` on all blocks; #6 printed Gonzalo Wangüemert-Pérez, list Juan Gonzalo Wangüemert-Pérez: dropped first given name of a distinctive family name, explicit `slot: 6` (D287 / D369) correct |
| han2024 | 8 / 0 / 0 | marker 3 on author 1 is a contact line (`dropped_markers` correct); IME of the CAS as one printed org name |
| hatai2024 | 7 / 0 / 0 | single block, Sagamihara; ward and prefecture not recorded |
| hausmann2014 | 4 / 1 / 0 | C2: one dagger line prints two present-address places, each followed by author initials (Schlumberger-Doll Research Center for I. Bulu, recorded; MIT Research Laboratory of Electronics for P. Deotare). Probes H1-H4: no recordable form for author 4 (markers [] -> D286d; dropped dagger -> "drops a recorded block"; a second dagger block -> "defined twice"; dagger on author 4 with status ok passes (H3b) but would give him Schlumberger, wrong). `unreadable` is the only correct choice; Harvard primary row and MIT present address missing for #4 |

## Findings and proposed fixes (not applied)

| # | paper, slots | rating | evidence (locator) | proposed fix |
|---|---|---|---|---|
| F1 | ferrotti2016 #1 (Thomas Ferrotti), #2 (Benjamin Blampey), #3 (Christophe Jany), #4 (Hélène Duprez), #8 (Badhise Ben Bakir), block 1 | imprecise, fixable now (LETI recorded as an org; nothing invented) | p.1 header: Université Grenoble Alpes, CEA, LETI, then campus / site, Grenoble, France. Committed precedent (11 blocks, lit_h07 / h09 / h10 / h13 / h14 / h21): structured `{org: "CEA", unit: "LETI", ...}`. Probe F1: 0 errors, rows 218 -> 213, unmapped strings 22 -> 21 | see YAML F1 below |
| F2 | dutt2018 #4 (Jaime Cardenas) | imprecise, fixable now (present-address row missing; note wrong about the asterisk) | p.6 (end-of-paper notes, both layers): asterisk line with the Currently-at cue: The Institute of Optics, University of Rochester, Rochester, New York, USA. The checker's cue list includes currently at. Probe D1 (U+2217 marker as printed): 0 errors, rows +1, present addresses 3 -> 4; with an ASCII asterisk: 4 errors (marker not printed); probe D2 (role affiliation): 2 errors (cue present), so the role is verified | see YAML F2 below |
| C1 | gatkine2022 #1-#5 | imprecise, not fixable now (no rows; nothing wrong) | p.1 header: author letter markers glued to the names in the text layer, block letters glued to the first word in both layers. Probes G1 / G2: 9 / 11 errors | none now; re-record after the glued-letter-marker fix (D416 (1)) with the blocks listed in the paper note: a Caltech + Division of Physics, Mathematics and Astronomy, Pasadena, US (authors 1, 2, 5); b Jet Propulsion Laboratory, Pasadena, US (authors 3, 4, 5) |
| C2 | hausmann2014 #4 (P. Deotare) | imprecise, not fixable under the contract (no rows; nothing wrong) | p.1 footnote: one dagger, two places separated by author initials. Probes H1-H4 | none now; needs a checker / contract device for one symbol pointing to per-author places (initials after each place). Then author 4: Harvard single block + `{role: present_address, org: "Massachusetts Institute of Technology", unit: "Research Laboratory of Electronics", locality: "Cambridge", country: "US"}` |

### F1 exact YAML edit (ferrotti2016)

```yaml
# block 1, before
    - {marker: "1", basis: printed, org: "Université Grenoble Alpes", more_orgs: ["CEA", "LETI"], locality: "Grenoble", country: "FR"}
# after
    - {marker: "1", basis: printed, org: "Université Grenoble Alpes", more_orgs: [{org: "CEA", unit: "LETI", locality: "Grenoble", country: "FR"}], locality: "Grenoble", country: "FR"}
# note: replace
#   "(recorded as three organizations; campus and site not recorded)"
# with
#   "(recorded as Université Grenoble Alpes with CEA and its unit LETI as a further organization, as lit_h07 / h13 / h14 / h21; campus and site not recorded)"
```

### F2 exact YAML edit (dutt2018)

```yaml
# note, before
  note: "arXiv preprint; asterisk and dagger mark contact lines; postal codes not recorded"
# after
  note: "arXiv preprint; the asterisk on author 4 points to a present address (Currently at) printed with the end-of-paper notes on page 6 (locator p.6 affiliations); dagger marks the contact line; postal codes not recorded"
# affiliations: insert after block 4
    - {marker: "∗", basis: printed, role: present_address, org: "University of Rochester", unit: "The Institute of Optics", locality: "Rochester", country: "US", locator: "p.6 affiliations"}
# authors, before
    - {name: "Jaime Cardenas", markers: ["2"]}
# after
    - {name: "Jaime Cardenas", markers: ["2", "∗"]}
```

The marker is U+2217 (asterisk operator) as printed in both layers, not an ASCII asterisk. Probe ALL (F1 + F2 together,
notes included): 0 errors / 1 warning (halir2016 explicit slot); rows 218 -> 214 (printed 185, prose 6, single 23;
primary 167, additional 43, present address 4); unmapped strings 21. Any change to the YAML changes its hash: re-run
`check lit_h29 --corpus lit` afterwards to refresh the stamp and derived files.

## Probes (dry-run, scratch copy; repo batch files md5 unchanged)

| probe | change | result | reading |
|---|---|---|---|
| P0 | none | 0 errors, rows 218 | baseline equals the repo dry-run |
| F1 | ferrotti2016 block 1 structured CEA / LETI | 0 errors, rows 213 | F1 |
| D1 | dutt2018 U+2217 present-address block on author 4 | 0 errors, rows 219 | F2 |
| D1 (ASCII) | same with an ASCII asterisk | 4 errors, marker not printed | marker must be U+2217 |
| D2 | D1 with role affiliation | 2 errors, cue present | role verified |
| ALL | F1 + F2 + both notes | 0 errors, rows 214 | apply set |
| G1 / G2 | gatkine2022 blocks recorded, basis printed / pdf | 9 / 11 errors | C1 confirmed |
| H1 | hausmann2014 author 4 markers [] | 3 errors (D249 partial, D286d both layers) | unreadable required |
| H2 | author 4 drops the dagger | 2 errors (drops a recorded block) | same |
| H3 / H3b | author 4 carries the dagger (status partial / ok) | 1 error (partial without unreadable) / 0 errors, but the passing form attaches Schlumberger to Deotare, which is wrong (the checker cannot see the per-author initials) | same |
| H4 | second dagger block (MIT) | 3 errors (marker defined twice) | C2 confirmed |

## Points checked and correct

- Cover pages: du2018 (ACS accepted-manuscript cover) and gehring2019 (AIP cover) carry `p.2 header` on every block;
  the author line on page 1 is unmarked in both, the marked line on page 2.
- First-page footnotes: halir2016, hausmann2014 and the fahrenkopf2019 prose blocks carry `p.1 footnote`.
- Countries left empty where only a US state code is printed: du2018 block 1. Localities left empty where only a state
  / prefecture is printed or the place is only inside the org name: eznaveh2018 blocks 4, 6, 7; gu2015 blocks 3, 5;
  guo2023 block 2.
- Dropped markers: gehring2019 a (equal contribution, authors 1-2) and c (contact, author 7); guan2017 3 (equal
  contribution, authors 1-2); han2024 3 (contact, author 1). Symbol marks that no block uses need no entry (du2018,
  guo2023, hausmann2014 double dagger, and the rest).
- Name forms: all 159 recorded slots match by name; capitals and initials only (eznaveh2018, ferrotti2016, fu2026,
  guan2017, guo2025, guzman2017, han2024, gehring2019, hausmann2014); halir2016 #6 explicit slot (above).
- Parents not copied: guan2014 A*STAR after IME.

## Privacy and as-printed scan

- Pattern scan over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv`, `papers.csv` and
  `check_stamp.txt`: contact / URL patterns, digit runs of 4 or more, phone-style postal codes, street words and the
  street / campus / site / park / district names printed on the header pages of this batch: 0 hits. Notes name campus,
  site, park and district only by type.
- As printed (kept, correct): du2018 unit with its leading article The College of Optics & Photonics (D288); eznaveh2018
  Southampton University and Optoelectronics Research Center (printed forms; unmapped, org round); ferrotti2016
  Institut des Nanotechnologies de Lyon-INL; hausmann2014 Schlumberger – Doll Research Center with its spaced dash.
- No `skip_prefix` or `skip_between` in this batch.

## Commands (2026-11-08, log times)

| Command | Result |
|---|---|
| `check lit_h29 --corpus lit --dry-run` 12:06:37 (pid 15471) | 0 errors, 1 warning (halir2016 explicit slot); slots 165, recorded 159, no_header 6; rows 218 (grade A 218; primary 172, additional 43; printed 189, prose 6, single 23); papers ok 19, partial 1, unreadable 1; multi-affiliation slots 35; present addresses 3; 22 unmapped org strings |
| `show lit_h29 --corpus lit --codes <id> --pdf` (all 21; du2018 / gehring2019 with `--pages 2`), 12:07-12:08 | headers and author lists read (scratchpad only) |
| `probe.py` P0 ... ALL, H3b, 12:09-12:15 | table above; each run writes its own dry-run log under `logs/` as the checker always does |

## Open questions (coordinator)

1. guo2025 block 1 (Key Laboratory of Optoelectronic Materials and Devices printed with the Chinese Academy of Sciences,
   no institute): org CAS + key laboratory as unit, or one org string as in the D522 yu2023a / lit_h19 guo2024 ministry
   cases? Recommended: keep as recorded. CAS is a research organization that employs the authors (the ministry cases
   recorded one string so as not to attribute authors to a ministry); the row maps to `org_chinese_academy_of_sciences`;
   inferring the host institute (Institute of Semiconductors) is not allowed. No committed precedent for this exact
   pattern; the org round can add an alias if the corpus later records the lab as an org.
2. Apply F1 and F2 now, then re-run `check lit_h29 --corpus lit`? Recommended: yes, before `aggregate`.
3. Lists: gatkine2022 (5 slots) to the re-record list after the glued-letter-marker fix (with jung2025, chang2026a);
   hausmann2014 #4 to the checker-gap list as a new case (one symbol, per-author places marked by initials).

## Verdict

GO. No slot carries a wrong person, org, city, country or marker, nothing is invented, and no address or contact text
is recorded. One present-address block was missed (dutt2018, page 6; F2) and one block splits CEA-LETI into two orgs
against all committed precedent (ferrotti2016; F1); both fixes pass the checker. Six slots stay without rows until the
two known checker gaps are closed (C1, C2), and the extractor's parking of them is the only correct choice today.
