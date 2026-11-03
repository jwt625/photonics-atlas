import { getJson } from './paths';
import type { Pub } from './pub';

export interface Metric {
	metric_id: string;
	parameter: string;
	value: string;
	value_max?: string;
	unit: string;
	qualifier?: string;
	statistic?: string;
	n_samples?: string;
	wavelength_nm?: string;
	wavelength_max_nm?: string;
	band?: string;
	polarization?: string;
	mode?: string;
	temperature_k?: string;
	bias_v?: string;
	ref_plane?: string;
	scope?: string;
	includes?: string;
	excludes?: string;
	condition?: string;
	method?: string;
	basis: string;
	locator: string;
	notes?: string;
}
export interface Component {
	component_id: string;
	source_id: string;
	class: string;
	label: string;
	row_kind: string;
	platform?: string;
	core_material?: string;
	cladding?: string;
	process_name?: string;
	test_structure?: string;
	notes?: string;
	fab_orgs: string[];
	/** registry org ids, `;`-separated, as in components.csv (present only when non-empty) */
	fab_org_ids?: string;
	facility_org_ids?: string;
	source: Pub;
	metrics: Metric[];
}
/** Primary metric spec of a layout template (D107). */
export interface PrimarySpec {
	parameter: string;
	scope?: string;
	better: 'lower' | 'higher';
}
/** One layout template of data/schema/component_layouts.yaml (DevLog-005 D103, D107). */
export interface LayoutTemplate {
	label: string;
	applies_to: string[];
	top: { required: string[]; optional: string[] };
	xsec: { required: string[]; optional: string[] };
	primary: PrimarySpec;
	/** Class-specific primary overriding `primary` (DevLog-007 D164 / D251; DevLog-005 D229a). */
	primary_by_class?: Record<string, PrimarySpec>;
	/** Platform-qualified showcase gaps (D112, D223): role + platform family key of explore/colors.ts. */
	gaps?: { role: string; platform_family: string }[];
}
/** One row of data/components/component_showcase.csv (D105). */
export interface ShowcaseRow {
	component_id: string;
	template: string;
	role: string;
	criterion?: string;
	rank?: string;
	rationale?: string;
}
export interface ComponentsView {
	generated_on: string;
	classes: Record<string, { label: string; subtypes: Record<string, string> }>;
	parameters: Record<string, { unit: string; kind: string; def: string }>;
	layouts?: Record<string, LayoutTemplate>;
	showcase?: ShowcaseRow[];
	components: Component[];
}

/** components/meta.json of app/scripts/shard-data.mjs */
export type ComponentsMeta = Omit<ComponentsView, 'components'> & { parts: number; total: number; showcase_components: Component[] };

// raw state: views are replaced as a whole, never mutated (no deep proxies over thousands of rows)
class ComponentsState {
	/** Everything, in canonical order. Null until the last part has arrived: counts and joins read only this. */
	view = $state.raw<ComponentsView | null>(null);
	/** Grows part by part, in class order, for pages that can show rows as they arrive. */
	partial = $state.raw<ComponentsView | null>(null);
	/** Registries and the showcase components only. */
	early = $state.raw<ComponentsView | null>(null);
	error = $state('');
}
export const comp = new ComponentsState();
let started = false;

/** a table re-sorts on every publish: at most one per this many ms, however fast the parts arrive */
const PUBLISH_MS = 150;

export async function loadComponents(): Promise<void> {
	if (started) return;
	started = true;
	try {
		const { parts, total, showcase_components, ...meta } = await getJson<ComponentsMeta>('data/parts/components/meta.json');
		comp.early = { ...meta, components: showcase_components };
		const pending = Array.from({ length: parts }, (_, i) => getJson<Component[]>(`data/parts/components/${i}.json`));
		pending.forEach((p) => p.catch(() => {})); // the first failure is reported below, in order
		const got: Component[] = [];
		let published = 0;
		for (const p of pending) {
			got.push(...(await p));
			if (performance.now() - published > PUBLISH_MS) {
				comp.partial = { ...meta, components: got.slice() };
				published = performance.now();
				await new Promise((r) => setTimeout(r, 0));
			}
		}
		if (got.length !== total) throw new Error(`components: ${got.length} of ${total} received; the site was updated during this load, please reload`);
		got.sort((a, b) => (a.component_id < b.component_id ? -1 : 1)); // canonical order of build_views.py
		comp.view = { ...meta, components: got };
		comp.partial = comp.view;
	} catch (e) {
		comp.error = e instanceof Error ? e.message : String(e);
	}
}

const QSYM: Record<string, string> = { lt: '<', gt: '>', le: '<=', ge: '>=', approx: '~' };

/** "~0.2", "> 40", "1.0-1.4": the stored value with its qualifier and range. */
export function fmtValue(m: Metric): string {
	const q = m.qualifier ? QSYM[m.qualifier] + ' ' : '';
	return q + m.value + (m.value_max ? '-' + m.value_max : '');
}

export function fmtWavelength(m: Metric): string {
	if (m.wavelength_nm) return m.wavelength_nm + (m.wavelength_max_nm ? '-' + m.wavelength_max_nm : '');
	return m.band ?? '';
}
