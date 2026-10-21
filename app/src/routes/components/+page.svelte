<script lang="ts">
	import { onMount } from 'svelte';
	import { comp, fmtValue, fmtWavelength, loadComponents, type Component, type Metric } from '../../lib/components.svelte';
	import { link } from '../../lib/paths';
	import LayoutViews from '../../lib/layout/LayoutViews.svelte';
	import { templateFor } from '../../lib/layout/resolve';

	let cls = $state('');
	let param = $state('');
	let q = $state('');
	let qLive = $state('');
	let selId = $state('');
	let sortKey = $state('class');
	let sortDir = $state<1 | -1>(1);
	let timer: ReturnType<typeof setTimeout> | null = null;

	onMount(() => {
		loadComponents();
		const fromHash = () => {
			const h = decodeURIComponent(location.hash.slice(1));
			if (h) selId = h;
		};
		fromHash();
		addEventListener('hashchange', fromHash);
		return () => removeEventListener('hashchange', fromHash);
	});

	type Row = { c: Component; m: Metric };
	let view = $derived(comp.view);
	let rows = $derived<Row[]>(view ? view.components.flatMap((c) => c.metrics.map((m) => ({ c, m }))) : []);
	let classCounts = $derived.by(() => {
		const n: Record<string, number> = {};
		for (const c of view?.components ?? []) {
			const top = c.class.split('.')[0];
			n[top] = (n[top] ?? 0) + 1;
		}
		return n;
	});
	let params = $derived([...new Set(rows.filter((r) => !cls || r.c.class.startsWith(cls + '.')).map((r) => r.m.parameter))].sort());
	const keyOf = (r: Row, k: string): string | number => {
		if (k === 'value') return Number(r.m.value);
		if (k === 'wavelength') return Number(r.m.wavelength_nm ?? 0);
		if (k in r.m) return String((r.m as unknown as Record<string, string>)[k] ?? '');
		return String((r.c as unknown as Record<string, string>)[k] ?? '');
	};
	let shown = $derived(
		rows
			.filter((r) => (!cls || r.c.class.startsWith(cls + '.')) && (!param || r.m.parameter === param))
			.filter((r) => !q || (r.c.label + ' ' + r.c.source_id + ' ' + r.c.class + ' ' + (r.c.platform ?? '')).toLowerCase().includes(q.toLowerCase()))
			.sort((a, b) => {
				const x = keyOf(a, sortKey), y = keyOf(b, sortKey);
				return x === y ? 0 : x < y ? -sortDir : sortDir;
			})
	);
	let sel = $derived(view?.components.find((c) => c.component_id === selId));
	function sortBy(k: string) {
		if (sortKey === k) sortDir = sortDir === 1 ? -1 : 1;
		else {
			sortKey = k;
			sortDir = 1;
		}
	}
	function select(id: string) {
		selId = id;
		history.replaceState(history.state, '', `#${encodeURIComponent(id)}`);
	}
	function onInput(v: string) {
		qLive = v;
		if (timer) clearTimeout(timer);
		timer = setTimeout(() => (q = v), 300);
	}
	const cols: [string, string, string][] = [
		['label', 'Component', 'Component label (source design)'],
		['parameter', 'Parameter', 'Registry parameter'],
		['value', 'Value', 'Reported value with qualifier / range'],
		['unit', 'Unit', ''],
		['wavelength', 'nm', 'Wavelength (or band)'],
		['scope', 'Scope', 'Loss scope'],
		['basis', 'Basis', 'measured, simulated, derived, ...'],
		['class', 'Class', 'class.subtype'],
		['platform', 'Platform', 'Waveguide platform'],
		['source_id', 'Source', 'Registry source id'],
		['locator', 'Loc', 'Page / figure / table in the source']
	];
</script>

{#if comp.error}
	<div class="err">{comp.error}</div>
{:else if view}
	<div class="page">
		<aside class="tree">
			<button class:on={!cls} onclick={() => ((cls = ''), (param = ''))}>All classes <span class="num">{view.components.length}</span></button>
			{#each Object.entries(view.classes) as [k, v]}
				<button class:on={cls === k} disabled={!classCounts[k]} onclick={() => ((cls = k), (param = ''))} data-tip={Object.values(v.subtypes).join('\n')}>
					{v.label} <span class="num">{classCounts[k] ?? ''}</span>
				</button>
			{/each}
		</aside>
		<div class="main">
			<div class="bar">
				<input type="search" placeholder="Search component, source, platform" value={qLive} oninput={(e) => onInput(e.currentTarget.value)} onkeydown={(e) => e.key === 'Enter' && (q = qLive)} />
				<select bind:value={param} data-tip="Filter by parameter"><option value="">all parameters</option>{#each params as p}<option>{p}</option>{/each}</select>
				<span class="muted num">{shown.length} / {rows.length} values</span>
			</div>
			<div class="scroll">
				<table class="t num">
					<thead><tr>{#each cols as [k, l, tip]}<th data-tip={tip} onclick={() => sortBy(k)}>{l}{sortKey === k ? (sortDir === 1 ? ' ^' : ' v') : ''}</th>{/each}</tr></thead>
					<tbody>
						{#each shown as r (r.m.metric_id)}
							<tr class:sel={r.c.component_id === selId} onclick={() => select(r.c.component_id)}>
								<td class="lbl" data-tip={r.c.label}>{r.c.label}</td>
								<td data-tip={view.parameters[r.m.parameter]?.def ?? ''}>{r.m.parameter}</td>
								<td class="r">{fmtValue(r.m)}</td>
								<td>{r.m.unit}</td>
								<td class="r">{fmtWavelength(r.m)}</td>
								<td>{r.m.scope ?? ''}</td>
								<td>{r.m.basis}</td>
								<td class="cls" data-tip={r.c.class}>{r.c.class}</td>
								<td>{r.c.platform ?? ''}</td>
								<td>{r.c.source_id}</td>
								<td data-tip={r.m.notes ?? ''}>{r.m.locator}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
		<aside class="detail">
			{#if sel}
				<h2>{sel.label}</h2>
				<dl>
					<dt>id</dt><dd class="mono">{sel.component_id}</dd>
					<dt>class</dt><dd>{sel.class}</dd>
					<dt>kind</dt><dd>{sel.row_kind}</dd>
					{#if sel.platform}<dt>platform</dt><dd>{sel.platform}</dd>{/if}
					{#if sel.core_material}<dt>core</dt><dd>{sel.core_material}</dd>{/if}
					{#if sel.cladding}<dt>cladding</dt><dd>{sel.cladding}</dd>{/if}
					{#if sel.fab_orgs.length}<dt>fab</dt><dd>{sel.fab_orgs.join(', ')}</dd>{/if}
					{#if sel.process_name}<dt>process</dt><dd>{sel.process_name}</dd>{/if}
					{#if sel.host_device_id}<dt>EO device</dt><dd class="mono">{sel.host_device_id}</dd>{/if}
					<dt>source</dt><dd>{#if sel.source.url}<a href={sel.source.url} target="_blank" rel="noopener">{sel.source.title}</a>{:else}{sel.source.title}{/if} <span class="muted">({sel.source.year}; {sel.source.access})</span></dd>
					<dt>verified</dt><dd>{sel.verified_on}</dd>
				</dl>
				{#if sel.notes}<p class="muted">{sel.notes}</p>{/if}
				{#if templateFor(sel.class, view.layouts)}
					<h3 class="lay">Layout <a href={link('/layout') + '?id=' + encodeURIComponent(sel.component_id)} data-tip="Full-size top view, cross-section and dimension table">full view</a></h3>
					<LayoutViews comp={sel} {view} compact />
				{/if}
				<h3>Values</h3>
				<table class="t num">
					<thead><tr><th>parameter</th><th class="r">value</th><th>unit</th><th>conditions</th><th>basis</th><th>loc</th></tr></thead>
					<tbody>
						{#each sel.metrics as m}
							<tr data-tip={[m.scope && 'scope ' + m.scope, m.includes && 'includes ' + m.includes, m.excludes && 'excludes ' + m.excludes, m.method && 'method ' + m.method, m.statistic && m.statistic + (m.n_samples ? ' n=' + m.n_samples : ''), m.notes].filter(Boolean).join('\n')}>
								<td>{m.parameter}</td><td class="r">{fmtValue(m)}</td><td>{m.unit}</td>
								<td>{[fmtWavelength(m) && fmtWavelength(m) + (m.wavelength_nm ? ' nm' : ''), m.polarization, m.temperature_k && m.temperature_k + ' K', m.bias_v && m.bias_v + ' V', m.ref_plane, m.condition].filter(Boolean).join(', ')}</td>
								<td>{m.basis}</td><td>{m.locator}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			{:else}
				<p class="muted">Select a value row.</p>
			{/if}
		</aside>
	</div>
{/if}

<style>
	.page { height: 100%; display: grid; grid-template-columns: 200px minmax(0, 1fr) 400px; grid-template-rows: minmax(0, 1fr); }
	.tree { min-height: 0; overflow: auto; border-right: 1px solid var(--border); background: var(--surface); padding: 4px; display: flex; flex-direction: column; gap: 1px; }
	.tree button { text-align: left; display: flex; justify-content: space-between; border: none; background: transparent; height: 22px; }
	.tree button.on { background: var(--sel); color: var(--ink); }
	.tree button:disabled { color: var(--ink-3); cursor: default; }
	.main { min-width: 0; min-height: 0; display: grid; grid-template-rows: auto minmax(0, 1fr); border-right: 1px solid var(--border); }
	.bar { display: flex; gap: 6px; align-items: center; padding: 6px 8px; background: var(--surface); border-bottom: 1px solid var(--border); }
	.bar input { flex: 1; }
	.scroll { overflow: auto; }
	table.t { border-collapse: collapse; width: 100%; }
	.t th, .t td { padding: 2px 6px; border-bottom: 1px solid var(--grid); text-align: left; white-space: nowrap; }
	.t th { position: sticky; top: 0; background: var(--surface); color: var(--ink-3); font-weight: 500; cursor: pointer; user-select: none; }
	.t .r { text-align: right; }
	.t td.lbl { max-width: 220px; overflow: hidden; text-overflow: ellipsis; }
	.t td.cls { max-width: 160px; overflow: hidden; text-overflow: ellipsis; }
	.t tbody tr { cursor: pointer; }
	.t tbody tr:hover { background: var(--hover); }
	.t tbody tr.sel { background: var(--sel); }
	.detail { min-height: 0; overflow: auto; padding: 8px 10px; background: var(--surface); }
	.detail .t th { position: static; cursor: default; }
	.detail .t td { white-space: normal; }
	.detail .t td:nth-child(4) { min-width: 140px; }
	h2 { margin: 0 0 6px; font-size: 14px; }
	h3.lay { display: flex; justify-content: space-between; }
	h3.lay a { text-transform: none; letter-spacing: 0; font-weight: 400; }
	h3 { margin: 10px 0 4px; font-size: 11px; color: var(--ink-3); font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }
	dl { display: grid; grid-template-columns: 80px 1fr; gap: 2px 8px; margin: 0; }
	dt { color: var(--ink-3); }
	dd { margin: 0; overflow-wrap: anywhere; }
	.err { padding: 12px; color: var(--crit); }
	@media (max-width: 1100px) { .page { grid-template-columns: 160px minmax(0, 1fr); } .detail { display: none; } }
</style>
