# Org curation batch contract (DevLog-001, task 8)

Goal: map each unmapped OFC 2026 affiliation string in `batch_N/input.csv` to registry organizations, so the crosswalk
reaches >= 90% of OFC author rows with no wrong mappings. A wrong mapping is worse than an unmapped string.

## Inputs (read-only)

- `batch_N/input.csv`: printed, n_rows (OFC author rows), ror_hit_kind / ror_hits (offline ROR hints: `ambiguous_name` =
  several ROR records share the name; `alias_only` = only a ROR alias field matched, review needed), ofc_codes (presentation codes).
- Registry: `data/registry/organizations.csv` (org_id, name, country, ror_id, parent_org_id ...) and
  `data/registry/org_aliases.csv`. Search them before proposing a new org (by key words, abbreviations, native names).
- ROR dump (CC0): `cache/ror/v2.15-2026-10-20-ror-data.csv` (columns `id`, `names.types.ror_display`,
  `names.types.label`, `names.types.alias`, `names.types.acronym`, `locations.geonames_details.country_code`, `types`,
  `relationships`, `established`). Use `grep -i` or a short `uv run python -I` script; do not load it into context whole.
- OFC paper text headers: `../PlayGround/20260320_OFC/extracted_text/<code>-*.md` (sibling repo, read-only). Read only
  the first ~40 lines (title, authors, affiliations with addresses) to disambiguate a string (e.g. which "Soochow
  University", which "Institute of Microelectronics"). Never copy e-mail addresses anywhere. Not open access
  (D172 / D244, DevLog-001 D339): quote only organization, unit, city and country as printed; never a street, building,
  PO box, room or postal code.
- No web access. No edits to any file except your own `batch_N/decisions.csv`.

## Rules

1. Map to an existing org when the string denotes it: a spelling/abbreviation/language variant (`printed_variant`,
   `abbreviation`, `native_name` for romanized native names such as "Sumitomo Denki Kogyo Kabushiki Kaisha" or
   "Nihon Denshin Denwa Kabushiki Kaisha"), a national subsidiary or site of a company (`subsidiary_printed`, mapped to
   the brand-level company org, e.g. "Huawei Technologies Duesseldorf GmbH" -> the Huawei org), or a department / lab /
   state-key-lab / school string of a host org (`unit_printed`, mapped to the most specific host org that exists or
   that you create, e.g. a State Key Lab at XIOPM -> the Xi'an Institute of Optics and Precision Mechanics org).
2. Separate research labs with their own identity that the registry already models separately stay separate (e.g.
   NEC Laboratories America vs NEC Corporation; Nokia Bell Labs vs Nokia). If the registry has no row for such a lab,
   create it with `parent_org_id` = the company org.
3. Time-aware entities are distinct orgs: do not map a renamed or acquired company's old/new name onto the other
   (e.g. Adtran Networks SE is not ADVA; Lightera is not OFS unless the string says OFS). Create the org that the
   string names.
4. A string naming two organizations (e.g. "Ghent University-imec") -> action `joint`, org_id = both ids `;`-separated.
5. New org: prefer an exact ROR record (give `ror_id`, name = ROR display name without a trailing " (Country)"
   disambiguator, `name_basis` ror, country and type from ROR). Otherwise `name_basis` printed, name = the cleanest
   printed form seen in your batch (expand nothing, abbreviate nothing, keep legal suffixes out only if a variant in the
   batch prints the name without one). Country only when the ROR record, the registry, or the paper header address
   states it (say which in `evidence`). `org_type` from the ROR record or the name's own words (University,
   Institute, Laboratory, Inc./Ltd./GmbH/Corporation -> company); otherwise `unknown`. Never classify from memory.
6. `skip` when unresolvable (ambiguous with no header evidence, not an organization, garbled). Give the reason.
7. Every row needs `evidence`: registry row id, ROR id, or `ofc2026:<code> p.1 affiliation` (the header block you
   used), plus a short why. Evidence quoting an OFC 2026 header (restricted corpus, D172 / D244) carries only
   organization, unit, city and country as printed; never a street, building, PO box, room or postal code. Same rule
   for registry notes, override entries, resolution files and DevLog text (D339).
8. Variants of one org across rows must all point to the same org_id; if you create a new org, reuse its proposed id
   for all its variants in your batch. Proposed new ids: `org_<lowercase ascii words joined by _>` from the name,
   legal suffix dropped (e.g. `org_zte`, `org_kddi_research`).
9. No emoji. ISO dates. Do not invent names, countries, parents or types.

## Output: `batch_N/decisions.csv` (UTF-8, header, RFC 4180 quoting), one row per input string

`printed,n_rows,action,org_id,alias_type,new_name,name_basis,ror_id,org_type,country,parent_org_id,evidence,notes`

- action: `alias` (existing org) | `new_org` (org_id is a new id; new_name, name_basis, org_type required; ror_id,
  country, parent_org_id when known) | `joint` | `skip`.
- alias_type: printed_variant | abbreviation | native_name | legal_name | short_name | brand | subsidiary_printed |
  unit_printed | joint_printed (empty for skip). For `new_org` rows give the alias_type of the printed string relative
  to the new org (printed_variant when it differs from new_name, empty when identical).
- When several input rows create the same new org, fill new_name/name_basis/org_type/... on every one of them
  identically.

Final message: counts per action, rows covered, and any decisions you were unsure about (listed for review).
