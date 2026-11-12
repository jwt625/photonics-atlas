// Scene module: blazed grating couplers for polymer waveguides (Waldhäusl et al., Appl. Opt. 1997). DevLog-017.
// Spec: data/history/showcases/waldhausl1997.yaml. Contract: ../showcase/types.ts. Renderer 2.5D (SVG).
//
// Five views, each after one of the paper's figures, cross-fading by chapter:
//   A  chip side view after Fig. 1 / 2 (schematic, drawn units "du", Y up; thicknesses enlarged, the 20 mm waveguide
//      compressed behind a break mark; a shallow oblique top face gives the slab depth),
//   B  true-scale close-up of the input grating in nm (Table 1 / p.9385: period 800, depth 250, steep side about 200,
//      grating region about 80 nm under the surface; straight facets, orientation as Fig. 1),
//   C  the single-order coupler after Fig. 3 (Fig. 3 pixels, Y up),
//   D  the 2 mm variable-depth grating (z in µm along, depth in nm across; vertical true to the plotted depths,
//      teeth drawn far wider than the 800 nm period),
//   E  isometric plan of the focusing chip after Fig. 9 (mm; lengths along the light in true ratio 4 : 2 : 4,
//      widths enlarged; grating lines are Eq. (11) ellipses with the derived n_eff and coupling angle).
// Coordinator ruling: beam and order angles stay as Fig. 1-3 draw them; derived angles only in hover.
// Animated quantities follow the plot pen (penAt): graded depth per subarea = Fig. 5 measured square at the pen,
// near-field brightness = Fig. 7 trace up to the pen. frame(p) is pure in (p, shown plot); no timers, no randomness.
import { clamp01, ease, easeOut, lerp, seg } from '../showcase/progress';
import { penAt } from '../showcase/plot';
import type { PickInfo, ShowcaseContext, ShowcaseHandle, ShowcaseModule, Theme } from '../showcase/types';

type P2 = [number, number];
type PathEl = SVGPathElement;

const NS = 'http://www.w3.org/2000/svg';
const DEG = Math.PI / 180;
let uid = 0;

// ------------------------------------------------------------------------------------------------ colours
interface Pal {
	sub: string; subA: number; subEdge: string;
	film: string; filmA: number; filmTopA: number; filmEdge: string;
	metal: string; ebeam: string; dose: string;
	nickel: string; copper: string; hatch: string;
	pmma: string; pmmaA: number; pams: string; pamsA: number;
	prism: string; prismA: number; liquid: string; heat: string;
	beam: string; core: string; glowA: number;
	ink: string; inkSoft: string; accent: string; trench: string;
}
const PAL: Record<Theme, Pal> = {
	dark: {
		sub: '#cfd8dc', subA: 0.13, subEdge: '#9fb0b6',
		film: '#9fd3e6', filmA: 0.36, filmTopA: 0.5, filmEdge: '#9fd3e6',
		metal: '#d4b25a', ebeam: '#8ab4ff', dose: '#8ab4ff',
		nickel: '#a7a9ac', copper: '#c07a4a', hatch: '#e4e6e8',
		pmma: '#d8e6ea', pmmaA: 0.2, pams: '#b9e0c9', pamsA: 0.42,
		prism: '#bfe3f2', prismA: 0.12, liquid: '#7fb6c8', heat: '#ff7a2a',
		beam: '#ff3b30', core: '#ffb3ad', glowA: 0.85,
		ink: '#c3c2b7', inkSoft: '#898781', accent: '#3987e5', trench: '#0e1418'
	},
	light: {
		sub: '#7f98a3', subA: 0.18, subEdge: '#4f6670',
		film: '#2f87a6', filmA: 0.34, filmTopA: 0.45, filmEdge: '#1d5f78',
		metal: '#b08a2a', ebeam: '#2a5fd6', dose: '#2a5fd6',
		nickel: '#7d8084', copper: '#a35a2a', hatch: '#3f4245',
		pmma: '#8fa7ad', pmmaA: 0.25, pams: '#3f9a6a', pamsA: 0.38,
		prism: '#5fa8c8', prismA: 0.16, liquid: '#2f6f8c', heat: '#e0641c',
		beam: '#d42a1f', core: '#ff6a5f', glowA: 0.45,
		ink: '#52514e', inkSoft: '#6f6d68', accent: '#2a78d6', trench: '#5d6a70'
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

// ------------------------------------------------------------------------------------------------ geometry helpers
/** polyline clipped to xa <= X <= xb (X-monotone, may have vertical steps) */
function clipLineX(line: P2[], xa: number, xb: number): P2[] {
	const out: P2[] = [];
	for (let i = 0; i < line.length - 1; i++) {
		const a = line[i], b = line[i + 1];
		if (a[0] === b[0]) {
			if (a[0] >= xa && a[0] <= xb) {
				if (!out.length) out.push(a);
				out.push(b);
			}
			continue;
		}
		const lo = Math.max(xa, Math.min(a[0], b[0]));
		const hi = Math.min(xb, Math.max(a[0], b[0]));
		if (hi < lo) continue;
		const at = (x: number): P2 => [x, a[1] + ((b[1] - a[1]) * (x - a[0])) / (b[0] - a[0])];
		if (!out.length) out.push(at(lo));
		out.push(at(hi));
	}
	return out;
}
/** polyline with every Y clamped to at most `level` (crossing points inserted) */
function clampBelow(line: P2[], level: number): P2[] {
	const out: P2[] = [];
	for (let i = 0; i < line.length; i++) {
		const a = line[i];
		if (i > 0) {
			const b = line[i - 1];
			if ((a[1] - level) * (b[1] - level) < 0) {
				const t = (level - b[1]) / (a[1] - b[1]);
				out.push([b[0] + (a[0] - b[0]) * t, level]);
			}
		}
		out.push([a[0], Math.min(level, a[1])]);
	}
	return out;
}
/** linear interpolation in a sorted point list */
function interp(pts: readonly [number, number][], x: number): number {
	if (!pts.length) return 0;
	if (x <= pts[0][0]) return pts[0][1];
	for (let i = 1; i < pts.length; i++) {
		if (x <= pts[i][0]) {
			const a = pts[i - 1], b = pts[i];
			return a[1] + ((b[1] - a[1]) * (x - a[0])) / (b[0] - a[0] || 1);
		}
	}
	return pts[pts.length - 1][1];
}

// ------------------------------------------------------------------------------------------------ 2D cameras
interface Cam {
	s: number;
	cx: number;
	cy: number;
	rx: number;
	ry: number;
}
interface Box {
	x0: number;
	x1: number;
	y0: number;
	y1: number;
}
type Rgn = [number, number, number, number];
const blend = (a: Cam, b: Cam, t: number): Cam =>
	t <= 0
		? a
		: t >= 1
			? b
			: {
					s: Math.exp(lerp(Math.log(a.s), Math.log(b.s), t)),
					cx: lerp(a.cx, b.cx, t),
					cy: lerp(a.cy, b.cy, t),
					rx: lerp(a.rx, b.rx, t),
					ry: lerp(a.ry, b.ry, t)
				};

// ------------------------------------------------------------------------------------------------ side view (A), du
const A = {
	L: 1000, // chip length, drawn
	T: 60, // film thickness, drawn (enlarged)
	SD: 200, // substrate depth shown, drawn
	PER: 36, // drawn period
	NT: 5, // teeth per grating (Fig. 1 draws five)
	G0: 110, // input grating start
	R: 6, // zero offset, drawn (80 / 800 of the film)
	D: 19, // depth, drawn (250 / 800 of the film)
	ST: 0.25, // steep side share of a period (200 / 800 nm)
	OX: 38, // oblique depth offset
	OY: 22,
	BRK: 500, // break mark
	TP: 34, // PaMS film, drawn (450 / 800 of the PMMA copolymer film)
	NI: 26, // nickel, drawn
	CU: 52 // copper, drawn (not to scale)
};
const XI = A.G0 + (A.NT * A.PER) / 2; // input grating centre
const XO = A.L - XI; // output grating centre
/** film top profile of the side view, developed fraction g (input grating as Fig. 1, output mirrored) */
function sideProfile(g: number, T: number): P2[] {
	const grat: P2[] = [[A.G0, T], [A.G0, T - g * A.R]];
	for (let i = 0; i < A.NT; i++) {
		const a = A.G0 + i * A.PER;
		grat.push([a + A.ST * A.PER, T - g * (A.R + A.D)], [a + A.PER, T - g * A.R]);
	}
	grat.push([A.G0 + A.NT * A.PER, T]);
	const out = grat.map(([x, y]) => [A.L - x, y] as P2).reverse();
	return [[0, T], ...grat, ...out, [A.L, T]];
}

// ------------------------------------------------------------------------------------------------ close-up (B), nm
const B = { X0: -600, X1: 3200, TF: 800, Q: 360, PER: 800, ST: 200, DEP: 250, OFF: 80, NP: 4, NS: 5 };
const DOSE = [1, 0.84, 0.68, 0.52, 0.36]; // schematic dose per step, step 0 at the high-dose (left) edge
/** film top in the close-up at development progress u (0 flat ... 1 final profile) */
function closeProfile(u: number): P2[] {
	const top = B.TF;
	const pk = top - u * B.OFF;
	const vl = top - u * (B.OFF + B.DEP);
	const pts: P2[] = [[B.X0, top], [0, top], [0, pk]];
	for (let j = 0; j < B.NP; j++) {
		const x0 = j * B.PER;
		pts.push([x0 + B.ST, vl], [x0 + B.PER, pk]);
	}
	return pts;
}

// ------------------------------------------------------------------------------------------------ Fig. 3 view (C), px
const C3 = {
	X0: 10, X1: 880, FT: -45, FB: -125, SB: -338, PT: -352, PB: -490, PL: 350, PF: 495, PR: 840,
	G0: 548, GP: 44, GW: 22, GN: 6, GD: 20, HIT: 680, ANG: 52, NP: 1.457
};

// ------------------------------------------------------------------------------------------------ graded view (D)
const D = { KX: 0.32, KY: 0.45, TF: 800, SUB: 70, XL: -110, XR: 700, TPS: 2, OX: 22, OY: 13, EH: 150 };

// ------------------------------------------------------------------------------------------------ iso view (E), mm
const E = {
	X0: -7.2, X1: 7.2, Y0: -3, Y1: 3, ZS: -1.3, ZF: 0.28, SW: 0.1, TW: 0.26, F: 4, HW: 1.4, NL: 9, DL: 0.09,
	AZ: -30, EL: 32, NEFF: 1.475, COS: 0.68375
};

const mod: ShowcaseModule = {
	renderer: '2.5d',
	build(ctx: ShowcaseContext): ShowcaseHandle {
		if (ctx.kind !== '2.5d') throw new Error('waldhausl1997 is a 2.5D scene');
		const { svg, spec } = ctx;
		const id = `wgc${++uid}`;
		let w = Math.max(1, ctx.width);
		let h = Math.max(1, ctx.height);
		let theme: Theme = ctx.theme;
		let hi: string[] = [];
		let shown: string | null = null;
		let lastP = 0;

		// ---------------------------------------------------------------------------- chapters
		const fallback: Record<string, [number, number]> = {
			substrate: [0, 0.06], resist: [0.06, 0.13], write: [0.13, 0.22], develop: [0.22, 0.31], couple: [0.31, 0.42],
			replica: [0.42, 0.53], one_order: [0.53, 0.62], graded: [0.62, 0.72], nearfield: [0.72, 0.82],
			focus: [0.82, 0.91], efficiency: [0.91, 1]
		};
		const CH: Record<string, [number, number]> = {};
		for (const [cid, r] of Object.entries(fallback)) CH[cid] = (spec.chapters.find((c) => c.id === cid)?.p ?? r) as [number, number];
		const cq = (cid: string, p: number) => seg(p, CH[cid][0], CH[cid][1]);
		const inCh = (cid: string, p: number) => p >= CH[cid][0] && p < CH[cid][1];

		// ---------------------------------------------------------------------------- data from the plots
		const plotPts = (pid: string, name: string): [number, number][] => {
			const s = spec.plots?.find((q) => q.id === pid)?.series?.find((q) => q.name === name);
			return (s?.points ?? []).filter((q) => Number.isFinite(q[0]) && Number.isFinite(q[1])).slice().sort((a, b) => a[0] - b[0]);
		};
		const MEAS = plotPts('graded', 'measured'); // 25 squares, z µm, depth nm
		const CALC = plotPts('graded', 'calculated');
		const TRACE = plotPts('nearfield', 'measured'); // x mm, intensity
		const NSUB = 25;
		const subDepth = (i: number) => (MEAS[i] ? MEAS[i][1] : 0);
		// cumulative out-coupled intensity along the grating (trapezoid), for the illustrative guided-power fade
		const cum: [number, number][] = [[0, 0]];
		for (let i = 1; i < TRACE.length; i++) {
			const a = TRACE[i - 1], b = TRACE[i];
			cum.push([b[0], cum[cum.length - 1][1] + 0.5 * (Math.max(0, a[1]) + Math.max(0, b[1])) * (b[0] - a[0])]);
		}
		const cumTot = cum[cum.length - 1][1] || 1;

		// ---------------------------------------------------------------------------- SVG scaffolding
		const mk = <K extends keyof SVGElementTagNameMap>(tag: K, parent: Element, attrs: Record<string, string | number> = {}): SVGElementTagNameMap[K] => {
			const e = document.createElementNS(NS, tag) as SVGElementTagNameMap[K];
			for (const [a, v] of Object.entries(attrs)) e.setAttribute(a, String(v));
			parent.appendChild(e);
			return e;
		};
		const root = mk('g', svg, { 'data-scene': 'grating-couplers' });
		const defs = mk('defs', root);
		const glow = mk('filter', defs, { id: `${id}-glow`, x: '-50%', y: '-50%', width: '200%', height: '200%', 'color-interpolation-filters': 'sRGB' });
		mk('feGaussianBlur', glow, { stdDeviation: 3 });
		const hatchPat = mk('pattern', defs, { id: `${id}-hatch`, patternUnits: 'userSpaceOnUse', width: 7, height: 7, patternTransform: 'rotate(45)' });
		const hatchLine = mk('line', hatchPat, { x1: 0, y1: 0, x2: 0, y2: 7, 'stroke-width': 1 });
		const vfade = mk('linearGradient', defs, { id: `${id}-vfade`, x1: 0, y1: 1, x2: 0, y2: 0 });
		const vf0 = mk('stop', vfade, { offset: 0, 'stop-opacity': 1 });
		const vf1 = mk('stop', vfade, { offset: 1, 'stop-opacity': 0 });
		const efade = mk('linearGradient', defs, { id: `${id}-efade`, x1: 0, y1: 1, x2: 0, y2: 0 });
		const ef0 = mk('stop', efade, { offset: 0, 'stop-opacity': 1 });
		const ef1 = mk('stop', efade, { offset: 1, 'stop-opacity': 0 });
		const qfade = mk('linearGradient', defs, { id: `${id}-qfade`, x1: 0, y1: 0, x2: 0, y2: 1 });
		const qf0 = mk('stop', qfade, { offset: 0 });
		const qf1 = mk('stop', qfade, { offset: 1, 'stop-opacity': 0 });
		const NG = 64;
		const mkLin = (gid: string) => {
			const g = mk('linearGradient', defs, { id: `${id}-${gid}`, gradientUnits: 'userSpaceOnUse' });
			const stops = Array.from({ length: NG }, (_, i) => mk('stop', g, { offset: (i / (NG - 1)).toFixed(4), 'stop-opacity': 0 }));
			return { g, stops };
		};
		const linA = mkLin('gA');
		const linC = mkLin('gC');
		const linD = mkLin('gD');
		const clipB = mk('clipPath', defs, { id: `${id}-clipB` });
		const clipBPath = mk('path', clipB);

		const path = (parent: Element, part: string | null, attrs: Record<string, string | number> = {}): PathEl => {
			const e = mk('path', parent, { 'stroke-linejoin': 'round', 'stroke-linecap': 'round', ...attrs });
			if (part) e.setAttribute('data-pick', part);
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
		const f1 = (v: number) => (Math.round(v * 10) / 10).toString();
		const dOf = (q: P2[], close = true) => (q.length < 2 ? '' : 'M' + q.map((v) => `${f1(v[0])} ${f1(v[1])}`).join('L') + (close ? 'Z' : ''));
		const pal = () => PAL[theme];
		const on = (pid: string) => hi.includes(pid);
		const hl = (c: string, pid: string) => (on(pid) ? mix(c, pal().accent, 0.55) : c);
		const paint = (e: PathEl, d: string, fill: string, fo: number, stroke: string, so: number, sw = 1, pid?: string) => {
			e.setAttribute('d', d);
			e.setAttribute('fill', fill === 'none' ? 'none' : pid ? hl(fill, pid) : fill);
			e.setAttribute('fill-opacity', fo.toFixed(3));
			const lit = pid && on(pid);
			e.setAttribute('stroke', lit ? pal().accent : stroke);
			e.setAttribute('stroke-opacity', (lit ? 0.95 : so).toFixed(3));
			e.setAttribute('stroke-width', String(lit ? Math.max(1.4, sw) : sw));
		};
		/** arrow head (filled triangle) at screen point tip, pointing along tip - from */
		const head = (tip: P2, from: P2, size: number): string => {
			const dx = tip[0] - from[0], dy = tip[1] - from[1];
			const l = Math.hypot(dx, dy) || 1;
			const ux = dx / l, uy = dy / l;
			const b: P2 = [tip[0] - ux * size, tip[1] - uy * size];
			return dOf([tip, [b[0] - uy * size * 0.45, b[1] + ux * size * 0.45], [b[0] + uy * size * 0.45, b[1] - ux * size * 0.45]]);
		};
		interface Ray {
			soft: PathEl;
			core: PathEl;
			hd: PathEl;
			hit: PathEl;
		}
		const mkRay = (parent: Element, pid: string): Ray => ({
			soft: path(parent, null, { fill: 'none', filter: `url(#${id}-glow)`, 'pointer-events': 'none' }),
			core: path(parent, null, { fill: 'none', 'pointer-events': 'none' }),
			hd: path(parent, null, { 'pointer-events': 'none' }),
			hit: path(parent, pid, { fill: 'none', stroke: 'transparent', 'stroke-width': 10 })
		});
		/** ray between screen points a -> b (head at b), drawn up to fraction t of its length */
		const drawRay = (r: Ray, a: P2, b: P2, o: number, width: number, t: number, pid: string, arrow = true) => {
			if (o < 0.01 || t < 0.01) {
				for (const e of [r.soft, r.core, r.hd, r.hit]) show(e, 0);
				return;
			}
			const c = pal();
			const e: P2 = [lerp(a[0], b[0], t), lerp(a[1], b[1], t)];
			const d = dOf([a, e], false);
			const col = on(pid) ? mix(c.beam, c.accent, 0.45) : c.beam;
			r.soft.setAttribute('d', d);
			r.soft.setAttribute('stroke', col);
			r.soft.setAttribute('stroke-width', f1(width * 3));
			r.core.setAttribute('d', d);
			r.core.setAttribute('stroke', theme === 'light' ? col : c.core);
			r.core.setAttribute('stroke-width', f1(width));
			r.hit.setAttribute('d', d);
			show(r.soft, o * c.glowA * 0.7);
			show(r.core, o);
			show(r.hit, 1);
			if (arrow && t > 0.98) {
				r.hd.setAttribute('d', head(e, a, 6 + width * 2));
				r.hd.setAttribute('fill', theme === 'light' ? col : c.core);
				show(r.hd, o);
			} else show(r.hd, 0);
		};

		// ---------------------------------------------------------------------------- view groups
		const gA = mk('g', root);
		const gB = mk('g', root);
		const gC = mk('g', root);
		const gD = mk('g', root);
		const gE = mk('g', root);

		// A: chip side view
		const aSub = { side: path(gA, 'substrate'), top: path(gA, 'substrate'), front: path(gA, 'substrate') };
		const aPlate = { side: path(gA, 'pmma_plate'), top: path(gA, 'pmma_plate'), floor: path(gA, 'pmma_plate'), front: path(gA, 'pmma_plate'), heat: path(gA, 'pmma_plate') };
		const aFilm = { side: path(gA, 'resist_film'), top: path(gA, 'resist_film'), floor: path(gA, 'resist_film'), front: path(gA, 'resist_film') };
		const aHatch = path(gA, null, { fill: 'none', 'pointer-events': 'none' });
		const aPams = { side: path(gA, 'pams_film'), top: path(gA, 'pams_film'), front: path(gA, 'pams_film') };
		const aGHit = [path(gA, 'grating_in', { stroke: 'none' }), path(gA, 'grating_out', { stroke: 'none' })];
		const aMetal = { top: path(gA, 'metal_layer'), front: path(gA, 'metal_layer') };
		const aBreak = path(gA, 'brk', { fill: 'none' });
		const aMaster = { ni: path(gA, 'nickel_master'), niH: path(gA, 'nickel_master'), cu: path(gA, 'nickel_master') };
		const aGlow = { soft: path(gA, null, { filter: `url(#${id}-glow)`, 'pointer-events': 'none' }), core: path(gA, 'guided_mode') };
		const aMode = path(gA, 'guided_mode', { fill: 'none' });
		const aArrow = { l: path(gA, null, { fill: 'none', 'pointer-events': 'none' }), hd: path(gA, null, { 'pointer-events': 'none' }) };
		const rayIn = mkRay(gA, 'beam_in');
		const raysIn = Array.from({ length: 6 }, () => mkRay(gA, 'orders_in'));
		const raysOut = Array.from({ length: 6 }, () => mkRay(gA, 'orders_out'));

		// B: close-up
		const bQ = path(gB, 'substrate');
		const bFilm = path(gB, 'resist_film');
		const bTintG = mk('g', gB, { 'clip-path': `url(#${id}-clipB)` });
		const bTint = Array.from({ length: B.NP * B.NS + 1 }, () => path(bTintG, 'dose_tint', { stroke: 'none' }));
		const bEdge = path(gB, null, { fill: 'none', 'pointer-events': 'none' });
		const bGHit = path(gB, 'grating_in', { stroke: 'none' });
		const bMetal = path(gB, 'metal_layer');
		const bBeam = { soft: path(gB, null, { filter: `url(#${id}-glow)`, 'pointer-events': 'none' }), core: path(gB, 'ebeam') };
		const bDims = path(gB, null, { fill: 'none', 'pointer-events': 'none' });
		const bDimsHd = path(gB, null, { 'pointer-events': 'none' });

		// C: Fig. 3
		const cSub = path(gC, 'sio2_plate');
		const cPrism = path(gC, 'prism');
		const cPrismH = path(gC, 'prism', { stroke: 'none' });
		const cLiquid = path(gC, 'prism');
		const cFilm = path(gC, 'oo_film');
		const cGHit = path(gC, 'grating_one_order', { stroke: 'none' });
		const cGlow = { soft: path(gC, null, { filter: `url(#${id}-glow)`, 'pointer-events': 'none' }), core: path(gC, 'oo_guided') };
		const cArrow = { l: path(gC, null, { fill: 'none', 'pointer-events': 'none' }), hd: path(gC, null, { 'pointer-events': 'none' }) };
		const cRays = [mkRay(gC, 'oo_beam'), mkRay(gC, 'oo_beam'), mkRay(gC, 'oo_beam')];
		const cZero = [mkRay(gC, 'oo_zero'), mkRay(gC, 'oo_zero')];

		// D: graded grating
		const dSub = { side: path(gD, 'substrate'), top: path(gD, 'substrate'), front: path(gD, 'substrate') };
		const dFilm = { side: path(gD, 'resist_film'), top: path(gD, 'resist_film'), floor: path(gD, 'resist_film'), front: path(gD, 'resist_film') };
		const dTicks = path(gD, null, { fill: 'none', 'pointer-events': 'none' });
		const dGHit = path(gD, 'graded_grating', { stroke: 'none' });
		const dGlow = { soft: path(gD, null, { filter: `url(#${id}-glow)`, 'pointer-events': 'none' }), core: path(gD, 'nf_guided') };
		const dCalc = path(gD, 'design_depth', { fill: 'none', 'stroke-dasharray': '5 4' });
		const dCalcHit = path(gD, 'design_depth', { fill: 'none', stroke: 'transparent', 'stroke-width': 9 });
		const dBreak = path(gD, 'brk_d', { fill: 'none' });
		const dPen = path(gD, null, { fill: 'none', 'pointer-events': 'none' });
		const dEmG = mk('g', gD);
		const NEM = 100;
		const dEm = Array.from({ length: NEM }, () => path(dEmG, 'outcoupled_beam', { stroke: 'none', fill: `url(#${id}-vfade)` }));

		// E: focusing chip
		const eSub = { side: path(gE, 'substrate'), top: path(gE, 'substrate'), front: path(gE, 'substrate') };
		const eFilm = { side: path(gE, 'resist_film'), top: path(gE, 'resist_film'), front: path(gE, 'resist_film') };
		const eTrench = [path(gE, 'strip_waveguide'), path(gE, 'strip_waveguide')];
		const eWall = [path(gE, 'strip_waveguide'), path(gE, 'strip_waveguide')];
		const eStripTop = path(gE, 'strip_waveguide');
		const eLines = path(gE, 'focusing_gratings', { fill: 'none' });
		const eLinesHit = path(gE, 'focusing_gratings', { fill: 'none', stroke: 'transparent', 'stroke-width': 8 });
		const eFan = [0, 1, 2, 3].map(() => ({ soft: path(gE, null, { filter: `url(#${id}-glow)`, 'pointer-events': 'none' }), core: path(gE, 'fan', { stroke: 'none' }) }));
		const eStrip = { soft: path(gE, null, { fill: 'none', filter: `url(#${id}-glow)`, 'pointer-events': 'none' }), core: path(gE, 'strip_light', { fill: 'none' }) };
		const eIn = mkRay(gE, 'beam_in_iso');
		const eOut = mkRay(gE, 'out_beam');

		// ---------------------------------------------------------------------------- regions and cameras
		const regions = (): { full: Rgn; plot: Rgn } => {
			if (w < 700) return { full: [0.04, 0.22, 0.96, 0.95], plot: [0.04, 0.2, 0.96, 0.43] };
			const top = Math.min(0.26, 170 / Math.max(1, h));
			return { full: [0.04, top, 0.97, 0.93], plot: [0.02, top + 0.04, 0.46, 0.9] };
		};
		const fit = (b: Box, rg: Rgn, zoom = 1): Cam => {
			const rx0 = rg[0] * w, ry0 = rg[1] * h, rw = (rg[2] - rg[0]) * w, rh = (rg[3] - rg[1]) * h;
			return {
				s: Math.min(rw / (b.x1 - b.x0), rh / (b.y1 - b.y0)) * zoom,
				cx: (b.x0 + b.x1) / 2,
				cy: (b.y0 + b.y1) / 2,
				rx: rx0 + rw / 2,
				ry: ry0 + rh / 2
			};
		};
		let cam: Cam = { s: 1, cx: 0, cy: 0, rx: 0, ry: 0 };
		const S2 = (X: number, Y: number): P2 => [cam.rx + cam.s * (X - cam.cx), cam.ry - cam.s * (Y - cam.cy)];
		const poly2 = (q: P2[], close = true) => dOf(q.map((v) => S2(v[0], v[1])), close);

		const BOX_A_SLAB: Box = { x0: -30, x1: A.L + A.OX + 30, y0: -A.SD - 20, y1: 130 };
		const BOX_A_LIGHT: Box = { x0: -30, x1: A.L + A.OX + 30, y0: -A.SD - 20, y1: 200 };
		const BOX_A_REP: Box = { x0: -30, x1: A.L + A.OX + 30, y0: -A.SD - 20, y1: 280 };
		const BOX_A_ZOOM: Box = { x0: 80, x1: 340, y0: -50, y1: 130 };
		const BOX_B: Box = { x0: B.X0 - 120, x1: B.X1 + 220, y0: -B.Q - 20, y1: 1250 };
		const BOX_C: Box = { x0: -10, x1: 900, y0: -530, y1: 40 };
		const BOX_D: Box = { x0: D.XL - 10, x1: D.XR + D.OX + 10, y0: -D.SUB - 10, y1: D.TF * D.KY + D.EH + 10 };

		// iso projection
		const projRaw = (X: number, Y: number, Z: number): P2 => {
			const ca = Math.cos(E.AZ * DEG), sa = Math.sin(E.AZ * DEG);
			return [X * ca - Y * sa, -((X * sa + Y * ca) * Math.sin(E.EL * DEG) - Z * Math.cos(E.EL * DEG))];
		};
		const BOX_E = (() => {
			let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
			const add = (q: P2) => {
				x0 = Math.min(x0, q[0]); x1 = Math.max(x1, q[0]); y0 = Math.min(y0, q[1]); y1 = Math.max(y1, q[1]);
			};
			for (const X of [E.X0, E.X1]) for (const Y of [E.Y0, E.Y1]) for (const Z of [E.ZS, E.ZF]) add(projRaw(X, Y, Z));
			add(projRaw(9.6, 0, 5.4));
			add(projRaw(-9.6, 0, 5.4));
			return { x0: x0 - 0.2, x1: x1 + 0.2, y0: y0 - 0.2, y1: y1 + 0.2 } as Box;
		})();
		const S3 = (X: number, Y: number, Z: number): P2 => {
			const q = projRaw(X, Y, Z);
			return S2(q[0], q[1]);
		};

		// ---------------------------------------------------------------------------- view A: chip side view
		/** extruded block (front face polygon given; top face and right side from the top edge / right edge) */
		const block = (
			el: { side: PathEl; top: PathEl; front: PathEl; floor?: PathEl },
			front: P2[],
			topY: number,
			x0: number,
			x1: number,
			yb: number,
			col: string,
			fa: number,
			ta: number,
			edge: string,
			pid: string,
			o: number,
			ox = A.OX,
			oy = A.OY,
			grooves: P2[] = []
		) => {
			if (el.floor) {
				// groove gaps of the front section: filled with the top-face colour (the corrugated surface receding
				// behind the section); the closed top profile covers exactly the gaps below the top line
				if (o >= 0.01 && grooves.length > 2) {
					paint(el.floor, poly2(grooves), col, ta * 0.85, 'none', 0, 1, pid);
					show(el.floor, o);
				} else show(el.floor, 0);
			}
			if (o < 0.01 || x1 <= x0 + 0.01) {
				for (const e of [el.side, el.top, el.front]) show(e, 0);
				return;
			}
			paint(el.side, poly2([[x1, yb], [x1, topY], [x1 + ox, topY + oy], [x1 + ox, yb + oy]]), mix(col, '#000000', 0.25), fa * 0.9, edge, 0.5, 1, pid);
			paint(el.top, poly2([[x0, topY], [x1, topY], [x1 + ox, topY + oy], [x0 + ox, topY + oy]]), col, ta, edge, 0.5, 1, pid);
			paint(el.front, poly2(front), col, fa, edge, 0.75, 1, pid);
			for (const e of [el.side, el.top, el.front]) show(e, o);
		};

		/** guided power along the side-view chip (input build-up, 0.6 or 1.2 dB/cm over 20 mm, exp(-2 alpha z) under the
		 *  output grating, 1 mm long) */
		const guidedPower = (X: number, rep: boolean): number => {
			const g0 = A.G0, g1 = A.G0 + A.NT * A.PER, o0 = A.L - g1, o1 = A.L - g0;
			const lossDb = rep ? 1.2 * 2 : 0.6 * 2; // dB over the 20 mm
			const alpha = rep ? 0.75 : 1.48; // 1/mm
			if (X < g0) return 0;
			if (X < g1) return (X - g0) / (g1 - g0);
			if (X < o0) return 10 ** ((-lossDb * (X - g1)) / (o0 - g1) / 10);
			const pin = 10 ** (-lossDb / 10);
			if (X < o1) return pin * Math.exp((-2 * alpha * (X - o0)) / (o1 - o0));
			return 0;
		};
		// Fig. 2 directions (screen-measured on the figure, Y up): reflection, transmission, cover, substrate orders
		const DIR = {
			i0: [217, -153] as P2,
			r: [[-113, 103], [2, 140], [115, 75]] as P2[],
			t: [[-137, -35], [-45, -120], [140, -70]] as P2[],
			c: [[-112, 97], [0, 145], [120, 75]] as P2[],
			s: [[-132, -35], [-40, -120], [125, -65]] as P2[]
		};
		const unit = (v: P2): P2 => {
			const l = Math.hypot(v[0], v[1]) || 1;
			return [v[0] / l, v[1] / l];
		};

		interface LightA {
			on: number;
			beam: number;
			ordersIn: number;
			front: number;
			ordersOut: number;
			mode: number;
		}
		const lightA = (q0: number, q1: number, q: number): LightA => {
			const k = (a: number, b: number) => seg(q, lerp(q0, q1, a), lerp(q0, q1, b));
			return {
				on: k(0, 0.04),
				beam: easeOut(k(0, 0.2)),
				ordersIn: k(0.18, 0.3),
				front: lerp(A.G0 - 2, A.L + 4, ease(k(0.2, 0.75))),
				ordersOut: k(0.68, 0.85),
				mode: k(0.35, 0.5)
			};
		};

		const drawA = (p: number, o: number) => {
			if (!show(gA, o)) return;
			const c = pal();
			// camera
			let cA: Cam;
			const R = regions().full;
			if (p < CH.resist[1]) cA = fit(BOX_A_SLAB, R);
			else if (p < CH.develop[0]) cA = blend(fit(BOX_A_SLAB, R), fit(BOX_A_ZOOM, R), ease(seg(cq('write', p), 0, 0.3)));
			else if (p < CH.replica[0]) cA = blend(fit(BOX_A_ZOOM, R), fit(BOX_A_LIGHT, R), ease(seg(cq('couple', p), 0, 0.22)));
			else cA = blend(fit(BOX_A_LIGHT, R), fit(BOX_A_REP, R), ease(seg(cq('replica', p), 0, 0.1)));
			cam = cA;

			const sq = cq('substrate', p), rq = cq('resist', p), xq = cq('replica', p);
			const rep = p >= CH.replica[0];
			// light geometry of the all-polymer chip once the PaMS film is there
			const lrep = rep && (xq >= 0.7 || p >= CH.one_order[0]);
			const T = A.T;
			// phases of the replica chapter (Fig. 1 sequence)
			const ni = rep ? ease(seg(xq, 0.04, 0.14)) : 0;
			const cu = rep ? ease(seg(xq, 0.12, 0.2)) : 0;
			const lift = rep ? ease(seg(xq, 0.2, 0.28)) : 0;
			const chipOut = rep ? ease(seg(xq, 0.22, 0.32)) : 0;
			const plateIn = rep ? easeOut(seg(xq, 0.28, 0.36)) : 0;
			const heat = rep ? seg(xq, 0.34, 0.4) * (1 - seg(xq, 0.62, 0.7)) : 0;
			const down = rep ? ease(seg(xq, 0.4, 0.5)) : 0;
			const up = rep ? ease(seg(xq, 0.52, 0.6)) : 0;
			const masterA = rep ? 1 - seg(xq, 0.58, 0.64) : 0;
			const pams = rep ? ease(seg(xq, 0.7, 0.8)) : 0; // after cooling (heat tint gone by 0.7)
			// master offset: on the chip (0), lifted (+90), pressed (-T), lifted again
			const dyLift = 90;
			const dy = xq < 0.4 ? lift * dyLift : xq < 0.52 ? lerp(dyLift, -T, down) : lerp(-T, dyLift, up);
			const dyMin = xq < 0.4 ? dyLift : xq < 0.52 ? lerp(dyLift, -T, down) : -T;

			// chip (substrate + film): slides in, then (replica) slides down and fades
			const subIn = p < CH.substrate[1] ? easeOut(seg(sq, 0, 0.5)) : 1;
			const chipDy = -(1 - subIn) * 120 - chipOut * 70;
			const chipA = subIn * (1 - chipOut);
			const sh = (q: P2[]) => q.map((v) => [v[0], v[1] + chipDy] as P2);
			block(aSub, sh([[0, -A.SD], [A.L, -A.SD], [A.L, 0], [0, 0]]), chipDy, 0, A.L, -A.SD + chipDy, c.sub, c.subA, c.subA * 1.4, c.subEdge, 'substrate', chipA);

			// film: spin coating spreads from the centre and thins; developed teeth after the develop chapter
			const fw = p < CH.resist[0] ? 0 : p < CH.resist[1] ? ease(seg(rq, 0.05, 0.6)) : 1;
			const g = p >= CH.develop[1] ? 1 : 0;
			const tf = T * lerp(2.4, 1, ease(seg(rq, 0.05, 0.6)));
			const xa = A.L / 2 - (A.L / 2) * fw, xb = A.L / 2 + (A.L / 2) * fw;
			const prof = sideProfile(g, T);
			const filmPid = p >= CH.couple[0] ? 'waveguide' : 'resist_film';
			if (fw > 0.001) {
				const top = fw >= 1 ? prof : ([[xa, tf], [xb, tf]] as P2[]);
				const front: P2[] = [[xa, 0], [xb, 0], ...top.slice().reverse()];
				const fls: P2[] = g && fw >= 1 ? sh(prof) : [];
				block(aFilm, sh(front), (fw >= 1 ? T : tf) + chipDy, xa, xb, chipDy, c.film, c.filmA, c.filmTopA, c.filmEdge, filmPid, chipA, A.OX, A.OY, fls);
			} else block(aFilm, [], 0, 0, 0, 0, c.film, 0, 0, c.filmEdge, filmPid, 0);
			// grating lines seen on the top face + hit areas
			if (g && chipA > 0.01) {
				const hs: string[] = [];
				for (const x0 of [A.G0, A.L - A.G0 - A.NT * A.PER]) {
					for (let i = 0; i <= A.NT; i++) {
						const x = x0 + i * A.PER;
						hs.push(poly2([[x, T + chipDy], [x + A.OX, T + A.OY + chipDy]], false));
					}
				}
				paint(aHatch, hs.join(''), 'none', 0, c.filmEdge, 0.7, 1);
				show(aHatch, chipA);
				const gx = [A.G0, A.L - A.G0 - A.NT * A.PER];
				aGHit.forEach((e, i) => {
					paint(e, poly2(sh([[gx[i], T - A.R - A.D - 2], [gx[i] + A.NT * A.PER, T - A.R - A.D - 2], [gx[i] + A.NT * A.PER + A.OX, T + A.OY], [gx[i] + A.OX, T + A.OY]])), on(i ? 'grating_out' : 'grating_in') ? c.accent : '#000000', on(i ? 'grating_out' : 'grating_in') ? 0.18 : 0.001, 'none', 0);
					show(e, chipA);
				});
			} else {
				show(aHatch, 0);
				aGHit.forEach((e) => show(e, 0));
			}
			// metal layer: settles in the resist chapter, present while writing
			const metal = p < CH.resist[0] ? 0 : p < CH.resist[1] ? ease(seg(rq, 0.62, 0.9)) : p < CH.develop[0] ? 1 : 0;
			if (metal > 0.01 && fw >= 1) {
				const my = T + (1 - metal) * 30 + chipDy;
				paint(aMetal.top, poly2([[0, my + 3], [A.L, my + 3], [A.L + A.OX, my + 3 + A.OY], [A.OX, my + 3 + A.OY]]), c.metal, 0.55, c.metal, 0.7, 1, 'metal_layer');
				paint(aMetal.front, poly2([[0, my], [A.L, my], [A.L, my + 3], [0, my + 3]]), c.metal, 0.95, c.metal, 0.9, 1, 'metal_layer');
				show(aMetal.top, metal);
				show(aMetal.front, metal);
			} else {
				show(aMetal.top, 0);
				show(aMetal.front, 0);
			}

			// PMMA plate (replica): embossed by the master, heated
			const plateTop = clampBelow(prof.map((v) => [v[0], v[1] + Math.min(dyMin, dyLift) ] as P2), 0);
			if (plateIn > 0.01) {
				const pdy = -(1 - plateIn) * 80;
				const pt = plateTop.map((v) => [v[0], v[1] + pdy] as P2);
				const flp: P2[] = pams < 0.99 ? pt : [];
				block(aPlate, [[0, -A.SD + pdy], [A.L, -A.SD + pdy], ...pt.slice().reverse()], pdy, 0, A.L, -A.SD + pdy, c.pmma, c.pmmaA, c.pmmaA * 1.4, c.subEdge, 'pmma_plate', plateIn, A.OX, A.OY, flp);
				if (heat > 0.01) {
					paint(aPlate.heat, poly2([[0, -A.SD + pdy], [A.L, -A.SD + pdy], ...pt.slice().reverse()]), c.heat, 0.08, 'none', 0);
					show(aPlate.heat, heat);
				} else show(aPlate.heat, 0);
			} else {
				block(aPlate, [], 0, 0, 0, 0, c.pmma, 0, 0, c.subEdge, 'pmma_plate', 0, A.OX, A.OY, []);
				show(aPlate.heat, 0);
			}
			// PaMS film over the embossed plate, flat top
			if (pams > 0.01) {
				const pa = A.L / 2 - (A.L / 2) * pams, pb = A.L / 2 + (A.L / 2) * pams;
				const bot = clipLineX(plateTop, pa, pb);
				const tp = A.TP * lerp(2, 1, pams);
				block(aPams, [...bot, [pb, tp], [pa, tp]], tp, pa, pb, 0, c.pams, c.pamsA, c.pamsA * 1.3, c.pams, 'pams_film', 1);
			} else block(aPams, [], 0, 0, 0, 0, c.pams, 0, 0, c.pams, 'pams_film', 0);

			// metal master: nickel grows into the grooves, copper backing, lift, press, lift
			if (rep && ni > 0.01 && masterA > 0.01) {
				// nickel grows on the surface: fills the grooves first, then a flat layer
				const niTop = lerp(T - A.R - A.D, T + A.NI, ni);
				const bot = prof.map((v) => [v[0], v[1] + dy] as P2);
				const upper = prof.map((v) => [v[0], Math.max(v[1], niTop) + dy] as P2);
				const niShape: P2[] = [...bot, ...upper.slice().reverse()];
				paint(aMaster.ni, poly2(niShape), c.nickel, 0.5, c.nickel, 0.9, 1, 'nickel_master');
				paint(aMaster.niH, poly2(niShape), `url(#${id}-hatch)`, 0.6, 'none', 0);
				aMaster.niH.setAttribute('fill', `url(#${id}-hatch)`);
				show(aMaster.ni, masterA);
				show(aMaster.niH, masterA);
				if (cu > 0.01) {
					const c0 = niTop + dy, c1 = niTop + A.CU * cu + dy;
					paint(aMaster.cu, poly2([[0, c0], [A.L, c0], [A.L, c1], [0, c1]]), c.copper, 0.55, c.copper, 0.9, 1, 'nickel_master');
					show(aMaster.cu, masterA);
				} else show(aMaster.cu, 0);
			} else for (const e of [aMaster.ni, aMaster.niH, aMaster.cu]) show(e, 0);

			// break mark (20 mm compressed)
			const brkA = p >= CH.couple[0] ? 1 : 0;
			if (brkA && (chipA > 0.01 || pams > 0.01)) {
				const yTop = lrep ? A.TP : T;
				const by = lrep ? 0 : chipDy;
				const ds = [-6, 6].map((dx) => poly2([[A.BRK + dx - 8, -18 + by], [A.BRK + dx + 8, yTop + 16 + by]], false));
				paint(aBreak, ds.join(''), 'none', 0, c.ink, 0.8, 1.3);
				show(aBreak, lrep ? pams : chipA);
			} else show(aBreak, 0);

			// light: couple chapter (chip) or end of the replica chapter (PaMS film)
			let L: LightA | null = null;
			if (inCh('couple', p)) L = lightA(0.22, 1.0, cq('couple', p));
			else if (inCh('replica', p) && xq >= 0.8) L = lightA(0.8, 0.99, xq);
			else if (inCh('one_order', p) && rep) {
				L = lightA(0.8, 0.99, 1);
				L.on = 1 - seg(cq('one_order', p), 0, 0.12);
			} else if (inCh('replica', p) && xq < 0.06) {
				L = lightA(0, 1, 1);
				L.on = 1 - seg(xq, 0, 0.05);
			}
			const yTop = lrep ? A.TP : T; // film top
			const yG = lrep ? -(A.R + A.D / 2) : T - A.R - A.D / 2; // grating level
			const yBot = lrep ? -(A.R + A.D) : 0; // film bottom under the grating
			if (L && L.on > 0.01) {
				const share = lrep ? 0.74 : 0.65;
				// guided glow
				const y0 = lrep ? 4 : T * 0.18, y1 = lrep ? A.TP - 4 : T * 0.82;
				const sx0 = S2(0, (y0 + y1) / 2), sx1 = S2(A.L, (y0 + y1) / 2);
				linA.g.setAttribute('x1', f1(sx0[0]));
				linA.g.setAttribute('y1', f1(sx0[1]));
				linA.g.setAttribute('x2', f1(sx1[0]));
				linA.g.setAttribute('y2', f1(sx1[1]));
				linA.stops.forEach((st, i) => {
					const X = (i / (NG - 1)) * A.L;
					const edge = clamp01((L!.front - X) / 30);
					st.setAttribute('stop-color', c.beam);
					st.setAttribute('stop-opacity', (guidedPower(X, lrep) * edge).toFixed(3));
				});
				const gp = poly2([[A.G0, y0], [A.L - A.G0, y0], [A.L - A.G0, y1], [A.G0, y1]]);
				paint(aGlow.soft, gp, `url(#${id}-gA)`, 1, 'none', 0);
				paint(aGlow.core, gp, `url(#${id}-gA)`, 1, 'none', 0);
				aGlow.soft.setAttribute('fill', `url(#${id}-gA)`);
				aGlow.core.setAttribute('fill', `url(#${id}-gA)`);
				show(aGlow.soft, L.on * c.glowA);
				show(aGlow.core, L.on * 0.75);
				// mode sketch and guided arrow (Fig. 2)
				const mx = 410;
				const mid = (y0 + y1) / 2, half = (y1 - y0) / 2 + 8;
				const prof2: P2[] = [];
				for (let k = 0; k <= 24; k++) {
					const Y = mid - 2.2 * half + (4.4 * half * k) / 24;
					prof2.push([mx + 34 * Math.exp(-(((Y - mid) / (half * 0.75)) ** 2)), Y]);
				}
				paint(aMode, poly2([[mx, mid - 2.4 * half], [mx, mid + 2.4 * half]], false) + poly2(prof2, false), 'none', 0, c.ink, 0.75, 1, 'guided_mode');
				show(aMode, L.on * L.mode);
				const a0 = S2(330, mid), a1 = S2(390, mid);
				paint(aArrow.l, dOf([a0, a1], false), 'none', 0, theme === 'light' ? c.beam : c.core, 0.9, 1.4);
				paint(aArrow.hd, head(a1, a0, 7), theme === 'light' ? c.beam : c.core, 1, 'none', 0);
				show(aArrow.l, L.on * L.mode);
				show(aArrow.hd, L.on * L.mode);
				// incoming beam I0 (Fig. 2 angle)
				const u0 = unit(DIR.i0);
				const tip: P2 = [XI, yG];
				const len = 200;
				drawRay(rayIn, S2(tip[0] - u0[0] * len, tip[1] - u0[1] * len), S2(tip[0], tip[1]), L.on, 2.2, L.beam, 'beam_in', false);
				// reflected / transmitted orders at the input grating (faint, illustrative)
				const rl = 105;
				raysIn.forEach((r, i) => {
					const up = i < 3;
					const d = unit(up ? DIR.r[i] : DIR.t[i - 3]);
					const a: P2 = up ? [XI, yTop - (lrep ? 0 : A.R)] : [XI, yBot];
					drawRay(r, S2(a[0], a[1]), S2(a[0] + d[0] * rl, a[1] + d[1] * rl), L!.on * 0.32, 1, L!.ordersIn, 'orders_in');
				});
				// out-coupled orders at the output grating: cover group brighter (65 % / 74 %), equal within a side
				raysOut.forEach((r, i) => {
					const up = i < 3;
					const d = unit(up ? DIR.c[i] : DIR.s[i - 3]);
					const a: P2 = up ? [XO, yTop - (lrep ? 0 : A.R)] : [XO, yBot];
					const bright = up ? share : 1 - share;
					drawRay(r, S2(a[0], a[1]), S2(a[0] + d[0] * rl, a[1] + d[1] * rl), L!.on * Math.min(1, bright * 1.35), 1.2 + bright, L!.ordersOut, 'orders_out');
				});
			} else {
				for (const e of [aGlow.soft, aGlow.core, aMode, aArrow.l, aArrow.hd]) show(e, 0);
				for (const r of [rayIn, ...raysIn, ...raysOut]) drawRay(r, [0, 0], [0, 0], 0, 1, 0, '');
			}
		};

		// ---------------------------------------------------------------------------- view B: close-up (nm)
		// Dose staircase in register with the drawn profile: each period's staircase starts in the middle of the steep
		// side (x0 + 100 nm), so the highest dose lies over the deepest part of the groove and the 200 nm steep side
		// straddles the low-to-high dose step. Sweep right to left: within a period the dose rises as the beam moves.
		const SH: [number, number, number][] = (() => {
			const out: [number, number, number][] = [];
			const sw = B.PER / B.NS;
			for (let j = B.NP - 1; j >= 0; j--)
				for (let i = B.NS - 1; i >= 0; i--) {
					const x0 = B.ST / 2 + j * B.PER + i * sw;
					if (x0 >= B.X1) continue;
					out.push([x0, Math.min(B.X1, x0 + sw), DOSE[i]]);
				}
			out.push([0, B.ST / 2, DOSE[B.NS - 1]]); // low-dose tail at the grating start
			return out;
		})();
		const SHOTS = SH.length;
		const shotRect = (k: number): [number, number, number] => SH[k];
		const drawB = (p: number, o: number) => {
			if (!show(gB, o)) return;
			const c = pal();
			const R = regions().full;
			const base = fit(BOX_B, R);
			const zw = p < CH.develop[0] ? lerp(0.22, 1, ease(seg(cq('write', p), 0.1, 0.32))) : p < CH.couple[0] ? 1 : lerp(1, 0.22, ease(seg(cq('couple', p), 0, 0.2)));
			cam = { ...base, s: base.s * zw };
			const wq = cq('write', p), dq = cq('develop', p);
			const dev = p < CH.develop[0] ? 0 : ease(seg(dq, 0.15, 0.7));
			const prof = closeProfile(dev);
			// quartz
			paint(bQ, poly2([[B.X0, -B.Q], [B.X1, -B.Q], [B.X1, 0], [B.X0, 0]]), `url(#${id}-qfade)`, 1, 'none', 0);
			bQ.setAttribute('fill', on('substrate') ? mix(c.sub, c.accent, 0.5) : `url(#${id}-qfade)`);
			qf0.setAttribute('stop-color', c.sub);
			qf0.setAttribute('stop-opacity', String(c.subA * 2.2));
			qf1.setAttribute('stop-color', c.sub);
			// film
			const filmPoly: P2[] = [[B.X0, 0], [B.X1, 0], ...prof.slice().reverse()];
			const fd = poly2(filmPoly);
			paint(bFilm, fd, c.film, c.filmA, 'none', 0, 1, 'resist_film');
			clipBPath.setAttribute('d', fd);
			paint(bEdge, poly2(prof, false) + poly2([[B.X0, 0], [B.X1, 0]], false), 'none', 0, c.filmEdge, 0.9, 1.2);
			// exposed resist, tinted by dose (latent image through the film thickness)
			const tWrite = p < CH.write[0] ? 0 : p >= CH.develop[0] ? SHOTS : seg(wq, 0.34, 0.95) * SHOTS;
			const tintFade = p < CH.develop[0] ? 1 : 1 - seg(dq, 0.55, 0.8);
			bTint.forEach((e, k) => {
				const grow = clamp01(tWrite - k);
				if (grow <= 0 || tintFade <= 0.01) return show(e, 0);
				const [x0, x1, dose] = shotRect(k);
				paint(e, poly2([[x0, 0], [x1, 0], [x1, B.TF], [x0, B.TF]]), c.dose, (0.1 + 0.5 * dose) * Math.min(1, grow * 3), 'none', 0, 1, 'dose_tint');
				show(e, tintFade);
			});
			// grating hit area (after development)
			if (dev > 0.5) {
				paint(bGHit, poly2([[0, B.TF - B.OFF - B.DEP - 20], [B.X1, B.TF - B.OFF - B.DEP - 20], [B.X1, B.TF + 40], [0, B.TF + 40]]), on('grating_in') ? c.accent : '#000000', on('grating_in') ? 0.15 : 0.001, 'none', 0);
				show(bGHit, 1);
			} else show(bGHit, 0);
			// metal layer (drawn as a line; thickness not stated)
			const metal = p < CH.develop[0] ? 1 : 1 - seg(dq, 0, 0.15);
			if (metal > 0.01) {
				paint(bMetal, poly2([[B.X0, B.TF], [B.X1, B.TF]], false), 'none', 0, hl(c.metal, 'metal_layer'), 1, 3);
				bMetal.setAttribute('stroke', hl(c.metal, 'metal_layer'));
				show(bMetal, metal);
			} else show(bMetal, 0);
			// shaped electron beam: one rectangle shot after the other
			const active = p >= CH.write[0] && p < CH.develop[0] && wq >= 0.34 && wq < 0.95;
			if (active) {
				const k = Math.min(SHOTS - 1, Math.floor(tWrite));
				const [x0, x1, dose] = shotRect(k);
				const d = poly2([[x0, B.TF + 4], [x1, B.TF + 4], [x1, BOX_B.y1], [x0, BOX_B.y1]]);
				ef0.setAttribute('stop-color', hl(c.ebeam, 'ebeam'));
				ef1.setAttribute('stop-color', hl(c.ebeam, 'ebeam'));
				paint(bBeam.soft, d, hl(c.ebeam, 'ebeam'), 0.5, 'none', 0);
				paint(bBeam.core, d, hl(c.ebeam, 'ebeam'), 0.25 + 0.55 * dose, 'none', 0, 1, 'ebeam');
				bBeam.core.setAttribute('fill', `url(#${id}-efade)`);
				bBeam.core.setAttribute('fill-opacity', (0.35 + 0.6 * dose).toFixed(3));
				bBeam.soft.setAttribute('fill', `url(#${id}-efade)`);
				show(bBeam.soft, 0.35 + 0.5 * dose);
				show(bBeam.core, 1);
			} else {
				show(bBeam.soft, 0);
				show(bBeam.core, 0);
			}
			// dimension marks for the canvas label: period (one period) and depth (last period)
			const dimA = p >= CH.develop[0] && p < CH.couple[0] ? ease(seg(dq, 0.72, 0.86)) : 0;
			if (dimA > 0.01) {
				const pk = B.TF - B.OFF, vl = B.TF - B.OFF - B.DEP;
				const yL = B.TF + 170;
				const xa = 1 * B.PER, xb = 2 * B.PER;
				const xr = B.X1 + 110;
				const segs = [
					poly2([[xa, pk + 20], [xa, yL + 40]], false), poly2([[xb, pk + 20], [xb, yL + 40]], false), poly2([[xa, yL], [xb, yL]], false),
					poly2([[(B.NP - 1) * B.PER + B.ST + 20, vl], [xr + 40, vl]], false), poly2([[B.X1 + 20, pk], [xr + 40, pk]], false), poly2([[xr, vl], [xr, pk]], false)
				];
				paint(bDims, segs.join(''), 'none', 0, c.inkSoft, 0.9, 1);
				const ha = S2(xa, yL), hb = S2(xb, yL), va = S2(xr, vl), vb = S2(xr, pk);
				paint(bDimsHd, [head(ha, hb, 6), head(hb, ha, 6), head(va, vb, 6), head(vb, va, 6)].join(''), c.inkSoft, 1, 'none', 0);
				bDims.setAttribute('stroke-dasharray', '');
				show(bDims, dimA);
				show(bDimsHd, dimA);
			} else {
				show(bDims, 0);
				show(bDimsHd, 0);
			}
		};

		// ---------------------------------------------------------------------------- view C: Fig. 3 single-order coupler
		// beam path: straight through prism, liquid and plate (index matched, assumed), Fig. 3 angle in the plate
		const cGeo = (() => {
			const ang = C3.ANG * DEG;
			const dIn: P2 = [Math.cos(ang), Math.sin(ang)];
			const top: P2 = [C3.HIT, C3.FT];
			const atY = (Y: number): P2 => [top[0] - (top[1] - Y) / Math.tan(ang), Y];
			const fb = atY(C3.FB);
			// entry on the sloped face (PL, PT) -> (PF, PB)
			const fx = (s: number): P2 => [C3.PL + (C3.PF - C3.PL) * s, C3.PT + (C3.PB - C3.PT) * s];
			const pTop = atY(C3.PT);
			// solve fx(s) + t dIn = pTop  ->  s e + t dIn = pTop - P0
			const ex = C3.PF - C3.PL, ey = C3.PB - C3.PT;
			const det = ex * dIn[1] - ey * dIn[0];
			const rx = pTop[0] - C3.PL, ry = pTop[1] - C3.PT;
			const s = (rx * dIn[1] - ry * dIn[0]) / det;
			const entry = fx(s);
			// refraction at the face (air outside, plate-like index inside, assumed)
			const tl = Math.hypot(ex, ey);
			const nIn: P2 = [-ey / tl, ex / tl]; // inward normal (into the prism, up-right)
			const nn: P2 = nIn[0] * dIn[0] + nIn[1] * dIn[1] > 0 ? nIn : [-nIn[0], -nIn[1]];
			const cosI = nn[0] * dIn[0] + nn[1] * dIn[1];
			const sinI = Math.sqrt(Math.max(0, 1 - cosI * cosI));
			const crs = nn[0] * dIn[1] - nn[1] * dIn[0];
			const sinO = Math.min(1, C3.NP * sinI);
			const aO = Math.atan2(nn[1], nn[0]) + Math.sign(crs || 1) * Math.asin(sinO);
			const dOut: P2 = [Math.cos(aO), Math.sin(aO)];
			const start: P2 = [entry[0] - dOut[0] * 150, entry[1] - dOut[1] * 150];
			// zero orders: transmitted into air (in-plane k conserved, n_s cos 52 deg) and reflected back into the plate
			const cosAir = Math.min(0.999, 1.457 * Math.cos(ang));
			const aAir = Math.acos(cosAir);
			return { start, entry, fb, top, dIn, tAir: [Math.cos(aAir), Math.sin(aAir)] as P2, refl: [Math.cos(ang), -Math.sin(ang)] as P2 };
		})();
		const filmTopC = (): P2[] => {
			const q: P2[] = [[C3.X0, C3.FT]];
			for (let k = 0; k < C3.GN; k++) {
				const a = C3.G0 + k * C3.GP;
				q.push([a, C3.FT], [a, C3.FT - C3.GD], [a + C3.GW, C3.FT - C3.GD], [a + C3.GW, C3.FT]);
			}
			q.push([C3.X1, C3.FT]);
			return q;
		};
		const drawC = (p: number, o: number) => {
			if (!show(gC, o)) return;
			const c = pal();
			cam = fit(BOX_C, regions().full);
			const q = cq('one_order', p);
			const lit = p >= CH.one_order[0] && p < CH.graded[0];
			paint(cSub, poly2([[C3.X0, C3.SB], [C3.X1, C3.SB], [C3.X1, C3.FB], [C3.X0, C3.FB]]), c.sub, c.subA, c.subEdge, 0.75, 1, 'sio2_plate');
			const pr: P2[] = [[C3.PL, C3.PT], [C3.PR, C3.PT], [C3.PR, C3.PB], [C3.PF, C3.PB]];
			paint(cPrism, poly2(pr), c.prism, c.prismA, c.subEdge, 0.8, 1, 'prism');
			paint(cPrismH, poly2(pr), c.prism, 0.35, 'none', 0);
			cPrismH.setAttribute('fill', `url(#${id}-hatch)`);
			// immersion liquid: thin lens between prism and plate
			const lens: P2[] = [];
			for (let k = 0; k <= 40; k++) {
				const t = (k / 40) * Math.PI * 2;
				lens.push([575 + 190 * Math.cos(t), (C3.SB + C3.PT) / 2 + 6 * Math.sin(t)]);
			}
			paint(cLiquid, poly2(lens), c.liquid, 0.55, c.liquid, 0.8, 1, 'prism');
			const ft = filmTopC();
			paint(cFilm, poly2([[C3.X0, C3.FB], [C3.X1, C3.FB], ...ft.slice().reverse()]), c.film, c.filmA, c.filmEdge, 0.85, 1, 'oo_film');
			paint(cGHit, poly2([[C3.G0 - 4, C3.FT - C3.GD - 4], [C3.G0 + C3.GN * C3.GP, C3.FT - C3.GD - 4], [C3.G0 + C3.GN * C3.GP, C3.FT + 8], [C3.G0 - 4, C3.FT + 8]]), on('grating_one_order') ? c.accent : '#000000', on('grating_one_order') ? 0.2 : 0.001, 'none', 0);
			// light
			const on1 = lit ? seg(q, 0.18, 0.22) * (1 - seg(cq('graded', p), 0, 0.1)) : p >= CH.graded[0] ? 1 - seg(cq('graded', p), 0, 0.1) : 0;
			const qq = p >= CH.graded[0] ? 1 : q;
			const tb = ease(seg(qq, 0.2, 0.45));
			const g = cGeo;
			// three straight pieces so the beam draws on in order
			const l1 = Math.hypot(g.entry[0] - g.start[0], g.entry[1] - g.start[1]);
			const l2 = Math.hypot(g.fb[0] - g.entry[0], g.fb[1] - g.entry[1]);
			const l3 = Math.hypot(g.top[0] - g.fb[0], g.top[1] - g.fb[1]);
			const lt = l1 + l2 + l3;
			const u = tb * lt;
			drawRay(cRays[0], S2(...g.start), S2(...g.entry), on1, 2.2, clamp01(u / l1), 'oo_beam', false);
			drawRay(cRays[1], S2(...g.entry), S2(...g.fb), on1, 2.2, clamp01((u - l1) / l2), 'oo_beam', false);
			drawRay(cRays[2], S2(...g.fb), S2(...g.top), on1 * 0.9, 2.2, clamp01((u - l1 - l2) / l3), 'oo_beam', false);
			// guided wave running back (to the left), built up under the grating
			const gf = ease(seg(qq, 0.42, 0.78));
			if (on1 * gf > 0.01) {
				const front = lerp(C3.G0 + C3.GN * C3.GP, C3.X0, gf);
				const y0 = C3.FB + 18, y1 = C3.FT - C3.GD - 8;
				const sx0 = S2(C3.X0, (y0 + y1) / 2), sx1 = S2(C3.X1, (y0 + y1) / 2);
				linC.g.setAttribute('x1', f1(sx0[0]));
				linC.g.setAttribute('y1', f1(sx0[1]));
				linC.g.setAttribute('x2', f1(sx1[0]));
				linC.g.setAttribute('y2', f1(sx1[1]));
				const g1 = C3.G0 + C3.GN * C3.GP;
				linC.stops.forEach((st, i) => {
					const X = lerp(C3.X0, C3.X1, i / (NG - 1));
					const pw = X > g1 ? 0 : X > C3.G0 ? (g1 - X) / (g1 - C3.G0) : 1;
					st.setAttribute('stop-color', c.beam);
					st.setAttribute('stop-opacity', (pw * clamp01((X - front) / 30)).toFixed(3));
				});
				const gp = poly2([[C3.X0, y0], [g1, y0], [g1, y1], [C3.X0, y1]]);
				for (const e of [cGlow.soft, cGlow.core]) {
					e.setAttribute('d', gp);
					e.setAttribute('fill', `url(#${id}-gC)`);
				}
				show(cGlow.soft, on1 * gf * c.glowA);
				show(cGlow.core, on1 * Math.min(1, gf * 2) * 0.8);
				const a0 = S2(500, (y0 + y1) / 2), a1 = S2(380, (y0 + y1) / 2);
				paint(cArrow.l, dOf([a0, a1], false), 'none', 0, theme === 'light' ? c.beam : c.core, 0.9, 1.4);
				paint(cArrow.hd, head(a1, a0, 7), theme === 'light' ? c.beam : c.core, 1, 'none', 0);
				show(cArrow.l, on1 * seg(gf, 0.5, 0.8));
				show(cArrow.hd, on1 * seg(gf, 0.5, 0.8));
			} else for (const e of [cGlow.soft, cGlow.core, cArrow.l, cArrow.hd]) show(e, 0);
			// faint zero orders (uncoupled light; brightness illustrative)
			const z = seg(qq, 0.5, 0.66);
			drawRay(cZero[0], S2(...g.top), S2(g.top[0] + g.tAir[0] * 120, g.top[1] + g.tAir[1] * 120), on1 * 0.3, 1, z, 'oo_zero');
			drawRay(cZero[1], S2(...g.top), S2(g.top[0] + g.refl[0] * 150, g.top[1] + g.refl[1] * 150), on1 * 0.3, 1, z, 'oo_zero');
		};

		// ---------------------------------------------------------------------------- view D: graded-depth grating
		const XD = (zum: number) => zum * D.KX;
		const YD = (nm: number) => nm * D.KY;
		const TOPD = YD(D.TF);
		const XG1 = XD(2000);
		/** film top with teeth: subarea i drawn at depth dep(i) (nm, 0 = flat); output-type teeth (long facet first) */
		const gradedTop = (dep: (i: number) => number): P2[] => {
			const q: P2[] = [[D.XL, TOPD], [0, TOPD]];
			const per = 80 / D.TPS;
			for (let i = 0; i < NSUB; i++) {
				const dd = YD(dep(i));
				for (let t = 0; t < D.TPS; t++) {
					const z0 = i * 80 + t * per;
					if (dd > 0.05) q.push([XD(z0 + 0.75 * per), TOPD - dd], [XD(z0 + per), TOPD]);
					else q.push([XD(z0 + per), TOPD]);
				}
			}
			q.push([D.XR, TOPD]);
			return q;
		};
		const drawD = (p: number, o: number) => {
			if (!show(gD, o)) return;
			const c = pal();
			cam = fit(BOX_D, regions().plot);
			const isNear = p >= CH.nearfield[0];
			// pens
			let nRev = 0;
			let calcX = -1;
			let markX: number | null = null;
			if (!isNear) {
				const pid = shown === 'leakage' ? 'leakage' : 'graded';
				const pens = penAt(spec, pid, p);
				if (pid === 'graded') {
					const pc = pens[0], pm = pens[1];
					calcX = pc ? pc.x : -1;
					nRev = pm ? pm.index + 1 : 0;
					markX = pm ? pm.x : pc ? pc.x : null;
				} else {
					nRev = NSUB;
					markX = pens[0] ? pens[0].x : null;
				}
			} else nRev = NSUB;
			const top = gradedTop((i) => (i < nRev ? subDepth(i) : 0));
			block(dSub, [[D.XL, -D.SUB], [D.XR, -D.SUB], [D.XR, 0], [D.XL, 0]], 0, D.XL, D.XR, -D.SUB, c.sub, c.subA, c.subA * 1.4, c.subEdge, 'substrate', 1, D.OX, D.OY);
			block(dFilm, [[D.XL, 0], [D.XR, 0], ...top.slice().reverse()], TOPD, D.XL, D.XR, 0, c.film, c.filmA, c.filmTopA, c.filmEdge, 'resist_film', 1, D.OX, D.OY, top);
			// subarea boundaries on the top face
			const tk: string[] = [];
			for (let i = 0; i <= NSUB; i++) tk.push(poly2([[XD(i * 80), TOPD], [XD(i * 80) + D.OX, TOPD + D.OY]], false));
			paint(dTicks, tk.join(''), 'none', 0, c.filmEdge, 0.55, 1);
			show(dTicks, 1);
			paint(dGHit, poly2([[0, TOPD - YD(240)], [XG1, TOPD - YD(240)], [XG1 + D.OX, TOPD + D.OY], [D.OX, TOPD + D.OY]]), on('graded_grating') ? c.accent : '#000000', on('graded_grating') ? 0.15 : 0.001, 'none', 0);
			// break mark on the waveguide coming from the input grating (20 mm away)
			const bx = D.XL + 50;
			paint(dBreak, [-5, 5].map((dx) => poly2([[bx + dx - 7, -14], [bx + dx + 7, TOPD + 14]], false)).join(''), 'none', 0, c.ink, 0.8, 1.3);
			show(dBreak, 1);
			// calculated depth (dashed, inside the film) up to the calculated pen
			if (!isNear && calcX > 0 && CALC.length) {
				const pts = CALC.filter((q) => q[0] <= calcX).map((q) => [XD(q[0]), TOPD - YD(q[1])] as P2);
				pts.push([XD(calcX), TOPD - YD(interp(CALC, calcX))]);
				const d = poly2(pts, false);
				paint(dCalc, d, 'none', 0, hl(c.ink, 'design_depth'), 0.85, 1.2);
				dCalcHit.setAttribute('d', d);
				show(dCalc, 1);
				show(dCalcHit, 1);
			} else {
				show(dCalc, 0);
				show(dCalcHit, 0);
			}
			// pen marker
			if (!isNear && markX !== null) {
				paint(dPen, poly2([[XD(markX), -10], [XD(markX), TOPD + 26]], false), 'none', 0, c.accent, 0.8, 1);
				show(dPen, 1 - seg(cq('graded', p), 0.92, 1));
			} else show(dPen, 0);
			// near field: guided light from the left, out-coupled light up to the Fig. 7 pen
			const nq = cq('nearfield', p);
			const lightOn = isNear ? seg(nq, 0, 0.12) * (1 - seg(cq('focus', p), 0, 0.1)) : 0;
			if (lightOn > 0.01) {
				const y0 = TOPD * 0.3, y1 = TOPD * 0.62;
				const sx0 = S2(D.XL, (y0 + y1) / 2), sx1 = S2(D.XR, (y0 + y1) / 2);
				linD.g.setAttribute('x1', f1(sx0[0]));
				linD.g.setAttribute('y1', f1(sx0[1]));
				linD.g.setAttribute('x2', f1(sx1[0]));
				linD.g.setAttribute('y2', f1(sx1[1]));
				linD.stops.forEach((st, i) => {
					const X = lerp(D.XL, D.XR, i / (NG - 1));
					const zmm = X / D.KX / 1000;
					const pw = zmm <= 0 ? 1 : 1 - 0.92 * (interp(cum, Math.min(2, zmm)) / cumTot);
					st.setAttribute('stop-color', c.beam);
					st.setAttribute('stop-opacity', (X > XG1 + 2 ? 0 : pw).toFixed(3));
				});
				const gp = poly2([[D.XL, y0], [XG1, y0], [XG1, y1], [D.XL, y1]]);
				for (const e of [dGlow.soft, dGlow.core]) {
					e.setAttribute('d', gp);
					e.setAttribute('fill', `url(#${id}-gD)`);
				}
				show(dGlow.soft, lightOn * c.glowA);
				show(dGlow.core, lightOn * 0.75);
				const pen = penAt(spec, 'nearfield', p)[0];
				const px = pen ? pen.x : p >= CH.focus[0] ? 2 : -1;
				vf0.setAttribute('stop-color', on('outcoupled_beam') ? mix(c.beam, c.accent, 0.4) : c.beam);
				vf1.setAttribute('stop-color', c.beam);
				const bw = XG1 / NEM;
				dEm.forEach((e, k) => {
					const xm = ((k + 0.5) / NEM) * 2;
					if (xm > px) return show(e, 0);
					const v = clamp01(interp(TRACE, xm));
					if (v < 0.01) return show(e, 0);
					const x0 = k * bw;
					e.setAttribute('d', poly2([[x0, TOPD + 2], [x0 + bw, TOPD + 2], [x0 + bw, TOPD + 2 + D.EH], [x0, TOPD + 2 + D.EH]]));
					show(e, lightOn * v * (theme === 'light' ? 0.85 : 1));
				});
			} else {
				for (const e of [dGlow.soft, dGlow.core]) show(e, 0);
				dEm.forEach((e) => show(e, 0));
			}
		};

		// ---------------------------------------------------------------------------- view E: focusing chip (iso)
		const ell = (() => {
			// Eq. (11): ellipses with one focus at the origin (the strip end), eccentricity e = n_c cos(phi_c) / n_eff
			const e = E.COS / E.NEFF;
			const line = (zv: number): P2[] => {
				const a = -zv / (1 + e), b = a * Math.sqrt(1 - e * e), zc = -a * e;
				const out: P2[] = [];
				for (let k = 0; k <= 24; k++) {
					const y = -E.HW + (2 * E.HW * k) / 24;
					out.push([zc - a * Math.sqrt(Math.max(0, 1 - (y * y) / (b * b))), y]);
				}
				return out;
			};
			// local (z, y) -> plan (X, Y): right grating focuses to X = +1 travelling -X; left grating mirrored
			const right = Array.from({ length: E.NL }, (_, j) => line(-E.F - j * E.DL).map(([z, y]) => [1 - z, y] as P2));
			const left = right.map((l) => l.map(([x, y]) => [-x, y] as P2));
			return { right, left };
		})();
		const drawE = (p: number, o: number) => {
			if (!show(gE, o)) return;
			const c = pal();
			const rg = regions();
			cam = p < CH.efficiency[0] ? fit(BOX_E, rg.full) : blend(fit(BOX_E, rg.full), fit(BOX_E, rg.plot), ease(seg(cq('efficiency', p), 0, 0.3)));
			const box3 = (el: { side: PathEl; top: PathEl; front: PathEl }, z0: number, z1: number, col: string, fa: number, ta: number, edge: string, pid: string) => {
				paint(el.side, dOf([S3(E.X0, E.Y0, z1), S3(E.X0, E.Y1, z1), S3(E.X0, E.Y1, z0), S3(E.X0, E.Y0, z0)]), mix(col, '#000000', 0.2), fa, edge, 0.6, 1, pid);
				paint(el.front, dOf([S3(E.X0, E.Y1, z1), S3(E.X1, E.Y1, z1), S3(E.X1, E.Y1, z0), S3(E.X0, E.Y1, z0)]), col, fa, edge, 0.6, 1, pid);
				paint(el.top, dOf([S3(E.X0, E.Y0, z1), S3(E.X1, E.Y0, z1), S3(E.X1, E.Y1, z1), S3(E.X0, E.Y1, z1)]), col, ta, edge, 0.6, 1, pid);
			};
			box3(eSub, E.ZS, 0, c.sub, c.subA * 1.2, c.subA, c.subEdge, 'substrate');
			box3(eFilm, 0, E.ZF, c.film, c.filmA, c.filmA * 0.8, c.filmEdge, 'resist_film');
			// dissolved bands (trench floors at the substrate) and the visible walls
			const Z = E.ZF;
			const tr = [[E.SW, E.SW + E.TW], [-E.SW - E.TW, -E.SW]];
			tr.forEach(([y0, y1], i) => {
				paint(eTrench[i], dOf([S3(-1, y0, 0), S3(1, y0, 0), S3(1, y1, 0), S3(-1, y1, 0)]), c.trench, 0.75, c.filmEdge, 0.6, 1, 'strip_waveguide');
				const wy = i === 0 ? E.SW : -E.SW - E.TW; // walls facing +Y
				paint(eWall[i], dOf([S3(-1, wy, Z), S3(1, wy, Z), S3(1, wy, 0), S3(-1, wy, 0)]), mix(c.film, '#000000', 0.3), 0.7, c.filmEdge, 0.6, 1, 'strip_waveguide');
			});
			paint(eStripTop, dOf([S3(-1, -E.SW, Z), S3(1, -E.SW, Z), S3(1, E.SW, Z), S3(-1, E.SW, Z)]), c.film, 0.55, c.filmEdge, 0.8, 1, 'strip_waveguide');
			// grating lines (thinned)
			const ld = [...ell.right, ...ell.left].map((l) => dOf(l.map(([x, y]) => S3(x, y, Z)), false)).join('');
			paint(eLines, ld, 'none', 0, hl(c.ink, 'focusing_gratings'), 0.9, 1.1);
			eLinesHit.setAttribute('d', ld);
			// light
			const fq = cq('focus', p);
			const lit = p >= CH.efficiency[0] ? 1 : p >= CH.focus[0] ? 1 : 0;
			const k = (a: number, b: number) => (p >= CH.efficiency[0] ? 1 : seg(fq, a, b));
			const inB = ease(k(0.22, 0.36)), conv = ease(k(0.34, 0.5)), strip = ease(k(0.48, 0.6)), dive = ease(k(0.58, 0.72)), outB = ease(k(0.7, 0.84));
			const on0 = lit * (p >= CH.efficiency[0] ? 1 : seg(fq, 0.2, 0.24));
			const Zl = Z + 0.01;
			const r0 = ell.right[0], rN = ell.right[E.NL - 1], l0 = ell.left[0], lN = ell.left[E.NL - 1];
			const fans: { poly: P2[]; t: number; a: number }[] = [
				{ poly: [...r0, ...rN.slice().reverse()], t: conv, a: 0.5 },
				{ poly: [[1, 0], ...r0], t: conv, a: 0.55 },
				{ poly: [[-1, 0], ...l0], t: dive, a: 0.42 },
				{ poly: [...l0, ...lN.slice().reverse()], t: dive, a: 0.3 }
			];
			fans.forEach((f, i) => {
				const el = eFan[i];
				if (on0 * f.t < 0.01) {
					show(el.soft, 0);
					show(el.core, 0);
					return;
				}
				const d = dOf(f.poly.map(([x, y]) => S3(x, y, Zl)));
				paint(el.soft, d, c.beam, 1, 'none', 0);
				paint(el.core, d, on('fan') ? mix(c.beam, c.accent, 0.4) : c.beam, 1, 'none', 0);
				show(el.soft, on0 * f.t * f.a * c.glowA * 0.6);
				show(el.core, on0 * f.t * f.a);
			});
			if (on0 * strip > 0.01) {
				const xe = lerp(1, -1, strip);
				const d = dOf([S3(1, 0, Zl), S3(xe, 0, Zl)], false);
				paint(eStrip.soft, d, 'none', 0, c.beam, 1, 6);
				paint(eStrip.core, d, 'none', 0, on('strip_light') ? c.accent : theme === 'light' ? c.beam : c.core, 1, 2);
				show(eStrip.soft, on0 * c.glowA);
				show(eStrip.core, on0);
			} else {
				show(eStrip.soft, 0);
				show(eStrip.core, 0);
			}
			const xg = 5 + ((E.NL - 1) * E.DL) / 2;
			drawRay(eIn, S3(9.6, 0, 5.4), S3(xg, 0, Zl), on0, 2.4, inB, 'beam_in_iso');
			drawRay(eOut, S3(-xg, 0, Zl), S3(-9.6, 0, 5.4), on0 * 0.6, 1.3, outB, 'out_beam');
		};

		// ---------------------------------------------------------------------------- frame
		const viewAlpha = (p: number): [number, number, number, number, number] => {
			let a = 0, b = 0, cc = 0, d = 0, e = 0;
			if (p < CH.write[0]) a = 1;
			else if (inCh('write', p)) {
				const t = seg(cq('write', p), 0.14, 0.3);
				a = 1 - t;
				b = t;
			} else if (inCh('develop', p)) b = 1;
			else if (inCh('couple', p)) {
				const t = seg(cq('couple', p), 0.04, 0.2);
				a = t;
				b = 1 - t;
			} else if (inCh('replica', p)) a = 1;
			else if (inCh('one_order', p)) {
				const t = seg(cq('one_order', p), 0.04, 0.18);
				a = 1 - t;
				cc = t;
			} else if (inCh('graded', p)) {
				const t = seg(cq('graded', p), 0.02, 0.14);
				cc = 1 - t;
				d = t;
			} else if (inCh('nearfield', p)) d = 1;
			else if (inCh('focus', p)) {
				const t = seg(cq('focus', p), 0.04, 0.18);
				d = 1 - t;
				e = t;
			} else e = 1;
			return [a, b, cc, d, e];
		};
		const frame = (p: number) => {
			lastP = p;
			const c = pal();
			hatchLine.setAttribute('stroke', c.hatch);
			hatchLine.setAttribute('stroke-opacity', '0.55');
			const [a, b, cc, d, e] = viewAlpha(p);
			drawA(p, a);
			drawB(p, b);
			drawC(p, cc);
			drawD(p, d);
			drawE(p, e);
		};

		// ---------------------------------------------------------------------------- anchors
		const anchor = (pid: string): [number, number] | null => {
			const p = lastP;
			const save = cam;
			let out: [number, number] | null = null;
			if (pid === 'grating_in' && inCh('develop', p) && cq('develop', p) >= 0.74) {
				cam = fit(BOX_B, regions().full);
				out = S2(2 * B.PER + 60, B.TF + 170);
			} else if (pid === 'waveguide' && inCh('couple', p) && cq('couple', p) >= 0.24) {
				const R = regions().full;
				cam = blend(fit(BOX_A_ZOOM, R), fit(BOX_A_LIGHT, R), ease(seg(cq('couple', p), 0, 0.22)));
				out = w < 700 ? S2(A.BRK - 140, -A.SD - 10) : S2(A.BRK + 30, A.T + 70);
			} else if (pid === 'strip_waveguide' && inCh('focus', p) && cq('focus', p) >= 0.22) {
				cam = fit(BOX_E, regions().full);
				const q = projRaw(0, E.SW + E.TW + 0.6, E.ZF);
				out = S2(q[0], q[1]);
			}
			cam = save;
			return out;
		};

		// ---------------------------------------------------------------------------- picking
		const INFO: Record<string, PickInfo> = {
			brk: {
				id: 'brk',
				label: 'Length compressed',
				detail: 'The 20 mm waveguide between the gratings is drawn much shorter (break mark); film thickness enlarged.'
			},
			brk_d: {
				id: 'brk_d',
				label: 'Waveguide from the input grating',
				detail: 'Light was coupled in by a constant-depth grating 20 mm away (Waldhäusl et al., Appl. Opt. 1997, p.9387 col. 1); length compressed.'
			},
			dose_tint: {
				id: 'dose_tint',
				label: 'Exposed resist',
				detail: [
					'Tint ∝ the dose of each shot (latent image). The dose rises stepwise across each 800 nm period and the pattern repeats (p.9383 col. 2 - p.9384 col. 1).',
					'Five steps per period, the dose values and the writing order (right to left here) are schematic: not given.'
				]
			},
			oo_film: {
				id: 'oo_film',
				label: 'Waveguide film',
				detail: [
					'The film of the single-order experiment is not stated (Waldhäusl et al., Appl. Opt. 1997, p.9385 col. 2); drawn as Fig. 3 draws it.',
					'Thicknesses not to scale: the SiO_{2} plate is about 2 mm thick.'
				]
			},
			oo_beam: {
				id: 'oo_beam',
				label: 'Incoming beam, through prism and plate',
				detail: [
					'Angle in the plate as Fig. 3 draws it (about 52° from the surface, schematic).',
					'Fig. 3 draws the beam entering the prism at a shallow angle (about 19°) and bending twice; drawn here as one straight, index-matched path through prism, liquid and plate (assumed), refracted at the prism face for an assumed prism index near the plate’s.',
					'Derived for this story with the Table 1 film (assumed): the single substrate order runs at about 136.5° from the guided direction, i.e. backward (Eq. (1)).'
				]
			},
			oo_guided: {
				id: 'oo_guided',
				label: 'Guided wave, running back',
				detail: [
					'Fed from the substrate side, the grating couples the light into a wave travelling against the beam’s in-plane direction, as Fig. 3 draws it (arrow to the left).',
					'Maximum input efficiency 67 % (Waldhäusl et al., Appl. Opt. 1997, p.9385 col. 2). Build-up under the grating drawn schematically.'
				]
			},
			oo_zero: {
				id: 'oo_zero',
				label: 'Uncoupled light',
				detail: [
					'Light not coupled in leaves as the transmitted and reflected zero order; no higher orders exist for Λ = 250 nm (p.9385 col. 2).',
					'Brightness illustrative; directions from refraction at the drawn angle (derived).'
				]
			},
			design_depth: {
				id: 'design_depth',
				label: 'Calculated depth (Fig. 5)',
				detail: 'Dashed: the calculated corrugation depth at the plot pen, drawn on the same vertical scale as the teeth (Waldhäusl et al., Appl. Opt. 1997, Fig. 5, p.9386).'
			},
			nf_guided: {
				id: 'nf_guided',
				label: 'Guided light',
				detail: [
					'Enters the variable-depth grating at its start (left), from a constant-depth input grating 20 mm away (p.9387 col. 1).',
					'Drawn fading as the out-coupled light accumulates (shape from the Fig. 7 trace); the power left at the grating end is not stated (illustrative).'
				]
			},
			fan: {
				id: 'fan',
				label: 'Focused guided light',
				detail: [
					'Converges from the first grating to the strip start over f = 4 mm, diverges from the strip end to the second grating (Fig. 8, 9; p.9388-9389).',
					'Input efficiency into the strip 42 % (Table 5, p.9389). Brightness illustrative.'
				]
			},
			strip_light: {
				id: 'strip_light',
				label: 'Light in the strip',
				detail: 'Carried along the 2 mm strip; throughput of the whole chip 5 % without and 10 % with the aberration correction (Table 5, p.9389).'
			},
			out_beam: {
				id: 'out_beam',
				label: 'Output beam',
				detail: [
					'Recollimated by the second focusing grating; 10 % of the input beam with the correction, 5 % without (Fig. 9; Table 5, p.9389).',
					'Direction as Fig. 9 draws it (schematic). Fig. 9 also draws further out-coupled orders as thin dashed arrows; they are not drawn here.'
				]
			}
		};
		const partInfo = (pid: string): string | PickInfo => {
			const p = lastP;
			const side = p < CH.write[1] || (p >= CH.couple[0] && p < CH.one_order[1]);
			const close = p >= CH.write[0] && p < CH.couple[1] && !side;
			const iso = p >= CH.focus[0];
			const graded = p >= CH.graded[0] && p < CH.focus[1] && !iso;
			const rep = (inCh('replica', p) && cq('replica', p) >= 0.7) || (inCh('one_order', p) && cq('one_order', p) < 0.2);
			const D1 = (lines: string | string[]): PickInfo => ({ id: pid, label: '', detail: lines });
			switch (pid) {
				case 'substrate':
					if (close) return D1('True scale (nm); only the top of the plate is shown.');
					if (iso) return D1('Chip size not stated: plain stand-in.');
					return D1('Plain stand-in: plate size and thickness not stated; drawn thickness schematic.');
				case 'resist_film':
					if (close) return D1('True scale: 800 nm film (Table 1, p.9385).');
					if (graded) return D1('Vertical scale true to the plotted depths (800 nm film); length along the grating compressed far more.');
					if (iso) return D1('Film thickness and chip size schematic.');
					return D1('Thickness drawn enlarged (schematic).');
				case 'grating_in':
					if (close)
						return D1([
							'True scale: period 800 nm, depth 250 nm; the about 200 nm "second inclination" read as the steep side (interpretation).',
							'Zero offset of about 80 nm reported for the paper’s e-beam gratings (Fig. 6, Sec. 4-5); drawn here under the Table 1 grating with t_{g} taken as peak-to-valley (assumed).',
							'Straight facets: the paper prints no profile image; orientation as Fig. 1 (steep side at the outer edge of each period).'
						]);
					return D1('Five teeth drawn (as Fig. 1); the 1 mm grating has about 1250 periods.');
				case 'grating_out':
					return D1('Mirror image of the input grating, as Fig. 1 draws it; five teeth drawn.');
				case 'waveguide':
					return D1('Drawn much shorter (break mark) and thicker than to scale.');
				case 'metal_layer':
					return D1(close ? 'Drawn as a line: thickness not stated; it is gone before development (removal not described).' : 'Thickness not stated; drawn schematic.');
				case 'ebeam':
					return D1('Variable-shaped beam: each shot exposes a rectangle. Five shots per period and their order are schematic.');
				case 'beam_in':
					return D1([
						'Drawn at the angle Fig. 2 draws (schematic).',
						rep
							? 'Derived for this story for the all-polymer replica (PαMS film 450 nm, n_{f} 1.603, on PMMA n_{s} 1.489): n_{eff} ≈ 1.542, first-order coupling angle about 41° from the surface (Eq. (1)); not printed. The master-chip value (about 47°) does not apply here.'
							: 'Derived for this story for the e-beam master chip: about 47° from the surface (Eq. (1), m = 1, λ = 633 nm, Λ = 800 nm, n_{eff} ≈ 1.475 from a slab-mode calculation with the Table 1 values); not printed.'
					]);
				case 'beam_in_iso':
					return { id: 'beam_in', label: '', detail: ['Direction as Fig. 9 draws it (schematic).', 'Coupling angle not printed; about 47° from the surface derived for the Table 1 chip.'] };
				case 'orders_in':
					return D1(['Directions as Fig. 2 draws them (schematic); brightness illustrative: their powers are not given.']);
				case 'orders_out':
					return D1([
						rep
							? 'Directions as Fig. 2 draws them (schematic). Derived for this story for the replica (n_{eff} ≈ 1.542): about 41°, 92°, 146° in air and 60°, 92°, 124° in PMMA from the propagation direction; the master-chip values do not apply.'
							: 'Directions as Fig. 2 draws them (schematic). Derived for this story for the e-beam master chip (Table 1 values): about 47°, 96°, 154° in air and 62°, 94°, 128° in quartz from the propagation direction.',
						rep
							? 'Cover side drawn brighter: about 74 % of the out-coupled light (text p.9385 col. 2; Table 3 prints "74/36"). Split among the orders not given: drawn equal.'
							: 'Cover side drawn brighter: about 65 % of the out-coupled light (Table 2, p.9385). Split among the orders not given: drawn equal.'
					]);
				case 'guided_mode':
					return D1(
						rep
							? 'Glow drawn with the replica values: 1.2 dB/cm over the 20 mm (Table 3) and exp(−2αz) with α = 0.75 mm^{-1} under the output grating (p.9385); build-up across the input grating schematic.'
							: 'Glow drawn with 0.6 dB/cm over the 20 mm (Table 2) and exp(−2αz) with the measured α = 1.48 mm^{-1} under the 1 mm output grating (Eq. (2), p.9384-9385); build-up across the input grating schematic.'
					);
				case 'nickel_master':
					return D1('Layer thicknesses not to scale (about 300 µm nickel, about 3 mm copper); hatched as Fig. 1.');
				case 'pmma_plate':
					return D1('Plain stand-in (lateral size not stated); about 2 mm thick, drawn thinner. Tint while heated to 150 °C.');
				case 'pams_film':
					return D1('450 nm film drawn enlarged, flat top over the embossed grating as Fig. 1.');
				case 'graded_grating':
					return D1([
						'Two teeth drawn per 80 µm subarea (the real period is 800 nm). Each subarea takes its Fig. 5 measured depth, on a vertical scale true to the plotted values.',
						'Tooth orientation as the output grating of Fig. 1 (not stated for this grating); the about 80 nm zero offset is not drawn here.'
					]);
				case 'outcoupled_beam':
					return D1([
						'Brightness along the grating = the Fig. 7 trace at the plot pen; x mapped onto the 2 mm grating as in the plot note.',
						'Drawn straight up (near-field brightness only); the first order leaves obliquely (Fig. 2).'
					]);
				case 'focusing_gratings':
					return D1([
						'Line shape: Eq. (11) ellipses with one focus at the strip end, using the derived n_{eff} ≈ 1.475 and φ_{c} ≈ 47°.',
						'Every n-th line only (the real lines are 800 nm apart); width drawn larger than the derived about 0.79 mm.'
					]);
				case 'strip_waveguide':
					return D1('Width and the 20 µm dissolved bands drawn enlarged; lengths along the light in true ratio (4 mm focal length, 2 mm strip, 4 mm).');
				case 'sio2_plate':
					return D1('About 2 mm thick, drawn as Fig. 3 draws it (not to scale).');
				case 'prism':
					return D1('Outline and the liquid layer as Fig. 3 draws them; prism material, angle and liquid not named.');
				case 'grating_one_order':
					return D1('Rectangular profile drawn as Fig. 3 draws it (period 250 nm, depth 150 nm; not to scale).');
			}
			return pid;
		};

		return {
			frame,
			highlight(ids) {
				hi = [...ids];
				if (ids.includes('beam_in')) hi.push('beam_in_iso');
			},
			pick(x, y) {
				const r = svg.getBoundingClientRect();
				const els = document.elementsFromPoint(r.left + x, r.top + y);
				for (const e of els) {
					if (!root.contains(e)) continue;
					const pid = (e as Element).getAttribute('data-pick');
					if (!pid) continue;
					if (INFO[pid]) return INFO[pid];
					const info = partInfo(pid);
					if (typeof info === 'string') return info;
					return { id: info.id, label: spec.parts.find((q) => q.id === info.id)?.name ?? info.id, detail: info.detail };
				}
				return null;
			},
			anchor,
			plot(pid) {
				shown = pid;
			},
			resize(nw, nh) {
				w = Math.max(1, nw);
				h = Math.max(1, nh);
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
