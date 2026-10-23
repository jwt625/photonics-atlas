---
title: Fresh-context audit of org registry round 6 (DevLog-001 2026-10-23 entry, D330-D338)
date: 2026-10-23
scope: data/_staging/org_curation/batch_8/decisions.csv (147 rows); round-6 rows of data/registry/organizations.csv, org_aliases.csv and config/org_curation_overrides.yaml; data/_staging/people/ofc_headers/org_requests_resolution.csv (127 rows appended 2026-10-23); data/_staging/supply/org_requests_resolution.csv (29 rows); OFC header rows newly mapped by the round (sample 40 of 587)
auditor: Claude (fresh context, read-only for repo data; scratch work outside the repo)
---

# Audit: org registry round 6

Verdict: the mapping work is sound. All 587 newly mapped header rows and the 40 sampled rows point to the org that
the printed string names. The campus rule (D301) holds, and the round only appended rows. Three findings are wrong:

- **W1**: `org_rogers` was created as a printed org. D271 gives it the ROR record "Rogers (United States)".
- **W2**: the YOFC parent of the new State Key Laboratory org is not supported by any row that maps to it. All 61
  header rows that map to the lab print China Telecom Research Institute (CTRI) in the same block.
- **W3**: street, building and postal-code text from the restricted OFC headers was copied into decision evidence,
  registry notes and the published `registry.json`. The DevLog says "addresses never copied".

Five mappings are imprecise. D339 corrections are proposed below. W2 overturns a coordinator ruling (D305), so the
coordinator has to decide it.

## What was run (2026-10-23 01:10-01:25 PDT; no network, no git writes)

| Step | Result |
|---|---|
| `uv run python scripts/build_org_crosswalk.py --dry-run` | eo 284/284 strings, pk 181/181, lin 172/172, ofc2026 731/734 strings, 6051/6055 rows (0.9993); acceptance PASS |
| In-memory `build()` of the crosswalk vs `data/crosswalk/org_crosswalk.csv` (scratch script, no write) | 0 differences in 1371 rows: the committed crosswalk matches the registry |
| `uv run python scripts/validate_db.py` | errors 0, warnings 15 (14 "acquired without an org event", 1 eo:powell2024 year): the 987 people errors of 00:50 are gone after the 01:02 people build |
| Diff against the round's own backup `backup_round6_20261023T002301.zip` (extracted in scratch) | header rows 5478 / 5478: 587 unmapped -> mapped, 0 re-pointed, 0 lost, 4 basis-only (Th3F.3 imec-Ghent University `alias:unit_org` -> `alias`), 0 field changes; organizations 1001 -> 1067, 0 pre-existing rows changed or removed; aliases 416 -> 511, 0 changed or removed |
| Crosswalk rows pointing to a batch_8 org | only the 2 overturned skips (ofc2026 metadata: bare SKL string 6 rows, "University of Georgia" 2 rows); no EO / PK / LIN string captured by a new name or ROR label |
| ROR checks (pinned dump v2.15-2026-10-20, JSON) | every one of the 33 ROR ids: record active, display / labels, country, types, parents; same-key records for all 66 new names and their printed forms |
| OFC header views (`ofc_headers.py show`, terminal only) | 25 papers: the D333 / D335 orgs, the SKL papers, the scoped-alias papers, the campus rows |

Both scripts wrote their usual logs to `logs/`, which is git-ignored. No repo file other than this audit was written.

The HEAD versions (`git show HEAD:<path>`) predate rounds 4-6. The round-6 delta was therefore isolated against
the round's own backup zip.

## Counts

| Object | n | ok | imprecise | wrong |
|---|---|---|---|---|
| New orgs (registry rows) | 66 | 63 | 1 (I5 UGA provenance) | 2 (W1 org_rogers, W2 SKL parent) |
| Alias decisions (77 alias + 3 joint) | 80 | 76 | 4 (I1 Toptica, I2 Corning Optical Communications, I3 Cisco Quantum Lab, I3 Innolight Technology Research Institute) | 0 |
| Skip decision (UNIDEF, D337) | 1 | 1 | 0 | 0 |
| Override rows added to `org_curation_overrides.yaml` | 2 | 0 | 1 (UGA: mapping right, postal code in text) | 1 (SKL parent, W2) |
| OFC request resolution rows (round 6) | 127 | 124 | 3 (I2, I3 x2) | 0 |
| Supply request resolution rows | 29 | 27 | 1 (I1) | 1 (W1) |
| Header-row sample (newly mapped) | 40 of 587 | 40 | 0 | 0 (8 of the 40 land on the SKL org: the row mapping is right, the parent is W2) |
| Restricted-text hygiene (cross-cutting) | 1 finding | - | - | 1 (W3) |
| DevLog round-6 statements checked | 9 | 7 | 1 (I6) | 1 ("addresses never copied", W3) |

Of the 66 new orgs, 63 are ok after these checks:

- **ROR ids:** exact for all 28 OFC ROR orgs and all 5 supply ROR orgs. The two same-name picks are right: Al-Azhar
  University EG (05fnp1145) out of EG / QA (02pwa4b62) / ID (03ewepe58); University of Georgia US (00te3t702) over GE
  (02bjhwk41).
- **Brand-level records (D271):** Hamamatsu takes the JP root over the GB child. SUSS MicroTec takes the DE root over
  the CH child. Tokyo Electron takes the JP root over the IE child.
- **Parents (D333):** BT Research -> BT Group and IO-CSIC -> CSIC (only ROR parent, in the registry). Lab-STICC ->
  CNRS (the only one of its 7 ROR parents printed in the block; IMT Atlantique is in another block). Empty for OCA and
  ARTEMIS (several parents printed in one block), Télécom SudParis, CSULA, IST and MPL (ROR parents not in the
  registry).
- **Types:** ROR facility -> research_institute, the same as the 30 earlier rows.
- **Countries:** all match the ROR record or the header.
- **D335 printed orgs:** every host is in a separate block or joined by "and", so no parent is right.

The campus rows (CUHK-Shenzhen, IIT Delhi, UMD College Park, and the UC Davis forms) all map to the campus org,
never the parent.

## Findings

### W1. org_rogers: D271 ROR record missed

- Evidence:
  - The decision row "Rogers" and the supply resolution say "no exact ROR record". That is false. Active ROR record
    05m9vrv91 "Rogers (United States)" (company, funder; website rogerscorp.com; Wikipedia Rogers_Corporation;
    established 1832; Wikidata Q16984188) has the key "rogers" after the disambiguator is removed.
  - It is the parent of the only other same-key record, 02s5qve69 "Rogers (Germany)". That is exactly the
    brand-level case of D271.
  - The print (pk:tcpmt.2025.3533388 p.7 "Rogers" 4350B / 4450 F; reference [28] "Rogers Corp.") is the laminate
    vendor that the record describes.
  - `no_name_match` stays right: "rogers" is a common name, and Rogers Communications appears in OFC. D310 already
    keeps no_name_match orgs out of the ROR route, so adding the id changes no crosswalk row.
- Proposed correction (`config/registry_corrections.yaml`, `orgs:`):

```yaml
  org_rogers:
    name: Rogers
    name_basis: ror
    name_source: https://ror.org/05m9vrv91
    ror_id: https://ror.org/05m9vrv91
    country: US
    status: active
    founded_on: '1832'
    wikidata_qid: Q16984188
    website: https://www.rogerscorp.com
    origin: pk;ror
    why: "D339 (round-6 audit W1): D271 brand-level record (active, no parent, parent of the only other same-key record 02s5qve69 Rogers (Germany)); no_name_match and the pk-scoped alias kept (common name)"
```

  The `add_aliases:` entry keeps the printed company form:

```yaml
  - {org_id: org_rogers, alias: "Rogers Corp.", alias_type: printed_variant, origin: pk, scope: pk, basis: curated, notes: "D339: name as printed in pk:tcpmt.2025.3533388 reference [28]; org renamed to the ROR display (D16 priority ror > printed)"}
```

  Supply resolution notes, row Rogers: replace "D273 printed vendor org; no exact ROR record;" with "D271 brand-level
  ROR 05m9vrv91 (D339);".

### W2. SKL parent org_yofc is not supported by the rows the org receives

- Evidence:
  - **Rows the org receives:** `org_state_key_laboratory_of_optical_fiber_and_cable_manufacture_technology` gets 61
    header rows in 12 papers (M1F.5, M1J.4, M2C.3, Tu2C.5, Tu2F.3, Tu3E.5, W1E.2, W4H.6, Th1I.5, Th4C.1, Th4C.4,
    W1G.2) and 6 metadata rows.
  - **Header rows:** every one is a Beijing block that prints "China Telecom Research Institute" together with the
    lab. CTRI comes first in 9 of the 12 papers and second in 3 (M1F.5, Tu2C.5, Th1I.5). None of the 61 rows prints
    YOFC.
  - **YOFC rows:** the lab is printed with YOFC only in the Wuhan YOFC blocks (for example Tu3E.5 block 2,
    M2J.1, M4E.4, M1B.5). Those rows map to `org_yofc` (org first, unit second), not to the lab org.
  - **Metadata rows:** M1C.4 #9-#10 and Th1A.6 #7-#9 are YOFC-side authors. W1G.2 #11 is the CTRI-side author (header
    block 6, CTRI + lab).
  - **Rules:** D335 in the same round sets a parent "only when the host is printed with the org". D337 rejects a unit
    whose "two hosts [are] printed as a pair, relation to each not stated". For this lab the printed hosts are CTRI
    (Beijing) and YOFC (Wuhan). No local source states the lab's host relation.
  - **Effect:** a single YOFC parent places CTRI researchers under the YOFC root. That root is what produced the 3
    candidate person joins of the 00:53 people dry run. The people stream did not apply them (DevLog-004, 01:02).
- Proposed correction (coordinator decision, because it changes D305):
  - In `config/registry_corrections.yaml` `orgs:`:

```yaml
  org_state_key_laboratory_of_optical_fiber_and_cable_manufacture_technology:
    parent_org_id: ''
    name_source: ofc2026 printed (round 6 override, D336)
    why: "D339 (round-6 audit W2): the 61 header rows mapped to the lab all print China Telecom Research Institute in the same block, none prints YOFC; YOFC prints map to org_yofc; two printed hosts, relation to each not stated by a local source (D335 / D337 rule); D305 parent withdrawn until a primary source states the host"
```

  - In the `org_curation_overrides.yaml` row for the bare string, set `parent_org_id: ""`. Replace the notes clause
    "(Th4C.1 prints it first)" with "(all 12 Beijing papers print China Telecom Research Institute in the same block;
    9 of 12 print it first)".
  - Keep the mapping of the bare string to the lab. That part of D336 is correct.

### W3. Restricted header text (street, building, postal code) copied into decisions, registry notes and the app

- Evidence:
  - D172 / D244 allow only org, unit, city and country from the paywalled OFC headers. The round-6 DevLog says "(affiliation lines only, addresses never copied)".
  - **batch_8 decisions:** 44 of the 90 rows with OFC header evidence quote street names, building or PO-box text,
    or postal codes. Examples by printed org: Adtran, Huawei Technologies Düsseldorf GmbH, imec vzw., Nokia Canada
    Inc, ASN/Nokia, 1Finity Americas, Cisco Photonics, Innolight Technology Research Institute, National Centre for
    Advanced Integrated Photonics(NCAIP), Cluster of Excellence PhoenixD, Corning Optical Communications, University
    of Bath, University of Georgia, and 16 rows with Chinese postal codes.
  - **Merged copies:** the text was copied into 17 org notes (16 batch_8 orgs and org_university_of_georgia), 32
    alias notes, the 2 new override entries, 1 OFC resolution row (UGA) and DevLog D333 ("Athens, GA" plus the postal
    code).
  - **Published app:** 10 of the probed strings are in the published `app/static/data/registry.json`.
  - **Contract conflict:** the org-curation contract (`data/_staging/org_curation/INSTRUCTIONS.md`: "quote nothing
    beyond the affiliation line you rely on") allows whole affiliation lines. This conflicts with D244.
  - **Older batches:** batch_2 has the same pattern (21 rows); batch_1, 3 and 4 have 1 row each.
- Proposed correction:
  - Scrub the evidence and notes of the round-6 rows down to "org / unit, city, country". The proposed rule text
    for D339 and INSTRUCTIONS.md rule 7 is:

```text
Evidence quoting an OFC 2026 header (restricted corpus, D172 / D244) carries only organization, unit, city and country as printed; never a street, building, PO box, room or postal code. Same rule for registry notes, override entries, resolution files and DevLog text.
```

  - Files to change:
    - batch_8 `decisions.csv` evidence and notes (44 rows).
    - The 2 override entries. For UGA use "Athens, GA" without the postal code.
    - The UGA notes in the OFC resolution row.
    - The 17 org notes and 32 alias notes, through `registry_corrections.yaml` `orgs:` / `aliases:` `notes` fields,
      or a re-merge from the scrubbed decisions.
    - DevLog D333: replace the quoted address with "Athens, GA".
  - Then run `build_views.py` so `registry.json` no longer carries the text.
  - Whether to scrub batches 1-4 the same way is open question Q4.

### I1. "Toptica" (supply) -> org_toptica_photonics: the bare brand points to a US-named org, unscoped

- Evidence:
  - **The org:** `org_toptica_photonics` is the EO row "TOPTICA Photonics Inc.", country US. It was created from an
    author affiliation (eo:lee2026, a US employee).
  - **Where "Toptica" is printed:** the bare brand names the laser maker. ROR has one same-key record, 00t9ms296
    "Toptica Photonics (Germany)", Gräfelfing, alias TuiOptics GmbH.
  - The requesting paper (lit:li2025) is from East China Normal University (Shanghai). It is not a German lab.
  - The alias has empty scope, so it also routes the other "Toptica" prints the supply scanner found (eo:berman2026,
    eo:lee2026, eo:liu2026d, lit:kuznetsov2025) to the US-named org.
  - The D338 reasoning holds as far as it goes: the org's key "toptica photonics" already routes "TOPTICA Photonics
    AG" there. The root problem is the org's name and country, which the DevLog already lists as a follow-up.
- Proposed correction:
  - Interim: scope the alias to `lit` (the requested corpus). Hold the other corpora's Toptica usage as org_gap.

```yaml
- match:
    org_id: org_toptica_photonics
    alias: Toptica
  set:
    scope: lit
  why: "D339 (round-6 audit I1): bare brand names the DE maker (ROR 00t9ms296); org row is the US Inc.; scoped until the brand-level org exists"
```

    (This goes under `aliases:` in `config/registry_corrections.yaml`.)
  - Then, after a coordinator decision: create the brand-level org from ROR 00t9ms296 (DE, company, D271 single
    record) under a new id, for example `org_toptica_photonics_de`. Give `no_name_match: true` to whichever of the two
    orgs keeps only scoped aliases, because both names normalize to "toptica photonics". Move "Toptica" to the
    brand-level org. Set no parent link unless a source states it.

### I2. "Corning Optical Communications" -> org_corning, unscoped

- Evidence:
  - M2C.5 and Tu3A.4 print a UK site, so subsidiary_printed to the brand is consistent with contract rule 1.
  - The unscoped key "corning optical communications" also catches a future "Corning Optical Communications GmbH &
    Co. KG" (legal suffixes are dropped). That string would then route to `org_corning`.
  - The registry models the German entity separately (`org_corning_optical_communication`, DE, parent org_corning,
    alias "Corning Optical Communication GmbH & Co. KG"). The singular/plural spelling is the only thing that splits
    the two routes.
- Proposed correction: in `org_curation_overrides.yaml` `rows:`, add
  `"Corning Optical Communications": {scope: ofc2026}`.

### I3. Company research labs mapped as unit_printed: "Cisco Quantum Lab", "Innolight Technology Research Institute"

- Evidence:
  - Contract rule 2 says separate research labs with their own identity get their own org, with parent = the
    company.
  - Registry precedent follows that rule: China Telecom / China Mobile / China Unicom Research Institute, Toshiba
    Europe Cambridge Research Laboratory, Lightera Laboratories, Hewlett Packard Labs.
  - Tu2K.6 prints "Cisco Quantum Lab, Santa Monica" as its own block, separate from "Cisco Systems Inc, San Jose".
    M1D.1 prints "Innolight Technology Research Institute" (Suzhou).
  - The unit mapping loses nothing for people, because the roots are the same. It is still inconsistent with rule 2.
- Proposed correction: coordinator choice.
  - Option (a): keep unit_printed and record the rule-2 exception in D339.
  - Option (b): create `org_cisco_quantum_lab` (printed, type unknown, US, parent org_cisco) and
    `org_innolight_technology_research_institute` (printed, research_institute, CN, parent org_innolight), and
    re-point the two aliases.

### I5. Provenance labels of the two override-created orgs say batch_4

- Evidence: `org_university_of_georgia` notes begin "curated (batch_4)". The SKL org has notes "curated (batch_4)"
  and `name_source` "ofc2026 printed (batch_4)". Both orgs were created in round 6 by override rows (D333 / D336);
  batch_4 skipped them.
- Proposed correction: in the notes prefix, write "curated (round 6 override, D333)" for UGA and "curated (round 6
  override, D336)" for the SKL. The SKL `name_source` is covered in W2.

### I6. DevLog D336 caveat understates the CTRI co-print

- Evidence: "Th4C.1 prints CTRI first" reads as if CTRI were printed in one paper. In fact all 12 Beijing papers print
  CTRI in the same block, 9 of 12 print it first, and none of the 61 mapped rows prints YOFC. Details are in W2.
- Proposed correction: in the D339 text, give the counts above.

## Checked and ok (selected, with the reasoning behind the rulings the brief asked about)

### Fraunhofer HHI forms

The 5 forms (Th3A.1, M1C.2, W2A.2, M3Z.1 etc., W3I.1 misprint "Franhofer") all name the same institute, Berlin, DE,
at the source date. They are aliases, not events. "Fraunhofer Heinrich-Hertz-Institut" as native_name is right; the
`lang` tag is empty, as for 31 of the 34 native_name rows.

### EPFL

"Swiss Federal Institute of Technology Lausanne (EPFL)" and "(EFPL)" are the same institution. The misprint shares a
paper with the correct form (Th2A.21). Unscoped is safe because "Lausanne" is in the string.

### UCL

The full form "UCL (University College London)" is unscoped and unambiguous. The bare "UCL" is scoped to ofc2026,
which is correct: the acronym is shared with Université catholique de Louvain. W2A.37 prints London, and the metadata
gives University College London.

### ASN/Nokia (joint)

W1H.3 / W3A.2 print "ASN/Nokia" in one block. W3A.3 prints "Nokia, Alcatel Submarine Networks". The metadata gives
"Alcatel Submarine Network". A joint is the literal reading. `org_alcatel_submarine_networks` has no parent, so the
registry asserts no ownership. ASN's ownership at the source date is open question Q1.

### imec-Ghent University (joint)

Th3D.4 / Th3F.2 print "IDLab, INTEC, imec-Ghent University". This matches the batch_1 precedent "Ghent
University-imec". The 4 Th3F.3 basis changes are the expected side effect.

### Short-form aliases with header and metadata evidence

- Adtran (ofc2026-scoped): the only bare "Adtran" print in OFC is Tu2F.1, Planegg, DE, and the metadata gives
  Adtran Networks SE. Adtran Networks SE is the 2023 successor name of ADVA (event_adva_rename_adtran_networks_2023).
  Scoping keeps ADTRAN Holdings prints elsewhere unrouted.
- EXFO (ofc2026-scoped): Th4B.6 metadata gives "EXFO Solutions" for the same 2 authors. The org was created from
  that header.
- KIST (ofc2026-scoped): Th2A.6 prints no place; the metadata gives Korea Institute of Science and Technology for 9
  of the 10 authors. The ROR acronym KIST is shared by KR / TZ / RW / MY records, so the scope is needed.
- Similar checks for AUTH, INRS, IRISA, FORTH, FOTON-UMR6082 / Institut FOTON, Artemis, Lab-STICC and "Universidad
  de la Republica": one paper or one group each, place printed, ROR acronym or metadata confirms.

### Time-aware strings

- "Finisar Australia" stays on org_finisar (string names Finisar).
- "Cisco - Acacia Communications" is joint; Acacia keeps its own id.
- "FUJIFILM Business Innovation Corp." is the legal_name of the existing (post-rename) org.
- "Shenzhen Polytechnic University" uses the as-of-source name.
- "California State Polytechnic University, Humboldt" keeps its campus word.
- OFS Fitel is not mapped to Lightera.
- Keithley is brand-level, not Tektronix.

### Supply ROR orgs and no_name_match choices

- ROR orgs: Micro Resist Technology, Mitaka Kohki and Okuno are single same-key records. SUSS MicroTec and Tokyo
  Electron are D271 roots.
- Vigo's ROR record 00qw0ej89 is an orthopaedics company (vigo-ortho.pl), so skipping it is right.
- FLIR: ROR has "FLIR Systems" only as an alias on Teledyne FLIR, so it is printed + no_name_match. Parker
  Corporation: the ROR "Parker" hits are aliases on Parker Hannifin, not a key match, so it is printed +
  no_name_match.
- Every other printed vendor has no same-key active ROR record.

### Header-row sample

The 40 rows (seed 20261023) come from 31 papers: SKL x8, AUTH x3, Fraunhofer HHI x3, Cisco-Acacia x2, BUPT x2,
CableLabs x2, UCL x2 (one full form, one bare), and single rows of 18 other strings. The `show` views were checked where the block was not
self-evident.

### Country mismatches

All 42 rows where the header country differs from the org country are subsidiary_printed or unit_printed brand
mappings: IMEC-NL / IMEC The Netherlands, NI Nokia, Nokia Bell NV, Nokia Canada, Huawei Düsseldorf / Ottawa, Fujitsu
R&D Center Beijing, Corning UK.

## Open questions

1. **ASN ownership:** no local source states Alcatel Submarine Networks' owner at the OFC 2026 date. The joint
   "ASN/Nokia" follows the print. Add an event only from a primary source.
2. **Al-Azhar "Assuit":** W4E.3 prints Al-Azhar University with the place Assuit. ROR has a single Egyptian record
   (Cairo) and no separate Assiut institution, so mapping to 05fnp1145 is right unless the coordinator wants the D301
   campus treatment for branch faculties.
3. **SKL host:** which organization or organizations host the lab needs a primary source (lab or YOFC / China
   Telecom page) before any parent or event is set (W2).
4. **Older batches:** should batches 1-4 (24 decision rows with address text, mostly batch_2) and their merged
   registry notes get the W3 scrub too?
5. **Toptica brand org:** whether to create the brand-level Toptica org now (I1 second step), and which of the two
   Toptica orgs gets `no_name_match`.
