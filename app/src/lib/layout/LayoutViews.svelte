<script lang="ts">
	// Top view + cross-section of one component with the material / basis legend. Compact for the components detail
	// panel, full for /layout?id=.
	import type { Component, ComponentsView } from '../components.svelte';
	import { MATERIALS } from './materials';
	import { BASIS_LEGEND, resolve } from './resolve';
	import { buildScenes } from './scene';
	import Scene from './Scene.svelte';

	let { comp, view, compact = false, height = 0 }: { comp: Component; view: ComponentsView; compact?: boolean; height?: number } = $props();

	const r = $derived(resolve(comp, view));
	const scenes = $derived(r ? buildScenes(r) : null);
	const mats = $derived.by(() => {
		const s = new Set<string>();
		for (const sc of scenes ? [scenes.top, scenes.xsec] : []) for (const sh of sc.shapes) if (!sh.line) s.add(sh.mat);
		return [...s].filter((m) => MATERIALS[m]);
	});
	const badges = $derived.by(() => {
		const s = new Set<string>();
		for (const d of Object.values(r?.dims ?? {})) if (d.badge) s.add(d.badge);
		return BASIS_LEGEND.filter(([b]) => s.has(b));
	});
	const h = $derived(height || (compact ? 150 : 360));
</script>

{#if r && scenes}
	<div class="lv" class:compact>
		<div class="views">
			<Scene scene={scenes.top} height={h} {compact} />
			<Scene scene={scenes.xsec} height={h} {compact} />
		</div>
		<div class="legend">
			{#each mats as m}<span class="sw" data-tip={MATERIALS[m]}><i style:background="var(--m-{m})"></i>{MATERIALS[m]}</span>{/each}
			<span class="sw" data-tip="Dimension not reported by the source: drawn at a fixed proportion of a reported neighbour, never labelled with a number"><i class="dash"></i>not reported</span>
			{#each badges as [b, t]}<span class="sw" data-tip={t}><b class:meas={b === 'M'}>{b}</b>{compact ? '' : t}</span>{/each}
		</div>
	</div>
{/if}

<style>
	.lv { min-width: 0; }
	.views { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 10px; }
	.compact .views { grid-template-columns: minmax(0, 1fr); gap: 4px; }
	@media (max-width: 1000px) { .views { grid-template-columns: minmax(0, 1fr); } }
	.legend { display: flex; flex-wrap: wrap; gap: 2px 10px; margin-top: 4px; font-size: 10px; color: var(--ink-3); }
	.sw { display: inline-flex; align-items: center; gap: 4px; white-space: nowrap; }
	.sw i { display: inline-block; width: 10px; height: 8px; opacity: 0.85; }
	.sw i.dash { border: 1px dashed var(--warn); background: transparent; }
	.sw b { font: 700 9px var(--mono); color: var(--ink-2); }
	.sw b.meas { color: var(--accent); }
</style>
