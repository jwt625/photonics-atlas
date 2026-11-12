// Scene module: optical phased array of 31 concentric bent Al2O3 ridge guides (Smit, Electron. Lett. 1988).
// Spec: data/history/showcases/smit1988.yaml. Contract: ../showcase/types.ts. Renderer 2.5D (SVG).
//
// World = the spec's plan frame in micrometres: origin at the common centre of curvature, x right, y up, z up out of
// the wafer (only the substrate stand-in has a drawn thickness). Orientation as in the Fig. 3 photograph: the beam
// enters from the left, the guides turn upward, the light leaves up and to the right.
// Drawn from the paper only: a bare 30 deg sector of 31 concentric arcs (drawn equidistant at the stated 6 um average;
// the true radii are not printed), a broad Gaussian He-Ne beam as a band over the input plane, convergence to the
// focal line 1 mm beyond the output plane. No input guide, no star couplers, no receiver guides (the paper's device
// has none; the prototype's layout is not printed, so it appears only as its stated 1.3 x 4 mm outline, empty).
// Ridge height / layer stack are withheld, so the guides are drawn flat (no extrusion).
// Dispersion chapter: the drawn wavelength is the point under the pen of the derived Eq. (4) plot (+-1 %); the focus
// sits at the plotted position along the focal line, drawn DRAW_X times larger (said in hover); direction derived.
import { AXES_END, staggerK } from '../showcase/plot';
import { clamp01, ease, easeOut, lerp, seg } from '../showcase/progress';
import type { PickInfo, ShowcaseContext, ShowcaseHandle, ShowcaseModule, Theme } from '../showcase/types';

type P2 = [number, number];
type Box4 = [number, number, number, number]; // x0, x1, y0, y1 (plan um)
type Geo = Record<string, unknown>;

const NS = 'http://www.w3.org/2000/svg';
const DEG = Math.PI / 180;
const num = (v: unknown, d: number): number => (typeof v === 'number' && Number.isFinite(v) ? v : d);
const pair = (v: unknown, d: P2): P2 => (Array.isArray(v) && v.length === 2 && v.every((x) => typeof x === 'number' && Number.isFinite(x)) ? [v[0], v[1]] : d);
let uid = 0;

/** focus shift on the model = DRAW_X x the Eq. (4) value (the true +-5.2 um is about 2 px at this scale) */
const DRAW_X = 10;
/** sag of the drawn phase front at the aperture edges, um (true sag for f = 1 mm is about 4 um; drawn larger) */
const SAG = 16;
/** drawn length of the spreading light past the focal line, um (Fig. 3 shows it continuing; it fades out) */
const DIV_L = 380;

// ------------------------------------------------------------------------------------------------ colours
interface Pal {
	sub: string; subFront: string; subSide: string; subA: number; subEdge: string;
	guide: string; guideA: number; white: string; whiteA: number; plane: string; ink: string; inkSoft: string;
	light: string; lightA: number; accent: string; mark: string;
}
const PAL: Record<Theme, Pal> = {
	dark: {
		sub: '#4a4d52', subFront: '#3a3c40', subSide: '#323438', subA: 0.85, subEdge: '#8a8d93',
		guide: '#d8e2ea', guideA: 0.95, white: '#d8e2ea', whiteA: 0.55, plane: '#a8a69d', ink: '#c3c2b7', inkSoft: '#898781',
		light: '#ff3b2f', lightA: 1, accent: '#3987e5', mark: '#9fd0ff'
	},
	light: {
		sub: '#bdb9ae', subFront: '#a29e93', subSide: '#949085', subA: 0.9, subEdge: '#6d6a62',
		guide: '#3d4a56', guideA: 0.95, white: '#6f7d8a', whiteA: 0.6, plane: '#6f6d68', ink: '#52514e', inkSoft: '#6f6d68',
		light: '#d42a1e', lightA: 0.9, accent: '#2a78d6', mark: '#1f5fae'
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

// ------------------------------------------------------------------------------------------------ camera
interface Shot {
	az: number;
	el: number;
	box: Box4;
	z: [number, number];
	region: 'full' | 'plot';
	/** plan points to fit instead of the box (top view only) */
	pts?: P2[];
	/** phone variant of pts (narrow strip between the keyword and the plot) */
	ptsPhone?: P2[];
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
		if (ctx.kind !== '2.5d') throw new Error('smit1988 is a 2.5D scene');
		const { svg, spec } = ctx;
		const id = `pa${++uid}`;
		let w = Math.max(1, ctx.width);
		let h = Math.max(1, ctx.height);
		let theme: Theme = ctx.theme;
		let hi: string[] = [];

		// ---------------------------------------------------------------------------- chapters
		const fallback: Record<string, [number, number]> = {
			arrays: [0, 0.1], bends: [0.1, 0.24], lengths: [0.24, 0.36], phase: [0.36, 0.48], beam: [0.48, 0.6],
			focus: [0.6, 0.74], dispersion: [0.74, 0.87], demux: [0.87, 1]
		};
		const C: Record<string, [number, number]> = {};
		for (const [cid, r] of Object.entries(fallback)) C[cid] = (spec.chapters.find((c) => c.id === cid)?.p ?? r) as [number, number];
		const cq = (cid: string, p: number) => seg(p, C[cid][0], C[cid][1]);
		const inCh = (cid: string, p: number) => p >= C[cid][0] && (p < C[cid][1] || (C[cid][1] >= 1 && p <= 1));

		// ---------------------------------------------------------------------------- geometry from the spec (plan um)
		const geo = (pid: string): Geo => (spec.parts.find((q) => q.id === pid)?.geometry ?? {}) as Geo;
		const ga = geo('array');
		const gr = (ga.radius_um ?? {}) as Geo;
		const NG = Math.max(2, Math.round(num(ga.count, 31)));
		const R0 = num(gr.first, 910);
		const R1 = num(gr.last, 1090);
		const DR = (R1 - R0) / (NG - 1); // drawn equidistant at the stated average (6 um)
		const RW = num(ga.width_um, 3);
		const th = pair(ga.theta_deg, [0, 30]);
		const PSI = (th[1] - th[0]) * DEG;
		const RAD = Array.from({ length: NG }, (_, i) => R0 + DR * i);
		const RM = (R0 + R1) / 2;
		const onArc = (r: number, t: number): P2 => [r * Math.sin(t), -r * Math.cos(t)];
		const E: P2 = [Math.cos(PSI), Math.sin(PSI)]; // exit direction, perpendicular to the output plane
		const U: P2 = [-Math.sin(PSI), Math.cos(PSI)]; // along the output / focal plane, toward the inner (smaller-radius) guides
		const M = onArc(RM, PSI); // output-plane midpoint
		const fpDim = spec.parts.find((q) => q.id === 'focal_plane')?.dims?.find((d) => d.label === 'focal length');
		const F_UM = num(fpDim?.value, 1) * 1000;
		const gf = geo('focal_plane');
		const F0: P2 = pair(gf.through, [M[0] + F_UM * E[0], M[1] + F_UM * E[1]]);
		const FHALF = num(gf.half_length_um, 160);
		const gfo = geo('foci');
		const ORD = num(gfo.spacing_um, 66);
		const gb = geo('he_ne_beam');
		const band = pair(gb.y_band, [-1100, -900]);
		const gs = geo('straight_light');
		const SX1 = num(gs.to_x, 1400);
		const go = geo('other_arrays');
		const PITCH = num(go.pitch_um, 500);
		const COPIES = [1, -1, -2, -3].map((k) => k * PITCH); // one above the excited array, three below (Fig. 3)
		const gp = geo('demux_prototype');
		const pz = pair(gp.size_mm, [4, 1.3]);
		const PW = pz[0] * 1000;
		const PH = pz[1] * 1000;
		// stand-ins (assumed; not in the paper): substrate rectangle and thickness, prototype placement
		const SUB: Box4 = [-420, 1720, -R1 + Math.min(...COPIES) - 210, -80];
		const T = 160;
		const PX0 = -500;
		const PY1 = -1760;
		const PROTO: Box4 = [PX0, PX0 + PW, PY1 - PH, PY1];
		// light: Gaussian across the band (stated "Gaussian"; width not stated: drawn so the band covers the input plane)
		const BC = (band[0] + band[1]) / 2;
		const SIG = 0.35 * Math.abs(band[1] - band[0]);
		const gauss = (y: number) => Math.exp(-0.5 * ((y - BC) / SIG) ** 2);
		const IG = RAD.map((r) => gauss(-r)); // guide i starts at (0, -R_i) on the input plane

		// ---------------------------------------------------------------------------- plot pen (derived Eq. (4) plot)
		/** point of series 0 of the dispersion plot under the pen at chapter progress q: the runtime assembles a plot over the
		 *  first 90 % of its chapter, draws the axes first (AXES_END), then the series; the pen holds at the last point */
		const plotId = spec.chapters.find((c) => c.id === 'dispersion')?.plot ?? 'dispersion';
		const ppts = ((spec.plots?.find((x) => x.id === plotId)?.series?.[0]?.points ?? []) as [number, number][]).filter(
			(q) => Array.isArray(q) && Number.isFinite(q[0]) && Number.isFinite(q[1])
		);
		const pen = (q: number): [number, number] => {
			const N = ppts.length;
			if (!N) return [0, 0];
			const kk = staggerK(seg(q, 0, 0.9), AXES_END, 1, 0, 1);
			const t = Math.max(0, Math.min(N - 1, kk * N - 1));
			const i = Math.floor(t);
			const j = Math.min(N - 1, i + 1);
			return [lerp(ppts[i][0], ppts[j][0], t - i), lerp(ppts[i][1], ppts[j][1], t - i)];
		};
		/** drawn wavelength offset (Dl/l, %) and focus position (um along the focal line, + = inner side) at p */
		const drive = (p: number): { x: number; y: number; onPen: boolean } => {
			if (inCh('dispersion', p)) {
				const q = cq('dispersion', p);
				const [x, y] = pen(q);
				// design point while the axes draw; the first pen frames carry the move to the plotted point
				const qs = 0.9 * AXES_END;
				const b = ease(seg(q, qs, qs + 0.06));
				return { x: lerp(0, x, b), y: lerp(0, y, b), onPen: b >= 1 };
			}
			if (p >= C.demux[0]) {
				const [x, y] = pen(1);
				const b = 1 - ease(seg(cq('demux', p), 0, 0.25));
				return { x: x * b, y: y * b, onPen: false };
			}
			return { x: 0, y: 0, onPen: false };
		};
		const focusAt = (yUm: number): P2 => [F0[0] + DRAW_X * yUm * U[0], F0[1] + DRAW_X * yUm * U[1]];

		// ---------------------------------------------------------------------------- SVG scaffolding
		const mk = <K extends keyof SVGElementTagNameMap>(tag: K, parent: Element, attrs: Record<string, string | number> = {}): SVGElementTagNameMap[K] => {
			const e = document.createElementNS(NS, tag) as SVGElementTagNameMap[K];
			for (const [a, v] of Object.entries(attrs)) e.setAttribute(a, String(v));
			parent.appendChild(e);
			return e;
		};
		type PathEl = SVGPathElement;
		const path = (parent: Element, part: string | null, attrs: Record<string, string | number> = {}): PathEl => {
			const e = mk('path', parent, { 'stroke-linejoin': 'round', 'stroke-linecap': 'round', ...attrs });
			if (part) e.setAttribute('data-pick', part);
			return e;
		};
		const show = (e: SVGElement, o: number) => {
			if (!(o >= 0.01)) {
				if (e.style.display !== 'none') e.style.display = 'none';
				return false;
			}
			if (e.style.display) e.style.display = '';
			e.setAttribute('opacity', o >= 0.999 ? '1' : o.toFixed(3));
			return true;
		};
		const root = mk('g', svg, { 'data-scene': 'phased-array' });
		const defs = mk('defs', root);
		// band profile across y (Gaussian); fans: brighter toward the focus; spots: radial falloff
		const bandG = mk('linearGradient', defs, { id: `${id}-band`, gradientUnits: 'userSpaceOnUse' });
		const BSTOP = 13;
		const bandStops = Array.from({ length: BSTOP }, (_, i) => mk('stop', bandG, { offset: (i / (BSTOP - 1)).toFixed(4), 'stop-color': '#ff3b2f', 'stop-opacity': 0 }));
		const strV = mk('linearGradient', defs, { id: `${id}-strv`, gradientUnits: 'userSpaceOnUse' });
		const strStops = Array.from({ length: BSTOP }, (_, i) => mk('stop', strV, { offset: (i / (BSTOP - 1)).toFixed(4), 'stop-color': '#ff3b2f', 'stop-opacity': 0 }));
		const straightG = mk('linearGradient', defs, { id: `${id}-str`, gradientUnits: 'userSpaceOnUse' });
		[0, 0.7, 1].forEach((o, i) => mk('stop', straightG, { offset: o, 'stop-color': '#ffffff', 'stop-opacity': [1, 0.8, 0][i] }));
		const strMask = mk('mask', defs, { id: `${id}-strm`, maskUnits: 'userSpaceOnUse', x: -1e5, y: -1e5, width: 2e5, height: 2e5 });
		mk('rect', strMask, { x: -1e5, y: -1e5, width: 2e5, height: 2e5, fill: `url(#${id}-str)` });
		const outGrad = (k: number) => {
			const g = mk('linearGradient', defs, { id: `${id}-out${k}`, gradientUnits: 'userSpaceOnUse' });
			return { g, s: [0, 1].map((o) => mk('stop', g, { offset: o, 'stop-color': '#ff3b2f', 'stop-opacity': 0 })) };
		};
		const outG = [outGrad(0), outGrad(1), outGrad(2)];
		const fanGrad = (k: number) => {
			const g = mk('linearGradient', defs, { id: `${id}-fan${k}`, gradientUnits: 'userSpaceOnUse' });
			return { g, s: [0, 1].map((o) => mk('stop', g, { offset: o, 'stop-color': '#ff3b2f', 'stop-opacity': 0 })) };
		};
		const fanG = [fanGrad(0), fanGrad(1), fanGrad(2)];
		const spotG = mk('radialGradient', defs, { id: `${id}-spot` });
		const spotStops = [0, 0.35, 1].map((o) => mk('stop', spotG, { offset: o, 'stop-color': '#ff3b2f', 'stop-opacity': 0 }));

		// substrate stand-in (top face plus two side faces while the view is tilted)
		const gSub = mk('g', root);
		const subFront = path(gSub, 'substrate');
		const subSide = path(gSub, 'substrate');
		const subTop = path(gSub, 'substrate');
		// further arrays and the excited array as pale sectors (the white areas of Fig. 3)
		const gArr = mk('g', root);
		const copies = COPIES.map(() => path(gArr, 'other_arrays'));
		const sector0 = path(gArr, 'array');
		// guides (31 arcs), drawn as strokes; a transparent sector over them is the pick target
		const gArcs = mk('g', root, { fill: 'none', 'stroke-linecap': 'butt' });
		const arcs = RAD.map(() => path(gArcs, null, { fill: 'none', 'stroke-linecap': 'butt' }));
		const arrayHit = path(root, 'array', { fill: 'transparent', stroke: 'none' });
		// inner / outer guide emphasis (lengths chapter)
		const gHl = mk('g', root, { fill: 'none' });
		const hlIn = path(gHl, 'inner_guide', { fill: 'none', 'stroke-linecap': 'butt' });
		const hlOut = path(gHl, 'outer_guide', { fill: 'none', 'stroke-linecap': 'butt' });
		// input / output planes (dash-dot, Fig. 1), their extension to the centre, sector angle arc
		const gPl = mk('g', root, { fill: 'none' });
		const planeIn = path(gPl, null, { fill: 'none', 'stroke-dasharray': '9 3 2 3', 'stroke-linecap': 'butt' });
		const planeOut = path(gPl, null, { fill: 'none', 'stroke-dasharray': '9 3 2 3', 'stroke-linecap': 'butt' });
		const extIn = path(gPl, null, { fill: 'none', 'stroke-dasharray': '9 3 2 3', 'stroke-linecap': 'butt' });
		const extOut = path(gPl, null, { fill: 'none', 'stroke-dasharray': '9 3 2 3', 'stroke-linecap': 'butt' });
		const planeInHit = path(gPl, 'input_plane', { fill: 'none', stroke: 'transparent', 'stroke-width': 10 });
		const planeOutHit = path(gPl, 'output_plane', { fill: 'none', stroke: 'transparent', 'stroke-width': 10 });
		const sectorArc = path(gPl, null, { fill: 'none' });
		const sectorHit = path(gPl, 'sector', { fill: 'none', stroke: 'transparent', 'stroke-width': 12 });
		const centre = mk('circle', gPl, { r: 2.2 });
		// phase front at the output plane (one dot per guide)
		const gTk = mk('g', root);
		const tkLine = path(gTk, null, { fill: 'none', 'pointer-events': 'none' });
		const tkDots = path(gTk, 'phase_front', { stroke: 'none' });
		const tkHit = path(gTk, 'phase_front', { fill: 'none', stroke: 'transparent', 'stroke-width': 12 });
		// light (the faint region outline sits under it)
		const freeReg = path(root, 'free_region', { 'stroke-dasharray': '2 3' });
		const gLt = mk('g', root, { 'pointer-events': 'none' });
		const bandEl = path(gLt, null, { stroke: 'none', fill: `url(#${id}-band)` });
		const strEl = mk('g', gLt);
		const strRect = path(strEl, null, { stroke: 'none', fill: `url(#${id}-strv)`, mask: `url(#${id}-strm)` });
		const gGl = mk('g', gLt, { fill: 'none' });
		const glSoft = RAD.map(() => path(gGl, null, { fill: 'none', 'stroke-linecap': 'butt' }));
		const glCore = RAD.map(() => path(gGl, null, { fill: 'none', 'stroke-linecap': 'butt' }));
		const fans = [0, 1, 2].map((k) => path(gLt, null, { stroke: 'none', fill: `url(#${id}-fan${k})` }));
		// light continues past the focal line and spreads again (Fig. 3), fading out
		const fansOut = [0, 1, 2].map((k) => path(gLt, null, { stroke: 'none', fill: `url(#${id}-out${k})` }));
		const bandHit = path(root, 'he_ne_beam', { fill: 'transparent', stroke: 'none' });
		const strHit = path(root, 'straight_light', { fill: 'transparent', stroke: 'none' });
		const fanHit = [path(root, 'order_neighbour', { fill: 'transparent', stroke: 'none' }), path(root, 'order_neighbour', { fill: 'transparent', stroke: 'none' })];
		// focal line, wavefronts, spots (top)
		const gTop = mk('g', root);
		const focal = path(gTop, null, { fill: 'none', 'stroke-dasharray': '6 4', 'stroke-linecap': 'butt' });
		const focalHit = path(gTop, 'focal_plane', { fill: 'none', stroke: 'transparent', 'stroke-width': 12 });
		const wf = [0, 1, 2].map(() => path(gTop, 'wavefront', { fill: 'none' }));
		const wfHit = [0, 1, 2].map(() => path(gTop, 'wavefront', { fill: 'none', stroke: 'transparent', 'stroke-width': 10 }));
		const spots = [0, 1, 2].map((k) => mk('circle', gTop, { fill: `url(#${id}-spot)`, 'data-pick': k === 0 ? 'foci' : 'order_neighbour' }));
		// prototype outline (empty)
		const proto = path(root, 'demux_prototype', { fill: 'transparent' });

		// ---------------------------------------------------------------------------- camera
		const regions = (): { full: [number, number, number, number]; plot: [number, number, number, number] } => {
			if (w < 700) return { full: [0.05, 0.2, 0.95, 0.95], plot: [0.04, 0.31, 0.96, 0.43] };
			const top = Math.min(0.26, 170 / Math.max(1, h));
			return { full: [0.04, top, 0.96, 0.94], plot: [0.03, top + 0.03, 0.46, 0.92] };
		};
		const FLAT: [number, number] = [0, 0];
		const SHOTS: Record<string, Shot> = {
			arrive: { az: -24, el: 46, box: SUB, z: [-T, 0], region: 'full' },
			column: { az: 0, el: 90, box: SUB, z: FLAT, region: 'full' },
			bends: { az: 0, el: 90, box: [-60, 610, -1130, -760], z: FLAT, region: 'full' },
			lengths: { az: 0, el: 90, box: [-150, 690, -1140, 70], z: FLAT, region: 'full' },
			phase: { az: 0, el: 90, box: [340, 680, -1030, -715], z: FLAT, region: 'full' },
			beam: { az: 0, el: 90, box: [-520, 1460, -1150, -640], z: FLAT, region: 'full' },
			focus: { az: 0, el: 90, box: [-120, 1760, -1140, -60], z: FLAT, region: 'full' },
			// beam axis turned horizontal beside the plot: the focal line runs up the screen, + (inner side) = up, like the plot's y
			disp: {
				az: PSI / DEG, el: 90, box: [0, 0, 0, 0], z: FLAT, region: 'plot',
				pts: [onArc(R0, PSI), onArc(R1, PSI), [M[0] - 130 * E[0], M[1] - 130 * E[1]], [F0[0] + 30 * E[0] + 190 * U[0], F0[1] + 30 * E[1] + 190 * U[1]], [F0[0] + 30 * E[0] - 190 * U[0], F0[1] + 30 * E[1] - 190 * U[1]]],
				ptsPhone: [onArc(R0, PSI), onArc(R1, PSI), [M[0] - 130 * E[0], M[1] - 130 * E[1]], [F0[0] + 30 * E[0] + 80 * U[0], F0[1] + 30 * E[1] + 80 * U[1]], [F0[0] + 30 * E[0] - 80 * U[0], F0[1] + 30 * E[1] - 80 * U[1]]]
			},
			demux: { az: 0, el: 90, box: [PROTO[0] - 60, Math.max(1760, PROTO[1]) + 60, PROTO[2] - 60, -60], z: FLAT, region: 'full' }
		};
		const projRaw = (az: number, el: number, x: number, y: number, z: number): P2 => {
			const ca = Math.cos(az * DEG), sa = Math.sin(az * DEG);
			const X = x, Y = -y;
			return [X * ca - Y * sa, (X * sa + Y * ca) * Math.sin(el * DEG) - z * Math.cos(el * DEG)];
		};
		interface Fit {
			s: number;
			f: [number, number, number]; // world point at the region centre
			c: P2; // region centre (px)
		}
		const fitOf = (sh: Shot): Fit => {
			const rg = regions()[sh.region];
			const rx0 = rg[0] * w, ry0 = rg[1] * h, rw = (rg[2] - rg[0]) * w, rh = (rg[3] - rg[1]) * h;
			let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
			const sp = w < 700 && sh.ptsPhone ? sh.ptsPhone : sh.pts;
			const pts3: [number, number, number][] = sp
				? sp.map((q) => [q[0], q[1], 0])
				: [sh.box[0], sh.box[1]].flatMap((x) => [sh.box[2], sh.box[3]].flatMap((y) => sh.z.map((z) => [x, y, z] as [number, number, number])));
			for (const v of pts3) {
				const q = projRaw(sh.az, sh.el, ...v);
				x0 = Math.min(x0, q[0]); x1 = Math.max(x1, q[0]); y0 = Math.min(y0, q[1]); y1 = Math.max(y1, q[1]);
			}
			const s = Math.min(rw / Math.max(1e-6, x1 - x0), rh / Math.max(1e-6, y1 - y0));
			let f: [number, number, number] = [(sh.box[0] + sh.box[1]) / 2, (sh.box[2] + sh.box[3]) / 2, (sh.z[0] + sh.z[1]) / 2];
			if (sp) {
				// top view: screen = plan rotated (and mirrored in y), its own inverse; centre of the projected extent
				const uc = (x0 + x1) / 2, vc = (y0 + y1) / 2, ca = Math.cos(sh.az * DEG), sa = Math.sin(sh.az * DEG);
				f = [uc * ca + vc * sa, uc * sa - vc * ca, 0];
			}
			return { s, f, c: [rx0 + rw / 2, ry0 + rh / 2] };
		};
		const camBlend = (a: Shot, b: Shot, t: number): Cam => {
			const fa = fitOf(a), fb = fitOf(b);
			const u = clamp01(t);
			const az = lerp(a.az, b.az, u), el = lerp(a.el, b.el, u);
			const s = Math.exp(lerp(Math.log(fa.s), Math.log(fb.s), u));
			const f: [number, number, number] = [lerp(fa.f[0], fb.f[0], u), lerp(fa.f[1], fb.f[1], u), lerp(fa.f[2], fb.f[2], u)];
			const c: P2 = [lerp(fa.c[0], fb.c[0], u), lerp(fa.c[1], fb.c[1], u)];
			const r = projRaw(az, el, ...f);
			return { ca: Math.cos(az * DEG), sa: Math.sin(az * DEG), ce: Math.cos(el * DEG), se: Math.sin(el * DEG), s, ox: c[0] - s * r[0], oy: c[1] - s * r[1] };
		};
		const camAt = (p: number): Cam => {
			const S = SHOTS;
			if (p < C.bends[0]) {
				const q = cq('arrays', p);
				return camBlend(S.arrive, S.column, ease(seg(q, 0.08, 0.6)));
			}
			// the zoom toward the second array opens the bends chapter (the arrays chapter ends on all five)
			if (p < C.lengths[0]) return camBlend(S.column, S.bends, ease(seg(cq('bends', p), 0, 0.3)));
			if (p < C.phase[0]) return camBlend(S.bends, S.lengths, ease(seg(cq('lengths', p), 0, 0.35)));
			if (p < C.beam[0]) return camBlend(S.lengths, S.phase, ease(seg(cq('phase', p), 0, 0.3)));
			if (p < C.focus[0]) return camBlend(S.phase, S.beam, ease(seg(cq('beam', p), 0, 0.3)));
			if (p < C.dispersion[0]) return camBlend(S.beam, S.focus, ease(seg(cq('focus', p), 0, 0.25)));
			if (p < C.demux[0]) return camBlend(S.focus, S.disp, ease(seg(cq('dispersion', p), 0, 0.2)));
			return camBlend(S.disp, S.demux, ease(seg(cq('demux', p), 0, 0.35)));
		};
		let cam: Cam = camAt(0);
		const P = (x: number, y: number, z = 0): P2 => [
			cam.ox + cam.s * (x * cam.ca + y * cam.sa),
			cam.oy + cam.s * ((x * cam.sa - y * cam.ca) * cam.se - z * cam.ce)
		];
		const f1 = (v: number) => (Math.round(v * 10) / 10).toString();
		const dOf = (q: P2[], close = true) => (q.length < 2 ? '' : 'M' + q.map((v) => `${f1(v[0])} ${f1(v[1])}`).join('L') + (close ? 'Z' : ''));
		/** projected arc of radius r from angle t0 to t1 (rad, measured from the input plane) */
		const arcPts = (r: number, t0: number, t1: number, cx = 0, cy = 0): P2[] => {
			const n = Math.max(2, Math.ceil((Math.abs(t1 - t0) / DEG) * 1.2) + 1);
			const out: P2[] = [];
			for (let i = 0; i < n; i++) {
				const t = lerp(t0, t1, i / (n - 1));
				out.push(P(cx + r * Math.sin(t), cy - r * Math.cos(t)));
			}
			return out;
		};
		const sectorPoly = (r0: number, r1: number, dy = 0): P2[] => {
			const a = arcPts(r0, 0, PSI, 0, dy);
			const b = arcPts(r1, PSI, 0, 0, dy);
			return [...a, ...b];
		};

		// ---------------------------------------------------------------------------- state
		interface State {
			sub: number;
			copies: number;
			sector0: number;
			arcT: number[]; // drawn angular extent of each guide (fraction of psi)
			planes: number;
			ext: number; // radial extension of the planes toward the centre (0 none ... 1 to the centre)
			sector: number;
			hlIn: number;
			hlOut: number;
			ticks: number;
			bendT: number;
			bandX: number; // band front x (um); <= -1e3 = no band
			band: number;
			guideT: number; // light front angle (fraction of psi)
			str: number;
			strX: number;
			free: number;
			focal: number;
			fan: number; // central fan front (0 at the output plane ... 1 at the focus)
			spot: number;
			div: number; // light past the focal line (0 none ... 1 full length)
			nb: number; // neighbouring orders
			wf: number;
			proto: number;
			x: number; // drawn wavelength offset (%)
			y: number; // focus position along the focal line (um, Eq. (4); + = inner side)
			onPen: boolean;
		}
		const state = (p: number): State => {
			const qa = cq('arrays', p), qb = cq('bends', p), ql = cq('lengths', p), qp = cq('phase', p), qe = cq('beam', p);
			const qf = cq('focus', p), qd = cq('dispersion', p), qm = cq('demux', p);
			const after = (cid: string) => p >= C[cid][1];
			const before = (cid: string) => p < C[cid][0];
			const arcT = RAD.map((_, i) => {
				if (before('bends')) return 0;
				const a = 0.28 + (0.34 * i) / (NG - 1);
				return ease(seg(qb, a, a + 0.24));
			});
			const dr = drive(p);
			const sec = inCh('lengths', p) ? ease(seg(ql, 0.38, 0.55)) : inCh('phase', p) ? 1 - ease(seg(qp, 0, 0.22)) : 0;
			return {
				sub: before('bends') ? easeOut(seg(qa, 0, 0.3)) : inCh('bends', p) ? 1 - ease(seg(qb, 0, 0.22)) : 0,
				copies: before('bends') ? ease(seg(qa, 0.15, 0.5)) : inCh('bends', p) ? 1 - ease(seg(qb, 0, 0.22)) : 0,
				sector0: before('bends') ? ease(seg(qa, 0.15, 0.5)) : inCh('bends', p) ? 1 - ease(seg(qb, 0.2, 0.5)) : 0,
				arcT,
				planes: before('bends') ? 0 : inCh('bends', p) ? ease(seg(qb, 0.7, 0.9)) : 1,
				ext: inCh('lengths', p) ? ease(seg(ql, 0.12, 0.42)) : inCh('phase', p) ? 1 - ease(seg(qp, 0, 0.22)) : 0,
				sector: sec,
				hlIn: inCh('lengths', p) ? seg(ql, 0.5, 0.6) * (1 - 0.45 * seg(ql, 0.72, 0.8)) : inCh('phase', p) ? 0.55 * (1 - seg(qp, 0, 0.2)) : 0,
				hlOut: inCh('lengths', p) ? seg(ql, 0.72, 0.82) : inCh('phase', p) ? 1 - seg(qp, 0, 0.2) : 0,
				ticks: inCh('phase', p) ? ease(seg(qp, 0.26, 0.4)) : inCh('beam', p) ? 1 - seg(qe, 0, 0.2) : 0,
				bendT: inCh('phase', p) ? ease(seg(qp, 0.55, 0.85)) : inCh('beam', p) ? 1 : 0,
				bandX: before('beam') ? -1e4 : inCh('beam', p) ? lerp(-2400, 0, easeOut(seg(qe, 0.06, 0.34))) : 0,
				band: before('beam') ? 0 : inCh('beam', p) ? seg(qe, 0.04, 0.1) : 1,
				guideT: before('beam') ? 0 : inCh('beam', p) ? seg(qe, 0.34, 0.72) : 1,
				str: before('beam') ? 0 : inCh('beam', p) ? seg(qe, 0.36, 0.42) : inCh('focus', p) ? 1 : inCh('dispersion', p) ? 1 - seg(qd, 0, 0.15) : ease(seg(qm, 0.2, 0.5)),
				strX: before('beam') ? 0 : inCh('beam', p) ? lerp(0, SX1, seg(qe, 0.38, 0.86)) : SX1,
				free: before('focus') ? 0 : inCh('focus', p) ? ease(seg(qf, 0, 0.2)) : 1,
				focal: before('focus') ? 0 : inCh('focus', p) ? ease(seg(qf, 0.04, 0.2)) : 1,
				fan: before('focus') ? 0 : inCh('focus', p) ? ease(seg(qf, 0.12, 0.6)) : 1,
				spot: before('focus') ? 0 : inCh('focus', p) ? seg(qf, 0.5, 0.7) : 1,
				div: before('focus') ? 0 : inCh('focus', p) ? ease(seg(qf, 0.62, 0.9)) : inCh('dispersion', p) ? 1 - seg(qd, 0, 0.12) : ease(seg(qm, 0.3, 0.6)),
				nb: inCh('focus', p) ? ease(seg(qf, 0.66, 0.86)) : inCh('dispersion', p) ? 1 - seg(qd, 0, 0.14) : 0,
				wf: inCh('dispersion', p) ? ease(seg(qd, 0.04, 0.18)) : inCh('demux', p) ? 1 - seg(qm, 0, 0.2) : 0,
				proto: inCh('demux', p) ? ease(seg(qm, 0.32, 0.6)) : 0,
				x: dr.x,
				y: dr.y,
				onPen: dr.onPen
			};
		};

		// ---------------------------------------------------------------------------- frame
		const pal = () => PAL[theme];
		const on = (pid: string) => hi.includes(pid);
		const hl = (c: string, pid: string) => (on(pid) ? mix(c, pal().accent, 0.6) : c);
		let lastS: State | null = null;
		const frame = (p: number) => {
			const c = pal();
			const S = state(p);
			lastS = S;
			cam = camAt(p);
			const s = cam.s;

			// substrate stand-in
			if (show(gSub, S.sub)) {
				const [x0, x1, y0, y1] = SUB;
				const tp = [P(x0, y1), P(x1, y1), P(x1, y0), P(x0, y0)];
				subTop.setAttribute('d', dOf(tp));
				subTop.setAttribute('fill', hl(c.sub, 'substrate'));
				subTop.setAttribute('fill-opacity', String(c.subA));
				subTop.setAttribute('stroke', on('substrate') ? c.accent : c.subEdge);
				subTop.setAttribute('stroke-width', '1');
				subTop.setAttribute('stroke-opacity', '0.6');
				const side = cam.ce > 0.02;
				if (side) {
					subFront.setAttribute('d', dOf([P(x0, y0), P(x1, y0), P(x1, y0, -T), P(x0, y0, -T)]));
					subSide.setAttribute('d', dOf([P(x0, y1), P(x0, y0), P(x0, y0, -T), P(x0, y1, -T)]));
					for (const [e, col] of [[subFront, c.subFront], [subSide, c.subSide]] as const) {
						e.setAttribute('fill', hl(col, 'substrate'));
						e.setAttribute('stroke', c.subEdge);
						e.setAttribute('stroke-opacity', '0.5');
						e.setAttribute('stroke-width', '1');
					}
				}
				show(subFront, side ? 1 : 0);
				show(subSide, side ? 1 : 0);
			}

			// pale sectors: the four further arrays and the excited one
			COPIES.forEach((dy, i) => {
				const e = copies[i];
				if (!show(e, S.copies)) return;
				e.setAttribute('d', dOf(sectorPoly(R0 - RW / 2, R1 + RW / 2, dy)));
				e.setAttribute('fill', hl(c.white, 'other_arrays'));
				e.setAttribute('fill-opacity', String(c.whiteA));
				e.setAttribute('stroke', on('other_arrays') ? c.accent : 'none');
			});
			if (show(sector0, S.sector0)) {
				sector0.setAttribute('d', dOf(sectorPoly(R0 - RW / 2, R1 + RW / 2)));
				sector0.setAttribute('fill', hl(c.white, 'array'));
				sector0.setAttribute('fill-opacity', String(Math.min(1, c.whiteA * 1.25)));
				sector0.setAttribute('stroke', on('array') ? c.accent : 'none');
			}

			// guides: true width (3 um) at the drawn scale, never thinner than a hairline
			const gw = Math.max(0.6, RW * s);
			const anyArc = S.arcT.some((t) => t > 0.001);
			if (show(gArcs, anyArc ? 1 : 0)) {
				const col = hl(c.guide, 'array');
				// at small scales neighbouring strokes merge; thin them so the sector does not read as a solid block
				const ga2 = DR * s < 2.2 ? 0.55 : c.guideA;
				RAD.forEach((r, i) => {
					const e = arcs[i];
					if (!show(e, S.arcT[i] > 0.001 ? ga2 : 0)) return;
					e.setAttribute('d', dOf(arcPts(r, 0, PSI * S.arcT[i]), false));
					e.setAttribute('stroke', col);
					e.setAttribute('stroke-width', f1(gw));
				});
			}
			if (show(arrayHit, S.sector0 > 0.01 || anyArc ? 1 : 0)) arrayHit.setAttribute('d', dOf(sectorPoly(R0 - 6, R1 + 6)));
			arrayHit.setAttribute('pointer-events', S.sector0 > 0.01 || anyArc ? 'all' : 'none');

			// inner / outer guide emphasis
			for (const [e, r, o, pid] of [[hlIn, R0, S.hlIn, 'inner_guide'], [hlOut, R1, S.hlOut, 'outer_guide']] as const) {
				if (!show(e, o)) continue;
				e.setAttribute('d', dOf(arcPts(r, 0, PSI), false));
				e.setAttribute('stroke', on(pid) ? c.accent : c.mark);
				e.setAttribute('stroke-width', f1(Math.max(3, gw * 2.2)));
			}

			// planes (Fig. 1): input plane along x = 0, output plane radial at psi; extended to the centre in the lengths chapter
			const rIn = R0 - 20, rOut = R1 + 20;
			if (show(gPl, Math.max(S.planes, S.sector))) {
				const pc = c.plane;
				const lw = '1.2';
				const seg2 = (e: PathEl, t: number, a: number, b: number, col: string) => {
					e.setAttribute('d', dOf([P(a * Math.sin(t), -a * Math.cos(t)), P(b * Math.sin(t), -b * Math.cos(t))], false));
					e.setAttribute('stroke', col);
					e.setAttribute('stroke-width', lw);
				};
				seg2(planeIn, 0, rIn, rOut, on('input_plane') ? c.accent : pc);
				seg2(planeOut, PSI, rIn, rOut, on('output_plane') ? c.accent : pc);
				show(planeIn, S.planes);
				show(planeOut, S.planes);
				const rc = lerp(rIn, 0, S.ext);
				seg2(extIn, 0, rc, rIn, on('input_plane') ? c.accent : pc);
				seg2(extOut, PSI, rc, rIn, on('output_plane') ? c.accent : pc);
				show(extIn, S.ext > 0.01 ? 0.75 : 0);
				show(extOut, S.ext > 0.01 ? 0.75 : 0);
				const hitIn = [P(0, -rc), P(0, -rOut)];
				planeInHit.setAttribute('d', dOf(hitIn, false));
				planeOutHit.setAttribute('d', dOf([P(rc * Math.sin(PSI), -rc * Math.cos(PSI)), P(rOut * Math.sin(PSI), -rOut * Math.cos(PSI))], false));
				show(planeInHit, S.planes);
				show(planeOutHit, S.planes);
				// sector angle at the centre of curvature
				const ra = 170;
				if (show(sectorArc, S.sector)) {
					sectorArc.setAttribute('d', dOf(arcPts(ra, 0, PSI * S.sector), false));
					sectorArc.setAttribute('stroke', on('sector') ? c.accent : c.ink);
					sectorArc.setAttribute('stroke-width', '1.4');
					sectorHit.setAttribute('d', dOf(arcPts(ra, 0, PSI), false));
				}
				show(sectorHit, S.sector > 0.5 ? 1 : 0);
				const o0 = P(0, 0);
				centre.setAttribute('cx', f1(o0[0]));
				centre.setAttribute('cy', f1(o0[1]));
				centre.setAttribute('fill', c.ink);
				show(centre, S.ext > 0.95 ? S.sector : 0);
			}

			// phase front just past the output plane: aligned (Eq. (2)), then quadratic (Eq. (3)), curvature drawn larger
			if (show(gTk, S.ticks)) {
				const base = 12;
				const half = (R1 - R0) / 2;
				const q: P2[] = RAD.map((r) => {
					const sd = (r - RM) / half;
					const d = base + SAG * S.bendT * sd * sd;
					const o = onArc(r, PSI);
					return P(o[0] + d * E[0], o[1] + d * E[1]);
				});
				tkLine.setAttribute('d', dOf(q, false));
				tkLine.setAttribute('stroke', on('phase_front') ? c.accent : c.ink);
				tkLine.setAttribute('stroke-width', '1');
				tkLine.setAttribute('stroke-opacity', '0.6');
				const rr = Math.max(1.4, Math.min(3.2, 1.1 * s));
				tkDots.setAttribute('d', q.map((v) => `M${f1(v[0] - rr)} ${f1(v[1])}a${f1(rr)} ${f1(rr)} 0 1 0 ${f1(2 * rr)} 0a${f1(rr)} ${f1(rr)} 0 1 0 ${f1(-2 * rr)} 0`).join(''));
				tkDots.setAttribute('fill', on('phase_front') ? c.accent : c.ink);
				tkHit.setAttribute('d', dOf(q, false));
			}

			// light colours
			const lc = on('he_ne_beam') || on('straight_light') ? mix(c.light, c.accent, 0.35) : c.light;
			for (const st of [...bandStops, ...strStops, ...spotStops, ...fanG.flatMap((g) => g.s)]) st.setAttribute('stop-color', c.light);

			// broad beam: band from the left onto the input plane, Gaussian across
			if (show(bandEl, S.band)) {
				const ya = band[0] - 90, yb = band[1] + 90;
				const xl = S.bandX - 6000;
				bandEl.setAttribute('d', dOf([P(xl, ya), P(S.bandX, ya), P(S.bandX, yb), P(xl, yb)]));
				const a = P(0, ya), b = P(0, yb);
				bandG.setAttribute('x1', f1(a[0])); bandG.setAttribute('y1', f1(a[1]));
				bandG.setAttribute('x2', f1(b[0])); bandG.setAttribute('y2', f1(b[1]));
				bandStops.forEach((st, i) => {
					st.setAttribute('stop-color', lc);
					st.setAttribute('stop-opacity', (0.5 * c.lightA * gauss(lerp(ya, yb, i / (BSTOP - 1)))).toFixed(3));
				});
				bandHit.setAttribute('d', dOf([P(xl, band[0]), P(S.bandX, band[0]), P(S.bandX, band[1]), P(xl, band[1])]));
				show(bandHit, 1);
			} else show(bandHit, 0);
			// light that misses the guides runs straight on (faint; fraction not stated); fades out toward its end
			if (show(strEl, S.str * (S.strX > 1 ? 1 : 0))) {
				const a = P(0, BC), b = P(SX1, BC);
				straightG.setAttribute('x1', f1(a[0])); straightG.setAttribute('y1', f1(a[1]));
				straightG.setAttribute('x2', f1(b[0])); straightG.setAttribute('y2', f1(b[1]));
				const base = theme === 'light' ? 0.3 : 0.25;
				const ya = band[0] - 90, yb = band[1] + 90;
				const va = P(0, ya), vb = P(0, yb);
				strV.setAttribute('x1', f1(va[0])); strV.setAttribute('y1', f1(va[1]));
				strV.setAttribute('x2', f1(vb[0])); strV.setAttribute('y2', f1(vb[1]));
				strStops.forEach((st, i) => {
					st.setAttribute('stop-color', lc);
					st.setAttribute('stop-opacity', (base * gauss(lerp(ya, yb, i / (BSTOP - 1)))).toFixed(3));
				});
				strRect.setAttribute('d', dOf([P(0, ya), P(S.strX, ya), P(S.strX, yb), P(0, yb)]));
				strHit.setAttribute('d', dOf([P(0, band[0]), P(S.strX, band[0]), P(S.strX, band[1]), P(0, band[1])]));
				show(strHit, 1);
			} else show(strHit, 0);
			// light in the guides: runs along every arc from the input to the output plane, Gaussian weight per guide
			if (show(gGl, S.guideT > 0.001 ? 1 : 0)) {
				const t1 = PSI * S.guideT;
				RAD.forEach((r, i) => {
					const d = dOf(arcPts(r, 0, t1), false);
					glCore[i].setAttribute('d', d);
					glSoft[i].setAttribute('d', d);
					glCore[i].setAttribute('stroke', lc);
					glSoft[i].setAttribute('stroke', lc);
					glCore[i].setAttribute('stroke-width', f1(Math.max(0.8, gw * 0.8)));
					glSoft[i].setAttribute('stroke-width', f1(Math.max(2, gw * 2.6)));
					show(glCore[i], c.lightA * (0.35 + 0.65 * IG[i]));
					show(glSoft[i], 0.22 * c.lightA * IG[i]);
				});
			}

			// region beyond the output plane (faint outline: support of the converging beams)
			const A = onArc(R0, PSI), B = onArc(R1, PSI);
			// phone: during the dispersion chapter the model sits in a narrow strip above the plot; focal line drawn shorter
			const shrink = w < 700 ? 1 - 0.5 * (inCh('dispersion', p) ? ease(seg(cq('dispersion', p), 0, 0.2)) : inCh('demux', p) ? 1 - ease(seg(cq('demux', p), 0, 0.3)) : 0) : 1;
			if (show(freeReg, S.free)) {
				const fa: P2 = [F0[0] + 150 * shrink * U[0], F0[1] + 150 * shrink * U[1]], fb: P2 = [F0[0] - 150 * shrink * U[0], F0[1] - 150 * shrink * U[1]];
				freeReg.setAttribute('d', dOf([P(...A), P(...fa), P(...fb), P(...B)]));
				freeReg.setAttribute('fill', hl(c.white, 'free_region'));
				freeReg.setAttribute('fill-opacity', theme === 'light' ? '0.07' : '0.035');
				freeReg.setAttribute('stroke', on('free_region') ? c.accent : c.inkSoft);
				freeReg.setAttribute('stroke-opacity', '0.5');
				freeReg.setAttribute('stroke-width', '1');
			}

			// converging beams: central order to the (driven) focus, neighbouring orders 66 um either side (illustrative)
			const Fc = focusAt(S.y);
			const foci: P2[] = [Fc, [Fc[0] + ORD * U[0], Fc[1] + ORD * U[1]], [Fc[0] - ORD * U[0], Fc[1] - ORD * U[1]]];
			const fanO = [0.62, 0.22, 0.22];
			foci.forEach((F, k) => {
				const e = fans[k];
				const t = k === 0 ? S.fan : S.nb > 0.01 ? 1 : 0;
				const o = k === 0 ? 1 : S.nb;
				if (!show(e, t > 0.001 ? o * c.lightA : 0)) {
					if (k > 0) show(fanHit[k - 1], 0);
					return;
				}
				const ta: P2 = [lerp(A[0], F[0], t), lerp(A[1], F[1], t)], tb: P2 = [lerp(B[0], F[0], t), lerp(B[1], F[1], t)];
				const poly = t >= 0.999 ? [P(...A), P(...F), P(...B)] : [P(...A), P(...ta), P(...tb), P(...B)];
				e.setAttribute('d', dOf(poly));
				const a = P(...M), b = P(...F);
				const g = fanG[k];
				g.g.setAttribute('x1', f1(a[0])); g.g.setAttribute('y1', f1(a[1]));
				g.g.setAttribute('x2', f1(b[0])); g.g.setAttribute('y2', f1(b[1]));
				g.s[0].setAttribute('stop-opacity', (fanO[k] * 0.35).toFixed(3));
				g.s[1].setAttribute('stop-opacity', (fanO[k] * (on(k === 0 ? 'free_region' : 'order_neighbour') ? 1.3 : 1)).toFixed(3));
				g.s.forEach((st) => st.setAttribute('stop-color', k === 0 ? lc : on('order_neighbour') ? mix(c.light, c.accent, 0.35) : c.light));
				if (k > 0) {
					fanHit[k - 1].setAttribute('d', dOf([P(...A), P(...F), P(...B)]));
					show(fanHit[k - 1], S.nb > 0.5 ? 1 : 0);
				}
			});
			// past the focal line: the same edges carry on and spread, fainter, fading out over DIV_L (Fig. 3)
			foci.forEach((F, k) => {
				const e = fansOut[k];
				const o = (k === 0 ? 1 : S.nb) * S.div;
				if (!show(e, o * c.lightA)) return;
				const L = DIV_L * S.div;
				const dA = Math.hypot(F[0] - A[0], F[1] - A[1]), dB = Math.hypot(F[0] - B[0], F[1] - B[1]);
				const a2: P2 = [F[0] + ((F[0] - A[0]) / dA) * L, F[1] + ((F[1] - A[1]) / dA) * L];
				const b2: P2 = [F[0] + ((F[0] - B[0]) / dB) * L, F[1] + ((F[1] - B[1]) / dB) * L];
				e.setAttribute('d', dOf([P(...F), P(...a2), P(...b2)]));
				const dm = Math.hypot(F[0] - M[0], F[1] - M[1]);
				const end: P2 = [F[0] + ((F[0] - M[0]) / dm) * L, F[1] + ((F[1] - M[1]) / dm) * L];
				const a = P(...F), b = P(...end);
				const g = outG[k];
				g.g.setAttribute('x1', f1(a[0])); g.g.setAttribute('y1', f1(a[1]));
				g.g.setAttribute('x2', f1(b[0])); g.g.setAttribute('y2', f1(b[1]));
				g.s[0].setAttribute('stop-opacity', (fanO[k] * 0.55).toFixed(3));
				g.s[1].setAttribute('stop-opacity', '0');
				g.s.forEach((st) => st.setAttribute('stop-color', k === 0 ? lc : c.light));
			});

			// focal line (dashed, Fig. 3 design position)
			if (show(focal, S.focal)) {
				const fh = FHALF * shrink;
				const a: P2 = [F0[0] - fh * U[0], F0[1] - fh * U[1]], b: P2 = [F0[0] + fh * U[0], F0[1] + fh * U[1]];
				const d = dOf([P(...a), P(...b)], false);
				focal.setAttribute('d', d);
				focalHit.setAttribute('d', d);
				focal.setAttribute('stroke', on('focal_plane') ? c.accent : c.ink);
				focal.setAttribute('stroke-width', '1.2');
			}
			show(focalHit, S.focal > 0.5 ? 1 : 0);

			// wavefronts (Fig. 2): arcs centred on the current focus; they tilt as the focus moves
			wf.forEach((e, i) => {
				const hit = wfHit[i];
				if (!show(e, S.wf * (0.9 - 0.2 * i))) return show(hit, 0);
				const r0 = Math.hypot(M[0] - Fc[0], M[1] - Fc[1]);
				const r = r0 - (70 + 110 * i);
				const aA = Math.atan2(A[1] - Fc[1], A[0] - Fc[0]);
				const aB = Math.atan2(B[1] - Fc[1], B[0] - Fc[0]);
				const q: P2[] = [];
				for (let j = 0; j <= 16; j++) {
					const a = lerp(aA, aB, j / 16);
					q.push(P(Fc[0] + r * Math.cos(a), Fc[1] + r * Math.sin(a)));
				}
				const d = dOf(q, false);
				e.setAttribute('d', d);
				hit.setAttribute('d', d);
				e.setAttribute('stroke', on('wavefront') ? c.accent : c.ink);
				e.setAttribute('stroke-width', '1.3');
				show(hit, S.wf > 0.5 ? 1 : 0);
			});

			// focal spots (spot size not stated: a small glow)
			const rs = Math.max(4, Math.min(13, 16 * s));
			spotStops.forEach((st, i) => {
				st.setAttribute('stop-color', lc);
				st.setAttribute('stop-opacity', String([1, 0.7, 0][i] * c.lightA));
			});
			foci.forEach((F, k) => {
				const e = spots[k];
				const o = k === 0 ? S.spot : S.nb * 0.5;
				if (!show(e, o)) return;
				const q = P(...F);
				e.setAttribute('cx', f1(q[0]));
				e.setAttribute('cy', f1(q[1]));
				e.setAttribute('r', f1(k === 0 ? rs : rs * 0.8));
				const pid = k === 0 ? (inCh('dispersion', p) ? 'focus_now' : 'foci') : 'order_neighbour';
				e.setAttribute('data-pick', pid);
				e.setAttribute('stroke', on(pid) || (k === 0 && on('foci')) ? c.accent : 'none');
				e.setAttribute('stroke-width', '1.2');
			});

			// demultiplexer prototype: stated 1.3 x 4 mm outline only, interior empty (layout not printed)
			if (show(proto, S.proto)) {
				const [x0, x1, y0, y1] = PROTO;
				proto.setAttribute('d', dOf([P(x0, y1), P(x1, y1), P(x1, y0), P(x0, y0)]));
				proto.setAttribute('stroke', on('demux_prototype') ? c.accent : c.ink);
				proto.setAttribute('stroke-width', on('demux_prototype') ? '1.6' : '1.2');
			}
		};

		// ---------------------------------------------------------------------------- picking
		const pctTxt = (v: number) => `${v >= 0 ? '+' : '−'}${Math.abs(v).toFixed(2)} %`;
		const umTxt = (v: number) => `${v >= 0 ? '+' : '−'}${Math.abs(v).toFixed(1)} µm`;
		const lenOf = (r: number) => Math.round(PSI * r);
		const INFO = (pid: string): PickInfo | null => {
			if (pid === 'inner_guide')
				return {
					id: pid,
					label: 'Innermost guide',
					detail: [
						`R = ${R0} µm, length ψR ≈ ${lenOf(R0)} µm (derived, Eq. (1)).`,
						'Every guide turns through the same ψ = 30°, so the length grows linearly with the radius.',
						'Smit, Electron. Lett. 1988, p.386 col. 1; Eq. (1), p.385'
					]
				};
			if (pid === 'outer_guide')
				return {
					id: pid,
					label: 'Outermost guide',
					detail: [
						`R = ${R1} µm, length ψR ≈ ${lenOf(R1)} µm (derived, Eq. (1)).`,
						`Average step between neighbours ψΔR ≈ ${(PSI * DR).toFixed(2)} µm (derived).`,
						'Smit, Electron. Lett. 1988, p.386 col. 1; Eq. (1), p.385'
					]
				};
			if (pid === 'phase_front')
				return {
					id: pid,
					label: 'Wavefront leaving the output plane',
					detail: [
						'One dot per guide. First aligned (Eq. (2)), then a quadratic phase profile Φ(R_{i}) (Eq. (3)) that focuses.',
						'Schematic: the letter prints no phase values; sag drawn about 4× larger (true ≈ 4 µm for f = 1 mm, derived).',
						'The radii that set these phases are not printed; the guides are drawn equidistant at the stated 6 µm average.',
						'Smit, Electron. Lett. 1988, Eq. (1)-(3), p.385'
					]
				};
			if (pid === 'order_neighbour')
				return {
					id: pid,
					label: 'Neighbouring order (illustrative)',
					detail: [
						'"A number of focused beams": the letter does not say how many orders were seen or how strong they were.',
						'Drawn: one neighbour on each side, 66 µm from the central focus (the stated theoretical spacing; measured "compares well").',
						'Smit, Electron. Lett. 1988, p.386 col. 1; Fig. 3'
					]
				};
			if (pid === 'focus_now') {
				const S = lastS;
				const x = S?.x ?? 0, y = S?.y ?? 0;
				return {
					id: pid,
					label: 'Focus, shifted by wavelength',
					detail: [
						S?.onPen
							? `Δλ/λ = ${pctTxt(x)} (plot pen): ${umTxt(y)} along the focal line.`
							: x === 0
								? 'Design wavelength: focus at the design point.'
								: `Δλ/λ = ${pctTxt(x)}: ${umTxt(y)} along the focal line (moving to the plotted point).`,
						`Computed from Eq. (4) with ψ = 30°, f = 1 mm; drawn ${DRAW_X}× larger. Focal length unchanged (stated).`,
						'Direction derived, not stated: a longer wavelength moves the focus toward the inner, smaller-radius guides.',
						'Smit, Electron. Lett. 1988, p.385 col. 2, Eq. (4); p.386 col. 1'
					]
				};
			}
			return null;
		};

		/** per-part caveats shown under the role in the part tooltip */
		const PART_DETAIL: Record<string, string[]> = {
			array: ['Drawn equidistant at the stated 6 µm average; the individual radii (Eq. (3)) are not printed.'],
			other_arrays: ['Drawn aligned (assumed); in the photograph each array sits about 0.07 mm left of the one above.'],
			he_ne_beam: ['Wavelength as printed; the common He-Ne line is 0.6328 µm.', 'Beam width and launch not stated: drawn as a band over the input plane.'],
			straight_light: ['Fraction not stated; drawn faint.'],
			foci: ['Count and relative strength of the orders not stated; drawn: the central focus and one neighbour each side, 66 µm apart.'],
			wavefront: ['Direction derived, not stated: a longer wavelength moves the focus toward the inner, smaller-radius guides.'],
			demux_prototype: ['Interior empty: its guide count, radii, receiver guides and the five wavelengths are not printed.']
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
					const info = INFO(pid);
					if (info) return info;
					const det = PART_DETAIL[pid];
					const part = spec.parts.find((q) => q.id === pid);
					return det && part ? { id: pid, label: part.name, detail: det } : pid;
				}
				return null;
			},
			anchor(pid) {
				const S = lastS;
				if (!S) return null;
				if (pid === 'array') {
					if (!S.arcT.every((t) => t > 0.98)) return null;
					const o = onArc(R1 + 8, PSI * 0.55);
					return P(o[0], o[1]);
				}
				if (pid === 'sector') {
					if (S.sector < 0.9) return null;
					const o = onArc(185, PSI * 0.5);
					return P(o[0], o[1]);
				}
				if (pid === 'demux_prototype') {
					if (S.proto < 0.9) return null;
					return P(PROTO[0], PROTO[3] + 110);
				}
				if (pid === 'focal_plane') {
					if (S.focal < 0.9) return null;
					return P(F0[0] + FHALF * U[0], F0[1] + FHALF * U[1]);
				}
				return null;
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
