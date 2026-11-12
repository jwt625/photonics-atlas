// Pure geometry of the plot assembler (PlotAssembler.svelte): data ranges, linear / log scales, ticks and how much of
// the plot is drawn at a local progress r in [0, 1] (axes first, then the points of each series in spec order).
import type { Axis, Bar, Plot, Series } from './types';
import { clamp01, seg } from './progress';

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
		for (const pt of [...(s.points ?? []), ...barPoints(s)]) {
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

export function fmt(v: number): string {
	if (v === 0) return '0';
	const a = Math.abs(v);
	if (a >= 1e5 || a < 1e-3) return v.toExponential(0).replace('e+', 'e');
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

/** Plain-text form of runs for tooltips (superscript / subscript digits where Unicode has them). */
export function plain(runs: Run[]): string {
	const SUP: Record<string, string> = { '0': '\u2070', '1': '\u00b9', '2': '\u00b2', '3': '\u00b3', '4': '\u2074', '5': '\u2075', '6': '\u2076', '7': '\u2077', '8': '\u2078', '9': '\u2079', '\u2212': '\u207b', '+': '\u207a' };
	const SUB: Record<string, string> = { '0': '\u2080', '1': '\u2081', '2': '\u2082', '3': '\u2083', '4': '\u2084', '5': '\u2085', '6': '\u2086', '7': '\u2087', '8': '\u2088', '9': '\u2089' };
	return runs.map((r) => (r.k ? [...r.t].map((c) => (r.k === 'sup' ? SUP : SUB)[c] ?? c).join('') : r.t)).join('');
}

export function styleOf(s: Series): 'line' | 'points' | 'both' | 'dashed' {
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
