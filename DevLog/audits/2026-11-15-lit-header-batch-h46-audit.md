---
title: Fresh-context audit of the lit author-affiliation batch lit_h46 (23 papers)
date: 2026-11-15
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only with --dry-run, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h46/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D412, D426, D442, D546, D557, D565, D572); format from the 2026-11-15 h43 / h44 audits; read-only comparison with earlier batches (lit_h31 liu2024 building span, lit_h16 chang2026a duplicate list name, lit_h24 UCSB campus, lit_h01 / h02 Ghent University + IMEC, MIT Lincoln Laboratory and WNLO unit forms)
verdict: GO with 1 fix; 185 list slots + 1 header-only author audited; 179 recorded slots ok, 6 slots correctly without rows, 0 wrong; F1 zou2020 note (statement numbers); extractor calls (wu2017 partial, zhong2021 slots, yang2020a unprinted list authors, xu2025b single, yu2025a Currently working at dropped) verified and forced or precedent-conform
---

# Lit header batch audit: lit_h46 (2026-11-15)

## Scope

Batch lit_h46: 23 papers (IEEE journals 6 (JLT x5, PTL x1), Optics Express / Optica 8, preprints 7, High Power
Laser Science and Engineering 1, one manuscript-format preprint (zhou2021a)); 185 list slots (wang2024c
and zhou2024 with `slots_from_header`) plus 1 header-only author (zhong2021 Hongtao Lin, slot 0); 246 rows.
Restricted corpus: this record names only authors, orgs, units, cities and countries; no paper text is quoted and no
contact, street, building, postal-box or postal text is copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h46 --corpus lit --codes <id> --pdf`
  (all 23; output kept in the session scratchpad `h46_audit/show/` only).
- Per slot: printed name vs the `show` author list and `compare.csv`; marker run vs text layer and PDF layer
  (identical in both layers for every printed-marker paper); block fields (org, unit chain, more_orgs, campus, city,
  country); role; locator; grade. Every distinct (paper, org, unit, city, country, org id, match basis, basis,
  locator) tuple of `header_rows.csv` read (75 tuples, 246 rows).
- Prose papers (vagionas2021, xie2020, xu2019a, xu2022a, zou2020): every statement subject, verb, clause and field read
  against the footnote; xu2025b singular statement read.
- Contact lines behind dropped markers (wu2020a 4 / 5, zhou2021a 8 / 9): the masked lines were confirmed in the
  source PDF to start with those digits and to be contact lines (only the first character inspected, nothing copied).
- Symbol legends read on page 1 (yang2020a, yang2024c, yi2022, zhang2019c, zhou2024, wang2024c, zheng2020).
- Probes on scratch copies (`h46_audit/probes/probe.py` in the session scratchpad, scratch `LIT_BASE`, batch name
  `lit_p46`, `cmd_check(..., dry_run=True)`). md5 of every repo batch file identical before and after the audit;
  `check_stamp.txt` matches `headers.yaml` (sha256 38041189...).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h46 | 23 / 23 | 185 + 1 header-only | 186 | 0 | 0 |

- Rows 246 (all grade A: printed 177, prose 56, single 13; primary 184, additional 62, present address 0); recorded
  179, no_header 6 (wu2017 #1-#3 unreadable; yang2020a #6 Sawaby and #8 Arbabian not printed; zhong2021 #11 duplicate
  list entry); papers ok 22, partial 1 (wu2017), unreadable 0; `slots_from_header` 2 (wang2024c, zhou2024);
  `author_list_differs` 2 (yang2020a, zhong2021); explicit slots 2 (vagionas2021 #11, zhong2021 #10) plus slot 0
  (zhong2021 Hongtao Lin); `order_differs` 0; multi-affiliation slots 42; 22 unmapped org strings.
- Per paper (slots / rows): vagionas2021 15 / 15; vissers2021 5 / 15; vu2010 2 / 2; wang2024c 11 / 17; west2019 8 / 8;
  wu2017 3 / 0; wu2020a 10 / 10; wu2020b 3 / 3; xiang2022 5 / 6; xie2020 9 / 9; xu2019a 9 / 9; xu2022a 7 / 14;
  xu2025b 1 / 1; yang2020a 11 / 13; yang2024c 7 / 7; yi2022 7 / 9; yu2025a 7 / 24; zhang2019c 12 / 13;
  zheng2020 11 / 14; zhong2021 11 (+1 slot 0) / 13; zhou2021a 14 / 25; zhou2024 9 / 10; zou2020 8 / 9.

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (185 + 1) | 186 | 0 | 0 |
| markers (183 header authors; 3 unreadable carry []) | 183 | 0 | 0 |
| header position (183) | 183 | 0 | 0 |
| blocks (org / unit / campus / locality / country) (180 authors with rows) | 180 | 0 | 0 |
| prose blocks (19 blocks, 5 papers) | 19 | 0 | 0 |
| present addresses (0 recorded; 1 dropped, yu2025a) | n/a | 0 | 0 |
| locators (all blocks) | all | 0 | 0 |
| notes (23) | 22 | 1 (zou2020 statement numbers, F1) | 0 |

## Per-paper findings

- vagionas2021 (15; prose, 4 statements): P1 Aristotle University of Thessaloniki + Department of Informatics and
  Center for Interdisciplinary Research and Innovation (6 authors); P2 same org + Department of Physics and the same
  center (Chrysostomidis, Roumpos, Vyrsokinos); P3 University of Twente + IOS Group, MESA+ Institute for
  Nanotechnology, Enschede, NL; P4 LIONIX International B.V., Enschede, NL (article after the verb not copied, prose
  form). Membership exact (probe V2). #11 printed Paulus W. L. van Dijk vs list Paul W. L. van Dijk: explicit slot
  required (probe V1), D287 (alternate form, all initials agree). ok.
- vissers2021 (5; printed, capitals): block 1 prints Ghent University and IMEC with no separator: org + `more_orgs`
  IMEC (lit_h02 form), Photonics Research Group, Department of Information Technology, Ghent, BE; block 2 Ghent
  University + Center for Nano- and Biophotonics (NB-Photonics), Ghent, BE. All five 1,2. ok.
- vu2010 (2; single): The Australian National University (article printed in the block, kept) + centre / research
  school chain, Canberra, AU; territory not recorded. Khu Vu vs list Khu T. Vu automatic. ok.
- wang2024c (11; printed, slots from header): 7 blocks read in both layers (ECNU XXL chain; SIOM, CAS with the state
  key laboratory and CAS center chain; UCAS centre, Beijing; ECNU precision spectroscopy laboratory; Shanxi
  University, Taiyuan; Shandong Normal University, Jinan; Hefei National Laboratory, Hefei); all CN. Ya Cheng
  1,2,4,5,6,7 and Yuan Zhou 2,3 exact. ok.
- west2019 (8; printed, closing-parenthesis markers): MIT + EECS, Cambridge, US; MIT + Lincoln Laboratory, Lexington,
  US (majority lit form; probe L1 shows the two-org form also passes, no change). ok.
- wu2017 (3; partial): the single block prints a building number and campus name between the unit chain and Zhejiang
  University (both layers). See call 1. ok.
- wu2020a (10; printed, capitals): Tsinghua University + Tsinghua-Berkeley Shenzhen Institute, Shenzhen (lit_h37
  form); Sun Yat-sen University + state key laboratory / school, Guangzhou; China University of Geosciences + school,
  Wuhan; all CN. Markers 4 (Fu) and 5 (Chen) are contact lines (verified). LIRONG CHENG vs list Li-Rong Lilly Cheng
  automatic (see question 3). ok.
- wu2020b (3; single, capitals): HUST + WNLO and school chain, Wuhan, CN (majority form). ok.
- xiang2022 (5; printed): Zhejiang University + three-part chain, Hangzhou (campus name after the org not recorded,
  lit_h01 / h10 / h33 / h44 precedent); Zhejiang University + Ningbo Research Institute, Ningbo; CN. #5 list form
  Daoxin Dai A (D412). ok.
- xie2020 (9; prose): P1 Harbin Institute of Technology at Shenzhen + Department of Electronic and Information
  Engineering, Shenzhen (6 authors; org kept whole, D565 Qinhuangdao precedent); P2 same org + Department of Science
  (Song); P3 Shanghai Jiao Tong University + state key laboratory, Shanghai (Du, He). Membership exact (probe Q3). ok.
- xu2019a (9; prose, abbreviated subjects): P1 McGill University + Photonic Systems Group, Department of ECE, Montreal,
  CA (8 authors); P2 Ciena Corporation, Ottawa, CA (Wang). Md Ghulam Saber vs list Md. Ghulam Saber automatic. ok.
- xu2022a (7; prose, The authors): P1 Shanghai Jiao Tong University + four-part chain, Shanghai; clause P2
  SJTU-Pinghu Institute of Intelligent Optoelectronics, Pinghu; CN. Clause bound (probe Q2). ok.
- xu2025b (1; single, footnote): Jiangsu University of Science and Technology + department / school chain, Zhenjiang,
  CN, `p.1 footnote`. See call 4. ok.
- yang2020a (11 list, 9 printed; printed): Stanford University + E. L. Ginzton Laboratory, Stanford; UT Austin + ECE,
  Austin; CUNY + Photonics Initiative, Advanced Science Research Center; CUNY + Physics Program, Graduate Center;
  CUNY + Department of Electrical Engineering; all New York, US. Cotrufo 2,3 and Alù 2,3,4,5 exact. See call 3. ok.
- yang2024c (7; single): Stanford + Ginzton Laboratory, Stanford, US. Joshua Yang vs Joshua SungWoo Yang automatic;
  #7 list form Jelena Vuckovic A (D412). ok.
- yi2022 (7; printed, capitals): HUST + WNLO and school chain, Wuhan; Beijing Institute of Technology + School of
  Information and Electronics, Beijing; Beijing Institute of Technology Chongqing Innovation Center, Chongqing (kept
  whole as printed); CN. Marker 4 = equal contribution (legend on page 1; probe M5 bound). ok.
- yu2025a (7; printed, closing-parenthesis markers): seven Seoul National University blocks, Seoul, KR, each with its
  unit; runs exact (Taehyun Kim 1,2,3,4,6,7). Block a) dropped, see call 5. ok.
- zhang2019c (12; printed, period markers): UESTC + national engineering research center, Chengdu, CN; MIT + DMSE,
  Cambridge, US; University of California + campus Santa Barbara + ECE, Santa Barbara, US (`org_ucsb`; lit_h24 form,
  acronym printed after the campus). ok.
- zheng2020 (11; printed): University of Washington ECE and Physics, Seattle, US; Ningbo University + laboratory /
  institute chain, Ningbo, CN; Intel Corporation + Silicon Photonic Products Division, Santa Clara, US; Stanford + EE,
  Stanford, US. Doylend, Dunham automatic. ok.
- zhong2021 (11 list + 1; printed, capitals): Zhejiang University + chain, Hangzhou; Westlake University + Zhejiang
  provincial key laboratory, School of Engineering, Hangzhou; Westlake Institute for Advanced Study + Institute of
  Advanced Technology, Hangzhou; Institute of Microelectronics of the Chinese Academy of Sciences, Beijing; all CN.
  See call 2. ok.
- zhou2021a (14; printed, capitals): 7 blocks (ECNU x2, SIOM, UCAS, ShanghaiTech, Shanxi, Shandong Normal) read in both
  layers; all CN. Markers 8 (Fang) and 9 (Cheng) are contact lines (verified; probe M4 bound, M3 not bound, G1). ok.
- zhou2024 (9; printed, slots from header): ECNU + State Key Laboratory of Precision Spectroscopy; ECNU + joint
  research center (name of both universities kept in the unit); Shanghai, CN. Last author's markers printed on the
  next line, checked (probe M7). Correspondence line not a block. ok.
- zou2020 (8; prose, 7 statements, 8 blocks): P1 Zhejiang University of Technology + College of Science, Hangzhou,
  clause P2 Nanyang Technological University + EEE, Singapore, SG (Zou; probe Q1 bound); P3 same org as P1 (Wang,
  Zhang); P4 Zhejiang University of Science and Technology, Hangzhou; P5 Shanghai Honghui Optics Communication Tech.
  Corp., Shanghai; P6 Hebei University of Engineer (as printed), Handan; P7 China Jiliang University, Hangzhou; P8
  Zhejiang University + centre / state key laboratory chain, Hangzhou; CN otherwise. Blocks exact; the note numbers
  blocks P6 / P8 as statements 6 / 8 (they are statements 5 / 7): F1.

## Extractor calls (verified)

1. wu2017 partial (block not recorded, all three authors unreadable). Probe W1 (unit chain + Zhejiang University):
   2 errors (unit and org not contiguous) in both layers. Probe W2 (org only, no unit) passes but drops the printed
   unit chain: not a valid form. Forced; same form as lit_h31 liu2024 (D426 G6, D546 re-record list). Keep; add
   wu2017 to the G6 re-record list (values in the paper note, no building number).
2. zhong2021 slots. The list prints Lan Li at 10 and 11 and omits Hongtao Lin. Probe Z1: Lan Li without slot matches
   [10, 11], error; Z2: Hongtao Lin without slot 0, error; Z4: without `author_list_differs`, error. Slot 10 follows
   the printed position (Z3 shows 11 also passes; 10 is the right choice, lit_h16 chang2026a precedent). Correct;
   slot 11 stays without rows; list form to the D412 file.
3. yang2020a unprinted list authors. The printed author line (both layers) has 9 names; list slots 6 and 8 have no
   header author. Probe A1: `author_list_differs` required. No rows for them, status ok (no unreadable author).
   Correct (chowdhury2022 / D572 handling of list-header mismatches).
4. xu2025b single. Probe X1 (prose P1): 2 errors, the checker reads only the plural subject. `single` with
   `p.1 footnote` gives the same row (grade A). Correct.
5. yu2025a block a) dropped. The footnote prints the cue Currently working at and an org (Samsung Display Co., Ltd.)
   with no place. Probe Y1 (block as present address): 2 errors (cue not accepted); Y2: `dropped_markers` entry
   required. Forced; same handling as liu2020b (h44) and the D442 cue list. Keep; add to the cue re-record list.
6. Explicit slot vagionas2021 #11 (probe V1 required), D287-conform.

## Fixes (exact YAML edits)

F1 (note accuracy). In `lit:zou2020` replace

```yaml
statement 6 prints Hebei University of Engineer as printed; statement 8 prints the centre
```

with

```yaml
block P6 (statement 5) prints Hebei University of Engineer as printed; block P8 (statement 7) prints the centre
```

Rows unchanged. Probe FIX_all (F1 on a scratch copy): 0 errors, 1 warning (vagionas2021 explicit slot).

## Open questions (with recommendation)

1. Re-record lists: wu2017 to the D426 G6 building-span list; yu2025a block a) (org Samsung Display Co., Ltd., no
   place printed) to the D442 cue list ("Currently working at" as a further cue). Recommended: yes.
2. D412 correction file: zhong2021 (Lan Li duplicated at 10 / 11, Hongtao Lin missing), yang2020a (list has Sawaby and
   Arbabian not printed in the cached version; also #11 Jelena Vuckovic A), yang2024c #7, xiang2022 #5, wu2017 #3
   (Daoxin Dai A forms). Recommended: add.
3. D426 review list: wu2020a #7 (list Li-Rong Lilly Cheng, printed Lirong Cheng; automatic match), yang2024c #1 (Joshua
   SungWoo Yang / Joshua Yang; automatic). Recommended: add wu2020a #7; yang2024c #1 optional.
4. G1 test list (last author's further markers not bound): wu2020a #10 Fu (probe M1) and zhou2021a #14 Cheng (M3) pass
   without their dropped contact markers; non-last authors are bound (M2, M4, M5). Recommended: add both.

## Unmapped org names (org round, no YAML change)

| printed org (unit) | place | proposal |
|---|---|---|
| Beijing Institute of Technology Chongqing Innovation Center | Chongqing, CN | new org or alias under Beijing Institute of Technology |
| China Jiliang University | Hangzhou, CN | new org |
| Harbin Institute of Technology at Shenzhen (2 units) | Shenzhen, CN | alias to the HIT Shenzhen campus org if the registry has one (lit_h07 prints Harbin Institute of Technology (Shenzhen)), else new org |
| Hebei University of Engineer (printed misnomer) | Handan, CN | alias to Hebei University of Engineering, flagged as a printed misnomer |
| Hefei National Laboratory | Hefei, CN | new org (also pending from D546 chen2026c) |
| Institute of Microelectronics of the Chinese Academy of Sciences | Beijing, CN | alias (IMECAS) or new org |
| Jiangsu University of Science and Technology | Zhenjiang, CN | new org |
| LIONIX International B.V. | Enschede, NL | alias (capitals form) to the LioniX org used by lit_h01 / h10 / h11 / h14 |
| Ningbo University | Ningbo, CN | new org |
| Seoul National University (7 units) | Seoul, KR | new org |
| Shanghai Honghui Optics Communication Tech. Corp. | Shanghai, CN | new org |
| The Australian National University | Canberra, AU | alias (article form) or new org |
| Westlake Institute for Advanced Study | Hangzhou, CN | new org or alias under Westlake University |
| Zhejiang University of Science and Technology | Hangzhou, CN | new org |
| Zhejiang University of Technology | Hangzhou, CN | new org |

(22 strings in `unmapped_orgs.csv`: Seoul National University with 7 units, HIT Shenzhen with 2.)

## Privacy and as-printed scan

- Grep over `headers.yaml`, `header_rows.csv`, `compare.csv`, `unmapped_orgs.csv` and `papers.csv` (paper ids and
  decision ids stripped) for contact / URL patterns, street / road / avenue / suite / room / building / box words,
  "No." + digit and digit runs of 4 or more: 0 hits. The wu2017 note says a building number is printed without
  giving it; campus names in the xiang2022 and zhang2019c notes follow earlier notes. No contact, street, building,
  postal code or P.O. box anywhere in the batch, notes included.
- `show` masking gap (outside the batch, known from h44): line-broken contact addresses leave domain fragments
  unmasked in several IEEE footnotes (vagionas2021, xie2020, xu2019a, zou2020). Not copied into the batch or this
  record.
- As printed (kept, correct): Hebei University of Engineer; LIONIX International B.V. (capitals); XXL—The Extreme
  Optoelectromechanics Laboratory (em dash, zhou2021a) and The Extreme Optoelectromechanics Laboratory (XXL)
  (wang2024c); School of Information & Electronic Engineering (ampersand); Department of Optoelectronic Information
  of Science and Engineering.

## Commands (2026-11-15 / 16, log times)

| Command | Result |
|---|---|
| `check lit_h46 --corpus lit --dry-run` 23:53:38 (pid 92204) | 0 errors, 1 warning (vagionas2021 explicit slot); slots 185, recorded 179, no_header 6; rows 246 (grade A 246; printed 177, prose 56, single 13; primary 184, additional 62); papers ok 22, partial 1; slots_from_header 2; multi-affiliation slots 42; 22 unmapped org strings |
| `show lit_h46 --corpus lit --codes <id> --pdf`, all 23 | headers, statements and author lists read (scratchpad only) |
| source PDF page 1, first character of contact lines (wu2020a, zhou2021a) | markers 4 / 5 and 8 / 9 confirmed as contact lines |
| `h46_audit/probes/probe.py` on scratch copies, 23:57:29-00:00:10 | below; repo batch files md5 unchanged; probe checks wrote their usual logs under `logs/` (prefix `lit_headers_check_lit_p46`) |

| probe | change | result | reading |
|---|---|---|---|
| BASE | unchanged copy | 0 errors, 1 warning | baseline |
| W1 | wu2017 block with unit chain + org, authors readable | 2 errors | partial forced (call 1) |
| W2 | wu2017 block org only | 0 errors | drops the printed unit; not valid |
| X1 | xu2025b as prose P1 | 2 errors | singular subject not read (call 4) |
| Y1 | yu2025a block a) as present address | 2 errors | cue not accepted (call 5) |
| Y2 | yu2025a Goo without dropped a | 2 errors | dropped entry required |
| Z1 / Z2 / Z4 | zhong2021 Lan Li no slot / Lin no slot 0 / no author_list_differs | 1 error each | all required |
| Z3 | zhong2021 Lan Li slot 11 | 0 errors | checker neutral; 10 kept (printed position) |
| A1 | yang2020a without author_list_differs | 1 error | required |
| V1 | vagionas2021 van Dijk without slot | 2 errors | slot required |
| V2 | vagionas2021 Vyrsokinos P1 | 4 errors | statement membership bound |
| V3 | vagionas2021 org with leading article | 0 errors | neutral; prose form without article kept |
| Q1 / Q2 | zou2020 Zou / xu2022a Zhou without clause | 3 / 2 errors | clauses bound |
| Q3 | xie2020 Song P1 | 5 errors | membership bound |
| M1 / M3 | wu2020a Fu without 4 / zhou2021a Cheng without 9 | 0 errors | G1 (last-author gap) |
| M2 / M4 / M5 | wu2020a Chen, zhou2021a Fang, yi2022 Yi without dropped | 2 errors each | bound |
| M6 / M7 | wang2024c Cheng without 7 / zhou2024 Li without 2 | 1 error each | block use bound |
| C1 | zhang2019c without campus | 0 errors | campus by precedent (lit_h24), not forced |
| L1 | west2019 Lincoln Laboratory as org + MIT more_orgs | 0 errors | neutral; unit form is the lit majority |
| FIX_all | F1 | 0 errors, 1 warning | fix valid |

## Checker gaps observed (scripts not edited)

- G1 Last author's further markers not bound: wu2020a Fu, zhou2021a Cheng (M1, M3). Known (D442 / D546 / D557).
- D426 G6 building span between unit and org (wu2017). Known; re-record after the fix.
- Present-address cue list lacks "Currently working at" (yu2025a). Same family as the D442 cue gap.
- Singular prose subject "The author" not read (xu2025b); `single` + footnote locator is an equivalent record.
- `show` masking: line-broken contact fragments (known from h44).

## Verdict

GO with fix F1. All 185 list slots and the header-only author carry the right person; the 179 recorded slots have the
right markers, org, unit, campus, city and country; the 6 slots without rows are correctly unreadable (wu2017),
unprinted (yang2020a #6, #8) or a duplicate list entry (zhong2021 #11). Nothing is invented, no block is missed, no
contact, street, building or postal text is recorded. F1 only corrects statement numbers in the zou2020 note.
