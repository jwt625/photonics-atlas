// /components as one row per component (DevLog-013 D502, D503): which parameters become columns for a selection, which
// stored row stands for a cell, and the row-level filters (basis, scope, wavelength) that feed the cells.
import { fmtValue, fmtWavelength, type Component, type Metric } from '../components.svelte';
import type { Filter, Filters, NumVal } from './filters';
import { inRange, isActive } from './filters';

export type Parameters = Record<string, { unit: string; kind: string; def: string }>;

const UNIT: Record<string, string> = { um: 'µm', um2: 'µm²', deg: '°', count: '', '1': '' };
export const unitText = (u: string | undefined): string => (u === undefined ? '' : (UNIT[u] ?? u));

const UNIT_TOKEN = /^(db|dbm|pct|nm|um|mm|cm|um2|cm2|ghz|mhz|khz|hz|mw|w|ma|na|a|v|ff|ohm|deg|us|ns|ps|pm|k|per|m|s)$/;

/** Parameter id without its unit tail: insertion_loss_db -> insertion loss, prop_loss_db_per_cm -> prop loss. */
export function paramLabel(p: string): string {
	const t = p.split('_');
	while (t.length > 1 && UNIT_TOKEN.test(t[t.length - 1])) t.pop();
	return t.join(' ');
}

export const BASIS_BADGE: Record<string, string> = { design_target: 'D', measured: 'M', extracted_from_figure: 'F', specification: 'P', derived: 'R', author_estimate: 'E', simulated: 'S' };
const BASIS_RANK: Record<string, number> = { measured: 0, extracted_from_figure: 1, specification: 2, design_target: 3, derived: 4, author_estimate: 5, simulated: 6 };

const metricOrder = (id: string): number => {
	const m = /-m(\d+)$/.exec(id);
	return m ? Number(m[1]) : 1e9;
};

/** The row that stands for a cell: not a spread statistic, measured first, then no condition, no qualifier, metric order. */
export function repRow(rows: Metric[]): Metric {
	const key = (m: Metric): number[] => [m.statistic === 'std' ? 1 : 0, BASIS_RANK[m.basis] ?? 9, m.condition ? 1 : 0, m.qualifier ? 1 : 0, metricOrder(m.metric_id)];
	let best = rows[0],
		kb = key(best);
	for (let i = 1; i < rows.length; i++) {
		const k = key(rows[i]);
		for (let j = 0; j < k.length; j++) {
			if (k[j] === kb[j]) continue;
			if (k[j] < kb[j]) [best, kb] = [rows[i], k];
			break;
		}
	}
	return best;
}

/** Rows with no scope and rows stored as `unspecified` share one column. */
export const normScope = (s: string | undefined): string => (s && s !== 'unspecified' ? s : '');
/** Column / cell identity of a stored row: the parameter and its scope, so scopes never mix in a cell, sort or range. */
export const cellKey = (m: Metric): string => m.parameter + '@' + normScope(m.scope);
export const scopeLabel = (s: string): string => (s ? s.replace(/_/g, ' ') : 'unspecified');

export interface RankedParam {
	/** cellKey of the column */
	key: string;
	param: string;
	/** normalized scope of the column's rows */
	scope: string;
	/** the parameter has more than one scope in this selection: one column per scope */
	split: boolean;
	/** components with at least one row in the column */
	n: number;
	kind: string;
}

/** Columns of a set of components: performance before geometry, then by coverage, then by name. A parameter with more than
 *  one scope gets one column per scope. Spread statistics are not values: a parameter with only those has no column. */
export function rankParams(comps: Component[], params: Parameters): RankedParam[] {
	const m = new Map<string, number>();
	const scopes = new Map<string, Set<string>>();
	for (const c of comps) {
		const seen = new Set<string>();
		for (const x of c.metrics) {
			if (x.statistic === 'std') continue;
			seen.add(cellKey(x));
			let s = scopes.get(x.parameter);
			if (!s) scopes.set(x.parameter, (s = new Set()));
			s.add(normScope(x.scope));
		}
		for (const k of seen) m.set(k, (m.get(k) ?? 0) + 1);
	}
	const order = (k: string) => (k === 'performance' ? 0 : 1);
	return [...m]
		.map(([key, n]) => {
			const [param, scope] = key.split('@');
			return { key, param, scope, split: (scopes.get(param)?.size ?? 1) > 1, n, kind: params[param]?.kind ?? 'performance' };
		})
		.sort((a, b) => order(a.kind) - order(b.kind) || b.n - a.n || a.key.localeCompare(b.key));
}

export const MAX_PERF = 12;
export const MAX_GEOM = 8;

/** Columns shown by default: reported by at least 10 % of the selection (3 rows at least; any row below 10 rows), at most
 *  MAX_PERF performance and MAX_GEOM geometry columns. The others stay in the column chooser. */
export function defaultParams(ranked: RankedParam[], total: number): string[] {
	const min = total < 10 ? 1 : Math.max(3, Math.ceil(0.1 * total));
	let perf = 0,
		geom = 0;
	const out: string[] = [];
	for (const r of ranked) {
		if (r.n < min) continue;
		if (r.kind === 'performance' ? perf++ < MAX_PERF : geom++ < MAX_GEOM) out.push(r.key);
	}
	return out;
}

// ITU-T G-series band edges (nm); other stored bands have no fixed range and fail an active wavelength filter
const BAND: Record<string, [number, number]> = { o_band: [1260, 1360], e_band: [1360, 1460], s_band: [1460, 1530], c_band: [1530, 1565], l_band: [1565, 1625], cl_band: [1530, 1625] };

/** Wavelength of a row in nm: a center wavelength row is its own value; otherwise the stored condition or range, else its
 *  band's range. */
export function rowWavelength(m: Metric): [number, number] | null {
	if (m.parameter === 'center_wavelength_nm') {
		const a = Number(m.value),
			b = m.value_max ? Number(m.value_max) : a;
		if (Number.isFinite(a) && Number.isFinite(b)) return [a, b];
	}
	if (m.wavelength_nm) {
		const a = Number(m.wavelength_nm),
			b = m.wavelength_max_nm ? Number(m.wavelength_max_nm) : a;
		if (Number.isFinite(a) && Number.isFinite(b)) return [a, b];
	}
	return m.band ? (BAND[m.band] ?? null) : null;
}

export type RowResult = 'hit' | 'exempt' | 'fail';

/** One stored row against the row filters. `fail`: out of the cell. `exempt`: stays in its cell, but a filter did not
 *  apply to it (a geometry row has no wavelength), so it does not keep a component in the table. */
export function rowPass(m: Metric, f: Filters, params: Parameters): RowResult {
	let exempt = false;
	const basis = f.basis;
	if (isActive(basis) && basis.t === 'enum' && !basis.sel.includes(m.basis)) return 'fail';
	const wl = f.wl;
	if (isActive(wl) && wl.t === 'num') {
		if (params[m.parameter]?.kind === 'geometry') exempt = true;
		else {
			const w = rowWavelength(m);
			if (!w || (wl.min !== null && w[1] < wl.min) || (wl.max !== null && w[0] > wl.max)) return 'fail';
		}
	}
	return exempt ? 'exempt' : 'hit';
}

export interface Cell {
	rep: Metric;
	rows: Metric[];
}
export interface PivotRow {
	c: Component;
	cells: Map<string, Cell>;
}

/** One table row per component. With row filters active a component stays only if a row passes all of them. */
export function pivot(comps: Component[], f: Filters, params: Parameters): PivotRow[] {
	const anyActive = isActive(f.basis) || isActive(f.wl);
	const out: PivotRow[] = [];
	for (const c of comps) {
		const by = new Map<string, Metric[]>();
		let hit = !anyActive;
		for (const m of c.metrics) {
			if (m.statistic === 'std') continue; // a spread is not a value of the component: panel only
			const res = anyActive ? rowPass(m, f, params) : 'hit';
			if (res === 'fail') continue;
			if (res === 'hit') hit = true;
			const k = cellKey(m);
			const l = by.get(k);
			if (l) l.push(m);
			else by.set(k, [m]);
		}
		if (!hit) continue;
		const cells = new Map<string, Cell>();
		for (const [p, rows] of by) cells.set(p, { rep: repRow(rows), rows });
		out.push({ c, cells });
	}
	return out;
}

/** What a stored row says on the number line: a value, a range, or a bound. */
export function rowNum(m: Metric): NumVal | null {
	const v = Number(m.value),
		w = m.value_max ? Number(m.value_max) : NaN;
	if (!Number.isFinite(v)) return null;
	if (Number.isFinite(w)) return [v, w];
	if (m.qualifier === 'gt' || m.qualifier === 'ge') return { lo: v, hi: Infinity, loOpen: m.qualifier === 'gt' };
	if (m.qualifier === 'lt' || m.qualifier === 'le') return { lo: -Infinity, hi: v, hiOpen: m.qualifier === 'lt' };
	return v;
}

/** Values of a cell for a range filter: every stored row of the cell. */
export function cellNums(cell: Cell | undefined): NumVal[] {
	if (!cell) return [];
	const out: NumVal[] = [];
	for (const m of cell.rows) {
		const n = rowNum(m);
		if (n !== null) out.push(n);
	}
	return out;
}

/** The row a cell shows: with a range filter active, the representative of the rows that matched it. */
export function cellRep(cell: Cell, f: Filter | undefined): Metric {
	if (!isActive(f) || f?.t !== 'num') return cell.rep;
	const hit = cell.rows.filter((m) => {
		const n = rowNum(m);
		return n !== null && inRange(n, f.min, f.max);
	});
	return hit.length ? repRow(hit) : cell.rep;
}

function sigDigits(s: string): number {
	const x = s.replace(/\.0+$/, '').replace(/^[-+]?0*/, '');
	const t = x.includes('.') ? x.replace('.', '').replace(/^0+/, '') : x.replace(/0+$/, '');
	return Math.min(Math.max(t.length, 1), 6);
}
/** The stored string where it fits; plain digits from 1e6 in exponent form with the stored precision. A value stored in
 *  exponent form stays as stored. */
const shortNum = (s: string): string => (/e/i.test(s) || Math.abs(Number(s)) < 1e6 ? s : Number(s).toExponential(sigDigits(s) - 1).replace('e+', 'e'));

/** Cell text of a stored row: qualifier, value (exponent form from 1e6), range. The stored string stays in the tooltip. */
export function cellText(m: Metric): string {
	const q = fmtValue(m).match(/^[<>=~]+ /)?.[0] ?? '';
	return q + shortNum(m.value) + (m.value_max ? '-' + shortNum(m.value_max) : '');
}

const MAX_TIP_ROWS = 14;

/** All rows behind a cell, the shown one first, one line each, with what makes them differ. */
export function cellTip(cell: Cell | undefined, shown0?: Metric): string | undefined {
	if (!cell) return undefined;
	const first = shown0 ?? cell.rep;
	const line = (m: Metric) => {
		const w = fmtWavelength(m);
		return [fmtValue(m) + ' ' + unitText(m.unit), m.basis.replace(/_/g, ' '), m.statistic, m.scope, w && (m.wavelength_nm ? w + ' nm' : w), m.polarization, m.condition, m.locator].filter(Boolean).join('; ');
	};
	const rows = [first, ...cell.rows.filter((m) => m !== first)];
	const shown = rows.slice(0, MAX_TIP_ROWS).map(line);
	if (rows.length > MAX_TIP_ROWS) shown.push(`${rows.length - MAX_TIP_ROWS} more rows in the panel`);
	return shown.join('\n');
}
