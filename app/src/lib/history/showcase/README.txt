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
