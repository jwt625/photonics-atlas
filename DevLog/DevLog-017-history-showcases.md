# DevLog-017: History tab, expanded view with scroll-driven device showcases

| | |
|---|---|
| Date | 2026-11-11 |
| Status | Pilot gate (D984): ruby + MCVD stories built, audited, fixed, in the page; waiting on owner review before the other 14 |
| Scope | Expanded timeline view (default) next to the current compact view; 1-3 showcase milestones per era, each a scroll-driven story that assembles the device, process or plot in 2.5D / 3D with ipatent-style part interactivity |
| Related | DevLog-016 (history layer, D974 history tab, D975 batch-1 audit); ipatent repo (tracing pipeline, `viewer/trace-render.js`); advanced-packaging-atlas DevLog-008 / DevLog-016 (three.js package viewer, process-flow animation); lithium-niobate baby mode (`frame(t)` + `settle` contract); PlayGround 20261009_pigeon_pluggable (OSFP explode-orbit hero) |
| Decisions | D980-D999 reserved for this DevLog |

## Request (2026-11-11, Wentao)

- Look at the history tab and the current milestones; upgrade it.
- Check the local ipatent repo for how drawings are traced.
- Pick 1~3 representative results per era; show them inline with a scrolling animation (Apple product page style:
  keywords, parts move in and rotate) that assembles the plot, components or schematic, or animates the process /
  recipe / steps of the experiment. 2.5D or 3D model of the device, component or chip as fit (e.g. the first ruby
  laser). Find extra reference material where needed. Interactivity built in, similar to ipatent.
- Two toggleable views: the current compact timeline and the new expanded one; expanded is the default.
- Reference: pigeon OSFP explosion view (hypothetical pigeon with the components of an 800G OSFP pluggable).
- Delegate to subagents; ask for proposal review and clarifications.

## Starting point (inspection 2026-11-11)

| item | state |
|---|---|
| History tab | `app/src/routes/history/+page.svelte` (serpentine timeline, era bands, 4 color modes, search, detail panel `HistoryPanel.svelte`), geometry `app/src/lib/history/layout.ts`; commit 83ed981 |
| Data | `app/static/data/history.json` from `scripts/build_history_view.py`: 7 eras, 72 milestones (batch 1, D975) |
| Milestones per era | E0 10, E1 26, E2 31, E3 2, E4 3, E5 2, E6 0. E3-E6 are thin because only batch 1 (hist_01-09) is merged; hist_10-18 are staged (`papers.csv` only) |
| Core candidate list | `data/_staging/literature/history_candidates.csv`, core 295 (E0 15, E1 26, E2 43, E3 39, E4 42, E5 44, E6 86); 293/295 core PDFs cached |
| Key figures | Licensed PDFs: thumbnails only in local builds (git-ignored), public build shows caption + note (D974) |
| App stack | SvelteKit static, Svelte 5, no three.js yet (advanced-packaging-atlas uses three ^0.186) |

### How ipatent traces drawings (what carries over)

- One JSON per figure (`data/<pn>/traces/fig-<id>.json`, schema `pipeline/TRACE_SCHEMA.md`): pixel coordinates of the
  upright crop; `elements[]` each with `id`, `ref` (the reference numeral it is), `kind` (block / wire / label /
  leader / text / outline / mark), `step` (sequence index), `shapes[]` (r, c, e, polylines, paths, text, hatch,
  stipple fills).
- A part = block + label + leader sharing one `ref`; hovering any of them highlights all three, and the side panel
  lists the verbatim text mentions with column:line citations. Parts tour (Left / Right), Redraw / Scan / Overlay.
- Quality loop: per-figure generator script measured from the scan (PIL / numpy / scipy), `overlay.py` (red trace
  over grey scan) and `coverage.py` (covered %, off-scan %, MISSING / EXTRA clusters) until 90-98 % covered.
- Renderer `viewer/trace-render.js` (GPL-3.0, same author) is plain JS and portable into a Svelte component.

Carried over: part ids keyed to source numerals or source names, hover / pin linking across views, parts tour,
`step` index for sequences, the trace + overlay + coverage loop for any 2D figure we redraw, verbatim quote +
locator for every part name.

## Proposal

### 1. Two views

- Toolbar toggle `Expanded | Compact` (Expanded default), state in the URL (`?view=compact`), the selected milestone
  hash keeps working in both.
- Compact = the current serpentine timeline, unchanged.
- Expanded = one vertical scroll through the eras:
  - era header (id, years, intro, count),
  - that era's showcase stories (full-width, scroll-driven, below),
  - the era's remaining milestones as a dense card strip (year, topic, DRI; hover tooltip; click opens the existing
    detail panel).
- Showcases are also reachable from the compact view: a showcase milestone gets a marker; clicking it opens the
  expanded view scrolled to its story.

### 2. Showcase story (one per pick)

- Tall section (about 4-6 viewport heights) with a sticky stage. Scroll progress `p` in [0, 1] drives a pure
  `frame(p)` (same contract as baby mode `frame(t)` + `settle`): deterministic, scrubbable both ways, no timers.
- Chapters inside `p`: keyword title (large, Apple style: "Ruby rod", "Helical flash lamp", "694.3 nm"), parts fly
  in and rotate, assembly, then the action (flash fires, layers grow, light switches ports), then the result plot
  assembles axis by axis and point by point.
- Three renderers, chosen per pick:
  - **3D** (three.js): rigid devices with real volume (ruby laser head, maser, MCVD lathe, microtoroid, TFLN ridge
    modulator). Exploded view on the way in, orbit, cutaway.
  - **2.5D** (SVG / Canvas with isometric extrusion of a traced plan view or layer stack): planar chips and stacks
    (DH laser layers, Ti:LiNbO3 switch, PHASAR, microring).
  - **2D traced** (ipatent renderer): public-domain patent figures and pre-1929 figures, shown as a linked "Drawing"
    pane next to the model.
- Interactivity once the stage is in view (any `p`):
  - hover / click a part in the model, the drawing or the parts list: all three highlight; tooltip = part name,
    verbatim quote, locator (paper page / patent column:line), dimensions with their basis;
  - parts tour (Left / Right), step buttons and a scrub bar (for keyboard users and reduced motion), free orbit /
    zoom on 3D after assembly, explode slider;
  - plot: hover a point for its digitized value and the figure it came from; log toggle where the axis warrants it.
- Performance: three.js lazy-imported when the first 3D story comes near; one shared WebGL renderer handed to the
  active stage (browsers cap live contexts); pause offscreen; pixel ratio capped at 2; `prefers-reduced-motion` gets
  the step buttons, no scroll-linked motion; phone width keeps the stage on top and captions below.

### 3. Provenance rules (from the layouts rule: no guessed drawings)

- Every dimension, material and topology choice carries a basis: `stated` (paper / patent text, locator),
  `figure` (measured from a figure with a printed scale), `ref` (other primary or museum source, URL), `assumed`
  (secondary dimensions only; shown as "assumed" in the tooltip). Topology is never assumed: if the sources do not
  fix how a part is arranged, that part is withheld and the reason is on the page.
- Plots are re-plotted from digitized points (locator = figure + page), not image crops; the public build never
  embeds licensed figure images (D974).
- Public-domain drawings (US patents, pre-1929 papers) may be traced and shown directly.
- Captions and keywords are short and factual; no editorial takeaways.

### 4. Picks (recommendation: 16 stories, 2-3 per era)

Status column: `merged` = in the 72-row timeline now; `staged` = core paper, milestone row still to distill and audit.

| era | pick | paper_id | status | renderer | story (scroll sequence) | extra references to research |
|---|---|---|---|---|---|---|
| E0 | Light guided in a water jet | colladon1842 | staged | 3D | tank fills, orifice opens, jet arcs, arc-lamp beam enters through the lens and stays inside the curved jet by total internal reflection | Colladon 1884 La Nature engraving (public domain) |
| E0 | Ammonia maser | gordon1954 | merged | 3D | NH3 source, electrostatic state focuser (quadrupole rods) passes the upper state, resonant cavity at 23.87 GHz, emission | paper text dims; Gordon 1955 Phys Rev long paper |
| E1 | First laser (ruby) | maiman1960 | merged | 3D + traced patent | exploded head: aluminium cylinder, helical xenon flash lamp, ruby rod with silvered ends; assemble, rotate, flash, red pulse; fluorescence vs output spectrum narrowing plot | Maiman patent US 3,353,115 (traceable drawing); Maiman 1961 Phys Rev 123, 1145; HRL / museum photos for scale |
| E1 | GaAs junction laser | hall1962 | merged | 3D | cube cut from the wafer, Zn-diffused junction, polished end faces, 77 K, pulsed current; spectral line collapses above threshold (plot) | GE patent (to find); Hall's later recollections for dims |
| E1 | Prism coupler into a thin film | tien1969 | merged | 2.5D | film on substrate, prism lowered to the gap, beam at the synchronous angle couples in, m-line pattern | paper only |
| E2 | Room-temperature CW DH laser | hayashi1970 | merged | 2.5D | LPE grows the layers one by one (n-GaAs, n-AlGaAs, GaAs active, p-AlGaAs, p-GaAs), stripe contact, band diagram assembles beside the stack, CW L-I plot | paper only (alferov1970 as the parallel note) |
| E2 | MCVD preform process | macchesney1974 | merged | 3D process | silica tube on a rotating lathe, traversing oxy-hydrogen burner, SiCl4 / GeCl4 / O2 in, soot deposit, sinter pass by pass, collapse, preform, draw; HUD shows the recipe values the paper prints | MacChesney MCVD patent (public domain, traceable) |
| E2 | Switched directional coupler (COBRA) | papuchon1975 | merged | 2.5D | Ti strips deposited, in-diffused into LiNbO3, electrodes, light hands over between guides; voltage toggles cross / bar; extinction plot | paper only |
| E3 | PHASAR / AWG | smit1988 | merged | 2.5D | plan view traces in: input guide, free region, arrayed guides (count from the paper), output; wavelengths focus to different ports | paper only |
| E3 | Erbium-doped fiber amplifier | mears1987 | staged | 3D | pump, WDM coupler, Er-doped fiber coil, signal in / out; gain vs pump power plot | desurvire1987 as the parallel note |
| E4 | Photonic crystal fiber | knight1996 | staged | 3D process | capillaries stacked into a hexagon around a solid rod, drawn to cane, drawn to fiber, cross-section zooms to the lattice; guided mode | paper only |
| E4 | Microring resonator | little1997 | staged | 2.5D | bus guides, ring, input wavelength sweep, drop port lights at resonance; through / drop spectra plot | little1998 Si version as note |
| E5 | GHz silicon modulator | liu2004 | staged | 3D cross-section extrusion | SOI rib, gate oxide, poly-Si, MZI arms extrude from the cross-section, accumulation charge, phase shift plot | paper only |
| E5 | Kerr microcomb on a toroid | delhaye2007 | merged | 3D | Si pillar undercut, silica toroid reflow, tapered fiber approaches, pump in, comb lines assemble in the spectrum plot | armani2003 toroid process as reference |
| E6 | TFLN electro-optic modulator | wang2018b | staged | 3D cross-section extrusion | LN thin film on SiO2, ridge etch, gold electrodes, MZI layout, field overlap, Vpi and bandwidth plot | paper SI |
| E6 | Dissipative Kerr soliton | herr2014 | staged | 2.5D + plot | pump laser scan across the resonance, transmission steps assemble, intracavity pulse forms | brasch2016 as note |

Alternates if any pick fails the provenance check: southworth1936 (hollow metal waveguide), franken1961 (SHG),
kapron1970 (low-loss fiber), desurvire1987, yamada1993 (periodic poling), fang2006 (hybrid III-V/Si laser),
lindenmann2012 (photonic wire bond), sun2015 (monolithic CMOS photonics).

### 4a. Showcase spec (`data/history/showcases/<id>.yaml`, written by the research agents)

```yaml
id: maiman1960                 # = milestone paper_id
title: First laser             # <= 4 words, the hero keyword
tagline: ...                   # <= 12 words, factual
renderer: 3d                   # 3d | 2.5d
parts:                         # every visible body
  - id: ruby_rod
    name: Ruby rod             # source wording where the source names it
    role: ...                  # <= 12 words, hover line
    detail: ...                # <= 80 words, side panel
    quote: ...                 # verbatim source text that names / describes it (optional)
    locator: ...               # e.g. "maiman1960 p.493", "US 3,353,115 col. 3:10-22", URL
    material: ...
    look: {color: "#rrggbb", opacity: 1.0, metal: 0.0, rough: 0.5, emissive: ""}   # appearance for the renderer
    geometry: {type: cylinder, ...}   # mm; dims below give the basis of each number
    dims: [{label: diameter, value: 9.5, unit: mm, basis: stated|figure|ref|assumed, locator: ..., essential: false}]
    essential: true            # may carry an on-canvas label
assembly:                      # topology: placement of each part relative to others (axis, offsets in mm, basis)
  - {part: ruby_rod, pos: [0,0,0], axis: x, basis: ..., locator: ...}
chapters:                      # scroll script, p in [0,1], ordered, non-overlapping
  - {id: rod, p: [0.00, 0.14], keyword: "Ruby rod", line: "...", action: "rod flies in, rotates, silvered ends glint", parts: [ruby_rod]}
process:                       # process / recipe stories only
  - {id: deposit, name: ..., params: [{label, value, unit, basis, locator}], parts: [...]}
plots:
  - {id: spectrum, x: {label, unit, log: false}, y: {label, unit, log: false},
     series: [{name, basis: digitized|stated, locator, points: [[x, y], ...]}]}
drawings:                      # public-domain drawings to trace (patents, pre-1929)
  - {source: "US 3,353,115 FIG. 1", url, page, numerals: {"10": ruby_rod}}
references: [{id, cite, url, public_domain: true|false, used_for}]
withheld: [{what, reason}]     # parts or values the sources do not fix
```

### 5. Files

| path | content | owner |
|---|---|---|
| `data/history/showcases/<id>.yaml` | spec: parts (id, name, quote, locator), dims (value, unit, basis, locator), chapters (keyword, caption, p range), plot points (digitized, locator), withheld items with reason | research agent, then audit |
| `scripts/build_history_view.py` | also emits `app/static/data/showcases/<id>.json` and a `showcase` flag on milestones | coordinator |
| `app/src/lib/history/showcase/` | runtime: `ScrollStage.svelte`, scroll driver, part registry and linking, shared three.js renderer, 2.5D extruder, ported trace renderer, plot assembler | coordinator / framework agent |
| `app/src/lib/history/showcases/<id>.ts` | one scene module per pick: `build(ctx)`, `frame(p)`, `parts` | one builder agent per pick, owns only this file |
| `app/src/routes/history/+page.svelte` | view toggle, expanded layout | coordinator |

### 6. Phases and gates

1. **Proposal** (this DevLog). Owner answers Q1-Q6.
2. **Research wave** (subagents, one per pick, max 10 concurrent): sources and locators, dimensions with basis,
   part list, chapter script, digitized plot points, public-domain drawings to trace; writes the spec YAML + a
   `report.txt`. Staged picks also get their milestone row distilled and audited (DevLog-016 contract) so the
   timeline and the story agree.
3. **Framework + pilot** (in parallel with 2): view toggle, expanded layout, runtime, and two pilot stories: ruby
   laser (3D, exploded, traced patent drawing linked) and MCVD (3D process with recipe HUD). **Owner review gate.**
4. **Builder wave**: one agent per remaining pick, each owning its scene module; screenshots and frame strips at
   fixed `p` values for review.
5. **Audit**: fresh-context agent per era group against the sources (physics, topology, dimensions, captions);
   corrections recorded here.
6. Verify (Playwright screenshots at desktop and 390 px, reduced motion, frame-time check), then owner review.

## Questions for the owner

- Q1. Picks: accept the 16 in section 4, or swap / cut? (Alternates listed.)
- Q2. 7 of the 16 are core papers whose milestone rows are not merged yet (colladon1842, mears1987, knight1996,
  little1997, liu2004, wang2018b, herr2014; E6 has no merged milestone at all). Distill + audit those rows as part of
  this work (recommended), or limit picks to the 72 merged milestones (then E6 has no story)?
- Q3. Plots: re-plot digitized data from licensed figures in the public build (recommended; data with locator, no
  image), or only plot values stated in text / tables?
- Q4. Assumed secondary dimensions (e.g. flash-lamp wall thickness): show them flagged "assumed" (recommended), or
  withhold any part without a sourced dimension?
- Q5. Pilot gate: ruby laser + MCVD first, then fan out (recommended), or fan out all 16 at once?
- Q6. Add `three` (same major as advanced-packaging-atlas, lazy-loaded) as an app dependency: OK?

## Decisions

| id | decision | basis |
|---|---|---|
| D980 | Picks: the 16 in section 4 accepted | owner Q1 "sounds good" |
| D981 | The 7 staged picks get milestone rows: new batch `hist_19` (colladon1842, mears1987, knight1996, little1997, liu2004, herr2014, wang2018b; mode full, cut by hand with the `hist_make_batches.py` columns); herr2014 moved out of the undispatched `hist_11` (backup in the session scratchpad). Milestone rows audited and merged like batch 1; component rows stay staged until their full audit (D974 rule) | owner Q2 "add them into the milestones" |
| D982 | Plots are rebuilt from digitized points of licensed figures, with figure + page locator; no figure images in the public build. Purpose: owner's own learning and education | owner Q3 |
| D983 | Visual style: clean and elegant (Apple product page), not heavy technical. On the canvas only the core / critical dimensions and short keywords; all other technical content (quotes, locators, dimension tables, bases, recipe values) lives in hover tooltips and the click-open side panel. `essential: true` in the spec marks what may appear on the canvas | owner Q4 |
| D984 | Pilot gate: ruby laser (maiman1960) and MCVD (macchesney1974) built into the page first; owner reviews the final presentation and experience before the other 14 | owner Q5 |
| D985 | `three` added as an app dependency (lazy-loaded, same major as advanced-packaging-atlas) | owner Q6 |
| D986 | Wrong history tags (owner 2026-11-11: "many theory / no device ones actually have devices, like the 1975 LiNbO3 modulator ... clear from the abstract, fabricated"). Root cause: `build_history_view.py` derives `material` only from merged component rows; only hist_01 rows are merged (hist_04-09: 33 staged, unaudited, e.g. kaminow1975 in hist_08), and out-of-taxonomy devices (bulk / gas lasers, masers, fibers) never get rows; generic thread-like `topic` labels came from the candidate list. Fix: (a) sourced per-paper tag table (`kind` theory / device / process / measurement / system / review, `material`, specific `topic`, locator) read from each paper, staged in `data/_staging/history/tags/`, merged to `data/history/milestone_tags.csv`, and the build uses it before the component fallback; "theory / no device" only for `kind = theory`; (b) fresh-context audit of the staged hist_04-09 component rows, then patch and merge (zip backup, serialized) | owner correction |
| D987 | hist_19 distiller rulings: (1) DRI changes herr2014 -> "T. Herr; M. L. Gorodetsky; T. J. Kippenberg" and wang2018b -> "Cheng Wang; Mian Zhang; Marko Loncar" kept (D953: PI plus the person credited with doing the work, from the papers' contribution statements); (2) herr2014 / wang2018b dates stay empty (cached copies are arXiv v3 / accelerated preview; year used downstream) until the journal version is cached; (3) wang2018b 0.2 dB/cm deleted if the audit confirms it is quoted from ref. 28 (earlier work, not this chip); (4) liu2004 facet coupler keeps fab `org_intel` (same chip, the paper's own fabrication); (5) herr2014 MgF2 machined resonator excluded (D411 bulk resonator); (6) colladon1842 page renders are produced by the colladon showcase research later | coordinator |
| D988 | hist_19 audit (fresh context, `hist_19/audit.txt`): GO, 18 rows, 2 wrong (wang2018b 800 nm ridge row: 0.2 dB/cm quoted after ref. 28 = zhang2017a, deleted with its geometry-only metrics per skill rules 3 / 9), 2 imprecise (colladon1842 event now includes "follows the jet's bends"; knight1996 caption paraphrased). Rulings: wang2018b DRI stays per D987 (Winzer co-supervised, not added); liu2004 facet row platform stays `soi`. Patch applied (3 changes, re-run 0), zip backup `cache/components_backup/components_before_hist_19_20261111T214850Z.zip`, merged: milestones 79 rows, components +2 / metrics +2 | audit |
| D989 | hist_09 component audit (fresh context, `hist_09/comp_audit.txt`): GO, 92 rows, 0 wrong, 17 imprecise (waldhausl1997 7 couplers -> `fiber_chip_coupler.other` (free-space beam), polarization / basis / scope fixes on ilchenko1999, soref1986, schwartz1978). `hist_apply_patch.py` gained `--patch <file>` (component audits write `comp_audit_patch.csv`, coordinator notes `coord_patch.csv`). Rulings: ilchenko1999 microspheres stay `resonator.disk` (sub-mm, fiber-coupled, passive); vellekoop1991 fab empty (people only); schwartz1978 stays `fiber_interface.other`; soref1986 losses stay `prop_loss_db_per_cm` with coupling / end-face in `includes`; missing orgs (JPL as child of org_caltech, RADC, Western Electric ERC, Fraunhofer IOF) and the follow-up fab fixes go to the next org round; history view: material comes from the tag table (D986), never a long `core_material` string. Patched (23 + 1, re-run 0), zip backup `components_before_hist_09_20261111T214943Z.zip`, merged +18 components / +74 metrics | audit |
| D990 | hist_04 / 06 / 07 / 08 component audit (fresh context, `comp_audit.txt` per batch): all GO; 59 rows, 2 wrong (dakss1970 couplers -> `fiber_chip_coupler.other`, free-space), 15 imprecise (13 unit-converted values re-based `derived` per D157 / D256; kato1973 platform `silica`; somekh1973 note: 6.4 um is the channel period), 1 missing (holonyak1962 junction area 1e-3 cm2 -> `footprint_um2` 100000 approx derived, added by the coordinator). Rulings: quist1962 fab stays empty (staff thanked, no org printed; same as vellekoop1991); GE Syracuse / GE Schenectady / Thomson-CSF to the org round, then holonyak1962 / hall1962 / papuchon1975 fab; hayashi1970 derived thresholds kept (approx); kogelnik1971 -m2 kept as a process value; flagged visible-band inferences (dakss, martin) accepted; figure-reading rows keep `extracted_from_figure`; hall1962 temperature empty; nathan1962 `laser.other`; uchida1970 / tien1971 0 rows confirmed; coupling-coefficient parameter is a registry gap (somekh1973 K = 0.52 /mm waits for it). Patched (11 + 6 + 3), zip backup `components_before_hist_04_08_*.zip`, merged +15 components / +45 metrics. All batch-1 component rows are now merged | audit |
| D991 | Tag tables audited (fresh context, `data/_staging/history/tags/tags_audit.txt`): pass with corrections, 26 field changes on 25 of 79 rows (kind 1: kao1966 -> measurement; material 6: qualifiers dropped, Nd-doped glass; topic 17; thread 2: waldhausl1997 -> integrated optics, schwartz1978 -> PLC, WDM, EDFA, systems). Final kinds: device 39, theory 26, measurement 8, review 3, process 2, system 1. Canonical table `data/history/milestone_tags.csv` (paper_id, kind, material, topic, thread, locator, notes; 79 rows = milestones.csv). Build rule: topic / thread / material / kind from this table; material empty -> "theory / no device" only when kind = theory, else "not stated" | audit |
| D992 | MCVD spec rulings (research report `data/history/showcases/macchesney1974.report.txt`): the 1974 paper prints no recipe numbers and never says "MCVD"; recipe values come from MacChesney and O'Connor US 4,217,027 (application 1974-02-22, same work, public domain). (1) hero title "MCVD" kept (established name, as in the audited topic) with a side-panel note that the paper calls it a CVD-derived method; (2) the HUD shows patent Example 1 values, each labelled as a patent value with column:line; (3) main loss plot = the paper's Fig. 1 (digitized, D982), the patent FIG. 4 curve stays available in the side panel / plot toggle, not as a second hero plot | coordinator |
| D993 | Viewer-facing notes never cite DevLog / decision ids (`tests/test_views.py` INTERNAL rule); coordinator notes added in D989 / D990 were stripped of them | test |
| D994 | Runtime follow-up (framework agent): levels plots (`kind: levels`, LevelsDiagram.svelte), `scale: none` axes, filled `bars`, staggered series reveal, `chapters[].labels`, all essential dims on labels, lighter plot panel, `pick()` info for non-part elements; all additive | ruby pilot review |
| D995 | Ruby audit (fresh context, `data/history/showcases/maiman1960.audit.txt`): NO-GO until 3 fixes; 3 wrong, 9 imprecise, 2 missing, 15 ok; sources, quotes, locators, digitization and 3D topology verified. Rulings: (W1) quote the YAML axis label; (W2) Fig. 1 heights are schematic: schematic energy axis (`scale: none`), physical values (6943 / 6929 / 5500 A, 29 cm^-1) only in hover; pump arrow ends inside the band; levels drawn by the runtime; (W3) beam overlaps the bright flash, both decay together, final chapter is a deliberate frozen moment; lamp tube about 6 mm from the GE catalog FT 506 photo (basis ref), flash color cited to the catalog; a / b spectra labelled normalized with the caveat in hover; no non-essential numbers in chapter lines; per-chapter labels that say which number is the diameter; supply and leads fade in plot chapters; the beam never runs under the plot panel | audit + coordinator |
| D996 | (owner 2026-11-11: "this is great. Add a play button to the bottom controls so that each scrolling anime can plays itself") Play / Pause in each story's bottom controls: autoplay scrolls the page so p, scrub bar and chapters stay in sync; fixed move + dwell per chapter (longer dwell on plot chapters); pauses on any user scroll / drag / key / control, when the story leaves the viewport or the tab hides; stops at the story end; reduced motion = chapter jumps with dwell | owner request |
| D997 | (owner 2026-11-11: "overall style/design language update: avoid the LLM like vertical color bar/line on the left edge of elements. Use e.g. horizontal color bars instead, and thicker or as background. Follow style of [the owner's private two-page share PDF deck style]") Design language for the history tab (expanded, compact, stories, panels): no left-edge color bars or lines anywhere; color as horizontal bars (top rules 3-4px), filled chips or low-alpha background tints; editorial plate typography: display Playfair Display (era titles, story keywords), text Source Serif 4 (story lines, panel prose), small-caps kickers (letter-spacing .07em, muted), accent-colored section numbers, amber italic for the one emphasized phrase; scotch rules (2px over 1px, muted) above sections; booktabs tables (2px top, 1px bottom, no vertical rules); no shadows, glows or gradients in UI chrome; sharp corners; palette bg #0d0d0d, panel #1a1a19, ink #f2f1ec, muted #a8a69d, faint #898781, line #383835, blue #4c9bf0, amber #f7962c, green #46dca5, violet #c6a6fa, pink #ea70a3 (light theme keeps its tokens). Fonts self-hosted (OFL, license files shipped). The private reference is not named in the repo | owner request |
| D998 | MCVD audit (fresh context, `data/history/showcases/macchesney1974.audit.txt`): NO-GO until 3 fixes; 3 wrong (soot line said "fuse on the next pass", sources say as the zone passes; graded rings equal-area, paper fixes equal radius steps; rotation arrow turns against its head), 17 imprecise, 3 missing, 16 ok; locators, quotes and digitized plots verified. Rulings sent to the builder (pass 2): fix W1-W3; essential on-canvas numbers = tube 14 mm OD / 12 mm ID, 45 cm/min, about 1900 C, under 2 dB/km; core sinters behind the zone like the barrier; consistent barrier : core ratio; slower collapse traverse; preform 18 in; outlet straight per FIG. 1; withheld entries for draw orientation, collapse pass count, input / exhaust lengths; Example 4 temperatures in the side panel; dashed lambda^-4 guide; hero framing for the opening chapters; HUD values print basis + locator (runtime) | audit + coordinator |
| D999 | (owner 2026-11-11: "remove E0, E1 etc., they are nonsense LLM speak. Fine to keep in devlogs. Make this a global rule: no scratchpad/devlog shorthands in actual product") Era codes removed from the UI (expanded era header, compact band, detail-panel tag; the Era color mode keys its legend on the year span); the component-row tooltip no longer shows the internal component id; showcase locators cite "Maiman, Nature 1960, p.493" / "MacChesney et al., Proc. IEEE 62(9) p.1280" instead of paper ids (specs backed up in the session scratchpad first). Era ids stay as internal data keys in history.json, never rendered. Rule added to the owner's global instructions | owner request |
| D1000 | (owner 2026-11-11: "for the play mode, cut down the wait/pause between phases/stages to near zero") Play dwell 80 ms on every chapter (was 1.2 s, plot chapters 2.5 s); the move easing is near-linear (0.75 linear + 0.25 ease-in-out) so motion does not stop at chapter ends; reduced motion keeps a 1.5 s hold per chapter (it has no move). Measured on the production preview: ruby story plays in 33 s (was 46 s), longest stall 103 ms | owner request |

## TODO

- [x] Inspect history tab, milestones, ipatent tracing, pigeon / baby-mode / packaging references.
- [x] Proposal (this DevLog).
- [x] Owner answers Q1-Q6 (D980-D985).
- [x] hist_19 milestone distill, audit, merge (D981, D988).
- [x] Tag fix (D986, D991): tags wired into build_history_view.py (kind / material / topic / thread), history.json rebuilt 79 milestones: tag tables E0-E1, E2-E6 (+hist_19); component audits hist_04-08, hist_09; patch, merge, wire tags into the build; fresh audit of tags.
- [x] Research (pilot picks): maiman1960, macchesney1974 specs, traced patent drawings (D992).
- [x] Framework + pilot stories (D994, D996, D997); audits D995, D998 applied.
- [ ] Owner review of the pilot (presentation and experience).
- [ ] Research wave for the other 14 picks.
- [ ] Builder wave.
- [ ] Audit, verify, owner review.

## Progress log

- 2026-11-11: inspection and proposal written.
- 2026-11-11: owner answers recorded (D980-D985); hist_19 cut; phase A launched: hist_19 distiller, research agents ruby + MCVD, framework agent.
- 2026-11-11: owner flagged wrong tags; root cause and fix recorded (D986); 2 tag agents + 2 component auditors launched.
- 2026-11-11: hist_19 distilled (7 milestones, +3 components / +8 metrics, dry-runs 0 errors); rulings D987; fresh-context audit launched.
- 2026-11-11 13:49 PST: hist_19 audited, patched, merged (D988); history.json rebuild waits for the framework agent's build_history_view.py change and the tag audit.
- 2026-11-11 13:50 PST: hist_09 components audited, patched, merged (D989).
- 2026-11-11 13:54 PST: hist_04-08 components audited, patched, merged (D990); batch 1 components fully merged.
- 2026-11-11: maiman1960 spec done (10 parts, 9 chapters, Fig. 1 levels + Fig. 2 spectrum digitized, US 3,353,115 FIG. 4 traced 98.9 % / 2.1 % off-scan, 12 withheld items); builder waits for the framework.
- 2026-11-11 14:00 PST: tags wired, history.json rebuilt (79; 23 theory / no device = theory papers without a stated material); MCVD spec done (D992); ruby + MCVD builders running.
- 2026-11-11: ruby scene built; runtime follow-up (D994); ruby audit NO-GO -> fixes D995 sent to the builder (pass 2).
- 2026-11-11: ruby pass 2 done (all audit fixes except 2 runtime items); MCVD audit NO-GO -> pass 2 (D998); framework queue: round 3 (axis state, title_note, plot alternates, dashed, orbit limits, phone overlap), play button (D996), design language (D997), runtime needs from ruby pass 2, HUD locators.
- 2026-11-11 15:20 PST: pilot ready for owner review. Final coordinator check on the production build (`pnpm build` ok; three.js only in a dynamic chunk, history route node 74 KB; fonts 181 KB preloaded, ~346 KB in the expanded view): `pnpm check` 0 errors, `pnpm test` 689 passed, pytest 377 passed (full run after D993) and views / showcase 17 passed; Playwright shots of both stories at 1440x900 and 390x844 (chapters 1, 6, 8/9, 10), no console errors. Chapter text of the ruby levels / flash chapters switched to term symbols (Cr3+ -> superscript). Preview: `vite preview` on 127.0.0.1:47961 in tmux `atlas-history`. Nothing committed.

## Handoff

- Workflow, rules and contract distilled into the repo skill `.claude/skills/history-showcase/SKILL.md` (2026-11-11).
- Pilot files: specs `data/history/showcases/<id>.yaml` (+ `.report.txt`, `.audit.txt`), drawings / traces beside them; scene modules `app/src/lib/history/showcases/<id>.ts`; runtime `app/src/lib/history/showcase/` (contract and all options in `types.ts` doc comment and `README.txt`); expanded view `app/src/lib/history/Expanded.svelte`; fonts `app/static/fonts/` (OFL).
- Add a story: research agent writes the spec per section 4a (plus runtime fields in types.ts), builder writes the module, `uv run --offline python scripts/build_history_view.py --figures`, fresh-context audit against sources, fixes, screenshots.
- Tags: `data/history/milestone_tags.csv` (D991) must get a row for every new milestone (the build logs missing rows).
- Open: owner review; the other 14 picks (D980); org round for JPL, RADC, Western Electric ERC, Fraunhofer IOF, GE Syracuse / Schenectady, Thomson-CSF and the dependent fab fixes (D989, D990); herr2014 / wang2018b journal dates (D987); app-wide serif typography only if the owner wants it (D997 scoped to the history tab).
- 2026-11-11 15:55 PST: D999 applied; check 0 errors, 689 tests, build ok; rendered text of both views has 0 era codes, no console errors (preview restarted: vite preview had indexed the previous build's files).
