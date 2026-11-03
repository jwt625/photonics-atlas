<script module lang="ts">
	let hydrated = false;
</script>

<script lang="ts">
	// Data the page will fetch, named in the prerendered HTML: the download starts while the HTML parses, before the app
	// code runs. The links must survive hydration, because removing one cancels its download. Pages mounted later, by
	// client-side navigation, get no links: their loaders start the same fetches at once.
	import { onMount } from 'svelte';
	import { dataUrl } from './paths';

	let { files }: { files: string[] } = $props();
	const show = !hydrated;
	onMount(() => {
		hydrated = true;
	});
</script>

<svelte:head>
	{#if show}
		{#each files as f}<link rel="preload" as="fetch" crossorigin="anonymous" href={dataUrl(f)} />{/each}
	{/if}
</svelte:head>
