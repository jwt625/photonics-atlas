// Real generated views (static/data/*.json, built by scripts/build_views.py), not synthetic fixtures.
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import type { ComponentsView } from './components.svelte';
import { decodePeople, type PeopleRaw } from './people.svelte';
import type { SupplyView } from './supply.svelte';
import type { Registry } from './types';
import { orgPublications, coverage, dateNum, descendants, orgComponents, orgPeople, orgTable, OTHER, personStats, rollup, shareByYear, split, vendors } from './views';

const load = <T>(f: string): T => JSON.parse(readFileSync(new URL(`../../static/data/${f}`, import.meta.url), 'utf-8')) as T;
const sv = load<SupplyView>('supply.json');
const pv = decodePeople(load<PeopleRaw>('people.json'));
const cv = load<ComponentsView>('components.json');
const rv = load<Registry>('registry.json');

describe('supply logic', () => {
	it('descendants follow parent links, not id prefixes', () => {
		const h1 = descendants(sv.categories, 'H1');
		expect(h1.has('H1')).toBe(true);
		expect(h1.has('H10')).toBe(false);
		const a2 = descendants(sv.categories, 'A2');
		expect([...a2].sort()).toEqual(['A2', 'A2.1', 'A2.2', 'A2.3', 'A2.4']);
	});
	it('rollup of a top level equals its usage rows; all top levels sum to the table', () => {
		const r = rollup(sv.categories, sv.usage);
		const tops = sv.categories.filter((c) => !c.parent);
		expect(tops.reduce((t, c) => t + (r.get(c.id) ?? 0), 0)).toBe(sv.usage.length);
		expect(r.get('B')).toBe(sv.usage.filter((u) => u.category_id.startsWith('B')).length);
	});
	it('vendor share by year accounts for every row of the subtree', () => {
		const ids = descendants(sv.categories, 'A');
		const s = shareByYear(sv.usage, sv.sources, ids);
		let n = s.noYear;
		for (const k of s.keys) n += (s.counts.get(k) as number[]).reduce((a, b) => a + b, 0);
		expect(n).toBe(s.total);
		expect(s.total).toBe(sv.usage.filter((u) => ids.has(u.category_id)).length);
		const own = s.keys.filter((k) => k !== OTHER);
		expect(own).toEqual([...own].sort());
		expect(own.length).toBeLessThanOrEqual(6);
		const vs = vendors(sv.usage, sv.sources, ids);
		expect(vs.reduce((t, v) => t + v.rows, 0)).toBe(s.total);
	});
});

describe('people logic', () => {
	it('decodes column arrays; every observation belongs to its person', () => {
		expect(pv.persons.length).toBe(pv.counts.persons_public);
		expect(pv.obs.length).toBe(pv.counts.obs_public);
		expect(pv.byPerson.reduce((t, os) => t + os.length, 0)).toBe(pv.obs.length);
		const st = personStats(pv);
		expect(st.reduce((t, s) => t + s.n, 0)).toBe(pv.obs.length);
	});
	it('org table and coverage count every public observation once', () => {
		const t = orgTable(pv);
		expect([...t.values()].reduce((a, b) => a + b.obs, 0)).toBe(pv.obs.filter((o) => o.org_id).length);
		const c = coverage(pv.obs, pv.sources);
		expect([...c.byYear.values()].flat().reduce((a, b) => a + b, 0)).toBe(pv.obs.length);
		expect([...c.byGrade.values()].reduce((a, b) => a + b, 0)).toBe(pv.obs.length);
		for (const [k, v] of Object.entries(pv.totals_by_type)) {
			expect((c.byYear.get(k) ?? []).reduce((a, b) => a + b, 0)).toBe(v.public);
		}
	});
	it('org people match the org table', () => {
		const t = orgTable(pv);
		const [org, n] = [...t].sort((a, b) => b[1].persons - a[1].persons)[0];
		const op = orgPeople(pv, org);
		expect(op.length).toBe(n.persons);
		expect(op.reduce((a, b) => a + b.n, 0)).toBe(n.obs);
	});
	it('dates: year-only at mid-year, full dates in order', () => {
		expect(dateNum('2024')).toBe(2024.5);
		expect(dateNum('2024-03-01')).toBeLessThan(dateNum('2024-03-20'));
	});
});

describe('org hub logic', () => {
	it('components by fab / facility org id', () => {
		const want = cv.components.filter((c) => split(c.fab_org_ids).includes('org_imec') || split(c.facility_org_ids).includes('org_imec')).length;
		expect(want).toBeGreaterThan(0);
		expect(orgComponents(cv.components, 'org_imec').length).toBe(want);
	});
	it('publication records carry title and type, never access or corpus fields', () => {
		for (const p of [...Object.values(sv.sources), ...Object.values(pv.sources), ...cv.components.map((c) => c.source)]) {
			expect(Object.keys(p).every((k) => ['title', 'venue', 'year', 'type', 'url', 'doi', 'arxiv', 'atlas'].includes(k))).toBe(true);
		}
	});
	it('hub publication list equals the publication lens count of /orgs for every org (D199t)', () => {
		const bad = rv.orgs.filter((o) => orgPublications(o.id, rv, cv.components, sv, pv).length !== (o.lens?.pub ?? 0));
		expect(bad.map((o) => [o.id, o.lens?.pub ?? 0, orgPublications(o.id, rv, cv.components, sv, pv).length])).toEqual([]);
	});
});
