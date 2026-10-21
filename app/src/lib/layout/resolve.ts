// Geometry resolver for the layout viewer (DevLog-005 D102-D107). For a component: pick the layout template served by
// its class, resolve every template dimension to one metric row (deterministic pick, alternatives exposed), and mark
// the dimensions the source does not report. Labels are the stored value strings plus unit: no number is computed.
import { fmtValue, type Component, type ComponentsView, type LayoutTemplate, type Metric } from '../components.svelte';

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
	dc: ['imbalance_db'],
	awg: ['crosstalk_adjacent_db'],
	ge_pd: ['bw3db_ghz'],
	ridge_laser: ['linewidth_hz']
};

export interface Primary {
	param: string;
	row: Metric | null;
	n: number;
	/** false when no row has the template scope and the best row of another scope is shown (scope printed). */
	scopeMatch: boolean;
	companions: { param: string; row: Metric }[];
}

/** Best value of the template's primary metric (scope as the template states; measured rows preferred over others,
 *  then better value, then metric id). ridge_laser falls back from output_power_mw to output_power_dbm. */
export function primaryMetric(c: Component, templateId: string, t: LayoutTemplate): Primary {
	const params = templateId === 'ridge_laser' ? [t.primary.parameter, 'output_power_dbm'] : [t.primary.parameter];
	for (const [p, strict] of [...params.map((q) => [q, true] as const), ...(t.primary.scope ? params.map((q) => [q, false] as const) : [])]) {
		const rows = c.metrics.filter((m) => m.parameter === p && (!strict || !t.primary.scope || m.scope === t.primary.scope) && Number.isFinite(Number(m.value)) && m.statistic !== 'std');
		if (!rows.length) continue;
		const sgn = t.primary.better === 'lower' ? 1 : -1;
		rows.sort((a, b) => (a.basis === 'measured' ? 0 : 1) - (b.basis === 'measured' ? 0 : 1) || sgn * (Number(a.value) - Number(b.value)) || metricOrder(a.metric_id) - metricOrder(b.metric_id));
		const companions = (COMPANION[templateId] ?? []).flatMap((q) => {
			const r = pickOrder(c.metrics.filter((m) => m.parameter === q && m.statistic !== 'std')).sort((a, b) => (a.basis === 'measured' ? 0 : 1) - (b.basis === 'measured' ? 0 : 1));
			return r.length ? [{ param: q, row: r[0] }] : [];
		});
		return { param: p, row: rows[0], n: rows.length, scopeMatch: strict || !t.primary.scope, companions };
	}
	return { param: t.primary.parameter, row: null, n: 0, scopeMatch: true, companions: [] };
}
