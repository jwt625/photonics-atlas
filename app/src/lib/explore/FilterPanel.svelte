<script lang="ts">
	// Explore filter side panel (structure and look of the sibling atlases' FilterPanel.svelte).
	import type { Component } from '../components.svelte';
	import { FAMILIES, GROUP_ORDER, familyLabel } from './colors';
	import { classFamily, countBy, familyOf, pubTypeOf, yearOf } from './logic';
	import { exFilters, resetExFilters } from './state.svelte';

	let { all, nShown, familyName }: { all: Component[]; nShown: number; familyName: (f: string) => string } = $props();

	let mobileOpen = $state(false);
	const open = $state<Record<string, boolean>>({ cls: true, plat: true, basis: true, src: true });

	type Opt = { value: string; label: string; n: number; tip: string };
	const classOpts = $derived.by<Opt[]>(() =>
		[...countBy(all, classFamily).entries()]
			.sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
			.map(([value, n]) => ({ value, label: familyName(value), n, tip: `${familyName(value)} (${value}): ${n} components` }))
	);
	const famOpts = $derived.by<Opt[]>(() => {
		const c = countBy(all, familyOf);
		return GROUP_ORDER.filter((g) => c.has(g)).map((g) => {
			const f = FAMILIES.find((x) => x.key === g);
			const tip = f ? `${f.label}: platform ${f.platforms.join(', ')}` : 'Other / unspecified: platform other, plasmonic_mim, al2o3, or not stated';
			return { value: g, label: familyLabel(g), n: c.get(g) ?? 0, tip };
		});
	});
	const typeOpts = $derived.by<Opt[]>(() =>
		[...countBy(all, pubTypeOf).entries()]
			.sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
			.map(([value, n]) => ({ value, label: value, n, tip: `${value}: ${n} components` }))
	);
	const yearBounds = $derived.by(() => {
		const ys = all.map(yearOf).filter((y): y is number => y !== null);
		return ys.length ? { min: Math.min(...ys), max: Math.max(...ys) } : { min: 0, max: 0 };
	});

	function toggle(list: string[], v: string): string[] {
		return list.includes(v) ? list.filter((x) => x !== v) : [...list, v];
	}
	function num(v: string): number | null {
		const n = Number(v);
		return v.trim() === '' || !Number.isFinite(n) ? null : Math.round(n);
	}
	const active = $derived(
		!!(exFilters.classes.length || exFilters.families.length || exFilters.pubTypes.length || exFilters.measuredOnly || exFilters.yearMin !== null || exFilters.yearMax !== null)
	);
</script>

{#snippet group(id: string, lbl: string, body: import('svelte').Snippet)}
	<section>
		<button class="gh" onclick={() => (open[id] = !open[id])} aria-expanded={open[id]}>
			<svg viewBox="0 0 10 10" width="8" height="8" class:rot={open[id]} aria-hidden="true"><path d="M3 1 L7 5 L3 9" fill="none" stroke="currentColor" stroke-width="1.5" /></svg>
			{lbl}
		</button>
		{#if open[id]}<div class="gb">{@render body()}</div>{/if}
	</section>
{/snippet}

{#snippet checks(list: Opt[], sel: string[], key: 'classes' | 'families' | 'pubTypes', tall: boolean)}
	<div class="checks" class:tall>
		{#each list as o (o.value)}
			<label data-tip={o.tip}>
				<input type="checkbox" checked={sel.includes(o.value)} onchange={() => (exFilters[key] = toggle(sel, o.value))} />
				<span class="lbl">{o.label}</span>
				<span class="n num">{o.n}</span>
			</label>
		{/each}
	</div>
{/snippet}

<aside class:mopen={mobileOpen}>
	<div class="top">
		<span class="muted num" data-tip="Components passing the filters">{nShown} shown</span>
		<span class="tb">
			<button class="mtoggle" onclick={() => (mobileOpen = !mobileOpen)} aria-expanded={mobileOpen} data-tip="Show or hide the filters">Filters{active ? ' *' : ''}</button>
			<button onclick={resetExFilters} disabled={!active} data-tip="Clear all filters">Reset</button>
		</span>
	</div>
	<div class="scroll">
		{#snippet clsBody()}
			{@render checks(classOpts, exFilters.classes, 'classes', true)}
		{/snippet}
		{@render group('cls', 'Class', clsBody)}

		{#snippet platBody()}
			{@render checks(famOpts, exFilters.families, 'families', false)}
		{/snippet}
		{@render group('plat', 'Platform family', platBody)}

		{#snippet basisBody()}
			<span class="seg" data-tip="Measured only: keeps measured performance values (ring radius, a geometry dimension, keeps any basis) and drops components without a measured value">
				<button class:on={!exFilters.measuredOnly} onclick={() => (exFilters.measuredOnly = false)}>all</button><button class:on={exFilters.measuredOnly} onclick={() => (exFilters.measuredOnly = true)}>measured only</button>
			</span>
		{/snippet}
		{@render group('basis', 'Basis', basisBody)}

		{#snippet srcBody()}
			<div class="sub">Publication type</div>
			{@render checks(typeOpts, exFilters.pubTypes, 'pubTypes', false)}
			<div class="sub">Publication year</div>
			<div class="yr">
				<input type="number" placeholder={String(yearBounds.min)} value={exFilters.yearMin ?? ''} onchange={(e) => (exFilters.yearMin = num(e.currentTarget.value))} data-tip="Earliest publication year" />
				<span class="muted">to</span>
				<input type="number" placeholder={String(yearBounds.max)} value={exFilters.yearMax ?? ''} onchange={(e) => (exFilters.yearMax = num(e.currentTarget.value))} data-tip="Latest publication year" />
			</div>
		{/snippet}
		{@render group('src', 'Publication', srcBody)}
	</div>
</aside>

<style>
	aside {
		display: flex;
		flex-direction: column;
		min-height: 0;
		height: 100%;
		background: var(--surface);
		border-right: 1px solid var(--border);
		width: 100%;
	}
	.top {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 6px 8px;
		border-bottom: 1px solid var(--border);
		flex: none;
		height: 36px;
	}
	.scroll {
		overflow-y: auto;
		flex: 1;
		min-height: 0;
	}
	.tb {
		display: flex;
		gap: 4px;
	}
	.mtoggle {
		display: none;
	}
	@media (max-width: 720px) {
		aside {
			height: auto;
			border-right: 0;
			border-bottom: 1px solid var(--border);
		}
		.mtoggle {
			display: inline-block;
		}
		.scroll {
			display: none;
		}
		aside.mopen .scroll {
			display: block;
			max-height: 55vh;
		}
	}
	section {
		border-bottom: 1px solid var(--border);
	}
	.gh {
		width: 100%;
		text-align: left;
		display: flex;
		align-items: center;
		gap: 6px;
		background: transparent;
		border: 0;
		height: 26px;
		padding: 0 8px;
		color: var(--ink-2);
		text-transform: uppercase;
		letter-spacing: 0.06em;
		font-size: 10px;
	}
	.gh svg {
		transition: transform 0.1s;
	}
	.gh svg.rot {
		transform: rotate(90deg);
	}
	.gb {
		padding: 2px 8px 8px;
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
	.sub {
		color: var(--ink-3);
		font-size: 10px;
		margin-top: 4px;
	}
	.checks {
		display: flex;
		flex-direction: column;
		max-height: 170px;
		overflow-y: auto;
	}
	.checks.tall {
		max-height: 260px;
	}
	label {
		display: flex;
		align-items: center;
		gap: 6px;
		padding: 1px 2px;
		cursor: pointer;
	}
	label:hover {
		background: var(--hover);
	}
	.lbl {
		flex: 1;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.n {
		color: var(--ink-3);
	}
	.yr {
		display: flex;
		align-items: center;
		gap: 6px;
	}
	.yr input {
		width: 64px;
	}
	.seg {
		display: inline-flex;
	}
	.seg button {
		height: 20px;
		font-size: 10px;
		padding: 0 6px;
	}
</style>
