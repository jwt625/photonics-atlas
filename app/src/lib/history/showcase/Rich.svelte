<script lang="ts">
	// Spec prose with sub / superscript markup: `_{...}` subscript, `^{...}` superscript (e.g. r_{33}, Cr^{3+}, O_{2}).
	// Everything else is literal, including plain underscores. Parser: markup() in plot.ts.
	import { markup } from './plot';

	let { text }: { text: string | number | null | undefined } = $props();
	const rs = $derived(markup(text == null ? '' : String(text)));
</script>

<!-- one inline wrapper: inside a flex container the runs stay one item (no stacked "Al / 2 / O / 3") -->
<span class="rich">{#each rs as r, i (i)}{#if r.k === 'sub'}<sub>{r.t}</sub>{:else if r.k === 'sup'}<sup>{r.t}</sup>{:else}{r.t}{/if}{/each}</span>

<style>
	.rich { display: inline; }
	sub, sup { font-size: 0.72em; line-height: 0; }
</style>
