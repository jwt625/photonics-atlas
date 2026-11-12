---
name: history-showcase
description: Build a scroll-driven interactive story (showcase) for a historical photonics milestone in the History tab of this repo - sourced spec, 2.5D / 3D scene module, assembling plots, traced public-domain drawing, part interactivity, Play button - and audit it against the sources. Use when adding, revising or auditing a showcase story, when changing the showcase runtime, or when fixing milestone tags (kind, material, topic, thread) that the History tab shows.
---

# History showcase stories

A showcase is a tall section in the expanded History view with a sticky stage: scroll progress p in [0, 1] drives a
pure `frame(p)` that assembles a device, an experiment or a process, then its result plot. Parts are linked across the
3D / 2.5D model, a traced public-domain drawing and a parts list (hover highlights all three; click opens a side panel
with the source quote, locator, dimensions with basis, references and withheld items). Play runs a story by itself.

Pilots, both passed a fresh-context audit: `maiman1960` (ruby laser head, 3D, Nature 1960 + US 3,353,115) and
`macchesney1974` (MCVD process, 3D, Proc. IEEE 1974 + US 4,217,027). Design record: `DevLog/DevLog-017-history-showcases.md`.

## Files

| path | what | owner |
|---|---|---|
| `data/history/showcases/<paper_id>.yaml` | spec (schema: DevLog-017 section 4a, runtime fields in `types.ts`) | research agent, then builder for runtime fields |
| `data/history/showcases/<paper_id>.report.txt` / `.audit.txt` | research report (sources, fixed / assumed / withheld, digitization calibration) / audit findings | research / audit agent |
| `data/history/showcases/drawings/`, `traces/` | public-domain drawing crop (PNG) and its vector trace (ipatent trace schema) | research agent |
| `app/src/lib/history/showcases/<paper_id>.ts` | scene module (registered automatically by `index.ts`) | one builder agent |
| `app/src/lib/history/showcase/` | runtime: `types.ts` (contract + every spec option, read it first), `README.txt`, `ShowcaseStory.svelte`, `PlotAssembler.svelte`, `LevelsDiagram.svelte`, `TraceView.svelte`, `PartPanel.svelte`, `progress.ts` (scroll mapping, Play pacing `PLAY`), `plot.ts`, `levels.ts`, `trace.ts`, `three.ts` | one runtime agent |
| `app/src/lib/history/Expanded.svelte`, `routes/history/+page.svelte` | expanded / compact views and toggle | coordinator |
| `data/history/milestone_tags.csv` | kind, material, topic, thread per milestone (read from the paper) | tag agents + audit |
| `scripts/build_history_view.py` | writes `app/static/data/history.json` and `static/data/showcases/` | coordinator |

Build data: `uv run --offline python scripts/build_history_view.py --figures` (local; without `--figures` the local
`history.json` loses `has_local_figure`). App: `pnpm check`, `pnpm test`, `pnpm build` in `app/`.

## Workflow (per story)

1. **Milestone first.** The paper needs an audited, merged milestone row (`data/_staging/history/CONTRACT.md`,
   `hist_merge_milestones.py`) and a row in `milestone_tags.csv`; the story and the timeline must agree.
2. **Research agent** writes the spec, the report, and (if a public-domain patent or pre-1929 figure shows the device)
   the drawing crop + trace with the loop of the sibling `ipatent` repo (its skill `patent-figure-viewer` and
   `pipeline/TRACE_SCHEMA.md`; copy overlay / coverage into a scratch folder, never edit the ipatent repo).
   A traced drawing is a clean object-by-object redrawing in the original's style (owner 2026-11-11, D1023, on an
   edge-map trace of the Colladon engraving: "horrible. focus on the actual objects, instead of bruteforce mimicry of
   the drawing"): recognize each object, draw deliberate outlines in measured proportions plus a few controlled
   hatching / tonal strokes; background plain or sparse. Never edge-map or pixel-following mimicry. Judge by a
   side-by-side render at equal size (clean and recognisable); coverage is only a sanity number. Crops contain the
   whole figure (bounds measured from the ink, frame to frame). Patent line drawings fit this naturally (their parts
   are already deliberate lines); engravings and photo-like plates need the redrawing. Patent PDFs: one paced request, generic User-Agent, into git-ignored `cache/showcases/<paper_id>/`.
   Plots are digitized from the page renders with axis calibration recorded in the report.
   Find sources by browsing the sibling atlases as structured data before any web search: `eo-modulator-atlas`
   (`data/devices.csv` columns such as `eo_material`, `electrode_type`, `drive`, joined to `data/papers.csv`, and
   `data/evidence/<paper_id>.yaml`; read its README and distill skill first), `advanced-packaging-atlas`, and this
   repo's `data/` and `references/`. Filter by columns, never blind keyword grep.
3. **Builder agent** writes the scene module against `types.ts` and adds runtime fields to the spec only (never sourced
   values). Verifies with `pnpm check`, `pnpm test`, Playwright shots at 1440x900 and 390x844 over p = 0.02 ... 1.0,
   hover, side panel, explode, orbit, light theme, reduced motion, a Play run, frame-time sampling; looks at every shot.
4. **Fresh-context audit agent** (read-only, writes `<paper_id>.audit.txt`): spec values, quotes and locators against
   the sources; re-measures a few digitized points; geometry and topology against the drawing; physics of the story
   text and animation; withheld items not drawn; on-canvas text budget. Both pilots came back NO-GO with 3 wrong items
   each (a YAML parse bug, schematic heights on a numbered axis, beam after the flash; same-pass sintering, equal-area
   instead of equal-radius rings, a rotation arrow turning against its head): budget for a fix pass.
5. **Coordinator** rules on the findings (record a decision in the DevLog), sends the builder one fix pass, routes
   runtime needs to the runtime agent, then checks the production build itself (below) before handing over.

Run independent streams in parallel (research per story, runtime, tag fixes, audits); each agent owns its files.
Runtime changes stay additive while builders work. Every new runtime option goes into the `types.ts` doc comment and
`README.txt` the same turn.

## Content rules

- **Never invent.** Every number, part and arrangement comes from the paper, the patent or another cited primary
  source, with a locator. Basis per value: `stated`, `figure`, `ref`, `digitized`, `assumed` (secondary sizes only,
  shown as assumed). If the sources do not fix a part's arrangement, the part is withheld with the reason, or drawn
  as a plain neutral stand-in (a box, a cylinder) that adds no detail; never a guessed drawing.
- A paper may lack the recipe (MCVD 1974 printed no process numbers): take values from the same group's patent of the
  same work and label each as a patent value with column:line.
- Schematic figures stay schematic: an energy-level figure drawn out of scale gets a schematic axis (`scale: none`),
  with the real values (wavelengths, splits) only in hover. Never put drawn heights on a numbered axis.
- Animated quantities follow the plot pen: when a plot draws, the model's drive (voltage, frequency) is the plotted point,
  and any response (brightness, modulation depth) comes from the digitized curve; never sweep past the measured range
  (D1006). Illustrative choices (a drawn wavelength, a compressed plan) are labelled where they show, not only in withheld.
- Physics must read right in the animation: lasing during the pump flash, soot depositing downstream of the hot zone
  and fusing as the zone passes, beam leaving through the output hole along the axis, rotation sense matching arrows.
- Do not model from famous publicity photos without checking they show the real hardware (the well-known Maiman ruby
  photo does not).
- "First" appears only when a cited source supports it; a later name for a process (MCVD) is fine with a side-panel
  note that the paper does not use it.
- Digitize densely: sample each curve at about 1/60 of its axis span (roughly 150-200 points for a full-width curve)
  from real reads of the figure, never by interpolating sparse reads. Vector figures: sample the exact PDF path at the
  centre of the drawn stroke (intersect the sample line with the path segments), not a mean of nearby vertices. Raster
  figures: per-column reads, median per bin; where a bin falls on masked grid-line columns on a steep part of the
  curve, drop the bin (it biases into a visible kink) rather than fill it. Record the sampling in the plot note and
  the report (D1007).
- When the owner wants features the paper's device did not have (e.g. T-rail electrodes, double differential drive on
  a 2018 TFLN modulator), keep the published device as is and add closing "what came next" chapters sourced from the
  later papers, labelled as later work in the chapter line and side panel (D1008).
- Names and spellings as the paper prints them ("Cobra", not "COBRA"); keep the tag table consistent with the story.
- Licensed papers: plots are re-plotted from digitized points (figure + page locator); no figure images in the public
  build. Public-domain drawings (US patents, pre-1929) may be shown as crop + trace.

## Presentation rules

- Clean and elegant, Apple-product-page feel: a big keyword (at most 3 words) and one line (at most 12 words) per
  chapter; on the canvas only `essential: true` dimensions (2-4 per story) and short part labels per chapter
  (`chapters[].labels`); everything technical lives in hover tooltips and the click-open side panel.
- Notation: write sub/superscripts as `_{...}` / `^{...}` in any spec text (`r_{33}`, `L_{0}`, `Cr^{3+}`, `Al_{2}O_{3}`);
  the runtime renders them (D1005). A raw `_` or `^` must never show: the data build logs "raw markup in <path>" for
  shown text fields (grep it before handover); unit fields may use the exponent shorthand `cm^-3` (D1106). Very large or
  small numbers print as 10⁵ / 2.5×10⁵, never 1e5. Caveats go in `plots[].note` / `dims[].note`, which
  the runtime displays.
- No numbers in chapter lines unless they are essential dims; labels say which number is which ("dia. 10 mm,
  length 20 mm", "OD 14 mm, ID 12 mm" via `dims[].label_short`).
- At most one amber italic emphasis per story (`*694.3 nm*` in a keyword). At most 3 plot chapters per story; further
  results go to the side panel (D1004).
- Editorial plate typography in the History tab: Playfair Display for era titles and story keywords, Source Serif 4
  for lines and panel prose (both self-hosted in `app/static/fonts` with OFL texts), small-caps kickers, double
  scotch rules (2px over 1px) above sections, booktabs tables; toolbar, legend and data ticks keep the app sans.
- No colored rules as decoration: no vertical color bar on the left edge and no colored top line either. Show a
  category as a small tag rectangle with a light fill of its color and text in the same color (`.ctag` in
  `Expanded.svelte`); highlights are light fills with matching text. Neutral 1px dividers and the gray scotch rules are
  fine. No shadows, glows or gradients in UI chrome (glow only for physical light in a scene).
  Sharp corners. Dark default, light theme must work.
- **No internal shorthands in anything a user sees**: no era / batch codes (E0, hist_19), decision ids, DevLog
  references, internal ids (cmp_..., paper ids such as maiman1960) in UI text, legends, tooltips, captions or
  locators. Locators cite like "Maiman, Nature 1960, p.493" or "US 3,353,115 col. 2:33-37". Before handing over, grep
  the rendered page text and `static/data/showcases/*.json` for such tokens. `tests/test_views.py` enforces part of
  this for served views (no DevLog / decision ids in viewer-facing notes).
- Composition: during plot chapters frame the model in the left half (plot on the right; bottom on phones); fade
  props (power supply, leads) that would clutter; beams and fibers end before the plot panel and the right column.
- Play: near-zero dwell between chapters (`PLAY` in `progress.ts`: 80 ms, near-linear easing); reduced motion jumps
  chapter to chapter with a hold. Play scrolls the page so p, scrub bar and chapters stay in sync; any user input
  pauses it.

## Scene module contract (summary; `types.ts` is authoritative)

- `export default { renderer: '3d' | '2.5d', build(ctx) }`; ctx gives the spec, pane size, theme, reduced flag and,
  for 3D, the three namespace, an empty scene and a camera (one shared WebGL renderer, three.js lazy-loaded).
- Handle: `frame(p)` pure (no timers, no accumulated state, seeded particles; same picture from either scroll
  direction), `highlight(ids)`, `pick(x, y)` (part id or `{id, label, detail}`), `resize`, `dispose`; optional
  `explode(k)`, `anchor(id)` (any visible point; the runtime keeps labels inside the pane), `target()`, `theme(t)`,
  `assembledAt`, `orbit` limits.
- The runtime owns keywords, labels, plots (series, `bars`, `style: dashed`, log toggles, `alt_of` alternates,
  `kind: levels` diagrams with `splits` and `transitions`), drawing pane, parts list, tooltips, side panel (incl.
  `title_note`), process HUD (`process[].params[]` with `basis`, `source`, `locator`), steps, scrub bar, Play,
  parts tour, explode slider, orbit.
- 3D lighting: use `handle.environmentIntensity` for the shared room environment's strength (not material.envMapIntensity);
  materials with onBeforeCompile set a unique `customProgramCacheKey()` (`${spec.id}:<role>`) (D1107).
- Follow the plot pen with `penAt(spec, plotId, p)` / `revealAt(...)` from `showcase/plot.ts` (the runtime's own reveal
  code), never a copied formula. Crowded legends: `series[].legend: false`, `legend_group`, `plots[].legend_note`.
- Module hooks: `handle.plot?(id | null)` reports the plot on screen (incl. `alt_of` toggles) so the model can follow it;
  `pick()` may return `{id, label, detail}` for a part to add per-part caveats to its tooltip (D1102).
- Category bar plots: `plots[].x.categories` with bars `{at: i, height}` and `x.category_grid` (D1110).
- Also available (D1102): stems `series[].style: 'stems'` (+ `stem_base`, `stem_cap`) for line / comb spectra, error bars `series[].err` / `err_x`, equal-aspect plots `plots[].aspect: 'equal'`, drawing
  `caption` / `note` under the traced drawing, pin / unpin menu bar in the expanded view.

## Coordinator final check (before handing over)

1. `pnpm check`, `pnpm test`, `pnpm build` in `app/`; three.js only in a dynamic chunk; History route node size.
2. Python: `uv run --offline pytest -q` (at least `tests/test_views.py`, `tests/test_showcase.py`).
3. Serve the build with `vite preview` on an uncommon free port in tmux. Restart the preview after every rebuild:
   it indexes the build's files at start and returns 404 for new hashed files (the page then loads empty).
4. Playwright on the preview: wait for the milestone count to load before asserting anything; shots of each story at
   desktop and phone; console errors; a Play run measuring the longest stall; visible-text grep for shorthands.
   Test Play on a phone profile too (390x844, touch, device scale 3, CPU throttle 4x via CDP): p must never step
   back, no long stalls, no fight between programmatic and user scroll (owner found mobile Play glitchy, D1009).
   Check the expanded view with the menu bar pinned and unpinned (auto-hide) as well.
5. Look at the shots yourself; give the owner the URL and the open decisions.

## Milestone tags (what the History tab colors by)

`material` once came only from merged component rows, so device papers whose rows were staged, or devices outside the
component taxonomy (bulk / gas lasers, masers, fibers), showed "theory / no device". The tag table fixes this: per
paper `kind` (theory / device / process / measurement / system / review), `material` in the paper's own word (do not
upgrade "glass" to "silica"), a specific `topic` (no generic thread names, no "origin" or "first" the paper does not
claim) and `thread` from the existing vocabulary, each read from the paper (the abstract usually settles kind, e.g.
"has been fabricated"), then audited by a fresh agent. "theory / no device" is shown only for `kind = theory` with no
stated material. Every new milestone needs a tag row; the build logs missing ones.
