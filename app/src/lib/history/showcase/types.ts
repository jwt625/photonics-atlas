/**
 * History showcases (DevLog-017): spec types (static/data/showcases/<id>.json) and the scene module contract.
 *
 * ---------------------------------------------------------------------------------------------------------------------
 * HOW A STORY RUNS
 *
 * A showcase milestone (history.json `showcase: true`) whose id has a scene module in `../showcases/<id>.ts` gets a
 * story in the expanded history view: a tall section (`spec.height` viewport heights, default 5) holding a sticky
 * stage. While the section scrolls through the page's scroll container, the runtime (ShowcaseStory.svelte) maps the
 * scroll position to a progress p in [0, 1] and calls `handle.frame(p)`. The runtime owns everything around the model:
 * chapter keywords (spec.chapters[].keyword / line), the parts list, the traced drawing, the plot assembler, the
 * tooltip, the side panel, the step buttons, the scrub bar, the parts tour, the explode slider and orbit. The module
 * owns only the model: its geometry, materials, lights, camera pose and motion as a function of p.
 *
 * Reduced motion (prefers-reduced-motion): no scroll-linked motion; the section is one viewport tall and p jumps
 * between chapter ends through the step buttons. The module needs nothing special: it is still `frame(p)`.
 *
 * ---------------------------------------------------------------------------------------------------------------------
 * THE CONTRACT (one file per pick: src/lib/history/showcases/<id>.ts, `export default` a ShowcaseModule)
 *
 *   import type { ShowcaseModule } from '../showcase/types';
 *   const mod: ShowcaseModule = {
 *     renderer: '3d',                       // '3d' (three.js) or '2.5d' (SVG)
 *     build(ctx) { ...; return handle; }    // may be async
 *   };
 *   export default mod;
 *
 * Files under src/lib/history/showcases/ are registered automatically (import.meta.glob in ../showcases/index.ts);
 * the file name is the milestone id. A spec without a module, or a module without a spec, shows no story.
 *
 * Rules for a module (binding):
 * 1. PURE IN p. `frame(p)` sets every animated property from p alone (plus the stored explode amount k, see 5). It must
 *    give the same picture for the same p whichever way the user scrolled to it, and it may be called with any p in
 *    any order (scrub, step jumps, reverse scroll). No timers, no requestAnimationFrame, no accumulated deltas, no
 *    Math.random() at frame time (seed a PRNG in build if you need jitter). Precompute in build, evaluate in frame.
 * 2. NO RENDERING. 3D modules never call renderer.render, never create a WebGLRenderer, never touch the canvas: the
 *    runtime renders `ctx.scene` with `ctx.camera` after each frame / highlight / explode / resize, and only while the
 *    stage is on screen and holds the one shared renderer. 2.5D modules mutate their SVG (`ctx.svg`) inside frame.
 * 3. CAMERA. A 3D module sets `ctx.camera` (position, lookAt, fov) in frame(p) to direct the shot. Once p reaches
 *    `handle.assembledAt` the user may orbit / zoom; the runtime then restores its own camera pose after every
 *    frame(p) call, so the module keeps writing the camera without checking. `handle.target()` gives the orbit
 *    pivot (default: centre of the scene's bounding box).
 * 4. PARTS. Every pickable body carries a spec part id (spec.parts[].id). `pick(x, y)` returns the part id under the
 *    pointer (x, y in CSS px from the model pane's top-left corner; the pane size is the last resize(w, h)) or null.
 *    `highlight(ids)` shows the given parts as emphasized (hover plus pinned; empty = none). It must survive later
 *    frame(p) calls (store the ids, apply them in frame or keep the emphasis in separate material properties).
 * 5. EXPLODE (optional, 3D after assembly). The runtime calls `explode(k)` (k in [0, 1], user slider) and then
 *    frame(p) again: store k in explode, apply it in frame. With k = 0 the picture equals plain frame(p).
 * 6. ANCHORS (optional). `anchor(id)` returns the on-screen point [x, y] (pane px) of a part, or null when it is not
 *    visible. The runtime puts a small label there for parts with `essential: true` that belong to the current
 *    chapter (name + essential dims): that is the only text a module gets on the canvas (D983). Draw no text yourself.
 * 7. LOOK. Colours, opacity, metalness and roughness come from `part.look` in the spec; geometry from `part.geometry`
 *    and `spec.assembly` (mm). Do not invent dimensions or topology the spec does not carry (DevLog-017 section 3).
 *    `ctx.theme` / `handle.theme(t)` tell dark or light; the stage background is the page background (transparent
 *    canvas), so do not paint a background.
 * 8. DISPOSE. `dispose()` frees geometries, materials and textures the module created and removes what it added to
 *    ctx.scene / ctx.svg. `scene.environment` is shared by all stories: never dispose it.
 *
 * Context (ShowcaseContext3D / ShowcaseContext2D below): the spec, the three namespace (3D: `ctx.THREE`, already
 * loaded; never `import 'three'` at module top level, it would pull three.js into the page chunk), an empty scene
 * with a neutral environment map set (scene.environment, for metals) and no lights, a PerspectiveCamera, the pane
 * size, the theme and the reduced-motion flag. 2.5D gets an empty <svg> sized to the pane (viewBox = 0 0 w h on each
 * resize; set your own viewBox if you prefer fixed logical units).
 *
 * Additions (2026-11-11, all optional, backward compatible):
 * - pick() may return a PickInfo {id, label, detail} for scene elements that are not spec parts: the runtime shows
 *   label + detail as a tooltip and includes the id in highlight(ids); clicking it does nothing. Returning a spec part
 *   id (string, or PickInfo whose id is a part) behaves as before.
 * - chapters[].labels: part ids labelled on the canvas in that chapter (default: the chapter's essential parts); a
 *   label shows every essential dim of the part ("10 mm x 20 mm" when the units agree).
 * - plots: `kind: levels` (levels / splits / transitions, drawn by the runtime's SVG plot); axis `scale: none` (no
 *   printed scale) and `ticks` (step or list); series `bars` ([x0, x1, h] or {from, to, height, line}); series of a plot
 *   reveal staggered and overlapping instead of one after another. The plot panel sits on the right half of the pane
 *   (phone: bottom 56 %) during its chapter.
 *
 * Round 3 (2026-11-11, optional, backward compatible):
 * - spec.title_note: shown under the tagline in the story side panel.
 * - plots[].alt_of: <plot id> (+ optional plots[].label): an alternate of that plot; its chapter gets a toggle in the
 *   plot panel corner (main first, then alternates in spec order). Log / linear choices are kept per plot id.
 * - series style 'dashed' (dashed line, dashed legend swatch).
 * - Free orbit limits: polar [2, 88] deg from +y by default (no view from under the floor); override with
 *   spec.orbit {polar, azimuth, distance} or handle.orbit (handle wins). The camera snaps into the limits on first drag.
 *
 * Ruby pass 2 (2026-11-11, optional): transitions[].from_energy / to_energy (end inside a band); series[].color;
 * dims[].show_label / label_short (canvas label "dia. 10 mm, length 20 mm"); with axis scale none, tooltips print
 * "as drawn" instead of the drawn height.
 *
 * Round 4 (D997): chapters[].keyword may wrap one phrase in *asterisks* for the amber italic emphasis; process params
 * and steps may carry `source` (short source label printed with basis and locator in the step tooltip).
 * Ruby pass 3: canvas labels stay inside the pane (flip left of the anchor or clamp and wrap), so anchor() may return
 * any visible point; keywords are shown without their *markers* outside the big keyword; levels tooltips print
 * "as drawn" under y scale none (split values are printed values and stay).
 * Cobra audit (2026-11-11): plots[].note and dims[].note reach the viewer (line under the plot / under the dims row).
 * Text markup in prose, names, notes, labels, legends and tooltips: `_{...}` subscript, `^{...}` superscript (braces
 * required: r_{33}, r_{yzy}, L_{0}, O_{2}, Cr^{3+}); plain underscores and carets stay literal. Units keep their own
 * shorthand (`cm^-1`, `10^3`). Plain-text tooltips use Unicode sub / superscripts where every character has one.
 * Error bars and equal aspect (2026-11-11): series[].err / err_x (number = symmetric for all points, or per point
 * number | [lo, hi] | null; offsets in data units; on a log axis a low end at or below zero clamps to the axis floor);
 * whiskers with small caps in the series colour, revealed with their point; hover adds "+hi / -lo". plots[].aspect:
 * 'equal' letterboxes the data area so x and y data units have equal length (ignored with a log axis).
 * Drawings: drawings[].caption (source line under the drawing, default `source`) and drawings[].note (short caveat,
 * 2 lines, full text on hover); both take `_{}` / `^{}` markup.
 * Stems: series[].style 'stems' draws a vertical line from series[].stem_base (data units; default the y-range
 * minimum, on log y the axis floor) to each point, revealed point by point; series[].stem_cap adds a small top marker.
 * Works with err / err_x and log axes.
 * handle.plot(id): see ShowcaseHandle. pick() returning a PickInfo whose id is a spec part: the part tooltip shows as
 * usual with the PickInfo detail lines added under the role (markup-rendered), for per-part caveats.
 * Legend: series[].legend false hides an entry; series[].legend_group merges series into one row (shared colour unless
 * `color` is set); plots[].legend_note prints one line under the legend. A legend that would leave the data area under
 * 60 % of the plot panel wraps into columns, then shows "+N more". Swatches carry a 1 px neutral outline.
 * Plot pen (shared with the runtime, ./plot): `revealAt(spec, plotId, p)` gives each series' revealed fraction 0..1
 * and `penAt(spec, plotId, p)` each series' pen {series, index, x, y} (data units; null before it starts), both in
 * plotSeries(plot) order. Pass the plot id on screen (from handle.plot); an `alt_of` alternate uses its main plot's
 * chapter. Example (in frame(p)): `const pen = shownPlot ? penAt(spec, shownPlot, p)[0] : null; if (pen) setVoltage(pen.x);`
 * 3D environment: `scene.environment` (the shared room map) is set before build and before any render, every run;
 * handle.environmentIntensity scales it per story. Modules using `onBeforeCompile` must give the material a unique
 * `customProgramCacheKey()` (e.g. story id + material role): all stories share one renderer and its program cache.
 * Play button (runtime only): autoplay scrolls the page, so modules see ordinary frame(p) calls; nothing to do.
 *
 * Chapters: `chapterAt(spec.chapters, p)` and `chapterLocal(chapter, p)` (./progress) give the chapter under p and the
 * local progress q in [0, 1] inside it; `ease`, `clamp01`, `seg(p, a, b)` help to write piecewise motion.
 *
 * Minimal 3D example:
 *
 *   build({ THREE, scene, camera, spec }) {
 *     const rod = new THREE.Mesh(new THREE.CylinderGeometry(4.75, 4.75, 30, 48), new THREE.MeshStandardMaterial({ color: '#c02030' }));
 *     rod.userData.part = 'ruby_rod'; scene.add(rod, new THREE.HemisphereLight(0xffffff, 0x333333, 1.5));
 *     const ray = new THREE.Raycaster(); let w = 1, h = 1, k = 0;
 *     return {
 *       frame(p) { const q = seg(p, 0, 0.14); rod.position.x = (1 - ease(q)) * 80; rod.rotation.z = q * Math.PI;
 *                  rod.position.y = k * 20; camera.position.set(0, 20, 120); camera.lookAt(0, 0, 0); },
 *       highlight(ids) { rod.material.emissive.set(ids.includes('ruby_rod') ? '#402020' : '#000000'); },
 *       pick(x, y) { ray.setFromCamera(new THREE.Vector2((x / w) * 2 - 1, 1 - (y / h) * 2), camera);
 *                    return (ray.intersectObject(rod)[0]?.object.userData.part as string) ?? null; },
 *       resize(nw, nh) { w = nw; h = nh; },
 *       explode(nk) { k = nk; },
 *       dispose() { rod.geometry.dispose(); rod.material.dispose(); scene.remove(rod); }
 *     };
 *   }
 * ---------------------------------------------------------------------------------------------------------------------
 */
import type * as THREE_NS from 'three';

export type Basis = 'stated' | 'figure' | 'ref' | 'assumed' | 'derived';

export interface Dim {
	label: string;
	value: number | string;
	unit?: string;
	basis?: Basis | string;
	locator?: string;
	/** may appear on the canvas next to the part (D983) */
	essential?: boolean;
	/** on-canvas label shows the dim name: `label_short` if given (e.g. "dia."), else `label` when show_label is true */
	show_label?: boolean;
	label_short?: string;
	/** caveat shown under the row in the side panel dims table (e.g. "model assumption, not a measured depth") */
	note?: string;
}
export interface PartLook {
	color?: string;
	opacity?: number;
	metal?: number;
	rough?: number;
	emissive?: string;
}
export interface Part {
	id: string;
	name: string;
	role?: string;
	detail?: string;
	quote?: string;
	locator?: string;
	material?: string;
	look?: PartLook;
	/** renderer-specific shape, mm; free form for the module (`type` plus fields) */
	geometry?: { type?: string; [k: string]: unknown };
	dims?: Dim[];
	/** may carry an on-canvas label */
	essential?: boolean;
}
export interface Placement {
	part: string;
	pos?: number[];
	axis?: string;
	basis?: string;
	locator?: string;
	[k: string]: unknown;
}
export interface Chapter {
	id: string;
	/** [p0, p1] inside [0, 1]; ordered, non-overlapping (gaps allowed) */
	p: [number, number];
	keyword: string;
	line?: string;
	/** build note for the module author; not shown */
	action?: string;
	parts?: string[];
	/** id of a plot that assembles across this chapter (default: a plot whose id equals the chapter id) */
	plot?: string;
	/** id of a process step shown during this chapter (default: a process step whose id equals the chapter id) */
	process?: string;
	/** part ids that get an on-canvas label in this chapter (default: the chapter's `parts` with `essential: true`);
	 *  [] = no labels. Only parts with `essential: true` and an anchor() point are labelled. */
	labels?: string[];
}
export interface Param {
	label: string;
	value: number | string;
	unit?: string;
	basis?: string;
	locator?: string;
	/** short source label shown with the locator (e.g. "patent Example 1"); default: the step's source */
	source?: string;
}
export interface ProcessStep {
	id: string;
	name: string;
	/** short source label for the step's params that carry none */
	source?: string;
	params?: Param[];
	parts?: string[];
}
export interface Axis {
	label: string;
	/** unit text; `^` / `_` mark super / subscripts: "10^3 cm^-1", "cm^{-1}" */
	unit?: string;
	/** true: the axis starts on a log scale and the plot offers a log / linear toggle */
	log?: boolean;
	/** optional fixed range [min, max] in data units */
	range?: [number, number];
	/** 'none': the source prints no scale; no ticks, tick labels or grid, the axis line and title stay */
	scale?: 'none' | 'linear' | 'log';
	/** number = tick step (short marks at every step, labels at round values); array = explicit labelled ticks */
	ticks?: number | number[];
}
/** Error bar spec: symmetric number for all points, or per point number | [lo, hi] | null. */
export type ErrSpec = number | (number | [number, number] | null)[];
/** A filled bar of a bar-style series: object form or [x0, x1, height]. */
export interface Bar {
	from: number;
	to: number;
	height: number;
	/** short name shown in the tooltip (e.g. "R1") */
	line?: string;
}
export type BarInput = Bar | [number, number, number];
export interface Series {
	name: string;
	basis?: string;
	locator?: string;
	/** 'line' | 'points' | 'both' | 'dashed' (dashed line, no markers) | 'stems' (a vertical line from stem_base up to
	 *  each point, e.g. comb lines); default: 'line' above 40 points, else 'both' */
	style?: 'line' | 'points' | 'both' | 'dashed' | 'stems';
	/** stems: base in data units (default: the y-range minimum; on a log axis never below the axis floor) */
	stem_base?: number;
	/** stems: small cap marker at the top of each stem */
	stem_cap?: boolean;
	/** false: no legend entry for this series */
	legend?: boolean;
	/** series sharing a key share one legend row (swatch combines line and dot when the group has both; label from the
	 *  group's first series) and, unless they set `color`, the colour of that first series */
	legend_group?: string;
	points: [number, number][];
	/** filled bars (low-alpha fill, thin outline); when present they replace the series' line and markers */
	bars?: BarInput[];
	/** CSS colour override (default palette: blue, amber, green, violet, pink, tuned per theme) */
	color?: string;
	/** y error bars: one number (symmetric, every point) or one entry per point: number (symmetric), [lo, hi] (absolute
	 *  offsets below / above the value, data units) or null (no bar for that point) */
	err?: ErrSpec;
	/** x error bars, same forms as err */
	err_x?: ErrSpec;
}
/** kind: levels. One energy level (kind line) or band (kind band, energy [low, high]). */
export interface Level {
	id: string;
	/** term symbol; leading digits = superscript, trailing digits = subscript ("4A2", "2E", "Ē"); or ^{} / _{} markup */
	label?: string;
	kind?: 'line' | 'band';
	energy: number | [number, number];
	/** optional horizontal extent as fractions of the plot width [x0, x1] (default: lowest level full width, levels
	 *  named in `splits` in the right column, the rest in the left column) */
	x?: [number, number];
	basis?: string;
	locator?: string;
	note?: string;
}
export interface Split {
	/** two level ids; the bracket is labelled with the printed value, not the drawn gap */
	between: [string, string];
	value: number | string;
	unit?: string;
	basis?: string;
	locator?: string;
}
export interface Transition {
	from: string;
	to: string;
	label?: string;
	/** pump: solid arrow (pump colour); nonradiative: dashed grey; emission: red */
	kind?: 'pump' | 'nonradiative' | 'emission' | string;
	wavelength_A?: number;
	/** optional end points on the drawn energy scale (same units as y), e.g. a pump arrow ending inside a band */
	from_energy?: number;
	to_energy?: number;
	basis?: string;
	locator?: string;
}
export interface Plot {
	id: string;
	title?: string;
	/** alternate of another plot (its id): shown in that plot's chapter, chosen with a toggle in the plot panel corner */
	alt_of?: string;
	/** short name on the alternates toggle (default: title, else id), e.g. "Paper Fig. 1" / "Patent FIG. 4" */
	label?: string;
	/** caveat shown as a small muted line under the plot (full text in its hover), e.g. "calculated (Eq. (2)), not a
	 *  measurement" */
	note?: string;
	/** 'equal': one data unit on x spans the same length as one on y (data area letterboxed, centred); ignored when
	 *  either axis is on a log scale */
	aspect?: 'equal' | 'auto';
	/** one line printed under the legend (markup-rendered), e.g. "line: simulated, dots: measured" */
	legend_note?: string;
	/** 'xy' (default): x / y axes with series; 'levels': energy-level diagram (y axis, levels, splits, transitions) */
	kind?: 'xy' | 'levels';
	x?: Axis;
	y: Axis;
	series?: Series[];
	levels?: Level[];
	splits?: Split[];
	transitions?: Transition[];
}
export interface Drawing {
	source: string;
	url?: string;
	page?: number | string;
	/** printed reference numeral -> spec part id */
	numerals?: Record<string, string>;
	/** trace file name (static/data/showcases/traces/<trace>), ipatent trace schema */
	trace?: string;
	/** public-domain scan (static/data/showcases/drawings/<image>), shown under the trace when present */
	image?: string;
	/** source line under the drawing (e.g. "US 3,584,230 FIG. 1"); default: `source` */
	caption?: string;
	/** one short caveat under the drawing (2 lines, full text on hover), e.g. a different embodiment from the paper */
	note?: string;
}
export interface Reference {
	id: string;
	cite: string;
	url?: string;
	public_domain?: boolean;
	used_for?: string;
}
export interface Withheld {
	what: string;
	reason: string;
}
/** Orbit limits in degrees (polar from straight above: 0 = top view, 90 = horizon) and world units (distance). */
export interface OrbitLimits {
	polar?: [number, number];
	azimuth?: [number, number];
	distance?: [number, number];
}
export interface ShowcaseSpec {
	id: string;
	title: string;
	tagline?: string;
	/** note on the title / naming, shown under the tagline in the story side panel */
	title_note?: string;
	/** p of the frame used for the compact-view thumbnail (default: end of the last chapter before the first plot
	 *  chapter, i.e. the model assembled and no plot; without plot chapters the end of the last chapter) */
	thumb_p?: number;
	/** orbit limits for free orbit (default polar [2, 88] deg: never under the floor); the module may override */
	orbit?: OrbitLimits;
	renderer: '3d' | '2.5d';
	/** section height in viewport heights (default 5) */
	height?: number;
	parts: Part[];
	assembly?: Placement[];
	chapters: Chapter[];
	process?: ProcessStep[];
	plots?: Plot[];
	drawings?: Drawing[];
	references?: Reference[];
	withheld?: Withheld[];
}

// ------------------------------------------------------------------------------------------------- module contract

export type Theme = 'dark' | 'light';

interface ContextBase {
	spec: ShowcaseSpec;
	/** model pane size in CSS px at build time (later sizes arrive through resize) */
	width: number;
	height: number;
	theme: Theme;
	/** prefers-reduced-motion is set: p only jumps between chapter ends (frame stays the same function) */
	reduced: boolean;
}
export interface ShowcaseContext3D extends ContextBase {
	kind: '3d';
	/** the three.js namespace, already loaded (lazy chunk) */
	THREE: typeof THREE_NS;
	/** empty scene; `scene.environment` holds a neutral room environment map (dispose not needed), no lights */
	scene: THREE_NS.Scene;
	/** fov 30, near 0.1, far 10000 (mm units suggested); aspect kept by the runtime */
	camera: THREE_NS.PerspectiveCamera;
}
export interface ShowcaseContext2D extends ContextBase {
	kind: '2.5d';
	/** empty <svg> filling the model pane; viewBox `0 0 w h` unless the module sets its own */
	svg: SVGSVGElement;
}
export type ShowcaseContext = ShowcaseContext3D | ShowcaseContext2D;

export interface ShowcaseHandle {
	/** Set the whole picture for progress p in [0, 1]. Pure: same p (and stored explode k) = same picture. */
	frame(p: number): void;
	/** Emphasize these part ids (hover plus pinned); [] = none. Persist across frame calls. */
	highlight(ids: readonly string[]): void;
	/** Part id under the pane point (x, y) in CSS px, or null; or a PickInfo for a scene element that is not a spec part
	 *  (it gets a tooltip and is passed to highlight(), but is never pinned). */
	pick(x: number, y: number): string | PickInfo | null;
	/** Pane size changed (CSS px). 3D: the runtime already set camera.aspect and the renderer size. */
	resize(w: number, h: number): void;
	/** Free everything the module created. */
	dispose(): void;
	/** Optional: store the user explode amount k in [0, 1]; the runtime calls frame(p) right after. */
	explode?(k: number): void;
	/** Optional: on-screen anchor of a part (pane px) for its canvas label, or null when hidden. Called after frame. */
	anchor?(id: string): [number, number] | null;
	/** Optional: orbit pivot in world units (default: centre of the scene bounding box). */
	target?(): [number, number, number];
	/** Optional: the page theme changed. */
	theme?(t: Theme): void;
	/** Optional: id of the plot on screen (null = none), called whenever it changes (a chapter's plot appears or leaves,
	 *  the viewer switches to an `alt_of` alternate) and once on mount. Store the id only; frame(p) reads it, so the
	 *  picture stays a function of (p, selected plot id). The runtime redraws after the call. */
	plot?(id: string | null): void;
	/** p from which orbit / zoom and the explode slider are offered (default: start of the last chapter). */
	assembledAt?: number;
	/** Optional (3D): strength of the shared room environment for this story, applied to `ctx.scene.environmentIntensity`
	 *  before each render (default three.js 1). In three r186 `material.envMapIntensity` does not scale
	 *  `scene.environment`; use this instead. The value lives on the story's own scene, so other stories are unaffected. */
	environmentIntensity?: number;
	/** Optional orbit limits (degrees / world units); wins over spec.orbit. Polar is measured from +y (camera.up). */
	orbit?: OrbitLimits;
}

/** pick() result for a scene element that is not a spec part (or a part with a custom tooltip). */
export interface PickInfo {
	id: string;
	label: string;
	detail?: string | string[];
}

export interface ShowcaseModule {
	renderer: '3d' | '2.5d';
	build(ctx: ShowcaseContext): ShowcaseHandle | Promise<ShowcaseHandle>;
}
