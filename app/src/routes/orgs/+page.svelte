<script lang="ts">
	import { onMount } from 'svelte';
	import { link } from '../../lib/paths';
	import { store } from '../../lib/state.svelte';
	import { matches } from '../../lib/orgs';
	import EventList from '../../lib/EventList.svelte';
	import Chips from '../../lib/table/Chips.svelte';
	import DataTable from '../../lib/table/DataTable.svelte';
	import { safeDecode, type Col, type Filters, type Sort } from '../../lib/table/filters';
	import type { Org, Summary } from '../../lib/types';

	let { data }: { data: { summary: Summary } } = $props();
	const head = $derived(data.summary.head.orgs);

	let q = $state('');
	let qLive = $state('');
	let selId = $state('');
	let filters = $state<Filters>({});
	let shown = $state(0);
	let reveal = $state('');
	let timer: ReturnType<typeof setTimeout> | null = null;

	// fixed widths: the columns must not move when the registry replaces the head rows
	const lens = (k: string): Pick<Col<Org>, 'kind' | 'right' | 'w' | 'get' | 'text'> => ({ kind: 'num', right: true, w: 104, get: (o) => o.lens?.[k] ?? 0, text: (o) => (o.lens?.[k] ? String(o.lens[k]) : '') });
	const columns: Col<Org>[] = [
		{ key: 'name', label: 'Organization', kind: 'text', w: 320, tip: 'Own preferred English name', get: (o) => o.name },
		{ key: 'type', label: 'Type', kind: 'enum', w: 130, tip: 'Institutional kind', get: (o) => o.type, enumLabel: (v) => v.replace(/_/g, ' ') },
		{ key: 'country', label: 'CC', kind: 'enum', w: 52, tip: 'ISO 3166-1 alpha-2, only when a record states it', get: (o) => o.country },
		{ key: 'status', label: 'Status', kind: 'enum', w: 86, tip: 'active, acquired, renamed, merged, historical, unknown', get: (o) => o.status },
		{ key: 'pub', label: 'Publications', tip: 'Publications linked to the organization through any lens (components, supply, standards, authors, events)', ...lens('pub') },
		{ key: 'ppl', label: 'People', tip: 'People with a published affiliation at the organization', ...lens('ppl') },
		{ key: 'cmp_fab', label: 'Components', tip: 'Components the publication states the organization fabricated', ...lens('cmp_fab') },
		{ key: 'sup', label: 'Supply', tip: 'Stated uses of the organization as a vendor, foundry or cleanroom', ...lens('sup') }
	];
	const defaultSort: Sort = { key: 'pub', dir: -1 };
	const tie = (a: Org, b: Org) => a.name.localeCompare(b.name);

	onMount(() => {
		const fromHash = () => {
			const h = safeDecode(location.hash.slice(1));
			if (h) {
				selId = h;
				reveal = h;
			}
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
	function select(id: string) {
		selId = id;
		history.replaceState(history.state, '', `#${encodeURIComponent(id)}`);
	}
	// real first rows until the registry is in (same order, so nothing moves)
	const headOrgs = $derived(head.rows.map((o) => ({ aliases: [], printed: [], ...o }) as unknown as Org));
	let orgs = $derived(store.reg?.orgs ?? headOrgs);
	let rows = $derived(q ? orgs.filter((o) => matches(o, q)) : orgs);
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
			{#if store.reg}<span class="muted num">{shown} / {orgs.length}</span>{:else}<span class="muted num" data-tip="rows shown so far; the rest arrive with the registry">{head.rows.length} / {head.total} loaded</span>{/if}
		</div>
		<Chips sets={[{ columns, filters }]} onremove={(_, k) => { const n = { ...filters }; delete n[k]; filters = n; }} onclear={() => (filters = {})} />
		<DataTable {columns} {rows} rowKey={(o) => o.id} selected={selId} onselect={select} {defaultSort} {tie} bind:filters bind:shown {reveal} onrevealed={() => (reveal = '')} empty={store.reg ? 'No organization matches.' : ''} />
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
			{#if store.reg}<p class="muted">Select an organization.</p>{/if}
		{/if}
	</aside>
</div>

<style>
	.page { height: 100%; display: grid; grid-template-columns: minmax(0, 1fr) 420px; grid-template-rows: minmax(0, 1fr); }
	.left { min-width: 0; min-height: 0; display: flex; flex-direction: column; border-right: 1px solid var(--border); }
	.left > :global(.scroll) { flex: 1; height: auto; }
	.bar { display: flex; gap: 6px; align-items: center; padding: 6px 8px; background: var(--surface); border-bottom: 1px solid var(--border); }
	.bar input { flex: 1; min-width: 80px; }
	@media (max-width: 700px) { .bar { flex-wrap: wrap; } .bar input { flex-basis: 100%; } }
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
