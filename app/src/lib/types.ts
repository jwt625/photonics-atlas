export interface Alias {
	alias: string;
	type: string;
	scope: string;
}
export interface Printed {
	corpus: string;
	printed: string;
	n: number;
	basis: string;
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
	name_basis: string;
	name_source: string;
	origin: string[];
	aliases: Alias[];
	rows: Record<string, number>;
	printed: Printed[];
	events: string[];
	/** per-lens counts (DevLog-010 D191): cmp_fab, cmp_fac, sup, proc, std, ppl, obs; non-zero keys only */
	lens?: Record<string, number>;
	notes: string;
}
export interface Participant {
	org: string;
	role: string;
	printed: string;
}
export interface OrgEvent {
	id: string;
	type: string;
	name: string;
	announced: string;
	effective: string;
	grade: string;
	status: string;
	basis: string;
	sources: string[];
	locator: string;
	notes: string;
	participants: Participant[];
}
export interface Coverage {
	strings: number;
	strings_mapped: number;
	rows: number;
	rows_mapped: number;
	by_basis: Record<string, number>;
}
export interface Registry {
	generated_on: string;
	counts: Record<string, number>;
	coverage: Record<string, Coverage>;
	org_types: Record<string, number>;
	sources_by_corpus: Record<string, Record<string, number>>;
	orgs: Org[];
	events: OrgEvent[];
}
