// People view (static/data/people.json, DevLog-010 D191, D192): public persons and public observations only.
import { staticUrl } from './paths';
import type { SrcMeta } from './supply.svelte';

export interface Person {
	id: string;
	name: string;
	orcid: string;
	disambiguator: string;
	/** lineage (LIN) record grade and `;`-separated LIN source ids (D199d); empty without a LIN record or in views built
	 *  before 2026-10-23 */
	lin_grade?: string;
	lin_sources: string;
	/** index in PeopleView.persons */
	i: number;
}
/** One public affiliation observation (DevLog-004 D67): a dated point, never an interval. */
export interface Obs {
	obs_id: string;
	p: number;
	printed_name: string;
	org_id: string;
	printed_org: string;
	unit: string;
	country: string;
	kind: string;
	aff_role: string;
	active_on: string;
	source_id: string;
	locator: string;
	grade: string;
}
export interface PeopleRaw {
	generated_on: string;
	counts: Record<string, number>;
	totals_by_corpus: Record<string, { all: number; public: number }>;
	person_fields: string[];
	persons: (string | number)[][];
	obs_fields: string[];
	obs: (string | number)[][];
	sources: Record<string, SrcMeta>;
}
export interface PeopleView {
	generated_on: string;
	counts: Record<string, number>;
	totals_by_corpus: Record<string, { all: number; public: number }>;
	persons: Person[];
	obs: Obs[];
	/** observations per person index, in (active_on, obs_id) order */
	byPerson: Obs[][];
	sources: Record<string, SrcMeta>;
}

function rows<T>(fields: string[], data: (string | number)[][]): T[] {
	return data.map((r) => Object.fromEntries(fields.map((f, i) => [f, r[i]])) as T);
}

export function decodePeople(raw: PeopleRaw): PeopleView {
	const persons = rows<Omit<Person, 'i'>>(raw.person_fields, raw.persons).map((p, i) => ({ ...p, lin_sources: p.lin_sources ?? '', i }));
	const obs = rows<Obs>(raw.obs_fields, raw.obs);
	const byPerson: Obs[][] = persons.map(() => []);
	for (const o of obs) byPerson[o.p].push(o);
	return { generated_on: raw.generated_on, counts: raw.counts, totals_by_corpus: raw.totals_by_corpus, persons, obs, byPerson, sources: raw.sources };
}

// raw state: the view is replaced as a whole, never mutated (no deep proxies over thousands of rows)
class PeopleViewState {
	view = $state.raw<PeopleView | null>(null);
	error = $state('');
}
export const ppl = new PeopleViewState();
let started = false;

export async function loadPeople(): Promise<void> {
	if (started) return;
	started = true;
	try {
		const res = await fetch(staticUrl('data/people.json'));
		if (!res.ok) throw new Error(`people.json: HTTP ${res.status}`);
		ppl.view = decodePeople((await res.json()) as PeopleRaw);
	} catch (e) {
		ppl.error = e instanceof Error ? e.message : String(e);
	}
}
