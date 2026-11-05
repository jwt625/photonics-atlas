// @ts-nocheck plain node script
// Splits the generated views for fast loading (DevLog-012). Input: static/data/*.json from scripts/build_views.py, which
// stay canonical. Output: static/data/parts/ (gitignored, rebuilt before every dev / build).
//   summary.json            overview, the org names it shows and the head rows of the tables (DevLog-013 D500): real
//                           first rows of each table's default order; inlined in every prerendered page
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

export const HEAD_ROWS = 40;
const clip = (s, n) => (s && s.length > n ? s.slice(0, n) : s);
const compact = (o) => Object.fromEntries(Object.entries(o).filter(([, v]) => v !== undefined && v !== '' && v !== null));

/** First rows of /components with no filter (class order; the parts arrive in this order), and the class tree. Long text is
 *  clipped to what a cell shows; the real row replaces it when part 0 arrives. */
export function headComponents(view) {
	const { parts, meta } = shardComponents(view);
	const counts = new Map();
	for (const c of view.components) counts.set(c.class, (counts.get(c.class) ?? 0) + 1);
	const tree = Object.entries(view.classes).map(([k, v]) => [k, v.label, Object.keys(v.subtypes).map((s) => [s, counts.get(k + '.' + s) ?? 0])]);
	const rows = (parts[0] ?? []).slice(0, HEAD_ROWS).map((c) =>
		compact({
			component_id: c.component_id,
			class: c.class,
			label: clip(c.label, 60),
			platform: c.platform,
			core_material: clip(c.core_material, 36),
			fab_orgs: c.fab_orgs,
			nv: c.metrics.length,
			source: compact({ title: clip(c.source?.title, 60), year: c.source?.year })
		})
	);
	return { total: meta.total, rows, tree };
}

/** First rows of /orgs: most publications, ties by name. */
export function headOrgs(registry) {
	const pub = (o) => o.lens?.pub ?? 0;
	const rows = [...registry.orgs]
		.sort((a, b) => pub(b) - pub(a) || a.name.localeCompare(b.name))
		.slice(0, HEAD_ROWS)
		.map((o) => compact({ id: o.id, name: o.name, type: o.type, country: o.country, status: o.status, lens: Object.fromEntries(['pub', 'ppl', 'cmp_fab', 'sup'].flatMap((k) => (o.lens?.[k] ? [[k, o.lens[k]]] : []))) }));
	return { total: registry.orgs.length, rows };
}

function dateNum(d) {
	const [y, m, day] = d.split('-').map(Number);
	if (!m) return y + 0.5;
	if (!day) return y + (m - 0.5) / 12;
	return y + (m - 1) / 12 + (day - 1) / 365;
}

/** First rows of /people: most affiliations, ties by name (same numbers as views.ts personStats). */
export function headPeople(raw) {
	const pf = (f) => raw.person_fields.indexOf(f);
	const of = (f) => raw.obs_fields.indexOf(f);
	const iP = of('p'), iD = of('active_on'), iO = of('org_id'), iPr = of('printed_org');
	const st = raw.persons.map(() => ({ n: 0, first: '', last: '', orgs: new Set() }));
	for (const o of raw.obs) {
		const s = st[o[iP]], d = o[iD];
		s.n++;
		if (!s.first || dateNum(d) < dateNum(s.first)) s.first = d;
		if (!s.last || dateNum(d) > dateNum(s.last)) s.last = d;
		s.orgs.add(o[iO] || 'printed:' + o[iPr]);
	}
	const rows = raw.persons
		.map((p, i) => ({ id: p[pf('id')], name: p[pf('name')], lin: p[pf('lin_grade')] || '', ...st[i], orgs: st[i].orgs.size }))
		.sort((a, b) => b.n - a.n || a.name.localeCompare(b.name))
		.slice(0, HEAD_ROWS)
		.map(compact);
	return { total: raw.persons.length, rows };
}

/** First rows of /supply (same numbers as views.ts vendors) and the category tree with rolled-up counts. */
export function headSupply(sv, registry) {
	const byId = new Map(registry.orgs.map((o) => [o.id, o]));
	const m = new Map();
	for (const u of sv.usage) {
		const v = m.get(u.org_id) ?? { rows: 0, src: new Set(), roles: new Set(), cats: new Set(), ys: [] };
		v.rows++;
		v.src.add(u.source_id);
		v.roles.add(u.role);
		v.cats.add(u.category_id);
		const y = Number(sv.sources[u.source_id]?.year);
		if (Number.isFinite(y) && y > 0) v.ys.push(y);
		m.set(u.org_id, v);
	}
	const rows = [...m]
		.sort((a, b) => b[1].rows - a[1].rows || a[0].localeCompare(b[0]))
		.slice(0, HEAD_ROWS)
		.map(([org, v]) =>
			compact({
				org,
				name: byId.get(org)?.name ?? org,
				type: byId.get(org)?.type,
				country: byId.get(org)?.country,
				rows: v.rows,
				sources: v.src.size,
				roles: [...v.roles].sort(),
				cats: [...v.cats].sort(),
				y0: v.ys.length ? Math.min(...v.ys) : null,
				y1: v.ys.length ? Math.max(...v.ys) : null
			})
		);
	const parent = new Map(sv.categories.map((c) => [c.id, c.parent]));
	const counts = new Map();
	for (const u of sv.usage) for (let c = u.category_id; c; c = parent.get(c)) counts.set(c, (counts.get(c) ?? 0) + 1);
	return { vendors: m.size, usage: sv.usage.length, rows, categories: sv.categories.map((c) => [c.id, c.label, c.parent ?? '', counts.get(c.id) ?? 0]) };
}

export function buildHead(componentsView, registry, peopleRaw, supplyView) {
	return { components: headComponents(componentsView), orgs: headOrgs(registry), people: headPeople(peopleRaw), supply: headSupply(supplyView, registry) };
}

export function buildSummary(registry, componentParts, peopleParts, head) {
	const ov = registry.overview;
	const wanted = new Set([...ov.top_fabs, ...ov.top_vendors].map(([id]) => id));
	const names = Object.fromEntries(registry.orgs.filter((o) => wanted.has(o.id)).map((o) => [o.id, o.name]));
	return { generated_on: registry.generated_on, overview: ov, names, parts: { components: componentParts, people: peopleParts }, head };
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
	const cv = read('components.json');
	const pv = read('people.json');
	const rv = read('registry.json');
	const c = shardComponents(cv);
	const p = shardPeople(pv);
	write('components/meta.json', c.meta);
	c.parts.forEach((x, i) => write(`components/${i}.json`, x));
	write('people/meta.json', p.meta);
	p.parts.forEach((x, i) => write(`people/${i}.json`, x));
	write('summary.json', buildSummary(rv, c.parts.length, p.parts.length, buildHead(cv, rv, pv, read('supply.json'))));
	console.log(`shard-data: components ${c.parts.length} parts, people ${p.parts.length} parts`);
}

if (process.argv[1] === fileURLToPath(import.meta.url)) main();
