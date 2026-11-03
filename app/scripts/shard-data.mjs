// @ts-nocheck plain node script
// Splits the generated views for fast loading (DevLog-012). Input: static/data/*.json from scripts/build_views.py, which
// stay canonical. Output: static/data/parts/ (gitignored, rebuilt before every dev / build).
//   summary.json            overview and the org names it shows; inlined in every prerendered page
//   components/meta.json    registries, layouts, showcase rows and showcase components (the layout gallery needs no more)
//   components/<n>.json     components in class order, at most MAX_PART bytes per part
//   people/meta.json        persons, sources and field lists
//   people/<n>.json         observation rows, at most MAX_PART bytes per part
import { mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

export const MAX_PART = 1_000_000;

/** Consecutive groups of items, each at most `max` bytes of JSON (a single larger item keeps its own group). */
export function splitBySize(items, max = MAX_PART) {
	const groups = [];
	let cur = [];
	let size = 0;
	for (const it of items) {
		const n = JSON.stringify(it).length + 1;
		if (cur.length && size + n > max) {
			groups.push(cur);
			cur = [];
			size = 0;
		}
		cur.push(it);
		size += n;
	}
	if (cur.length) groups.push(cur);
	return groups;
}

export function shardComponents(view) {
	const { components, ...rest } = view;
	const showcase = new Set((view.showcase ?? []).map((s) => s.component_id));
	// stable sort: within a class the canonical order holds, so a table sorted by class never reorders as parts arrive
	const ordered = [...components].sort((a, b) => (a.class < b.class ? -1 : a.class > b.class ? 1 : 0));
	const parts = splitBySize(ordered);
	return { meta: { ...rest, parts: parts.length, total: components.length, showcase_components: components.filter((c) => showcase.has(c.component_id)) }, parts };
}

export function shardPeople(raw) {
	const { obs, ...rest } = raw;
	const parts = splitBySize(obs);
	return { meta: { ...rest, parts: parts.length, total: obs.length }, parts };
}

export function buildSummary(registry, componentParts, peopleParts) {
	const ov = registry.overview;
	const wanted = new Set([...ov.top_fabs, ...ov.top_vendors].map(([id]) => id));
	const names = Object.fromEntries(registry.orgs.filter((o) => wanted.has(o.id)).map((o) => [o.id, o.name]));
	return { generated_on: registry.generated_on, overview: ov, names, parts: { components: componentParts, people: peopleParts } };
}

function main() {
	const data = join(dirname(fileURLToPath(import.meta.url)), '..', 'static', 'data');
	const read = (f) => JSON.parse(readFileSync(join(data, f), 'utf-8'));
	const out = join(data, 'parts');
	const write = (f, v) => {
		mkdirSync(dirname(join(out, f)), { recursive: true });
		writeFileSync(join(out, f), JSON.stringify(v));
	};
	rmSync(out, { recursive: true, force: true }); // generated, gitignored
	const c = shardComponents(read('components.json'));
	const p = shardPeople(read('people.json'));
	write('components/meta.json', c.meta);
	c.parts.forEach((x, i) => write(`components/${i}.json`, x));
	write('people/meta.json', p.meta);
	p.parts.forEach((x, i) => write(`people/${i}.json`, x));
	write('summary.json', buildSummary(read('registry.json'), c.parts.length, p.parts.length));
	console.log(`shard-data: components ${c.parts.length} parts, people ${p.parts.length} parts`);
}

if (process.argv[1] === fileURLToPath(import.meta.url)) main();
