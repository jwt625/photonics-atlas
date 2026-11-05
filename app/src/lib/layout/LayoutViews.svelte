<script lang="ts">
	// All views of one component with the material / layer / basis legend: the curated drawing when there is one (DevLog-013
	// D505), else the template scene. Compact for the components detail panel, full for /layout?id=.
	import { onMount } from 'svelte';
	import type { Component, ComponentsView } from '../components.svelte';
	import { curated, curatedScene, layersOf, loadCurated, loadCuratedIndex } from './curated.svelte';
	import { MATERIALS } from './materials';
	import { BASIS_LEGEND, resolve } from './resolve';
	import { buildScenes, type Scene as SceneT } from './scene';
	import Scene from './Scene.svelte';

	let { comp, view, compact = false, height = 0 }: { comp: Component; view: ComponentsView; compact?: boolean; height?: number } = $props();

	onMount(loadCuratedIndex);
	const has = $derived(!!curated.index?.[comp.component_id]);
	$effect(() => {
		if (has) loadCurated(comp.component_id);
	});
	const layout = $derived(has ? curated.got[comp.component_id] : undefined);
	const r = $derived(resolve(comp, view));
	const template = $derived(r && curated.index && !has ? buildScenes(r) : null);
	const scenes = $derived.by<SceneT[]>(() => {
		if (layout) {
			const all = layout.views.map((v) => curatedScene(layout, v, comp));
			return compact ? all.filter((s, i) => i === 0 || s.view === 'xsec').slice(0, 2) : all;
		}
		// a template view with no reported dimension is not a drawing of this device (DevLog-013 D509): not shown
		return template ? [template.top, template.xsec].filter((x) => !x.schematic) : [];
	});
	const undrawn = $derived(template ? [template.top, template.xsec].filter((x) => x.schematic) : []);
	let hidden = $state(new Set<string>());
	const layers = $derived(layersOf(scenes));
	const toggle = (l: string) => {
		const s = new Set(hidden);
		if (s.has(l)) s.delete(l);
		else s.add(l);
		hidden = s;
	};
	const mats = $derived.by(() => {
		const s = new Set<string>();
		for (const sc of scenes) for (const sh of sc.shapes) if (!sh.line) s.add(sh.mat);
		return [...s].filter((m) => MATERIALS[m]);
	});
	const badges = $derived.by(() => {
		const s = new Set<string>();
		for (const sc of scenes) {
			for (const m of sc.marks) if (m.dim.badge) s.add(m.dim.badge);
			for (const l of sc.labels) if (l.dim?.badge) s.add(l.dim.badge);
		}
		return BASIS_LEGEND.filter(([b]) => s.has(b));
	});
	const h = $derived(height || (compact ? 150 : 360));
	const main = $derived(!compact && !!layout && layout.views[0]?.kind !== 'xsec');
</script>

{#if layout?.not_drawn.length}
	<p class="undrawn">{layout.views.length ? 'Some views not drawn' : 'Not drawn'}: {layout.not_drawn.join('; ')}.</p>
{/if}
{#if undrawn.length}
	<p class="undrawn" data-tip={undrawn.flatMap((x) => x.notes).join('\n')}>{#if undrawn.length === 2}Not drawn: the source reports no dimension of this device's layout.{:else}{undrawn[0].view === 'top' ? 'Top view' : 'Cross-section'} not drawn: the source reports no dimension for it.{/if}</p>
{/if}
{#if scenes.length}
	<div class="lv" class:compact>
		{#if main}
			<div class="primary"><Scene scene={scenes[0]} height={Math.max(h, 460)} {hidden} /></div>
			{#if scenes.length > 1}
				<div class="views">
					{#each scenes.slice(1) as s}<Scene scene={s} height={320} {hidden} />{/each}
				</div>
			{/if}
		{:else}
			<div class="views">
				{#each scenes as s}<Scene scene={s} height={h} {compact} {hidden} />{/each}
			</div>
		{/if}
		<div class="legend">
			{#if layers.length}
				{#each layers as l}
					<button class="lay" class:off={hidden.has(l.layer)} onclick={() => toggle(l.layer)} data-tip="Show or hide this layer in every view"><i style:background="var(--m-{l.mat})"></i>{l.layer}</button>
				{/each}
			{:else}
				{#each mats as m}<span class="sw" data-tip={MATERIALS[m]}><i style:background="var(--m-{m})"></i>{MATERIALS[m]}</span>{/each}
			{/if}
			<span class="sw" data-tip={layout ? 'Not in the source: a drafting assumption, stated on hover' : 'Dimension not reported by the source: drawn at a fixed proportion of a reported neighbour, never labelled with a number'}><i class="dash"></i>{layout ? 'assumed' : 'not reported'}</span>
			{#each badges as [b, t]}<span class="sw" data-tip={t}><b class:meas={b === 'M'}>{b}</b>{compact ? '' : t}</span>{/each}
			{#if !layout && !compact}<span class="sw muted" data-tip="No source figures were read for this component: a generic drawing from its table values">template drawing</span>{/if}
		</div>
		{#if layout && !compact}
			<div class="prov">
				<span data-tip={layout.summary}>Drawn after {layout.sources.join(', ')}</span>
				{#if layout.checks.length}<span class="chk" data-tip={layout.checks.join('\n')}>{layout.checks.length} checks passed</span>{/if}
			</div>
		{/if}
	</div>
{/if}

<style>
	.lv { min-width: 0; }
	.undrawn { margin: 4px 0; font-size: 11px; color: var(--ink-3); }
	.primary { margin-bottom: 10px; }
	.views { display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 10px; }
	.compact .views { grid-template-columns: minmax(0, 1fr); gap: 4px; }
	.legend { display: flex; flex-wrap: wrap; align-items: center; gap: 2px 10px; margin-top: 4px; font-size: 10px; color: var(--ink-3); }
	.sw, .lay { display: inline-flex; align-items: center; gap: 4px; white-space: nowrap; }
	.lay { height: 16px; padding: 0 4px; font-size: 10px; color: var(--ink-2); background: transparent; border: 1px solid var(--grid); border-radius: 0; cursor: pointer; }
	.lay.off { color: var(--ink-3); opacity: 0.45; }
	.sw i, .lay i { display: inline-block; width: 10px; height: 8px; opacity: 0.85; }
	.sw i.dash { border: 1px dashed var(--warn); background: transparent; }
	.sw b { font: 700 9px var(--mono); color: var(--ink-2); }
	.sw b.meas { color: var(--accent); }
	.prov { display: flex; flex-wrap: wrap; gap: 2px 12px; margin-top: 4px; font-size: 10px; color: var(--ink-3); }
	.chk { color: var(--good); }
</style>
