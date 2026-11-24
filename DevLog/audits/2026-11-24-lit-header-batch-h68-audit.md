---
title: Fresh-context audit of the lit author-affiliation batch lit_h68 (18 papers)
date: 2026-11-24
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; checker run only in dry-run or write-run on scratch copies with logs in the scratchpad; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h68/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D352, D354, D361, D366, D368, D412 and later lit rulings (D449 / D461 UCSB campus, D699 misprints as printed); D287, D288, D301 from DevLog-008; format from the lit_h66 audit
verdict: GO; 117 slots audited, 117 recorded, 0 wrong rows, 0 imprecise rows; all named extractor calls confirmed; F1 removes a redundant explicit slot (wang2025d #2) and rewords its note (no row change)
---

# Lit header batch audit: lit_h68 (2026-11-24)

## Scope

Batch lit_h68: 18 papers (IEEE JLT / PTL / JSTQE / Photonics Journal prose footnotes, Optics Express printed
markers, IEEE / OSA conference headers with single or grouped blocks); 117 slots, 6 papers `slots_from_header`;
135 rows. Restricted corpus: this record names only authors, orgs, units, cities and countries; no paper text is
quoted and no contact, street, building, site or postal text is copied (such spans are named by type only).

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h68 --corpus lit --codes <id> --pdf`
  (all 18; watanabe2019 also with `--pages 1 2 3`); output kept in the session scratchpad `h68_audit/show/` only.
- Per slot: printed name vs the `show` author list (or the header order for the 6 header-slot papers) and
  `compare.csv`; marker run in both layers; prose statement subjects and every "and also with" clause; block fields
  (org, unit chain, more_orgs, campus, city, country); locator; notes.
- All 135 rows of `header_rows.csv` read by paper (roles primary 117, additional 18, present address 0; basis prose
  93, single 19, printed 18, grouped 5; all grade A; locators p.1 footnote 93, p.1 header 39, p.2 header 3).
  `compare.csv`: 117 `recorded`, 0 `no_header`; `order_differs` false on all 117.
- IEEE download stamp: present on the conference pages (e.g. sun2013b); no block in the batch is taken from it.
- Address / contact scan of `headers.yaml` and every derived file (contact sign, URL, 3-digit and 5-6-digit numbers,
  number-letter-comma tokens, street, road, rue, avenue, drive, suite, building, Bldg, room, box, campus, cedex,
  e-mail / mail, phone, the street and site tokens printed in this batch's blocks, the prefixed postal codes printed in
  riemensberger2012 and sapra2019). Hits: "DevLog-011" in the file comment, type words in notes ("street address",
  "postal code(s)", "site address", "campus Santa Barbara" in the spencer2012 note) and the D301 campus field value
  Santa Barbara. No contact, URL, postal code, street, building, box or site text anywhere, notes included.
- Probes on scratch copies (`h68_audit/probes/probe.py` + `mk.py`, scratch `LIT_BASE`, batch name `lit_p68`,
  `cmd_check(..., dry_run=True)`, `RunLog` redirected to the scratchpad: no log written under `logs/`; 37 runs). Dry
  run of the batch as written: 0 errors, 0 warnings; totals equal the stamped derived files (117 slots, 117
  recorded, 135 rows, 7 unmapped org strings). md5 of every repo batch file identical before and after the audit;
  `check_stamp.txt` matches `headers.yaml` (sha256 936c1928...).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h68 | 18 / 18 | 117 | 117 | 0 | 0 |

- Papers ok 18, partial 0, unreadable 0; `slots_from_header` 6 (sun2013b, spencer2012, subramanian2012a, ura2017,
  nambiar2017, shi2014; exactly the papers.csv rows with `n_authors_meta` 0, each prints the D352 line in `show`);
  `author_list_differs` 0; explicit slots 1 (wang2025d #2, redundant: F1); order warnings 0; present addresses 0;
  dropped markers 0; unreadable authors 0; 7 unmapped org strings.
- Per paper (slots / rows): sun2013b 4 / 4; riemensberger2012 6 / 9; pan2020 6 / 12; yang2025a 12 / 12;
  spencer2012 5 / 5; tokushima2016 3 / 3; zhao2015 8 / 8; subramanian2012a 6 / 6; xu2017d 8 / 9; watanabe2019 3 / 3;
  ura2017 5 / 5; wang2025d 8 / 9; xu2017c 3 / 3; nambiar2017 4 / 4; buf2015 14 / 14; sapra2019 7 / 8; shi2014 8 / 14;
  fang2016 7 / 7.
- Privacy findings: 0. Notes: 1 with a detail that F1 changes (wang2025d).

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (117) | 116 | 1 (wang2025d #2 redundant explicit slot; F1, same slot) | 0 |
| markers (printed / prose / single / grouped, 117) | 117 | 0 | 0 |
| header position / statement subject | 117 | 0 | 0 |
| blocks (org / unit / more_orgs / campus / locality / country) (117 recorded) | 117 | 0 | 0 |
| locators | all | 0 | 0 |
| notes (18) | 17 | 1 (wang2025d; F1) | 0 |

## Per-paper findings

- sun2013b (4; single, slots from header): Massachusetts Institute of Technology, unit Research Laboratory of
  Electronics (printed before the org), Cambridge, US (state and postal code not recorded). Header order = YAML
  order; probe SN1 (first two authors swapped): 2 errors. ok.
- riemensberger2012 (6; printed, Optics Express): block 1 École Polytechnique Fédérale de Lausanne (EPFL), Lausanne,
  CH (prefixed postal code not recorded); block 2 Menlo Systems GmbH, Martinsried, DE (street not recorded); block 3
  Max-Planck-Institut für Quantenoptik, Garching, DE. Marker runs match both layers; the asterisk points to the
  contact line (symbol, no entry). Kippenberg printed Tobias J., list Tobias Jan: matched by name, no slot
  (compare.csv slot 6); probe R1 (YAML name Tobias Jan): 2 errors (not printed). ok.
- pan2020 (6; prose): "The Authors" statement, Zhejiang University with the two key laboratories + research center
  + college as unit chain, Hangzhou, CN; "and also with" clause Zhejiang University, unit Ningbo Research Institute,
  Ningbo, CN (committed lit_h66 yu2023b form). Every author carries P1, P2. List form "Daoxin Dai A" (D412) matched
  to printed Daoxin Dai (slot 6). Membership designation after Dai in both layers. Call 4. ok.
- yang2025a (12; prose): five statements; P1 / P4 the same Suzhou institute (two statements, two blocks, D354),
  unit Nanofabrication Facility; P2 Ningbo University with laboratory + research institute chain, Ningbo, CN (6
  carriers including the last author); P3 ShanghaiTech University, School of Information Science and Technology,
  Shanghai, CN (statement extracted one word per line in both layers; subject still verified: probe Y1 moving Yi
  Zou to P2 gives 5 errors); P5 Peking University, state key laboratory + school, Beijing, CN. Probe Y2 (Rongping
  Wang to P4): 4 errors. Call 6. ok.
- spencer2012 (5; single, slots from header): University of California + campus Santa Barbara (printed without a
  comma), unit Department of Electrical and Computer Engineering, locality Santa Barbara, US; maps to org_ucsb. Call
  7. ok.
- tokushima2016 (3; prose): call 5. ok.
- zhao2015 (8; prose): "The authors" statement, Huazhong University of Science and Technology with Wuhan National
  Laboratory for Optoelectronics + School of Optical and Electronic Information as unit (lit_h66 zou2015 / D442
  form), Wuhan, CN. Probe ZH1 (unit without the national laboratory): 4 errors. ok.
- subramanian2012a (6; prose, slots from header): P1 Ghent University, Photonics Research Group + Center for Nano and
  Biophotonics, Ghent, BE (5 carriers named by initials); P2 IMEC, Leuven, BE (Verheyen). Probe SU1 (Verheyen on
  P1): 5 errors. ok.
- xu2017d (8; printed): block 1 Sun Yat-sen University, state key laboratory + school chain, Guangzhou, CN; block 2
  University of Bristol, Photonics Group + Merchant Venturers School of Engineering, Bristol, GB (printed UK; postal
  code not recorded). Siyuan Yu on 1, 2 in both layers. ok.
- watanabe2019 (3; single, p.2): call 3. ok.
- ura2017 (5; grouped, slots from header): call 2. ok.
- wang2025d (8; prose): P1 Jilin University, State Key Laboratory of Integrated Optoelectronics + college chain,
  Changchun, CN (7 carriers); P2 University of Chinese Academy of Sciences, College of Materials Science and
  Opto-Electronic Technology, Beijing, CN; clause P3 Institute of Semiconductors, Chinese Academy of Sciences (parent
  part of the printed name, contract example), unit Key Laboratory of Optoelectronic Materials and Devices, Beijing,
  CN. Probe W3 (clause dropped): 2 errors (D361). Call 1; F1.
- xu2017c (3; single): University of Central Florida, unit "CREOL, The College of Optics and Photonics", Orlando,
  US (state printed after the city, note); asterisk points to the contact line. ok.
- nambiar2017 (4; single, slots from header): Indian Institute of Science, Centre for Nanoscience and Engineering
  (printed before the org), Bangalore, IN. "Hemalatha M." as printed. ok.
- buf2015 (14; prose): call 8. ok.
- sapra2019 (7; prose): P1 Stanford University, Ginzton Laboratory, Stanford, US (6 carriers); P2 the same block
  for D. Vercruysse (second statement, own block, D354) with clause P3 KU Leuven, Department of Physics, Leuven, BE
  (prefixed postal code not recorded). List form "Jelena Vuckovic A" (D412) matched to printed Jelena Vučković (slot
  7). Probes SA1 (clause dropped) 2 errors, SA2 (Vercruysse on P1) 5 errors. ok.
- shi2014 (8; prose, slots from header): call 4. ok.
- fang2016 (7; prose): P1 Kunming University of Science and Technology, College of Science, Kunming, CN; P2 Jilin
  University, State Key Laboratory on Integrated Opto-Electronics (as printed, "on") + college, Changchun, CN; P3
  Institute of Microelectronics, Singapore, SG (5 carriers; A*STAR parent not copied). Printed Guoqiang Lo, list
  Guo-Qiang Lo (Unicode hyphen in the list): matched by name, no slot (compare.csv slot 7); probe FA1 (YAML name
  hyphenated): 0 errors (checker folds the hyphen; neutral, printed form kept). ok.

## Extractor calls (verified)

1. wang2025d "Yu Xin" (printed) vs list "Xin Yu", `slot: 2`. The pairing is right (same two name parts, swapped,
   D287 name-part variant; slot 2 is the only candidate). But the checker already matches this pair by name: probe
   W1 (explicit slot removed) gives 0 errors, 0 warnings, and the fix-applied write-run produces byte-identical
   `header_rows.csv`, `compare.csv` and `unmapped_orgs.csv` (slot 2 = Xin Yu). The explicit slot is redundant (h66
   F1 / h49 F2-F3 precedent; the committed lit_h53 / lit_h55 swapped-order notes read "matched by name"). F1. Probe
   W2 (YAML name Xin Yu) also passes with 0 errors (the text check tolerates the swapped order); the printed order
   Yu Xin is the correct YAML form.
2. ura2017 grouped (D368). Text and PDF print Ura, Mori, Tsujimoto, Inoue, then Department of Electronics / Kyoto
   Institute of Technology / Kyoto, Japan, then Kintaka, then Inorganic Functional Materials Research Institute /
   National Institute of Advanced Industrial Science and Technology / Ikeda, Osaka, Japan (contact lines masked
   after each block). G1 carried by authors 1-4, G2 by Kintaka; units printed before the orgs; locality Ikeda (first
   printed city, D288; prefecture in the note). Probes U1 (Kintaka on G1) 3 errors, U2 (Inoue on G2) 4 errors; U3
   (locality Osaka) 0 errors (known gap: prefecture accepted as locality). Header order = YAML order. Confirmed.
3. watanabe2019. Page 1 is the Photonics Journal cover (names and membership designations only); page 2 prints the
   author line and one unmarked block with only "Institute of Electromagnetics Fields" (misprint of the institute
   name, as printed, D699), Zurich, Switzerland and a postal code; no ETH Zurich or other parent anywhere in the
   header. Recorded as org with `locator: "p.2 header"` (D366 cover pages). Probes WT1 (locator p.1) 2 errors, WT2
   (org ETH Zurich + institute as unit) 2 errors (not printed), WT3 (corrected spelling) 2 errors. List "T. Watanabe"
   and "Yuriy Myronovych Fedoryshyn" match the printed full names by name. The 3 rows go unmapped until an alias to
   org_eth_ief exists (org round). Confirmed.
4. shi2014 (slots from header). Header order Shi, Guan, Novack, Streshinsky, Lim, Lo, Baehr-Jones, Hochberg = YAML
   order. Four statements: (1) four authors with the Institute of Microelectronics (A*STAR parent printed after it,
   not copied; extracted one word per line in both layers) and clause National University of Singapore, Department
   of Electrical and Computer Engineering; (2) Lim and Lo (subject "A. E.-J. Lim and G.-Q. Lo") with the Institute of
   Microelectronics (own block, D354); (3) Baehr-Jones with University of Delaware, ECE department, Newark, US and
   clause EastWest Photonics pte Ltd., Singapore, SG (as printed); (4) Hochberg with National University of
   Singapore, ECE department, and clause University of Delaware, ECE department, Newark. Probes SH1 (Shi without P2)
   2 errors, SH2 (EastWest clause dropped) 2 errors, SH3 (A*STAR parent copied into org) 0 errors and +1 unmapped
   (contract: parent not copied). Confirmed. See O1 for the order check.
5. tokushima2016. One "The authors" statement: Photonics Electronics Technology Research Association, followed by
   "Advanced Industrial Science and Technology" (without "National Institute of"), then the site / building
   designation and street, then Tsukuba and Japan. The span reads as the location of the association (it is followed
   directly by the site designation, and the statement names one employer), so it is not recorded as an
   organization; org PETRA (printed without the acronym here; maps to the registry PETRA id), locality Tsukuba, JP.
   Probe TK1 (span as `more_orgs`) passes with 0 errors (+3 rows, +1 unmapped), so the checker cannot decide this;
   probe TK2 (full AIST name) 2 errors (not printed). Recording AIST would add an affiliation the statement does not
   assert; the extractor's reading is the conservative one. Confirmed (judgment, noted in the paper note).
6. Institute of Microelectronics without the A*STAR parent (shi2014 P1 / P3, fang2016 P3): contract rule (parent
   named after the institute not copied); 38 committed lit blocks in other batches use the same org form; rows map to org_astar_ime.
   "Suzhou Institute of Nano-Tech and Nano-Bionics, Chinese Academy of Sciences" (yang2025a P1 / P4): the parent is
   part of the institute's printed name in the same comma form as the contract example; it equals the registry name
   of org_suzhou_institute_of_nano_tech_and_nano_bionics_chinese_academy_of_sciences and maps (probe Y3, parent
   dropped: 0 errors, +1 unmapped). Confirmed.
7. spencer2012 University of California + campus Santa Barbara (D301; printed "University of California Santa
   Barbara" without a comma, then "Santa Barbara, CA"). Same form as the D449 / D461 fixes and the lit_h59 / lit_h67
   blocks; maps to org_ucsb. Probe SP2 (campus removed): 0 errors, +1 unmapped (known gap: campus required for the
   mapping); probe SP1 (org "University of California Santa Barbara" in one string): 0 errors, maps (older committed
   form, superseded by D449 / D461). Probe SP3 (`slots_from_header` removed): 1 error. Confirmed.
8. buf2015 name variants and statements. Four statements naming authors by initials: (1) six authors with
   STMicroelectronics, Crolles, FR; (2) Temporiti with STMicroelectronics, Pavia, IT (second site, own block); (3)
   four authors with STMicroelectronics SRL, Agrate, IT (as printed); (4) three authors with Luxtera, Carlsbad, US
   (subject "G. L. Masini"). The prose article after "with" is not part of the org (probe B1 with it: 0 errors,
   neutral). Slots matched by name without explicit slots: Frédéric Boeuf / list F. Bœuf (ligature folded, slot 1),
   Gianlorenzo Masini / G. Masini (slot 10), Patrick Le Maitre / Patrick Le Maître (slot 12); also Mark Shaw / Mark
   Andrew Shaw, Thierry Pinguet / Thierry J. Pinguet, Massimo Ferè / Massimo Feré (accent folded). Probe B2 (Shaw on
   P1): 4 errors; B3 (SRL dropped): 0 errors, same org id, neutral. Confirmed.
9. "also with" clause blocks (pan2020 P2, wang2025d P3, sapra2019 P3, shi2014 P2 / P5 / P7): each further "with" of
   the same sentence is its own `clause: true` block right after its statement block, carried by every subject
   author (D366 (2)). Probes PA1 / W3 / SA1 / SH2 (clause dropped): 2 errors each (D361 coverage). Probe PA2 (pan2020
   clause as org Ningbo Research Institute + more_orgs Zhejiang University): 0 errors, +6 rows, +1 unmapped; the
   committed unit form is kept. Confirmed.
10. D412 list artefacts: pan2020 "Daoxin Dai A" and sapra2019 "Jelena Vuckovic A" are the known truncated list forms;
    printed names recorded, matched by name; noted in both paper notes. Confirmed.
11. slots_from_header: the 6 papers are exactly the papers.csv rows with `n_authors_meta` 0, `show` prints the D352
    line for each, and every YAML author list equals the printed header order (checked by reading for all 6). Probe
    SP3: 1 error without the flag. Confirmed.

## Fixes (exact YAML edits)

F1 (precision; no row change; wang2025d, lines 163 and 170). Remove the redundant explicit slot and update the note.
Line 170, replace

```
    - {name: "Yu Xin", markers: ["P1"], slot: 2}
```

with

```
    - {name: "Yu Xin", markers: ["P1"]}
```

In the line 163 `note`, replace

```
author 2 printed as Yu Xin, author list Xin Yu (same name parts in swapped order, slot set)
```

with

```
author 2 printed as Yu Xin, author list Xin Yu (same name parts in swapped order, matched by name)
```

Probe F (F1 applied): 0 errors, 0 warnings, 135 rows, 7 unmapped; scratch write-run derived files byte-identical to
the stamped ones (scratchpad `h68_audit/probes/y/F.yaml`). After applying, re-run
`uv run python scripts/ofc_headers.py check lit_h68 --corpus lit` (the stamp hash changes).

No other fix: no slot, marker, block, field, locator or other note is wrong.

## Observations (no YAML change)

- O1 Checker gap, header order for all-prose papers with `slots_from_header`: probe SH4 (shi2014 authors 5 and 6
  swapped in the YAML) gives 0 errors, because an author whose blocks are all prose is not checked against the
  author line (D354). For such papers the slot order rests on the extractor alone; in this batch shi2014 and
  subramanian2012a were checked by reading and are in printed order. Suggest an author-line order check whenever
  `slots_from_header` is set, independent of the basis. For printed / single papers the order is checked (SN1: 2
  errors).
- O2 Known gaps reconfirmed: missing `campus` (SP2), prefecture accepted as locality (U3), YAML name in swapped order
  accepted (W2), a non-organization span accepted as `more_orgs` when its words are printed in the block (TK1).

## Lists for the coordinator

- D412 list: pan2020 "Daoxin Dai A", sapra2019 "Jelena Vuckovic A" (known forms, matched by name).
- D426 review list: none.
- Re-record list: none.
- Org round (7 unmapped strings): EastWest Photonics pte Ltd. (SG; lit_h18 records the variant "EastWest Photonics PTE LTD");
  Indian Institute of Science (IN); Institute of Electromagnetics Fields (CH, printed misprint without parent; alias
  to org_eth_ief); Kunming University of Science and Technology (CN); Kyoto Institute of Technology (JP);
  Max-Planck-Institut für Quantenoptik (DE); Ningbo University (CN). Mapped but campus-qualified: University of
  California, Santa Barbara (org_ucsb).

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 0 warnings, 135 rows | batch as written |
| F | F1 | 0 errors, 135 rows, derived files identical | fix form |
| W1 / W2 | wang2025d slot removed / YAML name Xin Yu | 0 / 0 errors | slot redundant (F1) / known gap |
| W3 / W4 | wang2025d clause dropped / Institute of Semiconductors without CAS | 2 / 0 errors | clause verified / neutral, contract form kept |
| PA1 / PA2 | pan2020 clause dropped / Ningbo institute as org | 2 / 0 errors (+6 rows, +1 unmapped) | clause verified / committed unit form kept |
| Y1 / Y2 / Y3 | yang2025a Zou on P2 / Wang on P4 / Suzhou without CAS | 5 / 4 / 0 errors (+1 unmapped) | subjects verified / registry form kept |
| SP1 / SP2 / SP3 | spencer2012 org one string / campus removed / flag removed | 0 / 0 (+1 unmapped) / 1 errors | D449 form kept / known gap / flag required |
| TK1 / TK2 | tokushima2016 AIST span as more_orgs / full AIST name | 0 (+3 rows, +1 unmapped) / 2 errors | judgment (call 5) / not printed |
| WT1 / WT2 / WT3 | watanabe2019 locator p.1 / ETH Zurich org / corrected spelling | 2 / 2 / 2 errors | p.2 block verified as printed |
| U1 / U2 / U3 | ura2017 Kintaka on G1 / Inoue on G2 / locality Osaka | 3 / 4 / 0 errors | grouping verified / known gap |
| SH1 / SH2 / SH3 / SH4 | shi2014 Shi without P2 / EastWest clause dropped / A*STAR parent copied / authors 5-6 swapped | 2 / 2 / 0 (+1 unmapped) / 0 errors | verified / verified / contract form kept / O1 |
| SA1 / SA2 | sapra2019 clause dropped / Vercruysse on P1 | 2 / 5 errors | verified |
| B1 / B2 / B3 | buf2015 "the Luxtera" / Shaw on P1 / SRL dropped | 0 / 4 / 0 errors | neutral / verified / neutral |
| R1 | riemensberger2012 YAML name Tobias Jan | 2 errors | as printed verified |
| FA1 | fang2016 YAML name Guo-Qiang | 0 errors | neutral |
| ZH1 | zhao2015 unit without the national laboratory | 4 errors | unit chain verified |
| SU1 | subramanian2012a Verheyen on P1 | 5 errors | verified |
| SN1 | sun2013b first two authors swapped | 2 errors | order verified (printed / single papers) |
