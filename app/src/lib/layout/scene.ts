// Scene builders for the layout viewer (DevLog-005 D103, D104). A scene is geometry in micrometres (x right, y up)
// plus dimension marks and labels. Every visible number comes from a resolved metric row (Dim.label); a dimension the
// source does not report gets a schematic size (a fixed proportion of a reported neighbour), a dashed outline and the
// label "not reported". No source figure is reproduced or traced: shapes are generic template outlines.
import type { Component } from '../components.svelte';
import { MATERIALS, scanMaterials, stackOf, type Stack } from './materials';
import { resolveDim, segmentRows, type Dim, type Resolved, type View } from './resolve';

export type Pt = [number, number];
export interface Shape {
	rings: Pt[][];
	mat: string;
	role: string;
	schematic: boolean;
	tip: string;
	alpha?: number;
	line?: boolean;
	hatch?: boolean;
}
export interface Mark {
	dir: 'h' | 'v';
	a: number;
	b: number;
	/** Perpendicular coordinates of the measured features at a and b (extension lines start there). */
	from: [number, number];
	/** Perpendicular coordinate of the dimension line (um) and an extra pixel offset (+ = up for h, right for v). */
	pos: number;
	px: number;
	dim: Dim;
	inset?: boolean;
	/** Vertical marks: put the label at the upper end instead of the middle. */
	atEnd?: boolean;
}
export interface Label {
	at: Pt;
	text: string;
	anchor: 'start' | 'middle' | 'end';
	dx?: number;
	dy?: number;
	dim?: Dim;
	tip?: string;
	muted?: boolean;
}
export interface Scene {
	view: View;
	title: string;
	shapes: Shape[];
	marks: Mark[];
	labels: Label[];
	notes: string[];
	/** The aspect toggle is offered (linear structures); false for rings and the schematic AWG. */
	stretch: boolean;
	/** Whole scene is a schematic (not to scale in any mode): no reported length is drawn in this view (D225). */
	schematic: boolean;
	/** Reported dimensions are drawn to scale but some shapes are schematic (dashed, template proportions) (D225). */
	partial: boolean;
	inset?: { c: Pt; half: number };
}

const LEN_UNITS = new Set(['nm', 'um', 'mm', 'cm']);

const fmtList = (xs: string[]) => xs.join(', ');

class B {
	shapes: Shape[] = [];
	marks: Mark[] = [];
	labels: Label[] = [];
	notes: string[] = [];
	segs = new Set<string>();
	st: Stack;
	constructor(
		public r: Resolved,
		public view: View
	) {
		this.st = stackOf(r.comp);
	}
	d(p: string): Dim {
		return (
			this.r.dims[p] ?? { param: p, views: [], required: false, row: null, alts: [], num: null, unit: '', label: 'not reported', basis: null, badge: '', tip: p + ' - not a parameter of this template' }
		);
	}
	has(p: string): boolean {
		return this.d(p).num !== null;
	}
	v(p: string): number {
		return this.d(p).num as number;
	}
	/** Reported value, or the schematic fallback with a flag. */
	or(p: string, fb: () => number): [number, boolean] {
		const d = this.d(p);
		return d.num !== null && d.num > 0 ? [d.num, false] : [fb(), true];
	}
	tip(role: string, whyKey: string, mat: string, params: string[], extra = ''): string {
		const miss = params.filter((p) => !this.has(p));
		const why = this.st.why[whyKey] ?? '';
		return [
			`${role}: ${MATERIALS[mat] ?? mat}${why ? ' (' + why + ')' : ''}`,
			params.length ? 'dimensions: ' + fmtList(params) : '',
			miss.length ? 'dashed: not reported (' + fmtList(miss) + ')' : '',
			extra
		]
			.filter(Boolean)
			.join('\n');
	}
	poly(pts: Pt[], mat: string, role: string, params: string[], o: Partial<Shape> = {}, why = role): void {
		const { tip = '', schematic: sch, ...rest } = o;
		const schematic = sch ?? params.some((p) => !this.has(p));
		this.shapes.push({ rings: [pts], mat, role, schematic, tip: this.tip(role, why, mat, params, tip), ...rest });
	}
	rect(x0: number, y0: number, x1: number, y1: number, mat: string, role: string, params: string[], o: Partial<Shape> = {}, why = role): void {
		this.poly([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], mat, role, params, o, why);
	}
	mark(p: string | Dim, dir: 'h' | 'v', a: number, b: number, from: [number, number], pos: number, px: number, inset = false, atEnd = false): void {
		const d = typeof p === 'string' ? this.r.dims[p] : p;
		if (!d || (!d.views.includes(this.view) && !d.row)) return;
		const sw = a > b;
		this.marks.push({ dir, a: sw ? b : a, b: sw ? a : b, from: sw ? [from[1], from[0]] : from, pos, px, dim: d, inset, atEnd });
	}
	/** A value label with no geometric extent (counts, angles, ratios): "<word> <stored value>". */
	val(p: string, at: Pt, word: string, anchor: Label['anchor'] = 'start', dx = 0, dy = 0): void {
		const d = this.d(p);
		this.labels.push({ at, text: word + ' ' + d.label, anchor, dx, dy, dim: d });
	}
	text(at: Pt, text: string, anchor: Label['anchor'] = 'middle', dx = 0, dy = 0, tip = ''): void {
		this.labels.push({ at, text, anchor, dx, dy, tip, muted: true });
	}
	scene(title: string, o: Partial<Scene> = {}): Scene {
		const miss = this.r.template[this.view].required.filter((p) => !this.has(p));
		const notes = [...this.notes];
		if (miss.length) notes.unshift('required not reported: ' + fmtList(miss) + ' (drawn schematically)');
		const alts = Object.values(this.r.dims).filter((d) => d.row && d.alts.length && d.views.includes(this.view) && !this.segs.has(d.param));
		if (alts.length) notes.push('several rows: ' + fmtList(alts.map((d) => d.param)) + ' (first row drawn; others on hover)');
		// D225: a view with no reported length drawn is a schematic (no scale bar); with some dashed shapes it is partly
		// schematic (reported dimensions to scale, dashed shapes at template proportions).
		const anchored = this.marks.some((m) => m.dim.row && LEN_UNITS.has(m.dim.row.unit));
		const partial = this.shapes.some((x) => x.schematic && !x.line && x.role !== 'substrate');
		return { view: this.view, title, shapes: this.shapes, marks: this.marks, labels: this.labels, notes, stretch: true, schematic: !anchored, partial, ...o };
	}
}

// ---------- geometry helpers ----------

/** Polygon of a strip of width w(i) around a centreline. */
function strip(c: Pt[], w: (i: number) => number): Pt[] {
	const left: Pt[] = [], right: Pt[] = [];
	for (let i = 0; i < c.length; i++) {
		const p0 = c[Math.max(0, i - 1)], p1 = c[Math.min(c.length - 1, i + 1)];
		const dx = p1[0] - p0[0], dy = p1[1] - p0[1], n = Math.hypot(dx, dy) || 1;
		const nx = -dy / n, ny = dx / n, h = w(i) / 2;
		left.push([c[i][0] + nx * h, c[i][1] + ny * h]);
		right.push([c[i][0] - nx * h, c[i][1] - ny * h]);
	}
	return [...left, ...right.reverse()];
}
const circle = (cx: number, cy: number, r: number, n = 180): Pt[] => Array.from({ length: n }, (_, i) => [cx + r * Math.cos((2 * Math.PI * i) / n), cy + r * Math.sin((2 * Math.PI * i) / n)] as Pt);
/** Cosine S-bend centreline from (x0, y0) to (x0 + L, y0 + dy). */
const sbend = (x0: number, y0: number, L: number, dy: number, n = 40): Pt[] => Array.from({ length: n + 1 }, (_, i) => [x0 + (L * i) / n, y0 + (dy * (1 - Math.cos((Math.PI * i) / n))) / 2] as Pt);
/** Two-arc S-bend of radius R with lateral offset dy (length 2 R sin(phi), dy = 2 R (1 - cos(phi))). */
function arcSbend(x0: number, y0: number, R: number, dy: number, n = 40): Pt[] {
	const s = Math.sign(dy) || 1, a = Math.abs(dy);
	const phi = Math.acos(Math.max(-1, 1 - a / (2 * R)));
	const pts: Pt[] = [];
	for (let i = 0; i <= n; i++) {
		const f = (phi * i) / n;
		pts.push([x0 + R * Math.sin(f), y0 + s * R * (1 - Math.cos(f))]);
	}
	const xm = x0 + R * Math.sin(phi), ym = y0 + s * R * (1 - Math.cos(phi));
	for (let i = 1; i <= n; i++) {
		const f = phi - (phi * i) / n;
		pts.push([xm + R * (Math.sin(phi) - Math.sin(f)), ym + s * R * (Math.cos(f) - Math.cos(phi))]);
	}
	return pts;
}
const arcLen = (R: number, dy: number) => 2 * R * Math.sin(Math.acos(Math.max(-1, 1 - Math.abs(dy) / (2 * R))));
const line = (a: Pt, b: Pt, n = 2): Pt[] => Array.from({ length: n }, (_, i) => [a[0] + ((b[0] - a[0]) * i) / (n - 1), a[1] + ((b[1] - a[1]) * i) / (n - 1)] as Pt);
const isRib = (c: Component) => /rib|ridge/i.test((c.platform ?? '') + ' ' + (c.core_material ?? '') + ' ' + c.label);

// ---------- lateral cross-section (layer stack) ----------

interface XsecOpts {
	wParam?: string;
	layer2?: boolean;
	overlay?: boolean;
	absorber?: boolean;
	heater?: boolean;
	title?: string;
}

function xsecStack(b: B, o: XsecOpts = {}): Scene {
	const c = b.r.comp, st = b.st;
	const wp = o.wParam ?? 'width_nm';
	const etch = b.has('etch_depth_nm') ? b.v('etch_depth_nm') : null;
	const [t] = b.or('core_thickness_nm', () => (etch !== null ? etch / 0.6 : b.has(wp) ? 0.45 * b.v(wp) : 0.22));
	const [w] = b.or(wp, () => (wp === 'lower_width_nm' && b.has('width_nm') ? b.v('width_nm') : 2.2 * t));
	const tP = ['core_thickness_nm', wp];
	// Rib: slab reported, or core minus a reported etch depth, or a schematic slab when the text says rib.
	let slab = 0, slabParams: string[] = [];
	if (b.has('slab_thickness_nm') && b.v('slab_thickness_nm') < t) [slab, slabParams] = [b.v('slab_thickness_nm'), ['slab_thickness_nm']];
	else if (etch !== null && etch < t) [slab, slabParams] = [t - etch, ['core_thickness_nm', 'etch_depth_nm']];
	else if (etch === null && isRib(c)) [slab, slabParams] = [0.4 * t, ['slab_thickness_nm']];
	const ang = b.has('sidewall_angle_deg') ? b.v('sidewall_angle_deg') : 90;
	const dxs = ang > 0 && ang < 90 ? (t - slab) / Math.tan((ang * Math.PI) / 180) : 0;
	const [box] = b.or('box_thickness_um', () => Math.min(6 * t, 4));
	let top = t; // top of the drawn stack above y = 0

	// Optional layers above / around the core.
	let hx = 0, wo = 0, to = 0, os = 0, t2 = 0, g = 0, w2 = 0, ta = 0, wa = 0, wh = 0, gh = 0, th = 0;
	const ov = o.overlay && (b.has('overlay_width_um') || b.has('overlay_thickness_um'));
	if (ov) {
		[wo] = b.or('overlay_width_um', () => (b.has('overlay_thickness_um') ? b.v('overlay_thickness_um') : 6 * w));
		[to] = b.or('overlay_thickness_um', () => 0.8 * wo);
		os = b.has('overlay_slab_thickness_um') ? b.v('overlay_slab_thickness_um') : 0;
		top = Math.max(top, to);
	}
	if (o.layer2) {
		[t2] = b.or('layer2_thickness_nm', () => t);
		[g] = b.or('gap_nm', () => 0.5 * t);
		// D222: the section is at the lower-layer input, where the upper taper starts at its tip (tip_width_nm); same
		// schematic fallback as the top view.
		[w2] = b.or('tip_width_nm', () => 0.2 * w);
		top = t + g + t2;
	}
	if (o.absorber) {
		[ta] = b.or('absorber_thickness_nm', () => 1.5 * t);
		[wa] = b.or('absorber_width_um', () => 0.8 * w);
		top = t + ta;
	}
	const air = st.cladding === 'air';
	let [clad] = b.or('cladding_thickness_um', () => (o.heater && b.has('heater_gap_um') ? b.v('heater_gap_um') : Math.min(4 * t, 3)));
	if (o.heater) {
		[wh] = b.or('heater_width_um', () => 3 * w);
		[gh] = b.or('heater_gap_um', () => clad);
		th = b.has('heater_thickness_nm') ? b.v('heater_thickness_nm') : Math.max(0.25 * t, 0.06);
		hx = b.has('heater_offset_um') ? b.v('heater_offset_um') : 0;
	}
	if (air) clad = 0;
	// D229: an overlay SSC's cladding is measured from the overlay top; elsewhere from the core top. The solid band never
	// exceeds the labelled thickness: fill beside the overlay and above the reported thickness is drawn dashed.
	const cBase = ov ? to : t;
	const cladTop = air ? top : cBase + clad;
	const hTop = o.heater ? t + gh + th : 0;
	const yTop = Math.max(cladTop, hTop, top);
	const X = Math.max(1.5 * (w + 2 * dxs), 0.8 * wo, 0.8 * wh + Math.abs(hx), 0.8 * wa, 0.55 * (yTop + box), 0.8);
	const sub = 0.45 * Math.max(box, t);

	// Substrate and lower cladding.
	const lo = st.box === 'none' ? 0 : box;
	b.rect(-X, -lo - sub, X, -lo, st.substrate, 'substrate', [], { schematic: true, alpha: 0.5, tip: 'substrate thickness is not a template dimension: truncated band' });
	if (st.box === 'sio2' || st.box === 'glass' || st.box === 'polymer') b.rect(-X, -box, X, 0, st.box, 'BOX / lower cladding', ['box_thickness_um'], {}, 'box');
	else if (st.box === 'air') b.text([0, -box / 2], 'air (suspended)', 'middle');
	if (!air) {
		if (ov) b.rect(-X, 0, X, cBase, st.cladding, 'cladding beside the overlay', [], { alpha: 0.3, schematic: true, tip: 'fill beside the overlay: not a reported thickness (dashed)' }, 'cladding');
		b.rect(-X, ov ? cBase : 0, X, cladTop, st.cladding, 'cladding', ['cladding_thickness_um'], { alpha: 0.45, tip: ov ? 'cladding thickness drawn from the overlay top (planar top surface schematic)' : '' }, 'cladding');
		if (top > cladTop) b.rect(-X, cladTop, X, top, st.cladding, 'cladding above the reported thickness', [], { alpha: 0.3, schematic: true, tip: 'layers reach above the reported cladding thickness: cladding extent there not reported (dashed)' }, 'cladding');
	} else b.text([X, yTop], 'air', 'end', -4, -4);
	if (ov && os > 0) b.rect(-X, 0, X, os, st.overlay, 'overlay slab', ['overlay_slab_thickness_um'], {}, 'overlay');
	if (ov) b.rect(-wo / 2, os > 0 ? os : 0, wo / 2, to, st.overlay, 'overlay', ['overlay_width_um', 'overlay_thickness_um'], {}, 'overlay');
	if (slab > 0) b.rect(-X, 0, X, slab, st.core, 'slab', slabParams, {}, 'core');
	b.poly([[-w / 2 - dxs, slab], [w / 2 + dxs, slab], [w / 2, t], [-w / 2, t]], st.core, 'core', tP, {
		tip: ang !== 90 ? 'width drawn at the ridge top; sidewall angle from the data' : b.r.template.xsec.optional.includes('sidewall_angle_deg') ? 'sidewalls drawn vertical (angle not reported)' : ''
	}, 'core');
	if (o.layer2) b.rect(-w2 / 2, t + g, w2 / 2, t + g + t2, st.layer2, 'upper layer (taper tip)', ['layer2_thickness_nm', 'gap_nm', 'tip_width_nm'], { tip: 'upper layer at its taper tip (tip_width_nm), as in the top view at the lower-layer input' }, 'layer2');
	if (o.absorber) b.rect(-wa / 2, t, wa / 2, t + ta, st.absorber, 'absorber', ['absorber_width_um', 'absorber_thickness_nm'], {}, 'absorber');
	if (o.heater) b.rect(hx - wh / 2, t + gh, hx + wh / 2, t + gh + th, st.heater, 'heater', ['heater_width_um', 'heater_gap_um', 'heater_thickness_nm', 'heater_offset_um'], { tip: b.has('heater_offset_um') ? '' : 'lateral position not reported: drawn centred (schematic)' }, 'heater');

	// Marks: left chain (box, slab, etch, cladding), right chain (core and stacked layers), widths on top.
	const R = X, L = -X;
	if (st.box !== 'none') b.mark('box_thickness_um', 'v', -box, 0, [L, L], L, -8);
	if (slab > 0 && slabParams[0] === 'slab_thickness_nm') b.mark('slab_thickness_nm', 'v', 0, slab, [L, L], L, -8);
	if (etch !== null) b.mark('etch_depth_nm', 'v', t - etch, t, [-w / 2 - dxs, -w / 2], L, -8);
	else if (b.r.dims.etch_depth_nm && b.r.dims.etch_depth_nm.views.includes('xsec') && slab > 0) b.mark('etch_depth_nm', 'v', slab, t, [-w / 2, -w / 2], L, -8);
	if (!air) b.mark('cladding_thickness_um', 'v', cBase, cBase + clad, [L, L], L, -8);
	b.mark('core_thickness_nm', 'v', 0, t, [w / 2, w / 2], R, 8);
	if (o.layer2) {
		b.mark('gap_nm', 'v', t, t + g, [w / 2, w2 / 2], R, 8);
		b.mark('layer2_thickness_nm', 'v', t + g, t + g + t2, [w2 / 2, w2 / 2], R, 8);
		const tipD = b.d('tip_width_nm');
		b.mark({ ...tipD, views: [...tipD.views, 'xsec'] }, 'h', -w2 / 2, w2 / 2, [t + g + t2, t + g + t2], yTop, 30);
	}
	if (o.absorber) {
		b.mark('absorber_thickness_nm', 'v', t, t + ta, [wa / 2, wa / 2], R, 8);
		b.mark('absorber_width_um', 'h', -wa / 2, wa / 2, [t + ta, t + ta], yTop, 30);
	}
	if (ov) {
		b.mark('overlay_thickness_um', 'v', 0, to, [wo / 2, wo / 2], R, 76);
		b.mark('overlay_width_um', 'h', -wo / 2, wo / 2, [to, to], yTop, 30);
		if (os > 0) b.mark('overlay_slab_thickness_um', 'v', 0, os, [-X, -X], -X, -8);
	}
	if (o.heater) {
		b.mark('heater_gap_um', 'v', t, t + gh, [w / 2, hx + wh / 2], R, 76);
		b.mark('heater_width_um', 'h', hx - wh / 2, hx + wh / 2, [t + gh + th, t + gh + th], yTop, 30);
		b.mark('heater_thickness_nm', 'v', t + gh, t + gh + th, [hx - wh / 2, hx - wh / 2], L, -8);
		if (hx) b.mark('heater_offset_um', 'h', 0, hx, [t, t + gh], yTop, 48);
		else if (!b.has('heater_offset_um')) b.val('heater_offset_um', [hx + wh / 2, t + gh + th], 'offset', 'start', 6, -4);
	}
	b.mark(wp, 'h', -w / 2, w / 2, [t, t], yTop, 12);
	if (ang !== 90) b.val('sidewall_angle_deg', [w / 2 + dxs / 2, slab + (t - slab) / 2], 'sidewall', 'start', 6, 0);
	if (b.r.template.xsec.optional.includes('sidewall_angle_deg') && ang === 90) b.notes.push('sidewalls drawn vertical (sidewall_angle_deg not reported)');
	if (slab > 0 && slabParams[0] === 'slab_thickness_nm' && !b.has('slab_thickness_nm')) b.notes.push('rib from the platform / text; slab thickness not reported');
	if (st.cladding === 'unknown') b.notes.push('cladding material not stated');
	if (o.layer2) b.notes.push('layer order from the platform and core_material text');
	return b.scene(o.title ?? 'cross-section (lateral)');
}

// ---------- longitudinal sections ----------

function gcSection(b: B): Scene {
	const st = b.st;
	const [P] = b.or('period_nm', () => 0.6);
	const [ff] = b.or('fill_factor', () => 0.5);
	const etchR = b.has('etch_depth_nm');
	const [t] = b.or('core_thickness_nm', () => (etchR ? b.v('etch_depth_nm') / 0.5 : 0.22));
	const [e] = b.or('etch_depth_nm', () => 0.5 * t);
	const slab = b.has('slab_thickness_nm') ? b.v('slab_thickness_nm') : Math.max(t - e, 0);
	const nRep = b.has('n_periods') ? b.v('n_periods') : null;
	const K = Math.min(nRep ?? 10, 10);
	const [box] = b.or('box_thickness_um', () => Math.min(6 * t, 4));
	const air = st.cladding === 'air';
	const [clad] = b.or('cladding_thickness_um', () => Math.min(4 * t, 3));
	const x0 = -2.5 * P, x1 = (K + 1.5) * P;
	const top = air ? t : t + clad;
	const sub = 0.45 * box;
	const lo = st.box === 'none' ? 0 : box;
	b.rect(x0, -lo - sub, x1, -lo, st.substrate, 'substrate', [], { schematic: true, alpha: 0.5, tip: 'substrate: truncated band' });
	if (st.box !== 'none' && st.box !== 'air') b.rect(x0, -box, x1, 0, st.box, 'BOX / lower cladding', ['box_thickness_um'], {}, 'box');
	if (!air) b.rect(x0, 0, x1, top, st.cladding, 'cladding', ['cladding_thickness_um'], { alpha: 0.45 }, 'cladding');
	else b.text([x1, t], 'air', 'end', -4, -16);
	const gp = ['period_nm', 'fill_factor', 'core_thickness_nm', 'etch_depth_nm'];
	b.rect(x0, 0, 0, t, st.core, 'core (waveguide)', ['core_thickness_nm'], {}, 'core');
	if (slab > 0) b.rect(0, 0, x1, slab, st.core, 'slab under the grating', gp, {}, 'core');
	for (let i = 0; i < K; i++) b.rect(i * P, slab, i * P + ff * P, t, st.core, 'grating tooth', gp, { tip: 'tooth = unetched fraction of the period (fill factor convention as reported)' }, 'core');
	if (nRep === null || nRep > K) b.notes.push('periods truncated in this section');
	// Fiber axis, tilted from the chip normal by the reported angle (sign as printed; tilt direction schematic).
	if (b.has('fiber_angle_deg')) {
		const a = (b.v('fiber_angle_deg') * Math.PI) / 180, xc = (K * P) / 2, y0 = top + 0.15 * (x1 - x0), Lr = 0.45 * (x1 - x0);
		b.shapes.push({ rings: [[[xc, top], [xc + Lr * Math.sin(Math.abs(a)), y0 + Lr * Math.cos(a)]]], mat: 'unknown', role: 'fiber axis', schematic: false, line: true, tip: b.d('fiber_angle_deg').tip });
		b.shapes.push({ rings: [[[xc, top], [xc, y0 + Lr]]], mat: 'unknown', role: 'chip normal', schematic: true, line: true, tip: 'chip normal (reference for the fiber angle)' });
		b.val('fiber_angle_deg', [xc, y0 + Lr], 'fiber', 'start', 6, 0);
	} else b.notes.push('fiber angle not reported (fiber not drawn)');
	if (st.box !== 'none') b.mark('box_thickness_um', 'v', -box, 0, [x0, x0], x0, -8);
	if (!air) b.mark('cladding_thickness_um', 'v', t, top, [x0, x0], x0, -8);
	b.mark('core_thickness_nm', 'v', 0, t, [x0, x0], x0, -8);
	b.mark('etch_depth_nm', 'v', slab, t, [(K - 1) * P + ff * P, (K - 1) * P + ff * P], x1, 8);
	if (b.has('slab_thickness_nm')) b.mark('slab_thickness_nm', 'v', 0, slab, [x1, x1], x1, 8);
	b.mark('period_nm', 'h', P, 2 * P, [t, t], top, 12);
	b.val('fill_factor', [3.5 * P, t], 'ff', 'start', 0, -24);
	return b.scene('cross-section along propagation');
}

/** D220: the layer that core_thickness_nm / etch_depth_nm describe in a laser row is named by the rows' own condition /
 *  notes text (heterogeneous lasers report either the Si waveguide or the III-V layer under these generic names). */
function laserLayerMat(b: B): string | undefined {
	const text = ['core_thickness_nm', 'etch_depth_nm']
		.map((p) => b.d(p).row)
		.map((m) => (m ? (m.condition ?? '') + ' ' + (m.notes ?? '') : ''))
		.join(' ');
	return scanMaterials(text)[0]?.mat;
}

function laserSection(b: B): Scene {
	const st = b.st, c = b.r.comp;
	const [wr] = b.or('ridge_width_um', () => 2);
	const iii = st.core === 'inp' || st.core === 'gaas' ? st.core : 'inp';
	const wgMat = laserLayerMat(b);
	if (c.class === 'laser.heterogeneous' && wgMat && wgMat !== 'inp' && wgMat !== 'gaas') return hetLaserSection(b, wgMat, wr, iii);
	const [ta] = b.or('core_thickness_nm', () => 0.15 * wr);
	const [h] = b.or('etch_depth_nm', () => 0.75 * wr);
	const X = Math.max(2.2 * wr, 2 * h);
	const lowN = 1.2 * h;
	const membrane = c.platform === 'inp_membrane';
	if (st.box === 'none') b.rect(-X, -lowN, X, 0, st.substrate, 'substrate / lower cladding', [], { schematic: true, alpha: 0.6, tip: 'lower cladding / substrate thickness is not a template dimension' });
	else if (membrane) {
		b.rect(-X, -lowN - 0.4 * lowN, X, -lowN, 'si', 'substrate', [], { schematic: true, alpha: 0.5 });
		b.rect(-X, -lowN, X, 0, 'sio2', 'BOX / bottom reflector', [], { schematic: true, tip: 'layers under the membrane: not template dimensions' });
		b.notes.push('III-V membrane on oxide: layers under the membrane not drawn individually (not template dimensions)');
	} else {
		b.rect(-X, -lowN - 0.4 * lowN, X, -lowN, 'si', 'substrate', [], { schematic: true, alpha: 0.5 });
		b.rect(-X, -lowN, X, -0.35 * lowN, 'sio2', 'BOX', [], { schematic: true, tip: 'BOX / bonding layer: not a template dimension' });
		b.rect(-X, -0.35 * lowN, X, 0, iii, 'III-V lower cladding', [], { schematic: true });
		b.notes.push('layers below the III-V drawn schematically (not template dimensions; no waveguide row below the III-V)');
	}
	b.rect(-X, 0, X, ta, membrane ? iii : 'active', membrane ? 'III-V membrane' : 'active layer', ['core_thickness_nm'], { tip: membrane ? 'membrane (core) layer: core_thickness_nm' : 'active / core layer (material not parsed)' }, membrane ? 'core' : 'active');
	b.rect(-wr / 2, ta, wr / 2, ta + h, iii, 'ridge', ['ridge_width_um', 'etch_depth_nm'], {}, 'ridge');
	b.mark('ridge_width_um', 'h', -wr / 2, wr / 2, [ta + h, ta + h], ta + h, 12);
	b.mark('core_thickness_nm', 'v', 0, ta, [X, X], X, 8);
	b.mark('etch_depth_nm', 'v', ta, ta + h, [-wr / 2, -wr / 2], -X, -8);
	b.notes.push('shallow ridge drawn (active layer not etched); contacts not drawn');
	return b.scene('cross-section (lateral)');
}

/** Heterogeneous laser whose core_thickness_nm / etch_depth_nm rows describe the waveguide under the III-V (D220): the
 *  waveguide is drawn from its rows (width_nm when reported), the III-V mesa at ridge_width_um; III-V layer heights,
 *  bonding layer and BOX are not template dimensions (dashed). */
function hetLaserSection(b: B, wgMat: string, wr: number, iii: string): Scene {
	const [t] = b.or('core_thickness_nm', () => 0.15 * wr);
	const etch = b.has('etch_depth_nm') ? b.v('etch_depth_nm') : null;
	const slab = etch !== null && etch < t ? t - etch : 0;
	const wd = b.r.dims.width_nm ?? resolveDim(b.r.comp, 'width_nm', ['xsec'], false, 'waveguide width under the III-V');
	const ws = wd.num !== null && wd.num > 0 ? wd.num : 0.4 * wr;
	const gb = 0.15 * t, hm = 0.6 * wr, lowN = Math.max(3 * t, 0.5 * wr);
	const X = Math.max(1.6 * wr, 1.5 * ws);
	const yb = t + gb;
	const wName = MATERIALS[wgMat] ?? wgMat;
	b.rect(-X, -lowN - 0.4 * lowN, X, -lowN, 'si', 'substrate', [], { schematic: true, alpha: 0.5 });
	b.rect(-X, -lowN, X, 0, 'sio2', 'BOX', [], { schematic: true, tip: 'BOX thickness: not a template dimension' });
	if (slab > 0) b.rect(-X, 0, X, slab, wgMat, wName + ' slab', ['core_thickness_nm', 'etch_depth_nm'], {}, 'core');
	b.rect(-ws / 2, slab, ws / 2, t, wgMat, wName + ' waveguide', ['core_thickness_nm'], { schematic: !b.has('core_thickness_nm') || wd.num === null, tip: 'layer named in the row text (D220)' + (wd.num === null ? '; width not reported' : '') }, 'core');
	b.rect(-X, t, X, yb, 'unknown', 'bonding / interlayer', [], { schematic: true, tip: 'bonding layer: not a template dimension' });
	b.rect(-wr / 2, yb, wr / 2, yb + hm, iii, 'III-V mesa', ['ridge_width_um'], { schematic: true, tip: 'mesa width: ridge_width_um; III-V layer heights (active, cladding) not reported' }, 'ridge');
	b.mark('ridge_width_um', 'h', -wr / 2, wr / 2, [yb + hm, yb + hm], yb + hm, 12);
	b.mark('core_thickness_nm', 'v', 0, t, [slab > 0 ? X : ws / 2, ws / 2], X, 8);
	if (etch !== null) b.mark('etch_depth_nm', 'v', t - etch, t, [-ws / 2, -ws / 2], -X, -8);
	b.mark(wd, 'h', -ws / 2, ws / 2, [slab, slab], 0, -14);
	b.notes.push(`heterogeneous stack: core_thickness_nm / etch_depth_nm drawn on the ${wName} waveguide (layer named in the row text); III-V layer heights, bonding layer and BOX not reported (dashed)`);
	return b.scene('cross-section (lateral)');
}

// ---------- top views ----------

function gcTop(b: B): Scene {
	const core = b.st.core;
	const [P] = b.or('period_nm', () => 0.6);
	const [ff] = b.or('fill_factor', () => 0.5);
	let Lg: number, LgFromN = false;
	if (b.has('grating_length_um')) Lg = b.v('grating_length_um');
	else if (b.has('n_periods') && b.has('period_nm')) [Lg, LgFromN] = [b.v('n_periods') * P, true];
	else Lg = b.has('n_periods') ? b.v('n_periods') * P : 20 * P;
	const [Wg] = b.or('grating_width_um', () => 0.8 * Lg);
	const [Lt] = b.or('taper_length_um', () => 1.5 * Lg);
	const [w] = b.or('width_nm', () => Wg / 24);
	const lead = 0.2 * Lt;
	b.rect(-Lt - lead, -w / 2, -Lt, w / 2, core, 'access waveguide', ['width_nm'], {}, 'core');
	b.poly([[-Lt, -w / 2], [0, -Wg / 2], [0, Wg / 2], [-Lt, w / 2]], core, 'taper', ['taper_length_um', 'width_nm', 'grating_width_um'], {}, 'core');
	const gParams = ['period_nm', 'fill_factor', LgFromN ? 'n_periods' : 'grating_length_um', 'grating_width_um'];
	b.rect(0, -Wg / 2, Lg, Wg / 2, core, 'grating region (etched)', gParams, { alpha: 0.35 }, 'core');
	const nT = Math.floor(Lg / P + 1e-6);
	if (nT <= 400) for (let i = 0; i < nT; i++) b.rect(i * P, -Wg / 2, i * P + ff * P, Wg / 2, core, 'grating tooth', gParams, {}, 'core');
	else b.notes.push('grating teeth not drawn individually (too many periods for this view)');
	b.mark('taper_length_um', 'h', -Lt, 0, [-w / 2, -Wg / 2], -Wg / 2, -14);
	if (b.has('grating_length_um') || !LgFromN) b.mark('grating_length_um', 'h', 0, Lg, [-Wg / 2, -Wg / 2], -Wg / 2, -14);
	else {
		b.val('n_periods', [Lg / 2, -Wg / 2], 'periods', 'middle', 0, 28);
		b.notes.push('grating length drawn as n_periods x period');
	}
	b.mark('grating_width_um', 'v', -Wg / 2, Wg / 2, [Lg, Lg], Lg, 8);
	b.mark('width_nm', 'v', -w / 2, w / 2, [-Lt - lead, -Lt - lead], -Lt - lead, -8);
	b.mark('period_nm', 'h', 0, P, [Wg / 2, Wg / 2], Wg / 2, 12);
	if (b.has('n_periods') && !LgFromN) b.val('n_periods', [Lg / 2, -Wg / 2], 'periods', 'middle', 0, 28);
	b.val('fill_factor', [Lg, Wg / 2], 'ff', 'start', 8, -6);
	return b.scene('top view');
}

function edgeTop(b: B): Scene {
	const core = b.st.core;
	const tipR = b.has('tip_width_nm');
	const [w] = b.or('width_nm', () => (tipR ? 2.5 * b.v('tip_width_nm') : 0.5));
	const [tip] = b.or('tip_width_nm', () => 0.3 * w);
	const segs = segmentRows(b.r.comp, 'taper_length_um');
	if (segs.length) b.segs.add('taper_length_um');
	const [Lt0] = b.or('taper_length_um', () => 300 * w);
	const Lt = segs.length ? segs.reduce((acc, m) => acc + (resolveDim(b.r.comp, 'taper_length_um', ['top'], true, '', m).num as number), 0) : Lt0;
	const lead = 0.25 * Lt;
	if (b.has('overlay_width_um')) {
		const wo = b.v('overlay_width_um');
		b.rect(-0.05 * Lt, -wo / 2, Lt, wo / 2, b.st.overlay, 'overlay', ['overlay_width_um'], { alpha: 0.4, schematic: true, tip: 'overlay start position is not a template dimension (drawn over the taper)' }, 'overlay');
		b.mark('overlay_width_um', 'v', -wo / 2, wo / 2, [Lt, Lt], Lt, 44, false, true);
	}
	b.rect(-lead, -w / 2, 0, w / 2, core, 'waveguide', ['width_nm'], {}, 'core');
	if (segs.length) {
		// Several taper_length_um rows that differ by condition: consecutive sections, each labelled with its own row.
		let x = 0;
		const wAt = (xx: number) => w + ((tip - w) * xx) / Lt;
		segs.forEach((m, i) => {
			const d = { ...resolveDim(b.r.comp, 'taper_length_um', ['top'], true, '', m), alts: [] }; // other sections listed in the tip, no '*'
			const L = d.num as number;
			b.poly([[x, -wAt(x) / 2], [x + L, -wAt(x + L) / 2], [x + L, wAt(x + L) / 2], [x, wAt(x) / 2]], core, 'taper section', ['taper_length_um', 'width_nm', 'tip_width_nm'], { schematic: true, tip: 'section ' + (m.condition ?? '') + '\nwidths between sections not reported (linear schematic)' }, 'core');
			b.mark(d, 'h', x, x + L, [-wAt(x) / 2, -wAt(x + L) / 2], -w / 2, -14);
			x += L;
		});
		b.notes.push('taper drawn as consecutive sections in row order, one row each; widths between sections not reported');
	} else b.poly([[0, -w / 2], [Lt, -tip / 2], [Lt, tip / 2], [0, w / 2]], core, 'inverse taper', ['taper_length_um', 'width_nm', 'tip_width_nm'], {}, 'core');
	const fh = Math.max(w * 2.5, tip * 2.5, b.has('overlay_width_um') ? 0.62 * b.v('overlay_width_um') : 0);
	b.shapes.push({ rings: [[[Lt, -fh], [Lt, fh]]], mat: 'unknown', role: 'chip facet', schematic: false, line: true, tip: 'chip facet' });
	b.text([Lt, fh], 'facet', 'middle', 0, -6);
	if (!segs.length) b.mark('taper_length_um', 'h', 0, Lt, [-w / 2, -tip / 2], -w / 2, -14);
	b.mark('tip_width_nm', 'v', -tip / 2, tip / 2, [Lt, Lt], Lt, 8);
	b.mark('width_nm', 'v', -w / 2, w / 2, [-lead, -lead], -lead, -8);
	return b.scene('top view');
}

function transitionTop(b: B): Scene {
	const st = b.st;
	// width_nm is the upper-layer width, lower_width_nm the lower-layer width (D111); a missing one is drawn at the
	// other's value (schematic).
	const lw = 'lower_width_nm';
	const [w] = b.or(lw, () => (b.has('width_nm') ? b.v('width_nm') : 0.8));
	const upW = b.has('width_nm');
	const wu = upW ? b.v('width_nm') : w;
	const useLen = !b.has('taper_length_um') && b.has('length_um');
	const L = b.has('taper_length_um') ? b.v('taper_length_um') : useLen ? b.v('length_um') : 100 * w;
	const [tipU] = b.or('tip_width_nm', () => 0.2 * w);
	const [tipL] = b.or('lower_tip_width_nm', () => 0.2 * w);
	const lead = 0.3 * L;
	b.rect(-lead, -w / 2, 0, w / 2, st.core, 'lower layer', [lw], {}, 'core');
	b.poly([[0, -w / 2], [L, -tipL / 2], [L, tipL / 2], [0, w / 2]], st.core, 'lower taper', [useLen ? 'length_um' : 'taper_length_um', lw, 'lower_tip_width_nm'], {}, 'core');
	b.poly([[0, -tipU / 2], [L, -wu / 2], [L + lead, -wu / 2], [L + lead, wu / 2], [L, wu / 2], [0, tipU / 2]], st.layer2, 'upper taper', [useLen ? 'length_um' : 'taper_length_um', 'tip_width_nm', ...(upW ? ['width_nm'] : [])], { alpha: 0.55, schematic: upW ? undefined : true, tip: 'upper-layer width: width_nm; lower layer: lower_width_nm' }, 'layer2');
	b.mark(useLen ? 'length_um' : 'taper_length_um', 'h', 0, L, [-w / 2, -w / 2], -w / 2, -14);
	if (b.has('length_um') && !useLen) b.mark('length_um', 'h', 0, b.v('length_um'), [w / 2, w / 2], w / 2, 14);
	b.mark('tip_width_nm', 'v', -tipU / 2, tipU / 2, [0, 0], 0, 8);
	b.mark('lower_tip_width_nm', 'v', -tipL / 2, tipL / 2, [L, L], L, 8);
	b.mark(lw, 'v', -w / 2, w / 2, [-lead, -lead], -lead, -8);
	b.mark('width_nm', 'v', -wu / 2, wu / 2, [L + lead, L + lead], L + lead, 8);
	b.notes.push('tapers drawn co-located over the taper length; layer roles from the platform');
	return b.scene('top view');
}

function wgTop(b: B): Scene {
	const core = b.st.core;
	const [w] = b.or('width_nm', () => 0.5);
	if (b.has('min_bend_radius_um')) {
		const R = b.v('min_bend_radius_um');
		const c: Pt[] = [[-0.4 * R, 0], ...Array.from({ length: 61 }, (_, i) => [R * Math.sin((Math.PI / 2) * (i / 60)), R - R * Math.cos((Math.PI / 2) * (i / 60))] as Pt), [R, 1.4 * R]];
		b.poly(strip(c, () => w), core, 'waveguide bend', ['width_nm', 'min_bend_radius_um'], {}, 'core');
		b.text([0, R], '+', 'middle', 0, 4, 'bend centre');
		b.mark('min_bend_radius_um', 'h', 0, R, [R, R], R, 0);
		b.mark('width_nm', 'v', -w / 2, w / 2, [-0.4 * R, -0.4 * R], -0.4 * R, -8);
		return b.scene('top view (bend at the minimum radius)', { stretch: false });
	}
	const [L] = b.or('length_um', () => 30 * w);
	if (b.has('length_um') && L > 1000 * w) {
		// D228: a length far beyond the width is drawn with a break (drafting convention): two short runs, a break mark,
		// the length as a label across the whole drawn extent. The x extent is not to scale.
		const a = 16 * w, gp = 4 * w, E = 2 * a + gp;
		b.rect(0, -w / 2, a, w / 2, core, 'waveguide (start)', ['width_nm'], { tip: 'length drawn with a break: x extent not to scale' }, 'core');
		b.rect(a + gp, -w / 2, E, w / 2, core, 'waveguide (end)', ['width_nm'], { tip: 'length drawn with a break: x extent not to scale' }, 'core');
		for (const x of [a + 0.25 * gp, a + 0.75 * gp]) b.shapes.push({ rings: [[[x - 0.6 * w, -1.6 * w], [x + 0.6 * w, 1.6 * w]]], mat: 'unknown', role: 'break', schematic: false, line: true, tip: 'break: the waveguide continues (length on the label; layout shape, e.g. spiral, not drawn)' });
		b.mark('length_um', 'h', 0, E, [-w / 2, -w / 2], -w / 2, -14);
		b.mark('width_nm', 'v', -w / 2, w / 2, [0, 0], 0, -8);
		b.notes.push('length drawn with a break (length far above the width): x extent not to scale; routing shape not drawn');
		return b.scene('top view', { stretch: false, partial: true, schematic: !b.has('width_nm') });
	}
	b.rect(0, -w / 2, L, w / 2, core, 'waveguide', ['width_nm', 'length_um'], {}, 'core');
	b.mark('length_um', 'h', 0, L, [-w / 2, -w / 2], -w / 2, -14);
	b.mark('width_nm', 'v', -w / 2, w / 2, [0, 0], 0, -8);
	return b.scene('top view', { stretch: b.has('length_um') });
}

function ringTop(b: B): Scene {
	const core = b.st.core, cls = b.r.comp.class;
	const [w] = b.or('width_nm', () => 0.8);
	const [R] = b.or('radius_um', () => 25 * w);
	const [g] = b.or('gap_nm', () => 0.6 * w);
	const [wb] = b.or('bus_width_nm', () => w);
	const Lc = b.has('coupling_length_um') ? b.v('coupling_length_um') : 0;
	const rp = ['radius_um', 'width_nm', ...(Lc ? ['coupling_length_um'] : [])];
	// Ring / racetrack centreline (straights of length Lc at top and bottom), counter-clockwise from the bottom middle.
	const cl: Pt[] = [];
	const n = 90;
	for (let i = 0; i <= n; i++) cl.push([Lc / 2 + R * Math.sin((Math.PI * i) / n), -R * Math.cos((Math.PI * i) / n)]);
	for (let i = 0; i <= n; i++) cl.push([-Lc / 2 - R * Math.sin((Math.PI * i) / n), R * Math.cos((Math.PI * i) / n)]);
	const off = (h: number): Pt[] =>
		cl.map(([x, y]) => {
			const cx = x > Lc / 2 ? Lc / 2 : x < -Lc / 2 ? -Lc / 2 : x;
			const dx = x - cx, dy = y, nn = Math.hypot(dx, dy) || 1;
			return [x + (dx / nn) * h, y + (dy / nn) * h] as Pt;
		});
	b.shapes.push({ rings: [off(w / 2), off(-w / 2)], mat: core, role: Lc ? 'racetrack' : 'ring', schematic: rp.some((p) => !b.has(p)), tip: b.tip(Lc ? 'racetrack' : 'ring', 'core', core, rp) });
	const yb = -R - w / 2 - g - wb / 2, X = Lc / 2 + 1.35 * R;
	b.rect(-X, yb - wb / 2, X, yb + wb / 2, core, 'bus waveguide', ['bus_width_nm', 'gap_nm'], {}, 'core');
	if (b.has('heater_width_um')) {
		const wh = b.v('heater_width_um');
		const hc = cl.slice(Math.round(cl.length * 0.12), Math.round(cl.length * 0.88));
		b.poly(strip(hc, () => wh), 'metal', 'heater', ['heater_width_um'], { alpha: 0.45, tip: 'heater arc extent is not a template dimension' }, 'heater');
		b.val('heater_width_um', [0, R + wh], 'heater', 'middle', 0, -6);
	}
	b.text([0, 0], '+', 'middle', 0, 4, 'ring centre');
	b.mark('radius_um', 'h', Lc / 2, Lc / 2 + R, [0, 0], 0, 0);
	if (Lc) b.mark('coupling_length_um', 'h', -Lc / 2, Lc / 2, [R + w / 2, R + w / 2], R + w / 2, 12);
	// Coupling region: true-scale inset (both axes equal).
	const half = Math.max(1.6 * (w + g + wb), 0.5);
	const yc = -R - w / 2 - g / 2;
	b.mark('gap_nm', 'v', -R - w / 2 - g, -R - w / 2, [-0.3 * half, -0.3 * half], -0.3 * half, 0, true);
	b.mark('width_nm', 'v', -R - w / 2, -R + w / 2, [-0.8 * half, -0.8 * half], -0.8 * half, 0, true);
	b.mark('bus_width_nm', 'v', yb - wb / 2, yb + wb / 2, [0.3 * half, 0.3 * half], 0.3 * half, 0, true);
	// UI audit 13: also rings whose label states a second bus (add-drop / two-bus)
	if (cls === 'wdm.mrr' || /add[-/]drop|\b(two|double|dual)[- ]bus/i.test(b.r.comp.label)) b.notes.push('single bus drawn (drop port not a template dimension)');
	if (cls === 'resonator.coupled_rings') b.notes.push('coupled rings: one ring drawn');
	return b.scene('top view', { stretch: false, inset: { c: [0, yc], half } });
}

function mmiTop(b: B): Scene {
	const core = b.st.core, c = b.r.comp;
	const fromLabel = /\b([1-9])\s*[xX]\s*([1-9]|1[0-6])\b/.exec(c.label);
	const crossing = c.class === 'crossing.mmi';
	const nIn = b.has('n_inputs') ? b.v('n_inputs') : crossing ? 1 : fromLabel ? Number(fromLabel[1]) : 1;
	const nOut = b.has('n_outputs') ? b.v('n_outputs') : crossing ? 1 : fromLabel ? Number(fromLabel[2]) : 2;
	const portsFrom = b.has('n_inputs') && b.has('n_outputs') ? '' : crossing ? 'crossing' : fromLabel ? 'label' : 'default';
	const [L] = b.or('mmi_length_um', () => (b.has('mmi_width_um') ? 8 * b.v('mmi_width_um') : 40));
	const [W] = b.or('mmi_width_um', () => L / 8);
	const nMax = Math.max(nIn, nOut);
	const [pitch] = b.or('pitch_um', () => W / Math.max(nMax, 2));
	const [pw] = b.or('port_width_um', () => 0.6 * pitch);
	const [w] = b.or('width_nm', () => 0.4 * pw);
	const [Lt] = b.or('taper_length_um', () => 0.3 * L);
	const lead = 0.15 * L;
	const ys = (n: number) => Array.from({ length: n }, (_, i) => (i - (n - 1) / 2) * pitch);
	const portP = ['port_width_um', 'width_nm', 'taper_length_um', 'pitch_um'];
	const ports = (x0: number, dir: 1 | -1, n: number) => {
		for (const y of ys(n)) {
			const xa = dir > 0 ? x0 : x0 - Lt, xb = dir > 0 ? x0 + Lt : x0;
			const [wa, wb] = dir > 0 ? [pw, w] : [w, pw];
			b.poly([[xa, y - wa / 2], [xb, y - wb / 2], [xb, y + wb / 2], [xa, y + wa / 2]], core, 'access taper', portP, {}, 'core');
			const xl = dir > 0 ? x0 + Lt : x0 - Lt - lead;
			b.rect(xl, y - w / 2, xl + lead, y + w / 2, core, 'access waveguide', ['width_nm'], { schematic: portsFrom !== '' ? true : undefined }, 'core');
		}
	};
	b.rect(0, -W / 2, L, W / 2, core, 'multimode section', ['mmi_width_um', 'mmi_length_um'], {}, 'core');
	ports(0, -1, nIn);
	ports(L, 1, nOut);
	if (crossing) {
		b.rect(L / 2 - W / 2, -L / 2, L / 2 + W / 2, L / 2, core, 'multimode section (crossing arm)', ['mmi_width_um', 'mmi_length_um'], { alpha: 0.7 }, 'core');
		b.notes.push('MMI crossing drawn as two orthogonal multimode sections');
	}
	if (portsFrom === 'label') b.notes.push('port count from the component label (n_inputs / n_outputs not reported)');
	if (portsFrom === 'default') b.notes.push('port count not reported (one input, two outputs drawn)');
	const yTop = ys(nOut)[nOut - 1];
	b.mark('mmi_length_um', 'h', 0, L, [-W / 2, -W / 2], -W / 2, -14);
	b.mark('mmi_width_um', 'v', -W / 2, W / 2, [L / 2, L / 2], L / 2, 0);
	b.mark('taper_length_um', 'h', L, L + Lt, [yTop + pw / 2, yTop + w / 2], Math.max(yTop + pw / 2, W / 2), 12);
	b.mark('port_width_um', 'v', yTop - pw / 2, yTop + pw / 2, [L, L], L, 4);
	if (nOut > 1) b.mark('pitch_um', 'v', ys(nOut)[0], yTop, [L + Lt + lead, L + Lt + lead], L + Lt + lead, 8);
	b.mark('width_nm', 'v', ys(nIn)[0] - w / 2, ys(nIn)[0] + w / 2, [-Lt - lead, -Lt - lead], -Lt - lead, -8);
	if (b.has('n_inputs')) b.val('n_inputs', [-Lt - lead, -W / 2], 'inputs', 'start', 0, 14);
	if (b.has('n_outputs')) b.val('n_outputs', [L + Lt + lead, -W / 2], 'outputs', 'end', 0, 14);
	return b.scene('top view');
}

function dcTop(b: B): Scene {
	const core = b.st.core;
	const [w] = b.or('width_nm', () => 0.5);
	const [g] = b.or('gap_nm', () => 0.6 * w);
	const [Lc] = b.or('coupling_length_um', () => 40 * w);
	const dy = Math.max(4 * w, 0.12 * Lc);
	const Rr = b.has('min_bend_radius_um');
	let Lb = Rr ? arcLen(b.v('min_bend_radius_um'), dy) : 0.5 * Lc;
	if (!Rr && b.has('length_um') && b.v('length_um') > Lc) Lb = (b.v('length_um') - Lc) / 2;
	const yc = g / 2 + w / 2, lead = 0.15 * Lc;
	const bendP = ['width_nm', 'min_bend_radius_um'];
	for (const s of [1, -1] as const) {
		const y = s * yc, yo = s * (yc + dy);
		b.rect(0, y - w / 2, Lc, y + w / 2, core, 'coupling section', ['width_nm', 'gap_nm', 'coupling_length_um'], {}, 'core');
		const left = Rr ? arcSbend(-Lb, yo, b.v('min_bend_radius_um'), y - yo) : sbend(-Lb, yo, Lb, y - yo);
		const right = Rr ? arcSbend(Lc, y, b.v('min_bend_radius_um'), yo - y) : sbend(Lc, y, Lb, yo - y);
		b.poly(strip(left, () => w), core, 'S-bend', bendP, { tip: Rr ? 'two-arc S-bend at the minimum bend radius; lateral offset schematic' : 'bend shape and offset not reported' }, 'core');
		b.poly(strip(right, () => w), core, 'S-bend', bendP, { tip: Rr ? 'two-arc S-bend at the minimum bend radius; lateral offset schematic' : 'bend shape and offset not reported' }, 'core');
		b.rect(-Lb - lead, yo - w / 2, -Lb, yo + w / 2, core, 'access waveguide', ['width_nm'], {}, 'core');
		b.rect(Lc + Lb, yo - w / 2, Lc + Lb + lead, yo + w / 2, core, 'access waveguide', ['width_nm'], {}, 'core');
	}
	if (b.r.comp.class === 'splitter.adiabatic') b.notes.push('adiabatic coupler drawn as a uniform coupling section (taper profile not a template dimension)');
	b.mark('coupling_length_um', 'h', 0, Lc, [-yc - w / 2, -yc - w / 2], -yc - dy - w / 2, -14);
	b.mark('gap_nm', 'v', -g / 2, g / 2, [Lc / 2, Lc / 2], Lc / 2, 0);
	b.mark('width_nm', 'v', yc + dy - w / 2, yc + dy + w / 2, [-Lb - lead, -Lb - lead], -Lb - lead, -8);
	if (b.has('length_um')) b.mark('length_um', 'h', -Lb, Lc + Lb, [yc + dy + w / 2, yc + dy + w / 2], yc + dy + w / 2, 14);
	if (Rr) b.val('min_bend_radius_um', [-Lb / 2, yc + dy / 2], 'R', 'end', -6, 0);
	return b.scene('top view');
}

function yTop(b: B): Scene {
	const core = b.st.core;
	const [w] = b.or('width_nm', () => 0.5);
	const [L] = b.or('length_um', () => 30 * w);
	const [p] = b.or('pitch_um', () => Math.max(0.1 * L, 3 * w));
	const lead = 0.3 * L;
	b.rect(-lead, -w / 2, 0, w / 2, core, 'input waveguide', ['width_nm'], {}, 'core');
	for (const s of [1, -1]) {
		b.poly(strip(sbend(0, 0, L, (s * p) / 2), () => w), core, 'branch', ['width_nm', 'length_um', 'pitch_um'], { tip: 'branch curve shape not reported (cosine S-bend drawn)' }, 'core');
		b.rect(L, (s * p) / 2 - w / 2, L + lead, (s * p) / 2 + w / 2, core, 'output waveguide', ['width_nm', 'pitch_um'], {}, 'core');
	}
	b.mark('length_um', 'h', 0, L, [-w / 2, -p / 2 - w / 2], -p / 2 - w / 2, -14);
	b.mark('pitch_um', 'v', -p / 2, p / 2, [L + lead, L + lead], L + lead, 8);
	b.mark('width_nm', 'v', -w / 2, w / 2, [-lead, -lead], -lead, -8);
	return b.scene('top view');
}

function awgTop(b: B): Scene {
	// Schematic only (template: "schematic: FPRs + array"): shapes are not to scale; labels carry the data.
	const core = b.st.core;
	const nA = b.has('n_arms') ? b.v('n_arms') : null, nC = b.has('n_channels') ? b.v('n_channels') : null;
	const kA = Math.min(nA ?? 7, 9), kC = Math.min(nC ?? 4, 8);
	const F = 30, gap = 60, H = 40;
	const fpr = (x0: number, flip: boolean): Pt[] => {
		const pts: Pt[] = [];
		for (let i = 0; i <= 20; i++) {
			const a = -0.6 + (1.2 * i) / 20;
			pts.push([x0 + (flip ? -1 : 1) * F * Math.cos(a), H / 2 * Math.sin(a) * 1.6]);
		}
		return [[x0, -2], ...pts, [x0, 2]];
	};
	b.poly(fpr(0, false), core, 'free-propagation region', ['fpr_length_um'], { schematic: true }, 'core');
	b.poly(fpr(2 * F + gap, true), core, 'free-propagation region', ['fpr_length_um'], { schematic: true }, 'core');
	for (let i = 0; i < kA; i++) {
		const f = kA > 1 ? i / (kA - 1) : 0.5;
		const yA = (f - 0.5) * H * 1.3, rise = 12 + 26 * f;
		const cl: Pt[] = Array.from({ length: 41 }, (_, j) => {
			const s = j / 40;
			return [F + s * gap, yA + rise * Math.sin(Math.PI * s)] as Pt;
		});
		b.poly(strip(cl, () => 0.9), core, 'arrayed waveguide', ['n_arms', 'arm_length_increment_um'], { schematic: true }, 'core');
	}
	b.rect(-14, -0.45, 0, 0.45, core, 'input waveguide', [], { schematic: true }, 'core');
	for (let i = 0; i < kC; i++) {
		const y = (kC > 1 ? i / (kC - 1) - 0.5 : 0) * H * 0.7;
		b.rect(2 * F + gap, y - 0.45, 2 * F + gap + 14, y + 0.45, core, 'output waveguide', ['n_channels'], { schematic: true }, 'core');
	}
	const tx = F + gap / 2;
	b.val('n_arms', [tx, -H * 0.85], 'arms', 'middle');
	b.val('n_channels', [2 * F + gap + 14, H * 0.45], 'channels', 'end', 0, -6);
	b.val('fpr_length_um', [F / 2, -H * 0.62], 'FPR', 'middle');
	b.val('arm_length_increment_um', [tx, H * 1.75], 'ΔL', 'middle');
	if (b.has('diffraction_order')) b.val('diffraction_order', [tx, H * 2], 'order', 'middle');
	if (b.has('footprint_um2')) b.val('footprint_um2', [tx, -H * 1.15], 'footprint', 'middle');
	if (b.has('width_nm')) b.val('width_nm', [-14, 0], 'width', 'start', 0, -8);
	b.notes.push('schematic: arm count, path lengths and region sizes are not drawn to scale');
	return b.scene('top view (schematic)', { stretch: false, schematic: true });
}

function pdTop(b: B): Scene {
	const core = b.st.core;
	const [w] = b.or('width_nm', () => 0.5);
	const [La] = b.or('absorber_length_um', () => (b.has('length_um') ? b.v('length_um') : 20));
	const [Wa] = b.or('absorber_width_um', () => 0.12 * La);
	const lead = 0.4 * La;
	b.rect(-lead, -w / 2, 0, w / 2, core, 'waveguide', ['width_nm'], {}, 'core');
	b.rect(-0.03 * La, -0.7 * Wa, 1.03 * La, 0.7 * Wa, core, 'Si region under the absorber', [], { schematic: true, alpha: 0.5, tip: 'region under the absorber is not a template dimension' }, 'core');
	b.rect(0, -Wa / 2, La, Wa / 2, b.st.absorber, 'absorber', ['absorber_length_um', 'absorber_width_um'], {}, 'absorber');
	b.mark('absorber_length_um', 'h', 0, La, [Wa / 2, Wa / 2], 0.7 * Wa, 12);
	b.mark('absorber_width_um', 'v', -Wa / 2, Wa / 2, [La, La], 1.03 * La, 8);
	b.mark('width_nm', 'v', -w / 2, w / 2, [-lead, -lead], -lead, -8);
	if (b.has('length_um')) b.mark('length_um', 'h', 0, b.v('length_um'), [-0.7 * Wa, -0.7 * Wa], -0.7 * Wa, -14);
	if (!b.has('absorber_length_um') && b.has('length_um')) b.notes.push('absorber drawn at the device length (absorber_length_um not reported)');
	return b.scene('top view');
}

function heaterTop(b: B): Scene {
	const core = b.st.core;
	const [w] = b.or('width_nm', () => 0.5);
	const [Lh] = b.or('heater_length_um', () => (b.has('length_um') ? b.v('length_um') : 200 * w));
	const [Wh] = b.or('heater_width_um', () => Math.max(4 * w, 0.01 * Lh));
	const lead = 0.15 * Lh;
	b.rect(-lead, -w / 2, Lh + lead, w / 2, core, 'waveguide', ['width_nm'], {}, 'core');
	b.rect(0, -Wh / 2, Lh, Wh / 2, b.st.heater, 'heater', ['heater_length_um', 'heater_width_um'], { alpha: 0.5 }, 'heater');
	b.mark('heater_length_um', 'h', 0, Lh, [Wh / 2, Wh / 2], Wh / 2, 12);
	b.mark('heater_width_um', 'v', -Wh / 2, Wh / 2, [Lh, Lh], Lh + lead, 8);
	b.mark('width_nm', 'v', -w / 2, w / 2, [-lead, -lead], -lead, -8);
	if (b.has('length_um')) b.mark('length_um', 'h', 0, b.v('length_um'), [-Wh / 2, -Wh / 2], -Wh / 2, -14);
	if (!b.has('heater_length_um') && b.has('length_um')) b.notes.push('heater drawn at the device length (heater_length_um not reported)');
	b.notes.push('contacts / pads not drawn');
	return b.scene('top view');
}

function laserTop(b: B): Scene {
	const iii = b.st.core === 'gaas' ? 'gaas' : 'inp';
	const [L] = b.or('length_um', () => 500);
	const [wr] = b.or('ridge_width_um', () => L / 200);
	const nC = b.has('n_channels') ? b.v('n_channels') : 1;
	const k = Math.min(nC, 8);
	const [p] = b.or('pitch_um', () => 12 * wr);
	for (let i = 0; i < k; i++) {
		const y = (i - (k - 1) / 2) * p;
		b.rect(0, y - wr / 2, L, y + wr / 2, iii, 'ridge / cavity', ['length_um', 'ridge_width_um'], {}, 'ridge');
		if (b.has('period_nm')) b.rect(0, y - wr / 2, L, y + wr / 2, iii, 'grating', ['period_nm'], { hatch: true, alpha: 0.9, tip: 'grating: period far below the drawing resolution (hatch, not to scale)' }, 'ridge');
	}
	if (nC > k) b.notes.push('array truncated in the drawing');
	const y0 = -((k - 1) / 2) * p;
	b.mark('length_um', 'h', 0, L, [y0 - wr / 2, y0 - wr / 2], y0 - wr / 2, -14);
	b.mark('ridge_width_um', 'v', y0 - wr / 2, y0 + wr / 2, [0, 0], 0, -8);
	if (k > 1) b.mark('pitch_um', 'v', y0, y0 + p, [L, L], L, 8);
	if (b.has('n_channels')) b.val('n_channels', [L, -y0 + wr / 2], 'channels', 'end', 0, -8);
	if (b.has('period_nm')) b.val('period_nm', [L / 2, -y0 + wr / 2], 'grating period', 'middle', 0, -8);
	b.text([0, -y0 + wr / 2], 'facet', 'middle', 0, -8);
	b.text([L, y0 - wr / 2], 'facet', 'middle', 0, 30);
	return b.scene('top view');
}

/** Both scenes of a resolved component. */
export function buildScenes(r: Resolved): { top: Scene; xsec: Scene } {
	const T = (f: (b: B) => Scene) => f(new B(r, 'top'));
	const X = (f: (b: B) => Scene) => f(new B(r, 'xsec'));
	switch (r.templateId) {
		case 'gc_1d':
			return { top: T(gcTop), xsec: X(gcSection) };
		case 'edge_taper':
			return { top: T(edgeTop), xsec: X((b) => xsecStack(b, { wParam: 'tip_width_nm', overlay: true, title: 'cross-section at the facet (tip)' })) };
		case 'transition_bilayer':
			return { top: T(transitionTop), xsec: X((b) => xsecStack(b, { wParam: 'lower_width_nm', layer2: true, title: 'cross-section (layer stack at the lower-layer input)' })) };
		case 'waveguide_xsec':
			return { top: T(wgTop), xsec: X((b) => xsecStack(b)) };
		case 'ring_bus':
			return { top: T(ringTop), xsec: X((b) => xsecStack(b, { title: 'cross-section (ring waveguide)' })) };
		case 'mmi':
			return { top: T(mmiTop), xsec: X((b) => xsecStack(b, { title: 'cross-section (access waveguide)' })) };
		case 'dc':
			return { top: T(dcTop), xsec: X((b) => xsecStack(b)) };
		case 'y_branch':
			return { top: T(yTop), xsec: X((b) => xsecStack(b)) };
		case 'awg':
			return { top: T(awgTop), xsec: X((b) => xsecStack(b, { title: 'cross-section (array waveguide)' })) };
		case 'ge_pd':
			return { top: T(pdTop), xsec: X((b) => xsecStack(b, { absorber: true, title: 'cross-section (absorber on waveguide)' })) };
		case 'heater_ps':
			return { top: T(heaterTop), xsec: X((b) => xsecStack(b, { heater: true })) };
		case 'ridge_laser':
			return { top: T(laserTop), xsec: X(laserSection) };
		default:
			return { top: T(wgTop), xsec: X((b) => xsecStack(b)) };
	}
}

/** Every visible text of a scene (dimension labels, value labels, notes): the honesty test reads this. */
export function sceneTexts(s: Scene): string[] {
	return [...s.marks.map((m) => m.dim.label), ...s.labels.map((l) => l.text), ...s.notes, s.title];
}
