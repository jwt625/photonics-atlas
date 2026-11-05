<script lang="ts">
	// Gallery drawing of one component: the curated drawing's thumbnail view, fetched when the card nears the viewport.
	// Template scene when the component has no curated drawing. Nothing is drawn until the real drawing is available.
	import type { Component } from '../components.svelte';
	import { curated, curatedScene, loadCurated } from './curated.svelte';
	import { buildScenes } from './scene';
	import Scene from './Scene.svelte';
	import type { Resolved } from './resolve';

	let { c, r, height = 120 }: { c: Component; r: Resolved; height?: number } = $props();
	let box = $state<HTMLDivElement>();
	let near = $state(false);
	$effect(() => {
		if (!box || near) return;
		const io = new IntersectionObserver((es) => es.some((e) => e.isIntersecting) && (near = true), { rootMargin: '400px' });
		io.observe(box);
		return () => io.disconnect();
	});
	const has = $derived(!!curated.index?.[c.component_id]);
	$effect(() => {
		if (near && has) loadCurated(c.component_id);
	});
	const layout = $derived(has ? curated.got[c.component_id] : undefined);
	const scene = $derived.by(() => {
		if (!curated.index || !near) return null;
		if (layout) {
			const v = layout.views.find((x) => x.id === layout.thumb.view) ?? layout.views[0];
			if (!v) return null;
			const s = curatedScene(layout, v, c);
			return layout.thumb.window ? { ...s, window: layout.thumb.window } : s;
		}
		if (has) return null;
		const sc = buildScenes(r);
		const pick = r.templateId === 'waveguide_xsec' ? sc.xsec : sc.top;
		return pick.schematic ? null : pick;
	});
</script>

<div class="cs" bind:this={box} style:height="{height}px">
	{#if scene}<Scene {scene} {height} thumb />{:else if curated.index?.[c.component_id]?.drawn === false}<span class="nd" data-tip={curated.index[c.component_id].not_drawn.join('\n')}>not drawn: {curated.index[c.component_id].not_drawn[0]}</span>{/if}
</div>

<style>
	.cs { min-width: 0; background: var(--bg); border: 1px solid var(--grid); }
	.cs { display: flex; align-items: center; justify-content: center; }
	.cs > :global(*) { flex: 1; min-width: 0; }
	.cs :global(.svgwrap) { border: none; }
	.nd { flex: none; max-width: 90%; font-size: 11px; color: var(--ink-3); text-align: center; }
</style>
