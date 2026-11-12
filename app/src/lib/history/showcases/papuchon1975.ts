// Scene module: Cobra, the Ti:LiNbO3 electro-optic directional-coupler switch (Papuchon et al., Appl. Phys. Lett. 1975).
// Spec: data/history/showcases/papuchon1975.yaml. Contract: ../showcase/types.ts. Renderer 2.5D (SVG, axonometric).
//
// World units are the pixels of the paper's Fig. 5 plan drawing (X right along the guides, Y down the page = toward
// the viewer, Z up = crystal C axis); Fig. 5 is schematic, so nothing here carries a scale: only the printed a, b, c
// reach the canvas, through the runtime labels. Heights (slab, Ti film, resist, electrodes, guide depth) are
// schematic; the guide depth / width and electrode / guide ratios follow the Fig. 3a section drawing.
//
// Light: the guided power along the coupler is Eq. (2) of the paper evaluated per frame,
//   |E1|^2 = cos^2(s c x) + d2 / (d2 + 1) sin^2(s c x),  s = sqrt(d2 + 1),  d2 = (delta beta / 2c)^2,  c x = (pi / 2) x / L0,
// with the coupling region (Fig. 5, c = 3 mm, L0 about 1 mm) mapped to 0 ... 3 L0. 0 V: d2 = 0; 6 V: drawn for the
// Fig. 1 case delta beta = c sqrt(12) (d2 = 3); the paper does not state the delta beta reached at 6 V (hover says so).
// The faint glow left in the curved guide at 0 V marks the paper's "most of the guided light", not a value.
import { clamp01, ease, easeOut, lerp, seg } from '../showcase/progress';
import type { PickInfo, ShowcaseContext, ShowcaseHandle, ShowcaseModule, Theme } from '../showcase/types';

type P2 = [number, number];
type Rect = [number, number, number, number];
type Geo = Record<string, unknown>;

const NS = 'http://www.w3.org/2000/svg';
const DEG = Math.PI / 180;
const num = (v: unknown, d: number): number => (typeof v === 'number' && Number.isFinite(v) ? v : d);
const pts = (v: unknown, d: P2[]): P2[] =>
	Array.isArray(v) && v.every((q) => Array.isArray(q) && q.length === 2 && q.every((x) => typeof x === 'number')) && v.length > 1
		? (v as P2[]).map((q) => [q[0], q[1]] as P2)
		: d;
const rect4 = (v: unknown, d: Rect): Rect => (Array.isArray(v) && v.length === 4 && v.every((x) => typeof x === 'number') ? (v as Rect) : d);
let uid = 0;

// ------------------------------------------------------------------------------------------------ colours
interface Pal {
	subTop: string; subFront: string; subSide: string; subA: [number, number, number]; edge: string; edgeA: number;
	ti: string; tiSide: string; resist: string; guide: string; guideA: number; guideHi: string; guideLo: string;
	goldTop: string; goldFront: string; goldSide: string; goldEdge: string;
	light: string; lightCore: string; glowA: number; field: string; ink: string; inkSoft: string; accent: string;
	furnace: string; prism: string; prismEdge: string; uv: string; ion: string; box: string; boxEdge: string;
}
const PAL: Record<Theme, Pal> = {
	dark: {
		subTop: '#d9d3c4', subFront: '#d9d3c4', subSide: '#d9d3c4', subA: [0.17, 0.08, 0.12], edge: '#d9d3c4', edgeA: 0.42,
		ti: '#8e939a', tiSide: '#62666d', resist: '#c66f8e', guide: '#7fb6c8', guideA: 0.62, guideHi: '#a9dcff', guideLo: '#3f6f86',
		goldTop: '#c9a24a', goldFront: '#9a7426', goldSide: '#84631f', goldEdge: '#e6c878',
		light: '#36ff3c', lightCore: '#b8ffb4', glowA: 0.9, field: '#5aa6f5', ink: '#c3c2b7', inkSoft: '#898781', accent: '#3987e5',
		furnace: '#ff7a2a', prism: '#e9e2d0', prismEdge: '#d9d3c4', uv: '#b7a4ff', ion: '#a7a59c', box: '#3a3936', boxEdge: '#8a887f'
	},
	light: {
		subTop: '#b8ad94', subFront: '#8f866f', subSide: '#a39a82', subA: [0.2, 0.3, 0.26], edge: '#6d6758', edgeA: 0.75,
		ti: '#8c9096', tiSide: '#5e6268', resist: '#b0506f', guide: '#2f87a6', guideA: 0.62, guideHi: '#57b3e8', guideLo: '#1d4f66',
		goldTop: '#d4a640', goldFront: '#a87d22', goldSide: '#8f6a1d', goldEdge: '#6f5212',
		light: '#12a51c', lightCore: '#0b7a14', glowA: 0.55, field: '#2a6fc0', ink: '#52514e', inkSoft: '#6f6d68', accent: '#2a78d6',
		furnace: '#e0641c', prism: '#cfc6ad', prismEdge: '#6d6758', uv: '#6a4fd6', ion: '#6f6d68', box: '#d6d2c6', boxEdge: '#6f6d68'
	}
};
function hex(c: string): [number, number, number] {
	const h = c.replace('#', '');
	return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
}
function mix(a: string, b: string, t: number): string {
	const x = hex(a);
	const y = hex(b);
	const m = (i: number) => Math.round(x[i] + (y[i] - x[i]) * t).toString(16).padStart(2, '0');
	return `#${m(0)}${m(1)}${m(2)}`;
}

// ------------------------------------------------------------------------------------------------ plan geometry helpers
/** polyline with rounded corners (quadratic blend at each interior vertex), sampled */
function roundLine(p: P2[], maxR: number): P2[] {
	if (p.length < 3) return p;
	const out: P2[] = [p[0]];
	for (let i = 1; i < p.length - 1; i++) {
		const a = p[i - 1], v = p[i], b = p[i + 1];
		const la = Math.hypot(v[0] - a[0], v[1] - a[1]);
		const lb = Math.hypot(b[0] - v[0], b[1] - v[1]);
		const r = Math.min(maxR, 0.5 * la, 0.5 * lb);
		const s: P2 = [v[0] + ((a[0] - v[0]) / la) * r, v[1] + ((a[1] - v[1]) / la) * r];
		const e: P2 = [v[0] + ((b[0] - v[0]) / lb) * r, v[1] + ((b[1] - v[1]) / lb) * r];
		for (let k = 0; k <= 6; k++) {
			const t = k / 6;
			out.push([(1 - t) ** 2 * s[0] + 2 * (1 - t) * t * v[0] + t * t * e[0], (1 - t) ** 2 * s[1] + 2 * (1 - t) * t * v[1] + t * t * e[1]]);
		}
	}
	out.push(p[p.length - 1]);
	// adjacent rounded corners can meet in the same point: drop near-duplicates (a zero-length segment has no normal)
	return out.filter((q, i) => i === 0 || Math.hypot(q[0] - out[i - 1][0], q[1] - out[i - 1][1]) > 0.01);
}
/** outline polygon of a ribbon of width w around a centre line */
function ribbon(cl: P2[], w: number): P2[] {
	const L: P2[] = [];
	const R: P2[] = [];
	const n = cl.length;
	const segN = (i: number): P2 => {
		const a = cl[i], b = cl[i + 1];
		const l = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1;
		return [-(b[1] - a[1]) / l, (b[0] - a[0]) / l];
	};
	for (let i = 0; i < n; i++) {
		const n0 = segN(Math.max(0, i - 1));
		const n1 = segN(Math.min(n - 2, i));
		let nx = n0[0] + n1[0];
		let ny = n0[1] + n1[1];
		const l = Math.hypot(nx, ny) || 1;
		nx /= l;
		ny /= l;
		const m = 1 / Math.max(0.5, nx * n1[0] + ny * n1[1]);
		L.push([cl[i][0] + (nx * w * m) / 2, cl[i][1] + (ny * w * m) / 2]);
		R.push([cl[i][0] - (nx * w * m) / 2, cl[i][1] - (ny * w * m) / 2]);
	}
	return [...L, ...R.reverse()];
}
/** Sutherland-Hodgman clip of a plan polygon to xa <= X <= xb */
function clipX(poly: P2[], xa: number, xb: number): P2[] {
	const half = (inp: P2[], f: (q: P2) => number): P2[] => {
		const out: P2[] = [];
		for (let i = 0; i < inp.length; i++) {
			const a = inp[i], b = inp[(i + 1) % inp.length];
			const fa = f(a), fb = f(b);
			if (fa >= 0) out.push(a);
			if (fa >= 0 !== fb >= 0) {
				const t = fa / (fa - fb);
				out.push([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t]);
			}
		}
		return out;
	};
	return half(half(poly, (q) => q[0] - xa), (q) => xb - q[0]);
}
/** clip an X-monotone polyline to xa <= X <= xb */
function clipLineX(line: P2[], xa: number, xb: number): P2[] {
	const out: P2[] = [];
	for (let i = 0; i < line.length - 1; i++) {
		const a = line[i], b = line[i + 1];
		const lo = Math.max(xa, Math.min(a[0], b[0]));
		const hi = Math.min(xb, Math.max(a[0], b[0]));
		if (hi < lo) continue;
		const at = (x: number): P2 => {
			const t = b[0] === a[0] ? 0 : (x - a[0]) / (b[0] - a[0]);
			return [x, a[1] + (b[1] - a[1]) * t];
		};
		const s = at(a[0] < b[0] ? lo : hi);
		const e = at(a[0] < b[0] ? hi : lo);
		if (!out.length) out.push(s);
		out.push(e);
	}
	return out;
}

// ------------------------------------------------------------------------------------------------ camera
interface Shot {
	az: number;
	el: number;
	zoom: number;
	/** world focus point placed at (fx, fy) of the region; null = centre of the fit box */
	focus: [number, number, number] | null;
	region: 'full' | 'plot';
	fx: number;
	fy: number;
}
interface Cam {
	ca: number;
	sa: number;
	ce: number;
	se: number;
	s: number;
	ox: number;
	oy: number;
}

// ------------------------------------------------------------------------------------------------ module
const mod: ShowcaseModule = {
	renderer: '2.5d',
	build(ctx: ShowcaseContext): ShowcaseHandle {
		if (ctx.kind !== '2.5d') throw new Error('papuchon1975 is a 2.5D scene');
		const { svg, spec } = ctx;
		const id = `cobra${++uid}`;
		let w = Math.max(1, ctx.width);
		let h = Math.max(1, ctx.height);
		let theme: Theme = ctx.theme;
		let k = 0;
		let hi: string[] = [];

		// ---------------------------------------------------------------------------- chapters
		const fallback: Record<string, [number, number]> = {
			substrate: [0, 0.08], titanium: [0.08, 0.17], strips: [0.17, 0.28], diffusion: [0.28, 0.38], electrodes: [0.38, 0.48],
			crossover: [0.48, 0.6], field: [0.6, 0.7], switch: [0.7, 0.82], power: [0.82, 1]
		};
		const C: Record<string, [number, number]> = {};
		for (const [cid, r] of Object.entries(fallback)) C[cid] = (spec.chapters.find((c) => c.id === cid)?.p ?? r) as [number, number];
		const cq = (cid: string, p: number) => seg(p, C[cid][0], C[cid][1]);

		// ---------------------------------------------------------------------------- geometry from the spec (fig5_px)
		const geo = (pid: string): Geo => (spec.parts.find((q) => q.id === pid)?.geometry ?? {}) as Geo;
		const g1 = geo('guide_1');
		const g2 = geo('guide_2');
		const gw = num(g1.drawn_width_px, 15);
		const cl1 = roundLine(pts(g1.centerline, [[200, 130], [230, 131], [705, 131], [740, 124], [775, 108], [805, 85], [825, 62], [833, 47]]), 26);
		const cl2 = roundLine(pts(g2.centerline, [[196, 250], [199, 229], [207, 210], [215, 199], [230, 183.5], [245, 174], [260, 168], [285, 165], [820, 165]]), 26);
		const lg = geo('launch_region');
		const lr = rect4(lg.rect, [17, 92, 168, 169]);
		const lt = (lg.taper ?? {}) as Geo;
		const ltFy = pts([lt.from_y, lt.to_y], [[100, 160], [120, 141]]);
		const launchPoly: P2[][] = [
			[[lr[0], lr[1]], [lr[2], lr[1]], [lr[2], lr[3]], [lr[0], lr[3]]],
			[[num(lt.from_x, 168), ltFy[0][0]], [num(lt.to_x, 200), ltFy[1][0]], [num(lt.to_x, 200), ltFy[1][1]], [num(lt.from_x, 168), ltFy[0][1]]]
		];
		const og = geo('output_region');
		const orr = rect4(og.rect, [860, 128, 1008, 204]);
		const ot = (og.taper ?? {}) as Geo;
		const otFy = pts([ot.from_y, ot.to_y], [[158, 173], [128, 204]]);
		const outPoly: P2[][] = [
			[[num(ot.from_x, 820), otFy[0][0]], [num(ot.to_x, 860), otFy[1][0]], [num(ot.to_x, 860), otFy[1][1]], [num(ot.from_x, 820), otFy[0][1]]],
			[[orr[0], orr[1]], [orr[2], orr[1]], [orr[2], orr[3]], [orr[0], orr[3]]]
		];
		const cg = geo('coupling_region');
		const cr = rect4(cg.rect, [285, 35, 744.5, 263]);
		const dimY = num(cg.dim_line_y, 304);
		const X0c = cr[0];
		const X1c = cr[2];
		const og2 = geo('observation_region');
		const obsC = pts([og2.center, [0, 0]], [[763, 150], [0, 0]])[0];
		const obsR = num(og2.r, 62);
		// parallel section: where guide_2 has reached its straight line and guide_1 has not yet left it
		const y1 = cl1.find((q) => q[0] >= X0c + 1)?.[1] ?? 131;
		const y2 = cl2[cl2.length - 1][1];
		const gapIn1 = y1 + gw / 2; // inner edge of the curved guide
		const gapIn2 = y2 - gw / 2; // inner edge of the straight guide
		const yg = (gapIn1 + gapIn2) / 2; // centre of the gap
		const bendAt = (() => {
			for (let i = 1; i < cl1.length; i++) if (cl1[i][0] > X0c + 20 && Math.abs(cl1[i][1] - y1) > 0.6) return cl1[i - 1][0];
			return 705;
		})();
		const parStart = (() => {
			for (let i = cl2.length - 1; i > 0; i--) if (Math.abs(cl2[i][1] - y2) > 0.6) return cl2[i + 1]?.[0] ?? X0c;
			return X0c;
		})();
		// section proportions from Fig. 3a (drawn, schematic): guide depth / width, electrode thickness / guide width
		const fl = geo('field_lines');
		const gh = (Array.isArray(fl.guides_half_ellipse) ? fl.guides_half_ellipse[0] : null) as Geo | null;
		const ghx = pts([gh?.x, [0, 0]], [[259, 350], [0, 0]])[0];
		const surf = num(fl.surface_y, 237.5);
		const depthRatio = (num(gh?.bottom_y, 306) - surf) / Math.max(1, ghx[1] - ghx[0]);
		const elec = (Array.isArray(fl.electrodes) ? fl.electrodes[0] : null) as number[] | null;
		const elecRatio = elec && elec.length === 4 ? (elec[3] - elec[1]) / Math.max(1, ghx[1] - ghx[0]) : 0.33;

		// schematic heights and stand-in sizes (assumed; no values in the paper)
		const SUB: Rect = [0, 8, 1032, 326]; // slab plan (stand-in)
		const T = 44; // slab thickness, drawn
		const HF = 2.4; // Ti film / strips, drawn
		const HR = 4; // resist, drawn
		const HE = Math.max(3, elecRatio * gw); // electrode thickness, drawn (Fig. 3a ratio)
		const GW = gw * 1.25; // diffused guide wider than the strip (lateral diffusion, p.290 col. 2), drawn
		const GD = depthRatio * gw; // guide depth on the section, drawn (Fig. 3a ratio)
		const EW = 60; // electrode width, drawn (printed 1 mm not drawable in Fig. 5 proportions)
		// electrodes: the 3 mm coupling region c (printed 1 x 3 mm); inner edges over the guide inner edges (assumed)
		const e1: Rect = [X0c, gapIn1 - EW, X1c, gapIn1];
		const e2: Rect = [X0c, gapIn2, X1c, gapIn2 + EW];
		void bendAt;
		void parStart;
		const XC = (X0c + X1c) / 2; // section cut: middle of the coupling region
		const SLW = 34; // section slice thickness along X, drawn
		const SLY = 96; // section slice half width across the guides, drawn
		const LIFT = 34; // slice lift
		const SPOT = lr[0] + 0.62 * (lr[2] - lr[0]); // prism coupling spot in the launching region
		const XEND = orr[2];
		const PR = { x0: lr[0] + 22, x1: lr[2] - 20, y0: lr[1] + 4, y1: lr[3] - 4, hgt: 46 }; // prism stand-in
		const EX = { guides: 45, electrodes: 120, prism: 190 }; // explode lifts (drawn units)
		const VB = { x0: 560, x1: 650, y0: -96, y1: -40, z1: -T + 30 }; // voltage stand-in (behind the slab)

		const strip1 = ribbon(cl1, gw);
		const strip2 = ribbon(cl2, gw);
		const chan1 = ribbon(cl1, GW);
		const chan2 = ribbon(cl2, GW);
		const grow = (poly: P2[], d: number): P2[] => {
			const cx = poly.reduce((a, q) => a + q[0], 0) / poly.length;
			const cy = poly.reduce((a, q) => a + q[1], 0) / poly.length;
			return poly.map((q) => [q[0] + Math.sign(q[0] - cx) * d, q[1] + Math.sign(q[1] - cy) * d] as P2);
		};
		const launchChan = launchPoly.map((q) => grow(q, (GW - gw) / 2));
		const outChan = outPoly.map((q) => grow(q, (GW - gw) / 2));

		// ---------------------------------------------------------------------------- light (Eq. 2)
		const P1 = (L: number, d2: number): number => {
			const s = Math.sqrt(d2 + 1);
			const a = (Math.PI / 2) * L * s;
			const c = Math.cos(a);
			const sn = Math.sin(a);
			return c * c + (d2 / (d2 + 1)) * sn * sn;
		};
		const Lof = (X: number) => (3 * (X - X0c)) / (X1c - X0c);
		/** power in the curved (1) and straight (2) guide at X for mismatch d2; residue = 0 V output glow floor */
		const power = (X: number, d2: number, residue: number): [number, number] => {
			if (X < X0c) return [1, 0];
			const L = Math.min(3, Lof(X));
			const a = P1(L, d2);
			if (X <= X1c) return [a, 1 - a];
			const f = residue * seg(X, X1c, X1c + 40);
			return [a + f * (1 - a), 1 - a];
		};
		const NSTOP = 150;
		const XS = Array.from({ length: NSTOP }, (_, i) => lerp(lr[0], XEND + 4, i / (NSTOP - 1)));

		// ---------------------------------------------------------------------------- SVG scaffolding
		const mk = <K extends keyof SVGElementTagNameMap>(tag: K, parent: Element, attrs: Record<string, string | number> = {}): SVGElementTagNameMap[K] => {
			const e = document.createElementNS(NS, tag) as SVGElementTagNameMap[K];
			for (const [a, v] of Object.entries(attrs)) e.setAttribute(a, String(v));
			parent.appendChild(e);
			return e;
		};
		const root = mk('g', svg, { 'data-scene': 'cobra' });
		const defs = mk('defs', root);
		const blur = mk('filter', defs, { id: `${id}-glow`, filterUnits: 'userSpaceOnUse', 'color-interpolation-filters': 'sRGB' });
		const blurStd = mk('feGaussianBlur', blur, { stdDeviation: 3 });
		const blur2 = mk('filter', defs, { id: `${id}-soft`, filterUnits: 'userSpaceOnUse', 'color-interpolation-filters': 'sRGB' });
		const blurStd2 = mk('feGaussianBlur', blur2, { stdDeviation: 1.2 });
		const mkLin = (gid: string) => {
			const g = mk('linearGradient', defs, { id: `${id}-${gid}`, gradientUnits: 'userSpaceOnUse' });
			const stops = XS.map((_, i) => mk('stop', g, { offset: (i / (NSTOP - 1)).toFixed(4), 'stop-color': '#36ff3c', 'stop-opacity': 0 }));
			return { g, stops };
		};
		const lin1 = mkLin('l1');
		const lin2 = mkLin('l2');
		const mkRad = (gid: string) => {
			const g = mk('radialGradient', defs, { id: `${id}-${gid}`, gradientUnits: 'userSpaceOnUse', cx: 0, cy: 0, r: 1, fx: 0, fy: 0 });
			const s = [0, 0.45, 1].map((o) => mk('stop', g, { offset: o, 'stop-color': '#7fb6c8', 'stop-opacity': 0 }));
			return { g, s };
		};
		const rad1 = mkRad('r1');
		const rad2 = mkRad('r2');

		type PathEl = SVGPathElement;
		const pick = (e: SVGElement, part: string) => {
			e.setAttribute('data-pick', part);
			return e;
		};
		const path = (parent: Element, part: string | null, attrs: Record<string, string | number> = {}): PathEl => {
			const e = mk('path', parent, { 'stroke-linejoin': 'round', 'stroke-linecap': 'round', ...attrs });
			if (part) pick(e, part);
			return e;
		};
		const show = (e: SVGElement, o: number) => {
			if (o < 0.01) {
				if (e.style.display !== 'none') e.style.display = 'none';
				return false;
			}
			if (e.style.display) e.style.display = '';
			e.setAttribute('opacity', o >= 0.999 ? '1' : o.toFixed(3));
			return true;
		};

		// ---------------------------------------------------------------------------- pieces (main = right of the cut)
		interface Box {
			top: PathEl;
			front: PathEl;
			side: PathEl;
		}
		const box = (parent: Element, part: string): Box => ({ front: path(parent, part), side: path(parent, part), top: path(parent, part) });
		interface Piece {
			g: SVGGElement;
			sub: Box;
			furnace: PathEl;
			/** section face content (main piece only) */
			slot: SVGGElement;
			chans: PathEl[];
			stripLo: PathEl;
			stripHi: PathEl;
			filmSheet: Box;
			resistSheet: Box;
			resistPat: PathEl;
			/** annotations and light between the surface and the electrodes (main piece only) */
			mid: SVGGElement;
			e1: Box;
			e2: Box;
			/** gold film over the whole surface, its resist and the pad-shaped resist (Fig. 4 row 4), above the pads */
			goldSheet: Box;
			goldResist: Box;
			goldResistPat: PathEl;
			/** over the electrodes (slice piece: C axis in the gap) */
			over: SVGGElement;
		}
		const mkPiece = (): Piece => {
			const g = mk('g', root);
			const sub = box(g, 'substrate');
			const furnace = path(g, null, { 'pointer-events': 'none' });
			const slot = mk('g', g);
			const chanG = mk('g', g);
			const chans = [path(chanG, 'launch_region'), path(chanG, 'guide_1'), path(chanG, 'guide_2'), path(chanG, 'output_region')];
			const stripLo = path(g, 'ti_strips');
			const stripHi = path(g, 'ti_strips');
			const filmSheet = box(g, 'ti_film');
			const resistSheet = box(g, 'resist');
			const resistPat = path(g, 'resist');
			const mid = mk('g', g);
			const eg = mk('g', g);
			const e1b = box(eg, 'electrode_1');
			const e2b = box(eg, 'electrode_2');
			const goldSheet = box(eg, 'gold_film');
			const goldResist = box(eg, 'resist');
			const goldResistPat = path(eg, 'resist');
			return { g, sub, furnace, slot, chans, stripLo, stripHi, filmSheet, resistSheet, resistPat, mid, e1: e1b, e2: e2b, goldSheet, goldResist, goldResistPat, over: mk('g', g) };
		};
		// voltage stand-in sits behind the slab: drawn first
		const vg = mk('g', root);
		const vBox = box(vg, 'voltage');
		const vMeter = path(vg, 'voltage');
		const vKnob = path(vg, 'voltage');
		const main = mkPiece();
		// annotations and light, between the surface and the electrodes
		const mid = main.mid;
		const outline = path(mid, null, { fill: 'none', 'stroke-dasharray': '5 4', 'pointer-events': 'none' });
		const outlineHit = path(mid, 'coupling_region', { fill: 'none', stroke: 'transparent', 'stroke-width': 9 });
		const dimLine = path(mid, 'coupling_region', { fill: 'none' });
		const obs = path(mid, null, { fill: 'none', 'stroke-dasharray': '4 4', 'pointer-events': 'none' });
		const obsHit = path(mid, 'observation_region', { fill: 'none', stroke: 'transparent', 'stroke-width': 9 });
		const glowG = mk('g', mid, { 'pointer-events': 'none' });
		const glowSoft = mk('g', glowG, { filter: `url(#${id}-glow)` });
		const glowCore = mk('g', glowG);
		const lightPaths = (g: SVGGElement) => ({
			launch: path(g, null, { fill: `url(#${id}-l1)`, stroke: 'none' }),
			g1: path(g, null, { fill: 'none', stroke: `url(#${id}-l1)` }),
			g2: path(g, null, { fill: 'none', stroke: `url(#${id}-l2)` }),
			out: path(g, null, { fill: `url(#${id}-l2)`, stroke: 'none' })
		});
		const LS = lightPaths(glowSoft);
		const LC = lightPaths(glowCore);
		const lightHit = [
			path(mid, 'guided_light', { fill: 'none', stroke: 'transparent' }),
			path(mid, 'guided_light', { fill: 'none', stroke: 'transparent' })
		];
		const ghost = box(mid, 'central_electrode');
		// electrodes of the main piece are in main.e1 / main.e2 (after mid); leads, axis, prism, beam, arrows on top
		const topG = mk('g', root);
		const leads = [path(topG, 'voltage', { fill: 'none' }), path(topG, 'voltage', { fill: 'none' })];
		const cAxis = { line: path(topG, 'c_axis', { fill: 'none' }), head: path(topG, 'c_axis'), hit: path(topG, 'c_axis', { fill: 'none', stroke: 'transparent', 'stroke-width': 10 }) };
		const prismG = mk('g', topG);
		const prism = { right: path(prismG, 'prism'), left: path(prismG, 'prism'), front: path(prismG, 'prism') };
		const beamG = mk('g', topG, { 'pointer-events': 'none' });
		const beamSoft = path(beamG, null, { fill: 'none', filter: `url(#${id}-glow)` });
		const beamCore = path(beamG, null, { fill: 'none' });
		const beamHit = path(topG, 'argon_beam', { fill: 'none', stroke: 'transparent', 'stroke-width': 10 });
		const fluxG = mk('g', topG, { 'pointer-events': 'none' });
		const NFLUX = 22;
		const flux = Array.from({ length: NFLUX }, () => ({ l: path(fluxG, null, { fill: 'none' }), hd: path(fluxG, null) }));
		// section slice (lifted out of the middle of the coupler) and the left piece (nearer the viewer): drawn last
		const slice = mkPiece();
		const left = mkPiece();
		// section face (slice piece, its -X face at the cut): graded guides, field lines, C axis
		const secG = slice.slot;
		const sec1 = path(secG, 'guide_1', { fill: `url(#${id}-r1)` });
		const sec2 = path(secG, 'guide_2', { fill: `url(#${id}-r2)` });
		const secStrip = [path(secG, 'ti_strips'), path(secG, 'ti_strips')];
		const fieldG = mk('g', secG);
		const FL = [0, 1, 2].map(() => ({
			line: path(fieldG, 'field_lines', { fill: 'none', pathLength: 1 }),
			hitW: path(fieldG, 'field_lines', { fill: 'none', stroke: 'transparent', 'stroke-width': 9 }),
			a: path(fieldG, 'field_lines'),
			b: path(fieldG, 'field_lines')
		}));
		const cFace = { line: path(slice.over, 'c_axis', { fill: 'none' }), head: path(slice.over, 'c_axis') };


		// seeded flux arrow positions over the slab (pure: fixed at build)
		let seed = 1975;
		const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
		const fluxPos = Array.from({ length: NFLUX }, (_, i) => ({
			x: lerp(SUB[0] + 40, SUB[2] - 40, (i + 0.5) / NFLUX + (rnd() - 0.5) * 0.03),
			y: lerp(SUB[1] + 40, SUB[3] - 40, rnd()),
			ph: rnd()
		}));

		// ---------------------------------------------------------------------------- camera
		const regions = (): { full: Rect; plot: Rect } => {
			if (w < 700) return { full: [0.04, 0.2, 0.96, 0.95], plot: [0.04, 0.2, 0.96, 0.43] };
			const top = Math.min(0.26, 170 / Math.max(1, h));
			return { full: [0.04, top, 0.97, 0.93], plot: [0.02, top + 0.04, 0.46, 0.9] };
		};
		// fit box: slab plus the stand-ins around it
		const FIT = { x0: SUB[0] - 30, x1: SUB[2] + 10, y0: VB.y0, y1: SUB[3] + 6, z0: -T, z1: 40 };
		const ISO: Shot = { az: -30, el: 33, zoom: 1, focus: null, region: 'full', fx: 0.5, fy: 0.5 };
		const SHOTS: Record<string, Shot> = {
			arrive: { az: -6, el: 72, zoom: 0.8, focus: null, region: 'full', fx: 0.5, fy: 0.5 },
			iso: ISO,
			light: { az: -24, el: 44, zoom: 1, focus: null, region: 'full', fx: 0.5, fy: 0.5 },
			diffusion: { az: -60, el: 24, zoom: 5.2, focus: [XC, yg, LIFT - GD * 0.8], region: 'full', fx: 0.52, fy: 0.56 },
			field: { az: -62, el: 20, zoom: 5, focus: [XC, yg, LIFT - GD * 1.4], region: 'full', fx: 0.52, fy: 0.55 },
			plot: { az: -24, el: 44, zoom: 1, focus: null, region: 'plot', fx: 0.5, fy: 0.5 }
		};
		const projRaw = (az: number, el: number, X: number, Y: number, Z: number): P2 => {
			const ca = Math.cos(az * DEG), sa = Math.sin(az * DEG);
			return [X * ca - Y * sa, (X * sa + Y * ca) * Math.sin(el * DEG) - Z * Math.cos(el * DEG)];
		};
		const camOf = (sh: Shot): Cam => {
			const rg = regions()[sh.region];
			const rx0 = rg[0] * w, ry0 = rg[1] * h, rw = (rg[2] - rg[0]) * w, rh = (rg[3] - rg[1]) * h;
			let x0 = Infinity, x1 = -Infinity, yy0 = Infinity, yy1 = -Infinity;
			for (const X of [FIT.x0, FIT.x1]) for (const Y of [FIT.y0, FIT.y1]) for (const Z of [FIT.z0, FIT.z1]) {
				const q = projRaw(sh.az, sh.el, X, Y, Z);
				x0 = Math.min(x0, q[0]); x1 = Math.max(x1, q[0]); yy0 = Math.min(yy0, q[1]); yy1 = Math.max(yy1, q[1]);
			}
			// phone: the section close-ups pull back a little so both electrodes stay in the pane
			const s = Math.min(rw / (x1 - x0), rh / (yy1 - yy0)) * (w < 700 && sh.zoom > 2 ? sh.zoom * 0.8 : sh.zoom);
			const f = sh.focus ? projRaw(sh.az, sh.el, ...sh.focus) : ([(x0 + x1) / 2, (yy0 + yy1) / 2] as P2);
			return {
				ca: Math.cos(sh.az * DEG), sa: Math.sin(sh.az * DEG), ce: Math.cos(sh.el * DEG), se: Math.sin(sh.el * DEG), s,
				ox: rx0 + sh.fx * rw - s * f[0], oy: ry0 + sh.fy * rh - s * f[1]
			};
		};
		/** blend two shots: angles and zoom in shot space, then screen offset blend (keeps both ends exact) */
		const blendCam = (a: Shot, b: Shot, t: number): Cam => {
			if (t <= 0) return camOf(a);
			if (t >= 1) return camOf(b);
			const ca = camOf(a), cb = camOf(b);
			const az = lerp(a.az, b.az, t), el = lerp(a.el, b.el, t);
			const s = Math.exp(lerp(Math.log(ca.s), Math.log(cb.s), t));
			// keep the blended focus world point moving smoothly on screen
			const fa = a.focus ?? [(FIT.x0 + FIT.x1) / 2, (FIT.y0 + FIT.y1) / 2, (FIT.z0 + FIT.z1) / 2];
			const fb = b.focus ?? [(FIT.x0 + FIT.x1) / 2, (FIT.y0 + FIT.y1) / 2, (FIT.z0 + FIT.z1) / 2];
			const fw: [number, number, number] = [lerp(fa[0], fb[0], t), lerp(fa[1], fb[1], t), lerp(fa[2], fb[2], t)];
			const sa0 = projRaw(a.az, a.el, ...fw), sb0 = projRaw(b.az, b.el, ...fw);
			const pa: P2 = [ca.ox + ca.s * sa0[0], ca.oy + ca.s * sa0[1]];
			const pb: P2 = [cb.ox + cb.s * sb0[0], cb.oy + cb.s * sb0[1]];
			const pf: P2 = [lerp(pa[0], pb[0], t), lerp(pa[1], pb[1], t)];
			const r = projRaw(az, el, ...fw);
			return { ca: Math.cos(az * DEG), sa: Math.sin(az * DEG), ce: Math.cos(el * DEG), se: Math.sin(el * DEG), s, ox: pf[0] - s * r[0], oy: pf[1] - s * r[1] };
		};
		let cam: Cam = camOf(ISO);
		const P = (X: number, Y: number, Z: number): P2 => [
			cam.ox + cam.s * (X * cam.ca - Y * cam.sa),
			cam.oy + cam.s * ((X * cam.sa + Y * cam.ca) * cam.se - Z * cam.ce)
		];
		const f1 = (v: number) => (Math.round(v * 10) / 10).toString();
		const dOf = (q: P2[], close = true) => (q.length < 2 ? '' : 'M' + q.map((v) => `${f1(v[0])} ${f1(v[1])}`).join('L') + (close ? 'Z' : ''));
		const plan = (poly: P2[], Z: number, dx = 0) => poly.map((q) => P(q[0] + dx, q[1], Z));

		// ---------------------------------------------------------------------------- drawing helpers
		const pal = () => PAL[theme];
		const on = (pid: string) => hi.includes(pid);
		const hl = (c: string, pid: string) => (on(pid) ? mix(c, pal().accent, 0.55) : c);
		/** extruded plan box: X range clipped, front (+Y) and side (-X) faces visible from this view */
		const drawBox = (b: Box, r: Rect, z0: number, z1: number, xa: number, xb: number, dx: number, cols: [string, string, string], fo: [number, number, number], edge: string, ea: number, pid: string) => {
			const X0 = Math.max(r[0], xa), X1 = Math.min(r[2], xb);
			if (X1 <= X0 + 0.01) {
				for (const e of [b.top, b.front, b.side]) e.style.display = 'none';
				return false;
			}
			const [Y0, , , Y1] = [r[1], 0, 0, r[3]];
			const c = cols.map((x) => hl(x, pid));
			const set = (e: PathEl, d: string, col: string, o: number) => {
				e.style.display = '';
				e.setAttribute('d', d);
				e.setAttribute('fill', col);
				e.setAttribute('fill-opacity', o.toFixed(3));
				e.setAttribute('stroke', on(pid) ? pal().accent : edge);
				e.setAttribute('stroke-opacity', (on(pid) ? 0.9 : ea).toFixed(3));
				e.setAttribute('stroke-width', '1');
			};
			set(b.top, dOf([P(X0 + dx, Y0, z1), P(X1 + dx, Y0, z1), P(X1 + dx, Y1, z1), P(X0 + dx, Y1, z1)]), c[0], fo[0]);
			set(b.front, dOf([P(X0 + dx, Y1, z1), P(X1 + dx, Y1, z1), P(X1 + dx, Y1, z0), P(X0 + dx, Y1, z0)]), c[1], fo[1]);
			set(b.side, dOf([P(X0 + dx, Y0, z1), P(X0 + dx, Y1, z1), P(X0 + dx, Y1, z0), P(X0 + dx, Y0, z0)]), c[2], fo[2]);
			return true;
		};
		const hideBox = (b: Box) => {
			for (const e of [b.top, b.front, b.side]) e.style.display = 'none';
		};
		/** arrow head (filled triangle) at screen point tip, pointing along dir */
		const head = (tip: P2, from: P2, size: number): string => {
			const dx = tip[0] - from[0], dy = tip[1] - from[1];
			const l = Math.hypot(dx, dy) || 1;
			const ux = dx / l, uy = dy / l;
			const b: P2 = [tip[0] - ux * size, tip[1] - uy * size];
			return dOf([tip, [b[0] - uy * size * 0.45, b[1] + ux * size * 0.45], [b[0] + uy * size * 0.45, b[1] - ux * size * 0.45]]);
		};

		// ---------------------------------------------------------------------------- state from p
		interface State {
			slice: number; // 0 in place ... 1 section slice lifted out, the rest ghosted
			subIn: number;
			subDz: number;
			cAx: number;
			flux: number;
			fluxKind: 'sputter' | 'gold' | 'uv' | 'ion' | null;
			fluxT: number;
			film: number;
			resistSheet: number;
			resistPat: number;
			etch: number; // 0 film whole ... 1 only strips
			strips: number; // strip visibility
			sink: number; // diffusion progress
			furnace: number;
			chan: number; // diffused guides
			outline: number;
			dim: number;
			ghost: number;
			e1: number; // electrode pads present (under the gold film until it is etched)
			e2: number;
			goldFilm: number; // gold film coverage
			goldEtch: number; // 0 film whole ... 1 only the pads
			goldResist: number;
			goldResistPat: number;
			eAlpha: number; // electrode opacity (translucent while the light is on)
			prism: number;
			beam: number;
			front: number; // light front X
			light: number;
			obs: number;
			sec: number; // section face content
			field: number;
			fieldArrows: number;
			tint: number;
			cFace: number;
			volt: number;
			tog: number; // 0 V / 6 V toggle position (a step, not a readout)
			v: number; // crossfade 0 V pattern -> 6 V pattern (no intermediate voltages)
		}
		const state = (p: number): State => {
			const q = (cid: string) => cq(cid, p);
			const after = (cid: string) => p >= C[cid][1];
			const sq = q('substrate'), tq = q('titanium'), mq = q('strips'), dq = q('diffusion'), eq = q('electrodes');
			const xq = q('crossover'), fq = q('field'), wq = q('switch');
			const inCh = (cid: string) => p >= C[cid][0] && p < C[cid][1];
			// section slice: lifts out in diffusion / field, returns at the start of the next chapter
			const cut = inCh('diffusion') ? ease(seg(dq, 0, 0.25)) : inCh('electrodes') ? 1 - ease(seg(eq, 0, 0.22)) : inCh('field') ? ease(seg(fq, 0.08, 0.3)) : inCh('switch') ? 1 - ease(seg(wq, 0, 0.22)) : 0;
			const etch = ease(seg(mq, 0.45, 0.66));
			const sink = ease(seg(dq, 0.22, 0.82));
			const lightOn = p >= C.crossover[0] && p < C.field[0] ? 1 : inCh('field') ? 1 - seg(fq, 0, 0.1) : p >= C.switch[0] ? ease(seg(wq, 0.12, 0.28)) : 0;
			const frontX = p >= C.switch[0] ? XEND + 30 : lerp(SPOT - 2, XEND + 30, ease(seg(xq, 0.2, 0.8)));
			let fluxKind: State['fluxKind'] = null;
			let fluxA = 0;
			let fluxT = 0;
			if (inCh('titanium')) {
				fluxKind = 'sputter';
				fluxA = seg(tq, 0.02, 0.15) * (1 - seg(tq, 0.72, 0.85));
				fluxT = tq * 3.2;
			} else if (inCh('strips') && mq < 0.36) {
				fluxKind = 'uv';
				fluxA = seg(mq, 0.12, 0.18) * (1 - seg(mq, 0.3, 0.36));
				fluxT = mq * 9;
			} else if (inCh('strips') && mq >= 0.42) {
				fluxKind = 'ion';
				fluxA = seg(mq, 0.42, 0.47) * (1 - seg(mq, 0.6, 0.66));
				fluxT = mq * 9;
			} else if (inCh('electrodes') && eq < 0.63) {
				fluxKind = 'gold';
				fluxA = seg(eq, 0.4, 0.46) * (1 - seg(eq, 0.58, 0.63));
				fluxT = eq * 3.2;
			} else if (inCh('electrodes') && eq < 0.745) {
				fluxKind = 'uv';
				fluxA = seg(eq, 0.64, 0.67) * (1 - seg(eq, 0.71, 0.745));
				fluxT = eq * 9;
			} else if (inCh('electrodes')) {
				fluxKind = 'ion';
				fluxA = seg(eq, 0.76, 0.79) * (1 - seg(eq, 0.88, 0.92));
				fluxT = eq * 9;
			}
			// switch: the toggle steps to 6 V, then the 0 V pattern crossfades into the 6 V pattern
			const tog = p >= C.switch[0] ? ease(seg(wq, 0.32, 0.37)) : 0;
			const v = p >= C.switch[0] ? ease(seg(wq, 0.38, 0.62)) : 0;
			const goldFilm = p < C.electrodes[0] ? 0 : after('electrodes') ? 1 : ease(seg(eq, 0.42, 0.62));
			return {
				slice: cut,
				subIn: easeOut(seg(sq, 0, 0.45)),
				subDz: (1 - easeOut(seg(sq, 0, 0.6))) * 120,
				cAx: p < C.titanium[0] ? ease(seg(sq, 0.55, 0.85)) : 1 - seg(tq, 0, 0.3),
				flux: fluxA,
				fluxKind,
				fluxT,
				film: p < C.titanium[0] ? 0 : ease(seg(tq, 0.18, 0.8)),
				resistSheet: p < C.strips[0] ? 0 : after('strips') ? 0 : ease(seg(mq, 0, 0.12)) * (1 - seg(mq, 0.32, 0.42)),
				resistPat: p < C.strips[0] || after('strips') ? 0 : seg(mq, 0.3, 0.36) * (1 - seg(mq, 0.66, 0.74)),
				etch: p < C.strips[0] ? 0 : after('strips') ? 1 : etch,
				strips: p < C.strips[0] ? 0 : 1 - sink,
				sink: p < C.diffusion[0] ? 0 : after('diffusion') ? 1 : sink,
				furnace: inCh('diffusion') ? Math.sin(Math.PI * seg(dq, 0.15, 0.9)) ** 1.5 : 0,
				chan: p < C.diffusion[0] ? 0 : after('diffusion') ? 1 : sink,
				outline: p < C.strips[0] ? 0 : inCh('strips') ? ease(seg(mq, 0.72, 0.88)) : 1 - cut,
				dim: inCh('strips') ? ease(seg(mq, 0.72, 0.88)) : inCh('crossover') ? ease(seg(xq, 0.05, 0.2)) * (1 - seg(xq, 0.88, 1)) : 0,
				ghost: inCh('electrodes') ? seg(eq, 0.2, 0.28) * (1 - seg(eq, 0.35, 0.42)) : 0,
				e1: goldFilm,
				e2: goldFilm,
				goldFilm,
				goldEtch: p < C.electrodes[0] ? 0 : after('electrodes') ? 1 : ease(seg(eq, 0.78, 0.9)),
				goldResist: inCh('electrodes') ? ease(seg(eq, 0.6, 0.65)) * (1 - seg(eq, 0.7, 0.74)) : 0,
				goldResistPat: inCh('electrodes') ? seg(eq, 0.7, 0.74) * (1 - seg(eq, 0.9, 0.95)) : 0,
				eAlpha: 1 - 0.86 * lightOn,
				prism: p < C.crossover[0] ? 0 : inCh('field') ? 1 - cut : easeOut(seg(xq, 0, 0.16)),
				beam: p < C.crossover[0] ? 0 : lightOn * seg(xq, 0.1, 0.22),
				front: frontX,
				light: lightOn,
				obs: p < C.crossover[0] ? 0 : inCh('crossover') ? ease(seg(xq, 0.72, 0.88)) : inCh('field') ? 1 - cut : 1,
				sec: inCh('diffusion') ? cut : inCh('electrodes') ? cut : inCh('field') || inCh('switch') ? cut : 0,
				field: inCh('field') ? ease(seg(fq, 0.3, 0.72)) : inCh('switch') ? cut : 0,
				fieldArrows: inCh('field') ? seg(fq, 0.62, 0.74) : inCh('switch') ? cut : 0,
				tint: inCh('field') ? ease(seg(fq, 0.66, 0.84)) : inCh('switch') ? cut : 0,
				cFace: inCh('field') ? ease(seg(fq, 0.22, 0.4)) : inCh('switch') ? cut : 0,
				volt: p < C.switch[0] ? 0 : ease(seg(wq, 0.14, 0.3)),
				tog,
				v
			};
		};
		const camAt = (p: number): Cam => {
			const q = (cid: string) => cq(cid, p);
			if (p < C.titanium[0]) return blendCam(SHOTS.arrive, ISO, ease(seg(q('substrate'), 0, 0.75)));
			if (p < C.diffusion[0]) return camOf(ISO);
			if (p < C.electrodes[0]) return blendCam(ISO, SHOTS.diffusion, ease(seg(q('diffusion'), 0, 0.3)));
			if (p < C.crossover[0]) return blendCam(SHOTS.diffusion, ISO, ease(seg(q('electrodes'), 0, 0.25)));
			if (p < C.field[0]) return blendCam(ISO, SHOTS.light, ease(seg(q('crossover'), 0, 0.2)));
			if (p < C.switch[0]) return blendCam(SHOTS.light, SHOTS.field, ease(seg(q('field'), 0.05, 0.32)));
			if (p < C.power[0]) return blendCam(SHOTS.field, SHOTS.light, ease(seg(q('switch'), 0, 0.25)));
			return blendCam(SHOTS.light, SHOTS.plot, ease(seg(q('power'), 0, 0.3)));
		};

		// ---------------------------------------------------------------------------- draw a piece
		interface Cut {
			xa: number;
			xb: number;
			ya: number;
			yb: number;
			dx: number;
			dz: number;
			alpha: number;
		}
		const WHOLE: Cut = { xa: -1e9, xb: 1e9, ya: -1e9, yb: 1e9, dx: 0, dz: 0, alpha: 1 };
		const drawPiece = (pc: Piece, S: State, o: Cut) => {
			if (!show(pc.g, o.alpha)) return;
			// ghosted pieces (section chapters) are context only: not pickable
			pc.g.style.pointerEvents = o.alpha < 0.6 ? 'none' : '';
			const { xa, xb, dx } = o;
			const c = pal();
			// explode (k): guide layer, electrodes and prism lift apart
			const kz = k;
			const zSub = -S.subDz + o.dz;
			const sub: Rect = [SUB[0], Math.max(SUB[1], o.ya), SUB[2], Math.min(SUB[3], o.yb)];
			if (drawBox(pc.sub, sub, zSub - T, zSub, xa, xb, dx, [c.subTop, c.subFront, c.subSide], c.subA, c.edge, c.edgeA, 'substrate'))
				for (const e of [pc.sub.top, pc.sub.front, pc.sub.side]) show(e, S.subIn);
			// furnace tint on the top face
			if (S.furnace > 0.01) {
				const X0 = Math.max(SUB[0], xa), X1 = Math.min(SUB[2], xb);
				pc.furnace.setAttribute('d', dOf([P(X0 + dx, sub[1], zSub), P(X1 + dx, sub[1], zSub), P(X1 + dx, sub[3], zSub), P(X0 + dx, sub[3], zSub)]));
				pc.furnace.setAttribute('fill', c.furnace);
				show(pc.furnace, 0.15 * S.furnace);
			} else show(pc.furnace, 0);
			// diffused guides (on the surface, slightly wider than the strips); lift with explode
			const zg = zSub + EX.guides * kz;
			const chanPolys: P2[][][] = [launchChan, [chan1], [chan2], outChan];
			const gpid = ['launch_region', 'guide_1', 'guide_2', 'output_region'];
			pc.chans.forEach((e, i) => {
				const polys = chanPolys[i].map((q) => clipX(q, xa, xb)).filter((q) => q.length > 2);
				if (!polys.length || S.chan < 0.01) return show(e, 0);
				e.setAttribute('d', polys.map((q) => dOf(plan(q, zg, dx))).join(''));
				e.setAttribute('fill', hl(c.guide, gpid[i]));
				e.setAttribute('stroke', on(gpid[i]) ? c.accent : 'none');
				show(e, S.chan * c.guideA * (i === 0 || i === 3 ? 0.8 : 1) * (1 - 0.45 * S.light * (1 - S.slice)));
			});
			// Ti strips (pattern) with a thin extrusion that sinks during diffusion
			const hs = HF * (1 - S.sink);
			const stripPolys = [...launchPoly, strip1, strip2, ...outPoly].map((q) => clipX(q, xa, xb)).filter((q) => q.length > 2);
			const so = S.strips * (S.etch > 0 ? 1 : 0);
			if (so > 0.01 && stripPolys.length) {
				pc.stripLo.setAttribute('d', stripPolys.map((q) => dOf(plan(q, zSub, dx))).join(''));
				pc.stripHi.setAttribute('d', stripPolys.map((q) => dOf(plan(q, zSub + hs, dx))).join(''));
				pc.stripLo.setAttribute('fill', hl(c.tiSide, 'ti_strips'));
				pc.stripHi.setAttribute('fill', hl(mix(c.ti, c.guide, 0.6 * S.sink), 'ti_strips'));
				pc.stripHi.setAttribute('stroke', on('ti_strips') ? c.accent : 'none');
				show(pc.stripLo, so);
				show(pc.stripHi, so);
			} else {
				show(pc.stripLo, 0);
				show(pc.stripHi, 0);
			}
			// Ti film sheet: whole surface, etched away to the strips
			const fo = S.film * (1 - S.etch);
			if (fo > 0.01 && drawBox(pc.filmSheet, sub, zSub, zSub + HF, xa, xb, dx, [c.ti, c.tiSide, c.tiSide], [0.92, 1, 1], c.tiSide, 0.6, 'ti_film')) {
				for (const e of [pc.filmSheet.top, pc.filmSheet.front, pc.filmSheet.side]) show(e, fo);
			} else hideBox(pc.filmSheet);
			// resist sheet over the film, then resist left on the pattern only
			if (S.resistSheet > 0.01 && drawBox(pc.resistSheet, sub, zSub + HF, zSub + HF + HR, xa, xb, dx, [c.resist, mix(c.resist, '#000000', 0.25), mix(c.resist, '#000000', 0.35)], [0.55, 0.7, 0.7], c.resist, 0.7, 'resist')) {
				for (const e of [pc.resistSheet.top, pc.resistSheet.front, pc.resistSheet.side]) show(e, S.resistSheet);
			} else hideBox(pc.resistSheet);
			if (S.resistPat > 0.01 && stripPolys.length) {
				pc.resistPat.setAttribute('d', stripPolys.map((q) => dOf(plan(q, zSub + HF + HR, dx))).join(''));
				pc.resistPat.setAttribute('fill', hl(c.resist, 'resist'));
				pc.resistPat.setAttribute('fill-opacity', '0.8');
				show(pc.resistPat, S.resistPat);
			} else show(pc.resistPat, 0);
			// electrodes (Fig. 4 row 4): gold film over the surface, resist, exposure, ion etch back to two pads over the
			// guides; the pads sit under the film from the start. Translucent while the light is on so the guides show.
			const ze = zSub + EX.electrodes * kz;
			const gold: [string, string, string] = [c.goldTop, c.goldFront, c.goldSide];
			const ea = S.eAlpha;
			const eBox = (b: Box, r: Rect, t: number, pid: string) => {
				if (t <= 0.001) return hideBox(b);
				if (drawBox(b, r, ze, ze + HE, xa, xb, dx, gold, [ea, ea, ea], c.goldEdge, ea < 0.9 ? 0.85 : 0.55, pid)) {
					for (const e of [b.top, b.front, b.side]) show(e, t);
				}
			};
			eBox(pc.e1, e1, S.e1, 'electrode_1');
			eBox(pc.e2, e2, S.e2, 'electrode_2');
			const go = S.goldFilm * (1 - S.goldEtch);
			if (go > 0.01 && drawBox(pc.goldSheet, sub, ze, ze + HE, xa, xb, dx, gold, [1, 1, 1], c.goldEdge, 0.55, 'gold_film')) {
				for (const e of [pc.goldSheet.top, pc.goldSheet.front, pc.goldSheet.side]) show(e, go);
			} else hideBox(pc.goldSheet);
			if (S.goldResist > 0.01 && drawBox(pc.goldResist, sub, ze + HE, ze + HE + HR, xa, xb, dx, [c.resist, mix(c.resist, '#000000', 0.25), mix(c.resist, '#000000', 0.35)], [0.55, 0.7, 0.7], c.resist, 0.7, 'resist')) {
				for (const e of [pc.goldResist.top, pc.goldResist.front, pc.goldResist.side]) show(e, S.goldResist);
			} else hideBox(pc.goldResist);
			const pads = [e1, e2].map((r) => clipX([[r[0], r[1]], [r[2], r[1]], [r[2], r[3]], [r[0], r[3]]], xa, xb)).filter((q) => q.length > 2);
			if (S.goldResistPat > 0.01 && pads.length) {
				pc.goldResistPat.setAttribute('d', pads.map((q) => dOf(plan(q, ze + HE + HR, dx))).join(''));
				pc.goldResistPat.setAttribute('fill', hl(c.resist, 'resist'));
				pc.goldResistPat.setAttribute('fill-opacity', '0.8');
				show(pc.goldResistPat, S.goldResistPat);
			} else show(pc.goldResistPat, 0);
		};

		// ---------------------------------------------------------------------------- frame
		let lastS: State | null = null;
		let lastP = 0;
		const frame = (p: number) => {
			const c = pal();
			const S = state(p);
			lastS = S;
			lastP = p;
			cam = camAt(p);
			const s = cam.s;
			blurStd.setAttribute('stdDeviation', Math.max(1.2, 2.2 * s).toFixed(2));
			blurStd2.setAttribute('stdDeviation', Math.max(0.6, 1.2 * s).toFixed(2));
			for (const f of [blur, blur2]) {
				f.setAttribute('x', String(-w));
				f.setAttribute('y', String(-h));
				f.setAttribute('width', String(3 * w));
				f.setAttribute('height', String(3 * h));
			}
			// pieces: whole device, or (section chapters) a slice from the middle of the coupler lifted out, the rest ghosted
			const sl = S.slice;
			const dzS = LIFT * sl;
			if (sl > 0.001) {
				const yc = ease(seg(sl, 0, 0.6));
				const ghostA = 1 - 0.93 * sl;
				drawPiece(main, S, { ...WHOLE, xa: XC + SLW, dx: 70 * sl, alpha: ghostA });
				drawPiece(slice, S, { xa: XC, xb: XC + SLW, ya: lerp(SUB[1], yg - SLY, yc), yb: lerp(SUB[3], yg + SLY, yc), dx: 0, dz: dzS, alpha: 1 });
				drawPiece(left, S, { ...WHOLE, xb: XC, dx: -110 * sl, alpha: ghostA });
			} else {
				drawPiece(main, S, WHOLE);
				show(slice.g, 0);
				show(left.g, 0);
			}

			// section face at the cut (main piece's -X face)
			if (S.sec > 0.01) {
				show(secG, S.sec);
				// graded guides: gradient centred at the surface, ellipse = lateral half width x depth
				const gsec = (el: PathEl, rg: typeof rad1, yc: number, pid: string, tint: number) => {
					const dep = GD * (0.15 + 0.85 * S.sink);
					const z0 = dzS;
					const wl = (GW / 2) * (0.6 + 0.4 * S.sink);
					const q: P2[] = [];
					for (let i = 0; i <= 32; i++) {
						const th = (Math.PI * i) / 32;
						q.push(P(XC, yc + wl * Math.cos(th), z0 - dep * Math.sin(th)));
					}
					el.setAttribute('d', dOf(q));
					const o = P(XC, yc, z0);
					const ux = P(XC, yc + wl, z0), uz = P(XC, yc, z0 - dep);
					rg.g.setAttribute('gradientTransform', `matrix(${f1(ux[0] - o[0])} ${f1(ux[1] - o[1])} ${f1(uz[0] - o[0])} ${f1(uz[1] - o[1])} ${f1(o[0])} ${f1(o[1])})`);
					const base = tint > 0 ? mix(c.guide, c.guideHi, tint) : mix(c.guide, c.guideLo, -tint);
					const col = on('index_tint') ? mix(base, c.accent, 0.35) : hl(base, pid);
					rg.s.forEach((st, i) => {
						st.setAttribute('stop-color', col);
						st.setAttribute('stop-opacity', String([0.95, 0.6, 0.0][i] * S.chan));
					});
					el.setAttribute('stroke', on(pid) ? c.accent : 'none');
					show(el, S.chan > 0.01 ? 1 : 0);
				};
				gsec(sec1, rad1, y1, 'guide_1', 0.8 * S.tint);
				gsec(sec2, rad2, y2, 'guide_2', -0.8 * S.tint);
				// once tinted, the section guides explain the tint (opposite index changes) instead of the guide part
				for (const [e, pid] of [[sec1, 'guide_1'], [sec2, 'guide_2']] as const) e.setAttribute('data-pick', S.tint > 0.3 ? 'index_tint' : pid);
				// strip ends on the face while they still stand
				[y1, y2].forEach((yc, i) => {
					const hs = HF * (1 - S.sink);
					const e = secStrip[i];
					if (S.strips < 0.01 || hs < 0.05) return show(e, 0);
					e.setAttribute('d', dOf([P(XC, yc - gw / 2, dzS), P(XC, yc + gw / 2, dzS), P(XC, yc + gw / 2, dzS + hs), P(XC, yc - gw / 2, dzS + hs)]));
					e.setAttribute('fill', hl(c.tiSide, 'ti_strips'));
					show(e, S.strips);
				});
				// field lines (Fig. 3a): from under the electrode over the curved guide, down through it, under the gap, up
				// through the other guide; arrows down on one side, up on the other. Polarity not stated (hover).
				const half = [y1 - (gapIn1 - y1) * 0.25, y1, y1 - gw * 0.5].map((yy) => yg - yy);
				FL.forEach((L, i) => {
					const a = half[i];
					const b = a * 1.1 + 5;
					if (S.field < 0.01) {
						show(L.line, 0); show(L.hitW, 0); show(L.a, 0); show(L.b, 0);
						return;
					}
					const q: P2[] = [];
					for (let j = 0; j <= 40; j++) {
						const th = Math.PI - (Math.PI * j) / 40;
						q.push(P(XC - 0.5, yg + a * Math.cos(th), dzS - b * Math.sin(th)));
					}
					const d = dOf(q, false);
					const col = hl(c.field, 'field_lines');
					L.line.setAttribute('d', d);
					L.hitW.setAttribute('d', d);
					L.line.setAttribute('stroke', col);
					L.line.setAttribute('stroke-width', (on('field_lines') ? 2.2 : 1.6).toFixed(1));
					L.line.setAttribute('stroke-dasharray', '1 1');
					L.line.setAttribute('stroke-dashoffset', (1 - S.field).toFixed(4));
					show(L.line, 1);
					show(L.hitW, 1);
					const hs = Math.max(5, Math.min(11, 2.4 * s));
					const at = (th: number): P2 => P(XC - 0.5, yg + a * Math.cos(th), dzS - b * Math.sin(th));
					L.a.setAttribute('d', head(at(0.72 * Math.PI), at(0.76 * Math.PI), hs));
					L.b.setAttribute('d', head(at(0.24 * Math.PI), at(0.28 * Math.PI), hs));
					L.a.setAttribute('fill', col);
					L.b.setAttribute('fill', col);
					show(L.a, S.fieldArrows);
					show(L.b, S.fieldArrows);
				});
			} else show(secG, 0);

			// coupling region outline (Fig. 5 dashed box) and the c dimension line
			const zs = -S.subDz;
			if (S.outline > 0.01) {
				const d = dOf(plan([[cr[0], cr[1]], [cr[2], cr[1]], [cr[2], cr[3]], [cr[0], cr[3]]], zs));
				outline.setAttribute('d', d);
				outlineHit.setAttribute('d', d);
				outline.setAttribute('stroke', on('coupling_region') ? c.accent : c.inkSoft);
				outline.setAttribute('stroke-width', '1');
				show(outline, S.outline * (S.light > 0.5 ? 0.6 : 0.9));
				show(outlineHit, S.outline);
			} else {
				show(outline, 0);
				show(outlineHit, 0);
			}
			if (S.dim > 0.01) {
				const a0 = P(cr[0], dimY, zs), a1 = P(cr[2], dimY, zs);
				const t0a = P(cr[0], dimY - 10, zs), t0b = P(cr[0], dimY + 10, zs), t1a = P(cr[2], dimY - 10, zs), t1b = P(cr[2], dimY + 10, zs);
				const hs = Math.max(4, Math.min(8, 7 * s));
				dimLine.setAttribute('d', `${dOf([a0, a1], false)}${dOf([t0a, t0b], false)}${dOf([t1a, t1b], false)}${head(a1, a0, hs)}${head(a0, a1, hs)}`);
				dimLine.setAttribute('stroke', on('coupling_region') ? c.accent : c.ink);
				dimLine.setAttribute('fill', on('coupling_region') ? c.accent : c.ink);
				dimLine.setAttribute('stroke-width', '1');
				show(dimLine, S.dim);
			} else show(dimLine, 0);
			// observation circle (Fig. 5)
			if (S.obs > 0.01) {
				const q: P2[] = [];
				for (let i = 0; i < 64; i++) q.push(P(obsC[0] + obsR * Math.cos((i / 64) * 2 * Math.PI), obsC[1] + obsR * Math.sin((i / 64) * 2 * Math.PI), zs));
				const d = dOf(q);
				obs.setAttribute('d', d);
				obsHit.setAttribute('d', d);
				obs.setAttribute('stroke', on('observation_region') ? c.accent : mix(c.inkSoft, c.light, 0.35 * S.light));
				obs.setAttribute('stroke-width', '1');
				show(obs, S.obs);
				show(obsHit, S.obs);
			} else {
				show(obs, 0);
				show(obsHit, 0);
			}

			// guided light (Eq. 2): gradient along X, iso-lines parallel to the projected Y axis
			const zl = zs + EX.guides * k + 0.5;
			if (S.light > 0.01 && S.slice < 0.99) {
				show(glowG, S.light * (1 - S.slice));
				// 0 V (delta beta = 0, faint residue) and 6 V (drawn for delta beta = c sqrt(12): (dbeta / 2c)^2 = 3) patterns,
				// crossfaded; no intermediate voltage is drawn (for 3 L0, Eq. (2) passes other bar states on the way)
				const fade = S.v;
				const o = P(0, 0, zl);
				const ex = P(1, 0, zl), ey = P(0, 1, zl);
				const exv: P2 = [ex[0] - o[0], ex[1] - o[1]];
				const eyv: P2 = [ey[0] - o[0], ey[1] - o[1]];
				const ln = Math.hypot(eyv[0], eyv[1]) || 1;
				let n: P2 = [-eyv[1] / ln, eyv[0] / ln];
				if (n[0] * exv[0] + n[1] * exv[1] < 0) n = [-n[0], -n[1]];
				const exn = n[0] * exv[0] + n[1] * exv[1];
				const A = P(XS[0], 0, zl);
				const span = (XS[NSTOP - 1] - XS[0]) * exn;
				for (const lin of [lin1, lin2]) {
					lin.g.setAttribute('x1', f1(A[0]));
					lin.g.setAttribute('y1', f1(A[1]));
					lin.g.setAttribute('x2', f1(A[0] + n[0] * span));
					lin.g.setAttribute('y2', f1(A[1] + n[1] * span));
				}
				const soft = 14;
				const lc = on('argon_beam') || on('guided_light') ? mix(c.light, c.accent, 0.35) : c.light;
				for (let i = 0; i < NSTOP; i++) {
					const X = XS[i];
					const m = clamp01((S.front - X) / soft) * (X >= SPOT - 6 ? 1 : 0) * clamp01((X - (SPOT - 6)) / 8);
					const [p01, p02] = power(X, 0, 0.07);
					const [p61, p62] = power(X, 3, 0);
					const a1 = lerp(p01, p61, fade);
					const a2 = lerp(p02, p62, fade);
					lin1.stops[i].setAttribute('stop-opacity', (m * a1).toFixed(3));
					lin2.stops[i].setAttribute('stop-opacity', (m * a2).toFixed(3));
					lin1.stops[i].setAttribute('stop-color', lc);
					lin2.stops[i].setAttribute('stop-color', lc);
				}
				const g1d = dOf(plan(cl1, zl), false);
				const g2d = dOf(plan(cl2.filter((q) => q[0] >= X0c - 30), zl), false);
				const lw = Math.max(1.2, gw * 0.3 * s);
				for (const [L, wmul, op] of [[LS, 2.2, c.glowA], [LC, 1, 1]] as const) {
					L.g1.setAttribute('d', g1d);
					L.g2.setAttribute('d', g2d);
					L.g1.setAttribute('stroke-width', f1(lw * wmul));
					L.g2.setAttribute('stroke-width', f1(lw * wmul));
					L.launch.setAttribute('d', launchPoly.map((q) => dOf(plan(q, zl))).join(''));
					L.out.setAttribute('d', outPoly.map((q) => dOf(plan(q, zl))).join(''));
					show(L.launch, op * 0.32);
					show(L.out, op * 0.32);
					show(L.g1, op);
					show(L.g2, op);
				}
				for (const [i, d] of [[0, g1d], [1, g2d]] as const) {
					lightHit[i].setAttribute('d', d);
					lightHit[i].setAttribute('stroke-width', f1(Math.max(8, lw * 2)));
					show(lightHit[i], S.light > 0.5 ? 1 : 0);
				}
			} else {
				show(glowG, 0);
				show(lightHit[0], 0);
				show(lightHit[1], 0);
			}

			// ghost of the classical central electrode (Fig. 2a), between the guides
			if (S.ghost > 0.01) {
				const gr: Rect = [e1[0], yg - gw * 0.4, e1[2], yg + gw * 0.4];
				drawBox(ghost, gr, zs, zs + HE, -1e9, 1e9, 0, [c.goldTop, c.goldFront, c.goldSide], [0.25, 0.25, 0.25], c.goldEdge, 0.9, 'central_electrode');
				for (const e of [ghost.top, ghost.front, ghost.side]) {
					e.setAttribute('stroke-dasharray', '4 3');
					show(e, S.ghost);
				}
			} else hideBox(ghost);

			// voltage stand-in (behind the slab) and its leads; a plain two-position 0 V / 6 V toggle (no readout)
			if (S.volt > 0.01) {
				show(vg, S.volt);
				const r: Rect = [VB.x0, VB.y0, VB.x1, VB.y1];
				drawBox(vBox, r, -T + zs, VB.z1 + zs, -1e9, 1e9, 0, [c.box, mix(c.box, '#000000', 0.2), mix(c.box, '#000000', 0.3)], [1, 1, 1], c.boxEdge, 0.9, 'voltage');
				const mx0 = VB.x0 + 12, mx1 = VB.x1 - 12, my = (VB.y0 + VB.y1) / 2;
				const zt = VB.z1 + zs;
				vMeter.setAttribute('d', dOf([P(mx0, my - 6, zt), P(mx1, my - 6, zt), P(mx1, my + 6, zt), P(mx0, my + 6, zt)]));
				vMeter.setAttribute('fill', 'none');
				vMeter.setAttribute('stroke', c.boxEdge);
				vMeter.setAttribute('stroke-width', '1');
				show(vMeter, 1);
				const kw = (mx1 - mx0) * 0.42;
				const kx = lerp(mx0 + 1.5, mx1 - 1.5 - kw, S.tog);
				vKnob.setAttribute('d', dOf([P(kx, my - 4.5, zt), P(kx + kw, my - 4.5, zt), P(kx + kw, my + 4.5, zt), P(kx, my + 4.5, zt)]));
				vKnob.setAttribute('fill', on('voltage') ? c.accent : mix(c.boxEdge, c.field, S.tog));
				show(vKnob, 1);
				const ze = zs + EX.electrodes * k + HE;
				const lead = (e: PathEl, from: [number, number, number], to: [number, number, number], arc: number) => {
					const q: P2[] = [];
					for (let i = 0; i <= 24; i++) {
						const t = i / 24;
						q.push(P(lerp(from[0], to[0], t), lerp(from[1], to[1], t), lerp(from[2], to[2], t) + arc * 4 * t * (1 - t)));
					}
					e.setAttribute('d', dOf(q, false));
					e.setAttribute('stroke', on('voltage') ? c.accent : mix(c.boxEdge, c.field, 0.8 * S.tog));
					e.setAttribute('stroke-width', (1 + 0.6 * S.tog).toFixed(2));
					show(e, S.volt);
				};
				lead(leads[0], [VB.x0 + 20, VB.y1, VB.z1 + zs], [VB.x0 + 20, e1[1] + 10, ze], 18);
				lead(leads[1], [VB.x1 - 20, VB.y1, VB.z1 + zs], [VB.x1 - 20, e2[1] + 30, ze], 60);
			} else {
				show(vg, 0);
				show(leads[0], 0);
				show(leads[1], 0);
			}

			// C axis: up, normal to the surface (substrate chapter, on the slab corner; field chapter, in the electrode gap)
			const axis = (L: { line: PathEl; head: PathEl; hit?: PathEl }, base: [number, number, number], len: number, o: number) => {
				if (o < 0.01) {
					show(L.line, 0); show(L.head, 0); if (L.hit) show(L.hit, 0);
					return;
				}
				const a = P(...base);
				const b = P(base[0], base[1], base[2] + len * o);
				const col = on('c_axis') ? c.accent : c.ink;
				L.line.setAttribute('d', dOf([a, b], false));
				L.line.setAttribute('stroke', col);
				L.line.setAttribute('stroke-width', '1.4');
				L.head.setAttribute('d', head(b, a, Math.max(6, Math.min(10, 9 * s))));
				L.head.setAttribute('fill', col);
				show(L.line, Math.min(1, o * 2));
				show(L.head, Math.min(1, o * 2));
				if (L.hit) {
					L.hit.setAttribute('d', dOf([a, b], false));
					show(L.hit, 1);
				}
			};
			axis(cAxis, [SUB[0] + 46, SUB[3] - 40, zs], 80, S.cAx * S.subIn);
			axis(cFace, [XC - 0.5, yg, zs + dzS + 1], 26, S.cFace * S.sec);

			// prism stand-in over the launching region (plain, no dimensions)
			const zp = zs + EX.prism * k;
			if (S.prism > 0.01) {
				const dz = (1 - S.prism) * 80;
				const xm = (PR.x0 + PR.x1) / 2;
				const ridge0 = P(xm, PR.y0, zp + dz + PR.hgt), ridge1 = P(xm, PR.y1, zp + dz + PR.hgt);
				const bl0 = P(PR.x0, PR.y0, zp + dz), bl1 = P(PR.x0, PR.y1, zp + dz), br0 = P(PR.x1, PR.y0, zp + dz), br1 = P(PR.x1, PR.y1, zp + dz);
				const pc = hl(c.prism, 'prism');
				const face = (e: PathEl, q: P2[], o: number) => {
					e.setAttribute('d', dOf(q));
					e.setAttribute('fill', pc);
					e.setAttribute('fill-opacity', o.toFixed(2));
					e.setAttribute('stroke', on('prism') ? c.accent : c.prismEdge);
					e.setAttribute('stroke-opacity', '0.8');
					e.setAttribute('stroke-width', '1');
					show(e, S.prism);
				};
				face(prism.right, [ridge0, ridge1, br1, br0], theme === 'light' ? 0.32 : 0.14);
				face(prism.left, [ridge0, ridge1, bl1, bl0], theme === 'light' ? 0.22 : 0.2);
				face(prism.front, [bl1, br1, ridge1], theme === 'light' ? 0.4 : 0.26);
			} else for (const e of [prism.left, prism.right, prism.front]) show(e, 0);

			// argon beam: from upper left into the prism, down to the coupling spot
			if (S.beam > 0.01) {
				const yb = (PR.y0 + PR.y1) / 2 + 6;
				const start: [number, number, number] = [SUB[0] - 260, yb, zp + 150];
				const entry: [number, number, number] = [PR.x0 + 0.42 * ((PR.x1 - PR.x0) / 2), yb, zp + 0.42 * PR.hgt];
				const spot: [number, number, number] = [SPOT, yb, zp + 0.5];
				const t = S.beam;
				const along = (a: [number, number, number], b: [number, number, number], u: number): [number, number, number] => [lerp(a[0], b[0], u), lerp(a[1], b[1], u), lerp(a[2], b[2], u)];
				const q1 = t < 0.75 ? along(start, entry, t / 0.75) : entry;
				const pts3 = [start, q1, ...(t > 0.75 ? [along(entry, spot, (t - 0.75) / 0.25)] : [])];
				const d = dOf(pts3.map((v) => P(...v)), false);
				const bc = on('argon_beam') ? mix(c.light, c.accent, 0.4) : c.light;
				beamCore.setAttribute('d', d);
				beamSoft.setAttribute('d', d);
				beamHit.setAttribute('d', d);
				beamCore.setAttribute('stroke', theme === 'light' ? c.lightCore : c.lightCore);
				beamCore.setAttribute('stroke-width', f1(Math.max(1.2, 2.2 * s)));
				beamSoft.setAttribute('stroke', bc);
				beamSoft.setAttribute('stroke-width', f1(Math.max(3, 7 * s)));
				show(beamCore, S.light);
				show(beamSoft, S.light * c.glowA);
				show(beamHit, S.light);
			} else {
				show(beamCore, 0);
				show(beamSoft, 0);
				show(beamHit, 0);
			}

			// process flux arrows: sputtered Ti, exposure light, ions (Fig. 4 rows 1-2), falling with p (pure)
			if (S.flux > 0.01 && S.fluxKind) {
				const col = S.fluxKind === 'sputter' ? c.ti : S.fluxKind === 'gold' ? c.goldTop : S.fluxKind === 'uv' ? c.uv : c.ion;
				const len = S.fluxKind === 'uv' ? 34 : 22;
				fluxPos.forEach((f, i) => {
					const u = (S.fluxT + f.ph) % 1;
					const z = lerp(150, 14, u);
					const fade = Math.sin(Math.PI * u);
					const a = P(f.x, f.y, zs + z + len), b = P(f.x, f.y, zs + z);
					flux[i].l.setAttribute('d', dOf([a, b], false));
					flux[i].l.setAttribute('stroke', col);
					flux[i].l.setAttribute('stroke-width', S.fluxKind === 'uv' ? '1' : '1.3');
					flux[i].hd.setAttribute('d', head(b, a, 6));
					flux[i].hd.setAttribute('fill', col);
					show(flux[i].l, S.flux * fade * 0.9);
					show(flux[i].hd, S.flux * fade * 0.9);
				});
			} else for (const f of flux) {
				show(f.l, 0);
				show(f.hd, 0);
			}
		};

		// ---------------------------------------------------------------------------- picking
		const INFO: Record<string, PickInfo> = {
			c_axis: {
				id: 'c_axis',
				label: 'C axis',
				detail: ['Crystal C axis normal to the guide surface (Cobra configuration).', 'Papuchon et al., Appl. Phys. Lett. 1975, p.289 col. 2; Fig. 3a']
			},
			gold_film: {
				id: 'gold_film',
				label: 'Gold film',
				detail: [
					'2000 Å gold, rf sputtered onto the structure, then masked (optical superposition) and ion-etched to two 1 × 3 mm electrodes 3 µm apart.',
					'Papuchon et al., Appl. Phys. Lett. 1975, p.290 col. 2; Fig. 4 row 4'
				]
			},
			index_tint: {
				id: 'index_tint',
				label: 'Opposite index changes',
				detail: [
					'The opposite fields give index changes of opposite sign in the two guides (Papuchon et al., Appl. Phys. Lett. 1975, p.289 col. 2; Fig. 3).',
					'The paper gives no sign. Lighter = index raised, darker = lowered, for the polarity drawn.',
					'Tint direction from r_{33} > 0 (textbook sign, not from the paper); for TM light the change comes mainly from r_{zzz} (p.289 col. 2).'
				]
			}
		};
		const lightInfo = (): PickInfo => {
			const v = lastP >= C.switch[0] ? (lastS?.v ?? 0) : 0;
			const st = v > 0.98 ? '6 V: drawn for Δβ = c√12, the Fig. 1 case' : v > 0.02 ? 'Crossfade from the 0 V to the 6 V state' : '0 V: Δβ = 0, full transfer every L_{0} ≈ 1 mm';
			return {
				id: 'guided_light',
				label: 'Guided light, coupled-mode theory',
				detail: [
					st,
					'0 V and 6 V states shown; intermediate voltages are not shown.',
					'Power along the coupler from Eq. (2), coupling region = 3 L_{0} (Papuchon et al., Appl. Phys. Lett. 1975, p.289; p.291 col. 1).',
					'The Δβ reached at 6 V is not stated; Eq. (2) also returns all light at 3 L_{0} for a smaller Δβ ≈ 1.76 c (derived). Only the output end was observed.',
					'0 V output: "most of the guided light" in the straight guide; the faint glow left in the curved guide is not a measured fraction.'
				]
			};
		};

		return {
			frame,
			highlight(ids) {
				hi = [...ids];
			},
			pick(x, y) {
				const r = svg.getBoundingClientRect();
				const els = document.elementsFromPoint(r.left + x, r.top + y);
				for (const e of els) {
					if (!root.contains(e)) continue;
					const pid = (e as Element).getAttribute('data-pick');
					if (!pid) continue;
					if (pid === 'guided_light') return lightInfo();
					return INFO[pid] ?? pid;
				}
				return null;
			},
			anchor(pid) {
				const S = lastS;
				if (!S) return null;
				const zs = -S.subDz;
				// phone: both labels stacked under the slab's front edge (no room beside the pattern)
				const under = (row: number): [number, number] => {
					const b = P(SUB[0] + 0.12 * (SUB[2] - SUB[0]), SUB[3], zs - T);
					return [b[0], b[1] + 24 + 30 * row];
				};
				if (pid === 'ti_strips') {
					if (S.etch < 0.95 || S.resistPat > 0.05 || S.strips < 0.5) return null;
					return w < 700 ? under(0) : P(X0c + 16, cr[1] + 10, zs);
				}
				if (pid === 'coupling_region') {
					if (S.dim < 0.5) return null;
					return w < 700 ? under(1) : P(cr[2] + 12, dimY, zs);
				}
				return null;
			},
			resize(nw, nh) {
				w = Math.max(1, nw);
				h = Math.max(1, nh);
			},
			explode(nk) {
				k = clamp01(nk);
			},
			theme(t) {
				theme = t;
			},
			dispose() {
				root.remove();
			}
		};
	}
};
export default mod;
