<script lang="ts">
	// Org hub (DevLog-010 D190, D191, D198): one organization across all lenses. ?id=<org_id>, read client-side. Joins
	// run over the loaded views: registry, components, supply, people (public rows only).
	import { onMount } from 'svelte';
	import { afterNavigate } from '$app/navigation';
	import { link } from '../../../lib/paths';
	import { store } from '../../../lib/state.svelte';
	import { comp, loadComponents } from '../../../lib/components.svelte';
	import { loadSupply, sup } from '../../../lib/supply.svelte';
	import { loadPeople, ppl } from '../../../lib/people.svelte';
	import { orgComponents, orgPeople, orgPublications } from '../../../lib/views';
	import { pubTip } from '../../../lib/pub';
	import EventList from '../../../lib/EventList.svelte';

	let id = $state('');
	let allPeople = $state(false);
	let allSources = $state(false);
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

	const comps = $derived(comp.view && o ? orgComponents(comp.view.components, o.id) : []);
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
	const pv = $derived(ppl.view);
	const people = $derived(pv && o ? orgPeople(pv, o.id) : []);
	const nObs = $derived(people.reduce((t, p) => t + p.n, 0));
	const events = $derived(o ? o.events.map((e) => store.evById.get(e)).filter((e) => e !== undefined) : []);

	// Publications across the lenses (D199t; same definition as the lens count shown in the tile and on /orgs)
	const sources = $derived(o && store.reg && comp.view && sv && pv ? orgPublications(o.id, store.reg, comp.view.components, sv, pv) : []);
	const loading = $derived(!comp.view || !sv || !pv);
</script>

<div class="page">
	{#if !store.reg}
		<p class="muted">loading</p>
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
				{#if loading}<span class="spinner"></span>{/if}
			</div>
			<div class="tiles">
				{#each [[nFab, 'fabricated', 'components the publication states the organization fabricated'], [nFac, 'facility', 'components made in the organization as a shared facility'], [usage.length, 'supply', 'stated uses as a vendor, foundry or cleanroom'], [procs.length, 'processes', 'foundry processes described in publications (as foundry or broker)'], [stds.length, 'standards', 'standards issued by the organization'], [people.length, 'people', 'people with a published affiliation at the organization'], [nObs, 'affiliations', 'published author affiliations at the organization'], [events.length, 'events', 'acquisitions, renames, spin-offs, mergers'], [o.lens?.pub ?? 0, 'publications', 'publications linked to the organization through any lens']] as [n, k, t]}
					<div class="tile" class:zero={!n} data-tip={String(t)}><span class="v num">{n}</span><span class="k">{k}</span></div>
				{/each}
			</div>
		</header>
		<div class="grid">
			{#if comps.length}
				<section class="panel">
					<h3>Components <span class="muted num">{comps.length}</span> <a class="more" href={link('/components')}>atlas</a></h3>
					<div class="tw">
						<table class="t num">
							<thead><tr><th>component</th><th>class</th><th>role</th><th>platform</th><th class="r">year</th></tr></thead>
							<tbody>
								{#each comps as { c, fab, fac } (c.component_id)}
									<tr>
										<td class="lbl" data-tip={c.label}><a href={link('/components') + '#' + encodeURIComponent(c.component_id)}>{c.label}</a></td>
										<td>{c.class}</td><td>{[fab && 'fab', fac && 'facility'].filter(Boolean).join(', ')}</td><td>{c.platform ?? ''}</td><td class="r">{c.source.year}</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
				</section>
			{/if}
			{#if usage.length || procs.length || stds.length}
				<section class="panel">
					<h3>Supply <a class="more" href={supplyHref}>supply view</a></h3>
					{#if usage.length}
						<div class="tw">
							<table class="t num">
								<thead><tr><th>role</th><th data-tip="supply category">cat</th><th>product</th><th>publication</th><th class="r">year</th><th>stated</th></tr></thead>
								<tbody>
									{#each usage as u (u.usage_id)}
										{@const s = sv?.sources[u.source_id] ?? {}}
										<tr data-tip={pubTip(s, u.locator)}>
											<td>{u.role.replace(/_/g, ' ')}</td><td class="mono" data-tip={catLabel(u.category_id)}>{u.category_id}</td><td>{u.product_id ? (prodById.get(u.product_id)?.model ?? u.product_id) + (prodById.get(u.product_id)?.product_line ? ' (' + prodById.get(u.product_id)?.product_line + ')' : '') : ''}</td><td class="lbl">{s.title ?? ''}</td><td class="r">{s.year ?? ''}</td><td class="wrap">{u.stated_spec ?? ''}</td>
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
					{/if}
					{#if procs.length}
						<h4>Foundry processes</h4>
						<div class="tw">
							<table class="t num">
								<thead><tr><th>process (as printed)</th><th>platform</th><th>PDK</th><th>publication</th></tr></thead>
								<tbody>
									{#each procs as p (p.process_id)}
										{@const ps = sv?.sources[p.source_id]}
										<tr data-tip={[p.broker_org_id === o.id ? 'this organization as broker; foundry ' + name(p.org_id) : '', pubTip(ps, p.locator)].filter(Boolean).join('\n')}><td class="wrap">{p.process_name}</td><td>{p.platform ?? ''}</td><td>{p.pdk_name ?? ''}</td><td class="lbl">{ps?.title ?? ''}</td></tr>
									{/each}
								</tbody>
							</table>
						</div>
					{/if}
					{#if stds.length}
						<h4>Standards issued</h4>
						<p class="mono small">{stds.map((s) => s.designation).join(', ')}</p>
					{/if}
				</section>
			{/if}
			{#if people.length}
				<section class="panel">
					<h3>People <span class="muted num">{people.length} people, {nObs} affiliations</span> <a class="more" href={link('/people') + '#m=orgs&org=' + encodeURIComponent(o.id)}>people view</a></h3>
					<div class="tw">
						<table class="t num">
							<thead><tr><th>person</th><th class="r" data-tip="published affiliations at this organization">affiliations</th><th class="r">first</th><th class="r">last</th></tr></thead>
							<tbody>
								{#each allPeople ? people : people.slice(0, 25) as p (p.person.id)}
									<tr><td><a href={link('/people') + '#p=' + encodeURIComponent(p.person.id)}>{p.person.name}</a></td><td class="r">{p.n}</td><td class="r">{p.first}</td><td class="r">{p.last}</td></tr>
								{/each}
							</tbody>
						</table>
					</div>
					{#if people.length > 25}<button class="show" onclick={() => (allPeople = !allPeople)}>{allPeople ? 'top 25' : `all ${people.length}`}</button>{/if}
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
					<h3>Publications <span class="muted num">{sources.length}</span></h3>
					<div class="tw">
						<table class="t num">
							<thead><tr><th class="r">year</th><th>publication</th><th>type</th><th data-tip="what the publication contributes for this organization">for</th><th></th></tr></thead>
							<tbody>
								{#each allSources ? sources : sources.slice(0, 30) as s (s.id)}
									<tr>
										<td class="r">{s.p.year ?? ''}</td>
										<td class="lbl wide" data-tip={pubTip(s.p)}>{#if s.p.url}<a href={s.p.url} target="_blank" rel="noopener">{s.p.title}</a>{:else}{s.p.title}{/if}</td>
										<td class="muted">{s.p.type ?? ''}</td>
										<td class="muted">{[...s.uses].sort().join(', ')}</td>
										<td>{#if s.p.atlas}<a href={s.p.atlas[1]} target="_blank" rel="noopener" data-tip="Open in the {s.p.atlas[0]}">atlas</a>{/if}</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
					{#if sources.length > 30}<button class="show" onclick={() => (allSources = !allSources)}>{allSources ? 'latest 30' : `all ${sources.length}`}</button>{/if}
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
	.tw { max-height: 340px; overflow: auto; }
	table.t { border-collapse: collapse; width: 100%; }
	.t th, .t td { padding: 2px 6px; border-bottom: 1px solid var(--grid); text-align: left; white-space: nowrap; }
	.t th { position: sticky; top: 0; background: var(--surface); color: var(--ink-3); font-weight: 500; }
	.t .r { text-align: right; }
	.t td.lbl { max-width: 260px; overflow: hidden; text-overflow: ellipsis; }
	.t td.lbl.wide { max-width: 420px; }
	.t td.wrap { white-space: normal; }
	.t tbody tr:hover { background: var(--hover); }
	dl { display: grid; grid-template-columns: 96px 1fr; gap: 2px 8px; margin: 0; }
	dt { color: var(--ink-3); }
	dd { margin: 0; overflow-wrap: anywhere; }
	.small { font-size: 11px; }
	p { margin: 4px 0; }
	.show { margin-top: 4px; height: 20px; font-size: 11px; }
	@media (max-width: 700px) { .grid { grid-template-columns: minmax(0, 1fr); } .page { padding: 8px; } }
</style>
