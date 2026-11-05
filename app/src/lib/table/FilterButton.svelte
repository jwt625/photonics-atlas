<script lang="ts" generics="R">
	// A filter over something other than a table column (row-level filters of /components): a button with the same popover.
	import FilterPop from './FilterPop.svelte';
	import { isActive, type Col, type Filter } from './filters';

	let { col, rows, filter, onchange, tip }: { col: Col<R>; rows: R[]; filter: Filter | undefined; onchange: (f: Filter | null) => void; tip?: string } = $props();
	let btn: HTMLButtonElement | undefined = $state();
	let open = $state(false);
</script>

<button class="fbtn" class:act={isActive(filter)} bind:this={btn} onclick={() => (open = !open)} data-tip={tip}>{col.label}</button>
{#if open && btn}
	<FilterPop {col} {rows} {filter} anchor={btn} {onchange} onclose={() => (open = false)} />
{/if}

<style>
	.fbtn { flex: none; }
	.fbtn.act { border-color: var(--accent); color: var(--accent); }
</style>
