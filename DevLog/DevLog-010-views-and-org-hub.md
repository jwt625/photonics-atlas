# DevLog-010: Supply-chain view, people view, org hub

Date: 2026-10-22. Decisions here are D190-D199. Plan source: [DevLog-000](DevLog-000-plan.md) P2 "Views", P3 "Views",
P4 "Org hub page"; inputs [DevLog-003](DevLog-003-p2-supply-chain.md) (supply tables, D51-D60, read only),
[DevLog-004](DevLog-004-p3-people.md) (people tables, D61-D70, D90-D97, D210; privacy binding), deferred UI-audit nits
13-22 of [the 2026-10-22 UI audit](audits/2026-10-22-ui-audit-explore-layout.md) (DevLog-005 D220-D229 fixed 1-12, 23).

## Request (2026-10-22, coordinator for Wentao)

1. Supply-chain view `/supply`: category tree A-K -> vendor -> product / usage -> used-in-papers from `data/supply/*.csv`
   and `data/schema/supply_categories.yaml`; vendor share by category and year where the data supports it.
2. People view `/people`: person list + person timeline (dated public observations, grade, source, locator), org ->
   people with observation counts, coverage panel (observations per corpus / grade / year). Privacy binding (DevLog-004):
   only `visibility = public` persons and observations; nothing from `data/_local/`; no transition arrows, org-to-org
   flows or exchange networks built from local derived transitions. A flow view built honestly from public observations
   alone is proposed here and put to the coordinator, not built.
3. Org hub: one org across all lenses (registry facts, components fabricated / facility, supply rows, public people and
   observation counts, sources) with cross-links to the EO and packaging atlas sites.
4. UI-audit nits 13-22: fix the clear ones (18 gap card order, 20 log ticks, other one-liners); list the rest.

Constraints: `build_views.py` deterministic, extended tests, a test that fails if any review person / observation id is
emitted; no edits to `data/*` source tables or to DevLog-003; no git writes; no network beyond localhost.

## Data inventory (2026-10-22 22:30, read from the CSVs)

| Table | Rows | Notes |
|---|---|---|
| `supply/product_usage.csv` | 198 | 66 orgs, 127 sources (EO only); facility_use / B7 75, wafer_supply A2.1 42, fabrication B1 25, wafer_supply A2.2 14, fabrication B 10, material_supply A4 8, rest <= 3 each; source years 2017-2026 |
| `supply/products.csv`, `product_specs.csv` | 0 | header only (scanner / datasheet tranches not run) |
| `supply/foundry_processes.csv` | 39 | 21 orgs |
| `supply/standards.csv` | 24 | 22 with `body_org_id` |
| `supply/reliability_tests.csv` | 401 | 72 PK papers |
| `people/people.csv` | 6922 | public 6245, review 677 |
| `people/affiliation_observations.csv` | 10832 | public 9710, review 1122; ofc2026 5547 (grade B), eo 2880 + pk 2405 (grade A); 0 public observations of a review person |
| `components/components.csv` | 762 | `fab_org_ids` on 378, `facility_org_ids` on 121 |

Update 2026-10-23 (views as rebuilt by the coordinator 2026-10-23 00:16, `generated_on` 2026-10-23): `product_usage`
337 rows (138 orgs, 142 sources; 122 rows with `product_id`), `products` 115, `product_specs` 0, processes 39,
standards 24, tests 401; persons public 6248 / 6922; observations public 10691 / 11958 (eo 2582 / 2880, ofc2026
5873 / 6673, pk 2236 / 2405; OFC rows are grade A for paper-header rows, DevLog-008, and B for program metadata).

## Decisions (D190-D199)

| # | Decision | Rationale |
|---|---|---|
| D190 | Routes: `/supply`, `/people`, `/orgs/hub?id=<org_id>` (query parameter read client-side, like `/layout?id=`; one prerendered shell instead of ~930 pages). `/orgs` detail pane gets per-lens counts and a "hub" link; nav gains Supply and People | static adapter, `ssr = false`; same pattern as the layout viewer |
| D191 | New generated views: `app/static/data/supply.json` (category tree, usage, processes, standards, tests, products / specs as-is, cited-source metadata) and `people.json` (public persons, public observations in column arrays, cited-source metadata, per-corpus totals). `registry.json` orgs gain `lens` counts (`cmp_fab`, `cmp_fac`, `sup`, `proc`, `std`, `ppl`, `obs`; non-zero keys only; people counts from public rows only). `components.json` unchanged (it already carries `fab_org_ids` / `facility_org_ids`). Joins for the hub run client-side over the loaded views | one generated file per lens; no duplicated join file to keep in sync |
| D192 | People privacy (binding, DevLog-004): `people.json` holds only persons with `people.visibility = public` and observations with `visibility = public` whose person is public. Person fields whitelisted: `person_id`, `display_name`, `orcid`, `disambiguator` (curated, D93). Not emitted: person notes, research_status, aliases, xref rows (LIN ids, name keys). `build_views.py` never opens `data/_local/`. Only aggregate totals of withheld rows are emitted (per corpus: all vs public observation counts) | review queue, name-only candidates and transitions are local-only; counts are not person data |
| D193 | No flow / move view in this tranche. Proposal for the coordinator (not built): an org co-affiliation matrix from public observations alone, counting persons with public observations at both orgs (any date, no order, no arrow, labelled "co-affiliation, not a move"), threshold >= 2 persons. Open question: is that acceptable given that identity rests on D63 merges (grade X xref) | DevLog-004 privacy; ordered moves need the local transition derivation |
| D194 | Supply vendor share = count of `product_usage` rows (one row per source x org x role fact, D53) per vendor within the selected category subtree, by source year (`sources.year`). Labelled "usage rows", never "market share". Vendors coloured by a fixed categorical slot order (the six vendors with most rows in the subtree get slots in alphabetical order, the rest grey "other"); colour encodes identity, not rank | the only quantity the data supports; small counts |
| D195 | Product level: shown only where `products.csv` / `product_specs.csv` rows exist (none on 2026-10-22: the tree reads "0 products"); no product names inferred from `stated_spec` | no invented rows |
| D196 | Person timeline: one point per public observation at `active_on` (YYYY plotted at mid-year, marked "year only" in the card), y = organization; symbol = grade (A circle, B square); colour = corpus (eo / pk / ofc2026). Points, never intervals or connecting lines (D67, D183); `present_address` rows are points with their role in the card | publication affiliation is a dated point |
| D197 | Coverage panel: public observations per corpus x year (stacked bars, colour = corpus) and a corpus x grade table with public / all totals | data-only plot |
| D198 | Cross-links: EO atlas `https://outside5sigma.com/eo-modulator-atlas/table#q=<EO printed org>` (token search over paper fields incl. org names, so it may match more papers: labelled "search"); packaging atlas `https://outside5sigma.com/advanced-packaging-atlas/table#o=<PK org name>` (exact org filter on the PK canonical name). Only crosswalk strings with >= 1 row are linked. Site URLs: PK README; EO deploy workflow BASE_PATH `/eo-modulator-atlas` and the owner's site project list. Paper-level links (`#q=<native_id>`) for `eo:` / `pk:` sources | both siblings read filters from the hash |
| D199 | UI-audit nits 13-22: disposition in the table below | owner: fix the clear ones, list the rest |
| D199a | (views audit 2026-10-23 #1, #2) Privacy gate in CI: `.github/workflows/deploy.yml` runs `uv run --extra dev pytest -q tests/test_views.py` (astral-sh/setup-uv, Python 3.12) before the app steps; the workflow is otherwise unchanged. `test_views.py` reads committed files only (no sibling input repos: checked in a copy of the git-tracked files plus the new files, with `PHOTONICS_ATLAS_INPUTS_ROOT` pointing at a missing directory: 8 passed). The on-disk privacy test also scans `app/build/data/*.json` when present, so a stale local build fails it; `app/build` rebuilt | a commit that flips a person to review without rebuilding the views must not deploy |
| D199b | (audit #9, #10) The grade belongs to the row, not the corpus: corpus labels carry no grade (EO atlas paper, Packaging paper, OFC 2026); the timeline legend adds grade A (circle) / grade B (square) entries; rules: A = affiliation printed in the paper (EO, packaging, OFC paper header), B = OFC program metadata; withheld = observations of persons in the identity review queue and queued observations (no grade clause) | OFC header rows are grade A (DevLog-008) |
| D199c | (audit #11, #14) Supply: products listed per vendor with their usage-row count (click filters the used-in list), each used-in row and each hub supply row names the product model (and product line); empty state "no product rows for this vendor"; the category tree is dimmed and inert outside the Usage tab | D190 category -> vendor -> product / usage -> papers |
| D199d | (audit #12; amends D192) `people.json` person fields add `lin_grade` and `lin_sources` (the person's `person_xref` `lin_id` row: grade and the LIN source ids of its notes) for public persons only; the cited LIN sources join the sources map (title, year, venue, url, access; never source notes). The person pane shows "Public through the lineage (LIN) record, grade X" with the source links; the list shows "LIN" in the Obs column for persons without a public observation. Needs a views rebuild to reach the served JSON (verified with a fresh in-memory build served through a Playwright route) | every displayed person traceable to a cited source |
| D199e | (audit #6, #13, #21) Hub: "supply view" opens the tab that holds the org's rows (usage -> `#org=`, else standards / processes with the filter prefilled through a new `q` hash parameter); the Sources list adds, under lens S, the papers whose reliability tests cite a standard of the org; type / status "unknown" read "type unknown" / "status unknown"; the supply detail meta line drops unknown type / country | a link must land on the org's rows |
| D199f | (audit #3, #4, #5, #7, #16-#20, #23, #24) Layout and format fixes: Coverage chart keeps its height (flex none); /components class labels ellipsised (full label in the tooltip); `sig()` ignores a `.0` tail (3500000.0 -> 3.5e6); timeline y labels truncated to 40 characters (full string in the hover), x title "Date (year)"; supply chart 170 px and no legend below 900 px, 300 px with the legend above the plot area otherwise, vendor colour swatches in the vendor table; pointer cursor only on clickable tables; "No person / organization matches" rows; multiplicity line in the timeline hover ("N observations at this point"); gallery group headers wrap per item; Organizations mode loads more on scroll like Persons | audit findings |

## TODO

- [x] 1. Read DevLog-000/003/004/005, UI audit, app structure, sibling deep-link formats; write this plan.
- [x] 2. `build_views.py`: `build_supply()`, `build_people_view()`, registry `lens` counts; deterministic ordering.
- [x] 3. `tests/test_views.py`: privacy (no review person / observation id in any emitted JSON, in memory and on disk; mutation: a person flipped to review disappears), no `_local` access, determinism, row counts.
- [x] 4. App: loaders (`supply.svelte.ts`, `people.svelte.ts`), `/supply`, `/people`, `/orgs/hub`, `/orgs` pane links, nav.
- [x] 5. Nits 18, 20 and other one-liners; vitest for new logic.
- [x] 6. Run `build_views.py`; ruff, mypy, pytest, validate_db; pnpm check, test, build.
- [x] 7. Dev server on a free uncommon port; Playwright screenshots 1400x850 and 800x700; inspect each; stop server.
- [x] 8. Progress, sizes, open questions here.
- [ ] 9. Views rebuild after the parallel streams land (components 762 -> 809 lit merges, people visibility changes and `same_as` column in flight at 22:50); coordinator.
- [ ] 10. Fresh-context audit of the three views and the privacy boundary (coordinator).
- [ ] 11. Coordinator decision on D193 (co-affiliation matrix) and the open questions below.
- [x] 12. Views audit 2026-10-23 (`audits/2026-10-23-views-orghub-privacy-audit.md`, 24 findings): fixes D199a-D199f; status table below.
- [ ] 13. Views rebuild for D199d (LIN fields) once the registry round lands (coordinator).

## UI-audit nits 13-22 (D199)

| # | Status | Change / reason left open |
|---|---|---|
| 13 | partly fixed | single-bus note now also for rings whose label states add-drop / two-bus (`scene.ts` ringTop; M1E.6, montifiore2026). Open: Th1D.6 taper-coupled ring still draws a bus (needs a coupler-kind rule, not a one-liner) |
| 14 | open | Th1D.6 rib heuristic (`isRib` matches "ridge" in labels) and cladding "upper:" clause parsing: scene heuristics with knock-on effects on other components; needs its own check over all rib rows |
| 15 | fixed | panel j header tag "colour = class family" (tooltip explains it differs from the page legend) |
| 16 | open | pinned-card placement needs card measurement after render and stacking offsets (`ScatterChart.place`) |
| 17 | partly fixed | pinned cards no longer show the "click a point to pin" hint (`PointTip pinned`). Open: shortening the c / d / f descriptions to one line (content choice for the owner; the rule text would move to the badge tooltip) |
| 18 | fixed | gallery cards and gaps in one role-ordered list (`gallery.ts` `items`); vitest |
| 19 | fixed | `split_ratio_pct` is a dc companion; companions are now returned also when the primary metric has no row, and a gallery card without a primary value shows the first companion (larocque2024 dc: "not reported  split_ratio ~12 %"); vitest |
| 20 | fixed | log axes: dtick `D2` (labels 1 / 2 / 5) when the positive values span <= 3 decades, one label per decade beyond (`logDtick` in `explore/logic.ts`, used for x and y of every scatter panel); vitest |
| 21 | open | `/components#id` deep link: scroll the values table to the component and let the detail table wrap / scroll; needs a scroll-into-view effect plus layout change of the detail pane |
| 22 | open (data) | source year vs venue (churaev2023 2021 vs Nat. Commun. 14 = 2023; datta2024 2022 vs Optica 11 = 2024): registry `sources.year` check, not a UI change; belongs to the registry / source build stream |

## Views audit 2026-10-23: finding status

| # | Status | Note |
|---|---|---|
| 1, 2 | fixed | D199a |
| 3, 4, 5, 7 | fixed | D199f |
| 6 | fixed | D199e |
| 8 | not touched | unmapped OFC header org strings: separate org round (registry / crosswalk) |
| 9, 10 | fixed | D199b |
| 11, 14 | fixed | D199c |
| 12 | fixed (code); data after rebuild | D199d |
| 13, 21 | fixed | D199e |
| 15 | kept | vendor colour slots are per selected subtree (D194); stable global slots would need a fixed vendor list |
| 16, 17, 18, 19, 20, 23, 24 | fixed | D199f |
| 22 | open | MMI crossing tapers on one arm: layout scene (DevLog-005 scope) |

## Results (2026-10-22 22:33 build)

| File | Bytes | Content |
|---|---|---|
| `app/static/data/supply.json` | 401171 | 86 categories, 198 usage, 39 processes, 24 standards, 401 tests, 0 products, 0 specs, 199 cited sources |
| `app/static/data/people.json` | 2636424 (gzip ~0.44 MB) | 6245 public persons, 9710 public observations (eo 2582 / 2880, ofc2026 4908 / 5547, pk 2220 / 2405), cited-source metadata |
| `app/static/data/registry.json` | 632399 (was 610554) | unchanged except `lens` per org (751 orgs with >= 1 lens count) |
| `app/static/data/components.json` | 1981605 | unchanged content (only `generated_on`) |

- Routes: `/supply` (tabs Usage / Processes / Standards; tree A-K with rolled-up counts; vendor share chart a; vendor
  table; detail: products, used-in papers with locator, stated spec, EO atlas link), `/people` (Persons list with
  sort / search / incremental rendering, timeline + observation table; Organizations -> people; Coverage chart a +
  corpus x grade table), `/orgs/hub?id=` (meta + sibling-atlas links, lens tiles, components, supply, people,
  registry, sources). `/orgs` pane: lens counts and hub link. Nav: Supply, People. Header count hidden below 1050 px
  (the two new nav items no longer fit at 800 px).
- Files: `scripts/build_views.py` (new `build_supply`, `public_people`, `build_people_view`, `lens_counts`),
  `tests/test_views.py` (8 tests), `app/src/lib/{supply.svelte.ts, people.svelte.ts, views.ts, views.test.ts,
  StackBars.svelte}`, `app/src/routes/{supply, people, orgs/hub}/+page.svelte`; edits: `routes/+layout.svelte`,
  `routes/orgs/+page.svelte`, `lib/types.ts`, `lib/components.svelte.ts` (types), `lib/explore/{colors.ts,
  logic.ts, logic.test.ts, ScatterChart.svelte, PointTip.svelte, YearStack.svelte}`, `lib/layout/{gallery.ts,
  resolve.ts, scene.ts, layout.test.ts}`, `routes/layout/+page.svelte`.

## Progress

- 2026-10-22 22:35: plan written before code.
- 22:33-22:45: build functions, tests, views built (the coordinator's 22:27 build backed up first in the private
  scratch folder; `components.json` content identical, `registry.json` identical except `lens`), app routes.
- 22:40-22:52: dev server on 127.0.0.1:47613 (free; stopped), Playwright headless shell 1234: 15 pages x 2 viewports
  (30 screenshots, session scratchpad `views/`), every one inspected; 0 console / page errors, 0 elements with a
  non-zero border-radius (spinner excepted), no horizontal page overflow. Fixed after inspection: standards / test-type
  tables overlapped (split into scroll cells), standards detail table cramped (source moved to the row tooltip),
  selected category not expanded in the tree, missing spaces before "(additional)" / "atlas" in the observation table,
  header count wrapping at 800 px, companion text wrapping on the dc gallery card.
- 22:46-22:53 verification: `ruff check .` clean, `ruff format --check` clean on the owned Python files, `mypy` (81
  files) clean, `pytest -q` 244 passed (a run during other streams' edits showed 4 transient failures in
  `test_ofc_headers.py` / `test_people.py`, gone on rerun), `tests/test_views.py` 8 passed, `validate_db.py` 0
  errors, 16 warnings; `pnpm check` 0 errors 0 warnings, `pnpm test` 54 passed, `pnpm build` ok (`build/orgs/hub.html`
  prerendered).
- 22:50: the emitted views are already behind the source tables, which other streams are writing (components.csv
  762 -> 809 rows; people.csv public persons 6245 -> 6251 and a new `same_as` column): `supply.json` in sync,
  `people.json`, `registry.json`, `components.json` need a rebuild once those streams land (TODO 9). The on-disk
  privacy test re-checks the committed JSON against the current people tables on every pytest run, so a person moved
  to review after a build fails the suite until the views are rebuilt.

- 2026-10-23 00:30-00:50: views audit fixes D199a-D199f. Checks: `pnpm check` 0 errors 0 warnings, `pnpm test` 57
  passed, `pnpm build` ok (app/build rebuilt from the 00:16 views), `pytest -q tests/test_views.py` 8 passed (also in a
  tracked-files-only copy without sibling repos), `ruff check .` clean, `mypy` clean on the owned files (2 errors in
  `scripts/build_supply_staging.py`, another stream's untracked file). Dev server 127.0.0.1:47613 (stopped); 16
  screenshots of the fixed cases (session scratchpad `views_fix/`, people.json served from a fresh in-memory build),
  each inspected; 0 console errors, 0 rounded elements, no horizontal overflow. Found by inspection and fixed: product
  line glued to the model, supply meta punctuation, horizontal legend squeezing the 800 px chart (legend hidden there,
  swatches in the table), legend rows shrinking the 1400 px chart (300 px).

## Open questions (for the coordinator)

1. D193: build the co-affiliation matrix (persons with public observations at both orgs, no order, no arrows) or not?
   Identity for it rests on D63 merges (xref grade X).
2. `people.json` is 2.6 MB raw (0.44 MB gzip). Acceptable, or split per-person loading (e.g. one JSON per initial)?
3. Hub joins are per org only; units (children) are linked, not rolled up. Roll up children (e.g. Intel + Intel
   Silicon Photonics Solutions Group) with a toggle?
4. EO atlas cross-link is a token search (`#q=`), which can match more papers than the org's; an exact org filter
   would need an EO-side hash parameter (EO repo change, not done).
