// Column filters of the shared table (DevLog-013 D504): multi-select for discrete columns, min / max range for numeric
// columns, contains for free text. Pure logic, no framework state.
import type { Snippet } from 'svelte';
import { fold } from '../orgs';

export const EMPTY = '(empty)';

export type Kind = 'text' | 'enum' | 'num' | 'none';
/** One side unbounded: a stored "> 60" is { lo: 60, hi: Infinity, loOpen: true }. */
export interface NumSpan {
	lo: number;
	hi: number;
	loOpen?: boolean;
	hiOpen?: boolean;
}
/** A value, a stored low-high range, or a stored bound. */
export type NumVal = number | [number, number] | NumSpan;

export interface Col<R> {
	key: string;
	label: string;
	/** shown muted in the header */
	unit?: string;
	tip?: string;
	kind: Kind;
	/** text: one string. enum: one or several values. num: one or several numbers / ranges. Empty when absent. */
	get?: (r: R) => string | string[] | number | NumVal[] | null | undefined;
	/** sort key when it is not the filter value */
	sort?: (r: R) => string | number | null | undefined;
	/** cell text; default: the filter value */
	text?: (r: R) => string;
	cellTip?: (r: R) => string | undefined;
	/** small letter after the value (basis of the stored row) */
	badge?: (r: R) => string;
	badgeOn?: (r: R) => boolean;
	/** "+n": further rows behind the value */
	more?: (r: R) => number;
	/** custom cell markup (links, swatches) */
	cell?: Snippet<[R]>;
	right?: boolean;
	/** width / clipping class on the cell: lbl, pub, wide, wrap, mono */
	cls?: string;
	/** fixed width in px; default: from the header and the column's values, never shrinking */
	w?: number;
	/** no (empty) option: absent values are not a state of this column */
	noEmpty?: boolean;
	enumLabel?: (v: string) => string;
	/** first direction of the sort cycle (default: descending for numbers, ascending otherwise) */
	firstDir?: 1 | -1;
}

export type Filter = { t: 'enum'; sel: string[] } | { t: 'num'; min: number | null; max: number | null } | { t: 'text'; q: string };
export type Filters = Record<string, Filter>;
export interface Sort {
	key: string;
	dir: 1 | -1;
}

/** One entry of the column chooser. */
export interface Choice {
	key: string;
	label: string;
	unit?: string;
	group: string;
	tip?: string;
	/** rows with a value; omitted for always-present columns */
	n?: number;
}

export function enumVals<R>(c: Col<R>, r: R): string[] {
	const v = c.get?.(r);
	if (v === null || v === undefined || v === '') return [];
	return (Array.isArray(v) ? v : [v]).map(String).filter((x) => x !== '');
}

export function numVals<R>(c: Col<R>, r: R): NumVal[] {
	const v = c.get?.(r);
	if (v === null || v === undefined || v === '') return [];
	const xs = (Array.isArray(v) ? v : [v]) as unknown[];
	const out: NumVal[] = [];
	for (const x of xs) {
		if (Array.isArray(x)) {
			if (Number.isFinite(x[0]) && Number.isFinite(x[1])) out.push([x[0], x[1]]);
		} else if (typeof x === 'object' && x !== null) out.push(x as NumSpan);
		else if (x !== '' && x !== null && Number.isFinite(Number(x))) out.push(Number(x));
	}
	return out;
}

export function textVal<R>(c: Col<R>, r: R): string {
	const v = c.get?.(r);
	if (v === null || v === undefined) return '';
	return Array.isArray(v) ? v.join(', ') : String(v);
}

export function isActive(f: Filter | undefined): boolean {
	if (!f) return false;
	if (f.t === 'enum') return f.sel.length > 0;
	if (f.t === 'num') return f.min !== null || f.max !== null;
	return f.q.trim() !== '';
}

const spanOf = (v: NumVal): NumSpan => (typeof v === 'number' ? { lo: v, hi: v } : Array.isArray(v) ? { lo: v[0], hi: v[1] } : v);

/** Overlap of a value with a filter range. A stored bound is open at its value: "> 60" cannot match Max 60. */
export function inRange(v: NumVal, min: number | null, max: number | null): boolean {
	const s = spanOf(v);
	return (min === null || (s.hiOpen ? s.hi > min : s.hi >= min)) && (max === null || (s.loOpen ? s.lo < max : s.lo <= max));
}

/** A range matches if any value in the cell falls in it (a stored range or bound: if it overlaps); an empty cell never matches. */
export function matches<R>(c: Col<R>, f: Filter, r: R): boolean {
	if (!isActive(f)) return true;
	if (f.t === 'enum') {
		const vs = enumVals(c, r);
		if (!vs.length) return f.sel.includes(EMPTY);
		return vs.some((v) => f.sel.includes(v));
	}
	if (f.t === 'num') return numVals(c, r).some((v) => inRange(v, f.min, f.max));
	return fold(textVal(c, r)).includes(fold(f.q.trim()));
}

/** Rows passing every active filter whose column is known, optionally ignoring one column (facets). */
export function applyFilters<R>(rows: R[], cols: Col<R>[], filters: Filters, except?: string): R[] {
	const active = cols.filter((c) => c.key !== except && isActive(filters[c.key]));
	if (!active.length) return rows;
	return rows.filter((r) => active.every((c) => matches(c, filters[c.key], r)));
}

export interface Facet {
	value: string;
	label: string;
	n: number;
}

/** Values of a discrete column with their counts, most frequent first; `keep` (the current selection) stays listed at 0,
 *  so it can be unticked when other filters have removed it. */
export function facets<R>(rows: R[], c: Col<R>, keep: string[] = []): Facet[] {
	const m = new Map<string, number>();
	let empty = 0;
	for (const r of rows) {
		const vs = new Set(enumVals(c, r));
		if (!vs.size) empty++;
		for (const v of vs) m.set(v, (m.get(v) ?? 0) + 1);
	}
	const out = [...m].map(([value, n]) => ({ value, label: c.enumLabel?.(value) ?? value, n })).sort((a, b) => b.n - a.n || a.label.localeCompare(b.label));
	if (empty && !c.noEmpty) out.push({ value: EMPTY, label: EMPTY, n: empty });
	for (const v of keep) if (!out.some((o) => o.value === v)) out.push({ value: v, label: v === EMPTY ? EMPTY : (c.enumLabel?.(v) ?? v), n: 0 });
	return out;
}

export interface NumStats {
	min: number;
	max: number;
	/** rows with a value */
	cells: number;
	hist: number[];
	log: boolean;
}

/** Domain and histogram of a numeric column; log bins when positive values span three decades or more. */
export function numStats<R>(rows: R[], c: Col<R>, bins = 24): NumStats | null {
	const xs: number[] = [];
	let cells = 0;
	for (const r of rows) {
		const vs = numVals(c, r);
		if (vs.length) cells++;
		for (const v of vs) {
			const sp = spanOf(v);
			if (Number.isFinite(sp.lo)) xs.push(sp.lo);
			if (Number.isFinite(sp.hi) && sp.hi !== sp.lo) xs.push(sp.hi);
		}
	}
	if (!xs.length) return null;
	let min = Infinity,
		max = -Infinity;
	for (const x of xs) {
		if (x < min) min = x;
		if (x > max) max = x;
	}
	const log = min > 0 && max / min >= 1000;
	const f = (x: number) => (log ? Math.log10(x) : x);
	const a = f(min),
		w = f(max) - a;
	const hist = Array.from({ length: bins }, () => 0);
	for (const x of xs) hist[w > 0 ? Math.min(bins - 1, Math.floor(((f(x) - a) / w) * bins)) : 0]++;
	return { min, max, cells, hist, log };
}

type Key = string | number | null;

function keyOf<R>(c: Col<R>, r: R): Key {
	if (c.sort) {
		const s = c.sort(r);
		if (s === null || s === undefined || s === '') return null;
		return typeof s === 'string' ? fold(s) : s;
	}
	if (c.kind === 'num') {
		const v = numVals(c, r)[0];
		if (v === undefined) return null;
		const sp = spanOf(v);
		return Number.isFinite(sp.lo) ? sp.lo : sp.hi;
	}
	const s = c.kind === 'enum' ? (enumVals(c, r)[0] ?? '') : textVal(c, r);
	return s === '' ? null : fold(s);
}

/** Sorted copy; empty cells last in both directions; ties by `tie`, then input order. */
export function sortRows<R>(rows: R[], c: Col<R> | undefined, dir: 1 | -1, tie?: (a: R, b: R) => number): R[] {
	const dec = rows.map((r, i) => ({ r, i, k: c ? keyOf(c, r) : null }));
	dec.sort((a, b) => {
		if (a.k !== b.k) {
			if (a.k === null) return 1;
			if (b.k === null) return -1;
			if (a.k < b.k) return -dir;
			if (a.k > b.k) return dir;
		}
		return (tie ? tie(a.r, b.r) : 0) || a.i - b.i;
	});
	return dec.map((d) => d.r);
}

/** Next state of the sort cycle of a header: first direction, other direction, none. */
export function nextSort<R>(cur: Sort | null, c: Col<R>): Sort | null {
	const first = c.firstDir ?? (c.kind === 'num' ? -1 : 1);
	if (!cur || cur.key !== c.key) return { key: c.key, dir: first };
	return cur.dir === first ? { key: c.key, dir: -first as 1 | -1 } : null;
}

const fmtN = (x: number) => String(+x.toPrecision(6));

export function chipText<R>(c: Col<R>, f: Filter): string {
	if (f.t === 'enum') return f.sel.length <= 2 ? f.sel.map((v) => c.enumLabel?.(v) ?? v).join(', ') : `${f.sel.length} selected`;
	if (f.t === 'text') return `"${f.q.trim()}"`;
	const u = c.unit ? ' ' + c.unit : '';
	if (f.min !== null && f.max !== null) return `${fmtN(f.min)} to ${fmtN(f.max)}${u}`;
	return f.min !== null ? `>= ${fmtN(f.min)}${u}` : `<= ${fmtN(f.max as number)}${u}`;
}

const CAP: Record<string, number> = { lbl: 240, pub: 300, clip: 170, wide: 420, wrap: 320 };
const PX_PER_CHAR = 6.4;
const CELL_PAD = 14;
const HEADER_CHARS = 18; // a longer header wraps

/** Column width in px from the header and the longest cell text (characters). */
export function colWidth<R>(c: Col<R>, chars: number): number {
	if (c.w) return c.w;
	const head = Math.min(c.label.length + (c.unit ? c.unit.length + 1 : 0) + (c.kind === 'none' ? 0 : 4), HEADER_CHARS);
	return Math.min(CAP[c.cls ?? ''] ?? 280, Math.max(44, Math.ceil(Math.max(chars, head) * PX_PER_CHAR) + CELL_PAD));
}

/** Whether a text of this length may not fit: an upper estimate of the text width, so a tip is never missing on a clipped cell. */
export const mayClip = (chars: number, width: number): boolean => chars * 7.4 + CELL_PAD > width;

/** decodeURIComponent that keeps a malformed string as it is (a hand-edited hash must not throw). */
export function safeDecode(s: string): string {
	try {
		return decodeURIComponent(s);
	} catch {
		return s;
	}
}

/** Publication date to the integer year of a year-range filter: 2023 matches every date in 2023. */
export const dateYear = (d: string | undefined): number | null => {
	const y = Number((d ?? '').slice(0, 4));
	return Number.isFinite(y) && y > 0 ? y : null;
};
