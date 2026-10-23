---
title: Second fresh-context audit of the supply-chain vendor/model scanner (pilot_01 after fixes, pilot_02, unseen-paper precision)
date: 2026-10-23
scope: DevLog-003 (D205-D209, D290-D299, D299a-c, pilot results), audits/2026-10-22-supply-scanner-pilot-audit.md, src/photonics_atlas/supply_scan.py, config/supply_scanner.yaml, scripts/build_supply_staging.py, src/photonics_atlas/rules_supply.py, data/schema/supply.schema.yaml, data/schema/supply_categories.yaml, data/_staging/supply/products/pilot_01/ and pilot_02/ (review.csv, candidates*.csv, products.csv, product_usage.csv), data/_staging/supply/org_requests.csv (read only)
auditor: Claude (fresh context, read-only; scratch work in the private scratch folder; nothing in the repo edited except this file)
---

# Audit: supply scanner after fixes (pilot_01 changes, pilot_02, unseen papers)

Verdict: the staged facts are sound (0 wrong rows in pilot_02 or in the 27 changed pilot_01 lines). What needs fixing
before the merge is product identity (ids are immutable, D8), two pilot_01 lines that a registry edit at 23:43 now
silently holds (MUSASHI, SENJU), and a few stated_spec / category / note details. Raw precision on 20 unseen papers is
35 / 60 = 0.58 (Wilson 95 % 0.46-0.70); body-zone gazetteer / registry candidates are 33 / 37 (0.89); the `unlisted`
kind is the main noise source (0 / 8 in the sample, 2 / 18 over all 126 unseen candidates).

- (a) Merge pilot_01 + pilot_02: **conditional go** after the must-fix items M1-M6 below (all are review.csv / config
  edits plus a rebuild; no redesign).
- (b) Full corpus (EO + PK + OFC + lit): **no-go until M1-M3 and F1-F4 are fixed**; no third pilot needed, check the
  first full-corpus batch (about 30 papers) against the numbers here.

## What was run (2026-10-22 from 23:44 local, read-only for repo data)

| Step | Result |
|---|---|
| `uv run pytest -q` | 298 passed |
| `uv run python scripts/validate_db.py` | errors 0, warnings 15 (none from supply tables) |
| `build_supply_staging.py pilot_02 --dry-run` | reproduces the staged files: 22 lines -> 16 usage, 9 products, 6 held; 0 new validation errors; precision 34 / 47 |
| `build_supply_staging.py pilot_01 --dry-run` | **118 usage, 106 products, 17 held** vs the staged files 120 / 108 / 15: the registry edit of 23:43 (D311 removed the SENJU / MUSASHI aliases) holds 2 staged facts (finding M1); 0 new validation errors |
| In-memory re-scan of the pilot_01 / pilot_02 papers with the current config | pilot_02 identical (47 / 47 ids); pilot_01 +3 facility candidates (D299a, never reviewed), -1 reviewed dup (SENJU p.3) |
| Page check of every pilot_02 review line (22) and every changed pilot_01 line (7 corrections + 20 recall additions) | tables below |
| Product identity over all staged products (108 + 9 rows, 115 distinct ids) | table below |
| Verbatim span of stated_spec vs cited page (pilot_02 + changed pilot_01 lines) | longest span in restricted rows 4 words; no quotation marks (D297 ok) |
| Full reads for recall: pk:ectc51687.2025.00097 (whole text), lit:hu2023 (sections 2-4, setup figure, BER section); parenthetical / company-suffix sweep of the other pilot_02 papers | 0 misses in the two full reads; 2 misses elsewhere (Recall) |
| `scan_vendor_models.py --dry-run --force --only <20 unseen papers>` (log only) and the same scan in memory (scratch JSONL) | 126 candidates; 60-candidate seeded sample judged (Unseen papers) |
| Full-corpus in-memory scan (scratch only; 1214 sources) | 4390 candidates: body 3043, front 863, ack 353, affil 96, coi 35; vendor 2664, vendor+model 950, model 521, unlisted 255; facility-origin 76 (ack 68, body 8). Top unlisted names: Wiley-VCH 38 (page footers), Steps 11, Northrop Grumman Systems 10 (copyright footer "©2022 Northrop Grumman Systems Corporation"), Semiconductor Research 8 (funding), Macmillan Publishers 5; 16 unlisted models are numeric ranges |

Registry note: `data/registry/organizations.csv` / `org_aliases.csv` changed at 23:43 (after both builds: pilot_01
23:30, pilot_02 23:41). Numbers above use the registry as of 23:44.

## Counts

| Object | ok | imprecise | wrong | Notes |
|---|---|---|---|---|
| pilot_02 review lines (22) | 19 | 3 | 0 | Th3C.1 facility notes x2 (stale), W2A.15 UCSB (D299a bar) |
| pilot_02 staged usage rows (16) | 13 | 3 | 0 | same three |
| pilot_02 held lines (6) | 6 | 0 | 0 | facts right; SHF should not be held (finding M3) |
| pilot_02 candidate verdicts (47) | 46 | 0 | 1 | lit:hu2023 cdb278f3f4cf9 (row P2-4) |
| pilot_01 corrected lines (7, first-audit rows 1-7) | 6 | 1 | 0 | N1030A stated_spec still "module" |
| pilot_01 recall additions (20) | 18 | 2 | 0 | mao2024 DCA-X stated_spec; ams OSRAM category C1 |
| pilot_01 unchanged lines hit by the 23:43 registry edit (2) | 0 | 2 | 0 | MUSASHI, SENJU vendor_printed short forms (M1) |
| Staged products, distinct ids (115) | 107 | 8 | 0 | D290 table; no merge of distinct models found |
| Facility_use rows (3) | 2 | 1 | 0 | Th3C.1 x2 meet D291 / D299a; W2A.15 does not literally |
| Unseen-paper sample (60 candidates) | 35 true | | 25 false | raw precision 0.58 |

## pilot_02 rows (imprecise / wrong only; the other 19 lines match their pages)

| # | Row | Status | Evidence (page) | Fix |
|---|---|---|---|---|
| P2-1 | ofc2026:Th3C.1 Marvell Nanofabrication Laboratory B7 facility_use | imprecise (note) | p.~2 ack: "The devices were fabricated at Marvell Nanofabrication Laboratory (Berkeley, CA) and Center for Nano-Micro Manufacturing (Davis, CA)" (OFC, restricted; quoted here only as the evidence of the bar). Fact and bar ok. Review and usage note say "not a scanner candidate (facility, not vendor-typed)", but since D299a the line carries cand_id c57ee108027de | drop the stale clause from the note |
| P2-2 | ofc2026:Th3C.1 Center for Nano-Micro Manufacturing B7 | imprecise (note) | same sentence; cand_id c1056796235f6 | same |
| P2-3 | ofc2026:W2A.15 UCSB Nanofabrication Facility B7 facility_use | imprecise (rule) | p.~3 ack: a portion of the work was performed in the facility. No fabrication / processing verb, so it does not meet the literal D291 / D299a bar ("explicit fabrication / processing statement"); the body describes the SiN and III-V process steps without naming a site. It is an explicit use statement of a fabrication facility, not a thanks | coordinator decision: either amend D299a ("work performed in / at a registry facility" counts, stated_spec says the process is not named) and keep the row, or hold it. The same wording appears in pilot_01 eo:valdez2023a p.7 (SDNI, finding M5), so decide once |
| P2-4 | lit:hu2023 candidate cdb278f3f4cf9 (Finisar, p.2) verdict false / citation | wrong (verdict) | p.2 intro: the authors' own PD's large-signal reception is as good as the commercial 70 GHz Finisar PD, i.e. the same reference PD used in this work (p.6 XPDV3320R), not a citation | verdict true / dup; pilot_02 precision of record becomes 35 / 47 (0.74) after D299a-c |

Checked and ok: W4E.5 Corning SMF-28e+ (p.~1, D1); Th3C.1 ASML 5500/300 (printed "ASML DUV Stepper (Model
5500/300)"; G2), Ficontec (the Ficontec tool, F1); ectc51846.2026.00302 Schott D 263 T eco (A7 wafer_supply per D296;
the ack SCHOTT AG "constructive collaboration" correctly false); ectc32696.2021.00125 ANSYS (J; TSMC CoWoS-R is the
authors' own platform); hulyal2026 M8199B, WaveShaper 15000S (product_line WaveShaper), UXR series as a family-level
product; hu2023 XPDV3320R (measured side by side under the same conditions: in scope, not a comparison-only mention),
N1000A with product_line DCA-X, SHF driver (p.5, p.9), Keithley source meter (p.6 setup figure text); huang2019a
COMSOL, EpoCore / EpoClad (Micro Resist Technology GmbH, top-level A per D296), KEYSIGHT tunable laser, AQ6370,
KOHERAS SuperK Compact, OFS Fitel two-mode fiber; yin2026 AMF covered; ectc51687.2025.00097 has no supply fact (all 7
candidates are author blocks). Vendor as of source kept everywhere (Finisar in a 2023 paper, KOHERAS, OFS Fitel).

## pilot_01 changed lines (imprecise only; 24 of 27 ok)

| # | Row | Status | Evidence (page) | Fix |
|---|---|---|---|---|
| P1-1 | eo:mao2024 Keysight N1030A H7, stated_spec "DCA oscilloscope module (with DCA-X), 95 GHz" | imprecise (first-audit row 1 only partly fixed) | p.7 prints "Digital communication analyzer high-speed oscilloscopes (Keysight, DCA-XN100A and N1030A, 95 GHz)"; "module" is not printed | "DCA high-speed oscilloscope with DCA-X, 95 GHz" |
| P1-2 | eo:mao2024 Keysight DCA-X family row, stated_spec "DCA sampling oscilloscope mainframe, 95 GHz with N1030A" | imprecise | same sentence; "sampling" and "mainframe" are not printed; the garbled token is "N100A" | "DCA high-speed oscilloscope, 95 GHz (with N1030A)"; note may record the printed token N100A |
| P1-3 | lit:mu2026 ams OSRAM C1 laser_source | imprecise (category) | p.4: blue (about 450 nm), edge-emitting, single-spatial-mode InGaN laser diodes fabricated by ams OSRAM. C1 is "DFB/DBR/EML/EA-DFB die and arrays"; nothing on the page says DFB / DBR | top-level C with a note (no node for blue / FP edge emitters), as D296 does for other gaps |
| P1-4 | pk:ectc51687.2025.00027 MUSASHI FAD2500 F6 and SENJU SNR-1065GT F9 (unchanged lines) | imprecise; now held | p.2 / p.3 print "MUSASHI ENGENEERING., INC." and "SENJU METAL INDUSTRY Co., Ltd."; D311 (23:43) removed the short-form aliases, so the rebuild holds both (120 -> 118 staged) and reopens their requests | vendor_printed = the printed company strings (or explicit org_id org_musashi_engeneering / org_senju_metal_industry); set the gazetteer org for both (F2) |

Checked and ok: Infinity family product (p.14, GS / 67 GHz in stated_spec); Cascade ACP family (p.7 prints "from Cascade
(currently FormFactor)"); |Z| probe family and CSR-4; NRP110T.02 top-level H with note; Borofloat 33 E8; YWV-4635S
top-level F; Evatec vendor-only (printed "Evatec 50"); Vigo PVM-2TE-10.6; TBS 2000B inferred (Tektronix pattern);
Akrometrix TherMoire AXP; Shinko "fabricated" substrates A and B (E4 acceptable with the note); Pactech SB2 jet
machine; FLIR X6540sc; Rogers 4350B core; AtaiTec in situ de-embedding; Aixtron CCS 2D (AIXTRON Ltd is a co-author
affiliation: co-author supplier rule D296 applies); Moorfield MiniLab 60; Graphene Platform Cu foil; Eravant x2; LPKF
Protoflow S; Pasternack PE1BT1002; Gel-Pak NDT-XT-RA; Voltcraft 302K/J. Rights: longest verbatim span 4 words
(restricted rows).

## Product identity (D290) over all staged products

No merge of distinct models (EBPG 5200 / 5200+, N4372 / N4372E, XPD3120R / XPDV3320R, DAD3221 / DAD3360 stay apart;
M8199B and XPDV3320R are shared ids across the two batches with the same category, so the sequential merge appends them
once). Imprecise:

| # | Product(s) | Issue | Fix (before merge; ids are immutable) |
|---|---|---|---|
| D-1 | product_keysight_technologies-n1000 (johnson2025 "Keysight N1000 DCA-X") vs product_keysight_technologies-n1000a (hu2023 "Keysight (DCA-X, N1000A)") | one product split by a dropped suffix letter; both rows already carry product_line DCA-X | one product: either map johnson2025 to the family-level product DCA-X (only the family is unambiguous) or rule that a suffix-less printed form of a model whose suffixed form exists for the same vendor joins it (note "printed N1000"). Background knowledge (to verify on a Keysight datasheet): the DCA-X mainframe is sold as N1000A |
| D-2 | product_ansys-optics (didier2026 p.7 "an eigenmode expansion solver, Ansys Optics") | strip_vendor leaves the generic word "Optics" as the model | guard in strip_vendor: do not strip when the remainder is a generic word (Optics, Software, Systems, Multiphysics is borderline); stage as family-level "Ansys Optics" (model = product_line) |
| D-3 | product_ggb_industries-model110 ("Picoprobe Model 110") vs product_newport-1471 ("Model 1471" -> 1471) | inconsistent handling of the word Model; brand Picoprobe not in product_line | canonical rule: drop a leading Model / Type / Series token; model 110, product_line Picoprobe |
| D-4 | product_epo_tek-epotek3012 (model "EPO-TEK 301-2") | D290's own example (EPO-TEK 301-2 -> 301-2) not applied: strip_vendor uses gazetteer vendors with the product's org, and the gazetteer Epoxy Technology / EPO-TEK entry has org '' | set the gazetteer org to org_epo_tek (F2); id becomes product_epo_tek-3012 |
| D-5 | product_keysight_technologies-uxr0702ap (product_line empty) vs family product UXR | families go to product_line (D290) | product_line UXR |
| D-6 | product_formfactor-i67agsg (product_line empty) vs family product Infinity | I67-A-GSG is an Infinity probe part number (background knowledge, verify on the FormFactor datasheet) | product_line Infinity after verification |
| D-7 | product_msc_software-marc2023.4 | a software release number as the model: every release becomes a product | model Marc, product_line Marc, release in the usage note (or keep the release but set product_line) |
| D-8 | product_allied-multiprepsystem ("Multiprep System") | generic trailing word in the model; a later "MultiPrep" splits | model MultiPrep (printed "Multiprep System" in the note) |
| D-9 | (code) `rules_supply.canonical_model` | drops every non-ASCII letter instead of folding it: TherMoiré AXP -> THERMOIRAXP, TherMoire AXP -> THERMOIREAXP (two ids); micro sign dropped | NFKD and strip combining marks before the A-Z filter (é -> E; µ -> U); test. Akrometrix is held today, so no staged id changes |

Also noted (registry, outside this batch): org_musashi_engeneering keeps the printed typo in an immutable id (D273
names printed-only orgs as printed); product ids built on it inherit it.

## Recall

- Full reads: pk:ectc51687.2025.00097 (0 supply facts, 0 misses), lit:hu2023 (4 facts, 4 found). With the owner's
  three full reads (8 / 8 after D299a-c), full-read recall on pilot_02 is 12 / 12.
- Sweep misses: lit:huang2019a p.2 Metricon 2010 prism coupler used to measure the core / cladding indices (vendor
  Metricon, model 2010; H, no node for prism couplers). The `unlisted` kind did not propose it because `_model_token`
  rejects all-digit tokens (UNIT_TOKEN matches a bare number). pk:tcpmt.2025.3533388 p.7 Rogers 4450F prepreg in the
  same sentence as 4350B (second Rogers product; pilot_01). ofc2026:Th3C.1 p.~2 "the AIM die" (SiPh transceiver dies,
  implied AIM Photonics fabrication): borderline, the supplier is implied by the die name only; reviewer decision.
- pilot_01 was not re-scanned after D299a: the current config adds 3 facility candidates that no review covers:
  eo:didier2026 p.7 (InAs/InAsSb photodetectors fabricated by the ShanghaiTech Material and Device Lab) and p.9 ack
  (same lab), eo:valdez2023a p.7 ack (part of the work performed at the San Diego Nanotechnology Infrastructure, same
  wording as W2A.15). didier2026 SMDL meets the D291 bar (explicit "fabricated by"); valdez2023a SDNI follows the
  P2-3 decision.

## Unseen papers (dry scan, precision estimate)

20 papers drawn with seed 20261023, 5 per corpus, from registered sources with text not in pilot_01 / pilot_02:
eo:kawahara2026, eo:kholeif2026, eo:xu2020, eo:hillier2025, eo:saxena2023, pk:ectc51909.2023.00021,
pk:ectc51846.2026.00123, pk:ectc51909.2023.00135, pk:001c.74577, pk:ectc51909.2023.00302, lit:cheng2025, lit:xu2023a,
lit:mckenna2022, lit:virot2014, lit:hosseini2015, ofc2026:Th3D.6, ofc2026:Th4C.7, ofc2026:Th3A.3, ofc2026:W4F.6,
ofc2026:Th2A.34. 126 candidates (`--dry-run` count = in-memory count); 60 sampled with the same seed and judged on the
candidate sentence, with the page read where the sentence was not enough (saxena2023 AIM, hillier2025 SMART). Same
true definition as DevLog-003 (the candidate points at a usage fact the paper states, D207 / D291).

| cut | true / candidates |
|---|---|
| all | 35 / 60 (0.58; Wilson 95 % 0.46-0.70) |
| zone | body 33 / 45, ack 2 / 5 (Keysight lent the AWG and DCA; AGC supplied the glass substrate), front 0 / 8, affil 0 / 2 |
| body without `unlisted` | 33 / 37 (0.89) |
| kind | vendor+model 11 / 11, model 9 / 13, vendor 15 / 28, unlisted 0 / 8 |
| corpus | eo 16 / 20, lit 13 / 20, pk 5 / 9, ofc2026 1 / 11 |
| usage cue | cue 27 / 33, no cue 8 / 27 |

False (25): affiliations / author e-mail / title 10, `unlisted` "Steps" parentheticals 6 (ofc2026:Th2A.34 "(Steps
1-2)"), publisher page footers 2 ("Macmillan Publishers Limited", `unlisted` company suffix), reference text inside
the body 2 (lit:hosseini2015: Optics Express format with "References and links" right after the abstract, inside the
first 30 % of the text), citations of others' work 2 (JePPIX roadmap, Vescent on TriPleX), acknowledgement thanks 2,
funding 1. All 18 `unlisted` candidates of the 126: 2 true (lit:hosseini2015 SolMateS SMP700 PLD, aixACCT Aix4PB),
16 false (Steps 8, publisher footers 5, a funding sentence in body text 2, a front-matter reference entry 1).

Recall seen while judging (not measured): hillier2025 p.5 "fabricated ... at SMART photonics" has no candidate (the
gazetteer entry is `case: true` with 'SMART Photonics|Smart Photonics'); several vendor-only candidates point at
models the model list lacks (Keysight ADS, PNA5225B (sic), N5290/91A, Thorlabs APD410A): the candidate still reaches
the reviewer.

## Findings (code, config, data) with fixes

Must fix before the merge (a):

| # | Finding | Evidence | Fix |
|---|---|---|---|
| M1 | Two staged pilot_01 facts are now held | P1-4; dry run 118 / 106 / 17 vs staged 120 / 108 / 15 | P1-4 fix, rebuild, confirm 120 staged |
| M2 | Product identity | D-1 to D-8 | apply, rebuild both batches, re-run the combined validation |
| M3 | Gazetteer org gaps hold registry vendors | SHF alias is scoped to eo (D273), so lit:hu2023 SHF is held although org_shf_communication_technologies exists; FEI alias scoped to pk; 20 gazetteer vendors with org '' have a regex that matches a registry org name: LioniX, SMIC, Innolight, Eoptolink, Accelink, Epoxy Technology, Taiyo Ink, Senju Metal, Musashi Engineering, FEI, SHF, Physik Instrumente, Luceda, ams OSRAM (fix), Coherent, Henkel -> org_loctite, SUSS MicroTec, Vistec, EXFO, Toptica (intentional or wrong match, keep '') | write explicit `org:` for the first 14; in load_dictionary warn when a gazetteer vendor without org matches a registry org name and is not `resolve: false`; without the explicit org, registry twins are also not skipped (two candidates per sentence) |
| M4 | P1-1, P1-2, P1-3, P2-1, P2-2, P2-4 | tables above | edit review.csv / candidates.csv |
| M5 | pilot_01 lacks the D299a facility facts | 3 candidates from the in-memory re-scan | re-scan pilot_01 (`--batch pilot_01 --force --drop-reviewed`; the SENJU p.3 dup is no longer produced), review the 3, decide P2-3 |
| M6 | D299a bar wording | P2-3 | one coordinator ruling for "work performed in / at <facility>" |

Must fix before the full corpus (b), in addition to M1-M3:

| # | Finding | Evidence | Fix |
|---|---|---|---|
| F1 | canonical_model drops accented letters | D-9 | fold accents; test with TherMoiré / TherMoire |
| F2 | strip_vendor / canonical rules | D-2, D-3 | generic-remainder guard; drop leading Model / Type / Series; family product_line when a family product of the same vendor is a prefix of the model (UXR / UXR0702AP), as a build warning |
| F3 | `unlisted` noise | 16 / 18 false on unseen papers; OFC "(Steps 1-2)" alone gives 8 in one paper; full corpus 255 unlisted, of which at least 74 are footer / funding / step patterns (Wiley-VCH 38, Steps 11, Northrop Grumman copyright 10, Semiconductor Research 8, Macmillan 5, plus 16 numeric-range models) | NAME_STOP += step, steps, phase, case, stage; reject model tokens that are numeric ranges (`\d+-\d+`); drop company-suffix names in page headers / footers (lines with "Publishers", "Publishing", "©", "All rights reserved"); skip unlisted in sentences with supported / funded / sponsored by, grant, program; accept an all-digit model token when the name side is a capitalized non-stop word ("(Metricon 2010)") |
| F4 | Gazetteer case gaps | SMART photonics (hillier2025) not matched with `case: true` | add 'SMART photonics' (keep `case: true`) and review the 33 `case: true` vendors for a lowercase second word |

Can follow in the first batches: OE-format reference lists in the first 30 % (6 sources: eo:sun2026a, lit:billah2018,
lit:bock2010, lit:hosseini2015, lit:tanizawa2015, lit:vazquezcordova2014); model list additions (Keysight ADS,
N5290A / N5291A, Thorlabs APD410 series, Metricon 2010); `Dassault CST` gazetteer alternation 'CST' is a bare
3-capital acronym (check on the first batch); first-audit finding 6 holds only for labelled acknowledgements:
funding sentences in body footnotes are still body.

First-audit findings re-checked: 1 (optional spaces), 2 (`\w*` tails: Titanium / Titanate / "Lumerical and" no longer
match), 3 (`\S*` tails), 4 (SLM / IDT / AGC / TITAN / Hewlett Packard Enterprise / DOW CORNING / Dow-newline-Corning),
5 (reference headings; residual OE format above), 7 (D291), 11 (`infer: false` on lineage models, `lineage:` merge),
12 (NRP -> H), 13 (OFC span anchors), 14 (sentences), 15 (rights), 16 (request notes) are fixed as described in D292-D298.
8 is fixed in rule (D290) with the residuals D-1 to D-9. 9 and 10 are partly fixed (M3, F3).

## Go / no-go

- (a) Merge pilot_01 + pilot_02 (`--merge` per batch in sequence, D299): **go after M1-M6**. The facts themselves have
  0 wrong rows; the must-fix items change product ids (D-1 to D-8, immutable once merged) or keep correct facts from
  being silently held. Re-run both dry runs and the combined validation after the edits.
- (b) Full corpus: **no-go until M1-M3 and F1-F4 are done**. Expected after the fixes: body precision about 0.9,
  overall raw precision about 0.6-0.7 driven by front matter / affiliations (discarded by zone in review); recall
  tracks the gazetteer plus the improved `unlisted` kind. Then go in batches; measure the first batch (about 30
  papers, at least 8 OFC and 8 PK) against this audit before continuing.
