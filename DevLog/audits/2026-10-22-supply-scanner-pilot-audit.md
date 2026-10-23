---
title: Fresh-context audit of the supply-chain vendor/model scanner pilot (DevLog-003 D205-D209, batch pilot_01)
date: 2026-10-22
scope: DevLog-003 (D205-D209 + amendments, "Audit checklist (pilot_01)"), scripts/scan_vendor_models.py, src/photonics_atlas/supply_scan.py, config/supply_scanner.yaml, scripts/build_supply_staging.py, src/photonics_atlas/rules_supply.py, data/schema/supply.schema.yaml, tests/test_supply_scan.py, data/_staging/supply/products/pilot_01/ (candidates.csv, candidates_run1.csv, review.csv, products.csv, product_usage.csv), data/_staging/supply/org_requests.csv
auditor: Claude (fresh context, read-only; scratch work in the private scratch folder, nothing in the repo edited except this file)
---

# Audit: supply-chain vendor/model scanner pilot (pilot_01)

Verdict: the pilot data are sound. Of 115 review facts, 108 are ok, 6 imprecise, 1 wrong (a held row); of the 44
staged rows, 40 ok, 4 imprecise, 0 wrong. All 165 candidate verdicts (run 2) are defensible; run 1 and run 2 agree on
the 118 shared candidate ids. Recall is the weak side: 20 usage facts in the 10 pilot papers were missed by both the
scanner and the review (9 of them in the 3 papers read in full: review recall there 41 / 50 = 0.82), almost all because
the vendor is not in the gazetteer. The scanner has systematic defects that the full corpus will hit (an optional-space
regex bug, `\w*` / `\S*` model tails, acronym over-matches from the registry, product identity by printed spelling,
reference-list and inline-acknowledgement detection on OFC texts). One of them already breaks the build: after the
registry curation of 23:12 (made by another stream during this audit), `build_supply_staging.py pilot_01 --dry-run`
fails on `product_comsol-comsol-multiphysics` (COMSOL Multiphysics vs Comsol Multiphysics, finding 8).

**Merge of pilot_01: conditional go** (fix the 5 rows below and decide finding 8 first, because product ids are
immutable, D8). **Full corpus (EO 231 + PK 296 + OFC 677 + lit): no-go until findings 1-5, 8, 9 and 11 are fixed**;
6, 7, 10 and 12-16 can follow in the first full-corpus batches. All fixes are small (config and one module); none
needs a redesign.

## What was run (2026-10-22, read-only for repo data)

| Step | Result |
|---|---|
| `uv run pytest -q tests/test_supply_scan.py tests/test_supply.py` | 43 passed |
| `uv run pytest -q` | 261 passed |
| `uv run python scripts/validate_db.py` (23:01 and again 23:13 after the registry change) | errors 0, warnings 16 / 18 (no supply warnings; the 2 new ones come from the 23:12 registry edit) |
| `build_supply_staging.py pilot_01 --dry-run` at 23:01 | reproduces the staged files: 44 usage, 41 products, 71 held, 0 new requests, 0 new validation errors; run-2 precision 142 / 165 |
| same at 23:13 (registry now has 44 of the gazetteer gap vendors) | **ERROR** product_comsol-comsol-multiphysics already J / 'COMSOL Multiphysics'; would stage 113, hold 1 |
| Page check of every review line (115) against the cached page (NFKC, de-hyphenated) | table below |
| Verbatim-overlap check of `stated_spec` vs the cited page | no quotation marks; longest verbatim spans in restricted rows 4-8 words (finding 15) |
| Full reads (methods / setup / fabrication) for recall: eo:didier2026, pk:ectc51687.2025.00027, pk:tcpmt.2025.3533388; parenthetical / company-suffix sweep of the other 7 | 20 missed facts (Recall section) |
| Scanner library run in memory over all 1214 registered sources with text (scratch output only, 166 s) | 4367 candidates; per-zone, per-vendor and over-match statistics in the findings |

The registry (`data/registry/organizations.csv`, `org_aliases.csv`) was modified at 2026-10-22 23:12 by a parallel
stream (vendor orgs added: Thorlabs, Santec, Ansys, COMSOL, Oxford Instruments, ...). Row counts below refer to the
build of 22:49 (44 staged / 71 held). The full-corpus statistics used the registry as loaded at about 23:05.

## Counts

| Object | ok | imprecise | wrong | Notes |
|---|---|---|---|---|
| Staged usage rows (44) | 40 | 4 | 0 | rows 1-4 below |
| Held review facts (71) | 68 | 2 | 1 | rows 5-7 below |
| All review facts (115) | 108 | 6 | 1 | vendor and model printed on the cited page for all 112 stated rows; 3 inferred rows correct |
| Products staged (41) | 40 | 1 | 0 | GS Infinity (row 2) |
| Candidate verdicts, run 2 (165) | 165 | 0 | 0 | false 23: ack 12, affiliation 6, own_org 4, collaboration 1 (all re-read) |
| Candidate verdicts, run 1 (134) | consistent | | | 0 verdict / reason differences on the 118 shared ids |

Imprecise / wrong rows:

| # | Row | Status | Evidence (page) | Fix |
|---|---|---|---|---|
| 1 | eo:mao2024 Keysight N1030A H7, stated_spec "DCA sampling module, 95 GHz" | imprecise | p.7 names DCA-X and N1030A together as high-speed DCA oscilloscopes with 95 GHz; "sampling module" is not stated. The same sentence prints DCA-X, which valdez2023a stages as a product but mao2024 does not (note calls it garbled; only the mainframe number after it is garbled) | stated_spec "DCA oscilloscope (with DCA-X), 95 GHz"; stage DCA-X for mao2024 or stop using DCA-X as a model anywhere (finding 8) |
| 2 | eo:tiberi2025 FormFactor "GS Infinity" H9 (product_formfactor-gs-infinity) | imprecise | p.14: GS is the tip configuration, Infinity the probe line (printed with the typo Porbe) | model "Infinity", configuration GS and 67 GHz in stated_spec; or product_line Infinity (finding 8) |
| 3 | pk:tcpmt.2025.3533388 Cascade vendor-only H9 | imprecise | p.7 prints the product line acronym ACPs (air-coplanar probes); ref [29] names the ACP probe | model "ACP" (product line), keep vendor as printed (Cascade, D207) |
| 4 | pk:tcpmt.2025.3533388 FormFactor vendor-only H9 (40 GHz probes) | imprecise | p.7 prints the product line, the pipe-Z-pipe probe | model "&#124;Z&#124; Probe" (needs a slug rule for the pipes) or product_line |
| 5 | eo:valdez2023a Rohde & Schwarz NRP110T.02 H3 (held) | wrong | p.11: a calibrated thermal RF power meter; H3 is optical power meters. The config model pattern `NRP\d{2,3}[TSA]` carries the same wrong hint | top-level H with note (the tree has no RF power-meter node) or add one; fix the config cat |
| 6 | pk:tcpmt.2025.3533388 Schott Borofloat 33 A7 wafer_supply (held) | imprecise | p.2: glass core of the glass interposer test vehicles; the tree has both A7 (glass substrates / glass cores) and E8 (glass cores and interposers) | decide the A7 / E8 split once (packaging glass core -> E8 packaging_material is the closer node) and note it in D207 |
| 7 | pk:ectc51687.2025.00027 Sakura Seiki YWV-4635S F9 (held) | imprecise | p.3: flux cleaning machine; F9 is reflow and plating | top-level F with note (as VH-2347), or a cleaning node |

Checked and ok (checklist items 3-5): vendor as of the source is applied consistently (Agilent 8164B / 81110A,
Ando AQ6317B, Finisar XPDV3320R / XPD3120R, Cascade "currently FormFactor", Hewlett Packard 83651B, FEI Quanta in 2023,
Newport Model 1471): the printed vendor is kept, as D207 says. Inferred vendors: DWL 66+ -> Heidelberg Instruments,
ARB Rider AWG-7204 -> Active Technologies, Duralco 132 -> Cotronics (Cotronics printed with Duralco 128 two
pages earlier) are correct. EBPG 5200+ vs EBPG 5200 as two products is right. Borderline categories that are fine:
101-190D / CSR-4 calibration substrates as H9 (probe accessories), EPO-TEK 301-2 as E3 (the paper uses it as
underfill), Duralco as E7, VH-2347 as top-level F, TFS Helios FIB milling as G7 (G7 lists FIB). The 4 covered facts
(NanoLN valdez2023a, NGK didier2026, AMF / NLM johnson2025) exist in `data/supply/product_usage.csv`.

## Recall (facts missed by the scanner and the review)

Papers read in full: eo:didier2026 (19 review facts, 3 misses), pk:ectc51687.2025.00027 (13, 2), pk:tcpmt.2025.3533388
(9, 4): 41 / 50 = 0.82. The other 7 papers were swept for parentheticals and company suffixes only (lower bound).

| Paper | Missed fact (page) | Category / role | Why missed |
|---|---|---|---|
| eo:didier2026 | Evatec 50, gold evaporation (p.7) | G4 fab_tool | vendor not in gazetteer |
| eo:didier2026 | Vigo PVM-2TE-10.6 MCT detector (p.7) | H4 test_instrument | vendor not in gazetteer |
| eo:didier2026 | TBS 2000B oscilloscope, vendor not printed (p.7) | H7, inferred_from_model (Tektronix) | no model pattern |
| pk:ectc51687.2025.00027 | AKROMETRIX TherMoire AXP shadow moire warpage system (p.2) | G7 fab_tool | vendor not in gazetteer |
| pk:ectc51687.2025.00027 | SHINKO ELECTRIC INDUSTRIES fabricated substrates A and B (p.2) | B8 / E4 package substrate supply | vendor not in gazetteer |
| pk:tcpmt.2025.3533388 | Pactech SB2 jet machine, solder ball jetting (p.4) | F9 assembly_tool | gazetteer `PacTech|Pac Tech` is case-sensitive |
| pk:tcpmt.2025.3533388 | FLIR X6540sc infrared microscopy (p.4) | H17 / G7 | vendor not in gazetteer |
| pk:tcpmt.2025.3533388 | Rogers 4350B PCB core (p.7) | E4 packaging_material | gazetteer requires "Rogers Corp" |
| pk:tcpmt.2025.3533388 | AtaiTec in situ de-embedding software (p.9) | J software | vendor not in gazetteer |
| eo:tiberi2025 | Aixtron CCS 2D MOCVD reactor, hBN growth (p.9; p.16 Methods) | G4 fab_tool | registry org_aixtron matched only by its literal name "AIXTRON Ltd" |
| eo:tiberi2025 | Moorfield Nanotechnology MiniLab 60 thermal evaporator (p.9) | G4 fab_tool | vendor not in gazetteer |
| eo:tiberi2025 | Graphene Platform Cu foil for CVD graphene (p.16 Methods) | A5 material_supply | vendor not in gazetteer |
| eo:valdez2023a | Eravant SFA-503753420-15SF-E1 and SFA-753114616-10SF-E1 active multipliers (p.4) | H17 / H8, 2 products | vendor not in gazetteer |
| pk:eptc59621.2023.10457729 | LPKF Protoflow S reflow oven (p.3) | F9 assembly_tool | vendor not in gazetteer |
| lit:mu2026 | Pasternack PE1BT1002 bias tee (p.12) | H8 test_instrument | vendor not in gazetteer |
| lit:mu2026 | Gel-Pak NDT-XT-RA nano device tray holding the LDs (p.5) | F (assembly consumable) | vendor not in gazetteer |
| lit:mu2026 | Voltcraft 302K/J thermometer for the bonding temperature (p.5) | H17 | vendor not in gazetteer |
| lit:mu2026 | ams OSRAM fabricated the InGaN laser diodes (p.4) | C laser die (co-author company) | not in gazetteer; also a rule question: the AMF fabrication row of the same paper (also a co-author company) is staged, so the LD supply should be treated the same way |
| eo:mao2024 | Keysight DCA-X (p.7) | H7 | reviewer choice, see row 1 |

The DevLog claim "run 2 proposes all 115" is circular (the gazetteer was tuned on these pages). Expect recall on new
papers to track gazetteer coverage of long-tail vendors; finding 10 proposes a gazetteer-independent candidate class.

## Findings (scanner code and config; evidence from the full-corpus in-memory run unless stated)

| # | Finding | Evidence | Fix |
|---|---|---|---|
| 1 | `flex_spaces` turns an optional space `" ?"` into `\s+?` (lazy one-or-more), so the space becomes mandatory | 8 config patterns: University ?Wafer, Master ?Bond, West ?Bond, New ?Focus (vendor and model), Menlo ?Sys- ?tems / Menlo ?Systems, Lake ?Shore, VPI ?Transmission. Verified: none of NewFocus, MenloSystems, LakeShore, MasterBond match. valdez2023a MenloSystems was proposed only as a model-only candidate for this reason | map `" ?"` -> `\s*` and `" "` -> `\s+` (handle a quantifier after the space); unit test with the 8 patterns |
| 2 | Model regexes with `\s?\w*` / `\s?\w+` tails glue onto following words or suffixes | FEI `Titan\s?\w*` matched "Titanium" 13 and "Titanate" 10 times (23 false model candidates); 21 model strings end in a lowercase word ("Lumerical and", "Lumerical was", "Lumerical simulations"); same shape in Helios, Talos, PathWave, Savannah, Koheras, Cyclotene, Fineplacer, Dektak, BlueWave, Plasmalab, CoBrite | require whitespace then a token with a digit or capital (`Titan(\s+[A-Z0-9]\w*)?`), never `\w*` directly after the stem; drop trailing lowercase words in `_cand` |
| 3 | `\S*` / `\S+` model tails capture punctuation | 10 corpus candidates: TSMJ-...-2). , PAS 5500/350C) , AR-P 6200.09) , ZHL-42W+, , XR-1541, ; run 1 had "AEDFA-40)"; 8 models keep a line-break hyphen ("TSL- 510", "JBX- 6300FS", "VCM- 330MS") | `[\w.+/-]*[\w+]` tails; normalize "X- 123" -> "X-123" in `_cand` (ids change, so do it before the full run) |
| 4 | Acronym and word over-matches | registry aliases SLM (Silicon Light Machines) 39 candidates, all spatial light modulator / single-mode uses; IDT (Integrated Device Technology) 36, interdigital transducers; MEC (pk org) in references; gazetteer AGC 6 of 14 vendor-only = automatic gain control; MPI model TITAN 6 = EPSRC grant name; `Hewlett[- ]Packard` maps Hewlett Packard Enterprise / Labs to org_hewlett_packard (6 of 10 HP candidates); `DOW` alternative matches DOW CORNING; `(?<!Dow.)Corning` fails across a line wrap (`.` does not match a newline) | stoplist registry forms of <= 4 capitals unless whitelisted (BNR, CICT, FICT, IDT, MEC, SDL, SLM, TIM; keep JDSU, SHF via gazetteer); AGC only as "AGC Inc" / with a glass model; drop TITAN; `Hewlett[- ]Packard(?!\s+(Enterprise|Labs|Laboratories))`; `DOW(?!\s+CORNING)`; lookbehind `(?<!Dow\s)` |
| 5 | Reference lists not detected | OFC: 206 / 623 sources (33 %): headings `## <span id="page-2-0"></span>References` (82), singular "Reference" (about 40), bullet lists `- [1] ...` with no heading (86). eo / lit / pk: 24 sources ("■REFERENCES", "References and links", numbered lists without heading). Measured leakage is small for OFC (11 candidates in 9 sources) but eo / lit show reference text as body candidates (Springer Berlin Heidelberg -> Heidelberg Instruments; author "Furukawa, K.") | HEADING_LINE: allow span / bold / section-number prefixes and singular "Reference", "References and links", leading "■"; REF_FIRST: allow `- ` / `* ` bullets |
| 6 | Inline acknowledgement and funding paragraphs are not zoned | 160 sources (OFC 113, eo 34, lit 11, pk 2) have "Acknowledgement(s):" / "**Acknowledgements**" / "Funding." with text on the same line; 23 body candidates fall inside (thank-you mentions of Keysight, Cadence, Furukawa, HPE, ...). Competing-interest statements (an author works on a technology at a named company) are body too | detect an ack label at line start followed by text, to the end of the paragraph; add a `coi` zone for competing-interest statements |
| 7 | Acknowledgements can state supply facts; D207 makes every ack candidate false | corpus examples (paraphrased): a vendor thanked for lending a named laser (eo:montifiore2026) or a WSS (ofc2026:M1C.2), Ajinomoto thanked for providing the insulation material (4 pk papers), AGC and Schott thanked for glass panels (pk:ectc51906.2022.00180). The pilot's 12 ack candidates were all assistance / support thanks, so the pilot verdicts stand | amend D207: an acknowledgement that names an item the vendor loaned or provided for the work is a usage fact (basis stated, note "acknowledgement") |
| 8 | Product identity by printed spelling splits products and now fails the build | D206 keys products on the printed model; slugs lowercase, so case variants collide and the builder errors (COMSOL Multiphysics / Comsol Multiphysics, observed 23:13). Across the full-corpus candidates 24 vendor + model groups would split into 2-4 products (MLA 150 / MLA-150 / MLA150; TSL-510 x4; SMF-28 / SMF28; EBPG 5200 / EBPG5200; XPD3120R / XPD 3120R; EVG 620 / EVG620; ZEP-520A / ZEP520A; ...); vendor names inside models (SHF 807C vs S807C, EPO-TEK 301-2, Ansys Lumerical vs Lumerical, COMSOL Multiphysics); families vs variants (DCA-X vs N1000 vs 86100D; N4372 vs N4372E; GS Infinity vs I67-A-GSG) | product key = org + canonical model (uppercase; drop separators between alphanumerics; strip a leading vendor / brand token; keep `+`); store the printed form in the usage row (notes or a new `model_printed` column); use `products.product_line` (exists, unused) for families. Decide before the merge: product ids are immutable (D8) |
| 9 | Gazetteer and registry are out of sync after curation; the code does not resolve gazetteer names as D205 says | D205: org "explicit or resolved by orgmatch on the name"; `load_dictionary` reads only the explicit `org`. After the 23:12 registry edit, 44 gazetteer vendors with `org: ''` resolve by name (Thorlabs, Santec, Ansys, COMSOL, Oxford Instruments, SHF, ...). Their registry twins are now also matched automatically: a re-scan of eo:didier2026 gives 28 candidates instead of 24 (duplicate vendor-only candidates with new ids, which the batch writer then reports as unreviewed), and `Dictionary.by_name` lets the registry twin overwrite the gazetteer entry. Note `Coherent` resolves to org_coherent by name although the gazetteer left it empty on purpose | refresh `org:` in the config (keep Coherent empty), or resolve at load time with an explicit ambiguity list; skip registry orgs whose name equals a gazetteer vendor name; test that no sentence yields two candidates for one org |
| 10 | Recall depends entirely on the gazetteer | 18 of the 20 misses are vendors absent from the gazetteer or matched only in one spelling / case. A parenthetical / company-suffix sweep (pattern "(model, Vendor)", "Vendor Model" with Inc / Ltd / GmbH / Corporation / Co.) found most of them on the 10 pilot papers | add a gazetteer-independent candidate kind `unlisted` (parenthetical with a model-like token plus a capitalized name, or a company suffix) for review; make vendor regexes case-insensitive for names >= 5 letters (Pactech, AMKOR) |
| 11 | `infer: true` on models whose vendor changed (D6 lineage) | software: Lumerical (Lumerical Inc. until Ansys acquired it), HFSS (Ansoft era), CST (before Dassault), RSoft (before Synopsys); fab tools: Fiji / Savannah mapped to Cambridge NanoTech although tiberi2025 prints Veeco; Dektak / Dimension 3100 (Veeco era, now Bruker); EXFO T100S / XTA-50 (Yenista era); Keysight patterns that also cover Agilent-era models (N52xxA, N4373A-C, N90x0A, B29xxA, DSOX, E5071C, PNA-X). The acquisition history is background knowledge to verify, not from local sources | set `infer: false` on these patterns (or gate by source year); add a per-model `lineage` vendor list so a printed predecessor (Agilent, Ando, HP) merges with the model candidate instead of producing a vendor-only plus a model-only candidate (tiberi2025 8164B, valdez2023a 81110A / AQ6317B) |
| 12 | Wrong category hint | `NRP\d{2,3}[TSA]` -> H3 optical power meters (RF power sensors); see row 5 | H with note, or a new node |
| 13 | OFC page locators mostly pNA | 473 of 862 OFC candidates (55 %) are pNA (text before the first figure marker); 259 of 677 OFC markdown files also carry `<span id="page-N-M">` anchors | use span anchors as additional approximate page marks (p.~N) |
| 14 | Sentence splitting separates vendor and item | SENT_SPLIT splits at "; " inside parentheses (valdez2023a p.4: the DFB laser parenthetical holds a wavelength, then a semicolon, then the vendor, so the vendor sentence loses the item) and after "Inc." / "Co., Ltd." followed by a capital | do not split inside parentheses; abbreviation list |
| 15 | Rights: no quotation marks anywhere; restricted rows reuse short noun phrases | longest verbatim spans: 8 words (pk:ectc51846.2026.00176 alignment phrase), 5-6 words in valdez2023a / johnson2025 / tcpmt rows (instrument-type names). Registry side (outside this batch): 5 lit sources with CC-BY-NC-ND-4.0 (lit:mu2026 among them) are open_license_ok while all 21 eo CC-BY-NC-ND-4.0 sources are restricted_local_only | guidance: restricted rows paraphrase anything longer than an instrument-type name (<= 5 consecutive words); harmonize the NC-ND redistribution rule in the registry |
| 16 | Request notes are incomplete | gazetteer hint uses `fullmatch` on the printed form, so vendors whose regex needs a following model (TFS, PI, Allied, Delo) and MenloSystems (finding 1) get no canonical-vendor hint (D208 am.); notes carry the category of the first held fact only (Thorlabs listed as H8 although its facts are H1, H2, H4, H10) | match with `search` on printed vendor + model; list the union of categories |

Lower-impact observations: the usage-cue regex contains from / by / with / via, so the cue flag is nearly always true
(run 2: cue true 122 / 133, cue false 20 / 32) and is not useful for triage. Full-corpus workload: 4367 candidates
(body 2895, front 1087, ack 293, affiliation 92); fixes 2 and 4 remove about 120 obviously false ones (SLM 39,
IDT 36, Titanium / Titanate 23, AGC 6, TITAN 6). AIMECHATEC (ectc51687) merges a bonding tool and a laser debonding
system into one vendor-only row (allowed by D207; the second item is lost).

## Org requests (checklist item 7)

The 57 vendor requests are correct as printed. Brand -> vendor pairs the curation needs (printed form stays):
Loctite, Ablestik, Ablebond -> Henkel; EPO-TEK -> Epoxy Technology; TFS -> Thermo Fisher Scientific and FEI -> FEI
Company (org event); Lumerical -> Lumerical Inc. (org event to Ansys); PI -> Physik Instrumente; Picoprobe -> GGB
Industries; Fineplacer -> Finetech; MUSASHI ENGENEERING (sic) -> Musashi Engineering; SENJU METAL INDUSTRY -> Senju
Metal; ThorLabs / Thorlabs, Ansys / ANSYS, Comsol / COMSOL, MenloSystems / Menlo Systems are one entity each. Most of
these were resolved by the 23:12 registry edit; Allied (Allied High Tech) and the printed-variant aliases are what
remains (one row stays held in the 23:13 dry run).

## Go / no-go

- pilot_01 merge: conditional go after (a) rows 1-7 above are corrected in review.csv, (b) the product-identity rule
  (finding 8) is decided and the batch rebuilt (the build currently fails on COMSOL), (c) the config `org:` values
  are refreshed (finding 9) so a re-scan does not add unreviewed duplicate candidates.
- Full corpus: no-go until findings 1, 2, 3, 4, 5, 8, 9 and 11 are fixed and a second 10-paper pilot on unseen papers
  (at least 3 OFC, 3 pk) measures recall with finding 10's `unlisted` candidates. Findings 6, 7, 12-16 can be fixed
  in the first batches.
