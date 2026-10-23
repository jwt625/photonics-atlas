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
	import { corpusOf, eoSearch, orgComponents, orgPeople, pkOrg, siblingPaper } from '../../../lib/views';

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

	// Sources across lenses: C components, S supply, P people, E events.
	interface Src {
		id: string;
		title: string;
		year: string;
		url: string;
		lenses: Set<string>;
	}
	const sources = $derived.by(() => {
		const m = new Map<string, Src>();
		const add = (sid: string, lens: string, meta: { title?: string; year?: string; url?: string } = {}) => {
			const s = m.get(sid) ?? { id: sid, title: meta.title ?? '', year: meta.year ?? '', url: meta.url ?? '', lenses: new Set<string>() };
			if (!s.title && meta.title) Object.assign(s, { title: meta.title, year: meta.year ?? '', url: meta.url ?? '' });
			s.lenses.add(lens);
			m.set(sid, s);
		};
		for (const { c } of comps) add(c.source_id, 'C', c.source);
		for (const u of usage) add(u.source_id, 'S', sv?.sources[u.source_id]);
		for (const p of procs) add(p.source_id, 'S', sv?.sources[p.source_id]);
		// D199e: papers whose reliability tests cite a standard of this org (standards body)
		const sids = new Set(stds.map((x) => x.standard_id));
		if (sids.size) for (const t of sv?.tests ?? []) if (t.standard_ids?.split(';').some((x) => sids.has(x.trim()))) add(t.source_id, 'S', sv?.sources[t.source_id]);
		if (pv && o) for (const ob of pv.obs) if (ob.org_id === o.id) add(ob.source_id, 'P', pv.sources[ob.source_id]);
		for (const e of events) for (const s of e.sources) add(s, 'E');
		return [...m.values()].sort((a, b) => Number(b.year || 0) - Number(a.year || 0) || a.id.localeCompare(b.id));
	});
	const LENS_TIP: Record<string, string> = { C: 'components', S: 'supply rows', P: 'public people observations', E: 'org events' };
	const eoStrings = $derived(o ? o.printed.filter((p) => p.corpus === 'eo' && p.n > 0) : []);
	const pkStrings = $derived(o ? o.printed.filter((p) => p.corpus === 'pk' && p.n > 0) : []);
	const loading = $derived(!comp.view || !sv || !pv);
</script>

<div class="page">
	{#if !store.reg}
		<p class="muted">loading</p>
	{:else if !o}
		<p class="muted">No organization <span class="mono">{id || '(no id)'}</span>. <a href={link('/orgs')}>Organizations</a></p>
	{:else}
		<header class="hd">
			<div class="crumbs"><a href={link('/orgs') + '#' + encodeURIComponent(o.id)}>Organizations</a> / <span class="mono">{o.id}</span></div>
			<h1>{o.name}</h1>
			<div class="meta">
				<span data-tip="registry org type">{o.type === 'unknown' ? 'type unknown' : o.type}</span>
				{#if o.country}<span>{o.country}</span>{/if}
				<span data-tip="registry status">{o.status === 'unknown' ? 'status unknown' : o.status}</span>
				{#if o.founded}<span>founded {o.founded}</span>{/if}
				{#if o.dissolved}<span>dissolved {o.dissolved}</span>{/if}
				{#if o.parent}<span>parent <a href={hub(o.parent)}>{name(o.parent)}</a></span>{/if}
				{#if o.ror}<a href={o.ror} target="_blank" rel="noopener">ROR</a>{/if}
				{#if o.qid}<a href="https://www.wikidata.org/wiki/{o.qid}" target="_blank" rel="noopener">Wikidata</a>{/if}
				{#if o.website}<a href={o.website} target="_blank" rel="noopener">website</a>{/if}
				{#each eoStrings as p}<a href={eoSearch(p.printed)} target="_blank" rel="noopener" data-tip="EO modulator atlas table, search '{p.printed}' ({p.n} EO author rows); token search, may match more papers">EO atlas</a>{/each}
				{#each pkStrings as p}<a href={pkOrg(p.printed)} target="_blank" rel="noopener" data-tip="Advanced packaging atlas table filtered to org '{p.printed}' ({p.n} PK author rows)">packaging atlas</a>{/each}
				{#if loading}<span class="spinner"></span>{/if}
			</div>
			<div class="tiles">
				{#each [[nFab, 'fab', 'components whose source states the org fabricated them (fab_org_ids)'], [nFac, 'facility', 'components made in the org as facility (facility_org_ids)'], [usage.length, 'supply rows', 'product_usage rows naming the org'], [procs.length, 'processes', 'foundry process observations (as foundry or broker)'], [stds.length, 'standards', 'standards with the org as body'], [people.length, 'people', 'public persons with a public observation at the org'], [nObs, 'observations', 'public affiliation observations at the org'], [events.length, 'events', 'org events'], [sources.length, 'sources', 'distinct sources across the lenses']] as [n, k, t]}
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
										<td class="lbl" data-tip={c.component_id + '\n' + c.label}><a href={link('/components') + '#' + encodeURIComponent(c.component_id)}>{c.label}</a></td>
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
								<thead><tr><th>role</th><th>cat</th><th>product</th><th>source</th><th class="r">year</th><th>stated</th></tr></thead>
								<tbody>
									{#each usage as u (u.usage_id)}
										{@const s = sv?.sources[u.source_id] ?? {}}
										<tr data-tip={[u.usage_id, s.title, 'locator ' + u.locator, 'basis ' + u.basis, u.notes].filter(Boolean).join('\n')}>
											<td>{u.role}</td><td class="mono" data-tip={catLabel(u.category_id)}>{u.category_id}</td><td data-tip={u.product_id ?? ''}>{u.product_id ? (prodById.get(u.product_id)?.model ?? u.product_id) + (prodById.get(u.product_id)?.product_line ? ' (' + prodById.get(u.product_id)?.product_line + ')' : '') : ''}</td><td>{u.source_id}</td><td class="r">{s.year ?? ''}</td><td class="wrap">{u.stated_spec ?? ''}</td>
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
					{/if}
					{#if procs.length}
						<h4>Process observations</h4>
						<div class="tw">
							<table class="t num">
								<thead><tr><th>process (as printed)</th><th>platform</th><th>PDK</th><th>source</th></tr></thead>
								<tbody>
									{#each procs as p (p.process_id)}
										<tr data-tip={[p.process_id, p.broker_org_id === o.id ? 'this org as broker; foundry ' + name(p.org_id) : '', 'locator ' + p.locator].filter(Boolean).join('\n')}><td class="wrap">{p.process_name}</td><td>{p.platform ?? ''}</td><td>{p.pdk_name ?? ''}</td><td>{p.source_id}</td></tr>
									{/each}
								</tbody>
							</table>
						</div>
					{/if}
					{#if stds.length}
						<h4>Standards (body)</h4>
						<p class="mono small">{stds.map((s) => s.designation).join(', ')}</p>
					{/if}
				</section>
			{/if}
			{#if people.length}
				<section class="panel">
					<h3>People <span class="muted num">{people.length} public persons, {nObs} observations</span> <a class="more" href={link('/people') + '#m=orgs&org=' + encodeURIComponent(o.id)}>people view</a></h3>
					<div class="tw">
						<table class="t num">
							<thead><tr><th>person</th><th class="r" data-tip="public observations at this org">obs</th><th class="r">first</th><th class="r">last</th></tr></thead>
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
			<section class="panel">
				<h3>Registry</h3>
				<dl>
					<dt>id</dt><dd class="mono">{o.id}</dd>
					<dt>name from</dt><dd data-tip={o.name_source}>{o.name_basis}</dd>
					<dt>origin</dt><dd>{o.origin.join(', ')}</dd>
					{#if o.children.length}<dt>units</dt><dd>{#each o.children as c, i}{i ? ', ' : ''}<a href={hub(c)}>{name(c)}</a>{/each}</dd>{/if}
					{#if o.aliases.length}<dt>aliases</dt><dd>{#each o.aliases as a, i}{i ? '; ' : ''}{a.alias} <span class="muted">{a.type}{a.scope ? ' @' + a.scope : ''}</span>{/each}</dd>{/if}
				</dl>
				{#if o.notes}<p class="muted small">{o.notes}</p>{/if}
				{#if events.length}
					<h4>Events</h4>
					{#each events as ev}
						<div class="ev" data-tip={`${ev.locator}\nsources: ${ev.sources.join(', ')}${ev.notes ? '\n' + ev.notes : ''}`}>
							<span class="num">{ev.effective || ev.announced || 'undated'}</span> {ev.type} <span class="muted">[{ev.grade}]</span>
							<div>{#each ev.participants as p, i}{i ? '; ' : ''}{#if p.org === o.id}<b>{name(p.org)}</b>{:else}<a href={hub(p.org)}>{name(p.org)}</a>{/if} <span class="muted">{p.role}</span>{/each}</div>
						</div>
					{/each}
				{/if}
				{#if o.printed.length}
					<h4>Printed strings</h4>
					<div class="tw">
						<table class="t num">
							<thead><tr><th>corpus</th><th>string</th><th class="r">rows</th><th>match</th></tr></thead>
							<tbody>{#each o.printed as p}<tr><td>{p.corpus}</td><td class="wrap">{p.printed}</td><td class="r">{p.n}</td><td class="muted">{p.basis}</td></tr>{/each}</tbody>
						</table>
					</div>
				{/if}
			</section>
			{#if sources.length}
				<section class="panel">
					<h3>Sources <span class="muted num">{sources.length}</span></h3>
					<div class="tw">
						<table class="t num">
							<thead><tr><th data-tip="C components, S supply, P people, E events">lens</th><th class="r">year</th><th>source</th><th></th></tr></thead>
							<tbody>
								{#each allSources ? sources : sources.slice(0, 30) as s (s.id)}
									{@const sib = siblingPaper(s.id)}
									<tr>
										<td class="mono" data-tip={[...s.lenses].map((l) => LENS_TIP[l]).join(', ')}>{[...s.lenses].sort().join('')}</td>
										<td class="r">{s.year}</td>
										<td class="lbl wide" data-tip={s.id + (s.title ? '\n' + s.title : '')}>{#if s.url}<a href={s.url} target="_blank" rel="noopener">{s.title || s.id}</a>{:else}{s.title || s.id}{/if} <span class="muted">{corpusOf(s.id)}</span></td>
										<td>{#if sib}<a href={sib.href} target="_blank" rel="noopener" data-tip="Open in the {sib.site}">atlas</a>{/if}</td>
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
	dl { display: grid; grid-template-columns: 80px 1fr; gap: 2px 8px; margin: 0; }
	dt { color: var(--ink-3); }
	dd { margin: 0; overflow-wrap: anywhere; }
	.ev { padding: 3px 0; border-bottom: 1px solid var(--grid); }
	.small { font-size: 11px; }
	p { margin: 4px 0; }
	.show { margin-top: 4px; height: 20px; font-size: 11px; }
	@media (max-width: 700px) { .grid { grid-template-columns: minmax(0, 1fr); } .page { padding: 8px; } }
</style>
