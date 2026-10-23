<script lang="ts">
	import { onMount } from 'svelte';
	import { link } from '../../lib/paths';
	import { store } from '../../lib/state.svelte';
	import { matches, sortOrgs, type SortDir } from '../../lib/orgs';
	import EventList from '../../lib/EventList.svelte';
	import type { Org } from '../../lib/types';

	let q = $state('');
	let qLive = $state('');
	let type = $state('');
	let country = $state('');
	let sortKey = $state('lens.pub');
	let sortDir = $state<SortDir>('desc');
	let selId = $state('');
	let timer: ReturnType<typeof setTimeout> | null = null;

	const cols: { key: string; label: string; tip: string; num?: boolean }[] = [
		{ key: 'name', label: 'Organization', tip: 'Own preferred English name' },
		{ key: 'type', label: 'Type', tip: 'Institutional kind' },
		{ key: 'country', label: 'CC', tip: 'ISO 3166-1 alpha-2, only when a record states it' },
		{ key: 'status', label: 'Status', tip: 'active, acquired, renamed, merged, historical, unknown' },
		{ key: 'lens.pub', label: 'Publications', tip: 'Publications linked to the organization through any lens (components, supply, standards, authors, events)', num: true },
		{ key: 'lens.ppl', label: 'People', tip: 'People with a published affiliation at the organization', num: true },
		{ key: 'lens.cmp_fab', label: 'Components', tip: 'Components the publication states the organization fabricated', num: true },
		{ key: 'lens.sup', label: 'Supply', tip: 'Stated uses of the organization as a vendor, foundry or cleanroom', num: true }
	];

	onMount(() => {
		const fromHash = () => {
			const h = decodeURIComponent(location.hash.slice(1));
			if (h) selId = h;
		};
		fromHash();
		addEventListener('hashchange', fromHash);
		return () => removeEventListener('hashchange', fromHash);
	});
	function onInput(v: string) {
		qLive = v;
		if (timer) clearTimeout(timer);
		timer = setTimeout(() => (q = v), 300);
	}
	function sortBy(k: string) {
		if (sortKey !== k) {
			sortKey = k;
			sortDir = k.startsWith('lens.') ? 'desc' : 'asc';
		} else if (sortDir === 'asc') sortDir = 'desc';
		else if (sortDir === 'desc') {
			sortKey = 'name';
			sortDir = 'asc';
		}
	}
	function select(id: string) {
		selId = id;
		history.replaceState(history.state, '', `#${encodeURIComponent(id)}`);
	}
	let orgs = $derived(store.reg?.orgs ?? []);
	let types = $derived([...new Set(orgs.map((o) => o.type))].sort());
	let countries = $derived([...new Set(orgs.map((o) => o.country).filter(Boolean))].sort());
	let rows = $derived(sortOrgs(orgs.filter((o) => matches(o, q) && (!type || o.type === type) && (!country || o.country === country)), sortKey, sortDir));
	let sel = $derived<Org | undefined>(selId ? store.byId.get(selId) : undefined);
	const name = (id: string) => store.byId.get(id)?.name ?? id;
	const LENS: [string, string, string][] = [
		['cmp_fab', 'fab', 'components the publication states the organization fabricated'],
		['cmp_fac', 'facility', 'components made in the organization as a shared facility'],
		['sup', 'supply', 'stated uses as a vendor, foundry or cleanroom'],
		['proc', 'processes', 'foundry processes described in publications (as foundry or broker)'],
		['std', 'standards', 'standards issued by the organization'],
		['ppl', 'people', 'people with a published affiliation at the organization'],
		['obs', 'affiliations', 'published author affiliations'],
		['pub', 'publications', 'publications linked to the organization through any lens (components, supply, standards, authors, events)']
	];
</script>

<div class="page">
	<div class="left">
		<div class="bar">
			<input type="search" placeholder="Search name, alias, printed name" value={qLive} oninput={(e) => onInput(e.currentTarget.value)} onkeydown={(e) => e.key === 'Enter' && (q = qLive)} />
			<select bind:value={type} data-tip="Filter by org type"><option value="">all types</option>{#each types as t}<option>{t}</option>{/each}</select>
			<select bind:value={country} data-tip="Filter by country"><option value="">all countries</option>{#each countries as c}<option>{c}</option>{/each}</select>
			<span class="muted num">{rows.length} / {orgs.length}</span>
		</div>
		<div class="scroll">
			<table class="t num">
				<thead>
					<tr>
						{#each cols as c}
							<th class:r={c.num} data-tip={c.tip} onclick={() => sortBy(c.key)}>{c.label}{sortKey === c.key ? (sortDir === 'asc' ? ' ^' : ' v') : ''}</th>
						{/each}
					</tr>
				</thead>
				<tbody>
					{#each rows as o (o.id)}
						<tr class:sel={o.id === selId} onclick={() => select(o.id)}>
							<td class="name">{o.name}</td><td>{o.type.replace(/_/g, ' ')}</td><td>{o.country}</td><td>{o.status}</td>
							{#each ['pub', 'ppl', 'cmp_fab', 'sup'] as k}<td class="r">{o.lens?.[k] || ''}</td>{/each}
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
	<aside class="detail">
		{#if sel}
			<h2>{sel.name} <a class="hub" href={link('/orgs/hub') + '?id=' + encodeURIComponent(sel.id)} data-tip="Everything about this organization: components, supply, people, publications">hub</a></h2>
			{#if sel.lens && Object.keys(sel.lens).length}
				<div class="lens num">
					{#each LENS as [k, l, t]}{#if sel.lens[k]}<span data-tip={t}><b>{sel.lens[k]}</b> {l}</span>{/if}{/each}
				</div>
			{/if}
			<dl>
				<dt>type</dt><dd>{sel.type.replace(/_/g, ' ')}</dd>
				<dt>country</dt><dd>{sel.country}</dd>
				<dt>status</dt><dd>{sel.status}</dd>
				{#if sel.founded}<dt>founded</dt><dd>{sel.founded}</dd>{/if}
				{#if sel.dissolved}<dt>dissolved</dt><dd>{sel.dissolved}</dd>{/if}
				{#if sel.parent}<dt>parent</dt><dd><a href="#{sel.parent}" onclick={() => select(sel!.parent)}>{name(sel.parent)}</a></dd>{/if}
				{#if sel.ror}<dt>ROR</dt><dd><a href={sel.ror} target="_blank" rel="noopener">{sel.ror.replace('https://ror.org/', '')}</a></dd>{/if}
				{#if sel.qid}<dt>Wikidata</dt><dd><a href="https://www.wikidata.org/wiki/{sel.qid}" target="_blank" rel="noopener">{sel.qid}</a></dd>{/if}
				{#if sel.website}<dt>website</dt><dd><a href={sel.website} target="_blank" rel="noopener">{sel.website.replace(/^https?:\/\//, '')}</a></dd>{/if}
			</dl>
			{#if sel.children.length}
				<h3>Units ({sel.children.length})</h3>
				<ul>{#each sel.children as c}<li><a href="#{c}" onclick={() => select(c)}>{name(c)}</a></li>{/each}</ul>
			{/if}
			{#if sel.events.length}
				<h3>Events</h3>
				<EventList events={sel.events.map((e) => store.evById.get(e)).filter((e) => e !== undefined)} self={sel.id} {name} href={(id) => '#' + id} onpick={select} sources={store.reg?.sources ?? {}} />
			{/if}
			{#if sel.aliases.length}
				<h3>Aliases</h3>
				<ul>{#each sel.aliases as a}<li>{a.alias} <span class="muted">{a.type}</span></li>{/each}</ul>
			{/if}
			{#if sel.printed.length}
				<h3>Printed in publications as</h3>
				<ul>{#each sel.printed as p}<li>{p}</li>{/each}</ul>
			{/if}
		{:else}
			<p class="muted">Select an organization.</p>
		{/if}
	</aside>
</div>

<style>
	.page { height: 100%; display: grid; grid-template-columns: minmax(0, 1fr) 420px; grid-template-rows: minmax(0, 1fr); }
	.left { min-width: 0; min-height: 0; display: grid; grid-template-rows: auto minmax(0, 1fr); border-right: 1px solid var(--border); }
	.bar { display: flex; gap: 6px; align-items: center; padding: 6px 8px; background: var(--surface); border-bottom: 1px solid var(--border); }
	.bar input { flex: 1; }
	.scroll { overflow: auto; }
	table.t { border-collapse: collapse; width: 100%; }
	.t th, .t td { padding: 2px 6px; border-bottom: 1px solid var(--grid); text-align: left; white-space: nowrap; }
	.t th { position: sticky; top: 0; background: var(--surface); color: var(--ink-3); font-weight: 500; cursor: pointer; user-select: none; }
	.t .r { text-align: right; }
	.t td.name { max-width: 420px; overflow: hidden; text-overflow: ellipsis; }
	.t tbody tr { cursor: pointer; }
	.t tbody tr:hover { background: var(--hover); }
	.t tbody tr.sel { background: var(--sel); }
	.detail { min-height: 0; overflow: auto; padding: 8px 10px; background: var(--surface); }
	h2 { margin: 0 0 6px; font-size: 14px; }
	h2 .hub { font-size: 11px; font-weight: 400; margin-left: 6px; }
	.lens { display: flex; flex-wrap: wrap; gap: 2px 10px; margin: 0 0 6px; font-size: 11px; color: var(--ink-3); }
	.lens b { color: var(--ink); font-weight: 600; }
	h3 { margin: 10px 0 4px; font-size: 11px; color: var(--ink-3); font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }
	dl { display: grid; grid-template-columns: 80px 1fr; gap: 2px 8px; margin: 0; }
	dt { color: var(--ink-3); }
	dd { margin: 0; overflow-wrap: anywhere; }
	ul { margin: 0; padding-left: 16px; }
	@media (max-width: 900px) { .page { grid-template-columns: 1fr; grid-template-rows: minmax(0, 1fr) 40%; } }
</style>
