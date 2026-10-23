# Views, org hub and privacy audit (2026-10-23)

Fresh-context audit of `/supply`, `/people`, `/orgs/hub?id=` and the `/orgs` lens counts (DevLog-010 D190-D199), plus a
regression pass over `/explore`, `/components`, `/layout` (gallery and `?id=`) after the data growth (807 components incl.
the `lit` corpus, new platform enum values, `primary_by_class` on the mmi template, DevLog-005 D229a). Privacy boundary
per DevLog-004 (binding).

## Scope and method

- Data: `app/static/data/{components,people,registry,supply}.json` as rebuilt 2026-10-23 00:06 (`generated_on`
  2026-10-23); source tables `data/people/*.csv`, `data/supply/*.csv`, `data/components/*.csv`, `data/registry/*.csv`
  read at 2026-10-23 00:10.
- App: `vite dev` on 127.0.0.1:47731 (free port, started and stopped by the auditor), Playwright with the installed
  `chromium_headless_shell-1234`, viewports 1400x850 and 800x700. 23 routes / states x 2 viewports = 46 screenshots plus
  6 probe screenshots, every one inspected. Screenshots: session scratchpad `views_audit/` (not in the repo).
- Automated per page: console errors, page errors, failed or non-localhost requests, elements with non-zero computed
  border-radius (spinner excepted), horizontal page overflow, page-level vertical scroll.
- Privacy: JSON-level set comparison against the CSVs; rendered-DOM scan (inner text and every attribute value) for all
  674 review person ids, all 1267 withheld observation ids and the 337 review display names that no public person or
  public printed name shares; search-box probes; deep link to a review person id.
- Data spot-checks: 15 supply usage rows, 15 rendered person-timeline points, 12 hub / `/orgs` lens counts, each traced
  to the source CSVs with an independent script (not `build_views.py`).

## Privacy verdict

**Pass for the served app.** No review person, review observation, `data/_local/` content, e-mail address, street
address or phone number reaches `app/static/data/*.json` or any rendered page. No moves, flows or transition arrows are
drawn. Two latent issues outside the served data (findings 1, 2).

| Check | Result |
|---|---|
| `people.json` persons vs `people.csv` `visibility = public` | 6248 = 6248; 0 extra, 0 missing |
| `people.json` observations vs public observations of public persons | 10688 = 10688; 0 extra, 0 missing; 0 field mismatches (person, org, date, source, grade, printed name) on all 10688 |
| Review observations of public persons (12 rows) | withheld |
| Person fields emitted | `id, name, orcid, disambiguator` only (D192); no notes, research_status, aliases, xref, `same_as` |
| Review person ids (674, exact quoted match) in `app/static/data/*.json` | 0 |
| Withheld observation ids (1267) in `app/static/data/*.json` | 0 |
| Review-only display names (337) and review-only printed names (353) in `people.json` | 0 |
| `person_` strings in `registry.json`, `supply.json`, `components.json` | 0 |
| E-mail pattern in all four JSON files | 0 (6 regex hits are "@NEST" unit / "nano@stanford" org names) |
| Street / postal / phone patterns in printed_org, unit, locator | 0 (only telecom-word false positives) |
| `people.json` sources | 1293, each cited by >= 1 public observation; none cited only by withheld rows |
| Aggregates of withheld rows | `counts.persons_all`, `counts.obs_all`, `totals_by_corpus.*.all` only (allowed by D192) |
| `build_views.py` / `app/src` references to `data/_local` | docstrings only; no read |
| Rendered DOM, hubs imec / Intel / TSMC / EPFL with "all N" people expanded, `/people` orgs mode for the same 4 orgs, full persons list (6248 rows after scrolling), `/supply`, `/orgs`, `/components`, `/explore` | 0 review ids, 0 withheld obs ids, 0 review-only names (2 substring hits, "Nai-Yuan Liu" and "Shih-Wei Liu", are public persons whose names contain a review-only name) |
| Search box: 12 review-only names (every 28th of 337) and 3 review ids | 0 rows each (one partial-name query returned a different public person) |
| `/people#p=<review id>` | "Select a person." (no existence signal) |
| Flow / move views | none (timeline = points only, no lines; no org-to-org view) |

## Findings

### 1. privacy (latent, local only) - stale build output holds review rows

- Page: `app/build/data/people.json` (git-ignored build output, 2026-10-22 23:07).
- Reproduction: exact-match the review person ids of the current `people.csv` and the withheld observation ids against
  `app/build/data/people.json`.
- Evidence: 3 person ids and 8 observation ids that are `review` in the current tables are present (persons moved to
  review after that build). `app/static/data/people.json` (00:06) is clean.
- Impact: not deployed (the Pages workflow rebuilds from `app/static/data` in CI), but `vite preview` or a manual upload
  of `app/build/` would serve them.
- Suggested fix: rebuild (`pnpm build`) or let the owner remove `app/build/`; optionally have the privacy test also scan
  `app/build/data/` when it exists.

### 2. privacy (process) - deploy does not run the privacy tests

- Page: `.github/workflows/deploy.yml`.
- Evidence: CI runs `pnpm check`, `pnpm test`, `pnpm build` only. The guards in `tests/test_views.py`
  (`test_no_review_ids_in_committed_views`, `test_people_view_public_only`) run only in a local `pytest`. A commit that
  flips a person to review in `people.csv` without rebuilding `people.json` would deploy the stale view. Also
  `app/static/data/people.json` and `supply.json` are untracked (`??`) at audit time: `/people`, `/supply` and the hub
  people / supply panels need them committed together with `registry.json`.
- Suggested fix: add a CI step `uv run pytest tests/test_views.py -q` (or a node script doing the same set check) before
  the build; commit the four views together.

### 3. bug - Coverage chart collapses at 800 px

- Page: `/people#m=coverage`, 800x700.
- Evidence: the `StackBars` frame (height 320) renders 109 px tall; y title clipped ("bservations (co"), x title
  overlaps the tick labels, a stray grey bar over 2014 (`people-coverage-800.png`). 1400x850 is fine.
- Cause: `.cov` is a flex column inside a pane of ~50 % height; the frame shrinks (`flex-shrink: 1`).
- Suggested fix: `.cov > :global(*) { flex: none; }` (or a grid with `grid-auto-rows: max-content`).

### 4. bug - class list labels overlap on /components below 1100 px

- Page: `/components`, 800x700.
- Evidence: in the 160 px class column, "Free-space emitter (AMO)", "Resonator (single device)", "Phase shifter
  (non-EO)", "Waveguide / platform loss", "Mode converter / MDM" wrap to two lines inside fixed `height: 22px` buttons
  and overprint the next entry (`components-800.png`). New class labels from the data growth made it visible.
- Suggested fix: label span `white-space: nowrap; overflow: hidden; text-overflow: ellipsis` with the full label in
  `data-tip`, or `min-height: 22px; height: auto`.

### 5. bug - exponent labels show spurious digits for float-formatted values

- Page: `/layout?id=cmp_lit_heim2025_vernier_ring` (primary line), gallery and card labels of the same rows.
- Evidence: `q_intrinsic 3.50000e6` (stored `3500000.0`).
- Cause: `sig()` in `app/src/lib/layout/resolve.ts` treats every digit after the decimal point as significant, so
  `3500000.0` gets 6 significant digits. The `lit` corpus stores 35 integer-valued metrics as `N.0`; 6 rows reach the
  exponent path (q_intrinsic / q_loaded of `cmp_lit_heim2025_vernier_ring`, `cmp_lit_heim2025_coil_resonator` x2,
  `cmp_lit_wilson2019_gap_*` x2). Hz and length paths are unaffected (`Number()` strips the zeros).
- Suggested fix: in `sig()`, drop a `\.0+$` tail before counting (and a test); optionally normalise `N.0` in the lit
  distill output.

### 6. bug - hub "supply view" link lands on an empty usage pane for standards- or process-only orgs

- Page: `/orgs/hub?id=org_jedec_solid_state_technology_association` -> "supply view".
- Evidence: opens `/supply#org=...` on the Usage tab; detail reads "unknown: 0 of 0 usage rows", no products, no
  used-in (`supply-from-jedec-hub-1400.png`). The 9 standards are on the Standards tab, which the link does not open.
- Suggested fix: link to `#tab=standards` when the org has standards but no usage rows, `#tab=processes` (with the
  filter prefilled) when it has processes only; drop the leading "unknown:" when type and country are both empty or
  unknown.

### 7. bug - timeline x-axis title clipped

- Page: `/people#p=person_ronald_freund`, 1400x850.
- Evidence: long unmapped printed-org labels on the y axis shrink the plot to ~100 px; the x title reads
  "Observation date (yea" (`people-person2-1400.png`).
- Suggested fix: truncate y tick labels (e.g. 40 chars, full string in the hover card), or put the unit in a shorter
  title ("Date (year)").

### 8. bug (data join) - 528 public observations unmapped, mostly OFC paper-header strings of registry orgs

- Page: `/people` (Coverage note "528 public observations ... map to no registry org"), person timelines, hubs.
- Evidence: 444 of the 528 are `ofc2026` grade A (`p.~1 header`, DevLog-008), 84 grade B. Top strings are plain
  variants of registry orgs: "Fraunhofer Institute for Telecommunications, Heinrich-Hertz-Institut" 34, "UCL (University
  College London)" 25, "Swiss Federal Institute of Technology Lausanne (EPFL)" 19, "Denmarks Tekniske Universitet" 14,
  "University of Padova" 15, "NI Nokia" 12, "Yangtze Optical Fiber and Cable Joint Stock Limited Company (YOFC)" 10.
  Effects: hub and lens people / observation counts for these orgs are low (EPFL hub shows 112 observations; the 19
  EPFL-header rows are not joined), and the per-person "Orgs" count is inflated (Ronald Freund: 5 orgs, 3 of them HHI
  spellings).
- Suggested fix: extend `data/crosswalk/org_crosswalk.csv` with the DevLog-008 header strings (same review rules as the
  OFC program strings), rebuild views. Not a UI change.

### 9. spec deviation - OFC corpus labelled grade B although 4356 public OFC rows are grade A

- Page: `/people` timeline legend and Coverage (legend, panel description, Rules), persons count tooltip.
- Evidence: legend "OFC 2026 program (B)"; Coverage description "OFC 2026 program grade B"; Rules "Grade A: affiliation
  printed in an EO or packaging paper; grade B: OFC 2026 program metadata"; the same page's table shows ofc2026 grade A
  4356, grade B 1514. Grade A OFC points render as circles under a "(B)" legend entry (Ronald Freund, `ofc2026:Th2A.18`).
- Suggested fix: corpus labels without a grade ("OFC 2026"); Rules: A = affiliation printed in the paper (EO, packaging,
  OFC paper header), B = OFC program metadata. D196 symbol = grade already carries the grade.

### 10. spec deviation - "withheld" text does not match the data

- Page: `/people` Coverage Rules and badge tooltip, persons count tooltip.
- Evidence: "observations below grade B are not published" / "the rest belong to persons in the identity review queue or
  below grade B": no observation has a grade below B; the 1267 withheld rows are `visibility = review` (1033 grade A, 234
  grade B). "Persons in the identity review queue ... are not published": per the D94 ruling 2 queued LIN persons stay
  public (their queued observations are withheld).
- Suggested fix: "Observations of persons in the identity review queue, and queued observations, are not published"
  (or similar), no grade clause.

### 11. spec deviation - products exist now but usage rows do not show them

- Page: `/supply` detail "Used in", `/orgs/hub` Supply panel.
- Evidence: `supply.json` has 115 products and 122 usage rows with `product_id` (DevLog-010 inventory still says 198
  usage rows, 0 products; now 337 / 115). The detail lists the vendor's products as a separate list (Keysight 17) and
  the used-in rows never name the instrument model; the hub supply table has no product column. The tooltip "products.csv
  holds no rows yet (vendor/model scanner and datasheet tranches not run)" is shown on every vendor without products and
  is no longer true. D190 asks for category -> vendor -> product / usage -> papers.
- Suggested fix: show `model` on each used-in row and in the hub supply table (join `product_id`), list papers under
  each product in the detail, change the empty-state tooltip to "no product rows for this vendor"; update the
  DevLog-010 inventory.

### 12. spec deviation - 243 public persons listed without any visible evidence

- Page: `/people` Persons list (rows with empty Obs / First / Last), person card "No public observation."
- Evidence: 241 persons are public through a LIN record only (`person_xref` scheme `lin_id`), 2 more hold only withheld
  observations. The app shows the name with no source, locator or reason. Allowed by D94, but every other displayed
  person or value is traceable to a cited source.
- Suggested fix: hide persons with 0 public observations from the list by default (toggle "include lineage-only"), or
  state "public via lineage record (LIN), no affiliation observation published" in the card.

### 13. spec deviation (minor) - hub source count excludes standards and reliability tests

- Page: `/orgs/hub?id=org_jedec_solid_state_technology_association`.
- Evidence: tiles "9 standards", "0 sources"; the Sources panel is absent. Standards are cited by 401 test rows from 72
  PK papers.
- Suggested fix: add the papers of the tests citing the org's standards to the Sources list under lens S (or label the
  tile "sources (components, supply, people, events)").

### 14. convention - category tree stays live on Processes and Standards tabs

- Page: `/supply#tab=processes`, `#tab=standards`.
- Evidence: the A-K tree and its counts (usage rows) stay clickable; selecting a category changes nothing in those tabs.
- Suggested fix: dim / disable the tree outside Usage, or filter processes by the B subtree.

### 15. convention - vendor colour changes with the selected category

- Page: `/supply` chart a.
- Evidence: Keysight is green (slot 6) under All categories and teal (slot 3) under H (`supply-1400.png`,
  `supply-h5-keysight-1400.png`); slots are positions in the alphabetical top-6 of each subtree. Colour still never
  encodes rank, but identity is not stable across selections.
- Suggested fix: acceptable per D194; if stability is wanted, assign slots from the global top vendors first.

### 16. convention - /supply at 800x700 shows only the chart in the main pane

- Page: `/supply`, 800x700.
- Evidence: tree 150 px, main ~270 px, detail 35 %: the 250 px chart fills the main pane, its x labels are cut and the
  vendor table starts below the fold (`supply-800.png`).
- Suggested fix: chart height 160 px below 900 px, or a collapsed chart toggle.

### 17. nit - in-plot legend touches bars

- Page: `/supply#cat=B7`, chart a, 1400x850. The "other vendors" legend entry sits on the 2020 bar top (6 rows).
- Suggested fix: legend to the right of the plot area or `y: 1.0` with a top margin.

### 18. nit - pointer cursor on non-clickable rows

- Page: `/supply#tab=processes` (`.main .t tbody tr { cursor: pointer }` applies; rows have no click action).

### 19. nit - empty search shows a blank table

- Page: `/people` search with no match: "0 / 6248 persons", empty table body, no "no match" row.

### 20. nit - year-only observations stack on one marker

- Page: `/people#p=person_eric_beyne`: 12 observations, 4 visible markers (PK dates are year-only, plotted at mid-year).
  The table lists all 12; a count in the hover card or a small vertical jitter would show the multiplicity.

### 21. nit - "unknown unknown" in the hub meta line

- Page: `/orgs/hub?id=org_jedec_solid_state_technology_association`: type and status both "unknown" without labels.

### 22. nit - MMI crossing drawn with access tapers on one arm only

- Page: `/layout?id=cmp_lit_nevlacsil2020_mmi_te_te`: horizontal arm has both tapers, the orthogonal arm none. Marked
  PARTLY SCHEMATIC and noted; a 4-port crossing would read better with the same tapers on both arms.

### 23. nit - gallery group header wraps raggedly at 800 px

- Page: `/layout`, 800x700, edge_taper group: title, id, counts and primary wrap into three columns.

### 24. nit - inconsistent paging in /people

- Page: `/people` Persons mode loads more on scroll; Organizations mode needs a "show more" button.

## Data spot-checks

| Check | Sample | Result |
|---|---|---|
| Supply usage rows | 15 random rows (seed 23) of `supply.json` vs `product_usage.csv` (all fields) and `sources.csv` year | 15 / 15 match; all 337 ids present both ways; 0 rows without a source year |
| Person timeline points | 15 rendered Plotly points (`gd.data`) of Ya Cheng, Ronald Freund, Eric Beyne vs `affiliation_observations.csv`: source, locator, date -> x, org name (or "printed (unmapped)") -> y, grade -> symbol, corpus -> trace, hover date and grade | 15 / 15 match; point counts equal public CSV rows (18, 32, 12) |
| Hub tiles and `/orgs` lens | 12 orgs (imec, AMF, Intel, TSMC, CMNT, Jinan Jingzheng, JEDEC, Keysight, EPFL, 1Finity, AIM Photonics, BRNC): rendered hub tiles, rendered `/orgs` lens line, `registry.json` `lens`, independent CSV count (fab / facility ids, usage, processes incl. broker, standards body, public obs and persons) | 12 / 12 identical across all four |

## Regression pass (explore, components, layout)

- 0 console / page errors, 0 failed or external requests, 0 elements with non-zero border-radius, no horizontal page
  overflow on all 46 page states; panes scroll internally.
- `/explore`: 807 shown; platform families sum to 807 (Other / unspecified 114 = 62 empty + 47 `other` + 5 `al2o3`); every
  schema platform enum value is in a family or intentionally in Other; corpus filter lists `lit` 253.
- `/layout` gallery: mmi header "excess_loss_db per_component; crossing.mmi: crossing_loss_db per_component" (D229a);
  `/layout?id=cmp_lit_nevlacsil2020_mmi_te_te` primary line `crossing_loss_db (per_component) ~ 0.05 dB`.
- `/components`: 807 components, 3575 values; finding 4 at 800 px only.

## Summary

| Severity | Count | Findings |
|---|---|---|
| privacy | 2 (both latent, not in the served data) | 1, 2 |
| bug | 6 | 3, 4, 5, 6, 7, 8 |
| spec deviation | 5 | 9, 10, 11, 12, 13 |
| convention | 3 | 14, 15, 16 |
| nit | 8 | 17-24 |
| total | 24 | |
