<script lang="ts">
	// Data the page will fetch, named in the prerendered HTML: the download starts while the HTML parses, before the app
	// code runs. Server-side only; once the app runs, its loaders start these themselves.
	import { browser } from '$app/env';
	import { dataUrl } from './paths';

	let { files }: { files: string[] } = $props();
</script>

<svelte:head>
	{#if !browser}
		{#each files as f}<link rel="preload" as="fetch" crossorigin="anonymous" href={dataUrl(f)} />{/each}
	{/if}
</svelte:head>
