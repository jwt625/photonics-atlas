# DevLog-005: Explore panel and component layout viewer

Date: 2026-10-20. Builds on DevLog-002 (component atlas, D30-D50, D71-D84). Decisions here are D100-D112 (D85-D99 are
taken or reserved by other DevLogs).

## Request (2026-10-20, Wentao)

1. Hide the crosswalk coverage panel on the dashboard (internal workflow info). Done 2026-10-20 (commit 046e961).
2. Tables did not scroll. Root cause: the page grids of `/orgs` and `/components` had no bounded row, so the scroll
   container grew to the full table height (38,005 px on `/components`) inside a `main` with `overflow: hidden`. Fix:
   `grid-template-rows: minmax(0, 1fr)` on the page grid and `min-height: 0` on its panes; verified in Chrome
   (headless) by wheel-scrolling every pane at 1400 x 850 and 800 x 700. Done (commit 046e961).
3. An Explore panel like the EO modulator and advanced packaging atlases.
4. More detailed per-class information and hero / typical components, so that a front-end layout viewer can draw the
   actual components.

## Decisions

| id | decision | reason |
|---|---|---|
| D100 | Explore page `/explore` follows the sibling atlases: filter side panel (class, platform family, basis, corpus, year) and a grid of lettered panels (letter + one-line description in the tooltip, `plotted / total` badge with the omitted breakdown, lin / log toggles, hover card with component, source, locator, basis; click pins). Plotly (`plotly.js-dist-min`, lazy-loaded), the same `Plot` / `Frame` / `ScatterChart` / `TopBars` structure and colour rules (validated categorical palette, colour = platform family, never rank). Data only: no captions with takeaways, absolute units, no titles beyond axis titles | consistency with the two sibling atlases; his plot rules |
| D101 | Explore panels (first set): (a) fiber-chip coupler loss per coupler vs wavelength, GC vs edge symbol; (b) GC loss per coupler vs 1-dB bandwidth; (c) edge-coupler loss per facet vs chip MFD; (d) propagation loss by platform (strip, log y); (e) ring intrinsic Q vs radius; (f) transition loss by platform; (g) WDM insertion loss vs channel spacing; (h) PD bandwidth vs responsivity; (i) laser output power vs threshold; (j) components by class and year (stacked); (k) components per fab org (top bars); (l) class x platform counts (heat map). A point needs both values from the same component and compatible conditions (same wavelength / band when both carry one); simulated / design values drawn as diamonds, bounds as arrows; omitted counts reported per panel | the P1 views planned in DevLog-000, restricted to pairs the data can support |
| D102 | Layout geometry lives in the long-format metric table like every other value (no geometry side table): role-specific geometry parameters are added to the registry so a drawing never has to guess which width is which (MMI body vs access waveguide, ring vs bus, heater vs waveguide, upper vs lower taper tip, Ge absorber vs Si waveguide) | one validated table, one locator / basis model; ambiguous generic names cannot drive a to-scale drawing |
| D103 | Layout templates (`data/schema/component_layouts.yaml`): one per drawable family, each listing the subtypes it serves, the parameters it draws in the top view and in the cross-section, and which of them are required for a to-scale drawing. First set (12): gc_1d, edge_taper, transition_bilayer, waveguide_xsec, ring_bus, mmi, dc, y_branch, awg, ge_pd, heater_ps, ridge_laser | covers 397 of the 554 component rows (71.7 %, by subtype on 2026-10-20) |
| D104 | Viewer honesty rule: every drawn dimension comes from a metric row (value, basis, locator on hover). A dimension the source does not report is drawn schematically (dashed outline, label "not reported", proportion fixed by the template relative to a reported neighbour) and never shown as a number. Design values and measured (SEM / AFM) values are labelled by basis. No source figure, image or traced outline is reproduced | never invent numbers; rights (most sources are not open-licence) |
| D105 | Showcase table `data/components/component_showcase.csv` (component_id, template, role hero / typical, criterion, rationale, selected_on): per template up to 2 `typical` (a foundry / PDK or MPW component with measured performance, or the median performer of its subtype when >= 5 rows exist) and up to 2 `hero` (best measured value of the template's primary metric that also reports enough geometry for a to-scale top view), across at least two platforms where the data allow. Criterion and rank are recorded at selection time | reproducible selection; heroes without geometry cannot be drawn |
| D106 | Geometry extraction for showcase components (and opportunistically every component of the same paper): all template dimensions from text, tables and figure annotations. Figure dimensions only when the figure labels them (`extracted_from_figure`, reading uncertainty in notes); never measured off a micrograph or scale bar. Design dimensions `design_target`, SEM / AFM-measured `measured`. For showcase rows, rule 2 of the skill (do not re-enter EO geometry columns) is relaxed: the cross-section values may restate the EO row when verified at the paper locator, with a cross-note | a drawing needs the full stack; double counting does not arise for geometry |
| D107 | Primary metric per template (for hero ranking): gc_1d insertion_loss_db per_coupler; edge_taper insertion_loss_db per_facet; transition_bilayer transition_loss_db; waveguide_xsec prop_loss_db_per_cm; ring_bus q_intrinsic; mmi excess_loss_db; dc imbalance_db / excess_loss_db; y_branch excess_loss_db; awg insertion_loss_db + crosstalk_adjacent_db; ge_pd responsivity_a_per_w with bw3db_ghz; heater_ps p_pi_mw; ridge_laser output_power (dBm / mW) with linewidth_hz | one comparable number per template; ties broken by geometry completeness |
| D108 | Viewer placement: a "Layout" section in the component detail panel (`/components`) when the component's class maps to a template, plus `/layout?id=<component_id>` for a full-size view with top view, cross-section, dimension table and scale bar. SVG, to scale, dark theme, sharp corners, hover tooltips | stays inside the component atlas workflow; deep-linkable |
| D109 | Batches for the geometry pass are grouped by template family (couplers: gc_1d, edge_taper, transition_bilayer, waveguide_xsec; passives: ring_bus, mmi, dc, y_branch, awg; actives: ge_pd, heater_ps, ridge_laser). Output is a replayable `geometry.yaml` per staging batch (after patch / sweep / gapfill / addendum), plus showcase rows; then a fresh-context audit per family | same replayable patch model as D50 / D83h |
| D110 | Per-class detail: each template's parameter list doubles as the class's "detail spec"; the geometry pass also enters missing performance values of the template's primary metric for the showcase components | "more detailed info per class" with the same contract |
| D111 | (geometry-pass rulings) Registry additions: lower_width_nm, overlay_slab_thickness_um, subwavelength_period_nm (W4B.6 m12 repointed: its 500 nm is the transverse SWG period, not the grating period), heater_thickness_nm, heater_offset_um; templates updated. heater_length_um only when the paper states the heater length: a stated phase-section length stays length_um and the heater length is drawn as "not reported" (actives pass rows dropped). Unit rescaling keeps D82d (derived, printed value in notes). Angles printed from the chip normal are converted to the registry's angle-to-film-plane convention as derived with the printed value in notes (larocque2024 35 deg -> 55 deg). A component reported only with simulated performance is not a showcase `typical` (boynton2020 MMI) | geometry pass reports |
| D112 | Templates that stay without a hero or typical row (no source reports the required dimensions with a measured primary metric): dc hero, y_branch, awg hero, gc_1d SOI hero; the gallery shows these gaps instead of filling them | honesty rule D104 |

## Registry additions (D102), contract v5

Geometry parameters (kind geometry): `box_thickness_um`, `cladding_thickness_um` (all classes); `layer2_thickness_nm`,
`lower_tip_width_nm` (inter-layer structures); `overlay_width_um`, `overlay_thickness_um` (SSC overlay waveguide);
`grating_length_um`, `grating_width_um`; `bus_width_nm`, `coupling_length_um`; `mmi_width_um`, `mmi_length_um`,
`port_width_um`, `n_inputs`, `n_outputs`; `fpr_length_um`, `arm_length_increment_um`; `absorber_length_um`,
`absorber_width_um`, `absorber_thickness_nm`; `heater_length_um`, `heater_width_um`; `ridge_width_um`. Widened:
`pitch_um` (splitter, wdm, mode_converter: port pitch), `min_bend_radius_um` (splitter, resonator, wdm),
`fill_factor` (reflector, laser), `taper_length_um` (splitter, crossing), `pitch_um` also crossing and amplifier, `period_nm` (amplifier).

## TODO

- [x] Dashboard crosswalk panel hidden; table / pane scrolling fixed and verified (D-none, commit 046e961).
- [x] DevLog-005 plan; registry additions; `component_layouts.yaml`; showcase table schema.
- [ ] Explore page (subagent, D100-D101), screenshots, fresh-context UI audit.
- [ ] Layout viewer (subagent, D103-D104, D108) on the existing geometry, then on the geometry pass output.
- [x] Geometry pass: 3 family batches (D105-D107, D109-D110), showcase selection (35 rows), applied as geometry.yaml in 22 batches.
- [ ] Fresh-context audits of the geometry pass (couplers; passives + actives).
- [ ] Views rebuild, validator, tests, app check / build, screenshots; commit and push; update README.

## Progress

- 2026-10-20 16:55: feedback items 1-2 fixed and pushed; plan written.
- 2026-10-20 18:40: geometry pass done (couplers 16 showcase / 81 rows + 9 edits; passives 9 / 32 + 15; actives 10 / 34 + 35 edits after dropping 4 heater-length rows); D111 registry additions; combined per batch as geometry.yaml, no id collisions.
