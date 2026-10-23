# Review contract for supply scanner batches (DevLog-003 D328)

Brief for a reviewer of one batch `data/_staging/supply/products/<batch>/` (full_02 .. full_13). Decisions cited
are in [DevLog-003](../../../../DevLog/DevLog-003-p2-supply-chain.md).

## Boundaries

- Write ONLY `<batch>/review.csv`. Do not edit `candidates.csv`, `sources.csv`, anything in `data/` outside your
  `review.csv`, `config/`, the registry, `org_requests.csv`, or other batches. No network, no git.
- The build (products, usage rows, org requests, merge) is run later by the supply owner.
- Never invent a vendor, a model or a page. A fact needs the vendor (or a model that identifies it, see basis) and the
  use printed in the paper.

## Inputs and tools (read-only)

| What | Command |
|---|---|
| Papers of the batch (also those with 0 candidates) | `<batch>/sources.csv` |
| Candidates with sentence context | `uv run python scripts/scan_vendor_models.py --print-batch <batch>` |
| Full cached text of a paper (page markers kept) | `uv run python scripts/scan_vendor_models.py --print-source <source_id>` |
| Rights of a source | `data/registry/sources.csv` column `redistribution` |
| Facts already in the atlas (EO imports, merged batches) | `data/supply/product_usage.csv` (by `source_id`) |
| Category tree | `data/schema/supply_categories.yaml` |
| Self-check (writes nothing shared) | `uv run python scripts/build_supply_staging.py <batch> --check-review` |

## review.csv format (v2)

Header, exactly: `source_id,vendor_printed,org_id,model,product_line,category_id,role,basis,locator,stated_spec,notes,cand_ids,reviewed_on,line_kind,reason`

Two kinds of line:

- `line_kind=fact`: one usage fact = (source, vendor org, role, product). `cand_ids` = every candidate id that points
  at this fact (`;`-separated; empty when the scanner missed it). `reason` empty. All columns below apply.
- `line_kind=verdict`: candidates that are not a fact line of their own. Fill only `source_id`, `cand_ids`,
  `reason`, `reviewed_on` (and `notes` if useful). `reason` is one of:
  - true: `covered` (fact already in `data/supply`), `no_vendor` (item used but vendor neither printed nor inferable),
    `dup` (same fact as a fact line; prefer listing the id on the fact line instead);
  - false: `affiliation`, `acknowledgement` (thanks only), `funding`, `coi`, `own_org` (the authors' company as
    designer or test site), `collaboration`, `citation` (others' work), `generic` (mention without stated use),
    `word_fragment`, `not_this_work` (planned / future), `other` (explain in notes).

Every candidate of `candidates.csv` must get a verdict: listed on one or more fact lines (one sentence can carry two
products) or on one verdict line; never on a fact line and a false verdict line.

Fact line columns:

| Column | Rule |
|---|---|
| `vendor_printed` | the vendor exactly as printed on the cited page (brand forms allowed: Loctite, EPO-TEK). Vendor as of the source (D6, D207): Agilent stays Agilent, Finisar stays Finisar, HP stays HP |
| `org_id` | leave empty: the build resolves the printed name through the registry and the gazetteer. Set it only when the printed form is a known registry org under another name (e.g. HP -> `org_hewlett_packard`) |
| `model` | the model string as printed (keep its hyphens / spaces; one model per line); empty for vendor-only facts |
| `product_line` | only when the family name is printed on a cited page (D326): DCA-X, UXR, Infinity, Picoprobe; never from catalogue knowledge |
| `category_id`, `role` | see the table below; a top-level id (`H`, `F`, ...) only when no subcategory fits, with a note starting `category:` |
| `basis` | `stated` (vendor printed with the item) or `inferred_from_model` (vendor not printed; only when the candidate has `infer_ok=true`); otherwise no fact, verdict `no_vendor` |
| `locator` | page of the statement: `p.N` for eo / pk / lit, `p.~N` or `pNA` for ofc2026 (the candidate's locator is right); several pages `p.4; p.9`; a section name may follow (`p.7 Methods`) |
| `stated_spec` | short paraphrase of what the paper states about the use, <= 120 characters |
| `notes` | printed forms that differ, category reason, acknowledgement source, etc. |
| `reviewed_on` | ISO date of your review |

Product identity (D290, D317, D326): the build derives the product from vendor + canonical model (case, spaces,
hyphens folded) and strips a leading vendor / brand token and a leading Model / Type / Series word; write the printed
model and let the build normalize. Different suffixes are different products (N4372 vs N4372E, EBPG 5200 vs 5200+).
A printed number that differs from the catalogue form only by a missing suffix letter (Keysight N1000 vs N1000A) is
not that model: use the printed family as a family-level product (model = product_line = DCA-X) when the family is
printed, else the printed model. Software: model = product name, release in notes (MARC2023.4 -> MARC).

## What is a fact (verdict true)

The paper states that the vendor's item or service was used, bought, supplied, evaluated or fabricated for the
reported work (D207): setup instruments, fab tools and consumables, wafers and materials, fibers / FAUs / connectors,
packaging materials and tools, lasers / modules, software, foundries, shared facilities.

- Acknowledgements (D291): true when they state supply (equipment lent, materials or samples provided, devices
  fabricated or processed somewhere); thanks for help, discussion or support are false.
- Facilities (D299a, D316): a registry facility where work was performed or devices fabricated -> `facility_use`,
  category `B7`, never fabrication. "A portion of this work was performed at <facility>" counts.
- Co-author companies (D296): true when they supplied an item (fabrication, laser dies); false (`own_org`) when they
  are only designer or test site.
- Items evaluated and rejected in the work count (state the outcome in stated_spec).
- Comparisons with a commercial product that was measured in the same setup count; a product only cited from
  others' work does not (`citation`).
- `unlisted` candidates (D294, D299c) are proposals of unknown vendors: true only under the same rules.

## Category and role (D54, D207, D296)

| Item | role | category |
|---|---|---|
| Foundry / institute fabricating the devices | `fabrication` (`mpw_access` for brokers, `post_processing` for BEOL material services) | `B1`-`B5`, `B6` broker |
| Shared cleanroom (registry type facility) | `facility_use` | `B7` |
| Wafers, substrates, glass panels hosting waveguides | `wafer_supply` | `A1`-`A3`, `A6`, `A7`, `B2` |
| Materials (EO organics, 2D, polymer waveguide materials) | `material_supply` | `A` (note), `A4`, `A5`, `E*` |
| Packaging materials (adhesives, underfill, laminates, solder, TIM, glass cores) | `packaging_material` | `E1`-`E8` (glass cores of packages `E8`) |
| Assembly equipment (bonders, alignment, dispensers, molding, reflow, plating) | `assembly_tool` | `F1`-`F9` |
| Fab tools, resists, metrology (also SEM / X-ray CT in packaging flows) | `fab_tool` | `G1`-`G7` |
| Measurement instruments; lasers used as light sources of a measurement | `test_instrument` | `H1`-`H17` (`H` + note for RF power sensors, thermometers, IR cameras, prism couplers) |
| Commercial laser die / module built into the reported system | `laser_source` | `C` (note) / `C1`-`C7` |
| Fibers, fiber arrays, connectors, splicers | `fiber_component` | `D1`-`D5` |
| Software | `software` | `J` |
| Standards / implementation agreements used in the method (OIF 400ZR, R24) | `standard_reference` | `K` (bodies, MSAs) or `I1` |
| Network / transport equipment in the setup (line systems, ROADMs, routers, OCS; R4) | `test_instrument` | `H` with note `category: network / transport equipment in setup` |
| Pluggables, transceivers, transponders, CDM / ICR modules in the setup (R4) | `laser_source` | `C` with note `category: commercial module in setup` |

Cross-batch rulings R1-R25 (`COORD_RULINGS.md`) apply: e.g. compute / IT gear and datasets are not entered (R4), bare
"Lumerical" is `no_vendor` (R22), Thermo Scientific / Thermo Fisher are not FEI (R21), discrete electronic dies and
measurement services without a product are not entered (R23, R25).

## Rights (D53, D297)

Restricted sources (`redistribution = restricted_local_only`: all pk and ofc2026, many eo and lit): stated_spec and
notes are paraphrases, no quotation marks, at most about five consecutive words of the source (instrument-type names
are fine). Never paste sentences from any source into the repo.

## Recall (required)

For every paper in `sources.csv`, read the methods / experimental / fabrication / measurement-setup sections, figure
captions of setups, and acknowledgements (use `--print-source`). Add a fact line with empty `cand_ids` for every
fact the scanner missed (vendors not in the gazetteer, models printed without a vendor match, facilities).

## Self-check and hand-off

1. `uv run python scripts/build_supply_staging.py <batch> --check-review` must end with `CHECK OK`. It checks: header,
   every candidate has a verdict and none has two different ones, cand_ids exist, vendor (basis stated), model and product_line printed on
   the cited pages, category / role / basis / locator form, stated_spec length, quotation marks in restricted lines,
   and validates the would-be rows on a temporary copy. It writes no log files, batch files or org requests.
2. Report to the coordinator: papers read, fact lines (with / without candidates), verdict counts by reason, held
   vendors listed by the check, anything unclear.
