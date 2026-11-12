<script lang="ts">
	import { unitSuffix } from './progress';
	// Plot assembler (DevLog-017): SVG; at local progress r the axes draw first, then the series reveal with staggered,
	// overlapping starts (points / line in spec order, bars grow). Hover a point or bar for its value and locator; log /
	// linear toggle on axes flagged `log: true`; `scale: none` hides ticks; `kind: levels` draws an energy-level diagram.
	import LevelsDiagram from './LevelsDiagram.svelte';
	import Rich from './Rich.svelte';
	import { plotSeries, colorSlots, legendBlock, legendRows, stemBase, axesK, axisTicks, barK, cleanIndices, cleanPoints, equalAspect, errAt, errText, extent, fitTitle, whiskerPx, fmt, legendCorner, makeScale, markup, plainMarkup, plain, revealed, rich, startsLog, styleOf, toBars, type LogPair, type Run } from './plot';
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
	const all = $derived(plotSeries(plot));
	const series = $derived(all.map((s) => ({ s, pts: cleanPoints(s, logX, logY), idx: cleanIndices(s, logX, logY), bars: toBars(s), style: styleOf(s) })));
	// plots[].aspect 'equal': letterbox the data area so x and y data units have equal length (not with a log axis)
	const equal = $derived(plot.aspect === 'equal' && !logX && !logY);
	function scales(pad: { l: number; r: number; t: number; b: number }) {
		let box = { x0: pad.l, x1: Math.max(pad.l + 10, w - pad.r), y0: pad.t, y1: Math.max(pad.t + 10, h - pad.b) };
		if (equal) box = equalAspect(xr[1] - xr[0], yr[1] - yr[0], box);
		return { X: makeScale(xr[0], xr[1], box.x0, box.x1, logX), Y: makeScale(yr[0], yr[1], box.y1, box.y0, logY) };
	}
	const xr = $derived(extent(all, 0, logX, xAx.range));
	const yr = $derived(extent(all, 1, logY, yAx.range));
	// legend: the emptiest corner of the data area (all points and bars, so it does not move while assembling); when every
	// corner covers data (narrow plots), it moves above the data area and the plot shrinks to make room
	// legend rows (legend: false hidden, legend_group merged) and an optional note line under them
	const rows = $derived(legendRows(series));
	const slots = $derived(colorSlots(series));
	const noteRuns = $derived(plot.legend_note ? markup(plot.legend_note) : null);
	const hasLegend = $derived(rows.length > 1 || (rows.length > 0 && !!noteRuns));
	const ROWH = 15;
	const NOTEH = $derived(noteRuns ? 15 : 0);
	const itemW = $derived(26 + Math.max(0, ...rows.map((r) => plain(markup(series[r.first].s.name)).length)) * 6.2);
	const LGS = $derived({ w: Math.max(itemW, noteRuns ? plain(noteRuns).length * 6.2 : 0), h: rows.length * ROWH + 2 + NOTEH });
	let lgOpen = $state(false);
	const LG0 = $derived.by(() => {
		if (!hasLegend) return null;
		const { X: X0, Y: Y0 } = scales(PAD0);
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
	// above the data area the rows wrap into columns; on short panels (phones) the block keeps the data area at about
	// 60 % of the panel height (legend, note and x axis together take at most 40 %) and shows "+N more"
	const blk = $derived(
		lgOutside
			? legendBlock(rows.length, itemW + 10, Math.max(60, w - PAD0.l - PAD0.r), Math.max(ROWH, 0.4 * h - PAD0.b - LG_TOP - 10 - NOTEH), lgOpen)
			: legendBlock(rows.length, itemW, itemW, Infinity)
	);
	const PAD = $derived(lgOutside ? { ...PAD0, t: LG_TOP + blk.h + NOTEH + 10 } : PAD0);
	const LG = $derived(lgOutside ? { x: PAD.l, y: LG_TOP } : (LG0 ?? { x: 0, y: 0 }));
	const lgPos = (k: number) => ({ x: LG.x + Math.floor(k / Math.max(1, blk.perCol)) * (itemW + 10), y: LG.y + (k % Math.max(1, blk.perCol)) * ROWH });
	const XY = $derived(scales(PAD));
	const X = $derived(XY.X);
	const Y = $derived(XY.Y);
	const xt = $derived(axisTicks(xAx, xr[0], xr[1], logX, Math.max(3, Math.floor((X.r1 - X.r0) / 90))));
	const yt = $derived(axisTicks(yAx, yr[0], yr[1], logY, Math.max(3, Math.floor((Y.r0 - Y.r1) / 70))));
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
			// error bars of the revealed points (indexed like the spec's points)
			const errs = it.idx.slice(0, n).flatMap((oi, j) => {
				const ey = errAt(it.s.err, oi);
				const ex = errAt(it.s.err_x, oi);
				return ey || ex ? [whiskerPx(it.pts[j][0], it.pts[j][1], ey, ex, X, Y)] : [];
			});
			const stemY = it.style === 'stems' ? Y.map(stemBase(it.s, yr, logY)) : 0;
			return { sp, line: line.map((q) => q.join(',')).join(' '), bars, errs, stemY };
		})
	);
	// series colours: spec override, else the plot palette (CSS vars below, one set per theme)
	const color = (i: number) => series[i]?.s.color || `var(--pc${(slots[i] ?? i) % 5})`;
	const xLen = $derived(Math.max(0, X.r1 - X.r0));
	const yLen = $derived(Math.max(0, Y.r0 - Y.r1));
	const title = (a: Axis): Run[] => [...markup(a.label), ...(a.unit ? [{ t: ' (', k: '' as const }, ...rich(a.unit), { t: ')', k: '' as const }] : [])];
	// the rotated y title must fit the plot height (phones): shrink, then cut with the full title in its hover
	const yFit = $derived(fitTitle(plain(title(yAx)), Math.max(40, Y.r0 - Y.r1 + 30)));
	const shift = (k: Run['k']) => (k === 'sup' ? -0.42 : k === 'sub' ? 0.28 : 0);
	const dy = (rs: Run[], i: number) => `${shift(rs[i].k) - (i ? shift(rs[i - 1].k) : 0)}em`;
	const unitTxt = (a: Axis) => unitSuffix(a.unit ? plain(rich(a.unit)) : '');

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
			const ey = errAt(s.s.err, s.idx[pi]);
			const ex = errAt(s.s.err_x, s.idx[pi]);
			const eu = (a: Axis) => (a.unit ? plain(rich(a.unit)) : '');
			return tip(
				[
					s.s.name,
					`${xAx.label}: ${fmt(x)}${unitTxt(xAx)}${ex ? '  ' + errText(ex, eu(xAx)) : ''}`,
					yAx.scale === 'none' ? '' : `${yAx.label}: ${fmt(y)}${unitTxt(yAx)}${ey ? '  ' + errText(ey, eu(yAx)) : ''}`,
					[s.s.basis, s.s.locator].filter(Boolean).join(', ')
				].filter(Boolean),
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

<div class="plot">
<div class="area" bind:clientWidth={w} bind:clientHeight={h}>
	{#if !levels && (xAx.log || yAx.log || xAx.scale === 'log' || yAx.scale === 'log')}
		<div class="tg">
			{#if xAx.log || xAx.scale === 'log'}<button class:on={logX} onclick={() => onlog?.('x')} data-tip="x axis: log / linear">log x</button>{/if}
			{#if yAx.log || yAx.scale === 'log'}<button class:on={logY} onclick={() => onlog?.('y')} data-tip="y axis: log / linear">log y</button>{/if}
		</div>
	{/if}
	{#if plot.title}<div class="title"><Rich text={plot.title} /></div>{/if}
	{#if lgOutside && (blk.hidden > 0 || lgOpen)}
		{@const q = lgPos(lgOpen ? rows.length : blk.shown)}
		<button class="lgmore" style:left="{q.x}px" style:top="{q.y}px" onclick={() => (lgOpen = !lgOpen)} data-tip={lgOpen ? 'Fewer legend entries' : 'All legend entries'}>{lgOpen ? 'less' : `+${blk.hidden} more`}</button>
	{/if}
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
					<text class="at" transform="translate({Math.max(12, X.r0 - 40)} {(Y.r0 + Y.r1) / 2}) rotate(-90)" text-anchor="middle" font-size={yFit.fs}>{#if yFit.cut || yFit.fs < 11}{yFit.text}{:else}{@render runs(title(yAx))}{/if}{#if yFit.cut}<title>{plain(title(yAx))}</title>{/if}</text>
				</g>
				{#each shown as it, i (i)}
					{#each it.errs as E, j (j)}
						<g class="err" style:stroke={color(i)}>
							{#if E.v}<line x1={E.v[0]} x2={E.v[0]} y1={E.v[1]} y2={E.v[2]} /><line x1={E.v[0] - 3} x2={E.v[0] + 3} y1={E.v[1]} y2={E.v[1]} /><line x1={E.v[0] - 3} x2={E.v[0] + 3} y1={E.v[2]} y2={E.v[2]} />{/if}
							{#if E.h}<line y1={E.h[0]} y2={E.h[0]} x1={E.h[1]} x2={E.h[2]} /><line y1={E.h[0] - 3} y2={E.h[0] + 3} x1={E.h[1]} x2={E.h[1]} /><line y1={E.h[0] - 3} y2={E.h[0] + 3} x1={E.h[2]} x2={E.h[2]} />{/if}
						</g>
					{/each}
					{#if it.bars.length}
						{#each it.bars as B, j (j)}
							{#if B.k > 0}<rect class="bar" x={B.x} y={Math.min(B.y, base)} width={B.w} height={Math.max(0.5, B.hgt)} style:fill={color(i)} style:stroke={color(i)} />{/if}
						{/each}
					{:else}
						{#if series[i].style === 'stems'}
							<g class="stems" style:stroke={color(i)}>
								{#each it.sp as [x, y], j (j)}<line x1={x} x2={x} y1={it.stemY} y2={y} />{#if series[i].s.stem_cap}<circle cx={x} cy={y} r="2" style:fill={color(i)} />{/if}{/each}
							</g>
						{:else if series[i].style !== 'points' && it.line}<polyline points={it.line} style:stroke={color(i)} class="ln" class:dash={series[i].style === 'dashed'} />{/if}
						{#if series[i].style === 'points' || series[i].style === 'both'}
							{#each it.sp as [x, y], j (j)}<circle cx={x} cy={y} r="3" style:fill={color(i)} />{/each}
						{/if}
					{/if}
				{/each}
				{#if hasLegend}
					<g class="lg" style:opacity={ak}>
						{#each rows.slice(0, blk.shown) as rw, k (rw.key)}
							{@const q = lgPos(k)}
							{@const c = color(rw.first)}
							{#if rw.bars}
								<rect class="swo" x={q.x} y={q.y + 2} width="12" height="8" style:fill={c} style:fill-opacity="0.35" />
							{:else if rw.stems}
								<line class="stemsw" x1={q.x + 6} x2={q.x + 6} y1={q.y + 11} y2={q.y + 1} style:stroke={c} />
							{:else if rw.dashed}
								<line class="dash" x1={q.x} x2={q.x + 12} y1={q.y + 6} y2={q.y + 6} style:stroke={c} />
							{:else if rw.line && rw.dots}
								<line class="lsw" x1={q.x} x2={q.x + 14} y1={q.y + 6} y2={q.y + 6} style:stroke={c} /><circle class="swo" cx={q.x + 7} cy={q.y + 6} r="3" style:fill={c} />
							{:else if rw.dots}
								<circle class="swo" cx={q.x + 5} cy={q.y + 6} r="3" style:fill={c} />
							{:else}
								<rect x={q.x} y={q.y + 5} width="12" height="2" style:fill={c} />
							{/if}
							<text x={q.x + 18} y={q.y + 10}>{@render runs(markup(series[rw.first].s.name))}</text>
						{/each}
						{#if noteRuns}
							<text class="lnote" x={LG.x} y={LG.y + (lgOutside ? blk.h : rows.length * ROWH) + 11}>{@render runs(noteRuns)}</text>
						{/if}
					</g>
				{/if}
			{/if}
		</svg>
	{/if}
</div>
{#if plot.note}<div class="pnote" data-tip={plainMarkup(plot.note)}><Rich text={plot.note} /></div>{/if}
</div>

<style>
	.plot { position: relative; width: 100%; height: 100%; display: flex; flex-direction: column; --pc0: #4c9bf0; --pc1: #f7962c; --pc2: #46dca5; --pc3: #c6a6fa; --pc4: #ea70a3; }
	:global(:root[data-theme='light']) .plot { --pc0: #2a78d6; --pc1: #c96a0c; --pc2: #12936a; --pc3: #8459cf; --pc4: #c4457c; }
	.area { position: relative; flex: 1; min-height: 0; }
	svg { display: block; overflow: visible; }
	.pnote { flex: none; padding: 2px 4px 0 26px; font: italic 12px/1.35 var(--text, inherit); color: var(--ink-3); display: -webkit-box; -webkit-line-clamp: 2; line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
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
	.err line { stroke-width: 1; }
	/* swatches keep a 1 px neutral outline so near-white / near-black colours stay visible in either theme */
	.swo { stroke: color-mix(in srgb, var(--ink) 45%, transparent); stroke-width: 0.8; }
	.lsw { stroke-width: 1.5; }
	.lnote { fill: var(--ink-3); font-size: 10px; font-style: italic; }
	.lgmore { position: absolute; height: 15px; padding: 0 5px; font-size: 10px; z-index: 1; }
	.stems line, line.stemsw { stroke-width: 1.2; }
	.dash { stroke-dasharray: 5 4; }
	line.dash { stroke-width: 1.5; }
	.lg text { fill: var(--ink-2); }
	@media (max-width: 700px) {
		.tk text, .lg text { font-size: 11px; }
		.tk .at { font-size: 12px; }
	}
</style>
