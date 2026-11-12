History showcase runtime (DevLog-017). Plain-text notes for builder agents; the binding contract is the comment at
the top of types.ts.

Files
  types.ts               spec types (static/data/showcases/<id>.json) and the ShowcaseModule contract
  progress.ts            pure: scroll -> p, chapter lookup, keyword fades, step targets, easing (tests: progress.test.ts)
  plot.ts                pure: plot scales, ticks, reveal by plot progress
  trace.ts               TS port of ipatent viewer/trace-render.js (ipatent trace schema) + hit layer
  three.ts               lazy three.js, ONE shared WebGLRenderer (pixel ratio <= 2), most-visible story holds it
  ShowcaseStory.svelte   tall track + sticky stage; keywords, labels, parts list, drawing, plot, panel, controls
  PlotAssembler.svelte   SVG plot: axes draw, then points / line by p; hover = value + locator; log toggle
  TraceView.svelte       traced drawing linked to the parts (numerals -> part ids via spec.drawings[].numerals)
  PartPanel.svelte       side panel: part (detail, quote, locator, dims with basis) or story (process params),
                         then references and withheld items
  ../showcases/index.ts  registry: import.meta.glob of ../showcases/*.ts, file name = milestone id
  ../Expanded.svelte     expanded history view (era header, stories, card strip)

Add a scene
  1. Spec: data/history/showcases/<id>.yaml (DevLog-017 section 4a). Run from the repo root:
       uv run --offline python scripts/build_history_view.py --figures
     (--figures keeps the local key-figure thumbnails; without it the local history.json loses has_local_figure.)
     This writes app/static/data/showcases/<id>.json, copies drawings/*.png and traces/*.json, and sets
     `showcase: true` on milestone <id> (only for merged milestones).
  2. Module: app/src/lib/history/showcases/<id>.ts, `export default` a ShowcaseModule. No registry edit needed.
     Use `import type` for three types and ctx.THREE at runtime (never a value import of 'three').
  3. The story appears in the expanded view of the milestone's era, and a diamond marker in the compact view.
     A missing spec, missing module or a build() that throws makes the milestone fall back to a plain card.

Spec fields the runtime reads beyond section 4a (all optional)
  height                 track length in viewport heights (default 5)
  chapters[].plot        plot id assembling across that chapter (default: plot whose id equals a chapter id, else
                         the first plot across the last chapter)
  chapters[].process     process step shown during the chapter (default: process step with the chapter's id)
  plots[].x/y.log        true = starts log, with a log / linear toggle
  plots[].x/y.range      fixed [min, max]
  plots[].series[].style 'line' | 'points' | 'both' (default line above 40 points)
  drawings[].trace       trace file name in showcases/traces/; drawings[].image scan in showcases/drawings/

Additions 2026-11-11 (optional, backward compatible)
  chapters[].labels      part ids labelled on the canvas in that chapter (default: chapter parts with essential: true);
                         [] = no labels. A label shows all essential dims ("10 mm x 20 mm" when units agree, else ", ").
  pick() -> PickInfo     a module may return {id, label, detail?} for scene elements that are not spec parts: tooltip =
                         label + detail lines, the id is passed to highlight(), clicks do nothing. Strings work as before.
  axis.scale: none       no ticks, tick labels or grid; axis line and title stay (figures without a printed scale)
  axis.ticks             number = mark every step, labels at round values; list = exactly these labelled ticks
  axis.unit              ^ / _ marks render as super / subscripts: "10^3 cm^-1", "cm^{-1}"
  series[].bars          [[x0, x1, h], ...] or [{from, to, height, line?}, ...]: filled bars (16 % fill, thin outline),
                         grow by p; they replace that series' line and markers; hover = name: line, x range, height,
                         basis, locator
  series reveal          staggered and overlapping (start i at an even fraction, every series done by the chapter end)
  plot kind: levels      energy-level diagram, fields:
                           y: {label, unit, range?, ticks?, scale?}
                           levels: [{id, label, kind: line|band, energy: E | [E0, E1], x?: [f0, f1], basis, locator, note}]
                           splits: [{between: [idA, idB], value, unit, basis, locator}]   (bracket shows the printed value)
                           transitions: [{from, to, label?, kind: pump|nonradiative|emission, wavelength_A?, basis, locator}]
                         label = term symbol: leading digits superscript, trailing digits subscript ("4A2", "2E", "Ē").
                         Default columns: lowest level full width; levels named in splits on the right; the rest left;
                         one arrow slot per transition. Assembly: axis, levels bottom-up, split, arrows in spec order.
                         Hover levels / split / arrows for value + locator. Route a chapter to it with chapters[].plot.

Round 3, Play, ruby pass 2 (2026-11-11; optional, backward compatible)
  title_note             spec level; shown under the tagline in the story side panel ("Sources")
  plots[].alt_of         <plot id>: this plot is an alternate of that one; its chapter shows a toggle in the plot panel
  plots[].label          short toggle text (default title, else id), e.g. "Paper Fig. 1" / "Patent FIG. 4"
  log / linear           kept per plot id (switching plots or scrolling back never carries an axis choice over)
  series[].style dashed  dashed line, dashed legend swatch
  series[].color         CSS colour override; default palette blue, amber, green, violet, pink (darker set in light)
  orbit                  spec.orbit or handle.orbit {polar: [min, max] deg from +y, azimuth: [min, max] deg,
                         distance: [min, max]}; default polar [2, 88] (never under the floor); handle wins
  transitions[].from_energy / to_energy   end point on the drawn energy scale (e.g. inside a band)
  dims[].label_short / show_label         canvas label prefix: "dia. 10 mm, length 20 mm"
  scale: none            tooltips say "as drawn" instead of printing the drawn height (points and bars)
  Play button            bottom bar, left of the chapter buttons; Space toggles. Scrolls the page's scroll container
                         (p, scrub bar, chapter buttons stay in sync; frame(p) unchanged). Pacing PLAY in progress.ts:
                         3.5 s near-linear move + 80 ms dwell per chapter (no pause between stages); restarts from 0 at the end;
                         stops at p = 1. Pauses on wheel, touch, pointer down, arrow / page / home / end keys, step
                         buttons, scrub bar, the story leaving the view, tab hidden. Reduced motion: jump + 1.5 s hold per chapter.

Process step tooltip (D992): each param prints "label: value unit" then "basis, source, locator";
  process[].params[].source / process[].source give the short source label (param wins).

Design language (D997, round 4): plate typography in the history tab (display face for era years, story titles and
  keywords; serif text face for lines, taglines and panel prose; small-caps kickers; scotch rules above eras and
  stories; booktabs dim tables); no left-edge colour bars, no shadows or glows in the chrome. Fonts: static/fonts
  (OFL texts beside them), declared by HistoryFonts.svelte. chapters[].keyword may mark one phrase with *asterisks*:
  it renders as the amber italic emphasis.
  process[].params[].source, process[].source: see the step tooltip note above.

Ruby pass 3: canvas labels are measured and placed right of the anchor, else left, else clamped and wrapped inside
  the pane (modules need not reserve room); keyword *markers* are stripped in buttons, tooltips and aria labels;
  levels tooltips under y scale none say "as drawn" (split brackets keep their printed value).

MCVD pass 2: the plot legend sits in the emptiest corner of the data area (all series' points and bars counted);
  reduced motion: step buttons / scrub / Play bring the whole (non-sticky) stage into view below the header.

Cobra audit (2026-11-11)
  plots[].note           small muted italic line under the plot (2 lines max, full text on hover)
  dims[].note            italic muted line under that row of the side-panel dims table
  text markup            `_{...}` subscript, `^{...}` superscript, braces required: r_{33}, r_{yzy}, L_{0}, O_{2},
                         Cr^{3+}. Applies to part names / roles / details / quotes / locators, dims labels / values /
                         notes, process step names and params, titles, taglines, title notes, keywords, lines, canvas
                         labels, parts list, plot titles / notes / axis labels / legends, alternates labels, drawing
                         captions, references, withheld items and the stage tooltips. Plain _ and ^ stay literal; units
                         keep their shorthand (cm^-1). Plain-text (data-tip) tooltips fall back to Unicode sub /
                         superscripts where every character has one, else the text without markers.
  y-axis title           shrinks to 9 px, then cuts with an ellipsis (full title on hover) when the plot is short
  side-panel tables      fixed layout: long values wrap, basis badges stay visible

Menu bar pin / unpin and mobile Play (2026-11-11)
  The expanded history view has a pin button in its toolbar. Unpinned: the app nav row and the toolbar + legend slide up
  out of view (200 ms; none with reduced motion), the stories gain the height; pointer within 12 px of the top edge
  shows them, leaving the bar hides them; touch: a handle at the top edge shows them, the next scroll down hides them.
  Stored per viewer in localStorage `history.barPinned`. The scroll container height can therefore change at any time:
  stories observe it, keep their p when they are in view, and Play re-reads its geometry.
  Play writes scrollTop directly each frame from cached geometry (no layout reads), sets p and draws in that same frame
  (the scroll event it causes is ignored), pauses when the page moved by something else (user drag or momentum), and on
  touch devices renders at most 1.5 device px per CSS px while playing (restored on pause). Unforced redraws of an
  already drawn state are skipped; canvas labels re-render only when they move.

Error bars and equal aspect (2026-11-11)
  series[].err           y error bars: one number (symmetric, every point) or per point: number (symmetric), [lo, hi]
                         (offsets below / above, data units) or null (no bar). Thin whiskers with small caps in the
                         series colour, revealed with their point; a log axis clamps a low end at or below zero to the
                         axis floor. Hover adds "+hi / -lo" (or "+/- e") after the value. Whisker ends count in the
                         axis extent.
  series[].err_x         x error bars, same forms
  plots[].aspect: equal  one data unit on x has the same length as one on y: the data area is letterboxed and centred
                         in the plot panel (also on phones); ignored when either axis is on a log scale

Drawing caption and note (2026-11-11)
  drawings[].caption     source line under the traced drawing (e.g. "US 3,584,230 FIG. 1"); default: drawings[].source
  drawings[].note        one short caveat under it, italic muted, clamped to 2 lines with the full text on hover
                         (e.g. "patent embodiment, not the paper's apparatus"); both take _{...} / ^{...} markup

Stems (2026-11-11)
  series[].style: stems  a vertical line from the base up to each point (comb lines, discrete spectra), revealed point
                         by point; hover as for points; legend swatch a short stem; works with err / err_x and log y
  series[].stem_base     base in data units (default: the y-range minimum; on log y never below the axis floor)
  series[].stem_cap      true: a small marker at the top of each stem

Plot hook and part pick detail (2026-11-11)
  handle.plot?(id)       optional module hook: id of the plot on screen (null = none), called when it changes (chapter
                         plot appears / leaves, viewer switches to an alt_of alternate) and once when the story is
                         ready. Store the id only; frame(p) reads it, so the picture depends on (p, selected plot) and
                         nothing else. The runtime redraws after the call.
  pick() PickInfo on a part   {id: <spec part id>, label, detail}: the usual part tooltip with the detail lines
                         (markup-rendered) under the role

Legend groups, notes, compact phone legend, swatch outlines (2026-11-11)
  series[].legend: false        no legend entry
  series[].legend_group: <key>  series sharing the key share one legend row (label from the group's first series;
                                swatch combines line and dot when the group has both) and, unless they set `color`, the
                                first series' colour
  plots[].legend_note           one line under the legend (markup-rendered), e.g. "line: simulated, dots: measured"
  The legend sits in the emptiest corner of the data area; if every corner covers data it moves above the data area,
  wrapping into columns. On short panels (phones) it is capped so the data area keeps about 60 % of the panel and the
  rest is behind a "+N more" toggle. Swatches (plot legend, parts list, history legend chips) carry a 1 px neutral
  outline.

Plot pen helpers (2026-11-11; ./plot, the same code PlotAssembler uses)
  revealAt(spec, plotId, p)  per-series revealed fraction 0..1, in plotSeries(plot) order
  penAt(spec, plotId, p)     per-series pen {series, index, x, y} or null (index: last whole point, spec indices;
                             x, y in data units, on the growing segment between points)
  Both use the plot's chapter window (complete at 90 % of the chapter, PLOT_SPAN), the axes delay and the staggered
  series / point reveal; an alt_of alternate uses its main plot's chapter. Points are counted with the spec's default
  axes (log where the axis starts on log). Pass the plot id on screen, from handle.plot(id).
  Example, in a module:
    let shown: string | null = null;
    plot(id) { shown = id; },
    frame(p) { const pen = shown ? penAt(spec, shown, p)[0] : null; if (pen) drive = pen.x; ... }

3D environment and shader cache (2026-11-11)
  scene.environment      the shared room environment map is ready before a story's build and first render, every run
                         (one shared setup promise for all stories)
  handle.environmentIntensity   optional number: applied to the story's own scene.environmentIntensity before each
                         render (three r186 ignores material.envMapIntensity for scene.environment); other stories keep
                         theirs because the value lives on each story's scene
  onBeforeCompile        modules that patch shaders must set a unique material.customProgramCacheKey() (e.g.
                         `${spec.id}:glass`): every story shares one WebGLRenderer and its program cache

Layout to frame for: desktop stage = model pane + 300 px side column (drawing, parts list) + control bar; during a
plot chapter the plot covers the right half of the model pane (phone: the bottom 56 %), so keep the model in the left
half then. Keywords sit top-left (about 70 px tall on desktop).

On-canvas text (D983): chapter keyword + line (spec), the current process step name (params in its tooltip), and
labels for essential parts of the current chapter (name + first essential dim) when the module implements anchor().
Everything else (role, quote, locator, dims with basis, references, withheld) is in tooltips and the side panel.

Testing a module without shipping a fixture
  The framework was verified with Playwright route interception: the dev server's
  /src/lib/history/showcases/index.ts, data/history.json and data/showcases/<id>.json were answered from files outside
  the repo. Pure checks: same p from both scroll directions must give byte-identical stage screenshots.

- Units (2026-11-11): values meet units through `unitSuffix()` / `withUnit()` in progress.ts: "°", "%", prime, double prime attach without a space ("26°"); "deg" prints as "°"; other units keep the space.
