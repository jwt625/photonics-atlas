<script lang="ts">
	// Atlas overview (DevLog-010 D199l): every number comes from registry.json `overview`, computed by build_views.py.
	import { link } from '../lib/paths';
	import { store, ui } from '../lib/state.svelte';
	import { slotColor } from '../lib/explore/colors';
	import StackBars from '../lib/StackBars.svelte';

	let reg = $derived(store.reg);
	let ov = $derived(reg?.overview);
	const name = (id: string) => store.byId.get(id)?.name ?? id;
	const hub = (id: string) => link('/orgs/hub') + '?id=' + encodeURIComponent(id);
	let types = $derived(ov ? Object.entries(ov.orgs.by_type).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])) : []);
	let tmax = $derived(types.length ? types[0][1] : 1);
	let fmax = $derived(ov?.top_fabs.length ? ov.top_fabs[0][1] : 1);
	let vmax = $derived(ov?.top_vendors.length ? ov.top_vendors[0][1] : 1);
	// publication types in alphabetical order keep their colour slot (identity, not rank)
	let pubSeries = $derived(
		ov ? Object.keys(ov.publications.by_type).sort().map((t, i) => ({ key: t, name: t, color: slotColor(i, ui.theme), y: ov.publications.by_type[t] })) : []
	);
	let pubTotal = $derived(ov ? ov.publications.n : 0);
	let tiles = $derived(
		ov
			? [
					{ v: ov.components.n, k: 'components', href: '/components', tip: `${ov.components.classes} component classes in ${ov.components.class_families} families` },
					{ v: ov.values.n, k: 'values', href: '/explore', tip: `${ov.values.measured} measured; the rest simulated, design targets or derived` },
					{ v: ov.components.platforms, k: 'platforms', href: '/explore', tip: 'distinct waveguide platforms of the components' },
					{ v: ov.components.publications, k: 'component papers', href: '/components', tip: 'publications the component values come from' },
					{ v: ov.components.years.length ? `${ov.components.years[0]}-${ov.components.years[1]}` : '', k: 'years', href: '/explore', tip: 'publication years of the component papers' },
					{ v: ov.orgs.n, k: 'organizations', href: '/orgs', tip: 'companies, universities, institutes, foundries and facilities' },
					{ v: ov.people.persons, k: 'people', href: '/people', tip: `${ov.people.affiliations} published affiliations in ${ov.people.publications} publications` },
					{ v: ov.supply.vendors, k: 'vendors', href: '/supply', tip: `vendors of wafers, foundry runs, instruments, software and materials (shared cleanrooms not counted); ${ov.supply.usage} stated uses in all` },
					{ v: ov.supply.products, k: 'products', href: '/supply', tip: 'instrument, tool and material models named in the papers' },
					{ v: ov.supply.tests, k: 'reliability tests', href: '/supply#tab=standards', tip: `${ov.supply.standards} cited standards` }
				]
			: []
	);
</script>

{#if reg && ov}
	<div class="dash">
		<section class="tiles">
			{#each tiles as t}
				<a class="tile" href={link(t.href)} data-tip={t.tip}><div class="v num">{t.v}</div><div class="k">{t.k}</div></a>
			{/each}
		</section>

		<section class="chart">
			<StackBars
				letter="a"
				desc="Publications cited by the atlas (component values, supply facts, author affiliations) per publication year, stacked by publication type"
				badge={`${pubTotal - ov.publications.no_year}/${pubTotal}`}
				badgeTip={`${pubTotal - ov.publications.no_year} of ${pubTotal} publications have a year`}
				years={ov.publications.years}
				series={pubSeries}
				yTitle="Publications (count)"
				unit="publications"
				height={300}
			/>
		</section>

		<section class="panel">
			<h2>Organizations by type</h2>
			{#each types as [t, n]}
				<div class="bar" data-tip="{n} organizations of type {t}">
					<span class="lbl">{t.replace(/_/g, ' ')}</span><span class="track"><span class="fill" style:width="{(100 * n) / tmax}%"></span></span><span class="num">{n}</span>
				</div>
			{/each}
		</section>

		<section class="panel">
			<h2>Fabricating organizations <span class="muted">components</span></h2>
			{#each ov.top_fabs as [id, n]}
				<div class="bar" data-tip="{n} components whose publication states {name(id)} fabricated them">
					<a class="lbl" href={hub(id)}>{name(id)}</a><span class="track"><span class="fill" style:width="{(100 * n) / fmax}%"></span></span><span class="num">{n}</span>
				</div>
			{/each}
		</section>

		<section class="panel">
			<h2>Vendors <span class="muted">stated uses</span></h2>
			{#each ov.top_vendors as [id, n]}
				<div class="bar" data-tip="{n} stated uses of {name(id)} (wafers, foundry runs, instruments, materials; shared cleanrooms not counted)">
					<a class="lbl" href={hub(id)}>{name(id)}</a><span class="track"><span class="fill" style:width="{(100 * n) / vmax}%"></span></span><span class="num">{n}</span>
				</div>
			{/each}
		</section>
	</div>
{/if}

<style>
	.dash { height: 100%; overflow: auto; padding: 10px; display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); grid-auto-rows: max-content; gap: 10px; align-content: start; }
	.tiles { grid-column: 1 / -1; display: flex; gap: 8px; flex-wrap: wrap; }
	.tile { background: var(--surface); border: 1px solid var(--border); padding: 6px 10px; min-width: 104px; color: var(--ink); }
	.tile:hover { text-decoration: none; border-color: var(--accent); }
	.tile .v { font-size: 20px; font-weight: 600; }
	.tile .k { color: var(--ink-3); font-size: 11px; }
	.chart { grid-column: 1 / -1; min-width: 0; }
	.panel { background: var(--surface); border: 1px solid var(--border); padding: 8px 10px; min-width: 0; }
	h2 { margin: 0 0 6px; font-size: 12px; font-weight: 600; color: var(--ink-2); }
	h2 .muted { font-weight: 400; font-size: 11px; }
	.bar { display: grid; grid-template-columns: minmax(0, 190px) 1fr 40px; gap: 6px; align-items: center; height: 18px; }
	.bar .lbl { color: var(--ink-2); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
	.bar a.lbl { color: var(--accent); }
	.bar .track { height: 10px; background: var(--grid); }
	.bar .fill { display: block; height: 100%; background: var(--accent); }
	.bar .num { text-align: right; }
	@media (max-width: 700px) { .dash { grid-template-columns: minmax(0, 1fr); } }
</style>
