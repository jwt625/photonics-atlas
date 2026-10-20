<script lang="ts">
	import { link } from '../lib/paths';
	import { store } from '../lib/state.svelte';

	const CORPUS_LABEL: Record<string, string> = {
		eo: 'EO modulator atlas (org names + author affiliations)',
		pk: 'Advanced packaging atlas (org names + author affiliations)',
		lin: 'Photonics lineage (org records)',
		ofc2026: 'OFC 2026 presentation metadata (author affiliations)'
	};
	const pct = (a: number, b: number) => (b ? ((100 * a) / b).toFixed(1) : '100.0');
	let reg = $derived(store.reg);
	let types = $derived(reg ? Object.entries(reg.org_types).sort((a, b) => b[1] - a[1]) : []);
	let tmax = $derived(types.length ? types[0][1] : 1);
	let accesses = $derived(reg ? [...new Set(Object.values(reg.sources_by_corpus).flatMap((v) => Object.keys(v)))].sort() : []);
	let topOfc = $derived(reg ? [...reg.orgs].sort((a, b) => (b.rows.ofc2026 ?? 0) - (a.rows.ofc2026 ?? 0)).slice(0, 25) : []);
</script>

{#if reg}
	<div class="dash">
		<section class="tiles">
			{#each [['organizations', 'Organizations in the registry'], ['aliases', 'Curated alias rows'], ['events', 'Org events (acquisition, rename, spin-off, merger)'], ['sources', 'Source documents across corpora'], ['sources_duplicate', 'Source rows marked same_as another row']] as [k, tip]}
				<div class="tile" data-tip={tip}><div class="v num">{reg.counts[k]}</div><div class="k">{k.replace('_', ' ')}</div></div>
			{/each}
		</section>

		<section class="panel wide">
			<h2>Crosswalk coverage</h2>
			<table class="grid num">
				<thead><tr><th>corpus</th><th>strings</th><th>mapped</th><th>rows</th><th>mapped</th><th>row %</th><th>by name</th><th>by alias</th><th>by ROR</th><th>unmapped</th></tr></thead>
				<tbody>
					{#each Object.entries(reg.coverage) as [c, v]}
						<tr>
							<td data-tip={CORPUS_LABEL[c] ?? c}>{c}</td>
							<td>{v.strings}</td><td>{v.strings_mapped}</td><td>{v.rows}</td><td>{v.rows_mapped}</td>
							<td class:ok={v.rows_mapped / v.rows >= 0.9}>{pct(v.rows_mapped, v.rows)}</td>
							<td>{v.by_basis.name ?? 0}</td><td>{v.by_basis.alias ?? 0}</td><td>{v.by_basis.ror ?? 0}</td><td>{v.by_basis.unmapped ?? 0}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</section>

		<section class="panel">
			<h2>Org types</h2>
			{#each types as [t, n]}
				<div class="bar" data-tip="{n} organizations of type {t}">
					<span class="lbl">{t}</span><span class="track"><span class="fill" style:width="{(100 * n) / tmax}%"></span></span><span class="num">{n}</span>
				</div>
			{/each}
		</section>

		<section class="panel">
			<h2>Sources by corpus and access</h2>
			<table class="grid num">
				<thead><tr><th>corpus</th>{#each accesses as a}<th>{a}</th>{/each}</tr></thead>
				<tbody>
					{#each Object.entries(reg.sources_by_corpus) as [c, v]}
						<tr><td>{c}</td>{#each accesses as a}<td>{v[a] ?? ''}</td>{/each}</tr>
					{/each}
				</tbody>
			</table>
		</section>

		<section class="panel wide">
			<h2>Most frequent OFC 2026 affiliations (author rows)</h2>
			<table class="grid num">
				<thead><tr><th>organization</th><th>type</th><th>country</th><th>OFC rows</th><th>EO rows</th><th>PK rows</th></tr></thead>
				<tbody>
					{#each topOfc as o}
						<tr>
							<td><a href={link('/orgs') + '#' + o.id}>{o.name}</a></td><td>{o.type}</td><td>{o.country}</td>
							<td>{o.rows.ofc2026 ?? ''}</td><td>{o.rows.eo ?? ''}</td><td>{o.rows.pk ?? ''}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</section>
	</div>
{/if}

<style>
	.dash { height: 100%; overflow: auto; padding: 10px; display: grid; grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); grid-auto-rows: max-content; gap: 10px; align-content: start; }
	.tiles { grid-column: 1 / -1; display: flex; gap: 10px; flex-wrap: wrap; }
	.tile { background: var(--surface); border: 1px solid var(--border); padding: 8px 12px; min-width: 120px; }
	.tile .v { font-size: 22px; font-weight: 600; }
	.tile .k { color: var(--ink-3); font-size: 11px; }
	.panel { background: var(--surface); border: 1px solid var(--border); padding: 8px 10px; min-width: 0; overflow-x: auto; }
	.panel.wide { grid-column: 1 / -1; }
	h2 { margin: 0 0 6px; font-size: 12px; font-weight: 600; color: var(--ink-2); }
	table.grid { border-collapse: collapse; width: 100%; }
	.grid th, .grid td { text-align: right; padding: 2px 6px; border-bottom: 1px solid var(--grid); white-space: nowrap; }
	.grid th:first-child, .grid td:first-child { text-align: left; }
	.grid th { color: var(--ink-3); font-weight: 500; }
	.ok { color: var(--good); }
	.bar { display: grid; grid-template-columns: 130px 1fr 40px; gap: 6px; align-items: center; height: 18px; }
	.bar .lbl { color: var(--ink-2); }
	.bar .track { height: 10px; background: var(--grid); }
	.bar .fill { display: block; height: 100%; background: var(--accent); }
	.bar .num { text-align: right; }
</style>
