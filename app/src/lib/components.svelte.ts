import { staticUrl } from './paths';

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
	host_device_id?: string;
	platform?: string;
	core_material?: string;
	cladding?: string;
	process_name?: string;
	test_structure?: string;
	verified_on: string;
	notes?: string;
	fab_orgs: string[];
	source: { id: string; title: string; year: string; venue: string; url: string; access: string };
	metrics: Metric[];
}
/** One layout template of data/schema/component_layouts.yaml (DevLog-005 D103, D107). */
export interface LayoutTemplate {
	label: string;
	applies_to: string[];
	top: { required: string[]; optional: string[] };
	xsec: { required: string[]; optional: string[] };
	primary: { parameter: string; scope?: string; better: 'lower' | 'higher' };
}
/** One row of data/components/component_showcase.csv (D105). */
export interface ShowcaseRow {
	component_id: string;
	template: string;
	role: string;
	criterion?: string;
	rank?: string;
	rationale?: string;
	selected_on?: string;
}
export interface ComponentsView {
	generated_on: string;
	classes: Record<string, { label: string; subtypes: Record<string, string> }>;
	parameters: Record<string, { unit: string; kind: string; def: string }>;
	layouts?: Record<string, LayoutTemplate>;
	showcase?: ShowcaseRow[];
	components: Component[];
}

export const comp = $state<{ view: ComponentsView | null; error: string }>({ view: null, error: '' });
let started = false;

export async function loadComponents(): Promise<void> {
	if (started) return;
	started = true;
	try {
		const res = await fetch(staticUrl('data/components.json'));
		if (!res.ok) throw new Error(`components.json: HTTP ${res.status}`);
		comp.view = (await res.json()) as ComponentsView;
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
