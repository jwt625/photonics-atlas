// Supply-chain view (static/data/supply.json, DevLog-010 D191): DevLog-003 tables as generated, non-empty fields only.
import { staticUrl } from './paths';
import type { Pub } from './pub';

export interface SupplyCategory {
	id: string;
	label: string;
	parent?: string;
}
/** One product_usage row (D53): the source states the org was used in that role for the reported work. */
export interface Usage {
	usage_id: string;
	source_id: string;
	org_id: string;
	product_id?: string;
	category_id: string;
	role: string;
	stated_spec?: string;
	locator: string;
	basis: string;
}
export type Row = Record<string, string>;
export type SrcMeta = Pub;
export interface SupplyView {
	generated_on: string;
	categories: SupplyCategory[];
	usage: Usage[];
	processes: Row[];
	standards: Row[];
	tests: Row[];
	products: Row[];
	specs: Row[];
	sources: Record<string, SrcMeta>;
}

// raw state: the view is replaced as a whole, never mutated (no deep proxies over thousands of rows)
class SupplyViewState {
	view = $state.raw<SupplyView | null>(null);
	error = $state('');
}
export const sup = new SupplyViewState();
let started = false;

export async function loadSupply(): Promise<void> {
	if (started) return;
	started = true;
	try {
		const res = await fetch(staticUrl('data/supply.json'));
		if (!res.ok) throw new Error(`supply.json: HTTP ${res.status}`);
		sup.view = (await res.json()) as SupplyView;
	} catch (e) {
		sup.error = e instanceof Error ? e.message : String(e);
	}
}
