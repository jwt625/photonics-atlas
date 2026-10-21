// Explore page logic: filters, metric-row selection and pairing, plotted points with omitted counts, count tables.
// Pure functions (no runes) so they are unit-tested in logic.test.ts.
import type { Component, Metric } from '../components.svelte';
import { CLASS_SLOTS, GROUP_ORDER, OTHER_GROUP, platformFamily } from './colors';

export type Qual = 'lt' | 'gt' | null;

/** One metric row prepared for plotting. */
export interface Val {
	m: Metric;
	/** plotted value (after unit conversion) */
	v: number;
	vmax: number | null;
	/** plotted unit */
	unit: string;
	/** conversion note, '' when the stored value is plotted as is */
	note: string;
	/** position of the row in the component's metric list (source order) */
	idx: number;
	/** geometry dimension: its design basis does not make the point a diamond */
	geometry: boolean;
}

export interface Pt {
	/** unique within a chart panel */
	id: string;
	c: Component;
	x: number;
	y: number;
	group: string;
	/** a performance value of the pair is simulated / design target / author estimate */
	sim: boolean;
	qx: Qual;
	qy: Qual;
	panel: number;
	/** x metric row; null when x is a condition (wavelength of the y row) or a category */
	xv: Val | null;
	yv: Val;
	xLabel: string;
	yLabel: string;
	/** x shown in the hover when xv is null */
	xText: string;
}

export interface Omitted {
	total: number;
	plotted: number;
	missingX: number;
	missingY: number;
	missingBoth: number;
	/** both values present but no pair with compatible conditions */
	incomparable: number;
	/** value <= 0 on a log axis */
	nonpositive: number;
}

export function emptyOmitted(total = 0): Omitted {
	return { total, plotted: 0, missingX: 0, missingY: 0, missingBoth: 0, incomparable: 0, nonpositive: 0 };
}

export function combineOmitted(xs: Omitted[]): Omitted {
	const out = emptyOmitted();
	for (const x of xs) for (const k of Object.keys(out) as (keyof Omitted)[]) out[k] += x[k];
	return out;
}

// ---------------------------------------------------------------------------------------------------------------
// filters

export interface ExFilters {
	/** class families (prefix before the dot); empty = all */
	classes: string[];
	/** platform families (colors.ts); empty = all */
	families: string[];
	/** keep measured performance values only (and components with at least one measured value) */
	measuredOnly: boolean;
	/** source id prefix (eo / ofc2026 / pk); empty = all */
	corpora: string[];
	yearMin: number | null;
	yearMax: number | null;
}

export function defaultExFilters(): ExFilters {
	return { classes: [], families: [], measuredOnly: false, corpora: [], yearMin: null, yearMax: null };
}

export const classFamily = (c: Component): string => c.class.split('.')[0];
export const corpusOf = (c: Component): string => {
	const i = c.source.id.indexOf(':');
	return i > 0 ? c.source.id.slice(0, i) : c.source.id;
};
export const yearOf = (c: Component): number | null => {
	const y = Number(c.source.year);
	return c.source.year && Number.isFinite(y) ? y : null;
};
export const familyOf = (c: Component): string => platformFamily(c.platform);

export function applyExFilters(comps: Component[], f: ExFilters): Component[] {
	return comps.filter((c) => {
		if (f.classes.length && !f.classes.includes(classFamily(c))) return false;
		if (f.families.length && !f.families.includes(familyOf(c))) return false;
		if (f.corpora.length && !f.corpora.includes(corpusOf(c))) return false;
		const y = yearOf(c);
		if (f.yearMin !== null && (y === null || y < f.yearMin)) return false;
		if (f.yearMax !== null && (y === null || y > f.yearMax)) return false;
		if (f.measuredOnly && !c.metrics.some((m) => m.basis === 'measured')) return false;
		return true;
	});
}

export function countBy<T>(items: T[], key: (t: T) => string | string[]): Map<string, number> {
	const out = new Map<string, number>();
	for (const it of items) {
		const k = key(it);
		for (const v of Array.isArray(k) ? k : [k]) if (v) out.set(v, (out.get(v) ?? 0) + 1);
	}
	return out;
}

// ---------------------------------------------------------------------------------------------------------------
// metric rows

/** wavelength_inferred is in components.json but not in the shared Metric type */
export function isInferred(m: Metric): boolean {
	const w = (m as Metric & { wavelength_inferred?: unknown }).wavelength_inferred;
	return w === true || w === 'true' || w === 'True' || w === 1 || w === '1';
}

export const MODELLED = new Set(['simulated', 'design_target', 'author_estimate']);

export function num(s: string | undefined | null): number | null {
	if (s === undefined || s === null || String(s).trim() === '') return null;
	const v = Number(s);
	return Number.isFinite(v) ? v : null;
}

/** lt / le: upper bound (arrow down on y); gt / ge: lower bound; approx: plotted as a value. */
export function qualOf(m: Metric): Qual {
	if (m.qualifier === 'lt' || m.qualifier === 'le') return 'lt';
	if (m.qualifier === 'gt' || m.qualifier === 'ge') return 'gt';
	return null;
}

export interface AxisSpec {
	/** hover label, e.g. "Loss per coupler" */
	label: string;
	/** accepted parameter names */
	params: string[];
	/** accepted scope values; undefined = any */
	scopes?: string[];
	/** unit conversion of the stored value; null when the row cannot be converted */
	convert?: (m: Metric, v: number) => { v: number; unit: string; note: string } | null;
	geometry?: boolean;
}

/** Usable rows of one axis: finite value, not a spread (statistic std), accepted scope, basis filter. */
export function candidates(c: Component, spec: AxisSpec, measuredOnly: boolean): Val[] {
	const out: Val[] = [];
	c.metrics.forEach((m, idx) => {
		if (!spec.params.includes(m.parameter)) return;
		if (spec.scopes && !spec.scopes.includes(m.scope ?? '')) return;
		if (m.statistic === 'std') return;
		// geometry dimensions are design values by nature; the measured-only filter applies to performance values
		if (measuredOnly && !spec.geometry && m.basis !== 'measured') return;
		const v0 = num(m.value);
		if (v0 === null) return;
		const vm0 = num(m.value_max);
		if (spec.convert) {
			const cv = spec.convert(m, v0);
			if (!cv) return;
			const cm = vm0 === null ? null : spec.convert(m, vm0);
			out.push({ m, v: cv.v, vmax: cm ? cm.v : null, unit: cv.unit, note: cv.note, idx, geometry: !!spec.geometry });
		} else {
			out.push({ m, v: v0, vmax: vm0, unit: m.unit, note: '', idx, geometry: !!spec.geometry });
		}
	});
	return out;
}

/** dBm -> mW (exact); mW rows pass through. */
export function toMw(m: Metric, v: number): { v: number; unit: string; note: string } | null {
	if (m.parameter === 'output_power_dbm') return { v: 10 ** (v / 10), unit: 'mW', note: `converted from ${m.value} dBm` };
	if (m.parameter === 'output_power_mw') return { v, unit: 'mW', note: '' };
	return null;
}

// ---------------------------------------------------------------------------------------------------------------
// condition compatibility (pairing rule)

/** Nominal band edges in nm (ITU O to U; the others only bound the compatibility check). */
export const BAND_NM: Record<string, [number, number]> = {
	uv: [100, 380],
	visible: [380, 750],
	nir_below_o: [750, 1260],
	o_band: [1260, 1360],
	e_band: [1360, 1460],
	s_band: [1460, 1530],
	c_band: [1530, 1565],
	l_band: [1565, 1625],
	u_band: [1625, 1675],
	cl_band: [1530, 1625],
	nir_above_u: [1675, 2500],
	mid_ir: [2500, 100000]
};
/** two stated wavelengths (or ranges) closer than this are the same condition */
export const WL_TOL_NM = 2;
export const T_TOL_K = 5;

function wlRange(m: Metric): [number, number] | null {
	const a = num(m.wavelength_nm);
	if (a === null) return null;
	const b = num(m.wavelength_max_nm);
	return b === null ? [a, a] : [Math.min(a, b), Math.max(a, b)];
}
function bandRange(m: Metric): [number, number] | null {
	return m.band ? (BAND_NM[m.band] ?? null) : null;
}
const POL = new Set(['te', 'tm']);

/**
 * Why two rows of one component cannot share a point, or null when compatible. A condition is compared only when
 * both rows carry it: stated wavelengths (ranges) must agree within WL_TOL_NM; stated bands must overlap; a stated
 * wavelength must fall inside the other row's band; TE vs TM conflicts; temperatures must agree within T_TOL_K.
 * A row without a condition is compatible with any value of it.
 */
export function conflict(a: Metric, b: Metric): string | null {
	const wa = wlRange(a);
	const wb = wlRange(b);
	if (wa && wb && Math.max(wa[0], wb[0]) - Math.min(wa[1], wb[1]) > WL_TOL_NM) return 'wavelength';
	const ba = bandRange(a);
	const bb = bandRange(b);
	if (ba && bb && !(Math.max(ba[0], bb[0]) < Math.min(ba[1], bb[1]))) return 'band';
	if (wa && bb && !(wa[0] <= bb[1] && wa[1] >= bb[0])) return 'band';
	if (wb && ba && !(wb[0] <= ba[1] && wb[1] >= ba[0])) return 'band';
	if (a.polarization && b.polarization && POL.has(a.polarization) && POL.has(b.polarization) && a.polarization !== b.polarization)
		return 'polarization';
	const ta = num(a.temperature_k);
	const tb = num(b.temperature_k);
	if (ta !== null && tb !== null && Math.abs(ta - tb) > T_TOL_K) return 'temperature';
	return null;
}

/** both rows carry a spectral condition (wavelength or band), so compatibility was checked, not assumed */
function explicitMatch(a: Metric, b: Metric): boolean {
	return !!(wlRange(a) || bandRange(a)) && !!(wlRange(b) || bandRange(b));
}

const modelled = (v: Val): boolean => !v.geometry && MODELLED.has(v.m.basis);

/** Single-row preference: non-modelled first, then unqualified, then source order. */
function rowKey(v: Val): number[] {
	return [modelled(v) ? 1 : 0, qualOf(v.m) ? 1 : 0, v.idx];
}

function lexLess(a: number[], b: number[]): boolean {
	for (let i = 0; i < Math.max(a.length, b.length); i++) {
		const d = (a[i] ?? 0) - (b[i] ?? 0);
		if (d !== 0) return d < 0;
	}
	return false;
}

export function pickRow(vals: Val[]): Val | null {
	let best: Val | null = null;
	for (const v of vals) if (!best || lexLess(rowKey(v), rowKey(best))) best = v;
	return best;
}

export type PairStatus = 'ok' | 'missingX' | 'missingY' | 'missingBoth' | 'incomparable';

/**
 * Pairing rule: a point pairs an x row and a y row of the same component only when conflict() is null. Among the
 * compatible pairs the preferred one has fewer modelled (simulated / design target / author estimate) performance
 * values, then fewer bounds (lt / gt), then an explicit spectral match (both rows carry a wavelength or band) over
 * an assumed one (a row without a condition), then the earliest rows in source order.
 */
export function pairRows(xs: Val[], ys: Val[]): { status: PairStatus; x?: Val; y?: Val } {
	if (!xs.length && !ys.length) return { status: 'missingBoth' };
	if (!xs.length) return { status: 'missingX' };
	if (!ys.length) return { status: 'missingY' };
	let best: { x: Val; y: Val; key: number[] } | null = null;
	for (const x of xs)
		for (const y of ys) {
			if (conflict(x.m, y.m)) continue;
			const key = [
				(modelled(x) ? 1 : 0) + (modelled(y) ? 1 : 0),
				(qualOf(x.m) ? 1 : 0) + (qualOf(y.m) ? 1 : 0),
				explicitMatch(x.m, y.m) ? 0 : 1,
				x.idx + y.idx,
				x.idx
			];
			if (!best || lexLess(key, best.key)) best = { x, y, key };
		}
	return best ? { status: 'ok', x: best.x, y: best.y } : { status: 'incomparable' };
}

function tally(om: Omitted, s: PairStatus): void {
	if (s === 'missingX') om.missingX++;
	else if (s === 'missingY') om.missingY++;
	else if (s === 'missingBoth') om.missingBoth++;
	else if (s === 'incomparable') om.incomparable++;
}

export interface BuildOpts {
	measuredOnly: boolean;
	xLog?: boolean;
	yLog?: boolean;
	panel?: number;
}

/** x-y scatter of two metrics; one point per component (the preferred compatible pair). */
export function buildScatter(comps: Component[], xs: AxisSpec, ys: AxisSpec, o: BuildOpts): { pts: Pt[]; omitted: Omitted } {
	const om = emptyOmitted(comps.length);
	const pts: Pt[] = [];
	for (const c of comps) {
		const r = pairRows(candidates(c, xs, o.measuredOnly), candidates(c, ys, o.measuredOnly));
		if (r.status !== 'ok' || !r.x || !r.y) {
			tally(om, r.status);
			continue;
		}
		if ((o.xLog && r.x.v <= 0) || (o.yLog && r.y.v <= 0)) {
			om.nonpositive++;
			continue;
		}
		pts.push({
			id: c.component_id,
			c,
			x: r.x.v,
			y: r.y.v,
			group: familyOf(c),
			sim: modelled(r.x) || modelled(r.y),
			qx: qualOf(r.x.m),
			qy: qualOf(r.y.m),
			panel: o.panel ?? 0,
			xv: r.x,
			yv: r.y,
			xLabel: xs.label,
			yLabel: ys.label,
			xText: ''
		});
		om.plotted++;
	}
	return { pts, omitted: om };
}

const CENTER_WL: AxisSpec = { label: 'Center wavelength', params: ['center_wavelength_nm'] };

/**
 * y metric against wavelength. x is the wavelength stated with the y row (wavelength_nm; the range start when a
 * range is given), else the component's center_wavelength_nm row when compatible with the y row (band check).
 * A band alone gives no x position (counted as missing x).
 */
export function buildVsWavelength(comps: Component[], ys: AxisSpec, o: BuildOpts): { pts: Pt[]; omitted: Omitted } {
	const om = emptyOmitted(comps.length);
	const pts: Pt[] = [];
	for (const c of comps) {
		const yv = candidates(c, ys, o.measuredOnly);
		const cw = candidates(c, CENTER_WL, o.measuredOnly);
		type Opt = { y: Val; x: number; xRow: Val | null; xText: string; key: number[] };
		const opts: Opt[] = [];
		for (const v of yv) {
			const w = num(v.m.wavelength_nm);
			if (w !== null) {
				const wmax = v.m.wavelength_max_nm;
				const xText = `${v.m.wavelength_nm}${wmax ? '-' + wmax : ''} nm, stated with the y row${isInferred(v.m) ? ' (inferred)' : ''}`;
				opts.push({ y: v, x: w, xRow: null, xText, key: [modelled(v) ? 1 : 0, qualOf(v.m) ? 1 : 0, 0, v.idx] });
			} else
				for (const r of cw)
					// the center wavelength row's value is itself a wavelength condition
					if (!conflict({ ...r.m, wavelength_nm: r.m.value, wavelength_max_nm: undefined }, v.m))
						opts.push({
							y: v,
							x: r.v,
							xRow: r,
							xText: `${r.m.value} nm, center_wavelength_nm row (${r.m.basis}; ${r.m.locator})`,
							key: [(modelled(v) ? 1 : 0) + (modelled(r) ? 1 : 0), qualOf(v.m) ? 1 : 0, 1, v.idx + r.idx]
						});
		}
		let best: Opt | null = null;
		for (const op of opts) if (!best || lexLess(op.key, best.key)) best = op;
		if (!best) {
			const anyWl = cw.length > 0 || c.metrics.some((m) => num(m.wavelength_nm) !== null);
			if (!yv.length) tally(om, anyWl ? 'missingY' : 'missingBoth');
			else tally(om, cw.length ? 'incomparable' : 'missingX');
			continue;
		}
		const { x, y, xRow, xText } = best;
		if ((o.xLog && x <= 0) || (o.yLog && y.v <= 0)) {
			om.nonpositive++;
			continue;
		}
		pts.push({
			id: c.component_id,
			c,
			x,
			y: y.v,
			group: familyOf(c),
			sim: modelled(y) || (xRow ? modelled(xRow) : false),
			qx: null,
			qy: qualOf(y.m),
			panel: o.panel ?? 0,
			xv: null,
			yv: y,
			xLabel: 'Wavelength',
			yLabel: ys.label,
			xText
		});
		om.plotted++;
	}
	return { pts, omitted: om };
}

/** Deterministic jitter in [-1, 1] from an id string. */
export function jitter(id: string): number {
	let h = 2166136261;
	for (let i = 0; i < id.length; i++) {
		h ^= id.charCodeAt(i);
		h = Math.imul(h, 16777619);
	}
	return (((h >>> 0) % 2001) - 1000) / 1000;
}

export function median(xs: number[]): number | null {
	if (!xs.length) return null;
	const s = [...xs].sort((a, b) => a - b);
	const h = Math.floor(s.length / 2);
	return s.length % 2 ? s[h] : (s[h - 1] + s[h]) / 2;
}

export interface GroupStat {
	group: string;
	index: number;
	/** points entering the median (unqualified, basis measured) */
	n: number;
	total: number;
	median: number | null;
}

/**
 * Strip plot of one metric by platform family (x = family index + jitter). Only families with points get a column.
 * Median per family over unqualified values with basis measured.
 */
export function buildStrip(comps: Component[], ys: AxisSpec, o: BuildOpts): { pts: Pt[]; omitted: Omitted; stats: GroupStat[] } {
	const om = emptyOmitted(comps.length);
	const raw: { c: Component; y: Val }[] = [];
	for (const c of comps) {
		const y = pickRow(candidates(c, ys, o.measuredOnly));
		if (!y) {
			om.missingY++;
			continue;
		}
		if (o.yLog && y.v <= 0) {
			om.nonpositive++;
			continue;
		}
		raw.push({ c, y });
	}
	const present = GROUP_ORDER.filter((g) => raw.some((r) => familyOf(r.c) === g));
	const pos = new Map(present.map((g, i) => [g, i]));
	const pts: Pt[] = raw.map(({ c, y }) => ({
		id: c.component_id,
		c,
		x: (pos.get(familyOf(c)) ?? 0) + 0.28 * jitter(c.component_id),
		y: y.v,
		group: familyOf(c),
		sim: modelled(y),
		qx: null,
		qy: qualOf(y.m),
		panel: o.panel ?? 0,
		xv: null,
		yv: y,
		xLabel: 'Platform',
		yLabel: ys.label,
		xText: c.platform || 'not stated'
	}));
	om.plotted = pts.length;
	const stats: GroupStat[] = present.map((g, i) => {
		const gp = pts.filter((p) => p.group === g);
		const ys2 = gp.filter((p) => p.yv.m.basis === 'measured' && !p.qy).map((p) => p.y);
		return { group: g, index: i, n: ys2.length, total: gp.length, median: median(ys2) };
	});
	return { pts, omitted: om, stats };
}

// ---------------------------------------------------------------------------------------------------------------
// count panels

export const CLASS_OTHER = 'other_classes';

export function classSlot(family: string): string {
	return (CLASS_SLOTS as readonly string[]).includes(family) ? family : CLASS_OTHER;
}

/** Components per source year, stacked by class family (fixed slots + one folded group). */
export function yearStack(comps: Component[]): { years: number[]; groups: string[]; counts: Map<string, Map<number, number>>; noYear: number } {
	const counts = new Map<string, Map<number, number>>();
	const years = new Set<number>();
	let noYear = 0;
	for (const c of comps) {
		const y = yearOf(c);
		if (y === null) {
			noYear++;
			continue;
		}
		const g = classSlot(classFamily(c));
		const m = counts.get(g) ?? new Map<number, number>();
		m.set(y, (m.get(y) ?? 0) + 1);
		counts.set(g, m);
		years.add(y);
	}
	const ys = [...years].sort((a, b) => a - b);
	const full: number[] = [];
	if (ys.length) for (let y = ys[0]; y <= ys[ys.length - 1]; y++) full.push(y);
	const order = [...CLASS_SLOTS, CLASS_OTHER] as string[];
	return { years: full, groups: order.filter((g) => counts.has(g)), counts, noYear };
}

/** Class (family or full class.subtype) x platform family counts; rows by total, descending. */
export function classPlatformMatrix(comps: Component[], level: 'family' | 'subtype'): { rows: string[]; cols: string[]; z: number[][] } {
	const key = (c: Component) => (level === 'family' ? classFamily(c) : c.class);
	const tot = countBy(comps, key);
	const rows = [...tot.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).map((e) => e[0]);
	const cols = GROUP_ORDER.filter((g) => comps.some((c) => familyOf(c) === g));
	const ri = new Map(rows.map((r, i) => [r, i]));
	const ci = new Map(cols.map((g, i) => [g, i]));
	const z = rows.map(() => cols.map(() => 0));
	for (const c of comps) z[ri.get(key(c))!][ci.get(familyOf(c))!]++;
	return { rows, cols, z };
}

export function topCounts(map: Map<string, number>, n: number | null): [string, number][] {
	const e = [...map.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
	return n === null ? e : e.slice(0, n);
}

export { OTHER_GROUP };
