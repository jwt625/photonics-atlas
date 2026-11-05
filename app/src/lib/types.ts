import type { Pub } from './pub';

export interface Alias {
	alias: string;
	type: string;
}
export interface Org {
	id: string;
	name: string;
	type: string;
	country: string;
	parent: string;
	children: string[];
	status: string;
	founded: string;
	dissolved: string;
	ror: string;
	qid: string;
	website: string;
	aliases: Alias[];
	/** names as printed in publications (other than the org name) */
	printed: string[];
	/** [site name, href] of the org in a sibling atlas */
	links: [string, string][];
	events: string[];
	/** per-lens counts: cmp_fab, cmp_fac, sup, proc, std, ppl, obs, pub; non-zero keys only */
	lens?: Record<string, number>;
}
export interface Participant {
	org: string;
	role: string;
}
export interface OrgEvent {
	id: string;
	type: string;
	name: string;
	announced: string;
	effective: string;
	/** source ids (join keys into Registry.sources) */
	sources: string[];
	participants: Participant[];
}
/** Home-page overview computed by build_views.py (D199l). */
export interface Overview {
	components: { n: number; classes: number; class_families: number; platforms: number; publications: number; years: number[] };
	values: { n: number; measured: number };
	orgs: { n: number; by_type: Record<string, number> };
	people: { persons: number; affiliations: number; publications: number };
	supply: { usage: number; vendors: number; products: number; processes: number; tests: number; standards: number };
	top_fabs: [string, number][];
	top_vendors: [string, number][];
	publications: { n: number; years: number[]; by_type: Record<string, number[]>; no_year: number };
}
/** Real first rows of the tables in their default order, inlined in every page (DevLog-013 D500). */
export interface Head {
	components: {
		total: number;
		rows: { component_id: string; class: string; label: string; platform?: string; core_material?: string; fab_orgs?: string[]; nv: number; source?: Pub }[];
		/** [family, label, [subtype, components][]] */
		tree: [string, string, [string, number][]][];
	};
	orgs: { total: number; rows: (Pick<Org, 'id' | 'name'> & Partial<Pick<Org, 'type' | 'country' | 'status' | 'lens'>>)[] };
	people: { total: number; rows: { id: string; name: string; lin?: string; n?: number; first?: string; last?: string; orgs?: number }[] };
	supply: {
		vendors: number;
		usage: number;
		rows: { org: string; name: string; type?: string; country?: string; rows: number; sources: number; roles: string[]; cats: string[]; y0?: number; y1?: number }[];
		/** [id, label, parent, stated uses in the subtree][] */
		categories: [string, string, string, number][];
	};
}
/** parts/summary.json of app/scripts/shard-data.mjs */
export interface Summary {
	generated_on: string;
	overview: Overview;
	/** names of the organizations in overview.top_fabs and overview.top_vendors */
	names: Record<string, string>;
	parts: { components: number; people: number };
	head: Head;
}
export interface Registry {
	generated_on: string;
	counts: Record<string, number>;
	org_types: Record<string, number>;
	overview: Overview;
	orgs: Org[];
	events: OrgEvent[];
	sources: Record<string, Pub>;
}
