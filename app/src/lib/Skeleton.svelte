<script lang="ts">
	// Placeholder while a page's data loads: part of the prerendered HTML, so it paints on first bytes.
	let { rows = 24 }: { rows?: number } = $props();
</script>

<div class="skel" role="status" aria-label="Loading">
	<div class="hd"></div>
	{#each { length: rows } as _}<div class="r"></div>{/each}
</div>

<style>
	.skel { height: 100%; overflow: hidden; padding: 8px 10px; background: var(--bg); }
	.hd { height: 24px; margin-bottom: 8px; background: var(--surface); border: 1px solid var(--border); }
	.r { height: 17px; margin-bottom: 5px; background: var(--grid); animation: pulse 1.2s ease-in-out infinite; }
	.r:nth-child(3n) { width: 86%; }
	.r:nth-child(5n) { width: 72%; }
	@keyframes pulse { 50% { opacity: 0.45; } }
</style>
