// Pure logic of the supply, people and org-hub views (DevLog-010 D190-D198).
import type { Component } from './components.svelte';
import type { Obs, PeopleView, Person } from './people.svelte';
import type { SrcMeta, SupplyCategory, Usage } from './supply.svelte';

export const OTHER = 'other';

// ---------- supply ----------

/** The category and all nodes below it, following parent links (ids like H1 / H10 are siblings, not prefixes). */
export function descendants(cats: SupplyCategory[], id: string): Set<string> {
	const kids = new Map<string, string[]>();
	for (const c of cats) if (c.parent) kids.set(c.parent, [...(kids.get(c.parent) ?? []), c.id]);
	const out = new Set<string>();
	const stack = [id];
	while (stack.length) {
		const x = stack.pop() as string;
		if (out.has(x)) continue;
		out.add(x);
		stack.push(...(kids.get(x) ?? []));
	}
	return out;
}

/** Usage rows per category, rolled up over each node's subtree. */
export function rollup(cats: SupplyCategory[], usage: Usage[]): Map<string, number> {
	const own = new Map<string, number>();
	for (const u of usage) own.set(u.category_id, (own.get(u.category_id) ?? 0) + 1);
	const out = new Map<string, number>();
	for (const c of cats) {
		let n = 0;
		for (const d of descendants(cats, c.id)) n += own.get(d) ?? 0;
		out.set(c.id, n);
	}
	return out;
}

export function yearOf(sources: Record<string, SrcMeta>, sid: string): number | null {
	const y = Number(sources[sid]?.year);
	return Number.isFinite(y) && y > 0 ? y : null;
}

export interface VendorRow {
	org: string;
	rows: number;
	sources: number;
	roles: string[];
	cats: string[];
	y0: number | null;
	y1: number | null;
}

/** Vendors (orgs) with usage rows in the category set, most rows first, ties by org id. */
export function vendors(usage: Usage[], sources: Record<string, SrcMeta>, ids: Set<string> | null): VendorRow[] {
	const m = new Map<string, { rows: number; src: Set<string>; roles: Set<string>; cats: Set<string>; ys: number[] }>();
	for (const u of usage) {
		if (ids && !ids.has(u.category_id)) continue;
		const v = m.get(u.org_id) ?? { rows: 0, src: new Set(), roles: new Set(), cats: new Set(), ys: [] };
		v.rows++;
		v.src.add(u.source_id);
		v.roles.add(u.role);
		v.cats.add(u.category_id);
		const y = yearOf(sources, u.source_id);
		if (y !== null) v.ys.push(y);
		m.set(u.org_id, v);
	}
	return [...m]
		.map(([org, v]) => ({
			org,
			rows: v.rows,
			sources: v.src.size,
			roles: [...v.roles].sort(),
			cats: [...v.cats].sort(),
			y0: v.ys.length ? Math.min(...v.ys) : null,
			y1: v.ys.length ? Math.max(...v.ys) : null
		}))
		.sort((a, b) => b.rows - a.rows || a.org.localeCompare(b.org));
}

export interface Share {
	years: number[];
	/** vendor org ids with their own colour slot (alphabetical by id; D194), then OTHER when any row falls outside */
	keys: string[];
	counts: Map<string, number[]>;
	noYear: number;
	total: number;
}

/** Usage rows per source year and vendor within the category set (D194). The `slots` vendors with most rows get their
 *  own series, ordered by org id (colour = identity, never rank); the rest fold into OTHER. */
export function shareByYear(usage: Usage[], sources: Record<string, SrcMeta>, ids: Set<string> | null, slots = 6): Share {
	const rows = usage.filter((u) => !ids || ids.has(u.category_id));
	const vs = vendors(rows, sources, null);
	const top = vs.slice(0, slots).map((v) => v.org).sort();
	const keys = vs.length > slots ? [...top, OTHER] : top;
	const yrs = rows.map((u) => yearOf(sources, u.source_id)).filter((y): y is number => y !== null);
	const years: number[] = [];
	if (yrs.length) for (let y = Math.min(...yrs); y <= Math.max(...yrs); y++) years.push(y);
	const counts = new Map(keys.map((k) => [k, years.map(() => 0)]));
	let noYear = 0;
	for (const u of rows) {
		const y = yearOf(sources, u.source_id);
		if (y === null) {
			noYear++;
			continue;
		}
		const k = top.includes(u.org_id) ? u.org_id : OTHER;
		(counts.get(k) as number[])[y - years[0]]++;
	}
	return { years, keys, counts, noYear, total: rows.length };
}

// ---------- people ----------

/** Fractional year of an ISO date (YYYY at mid-year; YYYY-MM at mid-month; YYYY-MM-DD exact enough for a plot). */
export function dateNum(d: string): number {
	const [y, m, day] = d.split('-').map(Number);
	if (!m) return y + 0.5;
	if (!day) return y + (m - 0.5) / 12;
	return y + (m - 1) / 12 + (day - 1) / 365;
}

export interface PersonStat {
	n: number;
	first: string;
	last: string;
	orgs: number;
	/** orgs of the person's latest observation date (several when one source prints several) */
	lastOrgs: string[];
}

export function personStats(v: PeopleView): PersonStat[] {
	return v.byPerson.map((os) => {
		if (!os.length) return { n: 0, first: '', last: '', orgs: 0, lastOrgs: [] };
		const ds = os.map((o) => o.active_on);
		const first = ds.reduce((a, b) => (dateNum(b) < dateNum(a) ? b : a));
		const last = ds.reduce((a, b) => (dateNum(b) > dateNum(a) ? b : a));
		const orgKey = (o: Obs) => o.org_id || 'printed:' + o.printed_org;
		return {
			n: os.length,
			first,
			last,
			orgs: new Set(os.map(orgKey)).size,
			lastOrgs: [...new Set(os.filter((o) => o.active_on === last).map(orgKey))]
		};
	});
}

export interface OrgPerson {
	person: Person;
	n: number;
	first: string;
	last: string;
}

/** Public persons with public observations at the org, most observations first, ties by name. */
export function orgPeople(v: PeopleView, orgId: string): OrgPerson[] {
	const m = new Map<number, Obs[]>();
	for (const o of v.obs) if (o.org_id === orgId) m.set(o.p, [...(m.get(o.p) ?? []), o]);
	return [...m]
		.map(([p, os]) => {
			const ds = os.map((o) => o.active_on).sort((a, b) => dateNum(a) - dateNum(b));
			return { person: v.persons[p], n: os.length, first: ds[0], last: ds[ds.length - 1] };
		})
		.sort((a, b) => b.n - a.n || a.person.name.localeCompare(b.person.name));
}

/** Org id -> distinct public persons and public observations (observations without an org id are skipped). */
export function orgTable(v: PeopleView): Map<string, { persons: number; obs: number }> {
	const ps = new Map<string, Set<number>>();
	const ns = new Map<string, number>();
	for (const o of v.obs) {
		if (!o.org_id) continue;
		if (!ps.has(o.org_id)) ps.set(o.org_id, new Set());
		(ps.get(o.org_id) as Set<number>).add(o.p);
		ns.set(o.org_id, (ns.get(o.org_id) ?? 0) + 1);
	}
	return new Map([...ps].map(([k, s]) => [k, { persons: s.size, obs: ns.get(k) ?? 0 }]));
}

export const corpusOf = (sid: string): string => sid.split(':', 1)[0];

export interface Coverage {
	corpora: string[];
	years: number[];
	/** corpus -> counts per year (aligned with years) */
	byYear: Map<string, number[]>;
	/** `${corpus}|${grade}` -> count */
	byGrade: Map<string, number>;
	grades: string[];
}

export function coverage(obs: Obs[]): Coverage {
	const corpora = [...new Set(obs.map((o) => corpusOf(o.source_id)))].sort();
	const grades = [...new Set(obs.map((o) => o.grade))].sort();
	const ys = obs.map((o) => Number(o.active_on.slice(0, 4)));
	const years: number[] = [];
	if (ys.length) for (let y = Math.min(...ys); y <= Math.max(...ys); y++) years.push(y);
	const byYear = new Map(corpora.map((c) => [c, years.map(() => 0)]));
	const byGrade = new Map<string, number>();
	obs.forEach((o, i) => {
		const c = corpusOf(o.source_id);
		(byYear.get(c) as number[])[ys[i] - years[0]]++;
		byGrade.set(`${c}|${o.grade}`, (byGrade.get(`${c}|${o.grade}`) ?? 0) + 1);
	});
	return { corpora, years, byYear, byGrade, grades };
}

// ---------- org hub ----------

export const split = (s: string | undefined): string[] => (s ?? '').split(';').map((x) => x.trim()).filter(Boolean);

export interface OrgComponent {
	c: Component;
	fab: boolean;
	fac: boolean;
}

/** Components whose source states the org fabricated them (fab_org_ids) or hosted the work (facility_org_ids). */
export function orgComponents(comps: Component[], orgId: string): OrgComponent[] {
	const out: OrgComponent[] = [];
	for (const c of comps) {
		const fab = split(c.fab_org_ids).includes(orgId);
		const fac = split(c.facility_org_ids).includes(orgId);
		if (fab || fac) out.push({ c, fab, fac });
	}
	return out.sort((a, b) => a.c.class.localeCompare(b.c.class) || a.c.component_id.localeCompare(b.c.component_id));
}

// Sibling atlas sites (D198): both read their filters from the URL hash.
export const EO_SITE = 'https://outside5sigma.com/eo-modulator-atlas';
export const PK_SITE = 'https://outside5sigma.com/advanced-packaging-atlas';

/** EO table search (token AND over paper fields incl. org names). */
export const eoSearch = (q: string): string => `${EO_SITE}/table#q=${encodeURIComponent(q)}`;
/** Packaging table filtered to one canonical PK org name. */
export const pkOrg = (name: string): string => `${PK_SITE}/table#o=${encodeURIComponent(name)}`;

/** Sibling-atlas page of an `eo:` / `pk:` source (table searched by its paper id); null for other corpora. */
export function siblingPaper(sid: string): { href: string; site: string } | null {
	const [c, id] = [corpusOf(sid), sid.slice(sid.indexOf(':') + 1)];
	if (c === 'eo') return { href: eoSearch(id), site: 'EO atlas' };
	if (c === 'pk') return { href: `${PK_SITE}/table#q=${encodeURIComponent(id)}`, site: 'packaging atlas' };
	return null;
}
