---
title: Fresh-context audit of the lit author-affiliation batch lit_h17 (35 papers)
date: 2026-10-30
auditor: Claude (fresh context; wrote only lit_h17/headers.yaml, the derived files the checker writes, and this record; aggregate not run)
scope: data/_staging/people/lit_headers/lit_h17/headers.yaml; both header contracts; DevLog-011 D350-D369, D380, D400-D416; previous audits 2026-10-29-lit-header-batches-3-audit.md, 2026-10-29-lit-header-batches-4-audit.md
verdict: GO for the people rebuild after the fixes below (applied; check 0 errors, 2 warnings); 0 wrong and 20 imprecise slots in 247 audited (3 fixed, 17 checker gaps); 1 note made by-type
---

# Lit header batch audit, round 5: lit_h17 (2026-10-30)

## Scope

Batch lit_h17 (35 papers, 247 author-list slots), extracted 2026-10-30 (extractor check: 0 errors, 2 warnings; 30 ok /
5 partial; 236 / 247 slots recorded; 264 rows). lit_h18 is audited separately and was not touched. Restricted corpus:
this record names only authors, orgs, units, cities and countries; no paper text is quoted and no contact, street,
building, postal or box code is copied.

## Method

- Every paper read with `env -u VIRTUAL_ENV uv run python scripts/ofc_headers.py show lit_h17 --corpus lit --codes
  <id>` and the same with `--pdf` (all 35); `--pages 2` for the two cover-page papers (cavalier2011, chiles2017).
- Selection: all 35 papers (full coverage):
  - (a) explicit `slot:` / `slot: 0` / `author_list_differs` / order differs: chen2000, goh2001, keyvaninia2012;
  - (b) partial: barwicz2016, foster2006, kang2008, kang2008a, keyvaninia2012; prose: barwicz2016, goh2001,
    guan2014a; grouped: chen2000, keyvaninia2012; present addresses: barwicz2016, goh2001 (recorded), chen2000,
    kuyken2011 (dropped);
  - (c) flagged items: cabezon2012 (unit / org split by an address), kang2008 / kang2008a (campus, unit dropped),
    dash-joined orgs (acoleyen2009, bogaerts2007, chen2018a, keyvaninia2012, kuyken2011), two-org blocks
    (barwicz2016 P7, cavalier2011 blocks 2 / 4, dolgaleva2011 block 3, keyvaninia2012 G2), empty localities
    (barwicz2016, goh2001), parents (chee2012, fang2008, fang2010, guan2014a, huang2013), locators (cavalier2011,
    chiles2017 p.2 header; bi2011, foster2006, kang2008a, lee2012 p.1 footnote), D412 artefacts (a2011, a2013);
  - (d) the remaining papers: acoleyen2009, almeida2003, bi2011, biberman2012, bogaerts2007, campenhout2009,
    campenhout2010, chen2018a, derose2011, feng2011, fukuda2006, giuntoni2009, hutchison2016, jones2013, lee2012,
    lindenmann2012.
- Per slot: slot-to-name assignment (D359, D369, D287, D302), printed marker run vs `markers` + `dropped_markers`
  (text and PDF view), block mapping, org / unit / more_orgs split, parent rule, campus (D301), locality (first
  printed city as printed), country (printed), role, basis, locator. Every note claim checked against the page.
- Name scan: all 247 `compare.csv` rows, list name vs printed name (folded); 62 rows differ, every one inspected.
- Claims tested with dry-run probes (`check --dry-run` on a temporarily edited `headers.yaml`, file restored
  byte-identical, md5 asserted after each probe; helper `probe.py` in the session scratchpad `lit_h17_audit/`).
- Privacy scan (`privscan.py`, same folder): every field and note of `headers.yaml`; every value of `header_rows.csv`,
  `compare.csv`, `unmapped_orgs.csv`, `papers.csv`, `check_stamp.txt` (contact / URL / ORCID patterns, 3+ digit runs
  other than paper codes and decision numbers, street / building / box / campus words and the address words printed in
  this batch's blocks); `org_requests.csv` for the cavalier2011 box text.
- Backup before any edit: `backup_lit_h17_20261030T004648.zip` (lit_h17 directory + `org_requests.csv`) in the
  session scratchpad `lit_h17_audit/`.

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h17 | 35 / 35 | 247 | 227 | 20 | 0 |

- Fixed: 3 imprecise (keyvaninia2012 #6 #7 #8, F1). Not fixable within the contract / checker: 17 imprecise
  (barwicz2016 #11 #14, cabezon2012 #1 #2, chen2000 #1, foster2006 #1 #3 #6, kang2008 #7 #8, kang2008a #9 #10 #11
  #12, keyvaninia2012 #4 #5, kuyken2011 #2; C1-C8).
- The 11 `no_header` slots: barwicz2016 #14 (C1), foster2006 #1 #3 #6 (C3), keyvaninia2012 #4 #5 (C6) are checker
  gaps; goh2001 #3 (Kyota Hattori in the list, Kuninori Hattori printed: `slot: 0`, correct), kang2008 #10 #11
  (H.-D. Liu, D. C. McIntosh printed without any marker in both layers, and no unmarked block exists), kang2008 #13
  and kang2008a #8 (A. Pauchard: his block prints only an address and a place in CH, no organization) are correct
  under the never-guess rule.
- Header-only author (`slot: 0`): goh2001 Kuninori Hattori (correct; no rows, as for other header-only authors).

## Rulings on slot overrides and known items

| paper, slot | printed vs list | ruling |
|---|---|---|
| chen2000 #7 | Shajing Sun vs Sam-Shajing Sun | keep `slot: 7` (D287 name-part variant; same group block, same position) |
| goh2001 #3 | Kuninori Hattori vs Kyota Hattori | `slot: 0` + `author_list_differs` correct (different given name, D287); probe not needed: the names are not compatible |
| kang2008 #1 | Y. Kang vs list Yunlu Kang | match correct by the rules (initial explained); probe `slot: 0` gives the D302 error. kang2008a prints Yimin Kang with the same Intel block and co-authors: the list name is very likely wrong (open question 3) |
| fang2010 #5, feng2011 #5 | Ming Bin Yu vs list Ming Yu; Wei Qian vs list Wei Ping Qian | auto-matches with a dropped syllable on one side (G3 pattern of round 2, common family names); same org and position in both; accepted, flagged (open question 7) |
| keyvaninia2012 | printed group order differs from the list (Fedeli, Messaoudene at list #4 #5) | warning correct; G-.H. Duan matched to Guang-Hua Duan (#6); unreadable #4 #5 resolve by name |
| a2011 #1, a2013 #1 | Daoxin Dai vs list artefact "Daoxin Dai A" | correct person; new D412 cases (open question 4) |
| other list-side differences | e.g. Michal F. Lipson, Robert K. Leidy, Sebastian U Engelmann, Christopher Todd Derose, James Stewart Aitchison, Mingbin Yu / Shaohua Tao (joined given names, D369), Richard M. Osgood (printed Jr.), Juerg Leuthold, Christian G. Koos | all initials agree, same positions: correct |

## Findings and fixes

| # | paper, slots | rating | evidence (locator) | fix (field: before -> after) |
|---|---|---|---|---|
| F1 | keyvaninia2012 #6 #7 #8 (Duan, Lamponi, Lelarge), block G2 | imprecise | p.1 header: III-V Lab, then a description as a joint lab of Alcatel-Lucent Bell Labs France, Thales Research and Technology and CEA Leti, Palaiseau; the contract parent rule as applied in round 3 F2 (verdier2017, same description) and pommarede2017 / brun2014, and D416 (2) (JPL / Caltech normalized to the parent rule); probe without parents: 0 errors | G2 `more_orgs: ["Alcatel-Lucent Bell Labs France", "Thales Research and Technology", "CEA Leti"]` -> removed; note rewritten. -9 rows (264 -> 255); unmapped org strings 26 -> 24 (Alcatel-Lucent Bell Labs France, Thales Research and Technology gone); `compare.csv` org ids of the 3 slots `org_cea_leti;org_iii_v_lab` -> `org_iii_v_lab` |
| N1 | a2013 (note) | privacy rule | the note named the campus printed before Hangzhou (a site name, round 3 F5) | "campus name <name>" -> "a campus name"; no field changed |
| C1 | barwicz2016 #14 (Sebastian Engelmann), P1 | imprecise, not fixable (no row) | p.1 footnote: statement 1 prints his family name hyphenated across a line break; probe readable: "not named in the statement subject" (md, pdf) | none (gap G1); `unreadable` kept, statement kept for the other carriers |
| C2 | barwicz2016 #11 (Robert Leidy), present address | imprecise, not fixable | p.1 footnote: "was with" statement (IBM Microelectronics Division, US; recorded P8), then a pronoun present-address statement (Global Foundries, Essex Junction, US) after a comma, not a sentence end; probe P9 `present_address`: fields verify, "not named in the statement subject" (md, pdf) | none (gap G2; family of the known "was with A and is now with B" gap) |
| C3 | foster2006 #1 #3 #6 (Foster, Sharping, Gaeta), block 1 | imprecise, not fixable (no rows) | p.1 footnote: block 1 prints only the School of Applied and Engineering Physics, block 2 the School of Electrical and Computer Engineering, then Cornell University, Ithaca, US once for both; probe block 1 with org Cornell University: "unit and org are not one contiguous printed segment" and block 2 no longer found (md, pdf) | none (gap G3) |
| C4 | chen2000 #1 (Antao Chen), present address | imprecise, not fixable | p.1 footnote: asterisk on the name points to a present-address footnote (Lucent Technologies, Optoelectronics Center, Breinigsville; no country); probe block `*` `present_address`: "printed markers differ" (symbol not in the marker run) and "marker + first field not printed" | none (gap G4); asterisk ignored as a symbol mark |
| C5 | kang2008 #7 #8 (Kuo, Bowers), kang2008a #9 #10 #11 #12 (Kuo, Chen, Sfar Zaoui, Bowers) | imprecise, not fixable (unit lost) | p.1 header / footnote: University of California Santa Barbara (no comma), then the ECE Department, then Santa Barbara; org + `campus: "Santa Barbara"` recorded; probe adding the unit: "marker + first field not printed" (md, pdf) | none (round 3 G1, fang2006) |
| C6 | keyvaninia2012 #4 #5 (Fedeli, Messaoudene), block G3 | imprecise, not fixable (no rows) | p.1 header: group 3 prints CEA-LETI, Grenoble, FR; probe G3 recorded: "author not printed before this block" and "locality not inside this printed block" (md, pdf): the block anchor finds CEA Leti inside the G2 description first | none (gap G5); `unreadable` kept |
| C7 | kuyken2011 #2 (Xiaoping Liu), present address | imprecise, known | p.1 header: block 4 printed with the cue Current address (OFS Labs, Somerset, US); probe `present_address`: "marker + first field not printed" (md, pdf) | none (known gap: ji2017, koyaz2026, beeck2021); marker kept in `dropped_markers` |
| C8 | cabezon2012 #1 #2 (Cabezón, Garcés), block 1 | imprecise, not fixable | p.1 header: Photonics Technology Group at I3A, then a building name and street address, then Universidad de Zaragoza, Zaragoza, ES; recorded as org + `more_orgs` (lit_h01 COPL / Université Laval precedent); probe unit + org: "unit and org are not one contiguous printed segment" (md, pdf) | none (gap G6); open question 2 |

Checked and correct (highlights):
- Prose: barwicz2016 statements P1-P8 (subjects vs carriers both ways; "was with" P2 / P8; pronoun present address
  P3 Keio University; P2 / P6 two statements naming IBM Research—Tokyo are two blocks); goh2001 P1-P3 ("was with" P2,
  pronoun present address P3 NTT Network Innovation Laboratories); guan2014a P1-P5 (clause block P5 for Hochberg;
  Agency for Science, Technology and Research parent not copied).
- Grouped: chen2000 (two University of Southern California groups, units Department of Electrical
  Engineering-Electrophysics and Department of Chemistry; no country printed: ""), keyvaninia2012 G1 / G2 / G4.
- Empty fields: barwicz2016 P2 / P3 / P6 / P7 print a ward and the country, P8 a state and the country; goh2001 P1-P3
  print a prefecture and the country (`locality: ""`); almeida2003, campenhout2009, chen2000 print a state and no
  country (`country: ""`).
- Parents not copied: A*STAR in chee2012, fang2008, fang2010, huang2013; Agency for Science, Technology and Research in
  guan2014a.
- Campus: a2011 (comma form) and kang2008 / kang2008a (no comma) record University of California + `campus: "Santa
  Barbara"`; a2013's campus name is part of the address (not a distinct institution).
- Two-org blocks: barwicz2016 P7 Asahi Glass Co. + AGC Electronics (open question 6); cavalier2011 block 2 CEA + joint
  research unit UMR INAC-UJF (`more_orgs`, contract UMR rule); cavalier2011 block 4 records IMEP-LAHC only (its UMR
  designation names the lab itself with its parents; number not copied); dolgaleva2011 block 3 INESC-Porto + structured
  `more_orgs` Universidade do Porto with unit Departamento de Física e Astronomia (D367).
- Dash-joined orgs kept as printed (D416 (5)): acoleyen2009, bogaerts2007, chen2018a (two dash forms), keyvaninia2012
  G1, kuyken2011. The hyphen and spaced-dash forms already map to `org_ghent_university;org_imec` by alias; the em-dash
  form (kuyken2011) and the long Interuniversity MicroElectronics Center form (acoleyen2009) are unmapped (alias
  requests; open question 5).
- Locators: cavalier2011 and chiles2017 `p.2 header` (page 1 is a publisher cover page, author line and blocks on
  page 2); bi2011, foster2006, kang2008a, lee2012 `p.1 footnote` (blocks at the foot of page 1); barwicz2016, goh2001,
  guan2014a statements `p.1 footnote`.
- Markers: every readable author's printed run matches `markers` + `dropped_markers` in both layers; contact
  footnotes cavalier2011 a, chiles2017 a, chen2018a 5; equal contribution chen2018a 4; symbol marks (asterisk, dagger)
  never used by a block.
- As printed: barwicz2016 Ducan; fukuda2006 Atsugi-Shi; chen2018a Gent-Zwijnaarde; cavalier2011 St Martin d'Hères
  (detached accents in the extraction); derose2011 Sandia National Laboratory (singular), district before Cardiff only
  in the note, by type; giuntoni2009 Fraunhofer Institut für Nachrichtentechnik, Heinrich-Hertz-Institut as one org
  (pilot billah2018); campenhout2010 IBM Research + unit T. J. Watson Research Center (printed order); kang2008 Intel
  Electronics Ltd vs kang2008a Numonyx (Qiryat-Gat, IL; both as printed).

Consistency observations (no fix, other batches): lit_h02 keyvaninia2013 prints the same III-V Lab description and
still records the three parents (open question 1); lit_h01 and lit_h10 notes name the same campus as a2013 (open
question 8); the kang2008 / kang2008a author lists name M. Morse differently (Michael T. Morse vs Mike M. Morse), a
person-merge item.

## Privacy and as-printed scan

- No contact address, URL, ORCID id, phone number, street name, building name, postal code or box code in any field
  or note of `headers.yaml` after N1, nor in `header_rows.csv` (255 rows), `compare.csv` (247), `unmapped_orgs.csv`
  (24) or `papers.csv`: 3+ digit runs occur only in paper codes, decision numbers and the stamp hash. Notes name
  address parts only by type (street address, building name, postal box, district, ward, prefecture, state, campus
  name). No `skip_prefix` / `skip_between` span in the batch.
- cavalier2011 block 4: the postal-box designation and code and the UMR number are stored nowhere (no match in any
  lit_h17 file or in `org_requests.csv`); the note names them by type only.
- This record: same scan.

## Commands (2026-10-30, log times)

| Command | Result |
|---|---|
| `check lit_h17 --corpus lit --dry-run` (before) 00:46:48 (log `lit_headers_check_lit_h17_68181_20261030T004648.log`) | 0 errors, 2 warnings (chen2000 slot 7, keyvaninia2012 order); slots 247, recorded 236, no_header 11, rows 264, present addresses 1, 26 unmapped org strings |
| probes (`--dry-run`) 00:49:59 (73225), 00:50:06 (73264), 00:50:57 (74723), 00:51:59 (75724), 00:53:12 (77813), 00:54:06 (79307), 00:54:13 (79527), 00:55:08 (80809), 00:55:15 (80976), 00:55:59 (81999) | barwicz2016 Engelmann readable: 2 errors; barwicz2016 Leidy present address: 2 errors; cabezon2012 unit + org: 2 errors; chen2000 asterisk present address: 3 errors; foster2006 block 1: 4 errors; kang2008 unit: 2 errors; kang2008 `slot: 0`: 1 error (D302); keyvaninia2012 without parents: 0 errors, rows 255, unmapped 24; keyvaninia2012 G3: 7 errors; kuyken2011 Current address: 2 errors. File restored and md5-verified after each |
| `check lit_h17 --corpus lit` 00:57:14 (log `lit_headers_check_lit_h17_83498_20261030T005714.log`) | 0 errors, 2 warnings; ok 30, partial 5, unreadable 0; rows 255 (grade A 255), recorded 236, no_header 11, present addresses 1; 24 unmapped org strings; stamp matches headers.yaml (sha256 402cf512...) |

Changes to `headers.yaml` (diff against the backup): keyvaninia2012 G2 `more_orgs` removed and note rewritten; a2013
note; nothing else. `header_rows.csv` loses the 9 keyvaninia2012 parent rows; `compare.csv` changes only in the
org ids of keyvaninia2012 #6 #7 #8; `unmapped_orgs.csv` loses 2 strings. `aggregate` not run (coordinator).

## Checker gaps observed (scripts not edited)

- G1 A subject name hyphenated across a line break in a prose statement is not matched (barwicz2016 Engelmann); same
  family as the hyphenated country across a line break (ozdemir2021).
- G2 A pronoun present-address statement printed after a comma (no sentence end) following a "was with" statement is
  not attached to its subject (barwicz2016 Leidy); family of the "was with A and is now with B" gap.
- G3 Shared organization suffix: an org and place printed once after the last of several unit-only blocks (inverse of
  D283 `org_from_prefix`) cannot be attached to the earlier blocks (foster2006: 3 slots).
- G4 A symbol mark (asterisk) that points to a present-address footnote cannot carry a block: the symbol is not part
  of the checked marker run and the cue between marker and first field is not skipped (chen2000).
- G5 A grouped block whose org name also occurs inside an earlier block's text is anchored at that earlier occurrence
  (keyvaninia2012 CEA-LETI inside the III-V Lab description: 2 slots).
- G6 A building name / street address printed between a unit and its org has no verified skip span (D410
  `skip_between` covers postal boxes only), so the unit cannot be recorded (cabezon2012; lit_h01 COPL is the same
  layout).
- Known: "Current address:" cue (kuyken2011); unit printed after "org campus" (kang2008, kang2008a; round 3 G1).

## Open questions

1. keyvaninia2012 III-V Lab parents dropped (F1, parent rule): confirm, and normalize lit_h02 keyvaninia2013 (same
   description, parents recorded) in the D412 / checker follow-up pass like ledezma2022 (D416 (2))? Recommended: yes.
2. cabezon2012 block 1: keep org "Photonics Technology Group at I3A" + `more_orgs` Universidad de Zaragoza (COPL
   precedent, 2 rows kept) or leave it unrecorded? Recommended: keep; re-record as unit + org once G6 exists.
3. kang2008 #1 list name Yunlu Kang for printed Y. Kang (kang2008a prints Yimin Kang, same block and co-authors): add
   to the D412 author-list correction file? Recommended: yes.
4. a2011 #1 and a2013 #1 "Daoxin Dai A": add to the D412 list (with wang2014, bauters2013, zhang2025b)? Recommended:
   yes.
5. Dash-joined Ghent University / imec forms: keep as printed (hyphen and spaced forms already map to both orgs) and
   add aliases for the em-dash and the Interuniversity MicroElectronics Center forms in the org round; leave the older
   two-org splits (lit_h01, lit_h05, lit_h09) as they are (same org ids)? Recommended: yes.
6. barwicz2016 P7 Asahi Glass Co. + AGC Electronics as two orgs vs AGC Electronics as unit? Recommended: keep two
   orgs (as printed; the org round maps both to the same group).
7. fang2010 #5 (Ming Bin Yu / Ming Yu) and feng2011 #5 (Wei Qian / Wei Ping Qian) auto-matches with a dropped
   syllable: accept? Recommended: accept (same org and position), keep in the G3-pattern review list.
8. lit_h01 and lit_h10 notes name the same campus as a2013: make them by-type in the follow-up pass? Recommended: yes.
9. Re-record after checker fixes: barwicz2016 #11 #14 (G1, G2), foster2006 block 1 (G3), chen2000 #1 (G4),
   keyvaninia2012 G3 (G5), cabezon2012 (G6), kuyken2011 #2 (Current address), kang2008 / kang2008a units.
