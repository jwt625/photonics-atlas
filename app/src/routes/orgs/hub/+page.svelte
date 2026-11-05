<script lang="ts">
	// Org hub (DevLog-010 D190, D191, D198): one organization across all lenses. ?id=<org_id>, read client-side. Joins
	// run over the loaded views: registry, components, supply, people (public rows only).
	import { onMount } from 'svelte';
	import { afterNavigate } from '$app/navigation';
	import { link } from '../../../lib/paths';
	import { store } from '../../../lib/state.svelte';
	import { comp, loadComponents } from '../../../lib/components.svelte';
	import { loadSupply, sup, type SupplyView } from '../../../lib/supply.svelte';
	import { loadPeople, ppl, type PeopleView } from '../../../lib/people.svelte';
	import { dateNum, orgComponents, orgPeople, orgPublications } from '../../../lib/views';
	import { pubTip } from '../../../lib/pub';
	import EventList from '../../../lib/EventList.svelte';
	import Chips from '../../../lib/table/Chips.svelte';
	import DataTable from '../../../lib/table/DataTable.svelte';
	import { dateYear, type Col, type Filters, type Sort } from '../../../lib/table/filters';
	import type { Row, Usage } from '../../../lib/supply.svelte';
	import type { OrgComponent, OrgPerson, OrgPub } from '../../../lib/views';

	let id = $state('');
	const readId = () => (id = new URLSearchParams(location.search).get('id') ?? '');
	onMount(() => {
		loadComponents();
		loadSupply();
		loadPeople();
		readId();
	});
	afterNavigate(readId);

	const o = $derived(id ? store.byId.get(id) : undefined);
	const name = (x: string) => store.byId.get(x)?.name ?? x;
	const hub = (x: string) => link('/orgs/hub') + '?id=' + encodeURIComponent(x);

	// rows show as they arrive (D500); a tile shows the registry's lens count until its view is complete, never a false 0
	const cv = $derived(comp.view ?? comp.partial);
	const comps = $derived(cv && o ? orgComponents(cv.components, o.id) : []);
	const nFab = $derived(comps.filter((c) => c.fab).length);
	const nFac = $derived(comps.filter((c) => c.fac).length);
	const sv = $derived(sup.view);
	const usage = $derived(sv && o ? sv.usage.filter((u) => u.org_id === o.id) : []);
	const procs = $derived(sv && o ? sv.processes.filter((p) => p.org_id === o.id || p.broker_org_id === o.id) : []);
	const stds = $derived(sv && o ? sv.standards.filter((s) => s.body_org_id === o.id) : []);
	// D199e: open the tab that holds this org's rows (usage, else standards, else processes filtered by name)
	const supplyHref = $derived(
		!o ? '' : link('/supply') + '#' + (usage.length ? 'org=' + encodeURIComponent(o.id) : (stds.length ? 'tab=standards' : 'tab=processes') + '&q=' + encodeURIComponent(o.name))
	);
	const prodById = $derived(new Map((sv?.products ?? []).map((p) => [p.product_id, p])));
	const catLabel = (c: string) => sv?.categories.find((x) => x.id === c)?.label ?? '';
	const pv = $derived(ppl.view ?? ppl.partial);
	const people = $derived(pv && o ? orgPeople(pv, o.id) : []);
	const nObs = $derived(people.reduce((t, p) => t + p.n, 0));
	const events = $derived(o ? o.events.map((e) => store.evById.get(e)).filter((e) => e !== undefined) : []);

	// Publications across the lenses (D199t; same definition as the lens count shown in the tile and on /orgs)
	const EMPTY_S = { generated_on: '', categories: [], usage: [], processes: [], standards: [], tests: [], products: [], specs: [], sources: {} } as SupplyView;
	const EMPTY_P = { generated_on: '', counts: {}, totals_by_type: {}, persons: [], obs: [], byPerson: [], sources: {} } as PeopleView;
	const sources = $derived(o && store.reg ? orgPublications(o.id, store.reg, cv?.components ?? [], sv ?? EMPTY_S, pv ?? EMPTY_P) : []);
	const lens = (k: string) => o?.lens?.[k] ?? 0;
	const allIn = $derived(!!comp.view && !!sv && !!ppl.view);
	const tiles = $derived<[number, string, string][]>([
		[comp.view ? nFab : lens('cmp_fab'), 'fabricated', 'components the publication states the organization fabricated'],
		[comp.view ? nFac : lens('cmp_fac'), 'facility', 'components made in the organization as a shared facility'],
		[sv ? usage.length : lens('sup'), 'supply', 'stated uses as a vendor, foundry or cleanroom'],
		[sv ? procs.length : lens('proc'), 'processes', 'foundry processes described in publications (as foundry or broker)'],
		[sv ? stds.length : lens('std'), 'standards', 'standards issued by the organization'],
		[ppl.view ? people.length : lens('ppl'), 'people', 'people with a published affiliation at the organization'],
		[ppl.view ? nObs : lens('obs'), 'affiliations', 'published author affiliations at the organization'],
		[events.length, 'events', 'acquisitions, renames, spin-offs, mergers'],
		[allIn ? sources.length : lens('pub'), 'publications', 'publications linked to the organization through any lens']
	]);
	const pending = $derived([!comp.view && `components ${comp.loaded} / ${comp.total || '...'}`, !sv && 'supply', !ppl.view && `affiliations ${ppl.loaded} / ${ppl.total || '...'}`].filter(Boolean).join(', '));

	// tables (DevLog-013 D504); a panel's rows scroll inside it
	const H = '340px';
	const bg = 'var(--surface)';
	const yearNum = (y: string | undefined) => (y ? Number(y) : null);
	const cCols: Col<OrgComponent>[] = [
		{ key: 'label', label: 'component', kind: 'text', w: 220, get: (r) => r.c.label, cellTip: (r) => r.c.label, cell: compCell },
		{ key: 'class', label: 'class', kind: 'enum', w: 170, get: (r) => r.c.class },
		{ key: 'role', label: 'role', kind: 'enum', w: 66, get: (r) => [r.fab ? 'fab' : '', r.fac ? 'facility' : ''].filter(Boolean) },
		{ key: 'platform', label: 'platform', kind: 'enum', w: 90, get: (r) => r.c.platform },
		{ key: 'year', label: 'year', kind: 'num', w: 58, right: true, get: (r) => yearNum(r.c.source?.year) }
	];
	const product = (u: Usage) => {
		const p = u.product_id ? prodById.get(u.product_id) : undefined;
		return u.product_id ? (p?.model ?? u.product_id) + (p?.product_line ? ' (' + p.product_line + ')' : '') : '';
	};
	const uCols: Col<Usage>[] = [
		{ key: 'role', label: 'role', kind: 'enum', get: (u) => u.role, enumLabel: (r) => r.replace(/_/g, ' ') },
		{ key: 'cat', label: 'cat', kind: 'enum', cls: 'mono', tip: 'supply category', get: (u) => u.category_id, enumLabel: (c) => c + ' ' + catLabel(c), text: (u) => u.category_id, cellTip: (u) => catLabel(u.category_id) },
		{ key: 'product', label: 'product', kind: 'enum', get: product },
		{ key: 'pub', label: 'publication', kind: 'text', cls: 'lbl', get: (u) => sv?.sources[u.source_id]?.title },
		{ key: 'year', label: 'year', kind: 'num', right: true, get: (u) => yearNum(sv?.sources[u.source_id]?.year) },
		{ key: 'stated', label: 'stated', kind: 'text', cls: 'wrap', get: (u) => u.stated_spec }
	];
	const rCols: Col<Row>[] = [
		{ key: 'process', label: 'process (as printed)', kind: 'text', cls: 'wrap', get: (p) => p.process_name },
		{ key: 'platform', label: 'platform', kind: 'enum', get: (p) => p.platform },
		{ key: 'pdk', label: 'PDK', kind: 'enum', get: (p) => p.pdk_name },
		{ key: 'pub', label: 'publication', kind: 'text', cls: 'lbl', get: (p) => sv?.sources[p.source_id]?.title }
	];
	const nCols: Col<OrgPerson>[] = [
		{ key: 'name', label: 'person', kind: 'text', get: (p) => p.person.name, cell: personCell },
		{ key: 'n', label: 'affiliations', kind: 'num', right: true, tip: 'published affiliations at this organization', get: (p) => p.n },
		{ key: 'first', label: 'first', kind: 'num', right: true, tip: 'earliest publication date (range filter in years)', get: (p) => dateYear(p.first), text: (p) => p.first, sort: (p) => dateNum(p.first) },
		{ key: 'last', label: 'last', kind: 'num', right: true, tip: 'latest publication date (range filter in years)', get: (p) => dateYear(p.last), text: (p) => p.last, sort: (p) => dateNum(p.last) }
	];
	const nSort: Sort = { key: 'n', dir: -1 };
	const nTie = (a: OrgPerson, b: OrgPerson) => a.person.name.localeCompare(b.person.name);
	const sCols: Col<OrgPub>[] = [
		{ key: 'year', label: 'year', kind: 'num', w: 58, right: true, get: (s) => yearNum(s.p.year) },
		{ key: 'title', label: 'publication', kind: 'text', w: 330, get: (s) => s.p.title, cellTip: (s) => pubTip(s.p), cell: pubCell },
		{ key: 'type', label: 'type', kind: 'enum', w: 110, get: (s) => s.p.type },
		{ key: 'uses', label: 'for', kind: 'enum', w: 110, tip: 'what the publication contributes for this organization', get: (s) => [...s.uses].sort() },
		{ key: 'atlas', label: '', kind: 'none', w: 44, cell: atlasCell }
	];
	let cF = $state<Filters>({});
	let uF = $state<Filters>({});
	let rF = $state<Filters>({});
	let nF = $state<Filters>({});
	let sF = $state<Filters>({});
	let cN = $state(0);
	let uN = $state(0);
	let rN = $state(0);
	let nN = $state(0);
	let sN = $state(0);
	const drop = (f: Filters, k: string) => {
		const n = { ...f };
		delete n[k];
		return n;
	};
</script>

{#snippet compCell(r: OrgComponent)}<a href={link('/components') + '#' + encodeURIComponent(r.c.component_id)}>{r.c.label}</a>{/snippet}
{#snippet personCell(p: OrgPerson)}<a href={link('/people') + '#p=' + encodeURIComponent(p.person.id)}>{p.person.name}</a>{/snippet}
{#snippet pubCell(s: OrgPub)}{#if s.p.url}<a href={s.p.url} target="_blank" rel="noopener">{s.p.title}</a>{:else}{s.p.title}{/if}{/snippet}
{#snippet atlasCell(s: OrgPub)}{#if s.p.atlas}<a href={s.p.atlas[1]} target="_blank" rel="noopener" data-tip="Open in the {s.p.atlas[0]}">atlas</a>{/if}{/snippet}

<div class="page">
	{#if !store.reg}
		<p class="muted"><a href={link('/orgs')}>Organizations</a> / <span class="mono">{id}</span>: registry loading</p>
	{:else if !o}
		<p class="muted">No organization <span class="mono">{id || '(no id)'}</span>. <a href={link('/orgs')}>Organizations</a></p>
	{:else}
		<header class="hd">
			<div class="crumbs"><a href={link('/orgs') + '#' + encodeURIComponent(o.id)}>Organizations</a></div>
			<h1>{o.name}</h1>
			<div class="meta">
				<span>{o.type === 'unknown' ? 'type unknown' : o.type.replace(/_/g, ' ')}</span>
				{#if o.country}<span>{o.country}</span>{/if}
				<span>{o.status === 'unknown' ? 'status unknown' : o.status}</span>
				{#if o.founded}<span>founded {o.founded}</span>{/if}
				{#if o.dissolved}<span>dissolved {o.dissolved}</span>{/if}
				{#if o.parent}<span>parent <a href={hub(o.parent)}>{name(o.parent)}</a></span>{/if}
				{#if o.ror}<a href={o.ror} target="_blank" rel="noopener">ROR</a>{/if}
				{#if o.qid}<a href="https://www.wikidata.org/wiki/{o.qid}" target="_blank" rel="noopener">Wikidata</a>{/if}
				{#if o.website}<a href={o.website} target="_blank" rel="noopener">website</a>{/if}
				{#each o.links as [site, href]}<a {href} target="_blank" rel="noopener" data-tip="Papers of this organization in the {site}">{site}</a>{/each}
				{#if pending}<span class="muted num">loading {pending}</span>{/if}
			</div>
			<div class="tiles">
				{#each tiles as [n, k, t]}
					<div class="tile" class:zero={!n} data-tip={t}><span class="v num">{n}</span><span class="k">{k}</span></div>
				{/each}
			</div>
		</header>
		<div class="grid">
			{#if comps.length}
				<section class="panel">
					<h3>Components <span class="muted num">{cN} / {comps.length}{comp.view ? '' : ' so far'}</span> <a class="more" href={link('/components')}>atlas</a></h3>
					<Chips sets={[{ columns: cCols, filters: cF }]} onremove={(_, k) => (cF = drop(cF, k))} onclear={() => (cF = {})} />
					<DataTable columns={cCols} rows={comps} rowKey={(r) => r.c.component_id} bind:filters={cF} bind:shown={cN} maxHeight={H} {bg} />
				</section>
			{/if}
			{#if usage.length || procs.length || stds.length}
				<section class="panel">
					<h3>Supply {#if usage.length}<span class="muted num">{uN} / {usage.length}</span>{/if} <a class="more" href={supplyHref}>supply view</a></h3>
					{#if usage.length}
						<Chips sets={[{ columns: uCols, filters: uF }]} onremove={(_, k) => (uF = drop(uF, k))} onclear={() => (uF = {})} />
						<DataTable columns={uCols} rows={usage} rowKey={(u) => u.usage_id} bind:shown={uN} rowTip={(u) => pubTip(sv?.sources[u.source_id] ?? {}, u.locator)} bind:filters={uF} maxHeight={H} {bg} />
					{/if}
					{#if procs.length}
						<h4>Foundry processes <span class="num">{rN} / {procs.length}</span></h4>
						<Chips sets={[{ columns: rCols, filters: rF }]} onremove={(_, k) => (rF = drop(rF, k))} onclear={() => (rF = {})} />
						<DataTable columns={rCols} rows={procs} rowKey={(p) => p.process_id} bind:shown={rN} rowTip={(p) => [p.broker_org_id === o.id ? 'this organization as broker; foundry ' + name(p.org_id) : '', pubTip(sv?.sources[p.source_id], p.locator)].filter(Boolean).join('\n')} bind:filters={rF} maxHeight={H} {bg} />
					{/if}
					{#if stds.length}
						<h4>Standards issued</h4>
						<p class="mono small">{stds.map((s) => s.designation).join(', ')}</p>
					{/if}
				</section>
			{/if}
			{#if people.length}
				<section class="panel">
					<h3>People <span class="muted num">{nN} / {people.length} people, {nObs} affiliations{ppl.view ? '' : ' so far'}</span> <a class="more" href={link('/people') + '#m=orgs&org=' + encodeURIComponent(o.id)}>people view</a></h3>
					<Chips sets={[{ columns: nCols, filters: nF }]} onremove={(_, k) => (nF = drop(nF, k))} onclear={() => (nF = {})} />
					<DataTable columns={nCols} rows={people} rowKey={(p) => p.person.id} bind:shown={nN} defaultSort={nSort} tie={nTie} bind:filters={nF} maxHeight={H} {bg} />
				</section>
			{/if}
			{#if o.children.length || o.aliases.length || events.length || o.printed.length}
				<section class="panel">
					<h3>Organization</h3>
					<dl>
						{#if o.children.length}<dt>units</dt><dd>{#each o.children as c, i}{i ? ', ' : ''}<a href={hub(c)}>{name(c)}</a>{/each}</dd>{/if}
						{#if o.aliases.length}<dt>also known as</dt><dd>{#each o.aliases as a, i}{i ? '; ' : ''}<span data-tip={a.type}>{a.alias}</span>{/each}</dd>{/if}
						{#if o.printed.length}<dt>printed as</dt><dd>{o.printed.join('; ')}</dd>{/if}
					</dl>
					{#if events.length}
						<h4>Events</h4>
						<EventList {events} self={o.id} {name} href={hub} sources={store.reg.sources} />
					{/if}
				</section>
			{/if}
			{#if sources.length}
				<section class="panel">
					<h3>Publications <span class="muted num">{sN} / {sources.length}{allIn ? '' : ' so far'}</span></h3>
					<Chips sets={[{ columns: sCols, filters: sF }]} onremove={(_, k) => (sF = drop(sF, k))} onclear={() => (sF = {})} />
					<DataTable columns={sCols} rows={sources} rowKey={(x) => x.id} bind:shown={sN} bind:filters={sF} maxHeight={H} {bg} />
				</section>
			{/if}
		</div>
	{/if}
</div>

<style>
	.page { height: 100%; overflow: auto; padding: 10px 14px 24px; }
	.hd { margin-bottom: 10px; }
	.crumbs { font-size: 11px; color: var(--ink-3); }
	h1 { margin: 2px 0 4px; font-size: 15px; font-weight: 600; }
	.meta { display: flex; flex-wrap: wrap; align-items: center; gap: 4px 12px; font-size: 11px; color: var(--ink-2); }
	.tiles { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
	.tile { display: flex; align-items: baseline; gap: 6px; background: var(--surface); border: 1px solid var(--border); padding: 3px 8px; }
	.tile .v { font-size: 15px; font-weight: 600; }
	.tile .k { color: var(--ink-3); font-size: 11px; }
	.tile.zero .v { color: var(--ink-3); font-weight: 400; }
	.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(520px, 1fr)); gap: 10px; align-items: start; }
	.panel { background: var(--surface); border: 1px solid var(--border); padding: 6px 8px; min-width: 0; }
	h3 { display: flex; gap: 8px; align-items: baseline; margin: 0 0 4px; font-size: 11px; color: var(--ink-3); font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }
	h3 .muted { text-transform: none; letter-spacing: 0; font-weight: 400; }
	h3 .more { margin-left: auto; text-transform: none; letter-spacing: 0; font-weight: 400; }
	h4 { margin: 8px 0 2px; font-size: 11px; color: var(--ink-3); font-weight: 500; }
	.panel > :global(.scroll) { height: auto; }
	dl { display: grid; grid-template-columns: 96px 1fr; gap: 2px 8px; margin: 0; }
	dt { color: var(--ink-3); }
	dd { margin: 0; overflow-wrap: anywhere; }
	.small { font-size: 11px; }
	p { margin: 4px 0; }
	@media (max-width: 700px) { .grid { grid-template-columns: minmax(0, 1fr); } .page { padding: 8px; } }
</style>
