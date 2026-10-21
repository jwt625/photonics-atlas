<script lang="ts">
	// Class x platform-family component counts (adapted from the sibling HeatChart.svelte).
	import Frame from './Frame.svelte';
	import Plot from './Plot.svelte';
	import { ui } from '../state.svelte';
	import { familyLabel, plotTheme } from './colors';
	import { classPlatformMatrix } from './logic';
	import type { Component } from '../components.svelte';

	let { comps, rowName }: { comps: Component[]; rowName: (key: string) => string } = $props();
	let level = $state<'family' | 'subtype'>('family');
	const th = $derived(plotTheme(ui.theme));
	const m = $derived(classPlatformMatrix(comps, level));
	const cols = $derived(m.cols.map(familyLabel));
	const rows = $derived(m.rows.map(rowName));
	const height = $derived(Math.max(240, m.rows.length * 18 + 70));
	const zMax = $derived(Math.max(1, ...m.z.flat()));

	const traces = $derived([
		{
			type: 'heatmap',
			z: m.z.map((r) => r.map((v) => (v === 0 ? null : v))),
			x: cols,
			y: rows,
			colorscale: [
				[0, th.grid],
				[1, th.accent]
			],
			zmin: 0,
			zmax: zMax,
			xgap: 2,
			ygap: 2,
			showscale: false,
			texttemplate: '%{z}',
			textfont: { size: 10, color: th.ink },
			hovertemplate: '%{y}<br>%{x}: %{z} components<extra></extra>',
			hoverongaps: false
		}
	]);
	const layout = $derived({
		paper_bgcolor: 'rgba(0,0,0,0)',
		plot_bgcolor: 'rgba(0,0,0,0)',
		margin: { l: 8, r: 8, t: 8, b: 8 },
		font: { family: 'system-ui, sans-serif', size: 10, color: th.ink2 },
		showlegend: false,
		hoverlabel: { bgcolor: th.surface, bordercolor: th.line, font: { color: th.ink, size: 11 } },
		xaxis: { side: 'top', tickfont: { size: 10, color: th.ink2 }, automargin: true, linecolor: th.line, showgrid: false, type: 'category' },
		yaxis: { autorange: 'reversed', tickfont: { size: 10, color: th.ink }, automargin: true, linecolor: th.line, showgrid: false, type: 'category' }
	});
</script>

<Frame
	letter="l"
	desc="Component count per class (family or class.subtype) and platform family; empty cell = no component. Platform family mapping of the platform enum in the filter panel tooltip."
	height={Math.min(760, height + 30)}
	badge={`${comps.length}`}
	badgeTip="components in the current filter"
>
	{#snippet controls()}
		<span class="seg" data-tip="Row level">
			<button class:on={level === 'family'} onclick={() => (level = 'family')}>class family</button><button class:on={level === 'subtype'} onclick={() => (level = 'subtype')}>class.subtype</button>
		</span>
	{/snippet}
	<div class="sc">
		{#if m.rows.length}
			<div style="height:{height}px"><Plot data={traces} {layout} /></div>
		{:else}
			<div class="empty muted">no component in the filter</div>
		{/if}
	</div>
</Frame>

<style>
	.sc {
		height: 100%;
		overflow: auto;
	}
	.empty {
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>
