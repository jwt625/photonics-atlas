// Scene module: temporal solitons in a crystalline MgF2 microresonator (Herr et al., Nature Photonics 2014; every value
// and locator from the arXiv v3 preprint). Spec: data/history/showcases/herr2014.yaml. Contract: ../showcase/types.ts.
// Renderer 2.5D (SVG, axonometric).
//
// World units are the PDF points of the paper's Fig. 2d block diagram (X right, Y down the page = toward the viewer,
// Z up). Fig. 2d is a block diagram: boxes, fiber runs and branches keep its layout, nothing carries a scale. The
// resonator is a plain disc stand-in at the diagram's resonator position (diameter drawn, not to scale with the boxes;
// the 2 mm figure is derived from the FSR and lives in the dims table). The crystal is a plain post under it (tiers and
// fabrication not drawn). Coupling by the tapered fiber passing the back of the disc (Fig. 2d; Methods p.5).
//
// Transmission chapter (Fig. 2a): the scan position = the plot pen (runtime penAt, the reveal the plot draws). Output
// fiber brightness = the digitized transmission at the pen; ring brightness = the local mean transmission (lower
// transmission = more light inside, p.3). Ring waveform by scan time (illustrative, labelled in hover): cw build-up;
// from marker I (1.50 ms) a periodic un-pulsed waveform (Fig. 1c left inset); from about 1.55 ms, where the broad
// noisy beat note of Fig. 2c starts, a noisy one; at the first step (3.12 ms) 5 pulses, then 4, 3, 2 at the next
// steps (3.55, 3.65, 3.76 ms), and none after the last step (3.86 ms: flat plateau with no small thermal triangle,
// narrow beat note ends, Fig. 2a / 2c). Counts are illustrative (the paper gives none per step). Later chapters show
// one soliton (Fig. 4a one-soliton state); the 2 / 5 soliton alternates show 2 / 5 (handle.plot).
import { clamp01, ease, easeOut, lerp, seg } from '../showcase/progress';
import { penAt } from '../showcase/plot';
import type { PickInfo, ShowcaseContext, ShowcaseHandle, ShowcaseModule, Theme } from '../showcase/types';

type P2 = [number, number];
type P3 = [number, number, number];
type Rect = [number, number, number, number];
type Geo = Record<string, unknown>;

const NS = 'http://www.w3.org/2000/svg';
const DEG = Math.PI / 180;
const TAU = Math.PI * 2;
const num = (v: unknown, d: number): number => (typeof v === 'number' && Number.isFinite(v) ? v : d);
const rect4 = (v: unknown, d: Rect): Rect => (Array.isArray(v) && v.length === 4 && v.every((x) => typeof x === 'number') ? (v as Rect) : d);
const smooth = (a: number, b: number, x: number) => {
	const t = clamp01((x - a) / (b - a));
	return t * t * (3 - 2 * t);
};
const wrap = (a: number) => ((a % TAU) + TAU) % TAU;
let uid = 0;

// ------------------------------------------------------------------------------------------------ colours
interface Pal {
	light: string;
	lightCore: string;
	glowA: number;
	disc: string;
	discEdge: string;
	discA: [number, number, number];
	post: string;
	postA: number;
	fiber: string;
	fiberCore: string;
	ink: string;
	inkSoft: string;
	screen: string;
	glyph: string;
	boxA: [number, number, number];
	accent: string;
}
const PAL: Record<Theme, Pal> = {
	dark: {
		light: '#ff5a3c', lightCore: '#ffc2a8', glowA: 0.85, disc: '#e4eaf0', discEdge: '#c9d2dc', discA: [0.26, 0.2, 0.07],
		post: '#d9dee4', postA: 0.1, fiber: '#4fa8c8', fiberCore: '#9fd4e8', ink: '#c3c2b7', inkSoft: '#898781', screen: '#26262a',
		glyph: '#e8c860', boxA: [0.16, 0.1, 0.07], accent: '#3987e5'
	},
	light: {
		light: '#e0401f', lightCore: '#b02a10', glowA: 0.5, disc: '#8796a6', discEdge: '#5d6b7a', discA: [0.3, 0.22, 0.1],
		post: '#8a96a3', postA: 0.16, fiber: '#2f87a6', fiberCore: '#1d5f78', ink: '#52514e', inkSoft: '#6f6d68', screen: '#3a3a3e',
		glyph: '#e0b840', boxA: [0.34, 0.24, 0.18], accent: '#2a78d6'
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
	return out.filter((q, i) => i === 0 || Math.hypot(q[0] - out[i - 1][0], q[1] - out[i - 1][1]) > 0.01);
}

/** plan polyline with cumulative arclength */
interface Route {
	pts: P2[];
	cum: number[];
	len: number;
}
function mkRoute(pts: P2[]): Route {
	const cum = [0];
	for (let i = 1; i < pts.length; i++) cum.push(cum[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
	return { pts, cum, len: cum[cum.length - 1] };
}
function routeAt(r: Route, s: number): P2 {
	const x = Math.max(0, Math.min(r.len, s));
	let i = 1;
	while (i < r.cum.length - 1 && r.cum[i] < x) i++;
	const a = r.pts[i - 1], b = r.pts[i];
	const l = r.cum[i] - r.cum[i - 1] || 1;
	const t = (x - r.cum[i - 1]) / l;
	return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];
}
function subRoute(r: Route, s0: number, s1: number): P2[] {
	const a = Math.max(0, s0), b = Math.min(r.len, s1);
	if (b <= a) return [];
	const out: P2[] = [routeAt(r, a)];
	for (let i = 1; i < r.pts.length - 1; i++) if (r.cum[i] > a && r.cum[i] < b) out.push(r.pts[i]);
	out.push(routeAt(r, b));
	return out;
}
/** arclength where the route first reaches plan Y >= y (route length when never) */
function sAtY(r: Route, y: number): number {
	for (let i = 1; i < r.pts.length; i++) {
		const a = r.pts[i - 1], b = r.pts[i];
		if (b[1] >= y && a[1] < y) return r.cum[i - 1] + ((y - a[1]) / (b[1] - a[1])) * (r.cum[i] - r.cum[i - 1]);
	}
	return r.len;
}

// ------------------------------------------------------------------------------------------------ camera
interface Shot {
	az: number;
	el: number;
	/** world box to fit: x0, y0, x1, y1, z0, z1 */
	box: [number, number, number, number, number, number];
	region: 'full' | 'plot';
	zoom: number;
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

const mod: ShowcaseModule = {
	renderer: '2.5d',
	build(ctx: ShowcaseContext): ShowcaseHandle {
		if (ctx.kind !== '2.5d') throw new Error('herr2014 is a 2.5D scene');
		const { svg, spec } = ctx;
		const id = `sol${++uid}`;
		let w = Math.max(1, ctx.width);
		let h = Math.max(1, ctx.height);
		let theme: Theme = ctx.theme;
		let hi: string[] = [];

		// ---------------------------------------------------------------------------- chapters
		const fallback: Record<string, [number, number]> = {
			crystal: [0, 0.08], resonator: [0.08, 0.17], taper: [0.17, 0.25], setup: [0.25, 0.34], transmission: [0.34, 0.6],
			soliton: [0.6, 0.69], spectrum: [0.69, 0.84], pulse: [0.84, 1]
		};
		const C: Record<string, [number, number]> = {};
		for (const [cid, r] of Object.entries(fallback)) C[cid] = (spec.chapters.find((c) => c.id === cid)?.p ?? r) as [number, number];
		const cq = (cid: string, p: number) => seg(p, C[cid][0], C[cid][1]);

		// ---------------------------------------------------------------------------- Fig. 2d layout (PDF pt)
		const geo = (pid: string): Geo => (spec.parts.find((q) => q.id === pid)?.geometry ?? {}) as Geo;
		const PUMP = rect4(geo('pump').rect, [384.2, 292.5, 430.9, 320.2]);
		const SCAN = rect4(geo('scan').rect, [392.8, 322.6, 430.9, 335.4]);
		const FPC = rect4(geo('fpc').rect, [433.3, 298.4, 456.2, 305.4]);
		const OSA = rect4(geo('osa').rect, [384.2, 347.2, 430.9, 366.9]);
		const PDT = rect4(geo('pd_trans').rect, [456.8, 372.3, 462.6, 379.7]);
		const SCOPE = rect4(geo('scope').rect, [384.2, 369.1, 430.9, 391.4]);
		const PDB = rect4(geo('pd_beat').rect, [456.8, 399.9, 462.6, 407.4]);
		const LO = rect4(geo('lo').rect, [440.8, 400.5, 447.2, 406.9]);
		const ESA = rect4(geo('esa').rect, [384.2, 394.2, 430.8, 413.8]);
		const tg = geo('taper');
		const FY = num(tg.fiber_y, 306.5);
		const WAIST: P2 = Array.isArray(tg.waist_x) && tg.waist_x.length === 2 ? [num(tg.waist_x[0], 460.1), num(tg.waist_x[1], 483.0)] : [460.1, 483.0];
		const XD = 486.0; // output fiber down (Fig. 2d)
		const YOSA = 357.5, YPD = 376.0, YFBG = 403.7; // branch rows (Fig. 2d)
		const FBGX: P2 = [483.1, 462.6];
		// resonator stand-in: plain disc under the fiber's thin section (diagram position), drawn size
		const R = 10.5; // drawn radius (diagram units, not to scale)
		const GAP = 1.0; // drawn evanescent gap (not stated)
		const CX = (WAIST[0] + WAIST[1]) / 2;
		const CY = FY + GAP + R;
		const TD = 3.2; // disc thickness, drawn
		const RR = R - 0.7; // ring of light just inside the rim, drawn
		const HB = 5; // box height, drawn
		const ZF = 2.5; // fiber height = disc mid-plane
		const HP = 9; // crystal post height, drawn
		const RP = 0.6 * R; // post radius, drawn
		const PHI_T = -Math.PI / 2; // tangent point at the back of the disc (plan angle from +X toward +Y)

		// fiber routes (plan): bus = pump -> taper -> down -> FBG -> PD; branches to the OSA and the transmission PD
		const BUS = mkRoute(roundLine([[PUMP[2], FY], [XD, FY], [XD, YFBG], [PDB[2], YFBG]], 2.5));
		const OSAB = mkRoute(roundLine([[XD, YOSA - 5], [XD, YOSA], [OSA[2], YOSA]], 4));
		const PDTB = mkRoute(roundLine([[XD, YPD - 5], [XD, YPD], [PDT[2], YPD]], 4));
		const OUTA = mkRoute(roundLine([[CX, FY], [XD, FY], [XD, YFBG], [PDB[2], YFBG]], 2.5));
		const OUTO = mkRoute(roundLine([[CX, FY], [XD, FY], [XD, YOSA], [OSA[2], YOSA]], 2.5));
		const sT = CX - PUMP[2]; // bus arclength at the tangent point
		const sW0 = WAIST[0] - PUMP[2], sW1 = WAIST[1] - PUMP[2];
		const sJO = sAtY(BUS, YOSA - 5), sJP = sAtY(BUS, YPD - 5);
		const sFBG = (() => {
			// bus arclength where the FBG starts (on the bottom row, x = 483.1)
			const r = BUS;
			for (let i = 1; i < r.pts.length; i++) if (r.pts[i][1] >= YFBG - 0.01 && r.pts[i][0] <= FBGX[0]) return r.cum[i];
			return r.len;
		})();
		const Y_TAPER = CY + R + 14; // output fiber drawn down to here before the setup chapter (frame bottom)
		const wProf = (s: number) => 1 - 0.62 * smooth(sW0, sW0 + 4.4, s) * (1 - smooth(sW1 - 4.4, sW1, s));

		// ---------------------------------------------------------------------------- the scan: plot pen (Fig. 2a)
		const tRange = (() => {
			const c = spec.chapters.find((c) => c.plot === 'transmission') ?? spec.chapters.find((c) => c.id === 'transmission');
			return (c?.p ?? C.transmission) as [number, number];
		})();
		/** pen of a plot's first series at story progress p (runtime penAt: the same reveal the plot draws) */
		const penOf = (plotId: string) => {
			const pl = spec.plots?.find((q) => q.id === plotId);
			const pts: P2[] = ((pl?.series?.[0]?.points ?? []) as P2[]).filter((q) => Number.isFinite(q[0]) && Number.isFinite(q[1]));
			return {
				pts,
				at(p: number): { t: number; y: number } {
					if (pts.length < 2) return { t: 0, y: 1 };
					const pe = penAt(spec, plotId, p)[0];
					return pe ? { t: pe.x, y: pe.y } : { t: pts[0][0], y: pts[0][1] };
				}
			};
		};
		const PEN = { main: penOf('transmission'), zoom: penOf('transmission_steps'), sim: penOf('transmission_sim') };
		const tPts = PEN.main.pts;
		/** scan time (ms) and digitized transmission at the plot pen of the measured scan on screen (full or zoom) */
		const penScan = (p: number, zoom: boolean) => (zoom && PEN.zoom.pts.length > 1 ? PEN.zoom : PEN.main).at(p);
		// local mean transmission per 0.01 ms (for the ring brightness; the noise band averages out)
		const TB = 0.01;
		const tMax = tPts.length ? tPts[tPts.length - 1][0] : 4;
		const nB = Math.max(1, Math.ceil(tMax / TB) + 1);
		const sum = new Float64Array(nB), cnt = new Float64Array(nB);
		for (const [x, y] of tPts) {
			const i = Math.min(nB - 1, Math.max(0, Math.floor(x / TB)));
			sum[i] += y;
			cnt[i]++;
		}
		const tMean = new Float64Array(nB);
		let lastV = tPts[0]?.[1] ?? 1;
		for (let i = 0; i < nB; i++) {
			if (cnt[i]) lastV = sum[i] / cnt[i];
			tMean[i] = lastV;
		}
		const tOff = tMean[0];
		let tLow = tOff;
		for (let i = 0; i < nB; i++) tLow = Math.min(tLow, tMean[i]);
		const meanAt = (t: number) => tMean[Math.min(nB - 1, Math.max(0, Math.floor(t / TB)))];
		const inside = (t: number) => clamp01((tOff - meanAt(t)) / Math.max(1e-3, tOff - tLow));
		// scan events (ms): Fig. 2b markers and the steps (Fig. 2a, report readings)
		// T_NOISE: the broad, noisy beat note of Fig. 2c starts near 1.55 ms (between markers I and II)
		const T_I = 1.5, T_NOISE = 1.55, T_STEP = 3.12;
		const T_STEPS = [3.547, 3.647, 3.756, 3.855];
		const T_LAST = T_STEPS[T_STEPS.length - 1];
		// pulses after the first step (illustrative): 5, then 4, 3, 2, and none after the last step (no small thermal
		// triangle, narrow beat note ends, transmission back near its off-resonance level: Fig. 2a, 2c)
		const N0 = T_STEPS.length + 1;
		const nPulsesAt = (t: number) => (t < T_STEP || t >= T_LAST ? 0 : N0 - T_STEPS.filter((s) => t >= s).length);
		// p at which the pen first reaches scan time t (for the birth / end of a drawn pulse)
		const pOfT = (t: number, zoom: boolean): number => {
			let a = tRange[0], b = tRange[1];
			if (penScan(b, zoom).t < t) return Infinity;
			if (penScan(a, zoom).t >= t) return -Infinity;
			for (let i = 0; i < 40; i++) {
				const m = (a + b) / 2;
				if (penScan(m, zoom).t >= t) b = m;
				else a = m;
			}
			return b;
		};

		// ---------------------------------------------------------------------------- seeded illustrative pattern
		let seed = 2014;
		const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
		const pulseAng: number[] = [];
		while (pulseAng.length < N0) {
			const a = rnd() * TAU;
			if (pulseAng.every((b) => Math.abs(((a - b + 3 * Math.PI) % TAU) - Math.PI) > 32 * DEG)) pulseAng.push(a);
		}
		// drop order: the pulse with index dropIdx[k] leaves at step k (seeded)
		const order = pulseAng.map((_, i) => i);
		for (let i = order.length - 1; i > 0; i--) {
			const j = Math.floor(rnd() * (i + 1));
			[order[i], order[j]] = [order[j], order[i]];
		}
		const deathT = new Array<number>(N0).fill(T_LAST);
		T_STEPS.slice(0, -1).forEach((ts, k) => (deathT[order[k]] = ts));
		const lives = [false, true].map((zoom) => ({
			birth: pOfT(T_STEP, zoom),
			death: deathT.map((t) => (Number.isFinite(t) ? pOfT(t, zoom) : Infinity))
		}));
		const noise = Array.from({ length: 7 }, () => ({ n: 2 + Math.floor(rnd() * 13), ph: rnd() * TAU, nu: (0.6 + rnd()) * 900, a: 0.4 + rnd() * 0.6 }));
		const NL = 16; // lobes of the periodic waveform (illustrative)
		const OM = TAU * 40; // drawn circulation: turns per unit p (roundtrip time not to scale)
		const SOL0 = 0.3; // single-soliton start angle
		// two / five soliton states (Fig. 4a alternates): positions illustrative (spacing not stated)
		const multi: Record<number, number[]> = { 1: [SOL0] };
		for (const n of [2, 5]) {
			const a: number[] = [SOL0];
			while (a.length < n) {
				const v = rnd() * TAU;
				if (a.every((b) => Math.abs(((v - b + 3 * Math.PI) % TAU) - Math.PI) > 40 * DEG)) a.push(v);
			}
			multi[n] = a;
		}
		/** plot on screen (runtime hook handle.plot); frame(p) reads it */
		let plotId: string | null = null;

		// ---------------------------------------------------------------------------- SVG scaffolding
		const mk = <K extends keyof SVGElementTagNameMap>(tag: K, parent: Element, attrs: Record<string, string | number> = {}): SVGElementTagNameMap[K] => {
			const e = document.createElementNS(NS, tag) as SVGElementTagNameMap[K];
			for (const [a, v] of Object.entries(attrs)) e.setAttribute(a, String(v));
			parent.appendChild(e);
			return e;
		};
		const root = mk('g', svg, { 'data-scene': 'herr2014' });
		const defs = mk('defs', root);
		const blur = mk('filter', defs, { id: `${id}-glow`, filterUnits: 'userSpaceOnUse', 'color-interpolation-filters': 'sRGB' });
		const blurStd = mk('feGaussianBlur', blur, { stdDeviation: 3 });
		type PathEl = SVGPathElement;
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
		interface Box {
			g: SVGGElement;
			top: PathEl;
			front: PathEl;
			side: PathEl;
			glyph: PathEl;
			screen: PathEl;
			dot: PathEl;
		}
		const mkBox = (parent: Element, part: string): Box => {
			const g = mk('g', parent);
			return {
				g, front: path(g, part), side: path(g, part), top: path(g, part), screen: path(g, part), glyph: path(g, part, { fill: 'none' }),
				dot: path(g, part)
			};
		};
		// layers (back to front)
		const gElec = mk('g', root, { 'pointer-events': 'stroke' });
		const elec = Array.from({ length: 6 }, () => path(gElec, null, { fill: 'none' }));
		const gBoxes = mk('g', root);
		const boxes: Record<string, Box> = {};
		for (const pid of ['esa', 'scope', 'osa', 'scan', 'pump', 'lo', 'pd_beat', 'pd_trans']) boxes[pid] = mkBox(gBoxes, pid);
		const gFiber = mk('g', root);
		const tubeN = 1;
		const mkTube = (parent: Element, part: string | null) => Array.from({ length: tubeN }, () => path(parent, part));
		const busTube = mkTube(gFiber, 'taper');
		const brTube = [path(gFiber, 'taper', { fill: 'none' }), path(gFiber, 'taper', { fill: 'none' })];
		const fbgTicks = path(gFiber, 'fbg', { fill: 'none' });
		const fbgHit = path(gFiber, 'fbg', { fill: 'none', stroke: 'transparent' });
		const fpcG = mk('g', gFiber);
		const fpc = [0, 1, 2].map(() => path(fpcG, 'fpc', { fill: 'none' }));
		// light on the fiber
		const gFL = mk('g', root, { 'pointer-events': 'none' });
		const gFLs = mk('g', gFL, { filter: `url(#${id}-glow)` });
		const gFLc = mk('g', gFL);
		const lightTubes = {
			inS: mkTube(gFLs, null), inC: mkTube(gFLc, null), outS: mkTube(gFLs, null), outC: mkTube(gFLc, null),
			brS: [path(gFLs, null, { fill: 'none' }), path(gFLs, null, { fill: 'none' })], brC: [path(gFLc, null, { fill: 'none' }), path(gFLc, null, { fill: 'none' })]
		};
		const NOP = 8; // output pulses drawn at most
		const outP = Array.from({ length: NOP }, () => ({ s: path(gFLs, null, { fill: 'none' }), c: path(gFLc, null, { fill: 'none' }) }));
		const lightHit = { in: path(root, 'light_in', { fill: 'none', stroke: 'transparent' }), out: path(root, 'light_out', { fill: 'none', stroke: 'transparent' }) };
		const outHit = Array.from({ length: NOP }, () => path(root, 'out_pulses', { fill: 'none', stroke: 'transparent' }));
		// crystal stand-in, ring (back half), disc, ring (front half)
		const gPost = mk('g', root);
		const post = { side: path(gPost, 'crystal'), top: path(gPost, 'crystal') };
		const postEdge = path(gPost, 'crystal', { fill: 'none' });
		const NSEG = 90;
		interface RingLayer {
			soft: SVGGElement;
			core: SVGGElement;
			segS: PathEl[];
			segC: PathEl[];
			pS: PathEl[];
			pC: PathEl[];
			pN: PathEl[];
		}
		const mkRing = (): RingLayer => {
			const g = mk('g', root, { 'pointer-events': 'none' });
			const soft = mk('g', g, { filter: `url(#${id}-glow)` });
			const core = mk('g', g);
			return {
				soft, core,
				segS: Array.from({ length: NSEG }, () => path(soft, null, { fill: 'none', 'stroke-linecap': 'butt' })),
				segC: Array.from({ length: NSEG }, () => path(core, null, { fill: 'none', 'stroke-linecap': 'butt' })),
				pS: Array.from({ length: N0 }, () => path(soft, null, { fill: 'none' })),
				pC: Array.from({ length: N0 }, () => path(core, null, { fill: 'none' })),
				pN: Array.from({ length: N0 }, () => path(core, null, { fill: 'none' }))
			};
		};
		const ringBack = mkRing();
		const gDisc = mk('g', root);
		const disc = { side: path(gDisc, 'resonator'), top: path(gDisc, 'resonator') };
		const ringFront = mkRing();
		const gMode = mk('g', root);
		const modePath = path(gMode, 'wgm', { fill: 'none' });
		const modeHead = path(gMode, 'wgm');
		const ringHit = path(root, 'ring_light', { fill: 'none', stroke: 'transparent' });
		const pulseHit = Array.from({ length: N0 }, () => path(root, 'ring_pulses', { fill: 'none', stroke: 'transparent' }));

		// ---------------------------------------------------------------------------- camera
		const regions = (): { full: Rect; plot: Rect } => {
			if (w < 700) return { full: [0.05, 0.22, 0.95, 0.95], plot: [0.05, 0.2, 0.95, 0.43] };
			const top = Math.min(0.26, 170 / Math.max(1, h));
			return { full: [0.04, top, 0.97, 0.94], plot: [0.03, top + 0.02, 0.46, 0.92] };
		};
		const zLo = ZF - TD / 2 - HP;
		const discBox = (pad: number, z0: number, z1: number): Shot['box'] => [CX - R - pad, CY - R - pad, CX + R + pad, CY + R + pad, z0, z1];
		const SHOTS: Record<string, Shot> = {
			arrive: { az: -18, el: 18, box: discBox(6, zLo, ZF + 4), region: 'full', zoom: 0.55 },
			crystal: { az: -20, el: 24, box: discBox(3, zLo, ZF + 3), region: 'full', zoom: 0.78 },
			resonator: { az: -20, el: 46, box: discBox(1, ZF - 3, ZF + 3), region: 'full', zoom: 0.78 },
			taper: { az: -20, el: 42, box: [CX - R - 16, FY - 4, XD + 3, CY + R + 2, ZF - 4, ZF + 3], region: 'full', zoom: 0.92 },
			setup: { az: -14, el: 52, box: [PUMP[0] - 2, PUMP[1] - 4, XD + 3, ESA[3] + 2, 0, HB], region: 'full', zoom: 1 },
			scan: { az: -16, el: 50, box: [SCAN[0] - 2, PUMP[1] - 3, XD + 3, SCAN[3] + 3, 0, HB], region: 'plot', zoom: 1 },
			soliton: { az: -20, el: 40, box: [CX - R - 6, FY - 3, XD + 3, CY + R + 6, ZF - 4, ZF + 3], region: 'full', zoom: 0.9 },
			spectrum: { az: -16, el: 50, box: [OSA[0] - 1, FY - 6, XD + 3, OSA[3] + 2, 0, HB], region: 'plot', zoom: 1 },
			pulse: { az: -20, el: 40, box: [CX - R - 6, FY - 3, XD + 3, CY + R + 6, ZF - 4, ZF + 3], region: 'plot', zoom: 0.92 }
		};
		const projRaw = (az: number, el: number, X: number, Y: number, Z: number): P2 => {
			const ca = Math.cos(az * DEG), sa = Math.sin(az * DEG);
			return [X * ca - Y * sa, (X * sa + Y * ca) * Math.sin(el * DEG) - Z * Math.cos(el * DEG)];
		};
		const centre = (b: Shot['box']): P3 => [(b[0] + b[2]) / 2, (b[1] + b[3]) / 2, (b[4] + b[5]) / 2];
		const camOf = (sh: Shot): Cam => {
			const rg = regions()[sh.region];
			const rx0 = rg[0] * w, ry0 = rg[1] * h, rw = (rg[2] - rg[0]) * w, rh = (rg[3] - rg[1]) * h;
			let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
			const b = sh.box;
			for (const X of [b[0], b[2]]) for (const Y of [b[1], b[3]]) for (const Z of [b[4], b[5]]) {
				const q = projRaw(sh.az, sh.el, X, Y, Z);
				x0 = Math.min(x0, q[0]); x1 = Math.max(x1, q[0]); y0 = Math.min(y0, q[1]); y1 = Math.max(y1, q[1]);
			}
			const s = Math.min(rw / (x1 - x0), rh / (y1 - y0)) * sh.zoom;
			const f = projRaw(sh.az, sh.el, ...centre(b));
			return { ca: Math.cos(sh.az * DEG), sa: Math.sin(sh.az * DEG), ce: Math.cos(sh.el * DEG), se: Math.sin(sh.el * DEG), s, ox: rx0 + 0.5 * rw - s * f[0], oy: ry0 + 0.5 * rh - s * f[1] };
		};
		const blendCam = (a: Shot, b: Shot, t: number): Cam => {
			if (t <= 0) return camOf(a);
			if (t >= 1) return camOf(b);
			const ca = camOf(a), cb = camOf(b);
			const az = lerp(a.az, b.az, t), el = lerp(a.el, b.el, t);
			const s = Math.exp(lerp(Math.log(ca.s), Math.log(cb.s), t));
			const fa = centre(a.box), fb = centre(b.box);
			const fw: P3 = [lerp(fa[0], fb[0], t), lerp(fa[1], fb[1], t), lerp(fa[2], fb[2], t)];
			const sa0 = projRaw(a.az, a.el, ...fw), sb0 = projRaw(b.az, b.el, ...fw);
			const pa: P2 = [ca.ox + ca.s * sa0[0], ca.oy + ca.s * sa0[1]];
			const pb: P2 = [cb.ox + cb.s * sb0[0], cb.oy + cb.s * sb0[1]];
			const pf: P2 = [lerp(pa[0], pb[0], t), lerp(pa[1], pb[1], t)];
			const r = projRaw(az, el, ...fw);
			return { ca: Math.cos(az * DEG), sa: Math.sin(az * DEG), ce: Math.cos(el * DEG), se: Math.sin(el * DEG), s, ox: pf[0] - s * r[0], oy: pf[1] - s * r[1] };
		};
		const camAt = (p: number): Cam => {
			const k = (cid: string, a = 0, b = 0.35) => ease(seg(cq(cid, p), a, b));
			if (p < C.resonator[0]) return blendCam(SHOTS.arrive, SHOTS.crystal, k('crystal', 0, 0.7));
			if (p < C.taper[0]) return blendCam(SHOTS.crystal, SHOTS.resonator, k('resonator'));
			if (p < C.setup[0]) return blendCam(SHOTS.resonator, SHOTS.taper, k('taper', 0, 0.3));
			if (p < C.transmission[0]) return blendCam(SHOTS.taper, SHOTS.setup, k('setup', 0, 0.4));
			if (p < C.soliton[0]) return blendCam(SHOTS.setup, SHOTS.scan, k('transmission', 0, 0.08));
			if (p < C.spectrum[0]) return blendCam(SHOTS.scan, SHOTS.soliton, k('soliton', 0, 0.3));
			if (p < C.pulse[0]) return blendCam(SHOTS.soliton, SHOTS.spectrum, k('spectrum', 0, 0.2));
			return blendCam(SHOTS.spectrum, SHOTS.pulse, k('pulse', 0, 0.2));
		};
		let cam: Cam = camOf(SHOTS.crystal);
		const P = (X: number, Y: number, Z: number): P2 => [
			cam.ox + cam.s * (X * cam.ca - Y * cam.sa),
			cam.oy + cam.s * ((X * cam.sa + Y * cam.ca) * cam.se - Z * cam.ce)
		];
		const f1 = (v: number) => (Math.round(v * 10) / 10).toString();
		const dOf = (q: P2[], close = true) => (q.length < 2 ? '' : 'M' + q.map((v) => `${f1(v[0])} ${f1(v[1])}`).join('L') + (close ? 'Z' : ''));
		const plan = (q: P2[], Z: number) => q.map((v) => P(v[0], v[1], Z));
		/** plan angle that faces the viewer (nearest point of a horizontal circle) */
		const frontAng = () => Math.atan2(cam.ca, cam.sa);
		const isFront = (a: number) => Math.cos(a - frontAng()) > 0;
		const circ = (cx: number, cy: number, r: number, z: number, a0: number, a1: number, n: number): P2[] => {
			const out: P2[] = [];
			for (let i = 0; i <= n; i++) {
				const a = lerp(a0, a1, i / n);
				out.push(P(cx + r * Math.cos(a), cy + r * Math.sin(a), z));
			}
			return out;
		};

		// ---------------------------------------------------------------------------- state from p
		type Ring = 'off' | 'mode' | 'cw' | 'scan' | 'one';
		interface State {
			res: number; // disc + post presence
			dz: number; // rise
			post: number;
			mode: number; // mode path (resonator chapter)
			fiber: number; // fiber presence
			fdy: number; // fiber slide (from behind)
			boxes: number; // pump, scan, FPC
			lower: number; // OSA, scope, ESA, PDs, FBG, LO, branches, electrical lines
			osa: number; // OSA + its branch (spectrum chapter)
			yMax: number; // output fiber drawn down to this plan Y
			inF: number; // input light front (bus arclength)
			outF: number; // output light front (beyond the tangent point)
			outB: number; // output brightness 0..1
			ring: Ring;
			ringI: number; // ring brightness 0..1 (cw)
			fill: number; // ring fill fraction from the tangent point (taper chapter)
			t: number | null; // scan time at the pen (transmission chapter)
			ty: number; // transmission at the pen
			ramp: number; // scan ramp marker fraction, -1 = none
			outPulses: 'none' | 'scan' | 'one';
			view: 'meas' | 'zoom' | 'sim'; // transmission chapter: which plot drives the model
			nSol: number; // solitons drawn in the 'one' state (2 / 5 with the Fig. 4a alternates)
			sim: number; // simulated intracavity power at the pen (simulation alternate), as drawn
		}
		const state = (p: number): State => {
			const q = (cid: string) => cq(cid, p);
			const after = (cid: string) => p >= C[cid][1];
			const inCh = (cid: string) => p >= C[cid][0] && p < C[cid][1];
			const S: State = {
				res: easeOut(seg(q('crystal'), 0, 0.55)), dz: (1 - easeOut(seg(q('crystal'), 0, 0.6))) * 14, post: 1,
				mode: 0, fiber: 0, fdy: 0, boxes: 0, lower: 0, osa: 0, yMax: YFBG + 1, inF: 0, outF: 0, outB: 0, ring: 'off', ringI: 0, fill: 0,
				t: null, ty: 1, ramp: -1, outPulses: 'none', view: 'meas', nSol: 1, sim: 0
			};
			if (p >= C.resonator[0]) S.mode = after('taper') ? 0 : p >= C.taper[0] ? 1 - seg(q('taper'), 0.62, 0.75) : ease(seg(q('resonator'), 0.15, 0.45));
			if (p >= C.taper[0]) {
				const tq = q('taper');
				S.fiber = after('taper') ? 1 : easeOut(seg(tq, 0, 0.3));
				S.fdy = after('taper') ? 0 : (1 - easeOut(seg(tq, 0, 0.35))) * -22;
				const lit = after('taper') ? 1 : seg(tq, 0.38, 0.6);
				S.inF = lit * sT;
				S.fill = after('taper') ? 1 : ease(seg(tq, 0.58, 0.8));
				S.outF = after('taper') ? Infinity : seg(tq, 0.6, 0.95) * (OUTA.len - 0);
				S.ring = 'cw';
				S.ringI = 0.75;
				S.outB = 0.55;
				S.yMax = Y_TAPER;
			}
			if (p >= C.setup[0]) {
				const sq = q('setup');
				S.boxes = after('setup') ? 1 : ease(seg(sq, 0.1, 0.45));
				S.lower = after('setup') ? 1 : ease(seg(sq, 0.25, 0.6));
				S.inF = sT;
				S.yMax = after('setup') ? YFBG + 1 : lerp(Y_TAPER, YFBG + 1, ease(seg(sq, 0.2, 0.6)));
				S.outF = after('setup') ? Infinity : lerp(sAtY(BUS, Y_TAPER) - sT, BUS.len - sT, seg(sq, 0.45, 0.95));
			}
			if (p >= C.transmission[0]) {
				S.lower = after('transmission') ? 0 : 1 - ease(seg(q('transmission'), 0, 0.06));
				S.yMax = lerp(YFBG + 1, 345, ease(seg(q('transmission'), 0, 0.06)));
				S.outF = Infinity;
				if (!after('transmission') && plotId === 'transmission_sim' && PEN.sim.pts.length > 1) {
					// simulation alternate on screen: ring brightness = simulated intracavity power at its pen (as drawn);
					// no measured scan time, so no scan marker, waveform or pulses
					const ps = PEN.sim.at(p);
					S.view = 'sim';
					S.sim = clamp01(ps.y);
					S.ring = 'cw';
					S.fill = 1;
					S.ringI = 0.05 + 0.95 * S.sim;
					S.outB = 0.5;
				} else if (!after('transmission')) {
					const zoom = plotId === 'transmission_steps';
					const pe = penScan(p, zoom);
					S.view = zoom ? 'zoom' : 'meas';
					S.t = pe.t;
					S.ty = pe.y;
					S.ring = 'scan';
					S.ringI = inside(pe.t);
					S.outB = 0.15 + 0.85 * clamp01((pe.y - 0.68) / (1.0 - 0.68));
					S.ramp = clamp01(pe.t / 4);
					S.outPulses = 'scan';
				}
			}
			if (p >= C.soliton[0]) {
				S.ring = 'one';
				S.ringI = 0.12;
				S.outB = 0.42;
				S.outPulses = 'one';
				S.nSol = inCh('spectrum') && plotId === 'spectrum_two' ? 2 : inCh('spectrum') && plotId === 'spectrum_five' ? 5 : 1;
				S.yMax = 345;
				S.boxes = 1 - ease(seg(q('soliton'), 0, 0.25));
			}
			if (p >= C.spectrum[0]) {
				const sp = q('spectrum');
				S.boxes = after('spectrum') ? 1 - ease(seg(q('pulse'), 0, 0.12)) : ease(seg(sp, 0, 0.2));
				S.osa = after('spectrum') ? 1 - ease(seg(q('pulse'), 0, 0.12)) : ease(seg(sp, 0.05, 0.25));
				S.yMax = after('spectrum') ? lerp(YOSA, 345, ease(seg(q('pulse'), 0, 0.12))) : YOSA;
			}
			return S;
		};

		// ---------------------------------------------------------------------------- drawing helpers
		const pal = () => PAL[theme];
		const on = (pid: string) => hi.includes(pid);
		const hl = (c: string, pid: string) => (on(pid) ? mix(c, pal().accent, 0.55) : c);
		const lookOf = (pid: string, d: string) => (spec.parts.find((q) => q.id === pid)?.look?.color as string | undefined) || d;
		const drawBox = (b: Box, r: Rect, z0: number, z1: number, col: string, fo: [number, number, number], edge: string, pid: string, a: number) => {
			if (!show(b.g, a)) return;
			const c = hl(col, pid);
			const set = (e: PathEl, d: string, o: number) => {
				e.setAttribute('d', d);
				e.setAttribute('fill', c);
				e.setAttribute('fill-opacity', o.toFixed(3));
				e.setAttribute('stroke', on(pid) ? pal().accent : edge);
				e.setAttribute('stroke-opacity', on(pid) ? '0.95' : '0.8');
				e.setAttribute('stroke-width', '1');
			};
			const [X0, Y0, X1, Y1] = r;
			set(b.top, dOf([P(X0, Y0, z1), P(X1, Y0, z1), P(X1, Y1, z1), P(X0, Y1, z1)]), fo[0]);
			set(b.front, dOf([P(X0, Y1, z1), P(X1, Y1, z1), P(X1, Y1, z0), P(X0, Y1, z0)]), fo[1]);
			set(b.side, dOf([P(X0, Y0, z1), P(X0, Y1, z1), P(X0, Y1, z0), P(X0, Y0, z0)]), fo[2]);
		};
		/** instrument screen + glyph on a box top face (Fig. 2d icons), plan coordinates */
		const drawGlyph = (b: Box, scr: Rect | null, glyph: P2[][], col: string, z: number) => {
			const c = pal();
			if (scr) {
				b.screen.setAttribute('d', dOf(plan([[scr[0], scr[1]], [scr[2], scr[1]], [scr[2], scr[3]], [scr[0], scr[3]]], z)));
				b.screen.setAttribute('fill', c.screen);
				b.screen.setAttribute('fill-opacity', theme === 'light' ? '0.85' : '0.9');
				show(b.screen, 1);
			} else show(b.screen, 0);
			b.glyph.setAttribute('d', glyph.map((g) => dOf(plan(g, z), false)).join(''));
			b.glyph.setAttribute('stroke', col);
			b.glyph.setAttribute('stroke-width', f1(Math.max(0.8, 0.45 * cam.s)));
			show(b.glyph, glyph.length ? 1 : 0);
		};
		/** a tube (fiber or light) along a route [s0, s1], split in chunks so the width can follow the taper profile */
		const tube = (els: PathEl[], r: Route, s0: number, s1: number, wPx: (s: number) => number, col: string, o: number, waist: boolean) => {
			// one filled screen-space ribbon (smooth width along the thin taper section); els[0] carries it
			const a = Math.max(0, s0), b = Math.min(r.len, s1);
			for (let i = 1; i < els.length; i++) show(els[i], 0);
			const e = els[0];
			if (b <= a + 0.01 || o < 0.01) return show(e, 0);
			const ss: number[] = [a];
			for (let i = 1; i < r.cum.length - 1; i++) if (r.cum[i] > a && r.cum[i] < b) ss.push(r.cum[i]);
			if (waist) for (let x = sW0; x <= sW1; x += 0.5) if (x > a && x < b) ss.push(x);
			ss.push(b);
			ss.sort((u, v) => u - v);
			const pts = ss.map((x) => {
				const q = routeAt(r, x);
				return P(q[0], q[1], ZF);
			});
			const L: P2[] = [], Rt: P2[] = [];
			for (let i = 0; i < pts.length; i++) {
				const p0 = pts[Math.max(0, i - 1)], p1 = pts[Math.min(pts.length - 1, i + 1)];
				const dx = p1[0] - p0[0], dy = p1[1] - p0[1];
				const l = Math.hypot(dx, dy) || 1;
				const hw = Math.max(0.3, wPx(ss[i]) / 2);
				const nx = (-dy / l) * hw, ny = (dx / l) * hw;
				L.push([pts[i][0] + nx, pts[i][1] + ny]);
				Rt.push([pts[i][0] - nx, pts[i][1] - ny]);
			}
			e.setAttribute('d', dOf([...L, ...Rt.reverse()]));
			e.setAttribute('fill', col);
			e.setAttribute('stroke', 'none');
			show(e, o);
		};
		const head = (tip: P2, from: P2, size: number): string => {
			const dx = tip[0] - from[0], dy = tip[1] - from[1];
			const l = Math.hypot(dx, dy) || 1;
			const ux = dx / l, uy = dy / l;
			const b: P2 = [tip[0] - ux * size, tip[1] - uy * size];
			return dOf([tip, [b[0] - uy * size * 0.45, b[1] + ux * size * 0.45], [b[0] + uy * size * 0.45, b[1] - ux * size * 0.45]]);
		};
		/** ring brightness at plan angle a (fixed frame) for the current state; 0..1 */
		const ringIntensity = (S: State, p: number): ((a: number) => number) => {
			const rot = OM * p;
			if (S.ring === 'cw') return () => S.ringI;
			if (S.ring === 'one') return () => S.ringI;
			if (S.ring === 'scan' && S.t != null) {
				const t = S.t;
				const base = 0.05 + 0.95 * S.ringI;
				if (t >= T_LAST) return () => base;
				if (t >= T_STEP) return () => 0.1;
				if (t < T_I) return () => base;
				if (t < T_NOISE) return (a) => base * (0.55 + 0.45 * Math.cos(NL * (a - rot)));
				return (a) => {
					let v = 0, n = 0;
					for (const z of noise) {
						v += z.a * Math.cos(z.n * (a - rot) + z.ph + z.nu * t);
						n += z.a;
					}
					return base * clamp01(0.55 + (1.1 * v) / n);
				};
			}
			return () => 0;
		};
		/** angles of the pulses on the ring at p (scan: the alive ones; one: the single soliton) */
		const pulsesAt = (S: State, p: number): { a: number; k: number }[] => {
			if (S.ring === 'one') return (multi[S.nSol] ?? multi[1]).map((b, k) => ({ a: b + OM * p, k }));
			if (S.ring === 'scan' && S.t != null && S.t >= T_STEP && S.t < T_LAST) {
				const out: { a: number; k: number }[] = [];
				pulseAng.forEach((b, k) => {
					if (S.t! < deathT[k]) out.push({ a: b + OM * p, k });
				});
				return out;
			}
			return [];
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
			blurStd.setAttribute('stdDeviation', Math.max(1.4, 0.9 * s).toFixed(2));
			blur.setAttribute('x', String(-w));
			blur.setAttribute('y', String(-h));
			blur.setAttribute('width', String(3 * w));
			blur.setAttribute('height', String(3 * h));
			const fade = S.res;
			const zo = -S.dz; // rise of the disc and post (crystal chapter)

			// electrical lines (Fig. 2d, black): scan control, PD -> oscilloscope, PD -> mixer -> ESA, branch to the oscilloscope, LO
			const eLines: { pts: P2[]; a: number }[] = [
				{ pts: [[390.1, PUMP[3]], [390.1, (SCAN[1] + SCAN[3]) / 2], [SCAN[0], (SCAN[1] + SCAN[3]) / 2]], a: S.boxes },
				{ pts: [[PDT[0], YPD], [SCOPE[2], YPD]], a: S.lower },
				{ pts: [[PDB[0], YFBG], [LO[2], YFBG]], a: S.lower },
				{ pts: [[LO[0], YFBG], [ESA[2], YFBG]], a: S.lower },
				{ pts: [[436.8, YFBG], [436.8, 385.3], [SCOPE[2], 385.3]], a: S.lower },
				{ pts: [[(LO[0] + LO[2]) / 2, LO[1]], [(LO[0] + LO[2]) / 2, 393]], a: S.lower }
			];
			eLines.forEach((L, i) => {
				const e = elec[i];
				if (L.a < 0.01) return show(e, 0);
				e.setAttribute('d', dOf(plan(L.pts, HB / 2), false));
				e.setAttribute('stroke', c.ink);
				e.setAttribute('stroke-width', f1(Math.max(1, 0.35 * s)));
				show(e, L.a * 0.85);
			});

			// boxes: instruments (cream), pump (red edge), scan (teal edge), detectors and mixer (small)
			const cream = lookOf('osa', '#f2e8d0');
			const instEdge = theme === 'light' ? '#4a4790' : '#8f8cd8';
			const zb = (a: number) => (1 - a) * -8;
			const boxSpec: { pid: string; r: Rect; col: string; edge: string; a: number; hgt: number }[] = [
				{ pid: 'esa', r: ESA, col: cream, edge: instEdge, a: S.lower, hgt: HB },
				{ pid: 'scope', r: SCOPE, col: cream, edge: instEdge, a: S.lower, hgt: HB },
				{ pid: 'osa', r: OSA, col: cream, edge: instEdge, a: Math.max(S.lower, S.osa), hgt: HB },
				{ pid: 'scan', r: SCAN, col: cream, edge: lookOf('scan', '#46b4a0'), a: S.boxes, hgt: HB },
				{ pid: 'pump', r: PUMP, col: cream, edge: lookOf('pump', '#c8504a'), a: S.boxes, hgt: HB },
				{ pid: 'lo', r: LO, col: mix(lookOf('lo', '#3a3a3a'), c.ink, 0.6), edge: c.ink, a: S.lower, hgt: 1.6 },
				{ pid: 'pd_beat', r: PDB, col: mix(lookOf('pd_beat', '#3a3a3a'), c.ink, 0.6), edge: c.ink, a: S.lower, hgt: 4 },
				{ pid: 'pd_trans', r: PDT, col: mix(lookOf('pd_trans', '#3a3a3a'), c.ink, 0.6), edge: c.ink, a: S.lower, hgt: 4 }
			];
			for (const B of boxSpec) {
				const b = boxes[B.pid];
				if (B.a < 0.01) {
					show(b.g, 0);
					continue;
				}
				const z0 = zb(B.a);
				const z1 = z0 + B.hgt;
				drawBox(b, B.r, z0, z1, B.col, c.boxA, B.edge, B.pid, B.a);
				const [X0, Y0, X1, Y1] = B.r;
				const bw = X1 - X0, bh = Y1 - Y0;
				const scr: Rect = [X0 + 0.07 * bw, Y0 + 0.16 * bh, X0 + 0.4 * bw, Y1 - 0.16 * bh];
				const sx = (f: number) => lerp(scr[0] + 1, scr[2] - 1, f);
				const sy = (f: number) => lerp(scr[3] - 1, scr[1] + 1, f);
				let glyph: P2[][] = [];
				let col = c.glyph;
				let useScr: Rect | null = scr;
				if (B.pid === 'osa') glyph = Array.from({ length: 11 }, (_, i) => [[sx((i + 0.5) / 11), sy(0)], [sx((i + 0.5) / 11), sy(0.15 + 0.75 * Math.exp(-(((i - 5) / 3.2) ** 2)))]] as P2[]);
				else if (B.pid === 'scope') glyph = [Array.from({ length: 41 }, (_, i) => [sx(i / 40), sy(0.5 + 0.38 * Math.sin((i / 40) * TAU * 2.5))] as P2)];
				else if (B.pid === 'esa') glyph = [Array.from({ length: 41 }, (_, i) => [sx(i / 40), sy(0.08 + 0.82 / (1 + ((i - 20) / 2.2) ** 2))] as P2)];
				else if (B.pid === 'scan') {
					const sr: Rect = [X0 + 0.07 * bw, Y0 + 0.14 * bh, X0 + 0.48 * bw, Y1 - 0.14 * bh];
					useScr = sr;
					glyph = [[[sr[0] + 1, sr[3] - 1], [sr[2] - 1, sr[1] + 1]]];
				} else if (B.pid === 'pump') {
					// axes and one line (single-frequency laser), no screen
					useScr = null;
					const ax: Rect = [X0 + 0.1 * bw, Y0 + 0.12 * bh, X0 + 0.55 * bw, Y0 + 0.48 * bh];
					glyph = [[[ax[0], ax[1]], [ax[0], ax[3]], [ax[2], ax[3]]]];
					col = c.ink;
				} else if (B.pid === 'lo') {
					useScr = null;
					glyph = [[[X0 + 0.2 * bw, Y0 + 0.2 * bh], [X1 - 0.2 * bw, Y1 - 0.2 * bh]], [[X0 + 0.2 * bw, Y1 - 0.2 * bh], [X1 - 0.2 * bw, Y0 + 0.2 * bh]]];
					col = pal().inkSoft;
				} else useScr = null;
				drawGlyph(b, useScr, glyph, col, z1 + 0.05);
				// pump line (red) and the scan marker (dot on the ramp at the plot pen)
				if (B.pid === 'pump') {
					const ax: Rect = [X0 + 0.1 * bw, Y0 + 0.12 * bh, X0 + 0.55 * bw, Y0 + 0.48 * bh];
					const xl = lerp(ax[0], ax[2], 0.62);
					b.dot.setAttribute('d', dOf(plan([[xl, ax[3]], [xl, ax[1] + 0.15 * (ax[3] - ax[1])]], z1 + 0.05), false));
					b.dot.setAttribute('fill', 'none');
					b.dot.setAttribute('stroke', lookOf('pump', '#c8504a'));
					b.dot.setAttribute('stroke-width', f1(Math.max(1, 0.5 * s)));
					show(b.dot, 1);
				} else if (B.pid === 'scan' && S.ramp >= 0) {
					const sr: Rect = [X0 + 0.07 * bw, Y0 + 0.14 * bh, X0 + 0.48 * bw, Y1 - 0.14 * bh];
					const a: P2 = [sr[0] + 1, sr[3] - 1], e: P2 = [sr[2] - 1, sr[1] + 1];
					const m = P(lerp(a[0], e[0], S.ramp), lerp(a[1], e[1], S.ramp), z1 + 0.05);
					const rd = Math.max(2.2, 0.75 * s);
					b.dot.setAttribute('d', `M${f1(m[0] - rd)} ${f1(m[1])}a${f1(rd)} ${f1(rd)} 0 1 0 ${f1(2 * rd)} 0a${f1(rd)} ${f1(rd)} 0 1 0 ${f1(-2 * rd)} 0Z`);
					b.dot.setAttribute('fill', on('scan') ? c.accent : c.light);
					b.dot.setAttribute('stroke', 'none');
					show(b.dot, 1);
				} else show(b.dot, 0);
			}

			// fiber: bus (with the thin taper section), branches, FBG, FPC paddles
			const fdy = S.fdy;
			const yCut = sAtY(BUS, S.yMax);
			const busEnd = Math.min(BUS.len, yCut);
			const busStart = S.boxes > 0.01 ? 0 : Math.max(0, sW0 - 30);
			const fw = (sc: number) => (sv: number) => Math.max(1.3, 1.5 * s * sc) * wProf(sv);
			const fCol = hl(mix(c.fiber, theme === 'light' ? '#ffffff' : '#101010', theme === 'light' ? 0.15 : 0.3), 'taper');
			// the fiber slides in from behind (plan Y offset): applied through a temporary camera shift
			const camSave = cam;
			if (Math.abs(fdy) > 0.01) {
				const d = P(0, fdy, 0), o = P(0, 0, 0);
				cam = { ...cam, ox: cam.ox + d[0] - o[0], oy: cam.oy + d[1] - o[1] };
			}
			tube(busTube, BUS, busStart, busEnd, fw(1), fCol, S.fiber, true);
			const brs: [Route, number][] = [[OSAB, Math.max(S.lower, S.osa)], [PDTB, S.lower]];
			brs.forEach(([r, a], i) => {
				const e = brTube[i];
				if (a < 0.01) return show(e, 0);
				e.setAttribute('d', dOf(plan(r.pts, ZF), false));
				e.setAttribute('stroke', fCol);
				e.setAttribute('stroke-width', f1(Math.max(1.3, 1.5 * s)));
				show(e, a);
			});
			// FBG: grating ticks across the fiber on the bottom row
			if (S.lower > 0.01) {
				const tk: string[] = [];
				for (let x = FBGX[1] + 1; x < FBGX[0]; x += 1.6) tk.push(dOf([P(x, YFBG - 1.1, ZF), P(x, YFBG + 1.1, ZF)], false));
				fbgTicks.setAttribute('d', tk.join(''));
				fbgTicks.setAttribute('stroke', on('fbg') ? c.accent : c.ink);
				fbgTicks.setAttribute('stroke-width', f1(Math.max(0.8, 0.4 * s)));
				fbgHit.setAttribute('d', dOf([P(FBGX[1], YFBG, ZF), P(FBGX[0], YFBG, ZF)], false));
				fbgHit.setAttribute('stroke-width', f1(Math.max(8, 3 * s)));
				show(fbgTicks, S.lower);
				show(fbgHit, S.lower);
			} else {
				show(fbgTicks, 0);
				show(fbgHit, 0);
			}
			// FPC: three paddles standing on the fiber (Fig. 2d draws three circles)
			fpc.forEach((e, i) => {
				if (S.boxes < 0.01) return show(e, 0);
				const pw = (FPC[2] - FPC[0]) / 3;
				const xc = FPC[0] + pw * (i + 0.5);
				const r = 0.42 * pw;
				const q: P2[] = [];
				for (let j = 0; j <= 28; j++) {
					const a = (TAU * j) / 28;
					q.push(P(xc + r * Math.cos(a), FY, ZF + r + 0.4 + r * Math.sin(a) + zb(S.boxes)));
				}
				e.setAttribute('d', dOf(q));
				e.setAttribute('stroke', on('fpc') ? c.accent : lookOf('fpc', '#4fa8c8'));
				e.setAttribute('stroke-width', f1(Math.max(1.2, 0.6 * s)));
				e.setAttribute('fill', lookOf('fpc', '#4fa8c8'));
				e.setAttribute('fill-opacity', '0.12');
				show(e, S.boxes);
			});

			// light on the fiber: input (pump, constant), output (transmitted, brightness from the plot pen in the scan)
			const lc = c.light;
			const lw = (sc: number) => (sv: number) => Math.max(0.9, 0.85 * s * sc) * wProf(sv);
			const inA = S.inF > 0.01 ? 1 : 0;
			const inStart = busStart;
			tube(lightTubes.inS, BUS, inStart, Math.min(S.inF, sT), lw(2.4), lc, inA * c.glowA * (on('light_in') ? 1 : 0.75), true);
			tube(lightTubes.inC, BUS, inStart, Math.min(S.inF, sT), lw(0.8), c.lightCore, inA, true);
			const outEnd = Math.min(busEnd, sT + S.outF, S.lower > 0.01 ? sFBG : busEnd);
			const ob = S.outB * (on('light_out') ? 1.25 : 1);
			tube(lightTubes.outS, BUS, sT, outEnd, lw(2.4), lc, Math.min(1, ob) * c.glowA, true);
			tube(lightTubes.outC, BUS, sT, outEnd, lw(0.8), c.lightCore, Math.min(1, ob), true);
			// branches light up when the output front passes their junction
			[[OSAB, sJO, Math.max(S.lower, S.osa)], [PDTB, sJP, S.lower]].forEach(([r, sj, a], i) => {
				const rt = r as Route;
				const len = Math.min(rt.len, sT + S.outF - (sj as number));
				const els = [lightTubes.brS[i], lightTubes.brC[i]];
				if ((a as number) < 0.01 || len <= 0 || S.outB < 0.01) return els.forEach((e) => show(e, 0));
				const d = dOf(plan(subRoute(rt, 0, len), ZF), false);
				els.forEach((e, j) => {
					e.setAttribute('d', d);
					e.setAttribute('stroke', j ? c.lightCore : lc);
					e.setAttribute('stroke-width', f1(Math.max(0.9, 0.85 * s * (j ? 0.8 : 2.4))));
					show(e, (a as number) * Math.min(1, ob) * (j ? 1 : c.glowA));
				});
			});
			// hit strokes for the light
			const hitW = f1(Math.max(8, 2.5 * s));
			if (inA) {
				lightHit.in.setAttribute('d', dOf(plan(subRoute(BUS, inStart, Math.min(S.inF, sT)), ZF), false));
				lightHit.in.setAttribute('stroke-width', hitW);
				show(lightHit.in, 1);
			} else show(lightHit.in, 0);
			if (outEnd > sT + 0.5 && S.outB > 0.01) {
				lightHit.out.setAttribute('d', dOf(plan(subRoute(BUS, sT + 3, outEnd), ZF), false));
				lightHit.out.setAttribute('stroke-width', hitW);
				show(lightHit.out, 1);
			} else show(lightHit.out, 0);
			cam = camSave;

			// output pulses: one per roundtrip per pulse, moving at the drawn ring speed (spacing and width schematic)
			const ring = pulsesAt(S, p);
			const vS = RR * OM; // drawn speed, world units per unit p
			const route = S.osa > 0.5 ? OUTO : OUTA;
			const rEnd = Math.min(route.len, route === OUTO ? route.len : sAtY(route, S.yMax));
			let nOut = 0;
			if (S.outPulses !== 'none') {
				const srcs: { a: number; born: number; dies: number }[] =
					S.outPulses === 'one'
						? (multi[S.nSol] ?? multi[1]).map((b) => ({ a: b + OM * p, born: S.nSol === 1 ? C.soliton[0] : -Infinity, dies: Infinity }))
						: pulseAng.map((b, k) => ({ a: b + OM * p, born: lives[S.view === 'zoom' ? 1 : 0].birth, dies: lives[S.view === 'zoom' ? 1 : 0].death[k] }));
				for (const src of srcs) {
					const d0 = RR * wrap(src.a - PHI_T);
					for (let j = 0; j < 6 && nOut < NOP; j++) {
						const sPos = d0 + j * TAU * RR;
						if (sPos > rEnd) break;
						const te = p - sPos / vS; // emission time
						if (te < src.born || te >= src.dies) continue;
						const half = 2.2;
						const q = subRoute(route, sPos - half, sPos + half);
						if (q.length < 2) continue;
						const d = dOf(plan(q, ZF), false);
						const o = outP[nOut];
						o.s.setAttribute('d', d);
						o.c.setAttribute('d', d);
						o.s.setAttribute('stroke', lc);
						o.c.setAttribute('stroke', on('out_pulses') || on('pulse_train') ? mix(c.lightCore, c.accent, 0.5) : c.lightCore);
						o.s.setAttribute('stroke-width', f1(Math.max(4, 2.6 * s)));
						o.c.setAttribute('stroke-width', f1(Math.max(1.6, 1.0 * s)));
						show(o.s, c.glowA);
						show(o.c, 1);
						outHit[nOut].setAttribute('d', d);
						outHit[nOut].setAttribute('stroke-width', f1(Math.max(10, 3 * s)));
						show(outHit[nOut], 1);
						nOut++;
					}
				}
			}
			for (let i = nOut; i < NOP; i++) {
				show(outP[i].s, 0);
				show(outP[i].c, 0);
				show(outHit[i], 0);
			}

			// crystal stand-in: plain post under the disc (shape not drawn)
			const zTop = ZF - TD / 2 + zo;
			const fa = frontAng();
			const cyl = (els: { side: PathEl; top: PathEl }, r: number, z0: number, z1: number, col: string, edge: string, fo: [number, number], pid: string, a: number, top = true) => {
				if (a < 0.01) {
					show(els.side, 0);
					show(els.top, 0);
					return;
				}
				const sideP = [...circ(CX, CY, r, z1, fa - Math.PI / 2, fa + Math.PI / 2, 24), ...circ(CX, CY, r, z0, fa + Math.PI / 2, fa - Math.PI / 2, 24)];
				const cc = hl(col, pid);
				els.side.setAttribute('d', dOf(sideP));
				els.top.setAttribute('d', dOf(circ(CX, CY, r, z1, 0, TAU, 48)));
				for (const [e, o] of [[els.side, fo[1]], [els.top, fo[0]]] as const) {
					e.setAttribute('fill', cc);
					e.setAttribute('fill-opacity', o.toFixed(3));
					e.setAttribute('stroke', on(pid) ? c.accent : edge);
					e.setAttribute('stroke-opacity', on(pid) ? '0.95' : '0.7');
					e.setAttribute('stroke-width', '1');
					show(e, e === els.top && !top ? 0 : a);
				}
			};
			cyl(post, RP, zTop - HP, zTop, c.post, mix(c.post, c.inkSoft, 0.5), [c.postA, c.postA * 0.8], 'crystal', fade * S.post, false);
			// post outline: silhouette verticals and the bottom front arc only (its top edge is hidden under the disc)
			if (fade * S.post > 0.01) {
				post.side.setAttribute('stroke', 'none');
				const l0 = P(CX + RP * Math.cos(fa - Math.PI / 2), CY + RP * Math.sin(fa - Math.PI / 2), zTop);
				const r0 = P(CX + RP * Math.cos(fa + Math.PI / 2), CY + RP * Math.sin(fa + Math.PI / 2), zTop);
				const bot = circ(CX, CY, RP, zTop - HP, fa - Math.PI / 2, fa + Math.PI / 2, 24);
				postEdge.setAttribute('d', dOf([l0, ...bot, r0], false));
				postEdge.setAttribute('stroke', on('crystal') ? c.accent : mix(c.post, c.inkSoft, 0.5));
				postEdge.setAttribute('stroke-opacity', on('crystal') ? '0.95' : '0.7');
				postEdge.setAttribute('stroke-width', '1');
				show(postEdge, fade * S.post);
			} else show(postEdge, 0);

			// ring of light: segments (cw / modulated / noisy) and pulses, back half under the disc, front half over it
			const zr = ZF + zo;
			const I = ringIntensity(S, p);
			const fillTo = S.fill; // fraction of the ring lit from the tangent point (taper chapter)
			const ringOn = S.ring !== 'off' && fade > 0.01;
			const segW = Math.max(1.2, 0.9 * s);
			const hiRing = on('ring_light') || on('wgm');
			const lits = Array.from({ length: NSEG }, (_, i) => {
				const am = (TAU * (i + 0.5)) / NSEG;
				return ringOn ? I(am) * (S.ring === 'cw' ? (wrap(am - PHI_T + 1e-6) < fillTo * TAU ? 1 : 0) : 1) : 0;
			});
			const uniform = lits.every((v) => Math.abs(v - lits[0]) < 1e-6);
			const styleSeg = (L: RingLayer, i: number, d: string, lit: number) => {
				L.segS[i].setAttribute('d', d);
				L.segC[i].setAttribute('d', d);
				L.segS[i].setAttribute('stroke', c.light);
				L.segC[i].setAttribute('stroke', hiRing ? mix(c.lightCore, c.accent, 0.4) : c.lightCore);
				L.segS[i].setAttribute('stroke-width', f1(segW * 3.4));
				L.segC[i].setAttribute('stroke-width', f1(segW));
				show(L.segS[i], Math.min(1, 1.2 * lit) * c.glowA * fade);
				show(L.segC[i], Math.min(1, 1.2 * lit) * fade);
			};
			for (let i = 0; i < NSEG; i++) {
				if (!uniform) break;
				for (const L of [ringFront, ringBack]) {
					if (i === 0 && lits[0] >= 0.01) {
						const f0 = frontAng() + (L === ringFront ? -Math.PI / 2 : Math.PI / 2);
						styleSeg(L, 0, dOf(circ(CX, CY, RR, zr, f0, f0 + Math.PI, 48), false), lits[0]);
					} else {
						show(L.segS[i], 0);
						show(L.segC[i], 0);
					}
				}
			}
			for (let i = 0; i < NSEG && !uniform; i++) {
				const a0 = (TAU * i) / NSEG, a1 = (TAU * (i + 1)) / NSEG, am = (a0 + a1) / 2;
				const fr = isFront(am);
				const lit = lits[i];
				const L = fr ? ringFront : ringBack, Lo = fr ? ringBack : ringFront;
				show(Lo.segS[i], 0);
				show(Lo.segC[i], 0);
				if (lit < 0.01) {
					show(L.segS[i], 0);
					show(L.segC[i], 0);
					continue;
				}
				styleSeg(L, i, dOf(circ(CX, CY, RR, zr, a0, a1, 3), false), lit);
			}
			// pulses on the ring (sharp; width schematic)
			const hiP = on('ring_pulses') || on('soliton');
			for (let k = 0; k < N0; k++) {
				const pk = ring.find((r) => r.k === k);
				const els = [ringFront.pS[k], ringFront.pC[k], ringFront.pN[k], ringBack.pS[k], ringBack.pC[k], ringBack.pN[k]];
				if (!pk || fade < 0.01) {
					els.forEach((e) => show(e, 0));
					show(pulseHit[k], 0);
					continue;
				}
				const a = pk.a;
				const fr = isFront(wrap(a));
				const L = fr ? ringFront : ringBack, Lo = fr ? ringBack : ringFront;
				show(Lo.pS[k], 0);
				show(Lo.pC[k], 0);
				show(Lo.pN[k], 0);
				const wide = dOf(circ(CX, CY, RR, zr, a - 8 * DEG, a + 8 * DEG, 8), false);
				const mid = dOf(circ(CX, CY, RR, zr, a - 4 * DEG, a + 4 * DEG, 6), false);
				const nar = dOf(circ(CX, CY, RR, zr, a - 1.6 * DEG, a + 1.6 * DEG, 4), false);
				L.pS[k].setAttribute('d', wide);
				L.pC[k].setAttribute('d', mid);
				L.pN[k].setAttribute('d', nar);
				L.pS[k].setAttribute('stroke', c.light);
				L.pC[k].setAttribute('stroke', c.light);
				L.pN[k].setAttribute('stroke', hiP ? mix(c.lightCore, c.accent, 0.5) : c.lightCore);
				L.pS[k].setAttribute('stroke-width', f1(Math.max(5, 3.4 * s)));
				L.pC[k].setAttribute('stroke-width', f1(Math.max(2.4, 1.6 * s)));
				L.pN[k].setAttribute('stroke-width', f1(Math.max(2, 1.3 * s)));
				show(L.pS[k], c.glowA * fade);
				show(L.pC[k], fade);
				show(L.pN[k], fade);
				pulseHit[k].setAttribute('d', mid);
				pulseHit[k].setAttribute('stroke-width', f1(Math.max(12, 3 * s)));
				show(pulseHit[k], 1);
			}
			if (ringOn && (S.ring !== 'cw' || fillTo > 0.05)) {
				ringHit.setAttribute('d', dOf(circ(CX, CY, RR, zr, 0, TAU, 48)));
				ringHit.setAttribute('stroke-width', f1(Math.max(8, 2.2 * s)));
				ringHit.setAttribute('data-pick', S.ring === 'one' ? 'soliton_bg' : 'ring_light');
				show(ringHit, 1);
			} else show(ringHit, 0);

			// disc stand-in (translucent MgF2)
			const discA: [number, number] = [c.discA[0], c.discA[1]];
			cyl(disc, R, ZF - TD / 2 + zo, ZF + TD / 2 + zo, c.disc, c.discEdge, discA, 'resonator', fade);

			// mode path (resonator chapter): the path of the light round the rim and a marker running round it
			if (S.mode > 0.01 && fade > 0.01) {
				const zt = ZF + TD / 2 + zo + 0.02;
				const span = TAU * clamp01(S.mode * 1.02);
				modePath.setAttribute('d', dOf(circ(CX, CY, RR, zt, PHI_T, PHI_T + span, 96), false));
				modePath.setAttribute('stroke', on('wgm') ? c.accent : c.light);
				modePath.setAttribute('stroke-width', f1(Math.max(1.2, 0.22 * s)));
				modePath.setAttribute('stroke-opacity', '0.85');
				const am = PHI_T + OM * 0.5 * (p - C.resonator[0]);
				const tip = P(CX + RR * Math.cos(am), CY + RR * Math.sin(am), zt);
				const back = P(CX + RR * Math.cos(am - 0.12), CY + RR * Math.sin(am - 0.12), zt);
				modeHead.setAttribute('d', head(tip, back, Math.max(7, 2.6 * s)));
				modeHead.setAttribute('fill', on('wgm') ? c.accent : c.light);
				show(modePath, S.mode);
				show(modeHead, S.mode >= 0.999 ? S.mode : 0);
				modePath.setAttribute('data-pick', 'wgm');
			} else {
				show(modePath, 0);
				show(modeHead, 0);
			}
		};

		// ---------------------------------------------------------------------------- picking
		const LOC = 'Herr et al., arXiv v3 (2013)';
		const COLOUR = 'Colour illustrative: 1553 nm is infrared.';
		const ringInfo = (): PickInfo => {
			const S = lastS;
			const t = S?.t;
			if (S?.view === 'sim')
				return {
					id: 'ring_light',
					label: 'Light in the resonator (simulation shown)',
					detail: [
						`Brightness follows the simulated intracavity power at the plot pen, as drawn (Fig. 3a, ${LOC}, p.9); the waveform is not drawn.`,
						'Simulation, not a measurement. ' + COLOUR
					]
				};
			if (S?.ring === 'cw' || t == null)
				return {
					id: 'ring_light',
					label: 'Light in the resonator',
					detail: ['Pump light coupled in through the taper runs round the rim (drawn on resonance, brightness illustrative).', COLOUR]
				};
			const tt = `${t.toFixed(2)} ms`;
			const base = `Brightness follows the measured transmission at the plot pen (${tt}): lower transmission = more light inside (${LOC}, p.3; Fig. 2a).`;
			let what: string;
			if (t < T_I) what = 'Light builds up as the pump tunes into the resonance (thermal triangle, effectively blue detuned; p.2).';
			else if (t < T_NOISE)
				what = 'From marker I (1.50 ms) the spectrum shows comb lines: a periodic, un-pulsed waveform is drawn (Fig. 1c left inset); its lobe count is illustrative.';
			else if (t < T_STEP)
				what = `From about 1.55 ms the beat note is broad and noisy (Fig. 2c; spectra II and III, Fig. 2b caption): a noisy waveform is drawn, illustrative.`;
			else if (t >= T_LAST)
				what = `After the last step (3.86 ms) the narrow beat note ends (Fig. 2c) and the transmission returns to about its off-resonance level with no small thermal triangle: no solitons drawn.`;
			else
				return {
					id: 'ring_light',
					label: 'Light in the resonator during the scan',
					detail: [`Scan time ${tt}, past the first step (3.12 ms): the beat note is narrow; solitons on a weak background (background brightness illustrative).`, COLOUR]
				};
			return { id: 'ring_light', label: 'Light in the resonator during the scan', detail: [what, base, COLOUR] };
		};
		const pulsesInfo = (): PickInfo => {
			const S = lastS;
			if (S?.ring === 'one' && S.nSol > 1)
				return {
					id: 'ring_pulses',
					label: `${S.nSol} solitons`,
					detail: [
						`The ${S.nSol === 2 ? 'two' : 'five'}-soliton state of Fig. 4a (${LOC}, p.10): its spectrum is structured by the number and spacing of the solitons.`,
						'Positions on the ring illustrative: the spacing is not stated. Pulse width drawn schematic. ' + COLOUR
					]
				};
			if (S?.ring === 'one')
				return {
					id: 'ring_pulses',
					label: 'One soliton',
					detail: [
						`The one-soliton state of Fig. 4a (${LOC}, p.10), reached with the tuned scan of SI Fig. 6 (p.18), not necessarily the last step of Fig. 2a.`,
						'A sharp pulse on a weak continuous background; peak to background power can exceed several hundreds (p.3).',
						'Pulse width drawn schematic: 200 fs is 1/142 of the 28.4 ps roundtrip; circulation speed not to scale.',
						COLOUR
					]
				};
			const n = S?.t != null ? nPulsesAt(S.t) : 0;
			return {
				id: 'ring_pulses',
				label: `Solitons, illustrative count (${n} drawn)`,
				detail: [
					`The paper does not state how many solitons each step of Fig. 2a holds: 5, 4, 3, 2 are drawn for illustration. In simulation the first step gives several pulses and each further step fewer, at random spacing (Fig. 3c; ${LOC}, p.3).`,
					'Steps read at 3.12 (first), 3.55, 3.65, 3.76 and 3.86 ms (Fig. 2a). After the last step the narrow beat note ends (Fig. 2c) and the transmission returns to about its off-resonance level with no small thermal triangle: no solitons drawn.',
					'Pulse width drawn schematic; ' + COLOUR.toLowerCase()
				]
			};
		};
		const INFO = (pid: string): PickInfo | null => {
			const S = lastS;
			if (pid === 'ring_light') return ringInfo();
			if (pid === 'ring_pulses') return pulsesInfo();
			if (pid === 'soliton_bg')
				return {
					id: 'soliton_bg',
					label: 'Continuous background',
					detail: ['Weak cw background in the resonator around the soliton (Eq. (1), p.3); brightness illustrative.', COLOUR]
				};
			if (pid === 'light_in')
				return {
					id: 'light_in',
					label: 'Pump light, 1553 nm',
					detail: [`Fiber laser amplified by an EDFA; coupled pump power 5 mW for the Fig. 2a scan (${LOC}, p.5 Methods; p.8 Fig. 2a caption).`, COLOUR]
				};
			if (pid === 'light_out') {
				if (S?.t != null)
					return {
						id: 'light_out',
						label: `Transmitted light: ${S.ty.toFixed(3)} at ${S.t.toFixed(2)} ms`,
						detail: [`Brightness follows the digitized transmission at the plot pen (${LOC}, p.8 Fig. 2a).`, COLOUR]
					};
				return {
					id: 'light_out',
					label: 'Transmitted light',
					detail: ['Pump light that passes the resonator, plus the light coupled back out of it; brightness illustrative.', COLOUR]
				};
			}
			if (pid === 'resonator')
				return {
					id: 'resonator',
					label: 'MgF_{2} microresonator',
					detail: ['Drawn as a plain disc stand-in: diameter about 2 mm, derived from the FSR (not stated); drawn size, thickness and rim not to scale.']
				};
			if (pid === 'crystal')
				return {
					id: 'crystal',
					label: 'MgF_{2} crystal',
					detail: ['Drawn as a plain post stand-in, not to scale: the crystal body in Fig. 1a is wider than the resonator; its tiers and how it was made are not drawn.']
				};
			if (pid === 'taper')
				return {
					id: 'taper',
					label: 'tapered optical fiber',
					detail: ['Drawn as a plain fiber thinning past the disc (Fig. 2d); taper size, gap and contact point not stated. Layout of Fig. 2d, not to scale.']
				};
			if (pid === 'scan' && S && S.ramp >= 0)
				return {
					id: 'scan',
					label: 'Scan',
					detail: [`Marker on the ramp = scan time at the plot pen: ${S.t?.toFixed(2)} of 4 ms. Frequency span of the scan not stated.`]
				};
			if (pid === 'out_pulses')
				return {
					id: 'out_pulses',
					label: 'Output pulses',
					detail: [
						`Each pass of a soliton at the taper couples a pulse out; with one soliton the pulses are spaced by T_{R} = 28.4 ps (${LOC}, p.4).`,
						'Spacing and width drawn schematic. ' + COLOUR
					]
				};
			return null;
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
					return INFO(pid) ?? pid;
				}
				return null;
			},
			anchor(pid) {
				const S = lastS;
				if (!S) return null;
				if (pid === 'resonator') {
					if (S.res < 0.5 || lastP >= C.taper[0]) return null;
					const aR = Math.atan2(-cam.sa, cam.ca); // right-most point of the disc on screen
					return P(CX + R * Math.cos(aR), CY + R * Math.sin(aR), ZF + TD / 2 - S.dz);
				}
				if (pid === 'pump') {
					if (S.boxes < 0.6) return null;
					return P(PUMP[0] + 0.5 * (PUMP[2] - PUMP[0]), PUMP[1], HB);
				}
				return null;
			},
			resize(nw, nh) {
				w = Math.max(1, nw);
				h = Math.max(1, nh);
			},
			plot(pid) {
				plotId = pid;
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
