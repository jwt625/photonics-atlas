# UI audit: Explore page and component layout viewer (2026-10-22)

Fresh-context audit of `/explore`, `/layout` (gallery and `?id=`), and the Layout section of `/components` against
DevLog-005 (D100-D113), `data/schema/component_layouts.yaml`, `data/components/component_showcase.csv`, and the
owner's UI conventions. Read-only: no code or data changed.

## Method

- Vite dev server on 127.0.0.1:47391 (stopped after the audit); Playwright Chromium headless shell; viewports
  1400 x 850 and 800 x 700. Screenshots are in the session scratchpad `ui_audit/` folder (not committed); file names
  are cited below.
- Data audited: `app/static/data/components.json` as of 2026-10-22 (generated_on 2026-10-20; 554 components, 1977
  metric rows, 34 showcase rows). It matches `component_metrics.csv` (1977 rows, 0 differences in value / unit /
  basis / locator / parameter / scope) and the 12 templates of `component_layouts.yaml`.
- Explore: all 12 panels at both sizes, scrolled; badges and omitted breakdowns; hover cards on panels a-i; pin /
  unpin; lin / log toggles (b), GHz / nm toggle (g); filters class, platform family, measured only, year, empty state.
- Layout: gallery at both sizes; 21 component pages covering all 12 templates (incl. fully unreported cases);
  `/components#<id>` Layout section for 3 components; invalid id; mark tooltips; true scale / expanded toggle.
- Programmatic checks: every plotted point (270 across panels a-i) traced to a CSV row with the same component,
  parameter and value (dBm converted): 0 mismatches. Every drawn dimension label with a tooltip on the 21 pages (127)
  matched to a CSV row by parameter, value, unit, basis and locator: 0 mismatches. No "not reported" label contains a
  digit. No element on `/explore`, `/layout`, `/components` has a non-zero computed border-radius. No console errors
  or page errors on any page.

## Findings

### 1. bug - ridge_laser cross-section draws Si-waveguide rows as III-V layers

- Page: `/layout?id=cmp_ofc2026_m1g3_qd_dfb_memristor` (heterogeneous QD III-V/Si DFB).
- Reproduction: open the page; the cross-section labels a 300 nm "III-V active layer" and a 170 nm III-V ridge
  height under the 4 um mesa.
- Evidence: `layout_ofc2026_m1g3_qd_dfb_memristor.png`; rows `cmp_ofc2026_m1g3_qd_dfb_memristor-m7`
  (core_thickness_nm 300, notes "Si waveguide height") and `-m8` (etch_depth_nm 170, notes "Si rib etch depth").
  `laserSection()` in `app/src/lib/layout/scene.ts` always maps core_thickness_nm to the active layer and
  etch_depth_nm to the ridge height, while its own note says "Si waveguide below the III-V not drawn". This is the
  generic-name ambiguity D102 was meant to prevent.
- Suggested fix: for `laser.heterogeneous` do not draw core_thickness_nm / etch_depth_nm as III-V layers; either draw
  them on a Si waveguide layer below the III-V or add role-specific registry parameters (active / III-V thickness) and
  repoint rows. Check the other heterogeneous rows (`cmp_ofc2026_w4e5_membrane_sel_la70um-*` core_thickness_nm 220,
  "InP membrane thickness") under the same rule.

### 2. bug - edge_taper typical card shows a simulated value although measured rows exist

- Page: `/layout` gallery, edge_taper row, card "O-band SiN inverted-taper edge coupler ... PIC100G"; also the
  primary line of `/layout?id=cmp_ofc2026_tu2d4_sin_edge_coupler`.
- Evidence: `layout_gallery_1400x850.png` shows "< 0.15 dB simulated". Rows: `cmp_ofc2026_tu2d4_sin_edge_coupler-m4`
  (insertion_loss_db lt 0.15, simulated, per_facet) is shown; `-m1` (lt 0.7, measured, per_coupler) and `-m2` (lt 0.6,
  measured, per_coupler) are the basis of the showcase row ("below 0.7 dB TE / 0.6 dB TM"). Cause: `primaryMetric()`
  in `resolve.ts` returns the best strict-scope row of any basis before it looks at measured rows of another scope.
  This is the only showcase row affected (checked over all 34).
- Suggested fix: order the passes measured + template scope, then measured + any scope (scope printed), then
  non-measured + template scope, then the rest.

### 3. bug - transition cross-section location contradicts the top view

- Page: `/layout?id=cmp_churaev2023_ln_taper_transition`, `/layout?id=cmp_wu2025_vac_si_sin`.
- Reproduction: the cross-section is titled "layer stack at the lower-layer input", but the upper layer is drawn at
  its full width_nm. In the top view the upper taper starts at its tip at that position.
- Evidence: `layout_churaev2023_ln_taper_transition.png` (LN drawn 10000 nm wide over the SiN; row
  `cmp_churaev2023_ln_taper_transition-m7`, "LiNbO3 taper final width (upper layer)"; the tip is `-m3`, 500 nm);
  wu2025 draws the SiN at 1000 nm (`cmp_wu2025_vac_si_sin-m5`, "width after the taper") instead of the 350 nm tip
  (`-m3`).
- Suggested fix: at the lower-layer input draw the upper layer at tip_width_nm (dashed when not reported). Or move
  the section to the upper-layer output (upper = width_nm, lower = lower_tip_width_nm) and retitle it.

### 4. bug - SSC cross-section puts the cladding under the overlay and fills unlabelled height

- Page: `/layout?id=cmp_li2026aa_ssc` (edge_taper hero).
- Evidence: `layout_li2026aa_ssc.png`. Row `cmp_li2026aa_ssc-m25` cladding_thickness_um 2, condition "protective
  PECVD SiO2 over the SiON SSC". The drawing measures it from the LN core top (0.3 to 2.3 um, inside the 4.2 um SiON
  overlay `-m17`). `xsecStack()` then fills the cladding solid up to the overlay top (`cladTop = max(t + clad, top)`),
  so a 4.2 um band appears with only 2 um labelled. Two issues: the reference surface is wrong for an overlay SSC,
  and the drawn extent is not backed by a row (D104).
- Suggested fix: when an overlay is drawn, stack the cladding above the overlay top. In general, never fill cladding
  beyond the labelled thickness; draw any extension dashed as not reported.

### 5. spec deviation (D104) - fully unreported views claim TRUE SCALE and carry a scale bar

- Pages: `/layout?id=cmp_ofc2026_tu2d3_gc_1d_si` top view (23 of 23 shapes schematic, 5 um bar);
  `/layout?id=cmp_kieninger2020_mmi` top view (9 of 9 schematic; MMI length falls back to an absolute 40 um; bars
  x 10 um / y 1 um); `/layout?id=cmp_li2025b_y_splitter` (0 of 9 reported; cross-section "TRUE SCALE" with a 500 nm
  bar); `/layout?id=cmp_ofc2026_w1b3_soa_dfb_1p8mm` cross-section (ridge falls back to 2 um, TRUE SCALE). Gallery
  thumbnails repeat the bars (gc_1d typical cards show "5 um").
- Evidence: `layout_ofc2026_tu2d3_gc_1d_si.png`, `layout_kieninger2020_mmi.png`, `layout_li2025b_y_splitter.png`,
  `layout_gallery_1400x850.png`.
- Why: D104 sets schematic sizes "relative to a reported neighbour". With no reported neighbour, `scene.ts` uses
  absolute constants (period 0.6 um, MMI 40 um, laser 500 um, absorber 20 um, core 0.22 um). With a scale bar these
  constants read as real sizes, so an implied number is shown.
- Suggested fix: when the main body of a view has no reported length, set `schematic: true` (badge "SCHEMATIC, NOT TO
  SCALE", no scale bar), as the AWG scene already does. Apply the same rule to gallery thumbnails.

### 6. spec deviation (D104) - heater lateral offset assumed 0 without a not-reported mark

- Page: `/layout?id=cmp_liu2026d_tops_or` (heater_ps typical).
- Evidence: `layout_liu2026d_tops_or.png`. The heater is drawn centred over the waveguide. The showcase rationale
  says the heater is "beside the arm, lateral spacing not stated", and heater_offset_um is a template xsec parameter.
  `xsecStack()` draws the offset mark only when `hx != 0`, so the assumption is invisible (the table does list it as
  not reported).
- Suggested fix: when heater_offset_um is not reported, draw a dashed "not reported" offset mark, or a dashed ghost
  heater beside the core.

### 7. spec deviation (D112) - "gc_1d SOI hero" gap not shown in the gallery

- Page: `/layout` gallery, gc_1d row.
- Evidence: `layout_gallery_1400x850.png`. D112 lists "gc_1d SOI hero" as a gap the gallery must show. Both gc_1d
  heroes are LT / LN at 532 nm, and `gallery.ts` computes gaps per role only, so no gap card appears.
- Suggested fix: allow platform-qualified gaps (for example a `gaps` list per template in `component_layouts.yaml`)
  and render "no SOI hero: no qualifying source".

### 8. spec deviation (D101) - panel a split into two sub-panels, not recorded

- Page: `/explore` panel a.
- Evidence: `explore_1400x850.png`. D101(a) specifies one panel with a GC vs edge symbol. The implementation uses
  stacked grating / edge sub-panels coloured by platform. This is a sensible choice, but DevLog-005 records only the
  panel c change.
- Suggested fix: record the decision in DevLog-005 (no code change needed).

### 9. convention - panel a edge y-title says "per facet" but accepts per_coupler rows; a and c disagree

- Page: `/explore` panels a (edge sub-panel) and c.
- Evidence: A1 uses `IL_COUPLER` (scopes per_coupler, per_facet, loopback_half) under the title "Loss per facet
  (dB)". `cmp_ofc2026_tu2j5_ec_10mode` (1.1 dB at 1550.8 nm) and `cmp_ofc2026_tu2j5_ec_5mode` (1.9 dB at 1560.5 nm)
  are plotted only from per_coupler rows. Panel c (`IL_FACET`) excludes them and `cmp_wu2025_sin_edge_coupler`
  (badge 46/58). Panel b also uses `IL_COUPLER` while its description says "per_coupler or loopback_half" (no GC has
  a per_facet row today, so this is latent).
- Suggested fix: use `IL_FACET` for the edge sub-panel (or retitle it "Loss per coupler / facet"), and give panel b a
  GC spec without per_facet.

### 10. nit - Explore hover card prints raw unit codes

- Page: `/explore` panel e hover (and every card with um or dimensionless units).
- Evidence: `explore_pin_e.png`: "Radius 50 um", "Intrinsic Q ~ 112000 1" (row `cmp_datta2024_bare_sin_ring-m1`,
  unit "1"). The layout viewer renders "µm" and drops "1".
- Suggested fix: reuse `unitLabel()` from `resolve.ts` in `PointTip.svelte`.

### 11. nit - unformatted large numbers and missing statistic on cards

- Pages: `/layout` gallery ring_bus heroes; primary lines.
- Evidence: `layout_gallery_1400x850_s2.png` / gallery JSON. Th1D.6 shows "566000000". M1D.4 shows "> 40000000",
  which is the median row `cmp_ofc2026_m1d4_ull_sin_ring-m2` (statistic median), with no statistic shown; Explore
  panel e plots its `-m1` (> 30 M). Long stored strings ("390000 µm", "10000 nm") are hard to read.
- Suggested fix: keep the stored string in the tooltip and show an engineering-format value (5.66e8, 390 mm) on the
  card. Append the statistic (median, mean) to the primary value.

### 12. convention - 39 cm spiral drawn as a straight bar at y x138545

- Page: `/layout?id=cmp_wang2024b_spiral_1p75um` top view.
- Evidence: `layout_wang2024b_spiral_1p75um.png`. length_um 390000 (`cmp_wang2024b_spiral_1p75um-m4`, locator "p.11 Extended Data Fig. 2(a)
  caption") drawn as one straight waveguide filling the view. It is labelled honestly but conveys nothing.
- Suggested fix: for waveguide_xsec, when length_um is more than about 1000 x the width, show the length as a value
  label instead of a drawn extent (or note "spiral, drawn straight").

### 13. nit - ring scene draws a bus that may not exist; two-bus ring drawn single without a note

- Pages: `/layout?id=cmp_ofc2026_th1d6_gesilica_ring_d1p5mm` (coupled with a U-shaped fiber taper, no bus per the
  showcase rationale); `/layout?id=cmp_ofc2026_m1e6_sin_ring_r75um` (two-bus ring; the single-bus note is emitted only
  for `wdm.mrr`).
- Evidence: `layout_ofc2026_th1d6_gesilica_ring_d1p5mm.png`, `layout_ofc2026_m1e6_sin_ring_r75um.png`.
- Suggested fix: add the single-bus note for every ring class whose label or notes say two-bus / add-drop. For
  taper-coupled rings, label the bus "coupler not a bus (fiber taper)" or omit it.

### 14. nit - Th1D.6 cross-section heuristics add features not in the source

- Page: `/layout?id=cmp_ofc2026_th1d6_gesilica_ring_d1p5mm`.
- Evidence: `isRib()` matches "ridge" in the label, so a schematic slab is drawn ("rib from the platform / text").
  The cladding text "lower: 8-15 um thermal SiO2 on Si; upper: not stated" is parsed from its first clause, so the
  upper cladding is drawn and listed as SiO2.
- Suggested fix: restrict the rib heuristic to `*_rib` platform codes or an explicit slab / etch row. Parse an
  "upper:" clause in the cladding text, and fall back to "not stated".

### 15. nit - panel j reuses the platform palette for class families

- Page: `/explore` panel j.
- Evidence: `explore_1400x850_scroll2.png`. Blue is SOI in the page legend and in panels a-i, but Fiber-chip coupler
  in panel j (same for the other slots). The letter tooltip says so, but the page-level legend sits above it.
- Suggested fix: a separate palette (or neutral ramp) for class families, or a visible "colour = class family" tag
  in the panel corner.

### 16. nit - pinned-card placement

- Page: `/explore`, any scatter panel.
- Evidence: `place()` in `ScatterChart.svelte` assumes a 260 px card height. The laser card with a conversion note is
  about 280 px (`explore_hover_i.png`), so a pin on a low point can be cut by `.body { overflow: hidden }`. Two pins
  close together stack on top of each other (`explore_hover_i.png`, panel f).
- Suggested fix: measure the card after render; offset stacked pins.

### 17. nit - card hint and description length

- Pages: `/explore`.
- Evidence: pinned cards still show "click a point to pin its card". Letter tooltips for c, d, f are 2-3 sentences,
  where D100 says "one-line description".
- Suggested fix: hide the hint in pinned cards ("click x to unpin"); trim descriptions to one line and move the rule
  text into the badge tooltip.

### 18. nit - gallery gap card order

- Page: `/layout` gallery dc, awg, heater_ps.
- Evidence: `layout_gallery_1400x850_s2.png`, `_s4.png`. The "no hero" gap card is rendered after the typical card,
  while hero cards come first elsewhere.
- Suggested fix: merge gaps into the role-ordered card list.

### 19. nit - dc typical card shows "not reported" though a measured split exists

- Page: `/layout` gallery dc; `/layout?id=cmp_larocque2024_dc_michelson`.
- Evidence: `cmp_larocque2024_dc_michelson-m1` split_ratio_pct ~12 (measured, mean, n=5). The D107 companion for dc
  is imbalance_db only, so the card shows only "excess_loss_db not reported".
- Suggested fix: add split_ratio_pct as a dc companion (shown, never converted).

### 20. nit - log-axis minor tick labels

- Page: `/explore` panels e, i (log axes).
- Evidence: `explore_800x700_scroll2.png` (panel i). Plotly labels every minor tick (2-9) in each decade, so the
  axis reads "10 9 8 7 ...".
- Suggested fix: `dtick: 'D2'` or tick labels at 1, 2, 5 only.

### 21. nit - deep link and detail pane on /components

- Page: `/components#<id>`.
- Evidence: `components_ofc2026_m1e6_sin_ring_r75um.png`. The hash selects the component and the Layout section
  renders (with a working "full view" link), but the values table does not scroll to or filter the component.
  `components_guo2026_gc_532_layoutsection.png`: the detail values table is cut at the right pane edge (the basis
  column shows "deri", "mea").
- Suggested fix: scroll the table to the first row of the selected component; let the detail table wrap or scroll
  horizontally.

### 22. nit (data, visible in UI) - source year vs venue

- Pages: `/layout?id=cmp_churaev2023_ln_taper_transition` ("source (2021)", venue "Nature Communications 14, 3499",
  volume 14 = 2023); Explore hover of `cmp_datta2024_bare_sin_ring` ("2022, Optica 11(1), 48", volume 11 = 2024).
  This is likely the preprint year. It affects the year filter and panel j.
- Suggested fix: verify the registry `year` against the published venue.

### 23. nit - DevLog-005 showcase count

- Evidence: DevLog-005 TODO says "showcase selection (35 rows)". `component_showcase.csv` and components.json hold
  34 rows (35 lines including the header).
- Suggested fix: correct the count.

## Verified without findings

- Badges: for every scatter panel, plotted + omitted (missing x, missing y, missing both, incomparable, nonpositive)
  equals the total (a 51/120, b 9/62, c 46/58, d 82/119, e 12/52, f 29/30, g 2/21 GHz and 1/21 nm, h 29/38, i 10/61).
  The c total and omissions match an independent count (12 edge couplers lack a per_facet / loopback_half row).
- Hover cards on panels a-i match the CSV rows (value, unit, basis, locator): `cmp_ectc51909_2023_00009_spgc_oband-m1/
  -m2`, `cmp_ofc2026_tu2d3_gc_1d_si-m1/-m2`, `cmp_ectc51846_2026_00016_ec_fau_adhesive-m1`,
  `cmp_ectc51909_2023_00009_deep_rib_waveguide-m1`, `cmp_datta2024_bare_sin_ring-m1/-m3`,
  `cmp_ectc51687_2025_00284_transition_sin_si-m1`, `cmp_ofc2026_tu3c4_topic_ring_wdm_8ch-m2/-m3`,
  `cmp_liu2026a_ge_pd-m3/-m4`, and `cmp_bhasker2026_cmbh_dfb-m1/-m4` (11.5 dBm shown as > 14.1 mW, converted
  correctly).
- Drawn dimensions spot-checked (label, basis badge, locator on hover): `cmp_guo2026_gc_532-m4` 285 nm D and `-m8`
  100 nm D; `cmp_li2026aa_ssc-m12` 200 nm D and `-m16` 4.4 um D; `cmp_wu2025_vac_si_sin-m8` ~180 nm D;
  `cmp_wang2024b_spiral_1p75um-m11` ~70 deg M; `cmp_ofc2026_m1e6_sin_ring_r75um-m6` 700 nm D (true-scale inset);
  `cmp_feng2022_mmi_2x2-m3` 31.4 um D; `cmp_larocque2024_dc_michelson-m3` 34.5 um D;
  `cmp_liu2026a_ge_pd-m7` ~300 nm D; `cmp_liu2026d_tops_or-m10` 0.25 um R; `cmp_ofc2026_th2a9_awg_16ch_1p6nm-m8`
  324500 um2 R; `cmp_ofc2026_th1d6_gesilica_ring_d1p5mm-m7` 750 um R. These are all correct, and the remaining 114 of
  the 127 labels match too.
- Not-reported dimensions: dashed outline and amber dashed mark with the italic label "not reported"; the tooltip
  says "not reported by the source: drawn schematically". No number appears on a not-reported mark or label.
- The gallery covers all 12 templates. Role gaps for dc hero, y_branch hero and typical, awg hero and heater_ps hero
  are rendered as dashed cards (D112), except finding 7.
- Interaction: panes scroll at both viewports (Explore pane 3008 / 763 px, gallery 2290 / 794 px, components detail
  1504 / 794 px). Lin / log toggles change the Plotly axis type. Pin, unpin with the x button and with a click on
  empty space all work. Filters update every badge. The empty filter shows "No component matches the filters" with
  Reset. True scale / expanded y toggles relabel the badge. `/layout?id=` handles an unknown id and a
  laser.heterogeneous component.
- Conventions: dark by default (headless default light preference still renders dark). Sharp corners everywhere
  (computed border-radius 0 on all elements). Explore panels carry no titles or takeaway captions. Units are
  absolute. Details sit in hover tooltips.

## Summary

| severity | count | findings |
|---|---|---|
| bug | 4 | 1, 2, 3, 4 |
| spec deviation | 4 | 5, 6, 7, 8 |
| convention | 2 | 9, 12 |
| nit | 13 | 10, 11, 13-23 |
| total | 23 | |
