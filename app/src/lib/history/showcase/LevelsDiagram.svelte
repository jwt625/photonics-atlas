<svelte:options namespace="svg" />

<script lang="ts">
	// Energy-level diagram (plot `kind: levels`): energy axis, level lines and bands with term labels, split brackets
	// labelled with the printed value, transition arrows by kind; assembled by plot progress r; hover for value + locator.
	import { levelsLayout, lo, hi, PAD } from './levels';
	import { fmt, plain, rich, term, type Run } from './plot';
	import type { Level, Plot, Split, Transition } from './types';

	let { plot, r, w, h, tip }: { plot: Plot; r: number; w: number; h: number; tip: (lines: string[] | null, x?: number, y?: number) => void } = $props();

	const g = $derived(levelsLayout(plot, w, h, r));
	const unit = $derived(plot.y?.unit ? plain(rich(plot.y.unit)) : '');
	const lvName = (id: string) => {
		const l = plot.levels?.find((x) => x.id === id);
		return l ? plain(term(l.label ?? l.id)) : id;
	};
	const asDrawn = $derived(plot.y?.scale === 'none');
	const energyText = (l: Level) => (Array.isArray(l.energy) ? `${fmt(lo(l.energy))} to ${fmt(hi(l.energy))}` : fmt(l.energy)) + (unit ? ' ' + unit : '');
	const src = (x: { basis?: string; locator?: string }) => [x.basis, x.locator].filter(Boolean).join(', ');

	function tipLevel(e: PointerEvent, l: Level) {
		tip([plain(term(l.label ?? l.id)), `${plot.y?.label ?? 'Energy'}: ${asDrawn ? 'as drawn' : energyText(l)}`, l.note ?? '', src(l)].filter(Boolean), e.clientX, e.clientY);
	}
	function tipSplit(e: PointerEvent, s: Split) {
		tip([`${lvName(s.between[0])} / ${lvName(s.between[1])} split`, `${s.value}${s.unit ? ' ' + plain(rich(s.unit)) : ''} (printed)`, src(s)].filter(Boolean), e.clientX, e.clientY);
	}
	function tipTr(e: PointerEvent, t: Transition) {
		tip(
			[
				[t.label, `${lvName(t.from)} → ${lvName(t.to)}`].filter(Boolean).join('  '),
				t.kind ?? '',
				t.wavelength_A != null ? `${t.wavelength_A} Å` : '',
				src(t)
			].filter(Boolean),
			e.clientX,
			e.clientY
		);
	}
	const shift = (k: Run['k']) => (k === 'sup' ? -0.42 : k === 'sub' ? 0.28 : 0);
	/** dy of run i relative to the previous run (tspans accumulate dy) */
	const dy = (rs: Run[], i: number) => `${shift(rs[i].k) - (i ? shift(rs[i - 1].k) : 0)}em`;
	const yLen = $derived(Math.max(0, g.yBot - g.yTop));
	const yTitle = $derived<Run[]>(plot.y?.unit ? [{ t: `${plot.y.label} (`, k: '' }, ...rich(plot.y.unit), { t: ')', k: '' }] : [{ t: plot.y?.label ?? '', k: '' }]);
</script>

{#snippet runs(rs: Run[])}
	{#each rs as run, i (i)}<tspan dy={dy(rs, i)} class:small={!!run.k}>{run.t}</tspan>{/each}
{/snippet}

<g class="lv">
	<!-- axis -->
	<line class="ax" x1={PAD.l} x2={PAD.l} y1={g.yBot} y2={g.yTop} stroke-dasharray={yLen} stroke-dashoffset={(1 - g.axisK) * yLen} />
	<g class="tk" style:opacity={g.axisK}>
		{#each g.ticks as v (v)}
			<line class="tm" x1={PAD.l - 4} x2={PAD.l} y1={g.Y.map(v)} y2={g.Y.map(v)} />
			<text x={PAD.l - 7} y={g.Y.map(v) + 3} text-anchor="end">{fmt(v)}</text>
		{/each}
		<text class="at" transform="translate(12 {(g.yTop + g.yBot) / 2}) rotate(-90)" text-anchor="middle">{@render runs(yTitle)}</text>
	</g>

	<!-- levels -->
	{#each g.levels as L (L.lv.id)}
		<g class="lvl" class:band={L.band} style:opacity={Math.min(1, L.k * 2)} role="presentation" onpointerenter={(e) => tipLevel(e, L.lv)} onpointermove={(e) => tipLevel(e, L.lv)} onpointerleave={() => tip(null)}>
			{#if L.band}
				<rect class="bd" x={L.x0} y={L.yTop} width={Math.max(0, (L.x1 - L.x0) * L.k)} height={Math.max(1, L.yBot - L.yTop)} />
				<text class="term" x={(L.x0 + L.x1) / 2} y={(L.yTop + L.yBot) / 2 + 5} text-anchor="middle">{@render runs(term(L.lv.label ?? L.lv.id))}</text>
			{:else}
				<line class="ln" class:ground={L.col === 'full'} x1={L.x0} x2={L.x0 + (L.x1 - L.x0) * L.k} y1={L.yTop} y2={L.yTop} />
				<text class="term" x={L.x0 + 2} y={L.yTop - 6}>{@render runs(term(L.lv.label ?? L.lv.id))}</text>
			{/if}
			<rect class="hit" x={L.x0} y={Math.min(L.yTop, L.yBot) - 6} width={Math.max(0, L.x1 - L.x0)} height={Math.abs(L.yBot - L.yTop) + 12} />
		</g>
	{/each}

	<!-- split brackets: printed value, not the drawn gap -->
	{#each g.splits as S, i (i)}
		<g class="sp" style:opacity={S.k} role="presentation" onpointerenter={(e) => tipSplit(e, S.sp)} onpointermove={(e) => tipSplit(e, S.sp)} onpointerleave={() => tip(null)}>
			<path d="M{S.x} {S.ya} h5 V{S.yb} h-5" />
			<text x={S.x + 9} y={(S.ya + S.yb) / 2 + 4}>{S.sp.value}&#32;{#if S.sp.unit}{@render runs(rich(S.sp.unit))}{/if}</text>
			<rect class="hit" x={S.x - 4} y={S.ya - 4} width="70" height={S.yb - S.ya + 8} />
		</g>
	{/each}

	<!-- transitions -->
	{#each g.arrows as A, i (i)}
		{#if A.k > 0}
			<g class="tr {A.kind}" role="presentation" onpointerenter={(e) => tipTr(e, A.tr)} onpointermove={(e) => tipTr(e, A.tr)} onpointerleave={() => tip(null)}>
				<line class="ar" x1={A.x} x2={A.x} y1={A.y0} y2={A.yTip - Math.sign(A.y1 - A.y0) * 7} />
				{#if A.head}<polygon points={A.head.map((q) => q.join(',')).join(' ')} />{/if}
				{#if A.tr.label && A.k > 0.6}<text x={A.x + 6} y={(A.y0 + A.y1) / 2} style:opacity={(A.k - 0.6) / 0.4}>{A.tr.label}</text>{/if}
				<line class="hit" x1={A.x} x2={A.x} y1={A.y0} y2={A.yTip} />
			</g>
		{/if}
	{/each}
</g>

<style>
	.ax { stroke: var(--ink-3); stroke-width: 1; }
	.tm { stroke: var(--ink-3); stroke-width: 1; }
	.tk text { fill: var(--ink-3); font-size: 10px; font-variant-numeric: tabular-nums; }
	.tk .at { fill: var(--ink-2); font-size: 11px; }
	.small { font-size: 0.72em; }
	.ln { stroke: var(--ink); stroke-width: 1.5; }
	.ln.ground { stroke-width: 2.5; }
	.bd { fill: var(--lv-pump); fill-opacity: 0.16; stroke: var(--lv-pump); stroke-width: 1; }
	.term { fill: var(--ink); font: 15px var(--text, inherit); }
	.sp path { fill: none; stroke: var(--ink-2); stroke-width: 1; }
	.sp text { fill: var(--ink-2); font-size: 11px; }
	.tr line.ar { stroke-width: 1.6; }
	.tr text { font-size: 11px; font-weight: 600; }
	.tr.pump line.ar { stroke: var(--lv-pump); }
	.tr.pump polygon, .tr.pump text { fill: var(--lv-pump); }
	.tr.emission line.ar { stroke: var(--lv-emit); }
	.tr.emission polygon, .tr.emission text { fill: var(--lv-emit); }
	.tr.nonradiative line.ar { stroke: var(--ink-3); stroke-dasharray: 4 3; }
	.tr.nonradiative polygon, .tr.nonradiative text { fill: var(--ink-3); }
	.tr.other line.ar { stroke: var(--ink-2); }
	.tr.other polygon, .tr.other text { fill: var(--ink-2); }
	.hit { fill: transparent; stroke: transparent; }
	.tr line.hit { stroke: transparent; stroke-width: 14; }
	.lvl, .sp, .tr { cursor: default; }
	.lv { --lv-pump: #46c776; --lv-emit: #ff4d42; }
	:global(:root[data-theme='light']) .lv { --lv-pump: #14904a; --lv-emit: #d42a1e; }
	@media (max-width: 700px) {
		.tk text { font-size: 11px; }
	}
</style>
