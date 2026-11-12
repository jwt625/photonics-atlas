// Scene module: the prism-film coupler, Tien, Ulrich and Martin, Appl. Phys. Lett. 1969 (DevLog-017).
// Spec: data/history/showcases/tien1969.yaml. Contract: ../showcase/types.ts. Renderer 2.5D (SVG side view).
//
// World units are the pixels of the paper's Fig. 1 crop ("fig1_px", x right, y down), a schematic without scale.
// The prism is rebuilt from the printed values: base angle 26 deg, height 0.5 cm = the drawn 109 px, short vertical
// end faces (22 px, Fig. 1 proportion, assumed). Film and gap are drawn far thicker than to scale (hover says so).
//
// Coordinator rulings (D1015): the prism never moves down; the pointed tool presses substrate and film up against it
// (gap from a drawn rest to the drawn final width). The turntable turns prism, film, substrate, tool and screen
// together about an axis normal to the drawing (pivot: the coupling spot); the laser side (beam, polarizer, optic)
// stays fixed. Rotation amounts are schematic; no coupling angle is printed anywhere.
//
// Rays: refraction at the prism faces uses the index ratio implied by the Fig. 1 drawing (the drawn ray bends at the
// entrance face), only so that the drawn rays stay consistent while the turntable turns; it is not a rutile index and
// is never shown. The Fig. 1 pose is the synchronous pose: there the reflected B3 beam lands on the screen where the
// second m line runs (as drawn). Off-synchronous, the spot sits beside that line; the dark line, the dip of the spot,
// the film glow, the out-coupled rays and the m lines all scale with the overlap of the synchronous direction with the
// beam's angular spread (the spot), so they appear together, only at the synchronous angle and only after pressing.
// Guided power in the film follows the shape of Eq. (6), (7) (build-up over the illuminated length, decay beyond it
// under the prism), without numbers. Everything is a pure function of p.
import { clamp01, ease, lerp, seg } from '../showcase/progress';
import type { PickInfo, ShowcaseContext, ShowcaseHandle, ShowcaseModule, Theme } from '../showcase/types';

type P2 = [number, number];
type Box4 = [number, number, number, number];
type Geo = Record<string, unknown>;

const NS = 'http://www.w3.org/2000/svg';
const DEG = Math.PI / 180;
const num = (v: unknown, d: number): number => (typeof v === 'number' && Number.isFinite(v) ? v : d);
const pt = (v: unknown, d: P2): P2 => (Array.isArray(v) && v.length === 2 && v.every((x) => typeof x === 'number') ? [v[0], v[1]] : d);
const rect4 = (v: unknown, d: Box4): Box4 => (Array.isArray(v) && v.length === 4 && v.every((x) => typeof x === 'number') ? (v as Box4) : d);
const nums = (v: unknown, d: number[]): number[] => (Array.isArray(v) && v.length && v.every((x) => typeof x === 'number') ? (v as number[]) : d);
const f1 = (x: number) => x.toFixed(2);
let uid = 0;

// ------------------------------------------------------------------------------------------------ colours
interface Pal {
	glass: string; glassA: number; glassEdge: string; dot: string;
	film: string; filmA: number; filmEdge: string; hatch: string;
	prism: string; prismA: number; prismEdge: string;
	tool: string; toolEdge: string;
	beam: string; beamCore: string; glowA: number;
	screen: string; field: string; fieldEdge: string; line: string; lineCore: string; spot: string; dark: string;
	ink: string; inkSoft: string; accent: string; optic: string;
}
const PAL: Record<Theme, Pal> = {
	dark: {
		glass: '#cfd8dc', glassA: 0.14, glassEdge: '#9fb0b6', dot: '#cfd8dc',
		film: '#e6c86e', filmA: 0.42, filmEdge: '#e6c86e', hatch: '#e6c86e',
		prism: '#bfe3f2', prismA: 0.12, prismEdge: '#bfe3f2',
		tool: '#6b6b66', toolEdge: '#9a9a93',
		beam: '#ff3b30', beamCore: '#ffb3ad', glowA: 0.85,
		screen: '#d9d6cc', field: '#0b0b0b', fieldEdge: '#6f6d68', line: '#ff5a4f', lineCore: '#ffd9d4', spot: '#ffe6e2', dark: '#0b0b0b',
		ink: '#c3c2b7', inkSoft: '#898781', accent: '#3987e5', optic: '#9aa4ad'
	},
	light: {
		glass: '#7f98a3', glassA: 0.2, glassEdge: '#4f6670', dot: '#4f6670',
		film: '#c9a227', filmA: 0.5, filmEdge: '#8f7212', hatch: '#8f7212',
		prism: '#5fa8c8', prismA: 0.16, prismEdge: '#2f6f8c',
		tool: '#55554f', toolEdge: '#2f2f2b',
		beam: '#d42a1f', beamCore: '#ff6a5f', glowA: 0.45,
		screen: '#6f6d68', field: '#111111', fieldEdge: '#52514e', line: '#ff5a4f', lineCore: '#ffd9d4', spot: '#ffe6e2', dark: '#111111',
		ink: '#52514e', inkSoft: '#6f6d68', accent: '#2a78d6', optic: '#5f6a73'
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

// ------------------------------------------------------------------------------------------------ 2D vector helpers
const add = (a: P2, b: P2): P2 => [a[0] + b[0], a[1] + b[1]];
const sub = (a: P2, b: P2): P2 => [a[0] - b[0], a[1] - b[1]];
const mul = (a: P2, k: number): P2 => [a[0] * k, a[1] * k];
const dot = (a: P2, b: P2) => a[0] * b[0] + a[1] * b[1];
const nrm = (a: P2): P2 => {
	const l = Math.hypot(a[0], a[1]) || 1;
	return [a[0] / l, a[1] / l];
};
const lerp2 = (a: P2, b: P2, t: number): P2 => [lerp(a[0], b[0], t), lerp(a[1], b[1], t)];
/** intersection of ray o + t d (t > 0) with the infinite line through a, b; returns [point, t, s along a->b] */
function hitLine(o: P2, d: P2, a: P2, b: P2): [P2, number, number] | null {
	const e = sub(b, a);
	const den = d[0] * e[1] - d[1] * e[0];
	if (Math.abs(den) < 1e-9) return null;
	const w = sub(a, o);
	const t = (w[0] * e[1] - w[1] * e[0]) / den;
	const s = (w[0] * d[1] - w[1] * d[0]) / den;
	return [add(o, mul(d, t)), t, s];
}
/** refraction of unit d at a surface with unit normal n pointing to the incident side, eta = n_in / n_out */
function refract(d: P2, n: P2, eta: number): P2 | null {
	const ci = -dot(d, n);
	const k = 1 - eta * eta * (1 - ci * ci);
	if (k < 0) return null;
	return nrm(add(mul(d, eta), mul(n, eta * ci - Math.sqrt(k))));
}

// ------------------------------------------------------------------------------------------------ module
const mod: ShowcaseModule = {
	renderer: '2.5d',
	build(ctx: ShowcaseContext): ShowcaseHandle {
		if (ctx.kind !== '2.5d') throw new Error('tien1969 is a 2.5D scene');
		const { svg, spec } = ctx;
		const id = `pfc${++uid}`;
		let w = Math.max(1, ctx.width);
		let h = Math.max(1, ctx.height);
		let theme: Theme = ctx.theme;
		let hi: string[] = [];

		// ---------------------------------------------------------------------------- chapters
		const fallback: Record<string, [number, number]> = {
			substrate: [0, 0.07], film: [0.07, 0.16], prism: [0.16, 0.25], press: [0.25, 0.35], reflect: [0.35, 0.45],
			tunnel: [0.45, 0.57], mlines: [0.57, 0.67], modes: [0.67, 0.85], free: [0.85, 1]
		};
		const C: Record<string, [number, number]> = {};
		for (const [cid, r] of Object.entries(fallback)) C[cid] = (spec.chapters.find((c) => c.id === cid)?.p ?? r) as [number, number];
		const cq = (cid: string, p: number) => seg(p, C[cid][0], C[cid][1]);

		// ---------------------------------------------------------------------------- geometry from the spec (fig1_px)
		const geo = (pid: string): Geo => (spec.parts.find((q) => q.id === pid)?.geometry ?? {}) as Geo;
		const gSub = rect4(geo('substrate').rect, [52, 522, 535, 563]);
		const gFilm = rect4(geo('film').rect, [52, 509.5, 535, 521.5]);
		const gPr = geo('prism');
		const apex = pt(gPr.apex, [320, 391]);
		const BASE = num(gPr.base_y, 499.5);
		const prismDim = (spec.parts.find((q) => q.id === 'prism')?.dims ?? []).find((d) => d.label === 'base angle α');
		const ALPHA = num(prismDim?.value, 26) * DEG;
		const HP = BASE - apex[1]; // drawn prism height (0.5 cm)
		const EF = 22; // end-face height, drawn (Fig. 1 proportion 22 / 109 px, assumed)
		const HB = (HP - EF) / Math.tan(ALPHA); // half base of the sloped faces
		const PX = apex[0];
		const L0: P2 = [PX - HB, BASE]; // left base corner
		const L1: P2 = [PX - HB, BASE - EF]; // top of the left end face
		const R0: P2 = [PX + HB, BASE];
		const R1: P2 = [PX + HB, BASE - EF];
		const CUT: P2 = [PX, BASE]; // 90 deg corner of the half prism
		const PIV: P2 = [PX, BASE]; // turntable pivot (schematic)
		const FILM_T = gFilm[3] - gFilm[1]; // drawn film thickness
		const GAP = gFilm[1] - BASE; // drawn final gap
		const D0 = 34; // drawn rest gap excess before pressing (schematic)
		const gTool = geo('pressure_tool');
		const toolR = rect4(gTool.rect, [300, 560, 338, 648]);
		const toolTip = pt(gTool.tip, [320, 560]);
		const arrowsX = nums(gTool.arrows_x, [283, 357]);
		const gPol = geo('polarizer');
		const pol0 = pt(gPol.from, [88, 341]);
		const pol1 = pt(gPol.to, [64, 420]);
		const gOpt = geo('optic');
		const opt0 = pt(gOpt.top, [120, 350]);
		const opt1 = pt(gOpt.bottom, [97, 418]);
		const gBeam = geo('beam_in');
		const outside = (gBeam.outside ?? {}) as Geo;
		const inside = (gBeam.inside ?? {}) as Geo;
		const band = Array.isArray(outside.from_band) ? (outside.from_band as unknown[]) : [];
		const bandA = pt(band[0], [45, 358]);
		const bandB = pt(band[1], [45, 382]);
		const drawnEntry = pt(inside.from, [253, 424]);
		const drawnSpot = pt(inside.to, [320, 498]);
		const gScr = geo('screen');
		const edge = (gScr.edge_on ?? {}) as Geo;
		const S0 = pt(edge.from, [518, 296]);
		const S1 = pt(edge.to, [776, 553]);
		const SLEN = Math.hypot(S1[0] - S0[0], S1[1] - S0[1]);
		const SDIR = nrm(sub(S1, S0));
		const inset = rect4(((gScr.face_on_inset ?? {}) as Geo).rect, [523, 72, 788, 190]);
		const gM = geo('m_lines');
		const linesX = nums(gM.lines_x, [548, 587, 638, 682, 748]);
		const curved = nums(gM.curved, [638, 682, 748]);
		const spotG = (gM.spot ?? {}) as Geo;
		const spotC = pt(spotG.center, [587, 137]);
		const spotR = num(spotG.r, 16);
		const syncLine = linesX.reduce((b, x, i) => (Math.abs(x - spotC[0]) < Math.abs(linesX[b] - spotC[0]) ? i : b), 0);

		// faces
		const leftFace: [P2, P2] = [L1, apex];
		const rightFace: [P2, P2] = [apex, R1];
		const nLeft: P2 = [-Math.sin(ALPHA), -Math.cos(ALPHA)]; // outward normal, left face
		const nRight: P2 = [Math.sin(ALPHA), -Math.cos(ALPHA)]; // outward normal, right face

		// laser line (world, fixed): centre of the drawn band toward the drawn entry point
		const A0: P2 = lerp2(bandA, bandB, 0.5);
		const D_IN = nrm(sub(drawnEntry, A0));
		// index ratio implied by the drawing (ray bend at the entrance face); keeps the drawn rays consistent, never shown
		const NR = (() => {
			const dIn = nrm(sub(drawnSpot, drawnEntry));
			const si = Math.sqrt(Math.max(0, 1 - dot(D_IN, nLeft) ** 2));
			const sr = Math.sqrt(Math.max(0, 1 - dot(dIn, nLeft) ** 2));
			const n = si / Math.max(1e-6, sr);
			return Number.isFinite(n) && n > 1.2 && n < 4 ? n : 2.6;
		})();

		// rotation (SVG rotate, degrees, about PIV): prism frame -> world
		const rot = (q: P2, a: number): P2 => {
			const c = Math.cos(a * DEG), s = Math.sin(a * DEG);
			const x = q[0] - PIV[0], y = q[1] - PIV[1];
			return [c * x - s * y + PIV[0], s * x + c * y + PIV[1]];
		};
		const rotV = (v: P2, a: number): P2 => {
			const c = Math.cos(a * DEG), s = Math.sin(a * DEG);
			return [c * v[0] - s * v[1], s * v[0] + c * v[1]];
		};

		interface Ray {
			ok: boolean;
			E: P2; // entry on the left face (prism frame)
			B: P2; // hit on the base
			Er: P2; // exit on the right face
			H: P2; // hit on the screen
			u: number; // position along the screen from S0 (px)
			o: P2; // outside direction after the right face
		}
		/** trace the laser line (shifted by dx world px along x) through the turned prism, all in the prism frame */
		const trace = (ang: number, dx: number): Ray => {
			const a = rot(add(A0, [dx, 0]), -ang);
			const d = rotV(D_IN, -ang);
			const bad: Ray = { ok: false, E: drawnEntry, B: drawnSpot, Er: drawnEntry, H: S0, u: 0, o: [1, 0] };
			const he = hitLine(a, d, leftFace[0], leftFace[1]);
			if (!he) return bad;
			const E = he[0];
			const t = refract(d, nLeft, 1 / NR);
			if (!t || t[1] <= 0) return bad;
			const hb = hitLine(E, t, [0, BASE], [1, BASE]);
			if (!hb) return bad;
			const B = hb[0];
			const r: P2 = [t[0], -t[1]];
			const hr = hitLine(B, r, rightFace[0], rightFace[1]);
			if (!hr) return bad;
			const Er = hr[0];
			const o = refract(r, [-nRight[0], -nRight[1]], NR);
			if (!o) return bad;
			const hs = hitLine(Er, o, S0, S1);
			if (!hs) return bad;
			return { ok: true, E, B, Er, H: hs[0], u: hs[2] * SLEN, o };
		};
		const sync = trace(0, 0);
		// face-on view: inset x = x of the screen point (vertical projection, as Fig. 1); the drawn view is shifted so its
		// line through the spot sits over the synchronous B3 hit
		const DXI = (sync.ok ? sync.H[0] : spotC[0]) - spotC[0];
		const insetX = (u: number) => S0[0] + SDIR[0] * u;
		const IN: Box4 = [inset[0] + DXI, inset[1], inset[2] + DXI, inset[3]];
		const LX = linesX.map((x) => x + DXI);
		const uOfX = (x: number) => (x - S0[0]) / SDIR[0];
		const lineU = LX.map(uOfX);
		const SPOT_U = 22; // half width of the B3 band on the screen (px along the screen): spot radius / cos 45 deg, drawn
		// out-coupled rays (synchronous pose): from the coupling spot through the right face onto each m line
		const fan = lineU.map((uT, i) => {
			if (i === syncLine || !sync.ok) return null;
			const th0 = Math.atan2(sync.Er[0] - sync.B[0], sync.B[1] - sync.Er[1]);
			const at = (th: number) => {
				const r: P2 = [Math.sin(th), -Math.cos(th)];
				const hr = hitLine(sync.B, r, rightFace[0], rightFace[1]);
				if (!hr) return null;
				const o = refract(r, [-nRight[0], -nRight[1]], NR);
				if (!o) return null;
				const hs = hitLine(hr[0], o, S0, S1);
				return hs ? { Er: hr[0], H: hs[0], u: hs[2] * SLEN } : null;
			};
			const f = (th: number) => (at(th)?.u ?? NaN) - uT;
			// bracket a sign change among finite samples (steep inside angles reflect totally at the right face)
			let lo = NaN, hiT = NaN;
			for (let k = -120; k < 120; k++) {
				const a = th0 + k * 0.0025, b = a + 0.0025;
				const fa = f(a), fb = f(b);
				if (Number.isFinite(fa) && Number.isFinite(fb) && Math.sign(fa) !== Math.sign(fb)) {
					lo = a;
					hiT = b;
					break;
				}
			}
			if (!Number.isFinite(lo)) return null;
			let flo = f(lo);
			for (let k = 0; k < 50; k++) {
				const m = (lo + hiT) / 2;
				const fm = f(m);
				if (Math.sign(fm) === Math.sign(flo)) {
					lo = m;
					flo = fm;
				} else hiT = m;
			}
			return at((lo + hiT) / 2);
		});

		// turntable: off-synchronous angle (schematic), sign chosen so the spot starts beside the line, inside the screen
		const ANG_OFF = (() => {
			for (const a of [7, -7]) {
				const r = trace(a, 0);
				if (r.ok && r.u > 30 && r.u < SLEN - 30) return a;
			}
			return 7;
		})();
		// half prism: shift of the beam so that the illuminated length ends at the 90 deg corner (x = L)
		const FP = 22; // illuminated length on the base, drawn
		const shiftFree = (() => {
			const want = CUT[0] - FP / 2;
			let dx = 0;
			for (let k = 0; k < 4; k++) {
				const b0 = trace(0, dx).B[0];
				const b1 = trace(0, dx + 1).B[0];
				const g = b1 - b0 || 1;
				dx += (want - b0) / g;
			}
			return dx;
		})();
		const STREAK = 2 * HP; // about 1 cm = two prism heights (both stated)
		const SCRATCH_X = CUT[0] + 0.62 * STREAK; // assumed position along the streak

		// ---------------------------------------------------------------------------- SVG scaffolding
		const mk = <K extends keyof SVGElementTagNameMap>(tag: K, parent: Element, attrs: Record<string, string | number> = {}): SVGElementTagNameMap[K] => {
			const e = document.createElementNS(NS, tag) as SVGElementTagNameMap[K];
			for (const [a, v] of Object.entries(attrs)) e.setAttribute(a, String(v));
			parent.appendChild(e);
			return e;
		};
		const root = mk('g', svg, { 'data-scene': 'prism-film-coupler' });
		const defs = mk('defs', root);
		const glowF = mk('filter', defs, { id: `${id}-glow`, x: '-50%', y: '-50%', width: '200%', height: '200%', 'color-interpolation-filters': 'sRGB' });
		const glowStd = mk('feGaussianBlur', glowF, { stdDeviation: 2.5 });
		// film hatch (Fig. 1 draws the film hatched) and substrate stipple (seeded)
		const hatch = mk('pattern', defs, { id: `${id}-hatch`, patternUnits: 'userSpaceOnUse', width: 7, height: 7, patternTransform: 'rotate(-45)' });
		const hatchLine = mk('line', hatch, { x1: 0, y1: 0, x2: 0, y2: 7, 'stroke-width': 1.1 });
		const stip = mk('pattern', defs, { id: `${id}-stip`, patternUnits: 'userSpaceOnUse', width: 48, height: 24 });
		let seed = 1969;
		const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
		const dots = Array.from({ length: 34 }, () => mk('circle', stip, { cx: f1(rnd() * 48), cy: f1(rnd() * 24), r: f1(0.45 + rnd() * 0.5) }));
		const glowGrad = mk('linearGradient', defs, { id: `${id}-gm`, gradientUnits: 'userSpaceOnUse', x1: 0, y1: 0, x2: 1, y2: 0 });
		const NST = 48;
		const gStops = Array.from({ length: NST }, (_, i) => mk('stop', glowGrad, { offset: (i / (NST - 1)).toFixed(4), 'stop-color': '#ff3b30', 'stop-opacity': 0 }));
		const coreGrad = mk('linearGradient', defs, { id: `${id}-gc`, gradientUnits: 'userSpaceOnUse', x1: 0, y1: 0, x2: 1, y2: 0 });
		const cStops = Array.from({ length: NST }, (_, i) => mk('stop', coreGrad, { offset: (i / (NST - 1)).toFixed(4), 'stop-color': '#ffb3ad', 'stop-opacity': 0 }));
		const spotClip = mk('clipPath', defs, { id: `${id}-spot` });
		const spotClipC = mk('circle', spotClip, { cx: 0, cy: 0, r: spotR });
		const insetClip = mk('clipPath', defs, { id: `${id}-inset` });
		mk('rect', insetClip, { x: IN[0], y: IN[1], width: IN[2] - IN[0], height: IN[3] - IN[1] });

		const cam = mk('g', root);
		const pick = (e: SVGElement, part: string) => {
			e.setAttribute('data-pick', part);
			return e;
		};
		const path = (parent: Element, part: string | null, attrs: Record<string, string | number> = {}): SVGPathElement => {
			const e = mk('path', parent, { 'stroke-linejoin': 'round', 'stroke-linecap': 'round', ...attrs });
			if (part) pick(e, part);
			return e;
		};
		const hitPath = (parent: Element, part: string, wd = 10) => path(parent, part, { fill: 'none', stroke: 'transparent', 'stroke-width': wd });
		const show = (e: SVGElement, o: number) => {
			if (o < 0.01) {
				if (e.style.display !== 'none') e.style.display = 'none';
				return false;
			}
			if (e.style.display) e.style.display = '';
			e.setAttribute('opacity', o >= 0.999 ? '1' : o.toFixed(3));
			return true;
		};
		const dOf = (q: P2[], close = true) => (q.length ? `M${q.map((v) => `${f1(v[0])},${f1(v[1])}`).join('L')}${close ? 'Z' : ''}` : '');

		// layers: turntable arrow (world), assembly (turns), laser side (world), beams (world), face-on view (world)
		const arrowG = mk('g', cam);
		const turnArc = path(arrowG, null, { fill: 'none', 'pointer-events': 'none' });
		const turnHead = path(arrowG, null, { 'pointer-events': 'none' });
		const turnHit = hitPath(arrowG, 'turntable', 12);
		const asm = mk('g', cam);
		const slabG = mk('g', asm);
		const toolG = mk('g', asm);
		const tool = path(toolG, 'pressure_tool');
		const toolArrows = [0, 1].map(() => ({ l: path(toolG, 'pressure_tool', { fill: 'none' }), hd: path(toolG, 'pressure_tool') }));
		const subBody = path(slabG, 'substrate');
		const subDots = path(slabG, 'substrate', { 'pointer-events': 'none' });
		const filmBody = path(slabG, 'film');
		const filmHatch = path(slabG, 'film', { 'pointer-events': 'none' });
		const filmGlowSoft = path(slabG, null, { 'pointer-events': 'none', filter: `url(#${id}-glow)` });
		const filmGlow = path(slabG, null, { 'pointer-events': 'none' });
		const flow = path(slabG, null, { fill: 'none', 'pointer-events': 'none' });
		const glowHit = path(slabG, 'guided_mode', { stroke: 'none', fill: 'transparent' });
		const streakHit = path(slabG, 'streak', { stroke: 'none', fill: 'transparent' });
		const scratch = path(slabG, 'scratch', { fill: 'none' });
		const scratchGlow = mk('circle', slabG, { 'pointer-events': 'none', filter: `url(#${id}-glow)` });
		const scratchHit = mk('circle', slabG, { fill: 'transparent', r: 9 });
		pick(scratchHit, 'scratch');
		const gapHit = path(asm, 'gap', { stroke: 'none', fill: 'transparent' });
		const gapLines = path(asm, null, { fill: 'none', 'pointer-events': 'none', 'stroke-dasharray': '2 3' });
		const prismG = mk('g', asm);
		const prL = path(prismG, 'prism', { stroke: 'none' });
		const prR = path(prismG, 'prism', { stroke: 'none' });
		const prLEdge = path(prismG, null, { fill: 'none', 'pointer-events': 'none' });
		const prREdge = path(prismG, null, { fill: 'none', 'pointer-events': 'none' });
		const prSeam = path(prismG, null, { fill: 'none', 'pointer-events': 'none' });
		const prSeamR = path(prismG, null, { fill: 'none', 'pointer-events': 'none' });
		const dimG = mk('g', prismG);
		const alphaRef = path(dimG, 'prism', { fill: 'none', 'stroke-dasharray': '3 3' });
		const alphaArc = path(dimG, 'prism', { fill: 'none' });
		const heightLine = path(dimG, 'prism', { fill: 'none' });
		const heightHit = hitPath(dimG, 'prism', 9);
		const normalL = path(asm, null, { fill: 'none', 'stroke-dasharray': '4 4', 'pointer-events': 'none' });
		const thetaArc = path(asm, null, { fill: 'none', 'pointer-events': 'none' });
		const normalHit = hitPath(asm, 'theta3', 9);
		const scrG = mk('g', asm);
		const scrBody = path(scrG, 'screen');
		const scrHit = hitPath(scrG, 'screen', 10);
		const laserG = mk('g', cam);
		const polL = path(laserG, 'polarizer', { fill: 'none' });
		const polHit = hitPath(laserG, 'polarizer', 10);
		const optL = path(laserG, 'optic');
		const beamG = mk('g', cam);
		const beamSoftG = mk('g', beamG, { filter: `url(#${id}-glow)`, 'pointer-events': 'none' });
		const beamCoreG = mk('g', beamG, { 'pointer-events': 'none' });
		const mkBeam = () => ({ soft: path(beamSoftG, null), core: path(beamCoreG, null) });
		const bIn = mkBeam(); // outside incident band
		const bIn2 = mkBeam(); // inside, to the base
		const bRe = mkBeam(); // inside, reflected
		const bRe2 = mkBeam(); // outside reflected band (B3)
		const fanB = fan.map(() => mkBeam());
		const hitIn = hitPath(beamG, 'beam_in', 9);
		const hitRe = hitPath(beamG, 'beam_reflected', 9);
		const hitFan = fan.map(() => hitPath(beamG, 'm_lines', 7));
		const insetG = mk('g', cam);
		const projG = mk('g', insetG, { 'pointer-events': 'none' });
		const projL = LX.map(() => path(projG, null, { fill: 'none', 'stroke-dasharray': '4 4' }));
		const projHit = hitPath(insetG, 'projection', 8);
		const fieldR = path(insetG, 'screen');
		const faceG = mk('g', insetG, { 'clip-path': `url(#${id}-inset)` });
		const mSoftG = mk('g', faceG, { filter: `url(#${id}-glow)`, 'pointer-events': 'none' });
		const mCoreG = mk('g', faceG);
		const mSoft = LX.map(() => path(mSoftG, null, { fill: 'none' }));
		const mCore = LX.map(() => path(mCoreG, 'm_lines', { fill: 'none' }));
		const spotSoft = mk('circle', faceG, { 'pointer-events': 'none', filter: `url(#${id}-glow)` });
		const spotCore = mk('circle', faceG);
		pick(spotCore, 'beam_reflected');
		const darkLine = mk('line', faceG, { 'clip-path': `url(#${id}-spot)` });
		pick(darkLine, 'dark_line');
		const darkHit = mk('rect', faceG, { fill: 'transparent' });
		pick(darkHit, 'dark_line');

		// ---------------------------------------------------------------------------- state
		interface State {
			slab: number; slabDx: number; film: number; prism: number; dims: number; tool: number; toolDy: number; D: number;
			arrows: number; gapMark: number; optics: number; screen: number; reveal: number; inset: number; normal: number;
			ang: number; turn: number; turnDir: number; proj: number; half: number; offPeriph: number; shift: number;
			streak: number; scratch: number; prismPick: string; cutK: number;
		}
		const state = (p: number): State => {
			const qS = cq('substrate', p), qF = cq('film', p), qP = cq('prism', p), qPr = cq('press', p);
			const qR = cq('reflect', p), qT = cq('tunnel', p), qM = cq('mlines', p), qFr = cq('free', p);
			const slab = ease(seg(qS, 0, 0.75));
			const rise = ease(seg(qPr, 0.05, 0.4));
			const push = ease(seg(qPr, 0.4, 0.75));
			const set = ease(seg(qR, 0.0, 0.3)); // turntable set off-synchronous before the beam comes on
			const back = ease(seg(qT, 0.08, 0.7)); // turntable back to the synchronous angle
			const ang = ANG_OFF * (set - back);
			const turning = qR > 0 && qR < 0.32 ? 1 : qT > 0.05 && qT < 0.75 ? 1 : 0;
			const half = ease(seg(qFr, 0.1, 0.4));
			return {
				slab,
				slabDx: (1 - slab) * -620,
				film: ease(seg(qF, 0.1, 0.85)),
				prism: ease(seg(qP, 0.05, 0.55)),
				dims: seg(qP, 0.35, 0.7) * (1 - seg(qPr, 0, 0.25)),
				tool: rise,
				toolDy: (1 - rise) * 110,
				D: D0 * (1 - push),
				arrows: seg(qPr, 0.3, 0.45) * (1 - seg(qR, 0, 0.3)),
				gapMark: seg(qPr, 0.72, 0.85) * (1 - seg(qR, 0, 0.3)),
				optics: seg(qR, 0.05, 0.3),
				screen: seg(qR, 0.05, 0.3) * (1 - seg(qFr, 0, 0.1)),
				reveal: seg(qR, 0.32, 0.8),
				inset: seg(qR, 0.75, 0.95) * (1 - seg(qFr, 0, 0.1)),
				normal: seg(qR, 0.6, 0.85) * (1 - seg(qM, 0, 0.3)),
				ang,
				turn: turning,
				turnDir: qT > 0 ? -Math.sign(ANG_OFF) : Math.sign(ANG_OFF),
				proj: seg(qM, 0.15, 0.65) * (1 - seg(qFr, 0, 0.1)),
				half,
				offPeriph: 1 - seg(qFr, 0, 0.1),
				cutK: seg(qFr, 0, 0.1),
				shift: shiftFree * half,
				streak: seg(qFr, 0.4, 0.68),
				scratch: seg(qFr, 0.72, 0.86),
				prismPick: p >= C.free[0] ? 'half_prism' : 'prism'
			};
		};

		// ---------------------------------------------------------------------------- camera
		const regions = (): { full: Box4; plot: Box4 } => {
			if (w < 700) return { full: [0.03, 0.2, 0.97, 0.95], plot: [0.03, 0.17, 0.97, 0.43] };
			const top = Math.min(0.24, 150 / Math.max(1, h));
			return { full: [0.03, top, 0.97, 0.95], plot: [0.02, top + 0.03, 0.47, 0.93] };
		};
		interface Shot {
			box: Box4;
			region: 'full' | 'plot';
		}
		const BUILD: Box4 = [30, 380, 570, 690];
		const FULL: Box4 = [20, 60, 800, 700];
		const SHOT: Record<string, Shot> = {
			substrate: { box: [30, 420, 570, 660], region: 'full' },
			film: { box: [30, 420, 570, 660], region: 'full' },
			prism: { box: BUILD, region: 'full' },
			press: { box: [110, 372, 545, 690], region: 'full' },
			reflect: { box: FULL, region: 'full' },
			tunnel: { box: FULL, region: 'full' },
			mlines: { box: [250, 60, 800, 600], region: 'full' },
			modes: { box: FULL, region: 'plot' },
			free: { box: [20, 318, 600, 700], region: 'full' }
		};
		const ORDER = Object.keys(fallback);
		const fit = (box: Box4, rg: Box4): [number, number, number] => {
			const rx0 = rg[0] * w, ry0 = rg[1] * h, rw = (rg[2] - rg[0]) * w, rh = (rg[3] - rg[1]) * h;
			const s = Math.min(rw / (box[2] - box[0]), rh / (box[3] - box[1]));
			return [s, rx0 + rw / 2 - s * (box[0] + box[2]) / 2, ry0 + rh / 2 - s * (box[1] + box[3]) / 2];
		};
		const camAt = (p: number): [number, number, number] => {
			let i = ORDER.findIndex((cid) => p < C[cid][1]);
			if (i < 0) i = ORDER.length - 1;
			const cur = SHOT[ORDER[i]];
			const prev = SHOT[ORDER[Math.max(0, i - 1)]];
			const t = ease(seg(cq(ORDER[i], p), 0, 0.35));
			const a = fit(prev.box, regions()[prev.region]);
			const b = fit(cur.box, regions()[cur.region]);
			return [Math.exp(lerp(Math.log(a[0]), Math.log(b[0]), t)), lerp(a[1], b[1], t), lerp(a[2], b[2], t)];
		};
		let camNow: [number, number, number] = [1, 0, 0];
		const toPane = (q: P2): [number, number] => [camNow[1] + camNow[0] * q[0], camNow[2] + camNow[0] * q[1]];

		// ---------------------------------------------------------------------------- frame
		const pal = () => PAL[theme];
		const on = (pid: string) => hi.includes(pid);
		const edgeCol = (c: string, pid: string | string[]) => ((Array.isArray(pid) ? pid : [pid]).some(on) ? pal().accent : c);
		const head = (tip: P2, from: P2, size: number): string => {
			const d = nrm(sub(tip, from));
			const n: P2 = [-d[1], d[0]];
			const b = sub(tip, mul(d, size));
			return dOf([tip, add(b, mul(n, size * 0.45)), sub(b, mul(n, size * 0.45))]);
		};
		const setBeam = (bm: { soft: SVGPathElement; core: SVGPathElement }, d: string, wd: number, o: number, fill = false, lit = false) => {
			const c = pal();
			for (const [e, col, sw, a] of [
				[bm.soft, c.beam, wd * 3, o * c.glowA],
				[bm.core, lit ? mix(c.beamCore, c.accent, 0.6) : c.beamCore, wd, o]
			] as const) {
				e.setAttribute('d', d);
				if (fill) {
					e.setAttribute('fill', col);
					e.setAttribute('stroke', 'none');
					e.setAttribute('fill-opacity', e === bm.core ? '0.75' : '0.6');
				} else {
					e.setAttribute('fill', 'none');
					e.setAttribute('stroke', col);
					e.setAttribute('stroke-width', f1(sw));
				}
				show(e, a);
			}
		};
		const hideBeam = (bm: { soft: SVGPathElement; core: SVGPathElement }) => {
			show(bm.soft, 0);
			show(bm.core, 0);
		};
		/** guided power along the film (Eq. (6), (7) shape, no numbers): build-up over [x0, x0 + FP], then decay */
		const A_DEC = 1 / 34;
		const guided = (x: number, x0: number, halfPrism: number, scratchK: number): number => {
			const u = x - x0;
			if (u <= 0) return 0;
			const pk = (1 - Math.exp(-FP / 60)) ** 2;
			if (u <= FP) return (1 - Math.exp(-u / 60)) ** 2 / pk;
			const under = Math.exp(-A_DEC * (u - FP)); // the prism couples the light back out beyond x = L
			const free = x > SCRATCH_X && scratchK > 0 ? (1 - scratchK) : 1;
			const streak = Math.exp(-(x - CUT[0]) / (STREAK * 0.6)) * free; // scattering along the free film
			return lerp(under, x >= CUT[0] ? streak : under, halfPrism);
		};

		let lastS: State | null = null;
		const frame = (p: number) => {
			const c = pal();
			const S = state(p);
			lastS = S;
			camNow = camAt(p);
			const s = camNow[0];
			cam.setAttribute('transform', `matrix(${f1(s)} 0 0 ${f1(s)} ${f1(camNow[1])} ${f1(camNow[2])})`);
			glowStd.setAttribute('stdDeviation', f1(Math.max(1.2, 2.4 / Math.max(0.6, s)) ));
			hatchLine.setAttribute('stroke', c.hatch);
			hatchLine.setAttribute('stroke-opacity', theme === 'light' ? '0.7' : '0.55');
			for (const d of dots) d.setAttribute('fill', c.dot);
			asm.setAttribute('transform', `rotate(${S.ang.toFixed(4)} ${f1(PIV[0])} ${f1(PIV[1])})`);

			// ------------------------------------------------ substrate and film (pressed up by D -> 0)
			const dy = S.D;
			const sx = S.slabDx;
			const subQ: P2[] = [[gSub[0] + sx, gSub[1] + dy], [gSub[2] + sx, gSub[1] + dy], [gSub[2] + sx, gSub[3] + dy], [gSub[0] + sx, gSub[3] + dy]];
			subBody.setAttribute('d', dOf(subQ));
			subBody.setAttribute('fill', c.glass);
			subBody.setAttribute('fill-opacity', String(c.glassA));
			subBody.setAttribute('stroke', edgeCol(c.glassEdge, 'substrate'));
			subBody.setAttribute('stroke-width', f1(on('substrate') ? 2 / s : 1.1 / s));
			subDots.setAttribute('d', dOf(subQ));
			subDots.setAttribute('fill', `url(#${id}-stip)`);
			subDots.setAttribute('fill-opacity', theme === 'light' ? '0.55' : '0.32');
			show(subBody, S.slab);
			show(subDots, S.slab);
			const fTop = gFilm[3] + dy - FILM_T * S.film;
			const filmQ: P2[] = [[gFilm[0] + sx, fTop], [gFilm[2] + sx, fTop], [gFilm[2] + sx, gFilm[3] + dy], [gFilm[0] + sx, gFilm[3] + dy]];
			filmBody.setAttribute('d', dOf(filmQ));
			filmBody.setAttribute('fill', c.film);
			filmBody.setAttribute('fill-opacity', String(c.filmA));
			filmBody.setAttribute('stroke', edgeCol(c.filmEdge, ['film', 'scratch']));
			filmBody.setAttribute('stroke-width', f1(on('film') ? 1.8 / s : 0.9 / s));
			filmHatch.setAttribute('d', dOf(filmQ));
			filmHatch.setAttribute('fill', `url(#${id}-hatch)`);
			show(filmBody, S.film * S.slab);
			show(filmHatch, S.film * S.slab);

			// ------------------------------------------------ pressure tool (rises, then pushes)
			const ty = dy + S.toolDy;
			const tw = (toolR[2] - toolR[0]) / 2;
			const tq: P2[] = [
				[toolTip[0], toolTip[1] + ty],
				[toolTip[0] + tw, toolTip[1] + ty + tw * 1.1],
				[toolTip[0] + tw, toolR[3] + ty],
				[toolTip[0] - tw, toolR[3] + ty],
				[toolTip[0] - tw, toolTip[1] + ty + tw * 1.1]
			];
			tool.setAttribute('d', dOf(tq));
			tool.setAttribute('fill', c.tool);
			tool.setAttribute('stroke', edgeCol(c.toolEdge, 'pressure_tool'));
			tool.setAttribute('stroke-width', f1(1 / s));
			show(tool, S.tool);
			arrowsX.slice(0, 2).forEach((ax, i) => {
				const a: P2 = [ax, toolR[3] + ty - 3];
				const b: P2 = [ax, toolTip[1] + ty + 32];
				const A = toolArrows[i];
				A.l.setAttribute('d', dOf([a, b], false));
				A.l.setAttribute('stroke', edgeCol(c.ink, 'pressure_tool'));
				A.l.setAttribute('stroke-width', f1(1.2 / s));
				A.hd.setAttribute('d', head(b, a, 7));
				A.hd.setAttribute('fill', edgeCol(c.ink, 'pressure_tool'));
				show(A.l, S.arrows);
				show(A.hd, S.arrows);
			});

			// ------------------------------------------------ prism (fixed; never lowered). Two halves for the last chapter
			const onL = on(S.prismPick) || on('prism') || on('half_prism');
			const onR = on('prism') || (S.prismPick === 'prism' && on(S.prismPick));
			const hx = 260 * S.half; // right half slides away to the right
			const rightPoly: P2[] = [[PX + hx, BASE], [PX + hx, apex[1]], [R1[0] + hx, R1[1]], [R0[0] + hx, R0[1]]];
			const leftPoly: P2[] = [L0, L1, apex, CUT];
			prL.setAttribute('d', dOf(leftPoly));
			prR.setAttribute('d', dOf(rightPoly));
			prL.setAttribute('data-pick', S.prismPick);
			for (const [e, o] of [[prL, onL], [prR, onR]] as const) {
				e.setAttribute('fill', o ? mix(c.prism, c.accent, 0.4) : c.prism);
				e.setAttribute('fill-opacity', String(o ? c.prismA * 2 : c.prismA));
			}
			const ec = onL ? c.accent : c.prismEdge;
			const ew = f1((onL ? 2 : 1.2) / s);
			prLEdge.setAttribute('d', dOf([CUT, L0, L1, apex], false));
			prREdge.setAttribute('d', dOf([[PX + hx, apex[1]], [R1[0] + hx, R1[1]], [R0[0] + hx, R0[1]], [PX + hx, BASE]], false));
			prSeam.setAttribute('d', dOf([apex, CUT], false));
			prSeamR.setAttribute('d', dOf([[PX + hx, apex[1]], [PX + hx, BASE]], false));
			for (const e of [prLEdge, prREdge, prSeam, prSeamR]) {
				e.setAttribute('stroke', ec);
				e.setAttribute('stroke-width', ew);
			}
			show(prL, S.prism);
			show(prLEdge, S.prism);
			show(prR, S.prism * (1 - S.half));
			show(prREdge, S.prism * (1 - S.half));
			const split = S.half > 0.002 ? 1 : 0;
			show(prSeam, S.prism * split);
			show(prSeamR, S.prism * split * (1 - S.half));
			// dimension marks: alpha (horizontal reference from the end-face top, arc to the sloped face) and height
			const ar = 46;
			alphaRef.setAttribute('d', dOf([L1, [L1[0] + ar + 12, L1[1]]], false));
			const arc: P2[] = [];
			for (let i = 0; i <= 16; i++) {
				const t = (-ALPHA * i) / 16;
				arc.push([L1[0] + ar * Math.cos(t), L1[1] + ar * Math.sin(t)]);
			}
			alphaArc.setAttribute('d', dOf(arc, false));
			heightLine.setAttribute('d', `${dOf([[PX, apex[1] + 2], [PX, BASE - 1]], false)}${dOf([[PX - 6, apex[1] + 2], [PX + 6, apex[1] + 2]], false)}${dOf([[PX - 6, BASE - 1], [PX + 6, BASE - 1]], false)}`);
			heightHit.setAttribute('d', dOf([[PX, apex[1] + 2], [PX, BASE - 1]], false));
			for (const e of [alphaRef, alphaArc, heightLine]) {
				e.setAttribute('stroke', edgeCol(c.ink, 'prism'));
				e.setAttribute('stroke-width', f1(1 / s));
			}
			show(dimG, S.dims * S.prism);

			// ------------------------------------------------ gap marks (drawn enlarged)
			const gy0 = BASE, gy1 = gFilm[1] + dy;
			gapHit.setAttribute('d', dOf([[L0[0], gy0], [R0[0], gy0], [R0[0], gy1], [L0[0], gy1]]));
			show(gapHit, S.prism * S.film);
			gapLines.setAttribute('d', `${dOf([[R0[0] + 6, gy0], [R0[0] + 26, gy0]], false)}${dOf([[R0[0] + 6, gy1], [R0[0] + 26, gy1]], false)}`);
			gapLines.setAttribute('stroke', edgeCol(c.ink, 'gap'));
			gapLines.setAttribute('stroke-width', f1(1 / s));
			show(gapLines, Math.max(S.gapMark, on('gap') ? S.prism * S.film : 0));

			// ------------------------------------------------ screen (turns with the prism)
			const sn: P2 = [-SDIR[1], SDIR[0]];
			const st = 3;
			scrBody.setAttribute('d', dOf([add(S0, mul(sn, -st)), add(S1, mul(sn, -st)), add(S1, mul(sn, st)), add(S0, mul(sn, st))]));
			scrBody.setAttribute('fill', mix(c.screen, theme === 'light' ? '#ffffff' : '#000000', 0.55));
			scrBody.setAttribute('stroke', edgeCol(c.screen, 'screen'));
			scrBody.setAttribute('stroke-width', f1(1 / s));
			scrHit.setAttribute('d', dOf([S0, S1], false));
			show(scrBody, S.screen);
			show(scrHit, S.screen);

			// ------------------------------------------------ laser side (fixed): polarizer and the unlabelled optic
			polL.setAttribute('d', dOf([pol0, pol1], false));
			polL.setAttribute('stroke', edgeCol(c.optic, 'polarizer'));
			polL.setAttribute('stroke-width', f1(Math.max(2.4, 3 / s)));
			polHit.setAttribute('d', dOf([pol0, pol1], false));
			const om = lerp2(opt0, opt1, 0.5);
			const on2: P2 = nrm([-(opt1[1] - opt0[1]), opt1[0] - opt0[0]]);
			const bulge = 0.16 * Math.hypot(opt1[0] - opt0[0], opt1[1] - opt0[1]);
			const c1 = add(om, mul(on2, bulge * 2)), c2 = add(om, mul(on2, -bulge * 2));
			optL.setAttribute('d', `M${f1(opt0[0])},${f1(opt0[1])}Q${f1(c1[0])},${f1(c1[1])} ${f1(opt1[0])},${f1(opt1[1])}Q${f1(c2[0])},${f1(c2[1])} ${f1(opt0[0])},${f1(opt0[1])}Z`);
			optL.setAttribute('fill', c.optic);
			optL.setAttribute('fill-opacity', '0.08');
			optL.setAttribute('stroke', edgeCol(c.optic, 'optic'));
			optL.setAttribute('stroke-width', f1(1.1 / s));
			show(polL, S.optics);
			show(polHit, S.optics);
			show(optL, S.optics);

			// ------------------------------------------------ rays
			const ray = trace(S.ang, S.shift);
			const W = (q: P2) => rot(q, S.ang);
			// synchronous overlap from the beam angle only: where the unshifted beam would land vs the line of the excited
			// mode (a parallel shift of the beam, as in the half-prism set-up, does not change theta_3)
			const ang0 = S.shift === 0 ? ray : trace(S.ang, 0);
			const du = ang0.u - lineU[syncLine];
			const beamOn = seg(S.reveal, 0.98, 1);
			const g = ang0.ok ? Math.exp(-((du / (SPOT_U * 0.36)) ** 2)) * beamOn : 0;
			const bc = on('beam_in');
			// outside incident band, converging onto the entry point, revealed with the beam front
			const Ew = W(ray.E);
			const shiftV: P2 = [S.shift, 0];
			const a0 = add(bandA, shiftV), a1 = add(bandB, shiftV);
			const lenOut = Math.hypot(Ew[0] - A0[0] - S.shift, Ew[1] - A0[1]);
			const Bw = W(ray.B), Erw = W(ray.Er), Hw = W(ray.H);
			const lenIn = Math.hypot(Bw[0] - Ew[0], Bw[1] - Ew[1]);
			const lenRe = Math.hypot(Erw[0] - Bw[0], Erw[1] - Bw[1]);
			const lenRe2 = Math.hypot(Hw[0] - Erw[0], Hw[1] - Erw[1]);
			const total = lenOut + lenIn + lenRe + lenRe2;
			let rem = S.reveal * total;
			const take = (L: number) => {
				const t = clamp01(rem / Math.max(1e-6, L));
				rem -= L;
				return t;
			};
			const tOut = take(lenOut), tIn = take(lenIn), tRe = take(lenRe), tRe2 = take(lenRe2);
			if (S.reveal > 0.001 && ray.ok) {
				const tipC = lerp2(lerp2(a0, a1, 0.5), Ew, tOut);
				const wd = lerp(Math.hypot(a1[0] - a0[0], a1[1] - a0[1]) / 2, 1.4, tOut);
				const dirB = nrm(sub(Ew, lerp2(a0, a1, 0.5)));
				const nb: P2 = [-dirB[1], dirB[0]];
				// quad order chosen so it never self-crosses (a0 / a1 order vs the normal)
				const q = dot(sub(a1, a0), nb) > 0 ? [a0, a1, add(tipC, mul(nb, wd)), sub(tipC, mul(nb, wd))] : [a0, a1, sub(tipC, mul(nb, wd)), add(tipC, mul(nb, wd))];
				setBeam(bIn, dOf(q as P2[]), 1, 0.85, true, bc);
				hitIn.setAttribute('d', dOf([lerp2(a0, a1, 0.5), tipC], false));
				show(hitIn, 1);
				if (tIn > 0) {
					setBeam(bIn2, dOf([Ew, lerp2(Ew, Bw, tIn)], false), 2.2, 1, false, bc);
					hitIn.setAttribute('d', dOf([lerp2(a0, a1, 0.5), Ew, lerp2(Ew, Bw, tIn)], false));
				} else hideBeam(bIn2);
				// dip at the synchronous angle, drawn at the deepest reported ("occasionally down to 50%")
				const b3in = 1 - 0.5 * g;
				const b3 = b3in * S.offPeriph;
				const rc = on('beam_reflected');
				// half prism: the reflected beam stops at the cut face (its further path is not described)
				const hc = S.cutK > 0 ? hitLine(ray.B, [ray.Er[0] - ray.B[0], ray.Er[1] - ray.B[1]], CUT, [CUT[0], CUT[1] - 1]) : null;
				const reEnd = hc && hc[1] > 0 && hc[1] < 1 ? lerp2(Erw, W(hc[0]), S.cutK) : Erw;
				if (tRe > 0 && b3in > 0.01) {
					setBeam(bRe, dOf([Bw, lerp2(Bw, reEnd, tRe)], false), 2, b3in, false, rc);
					if (S.cutK > 0) {
						hitRe.setAttribute('d', dOf([Bw, reEnd], false));
						show(hitRe, 1);
					}
				} else hideBeam(bRe);
				if (tRe2 > 0 && b3 > 0.01) {
					const hA = W(add(S0, mul(SDIR, ray.u - SPOT_U))), hB = W(add(S0, mul(SDIR, ray.u + SPOT_U)));
					const e0 = add(Erw, mul(nrm(sub(hA, hB)), 1.2)), e1 = add(Erw, mul(nrm(sub(hB, hA)), 1.2));
					const fA = lerp2(e0, hA, tRe2), fB = lerp2(e1, hB, tRe2);
					setBeam(bRe2, dOf([e0, fA, fB, e1]), 1, 0.7 * b3, true, rc);
					hitRe.setAttribute('d', dOf([Bw, Erw, lerp2(Erw, Hw, tRe2)], false));
					show(hitRe, 1);
				} else {
					hideBeam(bRe2);
					if (S.cutK <= 0) show(hitRe, 0);
				}
			} else {
				for (const bm of [bIn, bIn2, bRe, bRe2]) hideBeam(bm);
				show(hitIn, 0);
				show(hitRe, 0);
			}
			// out-coupled rays onto the m lines (exist only at the synchronous angle)
			const fanO = g * S.offPeriph;
			fan.forEach((f, i) => {
				if (!f || fanO < 0.01) {
					hideBeam(fanB[i]);
					show(hitFan[i], 0);
					return;
				}
				const d = dOf([W(ray.B), W(f.Er), W(f.H)], false);
				setBeam(fanB[i], d, 0.9, 0.75 * fanO, false, on('m_lines'));
				hitFan[i].setAttribute('d', d);
				show(hitFan[i], 1);
			});

			// normal at the coupling spot and the angle theta3 (as drawn)
			if (S.normal > 0.01 && ray.ok) {
				const B = ray.B;
				normalL.setAttribute('d', dOf([[B[0], B[1] - 100], [B[0], B[1] - 1]], false));
				const t0 = -Math.PI / 2;
				const tIn = Math.atan2(ray.E[1] - B[1], ray.E[0] - B[0]);
				const q: P2[] = [];
				for (let i = 0; i <= 16; i++) {
					const t = lerp(t0, tIn, i / 16);
					q.push([B[0] + 38 * Math.cos(t), B[1] + 38 * Math.sin(t)]);
				}
				thetaArc.setAttribute('d', dOf(q, false));
				normalHit.setAttribute('d', dOf(q, false));
				for (const e of [normalL, thetaArc]) {
					e.setAttribute('stroke', edgeCol(c.ink, 'theta3'));
					e.setAttribute('stroke-width', f1(1 / s));
				}
				show(normalL, S.normal * 0.8);
				show(thetaArc, S.normal);
				show(normalHit, S.normal);
			} else {
				show(normalL, 0);
				show(thetaArc, 0);
				show(normalHit, 0);
			}

			// ------------------------------------------------ guided light in the film (prism frame)
			const glowO = g;
			const x0 = ray.B[0] - FP / 2;
			if (glowO > 0.01 && ray.ok) {
				const xa = x0, xb = gFilm[2];
				for (const gr of [glowGrad, coreGrad]) {
					gr.setAttribute('x1', f1(xa));
					gr.setAttribute('x2', f1(xb));
				}
				const reach = S.half > 0.01 ? CUT[0] + STREAK * (0.08 + 0.92 * ease(S.streak)) : Infinity;
				gStops.forEach((stp, i) => {
					const x = lerp(xa, xb, i / (NST - 1));
					const v = x > reach ? 0 : clamp01(guided(x, x0, S.half, S.scratch));
					stp.setAttribute('stop-color', c.beam);
					stp.setAttribute('stop-opacity', Math.min(1, v * 1.1).toFixed(3));
					cStops[i].setAttribute('stop-color', on('guided_mode') || (on('streak') && x >= CUT[0]) ? mix(c.beamCore, c.accent, 0.6) : c.beamCore);
					cStops[i].setAttribute('stop-opacity', Math.min(1, v * 1.2).toFixed(3));
				});
				const fy0 = gFilm[1] + dy, fy1 = gFilm[3] + dy;
				const gq: P2[] = [[xa, fy0 + 1], [xb, fy0 + 1], [xb, fy1 - 1], [xa, fy1 - 1]];
				filmGlow.setAttribute('d', dOf(gq));
				filmGlow.setAttribute('fill', `url(#${id}-gm)`);
				filmGlowSoft.setAttribute('d', dOf(gq));
				filmGlowSoft.setAttribute('fill', `url(#${id}-gm)`);
				show(filmGlow, glowO * (theme === 'light' ? 0.85 : 0.9));
				show(filmGlowSoft, glowO * c.glowA);
				// bright core of the guided light along the film centre
				const yc = (fy0 + fy1) / 2;
				flow.setAttribute('d', dOf([[xa, yc], [xb - 1, yc]], false));
				flow.setAttribute('stroke', `url(#${id}-gc)`);
				flow.setAttribute('stroke-width', f1(Math.max(1.4, 2.2 / s)));
				show(flow, glowO);
				const under = Math.min(xb, x0 + FP + 3 / A_DEC);
				glowHit.setAttribute('d', dOf([[xa, fy0 - 2], [under, fy0 - 2], [under, fy1 + 2], [xa, fy1 + 2]]));
				show(glowHit, glowO > 0.3 && S.half < 0.5 ? 1 : 0);
				const xe = Math.min(xb, S.scratch > 0.5 ? SCRATCH_X : CUT[0] + STREAK);
				streakHit.setAttribute('d', dOf([[CUT[0], fy0 - 3], [xe, fy0 - 3], [xe, fy1 + 3], [CUT[0], fy1 + 3]]));
				show(streakHit, S.half > 0.9 && S.streak > 0.3 ? 1 : 0);
			} else {
				show(filmGlow, 0);
				show(filmGlowSoft, 0);
				show(flow, 0);
				show(glowHit, 0);
				show(streakHit, 0);
			}
			// scratch: ends the streak sharply and radiates
			if (S.scratch > 0.01) {
				const fy0 = gFilm[1] + dy, fy1 = gFilm[3] + dy;
				scratch.setAttribute('d', `${dOf([[SCRATCH_X - 1.5, fy0 - 1], [SCRATCH_X, fy1 - 2], [SCRATCH_X + 1.5, fy0 - 1]], false)}`);
				scratch.setAttribute('stroke', edgeCol(c.ink, 'scratch'));
				scratch.setAttribute('stroke-width', f1(1.2 / s));
				scratchGlow.setAttribute('cx', f1(SCRATCH_X));
				scratchGlow.setAttribute('cy', f1((fy0 + fy1) / 2));
				scratchGlow.setAttribute('r', f1(5 + 3 * S.scratch));
				scratchGlow.setAttribute('fill', c.beam);
				scratchHit.setAttribute('cx', f1(SCRATCH_X));
				scratchHit.setAttribute('cy', f1((fy0 + fy1) / 2));
				show(scratch, S.scratch);
				show(scratchGlow, S.scratch * g);
				show(scratchHit, 1);
			} else {
				show(scratch, 0);
				show(scratchGlow, 0);
				show(scratchHit, 0);
			}

			// ------------------------------------------------ turntable arrow (sense matches the rotation)
			if (S.turn && S.optics > 0) {
				const r0 = 190;
				const dir = S.turnDir; // sign of d(ang)/dp
				const spanA = 9;
				const q: P2[] = [];
				for (let i = 0; i <= 20; i++) {
					const a = 90 + lerp(-spanA, spanA, i / 20) * dir;
					q.push([PIV[0] + r0 * Math.cos(a * DEG), PIV[1] + r0 * Math.sin(a * DEG)]);
				}
				turnArc.setAttribute('d', dOf(q, false));
				turnHead.setAttribute('d', head(q[q.length - 1], q[q.length - 3], 9));
				turnHit.setAttribute('d', dOf(q, false));
				turnArc.setAttribute('stroke', edgeCol(c.inkSoft, 'turntable'));
				turnArc.setAttribute('stroke-width', f1(1.2 / s));
				turnHead.setAttribute('fill', edgeCol(c.inkSoft, 'turntable'));
				show(arrowG, 1);
			} else show(arrowG, 0);

			// ------------------------------------------------ face-on view of the screen (Fig. 1 inset)
			if (S.inset > 0.01) {
				show(insetG, S.inset);
				fieldR.setAttribute('d', dOf([[IN[0], IN[1]], [IN[2], IN[1]], [IN[2], IN[3]], [IN[0], IN[3]]]));
				fieldR.setAttribute('fill', c.field);
				fieldR.setAttribute('stroke', edgeCol(c.fieldEdge, 'screen'));
				fieldR.setAttribute('stroke-width', f1(1 / s));
				const lo = g;
				LX.forEach((x, i) => {
					const b = curved.some((cx) => Math.abs(cx + DXI - x) < 1) ? 3 + 2.5 * curved.findIndex((cx) => Math.abs(cx + DXI - x) < 1) : 0;
					const d = b ? `M${f1(x)},${f1(IN[1] - 2)}Q${f1(x - 2 * b)},${f1((IN[1] + IN[3]) / 2)} ${f1(x)},${f1(IN[3] + 2)}` : dOf([[x, IN[1] - 2], [x, IN[3] + 2]], false);
					mSoft[i].setAttribute('d', d);
					mSoft[i].setAttribute('stroke', c.line);
					// widths thin outward and the last line is broken, as Fig. 1 draws them (schematic)
					const tw = [1.5, 1.15, 1.05, 0.95, 0.75][Math.min(4, i)];
					mSoft[i].setAttribute('stroke-width', f1(4 * tw));
					for (const e of [mSoft[i], mCore[i]]) e.setAttribute('stroke-dasharray', i === LX.length - 1 && LX.length > 2 ? '5 3' : 'none');
					mCore[i].setAttribute('d', d);
					mCore[i].setAttribute('stroke', on('m_lines') ? mix(c.lineCore, c.accent, 0.5) : c.lineCore);
					mCore[i].setAttribute('stroke-width', f1(Math.max(1, 1.4 / s) * tw));
					show(mSoft[i], lo * 0.9);
					show(mCore[i], lo);
				});
				const xs = insetX(ray.u);
				const b3 = (1 - 0.5 * g) * beamOn;
				spotCore.setAttribute('cx', f1(xs));
				spotCore.setAttribute('cy', f1(spotC[1]));
				spotCore.setAttribute('r', f1(spotR));
				spotCore.setAttribute('fill', on('beam_reflected') ? mix(c.spot, c.accent, 0.4) : c.spot);
				spotSoft.setAttribute('cx', f1(xs));
				spotSoft.setAttribute('cy', f1(spotC[1]));
				spotSoft.setAttribute('r', f1(spotR + 3));
				spotSoft.setAttribute('fill', c.line);
				show(spotCore, b3);
				show(spotSoft, b3 * 0.9);
				spotClipC.setAttribute('cx', f1(xs));
				spotClipC.setAttribute('cy', f1(spotC[1]));
				const xl = LX[syncLine];
				darkLine.setAttribute('x1', f1(xl));
				darkLine.setAttribute('x2', f1(xl));
				darkLine.setAttribute('y1', f1(spotC[1] - spotR - 1));
				darkLine.setAttribute('y2', f1(spotC[1] + spotR + 1));
				darkLine.setAttribute('stroke', c.dark);
				darkLine.setAttribute('stroke-width', '2.4');
				const inSpot = Math.abs(xl - xs) < spotR - 1 ? 1 : 0;
				show(darkLine, inSpot * beamOn * clamp01(g * 3));
				darkHit.setAttribute('x', f1(xl - 4));
				darkHit.setAttribute('y', f1(spotC[1] - spotR));
				darkHit.setAttribute('width', '8');
				darkHit.setAttribute('height', f1(2 * spotR));
				darkHit.setAttribute('stroke', on('dark_line') ? c.accent : 'none');
				darkHit.setAttribute('stroke-width', f1(1.2 / s));
				show(darkHit, inSpot * g > 0.3 ? 1 : 0);
				// projection lines from the edge-on screen to the face-on view (Fig. 1 convention; synchronous pose)
				LX.forEach((x, i) => {
					const H = W(add(S0, mul(SDIR, lineU[i])));
					projL[i].setAttribute('d', dOf([H, lerp2(H, [x, IN[3]], S.proj)], false));
					projL[i].setAttribute('stroke', edgeCol(c.inkSoft, 'projection'));
					projL[i].setAttribute('stroke-width', f1(1 / s));
					show(projL[i], S.proj > 0.01 ? 0.9 : 0);
				});
				projHit.setAttribute('d', LX.map((x, i) => dOf([W(add(S0, mul(SDIR, lineU[i]))), [x, IN[3]]], false)).join(''));
				show(projHit, S.proj > 0.5 ? 1 : 0);
			} else show(insetG, 0);
		};

		// ---------------------------------------------------------------------------- picking
		const INFO: Record<string, PickInfo> = {
			turntable: {
				id: 'turntable',
				label: 'Turntable (not drawn)',
				detail: [
					'"The whole prism-film assembly, including the screen but not the laser, is mounted on a turntable so that the direction θ_{3} can be varied at will" (Tien et al., Appl. Phys. Lett. 1969, p.293 col. 1).',
					'Shown as a turn of the assembly about an axis normal to the drawing; pivot and amount are schematic, no angle is given.'
				]
			},
			theta3: {
				id: 'theta3',
				label: 'Angle of incidence θ_{3}',
				detail: [
					'Measured from the normal to the prism base; θ_{3} is synchronous for a mode when β = k n_{3} sin θ_{3} (Tien et al., Appl. Phys. Lett. 1969, p.292 col. 1).',
					'Drawn as in Fig. 1 (about 42°); the synchronous angles are not shown: the paper prints β/k, not angles.'
				]
			},
			dark_line: {
				id: 'dark_line',
				label: 'Dark line in the B_{3} spot',
				detail: [
					'The mode accepts only a small part of the beam\'s 1° range of θ_{3}, so a dark line crosses the spot at the synchronous direction; an m line runs through it (Tien et al., Appl. Phys. Lett. 1969, p.293 col. 1-2).',
					'Drawn on the m line of the face-on view (schematic).'
				]
			},
			projection: {
				id: 'projection',
				label: 'Screen, face-on view',
				detail: ['Fig. 1 links the edge-on screen to a face-on view with dashed lines; reproduced as drawn (schematic, five lines, not tied to a particular film).']
			},
			scratch: {
				id: 'scratch',
				label: 'Scratch across the streak',
				detail: [
					'"When the continuity of the film is interrupted by scratching across the streak with a fine point, the streak ends sharply at the scratch and the scratch itself radiates brightly" (Tien et al., Appl. Phys. Lett. 1969, p.294 col. 2).',
					'Position along the streak assumed (not stated).'
				]
			}
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
					return INFO[pid] ?? pid;
				}
				return null;
			},
			anchor(pid) {
				const S = lastS;
				if (!S) return null;
				const W = (q: P2) => toPane(rot(q, S.ang));
				if (pid === 'prism') {
					if (S.prism < 0.6 || S.half > 0.05) return null;
					return W([R1[0] - 0.42 * (R1[0] - apex[0]), apex[1] + 0.42 * (R1[1] - apex[1]) - 6]);
				}
				if (pid === 'gap') {
					if (S.gapMark < 0.5) return null;
					return W([R0[0] + 28, BASE + GAP / 2]);
				}
				if (pid === 'streak') {
					// the length names the unscratched streak: shown only before the scratch
					if (S.streak < 0.6 || S.half < 0.9 || S.scratch > 0.05) return null;
					const xe = CUT[0] + 0.7 * STREAK;
					return W([lerp(CUT[0], xe, 0.5), gSub[3] + S.D + 14]);
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
