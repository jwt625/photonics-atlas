<script lang="ts" generics="R">
	// Active filters as removable chips, for the page's filter bar (DevLog-013 D504).
	import { chipText, isActive, type Col, type Filters } from './filters';

	let { sets, onremove, onclear }: { sets: { columns: Col<any>[]; filters: Filters }[]; onremove: (set: number, key: string) => void; onclear: () => void } = $props();

	const items = $derived(
		sets.flatMap((s, i) =>
			s.columns.filter((c) => isActive(s.filters[c.key])).map((c) => ({ set: i, key: c.key, label: c.label, text: chipText(c, s.filters[c.key]) }))
		)
	);
</script>

{#if items.length}
	<div class="chips">
		{#each items as it (it.set + it.key)}
			<button class="chip" onclick={() => onremove(it.set, it.key)} data-tip={'Remove this filter\n' + it.label + ': ' + it.text}><span class="ct"><span class="k">{it.label}</span> {it.text}</span><span class="x">x</span></button>
		{/each}
		{#if items.length > 1}<button class="chip all" onclick={onclear} data-tip="Remove all filters">clear all</button>{/if}
	</div>
{/if}

<style>
	.chips { display: flex; flex-wrap: wrap; gap: 3px; padding: 3px 8px; background: var(--surface); border-bottom: 1px solid var(--border); min-width: 0; }
	.chip { display: inline-flex; align-items: center; gap: 4px; height: 18px; padding: 0 5px; font-size: 11px; max-width: min(320px, 100%); min-width: 0; border-color: var(--accent); background: transparent; }
	.ct { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
	.k { color: var(--ink-3); }
	.x { flex: none; color: var(--ink-2); }
	.chip.all { flex: none; border-color: var(--line); color: var(--ink-2); }
</style>
