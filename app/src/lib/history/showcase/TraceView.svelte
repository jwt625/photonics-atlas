<script lang="ts">
	// Traced public-domain drawing (ipatent trace schema) linked to the story's parts: hover / click a numbered part to
	// highlight it in the model and the parts list. Parts not yet introduced at the current p are dimmed.
	import { untrack } from 'svelte';
	import { hitLayer, renderTrace, type Trace } from './trace';
	import type { Drawing } from './types';

	let {
		drawing,
		trace,
		image,
		on,
		pending,
		hover,
		pick
	}: {
		drawing: Drawing;
		trace: Trace | null;
		image: string | null;
		/** highlighted part ids */
		on: readonly string[];
		/** part ids not introduced yet */
		pending: ReadonlySet<string>;
		hover: (id: string | null, e?: PointerEvent) => void;
		pick: (id: string) => void;
	} = $props();

	let svg: SVGSVGElement | undefined = $state();
	let groups: SVGGElement[] = [];
	let mode = $state<'trace' | 'scan'>('trace');
	const uid = `tr${Math.random().toString(36).slice(2, 8)}`;

	// (re)draw when the trace arrives (it loads after the spec) or changes
	$effect(() => {
		const root = svg;
		const t = trace;
		if (!root || !t) return;
		const partOf = (ref: string) => drawing.numerals?.[ref];
		root.replaceChildren();
		const r = renderTrace(root, t, uid, partOf);
		groups = Object.values(r.groups);
		root.appendChild(hitLayer(t, partOf));
		untrack(paint);
	});

	function paint() {
		const sel = new Set(on);
		svg?.classList.toggle('sel', sel.size > 0);
		for (const g of groups) {
			const p = g.dataset.part;
			g.classList.toggle('on', !!p && sel.has(p));
			g.classList.toggle('fut', !!p && pending.has(p));
		}
	}
	$effect(() => {
		void on;
		void pending;
		paint();
	});

	const partAt = (e: Event) => ((e.target as Element | null)?.closest?.('[data-part]') as SVGElement | null)?.dataset.part ?? null;
</script>

<figure class="dw">
	<!-- pointer linking only; the parts list is the keyboard route to the same parts -->
	<div
		class="box"
		role="presentation"
		onpointermove={(e) => hover(partAt(e), e)}
		onpointerleave={() => hover(null)}
		onclick={(e) => {
			const id = partAt(e);
			if (id) pick(id);
		}}
	>
		{#if trace}
			<svg bind:this={svg} class:hide={mode === 'scan'} preserveAspectRatio="xMidYMid meet" role="img" aria-label={drawing.source}></svg>
		{/if}
		{#if image && (mode === 'scan' || !trace)}<img src={image} alt={drawing.source} />{/if}
	</div>
	<figcaption>
		{#if drawing.url}<a href={drawing.url} target="_blank" rel="noopener">{drawing.source}</a>{:else}{drawing.source}{/if}
		{#if trace && image}
			<span class="seg">
				<button class:on={mode === 'trace'} onclick={() => (mode = 'trace')}>Trace</button><button class:on={mode === 'scan'} onclick={() => (mode = 'scan')}>Scan</button>
			</span>
		{/if}
	</figcaption>
</figure>

<style>
	.dw { margin: 0; display: flex; flex-direction: column; min-height: 0; height: 100%; }
	.box { position: relative; flex: 1; min-height: 0; background: var(--surface); border: 1px solid var(--border); }
	svg, img { position: absolute; inset: 4px; width: calc(100% - 8px); height: calc(100% - 8px); object-fit: contain; }
	svg.hide { display: none; }
	img { background: #fff; }
	figcaption { display: flex; align-items: center; gap: 8px; padding: 3px 0 0; font-size: 10px; color: var(--ink-3); }
	.seg { margin-left: auto; display: inline-flex; }
	.seg button { height: 18px; font-size: 10px; padding: 0 5px; }
	svg :global(.tr-s) { stroke: var(--ink-2); fill: none; stroke-linecap: round; stroke-linejoin: round; }
	svg :global(.tr-fill-solid) { fill: var(--ink-2); }
	svg :global(.tr-fill-light) { fill: var(--ink-2); fill-opacity: 0.08; }
	svg :global(.tr-fill-paper) { fill: var(--surface); }
	svg :global(.tr-arrow) { fill: var(--ink-2); }
	svg :global(.tr-hatchline) { stroke: var(--ink-2); stroke-width: 2; }
	svg :global(.tr-t) { fill: var(--ink-2); font-family: Helvetica, Arial, sans-serif; }
	svg :global(.tr-it) { font-style: italic; }
	svg :global(.tr-b) { font-weight: 700; }
	svg :global(.tr-el) { transition: opacity 0.12s; }
	svg :global(.tr-el.fut) { opacity: 0.25; }
	svg:global(.sel) :global(.tr-el) { opacity: 0.3; }
	svg :global(.tr-el.on) { opacity: 1 !important; }
	svg :global(.tr-el.on .tr-s) { stroke: var(--accent); }
	svg :global(.tr-el.on .tr-t), svg :global(.tr-el.on .tr-fill-solid), svg :global(.tr-el.on .tr-arrow) { fill: var(--accent); }
	svg :global(.tr-hit [data-part]) { cursor: pointer; }
	@media (prefers-reduced-motion: reduce) {
		svg :global(.tr-el) { transition: none; }
	}
</style>
