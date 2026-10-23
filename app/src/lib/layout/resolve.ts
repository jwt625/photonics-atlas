// Geometry resolver for the layout viewer (DevLog-005 D102-D107). For a component: pick the layout template served by
// its class, resolve every template dimension to one metric row (deterministic pick, alternatives exposed), and mark
// the dimensions the source does not report. Labels are the stored value strings plus unit: no number is computed.
import { fmtValue, type Component, type ComponentsView, type LayoutTemplate, type Metric, type PrimarySpec } from '../components.svelte';

export type View = 'top' | 'xsec';
export type BasisKind = 'design' | 'measured' | 'figure' | 'spec' | 'derived' | 'estimate' | 'simulated' | 'other';

export const BASIS: Record<string, { kind: BasisKind; badge: string; rank: number }> = {
	design_target: { kind: 'design', badge: 'D', rank: 0 },
	measured: { kind: 'measured', badge: 'M', rank: 1 },
	extracted_from_figure: { kind: 'figure', badge: 'F', rank: 2 },
	specification: { kind: 'spec', badge: 'P', rank: 3 },
	derived: { kind: 'derived', badge: 'R', rank: 4 },
	author_estimate: { kind: 'estimate', badge: 'E', rank: 5 },
	simulated: { kind: 'simulated', badge: 'S', rank: 6 }
};
export const BASIS_LEGEND: [string, string][] = [
	['D', 'design target'],
	['M', 'measured (SEM / AFM / profilometer)'],
	['F', 'labelled in a source figure'],
	['P', 'specification'],
	['R', 'derived'],
	['E', 'author estimate'],
	['S', 'simulated']
];

export interface Dim {
	param: string;
	views: View[];
	required: boolean;
	/** The row drawn; null when the source does not report the dimension. */
	row: Metric | null;
	/** Other rows of the same parameter, in pick order (never drawn; listed on hover and in the table). */
	alts: Metric[];
	/** Drawing value: lengths in um, counts / angles / ratios as stored; a range is drawn at its midpoint. */
	num: number | null;
	unit: string;
	/** Visible label: the stored value string (qualifier, range) with its unit, or "not reported". */
	label: string;
	basis: BasisKind | null;
	badge: string;
	tip: string;
}

export interface Resolved {
	templateId: string;
	template: LayoutTemplate;
	comp: Component;
	dims: Record<string, Dim>;
	missingRequired: string[];
	missingOptional: string[];
	reported: number;
	total: number;
}

const UNIT_DISPLAY: Record<string, string> = { um: 'µm', um2: 'µm²', deg: '°', count: '', '1': '' };
const TO_UM: Record<string, number> = { nm: 1e-3, um: 1, mm: 1e3, cm: 1e4 };

export function unitLabel(u: string): string {
	return UNIT_DISPLAY[u] ?? u;
}

/** Template id serving a component class, or null. */
export function templateFor(cls: string, layouts: Record<string, LayoutTemplate> | undefined): string | null {
	for (const [id, t] of Object.entries(layouts ?? {})) if (t.applies_to.includes(cls)) return id;
	return null;
}

function metricOrder(id: string): number {
	const m = /-m(\d+)$/.exec(id);
	return m ? Number(m[1]) : 1e9;
}

/** Pick order: drawable (not a spread statistic) first, then basis rank (design before measured), rows without a
 *  condition, rows without a qualifier, then metric id. Deterministic for a given table. */
export function pickOrder(rows: Metric[]): Metric[] {
	const key = (m: Metric): number[] => [
		m.statistic === 'std' || !Number.isFinite(Number(m.value)) ? 1 : 0,
		BASIS[m.basis]?.rank ?? 9,
		m.condition ? 1 : 0,
		m.qualifier ? 1 : 0,
		metricOrder(m.metric_id)
	];
	return [...rows].sort((a, b) => {
		const x = key(a), y = key(b);
		for (let i = 0; i < x.length; i++) if (x[i] !== y[i]) return x[i] - y[i];
		return a.metric_id < b.metric_id ? -1 : a.metric_id > b.metric_id ? 1 : 0;
	});
}

/** Drawable rows of a parameter that differ by condition (e.g. taper sections s1, s2, s3), in metric-id order; empty
 *  unless there are at least two. They are drawn as consecutive segments, each with its own label (never summed). */
export function segmentRows(c: Component, param: string): Metric[] {
	const rows = c.metrics.filter((m) => m.parameter === param && m.statistic !== 'std' && Number.isFinite(Number(m.value)) && m.condition);
	const conds = new Set(rows.map((m) => m.condition));
	if (rows.length < 2 || conds.size !== rows.length || new Set(rows.map((m) => m.basis)).size !== 1) return [];
	return rows.sort((a, b) => metricOrder(a.metric_id) - metricOrder(b.metric_id));
}

export function rowLabel(m: Metric): string {
	const u = unitLabel(m.unit);
	return fmtValue(m) + (u ? ' ' + u : '');
}

function rowTip(m: Metric): string {
	return [
		`${rowLabel(m)}  [${m.basis}${m.statistic ? ', ' + m.statistic : ''}${m.n_samples ? ' n=' + m.n_samples : ''}]`,
		m.condition && 'condition: ' + m.condition,
		'locator: ' + m.locator,
		m.notes && 'notes: ' + m.notes
	]
		.filter(Boolean)
		.join('\n');
}

function drawValue(m: Metric): number | null {
	const v = Number(m.value);
	if (m.statistic === 'std' || !Number.isFinite(v)) return null;
	const vm = m.value_max !== undefined ? Number(m.value_max) : NaN;
	const n = Number.isFinite(vm) ? (v + vm) / 2 : v;
	return n * (TO_UM[m.unit] ?? 1);
}

/** Resolve one parameter; `force` draws that specific row (segments of a multi-row dimension). */
export function resolveDim(c: Component, param: string, views: View[], required: boolean, def = '', force?: Metric): Dim {
	const rows = pickOrder(c.metrics.filter((m) => m.parameter === param));
	const row = force ?? (rows.length && drawValue(rows[0]) !== null ? rows[0] : null);
	const alts = row ? rows.filter((m) => m !== row) : rows;
	const head = param + (def ? ' - ' + def : '') + (required ? '' : ' (optional)');
	if (!row) {
		return {
			param, views, required, row: null, alts, num: null, unit: '', label: 'not reported', basis: null, badge: '',
			tip: [head, 'not reported by the source: drawn schematically, proportion fixed by the template', ...alts.map((a) => 'not drawable: ' + rowTip(a))].join('\n')
		};
	}
	const b = BASIS[row.basis];
	const range = row.value_max !== undefined ? '\ndrawn at the midpoint of the range' : '';
	const bound = row.qualifier === 'lt' || row.qualifier === 'gt' || row.qualifier === 'le' || row.qualifier === 'ge' ? '\nbound: drawn at the bound' : '';
	const alt = alts.length ? `\n${alts.length} other row${alts.length > 1 ? 's' : ''} (not drawn):\n` + alts.map((a) => '  ' + rowTip(a).replace(/\n/g, '\n  ')).join('\n') : '';
	return {
		param, views, required, row, alts, num: drawValue(row), unit: row.unit, label: rowLabel(row),
		basis: b?.kind ?? 'other', badge: b?.badge ?? '?',
		tip: head + '\n' + rowTip(row) + range + bound + alt
	};
}

/** Resolve all dimensions of the component's template; null when no template serves its class. */
export function resolve(c: Component, view: ComponentsView): Resolved | null {
	const id = templateFor(c.class, view.layouts);
	if (!id || !view.layouts) return null;
	const t = view.layouts[id];
	const params = new Map<string, { views: View[]; required: boolean }>();
	for (const v of ['top', 'xsec'] as const) {
		for (const [list, req] of [[t[v].required, true], [t[v].optional, false]] as const) {
			for (const p of list) {
				const e = params.get(p) ?? { views: [], required: false };
				if (!e.views.includes(v)) e.views.push(v);
				e.required ||= req;
				params.set(p, e);
			}
		}
	}
	const dims: Record<string, Dim> = {};
	for (const [p, e] of params) dims[p] = resolveDim(c, p, e.views, e.required, view.parameters[p]?.def ?? '');
	const all = Object.values(dims);
	return {
		templateId: id,
		template: t,
		comp: c,
		dims,
		missingRequired: all.filter((d) => d.required && !d.row).map((d) => d.param),
		missingOptional: all.filter((d) => !d.required && !d.row).map((d) => d.param),
		reported: all.filter((d) => d.row).length,
		total: all.length
	};
}

/** D107 companions shown next to the primary metric. */
const COMPANION: Record<string, string[]> = {
	dc: ['imbalance_db', 'split_ratio_pct'],
	awg: ['crosstalk_adjacent_db'],
	ge_pd: ['bw3db_ghz'],
	ridge_laser: ['linewidth_hz']
};

/** Primary metric spec of a component (D229a): the template's class-specific `primary_by_class` entry, else `primary`. */
export function primaryFor(cls: string, t: LayoutTemplate): PrimarySpec {
	return t.primary_by_class?.[cls] ?? t.primary;
}

export interface Primary {
	/** spec used for this component (primaryFor) */
	spec: PrimarySpec;
	param: string;
	row: Metric | null;
	n: number;
	/** false when no row has the template scope and the best row of another scope is shown (scope printed). */
	scopeMatch: boolean;
	companions: { param: string; row: Metric }[];
}

/** Best value of the component's primary metric (primaryFor: class override, else the template primary). Passes in order (D221): measured rows with the template scope, measured
 *  rows of any scope (scope printed), rows of any basis with the template scope, then the rest; within a pass the better
 *  value, then metric id. ridge_laser falls back from output_power_mw to output_power_dbm inside each pass. */
export function primaryMetric(c: Component, templateId: string, t: LayoutTemplate): Primary {
	const spec = primaryFor(c.class, t);
	const params = templateId === 'ridge_laser' ? [spec.parameter, 'output_power_dbm'] : [spec.parameter];
	const scope = spec.scope;
	const passes: [boolean, boolean][] = scope ? [[true, true], [true, false], [false, true], [false, false]] : [[true, false], [false, false]];
	const sgn = spec.better === 'lower' ? 1 : -1;
	// companions are shown with or without a primary row (UI audit 19: a dc with a measured split but no excess loss)
	const companions = (COMPANION[templateId] ?? []).flatMap((q) => {
		const r = pickOrder(c.metrics.filter((m) => m.parameter === q && m.statistic !== 'std')).sort((a, b) => (a.basis === 'measured' ? 0 : 1) - (b.basis === 'measured' ? 0 : 1));
		return r.length ? [{ param: q, row: r[0] }] : [];
	});
	for (const [measured, strict] of passes) {
		for (const p of params) {
			const rows = c.metrics.filter(
				(m) => m.parameter === p && (!measured || m.basis === 'measured') && (!strict || m.scope === scope) && Number.isFinite(Number(m.value)) && m.statistic !== 'std'
			);
			if (!rows.length) continue;
			rows.sort((a, b) => sgn * (Number(a.value) - Number(b.value)) || metricOrder(a.metric_id) - metricOrder(b.metric_id));
			const n = c.metrics.filter((m) => m.parameter === p && Number.isFinite(Number(m.value)) && m.statistic !== 'std').length;
			return { spec, param: p, row: rows[0], n, scopeMatch: !scope || rows[0].scope === scope, companions };
		}
	}
	return { spec, param: spec.parameter, row: null, n: 0, scopeMatch: true, companions };
}

const SI_PREFIX: [number, string][] = [[1e12, 'T'], [1e9, 'G'], [1e6, 'M'], [1e3, 'k']];
const LEN_UP: Record<string, [string, number][]> = { nm: [['mm', 1e6], ['µm', 1e3]], um: [['mm', 1e3]] };

/** Significant digits of a stored number string (trailing zeros of an integer are not significant). */
function sig(s: string): number {
	// a float-formatted integer ("3500000.0", lit corpus) has no significant digits after the point (UI audit 2026-10-23 #5)
	s = s.replace(/\.0+$/, '');
	const d = s.replace(/^[-+]?0*/, '').replace('.', '');
	const t = s.includes('.') ? d.replace(/^0+/, '') : d.replace(/0+$/, '');
	return Math.min(Math.max(t.length, 1), 6);
}
function eng(s: string, k: number): string {
	const v = Number(s) / k;
	return String(Number(v.toPrecision(sig(s))));
}

/** Compact card text of a row (D224): lengths >= 1000 in the next unit (10000 nm -> 10 µm, 390000 µm -> 390 mm), Hz with
 *  an SI prefix, other values >= 1e5 in exponent form (566000000 -> 5.66e8). The stored string stays in the tooltip. */
export function compactLabel(m: Metric): string {
	const q = fmtValue(m).match(/^[<>=~]+ /)?.[0] ?? '';
	const v = Math.abs(Number(m.value));
	if (!Number.isFinite(v)) return rowLabel(m);
	const both = (f: (x: string) => string) => f(m.value) + (m.value_max ? '-' + f(m.value_max) : '');
	for (const [u, k] of LEN_UP[m.unit] ?? []) if (v >= k) return q + both((x) => eng(x, k)) + ' ' + u;
	if (m.unit === 'Hz') for (const [k, p] of SI_PREFIX) if (v >= k) return q + both((x) => eng(x, k)) + ' ' + p + 'Hz';
	if (v >= 1e5 && !(m.unit in TO_UM) && m.unit !== 'Hz') {
		const u = unitLabel(m.unit);
		return q + both((x) => Number(x).toExponential(sig(x) - 1).replace('e+', 'e')) + (u ? ' ' + u : '');
	}
	return rowLabel(m);
}

/** Basis plus statistic (median, mean, best ...) of a row, for the primary value on cards and the primary line. */
export function basisStat(m: Metric): string {
	return m.basis + (m.statistic ? ', ' + m.statistic : '');
}
