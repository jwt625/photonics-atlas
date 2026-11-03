// Real generated views: the parts of app/scripts/shard-data.mjs add up to the canonical JSON, and the loaders' reassembly
// gives the same view back.
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { buildSummary, MAX_PART, shardComponents, shardPeople, splitBySize } from '../../scripts/shard-data.mjs';
import type { ComponentsView } from './components.svelte';
import { gallery, templateCounts } from './layout/gallery';
import type { PeopleRaw } from './people.svelte';
import type { Registry } from './types';

const load = <T>(f: string): T => JSON.parse(readFileSync(new URL(`../../static/data/${f}`, import.meta.url), 'utf-8')) as T;
const cv = load<ComponentsView>('components.json');
const pr = load<PeopleRaw>('people.json');
const rv = load<Registry>('registry.json');

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
		const s = buildSummary(rv, 1, 1);
		for (const [id] of [...rv.overview.top_fabs, ...rv.overview.top_vendors]) expect(s.names[id]).toBe(rv.orgs.find((o) => o.id === id)?.name);
		expect(JSON.stringify(s).length).toBeLessThan(10_000);
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
