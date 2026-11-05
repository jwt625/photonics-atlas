# Curated component layouts

Per-component drawings computed in micrometres after a paper's micrographs, SEMs, schematics and text have been read
(DevLog-013 D505-D508). Output: `app/static/data/layouts/<component_id>.json`, read by the layout viewer. Components with
a cell here show the drawing; others fall back to the generic template scene.

    uv run python scripts/layouts/build.py --only <cell file substring>

Worked example: `cells/awg_fan2025.py`. API: `lib.py`.

## What a cell must be

A layout engineer looking at the source figure and the drawing must recognise the same device. Topology first: number and
position of ports, add and drop buses, bend types and directions, S-bends, tapers and their direction, grating shape
(focusing arcs if focusing), MZI arms, folded or spiral routing, heaters with their leads and pads, contacts, vias,
doped regions, trenches, undercuts, facets. Then dimensions.

- One component only: the row of the metric table, not its neighbours in the paper (several devices share a paper; read
  the component's label and notes). Context needed to understand it (the MZI around a heater, the folded loopbacks) is
  drawn; long routing to facets or pads is truncated with a note.
- True scale, both axes equal. No stretching. Small features get their own views: `c.view("tip", "...", like="top",
  window=(x0, y0, x1, y1))`, which reuses the shapes of `top` at another zoom. Do not add insets.
- Views: `top` (the whole device with its access waveguides) and at least one `kind="xsec"` view with the true stack at a
  stated plane: substrate (truncated), BOX, core, slab, cladding, metal, vias, absorber, doping, air gaps as the paper
  shows them. Add detail views wherever a feature is invisible in `top`.
- `c.thumb = {"view": "top", "window": [x0, y0, x1, y1]}`: the window that shows the device best in a 300 x 120 px
  thumbnail at true scale (omit the window to fit the whole view).
- Paint order is shape order: substrate first, metal last. Use `layer=` from: substrate, oxide, slab, waveguide, overlay,
  absorber, doped, metal, via, trench. Materials: see `MATERIALS` in `lib.py`.
- Dense periodic structures: pass `lod=<feature size in um>` on each tooth, with a filled region shape under them, so
  they do not alias when zoomed out. Keep each output below about 250 KB: use `Route(..., tol=...)` for long large-radius
  structures, `tol` about 1/5 of the smallest feature visible at that scale, not finer.

## Where numbers come from

Every shape carries its sources (`row`, `stated`, `fig`, `assumed`; lists concatenate). This is the honesty rule of the
atlas and it is checked at build time.

1. `c.um("m18")`, `c.num("m14")`: from the metric table, by the row's short id. Never retype a value that has a row.
2. `stated("p.3 Sec. II", "what")`: a value printed in text, a table or a labelled figure that has no row.
3. `fig("Fig. 1(a)", "against the 200 um bar", "10 %")`: read off a figure with a scale bar or by ratio to a stated
   dimension, with its uncertainty. Measure from the image, do not guess; state how.
4. `assumed("why")`: anything else. Drawn dashed and listed on hover. Keep these few, say why, and never give an assumed
   value a dimension label. Assumed BOX, cladding and substrate bands are normal when the paper does not state them.

Add `c.check("what", drawn, source, rel)` for physical closure wherever possible: path lengths against a stated
length, drawn footprint against a stated footprint, array pitch times count against a stated width, implied n_eff from
the grating equation. A failing check stops the build: fix the geometry, do not loosen the limit to pass.

## Rules for the source material

The repo and the site are public; the sources are mostly not open access.

- Facts, dimensions and topology only. No figure, image or pixel trace goes into a cell or the output: geometry is
  computed from dimensions, never auto-traced from pixels. Reading a dimension or a shape off a figure is fine.
- No sentence copied from a paper into code, comments, notes or summaries. No addresses, no personal names in comments.
- Never edit the metric table, the staging data or the sources. A wrong value found while reading (a table value that
  contradicts the figure) is reported, not fixed, and not silently drawn: draw the row, or if it cannot be the drawn
  dimension, say so in a note and in your report.

## Where sources are

| source id | folder |
|---|---|
| `lit:<id>` | `references/<id>/` |
| `eo:<id>` | `../eo-modulator-atlas/references/<id>/` |
| `pk:<id>` | `../advanced-packaging-atlas/references/<id>/` |
| `ofc2026:<code>` | `../PlayGround/20260320_OFC/extracted_text/<code>-*.md`: text and captions only, images not available |

Each has `text.md`, `figures/figures.json`, and `figures/page_NN.png` plus `img_pNN_M.png`. Look at the images with the
Read tool. For an OFC paper, say in `sources` that the figures were not available ("text and captions only") and be
strict: what the text does not fix is assumed.
