// Scene module: junction lasers that run continuously at room temperature (Hayashi, Panish, Foy, Sumski,
// Appl. Phys. Lett. 1970). Spec: data/history/showcases/hayashi1970.yaml. Contract: ../showcase/types.ts. Renderer 2.5D.
//
// Two pictures share one SVG:
// 1. The growth apparatus of the paper's Fig. 1, drawn flat as the figure draws it (a schematic section, no scale) in
//    Fig. 1 pixel units (spec `fig1_px`). The sliding solution holder moves toward the stop so that solutions 1-4 pass
//    over the seed in turn; a wall covers the seed between them (reading of the drawing, see the spec).
// 2. A layer stack in axonometric view (X along the cavity, Y across, Z up; plan units = µm, heights x5). First an
//    inset piece of the wafer that grows layer by layer, then the chip (plan 370 x 80 µm to scale), flipped p side down
//    onto diamond on a copper block (neutral stand-ins). Drawn thicknesses: printed values or midpoints (spec geometry).
//
// Light follows the Fig. 2 plot pen (penAt, the plot assembler's own reveal): current = pen x, light L = pen y from the
// digitized dc curve. Spontaneous glow from the end faces = min(L, L_B) / L_end; beam = (L - L_B) / (L_end - L_B) at
// and above the bend of the printed dc curve (about 0.81 A, a figure reading; no threshold is printed for this diode).
// Fig. 3 chapter: the current is that of the trace being drawn, glow from the Fig. 2 dc level there, beam onset with
// the 0.80 A trace. 311 K chapter: lasing shown, no drive current (the paper gives only current densities at 311 K).
import { clamp01, ease, lerp, seg } from '../showcase/progress';
import { cleanPoints, penAt, plotSeries, revealAt } from '../showcase/plot';
import type { PickInfo, Series, ShowcaseContext, ShowcaseHandle, ShowcaseModule, Theme } from '../showcase/types';

type P2 = [number, number];
type V3 = [number, number, number];
type Rect = [number, number, number, number];
type Geo = Record<string, unknown>;

const NS = 'http://www.w3.org/2000/svg';
const DEG = Math.PI / 180;
const num = (v: unknown, d: number): number => (typeof v === 'number' && Number.isFinite(v) ? v : d);
const pair = (v: unknown, d: P2): P2 => (Array.isArray(v) && v.length === 2 && v.every((x) => typeof x === 'number') ? [v[0], v[1]] : d);
const rect4 = (v: unknown, d: Rect): Rect => (Array.isArray(v) && v.length === 4 && v.every((x) => typeof x === 'number') ? (v as Rect) : d);
let uid = 0;

// ------------------------------------------------------------------------------------------------ colours
interface Pal {
	ink: string;
	inkSoft: string;
	accent: string;
	graphite: string;
	graphite2: string;
	hatch: string;
	tube: string;
	tubeA: number;
	heater: string;
	tc: string;
	melt: string;
	light: string;
	lightCore: string;
	glowA: number;
	heat: string;
	edgeTo: string;
	edgeMix: number;
	edgeA: number;
	shade: string;
}
const PAL: Record<Theme, Pal> = {
	dark: {
		ink: '#c3c2b7', inkSoft: '#898781', accent: '#3987e5', graphite: '#4a4d52', graphite2: '#5b5f66', hatch: '#9a9da3',
		tube: '#cfd8dc', tubeA: 0.07, heater: '#b07a4a', tc: '#9aa0a6', melt: '#c9c3a8', light: '#ff5a3c', lightCore: '#ffd2c4',
		glowA: 0.85, heat: '#e0905a', edgeTo: '#ffffff', edgeMix: 0.35, edgeA: 0.55, shade: '#000000'
	},
	light: {
		ink: '#52514e', inkSoft: '#6f6d68', accent: '#2a78d6', graphite: '#8a8d93', graphite2: '#9da1a8', hatch: '#4a4d52',
		tube: '#7d8b91', tubeA: 0.08, heater: '#8f5a2c', tc: '#5f656b', melt: '#b3ab88', light: '#e0401f', lightCore: '#b52a10',
		glowA: 0.5, heat: '#c0642a', edgeTo: '#000000', edgeMix: 0.45, edgeA: 0.75, shade: '#000000'
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

// ------------------------------------------------------------------------------------------------ stack (µm, heights x5)
const EX = 5; // vertical exaggeration of the stack (drawn units per µm of thickness; plan 1 unit = 1 µm)
/** chip stack bottom-up as grown; drawn thickness in µm (spec geometry.drawn_thickness_um, else these) */
const STACK = ['n_contact', 'substrate', 'layer_1', 'layer_2', 'layer_3', 'layer_4', 'zn_skin', 'p_contact'] as const;
type SId = (typeof STACK)[number];
const DRAWN_NOTE: Record<SId, string> = {
	n_contact: 'Film thickness not stated: drawn thin.',
	substrate: 'Drawn 6 µm and broken: thickness not stated (schematic).',
	layer_1: 'Drawn 3.5 µm: midpoint of the printed 3-4 µm (assumed for drawing).',
	layer_2: 'Drawn 1.0 µm: the printed upper bound (≲ 1 µm).',
	layer_3: 'Drawn 1.5 µm (printed ≈ 1.5 µm).',
	layer_4: 'Drawn 1.5 µm (printed ≈ 1.5 µm).',
	zn_skin: 'Drawn 0.2 µm (printed ≈ 0.2 µm), inside layer 4.',
	p_contact: 'Film thickness not stated: drawn thin.'
};
const HEIGHTS_NOTE = 'Heights exaggerated 5× against the plan; the wafer piece is illustrative, the chip plan 370 × 80 µm is to scale.';

// ------------------------------------------------------------------------------------------------ module
const mod: ShowcaseModule = {
	renderer: '2.5d',
	build(ctx: ShowcaseContext): ShowcaseHandle {
		if (ctx.kind !== '2.5d') throw new Error('hayashi1970 is a 2.5D scene');
		const { svg, spec } = ctx;
		const id = `dh${++uid}`;
		let w = Math.max(1, ctx.width);
		let h = Math.max(1, ctx.height);
		let theme: Theme = ctx.theme;
		let k = 0;
		let hi: string[] = [];

		// ---------------------------------------------------------------------------- chapters
		const fallback: Record<string, [number, number]> = {
			seed: [0, 0.07], layer1: [0.07, 0.15], layer2: [0.15, 0.23], layer3: [0.23, 0.3], layer4: [0.3, 0.37], contacts: [0.37, 0.45],
			diode: [0.45, 0.53], mount: [0.53, 0.62], cw: [0.62, 0.78], spectra: [0.78, 0.9], limit: [0.9, 1]
		};
		const C: Record<string, [number, number]> = {};
		for (const [cid, r] of Object.entries(fallback)) C[cid] = (spec.chapters.find((c) => c.id === cid)?.p ?? r) as [number, number];
		const cq = (cid: string, p: number) => seg(p, C[cid][0], C[cid][1]);
		const inCh = (cid: string, p: number) => p >= C[cid][0] && p < C[cid][1];

		// ---------------------------------------------------------------------------- spec values
		const part = (pid: string) => spec.parts.find((q) => q.id === pid);
		const geo = (pid: string): Geo => (part(pid)?.geometry ?? {}) as Geo;
		const look = (pid: string, d: string) => {
			const c = part(pid)?.look?.color;
			return typeof c === 'string' && /^#[0-9a-f]{6}$/i.test(c) ? c : d;
		};
		const drawnUm = (pid: string, d: number) => num(geo(pid).drawn_thickness_um, d);
		const TH: Record<SId, number> = {
			n_contact: 0.4,
			substrate: drawnUm('substrate', 6),
			layer_1: drawnUm('layer_1', 3.5),
			layer_2: drawnUm('layer_2', 1.0),
			layer_3: drawnUm('layer_3', 1.5),
			layer_4: drawnUm('layer_4', 1.5),
			zn_skin: drawnUm('zn_skin', 0.2),
			p_contact: 0.4
		};
		const COL: Record<SId, string> = {
			n_contact: look('n_contact', '#b8bcc2'),
			substrate: look('substrate', '#6f7d8c'),
			layer_1: look('layer_1', '#4c9bf0'),
			layer_2: look('layer_2', '#f7962c'),
			layer_3: look('layer_3', '#46dca5'),
			layer_4: look('layer_4', '#c6a6fa'),
			zn_skin: look('zn_skin', '#ea70a3'),
			p_contact: look('p_contact', '#d4a640')
		};
		const cDiamond = look('diamond', '#e6f1f5');
		const cCu = look('cu_block', '#b87333');
		const cIn = look('in_contact', '#a8a69d');
		const cDrive = look('drive', '#a8a69d');
		const cLight = look('emission', '#ff5a3c');
		const chipG = geo('diode');
		const CL = num(chipG.length_um, 370);
		const CW = num(chipG.width_um, 80);

		// Fig. 1 geometry (fig1_px, schematic)
		const tubeY = pair(geo('silica_tube').walls_y, [40, 340]);
		const heaterBox = rect4(geo('aux_heater').box, [155, 410, 1105, 475]);
		const tcG = geo('thermocouple');
		const tcFrom = pair(tcG.from, [35, 258]);
		const tcTip = pair(tcG.tip, [478, 258]);
		const barG = geo('seed_holder');
		const barBox = rect4(barG.box, [190, 168, 910, 200]);
		const stopG = (barG.stop ?? {}) as Geo;
		const stopC = pair(stopG.center, [170, 183]);
		const stopR = num(stopG.r, 20);
		const hG = geo('solution_holder');
		const wallsX: P2[] = Array.isArray(hG.walls_x) && hG.walls_x.length === 5 ? (hG.walls_x as unknown[]).map((v, i) => pair(v, [[430, 485], [537, 590], [640, 668], [720, 748], [800, 860]][i] as P2)) : [[430, 485], [537, 590], [640, 668], [720, 748], [800, 860]];
		const wellsG = (hG.wells_x ?? {}) as Geo;
		const wellsX: P2[] = [1, 2, 3, 4].map((i, j) => pair(wellsG[`solution_${i}`], [wallsX[j][1], wallsX[j + 1][0]]));
		const topY = pair(hG.top_y, [90, 160]);
		const lf = (hG.lower_frame ?? {}) as Geo;
		const lfUnder = pair(lf.under_bar_y, [200, 232]);
		const lfBottom = pair(lf.bottom_y, [285, 315]);
		const lfX = pair(lf.x, [430, 860]);
		const pr = (hG.push_rod ?? {}) as Geo;
		const prX = pair(pr.x, [860, 1130]);
		const prY = pair(pr.y, [222, 232]);
		const SEED: Rect = [wallsX[0][0], barBox[1] - 1, wallsX[0][1] + 5, barBox[1] + 6]; // seed set into the bar top under wall 1
		const seedX = (SEED[0] + SEED[2]) / 2;
		const FIG_W = 1156;
		const FIG_Y: P2 = [tubeY[0] - 12, heaterBox[3] + 10];
		// holder offsets (fig px, negative = toward the stop): wall i or well i centred over the seed
		const cen = (r: P2) => (r[0] + r[1]) / 2;
		const dxWall = wallsX.map((r) => seedX - cen(r));
		const dxWell = wellsX.map((r) => seedX - cen(r));
		// Fig. 1 leaves the holder only ~240 px of travel before the STOP; the story needs ~365 px. Fig. 1 is not to scale:
		// the bar's left end and the stop are drawn further left (BAR_EXT), and the last wall stops short of the
		// thermocouple tip (holder's closed end at least 4 px right of it).
		const dxEnd = Math.max(dxWall[4], tcTip[0] + 7 - (lfX[1] - 10));
		dxWall[4] = dxEnd;
		const BAR_EXT = Math.max(0, Math.ceil(stopC[0] + stopR + 8 - (lfX[0] + dxEnd)));
		const stopX = stopC[0] - BAR_EXT;

		// ---------------------------------------------------------------------------- Fig. 2 / Fig. 3 pens
		const liPlot = spec.plots?.find((q) => q.id === 'li');
		const liAll: Series[] = liPlot ? plotSeries(liPlot) : [];
		const dcI = Math.max(0, liAll.findIndex((s) => s.name === 'dc'));
		const dcPts = liAll[dcI] ? cleanPoints(liAll[dcI], false, false) : [];
		/** Fig. 2 dc light at current I (A), linear between digitized points (first crossing) */
		const dcAt = (I: number): number => {
			for (let i = 1; i < dcPts.length; i++) {
				const a = dcPts[i - 1], b = dcPts[i];
				if (b[0] >= I) return b[0] === a[0] ? b[1] : lerp(a[1], b[1], clamp01((I - a[0]) / (b[0] - a[0])));
			}
			return dcPts.length ? dcPts[dcPts.length - 1][1] : 0;
		};
		const IB = 0.81; // drawn bend of the printed dc curve (plot note, figure reading)
		const LB = dcAt(IB); // light at the bend (about 110 units)
		const END: P2 = dcPts.length ? dcPts[dcPts.length - 1] : [0.8537, 182.65]; // where the drawn dc curve leaves the frame
		const spPlot = spec.plots?.find((q) => q.id === 'spectra');
		const spAll: Series[] = spPlot ? plotSeries(spPlot) : [];
		const spI = spAll.map((s, i) => {
			const v = parseFloat(String(s.name));
			return Number.isFinite(v) ? v : ([0.1, 0.72, 0.8][i] ?? 0);
		});
		interface Light {
			I: number | null; // current, A (null = no current from a plot)
			L: number | null; // Fig. 2 dc light (arb. units)
			glow: number; // spontaneous glow from the end faces 0..1 (min(L, L_B) / L_end)
			beam: number; // laser beam 0..1 ((L - L_B) / (L_end - L_B) at and above the bend)
			mode: 'off' | 'li' | 'spectra' | 'limit';
			trace: number; // Fig. 3 trace index or -1
		}
		const fromL = (I: number, L: number, mode: Light['mode'], trace = -1): Light => ({
			I,
			L,
			glow: Math.min(L, LB) / END[1],
			beam: I >= IB ? clamp01((L - LB) / Math.max(1, END[1] - LB)) : 0,
			mode,
			trace
		});
		const lightAt = (p: number): Light => {
			const off: Light = { I: null, L: null, glow: 0, beam: 0, mode: 'off', trace: -1 };
			if (p >= C.cw[0] && p < C.cw[1]) {
				const pen = penAt(spec, 'li', p)[dcI];
				return pen ? fromL(pen.x, pen.y, 'li') : off;
			}
			if (p >= C.spectra[0] && p < C.spectra[1]) {
				// the trace being drawn sets the current; glow from the Fig. 2 dc level there, beam onset with 0.80 A
				const rv = revealAt(spec, 'spectra', p);
				let t = -1;
				rv.forEach((f, i) => {
					if (f > 0) t = i;
				});
				if (t < 0) return off;
				const I = spI[t] ?? 0;
				const st = clamp01(rv[t] * 8);
				const lt = fromL(I, dcAt(I), 'spectra', t);
				return { ...lt, glow: lt.glow * st, beam: I >= 0.795 ? 0.3 * st : 0 };
			}
			if (p >= C.limit[0]) {
				// 311 K: continuous lasing (abstract); no current from Fig. 2 (297 K)
				const f = ease(seg(cq('limit', p), 0, 0.2));
				return { I: null, L: null, glow: (LB / END[1]) * f, beam: f, mode: 'limit', trace: -1 };
			}
			return off;
		};

		// ---------------------------------------------------------------------------- SVG scaffolding
		const mk = <K extends keyof SVGElementTagNameMap>(tag: K, parent: Element, attrs: Record<string, string | number> = {}): SVGElementTagNameMap[K] => {
			const e = document.createElementNS(NS, tag) as SVGElementTagNameMap[K];
			for (const [a, v] of Object.entries(attrs)) e.setAttribute(a, String(v));
			parent.appendChild(e);
			return e;
		};
		const root = mk('g', svg, { 'data-scene': 'hayashi1970' });
		const defs = mk('defs', root);
		const glow = mk('filter', defs, { id: `${id}-glow`, x: '-50%', y: '-50%', width: '200%', height: '200%', 'color-interpolation-filters': 'sRGB' });
		mk('feGaussianBlur', glow, { stdDeviation: 4 });
		const haze = mk('filter', defs, { id: `${id}-haze`, x: '-80%', y: '-80%', width: '260%', height: '260%', 'color-interpolation-filters': 'sRGB' });
		mk('feGaussianBlur', haze, { stdDeviation: 9 });
		const hatch = (hid: string, rot: number) => {
			const pt = mk('pattern', defs, { id: `${id}-${hid}`, patternUnits: 'userSpaceOnUse', width: 9, height: 9, patternTransform: `rotate(${rot})` });
			const bg = mk('rect', pt, { x: 0, y: 0, width: 9, height: 9 });
			const ln = mk('line', pt, { x1: 0, y1: 0, x2: 0, y2: 9, 'stroke-width': 1.2 });
			return { bg, ln };
		};
		const hatchBar = hatch('hb', 45);
		const hatchHold = hatch('hh', -45);
		const beamGrad = [0, 1].map((i) => {
			const g = mk('linearGradient', defs, { id: `${id}-beam${i}`, gradientUnits: 'userSpaceOnUse' });
			const s0 = mk('stop', g, { offset: 0, 'stop-opacity': 1 });
			const s1 = mk('stop', g, { offset: 0.55, 'stop-opacity': 0.55 });
			const s2 = mk('stop', g, { offset: 1, 'stop-opacity': 0 });
			return { g, stops: [s0, s1, s2] };
		});

		type El = SVGElement;
		const setPick = (e: El, pid: string) => {
			e.setAttribute('data-pick', pid);
			return e;
		};
		const path = (parent: Element, pid: string | null, attrs: Record<string, string | number> = {}): SVGPathElement => {
			const e = mk('path', parent, { 'stroke-linejoin': 'round', 'stroke-linecap': 'round', ...attrs });
			if (pid) setPick(e, pid);
			return e;
		};
		const show = (e: El, o: number) => {
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
		const rectD = (x0: number, y0: number, x1: number, y1: number) => `M${x0} ${y0}H${x1}V${y1}H${x0}Z`;
		const NSS = { 'vector-effect': 'non-scaling-stroke' };

		// ---------------------------------------------------------------------------- apparatus (Fig. 1 px, one transform)
		const app = mk('g', root);
		const tubeFill = path(app, 'silica_tube', { d: rectD(0, tubeY[0], FIG_W, tubeY[1]), stroke: 'none' });
		const heaterRod = path(app, 'aux_heater', { d: rectD(heaterBox[0], heaterBox[1] + 12, heaterBox[2], heaterBox[3] - 6), 'fill-opacity': 0.08, ...NSS });
		const heaterCoil = (() => {
			// helix along the rod: loops every ~88 px (Fig. 1 draws 11)
			const n = 11;
			const pitch = (heaterBox[2] - heaterBox[0] - 30) / n;
			const yc = (heaterBox[1] + heaterBox[3]) / 2 + 3;
			const ry = (heaterBox[3] - heaterBox[1]) / 2 + 2;
			const q: P2[] = [];
			for (let t = 0; t <= n * 2 * Math.PI; t += Math.PI / 16) q.push([heaterBox[0] + 15 + (t / (2 * Math.PI)) * pitch + 9 * Math.sin(t), yc - ry * Math.cos(t)]);
			return path(app, 'aux_heater', { d: dOf(q, false), fill: 'none', ...NSS });
		})();
		const tcPath = path(app, 'thermocouple', {
			d: [-5, 0, 5].map((o) => `M${tcFrom[0]} ${tcTip[1] + o}H${tcTip[0] - 6}`).join('') + `M${tcTip[0] - 6} ${tcTip[1] - 9}a9 9 0 0 1 0 18`,
			fill: 'none',
			...NSS
		});
		const tcDot = path(app, 'thermocouple', { d: `M${tcTip[0] - 9} ${tcTip[1]}a3 3 0 1 0 6 0a3 3 0 1 0 -6 0Z`, stroke: 'none' });
		const bar = path(app, 'seed_holder', { d: rectD(barBox[0] - BAR_EXT, barBox[1], barBox[2], barBox[3]), fill: `url(#${id}-hb)`, ...NSS });
		const stop = path(app, 'seed_holder', { d: `M${stopX - stopR} ${stopC[1]}a${stopR} ${stopR} 0 1 0 ${2 * stopR} 0a${stopR} ${stopR} 0 1 0 ${-2 * stopR} 0Z`, ...NSS });
		const holder = mk('g', app);
		const lower = [
			path(holder, 'solution_holder', { d: rectD(lfX[0], lfUnder[0], lfX[1], lfUnder[1]), fill: `url(#${id}-hh)`, ...NSS }),
			path(holder, 'solution_holder', { d: rectD(lfX[0], lfBottom[0], lfX[1], lfBottom[1]), fill: `url(#${id}-hh)`, ...NSS }),
			path(holder, 'solution_holder', { d: rectD(lfX[1] - 10, lfUnder[1], lfX[1], lfBottom[0]), fill: `url(#${id}-hh)`, ...NSS })
		];
		const seedG = mk('g', app);
		const seedEl = path(seedG, 'substrate', { d: rectD(SEED[0], SEED[1], SEED[2], SEED[3]), ...NSS });
		const seedTop = path(seedG, 'substrate', { d: rectD(SEED[0], SEED[1] - 2.5, SEED[2], SEED[1]), stroke: 'none' });
		const holderTop = mk('g', app);
		const walls = wallsX.map((r) => path(holderTop, 'solution_holder', { d: rectD(r[0], topY[0], r[1], topY[1]), fill: `url(#${id}-hh)`, ...NSS }));
		const melts = wellsX.map((r, i) => path(holderTop, `solution_${i + 1}`, { d: rectD(r[0] + 2, topY[0] + 12, r[1] - 2, SEED[1] - 2.5), ...NSS }));
		const waves = wellsX.map((r, i) => {
			const cx = cen(r);
			const d = [0, 1, 2].map((j) => `M${cx - 9 + (j % 2) * 4} ${topY[0] + 30 + j * 13}q4 -4 8 0t8 0`).join('');
			return path(holderTop, `solution_${i + 1}`, { d, fill: 'none', ...NSS });
		});
		const rod = path(holderTop, 'solution_holder', { d: rectD(prX[0], prY[0], Math.min(FIG_W, prX[1]), prY[1]), stroke: 'none' });
		const tubeLines = path(app, 'silica_tube', { d: `M0 ${tubeY[0]}H${FIG_W}M0 ${tubeY[1]}H${FIG_W}`, fill: 'none', ...NSS });
		const tubeHit = path(app, 'silica_tube', { d: `M0 ${tubeY[0]}H${FIG_W}M0 ${tubeY[1]}H${FIG_W}`, fill: 'none', stroke: 'transparent', 'stroke-width': 10, ...NSS });
		const flowG = mk('g', app);
		const flowLines = [tubeY[0] + 22, tubeY[1] - 22].map((y) => path(flowG, 'hydrogen', { d: `M18 ${y}H${FIG_W - 18}`, fill: 'none', 'stroke-dasharray': '10 26', ...NSS }));
		const arrow = (x0: number, x1: number, y: number) => `M${x0} ${y}H${x1 + 10}M${x1 + 14} ${y - 6}L${x1} ${y}L${x1 + 14} ${y + 6}`;
		const flowArrows = path(flowG, 'hydrogen', { d: arrow(110, 22, tubeY[0] + 52) + arrow(1134, 1040, tubeY[1] - 30), fill: 'none', ...NSS });
		const flowHit = path(flowG, 'hydrogen', { d: arrow(110, 22, tubeY[0] + 52) + arrow(1134, 1040, tubeY[1] - 30), fill: 'none', stroke: 'transparent', 'stroke-width': 14, ...NSS });
		const leader = path(root, null, { fill: 'none', 'stroke-dasharray': '3 4', 'pointer-events': 'none' });

		// ---------------------------------------------------------------------------- 3D boxes
		interface Box {
			g: SVGGElement;
			faces: SVGPathElement[]; // -X +X -Y +Y -Z +Z
			extra?: SVGPathElement;
		}
		const FACES: [number[], V3][] = [
			[[0, 2, 6, 4], [-1, 0, 0]],
			[[1, 5, 7, 3], [1, 0, 0]],
			[[0, 4, 5, 1], [0, -1, 0]],
			[[2, 3, 7, 6], [0, 1, 0]],
			[[0, 1, 3, 2], [0, 0, -1]],
			[[4, 6, 7, 5], [0, 0, 1]]
		];
		const model = mk('g', root);
		const backG = mk('g', model); // drive, copper, diamond
		const beamBackG = mk('g', model, { 'pointer-events': 'none' });
		const backHitG = mk('g', model);
		const ghost = path(model, null, { fill: 'none', 'stroke-dasharray': '4 4', 'pointer-events': 'none' });
		const chipLayer = mk('g', model);
		const topG = mk('g', model);
		const mkBox = (parent: Element, pid: string, endPick?: string): Box => {
			const g = mk('g', parent);
			const faces = FACES.map((_, i) => path(g, i < 2 && endPick ? endPick : pid));
			return { g, faces };
		};
		const drive = mkBox(backG, 'drive');
		const cu = mkBox(backG, 'cu_block');
		const dia = mkBox(backG, 'diamond');
		const coat = mkBox(backG, 'diamond');
		const chip: Record<SId, Box> = {} as Record<SId, Box>;
		for (const sid of STACK) chip[sid] = mkBox(chipLayer, sid, 'diode');
		chip.substrate.extra = path(chip.substrate.g, 'substrate', { fill: 'none' });
		const inBox = mkBox(topG, 'in_contact');
		const leads = [path(topG, 'drive', { fill: 'none' }), path(topG, 'drive', { fill: 'none' })];
		const facet = path(topG, 'emission', { stroke: 'none' });
		const beamFrontG = mk('g', topG, { 'pointer-events': 'none' });
		const mkBeam = (g: SVGGElement, gi: number) => ({
			soft: path(g, null, { fill: `url(#${id}-beam${gi})`, filter: `url(#${id}-glow)`, stroke: 'none' }),
			core: path(g, null, { fill: `url(#${id}-beam${gi})`, stroke: 'none' })
		});
		const beamBack = mkBeam(beamBackG, 1);
		// spontaneous glow: soft halos at both end faces (no direction), the back one behind the chip
		const haloBack = path(beamBackG, null, { filter: `url(#${id}-haze)`, stroke: 'none' });
		const haloFront = path(beamFrontG, null, { filter: `url(#${id}-haze)`, stroke: 'none' });
		beamBackG.insertBefore(haloBack, beamBackG.firstChild);
		beamFrontG.insertBefore(haloFront, beamFrontG.firstChild);
		const beamFront = mkBeam(beamFrontG, 0);
		const beamHit = [path(topG, 'beam', { fill: 'transparent', stroke: 'none' }), path(backHitG, 'beam', { fill: 'transparent', stroke: 'none' })];
		topG.appendChild(facet); // over the beam hit areas: the end-face band picks the emission part
		const heatG = mk('g', topG);
		const heat = [0, 1, 2].map(() => ({ l: path(heatG, 'heat', { fill: 'none', 'stroke-dasharray': '5 4' }), hd: path(heatG, 'heat'), hit: path(heatG, 'heat', { fill: 'none', stroke: 'transparent', 'stroke-width': 12 }) }));

		// ---------------------------------------------------------------------------- camera
		const AZ = -30;
		const EL = 28;
		const ca = Math.cos(AZ * DEG), sa = Math.sin(AZ * DEG), ce = Math.cos(EL * DEG), se = Math.sin(EL * DEG);
		const VIEW: V3 = [sa * ce, ca * ce, se]; // toward the viewer
		const projRaw = (X: number, Y: number, Z: number): P2 => [X * ca - Y * sa, (X * sa + Y * ca) * se - Z * ce];
		interface Cam {
			s: number;
			ox: number;
			oy: number;
		}
		type Fit = [number, number, number, number, number, number];
		const WX = 200, WY = 70; // wafer piece half plan (illustrative)
		const FIT: Record<string, Fit> = {
			wafer: [-WX, WX, -WY, WY, -2, 72],
			chip: [-210, 210, -60, 60, -30, 80],
			mount: [-330, 330, -300, 170, -114, 150]
		};
		const regions = (): Record<'app' | 'inset' | 'full' | 'plot', Rect> => {
			if (w < 700) {
				const t = Math.min(0.24, 150 / h);
				return { app: [0.03, t, 0.97, 0.5], inset: [0.14, 0.54, 0.86, 0.94], full: [0.05, t + 0.02, 0.95, 0.92], plot: [0.05, t, 0.95, 0.43] };
			}
			const t = Math.min(0.26, 170 / Math.max(1, h));
			return { app: [0.03, t, 0.6, 0.95], inset: [0.63, t + 0.02, 0.985, 0.92], full: [0.08, t, 0.92, 0.94], plot: [0.03, t + 0.02, 0.46, 0.92] };
		};
		const camOf = (rg: Rect, f: Fit): Cam => {
			const rx0 = rg[0] * w, ry0 = rg[1] * h, rw = (rg[2] - rg[0]) * w, rh = (rg[3] - rg[1]) * h;
			let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
			for (const X of [f[0], f[1]]) for (const Y of [f[2], f[3]]) for (const Z of [f[4], f[5]]) {
				const q = projRaw(X, Y, Z);
				x0 = Math.min(x0, q[0]); x1 = Math.max(x1, q[0]); y0 = Math.min(y0, q[1]); y1 = Math.max(y1, q[1]);
			}
			const s = Math.min(rw / (x1 - x0), rh / (y1 - y0));
			return { s, ox: rx0 + rw / 2 - (s * (x0 + x1)) / 2, oy: ry0 + rh / 2 - (s * (y0 + y1)) / 2 };
		};
		const blend = (a: Cam, b: Cam, t: number): Cam =>
			t <= 0 ? a : t >= 1 ? b : { s: Math.exp(lerp(Math.log(a.s), Math.log(b.s), t)), ox: lerp(a.ox, b.ox, t), oy: lerp(a.oy, b.oy, t) };
		let cam: Cam = { s: 1, ox: 0, oy: 0 };
		const P = (X: number, Y: number, Z: number): P2 => [cam.ox + cam.s * (X * ca - Y * sa), cam.oy + cam.s * ((X * sa + Y * ca) * se - Z * ce)];
		const appCam = () => {
			const rg = regions().app;
			const rx0 = rg[0] * w, ry0 = rg[1] * h, rw = (rg[2] - rg[0]) * w, rh = (rg[3] - rg[1]) * h;
			const s = Math.min(rw / FIG_W, rh / (FIG_Y[1] - FIG_Y[0]));
			return { s, ox: rx0 + (rw - s * FIG_W) / 2, oy: ry0 + (rh - s * (FIG_Y[1] - FIG_Y[0])) / 2 - s * FIG_Y[0] };
		};

		// ---------------------------------------------------------------------------- state from p
		interface State {
			app: number; // apparatus opacity
			appIn: number[]; // staged fade-in (tube+heater, bar+seed, holder, thermocouple, gas)
			dx: number; // holder offset, fig px
			active: number; // well over the seed (0..3) or -1
			grow: number[]; // layers 1-4 grown fraction
			zn: number;
			pc: number;
			nc: number;
			inset: number; // stack visible
			camT: [string, string, number]; // shot blend a -> b
			narrow: number; // wafer -> chip plan
			mount: number; // stand-ins in
			flip: number; // 0 grown orientation ... 1 p side down
			lift: number; // chip lift during the flip (drawn units)
			inDrop: number; // In contact (1 = pressed)
			drive: number; // drive stand-in and leads opacity
			light: Light;
		}
		const holderDx = (p: number): [number, number] => {
			// growth chapters: slide to well i, dwell (growth), slide to the next wall
			const chs = ['layer1', 'layer2', 'layer3', 'layer4'];
			if (p < C.layer1[0]) return [dxWall[0], -1];
			for (let i = 0; i < 4; i++) {
				if (p >= C[chs[i]][1]) continue;
				const q = cq(chs[i], p);
				const a = ease(seg(q, 0, 0.2));
				const b = ease(seg(q, 0.8, 1));
				const dx = q < 0.8 ? lerp(dxWall[i], dxWell[i], a) : lerp(dxWell[i], dxWall[i + 1], b);
				return [dx, q >= 0.18 && q <= 0.82 ? i : -1];
			}
			return [dxWall[4], -1];
		};
		const state = (p: number): State => {
			const [dx, active] = holderDx(p);
			const sq = cq('seed', p);
			const chs = ['layer1', 'layer2', 'layer3', 'layer4'];
			const grow = chs.map((c) => (p >= C[c][1] ? 1 : p < C[c][0] ? 0 : seg(cq(c, p), 0.22, 0.78)));
			const tq = cq('contacts', p);
			const dq = cq('diode', p);
			const mq = cq('mount', p);
			const appOut = 1 - ease(seg(tq, 0, 0.3));
			const appIn = [seg(sq, 0, 0.3), seg(sq, 0.12, 0.42), seg(sq, 0.25, 0.55), seg(sq, 0.35, 0.65), seg(sq, 0.45, 0.8)];
			let camT: [string, string, number];
			if (p < C.contacts[0]) camT = ['inset', 'inset', 0];
			else if (p < C.diode[0]) camT = ['inset', 'wafer', ease(seg(tq, 0, 0.3))];
			else if (p < C.mount[0]) camT = ['wafer', 'chip', ease(seg(dq, 0.1, 0.6))];
			else if (p < C.cw[0]) camT = ['chip', 'mount', ease(seg(mq, 0, 0.3))];
			else if (p < C.limit[0]) camT = ['mount', 'plot', ease(seg(cq('cw', p), 0, 0.12))];
			else camT = ['plot', 'mount', ease(seg(cq('limit', p), 0, 0.3))];
			const flip = p < C.mount[0] ? 0 : ease(seg(mq, 0.28, 0.6));
			const lift = p < C.mount[0] ? 0 : 70 * Math.sin(Math.PI * seg(mq, 0.2, 0.72));
			const plotCh = p >= C.cw[0] && p < C.limit[0];
			return {
				app: p < C.contacts[0] ? 1 : appOut,
				appIn,
				dx,
				active,
				grow,
				zn: p < C.contacts[0] ? 0 : ease(seg(tq, 0.32, 0.5)),
				pc: p < C.contacts[0] ? 0 : ease(seg(tq, 0.52, 0.7)),
				nc: p < C.contacts[0] ? 0 : ease(seg(tq, 0.72, 0.9)),
				inset: seg(sq, 0.45, 0.85),
				camT,
				narrow: p < C.diode[0] ? 0 : ease(seg(dq, 0.1, 0.6)),
				mount: p < C.mount[0] ? 0 : ease(seg(mq, 0, 0.25)),
				flip,
				lift,
				inDrop: p < C.mount[0] ? 0 : ease(seg(mq, 0.72, 0.88)),
				drive: p < C.mount[0] ? 0 : seg(mq, 0.86, 1) * (plotCh ? 0.3 : 1),
				light: lightAt(p)
			};
		};

		// ---------------------------------------------------------------------------- drawing helpers
		const pal = () => PAL[theme];
		const on = (pid: string) => hi.includes(pid);
		const hl = (c: string, pid: string) => (on(pid) || (on('diode') && (STACK as readonly string[]).includes(pid)) ? mix(c, pal().accent, 0.5) : c);
		const LDIR: V3 = (() => {
			const v: V3 = [-0.35, 0.5, 0.8];
			const l = Math.hypot(...v);
			return [v[0] / l, v[1] / l, v[2] / l];
		})();
		const dot = (a: V3, b: V3) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
		interface BoxSpec {
			x: P2;
			y: P2;
			z: P2;
			/** rotation about X (rad) around (y = 0, z = zc) and the world Z of that axis */
			th?: number;
			zc?: number;
			zw?: number;
			dz?: number;
		}
		const corners = (b: BoxSpec): V3[] => {
			const th = b.th ?? 0, c = Math.cos(th), s = Math.sin(th);
			const zc = b.zc ?? 0, zw = (b.zw ?? zc) + (b.dz ?? 0);
			const out: V3[] = [];
			for (let i = 0; i < 8; i++) {
				const x = i & 1 ? b.x[1] : b.x[0];
				const y = i & 2 ? b.y[1] : b.y[0];
				const z = (i & 4 ? b.z[1] : b.z[0]) - zc;
				out.push([x, y * c - z * s, zw + y * s + z * c]);
			}
			return out;
		};
		const rotN = (n: V3, th: number): V3 => [n[0], n[1] * Math.cos(th) - n[2] * Math.sin(th), n[1] * Math.sin(th) + n[2] * Math.cos(th)];
		/** draw a box; returns its centre depth (toward the viewer) */
		const drawBox = (bx: Box, b: BoxSpec, col: string, o: number, pid: string, fo = 1): number => {
			if (o < 0.01 || b.z[1] - b.z[0] < 0.02 || b.x[1] - b.x[0] < 0.02) {
				bx.g.style.display = 'none';
				return 0;
			}
			bx.g.style.display = '';
			bx.g.setAttribute('opacity', o >= 0.999 ? '1' : o.toFixed(3));
			const cs = corners(b);
			const sc = cs.map((v) => P(...v));
			const c = pal();
			const base = hl(col, pid);
			const lit = on(pid) || (on('diode') && (STACK as readonly string[]).includes(pid));
			FACES.forEach(([ix, n0], i) => {
				const e = bx.faces[i];
				const n = rotN(n0, b.th ?? 0);
				if (dot(n, VIEW) <= 1e-6) {
					e.style.display = 'none';
					return;
				}
				e.style.display = '';
				const lam = Math.max(0, dot(n, LDIR));
				e.setAttribute('d', dOf(ix.map((j) => sc[j])));
				e.setAttribute('fill', mix(base, c.shade, 0.38 * (1 - lam)));
				e.setAttribute('fill-opacity', fo >= 0.999 ? '1' : fo.toFixed(3));
				e.setAttribute('stroke', lit ? c.accent : mix(col, c.edgeTo, c.edgeMix));
				e.setAttribute('stroke-opacity', (lit ? 0.95 : c.edgeA).toFixed(2));
				e.setAttribute('stroke-width', '0.8');
			});
			const m = cs.reduce((a, v) => [a[0] + v[0] / 8, a[1] + v[1] / 8, a[2] + v[2] / 8] as V3, [0, 0, 0] as V3);
			return dot(m, VIEW);
		};
		const head = (tip: P2, from: P2, size: number): string => {
			const dx = tip[0] - from[0], dy = tip[1] - from[1];
			const l = Math.hypot(dx, dy) || 1;
			const ux = dx / l, uy = dy / l;
			const b: P2 = [tip[0] - ux * size, tip[1] - uy * size];
			return dOf([tip, [b[0] - uy * size * 0.45, b[1] + ux * size * 0.45], [b[0] + uy * size * 0.45, b[1] - ux * size * 0.45]]);
		};

		// stack levels (local z, drawn units) for the current growth / contact state
		const levels = (S: State): Record<SId, P2> => {
			const t = (sid: SId) => TH[sid] * EX;
			const out = {} as Record<SId, P2>;
			let z = 0;
			out.n_contact = [-t('n_contact') * S.nc, 0];
			out.substrate = [0, (z += t('substrate'))];
			const g = (i: number, sid: SId) => {
				const z0 = z;
				z += t(sid) * S.grow[i];
				out[sid] = [z0, z];
			};
			g(0, 'layer_1');
			g(1, 'layer_2');
			g(2, 'layer_3');
			g(3, 'layer_4');
			// Zn skin: top of layer 4 (inside it)
			const zn = Math.min(t('zn_skin') * S.zn, out.layer_4[1] - out.layer_4[0]);
			out.zn_skin = [z - zn, z];
			out.layer_4 = [out.layer_4[0], z - zn];
			out.p_contact = [z, z + t('p_contact') * S.pc];
			return out;
		};
		const ZTOP = (TH.substrate + TH.layer_1 + TH.layer_2 + TH.layer_3 + TH.layer_4 + TH.p_contact) * EX;
		const ZC = (ZTOP - TH.n_contact * EX) / 2; // rotation axis height (local)
		const DIA_T = 24;
		const CU_T = 90;

		let lastS: State | null = null;
		let lastLev: Record<SId, P2> | null = null;
		let lastChip: { hx: number; hy: number; th: number; zw: number; dz: (sid: SId) => number } | null = null;

		// ---------------------------------------------------------------------------- frame
		const frame = (p: number) => {
			const S = state(p);
			lastS = S;
			const c = pal();
			const rg = regions();
			const cams: Record<string, Cam> = {
				inset: camOf(rg.inset, FIT.wafer),
				wafer: camOf(rg.full, FIT.wafer),
				chip: camOf(rg.full, FIT.chip),
				mount: camOf(rg.full, FIT.mount),
				plot: camOf(rg.plot, FIT.mount)
			};
			cam = blend(cams[S.camT[0]], cams[S.camT[1]], S.camT[2]);

			// ------------------------------------------------ apparatus
			if (show(app, S.app)) {
				const A = appCam();
				app.setAttribute('transform', `translate(${f1(A.ox)} ${f1(A.oy)}) scale(${A.s.toFixed(4)})`);
				for (const hb of [hatchBar, hatchHold]) {
					hb.ln.setAttribute('stroke', c.hatch);
					hb.ln.setAttribute('stroke-opacity', '0.45');
				}
				hatchBar.bg.setAttribute('fill', hl(look('seed_holder', c.graphite), 'seed_holder'));
				hatchHold.bg.setAttribute('fill', hl(look('solution_holder', c.graphite2), 'solution_holder'));
				const edge = (pid: string) => (on(pid) ? c.accent : c.ink);
				tubeFill.setAttribute('fill', on('silica_tube') ? c.accent : c.tube);
				tubeFill.setAttribute('fill-opacity', String(on('silica_tube') ? 0.12 : c.tubeA));
				show(tubeFill, S.appIn[0]);
				tubeLines.setAttribute('stroke', edge('silica_tube'));
				tubeLines.setAttribute('stroke-width', on('silica_tube') ? '2' : '1.4');
				show(tubeLines, S.appIn[0]);
				show(tubeHit, S.appIn[0]);
				for (const e of [heaterRod, heaterCoil]) {
					e.setAttribute('stroke', on('aux_heater') ? c.accent : c.heater);
					if (e === heaterRod) e.setAttribute('fill', on('aux_heater') ? c.accent : c.heater);
					e.setAttribute('stroke-width', on('aux_heater') ? '2' : '1.3');
					show(e, S.appIn[0]);
				}
				tcPath.setAttribute('stroke', edge('thermocouple') === c.accent ? c.accent : c.tc);
				tcPath.setAttribute('stroke-width', on('thermocouple') ? '1.8' : '1.1');
				tcDot.setAttribute('fill', on('thermocouple') ? c.accent : c.tc);
				show(tcPath, S.appIn[3]);
				show(tcDot, S.appIn[3]);
				bar.setAttribute('stroke', edge('seed_holder'));
				bar.setAttribute('stroke-width', '1.1');
				stop.setAttribute('fill', hl(c.graphite, 'seed_holder'));
				stop.setAttribute('stroke', edge('seed_holder'));
				show(bar, S.appIn[1]);
				show(stop, S.appIn[1]);
				seedEl.setAttribute('fill', hl(COL.substrate, 'substrate'));
				seedEl.setAttribute('stroke', edge('substrate'));
				seedEl.setAttribute('stroke-width', on('substrate') ? '1.6' : '0.8');
				show(seedG, S.appIn[1]);
				let topCol: string | null = null;
				(['layer_1', 'layer_2', 'layer_3', 'layer_4'] as SId[]).forEach((sid, i) => {
					if (S.grow[i] > 0.05) topCol = COL[sid];
				});
				if (topCol) seedTop.setAttribute('fill', topCol);
				show(seedTop, topCol ? 1 : 0);
				holder.setAttribute('transform', `translate(${f1(S.dx)} 0)`);
				holderTop.setAttribute('transform', `translate(${f1(S.dx)} 0)`);
				for (const e of [...lower, ...walls]) {
					e.setAttribute('stroke', edge('solution_holder'));
					e.setAttribute('stroke-width', '1.1');
					show(e, S.appIn[2]);
				}
				melts.forEach((e, i) => {
					const pid = `solution_${i + 1}`;
					e.setAttribute('fill', hl(c.melt, pid));
					e.setAttribute('fill-opacity', S.active === i ? '0.95' : '0.7');
					e.setAttribute('stroke', on(pid) ? c.accent : mix(c.melt, c.shade, 0.3));
					e.setAttribute('stroke-width', on(pid) ? '1.6' : '0.8');
					show(e, S.appIn[2]);
					waves[i].setAttribute('stroke', mix(c.melt, c.shade, 0.55));
					waves[i].setAttribute('stroke-width', '1');
					show(waves[i], S.appIn[2]);
				});
				rod.setAttribute('d', rectD(prX[0], prY[0], FIG_W + 4 - S.dx, prY[1])); // the rod runs out of the tube
				rod.setAttribute('fill', on('solution_holder') ? c.accent : c.ink);
				show(rod, S.appIn[2]);
				// hydrogen: dashes drift from the push-rod end to the stop end (pure in p)
				const growing = p < C.contacts[0] ? 1 : 0;
				flowLines.forEach((e) => {
					e.setAttribute('stroke', on('hydrogen') ? c.accent : c.inkSoft);
					e.setAttribute('stroke-width', '1');
					e.setAttribute('stroke-dashoffset', f1((p * 9000) % 36));
					show(e, S.appIn[4] * 0.55 * growing);
				});
				flowArrows.setAttribute('stroke', on('hydrogen') ? c.accent : c.ink);
				flowArrows.setAttribute('stroke-width', '1.4');
				show(flowArrows, S.appIn[4]);
				show(flowHit, S.appIn[4]);
			}

			// ------------------------------------------------ stack geometry
			const lev = levels(S);
			lastLev = lev;
			const hx = lerp(WX, CL / 2, S.narrow);
			const hy = lerp(WY, CW / 2, S.narrow);
			const th = Math.PI * S.flip;
			const zw = ZC + S.lift;
			const kk = p >= C.limit[0] ? k : 0;
			const order = [...STACK];
			const dz = (sid: SId) => (kk > 0 ? kk * 9 * (STACK.length - 1 - order.indexOf(sid)) * (S.flip > 0.5 ? 1 : -1) : 0);
			lastChip = { hx, hy, th, zw, dz };
			const stackO = S.inset;
			const depths: [number, Box][] = [];
			for (const sid of STACK) {
				const z = lev[sid];
				const d = drawBox(chip[sid], { x: [-hx, hx], y: [-hy, hy], z, th, zc: ZC, zw, dz: dz(sid) }, COL[sid], stackO, sid);
				depths.push([d, chip[sid]]);
			}
			// painter order inside the chip (stacked slabs: centre depth)
			depths.sort((a, b) => a[0] - b[0]);
			const cur = Array.from(chipLayer.children);
			if (depths.some(([, bx], i) => cur[i] !== bx.g)) for (const [, bx] of depths) chipLayer.appendChild(bx.g);

			// substrate break marks (schematic thickness): zigzags at mid height on its visible side faces
			const brk = chip.substrate.extra!;
			if (stackO > 0.01) {
				const zm = (lev.substrate[0] + lev.substrate[1]) / 2;
				const cs = Math.cos(th), sn = Math.sin(th);
				const W = (x: number, y: number, z: number): P2 => {
					const zz = z - ZC;
					return P(x, y * cs - zz * sn, zw + dz('substrate') + y * sn + zz * cs);
				};
				let d = '';
				const zig = (pt: (u: number, o: number) => P2) => {
					for (const o of [-1.4, 1.4]) {
						const q: P2[] = [];
						for (let i = 0; i <= 12; i++) q.push(pt(i / 12, o + (i % 2 ? 1.4 : -1.4)));
						d += dOf(q, false);
					}
				};
				for (const [n0, f] of [
					[[0, 1, 0] as V3, (u: number, o: number) => W(lerp(-hx, hx, u), hy, zm + o)],
					[[0, -1, 0] as V3, (u: number, o: number) => W(lerp(-hx, hx, u), -hy, zm + o)],
					[[-1, 0, 0] as V3, (u: number, o: number) => W(-hx, lerp(-hy, hy, u), zm + o)]
				] as [V3, (u: number, o: number) => P2][]) {
					if (dot(rotN(n0, th), VIEW) > 1e-6) zig(f);
				}
				brk.setAttribute('d', d);
				brk.setAttribute('stroke', c.ink);
				brk.setAttribute('stroke-width', '1');
				show(brk, 0.6);
			} else show(brk, 0);

			// wafer ghost while the piece narrows to the chip
			const gh = S.narrow > 0 && S.narrow < 1 ? (1 - S.narrow) * 0.8 : 0;
			if (gh > 0.01) {
				const zt = lev.p_contact[1];
				const q = [P(-WX, -WY, zt), P(WX, -WY, zt), P(WX, WY, zt), P(-WX, WY, zt)];
				const q2 = [P(-WX, WY, zt), P(-WX, WY, -2), P(WX, WY, -2), P(WX, WY, zt)];
				ghost.setAttribute('d', dOf(q) + dOf(q2, false));
				ghost.setAttribute('stroke', c.inkSoft);
				ghost.setAttribute('stroke-width', '1');
				show(ghost, gh);
			} else show(ghost, 0);

			// ------------------------------------------------ mount: copper block, diamond, In contact, drive
			const mo = S.mount;
			const kz = (v: number) => kk * v;
			const DX = 250, DY = 110, CX = 330, CY = 170;
			drawBox(cu, { x: [-CX, CX], y: [-CY, CY], z: [-DIA_T - CU_T - kz(40), -DIA_T - kz(40)] }, cCu, mo, 'cu_block');
			drawBox(dia, { x: [-DX, DX], y: [-DY, DY], z: [-DIA_T - kz(14), -1.5 - kz(14)] }, cDiamond, mo, 'diamond', theme === 'light' ? 0.55 : 0.4);
			drawBox(coat, { x: [-DX, DX], y: [-DY, DY], z: [-1.5 - kz(14), -kz(14)] }, '#b8bcc2', mo, 'diamond');
			const DRV: Fit = [-330, -230, -300, -235, -DIA_T - CU_T, -40];
			drawBox(drive, { x: [DRV[0], DRV[1]], y: [DRV[2], DRV[3]], z: [DRV[4], DRV[5]] }, cDrive, S.drive, 'drive');
			const zIn0 = (S.flip > 0.5 ? zw + (ZC - lev.n_contact[0]) : ZTOP) + dz('n_contact');
			const drop = (1 - S.inDrop) * 90 + kz(70);
			drawBox(inBox, { x: [-45, 45], y: [-28, 28], z: [zIn0 + drop, zIn0 + drop + 70] }, cIn, S.inDrop > 0 ? Math.min(1, S.inDrop * 3) : 0, 'in_contact');
			// leads (stand-in): drive -> In contact top, drive -> diamond coating beside the chip
			if (S.drive > 0.01) {
				const zt = zIn0 + drop + 70;
				const a = [P(-300, -268, DRV[5]), P(-300, -268, zt + 40), P(0, 0, zt + 40), P(0, 0, zt)];
				const b = [P(-255, -268, DRV[5]), P(-255, -268, 20), P(-220, -60, 20), P(-220, -60, -kz(14))];
				leads[0].setAttribute('d', dOf(a, false));
				leads[1].setAttribute('d', dOf(b, false));
				for (const e of leads) {
					e.setAttribute('stroke', on('drive') ? c.accent : c.inkSoft);
					e.setAttribute('stroke-width', '1.3');
					show(e, S.drive);
				}
			} else for (const e of leads) show(e, 0);

			// ------------------------------------------------ light: end-face band (layer 2) and beams along X
			const Lt = S.light;
			const zl = (lev.layer_2[0] + lev.layer_2[1]) / 2;
			const cs = Math.cos(th), sn = Math.sin(th);
			const Wd = (x: number, y: number, z: number): P2 => {
				const zz = z - ZC;
				return P(x, y * cs - zz * sn, zw + dz('layer_2') + y * sn + zz * cs);
			};
			const lc = theme === 'light' ? mix(cLight, '#000000', 0.12) : cLight;
			const lit = S.flip > 0.99 && (Lt.glow > 0.003 || Lt.beam > 0.003);
			if (lit) {
				// end-face band (layer 2): spontaneous glow level, brightened by the beam
				facet.setAttribute('d', dOf([Wd(-hx, -hy, lev.layer_2[0]), Wd(-hx, hy, lev.layer_2[0]), Wd(-hx, hy, lev.layer_2[1]), Wd(-hx, -hy, lev.layer_2[1])]));
				facet.setAttribute('fill', on('emission') ? mix(lc, c.accent, 0.4) : c.lightCore);
				show(facet, Math.min(1, 0.15 + 1.2 * Lt.glow + 0.4 * Lt.beam));
				// halos: soft, undirected, scaled by the glow
				const halo = (e: SVGPathElement, sgn: number) => {
					const a0 = Wd(sgn * hx, -hy, zl), a1 = Wd(sgn * hx, hy, zl), m = Wd(sgn * (hx + 14), 0, zl);
					const rx = 0.62 * Math.hypot(a1[0] - a0[0], a1[1] - a0[1]) + 6;
					const ry = rx * 0.55;
					e.setAttribute('d', `M${f1(m[0] - rx)} ${f1(m[1])}a${f1(rx)} ${f1(ry)} 0 1 0 ${f1(2 * rx)} 0a${f1(rx)} ${f1(ry)} 0 1 0 ${f1(-2 * rx)} 0Z`);
					e.setAttribute('fill', on('emission') ? mix(lc, c.accent, 0.4) : lc);
					show(e, Math.min(1, Lt.glow * 1.1) * c.glowA);
				};
				halo(haloFront, -1);
				halo(haloBack, 1);
			} else for (const e of [facet, haloFront, haloBack]) show(e, 0);
			if (lit && Lt.beam > 0.003) {
				const a = Lt.beam;
				const LEN = 140;
				const beams: [number, ReturnType<typeof mkBeam>, number][] = [
					[-1, beamFront, 0],
					[1, beamBack, 1]
				];
				for (const [sgn, bm, gi] of beams) {
					const x0 = sgn * hx, x1 = sgn * (hx + LEN);
					const q = [Wd(x0, -hy, zl), Wd(x1, -hy, zl), Wd(x1, hy, zl), Wd(x0, hy, zl)];
					const d = dOf(q);
					const g0 = Wd(x0, 0, zl), g1 = Wd(x1, 0, zl);
					const gr = beamGrad[gi];
					gr.g.setAttribute('x1', f1(g0[0]));
					gr.g.setAttribute('y1', f1(g0[1]));
					gr.g.setAttribute('x2', f1(g1[0]));
					gr.g.setAttribute('y2', f1(g1[1]));
					for (const st of gr.stops) st.setAttribute('stop-color', on('beam') ? mix(lc, c.accent, 0.4) : lc);
					bm.core.setAttribute('d', d);
					bm.soft.setAttribute('d', d);
					show(bm.core, Math.min(1, 0.15 + 0.85 * a));
					show(bm.soft, a * c.glowA);
					beamHit[gi].setAttribute('d', d);
					show(beamHit[gi], 1);
				}
			} else {
				for (const e of [beamFront.core, beamFront.soft, beamBack.core, beamBack.soft, ...beamHit]) show(e, 0);
			}
			// heat path (illustrative): from the active layer down through the p side, diamond and copper
			const heatO = S.flip > 0.99 && kk < 0.01 ? (Lt.mode === 'limit' ? 0.75 * Lt.beam : Lt.I ? Math.min(1, Lt.I / END[0]) * 0.75 : 0) : 0;
			heat.forEach((hh, i) => {
				if (heatO < 0.01) {
					show(hh.l, 0); show(hh.hd, 0); show(hh.hit, 0);
					return;
				}
				const x = (i - 1) * 110;
				const a = P(x, hy + 6, zw + (zl - ZC) * -1);
				const b = P(x, hy + 6, -DIA_T - 55);
				hh.l.setAttribute('d', dOf([a, b], false));
				hh.l.setAttribute('stroke', on('heat') ? c.accent : c.heat);
				hh.l.setAttribute('stroke-width', '1.4');
				hh.l.setAttribute('stroke-dashoffset', f1(-(p * 4000) % 9));
				hh.hd.setAttribute('d', head(b, a, 7));
				hh.hd.setAttribute('fill', on('heat') ? c.accent : c.heat);
				hh.hit.setAttribute('d', dOf([a, b], false));
				show(hh.l, heatO);
				show(hh.hd, heatO);
				show(hh.hit, 1);
			});

			// ------------------------------------------------ leader from the seed to the inset
			if (S.app > 0.01 && S.inset > 0.01) {
				const A = appCam();
				const a: P2 = [A.ox + A.s * (SEED[2] + 3), A.oy + A.s * (SEED[1] + 3)];
				const b = P(-WX, WY, 15);
				leader.setAttribute('d', dOf([a, b], false));
				leader.setAttribute('stroke', c.inkSoft);
				leader.setAttribute('stroke-width', '1');
				show(leader, Math.min(S.app, S.inset) * 0.8);
			} else show(leader, 0);
		};

		// ---------------------------------------------------------------------------- picking
		const fmtA = (v: number) => `${v.toFixed(3).endsWith('0') ? v.toFixed(2) : v.toFixed(3)} A`;
		const NIR = 'The light is near-infrared (1.446 eV at the 0.80 A peak of Fig. 3, about 0.857 µm, derived); the colour drawn is illustrative.';
		/** state line for the light hovers (beam and end faces) */
		const lightState = (): string[] => {
			const Lt = lastS?.light;
			if (!Lt || Lt.mode === 'off') return [];
			if (Lt.mode === 'li') {
				const atEnd = Lt.I != null && Lt.I >= END[0] - 1e-6;
				return [
					`dc current ${fmtA(Lt.I ?? 0)} (plot pen, Fig. 2, heat sink 297 K); light ${Math.round(Lt.L ?? 0)} arb. units from the digitized dc curve.` +
						(atEnd ? ' This is where the drawn dc curve leaves the scale; the last measured point is 0.833 A.' : ''),
					(Lt.I ?? 0) < IB
						? 'Below the bend: spontaneous emission (broad spectra in Fig. 3 at 0.1 and 0.72 A); glow from the Fig. 2 dc level.'
						: 'Past the bend of the dc curve (about 0.81 A, a figure reading; no threshold is printed for this diode): the beam grows with the light above the bend.'
				];
			}
			if (Lt.mode === 'spectra') {
				const I = Lt.I ?? 0;
				if (I >= 0.795)
					return [
						'0.80 A dc, 295 K: a narrow peak grows out of the broad base (I ≈ 10,000 against 370 at 0.72 A; peak cut off in the paper): threshold.',
						'The single laser line, ≲ 0.5 meV wide with I ≈ 100,000, appears at 0.82 A (not plotted). Fig. 2 (297 K) bends at about 0.81 A. Beam brightness illustrative.'
					];
				return [`${fmtA(I)} dc, 295 K: broad spontaneous spectrum (Fig. 3); glow from the Fig. 2 dc level at this current (297 K).`];
			}
			return [
				'Continuous lasing with the copper block at up to 311 K (abstract; text: diodes lased continuously at 270-311 K).',
				'At 311 K: J_{th} ≈ 3.5 kA/cm^{2} continuous, ≈ 2.0 kA/cm^{2} pulsed (stated); for 370 × 80 µm about 1.04 A continuous (derived), beyond the Fig. 2 range.',
				'The paper does not say which diode reached 311 K; no drive current is shown here.'
			];
		};
		const beamInfo = (): PickInfo => ({
			id: 'beam',
			label: 'Laser light (colour illustrative)',
			detail: [...lightState(), NIR, 'Drawn as a sheet from both uncoated end faces at the thin layer 2; far field and output per face are not given.']
		});
		const INFO: Record<string, () => PickInfo> = {
			beam: beamInfo,
			heat: () => ({
				id: 'heat',
				label: 'Heat path (illustrative)',
				detail: [
					'Heat from the active layer flows through the p side into the diamond and the copper block.',
					'At 297 K the authors estimate the junction ran about 25 K above the copper block (Hayashi et al., Appl. Phys. Lett. 1970, p.110 col. 2).',
					'Arrow strength follows the drawn current (full at 311 K, no current given); not a computed heat flux.'
				]
			}),
			hydrogen: () => ({
				id: 'hydrogen',
				label: 'Hydrogen flow',
				detail: ['Fig. 1: H_{2} in at the push-rod end, out at the stop end. Flow rate not given.', 'Hayashi et al., Appl. Phys. Lett. 1970, Fig. 1 (p.109)']
			})
		};
		const SCHEM = 'Fig. 1 is a schematic section without scale: arrangement only.';
		const partInfo = (pid: string): string | PickInfo => {
			const q = part(pid);
			if (!q) return pid;
			const det: string[] = [];
			if ((STACK as readonly string[]).includes(pid) && !(pid === 'substrate' && (lastS?.app ?? 0) > 0.5 && (lastS?.inset ?? 0) < 0.5)) {
				det.push(DRAWN_NOTE[pid as SId], HEIGHTS_NOTE);
			} else if (['silica_tube', 'aux_heater', 'thermocouple', 'seed_holder', 'solution_holder'].includes(pid)) {
				det.push(SCHEM);
				if (pid === 'seed_holder' || pid === 'solution_holder') det.push('Bar drawn longer than in Fig. 1 so the holder can travel past all four wells before the stop.');
			}
			else if (pid === 'diamond' || pid === 'cu_block' || pid === 'in_contact' || pid === 'drive') det.push('Neutral stand-in: shape and size not given.');
			if (pid === 'emission') det.push(...lightState(), 'Colour drawn is illustrative: the light is near-infrared (about 0.857 µm, derived).');
			if (pid === 'drive') det.push('Leads drawn to the In contact (n side) and to the Cr-Sn film on the diamond (p side): assumed; the paper does not describe the leads.');
			if (pid === 'drive' && lastS?.light.I) det.push(`Now: ${fmtA(lastS.light.I)} dc (plot pen).`);
			return det.length ? { id: pid, label: q.name, detail: det } : pid; // detail lines go under the part tooltip
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
					if (INFO[pid]) return INFO[pid]();
					return partInfo(pid);
				}
				return null;
			},
			anchor(pid) {
				const S = lastS, lev = lastLev, ch = lastChip;
				if (!S || !lev || !ch) return null;
				const below = (q: P2): [number, number] => [Math.max(8, q[0]), q[1] + 18];
				if (pid === 'layer_2') {
					if (S.grow[1] < 0.3 || S.inset < 0.5 || S.flip > 0) return null;
					const z = (lev.layer_2[0] + lev.layer_2[1]) / 2;
					// phone: under the piece (no room beside it)
					if (w < 700) return below(P(-ch.hx * 0.7, ch.hy, lev.n_contact[0]));
					return P(ch.hx, ch.hy, z);
				}
				if (pid === 'diode') {
					if (S.narrow < 0.9 || S.flip > 0) return null;
					if (w < 700) return below(P(-ch.hx * 0.7, ch.hy, lev.n_contact[0]));
					return P(ch.hx, -ch.hy, lev.p_contact[1]); // far end, top: free space to the right
				}
				if (pid === 'cu_block') {
					if (S.mount < 0.5) return null;
					if (w < 700) return below(P(-200, 170, -DIA_T - CU_T));
					return P(330, 170, -DIA_T - 20);
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
