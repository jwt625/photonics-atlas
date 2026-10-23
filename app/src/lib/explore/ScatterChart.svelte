<script lang="ts">
	// Adapted from the advanced-packaging / EO modulator atlases (ScatterChart.svelte): lettered panel, plotted / total
	// badge with the omitted breakdown, lin / log toggles, hover card, click to pin, click empty space to unpin.
	import type { Snippet } from 'svelte';
	import Plot from './Plot.svelte';
	import PointTip from './PointTip.svelte';
	import { ui } from '../state.svelte';
	import { groupColor, plotTheme, GROUP_ORDER } from './colors';
	import { logDtick, type Omitted, type Pt } from './logic';

	interface PanelSpec {
		pts: Pt[];
		yTitle: string;
		/** short label drawn in the panel corner when the chart is split (e.g. "grating") */
		tag?: string;
	}
	interface Props {
		letter: string;
		desc: string;
		panels: PanelSpec[];
		xTitle: string;
		xLog?: boolean;
		yLog?: boolean;
		allowX?: boolean;
		allowY?: boolean;
		omitted: Omitted;
		/** what the total counts, e.g. "grating and edge couplers" */
		unit: string;
		classLabel: (cls: string) => string;
		xTickvals?: number[];
		xTicktext?: string[];
		extraTraces?: unknown[];
		xRange?: [number, number];
		emptyText?: string;
		headerExtra?: Snippet;
		wide?: boolean;
	}
	let {
		letter,
		desc,
		panels,
		xTitle,
		xLog = $bindable(false),
		yLog = $bindable(false),
		allowX = true,
		allowY = true,
		omitted,
		unit,
		classLabel,
		xTickvals,
		xTicktext,
		extraTraces = [],
		xRange,
		emptyText = 'no component in the filter reports both values',
		headerExtra,
		wide = false
	}: Props = $props();

	const th = $derived(plotTheme(ui.theme));
	const nPan = $derived(panels.length);
	const yName = (panel: number) => (nPan === 1 ? 'yaxis' : panel === 0 ? 'yaxis2' : 'yaxis');
	const yRef = (panel: number) => (nPan === 1 ? 'y' : panel === 0 ? 'y2' : 'y');

	interface Pin {
		id: string;
		panel: number;
	}
	let pins = $state<Pin[]>([]);
	let hover = $state<{ key: string; x: number; y: number } | null>(null);
	let wrap: HTMLDivElement;
	let gdEl: any = $state(null);

	const ptIndex = $derived.by(() => {
		const m = new Map<string, Pt>();
		for (const p of panels) for (const pt of p.pts) m.set(`${pt.panel}|${pt.id}`, pt);
		return m;
	});

	$effect(() => {
		const keep = pins.filter((p) => ptIndex.has(`${p.panel}|${p.id}`));
		if (keep.length !== pins.length) pins = keep;
	});

	function symbolFor(p: Pt): string {
		if (p.qy === 'lt') return 'arrow-bar-down';
		if (p.qy === 'gt') return 'arrow-bar-up';
		if (p.qx === 'lt') return 'arrow-bar-left';
		if (p.qx === 'gt') return 'arrow-bar-right';
		return p.sim ? 'diamond' : 'circle';
	}

	const traces = $derived.by(() => {
		const out: any[] = [];
		panels.forEach((panel, pi) => {
			const ax = { xaxis: 'x', yaxis: yRef(pi) };
			for (const g of GROUP_ORDER) {
				const pts = panel.pts.filter((p) => p.group === g);
				if (!pts.length) continue;
				const color = groupColor(g, ui.theme);
				out.push({
					type: 'scatter',
					mode: 'markers',
					x: pts.map((p) => p.x),
					y: pts.map((p) => p.y),
					customdata: pts.map((p) => p.id),
					meta: pi,
					marker: { color, size: pts.map((p) => (symbolFor(p).startsWith('arrow') ? 13 : 10)), symbol: pts.map(symbolFor), line: { color: th.surface, width: 1.5 } },
					hoverinfo: 'none',
					showlegend: false,
					...ax
				});
			}
		});
		for (const t of extraTraces) out.push(t);
		const ringsByPanel = new Map<number, Pt[]>();
		for (const p of pins) {
			const pt = ptIndex.get(`${p.panel}|${p.id}`);
			if (pt) ringsByPanel.set(p.panel, [...(ringsByPanel.get(p.panel) ?? []), pt]);
		}
		for (const [pi, pts] of ringsByPanel) {
			out.push({ type: 'scatter', mode: 'markers', x: pts.map((p) => p.x), y: pts.map((p) => p.y), marker: { symbol: 'circle-open', size: 18, color: th.ink, line: { color: th.ink, width: 1.5 } }, hoverinfo: 'skip', showlegend: false, xaxis: 'x', yaxis: yRef(pi) });
		}
		return out;
	});

	const layout = $derived.by(() => {
		const axBase = {
			gridcolor: th.grid,
			gridwidth: 1,
			linecolor: th.line,
			zeroline: false,
			ticks: 'outside',
			tickcolor: th.line,
			tickfont: { size: 10, color: th.ink2 },
			automargin: true,
			showline: true,
			mirror: false,
			exponentformat: 'power',
			// an empty panel shows only its message, no placeholder axes
			visible: omitted.plotted > 0
		};
		const title = (t: string) => ({ text: t, standoff: 4, font: { size: 11, color: th.ink2 } });
		// UI audit 20: log axes label 1 / 2 / 5 per decade (or decades only), not every minor tick
		const yTicks = (pi: number) => (yLog ? { dtick: logDtick(panels[pi]?.pts.map((t) => t.y) ?? []) } : {});
		const l: Record<string, any> = {
			paper_bgcolor: 'rgba(0,0,0,0)',
			plot_bgcolor: 'rgba(0,0,0,0)',
			margin: { l: 52, r: 12, t: 8, b: 8 },
			font: { family: 'system-ui, -apple-system, Segoe UI, sans-serif', size: 11, color: th.ink2 },
			showlegend: false,
			hovermode: 'closest',
			hoverdistance: 28,
			dragmode: 'zoom',
			xaxis: {
				...axBase,
				title: title(xTitle),
				type: xLog ? 'log' : 'linear',
				...(xLog && !xTickvals ? { dtick: logDtick(panels.flatMap((p) => p.pts.map((t) => t.x))) } : {}),
				...(xTickvals ? { tickmode: 'array', tickvals: xTickvals, ticktext: xTicktext } : {}),
				...(xRange ? { range: xRange, autorange: false } : {}),
				anchor: 'y',
				domain: [0, 1]
			}
		};
		if (nPan === 1) {
			l.yaxis = { ...axBase, title: title(panels[0]?.yTitle ?? ''), type: yLog ? 'log' : 'linear', ...yTicks(0) };
		} else {
			l.yaxis = { ...axBase, domain: [0, 0.46], title: title(panels[1]?.yTitle ?? ''), type: yLog ? 'log' : 'linear', anchor: 'x', ...yTicks(1) };
			l.yaxis2 = { ...axBase, domain: [0.54, 1], title: title(panels[0]?.yTitle ?? ''), type: yLog ? 'log' : 'linear', anchor: 'x', ...yTicks(0) };
			l.annotations = panels
				.map((p, i) => (p.tag ? { text: p.tag, xref: 'paper', yref: 'paper', x: 1, xanchor: 'right', y: i === 0 ? 1 : 0.46, yanchor: 'top', showarrow: false, font: { size: 10, color: th.muted } } : null))
				.filter(Boolean);
		}
		return l;
	});

	function evPt(e: any): { id: string; panel: number } | null {
		const p = e?.points?.[0];
		if (!p || typeof p.customdata !== 'string') return null;
		return { id: p.customdata, panel: Number(p.data?.meta ?? 0) };
	}

	function onhover(e: any) {
		const p = evPt(e);
		if (!p || !wrap) return;
		const r = wrap.getBoundingClientRect();
		hover = { key: `${p.panel}|${p.id}`, x: e.event.clientX - r.left, y: e.event.clientY - r.top };
	}
	function onunhover() {
		hover = null;
	}

	let lastHit = 0;
	function onclick(e: any) {
		const p = evPt(e);
		if (!p) return;
		lastHit = performance.now();
		const exists = pins.some((x) => x.id === p.id && x.panel === p.panel);
		pins = exists ? pins.filter((x) => !(x.id === p.id && x.panel === p.panel)) : [...pins, p];
		hover = null;
	}
	let downXY: [number, number] | null = null;
	function pdown(e: PointerEvent) {
		downXY = [e.clientX, e.clientY];
	}
	function wclick(e: MouseEvent) {
		if ((e.target as HTMLElement).closest('.pin')) return;
		if (performance.now() - lastHit < 250) return;
		const moved = downXY ? Math.hypot(e.clientX - downXY[0], e.clientY - downXY[1]) > 4 : false;
		if (!moved && pins.length) pins = [];
	}

	let pinXY = $state<{ key: string; px: number; py: number }[]>([]);
	function recompute(gd: any) {
		const fl = gd?._fullLayout;
		if (!fl?.xaxis || fl.xaxis._offset === undefined) return;
		const out: { key: string; px: number; py: number }[] = [];
		for (const p of pins) {
			const pt = ptIndex.get(`${p.panel}|${p.id}`);
			const ya = fl[yName(p.panel)];
			if (!pt || !ya) continue;
			const px = fl.xaxis._offset + fl.xaxis.d2p(pt.x);
			const py = ya._offset + ya.d2p(pt.y);
			if (Number.isFinite(px) && Number.isFinite(py)) out.push({ key: `${p.panel}|${p.id}`, px, py });
		}
		pinXY = out;
	}
	$effect(() => {
		void pins;
		void panels;
		void xLog;
		void yLog;
		if (gdEl) recompute(gdEl);
	});

	function place(x: number, y: number, w = 340, h = 260): { left: number; top: number } {
		const W = wrap?.clientWidth ?? 600;
		const H = wrap?.clientHeight ?? 400;
		let left = x + 14;
		if (left + w > W) left = Math.max(0, x - 14 - w);
		let top = y + 10;
		if (top + h > H) top = Math.max(0, H - h);
		return { left, top };
	}

	const badgeTip = $derived(
		`${omitted.plotted} of ${omitted.total} ${unit} plotted. Omitted: missing x ${omitted.missingX}, missing y ${omitted.missingY}, missing both ${omitted.missingBoth}, no pair with compatible conditions ${omitted.incomparable}, nonpositive on a log axis ${omitted.nonpositive}.`
	);
	const hoverPt = $derived(hover ? (ptIndex.get(hover.key) ?? null) : null);
</script>

<section class="panel" class:wide aria-label={`Chart ${letter}`} style="height:{nPan > 1 ? 520 : 400}px">
	<header>
		<span class="letter" data-tip={desc}>{letter}</span>
		<span class="badge num" data-tip={badgeTip}>{omitted.plotted}/{omitted.total}</span>
		<div class="grow"></div>
		{@render headerExtra?.()}
		{#if allowX}
			<span class="seg" data-tip="x axis scale">
				<button class:on={!xLog} onclick={() => (xLog = false)}>x lin</button><button class:on={xLog} onclick={() => (xLog = true)}>x log</button>
			</span>
		{/if}
		{#if allowY}
			<span class="seg" data-tip="y axis scale">
				<button class:on={!yLog} onclick={() => (yLog = false)}>y lin</button><button class:on={yLog} onclick={() => (yLog = true)}>y log</button>
			</span>
		{/if}
	</header>
	<div class="body" bind:this={wrap} onpointerdown={pdown} onclick={wclick} role="presentation">
		<Plot data={traces} {layout} {onhover} {onunhover} {onclick} onafterplot={recompute} bind:gd={gdEl} />
		{#if omitted.plotted === 0}<div class="empty muted">{emptyText}</div>{/if}
		{#each pinXY as p (p.key)}
			{@const pos = place(p.px, p.py)}
			{@const pt = ptIndex.get(p.key)}
			{#if pt}
				<div class="pin" style="left:{pos.left}px; top:{pos.top}px">
					<button class="x" aria-label="Unpin" data-tip="Unpin" onclick={() => (pins = pins.filter((q) => `${q.panel}|${q.id}` !== p.key))}>
						<svg viewBox="0 0 10 10" width="8" height="8"><path d="M1 1 L9 9 M9 1 L1 9" stroke="currentColor" stroke-width="1.4" /></svg>
					</button>
					<PointTip {pt} {classLabel} pinned />
				</div>
			{/if}
		{/each}
		{#if hover && hoverPt}
			{@const pos = place(hover.x, hover.y)}
			<div class="float" style="left:{pos.left}px; top:{pos.top}px"><PointTip pt={hoverPt} {classLabel} /></div>
		{/if}
	</div>
</section>

<style>
	.panel {
		background: var(--surface);
		border: 1px solid var(--border);
		display: flex;
		flex-direction: column;
		min-width: 0;
	}
	.panel.wide {
		grid-column: 1 / -1;
	}
	header {
		display: flex;
		gap: 6px;
		align-items: center;
		height: 28px;
		padding: 0 6px;
		border-bottom: 1px solid var(--border);
		flex: none;
	}
	.letter {
		font-weight: 700;
		color: var(--ink-2);
		width: 16px;
		text-align: center;
		border: 1px solid var(--line);
		cursor: help;
	}
	.badge {
		color: var(--ink-3);
		font-size: 10px;
		cursor: help;
	}
	.grow {
		flex: 1;
	}
	.seg {
		display: inline-flex;
	}
	.seg button {
		height: 20px;
		font-size: 10px;
		padding: 0 6px;
	}
	.body {
		position: relative;
		flex: 1;
		min-height: 0;
		overflow: hidden;
	}
	.float {
		position: absolute;
		z-index: 10;
		pointer-events: none;
	}
	.pin {
		position: absolute;
		z-index: 9;
	}
	.pin :global(.tip) {
		pointer-events: auto;
	}
	.x {
		position: absolute;
		right: 2px;
		top: 2px;
		width: 18px;
		height: 18px;
		padding: 0;
		z-index: 2;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		background: transparent;
		border: 0;
	}
	.empty {
		position: absolute;
		inset: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		pointer-events: none;
		padding: 0 20px;
		text-align: center;
	}
</style>
