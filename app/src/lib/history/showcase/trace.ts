// Traced drawing renderer: TypeScript port of ipatent `viewer/trace-render.js` (same author; ipatent is GPL-3.0).
// Schema: ipatent `pipeline/TRACE_SCHEMA.md`. All coordinates are pixels of the upright crop, origin top-left.
// Differences from the original: typed; pattern ids scoped by `uid`; element groups carry `data-part` (the spec part
// id the reference numeral maps to, from Drawing.numerals) so the story can link drawing, model and parts list.

export interface TraceShape {
	t: 'r' | 'c' | 'e' | 'p' | 'l' | 'path' | 't';
	d?: unknown;
	w?: number;
	dash?: boolean | number[];
	fill?: 'none' | 'light' | 'solid' | 'hatch' | 'stipple' | 'dashes' | 'paper';
	ink?: 'paper';
	arrow?: 'end' | 'start' | 'both';
	pitch?: number;
	angle?: number;
	hw?: number;
	// text
	x?: number;
	y?: number;
	s?: string;
	size?: number;
	anchor?: 'start' | 'middle' | 'end';
	rot?: number;
	italic?: boolean;
	bold?: boolean;
	len?: number;
	sub?: SubStyle;
}
export interface SubStyle {
	scale?: number;
	drop?: number;
	rise?: number;
}
export interface TraceElement {
	id: string;
	ref?: string;
	kind?: 'block' | 'wire' | 'label' | 'leader' | 'text' | 'outline' | 'mark';
	name?: string;
	step?: number;
	shapes?: TraceShape[];
}
export interface Trace {
	fig?: string;
	w: number;
	h: number;
	stroke?: number;
	sub?: SubStyle;
	elements: TraceElement[];
}

const NS = 'http://www.w3.org/2000/svg';
type Attrs = Record<string, string | number | null | undefined>;
function mk<K extends keyof SVGElementTagNameMap>(tag: K, a: Attrs = {}): SVGElementTagNameMap[K] {
	const n = document.createElementNS(NS, tag);
	for (const k in a) if (a[k] != null) n.setAttribute(k, String(a[k]));
	return n;
}
const pts = (d: number[][]) => d.map((p) => p[0] + ',' + p[1]).join(' ');

interface Ctx {
	uid: string;
	defs: SVGDefsElement;
	made: Set<string>;
	sub?: SubStyle;
}

function defs(svg: SVGSVGElement, uid: string): SVGDefsElement {
	const d = mk('defs');
	// arrowheads sized in stroke widths so they scale with the line they sit on
	for (const [k, o] of [
		['end', 'auto'],
		['start', 'auto-start-reverse']
	]) {
		const m = mk('marker', { id: `${uid}-ar-${k}`, viewBox: '0 0 10 10', refX: 9, refY: 5, markerWidth: 5, markerHeight: 5, orient: o, markerUnits: 'strokeWidth' });
		m.appendChild(mk('path', { d: 'M0,0 L10,5 L0,10 z', class: 'tr-arrow' }));
		d.appendChild(m);
	}
	const p = mk('pattern', { id: `${uid}-hatch`, width: 14, height: 14, patternUnits: 'userSpaceOnUse', patternTransform: 'rotate(45)' });
	p.appendChild(mk('line', { x1: 0, y1: 0, x2: 0, y2: 14, class: 'tr-hatchline' }));
	d.appendChild(p);
	const st = mk('pattern', { id: `${uid}-stipple`, width: 18, height: 18, patternUnits: 'userSpaceOnUse' });
	for (const [x, y] of [
		[4, 4],
		[13, 9],
		[6, 14]
	])
		st.appendChild(mk('circle', { cx: x, cy: y, r: 1.6, class: 'tr-arrow' }));
	d.appendChild(st);
	const ds = mk('pattern', { id: `${uid}-dashes`, width: 28, height: 20, patternUnits: 'userSpaceOnUse' });
	ds.appendChild(mk('line', { x1: 3, y1: 5, x2: 13, y2: 5, class: 'tr-hatchline' }));
	ds.appendChild(mk('line', { x1: 17, y1: 15, x2: 27, y2: 15, class: 'tr-hatchline' }));
	d.appendChild(ds);
	svg.appendChild(d);
	return d;
}

// hatch with custom pitch / angle (px, degrees), defined once per combination
function hatchId(ctx: Ctx, pitch: number, angle: number, hw?: number): string {
	const id = `${ctx.uid}-hatch-${pitch}-${angle}-${hw || 0}`.replace(/\./g, '_');
	if (!ctx.made.has(id)) {
		ctx.made.add(id);
		const p = mk('pattern', { id, width: pitch, height: pitch, patternUnits: 'userSpaceOnUse', patternTransform: `rotate(${angle})` });
		p.appendChild(mk('line', { x1: 0, y1: 0, x2: 0, y2: pitch, class: 'tr-hatchline', style: hw ? `stroke-width:${hw}` : null }));
		ctx.defs.appendChild(p);
	}
	return id;
}

function shape(s: TraceShape, ctx: Ctx, dflt: number): SVGElement | null {
	const uid = ctx.uid;
	const w = s.w != null ? s.w : dflt;
	const pat = s.fill === 'hatch' || s.fill === 'stipple' || s.fill === 'dashes';
	const fill = s.fill === 'solid' ? 'tr-fill-solid' : s.fill === 'light' ? 'tr-fill-light' : s.fill === 'paper' ? 'tr-fill-paper' : pat ? 'tr-fill-pat' : 'tr-fill-none';
	const a: Attrs = { class: `tr-s ${fill}${s.dash ? ' tr-dash' : ''}${s.ink === 'paper' ? ' tr-ink-paper' : ''}`, 'stroke-width': w };
	const patId = s.fill === 'hatch' && (s.pitch || s.angle != null || s.hw) ? hatchId(ctx, s.pitch || 14, s.angle != null ? s.angle : 45, s.hw) : `${uid}-${s.fill}`;
	// inline style: stylesheet rules on .tr-s would override presentation attributes
	a.style = (pat ? `fill:url(#${patId});` : '') + (s.w === 0 ? 'stroke:none;' : '') || null;
	if (s.dash) a['stroke-dasharray'] = Array.isArray(s.dash) ? s.dash.join(' ') : `${w * 4} ${w * 3}`;
	const d = s.d as number[] & number[][] & string;
	let n: SVGElement;
	switch (s.t) {
		case 'r':
			n = mk('rect', { ...a, x: d[0], y: d[1], width: d[2] - d[0], height: d[3] - d[1] });
			break;
		case 'c':
			n = mk('circle', { ...a, cx: d[0], cy: d[1], r: d[2] });
			break;
		case 'e':
			n = mk('ellipse', { ...a, cx: d[0], cy: d[1], rx: d[2], ry: d[3] });
			break;
		case 'p':
			n = mk('polygon', { ...a, points: pts(d) });
			break;
		case 'l':
			n = mk('polyline', { ...a, points: pts(d), class: String(a.class).replace(/tr-fill-\w+/, 'tr-fill-none') });
			break;
		case 'path':
			n = mk('path', { ...a, d });
			break;
		case 't': {
			const sz = s.size || 28;
			const x = s.x ?? 0;
			const y = s.y ?? 0;
			n = mk('text', {
				class: `tr-t${s.italic ? ' tr-it' : ''}${s.bold ? ' tr-b' : ''}${s.ink === 'paper' ? ' tr-ink-paper' : ''}`,
				x,
				y,
				'font-size': sz,
				'text-anchor': s.anchor || 'start',
				transform: s.rot ? `rotate(${s.rot} ${x} ${y})` : null,
				textLength: s.len || null,
				lengthAdjust: s.len ? 'spacingAndGlyphs' : null
			});
			// subscripts: "V0_{12}" renders 12 as a subscript, "t^{2}" as a superscript
			for (const part of String(s.s ?? '').split(/(_\{[^}]*\}|\^\{[^}]*\})/)) {
				if (!part) continue;
				const sub = part.startsWith('_{');
				const sup = part.startsWith('^{');
				const ss = s.sub || ctx.sub || {};
				const k = ss.scale != null ? ss.scale : 0.68;
				const shift = sub ? (ss.drop != null ? -ss.drop : 'sub') : ss.rise != null ? ss.rise : 'super';
				const ts = mk('tspan', sub || sup ? { 'font-size': sz * k, 'baseline-shift': shift } : {});
				ts.textContent = sub || sup ? part.slice(2, -1) : part;
				n.appendChild(ts);
			}
			break;
		}
		default:
			return null;
	}
	if (s.t === 'l' || s.t === 'path') {
		if (s.arrow === 'end' || s.arrow === 'both') n.setAttribute('marker-end', `url(#${uid}-ar-end)`);
		if (s.arrow === 'start' || s.arrow === 'both') n.setAttribute('marker-start', `url(#${uid}-ar-start)`);
	}
	return n;
}

export interface Rendered {
	groups: Record<string, SVGGElement>;
	byRef: Record<string, SVGGElement[]>;
	uid: string;
}

/** Render `trace` into `svg`; `partOf` maps a reference numeral to a spec part id (set as data-part on its groups). */
export function renderTrace(svg: SVGSVGElement, trace: Trace, uid: string, partOf: (ref: string) => string | undefined = () => undefined): Rendered {
	svg.setAttribute('viewBox', `0 0 ${trace.w} ${trace.h}`);
	const ctx: Ctx = { uid, defs: defs(svg, uid), made: new Set(), sub: trace.sub };
	const body = mk('g', { class: 'tr-body' });
	svg.appendChild(body);
	const groups: Record<string, SVGGElement> = {};
	const byRef: Record<string, SVGGElement[]> = {};
	const dflt = trace.stroke || 3;
	for (const el of trace.elements || []) {
		const g = mk('g', { class: `tr-el tr-k-${el.kind || 'line'}` });
		g.dataset.id = el.id;
		if (el.ref) {
			g.dataset.ref = el.ref;
			const part = partOf(el.ref);
			if (part) g.dataset.part = part;
		}
		if (el.step != null) g.dataset.step = String(el.step);
		for (const s of el.shapes || []) {
			const n = shape(s, ctx, dflt);
			if (n) g.appendChild(n);
		}
		body.appendChild(g);
		groups[el.id] = g;
		if (el.ref) (byRef[el.ref] ??= []).push(g);
	}
	return { groups, byRef, uid };
}

/** End and control points of an absolute-command path (M L H V C S Q T A Z); arc radii / flags are skipped. */
export function pathPoints(d: string): [number, number][] {
	const out: [number, number][] = [];
	const toks = d.match(/[A-Za-z]|-?\d*\.?\d+(?:e-?\d+)?/g) || [];
	let cmd = 'M';
	let i = 0;
	let x = 0;
	let y = 0;
	const num = () => +toks[i++];
	while (i < toks.length) {
		if (/[A-Za-z]/.test(toks[i])) cmd = toks[i++].toUpperCase();
		if (cmd === 'Z') continue;
		if (i >= toks.length || /[A-Za-z]/.test(toks[i])) continue;
		if (cmd === 'H') x = num();
		else if (cmd === 'V') y = num();
		else if (cmd === 'A') {
			i += 5;
			x = num();
			y = num();
		} else {
			const n = ({ M: 1, L: 1, T: 1, Q: 2, S: 2, C: 3 } as Record<string, number>)[cmd] || 1;
			for (let k = 0; k < n; k++) {
				x = num();
				y = num();
				if (k < n - 1) out.push([x, y]);
			}
		}
		out.push([x, y]);
	}
	return out;
}

/** Bounding box [x0, y0, x1, y1] of an element in trace pixels, or null. */
export function elementBox(el: Pick<TraceElement, 'shapes'>): [number, number, number, number] | null {
	let x0 = Infinity;
	let y0 = Infinity;
	let x1 = -Infinity;
	let y1 = -Infinity;
	const add = (x: number, y: number) => {
		x0 = Math.min(x0, x);
		y0 = Math.min(y0, y);
		x1 = Math.max(x1, x);
		y1 = Math.max(y1, y);
	};
	for (const s of el.shapes || []) {
		const d = s.d as number[] & number[][] & string;
		if (s.t === 'r') {
			add(d[0], d[1]);
			add(d[2], d[3]);
		} else if (s.t === 'c') {
			add(d[0] - d[2], d[1] - d[2]);
			add(d[0] + d[2], d[1] + d[2]);
		} else if (s.t === 'e') {
			add(d[0] - d[2], d[1] - d[3]);
			add(d[0] + d[2], d[1] + d[3]);
		} else if (s.t === 'p' || s.t === 'l') (s.d as number[][]).forEach((p) => add(p[0], p[1]));
		else if (s.t === 't') {
			const sz = s.size || 28;
			const x = s.x ?? 0;
			const y = s.y ?? 0;
			const n = String(s.s ?? '').replace(/[_^]\{|\}/g, '').length * sz * 0.6;
			const ax = s.anchor === 'middle' ? n / 2 : s.anchor === 'end' ? n : 0;
			if (s.rot === -90 || s.rot === 270) {
				add(x - sz, y - n + ax);
				add(x, y + ax);
			} else if (s.rot === 90) {
				add(x, y - ax);
				add(x + sz, y + n - ax);
			} else {
				add(x - ax, y - sz);
				add(x - ax + n, y + sz * 0.25);
			}
		} else if (s.t === 'path') pathPoints(d).forEach((p) => add(p[0], p[1]));
	}
	return Number.isFinite(x0) ? [x0, y0, x1, y1] : null;
}

/**
 * Hit layer (simplified from ipatent FigureView.buildHit): one invisible target per shape of every element that maps
 * to a part; lines get a wide stroke target, labels a padded box. Largest areas underneath, strokes above, labels on
 * top, so small parts stay reachable.
 */
export function hitLayer(trace: Trace, partOf: (ref: string) => string | undefined): SVGGElement {
	const g = mk('g', { class: 'tr-hit' });
	const items: { n: SVGElement; a: number }[] = [];
	for (const e of trace.elements) {
		const part = e.ref ? partOf(e.ref) : undefined;
		if (!part) continue;
		for (const s of e.shapes || []) {
			const b = elementBox({ shapes: [s] });
			if (!b) continue;
			let n: SVGElement;
			let a: number;
			const d = s.d as number[] & number[][] & string;
			if (s.t === 't' || e.kind === 'label') {
				const pad = 8;
				n = mk('rect', { x: b[0] - pad, y: b[1] - pad, width: b[2] - b[0] + 2 * pad, height: b[3] - b[1] + 2 * pad, 'pointer-events': 'all' });
				a = -1;
			} else if (s.t === 'l' || (s.t === 'path' && s.fill !== 'solid') || e.kind === 'outline') {
				n = s.t === 'l' ? mk('polyline', { points: pts(d) }) : s.t === 'path' ? mk('path', { d }) : mk('rect', { x: b[0], y: b[1], width: b[2] - b[0], height: b[3] - b[1] });
				n.setAttribute('stroke-width', '22');
				n.setAttribute('pointer-events', 'stroke');
				n.setAttribute('fill', 'none');
				a = 0;
			} else {
				n = mk('rect', { x: b[0], y: b[1], width: b[2] - b[0], height: b[3] - b[1], 'pointer-events': 'all' });
				a = (b[2] - b[0]) * (b[3] - b[1]);
			}
			n.setAttribute('stroke', 'transparent');
			if (!n.getAttribute('fill')) n.setAttribute('fill', 'transparent');
			n.dataset.part = part;
			items.push({ n, a });
		}
	}
	items.sort((p, q) => Number(p.a === -1) - Number(q.a === -1) || Number(p.a === 0) - Number(q.a === 0) || q.a - p.a);
	for (const it of items) g.appendChild(it.n);
	return g;
}
