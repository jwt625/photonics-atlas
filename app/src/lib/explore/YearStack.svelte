<script lang="ts">
	// Adapted from the sibling atlases (YearStack.svelte): components per source year, stacked by class family.
	import Frame from './Frame.svelte';
	import Plot from './Plot.svelte';
	import { ui } from '../state.svelte';
	import { classColor, plotTheme } from './colors';
	import { CLASS_OTHER, yearStack } from './logic';
	import type { Component } from '../components.svelte';

	let { comps, familyName }: { comps: Component[]; familyName: (f: string) => string } = $props();
	const th = $derived(plotTheme(ui.theme));
	const data = $derived(yearStack(comps));
	const label = (g: string) => (g === CLASS_OTHER ? 'Other classes' : familyName(g));

	const traces = $derived(
		data.groups.map((g) => ({
			type: 'bar',
			name: label(g),
			x: data.years,
			y: data.years.map((yt) => data.counts.get(g)?.get(yt) ?? 0),
			marker: { color: classColor(g, ui.theme), line: { color: th.surface, width: 2 } },
			hovertemplate: `${label(g)}<br>%{x}: %{y} components<extra></extra>`,
			textposition: 'none'
		}))
	);
	const yMax = $derived(Math.max(1, ...data.years.map((yt) => data.groups.reduce((t, g) => t + (data.counts.get(g)?.get(yt) ?? 0), 0))));
	let ySpan = $state<number | null>(null);
	function onrelayout(e: any) {
		if (!e) return;
		if (e['yaxis.autorange']) ySpan = null;
		else if (typeof e['yaxis.range[0]'] === 'number' && typeof e['yaxis.range[1]'] === 'number') ySpan = Math.abs(e['yaxis.range[1]'] - e['yaxis.range[0]']);
		else if (Array.isArray(e['yaxis.range'])) ySpan = Math.abs(e['yaxis.range'][1] - e['yaxis.range'][0]);
	}
	const yDtick = $derived.by(() => {
		const raw = (ySpan ?? yMax * 1.05) / 6;
		if (raw <= 1) return 1;
		const p = 10 ** Math.floor(Math.log10(raw));
		const f = raw / p;
		return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10) * p;
	});
	const layout = $derived({
		uirevision: 'g',
		barmode: 'stack',
		bargap: 0.35,
		paper_bgcolor: 'rgba(0,0,0,0)',
		plot_bgcolor: 'rgba(0,0,0,0)',
		margin: { l: 44, r: 12, t: 8, b: 8 },
		font: { family: 'system-ui, sans-serif', size: 11, color: th.ink2 },
		showlegend: true,
		legend: { orientation: 'v', x: 0.01, xanchor: 'left', y: 0.99, yanchor: 'top', bgcolor: 'rgba(0,0,0,0)', font: { size: 10, color: th.ink2 }, traceorder: 'normal' },
		hoverlabel: { bgcolor: th.surface, bordercolor: th.line, font: { color: th.ink, size: 11 } },
		xaxis: { title: { text: 'Publication year', standoff: 4, font: { size: 11, color: th.ink2 } }, dtick: 1, tickformat: 'd', gridcolor: th.grid, linecolor: th.line, tickfont: { size: 10 }, automargin: true, zeroline: false },
		yaxis: { title: { text: 'Components (count)', standoff: 4, font: { size: 11, color: th.ink2 } }, gridcolor: th.grid, linecolor: th.line, tickfont: { size: 10 }, rangemode: 'tozero', dtick: yDtick, tickformat: 'd', automargin: true, zeroline: false }
	});
	const total = $derived(comps.length);
</script>

<Frame
	letter="j"
	desc="Components per source publication year, stacked by class family (the seven largest families keep a fixed colour; the rest fold into Other classes). Colours here mean class family, not platform."
	badge={`${total - data.noYear}/${total}`}
	badgeTip={`${total - data.noYear} of ${total} components in the filter plotted; ${data.noYear} without a publication year`}
>
	{#snippet controls()}<span class="tag" data-tip="Colours in this panel encode class family, not platform family (page legend)">colour = class family</span>{/snippet}
	{#if data.years.length}
		<Plot data={traces} {layout} {onrelayout} />
	{:else}
		<div class="empty muted">no component in the filter</div>
	{/if}
</Frame>

<style>
	.tag {
		font-size: 10px;
		color: var(--ink-3);
		border: 1px solid var(--line);
		padding: 0 4px;
	}
	.empty {
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>
