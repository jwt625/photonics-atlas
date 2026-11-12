// Pure geometry of the plot assembler (PlotAssembler.svelte): data ranges, linear / log scales, ticks and how much of
// the plot is drawn at a local progress r in [0, 1] (axes first, then the points of each series in spec order).
import type { Axis, Bar, ErrSpec, Plot, Series, ShowcaseSpec } from './types';
import { clamp01, plotRange, seg, unitSuffix } from './progress';

export interface Scale {
	log: boolean;
	d0: number;
	d1: number;
	r0: number;
	r1: number;
	map: (v: number) => number;
}

export function makeScale(d0: number, d1: number, r0: number, r1: number, log: boolean): Scale {
	const f = log ? (v: number) => Math.log10(v) : (v: number) => v;
	const a = f(d0);
	const b = f(d1);
	const span = b - a || 1;
	return { log, d0, d1, r0, r1, map: (v: number) => r0 + ((f(v) - a) / span) * (r1 - r0) };
}

/** Data extent of one axis over all series (points and bars); log axes ignore non-positive values; pads a degenerate
 *  range. */
export function extent(series: readonly Series[], axis: 0 | 1, log: boolean, fixed?: [number, number]): [number, number] {
	if (fixed && fixed.length === 2 && fixed[1] > fixed[0] && (!log || fixed[0] > 0)) return fixed;
	let lo = Infinity;
	let hi = -Infinity;
	for (const s of series)
		for (const pt of [...(s.points ?? []), ...barPoints(s), ...errPoints(s)]) {
			const v = pt[axis];
			if (!Number.isFinite(v) || (log && v <= 0)) continue;
			lo = Math.min(lo, v);
			hi = Math.max(hi, v);
		}
	if (!Number.isFinite(lo)) return log ? [1, 10] : [0, 1];
	if (log) {
		const a = 10 ** Math.floor(Math.log10(lo));
		const b = 10 ** Math.ceil(Math.log10(hi));
		return b > a ? [a, b] : [a, a * 10];
	}
	if (hi === lo) return [lo - 1, hi + 1];
	const pad = (hi - lo) * 0.04;
	return [lo - pad, hi + pad];
}

/** Round tick values covering [a, b], about n of them. */
export function linTicks(a: number, b: number, n = 5): number[] {
	const span = b - a;
	if (!(span > 0)) return [a];
	const raw = span / Math.max(1, n);
	const mag = 10 ** Math.floor(Math.log10(raw));
	const step = [1, 2, 2.5, 5, 10].map((k) => k * mag).find((s) => s >= raw) ?? 10 * mag;
	const out: number[] = [];
	for (let v = Math.ceil(a / step) * step; v <= b + step * 1e-9; v += step) out.push(Number(v.toPrecision(12)));
	return out;
}

/** Decades inside [a, b] (a > 0). */
export function logTicks(a: number, b: number): number[] {
	const out: number[] = [];
	for (let e = Math.ceil(Math.log10(a) - 1e-9); e <= Math.floor(Math.log10(b) + 1e-9); e++) out.push(10 ** e);
	return out;
}

const sup = (n: number): string => String(n).replace(/[0-9-]/g, (c) => SUP[c]); // SUP is declared below (hoisted const, used at call time)

/** Number for ticks and tooltips: plain up to 6 significant digits; very large / small values in scientific notation
 *  written as 10\u2075 or 2.5\u00d710\u2075 (never "1e5"), mantissa kept to 3 significant digits. */
export function fmt(v: number): string {
	if (v === 0) return '0';
	const a = Math.abs(v);
	if (a >= 1e5 || a < 1e-3) {
		let e = Math.floor(Math.log10(a));
		let m = Number((v / 10 ** e).toPrecision(3));
		if (Math.abs(m) >= 10) {
			m = Number((m / 10).toPrecision(3));
			e += 1;
		}
		return Math.abs(m) === 1 ? `${m < 0 ? '\u2212' : ''}10${sup(e)}` : `${m}\u00d710${sup(e)}`;
	}
	return String(Number(v.toPrecision(6)));
}

export const AXES_END = 0.25; // share of the plot progress used to draw the axes

/** Axis draw fraction at plot progress r. */
export const axesK = (r: number): number => seg(r, 0, AXES_END);

/**
 * Window [a, b] of item i of n inside [a0, b0]: with several items each window is half of the range and the starts are
 * spread evenly, so items overlap and the last one ends at b0.
 */
export function stagger(a0: number, b0: number, i: number, n: number): [number, number] {
	if (n <= 1) return [a0, b0];
	const len = (b0 - a0) * 0.5;
	const a = a0 + (i * (b0 - a0 - len)) / (n - 1);
	return [a, a + len];
}

/** Progress of item i of n at r inside [a0, b0] (see stagger). */
export const staggerK = (r: number, a0: number, b0: number, i: number, n: number): number => {
	const [a, b] = stagger(a0, b0, i, n);
	return seg(r, a, b);
};

/**
 * Points of a series revealed at plot progress r. Series reveal concurrently with staggered starts inside
 * [AXES_END, 1] (see stagger); returns the count of whole points and the fraction of the segment to the next one.
 */
export function revealed(r: number, nSeries: number, si: number, nPts: number): { n: number; frac: number } {
	const t = staggerK(r, AXES_END, 1, si, nSeries) * nPts;
	const n = Math.min(nPts, Math.floor(t + 1e-9));
	return { n, frac: n >= nPts ? 0 : t - n };
}

/** Bars of a series in object form; [x0, x1, h] tuples accepted; invalid entries dropped. */
export function toBars(s: Pick<Series, 'bars'>): Bar[] {
	const out: Bar[] = [];
	for (const b of s.bars ?? []) {
		const o: Bar | null = Array.isArray(b) ? { from: b[0], to: b[1], height: b[2] } : b && typeof b === 'object' ? b : null;
		if (o && [o.from, o.to, o.height].every(Number.isFinite)) out.push({ ...o, from: Math.min(o.from, o.to), to: Math.max(o.from, o.to) });
	}
	return out;
}

/** Corner points of a series' bars (for extents). */
function barPoints(s: Pick<Series, 'bars'>): [number, number][] {
	return toBars(s).flatMap((b) => [
		[b.from, 0],
		[b.to, b.height]
	] as [number, number][]);
}

/** Height fraction of bar i (of nb) of series si (of nSeries) at plot progress r. */
export function barK(r: number, nSeries: number, si: number, i: number, nb: number): number {
	const [a, b] = stagger(AXES_END, 1, si, nSeries);
	return staggerK(r, a, b, i, nb);
}

export const scaleNone = (a: Axis | undefined): boolean => a?.scale === 'none';
export const startsLog = (a: Axis | undefined): boolean => !!a && (a.log === true || a.scale === 'log');

/**
 * Ticks of an axis over [lo, hi]: `major` get labels (and grid lines), `minor` only short marks. scale none: no ticks;
 * `ticks` array: those values; `ticks` number: a mark at every step, labels at round values.
 */
export function axisTicks(a: Axis | undefined, lo: number, hi: number, log: boolean, nAuto: number): { major: number[]; minor: number[] } {
	if (scaleNone(a)) return { major: [], minor: [] };
	const inR = (v: number) => v >= lo - 1e-9 * Math.abs(hi - lo) && v <= hi + 1e-9 * Math.abs(hi - lo);
	if (Array.isArray(a?.ticks)) return { major: a.ticks.filter((v) => Number.isFinite(v) && inR(v)), minor: [] };
	const major = log ? logTicks(lo, hi) : linTicks(lo, hi, nAuto);
	const step = typeof a?.ticks === 'number' && a.ticks > 0 && !log ? a.ticks : 0;
	const minor: number[] = [];
	if (step && (hi - lo) / step <= 400) for (let v = Math.ceil(lo / step - 1e-9) * step; v <= hi + 1e-9; v += step) minor.push(Number(v.toPrecision(12)));
	return { major, minor };
}

export interface Run {
	t: string;
	k: '' | 'sup' | 'sub';
}

/** Text with `^x`, `^{..}`, `_x`, `_{..}` marks as runs; a hyphen in a superscript becomes a minus sign. */
export function rich(s: string): Run[] {
	const out: Run[] = [];
	for (const part of String(s ?? '').split(/(\^\{[^}]*\}|_\{[^}]*\}|\^-?[0-9A-Za-z+]+|_-?[0-9A-Za-z]+)/)) {
		if (!part) continue;
		const k = part[0] === '^' ? 'sup' : part[0] === '_' ? 'sub' : '';
		const t = k ? part.slice(1).replace(/^\{|\}$/g, '') : part;
		out.push({ t: k ? t.replace(/^-/, '\u2212') : t, k });
	}
	return out;
}

/** Spectroscopic term symbol as runs: leading digits superscript (multiplicity), trailing digits subscript
 *  ("4A2" -> ^4 A _2, "2E" -> ^2 E); labels with ^ / _ marks use rich(). */
export function term(label: string): Run[] {
	if (/[\^_]/.test(label)) return rich(label);
	const m = /^(\d+)?(\D+?)(\d+)?$/u.exec(label);
	if (!m) return [{ t: label, k: '' }];
	const out: Run[] = [];
	if (m[1]) out.push({ t: m[1], k: 'sup' });
	out.push({ t: m[2], k: '' });
	if (m[3]) out.push({ t: m[3], k: 'sub' });
	return out;
}

const SUP: Record<string, string> = { '0': '\u2070', '1': '\u00b9', '2': '\u00b2', '3': '\u00b3', '4': '\u2074', '5': '\u2075', '6': '\u2076', '7': '\u2077', '8': '\u2078', '9': '\u2079', '\u2212': '\u207b', '-': '\u207b', '+': '\u207a', '=': '\u207c', '(': '\u207d', ')': '\u207e', n: '\u207f', i: '\u2071' };
const SUB: Record<string, string> = { '0': '\u2080', '1': '\u2081', '2': '\u2082', '3': '\u2083', '4': '\u2084', '5': '\u2085', '6': '\u2086', '7': '\u2087', '8': '\u2088', '9': '\u2089', '+': '\u208a', '-': '\u208b', '\u2212': '\u208b', '=': '\u208c', '(': '\u208d', ')': '\u208e', a: '\u2090', e: '\u2091', o: '\u2092', x: '\u2093', h: '\u2095', k: '\u2096', l: '\u2097', m: '\u2098', n: '\u2099', p: '\u209a', s: '\u209b', t: '\u209c', i: '\u1d62', r: '\u1d63', u: '\u1d64', v: '\u1d65', j: '\u2c7c' };

/** Plain-text form of runs for plain-text tooltips: Unicode super / subscripts where every character of a run has
 *  one, else the run's text as is (never a raw marker). */
export function plain(runs: Run[]): string {
	return runs
		.map((r) => {
			if (!r.k) return r.t;
			const map = r.k === 'sup' ? SUP : SUB;
			const cs = [...r.t];
			return cs.every((c) => map[c]) ? cs.map((c) => map[c]).join('') : r.t;
		})
		.join('');
}

/** Prose markup: `_{...}` subscript and `^{...}` superscript (braces required); everything else literal, including
 *  plain underscores and carets ("r_{33}", "Cr^{3+}", "O_{2}", "file_name"). */
export function markup(s: string): Run[] {
	const out: Run[] = [];
	for (const part of String(s ?? '').split(/(_\{[^{}]*\}|\^\{[^{}]*\})/)) {
		if (!part) continue;
		const k = /^_\{.*\}$/s.test(part) ? 'sub' : /^\^\{.*\}$/s.test(part) ? 'sup' : '';
		out.push({ t: k ? part.slice(2, -1) : part, k });
	}
	return out;
}

/** Plain-text form of marked-up prose (tooltips that cannot hold sub / sup). */
export const plainMarkup = (s: string | number | null | undefined): string => plain(markup(s == null ? '' : String(s)));

/** Rotated axis title fitting a length (px): shrink from fs down to minFs, then cut with an ellipsis. Width estimate
 *  0.56 em per character. */
export function fitTitle(text: string, avail: number, fs = 11, minFs = 9): { text: string; fs: number; cut: boolean } {
	const need = (n: number, f: number) => n * f * 0.56;
	const n = [...text].length;
	if (need(n, fs) <= avail) return { text, fs, cut: false };
	const f = Math.max(minFs, Math.min(fs, avail / (n * 0.56)));
	if (need(n, f) <= avail) return { text, fs: f, cut: false };
	const keep = Math.max(1, Math.floor(avail / (f * 0.56)) - 1);
	return { text: [...text].slice(0, keep).join('').trimEnd() + '\u2026', fs: f, cut: true };
}

export function styleOf(s: Series): 'line' | 'points' | 'both' | 'dashed' | 'stems' {
	return s.style ?? ((s.points?.length ?? 0) > 40 ? 'line' : 'both');
}

/** Points in spec order (the reveal and line order); non-finite and (on log axes) non-positive values dropped. */
export function cleanPoints(s: Series, logX: boolean, logY: boolean): [number, number][] {
	return (s.points ?? [])
		.filter(([x, y]) => Number.isFinite(x) && Number.isFinite(y) && (!logX || x > 0) && (!logY || y > 0));
}

export interface LogPair {
	x: boolean;
	y: boolean;
}
export type LogState = Readonly<Record<string, LogPair>>;

/** Log / linear choice of a plot: the user's choice for this plot id, else the spec default. */
export function logOf(state: LogState, plot: Pick<Plot, 'id' | 'x' | 'y'>): LogPair {
	return state[plot.id] ?? { x: startsLog(plot.x), y: startsLog(plot.y) };
}

/** New state with one axis of one plot flipped; other plots keep their own choices. */
export function toggleLog(state: LogState, plot: Pick<Plot, 'id' | 'x' | 'y'>, axis: 'x' | 'y'): LogState {
	const cur = logOf(state, plot);
	return { ...state, [plot.id]: { ...cur, [axis]: !cur[axis] } };
}

/** A main plot and its alternates (plots with alt_of = main id), main first; [] when the main id is unknown. */
export function withAlternates(plots: readonly Plot[], mainId: string): Plot[] {
	const main = plots.find((p) => p.id === mainId);
	return main ? [main, ...plots.filter((p) => p.alt_of === mainId && p.id !== mainId)] : [];
}

export const plotLabel = (p: Pick<Plot, 'id' | 'title' | 'label'>): string => p.label || p.title || p.id;

export function axisTitle(a: Plot['x']): string {
	if (!a) return '';
	return a.unit ? `${a.label} (${plain(rich(a.unit))})` : a.label;
}

/**
 * Legend origin in the emptiest corner of the data area: counts data points (and segment midpoints) under a legend box
 * of size lw x lh in each corner, picks the least covered (ties: top-left, top-right, bottom-left, bottom-right).
 */
export function legendCorner(pts: readonly [number, number][], area: { x0: number; x1: number; y0: number; y1: number }, lw: number, lh: number, pad = 6): { x: number; y: number; hits: number } {
	const cand = [
		{ x: area.x0 + pad, y: area.y0 + pad },
		{ x: area.x1 - pad - lw, y: area.y0 + pad },
		{ x: area.x0 + pad, y: area.y1 - pad - lh },
		{ x: area.x1 - pad - lw, y: area.y1 - pad - lh }
	];
	let best = { ...cand[0], hits: Infinity };
	for (const c of cand) {
		let hits = 0;
		for (const [px, py] of pts) if (px >= c.x - 4 && px <= c.x + lw + 4 && py >= c.y - 4 && py <= c.y + lh + 4) hits++;
		if (hits < best.hits) best = { ...c, hits };
	}
	return best;
}

// ---------------------------------------------------------------------------------------------- error bars, aspect

/** Offsets [lo, hi] of point i from an err spec, or null (no bar). */
export function errAt(err: ErrSpec | undefined | null, i: number): [number, number] | null {
	if (err == null) return null;
	const e = typeof err === 'number' ? err : err[i];
	if (e == null) return null;
	if (typeof e === 'number') return Number.isFinite(e) && e > 0 ? [e, e] : null;
	if (Array.isArray(e) && e.length === 2 && e.every((v) => Number.isFinite(v) && v >= 0) && (e[0] > 0 || e[1] > 0)) return [e[0], e[1]];
	return null;
}

/** Ends [lo, hi] of a whisker around v in data units; on a log axis a low end at or below zero clamps to the floor. */
export function whiskerEnds(v: number, e: [number, number], log: boolean, floor: number): [number, number] {
	const lo = v - e[0];
	return [log && lo <= 0 ? floor : lo, v + e[1]];
}

/** Whisker end points of a series (for data extents): (x, y +- err) and (x +- err_x, y). Log axes skip non-positive ends. */
function errPoints(s: Pick<Series, 'points' | 'err' | 'err_x'>): [number, number][] {
	const out: [number, number][] = [];
	(s.points ?? []).forEach(([x, y], i) => {
		const ey = errAt(s.err, i);
		const ex = errAt(s.err_x, i);
		if (ey) out.push([x, y - ey[0]], [x, y + ey[1]]);
		if (ex) out.push([x - ex[0], y], [x + ex[1], y]);
	});
	return out;
}

/** Original indices of the points cleanPoints keeps (error bars are indexed like the spec's points). */
export function cleanIndices(s: Series, logX: boolean, logY: boolean): number[] {
	const out: number[] = [];
	(s.points ?? []).forEach(([x, y], i) => {
		if (Number.isFinite(x) && Number.isFinite(y) && (!logX || x > 0) && (!logY || y > 0)) out.push(i);
	});
	return out;
}

export interface Whisker {
	/** vertical whisker x, y0 (low end, px), y1 (high end, px) */
	v: [number, number, number] | null;
	/** horizontal whisker y, x0, x1 */
	h: [number, number, number] | null;
}

/** Pixel whiskers of one point; scales map data to px (log handled by the scales), floors are the axis minima. */
export function whiskerPx(x: number, y: number, ey: [number, number] | null, ex: [number, number] | null, X: Scale, Y: Scale): Whisker {
	const v = ey ? (() => { const [a, b] = whiskerEnds(y, ey, Y.log, Y.d0); return [X.map(x), Y.map(a), Y.map(b)] as [number, number, number]; })() : null;
	const h = ex ? (() => { const [a, b] = whiskerEnds(x, ex, X.log, X.d0); return [Y.map(y), X.map(a), X.map(b)] as [number, number, number]; })() : null;
	return { v, h };
}

/** Error text for a tooltip: "+hi / -lo" with the unit (symmetric: "+/- e"). */
export function errText(e: [number, number], unit = ''): string {
	const u = unitSuffix(unit);
	return e[0] === e[1] ? `\u00b1 ${fmt(e[0])}${u}` : `+${fmt(e[1])} / \u2212${fmt(e[0])}${u}`;
}

/** Equal-aspect data area: shrink the pixel box so one x data unit spans as many px as one y unit; centred. */
export function equalAspect(dx: number, dy: number, box: { x0: number; x1: number; y0: number; y1: number }): { x0: number; x1: number; y0: number; y1: number } {
	const w = box.x1 - box.x0;
	const h = box.y1 - box.y0;
	if (!(dx > 0 && dy > 0 && w > 0 && h > 0)) return box;
	const k = Math.min(w / dx, h / dy);
	const nw = dx * k;
	const nh = dy * k;
	const cx = (box.x0 + box.x1) / 2;
	const cy = (box.y0 + box.y1) / 2;
	return { x0: cx - nw / 2, x1: cx + nw / 2, y0: cy - nh / 2, y1: cy + nh / 2 };
}

/** Stem base of a series in data units: stem_base, else the y-range minimum; kept inside [y0, y1]; on log y never below
 *  the axis floor y0 (and a non-positive base becomes the floor). */
export function stemBase(s: Pick<Series, 'stem_base'>, yr: [number, number], logY: boolean): number {
	const b = typeof s.stem_base === 'number' && Number.isFinite(s.stem_base) ? s.stem_base : yr[0];
	if (logY && !(b > 0)) return yr[0];
	return Math.min(yr[1], Math.max(yr[0], b));
}

// ---------------------------------------------------------------------------------------------- legend rows, layout
export interface LegendRow {
	key: string;
	/** series index whose name and colour the row shows */
	first: number;
	members: number[];
	line: boolean;
	dashed: boolean;
	dots: boolean;
	stems: boolean;
	bars: boolean;
}

/** Legend rows: series with legend !== false, merged by legend_group (first member names the row), in series order. */
export function legendRows(series: readonly { s: Pick<Series, 'name' | 'legend' | 'legend_group'>; style: string; bars: readonly unknown[] }[]): LegendRow[] {
	const rows: LegendRow[] = [];
	const byKey = new Map<string, LegendRow>();
	series.forEach((it, i) => {
		if (it.s.legend === false) return;
		const key = it.s.legend_group ? `g:${it.s.legend_group}` : `s:${i}`;
		let row = byKey.get(key);
		if (!row) {
			row = { key, first: i, members: [], line: false, dashed: false, dots: false, stems: false, bars: false };
			byKey.set(key, row);
			rows.push(row);
		}
		row.members.push(i);
		if (it.bars.length) row.bars = true;
		else if (it.style === 'stems') row.stems = true;
		else if (it.style === 'dashed') row.dashed = true;
		else {
			if (it.style === 'line' || it.style === 'both') row.line = true;
			if (it.style === 'points' || it.style === 'both') row.dots = true;
		}
	});
	return rows;
}

/** Colour slot of each series: its own index, or the first member's index when it belongs to a legend group. */
export function colorSlots(series: readonly { s: Pick<Series, 'legend_group'> }[]): number[] {
	const first = new Map<string, number>();
	return series.map((it, i) => {
		const g = it.s.legend_group;
		if (!g) return i;
		if (!first.has(g)) first.set(g, i);
		return first.get(g)!;
	});
}

/**
 * Legend block above the data area: rows of height rowH in as many columns of width colW as fit availW; when the
 * block is taller than maxH (phones: keep the data area at about 60 % of the panel) it shows the rows that fit and
 * reports the rest as hidden ("+N more"), unless open.
 */
export function legendBlock(n: number, colW: number, availW: number, maxH: number, open = false, rowH = 15): { cols: number; perCol: number; shown: number; hidden: number; h: number } {
	if (n <= 0) return { cols: 1, perCol: 0, shown: 0, hidden: 0, h: 0 };
	const cols = Math.max(1, Math.min(n, Math.floor(availW / Math.max(1, colW))));
	let perCol = Math.ceil(n / cols);
	const fitRows = Math.max(1, Math.floor(maxH / rowH));
	if (open || perCol <= fitRows) return { cols, perCol, shown: n, hidden: 0, h: perCol * rowH };
	// clamp: keep one row slot for the "+N more" toggle
	perCol = fitRows;
	const shown = Math.max(1, cols * perCol - 1);
	return { cols, perCol, shown, hidden: n - shown, h: perCol * rowH };
}

// ---------------------------------------------------------------------------------------------- plot pen (shared)
// The runtime's plot reveal, exported so scene modules can follow the plot pen; PlotAssembler and ShowcaseStory use the
// same functions, so the model and the plot cannot drift apart.

/** Share of a plot chapter over which the plot assembles (it is complete at 90 % of the chapter). */
export const PLOT_SPAN = 0.9;

/** Series the plot draws (entries with points or bars), in spec order. */
export function plotSeries(plot: Pick<Plot, 'series'>): Series[] {
	return Array.isArray(plot.series) ? plot.series.filter((s) => s && (Array.isArray(s.points) || Array.isArray(s.bars))) : [];
}

/** Chapter range of a plot; an `alt_of` alternate uses its main plot's chapter. */
export function plotWindow(spec: Pick<ShowcaseSpec, 'chapters' | 'plots'>, plotId: string): [number, number] | null {
	const pl = spec.plots?.find((q) => q.id === plotId);
	return plotRange(spec, pl?.alt_of ?? plotId);
}

/** Local plot progress r in [0, 1] at story progress p (0 before the plot's chapter, 1 from 90 % of it on). */
export function plotProgressIn(r: [number, number], p: number): number {
	return seg(p, r[0], r[0] + PLOT_SPAN * (r[1] - r[0]));
}

/** Per-series revealed fraction 0..1 at story progress p, in plotSeries order ([] when the plot has no chapter).
 *  Points counted as drawn with the spec's default axes (log where the axis starts on log). */
export function revealAt(spec: Pick<ShowcaseSpec, 'chapters' | 'plots'>, plotId: string, p: number): number[] {
	const pl = spec.plots?.find((q) => q.id === plotId);
	const r = pl ? plotWindow(spec, plotId) : null;
	if (!pl || !r) return [];
	const rr = plotProgressIn(r, p);
	const ser = plotSeries(pl);
	const lx = startsLog(pl.x);
	const ly = startsLog(pl.y);
	return ser.map((s, i) => {
		const n = cleanPoints(s, lx, ly).length;
		if (!n) return staggerK(rr, AXES_END, 1, i, ser.length); // bars-only series: their window
		const { n: k, frac } = revealed(rr, ser.length, i, n);
		return Math.min(1, (k + frac) / n);
	});
}

export interface Pen {
	/** series index in plotSeries order */
	series: number;
	/** index (in the spec's points) of the last whole point drawn */
	index: number;
	/** pen position in data units (on the growing segment when the line is between points) */
	x: number;
	y: number;
}

/** Pen of every series at story progress p (null where nothing is drawn yet), in plotSeries order. */
export function penAt(spec: Pick<ShowcaseSpec, 'chapters' | 'plots'>, plotId: string, p: number): (Pen | null)[] {
	const pl = spec.plots?.find((q) => q.id === plotId);
	const r = pl ? plotWindow(spec, plotId) : null;
	if (!pl || !r) return [];
	const rr = plotProgressIn(r, p);
	const ser = plotSeries(pl);
	const lx = startsLog(pl.x);
	const ly = startsLog(pl.y);
	return ser.map((s, i) => {
		const pts = cleanPoints(s, lx, ly);
		const idx = cleanIndices(s, lx, ly);
		const { n, frac } = revealed(rr, ser.length, i, pts.length);
		if (n <= 0) return null;
		const last = pts[n - 1];
		if (n < pts.length && frac > 0) {
			const nx = pts[n];
			return { series: i, index: idx[n - 1], x: last[0] + (nx[0] - last[0]) * frac, y: last[1] + (nx[1] - last[1]) * frac };
		}
		return { series: i, index: idx[n - 1], x: last[0], y: last[1] };
	});
}
