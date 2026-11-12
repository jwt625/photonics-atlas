// History timeline (DevLog-016 D974): types of static/data/history.json (scripts/build_history_view.py) and the geometry
// of the serpentine path. Pure functions, no DOM.

export interface Era {
	id: string;
	years: string;
	intro: string;
}
export interface HistComponent {
	id: string;
	class: string;
	label: string;
	n: number;
}
export interface Milestone {
	id: string;
	year: number | null;
	date: string;
	era: string;
	thread: string;
	topic: string;
	event: string;
	significance: string;
	title: string;
	venue: string;
	doi: string;
	dri: string;
	orgs_printed: string;
	institutions: string[];
	inst: string;
	/** paper type from data/history/milestone_tags.csv (DevLog-017 D991): theory, device, process, measurement, system, review */
	kind?: string;
	material: string;
	materials: string[];
	components: HistComponent[];
	n_metrics: number;
	fig: { label: string; page: string; caption: string; reason: string } | null;
	has_local_figure: boolean;
	/** has a showcase spec (static/data/showcases/<id>.json, DevLog-017) */
	showcase?: boolean;
}
export interface HistoryView {
	eras: Era[];
	milestones: Milestone[];
}

export interface Band {
	era: Era;
	n: number;
	x: number;
	y: number;
	w: number;
	h: number;
}
export interface Layout {
	mobile: boolean;
	/** node centers, same index as the input milestones */
	nodes: { x: number; y: number }[];
	bands: Band[];
	path: string;
	height: number;
	/** horizontal room per node (desktop) or label width (mobile) */
	slot: number;
	/** nodes drawn as a story thumbnail card (same index as the milestones) and the card image size */
	thumb: boolean[];
	thumbW: number;
	thumbH: number;
}

/** Story thumbnail card image: 16:10, a bit wider than a node label on desktop, capped on phones. */
export const THUMB_MAX_W = 200;
export const THUMB_MAX_W_MOBILE = 240;
export const THUMB_LABEL_H = 46; // gap + up to three 14 px label lines under the image
const NODE_TOP = 7; // a plain node: dot top above the path
const NODE_BOTTOM = 53; // a plain node: dot + gap + up to three label lines below the path

export const MOBILE_W = 700;
const M = 56; // side margin: the turns bulge into it
const SLOT_MIN = 150;
const ROW_H = 92;
const NODE_H_MOBILE = 50;
const CHAR_W = 6.4; // 12 px sans, average

function bandHeight(text: string, w: number): number {
	const lines = Math.max(1, Math.ceil((text.length * CHAR_W) / Math.max(120, w - 20)));
	return 30 + lines * 17 + 12;
}

/** Era of a milestone: its own code when known, else the era whose year span holds its year, else the last era. */
export function eraOf(m: Milestone, eras: Era[]): string {
	if (eras.some((e) => e.id === m.era)) return m.era;
	for (const e of eras) {
		const [a, b] = e.years.split('-').map(Number);
		if (m.year !== null && m.year >= a && m.year <= b) return e.id;
	}
	return eras.at(-1)?.id ?? '';
}

/** Serpentine (desktop) or single-column (width <= MOBILE_W) layout; milestones in date order. Milestones whose id is in
 *  `thumbs` are drawn as story thumbnail cards: their rows get the extra height (no overlap), the path still runs through
 *  the node centre; rows without a card keep the plain spacing. */
export function layoutTimeline(ms: Milestone[], eras: Era[], width: number, thumbs: ReadonlySet<string> = new Set()): Layout {
	const mobile = width <= MOBILE_W;
	const thumb = ms.map((m) => thumbs.has(m.id));
	const W = Math.max(width, 280);
	const byEra = new Map<string, number[]>(eras.map((e) => [e.id, []]));
	ms.forEach((m, i) => byEra.get(eraOf(m, eras))?.push(i));
	const nodes: { x: number; y: number }[] = ms.map(() => ({ x: 0, y: 0 }));
	const bands: Band[] = [];
	let y = 12;

	if (mobile) {
		const x0 = 18;
		const bx = x0 + 14;
		const bw = W - bx - 4;
		const tw = Math.round(Math.min(THUMB_MAX_W_MOBILE, W - x0 - 20 + 7));
		const th = Math.round((tw * 10) / 16);
		let first = -1;
		let last = -1;
		for (const e of eras) {
			const idx = byEra.get(e.id) ?? [];
			const h = bandHeight(e.intro, bw);
			bands.push({ era: e, n: idx.length, x: bx, y, w: bw, h });
			y += h + 22;
			for (const i of idx) {
				nodes[i] = { x: x0, y };
				if (first < 0) first = y;
				last = y;
				// a card: the image hangs from the node point (its top-left at the dot's), the label under it
				y += thumb[i] ? th + THUMB_LABEL_H : NODE_H_MOBILE;
			}
			y += 8;
		}
		const path = first < 0 ? '' : `M${x0},${first} V${last}`;
		return { mobile, nodes, bands, path, height: y + 12, slot: W - x0 - 20, thumb, thumbW: tw, thumbH: th };
	}

	const inner = W - 2 * M;
	const k = Math.max(2, Math.floor(inner / SLOT_MIN));
	const slot = inner / k;
	const c = (M - 8) / 0.75; // cubic control offset: the turn's outer extent is 0.75 c
	const tw = Math.round(Math.min(THUMB_MAX_W, slot - 8));
	const th = Math.round((tw * 10) / 16);
	// vertical extent of a row around its path line: plain nodes 7 above / 53 below, cards centred on the line
	const top = (row: number[]) => (row.some((i) => thumb[i]) ? th / 2 : NODE_TOP);
	const bottom = (row: number[]) => (row.some((i) => thumb[i]) ? th / 2 + THUMB_LABEL_H : NODE_BOTTOM);
	const GAP_BAND = 30 - NODE_TOP; // band bottom to the first row's top
	const GAP_ROW = ROW_H - NODE_BOTTOM - NODE_TOP; // a row's bottom to the next row's top
	let dir = 1;
	let path = '';
	let prevY = -1;
	for (const e of eras) {
		const idx = byEra.get(e.id) ?? [];
		const h = bandHeight(e.intro, inner);
		bands.push({ era: e, n: idx.length, x: M, y, w: inner, h });
		let edge = y + h; // bottom of the band, then of the last row
		let gap = GAP_BAND;
		y = edge + gap + NODE_TOP;
		for (let r = 0; r < idx.length; r += k) {
			const row = idx.slice(r, r + k);
			y = edge + gap + top(row);
			const from = dir > 0 ? M : W - M;
			const to = dir > 0 ? W - M : M;
			if (prevY < 0) path = `M${from},${y}`;
			else {
				const out = from + (dir > 0 ? -c : c);
				path += ` C${out},${prevY} ${out},${y} ${from},${y}`;
			}
			path += ` H${to}`;
			row.forEach((i, j) => (nodes[i] = { x: from + dir * (j + 0.5) * slot, y }));
			prevY = y;
			dir = -dir;
			edge = y + bottom(row);
			gap = GAP_ROW;
		}
		// next band: 45 px under the last row's bottom (plain rows: the former ROW_H + 6)
		y = idx.length ? edge + ROW_H + 6 - NODE_BOTTOM : edge + 36;
	}
	return { mobile, nodes, bands, path, height: y + 12, slot, thumb, thumbW: tw, thumbH: th };
}

export interface Palette {
	key: (m: Milestone) => string;
	items: { key: string; n: number; color: string }[];
	color: Map<string, string>;
}

// categorical, readable on the dark and the light background
export const COLORS = ['#3987e5', '#e5843a', '#2fb37c', '#d55181', '#a77fe0', '#d6b237', '#3fb8c9', '#c45f3a', '#7fa83a', '#e070c0', '#8b95a8'];
export const OTHER_COLOR = '#6f6d68';
export const OTHER = 'other';

export type Mode = 'thread' | 'inst' | 'material' | 'era';

/** Legend and color per category; institution and material keep the top 10 by count and fold the rest into OTHER. */
export function palette(ms: Milestone[], eras: Era[], mode: Mode): Palette {
	// era mode keys on the year span: era codes are internal and never shown
	const years = new Map(eras.map((e) => [e.id, e.years]));
	const raw = (m: Milestone): string =>
		mode === 'thread'
			? m.thread || 'unknown'
			: mode === 'inst'
				? m.inst || 'unknown'
				: mode === 'material'
					? m.material || 'unknown'
					: (years.get(eraOf(m, eras)) ?? 'unknown');
	const counts = new Map<string, number>();
	for (const m of ms) counts.set(raw(m), (counts.get(raw(m)) ?? 0) + 1);
	let order = [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
	if (mode === 'era') order = eras.map((e) => [e.years, counts.get(e.years) ?? 0] as [string, number]).filter(([, n]) => n > 0);
	const cap = mode === 'inst' || mode === 'material' ? 10 : COLORS.length;
	const kept = new Set(order.slice(0, cap).map(([k]) => k));
	const key = (m: Milestone) => (kept.has(raw(m)) ? raw(m) : OTHER);
	const items = order.filter(([k]) => kept.has(k)).map(([k, n], i) => ({ key: k, n, color: COLORS[i % COLORS.length] }));
	const rest = order.filter(([k]) => !kept.has(k)).reduce((s, [, n]) => s + n, 0);
	if (rest) items.push({ key: OTHER, n: rest, color: OTHER_COLOR });
	return { key, items, color: new Map(items.map((it) => [it.key, it.color])) };
}

/** Lower-case haystack for the text search. */
export function haystack(m: Milestone): string {
	return [m.year, m.date, m.title, m.topic, m.event, m.significance, m.thread, m.dri, m.orgs_printed, m.institutions.join(' '), m.inst, m.venue, m.doi, m.material, m.kind ?? '']
		.join(' ')
		.toLowerCase();
}

/** Which milestones are shown: legend group (`only`, empty = all), every search term, and, with storiesOnly, a story. */
export function shownMask(
	ms: Milestone[],
	o: { only: ReadonlySet<string>; key: (m: Milestone) => string; terms: readonly string[]; hay: readonly string[]; storiesOnly: boolean; stories: ReadonlySet<string> }
): boolean[] {
	return ms.map((m, i) => (o.only.size === 0 || o.only.has(o.key(m))) && o.terms.every((t) => o.hay[i].includes(t)) && (!o.storiesOnly || o.stories.has(m.id)));
}
