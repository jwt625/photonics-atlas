<script lang="ts">
	// Foundry PDK benchmark (DevLog-014): one shared renderer with the standalone file (lib/benchmark/render.js).
	import { onMount } from 'svelte';
	import { getJson } from '../../lib/paths';
	import Preload from '../../lib/Preload.svelte';
	import { mountBenchmark } from '../../lib/benchmark/render.js';
	import type { BenchmarkView } from '../../lib/benchmark/render.js';
	import '../../lib/benchmark/benchmark.css';

	let el: HTMLDivElement | undefined = $state();
	let error = $state('');

	onMount(() => {
		let off = () => {};
		getJson<BenchmarkView>('data/benchmark.json')
			.then((v) => {
				if (el) off = mountBenchmark(el, v);
			})
			.catch((e) => (error = e instanceof Error ? e.message : String(e)));
		return () => off();
	});
</script>

<svelte:head><title>PDK benchmark | Photonics Atlas</title></svelte:head>
<Preload files={['data/benchmark.json']} />

{#if error}<div class="err">Could not load the benchmark: {error}</div>{/if}
<div class="bm" bind:this={el}></div>

<style>
	.err { padding: 12px; color: var(--crit); }
</style>
