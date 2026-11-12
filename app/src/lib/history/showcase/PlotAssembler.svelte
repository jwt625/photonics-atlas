<script lang="ts">
	// Plot assembler (DevLog-017): SVG; at local progress r the axes draw first, then the series reveal with staggered,
	// overlapping starts (points / line in spec order, bars grow). Hover a point or bar for its value and locator; log /
	// linear toggle on axes flagged `log: true`; `scale: none` hides ticks; `kind: levels` draws an energy-level diagram.
	import LevelsDiagram from './LevelsDiagram.svelte';
	import { axesK, axisTicks, barK, cleanPoints, extent, fmt, legendCorner, makeScale, plain, revealed, rich, startsLog, styleOf, toBars, type LogPair, type Run } from './plot';
	import type { Axis, Plot } from './types';

	let {
		plot,
		r,
		tip,
		log,
		onlog
	}: {
		plot: Plot;
		r: number;
		tip: (lines: string[] | null, x?: number, y?: number) => void;
		/** log / linear choice, owned by the story per plot id (see plot.ts logOf / toggleLog); default: the spec's */
		log?: LogPair;
		onlog?: (axis: 'x' | 'y') => void;
	} = $props();

	let w = $state(0);
	let h = $state(0);
	const logX = $derived(log?.x ?? startsLog(plot.x));
	const logY = $derived(log?.y ?? startsLog(plot.y));

	const levels = $derived(plot.kind === 'levels');
	const xAx = $derived<Axis>(plot.x ?? { label: '' });
	const yAx = $derived<Axis>(plot.y ?? { label: '' });
	const PAD0 = $derived({ l: yAx.scale === 'none' ? 26 : 52, r: 14, t: 26, b: 40 });
	const all = $derived(Array.isArray(plot.series) ? plot.series.filter((s) => s && (Array.isArray(s.points) || Array.isArray(s.bars))) : []);
	const series = $derived(all.map((s) => ({ s, pts: cleanPoints(s, logX, logY), bars: toBars(s), style: styleOf(s) })));
	const xr = $derived(extent(all, 0, logX, xAx.range));
	const yr = $derived(extent(all, 1, logY, yAx.range));
	// legend: the emptiest corner of the data area (all points and bars, so it does not move while assembling); when every
	// corner covers data (narrow plots), it moves above the data area and the plot shrinks to make room
	const LGS = $derived({ w: 24 + Math.max(0, ...series.map((it) => it.s.name.length)) * 6.2, h: series.length * 15 + 2 });
	const LG0 = $derived.by(() => {
		if (series.length < 2) return null;
		const X0 = makeScale(xr[0], xr[1], PAD0.l, Math.max(PAD0.l + 10, w - PAD0.r), logX);
		const Y0 = makeScale(yr[0], yr[1], Math.max(PAD0.t + 10, h - PAD0.b), PAD0.t, logY);
		const b0 = logY ? Y0.r0 : Y0.map(Math.min(Math.max(0, yr[0]), yr[1]));
		const pts: [number, number][] = [];
		for (const it of series) {
			const sp = it.pts.map(([x, y]) => [X0.map(x), Y0.map(y)] as [number, number]);
			sp.forEach((q, j) => {
				pts.push(q);
				if (j) pts.push([(q[0] + sp[j - 1][0]) / 2, (q[1] + sp[j - 1][1]) / 2]);
			});
			for (const b of it.bars) {
				const top = Y0.map(logY ? Math.max(b.height, yr[0]) : b.height);
				for (let f = 0; f <= 1; f += 0.25) for (const yy of [top, (top + b0) / 2]) pts.push([X0.map(b.from) + (X0.map(b.to) - X0.map(b.from)) * f, yy]);
			}
		}
		return legendCorner(pts, { x0: X0.r0, x1: X0.r1, y0: Y0.r1, y1: Y0.r0 }, LGS.w, LGS.h);
	});
	const LG_TOP = 22;
	const lgOutside = $derived(!!LG0 && LG0.hits > 0);
	const PAD = $derived(lgOutside ? { ...PAD0, t: LG_TOP + LGS.h + 10 } : PAD0);
	const LG = $derived(lgOutside ? { x: PAD.l, y: LG_TOP } : (LG0 ?? { x: 0, y: 0 }));
	const X = $derived(makeScale(xr[0], xr[1], PAD.l, Math.max(PAD.l + 10, w - PAD.r), logX));
	const Y = $derived(makeScale(yr[0], yr[1], Math.max(PAD.t + 10, h - PAD.b), PAD.t, logY));
	const xt = $derived(axisTicks(xAx, xr[0], xr[1], logX, Math.max(2, Math.floor(w / 90))));
	const yt = $derived(axisTicks(yAx, yr[0], yr[1], logY, Math.max(2, Math.floor(h / 70))));
	const ak = $derived(axesK(r));
	const base = $derived(logY ? Y.r0 : Y.map(Math.min(Math.max(0, yr[0]), yr[1])));
	const shown = $derived(
		series.map((it, i) => {
			const { n, frac } = revealed(r, series.length, i, it.pts.length);
			const sp = it.pts.slice(0, n).map(([x, y]) => [X.map(x), Y.map(y)] as [number, number]);
			const line = [...sp];
			if (n > 0 && n < it.pts.length && frac > 0) {
				const [x1, y1] = [X.map(it.pts[n][0]), Y.map(it.pts[n][1])];
				const [x0, y0] = line[line.length - 1];
				line.push([x0 + (x1 - x0) * frac, y0 + (y1 - y0) * frac]);
			}
			const bars = it.bars.map((b, j) => {
				const k = barK(r, series.length, i, j, it.bars.length);
				const top = Y.map(logY ? Math.max(b.height, yr[0]) : b.height);
				const x0 = X.map(b.from);
				const x1 = X.map(b.to);
				return { b, k, x: Math.min(x0, x1), w: Math.max(1, Math.abs(x1 - x0)), y: base + (top - base) * k, hgt: Math.abs(top - base) * k, top };
			});
			return { sp, line: line.map((q) => q.join(',')).join(' '), bars };
		})
	);
	// series colours: spec override, else the plot palette (CSS vars below, one set per theme)
	const color = (i: number) => series[i]?.s.color || `var(--pc${i % 5})`;
	const xLen = $derived(Math.max(0, X.r1 - X.r0));
	const yLen = $derived(Math.max(0, Y.r0 - Y.r1));
	const title = (a: Axis): Run[] => (a.unit ? [{ t: `${a.label} (`, k: '' }, ...rich(a.unit), { t: ')', k: '' }] : [{ t: a.label, k: '' }]);
	const shift = (k: Run['k']) => (k === 'sup' ? -0.42 : k === 'sub' ? 0.28 : 0);
	const dy = (rs: Run[], i: number) => `${shift(rs[i].k) - (i ? shift(rs[i - 1].k) : 0)}em`;
	const unitTxt = (a: Axis) => (a.unit ? ' ' + plain(rich(a.unit)) : '');

	function onMove(e: PointerEvent) {
		if (levels) return;
		const box = (e.currentTarget as SVGSVGElement).getBoundingClientRect();
		const mx = e.clientX - box.left;
		const my = e.clientY - box.top;
		let best: { d: number; si: number; pi: number } | null = null;
		shown.forEach((it, si) =>
			it.sp.forEach(([px, py], pi) => {
				const d = Math.hypot(px - mx, py - my);
				if (d < 14 && (!best || d < best.d)) best = { d, si, pi };
			})
		);
		if (best) {
			const { si, pi } = best as { d: number; si: number; pi: number };
			const s = series[si];
			const [x, y] = s.pts[pi];
			return tip(
				[s.s.name, `${xAx.label}: ${fmt(x)}${unitTxt(xAx)}`, yAx.scale === 'none' ? '' : `${yAx.label}: ${fmt(y)}${unitTxt(yAx)}`, [s.s.basis, s.s.locator].filter(Boolean).join(', ')].filter(Boolean),
				e.clientX,
				e.clientY
			);
		}
		// bars: inside the drawn rectangle (or within 4 px of a thin one)
		for (let si = shown.length - 1; si >= 0; si--)
			for (const B of shown[si].bars) {
				if (B.k <= 0) continue;
				const top = Math.min(B.y, base);
				const bot = Math.max(B.y, base);
				if (mx >= B.x - 3 && mx <= B.x + B.w + 3 && my >= top - 4 && my <= bot + 2) {
					const s = series[si].s;
					return tip(
						[
							[s.name, B.b.line].filter(Boolean).join(': '),
							`${xAx.label}: ${fmt(B.b.from)} to ${fmt(B.b.to)}${unitTxt(xAx)}`,
							yAx.scale === 'none' ? `${yAx.label}: as drawn` : `${yAx.label}: ${fmt(B.b.height)}${unitTxt(yAx)}`,
							[s.basis, s.locator].filter(Boolean).join(', ')
						].filter(Boolean),
						e.clientX,
						e.clientY
					);
				}
			}
		tip(null);
	}
</script>

{#snippet runs(rs: Run[])}
	{#each rs as run, i (i)}<tspan dy={dy(rs, i)} font-size={run.k ? '0.72em' : null}>{run.t}</tspan>{/each}
{/snippet}

<div class="plot" bind:clientWidth={w} bind:clientHeight={h}>
	{#if !levels && (xAx.log || yAx.log || xAx.scale === 'log' || yAx.scale === 'log')}
		<div class="tg">
			{#if xAx.log || xAx.scale === 'log'}<button class:on={logX} onclick={() => onlog?.('x')} data-tip="x axis: log / linear">log x</button>{/if}
			{#if yAx.log || yAx.scale === 'log'}<button class:on={logY} onclick={() => onlog?.('y')} data-tip="y axis: log / linear">log y</button>{/if}
		</div>
	{/if}
	{#if plot.title}<div class="title">{plot.title}</div>{/if}
	{#if w > 0 && h > 0}
		<svg width={w} height={h} role="img" aria-label={plot.title || (levels ? 'Energy-level diagram' : `${yAx.label} vs ${xAx.label}`)} onpointermove={onMove} onpointerleave={() => tip(null)}>
			{#if levels}
				<LevelsDiagram {plot} {r} {w} {h} {tip} />
			{:else}
				<g class="grid" style:opacity={ak}>
					{#each yt.major as v (v)}<line x1={X.r0} x2={X.r1} y1={Y.map(v)} y2={Y.map(v)} />{/each}
				</g>
				<line class="ax" x1={X.r0} x2={X.r1} y1={Y.r0} y2={Y.r0} stroke-dasharray={xLen} stroke-dashoffset={(1 - ak) * xLen} />
				<line class="ax" x1={X.r0} x2={X.r0} y1={Y.r0} y2={Y.r1} stroke-dasharray={yLen} stroke-dashoffset={(1 - ak) * yLen} />
				<g class="tk" style:opacity={ak}>
					{#each xt.minor as v (v)}<line class="mn" x1={X.map(v)} x2={X.map(v)} y1={Y.r0} y2={Y.r0 + 3} />{/each}
					{#each xt.major as v (v)}<line class="mj" x1={X.map(v)} x2={X.map(v)} y1={Y.r0} y2={Y.r0 + 5} /><text x={X.map(v)} y={Y.r0 + 16} text-anchor="middle">{fmt(v)}</text>{/each}
					{#each yt.minor as v (v)}<line class="mn" x1={X.r0 - 3} x2={X.r0} y1={Y.map(v)} y2={Y.map(v)} />{/each}
					{#each yt.major as v (v)}<text x={X.r0 - 6} y={Y.map(v) + 3} text-anchor="end">{fmt(v)}</text>{/each}
					<text class="at" x={(X.r0 + X.r1) / 2} y={h - 6} text-anchor="middle">{@render runs(title(xAx))}</text>
					<text class="at" transform="translate(12 {(Y.r0 + Y.r1) / 2}) rotate(-90)" text-anchor="middle">{@render runs(title(yAx))}</text>
				</g>
				{#each shown as it, i (i)}
					{#if it.bars.length}
						{#each it.bars as B, j (j)}
							{#if B.k > 0}<rect class="bar" x={B.x} y={Math.min(B.y, base)} width={B.w} height={Math.max(0.5, B.hgt)} style:fill={color(i)} style:stroke={color(i)} />{/if}
						{/each}
					{:else}
						{#if series[i].style !== 'points' && it.line}<polyline points={it.line} style:stroke={color(i)} class="ln" class:dash={series[i].style === 'dashed'} />{/if}
						{#if series[i].style === 'points' || series[i].style === 'both'}
							{#each it.sp as [x, y], j (j)}<circle cx={x} cy={y} r="3" style:fill={color(i)} />{/each}
						{/if}
					{/if}
				{/each}
				{#if series.length > 1}
					<g class="lg" style:opacity={ak}>
						{#each series as it, i (i)}
							{#if it.style === 'dashed' && !it.bars.length}
								<line class="dash" x1={LG.x} x2={LG.x + 12} y1={LG.y + 6 + i * 15} y2={LG.y + 6 + i * 15} style:stroke={color(i)} />
							{:else if it.style === 'points' && !it.bars.length}
								<circle cx={LG.x + 5} cy={LG.y + 6 + i * 15} r="3" style:fill={color(i)} />
							{:else}
								<rect x={LG.x} y={LG.y + (it.bars.length ? 2 : 5) + i * 15} width="12" height={it.bars.length ? 8 : 2} style:fill={color(i)} style:fill-opacity={it.bars.length ? 0.35 : 1} />
							{/if}
							<text x={LG.x + 16} y={LG.y + 10 + i * 15}>{it.s.name}</text>
						{/each}
					</g>
				{/if}
			{/if}
		</svg>
	{/if}
</div>

<style>
	.plot { position: relative; width: 100%; height: 100%; --pc0: #4c9bf0; --pc1: #f7962c; --pc2: #46dca5; --pc3: #c6a6fa; --pc4: #ea70a3; }
	:global(:root[data-theme='light']) .plot { --pc0: #2a78d6; --pc1: #c96a0c; --pc2: #12936a; --pc3: #8459cf; --pc4: #c4457c; }
	svg { display: block; overflow: visible; }
	.title { position: absolute; left: 52px; top: 4px; font-size: 11px; color: var(--ink-2); }
	.tg { position: absolute; right: 14px; top: 0; display: flex; gap: 2px; z-index: 1; }
	.tg button { height: 20px; font-size: 10px; padding: 0 6px; }
	.grid line { stroke: var(--grid); stroke-width: 1; opacity: 0.6; }
	.ax { stroke: var(--ink-3); stroke-width: 1; }
	.tk line { stroke: var(--ink-3); stroke-width: 1; }
	.tk .mn { opacity: 0.6; }
	.tk text, .lg text { fill: var(--ink-3); font-size: 10px; font-variant-numeric: tabular-nums; }
	.tk .at { fill: var(--ink-2); font-size: 11px; }
	.ln { fill: none; stroke-width: 1.5; stroke-linejoin: round; stroke-linecap: round; }
	.bar { fill-opacity: 0.24; stroke-width: 1.2; }
	.dash { stroke-dasharray: 5 4; }
	line.dash { stroke-width: 1.5; }
	.lg text { fill: var(--ink-2); }
	@media (max-width: 700px) {
		.tk text, .lg text { font-size: 11px; }
		.tk .at { font-size: 12px; }
	}
</style>
