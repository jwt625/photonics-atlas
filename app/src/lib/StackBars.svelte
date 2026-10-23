<script lang="ts">
	// Stacked bars per year (supply vendor share, people coverage; DevLog-010 D194, D197). Data only: no title, axis
	// titles with units, integer ticks, legend inside the plot, lin / log y toggle.
	import Frame from './explore/Frame.svelte';
	import Plot from './explore/Plot.svelte';
	import { ui } from './state.svelte';
	import { plotTheme } from './explore/colors';

	interface Series {
		key: string;
		name: string;
		color: string;
		y: number[];
	}
	let {
		letter,
		desc,
		badge = '',
		badgeTip = '',
		years,
		series,
		xTitle = 'Publication year',
		yTitle,
		unit,
		height = 260,
		legend = true
	}: { letter: string; desc: string; badge?: string; badgeTip?: string; years: number[]; series: Series[]; xTitle?: string; yTitle: string; unit: string; height?: number; legend?: boolean } = $props();

	let yLog = $state(false);
	const th = $derived(plotTheme(ui.theme));
	const traces = $derived(
		series.map((s) => ({
			type: 'bar',
			name: s.name,
			x: years,
			y: s.y.map((v) => (yLog && v === 0 ? null : v)),
			marker: { color: s.color, line: { color: th.surface, width: 1 } },
			hovertemplate: `${s.name.replace(/%/g, '%%')}<br>%{x}: %{y} ${unit}<extra></extra>`,
			textposition: 'none'
		}))
	);
	const layout = $derived({
		uirevision: 's',
		barmode: yLog ? 'group' : 'stack',
		bargap: 0.3,
		paper_bgcolor: 'rgba(0,0,0,0)',
		plot_bgcolor: 'rgba(0,0,0,0)',
		margin: { l: 44, r: 8, t: 6, b: 6 },
		font: { family: 'system-ui, sans-serif', size: 11, color: th.ink2 },
		showlegend: legend,
		// legend above the plot area (Plotly expands the top margin), never over the bars (audit 2026-10-23 #17)
		legend: { orientation: 'h', x: 0, xanchor: 'left', y: 1.0, yanchor: 'bottom', bgcolor: 'rgba(0,0,0,0)', font: { size: 10, color: th.ink2 }, traceorder: 'normal' },
		hoverlabel: { bgcolor: th.surface, bordercolor: th.line, font: { color: th.ink, size: 11 } },
		xaxis: { title: { text: xTitle, standoff: 4, font: { size: 11, color: th.ink2 } }, dtick: 1, tickformat: 'd', gridcolor: th.grid, linecolor: th.line, tickfont: { size: 10 }, automargin: true, zeroline: false },
		yaxis: {
			title: { text: yTitle, standoff: 4, font: { size: 11, color: th.ink2 } },
			type: yLog ? 'log' : 'linear',
			gridcolor: th.grid,
			linecolor: th.line,
			tickfont: { size: 10 },
			automargin: true,
			zeroline: false,
			...(yLog ? { dtick: 1 } : { rangemode: 'tozero', tickformat: 'd' })
		}
	});
</script>

<Frame {letter} {desc} {badge} {badgeTip} {height}>
	{#snippet controls()}
		<span class="seg" data-tip="y axis scale (log: bars side by side, not stacked)">
			<button class:on={!yLog} onclick={() => (yLog = false)}>y lin</button><button class:on={yLog} onclick={() => (yLog = true)}>y log</button>
		</span>
	{/snippet}
	{#if years.length}
		<Plot data={traces} {layout} />
	{:else}
		<div class="empty muted">no rows</div>
	{/if}
</Frame>

<style>
	.empty {
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>
