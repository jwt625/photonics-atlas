# Audit: org registry round 5 (DevLog-001 D270-D279)

2026-10-22, fresh-context auditor. Read-only except this file. No network; ROR = pinned local dump
`cache/ror/v2.15-2026-10-20-ror-data.csv`. Diffs against `git show HEAD:<path>`.

Scope checked: `data/_staging/org_curation/batch_7/decisions.csv` (92 rows), registry diff (`organizations.csv` +75 rows
and 1 changed, `org_aliases.csv` +20 rows), `config/registry_corrections.yaml` (D275 block), the resolution files
(`data/_staging/supply/org_requests.csv`, `data/_staging/people/ofc_headers/org_requests_resolution.csv`,
`data/_staging/people/intel_pilot/orgs_resolution.csv`, `data/_staging/components/lit_0[1-6]/org_resolution.csv`), the six
`coord2.yaml` files against the paper texts (`references/<id>/text.md`) and the merged `data/components/components.csv`.
Every printed vendor string was located in its cached source text (EO / PK `references/<id>/text.md` of the sibling
atlases, lit texts here, OFC extracted text); every ROR id was looked up in the dump (display, labels, aliases, status,
type, country, established, parents, children); every new org was checked for an existing registry org with the same
normalized name, alias key or ROR id (none found).

## Counts

| Object | n | ok | imprecise | wrong |
|---|---|---|---|---|
| New orgs | 75 | 71 | 4 (C2N, CNST, Qaleido, Schott) | 0 |
| Alias rows written (8 alias decisions + 12 from new_org rows) | 20 | 18 | 2 (SENJU, MUSASHI) | 0 |
| Alias decisions with no row (same key: ThorLabs, ANSYS, Comsol) | 3 | 3 | 0 | 0 |
| Skips (TFS, CNSE, BWRC, Nanostructures Lab, CMAM, LioniX BV) | 6 | 6 | 0 | 0 |
| Registry correction (D275 CNR) | 1 | 0 | 0 | 1 |
| coord2 component assignments (rows) | 26 | 26 | 0 | 0 |
| Resolution rows: supply vendor rows resolved in round 5 | 56 | 56 | 0 | 0 |
| Resolution rows: OFC header requests | 10 | 10 | 0 | 0 |
| Resolution rows: Intel pilot | 4 | 4 | 0 | 0 |
| Resolution rows: lit org_resolution.csv (6 files) | 27 | 26 | 1 (lit_03 CNST printed column) | 0 |

Runs:
- `uv run python scripts/build_org_crosswalk.py --dry-run`: EO 284/284 strings, PK 181/181, LIN 172/172, OFC 729/734
  strings, 6043/6055 rows (0.998); P0 acceptance PASS. A fresh `build()` compared in memory against
  `data/crosswalk/org_crosswalk.csv`: 1371 / 1371 rows, 0 differences (confirms "0 rows changed").
- `uv run python scripts/validate_db.py`: errors 0, warnings 15 (14 "status acquired without an org event" on lineage orgs,
  1 eo:powell2024 year; none from round 5).
- DevLog numbers reproduced: 1001 orgs, 481 with ROR id, 803 with country, 48 with supply_roles, 416 aliases; new orgs by
  name_basis printed 44 / ror 28 / cited_source 3; coord2 26 rows (fab 20, facility 13), merged values equal the yaml.

## Findings

### W1 (wrong) D275 does not keep the bare name "National Research Council" out of matching

Evidence: `orgmatch.Matcher.match` has a fourth route, ROR display / label lookup, used by `build_org_crosswalk.py`,
`add_ror_orgs.py`, `build_supply_seed.py` and `ofc_headers.map_org`. `load_matcher` registers `by_ror` for every org
with a ror_id, including no_name_match orgs. ROR 04zaypm56 has display "National Research Council" (labels
"Consiglio Nazionale delle Ricerche", "National Research Council"); `ror.lookup("National Research Council")` returns three
active records (04zaypm56 IT, 035rrps97 RO, 03bjn0010 LK), of which only the IT one is on a registry org, so the route
returns it uniquely. Test with the current registry:

- `m.match("National Research Council", c)` -> `(['org_national_research_council'], 'ror')` for eo, pk, lit, ofc2026.
- `ofc_headers.map_org` also tries the variant with the parenthetical removed, so a header "National Research Council
  (NRC), Ottawa" would route to Italy's CNR the same way.

So the D275 statement "maps through its aliases" / "kept out of name matching" is not what the code does; before D275 the
string mapped by name, now it maps by ROR, same target. Impact today: 0 rows (no "National Research Council" string in the
crosswalk, the OFC header staging or the first 3000 characters of any OFC text). The correction yaml itself is applied
correctly (no_name_match true, notes).

Proposed correction (code, `src/photonics_atlas/orgmatch.py`, `load_matcher`); checked: none of the 13 current
`match_basis = ror` crosswalk rows points to a no_name_match org, so the crosswalk stays unchanged:

```
        if o["ror_id"] and o.get("no_name_match") != "true":
            m.by_ror.setdefault(o["ror_id"], o["org_id"])
```

plus a DevLog note under D275: "no_name_match orgs are excluded from the ROR display / label route as well (their ROR
display name is their name)". Re-test: "National Research Council" -> unmapped; "Consiglio Nazionale delle Ricerche" ->
alias (row with basis ror_record exists).

### I1 (imprecise) C2N named by the French ROR display name; D274 text says English label

Evidence: ROR 00zay3w86 display "Centre de Nanosciences et de Nanotechnologies", labels French + English "Centre for
Nanoscience and Nanotechnology", acronym C2N, type facility. Registry name = the French display; D274 reads "C2N by its
exact ROR English label". The identification (printed form minus "(C2N)" equals the English label) is exact; the name
choice follows the `add_ror_orgs.py` convention (ROR display; precedents org_fonctions_optiques_pour_les_technologies_de_linformation,
org_istituto_di_fotonica_e_nanotecnologie) but not D16 ("own preferred English name"). Type research_institute (P0
audit 6.4 mapping), parent org_cnrs (printed; the only one of the three ROR parents in the registry): ok.

Proposed correction (wording only, keeps the convention): D274 "C2N: identified by the English label of ROR 00zay3w86
(printed form minus the acronym), named by the ROR display name (registry convention for ROR-named orgs)". Alternative if
D16 should win: `registry_corrections.yaml` `org_centre_de_nanosciences_et_de_nanotechnologies: {name: Centre for
Nanoscience and Nanotechnology, why: 'D16 English name; ROR en label'}` plus a native_name alias for the French display
(the id stays, ids are immutable).

### I2 (imprecise) CNST founded_on 1901 is NIST's founding year

Evidence: ROR 00tbs6p91 "Center for Nanoscale Science and Technology" `established` 1901, parent NIST 05xpvk416; the
registry copied it. 1901 is not credible for a NIST center (the record carries the parent's year); the dump states nothing
else, and the real founding year is not in any local source (not looked up: no network). Identification itself (NIST
prefix + acronym CNST under NIST; printed "Nanosacle Science and Nanotechnology" sic, alias kept as printed) is a curated
non-exact identification, acceptable as documented. Type government_lab (ROR government) and parent: ok.

Proposed correction: `org_center_for_nanoscale_science_and_technology: {founded_on: '', why: 'ROR established 1901 is the
parent NIST founding year; CNST founding not sourced'}` (or keep with a note if empty-overrides are not supported).

### I3 (imprecise) Qaleido Photonics org_type startup from the disclosures paragraph

Evidence: lit:ye2023 p.12 "Z. Y., H. J., Z. H. and J. Liu are co-founders of Qaleido Photonics, a start-up that is
developing ...". D17 restricts new-org types to the printed name's own words or the ROR record (otherwise unknown); the
schema rule (a) allows "a cited source". The type is stated in the source, but not by the D17 route. Country CN from the
p.1 address (D16 amendment): ok. The parallel case ALUVIA Photonics (garciablanco2025 p.11 "co-founder of ALUVIA
Photonics", no type word) stays unknown: consistent.

Proposed correction: either `org_qaleido_photonics: {org_type: unknown, why: 'D17: type word not in the name'}` or a
D17 amendment "a type word stated about the org in the cited source (e.g. 'a start-up') counts, quoted in notes".
Coordinator choice (Q4).

### I4 (imprecise) Schott supply_roles wafer_supplier is stale after D296

Evidence: the only review line (`data/_staging/supply/products/pilot_01/review.csv`, pk:tcpmt.2025.3533388 p.2,
"Borofloat 33", "460 um glass core of the thermal and electrical test vehicles") is now category E8 packaging_material per
D296 (review file modified 23:29, after round 5). D272 maps E -> materials_supplier. The registry row says wafer_supplier
and its notes / the decision evidence say "A7 wafer_supply". All other 47 vendor orgs' supply_roles equal the D272 mapping
of their current review lines (scripted check).

Proposed correction: `org_schott: {supply_roles: materials_supplier, notes: <replace 'A7 wafer_supply' by 'E8
packaging_material (D296)'>, why: 'D272 mapping of the D296 category'}`.

### I5 (imprecise) SENJU / MUSASHI aliases are reviewer short forms, not printed strings

Evidence: pk:ectc51687.2025.00027 prints "SENJU METAL INDUSTRY Co., Ltd." (p.3) and "MUSASHI  ENGENEERING.,  INC." (p.2);
the bare "SENJU" / "MUSASHI" are never printed alone. Schema: alias = "exact printed or official variant". The aliases
exist only because the review's vendor_printed column holds a shortened form. pk scope limits the harm. Same pattern, no
alias written: "Nordson" (printed "Nordson Advanced Technology", p.3), "KITAGAWA SEIKI", "Sakura Seiki" (those map by
name key anyway).

Proposed correction: set the review lines' vendor_printed to the printed strings ("SENJU METAL INDUSTRY Co., Ltd." maps by
name to org_senju_metal_industry; "MUSASHI ENGENEERING., INC." to org_musashi_engeneering), then drop the two pk-scoped
short_name alias rows (registry_corrections alias removal) or keep them with notes "not printed standalone; reviewer form".

### I6 (imprecise) lit_03 org_resolution.csv printed column silently corrected

Evidence: row printed "NIST Center for Nanoscale Science and Technology (CNST)"; meng2023 p.13 prints "NIST Center for
Nanosacle Science and Nanotechnology (CNST)" (the alias row keeps the printed form). Proposed: printed column = the
printed form.

### Checked ok (summary of evidence)

- ROR-named vendor orgs (D271): all 19 ids exist, active, parentless roots whose display minus " (Country)" has the
  printed key; country / type / established / website from the record; same-key children or inactive records as noted
  (e.g. Thorlabs DE 00p9kb710 child; Keyence 02s7aa368 withdrawn; Comsol US 00asd2k77 / GB 056h76p35 both parentless ->
  no ROR id). Hitachi High-Tech parent org_hitachi = ROR parent 02exqgm79; Panasonic Connect has no ROR parent. Amonics
  display "Amonics (China)" with country HK: registry HK, ok. Santec / Samco named from the ROR label (the dump's label cell
  is "Santec Corporation, Santec Corporation (Japan)", read correctly).
- Printed vendor orgs (D273): every printed string located at the stated page (e.g. "AT Microwaves AT-BBLF-0020-3022B"
  didier2026 p.7; "Amo- nics, AEDFA-40" mao2024 p.7; "Physik Instrumente (PI) SE &  Co. KG" bankwitz2026 p.19; "SHF
  Communication Technolo- gies AG" cai2025 p.6; "[114] Lumerical Inc." tiberi2025 p.20; "MARC2023.4, MSC  Software"
  ectc51687 p.3; "A FEI Quanta SEM" eptc59621 p.3). Types: company exactly where a legal suffix is printed. No country
  printed for any of them in the cited text (bankwitz2026 p.19 and cai2025 p.6 print none). "No exact ROR record" holds for
  every printed org; near records not attached: Lumerical Solutions (Canada) 035gbh774 (key differs), LioniX (Netherlands)
  00k8nkz10 (key differs), OSRAM (Germany) 01c0x3431, MSC Software x3 and FEI x4 withdrawn, Dow Corning 053ne5n46 withdrawn.
- Active Technologies: not printed in didier2026 (p.8 prints "ARB Rider AWG-7204" only); review basis inferred_from_model
  (D55 allows it); org from ROR 03zp7nb85 (IT); the decision notes say so. ok.
- Component / affiliation orgs: Technion (ROR alias "Technion", curated), Twente, NRC Canada, UConn (021nv2831 withdrawn),
  UPenn, Chiral Photonics, Honeywell (root of 10 country records): exact ROR. Facility orgs named as printed with printed
  hosts as parents (GWNIC -> GWU, MNFU -> Technion, SIMIT platform -> SIMIT, SMDL -> ShanghaiTech, MIT MTL -> MIT);
  Micronova no parent / country (host not printed). Type facility for printed fab-centre names matches the registry
  precedent (12 printed facility orgs at HEAD, e.g. Center for Nanoscale Characterization & Devices, Marvell
  Nanofabrication Laboratory). MESA+ (research_institute, NL, parent Twente), CMST (academic_lab,
  parent Ghent, imec noted), ALUVIA (unknown, NL), LioniX International BV (company, NL), Grace (company, CN), Dow Corning
  Corporation (company, US, Midland MI printed), ams OSRAM International GmbH (company, DE, Regensburg printed): as printed.
- ams AG: printed "ams AG, Premstätten, Austria" (nevlacsil2020 p.1); ROR 03vz6gs79 "AMS
  (Austria)", alias Austriamicrosystems AG, active, AT, 5 country children; D200 conditions met; no_name_match + lit-scoped
  alias ("ams" / "ams AG" map only in lit, tested). See Q3 for the time-aware caveat.
- Intel pilot orgs: printed strings in `observations_proposed.csv` ("Numonyx, Limited", deposited affiliation 2008-12;
  "Agility Communications"; "Gemfire Corporation"; UPenn ROR exact).
- Aliases: OFC headers verified in the extracted text: Tu2C.6 "Beijing Univ. of Posts and Telecommunications (BUPT),
  Beijing"; M2K.2 "Optical valley laboratory, Wuhan, Hubei" (ROR 01mf47c71 Optics Valley Laboratory, label 湖北光谷实验室, the
  only such record); Th3E.4 "UPC, Barcelona", "WEST Aquila S.r.l., L'Aquila", "TIM, Torino"; Th4C.2 "Technical
  University of Berlin, Germany"; M1F.7 "University of California at Davis, Davis, CA"; M1B.2 "University of Chinese
  Academy of Science, Beijing" (singular, as printed); M3F.4 "Now with ... University of Connecticut, Storrs". None
  is a rename or acquisition (TIM is a brand of Telecom Italia, ofc2026-scoped). Bare acronyms scoped (TIM, UPC, PI, SHF,
  FEI). MenloSystems: curated join of "MenloSys- tems" (valdez2023a p.4).
- Skips: TFS expansion is printed nowhere (the review note's "Thermo Fisher Scientific" is reviewer knowledge, correctly not
  used); CNSE (kim2019 p.1 affiliation only), BWRC (kim2019 p.12 "continued support"), Nanostructures Lab (mehta2016 p.7,
  no host; mehta2016 rows already fab org_mit), CMAM (garciablanco2025 p.11 RBS beam time), LioniX BV (hosseini2015 p.1;
  p.3 "fabricated using the standard TriPleX technology" is passive, D80b): all consistent with D42 / D72 / D80.
- coord2 (26 rows), each against the text:
  - ronn2019 (7 rows, fab C2N, facility Micronova): p.9 "X.L., C.R. and W.Z contributed to the design and fabrication of
    the waveguides" (Leroux, Alonso-Ramos, Zhang: affiliation 2 = C2N) -> D80b; p.9 "thank Micronova Nanofabrication Centre
    for providing the facilities" -> D42 / D80c.
  - mu2026 LD (fab ams OSRAM International): p.4 "InGaN laser diodes were fabricated by ams OSRAM [40]"; the only ams OSRAM
    entity printed is the p.1 affiliation "ams OSRAM International GmbH, Regensburg".
  - dangel2013 on-Si (fab Dow Corning): p.7 "the waveguides on Si were manufactured by wafer-scale spin coating and UV
    photolithography patterning"; Fig. 7 caption "(a) UV photolithography-based mask exposure at 365 nm, performed at DCC".
    Two-step reading, as ruled by the lit_02 audit.
  - heim2025 coil (fab Honeywell, borderline): p.16 "Karl Nelson of Honeywell for help fabricating the coil resonator" ->
    D84b borderline with note.
  - oz2023 (2 rows, facility MNFU): p.19 "The devices were fabricated at the Micro-Nano Fabrication Unit at Technion"
    (passive: facility only, fab stays empty, D80b).
  - meng2023 (3 rows, facility GWNIC): p.13 "performed in part at the George Washington University Nanofabrication and
    Imaging Center (GWNIC)", p.11 heater "fabricated in the nanofabrication and imaging center at George Washington
    University"; CNST thin-film analysis not a facility id (D42).
  - yue2026 (facility SIMIT platform + SMDL): p.16 "The sample fabrication is supported by SIMIT material-device and
    characterization platform and ShanghaiTech Material and Device Lab (SMDL)" -> D80c.
  - nevlacsil2020 (6 rows, fab ams AG): p.6 "fabricated by ams AG on their SiN photonic platform".
  - ye2023 (4 rows, fab Qaleido): p.12 "Z. Y., H. J. and Z. H. developed the fabrication process and fabricated the
    samples", all affiliation 1 "Qaleido Photonics, Hangzhou" (p.1) -> D80b.
- Supply org_requests: the 56 vendor rows resolved in round 5 point to the right orgs. The file now has 93 rows, 79
  resolved / 14 open: the 13 open rows besides TFS (Eravant, Evatec, Graphene Platform, Moorfield, Vigo, Gel-Pak,
  Pasternack, Voltcraft, AKROMETRIX, AtaiTec, FLIR, Pactech, Rogers) were appended at 23:30 by the supply audit recall,
  after round 5; the DevLog counts ("79 / 80", "TFS stays open") describe the 23:20 state and are not wrong.

## Open questions

1. bock2010: p.6 "While we used electron beam lithography to fabricate our structures" is a D72 authors-fabricated
   statement. Authors: 7 NRC Canada only, Bock NRC + U Ottawa, Hall U Ottawa only. Rule: org_national_research_council_canada
   as fab (borderline, the fabricating authors are not named) or keep empty (D277 "no ruling")?
2. Bare-name routing of time-aware vendor orgs: "Lumerical" (key of "Lumerical Inc.") and "Allied" (generic word) match by
   name in every corpus and year. A 2024+ source printing "Lumerical" would route to Lumerical Inc. rather than Ansys,
   against D207 "vendor as of the source". Apply the FEI / D201 pattern (no_name_match + eo-scoped alias) to org_lumerical
   and org_allied?
3. ams AG carries ROR 03vz6gs79, whose record represents the current group (5 country children, alias Austriamicrosystems
   AG; current name not in the dump). If a renamed successor org is ever added (D20), the ROR id belongs on one of the two;
   keep it on the 2020 name or drop it? Also its display "AMS" is a bare 3-letter key that D27 bars from automatic matching
   (here curated with the printed Premstätten address, so allowed).
4. Qaleido type (I3): amend D17 or set unknown?
5. ams OSRAM International GmbH has a D296 review line C1 laser_source (co-author company as supplier) but no
   supply_roles: D272 has no mapping for C; component_vendor?
6. Out of scope, noticed: the ROR adapter splits label / alias cells on "; " only, so comma-joined variants inside one
   language group stay one string (e.g. "National Research Council Canada, National Research Council of Canada");
   "National Research Council of Canada" therefore does not match its ROR record. Splitting is ambiguous for names that
   contain commas ("Senju Metal Industry Co., Ltd."), so any fix needs care.
