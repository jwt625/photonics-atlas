---
title: Fresh-context audit of the lit author-affiliation batch lit_h54 (22 papers)
date: 2026-11-18
mode: read-only on the batch (wrote only this record and scratchpad show dumps / probes; headers.yaml, derived files, scripts, people and registry data not edited; check run only with --dry-run, probes on scratch copies; aggregate and the people build not run; no network; no git)
scope: data/_staging/people/lit_headers/lit_h54/ (papers.csv, headers.yaml, header_rows.csv, compare.csv, unmapped_orgs.csv, check_stamp.txt); both header contracts; DevLog-011 D350-D369 and later lit rulings (D412, D413, D426, D442, D521, D546, D565, D599, D644); format from the lit_h51 audit
verdict: GO with 1 note fix; 132 slots (78 list + 54 slots_from_header) audited; 131 recorded slots with 0 wrong rows; 1 imprecise slot (zamek2011 #2 Liang Feng, Current Address block not recordable until the D442 cue fix; correct handling); F1 ji2022 note wording (unspaced statement spans two lines, not one)
---

# Lit header batch audit: lit_h54 (2026-11-18)

## Scope

Batch lit_h54: 22 papers (IEEE JLT / PTL / Photonics Journal prose footnotes, OSA Optics Express headers, three
conference papers); 132 slots, 10 papers `slots_from_header`; 141 rows. Restricted corpus: this record names only
authors, orgs, units, cities and countries; no paper text is quoted and no contact, street, building or postal text is
copied.

## Method

- Every paper printed with `uv run --offline python scripts/ofc_headers.py show lit_h54 --corpus lit --codes <id> --pdf`
  (all 22; wang2018c and zhao2019 also with `--pages 2`); output kept in the session scratchpad `h54_audit/show/` only.
- Per slot: printed name vs the `show` author list and `compare.csv`; marker run in the text and PDF layers; prose
  statement subjects; block fields (org, unit chain, campus, city, country); role; locator; notes. Asterisk lines of
  zamek2011, zheng2017, lu2017, tsarev2011, shang2015 checked in `references/<id>/text.md` (contacts masked in my own
  output): all contact lines. Later pages of ji2022, zamek2011, scarcella2017, hwang2007, chung2023 searched for
  present-address cues: only the page-1 statements and ji2022 biographies (not affiliation statements).
- 52 distinct (paper, marker, org, city, country, org id, match basis) tuples of `header_rows.csv` read (141 rows).
- Address / contact scan of `headers.yaml` and the derived CSVs (postal-code, street, building, ward, Eircode, box,
  phone and contact patterns): clean.
- Probes on scratch copies (`h54_audit/probes/probe.py`, scratch `LIT_BASE`, batch name `lit_p54`,
  `cmd_check(..., dry_run=True)`). Dry-run check of the real batch: 0 errors, 3 warnings (explicit slots wang2018c,
  scarcella2017, tsarev2011). md5 of every repo batch file identical before and after the audit; `check_stamp.txt`
  matches `headers.yaml` (sha256 fdf352c4...). Probe checks wrote their usual logs under `logs/` (prefix
  `lit_headers_check_lit_p54`).

## Counts

| batch | papers audited / total | slots audited | ok | imprecise | wrong |
|---|---|---|---|---|---|
| lit_h54 | 22 / 22 | 132 | 131 | 1 (zamek2011 #2, checker gap) | 0 |

- Rows 141 (all grade A: prose 81, printed 31, single 26, per_author 3; primary 131, additional 8, present address 2);
  recorded 131, no_header 1 (ji2022 #8 Wei Chen, unreadable); papers ok 21, partial 1 (ji2022), unreadable 0;
  `slots_from_header` 10; `author_list_differs` 0; explicit slots 3 (wang2018c 8, scarcella2017 7, tsarev2011 1);
  11 unmapped org strings; 0 order warnings.
- Per paper (slots / rows): liu2021c 4 / 8; wang2018c 11 / 11; zamek2011 6 / 6; zheng2017 11 / 11; chung2023 5 / 6;
  sakaguchi2015 13 / 13; scarcella2017 7 / 8; feng2014 2 / 2; dai2012 4 / 5; lu2017 10 / 10; tsarev2011 1 / 1;
  yamaguchi2022 3 / 3; liang2005 2 / 2; shang2015 5 / 5; zhao2019 5 / 5; hwang2007 6 / 7; watanabe2013 3 / 3;
  cheng2023a 8 / 8; ji2022 10 / 11; klaus2012 7 / 7; lee2014 5 / 5; horst2009 4 / 4.

### Per-slot field counts

| field | ok | imprecise | wrong |
|---|---|---|---|
| name / slot (132) | 132 | 0 | 0 |
| markers (printed / prose / per_author, 132) | 132 | 0 | 0 |
| header position | 132 | 0 | 0 |
| blocks (org / unit / locality / country) (131 authors with rows) | 131 | 0 | 0 |
| unreadable calls (1) | 1 | 0 | 0 |
| present addresses (2 recorded) | 2 + 1 not recordable (zamek2011, D442) | 1 | 0 |
| locators | all | 0 | 0 |
| notes (22) | 21 | 1 (ji2022, F1) | 0 |

## Per-paper findings

- liu2021c (4; prose): one "authors are with" statement + "and also with" clause: Zhejiang University with the state key
  laboratory / college / international research center chain, Hangzhou; clause Ningbo Research Institute as unit of
  Zhejiang University, Ningbo (same form as 5 committed blocks); CN. List slot 4 "Daoxin Dai A" (D412). ok.
- wang2018c (11; printed, cover page): marked author line and both blocks on p.2 (`p.2 header`, D366): McGill ECE,
  Montreal; UBC ECE, Vancouver; CA (provinces, postal codes not recorded). #8 printed "Nicolás Abadíacalvo" in both
  layers, list "Nicolás Abadía": explicit slot required (probe W1: 2 errors); same given name, same position, family
  name contained in the printed form (D287 name-part variant). #6 El-Fiky without middle initial matches automatically.
  ok.
- zamek2011 (6; printed, slots from header): block 1 UC + campus San Diego + ECE, La Jolla, US (6 committed La Jolla
  blocks). Block 2 is a "Current Address" line (Caltech EE, Pasadena): probe Z1 (recorded as present address, marker 2)
  2 errors (cue gap D442); Z2 (marker 2 not dropped) 2 errors; Z3 (status partial) 1 error (no unreadable author). The
  dropped marker + status ok is the committed handling (beeck2021, ji2017, koyaz2026, kuyken2011, jung2020,
  purnawirman2017, lit_h39 li2018). Asterisk = contact line (verified). Call 1 confirmed; #2 counted imprecise.
- zheng2017 (11; printed, capitals): HUST with WNLO + school chain printed before the org, Wuhan; "Sun Yatsen University"
  (both layers) + state key laboratory and school unit, Guangzhou; CN (province not recorded). Marker 4 = equal
  contribution on authors 1-2 (probe ZH1 without the entry: 2 errors); marker 3 on Cai = contact line (verified,
  masked). #8 printed JING DU, list Jing Lin Du: automatic match (D426 review list, xu2025 #7 precedent). ok.
- chung2023 (5; prose): five statements; P2 / P3 two statements for the same NSYSU department + center (two blocks, as
  the contract requires); P4 NCKU + P5 clause Miniaturized Photonic Gyroscope Research Center, NSYSU, Kaohsiung, printed
  without word spaces on one line: the checker verifies it (probe C1 wrong city: 2 errors). TW. Call 6 confirmed. ok.
- sakaguchi2015 (13; prose, slots from header): NICT (acronym kept) + Photonic Network Research Institute, Koganei
  (Tokyo after it, D288 first place); Sumitomo Electric Industries, Ltd., Yokohama; Yokohama National University,
  Yokohama; Optoquest Co., Ltd., Ageo (prefecture after it); JP. Leading "the" not copied (corpus practice for prose
  blocks). Detached accents written Luís / José (D282). ok.
- scarcella2017 (7; prose): "was with" Tyndall, Cork (affiliation of the work); "He is now with" CERN + Electronic
  Systems for Experiments, Geneva, CH, `present_address`; Photonics Packaging Group, Tyndall, Cork, IE; P4 CEA-Leti,
  Grenoble, FR with `skip_prefix: "MINATEC"` (probe S1 without it: 4 errors; "CEA-Leti" as one org has 6+ committed
  blocks). Eircode and Swiss / French postal codes not recorded. #7 typographic apostrophe: explicit slot required
  (S2: 2 errors; 5 committed O’Brien rows use the same form). #4 Jun-Su / Junsu automatic. Call 5 confirmed. ok.
- feng2014 (2; prose, slots from header): AIST + Network Photonics Research Center, Tsukuba, JP. ok.
- dai2012 (4; prose): Dai: Zhejiang University with the centre + state key laboratory chain, Hangzhou, CN, and clause UC
  + campus Santa Barbara + ECE Department, Santa Barbara, US (printed without the comma; maps to org_ucsb); others the
  same UCSB block. List "Daoxin Dai A" (D412); Jon D. / John Edward forms automatic. ok.
- lu2017 (10; single, capitals): HUST + School of Optical and Electrical Information (as printed), Wuhan, CN. ok.
- tsarev2011 (1; single): A.V. Rzhanov Institute of Semiconductor Physics SB RAS, Novosibirsk, RU (street and postal
  code not recorded). List name in Cyrillic: explicit slot required (T1: 2 errors). Under D413 a list name without Latin
  letters gets no lit slot in the people build, so this row stays staged (no person) until the D412 correction file
  gives a Latin list name. ok for the batch.
- yamaguchi2022 (3; per_author, slots from header): Keio Graduate School of Science and Technology; Sumitomo Electric
  Industries, Ltd.; Keio Faculty of Science and Technology; each prints only Kanagawa: locality empty (D288). Probe Y1
  (Kanagawa) passes: known checker gap (prefecture accepted as locality, D572), empty is the ruling. ok.
- liang2005 (2; prose): CUHK Department of Electronic Engineering, locality Hong Kong, HK, Shatin in the note (D366
  district rule). Probe L1 (Shatin) 0 errors: checker neutral; see O1. ok.
- shang2015 (5; single, slots from header): UC + campus Davis + ECE, Davis, US (9 committed blocks in the same form). ok.
- zhao2019 (5; single, cover page): SJTU state key laboratory + Department of Electronic Engineering, Shanghai, CN,
  `p.2 header`. ok.
- hwang2007 (6; prose, slots from header): Hwang "was with" ICU Optical Interconnection and Switching Laboratory,
  Daejeon, then "He is now with" KOPTI Integrated Optical Module Laboratory, Gwangju (`present_address`; probe H1 as
  affiliation: 2 errors); Cho / Kang / Lee / Park ICU; Rho KOPTI; KR ("Korea" printed). Call 5 confirmed. ok.
- watanabe2013 (3; printed "1)" / "2)", slots from header): Yokohama National University + "Graduate School of Eng."
  printed after the org, Yokohama; NTT Advanced Technology Corporation, Tokyo; JP. Street, building, wards and
  postal codes not recorded. Probe WA1 (no unit): 0 errors, neutral; as printed kept. ok.
- cheng2023a (8; prose): HUST + "Wuhan National Laboratory for Optoelectronics and School of Optical and Electronic
  Information" (joined by "and" as printed), Wuhan, CN. ok.
- ji2022 (10; prose, partial): S1 authors 1-5 Fudan five-part chain; S2 Liu and S3 Xu Fudan key laboratory /
  department / school chain, S3 clause Department of Physics; S4 Wei Chen: Shanghai University key laboratory + joint
  laboratory, Shanghai, clause Jiangsu Hengtong Fiber Science and Technology Corporation, Suzhou; S5 CityU Department
  of Electrical Engineering, Kowloon, CN; S6 Xiao Fudan chain + clause Yiwu Research Institute of Fudan University,
  Yiwu. Equal contribution printed as prose (no markers). Call 3, 4 confirmed; F1 note wording. Details below.
- klaus2012 (7; prose, slots from header): NICT (no acronym printed) + institute, Tokyo; Optoquest Co. Ltd. (printed
  without the comma here), locality empty; JP. Call 2 confirmed.
- lee2014 (5; single, slots from header): Hitachi, Ltd. + Central Research Laboratory, Kokubunji-shi (D366 "-shi" kept),
  JP. Figure text before the title does not disturb the header. ok.
- horst2009 (4; prose, slots from header): IBM Research GmbH + Zurich Research Laboratory, Rüschlikon, CH; IBM Research
  + Watson Research Laboratory, Yorktown Heights, US (state, postal codes not recorded). ok.

## Extractor calls (verified)

1. zamek2011 ok, not partial; marker 2 under `dropped_markers`; Liang Feng keeps block 1. Confirmed (probes Z1-Z3, seven
   committed precedents). The Caltech values are in the note for the D442 re-record list.
2. klaus2012 P2 locality empty. The block prints "Saitama" with a postal code whose prefix belongs to Ageo, and
   sakaguchi2015 prints the same company at "Ageo, Saitama": Saitama is the prefecture here, so "" (D288) is right;
   "Saitama" (probe K1) passes the checker but would name the wrong city. Keep.
3. ji2022 P7 country CN, locality Kowloon. The block prints "Kowloon" and "China" only; Hong Kong appears only inside
   the org name, which the contract excludes as a place. CN is the contract reading. Probe J2 (HK) also passes: the
   checker accepts the org-name occurrence (checker gap); J3 (locality Hong Kong) passes for the same reason. Keep; O2.
4. ji2022 P9 "Yiwu Research Institute of Fudan University" as one org: printed as one name (no comma split), as
   lit_h40 zhang2025d "Northeastern University at Qinhuangdao". Probe J5 (Fudan University + unit) 0 errors, neutral.
   Keep; parent link in the org round. ji2022 partial: probe J1 (Wei Chen readable) 4 errors (subject not found in the
   glued run, both layers), so `unreadable: true` is forced (zhuang2025 / psaila2024 glued-subject gap). P5 / P6 fields
   are still verified (J4 / J6 wrong city: 2 errors each). The note says the run ends at the first line end; it spans
   two lines in both layers: F1.
5. scarcella2017 `skip_prefix: "MINATEC"` required (S1). Present addresses scarcella2017 CERN and hwang2007 KOPTI with
   `role: present_address` (H1 confirms the cue binding). Keep.
6. chung2023 P5 unspaced line verified by the checker (C1). Keep.
7. zheng2017 "Sun Yatsen University" printed so in both layers (not an extraction artefact): keep, alias in the org
   round. watanabe2013 unit after the university: keep (WA1 neutral). yamaguchi2022 locality empty: keep (Y1 gap).
   liang2005 Shatin in the note: keep (D366; O1). dai2012 / liu2021c "Daoxin Dai A": list artefact, header form
   "Daoxin Dai" matches automatically; D412 list. Explicit slots wang2018c #8, scarcella2017 #7, tsarev2011 #1 all
   required (W1, S2, T1). wang2018c / zhao2019 `p.2 header` right (cover pages). The 10 `slots_from_header` papers all
   print "[no author list: slots_from_header (D352)]" in `show`.

## Fixes (exact YAML edits)

F1 (ji2022 note, factual wording). The glued statement of author 8 runs without word spaces over its first two printed
lines in both layers, not only to its first line end. Probe F1: 0 errors, rows unchanged.

In `lit:ji2022` replace

```yaml
is printed without word spaces up to its first line end in both the text and the PDF layer
```

with

```yaml
is printed without word spaces in its first two lines in both the text and the PDF layer
```

(inside the `note:` string; nothing else in the paper changes).

No other fix: no slot, marker, block or field is wrong.

## Observations (no YAML change)

- O1 Hong Kong districts: liang2005 records Hong Kong with Shatin in the note (D366), while lit_h51 liu2019b (same CUHK
  department) and lit_h04 / lit_h11 record Shatin. The corpus split is the open org-round question from the h43 / h51
  audits; the checker accepts either.
- O2 CityU country: ji2022 is the only CityU block in the lit corpus with country CN (14 record Kowloon, HK where Hong
  Kong is printed as the place). The row maps to org_city_university_of_hong_kong, so the org id is unaffected. The
  checker accepts HK from the org name (gap: org-name occurrence counted as a printed place); worth a checker test.
- O3 tsarev2011 #1: rows stay staged without a person (D413) until a Latin list name exists; add to the D412
  correction list (with lahijani2026, tebeneva2024).
- O4 Optoquest printed in two forms ("Optoquest Co., Ltd." sakaguchi2015, "Optoquest Co. Ltd." klaus2012): one org in
  the org round. Information and Communications University (hwang2007) and both IBM Research strings (horst2009) are
  unmapped: org round.

## Lists for the coordinator

- D412 author-list corrections: dai2012 #1 and liu2021c #4 ("Daoxin Dai A"); tsarev2011 #1 (Cyrillic list name, D413).
- D426 review list: zheng2017 #8 (list Jing Lin Du, printed JING DU; automatic match); wang2018c #8 (explicit slot,
  printed Abadíacalvo vs list Abadía).
- Re-record list (D442 "Current Address" cue): zamek2011 #2 Liang Feng, block 2 Caltech Department of Electrical
  Engineering, Pasadena, US, marker 2, `role: present_address`.
- Re-record list (glued statement subject): ji2022 #8 Wei Chen, P5 / P6 as recorded.
- Org round (11 unmapped strings): A.V. Rzhanov Institute of Semiconductor Physics SB RAS; CERN; IBM Research; IBM
  Research GmbH; Information and Communications University; Korea Photonics Technology Institute; NTT Advanced
  Technology Corporation; Optoquest (two forms); Sun Yatsen University (alias of Sun Yat-sen University); Yiwu Research
  Institute of Fudan University (child of Fudan).

## Probe table

| probe | change | result | reading |
|---|---|---|---|
| BASE | none | 0 errors, 3 warnings | batch as written |
| J1 | ji2022 Wei Chen readable, status ok | 4 errors | unreadable forced |
| J2 / J3 | ji2022 P7 country HK / locality Hong Kong | 0 / 0 errors | checker neutral (org-name gap); CN, Kowloon per contract |
| J4 / J6 | ji2022 P6 / P5 wrong city | 2 / 2 errors | glued-statement blocks verified |
| J5 | ji2022 P9 Fudan University + unit Yiwu Research Institute | 0 errors | neutral; one printed name kept |
| Z1 / Z2 / Z3 | zamek2011 present address recorded / marker not dropped / status partial | 2 / 2 / 1 errors | current handling forced |
| K1 | klaus2012 P2 locality Saitama | 0 errors | neutral; prefecture, empty kept |
| S1 / S2 | scarcella2017 no skip_prefix / no explicit slot | 4 / 2 errors | both required |
| W1 / T1 | wang2018c / tsarev2011 no explicit slot | 2 / 2 errors | required |
| L1 | liang2005 locality Shatin | 0 errors | neutral (O1) |
| C1 | chung2023 P5 wrong city | 2 errors | unspaced line verified |
| H1 | hwang2007 P2 as affiliation | 2 errors | present-address role required |
| Y1 | yamaguchi2022 G1 locality Kanagawa | 0 errors | checker gap; empty kept |
| WA1 | watanabe2013 no unit | 0 errors | neutral; as printed kept |
| ZH1 | zheng2017 author 1 without dropped marker 4 | 2 errors | entry required |
| F1 | ji2022 note wording | 0 errors | fix |
