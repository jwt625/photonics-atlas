// Real generated views: the parts of app/scripts/shard-data.mjs add up to the canonical JSON, and the loaders' reassembly
// gives the same view back.
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { buildHead, buildSummary, HEAD_ROWS, MAX_PART, shardComponents, shardPeople, splitBySize } from '../../scripts/shard-data.mjs';
import type { ComponentsView } from './components.svelte';
import { gallery, templateCounts } from './layout/gallery';
import { sortOrgs } from './orgs';
import { decodePeople, type PeopleRaw } from './people.svelte';
import type { SupplyView } from './supply.svelte';
import type { Head, Registry } from './types';
import { personStats, rollup, vendors } from './views';

const load = <T>(f: string): T => JSON.parse(readFileSync(new URL(`../../static/data/${f}`, import.meta.url), 'utf-8')) as T;
const cv = load<ComponentsView>('components.json');
const pr = load<PeopleRaw>('people.json');
const rv = load<Registry>('registry.json');
const sv = load<SupplyView>('supply.json');

describe('data parts', () => {
	it('components: reassembly in loader order equals the canonical view', () => {
		const { meta, parts } = shardComponents(cv);
		expect(parts.length).toBe(meta.parts);
		const got = parts.flat();
		got.sort((a: { component_id: string }, b: { component_id: string }) => (a.component_id < b.component_id ? -1 : 1));
		const { parts: _p, total, showcase_components: _s, ...rest } = meta;
		expect(got.length).toBe(total);
		expect({ ...rest, components: got }).toEqual(cv);
	});
	it('components: parts stay small and in class order, so a class-sorted table only ever appends', () => {
		const { parts } = shardComponents(cv);
		for (const p of parts) expect(JSON.stringify(p).length).toBeLessThanOrEqual(MAX_PART + 1000);
		const classes = parts.flat().map((c: { class: string }) => c.class);
		expect(classes).toEqual([...classes].sort());
	});
	it('people: reassembly equals the canonical view', () => {
		const { meta, parts } = shardPeople(pr);
		const { parts: _p, total, ...rest } = meta;
		expect(parts.flat().length).toBe(total);
		expect({ ...rest, obs: parts.flat() }).toEqual(pr);
	});
	it('a single item larger than a part keeps its own part', () => {
		expect(splitBySize(['aaaa', 'bbbbbbbbbbbb', 'c'], 8)).toEqual([['aaaa'], ['bbbbbbbbbbbb'], ['c']]);
	});
	it('summary names every organization the dashboard lists', () => {
		const s = buildSummary(rv, 1, 1, buildHead(cv, rv, pr, sv));
		for (const [id] of [...rv.overview.top_fabs, ...rv.overview.top_vendors]) expect(s.names[id]).toBe(rv.orgs.find((o) => o.id === id)?.name);
		// inlined in every page, head rows included: 2.9 KB before DevLog-013 D500
		expect(JSON.stringify(s).length).toBeLessThan(50_000);
	});
	it('head rows are the true first rows of each table, in the default order', () => {
		const h = buildHead(cv, rv, pr, sv) as unknown as Head;
		const { parts } = shardComponents(cv);
		expect(h.components.rows.map((r) => r.component_id)).toEqual(parts[0].slice(0, HEAD_ROWS).map((c: { component_id: string }) => c.component_id));
		expect(h.components.rows[3].nv).toBe(parts[0][3].metrics.length);
		expect(h.components.tree.flatMap((t) => t[2].map((s) => s[1])).reduce((a, b) => a + b, 0)).toBe(cv.components.length);
		expect(h.orgs.rows.map((o) => o.id)).toEqual(sortOrgs(rv.orgs, 'lens.pub', 'desc').slice(0, HEAD_ROWS).map((o) => o.id));
		const pv = decodePeople(pr);
		const st = personStats(pv);
		const want = pv.persons
			.map((p, i) => ({ ...p, ...st[i] }))
			.sort((a, b) => b.n - a.n || a.name.localeCompare(b.name))
			.slice(0, HEAD_ROWS);
		for (const [i, r] of h.people.rows.entries()) {
			expect([r.id, r.n, r.first, r.last, r.orgs]).toEqual([want[i].id, want[i].n, want[i].first, want[i].last, want[i].orgs]);
		}
		const vs = vendors(sv.usage, sv.sources, null).slice(0, HEAD_ROWS);
		for (const [i, r] of h.supply.rows.entries()) {
			expect([r.org, r.rows, r.sources, r.roles, r.cats, r.y0, r.y1]).toEqual([vs[i].org, vs[i].rows, vs[i].sources, vs[i].roles, vs[i].cats, vs[i].y0, vs[i].y1]);
		}
		const roll = rollup(sv.categories, sv.usage);
		for (const [id, , , n] of h.supply.categories) expect(n).toBe(roll.get(id));
	});
	it('layout gallery from the showcase part alone equals the gallery over all components', () => {
		const { meta } = shardComponents(cv);
		const { parts: _p, total: _t, showcase_components, ...rest } = meta;
		const early = gallery({ ...rest, components: showcase_components });
		const full = gallery(cv);
		const shape = (g: typeof full) => g.map((x) => [x.id, x.fallback, x.gaps, x.items]);
		expect(shape(early)).toEqual(shape(full));
		const counts = templateCounts(cv);
		for (const g of full) expect(counts.get(g.id)).toEqual({ served: g.served, withGeometry: g.withGeometry });
	});
});
